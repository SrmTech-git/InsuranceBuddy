# the actual Q&A interface

import logging
import os
import re
from dotenv import load_dotenv
import anthropic
from retrieve import query, find_form, list_all_forms
from abbreviations import expand_abbreviations
from states import STATE_MAP
from config import (
    GENERATION_MODEL,
    CHUNKS_PER_COLLECTION,
    CONTEXT_CAP,
    CLASSIFIER_MAX_TOKENS,
    ANSWER_MAX_TOKENS,
)

load_dotenv(override=True)

_api_key = os.getenv("ANTHROPIC_API_KEY")
if not _api_key:
    raise EnvironmentError(
        "ANTHROPIC_API_KEY is not set or is empty.\n"
        "Create a .env file in the project root with:\n"
        "  ANTHROPIC_API_KEY=sk-ant-..."
    )

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You're helping someone understand insurance documents — usually Ohio-specific regulatory and educational material. Insurance is genuinely complicated, and people often come to this with real decisions on the line, so accuracy matters more than completeness.

How to answer:
- Use only the provided context. If the answer isn't there, say "I don't have enough information in the provided documents to answer that question." A clear "I don't know" is more useful than a guess.
- Quote specific sections when it helps support the answer.
- Always tell the user which document the information came from — form number, edition date, or filename from the chunk metadata.
- Keep it clear and concise. People reading insurance answers are usually already overwhelmed.

Thank you for your attention."""

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    """Lazy-instantiate the Anthropic client so importing this module
    doesn't require a working API key (only calling ask() does)."""
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client

# ---------------------------------------------------------------------------
# Collection registry — add new collections here as they are created.
# The descriptions are passed directly to the Haiku classifier, so write
# them to be distinct and specific about what each collection contains.
# ---------------------------------------------------------------------------

COLLECTION_REGISTRY: dict[str, str] = {
    "regulatory": "state statutes and administrative code (e.g. Ohio ORC/OAC), compliance requirements, filing rules, penalties, legal limits",
    "educational": "conceptual explanations of insurance products, coverage types, and industry terms",
    "forms": "insurance forms and document templates — declarations pages, applications, endorsements, certificates of insurance, ACORD/ISO forms, and state-required notice forms",
}

# Known form-number prefixes across collections.
# - ORC/OAC: regulatory (Ohio statutes / admin code) — stored without
#   spaces (e.g. "ORC3937.18", "OAC3901-1-54")
# - ACORD: forms (industry-standard ACORD forms) — stored with a
#   single space (e.g. "ACORD 25", "ACORD 50WM")
# detect_form_number normalizes user queries to match the stored format
# of whichever prefix it sees.
_KNOWN_PREFIXES = ("ORC", "OAC", "ACORD")


# ---------------------------------------------------------------------------
# Query classification
# ---------------------------------------------------------------------------

def detect_form_numbers(text: str) -> list[str]:
    """Return ALL normalized form numbers found in the query, in order, deduped.

    Returns an empty list if none are present. Use this when a query may
    reference multiple forms (e.g. "What's the difference between ACORD 24
    and ACORD 28?"). For single-form-or-none cases, detect_form_number is
    a thin wrapper that returns the first match.

    Normalization matches how each prefix is stored in metadata:
    - ORC/OAC strip spaces ("ORC 3937.18" -> "ORC3937.18")
    - ACORD preserves a single space ("ACORD25" or "acord 25" -> "ACORD 25")

    The regex allows an alphabetic suffix after the digits to handle
    ACORD forms like 50WM, 60US, 64US.
    """
    prefixes = "|".join(_KNOWN_PREFIXES)
    raw_matches = re.findall(
        rf"\b((?:{prefixes})\s*\d+[A-Z]*(?:[.\-]\d+)*)\b", text, re.IGNORECASE
    )
    seen: set[str] = set()
    result: list[str] = []
    for raw_match in raw_matches:
        raw = raw_match.strip().upper()
        if raw.startswith("ACORD"):
            normalized = f"ACORD {raw[5:].lstrip()}"
        else:
            normalized = raw.replace(" ", "")
        if normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def detect_form_number(text: str) -> str | None:
    """Return the first normalized form number in the query, or None.

    Thin wrapper over detect_form_numbers — use this when only the first
    match matters. Most callers should use detect_form_numbers to handle
    multi-form comparison queries cleanly.
    """
    forms = detect_form_numbers(text)
    return forms[0] if forms else None


def detect_bare_section(text: str) -> str | None:
    """Return a bare section number if the query contains one (no prefix), else None.

    Matches patterns like 4509.51, 3937.18, 3901-1-54 — Ohio code formats
    that use dot or dash separators. Single bare integers are ignored to
    avoid false positives on random numbers.
    """
    match = re.search(r"\b(\d+(?:[.\-]\d+)+)\b", text)
    if not match:
        return None
    return match.group(1)


def is_inventory_query(text: str) -> bool:
    """Return True if the user is asking what forms/documents are available."""
    patterns = [
        r"what\s+(forms?|documents?)\s+(do\s+)?(we|you|I)\s+have",
        r"list\s+(all\s+)?(forms?|documents?)",
        r"what\s+do\s+we\s+have",
        r"show\s+(me\s+)?(all\s+)?(forms?|documents?)",
        r"which\s+(forms?|documents?)",
    ]
    lower = text.lower()
    return any(re.search(p, lower) for p in patterns)


def _llm_classify(question: str) -> list[str]:
    """Call Haiku to determine which collection(s) to search.

    Returns a list of one or more collection names from COLLECTION_REGISTRY.
    Falls back to ["regulatory"] if the response can't be parsed.
    """
    collection_lines = "\n".join(
        f"- {name}: {desc}" for name, desc in COLLECTION_REGISTRY.items()
    )
    prompt = (
        f"You route insurance queries to the correct document collection(s).\n\n"
        f"Available collections:\n{collection_lines}\n\n"
        f"Routing rules:\n"
        f"- Questions about whether coverage is REQUIRED, mandatory, or legally necessary -> regulatory\n"
        f"- Questions about legal limits, penalties, or state-specific rules and statutes -> regulatory\n"
        f"- Questions about what a coverage type IS, how it works, or general concepts -> educational\n"
        f"- Questions about what a specific FORM contains, what a dec page includes, or how a particular document is structured -> forms\n"
        f"- When in doubt, include all relevant collections.\n\n"
        f"This routing helps surface the right information for someone trying to "
        f"understand insurance, which is genuinely complicated. Thank you for your attention.\n\n"
        f"Reply with only the collection name(s) needed, comma-separated if multiple.\n"
        f'Examples: "regulatory" | "educational" | "regulatory, educational"\n\n'
        f"Query: {question}"
    )
    response = _get_client().messages.create(
        model=GENERATION_MODEL,
        max_tokens=CLASSIFIER_MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip().lower()
    valid = set(COLLECTION_REGISTRY.keys())
    result = [token.strip().rstrip(".") for token in raw.split(",")]
    result = [c for c in result if c in valid]
    # Safer fallback: if the LLM mangles the response, search every
    # collection rather than guessing one. Re-ranking sorts it out.
    return result if result else list(COLLECTION_REGISTRY.keys())


def detect_collection(text: str) -> list[str]:
    """Return which collection(s) to search for this query.

    Comparison queries (vs, compare, difference between) always get all
    collections via fast regex. Everything else is routed by Haiku so that
    routing stays correct as new collections are added.
    """
    comparison_patterns = [r"\bdifference\s+between\b", r"\bcompare\b", r"\bvs\.?\b"]
    if any(re.search(p, text, re.IGNORECASE) for p in comparison_patterns):
        return list(COLLECTION_REGISTRY.keys())
    return _llm_classify(text)


# ---------------------------------------------------------------------------
# State detection
# ---------------------------------------------------------------------------

# State name → code maps derived from the single source of truth in states.py.
# Full state names matched case-insensitively; abbreviations uppercase-only
# (avoids false positives on common words like "in", "oh", "ia").
_STATE_NAME_MAP: dict[str, str] = STATE_MAP
_STATE_ABBR_MAP: dict[str, str] = {v: v for v in STATE_MAP.values()}


def detect_states(text: str) -> list[str]:
    """Return sorted list of state codes mentioned in the query.

    Matches full state names (case-insensitive) and uppercase abbreviations
    (e.g. OH, IN) as standalone words. Short abbreviations are only matched
    uppercase to avoid false positives on common words.
    """
    found: set[str] = set()

    for name, code in _STATE_NAME_MAP.items():
        if re.search(rf"\b{re.escape(name)}\b", text, re.IGNORECASE):
            found.add(code)

    for abbr, code in _STATE_ABBR_MAP.items():
        if re.search(rf"\b{abbr}\b", text):  # case-sensitive — uppercase only
            found.add(code)

    return sorted(found)


def _build_state_filter(states: list[str]) -> dict | None:
    """Build a ChromaDB where-clause for one or more state codes."""
    if not states:
        return None
    if len(states) == 1:
        return {"state": states[0]}
    return {"$or": [{"state": s} for s in states]}


def _merge_filters(*filters: dict | None) -> dict | None:
    """AND together multiple ChromaDB filter dicts, ignoring None values."""
    active = [f for f in filters if f]
    if not active:
        return None
    if len(active) == 1:
        return active[0]
    return {"$and": active}


# ---------------------------------------------------------------------------
# ask() helpers
# ---------------------------------------------------------------------------

def _handle_inventory(question: str, collections: list[str]) -> str | None:
    """Return a formatted inventory listing if this is an inventory query, else None."""
    if not is_inventory_query(question):
        return None

    lines: list[str] = ["Here are the documents currently in the database:\n"]
    any_found = False

    for coll in collections:
        forms = list_all_forms(coll)
        if not forms:
            continue
        any_found = True
        lines.append(f"[ {coll} ]\n")
        for f in forms:
            label = f["form_number"] or "(no form number)"
            lines.append(f"  {label}")
            lines.append(f"    Edition:     {f['edition_date'] or '(none)'}")
            lines.append(f"    Description: {f['description'] or '(none)'}")
            lines.append(f"    Chunks:      {f['chunk_count']}")
            lines.append("")

    if not any_found:
        return "There are no documents in the database yet."
    return "\n".join(lines)


def _resolve_form_filter(question: str) -> tuple[dict | None, str | None, str | None]:
    """If the question names form numbers, locate them and return routing info.

    Multi-form comparison queries (e.g. "What's the difference between
    ACORD 24 and ACORD 28?") return an $or filter over all detected forms,
    scoped to the single collection they share. If detected forms span
    multiple collections, falls through to semantic search so the
    comparison fast-path can handle it.

    Returns:
        (filters, collection_name, None)  — form(s) found; use these for retrieval
        (None, None, None)                — no form number, OR cross-collection,
                                             OR detected forms not found in DB
    """
    form_numbers = detect_form_numbers(question)

    # Fallback: try bare section numbers with known prefixes (single only).
    if not form_numbers:
        bare = detect_bare_section(question)
        if bare:
            for prefix in _KNOWN_PREFIXES:
                candidate = f"{prefix}{bare}"
                for coll in COLLECTION_REGISTRY:
                    if find_form(candidate, coll):
                        form_numbers = [candidate]
                        logger.info("Resolved bare section %s -> %s", bare, candidate)
                        break
                if form_numbers:
                    break

    if not form_numbers:
        return None, None, None

    # Map each detected form to the first collection where it exists.
    # Forms not found in any collection are silently dropped — they'd have
    # no chunks to retrieve anyway.
    found_in: dict[str, str] = {}
    for fn in form_numbers:
        for coll in COLLECTION_REGISTRY:
            if find_form(fn, coll):
                found_in[fn] = coll
                break

    if not found_in:
        logger.info("No detected forms found in DB (%s) — falling back to semantic search",
                    ", ".join(form_numbers))
        return None, None, None

    # If forms span multiple collections, fall through. The cross-collection
    # re-ranker will pull relevant chunks via semantic search.
    collections = set(found_in.values())
    if len(collections) > 1:
        logger.info("Forms span multiple collections (%s) — falling back to semantic search",
                    ", ".join(sorted(collections)))
        return None, None, None

    collection_name = next(iter(collections))
    matched_forms = list(found_in.keys())

    if len(matched_forms) == 1:
        filters: dict = {"form_number": matched_forms[0]}
    else:
        filters = {"$or": [{"form_number": fn} for fn in matched_forms]}

    logger.info("Searching %s: %s", collection_name, ", ".join(matched_forms))
    return filters, collection_name, None


def _retrieve_chunks(
    question: str,
    collections: list[str],
    filters: dict | None,
) -> tuple[list[str], list[dict], list[str]]:
    """Query each collection, merge results, re-rank by L2 distance, return top CONTEXT_CAP."""
    all_docs: list[str] = []
    all_metas: list[dict] = []
    all_labels: list[str] = []
    all_distances: list[float] = []

    for coll in collections:
        try:
            result = query(question, n_results=CHUNKS_PER_COLLECTION, filters=filters, collection_name=coll)
            all_docs.extend(result.documents)
            all_metas.extend(result.metadatas)
            all_labels.extend([coll] * len(result))
            all_distances.extend(result.distances)
        except Exception as e:
            # Don't kill the whole query if one collection misbehaves —
            # but make the failure visible so it can be diagnosed.
            logger.warning("Query failed for collection %r: %s", coll, e)
            continue

    if not all_docs:
        return [], [], []

    # Sort by L2 distance ascending (lower = more relevant), keep top CONTEXT_CAP
    ranked = sorted(
        zip(all_distances, all_docs, all_metas, all_labels),
        key=lambda x: x[0],
    )[:CONTEXT_CAP]

    _, documents, metadatas, labels = zip(*ranked)
    return list(documents), list(metadatas), list(labels)


def _build_context(
    documents: list[str],
    metadatas: list[dict],
    labels: list[str],
) -> tuple[str, str]:
    """Format retrieved chunks into an LLM-ready context block and a sources summary.

    Returns (context, sources_str).
    """
    context_parts: list[str] = []
    sources: set[str] = set()

    for i, (doc, meta, coll_label) in enumerate(zip(documents, metadatas, labels)):
        form = meta.get("form_number", "")
        edition = meta.get("edition_date", "")
        desc = meta.get("description", "")
        source = form or desc or meta.get("filename", "unknown")
        source_label = f"{source} ({edition})" if edition else source

        context_parts.append(
            f"[Chunk {i + 1} — Collection: {coll_label} — Source: {source_label}]:\n{doc}"
        )
        sources.add(f"[{coll_label}] {source_label}")

    context = "\n\n---\n\n".join(context_parts)
    sources_str = ", ".join(sorted(sources))
    return context, sources_str


def _call_llm(question: str, context: str, sources_str: str, collections_searched: str) -> str:
    """Send the question and retrieved context to Claude and return the answer."""
    user_message = (
        f"Context from insurance documents (searched: {collections_searched}):\n\n"
        f"{context}\n\n"
        f"Sources available: {sources_str}\n\n"
        f"Question: {question}"
    )

    response = _get_client().messages.create(
        model=GENERATION_MODEL,
        max_tokens=ANSWER_MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def ask(question: str) -> str:
    """Classify the query, retrieve relevant context, and return an answer."""
    question = expand_abbreviations(question)
    collections = detect_collection(question)

    inventory_response = _handle_inventory(question, collections)
    if inventory_response is not None:
        return inventory_response

    filters, form_collection, error = _resolve_form_filter(question)
    if error:
        return error
    if form_collection:
        collections = [form_collection]

    # Detect states and combine with any form-number filter
    states = detect_states(question)
    state_filter = _build_state_filter(states)
    combined_filters = _merge_filters(filters, state_filter)

    documents, metadatas, labels = _retrieve_chunks(question, collections, combined_filters)

    if not documents:
        return "No relevant results found in the database."

    context, sources_str = _build_context(documents, metadatas, labels)
    return _call_llm(question, context, sources_str, " + ".join(collections))


# ---------------------------------------------------------------------------
# Demo / testing
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Insurance Document Assistant (type 'quit' to exit)\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() == "quit":
            print("Goodbye!")
            break

        print(f"\n{ask(question)}\n")
