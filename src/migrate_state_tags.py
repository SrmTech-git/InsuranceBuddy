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
