# chunkers/base.py — Chunker protocol
#
# A chunker takes a list of LangChain Documents (the loader's output —
# one or more "pages" of text with metadata) plus the file-level metadata
# parsed from the filename, and returns a list of chunks ready to embed.
#
# The protocol is intentionally narrow: input is text + metadata, output
# is chunks. Each chunker decides how to split — by character count, by
# section headers, by structural unit, or not at all (atomic).

from typing import Protocol
from langchain_core.documents import Document


class Chunker(Protocol):
    """Chunker takes loaded pages + file metadata and returns chunks.

    Implementations should:
    - Respect the doc's natural structural boundaries when possible
    - Attach file_metadata to every chunk's metadata dict
    - Optionally enrich chunk text with breadcrumbs (section path) for
      richer embedding and clearer LLM context
    """

    def __call__(
        self,
        pages: list[Document],
        file_metadata: dict,
    ) -> list[Document]:
        ...
