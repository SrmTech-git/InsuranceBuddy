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

## Session 4 — Prompt Tuning

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
