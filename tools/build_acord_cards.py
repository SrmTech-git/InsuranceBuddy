"""build_acord_cards.py — generate library-card .txt files for the
COUNTRYWIDE P&C national ACORD forms index.

One card per form, dropped into data/raw/forms/general/. Cards contain
just the metadata signal we need to make forms retrievable: form number,
edition date, title, type, state applicability. Detail/purpose can be
enriched per-form later by editing the .txt.

Run from project root:
    python tools/build_acord_cards.py
"""
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "forms" / "general"

# (form_number_raw, edition_raw, title) — directly transcribed from the
# COUNTRYWIDE P&C FORMS index. Editions are normalized below: the source
# uses YYYY/MM for modern entries and M/YY for older ones (1990s).
FORMS: list[tuple[str, str, str]] = [
    # --- left column ---
    ("1",         "2019-07", "Property Loss Notice"),
    ("2",         "2019-07", "Automobile Loss Notice"),
    ("3",         "2019-09", "Liability Notice of Occurrence / Claim"),
    ("4",         "2019-09", "Workers Compensation – First Report of Injury or Illness"),
    ("5",         "2019-09", "Aircraft Loss Notice"),
    ("6",         "2009-05", "Aviation Witness / Passenger Schedule"),
    ("7",         "2009-05", "Aviation Injured Schedule"),
    ("11",        "1995-02", "Auto Accident Information Form"),
    ("12",        "1995-02", "Exchange of Information Form"),
    ("13",        "1995-02", "Witness Card"),
    ("20",        "2016-03", "Certificate of Aviation Liability Insurance"),
    ("21",        "2016-03", "Certificate of Aircraft Insurance"),
    ("22",        "2016-03", "Intermodal Interchange Certificate of Insurance"),
    ("23",        "2016-03", "Vehicle or Equipment Certificate of Insurance"),
    ("24",        "2016-03", "Certificate of Property Insurance"),
    ("25",        "2025-12", "Certificate of Liability Insurance"),
    ("26",        "2002-01", "Policy Certification Log"),
    ("27",        "2016-03", "Evidence of Property Insurance"),
    ("28",        "2016-03", "Evidence of Commercial Property Insurance"),
    ("29",        "2016-03", "Evidence of Flood Insurance"),
    ("30",        "2016-03", "Certificate of Garage Insurance"),
    ("31",        "2016-03", "Certificate of Marine / Energy Insurance"),
    ("35",        "2017-05", "Cancellation Request / Policy Release"),
    ("36",        "2007-01", "Agent/Broker of Record Change"),
    ("37",        "2008-01", "Statement of No Loss"),
    ("38",        "2013-01", "Notice of Insurance Information Practices (Privacy)"),
    ("42",        "2014-08", "Residential Property Replacement Cost"),
    ("45",        "2016-03", "Additional Interest Schedule"),
    ("50",        "2007-02", "Automobile Insurance ID Card"),
    ("50 WM",     "2024-08", "Automobile Insurance ID Card (with Watermark)"),
    ("50 WM set", "2024-09", "Automobile Insurance ID Card (with Watermark)"),
    ("54",        "1997-01", "Financial Responsibility Form"),
    ("57",        "1997-01", "Financial Responsibility Form – Cancellation"),
    ("58",        "2007-11", "Notice of Cancellation or Termination of Policy"),
    ("60",        "2010-04", "Flood Insurance Selection / Rejection"),
    ("60 US",     "2015-01", "Insurance Supplement – Notice – Offer of Terrorism Coverage"),
    ("62 US",     "2015-01", "Insurance Supplement – Standard Fire Policy Only Notice – Offer of Terrorism Coverage"),
    ("63",        "2024-02", "Fraud Statements"),
    ("64 US",     "2015-01", "Insurance Supplement – Workers' Compensation Only Notice – Offer of Terrorism Coverage"),
    # --- right column ---
    ("66",        "2011-05", "Personal Insurance Supplement – Extraordinary Life Circumstances"),
    ("68",        "2019-06", "Electronic Delivery Supplement – Electronic Selection, Rejection Form"),
    ("70",        "2015-09", "Personal Policy Change Request (Except Auto)"),
    ("71",        "2016-08", "Personal Auto Policy Change Request"),
    ("72",        "2009-10", "Mobile Home Supplement"),
    ("73",        "2009-07", "Solid Fuel Questionnaire – Supplement to Residential Section"),
    ("74",        "2009-09", "Residence Based Business Supplement to Residential Section"),
    ("75",        "2016-03", "Insurance Binder"),
    ("76",        "1993-09", "Binder Log"),
    ("80",        "2016-11", "Homeowner Application"),
    ("81",        "2016-03", "Personal Inland Marine Application"),
    ("82",        "2025-07", "Watercraft Application"),
    ("83",        "2025-07", "Personal Umbrella Application"),
    ("84",        "2016-11", "Dwelling Fire Application"),
    ("85",        "2016-11", "Mobile Home Application"),
    ("88",        "2015-12", "Personal Insurance Application – Applicant Information Section"),
    ("89",        "2016-11", "Residential Section"),
    ("91",        "2009-10", "Good Student Driver Training"),
    ("92",        "2012-03", "Medical Statement"),
    ("93",        "2016-08", "Young Driver Questionnaire"),
    ("99",        "2009-02", "Accidents / Convictions Schedule"),
    ("101",       "2008-01", "Additional Remarks Schedule"),
    ("103",       "2012-03", "Personal Auto Application Schedule – Additional Resident and Driver Information Section"),
    ("105",       "2012-06", "Apartment Building Supplement"),
    ("106",       "2010-04", "Vacant Building Supplement"),
    ("125",       "2025-03", "Commercial Insurance Application Applicant Information Section"),
    ("126",       "2025-03", "Commercial General Liability Section"),
    ("127",       "2015-12", "Business Auto Section"),
    ("128",       "2015-12", "Garage and Dealers Section"),
    ("129",       "2009-11", "Vehicle Schedule"),
    ("130",       "2026-01", "Workers Compensation Application"),
    ("131",       "2017-11", "Umbrella Section"),
    ("132",       "2015-12", "Truckers / Motor Carriers Section"),
    ("133",       "2025-05", "Workers Compensation Insurance Plan – Assigned Risk Section"),
    ("139",       "2015-12", "Statement / Schedule of Values"),
    ("140",       "2016-03", "Property Section"),
]


def normalize_form_number(num: str) -> str:
    """'1' -> '1', '50 WM' -> '50WM', '50 WM set' -> '50WMSET'.

    No zero-padding: keeps the form number as users actually type it.
    'ACORD 25' beats 'ACORD 0025' for retrieval — semantic search hits
    cleanly when the query string appears verbatim in the card.
    """
    parts = num.split()
    base = parts[0]
    suffix = "".join(p.upper() for p in parts[1:])
    return base + suffix


def sanitize_for_filename(title: str) -> str:
    """Make the title safe for filenames. We replace ' / ' with ' - ' so
    'Liability Notice of Occurrence / Claim' becomes 'Liability Notice of
    Occurrence - Claim'. Preserves em-dashes (–), apostrophes, parens —
    those are filesystem-legal."""
    return title.replace(" / ", " - ").replace("/", "-")


def build_card(form_num_padded: str, edition: str, title: str) -> str:
    header = f"ACORD {form_num_padded} ({edition}) — {title}"
    rule = "=" * len(header)
    return (
        f"{header}\n"
        f"{rule}\n"
        f"Form number: ACORD {form_num_padded}\n"
        f"Edition: {edition}\n"
        f"Title: {title}\n"
        f"Type: Insurance form (ACORD industry standard)\n"
        f"States: All\n"
    )


def build_filename(form_num_padded: str, edition: str, title: str) -> str:
    return f"ACORD {form_num_padded} ({edition}) {sanitize_for_filename(title)}.txt"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for raw_num, edition, title in FORMS:
        padded = normalize_form_number(raw_num)
        filename = build_filename(padded, edition, title)
        content = build_card(padded, edition, title)
        path = OUTPUT_DIR / filename
        path.write_text(content, encoding="utf-8")
        written += 1
    print(f"Wrote {written} card(s) to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
