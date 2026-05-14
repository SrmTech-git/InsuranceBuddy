# chunkers/default.py — generic character-based chunker
#
# Wraps LangChain's RecursiveCharacterTextSplitter. Used as the fallback
# for any collection without a registered chunker. Preserves the existing
# behavior from before chunkers were pluggable, so unregistered
# collections keep working unchanged.

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_SIZE, CHUNK_OVERLAP


def default_chunker(
    pages: list[Document],
    file_metadata: dict,
) -> list[Document]:
    """Split pages using RecursiveCharacterTextSplitter, attach file metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(pages)

    for chunk in chunks:
        chunk.metadata.update(file_metadata)

    return chunks
