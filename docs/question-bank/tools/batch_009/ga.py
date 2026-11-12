"""Writes batches/parts/BATCH_009_GA.json: the 149 General Awareness questions of BATCH_009.

Same structure as tools/batch_008/ga.py. Current-affairs topics (National and International Current Affairs,
Appointments, Awards, Sports, Summits, Economic Affairs, Business) test events dated 2025-11-01 to 2026-11-04 with
event dates from the sources; every such question carries current_affairs {event_date, review_by 2027-05-05}. Other
time-sensitive facts (schemes, policies, reports, books, current heads) carry current_affairs too. Where a source gives
no exact day, ca(..., inferred=reason) records it and the list is printed and written into the batch notes.

Every question has fact_checks, and at least one source per question is an official/primary site or a major news
outlet (never only Wikipedia or an exam-prep site). Each URL is marked OPENED (fetched and read, giving
"web:fact-check") or SEARCH (confirmed only from search-result text, giving "web:search-confirmed"). checked_on is the
date the page was actually checked (2026-11-06). Sites that refused or failed a fetch (e.g. presidentofindia.gov.in, deccanherald.com,
niti.gov.in PDFs, unep.org, britannica.com, opec.org, nasaspaceflight.com, tcs.com PDFs, data.iwc.int)
were not worked around.
Explanations and why_others_wrong state only facts backed by the listed sources, or stay neutral.

All earlier GA stems (and the Banking subject's BFA stems) (BATCH_000 sample, BATCH_001_GA to BATCH_008_GA, 1,202 questions) were read first; no fact or
event tested there is tested again, and no event is used twice in this batch.

Statement questions have their key fixed by the statements (computed from truth values); other questions are written
with the correct option first and answer "*", and are then placed so that keys are balanced A to D.

    python tools/batch_009/ga.py
"""

import json
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-05"
REVIEW_BY = "2027-05-05"
CA_FROM, CA_TO = "2025-11-01", "2026-11-04"
LETTERS = "ABCD"
GA = "General Awareness and Current Affairs"
BATCH = "BATCH_009"
SECONDS = {"Basic": 15, "Intermediate": 25, "Advanced": 45}
CA_TOPICS = {"National Current Affairs", "International Current Affairs", "Important Appointments",
             "Awards and Honours", "Sports", "Summits and Conferences", "Economic Affairs",
             "Business and Corporate News"}

S12 = ["Only 1", "Only 2", "Both 1 and 2", "Neither 1 nor 2"]
S123 = ["1 and 2 only", "2 and 3 only", "1 and 3 only", "1, 2 and 3"]
KEY12 = {(True, False): "A", (False, True): "B", (True, True): "C", (False, False): "D"}
KEY123 = {(True, True, False): "A", (False, True, True): "B", (True, False, True): "C", (True, True, True): "D"}

QUESTIONS = []
OPENED, SEARCH = "opened", "search"


INFERRED = []


def ca(event_date, inferred=None):
    """inferred: short reason when the exact day is not stated by the source (listed in the report)."""
    if inferred:
        INFERRED.append((event_date, inferred))
    return {"event_date": event_date, "review_by": REVIEW_BY}


def stmt(about, statements, truth):
    """Build a statement question; the key is computed from the truth values, so it cannot drift."""
    lines = [f"Consider the following statements about {about}:"]
    lines += [f"{i + 1}. {s}" for i, s in enumerate(statements)]
    lines.append("Which of the statements given above is/are correct?")
    if len(statements) == 2:
        return "\n".join(lines), list(S12), KEY12[tuple(truth)]
    assert len(statements) == 3 and tuple(truth) in KEY123, (about, truth)
    return "\n".join(lines), list(S123), KEY123[tuple(truth)]


def G(topic, subtopic, difficulty, text, options, answer, concept, explanation, steps, facts,
      why=None, shortcut=None, current=None):
    assert len(options) == 4 and len(set(options)) == 4, text
    assert answer == "*" or answer in LETTERS, answer
    assert facts and why, text
    if topic in CA_TOPICS:
        assert current and CA_FROM <= current["event_date"] <= CA_TO, (text, current)
    if current:
        assert CA_FROM <= current["event_date"] <= CA_TO or topic not in CA_TOPICS, (text, current)
    QUESTIONS.append(dict(topic=topic, subtopic=subtopic, difficulty=difficulty, text=text, options=list(options),
                          answer=answer, concept=concept, explanation=explanation, steps=steps, facts=facts,
                          why=why, shortcut=shortcut, current=current))


def GS(topic, subtopic, difficulty, about, statements, truth, concept, explanation, facts, why, current=None,
       shortcut=None):
    text, options, key = stmt(about, statements, truth)
    steps = [f"{i + 1}: {'correct' if t else 'incorrect'}" for i, t in enumerate(truth)]
    steps.append("So " + options[LETTERS.index(key)])
    G(topic, subtopic, difficulty, text, options, key, concept, explanation, steps, facts, why=why,
      shortcut=shortcut, current=current)


# ====================================================================== sources
# key: (url, how) or (url, how, "YYYY-MM-DD" date the page/search was actually checked; default CHECKED)
CHECKED = "2026-11-06"
U = {}

def fact(claim, key):
    url, how, *day = U[key]
    return {"claim": claim, "source_url": url, "checked_on": day[0] if day else CHECKED, "_how": how}

AI_CHECK = ['ai:independent-check']
# reworded after the independent key-free check; re-solved by the author instead
REWORDED_AFTER_CHECK = []


# ###################################################################### part: nat (national CA)
# ###################################################################### part: nat (National Current Affairs)
U.update({
    # ---- Government decisions
    "nat9_da_air": ("https://newsonair.gov.in/cabinet-approves-scheme-worth-rs-10000-cr-to-promote-domestic-manufacturing/",
                    OPENED),
    "nat9_hpcl_dd": ("https://ddnews.gov.in/en/cabinet-approves-cost-revision-for-hpcl-rajasthan-refinery-project-boosts-"
                     "equity-infusion/", OPENED),
    "nat9_tun_dd": ("https://ddnews.gov.in/en/cabinet-approves-%E2%82%B96969-67-crore-tunnel-project-to-link-dwarka-"
                    "expressway-with-vasant-kunj/", OPENED),
    "nat9_odi_dd": ("https://ddnews.gov.in/en/cabinet-approves-%E2%82%B98300-crore-coastal-highway-project-between-"
                    "rameshwar-and-paradeep-in-odisha/", OPENED),
    # ---- States and UTs
    "nat9_cbdc_air": ("https://newsonair.gov.in/hm-amit-shah-launches-countrys-first-central-banks-digital-currency-to-"
                      "bring-transparency-in-the-delivery-mechanism/", OPENED),
    "nat9_iairo_tr": ("https://www.tribuneindia.com/news/business/indian-ai-research-organization-to-be-established-in-"
                      "gift-city-gandhinagar/", OPENED),
    "nat9_iairo_dh": ("https://www.deccanherald.com/india/gujarat/gujarat-govt-grants-approval-to-establish-indian-ai-"
                      "research-organization-in-gandhinagars-gift-city-3846742", SEARCH),
    "nat9_heli_air": ("https://newsonair.gov.in/cm-samrat-choudhary-launches-bihar-heli-tourism-scheme/", OPENED),
    "nat9_rrts_dd": ("https://ddnews.gov.in/en/pm-modi-inaugurates-indias-first-namo-bharat-rrts-dedicates-delhi-meerut-"
                     "corridor-to-nation/", OPENED),
    "nat9_pbcs_air": ("https://newsonair.gov.in/punjab-launches-first-ever-caste-socio-economic-survey/", OPENED),
    # ---- Defence
    "nat9_alh_ians": ("https://ianslive.in/govt-signs-rs-5083-crore-deals-to-acquire-helicopters-for-coast-guards-"
                      "missiles-for-navy--20260303154758", OPENED),
    "nat9_alh_etv": ("https://www.etvbharat.com/en/bharat/defence-ministry-deal-with-hindustan-aeronautics-ltd-for-"
                     "acquisition-of-six-advanced-light-helicopters-enn26030303555", SEARCH),
    "nat9_idsa_sep": ("https://idsa.in/wp-content/uploads/2024/06/Defence-Newsletter-September-2026.pdf", OPENED),
    "nat9_saaw_air": ("https://newsonair.gov.in/defence-ministry-signs-over-%E2%82%B9810-crore-contract-with-bdl-for-160-"
                      "sat-saaw-systems/", SEARCH),
    "nat9_idsa_aug": ("https://idsa.in/wp-content/uploads/2024/06/Defence-Newsletter-August-2026.pdf", OPENED),
    "nat9_mq9_tp": ("https://theprint.in/india/mod-inks-pact-with-general-atomics-to-lease-2-mq-9b-sea-guardian-unmanned-"
                    "aircraft/3017207/", SEARCH),
    "nat9_vp_air": ("https://www.newsonair.gov.in/16th-edition-of-joint-special-forces-exercise-vajra-prahar-between-"
                    "india-us-begins-today", OPENED),
    "nat9_vp_na": ("https://newsarenaindia.com/defence-and-security/india-us-special-forces-exercise-vajra-prahar-to-"
                   "begin-tomorrow/70564", OPENED),
    "nat9_idsa_jun": ("https://idsa.in/wp-content/uploads/2024/06/Defence-Newsletter-June-2026.pdf", OPENED),
    "nat9_netra_dp": ("https://dailypioneer.com/news/drdo-hands-over-foc-for-netra-aew-amp-c-system-to-indian-air-force",
                      OPENED),
    "nat9_nip_air": ("https://newsonair.gov.in/indian-navy-commissions-ins-nipun-at-naval-dockyard-mumbai/", OPENED),
    "nat9_dp_air": ("https://newsonair.gov.in/defence-minister-rajnath-singh-announces-record-defence-production-of-"
                    "%E2%82%B91-78-lakh-crore-in-fy-2025-26/", OPENED),
})

T = "National Current Affairs"
GOV, ST, DEF = "Government decisions", "States and UTs", "Defence"

# ------------------------------------------------------------------ National CA: Basic (4)
G(T, ST, "Basic",
  "India's first Namo Bharat Regional Rapid Transit System (RRTS), an 82 km corridor dedicated to the nation by the "
  "Prime Minister in February 2026, links Delhi with which city?",
  ["Meerut", "Panipat", "Alwar", "Agra"], "*",
  "Infrastructure: regional rapid transit",
  "On 22 February 2026 the Prime Minister inaugurated India's first Namo Bharat RRTS and dedicated the 82 km "
  "Delhi-Meerut Namo Bharat Corridor to the nation at Meerut. The Meerut Metro was launched at the same time and runs "
  "on the same tracks and stations as the Namo Bharat trains.",
  ["Namo Bharat RRTS: Delhi-Meerut, 82 km", "Inaugurated 22 Feb 2026; Meerut Metro shares its tracks and stations"],
  [fact("PM inaugurated India's first Namo Bharat RRTS and dedicated the 82-km Delhi-Meerut corridor on Sunday (22 Feb "
        "2026); Meerut Metro launched from the same platform, sharing tracks and stations", "nat9_rrts_dd")],
  why="The source names the Delhi-Meerut corridor; the other cities are not part of it.",
  current=ca("2026-02-22"))

G(T, ST, "Basic",
  "The first phase of the Bihar Heli Tourism and Air Tourism Service Scheme, launched by Chief Minister Samrat "
  "Choudhary in July 2026, covers Patna, Valmikinagar, Maa Mundeshwari and which other destination?",
  ["Rajgir", "Bodh Gaya", "Vaishali", "Vikramshila"], "*",
  "State initiatives: tourism",
  "Chief Minister Samrat Choudhary launched the scheme at a function in Patna and opened its online booking portal. "
  "The first phase covers Patna, Valmikinagar, Maa Mundeshwari and Rajgir, with helicopter rides every Saturday and "
  "Sunday from 18 July; the State subsidises up to ₹15,422 per ticket.",
  ["Phase 1: Patna, Valmikinagar, Maa Mundeshwari, Rajgir", "Subsidy up to ₹15,422 per ticket; weekend flights"],
  [fact("CM Samrat Choudhary launched the Bihar Heli Tourism and Air Tourism Service Scheme in Patna; first phase "
        "Patna, Valmikinagar, Maa Mundeshwari and Rajgir; subsidy up to ₹15,422 per ticket (AIR, 13 July 2026)",
        "nat9_heli_air")],
  why="The source lists Rajgir; Bodh Gaya, Vaishali and Vikramshila are not in the first phase.",
  current=ca("2026-07-13", inferred="AIR report dated 13 July 2026 gives no separate launch date"))

G(T, DEF, "Basic",
  "In June 2026 DRDO handed over the Final Operational Clearance (FOC) certificate of the indigenous 'Netra' system to "
  "the Indian Air Force. What is Netra?",
  ["Airborne Early Warning and Control system", "Long-range surface-to-air missile system",
   "Anti-drone electronic warfare system", "Satellite-based navigation system"], "*",
  "Defence: inductions and clearances",
  "On 25 June 2026 DRDO handed over the FOC certificate of the indigenous Netra Airborne Early Warning and Control "
  "(AEW&C) system to the IAF at Bengaluru. Netra had received its Initial Operational Clearance in 2017.",
  ["Netra = AEW&C", "FOC handed over 25 June 2026; IOC in 2017"],
  [fact("DRDO handed over the FOC certificate of the indigenous Netra AEW&C system to the IAF on 25 June 2026; IOC was "
        "given in 2017", "nat9_idsa_jun"),
   fact("FOC for Netra AEW&C handed over in Bengaluru, presided over by Deputy Chief of the Air Staff Air Marshal "
        "Awadhesh Kumar Bharti; IOC in 2017", "nat9_netra_dp")],
  why="The sources describe Netra as an AEW&C system, not a missile, anti-drone or navigation system.",
  current=ca("2026-06-25"))

G(T, DEF, "Basic",
  "INS Nipun, commissioned into the Indian Navy at Naval Dockyard, Mumbai, on 31 August 2026, is the second Diving "
  "Support Vessel of which class?",
  ["Nistar class", "Mahe class", "Nilgiri class", "Arnala class"], "*",
  "Navy: commissioning",
  "INS Nipun, designed and built by Hindustan Shipyard Limited, Visakhapatnam, is the second Diving Support Vessel of "
  "the Nistar class. It is a dedicated diving support and submarine rescue ship and will strengthen the Western Naval "
  "Command's underwater operations.",
  ["INS Nipun: 2nd Nistar-class DSV", "Commissioned 31 Aug 2026, Mumbai; built by HSL"],
  [fact("INS Nipun, the second Diving Support Vessel of the Nistar class, built by Hindustan Shipyard Limited, "
        "commissioned at Naval Dockyard, Mumbai (AIR, 31 Aug 2026)", "nat9_nip_air"),
   fact("Indian Navy commissioned INS Nipun, second DSV of the Nistar class, at Mumbai on 31 August 2026",
        "nat9_idsa_aug")],
  why="The sources place INS Nipun in the Nistar class; the other classes are not diving support vessels.",
  current=ca("2026-08-31"))

# ------------------------------------------------------------------ National CA: Intermediate (11)
G(T, GOV, "Intermediate",
  "The 3% increase in Dearness Allowance for Central Government employees and Dearness Relief for pensioners, "
  "approved by the Union Cabinet in October 2026, takes effect from which date?",
  ["1 July 2026", "1 January 2026", "1 April 2026", "1 October 2026"], "*",
  "Cabinet decisions: DA/DR",
  "The Union Cabinet approved a 3% rise in DA and DR effective 1 July 2026. It benefits over 48 lakh employees and 68 "
  "lakh pensioners, with a combined annual cost of over ₹10,000 crore.",
  ["DA/DR +3%, effective 1 July 2026", "48 lakh employees, 68 lakh pensioners; over ₹10,000 crore a year"],
  [fact("Cabinet approved 3% DA/DR increase effective 1 July 2026 for over 48 lakh employees and 68 lakh pensioners; "
        "annual impact over ₹10,000 crore (AIR, 29 Oct 2026)", "nat9_da_air")],
  why="The source gives 1 July 2026 as the effective date; the other dates are not mentioned.",
  current=ca("2026-10-29", inferred="AIR report dated 29 Oct 2026 does not state the Cabinet meeting date"))

G(T, GOV, "Intermediate",
  "In April 2026 the Cabinet Committee on Economic Affairs revised the cost of HPCL's 9 MMTPA greenfield refinery-cum-"
  "petrochemical complex at Pachpadra, Balotra district, Rajasthan. What is the revised project cost?",
  ["₹79,459 crore", "₹43,129 crore", "₹19,600 crore", "₹8,962 crore"], "*",
  "Cabinet decisions: energy projects",
  "The CCEA raised the cost of the HPCL Rajasthan refinery from ₹43,129 crore to ₹79,459 crore and approved an "
  "additional HPCL equity infusion of ₹8,962 crore, taking HPCL's total equity in the project to ₹19,600 crore.",
  ["Original ₹43,129 cr -> revised ₹79,459 cr", "Extra HPCL equity ₹8,962 cr; total HPCL equity ₹19,600 cr"],
  [fact("Cost of the 9 MMTPA HPCL refinery at Pachpadra, Balotra, revised from ₹43,129 crore to ₹79,459 crore; extra "
        "equity ₹8,962 crore; total HPCL equity ₹19,600 crore (DD News, 8 April 2026)", "nat9_hpcl_dd")],
  why="₹43,129 crore was the original cost; ₹19,600 crore and ₹8,962 crore are HPCL equity figures.",
  current=ca("2026-04-08"))

G(T, GOV, "Intermediate",
  "The ₹6,969.67 crore project approved by the CCEA on 1 July 2026, with a 3.14 km twin-tube road tunnel linking "
  "Dwarka Expressway with Nelson Mandela Marg at Vasant Kunj, Delhi, is to be built under which mode?",
  ["Hybrid Annuity Mode", "Build-Operate-Transfer (Toll) mode", "Engineering, Procurement and Construction mode",
   "Toll-Operate-Transfer mode"], "*",
  "Cabinet decisions: urban roads",
  "The CCEA approved the 8.1 km project, including a 3.14 km six-lane twin-tube tunnel built with tunnel boring "
  "machines, about 1.98 km of it under the Ridge area. It will be built in Hybrid Annuity Mode under the National "
  "Highways (Original) scheme.",
  ["Cost ₹6,969.67 crore; 8.1 km; 3.14 km tunnel", "Mode: Hybrid Annuity"],
  [fact("CCEA approved on 1 July 2026 the ₹6,969.67 crore project with a 3.14 km twin-tube six-lane tunnel linking "
        "Dwarka Expressway with Nelson Mandela Marg, in Hybrid Annuity Mode", "nat9_tun_dd")],
  why="The source says Hybrid Annuity Mode; the other modes are not used for this project.",
  current=ca("2026-07-01"))

G(T, ST, "Intermediate",
  "In February 2026 Gujarat became the first state to transfer Public Distribution System (PDS) subsidies using an "
  "RBI-authorised Central Bank Digital Currency, in a pilot covering over 26,000 families in four districts. Which of "
  "the following districts is NOT part of this pilot?",
  ["Rajkot", "Ahmedabad", "Surat", "Valsad"], "*",
  "State firsts: PDS delivery",
  "Union Home Minister Amit Shah launched the country's first CBDC-based PDS at Mahatma Mandir, Gandhinagar. "
  "Beneficiaries get digital wallet tokens showing item, quantity and price and collect rations using QR codes or "
  "OTPs; the pilot covers over 26,000 families in Ahmedabad, Surat, Anand and Valsad.",
  ["Gujarat: first CBDC-based PDS", "Pilot districts: Ahmedabad, Surat, Anand, Valsad", "Rajkot is not listed"],
  [fact("Gujarat first state to transfer PDS subsidies using RBI-authorised CBDC; launched by Amit Shah at Mahatma "
        "Mandir, Gandhinagar; pilot over 26,000 families in Ahmedabad, Surat, Anand, Valsad (AIR, 15 Feb 2026)",
        "nat9_cbdc_air")],
  why="The source lists Ahmedabad, Surat, Anand and Valsad as the pilot districts; Rajkot is not among them.",
  current=ca("2026-02-15", inferred="AIR report dated 15 Feb 2026 gives no separate launch date"))

G(T, ST, "Intermediate",
  "The Indian AI Research Organisation (IAIRO) at GIFT City, Gandhinagar, set up by Gujarat from 1 January 2026 under "
  "a tripartite PPP model with the Central Government, has which body as its anchor private partner?",
  ["Indian Pharmaceutical Alliance", "NASSCOM", "Confederation of Indian Industry", "Internet and Mobile Association of India"],
  "*",
  "State initiatives: artificial intelligence",
  "Chief Minister Bhupendra Patel gave in-principle approval to IAIRO, a Section 8 non-profit run through an SPV from "
  "1 January 2026. Its budget of about ₹300 crore over five years is shared equally by the State, the Centre and the "
  "private partner, the Indian Pharmaceutical Alliance (about 23 pharma companies). Gujarat said it was the first "
  "state to set up IAIRO under the PPP model.",
  ["IAIRO: GIFT City; State + Centre + Indian Pharmaceutical Alliance", "About ₹300 crore over 5 years, one-third each"],
  [fact("IAIRO set up through a tripartite partnership of the Gujarat government, the Government of India and the "
        "Indian Pharmaceutical Alliance as anchor private partner; operational as an SPV from 1 January 2026; about "
        "₹300 crore over five years (ANI via Tribune, 30 Dec 2025)", "nat9_iairo_tr"),
   fact("Gujarat government grants approval to establish Indian AI Research Organization in GIFT City",
        "nat9_iairo_dh")],
  why="The source names the Indian Pharmaceutical Alliance; the other industry bodies are not partners.",
  current=ca("2025-12-30", inferred="ANI report of 30 Dec 2025 does not give the exact approval day"))

G(T, ST, "Intermediate",
  "Punjab began its first-ever caste socio-economic survey on 1 April 2026, with about 28,000 enumerators collecting "
  "data across the State. What budget has been set for the survey?",
  ["₹250 crore", "₹500 crore", "₹150 crore", "₹1,000 crore"], "*",
  "State initiatives: surveys",
  "Punjab's first caste socio-economic survey aims to assess the living standards of all communities while keeping the "
  "data confidential. It has a budget of ₹250 crore, uses about 28,000 enumerators and is expected to take about "
  "three months.",
  ["Budget ₹250 crore; 28,000 enumerators", "Started 1 April 2026; about three months"],
  [fact("Punjab launched its first-ever caste socio-economic survey (on 1 April 2026, 'yesterday' in the AIR report of "
        "2 April); budget ₹250 crore; 28,000 enumerators; likely completed in three months", "nat9_pbcs_air")],
  why="The source gives ₹250 crore; the other amounts are not mentioned.",
  current=ca("2026-04-01"))

G(T, DEF, "Intermediate",
  "On 3 March 2026 the Ministry of Defence signed contracts worth ₹5,083 crore, including six ALH Mk-III helicopters "
  "for the Coast Guard from HAL. The other contract, worth ₹2,182 crore with Russia's Rosoboronexport, is for which "
  "missiles for the Indian Navy?",
  ["Vertical Launch Shtil surface-to-air missiles", "BrahMos supersonic cruise missiles",
   "Barak-8 long-range surface-to-air missiles", "Klub-S submarine-launched cruise missiles"], "*",
  "Defence contracts",
  "In the presence of Defence Secretary Rajesh Kumar Singh at South Block, the MoD signed a ₹2,901 crore contract with "
  "HAL for six ALH Mk-III (maritime role) helicopters for the Indian Coast Guard under Buy (Indian-IDDM), and a ₹2,182 "
  "crore contract with JSC Rosoboronexport for Surface-to-Air Vertical Launch Shtil missiles for the Navy's frontline "
  "warships.",
  ["HAL: 6 ALH Mk-III (MR), ₹2,901 cr, Coast Guard", "Rosoboronexport: VL-Shtil missiles, ₹2,182 cr, Navy"],
  [fact("Contracts of ₹5,083 crore on 3 March 2026: ₹2,901 crore with HAL for six ALH Mk-III for the Coast Guard; "
        "₹2,182 crore with JSC Rosoboronexport for Surface-to-Air Vertical Launch Shtil missiles for the Navy",
        "nat9_alh_ians"),
   fact("Defence Ministry deal with HAL for acquisition of six Advanced Light Helicopters", "nat9_alh_etv")],
  why="The source names VL-Shtil missiles from Rosoboronexport; the other missiles are not part of this contract.",
  current=ca("2026-03-03"))

G(T, DEF, "Intermediate",
  "On 23 September 2026 the Ministry of Defence signed an ₹810.79 crore contract for 160 Satellite Smart Anti-Airfield "
  "Weapons (SAT-SAAW) for the Indian Air Force with which company?",
  ["Bharat Dynamics Limited", "Bharat Electronics Limited", "Hindustan Aeronautics Limited", "Munitions India Limited"],
  "*",
  "Defence contracts",
  "The MoD contracted Bharat Dynamics Limited for 160 SAT-SAAW and associated equipment under Buy (Indian-IDDM), with "
  "60% indigenous content. SAT-SAAW is an air-to-ground precision-guided glide bomb that can be launched from Jaguar, "
  "Hawk and Su-30MKI aircraft.",
  ["160 SAT-SAAW, ₹810.79 crore, BDL", "Glide bomb for Jaguar, Hawk, Su-30MKI; 60% indigenous"],
  [fact("MoD signed a contract with Bharat Dynamics Limited for 160 SAT-SAAW for the IAF at ₹810.79 crore under "
        "Buy (Indian-IDDM) on 23 September 2026; glide bomb launched from Jaguar, Hawk and Su-30MKI", "nat9_idsa_sep"),
   fact("Defence Ministry signs over ₹810 crore contract with BDL for 160 SAT-SAAW systems (AIR, 23 Sep 2026)",
        "nat9_saaw_air")],
  why="The sources name Bharat Dynamics Limited as the supplier, not the other public sector firms.",
  current=ca("2026-09-23"))

G(T, DEF, "Intermediate",
  "In August 2026 the Ministry of Defence signed a contract of about ₹1,943 crore with General Atomics Aeronautical "
  "Systems to lease two MQ-9B Sea Guardian remotely piloted aircraft for the Indian Navy. For what period is the lease?",
  ["30 months", "12 months", "24 months", "60 months"], "*",
  "Defence contracts",
  "The contract, signed on 17 August 2026, is for leasing two MQ-9B Sea Guardian High-Altitude Long-Endurance RPAS for "
  "the Indian Navy for 30 months.",
  ["2 MQ-9B Sea Guardians on lease, ₹1,943 crore", "Lease period: 30 months; signed 17 Aug 2026"],
  [fact("MoD signed a contract on 17 August 2026 with GA-ASI for leasing two MQ-9B Sea Guardian HALE RPAS for the "
        "Indian Navy for 30 months; about ₹1,943 crore", "nat9_idsa_aug"),
   fact("MoD inks pact with General Atomics to lease 2 MQ-9B Sea Guardian unmanned aircraft", "nat9_mq9_tp")],
  why="The sources give a 30-month lease; the other periods are not mentioned.",
  current=ca("2026-08-17"))

G(T, DEF, "Intermediate",
  "The 16th edition of the India-US Joint Special Forces Exercise Vajra Prahar began at the Special Forces Training "
  "School, Bakloh (Himachal Pradesh), on 24 February 2026. The US contingent was drawn from which unit?",
  ["Green Berets", "Navy SEALs", "Delta Force", "Marine Raiders"], "*",
  "Defence exercises in India",
  "According to the Defence Ministry, 45 personnel from Indian Army Special Forces units and 12 personnel from the "
  "Green Berets of the US Special Forces took part in Vajra Prahar 2026 at Bakloh, aimed at interoperability, "
  "jointness and exchange of special operations tactics.",
  ["Vajra Prahar 2026: 16th edition, Bakloh", "India 45 SF personnel; US 12 Green Berets"],
  [fact("16th Vajra Prahar began 24 Feb 2026 at SFTS Bakloh; Indian Army 45 Special Forces personnel; US 12 personnel "
        "from the Green Berets", "nat9_vp_air"),
   fact("16th edition of Vajra Prahar at Special Forces Training School, Bakloh, Himachal Pradesh", "nat9_vp_na")],
  why="The source says the US personnel were from the Green Berets; the other units are not mentioned.",
  current=ca("2026-02-24"))

G(T, DEF, "Intermediate",
  "ICGS Akshay, commissioned into the Indian Coast Guard at Goa Shipyard Limited, Goa, on 27 June 2026, is a vessel of "
  "which type?",
  ["Fast Patrol Vessel", "Offshore Patrol Vessel", "Pollution Control Vessel", "Air Cushion Vehicle"], "*",
  "Coast Guard: commissioning",
  "The Coast Guard commissioned ICGS Akshay, a new-generation Fast Patrol Vessel, at Goa Shipyard Limited on 27 June "
  "2026. It is meant for maritime law enforcement, coastal security, search and rescue and marine environmental "
  "protection.",
  ["ICGS Akshay: new-generation Fast Patrol Vessel", "Commissioned 27 June 2026 at Goa Shipyard"],
  [fact("ICGS Akshay, a new-generation Fast Patrol Vessel, commissioned at Goa Shipyard Limited, Goa, on 27 June 2026",
        "nat9_idsa_jun")],
  why="The source describes ICGS Akshay as a Fast Patrol Vessel, not the other vessel types.",
  current=ca("2026-06-27"))

# ------------------------------------------------------------------ National CA: Advanced (2)
GS(T, GOV, "Advanced",
   "the Rameshwar-Paradeep coastal highway project in Odisha approved by the Cabinet Committee on Economic Affairs on "
   "3 June 2026",
   ["It will cost about ₹8,300.79 crore and is to be built under the Hybrid Annuity Model.",
    "The entire 160 km stretch from Rameshwar to Paradeep is to be a four-lane access-controlled highway.",
    "It passes through Khurda, Puri, Kendrapada and Jagatsinghpur districts."],
   [True, False, True],
   "Cabinet decisions: highways",
   "The CCEA approved the about 160.18 km project at ₹8,300.79 crore under HAM. Only Package 1 (Rameshwar-Konark, 79.4 "
   "km) is a four-lane access-controlled highway; Package 2 (Konark-Paradeep, 80.78 km) is two-lane with paved "
   "shoulders. It covers Khurda, Puri, Kendrapada and Jagatsinghpur districts and is expected to save nearly 2.5 hours.",
   [fact("CCEA approved on 3 June 2026 the ₹8,300.79 crore, about 160.18 km Rameshwar-Paradeep highway under HAM; "
         "Rameshwar-Konark 79.4 km four-lane access-controlled; Konark-Paradeep 80.78 km two-lane with paved shoulders; "
         "districts Khurda, Puri, Kendrapada, Jagatsinghpur", "nat9_odi_dd")],
   why="Statement 2 is wrong: only the Rameshwar-Konark package is four-lane; Konark-Paradeep is two-lane with paved "
       "shoulders.",
   current=ca("2026-06-03"))

GS(T, DEF, "Advanced",
   "India's defence production in 2025-26, announced by Defence Minister Rajnath Singh in June 2026",
   ["It reached a record ₹1.78 lakh crore, 15.6% higher than ₹1.54 lakh crore in 2024-25.",
    "It was about 110% higher than in 2020-21, when production was just over ₹84,000 crore.",
    "Defence Public Sector Undertakings accounted for less than half of the total production."],
   [True, True, False],
   "Defence production",
   "Defence production rose to an all-time high of ₹1.78 lakh crore in 2025-26, up 15.6% from ₹1.54 lakh crore, and "
   "about 110% above the 2020-21 level of just over ₹84,000 crore. At the annual review of 16 DPSUs on 1 September 2026, "
   "the Raksha Mantri noted that DPSUs contributed ₹1.29 lakh crore of the roughly ₹1.8 lakh crore produced, well over "
   "half.",
   [fact("Record defence production of ₹1.78 lakh crore in FY 2025-26, up 15.6% from ₹1.54 lakh crore; 110% rise from "
         "just over ₹84 thousand crore in FY 2020-21 (AIR, 17 June 2026)", "nat9_dp_air"),
    fact("Defence production about ₹1.8 lakh crore in 2025-26, with DPSUs contributing ₹1.29 lakh crore (review of 16 "
         "DPSUs, 1 Sep 2026)", "nat9_idsa_sep"),
    fact("Annual defence production at an all-time high of ₹1.78 lakh crore in FY 2025-26, 15.6% above ₹1.54 lakh crore",
         "nat9_idsa_jun")],
   why="Statement 3 is wrong: DPSUs contributed ₹1.29 lakh crore of about ₹1.8 lakh crore, i.e. well over half.",
   current=ca("2026-06-17"))

# ###################################################################### part: intl (international CA)
# ###################################################################### part: intl (International Current Affairs)
U.update({
    # ---- Bilateral relations / India abroad
    "intl_pb_air": ("https://newsonair.gov.in/iaf-to-start-exercise-pitch-black-2026-tomorrow-in-australia/", OPENED),
    "intl_pb_week": ("https://www.theweek.in/news/defence/2026/07/19/iafs-rafales-why-pitch-black-2026-air-exercise-will-"
                     "be-special.html", SEARCH),
    "intl_afg_air": ("https://www.newsonair.gov.in/afghan-commerce-minister-concludes-week-long-visit-to-india", OPENED),
    "intl_afg_trib": ("https://www.tribuneindia.com/news/world/afghan-commerce-minister-discusses-trade-bilateral-ties-"
                      "during-visit-to-india", SEARCH),
    "intl_kaz_air": ("https://newsonair.gov.in/60-member-indian-armed-forces-contingent-departs-for-kazind-2026-in-"
                     "kazakhstan/", OPENED),
    "intl_shipki_air": ("https://newsonair.gov.in/india-china-cross-border-trade-resumes-through-shipki-la-after-six-"
                        "years/", OPENED),
    "intl_nathu_air": ("https://newsonair.gov.in/india-china-border-trade-through-nathu-la-resumes-after-six-years/",
                       OPENED),
    "intl_cinbax_an": ("https://newsable.asianetnews.com/amp/india/indian-army-contingent-departs-for-cinbaxii-2026-"
                       "exercise-in-cambodia-articleshow-coh2gqx", OPENED),
    "intl_cinbax_lm": ("https://www.lokmattimes.com/national/indian-army-contingent-departs-for-india-cambodia-bilateral-"
                       "military-exercise-cinbax-ii-2026/amp/", SEARCH),
    "intl_ios_air": ("https://newsonair.gov.in/sri-lanka-ins-sunayna-with-crews-from-16-countries-to-arrive-in-colombo-"
                     "tomorrow/", OPENED),
    "intl_mur_air1": ("https://newsonair.gov.in/president-murmu-to-embark-on-three-nation-tour-first-to-visit-moldova-and-"
                      "north-macedonia/", OPENED),
    "intl_mur_air2": ("https://newsonair.gov.in/president-droupadi-murmu-returns-to-new-delhi-after-concluding-her-three-"
                      "nation-visit-to-moldova-north-macedonia-romania/", OPENED),
    "intl_jam_an": ("https://newsable.asianetnews.com/world/jaishankars-historic-jamaica-visit-deepens-indiacaribbean-"
                    "ties-articleshow-qd2oqrr", OPENED),
    "intl_ven_air": ("https://newsonair.gov.in/people-of-venezuela-express-appreciation-for-indian-medical-team-at-field-"
                     "hospital-established-under-operation-amistad/", OPENED),
    "intl_rim_mi": ("https://www.marineinsight.com/indian-navy-takes-on-leadership-role-in-us-led-multinational-exercise-"
                    "rimpac-2026", OPENED),
    "intl_rim_rw": ("https://www.republicworld.com/defence/indian-navy-s-p-8i-aircraft-arrives-at-joint-base-pearl-harbor-"
                    "hickam-in-hawaii-for-rimpac-2026-2026-07-03-131072", SEARCH),
    # ---- Global events
    "intl_sz_trib": ("https://www.tribuneindia.com/news/science-technology/chinese-astronauts-return-to-earth-after-"
                     "vessel-damaged-by-space-debris", OPENED),
    "intl_sz_reg": ("https://www.theregister.com/2025/11/14/shenzhou20_astronauts_return/", SEARCH),
    "intl_bondi_it": ("https://www.irishtimes.com/world/australia/2025/12/19/australia-plans-gun-buyback-scheme-after-"
                      "bondi-massacre", OPENED),
    "intl_bondi_nbc": ("https://www.nbcnews.com/world/australia/australia-announces-sweeping-gun-buyback-program-surfers-"
                       "honor-bondi-v-rcna250025", SEARCH),
    "intl_srb_air": ("https://newsonair.gov.in/seismic-political-shift-in-serbia-right-wing-progressive-party-loses-its-"
                     "14-year-grip-on-power/", OPENED),
    "intl_ice_air": ("https://newsonair.gov.in/iceland-voters-reject-proposal-to-resume-talks-on-joining-eu/", OPENED),
    "intl_benin_aj": ("https://www.aljazeera.com/news/2025/12/8/nigeria-says-it-deployed-troops-to-benin-to-dislodge-"
                      "coup-plotters", OPENED),
    "intl_benin_gna": ("https://gna.org.gh/2025/12/ecowas-troops-deployed-in-benin-after-foiled-coup/", SEARCH),
    "intl_minurso_air": ("https://newsonair.gov.in/un-peacekeeping-mission-in-western-sahara-ends-after-35-years-says-"
                         "un-chief-antonio-guterres/", OPENED),
    "intl_menon_air": ("https://newsonair.gov.in/indian-origin-nasa-astronaut-anil-menon-begins-first-mission-to-"
                       "international-space-station/", OPENED),
    "intl_pak_aj": ("https://www.aljazeera.com/amp/news/2025/11/11/how-would-pakistans-27th-amendment-reshape-its-"
                    "military-and-courts", OPENED),
    "intl_pak_an": ("https://www.arabnews.pk/node/2622483", SEARCH),
    "intl_unsc_un": ("https://news.un.org/en/story/2025/11/1166391", OPENED),
    "intl_unsc_gs": ("https://www.globalsecurity.org/military/library/news/2025/11/mil-251117-unsc02.htm", SEARCH),
    "intl_syr_trib": ("https://www.tribuneindia.com/news/world/trump-hosts-syrian-president-al-sharaa-at-white-house-"
                      "eases-caesar-act-sanctions", OPENED),
    "intl_syr_aj": ("https://www.aljazeera.com/news/2025/11/10/all-you-need-to-know-about-al-sharaas-historic-visit-to-"
                    "the-us", SEARCH),
    "intl_c11_sky": ("https://www.skyatnightmagazine.com/news/nasa-crew-11-medical-emergency", OPENED),
    "intl_c11_npr": ("https://www.npr.org/2026/01/15/nx-s1-5677647/nasa-spacex-crew-11-splashdown-return", SEARCH),
    "intl_nep_air1": ("https://newsonair.gov.in/nepal-flash-floods-death-toll-rises-to-768-over-2500-missing/", OPENED),
    "intl_nep_air2": ("https://newsonair.gov.in/indias-11-member-technical-team-conducts-reconnaissance-of-flood-hit-"
                      "hydropower-tunnels-in-nepal/", OPENED),
    "intl_nep_air3": ("https://newsonair.gov.in/india-sends-fourth-flight-carrying-11-tonnes-of-humanitarian-aid-to-"
                      "nepal/", OPENED),
    "intl_grl_air": ("https://newsonair.gov.in/eu-to-hold-emergency-meeting-after-us-president-trump-announces-tariffs-"
                     "on-eight-european-countries/", OPENED),
    "intl_fra_air": ("https://newsonair.gov.in/france-to-build-new-aircraft-carrier-french-president-emmanuel-macron-"
                     "announces/", OPENED),
})

T = "International Current Affairs"
BIL, GLO = "Bilateral relations", "Global events"

# ------------------------------------------------------------------ International CA: Basic (8)
G(T, BIL, "Basic",
  "Indian Air Force Rafale fighters took part in Exercise Pitch Black 2026 (20 July to 7 August 2026), the premier "
  "biennial multinational air combat exercise hosted by which air force?",
  ["Royal Australian Air Force", "Royal New Zealand Air Force", "Republic of Singapore Air Force",
   "Royal Malaysian Air Force"], "*",
  "Joint exercises abroad: air force",
  "Exercise Pitch Black is the premier biennial multinational air combat exercise of the Royal Australian Air Force. "
  "The 2026 edition was held at RAAF Base Darwin from 20 July to 7 August, and the IAF sent Rafale fighters supported "
  "by C-17 Globemaster III transports and IL-78 air-to-air refuellers. The IAF had also taken part in 2018, 2022 and "
  "2024. The name comes from its focus on night flying over sparsely populated northern Australia.",
  ["Pitch Black: RAAF's biennial multinational air combat exercise", "2026: RAAF Base Darwin, 20 July-7 August"],
  [fact("Pitch Black is the RAAF's premier biennial multinational air combat exercise; 2026 edition at RAAF Base Darwin "
        "till 7 August with IAF Rafales, C-17 and IL-78 (AIR, 19 July 2026)", "intl_pb_air"),
   fact("IAF Rafales in Pitch Black 2026 in Australia", "intl_pb_week")],
  why="The source names the Royal Australian Air Force as host; the other air forces are not the host.",
  current=ca("2026-07-20"))

G(T, BIL, "Basic",
  "During the India visit of Afghanistan's Commerce Minister Nooruddin Azizi in November 2025, India and Afghanistan "
  "agreed to start an Air Freight Corridor linking Kabul with Delhi and which other Indian city?",
  ["Amritsar", "Mumbai", "Jaipur", "Ahmedabad"], "*",
  "India-Afghanistan trade",
  "Afghan Commerce Minister Nooruddin Azizi concluded a week-long visit to India on 25 November 2025. The two sides "
  "agreed on the Air Freight Corridor on the Kabul-Delhi and Kabul-Amritsar sectors, welcomed the reactivation of the "
  "Joint Working Group on Trade, Commerce and Investment, and agreed to post commercial representatives in each "
  "other's embassies.",
  ["Air Freight Corridor: Kabul-Delhi and Kabul-Amritsar", "Visit concluded 25 November 2025"],
  [fact("Air Freight Corridor on the Kabul-Delhi and Kabul-Amritsar sectors; JWG on Trade, Commerce and Investment "
        "reactivated (AIR, 25 November 2025)", "intl_afg_air"),
   fact("Azizi's India visit on trade and bilateral ties", "intl_afg_trib")],
  why="The source names Amritsar along with Delhi; Mumbai, Jaipur and Ahmedabad are not part of the corridor.",
  current=ca("2025-11-25"))

G(T, BIL, "Basic",
  "KAZIND-2026, the ninth edition of a joint military exercise for which a 60-member Indian contingent left for "
  "Oskemen in September 2026, is held between India and which country?",
  ["Kazakhstan", "Kyrgyzstan", "Uzbekistan", "Tajikistan"], "*",
  "Joint exercises abroad: army",
  "A 60-member Indian Armed Forces contingent, drawn mainly from a battalion of the Garhwal Rifles along with Indian "
  "Air Force personnel, left for Oskemen, Kazakhstan, for the ninth edition of the India-Kazakhstan joint military "
  "exercise KAZIND-2026. It focuses on counter-terrorism operations in a sub-conventional setting under a UN mandate.",
  ["KAZIND = India + Kazakhstan", "2026: ninth edition, Oskemen"],
  [fact("60-member contingent departed for Oskemen, Kazakhstan, for the ninth edition of the India-Kazakhstan exercise "
        "KAZIND-2026; mainly Garhwal Rifles (AIR, 28 September 2026)", "intl_kaz_air")],
  why="The source names Kazakhstan; the other Central Asian countries are not partners in KAZIND.",
  current=ca("2026-09-28"))

G(T, BIL, "Basic",
  "India-China border trade resumed in August 2026 after about six years through the Shipki-La pass, with traders "
  "flagged off from the Chhupan Trade Mart at Namgya. In which State is Shipki-La?",
  ["Himachal Pradesh", "Sikkim", "Uttarakhand", "Arunachal Pradesh"], "*",
  "India-China border trade",
  "Border trade with China through Shipki-La in Kinnaur district, Himachal Pradesh, resumed after about six years; it "
  "had been halted since 2020 because of the COVID-19 pandemic. On the same day trade also resumed through Nathu La in "
  "Sikkim.",
  ["Shipki-La: Kinnaur district, Himachal Pradesh", "Trade halted since 2020 (COVID-19)"],
  [fact("Shipki-La trade resumed after about six years; Chhupan Trade Mart at Namgya, Kinnaur district, Himachal "
        "Pradesh; halted since 2020 (AIR, 1 August 2026)", "intl_shipki_air"),
   fact("Trade through Nathu La in Sikkim resumed the same day after more than six years", "intl_nathu_air")],
  why="Shipki-La is in Himachal Pradesh; Nathu La (the other pass reopened) is in Sikkim.",
  current=ca("2026-08-01"))

G(T, GLO, "Basic",
  "China's Shenzhou-20 crew returned to Earth on 14 November 2025, nine days late, after tiny cracks were found in a "
  "window of their own capsule, suspected to be caused by space debris. In which spacecraft did they return?",
  ["Shenzhou-21", "Shenzhou-19", "Shenzhou-22", "Tianzhou-9"], "*",
  "Space missions: China",
  "The three Shenzhou-20 astronauts landed at the Dongfeng landing site in Inner Mongolia on 14 November 2025 aboard "
  "Shenzhou-21. Their own Shenzhou-20 capsule had tiny cracks in a window and did not meet safety requirements for a "
  "crewed return, so it stayed in orbit. The return had been planned for 5 November.",
  ["Returned on Shenzhou-21, landed at Dongfeng", "Delayed nine days from 5 November"],
  [fact("Shenzhou-20 astronauts landed at Dongfeng on 14 November 2025 aboard Shenzhou-21; Shenzhou-20 window cracks; "
        "return delayed nine days from 5 November", "intl_sz_trib"),
   fact("Shenzhou-20 crew rides Shenzhou-21 home after debris strike", "intl_sz_reg")],
  why="The source says they returned aboard Shenzhou-21; Shenzhou-20 stayed in orbit.",
  current=ca("2025-11-14"))

G(T, GLO, "Basic",
  "On 14 December 2025, two gunmen opened fire on people celebrating Hanukkah, killing 15 people, at which beach in "
  "Australia?",
  ["Bondi Beach, Sydney", "St Kilda Beach, Melbourne", "Surfers Paradise, Gold Coast", "Cottesloe Beach, Perth"], "*",
  "Global events: terror attacks",
  "Fifteen people were killed when gunmen fired on a Hanukkah celebration at Bondi Beach in Sydney on 14 December 2025. "
  "On 19 December Prime Minister Anthony Albanese announced a national gun buyback scheme.",
  ["Bondi Beach, Sydney, 14 December 2025", "National gun buyback announced 19 December 2025"],
  [fact("Bondi shooting of 14 December 2025 at a Hanukkah celebration killed 15; buyback announced 19 December",
        "intl_bondi_it"),
   fact("Australia announces sweeping gun buyback after Bondi attack", "intl_bondi_nbc")],
  why="The source places the attack at Bondi Beach, Sydney; the other beaches are not involved.",
  current=ca("2025-12-14"))

G(T, GLO, "Basic",
  "In Serbia's parliamentary election of October 2026, which newly formed movement shaped by university students "
  "defeated Aleksandar Vučić's Serbian Progressive Party (SNS), ending its 14-year hold on power?",
  ["Students' List", "Movement for the People and State", "Freedom and Justice Party", "Green-Left Front"], "*",
  "Elections: Europe",
  "The Students' List won about 2.2 million votes against about 1.7 million for the SNS in the election to Serbia's "
  "250-member Parliament, and Vučić conceded defeat. He had resigned the presidency a month earlier to lead the SNS "
  "campaign. No students were on the ballot; the list's candidates were mostly experts, athletes, farmers and artists.",
  ["Students' List ~2.2 million votes vs SNS ~1.7 million", "250-member Parliament"],
  [fact("Students' List won about 2.2 million votes to the SNS's 1.7 million; Vučić conceded 'yesterday'; he had "
        "resigned the presidency the previous month (AIR, 26 October 2026)", "intl_srb_air")],
  why="The source names the Students' List as winner; the other names are not the winning movement.",
  current=ca("2026-10-25", inferred="AIR report of 26 October 2026 says Vucic conceded defeat 'yesterday'"))

G(T, GLO, "Basic",
  "In a referendum held in late August 2026, about 53% of voters in which country rejected the government's proposal "
  "to restart talks on joining the European Union?",
  ["Iceland", "Norway", "Switzerland", "United Kingdom"], "*",
  "Referendums: Europe",
  "Around 53% of voters in Iceland opposed the government's proposal to restart membership talks with the European "
  "Union, according to the national broadcaster.",
  ["Iceland: ~53% against restarting EU membership talks"],
  [fact("About 53% of Iceland's voters opposed restarting EU membership talks in the vote held 'yesterday' (AIR, 30 "
        "August 2026)", "intl_ice_air")],
  why="The source refers to Iceland; no such referendum is reported for the other countries.",
  current=ca("2026-08-29", inferred="AIR report of 30 August 2026 says the vote was held 'yesterday'"))

# ------------------------------------------------------------------ International CA: Intermediate (5)
G(T, GLO, "Intermediate",
  "After a coup attempt by a group of soldiers in Benin on 7 December 2025 was foiled, which neighbouring country sent "
  "fighter jets and ground troops at the request of President Patrice Talon's government?",
  ["Nigeria", "Togo", "Niger", "Burkina Faso"], "*",
  "Global events: Africa",
  "Benin's President Patrice Talon said loyal forces defeated the mutineers, reportedly led by Lieutenant Colonel "
  "Pascal Tigri. Nigeria's President Bola Tinubu ordered fighter jets to take over the airspace and later sent ground "
  "troops at Benin's request, and ECOWAS ordered troops from Nigeria, Sierra Leone, Ivory Coast and Ghana to Benin.",
  ["Nigeria: jets + ground troops at Benin's request", "ECOWAS standby troops: Nigeria, Sierra Leone, Ivory Coast, "
   "Ghana"],
  [fact("Nigeria's Tinubu ordered fighter jets and ground troops to Benin at its request; ECOWAS troops from Nigeria, "
        "Sierra Leone, Ivory Coast, Ghana; coup leader Lt Col Pascal Tigri", "intl_benin_aj"),
   fact("ECOWAS troops deployed in Benin after foiled coup", "intl_benin_gna")],
  why="The source names Nigeria as the country that sent jets; Togo, Niger and Burkina Faso are not mentioned.",
  current=ca("2025-12-07"))

G(T, BIL, "Intermediate",
  "CINBAX-II, the second edition of the India-Cambodia bilateral military exercise held in Kampong Speu province from "
  "4 to 17 May 2026, had an Indian contingent drawn mainly from a battalion of which regiment?",
  ["Maratha Light Infantry", "Garhwal Rifles", "Mahar Regiment", "Sikh Light Infantry"], "*",
  "Joint exercises abroad: army",
  "The 120-strong Indian contingent for CINBAX-II 2026 came mainly from a battalion of the Maratha Light Infantry "
  "Regiment; the Royal Cambodian Army fielded 160 personnel. The exercise was held at Camp Basil, Kampong Speu "
  "province, and focused on company-level operations in a sub-conventional setting linked to UN peacekeeping.",
  ["CINBAX-II: 4-17 May 2026, Kampong Speu", "India: 120 personnel, mainly Maratha Light Infantry"],
  [fact("CINBAX-II 2026, 4-17 May, Kampong Speu province; 120 Indian personnel mainly from a Maratha Light Infantry "
        "battalion; 160 from the Royal Cambodian Army", "intl_cinbax_an"),
   fact("Indian Army contingent departs for CINBAX-II 2026", "intl_cinbax_lm")],
  why="The source names the Maratha Light Infantry; the other regiments are not named for CINBAX-II.",
  current=ca("2026-05-04"))

G(T, BIL, "Intermediate",
  "INS Sunayna, deployed as 'IOS Sagar' with personnel from 16 countries on board for the second edition of this "
  "deployment, arrived on 15 May 2026 at which port?",
  ["Colombo", "Malé", "Port Louis", "Chattogram"], "*",
  "India's maritime cooperation",
  "INS Sunayna, deployed as IOS Sagar under India's regional maritime cooperation initiative, arrived at Colombo with a "
  "multinational crew from 16 countries, including Sri Lanka, Bangladesh, Maldives, Mauritius, South Africa, Singapore "
  "and the UAE. It was the second edition of the deployment.",
  ["IOS Sagar (2nd edition): INS Sunayna", "Crew from 16 countries; Colombo, 15 May 2026"],
  [fact("INS Sunayna deployed as IOS Sagar, second edition, crew from 16 countries, arrived at Colombo 'this morning' "
        "(AIR, 15 May 2026)", "intl_ios_air")],
  why="The source reports the arrival at Colombo; the other ports are not mentioned for that date.",
  current=ca("2026-05-15"))

G(T, GLO, "Intermediate",
  "The UN mission MINURSO, set up in 1991 to monitor a ceasefire and organise a referendum on self-determination, "
  "began its liquidation phase on 1 November 2026 after the Security Council did not renew its mandate. Which "
  "territory did it cover?",
  ["Western Sahara", "Cyprus", "Southern Lebanon", "Abyei"], "*",
  "UN peacekeeping",
  "The UN Mission for the Referendum in Western Sahara (MINURSO) ended after 35 years; Secretary-General António "
  "Guterres said 1 November marked the start of its liquidation. The referendum never took place because of disputes "
  "over voter eligibility. A Council resolution of the previous year had called Morocco's autonomy proposal the most "
  "feasible solution; the Algeria-backed Polisario Front expressed concern.",
  ["MINURSO = UN Mission for the Referendum in Western Sahara (1991)", "Liquidation from 1 November 2026"],
  [fact("MINURSO, established 1991, liquidation phase from 1 November; mandate not renewed; Morocco's autonomy plan; "
        "Polisario Front (AIR, 2 November 2026)", "intl_minurso_air")],
  why="MINURSO is the Western Sahara mission; Cyprus, Lebanon and Abyei have other UN missions not discussed here.",
  current=ca("2026-11-01"))

G(T, GLO, "Intermediate",
  "Indian-origin NASA astronaut Anil Menon began his first mission to the International Space Station on 14 July 2026 "
  "aboard which spacecraft?",
  ["Soyuz MS-29", "SpaceX Crew Dragon (Crew-12)", "Boeing Starliner-1", "Soyuz MS-27"], "*",
  "Space missions: ISS",
  "Anil Menon lifted off from the Baikonur Cosmodrome in Kazakhstan aboard Soyuz MS-29 with Roscosmos cosmonauts "
  "Pyotr Dubrov and Anna Kikina. The mission, his first spaceflight, is planned to last about eight months, with a "
  "return in April 2027.",
  ["Soyuz MS-29 from Baikonur", "Crew: Menon, Dubrov, Kikina; ~8 months"],
  [fact("Anil Menon launched 'yesterday' at 8:17 pm IST aboard Soyuz MS-29 from Baikonur with Pyotr Dubrov and Anna "
        "Kikina; return planned April 2027 (AIR, 15 July 2026)", "intl_menon_air")],
  why="The source names Soyuz MS-29; the other spacecraft did not carry him.",
  current=ca("2026-07-14", inferred="AIR report of 15 July 2026 says the launch was 'yesterday'"))

# ------------------------------------------------------------------ International CA: Advanced (11)
GS(T, GLO, "Advanced", "the Indian Navy's participation in RIMPAC 2026",
   ["RIMPAC 2026 was the 25th edition of the exercise, which began in 1971.",
    "For the first time, the Indian Navy served as Deputy Commander of the Task Force for Theatre-level Anti-Submarine "
    "Warfare.",
    "The Indian Navy deployed a P-8I long-range maritime patrol aircraft and the stealth frigate INS Shivalik."],
   [False, True, True],
   "Multinational exercises: RIMPAC",
   "RIMPAC 2026, held around the Hawaiian Islands, was the 30th edition of a series that began in 1971, with more than "
   "30 countries taking part. The Indian Navy, which sent a P-8I aircraft and INS Shivalik, served for the first time "
   "as Deputy Commander of the Task Force for Theatre-level Anti-Submarine Warfare.",
   [fact("RIMPAC 2026 is the 30th edition (series began 1971), around Hawaii; Indian Navy Deputy Commander Task Force "
         "for theatre-level ASW for the first time; P-8I and INS Shivalik (Marine Insight, 10 July 2026)", "intl_rim_mi"),
    fact("P-8I arrived at Joint Base Pearl Harbor-Hickam for RIMPAC 2026", "intl_rim_rw")],
   why="Statement 1 is wrong: RIMPAC 2026 was the 30th edition, not the 25th.",
   current=ca("2026-07-10", inferred="Marine Insight report of 10 July 2026 on India's role; exercise ran in July"))

GS(T, BIL, "Advanced", "President Droupadi Murmu's State visits of July 2026",
   ["They were the first-ever bilateral visits by an Indian President to Moldova and North Macedonia.",
    "The previous State visit by an Indian President to Romania had taken place in 2004.",
    "In Romania she received an honorary recognition from the Bucharest University of Economic Studies."],
   [True, False, True],
   "Presidential visits",
   "President Murmu visited Moldova, North Macedonia and Romania from 19 to 25 July 2026. These were the first-ever "
   "bilateral visits by an Indian President to Moldova and North Macedonia, and the first State visit to Romania in over "
   "three decades, the previous one being in 1994. In Romania she was honoured by the Bucharest University of Economic "
   "Studies.",
   [fact("Visits 19-25 July; first ever bilateral visit by an Indian President to Moldova and North Macedonia; Romania "
         "first in over 3 decades, previous in 1994 (AIR, 17 July 2026)", "intl_mur_air1"),
    fact("Honorary recognition from the Bucharest University of Economic Studies; returned 26 July (AIR)",
         "intl_mur_air2")],
   why="Statement 2 is wrong: the previous State visit by an Indian President to Romania was in 1994.",
   current=ca("2026-07-19"))

GS(T, GLO, "Advanced", "Pakistan's 27th Constitutional Amendment, approved by its Senate on 10 November 2025",
   ["It creates the post of Chief of Defence Forces, to be held by the army chief.",
    "The post of Chairman of the Joint Chiefs of Staff Committee is to be scrapped.",
    "It abolishes the Supreme Court and transfers all its cases to a new Federal Constitutional Court."],
   [True, True, False],
   "Pakistan: constitutional change",
   "The amendment creates a Chief of Defence Forces post held by the army chief, giving him authority over the air force "
   "and navy, and scraps the post of Chairman of the Joint Chiefs of Staff Committee. It sets up a permanent Federal "
   "Constitutional Court with judges from each province and Islamabad to hear disputes between governments, while the "
   "Supreme Court continues as an appellate court. Five-star officers may keep their rank for life.",
   [fact("Senate approved the amendment on 10 November 2025; CDF post held by the army chief; CJCSC post scrapped; "
         "Federal Constitutional Court created and Supreme Court reduced to an appellate court", "intl_pak_aj"),
    fact("Pakistan president signs into law 27th constitutional amendment", "intl_pak_an")],
   why="Statement 3 is wrong: the Supreme Court is not abolished; it is reduced to an appellate court.",
   current=ca("2025-11-10"))

GS(T, GLO, "Advanced", "UN Security Council Resolution 2803 (2025) on Gaza",
   ["It was adopted unanimously by all 15 members of the Council.",
    "It authorises a temporary International Stabilization Force (ISF) in Gaza.",
    "It welcomes a Board of Peace as a transitional administration to coordinate reconstruction in Gaza."],
   [False, True, True],
   "UN Security Council",
   "Resolution 2803 was adopted on 17 November 2025 by 13 votes to none, with China and Russia abstaining. It welcomes "
   "the Board of Peace as a transitional administration to coordinate Gaza's reconstruction and authorises it to set up "
   "a temporary International Stabilization Force under unified command.",
   [fact("Resolution 2803 adopted 17 November 2025 by 13 votes in favour, none against, China and Russia abstaining; "
         "Board of Peace as transitional administration; temporary ISF", "intl_unsc_un"),
    fact("Security Council authorizes International Stabilization Force in Gaza, adopting Resolution 2803 (2025)",
         "intl_unsc_gs")],
   why="Statement 1 is wrong: the vote was 13-0 with China and Russia abstaining.",
   current=ca("2025-11-17"))

GS(T, GLO, "Advanced", "Syrian President Ahmed al-Sharaa's visit to the White House on 10 November 2025",
   ["It was the first White House visit by a Syrian head of state since Syria's independence from France in 1946.",
    "During the visit Syria announced that it would stay out of the US-led coalition against the Islamic State.",
    "The US Treasury announced a 180-day suspension of Caesar Act sanctions, except for transactions involving Russia "
    "and Iran."],
   [True, False, True],
   "US-Syria relations",
   "Al-Sharaa's meeting with President Trump was the first White House visit by a Syrian head of state since "
   "independence in 1946. The Treasury announced a 180-day waiver suspending the Caesar Act, except for transactions "
   "involving Russia and Iran, and Syria was set to join the US-led coalition against the Islamic State.",
   [fact("First White House visit by a Syrian head of state since independence from France in 1946; Treasury 180-day "
         "waiver, Caesar Act suspended except for Russia/Iran transactions; Syria to join anti-IS coalition",
         "intl_syr_trib"),
    fact("Al-Sharaa's historic visit to the US on 10 November 2025", "intl_syr_aj")],
   why="Statement 2 is wrong: the source says Syria was set to join the US-led coalition against the Islamic State.",
   current=ca("2025-11-10"))

GS(T, GLO, "Advanced", "the return of NASA's SpaceX Crew-11 mission from the International Space Station",
   ["The crew splashed down in the Pacific Ocean off San Diego on 15 January 2026.",
    "The crew included Kimiya Yui of JAXA and Oleg Platonov of Roscosmos.",
    "The mission was cut short because space debris cracked a window of the Crew Dragon capsule."],
   [True, True, False],
   "Space missions: ISS",
   "Crew-11 (Zena Cardman and Mike Fincke of NASA, Kimiya Yui of JAXA and Oleg Platonov of Roscosmos) splashed down off "
   "San Diego on 15 January 2026. It came home early because of a medical issue with a crew member, the first time a "
   "NASA crewed mission returned early for medical reasons and the first early evacuation in the station's history.",
   [fact("Splashdown morning of 15 January 2026 in the Pacific off San Diego; crew Cardman, Fincke (NASA), Kimiya Yui "
         "(JAXA), Oleg Platonov (Roscosmos); first early return for a medical issue", "intl_c11_sky"),
    fact("After a medical evacuation from space, NASA's Crew-11 returns to Earth a month early", "intl_c11_npr")],
   why="Statement 3 is wrong: the return was brought forward because of a medical issue, not debris damage.",
   current=ca("2026-01-15"))

GS(T, BIL, "Advanced", "External Affairs Minister S. Jaishankar's visit to Jamaica on 2-4 May 2026",
   ["It was the first-ever bilateral visit by an Indian External Affairs Minister to Jamaica.",
    "India handed over BHISHM emergency medical units to help recovery from Hurricane Melissa.",
    "Jamaica backed India's candidature for a non-permanent seat on the UN Security Council for 2028-29."],
   [True, True, True],
   "India-Caribbean relations",
   "Jaishankar's visit was the first bilateral visit by an Indian EAM to Jamaica. He met Prime Minister Andrew Holness, "
   "three MoUs (health, renewable energy, media) were signed, India handed over 10 BHISHM units and pledged 30 dialysis "
   "units for Hurricane Melissa recovery, ITEC slots rose from 6 to 34, and Jamaica supported India's UNSC bid for "
   "2028-29.",
   [fact("First-ever bilateral visit by an Indian EAM to Jamaica, 2-4 May 2026; 10 BHISHM units and 30 dialysis units "
         "for Hurricane Melissa recovery; Jamaica supports India's UNSC bid for 2028-29", "intl_jam_an")],
   why="All three statements match the report of the visit.",
   current=ca("2026-05-02"))

GS(T, BIL, "Advanced", "the flash floods in central Nepal in August 2026 and India's response",
   ["The floods were caused by a cloudburst over the Kathmandu Valley.",
    "The mudslides also hit the Gyirong port on the China-Nepal border.",
    "India sent an 11-member team of doctors, paramedics and tunnel engineers to a flood-hit hydropower tunnel in Nuwakot "
    "district."],
   [False, True, True],
   "Disasters: India's assistance",
   "The floods swept the Bhotekoshi and Trishuli river corridors after an ice-rock avalanche following a glacial "
   "collapse near the Nepal-Tibet border; by 30 August the toll had reached 768 with over 2,500 missing. Gyirong port in "
   "Tibet was also hit. India sent an 11-member team of doctors, paramedics and tunnel engineers to Trishuli (Nuwakot) "
   "and had provided 68.5 tonnes of relief by 30 August.",
   [fact("Cause: ice-rock avalanche after a glacial collapse near the Nepal-Tibet border; Gyirong port hit; toll 768 "
         "(AIR, 30 August 2026)", "intl_nep_air1"),
    fact("11-member Indian team of doctors, paramedics and tunnel engineers at hydropower tunnel in Trishuli, Nuwakot; "
         "floods on Wednesday (AIR, 29 August 2026)", "intl_nep_air2"),
    fact("India provided 68.5 tonnes of relief materials to Nepal", "intl_nep_air3")],
   why="Statement 1 is wrong: the floods followed an ice-rock avalanche after a glacial collapse near the Tibet border.",
   current=ca("2026-08-26", inferred="AIR says the floods struck on a Wednesday and the linked Tibet floods on the 26th"))

GS(T, BIL, "Advanced", "the earthquakes in Venezuela in June 2026 and India's response",
   ["Twin earthquakes of magnitudes 7.2 and 7.5 struck the country on 24 June 2026.",
    "India launched 'Operation Amistad' and deployed an Indian Army medical team that ran a field hospital.",
    "The death toll given by National Assembly President Jorge Rodríguez was more than 2,000."],
   [True, True, True],
   "Disasters: India's assistance",
   "Twin earthquakes of magnitude 7.2 and 7.5 on 24 June 2026 caused widespread destruction. Venezuela's National "
   "Assembly President Jorge Rodríguez put the toll at 2,295 dead and 11,267 injured. India launched Operation Amistad "
   "and deployed a specialised Indian Army medical contingent at a field hospital.",
   [fact("Twin earthquakes of 7.2 and 7.5 on 24 June; Operation Amistad; Indian Army medical contingent at a field "
         "hospital; toll 2,295 dead per Jorge Rodríguez (AIR, 2 July 2026)", "intl_ven_air")],
   why="All three statements match the report.",
   current=ca("2026-06-24"))

GS(T, GLO, "Advanced", "the tariffs announced by US President Donald Trump in January 2026 over Greenland",
   ["A 10% tariff was to apply from 1 February 2026.",
    "The rate was to rise to 25% from 1 June.",
    "The countries targeted included Denmark, Norway and Poland."],
   [True, True, False],
   "US tariffs: Greenland",
   "Trump announced a 10% tariff from 1 February, rising to 25% on 1 June, on eight countries that opposed a US "
   "acquisition of Greenland: Denmark, Norway, Sweden, France, Germany, the UK, the Netherlands and Finland. The tariffs "
   "were to stay until Greenland was sold to the US. The EU called an emergency meeting.",
   [fact("10% from 'the 1st of next month', rising to 25% on 1 June; eight countries: Denmark, Norway, Sweden, France, "
         "Germany, UK, Netherlands, Finland (AIR, 18 January 2026)", "intl_grl_air")],
   why="Statement 3 is wrong: Poland was not among the eight countries named.",
   current=ca("2026-01-18", inferred="AIR report of 18 January 2026 says the tariffs were announced earlier on Truth "
              "Social"))

GS(T, GLO, "Advanced", "France's new aircraft carrier announced by President Emmanuel Macron in December 2025",
   ["Like the Charles de Gaulle, it will be nuclear-powered.",
    "At about 42,000 tonnes it will be smaller than the Charles de Gaulle.",
    "It is planned to enter service in 2038."],
   [True, False, True],
   "Defence: Europe",
   "The new nuclear-powered carrier will displace about 78,000 tonnes and be 310 m long, against 42,000 tonnes and 261 "
   "m for the Charles de Gaulle, in service since 2001. It is planned to enter service in 2038.",
   [fact("Nuclear-powered; about 78,000 tons and 310 m vs 42,000 tons and 261 m for the Charles de Gaulle (in service "
         "2001); planned for 2038 (AIR, 22 December 2025)", "intl_fra_air")],
   why="Statement 2 is wrong: 42,000 tonnes is the Charles de Gaulle; the new carrier is about 78,000 tonnes.",
   current=ca("2025-12-22", inferred="AIR report of 22 December 2025 says Macron 'has announced' it"))

# ###################################################################### part: pol (schemes + policies)
# ###################################################################### part: pol (Government Schemes, Government Policies)
U.update({
    # ---- Schemes
    "pol_relief_air": ("https://newsonair.gov.in/commerce-ministry-extends-relief-scheme-for-exporters-until-march-31-2027/",
                       OPENED),
    "pol_rodtep_air": ("https://newsonair.gov.in/government-extends-rodtep-scheme-upto-31st-december-2026/", OPENED),
    "pol_cbdc_air": ("https://newsonair.gov.in/digital-rupee-for-dbt-under-pm-garib-kalyan-anna-yojana-to-be-launched-in-"
                     "chandigarh-today/", OPENED),
    "pol_svn_air": ("https://newsonair.gov.in/union-cabinet-approves-restructuring-of-pm-svanidhi-scheme/", OPENED),
    "pol_avv_air": ("https://newsonair.gov.in/ayushman-vay-vandana-yojana-completes-two-years/", OPENED),
    "pol_pli_air": ("https://newsonair.gov.in/textiles-ministry-to-reopen-pli-scheme-application-portal-from-november-1/",
                    OPENED),
    "pol_cmr_air": ("https://newsonair.gov.in/cabinet-approves-incentive-scheme-to-promote-critical-mineral-recycling/",
                    OPENED),
    # ---- Policies
    "pol_bvn_air": ("https://newsonair.gov.in/govt-notifies-new-set-of-rules-governing-indias-civil-aviation-sector-"
                    "replacing-colonial-era-aircraft-rules-1937/", OPENED),
    "pol_bvn_tt": ("https://telanganatoday.com/govt-notifies-new-aviation-rules-bharatiya-vayuyan-niyam-effective-jan-1-2027",
                   OPENED),
    "pol_coal_air": ("https://newsonair.gov.in/coal-ministry-notifies-coal-exchange-rules-2026-to-enable-transparent-coal-"
                     "trading/", OPENED),
    "pol_coal_pl": ("https://powerline.net.in/2026/06/10/ministry-of-coal-notifies-coal-exchange-rules-2026/", SEARCH),
    "pol_ist_air": ("https://newsonair.gov.in/dept-of-consumer-affairs-notifies-legal-metrology-indian-standard-time-"
                    "rules-2026/", OPENED),
    "pol_ist2_air": ("https://newsonair.gov.in/government-notifies-rules-mandating-indian-standard-time/", OPENED),
    "pol_cas_air": ("https://newsonair.gov.in/sebi-revises-timings-and-operational-framework-of-closing-auction-session/",
                    OPENED),
    "pol_cas_ml": ("https://www.moneylife.in/article/sebi-introduces-10minute-closing-auction-session-revises-expiry-"
                   "settlement-rules-for-stock-index-derivatives/81965.html", SEARCH),
    "pol_crm_air": ("https://newsonair.gov.in/sebi-introduces-credit-risk-o-meter-to-help-investors-assess-debt-security-"
                    "risks/", OPENED),
    "pol_crm_ll": ("https://www.livelawbiz.com/securities-law/sebi/securities-and-exchange-board-of-india-introduced-six-"
                   "tier-colour-coded-credit-risk-indicator-for-debt-securities-553649", OPENED),
    "pol_vbg_air": ("https://newsonair.gov.in/govt-notifies-vb-g-ram-g-grievance-redressal-rules-2026-for-addressing-"
                    "grievances-relating-to-implementation-of-scheme/", OPENED),
})

T = "Government Schemes"
CS, SLC = "Central schemes", "Scheme launches and changes"

# ------------------------------------------------------------------ Schemes: Basic (4)
G(T, SLC, "Basic",
  "In October 2026 the Commerce Ministry extended Component II of 'RELIEF', an intervention for exporters hit by "
  "disruptions in West Asian shipping routes, up to 31 March 2027. What does RELIEF stand for?",
  ["Resilience and Logistics Intervention for Export Facilitation",
   "Relief for Exporters through Logistics and Insurance Enhancement Fund",
   "Regional Export Logistics Incentive for Enterprise Facilitation",
   "Rapid Export Loss Indemnity and Freight Equalisation"], "*",
  "Export support schemes: RELIEF",
  "RELIEF (Resilience and Logistics Intervention for Export Facilitation) is a time-bound intervention of the "
  "Department of Commerce under the Export Promotion Mission. It supports exporters facing higher freight costs, "
  "higher insurance premiums and war-related risks due to disruptions in the Gulf and the wider West Asian maritime "
  "corridor. Component II encourages exporters to take ECGC cover with 95% risk coverage; its timelines were extended "
  "to 31 March 2027.",
  ["RELIEF = Resilience and Logistics Intervention for Export Facilitation", "Under the Export Promotion Mission",
   "Component II: ECGC cover, 95% risk coverage; extended to 31 March 2027"],
  [fact("RELIEF (Resilience and Logistics Intervention for Export Facilitation), Department of Commerce, under the "
        "Export Promotion Mission; Component II timelines extended to 31 March 2027; ECGC cover with 95% risk coverage "
        "(AIR, 26 Oct 2026)", "pol_relief_air")],
  why="The source gives the expansion 'Resilience and Logistics Intervention for Export Facilitation'; the other "
      "expansions are made up.",
  current=ca("2026-10-26", inferred="AIR report dated 26 October 2026 gives no separate date for the extension"))

G(T, SLC, "Basic",
  "In October 2026 the Ministry of Commerce and Industry extended the RoDTEP scheme, which refunds embedded duties and "
  "taxes on exported products, up to which date?",
  ["31 December 2026", "31 March 2027", "30 September 2027", "31 March 2026"], "*",
  "Export schemes: RoDTEP",
  "The Remission of Duties and Taxes on Exported Products (RoDTEP) scheme was extended up to 31 December 2026. It "
  "covers exports by Domestic Tariff Area units, Advance Authorisation holders, SEZ units and Export Oriented Units, "
  "and refunds un-rebated Central, State and local duties, taxes and levies embedded in exported products.",
  ["RoDTEP = Remission of Duties and Taxes on Exported Products", "Extended up to 31 December 2026",
   "Covers DTA units, Advance Authorisation holders, SEZ units and EOUs"],
  [fact("Government extends RoDTEP scheme up to 31 December 2026 for exports by DTA units, Advance Authorisation "
        "holders, SEZ units and EOUs; refunds embedded un-rebated duties and taxes (AIR, 2 Oct 2026)", "pol_rodtep_air")],
  why="The source gives 31 December 2026 as the extended date; the other dates are not the RoDTEP deadline.",
  current=ca("2026-10-02", inferred="AIR report dated 2 October 2026 gives no separate date for the extension"))

G(T, SLC, "Basic",
  "On 14 August 2026, which Union Territory became the first UT to undertake a full-fledged roll-out of Digital Rupee "
  "(CBDC) based Direct Benefit Transfer of food subsidy under the Pradhan Mantri Garib Kalyan Anna Yojana?",
  ["Chandigarh", "Puducherry", "Ladakh", "Lakshadweep"], "*",
  "Scheme delivery: CBDC-based DBT",
  "The Digital Rupee (e₹) for Direct Benefit Transfer under PMGKAY was launched in Chandigarh on 14 August 2026, making "
  "it the first Union Territory to undertake a full-fledged roll-out of CBDC-based DBT for food subsidy. Union Ministers "
  "Shivraj Singh Chouhan and Pralhad Joshi and Chandigarh Administrator Gulab Chand Kataria took part; a virtual launch "
  "was also held for Dadra and Nagar Haveli.",
  ["Chandigarh: first UT with full CBDC-based DBT for food subsidy", "Scheme: PMGKAY; 14 August 2026"],
  [fact("Digital Rupee for DBT under PMGKAY launched in Chandigarh; first UT to undertake full-fledged roll-out of "
        "CBDC-based DBT for food subsidy; virtual launch for Dadra and Nagar Haveli (AIR, 14 Aug 2026)", "pol_cbdc_air")],
  why="The source names Chandigarh as the first UT; Puducherry, Ladakh and Lakshadweep are not mentioned.",
  current=ca("2026-08-14"))

G(T, CS, "Basic",
  "Under the restructured PM SVANidhi scheme approved by the Union Cabinet in August 2025, the first-tranche loan for "
  "street vendors was raised from ₹10,000 to what amount?",
  ["₹15,000", "₹20,000", "₹25,000", "₹12,000"], "*",
  "PM SVANidhi: restructuring",
  "The Cabinet extended the PM SVANidhi lending period to 31 March 2030 with an outlay of ₹7,332 crore. The first "
  "tranche was raised from ₹10,000 to ₹15,000 and the second from ₹20,000 to ₹25,000, while the third stays at ₹50,000. "
  "Beneficiaries who repay the second loan can get a UPI-linked RuPay credit card.",
  ["1st tranche: ₹10,000 -> ₹15,000", "2nd tranche: ₹20,000 -> ₹25,000; 3rd: ₹50,000",
   "Lending period to 31 March 2030; outlay ₹7,332 crore"],
  [fact("Restructured PM SVANidhi: lending to 31 March 2030; outlay ₹7,332 crore; first tranche ₹10,000 -> ₹15,000, "
        "second ₹20,000 -> ₹25,000, third unchanged at ₹50,000; UPI-linked RuPay credit card (AIR, 27 Aug 2025)",
        "pol_svn_air")],
  why="₹25,000 is the new second tranche and ₹20,000 the old second tranche; ₹12,000 is not mentioned.",
  current=ca("2025-08-27", inferred="AIR report dated 27 August 2025 on that day's Cabinet decision"))

# ------------------------------------------------------------------ Schemes: Intermediate (2)
G(T, CS, "Intermediate",
  "According to data released when the Ayushman Vay Vandana Yojana for citizens aged 70 and above completed two years "
  "in October 2026, which treatment was the most common among its beneficiaries?",
  ["Cataract surgery", "Chronic haemodialysis", "Total knee replacement", "Coronary angioplasty"], "*",
  "Health schemes: Ayushman Vay Vandana",
  "Launched in October 2024, the Ayushman Vay Vandana Yojana extends AB PM-JAY cover of up to ₹5 lakh per family per "
  "year to citizens aged 70 and above, irrespective of income. In two years it recorded over 23 lakh hospital "
  "admissions worth ₹5,668 crore. Cataract surgery was the most common treatment (4.71 lakh), followed by chronic "
  "haemodialysis (about 3 lakh).",
  ["Most common: cataract surgery (4.71 lakh)", "Second: chronic haemodialysis (~3 lakh)",
   "23 lakh+ admissions, ₹5,668 crore"],
  [fact("Ayushman Vay Vandana Yojana completes two years: over 23 lakh admissions, ₹5,668 crore; cataract surgery most "
        "common (4.71 lakh), chronic haemodialysis second (about 3 lakh); total knee replacement among other categories "
        "(AIR, 29 Oct 2026)", "pol_avv_air")],
  why="The source ranks chronic haemodialysis second and lists knee replacement only among other categories; "
      "angioplasty is not mentioned.",
  current=ca("2026-10-29", inferred="AIR report dated 29 October 2026 gives no separate release date"))

G(T, SLC, "Intermediate",
  "For the fourth round of the Production Linked Incentive (PLI) scheme for textiles, with applications open from 1 "
  "November to 31 December 2026, the minimum turnover requirement for applicants was reduced to what level?",
  ["₹100 crore", "₹50 crore", "₹150 crore", "₹200 crore"], "*",
  "PLI scheme for textiles: Round 4",
  "The Ministry of Textiles reopened the PLI application portal from 1 November to 31 December 2026 for Round 4, "
  "covering MMF apparel, MMF fabrics and technical textiles. The minimum turnover requirement was cut from ₹200 crore "
  "to ₹100 crore to help MSMEs and mid-sized units, and the scheme tenure was extended up to FY 2033-34 for Round 4 "
  "approved applicants.",
  ["Min turnover: ₹200 crore -> ₹100 crore", "Round 4 window: 1 Nov - 31 Dec 2026",
   "Sectors: MMF apparel, MMF fabrics, technical textiles; tenure to FY 2033-34 for Round 4"],
  [fact("Textiles PLI portal reopens 1 November to 31 December 2026 for Round 4; minimum turnover reduced from ₹200 "
        "crore to ₹100 crore; tenure extended to FY 2033-34 for Round 4 applicants (AIR, 29 Oct 2026)", "pol_pli_air")],
  why="₹200 crore was the earlier requirement; ₹50 crore and ₹150 crore are not mentioned.",
  current=ca("2026-10-29", inferred="AIR report dated 29 October 2026 on the announcement"))

# ------------------------------------------------------------------ Schemes: Advanced (1)
GS(T, CS, "Advanced",
   "the incentive scheme to promote critical mineral recycling approved by the Union Cabinet in September 2025",
   ["Incentives are available to recyclers that only produce black mass, even if they do not extract critical "
    "minerals.",
    "It has an outlay of ₹1,500 crore over six years, from FY 2025-26 to FY 2030-31.",
    "It offers a capex subsidy of 20% on plant and machinery, equipment and associated utilities for starting "
    "production within a specified time."],
   [False, True, True],
   "Critical mineral recycling scheme (part of NCMM)",
   "The ₹1,500 crore scheme, part of the National Critical Mineral Mission, runs from FY 2025-26 to FY 2030-31. "
   "Eligible feedstock includes e-waste, lithium-ion battery scrap and other scrap. Incentives go only to recyclers "
   "that actually extract critical minerals, not to those producing only black mass. It offers a 20% capex subsidy on "
   "plant, machinery, equipment and utilities (reduced if production starts later) plus an opex subsidy on incremental "
   "sales. It is expected to create at least 270 kilo tonnes a year of recycling capacity and about 40 kilo tonnes a "
   "year of critical mineral production.",
   [fact("₹1,500 crore scheme under NCMM, FY 2025-26 to FY 2030-31; feedstock e-waste, LIB scrap and other scrap; "
         "incentives only for recyclers extracting critical minerals, not those producing only black mass; 20% capex "
         "subsidy; opex subsidy on incremental sales; 270 KT capacity, ~40 KT production (AIR, 3 Sep 2025)",
         "pol_cmr_air")],
   why="Statement 1 is wrong: the source says only recyclers actually extracting critical minerals are eligible, not "
       "those producing only black mass.",
   current=ca("2025-09-03", inferred="AIR report dated 3 September 2025 on that day's Cabinet decision"))

# ====================================================================== Government Policies
T = "Government Policies"
PC, RR = "Policy changes", "Regulatory reforms"

# ------------------------------------------------------------------ Policies: Basic (1)
G(T, RR, "Basic",
  "Which new set of rules, notified by the Ministry of Civil Aviation in November 2026, will replace the colonial-era "
  "Aircraft Rules, 1937 from 1 January 2027?",
  ["Bharatiya Vayuyan Niyam, 2026", "Bharatiya Nagar Vimanan Niyam, 2026", "Rashtriya Vayu Suraksha Niyam, 2026",
   "Bharatiya Vimanpattan Niyam, 2026"], "*",
  "Civil aviation regulation",
  "The Bharatiya Vayuyan Niyam, 2026 replace the Aircraft Rules, 1937, which governed the sector for nearly nine "
  "decades, from 1 January 2027. They cover aircraft registration, airworthiness, manufacturing, maintenance, flight "
  "operations, personnel licensing and aerodromes, require airlines to disclose the full fare with a breakdown, keep "
  "tariffs under DGCA oversight and let the Centre issue directions in extraordinary situations.",
  ["Bharatiya Vayuyan Niyam, 2026 replace Aircraft Rules, 1937", "Effective 1 January 2027",
   "Fare transparency; DGCA monitors tariffs"],
  [fact("Govt notifies Bharatiya Vayuyan Niyam, 2026 replacing the Aircraft Rules, 1937; Centre may intervene in "
        "extraordinary situations; DGCA monitors tariffs (AIR, 3 Nov 2026)", "pol_bvn_air"),
   fact("Bharatiya Vayuyan Niyam, 2026 effective 1 January 2027; replaces Aircraft Rules, 1937 that governed the sector "
        "for nearly nine decades; fare breakdown disclosure (IANS via Telangana Today, 2 Nov 2026)", "pol_bvn_tt")],
  why="The sources name the Bharatiya Vayuyan Niyam, 2026; the other names are made up.",
  current=ca("2026-11-02", inferred="reports of 2-3 November 2026 say the rules have been notified but give no gazette "
                                    "date"))

# ------------------------------------------------------------------ Policies: Intermediate (5)
G(T, RR, "Intermediate",
  "Under the Coal Exchange Rules, 2026, notified by the Ministry of Coal in June 2026, which body registers and "
  "regulates coal exchanges?",
  ["Coal Controller Organisation", "Securities and Exchange Board of India", "Central Electricity Regulatory Commission",
   "Coal India Limited"], "*",
  "Coal sector reform: coal exchanges",
  "The Coal Exchange Rules, 2026 allow coal exchanges to be set up in India, moving coal sales from a one-to-many model "
  "to a many-to-many trading platform for better price discovery. The Coal Controller Organisation regulates and "
  "registers the exchanges.",
  ["Regulator of coal exchanges: Coal Controller Organisation", "Shift from one-to-many sales to many-to-many trading"],
  [fact("Coal Exchange Rules, 2026 notified by the Ministry of Coal; Coal Controller Organisation to regulate and "
        "register coal exchanges; one-to-many to many-to-many model (AIR, 9 Jun 2026)", "pol_coal_air"),
   fact("Ministry of Coal notifies Coal Exchange Rules, 2026 (Powerline, 10 Jun 2026)", "pol_coal_pl")],
  why="The source names the Coal Controller Organisation as regulator; SEBI, CERC and Coal India are not given this "
      "role.",
  current=ca("2026-06-09", inferred="AIR report dated 9 June 2026 gives no separate notification date"))

G(T, PC, "Intermediate",
  "The Legal Metrology (Indian Standard Time) Rules, 2026, notified by the Department of Consumer Affairs in August "
  "2026 to make IST the common time reference for legal, administrative and commercial purposes, come into force how "
  "long after their publication in the Official Gazette?",
  ["180 days", "90 days", "30 days", "One year"], "*",
  "Legal metrology: Indian Standard Time",
  "The Legal Metrology (Indian Standard Time) Rules, 2026 make IST the common, legally recognised and traceable time "
  "reference for the country, supporting the 'One Nation, One Time' vision. They name uses such as time-stamping of "
  "banking and digital payment transactions and coordination of railways and airports, and come into force 180 days "
  "after publication in the Official Gazette.",
  ["In force 180 days after Gazette publication", "'One Nation, One Time'",
   "Uses: banking/digital payments time-stamping, transport, emergency services"],
  [fact("Legal Metrology (IST) Rules, 2026 by the Department of Consumer Affairs; come into force 180 days after "
        "publication in the Official Gazette; banking and digital payments time-stamping (AIR, 30 Aug 2026)",
        "pol_ist_air"),
   fact("Rules notified on the 27th and published in the Gazette on the 29th; in force 180 days after publication; "
        "'One Nation, One Time' vision (AIR, 3 Sep 2026)", "pol_ist2_air")],
  why="The sources give 180 days; the other periods are not mentioned.",
  current=ca("2026-08-29", inferred="AIR (3 Sep 2026) says the rules were published in the Gazette on the 29th of the "
                                    "previous month, taken as 29 August 2026"))

G(T, RR, "Intermediate",
  "Under SEBI's revised framework for the Closing Auction Session (CAS) in the equity cash market, announced through a "
  "circular in October 2026, during which window will the CAS be held on all trading days?",
  ["3:30 pm to 3:40 pm", "3:15 pm to 3:35 pm", "3:40 pm to 3:50 pm", "3:50 pm to 4:00 pm"], "*",
  "Market microstructure: Closing Auction Session",
  "SEBI's revised framework sets a 10-minute CAS from 3:30 pm to 3:40 pm, with order entry closing at a random time "
  "between 3:38 pm and 3:40 pm. Stock and index derivatives trade until 3:45 pm, and a post-closing session runs from "
  "3:50 pm to 4:00 pm at the closing price. Most provisions apply from 7 December 2026. The earlier framework of "
  "January 2026 had a 20-minute CAS from 3:15 pm to 3:35 pm.",
  ["Revised CAS: 3:30-3:40 pm (10 minutes)", "Post-closing session: 3:50-4:00 pm",
   "Earlier CAS (Jan 2026 circular): 3:15-3:35 pm"],
  [fact("SEBI revised CAS: 3:30 pm to 3:40 pm on all trading days; random close between 3:38 and 3:40 pm; derivatives "
        "till 3:45 pm; post-closing session 3:50-4:00 pm; most provisions from 7 December 2026 (AIR, 16 Oct 2026)",
        "pol_cas_air"),
   fact("SEBI circular dated 15 October 2026 introduces a 10-minute CAS from 3:30 pm to 3:40 pm; earlier January 2026 "
        "circular had a 20-minute CAS from 3:15 to 3:35 pm (Moneylife, search result text)", "pol_cas_ml")],
  why="3:15-3:35 pm was the earlier CAS window; 3:50-4:00 pm is the post-closing session; 3:40-3:50 pm is not a CAS "
      "window in the source.",
  current=ca("2026-10-15", inferred="search-result text gives the circular date as 15 October 2026; AIR dated 16 "
                                    "October says it was issued 'yesterday'"))

G(T, RR, "Intermediate",
  "SEBI's 'Credit Risk-o-Meter', made a mandatory disclosure for debt securities by a circular of 7 October 2026, maps "
  "credit ratings into how many colour-coded risk levels?",
  ["Six", "Four", "Five", "Eight"], "*",
  "Debt market disclosures: Credit Risk-o-Meter",
  "The Credit Risk-o-Meter maps existing credit ratings into six colour-coded levels, from 'Lowest Credit Risk' (AAA, "
  "Irish green) to 'High to Very High Risk of Default' (B+ to D, red); if an issue has several ratings, the lowest is "
  "shown. It must appear in offer documents, abridged prospectuses, private placement memorandums, advertisements and "
  "on the platforms of Online Bond Platform Providers, and applies 45 days after the circular.",
  ["Six colour-coded levels", "Lowest rating shown if several", "Also on OBPP platforms; effective after 45 days"],
  [fact("Circular of 7 October 2026; ratings mapped into six risk categories from Irish green (AAA) to red (B+ to D); "
        "lowest rating used if multiple; mandatory in offer documents and OBPP platforms (LiveLaw Biz)", "pol_crm_ll"),
   fact("SEBI introduces Credit Risk-o-Meter, a colour-coded mandatory disclosure for debt securities, including on "
        "OBPP platforms; effective 45 days after the circular (AIR, 8 Oct 2026)", "pol_crm_air")],
  why="The source lists six risk categories, not four, five or eight.",
  current=ca("2026-10-07"))

GS(T, PC, "Intermediate",
   "the VB-G RAM G - Grievance Redressal Rules, 2026 notified by the Government in November 2026",
   ["State Governments are to set up a three-tier grievance redressal mechanism at the Gram Panchayat, Block and "
    "District levels.",
    "A grievance is to be resolved within 15 days of its receipt."],
   [True, True],
   "Rural employment guarantee: grievance redressal",
   "Under the Grievance Redressal Rules, 2026 for the Viksit Bharat - Guarantee for Rozgar and Ajeevika Mission "
   "(Gramin), States set up a three-tier mechanism at Gram Panchayat, Block and District levels with designated "
   "Grievance Redressal Officers. Enquiry is to be done within 7 working days and the grievance resolved within 15 "
   "days of receipt. Grievances can be filed in person, by speed post, by telephone or through the Centre's digital "
   "grievance platform.",
   [fact("VB-G RAM G Grievance Redressal Rules, 2026: three-tier mechanism at Gram Panchayat, Block and District; "
         "enquiry within 7 working days; resolution within 15 days of receipt (AIR, 2 Nov 2026)", "pol_vbg_air")],
   why="Both statements match the source; 7 working days is the time for the enquiry, not the resolution.",
   current=ca("2026-11-02", inferred="AIR report dated 2 November 2026 gives no separate notification date"))

# ###################################################################### part: appt (appointments + summits)
# ###################################################################### part: appt (Important Appointments, Summits and Conferences)
U.update({
    # ---- Appointments
    "ap_eco_air": ("https://newsonair.gov.in/senegals-president-bassirou-faye-elected-as-new-chairman-of-ecowas/", OPENED),
    "ap_hdfc_ob": ("https://www.outlookbusiness.com/corporate/rbi-approves-ex-chief-election-commissioner-rajiv-kumar-as-"
                   "hdfc-bank-chairman", OPENED),
    "ap_hdfc_fpj": ("https://www.freepressjournal.in/business/hdfc-bank-names-rajiv-kumar-as-part-time-chairman-after-"
                    "market-hours-rbi-approves-three-year-appointment-effective-july-15", SEARCH),
    "ap_ireda_pw": ("https://psuwatch.com/psu-appointments/jatin-kumar-nayak-assumes-charge-as-cmd-of-ireda", OPENED),
    "ap_ireda_sq": ("https://solarquarter.com/2026/10/31/jatin-kumar-nayak-takes-charge-as-the-chairman-and-managing-"
                    "director-of-ireda/", OPENED),
    "ap_bog_gr": ("https://greekreporter.com/2026/06/25/stournaras-sworn-in-historic-third-term-leading-bank-greece/",
                  OPENED),
    "ap_bog_e2d": ("https://www.euro2day.gr/en/article/2357309/stournarass-swearingin-as-governor-of-the-bank-of", SEARCH),
    "ap_syr_an": ("https://www.arabnews.com/node/2643734/middle-east", OPENED),
    "ap_syr_eb": ("https://english.enabbaladi.net/archives/2026/05/sharaa-appoints-safwat-raslan-central-bank-governor/",
                  SEARCH),
    "ap_ilfs_im": ("https://indianmasterminds.com/news/nagaraju-maddirala-appointed-ilfs-chairman-managing-director-"
                   "241919/", OPENED),
    "ap_sib_im": ("https://indianmasterminds.com/news/jose-joseph-kattoor-south-indian-bank-chairman-profile-193340/",
                  OPENED),
    "ap_kcv_im": ("https://indianmasterminds.com/news/who-is-kamlesh-chandra-varshney-irs-sebi-whole-time-member-"
                  "235460/", OPENED),
    "ap_hlc_im": ("https://indianmasterminds.com/news/centre-forms-high-level-banking-committee-viksit-bharat-2047-suresh-"
                  "patel-246887/", OPENED),
    "ap_sbi_im": ("https://indianmasterminds.com/news/sbi-appoints-group-chief-risk-officer-208680/", OPENED),
    "ap_untso_un": ("https://press.un.org/en/2026/sga2447.doc.htm", OPENED),
    "ap_icj_un": ("https://press.un.org/en/2026/sc16499.doc.htm", OPENED),
    # ---- Summits and conferences
    "sm_celac_eeas": ("https://www.eeas.europa.eu/delegations/chile/eu-celac-summit-9-november-2025_en", OPENED),
    "sm_celac_pa": ("https://www.parlament.gv.at/gegenstand/XXVIII/EU/45519", SEARCH),
    "sm_sco_tr": ("https://www.tribuneindia.com/news/india/zero-tolerance-no-whitewashing-jaishankar-on-terrorism-at-sco-"
                  "meeting-in-russia", OPENED),
    "sm_sco_air": ("https://www.newsonair.gov.in/external-affairs-minister-s-jaishankar-meets-russian-president-vladimir-"
                   "putin-in-moscow/", OPENED),
    "sm_ibsa_tr": ("https://www.tribuneindia.com/news/world/no-room-for-double-standards-pm-modi-calls-for-unity-against-"
                   "terrorism-at-ibsa-leaders-meeting-suggests-institutionalised-nsa-level-meetings", OPENED),
    "sm_ibsa_ians": ("https://ianslive.in/pm-narendra-modi-attends-ibsa-leaders-meeting-in-johannesburg--"
                     "20251123134551", SEARCH),
    "sm_brics_air": ("https://newsonair.gov.in/final-brics-finance-ministers-and-central-bank-governors-meeting-kicks-off-"
                     "in-mumbai/", OPENED),
    "sm_g20t_air": ("https://newsonair.gov.in/union-minister-piyush-goyal-to-participate-in-g20-trade-ministers-meeting-"
                    "in-us-today/", OPENED),
    "sm_g20t_air2": ("https://newsonair.gov.in/india-cautions-against-treating-legitimate-national-measures-to-protect-"
                     "food-security-as-weaponisation-of-food/", OPENED),
    "sm_atcm_adn": ("https://english.adnkronos.com/2026/05/11/antarctic-treaty-meeting-starts-in-hiroshima/", OPENED),
    "sm_atcm_bta": ("https://www.bta.bg/en/news/1124412-48th-antarctic-treaty-consultative-meeting-opens-in-hiroshima",
                    SEARCH),
    "sm_iwc_lc": ("https://law.lclark.edu/live/news/59010-professor-chris-wolds-reflections-on-the", OPENED),
    "sm_iwc_inf": ("https://www.informea.org/en/event/iwc70-international-whaling-commission-biennial-commission-meeting",
                   OPENED),
    "sm_ots_cp": ("https://caspianpost.com/analytics/turkistan-summit-digital-rise-of-the-turkic-world-in-age-of-ai",
                  OPENED),
    "sm_ots_24": ("https://24.kg/english/373205_Informal_summit_of_Organization_of_Turkic_States_to_be_held_in_Turkistan/",
                  SEARCH),
})

T = "Important Appointments"
BF, IB = "Banking and finance heads", "International bodies"

# ------------------------------------------------------------------ Appointments: Basic (1)
G(T, IB, "Basic",
  "At the 69th Ordinary Session of the ECOWAS Authority of Heads of State and Government, held in Sierra Leone in July "
  "2026, the President of which country was elected the new Chairman of ECOWAS?",
  ["Senegal", "Ghana", "Nigeria", "Côte d'Ivoire"], "*",
  "Regional organisations: ECOWAS chairmanship",
  "Senegal's President Bassirou Faye was elected Chairman of the Economic Community of West African States at the 69th "
  "Ordinary Session of its Authority of Heads of State and Government, held in Sierra Leone. He succeeded Sierra Leone's "
  "President Julius Maada Bio.",
  ["69th ECOWAS summit, Sierra Leone, July 2026", "New Chairman: President Bassirou Faye of Senegal",
   "Predecessor: Julius Maada Bio (Sierra Leone)"],
  [fact("AIR, 20 July 2026: Senegal's President Bassirou Faye elected new Chairman of ECOWAS at the 69th Ordinary Session "
        "held in Sierra Leone 'yesterday', succeeding Sierra Leone's President Julius Maada Bio", "ap_eco_air")],
  why="The source names Senegal's President; Ghana, Nigeria and Côte d'Ivoire are not mentioned for the post.",
  current=ca("2026-07-19", inferred="AIR report dated 20 July 2026 says the session was held 'yesterday'"))

# ------------------------------------------------------------------ Appointments: Intermediate (10)
G(T, BF, "Intermediate",
  "Former Chief Election Commissioner Rajiv Kumar received RBI approval on 15 July 2026 to become the part-time Chairman "
  "of which private sector bank?",
  ["HDFC Bank", "ICICI Bank", "Axis Bank", "Kotak Mahindra Bank"], "*",
  "Bank chairmen: RBI approval",
  "By a communication dated 15 July 2026, the RBI approved Rajiv Kumar as part-time Chairman of HDFC Bank for three "
  "years. The bank's board had approved him on 29 June 2026. He succeeds interim chairman Keki Mistry. Kumar is a former "
  "Chief Election Commissioner, was Secretary of the Department of Financial Services from 2017 to 2020 and is a 1984-"
  "batch IAS officer of the Jharkhand cadre.",
  ["RBI approval: 15 July 2026", "Post: part-time Chairman, HDFC Bank, three years", "Succeeds interim chairman Keki Mistry"],
  [fact("RBI approved Rajiv Kumar, ex-CEC and 1984-batch IAS (Jharkhand), as HDFC Bank part-time chairman for three "
        "years; RBI communication 15 July 2026; succeeds interim chairman Keki Mistry", "ap_hdfc_ob"),
   fact("HDFC Bank named Rajiv Kumar part-time chairman after RBI approved the three-year appointment effective 15 July",
        "ap_hdfc_fpj")],
  why="The sources concern HDFC Bank only; the appointment is not at ICICI, Axis or Kotak Mahindra Bank.",
  current=ca("2026-07-15"))

G(T, BF, "Intermediate",
  "Jatin Kumar Nayak, earlier Executive Director (Finance) of REC Limited, took charge on 30 October 2026 as Chairman "
  "and Managing Director of which public sector financial institution?",
  ["Indian Renewable Energy Development Agency (IREDA)", "Power Finance Corporation (PFC)",
   "India Infrastructure Finance Company Ltd (IIFCL)", "Solar Energy Corporation of India (SECI)"], "*",
  "PSU finance heads",
  "Jatin Kumar Nayak took charge as CMD of IREDA at its registered office in New Delhi on 30 October 2026, following an "
  "order dated 29 October 2026 and approval of the Appointments Committee of the Cabinet. IREDA is a Navratna CPSE under "
  "the Ministry of New and Renewable Energy. He was earlier Executive Director (Finance) at REC Limited.",
  ["Took charge: 30 October 2026", "Post: CMD, IREDA (Navratna CPSE, MNRE)", "Previous post: ED (Finance), REC Ltd"],
  [fact("Jatin Kumar Nayak took charge as CMD of IREDA at its registered office in New Delhi on October 30 (order dated "
        "29 October 2026); earlier ED (Finance), REC Ltd", "ap_ireda_pw"),
   fact("IREDA is a Navratna CPSE under MNRE; appointment followed ACC approval", "ap_ireda_sq")],
  why="The sources name IREDA; PFC, IIFCL and SECI are not mentioned for this appointment.",
  current=ca("2026-10-30"))

G(T, BF, "Intermediate",
  "Yannis Stournaras was sworn in on 24 June 2026 for a historic third six-year term as Governor of which country's "
  "central bank?",
  ["Greece", "Cyprus", "Portugal", "Italy"], "*",
  "Central bank governors",
  "Yannis Stournaras took the oath for a third six-year term as Governor of the Bank of Greece before President "
  "Konstantinos Tassoulas, with Finance Minister Kyriakos Pierrakakis present. The term runs to 2032, by when he will "
  "have led Greece's central bank for eighteen years.",
  ["Sworn in: 24 June 2026 (Wednesday)", "Third six-year term, to 2032", "Bank of Greece"],
  [fact("GreekReporter, 25 June 2026: Stournaras sworn in 'on Wednesday' before President Tassoulas, with Finance Minister "
        "Pierrakakis present, for a third six-year term leading the Bank of Greece, ending in 2032 (18 years in all)",
        "ap_bog_gr"),
   fact("Stournaras's swearing-in as Governor of the Bank of Greece before Tasoula", "ap_bog_e2d")],
  why="The sources concern the Bank of Greece; the other countries' central banks are not mentioned.",
  current=ca("2026-06-24", inferred="GreekReporter of 25 June 2026 says he was sworn in 'on Wednesday', i.e. 24 June"))

G(T, BF, "Intermediate",
  "Mohammed Safwat Raslan, who had headed the Syrian Development Fund, was appointed on 15 May 2026 as governor of "
  "which country's central bank?",
  ["Syria", "Lebanon", "Iraq", "Jordan"], "*",
  "Central bank governors",
  "On 15 May 2026 Mohammed Safwat Raslan was appointed governor of the Central Bank of Syria. His predecessor, "
  "Abdelkader Husriyeh, was named ambassador to Canada. Raslan had been appointed director-general of the Syrian "
  "Development Fund in 2025.",
  ["Appointed: 15 May 2026", "Post: Governor, Central Bank of Syria", "Predecessor Husriyeh named ambassador to Canada"],
  [fact("Arab News, 15 May 2026: Syria appoints Safwat Raslan as central bank governor; former governor Husriyeh named "
        "ambassador to Canada; Raslan was director-general of the Syrian Development Fund from 2025", "ap_syr_an"),
   fact("Enab Baladi: Sharaa appoints Safwat Raslan Central Bank governor", "ap_syr_eb")],
  why="The sources concern the Central Bank of Syria; the other countries are not mentioned.",
  current=ca("2026-05-15"))

G(T, BF, "Intermediate",
  "By an order dated 12 October 2026, the Ministry of Corporate Affairs designated Nagaraju Maddirala, a former "
  "Secretary of the Department of Financial Services, as Chairman and Managing Director of which company?",
  ["Infrastructure Leasing & Financial Services (IL&FS)", "IFCI Ltd", "India Infrastructure Finance Company Ltd (IIFCL)",
   "National Bank for Financing Infrastructure and Development (NaBFID)"], "*",
  "Finance company heads",
  "The NCLT Mumbai bench appointed Nagaraju Maddirala a director of IL&FS on 1 October 2026, and an MCA order of 12 "
  "October 2026 designated him Chairman and Managing Director for two years from the date he assumes charge. He "
  "succeeds Nand Kishore, whose tenure ended on 30 September 2026. Maddirala, a 1993-batch IAS officer of the Tripura "
  "cadre, was earlier DFS Secretary.",
  ["MCA order: 12 October 2026", "Post: CMD, IL&FS, two years", "Predecessor: Nand Kishore"],
  [fact("MCA order dated 12 Oct 2026 formalised Nagaraju Maddirala as IL&FS chairman and MD for two years from assuming "
        "charge; NCLT Mumbai made him director on 1 Oct 2026; succeeds Nand Kishore; ex-DFS Secretary, 1993 IAS Tripura",
        "ap_ilfs_im")],
  why="The source concerns IL&FS; IFCI, IIFCL and NaBFID are not mentioned for this appointment.",
  current=ca("2026-10-12"))

G(T, BF, "Intermediate",
  "Jose Joseph Kattoor, a former Executive Director of the RBI, became the non-executive part-time Chairman of which "
  "bank with effect from 23 March 2026?",
  ["South Indian Bank", "Federal Bank", "CSB Bank", "Dhanlaxmi Bank"], "*",
  "Bank chairmen",
  "With RBI approval granted on 3 February 2026, Jose Joseph Kattoor became non-executive part-time Chairman of South "
  "Indian Bank for three years from 23 March 2026, succeeding V. J. Kurian. He served the RBI for over 32 years, "
  "including as Executive Director.",
  ["RBI approval: 3 Feb 2026; effective 23 March 2026", "Post: part-time Chairman, South Indian Bank, three years",
   "Predecessor: V. J. Kurian"],
  [fact("Jose Joseph Kattoor, ex-RBI ED, non-executive part-time Chairman of South Indian Bank effective 23 March 2026 for "
        "three years after RBI approval of 3 Feb 2026; succeeds V. J. Kurian; over 32 years at the RBI, retired 2023",
        "ap_sib_im")],
  why="The source concerns South Indian Bank; Federal Bank, CSB Bank and Dhanlaxmi Bank are not mentioned.",
  current=ca("2026-03-23"))

GS(T, BF, "Intermediate", "Kamlesh Chandra Varshney of SEBI",
   ["A DoPT order of 15 September 2026 allows him to continue as a Whole-Time Member of SEBI until he turns 65 on 4 "
    "August 2029, or until further orders.",
    "He is a 1990-batch officer of the Indian Administrative Service."],
   [True, False],
   "Regulator appointments: SEBI",
   "Under a DoPT order dated 15 September 2026, approved by the ACC, Kamlesh Chandra Varshney continues as a Whole-Time "
   "Member of SEBI beyond 19 September 2026, until he attains 65 on 4 August 2029 or until further orders. He is a 1990-"
   "batch Indian Revenue Service (Income Tax) officer, not an IAS officer, and first took charge as WTM on 20 September "
   "2023.",
   [fact("DoPT order dated 15 Sep 2026: Varshney continues as SEBI WTM until age 65 on 4 Aug 2029 or further orders; "
         "1990-batch IRS (Income Tax); first assumed charge 20 Sep 2023", "ap_kcv_im")],
   why="Statement 2 is wrong because the source describes him as a 1990-batch IRS (Income Tax) officer.",
   current=ca("2026-09-15"))

G(T, BF, "Intermediate",
  "The High Level Committee on Banking for Viksit Bharat, constituted by the government in October 2026 to review the "
  "banking sector, is chaired by whom?",
  ["Suresh N. Patel", "Bimal Jalan", "K. V. Kamath", "Urjit Patel"], "*",
  "Committees: banking sector review",
  "The Department of Financial Services constituted the High Level Committee on Banking for Viksit Bharat, announced in "
  "the Union Budget 2026-27, with former Central Vigilance Commissioner Suresh N. Patel as chairman. Its members are RBI "
  "Deputy Governor Shirish Chandra Murmu, former Indian Bank MD and CEO Padmaja Chunduru and former RBI Deputy Governor "
  "N. S. Vishwanathan, with the Joint Secretary (Banking), DFS, as Member Secretary. It has a six-month tenure.",
  ["Chairman: Suresh N. Patel (ex-CVC)", "Members: S. C. Murmu, Padmaja Chunduru, N. S. Vishwanathan",
   "Tenure: six months"],
  [fact("Govt constituted the High Level Committee on Banking for Viksit Bharat chaired by former CVC Suresh N. Patel; "
        "members Murmu, Chunduru, Vishwanathan; six-month tenure; announced in Budget 2026-27 (article 30 Oct 2026)",
        "ap_hlc_im")],
  why="The source names Suresh N. Patel as chairman; the other persons are not named on the committee.",
  current=ca("2026-10-30", inferred="Indian Masterminds report of 30 Oct 2026 says the committee 'has constituted'; "
                                    "no exact order date given"))

G(T, BF, "Intermediate",
  "In a stock exchange filing of 5 June 2026, State Bank of India disclosed the appointment of Ratna Teja Dinakara "
  "Akella as Deputy Managing Director and to which other role?",
  ["Group Chief Risk Officer", "Chief Financial Officer", "Chief Compliance Officer", "Chief Technology Officer"], "*",
  "Bank management appointments",
  "SBI appointed Ratna Teja Dinakara Akella as Deputy Managing Director and Group Chief Risk Officer, as disclosed in a "
  "filing to the stock exchanges on 5 June 2026. He was earlier Chief General Manager of the Risk Management Department "
  "at SBI's Corporate Centre in Mumbai.",
  ["Disclosed: 5 June 2026", "Post: DMD and Group Chief Risk Officer, SBI", "Earlier: CGM, Risk Management Department"],
  [fact("SBI appointed Ratna Teja Dinakara Akella as DMD and Group Chief Risk Officer, disclosed in a filing of 5 June "
        "2026; earlier CGM, Risk Management Department, Corporate Centre, Mumbai", "ap_sbi_im")],
  why="The source names the Group Chief Risk Officer role; the other roles are not mentioned.",
  current=ca("2026-06-05", inferred="source gives only the 5 June 2026 filing date"))

G(T, IB, "Intermediate",
  "On 2 November 2026 the UN Secretary-General appointed Major General Nicholas James Foxall of Australia as Head of "
  "Mission and Chief of Staff of which UN body?",
  ["UN Truce Supervision Organization (UNTSO)", "UN Disengagement Observer Force (UNDOF)",
   "UN Military Observer Group in India and Pakistan (UNMOGIP)", "UN Peacekeeping Force in Cyprus (UNFICYP)"], "*",
  "UN appointments: peacekeeping",
  "Major General Nicholas James Foxall of Australia was appointed Head of Mission and Chief of Staff of the UN Truce "
  "Supervision Organization. He succeeds Major General Patrick Gauchat of Switzerland, whose assignment ended on 28 "
  "February 2026. He was until recently Director-General of Military Operations in the Australian Defence Force.",
  ["SG/A/2447, 2 November 2026", "Post: Head of Mission and Chief of Staff, UNTSO", "Predecessor: Patrick Gauchat"],
  [fact("SG/A/2447, 2 Nov 2026: Maj Gen Nicholas James Foxall (Australia) appointed Head of Mission and Chief of Staff, "
        "UNTSO; succeeds Maj Gen Patrick Gauchat (Switzerland); earlier DG Military Operations, ADF", "ap_untso_un")],
  why="The UN release names UNTSO; UNDOF, UNMOGIP and UNFICYP are not part of this appointment.",
  current=ca("2026-11-02"))

# ------------------------------------------------------------------ Appointments: Advanced (1)
GS(T, IB, "Advanced", "the International Court of Justice (ICJ) elections held on 3 November 2026",
   ["The Security Council and the General Assembly elected five judges whose terms begin on 6 February 2027.",
    "India's Dalveer Bhandari was re-elected to the Court.",
    "Phoebe Okowa of Kenya and Mahmoud Hmoud of Jordan were re-elected."],
   [True, False, True],
   "International bodies: ICJ elections",
   "Voting separately on 3 November 2026, the Security Council and the General Assembly elected Dapo Akande (United "
   "Kingdom), François Alabrune (France), Mahmoud Hmoud (Jordan), Rena Lee (Singapore) and Phoebe Okowa (Kenya) for "
   "nine-year terms beginning 6 February 2027. Hmoud and Okowa were re-elected. The five fill the seats of Ronny "
   "Abraham, Dalveer Bhandari, Leonardo Brant, Hmoud and Okowa, whose terms are expiring, so Bhandari was not re-elected.",
   [fact("SC/16499, 3 Nov 2026: Council and Assembly elected Akande, Alabrune, Hmoud, Rena Lee and Okowa for nine-year "
         "terms beginning 6 Feb 2027; Hmoud and Okowa re-elected; they replace Abraham, Bhandari, Brant, Hmoud, Okowa",
         "ap_icj_un")],
   why="Statement 2 is wrong: the source lists Bhandari among the judges whose terms expire, not among those elected.",
   current=ca("2026-11-03"))

T = "Summits and Conferences"
GBS, HC = "G20, BRICS, SCO and others", "Hosting countries"

# ------------------------------------------------------------------ Summits: Basic (1)
G(T, HC, "Basic",
  "The fourth EU-CELAC Summit, held on 9 November 2025 between the European Union and the Community of Latin American "
  "and Caribbean States, took place in Santa Marta in which country?",
  ["Colombia", "Brazil", "Spain", "Mexico"], "*",
  "Summits: host countries",
  "The fourth EU-CELAC summit was held in Santa Marta, Colombia, on 9 November 2025. It was co-chaired by European "
  "Council President António Costa and Colombian President Gustavo Petro, who held CELAC's pro tempore presidency. "
  "Leaders adopted a joint declaration.",
  ["4th EU-CELAC Summit: Santa Marta, Colombia, 9 Nov 2025", "Co-chairs: António Costa and Gustavo Petro"],
  [fact("EEAS: fourth EU-CELAC summit, Santa Marta, Colombia, 9 November 2025, co-chaired by Costa and Petro (CELAC pro "
        "tempore president); joint declaration adopted", "sm_celac_eeas"),
   fact("Joint declaration of the 4th CELAC-EU Summit (Santa Marta, 9 November 2025)", "sm_celac_pa")],
  why="The sources place the summit in Santa Marta, Colombia; it was not held in the other countries.",
  current=ca("2025-11-09"))

# ------------------------------------------------------------------ Summits: Intermediate (7)
G(T, GBS, "Intermediate",
  "External Affairs Minister S. Jaishankar represented India at the meeting of the SCO Council of Heads of Government "
  "held on 18 November 2025. In which city was it held?",
  ["Moscow", "Minsk", "Astana", "Tashkent"], "*",
  "SCO meetings",
  "Jaishankar addressed the SCO Council of Heads of Government meeting in Moscow on 18 November 2025, calling for zero "
  "tolerance towards terrorism. During the visit he also met Russian President Vladimir Putin along with other heads of "
  "delegation.",
  ["SCO Council of Heads of Government, Moscow, 18 Nov 2025", "India represented by EAM S. Jaishankar"],
  [fact("Tribune (ANI), 18 Nov 2025: Jaishankar addressed the SCO Council of Heads of Government meeting in Moscow",
        "sm_sco_tr"),
   fact("AIR: Jaishankar met Putin in Moscow with other heads of delegation at the SCO Council of Heads of Government",
        "sm_sco_air")],
  why="The sources place the meeting in Moscow; Minsk, Astana and Tashkent are not mentioned.",
  current=ca("2025-11-18"))

G(T, GBS, "Intermediate",
  "At the IBSA (India-Brazil-South Africa) Leaders' Meeting in Johannesburg on 23 November 2025, Prime Minister Modi "
  "proposed institutionalising meetings at which level to strengthen security cooperation?",
  ["National Security Advisers", "Defence Ministers", "Home Ministers", "Chiefs of Defence Staff"], "*",
  "IBSA",
  "At the IBSA Leaders' Meeting, held on the sidelines of the G20 Summit in Johannesburg, Modi noted that the first NSA "
  "meeting of the three countries took place in 2021 and proposed institutionalising it. He also proposed an IBSA "
  "Digital Innovation Alliance and an IBSA Fund for Climate-Resilient Agriculture. The meeting was chaired by Brazil's "
  "President Lula and hosted by South Africa's President Ramaphosa.",
  ["IBSA Leaders' Meeting, Johannesburg, 23 Nov 2025", "Proposal: institutionalise NSA-level meetings (first in 2021)"],
  [fact("Tribune (ANI), 23 Nov 2025: at the IBSA Leaders' Meeting in Johannesburg Modi suggested institutionalising NSA-"
        "level meetings (first held 2021); also proposed IBSA Digital Innovation Alliance and fund for climate-resilient "
        "agriculture", "sm_ibsa_tr"),
   fact("PM Modi attends IBSA Leaders' Meeting in Johannesburg", "sm_ibsa_ians")],
  why="The source says the proposal concerned NSA-level meetings; the other levels are not mentioned.",
  current=ca("2025-11-23"))

G(T, GBS, "Intermediate",
  "The final BRICS Finance Ministers' and Central Bank Governors' meeting under India's 2026 chairship, held on 9-10 "
  "September 2026 ahead of the Leaders' Summit, took place in which city?",
  ["Mumbai", "Bengaluru", "Hyderabad", "Gandhinagar"], "*",
  "BRICS finance track",
  "The final BRICS Finance Ministers' and Central Bank Governors' meeting was held in Mumbai on 9-10 September 2026, "
  "ahead of the BRICS Leaders' Summit, under the theme 'Building for Resilience, Innovation, Cooperation and "
  "Sustainability'. The finance ministers and governors had met in Jaipur the previous month.",
  ["Final BRICS FMCBG meeting: Mumbai, 9-10 Sep 2026", "Previous meeting: Jaipur"],
  [fact("AIR, 9 Sep 2026: final BRICS Finance Ministers' and Central Bank Governors' meeting kicks off in Mumbai, 9-10 "
        "September, ahead of the Leaders' Summit; previous meeting in Jaipur", "sm_brics_air")],
  why="The source places the final meeting in Mumbai; Bengaluru, Hyderabad and Gandhinagar are not mentioned.",
  current=ca("2026-09-09"))

G(T, GBS, "Intermediate",
  "Under the United States' G20 presidency, the G20 Trade Ministers' Meeting of 30 September-1 October 2026, attended "
  "by Commerce Minister Piyush Goyal, was held in which US city?",
  ["Milwaukee", "Chicago", "Detroit", "Houston"], "*",
  "G20 ministerial meetings",
  "The G20 Trade Ministers' Meeting was held in Milwaukee, Wisconsin, under the US G20 presidency. Piyush Goyal "
  "represented India and warned against treating legitimate national measures to protect food security as the "
  "'weaponisation of food'.",
  ["G20 Trade Ministers' Meeting: Milwaukee, Wisconsin", "30 Sep-1 Oct 2026, US presidency"],
  [fact("AIR, 30 Sep 2026: Goyal to attend the G20 Trade Ministers' Meeting in Milwaukee, Wisconsin, today and tomorrow; "
        "US holds the G20 presidency", "sm_g20t_air"),
   fact("AIR, 1 Oct 2026: at the G20 Trade Ministers' Meeting in Milwaukee, India cautioned against calling food security "
        "measures weaponisation of food", "sm_g20t_air2")],
  why="The sources place the meeting in Milwaukee; Chicago, Detroit and Houston are not mentioned.",
  current=ca("2026-09-30"))

G(T, HC, "Intermediate",
  "The 48th Antarctic Treaty Consultative Meeting, which opened on 11 May 2026 in Japan, was held in which city?",
  ["Hiroshima", "Kyoto", "Tokyo", "Osaka"], "*",
  "Conferences: host cities",
  "The 48th Antarctic Treaty Consultative Meeting opened in Hiroshima on 11 May 2026. It was Japan's third time as host, "
  "after Tokyo in 1970 and Kyoto in 1994, and was chaired by Japanese diplomat Hideki Uyama. Tourism regulation and "
  "the protection of emperor penguins were on the agenda.",
  ["ATCM 48: Hiroshima, opened 11 May 2026", "Japan's earlier ATCMs: Tokyo 1970, Kyoto 1994"],
  [fact("Adnkronos, 11 May 2026: 48th Antarctic Treaty consultative meeting starts in Hiroshima; Japan's third time after "
        "Tokyo 1970 and Kyoto 1994; chaired by Hideki Uyama", "sm_atcm_adn"),
   fact("BTA: 48th Antarctic Treaty Consultative Meeting opens in Hiroshima", "sm_atcm_bta")],
  why="Tokyo (1970) and Kyoto (1994) hosted earlier meetings per the source; Osaka is not mentioned; ATCM 48 was in "
      "Hiroshima.",
  current=ca("2026-05-11"))

G(T, HC, "Intermediate",
  "The 70th meeting of the International Whaling Commission (IWC70), which ended on 3 October 2026 with the adoption by "
  "consensus of the Hobart Declaration, was hosted by which country?",
  ["Australia", "New Zealand", "Peru", "Norway"], "*",
  "Conferences: host countries",
  "IWC70 was held at the Grand Chancellor Hotel in Hobart, Australia, in late September-early October 2026. The meeting "
  "concluded on 3 October 2026; its Australian chair called the adoption of the Hobart Declaration a historic consensus. "
  "2026 marks the IWC's 80th anniversary and the 40th year of the moratorium on commercial whaling. A proposal for a "
  "South Atlantic Whale Sanctuary was rejected again.",
  ["IWC70: Hobart, Australia; ended 3 Oct 2026", "Hobart Declaration adopted by consensus"],
  [fact("InforMEA: IWC70 biennial commission meeting, 28 Sep-3 Oct 2026, Grand Chancellor Hotel, Hobart, Australia",
        "sm_iwc_inf"),
   fact("Lewis & Clark Law School: IWC70 in Tasmania, Australia concluded 3 Oct 2026; Hobart Declaration adopted by "
        "consensus; 80th anniversary of IWC; South Atlantic sanctuary rejected", "sm_iwc_lc")],
  why="The sources place IWC70 in Hobart, Australia; New Zealand, Peru and Norway are not named as hosts.",
  current=ca("2026-10-03"))

G(T, HC, "Intermediate",
  "The informal summit of the Organization of Turkic States held on 15 May 2026 on the theme 'Artificial Intelligence "
  "and Digital Development' took place in the city of Turkistan in which country?",
  ["Kazakhstan", "Uzbekistan", "Kyrgyzstan", "Azerbaijan"], "*",
  "Summits: host countries",
  "The Council of Heads of State of the Organization of Turkic States held an informal summit on 15 May 2026 in the "
  "ancient city of Turkistan, Kazakhstan. Its theme was 'Artificial Intelligence and Digital Development', and a joint "
  "statement was issued after the summit.",
  ["OTS informal summit: Turkistan, Kazakhstan, 15 May 2026", "Theme: AI and Digital Development"],
  [fact("Caspian Post: OTS informal summit on 15 May 2026 in the ancient city of Turkistan, Kazakhstan; theme 'Artificial "
        "Intelligence and Digital Development'", "sm_ots_cp"),
   fact("24.kg: Informal summit of Organization of Turkic States to be held in Turkistan", "sm_ots_24")],
  why="The sources place Turkistan in Kazakhstan; the summit was not held in the other member states.",
  current=ca("2026-05-15"))

# ###################################################################### part: awsp (awards + sports)
# ###################################################################### part: awsp (Awards and Honours, Sports)
U.update({
    # ---- National awards
    "aw_dak_air": ("https://newsonair.gov.in/kendriya-grihmantri-dakshata-padak-awarded-to-490-police-personnel-for-2026/",
                   OPENED),
    "aw_dak_dg": ("https://deshgujarat.com/2026/10/31/six-gujarat-cops-awarded-kendriya-grihamantri-dakshata-padak-2026/",
                  SEARCH),
    "aw_nwa_air": ("https://www.newsonair.gov.in/president-murmu-calls-for-collective-efforts-to-ensure-water-security",
                   OPENED),
    "aw_nwa_tag": ("https://www.newsonair.gov.in/tag/6th-national-water-awards", OPENED),
    "aw_sna_air": ("https://newsonair.gov.in/culture-ministry-announces-sangeet-natak-akademi-fellowships-awards-and-ustad-"
                   "bismillah-khan-yuva-puraskar/", OPENED),
    "aw_neca_air": ("https://www.newsonair.gov.in/president-droupadi-murmu-to-felicitate-winners-of-national-energy-"
                    "conservation-awards-2025-in-new-delhi", OPENED),
    "aw_neca_st": ("https://www.thestatesman.com/india/energy-conservation-is-not-just-an-option-but-the-most-crucial-need-"
                   "of-today-prez-murmu-1503525834.html", SEARCH),
    "aw_raj_dd": ("https://ddnews.gov.in/en/dfs-bags-first-prize-in-rajbhasha-kirti-awards-for-hindi-implementation/",
                  OPENED),
    "aw_raj2_dd": ("https://ddnews.gov.in/en/hindi-diwas-2026-amit-shah-to-present-rajbhasha-awards-at-mumbai-conference/",
                   OPENED),
    "aw_lka_dd": ("https://ddnews.gov.in/en/lalit-kala-akademi-announces-20-awards-at-65th-national-exhibition-of-art/",
                  OPENED),
    # ---- International awards
    "aw_agr_fao": ("https://www.fao.org/newsroom/detail/fao-director-general-honours-india-s-prime-minister-narendra-modi-"
                   "with-fao-s-prestigious-agricola-medal/en", OPENED),
    "aw_agr_pmi": ("https://www.pmindia.gov.in/en/news_updates/pm-receives-agricola-medal-from-the-food-and-agriculture-"
                   "organization-fao-of-the-united-nations-in-rome/", SEARCH),
    "aw_god_dc": ("https://www.deccanchronicle.com/technology/chandrayaan-3-receives-2026-aiaa-goddard-astronautics-award-"
                  "1958336", OPENED),
    "aw_god_etv": ("https://www.etvbharat.com/en/technology/india-chandrayaan-3-mission-gets-goddard-astronautics-award-"
                   "from-aiaa-enn26052107075", SEARCH),
    "aw_nmt_air": ("https://newsonair.gov.in/us-president-trump-honours-microsoft-ceo-satya-nadella-and-five-other-tech-"
                   "leaders-with-top-scientific-awards/", OPENED),
    "aw_nmt_tnw": ("https://thenextweb.com/news/national-medal-of-science-musk-huang-su-brin-nadella-dell", OPENED),
    "aw_gg_week": ("https://www.theweek.in/news/entertainment/2026/01/12/golden-globes-2026-the-full-list-of-winners.html",
                   OPENED),
    "aw_gg_bos": ("https://www.boston.com/culture/entertainment/2026/01/11/golden-globes-2026-winners/", SEARCH),
    "aw_baf_ol": ("https://www.outlookindia.com/art-entertainment/bafta-2026-full-winners-list", OPENED),
    "aw_baf_dc": ("https://www.deccanchronicle.com/entertainment/manipuri-film-boong-scripts-history-wins-best-childrens-"
                  "film-at-bafta-2026-1939178", OPENED),
    "aw_emy_npr": ("https://www.nprillinois.org/2026-09-14/emmys-2026-heres-the-list-of-winners", OPENED),
    "aw_emy_abc": ("https://abc7news.com/story/emmys-2026-full-list-winners-nominees-78th-primetime-emmy-awards/19831393/",
                   SEARCH),
    "aw_sas_dd": ("https://www.devdiscourse.com/article/headlines/3982426-stanford-researcher-sarah-peluse-wins-2026-"
                  "sastra-ramanujan-award", OPENED),
    "aw_sas_nk": ("https://www.newkerala.com/news/a/stanford-researcher-sarah-peluse-wins-2026-sastra-ramanujan-award-"
                  "410.htm", SEARCH),
    "aw_qep_eur": ("https://www.eurekalert.org/news-releases/1115305", OPENED),
    "aw_qep_bst": ("https://www.biosciencetoday.co.uk/neural-interface-pioneers-win-2026-queen-elizabeth-prize-for-"
                   "engineering", OPENED),
    "aw_abu_dd": ("https://ddnews.gov.in/en/prasar-bharati-wins-abu-broadcast-engineering-excellence-award-2026/", OPENED),
    "aw_isr_dd": ("https://ddnews.gov.in/en/israel-to-honour-indian-captain-smit-machchhar-with-presidential-award-for-"
                  "civilian-heroism/", OPENED),
    "aw_fao_dd": ("https://ddnews.gov.in/en/mizoram-woman-farmer-to-receive-fao-award/", OPENED),
    # ---- Sports
    "sp_kitg_hit": ("https://www.thehitavada.com/Encyc/2026/4/4/curtains-fall-on-first-kitg-2026-karnataka-tops-medal-"
                    "tally-cm-announces-cash-awards-for-state-medalists.html", OPENED),
    "sp_kitg_ians": ("https://ianslive.in/kitg-2026-karnataka-emerge-overall-champions-chhattisgarh-finishes-ninth-as-"
                     "games-end--20260403231957", SEARCH),
    "sp_io_rep": ("https://www.republicworld.com/sports/badminton/india-open-2026-lin-chun-yi-crushes-jonatan-christie-to-"
                  "lift-men-s-singles-title-an-se-young-takes-home-women-s-singles-top-honour", OPENED),
    "sp_io_mx": ("https://morungexpress.com/india-open-badminton-an-se-young-lin-chun-yi-crowned-womens-and-mens-singles-"
                 "champions", SEARCH),
    "sp_u17_aj": ("https://www.aljazeera.com/sports/2025/11/27/portugal-beat-austria-to-live-fifa-u-17-world-cup-in-qatar",
                  OPENED),
    "sp_u17_pen": ("https://thepeninsulaqatar.com/article/28/11/2025/qatar-successfully-delivers-historic-edition-of-fifa-"
                   "u-17-world-cup", OPENED),
    "sp_ind_nbc": ("https://www.nbcsports.com/olympics/news/world-indoor-track-and-field-championships-results-2026",
                   OPENED),
    "sp_ash_ol": ("https://www.outlookindia.com/sports/hockey/india-vs-belgium-match-report-sultan-azlan-shah-cup-2025-"
                  "final", OPENED),
    "sp_ash_fpj": ("https://www.freepressjournal.in/amp/sports/sultan-azlan-shah-cup-2025-india-settle-for-silver-medal-"
                   "after-hard-fought-0-1-loss-to-belgium", SEARCH),
})

T = "Awards and Honours"
NAT, INTL = "National awards", "International awards"

# ------------------------------------------------------------------ Awards: Basic (7)
G(T, NAT, "Basic",
  "How many police personnel were awarded the Kendriya Grihmantri Dakshata Padak for 2026, announced by the Ministry of "
  "Home Affairs on 31 October 2026?",
  ["490", "375", "520", "610"], "*",
  "Police medals: Kendriya Grihmantri Dakshata Padak",
  "The Ministry of Home Affairs awarded the Kendriya Grihmantri Dakshata Padak for 2026 to 490 personnel of State/UT "
  "police forces, Central Armed Police Forces and Central Police Organisations. The medal, instituted on 1 February "
  "2024, is announced every year on 31 October, the birth anniversary of Sardar Vallabhbhai Patel.",
  ["Dakshata Padak 2026: 490 personnel", "Instituted 1 February 2024; announced each year on 31 October"],
  [fact("Kendriya Grihmantri Dakshata Padak for 2026 awarded to 490 police personnel; instituted 1 Feb 2024; announced "
        "every year on 31 October, Sardar Patel's birth anniversary (AIR, 31 Oct 2026)", "aw_dak_air"),
   fact("Gujarat report of 31 Oct 2026 on the Dakshata Padak 2026 awardees", "aw_dak_dg")],
  why="The source gives 490 awardees; the other numbers do not match it.",
  current=ca("2026-10-31"))

G(T, NAT, "Basic",
  "Which State was ranked first in the Best State category of the 6th National Water Awards (2024), presented by "
  "President Droupadi Murmu in New Delhi on 18 November 2025?",
  ["Maharashtra", "Madhya Pradesh", "Uttar Pradesh", "Tamil Nadu"], "*",
  "National Water Awards",
  "Maharashtra was ranked first in the Best State category of the 6th National Water Awards, with Gujarat second and "
  "Haryana third. In all, 46 winners were chosen across ten categories, and the first Jal Sanchay Jan Bhagidari Awards "
  "were presented at the same ceremony.",
  ["Best State: 1 Maharashtra, 2 Gujarat, 3 Haryana", "46 winners, 10 categories"],
  [fact("President Murmu presented the 6th National Water Awards 2024 and the first Jal Sanchay Jan Bhagidari Awards on "
        "18 Nov 2025; Best State: Maharashtra 1st, Gujarat 2nd, Haryana 3rd; 46 winners in ten categories", "aw_nwa_air"),
   fact("AIR, 11 Nov 2025: Maharashtra tops 6th National Water Awards 2024", "aw_nwa_tag")],
  why="The source names Maharashtra first (Gujarat second, Haryana third); the other States are not among the top three.",
  current=ca("2025-11-18"))

G(T, INTL, "Basic",
  "On 20 May 2026, Prime Minister Narendra Modi received the Agricola Medal at the Plenary Hall of which organisation's "
  "headquarters in Rome?",
  ["Food and Agriculture Organization (FAO)", "International Fund for Agricultural Development (IFAD)",
   "World Food Programme (WFP)", "United Nations Environment Programme (UNEP)"], "*",
  "International honours to the Prime Minister",
  "FAO Director-General Qu Dongyu presented the FAO Agricola Medal, the organisation's highest award, to Prime Minister "
  "Modi in the Plenary Hall of FAO headquarters in Rome on 20 May 2026. The medal goes to leaders committed to FAO's "
  "mandate of ending hunger and ensuring food security and nutrition.",
  ["Agricola Medal: highest award of FAO", "Presented by DG Qu Dongyu, Rome, 20 May 2026"],
  [fact("FAO DG Qu Dongyu presented the FAO Agricola Medal, FAO's highest award, to PM Modi in the Plenary Hall at FAO "
        "headquarters, Rome, 20 May 2026", "aw_agr_fao"),
   fact("PMO release: PM receives Agricola Medal from FAO in Rome", "aw_agr_pmi")],
  why="The sources say the Agricola Medal is FAO's own award; the other UN bodies did not confer it.",
  current=ca("2026-05-20"))

G(T, INTL, "Basic",
  "Which film won Best Motion Picture – Drama at the 83rd Golden Globe Awards held in January 2026?",
  ["Hamnet", "Sinners", "Frankenstein", "Sentimental Value"], "*",
  "Film awards: Golden Globes",
  "'Hamnet' won Best Motion Picture – Drama at the 83rd Golden Globes, and Jessie Buckley won Best "
  "Actress – Drama for it. 'Sinners', 'Frankenstein' and 'Sentimental Value' were among the other nominees in the "
  "category.",
  ["83rd Golden Globes: Best Drama film = Hamnet", "Jessie Buckley: Best Actress – Drama"],
  [fact("83rd Golden Globes: Best Motion Picture, Drama - Hamnet; Best Actress, Drama - Jessie Buckley (Hamnet)",
        "aw_gg_week"),
   fact("Golden Globes of 11 Jan 2026: Hamnet won Drama; other nominees Frankenstein, It Was Just An Accident, The Secret "
        "Agent, Sentimental Value, Sinners", "aw_gg_bos")],
  why="'Sinners', 'Frankenstein' and 'Sentimental Value' were nominees in the category but did not win.",
  current=ca("2026-01-11"))

G(T, INTL, "Basic",
  "Z T Lalrithangi of Lawngtlai district, Mizoram, selected in September 2026 as one of the FAO '100 Women Heroes in "
  "Agrifood Systems and Rural Development', is known for turning the cultivation of which crop into a profitable "
  "livelihood?",
  ["Strawberry", "Kiwi", "Dragon fruit", "Passion fruit"], "*",
  "International recognition: FAO",
  "Z T Lalrithangi, a former teacher from Sangau in Lawngtlai district, grows over 10,000 strawberry plants on two "
  "hectares. FAO selected her among its '100 Women Heroes' during the International Year of Women Farmers 2026, with "
  "the honour to be presented at the World Food Forum in Rome.",
  ["Lalrithangi (Mizoram): strawberry farmer", "FAO 100 Women Heroes; International Year of Women Farmers 2026"],
  [fact("Mizoram farmer Z T Lalrithangi selected among FAO 100 Women Heroes in Agrifood Systems and Rural Development "
        "for making strawberry cultivation profitable; FAO notified her on 21 September (DD News, 24 Sep 2026)",
        "aw_fao_dd")],
  why="The source credits her strawberry cultivation; the other crops are not mentioned.",
  current=ca("2026-09-21"))

G(T, INTL, "Basic",
  "A Prasar Bharati engineer won the Asia-Pacific Broadcasting Union (ABU) Broadcast Engineering Excellence Award 2026, "
  "received at the 63rd ABU General Assembly in October 2026. In which city was that General Assembly held?",
  ["Colombo", "Kuala Lumpur", "Bangkok", "Dhaka"], "*",
  "International awards: broadcasting",
  "Nongmaithem Nandakumar Singh of Prasar Bharati won the ABU Broadcast Engineering Excellence Award 2026 for DDPlayout, "
  "an indigenous automated playout software, and DDSlowMo, a low-cost slow-motion replay system. The award was "
  "received on his behalf at the 63rd ABU General Assembly in Colombo (30 October to 3 November 2026).",
  ["ABU Broadcast Engineering Excellence Award 2026: Prasar Bharati engineer", "63rd ABU General Assembly: Colombo"],
  [fact("Prasar Bharati engineer Nongmaithem Nandakumar Singh won the ABU Broadcast Engineering Excellence Award 2026 "
        "for DDPlayout and DDSlowMo; received at the 63rd ABU General Assembly in Colombo, 30 Oct-3 Nov (DD News, "
        "30 Oct 2026)", "aw_abu_dd")],
  why="The source places the 63rd ABU General Assembly in Colombo; the other cities are not mentioned.",
  current=ca("2026-10-30", inferred="DD News report dated 30 Oct 2026 announces the win; no separate presentation day"))

G(T, INTL, "Basic",
  "In October 2026, Israeli President Isaac Herzog announced that Indian pilot Captain Smit Machchhar, who fought off "
  "an attack in the cockpit of a flydubai Dubai–Tel Aviv flight, would receive which award?",
  ["Presidential Award for Civilian Heroism", "Israel Prize", "Presidential Medal of Distinction", "Wolf Prize"], "*",
  "International honours to Indians",
  "President Herzog announced the Presidential Award for Civilian Heroism, which he established after 7 October and "
  "which DD News describes as Israel's highest civilian award for heroism, for Captain Smit Machchhar. On 30 September "
  "2026 the captain, though stabbed, fought off his co-pilot's attack and helped save 172 passengers and crew. Herzog "
  "said he would present the award once the captain recovers.",
  ["Capt Smit Machchhar: Presidential Award for Civilian Heroism (announced)", "Award to be presented after recovery"],
  [fact("Herzog announced the Presidential Award for Civilian Heroism for Capt Smit Machchhar, pilot of flydubai Flight "
        "1073, who fought off a cockpit attack on 30 Sep 2026; announced at a ceremony on Thursday, reported 9 Oct 2026",
        "aw_isr_dd")],
  why="The source names the Presidential Award for Civilian Heroism; the other awards are not mentioned.",
  current=ca("2026-10-08", inferred="DD News of Friday 9 Oct 2026 says Herzog announced it at a ceremony on Thursday"))

# ------------------------------------------------------------------ Awards: Intermediate (2)
G(T, INTL, "Intermediate",
  "In May 2026, ISRO's Chandrayaan-3 mission received which award, the highest honour of the American Institute of "
  "Aeronautics and Astronautics (AIAA) for achievements in astronautics?",
  ["Goddard Astronautics Award", "Space Systems Award", "Lawrence Sperry Award", "Durand Lectureship"], "*",
  "International awards: space",
  "The 2026 AIAA Goddard Astronautics Award was presented for Chandrayaan-3 at the AIAA ASCEND 2026 conference in "
  "Washington, D.C., on 21 May 2026; Ambassador Vinay Kwatra received it for ISRO. The award is named after rocket "
  "pioneer Robert H. Goddard.",
  ["Chandrayaan-3: AIAA Goddard Astronautics Award 2026", "Presented 21 May 2026 at AIAA ASCEND, Washington, D.C."],
  [fact("Chandrayaan-3 received the 2026 AIAA Goddard Astronautics Award, AIAA's highest honour in astronautics; "
        "presented 21 May 2026 at AIAA ASCEND 2026, Washington, D.C.; received by Ambassador Vinay Kwatra",
        "aw_god_dc"),
   fact("ETV Bharat: India's Chandrayaan-3 mission gets Goddard Astronautics Award from AIAA", "aw_god_etv")],
  why="The sources name the Goddard Astronautics Award; the other AIAA honours are not mentioned for the mission.",
  current=ca("2026-05-21"))

G(T, INTL, "Intermediate",
  "The 2026 Queen Elizabeth Prize for Engineering, announced at the Science Museum, London, on 3 February 2026, was "
  "shared by nine engineers for developing which technology?",
  ["Modern neural interfaces such as cochlear implants and brain-computer interfaces", "Lithium-ion batteries",
   "Satellite navigation systems", "Perovskite solar cells"], "*",
  "International awards: engineering",
  "Nine engineers shared the 2026 QEPrize for modern neural interfaces that restore human function: cochlear implants "
  "(Graeme Clark, Erwin and Ingeborg Hochmair, Blake Wilson), deep brain stimulation (Alim Louis Benabid, Pierre "
  "Pollak), brain-computer interfaces (John Donoghue) and electronic spinal stimulation (Jocelyne Bloch, Grégoire "
  "Courtine). The prize is worth £500,000.",
  ["QEPrize 2026: modern neural interfaces", "Nine laureates; £500,000"],
  [fact("2026 QEPrize announced Tuesday 3 February at the Science Museum, London, to nine engineers for modern neural "
        "interfaces", "aw_qep_eur"),
   fact("Laureates by technology (cochlear implants, DBS, BCI, spinal stimulation); prize £500,000", "aw_qep_bst")],
  why="The sources cite neural interfaces; the other technologies are not mentioned.",
  current=ca("2026-02-03"))

# ------------------------------------------------------------------ Awards: Advanced (8)
GS(T, NAT, "Advanced", "the Sangeet Natak Akademi awards for 2024 and 2025 announced by the Culture Ministry in June 2026",
   ["108 artists were selected for the Akademi Puraskar.",
    "The Akademi Fellowship carries a purse of ₹3 lakh.",
    "The Ustad Bismillah Khan Yuva Puraskar is conferred by the President at a special investiture ceremony."],
   [True, True, False],
   "Performing arts awards",
   "For 2024 and 2025, 108 artists were chosen for the Akademi Puraskar (₹1 lakh each) and 106 young artists for the "
   "Ustad Bismillah Khan Yuva Puraskar (₹25,000). The Fellowship carries ₹3 lakh. The Fellowship and Akademi Puraskar "
   "are conferred by the President, while the Yuva Puraskar is presented by the Chairman of the Akademi.",
   [fact("108 artists for Akademi Puraskar; 106 for Yuva Puraskar; Fellowship ₹3 lakh, Puraskar ₹1 lakh, Yuva ₹25,000; "
         "Fellowship and Puraskar conferred by the President, Yuva Puraskar by the SNA Chairman (AIR, 11 Jun 2026)",
         "aw_sna_air")],
   why="Statement 3 is wrong: the Yuva Puraskar is presented by the Chairman of the Sangeet Natak Akademi.",
   current=ca("2026-06-11"))

GS(T, NAT, "Advanced", "the National Energy Conservation Awards (NECA) 2025",
   ["They were presented in New Delhi on 14 December 2025, National Energy Conservation Day, by President Droupadi "
    "Murmu.",
    "Andhra Pradesh was ranked first among the States in Group 1.",
    "More than 83 lakh students took part in the National Painting Competition on Energy Conservation 2025."],
   [True, False, True],
   "Energy conservation awards",
   "President Droupadi Murmu presented NECA 2025 on National Energy Conservation Day, 14 December 2025. First-place "
   "State winners were Karnataka (Group 1), Andhra Pradesh (Group 2), Kerala (Group 3), Assam (Group 4) and Chandigarh "
   "(Group 5). Over 83 lakh students from more than 1.1 lakh schools took part in the painting competition.",
   [fact("President Murmu to felicitate NECA 2025 winners in New Delhi on 14 Dec 2025 (National Energy Conservation Day); "
         "first-place States: Karnataka G1, Andhra Pradesh G2, Kerala G3, Assam G4, Chandigarh G5; painting competition "
         "drew over 83 lakh students from 1.1 lakh schools", "aw_neca_air"),
    fact("President Murmu's address at the NECA 2025 ceremony", "aw_neca_st")],
   why="Statement 2 is wrong: Karnataka was first in Group 1; Andhra Pradesh topped Group 2.",
   current=ca("2025-12-14"))

GS(T, NAT, "Advanced", "the Rajbhasha awards for 2025-26 presented in September 2026",
   ["Union Home Minister Amit Shah presented the Rajbhasha Gaurav and Rajbhasha Kirti Awards at the 6th All India "
    "Official Language Conference in Navi Mumbai.",
    "The Department of Financial Services won first prize in the Rajbhasha Kirti Awards in the category of ministries "
    "and departments with fewer than 300 personnel.",
    "The conference was organised by the Ministry of Culture."],
   [True, True, False],
   "Official language awards",
   "The 6th All India Official Language Conference and Hindi Diwas was held on 14-15 September 2026 at the CIDCO "
   "Exhibition Centre, Vashi, Navi Mumbai. Amit Shah presented the Rajbhasha Gaurav and Kirti Awards for 2025-26; the "
   "Department of Financial Services took first prize in the Kirti category for bodies with fewer than 300 personnel. "
   "The conference is organised by the Department of Official Language, Ministry of Home Affairs.",
   [fact("DFS won first prize under Rajbhasha Kirti Awards 2025-26 (ministries/departments with fewer than 300 personnel), "
         "received from Amit Shah at the 6th All India Official Language Conference, Navi Mumbai, 14 Sep 2026",
         "aw_raj_dd"),
    fact("Conference organised by the Department of Official Language, MHA; Amit Shah to present Rajbhasha Gaurav and "
         "Kirti Awards 2025-26", "aw_raj2_dd")],
   why="Statement 3 is wrong: the organiser is the Department of Official Language under the Ministry of Home Affairs.",
   current=ca("2026-09-14"))

GS(T, NAT, "Advanced", "the Lalit Kala Akademi awards announced in September 2026",
   ["They were announced at the 64th National Exhibition of Art.",
    "Twenty artists were selected for the awards.",
    "The exhibition received 6,175 artworks from 2,495 artists across 27 States and Union Territories."],
   [False, True, True],
   "Visual arts awards",
   "The Lalit Kala Akademi, the National Academy of Art, announced 20 awards at its 65th National Exhibition of Art. "
   "Of 6,175 entries from 2,495 artists in 27 States/UTs, a first-tier jury picked 270 works for display and a "
   "second-tier jury chose the 20 award-winning works.",
   [fact("Lalit Kala Akademi announced 20 awards at the 65th National Exhibition of Art on a Sunday; 6,175 artworks from "
         "2,495 artists across 27 States/UTs (DD News, 28 Sep 2026)", "aw_lka_dd")],
   why="Statement 1 is wrong: it was the 65th National Exhibition of Art.",
   current=ca("2026-09-27", inferred="DD News of Monday 28 Sep 2026 says the awards were announced on Sunday"))

GS(T, INTL, "Advanced", "the US National Medals presented at the White House in October 2026",
   ["Microsoft CEO Satya Nadella received the National Medal of Science.",
    "Elon Musk, Sergey Brin, Jensen Huang and Lisa Su received the National Medal of Science.",
    "The National Medal of Technology has been awarded since 1985."],
   [False, True, True],
   "International awards: science and technology",
   "On 8 October 2026 at the 'Science: A New Golden Age' summit, President Trump gave the National Medal of Technology "
   "and Innovation to Satya Nadella and Michael Dell, and the National Medal of Science to Elon Musk, Sergey Brin, Jensen "
   "Huang and Lisa Su. The Medal of Science dates from 1963 and the technology medal from 1985.",
   [fact("Nadella and Dell: National Medal of Technology and Innovation; Musk, Brin, Huang, Su: National Medal of "
         "Science (AIR)", "aw_nmt_air"),
    fact("Ceremony Thursday 8 Oct 2026; Medal of Science awarded since 1963, Medal of Technology since 1985",
         "aw_nmt_tnw")],
   why="Statement 1 is wrong: Nadella received the National Medal of Technology and Innovation.",
   current=ca("2026-10-08"))

GS(T, INTL, "Advanced", "the 79th British Academy Film Awards (BAFTA) held on 22 February 2026",
   ["'One Battle After Another' won Best Film.",
    "'Boong', a Manipuri feature film directed by Lakshmipriya Devi, won Best Children's and Family Film.",
    "The ceremony was held at the Royal Albert Hall, London."],
   [True, True, False],
   "Film awards: BAFTA",
   "Paul Thomas Anderson's 'One Battle After Another' won Best Film and five other awards at the 79th BAFTAs, hosted by "
   "Alan Cumming at the Royal Festival Hall, London. 'Boong', backed by Excel Entertainment, won Best Children's and "
   "Family Film; 'Hamnet' won Outstanding British Film.",
   [fact("79th BAFTAs, 22 Feb 2026, Royal Festival Hall, London; Best Film: One Battle After Another (six awards); "
         "Boong won Best Children's and Family Film", "aw_baf_ol"),
    fact("Manipuri feature film 'Boong', directed by Lakshmipriya Devi, won Best Children's and Family Film at the 79th "
         "BAFTAs at the Royal Festival Hall", "aw_baf_dc")],
   why="Statement 3 is wrong: the venue was the Royal Festival Hall.",
   current=ca("2026-02-22"))

GS(T, INTL, "Advanced", "the 78th Primetime Emmy Awards held on 14 September 2026",
   ["'The Pitt' won Outstanding Drama Series.",
    "Matthew Rhys became the first person to win two lead acting categories on the same night.",
    "'Widow's Bay' won Outstanding Comedy Series."],
   [True, True, True],
   "Television awards: Emmys",
   "'The Pitt' won Outstanding Drama Series and Noah Wyle won lead actor in drama. 'Widow's Bay' won Outstanding Comedy "
   "Series, and its star Matthew Rhys, who also won lead actor in a limited series for 'The Beast in Me', became the "
   "first person to win two lead acting Emmys in one night.",
   [fact("Emmys of 14 Sep 2026: Drama - The Pitt; Comedy - Widow's Bay; Matthew Rhys first person to win two lead acting "
         "categories in one night", "aw_emy_npr"),
    fact("78th Primetime Emmy Awards winners list", "aw_emy_abc")],
   why="All three statements are correct.",
   current=ca("2026-09-14"))

GS(T, INTL, "Advanced", "the SASTRA Ramanujan Prize 2026",
   ["It was awarded to Sarah Peluse, an associate professor of mathematics at Stanford University.",
    "The prize carries USD 100,000 along with a citation.",
    "The laureate's doctoral adviser, Kannan Soundararajan, shared the inaugural award in 2005, the first time an "
    "adviser and a student have both received it."],
   [True, False, True],
   "International awards: mathematics",
   "SASTRA University announced on 25 September 2026 that Stanford's Sarah Peluse had won the prize for work in analytic "
   "number theory, additive combinatorics, combinatorial geometry and group theory. It carries USD 10,000 and a "
   "citation and is presented on 22 December, Ramanujan's birth anniversary, at SASTRA's Kumbakonam campus.",
   [fact("2026 SASTRA-Ramanujan award to Sarah Peluse (Stanford); USD 10,000 and citation; adviser Kannan Soundararajan "
         "shared inaugural 2005 award, first adviser-student pair; announced 25 Sep 2026", "aw_sas_dd"),
    fact("NewKerala: Stanford researcher Sarah Peluse wins 2026 SASTRA-Ramanujan award", "aw_sas_nk")],
   why="Statement 2 is wrong: the prize is USD 10,000.",
   current=ca("2026-09-25"))

# ====================================================================== Sports
T = "Sports"
TW, VR = "Tournaments and winners", "Venues and records"

G(T, TW, "Basic",
  "Which State emerged as the overall champion of the inaugural Khelo India Tribal Games, which concluded in Raipur, "
  "Chhattisgarh, on 3 April 2026?",
  ["Karnataka", "Odisha", "Jharkhand", "Chhattisgarh"], "*",
  "Khelo India Tribal Games",
  "Karnataka topped the first Khelo India Tribal Games with 38 medals (23 gold, 8 silver, 7 bronze). Odisha came second "
  "and Jharkhand third. Events in nine disciplines were held in Raipur, Jagdalpur and Ambikapur.",
  ["KITG 2026 (first edition): Karnataka overall champion", "Odisha 2nd, Jharkhand 3rd"],
  [fact("First KITG closed in Raipur on Friday 3 Apr 2026; Karnataka champion (23-8-7), Odisha 2nd, Jharkhand 3rd",
        "sp_kitg_hit"),
   fact("IANS: KITG 2026 - Karnataka overall champions, Chhattisgarh ninth", "sp_kitg_ians")],
  why="The source ranks Odisha second and Jharkhand third; host Chhattisgarh finished ninth.",
  current=ca("2026-04-03"))

G(T, TW, "Intermediate",
  "Which player retained the women's singles title at the India Open 2026 (BWF Super 750) in New Delhi, beating China's "
  "Wang Zhi Yi in the final on 18 January 2026?",
  ["An Se Young", "Akane Yamaguchi", "Chen Yufei", "P. V. Sindhu"], "*",
  "Badminton: India Open",
  "Defending champion and world No. 1 An Se Young of Korea beat Wang Zhi Yi 21-13, 21-11 to retain the India Open "
  "title. Lin Chun-Yi of Chinese Taipei won the men's singles, beating Jonatan Christie 21-10, 21-18 for his first "
  "Super 750 title.",
  ["India Open 2026 WS: An Se Young (retained)", "MS: Lin Chun-Yi"],
  [fact("India Open 2026 (Super 750), 18 Jan 2026: defending champion An Se Young bt Wang Zhi Yi 21-13, 21-11; Lin "
        "Chun-Yi bt Jonatan Christie", "sp_io_rep"),
   fact("India Open Badminton: An Se Young, Lin Chun-Yi crowned singles champions", "sp_io_mx")],
  why="The sources name An Se Young as champion; the other players were not in the final.",
  current=ca("2026-01-18"))

GS(T, VR, "Advanced", "the FIFA U-17 World Cup 2025 held in Qatar",
   ["It was the first FIFA tournament to feature 48 teams.",
    "The final was played at Lusail Stadium.",
    "Portugal beat Austria 1-0 in the final to win the title for the first time."],
   [True, False, True],
   "Football: youth world cups",
   "Matches were played at the Aspire Zone, and the final at Khalifa International Stadium, Doha, on 27 November 2025, "
   "where Anisio Cabral's goal gave Portugal a 1-0 win over Austria and a first title. Italy took bronze. The 48-team "
   "edition was the first FIFA competition of that size.",
   [fact("Portugal beat Austria 1-0 at Khalifa International Stadium, Doha, 27 Nov 2025, for their first U-17 World Cup",
         "sp_u17_aj"),
    fact("48 teams, first FIFA competition to feature that many; matches at Aspire Zone, final at Khalifa International "
         "Stadium", "sp_u17_pen")],
   why="Statement 2 is wrong: the final was at Khalifa International Stadium.",
   current=ca("2025-11-27"))

GS(T, VR, "Advanced", "the World Athletics Indoor Championships 2026",
   ["They were held in Toruń, Poland, from 20 to 22 March 2026.",
    "Switzerland's Simon Ehammer set an indoor world record in the men's heptathlon.",
    "17-year-old Cooper Lutkenhaus of the USA won the men's 800 m, becoming the youngest individual medallist in the "
    "championships' history."],
   [True, True, True],
   "Athletics: world indoor championships",
   "At Toruń, Simon Ehammer won the heptathlon with an indoor world record of 6,670 points and Devynne Charlton won the "
   "60 m hurdles in 7.65. Cooper Lutkenhaus won the 800 m in 1:44.24, and Mondo Duplantis took his fourth world indoor "
   "pole vault title.",
   [fact("Torun, Poland, 20-22 Mar 2026; Ehammer heptathlon 6,670 indoor world record; Lutkenhaus, 17, won 800m, "
         "youngest individual medallist in Indoor Worlds history", "sp_ind_nbc")],
   why="All three statements are correct.",
   current=ca("2026-03-22"))

GS(T, TW, "Advanced", "the Sultan Azlan Shah Cup 2025 hockey tournament in Malaysia, in which India finished runner-up",
   ["The final was decided in a penalty shoot-out after a goalless draw.",
    "Belgium won the title for the first time.",
    "It was the 31st edition of the tournament."],
   [False, True, True],
   "Hockey: invitational tournaments",
   "Belgium beat India 1-0 in the final on 30 November 2025, Thibeau Stockbroekx scoring in the 34th minute. It was "
   "Belgium's maiden title, in only their second appearance at the 31st edition of the tournament.",
   [fact("31st Sultan Azlan Shah Cup final, 30 Nov 2025: Belgium 1-0 India (Stockbroekx 34'); Belgium's maiden title",
         "sp_ash_ol"),
    fact("India settle for silver after 0-1 loss to Belgium", "sp_ash_fpj")],
   why="Statement 1 is wrong: Belgium won 1-0 in regulation time.",
   current=ca("2025-11-30"))

# ###################################################################### part: org (organizations + days)
# ###################################################################### part: org (Organizations + Important Days)
U.update({
    # ---- Organizations: static
    "org_spices": ("https://www.indianspices.com/", OPENED),
    "org_tea_home": ("https://www.teaboard.gov.in/", OPENED),
    "org_tea_addr": ("https://teaboard.gov.in/TEABOARDCSM/MTEx", OPENED),
    "org_nddb": ("https://www.nddb.coop/about/genesis", OPENED),
    "org_mpeda": ("https://mpeda.gov.in/", OPENED),
    "org_ilo_bio": ("https://www.ilo.org/resource/other/biography-gilbert-f-houngbo-11th-ilo-director-general", OPENED),
    "org_ilo_dg": ("https://www.ilo.org/about-ilo/ilo-director-general", OPENED),
    "org_who_dg": ("https://www.who.int/director-general/biography", OPENED),
    "org_ibca_air": ("https://www.newsonair.gov.in/framework-agreement-on-establishment-of-international-big-cat-alliance-"
                     "officially-comes-into-force", OPENED),
    "org_ecowas_hq": ("https://www.ecowas.int/h-e-julius-maada-bio-commissions-new-ecowas-commission-headquarters-"
                      "heralding-a-new-era-of-regional-integration/", OPENED),
    "org_ecowas_td": ("https://www.thisdaylive.com/2026/07/03/ecowas-commissions-landmark-abuja-headquarters-as-nigeria-"
                      "china-renew-commitment-to-regional-integration/", OPENED),
    # ---- Organizations: membership
    "org_epo_news": ("https://www.epo.org/en/news-events/news/republic-moldova-become-40th-epo-member-state", OPENED),
    "org_epo_pr": ("https://www.epo.org/en/news-events/press-centre/press-release/2026/1362566", OPENED),
    "org_laos_cgtn": ("https://news.cgtn.com/news/2026-07-10/Laos-officially-becomes-SCO-dialogue-partner-1OEYFdMJQkw/"
                      "p.html", OPENED),
    "org_paris_bt": ("https://www.brusselstimes.com/1934812/us-leaves-paris-climate-agreement-again-despite-being-worlds-"
                     "2nd-largest-emitter", OPENED),
    "org_paris_ee": ("https://www.eenews.net/articles/so-long-paris-us-officially-leaves-landmark-climate-pact/", SEARCH),
    "org_ecowas_an": ("https://www.africanews.com/2025/01/29/ecowas-confirms-exit-of-the-alliance-of-sahel-states-from-"
                      "the-regional-bloc/", OPENED),
    "org_ecowas_ah": ("https://english.ahram.org.eg/NewsContent/2/10/539454/World/Africa/Burkina-Faso,-Mali-and-Niger-"
                      "officially-leave-West.aspx", SEARCH),
    "org_jordan_tt": ("https://telanganatoday.com/jordan-joins-india-led-isa-cdri-and-global-biofuel-alliance", OPENED),
    "org_jordan_lm": ("https://www.lokmattimes.com/international/jordan-joins-india-led-global-initiatives-isa-cdri-and-"
                      "gba/", SEARCH),
    # ---- Important Days
    "day_malaria": ("https://www.who.int/campaigns/world-malaria-day/2026", OPENED),
    "day_tobacco": ("https://www.who.int/news/item/17-10-2025-world-no-tobacco-day-2026--unmasking-the-appeal---"
                    "countering-nicotine-and-tobacco-addiction", OPENED),
    "day_wtisd": ("https://newsonair.gov.in/world-telecommunication-and-information-society-day-digital-lifelines-"
                  "strengthening-resilience-in-a-connected-world/", OPENED),
    "day_ip": ("https://www.wipo.int/en/web/ipday/2026/index", OPENED),
    "day_mh": ("https://wfmh.global/news/2026.26-08-11_world-mental-health-day-2026", OPENED),
    "day_wmo": ("https://wmo.int/about-wmo/world-meteorological-day", OPENED),
    "day_habitat": ("https://unhabitat.org/sites/default/files/2026/10/press_release_whd_2026.pdf", OPENED),
    "day_habitat_ma": ("https://unhabitat.org/sites/default/files/2026/10/media_advisory_whd_2026.pdf", SEARCH),
    "day_teachers": ("https://www.unesco.org/en/days/teachers-day", OPENED),
    "day_hep_un": ("https://transcripts.un.org/en/briefing/geneva/2026-07-28.txt", OPENED),
    "day_hep_sa": ("https://www.sanews.gov.za/south-africa/world-hepatitis-day-observed", SEARCH),
})

T = "National and International Organizations"
HQ, MEM = "Headquarters and heads", "Membership"

# ------------------------------------------------------------------ Organizations: Basic (2)
G(T, HQ, "Basic",
  "The Spices Board, the statutory body under the Ministry of Commerce and Industry that promotes the export of Indian "
  "spices, has its head office in which city?",
  ["Kochi", "Kolkata", "Bengaluru", "Guntur"], "*",
  "Commodity boards: head offices",
  "The Spices Board functions under the Union Ministry of Commerce and Industry, and its head office is in Kochi, "
  "Kerala.",
  ["Spices Board -> Ministry of Commerce and Industry", "Head office: Kochi (Kerala)"],
  [fact("Spices Board website refers to 'Spices Board, Head Office, Kochi' and lists the Ministry of Commerce and "
        "Industry", "org_spices")],
  why="The Board's own website gives Kochi as its head office; the other cities are not named for it.")

G(T, HQ, "Basic",
  "The Tea Board India, constituted on 1 April 1954 under Section 4 of the Tea Act, 1953, has its head office in which "
  "city?",
  ["Kolkata", "Guwahati", "Kochi", "Darjeeling"], "*",
  "Commodity boards: head offices",
  "The Tea Board was constituted on 1 April 1954 under Section 4 of the Tea Act, 1953, and works under the Department of "
  "Commerce, Ministry of Commerce and Industry. Its head office is at 14 B.T.M. Sarani (Brabourne Road), Kolkata.",
  ["Tea Act, 1953 (Section 4) -> Tea Board, 1 April 1954", "Head office: 14 B.T.M. Sarani, Kolkata"],
  [fact("Tea Board constituted on 1 April 1954 under Section 4 of the Tea Act, 1953; Department of Commerce, Ministry of "
        "Commerce and Industry", "org_tea_home"),
   fact("Tea Board India office address: 14 B.T.M. Sarani (Brabourne Road), Kolkata 700 001", "org_tea_addr")],
  why="The Tea Board's official site gives a Kolkata address; the other cities are not its head office.")

# ------------------------------------------------------------------ Organizations: Intermediate (9)
G(T, HQ, "Intermediate",
  "The National Dairy Development Board (NDDB), founded in 1965, is headquartered in which town?",
  ["Anand", "Karnal", "Mehsana", "Bengaluru"], "*",
  "Indian institutions: head offices",
  "NDDB was founded in 1965; its address is Anand - 388 001, Gujarat, the town associated with the Amul cooperative "
  "model.",
  ["NDDB founded 1965", "Headquarters: Anand, Gujarat"],
  [fact("NDDB 'was founded in 1965'; address Anand - 388 001, Gujarat, India", "org_nddb")],
  why="NDDB's own website gives Anand, Gujarat as its address; the other towns are not given.")

G(T, HQ, "Intermediate",
  "The Marine Products Export Development Authority (MPEDA), set up in 1972 under the MPEDA Act, 1972 to promote "
  "seafood exports, has its head office in which city?",
  ["Kochi", "Visakhapatnam", "Chennai", "Mumbai"], "*",
  "Export promotion bodies: head offices",
  "MPEDA is a statutory body under the Ministry of Commerce and Industry, set up in 1972 under the MPEDA Act, 1972. Its "
  "head office is MPEDA House, Panampilly Nagar, Kochi.",
  ["MPEDA: MPEDA Act, 1972; Ministry of Commerce and Industry", "Head office: MPEDA House, Kochi"],
  [fact("MPEDA established in 1972 under the Ministry of Commerce & Industry; statutory functions under the MPEDA Act "
        "1972; head office MPEDA House, Panampilly Nagar, Kochi 682 036", "org_mpeda")],
  why="MPEDA's website gives Kochi as the head office; the other port cities are not named.")

G(T, HQ, "Intermediate",
  "Gilbert F. Houngbo, the 11th Director-General of the International Labour Organization and the first African to "
  "hold the post, earlier served as President of which UN agency?",
  ["International Fund for Agricultural Development (IFAD)", "World Food Programme (WFP)",
   "UN Development Programme (UNDP)", "Food and Agriculture Organization (FAO)"], "*",
  "Heads of international organisations",
  "Houngbo took office as the ILO's 11th Director-General on 1 October 2022, the first African in the post. He had been "
  "elected the sixth President of IFAD in 2017 and re-elected in 2021, and was Prime Minister of Togo from 2008 to "
  "2012.",
  ["ILO DG since 1 Oct 2022 (11th; first African)", "Earlier: IFAD President (elected 2017, re-elected 2021)",
   "Prime Minister of Togo 2008-2012"],
  [fact("Houngbo took office on 1 October 2022; first African to hold the position; elected sixth President of IFAD in "
        "2017 and re-elected 2021; PM of Togo 2008-2012", "org_ilo_bio"),
   fact("ILO page: Gilbert F. Houngbo, 11th Director-General, assumed the role in October 2022", "org_ilo_dg")],
  why="The ILO biography names IFAD; it mentions earlier UNDP posts, but not as its head, and does not mention WFP or "
      "FAO.",
  current=ca("2022-10-01"))

G(T, HQ, "Intermediate",
  "Before becoming Director-General of the World Health Organization in July 2017, Dr Tedros Adhanom Ghebreyesus "
  "served Ethiopia as Minister of Health and later held which other ministerial post?",
  ["Minister of Foreign Affairs", "Minister of Finance", "Minister of Education", "Minister of Defence"], "*",
  "Heads of international organisations",
  "Tedros was Ethiopia's Minister of Health from 2005 to 2012 and Minister of Foreign Affairs from 2012 to 2016. He was "
  "elected WHO Director-General by the Seventieth World Health Assembly in May 2017, took office on 1 July 2017, and is "
  "the first person from the WHO African Region to head the agency.",
  ["Health Minister 2005-2012", "Foreign Minister 2012-2016", "WHO DG from 1 July 2017"],
  [fact("Tedros: Minister of Health 2005-2012, Minister of Foreign Affairs 2012-2016; elected by the 70th WHA in May 2017;"
        " took office 1 July 2017; first from the WHO African Region", "org_who_dg")],
  why="The WHO biography lists Health and Foreign Affairs as his ministerial posts, not Finance, Education or Defence.",
  current=ca("2017-07-01"))

G(T, HQ, "Intermediate",
  "The International Big Cat Alliance (IBCA), headquartered in India, became a treaty-based body when its framework "
  "agreement came into force on 23 January 2025. Which of the following is NOT one of the seven big cats it covers?",
  ["Clouded leopard", "Puma", "Jaguar", "Snow leopard"], "*",
  "India-led organisations",
  "IBCA, launched by Prime Minister Narendra Modi on 9 April 2023 at the event marking 50 years of Project Tiger, covers "
  "seven big cats: tiger, lion, leopard, snow leopard, cheetah, jaguar and puma. Its framework agreement came into "
  "force on 23 January 2025 after ratification by Nicaragua, Eswatini, India, Somalia and Liberia.",
  ["7 big cats: tiger, lion, leopard, snow leopard, cheetah, jaguar, puma", "Clouded leopard is not in the list"],
  [fact("IBCA framework agreement in force from 23 January 2025; seven big cats: tiger, lion, leopard, snow leopard, "
        "cheetah, jaguar, puma; launched 9 April 2023 by PM Modi; headquarters in India (AIR)", "org_ibca_air")],
  why="Puma, jaguar and snow leopard are among the seven listed big cats; the clouded leopard is not listed.",
  current=ca("2025-01-23"))

G(T, HQ, "Intermediate",
  "On 2 July 2026, Sierra Leone's President Julius Maada Bio, as Chair of the ECOWAS Authority, commissioned the new "
  "headquarters of the ECOWAS Commission in Abuja. Which country financed and built it?",
  ["China", "Nigeria", "Japan", "United Arab Emirates"], "*",
  "Regional organisations: headquarters",
  "The new ECOWAS Commission headquarters in Abuja, Nigeria, costing about ₦78 billion (about US$56.5 million), was "
  "financed and built by China as a China-aid project under the Forum on China-Africa Cooperation (FOCAC).",
  ["Commissioned 2 July 2026 by Julius Maada Bio (Chair, ECOWAS Authority)", "Built and financed by China (FOCAC)",
   "Location: Abuja"],
  [fact("2 July 2026: Julius Maada Bio, Chair of the ECOWAS Authority and President of Sierra Leone, commissioned the "
        "new Commission HQ in Abuja, financed and built by China as a China-Aid project under FOCAC; ~₦78 billion",
        "org_ecowas_hq"),
   fact("ThisDay: the new permanent headquarters in Abuja was financed by the People's Republic of China",
        "org_ecowas_td")],
  why="Both sources name China as the financier; Nigeria is the host country, not the funder.",
  current=ca("2026-07-02"))

G(T, MEM, "Intermediate",
  "On 1 June 2026, Moldova became the 40th member state of which organisation, after depositing its instrument of "
  "accession on 25 March 2026?",
  ["European Patent Organisation", "European Space Agency", "Council of Europe", "OECD"], "*",
  "Membership changes",
  "Moldova deposited its instrument of accession to the European Patent Convention on 25 March 2026 and became the "
  "40th contracting state of the European Patent Organisation on 1 June 2026. A validation agreement with the EPO had "
  "been in effect since 1 November 2015.",
  ["Deposit: 25 March 2026", "Member from 1 June 2026 (40th)", "Validation agreement in force since 1 Nov 2015"],
  [fact("Moldova due to become the 40th contracting state on 1 June 2026; instrument deposited 25 March 2026; validation "
        "agreement in effect since 1 November 2015", "org_epo_news"),
   fact("EPO press release headline: Republic of Moldova joins European Patent Organisation as 40th member state",
        "org_epo_pr")],
  why="The EPO sources describe the European Patent Organisation accession; the other bodies are not involved.",
  current=ca("2026-06-01"))

G(T, MEM, "Intermediate",
  "In July 2026, Laos signed a memorandum in Beijing formalising its status as a dialogue partner of which "
  "organisation?",
  ["Shanghai Cooperation Organisation", "BRICS", "Asia-Pacific Economic Cooperation", "Organisation of Islamic Cooperation"],
  "*",
  "Membership changes",
  "Laos had been accepted as a dialogue partner at the 25th SCO Heads of State Council meeting in Tianjin. The "
  "memorandum signed in Beijing formalised the status. The SCO then had 10 member states, 2 observer states and 15 "
  "dialogue partners.",
  ["Accepted at SCO Tianjin summit", "Memorandum signed in Beijing, 10 July 2026", "SCO: 10 members, 2 observers, 15 partners"],
  [fact("CGTN, 10 July 2026: signing in Beijing on Friday formalised Laos's SCO dialogue partner status, accepted at the "
        "25th Heads of State Council in Tianjin; SCO has 10 members, 2 observers, 15 dialogue partners", "org_laos_cgtn")],
  why="The source concerns the SCO; BRICS, APEC and the OIC are not mentioned.",
  current=ca("2026-07-10", inferred="CGTN article dated 10 July 2026 says the signing took place 'on Friday morning'"))

G(T, MEM, "Intermediate",
  "On which date did the United States' withdrawal from the Paris Agreement on climate change take effect, one year "
  "after it notified the UN in January 2025?",
  ["27 January 2026", "20 January 2026", "1 January 2026", "4 November 2025"], "*",
  "Membership changes: withdrawals",
  "The US notified the UN in January 2025 of its intention to leave the Paris Agreement. Under the Agreement's rules the "
  "exit takes effect one year after notification, which made 27 January 2026 the official date. It was the second time "
  "the US left the accord.",
  ["Notification: January 2025", "Exit effective after one year: 27 January 2026", "Second US withdrawal"],
  [fact("US withdrawal formally takes effect one year after notification, making 27 January 2026 the official date; its "
        "second withdrawal from the accord", "org_paris_bt"),
   fact("E&E News: 'So long, Paris: US officially leaves landmark climate pact'", "org_paris_ee")],
  why="The sources give 27 January 2026 as the effective date; the other dates are not given for the exit.",
  current=ca("2026-01-27"))

# ------------------------------------------------------------------ Organizations: Advanced (2)
GS(T, MEM, "Advanced",
   "the withdrawal of three Sahel countries from the Economic Community of West African States (ECOWAS)",
   ["Niger, Mali and Burkina Faso formally ceased to be members of ECOWAS on 29 January 2025.",
    "The three countries have grouped themselves as the Alliance of Sahel States.",
    "On their exit, ECOWAS closed its doors to their return and ended free movement within the region for their "
    "citizens."],
   [True, True, False],
   "Membership changes: regional blocs",
   "Niger, Mali and Burkina Faso formally withdrew from ECOWAS on 29 January 2025 and have formed the Alliance of Sahel "
   "States. ECOWAS said its doors remained open and asked member countries to keep allowing their citizens free "
   "movement with an ECOWAS passport, so statement 3 is wrong.",
   [fact("Niger, Mali and Burkina Faso formally withdrew from ECOWAS on Wednesday, 29 January 2025; they formed the "
         "Alliance of Sahel States; ECOWAS said its doors remained open and asked members to allow free movement",
         "org_ecowas_an"),
    fact("Ahram Online: Burkina Faso, Mali and Niger officially leave West Africa bloc", "org_ecowas_ah")],
   why="Statement 3 reverses the ECOWAS position: it kept its doors open and sought continued free movement.",
   current=ca("2025-01-29"))

GS(T, MEM, "Advanced",
   "Jordan joining India-led global initiatives in April 2026",
   ["Jordan joined the International Solar Alliance and the Coalition for Disaster Resilient Infrastructure, but not "
    "the Global Biofuel Alliance.",
    "Jordan's Ambassador handed over the membership documents to the Secretary (South) of the Ministry of External "
    "Affairs in New Delhi.",
    "According to the report, the Coalition for Disaster Resilient Infrastructure had 53 member countries and 12 "
    "partner organisations."],
   [False, True, True],
   "Membership: India-led initiatives",
   "On 27 April 2026 Jordan confirmed its membership of three India-led initiatives: the International Solar Alliance, "
   "the Coalition for Disaster Resilient Infrastructure and the Global Biofuel Alliance. Ambassador Yousef Abdelghani "
   "handed the documents to Secretary (South) Dr Neena Malhotra in New Delhi. The report put CDRI at 53 member countries "
   "and 12 partner organisations, and the GBA at 33 countries and 14 international organisations.",
   [fact("Jordan joined ISA, CDRI and GBA on Monday (27 April 2026); Ambassador Yousef Abdelghani handed documents to "
         "Secretary (South) Dr Neena Malhotra in New Delhi; CDRI 53 member countries and 12 partner organisations",
         "org_jordan_tt"),
    fact("Lokmat Times: Jordan joins India-led global initiatives ISA, CDRI and GBA", "org_jordan_lm")],
   why="Statement 1 is wrong because Jordan joined the Global Biofuel Alliance too.",
   current=ca("2026-04-27", inferred="Telangana Today report of 27 April 2026 says Jordan joined 'on Monday'"))

# ------------------------------------------------------------------ Important Days: Basic (5)
T = "Important Days"
DT = "Days and themes"

G(T, DT, "Basic",
  "What was the theme of World Malaria Day 2026, observed on 25 April?",
  ["Driven to End Malaria: Now We Can. Now We Must.", "Accelerate the Fight Against Malaria Together",
   "Zero Malaria Starts with Every Community", "Invest Today for a Malaria-Free Tomorrow"], "*",
  "Health days: themes",
  "WHO's campaign page gives the World Malaria Day 2026 theme as 'Driven to End Malaria: Now We Can. Now We Must.' It "
  "notes about 610,000 malaria deaths in 2024 and 47 countries certified malaria-free.",
  ["World Malaria Day: 25 April", "2026 theme: Driven to End Malaria: Now We Can. Now We Must."],
  [fact("WHO World Malaria Day 2026 page: theme 'Driven to End Malaria: Now We Can. Now We Must.'; 25 April; about "
        "610,000 deaths in 2024; 47 countries certified malaria-free", "day_malaria")],
  why="Only the first option matches the theme on WHO's page; the others are not the 2026 theme.",
  current=ca("2026-04-25"))

G(T, DT, "Basic",
  "Under which theme, announced by WHO in October 2025, was World No Tobacco Day 2026 (31 May) observed?",
  ["Unmasking the appeal - countering nicotine and tobacco addiction", "Protect youth from industry interference",
   "Grow food, not tobacco", "Commit to quit: a healthier tomorrow"], "*",
  "Health days: themes",
  "WHO announced on 17 October 2025 that World No Tobacco Day 2026 would focus on 'Unmasking the appeal - countering "
  "nicotine and tobacco addiction'. The campaign targets how companies rebrand and reformulate products such as "
  "e-cigarettes and nicotine pouches to attract young users.",
  ["Announced 17 Oct 2025", "Theme: Unmasking the appeal - countering nicotine and tobacco addiction"],
  [fact("WHO, 17 October 2025: World No Tobacco Day 2026 theme 'Unmasking the appeal - countering nicotine and tobacco "
        "addiction'; observed 31 May; targets e-cigarettes, nicotine pouches", "day_tobacco")],
  why="WHO's announcement gives the 'Unmasking the appeal' theme; the other phrases are not the 2026 theme.",
  current=ca("2026-05-31"))

G(T, DT, "Basic",
  "World Telecommunication and Information Society Day, observed on 17 May to mark the founding of the ITU in 1865, "
  "had which theme in 2026?",
  ["Digital lifelines: Strengthening resilience in a connected world", "Space for all: Expanding connectivity beyond borders",
   "Bridging the digital divide for the last mile", "Connecting the unconnected through innovation"], "*",
  "UN days: themes",
  "The 2026 theme of World Telecommunication and Information Society Day was 'Digital lifelines: Strengthening "
  "resilience in a connected world'. The day marks the establishment of the International Telecommunication Union in "
  "Paris in 1865.",
  ["17 May: ITU founded in Paris, 1865", "2026 theme: Digital lifelines"],
  [fact("AIR: WTISD 17 May 2026 theme 'Digital lifelines: Strengthening resilience in a connected world'; marks the 1865 "
        "establishment of ITU in Paris", "day_wtisd")],
  why="AIR gives 'Digital lifelines' as the 2026 theme; the other options are not the 2026 theme.",
  current=ca("2026-05-17"))

G(T, DT, "Basic",
  "World Intellectual Property Day 2026, observed on 26 April, was themed around which field?",
  ["Sports", "Music", "Artificial intelligence", "Traditional medicine"], "*",
  "UN days: themes",
  "WIPO's theme for World IP Day 2026 was 'IP and Sports: Ready, Set, Innovate', celebrated on 26 April 2026.",
  ["World IP Day: 26 April", "2026 theme: IP and Sports: Ready, Set, Innovate"],
  [fact("WIPO: World IP Day 2026 theme 'IP and Sports: Ready, Set, Innovate', 26 April 2026", "day_ip")],
  why="WIPO's page links the 2026 theme to sports, not to the other fields.",
  current=ca("2026-04-26"))

G(T, DT, "Basic",
  "What was the theme of World Mental Health Day 2026 (10 October), announced by the World Federation for Mental Health "
  "in August 2026?",
  ["Lived Experiences Heard: Real Voices, Real Change", "Mental Health is a Universal Human Right",
   "Access to Services: Mental Health in Catastrophes and Emergencies", "Make Mental Health a Global Priority for All"],
  "*",
  "Health days: themes",
  "The World Federation for Mental Health announced on 11 August 2026 that the theme for World Mental Health Day 2026 "
  "would be 'Lived Experiences Heard: Real Voices, Real Change'. It also asked that the Day support WHO's initiative on "
  "deinstitutionalisation.",
  ["Announced by WFMH on 11 Aug 2026", "Theme: Lived Experiences Heard: Real Voices, Real Change"],
  [fact("WFMH, 11 August 2026: World Mental Health Day 2026 theme 'Lived Experiences Heard: Real Voices, Real Change'",
        "day_mh")],
  why="WFMH names 'Lived Experiences Heard' as the 2026 theme; the other options are not the 2026 theme.",
  current=ca("2026-10-10"))

# ------------------------------------------------------------------ Important Days: Advanced (4)
GS(T, DT, "Advanced",
   "World Habitat Day 2026",
   ["Its global observance was held under the theme 'Adequate Housing for All'.",
    "The global observance was hosted in Nairobi, Kenya, at UN-Habitat's headquarters.",
    "UN-Habitat said that more than 1.1 billion people live in informal settlements and slums."],
   [True, False, True],
   "UN days: themes and hosts",
   "World Habitat Day 2026 was marked on 5 October 2026 with a global observance in Muscat hosted by Oman, under the "
   "theme 'Adequate Housing for All'. UN-Habitat Executive Director Anacláudia Rossbach spoke there. The release "
   "described a housing crisis affecting nearly 3.4 billion people, with more than 1.1 billion living in informal "
   "settlements and slums.",
   [fact("UN-Habitat press release, Muscat, 5 October 2026: theme 'Adequate Housing for All', hosted by Oman; more than "
         "1.1 billion people live in informal settlements and slums", "day_habitat"),
    fact("UN-Habitat media advisory: World Habitat Day 2026: Adequate Housing for All, 5 October 2026, Oman Convention & "
         "Exhibition Centre, Muscat", "day_habitat_ma")],
   why="Statement 2 is wrong: the 2026 global observance was in Muscat, Oman.",
   current=ca("2026-10-05"))

GS(T, DT, "Advanced",
   "World Teachers' Day 2026 (5 October)",
   ["Its theme was 'Standing with teachers: 60 years of protecting the profession, advancing its status and shaping our "
    "futures'.",
    "It marked the 60th anniversary of the 1966 ILO/UNESCO Recommendation concerning the Status of Teachers.",
    "The global celebration was held at UNESCO Headquarters in Paris."],
   [True, True, True],
   "UN days: themes",
   "UNESCO gives the 2026 theme as 'Standing with teachers: 60 years of protecting the profession, advancing its status "
   "and shaping our futures', marking 60 years of the 1966 ILO/UNESCO Recommendation concerning the Status of Teachers. "
   "The global celebration was at UNESCO Headquarters, Paris, on 5 October.",
   [fact("UNESCO: 2026 theme 'Standing with teachers: 60 years of protecting the profession, advancing its status and "
         "shaping our futures'; 60th anniversary of the 1966 ILO/UNESCO Recommendation; global celebration at UNESCO "
         "HQ, Paris, 5 October", "day_teachers")],
   why="All three statements match UNESCO's World Teachers' Day page.",
   current=ca("2026-10-05"))

GS(T, DT, "Advanced",
   "World Hepatitis Day 2026 (28 July)",
   ["Its theme was 'Hepatitis: Let's Break It Down'.",
    "The Government of Brazil and WHO convened a high-level event for the Day in Rio de Janeiro, on the sidelines of "
    "the International AIDS Conference.",
    "WHO said that deaths from viral hepatitis had fallen over the past decade while HIV deaths had risen."],
   [True, True, False],
   "Health days: themes",
   "At the UN Geneva briefing of 28 July 2026, WHO gave the theme as 'Hepatitis: Let's Break It Down' and said Brazil and "
   "WHO were convening a high-level event in Rio de Janeiro alongside the 26th International AIDS Conference. WHO said "
   "viral hepatitis deaths had risen by over 17% in the past decade while HIV deaths fell by nearly 60%, and that "
   "hepatitis caused 1.3 million deaths in 2024.",
   [fact("UN Geneva briefing transcript, 28 July 2026: theme 'Hepatitis, Let's Break It Down'; Brazil and WHO high-level "
         "event in Rio de Janeiro on the sidelines of the 26th International AIDS Conference; hepatitis mortality up over "
         "17% in a decade while HIV deaths fell nearly 60%", "day_hep_un"),
    fact("SAnews: World Hepatitis Day observed; WHO urges testing and treatment", "day_hep_sa")],
   why="Statement 3 reverses the trend: hepatitis deaths rose while HIV deaths fell.",
   current=ca("2026-07-28"))

GS(T, DT, "Advanced",
   "World Meteorological Day",
   ["It commemorates the coming into force of the Convention establishing the World Meteorological Organization on "
    "23 March 1948.",
    "Its theme for 2026 was 'Observing Today, Protecting Tomorrow'.",
    "Its theme for 2025 was 'Closing the Early Warning Gap Together'."],
   [False, True, True],
   "UN days: themes",
   "World Meteorological Day, 23 March, marks the coming into force of the WMO Convention on 23 March 1950, not 1948. "
   "The 2026 theme was 'Observing Today, Protecting Tomorrow' and the 2025 theme was 'Closing the Early Warning Gap "
   "Together'.",
   [fact("WMO: Day marks the coming into force of the WMO Convention on 23 March 1950; 2026 theme 'Observing Today, "
         "Protecting Tomorrow'; 2025 theme 'Closing the Early Warning Gap Together'", "day_wmo")],
   why="Statement 1 gives the wrong year: the Convention came into force in 1950.",
   current=ca("2026-03-23"))

# ###################################################################### part: eco (economic affairs + reports)
# ###################################################################### part: eco (Economic Affairs; Important Reports and Indexes)
U.update({
    # ---- Economic Affairs
    "eco_imf_bt": ("https://www.businesstoday.in/latest/economy/story/imf-trims-indias-2026-growth-forecast-to-6-4-raises-"
                   "2027-outlook-to-6-7-541744-2026-07-08", OPENED),
    "eco_imf_dh": ("https://www.deccanherald.com/business/imf-lowers-indias-fy27-growth-forecast-to-64-4066788", SEARCH),
    "eco_wb_week": ("https://www.theweek.in/wire-updates/business/2026/01/14/world-bank-raises-indias-gdp-growth-"
                    "projection-to-7.2-pc-for-fy26.html", OPENED),
    "eco_wb_print": ("https://theprint.in/economy/world-bank-raises-indias-gdp-growth-projection-to-7-2-pc-for-fy26/2827191",
                     SEARCH),
    "eco_gst_bt": ("https://www.businesstoday.in/latest/economy/story/gst-collections-jump-15-4-to-rs2-11-lakh-crore-in-"
                   "july-import-tax-revenues-surge-nearly-29-546657-2026-08-01", OPENED),
    "eco_gst_etv": ("https://www.etvbharat.com/en/business/gross-gst-collection-rose-in-july-2026-enn26080101798", SEARCH),
    "eco_cga_ians": ("https://ianslive.in/centres-fiscal-deficit-in-april-november-at-623-pc-of-full-year-estimate-govt-"
                     "capex-goes-up--20251231185104", OPENED),
    "eco_cga_mp": ("https://www.millenniumpost.in/business/centres-fiscal-deficit-touches-623-of-budget-estimate-in-nov-"
                   "govt-data-642098", SEARCH),
    "eco_boe_nov": ("https://www.bankofengland.co.uk/monetary-policy-summary-and-minutes/2026/november-2026", OPENED),
    "eco_boe_sep": ("https://www.bankofengland.co.uk/monetary-policy-summary-and-minutes/2026/september-2026", SEARCH),
    "eco_wpi_air": ("https://newsonair.gov.in/wholesale-inflation-up-to-9-87-in-june-food-fuel-key-drivers/", OPENED),
    "eco_wpi_bt": ("https://www.businesstoday.in/latest/economy/story/another-inflation-warning-wholesale-prices-jump-more-"
                   "than-expected-in-june-542819-2026-07-14", SEARCH),
    "eco_ecb_rates": ("https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html",
                      OPENED),
    "eco_ecb_ds": ("https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/shared/pdf/"
                   "ecb.ds260910~fbf0ab9b8d.en.pdf", OPENED),
    # ---- Important Reports and Indexes
    "rep_wir_wire": ("https://m.thewire.in/article/political-economy/in-charts-world-inequality-report-2026", OPENED),
    "rep_bf": ("https://brandfinance.com/press-releases/state-bank-of-india-16th-strongest-banking-brand-globally-indias-"
               "only-aaa-rated-bank", OPENED),
    "rep_bf_psu": ("https://www.psuconnect.in/bank-news/sbi-emerges-as-strongest-indian-bank-globally-hdfc-bank-tops-in-"
                   "brand-value", SEARCH),
    "rep_the_ep": ("https://educationpost.in/news/education/iisc-tops-indian-universities-in-the-world-university-rankings-"
                   "2027-ranks-254-globally", OPENED),
    "rep_the_ci": ("https://www.careerindia.com/news/iisc-bengaluru-tops-india-in-the-world-university-rankings-2027-"
                   "066393.html", SEARCH),
    "rep_sipri_week": ("https://www.theweek.in/news/defence/2026/03/09/india-still-top-arms-importer-but-atmanirbharta-"
                       "paying-off-pakistan-ramps-up-weapon-purchases-sipri.html", OPENED),
    "rep_sipri_trib": ("https://www.tribuneindia.com/news/defence/india-becomes-worlds-2nd-largest-arms-importer-sipri-"
                       "report/", SEARCH),
    "rep_wipi_eu": ("https://intellectual-property-helpdesk.ec.europa.eu/news-events/news/world-intellectual-property-"
                    "indicators-2025-india-records-double-digit-growth-patents-and-designs-2025-11-18_en", OPENED),
    "rep_fhi_df": ("https://insights.dataful.in/articles/indias-fiscal-divide-odisha-leads-as-several-states-slip-in-niti-"
                   "aayogs-fiscal-health-index", OPENED),
    "rep_fhi_niti": ("https://www.niti.gov.in/sites/default/files/2026-03/Fiscal-Health-Index-2026.pdf", SEARCH),
    "rep_wmo": ("https://wmo.int/news/media-centre/earths-climate-swings-increasingly-out-of-balance", OPENED),
    "rep_unctad_ao": ("https://www.angelone.in/news/economy/india-rises-to-11th-largest-fdi-recipient-in-2025-unctad-report",
                      OPENED),
    "rep_unctad_de": ("https://www.dailyexcelsior.com/fdi-inflows-to-india-increased-by-44-per-cent-to-usd-39-billion-in-"
                      "2025-un/", OPENED),
    "rep_ief_pdf": ("https://static.heritage.org/index/pdf/2026/2026_indexofeconomicfreedom_india.pdf", OPENED),
    "rep_ief_node": ("https://www.heritage.org/node/25159669", SEARCH),
    "rep_hurun_omm": ("https://ommcomnews.com/business-news/indias-billionaire-count-rises-to-308-ranks-3rd-worldwide-"
                      "hurun-global-list/", OPENED),
    "rep_hurun_sb": ("https://www.storyboard18.com/amp/brand-makers/hurun-global-rich-list-2026-elon-musk-leads-india-"
                     "ranks-third-with-308-billionaires-ws-l-92876.htm", OPENED),
})

T = "Economic Affairs"
GDP, INF, FIS, MON = "GDP and growth projections", "Inflation data", "Fiscal data", "Monetary policy decisions"

# ------------------------------------------------------------------ Economic Affairs: Intermediate (5)
G(T, GDP, "Intermediate",
  "In its World Economic Outlook Update released on 8 July 2026, what growth did the International Monetary Fund "
  "project for India for 2026 (fiscal year 2026-27)?",
  ["6.4%", "6.5%", "6.7%", "7.2%"], "*",
  "IMF growth projections for India",
  "The IMF's July 2026 WEO Update cut India's 2026 growth projection by 0.1 percentage point to 6.4%, from 6.5% in "
  "April, citing a more challenging global environment. It raised the 2027 projection to 6.7% and kept global growth "
  "at 3.0% for 2026.",
  ["WEO Update, 8 July 2026", "India 2026: 6.4% (April: 6.5%)", "India 2027: 6.7%"],
  [fact("IMF WEO Update of 8 July 2026 trimmed India's 2026 growth forecast by 0.1 point to 6.4% and raised the 2027 "
        "forecast to 6.7%; global growth kept at 3.0% for 2026", "eco_imf_bt"),
   fact("IMF lowered India's FY27 growth forecast to 6.4%", "eco_imf_dh")],
  why="6.5% was the April 2026 projection that was cut; 6.7% is the projection for 2027; 7.2% is not the IMF's July "
      "figure for 2026.",
  current=ca("2026-07-08"))

G(T, GDP, "Intermediate",
  "In its Global Economic Prospects report of January 2026, the World Bank raised its estimate of India's real GDP "
  "growth for fiscal year 2025-26 to what level?",
  ["7.2%", "6.3%", "6.5%", "7.4%"], "*",
  "World Bank Global Economic Prospects",
  "The World Bank's January 2026 Global Economic Prospects put India's FY 2025-26 growth at 7.2%, up from its June "
  "2025 estimate of 6.3%, citing robust domestic demand. It projected growth of 6.5% in FY 2026-27 and 6.6% in "
  "FY 2027-28. The 7.4% figure is the government's First Advance Estimate, not the World Bank's.",
  ["GEP, January 2026", "FY26: 7.2% (earlier 6.3%)", "FY27: 6.5%; FY28: 6.6%"],
  [fact("World Bank GEP (PTI, 14 Jan 2026): India FY26 growth estimated at 7.2%, up from 6.3% in June; FY27 6.5%, "
        "FY28 6.6%; MoSPI First Advance Estimate 7.4%", "eco_wb_week"),
   fact("World Bank raises India's GDP growth projection to 7.2% for FY26", "eco_wb_print")],
  why="6.3% was the earlier (June 2025) estimate; 6.5% is the FY 2026-27 projection; 7.4% is MoSPI's First Advance "
      "Estimate.",
  current=ca("2026-01-14", inferred="PTI report dated 14 Jan 2026; the opened page does not state the report's "
                                    "release day"))

G(T, FIS, "Intermediate",
  "According to data released on 1 August 2026, India's gross GST collections for July 2026 grew 15.4% year-on-year "
  "to about how much?",
  ["₹2.11 lakh crore", "₹1.83 lakh crore", "₹1.81 lakh crore", "₹1.45 lakh crore"], "*",
  "Monthly GST collections",
  "Gross GST collections in July 2026 were about ₹2.11 lakh crore, up 15.4% from ₹1.83 lakh crore in July 2025. "
  "Gross domestic GST was ₹1.45 lakh crore and GST on imports ₹66,511 crore (up 28.8%). Net collections after "
  "refunds were about ₹1.81 lakh crore.",
  ["Gross GST, July 2026: ₹2.11 lakh crore (+15.4%)", "July 2025: ₹1.83 lakh crore"],
  [fact("Gross GST July 2026 ₹2.11 lakh crore, +15.4% from ₹1.83 lakh crore; domestic ₹1.45 lakh crore; imports "
        "₹66,511 crore (+28.8%); net ₹1.81 lakh crore", "eco_gst_bt"),
   fact("Gross GST collection grows 15.4% to over ₹2.11 lakh crore in July", "eco_gst_etv")],
  why="₹1.83 lakh crore was the July 2025 figure; ₹1.81 lakh crore is the net collection; ₹1.45 lakh crore is gross "
      "domestic GST only.",
  current=ca("2026-08-01"))

G(T, FIS, "Intermediate",
  "According to Controller General of Accounts data released on 31 December 2025, the Centre's fiscal deficit for "
  "April-November 2025 reached what share of the 2025-26 Budget Estimate?",
  ["62.3%", "58.7%", "55.9%", "49.1%"], "*",
  "Centre's monthly accounts (CGA)",
  "The fiscal deficit for April-November 2025 was about ₹9.8 lakh crore, or 62.3% of the full-year Budget Estimate. "
  "In the same period capital expenditure reached 58.7% of its target, net tax revenue 49.1% and total revenue "
  "receipts 55.9% of their Budget Estimates.",
  ["CGA data, 31 Dec 2025", "Fiscal deficit Apr-Nov 2025: 62.3% of BE"],
  [fact("IANS, 31 Dec 2025: fiscal deficit April-November ₹9.8 lakh crore, 62.3% of BE; capex 58.7% of target; net "
        "tax revenue 49.1% of BE; revenue receipts 55.9%", "eco_cga_ians"),
   fact("Centre's fiscal deficit touches 62.3% of Budget Estimate in November", "eco_cga_mp")],
  why="58.7% is capital expenditure's share of its target; 55.9% is revenue receipts and 49.1% net tax revenue as "
      "shares of their Budget Estimates.",
  current=ca("2025-12-31"))

G(T, MON, "Intermediate",
  "At its meeting ending on 4 November 2026, the Bank of England's Monetary Policy Committee raised Bank Rate by 0.25 "
  "percentage point to 4%. By what vote was the decision taken?",
  ["8-1", "6-3", "5-4", "9-0"], "*",
  "Central bank decisions: Bank of England",
  "The Bank of England's MPC voted 8-1 to raise Bank Rate from 3.75% to 4%. The lone dissenter, Catherine L Mann, "
  "preferred a larger 0.5 percentage point increase. At its September 2026 meeting the MPC had held the rate at "
  "3.75% by a 6-3 vote.",
  ["Meeting ended 4 Nov 2026 (published 5 Nov)", "Bank Rate 3.75% -> 4%", "Vote 8-1; Mann wanted 0.5 point"],
  [fact("Bank of England, 5 Nov 2026: MPC meeting ending 4 Nov voted 8-1 to raise Bank Rate by 0.25 point to 4%; "
        "Catherine L Mann preferred a 0.5 point increase", "eco_boe_nov"),
   fact("September 2026: MPC voted 6-3 to maintain Bank Rate at 3.75%", "eco_boe_sep")],
  why="6-3 was the vote to hold the rate in September 2026; a 9-0 or 5-4 vote does not match the November decision, "
      "which had one dissent.",
  current=ca("2026-11-04"))

# ------------------------------------------------------------------ Economic Affairs: Advanced (2)
GS(T, INF, "Advanced",
   "India's wholesale price (WPI) inflation for June 2026, released on 14 July 2026",
   ["WPI inflation eased in June 2026 compared with May 2026.",
    "Inflation in the fuel and power group eased to 27.41% from over 30% in May 2026.",
    "Inflation in the WPI Food Index rose to 6.14% from 4.49% in May 2026."],
   [False, True, True],
   "WPI inflation (base 2022-23)",
   "WPI inflation rose to 9.87% in June 2026 from 9.68% in May, so statement 1 is wrong. Fuel and power inflation "
   "eased to 27.41% but stayed very high; primary articles inflation rose to 7% from 4.99%; the WPI Food Index rose "
   "to 6.14% from 4.49%. Mineral oils, food articles, basic metals and chemicals were the main drivers.",
   [fact("AIR, 14 Jul 2026: WPI inflation 9.87% in June vs 9.68% in May; fuel and power 27.41% from over 30%; primary "
         "articles 7% from 4.99%; WPI Food Index 6.14% from 4.49%", "eco_wpi_air"),
    fact("Wholesale prices jump more than expected in June 2026", "eco_wpi_bt")],
   why="Statement 1 is wrong because WPI inflation rose (9.68% to 9.87%); statements 2 and 3 match the release.",
   current=ca("2026-07-14"))

GS(T, MON, "Advanced",
   "the European Central Bank's monetary policy decision of 10 September 2026",
   ["With effect from 16 September 2026, the deposit facility, main refinancing operations and marginal lending "
    "facility rates became 2.50%, 2.65% and 2.90% respectively.",
    "It was the ECB's first increase in its key interest rates in 2026.",
    "The new ECB staff baseline projected headline euro area inflation averaging 3.0% in 2026."],
   [True, False, True],
   "Central bank decisions: ECB",
   "On 10 September 2026 the ECB Governing Council raised its three key rates by 25 basis points, citing inflation "
   "pressures from the Middle East conflict; the new rates (2.50%, 2.65%, 2.90%) took effect on 16 September. It was "
   "not the first hike of 2026: the rates had already been raised to 2.25%, 2.40% and 2.65% with effect from "
   "17 June 2026. Staff projected inflation of 3.0% in 2026, 2.5% in 2027 and 2.1% in 2028.",
   [fact("ECB statement of 10 Sep 2026: three key rates raised by 25 bps to 2.50%, 2.65% and 2.90% from 16 Sep 2026; "
         "staff baseline inflation 3.0% (2026), 2.5% (2027), 2.1% (2028)", "eco_ecb_ds"),
    fact("ECB key rates table: 11 Jun 2025 DFR 2.00, MRO 2.15, MLF 2.40 (no change until 2026); 17 Jun 2026 DFR 2.25, "
         "MRO 2.40, MLF 2.65; 16 Sep 2026 DFR 2.50, MRO 2.65, MLF 2.90",
         "eco_ecb_rates")],
   why="Statement 2 is wrong because the ECB had already raised rates with effect from 17 June 2026; statements 1 and "
       "3 match the ECB's statement.",
   current=ca("2026-09-10"))

# ====================================================================== Important Reports and Indexes
T = "Important Reports and Indexes"
PUB, RANK = "Publishing body", "India's rank"

# ------------------------------------------------------------------ Reports: Basic (4)
G(T, PUB, "Basic",
  "The World Inequality Report 2026, released in December 2025, found that the top 10% of earners in India take "
  "about 58% of national income. Which body publishes this report?",
  ["World Inequality Lab", "Oxfam International", "United Nations Development Programme", "World Bank"], "*",
  "Publishers of global reports",
  "The World Inequality Report 2026 was published by the Paris-based World Inequality Lab; its editors included "
  "Lucas Chancel and Thomas Piketty. For India it reported that the top 10% take about 58% of national income and the "
  "bottom 50% about 15%, while the top 1% hold about 40% of wealth.",
  ["World Inequality Report 2026 -> World Inequality Lab (Paris)"],
  [fact("The Wire, 10 Dec 2025: World Inequality Report 2026 by the Paris-based World Inequality Lab (editors incl. "
        "Lucas Chancel, Thomas Piketty); India top 10% ~58% of income, bottom 50% ~15%, top 1% ~40% of wealth",
        "rep_wir_wire")],
  why="The source names the World Inequality Lab as the publisher; the other organisations are not mentioned as "
      "publishers of this report.",
  current=ca("2025-12-10", inferred="The Wire report dated 10 Dec 2025; the opened page does not state the exact "
                                    "release day"))

G(T, PUB, "Basic",
  "The 'Banking 500 2026' report, released in March 2026, named State Bank of India the world's 16th strongest "
  "banking brand. Which brand valuation consultancy publishes this report?",
  ["Brand Finance", "Interbrand", "Kantar", "The Banker"], "*",
  "Publishers of rankings",
  "Brand Finance released its Banking 500 2026 ranking on 5 March 2026. SBI was the 16th strongest banking brand with "
  "a Brand Strength Index score of 90.3 and an AAA+ rating, and HDFC Bank was India's most valuable banking brand at "
  "USD 12.4 billion.",
  ["Banking 500 2026 -> Brand Finance", "SBI: 16th strongest, AAA+"],
  [fact("Brand Finance press release, 5 Mar 2026: Banking 500 2026; SBI 16th strongest banking brand, BSI 90.3, AAA+; "
        "HDFC Bank USD 12.4 bn, 31st by brand value", "rep_bf")],
  why="The report is Brand Finance's own; the other firms are not named as its publisher.",
  current=ca("2026-03-05"))

G(T, RANK, "Basic",
  "In the Times Higher Education (THE) World University Rankings 2027, released in September 2026, what was the rank "
  "of the Indian Institute of Science (IISc), Bengaluru, India's highest-ranked institution?",
  ["254th", "118th", "201st", "326th"], "*",
  "India in university rankings",
  "IISc Bengaluru was India's top institution at 254th in the THE World University Rankings 2027, which covered 2,297 "
  "universities in 118 countries and territories and was again topped by the University of Oxford. India had 143 "
  "ranked institutions; Saveetha Institute of Medical and Technical Sciences was next in the 326-350 band.",
  ["THE WUR 2027", "IISc Bengaluru: 254th (India's best)"],
  [fact("Education Post, 30 Sep 2026: IISc 254th, India's highest-ranked; 143 Indian institutions; 2,297 universities "
        "in 118 countries; Oxford first for 11th year; Saveetha in 326-350 band", "rep_the_ep"),
   fact("IISc Bengaluru tops India in THE World University Rankings 2027", "rep_the_ci")],
  why="The source places IISc at 254th; 326th is within the band of the next Indian institution (Saveetha), and the "
      "other ranks are not IISc's position.",
  current=ca("2026-09-30", inferred="Education Post report dated 30 Sep 2026; ranking release day not stated"))

G(T, RANK, "Basic",
  "According to SIPRI's 'Trends in International Arms Transfers, 2025', released in March 2026, what was India's "
  "rank among the world's arms importers for 2021-25?",
  ["Second", "First", "Third", "Fifth"], "*",
  "India in global arms trade",
  "SIPRI ranked India the second-largest arms importer in 2021-25, with 8.2% of global imports, behind Ukraine. "
  "India's imports fell 4.0% from 2016-20, which SIPRI partly linked to growing domestic production. Pakistan ranked "
  "fifth.",
  ["SIPRI arms transfers report, March 2026", "2021-25: Ukraine 1st, India 2nd (8.2%)"],
  [fact("The Week, 9 Mar 2026: SIPRI ranks India second among arms importers in 2021-25 (8.2%) behind Ukraine; India's "
        "imports down 4.0%; Pakistan fifth", "rep_sipri_week"),
   fact("India becomes world's 2nd largest arms importer: SIPRI report", "rep_sipri_trib")],
  why="Ukraine was first and Pakistan fifth; India was second.",
  current=ca("2026-03-09", inferred="The Week article dated 9 Mar 2026; report release day not separately stated"))

# ------------------------------------------------------------------ Reports: Intermediate (1)
G(T, RANK, "Intermediate",
  "According to WIPO's World Intellectual Property Indicators 2025 report, released in November 2025, where did India "
  "rank in trademark filing activity, with a class count of about 5.33 lakh?",
  ["Fourth", "Second", "Third", "Sixth"], "*",
  "India in IP statistics",
  "WIPI 2025 placed India fourth in trademark filing activity (class count 532,900), after China, the United States "
  "and the Russian Federation, and ahead of Brazil. The report also noted India's patent filings rose 19.1% in 2024, "
  "its sixth straight year of double-digit growth, and design filings rose 44.9%.",
  ["WIPI 2025 trademarks: China, US, Russia, India (4th), Brazil"],
  [fact("EU IP Helpdesk, 18 Nov 2025: WIPI 2025 - India fourth in trademarks with class count 532,900 after China, US "
        "and Russian Federation; India patent filings +19.1%; designs +44.9%", "rep_wipi_eu")],
  why="China, the United States and the Russian Federation ranked above India; Brazil was fifth.",
  current=ca("2025-11-18", inferred="EU IP Helpdesk news dated 18 Nov 2025; report release day not stated"))

# ------------------------------------------------------------------ Reports: Advanced (5)
GS(T, PUB, "Advanced",
   "the Fiscal Health Index (FHI) 2026",
   ["It was released by NITI Aayog as the second edition of the index, using data for 2023-24.",
    "Among the 18 major States, Odisha ranked first, followed by Goa and Jharkhand.",
    "For the first time, 10 North-Eastern and Himalayan States were also assessed."],
   [True, True, True],
   "NITI Aayog's Fiscal Health Index",
   "NITI Aayog's Fiscal Health Index 2026, its second edition, scores States on 2023-24 data across Quality of "
   "Expenditure, Revenue Mobilisation, Fiscal Prudence, Debt Index and Debt Sustainability. Odisha (73.1) led the 18 "
   "major States, followed by Goa (54.7) and Jharkhand (50.5); Punjab (12.4) was last. Ten North-Eastern and "
   "Himalayan States were included for the first time.",
   [fact("Dataful: NITI Aayog FHI in its second edition; 2023-24 data; Odisha 73.1, Goa 54.7, Jharkhand 50.5 among 18 "
         "major states; 10 NE and Himalayan states included for the first time; five sub-indices", "rep_fhi_df"),
    fact("NITI Aayog document 'Fiscal Health Index 2026, for the Financial Year 2023-24'", "rep_fhi_niti")],
   why="All three statements match the index as reported.",
   current=ca("2026-03-11", inferred="search results date the release to 11 Mar 2026; the opened Dataful article "
                                     "does not state the day"))

GS(T, PUB, "Advanced",
   "the 'State of the Global Climate 2025' report",
   ["It is a flagship report of the World Meteorological Organization, released on 23 March 2026, World "
    "Meteorological Day.",
    "It confirmed 2025 as the warmest year on record.",
    "It included Earth's energy imbalance as one of the key climate indicators for the first time."],
   [True, False, True],
   "WMO flagship reports",
   "The WMO released its State of the Global Climate 2025 on 23 March 2026, World Meteorological Day. It found 2025 "
   "was the second or third warmest year on record (about 1.43 °C above the 1850-1900 average), with 2015-2025 the "
   "eleven warmest years on record, and for the first time included Earth's energy imbalance as a key indicator.",
   [fact("WMO press release, 23 Mar 2026 (World Meteorological Day): State of the Global Climate 2025; energy "
         "imbalance a key indicator for the first time; 2025 second or third warmest year, ~1.43 °C", "rep_wmo")],
   why="Statement 2 is wrong because the report placed 2025 second or third warmest, not warmest; statements 1 and 3 "
       "match the WMO release.",
   current=ca("2026-03-23"))

GS(T, RANK, "Advanced",
   "India in UNCTAD's World Investment Report 2026, released on 7 July 2026",
   ["India re-entered the world's top 10 recipients of FDI in 2025.",
    "The value of greenfield projects announced in India fell to about USD 74 billion in 2025 from about USD 111 "
    "billion in 2024.",
    "Alphabet's USD 14.5 billion data centre project in India was the largest greenfield project announced "
    "worldwide."],
   [False, True, True],
   "India in the World Investment Report",
   "India's FDI inflows rose about 44% to USD 38.89 billion in 2025, lifting it two places to 11th among recipients, "
   "still outside the top 10. Announced greenfield projects fell to USD 74.12 billion from USD 111.14 billion, though "
   "India attracted the world's largest greenfield project, Alphabet's USD 14.5 billion data centre. India ranked 18th "
   "among home economies for outward FDI.",
   [fact("Angel One, 7 Jul 2026 (UNCTAD WIR 2026): India 11th, up from 13th; inflows +44% to USD 38.89 bn; greenfield "
         "announcements USD 74.12 bn vs 111.14 bn; Alphabet USD 14.5 bn data centre largest greenfield project globally",
         "rep_unctad_ao"),
    fact("PTI/UN, 7 Jul: FDI inflows to India up 44% to USD 39 bn; announced greenfield investment fell from over "
         "USD 111 bn to about USD 74 bn", "rep_unctad_de")],
   why="Statement 1 is wrong because India rose only to 11th place; statements 2 and 3 match the report coverage.",
   current=ca("2026-07-07"))

GS(T, RANK, "Advanced",
   "India in the Heritage Foundation's 2026 Index of Economic Freedom",
   ["India was ranked 132nd with an economic freedom score of 52.5.",
    "India was ranked 29th of 39 countries in the Asia-Pacific region and its economy was rated 'mostly unfree'.",
    "India's score improved by 0.5 point over the previous year."],
   [True, True, False],
   "India in economic freedom rankings",
   "The 2026 Index of Economic Freedom gave India a score of 52.5, making it the 132nd freest economy, and ranked it "
   "29th of 39 countries in Asia-Pacific. India's economy was rated 'mostly unfree', and its score fell by 0.5 point "
   "from the previous year, staying below the global and regional averages.",
   [fact("Heritage 2026 India page: score 52.5, 132nd freest; decreased by 0.5 point; 29th of 39 in Asia-Pacific; "
         "'mostly unfree'", "rep_ief_pdf"),
    fact("Heritage published the 2026 Index of Economic Freedom on 9 March 2026", "rep_ief_node")],
   why="Statement 3 is wrong because India's score decreased by 0.5 point; statements 1 and 2 match the Heritage "
       "country page.",
   current=ca("2026-03-09"))

GS(T, RANK, "Advanced",
   "India in the Hurun Global Rich List 2026, released in March 2026",
   ["With 308 billionaires, India ranked third in the world, behind the US and China.",
    "Mukesh Ambani was named the richest person in Asia.",
    "Mumbai, with 95 billionaires, retained its position as Asia's billionaire capital."],
   [True, True, False],
   "India in wealth rankings",
   "The Hurun Global Rich List 2026, released on 7 March 2026, counted 308 Indian billionaires (up 24), third behind "
   "the US and China. Mukesh Ambani of Reliance Industries was the richest person in Asia. Mumbai had 95 billionaires "
   "but lost its position as Asia's billionaire capital to Shenzhen (133).",
   [fact("IANS via Ommcom News, 7 Mar 2026: India 308 billionaires (+24), third behind US and China; Mumbai 95, lost "
         "Asia's billionaire capital position to Shenzhen (133)", "rep_hurun_omm"),
    fact("Storyboard18: Mukesh Ambani, with USD 109 bn, the richest person in Asia in 2026; India third with 308",
         "rep_hurun_sb")],
   why="Statement 3 is wrong because Mumbai lost the title to Shenzhen; statements 1 and 2 match the reports.",
   current=ca("2026-03-07"))

# ###################################################################### part: biz (business + static)
# ###################################################################### part: biz (Business and Corporate News, Static)
U.update({
    # ---- Mergers and acquisitions
    "biz_ea": ("https://www.ea.com/en-us/news/ea-announces-completion-of-acquisition", OPENED),
    "biz_ea_sl": ("https://www.silverlake.com/ea-announces-completion-of-acquisition-by-pif-silver-lake-and-affinity-"
                  "partners/", SEARCH),
    "biz_cybr_sec": ("https://www.sec.gov/Archives/edgar/data/1327567/000119312526045600/d40626dex991.htm", OPENED),
    "biz_cybr_tz": ("https://www.techzine.eu/news/security/138718/palo-alto-completes-25-billion-acquisition-of-cyberark",
                    OPENED),
    "biz_cap_fpj": ("https://www.freepressjournal.in/business/capillary-technologies-completes-acquisition-of-session-m-"
                    "from-mastercard", OPENED),
    "biz_anu_week": ("https://www.theweek.in/wire-updates/business/2026/02/27/anupam-rasayan-completes-usd150-mln-"
                     "acquisition-of-us-speciality-chemical-maker-jayhawk.html", OPENED),
    "biz_anu_cabb": ("https://cabb-chemicals.com/sale-of-jayhawk-fine-chemicals-the-cabb-group-completes-the-sale-jayhawk-"
                     "fine-chemicals-corporation-to-anupam-rasayan-india-ltd/", OPENED),
    "biz_aesl_week": ("https://www.theweek.in/wire-updates/business/2026/10/30/adani-energy-solutions-gets-cci-nod-to-"
                      "acquire-intellismart-infrastructure.html", OPENED),
    "biz_cyient_nse": ("https://nsearchives.nseindia.com/corporate/CYIENT_04092026172618_4September2026AcquisitionUpdate"
                       "SignedFinal.pdf", SEARCH),
    "biz_cyient_prn": ("https://tools.prnewswire.com/en-us/live/20813/release/20260530EN71930", OPENED),
    "biz_zyd_md": ("https://medicaldialogues.in/amp/news/industry/pharma/zydus-completes-usd-1664-million-acquisition-of-"
                   "us-based-assertio-holdings-173050", OPENED),
    "biz_zyd_nse": ("https://nsearchives.nseindia.com/corporate/Cadilahc_16062026161500_PressRelease16062026.pdf", SEARCH),
    "biz_dvn_wo": ("https://worldoil.com/news/2026/5/7/devon-completes-coterra-merger-expands-delaware-basin-position/",
                   OPENED),
    # ---- Corporate partnerships
    "biz_infy_anth": ("https://anthropic.com/news/anthropic-infosys", OPENED),
    "biz_fazer_trib": ("https://www.tribuneindia.com/news/business/reliance-consumer-products-sign-mou-with-finnish-food-"
                       "major-fazer-to-produce-and-market-premium-chocolates-in-india/", OPENED),
    "biz_emb_adani": ("https://www.adani.com/newsroom/media-releases/adani-defence-and-aerospace-and-embraer-announce-"
                      "strategic-partnership", OPENED),
    "biz_ailh_capa": ("https://centreforaviation.com/news/lufthansa-group-and-air-india-advance-joint-business-"
                      "partnership-1348943", OPENED),
    "biz_ailh_ai": ("https://www.airindia.com/in/en/newsroom/press-release/Air-India-and-Lufthansa-Group-sign-landmark-"
                    "MoU-to-advance-joint-business-partnership.html", SEARCH),
    "biz_ntpc_wnn": ("https://world-nuclear-news.org/articles/edf-ntpc-sign-mou-to-explore-new-indian-nuclear-projects",
                     OPENED),
    "biz_ntpc_psu": ("https://psuwatch.com/amp/story/newsupdates/ntpc-signs-mou-with-edf-to-explore-nuclear-power-"
                     "collaboration", OPENED),
    "biz_ntpc_pdf": ("https://ntpc.co.in/sites/default/files/inline-files/20260408_STEX_PRESSRELEASE.pdf", SEARCH),
    # ---- Static
    "st_krs_nic": ("https://mandya.nic.in/en/tourist-place/krs-dam/", OPENED),
})

T = "Business and Corporate News"
MA, CP = "Mergers and acquisitions", "Corporate partnerships"

# ------------------------------------------------------------------ Business: Basic (6)
G(T, CP, "Basic",
  "Under the partnership announced by Anthropic and Infosys on 17 February 2026, Anthropic's Claude models and Claude "
  "Code are being combined with which Infosys AI offering to build enterprise AI agents?",
  ["Infosys Topaz", "Infosys Finacle", "Infosys Cobalt", "Infosys Nia"], "*",
  "Corporate partnerships: IT services and AI",
  "Anthropic and Infosys announced on 17 February 2026 that they would build and deliver enterprise AI solutions for "
  "sectors such as telecommunications, financial services, manufacturing and software development, combining Claude "
  "models and Claude Code with Infosys Topaz. The Claude Agent SDK will be used to help clients build AI agents for "
  "long, complex tasks. Infosys is headquartered in Bengaluru.",
  ["Anthropic + Infosys, 17 Feb 2026", "Claude / Claude Code + Infosys Topaz", "Claude Agent SDK for client agents"],
  [fact("Anthropic announcement of 17 February 2026: Claude models and Claude Code combined with Infosys Topaz; "
        "telecom, financial services, manufacturing, software development; Claude Agent SDK; Infosys HQ Bengaluru",
        "biz_infy_anth")],
  why="The source names Infosys Topaz as the platform; the other Infosys offerings are not part of this announcement.",
  current=ca("2026-02-17"))

G(T, CP, "Basic",
  "Reliance Consumer Products, the FMCG arm of Reliance Industries, signed an MoU in March 2026 to produce, market and "
  "distribute premium chocolates in India using the recipes of Fazer. Fazer is a food company from which country?",
  ["Finland", "Sweden", "Denmark", "Norway"], "*",
  "Corporate partnerships: FMCG",
  "Reliance Consumer Products (RCPL) signed an MoU with Finnish food major Fazer for a long-term partnership under which "
  "RCPL would produce, market and distribute branded premium chocolates in India using Fazer's recipes and quality "
  "standards. The MoU was formalised during the state visit of Finland's President Alexander Stubb to India.",
  ["RCPL + Fazer (Finland)", "Premium chocolates for India", "During Finnish President's state visit, March 2026"],
  [fact("RCPL signed an MoU with Finnish food major Fazer to produce, market and distribute premium chocolates in India "
        "using Fazer's recipes; formalised during President Alexander Stubb's state visit (ANI, 6 March 2026)",
        "biz_fazer_trib")],
  why="The source calls Fazer a Finnish food major; it is not from Sweden, Denmark or Norway.",
  current=ca("2026-03-06", inferred="Tribune/ANI report datelined 6 March 2026 gives no separate signing date"))

G(T, CP, "Basic",
  "Adani Defence & Aerospace signed an MoU in New Delhi on 27 January 2026 with which aircraft maker to develop a "
  "regional transport aircraft ecosystem in India, starting with an assembly line?",
  ["Embraer", "Bombardier", "ATR", "Airbus"], "*",
  "Corporate partnerships: aerospace",
  "Adani Defence & Aerospace and Embraer, headquartered in Brazil, signed an MoU in New Delhi on 27 January 2026 for "
  "India's Regional Transport Aircraft programme. The plan is to set up an assembly line first and then raise "
  "indigenisation in phases. Nearly 50 Embraer aircraft of 11 types already operate in India.",
  ["Adani Defence & Aerospace + Embraer (Brazil)", "MoU 27 Jan 2026, New Delhi", "Assembly line, then indigenisation"],
  [fact("Adani Defence & Aerospace and Embraer signed an MoU on 27 January 2026 in New Delhi for a regional transport "
        "aircraft ecosystem; assembly line followed by phased indigenisation; Embraer headquartered in Brazil; nearly 50 "
        "Embraer aircraft of 11 types in India", "biz_emb_adani")],
  why="The source names Embraer as Adani's partner; Bombardier, ATR and Airbus are not part of this MoU.",
  current=ca("2026-01-27"))

G(T, MA, "Basic",
  "Bengaluru-based Capillary Technologies completed on 1 May 2026 the acquisition of 100% of SessionM, a loyalty and "
  "customer-engagement business. From which company did it buy SessionM?",
  ["Mastercard", "Visa", "American Express", "PayPal"], "*",
  "Acquisitions: technology",
  "Capillary Technologies, through its wholly owned subsidiary Capillary Pte. Ltd., completed on 1 May 2026 the "
  "acquisition of 100% of Session M Inc., which had been a subsidiary of Mastercard Inc. Capillary said the deal would "
  "strengthen its loyalty management and personalised marketing solutions.",
  ["Capillary Technologies buys SessionM", "Seller: Mastercard", "Completed 1 May 2026; via Capillary Pte. Ltd."],
  [fact("Capillary completed acquisition of 100 percent shareholding in Session M Inc., a subsidiary of Mastercard Inc., "
        "on 1 May 2026 through Capillary Pte. Ltd.; to enhance loyalty management and personalised marketing",
        "biz_cap_fpj")],
  why="The source says SessionM was a Mastercard subsidiary; the other payment companies were not sellers.",
  current=ca("2026-05-01"))

G(T, MA, "Basic",
  "Speciality chemicals maker Anupam Rasayan India completed on 27 February 2026 the acquisition of Jayhawk Fine "
  "Chemicals for about USD 150 million. Jayhawk's plant is in Galena, in which US state?",
  ["Kansas", "Texas", "Louisiana", "Ohio"], "*",
  "Acquisitions: overseas, chemicals",
  "Anupam Rasayan completed the acquisition of Jayhawk Fine Chemicals Corporation of Galena, Kansas, for about USD 150 "
  "million through its wholly owned subsidiary Doriath SARL. The seller was the CABB Group, which sold 100% of the "
  "equity in its US production site.",
  ["Jayhawk Fine Chemicals, Galena, Kansas", "~USD 150 million; via Doriath SARL", "Seller: CABB Group"],
  [fact("Anupam Rasayan completed the about USD 150 million acquisition of Jayhawk, Galena, Kansas, via wholly owned "
        "subsidiary Doriath SARL (PTI, 27 Feb 2026)", "biz_anu_week"),
   fact("CABB Group completed the sale of 100% of the equity of Jayhawk Fine Chemicals Corporation, Galena, Kansas, USA, "
        "to Anupam Rasayan India Ltd for USD 150 million", "biz_anu_cabb")],
  why="Both sources place Jayhawk in Galena, Kansas; it is not in the other states.",
  current=ca("2026-02-27"))

G(T, MA, "Basic",
  "Which Indian engineering and technology company completed on 4 September 2026 the acquisition of 100% of TAO "
  "Digital Solutions, an AI-native data and product engineering firm headquartered in Santa Clara, California?",
  ["Cyient", "Tata Elxsi", "KPIT Technologies", "L&T Technology Services"], "*",
  "Acquisitions: overseas, IT and engineering",
  "Cyient announced on 30 May 2026 an agreement to acquire TAO Digital, an AI-native data and product engineering firm "
  "based in Santa Clara with more than 3,500 experts. In a filing dated 4 September 2026 it said it had completed the "
  "acquisition of a 100% stake (fully diluted) in Tao Digital Solutions Inc., a company incorporated in the USA.",
  ["Cyient acquires TAO Digital (Santa Clara)", "Announced 30 May 2026; completed 4 Sep 2026", "100% stake"],
  [fact("Cyient release of 30 May 2026: agreement to acquire TAO Digital, AI-native data and product engineering firm "
        "headquartered in Santa Clara, California, 3,500+ experts", "biz_cyient_prn"),
   fact("Cyient filing dated 4 September 2026: completed acquisition of 100% stake (fully diluted) in Tao Digital "
        "Solutions Inc., incorporated in the USA", "biz_cyient_nse")],
  why="The sources name Cyient as the buyer; the other engineering companies are not involved.",
  current=ca("2026-09-04"))

# ------------------------------------------------------------------ Business: Intermediate (1)
G(T, MA, "Intermediate",
  "On 30 October 2026 the Competition Commission of India approved Adani Energy Solutions' proposal to acquire 100% of "
  "the equity of IntelliSmart Infrastructure, a provider of smart-metering infrastructure, in a deal of about ₹3,050 "
  "crore. From which two entities is the stake being bought?",
  ["NIIF and EESL", "NTPC and EESL", "NIIF and Power Finance Corporation", "REC and NTPC"], "*",
  "Competition approvals: power sector",
  "The CCI approved on Friday, 30 October 2026, Adani Energy Solutions' acquisition of all the equity of IntelliSmart "
  "Infrastructure from the National Investment and Infrastructure Fund (NIIF) and Energy Efficiency Services Ltd "
  "(EESL). The ₹3,050 crore value also covers redemption of optionally convertible debentures held by NIIF. "
  "IntelliSmart provides advanced metering infrastructure for electricity.",
  ["CCI approval: 30 Oct 2026", "Sellers: NIIF + EESL", "₹3,050 crore incl. NIIF's OCDs"],
  [fact("CCI on Friday (30 Oct 2026) approved Adani Energy Solutions' acquisition of 100% equity of IntelliSmart "
        "Infrastructure from NIIF and EESL; ₹3,050 crore including redemption of NIIF's OCDs; advanced metering "
        "infrastructure", "biz_aesl_week")],
  why="The source names NIIF and EESL as the sellers; NTPC, PFC and REC are not parties to this deal.",
  current=ca("2026-10-30"))

# ------------------------------------------------------------------ Business: Advanced (6)
GS(T, MA, "Advanced", "the acquisition of Electronic Arts (EA) completed in August 2026",
   ["The acquisition was completed on 4 August 2026 by a consortium of Saudi Arabia's Public Investment Fund (PIF), "
    "Silver Lake and Affinity Partners.",
    "EA stockholders received $210 in cash for each share of EA common stock.",
    "EA's common stock continues to trade on NASDAQ after the deal, with the consortium holding a controlling stake."],
   [True, True, False],
   "Take-private deals: gaming",
   "EA announced that a consortium of PIF, Silver Lake and Affinity Partners completed its acquisition on 4 August 2026. "
   "Stockholders received $210 in cash per share. EA's stock ceased trading and is being delisted from NASDAQ, so "
   "statement 3 is wrong. The deal had been announced on 29 September 2025 and approved by stockholders on 22 December "
   "2025.",
   [fact("EA release: consortium of PIF, Silver Lake and Affinity Partners completed the acquisition on 4 August 2026; "
         "$210 per share in cash; EA stock ceased trading and will be delisted from NASDAQ; announced 29 Sep 2025, "
         "stockholders approved 22 Dec 2025", "biz_ea"),
    fact("Silver Lake page: EA announces completion of acquisition by PIF, Silver Lake and Affinity Partners", "biz_ea_sl")],
   why="Statement 3 is wrong: EA was taken private and its stock is being delisted from NASDAQ.",
   current=ca("2026-08-04"))

GS(T, MA, "Advanced", "Palo Alto Networks' acquisition of CyberArk",
   ["Palo Alto Networks announced the completion of the acquisition on 11 February 2026.",
    "For each CyberArk ordinary share, shareholders received $45.00 in cash plus 2.2005 shares of Palo Alto Networks "
    "common stock.",
    "Palo Alto Networks said it intends to seek a secondary listing on the Tel Aviv Stock Exchange under the ticker "
    "'CYBR'."],
   [True, True, True],
   "Acquisitions: cybersecurity",
   "Palo Alto Networks' release of 11 February 2026 announced the completion of its acquisition of identity-security "
   "company CyberArk, a deal reported at about $25 billion. Each CyberArk share was exchanged for $45.00 in cash and "
   "2.2005 Palo Alto Networks shares. The company said it intends to seek a secondary listing on the Tel Aviv Stock "
   "Exchange under CyberArk's old ticker 'CYBR', while continuing to trade on NASDAQ as PANW. All three statements are "
   "correct.",
   [fact("Release dated 11 February 2026: completion of acquisition of CyberArk; $45.00 cash + 2.2005 PANW shares per "
         "CyberArk share; intends secondary listing on TASE under 'CYBR'; continues on NASDAQ as PANW", "biz_cybr_sec"),
    fact("Palo Alto officially completed its $25 billion acquisition of CyberArk (Techzine, 12 Feb 2026)", "biz_cybr_tz")],
   why="All three statements match the completion release.",
   current=ca("2026-02-11"))

GS(T, MA, "Advanced", "Zydus Lifesciences' acquisition of Assertio Holdings, completed in June 2026",
   ["Zydus completed a cash tender offer at $23.50 per share through Zara Merger Sub Inc., a wholly owned subsidiary.",
    "Assertio's shares were listed on the New York Stock Exchange before the deal.",
    "Assertio, a US-based company focused on specialty and oncology supportive care therapies, became a wholly owned "
    "subsidiary of Zydus."],
   [True, False, True],
   "Acquisitions: overseas, pharmaceuticals",
   "Zydus Lifesciences said on Tuesday, 16 June 2026, that it had completed the cash tender offer for Assertio Holdings "
   "at $23.50 per share through Zara Merger Sub Inc. The deal was valued at about $166.4 million (over ₹1,590 crore). "
   "Assertio, which focuses on specialty and oncology supportive care therapies, became a wholly owned subsidiary and "
   "its shares are no longer listed on the Nasdaq Global Market, so statement 2 is wrong.",
   [fact("Zydus completed the cash tender offer at $23.50 per share via Zara Merger Sub Inc.; $166.4 million; Assertio "
         "now a wholly owned subsidiary; no longer listed or traded on the Nasdaq Global Market; specialty and oncology "
         "supportive care (Medical Dialogues, 17 June 2026, 'on Tuesday')", "biz_zyd_md"),
    fact("Zydus press release of 16 June 2026 announcing successful completion of acquisition of Assertio Holdings",
         "biz_zyd_nse")],
   why="Statement 2 is wrong: Assertio was listed on the Nasdaq Global Market, not the NYSE.",
   current=ca("2026-06-16"))

GS(T, MA, "Advanced", "the merger of Devon Energy and Coterra Energy, completed in May 2026",
   ["Former Coterra shareholders own about 54% of the combined company.",
    "Each Coterra common share was converted into 0.70 Devon common share.",
    "The combined company is headquartered in Houston and trades on the NYSE under the ticker DVN."],
   [False, True, True],
   "Mergers: energy",
   "Devon Energy completed its all-stock merger with Coterra Energy. Each Coterra share became 0.70 Devon share; former "
   "Devon shareholders own about 54% and former Coterra shareholders about 46%, so statement 1 is wrong. The company is "
   "headquartered in Houston with a continued presence in Oklahoma City, trades on the NYSE as DVN, and has a stronger "
   "position in the Delaware basin. Former Coterra chairman Tom Jorden is non-executive chairman.",
   [fact("Devon completed merger with Coterra: 0.70 Devon share per Coterra share; Devon holders ~54%, Coterra holders "
         "~46%; HQ Houston, presence in Oklahoma City; NYSE: DVN; Tom Jorden non-executive chairman (World Oil, 7 May "
         "2026)", "biz_dvn_wo")],
   why="Statement 1 is wrong: former Coterra shareholders own about 46%; about 54% is held by former Devon shareholders.",
   current=ca("2026-05-07", inferred="World Oil report dated 7 May 2026 reports the merger as completed"))

GS(T, CP, "Advanced", "the MoU signed by Air India and the Lufthansa Group on 17 February 2026",
   ["The MoU is a final joint business agreement that had already received all regulatory approvals when signed.",
    "It covers Air India and Air India Express and, on the Lufthansa side, Austrian Airlines, Brussels Airlines, ITA "
    "Airways, Lufthansa and SWISS.",
    "The airlines' existing codeshare covers 145 routes across 15 Indian and 29 European cities."],
   [False, True, True],
   "Corporate partnerships: aviation",
   "Air India and the Lufthansa Group signed an MoU on 17 February 2026 to advance a joint business partnership. It is "
   "a framework for a future joint business agreement whose scope will be finalised subject to regulatory approvals, so "
   "statement 1 is wrong. It covers Air India, Air India Express and the Lufthansa Group carriers Austrian, Brussels, "
   "ITA Airways, Lufthansa and SWISS, with coordinated route planning, schedules, joint sales and integrated "
   "frequent-flyer programmes. Their existing codeshare covers 145 routes across 15 Indian and 29 European cities.",
   [fact("MoU signed 17 Feb 2026; carriers: Air India, Air India Express, Austrian, Brussels, ITA Airways, Lufthansa, "
         "SWISS; existing codeshare 145 routes across 15 Indian and 29 European cities (CAPA, 18 Feb 2026)",
         "biz_ailh_capa"),
    fact("Air India release: MoU to advance a joint business partnership; precise scope to be finalised on formation "
         "of a comprehensive joint business agreement, subject to regulatory approvals", "biz_ailh_ai")],
   why="Statement 1 is wrong: the MoU only sets a framework; a joint business agreement still needs regulatory "
       "approvals.",
   current=ca("2026-02-17"))

GS(T, CP, "Advanced", "the MoU signed by NTPC and Électricité de France (EDF) in April 2026",
   ["It is a non-binding MoU to explore cooperation in nuclear power projects in India.",
    "The partners will evaluate EDF's European Pressurised Reactor (EPR) technology for its suitability for India.",
    "It was signed on behalf of NTPC by Anushakti Vidhyut Nigam Ltd (Ashvini), NTPC's joint venture with NPCIL."],
   [True, True, False],
   "Corporate partnerships: nuclear power",
   "NTPC signed a non-binding MoU with EDF on 8 April 2026, after approvals from the relevant ministries, to explore "
   "nuclear power projects in India. The partners will assess EDF's EPR technology for Indian conditions, localisation, "
   "economic and tariff aspects, possible sites and training. It was signed for NTPC by Arnada Prasad Samal, CGM "
   "(Nuclear Cell), not by Ashvini, so statement 3 is wrong; Ashvini is the NPCIL-NTPC joint venture building reactors "
   "at Mahi Banswara in Rajasthan.",
   [fact("Non-binding MoU; evaluate EDF's EPR technology for India; signed for NTPC by Arnada Prasad Samal, CGM (Nuclear "
         "Cell); Ashvini is NPCIL-NTPC JV developing Mahi Banswara (WNN, 9 April 2026)", "biz_ntpc_wnn"),
    fact("NTPC signed a non-binding MoU with EDF (PSU Watch, 8 April 2026); signed by Arnada Prasad Samal, CGM (Nuclear "
         "Cell)", "biz_ntpc_psu"),
    fact("NTPC stock-exchange press release dated 8 April 2026 on the MoU with EDF", "biz_ntpc_pdf")],
   why="Statement 3 is wrong: NTPC itself signed through its CGM (Nuclear Cell); Ashvini was not the signatory.",
   current=ca("2026-04-08"))

# ------------------------------------------------------------------ Static Awareness: Intermediate (1)
G("Static Awareness", "National parks and dams", "Intermediate",
  "A dam in Mandya district, Karnataka, originally called 'Kannambadi Katte', was built between 1911 and 1932 and "
  "renamed in 1917 after a ruler of Mysore; the Brindavan Gardens lie at its foot. By what name is it known today, and "
  "on which river is it built?",
  ["Krishnaraja Sagara; Kaveri", "Tungabhadra Dam; Tungabhadra", "Almatti Dam; Krishna", "Linganamakki Dam; Sharavati"],
  "*",
  "Dams of India: Karnataka",
  "The Mandya district administration describes the KRS dam as having been built across the Kaveri at Kannambadi, "
  "originally called Kannambadi Katte. It was renamed Krishnaraja Sagara in 1917 after King Krishnaraja Odeya IV, was "
  "built between 1911 and 1932 at a cost of about two and a half crore rupees, and has the Brindavan Gardens at its "
  "foot.",
  ["Kannambadi Katte -> Krishnaraja Sagara (1917)", "River: Kaveri; Mandya district", "Built 1911-1932; Brindavan Gardens"],
  [fact("Mandya district (NIC) page: KRS dam across the river Kaveri at Kannambadi ('Kannambadi Katte'); renamed "
        "Krishnaraja Sagara in 1917 after King Krishnaraja Odeya IV; built 1911-1932; Brindavan Gardens at the bottom of "
        "the dam", "st_krs_nic")],
  why="The official page identifies the dam as Krishnaraja Sagara on the Kaveri; the other dams are not described there.")


# ====================================================================== build
def place_answers(items):
    """Keep fixed keys; move the correct option of flexible items so overall keys are balanced."""
    counts = Counter(it["answer"] for it in items if it["answer"] != "*")
    turn = 0
    for it in items:
        if it["answer"] != "*":
            continue
        low = min(counts.get(k, 0) for k in LETTERS)
        candidates = [k for k in LETTERS if counts.get(k, 0) == low]
        key = candidates[turn % len(candidates)]
        turn += 1
        idx = LETTERS.index(key)
        opts = it["options"]
        opts[0], opts[idx] = opts[idx], opts[0]
        it["answer"] = key
        counts[key] += 1
    return counts


def build(items):
    plan = json.loads((ROOT / "batches" / "plans" / f"{BATCH}_plan.json").read_text(encoding="utf-8"))
    ga = next(s for s in plan["subjects"] if s["subject"] == GA)
    first = int(ga["question_ids"][0].rsplit("_", 1)[1])
    counts = place_answers(items)
    out = []
    for n, it in enumerate(items):
        ans = it["answer"]
        opts = it["options"]
        hows = {f.pop("_how") for f in it["facts"]}
        verified_by = list(AI_CHECK)
        if any(m in it["text"] for m in REWORDED_AFTER_CHECK):
            verified_by = ["ai:self-recheck"]
        if OPENED in hows:
            verified_by.append("web:fact-check")
        if SEARCH in hows:
            verified_by.append("web:search-confirmed")
        q = {
            "question_id": f"BANK_GA_{first + n:06d}",
            "exam_mappings": default_mappings(GA, it["difficulty"]),
            "subject": GA, "topic": it["topic"], "subtopic": it["subtopic"], "difficulty": it["difficulty"],
            "question_type": "MCQ", "language": "en",
            "question_text": it["text"],
            "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(opts)],
            "correct_answer": ans,
            "solution": {"concept": it["concept"], "explanation": it["explanation"], "steps": it["steps"],
                         "shortcut": it["shortcut"], "why_others_wrong": it["why"],
                         "final_answer": f"Option {ans}: {opts[LETTERS.index(ans)]}"},
            "suggested_time_seconds": SECONDS[it["difficulty"]],
        }
        if it["current"]:
            q["current_affairs"] = it["current"]
        q["source"] = {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                       "original_exam_year": None, "license_note": None}
        q["verification"] = {"answer_verified": True, "solution_verified": True,
                             "review_status": "Pending Human Review",
                             "verified_by": verified_by, "verified_at": TODAY,
                             "fact_checks": it["facts"]}
        out.append(q)

    # quota check against the plan before writing
    have = Counter((q["topic"], q["difficulty"]) for q in out)
    for t in ga["topics"]:
        for d, k in t["quota"].items():
            assert have[(t["topic"], d)] == k, (t["topic"], d, have[(t["topic"], d)], k)
        assert all(q["subtopic"] in t["subtopics"] for q in out if q["topic"] == t["topic"]), t["topic"]
    assert len(out) == ga["total"] == 149
    assert out[0]["question_id"] == ga["question_ids"][0] and out[-1]["question_id"] == ga["question_ids"][1]
    for q in out:
        if q["topic"] in CA_TOPICS:
            assert CA_FROM <= q["current_affairs"]["event_date"] <= CA_TO, q["question_id"]
        texts = [o["text"] for o in q["options"]]
        if texts in (S12, S123):
            assert q["correct_answer"] in LETTERS
    assert len({q["question_text"] for q in out}) == len(out)
    assert max(counts.values()) - min(counts.values()) <= 2, counts
    return out, counts


_plan = json.loads((ROOT / "batches" / "plans" / f"{BATCH}_plan.json").read_text(encoding="utf-8"))
_order = [t["topic"] for t in next(s for s in _plan["subjects"] if s["subject"] == GA)["topics"]]
_rank = {"Basic": 0, "Intermediate": 1, "Advanced": 2}
QUESTIONS.sort(key=lambda it: (_order.index(it["topic"]), _rank[it["difficulty"]]))

questions, keys = build(QUESTIONS)
print("inferred dates:", len(INFERRED))
for d, why in INFERRED:
    print("  ", d, why)
batch = {
    "schema_version": "1.0",
    "batch_id": BATCH,
    "created_at": TODAY,
    "notes": "BATCH_009 General Awareness part: 149 original questions. Current-affairs topics (National and "
             "International Current Affairs, Appointments, Awards, Sports, Summits, Economic Affairs, Business) test "
             "events dated 2025-11-01 to 2026-11-04, with event dates from the sources and review_by 2027-05-05. "
             "Other time-sensitive facts also carry current_affairs dates. No fact or event tested in BATCH_000 to "
             "BATCH_008 GA is tested again. Fact checks dated 2026-11-06 (the day the pages were checked); verified_by says whether each question's "
             "sources were opened (web:fact-check) or confirmed only in search results (web:search-confirmed). "
             "Pending human review. Event dates inferred (source gives no exact day): " +
             "; ".join(f"{d} ({why})" for d, why in INFERRED) + ".",
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / f"{BATCH}_GA.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions; keys {dict(sorted(keys.items()))})")
