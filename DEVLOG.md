### Ohio Administrative Code — Chapter 3901-1 (General Insurance Rules)
- 23 rules downloaded and ingested
- Source: https://codes.ohio.gov/ohio-administrative-code/chapter-3901-1
- Naming format: OAC3901-1.XX Section Title.pdf
- 23 vectors added, 1,387 total in collection
- Key topics: claims handling timeframes, policy form requirements,
  unfair practices rules, insurer conduct standards

### What Worked Well
- Abbreviation expansion — silent query preprocessing maps
  industry standard abbreviations to full terms before retrieval.
  UM, UIM, BI, PD, LOB and 60+ others handled. Source:
  src/abbreviations.py. Eliminates a major usability gap.

## Session 2 — Dual Collection Architecture & Usability Improvements

### Two Collection System
- Split ChromaDB into two named collections: `regulatory` and `educational`
- Regulatory: Ohio statutes and admin code (1,387 vectors)
- Educational: Industry coverage explanations (growing)
- Query router detects collection based on question type:
  - Conceptual triggers ("what is", "how does", "explain") → educational
  - Comparative triggers ("difference between", "compare", "vs") → both collections
  - Everything else → regulatory
- Chunks labeled by collection in LLM context for source authority

### Multi-file Type Support
- ingest.py now handles .pdf and .txt files
- TextLoader added for .txt, PyPDFLoader retained for .pdf
- ingest_batch.py scans for both file types

### Abbreviation Expansion
- src/abbreviations.py — 60+ industry standard abbreviations
- Silent preprocessing — user sees original query, retrieval uses expanded version
- UM, UIM, BI, PD, LOB, IM and many others handled

### Folder Structure Reorganization
- data/raw/ split into subfolders by collection type
- data/raw/regulatory/ — all ORC and OAC source PDFs (306 files)
- data/raw/educational/ — coverage overview and training documents
- ingest_batch.py now infers collection from subfolder name automatically
- scrape_orc.py updated to output directly to data/raw/regulatory/
- Drop a file in the right folder and run ingest_batch.py — no flags needed
