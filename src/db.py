# shared ChromaDB client and embedding function — imported by embed.py and retrieve.py

import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path

CHROMA_DB_PATH = str(Path(__file__).parent.parent / "chroma_db")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

_client: chromadb.ClientAPI | None = None
_embedding_fn: embedding_functions.EmbeddingFunction | None = None


def _get_client() -> chromadb.ClientAPI:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    return _client


def _get_embedding_fn() -> embedding_functions.EmbeddingFunction:
    global _embedding_fn
    if _embedding_fn is None:
        _embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )
    return _embedding_fn


def get_collection(collection_name: str = "regulatory") -> chromadb.Collection:
    """Return (or create) a named ChromaDB collection.

    Reuses a single client and embedding-function instance for the lifetime
    of the process so the sentence-transformer model is only loaded once.
    """
    return _get_client().get_or_create_collection(
        name=collection_name,
        embedding_function=_get_embedding_fn(),
    )
