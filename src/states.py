# states.py — single source of truth for supported state mappings
#
# Every place that needs to know about states imports from here.
# To add a new state:
#   1. Add an entry to STATE_MAP below (lowercase folder name -> uppercase code)
#   2. Create the matching folder under data/raw/regulatory/
#   3. Run `python main.py ingest`
#
# No other files need changing.

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
