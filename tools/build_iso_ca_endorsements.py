"""build_iso_ca_endorsements.py — generate library-card .txt files for
the ISO Commercial Auto (CA) line.

Source: ISO COMMERCIAL AUTO FORMS LIST.txt (an ISO forms index transcript).
Parses each line into (form_number, edition_MMYY, title), dedupes by
form_number keeping the newest edition, normalizes editions to YYYY-MM,
and writes one bare metadata card per form into
data/raw/endorsements/general/.

Cards start as bare metadata (form_number, edition, title, type, states)
and get enriched later in thematic batches — same workflow as Sessions 7-9
did for the national ACORD forms.

Run from project root:
    python tools/build_iso_ca_endorsements.py
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_PATH = Path(r"C:\Users\shann\OneDrive\Documents\ISO COMMERCIAL AUTO FORMS LIST.txt")
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw" / "endorsements" / "general"

# Form-number-prefix → series category (used to classify form types).
# CA 00 are base coverage forms; CA P are advisory notices; CA R are
# tables of contents; everything else is an endorsement.
SERIES_CATEGORY = {
    "CA 00": "coverage form",
    "CA DS": "declarations form",
    "CA P":  "policyholder advisory notice",
    "CA R":  "form table of contents",
}


def normalize_edition(mmyy: str) -> str:
    """Convert ISO 'MM YY' edition (e.g., '11 20', '01 87') to 'YYYY-MM'.

    Two-digit years <= current year tail (say <=30) are 2000s; otherwise
    1900s. Conservative cutoff at 30 captures everything ISO has filed
    through 2030 as 20xx, and 1990s/older as 19xx.
    """
    m = re.fullmatch(r"(\d{2})\s+(\d{2})", mmyy.strip())
    if not m:
        return mmyy.strip()
    month, yy = m.group(1), m.group(2)
    yy_int = int(yy)
    century = 2000 if yy_int <= 30 else 1900
    return f"{century + yy_int:04d}-{month}"


def parse_line(line: str) -> tuple[str, str, str] | None:
    """Parse 'CA 00 01 11 20 | BUSINESS AUTO COVERAGE FORM' into
    (form_number, edition_YYYY-MM, title). Returns None for headers/blanks.
    """
    line = line.rstrip("\n")
    if "|" not in line:
        return None

    head, title = line.split("|", 1)
    head = head.strip()
    title = title.strip()
    if not head or not title:
        return None

    # head is something like "CA 00 01 11 20" or "CA P 001 09 04" or
    # "CA R 020 03 22". The last two whitespace-separated tokens are the
    # MM YY edition; the rest is the form number.
    tokens = head.split()
    if len(tokens) < 3:
        return None
    edition_raw = " ".join(tokens[-2:])
    edition = normalize_edition(edition_raw)
    form_number = " ".join(tokens[:-2])

    # Sanity check: edition normalized successfully (yyyy-mm)
    if not re.fullmatch(r"\d{4}-\d{2}", edition):
        return None
    return form_number, edition, title


def classify(form_number: str) -> str:
    """Map a form number to its category description for the card 'Type' field."""
    for prefix, cat in SERIES_CATEGORY.items():
        if form_number.startswith(prefix + " ") or form_number == prefix:
            return cat
    return "endorsement"


def dedupe_to_current(rows: Iterable[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    """Given (form_number, edition, title) tuples, keep one row per
    form_number — the one with the newest edition. Edition is YYYY-MM so
    string comparison sorts chronologically.
    """
    best: dict[str, tuple[str, str, str]] = {}
    for form_number, edition, title in rows:
        cur = best.get(form_number)
        if cur is None or edition > cur[1]:
            best[form_number] = (form_number, edition, title)
    # Sort the result by form number for stable output
    return sorted(best.values(), key=lambda x: x[0])


def sanitize_filename(text: str) -> str:
    """Make text safe for filenames: replace path separators and other
    problematic characters with hyphens. Preserves spaces, parens, dashes."""
    text = text.replace("/", " - ").replace("\\", " - ")
    text = re.sub(r'[<>:"|?*]', "-", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_filename(form_number: str, edition: str, title: str) -> str:
    """E.g., 'CA 00 01 (2020-11) Business Auto Coverage Form.txt'."""
    safe_title = sanitize_filename(title.title())
    return f"{form_number} ({edition}) {safe_title}.txt"


def build_card(form_number: str, edition: str, title: str) -> str:
    """Bare metadata card. Same shape as ACORD bare cards before enrichment."""
    safe_title = title.title()
    category = classify(form_number)
    type_line = f"ISO Commercial Auto {category}"
    header = f"{form_number} ({edition}) — {safe_title}"
    rule = "=" * len(header)
    return (
        f"{header}\n"
        f"{rule}\n"
        f"Form number: {form_number}\n"
        f"Edition: {edition}\n"
        f"Title: {safe_title}\n"
        f"Type: {type_line}\n"
        f"States: All\n"
    )


def main() -> None:
    if not SOURCE_PATH.exists():
        raise SystemExit(f"Source file not found: {SOURCE_PATH}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    parsed: list[tuple[str, str, str]] = []
    for line in SOURCE_PATH.read_text(encoding="utf-8").splitlines():
        row = parse_line(line)
        if row is not None:
            parsed.append(row)

    rows = dedupe_to_current(parsed)

    written = 0
    for form_number, edition, title in rows:
        filename = build_filename(form_number, edition, title)
        content = build_card(form_number, edition, title)
        path = OUTPUT_DIR / filename
        path.write_text(content, encoding="utf-8")
        written += 1

    print(f"Source rows parsed:        {len(parsed)}")
    print(f"Unique form numbers:       {len(rows)}")
    print(f"Wrote {written} card(s) to {OUTPUT_DIR}")

    # Categorize for visibility
    by_cat: dict[str, int] = {}
    for form_number, _, _ in rows:
        by_cat[classify(form_number)] = by_cat.get(classify(form_number), 0) + 1
    print()
    print("By category:")
    for cat, n in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"  {cat:35s} {n}")


if __name__ == "__main__":
    main()
