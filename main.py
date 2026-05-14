import argparse
import logging
import sys
from pathlib import Path

# Make src/ importable regardless of working directory
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Show INFO-level breadcrumbs from src/* without log-level prefixes.
# Library users who want different formatting can reconfigure.
logging.basicConfig(level=logging.INFO, format="%(message)s")


def cmd_chat(_args: argparse.Namespace) -> None:
    from chat import ask

    print("Insurance Document Assistant (type 'quit' to exit)\n")
    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() == "quit":
            print("Goodbye!")
            break

        print(f"\n{ask(question)}\n")


def cmd_ingest(args: argparse.Namespace) -> None:
    from ingest_batch import ingest_all

    ingest_all(force=args.force, collection_override=args.collection)


def cmd_migrate(args: argparse.Namespace) -> None:
    from migrate_state_tags import migrate
    migrate(args.collection, args.state, dry_run=args.dry_run)


def cmd_eval(args: argparse.Namespace) -> None:
    from eval.run_eval import run_eval
    run_eval(args)


def cmd_scrape(args: argparse.Namespace) -> None:
    from scrape_orc import detect_code_type, fetch_chapter_page, find_pdf_sections, download_pdfs

    code_type = detect_code_type(args.url)
    print(f"Code type detected: {code_type}")
    soup = fetch_chapter_page(args.url)
    sections = find_pdf_sections(soup, code_type)

    if not sections:
        print("No PDF links found on the page.")
    else:
        print(f"\nFound {len(sections)} PDF links.\n")
        download_pdfs(sections, code_type)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="insurance-rag",
        description="Insurance RAG — chat, ingest, and scrape Ohio insurance documents.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    subparsers.required = True

    # chat
    subparsers.add_parser("chat", help="Start the interactive Q&A assistant")

    # ingest — choices are sourced from chat.COLLECTION_REGISTRY so adding
    # a new collection there automatically extends this CLI.
    from router import COLLECTION_REGISTRY
    ingest_parser = subparsers.add_parser("ingest", help="Batch-embed documents from data/raw/")
    ingest_parser.add_argument(
        "--collection",
        choices=list(COLLECTION_REGISTRY.keys()),
        default=None,
        help="Only ingest this collection (default: all subfolders)",
    )
    ingest_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite documents that already exist in the database",
    )

    # migrate
    migrate_parser = subparsers.add_parser("migrate", help="Back-fill state tags on existing chunks")
    migrate_parser.add_argument("--collection", default="regulatory", help="Collection to migrate (default: regulatory)")
    migrate_parser.add_argument("--state", default="OH", help="State code to apply to untagged chunks (default: OH)")
    migrate_parser.add_argument("--dry-run", action="store_true", help="Preview without writing")

    # eval
    eval_parser = subparsers.add_parser("eval", help="Run the eval suite against test cases")
    eval_parser.add_argument(
        "--tags",
        default=None,
        help="Comma-separated tags to filter cases (e.g. 'regression,routing')",
    )
    eval_parser.add_argument(
        "--baseline",
        action="store_true",
        help="Also overwrite eval/baseline.md with this run's report",
    )

    # scrape
    scrape_parser = subparsers.add_parser("scrape", help="Download authenticated PDFs from codes.ohio.gov")
    scrape_parser.add_argument(
        "url",
        nargs="?",
        default="https://codes.ohio.gov/ohio-revised-code/chapter-3937",
        help="Chapter page URL (default: ORC chapter 3937)",
    )

    args = parser.parse_args()
    dispatch = {"chat": cmd_chat, "ingest": cmd_ingest, "migrate": cmd_migrate, "eval": cmd_eval, "scrape": cmd_scrape}
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
