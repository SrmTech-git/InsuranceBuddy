# eval/run_eval.py — eval framework runner
#
# Loads test cases from cases.json, runs each through ask_traced(), scores
# the results, and writes a markdown report to eval/reports/.
#
# Usage:
#   python main.py eval                    # run all cases
#   python main.py eval --tags routing     # filter by tag (comma-separated)
#   python main.py eval --baseline         # also overwrite eval/baseline.md

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Make src/ and the project root importable. src/ is needed so `from chat
# import ...` resolves; the project root is needed so `from eval.scorer
# import ...` resolves when this file is run directly as a script (the CLI
# path through main.py already has both).
_THIS_DIR = Path(__file__).resolve().parent
_ROOT = _THIS_DIR.parent
sys.path.insert(0, str(_ROOT / "src"))
sys.path.insert(0, str(_ROOT))

# Silence noisy library loggers — the eval doesn't need HTTP traces or
# embedding model progress bars. Has to happen before sentence_transformers
# imports because the bars are managed at import time.
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("anthropic").setLevel(logging.WARNING)
logging.getLogger("chat").setLevel(logging.WARNING)
logging.getLogger("retrieve").setLevel(logging.WARNING)
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TQDM_DISABLE", "1")

from chat import ask_traced
from eval.scorer import score_case, CaseScore


CASES_PATH = _THIS_DIR / "cases.json"
REPORTS_DIR = _THIS_DIR / "reports"
BASELINE_PATH = _THIS_DIR / "baseline.md"


def load_cases(tag_filter: list[str] | None = None) -> list[dict]:
    with CASES_PATH.open(encoding="utf-8") as f:
        cases = json.load(f)
    if tag_filter:
        cases = [c for c in cases if any(t in c.get("tags", []) for t in tag_filter)]
    return cases


def run_cases(cases: list[dict]) -> list[CaseScore]:
    """Execute each case and return per-case scores."""
    scores: list[CaseScore] = []
    for i, case in enumerate(cases, 1):
        print(f"[{i}/{len(cases)}] {case['id']:35s}  ", end="", flush=True)
        try:
            trace = ask_traced(case["query"])
            score = score_case(case, trace)
            print("PASS" if score.passed else "FAIL")
        except Exception as e:
            print(f"ERROR: {e}")
            score = CaseScore(
                case_id=case["id"],
                query=case["query"],
                source_recall=0.0,
                content_recall=0.0,
                refused_correctly=False,
                passed=False,
                notes=[f"runtime error: {e}"],
            )
        scores.append(score)
    return scores


def render_report(scores: list[CaseScore], timestamp: str) -> str:
    """Render scores as a markdown report."""
    total = len(scores)
    passed = sum(1 for s in scores if s.passed)
    avg_src = sum(s.source_recall for s in scores) / total if total else 0.0
    avg_content = sum(s.content_recall for s in scores) / total if total else 0.0

    lines = [
        f"# Eval Report — {timestamp}",
        "",
        f"**Summary:** {passed}/{total} cases passed ({100*passed/total:.0f}%)",
        "",
        f"- Average source recall:   {avg_src:.2f}",
        f"- Average content recall:  {avg_content:.2f}",
        "",
        "## Per-case results",
        "",
        "| Result | Case ID | Source recall | Content recall | Notes |",
        "|---|---|---|---|---|",
    ]
    for s in scores:
        result = "✅ PASS" if s.passed else "❌ FAIL"
        notes = "; ".join(s.notes) if s.notes else "-"
        # Escape pipes that would otherwise break the table
        notes = notes.replace("|", "\\|")
        lines.append(
            f"| {result} | `{s.case_id}` | {s.source_recall:.2f} | {s.content_recall:.2f} | {notes} |"
        )

    # Detail section for failed cases
    failed = [s for s in scores if not s.passed]
    if failed:
        lines += ["", "## Failed cases — detail", ""]
        for s in failed:
            lines += [
                f"### `{s.case_id}`",
                f"**Query:** {s.query}",
                f"- Source recall: {s.source_recall:.2f}",
                f"- Content recall: {s.content_recall:.2f}",
                f"- Notes: {'; '.join(s.notes) if s.notes else 'no notes'}",
                "",
            ]

    return "\n".join(lines) + "\n"


def run_eval(args) -> None:
    """Run the eval suite from parsed args.

    Shared entry point for both the standalone `python eval/run_eval.py`
    invocation and the `python main.py eval` CLI dispatch — both produce
    the same argparse.Namespace shape (.tags, .baseline).
    """
    tag_filter = [t.strip() for t in args.tags.split(",")] if args.tags else None
    cases = load_cases(tag_filter)
    print(f"Running {len(cases)} eval case(s)\n")

    scores = run_cases(cases)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report = render_report(scores, timestamp)

    REPORTS_DIR.mkdir(exist_ok=True)
    report_path = REPORTS_DIR / f"{timestamp}.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"\nReport: {report_path}")

    if args.baseline:
        BASELINE_PATH.write_text(report, encoding="utf-8")
        print(f"Baseline updated: {BASELINE_PATH}")

    passed = sum(1 for s in scores if s.passed)
    print(f"\n{passed}/{len(scores)} passed")


def _parse_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the eval suite")
    parser.add_argument("--tags", default=None, help="Comma-separated tags to filter cases")
    parser.add_argument("--baseline", action="store_true", help="Also overwrite eval/baseline.md")
    return parser.parse_args()


if __name__ == "__main__":
    run_eval(_parse_cli_args())
