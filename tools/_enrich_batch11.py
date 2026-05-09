"""Batch 11 — agriculture, surety, premium (15 forms)."""
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
    "ACORD 401 (2016-03) Agriculture Application.txt": card(
        "401", "2016-03", "Agriculture Application",
        "12 months (typical, sometimes seasonal for crop programs)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Master application for agricultural / farm insurance — captures the
farm operation, ownership, livestock, crops, equipment, and
exposures that drive farm program rating. Used in lieu of ACORD 80
(homeowner) when the property has significant farm exposure.

Captures:
- Producer / agency information
- Applicant / farm owner / operator
- Farm location and acreage
- Type of operation:
  * Crop farming (grain, fruit, vegetables, specialty)
  * Livestock (cattle, hogs, poultry, dairy, equine)
  * Dairy operations
  * Aquaculture
  * Mixed operations
  * Hobby farm vs. commercial farm
- Annual farm revenue
- Number of farm employees
- Farm dwelling(s) (separate from personal HO)
- Farm structures (barns, silos, sheds, equipment storage)
- Farm equipment / machinery
- Livestock counts and values
- Crops and stored grain values
- Coverage requested:
  * Farm dwelling and contents
  * Farm structures
  * Farm personal property
  * Farm liability
  * Equipment / machinery
  * Livestock mortality
  * Crop coverage (or referred to crop insurance)
- Loss history

When used:
- Farm new business
- Renewal review
- Pairs with ACORD 402 (Agriculture Property Section), 404
  (Agriculture Liability Section), and other ag-specific sections

Notes:
- Federal crop insurance (RMA-administered) is separate from this
  form — for crop insurance, a different application family applies
- Hobby vs. commercial farm distinction matters for coverage
  eligibility""",
    ),

    "ACORD 402 (2016-03) Agriculture Property Section.txt": card(
        "402", "2016-03", "Agriculture Property Section",
        "12 months (typical)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Property line-of-business section for farm policies — captures
buildings, contents, equipment, and structures specific to agricultural
operations. Pairs with ACORD 401 to form a complete farm property
submission.

Captures:
- Reference to ACORD 401
- Farm dwelling(s):
  * Year built, square footage, construction
  * Coverage limit, deductible
- Farm structures:
  * Barns, silos, equipment sheds, grain bins, machine sheds
  * Construction, age, value
  * Use (hay storage, equipment, livestock, grain)
- Farm personal property (FPP):
  * Stored grain
  * Hay, feed
  * Tools, supplies
  * Schedule or blanket
- Farm machinery / equipment:
  * Mobile equipment (tractors, combines, balers)
  * Stationary equipment (irrigation, milking systems)
  * Schedule or blanket
- Coverage forms:
  * Special vs. broad vs. basic perils
  * Replacement cost vs. ACV
- Coinsurance percentages
- Catastrophe perils (windstorm, hail, lightning common in farm)

When used:
- Farm property new business
- Renewal review
- Pairs with ACORD 403 (Agriculture Property Section Scheduled /
  Unscheduled Personal Property)

Notes:
- Farm property has unique exposures (grain storage, livestock
  facilities) that standard CP doesn't address well
- Mobile farm equipment often covered as inland marine within the
  farm package""",
    ),

    "ACORD 403 (2016-03) Agriculture Property Section Scheduled - Unscheduled Personal Property.txt": card(
        "403", "2016-03", "Agriculture Property Section Scheduled / Unscheduled Personal Property",
        "12 months (typical)",
        "New business / renewal underwriting (farm personal property detail)",
        """Purpose:
Schedule of farm personal property for ACORD 402 (Agriculture
Property Section) — used when the operation has significant
scheduled or unscheduled FPP that needs detailed valuation. Captures
livestock, machinery, stored crops, and other movable farm property.

Captures:
- Reference to ACORD 401 / 402
- Scheduled items:
  * Specific farm machinery with serial numbers and values
  * Specialty equipment (irrigation, automated systems)
  * Specific livestock by ID / breed / value
- Unscheduled blanket coverage:
  * General farm personal property
  * Stored grain (with location and quantity limits)
  * Hay and feed
  * Supplies and inventory
  * Blanket equipment / tools
- Per-item and aggregate limits
- Deductibles by category

When used:
- Larger farms with significant FPP exposure
- Operations with valuable specialty equipment
- Renewal review of scheduled values

Notes:
- Pairs with ACORD 402 (Agriculture Property Section) and ACORD 406
  (Agriculture Supplement - Unscheduled Farm Personal Property
  Inventory Form)
- Stored grain has specific underwriting concerns (quantity,
  storage type, monitoring) that affect coverage""",
    ),

    "ACORD 404 (2016-03) Agriculture Liability Section.txt": card(
        "404", "2016-03", "Agriculture Liability Section",
        "12 months (typical)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Liability line-of-business section for farm policies — captures
premises, operations, products (farm goods sold direct), pollution,
and farm-specific liability exposures. Pairs with ACORD 401 to form
a complete farm liability submission.

Captures:
- Reference to ACORD 401
- Liability coverage parts:
  * Premises liability (each occurrence, aggregate)
  * Farm operations
  * Products / completed operations (farm products sold direct)
  * Personal and advertising injury
  * Medical payments
  * Pollution liability (chemical application, manure management)
- Special exposures:
  * U-pick / agritourism operations
  * Farm stand / farmers market sales
  * Custom farming for others
  * Animal-related liability (livestock escape, equine activities)
  * Hunting / fishing on farm property
- Limits and deductibles
- Additional insureds (landlords, lenders, custom operators)

When used:
- Farm new business
- Renewal review
- Operations with significant public exposure (agritourism)

Notes:
- Equine activities have specific liability statutes in many states
  (limitations on liability for inherent equine risks)
- Pesticide and chemical exposure can trigger pollution liability
  questions""",
    ),

    "ACORD 405 (2007-09) Agriculture Premises Diagram.txt": card(
        "405", "2007-09", "Agriculture Premises Diagram",
        "Matches underlying farm policy",
        "Underwriting documentation (farm premises layout)",
        """Purpose:
Diagram form used to depict the layout of farm premises — buildings,
structures, fields, livestock areas, fuel and chemical storage, and
distance relationships. Provides the underwriter with spatial
context that text descriptions can't convey.

Captures:
- Reference to underlying farm application
- Drawing of premises layout including:
  * Farm dwelling
  * Farm buildings (barns, silos, sheds)
  * Livestock facilities
  * Fuel storage tanks
  * Chemical storage
  * Stored grain / hay
  * Distances between structures (fire spread risk)
  * Distance to highways, neighboring properties
  * Access roads, water sources
- Annotation of construction types, fire protection, hazardous
  storage

When used:
- Larger farm submissions
- Properties with multiple high-value structures
- Operations with hazardous storage (fuel, fertilizer, chemicals)
- Renewal review when significant changes have occurred

Notes:
- Often replaced by aerial photography or satellite imagery in
  modern submissions; the form persists for older agency workflows
- Spatial relationships (distances, structure clustering) drive
  fire spread risk underwriting""",
    ),

    "ACORD 406 (2007-09) Agriculture Supplement - Unscheduled Farm Personal Property Inventory Form.txt": card(
        "406", "2007-09", "Agriculture Supplement - Unscheduled Farm Personal Property Inventory Form",
        "Matches underlying farm policy",
        "Underwriting documentation (FPP inventory)",
        """Purpose:
Inventory form for unscheduled farm personal property — provides a
detailed list of farm machinery, equipment, tools, and supplies
covered under blanket FPP coverage. Used to support underwriting
decisions on blanket limits and coinsurance.

Captures:
- Reference to ACORD 401 / 402 / 403
- Inventory of unscheduled FPP:
  * Tractors and farm machinery (year, make, model, value)
  * Hay and forage equipment (balers, mowers, rakes)
  * Tillage equipment (plows, discs, planters)
  * Livestock equipment (feeders, waterers, milking equipment)
  * Tools and supplies
  * Stored feed, hay, grain
  * Fuels and chemicals
- Total declared value
- Storage locations
- Replacement vs. ACV valuation

When used:
- Underwriting documentation for blanket FPP coverage
- Renewal updates as equipment is bought / sold
- After-loss claim documentation

Notes:
- Pairs with ACORD 403 (Agriculture Property Section Scheduled /
  Unscheduled Personal Property)
- Coinsurance compliance depends on accurate inventory valuation""",
    ),

    "ACORD 407 (2016-03) Livestock Mortality Section.txt": card(
        "407", "2016-03", "Livestock Mortality Section",
        "12 months (typical)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Line-of-business section for livestock mortality coverage —
specialty coverage for high-value individual animals (breeding stock,
show animals, racehorses, valuable bulls / dairy cows) that
warrants per-animal underwriting beyond blanket farm livestock
coverage.

Captures:
- Reference to ACORD 401 (or stand-alone equine application)
- Animal information:
  * Species, breed
  * Age, gender, color, markings
  * Registration / pedigree
  * ID (microchip, tattoo, brand)
  * Insured value
  * Use (breeding, show, racing, dairy, performance)
- Veterinary information:
  * Pre-insurance vet exam
  * Vaccinations / health history
  * Known medical conditions
- Coverage type:
  * Mortality (death from any cause)
  * Limited mortality (specified perils)
  * Theft and straying
  * Major medical / surgical (often separate)
  * Loss of use (specific to equine)
- Per-animal limits and aggregate limits
- Deductibles (% of value typical for some breeds)
- Loss history

When used:
- Stand-alone or endorsed coverage for valuable individual animals
- Equine operations (racing, breeding, show)
- Dairy / breeding operations with high-value individuals
- Renewal review

Notes:
- Pairs with ACORD 408 (Equine Liability Supplement) for equine
  operations with public exposure
- Vet exam typically required for high-value animals""",
    ),

    "ACORD 408 (2007-09) Equine Liability Supplement.txt": card(
        "408", "2007-09", "Equine Liability Supplement",
        "12 months (typical)",
        "New business / renewal underwriting (equine liability detail)",
        """Purpose:
Liability supplement specific to equine operations — boarding
stables, riding lessons, trail rides, breeding farms, training
facilities. Captures the unique liability exposure of operating
businesses involving horses and members of the public.

Captures:
- Reference to ACORD 401 / 404
- Equine operation type:
  * Boarding stable
  * Riding lessons / instruction
  * Trail rides / guided rides
  * Training / breaking
  * Breeding / standing stallions
  * Show / event hosting
- Number of horses owned vs. boarded
- Public exposure (number of riders, students, visitors per year)
- Riding programs:
  * Beginner vs. advanced
  * Children programs
  * Trail rides (length, terrain)
- Equine activity statute compliance (release / waiver
  documentation)
- Helmet policies, instructor qualifications
- Loss history (rider injuries, horse-related claims)

When used:
- Equine business new business
- Renewal review
- Operations adding lessons, trail rides, or other public exposure

Notes:
- Equine activity statutes in most states limit liability for
  inherent equine risks if the operation provides proper warnings
  and waivers — the form documents compliance
- Pairs with ACORD 407 (Livestock Mortality) when valuable horses
  are individually insured""",
    ),

    "ACORD 410 (2016-03) Small Farm - Ranch Application.txt": card(
        "410", "2016-03", "Small Farm / Ranch Application",
        "12 months (typical)",
        "New business, renewal (Quote / Bound / Issue Policy status)",
        """Purpose:
Streamlined application for small farm and ranch operations —
hobby farms, small-acreage operations with limited livestock or
crops, country properties with farm-like exposure. Simpler than the
full ACORD 401 (Agriculture Application) but more comprehensive than
a homeowners application.

Captures:
- Producer / agency information
- Applicant / property owner
- Property location and acreage (typically under specified threshold
  for "small farm" definition)
- Operation type:
  * Hobby farm
  * Part-time small-scale agriculture
  * Country property with limited livestock
  * Personal use with farm-like exposures
- Annual gross farm income (typically below carrier threshold for
  full ag program)
- Dwelling
- Outbuildings (limited inventory)
- Livestock (limited count, owner-use focus)
- Equipment (limited)
- Coverage requested:
  * Dwelling and contents
  * Outbuildings
  * Limited farm liability
  * Optional farm property and equipment
- Loss history

When used:
- Hobby farms not eligible for HO due to farm exposure
- Small-acreage country properties with farm characteristics
- Limited commercial farm exposure (under carrier-set thresholds)

Notes:
- Eligibility thresholds vary by carrier — some require minimum or
  maximum acreage / income to qualify
- For larger commercial operations, use ACORD 401 (Agriculture
  Application)""",
    ),

    "ACORD 501 (2016-06) Surety Report of Execution.txt": card(
        "501", "2016-06", "Surety Report of Execution",
        "Bond term (varies; typically 1-3 years for contract bonds)",
        "Bond execution reporting",
        """Purpose:
Producer / agency report to a surety carrier confirming the
execution of a surety bond on behalf of a principal. Documents the
bond issuance, principal, obligee, bond amount, and term — the
core information the surety needs for record-keeping and reporting
to the obligee.

Captures:
- Producer / agency information
- Surety carrier
- Principal (the party purchasing the bond)
- Obligee (the party requiring the bond, beneficiary)
- Bond type (contract, license, court, fiduciary, public official,
  etc.)
- Bond amount / penal sum
- Effective date and expiration / cancellation provisions
- Premium charged
- Indemnitor information (where applicable)
- Bond number / reference

When used:
- Initial bond execution
- Bond renewal / continuation
- Reporting to the surety carrier after bond issuance

Notes:
- Surety bonds are NOT insurance — they are guarantees of
  performance with three parties (principal, obligee, surety)
- Pairs with ACORD 502 (Contract Bond Request Form) and ACORD 503
  (Commercial or Miscellaneous Bond Request Form)""",
    ),

    "ACORD 502 (2018-08) Contract Bond Request Form.txt": card(
        "502", "2018-08", "Contract Bond Request Form",
        "Project / contract term",
        "Bond submission (bid bonds, performance bonds, payment bonds)",
        """Purpose:
Application form for contract surety bonds — bid bonds, performance
bonds, and payment bonds — used by contractors bidding on or
executing public works contracts and many private construction
projects. Captures the contract, contractor, and project specifics
the surety needs to underwrite the bond.

Captures:
- Producer / agency information
- Principal (contractor) name, address, FEIN
- Contractor information:
  * Years in business
  * Contractor type (general, subcontractor, specialty trade)
  * Bonding capacity (single project / aggregate)
  * Surety credit history
- Obligee / project owner
- Project information:
  * Project name and location
  * Contract amount
  * Contract term
  * Scope of work
  * Bid date (bid bond) or contract execution date
- Bond requested:
  * Bid bond (typically 5-20% of bid)
  * Performance bond (typically 100% of contract)
  * Payment bond (typically 100% of contract)
  * Maintenance / warranty bond
- Indemnitor information (corporate, personal)
- Financial information (often references separate financial
  statements)

When used:
- Contractor bid bond requests
- Performance / payment bond requests at contract execution
- Bond capacity establishment with a new surety

Notes:
- Surety underwriting is heavily based on contractor financial
  strength and project history — financial statements typically
  required separately
- Federal Miller Act and state Little Miller Acts require P&P bonds
  on public works above specified thresholds""",
    ),

    "ACORD 503 (2016-06) Commercial or Miscellaneous Bond Request Form.txt": card(
        "503", "2016-06", "Commercial or Miscellaneous Bond Request Form",
        "Bond term (varies by bond type)",
        "Bond submission (commercial / miscellaneous surety)",
        """Purpose:
Application form for commercial and miscellaneous surety bonds —
license bonds, permit bonds, court bonds, fiduciary bonds, public
official bonds, and other non-contract surety. Captures the bond
type, principal, obligee, and bond amount specific to the type of
bond requested.

Captures:
- Producer / agency information
- Principal (the party needing the bond)
- Bond type:
  * License bonds (insurance license, contractor license, etc.)
  * Permit bonds (sales tax, fuel tax)
  * Court bonds (appeal, supersedeas, replevin)
  * Fiduciary bonds (executor, administrator, guardian)
  * Public official bonds
  * Notary bonds
  * ERISA fidelity bonds
  * Customs / federal bonds
- Obligee (state, court, federal agency, etc.)
- Bond amount / penal sum
- Effective date and term
- Principal information (relevant to bond type)
- Indemnitor / financial information

When used:
- License and permit bond requirements
- Court-ordered bonds
- Fiduciary appointments requiring bond
- Public official appointments

Notes:
- Each bond type has its own underwriting considerations — court
  bonds focus on litigation context; license bonds on regulatory
  compliance; fiduciary on personal financial responsibility
- Pairs with ACORD 504 (Additional Entity Schedule) for bonds with
  multiple principals""",
    ),

    "ACORD 504 (2016-06) Additional Entity Schedule.txt": card(
        "504", "2016-06", "Additional Entity Schedule",
        "Matches underlying bond / policy",
        "Attached to bond or insurance submission",
        """Purpose:
Schedule listing additional entities — corporations, LLCs,
partnerships, individuals — that should be included as principals,
indemnitors, additional insureds, or other status on a bond or
insurance submission.

Captures:
- Reference to underlying bond or insurance application
- For each additional entity:
  * Entity name and type (corp, LLC, partnership, individual)
  * Tax ID / FEIN
  * Address
  * State of incorporation / formation
  * Relationship to primary principal / insured (subsidiary,
    affiliate, sister company, joint venture)
  * Status on the bond / policy (principal, indemnitor, additional
    insured, named insured)
  * Effective date

When used:
- Surety bonds with multiple principals or indemnitors
- Insurance applications with multiple named insureds
- Holding company / subsidiary structures
- Joint ventures

Notes:
- Pairs with ACORD 502 / 503 for surety, ACORD 125 for commercial
  insurance applications
- Critical for ensuring all related entities have proper bond /
  insurance status""",
    ),

    "ACORD 610 (2015-12) Premium Payment Supplement.txt": card(
        "610", "2015-12", "Premium Payment Supplement",
        "Matches underlying policy",
        "Premium payment processing",
        """Purpose:
Supplement capturing premium payment information for an insurance
policy — payment plan selected, billing arrangements, financing,
and any premium-related arrangements that don't fit on the primary
application.

Captures:
- Reference to underlying policy / application
- Premium payment plan:
  * Annual / semi-annual / quarterly / monthly
  * Direct bill (carrier bills insured)
  * Agency bill (producer collects and remits)
  * Insured bill
- Premium financing:
  * Premium finance company name and contact
  * Loan number
  * Down payment, balance financed
  * Power of Attorney for cancellation
- Payment method:
  * Check, ACH, credit card, wire
  * Recurring payment authorization
- Mortgagee escrow billing (where applicable)
- Audit billing (commercial)

When used:
- New business with non-standard payment arrangements
- Premium-financed policies
- Mortgagee escrow billing setups
- Mid-term changes to payment plan

Notes:
- Premium finance companies use Power of Attorney for cancellation —
  if the loan defaults, the finance company can cancel the policy
- Distinct from ACORD 305 (NFIP Credit Card Payment) which is
  NFIP-specific""",
    ),

    "ACORD 611 (2015-07) Claims History - Loss Run Request.txt": card(
        "611", "2015-07", "Claims History / Loss Run Request",
        "N/A (administrative request)",
        "Claims history / loss run documentation request",
        """Purpose:
Insured's request to a current or prior carrier for a loss run —
the official record of claims history under a policy. Loss runs are
required by new carriers during underwriting to verify the insured's
claims experience.

Captures:
- Insured / policy reference (current or prior policy)
- Producer making the request
- Carrier being requested (current or prior)
- Period of loss run requested (typically 3-5 years)
- Where to send the loss run (producer, new carrier, insured)
- Insured signature authorizing the request

When used:
- Marketing / quoting new business — new carriers request loss runs
- Renewal underwriting reviews
- Mid-term carrier transitions
- Claim auditing

Notes:
- Carriers are generally required to provide loss runs to their
  insureds within reasonable timeframes (varies by state)
- Loss runs are critical underwriting documents — multiple losses
  or large losses may make the risk unattractive to new carriers""",
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
