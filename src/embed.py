# embedding and storing in chromadb

import hashlib
import chromadb
from db import get_collection
from ingest import load_and_split


# These are the metadata keys we pass through to ChromaDB
METADATA_KEYS = ["form_number", "edition_date", "description", "filename", "parsed", "state"]


def document_exists(
    collection: chromadb.Collection,
    form_number: str,
    filename: str = "",
) -> dict | None:
    """Check if a document is already in the collection.

    Queries by form_number when available; falls back to filename for
    documents that have no form number (e.g. plain educational docs).
    Returns the first matching chunk's metadata if found, None otherwise.
    """
    if form_number:
        where = {"form_number": form_number}
    elif filename:
        where = {"filename": filename}
    else:
        return None

    results = collection.get(where=where, limit=1)
    return results["metadatas"][0] if results["ids"] else None


def embed_chunks(
    chunks: list,
    collection_name: str = "regulatory",
    state: str = "",
    force: bool = False,
) -> chromadb.Collection:
    """Store pre-built chunks in ChromaDB.

    Lower-level function used by embed_document() and xlsx ingestion.
    Handles deduplication, force-overwrite, ID generation, and storage.
    """
    if not chunks:
        print("No chunks to store.")
        return get_collection(collection_name)

    # Inject state into every chunk's metadata
    for chunk in chunks:
        chunk.metadata["state"] = state

    file_meta = {k: chunks[0].metadata.get(k, "") for k in METADATA_KEYS}
    form_number = file_meta["form_number"]
    filename = file_meta["filename"]
    collection = get_collection(collection_name)

    if not force:
        existing = document_exists(collection, form_number, filename)
        if existing:
            print()
            print("-" * 60)
            print("WARNING: Document already exists in the collection!")
            print(f"  Form number:  {existing.get('form_number', 'N/A')}")
            print(f"  Edition date: {existing.get('edition_date', 'N/A')}")
            print(f"  Filename:     {existing.get('filename', 'N/A')}")
            print(f"  State:        {existing.get('state', '(none)')}")
            print()
            print("  Skipping re-embedding to avoid duplicates.")
            print("  To overwrite, re-run with force=True")
            print("-" * 60)
            return collection

    if force:
        where = {"form_number": form_number} if form_number else {"filename": filename}
        existing_chunks = collection.get(where=where)
        if existing_chunks["ids"]:
            label = form_number or filename
            print(f"\nRemoving {len(existing_chunks['ids'])} existing chunks for {label}...")
            collection.delete(ids=existing_chunks["ids"])

    documents = [chunk.page_content for chunk in chunks]
    metadatas = [{k: chunk.metadata.get(k, "") for k in METADATA_KEYS} for chunk in chunks]

    # ID prefix: form_number > filename_hash. Include state so per-state xlsx
    # chunks from the same file don't collide (e.g. StateSpreadSheet_OH_0).
    if form_number:
        id_prefix = form_number
    else:
        base = hashlib.sha1(filename.encode()).hexdigest()[:8]
        id_prefix = f"{base}_{state}" if state else base

    ids = [f"{id_prefix}_{i}" for i in range(len(chunks))]

    collection.add(documents=documents, metadatas=metadatas, ids=ids)

    print()
    print("=" * 60)
    print(f"Embedding complete! (collection: {collection_name})")
    print(f"  Form number:  {file_meta['form_number'] or '(none)'}")
    print(f"  Edition date: {file_meta['edition_date'] or '(none)'}")
    print(f"  State:        {state or '(none)'}")
    print(f"  Chunks stored: {len(chunks)}")
    print(f"  Total vectors in collection: {collection.count()}")
    print("=" * 60)

    return collection


def embed_document(
    file_path: str,
    force: bool = False,
    collection_name: str = "regulatory",
    state: str = "",
) -> chromadb.Collection:
    """Embed a single document end-to-end: parse, chunk, embed, store."""
    chunks = load_and_split(file_path, collection_name=collection_name)
    if not chunks:
        print("No chunks created — nothing to store.")
        return get_collection(collection_name)
    return embed_chunks(chunks, collection_name=collection_name, state=state, force=force)


if __name__ == "__main__":
    # Use the batch ingester instead of running this directly:
    #   python main.py ingest
    print("Run `python main.py ingest` to embed documents from data/raw/.")
