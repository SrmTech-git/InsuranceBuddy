# eval/scorer.py — deterministic scoring for eval cases
#
# Three dimensions of scoring:
#   1. Source recall    — did the expected source(s) appear in retrieved chunks?
#   2. Content recall   — did the expected content phrases appear in the answer?
#   3. Refusal correctness — when should_have_info=False, did the system
#                            actually refuse?
#
# Each case gets a pass/fail per dimension plus an overall pass flag.
# Source recall and content recall use case-insensitive substring matching —
# deliberately permissive so paraphrasing isn't punished; deliberately
# strict on which DOCUMENT was retrieved (the filename has to actually
# appear among retrieved sources).

from dataclasses import dataclass

# Phrases that indicate the system refused to answer due to insufficient info.
# Kept lowercase for case-insensitive matching.
REFUSAL_MARKERS = (
    "don't have enough",
    "do not have enough",
    "don't have information",
    "do not have information",
    "no relevant results",
    "no information",
    "i don't have",
    "i do not have",
)


@dataclass
class CaseScore:
    case_id: str
    query: str
    source_recall: float        # 0.0 to 1.0
    content_recall: float       # 0.0 to 1.0
    refused_correctly: bool     # for should_have_info=False cases
    passed: bool                # overall pass flag
    notes: list[str]            # human-readable diagnostic strings


def _answer_is_refusal(answer: str) -> bool:
    """Detect whether the answer is a "no info available" refusal."""
    lower = answer.lower()
    return any(marker in lower for marker in REFUSAL_MARKERS)


def _source_recall(expected_sources: list[str], retrieved_sources: list[dict]) -> tuple[float, list[str]]:
    """Return 1.0 if ANY expected source matched a retrieved chunk, else 0.0.

    Treating expected_sources as "any-of" rather than "all-of" reflects
    the reality that a correct answer can often be sourced from multiple
    documents — e.g. the duty-to-cooperate answer is fully present in
    Exclusions/Conditions AND in Claims Process, and either is a valid
    grounding. Source recall is binary: at least one expected source is
    retrieved (pass) or none are (fail).

    Matching is case-insensitive substring against the filename or
    form_number of each retrieved chunk. Returns (recall, missing_list)
    where missing_list contains the unmatched expected sources for
    diagnostic display when the case still failed for other reasons.
    """
    if not expected_sources:
        return 1.0, []  # nothing expected = trivially met

    retrieved_strings = [
        f"{s.get('filename', '')} {s.get('form_number', '')}".lower()
        for s in retrieved_sources
    ]
    matched = []
    missing = []
    for expected in expected_sources:
        e = expected.lower()
        if any(e in r for r in retrieved_strings):
            matched.append(expected)
        else:
            missing.append(expected)

    recall = 1.0 if matched else 0.0
    return recall, missing


def _content_recall(expected_content: list[str], answer: str) -> tuple[float, list[str]]:
    """Compute fraction of expected content phrases that appear in answer.

    Case-insensitive substring match. Returns (recall, missing_phrases).
    """
    if not expected_content:
        return 1.0, []  # nothing expected = trivially met

    lower_answer = answer.lower()
    found = []
    missing = []
    for phrase in expected_content:
        if phrase.lower() in lower_answer:
            found.append(phrase)
        else:
            missing.append(phrase)

    return len(found) / len(expected_content), missing


def score_case(case: dict, trace) -> CaseScore:
    """Score a single case against the trace from ask_traced().

    Pass rules:
      - For should_have_info=True cases:
          source_recall >= 1.0 AND content_recall >= 0.66 AND not a refusal
      - For should_have_info=False cases:
          must refuse (refused_correctly=True)
    """
    case_id = case["id"]
    query = case["query"]
    should_have_info = case.get("should_have_info", True)
    expected_sources = case.get("expected_sources", [])
    expected_content = case.get("expected_content", [])

    notes: list[str] = []

    source_recall, missing_sources = _source_recall(expected_sources, trace.retrieved_sources)
    content_recall, missing_content = _content_recall(expected_content, trace.answer)
    is_refusal = _answer_is_refusal(trace.answer)

    if should_have_info:
        refused_correctly = not is_refusal  # answered = correct here
        passed = (
            source_recall >= 1.0
            and content_recall >= 0.66
            and not is_refusal
        )
        if missing_sources:
            notes.append(f"missing sources: {missing_sources}")
        if missing_content:
            notes.append(f"missing content phrases: {missing_content}")
        if is_refusal:
            notes.append("system refused but case expected info")
    else:
        refused_correctly = is_refusal
        passed = is_refusal
        if not is_refusal:
            notes.append("system answered but case expected refusal")

    return CaseScore(
        case_id=case_id,
        query=query,
        source_recall=source_recall,
        content_recall=content_recall,
        refused_correctly=refused_correctly,
        passed=passed,
        notes=notes,
    )
