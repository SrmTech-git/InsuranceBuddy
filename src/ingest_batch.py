# ingest_batch.py — scan data/raw/ subfolders and embed into ChromaDB
# Subfolder name determines collection: regulatory/ -> regulatory, educational/ -> educational

import argparse
from pathlib import Path
from embed import embed_document, get_collection, document_exists
from ingest import parse_filename

RAW_DIR = Path("data/raw")
SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx", ".xlsx"}


def find_files(collection_override: str | None = None) -> list[tuple[Path, str]]:
    """Scan data/raw/ subfolders and return (file_path, collection_name) pairs.

    If collection_override is set, only scan that subfolder.
    Otherwise, scan all subfolders and infer collection from folder name.
    """

    files = []

    if collection_override:
        # Only scan the specified subfolder
        subfolders = [RAW_DIR / collection_override]
    else:
        # Scan all subfolders
        subfolders = sorted(
            p for p in RAW_DIR.iterdir() if p.is_dir()
        )

    for subfolder in subfolders:
        if not subfolder.exists():
            print(f"Warning: {subfolder} does not exist, skipping.")
            continue

        collection_name = subfolder.name

        for filepath in sorted(subfolder.iterdir()):
            if filepath.suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append((filepath, collection_name))

    return files


def ingest_all(force: bool = False, collection_override: str | None = None) -> None:
    """Find all supported files in data/raw/ subfolders and embed each one."""

    files = find_files(collection_override)

    if not files:
        print("No supported files found in data/raw/ subfolders.")
        return

    total = len(files)
    succeeded = 0
    skipped = 0
    failed = 0

    print(f"Found {total} file(s) to process\n")

    for i, (filepath, collection_name) in enumerate(files, 1):
        filename = filepath.name
        subfolder = filepath.parent.name
        print(f"[{i}/{total}] {subfolder}/ -> {collection_name}")
        print(f"         {filename}")

        try:
            # Quick duplicate check before doing the full load-and-split
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

            # Run the full embed pipeline
            embed_document(str(filepath), force=force, collection_name=collection_name)
            succeeded += 1

        except Exception as e:
            print(f"         FAILED: {e}\n")
            failed += 1

        print()

    # Final summary
    print("=" * 60)
    print("Batch ingestion complete!")
    if collection_override:
        print(f"  Collection: {collection_override}")
    else:
        print("  Collections: inferred from subfolders")
    print(f"  Succeeded: {succeeded}")
    print(f"  Skipped:   {skipped} (duplicates)")
    print(f"  Failed:    {failed}")
    print(f"  Total:     {total}")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch ingest files into ChromaDB")
    parser.add_argument(
        "--collection",
        choices=["regulatory", "educational"],
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
