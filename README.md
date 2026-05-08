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

---

## Architecture

```
User query
    │
    ├─ Abbreviation expansion (UM → uninsured motorist coverage, etc.)
    ├─ State detection       (Ohio → OH, Indiana → IN, etc.)
    ├─ Collection routing    (Haiku fast call → regulatory / educational / both)
    │
    ├─ ChromaDB vector search (top 8 per collection, filtered by state if detected)
    ├─ Cross-collection re-rank by L2 distance → top 10 chunks
    │
    └─ Claude Haiku generation (context-only, sources cited)
```

### Collections

| Collection | Contents | State-tagged |
|---|---|---|
| `regulatory` | Ohio ORC/OAC statutes + multi-state reference spreadsheet | Yes |
| `educational` | Coverage concept docs (.txt, .docx) | No |

New collections are registered in `COLLECTION_REGISTRY` in `src/chat.py`. The Haiku router prompt updates automatically.

### State Metadata

Every regulatory chunk carries a `state` metadata field (e.g. `OH`, `IN`). When a state is mentioned in a query, it is added as a ChromaDB filter so results are scoped to the relevant state(s). Queries with no state mention search across all states.

---

## Folder Structure

```
insurance-rag/
├── main.py                        # CLI entry point
├── pyproject.toml                 # Dependencies (uv)
├── .env                           # ANTHROPIC_API_KEY (never commit)
│
├── src/
│   ├── db.py                      # Shared ChromaDB client + embedding function (singleton)
│   ├── ingest.py                  # Document loading & chunking (.pdf, .txt, .docx)
│   ├── ingest_xlsx.py             # Multi-state Excel spreadsheet parser
│   ├── ingest_batch.py            # Batch ingestion — scans data/raw/ folder tree
│   ├── embed.py                   # Embedding & ChromaDB storage
│   ├── retrieve.py                # Vector search & metadata lookup
│   ├── chat.py                    # Query pipeline: classify → retrieve → generate
│   ├── abbreviations.py           # Insurance abbreviation expansion (60+ terms)
│   ├── scrape_orc.py              # Scraper for codes.ohio.gov PDFs
│   └── migrate_state_tags.py      # One-time migration: back-fill state metadata
│
├── data/
│   └── raw/
│       ├── regulatory/
│       │   ├── ohio/              # Ohio ORC + OAC PDFs  → state: OH
│       │   ├── indiana/           # Indiana statutes     → state: IN
│       │   ├── [state]/           # Other states         → state: XX
│       │   └── reference/        # Cross-state .xlsx files (state tags per chunk)
│       └── educational/           # .txt and .docx concept docs (no state tag)
│
└── chroma_db/                     # Persisted ChromaDB vector index
```

### Adding a New State

1. Create `data/raw/regulatory/{state_name}/` (e.g. `data/raw/regulatory/kentucky/`)
2. Add `"kentucky": "KY"` to `STATE_FOLDER_MAP` in `src/ingest_batch.py`
3. Add `"kentucky": "KY"` to `_STATE_NAME_MAP` in `src/chat.py`
4. Drop PDFs or text files into the folder
5. Run `python main.py ingest`

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

`claude-haiku-4-5-20251001` — used for both collection routing (fast, max_tokens=20) and answer generation (max_tokens=1024).

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
