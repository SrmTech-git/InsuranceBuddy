# embedding and storing in chromadb

import hashlib
import chromadb
from db import get_collection
from ingest import load_and_split


# These are the metadata keys we pass through to ChromaDB
METADATA_KEYS = ["form_number", "edition_date", "description", "filename", "parsed"]


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


def embed_document(file_path: str, force: bool = False, collection_name: str = "regulatory") -> chromadb.Collection:
    """Embed a single document end-to-end: parse, chunk, embed, store.

    Args:
        file_path: Path to the PDF file.
        force: If True, overwrite existing chunks for this form number.
               If False (default), skip documents that already exist.
        collection_name: Which collection to store in — "regulatory" or "educational".
    """

    # Load and split the PDF — this also parses metadata from the filename
    chunks = load_and_split(file_path)

    if not chunks:
        print("No chunks created — nothing to store.")
        return get_collection(collection_name)

    # Grab the parsed metadata from the first chunk (same for all chunks)
    file_meta = {k: chunks[0].metadata.get(k, "") for k in METADATA_KEYS}
    form_number = file_meta["form_number"]

    filename = file_meta["filename"]
    collection = get_collection(collection_name)

    # Check for duplicates by form_number, falling back to filename
    if not force:
        existing = document_exists(collection, form_number, filename)
        if existing:
            print()
            print("-" * 60)
            print("WARNING: Document already exists in the collection!")
            print(f"  Form number:  {existing.get('form_number', 'N/A')}")
            print(f"  Edition date: {existing.get('edition_date', 'N/A')}")
            print(f"  Filename:     {existing.get('filename', 'N/A')}")
            print()
            print("  Skipping re-embedding to avoid duplicates.")
            print("  To overwrite, re-run with force=True")
            print("-" * 60)
            return collection

    # If force=True, remove existing chunks before re-embedding
    if force:
        where = {"form_number": form_number} if form_number else {"filename": filename}
        existing_chunks = collection.get(where=where)
        if existing_chunks["ids"]:
            label = form_number or filename
            print(f"\nRemoving {len(existing_chunks['ids'])} existing chunks for {label}...")
            collection.delete(ids=existing_chunks["ids"])

    # Prepare data for ChromaDB — only pass through our metadata keys
    documents = [chunk.page_content for chunk in chunks]
    metadatas = [{k: chunk.metadata.get(k, "") for k in METADATA_KEYS} for chunk in chunks]
    # Use form_number as the ID prefix when available; fall back to a short
    # hash of the filename so documents without form numbers don't collide.
    if form_number:
        id_prefix = form_number
    else:
        id_prefix = hashlib.sha1(file_meta["filename"].encode()).hexdigest()[:8]
    ids = [f"{id_prefix}_{i}" for i in range(len(chunks))]

    # Store everything in the collection
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
    )

    # Print summary
    print()
    print("=" * 60)
    print(f"Embedding complete! (collection: {collection_name})")
    print(f"  Form number:  {file_meta['form_number'] or '(none)'}")
    print(f"  Edition date: {file_meta['edition_date'] or '(none)'}")
    print(f"  Chunks stored: {len(chunks)}")
    print(f"  Total vectors in collection: {collection.count()}")
    print("=" * 60)

    return collection


if __name__ == "__main__":
    pdf_path = "data/raw/2020 - Residential Purchase Contract (CBR)  (28).pdf"
    embed_document(pdf_path)
