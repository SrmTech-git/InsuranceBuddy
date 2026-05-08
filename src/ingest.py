# document loading and chunking

import re
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def parse_filename(file_path: str) -> dict:
    """Extract form number, edition date, and description from a PDF filename.

    Parsing strategy:
    1. Use regex to find a form number, edition date, and description
       directly from the full path string — avoids os.path.basename which
       misinterprets '/' in dates like '02/2021' as path separators on Windows.
    2. Fall back gracefully if any part is missing.
    """

    form_number = ""
    edition_date = ""
    description = ""
    parsed = True

    # Master pattern that captures all three parts in one pass:
    #   form_number  = 2-4 uppercase letters + optional space + digits
    #   edition_date = parenthesized group right after the form number
    #   description  = whatever text follows
    pattern = (
        r"([A-Z]{2,4}\s?\d+(?:[.\-]\d+)*)"   # group 1: form number
        r"\s*\(([^)]+)\)"        # group 2: edition date in parens
        r"\s*(.+?)\.(?:pdf|txt|docx)"    # group 3: description before extension
    )
    full_match = re.search(pattern, file_path, re.IGNORECASE)

    if full_match:
        form_number = full_match.group(1).strip()
        edition_date = full_match.group(2).strip()
        description = full_match.group(3).strip(" -–—")
    else:
        # Try matching just a form number (no edition date)
        partial = re.search(
            r"([A-Z]{2,4}\s?\d+(?:[.\-]\d+)*)\s*(.+?)\.(?:pdf|txt|docx)",
            file_path, re.IGNORECASE,
        )
        if partial:
            form_number = partial.group(1).strip()
            remainder = partial.group(2).strip(" -–—")
            # Check if remainder starts with a parenthesized group
            date_match = re.match(r"\(([^)]+)\)\s*(.*)", remainder)
            if date_match:
                edition_date = date_match.group(1).strip()
                description = date_match.group(2).strip(" -–—")
            else:
                description = remainder
        else:
            # No form number found at all — pull description from the filename
            # Strip directory prefixes and extension manually
            name = re.sub(r"\.(?:pdf|txt|docx)$", "", file_path, flags=re.IGNORECASE)
            # Remove any directory path (split on / and \ )
            name = re.split(r"[\\/]", name)[-1]
            description = name.strip()
            parsed = False

    # If we got a form number but nothing else, flag as partially parsed
    if form_number and not edition_date and not description:
        parsed = False

    # Build display filename by stripping directory prefixes.
    # We strip on '\' always, and strip on '/' only when the slash
    # appears before any parenthesized group (real dir separator,
    # not a date like '02/2021' inside parens).
    display_name = file_path.rsplit("\\", 1)[-1]
    # Find the position of the first '(' — slashes before it are directories
    paren_pos = display_name.find("(")
    if paren_pos == -1:
        # No parens at all — safe to split on '/' normally
        display_name = display_name.rsplit("/", 1)[-1]
    else:
        # Only strip directory slashes that appear before the first '('
        prefix = display_name[:paren_pos]
        if "/" in prefix:
            dir_end = prefix.rfind("/") + 1
            display_name = display_name[dir_end:]

    metadata = {
        "form_number": form_number,
        "edition_date": edition_date,
        "description": description,
        "filename": display_name,
        "parsed": parsed,
    }

    return metadata


def _load_docx(file_path: str) -> list[Document]:
    """Extract text from a .docx file and return a single LangChain Document."""
    from docx import Document as DocxDocument

    doc = DocxDocument(file_path)
    text = "\n\n".join(para.text for para in doc.paragraphs if para.text.strip())
    return [Document(page_content=text, metadata={"source": file_path})]


def _load_xlsx(file_path: str) -> list[Document]:
    """Convert an Excel spreadsheet into natural-language Document chunks.

    Designed for the StateSpreadSheet format: tabular state-by-state data
    with categories in rows and states in columns.  Each state + category
    combination becomes one chunk so that queries like "What are Ohio's
    liability minimums?" retrieve a compact, semantically meaningful block.
    """
    import openpyxl

    wb = openpyxl.load_workbook(file_path, read_only=True)
    filename = re.split(r"[\\/]", file_path)[-1]
    docs: list[Document] = []

    # ------------------------------------------------------------------
    # Sheet 1: "State Auto Requirements" — detailed per-category data
    # ------------------------------------------------------------------
    ws = wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))

    # Build a map of column index -> state name from the header row (index 3).
    header = rows[3]
    state_cols: dict[int, str] = {}
    skip_labels = {"Category", "Data Point", "Notes / Key Differences", "", None}
    for i, val in enumerate(header):
        if val and str(val).strip() not in skip_labels:
            state_cols[i] = str(val).strip()

    # Find the notes column (if present).
    notes_col: int | None = None
    for i, val in enumerate(header):
        if val and "Notes" in str(val):
            notes_col = i
            break

    # Walk data rows, grouping by category.  Column 0 = category (carried
    # forward when blank), column 1 = data point.  Rows where column 1 is
    # blank or equals "Data Point" are section headers — skip them.
    current_category = ""
    # {state: [(data_point, value, notes), ...]}
    category_rows: dict[str, list[tuple[str, str, str]]] = {}

    def _flush_category() -> None:
        """Emit one Document per state for the current category group."""
        nonlocal category_rows
        if not current_category or not category_rows:
            category_rows = {}
            return
        for state, entries in category_rows.items():
            lines = [f"{state} — {current_category}"]
            for dp, val, note in entries:
                lines.append(f"{dp}: {val}")
                if note:
                    lines.append(f"  Note: {note}")
            text = "\n".join(lines)
            docs.append(Document(
                page_content=text,
                metadata={
                    "source": file_path,
                    "form_number": f"StateReq-{state}",
                    "edition_date": "",
                    "description": current_category,
                    "filename": filename,
                    "parsed": True,
                },
            ))
        category_rows = {}

    for row in rows[4:]:  # skip title rows 0-3
        cat_cell = str(row[0]).strip() if row[0] else ""
        dp_cell = str(row[1]).strip() if row[1] else ""

        # Skip section dividers and repeated headers.
        if not dp_cell or dp_cell == "Data Point":
            # A new section title with no data point means a new category
            # group is about to start — flush what we have.
            if cat_cell and cat_cell != "Category":
                _flush_category()
            continue

        # Track the current category.
        if cat_cell and cat_cell != "Category":
            if cat_cell != current_category:
                _flush_category()
                current_category = cat_cell

        # Collect this data point for every state.
        notes_val = str(row[notes_col]).strip() if notes_col and row[notes_col] else ""
        for col_idx, state_name in state_cols.items():
            val = str(row[col_idx]).strip() if row[col_idx] else ""
            if not val:
                continue
            category_rows.setdefault(state_name, []).append(
                (dp_cell, val, notes_val)
            )

    _flush_category()  # flush the last group

    # ------------------------------------------------------------------
    # Sheet 2: "Quick Reference" — one chunk per state
    # ------------------------------------------------------------------
    if len(wb.worksheets) >= 2:
        ws2 = wb.worksheets[1]
        rows2 = list(ws2.iter_rows(values_only=True))
        if len(rows2) > 2:
            # Row 1 is the header: col 0 = label, cols 1..N = state names
            qr_header = rows2[1]
            qr_states: dict[int, str] = {}
            for i, val in enumerate(qr_header):
                if i == 0 or not val:
                    continue
                qr_states[i] = str(val).strip()

            for col_idx, state_name in qr_states.items():
                lines = [f"{state_name} — Quick Reference"]
                for row in rows2[2:]:
                    label = str(row[0]).strip() if row[0] else ""
                    val = str(row[col_idx]).strip() if col_idx < len(row) and row[col_idx] else ""
                    if label and val:
                        lines.append(f"{label}: {val}")
                if len(lines) > 1:
                    docs.append(Document(
                        page_content="\n".join(lines),
                        metadata={
                            "source": file_path,
                            "form_number": f"StateReq-{state_name}",
                            "edition_date": "",
                            "description": "Quick Reference",
                            "filename": filename,
                            "parsed": True,
                        },
                    ))

    # ------------------------------------------------------------------
    # Sheet 3: "Notes & Sources" — one single chunk
    # ------------------------------------------------------------------
    if len(wb.worksheets) >= 3:
        ws3 = wb.worksheets[2]
        rows3 = list(ws3.iter_rows(values_only=True))
        lines = ["State Auto Insurance — Notes & Sources"]
        for row in rows3[2:]:  # skip title and header
            topic = str(row[0]).strip() if row[0] else ""
            note = str(row[1]).strip() if len(row) > 1 and row[1] else ""
            url = str(row[2]).strip() if len(row) > 2 and row[2] else ""
            if topic:
                entry = f"{topic}: {note}"
                if url:
                    entry += f" ({url})"
                lines.append(entry)
        if len(lines) > 1:
            docs.append(Document(
                page_content="\n".join(lines),
                metadata={
                    "source": file_path,
                    "form_number": "StateReq-Notes",
                    "edition_date": "",
                    "description": "Notes & Sources",
                    "filename": filename,
                    "parsed": True,
                },
            ))

    wb.close()
    return docs


def load_and_split(file_path: str) -> list:
    """Load a document and split it into chunks with parsed filename metadata.

    Supports .pdf, .txt, .docx, and .xlsx files.
    """

    # Parse metadata from the filename
    file_metadata = parse_filename(file_path)

    print("Parsed metadata:")
    for key, value in file_metadata.items():
        print(f"  {key}: {value}")

    # Pick the right loader based on file extension
    ext = file_path.rsplit(".", 1)[-1].lower() if "." in file_path else ""
    if ext == "pdf":
        loader = PyPDFLoader(file_path)
        pages = loader.load()
    elif ext == "txt":
        loader = TextLoader(file_path, encoding="utf-8")
        pages = loader.load()
    elif ext == "docx":
        pages = _load_docx(file_path)
    elif ext == "xlsx":
        # Excel chunks are pre-sized by the loader (one per state + category),
        # so we skip the text splitter and return directly.
        chunks = _load_xlsx(file_path)
        print(f"\nLoaded {len(chunks)} chunk(s) from {file_path}")
        print(f"Created {len(chunks)} chunks")
        return chunks
    else:
        raise ValueError(f"Unsupported file type: .{ext} — supported: .pdf, .txt, .docx, .xlsx")

    print(f"\nLoaded {len(pages)} page(s) from {file_path}")

    # Split pages into smaller chunks for better retrieval
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    chunks = splitter.split_documents(pages)

    # Attach our parsed metadata to every chunk
    for chunk in chunks:
        chunk.metadata.update(file_metadata)

    print(f"Created {len(chunks)} chunks")

    return chunks


if __name__ == "__main__":
    # Test with the insurance filing instructions PDF
    test_filename = "INS7059 (Rev. 02/2021) Instructions For Filing Annual & Quarterly Statements - MEWAs.pdf"
    print(f"Testing filename parsing on: {test_filename}\n")
    metadata = parse_filename(test_filename)
    for key, value in metadata.items():
        print(f"  {key}: {value}")

    # Also run the full pipeline on our existing document
    print("\n" + "=" * 60 + "\n")
    pdf_path = "data/raw/2020 - Residential Purchase Contract (CBR)  (28).pdf"
    chunks = load_and_split(pdf_path)

    # Preview the first chunk's metadata
    print(f"\nFirst chunk metadata: {chunks[0].metadata}")
