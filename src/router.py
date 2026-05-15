# router.py — collection routing and form-intent classification
#
# A single Haiku call classifies a query along two dimensions in one shot:
#   1. Which collection(s) to search
#   2. If forms are mentioned, whether they're the SUBJECT of the query
#      or just CONTEXT for a conceptual question
#
# The Anthropic client lives here because router.py is the first module
# in the dependency graph that needs it. chat.py imports _get_client from
# here for the answer call.

import logging
import os
import anthropic

from config import GENERATION_MODEL, CLASSIFIER_MAX_TOKENS

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Collection registry — add new collections here as they are created.
# The descriptions are passed directly to the Haiku classifier, so write
# them to be distinct and specific about what each collection contains.
# ---------------------------------------------------------------------------

COLLECTION_REGISTRY: dict[str, str] = {
    "regulatory": "state statutes and administrative code (e.g. Ohio ORC/OAC), compliance requirements, filing rules, penalties, legal limits",
    "educational": "conceptual explanations of insurance products, coverage types, and industry terms",
    "forms": "insurance application forms and document templates — declarations pages, ACORD applications, sections, certificates of insurance, ID cards, and state-required notice forms (NOT policy endorsements — see endorsements collection)",
    "endorsements": "policy endorsement forms that modify coverage — ISO/AAIS/NCCI standard endorsements (CG 20 10 Additional Insured, CA 99 23 Drive Other Car, HO 04 90 Personal Injury, etc.), exclusion endorsements, coverage extensions, and state-mandated coverage amendments",
}


# ---------------------------------------------------------------------------
# Anthropic client (lazy — only validates the API key on first use, so
# importing this module is safe in tests and for `--help`).
# ---------------------------------------------------------------------------

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    """Return the shared Anthropic client, validating the API key on first call."""
    global _client
    if _client is None:
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise EnvironmentError(
                "ANTHROPIC_API_KEY is not set or is empty.\n"
                "Create a .env file in the project root with:\n"
                "  ANTHROPIC_API_KEY=sk-ant-..."
            )
        _client = anthropic.Anthropic()
    return _client


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------

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

    # If forms were detected but the LLM returned "none" (an invalid response
    # per the prompt — forms-present queries must return "subject" or
    # "context"), default to "subject" so the form filter still applies.
    # Log it so silent prompt-compliance failures don't accumulate unseen.
    if detected_forms and intent == "none":
        logger.warning(
            "Router returned intent='none' despite forms detected (%s); defaulting to 'subject'. Raw response: %r",
            detected_forms, raw,
        )
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
        temperature=0,  # routing should be deterministic — same query, same route
        messages=[{"role": "user", "content": prompt}],
    )
    return _parse_route_response(response.content[0].text, detected_forms)


def detect_collection(text: str, detected_forms: list[str] | None = None) -> tuple[list[str], str]:
    """Return (collections, form_intent) for this query.

    Routes via Haiku, which classifies both the collection(s) to search
    and (when forms are detected) the form intent.
    """
    return _llm_route(text, detected_forms)
