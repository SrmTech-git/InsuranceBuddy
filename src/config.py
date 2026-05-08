# config.py — central tunables.  Lean by design: literals only, no logic.
# If a value is reused in more than one place, it belongs here.

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GENERATION_MODEL = "claude-haiku-4-5-20251001"

# ---------------------------------------------------------------------------
# Document chunking
# ---------------------------------------------------------------------------
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# ---------------------------------------------------------------------------
# Retrieval (cross-collection re-ranking)
# ---------------------------------------------------------------------------
CHUNKS_PER_COLLECTION = 8     # how many chunks to pull from each collection
CONTEXT_CAP = 10              # how many to keep after re-ranking

# ---------------------------------------------------------------------------
# LLM token budgets
# ---------------------------------------------------------------------------
CLASSIFIER_MAX_TOKENS = 20    # routing call — short answer
ANSWER_MAX_TOKENS = 1024      # final answer to user

# ---------------------------------------------------------------------------
# Scraping
# ---------------------------------------------------------------------------
SCRAPE_DELAY_SECONDS = 1      # polite pacing between requests
