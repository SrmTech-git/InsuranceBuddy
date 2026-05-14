# chunkers/educational.py — section-aware chunker for educational content
#
# Educational .txt docs in this project follow a consistent structure:
#
#   Document Title Here
#   ===================
#
#   Optional intro.
#
#
#   MAJOR SECTION HEADER
#   ====================
#
#   Body of the major section.
#
#   Subsection header:
#   Body of the subsection. Multiple paragraphs allowed.
#
#   Another subsection:
#   ...
#
#
# This chunker parses that structure and produces chunks of the shape:
#
#   [Doc Title > MAJOR SECTION > Subsection Header]
#
#   <subsection body>
#
# The breadcrumb prefix does two jobs:
# 1. Embedding signal — short keyword queries like "Part C" or "duty to
#    cooperate" hit the breadcrumb's tokens directly, surfacing the right
#    chunk instead of being lost in body-level semantic noise
# 2. LLM context — the model sees exactly which doc section it's reading
#    when assembling the answer
#
# Docs without recognizable section structure (most .docx files, some
# free-form .txt) fall back to the default character chunker, so this
# chunker never regresses on already-working content.

import re
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_SIZE, CHUNK_OVERLAP
from chunkers.default import default_chunker


# Section underline: 3+ '=' chars on their own line
_UNDERLINE_RE = re.compile(r"^={3,}\s*$")

# Subsection header heuristic: a standalone line that
# - starts with an uppercase letter, digit, or paren (covers headers like
#   "Part C ...", "1. ...", "(A) Definitions:")
# - ends with ':'
# - is shorter than 100 chars (avoids matching sentences that happen to
#   end with a colon)
# - contains no period before the trailing colon (excludes prose
#   sentences with mid-line punctuation patterns)
_SUBSECTION_RE = re.compile(r"^([A-Z0-9(][^:\n.]{1,100}):\s*$")


def _parse_major_sections(text: str) -> list[tuple[str, list[str]]]:
    """Split text into [(header, body_lines)] using '===' underlines.

    The first entry's header is the document title; subsequent entries
    are major sections. Returns empty list if no underline structure is
    found — caller should fall back to default chunker in that case.
    """
    lines = text.split("\n")
    sections: list[tuple[str, list[str]]] = []
    current_header: str | None = None
    current_body: list[str] = []

    i = 0
    while i < len(lines):
        line = lines[i]
        next_line = lines[i + 1] if i + 1 < len(lines) else ""

        if _UNDERLINE_RE.match(next_line) and line.strip():
            # Save the previous section before starting a new one
            if current_header is not None:
                sections.append((current_header, current_body))
            current_header = line.strip()
            current_body = []
            i += 2  # skip header line + underline line
            continue

        if current_header is None:
            # Pre-title content — discard (usually blank lines)
            i += 1
            continue

        current_body.append(line)
        i += 1

    if current_header is not None:
        sections.append((current_header, current_body))

    return sections


def _split_subsections(body_lines: list[str]) -> list[tuple[str | None, list[str]]]:
    """Group body lines into [(subsection_header_or_None, body_lines)].

    When a subsection header is followed by ANOTHER subsection header
    with no body between them, the first is carried forward as a parent
    prefix on the next group's breadcrumb. This preserves the parent
    header in cases like:

        Part D — Coverage for Damage to Your Auto:
        Two sub-coverages:
        - Collision: ...

    where 'Part D —' would otherwise be dropped because its body is
    empty.
    """
    groups: list[tuple[str | None, list[str]]] = []
    current_header: str | None = None
    pending_parent: str | None = None
    current_lines: list[str] = []

    def _join_with_parent(header: str | None) -> str | None:
        if pending_parent and header:
            return f"{pending_parent} > {header}"
        return pending_parent or header

    for line in body_lines:
        m = _SUBSECTION_RE.match(line)
        if m:
            new_header = m.group(1).strip()
            has_body = any(s.strip() for s in current_lines)

            if not has_body and current_header is not None:
                # Header-only group — carry forward as a parent prefix
                pending_parent = _join_with_parent(current_header)
            elif current_header is not None or current_lines:
                groups.append((_join_with_parent(current_header), current_lines))
                pending_parent = None

            current_header = new_header
            current_lines = []
        else:
            current_lines.append(line)

    has_body = any(s.strip() for s in current_lines)
    if current_header is not None or has_body:
        groups.append((_join_with_parent(current_header), current_lines))

    return groups


def _build_breadcrumb(parts: list[str]) -> str:
    """Render '[A > B > C]' from a list of section labels, skipping empties."""
    filtered = [p.strip() for p in parts if p and p.strip()]
    if not filtered:
        return ""
    return "[" + " > ".join(filtered) + "]"


def _make_chunk_text(breadcrumb: str, body: str) -> str:
    """Combine breadcrumb and body into the chunk's embedded text."""
    body = body.strip()
    if breadcrumb:
        return f"{breadcrumb}\n\n{body}"
    return body


def educational_chunker(
    pages: list[Document],
    file_metadata: dict,
) -> list[Document]:
    """Chunk an educational doc by section structure with breadcrumb prefixes.

    Falls back to the default chunker if the doc has no recognizable
    section structure (no '===' underlines found).
    """
    # Concatenate all loaded pages — educational docs are typically one
    # page anyway, but this is robust to multi-page sources
    full_text = "\n\n".join(p.page_content for p in pages)

    sections = _parse_major_sections(full_text)

    # No structure detected — fall back to default behavior. This handles
    # .docx files (which lose underline structure on conversion) and any
    # free-form .txt that doesn't follow the convention.
    if len(sections) < 2:
        return default_chunker(pages, file_metadata)

    doc_title = sections[0][0]
    major_sections = sections[1:]  # everything after the title

    chunks: list[Document] = []

    # Splitter used only for oversized subsections — applies the same
    # CHUNK_SIZE/CHUNK_OVERLAP as the default chunker so chunk sizes
    # stay in the same ballpark
    long_body_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    for section_header, section_body in major_sections:
        subsections = _split_subsections(section_body)

        for sub_header, sub_lines in subsections:
            body_text = "\n".join(sub_lines).strip()
            if not body_text:
                continue

            breadcrumb = _build_breadcrumb([doc_title, section_header, sub_header or ""])

            # If body is comfortably within chunk size, emit as one chunk
            chunk_text = _make_chunk_text(breadcrumb, body_text)
            if len(chunk_text) <= CHUNK_SIZE + CHUNK_OVERLAP:
                chunks.append(Document(page_content=chunk_text, metadata={}))
                continue

            # Body is too long — split it and prepend the breadcrumb to
            # each split so every chunk carries its location
            sub_splits = long_body_splitter.split_text(body_text)
            for piece in sub_splits:
                chunks.append(
                    Document(
                        page_content=_make_chunk_text(breadcrumb, piece),
                        metadata={},
                    )
                )

    # Attach file metadata to every chunk
    for chunk in chunks:
        chunk.metadata.update(file_metadata)

    return chunks
