# querying the vector store

import logging
from dataclasses import dataclass
import chromadb
from db import get_collection
from config import CHUNKS_PER_COLLECTION, CONTEXT_CAP
from query_parsing import merge_filters

logger = logging.getLogger(__name__)


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
# Multi-collection retrieval orchestration
# ---------------------------------------------------------------------------

def retrieve_chunks(
    question: str,
    collections: list[str],
    filters: dict | None,
) -> tuple[list[str], list[dict], list[str]]:
    """Query each collection, merge results, re-rank by L2 distance, return top CONTEXT_CAP."""
    all_docs: list[str] = []
    all_metas: list[dict] = []
    all_labels: list[str] = []
    all_distances: list[float] = []

    for coll in collections:
        try:
            result = query(question, n_results=CHUNKS_PER_COLLECTION, filters=filters, collection_name=coll)
            all_docs.extend(result.documents)
            all_metas.extend(result.metadatas)
            all_labels.extend([coll] * len(result))
            all_distances.extend(result.distances)
        except Exception as e:
            # Don't kill the whole query if one collection misbehaves —
            # but make the failure visible so it can be diagnosed.
            logger.warning("Query failed for collection %r: %s", coll, e)
            continue

    if not all_docs:
        return [], [], []

    # Sort by L2 distance ascending (lower = more relevant), keep top CONTEXT_CAP
    ranked = sorted(
        zip(all_distances, all_docs, all_metas, all_labels),
        key=lambda x: x[0],
    )[:CONTEXT_CAP]

    _, documents, metadatas, labels = zip(*ranked)
    return list(documents), list(metadatas), list(labels)


def retrieve_chunks_multistate(
    question: str,
    collections: list[str],
    base_filters: dict | None,
    states: list[str],
) -> tuple[list[str], list[dict], list[str]]:
    """Multi-state retrieval with per-state balance.

    When the query mentions 2+ states, a single OR-filtered query lets
    the semantically-richer state dominate the top results (e.g. Ohio's
    detailed ORC chapters squeeze out Indiana's sparser content). To
    ensure each state gets representation, run a separate per-state
    query for each state, plus a state-agnostic query to surface
    untagged content (educational concepts).

    Results are merged and re-ranked by L2 distance, then capped at
    CONTEXT_CAP — so the final ranking is still distance-based but each
    state had a fair shot at contributing candidates.
    """
    # Budget per call — leave room for the state-agnostic pull too
    per_call = max(2, CHUNKS_PER_COLLECTION // (len(states) + 1))

    all_docs: list[str] = []
    all_metas: list[dict] = []
    all_labels: list[str] = []
    all_distances: list[float] = []

    def _run(filters: dict | None) -> None:
        for coll in collections:
            try:
                result = query(question, n_results=per_call, filters=filters, collection_name=coll)
                all_docs.extend(result.documents)
                all_metas.extend(result.metadatas)
                all_labels.extend([coll] * len(result))
                all_distances.extend(result.distances)
            except Exception as e:
                logger.warning("Multi-state query failed (%s): %s", coll, e)

    # Per-state pulls — each state gets its own quota
    for state in states:
        state_only = {"$or": [{"state": state}, {"state": ""}]}
        _run(merge_filters(base_filters, state_only))

    # State-agnostic pull — catches untagged content if it ranked weakly
    # against the per-state filtered pools
    untagged_only = {"state": ""}
    _run(merge_filters(base_filters, untagged_only))

    if not all_docs:
        return [], [], []

    # Deduplicate while preserving lowest distance — chunks can show up
    # in multiple per-state pulls if state="" matched
    seen: dict[str, int] = {}  # chunk text -> index into lists
    for i, doc in enumerate(all_docs):
        if doc in seen:
            existing = seen[doc]
            if all_distances[i] < all_distances[existing]:
                seen[doc] = i
        else:
            seen[doc] = i

    indices = sorted(seen.values(), key=lambda i: all_distances[i])[:CONTEXT_CAP]
    return (
        [all_docs[i] for i in indices],
        [all_metas[i] for i in indices],
        [all_labels[i] for i in indices],
    )


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
