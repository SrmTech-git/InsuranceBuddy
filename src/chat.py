# chat.py — orchestrates a question through the pipeline:
#   abbreviation expand → route → retrieve → format → LLM → answer
#
# This module is the high-level orchestrator. Subcomponents live in:
#   - router.py        — collection + form-intent classification (Haiku)
#   - query_parsing.py — pure regex helpers (forms, states, inventory)
#   - retrieve.py      — ChromaDB queries + cross-collection re-ranking
#   - abbreviations.py — insurance abbreviation expansion

import logging
from dataclasses import dataclass, field
from dotenv import load_dotenv

from retrieve import find_form, list_all_forms, retrieve_chunks, retrieve_chunks_multistate
from abbreviations import expand_abbreviations
from router import COLLECTION_REGISTRY, detect_collection, _get_client
from query_parsing import (
    KNOWN_PREFIXES,
    detect_form_numbers,
    detect_bare_section,
    strip_form_context_prefix,
    is_inventory_query,
    detect_states,
    build_state_filter,
    merge_filters,
)
from config import GENERATION_MODEL, ANSWER_MAX_TOKENS


load_dotenv(override=True)
logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You're helping someone understand insurance documents — usually Ohio-specific regulatory and educational material. Insurance is genuinely complicated, and people often come to this with real decisions on the line, so accuracy matters more than completeness.

How to answer:
- Use only the provided context. If the answer isn't there, say "I don't have enough information in the provided documents to answer that question." A clear "I don't know" is more useful than a guess.
- Quote specific sections when it helps support the answer.
- Always tell the user which document the information came from — form number, edition date, or filename from the chunk metadata.
- Keep it clear and concise. People reading insurance answers are usually already overwhelmed.

Thank you for your attention."""


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


def _resolve_form_filter(question: str) -> tuple[dict | None, list[str] | None]:
    """If the question names form numbers, locate them and return routing info.

    Single-form / single-collection: scope retrieval to that collection.
    Multi-form same-collection: $or filter scoped to the shared collection.
    Multi-form cross-collection: $or filter spanning the relevant collections.
        Each chunk's form_number metadata only matches one $or branch, so
        chunks from each collection are correctly filtered while semantic
        search still operates broadly.

    Returns:
        (filters, collections_list)  — form(s) found; use these for retrieval
        (None, None)                 — no form number OR detected forms
                                       not found in DB
    """
    form_numbers = detect_form_numbers(question)

    # Fallback: try bare section numbers with known prefixes (single only).
    if not form_numbers:
        bare = detect_bare_section(question)
        if bare:
            for prefix in KNOWN_PREFIXES:
                candidate = f"{prefix}{bare}"
                for coll in COLLECTION_REGISTRY:
                    if find_form(candidate, coll):
                        form_numbers = [candidate]
                        logger.info("Resolved bare section %s -> %s", bare, candidate)
                        break
                if form_numbers:
                    break

    if not form_numbers:
        return None, None

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
        return None, None

    matched_forms = list(found_in.keys())
    collections = sorted(set(found_in.values()))  # deterministic order

    if len(matched_forms) == 1:
        filters: dict = {"form_number": matched_forms[0]}
    else:
        filters = {"$or": [{"form_number": fn} for fn in matched_forms]}

    logger.info("Searching %s: %s", " + ".join(collections), ", ".join(matched_forms))
    return filters, collections


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
        temperature=0,  # grounded answers should be deterministic and faithful to context
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

    # Build the trace up-front with everything we know; fill in answer and
    # retrieved_sources at whichever exit point we reach.
    trace = AskTrace(
        question=question,
        answer="",
        collections_searched=collections,
        intent=intent,
        detected_forms=detected_forms,
        detected_states=states,
    )

    inventory_response = _handle_inventory(expanded, collections)
    if inventory_response is not None:
        trace.answer = inventory_response
        return trace

    # Apply the form filter only when the LLM classifier judged the forms
    # are the subject of the query. When the intent is "context" (forms
    # mentioned in passing for a conceptual question), skip the filter so
    # semantic search can find the conceptual content.
    if intent == "context":
        filters: dict | None = None
        form_collections: list[str] | None = None
        logger.info("Form intent is context — skipping form filter")
    else:
        filters, form_collections = _resolve_form_filter(expanded)

    if form_collections:
        collections = form_collections
        trace.collections_searched = collections

    # For multi-state queries, use balanced per-state retrieval so one
    # semantically-rich state doesn't squeeze out the others. Single-state
    # and stateless queries take the normal path.
    if len(states) >= 2:
        documents, metadatas, labels = retrieve_chunks_multistate(
            expanded, collections, filters, states
        )
    else:
        state_filter = build_state_filter(states)
        combined_filters = merge_filters(filters, state_filter)
        documents, metadatas, labels = retrieve_chunks(expanded, collections, combined_filters)

    if not documents:
        trace.answer = "No relevant results found in the database."
        return trace

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

    trace.answer = _call_llm(llm_query, context, sources_str, " + ".join(collections))
    trace.retrieved_sources = [
        {
            "filename": m.get("filename", ""),
            "form_number": m.get("form_number", ""),
            "description": m.get("description", ""),
            "state": m.get("state", ""),
            "collection": label,
        }
        for m, label in zip(metadatas, labels)
    ]
    return trace


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
