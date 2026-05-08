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
}

# Known form-number prefixes in the regulatory collection.
# Used to resolve bare section numbers like "4509.51" -> "ORC4509.51".
_KNOWN_PREFIXES = ("ORC", "OAC")


# ---------------------------------------------------------------------------
# Query classification
# ---------------------------------------------------------------------------

def detect_form_number(text: str) -> str | None:
    """Return a normalized form number if the query contains one, else None."""
    # Only match known prefixes (ORC, OAC) to avoid false positives on
    # common English words like "does", "can", "from", "code", etc.
    prefixes = "|".join(_KNOWN_PREFIXES)
    match = re.search(
        rf"\b((?:{prefixes})\s?\d+(?:[.\-]\d+)*)\b", text, re.IGNORECASE
    )
    if not match:
        return None
    # Normalize: uppercase and collapse any spaces (e.g. "ORC 3937.18" -> "ORC3937.18")
    return match.group(1).upper().replace(" ", "")


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
    """If the question names a form number, locate it and return routing info.

    Returns:
        (filters, collection_name, None)  — form found; use these for retrieval
        (None, None, error_message)       — form named but not in the database
        (None, None, None)                — no form number in the question
    """
    form_number = detect_form_number(question)

    # Fallback: try bare section numbers with known prefixes
    if not form_number:
        bare = detect_bare_section(question)
        if bare:
            for prefix in _KNOWN_PREFIXES:
                candidate = f"{prefix}{bare}"
                for coll in COLLECTION_REGISTRY:
                    if find_form(candidate, coll):
                        form_number = candidate
                        logger.info("Resolved bare section %s -> %s", bare, candidate)
                        break
                if form_number:
                    break

    if not form_number:
        return None, None, None

    # Search every registered collection — adding a new one to
    # COLLECTION_REGISTRY automatically extends form-number lookup.
    collection_name = next(
        (coll for coll in COLLECTION_REGISTRY if find_form(form_number, coll)),
        None,
    )

    if collection_name is None:
        # Form number not found — fall through to semantic search
        # instead of hard-failing, since the query text itself is still useful.
        logger.info("Form %s not found — falling back to semantic search", form_number)
        return None, None, None

    logger.info("Searching %s: %s", collection_name, form_number)
    return {"form_number": form_number}, collection_name, None


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
