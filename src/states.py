# states.py — single source of truth for supported state mappings
#
# STATE_MAP is canonical (lowercase folder name -> uppercase code).
# The other maps below are mechanical derivations exported alongside it
# so every consumer (ingest_batch, ingest_xlsx, query_parsing) reads from
# one place. To add a state, change STATE_MAP and run the test suite —
# everything downstream picks it up automatically.
#
# To add a new state:
#   1. Add an entry to STATE_MAP below
#   2. Create the matching folder under data/raw/regulatory/
#   3. Run `python main.py ingest`

STATE_MAP: dict[str, str] = {
    "ohio": "OH",
    "indiana": "IN",
    "illinois": "IL",
    "kentucky": "KY",
    "minnesota": "MN",
    "virginia": "VA",
    "michigan": "MI",
    "georgia": "GA",
    "tennessee": "TN",
    "iowa": "IA",
    "wisconsin": "WI",
}

# Code -> code map. Useful for "is this token a known state abbreviation"
# checks (matched case-sensitively against uppercase letters in queries
# so common words like "in", "oh", "ia" don't trigger false positives).
STATE_ABBR_MAP: dict[str, str] = {v: v for v in STATE_MAP.values()}

# Title-Case spreadsheet column header -> code. Used by ingest_xlsx to
# identify per-state columns in the multi-state reference spreadsheet.
HEADER_TO_STATE_MAP: dict[str, str] = {name.title(): code for name, code in STATE_MAP.items()}
