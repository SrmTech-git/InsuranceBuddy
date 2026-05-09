"""Batch 5 — flood, fraud, terrorism, electronic delivery (7 forms)."""
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
    "ACORD 60 (2010-04) Flood Insurance Selection - Rejection.txt": card(
        "60", "2010-04", "Flood Insurance Selection / Rejection",
        "N/A (acknowledgment document)",
        "New business / renewal acknowledgment",
        """Purpose:
Insured's signed selection or rejection of flood insurance coverage.
Documents that the insured was offered flood coverage (NFIP or
private market) and either accepted at a specific limit or declined.
Used to establish the agent's E&O record on flood offering.

Captures:
- Insured name, address
- Property location
- Producer / agency information
- Whether the property is in a Special Flood Hazard Area (SFHA)
- Federal flood zone designation (where known)
- Coverage offered: NFIP, private market, or both
- Selection: limits selected (building, contents) OR rejection
- Insured signature with date
- Producer signature

When used:
- New homeowner / commercial property business in any flood zone
- Renewal review where flood election needs re-confirmation
- Documentation when a known flood zone risk is declined

Notes:
- Distinct from ACORD 29 (Evidence of Flood Insurance), which proves
  flood coverage to a mortgagee — ACORD 60 documents the OFFER and
  the insured's CHOICE
- E&O exposure on flood is significant; this form is the standard
  defense when an agent is later accused of failing to recommend
  flood coverage
- Even properties outside SFHAs flood — the form is recommended for
  every property, not just high-risk zones""",
    ),

    "ACORD 60US (2015-01) Insurance Supplement – Notice – Offer of Terrorism Coverage.txt": card(
        "60US", "2015-01", "Insurance Supplement – Notice – Offer of Terrorism Coverage",
        "N/A (disclosure / acknowledgment)",
        "New business / renewal disclosure (TRIA-required)",
        """Purpose:
Federally mandated notice of terrorism risk insurance offering under
the Terrorism Risk Insurance Act (TRIA). Insurers must offer
terrorism coverage on commercial property and casualty policies and
disclose the federal government's share of insured losses.
Documents that the offer was made and the insured's acceptance or
rejection.

Captures:
- Insured name, address
- Producer / agency information
- Insurer / policy reference
- TRIA-required disclosures:
  * Federal share of insured losses
  * Insurer deductible and copay levels under TRIA
  * Premium charge for terrorism coverage (or that the offer is at
    no additional premium, where applicable)
- Selection: accept or reject terrorism coverage
- Insured signature acknowledging the disclosure
- Effective dates

When used:
- New commercial property and casualty business
- Renewal of TRIA-eligible policies
- Mid-term changes affecting terrorism election

Notes:
- TRIA covers commercial lines only — not personal lines, workers
  comp (which has separate handling), or surety
- Pairs with ACORD 62 US (Standard Fire Policy variant) and ACORD
  64 US (Workers Compensation variant)
- Disclosure is REQUIRED even if terrorism coverage is provided at
  no additional premium — the insured must be informed of the
  federal backstop""",
    ),

    "ACORD 62US (2015-01) Insurance Supplement – Standard Fire Policy Only Notice – Offer of Terrorism Coverage.txt": card(
        "62US", "2015-01", "Insurance Supplement – Standard Fire Policy Only Notice – Offer of Terrorism Coverage",
        "N/A (disclosure / acknowledgment)",
        "New business / renewal disclosure (TRIA-required, fire-policy variant)",
        """Purpose:
TRIA terrorism offering disclosure tailored to states that mandate
the Standard Fire Policy. Some states require terrorism coverage to
be embedded in property policies issued under the SFP framework
rather than offered separately. This form documents the offering and
acknowledgment in those jurisdictions.

Captures:
- Insured name, address
- Producer / agency information
- Insurer / policy reference
- TRIA disclosures (federal share, insurer deductible/copay)
- Standard Fire Policy context — that the SFP framework requires
  certain perils including fire be covered without exclusion
- Selection: accept or reject terrorism coverage where election is
  available; acknowledgment where embedded
- Insured signature
- Effective dates

When used:
- Property policies issued in Standard Fire Policy states
- Where state law conflicts with TRIA's optional offering structure

Notes:
- Variant of ACORD 60 US for SFP states; same TRIA disclosures with
  additional SFP-specific language
- Standard Fire Policy states historically include New York, New
  Jersey, North Carolina, and others — though specific requirements
  have evolved
- Pairs with ACORD 60 US (general TRIA) and ACORD 64 US (workers comp)""",
    ),

    "ACORD 63 (2024-02) Fraud Statements.txt": card(
        "63", "2024-02", "Fraud Statements",
        "N/A (statutory disclosure)",
        "New business / claim filing disclosure",
        """Purpose:
Compendium of state-mandated fraud warning statements that must
appear on insurance applications, claim forms, or both. Each state
has its own required language warning the applicant or claimant that
materially false statements constitute insurance fraud and may carry
criminal penalties.

Captures:
- State-by-state fraud warning statements (varies by jurisdiction)
- Distinct warnings for application context vs. claim context
- Specific statutory references for each state's fraud language
- Effective dates and updates as state laws change

When used:
- Attached to applications and claim forms
- Updated when state insurance laws change fraud warning
  requirements
- Referenced by carriers for compliance with each state's
  application and claim disclosure requirements

Notes:
- This form is a reference document — the actual warnings are
  included on the relevant ACORD applications and claim forms; this
  form aggregates the source language
- States periodically revise fraud language; producers should use
  the most current ACORD 63 to confirm warnings on outgoing forms
  reflect current state law
- Some states have very specific language requirements (font size,
  exact wording) — close attention to state-specific requirements
  is critical""",
    ),

    "ACORD 64US (2015-01) Insurance Supplement – Workers' Compensation Only Notice – Offer of Terrorism Coverage.txt": card(
        "64US", "2015-01", "Insurance Supplement – Workers' Compensation Only Notice – Offer of Terrorism Coverage",
        "N/A (disclosure / acknowledgment)",
        "New business / renewal disclosure (TRIA-required, WC variant)",
        """Purpose:
TRIA terrorism offering disclosure tailored specifically to workers
compensation policies. Workers comp has unique TRIA treatment
because terrorism coverage cannot be excluded from a WC policy —
employees injured in a terrorist event are still entitled to WC
benefits. This form documents the disclosure and any premium charge
for the federal backstop.

Captures:
- Insured / employer name, address
- Producer / agency information
- Insurer / policy reference
- TRIA disclosures specific to workers compensation:
  * Federal share and insurer share for WC terrorism losses
  * Premium charge for terrorism (if any)
- Acknowledgment that terrorism coverage is included as required by
  state WC law (cannot be rejected on a WC policy)
- Insured signature
- Effective dates

When used:
- New workers compensation business
- Renewal of WC policies
- Required for every WC policy regardless of whether the employer
  perceives terrorism risk

Notes:
- Unlike commercial property/GL where terrorism can be rejected,
  workers comp terrorism coverage is mandatory — the form documents
  disclosure rather than offering a choice
- Pairs with ACORD 60 US (commercial P&C) and ACORD 62 US (Standard
  Fire Policy variant)
- TRIA assessments and recoupment provisions for WC differ from
  other lines; the disclosure reflects this""",
    ),

    "ACORD 66 (2011-05) Personal Insurance Supplement – Extraordinary Life Circumstances.txt": card(
        "66", "2011-05", "Personal Insurance Supplement – Extraordinary Life Circumstances",
        "N/A (underwriting supplement)",
        "New business / renewal underwriting (rate impact mitigation)",
        """Purpose:
Supplemental form documenting "extraordinary life circumstances"
that may have negatively affected an applicant's credit-based
insurance score, allowing the underwriter to mitigate or set aside
the credit impact when rating personal lines insurance. Required by
laws in many states regulating insurance scoring.

Captures:
- Insured / applicant name, contact
- Identification of the extraordinary life circumstance:
  * Catastrophic illness or injury (self or family)
  * Death of a spouse, child, or parent
  * Divorce or involuntary loss of employment
  * Identity theft
  * Military deployment
  * Other circumstances allowed under state law
- Time period during which the circumstance occurred
- Supporting documentation reference (death certificates, medical
  records, court orders, etc.)
- Producer attestation
- Insured signature

When used:
- Personal auto / homeowner new business or renewal where the
  applicant believes their credit-based insurance score reflects an
  extraordinary circumstance
- Adverse action notice follow-up after credit-based rating
- Mid-term re-rating requests

Notes:
- State laws vary significantly on which circumstances qualify and
  the documentation required
- Carriers must respond within statutorily defined timeframes
  (typically 30 days)
- Pairs with adverse action notices required by FCRA and state
  insurance scoring laws""",
    ),

    "ACORD 68 (2019-06) Electronic Delivery Supplement – Electronic Selection, Rejection Form.txt": card(
        "68", "2019-06", "Electronic Delivery Supplement – Electronic Selection, Rejection Form",
        "N/A (consent / preference document)",
        "New business / renewal consent (electronic delivery election)",
        """Purpose:
Insured's election or rejection of electronic delivery for policy
documents, notices, and other insurance communications. Required
under the federal E-SIGN Act and various state laws for the insurer
to deliver documents electronically (rather than by mail) with the
same legal effect.

Captures:
- Insured name, address
- Producer / agency information
- Email address(es) for electronic delivery
- Selection of which document categories to receive electronically:
  * Policy documents and endorsements
  * Renewal notices
  * Cancellation and non-renewal notices
  * Billing and payment notices
  * Privacy notices
  * Marketing communications
- Acknowledgment of the right to receive paper copies on request
- Hardware/software requirements acknowledgment (E-SIGN Act
  requirement)
- Insured signature with date
- Effective date

When used:
- New business when the insured wants electronic delivery
- Renewal where electronic delivery preferences are being updated
- Mid-term changes to delivery preference

Notes:
- E-SIGN Act requires affirmative consent and disclosure of hardware
  / software requirements before electronic delivery is legally
  effective
- Some state cancellation / non-renewal notices have special
  electronic delivery rules — they may still need to be delivered
  on paper even if other notices are electronic
- Insured can revoke electronic consent at any time""",
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
