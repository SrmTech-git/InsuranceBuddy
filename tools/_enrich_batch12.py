"""Batch 12 — professional liability, E&O, consumer report (26 forms)."""
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
    "ACORD 801 (2002-01) Railroad Protective Liability Supplement.txt": card(
        "801", "2002-01", "Railroad Protective Liability Supplement",
        "Project term (typically duration of work near railroad)",
        "New business / project underwriting (railroad protective liability)",
        """Purpose:
Underwriting supplement for Railroad Protective Liability (RPL)
coverage — required when a contractor or other party performs work
on or near railroad property. Protects the railroad against liability
arising from the contractor's operations near tracks. Captures the
specific work, location, and railroad relationship that drive RPL
underwriting.

Captures:
- Reference to ACORD 125 / underlying CGL
- Railroad name, division, mile post location
- Project description and scope
- Distance to active rail (typically within 50 feet triggers RPL
  requirement)
- Project start and completion dates
- Contractor performing work (named insured)
- Railroad as designated insured / additional insured
- Limits required (typically $2M-$10M each occurrence)
- Permit reference (railroad work permit)
- Loss history near rail operations

When used:
- Construction near railroad tracks (utility installation,
  excavation, grading)
- Highway / bridge work crossing or paralleling rail
- Temporary work on rail property
- Required when railroad is the obligee on the project

Notes:
- RPL is mandated by railroads on virtually all near-rail work;
  the railroad specifies the form, limits, and named insured
- Distinct from CGL — RPL specifically protects the railroad,
  not the contractor""",
    ),

    "ACORD 802 (2011-09) Hotel - Motel Supplement.txt": card(
        "802", "2011-09", "Hotel / Motel Supplement",
        "12 months (typical commercial term)",
        "New business / renewal underwriting (hotel / motel exposure)",
        """Purpose:
Underwriting supplement for hotels, motels, inns, B&Bs, and
hospitality operations. Captures occupancy, amenities, food service,
liquor service, pool / spa, and event hosting exposures specific to
lodging operations.

Captures:
- Reference to ACORD 125
- Property type (hotel, motel, inn, B&B, resort, extended stay)
- Number of rooms / units, average occupancy
- Average daily rate / annual revenue
- Building characteristics (already on ACORD 140 / 160)
- Amenities:
  * Pool, spa, hot tub
  * Fitness center, sauna
  * Restaurant / bar / lounge (revenue %)
  * Catering, event spaces, banquet
  * Conference / meeting rooms
- Liquor service (% of revenue, late-night service, dram shop
  exposure)
- Food service (kitchen equipment, hood / suppression — reference
  ACORD 185)
- Guest activities (tours, transportation, recreational equipment)
- Security (staff, cameras, key cards)
- Loss history (slips/falls, food-related, liquor-related, theft,
  fire)

When used:
- Hotel / motel new business
- Renewal review of operational changes
- Acquisitions of hospitality properties

Notes:
- Pools and recreational amenities are major liability concerns —
  drowning, slip and fall claims
- Liquor service triggers dram shop liability (state-specific)""",
    ),

    "ACORD 803 (2016-03) Liquor Liability Section.txt": card(
        "803", "2016-03", "Liquor Liability Section",
        "12 months (typical commercial term)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for liquor liability (dram shop) coverage —
required by establishments serving alcoholic beverages. Covers the
unique liability exposure of selling, serving, or furnishing alcohol
to a patron who later causes injury or property damage.

Captures:
- Reference to ACORD 125 / 185 (Restaurant / Tavern Supplement)
- Type of operation (restaurant, bar, tavern, nightclub, brewery,
  package store)
- Annual liquor sales / total sales (% from alcohol)
- Hours of operation (especially late-night service)
- Service practices:
  * TIPS / responsible service training
  * ID checking procedures
  * Refusal of service policies
- Age / geographic limitations
- Entertainment (live music, DJ, dance floor — increases late-night
  liquor exposure)
- BYOB or off-premises sales
- Coverage limits (each occurrence, aggregate)
- Defense within or outside limits
- Loss history (dram shop claims)

When used:
- Restaurants and bars
- Hotels with bar / lounge
- Liquor stores (off-premises)
- Caterers serving alcohol
- Special event hosts

Notes:
- Dram shop laws are heavily state-specific — some states (Texas,
  some others) have very high statutory damages, others have caps
  or limit liability
- Pairs with ACORD 185 (Restaurant / Tavern Supplement) and ACORD
  802 (Hotel / Motel Supplement)""",
    ),

    "ACORD 807 (2016-03) Directors & Officers Liability Section.txt": card(
        "807", "2016-03", "Directors & Officers Liability Section",
        "12 months (typical, claims-made)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for Directors and Officers (D&O) liability
coverage — protects company directors and officers from personal
liability arising from their decisions in those capacities. Coverage
parts typically include Side A (individual D&O), Side B
(reimbursement to corporation), and Side C (entity coverage for
public companies).

Captures:
- Reference to ACORD 125
- Entity type (public, private, non-profit)
- Industry / business operations
- Annual revenue, market cap (public)
- Number of directors and officers
- Subsidiaries / joint ventures
- Foreign operations
- Recent transactions (M&A, IPO, secondary offerings)
- Litigation history (current, threatened, recent settled)
- Regulatory investigations / enforcement actions
- Coverage parts requested:
  * Side A (non-indemnifiable D&O)
  * Side B (corporate reimbursement)
  * Side C (entity coverage for securities claims, public)
  * EPL (employment practices) — often packaged with D&O
- Limits and self-insured retentions
- Claims-made retroactive date
- Loss history (D&O specific)

When used:
- Public company D&O
- Private company D&O
- Non-profit D&O
- D&O placement at IPO
- Renewal review

Notes:
- D&O is virtually always claims-made; retroactive date and tail
  coverage matter
- Side A coverage (non-indemnifiable) is critical for individual
  directors when the company can't or won't indemnify""",
    ),

    "ACORD 808 (2010-08) P&C Agency Appointment Form.txt": card(
        "808", "2010-08", "P&C Agency Appointment Form",
        "N/A (administrative form)",
        "Producer / agency appointment with carrier",
        """Purpose:
Carrier-issued agency appointment form establishing a property and
casualty agency's authority to write business with the carrier.
Captures the agency's licensing, authorities, and contractual
arrangement with the carrier.

Captures:
- Agency name, address, FEIN
- Producer / individual agents to be appointed
- Lines of authority (P&C, surplus lines, etc.)
- Geographic territory
- Commission structure
- Production goals / minimums
- Authorized signatories
- E&O insurance details
- Compliance certifications

When used:
- New agency appointments with a carrier
- Adding individual agents to an existing agency appointment
- Renewal / recertification

Notes:
- Pairs with ACORD 200 (Producer Account)
- State-specific appointment filings may also be required""",
    ),

    "ACORD 810 (2014-12) Business Income - Extra Expense - Rental Value Supplement to Property Section.txt": card(
        "810", "2014-12", "Business Income / Extra Expense / Rental Value Supplement to Property Section",
        "12 months (typical, matches underlying property)",
        "New business / renewal underwriting (BI / EE / RV detail)",
        """Purpose:
Underwriting supplement for Business Income (BI), Extra Expense
(EE), and Rental Value (RV) coverages on commercial property
policies. Captures the financial detail needed to set BI / EE / RV
limits — historical revenue, expense structure, dependencies, and
recovery time after a loss.

Captures:
- Reference to ACORD 125 / 140
- BI worksheet:
  * Annual gross sales / revenue
  * Cost of goods sold
  * Continuing expenses during shutdown
  * Non-continuing expenses
  * Net income
  * Period of restoration estimate (recovery time)
- BI limit selected (12-month, 18-month, custom)
- Coinsurance election (50%, 80%, 90%, 100%, agreed value)
- Extra Expense:
  * Costs to continue operations during recovery
  * Temporary location costs
  * Expedited repair / replacement
- Rental Value (for landlords):
  * Annual rental income
  * Loss of rents period
- Dependent properties (suppliers, customers, attraction
  properties)
- Loss history

When used:
- Commercial property submissions with significant BI exposure
- Manufacturers, retailers, service businesses
- Multi-tenant landlords
- Renewal review of BI limits

Notes:
- BI is one of the most under-purchased coverages — actual recovery
  often exceeds purchased limits because business owners
  underestimate restoration time
- Pairs with ACORD 140 (Property Section) and ACORD 811 (Value
  Reporting Information Supplement)""",
    ),

    "ACORD 811 (2014-12) Value Reporting Information Supplement to Property Section.txt": card(
        "811", "2014-12", "Value Reporting Information Supplement to Property Section",
        "12 months (typical, with monthly / quarterly reporting)",
        "Reporting form policy underwriting / monthly value reports",
        """Purpose:
Underwriting and reporting supplement for value-reporting commercial
property policies — typically used by businesses with fluctuating
inventory values (retail, manufacturing, distribution) where flat
limits don't fit. Captures the reporting structure and historical
values needed to set reporting policy parameters.

Captures:
- Reference to ACORD 140 (Property Section)
- Reporting form selected:
  * Monthly value reporting
  * Quarterly value reporting
  * Annual value reporting
- Maximum (or "limit of insurance") values per location
- Premium calculation (deposit premium based on average value;
  audit at end of term)
- Historical inventory / value patterns:
  * Seasonal peaks and valleys
  * Year-over-year growth trends
- Locations covered
- Reporting forms / process

When used:
- Retailers with seasonal inventory swings (toys, holiday goods)
- Manufacturers with WIP and finished goods variability
- Distributors and wholesalers
- Multi-location operations with shifting inventory

Notes:
- Reporting forms can save premium for businesses with major
  seasonal swings vs. flat limits
- Failure to report timely can trigger reduced coverage (penalty
  clause)
- Pairs with ACORD 140 and ACORD 810""",
    ),

    "ACORD 812 (2006-02) Agency Questionnaire.txt": card(
        "812", "2006-02", "Agency Questionnaire",
        "N/A (administrative questionnaire)",
        "Carrier appointment / due diligence",
        """Purpose:
Detailed questionnaire issued by a carrier to an agency as part of
the appointment due-diligence process. Captures the agency's
operations, ownership, financial condition, and compliance posture
beyond the basic ACORD 200 / 808 appointment forms.

Captures:
- Agency ownership structure (principals, % ownership)
- Years in business
- Number of employees and producers
- Specialties / classes of business written
- Carriers represented (current and recent)
- E&O insurance details (carrier, limits, any claims)
- Financial information (revenue, profitability, premium volume)
- Sub-producers / downline producers
- Office locations
- Trust account / premium handling procedures
- Compliance with state regulations
- Disciplinary / regulatory history
- References

When used:
- New agency appointments
- Carrier due diligence on existing appointments
- Annual recertification with carriers
- Acquisition due diligence on agency targets

Notes:
- Pairs with ACORD 200 (Producer Account) and ACORD 808 (P&C
  Agency Appointment Form)
- Edition is from 2006 — many carriers have proprietary
  questionnaires now""",
    ),

    "ACORD 813 (2025-06) Request for Proof of Property Insurance.txt": card(
        "813", "2025-06", "Request for Proof of Property Insurance",
        "N/A (administrative request)",
        "Property insurance proof request",
        """Purpose:
Form used to request proof of property insurance from an insured
or producer — typically by a mortgagee, lessor, or contracting
party who needs evidence of coverage. Captures what documentation
the requester needs and where to send it.

Captures:
- Requester name, contact, role (mortgagee, lessor, vendor)
- Insured / property reference
- Property location
- Loan / lease / contract reference
- Type of proof requested:
  * ACORD 24 (Certificate of Property Insurance)
  * ACORD 27 / 28 (Evidence of Property Insurance)
  * ACORD 29 (Evidence of Flood Insurance)
- Specific coverage requirements (limits, deductibles, mortgagee
  clause, additional insured)
- Where / how to deliver the proof
- Deadline for delivery

When used:
- Mortgagees requesting evidence at loan inception or renewal
- Lessors requiring proof of tenant insurance
- Contracting parties requesting insurance evidence
- Loan servicing transfers requiring re-issuance to new servicer

Notes:
- Initiates issuance of ACORD 24, 27, 28, or 29 depending on the
  type of proof required""",
    ),

    "ACORD 815 (2009-02) International Liability Exposure Supplement.txt": card(
        "815", "2009-02", "International Liability Exposure Supplement",
        "12 months (typical commercial term)",
        "New business / renewal underwriting (international liability)",
        """Purpose:
Underwriting supplement for businesses with international liability
exposure — foreign operations, foreign sales, international travel
of employees, products distributed abroad. Captures geographic
distribution and exposure detail that drives international liability
and foreign voluntary workers compensation rating.

Captures:
- Reference to ACORD 125 / 126
- Foreign operations:
  * Countries with offices / facilities
  * Number of employees abroad (US nationals, third country
    nationals, local hires)
  * Business activities in each country
- Foreign sales / exports:
  * Countries shipped to
  * Annual export sales by region
  * Products exported
- Employee international travel:
  * Frequency, destinations
  * Business purpose
- Coverage requested:
  * Foreign liability (CGL extended overseas)
  * Foreign voluntary WC
  * Defense base act (where applicable)
  * Kidnap and ransom
  * Political risk
- Loss history (international claims)

When used:
- Domestic businesses with foreign sales / operations
- Multinational enterprises
- Renewal review of international footprint

Notes:
- Pairs with ACORD 816 (International Property Exposure Supplement)
- Foreign Voluntary WC is critical — domestic WC typically doesn't
  cover injuries abroad""",
    ),

    "ACORD 816 (2005-06) International Property Exposure Supplement.txt": card(
        "816", "2005-06", "International Property Exposure Supplement",
        "12 months (typical commercial term)",
        "New business / renewal underwriting (international property)",
        """Purpose:
Underwriting supplement for international property exposures —
foreign-located property, property in transit internationally, and
property of US-based businesses operating abroad. Captures
locations, values, and protection details for international
property risk.

Captures:
- Reference to ACORD 125 / 140
- Foreign property locations:
  * Address / city / country
  * Type (office, manufacturing, warehouse, retail)
  * Building value, BPP value, BI value
  * Construction, occupancy, protection
- Local protection class (varies dramatically by country)
- Catastrophe exposure (earthquake, typhoon, political risk)
- Local insurance requirements / Admitted vs. non-admitted coverage
- Master / DIC structure (Difference in Conditions)
- Cargo in transit internationally
- Loss history

When used:
- Multinational property programs
- Foreign subsidiary operations
- International expansion underwriting

Notes:
- Many countries require admitted (locally licensed) insurance,
  with US program providing DIC / DIL coverage on top
- Pairs with ACORD 815 (International Liability Exposure)""",
    ),

    "ACORD 821 (2015-10) Producer Information Form (PIF).txt": card(
        "821", "2015-10", "Producer Information Form (PIF)",
        "N/A (administrative form)",
        "Producer onboarding / appointment maintenance",
        """Purpose:
Producer Information Form used to capture and maintain individual
producer information for carrier appointments — the agent or broker
acting under an agency contract. Pairs with ACORD 808 (P&C Agency
Appointment Form) which appoints the agency itself; PIF maintains
the individual producers under that agency.

Captures:
- Producer name, address, contact
- National Producer Number (NPN)
- State licenses (state, license number, lines of authority,
  expiration)
- Continuing education compliance
- Date of birth (for license verification)
- Employment history with insurance industry
- Disciplinary / regulatory history
- E&O coverage details

When used:
- Adding individual producers to an agency appointment
- Annual license verification
- Producer transitions between agencies

Notes:
- NPN is a unique identifier maintained by NIPR for cross-state
  producer tracking
- Pairs with ACORD 808 (Agency Appointment) and ACORD 200 (Producer
  Account)""",
    ),

    "ACORD 822 (2009-07) Driver Work - School Address Information Supplement.txt": card(
        "822", "2009-07", "Driver Work / School Address Information Supplement",
        "Matches underlying auto policy",
        "New business / renewal underwriting (driver garaging)",
        """Purpose:
Supplement capturing driver work and school addresses for personal
auto underwriting — particularly relevant for college students
attending out-of-state schools, employees with long commutes, and
households where vehicles are garaged at non-residence addresses
during the day or workweek.

Captures:
- Reference to underlying auto policy
- For each driver:
  * Home / residence address
  * Work address (employer, location)
  * School address (where applicable, for student drivers)
  * Days / hours per week at each location
  * Vehicle assigned / driven to each location
  * Out-of-state college status
  * Garaging at work / school (overnight, weekday, weekend)

When used:
- Personal auto with college students attending out-of-state
- Long-distance commuters
- Employees garaging vehicles at work
- Mid-term driver / address changes

Notes:
- Garaging address can affect rates substantially — territory
  rating uses primary garaging address
- Out-of-state college student status requires specific carrier
  endorsement in many states""",
    ),

    "ACORD 823 (2015-12) Additional Premises Information Schedule.txt": card(
        "823", "2015-12", "Additional Premises Information Schedule",
        "Matches underlying policy",
        "Attached to new business / renewal / mid-term change",
        """Purpose:
Schedule capturing additional commercial premises beyond what the
primary application accommodates. Used for multi-location operations
where ACORD 125 / 140 doesn't have space for all locations, or for
adding premises mid-term.

Captures:
- Reference to underlying commercial application
- For each additional premises:
  * Address
  * Building number / suite / unit
  * Construction (COPE: construction, occupancy, protection,
    exposure)
  * Year built, square footage
  * Building value, BPP value, BI value
  * Coverage form
  * Deductibles
  * Local protection (FD, hydrants, alarms, sprinklers)
  * Mortgagee / additional interest

When used:
- Multi-location commercial property submissions
- Mid-term acquisitions adding premises
- Lease additions (new tenant locations)

Notes:
- Pairs with ACORD 140 (Property Section) and ACORD 139 (SOV)""",
    ),

    "ACORD 825 (2016-05) Professional - Specialty Insurance Application – For Use in Management, Executive & Professional Lines Applicant Section.txt": card(
        "825", "2016-05", "Professional / Specialty Insurance Application – For Use in Management, Executive & Professional Lines Applicant Section",
        "12 months (typical, claims-made for most lines)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Master applicant information section for professional and specialty
lines submissions — D&O, EPL, fiduciary, employed lawyers, miscellaneous
professional, errors and omissions. Counterpart to ACORD 125 for
management / executive / professional lines coverage rather than
standard commercial P&C.

Captures:
- Producer / agency information
- Applicant entity name, FEIN, state of incorporation
- Entity type (public, private, non-profit, governmental, mutual)
- Industry / SIC / NAICS
- Annual revenue / total assets / market cap (public)
- Number of employees, directors, officers
- Subsidiaries and JVs
- Recent corporate transactions
- Foreign operations
- Stock ownership structure (institutional, insider, public float)
- Recent litigation, regulatory, or enforcement actions
- Existing coverages (D&O, EPL, fiduciary, E&O)
- Coverage requested (with cross-reference to specific section)
- Loss history (claims, regulatory matters, complaints)

When used:
- D&O submissions (pairs with ACORD 807)
- Employment Practices Liability submissions (pairs with ACORD 827)
- Fiduciary Liability (pairs with ACORD 828)
- Professional / specialty E&O (pairs with ACORD 832, 833, 838)
- Cyber and privacy (pairs with ACORD 834)

Notes:
- Distinct from ACORD 125 — captures the executive-line-specific
  exposures (corporate governance, financial structure, public
  filings) that traditional commercial submissions don't""",
    ),

    "ACORD 827 (2016-03) Employment Practices Liability Insurance Section.txt": card(
        "827", "2016-03", "Employment Practices Liability Insurance Section",
        "12 months (typical, claims-made)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for Employment Practices Liability (EPL)
coverage — protects employers from claims by employees, former
employees, and applicants for discrimination, harassment, wrongful
termination, retaliation, and related employment claims.

Captures:
- Reference to ACORD 825
- Employer information (revenue, # employees by location)
- HR practices:
  * Written employee handbook
  * Anti-harassment / discrimination training
  * Performance review process
  * Termination procedures
  * Background check practices
- Employment claims history (claims, complaints, EEOC charges)
- Recent layoffs / RIFs
- Class action exposure
- Coverage parts:
  * Discrimination
  * Harassment (sexual and otherwise)
  * Wrongful termination
  * Retaliation
  * Wage and hour (often sublimited or excluded)
  * Third-party liability (EPL extended to vendors, customers)
- Limits and SIR / deductible
- Defense provisions (in or outside limit)
- Claims-made retroactive date

When used:
- All commercial employers
- Public and private companies
- Non-profits and governmental entities
- Renewal review

Notes:
- Wage and hour claims (FLSA, state wage laws) often sublimited or
  excluded; separate wage and hour coverage may be needed
- Often packaged with D&O for private and non-profit accounts""",
    ),

    "ACORD 828 (2016-03) Fiduciary Liability Coverage Section.txt": card(
        "828", "2016-03", "Fiduciary Liability Coverage Section",
        "12 months (typical, claims-made)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for Fiduciary Liability coverage —
protects employers, plan sponsors, and individual fiduciaries from
liability arising from breach of ERISA fiduciary duties on employee
benefit plans (401(k), pension, health, welfare plans).

Captures:
- Reference to ACORD 825
- Plans sponsored:
  * Type (401(k), pension, defined benefit, defined contribution,
    health & welfare, NQDC)
  * Number of plans
  * Plan assets per plan
  * Number of participants per plan
  * Plan administrator
- Plan investments:
  * Investment options
  * Use of investment advisors
  * Company stock in plan (concentration risk)
- Plan governance:
  * Plan committees
  * Investment policy statements
  * Fiduciary training
- Recent plan changes (mergers, terminations, restatements)
- Claims history (fiduciary claims, DOL investigations,
  participant lawsuits)
- Coverage limits, SIR, defense provisions
- Claims-made retroactive date

When used:
- Employers with employee benefit plans subject to ERISA
- Multi-employer plan sponsors
- Plan trustees and committees
- Renewal review

Notes:
- Distinct from ERISA fidelity bond (ACORD 503 type) — fidelity
  covers theft / misappropriation of plan assets; fiduciary covers
  liability for fiduciary breaches
- ERISA fiduciary duties include duty of loyalty, prudence, plan
  document compliance, and reasonable expense management""",
    ),

    "ACORD 829 (2009-05) Forms and Endorsements Schedule.txt": card(
        "829", "2009-05", "Forms and Endorsements Schedule",
        "Matches underlying policy",
        "Documentation of policy forms and endorsements",
        """Purpose:
Schedule listing all forms and endorsements attached to a commercial
insurance policy. Provides a roadmap to the policy's actual coverage
structure — base form, mandatory endorsements, optional endorsements,
state-specific amendatory endorsements.

Captures:
- Reference to underlying policy
- For each form / endorsement attached:
  * Form number (ISO, AAIS, carrier-proprietary)
  * Form title / description
  * Edition date
  * Type (base coverage form, declaration page, exclusion,
    enhancement, state amendatory)
  * Effective date
  * Reason for inclusion (mandatory, optional, state-required)

When used:
- Policy issuance documentation
- Renewal review of forms attached
- Coverage analysis after a loss
- Carrier transitions (matching forms across markets)

Notes:
- Critical document for understanding actual coverage — the named
  insured agreement is just the start; endorsements modify almost
  every aspect of coverage
- ISO, AAIS, and carrier-proprietary forms each have their own
  numbering conventions""",
    ),

    "ACORD 830 (2026-03) Property Insurance Card.txt": card(
        "830", "2026-03", "Property Insurance Card",
        "Matches underlying property policy",
        "Issued at policy inception, renewal, or mid-term changes affecting evidence",
        """Purpose:
Compact wallet-sized card or printable summary providing quick
evidence of property insurance — analog to the auto ID card
(ACORD 50) but for property coverage. Used for situations where
abbreviated proof of property insurance is needed without issuing
a full ACORD 24 / 27 / 28.

Captures:
- Insurer name and contact
- Policy number
- Insured name
- Property location
- Policy effective and expiration dates
- Coverage summary (limits, type)
- Producer / agency contact
- Claims reporting information

When used:
- Quick on-property reference for the insured
- Permit applications requiring proof of property coverage
- Light-touch evidence requirements
- Insured's records

Notes:
- 2026-03 edition reflects current standardized format
- Less detailed than ACORD 24 / 27 / 28 — intended for the
  insured's reference, not third-party mortgagee or lender
  evidence""",
    ),

    "ACORD 831 (2019-09) Professional - Specialty Insurance Notice of Incident - Claim.txt": card(
        "831", "2019-09", "Professional / Specialty Insurance Notice of Incident / Claim",
        "N/A (claim notification)",
        "N/A (claim / incident notification)",
        """Purpose:
First Notice of Loss / Incident form for professional and specialty
lines policies — D&O, E&O, EPL, fiduciary, cyber, professional
liability. Captures incident or formal claim details on claims-made
policies, where timely notice during the policy period is a
coverage condition.

Captures:
- Producer / agency information
- Insured name, policy number
- Notice type:
  * Notice of incident (potential claim, no demand yet)
  * Notice of claim (formal demand, suit, regulatory action)
- Date of incident vs. date insured first became aware
- Date insured was first contacted by claimant / regulator
- Description of incident or claim:
  * For E&O / professional: alleged error, omission, or wrongful act
  * For D&O: alleged breach of duty, mismanagement
  * For EPL: alleged employment practice violation
  * For cyber: nature of breach, data affected
- Claimant information (claimant, attorney, regulator)
- Demand amount or alleged damages
- Authorities contacted
- Witnesses
- Insured's initial response

When used:
- All claims-made specialty lines (D&O, EPL, fiduciary, cyber, E&O)
- Notice of circumstances that could become claims
- Pre-suit demand letters
- Regulatory investigations / enforcement actions

Notes:
- Claims-made policies require notice WITHIN the policy period —
  late notice is the leading cause of coverage denial
- "Notice of incident" path preserves coverage even before a
  formal claim is made
- Pairs with ACORD 825 (and the line-specific sections 807, 827,
  828, 832, 833, 834, 838)""",
    ),

    "ACORD 832 (2016-03) Miscellaneous E&O Section.txt": card(
        "832", "2016-03", "Miscellaneous E&O Section",
        "12 months (typical, claims-made)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Generic professional / errors and omissions section for professions
without dedicated forms — consultants, real estate professionals,
property managers, insurance agents (where applicable), various
service professionals. Captures profession-specific exposures
modularly.

Captures:
- Reference to ACORD 825
- Profession / services performed
- Annual revenue and number of professionals
- Years in practice
- Services performed in detail (descriptions, % of revenue)
- Client mix and industries served
- Geographic scope
- Claims-made retroactive date and tail provisions
- Coverage limits and deductible / SIR
- Defense within or outside limits
- Subcontractor / independent contractor use
- Engagement letter / contract practices
- Quality control / peer review
- Loss history (E&O claims, regulatory complaints)

When used:
- Generic E&O for professions without dedicated forms
- Hybrid service professions (consultants, advisors)
- Renewal review

Notes:
- Specific professions have dedicated forms (833 lawyers, 838
  accountants, 196 medical, etc.) — use those when available
- Pairs with ACORD 187 (Professional Liability Supplement) for
  detailed risk profile""",
    ),

    "ACORD 833 (2014-12) Lawyers Professional Liability Section.txt": card(
        "833", "2014-12", "Lawyers Professional Liability Section",
        "12 months (typical, claims-made)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for Lawyers Professional Liability (LPL)
coverage — protects attorneys, law firms, and legal staff from
malpractice claims arising from legal services. Captures the
practice-specific detail driving LPL underwriting.

Captures:
- Reference to ACORD 825
- Firm structure (solo, partnership, PLLC, professional corporation)
- Number of attorneys (partners, associates, of counsel,
  contractors)
- Bar admission states
- Years in practice
- Revenue
- Practice areas (% of revenue):
  * Corporate / transactional
  * Litigation / trial work
  * Real estate
  * Wills, trusts, estates
  * Tax
  * IP
  * Securities
  * Personal injury (plaintiff or defense)
  * Family law
  * Criminal defense
  * Other specialties
- High-risk practice areas (often subject to surcharge or exclusion):
  * Securities
  * Patent
  * Class actions
  * Foreign / international
- Client matter management:
  * Conflict checks
  * Engagement letters
  * Statute of limitations docketing
  * Trust account procedures
- Bar association disciplinary / grievance history
- Claims history (open, closed, reserves)
- Claims-made retroactive date and tail provisions

When used:
- Solo practitioner LPL
- Firm LPL submissions
- Renewal review
- New attorneys joining a firm

Notes:
- LPL is heavily state-specific — bar association requirements,
  disciplinary procedures, and minimum coverage rules vary
- Tail / Extended Reporting Period at policy expiration is
  critical for retiring attorneys""",
    ),

    "ACORD 834 (2014-12) Cyber and Privacy Coverage Section.txt": card(
        "834", "2014-12", "Cyber and Privacy Coverage Section",
        "12 months (typical, claims-made for liability components)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for Cyber Liability and Privacy coverage —
protects organizations from data breaches, network security
failures, privacy violations, ransomware, and related cyber
incidents. Captures both first-party (insured's own losses) and
third-party (liability to affected parties) cyber exposures.

Captures:
- Reference to ACORD 825
- Operations and data exposure:
  * Number of records (PII, PHI, PCI)
  * Type of data held (customer, employee, financial, health,
    payment card)
  * Use of cloud services / SaaS providers
  * Outsourced IT / managed service providers
  * Use of vendors with data access
- Security posture:
  * Multi-factor authentication
  * Endpoint protection
  * Email security / phishing protection
  * Encryption (at rest, in transit)
  * Backup procedures and offline backups
  * Incident response plan
  * Employee training
- Compliance frameworks (PCI, HIPAA, SOC 2, ISO 27001, NIST)
- Coverage parts:
  * Network Security Liability (third-party)
  * Privacy Liability (third-party)
  * Regulatory Defense and Penalties
  * Breach Response Costs (notification, credit monitoring,
    forensics, PR)
  * Network Business Interruption (first-party)
  * Cyber Extortion / Ransomware
  * Data Restoration
  * Social Engineering / Funds Transfer Fraud
  * Reputational Harm
- Limits, sublimits, retention
- Claims-made retroactive date for liability components
- Loss history (incidents, ransomware events, regulatory inquiries)

When used:
- Most commercial accounts (cyber is now near-universal exposure)
- Healthcare, financial services, retail (high-data industries)
- Renewal review (rates moving rapidly with the threat landscape)

Notes:
- Cyber rates have changed dramatically over recent years; carrier
  appetite tightened then loosened with market cycles
- Sublimits often apply to ransomware, social engineering, and
  some other coverage parts
- Pairs with ACORD 180 (Tech E&O) for tech service operations""",
    ),

    "ACORD 838 (2013-12) Accountants Professional Liability Section.txt": card(
        "838", "2013-12", "Accountants Professional Liability Section",
        "12 months (typical, claims-made)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for Accountants Professional Liability —
protects CPAs, accounting firms, and accounting staff from
malpractice claims arising from accounting, tax, audit, and
advisory services.

Captures:
- Reference to ACORD 825
- Firm structure
- Number of professionals (CPAs, EAs, staff)
- State licensing
- Years in practice
- Revenue
- Service mix (% of revenue):
  * Audit / attest (highest risk)
  * Tax preparation and planning
  * Bookkeeping / write-up
  * Consulting / advisory
  * Personal financial planning
  * Forensic / litigation support
  * Business valuation
- Audit clients:
  * Public companies (SEC registrants — typically excluded or
    carefully underwritten)
  * Non-profits (single audits / Yellow Book)
  * Government entities
  * Privately held companies
  * Sizes (revenue ranges)
- Tax practice:
  * Individual vs. business tax returns
  * IRS audit representation
  * High-risk areas (offshore, complex partnerships, R&D credits)
- Quality control:
  * Peer review compliance
  * Engagement letters
  * Documentation standards
- Claims history
- Claims-made retroactive date

When used:
- CPA firm new business
- Renewal review
- Firm transitions (mergers, splits)

Notes:
- Audit work is the highest-risk service line — many carriers
  surcharge or exclude SEC audit work
- Peer review compliance (AICPA / state) is critical for
  underwriting""",
    ),

    "ACORD 876 (2015-10) Background Check Authorization.txt": card(
        "876", "2015-10", "Background Check Authorization",
        "N/A (consent document)",
        "Underwriting / employment / claim investigation consent",
        """Purpose:
Insured's signed authorization for the insurer (or its agents) to
conduct a background check — credit report, criminal history,
motor vehicle records, employment verification, prior insurance
history. Required under federal Fair Credit Reporting Act (FCRA)
and similar state laws before consumer reports can be obtained.

Captures:
- Insured / applicant name, DOB, SSN
- Address history
- Authorization for specific report types:
  * Credit report (consumer or specialty insurance score)
  * Criminal background check
  * Motor vehicle records
  * Employment verification
  * Prior insurance loss history (CLUE, MIB)
- Purpose of the report (underwriting, claim investigation,
  appointment due diligence)
- Insured signature with date
- Witness or notary (where required)
- FCRA disclosures (rights to copy of report, dispute process)

When used:
- Personal auto / homeowner underwriting (credit-based insurance
  scoring)
- Workers compensation underwriting (some carriers)
- Producer appointment due diligence
- Claim investigation
- Bond underwriting

Notes:
- Required under FCRA before pulling consumer reports
- Pairs with ACORD 877 (Disclosure of Intent to Obtain Consumer
  Report) which is the FCRA disclosure""",
    ),

    "ACORD 877 (2015-10) Disclosure of Intent to Obtain Consumer Report or Investigative Consumer Report (except California).txt": card(
        "877", "2015-10", "Disclosure of Intent to Obtain Consumer Report or Investigative Consumer Report (except California)",
        "N/A (disclosure document)",
        "FCRA-required disclosure prior to obtaining consumer reports",
        """Purpose:
Federally required disclosure under the Fair Credit Reporting Act
(FCRA) informing the consumer that the insurer intends to obtain a
consumer report or investigative consumer report. Must be provided
before the report is obtained. Specifically excludes California,
which has its own enhanced disclosure requirements (ICRAA).

Captures:
- Consumer (insured / applicant) name and contact
- Disclosure that a consumer report and/or investigative consumer
  report will be obtained
- Purpose of the report (underwriting, employment, etc.)
- Consumer's rights under FCRA:
  * Right to request additional information about the
    investigative report
  * Right to a free copy if adverse action is taken based on the
    report
  * Right to dispute inaccurate information
- Disclosure of consumer reporting agency (where known)
- Effective date

When used:
- Personal lines underwriting using credit-based insurance scoring
- Pre-employment screening (where insurance is involved)
- Claim investigation involving consumer reports
- New producer appointment due diligence

Notes:
- California has separate ICRAA disclosure requirements; this form
  applies in all other states
- Pairs with ACORD 876 (Background Check Authorization) — disclosure
  precedes authorization
- Adverse action notices have separate requirements when reports
  result in unfavorable underwriting decisions""",
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
