# chunkers — pluggable per-collection chunking strategies
#
# Each collection's documents have different natural structures (concept
# docs use section headers; statute PDFs use lettered subsections; ACORD
# library cards are atomic units). One generic chunker can't respect all
# of those boundaries, so we register a chunker per collection.
#
# Adding a new chunker: write a function matching the Chunker protocol
# in base.py and register it in CHUNKER_REGISTRY below. Unregistered
# collections fall back to the default chunker.

from chunkers.base import Chunker
from chunkers.default import default_chunker
from chunkers.educational import educational_chunker

# Registry: collection name -> chunker function.
# Add new entries as collection-specific chunkers are written.
CHUNKER_REGISTRY: dict[str, Chunker] = {
    "educational": educational_chunker,
    # "forms":       forms_chunker,         # Phase 3
    # "regulatory":  regulatory_chunker,    # Phase 4
}


def get_chunker(collection_name: str) -> Chunker:
    """Return the chunker registered for this collection, or the default."""
    return CHUNKER_REGISTRY.get(collection_name, default_chunker)
