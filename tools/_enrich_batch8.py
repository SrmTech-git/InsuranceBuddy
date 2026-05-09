"""Batch 8 — specialty commercial supplements (17 forms)."""
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
    "ACORD 180 (2016-03) Technology E&O Section – Electronic Data Processors, Electric Products Manufacturers, Computer Services etc..txt": card(
        "180", "2016-03", "Technology E&O Section – Electronic Data Processors, Electric Products Manufacturers, Computer Services etc.",
        "12 months (typical commercial term)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for technology errors and omissions
(tech E&O) coverage. Captures the unique professional liability
exposure of technology service providers — software developers, IT
consultants, electronic data processors, computer services,
electronics manufacturers — whose errors can cause financial loss
to clients without bodily injury or property damage.

Captures:
- Reference to ACORD 125
- Tech E&O coverage parts:
  * Professional liability (errors and omissions)
  * Technology products liability
  * Network security / privacy (often referred to ACORD 834)
  * Media liability (where applicable)
- Services performed:
  * Software development / customization
  * IT consulting / managed services
  * Hardware sales / installation / maintenance
  * Cloud / SaaS / hosting
  * Data processing / electronic records
- Annual revenue by service line
- Client industries served
- Contract terms (LoL caps, indemnification, hold harmless)
- Quality control: testing, version control, documentation
- Subcontractor / outsourcing arrangements
- Loss history (E&O claims, near-misses)

When used:
- Tech E&O new business
- Renewal review
- Adding tech E&O to existing commercial submissions

Notes:
- Distinct from cyber liability (ACORD 834) — tech E&O covers
  professional service errors; cyber covers data breach response
  and security failures
- Many carriers package tech E&O with cyber as a "tech / cyber"
  product""",
    ),

    "ACORD 185 (2011-09) Restaurant - Tavern Supplement.txt": card(
        "185", "2011-09", "Restaurant / Tavern Supplement",
        "12 months (typical commercial term)",
        "New business / renewal underwriting (specialty exposure detail)",
        """Purpose:
Underwriting supplement for restaurants, taverns, bars, and food
service operations. Captures the operational characteristics that
drive both property and liability rating — kitchen equipment, alcohol
service, hours of operation, entertainment, food preparation type.

Captures:
- Reference to ACORD 125 / 140 / 160 (BOP often used for restaurants)
- Operation type (full-service restaurant, fast food, tavern,
  brewpub, nightclub, catering)
- Annual revenue, revenue mix (food vs. alcohol)
- Hours of operation (especially late-night exposure)
- Kitchen and cooking equipment:
  * Type of cooking (deep frying, broiling, charbroiling)
  * Hood / suppression system (UL 300, Ansul, last service)
  * Grease management
- Alcohol service:
  * % of sales from alcohol
  * Liquor liability coverage
  * TIPS / responsible service training
  * Late-night service
- Entertainment (live music, DJ, dance floor, karaoke)
- Outdoor seating, patio
- Off-premise catering
- Delivery operations (auto exposure)
- Loss history (slips/falls, food liability, liquor, fire)

When used:
- Restaurant / tavern new business
- BOP submissions for food service
- Renewal review
- Adding liquor liability to existing restaurant policy

Notes:
- Hood / fire suppression maintenance is a key underwriting
  question — expired suppression systems are a major fire risk
- Liquor liability ("dram shop") is heavily state-regulated; some
  states have very high statutory damages""",
    ),

    "ACORD 186 (2011-10) Contractors Supplement.txt": card(
        "186", "2011-10", "Contractors Supplement",
        "12 months (typical commercial term)",
        "New business / renewal underwriting (specialty exposure detail)",
        """Purpose:
Underwriting supplement for contractors and construction operations.
Captures the trade type, work performed, subcontracting practices,
and exposure mix that drive contractor general liability and
contractors equipment underwriting.

Captures:
- Reference to ACORD 125 / 126 (CGL)
- Contractor type (general, subcontractor, specialty trade)
- Trades performed (% of revenue per trade):
  * Roofing, framing, electrical, plumbing, HVAC
  * Concrete, masonry, drywall, painting
  * Excavation, demolition, paving
  * Specialty (waterproofing, scaffolding, crane, blasting, etc.)
- Residential vs. commercial vs. industrial mix
- New construction vs. renovation / remodeling vs. service work
- Annual revenue and payroll
- Subcontractor usage (% of work subbed out, certificate of
  insurance requirements, hold harmless agreements)
- Work at heights, in confined spaces, with hazardous materials
- Use of cranes, hoists, scaffolding, mobile equipment
- Geographic operating area
- Quality control / safety programs (OSHA recordable incidents)
- Loss history (CGL, auto, WC, equipment)

When used:
- Contractor new business
- Renewal review
- Multi-line contractor submissions (CGL + auto + WC + equipment)

Notes:
- Subcontractor controls are critical — uninsured subs become the
  GC's exposure on losses
- Pairs with ACORD 147 (Installation / Builders Risk) where the
  contractor takes property risk
- Heavy underwriting focus on prior loss frequency, especially
  water damage / construction defect""",
    ),

    "ACORD 187 (2016-03) Professional Liability Supplement.txt": card(
        "187", "2016-03", "Professional Liability Supplement",
        "12 months (typical, usually claims-made)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Generic professional liability (errors & omissions) supplement for
service professions — accountants, consultants, real estate agents,
insurance agents, and other professionals whose work product creates
financial-loss exposure to clients.

Captures:
- Reference to ACORD 125
- Profession / services provided
- Annual gross revenue and number of professionals
- Years in practice
- Claims-made vs. occurrence form
- Retroactive date (claims-made)
- Extended Reporting Period (tail) requirements
- Coverage limits:
  * Each claim
  * Aggregate
  * Defense in or outside the limit
- Deductible / SIR
- Services performed in detail (descriptions, % of revenue per
  service)
- Geographic scope
- Client mix (corporate, individual, government, regulatory)
- Quality control: peer review, supervision, documentation
- Use of subcontractors / independent contractors
- Engagement letter practices
- Loss history (E&O claims, regulatory complaints, disciplinary
  actions)

When used:
- Generic E&O new business for professions without dedicated forms
- Renewal review for ongoing E&O policies
- Coverage transitions (claims-made retroactive date considerations)

Notes:
- Specific professions have dedicated forms (ACORD 196 medical
  professional liability, 825 management/executive lines, 833
  lawyers, 838 accountants, etc.) — use those when available
- Claims-made retroactive date is critical — coverage gaps between
  prior and new policies expose the insured""",
    ),

    "ACORD 190 (2013-09) Supplemental Property Application.txt": card(
        "190", "2013-09", "Supplemental Property Application",
        "12 months (typical commercial term)",
        "New business / renewal underwriting (additional property detail)",
        """Purpose:
Supplement to ACORD 140 (Property Section) capturing additional
property underwriting detail not accommodated by the main property
section. Used when the property exposure has unique characteristics
or risk factors requiring deeper underwriting.

Captures:
- Reference to ACORD 125 / 140
- Specific property features needing additional disclosure:
  * Special construction (heavy timber, fire-resistive, mixed)
  * Specialty occupancies (warehouse, manufacturing, processing)
  * High-value contents requiring scheduled coverage
  * Spoilage / temperature control exposure
  * Vacancy or partial occupancy
  * Renovation activity
- Protection details:
  * Sprinkler coverage (% of building, dry vs. wet, monitoring)
  * Fire alarm (central station, local, monitored)
  * Burglar alarm (UL grade)
  * Watchman / security
- Catastrophe exposure detail (hurricane, earthquake, wildfire,
  flood)
- Building code / ordinance compliance
- Recent inspections / engineering reports
- Loss control recommendations from prior carriers

When used:
- Complex commercial property submissions
- Properties with unusual exposures or recent claims
- Schedule of large or high-value buildings
- Carrier-specific underwriting requests

Notes:
- Pairs with ACORD 140 (Property Section) and ACORD 139 (SOV)
- Often a carrier-specific or specialty market requirement""",
    ),

    "ACORD 193 (2009-03) Open Cargo Section.txt": card(
        "193", "2009-03", "Open Cargo Section",
        "12 months (typical, with annual reporting)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for open cargo (ocean and inland marine
cargo) coverage on a continuous, all-risk basis. Used for shippers
and consignees who move goods regularly and need ongoing coverage
rather than trip-by-trip insurance.

Captures:
- Reference to ACORD 125
- Cargo coverage details:
  * Commodities shipped (description, special hazards)
  * Annual shipment volume / values
  * Maximum value per conveyance
  * Mode (ocean, air, motor truck, rail, intermodal)
  * Geographic origins and destinations
- Coverage form:
  * Institute Cargo Clauses (A, B, C) for ocean
  * All risk vs. named perils
  * Warehouse-to-warehouse coverage
- Limits per occurrence and aggregate
- Deductible
- Refrigeration / temperature control
- Storage in transit (terminals, warehouses)
- Reporting / declaration requirements
- War, strikes, riots, civil commotion (often separate)
- Loss history

When used:
- Manufacturers, distributors, importers / exporters
- Logistics and freight forwarders (cargo on customers' behalf)
- Renewal of open cargo policies

Notes:
- Distinct from ACORD 143 (Transportation Section) which focuses on
  motor truck cargo for domestic carriers; ACORD 193 covers the
  shipper / consignee side and includes ocean cargo
- Pairs with ACORD 31 (Certificate of Marine / Energy Insurance)
  for evidence to third parties""",
    ),

    "ACORD 194 (2009-03) Truckers - Motor Carrier Supplement.txt": card(
        "194", "2009-03", "Truckers / Motor Carrier Supplement",
        "12 months (typical commercial term)",
        "New business / renewal underwriting (additional trucking detail)",
        """Purpose:
Supplement to ACORD 132 (Truckers / Motor Carriers Section)
capturing additional underwriting detail specific to motor carrier
operations. Used when the standard ACORD 132 doesn't capture enough
trucking-specific exposure information.

Captures:
- Reference to ACORD 125 / 132
- Operating authority detail:
  * Federal MC# and DOT# verification
  * State authorities held
  * Hazmat endorsements
  * Operating jurisdictions
- Fleet detail beyond ACORD 132:
  * Power units by type (tractor, straight truck, day cab, sleeper)
  * Trailers by type (van, reefer, flatbed, tank, intermodal)
  * Average vehicle age / value
  * Owner-operators vs. company drivers
- Driver detail:
  * Driver hiring criteria
  * Drug and alcohol testing program
  * Hours of service compliance
  * Driver retention rate
  * MVR review frequency
- DOT compliance:
  * Safety rating (Satisfactory, Conditional, Unsatisfactory)
  * BASIC scores (Behavior Analysis Safety Improvement Categories)
  * CSA scores
  * DOT compliance reviews / audits
  * Out-of-service rates
- Cargo handling:
  * Freight types
  * High-theft commodities (electronics, pharmaceuticals)
  * Special handling (hazmat, oversize, refrigerated)
- Loss history detail beyond ACORD 132

When used:
- Standard motor carrier submissions
- Hazmat carriers requiring additional disclosure
- Carriers with prior DOT compliance issues

Notes:
- Pairs with ACORD 132 — supplemental detail rather than standalone
- DOT BASIC scores and Safety Rating are critical underwriting
  factors""",
    ),

    "ACORD 195 (1996-10) Design Professional's Individual Property Survey.txt": card(
        "195", "1996-10", "Design Professional's Individual Property Survey",
        "Project-based or matched to underlying policy",
        "Project review / underwriting documentation",
        """Purpose:
Property survey form completed by a design professional (architect,
engineer) documenting a building's characteristics for insurance
underwriting purposes. Used when a building's value or condition
needs to be established by a professional rather than relying on
self-reported information.

Captures:
- Property location and description
- Design professional information (license, firm, contact)
- Building characteristics:
  * Construction type and quality
  * Age, additions, renovations
  * Structural integrity
  * Mechanical / electrical / plumbing
  * Roof condition and remaining life
  * Foundation
- Replacement cost analysis:
  * Construction quality
  * Building code requirements
  * Site conditions
  * Calculated replacement cost per square foot
- Recommended coverage limits
- Conditions / deficiencies noted
- Estimated repair / improvement costs

When used:
- High-value properties requiring professional valuation
- Historic buildings or unusual construction
- Disputed coverage limits / coinsurance issues
- After-loss disputes where construction cost is contested

Notes:
- Edition is from 1996 — modern carriers typically use proprietary
  appraisal services or reconstruction cost software rather than
  this form; still occasionally used for unique buildings
- Distinct from ACORD 42 (Residential Property Replacement Cost)
  which is for residential underwriting""",
    ),

    "ACORD 196 (2013-09) Medical Professional Liability Insurance Application.txt": card(
        "196", "2013-09", "Medical Professional Liability Insurance Application",
        "12 months (typical, usually claims-made)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Application for medical professional liability (medical malpractice)
insurance covering physicians, surgeons, allied health professionals,
and medical groups. Captures the practice characteristics, procedures
performed, and risk management practices that drive med-mal
underwriting.

Captures:
- Producer / agency information
- Applicant / insured (individual physician, group, facility)
- Specialty / specialties practiced
- Medical license details (state, license #, year licensed)
- Board certifications
- Hospital affiliations and privileges
- Procedures performed and frequency:
  * High-risk procedures (especially surgical)
  * Office-based vs. hospital-based
- Patient volume (annual visits, surgeries, deliveries)
- Practice setting (solo, group, employed, locum tenens)
- Prior carriers and continuous coverage
- Claims-made retroactive date
- Tail / Extended Reporting Period requirements
- Coverage limits:
  * Per claim / annual aggregate
  * Defense within or outside limits
- Deductible / SIR
- Subcontracted physicians, residents, fellows
- Non-physician staff (NPs, PAs, RNs, technicians)
- Risk management practices (peer review, EMR, informed consent)
- Loss history (claims, settlements, adverse outcomes, disciplinary
  actions)
- Sanctions, restrictions, license actions

When used:
- Physician new business
- Group / facility med-mal submissions
- Renewal review with retroactive date considerations
- Carrier transitions requiring tail or nose coverage

Notes:
- Med-mal is heavily state-specific and specialty-specific —
  underwriting and rates vary dramatically by state and specialty
- Tail coverage at policy expiration can be costly; non-renewal
  planning is critical""",
    ),

    "ACORD 199 (1999-01) Application Supplement – Undertaking.txt": card(
        "199", "1999-01", "Application Supplement – Undertaking",
        "Matches underlying policy",
        "New business / renewal underwriting (formal undertaking / disclosure)",
        """Purpose:
Insured's signed undertaking (formal acknowledgment) of specific
underwriting representations, conditions, or commitments. Used when
the underwriter requires the insured to attest under penalty of
misrepresentation to specific facts or commitments — beyond what's
on the standard application.

Captures:
- Reference to underlying application / policy
- Insured / applicant identification
- Specific undertakings being made:
  * Compliance with code requirements / building updates
  * Implementation of safety / security measures
  * Maintenance of specific procedures
  * Disclosure of specific facts (prior losses, conditions, etc.)
  * Acknowledgment of policy exclusions / conditions
- Effective date of the undertaking
- Insured signature with date
- Witness signature (where required)

When used:
- Underwriting accommodations conditional on specific commitments
- Reinstatement following lapse with specific conditions
- High-hazard or specialty submissions requiring additional
  representations
- Backdating coverage with specific representations

Notes:
- Edition is from 1999 and the form sees less use today — most
  modern undertakings are captured via specific endorsement
  conditions or carrier-specific forms
- Material misrepresentation in an undertaking generally voids
  coverage in the same way as misrepresentation on the application""",
    ),

    "ACORD 200 (1993-03) Producer Account.txt": card(
        "200", "1993-03", "Producer Account",
        "N/A (administrative form)",
        "Producer onboarding / agency administration",
        """Purpose:
Producer / agency information form establishing or maintaining a
producer's account relationship with a carrier. Captures the
producer's licensing, E&O coverage, banking, commission structure,
and authorization to write business with the carrier.

Captures:
- Agency / producer name, address, contact
- Tax ID / FEIN
- Licensing detail by state
- Lines of authority (P&C, life, health, surplus lines, etc.)
- E&O insurance details (carrier, limit, expiration)
- Banking / ACH information for commission deposits
- Commission structure agreed to
- Production goals / minimums
- Sub-producers and downline producers (where applicable)
- Authorized signatories
- Compliance certifications (anti-money laundering, fraud awareness)

When used:
- New producer appointments with a carrier
- Agency acquisition or producer transition
- Annual recertification / contract renewal
- Updates to banking, address, or authorized signers

Notes:
- Edition is from 1993 — most carriers now use proprietary
  onboarding portals; the ACORD form persists for some specialty
  and surplus lines markets
- Pairs with ACORD 201 (Producer Account Discrepancy Notice) when
  account issues arise""",
    ),

    "ACORD 201 (1993-03) Producer Account Discrepancy Notice.txt": card(
        "201", "1993-03", "Producer Account Discrepancy Notice",
        "N/A (administrative form)",
        "Producer / carrier account reconciliation",
        """Purpose:
Notice from a producer to a carrier (or vice versa) identifying a
discrepancy in producer account records — commission calculations,
premium remittance, policy fee applications, or similar accounting
issues requiring reconciliation.

Captures:
- Reference to producer account (ACORD 200 reference)
- Period covered by the discrepancy
- Specific discrepancy items:
  * Commissions claimed vs. paid
  * Premium remittance differences
  * Policy fees / surcharges
  * Endorsement adjustments
  * Cancellation refunds
- Supporting documentation references
- Producer / carrier contact
- Resolution requested
- Authorized signature

When used:
- Producer reconciliation of monthly / quarterly statements
- Disputed commission calculations
- Premium accounting differences
- Annual audits

Notes:
- Edition is from 1993 — most carriers handle account discrepancies
  through producer portals or AMS integrations now
- Pairs with ACORD 200 (Producer Account)""",
    ),

    "ACORD 210 (2016-03) Yacht Section.txt": card(
        "210", "2016-03", "Yacht Section",
        "12 months (typical, may be seasonal in northern markets)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for yacht insurance — typically applied to
larger watercraft (often 26+ feet) requiring specialty marine
underwriting beyond standard personal watercraft coverage.

Captures:
- Reference to ACORD 125 / personal lines application
- Yacht information:
  * Year, make, model, length, beam, draft
  * Hull material (fiberglass, aluminum, wood, composite)
  * Propulsion (inboard, sterndrive, sail, twin)
  * Hull / motor identification (HIN, MMSI)
  * Survey date and surveyor
  * Agreed value
- Use: pleasure, charter, racing, commercial
- Navigation area:
  * Inland, coastal, ocean
  * Specific cruising grounds
  * Hurricane plan / lay-up
- Mooring / storage:
  * Marina, mooring, dry storage, trailered
  * Hurricane plan
- Operator detail:
  * Captain (full-time, hired)
  * Owner experience, USCG license
  * Crew complement
- Coverage:
  * Hull (agreed value, deductible)
  * Liability (P&I)
  * Medical payments
  * Uninsured boater
  * On-water towing
  * Personal effects
- Loss history

When used:
- Yachts above standard personal watercraft thresholds
- Specialty marine markets
- Charter operations
- Renewal review

Notes:
- Pairs with ACORD 82 (Watercraft Application) and ACORD 282
  (Watercraft Section) for full submission package
- Survey requirements depend on vessel age and value""",
    ),

    "ACORD 211 (2016-09) Schedule of Hazards.txt": card(
        "211", "2016-09", "Schedule of Hazards",
        "Matches underlying policy",
        "Attached to new business, renewal, or audit",
        """Purpose:
Schedule of CGL classification codes and rating exposures by
location and operation. Used to capture the rating-by-class structure
of commercial general liability exposures — separate exposure bases
(payroll, gross sales, area, units) for each class code at each
location.

Captures:
- Reference to underlying CGL application
- For each location and class code:
  * Class code (ISO or carrier-specific)
  * Class description
  * Premium basis (payroll, sales, area, etc.)
  * Exposure amount
  * Rate per unit
  * Annual premium
- Sub-totals by location
- Aggregate totals

When used:
- Multi-class CGL submissions
- Multi-location commercial accounts
- Renewal audit reconciliation
- Premium audit documentation

Notes:
- Pairs with ACORD 126 (CGL Section) — 211 provides the per-class
  exposure detail that drives CGL premium calculation
- Critical for premium audit accuracy and reconciliation""",
    ),

    "ACORD 212 (2017-09) Commercial Umbrella Underlying Schedule.txt": card(
        "212", "2017-09", "Commercial Umbrella Underlying Schedule",
        "Matches underlying umbrella policy",
        "New business / renewal underwriting (commercial umbrella)",
        """Purpose:
Schedule listing all underlying primary policies that support a
commercial umbrella. Captures carriers, policy numbers, limits, and
effective dates for each underlying policy so the umbrella
underwriter can verify required limits are met and identify
coverage gaps.

Captures:
- Reference to ACORD 131 (Umbrella Section)
- For each underlying policy:
  * Coverage type (CGL, auto, employers liability, foreign liability,
    liquor, professional, marine, etc.)
  * Carrier name and NAIC
  * Policy number
  * Policy effective and expiration dates
  * Per-occurrence / per-claim limits
  * Aggregate limits (where applicable)
  * Self-insured retention or deductible
  * Whether claims-made or occurrence
  * Whether following form
- Required underlying limits for the umbrella
- Compliance check (does each underlying meet umbrella minimums?)
- Authorized signature

When used:
- Commercial umbrella new business submissions
- Renewal review when underlying carriers change
- Annual verification that underlying limits are maintained
- Claim handling when umbrella attaches

Notes:
- Pairs with ACORD 131 (Umbrella Section) — 212 is the detailed
  underlying schedule
- Failure to maintain underlying coverage at the required limits
  creates coverage gaps that the umbrella may not bridge""",
    ),

    "ACORD 225 (1998-01) Policyholder's Report.txt": card(
        "225", "1998-01", "Policyholder's Report",
        "N/A (audit document)",
        "Premium audit reporting (typically annual)",
        """Purpose:
Policyholder's self-report of audit-basis exposures (payroll, gross
sales, units) for premium audit purposes. Used to true up actual
exposures against estimated exposures for policies rated on auditable
bases — typically commercial GL, workers comp, business auto, and
package policies.

Captures:
- Insured / policy reference
- Audit period (typically 12 months matching policy term)
- For each class / exposure base:
  * Estimated exposure (per policy)
  * Actual exposure (audit period)
  * Variance
- Payroll detail (where audited):
  * Total payroll by class
  * Officer / owner exclusions or inclusions
  * Overtime treatment
- Gross sales detail (where audited):
  * Total receipts
  * Tax exclusions
- Subcontractor costs (where audited)
- Insured signature attesting to accuracy
- Producer / auditor verification

When used:
- Annual premium audit on auditable policies
- Mid-term audits triggered by significant exposure changes
- Final audit on cancelled policies

Notes:
- Edition is from 1998 — most carriers use proprietary audit forms
  or online portals now, but ACORD 225 remains a baseline standard
- Material understatement of exposures can trigger additional
  premium and possibly fraud allegations""",
    ),

    "ACORD 226 (1993-03) Statement of Premium Adjustment.txt": card(
        "226", "1993-03", "Statement of Premium Adjustment",
        "N/A (audit document)",
        "Premium audit settlement / adjustment notification",
        """Purpose:
Carrier-issued statement of premium adjustment following a premium
audit. Notifies the insured (and producer) of the audit results —
additional premium owed, refund due, or no change — and the basis
for the adjustment.

Captures:
- Insured / policy reference
- Audit period
- Original policy premium (estimated)
- Audited premium (actual)
- Premium adjustment (additional or return)
- Detail by class / exposure:
  * Estimated vs. audited exposure
  * Estimated vs. audited premium
- Reason for adjustment
- Carrier / auditor contact
- Dispute / appeal process

When used:
- Issued at completion of premium audit
- Follow-up to ACORD 225 (Policyholder's Report)
- Final audit on cancelled policies

Notes:
- Edition is from 1993 — superseded by carrier-specific notices in
  most modern audits
- Insured has appeal rights for disputed audit results; specific
  processes vary by carrier and state""",
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
