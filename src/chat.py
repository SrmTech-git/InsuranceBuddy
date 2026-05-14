# the actual Q&A interface

import logging
import os
import re
from dataclasses import dataclass, field
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


@dataclass
class AskTrace:
    """Structured result from ask_traced() — answer plus pipeline state.

    Used by the eval framework (and any other caller that needs visibility
    into routing/retrieval decisions). For chat use, prefer the plain ask()
    wrapper.
    """
    question: str
    answer: str
    collections_searched: list[str]
    intent: str
    detected_forms: list[str]
    detected_states: list[str]
    retrieved_sources: list[dict] = field(default_factory=list)

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


def strip_form_context_prefix(question: str) -> str:
    """Strip leading form-reference clauses from a query.

    Used when the router has classified a form as CONTEXT (not subject),
    meaning the form is mentioned only as backdrop for a conceptual
    question. Without stripping, the LLM sees the form name in the
    question and can refuse on literalism grounds even when relevant
    conceptual content was retrieved.

    Strips patterns like:
        "Per ACORD 25 standards, what is GL?"   -> "what is GL?"
        "Under ORC 3937.18, what is UM?"         -> "what is UM?"
        "According to ACORD 25, explain..."      -> "explain..."

    Only strips when the form reference appears at the BEGINNING of the
    query (after optional whitespace). Mid-sentence form references are
    left alone since they may carry semantic weight the LLM needs.
    """
    prefixes = "|".join(_KNOWN_PREFIXES)
    # Connector words that introduce a form-context clause
    connectors = (
        r"(?:per|under|according\s+to|in|using|on|with|based\s+on|via|"
        r"as\s+(?:described|defined|outlined|stated)\s+in|"
        r"from|by|in\s+accordance\s+with)"
    )
    pattern = (
        rf"^\s*{connectors}\s+"
        rf"(?:the\s+)?"
        rf"(?:{prefixes})\s*\d+[A-Z]*(?:[.\-]\d+)*"
        rf"(?:\s+(?:standards?|form|rules?|guidelines?|requirements?))?"
        rf"[\s,;:\-]*"
    )
    cleaned = re.sub(pattern, "", question, count=1, flags=re.IGNORECASE).strip()
    # Capitalize the first letter if the strip left a lowercase question
    if cleaned and cleaned[0].islower():
        cleaned = cleaned[0].upper() + cleaned[1:]
    return cleaned if cleaned else question


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


def _parse_route_response(raw: str, detected_forms: list[str] | None = None) -> tuple[list[str], str]:
    """Parse the LLM router's "<collections> | <intent>" response.

    Robust against malformed responses — falls back to all collections if
    the routing part is unparseable, and to "none" intent (or "subject" if
    forms were detected) if the intent part is unparseable.

    Returns (collections, intent) where intent is "subject", "context", or
    "none".
    """
    valid_colls = set(COLLECTION_REGISTRY.keys())
    valid_intents = {"subject", "context", "none"}

    raw = raw.strip().lower()
    if "|" in raw:
        coll_part, intent_part = raw.split("|", 1)
    else:
        coll_part, intent_part = raw, "none"

    collections = [c.strip().rstrip(".") for c in coll_part.split(",")]
    collections = [c for c in collections if c in valid_colls]

    intent = intent_part.strip().rstrip(".")
    if intent not in valid_intents:
        intent = "none"

    # Fallback if LLM mangled the routing — search broadly rather than guess
    if not collections:
        collections = list(COLLECTION_REGISTRY.keys())

    # If forms were detected but intent didn't classify them, default to
    # "subject" so the form filter still applies. This preserves the prior
    # behavior — we never get worse than before this change.
    if detected_forms and intent == "none":
        intent = "subject"

    return collections, intent


def _llm_route(question: str, detected_forms: list[str] | None = None) -> tuple[list[str], str]:
    """Call Haiku to classify the query along two dimensions in one shot:

    1. Which collection(s) to search
    2. If forms are mentioned, whether they're the SUBJECT of the query
       or just CONTEXT for a conceptual question

    Returns (collections, intent). See _parse_route_response for shape.
    """
    collection_lines = "\n".join(
        f"- {name}: {desc}" for name, desc in COLLECTION_REGISTRY.items()
    )

    if detected_forms:
        forms_block = (
            f"\nForms mentioned in this query: {', '.join(detected_forms)}\n"
            f"Decide whether the user is asking ABOUT these forms (subject) "
            f"or whether they're mentioned as context for a conceptual question (context):\n"
            f"  - subject: \"What does ACORD 25 contain?\", \"Show me ACORD 130\"\n"
            f"  - context: \"Per ACORD 25 standards, what is general liability?\", "
            f"\"Under ORC 3937.18, what is UM coverage?\"\n"
        )
        intent_label = "subject | context"
    else:
        forms_block = ""
        intent_label = "none"

    prompt = (
        f"You classify insurance queries on two dimensions: which "
        f"collection(s) to search, and form intent (when forms are mentioned).\n\n"
        f"Available collections:\n{collection_lines}\n\n"
        f"Routing rules:\n"
        f"- A query can name MULTIPLE collections (comma-separated) when its answer spans them. Prefer including educational alongside forms or regulatory whenever the question is conceptual (\"what is...\", \"what does X cover\", \"how does X work\") even if it names a form or statute.\n"
        f"- Pure form-content lookup (\"show me ACORD 25\", \"what fields are on ACORD 130\") -> forms only\n"
        f"- Pure statute lookup (\"what does ORC 3937.18 say\") -> regulatory only\n"
        f"- Conceptual question that happens to mention a form (\"what is CG 20 10?\", \"what's in a dec package?\") -> forms, educational\n"
        f"- Conceptual question that happens to mention a statute or legal duty (\"what is late notice\", \"does the law require cooperation\") -> regulatory, educational (or just educational if no state is mentioned)\n"
        f"- Pure concept with no form or statute reference (\"what is general liability\") -> educational\n"
        f"- When unsure, include educational.\n"
        f"{forms_block}\n"
        f"This routing helps surface the right information for someone trying to "
        f"understand insurance, which is genuinely complicated. Thank you for your attention.\n\n"
        f"Reply on ONE line in this exact format:\n"
        f"<collection>[, <collection>...] | <intent>\n"
        f"where intent is one of: {intent_label}\n\n"
        f"Examples:\n"
        f"  regulatory | none\n"
        f"  forms | subject\n"
        f"  educational | none\n"
        f"  educational | context\n"
        f"  forms, educational | subject\n"
        f"  regulatory, educational | none\n"
        f"  forms, regulatory | subject\n\n"
        f"Query: {question}"
    )
    response = _get_client().messages.create(
        model=GENERATION_MODEL,
        max_tokens=CLASSIFIER_MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )
    return _parse_route_response(response.content[0].text, detected_forms)


def detect_collection(text: str, detected_forms: list[str] | None = None) -> tuple[list[str], str]:
    """Return (collections, form_intent) for this query.

    Comparison queries (vs, compare, difference between) always get all
    collections via fast regex; intent defaults to "subject" when forms
    are detected so the form filter still applies. Everything else is
    routed by Haiku, which also classifies the form intent.
    """
    comparison_patterns = [r"\bdifference\s+between\b", r"\bcompare\b", r"\bvs\.?\b"]
    if any(re.search(p, text, re.IGNORECASE) for p in comparison_patterns):
        intent = "subject" if detected_forms else "none"
        return list(COLLECTION_REGISTRY.keys()), intent
    return _llm_route(text, detected_forms)


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
    """Build a ChromaDB where-clause for one or more state codes.

    Always includes state="" alongside the detected states so that
    untagged content (educational concepts, industry-general forms) is
    not filtered out of state-scoped queries. The state filter narrows
    *state-tagged* content to the relevant state(s) without sweeping
    away the conceptual layer.
    """
    if not states:
        return None
    options = [{"state": s} for s in states] + [{"state": ""}]
    return {"$or": options}


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


def _resolve_form_filter(question: str) -> tuple[dict | None, list[str] | None, str | None]:
    """If the question names form numbers, locate them and return routing info.

    Single-form / single-collection: scope retrieval to that collection.
    Multi-form same-collection: $or filter scoped to the shared collection.
    Multi-form cross-collection: $or filter spanning the relevant collections.
        Each chunk's form_number metadata only matches one $or branch, so
        chunks from each collection are correctly filtered while semantic
        search still operates broadly.

    Returns:
        (filters, collections_list, None)  — form(s) found; use these for retrieval
        (None, None, None)                  — no form number OR detected forms
                                              not found in DB
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

    matched_forms = list(found_in.keys())
    collections = sorted(set(found_in.values()))  # deterministic order

    if len(matched_forms) == 1:
        filters: dict = {"form_number": matched_forms[0]}
    else:
        filters = {"$or": [{"form_number": fn} for fn in matched_forms]}

    logger.info("Searching %s: %s", " + ".join(collections), ", ".join(matched_forms))
    return filters, collections, None


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


def _retrieve_chunks_multistate(
    question: str,
    collections: list[str],
    base_filters: dict | None,
    states: list[str],
) -> tuple[list[str], list[dict], list[str]]:
    """Multi-state retrieval with per-state balance.

    When the query mentions 2+ states, a single OR-filtered query lets
    the semantically-richer state dominate the top results (e.g. Ohio's
    detailed ORC chapters squeeze out Indiana's sparser content). To
    ensure each state gets representation, run a separate per-state
    query for each state, plus a state-agnostic query to surface
    untagged content (educational concepts).

    Results are merged and re-ranked by L2 distance, then capped at
    CONTEXT_CAP — so the final ranking is still distance-based but each
    state had a fair shot at contributing candidates.
    """
    # Budget per call — leave room for the state-agnostic pull too
    per_call = max(2, CHUNKS_PER_COLLECTION // (len(states) + 1))

    all_docs: list[str] = []
    all_metas: list[dict] = []
    all_labels: list[str] = []
    all_distances: list[float] = []

    def _run(filters: dict | None) -> None:
        for coll in collections:
            try:
                result = query(question, n_results=per_call, filters=filters, collection_name=coll)
                all_docs.extend(result.documents)
                all_metas.extend(result.metadatas)
                all_labels.extend([coll] * len(result))
                all_distances.extend(result.distances)
            except Exception as e:
                logger.warning("Multi-state query failed (%s): %s", coll, e)

    # Per-state pulls — each state gets its own quota
    for state in states:
        state_only = {"$or": [{"state": state}, {"state": ""}]}
        _run(_merge_filters(base_filters, state_only))

    # State-agnostic pull — catches untagged content if it ranked weakly
    # against the per-state filtered pools
    untagged_only = {"state": ""}
    _run(_merge_filters(base_filters, untagged_only))

    if not all_docs:
        return [], [], []

    # Deduplicate while preserving lowest distance — chunks can show up
    # in multiple per-state pulls if state="" matched
    seen: dict[str, int] = {}  # chunk text -> index into lists
    for i, doc in enumerate(all_docs):
        if doc in seen:
            existing = seen[doc]
            if all_distances[i] < all_distances[existing]:
                seen[doc] = i
        else:
            seen[doc] = i

    indices = sorted(seen.values(), key=lambda i: all_distances[i])[:CONTEXT_CAP]
    return (
        [all_docs[i] for i in indices],
        [all_metas[i] for i in indices],
        [all_labels[i] for i in indices],
    )


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
    return ask_traced(question).answer


def ask_traced(question: str) -> AskTrace:
    """Like ask() but returns the full pipeline trace alongside the answer.

    Used by the eval framework to score routing, retrieval, and content
    correctness. The trace captures the router's decisions, what forms
    and states were detected, and which source documents were retrieved.
    """
    expanded = expand_abbreviations(question)
    detected_forms = detect_form_numbers(expanded)
    collections, intent = detect_collection(expanded, detected_forms)
    states = detect_states(expanded)

    inventory_response = _handle_inventory(expanded, collections)
    if inventory_response is not None:
        return AskTrace(
            question=question,
            answer=inventory_response,
            collections_searched=collections,
            intent=intent,
            detected_forms=detected_forms,
            detected_states=states,
            retrieved_sources=[],
        )

    # Apply the form filter only when the LLM classifier judged the forms
    # are the subject of the query. When the intent is "context" (forms
    # mentioned in passing for a conceptual question), skip the filter so
    # semantic search can find the conceptual content.
    if intent == "context":
        filters: dict | None = None
        form_collections: list[str] | None = None
        logger.info("Form intent is context — skipping form filter")
    else:
        filters, form_collections, error = _resolve_form_filter(expanded)
        if error:
            return AskTrace(
                question=question,
                answer=error,
                collections_searched=collections,
                intent=intent,
                detected_forms=detected_forms,
                detected_states=states,
                retrieved_sources=[],
            )

    if form_collections:
        collections = form_collections

    # For multi-state queries, use balanced per-state retrieval so one
    # semantically-rich state doesn't squeeze out the others. Single-state
    # and stateless queries take the normal path.
    if len(states) >= 2:
        documents, metadatas, labels = _retrieve_chunks_multistate(
            expanded, collections, filters, states
        )
    else:
        state_filter = _build_state_filter(states)
        combined_filters = _merge_filters(filters, state_filter)
        documents, metadatas, labels = _retrieve_chunks(expanded, collections, combined_filters)

    if not documents:
        return AskTrace(
            question=question,
            answer="No relevant results found in the database.",
            collections_searched=collections,
            intent=intent,
            detected_forms=detected_forms,
            detected_states=states,
            retrieved_sources=[],
        )

    context, sources_str = _build_context(documents, metadatas, labels)

    # When the form was mentioned only as context for a conceptual question,
    # strip the form-reference prefix before sending to the LLM. Retrieval
    # used the original query (so the form keyword still helped semantic
    # match), but the LLM otherwise refuses on literalism grounds — "Per
    # ACORD 25 standards, what is GL?" -> the LLM doesn't find anything
    # titled "ACORD 25 standards" and declines, even when the right
    # educational chunks are right there in context.
    if intent == "context" and detected_forms:
        llm_query = strip_form_context_prefix(expanded)
        if llm_query != expanded:
            logger.info(f"Stripped form-context prefix for LLM: {llm_query!r}")
    else:
        llm_query = expanded

    answer = _call_llm(llm_query, context, sources_str, " + ".join(collections))

    # Capture per-chunk source info — used by eval scoring
    retrieved_sources = [
        {
            "filename": m.get("filename", ""),
            "form_number": m.get("form_number", ""),
            "description": m.get("description", ""),
            "state": m.get("state", ""),
            "collection": label,
        }
        for m, label in zip(metadatas, labels)
    ]

    return AskTrace(
        question=question,
        answer=answer,
        collections_searched=collections,
        intent=intent,
        detected_forms=detected_forms,
        detected_states=states,
        retrieved_sources=retrieved_sources,
    )


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
