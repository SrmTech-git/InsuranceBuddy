"""One-off: enrich Batch 2 cards (ACORD 1-7, 11-13) with full descriptions.

Run from project root:
    python tools/_enrich_batch2.py

Idempotent — safe to re-run if the content needs tweaking.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "raw" / "forms" / "general"


def card(form_num, edition, title, policy_term, transaction_types, body):
    header = f"ACORD {form_num} ({edition}) — {title}"
    rule = "=" * len(header)
    return (
        f"{header}\n"
        f"{rule}\n"
        f"Form number: ACORD {form_num}\n"
        f"Edition: {edition}\n"
        f"Title: {title}\n"
        f"Type: Insurance form (ACORD industry standard)\n"
        f"States: All\n"
        f"Policy term: {policy_term}\n"
        f"Transaction types: {transaction_types}\n"
        f"\n"
        f"{body}\n"
    )


CARDS = {
    "ACORD 1 (2019-07) Property Loss Notice.txt": card(
        "1", "2019-07", "Property Loss Notice",
        "N/A (claim/loss event)",
        "N/A (loss notification)",
        """Purpose:
First Notice of Loss (FNOL) form for property claims. Provides the
carrier with the information needed to set up a claim file, assign
an adjuster, and begin investigating the loss.

Captures:
- Producer / agency information
- Insured name, address, contact
- Policy number, policy type, effective dates, deductible
- Loss date, time, and location
- Type of loss (fire, water, theft, vandalism, weather, etc.)
- Description of how the loss occurred
- Property damaged (building, contents, business personal property)
- Estimated dollar amount of loss
- Police / fire department report numbers
- Witness names and contact info
- Authority contacted (police, fire, etc.)
- Reporter name and relationship to insured
- Whether the property is occupied / vacant / under repair

When used:
- Reporting a property loss to the carrier
- Initial claim setup before adjuster assignment
- Submitted by the insured, agent, or adjuster

Notes:
- Some carriers accept ACORD 1 directly; others require their own
  proprietary FNOL form
- Used for residential and commercial property claims; commercial
  losses may require additional documentation (BI calculations,
  inventory schedules, etc.)"""
    ),

    "ACORD 2 (2019-07) Automobile Loss Notice.txt": card(
        "2", "2019-07", "Automobile Loss Notice",
        "N/A (claim/loss event)",
        "N/A (loss notification)",
        """Purpose:
First Notice of Loss (FNOL) form for automobile claims. Captures
the basic facts of an auto accident or loss so the carrier can
establish a claim, assign an adjuster, and begin investigation.

Captures:
- Producer / agency information
- Insured name, address, contact
- Policy number, policy type, effective dates, coverage details
  (liability limits, comp/coll deductibles, UM/UIM)
- Driver of insured vehicle (name, license, relationship to insured)
- Insured vehicle (year, make, model, VIN, plate, damage description)
- Loss date, time, and location
- How the accident occurred (description, diagram)
- Other vehicle(s) involved: owner, driver, vehicle info, insurance,
  damage description
- Injuries: names, contact, injury descriptions, medical providers
- Witnesses (names, contact)
- Police agency and report number, citations issued
- Towing, storage, and repair shop info

When used:
- Reporting an auto accident or loss to the carrier
- Initial claim setup before adjuster assignment
- Filed by the insured, driver, agent, or claims contact

Notes:
- Pairs with ACORD 11 (Auto Accident Information Form) and ACORD 12
  (Exchange of Information) for at-scene documentation
- Some carriers require their own FNOL form or online intake; ACORD 2
  is widely accepted but check carrier-specific requirements"""
    ),

    "ACORD 3 (2019-09) Liability Notice of Occurrence - Claim.txt": card(
        "3", "2019-09", "Liability Notice of Occurrence / Claim",
        "N/A (claim/loss event)",
        "N/A (loss notification)",
        """Purpose:
First Notice of Loss for general liability incidents — slips and
falls, product liability, premises injuries, third-party property
damage. Distinguishes between a notice of OCCURRENCE (potential
claim, no demand yet) and a CLAIM (formal demand received) so the
carrier can respond appropriately.

Captures:
- Producer / agency information
- Insured name, address, contact
- Policy number, policy type, effective dates, limits
- Notice type: occurrence vs. claim
- Date of occurrence, date insured received notice
- Location of occurrence
- Description of how the incident occurred
- Claimant information (name, address, contact, age, occupation)
- Description of injuries or damages alleged
- Property damaged (if applicable) and amount of damages
- Whether claimant is represented by attorney
- Suit / demand information if any
- Witnesses
- Authorities contacted (police, fire, OSHA, etc.)
- Other parties potentially responsible

When used:
- Reporting a GL occurrence or formal claim to the carrier
- Triggering carrier investigation and reservation of rights
- Filed promptly to avoid late-notice coverage issues

Notes:
- Timely notice is a coverage condition under most GL policies —
  ACORD 3 is often filed even when liability is unclear or contested
- The "Notice of Occurrence" path documents potential claims that
  haven't yet been formalized; useful for preserving coverage"""
    ),

    "ACORD 4 (2019-09) Workers Compensation – First Report of Injury or Illness.txt": card(
        "4", "2019-09", "Workers Compensation – First Report of Injury or Illness",
        "N/A (claim/loss event)",
        "N/A (workers compensation claim)",
        """Purpose:
First Report of Injury (FROI) for workers compensation claims.
Captures the employee, employer, and injury details needed to open
a WC claim and initiate medical and indemnity benefits.

Captures:
- Producer / agency information
- Employer name, address, FEIN, NAICS, SIC, location of incident
- WC carrier, policy number, effective dates
- Employee information: name, address, DOB, SSN, gender, marital
  status, dependents
- Employment details: hire date, occupation, department, employment
  status (full/part-time), wage information (rate and frequency),
  hours per day/week
- Injury details: date and time of injury, date employer notified,
  date of last day worked, location of injury, body part(s) affected,
  nature of injury, cause/source
- Description of how the injury occurred
- Whether the injury was witnessed; witness contact info
- Initial medical treatment: provider, date, hospital
- Whether the injury resulted in lost time, restricted duty, or
  fatality
- Authority contacted (police, OSHA, etc.)

When used:
- Reporting a workplace injury or occupational illness
- Filed promptly (often within 24-72 hours, varies by state)
- Submitted by employer, supervisor, or HR

Notes:
- Many states have their own jurisdictional First Report forms that
  must be used instead of (or in addition to) ACORD 4 — check state
  WC requirements before relying on ACORD 4 alone
- Time limits for filing vary by state and carrier; late filing can
  trigger employer penalties
- Pairs with subsequent forms during claim management (medical-only
  vs. lost-time tracking, return-to-work documentation, etc.)"""
    ),

    "ACORD 5 (2019-09) Aircraft Loss Notice.txt": card(
        "5", "2019-09", "Aircraft Loss Notice",
        "N/A (claim/loss event)",
        "N/A (loss notification)",
        """Purpose:
First Notice of Loss for aviation hull and/or liability claims.
Captures the facts of an aircraft incident or accident so the
carrier can begin claim handling and coordinate with the FAA, NTSB,
and other regulatory agencies as required.

Captures:
- Producer / agency information
- Named insured / aircraft owner / operator
- Policy number, policy type (hull, liability, both), effective
  dates, limits
- Aircraft information: registration (N-number), make, model, year,
  serial number, type of operation
- Pilot in command: name, license, ratings, total hours, hours in
  type, medical certificate
- Loss date, time, location (airport / off-airport)
- Phase of flight (taxi, takeoff, en route, approach, landing,
  parked, etc.)
- Description of the incident or accident
- Damage description (hull damage)
- Persons aboard, injuries, fatalities
- Cargo / property damage
- FAA and NTSB notification status
- Weather conditions, ATC contact
- Authorities contacted

When used:
- Reporting an aviation hull or liability loss
- Initial claim setup and regulatory coordination

Notes:
- Aviation losses typically trigger FAA and (for accidents) NTSB
  notification requirements separate from carrier reporting
- Often filed alongside ACORD 6 (Aviation Witness / Passenger
  Schedule) and ACORD 7 (Aviation Injured Schedule)"""
    ),

    "ACORD 6 (2009-05) Aviation Witness - Passenger Schedule.txt": card(
        "6", "2009-05", "Aviation Witness / Passenger Schedule",
        "N/A (incident document)",
        "N/A (claim documentation)",
        """Purpose:
Schedule of witnesses and/or passengers associated with an aviation
incident or accident. Provides contact information and brief
statements for each individual to support the carrier's
investigation and any subsequent claim handling.

Captures:
- Loss reference (date, location, aircraft N-number)
- For each witness or passenger:
  * Name
  * Address
  * Phone / contact information
  * Date of birth (passengers)
  * Relationship to flight (passenger, ground witness, crew, etc.)
  * Brief statement / observation
  * Whether the person was injured (and if so, refers to ACORD 7)

When used:
- Submitted alongside ACORD 5 (Aircraft Loss Notice) when there are
  passengers or witnesses to document
- Updated as additional witnesses are identified during investigation

Notes:
- Used for both accident scenes and incidents (e.g. hard landings,
  near-misses, ground events)
- Pairs with ACORD 7 for any individuals who suffered injuries"""
    ),

    "ACORD 7 (2009-05) Aviation Injured Schedule.txt": card(
        "7", "2009-05", "Aviation Injured Schedule",
        "N/A (incident document)",
        "N/A (claim documentation)",
        """Purpose:
Schedule of individuals injured in an aviation incident or accident.
Captures injury details, medical providers, and treatment information
to support claim handling and coverage analysis under aviation
liability and medical payments coverages.

Captures:
- Loss reference (date, location, aircraft N-number)
- For each injured person:
  * Name, address, contact, date of birth
  * Relationship to flight (passenger, crew, third party, ground)
  * Description of injuries (body parts, severity)
  * Whether the person was hospitalized
  * Hospital / medical provider name and contact
  * Initial diagnosis or treatment
  * Whether attorney representation has been retained
  * Status (alive, deceased, transferred, etc.)

When used:
- Submitted alongside ACORD 5 (Aircraft Loss Notice) and ACORD 6
  (Witness / Passenger Schedule) when there are injuries
- Updated as additional medical information becomes available

Notes:
- Triggers medical payments coverage analysis under aviation
  liability policies
- Typically used in conjunction with formal claim files maintained
  by the aviation adjuster or specialty TPA"""
    ),

    "ACORD 11 (1995-02) Auto Accident Information Form.txt": card(
        "11", "1995-02", "Auto Accident Information Form",
        "N/A (incident document)",
        "N/A (claim documentation)",
        """Purpose:
At-scene information form for drivers and passengers to capture
the facts of an auto accident immediately after it occurs. Designed
for use in the field — typically kept in glove boxes or claim
intake kits. Provides the raw data that later feeds into the formal
ACORD 2 (Automobile Loss Notice) when the claim is filed.

Captures:
- Date, time, and location of accident
- Weather, road, and visibility conditions
- Diagram of the accident (basic field for sketching)
- Description of how the accident occurred
- For each vehicle involved:
  * Year, make, model, color
  * Plate number, state
  * VIN
  * Damage description
- For each driver:
  * Name, address, phone
  * Driver's license number and state
  * Insurance company and policy number
- Passenger names and contact
- Witness names and contact
- Police agency, badge number, report number
- Citations issued (if any)
- Injuries (yes/no, who, where transported)

When used:
- At the scene of an auto accident, by drivers or passengers
- Pre-claim documentation; data later transferred to ACORD 2 for
  formal claim filing

Notes:
- Edition is from 1995 and reflects pre-digital field documentation
  practices; many carriers now offer mobile app intake for the same
  purpose
- Pairs with ACORD 12 (Exchange of Information) for sharing details
  between drivers, and ACORD 13 (Witness Card) for witness statements
- Glove-box reference; not a formal claim filing"""
    ),

    "ACORD 12 (1995-02) Exchange of Information Form.txt": card(
        "12", "1995-02", "Exchange of Information Form",
        "N/A (incident document)",
        "N/A (claim documentation)",
        """Purpose:
Two-party information exchange form for drivers involved in an auto
accident. Each driver fills out their side; the forms are exchanged
so that both parties leave the scene with the other's identity,
insurance, and contact info — the minimum needed to file claims with
each other's carriers.

Captures:
- Driver name, address, phone, email
- Driver's license number and state
- Vehicle year, make, model, plate, state, VIN
- Vehicle owner (if different from driver)
- Insurance company name and policy number
- Insurance company phone / claims number
- Producer / agency name and contact
- Brief description of damage to driver's vehicle

When used:
- At the scene of an auto accident, exchanged between drivers
- Replaces ad-hoc napkin scribbles with a standardized minimum
  data set

Notes:
- Edition is from 1995; widely superseded by smartphone photos of
  insurance cards and licenses, but still seen in glove-box kits
- Complements ACORD 11 (Auto Accident Information Form) which
  captures broader scene details"""
    ),

    "ACORD 13 (1995-02) Witness Card.txt": card(
        "13", "1995-02", "Witness Card",
        "N/A (incident document)",
        "N/A (claim documentation)",
        """Purpose:
Pocket-sized card for capturing a witness's identity, contact
information, and brief statement at the scene of an accident or
incident. Designed to be filled out quickly while the witness is
still present and willing to provide information.

Captures:
- Witness name
- Address
- Phone (home, work, cell)
- Email (where applicable)
- Brief statement of what the witness observed
- Date, time, and location of the incident witnessed
- Reporter name (who collected the statement)

When used:
- At the scene of an auto accident or other incident
- Adjuster or claim investigator field tool
- Insured field documentation when collecting witnesses' info

Notes:
- Edition is from 1995; the compact card format reflects pre-digital
  field practices but remains useful for quick witness intake
- Witness statements gathered via ACORD 13 are typically supplemented
  later with full recorded statements during formal investigation"""
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
