# Insurance Industry Standard Abbreviations
# Source: Grange Enterprise Acronyms V2, filtered to industry-standard terms only
# Company-specific systems, designations, and internal programs removed
# Expand this dictionary as needed

import re

INSURANCE_ABBREVIATIONS = {
    # Coverage Types
    "UM": "uninsured motorist coverage",
    "UIM": "underinsured motorist coverage",
    "UMPD": "uninsured motorist property damage coverage",
    "BI": "bodily injury coverage",
    "PD": "property damage coverage",
    "PIP": "personal injury protection coverage",
    "MP": "medical payments coverage",
    "MED PAY": "medical payments coverage",
    "COLL": "collision coverage",
    "OTC": "other than collision coverage",
    "AMD": "auto material damage coverage",
    "CGL": "commercial general liability",
    "GL": "general liability",
    "GLA": "general liability",
    "SCP": "crime coverage",
    "CUP": "commercial umbrella policy",
    "FUP": "farmowners umbrella policy",
    "EPLI": "employment practices liability insurance",
    "DI": "disability insurance",
    "DIC": "difference in conditions",
    "WC": "workers compensation",
    "WCP": "workers compensation",
    "E&O": "errors and omissions",
    "D&O": "directors and officers",
    "BOP": "businessowners policy",
    "CPP": "commercial package policy",
    "PUL": "personal umbrella liability",
    "GKLL": "garagekeepers legal liability",
    "SIR": "self insured retention",

    # Policy Types / Programs
    "PPA": "private passenger auto",
    "PA": "personal auto",
    "CA": "commercial auto",
    "BA": "business auto",
    "HO": "homeowner",
    "PL": "personal lines",
    "CL": "commercial lines",
    "AR": "assigned risk",
    "NSA": "non standard auto",
    "IM": "inland marine",
    "DF": "dwelling fire",
    "FO": "farmowners",
    "MC": "motorcycle",
    "MH": "mobilehome",
    "CT": "contractors and tradesmen",
    "C&T": "contractors and tradesmen",
    "DEC": "declarations",
    "LOB": "line of business",

    # Industry Organizations
    "DOI": "department of insurance",
    "ODI": "Ohio department of insurance",
    "NAIC": "National Association of Insurance Commissioners",
    "ISO": "Insurance Services Office",
    "NCCI": "National Council on Compensation Insurance",
    "FEMA": "Federal Emergency Management Agency",
    "NHTSA": "National Highway Traffic Safety Administration",
    # Note: "ACORD" is intentionally NOT expanded — it appears in form
    # names ("ACORD 25") that need to flow through to retrieval as-is.
    # Expanding it would mangle form-number queries.

    # Common Insurance Terms
    "ACV": "actual cash value",
    "RC": "replacement cost",
    "ITV": "insurance to value",
    "LAE": "loss adjustment expense",
    "LR": "loss ratio",
    "ER": "expense ratio",
    "COR": "combined operating ratio",
    "IBNR": "incurred but not reported",
    "LKQ": "like kind and quality",
    "TPA": "third party administrator",
    "FNOL": "first notice of loss",
    "NCAN": "notice of cancellation",
    "COI": "certificate of insurance",
    "MVR": "motor vehicle record",
    "SR": "systems request",
    "ILF": "increased limit factor",
    "DWP": "direct written premium",
    "DEP": "direct earned premium",
    "NB": "new business",
    "PIF": "policies in force",
    "WP": "written premium",
    "EFT": "electronic funds transfer",
    "EQ": "earthquake",
    "CAT": "catastrophe",
    "SIU": "special investigations unit",
    "CLUE": "comprehensive loss underwriting exchange",
    "AOR": "agent of record",
    "BOR": "broker of record",
    "MGA": "managing general agent",
    "E&S": "excess and surplus",
    "P&C": "property and casualty",
    "SNL": "statement of no loss",
    "DOV": "diminution of value",
    "CBR": "credit bureau rating",
    "POP": "proof of insurance",
    "SVLO": "single vehicle liability only",
    "YTD": "year to date",
    "PYTD": "prior year to date",
}


def expand_abbreviations(query: str) -> str:
    """
    Expand insurance abbreviations in a query string to their full terms.
    Case insensitive matching, preserves original case of surrounding text.
    Returns the expanded query string.

    Iterates longest-first so multi-word abbreviations like "MED PAY" are
    matched before any shorter overlap could clobber them.
    """
    expanded = query

    for abbrev in sorted(INSURANCE_ABBREVIATIONS, key=len, reverse=True):
        full_term = INSURANCE_ABBREVIATIONS[abbrev]
        # Match whole words only, case insensitive
        pattern = r'\b' + re.escape(abbrev) + r'\b'
        expanded = re.sub(pattern, full_term, expanded, flags=re.IGNORECASE)

    return expanded


if __name__ == "__main__":
    # Quick test
    test_queries = [
        "Does Ohio require UM coverage?",
        "Does Ohio require UIM?",
        "What are the BI limits in Ohio?",
        "Is PIP required for PA policies?",
        "What does the DOI say about NCAN requirements?",
    ]

    print("Abbreviation expansion test:\n")
    for q in test_queries:
        expanded = expand_abbreviations(q)
        if expanded != q:
            print(f"  Original: {q}")
            print(f"  Expanded: {expanded}\n")
        else:
            print(f"  No change: {q}\n")
