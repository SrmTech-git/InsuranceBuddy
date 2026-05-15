# query_parsing.py — pure functions that extract structure from a user query
#
# Everything in this module is regex/dict-based and side-effect-free:
#   - Form-number detection (ACORD 25, ORC 3937.18, OAC 3901-1-54, ...)
#   - Bare section detection (3937.18 → try as ORC/OAC fallback)
#   - Form-context prefix stripping ("Per ACORD 25, ..." → "...")
#   - Inventory-query detection ("what forms do we have")
#   - State detection (Ohio, IN, ...) and ChromaDB filter construction
#
# These functions don't talk to the DB or the LLM. chat.py and retrieve.py
# use them to decide WHAT to query.

import re
from states import STATE_MAP, STATE_ABBR_SET


# Known form-number prefixes across collections.
# - ORC/OAC: regulatory (Ohio statutes / admin code) — stored without
#   spaces (e.g. "ORC3937.18", "OAC3901-1-54")
# - ACORD: forms (industry-standard ACORD forms) — stored with a
#   single space (e.g. "ACORD 25", "ACORD 50WM")
# detect_form_numbers normalizes user queries to match the stored format
# of whichever prefix it sees.
KNOWN_PREFIXES = ("ORC", "OAC", "ACORD")


# ---------------------------------------------------------------------------
# Form-number detection
# ---------------------------------------------------------------------------

def detect_form_numbers(text: str) -> list[str]:
    """Return ALL normalized form numbers found in the query, in order, deduped.

    Returns an empty list if none are present. Handles multi-form queries
    like "What's the difference between ACORD 24 and ACORD 28?".

    Normalization matches how each prefix is stored in metadata:
    - ORC/OAC strip spaces ("ORC 3937.18" -> "ORC3937.18")
    - ACORD preserves a single space ("ACORD25" or "acord 25" -> "ACORD 25")

    The regex allows an alphabetic suffix after the digits to handle
    ACORD forms like 50WM, 60US, 64US (attached) and state variants
    like 50 IL, 66 MI, 90 VA (space-separated, normalized to attached).

    The space-separated suffix is restricted to known state codes and
    known national ACORD suffixes so natural English like "ACORD 50 to
    ACORD 50WM" doesn't capture "TO" as a suffix.
    """
    prefixes = "|".join(KNOWN_PREFIXES)
    # State codes (IL, IN, IA, KY, MI, OH, VA, WI, GA, MN, TN) +
    # known national ACORD suffixes (WM, US, WMSET) — the only valid
    # tokens that may appear AFTER a space before a form-number boundary.
    space_suffix_alts = "|".join(sorted(STATE_ABBR_SET) + ["WM", "WMSET", "US"])
    raw_matches = re.findall(
        rf"\b((?:{prefixes})\s*\d+(?:[A-Z]+|\s+(?:{space_suffix_alts}))?(?:[.\-]\d+)*)\b",
        text,
        re.IGNORECASE,
    )
    seen: set[str] = set()
    result: list[str] = []
    for raw_match in raw_matches:
        raw = raw_match.strip().upper()
        if raw.startswith("ACORD"):
            # Collapse all internal whitespace so "ACORD 66 MI" -> "ACORD 66MI"
            # matches the stored form_number ("ACORD" + number + attached suffix)
            after = re.sub(r"\s+", "", raw[5:])
            normalized = f"ACORD {after}"
        else:
            normalized = raw.replace(" ", "")
        if normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


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
    prefixes = "|".join(KNOWN_PREFIXES)
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


# ---------------------------------------------------------------------------
# State detection
# ---------------------------------------------------------------------------

def detect_states(text: str) -> list[str]:
    """Return sorted list of state codes mentioned in the query.

    Matches full state names (case-insensitive) and uppercase abbreviations
    (e.g. OH, IN) as standalone words. Short abbreviations are only matched
    uppercase to avoid false positives on common words like "in", "oh", "ia".
    """
    found: set[str] = set()

    for name, code in STATE_MAP.items():
        if re.search(rf"\b{re.escape(name)}\b", text, re.IGNORECASE):
            found.add(code)

    for code in STATE_ABBR_SET:
        if re.search(rf"\b{code}\b", text):  # case-sensitive — uppercase only
            found.add(code)

    return sorted(found)


# ---------------------------------------------------------------------------
# Filter construction
# ---------------------------------------------------------------------------

def build_state_filter(states: list[str]) -> dict | None:
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


def merge_filters(*filters: dict | None) -> dict | None:
    """AND together multiple ChromaDB filter dicts, ignoring None values."""
    active = [f for f in filters if f]
    if not active:
        return None
    if len(active) == 1:
        return active[0]
    return {"$and": active}
