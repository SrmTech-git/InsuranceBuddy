# scrape_orc.py — download authenticated PDFs from Ohio code chapter pages
# Supports both Ohio Revised Code (ORC) and Ohio Administrative Code (OAC)

import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from config import SCRAPE_DELAY_SECONDS

BASE_URL = "https://codes.ohio.gov"
DEFAULT_CHAPTER_URL = f"{BASE_URL}/ohio-revised-code/chapter-3937"
# Ohio statutes only — OUTPUT_DIR matches the multi-state folder layout.
OUTPUT_DIR = Path("data/raw/regulatory/ohio")

HEADERS = {"User-Agent": "insurance-rag-research/1.0"}


def detect_code_type(url: str) -> str:
    """Determine whether the URL points to revised code or administrative code."""

    if "administrative-code" in url:
        return "OAC"
    return "ORC"


def fetch_chapter_page(chapter_url: str) -> BeautifulSoup:
    """Fetch the chapter page and return parsed HTML."""

    print(f"Fetching chapter page: {chapter_url}")
    resp = requests.get(chapter_url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def find_pdf_sections(soup: BeautifulSoup, code_type: str) -> list[dict]:
    """Find all 'Download Authenticated PDF' links and extract metadata.

    Returns a list of dicts with keys: section, title, pdf_url
    """

    sections = []

    pdf_links = soup.find_all("a", string=re.compile(r"Download Authenticated PDF", re.I))

    for link in pdf_links:
        href = link.get("href", "")
        if not href:
            continue

        pdf_url = href if href.startswith("http") else BASE_URL + href

        # Extract section number from the URL path
        if code_type == "OAC":
            # Admin code: /3901-1-01_20250213.pdf → 3901-1-01
            section_match = re.search(r"/(\d+-\d+-\d+)_", href)
        else:
            # Revised code: /3937.18/ → 3937.18
            section_match = re.search(r"/(\d+\.\d+)/", href)

        section = section_match.group(1) if section_match else ""

        # Walk up to the .list-content container to find the title
        # Header format: "Section 3937.18 | Title" or "Rule 3901-1-01 | Title"
        title = ""
        container = link.find_parent("div", class_="list-content")
        if container:
            head_link = container.select_one(".content-head-text a")
            if head_link:
                full_text = head_link.get_text(separator=" ").strip()
                title_match = re.search(r"\|\s*(.+)", full_text)
                if title_match:
                    title = title_match.group(1).strip().rstrip(".")

        if not section:
            print(f"  Skipping link (could not parse section number): {href}")
            continue

        sections.append({
            "section": section,
            "title": title,
            "pdf_url": pdf_url,
        })

    return sections


def sanitize_filename(name: str) -> str:
    """Remove characters that are invalid in Windows/Mac/Linux filenames."""

    return re.sub(r'[<>:"/\\|?*]', "", name).strip()


def download_pdfs(sections: list[dict], code_type: str) -> None:
    """Download each PDF to data/raw/ with a formatted filename.

    ORC files: ORC3937.18 Uninsured and underinsured motorist coverage.pdf
    OAC files: OAC3901-1-01 Public notice by publication.pdf
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total = len(sections)
    success = 0
    skipped = 0
    failed = 0

    for i, sec in enumerate(sections, 1):
        section = sec["section"]
        title = sec["title"]
        pdf_url = sec["pdf_url"]

        title_part = f" {title}" if title else ""
        filename = sanitize_filename(f"{code_type}{section}{title_part}.pdf")
        filepath = OUTPUT_DIR / filename

        print(f"[{i}/{total}] {section} — {title or '(no title)'}")

        if filepath.exists():
            print(f"         Skipped (already downloaded): {filename}")
            skipped += 1
            continue

        try:
            resp = requests.get(pdf_url, headers=HEADERS, timeout=30)
            resp.raise_for_status()

            filepath.write_bytes(resp.content)
            print(f"         Saved: {filepath} ({len(resp.content):,} bytes)")
            success += 1

        except requests.RequestException as e:
            print(f"         FAILED: {e}")
            failed += 1

        if i < total:
            time.sleep(SCRAPE_DELAY_SECONDS)

    print()
    print("=" * 60)
    print(f"Done! {success} downloaded, {skipped} skipped, {failed} failed, {total} total.")
    print("=" * 60)


if __name__ == "__main__":
    chapter_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CHAPTER_URL
    code_type = detect_code_type(chapter_url)

    print(f"Code type detected: {code_type}")
    soup = fetch_chapter_page(chapter_url)
    sections = find_pdf_sections(soup, code_type)

    if not sections:
        print("No PDF links found on the page.")
    else:
        print(f"\nFound {len(sections)} PDF links.\n")
        download_pdfs(sections, code_type)
