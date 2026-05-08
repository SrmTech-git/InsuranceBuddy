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
    # --- continued page (forms 141+) ---
    ("141",       "2016-03", "Crime Section"),
    ("143",       "2013-09", "Transportation Section"),
    ("144",       "2013-09", "Glass and Sign Section"),
    ("145",       "2013-09", "Accounts Receivable / Valuable Papers"),
    ("147",       "2016-03", "Installation / Builders Risk Section"),
    ("148",       "2016-03", "Electronic Data Processing Section"),
    ("149",       "2013-09", "Dealers Section"),
    ("152",       "2015-06", "Commercial Inland Marine Section"),
    ("155",       "2016-09", "Equipment Breakdown Section"),
    ("159",       "2014-09", "Schedule of Property Limits"),
    ("160",       "2016-09", "Business Owners Section"),
    ("163",       "2012-06", "Commercial Auto Driver Information Schedule"),
    ("175",       "2016-03", "Commercial Policy Change Request"),
    ("180",       "2016-03", "Technology E&O Section – Electronic Data Processors, Electric Products Manufacturers, Computer Services etc."),
    ("185",       "2011-09", "Restaurant / Tavern Supplement"),
    ("186",       "2011-10", "Contractors Supplement"),
    ("187",       "2016-03", "Professional Liability Supplement"),
    ("190",       "2013-09", "Supplemental Property Application"),
    ("193",       "2009-03", "Open Cargo Section"),
    ("194",       "2009-03", "Truckers / Motor Carrier Supplement"),
    ("195",       "1996-10", "Design Professional's Individual Property Survey"),
    ("196",       "2013-09", "Medical Professional Liability Insurance Application"),
    ("199",       "1999-01", "Application Supplement – Undertaking"),
    ("200",       "1993-03", "Producer Account"),
    ("201",       "1993-03", "Producer Account Discrepancy Notice"),
    ("210",       "2016-03", "Yacht Section"),
    ("211",       "2016-09", "Schedule of Hazards"),
    ("212",       "2017-09", "Commercial Umbrella Underlying Schedule"),
    ("225",       "1998-01", "Policyholder's Report"),
    ("226",       "1993-03", "Statement of Premium Adjustment"),
    ("275",       "2016-03", "Aviation Insurance Binder"),
    ("276",       "2016-03", "Aircraft Insurance Binder"),
    ("281",       "2016-05", "Personal Inland Marine Section"),
    ("282",       "2025-07", "Watercraft Section"),
    ("283",       "2025-07", "Personal Umbrella Application Section"),
    ("285",       "2024-06", "Commercial Marine Insurance Supplement Hull & Machinery & Protection & Indemnity"),
    ("301",       "2022-12", "National Flood Insurance Program Flood Insurance Application"),
    ("302",       "2015-04", "NFIP – Flood Insurance General Change Endorsement"),
    ("303",       "2015-04", "NFIP – Flood Insurance Preferred Risk Policy Application"),
    ("304",       "2022-12", "NFIP – Flood Insurance Cancellation / Nullification"),
    ("305",       "2012-02", "NFIP – Credit Card Payment Form"),
    ("306",       "2011-04", "NFIP – Rating Information and Elevated Building Determination Form"),
    ("307",       "2016-02", "NFIP – Floodproofing Certificate for Non-Residential Structures"),
    ("308",       "2015-04", "NFIP – Residential Basement Floodproofing Certificate"),
    ("325",       "2013-09", "Aviation Insurance Application – Applicant Information Section"),
    ("326",       "2006-04", "Airport Property Supplement"),
    ("327",       "2016-03", "Airport and FBO Liability Section"),
    ("328",       "2024-06", "Private Hangar Liability Section"),
    ("329",       "2014-12", "Aviation Products Liability"),
    ("330",       "2016-03", "Aircraft Section"),
    ("331",       "2011-11", "Pilot Experience"),
    ("332",       "2006-04", "Hangar Schedule"),
    ("333",       "2009-05", "Aircraft Schedule"),
    ("335",       "2009-06", "Aviation Policy Change Request – Applicant Information Section"),
    ("336",       "2009-06", "Airport Property Change Request"),
    ("337",       "2016-03", "Airport and FBO Liability Change Request"),
    ("338",       "2009-06", "Private Hangar Liability Change Request"),
    ("339",       "2009-06", "Aviation Products Liability Change Request"),
    ("340",       "2016-03", "Aircraft Change Request"),
    ("341",       "2011-11", "Pilot Experience Change Request"),
    ("342",       "2009-06", "Hangar Change Request"),
    # Watermark paper stock — no edition date in the index
    ("350",       "",        "Watermark Paper – 20 # ID Card Stock (4-part perforation)"),
    ("360",       "",        "Watermark Paper – 32 # ID Card Stock (4-part perforation)"),
    ("370",       "",        "Watermark Paper – 32 # ID Card Stock (non-perforated)"),
    # Agriculture / farm
    ("401",       "2016-03", "Agriculture Application"),
    ("402",       "2016-03", "Agriculture Property Section"),
    ("403",       "2016-03", "Agriculture Property Section Scheduled / Unscheduled Personal Property"),
    ("404",       "2016-03", "Agriculture Liability Section"),
    ("405",       "2007-09", "Agriculture Premises Diagram"),
    ("406",       "2007-09", "Agriculture Supplement - Unscheduled Farm Personal Property Inventory Form"),
    ("407",       "2016-03", "Livestock Mortality Section"),
    ("408",       "2007-09", "Equine Liability Supplement"),
    ("410",       "2016-03", "Small Farm / Ranch Application"),
    # Surety / bonds
    ("501",       "2016-06", "Surety Report of Execution"),
    ("502",       "2018-08", "Contract Bond Request Form"),
    ("503",       "2016-06", "Commercial or Miscellaneous Bond Request Form"),
    ("504",       "2016-06", "Additional Entity Schedule"),
    # Premium / loss runs
    ("610",       "2015-12", "Premium Payment Supplement"),
    ("611",       "2015-07", "Claims History / Loss Run Request"),
    # Specialty commercial
    ("801",       "2002-01", "Railroad Protective Liability Supplement"),
    ("802",       "2011-09", "Hotel / Motel Supplement"),
    ("803",       "2016-03", "Liquor Liability Section"),
    ("807",       "2016-03", "Directors & Officers Liability Section"),
    ("808",       "2010-08", "P&C Agency Appointment Form"),
    ("810",       "2014-12", "Business Income / Extra Expense / Rental Value Supplement to Property Section"),
    ("811",       "2014-12", "Value Reporting Information Supplement to Property Section"),
    ("812",       "2006-02", "Agency Questionnaire"),
    ("813",       "2025-06", "Request for Proof of Property Insurance"),
    ("815",       "2009-02", "International Liability Exposure Supplement"),
    ("816",       "2005-06", "International Property Exposure Supplement"),
    # Producer info / commercial supplements
    ("821",       "2015-10", "Producer Information Form (PIF)"),
    ("822",       "2009-07", "Driver Work / School Address Information Supplement"),
    ("823",       "2015-12", "Additional Premises Information Schedule"),
    ("825",       "2016-05", "Professional / Specialty Insurance Application – For Use in Management, Executive & Professional Lines Applicant Section"),
    ("827",       "2016-03", "Employment Practices Liability Insurance Section"),
    ("828",       "2016-03", "Fiduciary Liability Coverage Section"),
    ("829",       "2009-05", "Forms and Endorsements Schedule"),
    ("830",       "2026-03", "Property Insurance Card"),
    ("831",       "2019-09", "Professional / Specialty Insurance Notice of Incident / Claim"),
    ("832",       "2016-03", "Miscellaneous E&O Section"),
    ("833",       "2014-12", "Lawyers Professional Liability Section"),
    ("834",       "2014-12", "Cyber and Privacy Coverage Section"),
    ("838",       "2013-12", "Accountants Professional Liability Section"),
    # Background check / consumer report
    ("876",       "2015-10", "Background Check Authorization"),
    ("877",       "2015-10", "Disclosure of Intent to Obtain Consumer Report or Investigative Consumer Report (except California)"),
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


def build_card(form_num: str, edition: str, title: str) -> str:
    header_edition = f" ({edition})" if edition else ""
    header = f"ACORD {form_num}{header_edition} — {title}"
    rule = "=" * len(header)
    edition_line = f"Edition: {edition}" if edition else "Edition: (not specified)"
    return (
        f"{header}\n"
        f"{rule}\n"
        f"Form number: ACORD {form_num}\n"
        f"{edition_line}\n"
        f"Title: {title}\n"
        f"Type: Insurance form (ACORD industry standard)\n"
        f"States: All\n"
    )


def build_filename(form_num: str, edition: str, title: str) -> str:
    safe_title = sanitize_for_filename(title)
    if edition:
        return f"ACORD {form_num} ({edition}) {safe_title}.txt"
    return f"ACORD {form_num} {safe_title}.txt"


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
