"""Writes batches/parts/BATCH_008_GA.json: the 149 General Awareness questions of BATCH_008.

Same structure as tools/batch_007/ga.py. Current-affairs topics (National and International Current Affairs,
Appointments, Awards, Sports, Summits, Economic Affairs, Business) test events dated 2025-11-01 to 2026-11-04 with
event dates from the sources; every such question carries current_affairs {event_date, review_by 2027-05-05}. Other
time-sensitive facts (schemes, policies, reports, books, current heads) carry current_affairs too. Where a source gives
no exact day, ca(..., inferred=reason) records it and the list is printed and written into the batch notes.

Every question has fact_checks, and at least one source per question is an official/primary site or a major news
outlet (never only Wikipedia or an exam-prep site). Each URL is marked OPENED (fetched and read, giving
"web:fact-check") or SEARCH (confirmed only from search-result text, giving "web:search-confirmed"). checked_on is the
date the page was actually checked (2026-11-06). Sites that refused a fetch (e.g. pib.gov.in pages,
business-standard.com, thestatesman.com, britannica.com, unep.org, oecd.org, pmindia.gov.in) were not worked around.
Explanations and why_others_wrong state only facts backed by the listed sources, or stay neutral.

All earlier GA stems (BATCH_000 sample, BATCH_001_GA to BATCH_007_GA, 1,053 questions) were read first; no fact or
event tested there is tested again, and no event is used twice in this batch.

Statement questions have their key fixed by the statements (computed from truth values); other questions are written
with the correct option first and answer "*", and are then placed so that keys are balanced A to D.

    python tools/batch_008/ga.py
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
BATCH = "BATCH_008"
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
    "nat_jjm_air": ("https://newsonair.gov.in/cabinet-approves-extension-of-jal-jeevan-mission-up-to-december-2028/",
                    OPENED),
    "nat_jjm_dd": ("https://ddnews.gov.in/en/cabinet-approves-extension-of-jal-jeevan-mission-till-december-2028-outlay-"
                   "raised-to-rs-8-69-lakh-crore/", SEARCH),
    "nat_msp_air": ("https://newsonair.gov.in/cabinet-approves-msp-for-kharif-crops-for-2026-27-season/", OPENED),
    "nat_itla_pio": ("https://dailypioneer.com/news/cabinet-approves-integrated-transport-logistics-authority", OPENED),
    "nat_itla_ys": ("https://yourstory.com/2026/10/cabinet-approves-proposal-to-set-up-integrated-transport-and-"
                    "logistics-authority", SEARCH),
    "nat_nvs_air": ("https://newsonair.gov.in/isro-launches-nvs-03-satellite-strengthening-indias-indigenous-navigation-"
                    "capabilities/", OPENED),
    "nat_cmp_dd": ("https://ddnews.gov.in/en/capex-support-scheme-to-promote-critical-mineral-processing-a-rs-2814-crore-"
                   "push-for-domestic-lithium-and-nickel-processing/", OPENED),
    "nat_plb_air": ("https://newsonair.gov.in/cabinet-approves-78-days-productivity-linked-bonus-for-over-11-4-lakh-"
                    "railway-employees/", OPENED),
    "nat_plb_na": ("https://www.newsarenaindia.com/tag/union-cabinet", SEARCH),
    "nat_rail_dd": ("https://ddnews.gov.in/en/cabinet-approves-three-railway-multitracking-projects-worth-%E2%82%B99072-"
                    "crore/", OPENED),
    "nat_yyb_dd": ("https://ddnews.gov.in/en/cabinet-approves-transition-of-north-south-blocks-into-yuge-yugeen-bharat-"
                   "national-museum/", OPENED),
    # ---- States and UTs
    "nat_sik_air": ("https://newsonair.gov.in/sikkim-becomes-countrys-first-paperless-judiciary-state/", OPENED),
    "nat_tsim_dd": ("https://www.devdiscourse.com/article/law-order/3819057-tripura-launches-indias-first-state-"
                    "innovation-mission", OPENED),
    "nat_tsim_itne": ("https://www.indiatodayne.in/tripura/story/tripura-to-launch-indias-first-state-ai-policy-agartala-"
                      "to-get-ai-based-smart-solutions-1352109-2026-02-26", SEARCH),
    "nat_cg_itv": ("https://www.indiatvnews.com/chhattisgarh/chhattisgarh-becomes-first-state-to-adopt-risk-based-"
                   "business-approval-system-2026-07-16-1048480", OPENED),
    "nat_cg_dc": ("https://www.deccanchronicle.com/nation/chhattisgarh-becomes-first-state-with-risk-based-business-"
                  "approvals-1971480", SEARCH),
    "nat_up_bt": ("https://www.businesstoday.in/india/story/uttar-pradesh-presents-first-ever-economic-survey-2025-26-"
                  "targets-1-trillion-economy-with-investment-led-growth-515312-2026-02-09", OPENED),
    "nat_up_fpj": ("https://www.freepressjournal.in/india/up-presents-first-ever-economic-survey-eyes-1-trillion-economy",
                   SEARCH),
    "nat_kml_sf": ("https://thesouthfirst.com/health/menstrual-leave-policy-now-a-reality-in-karnataka", OPENED),
    "nat_kml_tnm": ("https://www.thenewsminute.com/karnataka/karnataka-approves-menstrual-leave-policy-allowing-one-day-"
                    "paid-leave-per-month", OPENED),
    "nat_pb_air": ("https://newsonair.gov.in/punjab-government-launches-punjab-sikhya-kranti-2-0-to-reform-school-"
                   "education-in-collaboration-with-world-bank/", OPENED),
    "nat_as_air": ("https://newsonair.gov.in/assam-cm-himanta-biswa-sarma-inaugurates-indias-first-ai-powered-phygital-"
                   "banking-branch-in-guwahati/", OPENED),
    "nat_bhi_dd": ("https://ddnews.gov.in/en/rajasthan-enters-indias-semiconductor-map-with-inauguration-of-states-first-"
                   "chip-packaging-facility-in-bhiwadi/", OPENED),
    # ---- Defence
    "nat_sfdr_itv": ("https://www.indiatvnews.com/news/india/drdo-successfully-tests-advanced-ramjet-technology-india-air-"
                     "combat-capability-to-get-major-boost-2026-02-03-1028779", OPENED),
    "nat_fss_dc": ("https://www.deccanchronicle.com/southern-states/andhra-pradesh/rajnath-singh-launches-first-"
                   "indigenous-fss-surya-in-vizag-1993651", OPENED),
    "nat_sud_dd": ("https://ddnews.gov.in/en/ins-sudarshini-returns-to-kochi-after-completing-22000-nautical-mile-"
                   "lokayan-26-expedition/", OPENED),
    "nat_dac_psu": ("https://www.psuconnect.in/ministry-of-india-news/dac-clears-capital-acquisition-proposals-worth-2-12-"
                    "lakh-crore-for-defence-forces", OPENED),
    "nat_dac2_tt": ("https://telanganatoday.com/defence-acquisition-council-clears-rs-52000-crore-military-procurement-"
                    "proposals-to-boost-armed-forces", OPENED),
    "nat_ngopv_bm": ("https://www.bairdmaritime.com/security/naval/naval-ships/grse-launches-third-offshore-patrol-vessel",
                     OPENED),
    "nat_ngopv_psu": ("https://www.psuconnect.in/psu-news/grse-launches-shreyas-third-ngopv-in-under-five-months", SEARCH),
    "nat_rad_dd": ("https://ddnews.gov.in/en/mod-inks-rs-1950-crore-pact-with-bel-for-iaf-mountain-radars-system/", OPENED),
    "nat_dor_dd": ("https://ddnews.gov.in/en/india-signs-%E2%82%B92312-crore-deal-with-hal-for-eight-dornier-aircraft-for-"
                   "coast-guard/", OPENED),
    "nat_mal_dd": ("https://ddnews.gov.in/en/indian-navy-commissions-ins-malvan-second-mahe-class-anti-submarine-shallow-"
                   "water-craft/", OPENED),
})

T = "National Current Affairs"
GOV, ST, DEF = "Government decisions", "States and UTs", "Defence"

# ------------------------------------------------------------------ National CA: Basic (9)
G(T, GOV, "Basic",
  "Along with extending the Jal Jeevan Mission, the Union Cabinet on 10 March 2026 approved declaring which airport in "
  "Tamil Nadu an international airport?",
  ["Madurai Airport", "Thoothukudi Airport", "Salem Airport", "Vellore Airport"], "*",
  "Cabinet decisions: airports",
  "At the Cabinet meeting reported on 10 March 2026, Madurai Airport in Tamil Nadu was declared an international "
  "airport. The same set of decisions extended the Jal Jeevan Mission to December 2028 and cleared a greenfield "
  "connectivity corridor for Jewar Airport.",
  ["Cabinet, 10 March 2026", "Madurai Airport (Tamil Nadu) declared international"],
  [fact("AIR report of 10 March 2026: Cabinet declared Madurai Airport, Tamil Nadu, an international airport; same "
        "briefing extended JJM to December 2028", "nat_jjm_air")],
  why="The source names Madurai Airport; the other airports are not mentioned in the decision.",
  current=ca("2026-03-10", inferred="AIR report published the evening of 10 March 2026 on that day's Cabinet decisions"))

G(T, GOV, "Basic",
  "After the Prime Minister's Office moved to Seva Teerth, the Union Cabinet in February 2026 approved integrating the "
  "historic North and South Blocks into which proposed museum?",
  ["Yuge Yugeen Bharat National Museum", "Pradhanmantri Sangrahalaya", "Bharat Mandapam Heritage Museum",
   "Kartavya Path National Museum"], "*",
  "Cabinet decisions: heritage buildings",
  "The Union Cabinet approved the transition of the North and South Blocks into the proposed Yuge Yugeen Bharat "
  "National Museum. Cabinet meetings will no longer be held in South Block, which had nearly 95 years of continuous "
  "administrative use; the new PMO complex, Seva Teerth, was dedicated on 13 February 2026.",
  ["North and South Blocks -> Yuge Yugeen Bharat National Museum", "South Block: ~95 years of administrative use"],
  [fact("Cabinet approved transition of North and South Blocks into the proposed Yuge Yugeen Bharat National Museum; "
        "Cabinet meetings no longer to be held in South Block (DD News, 14 Feb 2026)", "nat_yyb_dd")],
  why="The source names the Yuge Yugeen Bharat National Museum; the other names are not used for this project.",
  current=ca("2026-02-13", inferred="DD News of 14 Feb 2026 says the Cabinet approved it 'on Friday' (13 Feb 2026)"))

G(T, ST, "Basic",
  "Which State was declared the country's first paperless judiciary state by Chief Justice of India Surya Kant in May "
  "2026?",
  ["Sikkim", "Kerala", "Goa", "Tripura"], "*",
  "State firsts: judiciary",
  "At a conclave in Gangtok, Chief Justice of India Surya Kant declared Sikkim the country's first paperless judiciary "
  "state. Chief Minister Prem Singh Tamang Golay welcomed it, saying e-filing and digital case management would make "
  "justice delivery faster and more transparent.",
  ["Sikkim: first paperless judiciary state", "Declared by CJI Surya Kant at Gangtok"],
  [fact("Sikkim declared the country's first paperless judiciary state by CJI Surya Kant at a conclave in Gangtok (AIR, "
        "1 May 2026)", "nat_sik_air")],
  why="The source names Sikkim; Kerala, Goa and Tripura were not declared.",
  current=ca("2026-05-01", inferred="AIR report dated 1 May 2026 gives no separate date for the conclave"))

G(T, ST, "Basic",
  "Under Karnataka's Menstrual Leave Policy, 2025, notified by the State labour department on 12 November 2025, how "
  "many days of paid menstrual leave can an eligible woman employee get in a year?",
  ["12", "6", "10", "24"], "*",
  "State policies: menstrual leave",
  "The Karnataka labour department notified the Menstrual Leave Policy, 2025 on 12 November 2025. It gives one day of "
  "paid leave a month, or 12 days a year, to permanent, contract and outsourced women employees; no medical certificate "
  "is needed and unused leave cannot be carried forward. The Cabinet had approved the policy on 9 October 2025; a "
  "six-day proposal had been floated earlier.",
  ["1 day per month = 12 days per year", "Notified 12 Nov 2025; no medical certificate; no carry-forward"],
  [fact("Notified on Wednesday, 12 November 2025; 12 paid days a year, one per month; no medical certificate; no "
        "carry-forward", "nat_kml_sf"),
   fact("Cabinet approved the Menstrual Leave Policy, 2025 on 9 October; one paid day per month; government had earlier "
        "floated six days a year", "nat_kml_tnm")],
  why="The policy gives one day a month, i.e. 12 days; six days a year was only an earlier proposal.",
  current=ca("2025-11-12"))

G(T, ST, "Basic",
  "'Punjab Sikhya Kranti 2.0', the second phase of Punjab's school education reform with a total investment of ₹3,500 "
  "crore over six years, is being carried out with loan assistance from which institution?",
  ["World Bank", "Asian Development Bank", "Asian Infrastructure Investment Bank", "New Development Bank"], "*",
  "State initiatives: education",
  "Punjab's Sikhya Kranti 2.0 has a total investment of ₹3,500 crore over six years: ₹2,500 crore as a World Bank loan "
  "and ₹1,000 crore from the State government.",
  ["₹3,500 crore = ₹2,500 crore World Bank loan + ₹1,000 crore State", "Duration: six years"],
  [fact("Punjab Sikhya Kranti 2.0 in collaboration with the World Bank; ₹3,500 crore (₹2,500 crore World Bank loan, "
        "₹1,000 crore State) over six years (AIR, 18 March 2026)", "nat_pb_air")],
  why="The source names the World Bank as lender; the other banks are not involved.",
  current=ca("2026-03-18", inferred="AIR report dated 18 March 2026 gives no separate launch date"))

G(T, ST, "Basic",
  "India's first AI-powered 'phygital' banking branch, inaugurated by Assam Chief Minister Himanta Biswa Sarma at GS "
  "Road, Guwahati, in May 2026, belongs to which bank?",
  ["Slice Small Finance Bank", "AU Small Finance Bank", "Ujjivan Small Finance Bank", "Equitas Small Finance Bank"],
  "*",
  "State firsts: banking",
  "Assam Chief Minister Himanta Biswa Sarma inaugurated Slice Small Finance Bank's branch at GS Road, Guwahati, "
  "described as India's first AI-powered phygital branch. It combines physical and digital banking through AI-enabled "
  "self-service kiosks, paperless cash deposits and withdrawals, and simple digital onboarding.",
  ["Slice Small Finance Bank, GS Road, Guwahati", "First AI-powered phygital branch"],
  [fact("Assam CM Himanta Biswa Sarma inaugurated Slice Small Finance Bank's branch at GS Road, Guwahati, India's first "
        "AI-powered phygital banking branch (AIR, 16 May 2026)", "nat_as_air")],
  why="The source names Slice Small Finance Bank; the other small finance banks are not mentioned.",
  current=ca("2026-05-16", inferred="AIR report dated 16 May 2026 gives no separate inauguration date"))

G(T, DEF, "Basic",
  "DRDO flight-tested Solid Fuel Ducted Ramjet (SFDR) technology from the Integrated Test Range, Chandipur, on 3 "
  "February 2026. DRDO described this technology as crucial for developing which weapons?",
  ["Long-range air-to-air missiles", "Submarine-launched ballistic missiles", "Man-portable anti-tank missiles",
   "Intercontinental ballistic missiles"], "*",
  "DRDO tests: propulsion",
  "On 3 February 2026 DRDO tested SFDR technology from ITR Chandipur. A ground booster took the missile to the "
  "required Mach number, after which the ramjet took over; the nozzle-less booster, ramjet motor and fuel flow "
  "controller worked as designed. DRDO called SFDR crucial for long-range air-to-air missiles.",
  ["SFDR test: 3 Feb 2026, ITR Chandipur", "Purpose: long-range air-to-air missiles"],
  [fact("SFDR flight test on 3 February from ITR Chandipur; 'very crucial for development of long range Air to Air "
        "Missiles'; nozzle-less booster, ramjet motor, fuel flow controller", "nat_sfdr_itv")],
  why="The source links SFDR to long-range air-to-air missiles, not to the other missile types.",
  current=ca("2026-02-03"))

G(T, DEF, "Basic",
  "INS Malvan, the second ship of the indigenous Mahe-class Anti-Submarine Warfare Shallow Water Craft, was "
  "commissioned on 22 July 2026 as the first Indian naval ship to be commissioned at which place?",
  ["Karwar", "Kochi", "Mumbai", "Visakhapatnam"], "*",
  "Navy: commissioning",
  "INS Malvan, built by Cochin Shipyard Ltd with about 80% indigenous content, was commissioned at Karwar, Karnataka, "
  "becoming the first Indian naval ship commissioned there.",
  ["INS Malvan: 2nd Mahe-class ASW-SWC", "Commissioned 22 July 2026 at Karwar (first there)", "Builder: Cochin Shipyard"],
  [fact("INS Malvan, second Mahe-class ASW-SWC built by Cochin Shipyard, commissioned at Karwar on Wednesday (22 July "
        "2026); first Indian naval ship commissioned at Karwar", "nat_mal_dd")],
  why="The source says INS Malvan was the first naval ship commissioned at Karwar; it was built at Kochi, not "
      "commissioned there.",
  current=ca("2026-07-22"))

G(T, DEF, "Basic",
  "In February 2026 the Ministry of Defence signed a ₹2,312 crore contract with HAL for eight Dornier 228 aircraft. "
  "Which force are these aircraft for?",
  ["Indian Coast Guard", "Indian Navy", "Indian Air Force", "Border Security Force"], "*",
  "Defence contracts",
  "The Ministry of Defence signed a ₹2,312 crore contract with HAL's Transport Aircraft Division, Kanpur, for eight "
  "Dornier 228 aircraft with operational role equipment for the Indian Coast Guard, under the Buy (Indian) category, to "
  "strengthen maritime and coastal surveillance.",
  ["8 Dornier 228, ₹2,312 crore", "User: Indian Coast Guard", "HAL Transport Aircraft Division, Kanpur; Buy (Indian)"],
  [fact("₹2,312 crore contract with HAL for eight Dornier 228 aircraft for the Indian Coast Guard; Buy (Indian); HAL "
        "Transport Aircraft Division, Kanpur; signed on Wednesday (DD News, 12 Feb 2026)", "nat_dor_dd")],
  why="The source says the aircraft are for the Indian Coast Guard, not the other forces.",
  current=ca("2026-02-11", inferred="DD News of 12 Feb 2026 says the contract was signed on Wednesday (11 Feb 2026)"))

# ------------------------------------------------------------------ National CA: Intermediate (6)
G(T, GOV, "Intermediate",
  "In the Minimum Support Prices for 14 Kharif crops for the 2026-27 season approved by the CCEA in May 2026, which "
  "crop got the highest increase per quintal over the previous year?",
  ["Sunflower seed", "Cotton", "Sesamum", "Tur (arhar)"], "*",
  "Cabinet decisions: MSP",
  "The CCEA raised MSPs of 14 Kharif crops for 2026-27. The largest rise was for sunflower seed (₹622 per quintal), "
  "followed by cotton (₹557) and sesamum (₹500). Grade A paddy MSP is ₹2,461 per quintal; the estimated payout to "
  "farmers is ₹2.60 lakh crore.",
  ["Highest rise: sunflower seed +₹622", "Next: cotton +₹557, sesamum +₹500"],
  [fact("Kharif MSP 2026-27: highest increase sunflower seed ₹622/qtl, then cotton ₹557 and sesamum ₹500; 14 crops; "
        "payout ₹2.60 lakh crore (AIR, 13 May 2026)", "nat_msp_air")],
  why="Cotton (₹557) and sesamum (₹500) rose less than sunflower seed (₹622); tur is not among the top increases.",
  current=ca("2026-05-13", inferred="AIR report dated 13 May 2026 gives no separate CCEA meeting date"))

G(T, GOV, "Intermediate",
  "The Union Cabinet in October 2026 approved a Productivity Linked Bonus equal to 78 days' wages for over 11.4 lakh "
  "non-gazetted railway employees. What is the maximum amount payable per eligible employee?",
  ["₹17,951", "₹7,000", "₹18,000", "₹20,000"], "*",
  "Cabinet decisions: railway bonus",
  "The Cabinet approved a Productivity Linked Bonus of 78 days' wages for over 11.4 lakh railway employees, costing "
  "over ₹2,009 crore. The maximum payable per eligible employee is ₹17,951. Beneficiaries include track maintainers, "
  "loco pilots, train managers (guards), station masters, technicians and pointsmen.",
  ["78 days' wages; >11.4 lakh employees; >₹2,009 crore", "Maximum per employee: ₹17,951"],
  [fact("78 days' PLB for over 11.4 lakh railway employees; over ₹2,009 crore; maximum payable 17,951 (AIR, 15 Oct "
        "2026)", "nat_plb_air"),
   fact("On 14 October 2026 the Cabinet approved a 78-day bonus for about 11.4 lakh railway staff", "nat_plb_na")],
  why="The source gives the ceiling as ₹17,951 per employee; the other amounts are not stated.",
  current=ca("2026-10-14", inferred="AIR report early on 15 Oct 2026; search result (News Arena) dates the approval "
             "14 Oct"))

G(T, ST, "Intermediate",
  "Uttar Pradesh presented its first-ever State Economic Survey (2025-26) in the Assembly on 9 February 2026. Who "
  "presented it?",
  ["Suresh Khanna", "Keshav Prasad Maurya", "Brajesh Pathak", "Yogi Adityanath"], "*",
  "States: Economic Survey",
  "Uttar Pradesh Finance Minister Suresh Khanna presented the State's first annual Economic Survey, modelled on the "
  "Centre's, on 9 February 2026. It put UP's GSDP at ₹30.25 lakh crore in 2024-25 (up from ₹13.30 lakh crore in "
  "2016-17), expected to reach ₹36 lakh crore in 2025-26, and set a goal of a $1 trillion economy.",
  ["Presented by FM Suresh Khanna, 9 Feb 2026", "GSDP ₹30.25 lakh crore (2024-25); target $1 trillion"],
  [fact("UP's first-ever Economic Survey presented in the Assembly on Monday, 9 February 2026 by Finance Minister "
        "Suresh Khanna; GSDP ₹30.25 lakh crore in 2024-25; ₹36 lakh crore expected in 2025-26", "nat_up_bt"),
   fact("UP presents first-ever Economic Survey, eyes $1 trillion economy", "nat_up_fpj")],
  why="The source names Finance Minister Suresh Khanna as the presenter; the Chief Minister and Deputy CMs did not "
      "present it.",
  current=ca("2026-02-09"))

G(T, DEF, "Intermediate",
  "On 26 October 2026 the Defence Acquisition Council chaired by Rajnath Singh accorded Acceptance of Necessity to "
  "proposals worth about ₹2.12 lakh crore. Roughly what share of this value is to come from Indian industry?",
  ["About 82%", "About 68%", "About 75%", "About 90%"], "*",
  "Defence procurement: DAC",
  "The DAC meeting of 26 October 2026 approved AoN for proposals worth about ₹2.12 lakh crore, roughly 82% of it from "
  "Indian industry. Army items include high mobility vehicles, self-propelled tracked guns, VSHORADS and Light Multi "
  "Role Helicopters; the Navy gets Active Offboard Decoy Systems and the Air Force a Mobile X-Band Doppler Weather "
  "Radar System.",
  ["DAC, 26 Oct 2026: ~₹2.12 lakh crore", "~82% from Indian industry"],
  [fact("DAC meeting 26 October 2026, chaired by Rajnath Singh, ~₹2.12 lakh crore; roughly 82% from Indian industry",
        "nat_dac_psu")],
  why="The source puts the domestic share at about 82%, not the other percentages.",
  current=ca("2026-10-26"))

G(T, DEF, "Intermediate",
  "'Shreyas', launched by Garden Reach Shipbuilders and Engineers at Kolkata on 10 October 2026, is the third ship of "
  "which class being built for the Indian Navy?",
  ["Next Generation Offshore Patrol Vessel", "Anti-Submarine Warfare Shallow Water Craft", "Fleet Support Ship",
   "Survey Vessel (Large)"], "*",
  "Navy: ship launches",
  "GRSE launched Shreyas, the third Next Generation Offshore Patrol Vessel (NGOPV), on 10 October 2026. The Ministry of "
  "Defence contracted 11 NGOPVs in March 2023: seven from Goa Shipyard and four from GRSE. The GRSE ships are about "
  "113 m long and displace about 3,000 tonnes.",
  ["Shreyas: 3rd NGOPV, GRSE, 10 Oct 2026", "11 NGOPVs: 7 GSL + 4 GRSE"],
  [fact("GRSE launched INS Shreyas, third unit of the NGOPV class, on Saturday 10 October; 11-ship programme, seven by "
        "Goa Shipyard and four by GRSE", "nat_ngopv_bm"),
   fact("GRSE launches 'Shreyas', third NGOPV in under five months", "nat_ngopv_psu")],
  why="The sources call Shreyas a Next Generation Offshore Patrol Vessel, not one of the other ship types.",
  current=ca("2026-10-10"))

G(T, DEF, "Intermediate",
  "The ₹1,950 crore contract signed by the Ministry of Defence with Bharat Electronics Limited on 31 March 2026 for "
  "two mountain radars for the Indian Air Force covers radars designed by which DRDO laboratory?",
  ["Electronics and Radar Development Establishment", "Defence Electronics Research Laboratory",
   "Centre for Airborne Systems", "Instruments Research and Development Establishment"], "*",
  "Defence contracts: radars",
  "The Ministry of Defence signed a ₹1,950 crore contract with BEL for two mountain radars with associated equipment "
  "for the IAF, under Buy (Indian-IDDM). The radars are designed by DRDO's Electronics and Radar Development "
  "Establishment (ERDE) and made by BEL, to strengthen air defence in mountainous terrain.",
  ["₹1,950 crore, 2 mountain radars, IAF", "Designed by ERDE (DRDO), made by BEL; Buy (Indian-IDDM)"],
  [fact("₹1,950 crore contract with BEL for two mountain radars for the IAF, signed on Tuesday (31 March 2026); designed "
        "by DRDO's Electronics and Radar Development Establishment; Buy (Indian-IDDM)", "nat_rad_dd")],
  why="The source names the Electronics and Radar Development Establishment as the designer; the other labs are not "
      "mentioned.",
  current=ca("2026-03-31"))

# ------------------------------------------------------------------ National CA: Advanced (11)
GS(T, GOV, "Advanced", "the extension of the Jal Jeevan Mission approved by the Union Cabinet in March 2026",
   ["The mission has been extended up to December 2028.",
    "Its total outlay has been raised to ₹8.69 lakh crore.",
    "Central assistance under the extended mission is ₹2.08 lakh crore."],
   [True, True, False],
   "Cabinet decisions: Jal Jeevan Mission",
   "The Cabinet extended the Jal Jeevan Mission to December 2028, shifting its focus from building infrastructure to "
   "service delivery. Total outlay rises to ₹8.69 lakh crore with central assistance of ₹3.59 lakh crore, up from ₹2.08 "
   "lakh crore at launch in 2019-20. A digital framework, Sujalam Bharat, gives each village a service area ID.",
   [fact("JJM extended to December 2028; total outlay ₹8.69 lakh crore; central assistance ₹3.59 lakh crore; Sujalam "
         "Bharat framework (AIR, 10 March 2026)", "nat_jjm_air"),
    fact("Central assistance ₹3.59 lakh crore, up from ₹2.08 lakh crore at launch in 2019-20", "nat_jjm_dd")],
   why="Statement 3 is wrong: ₹2.08 lakh crore was the original central share; it is now ₹3.59 lakh crore.",
   current=ca("2026-03-10", inferred="AIR report published the evening of 10 March 2026 on that day's Cabinet decisions"))

GS(T, GOV, "Advanced", "the Integrated Transport and Logistics Authority (ITLA) approved by the Union Cabinet on 6 "
   "October 2026",
   ["It is to be set up as a Special Purpose Vehicle.",
    "Its National Transport Data Repository will draw on data such as GSTN e-way bills, FASTag and Vahan.",
    "It will carry out technical appraisal of all Central infrastructure projects costing ₹1,000 crore or more."],
   [True, True, False],
   "Cabinet decisions: transport planning",
   "The Cabinet approved ITLA as a Special Purpose Vehicle and national apex institution for integrated transport and "
   "logistics planning. It will prepare a National Transport Master Plan with a horizon of 10 years or more and run a "
   "National Transport Data Repository using GSTN e-way bills, FASTag, Vahan and GPS data. Its technical appraisal and "
   "monitoring covers Central projects of ₹500 crore or more; financial appraisal stays with existing mechanisms.",
   [fact("ITLA approved as an SPV on Tuesday (6 Oct 2026); NTDR to use GSTN e-way bills, FASTag, Vahan, GPS data; "
         "technical appraisal of Central projects costing ₹500 crore or more", "nat_itla_pio"),
    fact("Cabinet approves proposal to set up Integrated Transport and Logistics Authority (October 2026)",
         "nat_itla_ys")],
   why="Statement 3 is wrong: the threshold is ₹500 crore, not ₹1,000 crore.",
   current=ca("2026-10-06"))

GS(T, GOV, "Advanced", "the launch of the NVS-03 navigation satellite in October 2026",
   ["It was launched by GSLV-F18, the 20th flight of the GSLV.",
    "It lifted off from the First Launch Pad at Sriharikota.",
    "The 56-day gap between two successive GSLV missions was the shortest so far."],
   [True, False, True],
   "ISRO missions: NavIC",
   "GSLV-F18, the 20th GSLV flight, lifted off from the Second Launch Pad at Satish Dhawan Space Centre, Sriharikota, "
   "carrying the 2,232 kg NVS-03 into geosynchronous transfer orbit. It is the third second-generation NavIC satellite. "
   "The mission came 56 days after the previous GSLV mission, the shortest such gap so far.",
   [fact("NVS-03 launched 'last night' (AIR, 31 Oct 2026) by GSLV-F18, 20th GSLV flight, from the Second Launch Pad; "
         "~2,232 kg; 56-day turnaround, shortest so far", "nat_nvs_air")],
   why="Statement 2 is wrong: the launch was from the Second Launch Pad.",
   current=ca("2026-10-30", inferred="AIR report of 31 Oct 2026 says the launch took place 'last night'"))

GS(T, GOV, "Advanced", "the CAPEX Support Scheme to Promote Critical Mineral Processing approved by the Union Cabinet "
   "on 4 November 2026",
   ["Its outlay is ₹2,814 crore, of which ₹2,800 crore is capital support.",
    "It offers a 50% capital subsidy on eligible investment.",
    "It will support four plants, two each for lithium and nickel processing."],
   [True, False, True],
   "Cabinet decisions: critical minerals",
   "The ₹2,814 crore scheme (₹2,800 crore capital support, ₹14 crore administrative) runs from 2026-27 to 2030-31 under "
   "the Ministry of Mines. It gives a 30% capital subsidy, capped at ₹500 crore per lithium plant and ₹900 crore per "
   "nickel plant, to four plants (two lithium, two nickel), with beneficiaries chosen through competitive bidding.",
   [fact("Approved 4 November 2026; ₹2,814 crore (₹2,800 crore capital support + ₹14 crore admin); 30% capital "
         "subsidy; four plants, two each for lithium and nickel; Ministry of Mines; FY27-FY31", "nat_cmp_dd")],
   why="Statement 2 is wrong: the capital subsidy is 30%.",
   current=ca("2026-11-04"))

GS(T, GOV, "Advanced", "the three railway multitracking projects worth ₹9,072 crore approved by the Cabinet "
   "Committee on Economic Affairs on 24 February 2026",
   ["They include a third and fourth line between Gondia and Nagpur.",
    "Together they add about 307 km to the rail network across Maharashtra, Madhya Pradesh, Bihar and Jharkhand.",
    "They include the Gamharia-Chandil third and fourth line."],
   [False, True, True],
   "Cabinet decisions: railways",
   "The CCEA approved three projects costing ₹9,072 crore: Gondia-Jabalpur doubling, Punarakh-Kiul third and fourth "
   "line, and Gamharia-Chandil third and fourth line. They add about 307 km across eight districts of Maharashtra, "
   "Madhya Pradesh, Bihar and Jharkhand and are planned under the PM Gati Shakti National Master Plan.",
   [fact("CCEA approved on Tuesday (DD News, 24 Feb 2026): Gondia-Jabalpur doubling, Punarakh-Kiul 3rd/4th line, "
         "Gamharia-Chandil 3rd/4th line; ~307 km; Maharashtra, MP, Bihar, Jharkhand; ₹9,072 crore", "nat_rail_dd")],
   why="Statement 1 is wrong: the Gondia project is a Gondia-Jabalpur doubling, not a Gondia-Nagpur line.",
   current=ca("2026-02-24"))

GS(T, ST, "Advanced", "the State Innovation Mission launched in Tripura on 26 February 2026",
   ["It is described as India's first State-level innovation mission.",
    "It was launched by the Atal Innovation Mission of NITI Aayog as part of AIM 2.0.",
    "It is institutionalised under the Tripura Institution for Transformation (TIFT)."],
   [True, True, True],
   "State initiatives: innovation",
   "The Atal Innovation Mission (NITI Aayog) launched India's first State Innovation Mission in Agartala on 26 February "
   "2026, under AIM 2.0. It is housed in the Tripura Institution for Transformation, with the T-NEST incubation hub "
   "and innovation centres planned in all eight districts. Chief Minister Manik Saha also announced a State AI policy.",
   [fact("26 February 2026, Agartala: AIM (NITI Aayog) launched India's first State Innovation Mission under AIM 2.0; "
         "institutionalised under TIFT; T-NEST hub", "nat_tsim_dd"),
    fact("Tripura to launch India's first state AI policy (report of 26 Feb 2026)", "nat_tsim_itne")],
   why="All three statements match the source.",
   current=ca("2026-02-26"))

GS(T, ST, "Advanced", "the Chhattisgarh Ease of Doing Business Bill, 2026, passed by the State Assembly in July 2026",
   ["It abolishes mandatory annual renewal of licences.",
    "In the first phase it covers 43 services of eight State departments.",
    "The apex body of its three-tier monitoring system is chaired by the Chief Secretary."],
   [True, True, False],
   "States: business reforms",
   "Chhattisgarh became the first State to adopt a risk-based business approval system. The Bill covers 43 services of "
   "eight departments, abolishes mandatory annual licence renewals, allows self-certification for low-risk units and "
   "deemed approval for delayed applications. A council chaired by Chief Minister Vishnu Deo Sai heads the three-tier "
   "system; committees under the Chief Secretary and Collectors work under it.",
   [fact("Passed on Thursday (16 July 2026); 43 services of eight departments; annual licence renewals abolished; "
         "council chaired by CM Vishnu Deo Sai, with Chief Secretary and Collector committees under it", "nat_cg_itv"),
    fact("Chhattisgarh becomes first state with risk-based business approvals", "nat_cg_dc")],
   why="Statement 3 is wrong: the top council is chaired by the Chief Minister; the Chief Secretary heads the "
       "state-level committee below it.",
   current=ca("2026-07-16"))

GS(T, ST, "Advanced", "the semiconductor facility of Sahasra Semiconductors at Bhiwadi, Rajasthan, inaugurated in May "
   "2026",
   ["It is described as India's first SME-led unit to begin commercial production of semiconductor chips.",
    "It was inaugurated in person by Prime Minister Narendra Modi.",
    "It was set up under MeitY's SPECS scheme."],
   [True, False, True],
   "States: semiconductors",
   "Union Electronics and IT Minister Ashwini Vaishnaw virtually inaugurated Sahasra Semiconductors' ATMP/OSAT unit, "
   "Rajasthan's first chip packaging facility, and the ELCINA Electronics Manufacturing Cluster at Bhiwadi on 15 May "
   "2026. The over ₹150 crore unit, set up under MeitY's SPECS scheme, is India's first SME-led unit to start "
   "commercial chip production and exports over 60% of output.",
   [fact("Inaugurated virtually by Ashwini Vaishnaw on Friday 15 May 2026; Sahasra unit is India's first SME-led unit to "
         "begin commercial semiconductor chip production; over ₹150 crore under MeitY SPECS scheme", "nat_bhi_dd")],
   why="Statement 2 is wrong: Union Minister Ashwini Vaishnaw inaugurated it virtually.",
   current=ca("2026-05-15"))

GS(T, DEF, "Advanced", "the Lokayan 26 expedition of the Indian Navy's sail training ship INS Sudarshini",
   ["The ship was flagged off from Mumbai on 20 January 2026.",
    "It covered more than 22,000 nautical miles with 17 port calls in 11 countries.",
    "The flag-in ceremony on its return was presided over by the Flag Officer Commanding-in-Chief, Southern Naval "
    "Command."],
   [False, True, True],
   "Navy: sail training expeditions",
   "INS Sudarshini left Kochi on 20 January 2026 and returned to Kochi on 2 November 2026 after the ten-month Lokayan 26 "
   "voyage of over 22,000 nautical miles, with 17 port calls in 11 countries across four continents, including SAIL 250 "
   "and the International Naval Review in the US. Vice Admiral Sameer Saxena, FOC-in-C Southern Naval Command, "
   "presided over the flag-in.",
   [fact("Flagged off from Kochi on 20 January 2026; returned to Kochi on 2 November 2026; over 22,000 nm; 17 port calls "
         "in 11 countries; flag-in presided by VAdm Sameer Saxena, FOC-in-C, Southern Naval Command", "nat_sud_dd")],
   why="Statement 1 is wrong: the voyage began (and ended) at Kochi.",
   current=ca("2026-11-02"))

GS(T, DEF, "Advanced", "the launch of 'Surya', the first indigenous Fleet Support Ship, in October 2026",
   ["It was launched at Hindustan Shipyard Limited, Visakhapatnam.",
    "It is a 43,500-tonne vessel.",
    "The keel of the fifth Fleet Support Ship was laid on the same day."],
   [True, True, True],
   "Navy: fleet support ships",
   "Defence Minister Rajnath Singh launched Surya, the first indigenous 43,500-tonne Fleet Support Ship, at Hindustan "
   "Shipyard Limited, Visakhapatnam, on 6 October 2026. On the same day he laid the keel of FSS-5 and opened the "
   "upgraded Slipway-4 and a 300-tonne Goliath crane. Launch honours were performed by Laila Swaminathan, President of "
   "the Navy Wives Wellness Association.",
   [fact("6 October 2026: Rajnath Singh launched first indigenous FSS Surya at HSL Visakhapatnam; 43,500 tonnes; keel of "
         "FSS-5 laid; Slipway-4 and 300-tonne Goliath crane inaugurated", "nat_fss_dc")],
   why="All three statements match the source.",
   current=ca("2026-10-06"))

GS(T, DEF, "Advanced", "the Defence Acquisition Council approvals worth about ₹52,000 crore announced on 3 July 2026",
   ["Fixed-Wing High Altitude Pseudo Satellites were approved for the Indian Navy.",
    "The Indian Army's approvals included the AKASH TARANG anti-drone electronic warfare system.",
    "The Indian Navy's approvals included Multi Influence Ground Mines."],
   [False, True, True],
   "Defence procurement: DAC",
   "The DAC chaired by Rajnath Singh accorded AoN to proposals worth about ₹52,000 crore. Army items included the "
   "AKASH TARANG anti-drone EW system, MPATGM, MRSAM, V-SHORADS and jet-based kamikaze drones; Navy items included "
   "Multi Influence Ground Mines and a Naval Shipborne UAS; the Air Force got Fixed-Wing High Altitude Pseudo "
   "Satellites (FW-HAPS).",
   [fact("Announced Friday (3 July 2026): ~₹52,000 crore AoN; Army: AKASH TARANG anti-drone EW system etc.; Navy: Multi "
         "Influence Ground Mine, NSUAS; Air Force: FW-HAPS", "nat_dac2_tt")],
   why="Statement 1 is wrong: FW-HAPS were approved for the Indian Air Force.",
   current=ca("2026-07-03"))

# ###################################################################### part: stat (static + reports + business)
# ###################################################################### part: stat (static + reports + business)
U.update({
    # ---- Static Awareness
    "stat_abuja_emb": ("https://nigerianembmexico.org/tourism", OPENED),
    "stat_abuja_wiki": ("https://en.wikipedia.org/wiki/Abuja", SEARCH),
    "stat_nrb_site": ("https://www.nrb.org.np/", SEARCH),
    "stat_nrb_act": ("https://www.nrb.org.np/contents/uploads/2020/01/nepal_rastra_bank_act_2002_english.pdf", SEARCH),
    "stat_bot_hist": ("https://www.bot.or.th/en/about-us/history.html", OPENED),
    "stat_ukai_wrd": ("https://guj-nwrws.gujarat.gov.in/showpage.aspx?contentid=1601&lang=english", OPENED),
    "stat_ukai_surat": ("https://surat.nic.in/places-of-interest/", OPENED),
    "stat_dachi_sxr": ("https://srinagar.nic.in/tourist-place/dachigam-national-park/", OPENED),
    "stat_dachi_ot": ("https://outlooktraveller.com/experiences/nature/home-to-the-hangul-about-srinagars-dachigam-"
                      "national-park", SEARCH),
    "stat_simil_org": ("https://www.similipal.org/", OPENED),
    "stat_odisha_gov": ("https://odisha.gov.in/odisha-profile/about-odisha", OPENED),
    "stat_odisha_wiki": ("https://en.wikipedia.org/wiki/Odisha", OPENED),
    "stat_mp_gov": ("https://mp.gov.in/history", OPENED),
    "stat_assam_gov": ("https://assam.gov.in/about-us/394", OPENED),
    # ---- Important Reports and Indexes
    "stat_epi_scroll": ("https://scroll.in/latest/1094224/scroll_in", OPENED),
    "stat_epi_dte": ("https://www.downtoearth.org.in/environment/wake-up-call-say-experts-as-india-gets-second-lowest-"
                     "global-ranking-on-yales-environment-performance-index-also-raise-questions-on-methodology", OPENED),
    "stat_epi_pr": ("https://epi.yale.edu/downloads/epi2026pressrelease2026-07-09.pdf", SEARCH),
    "stat_nri_trib": ("https://www.tribuneindia.com/news/business/india-climbs-four-spots-to-45th-rank-in-network-"
                      "readiness-index-2025/", OPENED),
    "stat_nri_ians": ("https://ianslive.in/india-leads-in-several-indicators-in-global-network-readiness-index-improves-"
                      "its-position--20260209162837", SEARCH),
    "stat_live_bt": ("https://www.businesstoday.in/latest/trends/story/planning-to-move-abroad-these-are-the-worlds-10-"
                     "most-liveable-cities-in-2026-541841-2026-07-08", OPENED),
    "stat_gii_in": ("https://www.wipo.int/edocs/gii-ranking/2026/in.pdf", OPENED),
    "stat_gii_pr": ("https://www.wipo.int/pressroom/en/articles/2026/article_0014.html", SEARCH),
    # ---- Business and Corporate News
    "stat_avid_nvs": ("https://www.novartis.com/news/media-releases/novartis-successfully-completes-acquisition-avidity-"
                      "biosciences-strengthening-late-stage-neuroscience-pipeline-and-advancing-xrna-strategy", OPENED),
    "stat_avid_apr": ("https://www.americanpharmaceuticalreview.com/1315-News/624352-Novartis-Completes-Acquisition-of-"
                      "Avidity-Biosciences/", SEARCH),
})

T = "Static Awareness"
CAP, PARK, STATE = "Capitals and currencies", "National parks and dams", "Indian states facts"

# ------------------------------------------------------------------ Static: Intermediate (8)
G(T, CAP, "Intermediate",
  "Abuja officially became the capital of Nigeria on 12 December 1991. Which city did it replace as the capital?",
  ["Lagos", "Kano", "Ibadan", "Port Harcourt"], "*",
  "World capitals: planned capitals",
  "Abuja officially became Nigeria's capital on 12 December 1991, replacing Lagos. Lagos remains the country's "
  "commercial capital and its most populous city.",
  ["Nigeria's capital since 12 Dec 1991: Abuja", "Earlier capital: Lagos (still the commercial capital)"],
  [fact("Abuja officially became Nigeria's capital on 12 December 1991, replacing Lagos, its commercial capital and "
        "most populous city", "stat_abuja_emb"),
   fact("Abuja replaced Lagos as the capital of Nigeria on 12 December 1991", "stat_abuja_wiki")],
  why="The sources say Abuja replaced Lagos; Kano, Ibadan and Port Harcourt were not the earlier capital.")

G(T, CAP, "Intermediate",
  "Nepal Rastra Bank, which has the monopoly over issuing banknotes and coins of the Nepalese rupee, was established "
  "in which year?",
  ["1956", "1949", "1962", "1971"], "*",
  "Central banks and currencies: Nepal",
  "Nepal Rastra Bank, the central bank of Nepal, was established in 1956 under the Nepal Rastra Bank Act, 1955. Under "
  "the Nepal Rastra Bank Act, 2002 it has the monopoly over the issue of banknotes and coins in Nepal.",
  ["Nepal Rastra Bank: est. 1956 (Act of 1955)", "Sole issuer of Nepalese notes and coins (NRB Act, 2002)"],
  [fact("NRB, the central bank of Nepal, was established in 1956 under the Nepal Rastra Bank Act 1955", "stat_nrb_site"),
   fact("Nepal Rastra Bank Act, 2002 gives the bank the monopoly over the issue of banknotes and coins in Nepal",
        "stat_nrb_act")],
  why="The bank's own site gives 1956 as the year of establishment; the other years are not.")

G(T, PARK, "Intermediate",
  "The Ukai Dam in Songadh taluka of Surat district, Gujarat, a multipurpose project completed in 1972, is built on "
  "which river?",
  ["Tapi", "Narmada", "Mahi", "Sabarmati"], "*",
  "Dams of India: Gujarat",
  "The Ukai project of the Gujarat Water Resources Department is a multipurpose dam on the Tapi river at village Ukai, "
  "Songadh taluka, Surat district. Work began in 1964 and was completed in 1972; the dam is about 80.8 m high. It "
  "is used for both hydroelectric power and water storage.",
  ["Ukai Dam: Tapi river, Surat district", "Built 1964-1972; multipurpose"],
  [fact("Ukai: river Tapi; village Ukai, Songadh taluka, Surat district; started 1964, completed 1972; multipurpose; "
        "height 80.772 m", "stat_ukai_wrd"),
   fact("Ukai Dam, reached from Surat, serves both hydroelectric power generation and water storage",
        "stat_ukai_surat")],
  why="The State water resources department lists the Tapi as Ukai's river; the Narmada, Mahi and Sabarmati are not.")

G(T, PARK, "Intermediate",
  "Dachigam National Park, about 22 km from Srinagar, originally set up to secure clean drinking water for the city "
  "and declared a national park in 1981, is best known as the home of which animal?",
  ["Hangul (Kashmir stag)", "Barasingha (swamp deer)", "Sangai (brow-antlered deer)", "Nilgiri tahr"], "*",
  "National parks: Jammu and Kashmir",
  "Dachigam National Park lies about 22 km from Srinagar and covers about 141 sq km. It was first created to ensure "
  "clean drinking water for Srinagar and was declared a national park in 1981. It is the home of the hangul, or "
  "Kashmir stag.",
  ["Dachigam: 22 km from Srinagar, 141 sq km", "National park since 1981", "Home of the hangul (Kashmir stag)"],
  [fact("Dachigam National Park: 22 km from Srinagar; declared a national park in 1981; home of the hangul, or Kashmir "
        "stag; 141 sq km; initially established to ensure clean drinking water for Srinagar", "stat_dachi_sxr"),
   fact("Srinagar's Dachigam National Park is home to the endangered hangul", "stat_dachi_ot")],
  why="The district administration names the hangul as Dachigam's signature animal; the other deer and the tahr are "
      "not named.")

G(T, PARK, "Intermediate",
  "Similipal, a tiger reserve that is also part of UNESCO's network of biosphere reserves, is located in which "
  "district of Odisha?",
  ["Mayurbhanj", "Kendrapara", "Koraput", "Angul"], "*",
  "Protected areas: Odisha",
  "Similipal, described as the jewel of Mayurbhanj, lies in Mayurbhanj district of Odisha, with its office at "
  "Baripada. It is listed as a UNESCO biosphere reserve.",
  ["Similipal: Mayurbhanj district (Baripada), Odisha", "UNESCO biosphere reserve"],
  [fact("Similipal is called the jewel of Mayurbhanj; address Baripada, Mayurbhanj, Odisha; labelled a UNESCO "
        "biosphere", "stat_simil_org")],
  why="The reserve's site places Similipal in Mayurbhanj district; Kendrapara, Koraput and Angul are not named.")

G(T, STATE, "Intermediate",
  "In which year was Odisha (then Orissa) formed as a separate province, out of parts of the Bihar and Orissa "
  "Province and the Madras Presidency?",
  ["1936", "1912", "1947", "1950"], "*",
  "Formation of Indian states: Odisha",
  "Odisha was formed as a separate province in 1936 from parts of the Bihar and Orissa Province and the Madras "
  "Presidency (and the Central Provinces). The province came into existence on 1 April 1936, which is celebrated as "
  "Utkala Divas (Odisha Day).",
  ["Separate province: 1 April 1936", "Formed from Odia-speaking areas of Bihar-Orissa, Madras and the Central "
   "Provinces", "1 April: Utkala Divas"],
  [fact("In 1936 Odisha was formed as a separate province from parts of the Bihar, Odisha and Madras provinces",
        "stat_odisha_gov"),
   fact("On 1 April 1936 Bihar and Orissa were split into separate provinces; Odia-speaking districts of Bihar and "
        "Orissa, Madras Presidency and Central Provinces; Utkala Divas celebrated on 1 April", "stat_odisha_wiki")],
  why="The State's own profile gives 1936; the other years are not the year of its formation as a province.")

G(T, STATE, "Intermediate",
  "When Madhya Pradesh was first formed in 1950 from the former Central Provinces and Berar, the Makrai princely "
  "state and Chhattisgarh, which city was made its capital?",
  ["Nagpur", "Bhopal", "Jabalpur", "Gwalior"], "*",
  "Formation of Indian states: Madhya Pradesh",
  "According to the Madhya Pradesh government, the State was formed in 1950 by combining the former British Central "
  "Provinces and Berar, the Makrai princely state and Chhattisgarh, with Nagpur as its capital. In 1956 Madhya "
  "Bharat, Vindhya Pradesh and Bhopal were merged into it and Bhopal became the new capital. In November 2000 the "
  "south-eastern part became Chhattisgarh.",
  ["1950: Madhya Pradesh formed, capital Nagpur", "1956: reorganised, capital Bhopal", "2000: Chhattisgarh carved out"],
  [fact("1950: Central Provinces and Berar, Makrai princely state and Chhattisgarh combined to form Madhya Pradesh; "
        "Nagpur was made the capital; 1956: Madhya Bharat, Vindhya Pradesh and Bhopal merged and Bhopal became the "
        "new capital", "stat_mp_gov")],
  why="The State's history page names Nagpur as the first capital; Bhopal became the capital only in 1956.")

G(T, STATE, "Intermediate",
  "Following the Burmese invasion that ended Ahom rule, Assam was annexed by the British East India Company under "
  "which treaty of 1826?",
  ["Treaty of Yandaboo", "Treaty of Sugauli", "Treaty of Salbai", "Treaty of Amritsar"], "*",
  "History of Indian states: Assam",
  "The Assam government's history page notes that the Burmese invasion ended Ahom rule, and Assam was then annexed "
  "by the British East India Company following the Treaty of Yandaboo in 1826. Later, Meghalaya, Nagaland, "
  "Arunachal Pradesh and Mizoram became separate states formed from territory within Assam's borders.",
  ["Burmese invasion ends Ahom rule", "Treaty of Yandaboo, 1826: British annexation of Assam"],
  [fact("Annexation by the British East India Company following the Treaty of Yandaboo in 1826, after the Burmese "
        "invasion ended Ahom rule; Meghalaya, Nagaland, Arunachal Pradesh and Mizoram later became separate states",
        "stat_assam_gov")],
  why="The Assam government names the Treaty of Yandaboo (1826); the other treaties are not linked to Assam there.")

# ------------------------------------------------------------------ Static: Advanced (1)
GS(T, CAP, "Advanced", "the history of the Bank of Thailand, the central bank of Thailand",
   ["Its inauguration ceremonies were held on 10 December 1942, which was Constitution Day.",
    "Its predecessor, the Thai National Banking Bureau, started operations in 1940.",
    "It began operations in a newly built headquarters of its own on its first working day."],
   [True, True, False],
   "Central banks: Bank of Thailand",
   "The Thai National Banking Bureau started operations on 13 May 1940. After the Japanese invasion, the Bank of "
   "Thailand Act was issued on 16 April 1942, converting the Bureau into a central bank. Inauguration ceremonies were "
   "held on 10 December 1942, Constitution Day, with Prince Viwat as the first Governor. The bank started operations "
   "on 11 December 1942 in the former offices of the Hongkong and Shanghai Banking Corporation on Siphraya Road, not "
   "in a new building of its own.",
   [fact("Thai National Banking Bureau started operations on 13 May 1940; Act issued 16 April 1942; inauguration "
         "ceremonies on 10 December 1942, Constitution Day; Prince Viwat first Governor; operations began 11 December "
         "1942 at the former HSBC offices on Siphraya Road", "stat_bot_hist")],
   why="Statement 3 is wrong: the bank began work in the former HSBC offices on Siphraya Road.")

# ------------------------------------------------------------------ Reports and Indexes
T = "Important Reports and Indexes"
PUB, RANK = "Publishing body", "India's rank"

G(T, RANK, "Intermediate",
  "In the Environmental Performance Index (EPI) 2026, released in July 2026 and topped by Estonia, what was India's "
  "rank among 177 countries?",
  ["176th", "175th", "177th", "170th"], "*",
  "Environmental Performance Index 2026",
  "The EPI, compiled every two years by researchers at Yale and Columbia universities, ranked 177 countries in 2026. "
  "Estonia topped it with a score of 74.79. India ranked 176th with a score of 22.46, second from the bottom, just "
  "above Laos.",
  ["EPI 2026: 177 countries; Estonia 1st (74.79)", "India 176th (22.46); Laos 177th"],
  [fact("India ranked 176th of 177 countries in EPI 2026 with a score of 22.4; Estonia highest with 74.79; index "
        "compiled every two years by Yale and Columbia researchers", "stat_epi_scroll"),
   fact("India 176th of 177 with 22.46, second lowest after Laos; Estonia top with 74.79", "stat_epi_dte"),
   fact("EPI 2026 press release dated 9 July 2026", "stat_epi_pr")],
  why="The sources put India at 176th; 177th was Laos.",
  current=ca("2026-07-09"))

G(T, RANK, "Intermediate",
  "In the Network Readiness Index 2025 of the Portulans Institute, released in February 2026, what was India's rank "
  "among 127 economies?",
  ["45th", "49th", "40th", "52nd"], "*",
  "Network Readiness Index 2025",
  "The Network Readiness Index 2025, published by the Washington DC-based Portulans Institute and released on 4 "
  "February 2026, ranked India 45th among 127 economies, four places higher than in the previous edition.",
  ["NRI 2025: 127 economies", "India 45th, up four places (from 49th)"],
  [fact("India climbed four spots to 45th in the Network Readiness Index 2025; 127 economies; Portulans Institute, "
        "Washington DC; report released on 4 February 2026", "stat_nri_trib"),
   fact("India leads in several indicators in the Network Readiness Index and improves its position", "stat_nri_ians")],
  why="The sources give 45th; 49th was India's earlier position.",
  current=ca("2026-02-04"))

G(T, PUB, "Intermediate",
  "The Global Liveability Index 2026, which ranked 173 cities and placed Copenhagen first, Vienna second and "
  "Melbourne third, is published by which organisation?",
  ["Economist Intelligence Unit (EIU)", "Mercer", "UN-Habitat", "World Economic Forum"], "*",
  "Global Liveability Index",
  "The Global Liveability Index is published by the Economist Intelligence Unit (EIU). Its 2026 edition, released in "
  "July 2026, covered 173 cities, with Copenhagen ranked first, followed by Vienna and Melbourne.",
  ["Publisher: EIU", "2026: 173 cities; Copenhagen, Vienna, Melbourne top three"],
  [fact("The EIU's Global Liveability Index 2026 was released on a Tuesday (article of Wednesday 8 July 2026); 173 "
        "cities; Copenhagen 1st, Vienna 2nd, Melbourne 3rd", "stat_live_bt")],
  why="The sources name the EIU as the publisher; Mercer, UN-Habitat and the WEF are not.",
  current=ca("2026-07-07", inferred="Business Today article of Wed 8 July 2026 says the index came out on Tuesday"))

GS(T, RANK, "Advanced", "India in the Global Innovation Index (GII) 2026, released by WIPO on 29 September 2026",
   ["India ranked 38th among 139 economies, the same position as in 2025.",
    "India performed better in innovation inputs than in innovation outputs.",
    "India ranked first among the 36 lower-middle-income economies."],
   [True, False, True],
   "Global Innovation Index 2026",
   "WIPO's India profile for the GII 2026 says India ranks 38th among the 139 economies covered, unchanged from 2025. "
   "It ranks 49th in innovation inputs and 25th in innovation outputs, so it performs better in outputs than inputs. "
   "India ranks first among the 36 lower-middle-income economies and first among the 11 economies of Central and "
   "Southern Asia, and has 4 clusters among the world's top innovation clusters.",
   [fact("India ranks 38th among 139 economies in GII 2026 (38th in 2025 too); 49th in innovation inputs, 25th in "
         "outputs; performs better in outputs than inputs; 1st among 36 lower-middle-income economies",
         "stat_gii_in"),
    fact("WIPO press release dated Geneva, 29 September 2026 announces the GII 2026 results", "stat_gii_pr")],
   why="Statement 2 is wrong: India ranks 25th in outputs but 49th in inputs.",
   current=ca("2026-09-29"))

# ------------------------------------------------------------------ Business and Corporate News
T = "Business and Corporate News"
G(T, "Mergers and acquisitions", "Intermediate",
  "Novartis completed its acquisition of which US biotech company on 27 February 2026, paying USD 72 per share in "
  "cash (about USD 12 billion) to gain an antibody oligonucleotide conjugate (AOC) platform for neuromuscular "
  "diseases?",
  ["Avidity Biosciences", "Alnylam Pharmaceuticals", "Sarepta Therapeutics", "Ionis Pharmaceuticals"], "*",
  "Pharma M&A: Novartis",
  "Novartis completed its acquisition of Avidity Biosciences on 27 February 2026. Avidity shareholders received USD "
  "72 per share in cash, valuing the company at about USD 12 billion (enterprise value about USD 11 billion). The "
  "deal, announced on 26 October 2025, brings a muscle-directed Antibody Oligonucleotide Conjugates (AOC) platform "
  "and three late-stage programmes for genetic neuromuscular diseases.",
  ["Announced 26 Oct 2025; completed 27 Feb 2026", "USD 72/share; about USD 12 billion", "AOC platform; neuromuscular"],
  [fact("Novartis completed the acquisition of Avidity Biosciences on 27 February 2026; USD 72 per share in cash; about "
        "USD 12 billion fully diluted; AOC platform; three late-stage programmes in neuromuscular diseases; announced "
        "26 October 2025", "stat_avid_nvs"),
   fact("Novartis completes acquisition of Avidity Biosciences", "stat_avid_apr")],
  why="The Novartis release names Avidity Biosciences; the other biotech companies are not part of this deal.",
  current=ca("2026-02-27"))

# ###################################################################### part: intl (international + summits)
# ###################################################################### part: intl (International CA + Summits)
U.update({
    # ---- International Current Affairs
    "intl_soml_aj": ("https://aljazeera.com/news/2025/12/26/israel-becomes-first-country-to-recognise-somaliland", OPENED),
    "intl_soml_an": ("https://www.africanews.com/2025/12/26/israel-becomes-first-country-to-recognize-somaliland/",
                     SEARCH),
    "intl_liech_dd": ("https://ddindia.co.in/2026/10/hereditary-prince-alois-of-liechtenstein-arrives-in-mumbai-on-"
                      "state-visit-to-india/", OPENED),
    "intl_liech_air": ("https://newsonair.gov.in/pm-modi-to-hold-talks-with-acting-head-of-state-of-principality-of-"
                       "liechtenstein-hereditary-prince-alois-in-new-delhi-today/", OPENED),
    "intl_merc_mp": ("https://en.mercopress.com/2026/01/17/mercosur-and-eu-sign-historic-trade-agreement-in-asuncion-"
                     "after-26-years-of-negotiations", OPENED),
    "intl_merc_en": ("https://www.euronews.com/2026/01/17/eu-and-mercosur-sign-major-trade-deal-in-asuncion", OPENED),
    "intl_has_aj": ("https://www.aljazeera.com/news/2025/11/17/sheikh-hasina-convicted-of-crimes-against-humanity-what-"
                    "we-know", OPENED),
    "intl_has_occrp": ("https://www.occrp.org/en/news/bangladesh-tribunal-sentences-ex-pm-hasina-to-death-in-absentia-"
                       "for-2024-crackdown", SEARCH),
    "intl_vpsl_trib": ("https://www.tribuneindia.com/news/world/vice-president-cp-radhakrishnans-historic-visit-to-sri-"
                       "lanka-reinforces-centuries-old-ties/", OPENED),
    "intl_vpsl_nf": ("https://english.newsfirst.lk/2026/04/17/indian-vp-to-make-historic-first-bilateral-visit-to-sri-"
                     "lanka", SEARCH),
    "intl_dk_ap": ("https://www.click2houston.com/news/2026/03/24/denmark-votes-in-an-early-election-that-follows-a-"
                   "crisis-over-us-designs-on-greenland/", OPENED),
    "intl_dk_bt": ("https://www.brusselstimes.com/2043112/danish-pm-ready-to-take-on-role-again-despite-disappointing-"
                   "election-result", OPENED),
    "intl_ecu_aj": ("https://www.aljazeera.com/news/2025/11/17/no-vote-leads-in-ecuador-referendum-on-hosting-foreign-"
                    "military-bases", OPENED),
    "intl_ecu_npr": ("https://www.wamc.org/2025-11-17/ecuador-rejects-u-s-military-bases-in-major-defeat-for-president-"
                     "noboa", SEARCH),
    "intl_tusk_nk": ("https://www.newkerala.com/news/a/pm-modi-polish-pm-donald-tusk-hold-delegation-level-595.htm",
                     OPENED),
    "intl_tusk_org": ("https://organiser.org/2026/10/22/419306/world/india-poland-ties-gain-momentum-trade-tech-defence-"
                      "counter-terrorism-more-highlights-of-pm-modi-pm-tusk-talks/", OPENED),
    "intl_tusk_ol": ("https://www.outlookindia.com/international/donald-tusk-india-visit-october-21-defence-trade-space",
                     OPENED),
    # ---- Summits and Conferences
    "sum_gcc_air": ("https://www.newsonair.gov.in/gcc-summit-concludes-with-sakhir-declaration-calling-for-greater-unity",
                    OPENED),
    "sum_gcc_kt": ("https://www.khaleejtimes.com/world/gulf/46th-gcc-summit-bahrain-sakhir-declation", OPENED),
    "sum_pif_pina": ("https://pina.com.fj/2026/03/05/palau-steps-up-preparations-for-55th-pacific-leaders-meeting/",
                     OPENED),
    "sum_pif_ib": ("https://islandsbusiness.com/?p=51756", SEARCH),
    "sum_epc_eu4": ("https://eu4armenia.eu/european-political-community-in-yerevan-this-summit-will-forever-be-"
                    "remembered-as-a-summit-of-peace-in-the-caucasus-costa-says/", OPENED),
    "sum_epc_pan": ("https://panarmenian.net/eng/news/332045/", SEARCH),
    "sum_wtdc_az": ("https://azertag.az/en/xeber/wtdc_25_itu_member_states_define_roadmap_for_digital_opportunities-"
                    "3887939", OPENED),
    "sum_wtdc_min": ("https://mincom.gov.az/en/media-en/news/wtdc-25-in-baku-sets-attendance-record", SEARCH),
    "sum_ioc_iora": ("https://iora.int/indian-ocean-conference-2026-collective-stewardship-indian-ocean-governance",
                     OPENED),
    "sum_ioc_ht": ("https://thehimalayantimes.com/nepal/foreign-minister-khanal-to-attend-9th-indian-ocean-conference-"
                   "in-mauritius", OPENED),
    "sum_aueu_eeas": ("https://www.eeas.europa.eu/delegations/african-union-au/seventh-african-union-european-union-"
                      "summit_en?etrans=fr", OPENED),
    "sum_aueu_mia": ("https://mia.mk/story/euau-summit-kicks-off-in-luanda-as-continents-eye-closer-cooperation",
                     SEARCH),
    "sum_franc_lpj": ("https://lepetitjournal.com/cambodge/le-20e-sommet-de-la-francophonie-est-transfere-de-siem-reap-"
                      "phnom-penh-435509", OPENED),
    "sum_franc_cm": ("https://www.cambodgemag.com/en/post/cambodia-20th-francophonie-summit-relocated-to-phnom-penh",
                     OPENED),
    "sum_ipbes_jncc": ("https://hub.jncc.gov.uk/our-work/ipbes-12/", OPENED),
    "sum_ipbes_ispra": ("https://www.isprambiente.gov.it/en/news/ipbes-publishes-a-report-on-the-links-between-business-"
                        "and-biodiversity", OPENED),
    "sum_npt_vn": ("https://vietnamnews.vn/politics-laws/1781999/11th-npt-review-conference-under-viet-nam-s-presidency-"
                   "concludes.html", OPENED),
    "sum_npt_at": ("https://astanatimes.com/?p=115530", OPENED),
    "sum_cms_dte": ("https://www.downtoearth.org.in/wildlife-biodiversity/cms-cop15-ends-in-brazil-with-40-new-species-"
                    "being-accorded-protection", OPENED),
    "sum_cms_enb": ("https://enb.iisd.org/es/conference-parties-convention-migratory-species-wild-animals-cms-cop15-"
                    "summary", SEARCH),
    "sum_unea_aa": ("https://allafrica.com/stories/202512090022.html", OPENED),
    "sum_unea_unep": ("https://www.unep.org/news-and-stories/story/unea-7-charts-path-toward-resilient-planet", SEARCH),
    "sum_tm_air1": ("https://www.newsonair.gov.in/second-who-global-summit-on-traditional-medicine-commences-with-focus-"
                    "on-science-and-tradition", OPENED),
    "sum_tm_air2": ("https://www.newsonair.gov.in/second-who-global-summit-on-traditional-medicine-begins-in-new-delhi",
                    OPENED),
    "sum_tm_week": ("https://www.theweek.in/wire-updates/national/2025/12/17/del103-ayush-who-summit.html", SEARCH),
    "sum_wha_who": ("https://www.who.int/news/item/18-05-2026-world-health-assembly-opens-in-geneva--switzerland",
                    OPENED),
    "sum_wha_dt": ("https://dominicantoday.com/victor-atallah-officially-installed-as-president-of-the-world-health-"
                   "assembly/", OPENED),
    "sum_paris_ki": ("https://kyivindependent.com/zelensky-uk-france-sign-declaration-on-multinational-force-deployment-"
                     "in-ukraine-post-war", OPENED),
    "sum_paris_osw": ("https://www.osw.waw.pl/en/publikacje/analyses/2026-01-08/paris-declaration-a-tool-to-influence-"
                      "us-policy", SEARCH),
})

T = "International Current Affairs"
BIL, GEV = "Bilateral relations", "Global events"

# ------------------------------------------------------------------ International CA: Basic (4)
G(T, GEV, "Basic",
  "On 26 December 2025, which country became the first UN member state to formally recognise Somaliland, the region "
  "that declared independence from Somalia in 1991?",
  ["Israel", "United States", "Ethiopia", "United Arab Emirates"], "*",
  "Recognition of Somaliland",
  "On 26 December 2025, Israel and Somaliland signed a joint declaration establishing full diplomatic relations, making "
  "Israel the first country to formally recognise Somaliland. Somaliland, led by President Abdirahman Mohamed Abdullahi "
  "(Cirro), had declared independence from Somalia in 1991 but had not been recognised by any UN member state. Somalia "
  "called the move an attack on its sovereignty, and Egypt also rejected it.",
  ["Somaliland: declared independence from Somalia in 1991", "26 Dec 2025: Israel becomes first to recognise it"],
  [fact("Israel and Somaliland signed a joint declaration on 26 December 2025 establishing full diplomatic ties; "
        "Somaliland declared independence in 1991 and no UN member state had recognised it until Israel; Somalia called "
        "it an attack on its sovereignty; the US had not changed its position", "intl_soml_aj"),
   fact("Israel becomes first country to recognize Somaliland (26 December 2025)", "intl_soml_an")],
  why="The sources name Israel; they say the United States had not changed its position, and the other countries are "
      "not named as recognising Somaliland.",
  current=ca("2025-12-26"))

G(T, BIL, "Basic",
  "Hereditary Prince Alois, who arrived in Mumbai on 25 October 2026 for a four-day State visit to India and held talks "
  "with Prime Minister Narendra Modi in New Delhi, is the acting head of state of which country?",
  ["Liechtenstein", "Luxembourg", "Monaco", "Andorra"], "*",
  "Bilateral visits to India",
  "Hereditary Prince Alois, Acting Head of State of the Principality of Liechtenstein, made a State visit to India from "
  "25 to 28 October 2026, accompanied by Hereditary Princess Sophie and official and business delegations. He began in "
  "Mumbai and held talks with Prime Minister Modi in New Delhi on 27 October; the two sides welcomed the momentum from "
  "the India-EFTA Trade and Economic Partnership Agreement (TEPA).",
  ["Prince Alois = acting head of state, Liechtenstein", "State visit 25-28 Oct 2026; talks with PM on 27 Oct",
   "Context: India-EFTA TEPA"],
  [fact("Hereditary Prince Alois, Acting Head of State of the Principality of Liechtenstein, arrived in Mumbai on 25 "
        "October for a four-day State visit (to 28 October) with Hereditary Princess Sophie; visit builds on India-EFTA "
        "TEPA", "intl_liech_dd"),
   fact("PM Modi held talks with Hereditary Prince Alois of Liechtenstein in New Delhi on 27 October 2026; leaders "
        "welcomed the momentum of the India-EFTA TEPA", "intl_liech_air")],
  why="The sources identify Prince Alois as the acting head of state of Liechtenstein; the other principalities and "
      "the Grand Duchy are not involved.",
  current=ca("2026-10-25"))

G(T, GEV, "Basic",
  "After more than 25 years of negotiations, the European Union and Mercosur formally signed their trade agreement on "
  "17 January 2026 in which city?",
  ["Asunción", "Montevideo", "Buenos Aires", "Brasília"], "*",
  "EU-Mercosur trade agreement",
  "The EU and the Mercosur bloc formally signed their long-negotiated association and free trade agreement on 17 "
  "January 2026 in Asunción, Paraguay, the city where Mercosur's founding treaty was signed in 1991. European Council "
  "President António Costa and European Commission President Ursula von der Leyen attended; Brazil's President Lula did "
  "not, sending his foreign minister. The deal still needs approval by the European Parliament and Mercosur "
  "parliaments before it can enter into force.",
  ["Signed 17 Jan 2026, Asunción (Paraguay)", "Mercosur founding treaty also signed in Asunción (1991)",
   "Needs ratification before entry into force"],
  [fact("Mercosur and the EU to sign the agreement on 17 January 2026 in Asunción, at the Gran Teatro José Asunción "
        "Flores, after nearly 26 years; Mercosur's founding treaty was signed there in 1991; Lula absent; approval by "
        "European Parliament and Mercosur parliaments still required", "intl_merc_mp"),
   fact("EU and Mercosur signed the trade deal in Asunción on Saturday 17 January 2026 after more than 25 years of "
        "negotiations; Costa and von der Leyen attended", "intl_merc_en")],
  why="The sources place the signing in Asunción, Paraguay; Montevideo, Buenos Aires and Brasília did not host it.",
  current=ca("2026-01-17"))

G(T, GEV, "Basic",
  "On 17 November 2025, former Bangladesh Prime Minister Sheikh Hasina was sentenced to death in absentia for crimes "
  "against humanity linked to the crackdown on the 2024 student-led uprising. Which body delivered the verdict?",
  ["International Crimes Tribunal-1, Dhaka", "Appellate Division of the Supreme Court of Bangladesh",
   "International Criminal Court, The Hague", "Special Judge's Court under the Anti-Corruption Commission"], "*",
  "Bangladesh: verdict against Sheikh Hasina",
  "The International Crimes Tribunal-1 (ICT-1) in Dhaka, a special tribunal, found Sheikh Hasina guilty of crimes "
  "against humanity over the 2024 crackdown and sentenced her to death in absentia on 17 November 2025. Former Home "
  "Minister Asaduzzaman Khan was also sentenced to death, while former police chief Chowdhury Abdullah Al-Mamun, who "
  "cooperated with the trial, got five years. Hasina is living in exile in India.",
  ["Verdict: 17 Nov 2025, ICT-1 Dhaka", "Hasina and ex-Home Minister Asaduzzaman Khan: death (in absentia)",
   "Ex-police chief Al-Mamun: 5 years"],
  [fact("On Monday 17 November 2025 the International Crimes Tribunal 1 in Dhaka sentenced Sheikh Hasina to death for "
        "crimes against humanity; Asaduzzaman Khan also sentenced to death; Al-Mamun five years; Hasina in exile in "
        "India", "intl_has_aj"),
   fact("Bangladesh tribunal sentences ex-PM Hasina to death in absentia for 2024 crackdown", "intl_has_occrp")],
  why="The sources name the International Crimes Tribunal-1 in Dhaka; the other courts did not deliver this verdict.",
  current=ca("2025-11-17"))

# ------------------------------------------------------------------ International CA: Intermediate (2)
G(T, BIL, "Intermediate",
  "During Vice-President C. P. Radhakrishnan's visit to Sri Lanka on 19-20 April 2026, described as the first-ever "
  "bilateral visit by an Indian Vice-President to that country, Sri Lanka decided to join which India-led initiative?",
  ["International Big Cat Alliance", "Global Biofuels Alliance", "Coalition for Disaster Resilient Infrastructure",
   "Indo-Pacific Oceans Initiative"], "*",
  "India-Sri Lanka relations",
  "Vice-President C. P. Radhakrishnan visited Sri Lanka on 19-20 April 2026, the first-ever bilateral visit by an "
  "Indian Vice-President there. He called on President Anura Kumara Disanayaka. Sri Lanka decided to join the "
  "India-led International Big Cat Alliance; MoUs were exchanged on six priority projects in the Eastern Province and a "
  "medical ward complex at Mullaitivu; and OCI eligibility was extended to 5th and 6th generation Indian Origin Tamils.",
  ["Visit: 19-20 Apr 2026, first by an Indian VP", "Sri Lanka to join International Big Cat Alliance",
   "OCI eligibility extended to 5th/6th generation Indian Origin Tamils"],
  [fact("Historic first-ever bilateral visit of the Indian Vice President to Sri Lanka, 19-20 April 2026; Sri Lanka "
        "decided to join the India-led International Big Cat Alliance; MoUs on Eastern Province projects and Mullaitivu "
        "ward complex; OCI extended to 5th and 6th generation Indian Origin Tamils", "intl_vpsl_trib"),
   fact("Indian VP to make historic first bilateral visit to Sri Lanka (April 2026)", "intl_vpsl_nf")],
  why="The sources say Sri Lanka decided to join the International Big Cat Alliance; the other initiatives are not "
      "named for this visit.",
  current=ca("2026-04-19"))

G(T, GEV, "Intermediate",
  "In Denmark's early general election of 24 March 2026, neither bloc won a majority in the 179-seat Folketing. Which "
  "party, led by Foreign Minister Lars Løkke Rasmussen and holding 14 seats, emerged as the kingmaker?",
  ["Moderates", "Venstre (Liberal Party)", "Socialist People's Party", "Danish People's Party"], "*",
  "Elections: Denmark 2026",
  "Prime Minister Mette Frederiksen called an early election, held on 24 March 2026, after a standoff with the US over "
  "Greenland. The left-leaning bloc won 84 seats and the right-leaning bloc 77, short of the 90 needed for a majority "
  "in the 179-seat Folketing. Her Social Democrats stayed the largest party but fell to 21.9%, their lowest in over a "
  "century. The centrist Moderates of Lars Løkke Rasmussen, with 14 seats, became the kingmaker.",
  ["Election 24 Mar 2026; Folketing 179 seats", "Left bloc 84, right bloc 77", "Moderates (Løkke Rasmussen): 14 seats, "
   "kingmaker"],
  [fact("Election on 24 March 2026; Social Democrats 21.9% (27.5% in 2022); Lars Løkke Rasmussen's centrist Moderate "
        "party holds 14 of 179 seats and is the kingmaker", "intl_dk_ap"),
   fact("Left bloc 84 seats, right bloc 77 in the 179-seat parliament; Social Democrats' lowest result in over a "
        "century; Moderates 14 seats led by Lars Løkke Rasmussen", "intl_dk_bt")],
  why="The sources name Løkke Rasmussen's Moderates as the 14-seat kingmaker; the AP report notes the Liberal party "
      "did not intend to govern with the Social Democrats again.",
  current=ca("2026-03-24"))

# ------------------------------------------------------------------ International CA: Advanced (2)
GS(T, GEV, "Advanced", "the referendum held in Ecuador on 16 November 2025",
   ["Voters rejected the proposal to allow foreign military bases, blocking a return of the US military to the airbase "
    "at Manta.",
    "Voters approved the convening of an assembly to rewrite the constitution.",
    "Ecuador had banned foreign military bases on its soil in 2008."],
   [True, False, True],
   "Ecuador referendum 2025",
   "In the referendum of 16 November 2025, Ecuadorians rejected all of President Daniel Noboa's proposals: hosting "
   "foreign military bases (about 60% no), convening a constituent assembly, cutting public funding for parties and "
   "shrinking the National Assembly from 151 to 73 members. The 'no' blocks a US return to the Manta airbase. Foreign "
   "bases had been banned in 2008. Noboa said he respected the people's will.",
   [fact("Referendum on Sunday 16 November 2025: foreign bases rejected; constitutional assembly rejected by more than "
         "61%; rejection blocks US return to the Manta airbase; ban on foreign bases dates from 2008", "intl_ecu_aj"),
    fact("Ecuador rejects US military bases in major defeat for President Noboa", "intl_ecu_npr")],
   why="Statement 2 is wrong: voters rejected the constituent assembly as well.",
   current=ca("2025-11-16"))

GS(T, BIL, "Advanced", "Polish Prime Minister Donald Tusk's visit to India in October 2026",
   ["India and Poland established their Strategic Partnership during this visit.",
    "It was the first visit by a Polish Prime Minister to India since 2010.",
    "Poland announced that it would join the Coalition for Disaster Resilient Infrastructure (CDRI)."],
   [False, True, True],
   "India-Poland relations",
   "Donald Tusk visited India from 21 to 23 October 2026, the first visit by a Polish Prime Minister since 2010. He held "
   "talks with Prime Minister Modi at Hyderabad House on 22 October and also visited Bengaluru. The Strategic "
   "Partnership itself dates from Modi's visit to Poland in August 2024. Poland said it would join the CDRI, and India "
   "invited it to join the International Solar Alliance, the Global Biofuels Alliance and the Indo-Pacific Oceans "
   "Initiative.",
   [fact("Tusk's visit 21-23 October; talks at Hyderabad House on 22 October; first visit by a Polish PM since 2010; "
         "Strategic Partnership elevated in August 2024 during Modi's visit to Poland", "intl_tusk_nk"),
    fact("Poland will join the Coalition for Disaster Resilient Infrastructure (CDRI); India invited Poland to join ISA, "
         "GBA and IPOI", "intl_tusk_org"),
    fact("Tusk's first visit to India as Polish prime minister in 16 years; New Delhi and Bengaluru; Strategic "
         "Partnership elevated during Modi's August 2024 visit to Poland", "intl_tusk_ol")],
   why="Statement 1 is wrong: the Strategic Partnership was established in August 2024, during Modi's visit to Poland.",
   current=ca("2026-10-22"))

T = "Summits and Conferences"
GBS, HOST = "G20, BRICS, SCO and others", "Hosting countries"

# ------------------------------------------------------------------ Summits: Basic (7)
G(T, GBS, "Basic",
  "The 46th Gulf Cooperation Council (GCC) Summit, which concluded on 3 December 2025 with the adoption of the 'Sakhir "
  "Declaration', was hosted by which country?",
  ["Bahrain", "Kuwait", "Oman", "Qatar"], "*",
  "GCC summits",
  "The 46th GCC Summit was held at Sakhir Palace, Manama, and ended on 3 December 2025 with the Sakhir Declaration, "
  "which called the security of member states indivisible and backed deeper economic and digital integration. Italian "
  "Prime Minister Giorgia Meloni joined the summit for talks with GCC leaders. The leaders also backed Bahrain's "
  "two-year term on the UN Security Council for the Arab Group.",
  ["46th GCC Summit: Sakhir Palace, Manama (Bahrain)", "Outcome: Sakhir Declaration", "Guest: Italian PM Meloni"],
  [fact("46th GCC Summit at Sakhir Palace, Manama, concluded with the Sakhir Declaration; Italian PM Giorgia Meloni "
        "joined discussions (report of 4 December 2025)", "sum_gcc_air"),
   fact("46th GCC Summit hosted by the Kingdom of Bahrain concluded with the 'Sakhir Declaration' (3 December 2025)",
        "sum_gcc_kt")],
  why="The sources name Bahrain (Sakhir Palace, Manama) as host; Kuwait, Oman and Qatar did not host the 46th summit.",
  current=ca("2025-12-03"))

G(T, HOST, "Basic",
  "The 55th Pacific Islands Forum Leaders Meeting, held from 30 August to 4 September 2026 under the theme 'BELAU - "
  "Building Economies: Life. Action. Unity.', was hosted by which country?",
  ["Palau", "Fiji", "Tonga", "Samoa"], "*",
  "Pacific Islands Forum",
  "Palau hosted the 55th Pacific Islands Forum Leaders Meeting in Koror from 30 August to 4 September 2026. Its theme, "
  "'Building Economies: Life. Action. Unity.', spells out BELAU, the local name of Palau. Palau's President Surangel "
  "Whipps Jr. took over the Forum chair.",
  ["55th PIF Leaders Meeting: Koror, Palau", "30 Aug-4 Sep 2026", "Theme spells BELAU"],
  [fact("55th Pacific Islands Forum Leaders Meeting hosted by Palau in Koror, 30 August-4 September 2026; theme 'BELAU "
        "- Building Economies: Life. Action. Unity.'", "sum_pif_pina"),
   fact("Palau President Whipps takes Forum chair at the opening in Koror (PACNEWS, 1 September 2026)", "sum_pif_ib")],
  why="The sources name Palau (Koror) as host; Fiji, Tonga and Samoa did not host the 2026 meeting.",
  current=ca("2026-08-30"))

G(T, HOST, "Basic",
  "The eighth summit of the European Political Community (EPC), attended by more than 40 heads of state and government "
  "on 4 May 2026, was hosted by which country?",
  ["Armenia", "Georgia", "Azerbaijan", "Moldova"], "*",
  "European Political Community",
  "The eighth European Political Community summit was held in Yerevan, Armenia, on 4 May 2026, with more than 40 heads "
  "of state and government. European Council President António Costa called it a summit of peace in the Caucasus. The "
  "next EPC meetings are to be hosted by Ireland (November 2026) and Switzerland (April 2027).",
  ["8th EPC summit: Yerevan, Armenia, 4 May 2026", "Next: Ireland (Nov 2026), Switzerland (Apr 2027)"],
  [fact("Eighth EPC summit held in Yerevan, Armenia, on 4 May 2026 with more than 40 heads of state and government; "
        "next in Ireland (November 2026) and Switzerland (April 2027)", "sum_epc_eu4"),
   fact("Yerevan prepares to host EPC summit on May 4", "sum_epc_pan")],
  why="The sources place the summit in Yerevan, Armenia; Georgia, Azerbaijan and Moldova did not host it.",
  current=ca("2026-05-04"))

G(T, HOST, "Basic",
  "The ITU's World Telecommunication Development Conference (WTDC-25), which concluded on 28 November 2025 by adopting "
  "an Action Plan for 2026-2029, was held in which city?",
  ["Baku", "Doha", "Kigali", "Tashkent"], "*",
  "ITU conferences",
  "WTDC-25, organised by the International Telecommunication Union with Azerbaijan, was held in Baku and concluded on 28 "
  "November 2025. It adopted the Baku Declaration and the Baku Action Plan, which sets ITU-D priorities for 2026-2029. "
  "It was described as the first WTDC held in the CIS region.",
  ["WTDC-25: Baku, Azerbaijan; ended 28 Nov 2025", "Baku Action Plan 2026-2029 + Baku Declaration",
   "First WTDC in the CIS region"],
  [fact("WTDC-25 in Baku concluded on Friday 28 November 2025; adopted the Baku Action Plan for 2026-2029 and the Baku "
        "Declaration; first WTDC in the CIS region; organised by ITU with Azerbaijan", "sum_wtdc_az"),
   fact("WTDC-25 in Baku sets attendance record (Azerbaijan ministry)", "sum_wtdc_min")],
  why="The sources place WTDC-25 in Baku; Doha, Kigali and Tashkent did not host it.",
  current=ca("2025-11-28"))

G(T, HOST, "Basic",
  "The 9th Indian Ocean Conference, organised by the India Foundation from 10 to 12 April 2026 on the theme 'Collective "
  "Stewardship for Indian Ocean Governance', was held in which city?",
  ["Port Louis", "Victoria", "Malé", "Colombo"], "*",
  "Indian Ocean Conference",
  "The 9th Indian Ocean Conference (IOC 2026) was held in Port Louis, Mauritius, from 10 to 12 April 2026. It was "
  "organised by the India Foundation together with the Government of Mauritius, on the theme 'Collective Stewardship "
  "for Indian Ocean Governance'.",
  ["IOC 2026 (9th): Port Louis, Mauritius, 10-12 Apr 2026", "Organiser: India Foundation + Govt of Mauritius"],
  [fact("9th Indian Ocean Conference, 10-12 April 2026, Mauritius; theme 'Collective Stewardship for Indian Ocean "
        "Governance'; India Foundation with the Governments of India and Mauritius", "sum_ioc_iora"),
   fact("9th Indian Ocean Conference in Port Louis, Mauritius, 10-12 April 2026, organised by India Foundation with the "
        "Government of Mauritius", "sum_ioc_ht")],
  why="The sources place the conference in Port Louis, Mauritius; the other capitals did not host the 9th edition.",
  current=ca("2026-04-10"))

G(T, GBS, "Basic",
  "The seventh African Union-European Union Summit, held on 24-25 November 2025 under the theme 'Promoting Peace and "
  "Prosperity through Effective Multilateralism', took place in which city?",
  ["Luanda", "Addis Ababa", "Nairobi", "Abuja"], "*",
  "AU-EU summits",
  "The seventh AU-EU Summit was held in Luanda, Angola, on 24-25 November 2025, marking 25 years of the AU-EU "
  "partnership. Its theme was 'Promoting Peace and Prosperity through Effective Multilateralism'.",
  ["7th AU-EU Summit: Luanda, Angola, 24-25 Nov 2025", "Marks 25 years of partnership"],
  [fact("Seventh AU-EU Summit, 24-25 November 2025, Luanda, Angola; theme 'Promoting Peace and Prosperity through "
        "Effective Multilateralism'; 25 years of cooperation", "sum_aueu_eeas"),
   fact("EU-AU summit kicks off in Luanda", "sum_aueu_mia")],
  why="The sources place the summit in Luanda, Angola; Addis Ababa, Nairobi and Abuja did not host it.",
  current=ca("2025-11-24"))

G(T, HOST, "Basic",
  "In February 2026, Cambodia and the International Organisation of La Francophonie (OIF) moved the 20th Francophonie "
  "Summit, scheduled for November 2026, from Siem Reap to which city?",
  ["Phnom Penh", "Battambang", "Sihanoukville", "Kampot"], "*",
  "Francophonie Summit 2026",
  "The 20th Summit of La Francophonie, to be hosted by Cambodia in November 2026, was originally assigned to Siem Reap, "
  "near the Angkor temples. In February 2026 Cambodia's Ministry of Foreign Affairs and the OIF moved it to Phnom Penh "
  "for logistical and operational reasons, such as scattered infrastructure for thousands of delegates and distance "
  "from international connections.",
  ["20th Francophonie Summit (Nov 2026), Cambodia", "Moved from Siem Reap to Phnom Penh (Feb 2026)"],
  [fact("Ministry of Foreign Affairs spokesperson confirmed on 18 February 2026 that the 20th Francophonie Summit is "
        "transferred from Siem Reap to Phnom Penh; summit in November 2026", "sum_franc_lpj"),
   fact("20th Francophonie Summit relocated from Siem Reap to Phnom Penh for logistical and operational reasons, "
        "announced by Cambodia's Foreign Ministry and the OIF", "sum_franc_cm")],
  why="The sources name Phnom Penh as the new venue; the other Cambodian cities are not.",
  current=ca("2026-02-18"))

# ------------------------------------------------------------------ Summits: Intermediate (1)
G(T, GBS, "Intermediate",
  "At its twelfth plenary session (IPBES-12), held in Manchester, UK, in February 2026, the Intergovernmental "
  "Science-Policy Platform on Biodiversity and Ecosystem Services approved which assessment report?",
  ["Business and Biodiversity (methodological) Assessment", "Transformative Change Assessment",
   "Invasive Alien Species Assessment", "Nexus Assessment on biodiversity, water, food and health"], "*",
  "IPBES plenary sessions",
  "The UK hosted IPBES-12 in Manchester from 3 to 8 February 2026, preceded by a Stakeholder Day on 2 February. The "
  "plenary approved the Business and Biodiversity methodological assessment and its Summary for Policymakers, which "
  "examines how businesses depend on and affect biodiversity and nature's contributions to people.",
  ["IPBES-12: Manchester, UK, 3-8 Feb 2026", "Approved: Business and Biodiversity Assessment + SPM"],
  [fact("IPBES-12 in Manchester, UK, 3-8 February 2026 (Stakeholder Day 2 February); Business and Biodiversity "
        "Assessment considered for approval", "sum_ipbes_jncc"),
   fact("12th IPBES plenary in Manchester approved the 'Business and Biodiversity: Methodological Assessment' and its "
        "Summary for Policymakers", "sum_ipbes_ispra")],
  why="The sources name the Business and Biodiversity Assessment as the report approved at IPBES-12; the other "
      "assessments are not.",
  current=ca("2026-02-08"))

# ------------------------------------------------------------------ Summits: Advanced (6)
GS(T, GBS, "Advanced", "the Eleventh Review Conference of the Treaty on the Non-Proliferation of Nuclear Weapons "
   "(NPT), held in 2026",
   ["It was held at UN Headquarters in New York under the presidency of Viet Nam's Ambassador Do Hung Viet.",
    "It ended with the adoption of a substantive final outcome document by consensus.",
    "The treaty has 191 member states."],
   [True, False, True],
   "NPT Review Conference 2026",
   "The Eleventh NPT Review Conference met for four weeks at UN Headquarters, New York, under the presidency of Viet "
   "Nam's Permanent Representative Do Hung Viet, and concluded in May 2026 without agreeing a final outcome document, "
   "the third review cycle in a row to end that way. Procedural reports and arrangements for the next cycle (2031) "
   "were adopted. The treaty has 191 member states.",
   [fact("11th NPT Review Conference at UN Headquarters, New York, under Viet Nam's presidency (Ambassador Do Hung "
         "Viet); no final outcome document due to irreconcilable differences, third consecutive cycle; 191 NPT member "
         "states; next cycle 2031", "sum_npt_vn"),
    fact("Month-long conference concluded 22 May 2026 without a consensus outcome document; third consecutive failure",
         "sum_npt_at")],
   why="Statement 2 is wrong: no consensus outcome document was agreed.",
   current=ca("2026-05-22"))

GS(T, GBS, "Advanced", "the 15th Conference of the Parties to the Convention on Migratory Species (CMS COP15)",
   ["It was held in Campo Grande, Brazil, and ended on 29 March 2026.",
    "Forty species, including the cheetah and the striped hyena, were added to the Convention's appendices.",
    "An interim report presented there found that 49% of the migratory species populations covered by CMS are "
    "declining."],
   [True, True, True],
   "CMS COP15",
   "CMS COP15 ended in Campo Grande, Brazil, on 29 March 2026. Parties added 40 migratory species, among them the "
   "cheetah, striped hyena, snowy owl, giant otter and great hammerhead shark. The interim 'State of the World's "
   "Migratory Species' report found 49% of populations covered by the treaty declining and 24% facing extinction.",
   [fact("COP15 ended on 29 March 2026 in Campo Grande, Brazil; 40 species added incl. cheetah, striped hyena, snowy "
         "owl, giant otter, great hammerhead shark; interim report: 49% of populations declining, 24% face extinction",
         "sum_cms_dte"),
    fact("CMS COP15 convened in Campo Grande, Brazil, 23-29 March 2026", "sum_cms_enb")],
   why="All three statements match the sources.",
   current=ca("2026-03-29"))

GS(T, GBS, "Advanced", "the seventh session of the UN Environment Assembly (UNEA-7)",
   ["It opened on 8 December 2025 at Gigiri, Nairobi, the headquarters of UNEP.",
    "Its theme was 'Advancing Sustainable Solutions for a Resilient Planet'.",
    "Kenyan President William Ruto served as President of UNEA-7."],
   [True, True, False],
   "UN Environment Assembly",
   "UNEA-7 opened on 8 December 2025 at UNEP's headquarters in Gigiri, Nairobi, and ran until 12 December, with nearly "
   "6,000 participants from more than 170 countries. Its theme was 'Advancing Sustainable Solutions for a Resilient "
   "Planet'. The Assembly President was Abdullah bin Ali Al-Amri of Oman; Kenya's President Ruto addressed it as head "
   "of the host country.",
   [fact("Assembly opened Monday 8 December 2025 at Gigiri, Nairobi; theme 'Advancing Sustainable Solutions for a "
         "Resilient Planet'; Abdullah Bin Ali Al-Amri named UNEA-7 President; Ruto to deliver Kenya's national "
         "statement", "sum_unea_aa"),
    fact("UNEA-7 held 8-12 December 2025 in Nairobi; President Abdullah bin Ali Al-Amri of Oman", "sum_unea_unep")],
   why="Statement 3 is wrong: the President of UNEA-7 was Abdullah bin Ali Al-Amri of Oman; Ruto spoke for the host "
       "country.",
   current=ca("2025-12-08"))

GS(T, GBS, "Advanced", "the WHO Global Summit on Traditional Medicine held in New Delhi in December 2025",
   ["It was organised by WHO with India's Ministry of Ayush at Bharat Mandapam.",
    "Its theme was 'Restoring balance: The science and practice of health and well-being'.",
    "It was the first edition of the WHO Global Summit on Traditional Medicine."],
   [True, True, False],
   "WHO traditional medicine summit",
   "The second WHO Global Summit on Traditional Medicine began at Bharat Mandapam, New Delhi, on 17 December 2025, "
   "co-organised by WHO and India's Ministry of Ayush, with the theme 'Restoring balance: The science and practice of "
   "health and well-being'. It was guided by the WHO Global Traditional Medicine Strategy 2025-2034, and an Ayush Expo "
   "was a central feature.",
   [fact("Second WHO Global Summit on Traditional Medicine inaugurated 17 December 2025 at Bharat Mandapam; organised by "
         "WHO and the Ministry of Ayush; theme 'Restoring balance: The science and practice of health and well-being'",
         "sum_tm_air1"),
    fact("Second WHO Global Summit on Traditional Medicine began at Bharat Mandapam; WHO Global Traditional Medicine "
         "Strategy 2025-2034", "sum_tm_air2"),
    fact("Second WHO Global Summit on Traditional Medicine begins in Delhi (17 December 2025)", "sum_tm_week")],
   why="Statement 3 is wrong: the New Delhi summit was the second edition.",
   current=ca("2025-12-17"))

GS(T, GBS, "Advanced", "the 79th World Health Assembly (WHA79), which opened in Geneva on 18 May 2026",
   ["Its Committee A was chaired by Ghana's Kwabena Mintah Akandoh.",
    "Víctor Atallah, Public Health Minister of the Dominican Republic, was elected President of the Assembly.",
    "Ghana's President John Dramani Mahama addressed the opening as Special Guest of Honour."],
   [False, True, True],
   "World Health Assembly",
   "WHA79 opened in Geneva on 18 May 2026 and elected Dr Víctor Elías Atallah Lajam of the Dominican Republic as "
   "President. Committee A was chaired by Dr Timur Sultangaziyev of Kazakhstan and Committee B by Dr Kwabena Mintah "
   "Akandoh of Ghana. Ghana's President John Dramani Mahama spoke as Special Guest of Honour.",
   [fact("WHA79 opened 18 May 2026; President Dr Víctor Elías Atallah Lajam (Dominican Republic); Committee A chair "
         "Timur Sultangaziyev (Kazakhstan), Committee B chair Kwabena Mintah Akandoh (Ghana); Mahama spoke as Special "
         "Guest of Honour", "sum_wha_who"),
    fact("Víctor Atallah, Dominican Public Health Minister, unanimously chosen to preside over the 79th WHA",
         "sum_wha_dt")],
   why="Statement 1 is wrong: Akandoh chaired Committee B; Committee A was chaired by Kazakhstan's Timur Sultangaziyev.",
   current=ca("2026-05-18"))

GS(T, GBS, "Advanced", "the 'Coalition of the Willing' summit on Ukraine held in Paris on 6 January 2026",
   ["It was held at the Élysée Palace.",
    "Ukraine, France and the United Kingdom signed a declaration of intent on deploying a multinational force in "
    "Ukraine after a ceasefire.",
    "The partners agreed to set up a US-Ukraine-Coalition coordination cell at the Coalition's operational "
    "headquarters in Paris."],
   [True, True, True],
   "Ukraine security guarantees",
   "At the Coalition of the Willing summit at the Élysée Palace on 6 January 2026, Presidents Zelensky and Macron and "
   "Prime Minister Keir Starmer signed a declaration of intent on a post-war multinational force for Ukraine. The "
   "framework also includes US-led ceasefire monitoring, and the partners agreed to a US-Ukraine-Coalition "
   "coordination cell at the Coalition Operational Headquarters in Paris. The summit adopted the Paris Declaration on "
   "security guarantees.",
   [fact("6 January 2026, Élysée Palace: Zelensky, Macron and Starmer signed a declaration of intent on a post-war "
         "multinational force; US-Ukraine-Coalition coordination cell at the Coalition Operational Headquarters in "
         "Paris", "sum_paris_ki"),
    fact("Paris Declaration adopted at the 6 January 2026 meeting of the Coalition of the Willing", "sum_paris_osw")],
   why="All three statements match the sources.",
   current=ca("2026-01-06"))

# ###################################################################### part: appt (appointments)
# ###################################################################### part: appt (Important Appointments)
U.update({
    # ---- UN Secretary-General appointment listings (press.un.org)
    "appt_un_p1": ("https://press.un.org/en/content/appointments?page=1", OPENED),
    "appt_un_p2": ("https://press.un.org/en/content/appointments?page=2", OPENED),
    "appt_un_p3": ("https://press.un.org/en/content/appointments?page=3", OPENED),
    "appt_un_p4": ("https://press.un.org/en/content/appointments?page=4", OPENED),
    "appt_un_p5": ("https://press.un.org/en/content/appointments?page=5", OPENED),
    "appt_un_p6": ("https://press.un.org/en/content/appointments?page=6", OPENED),
    # ---- ESCWA
    "appt_escwa_es": ("https://egyptianstreets.com/2026/04/21/rania-al-mashat-appointed-executive-secretary-of-un-escwa/",
                      OPENED),
    "appt_escwa_dne": ("https://www.dailynewsegypt.com/?p=849991", OPENED),
    # ---- OECD
    "appt_oecd_pj": ("https://en.paperjam.lu/article/mathias-cormann-reappointed-secretary-general-of-the-oecd", OPENED),
    "appt_oecd_pr": ("https://www.oecd.org/en/about/news/press-releases/2025/07/oecd-council-extends-the-mandate-of-"
                     "secretary-general-mathias-cormann-to-2031.html", SEARCH),
    # ---- IsDB
    "appt_isdb": ("https://www.isdb.org/news/isdb-board-of-governors-renews-confidence-in-dr-muhammad-al-jasser-with-new-"
                  "five-year-mandate", OPENED),
    # ---- Basel Committee
    "appt_bcbs_bis": ("https://www.bis.org/press/p260317.htm", OPENED),
    "appt_bcbs_osfi": ("https://www.osfi-bsif.gc.ca/index%2ephp/en/news/ben-gully-appointed-next-secretary-general-basel-"
                       "committee-banking-supervision", SEARCH),
    # ---- Banking and finance heads
    "appt_iifcl_pr": ("https://www.iifcl.in/images/FileUploaded/PressReleaseShriRohitRishiAssumesChargeAsManagingDirector"
                      "OfIIFCLpdf04022026205558.pdf", OPENED),
    "appt_iifcl_mp": ("https://www.millenniumpost.in/business/rohit-rishi-takes-charge-as-md-of-india-infrastructure-"
                      "finance-co-ltd-647286", SEARCH),
    "appt_kvb": ("https://www.kvb.bank.in/docs/rbi-approval-for-re-appointment-of-md-ceo.pdf", OPENED),
    "appt_kvb_bs": ("https://boardstewardship.com/rbi-approves-re-appointment-of-b-ramesh-babu-as-md-ceo-of-karur-vysya-"
                    "bank/", SEARCH),
    "appt_ktk_fr": ("https://filingreader.com/news-wire/mumbai/2025-11-15/karnataka-bank-appoints-raghavendra-srinivas-"
                    "bhat-as-md-ceo", OPENED),
    "appt_ktk_nse": ("https://nsearchives.nseindia.com/corporate/KTKBANK_15112025172517_MDFINAL.pdf", SEARCH),
    "appt_ktk_mang": ("https://www.mangalorean.com/karnataka-bank-appoints-raghavendra-srinivas-bhat-as-interim-md-ceo",
                      SEARCH),
    "appt_rbib_som": ("https://financialservices.gov.in/sites/default/files/Order-Notices/2026-09/Somanath-Sreedhara-"
                      "Panicker.pdf", OPENED),
    "appt_rbib_mah": ("https://financialservices.gov.in/sites/default/files/Order-Notices/2026-09/Anand-Gopal-"
                      "Mahindra.pdf", OPENED),
    "appt_rbib_bt": ("https://www.businesstoday.in/amp/industry/banks/story/rbi-appoints-s-somanath-reappoints-anand-"
                     "mahindra-to-its-board-550526-2026-08-21", OPENED),
    "appt_aic_ord": ("https://financialservices.gov.in/sites/default/files/Order-Notices/2026-10/Order-dated-30.09.2026"
                     "---Additional-Charge-CMD--AICIL.pdf", OPENED),
    "appt_aic_pg": ("https://financialservices.gov.in/assignment-additional-charge-ms-mini-george-position-chairman-cum-"
                    "managing-director-cmd-agriculture", OPENED),
    "appt_nrb_kp": ("https://kathmandupost.com/money/2026/08/19/dirgha-rawal-appointed-central-bank-deputy-governor",
                    OPENED),
})

T = "Important Appointments"
BANK, INTL = "Banking and finance heads", "International bodies"

# ------------------------------------------------------------------ Basic (7)
G(T, INTL, "Basic",
  "Stefan Priesner of Austria was appointed by the UN Secretary-General on 2 December 2025 as the United Nations "
  "Resident Coordinator in which country?",
  ["India", "Nepal", "Bangladesh", "Sri Lanka"], "*",
  "UN Resident Coordinators",
  "The UN Secretary-General's appointments list dated 2 December 2025 names Stefan Priesner of Austria as the United "
  "Nations Resident Coordinator in India. A Resident Coordinator is the senior UN representative who leads the UN "
  "country team in a country.",
  ["Appointment of 2 December 2025", "Stefan Priesner (Austria)", "UN Resident Coordinator in India"],
  [fact("2 December 2025: Stefan Priesner of Austria appointed United Nations Resident Coordinator in India",
        "appt_un_p6"),
   fact("2 February 2026: Lila Pieters Yahia of Canada appointed UN Resident Coordinator in Nepal", "appt_un_p5")],
  why="The UN list names Priesner for India; the Resident Coordinator named for Nepal in 2026 is Lila Pieters Yahia, "
      "and no such appointment of Priesner to Bangladesh or Sri Lanka is listed.",
  current=ca("2025-12-02"))

G(T, INTL, "Basic",
  "Rabab Fatima of Bangladesh was appointed by the UN Secretary-General on 15 July 2026 as Special Representative and "
  "head of which UN mission?",
  ["UN Assistance Mission in Afghanistan (UNAMA)", "UN Assistance Mission for Iraq (UNAMI)",
   "UN Mission in South Sudan (UNMISS)", "UN Support Mission in Libya (UNSMIL)"], "*",
  "UN Special Representatives",
  "On 15 July 2026 the UN Secretary-General appointed Rabab Fatima of Bangladesh as his Special Representative for "
  "Afghanistan and Head of the UN Assistance Mission in Afghanistan (UNAMA).",
  ["Appointment of 15 July 2026", "Rabab Fatima (Bangladesh)", "Special Representative for Afghanistan, Head of UNAMA"],
  [fact("15 July 2026: Rabab Fatima of Bangladesh appointed Special Representative for Afghanistan and Head of UNAMA",
        "appt_un_p1")],
  why="The UN list names her for Afghanistan (UNAMA); the other missions are not mentioned in her appointment.",
  current=ca("2026-07-15"))

G(T, BANK, "Basic",
  "On 30 September 2026 the Department of Financial Services gave Mini George, an Executive Director of the company, "
  "additional charge of the post of Chairman-cum-Managing Director of which public sector insurer?",
  ["Agriculture Insurance Company of India Limited", "New India Assurance Company Limited",
   "General Insurance Corporation of India", "Oriental Insurance Company Limited"], "*",
  "Public sector insurers: leadership",
  "By an order dated 30 September 2026, the Department of Financial Services assigned the additional charge of "
  "Chairman-cum-Managing Director (CMD) of Agriculture Insurance Company of India Limited (AICIL) to Mini George, "
  "Executive Director of AICIL, from the date of vacancy (30 September 2026), for an initial three months or until a "
  "regular CMD is appointed, whichever is earlier.",
  ["DFS order dated 30.09.2026", "Mini George, ED, AICIL", "Additional charge of CMD, AICIL, initially for 3 months"],
  [fact("Order dated 30 September 2026: additional charge of CMD, AICIL, to Ms. Mini George, ED, AICIL, from the date of "
        "vacancy 30.09.2026, for an initial three months or till a regular CMD is appointed", "appt_aic_ord"),
   fact("DFS notice: Assignment of Additional Charge to Ms. Mini George for the position of CMD, AICIL (order date "
        "30 Sep 2026)", "appt_aic_pg")],
  why="The DFS order is for Agriculture Insurance Company of India; the other insurers are not named in it.",
  current=ca("2026-09-30"))

G(T, INTL, "Basic",
  "Jeanine Hennis-Plasschaert of the Netherlands was appointed by the UN Secretary-General on 15 May 2026 as "
  "Under-Secretary-General for which department?",
  ["Safety and Security", "Peace Operations", "Political and Peacebuilding Affairs", "Humanitarian Affairs"], "*",
  "UN Under-Secretaries-General",
  "The UN appointments list dated 15 May 2026 names Jeanine Hennis-Plasschaert of the Netherlands as "
  "Under-Secretary-General for Safety and Security.",
  ["Appointment of 15 May 2026", "Jeanine Hennis-Plasschaert (Netherlands)", "USG for Safety and Security"],
  [fact("15 May 2026: Jeanine Hennis-Plasschaert (Netherlands) appointed Under-Secretary-General for Safety and "
        "Security", "appt_un_p3")],
  why="The UN list gives her post as Under-Secretary-General for Safety and Security; the other departments are not "
      "named in her appointment.",
  current=ca("2026-05-15"))

G(T, INTL, "Basic",
  "On 24 February 2026 the UN Secretary-General appointed Pekka Haavisto of Finland as his Personal Envoy for which "
  "country?",
  ["Sudan", "Myanmar", "Yemen", "Haiti"], "*",
  "UN Personal Envoys",
  "The UN appointments list dated 24 February 2026 names Pekka Haavisto of Finland as the Secretary-General's Personal "
  "Envoy for Sudan.",
  ["Appointment of 24 February 2026", "Pekka Haavisto (Finland)", "Personal Envoy for Sudan"],
  [fact("24 February 2026: Pekka Haavisto (Finland) appointed Personal Envoy for Sudan", "appt_un_p5")],
  why="The UN list names Sudan as his assignment; the other countries are not mentioned in it.",
  current=ca("2026-02-24"))

G(T, BANK, "Basic",
  "Dirgha Rawal, who headed the Bank Supervision Department as an executive director, was appointed a deputy governor "
  "of which central bank in August 2026?",
  ["Nepal Rastra Bank", "Royal Monetary Authority of Bhutan", "Bangladesh Bank", "Central Bank of Sri Lanka"], "*",
  "Central banks of neighbouring countries",
  "The Kathmandu Post reported on 19 August 2026 that a Cabinet meeting on Wednesday decided to appoint Dirgha Rawal as "
  "deputy governor of Nepal Rastra Bank. He was an executive director heading the bank's Bank Supervision Department "
  "and has two decades of central banking experience.",
  ["Cabinet decision reported 19 August 2026", "Dirgha Rawal: earlier ED, Bank Supervision Department",
   "Deputy Governor, Nepal Rastra Bank"],
  [fact("Government appointed Dirgha Rawal deputy governor of Nepal Rastra Bank by a Cabinet decision on Wednesday; he "
        "was executive director heading the Bank Supervision Department; article published 19 August 2026",
        "appt_nrb_kp")],
  why="The source names Nepal Rastra Bank; the other central banks are not mentioned in the report.",
  current=ca("2026-08-19", inferred="source (19 Aug 2026) says the Cabinet decided on 'Wednesday'; 19 Aug 2026 is a "
                                     "Wednesday"))

G(T, INTL, "Basic",
  "James Swan of the United States was appointed by the UN Secretary-General on 5 March 2026 as Special "
  "Representative and head of which UN peacekeeping mission?",
  ["MONUSCO", "UNMISS", "MINUSCA", "UNIFIL"], "*",
  "UN Special Representatives",
  "The UN appointments list dated 5 March 2026 names James Swan of the United States as Special Representative for "
  "MONUSCO. On the same day Major General Junhui Wu of China was named Force Commander of UNMISS.",
  ["Appointment of 5 March 2026", "James Swan (United States)", "Special Representative, MONUSCO"],
  [fact("5 March 2026: James Swan (United States) appointed Special Representative, MONUSCO; Major General Junhui Wu "
        "(China) appointed Force Commander, UNMISS", "appt_un_p5")],
  why="The UN list names MONUSCO for Swan; UNMISS's appointment that day was of a Force Commander, and MINUSCA and "
      "UNIFIL are not mentioned.",
  current=ca("2026-03-05"))

# ------------------------------------------------------------------ Intermediate (2)
G(T, INTL, "Intermediate",
  "On 1 June 2026 the UN Secretary-General announced several Resident Coordinator appointments. Rosemary Kalapurakal "
  "of India was named UN Resident Coordinator in which country?",
  ["Zimbabwe", "Malaysia", "Mauritania", "Brazil"], "*",
  "UN Resident Coordinators",
  "The UN appointments list of 1 June 2026 names Rosemary Kalapurakal of India as Resident Coordinator in Zimbabwe. "
  "Appointments made the same day were Nikolas Myint (Germany) for Malaysia, Jutta Hinkkanen (Finland) for Mauritania "
  "and Igor Garafulic (Chile) for Brazil.",
  ["1 June 2026 appointments", "Rosemary Kalapurakal (India): Zimbabwe",
   "Malaysia, Mauritania, Brazil: other appointees"],
  [fact("1 June 2026: Rosemary Kalapurakal (India) UN Resident Coordinator in Zimbabwe; Nikolas Myint (Germany) "
        "Malaysia; Jutta Hinkkanen (Finland) Mauritania", "appt_un_p2"),
   fact("1 June 2026: Igor Garafulic (Chile) UN Resident Coordinator in Brazil", "appt_un_p3")],
  why="Malaysia, Mauritania and Brazil got other Resident Coordinators (Myint, Hinkkanen and Garafulic) on the same day.",
  current=ca("2026-06-01"))

G(T, INTL, "Intermediate",
  "Awa Dabo of the Gambia was appointed by the UN Secretary-General on 16 February 2026 to which post?",
  ["Deputy High Commissioner for Human Rights", "Deputy High Commissioner for Refugees",
   "Assistant Secretary-General for Human Rights, New York", "Deputy Executive Director, UNFPA"], "*",
  "UN senior appointments",
  "The UN appointments list dated 16 February 2026 names Awa Dabo of the Gambia as Deputy High Commissioner for Human "
  "Rights. On the same day Claudia Fuentes Julio of Chile was named Assistant Secretary-General for Human Rights in New "
  "York. Later in 2026, Tressa Rae Finerty (United States) was named Deputy High Commissioner of UNHCR and Catharina "
  "Boehme (Germany) Deputy Executive Director of UNFPA.",
  ["16 February 2026: Awa Dabo (Gambia)", "Deputy High Commissioner for Human Rights",
   "Other posts went to Fuentes Julio, Finerty and Boehme"],
  [fact("16 February 2026: Awa Dabo (Gambia) Deputy High Commissioner for Human Rights; Claudia Fuentes Julio (Chile) "
        "Assistant Secretary-General for Human Rights, New York", "appt_un_p5"),
   fact("8 June 2026: Tressa Rae Finerty (US) Deputy High Commissioner, UNHCR; 26 June 2026: Catharina Boehme "
        "(Germany) Deputy Executive Director, UNFPA", "appt_un_p2")],
  why="The other three posts went to Claudia Fuentes Julio, Tressa Rae Finerty and Catharina Boehme respectively.",
  current=ca("2026-02-16"))

# ------------------------------------------------------------------ Advanced (8)
GS(T, BANK, "Advanced", "the leadership of Karur Vysya Bank",
   ["By a letter dated 24 April 2026, the Reserve Bank of India approved the re-appointment of B. Ramesh Babu as MD "
    "and CEO.",
    "The re-appointment is for a term of three years.",
    "It is his third term as MD and CEO and takes effect from 29 July 2026."],
   [True, False, True],
   "Private bank MD and CEO appointments",
   "In a stock-exchange intimation dated 24 April 2026, Karur Vysya Bank said the RBI, by its letter dated 24.04.2026, "
   "had approved the re-appointment of B. Ramesh Babu as Managing Director and CEO for a third term of two years with "
   "effect from 29 July 2026. The board had recommended it in January 2026.",
   [fact("KVB intimation of 24 April 2026: RBI letter dated 24.04.2026 approved re-appointment of B Ramesh Babu as MD & "
         "CEO for third term of two years with effect from July 29, 2026", "appt_kvb"),
    fact("RBI approved re-appointment of B Ramesh Babu as MD & CEO of Karur Vysya Bank", "appt_kvb_bs")],
   why="Statement 2 is wrong: the third term is of two years, not three.",
   current=ca("2026-04-24"))

GS(T, BANK, "Advanced", "Raghavendra Srinivas Bhat's appointment at Karnataka Bank",
   ["With RBI approval, he was appointed MD and CEO for one year with effect from 16 November 2025.",
    "He joined Karnataka Bank as a clerk in 1981.",
    "He had earlier taken over as interim MD and CEO in July 2025 after Srikrishnan Hari Hara Sarma resigned."],
   [True, True, True],
   "Private bank MD and CEO appointments",
   "Karnataka Bank told the exchanges on 15 November 2025 that, following RBI approval of 14 November 2025, Raghavendra "
   "Srinivas Bhat was appointed MD and CEO for one year from 16 November 2025. He joined the bank as a clerk in 1981 "
   "and had risen to chief operating officer by 2019. He had been interim MD and CEO since July 2025, after "
   "Srikrishnan Hari Hara Sarma resigned.",
   [fact("Filing of 15 Nov 2025: RBI approval 14 Nov 2025; MD & CEO for one year effective 16 Nov 2025; joined Karnataka "
         "Bank as a clerk in 1981; COO by 2019", "appt_ktk_fr"),
    fact("RBI approval letter dated 14 November 2025; appointment effective 16 November 2025 for one year",
         "appt_ktk_nse"),
    fact("Bhat took over as interim MD and CEO for three months from 16 July 2025 after Srikrishnan Hari Hara Sarma "
         "resigned", "appt_ktk_mang")],
   why="All three statements match the bank's filing and reports.",
   current=ca("2025-11-16"))

GS(T, BANK, "Advanced", "Rohit Rishi, who took charge at India Infrastructure Finance Company Ltd (IIFCL) in February "
   "2026",
   ["He joined IIFCL as Managing Director on 4 February 2026.",
    "Immediately before joining IIFCL he was an Executive Director of Indian Bank.",
    "He began his career in 1995 with Indian Bank as an Industrial Development Officer."],
   [True, False, True],
   "Financial institutions: heads",
   "IIFCL's press release of 4 February 2026 says Rohit Rishi joined as its Managing Director that day. Before joining "
   "IIFCL he was Executive Director of Bank of Maharashtra; he had also been a Field General Manager with Indian Bank, "
   "where he began his career in 1995 as an Industrial Development Officer.",
   [fact("Rohit Rishi joined as MD, IIFCL on 4 February 2026; prior to joining he served as ED at Bank of Maharashtra and "
         "was FGM with Indian Bank; began in 1995 with Indian Bank as Industrial Development Officer", "appt_iifcl_pr"),
    fact("Rohit Rishi took charge as MD of India Infrastructure Finance Co Ltd", "appt_iifcl_mp")],
   why="Statement 2 is wrong: he came from Bank of Maharashtra, where he was Executive Director.",
   current=ca("2026-02-04"))

GS(T, BANK, "Advanced", "the appointments to the Central Board of the Reserve Bank of India notified on 20 August 2026",
   ["Former ISRO chairman S. Somanath was appointed a part-time, non-official director.",
    "Industrialist Anand Mahindra was re-appointed a part-time, non-official director.",
    "Both appointments are for a term of three years."],
   [True, True, False],
   "RBI Central Board",
   "By notifications dated 20 August 2026 under Section 8(1)(c) read with Section 8(4) of the RBI Act, 1934, the "
   "Central Government appointed Somanath Sreedhara Panicker (S. Somanath, former ISRO chairman) and re-appointed Anand "
   "Gopal Mahindra (Mahindra Group chairman) as part-time, non-official directors on the RBI's Central Board, each for "
   "four years or until further orders, whichever is earlier.",
   [fact("Notification dated 20 August 2026: Somanath Sreedhara Panicker appointed part-time non-official director on "
         "the RBI Central Board for four years or until further orders (Section 8(1)(c) read with 8(4), RBI Act)",
         "appt_rbib_som"),
    fact("Notification dated 20 August 2026: Anand Gopal Mahindra re-appointed part-time non-official director for four "
         "years or until further orders", "appt_rbib_mah"),
    fact("RBI said S Somanath, former ISRO chair, appointed and Anand Mahindra re-appointed, both for four years from "
         "20 August 2026", "appt_rbib_bt")],
   why="Statement 3 is wrong: both terms are of four years.",
   current=ca("2026-08-20"))

GS(T, INTL, "Advanced", "Ben Gully's appointment announced by the Bank for International Settlements on 17 March 2026",
   ["He was appointed Secretary General of the Basel Committee on Banking Supervision for three years, effective "
    "14 August 2026.",
    "At the time of the appointment he was a Deputy Superintendent at Canada's Office of the Superintendent of "
    "Financial Institutions (OSFI).",
    "He succeeds Erik Thedéen in the post."],
   [True, True, False],
   "Global financial standard setters",
   "On 17 March 2026 the BIS announced that Erik Thedéen, Chair of the Basel Committee and Governor of Sveriges "
   "Riksbank, had appointed Ben Gully as Secretary General of the Committee for three years from 14 August 2026. Gully "
   "was a Deputy Superintendent at OSFI, Canada. He succeeds Neil Esho, Secretary General since February 2022, who "
   "retired on 31 March 2026; Deputy Secretary General Toshio Tsuiki was to act until Gully joined.",
   [fact("17 March 2026: Erik Thedéen (BCBS Chair) appointed Ben Gully Secretary General for three years effective "
         "14 August 2026; Gully is Deputy Superintendent, OSFI; succeeds Neil Esho", "appt_bcbs_bis"),
    fact("Ben Gully appointed as the next Secretary General of the Basel Committee on Banking Supervision",
         "appt_bcbs_osfi")],
   why="Statement 3 is wrong: Gully succeeds Neil Esho; Erik Thedéen is the Committee's Chair who appointed him.",
   current=ca("2026-03-17"))

GS(T, INTL, "Advanced", "Rania Al-Mashat's appointment at the UN Economic and Social Commission for Western Asia "
   "(ESCWA)",
   ["She succeeded Armida Alisjahbana as Executive Secretary.",
    "Before this appointment she was Egypt's Minister of International Cooperation.",
    "She assumed her duties on 19 June 2026 after taking the oath before UN Secretary-General António Guterres."],
   [False, True, True],
   "UN regional commissions",
   "UN Secretary-General António Guterres announced on 20 April 2026 the appointment of Egypt's Rania Al-Mashat, then "
   "Minister of International Cooperation, as Executive Secretary of ESCWA, succeeding Rola Dashti of Kuwait; Mourad "
   "Wahba was to act until she took over. She assumed her duties as Under-Secretary-General and Executive Secretary on "
   "19 June 2026 after taking the oath before Guterres.",
   [fact("Appointment announced 20 April 2026 by Guterres; predecessor Rola Dashti of Kuwait; she was Egypt's Minister "
         "of International Cooperation; Mourad Wahba acting", "appt_escwa_es"),
    fact("She assumed her duties on Friday, 19 June 2026, after taking the oath before Guterres, as USG and Executive "
         "Secretary", "appt_escwa_dne"),
    fact("20 April 2026: Rania A. al-Mashat (Egypt) appointed Executive Secretary of ESCWA", "appt_un_p4")],
   why="Statement 1 is wrong: her predecessor at ESCWA was Rola Dashti of Kuwait.",
   current=ca("2026-06-19"))

GS(T, INTL, "Advanced", "Mathias Cormann, Secretary-General of the OECD",
   ["His renewed mandate, which began on 1 June 2026, runs until 2029.",
    "He is the first OECD Secretary-General from the Asia-Pacific region.",
    "He was born in the German-speaking part of Belgium and was earlier Australia's finance minister."],
   [False, True, True],
   "International organisations: heads",
   "The OECD Council renewed Mathias Cormann's mandate for a second and final five-year term starting 1 June 2026 and "
   "running to 2031; his first term began in June 2021. A former Australian finance minister and senator for Western "
   "Australia, he was born in the German-speaking part of Belgium, and is the first OECD Secretary-General from the "
   "Asia-Pacific region.",
   [fact("Second and final five-year term beginning 1 June 2026, until 2031; former Australian finance minister; born "
         "in the German-speaking part of Belgium; first OECD Secretary-General from the Asia-Pacific region",
         "appt_oecd_pj"),
    fact("OECD Council extends the mandate of Secretary-General Mathias Cormann to 2031, second five-year term from "
         "1 June 2026", "appt_oecd_pr")],
   why="Statement 1 is wrong: the second five-year term runs until 2031.",
   current=ca("2026-06-01"))

GS(T, INTL, "Advanced", "the Islamic Development Bank (IsDB) leadership decision of 18 June 2026",
   ["The Board of Governors re-elected Muhammad Al Jasser as President of the IsDB and Chairman of the IsDB Group.",
    "The decision was taken at the plenary of the 2026 IsDB Group Annual Meetings in Baku, Azerbaijan.",
    "His new term is of five years; he first took office in 2021."],
   [True, True, True],
   "Multilateral development banks: heads",
   "On 18 June 2026, at the plenary of the 2026 IsDB Group Annual Meetings in Baku, Azerbaijan, the IsDB Board of "
   "Governors re-elected Dr. Muhammad Al Jasser as President of the IsDB and Chairman of the IsDB Group for a new "
   "five-year term. He first took office in 2021.",
   [fact("18 June 2026, Baku: Board of Governors renewed Al Jasser's mandate as IsDB President and IsDB Group Chairman "
         "for a new five-year term at the plenary of the 2026 Annual Meetings; first took office in 2021", "appt_isdb")],
   why="All three statements match the IsDB announcement.",
   current=ca("2026-06-18"))

# ###################################################################### part: org (organizations + books)
# ###################################################################### part: org (organisations + books)
U.update({
    # ---- National and International Organizations
    "org_woah": ("https://www.woah.org/en/who-we-are/", OPENED),
    "org_apo_br": ("https://www.apo-tokyo.org/wp-content/uploads/2020/03/APO-Brochure_APO-Overview_light_10Jan2020.pdf",
                   OPENED),
    "org_apo_hist": ("https://apo-tokyo.org/history", OPENED),
    "org_nabfid": ("https://nabfid.org/", OPENED),
    "org_nabfid_iih": ("https://indiainfrahub.com/featured/lok-sabha-passes-national-bank-for-financing-infrastructure-and-"
                       "development-nbfid-bill-2021/", SEARCH),
    "org_ifsca": ("https://ifsca.gov.in/", OPENED),
    "org_cgtmse": ("https://www.cgtmse.in/", OPENED),
    "org_imo_week": ("https://www.theweek.in/news/maritime/2025/11/29/india-re-elected-to-imo-council-for-2026-27-after-"
                     "winning-over-90-pc-votes.html", OPENED),
    "org_imo_mg": ("https://www.maritimegateway.com/india-wins-resounding-re-election-to-imo-council-for-2026-27-term",
                   SEARCH),
    "org_isa": ("https://www.isa.org.jm/about-isa/", OPENED),
    "org_isa_sg": ("https://isa.org.jm/news/the-road-that-brought-me-here-madam-secretary-general-celebrates-"
                   "international-day-of-women-in-diplomacy/", SEARCH),
    "org_isa_br": ("https://www.gov.br/mre/en/contact-us/press-area/press-releases/election-of-brazilian-oceanographer-"
                   "leticia-carvalho-as-secretary-general-of-the-international-seabed-authority", SEARCH),
    "org_bis_origin": ("https://www.bis.gov.in/the-bureau/origin-of-bis/", OPENED),
    "org_bis_about": ("https://www.bis.gov.in/about-bis/", OPENED),
    "org_ecgc_home": ("https://main.ecgc.in/", OPENED),
    "org_ecgc_about": ("https://main.ecgc.in/english/?p=224", OPENED),
    "org_wipo": ("https://www.wipo.int/about-wipo/en/", OPENED),
    "org_wco": ("https://www.wcoomd.org/en/about-us/what-is-the-wco/discover-the-wco.aspx", OPENED),
    "org_wco_basel": ("https://www.basel.int/?tabid=2935", SEARCH),
    "org_wco_brit": ("https://www.britannica.com:443/facts/World-Customs-Organization", SEARCH),
    # ---- Books and Authors
    "bk_dhawan_an": ("https://newsable.asianetnews.com/sports/shikhar-dhawan-unveils-autobiography-the-one-shares-success-"
                     "mindset-articleshow-my98y85", OPENED),
    "bk_dhawan_ly": ("https://www.latestly.com/agency-news/business-news-harpercollins-publishers-india-and-bmw-deutsche-"
                     "motoren-launch-shikhar-dhawans-the-one-cricket-my-life-and-more-at-exclusive-new-delhi-event-"
                     "7241859.html", SEARCH),
    "bk_apnapan_nk": ("https://www.newkerala.com/news/a/he-could-see-far-ahead-shivraj-singh-chouhan-446.htm", OPENED),
    "bk_apnapan_dd": ("https://www.devdiscourse.com/article/law-order/3908227-shivraj-singh-briefs-new-book-apnapan-"
                      "offering-personal-insights-into-pm-modis-leadership", SEARCH),
    "bk_mehta_rw": ("https://www.republicworld.com/india/beyond-the-gavel-tushar-mehta-s-new-books-sheds-light-on-"
                    "courtroom-curiosities-and-lighter-side-of-law-2026-05-10-123740", OPENED),
    "bk_mehta_ll": ("https://www.livelaw.in/amp/news-updates/justice-surya-kant-to-preside-over-launch-of-sg-tushar-"
                    "mehtas-books-at-bharat-mandapam-on-may-10-532861", SEARCH),
    "bk_mahatma_air": ("https://www.newsonair.gov.in/union-minister-dr-mansukh-mandaviya-releases-book-titled-mahatma-a-"
                       "great-communicator", OPENED),
    "bk_shinjini_tp": ("https://theprint.in/feature/what-is-common-among-successful-women-they-laugh-at-patriarchy-says-"
                       "shinjini-kumar/2998749/", OPENED),
    "bk_nene_tp": ("https://theprint.in/feature/shriram-nene-health-book-gets-celebrity-endorsements/3082013/", OPENED),
})

T = "National and International Organizations"
HQ, MEM = "Headquarters and heads", "Membership"

# ------------------------------------------------------------------ Organizations: Basic (4)
G(T, HQ, "Basic",
  "The World Organisation for Animal Health (WOAH), founded in 1924 as the Office International des Epizooties (OIE), "
  "is headquartered in which city?",
  ["Paris", "Geneva", "Rome", "Vienna"], "*",
  "International organisations: headquarters",
  "The World Organisation for Animal Health was founded in 1924 as the Office International des Epizooties (OIE) and "
  "adopted its present name in May 2003. Its headquarters is at 12, rue de Prony, Paris, and it has 183 members.",
  ["WOAH (formerly OIE, 1924)", "Renamed May 2003", "HQ: Paris; 183 members"],
  [fact("WOAH founded in 1924 as the Office International des Epizooties (OIE); name WOAH adopted in May 2003; "
        "headquarters 12, rue de Prony, 75017 Paris; 183 members", "org_woah")],
  why="WOAH's own site gives its headquarters as Paris; it is not based in Geneva, Rome or Vienna.")

G(T, HQ, "Basic",
  "The Asian Productivity Organization (APO), an intergovernmental body established in 1961 of which India is a "
  "founding member, has its Secretariat in which city?",
  ["Tokyo", "Manila", "Bangkok", "Singapore"], "*",
  "Regional organisations: headquarters",
  "The APO is an intergovernmental organisation for improving productivity in Asia and the Pacific. Its convention was "
  "signed in Manila on 14 April 1961 by eight founding members, including India, Japan, Nepal, Pakistan, the "
  "Philippines and Thailand. Its Secretariat is in Tokyo (Hongo, Bunkyo-ku), headed by a Secretary-General.",
  ["APO convention: Manila, 14 April 1961; 8 founders incl. India", "Secretariat: Tokyo, Japan"],
  [fact("The APO Secretariat is located in Tokyo, Japan, headed by a Secretary-General; established in 1961; India is "
        "a member; address 1-24-1 Hongo, Bunkyo-ku, Tokyo", "org_apo_br"),
   fact("APO convention signed on 14 April 1961 in Manila; eight founding members including India, Japan, Nepal, "
        "Pakistan, Philippines, Thailand; Secretariat moved to Hongo in 2012", "org_apo_hist")],
  why="The APO's convention was signed in Manila, but its Secretariat is in Tokyo; Bangkok and Singapore are not its "
      "seat.")

G(T, HQ, "Basic",
  "The National Bank for Financing Infrastructure and Development (NaBFID), a development finance institution set up "
  "on 19 April 2021, is headquartered in which city?",
  ["Mumbai", "New Delhi", "Lucknow", "Gandhinagar"], "*",
  "Indian financial institutions: headquarters",
  "NaBFID was established on 19 April 2021 as a development finance institution for long-term infrastructure "
  "financing. Its office is in the Bandra Kurla Complex, Mumbai; the Bill passed by Parliament provided for a national "
  "bank headquartered in Mumbai.",
  ["NaBFID: DFI for infrastructure, 19 April 2021", "HQ: Mumbai (BKC)"],
  [fact("NaBFID founded on 19 April 2021 as a development finance institution; office at The Capital, G Block, Bandra "
        "Kurla Complex, Mumbai", "org_nabfid"),
   fact("The NaBFID Bill seeks to establish a national bank headquartered in Mumbai with branches elsewhere",
        "org_nabfid_iih")],
  why="The sources place NaBFID in Mumbai; New Delhi, Lucknow and Gandhinagar are not named as its seat.")

G(T, HQ, "Basic",
  "The International Financial Services Centres Authority (IFSCA), established on 27 April 2020 under the IFSCA Act, "
  "2019, is headquartered in which city?",
  ["Gandhinagar (GIFT City)", "Mumbai", "New Delhi", "Ahmedabad"], "*",
  "Indian regulators: headquarters",
  "IFSCA, the unified regulator for International Financial Services Centres in India, was established on 27 April "
  "2020 under the International Financial Services Centres Authority Act, 2019. It is headquartered at GIFT City, "
  "Gandhinagar, Gujarat.",
  ["IFSCA Act, 2019", "Established 27 April 2020", "HQ: GIFT City, Gandhinagar"],
  [fact("IFSCA is headquartered at GIFT City, Gandhinagar, Gujarat; established on 27 April 2020 under the IFSCA Act, "
        "2019", "org_ifsca")],
  why="IFSCA's site gives GIFT City, Gandhinagar as its headquarters, not Mumbai, New Delhi or Ahmedabad.")

# ------------------------------------------------------------------ Organizations: Intermediate (2)
G(T, MEM, "Intermediate",
  "At the 34th session of the International Maritime Organization (IMO) Assembly in London in November 2025, India was "
  "re-elected to the IMO Council for 2026-27 with 154 of 169 valid votes, the highest in its category. India was "
  "elected in the category of States with:",
  ["The largest interest in international seaborne trade",
   "The largest interest in providing international shipping services",
   "Special interests in maritime transport or navigation",
   "Small island developing economies dependent on shipping"], "*",
  "IMO Council elections",
  "India was re-elected to the IMO Council for 2026-27 at the 34th IMO Assembly in London on 28 November 2025. It won "
  "154 of 169 valid votes, the highest in Category (b), which covers the 10 States with the largest interest in "
  "international seaborne trade. The other Category (b) members include Australia, Brazil, Canada, France, Germany, "
  "the Netherlands, Spain, Sweden and the UAE.",
  ["IMO Council 2026-27: India re-elected, 28 Nov 2025", "Category (b): largest interest in international seaborne "
   "trade", "154 of 169 votes, highest in the category"],
  [fact("India re-elected to IMO Council for 2026-27 at the 34th IMO session in London on Friday 28 November 2025; 154 "
        "of 169 valid votes; Category (b): 10 States with the largest interest in international seaborne trade",
        "org_imo_week"),
   fact("India wins resounding re-election to IMO Council for 2026-27 term", "org_imo_mg")],
  why="The sources place India in Category (b), the States with the largest interest in international seaborne trade; "
      "the other descriptions are not India's category.",
  current=ca("2025-11-28"))

G(T, HQ, "Intermediate",
  "The Credit Guarantee Fund Trust for Micro and Small Enterprises (CGTMSE), based in Mumbai, was jointly set up by the "
  "Ministry of Micro, Small and Medium Enterprises and which institution?",
  ["Small Industries Development Bank of India (SIDBI)", "NABARD", "Export-Import Bank of India",
   "State Bank of India"], "*",
  "Credit guarantee institutions",
  "CGTMSE was jointly established by the Ministry of MSME, Government of India, and the Small Industries Development "
  "Bank of India (SIDBI). Its office is in SIDBI's Swavalamban Bhavan, Bandra Kurla Complex, Mumbai.",
  ["CGTMSE = Ministry of MSME + SIDBI", "Office: Swavalamban Bhavan (SIDBI), BKC, Mumbai"],
  [fact("CGTMSE was jointly established by the Ministry of MSME, Government of India and SIDBI; address 1st Floor, "
        "SIDBI, Swavalamban Bhavan, BKC, Mumbai", "org_cgtmse")],
  why="CGTMSE's site names SIDBI as the co-founder with the Ministry of MSME; NABARD, Exim Bank and SBI are not.")

# ------------------------------------------------------------------ Organizations: Advanced (5)
GS(T, HQ, "Advanced", "the International Seabed Authority (ISA)",
   ["It came into existence on 16 November 1994, when the UN Convention on the Law of the Sea (UNCLOS) entered into "
    "force.",
    "Its headquarters is in The Hague, Netherlands.",
    "Leticia Carvalho of Brazil, who took office as Secretary-General on 1 January 2025, is the first woman to lead "
    "it."],
   [True, False, True],
   "ISA: establishment, seat and head",
   "The ISA was established under UNCLOS (1982) and the 1994 Part XI Implementation Agreement, and came into existence "
   "on 16 November 1994 when UNCLOS entered into force. It is headquartered in Kingston, Jamaica, and had 172 members "
   "(171 States and the EU) as of February 2026. Brazilian oceanographer Leticia Carvalho assumed office as "
   "Secretary-General on 1 January 2025, the first woman to lead the ISA.",
   [fact("ISA headquartered in Kingston, Jamaica; established under UNCLOS and the 1994 Agreement; came into existence "
         "on 16 November 1994 when UNCLOS entered into force; 172 members as of 6 February 2026", "org_isa"),
    fact("Leticia Carvalho officially assumed the role of ISA Secretary-General on 1 January 2025; first woman, first "
         "Latin American and first oceanographer to lead the ISA", "org_isa_sg"),
    fact("Brazilian oceanographer Leticia Carvalho elected Secretary-General of the International Seabed Authority",
         "org_isa_br")],
   why="Statement 2 is wrong: the ISA's seat is Kingston, Jamaica, not The Hague. Statements 1 and 3 match the ISA's "
       "own pages.",
   current=ca("2025-01-01"))

GS(T, HQ, "Advanced", "the Bureau of Indian Standards (BIS)",
   ["Its predecessor, the Indian Standards Institution (ISI), came into being in 1950, the year the Constitution came "
    "into force.",
    "BIS came into existence on 1 April 1987 under an Act of Parliament dated 26 November 1986.",
    "It now functions under the Bureau of Indian Standards Act, 2016, under the Ministry of Consumer Affairs, Food and "
    "Public Distribution, with headquarters in New Delhi."],
   [False, True, True],
   "BIS: national standards body",
   "The Indian Standards Institution came into being on 6 January 1947. The Bureau of Indian Standards came into "
   "existence on 1 April 1987 under an Act of Parliament dated 26 November 1986, taking over from the ISI. BIS is now "
   "governed by the BIS Act, 2016, functions under the Ministry of Consumer Affairs, Food and Public Distribution, and "
   "is headquartered in New Delhi.",
   [fact("ISI came into being on 6 January 1947; BIS came into existence on 1 April 1987 under an Act of Parliament "
         "dated 26 November 1986", "org_bis_origin"),
    fact("BIS governed by the BIS Act, 2016; under the Ministry of Consumer Affairs, Food & Public Distribution; "
         "headquartered in New Delhi", "org_bis_about")],
   why="Statement 1 is wrong: the ISI came into being on 6 January 1947, not in 1950. Statements 2 and 3 match BIS's "
       "own pages.")

GS(T, HQ, "Advanced", "ECGC Ltd",
   ["It was set up in 1957, and its former name was Export Credit Guarantee Corporation of India Ltd.",
    "It is wholly owned by the Government of India and functions under the administrative control of the Ministry of "
    "Commerce and Industry.",
    "Its head office is in New Delhi."],
   [True, True, False],
   "ECGC: export credit insurance",
   "ECGC Ltd, formerly Export Credit Guarantee Corporation of India Ltd, was set up in 1957. It is wholly owned by the "
   "Government of India and functions under the administrative control of the Ministry of Commerce and Industry. It "
   "provides export credit insurance to exporters and banks, and its headquarters (ECGC Bhavan) is in Mumbai.",
   [fact("ECGC was set up in 1957; former name Export Credit Guarantee Corporation of India Ltd; wholly owned by the "
         "Government of India; functions under the administrative control of the Ministry of Commerce & Industry",
         "org_ecgc_about"),
    fact("ECGC is an export credit insurer; headquarters at ECGC Bhavan, Mumbai; CIN U74999MH1957GOI010918",
         "org_ecgc_home")],
   why="Statement 3 is wrong: ECGC's headquarters is in Mumbai, not New Delhi. Statements 1 and 2 match ECGC's own "
       "pages.")

GS(T, MEM, "Advanced", "the World Intellectual Property Organization (WIPO)",
   ["It was established in 1967.",
    "It is headquartered in Geneva, Switzerland.",
    "It has 194 member states."],
   [True, True, True],
   "WIPO: basic facts",
   "According to WIPO, it was established in 1967, is headquartered in Geneva, Switzerland, and has 194 member states. "
   "All three statements are correct.",
   [fact("WIPO: headquarters Geneva, Switzerland; established 1967; 194 member states", "org_wipo")],
   why="All three statements match WIPO's own 'About WIPO' page, so none of the other combinations is right.")

GS(T, MEM, "Advanced", "the World Customs Organization (WCO)",
   ["It was established in 1972 as the Customs Co-operation Council.",
    "Its headquarters is in Brussels.",
    "Its members are 187 Customs administrations, which together process about 98% of world trade."],
   [False, True, True],
   "WCO: origin, seat and membership",
   "The WCO was established in 1952 as the Customs Co-operation Council (CCC). Its headquarters is in Brussels. It has "
   "187 member Customs administrations, which together process about 98% of world trade.",
   [fact("WCO established in 1952 as the Customs Co-operation Council (CCC); 187 Customs administrations processing "
         "about 98% of world trade", "org_wco"),
    fact("WCO fact sheet: established by a convention signed in Brussels, headquarters in Brussels", "org_wco_basel"),
    fact("World Customs Organization: established in 1952 as the Customs Co-operation Council, headquarters Brussels",
         "org_wco_brit")],
   why="Statement 1 is wrong: the CCC was established in 1952, not 1972. Statements 2 and 3 are supported by the "
       "sources.")

# ------------------------------------------------------------------ Books and Authors: Intermediate (6)
T = "Books and Authors"
RB = "Recent books"

G(T, RB, "Intermediate",
  "'The One: Cricket, My Life and More', published by HarperCollins and launched at an event in New Delhi in "
  "December 2025, is the autobiography of which Indian cricketer?",
  ["Shikhar Dhawan", "Cheteshwar Pujara", "Ajinkya Rahane", "Rohit Sharma"], "*",
  "Recent books: sports autobiographies",
  "Former India opener Shikhar Dhawan unveiled his autobiography 'The One: Cricket, My Life and More', published by "
  "HarperCollins, at a special event in New Delhi on Sunday, 14 December 2025. It traces his journey and his "
  "comebacks.",
  ["'The One: Cricket, My Life and More' - Shikhar Dhawan", "HarperCollins; launched New Delhi, 14 Dec 2025"],
  [fact("Shikhar Dhawan unveiled his autobiography 'The One: Cricket, My Life and More' (HarperCollins) at a special "
        "event in New Delhi on Sunday; article dated 14 December 2025", "bk_dhawan_an"),
   fact("HarperCollins Publishers India and BMW Deutsche Motoren launch Shikhar Dhawan's 'The One: Cricket, My Life "
        "and More' at an exclusive New Delhi event", "bk_dhawan_ly")],
  why="The sources name Shikhar Dhawan as the author; the book is not by Pujara, Rahane or Rohit Sharma.",
  current=ca("2025-12-14", inferred="Asianet report dated 14 Dec 2025 says the launch was on 'Sunday'"))

G(T, RB, "Intermediate",
  "'Apnapan', a book launched in New Delhi on 26 May 2026 about the author's experiences with Prime Minister Narendra "
  "Modi, was written by which Union Minister?",
  ["Shivraj Singh Chouhan", "Rajnath Singh", "Nitin Gadkari", "Dharmendra Pradhan"], "*",
  "Recent books by public figures",
  "Union Minister Shivraj Singh Chouhan launched his book 'Apnapan', an account of his decades of association with "
  "Prime Minister Narendra Modi, in New Delhi on Tuesday, 26 May 2026.",
  ["'Apnapan' - Shivraj Singh Chouhan", "Launched New Delhi, 26 May 2026", "On his experiences with PM Modi"],
  [fact("Union Minister Shivraj Singh Chouhan launched his book 'Apnapan: My Experiences With Narendra Modi' in New "
        "Delhi on Tuesday, 26 May 2026", "bk_apnapan_nk"),
   fact("Shivraj Singh briefs new book 'Apnapan' offering personal insights into PM Modi's leadership",
        "bk_apnapan_dd")],
  why="The sources name Shivraj Singh Chouhan as the author; the other ministers did not write it.",
  current=ca("2026-05-26"))

G(T, RB, "Intermediate",
  "Two books of humorous courtroom anecdotes, 'The Bench, the Bar, and the Bizarre' and 'The Lawful and the Awful', "
  "were launched in New Delhi on 10 May 2026 in the presence of Union Home Minister Amit Shah. Who wrote them?",
  ["Tushar Mehta", "R. Venkataramani", "Harish Salve", "Kapil Sibal"], "*",
  "Recent books: law",
  "Solicitor General of India Tushar Mehta launched two books, 'The Bench, the Bar, & the Bizarre' and 'The Lawful "
  "and the Awful', in New Delhi on Sunday, 10 May 2026 (Mother's Day). Union Home Minister Amit Shah presided, and "
  "Chief Justice of India Surya Kant also spoke; the event was held at Bharat Mandapam.",
  ["Author: Solicitor General Tushar Mehta", "Launched 10 May 2026, New Delhi (Bharat Mandapam)",
   "Amit Shah presided; CJI Surya Kant present"],
  [fact("Solicitor General Tushar Mehta's books 'The Bench, the Bar, & the Bizarre' and 'The Lawful and the Awful' "
        "launched on Sunday, 10 May 2026; Amit Shah presided; Justice Surya Kant spoke", "bk_mehta_rw"),
   fact("CJI Surya Kant to preside over launch of SG Tushar Mehta's books at Bharat Mandapam on May 10",
        "bk_mehta_ll")],
  why="The sources name Solicitor General Tushar Mehta as the author; the other lawyers are not.",
  current=ca("2026-05-10"))

G(T, RB, "Intermediate",
  "'Mahatma: A Great Communicator', released by Union Minister Mansukh Mandaviya at Gandhi Darshan, Rajghat, New Delhi "
  "on 2 March 2026, was written by Dr Dhiraj Kakadia, an Additional Director General of which organisation?",
  ["Akashvani (All India Radio)", "Doordarshan", "Press Information Bureau", "National Book Trust"], "*",
  "Recent books: Gandhi",
  "Union Minister Mansukh Mandaviya released 'Mahatma: A Great Communicator' at Gandhi Darshan, Rajghat, New Delhi on "
  "2 March 2026. Written by Dr Dhiraj Kakadia, Additional Director General of Akashvani, the book, available in Hindi, "
  "English and Gujarati, looks at how Mahatma Gandhi's communication skills shaped the freedom movement.",
  ["Author: Dr Dhiraj Kakadia, ADG, Akashvani", "Released 2 March 2026 by Mansukh Mandaviya, Rajghat",
   "Hindi, English, Gujarati"],
  [fact("Mansukh Mandaviya released 'Mahatma: A Great Communicator' by Dr Dhiraj Kakadia, Additional Director General, "
        "Akashvani, at Gandhi Darshan, Rajghat; page dated 2 March 2026; in Hindi, English and Gujarati",
        "bk_mahatma_air")],
  why="The source describes the author as an Additional Director General of Akashvani, not of the other bodies.",
  current=ca("2026-03-02"))

G(T, RB, "Intermediate",
  "'Busy Women: Building Commerce and Culture in Middle India', launched at the India International Centre, New Delhi "
  "in July 2026, is by Shinjini Kumar. She was earlier the first CEO of which payments bank?",
  ["Paytm Payments Bank", "Airtel Payments Bank", "India Post Payments Bank", "Fino Payments Bank"], "*",
  "Recent books: banking and entrepreneurship",
  "Shinjini Kumar's 'Busy Women: Building Commerce and Culture in Middle India' was launched at the India "
  "International Centre, New Delhi on 27 July 2026. It draws on three years of travel across 30 Tier-II cities and "
  "meetings with more than 300 women entrepreneurs. Kumar joined the RBI at 20, was later the first CEO of Paytm "
  "Payments Bank and co-founded a personal finance start-up.",
  ["'Busy Women' - Shinjini Kumar, launched 27 July 2026, IIC", "Author: ex-RBI; first CEO of Paytm Payments Bank",
   "Based on 300+ women entrepreneurs in 30 Tier-II cities"],
  [fact("Shinjini Kumar's book 'Busy Women, Building Commerce and Culture in Middle India' launched on 27 July at the "
        "India International Centre (article of 28 July 2026); she joined the RBI at 20 and became the first CEO of "
        "Paytm Payments Bank", "bk_shinjini_tp")],
  why="The source names her as the first CEO of Paytm Payments Bank, not of the other payments banks.",
  current=ca("2026-07-27"))

G(T, RB, "Intermediate",
  "'21 Days to Good Health: A Surgeon's Evidence-Based Program to Reset Your Body, Calm Your Mind, and Add Years to "
  "Your Life', a 2026 book carrying endorsements from Nita Ambani and Sachin Tendulkar, was written by whom?",
  ["Dr Shriram Nene", "Dr Devi Shetty", "Dr Naresh Trehan", "Dr Ramakanta Panda"], "*",
  "Recent books: health",
  "Surgeon Dr Shriram Nene launched '21 Days to Good Health: A Surgeon's Evidence-Based Program to Reset Your Body, "
  "Calm Your Mind, and Add Years to Your Life' in 2026. Its opening pages carry endorsements from Nita Ambani, Madhuri "
  "Dixit, Sachin Tendulkar, Harsh Goenka, Amitabh Kant and others.",
  ["'21 Days to Good Health' - Dr Shriram Nene (surgeon)", "Endorsed by Nita Ambani, Sachin Tendulkar and others"],
  [fact("Dr Shriram Nene has launched '21 Days to Good Health: A Surgeon's Evidence-Based Program...'; endorsements "
        "from Nita Ambani, Madhuri Dixit, Sachin Tendulkar, Harsh Goenka, Amitabh Kant; article dated 26 October 2026",
        "bk_nene_tp")],
  why="The source names Dr Shriram Nene as the author; the other doctors are not.",
  current=ca("2026-10-26", inferred="ThePrint article of 26 Oct 2026 says the book has been launched; no exact date"))

# ###################################################################### part: awsp (awards + sports)
# ###################################################################### part: awsp (Awards and Honours + Sports)
U.update({
    # ---- Awards and Honours
    "aw_fifa_legal": ("https://legal.fifa.com/organisation/news/aitana-bonmati-ousmane-dembele-top-honours-the-best-"
                      "football-awards-2025", OPENED),
    "aw_fifa_africanews": ("https://www.africanews.com/amp/2025/12/16/aitana-bonmati-and-ousmane-dembele-emerge-as-"
                           "winners-at-the-fifa-awards", SEARCH),
    "aw_lata_ks": ("https://www.kailashsatyarthi.net/?p=1412", OPENED),
    "aw_lata_kk": ("https://www.kolkatakonnect.com/2026/04/pt-hridaynath-mangeshkar-declares.html", OPENED),
    "aw_fn_air": ("https://newsonair.gov.in/president-droupadi-murmu-conferred-national-florence-nightingale-awards-"
                  "2026-at-rashtrapati-bhavan/", OPENED),
    "aw_fn_md": ("https://medicaldialogues.in/nursing/news/president-murmu-felicitates-15-nurses-with-national-"
                 "florence-nightingale-awards-2026-170512", SEARCH),
    "aw_messi_fpa": ("https://www.fpa.es/en/area-of-communication-and-media/press-releases/leo-messi-princess-of-"
                     "asturias-award-for-sports-2026/", OPENED),
    "aw_messi_open": ("https://openthemagazine.com/sports/lionel-messi-becomes-first-footballer-to-win-princess-of-"
                      "asturias-sports-award", OPENED),
    "aw_messi_ara": ("https://en.ara.cat/sports/leo-messi-awarded-the-princess-of-asturias-award-for-sports-2026_1_"
                     "5756842.amp.html", OPENED),
    "aw_wa_pr": ("https://worldathletics.org/awards/news/duplantis-mclaughlin-levrone-world-athletics-awards-2025",
                 OPENED),
    "aw_wa_aw": ("https://athleticsweekly.com/news/mondo-duplantis-and-sydney-mclaughlin-levrone-named-world-"
                 "athletes-of-the-year-1040008986/", SEARCH),
    # ---- Sports
    "sp_afcon_caf": ("https://www.cafonline.com/afcon2025/news/afcon-2025-senegal-to-face-hosts-morocco-in-final-"
                     "after-dramatic-semi-final-night/", OPENED),
    "sp_afcon_icir": ("https://www.icirnigeria.org/historic-night-as-senegal-beat-morocco-emerge-2025-afcon-winner/",
                      OPENED),
    "sp_afcon_tel": ("https://telegraph.ng/?p=30679", SEARCH),
    "sp_wta_nbc": ("https://www.nbcsports.com/tennis/news/rybakina-beats-no-1-ranked-sabalenka-to-win-wta-finals",
                   OPENED),
    "sp_wta_ewn": ("https://www.ewn.co.za/2025/11/09/rybakina-outguns-world-no1-sabalenka-to-win-wta-finals", SEARCH),
    "sp_blitz_qt": ("https://www.qatar-tribune.com/article/211888/sports/carlsen-wins-20th-world-title-in-doha-"
                    "assaubayeva-becomes-womens-blitz-champion-for-a-third-time", OPENED),
    "sp_blitz_fide": ("https://worldrapidandblitz2025.fide.com/author/press/", SEARCH),
    "sp_sc_aiff": ("https://www.the-aiff.com/article/aiff-super-cup-2025-26-fc-goa-three-time-champions", OPENED),
    "sp_sc_week": ("https://www.theweek.in/news/sports/2025/12/07/super-cup-2025-final-fc-goa-retain-title-after-"
                   "beating-east-bengal-in-penalty-shootout.html", SEARCH),
    "sp_wtf_cgtn": ("https://news.cgtn.com/news/2025-12-22/China-claims-mixed-doubles-title-at-BWF-World-Tour-Finals-"
                    "in-Hangzhou-1Jj6WtFannO/p.html", OPENED),
    "sp_wtf_yonex": ("https://news.yonex.co.uk/2025/12/23/christo-popov-makes-history-at-bwf-world-tour-finals-2025/",
                     SEARCH),
    "sp_tata_fide": ("https://www.fide.com/nodirbek-abdusattorov-wins-tata-steel-chess-masters-2026/", OPENED),
    "sp_tata_cc": ("https://www.chess.com/news/view/abdusattorov-wins-2026-tata-steel-chess", SEARCH),
    "sp_ae_macao": ("https://macaonews.org/life/sports/wang-zhiyi-beats-an-se-young-all-england-2026/", OPENED),
    "sp_ae_latestly": ("https://www.latestly.com/quickly/sports/badminton/lin-chun-yi-defeats-lakshya-sen-to-claim-"
                       "historic-all-england-2026-title-7346864.html", SEARCH),
    "sp_whil_ians": ("https://ianslive.in/womens-hil-sg-pipers-beat-shrachi-bengal-tigers-in-penalty-shoot-out-to-"
                     "lift-title--20260110224935", OPENED),
    "sp_whil_bridge": ("https://thebridge.in/hockey/sg-pipers-clinch-womens-hil-202526-title-55665", SEARCH),
    "sp_mast_pga": ("https://www.pgatour.com/article/news/daily-wrapup/2026/04/12/rory-mcilroy-wins-90th-masters-"
                    "augusta-national-leaderboard-results-scores-round-4-scottie-scheffler-cameron-young", OPENED),
    "sp_mast_cbs": ("https://www.cbsnews.com/news/rory-mcilroy-masters-2026", SEARCH),
    "sp_ic_arab": ("https://www.arabnews.com/node/2626638/sport", OPENED),
    "sp_ic_dsabah": ("https://www.dailysabah.com/sports/football/safonovs-shootout-heroics-lift-psg-to-intercontinental-"
                     "cup-title/amp", SEARCH),
    "sp_nba_cgtn": ("https://news.cgtn.com/news/2026-06-14/New-York-Knicks-complete-comeback-to-win-first-NBA-title-in-"
                    "53-years-1NXRKaD83OE/p.html", OPENED),
    "sp_nba_br": ("https://bleacherreport.com/articles/25440298-jalen-brunson-wins-nba-finals-2026-mvp-top-stats-"
                  "highlights-and-twitter-reaction", SEARCH),
    "sp_sb_wlbt": ("https://www.wlbt.com/2026/02/09/seattle-seahawks-defeat-new-england-patriots-claim-super-bowl-lx-"
                   "29-13/", OPENED),
    "sp_sb_nbc": ("https://www.nbcdfw.com/super-bowl/recap-seahawks-defense-patriots-maye/3980685/", SEARCH),
})

T = "Awards and Honours"
NAT, INTL = "National awards", "International awards"

# ------------------------------------------------------------------ Awards: Basic (1)
G(T, INTL, "Basic",
  "Who was named The Best FIFA Men's Player 2025 at The Best FIFA Football Awards held in Qatar on 16 December 2025?",
  ["Ousmane Dembélé", "Lamine Yamal", "Kylian Mbappé", "Mohamed Salah"], "*",
  "The Best FIFA Football Awards 2025",
  "At The Best FIFA Football Awards 2025, presented in Qatar on 16 December 2025, Ousmane Dembélé of Paris "
  "Saint-Germain and France was named The Best FIFA Men's Player. Aitana Bonmatí (Barcelona/Spain) won the women's "
  "award, and PSG's Luis Enrique was named best men's coach.",
  ["Men's Player: Ousmane Dembélé (PSG/France)", "Women's Player: Aitana Bonmatí", "Men's Coach: Luis Enrique"],
  [fact("The Best FIFA Football Awards 2025, 16 December 2025, Qatar: Men's Player Ousmane Dembélé (PSG/France); "
        "Women's Player Aitana Bonmatí; Men's Coach Luis Enrique", "aw_fifa_legal"),
   fact("Aitana Bonmatí and Ousmane Dembélé emerge as winners at the FIFA awards (16 December 2025)",
        "aw_fifa_africanews")],
  why="FIFA's announcement names Ousmane Dembélé as the men's winner; the other players did not win the award.",
  current=ca("2025-12-16"))

# ------------------------------------------------------------------ Awards: Intermediate (1)
G(T, NAT, "Intermediate",
  "Which Nobel Peace Prize laureate received the Lata Deenanath Mangeshkar Award 2026 at a ceremony in Pune on 24 "
  "April 2026, the death anniversary of Master Deenanath Mangeshkar?",
  ["Kailash Satyarthi", "Malala Yousafzai", "Muhammad Yunus", "Narges Mohammadi"], "*",
  "Lata Deenanath Mangeshkar Award",
  "Pandit Hridaynath Mangeshkar announced and presented the Lata Deenanath Mangeshkar Award 2026, the fifth year of "
  "the award, to Kailash Satyarthi for his contribution to child rights and social justice. The ceremony was held "
  "on 24 April 2026, the 84th death anniversary of Master Deenanath Mangeshkar, at Ganesh Kala Krida Mandir, "
  "Swargate, Pune.",
  ["Lata Deenanath Mangeshkar Award 2026: Kailash Satyarthi", "24 April 2026, Ganesh Kala Krida Mandir, Pune",
   "Fifth year of the award"],
  [fact("Kailash Satyarthi received the Lata Deenanath Mangeshkar Award on Friday, 24 April 2026 (84th death "
        "anniversary of Master Deenanath Mangeshkar) at Ganesh Kala Krida Mandir, Swargate, Pune; presented by Pt. "
        "Hridaynath Mangeshkar; 5th year of the award", "aw_lata_ks"),
   fact("Pt Hridaynath Mangeshkar declared that Nobel laureate Kailash Satyarthi will receive the Lata Deenanath "
        "Mangeshkar Award 2026 for his work on child rights and social justice; ceremony 24 April 2026, Pune",
        "aw_lata_kk")],
  why="The sources name Kailash Satyarthi as the 2026 recipient; the other laureates are not mentioned.",
  current=ca("2026-04-24"))

# ------------------------------------------------------------------ Awards: Advanced (3)
GS(T, NAT, "Advanced",
   "the National Florence Nightingale Awards 2026",
   ["The awards were instituted in 1990 by the Indian Nursing Council.",
    "President Droupadi Murmu conferred them on 15 nursing professionals at Rashtrapati Bhavan on 12 May 2026.",
    "Each awardee receives a certificate of merit, a medal and a cash prize of ₹1 lakh."],
   (False, True, True),
   "National Florence Nightingale Awards",
   "President Droupadi Murmu presented the National Florence Nightingale Awards 2026 to 15 nursing professionals at "
   "Rashtrapati Bhavan on 12 May 2026, around International Nurses Day. The awards were instituted in 1973 by the "
   "Ministry of Health and Family Welfare for Registered Nurses, Midwives, ANMs and Lady Health Visitors. Each "
   "awardee gets a certificate of merit, a medal and ₹1 lakh. Statement 1 is wrong on both the year and the body.",
   [fact("President Droupadi Murmu conferred the National Florence Nightingale Awards 2026 on 15 nursing professionals "
         "at Rashtrapati Bhavan on 12 May 2026; instituted in 1973 by the Ministry of Health and Family Welfare; "
         "certificate of merit, ₹1 lakh cash and a medal", "aw_fn_air"),
    fact("President Murmu felicitates 15 nurses with National Florence Nightingale Awards 2026", "aw_fn_md")],
   why="Statement 1 is incorrect: the awards were instituted in 1973 by the Ministry of Health and Family Welfare.",
   current=ca("2026-05-12"))

GS(T, INTL, "Advanced",
   "the Princess of Asturias Award for Sports 2026",
   ["It was awarded to Argentine footballer Lionel Messi.",
    "The award comprises a Joan Miró sculpture, a diploma, an insignia and a cash prize of 50,000 euros.",
    "It was the first of that year's eight Princess of Asturias Awards to be announced."],
   (True, True, False),
   "Princess of Asturias Awards",
   "On 3 June 2026 the jury of the Princess of Asturias Award for Sports chose Argentine footballer Leo Messi; he is "
   "described as the first individual footballer to receive the honour. Each laureate receives a Joan Miró sculpture, "
   "a diploma, an insignia and €50,000. The Foundation said the Sports award was the sixth of the eight awards "
   "bestowed that year, so statement 3 is wrong.",
   [fact("Leo Messi, Princess of Asturias Award for Sports 2026; Joan Miró sculpture, diploma, insignia and 50,000 "
         "euros; sixth of the eight Princess of Asturias Awards bestowed in the forty-sixth year", "aw_messi_fpa"),
    fact("Messi became the first individual footballer to receive the Princess of Asturias Sports award",
         "aw_messi_open"),
    fact("Leo Messi awarded the Princess of Asturias Award for Sports 2026 (report of 3 June 2026)", "aw_messi_ara")],
   why="Statement 3 is incorrect: the Foundation calls the Sports award the sixth of the eight awards that year.",
   current=ca("2026-06-03"))

GS(T, INTL, "Advanced",
   "the World Athletics Awards 2025 held in Monaco on 30 November 2025",
   ["Mondo Duplantis and Sydney McLaughlin-Levrone were named the World Athletes of the Year.",
    "Kenya's Sabastian Sawe won the men's Out of Stadium Athlete of the Year award.",
    "Kenya's Edmund Serem was named the men's Rising Star."],
   (True, True, True),
   "World Athletics Awards",
   "At the World Athletics Awards 2025 in Monaco on 30 November 2025, Sweden's Mondo Duplantis and USA's Sydney "
   "McLaughlin-Levrone were named World Athletes of the Year. Category winners included Emmanuel Wanyonyi (men's "
   "track), Nicola Olyslagers (women's field), Maria Perez and Sabastian Sawe (Out of Stadium). The Rising Star awards "
   "went to Zhang Jiale of China and Edmund Serem of Kenya.",
   [fact("World Athletics Awards 2025, Monaco, 30 Nov 2025: World Athletes of the Year Mondo Duplantis (SWE) and Sydney "
         "McLaughlin-Levrone (USA); Out of Stadium: Maria Perez (ESP), Sabastian Sawe (KEN); Rising Stars: Zhang "
         "Jiale (CHN), Edmund Serem (KEN)", "aw_wa_pr"),
    fact("Mondo Duplantis and Sydney McLaughlin-Levrone named world athletes of the year", "aw_wa_aw")],
   why="All three statements match the World Athletics press release.",
   current=ca("2025-11-30"))

T = "Sports"
TW, VR = "Tournaments and winners", "Venues and records"

# ------------------------------------------------------------------ Sports: Basic (1)
G(T, TW, "Basic",
  "Which country won the 2025 Africa Cup of Nations (AFCON), beating hosts Morocco 1-0 after extra time in the final "
  "at Rabat on 18 January 2026?",
  ["Senegal", "Nigeria", "Egypt", "Ivory Coast"], "*",
  "Africa Cup of Nations 2025",
  "Senegal beat hosts Morocco 1-0 after extra time in the AFCON 2025 final at the Prince Moulay Abdellah Stadium, "
  "Rabat, on 18 January 2026; Pape Gueye scored. In the semi-finals Morocco had beaten Nigeria on penalties and "
  "Senegal had beaten Egypt 1-0. It was Senegal's second AFCON title.",
  ["Final: Senegal 1-0 Morocco (a.e.t.), Rabat, 18 Jan 2026", "Semis: Morocco beat Nigeria (pens), Senegal beat Egypt"],
  [fact("Final on Sunday 18 January 2026 at Prince Moulay Abdellah Stadium, Rabat: Morocco vs Senegal; Morocco beat "
        "Nigeria 4-2 on penalties, Senegal beat Egypt 1-0 in the semi-finals", "sp_afcon_caf"),
   fact("Senegal beat Morocco to win AFCON 2025 in Rabat; Pape Gueye scored in extra time; Senegal's second title",
        "sp_afcon_icir"),
   fact("Senegal beat Morocco 1-0 to win second AFCON title", "sp_afcon_tel")],
  why="Nigeria and Egypt lost in the semi-finals; the sources name Senegal as champions.",
  current=ca("2026-01-18"))

# ------------------------------------------------------------------ Sports: Intermediate (10)
G(T, TW, "Intermediate",
  "Who won the WTA Finals 2025 singles title in Riyadh on 8 November 2025, beating world No. 1 Aryna Sabalenka "
  "6-3, 7-6(0) in the final?",
  ["Elena Rybakina", "Iga Świątek", "Coco Gauff", "Amanda Anisimova"], "*",
  "WTA Finals 2025",
  "Elena Rybakina beat world No. 1 Aryna Sabalenka 6-3, 7-6(0) in the WTA Finals 2025 final at the King Saud "
  "University Indoor Arena, Riyadh, on 8 November 2025. It was her first WTA Finals title, and she collected USD 5.23 "
  "million.",
  ["WTA Finals 2025, Riyadh: Rybakina bt Sabalenka 6-3, 7-6(0)", "First WTA Finals title; USD 5.23 million"],
  [fact("Rybakina beat Sabalenka 6-3, 7-6 (0) on Saturday, 8 November 2025, at King Saud University Indoor Arena, "
        "Riyadh; first WTA Finals title; USD 5.23 million", "sp_wta_nbc"),
   fact("Rybakina outguns world No.1 Sabalenka to win WTA Finals", "sp_wta_ewn")],
  why="The sources name Elena Rybakina as the champion; the other players did not win the 2025 WTA Finals.",
  current=ca("2025-11-08"))

G(T, TW, "Intermediate",
  "At the FIDE World Blitz Championships 2025 in Doha, where Magnus Carlsen won the open title, who won the "
  "women's world blitz title for the third time by beating Anna Muzychuk in the final?",
  ["Bibisara Assaubayeva", "Ju Wenjun", "Koneru Humpy", "Hou Yifan"], "*",
  "FIDE World Blitz Championships 2025",
  "Kazakhstan's Bibisara Assaubayeva won her third women's world blitz title in Doha, beating Ukraine's Anna Muzychuk "
  "2.5-1.5 in the final. Magnus Carlsen won the open blitz title, beating Nodirbek Abdusattorov 2.5-1.5 in the final, "
  "for his ninth world blitz crown.",
  ["Women's blitz: Bibisara Assaubayeva (KAZ), third title", "Open blitz: Magnus Carlsen (ninth)"],
  [fact("Bibisara Assaubayeva (Kazakhstan) won her third world women's blitz title, beating Anna Muzychuk 2.5-1.5 in "
        "the final; Carlsen beat Abdusattorov in the open final; article of 31 December 2025 says the final was on "
        "Tuesday", "sp_blitz_qt"),
   fact("FIDE World Rapid and Blitz Championships 2025, Doha (FIDE press page)", "sp_blitz_fide")],
  why="The source names Bibisara Assaubayeva as women's blitz champion; the others did not win it.",
  current=ca("2025-12-30", inferred="Qatar Tribune report of 31 Dec 2025 says the blitz finals were on Tuesday"))

G(T, TW, "Intermediate",
  "FC Goa won the AIFF Super Cup 2025-26 on 7 December 2025, beating East Bengal 6-5 on penalties after a goalless "
  "final at Fatorda. How many Super Cup titles has FC Goa now won?",
  ["Three", "Two", "Four", "One"], "*",
  "AIFF Super Cup 2025-26",
  "FC Goa and East Bengal drew 0-0 after extra time in the AIFF Super Cup final at PJN Stadium, Fatorda, on 7 "
  "December 2025, and Goa won the first-ever penalty shoot-out in a Super Cup final 6-5. It was Goa's record third "
  "Super Cup title; Goa had also won the previous edition, so they retained the trophy.",
  ["Final: FC Goa 0-0 East Bengal, Goa won 6-5 on penalties", "Venue: PJN Stadium, Fatorda", "Goa's third title"],
  [fact("Sunday 7 December 2025, PJN Stadium, Fatorda: FC Goa beat East Bengal 6-5 on penalties after 0-0; Goa's "
        "third Super Cup, a record", "sp_sc_aiff"),
   fact("FC Goa retain Super Cup title after beating East Bengal in penalty shootout", "sp_sc_week")],
  why="The AIFF calls this Goa's third Super Cup title.",
  current=ca("2025-12-07"))

G(T, TW, "Intermediate",
  "Who won the men's singles title at the BWF World Tour Finals 2025 in Hangzhou on 21 December 2025, beating "
  "China's Shi Yuqi in the final?",
  ["Christo Popov", "Viktor Axelsen", "Kunlavut Vitidsarn", "Anders Antonsen"], "*",
  "BWF World Tour Finals 2025",
  "France's Christo Popov beat Shi Yuqi 21-19, 21-9 in the men's singles final of the BWF World Tour Finals in "
  "Hangzhou on 21 December 2025. An Se-young of South Korea won the women's singles, beating Wang Zhiyi.",
  ["Men's singles: Christo Popov (FRA) bt Shi Yuqi 21-19, 21-9", "Women's singles: An Se-young (KOR)"],
  [fact("BWF World Tour Finals, Hangzhou, 21 December 2025: men's singles Christo Popov (France) beat Shi Yuqi 21-19, "
        "21-9; women's singles An Se-young beat Wang Zhiyi", "sp_wtf_cgtn"),
   fact("Christo Popov makes history at BWF World Tour Finals 2025", "sp_wtf_yonex")],
  why="The sources name Christo Popov as the men's singles champion; the other players did not win the title.",
  current=ca("2025-12-21"))

G(T, TW, "Intermediate",
  "Which grandmaster won the Masters section of the 88th Tata Steel Chess Tournament at Wijk aan Zee, which ended "
  "on 1 February 2026?",
  ["Nodirbek Abdusattorov", "Javokhir Sindarov", "Vincent Keymer", "Hans Niemann"], "*",
  "Tata Steel Chess 2026",
  "Uzbekistan's Nodirbek Abdusattorov won the Tata Steel Chess Masters 2026, the 88th edition, held at Wijk aan Zee "
  "from 16 January to 1 February 2026. It was his first Masters title, on his fourth attempt. Andy Woodward won the "
  "Challengers section and earned a place in the 2027 Masters.",
  ["Masters 2026: Nodirbek Abdusattorov (UZB)", "Challengers: Andy Woodward", "Dates: 16 Jan-1 Feb 2026"],
  [fact("Nodirbek Abdusattorov wins Tata Steel Chess Masters 2026; 88th edition at Wijk aan Zee, 16 January-1 "
        "February 2026; Andy Woodward won the Challengers; Sindarov, Niemann, Keymer and van Foreest were in "
        "contention before the last round", "sp_tata_fide"),
   fact("Abdusattorov wins 2026 Tata Steel Masters, Woodward takes Challengers", "sp_tata_cc")],
  why="FIDE names Abdusattorov as the winner; Sindarov, Keymer and Niemann were contenders who did not win.",
  current=ca("2026-02-01"))

G(T, TW, "Intermediate",
  "India's Lakshya Sen finished runner-up in the men's singles at the All England Open Badminton Championships 2026 "
  "in Birmingham. Who beat him 21-15, 22-20 in the final?",
  ["Lin Chun-yi", "Shi Yuqi", "Kodai Naraoka", "Jonatan Christie"], "*",
  "All England Open 2026",
  "Lin Chun-yi of Chinese Taipei beat Lakshya Sen 21-15, 22-20 in the men's singles final of the All England Open "
  "2026 at the Utilita Arena, Birmingham, for his first BWF Super 1000 title. In the women's final, Wang Zhiyi of "
  "China beat An Se-young, ending her 36-match winning streak.",
  ["Men's singles: Lin Chun-yi (TPE) bt Lakshya Sen 21-15, 22-20", "Women's singles: Wang Zhiyi bt An Se-young"],
  [fact("All England Open 2026, Utilita Arena, Birmingham: Lin Chun-yi beat Lakshya Sen 21-15, 22-20 for his first "
        "Super 1000 title; Wang Zhiyi beat An Se-young; article of 9 March 2026 says the women's final was "
        "'yesterday'", "sp_ae_macao"),
   fact("Lin Chun-yi defeats Lakshya Sen to claim historic All England 2026 title", "sp_ae_latestly")],
  why="The sources name Lin Chun-yi as Lakshya Sen's opponent and winner in the final.",
  current=ca("2026-03-08", inferred="Macao News report of 9 March 2026 says the finals were played 'yesterday'"))

G(T, TW, "Intermediate",
  "SG Pipers, led by captain Navneet Kaur, won the Women's Hockey India League 2025-26 title in Ranchi on 10 January "
  "2026. Which team did they beat in a penalty shoot-out in the final?",
  ["Shrachi Bengal Tigers", "Ranchi Royals", "JSW Soorma Hockey Club", "Odisha Warriors"], "*",
  "Women's Hockey India League 2025-26",
  "SG Pipers and Shrachi Bengal Tigers drew 1-1 in the Women's HIL final in Ranchi on 10 January 2026, and SG Pipers "
  "won the shoot-out 3-2. Captain Navneet Kaur was Player of the Tournament. The winners received ₹1.5 crore, the "
  "runners-up ₹1 crore and third-placed Ranchi Royals ₹50 lakh.",
  ["Final: SG Pipers 1-1 Shrachi Bengal Tigers; SG Pipers won shoot-out 3-2", "Player of the Tournament: Navneet Kaur",
   "Prize: ₹1.5 crore (winners)"],
  [fact("SG Pipers beat Shrachi Bengal Tigers 3-2 in a shoot-out after 1-1 in the Women's HIL final in Ranchi (10 "
        "January 2026); Navneet Kaur Player of the Tournament; Ranchi Royals third", "sp_whil_ians"),
   fact("SG Pipers clinch Women's HIL 2025-26 title", "sp_whil_bridge")],
  why="Ranchi Royals finished third; the source names Shrachi Bengal Tigers as the beaten finalists.",
  current=ca("2026-01-10"))

G(T, TW, "Intermediate",
  "Rory McIlroy won the 90th Masters golf tournament at Augusta National on 12 April 2026, becoming only the fourth "
  "player to win the event in consecutive years. Whom did he beat by one stroke?",
  ["Scottie Scheffler", "Justin Rose", "Jon Rahm", "Xander Schauffele"], "*",
  "The Masters 2026",
  "Rory McIlroy won the 90th Masters at 12 under par (276), one shot ahead of Scottie Scheffler, a year after his "
  "play-off win over Justin Rose. He joined Jack Nicklaus, Nick Faldo and Tiger Woods as the only back-to-back "
  "Masters champions.",
  ["90th Masters: McIlroy, -12 (276), by one shot over Scheffler", "Back-to-back winners: Nicklaus, Faldo, Woods, "
   "McIlroy"],
  [fact("McIlroy won the 90th Masters at 12-under 276, one shot ahead of Scottie Scheffler; fourth back-to-back "
        "champion after Nicklaus, Faldo and Woods; a year after his playoff win over Justin Rose (12 April 2026)",
        "sp_mast_pga"),
   fact("Rory McIlroy wins Masters 2026", "sp_mast_cbs")],
  why="Justin Rose was McIlroy's 2025 play-off opponent; the 2026 runner-up was Scottie Scheffler.",
  current=ca("2026-04-12"))

G(T, TW, "Intermediate",
  "Paris Saint-Germain won the FIFA Intercontinental Cup 2025 in Qatar on 17 December 2025 on penalties after a 1-1 "
  "draw, with substitute goalkeeper Matvei Safonov saving four spot-kicks. Which club did PSG beat in the final?",
  ["Flamengo", "Palmeiras", "Botafogo", "Pyramids FC"], "*",
  "FIFA Intercontinental Cup 2025",
  "PSG drew 1-1 with Brazil's Flamengo in the FIFA Intercontinental Cup final in Doha on 17 December 2025 "
  "(Kvaratskhelia scored, Jorginho equalised from the spot) and won the shoot-out 2-1, with Matvei Safonov saving "
  "four penalties.",
  ["Final: PSG 1-1 Flamengo; PSG won 2-1 on penalties", "Safonov saved four penalties"],
  [fact("Wednesday 17 December 2025, Doha: PSG beat Flamengo 2-1 on penalties after 1-1; Kvaratskhelia scored, "
        "Jorginho equalised; Safonov saved four penalties", "sp_ic_arab"),
   fact("Safonov's shootout heroics lift PSG to Intercontinental Cup title", "sp_ic_dsabah")],
  why="The source names Flamengo as PSG's opponent in the final.",
  current=ca("2025-12-17"))

G(T, TW, "Intermediate",
  "The New York Knicks won the 2026 NBA title, their first since 1973, by beating which team 4-1 in the NBA Finals "
  "that ended on 13 June 2026?",
  ["San Antonio Spurs", "Oklahoma City Thunder", "Denver Nuggets", "Minnesota Timberwolves"], "*",
  "NBA Finals 2026",
  "The New York Knicks beat the San Antonio Spurs 4-1 in the 2026 NBA Finals, clinching the title in Game 5 at the "
  "Frost Bank Center, San Antonio, on 13 June 2026. It was their first title since 1973, and Jalen Brunson was named "
  "Finals MVP.",
  ["Knicks bt Spurs 4-1; Game 5 on 13 June 2026", "Finals MVP: Jalen Brunson", "First Knicks title since 1973"],
  [fact("Knicks beat the San Antonio Spurs 4-1; Game 5 on 13 June 2026 at Frost Bank Center, San Antonio; Jalen "
        "Brunson Finals MVP; first title since 1973", "sp_nba_cgtn"),
   fact("Jalen Brunson wins NBA Finals 2026 MVP", "sp_nba_br")],
  why="The source names the San Antonio Spurs as the Knicks' opponents in the Finals.",
  current=ca("2026-06-13"))

# ------------------------------------------------------------------ Sports: Advanced (1)
GS(T, VR, "Advanced",
   "Super Bowl LX played on 8 February 2026",
   ["The Seattle Seahawks beat the New England Patriots 29-13 in Santa Clara, California.",
    "It was the Seattle Seahawks' first Super Bowl title.",
    "Running back Kenneth Walker III was named MVP, the first running back to win the award since Terrell Davis "
    "in 1998."],
   (True, False, True),
   "Super Bowl LX",
   "The Seattle Seahawks beat the New England Patriots 29-13 in Super Bowl LX in Santa Clara, California, on 8 "
   "February 2026. It was Seattle's second Super Bowl title (its first since the 2014 season). Kenneth Walker III, "
   "who rushed for 135 yards on 27 carries, was named MVP, the first running back to win it since Terrell Davis in "
   "1998.",
   [fact("Seahawks 29, Patriots 13 in Santa Clara, California; Seattle's second Super Bowl win; Kenneth Walker III MVP, "
         "first running back since Terrell Davis in 1998 (article of 8 February 2026)", "sp_sb_wlbt"),
    fact("Super Bowl LX recap: Seahawks defence overwhelms Drake Maye and the Patriots", "sp_sb_nbc")],
   why="Statement 2 is incorrect: the source calls it Seattle's second Super Bowl win.",
   current=ca("2026-02-08"))

# ###################################################################### part: eco (economic affairs)
# ###################################################################### part: eco (Economic Affairs)
U.update({
    # ---- Inflation data
    "eco_wpinov_week": ("https://www.theweek.in/news/biz-tech/2025/12/15/india-posts-negative-wholesale-inflation-"
                        "november-2025-cheaper-food-oil-fuel-provisional-govt-data-dpiit.html", OPENED),
    "eco_wpinov_trib": ("https://www.tribuneindia.com/news/business/wholesale-inflation-remains-in-negative-territory-"
                        "at-0-32-in-nov-despite-monthly-price-uptick", SEARCH),
    "eco_wpiapr_ao": ("https://www.angelone.in/news/economy/india-wpi-inflation-hits-42-month-high-of-8-percent-in-"
                      "april-2026", OPENED),
    "eco_wpiapr_rw": ("https://www.republicworld.com/business/india-wholesale-inflation-wpi-april-2026-hits-42-month-"
                      "high-2026-05-14-124191", SEARCH),
    "eco_cpimay_pib": ("https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/jun/doc2026612891101.pdf",
                       OPENED),
    "eco_cpimay_ziro": ("https://www.ziromarket.com/blog/india-may-2026-cpi-inflation-3-93-percent", SEARCH),
    # ---- GDP and growth projections
    "eco_fae_trib": ("https://www.tribuneindia.com/news/fy26-forecast/indias-economy-to-grow-by-7-4-in-fy26-driven-"
                     "largely-by-service-sector-nso-data", OPENED),
    "eco_fae_dtn": ("https://www.dtnext.in/news/business/india-to-be-fastest-economy-in-fy26-nso-data", SEARCH),
    "eco_imfjan_air": ("https://www.newsonair.gov.in/imf-raises-indias-economic-growth-projection-for-2025-by-0-7-"
                       "percentage-point-to-7-3", OPENED),
    "eco_imfjan_fpj": ("https://www.freepressjournal.in/business/imf-raises-indias-gdp-growth-forecast-to-73-per-cent-"
                       "for-fy26-on-strong-economic-momentum", SEARCH),
    "eco_adb_adb": ("https://www.adb.org/news/adb-upgrades-asia-and-pacific-growth-outlook", OPENED),
    "eco_adb_org": ("https://organiser.org/2025/12/12/329868/bharat/india-to-grow-at-7-2-percent-in-2025-26-says-adb-"
                    "in-upgraded-economic-outlook/", SEARCH),
    "eco_oecd_ians": ("https://ianslive.in/india-to-remain-worlds-fastest-growing-economy-in-fy26-oecd--20251202215103",
                      OPENED),
    "eco_oecd_inf": ("https://informistmedia.com/MoneyWire/40058/Economic-Outlook-OECD-retains-India-s-FY26-GDP-growth-"
                     "forecast-at-6-7-37-cuts-CPI-view-to-1-9-37-", SEARCH),
    "eco_iip_etv": ("https://www.etvbharat.com/en/business/india-industrial-output-rises-in-november-on-robust-"
                    "manufacturing-enn25122903751", OPENED),
    "eco_iip_ob": ("https://www.outlookbusiness.com/news/industrial-output-growth-at-2-year-high-of-67-pc-in-nov-on-"
                   "robust-manufacturing", SEARCH),
    # ---- Fiscal data
    "eco_cgaoct_np": ("https://nagalandpost.com/centres-fiscal-deficit-hits-52-6-pc-of-full-year-target-at-oct-end/",
                      OPENED),
    "eco_cgaoct_bs": ("https://www.business-standard.com/economy/news/india-s-fiscal-deficit-during-apr-oct-reaches-"
                      "52-6-of-fy26-target-125112800733_1.html", SEARCH),
    "eco_gstnov_air": ("https://www.newsonair.gov.in/gross-gst-collections-rise-0-7-to-over-%E2%82%B91-70-lakh-crore-in-"
                       "november/", OPENED),
    "eco_gstnov_bt": ("https://www.businesstoday.in/latest/economy/story/gross-gst-collection-up-0-7-percent-to-rs-1-70-"
                      "lakh-crore-in-november-504447-2025-12-01", SEARCH),
    "eco_cgajul_de": ("https://www.dailyexcelsior.com/centres-fy27-fiscal-deficit-touches-26-8-pc-of-full-year-target-"
                      "at-end-july-govt-data/", OPENED),
    "eco_cgajul_pio": ("https://dailypioneer.com/news/centre-fiscal-deficit-fy27-july-cga-data", SEARCH),
    # ---- Monetary policy decisions
    "eco_fed_frb": ("https://www.federalreserve.gov/newsevents/pressreleases/monetary20251210a.htm", OPENED),
    "eco_fed_mp": ("https://www.marketpulse.com/markets/breaking-news-us-federal-reserve-cuts-rates-by-25-bps-bringing-"
                   "target-range-to-350-375/", SEARCH),
    "eco_boj_air": ("https://www.newsonair.gov.in/bank-of-japan-raises-key-policy-interest-rate-to-0-75-from-0-5",
                    OPENED),
    "eco_boj_wam": ("https://www.wam.ae/en/article/15xgblt-bank-japan-raises-interest-rates-30-year-high", SEARCH),
    "eco_boe_pp": ("https://www.professionalpensions.com/news/4523497/bank-england-cuts-interest-rate-375", OPENED),
    "eco_boe_fr": ("https://www.financialreporter.co.uk/bank-of-england-cuts-interest-rates-to-375.html", SEARCH),
})

T = "Economic Affairs"
GDP, INF, FIS, MON = ("GDP and growth projections", "Inflation data", "Fiscal data", "Monetary policy decisions")

# ------------------------------------------------------------------ Economic Affairs: Basic (6)
G(T, INF, "Basic",
  "According to provisional data released on 15 December 2025, what was India's annual wholesale price (WPI) "
  "inflation for November 2025?",
  ["(-) 0.32%", "0.32%", "(-) 0.56%", "(-) 1.48%"], "*",
  "WPI inflation: November 2025",
  "Provisional data released on 15 December 2025 put India's annual WPI inflation for November 2025 at (-) 0.32%, so "
  "wholesale prices were slightly lower than a year earlier. Food inflation in the WPI narrowed to (-) 2.60% from "
  "(-) 5.04% in October, while the WPI rose month-on-month in November.",
  ["WPI inflation, Nov 2025: (-) 0.32% (provisional)", "WPI food inflation: (-) 2.60% (Oct: (-) 5.04%)"],
  [fact("Annual WPI inflation (provisional) for November 2025 was (-) 0.32%; WPI food inflation narrowed to -2.60% from "
        "-5.04% in October; article dated 15 December 2025", "eco_wpinov_week"),
   fact("Wholesale inflation remains in negative territory at -0.32% in November despite monthly price uptick",
        "eco_wpinov_trib")],
  why="The sources give (-) 0.32%; the figure was negative, so 0.32% is wrong, and the other values are not reported.",
  current=ca("2025-12-15"))

G(T, GDP, "Basic",
  "According to the First Advance Estimates released by the National Statistics Office (NSO) on 7 January 2026, "
  "India's real GDP was estimated to grow by how much in 2025-26?",
  ["7.4%", "7.0%", "6.9%", "7.8%"], "*",
  "First Advance Estimates of GDP, 2025-26",
  "The NSO released the First Advance Estimates of national income for 2025-26 on 7 January 2026. Real GDP was "
  "estimated to grow 7.4% in 2025-26, up from 6.5% in 2024-25; nominal GDP growth was put at 8% and real GVA growth at "
  "7.3%.",
  ["FAE released 7 Jan 2026", "Real GDP 2025-26: 7.4% (2024-25: 6.5%)", "Nominal GDP: 8%; real GVA: 7.3%"],
  [fact("NSO first advance estimates released on Wednesday, 7 January 2026: real GDP growth 7.4% in FY26 against 6.5% "
        "in FY25; nominal GDP growth 8%; real GVA up 7.3%", "eco_fae_trib"),
   fact("India to be fastest economy in FY26: NSO data (first advance estimates, 7.4% growth)", "eco_fae_dtn")],
  why="The First Advance Estimates put real GDP growth at 7.4%; the other figures are not the NSO estimate.",
  current=ca("2026-01-07"))

G(T, GDP, "Basic",
  "In its World Economic Outlook Update released on 19 January 2026, the IMF raised India's growth projection for "
  "2025 (fiscal year 2025-26) by 0.7 percentage point to what level?",
  ["7.3%", "6.6%", "6.9%", "7.6%"], "*",
  "IMF World Economic Outlook Update, January 2026",
  "The IMF's January 2026 World Economic Outlook Update raised India's growth projection for 2025 (FY 2025-26) by 0.7 "
  "percentage point to 7.3%. It projected growth of 6.4% for 2026-27 and global growth of 3.3% in 2026.",
  ["India FY 2025-26: raised by 0.7 pp to 7.3%", "India 2026-27: 6.4%", "Global growth 2026: 3.3%"],
  [fact("IMF raised India's economic growth projection for 2025 by 0.7 percentage point to 7.3%; projected 6.4% for "
        "2026-27; global growth 3.3% in 2026 (article of 19 January 2026)", "eco_imfjan_air"),
   fact("IMF raises India's GDP growth forecast to 7.3 per cent for FY26 on strong economic momentum", "eco_imfjan_fpj")],
  why="The IMF's revised figure is 7.3%; 6.6% is the level before the 0.7-point increase, and the others are not cited.",
  current=ca("2026-01-19"))

G(T, MON, "Basic",
  "At its meeting concluded on 10 December 2025, the US Federal Reserve's Federal Open Market Committee (FOMC) cut "
  "the target range for the federal funds rate by 25 basis points to which range?",
  ["3.50%-3.75%", "3.75%-4.00%", "3.25%-3.50%", "4.00%-4.25%"], "*",
  "US Federal Reserve: December 2025 decision",
  "On 10 December 2025 the FOMC lowered the target range for the federal funds rate by 1/4 percentage point to "
  "3.50%-3.75%. Three members dissented: Stephen Miran wanted a half-point cut, while Austan Goolsbee and Jeffrey "
  "Schmid preferred no change. The Committee also said it would begin buying shorter-term Treasury securities as "
  "needed to keep reserves ample.",
  ["Cut of 25 bps to 3.50%-3.75%", "Dissents: Miran (wanted 50 bps cut); Goolsbee and Schmid (no change)"],
  [fact("FOMC statement of 10 December 2025: target range lowered by 1/4 percentage point to 3-1/2 to 3-3/4 percent; "
        "Miran preferred a 1/2-point cut; Goolsbee and Schmid preferred no change", "eco_fed_frb"),
   fact("US Federal Reserve cuts rates by 25 bps, bringing target range to 3.50-3.75%", "eco_fed_mp")],
  why="The Fed statement sets the new range at 3.50%-3.75%; 3.75%-4.00% was the range before the cut.",
  current=ca("2025-12-10"))

G(T, FIS, "Basic",
  "According to Controller General of Accounts (CGA) data released on 28 November 2025, the Centre's fiscal deficit "
  "for April-October 2025 reached what share of the 2025-26 Budget Estimate?",
  ["52.6%", "46.5%", "58.4%", "61.3%"], "*",
  "CGA monthly accounts: April-October 2025",
  "CGA data released on 28 November 2025 showed the Centre's fiscal deficit at ₹8,25,144 crore in April-October 2025, "
  "or 52.6% of the 2025-26 Budget Estimate of ₹15.69 lakh crore (4.4% of GDP). In the same period of 2024-25 it had "
  "been 46.5% of that year's Budget Estimate.",
  ["Apr-Oct 2025 fiscal deficit: ₹8.25 lakh crore = 52.6% of BE", "Year-ago: 46.5% of BE 2024-25",
   "BE 2025-26: ₹15.69 lakh crore (4.4% of GDP)"],
  [fact("Fiscal deficit touched 52.6% of the full-year target at end-October; ₹8,25,144 crore; 46.5% a year earlier; "
        "target 4.4% of GDP or ₹15.69 lakh crore; CGA data released Friday (dateline 28 November 2025)",
        "eco_cgaoct_np"),
   fact("India's fiscal deficit during Apr-Oct reaches 52.6% of FY26 target", "eco_cgaoct_bs")],
  why="The CGA data give 52.6%; 46.5% was the share a year earlier, and the other figures are not reported.",
  current=ca("2025-11-28"))

G(T, MON, "Basic",
  "On 19 December 2025 the Bank of Japan raised its key policy interest rate to its highest level since September "
  "1995. What is the new rate?",
  ["0.75%", "0.50%", "1.00%", "0.25%"], "*",
  "Bank of Japan: December 2025 rate hike",
  "The Bank of Japan raised its key policy interest rate by a quarter point, from 0.5% to 0.75%, on 19 December 2025. "
  "This is the highest level since September 1995.",
  ["BoJ policy rate: 0.5% to 0.75%", "Highest since September 1995"],
  [fact("Bank of Japan raised its key policy interest rate to 0.75 per cent from 0.5 per cent; highest level since "
        "September 1995 (article of 19 December 2025)", "eco_boj_air"),
   fact("Bank of Japan raises interest rates to 30-year high", "eco_boj_wam")],
  why="The sources give the new rate as 0.75%; 0.50% was the rate before the hike.",
  current=ca("2025-12-19"))

# ------------------------------------------------------------------ Economic Affairs: Intermediate (6)
G(T, GDP, "Intermediate",
  "In its Asian Development Outlook released on 10 December 2025, the Asian Development Bank raised India's growth "
  "forecast for 2025 (FY 2025-26) to 7.2%. What growth did it project for India for 2026 (FY 2026-27)?",
  ["6.5%, unchanged", "6.7%, raised", "7.0%, raised", "6.2%, lowered"], "*",
  "ADB Asian Development Outlook, December 2025",
  "The ADB's Asian Development Outlook of December 2025 (released 10 December) raised India's 2025 growth forecast by "
  "0.7 percentage point to 7.2%, citing stronger third-quarter expansion, and kept the 2026 forecast unchanged at "
  "6.5%. For developing Asia and the Pacific it raised the 2025 forecast to 5.1% from 4.8%.",
  ["India 2025 (FY26): 7.2% (up 0.7 pp from 6.5%)", "India 2026 (FY27): 6.5%, unchanged",
   "Developing Asia 2025: 5.1%"],
  [fact("ADO December 2025 (10 December 2025): India's 2025 growth raised 0.7 pp to 7.2%; 2026 forecast unchanged at "
        "6.5%; developing Asia and Pacific 2025 forecast 5.1% from 4.8%", "eco_adb_adb"),
   fact("India to grow at 7.2 percent in 2025-26, says ADB in upgraded economic outlook", "eco_adb_org")],
  why="The ADB kept its 2026 forecast for India unchanged at 6.5%; it was neither raised nor lowered.",
  current=ca("2025-12-10"))

G(T, GDP, "Intermediate",
  "In its Economic Outlook released on 2 December 2025, the OECD projected India's real GDP growth for 2025-26, "
  "2026-27 and 2027-28 respectively as:",
  ["6.7%, 6.2% and 6.4%", "6.7%, 6.4% and 6.2%", "7.2%, 6.5% and 6.4%", "6.4%, 6.2% and 6.7%"], "*",
  "OECD Economic Outlook, December 2025",
  "The OECD's Economic Outlook of 2 December 2025 projected India's growth at 6.7% in 2025-26, 6.2% in 2026-27 and "
  "6.4% in 2027-28, keeping India the fastest-growing major economy. It expected low headline inflation to converge "
  "gradually towards the 4% target.",
  ["2025-26: 6.7%", "2026-27: 6.2%", "2027-28: 6.4%"],
  [fact("OECD economic outlook released Tuesday (article of 2 December 2025): India to grow 6.7% in 2025-26, 6.2% in "
        "2026-27 and 6.4% in 2027-28", "eco_oecd_ians"),
   fact("Economic Outlook: OECD retains India's FY26 GDP growth forecast at 6.7%, cuts CPI view to 1.9%",
        "eco_oecd_inf")],
  why="The OECD figures are 6.7%, 6.2% and 6.4% in that order; the other options swap or alter them.",
  current=ca("2025-12-02"))

G(T, GDP, "Intermediate",
  "India's Index of Industrial Production (IIP) grew 6.7% in November 2025, a two-year high (data released on 29 "
  "December 2025). Which of the following sectors recorded a contraction in that month?",
  ["Electricity", "Manufacturing", "Mining", "None of these; all three sectors grew"], "*",
  "IIP: November 2025",
  "Industrial output growth rose to a two-year high of 6.7% in November 2025, from a revised 0.5% in October. "
  "Manufacturing grew 8% and mining 5.4%, while electricity generation contracted 1.5% (against 4.4% growth a year "
  "earlier). The previous higher reading was 11.9% in November 2023.",
  ["IIP Nov 2025: 6.7% (Oct: 0.5%)", "Manufacturing +8%, mining +5.4%, electricity -1.5%"],
  [fact("IIP growth 6.7% in November 2025, a two-year high (11.9% in Nov 2023); October revised to 0.5%; manufacturing "
        "8%, mining 5.4%, electricity contracted 1.5%; NSO data released Monday, 29 December 2025", "eco_iip_etv"),
   fact("Industrial output growth at 2-year high of 6.7% in Nov on robust manufacturing", "eco_iip_ob")],
  why="Only electricity contracted (-1.5%); manufacturing (+8%) and mining (+5.4%) grew.",
  current=ca("2025-12-29"))

G(T, FIS, "Intermediate",
  "According to data released on 1 December 2025, India's gross GST collections for November 2025 were over ₹1.70 "
  "lakh crore. By how much did they grow year-on-year?",
  ["0.7%", "3.2%", "5.4%", "8.9%"], "*",
  "GST collections: November 2025",
  "Gross GST collections rose 0.7% year-on-year to over ₹1.70 lakh crore in November 2025, against about ₹1.69 lakh "
  "crore in November 2024. The modest rise followed the GST rate cuts. Cumulative gross collections for "
  "April-November 2025 grew about 8.9%.",
  ["Nov 2025 gross GST: over ₹1.70 lakh crore", "Growth: 0.7% y-o-y (Nov 2024: ₹1.69 lakh crore)"],
  [fact("Gross GST collections rise 0.7% to over ₹1.70 lakh crore in November; November 2024: ₹1.69 lakh crore "
        "(article of 1 December 2025)", "eco_gstnov_air"),
   fact("Gross GST collection up 0.7 percent to ₹1.70 lakh crore in November; April-November gross collections up "
        "about 8.9%", "eco_gstnov_bt")],
  why="November's growth was 0.7%; 8.9% is the April-November cumulative growth, and the others are not reported.",
  current=ca("2025-12-01"))

G(T, INF, "Intermediate",
  "India's wholesale price (WPI) inflation jumped to a 42-month high in April 2026 (data released on 14 May 2026), "
  "driven mainly by fuel and power prices. What was it?",
  ["8.3%", "3.88%", "5.6%", "7.1%"], "*",
  "WPI inflation: April 2026",
  "Annual WPI inflation rose sharply to 8.3% (provisional) in April 2026 from 3.88% in March 2026, a 42-month high. "
  "The surge came mainly from fuel and power, whose inflation rose to 24.71%; crude petroleum and natural gas "
  "inflation was 67.18%.",
  ["WPI Apr 2026: 8.3% (Mar: 3.88%)", "Fuel and power: 24.71%"],
  [fact("WPI inflation rose sharply to 8.3% in April 2026 from 3.88% in March, driven by fuel and power prices; crude "
        "petroleum and natural gas 67.18%; article of 14 May 2026, 42-month high", "eco_wpiapr_ao"),
   fact("India wholesale inflation WPI April 2026 hits 42-month high of 8.3%; fuel and power 24.71% (14 May 2026)",
        "eco_wpiapr_rw")],
  why="The sources give 8.3% for April 2026; 3.88% was the March figure, and the others are not reported.",
  current=ca("2026-05-14"))

G(T, MON, "Intermediate",
  "On 18 December 2025 the Bank of England's Monetary Policy Committee cut Bank Rate from 4% to 3.75%. By what vote "
  "was the decision taken?",
  ["5-4", "7-2", "6-3", "9-0"], "*",
  "Bank of England: December 2025 decision",
  "At its final meeting of 2025 on 18 December, the Bank of England's Monetary Policy Committee cut Bank Rate by 25 "
  "basis points from 4% to 3.75% by a narrow 5-4 vote; Governor Andrew Bailey's vote fell on the side of the cut.",
  ["Bank Rate: 4% to 3.75%", "Vote: 5-4"],
  [fact("Bank of England MPC cut rates by 25 bps to 3.75% from 4%; vote 5-4; Governor Bailey's vote on the cut side; "
        "18 December 2025", "eco_boe_pp"),
   fact("Bank of England cuts interest rates to 3.75% in tight 5-4 vote", "eco_boe_fr")],
  why="The sources report a 5-4 vote; the other splits are not reported.",
  current=ca("2025-12-18"))

# ------------------------------------------------------------------ Economic Affairs: Advanced (2)
GS(T, INF, "Advanced", "India's retail (CPI) inflation for May 2026, released on 12 June 2026",
   ["Headline inflation on the CPI (base 2024=100) was 3.93% (provisional).",
    "Urban inflation was higher than rural inflation.",
    "Food inflation measured by the Consumer Food Price Index was higher than headline inflation."],
   [True, False, True],
   "CPI inflation: May 2026",
   "MoSPI's release of 12 June 2026 put year-on-year CPI inflation (base 2024=100) for May 2026 at 3.93% "
   "(provisional), with rural inflation at 4.25% and urban at 3.53%, so rural was higher. Food inflation (CFPI) was "
   "4.78%, above headline inflation.",
   [fact("MoSPI press release dated 12 June 2026: CPI (base 2024) inflation for May 2026 3.93% (provisional); rural "
         "4.25%, urban 3.53%; CFPI food inflation 4.78%", "eco_cpimay_pib"),
    fact("India May 2026 CPI inflation 3.93 percent", "eco_cpimay_ziro")],
   why="Statement 2 is wrong: urban inflation (3.53%) was below rural inflation (4.25%).",
   current=ca("2026-06-12"))

GS(T, FIS, "Advanced", "the Centre's fiscal data for April-July 2026, released by the Controller General of Accounts "
   "on 31 August 2026",
   ["The fiscal deficit was about ₹4.55 lakh crore, or 26.8% of the 2026-27 Budget Estimate.",
    "As a share of the Budget Estimate, the deficit was lower than in April-July 2025.",
    "Tax devolution to States was higher than in the same period of the previous year."],
   [True, True, False],
   "CGA monthly accounts: April-July 2026",
   "CGA data released on 31 August 2026 showed the Centre's fiscal deficit at ₹4,55,144 crore in April-July 2026, or "
   "26.8% of the 2026-27 Budget Estimate of ₹16.96 lakh crore (4.3% of GDP), against 29.9% of the Budget Estimate a "
   "year earlier. Devolution to States was ₹3,72,354 crore, ₹56,190 crore less than in the previous year.",
   [fact("CGA data released Monday (article of 31 August 2026): fiscal deficit April-July 2026 ₹4,55,144 crore, 26.8% "
         "of full-year target; 29.9% a year earlier; target 4.3% of GDP or ₹16.96 lakh crore; devolution to states "
         "₹3,72,354 crore, ₹56,190 crore lower than previous year", "eco_cgajul_de"),
    fact("FY27 fiscal deficit stands at Rs 4.55 lakh crore by July, 26.8 pc of target", "eco_cgajul_pio")],
   why="Statement 3 is wrong: devolution to States was ₹56,190 crore lower than a year earlier.",
   current=ca("2026-08-31"))

# ###################################################################### part: pol (schemes + policies)
# ###################################################################### part: pol (Government Schemes + Government Policies)
U.update({
    # ---- Government Schemes
    "pol_vidya_etv": ("https://etvbharat.com/en/!bharat/cabinet-approves-pm-vidyalaxmi-scheme-to-provide-financial-"
                      "support-to-meritorious-students-enn24110604100", OPENED),
    "pol_vidya_bs": ("https://business-standard.com/amp/india-news/pm-vidyalaxmi-scheme-approved-to-provide-collateral-"
                     "free-student-loans-124110601320_1.html", SEARCH),
    "pol_onos_trib": ("https://tribuneindia.com/news/cabinet-approves-one-nation-one-subscription-scheme-for-access-to-"
                      "research-articles-journals", OPENED),
    "pol_onos_etv": ("https://etvbharat.com/en/!bharat/cabinet-approves-one-nation-one-subscription-enn24112506913",
                     SEARCH),
    "pol_nmnf_itv": ("https://www.indiatvnews.com/news/india/cabinet-approves-national-mission-on-natural-farming-what-"
                     "is-it-2024-11-25-963398", OPENED),
    "pol_nmnf_rv": ("https://eng.ruralvoice.in/cabinet-approved-2481-crore-national-mission-on-natural-farming", SEARCH),
    "pol_pmfby_air": ("https://www.newsonair.gov.in/wild-animal-attacks-paddy-inundation-to-be-covered-under-pmfby-from-"
                      "kharif-2026/", OPENED),
    "pol_pmfby_st": ("https://www.thestatesman.com/business/relief-for-farmers-wild-animal-attack-paddy-inundation-"
                     "included-under-localised-risk-cover-1503514118.html", SEARCH),
    "pol_rgm_air": ("https://newsonair.gov.in/centre-approves-revised-rashtriya-gokul-mission-to-boost-growth-in-"
                    "livestock-sector/", OPENED),
    "pol_rgm_nm": ("https://www.narendramodi.in/cabinet-approves-implementation-of-revised-rashtriya-gokul-mission-with-"
                   "enhanced-allocation-for-the-years-2024-25-and-2025-26-591847", SEARCH),
    "pol_nbs_air": ("https://newsonair.gov.in/govt-approves-nutrient-based-subsidy-rates-for-kharif-season-2026-on-"
                    "phosphatic-and-potassic-fertilisers/", OPENED),
    "pol_star_pfrda": ("https://www.pfrda.org.in/documents/33652/86710/Press+Release+StAR+NPS+Bengaluru.pdf", OPENED),
    "pol_star_page": ("https://www.pfrda.org.in/w/press-release-star-nps-taking-nps-distribution-across-every-"
                      "socioeconomic-stratum", OPENED),
    "pol_cab_pfrda": ("https://www.pfrda.org.in/documents/33652/86710/Press+Release+-Government+Extends+Additional+NPS+"
                      "Investment.pdf", OPENED),
    "pol_sanchay_pfrda": ("https://www.pfrda.org.in/documents/33652/726954/Clarification+regarding+applicability+of+"
                          "incentive+to+PoPs+for+NPS+enrolment+facilitated+through+FPOs+vide+Circular+No.+"
                          "PFRDA202523NPS-AGRI01+dated+15th+December%2C+2025+-+extension+to+NPS.pdf", OPENED),
    "pol_pss_air": ("https://newsonair.gov.in/centre-approves-%E2%82%B95547-99-crore-procurement-at-msp-for-pulses-"
                    "oilseeds-in-three-states/", OPENED),
    "pol_edrive_acp1": ("https://www.autocarpro.in/news/pm-e-drive-scheme-extended-till-fy28-end-e2ws-e3ws-subsidies-to-"
                        "end-in-fy26-end-127971", OPENED),
    "pol_edrive_acp2": ("https://www.autocarpro.in/news/govt-extends-pm-e-drive-subsidy-for-e2ws-till-july-e3w-to-get-"
                        "incentives-till-2028-131843", OPENED),
    # ---- Government Policies
    "pol_nom_trib": ("https://www.tribuneindia.com/news/business/now-bank-customers-can-opt-for-four-nominees-in-"
                     "accounts-from-nov-1", OPENED),
    "pol_nom_ao": ("https://www.angelone.in/news/personal-finance/banking-laws-amendment-act-2025-new-nomination-rules-"
                   "effective-november-1-2025", SEARCH),
    "pol_saha_rbi": ("https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=62870", OPENED),
    "pol_khelo_dc": ("https://www.deccanchronicle.com/nation/cabinet-approves-khelo-bharat-niti-aims-to-make-india-top-5-"
                     "sporting-nations-1888636", OPENED),
    "pol_apr_rbi": ("https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=62516", OPENED),
    "pol_sahayak_pfrda": ("https://www.pfrda.org.in/w/pfrda-launches-ai-powered-pfrda-pension-sahayak-portal-to-"
                          "transform-pension-grievance-redressal-1", OPENED),
    "pol_visa_air": ("https://newsonair.gov.in/govt-relaxes-passport-and-visa-rules-for-several-categories-of-foreign-"
                     "nationals-residing-in-india/", OPENED),
    "pol_dicgc_rbi": ("https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=62183", OPENED),
    "pol_gold_rbi": ("https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12859", OPENED),
    "pol_feb_rbi": ("https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=62171", OPENED),
    "pol_demat_sebi": ("https://www.sebi.gov.in/media-and-notifications/press-releases/sep-2026/successful-launch-of-"
                       "demat-2-0-pilot-project-for-tokenised-corporate-bonds_104418.html", OPENED),
    "pol_demat_faq": ("https://www.sebi.gov.in/sebi_data/faqfiles/sep-2026/1789049630065.pdf", OPENED),
})

T = "Government Schemes"
CS, SL = "Central schemes", "Scheme launches and changes"

# ------------------------------------------------------------------ Schemes: Basic (1)
G(T, CS, "Basic",
  "The PM-Vidyalaxmi scheme, approved by the Union Cabinet on 6 November 2024, mainly provides which of the following?",
  ["Collateral-free and guarantor-free education loans to students admitted to quality higher education institutions",
   "A monthly stipend to girl students pursuing science and engineering courses",
   "Free digital devices to students of government higher secondary schools",
   "Interest-free loans to student-led start-ups incubated in universities"], "*",
  "PM-Vidyalaxmi: education loans",
  "PM-Vidyalaxmi, a Central Sector scheme of the Department of Higher Education, lets meritorious students admitted to "
  "quality higher education institutions (QHEIs) get collateral-free and guarantor-free education loans from banks. "
  "Loans up to ₹7.5 lakh carry a 75% credit guarantee, and students with family income up to ₹8 lakh get 3% interest "
  "subvention during the moratorium on loans up to ₹10 lakh. Applications go through the unified 'PM-Vidyalaxmi' "
  "portal; the outlay is ₹3,600 crore for 2024-25 to 2030-31.",
  ["PM-Vidyalaxmi: approved 6 Nov 2024", "Collateral-free, guarantor-free education loans for QHEI students",
   "75% guarantee up to ₹7.5 lakh; 3% subvention (income up to ₹8 lakh)"],
  [fact("Cabinet approved PM-Vidyalaxmi on Wednesday 6 November 2024; 75% credit guarantee on loans up to ₹7.5 lakh; 3% "
        "interest subvention for family income up to ₹8 lakh on loans up to ₹10 lakh; ₹3,600 crore for 2024-25 to "
        "2030-31; 860 QHEIs; unified 'PM-Vidyalaxmi' portal; Department of Higher Education", "pol_vidya_etv"),
   fact("PM-Vidyalaxmi scheme approved to provide collateral-free student loans", "pol_vidya_bs")],
  why="The sources describe PM-Vidyalaxmi only as a collateral-free, guarantor-free education loan scheme; it does not "
      "provide stipends, devices or start-up loans.",
  current=ca("2024-11-06"))

# ------------------------------------------------------------------ Schemes: Intermediate (10)
G(T, CS, "Intermediate",
  "Under the 'One Nation One Subscription' scheme approved by the Union Cabinet in November 2024, which agency "
  "coordinates the national subscription to international scholarly journals?",
  ["INFLIBNET (Information and Library Network)", "National Informatics Centre (NIC)",
   "Anusandhan National Research Foundation (ANRF)", "National Digital Library of India (NDLI)"], "*",
  "One Nation One Subscription",
  "One Nation One Subscription (ONOS) is a new Central Sector Scheme with about ₹6,000 crore for the calendar years "
  "2025, 2026 and 2027. It gives over 6,300 government higher education and Central government R&D institutions "
  "access to nearly 13,000 e-journals of 30 international publishers. The subscription is coordinated centrally by "
  "INFLIBNET, an autonomous inter-university centre of the UGC.",
  ["ONOS: ~₹6,000 crore for 2025-2027", "30 publishers, ~13,000 e-journals, 6,300+ institutions",
   "Coordinator: INFLIBNET (UGC inter-university centre)"],
  [fact("Cabinet approved ONOS (article of 26 Nov 2024, decision 'on Monday'); about ₹6,000 crore for 2025, 2026, 2027; "
        "30 publishers; ~13,000 e-journals; 6,300+ institutions; coordinated by INFLIBNET, an autonomous inter-university "
        "centre of UGC", "pol_onos_trib"),
   fact("Cabinet approves One Nation One Subscription", "pol_onos_etv")],
  why="The sources name INFLIBNET as the coordinating agency; NIC, ANRF and NDLI are not given this role.",
  current=ca("2024-11-25", inferred="Tribune report of 26 Nov 2024 says the Cabinet approved it on Monday"))

G(T, CS, "Intermediate",
  "What is the total outlay of the National Mission on Natural Farming (NMNF), approved by the Union Cabinet on 25 "
  "November 2024 as a standalone Centrally Sponsored Scheme?",
  ["₹2,481 crore", "₹1,584 crore", "₹3,400 crore", "₹6,000 crore"], "*",
  "National Mission on Natural Farming",
  "The NMNF, under the Ministry of Agriculture and Farmers' Welfare, has a total outlay of ₹2,481 crore up to 2025-26 "
  "(the 15th Finance Commission period). The Centre's share is ₹1,584 crore and the States' share ₹897 crore.",
  ["NMNF total: ₹2,481 crore", "Centre ₹1,584 crore + States ₹897 crore"],
  [fact("Cabinet approved NMNF on Monday 25 November 2024; total outlay ₹2,481 crore; Centre ₹1,584 crore, States ₹897 "
        "crore till 2025-26; Ministry of Agriculture & Farmers' Welfare", "pol_nmnf_itv"),
   fact("Cabinet approved ₹2,481 crore National Mission on Natural Farming", "pol_nmnf_rv")],
  why="₹1,584 crore is only the Centre's share; the total outlay given by the sources is ₹2,481 crore.",
  current=ca("2024-11-25"))

G(T, SL, "Intermediate",
  "From the Kharif 2026 season, crop losses caused by wild animal attacks are covered under the Pradhan Mantri Fasal "
  "Bima Yojana (PMFBY) as the fifth add-on cover under which risk category?",
  ["Localised risk", "Prevented sowing", "Mid-season adversity", "Post-harvest losses"], "*",
  "PMFBY: new risk covers",
  "The Agriculture Ministry announced in November 2025 that from Kharif 2026, crop loss from wild animal attacks will be "
  "the fifth add-on cover under the Localised Risk category of PMFBY. States will notify the wild animals and the "
  "vulnerable districts, and farmers must report losses within 72 hours through the Crop Insurance App with geotagged "
  "photographs. Paddy inundation has also been brought back as a localised calamity cover.",
  ["Wild animal attack: 5th add-on cover under Localised Risk", "From Kharif 2026; report within 72 hours",
   "Paddy inundation restored as localised calamity cover"],
  [fact("Article of 18 Nov 2025: wild animal attack becomes fifth add-on cover under the Localised Risk category of PMFBY "
        "from Kharif 2026; States notify animals; report within 72 hours via Crop Insurance App with geotagged photos; "
        "paddy inundation reintroduced as localised calamity cover", "pol_pmfby_air"),
   fact("Wild animal attack, paddy inundation included under 'Localised Risk' cover", "pol_pmfby_st")],
  why="The sources place the new cover under the Localised Risk category, not under the other risk categories.",
  current=ca("2025-11-18"))

G(T, SL, "Intermediate",
  "In March 2025 the Union Cabinet approved a revised Rashtriya Gokul Mission with an additional ₹1,000 crore. What is "
  "its total allocation during the 15th Finance Commission cycle (2021-22 to 2025-26)?",
  ["₹3,400 crore", "₹2,400 crore", "₹1,000 crore", "₹4,400 crore"], "*",
  "Rashtriya Gokul Mission",
  "The revised Rashtriya Gokul Mission, meant to raise milk production and productivity and farmers' incomes, got an "
  "additional outlay of ₹1,000 crore. This takes its total allocation to ₹3,400 crore for the 15th Finance Commission "
  "cycle.",
  ["Additional outlay: ₹1,000 crore (March 2025)", "Total for 15th FC cycle: ₹3,400 crore"],
  [fact("Article of 20 Mar 2025: Cabinet decision briefed 'last evening'; revised Rashtriya Gokul Mission with additional "
        "outlay of ₹1,000 crore", "pol_rgm_air"),
   fact("Cabinet approves revised Rashtriya Gokul Mission with enhanced allocation; total allocation of ₹3,400 crore "
        "during the 15th Finance Commission cycle", "pol_rgm_nm")],
  why="₹1,000 crore is only the additional amount; the sources give the total allocation as ₹3,400 crore.",
  current=ca("2025-03-19", inferred="newsonair report of 20 Mar 2025 says the decision was briefed 'last evening'"))

G(T, CS, "Intermediate",
  "Under the incentive scheme for low-value BHIM-UPI person-to-merchant transactions approved by the Union Cabinet in "
  "March 2025, an incentive of 0.15% of the transaction value is given for transactions with small merchants up to "
  "what amount?",
  ["₹2,000", "₹500", "₹5,000", "₹10,000"], "*",
  "UPI incentive scheme",
  "Along with the revised Rashtriya Gokul Mission, the Union Cabinet approved in March 2025 an incentive scheme to "
  "promote low-value BHIM-UPI person-to-merchant transactions. Transactions of up to ₹2,000 with small merchants carry "
  "an incentive of 0.15% of the transaction value.",
  ["Low-value BHIM-UPI P2M incentive", "0.15% of transaction value", "Transactions up to ₹2,000, small merchants"],
  [fact("Article of 20 Mar 2025 on Cabinet decisions: UPI incentive of 0.15% of transaction value for small-merchant "
        "transactions up to ₹2,000", "pol_rgm_air")],
  why="The source gives ₹2,000 as the ceiling for the 0.15% incentive; the other amounts are not the limit.",
  current=ca("2025-03-19", inferred="newsonair report of 20 Mar 2025 says the decisions were briefed 'last evening'"))

G(T, SL, "Intermediate",
  "On 8 April 2026 the government approved Nutrient Based Subsidy (NBS) rates on phosphatic and potassic fertilisers "
  "for the Kharif 2026 season. What is the tentative budgetary requirement for the season?",
  ["About ₹41,533 crore", "About ₹24,000 crore", "About ₹62,500 crore", "About ₹1,00,000 crore"], "*",
  "Nutrient Based Subsidy scheme",
  "Under the Nutrient Based Subsidy scheme, the government fixes per-nutrient subsidy rates for phosphatic and potassic "
  "(P&K) fertilisers each season so that farmers get them at affordable prices. For Kharif 2026, the tentative budget "
  "is about ₹41,533 crore. The decision was briefed by I&B Minister Ashwini Vaishnaw on 8 April 2026.",
  ["NBS: P&K fertilisers", "Kharif 2026 budget: ~₹41,533 crore", "Approved 8 Apr 2026"],
  [fact("Article of 8 April 2026: government approved NBS rates for Kharif 2026 on phosphatic and potassic fertilisers; "
        "tentative budget about ₹41,533 crore; briefed by Ashwini Vaishnaw", "pol_nbs_air")],
  why="The source gives about ₹41,533 crore as the Kharif 2026 NBS requirement; the other figures are not stated.",
  current=ca("2026-04-08"))

G(T, SL, "Intermediate",
  "StAR NPS, which the PFRDA urged mutual fund distributors to use at an event in Bengaluru on 24 October 2026, is a "
  "digital distribution platform for the National Pension System developed with the support of which entity?",
  ["BSE Technologies Private Limited", "Computer Age Management Services (CAMS)", "KFin Technologies",
   "National Payments Corporation of India"], "*",
  "NPS distribution: StAR NPS",
  "StAR NPS is PFRDA's digital distribution platform for NPS. Developed with BSE Technologies Private Limited (BTPL), it "
  "lets distributors move between mutual fund products and NPS. Mutual fund distributors, PACS, banking "
  "correspondents, NBFCs and other eligible entities can distribute NPS through it, and PFRDA has envisaged a higher "
  "incentive for distributors using it. PFRDA said it would work with BTPL to give distributors efficiencies comparable "
  "to those of registrar and transfer agents such as CAMS and KFin Technologies.",
  ["StAR NPS: digital NPS distribution platform", "Developed with BSE Technologies (BTPL)",
   "Open to MFDs, PACS, BCs, NBFCs"],
  [fact("Bengaluru, 24 October 2026: PFRDA called on MFDs to use StAR NPS, its digital distribution platform, developed "
        "with the support of BSE Technologies Private Limited; CAMS and KFin Technologies mentioned as RTAs for "
        "comparison", "pol_star_pfrda"),
   fact("PFRDA press release 'StAR NPS: Taking NPS Distribution Across Every Socioeconomic Stratum', published "
        "28-10-2026", "pol_star_page")],
  why="The source names BSE Technologies as the developer; CAMS and KFin are mentioned only as registrar and transfer "
      "agents for comparison, and NPCI is not mentioned.",
  current=ca("2026-10-24"))

G(T, SL, "Intermediate",
  "In July 2026 the Government extended two additional NPS investment choices, the Aggressive Life Cycle Fund (LC-75, "
  "now LC-75-High) and the Balanced Life Cycle Fund (BLC), to the NPS subscribers of which group?",
  ["Employees of Central Autonomous Bodies", "Employees of State Governments",
   "Subscribers under the All Citizen model", "Members of the armed forces"], "*",
  "NPS: investment choices",
  "The Department of Expenditure, Ministry of Finance, extended a Department of Financial Services notification of 13 "
  "November 2025 to employees of Central Autonomous Bodies (CABs) covered under NPS. These choices had earlier been "
  "given to Central Government employees. LC-75 (now LC-75-High) allows equity of up to 75%; BLC has equity capped at "
  "50%, with equity reduced gradually from age 45.",
  ["Released 7 July 2026 (Ministry of Finance)", "Extended to: Central Autonomous Body employees",
   "LC-75: equity up to 75%; BLC: equity up to 50%, tapering from 45"],
  [fact("PIB release of 07 Jul 2026 (Ministry of Finance): two additional NPS investment choices, LC-75 and BLC, earlier "
        "for Central Government employees, extended to employees of Central Autonomous Bodies; DFS notification of 13 "
        "November 2025", "pol_cab_pfrda")],
  why="The source says the choices, earlier given to Central Government employees, were extended to employees of "
      "Central Autonomous Bodies; the other groups are not mentioned.",
  current=ca("2026-07-07"))

G(T, SL, "Intermediate",
  "Under a PFRDA circular of 15 December 2025, later applied to NPS Sanchay (formally launched on 6 May 2026), what "
  "incentive does a Point of Presence (PoP) get for each NPS enrolment facilitated through Farmer Producer "
  "Organisations (FPOs)?",
  ["₹100 per subscriber", "₹50 per subscriber", "₹200 per subscriber", "₹500 per subscriber"], "*",
  "NPS outreach: NPS Sanchay",
  "PFRDA's December 2025 circular introduced an incentive of ₹100 per subscriber for PoPs for NPS enrolments through "
  "FPOs engaged as Pension Agents, valid till 31 March 2027. After NPS Sanchay was launched on 6 May 2026, a May 2026 "
  "circular extended the same ₹100 incentive to enrolments through CSC-VLEs, Business Correspondents/Pension Sakhis "
  "and PACS. An October 2026 clarification said the FPO incentive applies to opening NPS Sanchay accounts.",
  ["Dec 2025: ₹100/subscriber to PoPs for FPO-facilitated enrolment", "NPS Sanchay launched 6 May 2026",
   "Valid till 31 March 2027"],
  [fact("PFRDA circular of 8 October 2026: the December 2025 circular introduced ₹100 per subscriber incentive to PoPs "
        "for NPS enrolment through FPOs, valid till 31 March 2027; NPS Sanchay formally launched on 6 May 2026; May 2026 "
        "circular extended ₹100 to CSC-VLEs, BCs/Pension Sakhis and PACS", "pol_sanchay_pfrda")],
  why="The circular fixes the incentive at ₹100 per subscriber; the other amounts are not stated.",
  current=ca("2026-10-08"))

G(T, CS, "Intermediate",
  "On 30 September 2026 the Centre approved procurement worth ₹5,547.99 crore under the Price Support Scheme for "
  "Kharif Marketing Season 2026-27 in Uttar Pradesh, Karnataka and Telangana. Which crop accounts for the largest "
  "share of this amount?",
  ["Tur, in Uttar Pradesh", "Soybean, in Karnataka", "Moong, in Karnataka", "Soybean, in Telangana"], "*",
  "Price Support Scheme",
  "Under the Price Support Scheme, the Centre buys pulses and oilseeds at MSP when market prices fall. Of the ₹5,547.99 "
  "crore approved for KMS 2026-27, procurement of 4.66 lakh MT of tur in Uttar Pradesh accounts for ₹3,937.70 crore. "
  "Soybean in Karnataka (₹659.27 crore), soybean in Telangana (₹353.90 crore) and moong in Karnataka (₹335.83 crore) "
  "are much smaller.",
  ["Total: ₹5,547.99 crore (UP, Karnataka, Telangana)", "UP tur: 4.66 lakh MT, ₹3,937.70 crore (largest)"],
  [fact("Article of 30 Sep 2026: ₹5,547.99 crore PSS procurement for KMS 2026-27; UP tur 4.66 lakh MT ₹3,937.70 crore; "
        "Karnataka soybean ₹659.27 crore, moong ₹335.83 crore; Telangana soybean ₹353.90 crore", "pol_pss_air")],
  why="The source's figures show UP tur (₹3,937.70 crore) far ahead of soybean and moong in the other States.",
  current=ca("2026-09-30"))

# ------------------------------------------------------------------ Schemes: Advanced (1)
GS(T, SL, "Advanced",
   "the PM E-DRIVE scheme",
   ["Its terminal date was extended from 31 March 2026 to 31 March 2028, with the total outlay kept at ₹10,900 crore.",
    "It is administered by the Ministry of Heavy Industries.",
    "Under the amendment reported in March 2026, demand incentives for electric two-wheelers were extended up to 31 "
    "March 2028."],
   [True, True, False],
   "PM E-DRIVE: extensions",
   "The Ministry of Heavy Industries extended PM E-DRIVE by two years, to 31 March 2028, without raising its fund-limited "
   "outlay of ₹10,900 crore. A later amendment, reported on 28 March 2026, extended e-two-wheeler demand incentives only "
   "to 31 July 2026, while e-three-wheeler incentives continue for registrations up to 31 March 2028.",
   [fact("Article of 8 Aug 2025: Ministry of Heavy Industries; scheme extended from 31 March 2026 to 31 March 2028; outlay "
         "₹10,900 crore; fund-limited", "pol_edrive_acp1"),
    fact("Article of 28 March 2026: e-2W subsidy extended from 31 March 2026 to 31 July 2026; e-3W incentives to 31 March "
         "2028; outlay ₹10,900 crore", "pol_edrive_acp2")],
   why="Statement 3 is wrong: the March 2026 amendment extended e-two-wheeler incentives only to 31 July 2026; 31 March "
       "2028 applies to e-three-wheelers.",
   current=ca("2026-03-28", inferred="Autocar Pro report dated 28 Mar 2026; notification date not stated"))

T = "Government Policies"
PC, RR = "Policy changes", "Regulatory reforms"

# ------------------------------------------------------------------ Policies: Basic (5)
G(T, RR, "Basic",
  "Under the Banking Laws (Amendment) Act, 2025, whose nomination provisions took effect on 1 November 2025, up to how "
  "many nominees can a bank depositor name?",
  ["Four", "Two", "Three", "Five"], "*",
  "Banking Laws (Amendment) Act, 2025: nomination",
  "The Finance Ministry said the nomination provisions of the Banking Laws (Amendment) Act, 2025 (notified on 15 April "
  "2025) would take effect from 1 November 2025. Depositors may name up to four nominees, simultaneously or "
  "successively, and fix each nominee's share. For articles in safe custody and safety lockers only successive "
  "nomination is allowed.",
  ["Up to 4 nominees from 1 Nov 2025", "Deposits: simultaneous or successive", "Lockers/safe custody: successive only"],
  [fact("PTI report of 24 Oct 2025: from 1 November 2025, depositors can name up to four nominees, simultaneous or "
        "successive; lockers and safe custody only successive; Act notified 15 April 2025", "pol_nom_trib"),
   fact("Banking Laws (Amendment) Act 2025: new nomination rules effective November 1, 2025", "pol_nom_ao")],
  why="The sources give the limit as four nominees.",
  current=ca("2025-11-01"))

G(T, RR, "Basic",
  "In June 2026 the RBI recognised which entity as the Self-Regulatory Organisation (SRO) for the Account Aggregator "
  "ecosystem?",
  ["Sahamati Foundation", "Fintech Association for Consumer Empowerment (FACE)", "National Payments Corporation of India",
   "Indian Banks' Association"], "*",
  "RBI: SRO for Account Aggregators",
  "In a press release of 5 June 2026, the RBI said it had recognised Sahamati Foundation as the SRO for the Account "
  "Aggregator ecosystem. Its application was examined under the RBI's 'Framework for recognising SROs for the Account "
  "Aggregator Ecosystem' of 12 March 2025.",
  ["SRO-AA: Sahamati Foundation (5 June 2026)", "Framework dated 12 March 2025"],
  [fact("RBI press release of 5 June 2026: Sahamati Foundation recognised as SRO for the Account Aggregator ecosystem "
        "under the framework of 12 March 2025", "pol_saha_rbi")],
  why="The RBI release names Sahamati Foundation; the other bodies were not recognised as the SRO for Account "
      "Aggregators.",
  current=ca("2026-06-05"))

G(T, PC, "Basic",
  "Khelo Bharat Niti 2025, the national sports policy approved by the Union Cabinet on 1 July 2025, replaces the "
  "National Sports Policy of which year?",
  ["2001", "1984", "2007", "2011"], "*",
  "Khelo Bharat Niti 2025",
  "The Union Cabinet approved Khelo Bharat Niti 2025 on 1 July 2025 in place of the National Sports Policy, 2001. It "
  "aims to make India a top-five sporting nation by 2047 and a strong contender at events including the 2036 "
  "Olympics. Its five pillars include excellence on the global stage, sports for economic and social development, "
  "sports as a people's movement and integration with education (NEP 2020).",
  ["Khelo Bharat Niti: 1 July 2025", "Replaces National Sports Policy 2001", "Goal: top five by 2047"],
  [fact("Cabinet approved Khelo Bharat Niti on Tuesday 1 July 2025; replaces the National Sports Policy of 2001; top-five "
        "sporting nation by 2047; 2036 Olympics; five pillars", "pol_khelo_dc")],
  why="The source says the new policy replaces the National Sports Policy of 2001.",
  current=ca("2025-07-01"))

G(T, RR, "Basic",
  "In its Statement on Developmental and Regulatory Policies of 8 April 2026, the RBI proposed dropping which "
  "requirement for commercial banks (other than Small Finance Banks, Payments Banks and RRBs), since they already hold "
  "capital for market risk?",
  ["Investment Fluctuation Reserve", "Capital Conservation Buffer", "Statutory Liquidity Ratio",
   "Liquidity Coverage Ratio"], "*",
  "RBI: April 2026 regulatory measures",
  "On 8 April 2026 the RBI proposed removing the Investment Fluctuation Reserve (IFR) requirement for commercial banks, "
  "including Local Area Banks but excluding Small Finance Banks, Payments Banks and RRBs, as they already maintain "
  "capital charges for market risk and follow revised investment norms. It also proposed letting banks count quarterly "
  "profits towards CRAR without the earlier provisioning-deviation condition.",
  ["Proposal: drop IFR for commercial banks", "Reason: market-risk capital charge already held",
   "Draft directions to follow"],
  [fact("RBI Statement on Developmental and Regulatory Policies, 8 April 2026: proposes dropping the IFR requirement for "
        "commercial banks including LABs, excluding SFBs, PBs and RRBs, as they hold market-risk capital charges",
        "pol_apr_rbi")],
  why="The statement names the Investment Fluctuation Reserve; the other requirements are not part of this proposal.",
  current=ca("2026-04-08"))

G(T, RR, "Basic",
  "'PFRDA Pension Sahayak', launched by the Pension Fund Regulatory and Development Authority in June 2026, is an "
  "AI-powered portal for what purpose?",
  ["Pension grievance redressal", "Opening NPS accounts for minors", "Submitting digital life certificates",
   "Comparing returns of pension fund managers"], "*",
  "PFRDA: grievance redressal",
  "On 22 June 2026 the PFRDA announced the launch of 'PFRDA Pension Sahayak', an AI-powered portal meant to transform "
  "pension grievance redressal.",
  ["PFRDA Pension Sahayak: 22 June 2026", "AI-powered pension grievance redressal portal"],
  [fact("PFRDA press release of 22-06-2026: 'PFRDA Launches AI-Powered PFRDA Pension Sahayak Portal to Transform Pension "
        "Grievance Redressal'", "pol_sahayak_pfrda")],
  why="The PFRDA release describes the portal only as a grievance redressal platform.",
  current=ca("2026-06-22"))

# ------------------------------------------------------------------ Policies: Intermediate (1)
G(T, PC, "Intermediate",
  "Under the Immigration and Foreigners (Exemption) Order as amended in November 2026, Hindu, Sikh, Buddhist, Jain, "
  "Parsi and Christian migrants from Afghanistan, Bangladesh and Pakistan who sought shelter in India due to religious "
  "persecution are covered if they entered India on or before which date?",
  ["31 December 2024", "31 December 2014", "31 December 2009", "9 January 2015"], "*",
  "Immigration: exemption order",
  "The Home Ministry published the Immigration and Foreigners (Exemption) (Amendment) Order, 2026 in the Official "
  "Gazette. It covers persecuted minority migrants from Afghanistan, Bangladesh and Pakistan who entered on or before 31 "
  "December 2024 (they must obtain an appropriate visa for continued stay), registered Sri Lankan Tamils who took "
  "shelter up to 9 January 2015, and certain persons who returned on or before 31 December 2009. It also adds a "
  "definition of the Visa Manual.",
  ["Persecuted minorities (Afghanistan, Bangladesh, Pakistan): entry by 31 Dec 2024",
   "Sri Lankan Tamils: shelter up to 9 Jan 2015", "Some other categories: 31 Dec 2009"],
  [fact("newsonair, 6 Nov 2026: MHA published the Immigration and Foreigners (Exemption) (Amendment) Order, 2026; "
        "minority migrants from Afghanistan, Bangladesh and Pakistan who entered on or before 31 December 2024; Sri "
        "Lankan Tamils up to 9 January 2015; other categories 31 December 2009", "pol_visa_air")],
  why="31 December 2024 is the cut-off for these migrants; 9 January 2015 applies to Sri Lankan Tamils and 31 December "
      "2009 to certain other categories in the same order.",
  current=ca("2026-11-06", inferred="newsonair report dated 6 Nov 2026; gazette date not stated"))

# ------------------------------------------------------------------ Policies: Advanced (4)
GS(T, RR, "Advanced",
   "the risk-based deposit insurance premium framework announced by DICGC with RBI approval on 6 February 2026",
   ["It applies from 1 April 2026, with the flat card rate of 12 paise per ₹100 of assessable deposits as the reference.",
    "Payments Banks and Local Area Banks are assessed under the Tier 2 model used for RRBs and co-operative banks.",
    "Banks with a long record of contributing to the Deposit Insurance Fund without major distress can get a vintage "
    "incentive of up to 25%."],
   [True, False, True],
   "Deposit insurance: risk-based premium",
   "DICGC's risk-based premium framework replaces the flat premium from 1 April 2026; the card rate is 12 paise per ₹100 "
   "of assessable deposits. Scheduled commercial banks other than RRBs are rated under a Tier 1 model, and RRBs and "
   "co-operative banks under a Tier 2 model. Local Area Banks and Payments Banks, and UCBs under SAF/PCA, stay at the "
   "card rate. A vintage incentive of up to 25% rewards a long, claim-free record.",
   [fact("RBI/DICGC release of 6 Feb 2026: effective 1 April 2026; card rate 12 paise per ₹100 AD; Tier 1 for SCBs "
         "other than RRBs, Tier 2 for RRBs and co-operative banks; LABs and Payments Banks remain at card rate; vintage "
         "incentive up to 25%", "pol_dicgc_rbi")],
   why="Statement 2 is wrong: Local Area Banks and Payments Banks remain at the card rate and are not rated under the "
       "Tier 2 model.",
   current=ca("2026-02-06"))

GS(T, RR, "Advanced",
   "the RBI (Lending Against Gold and Silver Collateral) Directions, 2025, to be complied with by 1 April 2026",
   ["For consumption loans totalling up to ₹2.5 lakh per borrower, the loan-to-value ratio may be up to 85%.",
    "The aggregate weight of silver ornaments pledged by one borrower cannot exceed 10 kg.",
    "Lenders may lend against silver bullion of up to 500 grams per borrower."],
   [True, True, False],
   "RBI: gold and silver loans",
   "The Directions, issued on 6 June 2025 and to be adopted by 1 April 2026 at the latest, set LTV caps of 85% (up to "
   "₹2.5 lakh), 80% (above ₹2.5 lakh to ₹5 lakh) and 75% (above ₹5 lakh). Per borrower, pledged collateral is capped at "
   "1 kg of gold ornaments, 10 kg of silver ornaments, 50 g of gold coins and 500 g of silver coins. Lending against "
   "primary gold or silver such as bullion is not allowed.",
   [fact("RBI Master Direction (issued 6 June 2025): comply no later than 1 April 2026; LTV 85% up to ₹2.5 lakh, 80% up "
         "to ₹5 lakh, 75% above; limits 1 kg gold ornaments, 10 kg silver ornaments, 50 g gold coins, 500 g silver "
         "coins; no lending against primary gold or silver (bullion)", "pol_gold_rbi")],
   why="Statement 3 is wrong: lending against bullion is not allowed; 500 g is the cap for silver coins.",
   current=ca("2026-04-01"))

GS(T, RR, "Advanced",
   "the RBI's Statement on Developmental and Regulatory Policies of 6 February 2026",
   ["The limit for collateral-free loans to micro and small enterprises was raised from ₹10 lakh to ₹20 lakh for loans "
    "sanctioned or renewed on or after 1 April 2026.",
    "It proposed exempting from registration Type I NBFCs that do not use public funds, have no customer interface and "
    "have assets of up to ₹1,000 crore.",
    "Mission SAKSHAM was announced as a capacity-building and certification framework for urban co-operative banks."],
   [True, True, True],
   "RBI: February 2026 regulatory measures",
   "The 6 February 2026 statement raised the collateral-free loan limit for MSEs from ₹10 lakh to ₹20 lakh (from 1 April "
   "2026), proposed registration exemption for small Type I NBFCs (assets up to ₹1,000 crore, no public funds, no "
   "customer interface), and announced Mission SAKSHAM (Sahakari Bank Kshamta Nirman) for about 1.40 lakh participants "
   "of urban co-operative banks. It also proposed letting banks lend to REITs and extending KCC tenure to six years.",
   [fact("RBI Statement on Developmental and Regulatory Policies, 6 Feb 2026: MSE collateral-free limit ₹10 lakh to ₹20 "
         "lakh for loans on or after 1 April 2026; exemption for Type I NBFCs with assets up to ₹1,000 crore; Mission "
         "SAKSHAM for UCBs (~1.40 lakh participants); bank lending to REITs and KCC tenure of six years proposed",
         "pol_feb_rbi")],
   why="All three statements match the RBI statement of 6 February 2026.",
   current=ca("2026-02-06"))

GS(T, RR, "Advanced",
   "SEBI's 'Demat 2.0' pilot for tokenised corporate bonds, launched in September 2026",
   ["A tokenised bond under the pilot is a new asset class outside the Securities Contracts (Regulation) Act, 1956 and "
    "gets a fresh ISIN.",
    "The depositories hold and manage the private keys of Demat 2.0 accounts on behalf of investors.",
    "The funds leg is settled in CBDC (e₹), so that the bond and the payment move together as atomic "
    "delivery-versus-payment."],
   [False, True, True],
   "SEBI: tokenised corporate bonds",
   "SEBI announced the launch of the Demat 2.0 pilot on 10 September 2026. Corporate bonds are issued as native digital "
   "tokens on a permissioned DLT network owned by the depositories, but remain securities under the SCRA, 1956 with the "
   "same ISIN, terms and rights. The Demat 2.0 account extends the investor's existing demat account, the depositories "
   "manage the private keys, and settlement uses CBDC wallets so that both legs settle atomically.",
   [fact("SEBI press release PR No. 56/2026 of 10 September 2026: 'Successful launch of Demat 2.0 Pilot project for "
         "Tokenised Corporate Bonds'", "pol_demat_sebi"),
    fact("SEBI FAQs on Demat 2.0: tokenised bond remains a security under SCRA 1956 with the same ISIN, not a new asset "
         "class; depositories hold and manage private keys; CBDC (e₹) used for funds leg; atomic DvP", "pol_demat_faq")],
   why="Statement 1 is wrong: SEBI says the tokenised bond remains a security under the SCRA with the same ISIN.",
   current=ca("2026-09-10"))


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
    "notes": "BATCH_008 General Awareness part: 149 original questions. Current-affairs topics (National and "
             "International Current Affairs, Appointments, Awards, Sports, Summits, Economic Affairs, Business) test "
             "events dated 2025-11-01 to 2026-11-04, with event dates from the sources and review_by 2027-05-05. "
             "Other time-sensitive facts also carry current_affairs dates. No fact or event tested in BATCH_000 to "
             "BATCH_007 GA is tested again. Fact checks dated 2026-11-06 (the day the pages were checked); verified_by says whether each question's "
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
