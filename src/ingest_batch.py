# ingest_batch.py — scan data/raw/ subfolders and embed into ChromaDB
#
# Folder layout:
#   data/raw/{collection}/                    → flat collection, no state tag
#   data/raw/{collection}/{state_folder}/     → collection + state tag
#   data/raw/regulatory/reference/            → xlsx files, state tags applied per-chunk
#
# Collection is always inferred from the top-level subfolder name.
# State is inferred from the second-level subfolder name via STATE_FOLDER_MAP.

import argparse
from pathlib import Path
from embed import embed_document, embed_chunks, get_collection, document_exists
from ingest import parse_filename
from ingest_xlsx import load_xlsx_by_state

RAW_DIR = Path("data/raw")
SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx"}
XLSX_EXTENSIONS = {".xlsx"}

# Maps state subfolder names → two-letter state codes.
# Add entries here as new state folders are created.
STATE_FOLDER_MAP: dict[str, str] = {
    "ohio": "OH",
    "indiana": "IN",
    "illinois": "IL",
    "kentucky": "KY",
    "minnesota": "MN",
    "virginia": "VA",
    "michigan": "MI",
    "georgia": "GA",
    "tennessee": "TN",
    "iowa": "IA",
    "wisconsin": "WI",
}

# Subfolders whose files carry their own per-chunk state tags (xlsx processing)
SELF_TAGGED_FOLDERS = {"reference"}


def find_files(
    collection_override: str | None = None,
) -> list[tuple[Path, str, str]]:
    """Scan data/raw/ and return (file_path, collection_name, state_code) triples.

    Handles two layouts:
      - Flat:   data/raw/educational/doc.txt   → ("educational", "")
      - Nested: data/raw/regulatory/ohio/f.pdf → ("regulatory", "OH")
      - Ref:    data/raw/regulatory/reference/ → ("regulatory", "SELF") — xlsx only
    """
    files: list[tuple[Path, str, str]] = []

    top_dirs = (
        [RAW_DIR / collection_override]
        if collection_override
        else sorted(p for p in RAW_DIR.iterdir() if p.is_dir())
    )

    for top_dir in top_dirs:
        if not top_dir.exists():
            print(f"Warning: {top_dir} does not exist, skipping.")
            continue

        collection_name = top_dir.name

        for entry in sorted(top_dir.iterdir()):
            if entry.is_file():
                # Flat layout — file directly in collection folder
                ext = entry.suffix.lower()
                if ext in SUPPORTED_EXTENSIONS or ext in XLSX_EXTENSIONS:
                    files.append((entry, collection_name, ""))

            elif entry.is_dir():
                # Nested layout — subfolder = state or reference
                subfolder = entry.name.lower()
                if subfolder in SELF_TAGGED_FOLDERS:
                    state_code = "SELF"  # xlsx handles its own state tags
                else:
                    state_code = STATE_FOLDER_MAP.get(subfolder, "")

                for filepath in sorted(entry.iterdir()):
                    ext = filepath.suffix.lower()
                    if ext in SUPPORTED_EXTENSIONS or ext in XLSX_EXTENSIONS:
                        files.append((filepath, collection_name, state_code))

    return files


def _ingest_xlsx(
    filepath: Path,
    collection_name: str,
    force: bool,
) -> tuple[int, int, int]:
    """Ingest a multi-state xlsx file. Returns (succeeded, skipped, failed) counts."""
    succeeded = skipped = failed = 0

    try:
        state_docs = load_xlsx_by_state(str(filepath))
    except Exception as e:
        print(f"         FAILED to parse xlsx: {e}\n")
        return 0, 0, 1

    collection = get_collection(collection_name)

    for state_code, chunks in state_docs:
        if not chunks:
            continue

        state_filename = chunks[0].metadata.get("filename", "")
        print(f"         [{state_code}] {len(chunks)} chunk(s) -> {state_filename}")

        if not force:
            existing = document_exists(collection, "", state_filename)
            if existing:
                print(f"         Skipped (duplicate: {state_filename})")
                skipped += 1
                continue

        try:
            embed_chunks(chunks, collection_name=collection_name, state=state_code, force=force)
            succeeded += 1
        except Exception as e:
            print(f"         FAILED [{state_code}]: {e}")
            failed += 1

    return succeeded, skipped, failed


def ingest_all(force: bool = False, collection_override: str | None = None) -> None:
    """Find all supported files in data/raw/ and embed each one."""
    files = find_files(collection_override)

    if not files:
        print("No supported files found in data/raw/ subfolders.")
        return

    total = len(files)
    succeeded = skipped = failed = 0

    print(f"Found {total} file(s) to process\n")

    for i, (filepath, collection_name, state_code) in enumerate(files, 1):
        state_label = f" [{state_code}]" if state_code and state_code != "SELF" else ""
        print(f"[{i}/{total}] {collection_name}/{filepath.parent.name}/{filepath.name}{state_label}")

        # xlsx files in reference/ get special per-state processing
        if filepath.suffix.lower() in XLSX_EXTENSIONS:
            s, sk, f = _ingest_xlsx(filepath, collection_name, force)
            succeeded += s
            skipped += sk
            failed += f
            print()
            continue

        try:
            meta = parse_filename(str(filepath))
            form_number = meta.get("form_number", "")
            filename = meta.get("filename", "")

            if not force:
                collection = get_collection(collection_name)
                existing = document_exists(collection, form_number, filename)
                if existing:
                    label = form_number or filename
                    print(f"         Skipped (duplicate: {label})\n")
                    skipped += 1
                    continue

            embed_document(
                str(filepath),
                force=force,
                collection_name=collection_name,
                state=state_code,
            )
            succeeded += 1

        except Exception as e:
            print(f"         FAILED: {e}\n")
            failed += 1

        print()

    print("=" * 60)
    print("Batch ingestion complete!")
    print(f"  Collection: {collection_override or 'all'}")
    print(f"  Succeeded: {succeeded}")
    print(f"  Skipped:   {skipped} (duplicates)")
    print(f"  Failed:    {failed}")
    print(f"  Total:     {total}")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch ingest files into ChromaDB")
    parser.add_argument(
        "--collection",
        default=None,
        help="Override collection (default: infer from subfolder name)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing documents",
    )
    args = parser.parse_args()
    ingest_all(force=args.force, collection_override=args.collection)
