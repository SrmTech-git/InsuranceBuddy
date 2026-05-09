"""One-off: enrich Batch 3 cards (ACORD 20-24, 26-31) with full descriptions.

Run from project root:
    python tools/_enrich_batch3.py

Idempotent — safe to re-run if content needs tweaking.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "raw" / "forms" / "general"


def card(form_num, edition, title, policy_term, transaction_types, body, *, type_label="Insurance form (ACORD industry standard)"):
    header = f"ACORD {form_num} ({edition}) — {title}"
    rule = "=" * len(header)
    return (
        f"{header}\n"
        f"{rule}\n"
        f"Form number: ACORD {form_num}\n"
        f"Edition: {edition}\n"
        f"Title: {title}\n"
        f"Type: {type_label}\n"
        f"States: All\n"
        f"Policy term: {policy_term}\n"
        f"Transaction types: {transaction_types}\n"
        f"\n"
        f"{body}\n"
    )


CERT = "Insurance certificate (ACORD industry standard)"


CARDS = {
    "ACORD 20 (2016-03) Certificate of Aviation Liability Insurance.txt": card(
        "20", "2016-03", "Certificate of Aviation Liability Insurance",
        "N/A (reflects underlying policies)",
        "N/A (issued on demand)",
        """Purpose:
Provides evidence of aviation liability insurance to a third party
(certificate holder). Used in lieu of ACORD 25 when the underlying
exposure is aviation-related — airport tenants, FBOs, charter
operators, aircraft owners — because aviation policies have
distinct coverage parts and limits structures (per-passenger limits,
products-completed operations for aviation, war risk indicators)
that the standard ACORD 25 doesn't capture.

Captures:
- Producer / agency information
- Named insured
- Insurer(s) affording coverage with NAIC numbers
- Certificate holder name and address
- Aviation policy number, effective and expiration dates
- Coverage parts:
  * Aircraft Liability (each occurrence, per passenger seat)
  * Hangarkeepers Liability (sublimit per aircraft, aggregate)
  * Premises / Products-Completed Operations
  * Personal Injury / Advertising Injury
  * Medical Payments
  * War Risk indicator (if covered)
- Description of operations / aircraft / locations
- Additional Insured / Loss Payee / Cancellation indicators

When used:
- Airport tenant lease compliance
- FBO operations and ground service agreements
- Aircraft charter and management contracts
- Aircraft lender / lessor requirements
- Government airport operations contracts

Notes:
- Aviation policies have substantially different coverage structure
  than general liability — uses dedicated certificate rather than
  ACORD 25 to avoid mislabeling limits
- Often paired with ACORD 21 (Certificate of Aircraft Insurance) when
  both hull and broader liability evidence is needed""",
        type_label=CERT,
    ),

    "ACORD 21 (2016-03) Certificate of Aircraft Insurance.txt": card(
        "21", "2016-03", "Certificate of Aircraft Insurance",
        "N/A (reflects underlying policies)",
        "N/A (issued on demand)",
        """Purpose:
Provides evidence of aircraft hull and liability insurance for a
specific aircraft. Used by aircraft lenders, lessors, and partners
to verify coverage on the financed or leased asset. More aircraft-
specific than ACORD 20 — focuses on the specific aircraft and its
hull AND liability coverage parts together.

Captures:
- Producer / agency information
- Insured / aircraft owner / operator
- Aircraft information: registration (N-number), make, model, year,
  serial number, type of operation
- Insurer(s) affording coverage
- Hull coverage:
  * Agreed value / hull limit
  * Deductible (in motion / not in motion)
- Liability coverage:
  * Each occurrence
  * Per passenger seat
  * Property damage / passenger property
- Certificate holder (lender, lessor, additional insured)
- Loss Payable Clause and Additional Insured indicators
- Effective and expiration dates

When used:
- Aircraft financing and lease compliance
- Aircraft management agreements
- Joint ownership / partnership documentation
- Charter operator agreements

Notes:
- Pairs with ACORD 20 (Certificate of Aviation Liability) when both
  hull and broader liability evidence is needed
- Aircraft lenders typically require Loss Payable in their favor
  and Breach of Warranty endorsement on the hull policy""",
        type_label=CERT,
    ),

    "ACORD 22 (2016-03) Intermodal Interchange Certificate of Insurance.txt": card(
        "22", "2016-03", "Intermodal Interchange Certificate of Insurance",
        "N/A (reflects underlying policies)",
        "N/A (issued on demand)",
        """Purpose:
Specialty certificate proving a motor carrier has the insurance
coverage required by an Intermodal Equipment Provider (IEP) under
the Uniform Intermodal Interchange Agreement (UIIA). Required when
a trucker picks up or drops off intermodal containers, chassis, or
trailers from steamship lines, terminal operators, or equipment
leasing companies.

Captures:
- Producer / agency information
- Motor carrier name, address, MC and DOT numbers
- Intermodal Equipment Provider (certificate holder)
- Auto liability coverage (typically $1M CSL minimum per UIIA)
- Trailer interchange / non-owned trailer coverage with limit
- Cargo / motor truck cargo coverage
- Physical damage on intermodal equipment
- General liability (where applicable)
- Workers compensation (where applicable)
- Effective and expiration dates

When used:
- Submitting carrier credentials to UIIA
- Periodic re-verification with IEPs
- Adding new IEPs to a carrier's authorized list

Notes:
- UIIA requirements set the minimum limits; individual IEPs may
  require higher limits or additional coverages
- Filed via UIIA's online system in addition to (or instead of)
  manual delivery to the IEP""",
        type_label=CERT,
    ),

    "ACORD 23 (2016-03) Vehicle or Equipment Certificate of Insurance.txt": card(
        "23", "2016-03", "Vehicle or Equipment Certificate of Insurance",
        "N/A (reflects underlying policies)",
        "N/A (issued on demand)",
        """Purpose:
Certificate proving liability and physical damage coverage on a
specific vehicle or piece of equipment. More targeted than
ACORD 25 — used when the certificate holder needs proof of coverage
on a particular asset rather than blanket policy evidence.

Captures:
- Producer / agency information
- Insured name, address
- Insurer(s) with NAIC numbers
- Specific vehicle or equipment:
  * Year, make, model
  * VIN or serial number
  * Description of the unit
- Auto liability coverage and limits
- Physical damage coverage (comprehensive, collision, deductibles)
- Other coverages as applicable (UM/UIM, medical payments)
- Certificate holder
- Loss Payee / Additional Insured indicators
- Effective and expiration dates

When used:
- Equipment lender / lessor compliance for a specific unit
- Government / contractor proof on a specific vehicle
- Permit applications requiring vehicle-specific coverage proof

Notes:
- Use ACORD 25 instead when the certificate holder just needs
  blanket liability evidence and doesn't care about a specific unit
- Often issued together with the policy declarations page for the
  named vehicle""",
        type_label=CERT,
    ),

    "ACORD 24 (2016-03) Certificate of Property Insurance.txt": card(
        "24", "2016-03", "Certificate of Property Insurance",
        "N/A (reflects underlying policies)",
        "N/A (issued on demand)",
        """Purpose:
Provides evidence of commercial property insurance to a third
party. Used when a certificate holder needs proof of property
coverage (rather than just liability), typically for lease
compliance or contractual requirements. ACORD 25 covers liability;
ACORD 24 covers property.

Captures:
- Producer / agency information
- Insured name, address
- Insurer(s) with NAIC numbers
- Property location(s) and description
- Coverage details:
  * Building (limit, deductible)
  * Business personal property
  * Business income / extra expense
  * Coverage form (special, broad, basic)
  * Coinsurance percentage
- Property valuation method (RC, ACV, agreed value)
- Mortgagee / loss payee / certificate holder
- Effective and expiration dates

When used:
- Commercial lease compliance (lessor requires property cert)
- Loan / lender requirements
- Vendor / contractor obligations involving leased space
- Cross-tenant or shared-occupancy property arrangements

Notes:
- Distinct from ACORD 28 (Evidence of Commercial Property Insurance)
  which is specifically for mortgagee evidence with stricter
  cancellation language
- Often paired with ACORD 25 when both liability and property
  evidence is required""",
        type_label=CERT,
    ),

    "ACORD 26 (2002-01) Policy Certification Log.txt": card(
        "26", "2002-01", "Policy Certification Log",
        "N/A (administrative log)",
        "N/A (administrative tracking)",
        """Purpose:
Internal agency log used to track certificates of insurance issued
against a policy. Provides an audit trail of who received which
certificate, when, and for what coverage — useful for compliance
review, renewal management, and reissuance tracking.

Captures:
- Insured / policy reference (named insured, policy number)
- For each certificate issued:
  * Certificate number / sequence
  * Date issued
  * Certificate holder name and address
  * Type of coverage certified
  * Form used (ACORD 25, 24, etc.)
  * Issuer / authorized representative
  * Reissuance flags (renewal, replacement, etc.)

When used:
- Agency administrative recordkeeping
- E&O compliance / audit trail
- Renewal time review of who received what
- Tracking certificate volume per account

Notes:
- Edition is from 2002 and predates most agency management systems
  that now track this data automatically — many agencies maintain
  the equivalent log in their AMS rather than on paper
- Not issued to third parties; purely an internal document""",
    ),

    "ACORD 27 (2016-03) Evidence of Property Insurance.txt": card(
        "27", "2016-03", "Evidence of Property Insurance",
        "N/A (reflects underlying policies)",
        "N/A (issued on demand — typically at policy inception, renewal, or mortgagee change)",
        """Purpose:
Standard form for evidencing personal lines property insurance
(homeowners, dwelling fire) to a mortgagee or other lender. Replaces
the legacy "binder of insurance" for this purpose. Includes
mortgagee-friendly language about cancellation notice and loss
payable arrangements.

Captures:
- Producer / agency information
- Insured (homeowner) name, address, contact
- Property location (if different from mailing)
- Mortgagee / additional interest (lender) name and address
- Loan number
- Insurer(s) with NAIC numbers
- Policy number, effective and expiration dates
- Policy form (HO-3, HO-5, etc.) or dwelling fire form
- Coverage A (dwelling) limit and deductible
- Coverage B, C, D limits where shown
- Personal liability and medical payments
- Mortgage clause type (standard mortgage clause typical)

When used:
- Mortgagee evidence at policy inception (new home purchase, refi)
- Annual renewal evidence to mortgage servicer
- Mortgagee change requests (loan sold, refinanced)
- Real estate closing requirements

Notes:
- Replaced earlier "binder" formats for personal property evidence
- Mortgagees often request directly from the agency on a recurring
  schedule — many agencies automate ACORD 27 issuance via AMS
- Distinct from ACORD 28 (commercial property evidence)""",
    ),

    "ACORD 28 (2016-03) Evidence of Commercial Property Insurance.txt": card(
        "28", "2016-03", "Evidence of Commercial Property Insurance",
        "N/A (reflects underlying policies)",
        "N/A (issued on demand — typically at policy inception, renewal, or mortgagee change)",
        """Purpose:
Standard form for evidencing commercial property insurance to a
mortgagee or lender. Commercial counterpart to ACORD 27. Used when
a commercial property has loan financing and the lender requires
ongoing evidence of coverage.

Captures:
- Producer / agency information
- Named insured
- Property location
- Mortgagee / additional interest name and address
- Loan number
- Insurer(s) with NAIC numbers
- Policy number, effective and expiration dates
- Coverage form (special, broad, basic, ISO CP)
- Building coverage (limit, deductible, valuation method)
- Business personal property coverage
- Business income / extra expense (if applicable)
- Coinsurance percentage
- Mortgage clause type and any additional lender language

When used:
- Commercial mortgagee evidence at closing
- Annual renewal evidence to commercial lenders
- Loan sale / mortgagee change documentation
- Commercial real estate transactions

Notes:
- Pairs with ACORD 24 (Certificate of Property Insurance) when both
  general property cert AND mortgagee evidence are needed — they
  serve different audiences
- Commercial mortgagees often have specific endorsement requirements
  that need to appear on the policy in addition to the form""",
    ),

    "ACORD 29 (2016-03) Evidence of Flood Insurance.txt": card(
        "29", "2016-03", "Evidence of Flood Insurance",
        "N/A (reflects underlying policies)",
        "N/A (issued on demand — typically at policy inception, renewal, or mortgagee change)",
        """Purpose:
Standard form for evidencing flood insurance — National Flood
Insurance Program (NFIP) policies or private flood policies — to a
mortgagee or lender. Required by federal regulations when the
property is located in a Special Flood Hazard Area (SFHA) and has
a federally backed mortgage.

Captures:
- Producer / agency information
- Insured name and contact
- Property location with FEMA flood zone designation
- Insurer (NFIP carrier or private market)
- Policy number, effective and expiration dates
- Building coverage limit
- Contents coverage limit
- Deductibles (building, contents)
- Mortgagee name, address, loan number
- Whether the policy is NFIP standard or excess/private

When used:
- Initial mortgage closing on properties in SFHAs
- Annual renewal evidence to mortgage servicer
- Flood zone changes triggering mandatory purchase requirements
- Loan sale / mortgagee change documentation

Notes:
- Federally regulated — mortgagees on federally backed loans must
  receive evidence and verify coverage limits at least equal to the
  lower of (a) outstanding loan balance, (b) NFIP maximum, or
  (c) replacement cost
- Private flood policies must meet "private flood insurance"
  definition under federal regulation to satisfy the mandatory
  purchase requirement
- Pairs with NFIP forms 301-308 (Flood Insurance Application,
  endorsements, certifications) when handling the underlying policy""",
    ),

    "ACORD 30 (2016-03) Certificate of Garage Insurance.txt": card(
        "30", "2016-03", "Certificate of Garage Insurance",
        "N/A (reflects underlying policies)",
        "N/A (issued on demand)",
        """Purpose:
Specialty certificate for garage operations — auto dealers, body
shops, repair facilities, valet services. Captures garage liability
AND garagekeepers coverage on a single form, reflecting the unique
exposure of operating on customer vehicles.

Captures:
- Producer / agency information
- Insured (garage operation) name, address
- Insurer(s) with NAIC numbers
- Garage Liability coverage:
  * Each accident / aggregate limits
  * Auto Medical Payments
  * UM/UIM where applicable
- Garagekeepers Coverage:
  * Coverage form (Legal Liability, Direct Primary, Direct Excess)
  * Each-vehicle and aggregate limits
  * Comp and collision deductibles
- Description of operations (dealer, body shop, repair, etc.)
- Certificate holder
- Effective and expiration dates

When used:
- Manufacturer / dealer franchise compliance
- Customer vehicle storage agreements
- Lender requirements on dealer floor plans
- Tow / repair contract compliance

Notes:
- The Garagekeepers coverage form (Legal Liability vs. Direct
  Primary/Excess) materially affects when and how customer-vehicle
  damage is paid — coverage form selection is shown on the cert
- Distinct from ACORD 25 because garage policies have the unique
  Garagekeepers coverage that ACORD 25 doesn't model""",
        type_label=CERT,
    ),

    "ACORD 31 (2016-03) Certificate of Marine - Energy Insurance.txt": card(
        "31", "2016-03", "Certificate of Marine / Energy Insurance",
        "N/A (reflects underlying policies)",
        "N/A (issued on demand)",
        """Purpose:
Specialty certificate for ocean marine, inland marine, and energy
industry insurance. Captures the multi-policy structure typical of
marine and energy programs (hull, P&I, cargo, energy package) on
a single certificate.

Captures:
- Producer / agency information
- Insured name, address
- Insurer(s) with NAIC numbers (often multiple — Lloyd's syndicates,
  marine specialty markets)
- Marine policy parts:
  * Hull and Machinery (vessel value, deductible)
  * Protection and Indemnity (P&I) (limits, club / fixed premium)
  * Cargo coverage (limits per conveyance, locations)
  * Marine Liability / Excess Marine
- Energy policy parts (where applicable):
  * Operators Extra Expense
  * Control of Well
  * Onshore / offshore property and BI
- Vessel or rig identification (where specific assets covered)
- Certificate holder
- Loss Payee / Additional Insured / Notice of Cancellation
- Effective and expiration dates

When used:
- Charter party and vessel operating agreements
- Cargo shipper and consignee documentation
- Energy operator joint operating agreements
- Drilling / service contracts on offshore or onshore rigs
- Lender requirements on marine vessels and energy assets

Notes:
- Marine and energy programs often use multiple specialty insurers
  (Lloyd's, mutual P&I clubs, specialty markets); the certificate
  should list each insurer covering each part
- Replaces use of ACORD 25 for marine/energy because the underlying
  policy structure (e.g. P&I clubs, hull warranties) doesn't fit
  the standard CGL/auto/umbrella layout of ACORD 25""",
        type_label=CERT,
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
    print(f"\nWrote {written} card(s) to {OUT}")


if __name__ == "__main__":
    main()
