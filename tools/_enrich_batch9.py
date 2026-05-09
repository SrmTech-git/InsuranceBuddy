"""Batch 9 — marine, NFIP, watermark stock (17 forms)."""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "raw" / "forms" / "general"


def card(form_num, edition, title, policy_term, transaction_types, body):
    header_edition = f" ({edition})" if edition else ""
    header = f"ACORD {form_num}{header_edition} — {title}"
    rule = "=" * len(header)
    edition_line = f"Edition: {edition}" if edition else "Edition: (not specified)"
    return (
        f"{header}\n{rule}\n"
        f"Form number: ACORD {form_num}\n"
        f"{edition_line}\n"
        f"Title: {title}\n"
        f"Type: Insurance form (ACORD industry standard)\n"
        f"States: All\n"
        f"Policy term: {policy_term}\n"
        f"Transaction types: {transaction_types}\n\n"
        f"{body}\n"
    )


CARDS = {
    "ACORD 275 (2016-03) Aviation Insurance Binder.txt": card(
        "275", "2016-03", "Aviation Insurance Binder",
        "Typically 30-90 days (binder validity period)",
        "Temporary aviation coverage at policy inception",
        """Purpose:
Temporary evidence of aviation insurance coverage in force pending
issuance of the formal aviation policy. Aviation-specific binder
form parallel to ACORD 75 (general Insurance Binder) but tailored to
aviation underwriting requirements (aircraft identification, pilot
qualifications, navigation limits).

Captures:
- Producer / agency information
- Insured / aircraft owner / operator
- Insurer(s) and NAIC numbers
- Aircraft information: N-number, make, model, year, serial number
- Pilot in command information
- Coverage parts bound:
  * Hull (agreed value, deductible)
  * Liability (each occurrence, per passenger seat, PD)
  * Hangarkeepers, premises, products
  * War risk (where applicable)
- Limits and deductibles
- Effective date and binder expiration
- Mortgagee / loss payee / additional insured
- Underwriter approval

When used:
- Aircraft purchase requiring immediate coverage
- Closing on aircraft financing or lease
- Court-ordered coverage on aviation assets
- Bridge between policy negotiation and formal issuance

Notes:
- Aviation binders typically have stricter underwriter approval
  requirements than standard property/casualty binders
- Pairs with ACORD 75 (general binder) — used in lieu of when the
  exposure is aviation-specific
- Often paired with ACORD 21 (Certificate of Aircraft Insurance)
  once policy issues""",
    ),

    "ACORD 276 (2016-03) Aircraft Insurance Binder.txt": card(
        "276", "2016-03", "Aircraft Insurance Binder",
        "Typically 30-90 days (binder validity period)",
        "Temporary aircraft coverage at policy inception",
        """Purpose:
Aircraft-specific binder for temporary evidence of insurance on a
particular aircraft. More focused than ACORD 275 (Aviation Insurance
Binder) — captures the specific aircraft and the hull and liability
coverage on it pending formal policy issuance.

Captures:
- Producer / agency information
- Insured / aircraft owner / operator
- Aircraft: N-number, make, model, year, serial number
- Insurer(s)
- Hull coverage (agreed value, deductibles)
- Liability coverage (each occurrence, per passenger, PD)
- Pilot information
- Effective date and binder expiration
- Lender / lessor / loss payee
- Underwriter approval

When used:
- Aircraft purchase closing requiring immediate proof of insurance
- Aircraft delivery from manufacturer or seller
- Lender-required temporary coverage
- Bridge to formal policy issuance

Notes:
- Pairs with ACORD 21 (Certificate of Aircraft Insurance) issued
  once the policy is bound
- Distinct from ACORD 275 (general aviation binder) which can
  cover broader operations rather than a specific aircraft""",
    ),

    "ACORD 281 (2016-05) Personal Inland Marine Section.txt": card(
        "281", "2016-05", "Personal Inland Marine Section",
        "12 months (typical)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for personal inland marine coverage when
endorsed onto a homeowners or other personal lines policy. Captures
scheduled and blanket personal property coverage detail without
requiring a separate stand-alone IM application (ACORD 81).

Captures:
- Reference to underlying personal lines policy
- Scheduled items:
  * Description, value, year acquired
  * Appraisal date and appraiser
  * Photographs available
  * Storage location
- Blanket coverage on unscheduled categories:
  * Jewelry blanket sublimit
  * Fine arts blanket
  * Silverware
  * Other personal property
- Coverage form (all-risk, named perils)
- Deductibles
- Loss history on personal property
- Security: alarms, safes, vault

When used:
- Endorsing personal IM onto an existing HO policy
- Adding scheduled jewelry, fine art, or collectibles
- Renewal review of scheduled values
- After major personal property purchases

Notes:
- Pairs with ACORD 80 (Homeowner Application) or ACORD 81
  (Personal Inland Marine Application) depending on whether IM is
  an endorsement or stand-alone policy
- Appraisals typically required for items above carrier thresholds
  (often $5,000+)""",
    ),

    "ACORD 282 (2025-07) Watercraft Section.txt": card(
        "282", "2025-07", "Watercraft Section",
        "12 months (typical, may be seasonal in northern markets)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for personal watercraft coverage when
endorsed onto a personal lines policy package. Captures the
watercraft, use, navigation area, and coverage detail. Used as a
section within a multi-line personal submission rather than the
stand-alone ACORD 82 (Watercraft Application).

Captures:
- Reference to underlying personal lines policy
- Watercraft information: year, make, model, length, hull material,
  propulsion, HIN
- Trailer (if applicable): year, make, value
- Use: pleasure, fishing, racing
- Navigation area: lakes, coastal, ocean, US/international
- Storage: in water, dry storage, trailered
- Operator information: experience, USCG license, prior losses
- Coverage:
  * Hull (agreed value, ACV, deductible)
  * Liability limit
  * Medical payments
  * Uninsured boater
  * On-water towing
- Loss history

When used:
- Adding watercraft to a multi-line personal package
- Renewal review of watercraft coverage
- Pairs with ACORD 82 (Watercraft Application) for stand-alone
  policies

Notes:
- For larger yachts (typically 26+ feet), use ACORD 210 (Yacht
  Section) instead
- 2025-07 edition reflects current market practices for personal
  watercraft underwriting""",
    ),

    "ACORD 283 (2025-07) Personal Umbrella Application Section.txt": card(
        "283", "2025-07", "Personal Umbrella Application Section",
        "12 months (typical)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for personal umbrella coverage when
endorsed onto a personal lines package. Captures household, vehicles,
properties, and underlying policies the umbrella sits over. Used as
a section within a multi-line personal submission rather than the
stand-alone ACORD 83 (Personal Umbrella Application).

Captures:
- Reference to underlying personal lines policies
- Umbrella limit requested ($1M, $2M, $5M, higher)
- Underlying policies (auto, HO, watercraft, etc.):
  * Carriers
  * Limits (must meet umbrella underlying requirements)
  * Effective dates
- Household members and drivers
- Vehicles (autos, motorcycles, RVs, ATVs)
- Watercraft, aircraft (where applicable)
- Rental properties owned
- Business activities, board / officer positions
- Domestic employees
- Loss history
- Animals, special exposures (pools, trampolines, etc.)
- Underwriting questions (foreign travel, criminal history, etc.)

When used:
- Adding umbrella to a multi-line personal package
- Renewal review of umbrella limits
- Pairs with ACORD 83 (Personal Umbrella Application) for
  stand-alone policies

Notes:
- Underlying limits requirement is strict (typically $250/500/100K
  auto and $300K HO)
- 2025-07 edition reflects current carrier requirements""",
    ),

    "ACORD 285 (2024-06) Commercial Marine Insurance Supplement Hull & Machinery & Protection & Indemnity.txt": card(
        "285", "2024-06", "Commercial Marine Insurance Supplement Hull & Machinery & Protection & Indemnity",
        "12 months (typical commercial term)",
        "New business / renewal underwriting (commercial marine)",
        """Purpose:
Underwriting supplement for commercial marine vessels covering Hull
& Machinery (H&M) and Protection & Indemnity (P&I) — the two core
commercial marine coverages. Captures vessel, voyage, crew, and
operational detail beyond what the certificate (ACORD 31) provides.

Captures:
- Reference to ACORD 125
- Vessel information:
  * Name, official number, IMO number, MMSI
  * Type (cargo, tanker, tug, fishing, passenger, offshore supply)
  * Year built, builder, country of build
  * Tonnage (gross, net, deadweight)
  * Length, beam, draft
  * Classification society
  * Class certificates and surveys
  * Insured value (H&M)
- Trading area / routes
- Crew complement and qualifications
- Cargo carried (where applicable)
- Hull & Machinery coverage:
  * Agreed value
  * Deductible
  * War / strikes coverage
  * Increased value coverage
- Protection & Indemnity:
  * P&I club membership (or fixed-premium market)
  * P&I limits
  * Pollution coverage
  * Crew coverage / Jones Act exposure
- Loss history

When used:
- Commercial vessel new business
- Renewal of marine programs
- Vessel acquisition or fleet additions
- Jones Act / maritime employer exposure

Notes:
- P&I clubs (mutual insurance) operate differently from fixed-
  premium markets — captured detail differs accordingly
- Pairs with ACORD 31 (Certificate of Marine / Energy Insurance)
  for evidence to charterers and lenders""",
    ),

    "ACORD 301 (2022-12) National Flood Insurance Program Flood Insurance Application.txt": card(
        "301", "2022-12", "National Flood Insurance Program Flood Insurance Application",
        "12 months (NFIP standard)",
        "New business, renewal (NFIP / Write Your Own carriers)",
        """Purpose:
Application for flood insurance under the National Flood Insurance
Program (NFIP). Used by NFIP direct policies and Write Your Own
(WYO) carriers to issue NFIP-backed flood coverage on residential
and commercial properties.

Captures:
- Producer / agency information
- Applicant / policyholder
- Property address (with FEMA flood zone designation)
- Community participation status (NFIP-participating community)
- Flood zone (X, A, AE, AH, AO, V, VE, etc.)
- Elevation Certificate information (where required)
- Property occupancy:
  * Single-family, 2-4 family, multi-family, residential
    condominium, non-residential, mobile home
  * Primary, secondary, rental, business
- Building characteristics:
  * Year built (pre-FIRM vs. post-FIRM)
  * Number of floors, basement, crawl space
  * Foundation type
  * Square footage
- Coverage requested:
  * Building coverage
  * Contents coverage
  * Building deductible
  * Contents deductible
- Mortgagee / loss payee
- Risk Rating 2.0 information
- Loss history (NFIP and private flood)

When used:
- New flood insurance business
- Required when properties in SFHAs have federally backed mortgages
- Renewal (annual)
- Mortgagee changes

Notes:
- NFIP transitioned to Risk Rating 2.0 in 2021 — premiums based on
  individual property characteristics rather than flood zone alone
- Pairs with ACORD 29 (Evidence of Flood Insurance) for mortgagee
  evidence
- Pre-FIRM vs. post-FIRM (FIRM = Flood Insurance Rate Map) status
  affects rates and grandfathering""",
    ),

    "ACORD 302 (2015-04) NFIP – Flood Insurance General Change Endorsement.txt": card(
        "302", "2015-04", "NFIP – Flood Insurance General Change Endorsement",
        "N/A (existing NFIP policy)",
        "Mid-term change / endorsement on NFIP policy",
        """Purpose:
General change endorsement form for active NFIP policies. Used to
update coverage limits, deductibles, mortgagee information,
property characteristics, or other policy details mid-term.

Captures:
- Reference to underlying NFIP policy (policy number, insured)
- Effective date of change
- Type of change requested:
  * Coverage limit changes (building, contents)
  * Deductible changes
  * Mortgagee additions / changes
  * Property characteristic updates (occupancy, elevation, etc.)
  * Address changes
  * Insured name changes
- Description of change
- Premium impact
- Insured signature

When used:
- Mid-term coverage adjustments on NFIP policies
- Mortgagee change after loan transfer
- Property updates affecting rating

Notes:
- NFIP changes have specific waiting periods — coverage increases
  often require 30-day waiting period
- Pairs with ACORD 301 (NFIP Application) — change is to the
  policy issued from that application""",
    ),

    "ACORD 303 (2015-04) NFIP – Flood Insurance Preferred Risk Policy Application.txt": card(
        "303", "2015-04", "NFIP – Flood Insurance Preferred Risk Policy Application",
        "12 months (NFIP standard)",
        "New business, renewal (Preferred Risk Policy variant)",
        """Purpose:
Application for the NFIP Preferred Risk Policy (PRP) — a low-cost
flood insurance option for properties in low-to-moderate risk flood
zones (B, C, X). Streamlined version of ACORD 301 with limited
coverage options at preferred rates.

Captures:
- Producer / agency information
- Applicant / policyholder
- Property address
- Flood zone (must be B, C, or X for PRP eligibility)
- Property type (1-4 family residential, non-residential)
- Occupancy
- Coverage tier selected (PRP offers fixed coverage tiers rather
  than custom limits)
- Mortgagee / loss payee
- Loss history (limited NFIP losses; properties with significant
  loss history may not qualify)

When used:
- Low-risk-zone flood insurance new business
- Customers wanting basic flood coverage at affordable rates
- Renewal of PRP policies

Notes:
- PRP is being phased out / merged into Risk Rating 2.0 — available
  policies may still exist but new business directives have changed
- Properties that experience repetitive flood losses lose PRP
  eligibility""",
    ),

    "ACORD 304 (2022-12) NFIP – Flood Insurance Cancellation - Nullification.txt": card(
        "304", "2022-12", "NFIP – Flood Insurance Cancellation / Nullification",
        "N/A (existing NFIP policy)",
        "Cancellation or nullification of NFIP policy",
        """Purpose:
Cancellation or nullification request for active NFIP policies.
Documents the specific NFIP-approved cancellation reason and the
effective date. Unlike many private market policies, NFIP requires
specific reason codes for cancellation.

Captures:
- Reference to NFIP policy
- Cancellation effective date
- NFIP-approved cancellation reason code:
  * Sale of property
  * Duplicate NFIP policy
  * Insured no longer has insurable interest
  * Policy condemned / property destroyed
  * Mistake in writing the policy
  * Other approved reason
- Refund calculation (NFIP has specific refund rules by reason)
- Mortgagee notification (often required for federally backed loans)
- Insured signature

When used:
- Property sold and new owner gets their own policy
- Property destroyed and rebuilding not planned
- Duplicate coverage discovered
- Mortgage paid off and no other requirement for flood coverage

Notes:
- NFIP cancellation reasons are strictly defined; not every reason
  is eligible for refund
- Mortgagee on federally backed loans may have rights that affect
  cancellation timing
- Pairs with ACORD 301 (NFIP Application) for the underlying policy""",
    ),

    "ACORD 305 (2012-02) NFIP – Credit Card Payment Form.txt": card(
        "305", "2012-02", "NFIP – Credit Card Payment Form",
        "N/A (payment authorization)",
        "Premium payment authorization (NFIP)",
        """Purpose:
Authorization form for credit card payment of NFIP flood insurance
premiums. Used when the insured pays NFIP premium by credit card
rather than check, ACH, or escrow.

Captures:
- Reference to NFIP policy or application
- Cardholder name
- Card type (Visa, MasterCard, Discover, AMEX)
- Card number, expiration date, security code
- Billing address
- Authorized payment amount
- Insured signature authorizing the charge

When used:
- New NFIP policy where insured pays premium directly by card
- Renewal premium payment by card
- Endorsement-driven additional premium

Notes:
- PCI-DSS compliance considerations apply when collecting card
  data; many agencies now use online payment portals instead of
  paper forms
- Pairs with ACORD 301 (NFIP Application)""",
    ),

    "ACORD 306 (2011-04) NFIP – Rating Information and Elevated Building Determination Form.txt": card(
        "306", "2011-04", "NFIP – Rating Information and Elevated Building Determination Form",
        "N/A (rating documentation)",
        "Rating support documentation (NFIP)",
        """Purpose:
Rating information form for NFIP policies on elevated buildings —
buildings raised on pilings, piers, posts, or columns above grade.
Captures the elevation and construction characteristics that drive
NFIP elevated building rating, particularly important in coastal V
and VE zones.

Captures:
- Reference to NFIP policy or application
- Property address
- Flood zone (V, VE, AE, etc.)
- Building elevation:
  * Lowest floor elevation
  * Lowest adjacent grade
  * Base flood elevation (BFE) from FIRM
  * Elevation of machinery and equipment
- Foundation type:
  * Pilings, piers, posts, columns
  * Number and spacing of supports
  * Foundation walls (if applicable)
- Enclosure characteristics:
  * Enclosed area below the elevated floor
  * Use (parking, storage, machinery, finished living)
  * Breakaway walls (V zone requirement)
  * Flood vents / openings
- Elevation Certificate reference
- Diagram of building section (often attached)

When used:
- New NFIP business on elevated buildings (especially coastal)
- Rating verification on existing policies
- Substantial improvements / additions to elevated buildings
- Re-rating after FIRM revisions

Notes:
- Elevation Certificate (FEMA Form 81-31) is the foundational
  document; ACORD 306 supplements it for NFIP rating
- Critical for V-zone and post-FIRM AE-zone rating""",
    ),

    "ACORD 307 (2016-02) NFIP – Floodproofing Certificate for Non-Residential Structures.txt": card(
        "307", "2016-02", "NFIP – Floodproofing Certificate for Non-Residential Structures",
        "N/A (rating documentation)",
        "Rating support documentation (NFIP non-residential)",
        """Purpose:
Floodproofing certificate documenting that a non-residential
structure has been floodproofed to NFIP-approved standards.
Floodproofing — making a building water-tight to a specified
elevation — can qualify a non-residential structure for rating as
if it were elevated, significantly reducing flood premium.

Captures:
- Reference to NFIP policy or application
- Property address
- Building characteristics
- Floodproofing design:
  * Floodproofing elevation (must be at or above BFE + 1 foot)
  * Sealants, barriers, closures
  * Sump pumps, drainage
  * Engineered design certification
- Certifying engineer or architect (license, signature)
- Annual inspection / maintenance plan
- Operations and maintenance manual reference
- Photographs and design drawings (typically attached)

When used:
- Non-residential properties in SFHAs that have been floodproofed
- New construction designed with floodproofing
- Existing buildings retrofitted for floodproofing

Notes:
- Floodproofing is only allowed on non-residential structures —
  residential floodproofing is prohibited under NFIP rules
- Annual recertification of floodproofing is typically required
- Engineer / architect must be licensed in the state of the property""",
    ),

    "ACORD 308 (2015-04) NFIP – Residential Basement Floodproofing Certificate.txt": card(
        "308", "2015-04", "NFIP – Residential Basement Floodproofing Certificate",
        "N/A (rating documentation)",
        "Rating support documentation (NFIP residential basement)",
        """Purpose:
Floodproofing certificate for residential basements in
NFIP-participating communities that have been granted FEMA exception
for residential basement floodproofing. A limited program — most
residential basement floodproofing is not allowed under NFIP, but
specific communities have approved exceptions.

Captures:
- Reference to NFIP policy or application
- Property address
- Community NFIP participation status
- Community-granted floodproofing exception (must be in effect)
- Basement floodproofing details:
  * Floodproofing elevation
  * Sealants, barriers
  * Sump pumps, drainage
  * Mechanical equipment elevation
- Certifying engineer or architect
- Annual maintenance plan

When used:
- Residential properties in communities with NFIP-approved
  basement floodproofing exceptions
- New construction or retrofits in eligible communities
- Rare — most communities don't have basement floodproofing
  exceptions

Notes:
- Most residential basement floodproofing is NOT allowed under NFIP
  rules; check community participation and exception status before
  using this form
- Pairs with ACORD 307 (Non-Residential Floodproofing Certificate)
  which covers the more common non-residential use case""",
    ),

    "ACORD 350 Watermark Paper – 20 # ID Card Stock (4-part perforation).txt": card(
        "350", "", "Watermark Paper – 20 # ID Card Stock (4-part perforation)",
        "N/A (physical material)",
        "N/A (physical material)",
        """Purpose:
Physical paper stock — watermarked, 20-pound weight, with 4-part
perforation — used for printing automobile insurance ID cards
(ACORD 50 WM and similar). Provides fraud-prevention features
(watermark) and convenient perforations for separating multi-part
documents.

Captures:
- This is a physical paper specification, not a data form
- Stock characteristics:
  * 20 # weight (lighter weight, suitable for ID cards in wallet
    or vehicle)
  * Watermark (fraud-prevention feature visible when held to light)
  * 4-part perforation (for separating into multiple cards)

When used:
- Printing ACORD 50 WM (Auto ID Card with Watermark)
- Producer / agency offices that print physical ID cards
- States or carriers requiring watermark stock for fraud prevention

Notes:
- Physical material rather than a data-bearing form — the underlying
  ACORD form is what carries data; the paper stock supports printing
- Pairs with ACORD 360 (32 # ID Card Stock) and ACORD 370 (32 # non-
  perforated) for related paper stocks
- Increasingly rare as electronic ID card delivery has become
  standard""",
    ),

    "ACORD 360 Watermark Paper – 32 # ID Card Stock (4-part perforation).txt": card(
        "360", "", "Watermark Paper – 32 # ID Card Stock (4-part perforation)",
        "N/A (physical material)",
        "N/A (physical material)",
        """Purpose:
Physical paper stock — watermarked, 32-pound weight (heavier, more
durable than 20#), with 4-part perforation — used for printing
automobile insurance ID cards. Heavier weight provides longer-
lasting cards for wallet or vehicle storage.

Captures:
- This is a physical paper specification, not a data form
- Stock characteristics:
  * 32 # weight (heavier, more durable for repeated handling)
  * Watermark (fraud-prevention feature)
  * 4-part perforation (for separating into multiple cards)

When used:
- Printing ACORD 50 WM (Auto ID Card with Watermark) when heavier
  stock is preferred
- States or carriers requiring more durable ID cards
- Producer / agency offices favoring heavier-weight cards

Notes:
- Physical material rather than a data-bearing form
- Pairs with ACORD 350 (20 # weight) and ACORD 370 (32 # non-
  perforated)
- Heavier weight chosen when card durability is prioritized over
  print volume / cost""",
    ),

    "ACORD 370 Watermark Paper – 32 # ID Card Stock (non-perforated).txt": card(
        "370", "", "Watermark Paper – 32 # ID Card Stock (non-perforated)",
        "N/A (physical material)",
        "N/A (physical material)",
        """Purpose:
Physical paper stock — watermarked, 32-pound weight, without
perforations — used for printing automobile insurance ID cards
when the cards are cut to size by a printer or trimmer rather than
separated by hand at perforations. For high-volume or
custom-printed environments.

Captures:
- This is a physical paper specification, not a data form
- Stock characteristics:
  * 32 # weight (heavier, more durable)
  * Watermark (fraud-prevention feature)
  * Non-perforated (cut to size by printer / trimmer)

When used:
- High-volume ID card printing environments where mechanical cutting
  is more efficient than hand-separation
- Custom card layouts that don't fit the standard 4-part perforation
- Producer offices with appropriate paper trimming equipment

Notes:
- Physical material rather than a data-bearing form
- Pairs with ACORD 350 (20 # 4-part) and ACORD 360 (32 # 4-part)
- Choice between perforated and non-perforated depends on the
  printing workflow""",
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
