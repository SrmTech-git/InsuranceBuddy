# Development Log

---

## Session 1 — Initial Build

### Ohio Administrative Code — Chapter 3901-1
- 23 rules downloaded and ingested
- Source: https://codes.ohio.gov/ohio-administrative-code/chapter-3901-1
- Naming format: OAC3901-1.XX Section Title.pdf
- 1,387 total vectors in collection

### Abbreviation Expansion
- `src/abbreviations.py` — 60+ industry standard insurance abbreviations
- Silent preprocessing — user sees original query, retrieval uses expanded version
- UM, UIM, BI, PD, LOB, IM and many others handled

---

## Session 2 — Dual Collection Architecture & Usability Improvements

### Two Collection System
- Split ChromaDB into two named collections: `regulatory` and `educational`
- Regulatory: Ohio statutes and admin code
- Educational: Industry coverage explanations
- Query router detects collection based on question type

### Multi-file Type Support
- `ingest.py` handles `.pdf` and `.txt` files
- `ingest_batch.py` scans for both file types

### Folder Structure
- `data/raw/regulatory/` — all ORC and OAC source PDFs
- `data/raw/educational/` — coverage overview and training documents
- Collection inferred automatically from subfolder name

---

## Session 3 — Architecture Refactor, Multi-State Support & Intelligent Routing

### Architecture fixes (7 items)

**1. Missing dependencies declared**
- `langchain-community` and `langchain-text-splitters` were imported but missing from `pyproject.toml`

**2. Shared `src/db.py` extracted**
- `get_collection()` was duplicated identically in `embed.py` and `retrieve.py`
- Extracted to `src/db.py` with lazy-initialized singletons for the ChromaDB client and sentence-transformer embedding model
- Model now loads once per process instead of on every query call

**3. Document ID collision fixed**
- Chunks from documents without form numbers all got IDs like `doc_0`, `doc_1`, causing silent overwrites
- Fixed: SHA-1 hash of the filename used as the ID prefix fallback

**4. `main.py` wired up as a proper CLI**
- Was a stub; now an `argparse` CLI with subcommands: `chat`, `ingest`, `scrape`, `migrate`
- `sys.path.insert` makes it runnable from any working directory

**5. `ask()` broken into focused helpers**
- Extracted `_handle_inventory()`, `_resolve_form_filter()`, `_retrieve_chunks()`, `_build_context()`, `_call_llm()`
- Fixed redundant double `find_form()` call in form resolution
- `anthropic.Anthropic()` client moved to module-level singleton

**6. `detect_collection()` heuristic improved**
- Regex-based educational routing was misfiring on regulatory questions phrased as "what is the UM limit under ORC 3937.18?"
- Added `_REGULATORY_SIGNALS` regex as a tiebreaker — later replaced entirely by Haiku classification (see below)

**7. `list_all_forms()` print side effect removed**
- Was printing a table unconditionally — bad for composability and testing
- Now a pure function; new `print_forms()` wrapper handles display separately

### .docx support added
- `python-docx` added to dependencies
- `ingest.py` can now load `.docx` files via `_load_docx()`
- `ingest_batch.py` includes `.docx` in `SUPPORTED_EXTENSIONS`
- Filename-based deduplication fallback added for documents without form numbers — prevents re-ingesting identical files

### Haiku-based collection routing
- Replaced brittle regex routing entirely with a fast Haiku API call (`max_tokens=20`)
- `COLLECTION_REGISTRY` dict in `chat.py` drives the classifier prompt — add a new collection in one place, routing updates automatically
- Returns comma-separated collection names, parsed and validated against the registry
- Comparison queries (vs, compare, difference between) still short-circuit to all collections via fast regex — no API call needed
- Scales cleanly to any number of collections

### Cross-collection chunk re-ranking
- Previously: 8 chunks per collection, all passed to LLM (16 for two collections, 24 for three, etc.)
- Now: 8 chunks fetched per collection, all merged, sorted by ChromaDB L2 distance ascending, top 10 kept
- Context window stays bounded regardless of how many collections are searched
- `_CHUNKS_PER_COLLECTION = 8`, `_CONTEXT_CAP = 10` tunable constants in `chat.py`

### Multi-state regulatory support

**Folder structure redesigned:**
```
data/raw/regulatory/
    ohio/          → state: OH
    indiana/       → state: IN
    [state]/       → state: XX
    reference/     → xlsx files, state tags applied per-chunk
```

**State metadata added:**
- `state` field added to `METADATA_KEYS` in `embed.py`
- `embed_document()` now accepts a `state` parameter
- `embed_chunks()` extracted as a lower-level reusable function

**Excel spreadsheet ingestion (`src/ingest_xlsx.py`):**
- Parses `StateSpreadSheet.xlsx` (11 states: OH, IN, IL, KY, MN, VA, MI, GA, TN, IA, WI)
- Dynamically detects state columns from the header row — no hardcoded column indices
- Generates one text document per state with structured requirements
- Each document tagged with its state code and a composite filename (e.g. `StateSpreadSheet_OH`) for deduplication
- Chunks routed through the standard `embed_chunks()` pipeline

**`ingest_batch.py` updated:**
- Handles two-level nested folder structure (collection → state subfolder)
- `STATE_FOLDER_MAP` maps folder names to state codes
- `reference/` folder triggers xlsx processing via `_ingest_xlsx()`
- `.xlsx` added as a supported extension

**State detection in queries (`src/chat.py`):**
- `detect_states()` matches full state names (case-insensitive) and uppercase abbreviations
- `_build_state_filter()` constructs ChromaDB `where` clause for one or more states
- `_merge_filters()` ANDs state filter with any existing form-number filter
- Queries with no state detected search all states

**Migration tooling (`src/migrate_state_tags.py`):**
- One-time script to back-fill `state: OH` on 1,531 existing regulatory chunks
- `--dry-run` flag previews changes without writing
- Accessible via `python main.py migrate`

### Current database state
- `regulatory` collection: ~1,850 vectors
  - Ohio ORC + OAC statutes (306 PDFs, state: OH)
  - 11-state auto requirements reference (StateSpreadSheet.xlsx, per-state chunks)
- `educational` collection: 10 documents (.txt and .docx)
  - Inland marine, commercial auto, BOP, farm, package policy, property, umbrella, crime, GL, workers comp

### load_dotenv fix
- `ANTHROPIC_API_KEY` was being set as an empty string in the OS environment, causing `load_dotenv()` to silently skip the `.env` file
- Fixed: `load_dotenv(override=True)` in `src/chat.py`

---

## Session 4 — Code Review & Cleanup

A top-down audit after Session 3 surfaced a cluster of small issues — band-aids, hardcoded values that risked drift, dead code, missing tests, leaky abstractions. None individually scary; together they were starting to add up. Worked through them in priority order while keeping the codebase lean.

### Test suite (`tests/test_suite.py`)
- Three tiers: unit (no DB, no API), DB integration (ChromaDB only), end-to-end API (live Haiku calls)
- `--skip-api` flag for fast local runs (~11 sec); full suite ~25 sec
- Grew from 0 → 76 tests over the session as fixes added their own coverage
- Fixture-based xlsx test builds an in-memory spreadsheet — no binary fixture committed

### Single source of truth: `src/states.py`
- Three places held identical state dicts: `_STATE_NAME_MAP` in `chat.py`, `STATE_FOLDER_MAP` in `ingest_batch.py`, `_HEADER_TO_STATE` in `ingest_xlsx.py`
- Consolidated into one `STATE_MAP` — the other three now derive from it
- Adding a state is a one-line change in `states.py`
- Tests assert the import chain with `assertIs` so re-introducing a local copy would fail the suite

### Central config: `src/config.py`
- Pulled chunk sizes, model names, retrieval caps, max_tokens budgets, and scrape delay into one module
- Removes drift risk between e.g. the chunk sizes used in `ingest.py` and `ingest_xlsx.py` (which had been duplicated `1000`/`100` literals)

### Bug fixes
- **Dead `_load_xlsx` in `ingest.py`** (~165 lines) — was unreachable AND produced different metadata than the live `ingest_xlsx.py` path. Removed.
- **`_resolve_form_filter` hardcoded the two collections** — now iterates `COLLECTION_REGISTRY` so adding a new collection automatically extends form-number lookup
- **`scrape_orc.py:OUTPUT_DIR`** still pointed at the pre-state-restructure flat layout — fixed to `data/raw/regulatory/ohio/`
- **`pyproject.toml` listed `openpyxl` twice** — deduplicated
- **`__main__` demo blocks** in `embed.py` and `ingest.py` referenced files that were moved during the state restructure — fixed

### Robustness
- **Lazy Anthropic client** (`_get_client()` in `chat.py`) — importing chat no longer requires a working API key, only calling `ask()` does
- **Logging** replaced `print()` breadcrumbs in `chat.py` library code; `main.py` configures `basicConfig` so the CLI still surfaces them
- **Explicit API key validation** at module load with a clear `EnvironmentError` instead of failing cryptically later (replaces the previous `load_dotenv(override=True)` band-aid)
- **`_retrieve_chunks` now logs collection-level query failures** instead of swallowing them silently
- **`_llm_classify` falls back to all collections** if the LLM mangles its routing response — re-ranking sorts it out (was: defaulted to `["regulatory"]`)
- **Abbreviation expansion iterates longest-first** — defends against future overlapping entries (e.g. adding `"MED"` won't clobber `"MED PAY"`)

### Scraper hardening (`scrape_orc.py`)
- **Retry with exponential backoff** — 3 attempts at 2s, 4s, 8s delays on transient `requests.RequestException`
- **Atomic writes** — stage to `*.tmp`, then `replace()` — an interrupted download can never leave a corrupt PDF behind
- **Skip-existing** — re-runs no longer re-download the same 300+ files

### Cleaner abstractions
- **`QueryResult` dataclass in `retrieve.py`** replaces ChromaDB's nested batched-query return shape. Iterates as `(doc, meta, distance)` triples. `chat.py:_retrieve_chunks` and three tests now use the clean shape.

### xlsx Sheet 2 restored
- The dead `_load_xlsx` in `ingest.py` had parsed Sheet 2 ("Quick Reference") and Sheet 3 ("Notes & Sources"); the live `ingest_xlsx.py` was only parsing Sheet 1
- **Sheet 2 restored** — adds compact state-by-state summary content to each state's chunks (Ohio doc went from ~6,500 → 11,500 chars)
- **Sheet 3 deliberately skipped** — maintainer disclaimers, not retrieval material
- Re-ingested the 11 spreadsheet entries; PDFs dedup-skipped automatically. Final regulatory collection: 1,873 vectors.

### Final stats
- 76 tests passing (5 live API tests included)
- 12 focused modules in `src/`: `abbreviations`, `chat`, `config`, `db`, `embed`, `ingest`, `ingest_batch`, `ingest_xlsx`, `migrate_state_tags`, `retrieve`, `scrape_orc`, `states`
- Net diff across the cleanup arc: more capability, fewer lines

---

## Session 5 — Prompt Tuning

Both AI calls (the Haiku classifier and the Haiku answerer) got a small but meaningful rewrite: a brief "why" statement explaining the purpose, an appreciative thank-you to the model, and slightly more context about who's on the receiving end. The goal was to lift quality without adding tokens.

### Classifier prompt (`_llm_classify` in `chat.py`)
- Added a "why" sentence: *"This routing helps surface the right information for someone trying to understand insurance, which is genuinely complicated. Thank you for your attention."*
- Generalized "Ohio-specific rules" → "state-specific rules and statutes" so the prompt scales as more state regulatory content is added.
- `COLLECTION_REGISTRY` description for `regulatory` updated from `"Ohio statutes (ORC/OAC)"` to `"state statutes and administrative code (e.g. Ohio ORC/OAC)"` — keeps Ohio as a concrete anchor without excluding other states.

### Answerer prompt (`SYSTEM_PROMPT` + user message in `_call_llm`)
- Replaced the "rules" framing with a stakes-aware opening: *"people often come to this with real decisions on the line, so accuracy matters more than completeness."*
- Added a clearer fallback instruction: *"A clear 'I don't know' is more useful than a guess."*
- Closes with *"Thank you for your attention."*
- Dropped the trailing `"Remember: Tell the user which document(s) the answer came from"` line from the user message — the system prompt already covers sourcing, no need to repeat per call.

### Observed results
- **Routing got more deliberate on ambiguous queries.** Before: "What are BI minimums?" would have leaned toward one collection. After: routes to both regulatory and educational — accepts the ambiguity instead of guessing.
- **Answers kept their citation discipline but gained a warmer voice.** Statute summaries now naturally include framing like *"Your actual policy may have higher limits"* — the empathy implicit in the new system prompt is showing up in the output.
- **Net change to `chat.py`:** -3 lines across both edits combined. Cleaner *and* better.

---

## Session 6 — Forms Collection

Added a third collection for insurance forms — the documents people actually work with day-to-day. Distinct from regulatory (statutes) and educational (concepts).

### What lives here
- General industry forms: ACORD applications, ISO standardized forms (CG 00 01, CA 00 01), endorsement templates, dec page boilerplate
- State-specific mandatory forms: state-required notice forms, UM rejection forms, etc.

### Code changes
- One line in `COLLECTION_REGISTRY` registering `"forms"` with a description.
- One line in the classifier prompt's routing rules: *"Questions about what a specific FORM contains, what a dec page includes, or how a particular document is structured -> forms"*
- New folder layout under `data/raw/forms/`: `general/` (state="") and `ohio/` (state="OH"). Add more state subfolders as needed; `STATE_FOLDER_MAP` already covers all 11 states.
- New `TestCollectionRegistry` test class enforces the expected three-collection set. Adding a fourth collection will fail this test until updated — forces deliberate registration.
- New `test_forms_collection_exists` in `TestDatabase` confirms the collection is reachable in ChromaDB even before any documents are ingested.

### Routing examples
| Query | Routes to |
|---|---|
| "What does a dec package contain?" | forms |
| "What's on an ACORD 25?" | forms |
| "What forms exist for UM rejection in Ohio?" | regulatory + forms (mixed) |
| "Compare a CG 00 01 and a CA 00 01" | all three (comparison fast-path) |

The mixed-routing case is the interesting one — a UM rejection question is partly statutory (what's required) and partly forms (which document). Cross-collection re-ranking handles it naturally.

### Stats
- 79 tests passing (3 new tests added)
- `forms` collection: 0 vectors (awaiting content)
- Drop PDFs/docs into `data/raw/forms/general/` or `data/raw/forms/{state}/` then run `python main.py ingest` — no other code changes needed.

---

## Session 7 — Forms Collection: First Content (ACORD National Index)

Loaded the first 75 forms into the new `forms` collection from a snapshot of the COUNTRYWIDE P&C FORMS index. Spent the session deciding what goes into the collection, what doesn't, and tuning retrieval until short-form-number queries resolved cleanly.

### Strategic decision: card catalog over full text

We initially planned to ingest the actual ACORD PDFs alongside descriptions. After a dry-run revealed that PyPDFLoader on fillable forms produces field-label garbage (`CIVIL UNION (if applicable)MARITAL STATUS /FEINPHONE #CELL...`), we reframed:

- **The forms collection is a card catalog, not a full-text index.** Field labels aren't useful for retrieval — what matters is *which forms exist, what they're for, when they're used, what edition is current, what states they apply to.*
- PDFs of the actual forms can live in a separate human-reference library if/when we want them — they're not what the AI needs to know about.

This also scales: 75 short cards → ~75 vectors. If the index grows to thousands of forms, we're still fine.

### What got built

- **`tools/build_acord_cards.py`** — one-time generator that emits one `.txt` library card per form into `data/raw/forms/general/`. Inline data table covers all 75 national forms from the COUNTRYWIDE P&C index.
- **75 library cards** with the structure:
  ```
  ACORD 25 (2025-12) — Certificate of Liability Insurance
  =======================================================
  Form number: ACORD 25
  Edition: 2025-12
  Title: Certificate of Liability Insurance
  Type: Insurance form (ACORD industry standard)
  States: All
  ```

### Bug fixes uncovered along the way

- **`parse_filename` regex capped prefixes at 4 letters.** "ACORD" (5 letters) parsed as "CORD". Bumped `[A-Z]{2,4}` → `[A-Z]{2,6}`.
- **No alphabetic suffix support** in form number patterns — broke for forms like `50 WM` and `60 US`. Added `[A-Z]*` after `\d+` in the regex.
- **`ACORD` was in `INSURANCE_ABBREVIATIONS`** as "Association for Cooperative Operations Research and Development". `expand_abbreviations` would mangle "ACORD 25" → "Association for ... 25" before form lookup. Removed the entry with a comment explaining why.
- **`main.py` hardcoded `--collection {regulatory,educational}`** — adding "forms" required a CLI fix. Now sources choices from `COLLECTION_REGISTRY` so future collections extend automatically.

### Retrieval tuning: dropped zero-padding

First-pass smoke test exposed a precision issue: cards used `ACORD 0025` (zero-padded), but users naturally type `ACORD 25`. With 75 highly uniform cards, semantic similarity returned numerically-adjacent forms but missed the exact one asked for. Dropped the padding — `ACORD 0025` → `ACORD 25` — and re-ingested. After the change, *"What's the current edition of ACORD 25?"* and *"What's form 88?"* both resolve cleanly to the right form.

Lesson: when chunks are uniformly structured (as a card catalog is), **the user's natural query phrasing must appear verbatim** in the card. Padding made sense visually but hurt retrieval.

### Tests
- New `parse_filename` tests for ACORD prefix and suffix-form variants
- 81 tests passing total

### Stats
- `forms` collection: 75 vectors (one per card)
- Total across all collections: 1,873 (regulatory) + 53 (educational) + 75 (forms) = **2,001 vectors**
- Re-ingestion of forms after un-padding: ~17 seconds

---

## Session 8 — National Forms Backfill

Loaded the rest of the national ACORD forms from the COUNTRYWIDE P&C index (the "continued" pages). 105 new entries — forms 141 through 877 — covering crime, transportation, builders risk, business owners, NFIP flood, aviation, agriculture, surety, specialty/E&O lines, professional liability, and consumer-report disclosures.

### Build script tweaks
- **Empty edition support** — three forms in the index (350, 360, 370) are watermark paper stock with no edition date. Updated `build_card` and `build_filename` to handle empty `edition`: filename omits the `(date)` segment and the card content shows `Edition: (not specified)`.
- One new `parse_filename` test (`test_no_edition_in_filename`) locks in the partial-match path that handles this case.

### Re-ingestion was a one-liner
The dedup-skip on filename made the re-ingest trivial:
- Existing 75 cards: unchanged content → skipped
- New 105 cards: embedded fresh
- Total runtime: ~20 seconds

### Smoke check
5 of 6 sample queries resolved cleanly:
| Query | Result |
|---|---|
| "What's ACORD 25?" | ✅ Cert of Liability Insurance, 2025-12 |
| "What's the current edition of ACORD 130?" | ✅ Workers Comp App, 2026-01 |
| "Is there an ACORD form for cyber coverage?" | ✅ ACORD 834 (2014-12) |
| "Show me ACORD aviation forms" | ✅ Listed 325, 329, 330... |
| "What's form 877?" | ❌ Returned 876 instead — fuzziness at 180 uniform cards |
| "What forms cover NFIP flood insurance?" | ✅ Listed 301, 302, 303... |

The 877 miss is the precision-vs-recall tradeoff we accepted in Session 7 ("fine until it's not"). At 180 cards with near-identical structure, semantic similarity returns numerically-adjacent forms when the query is just a bare number. Filed for future revisit if it becomes a real problem in daily use.

### Stats
- `forms` collection: 180 vectors
- Total across all collections: 1,873 (regulatory) + 53 (educational) + 180 (forms) = **2,106 vectors**
- 82 tests passing (one new for the no-edition path)
- National ACORD forms backlog: complete
