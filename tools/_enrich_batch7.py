"""Batch 7 — commercial line-of-business sections (22 forms)."""
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
    "ACORD 127 (2015-12) Business Auto Section.txt": card(
        "127", "2015-12", "Business Auto Section",
        "12 months (typical commercial term)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for commercial / business auto coverage.
Pairs with ACORD 125 (Applicant Information Section) to form a
complete commercial auto submission. Captures vehicles, drivers,
coverages, and exposures for non-trucking commercial fleets.

Captures:
- Reference to ACORD 125 (insured info, business operations)
- Business auto coverage form (BAC) selection
- Covered autos symbols (1=any, 2=owned, 7=specifically described,
  8=hired, 9=non-owned, etc.)
- Vehicle schedule reference (often ACORD 129)
- Driver schedule reference (often ACORD 163)
- Coverage limits requested:
  * Liability (BI/PD or CSL)
  * Medical Payments
  * UM/UIM (state-specific)
  * Personal Injury Protection (no-fault states)
  * Comprehensive and collision (deductibles)
  * Hired auto, non-owned auto liability
  * Towing and labor
- Garaging locations and radius of operation
- Loss history (auto-specific)
- Drive-other-car / extended named insured endorsements

When used:
- Commercial auto new business (non-trucking)
- Commercial auto renewal
- Adding business auto to a multi-line commercial submission

Notes:
- Use ACORD 132 (Truckers / Motor Carriers Section) for trucking
  operations — they need different exposure detail
- Pairs with ACORD 129 (Vehicle Schedule) and ACORD 163 (Commercial
  Auto Driver Information Schedule) for the underlying detail
- Pairs with ACORD 125 always — never submitted standalone""",
    ),

    "ACORD 128 (2015-12) Garage and Dealers Section.txt": card(
        "128", "2015-12", "Garage and Dealers Section",
        "12 months (typical commercial term)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for garage operations and auto dealers —
new and used car dealers, body shops, repair facilities, service
stations, towing operations, valet parking. Captures the unique
combined exposure of operating ON customer vehicles AND owning /
selling vehicles for inventory.

Captures:
- Reference to ACORD 125 (insured info, operations)
- Garage operation type (new dealer, used dealer, body shop,
  service, towing, valet, parking lot)
- Inventory description (number of vehicles, average value, max
  value, location)
- Garage Liability:
  * Limits (each accident / aggregate)
  * Auto medical payments
  * UM/UIM
- Garagekeepers Coverage:
  * Coverage form (Legal Liability, Direct Primary, Direct Excess)
  * Limits per vehicle / aggregate
  * Comprehensive and collision deductibles
- Dealers Open Lot (for inventory):
  * Limit per vehicle / max per location
  * Catastrophe limit (fire, hail, flood, theft)
  * Deductibles
- False Pretense coverage
- Operations radius
- Drivers / employees / volunteers
- Loss history

When used:
- Auto dealer new business
- Body shop / repair facility submissions
- Towing operator submissions
- Renewal of garage operations

Notes:
- Garagekeepers coverage form (Legal Liability vs. Direct
  Primary/Excess) is a critical coverage decision — Legal Liability
  only pays when the garage is legally liable; Direct Primary/Excess
  pays for damage to customer vehicles regardless of fault
- Pairs with ACORD 30 (Certificate of Garage Insurance) for
  third-party evidence
- Different from ACORD 127 (Business Auto) — garage policies have
  unique coverage parts that BAC doesn't model""",
    ),

    "ACORD 129 (2009-11) Vehicle Schedule.txt": card(
        "129", "2009-11", "Vehicle Schedule",
        "Matches underlying policy",
        "Attached to new business, renewal, or mid-term endorsement",
        """Purpose:
Schedule listing vehicles covered under a commercial auto policy.
Used as an attachment when there are more vehicles than the primary
section accommodates, or as the master vehicle list for fleets.

Captures:
- Reference to underlying policy / application
- For each vehicle:
  * Year, make, model, body type
  * VIN
  * Original cost / agreed value
  * Garaging address
  * Use (business, pleasure, livery, retail/service)
  * Radius (local, intermediate, long-distance)
  * Vehicle weight / GVWR
  * Coverage parts requested per vehicle (liability, comp, coll)
  * Comprehensive and collision deductibles
  * Lienholder / loss payee
  * Effective date for the vehicle's coverage

When used:
- Commercial auto with 5+ vehicles
- Trucking fleets
- Mid-term vehicle additions / deletions
- Renewal vehicle review

Notes:
- Pairs with ACORD 127 (Business Auto Section) or ACORD 132
  (Truckers Section) as the master vehicle list
- AMS-generated for large fleets; the form structure is the
  industry standard for fleet-level data""",
    ),

    "ACORD 130 (2026-01) Workers Compensation Application.txt": card(
        "130", "2026-01", "Workers Compensation Application",
        "12 months (typical; some states allow 3-year terms)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Standalone workers compensation application capturing the employer,
operations, payroll by class code, and loss history needed to quote
and issue a WC policy. Can be submitted with ACORD 125 or
standalone depending on whether the carrier writes WC alongside
other lines.

Captures:
- Producer / agency information
- Employer (named insured) name, address, FEIN
- Business description, operations, NAICS, SIC
- Years in business, number of employees
- Locations (each state / each location)
- Payroll by:
  * Class code (NCCI or state-specific)
  * Employee classification description
  * Payroll amount
  * Number of employees
- Officer / partner inclusion / exclusion elections
- Subcontractor / 1099 contractor exposure
- Prior carrier and 5-year experience modification factor
- 3-5 year loss history (paid, reserved, by year)
- Safety programs, drug testing, return-to-work
- Additional insureds, waiver of subrogation requirements
- General information (other policies, foreign operations, prior
  cancellations)

When used:
- WC new business
- WC renewal
- Audit-driven policy adjustments

Notes:
- 2026-01 edition reflects current carrier and NCCI requirements
- WC is heavily state-regulated; some states use monopolistic state
  funds (ND, OH, WA, WY) that require state-specific applications
  rather than ACORD 130
- Experience modification (mod) factor is critical — captured here
  and verified via NCCI / state rating bureau""",
    ),

    "ACORD 131 (2017-11) Umbrella Section.txt": card(
        "131", "2017-11", "Umbrella Section",
        "12 months (typical commercial term)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for commercial umbrella / excess liability
coverage. Sits above underlying CGL, business auto, employers
liability (under WC), and other liability policies. Pairs with
ACORD 125 to form a complete umbrella submission.

Captures:
- Reference to ACORD 125 (insured info, operations)
- Umbrella limit requested ($1M, $5M, $10M, higher)
- Self-insured retention (SIR) / deductible
- Underlying policies and required limits:
  * CGL (typically $1M each occurrence / $2M aggregate)
  * Auto liability (typically $1M CSL)
  * Employers liability (typically $500K/$500K/$500K)
  * Other (foreign liability, liquor, professional, etc.)
- Carrier and policy numbers for each underlying policy
- Coverage form (follow-form vs. self-contained)
- Underlying limits compliance
- Loss history (umbrella attaching, primary)
- Subsidiaries, joint ventures, additional named insureds
- Foreign operations, watercraft, aircraft, professional liability
  exposure

When used:
- Commercial umbrella new business
- Renewal review
- Adding umbrella to existing primary lines

Notes:
- Underlying limits MUST be maintained — if primary cancels, umbrella
  may drop down or void
- "Follow-form" umbrellas inherit primary coverage terms; "self-
  contained" umbrellas have their own form and may exclude what
  primary covers
- Pairs with ACORD 212 (Commercial Umbrella Underlying Schedule)
  for the detailed list of underlying policies""",
    ),

    "ACORD 132 (2015-12) Truckers - Motor Carriers Section.txt": card(
        "132", "2015-12", "Truckers / Motor Carriers Section",
        "12 months (typical commercial term)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for motor carriers / trucking operations.
Captures the unique exposure of for-hire trucking — auto liability,
motor truck cargo, trailer interchange, non-trucking liability —
that ACORD 127 (Business Auto) doesn't fully cover.

Captures:
- Reference to ACORD 125 (insured info)
- Motor carrier / authority info: MC#, DOT#, intrastate authority
- Operation type: for-hire, private, owner-operator, broker
- Commodity hauled (general freight, hazmat, household goods,
  livestock, refrigerated, etc.)
- Radius of operations (local, intermediate, long-haul)
- Power units (tractors), trailers, owner-operators
- Drivers (count, MVRs, CDL status, hours-of-service compliance)
- Coverage requested:
  * Auto liability (BIPD or CSL, typically $750K-$5M for ICC/MCS-90)
  * Motor truck cargo (limit, deductible, commodity coverage)
  * Trailer interchange / non-owned trailer
  * Physical damage (comp/coll, agreed value or ACV)
  * Non-trucking liability (bobtail) for owner-operators
  * General liability
  * Workers compensation
- Filing requirements (MCS-90, BMC-91, state filings)
- Loss history

When used:
- Trucking new business
- Owner-operator submissions
- Motor carrier renewals

Notes:
- MCS-90 endorsement is federal financial responsibility — required
  on for-hire interstate trucking and triggers minimum auto
  liability limits ($750K-$5M depending on commodity)
- Pairs with ACORD 22 (Intermodal Interchange Certificate) for
  intermodal operations and ACORD 194 (Truckers Supplement) for
  additional exposure detail""",
    ),

    "ACORD 133 (2025-05) Workers Compensation Insurance Plan – Assigned Risk Section.txt": card(
        "133", "2025-05", "Workers Compensation Insurance Plan – Assigned Risk Section",
        "12 months (per assigned risk pool rules)",
        "New business / renewal in residual market (assigned risk pool)",
        """Purpose:
Supplement to ACORD 130 used when an employer is being placed in
the residual market — the state-administered Workers Compensation
Insurance Plan for risks that voluntary markets won't write.
Captures the additional disclosures the assigned risk pool requires
to accept and assign the risk.

Captures:
- Reference to ACORD 130 (the underlying WC application)
- Reason for assigned risk submission (declined by voluntary
  carriers, prior cancellation, high mod factor, hazardous class)
- Voluntary market submission history (carriers approached,
  decline reasons)
- Specific assigned risk pool rules disclosures
- Premium financing arrangements
- Safety program commitments
- Compliance with state WC laws and assigned risk rules
- Officer / owner attestations
- Producer disclosures (commission caps in assigned risk markets)

When used:
- Submitting to NCCI's Assigned Risk Plan or state-specific plans
- Renewal of assigned risk coverage
- Transitioning from voluntary to residual market

Notes:
- Most states use NCCI's Assigned Risk Plan; some have their own
  (CA, MI, NJ, NY, others)
- Producer commissions in assigned risk markets are typically
  capped below voluntary market rates
- Pairs with ACORD 130 (Workers Compensation Application) — never
  submitted alone""",
    ),

    "ACORD 139 (2015-12) Statement - Schedule of Values.txt": card(
        "139", "2015-12", "Statement / Schedule of Values",
        "Matches underlying policy",
        "Attached to new business, renewal, or audit",
        """Purpose:
Schedule of values (SOV) listing buildings, contents, business
income, and other property values by location. Used for blanket
property programs, scheduled property programs, and large commercial
accounts where total insurable value drives rating.

Captures:
- Insured / policy reference
- For each location:
  * Address, building number / description
  * Construction type (frame, joisted masonry, non-combustible,
    masonry non-combustible, modified fire-resistive, fire-resistive)
  * Occupancy type (office, retail, manufacturing, warehouse, etc.)
  * Year built, square footage
  * Protection class (PPC), distance to fire department / hydrant
  * Building value (RC or ACV)
  * Business personal property value
  * Business income / extra expense value
  * Equipment, EDP, stock values
- Total insurable value (TIV) summary
- Coinsurance percentages
- Blanket vs. scheduled limits

When used:
- Large commercial property submissions (blanket programs)
- Annual renewal SOV updates
- Property value audits
- Mid-term acquisitions adding locations

Notes:
- Drives blanket rate calculation — TIV at each location is the
  rating exposure
- Pairs with ACORD 140 (Property Section) and ACORD 159 (Schedule
  of Property Limits) for full property submissions""",
    ),

    "ACORD 140 (2016-03) Property Section.txt": card(
        "140", "2016-03", "Property Section",
        "12 months (typical commercial term)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for commercial property coverage. Pairs
with ACORD 125 to form a complete commercial property submission.
Captures locations, building characteristics, coverage limits, and
property exposures.

Captures:
- Reference to ACORD 125 (insured info, operations)
- Coverage form requested (CP — Commercial Property): Special
  (causes-of-loss CP 10 30), Broad (CP 10 20), Basic (CP 10 10)
- Per-location detail (often via ACORD 139 SOV):
  * Address, building number
  * Construction, occupancy, protection, exposure (COPE)
  * Building value, BPP value, BI/EE value
  * Coinsurance percentage
  * Deductibles
- Coverage extensions:
  * Equipment breakdown (or referred to ACORD 155)
  * Ordinance or law
  * Spoilage
  * Crime (or referred to ACORD 141)
  * Inland marine (or referred to ACORD 152)
- Catastrophe perils: wind/hail, earthquake, flood (separate
  coverage or excluded)
- Property valuation (RC, ACV, agreed value, functional)
- Loss history (property-specific)

When used:
- Commercial property new business
- Renewal review
- Adding property to multi-line commercial submission
- Mid-term additions of locations

Notes:
- Pairs with ACORD 139 (Statement / Schedule of Values), ACORD 155
  (Equipment Breakdown), ACORD 141 (Crime), ACORD 152 (Commercial
  Inland Marine) where those exposures are present
- For BOP-eligible smaller commercial, use ACORD 160 instead""",
    ),

    "ACORD 141 (2016-03) Crime Section.txt": card(
        "141", "2016-03", "Crime Section",
        "12 months (typical commercial term)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for commercial crime coverage — employee
dishonesty, computer fraud, money / securities, forgery, funds
transfer fraud, social engineering. Pairs with ACORD 125 for a full
commercial crime submission.

Captures:
- Reference to ACORD 125 (insured info, operations)
- Crime policy form (typically ISO CR 00 21 Commercial Crime
  Coverage Form)
- Coverage parts and limits requested:
  * Employee Theft
  * Forgery or Alteration
  * Inside the Premises — Theft of Money and Securities
  * Inside the Premises — Robbery or Safe Burglary of Other Property
  * Outside the Premises
  * Computer Fraud
  * Funds Transfer Fraud
  * Money Orders and Counterfeit Money
  * Social Engineering Fraud (often sublimited)
- Deductibles per coverage part
- Number of employees, locations, ERISA fidelity bond requirement
- Cash on premises and in transit
- Internal controls (segregation of duties, dual authorization,
  audits, background checks)
- Loss history

When used:
- New business with money handling, employee theft exposure
- Renewal review of crime limits
- ERISA fidelity bond requirements (employee benefit plans)

Notes:
- Social engineering fraud is increasingly important — many policies
  sublimit it heavily
- ERISA requires fidelity bond at 10% of plan assets up to $500K
  ($1M for plans holding employer securities)
- Pairs with ACORD 140 (Property Section) where crime is part of a
  property package""",
    ),

    "ACORD 143 (2013-09) Transportation Section.txt": card(
        "143", "2013-09", "Transportation Section",
        "12 months (typical commercial term)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for transportation inland marine coverage —
motor truck cargo (carrier's own goods or for-hire cargo),
transit coverage, processing risks, shipper's interest. Distinct
from ACORD 132 (Truckers / Motor Carriers Section) which covers the
full motor carrier exposure.

Captures:
- Reference to ACORD 125 (insured info)
- Coverage type: motor truck cargo, transit (annual or trip),
  processing, shipper's interest
- Commodities transported / processed (description, value)
- Limit per conveyance / per occurrence
- Aggregate limit
- Deductible
- Routes / radius of operations
- Owned vs. hired vehicles, contracted carriers
- Refrigeration / temperature control (where applicable)
- Loading and unloading
- Storage in transit (warehouse, terminals)
- Loss history

When used:
- Commercial inland marine new business focused on transportation
- Manufacturers shipping their own goods
- Logistics / 3PL operations
- Renewal review

Notes:
- For motor carrier (for-hire trucking) operations, use ACORD 132
- Pairs with ACORD 152 (Commercial Inland Marine) for broader IM
  exposures""",
    ),

    "ACORD 144 (2013-09) Glass and Sign Section.txt": card(
        "144", "2013-09", "Glass and Sign Section",
        "12 months (typical commercial term)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for glass and sign inland marine coverage.
Covers physical damage to glass (windows, doors, mirrors, display
cases) and signs (on-premise and off-premise) on a scheduled or
blanket basis.

Captures:
- Reference to ACORD 125
- Glass coverage:
  * Per-pane limit / aggregate
  * Lettering and ornamentation
  * Boarding-up costs
  * Replacement vs. repair valuation
- Sign coverage:
  * On-premise signs (description, location, value)
  * Off-premise signs (billboards, location-specific)
  * Neon, electronic, illuminated signs (separate sublimits)
- Deductibles per coverage
- Locations covered
- Loss history (glass / sign claims)

When used:
- Retail operations with significant glass exposure
- Restaurants, dealerships, banks, jewelers
- Properties with valuable signage (digital billboards, neon, etc.)

Notes:
- Often included in BOP or commercial property as a sublimit; this
  form is for stand-alone or scheduled coverage when the BOP/CP
  sublimit is insufficient
- Pairs with ACORD 152 (Commercial Inland Marine) for broader IM
  package""",
    ),

    "ACORD 145 (2013-09) Accounts Receivable - Valuable Papers.txt": card(
        "145", "2013-09", "Accounts Receivable / Valuable Papers",
        "12 months (typical commercial term)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for accounts receivable and valuable papers
inland marine coverage. Covers the cost of reconstructing damaged or
destroyed AR records and valuable papers (contracts, manuscripts,
plans, drawings, deeds, books).

Captures:
- Reference to ACORD 125
- Accounts Receivable coverage:
  * Maximum AR balance
  * Average AR balance
  * AR aging
  * Where records are kept (on-premises, off-site, electronic)
  * Backup procedures and frequency
- Valuable Papers coverage:
  * Description of valuable papers
  * Storage (on-premises, off-site, fireproof safe)
  * Cost to reconstruct
  * Specific items (originals, masters, plates, dies)
- Limits per location and aggregate
- Deductibles
- Loss history

When used:
- Service businesses, professional offices, manufacturers
- Operations with significant credit / AR exposure
- Architects, engineers, attorneys (for plans and files)

Notes:
- Electronic data is typically covered under ACORD 148 (EDP
  Section); valuable papers focuses on hard-copy documents
- Off-site backups dramatically reduce both AR and valuable papers
  reconstruction costs""",
    ),

    "ACORD 147 (2016-03) Installation - Builders Risk Section.txt": card(
        "147", "2016-03", "Installation / Builders Risk Section",
        "Project term (3, 6, 12 months typical) or annual reporting",
        "New business / renewal (project-based)",
        """Purpose:
Line-of-business section for installation floater (covering
property of contractors during installation) and builders risk
(covering structures during construction). Inland marine coverage
specific to construction and installation exposures.

Captures:
- Reference to ACORD 125
- Coverage form: Installation Floater, Builders Risk, or both
- For Installation Floater:
  * Description of installation work
  * Maximum value at any one location
  * Maximum in transit
  * Annual receipts (volume of installation work)
- For Builders Risk:
  * Project address and description
  * Construction type, height, square footage
  * Estimated completed value
  * Projected start and completion dates
  * Existing structures (renovation vs. new construction)
  * Soft costs coverage (delay in completion)
- Coverage extensions: testing, debris removal, scaffolding,
  temporary structures, fire protection during construction
- Deductibles
- Loss history (construction-specific)

When used:
- New construction projects (commercial and residential)
- Renovation / remodeling projects
- Contractors with significant installation exposure
- Renewal of annual reporting installation policies

Notes:
- Coverage typically terminates at occupancy or completion (whichever
  is earlier); CP coverage takes over once the building is
  operational
- Soft costs (lost rents, additional financing) often need separate
  coverage""",
    ),

    "ACORD 148 (2016-03) Electronic Data Processing Section.txt": card(
        "148", "2016-03", "Electronic Data Processing Section",
        "12 months (typical commercial term)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for electronic data processing (EDP)
inland marine coverage. Covers computer hardware, software,
electronic data, and the business income loss from EDP system
breakdown — exposures that traditional commercial property doesn't
fully cover.

Captures:
- Reference to ACORD 125
- Hardware coverage:
  * Owned vs. leased equipment
  * Schedule or blanket
  * Replacement cost or ACV
  * Off-premises coverage (laptops, mobile devices)
- Software coverage:
  * Off-the-shelf vs. custom software
  * Cost to reproduce / replace
- Data coverage:
  * Backup procedures
  * Cost to recreate data
  * Transit and off-site storage
- Extra expense (continuing operations during outage)
- Business income from EDP breakdown
- Mechanical / electrical breakdown coverage (or referred to
  ACORD 155)
- Cyber exclusions and where cyber coverage applies separately

When used:
- Operations with significant computer / data exposure
- Tech companies, professional services, financial firms
- Data-heavy businesses (healthcare, legal, accounting)

Notes:
- Distinct from cyber liability — EDP covers the hardware / software /
  data themselves; cyber covers the liability and response costs
  for breaches and attacks
- Pairs with ACORD 834 (Cyber and Privacy Coverage Section) for
  cyber liability""",
    ),

    "ACORD 149 (2013-09) Dealers Section.txt": card(
        "149", "2013-09", "Dealers Section",
        "12 months (typical commercial term)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for dealers inland marine — coverage for
the inventory of jewelry dealers, equipment dealers, fine art
dealers, musical instrument dealers, and similar operations whose
"stock" is high-value movable property requiring specialized IM
coverage.

Captures:
- Reference to ACORD 125
- Type of dealer (jeweler, equipment, fine art, instruments, coins,
  stamps, antiques, etc.)
- Inventory description and average / maximum values
- Locations: retail, warehouse, off-premises, in-transit, at shows
- Security:
  * Vault, safe specifications (TL/TRTL ratings)
  * Alarm (UL grade, central station)
  * Surveillance, access control
  * Employee background checks
- Coverage parts:
  * Stock at premises
  * Stock at exhibitions / trade shows
  * In transit (carrier, armored car, mail, bonded courier)
  * Customer goods (consigned, taken in trade)
- Limits per location / per occurrence / annual aggregate
- Deductibles
- Loss history

When used:
- Jewelers Block coverage for retail jewelers
- Equipment / fine art / antique dealers
- Renewal review of inventory values and security
- New business with high-value inventory

Notes:
- Jewelers Block is a specialty coverage with its own market and
  underwriting; ACORD 149 is the standard intake form
- Security upgrades (vault grade, alarm grade, employee
  qualifications) materially affect rate and capacity""",
    ),

    "ACORD 152 (2015-06) Commercial Inland Marine Section.txt": card(
        "152", "2015-06", "Commercial Inland Marine Section",
        "12 months (typical commercial term)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
General line-of-business section for commercial inland marine
coverage. Captures IM exposures that don't fit the more specialized
sections (transportation, glass/sign, AR/valuable papers, EDP,
dealers, builders risk). Used as the catch-all IM intake.

Captures:
- Reference to ACORD 125
- IM coverage parts requested:
  * Contractors equipment floater
  * Tools floater
  * Equipment dealers / fine arts / camera (if not on ACORD 149)
  * Bailees coverage
  * Mobile equipment
  * Specialty exposures (athletic equipment, theatrical property,
    professional offices, etc.)
- Per-coverage limits and deductibles
- Schedule of equipment / property
- Locations covered, in-transit, off-premises
- Loss history

When used:
- Contractors with equipment floaters
- Mobile equipment operators
- Catch-all IM exposures not fitting specialized sections
- Renewal review

Notes:
- Use specialized sections when applicable (143 transportation, 144
  glass/sign, 145 AR/VP, 147 builders risk, 148 EDP, 149 dealers)
- Many IM coverages have their own ISO floaters; this section is the
  ACORD intake regardless of which specific floater applies""",
    ),

    "ACORD 155 (2016-09) Equipment Breakdown Section.txt": card(
        "155", "2016-09", "Equipment Breakdown Section",
        "12 months (typical commercial term)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for equipment breakdown coverage (formerly
"boiler & machinery"). Covers physical damage and resulting business
income loss from sudden mechanical / electrical breakdown of
boilers, pressure vessels, HVAC, electrical systems, production
equipment, and computers.

Captures:
- Reference to ACORD 125
- Coverage parts:
  * Direct damage (limit, deductible)
  * Business income / extra expense from breakdown
  * Spoilage (perishables affected by breakdown)
  * Service interruption (utility breakdown causing BI)
  * Production equipment (where applicable)
- Equipment schedule (boilers, vessels, refrigeration, computers,
  electrical) or blanket coverage
- Inspection requirements
- Existing inspections / certifications
- Loss history

When used:
- Manufacturing operations
- Restaurants and food service (refrigeration / freezers)
- Buildings with significant HVAC / boiler exposure
- Data-dependent operations (servers, electrical, cooling)

Notes:
- Equipment breakdown is one of the few coverages that includes
  inspection services — carriers send inspectors to check pressure
  vessels and other regulated equipment
- Pairs with ACORD 140 (Property Section) — equipment breakdown
  fills a gap that standard CP excludes (mechanical breakdown,
  artificially generated current)""",
    ),

    "ACORD 159 (2014-09) Schedule of Property Limits.txt": card(
        "159", "2014-09", "Schedule of Property Limits",
        "Matches underlying policy",
        "Attached to new business, renewal, or audit",
        """Purpose:
Continuation schedule for property limits when the property section
or SOV needs more space, or when limits need to be broken down by
sublimit / coverage extension. Captures per-location, per-coverage
limits in detail.

Captures:
- Reference to underlying policy / application
- For each location and coverage:
  * Building limit
  * BPP limit
  * BI / extra expense limit
  * Per-coverage extension limits (ordinance, debris, sign, etc.)
  * Sublimits (theft, water damage, etc.)
  * Per-occurrence vs. annual aggregate limits
- Deductibles per coverage
- Coinsurance percentages
- Special perils sublimits (earthquake, wind/hail, flood)

When used:
- Large commercial property submissions
- Blanket programs requiring per-location detail
- Sublimit-heavy policies (extensions, endorsements)
- Renewal reviews

Notes:
- Pairs with ACORD 140 (Property Section) and ACORD 139 (SOV) — 159
  fills in detail when 139 alone isn't granular enough
- Useful for verifying coinsurance compliance per location""",
    ),

    "ACORD 160 (2016-09) Business Owners Section.txt": card(
        "160", "2016-09", "Business Owners Section",
        "12 months (typical BOP term)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for Business Owners Policy (BOP) — a
package combining commercial property and general liability for
small to mid-sized businesses meeting BOP eligibility criteria.
Pairs with ACORD 125 to form a complete BOP submission.

Captures:
- Reference to ACORD 125
- BOP eligibility class (carrier-specific or ISO BOP class)
- Property:
  * Per-location detail (address, COPE, building value, BPP value)
  * Coverage form (Standard or Special)
  * BI / extra expense (typically built-in for BOP)
  * Deductibles
- Liability:
  * Each occurrence / aggregate
  * Products / completed operations
  * Personal and advertising injury
  * Medical payments
  * Hired and non-owned auto (where included)
- Optional coverages:
  * Equipment breakdown
  * Cyber / data compromise (often included or sublimit)
  * Employment practices liability (where offered)
- Loss history

When used:
- Small to mid-sized commercial submissions eligible for BOP
- Office, retail, restaurant, light manufacturing, service
- Renewal review

Notes:
- BOP eligibility varies by carrier — generally limited by class
  (some classes excluded), revenue, square footage, and exposure
  type
- For larger or non-BOP-eligible accounts, use separate ACORD 140
  (Property) and ACORD 126 (CGL)""",
    ),

    "ACORD 163 (2012-06) Commercial Auto Driver Information Schedule.txt": card(
        "163", "2012-06", "Commercial Auto Driver Information Schedule",
        "Matches underlying auto policy",
        "Attached to new business, renewal, or mid-term driver changes",
        """Purpose:
Schedule of drivers covered under a commercial / business auto
policy. Captures the personal and driving history detail needed for
underwriting and rating each driver. Used as an attachment when
ACORD 127 / 132 doesn't accommodate enough drivers.

Captures:
- Reference to underlying policy / application
- For each driver:
  * Name, DOB, gender, marital status
  * Driver's license number, state, issue date, class (CDL where
    applicable)
  * Years licensed
  * Position / job title (operator, mechanic, supervisor, etc.)
  * Hire date
  * Hours of service compliance (CDL drivers)
  * Whether driver is owner / officer / family member
  * Excluded driver status (where applicable)
- 3-5 year MVR / loss history (accidents, violations, suspensions)
- Driver training / safety program participation

When used:
- Commercial / business auto with multiple drivers
- Trucking with CDL drivers and DOT-required driver files
- Mid-term driver additions or removals
- Renewal driver review

Notes:
- For trucking operations, additional driver detail (DOT
  qualifications, hours of service) may be required beyond ACORD 163
- Pairs with ACORD 127 (Business Auto) and ACORD 132 (Truckers /
  Motor Carriers)""",
    ),

    "ACORD 175 (2016-03) Commercial Policy Change Request.txt": card(
        "175", "2016-03", "Commercial Policy Change Request",
        "N/A (existing policy)",
        "Mid-term change / endorsement (commercial)",
        """Purpose:
Mid-term change request for commercial policies — property, GL,
auto, umbrella, WC, package, BOP, specialty. Counterpart to ACORD
70 / 71 for personal lines. Captures what the insured wants changed
so the carrier can issue an endorsement.

Captures:
- Producer / agency information
- Insured name, policy number, policy type / line of business
- Effective date of change
- Description of change requested:
  * Coverage limit changes
  * Adding / removing locations or operations
  * Adding / removing vehicles, drivers, equipment
  * Adding / removing additional insureds, loss payees, mortgagees
  * Endorsement additions or deletions
  * Named insured changes
  * Premium audit-driven adjustments
  * Mid-term renewal effective date changes
- Insured signature

When used:
- Commercial mid-term changes across all lines of business
- Acquisition or divestiture of business operations
- Change in business operations triggering coverage adjustments
- Lender / contract requirement changes

Notes:
- Pairs with ACORD 70 (personal non-auto changes) and ACORD 71
  (personal auto changes) — this is the commercial equivalent
- Often pre-populated by AMS systems and signed by the insured to
  document authorization""",
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
