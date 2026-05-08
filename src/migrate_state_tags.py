# migrate_state_tags.py — back-fill state metadata on chunks that lack it.
#
# Run via the CLI:
#   python main.py migrate                                  # default: regulatory + OH
#   python main.py migrate --collection regulatory --state IN
#   python main.py migrate --dry-run                        # preview only
#
# Originally written as a one-shot to tag pre-existing Ohio chunks, but kept
# around as a generic utility since it's idempotent — only chunks with no
# state tag are touched. Useful any time a collection gets bulk-imported
# without state metadata.

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from db import get_collection


def migrate(collection_name: str, state_code: str, dry_run: bool = False) -> None:
    """Add state_code to all chunks in collection_name that have no state tag."""
    collection = get_collection(collection_name)
    all_data = collection.get(include=["metadatas"])

    ids_to_update = []
    new_metadatas = []

    for chunk_id, meta in zip(all_data["ids"], all_data["metadatas"]):
        if not meta.get("state"):
            ids_to_update.append(chunk_id)
            new_metadatas.append({**meta, "state": state_code})

    if not ids_to_update:
        print(f"[{collection_name}] All chunks already have a state tag — nothing to do.")
        return

    print(f"[{collection_name}] {len(ids_to_update)} chunk(s) missing state tag.")

    if dry_run:
        print("  Dry run — no changes made. Re-run without --dry-run to apply.")
        return

    collection.update(ids=ids_to_update, metadatas=new_metadatas)
    print(f"  Tagged {len(ids_to_update)} chunk(s) with state: {state_code}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Back-fill state metadata on existing regulatory chunks."
    )
    parser.add_argument(
        "--collection",
        default="regulatory",
        help="Collection to migrate (default: regulatory)",
    )
    parser.add_argument(
        "--state",
        default="OH",
        help="State code to apply to untagged chunks (default: OH)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing anything",
    )
    args = parser.parse_args()

    migrate(args.collection, args.state, dry_run=args.dry_run)
