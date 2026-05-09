# insurance-rag

A RAG (Retrieval-Augmented Generation) system for querying insurance documents — state statutes, administrative code, and educational coverage references — using ChromaDB for vector storage and Claude for generation.

---

## Overview

Ask natural language questions about insurance regulations and coverage concepts. The system retrieves the most relevant document chunks, re-ranks them across collections, and generates a grounded answer citing its sources.

Example queries:
- "Does Ohio require uninsured motorist coverage?"
- "What are Indiana's BI liability minimums?"
- "Compare UM requirements between Ohio and Virginia"
- "Explain what inland marine coverage is"
- "What does ORC 3937.18 say?"
- "What does a dec package contain?"
- "What's on an ACORD 25?"

---

## Architecture

```
User query
    │
    ├─ Abbreviation expansion (UM → uninsured motorist coverage, etc.)
    ├─ Form-number detection (ACORD 25, ORC 3937.18, OAC 3901-1-54, etc.)
    ├─ State detection       (Ohio → OH, Indiana → IN, etc.)
    ├─ Routing classifier    (single Haiku call returns "<collections> | <intent>")
    │     ├─ collections: which collection(s) to search
    │     └─ intent:      "subject" / "context" / "none"
    │                     (skip the form filter when forms are mentioned only as context
    │                      for a conceptual question)
    │
    ├─ Filter resolution
    │     ├─ form_number filter when intent is "subject" (single, $or for multi-form, or
    │     │   $or spanning collections for cross-collection comparisons)
    │     └─ state filter when states are detected
    │
    ├─ ChromaDB vector search (top 8 per collection, filtered as above)
    ├─ Cross-collection re-rank by L2 distance → top 10 chunks
    │
    └─ Claude Haiku generation (context-only, sources cited)
```

### Collections

| Collection | Contents | State-tagged |
|---|---|---|
| `regulatory` | Ohio ORC/OAC statutes + multi-state reference spreadsheet | Yes |
| `educational` | Coverage concept docs (.txt, .docx) | No |
| `forms` | Insurance forms — dec pages, ACORD/ISO forms, endorsements, certificates, state notice forms | Yes |

New collections are registered in `COLLECTION_REGISTRY` in `src/chat.py`. The Haiku router prompt updates automatically.

### State Metadata

Every regulatory chunk carries a `state` metadata field (e.g. `OH`, `IN`). When a state is mentioned in a query, it is added as a ChromaDB filter so results are scoped to the relevant state(s). Queries with no state mention search across all states.

### Form-Number Recognition

The query pipeline recognizes form numbers across three prefix families:

| Prefix | Collection | Stored format | Example query |
|---|---|---|---|
| `ORC` | regulatory | `"ORC3937.18"` (no space) | "What does ORC 3937.18 say?" |
| `OAC` | regulatory | `"OAC3901-1-54"` (no space) | "What is OAC 3901-1-54 about?" |
| `ACORD` | forms | `"ACORD 25"` (single space) | "What does ACORD 25 contain?" |

Detection is case-insensitive and tolerates spacing variations (`acord25` / `ACORD 25` / `Acord  25` all normalize to the stored format). When a query mentions multiple forms ("Compare ACORD 24 and ACORD 28"), all are detected and a `$or` filter retrieves chunks from each. When forms span collections, the filter spans collections too.

When the routing classifier judges that a form is mentioned only as **context** for a conceptual question ("Per ACORD 25 standards, what is general liability?"), the form filter is skipped so semantic search can find the conceptual content instead of being trapped in form-specific chunks.

---

## Folder Structure

```
insurance-rag/
├── main.py                        # CLI entry point
├── pyproject.toml                 # Dependencies (uv)
├── .env                           # ANTHROPIC_API_KEY (never commit)
│
├── src/
│   ├── chat.py                    # Query pipeline: classify → retrieve → generate
│   ├── config.py                  # Central tunables — model names, chunk sizes, token budgets
│   ├── states.py                  # Single source of truth for state name → code mapping
│   ├── db.py                      # Shared ChromaDB client + embedding function (singleton)
│   ├── retrieve.py                # Vector search & metadata lookup (QueryResult dataclass)
│   ├── ingest.py                  # Document loading & chunking (.pdf, .txt, .docx)
│   ├── ingest_xlsx.py             # Multi-state Excel spreadsheet parser
│   ├── ingest_batch.py            # Batch ingestion — scans data/raw/ folder tree
│   ├── embed.py                   # Embedding & ChromaDB storage
│   ├── abbreviations.py           # Insurance abbreviation expansion (60+ terms)
│   ├── scrape_orc.py              # Scraper for codes.ohio.gov PDFs (atomic + retrying)
│   └── migrate_state_tags.py      # Back-fill state metadata on existing chunks
│
├── tools/
│   ├── build_acord_cards.py       # Generates the 180 ACORD library cards from inline index
│   └── _enrich_batch*.py          # One-off scripts that applied per-batch card enrichment
│                                  # (kept as a record of what content went into each card)
│
├── data/
│   └── raw/
│       ├── regulatory/
│       │   ├── ohio/              # Ohio ORC + OAC PDFs  → state: OH
│       │   ├── indiana/           # Indiana statutes     → state: IN
│       │   ├── [state]/           # Other states         → state: XX
│       │   └── reference/         # Cross-state .xlsx files (state tags per chunk)
│       ├── educational/           # .txt and .docx concept docs (no state tag)
│       └── forms/
│           ├── general/           # ACORD/ISO forms, industry-wide  → state: ""
│           ├── ohio/              # Ohio-required forms             → state: OH
│           └── [state]/           # State-specific forms            → state: XX
│
└── chroma_db/                     # Persisted ChromaDB vector index
```

### Adding a New State

1. Add `"kentucky": "KY"` to `STATE_MAP` in `src/states.py` — this is the **single source of truth** for state mappings; `ingest_batch`, `chat`, and `ingest_xlsx` all import from here, so adding it once is enough.
2. Create `data/raw/regulatory/{state_name}/` (e.g. `data/raw/regulatory/kentucky/`)
3. Drop PDFs or text files into the folder
4. Run `python main.py ingest`

### Adding a New Collection

1. Create `data/raw/{collection_name}/` and populate it
2. Add an entry to `COLLECTION_REGISTRY` in `src/chat.py`:
   ```python
   "company": "internal company guidelines, underwriting rules, and policy standards"
   ```
3. Run `python main.py ingest`

The Haiku router and inventory listing update automatically.

---

## Setup

### Prerequisites
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager

### Install

```bash
git clone <repo>
cd insurance-rag
uv sync
```

### Configure

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=sk-ant-...
```

---

## Usage

All commands run from the project root.

### Chat

```bash
python main.py chat
```

Interactive Q&A. Type `quit` to exit.

### Ingest

```bash
# Ingest everything in data/raw/
python main.py ingest

# Ingest one collection only
python main.py ingest --collection educational

# Re-embed existing documents (overwrite)
python main.py ingest --force
```

Supported file types: `.pdf`, `.txt`, `.docx`, `.xlsx`

Excel files in `data/raw/regulatory/reference/` are automatically parsed into per-state chunks — each state gets its own document tagged with its state code.

### Scrape Ohio Statutes

```bash
# Default: ORC chapter 3937 (auto insurance)
python main.py scrape

# Specific chapter
python main.py scrape https://codes.ohio.gov/ohio-revised-code/chapter-3901
python main.py scrape https://codes.ohio.gov/ohio-administrative-code/chapter-3901-1
```

Downloaded PDFs go to `data/raw/regulatory/ohio/`. Run `ingest` afterwards.

### Migrate State Tags

One-time utility to back-fill `state` metadata on chunks ingested before state tagging was introduced.

```bash
# Preview changes
python main.py migrate --dry-run

# Apply (defaults to state: OH on regulatory collection)
python main.py migrate

# Other collection or state
python main.py migrate --collection regulatory --state IN
```

---

## Embedding Model

`all-MiniLM-L6-v2` (sentence-transformers, 384 dimensions). Loaded once per process via a module-level singleton in `src/db.py`.

## Generation Model

`claude-haiku-4-5-20251001` — used for both the routing classifier (`max_tokens=30`, returns `<collections> | <intent>`) and answer generation (`max_tokens=1024`, full prose answer with citations).

All token budgets and model identifiers live in `src/config.py`.

---

## Document Metadata

Every chunk stored in ChromaDB carries:

| Field | Description |
|---|---|
| `form_number` | Parsed form/statute number (e.g. `ORC3937.18`) |
| `edition_date` | Edition date if present in filename |
| `description` | Human-readable document description |
| `filename` | Display filename |
| `parsed` | Whether filename parsing succeeded |
| `state` | Two-letter state code (e.g. `OH`), empty string if not state-specific |
