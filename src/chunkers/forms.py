# chunkers/forms.py — atomic chunker for forms library cards
#
# The forms collection is a "card catalog, not a full-text index" — each
# document is a short self-contained library card (form number, edition,
# purpose, captures, when used, notes). The natural chunk size is the
# whole card; splitting a card mid-content would break the embedding's
# semantic coherence and risk retrieving "purpose" without "captures",
# "when used" without "notes", etc.
#
# This chunker concatenates all loader-emitted pages into one chunk per
# input document, no character-based splitting. Cards average ~500 chars;
# the largest (E&O, professional liability) reach ~2400 chars — still
# comfortably inside any sensible embedding context window.

from langchain_core.documents import Document


def forms_chunker(
    pages: list[Document],
    file_metadata: dict,
) -> list[Document]:
    """Return one chunk per input file. Concatenates pages if multiple."""
    full_text = "\n\n".join(p.page_content for p in pages if p.page_content.strip())
    if not full_text:
        return []
    chunk = Document(page_content=full_text, metadata=dict(file_metadata))
    return [chunk]
