"""Batch 10 — aviation forms (17 forms)."""
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
    "ACORD 325 (2013-09) Aviation Insurance Application – Applicant Information Section.txt": card(
        "325", "2013-09", "Aviation Insurance Application – Applicant Information Section",
        "12 months (typical)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Applicant information section for aviation insurance — the aviation-
specific counterpart to ACORD 125 (Commercial Insurance Application
Applicant Information Section). Captures the operator, ownership,
operational characteristics, and prior coverage that drive aviation
underwriting.

Captures:
- Producer / agency information
- Insured / aircraft owner / operator name and contact
- Type of operation:
  * Pleasure / business
  * Industrial aid
  * Charter / commercial passenger
  * Aerial application (crop dusting, fire suppression)
  * Flight school / instruction
  * Aircraft management / FBO
- Operating organization (sole proprietor, LLC, corp, partnership)
- Years in aviation
- Number of aircraft, hangars, locations
- Number of pilots and flight hours flown annually
- Prior aviation insurance carriers (5+ year history)
- Prior aviation losses
- Geographic operating area
- Use restrictions / regulatory authorizations (Part 91, 121, 135)
- Subsidiaries, joint ventures, related entities
- Certificate holder / lender / lessor relationships

When used:
- All aviation submissions — pairs with line-specific sections
  (ACORD 330 Aircraft Section, ACORD 327 Airport / FBO Liability,
  etc.)
- Renewal review of operational changes
- New business across all aviation lines

Notes:
- Pairs with line-of-business sections rather than ACORD 125 —
  aviation has its own application family
- Industry / operation type drives carrier appetite significantly""",
    ),

    "ACORD 326 (2006-04) Airport Property Supplement.txt": card(
        "326", "2006-04", "Airport Property Supplement",
        "12 months (typical commercial term)",
        "New business / renewal underwriting (airport property)",
        """Purpose:
Underwriting supplement for airport property exposures — buildings,
runways, hangars, FBO facilities, hangar contents. Captures the
property characteristics specific to airport operations beyond what
the standard property section accommodates.

Captures:
- Reference to ACORD 325
- Airport identification (FAA identifier, name, location)
- Airport type (private, public, towered, untowered)
- Property to be insured:
  * Buildings (terminal, hangars, FBO, maintenance, fuel facilities)
  * Construction, year built, square footage
  * Building values
  * Contents values
- Runway and taxiway exposure (paved length, condition)
- Fueling operations:
  * Fuel storage (tanks, capacity, type — Avgas, Jet-A)
  * Fuel handling equipment
  * Fuel-related liability
- Aircraft handling / ground operations
- Tenant aircraft (number, value, occupancy of hangars)
- Protection: fire suppression, alarm, on-airport firefighting
- Loss history (property and aviation-related)

When used:
- Airport / FBO new business
- Renewal review of property values and exposures
- Pairs with ACORD 327 (Airport and FBO Liability Section)

Notes:
- Airport property has unique exposures — fueling, runway, hangar
  collapse — that standard CP doesn't fully address
- Fuel storage / handling is heavily regulated and a major
  underwriting concern""",
    ),

    "ACORD 327 (2016-03) Airport and FBO Liability Section.txt": card(
        "327", "2016-03", "Airport and FBO Liability Section",
        "12 months (typical commercial term)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for airport and Fixed-Base Operator (FBO)
liability coverage. Captures the unique liability exposure of
operating an airport, FBO, or aircraft service facility — premises
liability, products and completed operations on aviation services,
hangarkeepers liability for aircraft in custody.

Captures:
- Reference to ACORD 325
- Operation type: airport, FBO, fueling, maintenance, flight school,
  charter
- Coverage parts requested:
  * Premises and operations liability (each occurrence, aggregate)
  * Products and completed operations
  * Personal and advertising injury
  * Hangarkeepers liability (each aircraft, aggregate)
  * Aircraft fueling liability
  * Aircraft sales liability
  * Lessors liability (where applicable)
  * Contractual liability
- Limits and deductibles
- Annual revenue by service line
- Number of aircraft serviced, fueled, maintained per year
- Aircraft in custody (max value, average value)
- Pilot training / flight school (hours, students, instructors)
- Subcontractors and their insurance
- Loss history (premises, operations, hangarkeepers)

When used:
- Airport / FBO new business
- Aviation service operator submissions
- Aircraft maintenance facility coverage

Notes:
- Hangarkeepers liability covers aircraft in the FBO's custody for
  service / storage — a significant exposure
- Fueling operations are a major liability concern (fueling errors
  can cause engine failure)
- Pairs with ACORD 326 (Airport Property Supplement) and ACORD 20
  (Certificate of Aviation Liability)""",
    ),

    "ACORD 328 (2024-06) Private Hangar Liability Section.txt": card(
        "328", "2024-06", "Private Hangar Liability Section",
        "12 months (typical)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Liability section for private hangars — typically owned by aircraft
owners or small flight departments rather than commercial FBOs.
Covers premises liability and limited hangarkeepers exposure for
the owner's own aircraft and occasional guest aircraft.

Captures:
- Reference to ACORD 325
- Hangar location (airport, address)
- Hangar ownership (insured, leased, condo)
- Aircraft typically housed (own vs. guest)
- Coverage:
  * Premises liability (each occurrence, aggregate)
  * Hangarkeepers (limited — usually for guest aircraft)
  * Personal and advertising injury
  * Medical payments
- Annual hangar use (frequency, hours)
- Other tenants in shared hangars
- Maintenance activity in the hangar (self vs. contracted)
- Loss history

When used:
- Private aircraft owners with hangars
- Small flight departments
- Aircraft owners renting hangar space at airports

Notes:
- Distinct from ACORD 327 (Airport and FBO Liability) — 328 is for
  private use rather than commercial operation
- Hangarkeepers exposure is much lower than commercial FBOs""",
    ),

    "ACORD 329 (2014-12) Aviation Products Liability.txt": card(
        "329", "2014-12", "Aviation Products Liability",
        "12 months (typical, often claims-made for products)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Aviation products liability section for manufacturers, distributors,
service centers, and overhaulers of aviation products — engines,
airframes, avionics, parts, accessories. Aviation products
liability is a specialty market with extreme stakes (product failure
can cause fatal accidents).

Captures:
- Reference to ACORD 325
- Type of operation:
  * Manufacturer (OEM, parts)
  * Distributor / dealer
  * Maintenance / service / overhaul
  * STC (Supplemental Type Certificate) holder
  * Component repair
- Products manufactured / distributed / serviced
- Annual revenue by product line
- Geographic distribution
- FAA certifications (PMA, STC, repair station authorization)
- Quality control / testing programs
- Product traceability and serial number tracking
- Service bulletins and AD compliance
- Coverage:
  * Each occurrence / aggregate
  * Products / completed operations
  * Defense provisions
- Claims-made retroactive date (where applicable)
- Loss history (product claims, recalls, AD-driven losses)

When used:
- Aviation product manufacturers
- Parts distributors
- Maintenance / repair / overhaul (MRO) operations
- Component overhaul shops

Notes:
- Aviation products liability is one of the highest-stakes E&O / PL
  exposures — single product failure can cause multiple fatalities
- Aviation product claims often involve lengthy investigations
  (NTSB, FAA) that can extend tail liability
- Pairs with ACORD 339 (Aviation Products Liability Change Request)
  for mid-term changes""",
    ),

    "ACORD 330 (2016-03) Aircraft Section.txt": card(
        "330", "2016-03", "Aircraft Section",
        "12 months (typical)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for aircraft hull and liability coverage —
the core aviation policy section. Captures the specific aircraft,
pilots, use, and coverage detail that drive aviation underwriting.

Captures:
- Reference to ACORD 325
- Aircraft information:
  * Registration (N-number)
  * Make, model, year, serial number
  * Engine type and total time
  * Airframe total time
  * Type of operation (Part 91 personal/business, Part 135 charter,
    Part 121 air carrier)
- Hull coverage:
  * Agreed value or stated value
  * Deductible (in motion / not in motion)
- Liability coverage:
  * Each occurrence
  * Per-passenger seat
  * Property damage / passenger property
  * Bodily injury (passenger and non-passenger)
- Use limitations (pleasure, business, commercial, instruction)
- Geographic operating area / international approvals
- Pilot information (referenced separately on ACORD 331 Pilot
  Experience):
  * Named pilots and qualifications
  * Open pilot warranty (minimum hours, ratings, type training)
- Storage location (hangared vs. tied down)
- Lender / lessor / loss payable
- Loss history

When used:
- Aircraft new business
- Renewal review
- Adding aircraft to existing aviation programs
- Mid-term changes (referred to ACORD 340)

Notes:
- Pairs with ACORD 331 (Pilot Experience) for pilot detail and
  ACORD 333 (Aircraft Schedule) for fleet detail
- Open pilot warranty is critical — pilots must meet warranty
  qualifications or coverage may not apply""",
    ),

    "ACORD 331 (2011-11) Pilot Experience.txt": card(
        "331", "2011-11", "Pilot Experience",
        "Matches underlying aviation policy",
        "Attached to new business, renewal, or mid-term pilot changes",
        """Purpose:
Schedule of pilot experience for each named pilot on an aviation
policy. Aviation underwriting is heavily pilot-driven — total
hours, ratings, type-specific experience, and recent currency are
material factors in coverage acceptance and rates.

Captures:
- Reference to underlying aviation policy
- For each pilot:
  * Name, DOB
  * Pilot certificate (Private, Commercial, ATP)
  * Ratings (instrument, multi-engine, ATP, type ratings)
  * Medical certificate (1st, 2nd, 3rd class, expiration)
  * Flight Review / IPC currency
  * Total flight hours (logbook)
  * Hours in make / model
  * Last 90 days, last 12 months
  * Hours as PIC vs. SIC
  * Type-specific training (factory, simulator, type rating school)
  * Prior aviation accidents / incidents / violations

When used:
- New aviation policies for each named pilot
- Pilot additions / changes mid-term
- Annual renewal updates as hours accumulate

Notes:
- Pairs with ACORD 330 (Aircraft Section)
- Open pilot warranty in the policy specifies minimum experience —
  named pilots may have different requirements
- Recurrent training (annual or biennial flight review) is often
  a coverage condition""",
    ),

    "ACORD 332 (2006-04) Hangar Schedule.txt": card(
        "332", "2006-04", "Hangar Schedule",
        "Matches underlying policy",
        "Attached to new business, renewal, or mid-term changes",
        """Purpose:
Schedule listing hangars covered under an aviation policy. Used as
a continuation when the airport property supplement (ACORD 326)
needs more space or when hangars span multiple locations.

Captures:
- Reference to underlying policy
- For each hangar:
  * Airport / location
  * Hangar number / identifier
  * Construction (steel, concrete, fabric, wood)
  * Year built
  * Square footage / dimensions
  * Capacity (number / type of aircraft)
  * Tenant aircraft (if leased to others)
  * Building value
  * Contents value (tools, equipment, owner-occupied items)
  * Fire protection
  * Doors (manual, motorized, bi-fold)
- Tenant lease information (where applicable)

When used:
- Multi-hangar operations
- FBOs / airports with several hangar buildings
- Renewal review of hangar values

Notes:
- Pairs with ACORD 326 (Airport Property Supplement)
- Hangar collapse and fire are major property concerns; construction
  and protection details drive rating""",
    ),

    "ACORD 333 (2009-05) Aircraft Schedule.txt": card(
        "333", "2009-05", "Aircraft Schedule",
        "Matches underlying aviation policy",
        "Attached to new business, renewal, or mid-term changes",
        """Purpose:
Schedule of aircraft covered under an aviation policy. Used as a
continuation when the Aircraft Section (ACORD 330) needs more space
or when fleets are large enough to warrant a master schedule.

Captures:
- Reference to underlying aviation policy
- For each aircraft:
  * Registration (N-number)
  * Make, model, year, serial number
  * Type of operation
  * Total time on airframe / engines
  * Hull value (agreed / stated)
  * Hull deductibles (in motion / not in motion)
  * Liability limits applicable
  * Use limitations
  * Hangared location
  * Lender / lessor / loss payable
  * Effective date for the aircraft

When used:
- Multi-aircraft fleets
- Charter / FBO / flight school fleets
- Mid-term aircraft additions / deletions
- Renewal fleet review

Notes:
- Pairs with ACORD 330 (Aircraft Section) and ACORD 331 (Pilot
  Experience)
- Often AMS-generated for large fleets""",
    ),

    "ACORD 335 (2009-06) Aviation Policy Change Request – Applicant Information Section.txt": card(
        "335", "2009-06", "Aviation Policy Change Request – Applicant Information Section",
        "N/A (existing aviation policy)",
        "Mid-term change / endorsement (aviation applicant information)",
        """Purpose:
Aviation policy change request capturing applicant information
updates — name changes, address changes, ownership changes,
operational changes that affect the underlying ACORD 325 (Aviation
Insurance Application – Applicant Information Section).

Captures:
- Reference to underlying aviation policy
- Effective date of change
- Change in:
  * Insured name (legal name change, entity restructuring)
  * Mailing / business address
  * Operating organization type
  * Primary operations / use
  * Geographic operating area
  * Subsidiaries / related entities
- Insured signature

When used:
- Mid-term applicant information changes
- Entity restructuring affecting aviation policies
- Operational changes that affect underwriting basis

Notes:
- Pairs with ACORD 325 (the underlying applicant information
  section)
- Other aviation change requests cover specific exposures (336
  airport property, 337 airport/FBO liability, 338 private hangar
  liability, 339 aviation products, 340 aircraft, 341 pilot
  experience, 342 hangar)""",
    ),

    "ACORD 336 (2009-06) Airport Property Change Request.txt": card(
        "336", "2009-06", "Airport Property Change Request",
        "N/A (existing aviation policy)",
        "Mid-term change / endorsement (airport property)",
        """Purpose:
Mid-term change request for airport property exposures — adding,
deleting, or updating buildings, hangars, contents, fueling
facilities, runways covered under an aviation property policy.

Captures:
- Reference to underlying aviation policy and ACORD 326 (Airport
  Property Supplement)
- Effective date of change
- Change requested:
  * Adding new buildings / hangars / structures
  * Deleting structures (sold, demolished)
  * Updating values (after improvements, additions, depreciation)
  * Coverage limit changes
  * Fuel facility changes
  * Runway / taxiway updates
- Insured signature

When used:
- Construction / acquisition of new airport facilities
- Disposal of facilities
- Annual property value reviews triggering mid-term updates
- Adding fuel facilities or storage

Notes:
- Pairs with ACORD 326 (Airport Property Supplement) — change is to
  the property exposure that supplement documents""",
    ),

    "ACORD 337 (2016-03) Airport and FBO Liability Change Request.txt": card(
        "337", "2016-03", "Airport and FBO Liability Change Request",
        "N/A (existing aviation policy)",
        "Mid-term change / endorsement (airport and FBO liability)",
        """Purpose:
Mid-term change request for airport and FBO liability exposures —
adding services, changing coverage limits, modifying hangarkeepers
exposure, or updating operations that affect ACORD 327 (Airport and
FBO Liability Section).

Captures:
- Reference to underlying aviation policy and ACORD 327
- Effective date of change
- Change requested:
  * Coverage limit changes (premises, hangarkeepers, products)
  * Adding / removing service lines (fueling, maintenance, charter)
  * Hangarkeepers limit adjustments
  * Adding additional insureds (lenders, lessors, customers)
  * Operational changes affecting liability exposure
- Insured signature

When used:
- Operational changes affecting FBO services
- Coverage limit increases (often driven by contract requirements)
- Adding new revenue lines (e.g., adding a charter operation to an
  existing FBO)
- Mortgagee / additional insured changes

Notes:
- Pairs with ACORD 327 (Airport and FBO Liability Section)""",
    ),

    "ACORD 338 (2009-06) Private Hangar Liability Change Request.txt": card(
        "338", "2009-06", "Private Hangar Liability Change Request",
        "N/A (existing aviation policy)",
        "Mid-term change / endorsement (private hangar liability)",
        """Purpose:
Mid-term change request for private hangar liability — for aircraft
owners and small flight departments with private hangar coverage
under ACORD 328 (Private Hangar Liability Section).

Captures:
- Reference to underlying aviation policy and ACORD 328
- Effective date of change
- Change requested:
  * Coverage limit adjustments
  * Adding or removing hangars
  * Changing hangar tenants (own vs. shared)
  * Updating hangarkeepers exposure for guest aircraft
  * Liability limit changes
- Insured signature

When used:
- Acquiring new hangar space
- Releasing hangar space
- Changing aircraft housed in the hangar
- Adjusting liability limits

Notes:
- Pairs with ACORD 328 (Private Hangar Liability Section)
- Smaller and simpler than the FBO change (337) — private hangar
  use is less complex""",
    ),

    "ACORD 339 (2009-06) Aviation Products Liability Change Request.txt": card(
        "339", "2009-06", "Aviation Products Liability Change Request",
        "N/A (existing aviation products policy)",
        "Mid-term change / endorsement (aviation products liability)",
        """Purpose:
Mid-term change request for aviation products liability coverage —
for manufacturers, distributors, MROs, and STC holders adjusting
coverage on the products policy issued via ACORD 329.

Captures:
- Reference to underlying aviation products policy and ACORD 329
- Effective date of change
- Change requested:
  * Coverage limit adjustments
  * Adding or removing product lines
  * Adding or removing services (manufacturing, distribution,
    overhaul, STC)
  * Geographic distribution changes
  * FAA certification additions (new PMA, new STC, repair station
    authorization)
  * Retroactive date adjustments (claims-made)
- Insured signature

When used:
- New product introductions
- Acquiring or divesting product lines
- Adding new services (e.g., distributor adding STC business)
- Coverage limit changes driven by contracts or regulatory needs

Notes:
- Aviation products mid-term changes can have significant pricing
  impact — additional product lines add tail exposure
- Pairs with ACORD 329 (Aviation Products Liability)""",
    ),

    "ACORD 340 (2016-03) Aircraft Change Request.txt": card(
        "340", "2016-03", "Aircraft Change Request",
        "N/A (existing aviation policy)",
        "Mid-term change / endorsement (aircraft / hull / liability)",
        """Purpose:
Mid-term change request for aircraft on an existing aviation policy
— adding, deleting, or modifying aircraft coverage. Counterpart to
ACORD 71 (Personal Auto Policy Change Request) for the aviation
context.

Captures:
- Reference to underlying aviation policy and ACORD 330 / 333
- Effective date of change
- Change requested:
  * Adding new aircraft (with full ACORD 333 detail)
  * Deleting aircraft (sold, totaled, retired)
  * Hull value changes (purchase price changes, depreciation,
    appreciation on collectible aircraft)
  * Coverage limit changes
  * Use changes (e.g., personal to business, business to charter)
  * Geographic operating area changes
  * Lender / lessor / loss payable changes
- Insured signature

When used:
- Aircraft acquisition or sale
- Annual hull value reviews (especially for collectible / vintage
  aircraft)
- Use changes (often triggered by FAA certificate changes)
- Mid-term coverage adjustments

Notes:
- Aircraft purchases / sales typically require coverage to be in
  place at closing — often handled via ACORD 276 (Aircraft Insurance
  Binder) and then formalized with this change request
- Pairs with ACORD 330 (Aircraft Section) and ACORD 333 (Aircraft
  Schedule)""",
    ),

    "ACORD 341 (2011-11) Pilot Experience Change Request.txt": card(
        "341", "2011-11", "Pilot Experience Change Request",
        "N/A (existing aviation policy)",
        "Mid-term change / endorsement (pilot additions or changes)",
        """Purpose:
Mid-term change request for pilot information on an existing
aviation policy — adding new pilots, deleting pilots, or updating
pilot qualifications and currency.

Captures:
- Reference to underlying aviation policy and ACORD 331 (Pilot
  Experience)
- Effective date of change
- Change requested:
  * Adding new named pilot (with full ACORD 331 detail)
  * Deleting pilot
  * Updating pilot qualifications (new ratings, type ratings,
    additional hours)
  * Recurrent training updates
  * Medical certificate updates
- Insured signature

When used:
- Adding a new pilot to a policy mid-term
- Pilot retirements or departures
- Annual qualification updates as hours accumulate
- New ratings / type training completed

Notes:
- Aviation policies often have pilot warranties — adding a pilot
  who doesn't meet warranty requirements may require carrier
  approval before coverage applies
- Pairs with ACORD 331 (Pilot Experience)""",
    ),

    "ACORD 342 (2009-06) Hangar Change Request.txt": card(
        "342", "2009-06", "Hangar Change Request",
        "N/A (existing aviation policy)",
        "Mid-term change / endorsement (hangar coverage)",
        """Purpose:
Mid-term change request for hangar coverage on an existing aviation
policy — adding, deleting, or modifying hangar exposure documented
on ACORD 332 (Hangar Schedule).

Captures:
- Reference to underlying aviation policy and ACORD 332
- Effective date of change
- Change requested:
  * Adding new hangars
  * Deleting hangars
  * Building / contents value updates
  * Tenant changes (occupancy mix)
  * Construction or improvement updates
  * Fire protection updates
- Insured signature

When used:
- New hangar acquisition or construction
- Hangar disposal
- Improvements affecting value or rating
- Tenant changes affecting occupancy mix

Notes:
- Pairs with ACORD 332 (Hangar Schedule) and ACORD 326 (Airport
  Property Supplement)""",
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
