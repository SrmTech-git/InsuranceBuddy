"""Batch 6 — personal lines applications and supplements (21 forms)."""
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
    "ACORD 70 (2015-09) Personal Policy Change Request (Except Auto).txt": card(
        "70", "2015-09", "Personal Policy Change Request (Except Auto)",
        "N/A (existing policy)",
        "Mid-term change / endorsement (personal lines, except auto)",
        """Purpose:
Mid-term change request for personal lines policies OTHER than
auto — homeowners, dwelling fire, personal umbrella, watercraft,
inland marine. Captures what the insured wants to change so the
carrier can issue an endorsement. Auto changes use ACORD 71.

Captures:
- Producer / agency information
- Insured name, policy number, policy type
- Effective date of change
- Description of change requested:
  * Coverage limit changes (Coverage A increase, deductible change)
  * Add / remove additional interests (mortgagees, loss payees)
  * Property updates (renovations, new outbuildings, alarms)
  * Location changes
  * Endorsement additions (water backup, scheduled property,
    identity theft)
- Insured signature

When used:
- Insured-initiated mid-term changes on HO, DF, umbrella,
  watercraft, IM
- Annual review-driven endorsements
- Lender/mortgagee requirement changes triggering policy edits

Notes:
- Pairs with ACORD 71 (Personal Auto Policy Change Request) — use
  the auto form for auto-specific changes
- Some carriers accept oral or AMS-driven change requests instead;
  ACORD 70 documents the change request formally for the file""",
    ),

    "ACORD 71 (2016-08) Personal Auto Policy Change Request.txt": card(
        "71", "2016-08", "Personal Auto Policy Change Request",
        "N/A (existing policy)",
        "Mid-term change / endorsement (personal auto)",
        """Purpose:
Mid-term change request specifically for personal auto policies.
Captures vehicle, driver, and coverage changes the insured wants
applied to their auto policy.

Captures:
- Producer / agency information
- Insured name, policy number
- Effective date of change
- Vehicle changes (add / delete / replace):
  * Year, make, model, VIN
  * Annual mileage, garaging address, use
  * Lienholder / loss payee
- Driver changes (add / delete):
  * Name, DOB, license number, relationship
  * Driver training, good student, defensive driving credits
- Coverage changes:
  * Liability limits (BI, PD)
  * UM/UIM / med pay / PIP
  * Comp / collision deductibles
  * Towing, rental, gap
- Insured signature

When used:
- Adding or removing vehicles
- Adding or removing drivers
- Changing coverage limits or deductibles
- Garaging address changes
- Lienholder updates after vehicle financing changes

Notes:
- Pairs with ACORD 70 (non-auto personal lines changes)
- ID card (ACORD 50) reissued automatically when vehicle or
  effective dates change""",
    ),

    "ACORD 72 (2009-10) Mobile Home Supplement.txt": card(
        "72", "2009-10", "Mobile Home Supplement",
        "6 or 12 months (matches underlying policy)",
        "New business / renewal underwriting (supplement to mobile home application)",
        """Purpose:
Underwriting supplement specific to mobile / manufactured homes.
Captures the structural, foundation, and tie-down characteristics
that distinguish mobile homes from conventional dwellings and drive
their unique exposure profile.

Captures:
- Insured / property location
- Mobile home identification: make, model, year, serial / HUD number
- Dimensions (length, width, square footage)
- Single-wide vs. double-wide vs. triple-wide
- Foundation type (permanent, pier, slab, basement)
- Tie-down / anchoring system
- Skirting type and condition
- Park name (if in mobile home park) or owned land
- Distance to fire department, hydrant
- Roof type and age
- Heating, plumbing, electrical
- Updates and improvements
- Other dwellings on the same lot

When used:
- New mobile / manufactured home business
- Renewal review
- Coverage moves between policy forms (DP-1 to DP-3, etc.)
- Pairs with ACORD 85 (Mobile Home Application)

Notes:
- Mobile home rates and underwriting differ substantially from
  conventional homes — wind / tie-down / age factors matter heavily
- Pre-1976 mobile homes (pre-HUD code) face very different
  underwriting than post-1976 manufactured homes""",
    ),

    "ACORD 73 (2009-07) Solid Fuel Questionnaire – Supplement to Residential Section.txt": card(
        "73", "2009-07", "Solid Fuel Questionnaire – Supplement to Residential Section",
        "N/A (underwriting supplement)",
        "New business / renewal underwriting",
        """Purpose:
Supplement collecting information on wood stoves, pellet stoves,
fireplaces, and other solid-fuel heating devices on a residential
property. Solid fuel devices are a leading cause of home fires;
carriers underwrite them carefully and may require specific
installation, clearance, and inspection criteria.

Captures:
- Insured / property location
- Type of solid fuel device (wood stove, pellet stove, fireplace,
  insert, outdoor wood furnace)
- Make, model, age
- Installation:
  * Installer (professional vs. self)
  * Permit and inspection records
  * Clearance from combustibles (floor, walls, ceiling)
  * Floor protection (hearth pad, masonry)
  * Wall protection
- Chimney type, age, last cleaning, last inspection
- Use frequency (primary heat, supplemental, decorative)
- Smoke detectors, carbon monoxide detectors
- Fire extinguisher availability

When used:
- HO new business with solid fuel devices on the property
- Renewal review where solid fuel device added mid-term
- Underwriting of country / rural homes with wood heat

Notes:
- Some carriers won't write or will surcharge homes with solid
  fuel as primary heat
- Pairs with ACORD 89 (Residential Section) for the underlying
  property data""",
    ),

    "ACORD 74 (2009-09) Residence Based Business Supplement to Residential Section.txt": card(
        "74", "2009-09", "Residence Based Business Supplement to Residential Section",
        "N/A (underwriting supplement)",
        "New business / renewal underwriting",
        """Purpose:
Supplement disclosing in-home business activity on a residential
property. Most homeowners policies exclude or limit business
exposures; this form lets the underwriter assess the activity and
either accept it (often with an endorsement), exclude it, or refer
it to commercial lines.

Captures:
- Insured / property location
- Type of business activity (occupation, services provided)
- Annual revenue
- Number of employees / contractors
- Customer / client visits to the residence (frequency, parking,
  signage)
- Business property kept on premises (computers, inventory,
  equipment)
- Business vehicles
- Professional licenses
- Whether the business is incorporated / LLC

When used:
- HO new business where any in-home business is disclosed
- Mid-term endorsement when an insured starts a home business
- Renewal review where business activity changes

Notes:
- Many activities can be covered with a home business endorsement
  (HO 04 42 or similar); larger operations require a BOP or other
  commercial policy
- Failure to disclose can void coverage on business-related claims
- Pairs with ACORD 89 (Residential Section) and ACORD 80
  (Homeowner Application)""",
    ),

    "ACORD 75 (2016-03) Insurance Binder.txt": card(
        "75", "2016-03", "Insurance Binder",
        "Typically up to 30-90 days (binder validity period)",
        "Temporary coverage at policy inception (pending formal policy issuance)",
        """Purpose:
Temporary evidence of insurance coverage in force pending issuance
of the formal policy. Binds coverage immediately upon agreement
between the producer and insured (or carrier and insured), with the
formal policy issued later. Used when insurance must be in effect
before the policy can be physically issued — closings, court orders,
contractual deadlines.

Captures:
- Producer / agency information
- Insured name, address
- Insurer name(s) and NAIC numbers
- Type of insurance and coverage form
- Coverage limits and deductibles
- Premium (estimated or final)
- Property / vehicle / risk being covered
- Effective date and expiration of the binder
- Mortgagee / loss payee / additional insured
- Producer / authorized representative signature
- Underwriter approval (where required)

When used:
- Real estate closings requiring proof of insurance at closing
- Vehicle purchases where the buyer needs immediate insurance to
  drive off the lot
- Court-ordered coverage with a deadline
- Commercial transactions requiring coverage before formal policy
  issuance

Notes:
- A binder is enforceable evidence of coverage with the same legal
  effect as the policy for the binder period
- Most binders are valid 30-90 days; if the formal policy isn't
  issued by then, the binder may need to be renewed
- Distinct from ACORD 27/28 (evidence forms) which are issued AFTER
  the policy is in force; the binder is the bridge document""",
    ),

    "ACORD 76 (1993-09) Binder Log.txt": card(
        "76", "1993-09", "Binder Log",
        "N/A (administrative log)",
        "N/A (administrative tracking of issued binders)",
        """Purpose:
Internal agency log tracking insurance binders issued. Provides an
audit trail of who received which binder, when, and for what
coverage — paired with policy issuance tracking to ensure binders
don't expire without the formal policy being in place.

Captures:
- Producer / agency information
- For each binder issued:
  * Binder number / sequence
  * Date issued
  * Insured name
  * Type of coverage
  * Insurer
  * Binder effective and expiration dates
  * Date formal policy issued (closing the binder)
  * Authorized representative

When used:
- Agency administrative recordkeeping for binders
- E&O compliance / audit trail
- Identifying binders approaching expiration without policy issuance

Notes:
- Edition is from 1993 — most agencies now track binders in their
  AMS rather than on paper logs
- Critical E&O exposure: an expired binder without a formal policy
  in place leaves the insured uncovered
- Companion to ACORD 75 (Insurance Binder)""",
    ),

    "ACORD 81 (2016-03) Personal Inland Marine Application.txt": card(
        "81", "2016-03", "Personal Inland Marine Application",
        "12 months (typical)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Application for personal inland marine coverage — scheduled and
unscheduled personal property requiring specialized coverage that
exceeds standard homeowners limits. Used for jewelry, fine art,
collectibles, musical instruments, cameras, sports equipment, and
similar high-value personal property.

Captures:
- Producer / agency information
- Applicant name, address, contact, occupation
- Whether applicant has homeowners coverage and with what carrier
- Items to be scheduled:
  * Description, value, year acquired
  * Appraisal date and appraiser
  * Photographs available
  * Storage location (home, safe deposit box, traveling)
  * Whether item is worn / used regularly
- Blanket coverage on unscheduled property (sublimits)
- Loss history on personal property
- Security: alarms, safes, vault, lock systems
- Insured signature

When used:
- New business for stand-alone personal IM policies
- Adding scheduled property to an HO via IM endorsement
- Renewal review of scheduled values
- After major purchases (engagement ring, art acquisition)

Notes:
- Pairs with ACORD 80 (Homeowner Application) when IM is endorsed
  to a homeowners policy
- Appraisals are typically required for items above carrier
  thresholds (often $5,000 or higher per piece)""",
    ),

    "ACORD 82 (2025-07) Watercraft Application.txt": card(
        "82", "2025-07", "Watercraft Application",
        "12 months (typical, may be seasonal in some markets)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Application for personal watercraft (boat) insurance covering hull,
liability, medical payments, and uninsured boater coverages. Used
for pleasure craft — runabouts, sailboats, fishing boats,
houseboats, personal watercraft (jet skis), and small yachts.

Captures:
- Producer / agency information
- Applicant name, address, contact
- Watercraft information:
  * Year, make, model, length
  * Hull material, propulsion (inboard, outboard, sail, PWC)
  * Hull / motor identification numbers
  * Horsepower, top speed
  * Trailer (year, make, value)
- Use: pleasure, fishing, racing, charter, commercial
- Navigation area (lakes, coastal, ocean, US/international)
- Storage: in water, dry storage, trailered
- Operator information: experience, USCG license, prior boating
  losses
- Coverage requested:
  * Hull (agreed value, ACV, deductible)
  * Liability limit
  * Medical payments
  * Uninsured boater
  * On-water towing
- Loss history
- Insured signature

When used:
- New business on personal watercraft
- Renewal review with seasonal/use changes
- Adding watercraft to existing personal lines portfolio

Notes:
- Larger yachts (typically 26+ feet) often go to specialty marine
  markets rather than standard personal watercraft policies
- Pairs with ACORD 282 (Watercraft Section) and ACORD 283 (Personal
  Umbrella Application Section) for specialty coverage details""",
    ),

    "ACORD 83 (2025-07) Personal Umbrella Application.txt": card(
        "83", "2025-07", "Personal Umbrella Application",
        "12 months (typical)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Application for personal umbrella liability insurance — excess
liability coverage sitting above the limits of underlying personal
auto, homeowner, watercraft, and other personal liability policies.
Provides additional protection against catastrophic liability
claims and certain coverages not available in primary policies.

Captures:
- Producer / agency information
- Applicant name, address, contact, occupation
- Spouse / co-applicant information
- Umbrella limit requested ($1M, $2M, $5M, higher)
- Underlying policies (auto, HO, watercraft, motorcycle, ATV):
  * Carrier
  * Limits (must meet umbrella underlying requirements)
  * Policy effective dates
- Household members and drivers
- Vehicles: autos, motorcycles, RVs, ATVs
- Watercraft, aircraft (where applicable)
- Rental properties owned
- Business activities, board / officer positions
- Domestic employees
- Loss history (auto, HO, prior umbrella)
- Animals (especially "vicious breeds" listed by carrier)
- Underwriting questions: trampolines, swimming pools, foreign
  travel, criminal history
- Insured signature

When used:
- High-net-worth or above-average liability exposure
- Customers with multiple primary policies wanting consolidated
  excess coverage
- Replacing or upgrading existing umbrella

Notes:
- Underlying limits requirement is strict — typically $250K/500K/100K
  on auto and $300K on HO; failing to maintain underlying coverage
  voids the umbrella
- Pairs with ACORD 283 (Personal Umbrella Application Section)""",
    ),

    "ACORD 84 (2016-11) Dwelling Fire Application.txt": card(
        "84", "2016-11", "Dwelling Fire Application",
        "12 months (typical)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Application for dwelling fire (DP-1, DP-2, DP-3) coverage —
typically used for non-owner-occupied residential properties such as
rental properties, secondary homes, or properties under renovation
where a homeowners policy isn't appropriate.

Captures:
- Producer / agency information
- Applicant name, address, contact
- Property location and description
- Occupancy: owner-occupied, tenant-occupied, vacant, seasonal
- Number of units / families
- Construction, year built, square footage, roof
- Coverage requested:
  * Coverage A (dwelling)
  * Coverage B (other structures)
  * Coverage C (personal property — usually limited on DP)
  * Coverage D (loss of rents / loss of use)
  * Liability (Coverage L) and medical payments (Coverage M) where
    available
- Form selection: DP-1 (basic), DP-2 (broad), DP-3 (special)
- Deductibles
- Mortgagee / additional interest information
- Tenant information (if applicable)
- Prior insurance and loss history

When used:
- Rental property new business
- Vacant property coverage
- Property under renovation
- Secondary / seasonal homes that don't meet HO occupancy
  requirements

Notes:
- DP-3 is the most common form (special perils named on dwelling,
  named perils on contents)
- Pairs with ACORD 80 (Homeowner Application) when an applicant has
  both a primary residence and rental properties""",
    ),

    "ACORD 85 (2016-11) Mobile Home Application.txt": card(
        "85", "2016-11", "Mobile Home Application",
        "12 months (typical)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Application for mobile / manufactured home insurance. Captures the
specific characteristics of mobile homes that drive underwriting and
rating differently than conventional dwellings.

Captures:
- Producer / agency information
- Applicant name, address, contact
- Mobile home information: year, make, model, serial / HUD number
- Dimensions (length, width)
- Single-wide / double-wide / triple-wide
- Foundation, tie-down, skirting (see ACORD 72 for detailed
  supplement)
- Park or owned land
- Occupancy
- Coverage requested:
  * Coverage A (dwelling) at replacement cost or ACV
  * Coverage B (other structures)
  * Coverage C (personal property)
  * Coverage D (loss of use)
  * Personal liability and medical payments
- Deductibles (all-other-perils, wind/hail)
- Prior insurance and loss history
- Mortgagee / additional interest
- Underwriting questions

When used:
- New business for mobile / manufactured home owners
- Renewal review
- Pairs with ACORD 72 (Mobile Home Supplement) for detailed
  characteristics

Notes:
- HUD-code (post-1976) homes are far easier to insure than
  pre-HUD-code homes; some carriers won't write pre-HUD
- Wind / tie-down characteristics drive rates substantially
  in coastal and tornado-prone states""",
    ),

    "ACORD 89 (2016-11) Residential Section.txt": card(
        "89", "2016-11", "Residential Section",
        "Matches underlying personal lines policy",
        "New business / renewal underwriting (residential exposure detail)",
        """Purpose:
Modular section capturing residential property underwriting detail
that attaches to a personal lines application (homeowners, dwelling
fire, etc.). Allows the underwriter to assess the structure,
protection, and exposure characteristics in a standardized format.

Captures:
- Insured / property location
- Property characteristics:
  * Year built, year of major updates
  * Square footage, number of stories
  * Construction type (frame, masonry veneer, masonry)
  * Foundation type
  * Roof type, material, age
  * Heating type and age
  * Plumbing and electrical updates
- Protection:
  * Distance to fire department
  * Distance to fire hydrant
  * Protection class
  * Smoke detectors, fire extinguishers, sprinklers
  * Burglar alarm (local, central station)
- Occupancy and use
- Special features (pool, trampoline, deck, outbuildings)
- Animals, business activities, prior cancellations

When used:
- HO new business as the residential exposure detail
- Renewal review of structure and protection class
- Pairs with ACORD 80 (Homeowner Application), ACORD 84 (Dwelling
  Fire), ACORD 85 (Mobile Home), ACORD 88 (Personal Insurance
  Application)

Notes:
- Often pre-populated by data feeds (CoreLogic, etc.) and confirmed
  by the producer rather than re-keyed
- Drives Coverage A replacement cost calculation when paired with
  ACORD 42""",
    ),

    "ACORD 91 (2009-10) Good Student Driver Training.txt": card(
        "91", "2009-10", "Good Student Driver Training",
        "Matches underlying auto policy",
        "New business / renewal underwriting (rate credit qualification)",
        """Purpose:
Documentation supporting good student and driver training rate
credits on personal auto policies. Captures the academic standing or
training course completion that qualifies a young driver for a
discount.

Captures:
- Insured / driver name, DOB, license number
- Underlying auto policy information
- Good student credit:
  * School name and address
  * GPA or class rank
  * Term / period covered
  * Verification (transcript, school official signature)
- Driver training credit:
  * Course name, provider, location
  * Completion date
  * Course type (defensive driving, accident prevention,
    state-approved teen course)
  * Certificate number
- Insured / parent signature

When used:
- New business for households with high school or college-age
  drivers
- Renewal review when grades or course completion change
  qualification status
- Adding a young driver to an existing policy

Notes:
- State and carrier credits vary; the form supports the broadest
  set of typical credit programs
- Most carriers re-verify good student credits at renewal""",
    ),

    "ACORD 92 (2012-03) Medical Statement.txt": card(
        "92", "2012-03", "Medical Statement",
        "Matches underlying policy",
        "New business / renewal underwriting (medical disclosure)",
        """Purpose:
Insured's signed medical statement disclosing medical conditions
relevant to underwriting decisions on personal lines (auto medical,
disability, certain health-adjacent products) or supporting claim
investigations.

Captures:
- Insured / claimant name, DOB
- Underlying policy / claim reference
- Medical history:
  * Current conditions and treatments
  * Medications
  * Recent hospitalizations or surgeries
  * Treating physicians
- Authorization to release medical records (HIPAA-compliant
  language)
- Specific questions relevant to the underwriting or claim context
- Insured signature with date and witness (if required)

When used:
- Underwriting personal lines products with medical questions
- Auto medical payments claim investigation
- Disability or related coverage claim follow-up

Notes:
- Medical authorizations have specific HIPAA requirements; the form
  language must comply with current federal and state privacy law
- Often used in conjunction with separate HIPAA authorization
  forms""",
    ),

    "ACORD 93 (2016-08) Young Driver Questionnaire.txt": card(
        "93", "2016-08", "Young Driver Questionnaire",
        "Matches underlying auto policy",
        "New business / mid-term change (adding a young driver)",
        """Purpose:
Underwriting questionnaire for young or newly licensed drivers being
added to a personal auto policy. Captures driving history,
education, and household context that drive rating and underwriting
decisions on the riskiest segment of personal auto.

Captures:
- Insured / parent name, policy number
- Young driver name, DOB, license number, license issue date
- Driver education / training:
  * State-approved teen course completion
  * Driver's ed grade
  * Defensive driving courses
- Academic standing (good student qualification — see ACORD 91)
- Vehicle assigned (or principal driver of multiple)
- Anticipated annual mileage
- Vehicle access (own car, shared, occasional)
- Out-of-state college student (where applicable)
- Driving history:
  * Prior accidents (at-fault, not at-fault)
  * Prior violations
  * SR-22 / FR filings
- Insured / parent signature

When used:
- Adding a teen driver to a household policy
- New business with young drivers in household
- Renewal review when driver status changes

Notes:
- Pairs with ACORD 91 (Good Student Driver Training) when credit
  qualification applies
- Some carriers require this for any driver under a specified age
  (typically 25)""",
    ),

    "ACORD 99 (2009-02) Accidents - Convictions Schedule.txt": card(
        "99", "2009-02", "Accidents / Convictions Schedule",
        "N/A (attaches to underlying policy)",
        "New business / renewal underwriting (loss history)",
        """Purpose:
Schedule capturing all auto accidents and motor vehicle convictions
for each driver on a personal auto policy. Provides the loss history
detail that carriers use for rating, surcharging, or accept/decline
decisions.

Captures:
- Underlying auto policy / insured information
- For each driver, for each accident:
  * Date, location
  * Description of accident
  * At-fault determination
  * Bodily injury and property damage amounts
  * Citation issued
  * Insurance company that paid
- For each driver, for each conviction:
  * Date, location
  * Type of violation (moving, non-moving, DUI, reckless)
  * Citation / case number
  * Disposition (guilty, no contest, dismissed)
- Driver signatures attesting to accuracy

When used:
- New business loss history disclosure
- Renewal review where MVR changes prompt re-rating
- Resolving discrepancies between insured-disclosed history and
  carrier-pulled MVRs / CLUE reports

Notes:
- Carriers verify against MVR (Motor Vehicle Report) and CLUE
  (Comprehensive Loss Underwriting Exchange); discrepancies
  between disclosed and verified history trigger underwriting
  review
- Material misrepresentation can void coverage""",
    ),

    "ACORD 101 (2008-01) Additional Remarks Schedule.txt": card(
        "101", "2008-01", "Additional Remarks Schedule",
        "N/A (attaches to underlying form)",
        "Continuation / supplement of remarks on any application",
        """Purpose:
Generic continuation page for capturing additional remarks,
explanations, or notes that exceed the space available on the
primary application or supplement. Used across personal and
commercial lines as a "spillover" or annotation page.

Captures:
- Reference to primary form (form number, applicant)
- Section / field being continued
- Free-text remarks
- Additional disclosures or explanations
- Signatures (where supporting underlying disclosures)

When used:
- Any application or supplement requiring more space than provided
- Long-form explanations for prior losses, lapses, or
  cancellations
- Detailed narrative for unique exposures

Notes:
- Treated as part of the underlying application for misrepresentation
  purposes — content here has the same effect as on the primary form
- Most modern AMS systems handle this digitally; the paper form
  exists for consistent format""",
    ),

    "ACORD 103 (2012-03) Personal Auto Application Schedule – Additional Resident and Driver Information Section.txt": card(
        "103", "2012-03", "Personal Auto Application Schedule – Additional Resident and Driver Information Section",
        "Matches underlying auto policy",
        "New business / renewal underwriting (additional drivers / residents)",
        """Purpose:
Continuation schedule for personal auto applications with more
drivers or household residents than the main application form
accommodates. Captures the same information per driver/resident as
the main app.

Captures:
- Reference to primary auto application (insured, policy)
- For each additional driver / resident:
  * Name, DOB, gender, marital status
  * Relationship to named insured
  * License number and state
  * Years licensed
  * Occupation, employer, education
  * Good student status, driver training
  * Excluded driver status (where applicable)
  * Vehicle assigned / principal operator
- Signatures

When used:
- Households with 4+ drivers or residents
- Multi-generational households
- Auto policies with multiple covered or excluded drivers

Notes:
- Most AMS systems generate this automatically when driver count
  exceeds the primary form's capacity
- Pairs with ACORD 99 (Accidents / Convictions Schedule) where
  loss history detail also requires continuation""",
    ),

    "ACORD 105 (2012-06) Apartment Building Supplement.txt": card(
        "105", "2012-06", "Apartment Building Supplement",
        "12 months (typical)",
        "New business / renewal underwriting (commercial residential supplement)",
        """Purpose:
Supplement capturing the operational and structural detail of
apartment buildings being underwritten as commercial property. Used
when the property is large enough that ACORD 84 (Dwelling Fire) or
HO doesn't apply — typically 4+ units or commercial ownership.

Captures:
- Insured / property location
- Number of buildings, units, stories
- Construction, year built, square footage
- Roof type, age, last replacement
- Heating, plumbing, electrical updates
- Protection: smoke detectors, sprinklers, alarms, distance to FD
- Occupancy: percent occupied, tenant mix (residential / commercial)
- Tenant screening procedures
- On-site management / maintenance
- Common areas (pools, fitness, laundry, parking)
- Pet policy
- Loss history (claims, fires, water damage, liability)
- Mortgagee / additional interests

When used:
- Commercial property new business on apartment buildings
- Renewal review for multifamily properties
- Acquisition / portfolio additions

Notes:
- Pairs with ACORD 140 (Property Section) for the underlying
  commercial property exposure
- Pairs with ACORD 126 (CGL Section) for premises liability detail""",
    ),

    "ACORD 106 (2010-04) Vacant Building Supplement.txt": card(
        "106", "2010-04", "Vacant Building Supplement",
        "12 months (often shorter; vacant policies sometimes 3-6 month terms)",
        "New business / renewal underwriting (specialty / non-standard market)",
        """Purpose:
Supplement underwriting vacant or unoccupied buildings, which
present elevated risks (vandalism, theft, undetected water damage,
fire) that standard property markets may decline. Vacant building
coverage often goes to specialty markets with specific underwriting
requirements.

Captures:
- Insured / property location
- Reason for vacancy (renovation, for sale, for lease, abandoned)
- Length of vacancy (current and projected)
- Prior occupancy (residential, commercial, industrial)
- Building condition: structural integrity, roof, windows, doors
- Security: locks, fencing, lighting, alarm, monitoring service,
  caretaker / property manager visits
- Utilities status (electric, gas, water shut off or maintained)
- Heating during winter (to prevent freeze damage)
- Renovation activity, contractor info, permits
- Distance to fire department
- Loss history including any prior vacant-period claims

When used:
- Vacant property new business
- Renewal of vacancy policies (usually shorter terms than standard
  HO/CP)
- Properties between tenants undergoing renovation

Notes:
- Many standard markets exclude or limit vacant property coverage
  beyond 30-60 days; specialty markets pick up the longer-vacancy
  exposure
- Vacancy often triggers coverage exclusions (e.g., vandalism,
  glass, water damage) on standard property forms — the supplement
  documents the underwriter's awareness of the vacancy""",
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
