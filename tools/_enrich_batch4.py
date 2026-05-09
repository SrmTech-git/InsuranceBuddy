"""Batch 4 — cancellations, ID cards, financial responsibility (12 forms)."""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "raw" / "forms" / "general"


def card(form_num, edition, title, policy_term, transaction_types, body):
    header = f"ACORD {form_num} ({edition}) — {title}"
    rule = "=" * len(header)
    return (
        f"{header}\n{rule}\n"
        f"Form number: ACORD {form_num}\n"
        f"Edition: {edition}\n"
        f"Title: {title}\n"
        f"Type: Insurance form (ACORD industry standard)\n"
        f"States: All\n"
        f"Policy term: {policy_term}\n"
        f"Transaction types: {transaction_types}\n\n"
        f"{body}\n"
    )


CARDS = {
    "ACORD 35 (2017-05) Cancellation Request - Policy Release.txt": card(
        "35", "2017-05", "Cancellation Request / Policy Release",
        "N/A (existing policy)",
        "Cancellation (insured-initiated)",
        """Purpose:
Insured's request to cancel a policy mid-term. Documents the
cancellation date, reason, and the handling of any return premium.
Used by the insured (not the carrier) to initiate cancellation.

Captures:
- Producer / agency information
- Insured name, address, contact
- Policy number, type, effective dates
- Insurer name
- Cancellation effective date
- Reason for cancellation (replaced, sold, no longer needed, etc.)
- Return premium handling (refund to insured, retain with producer)
- Insured signature
- Producer signature / acknowledgment

When used:
- Insured-initiated mid-term cancellation
- Replacement of coverage with another carrier
- Cancellation of vehicle / property no longer owned
- Termination at insured's request

Notes:
- Distinct from ACORD 58 (Notice of Cancellation or Termination of
  Policy), which is the CARRIER's notice — ACORD 35 is the INSURED's
  request
- Most carriers require this signed by the insured to process the
  cancellation; some accept other written authorization""",
    ),

    "ACORD 36 (2007-01) Agent-Broker of Record Change.txt": card(
        "36", "2007-01", "Agent/Broker of Record Change",
        "N/A (existing policy)",
        "Agent of Record change (mid-term, no coverage change)",
        """Purpose:
Insured's authorization to change which agent or broker has
servicing rights on a policy. Establishes that all future
correspondence, commissions, and policy servicing should go to the
new agent/broker as of the change effective date.

Captures:
- Insured name, address
- Policy number(s) affected
- Insurer name
- Current (former) agent/broker information
- New agent/broker information
- Effective date of the change
- Insured signature with date

When used:
- Insured switching agents mid-term
- Acquisition of an account by a new producer
- Producer transitions or retirements
- Specialty market access (BOR change to access E&S markets)

Notes:
- Coverage doesn't change — only the agent of record does
- BOR changes typically take effect 5 business days after the carrier
  receives the signed letter; some carriers accept "BOR letters" as
  alternatives to ACORD 36 specifically
- Triggers commission redirection to the new producer""",
    ),

    "ACORD 37 (2008-01) Statement of No Loss.txt": card(
        "37", "2008-01", "Statement of No Loss",
        "N/A (statement document)",
        "Reinstatement, new business after lapse, backdating",
        """Purpose:
Insured's signed statement that no losses have occurred during a
coverage gap or specified period. Used to bind, reinstate, or
backdate coverage after a lapse without the carrier inheriting an
unreported claim.

Captures:
- Insured name, address
- Policy number / coverage being bound or reinstated
- Lapse period or "no loss" date range covered by the statement
- Description of property / vehicles / operations covered
- Insured's affirmation (under penalty of misrepresentation) that
  no losses occurred during the specified period
- Insured signature with date
- Witness signature (where required)

When used:
- Reinstating a policy after a non-payment cancellation
- Binding new coverage after a coverage gap
- Backdating coverage to an effective date prior to the binding date
- Mid-term replacement of coverage where prior coverage lapsed

Notes:
- A material misrepresentation on this form (signing despite a known
  loss) generally voids coverage and may constitute fraud
- Carriers vary in how far back they'll accept a statement of no
  loss — some won't honor any lapse beyond a few days; specialty
  markets may accept longer gaps""",
    ),

    "ACORD 38 (2013-01) Notice of Insurance Information Practices (Privacy).txt": card(
        "38", "2013-01", "Notice of Insurance Information Practices (Privacy)",
        "N/A (disclosure document)",
        "New business / renewal disclosure",
        """Purpose:
Privacy disclosure delivered to applicants and insureds describing
how the insurer collects, uses, and shares personal information.
Required under state insurance information and privacy protection
acts (modeled on the NAIC Insurance Information and Privacy
Protection Model Act).

Captures:
- Insurer / producer information
- Insured / applicant name
- Description of:
  * What personal information is collected
  * Sources of the information (the applicant, third parties, MIB,
    motor vehicle reports, consumer reports)
  * How the information is used (underwriting, claim handling,
    marketing)
  * To whom it may be disclosed without authorization
  * The applicant's rights to access and correct their information
- Acknowledgment of receipt (insured signature, optional)

When used:
- New business applications
- Renewal in states that require ongoing notice
- When the insurer obtains consumer reports or investigative reports
- Triggered by FCRA-related disclosures and state privacy law
  requirements

Notes:
- Required by many states under their adoption of the NAIC privacy
  model act; California, New York, and others have enhanced versions
- Delivery requirements vary by state (with the application,
  separately, by mail)
- Distinct from the federal Gramm-Leach-Bliley privacy notice that
  carriers also provide separately""",
    ),

    "ACORD 42 (2014-08) Residential Property Replacement Cost.txt": card(
        "42", "2014-08", "Residential Property Replacement Cost",
        "N/A (underwriting worksheet)",
        "New business / renewal underwriting",
        """Purpose:
Worksheet for calculating the replacement cost of a residential
dwelling, supporting the Coverage A limit on a homeowners policy.
Captures property characteristics — square footage, construction,
materials, features — that drive a per-square-foot replacement cost
calculation.

Captures:
- Insured / property location
- Year built, year of significant updates
- Square footage (above grade, basement)
- Construction type (frame, masonry veneer, masonry)
- Number of stories / units
- Foundation type (basement, crawl, slab)
- Roof type and material
- Heating, plumbing, electrical features
- Interior features (kitchen quality, bath count, fireplace,
  hardwood, etc.)
- Garage type (attached / detached, number of bays)
- Special features (deck, porch, pool, outbuildings)
- Calculated replacement cost (often via 360Value, MSB, or carrier
  worksheet)

When used:
- New homeowner business underwriting
- Renewal review of Coverage A adequacy
- Coverage adjustments after major renovations
- Insurance-to-value (ITV) audits

Notes:
- Most carriers use proprietary tools (360Value, MSB) rather than
  ACORD 42 directly, but the data captured is the same
- Coverage A inadequacy is a leading cause of underinsurance disputes
  after a total loss; ACORD 42 documents the basis for the limit
  selected
- Pairs with ACORD 80 (Homeowner Application) where Coverage A is
  set""",
    ),

    "ACORD 45 (2016-03) Additional Interest Schedule.txt": card(
        "45", "2016-03", "Additional Interest Schedule",
        "N/A (attaches to policy)",
        "New business, mid-term endorsement",
        """Purpose:
Schedule listing all additional interests on a policy — additional
insureds, mortgagees, loss payees, lienholders, lessors, certificate
holders. Used as an attachment when there are more additional
interests than the main application form provides space for, or to
track them as a single reference document.

Captures:
- Insured / policy information
- For each additional interest:
  * Name and full address
  * Type (mortgagee, additional insured, loss payee, lienholder,
    certificate holder, lessor)
  * Reference (loan number, lease ID, contract reference)
  * Position (1st mortgagee, 2nd mortgagee, etc.)
  * Specific property / vehicle / equipment the interest applies to
  * Effective date
  * Whether the additional interest receives notice of cancellation

When used:
- New business with multiple additional interests
- Mid-term endorsement adding or changing additional interests
- Renewal review of additional interests
- Commercial accounts with many lenders / mortgagees / certificate
  holders

Notes:
- Additional interest treatment differs by type — a "mortgagee" gets
  specific contractual protections (mortgage clause, notice of
  cancellation) that an "additional insured" doesn't, and vice versa
- Often referenced by ACORD 27/28/29 (evidence forms), which list
  the specific mortgagee being evidenced""",
    ),

    "ACORD 50 (2007-02) Automobile Insurance ID Card.txt": card(
        "50", "2007-02", "Automobile Insurance ID Card",
        "6 or 12 months (matches underlying auto policy)",
        "Issued at policy inception, renewal, and mid-term changes affecting vehicles or dates",
        """Purpose:
Proof-of-insurance card for an insured vehicle. Required by every
state to be carried in the vehicle (or accessible electronically);
presented to law enforcement, at registration renewal, and after
accidents to demonstrate financial responsibility.

Captures:
- Insurer name, NAIC code
- Producer / agency information
- Insured name, address
- Vehicle identification: year, make, model, VIN
- Policy number
- Policy effective and expiration dates
- Where applicable: limits or coverage indicator (some states
  require limits shown)

When used:
- Issued automatically at policy inception and at each renewal
- Reissued mid-term for vehicle additions or replacements
- Reissued on policy changes affecting effective dates
- Delivered to insured to carry in vehicle (paper or electronic)

Notes:
- Every state has its own requirements for what must appear on an
  auto ID card; ACORD 50 is the industry baseline but state-specific
  variants exist
- Many states now accept electronic ID cards in addition to paper
- Distinct from ACORD 50 WM and 50 WM Set (watermark stock variants
  for fraud prevention)""",
    ),

    "ACORD 50WM (2024-08) Automobile Insurance ID Card (with Watermark).txt": card(
        "50WM", "2024-08", "Automobile Insurance ID Card (with Watermark)",
        "6 or 12 months (matches underlying auto policy)",
        "Issued at policy inception, renewal, and mid-term changes affecting vehicles or dates",
        """Purpose:
Watermark version of the standard ACORD 50 auto insurance ID card.
Printed on watermarked paper stock to deter fraudulent duplication.
Required by certain states or carriers in lieu of (or in addition
to) plain ACORD 50.

Captures:
- Same data as ACORD 50:
  * Insurer name, NAIC code
  * Producer / agency information
  * Insured name, address
  * Vehicle identification (year, make, model, VIN)
  * Policy number
  * Effective and expiration dates
- Printed on watermarked paper stock (see ACORD 350/360 for the
  underlying paper)

When used:
- Issued in states or by carriers requiring watermark stock
- Same trigger points as ACORD 50: policy inception, renewal,
  mid-term vehicle changes

Notes:
- Watermarked stock is a fraud-prevention measure; some carriers no
  longer use it given electronic verification systems are now
  broadly adopted
- Pairs with ACORD 50 WM Set when carbon-copy / multi-part formats
  are needed""",
    ),

    "ACORD 50WMSET (2024-09) Automobile Insurance ID Card (with Watermark).txt": card(
        "50WMSET", "2024-09", "Automobile Insurance ID Card (with Watermark)",
        "6 or 12 months (matches underlying auto policy)",
        "Issued at policy inception, renewal, and mid-term changes affecting vehicles or dates",
        """Purpose:
Multi-part / set version of the watermark auto ID card. Designed to
produce multiple copies in one printing pass — one for the insured,
one for the agency file, etc. Functionally identical to ACORD 50 WM
but in a different physical format.

Captures:
- Same data as ACORD 50 WM (insurer, producer, insured, vehicle,
  policy)
- Multi-part stock with carbon or NCR (no carbon required)
  duplication

When used:
- Producer offices issuing physical ID cards that need multiple
  copies
- Agencies retaining a copy for the file
- Same trigger points as ACORD 50 / 50 WM

Notes:
- Increasingly rare as electronic ID card delivery has become
  standard
- The "set" variant exists for legacy paper-workflow agencies""",
    ),

    "ACORD 54 (1997-01) Financial Responsibility Form.txt": card(
        "54", "1997-01", "Financial Responsibility Form",
        "Matches underlying auto policy",
        "New filing, maintenance, or update of state DMV financial responsibility filing",
        """Purpose:
Filing with a state Department of Motor Vehicles certifying that an
insured carries the minimum auto insurance limits required for
financial responsibility. Used for SR-22-style filings:
court-ordered, post-suspension reinstatement, or high-risk driver
requirements.

Captures:
- Insurer name, NAIC code
- Insured / driver name, address, date of birth
- Driver's license number and state
- Vehicle information (where applicable)
- Policy number, effective dates
- Coverage limits being certified
- State DMV / DOT reference (case number, suspension reference)
- Insurer attestation that coverage is in force at the certified
  limits

When used:
- Filing required after a license suspension (DUI, uninsured
  accident, etc.)
- Court-ordered financial responsibility filings
- Reinstatement of driving privileges
- High-risk / non-standard auto policies

Notes:
- Many states use their own SR-22 form rather than ACORD 54; check
  state DMV requirements
- Filing is typically required for 3 years from the triggering event
- Pairs with ACORD 57 (Financial Responsibility Form – Cancellation)
  when coverage ends and the filing must be released""",
    ),

    "ACORD 57 (1997-01) Financial Responsibility Form – Cancellation.txt": card(
        "57", "1997-01", "Financial Responsibility Form – Cancellation",
        "N/A (existing policy)",
        "Cancellation of state DMV financial responsibility filing",
        """Purpose:
Cancellation notice filed with a state DMV ending an active
financial responsibility (SR-22 / ACORD 54) filing. Used when the
underlying policy cancels, lapses, or no longer covers the affected
driver.

Captures:
- Insurer name, NAIC code
- Insured / driver name, address, license number
- Original ACORD 54 filing reference
- Underlying policy number
- Cancellation effective date
- Reason for cancellation (policy cancelled, driver removed, filing
  no longer required)
- State DMV reference

When used:
- Underlying policy cancels for non-payment, replacement, or insured
  request
- Insured no longer required to maintain financial responsibility
  filing
- Driver removed from a policy that maintained the filing

Notes:
- Filing this form may trigger automatic license suspension if the
  insured's filing requirement is still active and no replacement
  filing is in place
- Counterpart to ACORD 54 — same data, opposite direction""",
    ),

    "ACORD 58 (2007-11) Notice of Cancellation or Termination of Policy.txt": card(
        "58", "2007-11", "Notice of Cancellation or Termination of Policy",
        "N/A (existing policy)",
        "Cancellation, non-renewal, termination",
        """Purpose:
Carrier-issued notice of cancellation, non-renewal, or termination,
sent to the insured AND to interested parties (mortgagees,
additional insureds, certificate holders, loss payees) who are
entitled to advance notice under the policy or contract.

Captures:
- Insurer name, NAIC code
- Producer / agency information
- Insured name, policy number, policy type
- Cancellation / non-renewal effective date
- Reason for cancellation (non-payment, underwriting, insured
  request, etc.)
- Recipient name and address (insured, mortgagee, additional
  insured, certificate holder)
- Statutory or contractual notice period referenced
- Reinstatement procedure (where applicable)

When used:
- Carrier-initiated cancellation for non-payment of premium
- Cancellation for material misrepresentation or substantial change
  in risk
- Non-renewal at expiration
- Termination at insured's written request (carrier confirmation)
- Required notice to mortgagees and additional insureds with notice
  rights

Notes:
- Distinct from ACORD 35 (Cancellation Request / Policy Release),
  which is the INSURED's request — ACORD 58 is the CARRIER's notice
- Statutory notice periods vary by state and reason (e.g., 10 days
  for non-payment vs. 30-60 days for underwriting cancellations)
- Mortgagees and certain additional insureds have separate, often
  longer notice rights""",
    ),
}


def main():
    written = 0
    for filename, content in CARDS.items():
        path = OUT / filename
        if not path.exists():
            print(f"  WARN: {filename} does not exist, skipping")
            continue
        path.write_text(content, encoding="utf-8")
        print(f"  wrote {filename}")
        written += 1
    print(f"\nWrote {written} card(s)")


if __name__ == "__main__":
    main()
