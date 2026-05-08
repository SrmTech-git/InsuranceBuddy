# querying the vector store

from dataclasses import dataclass
import chromadb
from db import get_collection


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class QueryResult:
    """Single-query view of ChromaDB's batched query response.

    ChromaDB's native shape is `{"documents": [[...]], "distances": [[...]], ...}`
    where the outer list is one entry per query text. We only ever pass a single
    query, so this dataclass strips that outer layer and exposes the three
    parallel lists directly. Iterate with `for doc, meta, dist in result:`.
    """
    documents: list[str]
    metadatas: list[dict]
    distances: list[float]

    def __len__(self) -> int:
        return len(self.documents)

    def __iter__(self):
        return zip(self.documents, self.metadatas, self.distances)


# ---------------------------------------------------------------------------
# Semantic search
# ---------------------------------------------------------------------------

def query(query_text: str, n_results: int = 8, filters: dict | None = None,
          collection_name: str = "regulatory") -> QueryResult:
    """Search for the most relevant chunks by meaning.

    Args:
        query_text: Natural-language question to search for.
        n_results:  Number of results to return (default 8).
        filters:    Optional dict of metadata filters, e.g.
                    {"form_number": "INS7059"}.  Multiple keys are ANDed.
        collection_name: Which collection to search.
    """

    collection = get_collection(collection_name)

    # Build a ChromaDB 'where' clause from the filters dict
    where = _build_where(filters) if filters else None

    raw = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where=where,
    )

    return QueryResult(
        documents=raw["documents"][0],
        metadatas=raw["metadatas"][0],
        distances=raw["distances"][0],
    )


def print_results(results: QueryResult) -> None:
    """Pretty-print query results with scores and text."""

    if not results:
        print("  (no results)")
        return

    for i, (doc, meta, distance) in enumerate(results):
        form = meta.get("form_number", "")
        label = f" [{form}]" if form else ""
        # ChromaDB returns L2 distance — lower is more relevant
        print(f"\n--- Result {i + 1}{label} (distance: {distance:.4f}) ---")
        print(doc)


# ---------------------------------------------------------------------------
# Metadata lookup (no semantic search needed)
# ---------------------------------------------------------------------------

def find_form(form_number: str, collection_name: str = "regulatory") -> dict | None:
    """Look up a form by its form number and return its metadata.

    Returns the metadata dict if found, None otherwise.
    Useful for answering "do we have this form?" without a vector search.
    """

    collection = get_collection(collection_name)

    results = collection.get(
        where={"form_number": form_number},
        limit=1,
    )

    if results["ids"]:
        return results["metadatas"][0]

    return None


def list_all_forms(collection_name: str = "regulatory") -> list[dict]:
    """Return every unique form in the database with its metadata.

    Each entry has: form_number, edition_date, description, filename, chunk_count.
    """

    collection = get_collection(collection_name)
    all_data = collection.get(include=["metadatas"])

    seen = {}
    for meta in all_data["metadatas"]:
        form = meta.get("form_number", "")
        key = form if form else meta.get("filename", "unknown")

        if key not in seen:
            seen[key] = {
                "form_number": form,
                "edition_date": meta.get("edition_date", ""),
                "description": meta.get("description", ""),
                "filename": meta.get("filename", ""),
                "chunk_count": 0,
            }
        seen[key]["chunk_count"] += 1

    return list(seen.values())


def print_forms(collection_name: str = "regulatory") -> None:
    """Print a summary table of all forms in the given collection."""
    forms = list_all_forms(collection_name)
    print(f"Found {len(forms)} document(s) in the '{collection_name}' collection:\n")
    for f in forms:
        label = f["form_number"] or "(no form number)"
        print(f"  {label}")
        print(f"    Edition:     {f['edition_date'] or '(none)'}")
        print(f"    Description: {f['description'] or '(none)'}")
        print(f"    Filename:    {f['filename']}")
        print(f"    Chunks:      {f['chunk_count']}")
        print()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_where(filters: dict) -> dict:
    """Convert a flat filters dict into a ChromaDB 'where' clause.

    Single filter:  {"form_number": "INS7059"}
        -> {"form_number": "INS7059"}

    Multiple filters: {"form_number": "INS7059", "edition_date": "Rev. 02/2021"}
        -> {"$and": [{"form_number": "INS7059"}, {"edition_date": "Rev. 02/2021"}]}
    """

    conditions = [{k: v} for k, v in filters.items()]

    if len(conditions) == 1:
        return conditions[0]

    return {"$and": conditions}


# ---------------------------------------------------------------------------
# Demo / testing
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # 1. List all forms in the database
    print("=" * 60)
    print("ALL FORMS IN DATABASE (regulatory)")
    print("=" * 60)
    print_forms("regulatory")

    # 2. Look up a specific form by number
    print("=" * 60)
    print("FORM LOOKUP: ORC3937.18")
    print("=" * 60)
    result = find_form("ORC3937.18")
    if result:
        print(f"  Found: {result}")
    else:
        print("  Not found in the database.")
    print()

    # 3. Unfiltered semantic search
    test_query = "uninsured motorist coverage"
    print("=" * 60)
    print(f"SEMANTIC SEARCH: '{test_query}'")
    print("=" * 60)
    results = query(test_query)
    print_results(results)
