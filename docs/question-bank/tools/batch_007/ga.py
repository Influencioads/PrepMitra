"""Writes batches/parts/BATCH_007_GA.json: the 150 General Awareness questions of BATCH_007.

Same structure as tools/batch_006/ga.py. Current-affairs topics (National and International Current Affairs,
Appointments, Awards, Sports, Summits, Economic Affairs, Business) test events dated 2025-11-01 to 2026-11-04 with
event dates from the sources; every such question carries current_affairs {event_date, review_by 2027-05-05}. Other
time-sensitive facts (schemes, policies, reports, themes of days) carry current_affairs too. Where a source gives no
exact day, ca(..., inferred=reason) records it and the list is printed and written into the batch notes.

Every question has fact_checks. Each URL is marked OPENED (fetched and read, giving "web:fact-check") or SEARCH
(confirmed only from search-result text, giving "web:search-confirmed"); research ran on 2026-11-05 and 2026-11-06
(checked_on is recorded as the batch date 2026-11-05). Sites that refused a fetch (e.g. pib.gov.in,
business-standard.com, thestatesman.com, pmindia.gov.in, espncricinfo.com, thehindu.com) were not worked around.
Explanations and why_others_wrong state only facts backed by the listed sources, or stay neutral.

All earlier GA stems (BATCH_000 sample, BATCH_001_GA to BATCH_006_GA) were read first; no fact or event tested
there is tested again, and no event is used twice in this batch.

Statement questions have their key fixed by the statements (computed from truth values); other questions are written
with the correct option first and answer "*", and are then placed so that keys are balanced A to D.

    python tools/batch_007/ga.py
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
BATCH = "BATCH_007"
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
    """inferred: why the day is not stated by the source; such dates are listed in the batch notes."""
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
# key: (url, how it was checked on 2026-11-05); each part adds its own keys
U = {}

def fact(claim, key):
    url, how = U[key]
    return {"claim": claim, "source_url": url, "checked_on": TODAY, "_how": how}

AI_CHECK = []
# questions a fresh subagent answered from a key-free dump (2026-11-06), matching the key with high or
# medium confidence; low-confidence matches and mismatches are not tagged
INDEPENDENT_CHECK_IDS = {
    "BANK_GA_000904", "BANK_GA_000905", "BANK_GA_000907", "BANK_GA_000908", "BANK_GA_000909", "BANK_GA_000912",
    "BANK_GA_000916", "BANK_GA_000917", "BANK_GA_000918", "BANK_GA_000920", "BANK_GA_000923", "BANK_GA_000924",
    "BANK_GA_000925", "BANK_GA_000926", "BANK_GA_000927", "BANK_GA_000929", "BANK_GA_000930", "BANK_GA_000932",
    "BANK_GA_000934", "BANK_GA_000935", "BANK_GA_000936", "BANK_GA_000937", "BANK_GA_000938", "BANK_GA_000943",
    "BANK_GA_000944", "BANK_GA_000945", "BANK_GA_000946", "BANK_GA_000947", "BANK_GA_000949", "BANK_GA_000950",
    "BANK_GA_000951", "BANK_GA_000952", "BANK_GA_000953", "BANK_GA_000957", "BANK_GA_000959", "BANK_GA_000960",
    "BANK_GA_000962", "BANK_GA_000965", "BANK_GA_000966", "BANK_GA_000967", "BANK_GA_000968", "BANK_GA_000969",
    "BANK_GA_000971", "BANK_GA_000972", "BANK_GA_000973", "BANK_GA_000975", "BANK_GA_000976", "BANK_GA_000977",
    "BANK_GA_000978", "BANK_GA_000983", "BANK_GA_000984", "BANK_GA_000985", "BANK_GA_000986", "BANK_GA_000993",
    "BANK_GA_000999", "BANK_GA_001000", "BANK_GA_001001", "BANK_GA_001002", "BANK_GA_001004", "BANK_GA_001005",
    "BANK_GA_001007", "BANK_GA_001008", "BANK_GA_001009", "BANK_GA_001010", "BANK_GA_001012", "BANK_GA_001013",
    "BANK_GA_001014", "BANK_GA_001018", "BANK_GA_001023", "BANK_GA_001024", "BANK_GA_001033", "BANK_GA_001034",
    "BANK_GA_001035", "BANK_GA_001037", "BANK_GA_001038", "BANK_GA_001039", "BANK_GA_001041", "BANK_GA_001042",
    "BANK_GA_001043", "BANK_GA_001044", "BANK_GA_001045", "BANK_GA_001046", "BANK_GA_001047", "BANK_GA_001048",
    "BANK_GA_001049", "BANK_GA_001050", "BANK_GA_001051", "BANK_GA_001052", "BANK_GA_001053",
}
# reworded after the independent key-free check; re-solved by the author instead
REWORDED_AFTER_CHECK = []


# ###################################################################### part: nat (national CA + static)
# ###################################################################### part: nat (national CA + static)
U.update({
    # ---- National Current Affairs
    "nat_delhi_trib": ("https://www.tribuneindia.com/news/delhi/national-capital-gets-two-new-districts", OPENED),
    "nat_delhi_pio": ("https://dailypioneer.com/news/delhi-cabinet-approves-overhaul-revenue-districts-to-rise-to-13",
                      OPENED),
    "nat_h2_ians": ("https://ianslive.in/haryana-countrys-first-hydrogen-train-rolls-out-from-jind-locals-express-joy-"
                    "and-jubilation--20260717180603", OPENED),
    "nat_h2_dr": ("https://www.drishtiias.com/state-pcs-current-affairs/india-launches-first-indigenous-hydrogen-powered-"
                  "train/print_manually", SEARCH),
    "nat_zoo_air": ("https://newsonair.gov.in/indias-first-virtual-zoo-opens-in-indore-with-14-d-cinema-and-virtual-"
                    "jungle-safari-facilities/", OPENED),
    "nat_zoo_ot": ("https://www.outlooktraveller.com/News/indias-first-virtual-zoo-opens-in-indore-with-a-14d-cinema-and-"
                   "digital-jungle-safari", SEARCH),
    "nat_wb_me": ("https://morungexpress.com/west-bengal-becomes-36th-stateut-to-implement-ayushman-bharat-pm-jay",
                  OPENED),
    "nat_wb_dr": ("https://www.drishtiias.com/state-pcs-current-affairs/west-bengal-to-become-36th-state-ut-to-implement-"
                  "ayushman-bharat-pm-jay/print_manually", SEARCH),
    "nat_kusha_air": ("https://newsonair.gov.in/drdo-successfully-conducts-maiden-flight-test-of-long-range-surface-to-"
                      "air-missile-kusha/", OPENED),
    "nat_kusha_ians": ("https://ianslive.in/drdo-carries-out-maiden-flight-test-of-kusha-long-range-surface-to-air-"
                       "missile--20260723210815", SEARCH),
    "nat_vadinar_mm": ("https://www.manoramayearbook.in/current-affairs/india/2026/05/06/ship-repair-facility-in-"
                       "vadinar.html", OPENED),
    "nat_vadinar_ao": ("https://www.angelone.in/news/economy/cabinet-approves-1-570-crore-ship-repair-facility-in-"
                       "gujarat", OPENED),
    "nat_eos5_onm": ("https://www.onmanorama.com/news/india/2026/09/04/eos-05-earth-observation-satellite-launch-isro-"
                     "geosynchronous-orbit-success.html", OPENED),
    "nat_eos5_air": ("https://newsonair.gov.in/isro-successfully-launches-earth-observation-satellite-eos-05-from-"
                     "sriharikota/", SEARCH),
    "nat_nipu_ians": ("https://ianslive.in/cabinet-gives-nod-for-national-investment-policy-for-urea-2026-to-boost-"
                      "fertiliser-production--20260715155703", OPENED),
    "nat_nipu_bt": ("https://www.businesstoday.in/latest/economy/story/cabinet-approves-national-investment-policy-for-"
                    "urea-2026-to-boost-domestic-production-543124-2026-07-15", SEARCH),
    "nat_tara_air": ("https://www.newsonair.gov.in/drdo-indian-air-force-conduct-maiden-flight-trial-of-tara-weapon-off-"
                     "coast-of-odisha/", OPENED),
    "nat_tara_itv": ("https://www.indiatvnews.com/news/india/india-tests-maiden-flight-of-tactical-advanced-range-"
                     "augmentation-weapon-system-2026-05-08-1040369", SEARCH),
    "nat_kamala_air": ("https://www.newsonair.gov.in/union-cabinet-approves-two-hydro-electric-projects-in-arunachal-"
                       "pradesh", OPENED),
    "nat_kamala_mm": ("https://www.manoramayearbook.in/current-affairs/india/2026/04/10/two-hydro-projects-in-arunachal-"
                      "pradesh.html", OPENED),
    "nat_tunnel_air": ("https://www.newsonair.gov.in/ccea-approves-construction-of-countrys-first-underwater-road-cum-"
                       "rail-tunnel-project-under-brahmaputra-river-assam", OPENED),
    "nat_tunnel_etv": ("https://www.etvbharat.com/en/bharat/cabinet-approves-construction-of-road-cum-rail-tunnel-under-"
                       "brahmaputra-river-enn26021404334", OPENED),
    "nat_vns_nbm": ("https://www.nbmcw.com/news/roads-highways/cabinet-approves-two-varanasi-highway-corridors-worth-"
                    "over-rs-25-400-crore.html", OPENED),
    "nat_vns_fpj": ("https://www.freepressjournal.in/uttar-pradesh/uttar-pradesh-varanasi-gets-14447-crore-elevated-"
                    "corridor-project-to-cut-travel-time-boost-connectivity", OPENED),
    # ---- Static Awareness
    "nat_rupiah_wiki": ("https://en.wikipedia.org/wiki/Indonesian_rupiah", OPENED),
    "nat_rupiah_bi": ("https://www.bi.go.id/en/default.aspx", OPENED),
    "nat_brasilia_wiki": ("https://en.wikipedia.org/wiki/Brasília", OPENED),
    "nat_hemis_wiki": ("https://en.wikipedia.org/wiki/Hemis_National_Park", OPENED),
    "nat_hemis_np": ("https://national-parks.org/india/hemis-national-park/", SEARCH),
    "nat_pong_wiki": ("https://en.wikipedia.org/wiki/Pong_Dam", OPENED),
    "nat_pong_kangra": ("https://hpkangra.nic.in/tourist-place/pong-dam/", OPENED),
    "nat_aru_wiki": ("https://en.wikipedia.org/wiki/Arunachal_Pradesh", OPENED),
    "nat_aru_outlook": ("https://www.outlookindia.com/national/50-years-of-arunachal-pradesh-a-brief-look-at-its-"
                        "formation-news-47102", SEARCH),
    "nat_sariska_wiki": ("https://en.wikipedia.org/wiki/Sariska_Tiger_Reserve", OPENED),
    "nat_sariska_bci": ("https://bigcatsindia.com/sariska-tiger-reserve/", SEARCH),
    "nat_manas_wiki": ("https://en.wikipedia.org/wiki/Manas_National_Park", OPENED),
    "nat_manas_sp": ("https://www.sahapedia.org/manas-national-park-overview", SEARCH),
    "nat_farakka_fbp": ("https://fbp.gov.in/", OPENED),
    "nat_farakka_wiki": ("https://en.wikipedia.org/wiki/Farakka_Barrage", OPENED),
    "nat_bolivia_wiki": ("https://en.wikipedia.org/wiki/Bolivia", OPENED),
    "nat_bolivia_nwe": ("https://www.newworldencyclopedia.org/entry/Sucre", SEARCH),
    "nat_chf_wiki": ("https://en.wikipedia.org/wiki/Swiss_franc", OPENED),
    "nat_snb": ("https://www.snb.ch/en/", OPENED),
    "nat_mysore_wiki": ("https://en.wikipedia.org/wiki/Mysore_State", OPENED),
    "nat_madras_wiki": ("https://en.wikipedia.org/wiki/Madras_State", OPENED),
    "nat_kerala_wiki": ("https://en.wikipedia.org/wiki/Kerala", OPENED),
    "nat_kanchen_wiki": ("https://en.wikipedia.org/wiki/Khangchendzonga_National_Park", OPENED),
})

T = "National Current Affairs"
GOV, ST, DEF = "Government decisions", "States and UTs", "Defence"

# ------------------------------------------------------------------ National CA: Basic (5)
G(T, ST, "Basic",
  "In December 2025 the Delhi Cabinet, chaired by Chief Minister Rekha Gupta, approved a reorganisation of the "
  "National Capital Territory's revenue districts. How many revenue districts does Delhi have after this change?",
  ["13", "12", "14", "15"], "*",
  "Delhi: reorganisation of revenue districts",
  "The Delhi Cabinet chaired by Chief Minister Rekha Gupta approved reorganising Delhi's 11 revenue districts into 13, "
  "and raising the number of sub-divisions (SDM offices) from 33 to 39. The aim is to align revenue districts with "
  "municipal zones; in-principle approval had been reported in November 2025, before the Lieutenant Governor's nod.",
  ["Before: 11 revenue districts, 33 sub-divisions", "After: 13 districts, 39 sub-divisions"],
  [fact("Delhi Cabinet chaired by CM Rekha Gupta approved reorganising 11 revenue districts into 13; sub-divisions from "
        "33 to 39; report dated 12 December 2025 refers to the decision of 'Thursday'", "nat_delhi_trib"),
   fact("In-principle approval: revenue districts to rise from 11 to 13 and SDM offices from 33 to 39; MCD's 12 zones "
        "to be aligned with districts", "nat_delhi_pio")],
  why="The sources put the new total at 13 (up from 11); 12 is the number of MCD zones, not revenue districts.",
  current=ca("2025-12-11", inferred="Tribune report of 12 Dec 2025 says the Cabinet decided on 'Thursday'"))

G(T, GOV, "Basic",
  "India's first hydrogen-powered train, flagged off by Prime Minister Narendra Modi on 17 July 2026, runs between "
  "Jind and which station in Haryana?",
  ["Sonipat", "Panipat", "Rohtak", "Hisar"], "*",
  "India's first hydrogen train",
  "Prime Minister Narendra Modi flagged off India's first hydrogen-powered train at Jind on 17 July 2026. It runs on the "
  "89 km Jind-Sonipat section of Northern Railway in Haryana.",
  ["First hydrogen train: 17 July 2026", "Route: Jind-Sonipat (89 km), Northern Railway"],
  [fact("India's first hydrogen-powered train flagged off by PM Modi from Jind on Friday, 17 July 2026; Jind-Sonipat "
        "route, 89 km, Northern Railway", "nat_h2_ians"),
   fact("India's first indigenous hydrogen-powered train launched on the Jind-Sonipat section", "nat_h2_dr")],
  why="The sources name the Jind-Sonipat section; Panipat, Rohtak and Hisar are not the other terminal.",
  current=ca("2026-07-17"))

G(T, ST, "Basic",
  "India's first virtual zoo, with a 14-D cinema theatre and a virtual jungle safari, was inaugurated by Chief "
  "Minister Mohan Yadav in August 2026 in which city of Madhya Pradesh?",
  ["Indore", "Bhopal", "Jabalpur", "Gwalior"], "*",
  "State firsts: virtual zoo",
  "Madhya Pradesh Chief Minister Mohan Yadav inaugurated India's first virtual zoo at the Indore Zoo on 16 August 2026. "
  "Built for about ₹4.5 crore under the PPP model, it includes a 14-D cinema theatre and a virtual jungle safari.",
  ["First virtual zoo: Indore Zoo, Madhya Pradesh", "Inaugurated 16 Aug 2026 by CM Mohan Yadav", "Cost ~₹4.5 crore (PPP)"],
  [fact("India's first virtual zoo opened at Indore Zoo; CM Mohan Yadav inaugurated it 'yesterday' (article of 17 August "
        "2026); 14-D cinema and virtual jungle safari; about ₹4.5 crore, PPP model", "nat_zoo_air"),
   fact("India's first virtual zoo opens in Indore with a 14D cinema and digital jungle safari", "nat_zoo_ot")],
  why="The sources place the virtual zoo at Indore Zoo; Bhopal, Jabalpur and Gwalior are not named.",
  current=ca("2026-08-16"))

G(T, ST, "Basic",
  "With the signing of an MoU with the National Health Authority on 8 June 2026 at Vigyan Bhawan, West Bengal became "
  "which State/UT to implement Ayushman Bharat Pradhan Mantri Jan Arogya Yojana (AB PM-JAY)?",
  ["36th", "33rd", "34th", "35th"], "*",
  "AB PM-JAY coverage",
  "On 8 June 2026, the National Health Authority and West Bengal's Department of Health and Family Welfare signed an "
  "MoU at Vigyan Bhawan, New Delhi, making West Bengal the 36th State/UT to implement AB PM-JAY. Union Health Minister "
  "J.P. Nadda presided, and Chief Minister Suvendu Adhikari was present.",
  ["MoU: NHA + West Bengal, 8 June 2026, Vigyan Bhawan", "West Bengal: 36th State/UT under AB PM-JAY"],
  [fact("West Bengal became the 36th State/UT to implement AB-PMJAY after an MoU signed with NHA on Monday, 8 June 2026, "
        "at Vigyan Bhavan; J.P. Nadda presided; CM Suvendu Adhikari present", "nat_wb_me"),
   fact("West Bengal to become 36th State/UT to implement Ayushman Bharat PM-JAY (June 2026)", "nat_wb_dr")],
  why="The sources call West Bengal the 36th State/UT to implement the scheme.",
  current=ca("2026-06-08"))

G(T, DEF, "Basic",
  "DRDO carried out the maiden flight test of 'Kusha' from Dr APJ Abdul Kalam Island off Odisha in July 2026. What "
  "type of weapon system is Kusha?",
  ["Long-range surface-to-air missile system", "Air-launched beyond-visual-range air-to-air missile",
   "Submarine-launched ballistic missile", "Man-portable anti-tank guided missile"], "*",
  "Defence: DRDO missile tests",
  "Kusha is a long-range surface-to-air missile (LRSAM) system developed by DRDO. In its maiden flight test from Dr APJ "
  "Abdul Kalam Island, it intercepted an electronic target simulating a high-speed, high-altitude aerial threat. The "
  "Defence Ministry said it is meant to counter fighter aircraft, missiles, drones and large aircraft.",
  ["Kusha = long-range surface-to-air missile", "Maiden test: 23 July 2026, Abdul Kalam Island"],
  [fact("DRDO conducted the maiden flight test of the Kusha long-range surface-to-air missile from Dr APJ Abdul Kalam "
        "Island; intercepted an electronic target simulating a high-speed, high-altitude threat (article of 24 July "
        "2026)", "nat_kusha_air"),
   fact("DRDO carried out the maiden flight test of Kusha long-range surface-to-air missile on 23 July 2026",
        "nat_kusha_ians")],
  why="The sources describe Kusha as a long-range surface-to-air missile system, not any of the other types.",
  current=ca("2026-07-23"))

# ------------------------------------------------------------------ National CA: Intermediate (4)
G(T, GOV, "Intermediate",
  "The ₹1,570 crore ship repair facility at Vadinar, Gujarat, approved by the Cabinet Committee on Economic Affairs in "
  "May 2026 for vessels up to 300 metres long, will be implemented by Deendayal Port Authority jointly with which "
  "company?",
  ["Cochin Shipyard Limited", "Mazagon Dock Shipbuilders Limited", "Garden Reach Shipbuilders and Engineers",
   "Hindustan Shipyard Limited"], "*",
  "Cabinet decisions: maritime infrastructure",
  "The CCEA chaired by the Prime Minister approved a ship repair facility at Vadinar, Gujarat, with a combined "
  "investment of ₹1,570 crore, to be implemented jointly by Deendayal Port Authority and Cochin Shipyard Limited. It "
  "will have a 650-metre jetty and two large floating dry docks and will handle vessels up to 300 metres; India lacks "
  "adequate domestic capacity for ships longer than 230 metres.",
  ["Vadinar (Gujarat): ₹1,570 crore", "Deendayal Port Authority + Cochin Shipyard", "Ships up to 300 m; 650 m jetty; "
   "2 floating dry docks"],
  [fact("CCEA approved ship repair facility at Vadinar, Gujarat, ₹1,570 crore, jointly by Deendayal Port Authority and "
        "Cochin Shipyard Limited; vessels up to 300 m; 650 m jetty; two floating dry docks", "nat_vadinar_mm"),
   fact("Statement issued Wednesday (article 6 May 2026): Deendayal Port Authority and Cochin Shipyard Limited; ships up "
        "to 300 m; domestic facilities inadequate above 230 m", "nat_vadinar_ao")],
  why="The sources name Cochin Shipyard Limited as Deendayal Port Authority's partner; the other shipyards are not.",
  current=ca("2026-05-06", inferred="source says the government statement was issued on Wednesday, 6 May 2026"))

G(T, GOV, "Intermediate",
  "EOS-05, launched by GSLV-F17 from Sriharikota on 4 September 2026, is described as India's first Earth observation "
  "satellite designed to operate from which orbit?",
  ["Geosynchronous orbit", "Sun-synchronous polar orbit", "Low Earth equatorial orbit", "Lunar orbit"], "*",
  "ISRO missions",
  "GSLV-F17, the 19th flight of the GSLV, lifted off from the second launch pad at Sriharikota at 2:55 am on 4 "
  "September 2026 carrying the 2,367 kg EOS-05. It is India's first Earth observation satellite designed to operate "
  "in geosynchronous orbit, about 36,000 km up. It follows the GSLV-F10/EOS-03 mission of 2021, which failed because of "
  "a cryogenic upper stage anomaly.",
  ["GSLV-F17 / EOS-05: 4 Sep 2026", "2,367 kg; first geosynchronous Earth observation satellite",
   "Successor to failed GSLV-F10/EOS-03 (2021)"],
  [fact("GSLV-F17 launched EOS-05 (2,367 kg) on 4 September 2026 at 2:55 am from the second launch pad; India's first "
        "Earth observation satellite designed for geosynchronous orbit; follows GSLV-F10/EOS-03 (2021) failure",
        "nat_eos5_onm"),
   fact("ISRO successfully launched Earth observation satellite EOS-05 from Sriharikota", "nat_eos5_air")],
  why="The source states EOS-05 is designed for geosynchronous orbit; the other orbits are not its operating orbit.",
  current=ca("2026-09-04"))

G(T, GOV, "Intermediate",
  "The National Investment Policy for Urea-2026 (NIPU-2026), approved by the Cabinet Committee on Economic Affairs on "
  "15 July 2026 to attract investment in new gas-based urea units, provides for a Return on Equity (RoE) band of:",
  ["12% to 16%", "10% to 14%", "14% to 18%", "8% to 12%"], "*",
  "Cabinet decisions: fertiliser policy",
  "On 15 July 2026 the CCEA approved NIPU-2026, proposed by the Department of Fertilizers, to encourage fresh "
  "investment in gas-based urea units and move towards self-sufficiency in urea. It assures a Return on Equity band "
  "with a 12% floor and a 16% ceiling, and the government expects savings of over ₹250 crore per plant compared with "
  "the earlier National Investment Policy of 2012.",
  ["NIPU-2026: approved 15 July 2026", "Gas-based urea units", "RoE band: 12% floor, 16% ceiling"],
  [fact("CCEA approved NIPU-2026 on Wednesday, 15 July 2026; gas-based urea units; RoE floor 12% and ceiling 16%; "
        "savings over ₹250 crore per plant vs NIP-2012", "nat_nipu_ians"),
   fact("NIPU-2026 guarantees a Return on Equity band between 12% and 16%", "nat_nipu_bt")],
  why="The sources give the RoE band as 12% to 16%; the other ranges are not in the policy.",
  current=ca("2026-07-15"))

G(T, DEF, "Intermediate",
  "The Tactical Advanced Range Augmentation (TARA) weapon, a glide weapon that turns unguided munitions into "
  "precision-guided ones, had its maiden flight trial off Odisha on 7 May 2026. Which DRDO laboratory developed it, "
  "along with other DRDO labs?",
  ["Research Centre Imarat, Hyderabad", "Armament Research and Development Establishment, Pune",
   "Aeronautical Development Establishment, Bengaluru", "Defence Research and Development Establishment, Gwalior"], "*",
  "Defence: DRDO weapon trials",
  "DRDO and the Indian Air Force carried out the maiden flight trial of TARA off the Odisha coast on 7 May 2026. TARA "
  "is a glide weapon that upgrades unguided munitions into precision-guided weapons against ground targets. It was "
  "developed by Research Centre Imarat, Hyderabad, with other DRDO laboratories, and industry partners have begun "
  "production.",
  ["TARA = Tactical Advanced Range Augmentation", "Glide weapon kit for unguided munitions",
   "Lab: Research Centre Imarat, Hyderabad"],
  [fact("TARA (Tactical Advanced Range Augmentation), a glide weapon converting unguided munitions into precision-guided "
        "ones; maiden flight trial off Odisha on 7 May 2026 by DRDO and IAF; developed by Research Centre Imarat, "
        "Hyderabad, with other DRDO labs", "nat_tara_air"),
   fact("India tests maiden flight of Tactical Advanced Range Augmentation weapon system (8 May 2026 report)",
        "nat_tara_itv")],
  why="The source names Research Centre Imarat, Hyderabad, as the developing lab; the other labs are not named.",
  current=ca("2026-05-07"))

# ------------------------------------------------------------------ National CA: Advanced (3)
GS(T, ST, "Advanced", "the two hydroelectric projects in Arunachal Pradesh approved by the Union Cabinet in April 2026",
   ["The Kalai-II project is to be built by a joint venture of NHPC Limited and the State government.",
    "Kalai-II, on the Lohit river in Anjaw district, is the first hydro project in the Lohit basin.",
    "The 1,720 MW Kamala project spans Kamle, Kra Daadi and Kurung Kumey districts."],
   [False, True, True],
   "Cabinet decisions: hydropower in Arunachal Pradesh",
   "On 8 April 2026 the Cabinet Committee on Economic Affairs approved investments of about ₹40,150 crore for two "
   "Arunachal Pradesh projects. Kamala (1,720 MW, ₹26,069.50 crore, 96 months) spans Kamle, Kra Daadi and Kurung Kumey "
   "districts and is a joint venture of NHPC and the State government. Kalai-II (1,200 MW, ₹14,105.83 crore, 78 "
   "months) is on the Lohit river in Anjaw district, the first hydro project in the Lohit basin, and is a joint "
   "venture of THDC India Limited and the State government.",
   [fact("Kalai-II 1,200 MW, Anjaw district, ₹14,105.83 crore, 78 months; Kamala 1,720 MW, Kamle, Kra Daadi and Kurung "
         "Kumey districts, ₹26,069.50 crore, 96 months", "nat_kamala_air"),
    fact("Approved 8 April; Kamala: NHPC-State JV; Kalai-II: THDC India-State JV, on the Lohit river in Anjaw, first "
         "hydro project in the Lohit basin; total about ₹40,150 crore", "nat_kamala_mm")],
   why="Statement 1 is wrong: Kalai-II is a THDC India-State JV; NHPC is the partner for Kamala.",
   current=ca("2026-04-08"))

GS(T, GOV, "Advanced", "the Gohpur-Numaligarh project in Assam approved by the Cabinet Committee on Economic Affairs "
   "in February 2026",
   ["It links Gohpur on NH-15 with Numaligarh on NH-715.",
    "It is to be executed under the Hybrid Annuity Model.",
    "It includes a 15.79 km twin-tube road-cum-rail tunnel under the Brahmaputra, the first such project in India."],
   [True, False, True],
   "Cabinet decisions: Brahmaputra road-cum-rail tunnel",
   "The CCEA approved a 33.7 km four-lane access-controlled greenfield corridor between Gohpur (NH-15) and Numaligarh "
   "(NH-715) in Assam at a cost of ₹18,662 crore, to be built in EPC (Engineering Procurement Construction) mode. It "
   "includes a 15.79 km twin-tube road-cum-rail tunnel under the Brahmaputra, the country's first underwater "
   "road-cum-rail tunnel project and the second in the world. It will cut the 240 km, six-hour journey to 34 km.",
   [fact("Gohpur (NH-15)-Numaligarh (NH-715), 33.7 km, ₹18,662 crore, EPC mode; 15.79 km twin-tube tunnel under the "
         "Brahmaputra, country's first underwater road-cum-rail tunnel, second in the world; 240 km cut to 34 km",
         "nat_tunnel_air"),
    fact("Cabinet approval reported 14 February 2026; ₹18,662 crore, EPC basis; 15.79 km road-cum-rail tunnel; Gohpur "
         "on NH-15 and Numaligarh on NH-715", "nat_tunnel_etv")],
   why="Statement 2 is wrong: the sources say the project will be built in EPC mode, not under the Hybrid Annuity "
       "Model.",
   current=ca("2026-02-14"))

GS(T, GOV, "Advanced", "the two Varanasi highway corridors approved by the Cabinet Committee on Economic Affairs on "
   "15 July 2026",
   ["The 46.039 km NH-19 to Varanasi Ring Road connector includes a 910 m cable-stayed bridge over the Ganga.",
    "The 43.218 km corridor linking NH-31 with the Varanasi Ring Road runs along the Varuna river.",
    "Both corridors are to be built in EPC (Engineering Procurement Construction) mode."],
   [True, True, False],
   "Cabinet decisions: highway projects",
   "On 15 July 2026 the CCEA approved two Varanasi projects worth over ₹25,400 crore, both under the Hybrid Annuity "
   "Model (HAM). The 46.039 km NH-19 to Ring Road connector (₹14,447.64 crore) runs along the Ganga and includes a "
   "910 m cable-stayed bridge, a 1.32 km extradosed bridge with travelators and a rail over bridge. The 43.218 km "
   "NH-31 to Ring Road link (₹10,998.32 crore) runs along the Varuna.",
   [fact("NH-19 to Varanasi Ring Road, 46.039 km, ₹14,447.64 crore, HAM, 910 m cable-stayed bridge over the Ganga; "
         "NH-31 to Ring Road, 43.218 km, ₹10,998.32 crore, HAM, along the Varuna", "nat_vns_nbm"),
    fact("46.039 km corridor along the Ganga, ₹14,447.64 crore, Hybrid Annuity Model; article of 15 July 2026",
         "nat_vns_fpj")],
   why="Statement 3 is wrong: both corridors are to be built under the Hybrid Annuity Model.",
   current=ca("2026-07-15"))

# ====================================================================== Static Awareness
T = "Static Awareness"
CC, NPD, SF = "Capitals and currencies", "National parks and dams", "Indian states facts"

# ------------------------------------------------------------------ Static: Basic (6)
G(T, CC, "Basic",
  "The rupiah, managed by Bank Indonesia, is the currency of which country?",
  ["Indonesia", "Malaysia", "Thailand", "Philippines"], "*",
  "World currencies",
  "The rupiah (ISO code IDR) is the currency of Indonesia; Bank Indonesia, the central bank, manages it.",
  ["Rupiah (IDR): Indonesia", "Central bank: Bank Indonesia"],
  [fact("Indonesian rupiah, ISO code IDR, issued by Bank Indonesia", "nat_rupiah_wiki"),
   fact("The rupiah is the currency of the Republic of Indonesia managed by Bank Indonesia", "nat_rupiah_bi")],
  why="The sources tie the rupiah to Indonesia; Malaysia, Thailand and the Philippines have other currencies.")

G(T, CC, "Basic",
  "Brasília, inaugurated on 21 April 1960 as the new capital of Brazil, replaced which city as the capital?",
  ["Rio de Janeiro", "São Paulo", "Belo Horizonte", "Recife"], "*",
  "World capitals",
  "Brasília, planned by Lúcio Costa with most public buildings designed by Oscar Niemeyer, was inaugurated on 21 April "
  "1960. It replaced Rio de Janeiro, which had been Brazil's capital from 1763 to 1960.",
  ["Brasília inaugurated 21 April 1960", "Previous capital: Rio de Janeiro (1763-1960)"],
  [fact("Brasília, federal capital of Brazil, inaugurated 21 April 1960; replaced Rio de Janeiro (capital 1763-1960); "
        "planned by Lúcio Costa, buildings by Oscar Niemeyer", "nat_brasilia_wiki")],
  why="The source names Rio de Janeiro as the capital before Brasília; the other cities were not replaced in 1960.")

G(T, NPD, "Basic",
  "Hemis National Park, described as the largest notified protected area in India and known for its snow leopards, is "
  "located in which State/UT?",
  ["Ladakh", "Sikkim", "Himachal Pradesh", "Uttarakhand"], "*",
  "National parks of India",
  "Hemis National Park lies in Leh district of Ladakh, about 50 km from Leh. Established in 1981 and covering about "
  "4,400 sq km, it is described as the largest notified protected area in India and has the highest density of snow "
  "leopards of any protected area in the world.",
  ["Hemis NP: Leh district, Ladakh", "~4,400 sq km; est. 1981", "Snow leopards"],
  [fact("Hemis National Park, Leh district, Ladakh; about 4,400 sq km; established 1981; largest notified protected "
        "area in India; highest density of snow leopards", "nat_hemis_wiki"),
   fact("Hemis spans 4,400 sq km, the largest national park in India", "nat_hemis_np")],
  why="The sources place Hemis in Ladakh; it is not in the other states.")

G(T, NPD, "Basic",
  "The Pong Dam in Kangra district of Himachal Pradesh, whose reservoir is called Maharana Pratap Sagar, is built on "
  "which river?",
  ["Beas", "Sutlej", "Ravi", "Chenab"], "*",
  "Dams of India",
  "The Pong Dam is an earth-fill dam on the Beas river in Kangra district, Himachal Pradesh. Its reservoir is named "
  "Maharana Pratap Sagar, also called the Pong reservoir.",
  ["Pong Dam: Beas river, Kangra (HP)", "Reservoir: Maharana Pratap Sagar"],
  [fact("Pong Dam on the Beas river, Kangra district, Himachal Pradesh; reservoir Maharana Pratap Sagar",
        "nat_pong_wiki"),
   fact("Pong Dam on the Beas; reservoir Maharana Pratap Sagar; Kangra district", "nat_pong_kangra")],
  why="The sources put the Pong Dam on the Beas; the Sutlej, Ravi and Chenab are not its river.")

G(T, SF, "Basic",
  "Arunachal Pradesh, which became a full state on 20 February 1987, was known by which name until 1972?",
  ["North-East Frontier Agency (NEFA)", "Lushai Hills", "Naga Hills-Tuensang Area", "United Khasi-Jaintia Hills"], "*",
  "Formation of Indian states",
  "Arunachal Pradesh was called the North-East Frontier Agency (NEFA) until 1972, when it was renamed and became a "
  "Union Territory. It became a state on 20 February 1987. Its capital is Itanagar.",
  ["Until 1972: NEFA", "1972: renamed, Union Territory", "20 Feb 1987: state"],
  [fact("Arunachal Pradesh: former name North-East Frontier Agency (NEFA), used until 1972; statehood 20 February 1987; "
        "capital Itanagar", "nat_aru_wiki"),
   fact("NEFA was renamed Arunachal Pradesh and made a Union Territory in January 1972; statehood on 20 February 1987",
        "nat_aru_outlook")],
  why="The sources give NEFA as the former name; the other names do not refer to Arunachal Pradesh.")

G(T, NPD, "Basic",
  "Sariska Tiger Reserve, in the Aravalli hills, where tigers were relocated from Ranthambhore in 2008, is in which "
  "district of Rajasthan?",
  ["Alwar", "Sawai Madhopur", "Bundi", "Bharatpur"], "*",
  "Tiger reserves of India",
  "Sariska Tiger Reserve lies in Alwar district, Rajasthan, in the Aravalli Range. It became part of Project Tiger in "
  "1978 and a national park in 1982. Tigers were relocated there from Ranthambhore in 2008.",
  ["Sariska: Alwar district, Rajasthan", "Aravalli Range", "Tigers relocated from Ranthambhore, 2008"],
  [fact("Sariska Tiger Reserve, Alwar district, Rajasthan; Aravalli Range; national park 1982; tigers relocated from "
        "Ranthambhore in 2008", "nat_sariska_wiki"),
   fact("Sariska lies in Alwar district, about 107 km from Jaipur", "nat_sariska_bci")],
  why="The sources place Sariska in Alwar district; the other districts are not its location.")

# ------------------------------------------------------------------ Static: Advanced (6)
GS(T, NPD, "Advanced", "Manas National Park",
   ["It was inscribed as a UNESCO World Heritage Site in 1985.",
    "It lies in Arunachal Pradesh.",
    "It borders the Royal Manas National Park of Bhutan."],
   [True, False, True],
   "National parks of India",
   "Manas National Park is in Assam (Chirang and Baksa districts, Bodoland Territorial Region), in the Himalayan "
   "foothills along the Manas river. It was inscribed as a World Heritage Site in 1985, was on the List of World "
   "Heritage in Danger from 1992 to 2011, and borders Bhutan's Royal Manas National Park. It is also a tiger reserve, "
   "an elephant reserve and a biosphere reserve.",
   [fact("Manas NP: Assam (Chirang and Baksa); UNESCO 1985; in Danger 1992-2011; adjoins Royal Manas National Park, "
         "Bhutan", "nat_manas_wiki"),
    fact("Manas borders the Royal Manas National Park in Bhutan", "nat_manas_sp")],
   why="Statement 2 is wrong: Manas National Park is in Assam, not Arunachal Pradesh.")

GS(T, NPD, "Advanced", "the Farakka Barrage",
   ["It is built across the Ganga in Murshidabad district of West Bengal.",
    "Its feeder canal diverts Ganga water into the Bhagirathi-Hooghly, mainly to preserve Kolkata Port.",
    "The project was dedicated to the nation in 1995."],
   [True, True, False],
   "Dams and barrages of India",
   "The Farakka Barrage is across the Ganga at Farakka in Murshidabad district (with parts in Malda), West Bengal. Its "
   "feeder canal diverts about 40,000 cusecs into the Bhagirathi-Hooghly system mainly to preserve Kolkata Port by "
   "flushing silt. The Farakka Barrage Project Authority was set up in 1961 and the project was dedicated to the nation "
   "in May 1975.",
   [fact("Farakka Barrage on the Ganga, Murshidabad and Malda districts; feeder canal diverts about 40,000 cusecs into "
         "the Bhagirathi-Hooghly mainly for preservation of Kolkata Port; dedicated to the nation in May 1975",
         "nat_farakka_fbp"),
    fact("Barrage across the Ganges in Murshidabad district; diverts water into the Hooghly to flush silt from Kolkata "
         "harbour; operational 21 April 1975", "nat_farakka_wiki")],
   why="Statement 3 is wrong: the project was dedicated to the nation in 1975, not 1995.")

GS(T, CC, "Advanced", "Bolivia",
   ["Its currency is the Bolivian peso.",
    "Sucre is its constitutional capital and the seat of the judiciary.",
    "La Paz is the seat of its executive and legislative branches."],
   [False, True, True],
   "World capitals and currencies",
   "Bolivia has a split capital: Sucre is the constitutional capital and seat of the judiciary, while La Paz houses the "
   "executive, legislative and electoral branches. Its currency is the boliviano (BOB).",
   [fact("Sucre is the constitutional capital and seat of the judiciary; La Paz is the seat of government (executive, "
         "legislative, electoral); currency boliviano (BOB)", "nat_bolivia_wiki"),
    fact("The seat of government moved from Sucre to La Paz in 1898; Sucre remains the constitutional capital and seat "
         "of the Supreme Court", "nat_bolivia_nwe")],
   why="Statement 1 is wrong: Bolivia's currency is the boliviano.")

GS(T, CC, "Advanced", "the Swiss franc",
   ["It is legal tender in Liechtenstein as well as in Switzerland.",
    "Its ISO code CHF comes from 'Confoederatio Helvetica', the Latin name of Switzerland.",
    "The Swiss National Bank, which issues its banknotes, has head offices in Zurich and Berne."],
   [True, True, True],
   "World currencies",
   "The Swiss franc is the currency of Switzerland and Liechtenstein and is divided into 100 Rappen/centimes. Its ISO "
   "code CHF stands for Confoederatio Helvetica; Latin was chosen because Switzerland has four national languages. The "
   "Swiss National Bank holds the note-issuing privilege (coins are issued by Swissmint) and has head offices in Zurich "
   "and Berne.",
   [fact("Swiss franc is currency and legal tender of Switzerland and Liechtenstein; CHF from Confoederatio Helvetica; "
         "SNB issues banknotes, Swissmint coins", "nat_chf_wiki"),
    fact("The SNB is entrusted with the note-issuing privilege; head offices in Zurich and Berne", "nat_snb")],
   why="All three statements are supported by the sources.")

GS(T, SF, "Advanced", "the formation and renaming of southern Indian states",
   ["Kerala was formed on 1 November 1956 under the States Reorganisation Act, including Travancore-Cochin and the "
    "Malabar district of Madras State.",
    "Mysore State was renamed Karnataka on 1 November 1973.",
    "Madras State was renamed Tamil Nadu in 1973."],
   [True, True, False],
   "Formation of Indian states",
   "Kerala was formed on 1 November 1956 under the States Reorganisation Act, combining Travancore-Cochin (minus some "
   "southern taluks) with Malabar district and Kasaragod taluk of Madras State. Mysore State was renamed Karnataka on "
   "1 November 1973 under the Mysore State (Alteration of Name) Act. Madras State was renamed Tamil Nadu on 14 January "
   "1969.",
   [fact("Kerala formed 1 November 1956 under the States Reorganisation Act from Travancore-Cochin and Malabar district "
         "of Madras State", "nat_kerala_wiki"),
    fact("Mysore State renamed Karnataka on 1 November 1973 under the Mysore State (Alteration of Name) Act",
         "nat_mysore_wiki"),
    fact("Madras State renamed Tamil Nadu on 14 January 1969", "nat_madras_wiki")],
   why="Statement 3 is wrong: Madras State became Tamil Nadu on 14 January 1969, not in 1973.")

GS(T, NPD, "Advanced", "Khangchendzonga National Park",
   ["In July 2016 it became India's first 'mixed' World Heritage Site.",
    "It is named after Kangchenjunga, the world's third-highest peak.",
    "It was established as a national park in 1977."],
   [True, True, True],
   "National parks of India",
   "Khangchendzonga National Park in Sikkim was established in 1977 and named after Kangchenjunga, the world's "
   "third-highest peak (8,586 m). It was inscribed at the 40th session of the World Heritage Committee in July 2016, "
   "becoming India's first mixed (natural and cultural) World Heritage Site.",
   [fact("Khangchendzonga National Park, Sikkim; established 1977; named after Kangchenjunga, world's third-highest "
         "peak; inscribed July 2016 (40th session), India's first Mixed Heritage site", "nat_kanchen_wiki")],
   why="All three statements are supported by the source.")

# ###################################################################### part: intl (international + summits)
# ###################################################################### part: intl (international CA + summits)
U.update({
    "intl_zambia_dm": ("https://www.dailymirror.lk/international/Zambias-President-Hakainde-Hichilema-wins-second-term/"
                       "107-348355", OPENED),
    "intl_zambia_aa": ("https://allafrica.com/stories/202609020720.html", OPENED),
    "intl_tz_star": ("https://www.thestar.com.my/news/world/2025/11/03/tanzania039s-hassan-sworn-into-office-after-"
                     "deadly-election-violence", OPENED),
    "intl_austria_ob": ("https://www.outlookbusiness.com/economy-and-policy/modi-stocker-talks-focus-on-west-asia-"
                        "ukraine-15-deals-deepen-india-austria-ties-mea", OPENED),
    "intl_austria_trib": ("https://www.tribuneindia.com/news/world/india-austria-ties-pm-modi-and-chancellor-stocker-"
                          "forge-new-chapter-in-tech-and-trade-partnership/", OPENED),
    "intl_duma_meduza": ("https://meduza.io/en/news/2026/09/25/united-russia-won-349-of-450-seats-in-russia-s-new-state-"
                         "duma-parliament-will-include-46-war-participants", OPENED),
    "intl_duma_air": ("https://newsonair.gov.in/vladimir-putins-united-russia-party-retains-majority-in-parliament/",
                      OPENED),
    "intl_arm_jam": ("https://jam-news.net/final-election-results-in-armenia-pashinyans-party-wins-majority/", OPENED),
    "intl_arm_bta": ("https://www.bta.bg/en/news/1142413-prime-minister-nikol-pashinyan-s-civil-contract-party-wins-"
                     "parliamentary-electio", OPENED),
    "intl_vn_vns": ("https://vietnamnews.vn/politics-laws/1780938/party-general-secretary-state-president-to-lam-"
                    "concludes-state-visit-to-india.html", OPENED),
    "intl_vn_vnp": ("https://en.vietnamplus.vn/vietnam-india-issue-joint-statement-on-enhanced-comprehensive-strategic-"
                    "partnership-post342314.vnp", SEARCH),
    "intl_kor_onm": ("https://www.onmanorama.com/upsc/current-affairs/2026/04/21/india-south-korea-target-50-billion-"
                     "annual-trade-by-2030.html", OPENED),
    "intl_kor_stat": ("https://www.thestatesman.com/india/india-s-korea-deepen-strategic-ties-with-focus-on-tech-trade-"
                      "and-indo-pacific-cooperation-1503584009.html", SEARCH),
    "intl_fin_mon": ("https://the-monitor.org/country-profile/finland/mine-ban-policy", OPENED),
    "intl_fin_gov": ("https://valtioneuvosto.fi/en/-/236553176/finland-s-withdrawal-from-ottawa-convention-to-take-effect",
                     SEARCH),
    "intl_afq_star": ("https://www.thestar.com.my/news/world/2025/11/03/magnitude-63-earthquake-shakes-afghanistan039s-"
                      "mazar-e-sharif-city-casualties-feared", OPENED),
    "intl_afq_arab": ("https://www.arabnews.com/node/2621434/world", SEARCH),
    "intl_unsc_rtt": ("https://www.rttnews.com/3658070/kyrgyzstan-elected-as-non-permanent-member-of-security-council-"
                      "for-first-time.aspx?type=uspn", OPENED),
    "intl_unsc_air": ("https://newsonair.gov.in/five-countries-elected-non-permanent-members-of-un-security-council/",
                      OPENED),
    "intl_esc_upi": ("https://www.upi.com/Science_News/2025/11/13/blue-origin-new-glenn-launch/1621763070496/", OPENED),
    "intl_esc_space": ("https://www.space.com/space-exploration/launches-spacecraft/blue-origin-lands-huge-new-glenn-"
                       "rocket-booster-for-1st-time-after-acing-mars-escapade-launch-for-nasa", SEARCH),
    "intl_saudi_cbs": ("https://www.cbsnews.com/amp/news/trump-saudi-arabia-major-non-nato-ally", OPENED),
    "intl_saudi_arab": ("https://arabnews.com/node/2623140/saudi-arabia", SEARCH),
    "intl_gcc_air": ("https://www.newsonair.gov.in/india-and-gulf-cooperation-council-sign-terms-of-reference-for-a-"
                     "free-trade-agreement", OPENED),
    "intl_gcc_bs": ("https://www.business-standard.com/economy/news/india-gcc-sign-tor-free-trade-agreement-"
                    "negotiations-126020501471_1.html", SEARCH),
    "intl_isr_ob": ("https://www.outlookbusiness.com/news/india-israel-ink-terms-of-reference-to-formally-launch-fta-"
                    "talks", OPENED),
    "intl_isr_week": ("https://www.theweek.in/wire-updates/business/2025/11/20/fgn52-biz-ld-india-israel-fta.html",
                      SEARCH),
    "intl_kz_cevro": ("https://www.cevro.cz/en/caps/kazakhstan-adopts-new-constitution-after-march-2026-referendum",
                      OPENED),
    "intl_kz_tengri": ("https://en.tengrinews.kz/politics_sub/Referendum-on-new-Constitution-voting-results-announced-"
                       "271205", OPENED),
    "intl_kz_timesca": ("https://timesca.com/new-constitution-backed-by-majority-as-kazakhstan-reports-record-"
                        "referendum-turnout/", OPENED),
    "intl_merc_gov": ("https://www.gov.br/planalto/en/latest-news/2025/12/president-lula-attends-the-67th-summit-of-"
                      "mercosur-heads-of-state-and-associated-states", OPENED),
    "intl_merc_mp": ("https://en.mercopress.com/2025/12/22/paraguay-handed-over-mercosur-pro-tempore-presidency", OPENED),
})

T = "International Current Affairs"
BIL, GLB = "Bilateral relations", "Global events"

# ------------------------------------------------------------------ Basic (3)
G(T, GLB, "Basic",
  "Hakainde Hichilema, who won the general election of 13 August 2026 and was sworn in for another five-year term on "
  "1 September 2026, is the President of which country?",
  ["Zambia", "Zimbabwe", "Malawi", "Botswana"], "*",
  "Elections in Africa, 2026",
  "Zambia held its general election on 13 August 2026. On 18 August the Electoral Commission declared President "
  "Hakainde Hichilema of the United Party for National Development (UPND) the winner with about 61.4% of valid votes; "
  "his main rival, Brian Mundubile, got about 38%. Hichilema was sworn in for another five-year term on 1 September "
  "2026 at the National Heroes Stadium, Lusaka.",
  ["Zambia election: 13 Aug 2026", "Winner: Hakainde Hichilema (UPND), ~61.4%", "Sworn in: 1 Sep 2026, Lusaka"],
  [fact("Zambia's election on 13 August 2026; Hichilema (UPND) won a second five-year term with about 61.4%; Brian "
        "Mundubile about 38%; declared on 18 August 2026", "intl_zambia_dm"),
   fact("Hichilema sworn in on 1 September 2026 at National Heroes Stadium, Lusaka, for another five-year term",
        "intl_zambia_aa")],
  why="The sources describe Hichilema as Zambia's President; he does not lead Zimbabwe, Malawi or Botswana.",
  current=ca("2026-09-01"))

G(T, GLB, "Basic",
  "Samia Suluhu Hassan was sworn in as President at a military facility in Dodoma on 3 November 2025, after being "
  "declared the winner of the 29 October election with 97.66% of the vote. Which country does she lead?",
  ["Tanzania", "Kenya", "Uganda", "Mozambique"], "*",
  "Elections in Africa, 2025",
  "Tanzania voted on 29 October 2025. Samia Suluhu Hassan was declared the winner with 97.66% of the vote and was "
  "sworn in on 3 November 2025 at a military base in Dodoma, Tanzania's administrative capital, amid deadly protests "
  "after the election. She first became President in 2021 after the death of her predecessor.",
  ["Tanzania election: 29 Oct 2025", "Samia Suluhu Hassan: 97.66%", "Sworn in: 3 Nov 2025, Dodoma"],
  [fact("Samia Suluhu Hassan sworn in on 3 November 2025 at a military base in Dodoma, Tanzania's administrative "
        "capital; won 97.66% in the 29 October vote; took office in 2021 after her predecessor died", "intl_tz_star")],
  why="Dodoma is Tanzania's administrative capital and the source names her as Tanzania's President.",
  current=ca("2025-11-03"))

G(T, BIL, "Basic",
  "Chancellor Christian Stocker held talks with Prime Minister Modi at Hyderabad House on 16 April 2026, in the first "
  "visit to India by a leader of his country in over four decades. Which country does he lead?",
  ["Austria", "Germany", "Hungary", "Belgium"], "*",
  "India-Austria relations",
  "Austrian Chancellor Christian Stocker made a four-day official visit to India and held talks with Prime Minister "
  "Narendra Modi at Hyderabad House, New Delhi, on 16 April 2026. It was the first visit by an Austrian leader to "
  "India in over four decades (the previous one was in 1984), and India was his first destination outside Europe as "
  "Chancellor. The visit produced 15 outcomes, including six MoUs on defence, counter-terrorism, skills, education, "
  "green energy and nursing.",
  ["Christian Stocker: Chancellor of Austria", "Talks: 16 Apr 2026, Hyderabad House", "15 outcomes incl. 6 MoUs"],
  [fact("Austrian Chancellor Christian Stocker held talks with PM Modi at Hyderabad House on 16 April 2026; first "
        "visit by an Austrian leader in over four decades (previous in 1984); 15 outcomes including six MoUs",
        "intl_austria_ob"),
   fact("Stocker chose India for his first visit outside Europe; four-day official trip", "intl_austria_trib")],
  why="The sources identify Christian Stocker as the Chancellor of Austria; Germany's Chancellor is a different person.",
  current=ca("2026-04-16"))

# ------------------------------------------------------------------ Intermediate (11)
G(T, GLB, "Intermediate",
  "In the elections to Russia's ninth State Duma held from 18 to 20 September 2026, how many of the 450 seats did "
  "United Russia win, according to the final results announced by the Central Election Commission?",
  ["349", "324", "301", "375"], "*",
  "Russian State Duma election, 2026",
  "Russia elected its ninth State Duma (lower house, 450 deputies, half by party list and half from single-member "
  "constituencies) on 18-20 September 2026. Central Election Commission head Ella Pamfilova announced that United "
  "Russia won 349 of the 450 seats; turnout was 59.8%.",
  ["9th State Duma: 18-20 Sep 2026", "United Russia: 349 of 450 seats", "Turnout: 59.8%"],
  [fact("United Russia won 349 of 450 seats in the State Duma elections of 18-20 September 2026, as announced by CEC "
        "head Ella Pamfilova; turnout 59.8%", "intl_duma_meduza"),
   fact("Election to the 9th State Duma; 450 deputies, half by party list and half in single-mandate constituencies",
        "intl_duma_air")],
  why="The final figure given by the source is 349 seats; the other numbers do not match it.",
  current=ca("2026-09-25"))

G(T, GLB, "Intermediate",
  "Prime Minister Nikol Pashinyan's party retained its majority in Armenia's parliamentary election of 7 June 2026, "
  "winning about 49.7% of the vote. What is the name of his party?",
  ["Civil Contract", "Strong Armenia", "Prosperous Armenia", "Republican Party of Armenia"], "*",
  "Armenian parliamentary election, 2026",
  "In Armenia's parliamentary election of 7 June 2026, Pashinyan's Civil Contract won 49.7456% of the vote and 64 of "
  "the 105 seats in the final results. The Strong Armenia alliance of businessman Samvel Karapetyan came second with "
  "about 23.3% and 29 seats. Turnout was about 59%.",
  ["Armenia vote: 7 Jun 2026", "Civil Contract: ~49.7%, 64 of 105 seats", "Second: Strong Armenia (Samvel Karapetyan)"],
  [fact("Final results: Civil Contract 49.7456% and 64 of 105 seats; Strong Armenia alliance led by Samvel Karapetyan "
        "23.2710% and 29 seats; election on 7 June 2026", "intl_arm_jam"),
   fact("Pashinyan's Civil Contract party won the 7 June 2026 elections; turnout 59%", "intl_arm_bta")],
  why="The sources name Civil Contract as Pashinyan's party; Strong Armenia, led by Samvel Karapetyan, came second.",
  current=ca("2026-06-07"))

G(T, BIL, "Intermediate",
  "During the state visit of Vietnam's General Secretary and President To Lam to India from 5 to 7 May 2026, India "
  "and Vietnam elevated their relationship to which level?",
  ["Enhanced Comprehensive Strategic Partnership", "Comprehensive Strategic Partnership",
   "Special Global Strategic Partnership", "Special Strategic Partnership"], "*",
  "India-Vietnam relations",
  "To Lam paid a state visit to India from 5 to 7 May 2026, holding talks in New Delhi and visiting Mumbai, where he "
  "rang the bell at the National Stock Exchange. The two sides raised their ties to an 'Enhanced Comprehensive "
  "Strategic Partnership' and set a target of USD 25 billion in two-way trade by 2030 (trade exceeded USD 16.4 billion "
  "in 2025).",
  ["Visit: 5-7 May 2026 (New Delhi, Mumbai)", "New level: Enhanced Comprehensive Strategic Partnership",
   "Trade target: USD 25 bn by 2030"],
  [fact("To Lam's state visit to India, 5-7 May 2026; ties elevated to Enhanced Comprehensive Strategic Partnership; "
        "trade target USD 25 billion by 2030; visited New Delhi and Mumbai", "intl_vn_vns"),
   fact("Vietnam and India issued a Joint Statement on the Enhanced Comprehensive Strategic Partnership",
        "intl_vn_vnp")],
  why="The sources name the new level as the Enhanced Comprehensive Strategic Partnership, an upgrade of the earlier "
      "Comprehensive Strategic Partnership.",
  current=ca("2026-05-05"))

G(T, BIL, "Intermediate",
  "After talks between Prime Minister Modi and South Korean President Lee Jae Myung in New Delhi on 20 April 2026, the "
  "two countries set what target for annual bilateral trade?",
  ["USD 50 billion by 2030", "USD 25 billion by 2030", "USD 100 billion by 2035", "USD 40 billion by 2028"], "*",
  "India-South Korea relations",
  "During President Lee Jae Myung's state visit, he and Prime Minister Modi held talks in New Delhi on 20 April 2026. "
  "They aimed to nearly double annual trade to USD 50 billion by 2030, launched a framework for an 'India-Korea "
  "Digital Bridge' on AI, data governance and digital businesses, agreed to resume and expedite talks to upgrade the "
  "CEPA, and adopted a Joint Strategic Vision for the Special Strategic Partnership for 2026-2030.",
  ["Talks: 20 Apr 2026, New Delhi", "Trade target: USD 50 bn by 2030", "India-Korea Digital Bridge; CEPA upgrade talks"],
  [fact("India and South Korea aim to nearly double annual trade to USD 50 billion by 2030; talks in New Delhi on 20 "
        "April 2026; Digital Bridge framework; CEPA upgrade talks to resume", "intl_kor_onm"),
   fact("India and South Korea deepen strategic ties with focus on tech, trade and Indo-Pacific cooperation",
        "intl_kor_stat")],
  why="The source gives USD 50 billion by 2030 as the trade target; the other figures do not appear in it.",
  current=ca("2026-04-20"))

G(T, GLB, "Intermediate",
  "Finland's withdrawal from which international convention took effect on 10 January 2026, six months after it "
  "deposited its instrument of withdrawal?",
  ["Ottawa Convention (Mine Ban Treaty) on anti-personnel landmines", "Convention on Cluster Munitions",
   "Chemical Weapons Convention", "Arms Trade Treaty"], "*",
  "Treaty withdrawals",
  "Finland deposited its instrument of withdrawal from the Ottawa Convention, which bans anti-personnel landmines, on "
  "10 July 2025. Under the treaty, a withdrawal takes effect six months after the depositary receives it, so "
  "Finland's exit took effect on 10 January 2026.",
  ["Ottawa Convention: bans anti-personnel mines", "Instrument deposited: 10 Jul 2025",
   "Withdrawal effective: 10 Jan 2026"],
  [fact("Finland deposited its instrument of withdrawal from the Mine Ban Treaty on 10 July 2025; it took effect on "
        "10 January 2026", "intl_fin_mon"),
   fact("Finland's withdrawal from the Ottawa Convention took effect on 10 January 2026", "intl_fin_gov")],
  why="The sources concern the Ottawa (Mine Ban) Convention; they record no Finnish withdrawal from the other treaties.",
  current=ca("2026-01-10"))

G(T, GLB, "Intermediate",
  "A magnitude 6.3 earthquake struck northern Afghanistan early on 3 November 2025, killing at least 20 people and "
  "damaging part of the famous Blue Mosque shrine. Near which city did it strike?",
  ["Mazar-e-Sharif", "Herat", "Kandahar", "Jalalabad"], "*",
  "Earthquakes",
  "On 3 November 2025 a magnitude 6.3 earthquake (as per the US Geological Survey) hit near Mazar-e-Sharif, a city of "
  "about 523,000 people in Balkh province. Preliminary figures put the toll at least 20 dead and 643 injured. Part of "
  "the Blue Mosque shrine was damaged, though its main structure remained standing.",
  ["3 Nov 2025: M6.3 quake", "Near Mazar-e-Sharif (Balkh)", "Blue Mosque partly damaged"],
  [fact("Magnitude 6.3 earthquake near Mazar-e-Sharif on 3 November 2025; at least 20 killed, 643 injured; part of "
        "the Blue Mosque shrine damaged", "intl_afq_star"),
   fact("Afghanistan earthquake damaged historical sites including the Blue Mosque", "intl_afq_arab")],
  why="The sources place the quake near Mazar-e-Sharif, home of the Blue Mosque; the other cities are not named.",
  current=ca("2025-11-03"))

G(T, GLB, "Intermediate",
  "Of the five countries elected to the UN Security Council in June 2026 as non-permanent members for 2027-2028, which "
  "one won a seat for the first time, defeating the Philippines in the Asia-Pacific contest?",
  ["Kyrgyzstan", "Uzbekistan", "Tajikistan", "Turkmenistan"], "*",
  "UN Security Council elections",
  "In June 2026 the UN General Assembly elected Austria, Kyrgyzstan, Portugal, Trinidad and Tobago and Zimbabwe as "
  "non-permanent members for 1 January 2027 to 31 December 2028. Kyrgyzstan, a UN member since 1992, won its first "
  "term, beating the Philippines 142-49 in the fourth round. The five replace Denmark, Greece, Pakistan, Panama and "
  "Somalia.",
  ["Elected for 2027-28: Austria, Kyrgyzstan, Portugal, Trinidad and Tobago, Zimbabwe", "Kyrgyzstan: first term",
   "Beat the Philippines 142-49"],
  [fact("Kyrgyzstan won the Asia-Pacific seat in its first Security Council term, beating the Philippines 142-49 in "
        "the fourth round; others elected: Austria, Portugal, Trinidad and Tobago, Zimbabwe", "intl_unsc_rtt"),
   fact("Five countries elected for 1 January 2027 to 31 December 2028, replacing Denmark, Greece, Pakistan, Panama "
        "and Somalia", "intl_unsc_air")],
  why="Only Kyrgyzstan is among the five countries the sources list as elected; the other Central Asian states are not.",
  current=ca("2026-06-03", inferred="source says the vote was on a Wednesday; article dated 4 June 2026"))

G(T, GLB, "Intermediate",
  "NASA's twin ESCAPADE probes, meant to study how the atmosphere of Mars has changed, were launched on 13 November "
  "2025 aboard which rocket?",
  ["New Glenn (Blue Origin)", "Falcon Heavy (SpaceX)", "Vulcan Centaur (United Launch Alliance)",
   "Space Launch System (NASA)"], "*",
  "Space missions",
  "Blue Origin's New Glenn rocket, on its second flight, lifted off from Launch Complex 36 at Cape Canaveral on 13 "
  "November 2025 carrying NASA's two ESCAPADE probes, built by Rocket Lab, to study Mars's thin atmosphere. The "
  "reusable booster landed on a drone ship in the Atlantic, the first successful recovery of a New Glenn booster.",
  ["ESCAPADE: twin NASA Mars probes", "Rocket: Blue Origin's New Glenn (2nd flight)", "Launch: 13 Nov 2025, Cape Canaveral"],
  [fact("New Glenn launched NASA's two ESCAPADE probes on 13 November 2025 from Launch Complex 36, Cape Canaveral; "
        "probes built by Rocket Lab; booster landed on a drone ship", "intl_esc_upi"),
   fact("Blue Origin landed the New Glenn booster for the first time after the ESCAPADE launch", "intl_esc_space")],
  why="The sources name Blue Origin's New Glenn as the launch vehicle; the other rockets were not used.",
  current=ca("2025-11-13"))

G(T, GLB, "Intermediate",
  "At a White House dinner for Crown Prince Mohammed bin Salman on 18 November 2025, US President Donald Trump "
  "announced that Saudi Arabia would be given which status?",
  ["Major non-NATO ally", "NATO partner country", "Five Eyes partner", "Quad observer"], "*",
  "US-Saudi relations",
  "On 18 November 2025 Trump said he would designate Saudi Arabia a major non-NATO ally, a status held by about 20 "
  "countries including Israel, Qatar, Kuwait, Bahrain, Egypt, Tunisia and Jordan. A strategic defence agreement was "
  "signed the same day, and the crown prince pledged to raise Saudi investment in the US to nearly USD 1 trillion.",
  ["18 Nov 2025: Saudi Arabia to be major non-NATO ally", "Strategic defence agreement signed",
   "Investment pledge: ~USD 1 trillion"],
  [fact("Trump said on 18 November 2025, at a White House dinner for Mohammed bin Salman, that he would designate "
        "Saudi Arabia a major non-NATO ally; about 20 such allies; strategic defence agreement signed",
        "intl_saudi_cbs"),
   fact("Trump designates Saudi Arabia as major non-NATO ally", "intl_saudi_arab")],
  why="The sources report the major non-NATO ally designation; they mention none of the other statuses.",
  current=ca("2025-11-18"))

G(T, BIL, "Intermediate",
  "On 5 February 2026, in New Delhi, India signed the Terms of Reference for negotiating a free trade agreement with "
  "which regional grouping?",
  ["Gulf Cooperation Council (GCC)", "Eurasian Economic Union (EAEU)", "Mercosur", "Southern African Customs Union"],
  "*",
  "India's trade agreements",
  "India and the six-nation Gulf Cooperation Council signed the Terms of Reference for an FTA in New Delhi on 5 "
  "February 2026, in a ceremony presided over by Commerce and Industry Minister Piyush Goyal. The ToR set the scope "
  "and method of the negotiations.",
  ["5 Feb 2026, New Delhi", "India-GCC FTA Terms of Reference", "Presided over by Piyush Goyal"],
  [fact("India and the GCC signed Terms of Reference for an FTA in New Delhi on 5 February 2026, presided over by "
        "Piyush Goyal; six GCC countries", "intl_gcc_air"),
   fact("India, GCC sign ToR for free trade agreement negotiations", "intl_gcc_bs")],
  why="The sources concern the GCC; no ToR with the other groupings was signed on that date.",
  current=ca("2026-02-05"))

G(T, BIL, "Intermediate",
  "On 20 November 2025, Commerce and Industry Minister Piyush Goyal and Israel's Economy and Industry Minister Nir "
  "Barkat signed Terms of Reference to formally launch negotiations for which agreement?",
  ["Free Trade Agreement", "Bilateral Investment Treaty", "Double Taxation Avoidance Agreement",
   "Social Security Agreement"], "*",
  "India-Israel relations",
  "During Piyush Goyal's visit to Israel with a business delegation, he and Nir Barkat signed the Terms of Reference "
  "on 20 November 2025 to formally launch India-Israel FTA negotiations. The ToR cover market access for goods, "
  "investment facilitation, simpler customs procedures, services and cooperation on innovation and technology transfer.",
  ["20 Nov 2025: India-Israel ToR", "Signed by Piyush Goyal and Nir Barkat", "Launches FTA negotiations"],
  [fact("Piyush Goyal and Nir Barkat, Israel's Economy and Industry Minister, signed ToR to formally launch FTA "
        "negotiations; signed on Thursday 20 November 2025", "intl_isr_ob"),
   fact("India, Israel ink terms of reference to formally launch FTA talks (report dated 20 November 2025)",
        "intl_isr_week")],
  why="The sources say the ToR launch FTA negotiations, not the other agreements.",
  current=ca("2025-11-20"))

# ------------------------------------------------------------------ Advanced (1)
GS(T, GLB, "Advanced", "Kazakhstan's new Constitution",
   ["It was approved by about 87% of those who voted in a referendum held on 15 March 2026.",
    "It replaces the bicameral parliament with a single chamber, the Kurultai, of 145 deputies elected entirely "
    "through party lists.",
    "It abolishes the post of Vice-President."],
   [True, True, False],
   "Kazakhstan constitutional referendum, 2026",
   "In the referendum of 15 March 2026, 87.15% of voters (turnout 73.12%) backed the new Constitution. It abolishes the "
   "Senate and creates a unicameral parliament, the Kurultai, of 145 deputies elected for five years entirely by "
   "party-list proportional representation, and it entered into force on 1 July 2026. It creates (restores) the post "
   "of Vice-President rather than abolishing it, so statement 3 is wrong.",
   [fact("Referendum on 15 March 2026; 87.15% in favour; turnout 73.12%; unicameral Kurultai of 145 deputies, five-year "
         "terms, elected entirely by party lists; Senate abolished; in force from 1 July 2026", "intl_kz_cevro"),
    fact("New Constitution creates the position of Vice President; Kurultai replaces bicameral system; 87.15% yes",
         "intl_kz_tengri"),
    fact("Draft restores the vice-president post abolished in 1996; 87.15% yes, turnout 73.12%", "intl_kz_timesca")],
   why="Statement 3 is wrong: the sources say the new Constitution creates (restores) the Vice-President's post.",
   current=ca("2026-03-15"))

# ------------------------------------------------------------------ Summits and Conferences: Intermediate (1)
G("Summits and Conferences", "G20, BRICS, SCO and others", "Intermediate",
  "At the 67th Summit of Mercosur Heads of State, held in Foz do Iguaçu, Brazil, on 20 December 2025, Brazil handed "
  "over the bloc's pro tempore presidency to which country?",
  ["Paraguay", "Argentina", "Uruguay", "Bolivia"], "*",
  "Mercosur",
  "Brazil hosted the 67th Summit of Mercosur Heads of State and Associated States at Foz do Iguaçu, Paraná, on 20 "
  "December 2025, attended by President Lula. At its close Paraguay, under President Santiago Peña, took over the "
  "pro tempore presidency. The EU-Mercosur free trade agreement was not signed there; its signing was put off to "
  "January 2026.",
  ["67th Mercosur Summit: Foz do Iguaçu, 20 Dec 2025", "Pro tempore presidency: Brazil -> Paraguay",
   "EU-Mercosur FTA signing postponed"],
  [fact("67th Summit of Mercosur Heads of State and Associated States, Foz do Iguaçu, Paraná, Saturday 20 December "
        "2025", "intl_merc_gov"),
   fact("Paraguay took over the Mercosur pro tempore presidency from host Brazil at the 67th summit in Foz do Iguaçu; "
        "EU FTA not signed, postponed to January 2026", "intl_merc_mp")],
  why="The source says Paraguay, led by Santiago Peña, took over from Brazil; the other members did not.",
  current=ca("2025-12-20"))

# ###################################################################### part: appt (appointments + organizations + books)
# ###################################################################### part: appt (appointments, organisations, books)
U.update({
    "appt_breman_wiki": ("https://en.wikipedia.org/wiki/Anna_Breman", OPENED),
    "appt_breman_il": ("https://investinglive.com/centralbank/anna-breman-takes-charge-at-rbnz-pledging-focus-and-"
                       "credibility-20251201", OPENED),
    "appt_dolenc_bsi": ("https://www.bsi.si/en/media/posts/primoz-dolenc-took-up-the-position-of-governor-of-banka-"
                        "slovenije", OPENED),
    "appt_antony_air": ("https://newsonair.gov.in/vp-radhakrishnan-releases-book-advantage-india-reshaping-the-future-"
                        "for-an-equitable-world/", OPENED),
    "appt_murty_air": ("https://newsonair.gov.in/vice-president-c-p-radhakrishnan-releases-the-book-tides-of-time-"
                       "authored-by-mp-sudha-murty/", OPENED),
})

T_AP = "Important Appointments"
BFH, INTB = "Banking and finance heads", "International bodies"
T_OR = "National and International Organizations"
HQH, MEM = "Headquarters and heads", "Membership"
T_BK = "Books and Authors"
RB = "Recent books"

# ================================================================== Important Appointments
GS(T_AP, BFH, "Advanced", "Anna Breman's appointment as Governor of the Reserve Bank of New Zealand",
   ["She took office on 1 December 2025, succeeding Adrian Orr.",
    "Before this she was First Deputy Governor of Sveriges Riksbank, Sweden's central bank.",
    "She is the second woman to head the Reserve Bank of New Zealand."],
   [True, True, False],
   "Heads of foreign central banks",
   "Swedish economist Anna Breman, whose appointment was announced by Finance Minister Nicola Willis on 24 September "
   "2025, took office as Governor of the Reserve Bank of New Zealand on 1 December 2025 for a term ending 30 November "
   "2030. She succeeded Adrian Orr (Christian Hawkesby had acted in the interim). She had been First Deputy Governor of "
   "Sveriges Riksbank from September 2022 to October 2025. She is the first woman, and the first foreign national, to "
   "lead the RBNZ, so statement 3 is wrong.",
   [fact("Anna Breman took office as RBNZ Governor on 1 December 2025, term to 30 November 2030; predecessor Adrian Orr; "
         "First Deputy Governor of Sveriges Riksbank 2 Sep 2022-11 Oct 2025; first woman and first foreign national in "
         "the post; announced 24 Sep 2025 by Nicola Willis", "appt_breman_wiki"),
    fact("Breman takes office at RBNZ (1 Dec 2025), replacing Adrian Orr after interim governor Christian Hawkesby; "
         "earlier deputy governor of Sweden's Riksbank; first woman and first foreigner to lead the RBNZ",
         "appt_breman_il")],
   why="Statement 3 is wrong: the sources describe her as the first woman to lead the RBNZ, not the second.",
   current=ca("2025-12-01"))

G(T_AP, BFH, "Intermediate",
  "Primož Dolenc, confirmed by his country's National Assembly on 3 February 2026, took office on 1 March 2026 as the "
  "sixth Governor of which central bank, for a six-year term?",
  ["Banka Slovenije (Bank of Slovenia)", "Hrvatska narodna banka (Croatian National Bank)",
   "Národná banka Slovenska (National Bank of Slovakia)", "Česká národní banka (Czech National Bank)"], "*",
  "Heads of foreign central banks",
  "Primož Dolenc became the sixth Governor of Banka Slovenije, the central bank of Slovenia, on 1 March 2026. The "
  "National Assembly appointed him on 3 February 2026, by secret ballot with 55 votes in favour, on the proposal of the "
  "President of the Republic. The term is six years and the governor may be reappointed.",
  ["Dolenc: Governor, Banka Slovenije", "Appointed 3 Feb 2026; took office 1 Mar 2026", "Six-year term; sixth governor"],
  [fact("Primož Dolenc took up the position of Governor of Banka Slovenije on 1 March 2026; sixth Governor; six-year "
        "term; appointed by the National Assembly on 3 February 2026 on the President's proposal, 55 votes in favour",
        "appt_dolenc_bsi")],
  why="The source names Banka Slovenije; the other central banks are not the ones Dolenc heads.",
  current=ca("2026-03-01"))

# ================================================================== Books and Authors
G(T_BK, RB, "Basic",
  "'Advantage India: Reshaping the Future for an Equitable World', released by Vice-President C. P. Radhakrishnan in "
  "October 2026, was written by whom?",
  ["Anil K. Antony", "Shashi Tharoor", "Amitabh Kant", "Sanjeev Sanyal"], "*",
  "Recent books by Indian public figures",
  "Vice-President C. P. Radhakrishnan released 'Advantage India: Reshaping the Future for an Equitable World', written "
  "by Anil K. Antony, on 23 October 2026. The book examines India's transformation over the past decade.",
  ["Advantage India: Anil K. Antony", "Released by VP C. P. Radhakrishnan, 23 Oct 2026"],
  [fact("VP Radhakrishnan released 'Advantage India: Reshaping the Future for an Equitable World' authored by Anil K. "
        "Antony; article dated 23 October 2026", "appt_antony_air")],
  why="The source names Anil K. Antony as the author; the others did not write this book.",
  current=ca("2026-10-23"))

G(T_BK, RB, "Basic",
  "'Tides of Time', a book on the Parliamentary murals in the Samvidhan Sadan, released by Vice-President C. P. "
  "Radhakrishnan in New Delhi on 1 April 2026, was written by which Rajya Sabha MP?",
  ["Sudha Murty", "Kapil Sibal", "P. T. Usha", "Ilaiyaraaja"], "*",
  "Recent books by Indian public figures",
  "'Tides of Time', written by Rajya Sabha MP Sudha Murty, was released by Vice-President C. P. Radhakrishnan in New "
  "Delhi on 1 April 2026. It is about the beauty and symbolism of the Parliamentary murals in the Samvidhan Sadan.",
  ["Tides of Time: Sudha Murty", "Theme: murals of the Samvidhan Sadan", "Released by VP, 1 Apr 2026"],
  [fact("VP C P Radhakrishnan released 'Tides of Time' authored by MP Sudha Murty, on the Parliamentary murals in the "
        "Samvidhan Sadan; New Delhi; 1 April 2026", "appt_murty_air")],
  why="The source names Sudha Murty as the author; the other MPs did not write it.",
  current=ca("2026-04-01"))

# ------------------------------------------------------------------ more sources
U.update({
    "appt_akb_pdf": ("https://financialservices.gov.in/sites/default/files/Order-Notices/2026-09/Syed-Akbaruddin.pdf",
                     OPENED),
    "appt_dfs_p1": ("https://financialservices.gov.in/orders-and-notices?page=1", OPENED),
    "appt_dfs_p4": ("https://financialservices.gov.in/orders-and-notices?page=4", OPENED),
    "appt_hemmati_air": ("https://newsonair.gov.in/iran-appoints-new-central-bank-governor-amid-protests-over-plunging-"
                         "rial/", OPENED),
    "appt_anand_air": ("https://newsonair.gov.in/viswanathan-anand-takes-charge-as-fide-interim-president/", OPENED),
    "appt_sdf_wiki": ("https://en.wikipedia.org/wiki/SAARC_Development_Fund", OPENED),
    "appt_iosco_wiki": ("https://en.wikipedia.org/wiki/International_Organization_of_Securities_Commissions", OPENED),
    "appt_ebrd_wiki": ("https://en.wikipedia.org/wiki/European_Bank_for_Reconstruction_and_Development", OPENED),
    "appt_isdb_wiki": ("https://en.wikipedia.org/wiki/Islamic_Development_Bank", OPENED),
    "appt_acu_wiki": ("https://en.wikipedia.org/wiki/Asian_Clearing_Union", OPENED),
    "appt_chalice_air": ("https://newsonair.gov.in/vp-radhakrishnan-launches-book-chalice-of-ambrosia-ram-janmabhoomi-"
                         "challenge-response-in-new-delhi/", OPENED),
    "appt_agat_air": ("https://newsonair.gov.in/vice-president-releases-book-named-agatthiyar-the-unifier-at-"
                      "uprashtrapati-bhavan-in-new-delhi/", OPENED),
    "appt_iit_air": ("https://newsonair.gov.in/lok-sabha-speaker-om-birla-launches-book-on-indias-iit-ecosystem-in-new-"
                     "delhi/", OPENED),
    "appt_atal_air": ("https://newsonair.gov.in/vp-radhakrishnan-releases-book-atal-bihari-vajpayee-the-eternal-"
                      "statesman/", OPENED),
    "appt_celorio_ib": ("https://www.infobae.com/espana/cultura/2025/11/03/el-escritor-mexicano-gonzalo-celorio-ganador-"
                        "del-premio-cervantes-2025/", OPENED),
    "appt_cerv_wiki": ("https://en.wikipedia.org/wiki/Miguel_de_Cervantes_Prize", OPENED),
    "appt_vayalar_kk": ("https://www.keralakaumudi.com/en/KERALA/GENERAL/r-rajasree-bags-50th-vayalar-ramavarma-literary-"
                        "award-for-aathreyakam-1810992", OPENED),
    "appt_vayalar_wiki": ("https://en.wikipedia.org/wiki/Vayalar_Award", OPENED),
    "appt_wbf_air1": ("https://newsonair.gov.in/new-delhi-world-book-fair-2026-to-be-held-from-jan-10-to-jan-18/", OPENED),
    "appt_wbf_air2": ("https://newsonair.gov.in/53rd-new-delhi-world-book-fair-2026-kicks-off-with-focus-on-indian-"
                      "military-history/", OPENED),
    "appt_acu_uia": ("https://uia.org/s/or/en/1100043447", OPENED),
    "appt_acu_unb": ("https://unb.com.bd/category/Bangladesh/acus-dhaka-meeting-focuses-on-simplifying-cross-border-"
                     "transactions/154192", OPENED),
    "appt_bhaw_air": ("https://newsonair.gov.in/vp-radhakrishnan-releases-book-titled-sanskritir-ratna-bhandar-"
                      "bhaowaiyar-itibritto-in-new-delhi/", OPENED),
    "appt_dylan_wiki": ("https://en.wikipedia.org/wiki/Dylan_Thomas_Prize", OPENED),
    "appt_dylan_swan": ("https://www.swansea.ac.uk/cultural-institute/news-archive/swansea-university-dylan-thomas-prize-"
                        "2026-announces-shortlist/swansea-university-dylan-thomas-prize-2026-announces-shortlist.php",
                        OPENED),
})

# ================================================================== Important Appointments (contd.)
G(T_AP, BFH, "Basic",
  "Abdolnasser Hemmati, a former economy minister, was appointed governor of which country's central bank at the end "
  "of December 2025, after his predecessor resigned amid protests over the fall of the national currency?",
  ["Iran", "Iraq", "Pakistan", "Afghanistan"], "*",
  "Heads of foreign central banks",
  "Iran's Cabinet under President Masoud Pezeshkian appointed Abdolnasser Hemmati as governor of the Central Bank of "
  "Iran. His predecessor Mohammad Reza Farzin, in office since 2022, had resigned a day after large protests over the "
  "plunging rial. Hemmati had earlier served as minister of economic and financial affairs.",
  ["Hemmati: Governor, Central Bank of Iran", "Succeeded Mohammad Reza Farzin", "Context: fall of the rial"],
  [fact("Iran's Cabinet appointed Abdolnasser Hemmati as central bank governor after Mohammad Reza Farzin resigned amid "
        "protests over the plunging rial; Hemmati was earlier economy minister; report dated 1 January 2026, "
        "appointment made on the Wednesday before", "appt_hemmati_air")],
  why="The source concerns Iran's central bank and the rial; the other countries are not involved.",
  current=ca("2025-12-31", inferred="AIR report of 1 Jan 2026 says the Cabinet appointed him on Wednesday (31 Dec 2025)"))

G(T_AP, INTB, "Basic",
  "Five-time world chess champion Viswanathan Anand took charge in July 2026 as interim President of which body, after "
  "its President Arkady Dvorkovich was placed on a European Union sanctions list?",
  ["FIDE (International Chess Federation)", "All India Chess Federation", "European Chess Union",
   "International Olympic Committee"], "*",
  "Heads of international bodies",
  "Viswanathan Anand took charge as interim President of FIDE, the International Chess Federation, in July 2026. FIDE "
  "President Arkady Dvorkovich of Russia had been placed on the latest EU sanctions list, and Anand is to serve while "
  "Dvorkovich remains under restrictive measures under Swiss and EU laws.",
  ["Anand: interim President, FIDE (Jul 2026)", "Reason: EU sanctions on Arkady Dvorkovich"],
  [fact("Viswanathan Anand took charge as interim President of FIDE after FIDE President Arkady Dvorkovich was put on "
        "the EU sanctions list; to serve while Dvorkovich is under Swiss/EU restrictive measures; 24 July 2026",
        "appt_anand_air")],
  why="The source names FIDE, the world chess body headed by Dvorkovich; the other bodies are not involved.",
  current=ca("2026-07-24"))

GS(T_AP, BFH, "Advanced", "the appointment of Syed Akbaruddin to the Central Board of the Reserve Bank of India",
   ["He was appointed a part-time, non-official director under Section 8(1)(c) of the Reserve Bank of India Act, 1934.",
    "The appointment was made by the RBI Governor under the Banking Regulation Act, 1949.",
    "His term is four years from the date of the notification of 24 August 2026, or until further orders."],
   [True, False, True],
   "RBI Central Board",
   "By a notification of the Department of Financial Services dated 24 August 2026, the Central Government appointed "
   "Syed Akbaruddin as a part-time, non-official director on the Central Board of the RBI under clause (c) of Section "
   "8(1), read with Section 8(4), of the RBI Act, 1934, for four years from the date of the notification or until "
   "further orders. Statement 2 is wrong: the Central Government, not the RBI Governor, made the appointment, and under "
   "the RBI Act.",
   [fact("Notification dated 24 August 2026: Central Government appoints Syed Akbaruddin as part-time, non-official "
         "director on the RBI Central Board under Section 8(1)(c) read with 8(4) of the RBI Act, 1934, for four years from "
         "the date of issue or until further orders", "appt_akb_pdf"),
    fact("DFS orders list, published 24 August 2026: appointment of Syed Akbaruddin as part-time non-official director "
         "on the Central Board of RBI", "appt_dfs_p1")],
   why="Statement 2 is wrong: the notification is issued by the Central Government under the RBI Act, 1934.",
   current=ca("2026-08-24"))

GS(T_AP, BFH, "Advanced", "the Executive Director appointments in public sector banks notified in November 2025",
   ["Mini T. M., a Chief General Manager of Bank of Baroda, was appointed an Executive Director of Bank of Baroda.",
    "Sunil Kumar Chugh, a Chief General Manager of Punjab National Bank, was appointed an Executive Director of Canara "
    "Bank.",
    "Prabhat Kiran, a Chief General Manager of Canara Bank, was appointed an Executive Director of Bank of Maharashtra."],
   [False, True, True],
   "Whole-time directors of public sector banks",
   "The Department of Financial Services published a set of Executive Director appointments on 24 November 2025. "
   "Sunil Kumar Chugh (CGM, PNB) went to Canara Bank and Prabhat Kiran (CGM, Canara Bank) went to Bank of Maharashtra. "
   "Mini T. M., a CGM of Bank of Baroda, was appointed ED in Indian Bank, not in Bank of Baroda, so statement 1 is "
   "wrong.",
   [fact("DFS orders, 24 Nov 2025: Sunil Kumar Chugh, CGM PNB, as ED in Canara Bank; Prabhat Kiran, CGM Canara Bank, as "
         "ED in Bank of Maharashtra; Mini T M, CGM Bank of Baroda, as ED in Indian Bank", "appt_dfs_p4")],
   why="Statement 1 is wrong: the order posts Mini T. M. to Indian Bank.",
   current=ca("2025-11-24", inferred="publication date of the orders on the DFS Orders and Notices list"))

# ================================================================== National and International Organizations
G(T_OR, HQH, "Intermediate",
  "The SAARC Development Fund (SDF), whose charter was signed in 2008 and which funds social, economic and "
  "infrastructure projects in SAARC countries, has its permanent secretariat in which city?",
  ["Thimphu", "Kathmandu", "Dhaka", "Colombo"], "*",
  "Regional development institutions",
  "The SAARC Development Fund is headquartered in Thimphu, Bhutan. Its charter was signed on 3 August 2008 and its "
  "permanent secretariat was inaugurated in Thimphu on 28 April 2010. It works in three areas: social, economic and "
  "infrastructure.",
  ["SDF HQ: Thimphu, Bhutan", "Charter 2008; secretariat opened 2010", "Windows: social, economic, infrastructure"],
  [fact("SAARC Development Fund headquartered in Thimphu, Bhutan; charter signed 3 August 2008; secretariat inaugurated "
        "28 April 2010; three areas: social, economic, infrastructure", "appt_sdf_wiki")],
  why="The source places the SDF secretariat in Thimphu; the other capitals are not its seat.")

G(T_OR, HQH, "Intermediate",
  "The International Organization of Securities Commissions (IOSCO), the global standard-setter for securities "
  "regulation, has its permanent secretariat in which city?",
  ["Madrid", "Basel", "Paris", "Geneva"], "*",
  "Global financial standard-setters",
  "IOSCO, set up as a global body in 1983, has its permanent secretariat in Madrid, Spain; it moved there from "
  "Montreal in 1999. Its Objectives and Principles of Securities Regulation are endorsed by the G20 and the FSB, and "
  "with the Basel Committee and the IAIS it forms the Joint Forum of financial regulators.",
  ["IOSCO HQ: Madrid (from Montreal, 1999)", "Global body since 1983"],
  [fact("IOSCO headquarters Madrid, Spain; permanent secretariat moved from Montreal in 1999; founded 1983",
        "appt_iosco_wiki")],
  why="The source names Madrid as IOSCO's seat; it is not in Basel, Paris or Geneva.")

G(T_OR, HQH, "Intermediate",
  "The European Bank for Reconstruction and Development (EBRD), founded in 1991, of which India became a shareholder "
  "in July 2018, is headquartered in which city?",
  ["London", "Frankfurt", "Luxembourg", "Brussels"], "*",
  "Multilateral development banks",
  "The EBRD, founded in 1991, is headquartered in London (at Canary Wharf since 2022). India became a shareholder on "
  "11 July 2018. Its President is Odile Renaud-Basso.",
  ["EBRD HQ: London", "Founded 1991", "India joined: 11 Jul 2018"],
  [fact("EBRD headquarters London, United Kingdom; founded 1991; India a shareholder since 11 July 2018; President "
        "Odile Renaud-Basso", "appt_ebrd_wiki")],
  why="The source places the EBRD in London; the other cities are not its headquarters.")

G(T_OR, HQH, "Intermediate",
  "The Islamic Development Bank, founded in 1973 and operational since 1975, with 57 shareholding member states, is "
  "headquartered in which city?",
  ["Jeddah", "Riyadh", "Kuwait City", "Abu Dhabi"], "*",
  "Multilateral development banks",
  "The Islamic Development Bank is headquartered in Jeddah, Saudi Arabia. It was founded in 1973 by finance ministers "
  "at the first OIC finance ministers' meeting, began operations on 3 April 1975, and has 57 shareholding member "
  "states.",
  ["IsDB HQ: Jeddah", "Founded 1973; operations from 3 Apr 1975", "57 member states"],
  [fact("Islamic Development Bank headquarters Jeddah, Saudi Arabia; founded 1973; began operations 3 April 1975; 57 "
        "shareholding member states", "appt_isdb_wiki")],
  why="The source names Jeddah; the bank is not based in Riyadh, Kuwait City or Abu Dhabi.")

GS(T_OR, MEM, "Advanced", "the Asian Clearing Union (ACU)",
   ["It was established on 9 December 1974.",
    "Belarus is one of its member countries.",
    "It provides a mechanism for settling payments for intra-regional transactions among the participating central "
    "banks."],
   [True, True, True],
   "Regional payment arrangements",
   "The ACU was set up on 9 December 1974 (in Bangkok, at the initiative of ESCAP) so that participating central banks "
   "could settle payments for intra-regional transactions, cutting the use of foreign exchange reserves and transfer "
   "costs. Its members are Bangladesh, Bhutan, India, Iran, Maldives, Myanmar, Nepal, Pakistan and Sri Lanka, and "
   "Belarus, which attended the Dhaka meeting of February 2025 as a member country. All three statements are correct.",
   [fact("ACU established 9 December 1974 at ESCAP's initiative; members include India, Iran, Pakistan, Sri Lanka and "
         "others, with Belarus listed (2024)", "appt_acu_wiki"),
    fact("Asian Clearing Union founded 9 December 1974, Bangkok; settles payments for intra-regional transactions among "
         "participating central banks", "appt_acu_uia"),
    fact("ACU meeting in Dhaka, 19 February 2025: member countries attending included Myanmar, Pakistan, Belarus, Iran, "
         "India, Nepal and Bangladesh", "appt_acu_unb")],
   why="All three statements match the sources.")

# ================================================================== Books and Authors (contd.)
G(T_BK, RB, "Basic",
  "'Chalice of Ambrosia: Ram Janmabhoomi - Challenge and Response', launched by Vice-President C. P. Radhakrishnan in "
  "New Delhi in January 2026, was written by whom?",
  ["Surendra Kumar Pachauri", "Nripendra Misra", "Champat Rai", "Kishore Kunal"], "*",
  "Recent books by Indian public figures",
  "Vice-President C. P. Radhakrishnan launched 'Chalice of Ambrosia: Ram Janmabhoomi - Challenge and Response', written "
  "by Surendra Kumar Pachauri, a former Secretary to the Government of India, in New Delhi on 20 January 2026.",
  ["Author: Surendra Kumar Pachauri (former Secretary, GoI)", "Launched by VP, 20 Jan 2026"],
  [fact("VP Radhakrishnan launched 'Chalice of Ambrosia: Ram Janmabhoomi-Challenge and Response' by Surendra Kumar "
        "Pachauri, former secretary to the Government of India; New Delhi; 20 January 2026", "appt_chalice_air")],
  why="The source names Surendra Kumar Pachauri as the author; the others did not write this book.",
  current=ca("2026-01-20"))

G(T_BK, RB, "Basic",
  "Mexican novelist and essayist Gonzalo Celorio was announced on 3 November 2025 as the winner of which prize, worth "
  "€125,000 and awarded by Spain's Ministry of Culture?",
  ["Miguel de Cervantes Prize", "Princess of Asturias Award for Literature", "Prix Goncourt",
   "Neustadt International Prize for Literature"], "*",
  "Literary prizes",
  "Spain's Ministry of Culture announced on 3 November 2025 that Gonzalo Celorio, a Mexican essayist and novelist born "
  "in 1948 and a member of the Mexican Academy of the Language, had won the Miguel de Cervantes Prize 2025, worth "
  "€125,000. The prize, set up in 1975, honours the lifetime achievement of a writer in Spanish.",
  ["Cervantes Prize 2025: Gonzalo Celorio (Mexico)", "Announced 3 Nov 2025", "€125,000; Spain's Ministry of Culture"],
  [fact("Mexican writer Gonzalo Celorio wins the Cervantes Prize 2025, announced Monday 3 November 2025 by Spain's "
        "Ministry of Culture; 125,000 euros", "appt_celorio_ib"),
   fact("Cervantes Prize: established 1975 by Spain's Ministry of Culture, €125,000; 2025 winner Gonzalo Celorio "
        "(Mexico)", "appt_cerv_wiki")],
  why="The sources name the Cervantes Prize; the other prizes are different awards.",
  current=ca("2025-11-03"))

GS(T_BK, RB, "Advanced", "the 50th Vayalar Ramavarma Literary Award announced in October 2026",
   ["It was given to R. Rajasree for a collection of poems titled 'Aathreyakam'.",
    "The award carries ₹1 lakh, a bronze sculpture designed by Kanayi Kunhiraman and a citation.",
    "It is presented on 27 October, the death anniversary of the poet Vayalar Ramavarma."],
   [False, True, True],
   "Indian-language literary awards",
   "The 50th Vayalar Award, a Malayalam literary prize, went to R. Rajasree for her novel 'Aathreyakam', as reported on "
   "4 October 2026. It carries ₹1 lakh, a bronze sculpture designed by Kanayi Kunhiraman and a citation, and is "
   "presented on 27 October, Vayalar Ramavarma's death anniversary, in Thiruvananthapuram. Statement 1 is wrong because "
   "'Aathreyakam' is a novel.",
   [fact("R Rajasree bags 50th Vayalar Ramavarma Literary Award for her novel Aathreyakam; Rs 1 lakh, bronze sculpture by "
         "Kanayi Kunhiraman and citation; presentation 27 October, death anniversary; published 4 October 2026",
         "appt_vayalar_kk"),
    fact("Vayalar Award: best Malayalam literary work; ₹1,00,000; presented on 27 October; 2026 winner R. Rajasree, "
         "Aathreyakam", "appt_vayalar_wiki")],
   why="Statement 1 is wrong: the source calls Aathreyakam a novel.",
   current=ca("2026-10-04"))

GS(T_BK, RB, "Advanced", "the 53rd New Delhi World Book Fair held in January 2026",
   ["Its theme was 'Indian Military History: Valour and Wisdom @ 75'.",
    "Spain was the Guest of Honour country.",
    "It was held at Bharat Mandapam, and entry was free for the first time."],
   [True, False, True],
   "Book fairs",
   "The 53rd New Delhi World Book Fair, organised by the National Book Trust, was held at Bharat Mandapam from 10 to 18 "
   "January 2026 and inaugurated by Education Minister Dharmendra Pradhan. Its theme was 'Indian Military History: "
   "Valour and Wisdom @ 75'. Qatar was the Guest of Honour and Spain the Focus Country, so statement 2 is wrong. Entry "
   "was free for the first time.",
   [fact("53rd NDWBF, 10-18 January 2026, Bharat Mandapam; organised by NBT; theme Indian Military History: Valour and "
         "Wisdom @ 75; Guest of Honour Qatar; Focus Country Spain; free entry for the first time", "appt_wbf_air1"),
    fact("Fair inaugurated on 10 January 2026 by Dharmendra Pradhan; over 1,000 publishers from more than 35 countries",
         "appt_wbf_air2")],
   why="Statement 2 is wrong: Qatar was Guest of Honour; Spain was the Focus Country.",
   current=ca("2026-01-10"))

GS(T_BK, RB, "Advanced", "books released in New Delhi in 2026",
   ["'Agatthiyar - The Unifier', on the legacy of Sage Agatthiyar, was brought out by the Tamil magazine Kalaimagal and "
    "released by Vice-President C. P. Radhakrishnan.",
    "'Atal Bihari Vajpayee: The Eternal Statesman', released by the Vice-President in February 2026, is a coffee table "
    "book.",
    "'IIT - The Story of India's Most Prestigious Educational Ecosystem' was launched by the Vice-President."],
   [True, True, False],
   "Recent books by Indian public figures",
   "Vice-President C. P. Radhakrishnan released 'Agatthiyar - The Unifier', brought out by Kalaimagal magazine, on 15 "
   "June 2026, and the coffee table book 'Atal Bihari Vajpayee: The Eternal Statesman' on 21 February 2026. The book "
   "'IIT - The Story of India's Most Prestigious Educational Ecosystem' was launched on 20 June 2026 by Lok Sabha Speaker "
   "Om Birla, not by the Vice-President, so statement 3 is wrong.",
   [fact("VP released 'Agatthiyar - The Unifier', brought out by Kalaimagal magazine, on 15 June 2026", "appt_agat_air"),
    fact("VP Radhakrishnan released coffee table book 'Atal Bihari Vajpayee: The Eternal Statesman', 21 February 2026",
         "appt_atal_air"),
    fact("Lok Sabha Speaker Om Birla launched 'IIT - The Story of India's Most Prestigious Educational Ecosystem' in New "
         "Delhi on 20 June 2026", "appt_iit_air")],
   why="Statement 3 is wrong: the IIT book was launched by Lok Sabha Speaker Om Birla.",
   current=ca("2026-06-15"))

GS(T_BK, RB, "Advanced", "the book 'Sanskritir Ratna Bhandar: Bhaowaiyar Itibritto'",
   ["It traces the history of Bhawaiya, a folk music tradition of North Bengal, Assam and neighbouring regions.",
    "It was written by Lok Sabha MP Jayanta Kumar Roy and Sangita Roy.",
    "It was released by Vice-President C. P. Radhakrishnan in New Delhi in June 2026."],
   [True, True, True],
   "Recent books by Indian public figures",
   "Vice-President C. P. Radhakrishnan released 'Sanskritir Ratna Bhandar: Bhaowaiyar Itibritto' (Bhawaiya: A Cultural "
   "Treasure and Its Historical Journey) in New Delhi on 25 June 2026. Written by Lok Sabha MP Dr Jayanta Kumar Roy and "
   "Sangita Roy, it traces the history of Bhawaiya, a folk music tradition of North Bengal, Assam and nearby regions, "
   "and the cultural history of North Bengal and the Koch Rajbanshi community. All three statements are correct.",
   [fact("VP Radhakrishnan released 'Sanskritir Ratna Bhandar: Bhaowaiyar Itibritto' by Lok Sabha MP Dr Jayanta Kumar "
         "Roy and Sangita Roy in New Delhi; on Bhawaiya, folk music of North Bengal, Assam and nearby regions; article "
         "dated 25 June 2026", "appt_bhaw_air")],
   why="All three statements match the source.",
   current=ca("2026-06-25"))

GS(T_BK, RB, "Advanced", "the Swansea University Dylan Thomas Prize 2026",
   ["The winner was announced at a ceremony in Cardiff.",
    "It was won by American poet Sasha Debevec-McKenney for the poetry collection 'Joy is My Middle Name'.",
    "The prize is open to English-language writers aged 39 or under."],
   [False, True, True],
   "Literary prizes",
   "The 2026 Dylan Thomas Prize, for English-language writers aged 39 or under, was won by American poet Sasha "
   "Debevec-McKenney for the poetry collection 'Joy is My Middle Name' (Fitzcarraldo Editions). The winner was announced "
   "on 14 May 2026, International Dylan Thomas Day, at a ceremony in Swansea, not Cardiff, so statement 1 is wrong.",
   [fact("2026 shortlist includes Joy is My Middle Name by Sasha Debevec-McKenney (poetry); writers aged 39 or under; "
         "winner announced Thursday 14 May at a ceremony in Swansea on International Dylan Thomas Day", "appt_dylan_swan"),
    fact("2026 winner Sasha Debevec-McKenney, Joy is My Middle Name (Fitzcarraldo); cited Guardian report of 14 May 2026 "
         "calls the winner an American poet; prize open to English-language writers under forty", "appt_dylan_wiki")],
   why="Statement 1 is wrong: the ceremony was in Swansea.",
   current=ca("2026-05-14"))

# ###################################################################### part: awr (awards + reports)
# ###################################################################### part: awr (awards + reports)
U.update({
    # ---- Awards and Honours
    "awr_tilak_air": ("https://newsonair.gov.in/nsa-ajit-doval-receives-lokmanya-tilak-national-award-2026/", OPENED),
    "awr_tilak_ians": ("https://ianslive.in/nsa-ajit-doval-to-receive-lokmanya-tilak-national-award-today--"
                       "20260801070224", SEARCH),
    "awr_holberg_page": ("https://holbergprize.org/laureates/holbergprize/lyndal-roper/", OPENED),
    "awr_holberg_home": ("https://holbergprize.org/en", OPENED),
    "awr_zayed_kt": ("https://www.khaleejtimes.com/uae/zayed-award-for-human-fraternity-2026-winners", OPENED),
    "awr_shaw_aap": ("https://www.aap.com.au/aapreleases/cision20260527ae68781/", OPENED),
    "awr_japan_kyodo": ("https://kyodonewsprwire.jp/release/202601142440", OPENED),
    "awr_kfp_riyadh": ("https://alriyadhdaily.com/article/124db83466174bd8a9422cd3f8b343c7", OPENED),
    "awr_kfp_arab": ("https://www.arabnews.com/tags/king-faisal-prize-2026", OPENED),
    "awr_euromoney": ("https://www.euromoney.com/article/9aemiby4w34ss84wgw8kw4os/investment-banking/awards-for-"
                      "excellence-country-territory-winners-2026-india/", OPENED),
    "awr_bal_rb": ("https://dpl.rashtrapatibhavan.gov.in/view_datails/Mjc5NzA=", OPENED),
    "awr_bal_dd": ("https://www.devdiscourse.com/article/law-order/3742605-president-murmu-confers-pm-rashtriya-bal-"
                   "puraskar-hails-indias-young-heroes", OPENED),
    "awr_teach_fpj": ("https://www.freepressjournal.in/education/national-teachers-awards-2026-president-murmu-to-honour-"
                      "48-outstanding-school-teachers-on-september-5", OPENED),
    "awr_teach_tt": ("https://telanganatoday.com/president-murmu-confers-national-teachers-awards-on-48-educators",
                     SEARCH),
    "awr_kc_print": ("https://theprint.in/india/president-murmu-approves-78-gallantry-awards/3015293/", OPENED),
    "awr_kc_dc": ("https://www.deccanchronicle.com/nation/president-approves-78-gallantry-awards-1979222", OPENED),
    "awr_lasker": ("https://laskerfoundation.org/winners/orexin-a-brain-peptide-that-maintains-wakefulness/", OPENED),
    "awr_earth_news": ("https://earthshotprize.org/news/the-earthshot-prize-announces-2025-winners/", OPENED),
    "awr_earth_rio": ("https://earthshotprize.org/the-prize/rio-2025/", OPENED),
})

T = "Awards and Honours"
NAT, INTL = "National awards", "International awards"

# ------------------------------------------------------------------ Basic (1)
G(T, NAT, "Basic",
  "Who was presented the Lokmanya Tilak National Award 2026 by Union Home Minister Amit Shah in Pune on 1 August "
  "2026?",
  ["Ajit Doval", "S. Jaishankar", "Rajnath Singh", "Anil Chauhan"], "*",
  "Lokmanya Tilak National Award",
  "The Lokmanya Tilak National Award is given by the Lokmanya Tilak Smarak Trust. The 2026 award went to National "
  "Security Adviser Ajit Doval and was presented by Union Home Minister Amit Shah in Pune on 1 August 2026, the 106th "
  "death anniversary of Bal Gangadhar Tilak.",
  ["Lokmanya Tilak National Award 2026: NSA Ajit Doval", "Presented by Amit Shah, Pune, 1 Aug 2026",
   "Given by the Lokmanya Tilak Smarak Trust"],
  [fact("NSA Ajit Doval received the Lokmanya Tilak National Award 2026 from Amit Shah in Pune on 1 August 2026, the "
        "106th death anniversary of Tilak; award of the Lokmanya Tilak Smarak Trust", "awr_tilak_air"),
   fact("NSA Ajit Doval to receive the Lokmanya Tilak National Award on 1 August 2026", "awr_tilak_ians")],
  why="The sources name NSA Ajit Doval as the 2026 recipient; the other leaders were not.",
  current=ca("2026-08-01"))

# ------------------------------------------------------------------ Intermediate (10)
G(T, INTL, "Intermediate",
  "Australian scholar Lyndal Roper, Regius Professor of History at the University of Oxford and author of works on "
  "Reformation-era witch hunts and a biography of Martin Luther, was named the 2026 laureate of which prize?",
  ["Holberg Prize", "Templeton Prize", "Abel Prize", "Kyoto Prize"], "*",
  "Holberg Prize",
  "The Holberg Prize honours outstanding work in the humanities and social sciences. Its 2026 laureate is Lyndal "
  "Roper, Regius Professor of History at Oxford, recognised for pioneering work on early modern European history. "
  "Her books include 'Witch Craze' (2004) and 'Martin Luther: Renegade and Prophet' (2016). The 2026 prize was "
  "announced on 17 March 2026 and the award ceremony was held on 4 June 2026.",
  ["Holberg Prize 2026: Lyndal Roper (Oxford)", "Field: early modern European history",
   "Announced 17 Mar 2026; ceremony 4 Jun 2026"],
  [fact("Lyndal Roper, Australian scholar and Regius Professor of History at Oxford, is the 2026 Holberg Prize "
        "laureate for pioneering work on early modern European history; works on witch hunts and Martin Luther; "
        "announcement event 17 March 2026, award ceremony 4 June 2026", "awr_holberg_page"),
   fact("Lyndal Roper named the 2026 Holberg Prize laureate (Holberg Prize homepage)", "awr_holberg_home")],
  why="The Holberg Prize site names Roper as its 2026 laureate; the Templeton, Abel and Kyoto prizes did not go to "
      "her.",
  current=ca("2026-03-17"))

G(T, INTL, "Intermediate",
  "The 2026 Zayed Award for Human Fraternity, announced on 19 January 2026, honoured Afghan girls' education advocate "
  "Zarqa Yaftali and the peace agreement between which two countries?",
  ["Armenia and Azerbaijan", "Ethiopia and Eritrea", "Thailand and Cambodia", "Serbia and Kosovo"], "*",
  "Zayed Award for Human Fraternity",
  "The Zayed Award for Human Fraternity, started in 2019, is inspired by the Document on Human Fraternity signed by "
  "Pope Francis and Ahmed Al-Tayeb. Its 2026 honourees, announced on 19 January 2026, included the Armenia-Azerbaijan "
  "peace agreement and Afghan education advocate Zarqa Yaftali. The ceremony was set for 4 February 2026, the "
  "International Day of Human Fraternity, at the Founder's Memorial in Abu Dhabi.",
  ["2026 honourees: Armenia-Azerbaijan peace agreement, Zarqa Yaftali", "Award began in 2019",
   "Ceremony: 4 Feb 2026, Abu Dhabi"],
  [fact("2026 Zayed Award for Human Fraternity honourees announced 19 January 2026: the Armenia-Azerbaijan peace "
        "agreement and Afghan girls' education advocate Zarqa Yaftali; ceremony 4 February 2026 at the Founder's "
        "Memorial, Abu Dhabi; award started 2019", "awr_zayed_kt")],
  why="The source names the Armenia-Azerbaijan peace agreement; the other pairs were not honoured.",
  current=ca("2026-01-19"))

G(T, INTL, "Intermediate",
  "The Shaw Prize, whose 2026 laureates were announced in Hong Kong on 27 May 2026, is to add a new prize category "
  "from 2027. Which field is it?",
  ["Computer Science", "Chemistry", "Environmental Science", "Economics"], "*",
  "Shaw Prize",
  "The Shaw Prize has been awarded in Astronomy, Life Science and Medicine, and Mathematical Sciences, each carrying "
  "USD 1.2 million. The 2026 laureates included Ken'ichi Nomoto and Stanford Woosley (Astronomy) and Emmanuel Candes "
  "and Camillo De Lellis (Mathematical Sciences). The same announcement said a new Shaw Prize in Computer Science "
  "would be awarded from 2027.",
  ["Existing categories: Astronomy, Life Science and Medicine, Mathematical Sciences",
   "New from 2027: Computer Science", "Each prize: USD 1.2 million"],
  [fact("Announcement of the Shaw Laureates 2026, Hong Kong, 27 May 2026: three categories, USD 1.2 million each; a "
        "new Shaw Prize in Computer Science to be awarded from 2027", "awr_shaw_aap")],
  why="The announcement names Computer Science as the new category; the other fields are not being added.",
  current=ca("2026-05-27"))

G(T, INTL, "Intermediate",
  "American computer scientist Cynthia Dwork, awarded the 2026 Japan Prize in the field of Electronics, Information "
  "and Communication, is best known for pioneering which concept?",
  ["Differential privacy", "Public-key cryptography", "The PageRank algorithm", "The World Wide Web"], "*",
  "Japan Prize",
  "The Japan Prize Foundation announced the 2026 laureates on 21 January 2026. Cynthia Dwork (USA) won in "
  "Electronics, Information and Communication for research towards an ethical digital society, including differential "
  "privacy and fairness. The Life Sciences prize went to Shizuo Akira (Japan) and Zhijian 'James' Chen (USA) for "
  "discovering how innate immunity senses nucleic acids.",
  ["Japan Prize 2026 (announced 21 Jan 2026)", "Cynthia Dwork: differential privacy and fairness",
   "Life Sciences: Shizuo Akira, Zhijian Chen"],
  [fact("2026 Japan Prize announced 21 January 2026: Cynthia Dwork (USA), Electronics, Information and Communication, "
        "for research building an ethical digital society including differential privacy and fairness; Shizuo Akira "
        "and Zhijian Chen, Life Sciences", "awr_japan_kyodo")],
  why="The source credits Dwork with differential privacy; the other concepts are not cited for her prize.",
  current=ca("2026-01-21"))

G(T, INTL, "Intermediate",
  "Svetlana Mojsov of Rockefeller University won the King Faisal Prize 2026 in Medicine for discovering the "
  "biologically active form of which hormone, whose role in insulin secretion advanced obesity and diabetes treatment?",
  ["Glucagon-like peptide-1 (GLP-1)", "Leptin", "Ghrelin", "Insulin-like growth factor 1 (IGF-1)"], "*",
  "King Faisal Prize",
  "The King Faisal Prize laureates for the 48th session were announced on 7 January 2026. The Medicine prize, on the "
  "theme 'Discoveries Transforming Obesity Therapeutics', went to Svetlana Mojsov for discovering biologically active "
  "GLP-1 and its role as a potent insulin secretagogue. The Science prize (Mathematics) went to Carlos Kenig of the "
  "University of Chicago.",
  ["KFP 2026 announced 7 Jan 2026", "Medicine: Svetlana Mojsov (GLP-1)", "Science (Mathematics): Carlos Kenig"],
  [fact("King Faisal Prize 2026 announced 7 January 2026; Medicine ('Discoveries Transforming Obesity Therapeutics'): "
        "Svetlana Mojsov, Rockefeller University, for discovering biologically active GLP-1 and its role as an insulin "
        "secretagogue; Mathematics: Carlos Kenig", "awr_kfp_riyadh"),
   fact("Svetlana Mojsov honoured with the King Faisal Prize 2026 for laying the foundations of weight-loss drugs; "
        "article dated 16 April 2026", "awr_kfp_arab")],
  why="The source credits Mojsov with GLP-1; leptin, ghrelin and IGF-1 are not named in her citation.",
  current=ca("2026-01-07"))

G(T, NAT, "Intermediate",
  "In Euromoney's Awards for Excellence 2026 country awards for India, published in July 2026, which bank was named "
  "India's Best Bank?",
  ["HDFC Bank", "State Bank of India", "ICICI Bank", "Axis Bank"], "*",
  "Banking awards",
  "Euromoney's Awards for Excellence 2026 country and territory winners for India, published on 17 July 2026, named "
  "HDFC Bank as India's best bank, citing its leadership across every major segment of Indian banking in 2025.",
  ["Euromoney Awards for Excellence 2026", "India's Best Bank: HDFC Bank"],
  [fact("Euromoney Awards for Excellence country/territory winners 2026, India (17 July 2026): Best bank - HDFC Bank",
        "awr_euromoney")],
  why="The Euromoney page names HDFC Bank as India's best bank for 2026; the other banks were not.",
  current=ca("2026-07-17"))

G(T, NAT, "Intermediate",
  "President Droupadi Murmu conferred the Pradhan Mantri Rashtriya Bal Puraskar 2025 in New Delhi on 26 December "
  "2025. Which of the following is NOT one of the categories in which the award recognises children?",
  ["Academic excellence", "Bravery", "Environment", "Science and Technology"], "*",
  "Pradhan Mantri Rashtriya Bal Puraskar",
  "The Pradhan Mantri Rashtriya Bal Puraskar recognises exceptional achievements of children in six categories: "
  "Bravery, Social Service, Environment, Sports, Art and Culture, and Science and Technology. The 2025 awards were "
  "conferred by President Droupadi Murmu in New Delhi on 26 December 2025.",
  ["PMRBP 2025 conferred 26 Dec 2025 by President Murmu",
   "Categories: Bravery, Social Service, Environment, Sports, Art and Culture, Science and Technology"],
  [fact("President conferred the Pradhan Mantri Rashtriya Bal Puraskar on 26 December 2025 in New Delhi; categories: "
        "Bravery, Social Service, Environment, Sports, Art Culture and Science Technology", "awr_bal_rb"),
   fact("President Murmu conferred the PM Rashtriya Bal Puraskar in New Delhi on 26 December 2025 in the same six "
        "categories", "awr_bal_dd")],
  why="Bravery, Environment and Science and Technology are listed categories; academic excellence is not.",
  current=ca("2025-12-26"))

G(T, NAT, "Intermediate",
  "How many school teachers did President Droupadi Murmu honour with the National Teachers' Awards 2026 at Vigyan "
  "Bhawan, New Delhi, on Teachers' Day, 5 September 2026?",
  ["48", "50", "44", "46"], "*",
  "National Teachers' Awards",
  "The Ministry of Education selected 48 school teachers (26 men and 22 women) from 27 states, seven Union "
  "Territories and six Central Government organisations for the National Teachers' Awards 2026, through a three-stage "
  "district, state and national selection. President Droupadi Murmu presented the awards at Vigyan Bhawan on 5 "
  "September 2026.",
  ["48 school teachers: 26 men, 22 women", "27 states, 7 UTs, 6 central organisations", "Vigyan Bhawan, 5 Sep 2026"],
  [fact("48 school teachers (26 men, 22 women) from 27 states, seven UTs and six Central Government organisations to "
        "receive the National Teachers Awards 2026 from President Murmu at Vigyan Bhawan on 5 September 2026",
        "awr_teach_fpj"),
   fact("President Murmu confers National Teachers Awards on 48 educators (5 September 2026)", "awr_teach_tt")],
  why="The sources give 48 school teachers; the other numbers do not match.",
  current=ca("2026-09-05"))

G(T, NAT, "Intermediate",
  "On the eve of the 80th Independence Day in August 2026, President Droupadi Murmu approved 78 gallantry awards for "
  "the armed forces and CAPFs. How many Kirti Chakras, the second-highest peacetime gallantry award, were among them?",
  ["9", "7", "11", "5"], "*",
  "Gallantry awards",
  "On 14 August 2026 the President approved 78 gallantry awards, 13 of them posthumous. They included nine Kirti "
  "Chakras (seven posthumous), one Bar to Shaurya Chakra, 19 Shaurya Chakras, five Bars to Sena Medal (Gallantry), 36 "
  "Sena Medals (Gallantry), three Nao Sena Medals (Gallantry) and five Vayu Sena Medals (Gallantry).",
  ["78 awards, 13 posthumous", "Kirti Chakra: 9 (7 posthumous)", "Shaurya Chakra: 19"],
  [fact("President approved 78 gallantry awards on 14 August 2026 including 9 Kirti Chakras and 19 Shaurya Chakras",
        "awr_kc_print"),
   fact("78 gallantry awards, 13 posthumous; Kirti Chakra 9 (7 posthumous), the second-highest peacetime gallantry "
        "award; Shaurya Chakra 19", "awr_kc_dc")],
  why="Both sources give nine Kirti Chakras; seven is the number of posthumous Kirti Chakras, not the total.",
  current=ca("2026-08-14"))

G(T, INTL, "Intermediate",
  "Emmanuel Mignot and Masashi Yanagisawa received the 2026 Albert Lasker Basic Medical Research Award for identifying "
  "orexin, a brain peptide that maintains wakefulness, and showing that its deficiency causes which disorder?",
  ["Narcolepsy", "Insomnia", "Obstructive sleep apnoea", "Restless legs syndrome"], "*",
  "Lasker Awards",
  "The 2026 Albert Lasker Basic Medical Research Award honoured Emmanuel Mignot (Stanford University School of "
  "Medicine) and Masashi Yanagisawa (University of Tsukuba) for identifying orexin, a brain peptide that maintains "
  "wakefulness, and discovering that orexin deficiency causes uncontrolled sleep in narcolepsy.",
  ["Lasker Basic 2026: Mignot and Yanagisawa", "Orexin deficiency causes narcolepsy"],
  [fact("2026 Albert Lasker Basic Medical Research Award: Emmanuel Mignot and Masashi Yanagisawa, for identifying "
        "orexin and discovering that orexin deficiency causes uncontrolled sleep in narcolepsy (page dated 22 September "
        "2026)", "awr_lasker")],
  why="The citation names narcolepsy; the other sleep disorders are not mentioned.",
  current=ca("2026-09-22", inferred="Lasker page post date 22 Sep 2026; announcement day not stated on the page"))

# ------------------------------------------------------------------ Advanced (1)
GS(T, INTL, "Advanced", "the Earthshot Prize 2025",
   ["Its awards ceremony was held at the Museum of Tomorrow in Rio de Janeiro, the first time the Prize was held in "
    "Latin America.",
    "The City of Bogota won in the 'Clean Our Air' category.",
    "Each of the five winners receives GBP 5 million."],
   [True, True, False],
   "Earthshot Prize",
   "The Earthshot Prize 2025 winners were announced at the Awards Night on 5 November 2025 at the Museum of Tomorrow, "
   "Rio de Janeiro, the first time the Prize was held in Latin America. The winners were re.green (Brazil, Protect "
   "and Restore Nature), the City of Bogota (Colombia, Clean Our Air), the High Seas Treaty (Revive Our Oceans), Lagos "
   "Fashion Week (Nigeria, Build a Waste-Free World) and Friendship (Bangladesh, Fix Our Climate). Each winner "
   "receives GBP 1 million.",
   [fact("Earthshot Prize 2025 Awards Night on 5 November at the Museum of Tomorrow, Rio de Janeiro; first time the "
         "Prize was held in Latin America", "awr_earth_rio"),
    fact("2025 winners: re.green, City of Bogota (Clean Our Air), High Seas Treaty, Lagos Fashion Week, Friendship; "
         "GBP 1 million each", "awr_earth_news")],
   why="Statements 1 and 2 match the organiser's pages; statement 3 is wrong because each winner gets GBP 1 million.",
   current=ca("2025-11-05"))

# ---------------------------------------------------------------------- Important Reports and Indexes
U.update({
    "awr_gci_itu": ("https://www.itu.int/en/ITU-D/Cybersecurity/Pages/global-cybersecurity-index.aspx", OPENED),
    "awr_gem_unesco": ("https://www.unesco.org/gem-report/en", OPENED),
    "awr_eti_etv": ("https://www.etvbharat.com/en/business/global-energy-transition-readiness-dips-india-among-top-"
                    "gainers-wef-enn26061803354", OPENED),
    "awr_eti_utk": ("https://utkarsh.com/current-affairs/international/index-update/energy-transition-index-2026-india-"
                    "ranks-70th-among-top-improvers-globally", SEARCH),
    "awr_wjp_site": ("https://worldjusticeproject.org/rule-of-law-index/", OPENED),
    "awr_wjp_wiki": ("https://en.wikipedia.org/wiki/World_Justice_Project", OPENED),
    "awr_bready_wb": ("https://www.worldbank.org/en/businessready", OPENED),
    "awr_gwr_ubs": ("https://www.ubs.com/global/en/wealthmanagement/insights/global-wealth-report.html", OPENED),
    "awr_the_wur": ("https://www.timeshighereducation.com/world-university-rankings/latest/world-ranking", OPENED),
    "awr_gspi_bf": ("https://brandfinance.com/?p=37258", OPENED),
    "awr_gspi_dj": ("https://english.dainikjagranmpcg.com/international/global-soft-power-index-2026-india-at-32nd/"
                    "article-16521", OPENED),
    "awr_nri_site": ("https://networkreadinessindex.org/", OPENED),
})

T = "Important Reports and Indexes"
PUB, RANK = "Publishing body", "India's rank"

# ------------------------------------------------------------------ Basic (2)
G(T, PUB, "Basic",
  "The Global Cybersecurity Index, which assesses countries' commitment to cybersecurity, is published by which body?",
  ["International Telecommunication Union (ITU)", "World Economic Forum (WEF)", "INTERPOL",
   "Organisation for Economic Co-operation and Development (OECD)"], "*",
  "Global Cybersecurity Index",
  "The Global Cybersecurity Index (GCI) is published by the International Telecommunication Union through its "
  "Telecommunication Development Sector (ITU-D). Countries are scored on five pillars - Legal, Technical, "
  "Organizational, Capacity Development and Cooperation measures - which are combined into an overall score.",
  ["GCI: ITU (ITU-D)", "Five pillars: legal, technical, organisational, capacity development, cooperation"],
  [fact("The Global Cybersecurity Index is an ITU (ITU-D) publication; five pillars: Legal, Technical, Organizational, "
        "Capacity Development and Cooperation", "awr_gci_itu")],
  why="The ITU page presents the GCI as its own index; the other bodies do not publish it.")

G(T, PUB, "Basic",
  "The Global Education Monitoring (GEM) Report, which tracks progress towards the education targets of Sustainable "
  "Development Goal 4, is hosted and published by which organisation?",
  ["UNESCO", "UNICEF", "World Bank", "OECD"], "*",
  "Global Education Monitoring Report",
  "The GEM Report, established in 2002, is an editorially independent report hosted and published by UNESCO. It "
  "monitors progress systematically towards the targets in SDG 4 on education.",
  ["GEM Report: hosted and published by UNESCO", "Monitors SDG 4 (education)", "Established 2002"],
  [fact("The GEM Report, established in 2002, is an editorially independent report hosted and published by UNESCO, "
        "monitoring progress towards the targets of SDG 4 on education", "awr_gem_unesco")],
  why="UNESCO's own page states that it hosts and publishes the GEM Report; the other bodies do not.")

# ------------------------------------------------------------------ Intermediate (5)
G(T, RANK, "Intermediate",
  "In the World Economic Forum's Energy Transition Index 2026, released on 18 June 2026, what was India's rank among "
  "120 countries?",
  ["70th", "74th", "63rd", "81st"], "*",
  "Energy Transition Index",
  "The Energy Transition Index is published by the World Economic Forum, developed with Accenture. In the 2026 edition "
  "India rose two places to 70th among 120 countries. Sweden, Finland and Denmark kept the top three spots, and global "
  "transition readiness fell for the first time in more than a decade.",
  ["ETI: WEF (with Accenture)", "2026: India 70th of 120, up two places", "Top 3: Sweden, Finland, Denmark"],
  [fact("Energy Transition Index 2026 (WEF with Accenture), released 18 June 2026: India 70th of 120 countries, up "
        "two places; Sweden, Finland, Denmark top three", "awr_eti_etv"),
   fact("Energy Transition Index 2026: India improved two places to 70th with a score of 54.9", "awr_eti_utk")],
  why="The sources give India's 2026 rank as 70th; the other ranks do not match.",
  current=ca("2026-06-18"))

G(T, PUB, "Intermediate",
  "The Rule of Law Index, which measures the rule of law in countries across eight factors, is published by which "
  "organisation?",
  ["World Justice Project", "Transparency International", "Freedom House", "International Commission of Jurists"],
  "*",
  "Rule of Law Index",
  "The Rule of Law Index is published, typically every year, by the World Justice Project, an independent "
  "organisation headquartered in Washington, D.C. It measures the rule of law across eight factors; the 2024 edition "
  "ranked 142 countries and jurisdictions, with Denmark first.",
  ["Rule of Law Index: World Justice Project (Washington, D.C.)", "Eight factors", "2024: 142 countries, Denmark 1st"],
  [fact("The WJP Rule of Law Index (index page on the World Justice Project website)", "awr_wjp_site"),
   fact("WJP publishes the Rule of Law Index, typically annually; eight factors; 2024 edition ranks 142 countries, "
        "Denmark first; WJP headquartered in Washington, D.C.", "awr_wjp_wiki")],
  why="The sources name the World Justice Project as the publisher; the other organisations are not.")

G(T, PUB, "Intermediate",
  "B-READY (Business Ready), a report that assesses the regulatory framework and public services directed at firms "
  "in economies worldwide, is published by which institution?",
  ["World Bank Group", "International Monetary Fund", "World Trade Organization", "World Economic Forum"], "*",
  "B-READY report",
  "B-READY is a World Bank Group report that assesses the regulatory framework and public services directed at firms. "
  "Its pilot editions are to cover about 170 economies gradually.",
  ["B-READY: World Bank Group", "Assesses regulation and public services for firms", "To cover about 170 economies"],
  [fact("B-READY assesses the regulatory framework and public services directed at firms; World Bank Group site; "
        "first three editions to gradually cover about 170 economies", "awr_bready_wb")],
  why="B-READY appears on the World Bank Group's site as its own report; the other institutions do not publish it.")

G(T, PUB, "Intermediate",
  "The Global Wealth Report, which covers 56 key markets estimated to hold over 92% of the world's wealth, is published "
  "by which financial institution?",
  ["UBS", "Credit Suisse", "Knight Frank", "Capgemini"], "*",
  "Global Wealth Report",
  "The Global Wealth Report is published by UBS as part of its Wealth Intelligence reports. The report covers 56 key "
  "markets that UBS estimates account for over 92% of the world's wealth; the 2026 edition is its seventeenth.",
  ["Global Wealth Report: UBS", "56 markets, over 92% of world wealth"],
  [fact("UBS Global Wealth Report, part of UBS Wealth Intelligence, 'now in its seventeenth edition' (2026), covering "
        "56 key markets (over 92% of world wealth)", "awr_gwr_ubs")],
  why="The report's own page shows UBS as the publisher; the other firms are not.")

G(T, PUB, "Intermediate",
  "The 'World University Rankings', not to be confused with the QS rankings, are published by which organisation?",
  ["Times Higher Education (THE)", "U.S. News & World Report", "ShanghaiRanking Consultancy",
   "Centre for World University Rankings (CWUR)"], "*",
  "Global university rankings",
  "The World University Rankings are published by Times Higher Education (THE). In the 2027 edition the University "
  "of Oxford ranked first for the 11th consecutive year.",
  ["World University Rankings: Times Higher Education", "2027 edition: Oxford 1st for the 11th year running"],
  [fact("Times Higher Education World University Rankings 2027: University of Oxford first for an 11th consecutive "
        "year", "awr_the_wur")],
  why="The rankings page belongs to Times Higher Education; the other bodies publish separate rankings.")

# ------------------------------------------------------------------ Advanced (2)
GS(T, RANK, "Advanced", "the Brand Finance Global Soft Power Index 2026",
   ["India was ranked 32nd with a score of 48.0, two places lower than in 2025.",
    "China overtook the United States to top the index.",
    "Japan overtook the United Kingdom to take third place."],
   [True, False, True],
   "Global Soft Power Index",
   "Brand Finance released the Global Soft Power Index 2026 on 27 January 2026 at the Global Soft Power Summit held "
   "alongside the World Economic Forum in Davos. It covers all 193 UN member states. The United States stayed first "
   "(74.9), China was second (73.5), and Japan (70.6) overtook the United Kingdom for third place. India fell two "
   "places to 32nd with a score of 48.0.",
   [fact("Global Soft Power Index 2026 released 27 January 2026 at the Global Soft Power Summit alongside the WEF in "
         "Davos; covers 193 UN member states; US 1st; Japan 3rd, overtaking the UK (4th)", "awr_gspi_bf"),
    fact("Global Soft Power Index 2026: India 32nd with 48.0, down 1.8 points and two places; US 74.9, China 73.5, "
         "Japan 70.6, UK 69.2", "awr_gspi_dj")],
   why="Statements 1 and 3 match the sources; statement 2 is wrong because the United States remained first and China "
       "was second.",
   current=ca("2026-01-27"))

GS(T, PUB, "Advanced", "the Network Readiness Index (NRI)",
   ["It is published under the auspices of the Portulans Institute.",
    "It was originally launched in 2002 with the International Telecommunication Union."],
   [True, False],
   "Network Readiness Index",
   "The Network Readiness Index is published under the auspices of the Portulans Institute. It was originally "
   "launched in 2002 with the World Economic Forum, not the ITU.",
   [fact("NRI published under the auspices of the Portulans Institute; originally launched in 2002 with the World "
         "Economic Forum", "awr_nri_site")],
   why="Statement 1 matches the NRI site; statement 2 is wrong because the NRI was launched with the World Economic "
       "Forum.")

# ###################################################################### part: ssd (sports + days)
# ###################################################################### part: ssd (sports + important days)
U.update({
    "ssd_kab_air": ("https://www.newsonair.gov.in/india-beat-chinese-taipei-35-28-to-win-their-second-consecutive-"
                    "womens-kabaddi-world-cup", OPENED),
    "ssd_kab_bridge": ("https://thebridge.in/kabaddi/india-win-womens-kabaddi-world-cup-2025-final-55281", SEARCH),
    "ssd_blind_trib": ("https://www.tribuneindia.com/news/sports/india-win-inaugural-t20-blind-womens-world-cup-after-"
                       "defeating-nepal-by-seven-wickets", OPENED),
    "ssd_squash_tt": ("https://telanganatoday.com/india-wins-maiden-squash-world-cup-title-after-beating-hong-kong-in-"
                      "final", OPENED),
    "ssd_smi_wiki": ("https://en.wikipedia.org/wiki/2025_Syed_Modi_International", OPENED),
    "ssd_wauc_nbc": ("https://www.nbcsports.com/olympics/news/world-athletics-ultimate-championship-results-2026",
                     OPENED),
    "ssd_f1_aus": ("https://www.formula1.com/en/latest/article/russell-wins-action-packed-australian-gp-from-antonelli-"
                   "as-mercedes-secure-1.4WRxPAtF4dFtrKCsWIiQX2", OPENED),
    "ssd_lakshya_trib": ("https://www.tribuneindia.com/news/sports/lakshya-sen-wins-australian-open-2025-beats-japans-"
                         "yushi-tanaka-21-15-21-11", OPENED),
    "ssd_kiug_bridge": ("https://thebridge.in/khelo-india-university-games/2025-chandigarh-university-champions-55383",
                        OPENED),
    "ssd_kiug_stat": ("https://www.thestatesman.com/sports/rajasthan-to-host-5th-khelo-india-university-games-from-"
                      "november-24-to-december-5-2025-1503503575.html", SEARCH),
    "ssd_rapid_air": ("https://www.newsonair.gov.in/arjun-erigaisi-and-koneru-humpy-win-bronze-at-2025-fide-world-"
                      "rapid-championships/", OPENED),
    "ssd_ashes_nx": ("https://www.newsx.com/sports/ashes-2025-2026-australia-clinch-series-4-1-with-scg-triumph-over-"
                     "england-mitchell-starc-named-player-of-the-series-142405", OPENED),
    "ssd_ind_sa_sky": ("https://www.skysports.com/cricket/news/12123/13475525/india-vs-south-africa-visitors-clinch-"
                       "first-test-series-win-on-indian-soil-in-25-years-after-408-run-victory", OPENED),
    "ssd_ind_sa_dh": ("https://www.deccanherald.com/sports/cricket/india-vs-south-africa-harmer-the-wrecker-in-chief-"
                      "again-as-proteas-complete-series-win-3810679", SEARCH),
    "ssd_u19_outlook": ("https://www.outlookindia.com/sports/cricket/india-vs-england-live-streaming-icc-under-19-world-"
                        "cup-2026-final-result-toss-playing-xis", OPENED),
    "ssd_box_wb": ("https://worldboxing.org/home-nation-india-tops-the-medal-table-with-nine-golds-on-superb-final-day-"
                   "of-action-at-world-boxing-cup-finals-greater-noida-2025/", OPENED),
    "ssd_deaf_trib": ("https://www.tribuneindia.com/news/sports/pm-modi-lauds-performance-of-athletes-at-deaflympics-in-"
                      "tokyo", OPENED),
    "ssd_para_air": ("https://newsonair.gov.in/india-shine-at-asian-para-games-2026-with-record-114-medal-haul/", OPENED),
    # added in review: Hangzhou tally per the Paralympic Committee of India (seen in search results only)
    "pci_apg_111": ("https://www.paralympicindia.org.in/india-team-creates-historical-with-111-medals-at-apg", SEARCH),
    "ssd_issf_bridge": ("https://thebridge.in/shooting/issf-world-cup-final-zoravar-sandhu-finish-7th-india-win-6-medals-"
                        "55408", OPENED),
    "ssd_day_edu": ("https://www.un.org/en/observances/education-day", OPENED),
    "ssd_day_forest": ("https://www.fao.org/international-day-of-forests/en", OPENED),
    "ssd_day_radio": ("https://www.un.org/en/observances/radio-day", OPENED),
    "ssd_day_youth": ("https://www.un.org/en/observances/youth-day", OPENED),
    "ssd_day_girl": ("https://www.un.org/en/observances/girl-child-day", OPENED),
    "ssd_day_girl_unicef": ("https://www.unicef.org/gender-equality/international-day-girl", SEARCH),
    "ssd_day_older": ("https://www.un.org/en/observances/older-persons-day", OPENED),
})

T = "Sports"
TW, VR = "Tournaments and winners", "Venues and records"

# ------------------------------------------------------------------ Basic (8)
G(T, TW, "Basic",
  "India retained the Women's Kabaddi World Cup in Dhaka in November 2025, winning the final 35-28. Which team did "
  "India beat in the final?",
  ["Chinese Taipei", "Iran", "Bangladesh", "Nepal"], "*",
  "Women's Kabaddi World Cup 2025",
  "India beat Chinese Taipei 35-28 in the final in Dhaka to win a second straight Women's Kabaddi World Cup. Eleven "
  "countries took part. In the semi-finals India beat Iran 33-21 and Chinese Taipei beat hosts Bangladesh 25-18.",
  ["Final: India 35-28 Chinese Taipei, Dhaka", "India's second consecutive title"],
  [fact("India beat Chinese Taipei 35-28 in Dhaka for a second straight Women's Kabaddi World Cup; semi-finals India "
        "33-21 Iran, Chinese Taipei 25-18 Bangladesh; 11 countries", "ssd_kab_air"),
   fact("Final held on 24 November 2025 in Dhaka", "ssd_kab_bridge")],
  why="Iran and Bangladesh lost in the semi-finals, per the source; Nepal did not reach the final.",
  current=ca("2025-11-24"))

G(T, TW, "Basic",
  "India won the inaugural Women's T20 World Cup for the Blind on 23 November 2025 in Colombo. Which team did India "
  "beat by seven wickets in the final?",
  ["Nepal", "Pakistan", "Sri Lanka", "Australia"], "*",
  "Women's T20 World Cup for the Blind 2025",
  "In the first-ever Women's T20 World Cup for the Blind, India, led by Deepika TC, beat Nepal by seven wickets in the "
  "final in Colombo. Nepal made 114/5; Phula Saren (44 off 27 balls) was Player of the Match. India went through the "
  "tournament unbeaten and beat Australia in the semi-final.",
  ["Inaugural edition", "Final: India beat Nepal by 7 wickets, Colombo, 23 Nov 2025"],
  [fact("Inaugural Women's T20 World Cup for the Blind; India beat Nepal by seven wickets in Colombo on 23 November "
        "2025; Nepal 114/5; Phula Saren Player of the Match; captain Deepika TC; India beat Australia in the semi-final",
        "ssd_blind_trib")],
  why="The source names Nepal as the finalist; India beat Australia in the semi-final and Pakistan and Sri Lanka in "
      "earlier matches.",
  current=ca("2025-11-23"))

G(T, TW, "Basic",
  "India won its first Squash World Cup title in Chennai on 14 December 2025, beating the top seeds 3-0 in the final. "
  "Who were India's opponents in the final?",
  ["Hong Kong, China", "Egypt", "Japan", "Malaysia"], "*",
  "WSF Squash World Cup 2025",
  "At Express Avenue Mall, Chennai, India beat top seeds Hong Kong, China 3-0 in the final, with wins by Joshna "
  "Chinappa, Abhay Singh and Anahat Singh. India, which had beaten two-time champions Egypt 3-0 in the semi-final, "
  "became the first Asian nation and only the fourth country, after Australia, England and Egypt, to win the title.",
  ["Final: India 3-0 Hong Kong, China", "First Asian winner; fourth country to win"],
  [fact("India beat Hong Kong 3-0 in the final at Express Avenue Mall, Chennai, on Sunday 14 December 2025; Joshna "
        "Chinappa, Abhay Singh, Anahat Singh won; Egypt beaten 3-0 in the semi-final; first Asian nation and fourth "
        "country after Australia, England and Egypt", "ssd_squash_tt")],
  why="Egypt lost to India in the semi-final, per the source; Japan and Malaysia did not play the final.",
  current=ca("2025-12-14"))

G(T, VR, "Basic",
  "India's Kidambi Srikanth finished runner-up in the men's singles at the Syed Modi International badminton "
  "tournament held in Lucknow from 25 to 30 November 2025. Who beat him in the final?",
  ["Jason Gunawan", "Lakshya Sen", "Lee Zii Jia", "Loh Kean Yew"], "*",
  "Syed Modi International 2025",
  "The 2025 Syed Modi International was held at the Babu Banarasi Das Indoor Stadium, Lucknow, from 25 to 30 November "
  "2025. Hong Kong's Jason Gunawan beat Kidambi Srikanth 21-16, 8-21, 22-20 in the men's singles final. Japan's Hina "
  "Akechi won the women's singles, beating Turkey's Neslihan Arin.",
  ["Venue: BBD Indoor Stadium, Lucknow, 25-30 Nov 2025", "Men's singles: Jason Gunawan bt Kidambi Srikanth"],
  [fact("2025 Syed Modi International, 25-30 November 2025, Babu Banarasi Das Indoor Stadium, Lucknow; men's singles "
        "final Jason Gunawan (Hong Kong) bt Srikanth Kidambi 21-16, 8-21, 22-20; women's singles Hina Akechi bt "
        "Neslihan Arin", "ssd_smi_wiki")],
  why="The source names Jason Gunawan as the men's singles champion; the other players did not beat Srikanth in the "
      "final.",
  current=ca("2025-11-30", inferred="source gives tournament dates 25-30 Nov 2025; final taken as the last day"))

G(T, VR, "Basic",
  "The inaugural World Athletics Ultimate Championship, a new season-ending event, was held from 11 to 13 September "
  "2026 in which city?",
  ["Budapest", "Tokyo", "Zurich", "Brussels"], "*",
  "World Athletics Ultimate Championship",
  "The first World Athletics Ultimate Championship was held in Budapest, Hungary, from 11 to 13 September 2026. "
  "Winners included Kenny Bednarek (men's 100m, 9.85 s), Melissa Jefferson-Wooden (women's 100m, 10.62 s) and Sri "
  "Lanka's Rumesh Pathirage (men's javelin, 91.09 m).",
  ["Venue: Budapest, 11-13 Sep 2026"],
  [fact("World Athletics Ultimate Championship held 11-13 September 2026 in Budapest, Hungary; Bednarek 9.85, "
        "Jefferson-Wooden 10.62, Rumesh Pathirage javelin 91.09 m", "ssd_wauc_nbc")],
  why="The source names Budapest as the host city.",
  current=ca("2026-09-11"))

G(T, TW, "Basic",
  "Who won the 2026 Australian Grand Prix at Albert Park, Melbourne, on 8 March 2026, the first Formula One race "
  "under the new technical regulations?",
  ["George Russell", "Kimi Antonelli", "Charles Leclerc", "Lando Norris"], "*",
  "Formula One 2026 season opener",
  "George Russell won the 2026 Australian Grand Prix for Mercedes, his sixth career win, ahead of team-mate Kimi "
  "Antonelli, giving Mercedes a 1-2. Charles Leclerc (Ferrari) was third. It was the first race of the season under "
  "a wave of new technical regulations.",
  ["Winner: George Russell (Mercedes)", "2nd Antonelli, 3rd Leclerc"],
  [fact("Russell won the Australian GP at Albert Park, Melbourne, on 8 March 2026 ahead of Antonelli (Mercedes 1-2), "
        "Leclerc third, Norris fifth; first race under new technical regulations", "ssd_f1_aus")],
  why="Per the source Antonelli was second, Leclerc third and Norris fifth.",
  current=ca("2026-03-08"))

G(T, TW, "Basic",
  "Lakshya Sen won the Australian Open Super 500 badminton title in Sydney on 23 November 2025 by beating which player "
  "21-15, 21-11 in the final?",
  ["Yushi Tanaka", "Chou Tien Chen", "Ayush Shetty", "Kunlavut Vitidsarn"], "*",
  "BWF World Tour 2025",
  "Lakshya Sen beat Japan's Yushi Tanaka 21-15, 21-11 in a 38-minute final in Sydney to win the Australian Open Super "
  "500, his first title of the 2025 BWF World Tour, without dropping a game.",
  ["Final: Lakshya Sen bt Yushi Tanaka 21-15, 21-11", "Sydney, 23 Nov 2025"],
  [fact("Lakshya Sen beat Japan's Yushi Tanaka 21-15, 21-11 in Sydney on Sunday 23 November 2025 to win the Australian "
        "Open Super 500, his first title of the 2025 World Tour", "ssd_lakshya_trib")],
  why="The source names Yushi Tanaka as the final opponent; the other players were not his final opponent.",
  current=ca("2025-11-23"))

G(T, TW, "Basic",
  "Which university retained the overall title at the Khelo India University Games 2025, held in Rajasthan, with 42 "
  "gold medals?",
  ["Chandigarh University", "Lovely Professional University", "Jain University", "Guru Nanak Dev University"], "*",
  "Khelo India University Games 2025",
  "The fifth Khelo India University Games were held in Rajasthan from 24 November to 5 December 2025. Chandigarh "
  "University defended its overall title with 67 medals (42 gold, 14 silver, 11 bronze); Lovely Professional "
  "University was runner-up. Swimmer Srihari Nataraj of Jain University was the most successful athlete with nine "
  "golds.",
  ["Champion: Chandigarh University (42 gold)", "Runner-up: LPU", "Host: Rajasthan"],
  [fact("Chandigarh University retained the overall title with 42 gold, 14 silver, 11 bronze; LPU runner-up; Srihari "
        "Nataraj (Jain University) nine golds; Games closed 5 December 2025 in Rajasthan", "ssd_kiug_bridge"),
   fact("Rajasthan to host 5th Khelo India University Games from 24 November to 5 December 2025", "ssd_kiug_stat")],
  why="The source lists LPU as runner-up and Jain University for Srihari Nataraj's medals, not the overall title.",
  current=ca("2025-12-05"))

# ------------------------------------------------------------------ Intermediate (2)
G(T, TW, "Intermediate",
  "At the FIDE World Rapid Championships 2025 in Doha, where Magnus Carlsen won his sixth open title, who won the "
  "women's title, with India's Koneru Humpy taking bronze?",
  ["Aleksandra Goryachkina", "Zhu Jiner", "Ju Wenjun", "Bibisara Assaubayeva"], "*",
  "World Rapid Chess Championship 2025",
  "Russia's Aleksandra Goryachkina won the women's World Rapid title in Doha in December 2025. Magnus Carlsen took his "
  "sixth open World Rapid title. India's Arjun Erigaisi (open) and Koneru Humpy (women) won bronze; Humpy had won the "
  "women's title in 2019 and 2024.",
  ["Women's champion: Goryachkina", "Open: Carlsen (6th title)", "Bronze: Erigaisi, Humpy"],
  [fact("Carlsen won his sixth World Rapid title; women's champion Alexandra Goryachkina; Arjun Erigaisi and Koneru "
        "Humpy won bronze in Doha; article dated 29 December 2025 says the event ended the previous day",
        "ssd_rapid_air")],
  why="The source names Goryachkina as women's champion; the other players did not win the 2025 women's rapid title.",
  current=ca("2025-12-28", inferred="article dated 29 Dec 2025 says the event concluded 'yesterday'"))

G(T, TW, "Intermediate",
  "Australia won the 2025-26 Ashes series 4-1, sealing it with a five-wicket win at the Sydney Cricket Ground in "
  "January 2026. Who was named Player of the Series?",
  ["Mitchell Starc", "Travis Head", "Pat Cummins", "Joe Root"], "*",
  "The Ashes 2025-26",
  "Australia won the first three Tests and the fifth, at Sydney, by five wickets while chasing 160, to take the "
  "series 4-1. Fast bowler Mitchell Starc was named Player of the Series, while Travis Head was Player of the Match "
  "in the Sydney Test.",
  ["Series: Australia 4-1", "Player of the Series: Mitchell Starc", "Sydney Test PoM: Travis Head"],
  [fact("Australia beat England by five wickets chasing 160 at the SCG to win the series 4-1; Mitchell Starc Player of "
        "the Series; Travis Head Player of the Match; article published 8 January 2026", "ssd_ashes_nx")],
  why="The source names Head as Player of the Match in Sydney, not of the series; Cummins and Root are not named.",
  current=ca("2026-01-08", inferred="source article dated 8 Jan 2026 reports the final-day result"))

# ------------------------------------------------------------------ Advanced (6)
GS(T, TW, "Advanced", "South Africa's Test tour of India in November 2025",
   ["South Africa won the two-match series 2-0, its first Test series win in India in 25 years.",
    "South Africa's 408-run win in the second Test was its biggest winning margin over India in Tests.",
    "Marco Jansen was named Player of the Series."],
   (True, True, False),
   "India vs South Africa Test series 2025",
   "South Africa won the first Test in Kolkata by 30 runs and the second at Guwahati by 408 runs, its biggest Test win "
   "over India, to take the series 2-0 and win a Test series in India for the first time in 25 years. Off-spinner "
   "Simon Harmer, with 17 wickets, was Player of the Series; Marco Jansen was Player of the Match at Guwahati.",
   [fact("South Africa won 2-0 with a 408-run win, its biggest margin over India in Tests and first series win in India "
         "in 25 years; first Test won by 30 runs; Harmer 17 wickets; article dated 27 Nov 2025", "ssd_ind_sa_sky"),
    fact("Harmer named player of the series with 17 wickets; Marco Jansen player of the match at Guwahati",
         "ssd_ind_sa_dh")],
   why="Statement 3 is wrong: Simon Harmer was Player of the Series; Jansen was Player of the Match in Guwahati.",
   current=ca("2025-11-26"))

GS(T, VR, "Advanced", "the final of the ICC Under-19 Men's World Cup 2026",
   ["It was played at Harare Sports Club, and India beat England by 100 runs.",
    "The win gave India a record-extending sixth Under-19 World Cup title.",
    "Vaibhav Sooryavanshi scored 175 off 80 balls with a record 15 sixes."],
   (True, True, True),
   "ICC U19 Men's World Cup 2026",
   "On 6 February 2026 at Harare Sports Club, India (captain Ayush Mhatre) made 411 and bowled England out for 311 to "
   "win by 100 runs and lift a record sixth U19 World Cup. Vaibhav Sooryavanshi struck 175 off 80 balls with a record "
   "15 sixes.",
   [fact("Final on 6 February 2026 at Harare Sports Club; India 411, England 311; India won by 100 runs for a record "
         "sixth title; Sooryavanshi 175 off 80 balls with a record 15 sixes; captains Ayush Mhatre and Thomas Rew",
         "ssd_u19_outlook")],
   why="All three statements match the source.",
   current=ca("2026-02-06"))

GS(T, VR, "Advanced", "the World Boxing Cup Finals 2025, which ended on 20 November 2025",
   ["The event was held in Bhubaneswar.",
    "Host India topped the medal table with nine gold medals.",
    "Uzbekistan finished second with four gold medals."],
   (False, True, True),
   "World Boxing Cup Finals 2025",
   "The World Boxing Cup Finals were held in Greater Noida and ended on 20 November 2025. India topped the medal table "
   "with nine golds: seven by women (including Nikhat Zareen at 51 kg and Jaismine at 57 kg) and two by men (Sachin "
   "at 60 kg and Hitesh at 70 kg). Uzbekistan was next best with four golds from nine finals.",
   [fact("World Boxing Cup Finals Greater Noida 2025 ended 20 November 2025; India topped the medal table with nine "
         "golds (seven women, two men); Uzbekistan four golds from nine finals", "ssd_box_wb")],
   why="Statement 1 is wrong: the event was held in Greater Noida, not Bhubaneswar.",
   current=ca("2025-11-20"))

GS(T, TW, "Advanced", "India's performance at the 25th Summer Deaflympics held in Tokyo in November 2025",
   ["India won 20 medals, including 9 gold, its best-ever performance at the Games.",
    "India finished sixth in the medals table.",
    "Wrestling contributed the largest share of India's medals."],
   (True, True, False),
   "Deaflympics 2025",
   "At the 25th Summer Deaflympics in Tokyo, India won 20 medals (9 gold, 7 silver, 4 bronze) and finished sixth, its "
   "best-ever performance. Shooting accounted for 16 of the 20 medals.",
   [fact("25th Summer Deaflympics Tokyo 2025: India 20 medals (9 gold, 7 silver, 4 bronze), sixth in the table, best-ever "
         "performance; 16 medals from shooting; article dated 27 November 2025", "ssd_deaf_trib")],
   why="Statement 3 is wrong: shooting, with 16 medals, was India's biggest contributor.",
   current=ca("2025-11-27", inferred="source article dated 27 Nov 2025 reports the final tally; closing day not stated"))

GS(T, VR, "Advanced", "India at the Asian Para Games 2026 in Aichi-Nagoya, Japan",
   ["India's record haul included 35 gold medals.",
    "India's total of 114 medals was its best-ever tally at the Asian Para Games.",
    "The 2026 edition was the first time the Asian Para Games were held in Japan."],
   (False, True, True),
   "Asian Para Games 2026",
   "The Aichi-Nagoya Asian Para Games, the first held in Japan, ended on 24 October 2026. India won a record 114 medals "
   "(30 gold, 35 silver, 49 bronze), its best-ever tally, beating its previous best at Hangzhou 2023 (reported as "
   "111 by the Paralympic Committee of India; some listings give 108). Double gold medallists Nishad Kumar and Mona "
   "Agarwal were India's flag-bearers at the closing ceremony.",
   [fact("India won 114 medals (30 gold, 35 silver, 49 bronze), surpassing 108 at Hangzhou 2023; Games held in Japan for "
         "the first time; concluded 24 October 2026; flag-bearers Nishad Kumar and Mona Agarwal", "ssd_para_air"),
    fact("India's Hangzhou 2023 Asian Para Games tally was 111 medals (29 gold, 31 silver, 51 bronze), then its best",
         "pci_apg_111")],
   why="Statement 1 is wrong: India won 30 gold; 35 was its silver count.",
   current=ca("2026-10-24"))

GS(T, TW, "Advanced", "India at the ISSF World Cup Final 2025 in Doha",
   ["Suruchi Singh won gold in the women's 10m air pistol.",
    "India topped the medal table.",
    "Simranpreet Kaur Brar won gold in the women's 25m sports pistol."],
   (True, False, True),
   "ISSF World Cup Final 2025",
   "India won six medals (2 gold, 3 silver, 1 bronze) at the ISSF World Cup Final in Doha in December 2025 and finished "
   "second on the medal table, just behind China. The golds came from Suruchi Singh (women's 10m air pistol) and "
   "Simranpreet Kaur Brar (women's 25m sports pistol).",
   [fact("India 6 medals (2 gold, 3 silver, 1 bronze); golds Suruchi Singh (10m air pistol women) and Simranpreet Brar "
         "(25m sports pistol women); second on the medal table behind China; article dated 8 December 2025",
         "ssd_issf_bridge")],
   why="Statement 2 is wrong: India finished second, behind China.",
   current=ca("2025-12-08", inferred="source article dated 8 Dec 2025 sums up India's campaign; final day not stated"))

# ====================================================================== Important Days
T = "Important Days"
DT = "Days and themes"

G(T, DT, "Intermediate",
  "What was the theme of the International Day of Education, observed on 24 January 2026?",
  ["The power of youth in co-creating education", "AI and education: Preserving human agency in a world of automation",
   "Learning for lasting peace", "Education for people, planet and prosperity"], "*",
  "International Day of Education",
  "The UN General Assembly, by resolution 73/25, designated 24 January as the International Day of Education. The "
  "2026 theme was 'The power of youth in co-creating education'.",
  ["24 January: International Day of Education (A/RES/73/25)", "2026 theme: youth co-creating education"],
  [fact("2026 theme 'The power of youth in co-creating education'; 24 January designated by UNGA resolution 73/25",
        "ssd_day_edu")],
  why="The UN page gives 'The power of youth in co-creating education' as the 2026 theme; the other phrases are not "
      "the 2026 theme.",
  current=ca("2026-01-24"))

G(T, DT, "Intermediate",
  "The International Day of Forests, proclaimed by the UN General Assembly in 2012, was observed on 21 March 2026 "
  "under which theme?",
  ["Forests and Economies", "Forests and Food", "Forests and Innovation", "Forests and Health"], "*",
  "International Day of Forests",
  "The International Day of Forests (21 March) was proclaimed by the UN General Assembly in 2012. FAO's page gives "
  "'Forests and Economies' as the theme for 2026.",
  ["21 March: International Day of Forests (proclaimed 2012)", "2026 theme: Forests and Economies"],
  [fact("2026 theme 'Forests and Economies'; Day proclaimed by the UN General Assembly in 2012", "ssd_day_forest")],
  why="FAO's page lists 'Forests and Economies' for 2026; the other options are not the 2026 theme.",
  current=ca("2026-03-21"))

G(T, DT, "Intermediate",
  "World Radio Day is observed on 13 February. The date marks which event?",
  ["The establishment of United Nations Radio in 1946", "The first public radio broadcast in 1906",
   "The founding of the International Telecommunication Union in 1865", "The founding of UNESCO in 1945"], "*",
  "World Radio Day",
  "UNESCO proclaimed World Radio Day in 2011 and the UN General Assembly endorsed it in 2012 (A/RES/67/124). 13 "
  "February was chosen because United Nations Radio was established on that day in 1946. The 2026 observance focused "
  "on radio and artificial intelligence.",
  ["13 Feb = UN Radio established, 1946", "Proclaimed by UNESCO 2011; endorsed by UNGA 2012"],
  [fact("13 February marks the establishment of United Nations Radio in 1946; proclaimed by UNESCO in 2011, endorsed by "
        "UNGA in 2012 (A/RES/67/124); 2026 focus on radio and AI", "ssd_day_radio")],
  why="The UN page links the date to the establishment of United Nations Radio in 1946, not to the other events.",
  current=ca("2026-02-13"))

G(T, DT, "Intermediate",
  "International Youth Day 2026 (12 August), which highlighted young people in Least Developed Countries, Landlocked "
  "Developing Countries and Small Island Developing States, was observed under which theme?",
  ["Different Contexts, Common Aspirations", "Local Youth Actions for the SDGs and Beyond",
   "From Clicks to Progress: Youth Digital Pathways", "Youth Voices for Climate Justice"], "*",
  "International Youth Day",
  "The UN theme for International Youth Day 2026 was 'Different Contexts, Common Aspirations'. It focused on young "
  "people in Least Developed Countries, Landlocked Developing Countries and Small Island Developing States.",
  ["12 August: International Youth Day", "2026 theme: Different Contexts, Common Aspirations"],
  [fact("2026 theme 'Different Contexts, Common Aspirations', highlighting youth in LDCs, LLDCs and SIDS",
        "ssd_day_youth")],
  why="The UN page gives 'Different Contexts, Common Aspirations' as the 2026 theme; the others are not the 2026 theme.",
  current=ca("2026-08-12"))

G(T, DT, "Intermediate",
  "The International Day of the Girl Child, established by UN General Assembly resolution 66/170 of 19 December 2011, "
  "was observed on 11 October 2026 with which theme?",
  ["End child marriage and invest in girls' rights", "The girl I am, the change I lead",
   "Girls' vision for the future", "Digital generation. Our generation."], "*",
  "International Day of the Girl Child",
  "UNGA resolution 66/170, adopted on 19 December 2011, declared 11 October the International Day of the Girl Child. "
  "The 2026 theme, 'End child marriage and invest in girls' rights', was developed through consultations with girls, "
  "girls' organisations, civil society and UN partners.",
  ["11 October (A/RES/66/170, 19 Dec 2011)", "2026 theme: End child marriage and invest in girls' rights"],
  [fact("2026 theme 'end child marriage and invest in girls' rights'; Day declared by UNGA resolution 66/170 of 19 "
        "December 2011", "ssd_day_girl"),
   fact("UNICEF page on International Day of the Girl 2026 with theme on ending child marriage and investing in girls' "
        "rights", "ssd_day_girl_unicef")],
  why="The UN page gives the child-marriage theme for 2026; the other options are not the 2026 theme.",
  current=ca("2026-10-11"))

G(T, DT, "Intermediate",
  "What was the theme of the International Day of Older Persons observed on 1 October 2026?",
  ["The Age of Longevity: Rethinking Systems for Longer Lives",
   "Older Persons Driving Local and Global Action: Our Aspirations, Our Well-Being and Our Rights",
   "Ageing with Dignity", "Resilience of Older Persons in a Changing World"], "*",
  "International Day of Older Persons",
  "UN General Assembly resolution 45/106 of 14 December 1990 designated 1 October as the International Day of Older "
  "Persons. The 2026 theme was 'The Age of Longevity: Rethinking Systems for Longer Lives'.",
  ["1 October (A/RES/45/106, 14 Dec 1990)", "2026 theme: The Age of Longevity"],
  [fact("2026 theme 'The Age of Longevity: Rethinking Systems for Longer Lives'; designated by UNGA resolution 45/106 "
        "on 14 December 1990", "ssd_day_older")],
  why="The UN page gives 'The Age of Longevity: Rethinking Systems for Longer Lives' as the 2026 theme; the other "
      "options are not the 2026 theme.",
  current=ca("2026-10-01"))

# ###################################################################### part: eco (economy + policies)
# ###################################################################### part: eco (Economic Affairs + 1 Government Policies)
U.update({
    "eco_cpi_nov_trib": ("https://www.tribuneindia.com/news/business/indias-retail-inflation-rises-to-0-71-in-november",
                         OPENED),
    "eco_cpi_dec_trib": ("https://www.tribuneindia.com/news/india/retail-inflation-rises-to-1-33-per-cent-in-december-"
                         "govt-data/", OPENED),
    "eco_cpi_feb_na": ("https://newsarenaindia.com/economy/retail-inflation-goes-up-to-3-21-pc-in-feb/72039", OPENED),
    "eco_cpi_mar_rep": ("https://www.republicworld.com/business/india-retail-inflation-cpi-march-rbi-limits", OPENED),
    "eco_wpi_aug_air": ("https://newsonair.gov.in/indias-wpi-based-inflation-rises-to-9-92-in-august/", OPENED),
    "eco_iip_sep_air": ("https://newsonair.gov.in/indias-industrial-output-grows-by-6-7-in-september-2026/", OPENED),
    "eco_iip_sep_dh": ("https://www.deccanherald.com/business/industrial-output-growth-slows-to-4-month-low-of-67-in-"
                       "september-2-4127253", SEARCH),
    "eco_iip_aug_air": ("https://newsonair.gov.in/indias-iip-growth-rises-to-8-in-august-2026/", OPENED),
    "eco_gst_sep_bt": ("https://businesstoday.in/latest/economy/story/september-gst-collections-rise-14-7-to-rs2-04-"
                       "lakh-crore-558985-2026-10-01", OPENED),
    "eco_fx_print": ("https://theprint.in/economy/record-weekly-jump-of-usd-44-9-bn-takes-forex-reserves-to-new-"
                     "lifetime-high-of-usd-785-71-bn/3040382/", OPENED),
    "eco_cad_q3_trib": ("https://www.tribuneindia.com/news/business/indias-current-account-deficit-rises-to-13-2-"
                        "billion-in-q3-rbi", OPENED),
    "eco_cad_q3_bs": ("https://www.business-standard.com/economy/news/india-account-deficit-widens-rs-13-2-billion-in-"
                      "q3fy26-rbi-126030200958_1.html", SEARCH),
    "eco_sp_ob": ("https://www.outlookbusiness.com/news/sp-raises-indias-fy27-gdp-growth-forecast-to-7-sees-25-bps-"
                  "rbi-rate-hike", OPENED),
    "eco_fsr_rbi": ("https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=63050", OPENED),
    "eco_fsr_psu": ("https://psuwatch.com/newsupdates/banks-gnpas-at-a-multidecadal-low-may-inch-up-to-19-pc-by-mar-"
                    "2028-rbi", OPENED),
    "eco_ar_print": ("https://theprint.in/economy/rbis-balance-sheet-size-grows-20-6-pc-to-rs-91-97-lakh-crore-in-"
                     "fy26/2944887/", OPENED),
})

T = "Economic Affairs"
GDP, INF, FIS, MON = ("GDP and growth projections", "Inflation data", "Fiscal data", "Monetary policy decisions")

# ------------------------------------------------------------------ Basic
G(T, INF, "Basic",
  "According to data released by MoSPI on 12 December 2025, what was India's headline retail (CPI) inflation for "
  "November 2025?",
  ["0.71%", "0.25%", "1.33%", "1.40%"], "*",
  "Consumer Price Index inflation",
  "Headline CPI inflation rose to 0.71% in November 2025, 46 basis points above October's record low. Food inflation "
  "was still negative at (-)3.91%. Rural inflation was 0.10% and urban inflation 1.40%.",
  ["November 2025 CPI: 0.71%", "October 2025: about 0.25%", "Released 12 December 2025"],
  [fact("Headline CPI November 2025 0.71%, up 46 bps from October; released 12 December 2025; food -3.91%; rural "
        "0.10%, urban 1.40%", "eco_cpi_nov_trib"),
   fact("December 2025 CPI 1.33%, up from 0.71% in November", "eco_cpi_dec_trib")],
  why="The source gives 0.71% for November; 1.40% was the urban figure only, and 1.33% was December's print.",
  current=ca("2025-12-12"))

G(T, INF, "Basic",
  "India's headline retail (CPI) inflation for February 2026, released on 12 March 2026 on the new series with base "
  "year 2024, was:",
  ["3.21%", "2.74%", "3.40%", "3.47%"], "*",
  "Consumer Price Index inflation",
  "CPI inflation rose to 3.21% in February 2026 from 2.74% in January 2026. Food inflation rose to 3.47% from 2.13%. "
  "Rural inflation was 3.37% and urban 3.02%. The data is on the new CPI series with base year 2024.",
  ["February 2026 CPI: 3.21%", "January 2026 (revised): 2.74%"],
  [fact("February 2026 CPI 3.21%, up from 2.74% in January; food 3.47%; rural 3.37%, urban 3.02%; new series base "
        "2024; article dated 12 March 2026", "eco_cpi_feb_na"),
   fact("March 2026 CPI 3.40%, up from 3.21% in February", "eco_cpi_mar_rep")],
  why="2.74% was January's figure, 3.47% the February food inflation and 3.40% the March reading.",
  current=ca("2026-03-12"))

G(T, MON, "Basic",
  "According to RBI data released on 11 September 2026, India's foreign exchange reserves reached a new all-time high "
  "in the week ended 4 September 2026, after a record weekly jump of about USD 44.9 billion. What was the level?",
  ["About USD 785.7 billion", "About USD 740.8 billion", "About USD 728.5 billion", "About USD 709.4 billion"], "*",
  "Foreign exchange reserves",
  "Reserves rose by a record USD 44.903 billion to a lifetime high of USD 785.706 billion in the week ended 4 September "
  "2026; the previous week's level was USD 740.803 billion. Foreign currency assets rose by USD 47.498 billion to USD "
  "648.168 billion, while gold reserves fell. The report linked the recovery to the RBI's concessional forex swap "
  "initiatives announced in June 2026.",
  ["Week ended 4 Sep 2026: USD 785.706 bn", "Weekly rise: USD 44.903 bn (record)"],
  [fact("Forex reserves rose a record USD 44.903 bn to a lifetime high of USD 785.706 bn in week ended 4 September "
        "2026; previous week rise USD 11.475 bn; FCA up USD 47.498 bn to USD 648.168 bn; gold down; concessional forex "
        "swap initiatives announced in June; PTI report of 11 September 2026", "eco_fx_print")],
  why="USD 740.8 billion was the level a week earlier; the other figures are not the 4 September 2026 level.",
  current=ca("2026-09-11"))

G(T, GDP, "Basic",
  "According to the Index of Industrial Production released on 28 September 2026, India's industrial output grew by "
  "how much in August 2026?",
  ["8%", "6.7%", "7.4%", "9%"], "*",
  "Index of Industrial Production",
  "IIP growth was 8% in August 2026. July 2026 growth was revised up to 7.4%. Electricity grew 12.3% and manufacturing "
  "9%, while mining contracted 5.6%.",
  ["August 2026 IIP growth: 8%", "July 2026 revised: 7.4%"],
  [fact("IIP grew 8% in August 2026; July revised to 7.4%; electricity 12.3%, manufacturing 9%, mining -5.6%; released "
        "28 September 2026", "eco_iip_aug_air"),
   fact("IIP grew 6.7% in September 2026", "eco_iip_sep_air")],
  why="7.4% was July's revised growth and 9% the manufacturing growth; 6.7% was the later September print.",
  current=ca("2026-09-28"))

# ------------------------------------------------------------------ Intermediate
G(T, GDP, "Intermediate",
  "In its 'Economic Activity for Asia Pacific' report of 23 September 2026, S&P Global Ratings revised its forecast of "
  "India's GDP growth for 2026-27 (FY27). What was the revision?",
  ["Raised to 7% from 6.6%", "Cut to 6.6% from 7%", "Raised to 7.4% from 7%", "Cut to 6.4% from 6.7%"], "*",
  "Agency forecasts of India's growth",
  "S&P Global Ratings raised its FY27 growth forecast for India to 7% from 6.6%. It projected consumer inflation "
  "averaging 5.1% in FY27 and said it expected the RBI to raise its policy rate by 25 basis points during FY27.",
  ["S&P (23 Sep 2026): FY27 growth 7% (from 6.6%)", "FY27 CPI forecast: 5.1%"],
  [fact("S&P Global Ratings, 23 September 2026, Economic Activity for Asia Pacific report: FY27 growth forecast raised to "
        "7% from 6.6%; CPI 5.1%; expects 25 bps RBI hike in FY27", "eco_sp_ob")],
  why="The source reports an upgrade from 6.6% to 7%; the other revisions do not match it.",
  current=ca("2026-09-23"))

G(T, MON, "Intermediate",
  "According to the RBI's Financial Stability Report released on 30 June 2026, the gross non-performing assets (GNPA) "
  "ratio of scheduled commercial banks fell to a multi-decadal low at end-March 2026. What was it?",
  ["1.8%", "2.3%", "2.8%", "1.2%"], "*",
  "Financial Stability Report",
  "The June 2026 FSR, reflecting the assessment of the FSDC Sub-Committee, put the GNPA ratio of scheduled commercial "
  "banks at a multi-decadal low of 1.8% at end-March 2026. Under the baseline stress scenario it could inch up to 1.9% "
  "by March 2028. The annual slippage ratio eased to 1.2% in 2025-26.",
  ["FSR June 2026 (30 Jun 2026)", "SCB GNPA end-March 2026: 1.8%", "Baseline March 2028: 1.9%"],
  [fact("RBI released the Financial Stability Report, June 2026 on 30 June 2026; SCBs safe and sound", "eco_fsr_rbi"),
   fact("GNPA of SCBs at multi-decadal low of 1.8% in March 2026; may rise to 1.9% by March 2028 in baseline; slippage "
        "ratio 1.2% in 2025-26", "eco_fsr_psu")],
  why="The FSR figure is 1.8%; 1.2% was the slippage ratio, and the other values are not the end-March 2026 GNPA.",
  current=ca("2026-06-30"))

# ------------------------------------------------------------------ Advanced
GS(T, INF, "Advanced", "India's retail (CPI) inflation for December 2025, released on 12 January 2026",
   ["Headline inflation rose to 1.33%, a three-month high.",
    "Urban inflation was lower than rural inflation.",
    "Food inflation stayed negative for the seventh consecutive month."],
   [True, False, True],
   "Consumer Price Index inflation",
   "Headline CPI inflation rose to a three-month high of 1.33% in December 2025 from 0.71% in November. Urban inflation "
   "(2.03%) was higher than rural inflation (0.76%). Food inflation was (-)2.71%, negative for the seventh straight "
   "month. Inflation stayed below the RBI's lower tolerance level of 2% for the fourth month in a row.",
   [fact("December 2025 CPI 1.33%, three-month high; food -2.71%, negative for seven straight months; urban 2.03%, rural "
         "0.76%; below lower tolerance for the fourth consecutive month; article of 12 January 2026", "eco_cpi_dec_trib")],
   why="Statement 2 is wrong: urban inflation (2.03%) was above rural inflation (0.76%).",
   current=ca("2026-01-12"))

GS(T, INF, "Advanced", "India's retail (CPI) inflation for March 2026, released on 13 April 2026",
   ["Headline inflation rose to 3.40% from 3.21% in February 2026.",
    "Rural inflation was higher than urban inflation.",
    "Food inflation was lower than headline inflation."],
   [True, True, False],
   "Consumer Price Index inflation",
   "Headline CPI inflation rose to 3.40% in March 2026 from 3.21% in February. Rural inflation (3.63%) was above urban "
   "inflation (3.11%). Food inflation (CFPI) rose to 3.87%, above the headline rate.",
   [fact("March 2026 CPI 3.40% from 3.21% in February; CFPI 3.87%; rural 3.63%, urban 3.11%; released 13 April 2026",
         "eco_cpi_mar_rep")],
   why="Statement 3 is wrong: food inflation (3.87%) was higher than headline inflation (3.40%).",
   current=ca("2026-04-13"))

GS(T, INF, "Advanced", "India's wholesale price (WPI) inflation for August 2026, released on 14 September 2026",
   ["WPI inflation rose to 9.92% from 9.78% in July 2026.",
    "Inflation in the fuel and power group was above 20%.",
    "Inflation in the WPI food index rose to 7.05% from 6.65% in July 2026."],
   [True, True, True],
   "Wholesale Price Index inflation",
   "WPI inflation rose marginally to 9.92% in August 2026 from 9.78% in July. Fuel and power inflation rose to about "
   "22.9% from 20%, manufactured products to about 8.4%, while primary articles eased to about 7.8% from 8.5%. The WPI "
   "food index inflation rose to 7.05% from 6.65%.",
   [fact("WPI inflation 9.92% in August 2026 from 9.78% in July; fuel and power 22.9% from 20%; primary articles about "
         "7.8% from 8.5%; manufactured about 8.4%; WPI food index 7.05% from 6.65%; 14 September 2026",
         "eco_wpi_aug_air")],
   why="All three statements match the reported August 2026 data.",
   current=ca("2026-09-14"))

GS(T, GDP, "Advanced", "India's Index of Industrial Production (IIP) for September 2026, released on 28 October 2026",
   ["Electricity and gas supply grew more slowly than manufacturing.",
    "Mining and quarrying output contracted by 6.2%.",
    "Overall growth of 6.7% was slower than the revised 7.8% growth of August 2026."],
   [False, True, True],
   "Index of Industrial Production",
   "Industrial output grew 6.7% in September 2026, a four-month low, down from a downward-revised 7.8% in August. "
   "Manufacturing grew 7.6% and electricity and gas supply 11.2%, while mining contracted 6.2%.",
   [fact("IIP September 2026 6.7%; August revised to 7.8%; manufacturing 7.6%, mining -6.2%, electricity and gas 11.2%; "
         "released 28 October 2026", "eco_iip_sep_air"),
    fact("Industrial output growth slowed to a four-month low of 6.7% in September", "eco_iip_sep_dh")],
   why="Statement 1 is wrong: electricity and gas grew 11.2%, faster than manufacturing's 7.6%.",
   current=ca("2026-10-28"))

GS(T, FIS, "Advanced", "India's GST collections for September 2026, released on 1 October 2026",
   ["Gross GST collections were about ₹2.04 lakh crore, up 14.7% year-on-year.",
    "Gross revenue from imports grew faster than gross domestic revenue.",
    "Total GST refunds rose compared with September 2025."],
   [True, True, False],
   "GST collections",
   "Gross GST collections in September 2026 were about ₹2.04 lakh crore, up 14.7% from ₹1.77 lakh crore. Domestic gross "
   "revenue rose 10.1% and import revenue 25.9% to ₹65,525 crore. Refunds fell 3% to ₹27,001 crore, and net GST revenue "
   "rose 18.1% to ₹1.77 lakh crore.",
   [fact("September 2026 gross GST ₹2.04 lakh crore, +14.7%; domestic +10.1%; imports +25.9% to ₹65,525 crore; refunds "
         "₹27,001 crore, down 3%; net ₹1.77 lakh crore, +18.1%; 1 October 2026", "eco_gst_sep_bt")],
   why="Statement 3 is wrong: refunds fell 3% to ₹27,001 crore.",
   current=ca("2026-10-01"))

GS(T, FIS, "Advanced",
   "India's balance of payments for October-December 2025 (Q3 of 2025-26), as per RBI data released on 2 March 2026",
   ["The current account deficit narrowed from the level of October-December 2024.",
    "The current account deficit was USD 13.2 billion, or 1.3% of GDP.",
    "Net services receipts rose to USD 57.5 billion."],
   [False, True, True],
   "Current account deficit",
   "India's CAD widened to USD 13.2 billion (1.3% of GDP) in Q3 of 2025-26 from USD 11.3 billion (1.1% of GDP) a year "
   "earlier, as the merchandise trade deficit rose to USD 93.6 billion. Net services receipts rose to USD 57.5 billion "
   "from USD 51.2 billion and remittances to USD 36.9 billion. Reserves were depleted by USD 24.4 billion on a BoP basis.",
   [fact("CAD Q3 FY26 USD 13.2 bn (1.3% of GDP) vs USD 11.3 bn (1.1%) in Q3 FY25; goods deficit USD 93.6 bn; net "
         "services USD 57.5 bn from 51.2 bn; remittances USD 36.9 bn; reserves depleted USD 24.4 bn", "eco_cad_q3_trib"),
    fact("Current account deficit widens to USD 13.2 billion in Q3 FY26 (RBI, 2 March 2026)", "eco_cad_q3_bs")],
   why="Statement 1 is wrong: the deficit widened from USD 11.3 billion a year earlier.",
   current=ca("2026-03-02"))

GS(T, MON, "Advanced", "the RBI's Annual Report for 2025-26, released on 29 May 2026",
   ["The RBI's balance sheet grew 20.6% to about ₹91.97 lakh crore as on 31 March 2026.",
    "Foreign investments grew faster than domestic investments on the asset side.",
    "The RBI's gold holdings rose to 880.52 tonnes."],
   [True, False, True],
   "RBI balance sheet",
   "The RBI's balance sheet grew by ₹15.72 lakh crore, or 20.6%, to ₹91.97 lakh crore as on 31 March 2026. Domestic "
   "investments rose 44.9%, gold 63.8% and foreign investments 7.9%. Gold holdings rose to 880.52 tonnes from 879.58 "
   "tonnes, and income rose 26.4%.",
   [fact("Balance sheet ₹91,97,121.08 crore on 31 March 2026, up 20.6% from ₹76,25,421.93 crore; domestic investments "
         "+44.9%, gold +63.8%, foreign investments +7.9%; gold 880.52 tonnes from 879.58; income +26.4%; report released "
         "29 May 2026", "eco_ar_print")],
   why="Statement 2 is wrong: foreign investments grew 7.9%, much slower than domestic investments (44.9%).",
   current=ca("2026-05-29"))

U.update({
    "eco_wpi_jan_dt": ("https://www.dtnext.in/news/business/wholesale-price-inflation-rises-to-181-pc-in-jan", OPENED),
    "eco_wpi_jan_st": ("https://www.thestatesman.com/business/wpi-inflation-rises-to-10-month-high-of-1-81-in-january-on-"
                       "costlier-manufactured-goods-1503557703.html", SEARCH),
    "eco_gst_dec_print": ("https://theprint.in/economy/gst-collections-rise-6-pc-to-over-rs-1-74-lakh-cr-in-december-"
                          "2025/2816534/", OPENED),
    "eco_jcr_air": ("https://newsonair.gov.in/indias-sovereign-credit-rating-upgraded-to-a-with-stable-outlook/", OPENED),
    "eco_fd_dec_bt": ("https://www.businesstoday.in/latest/economy/story/centres-fiscal-deficit-at-545-in-april-december-"
                      "2025-513734-2026-01-30", OPENED),
    "eco_cad_q2_mp": ("https://www.millenniumpost.in/business/indias-cad-narrows-to-13-of-gdp-in-sept-quarter-says-"
                      "reserve-bank-637908", OPENED),
    "eco_swap_bt": ("https://businesstoday.in/latest/economy/story/fcnrb-deposits-contribute-over-90-of-40-82-bn-raised-"
                    "under-rbis-forex-swap-scheme-546658-2026-08-01", OPENED),
    "eco_swap_ent": ("https://india.entrepreneur.com/business-news/rbis-concessional-forex-swap-window-draws-usd-143-5-bn",
                     OPENED),
    "eco_pms_om": ("https://www.outlookmoney.com/invest/what-are-sebis-new-portfolio-managers-regulations-2026-and-"
                   "advertising-rules-key-changes-explained", OPENED),
    "eco_pms_sebi": ("https://www.sebi.gov.in/sebi_data/attachdocs/sep-2026/1790259036651.pdf", SEARCH),
})

# ------------------------------------------------------------------ more Basic
G(T, INF, "Basic",
  "India's wholesale price (WPI) inflation rose to a ten-month high in January 2026, from 0.83% in December 2025. What "
  "was it?",
  ["1.81%", "2.86%", "1.55%", "2.75%"], "*",
  "Wholesale Price Index inflation",
  "WPI inflation rose to 1.81% in January 2026 from 0.83% in December 2025. Manufactured products inflation rose to "
  "2.86% from 1.82%, food articles turned positive at 1.55%, and fuel and power stayed in deflation at (-)4.01%.",
  ["January 2026 WPI: 1.81%", "December 2025: 0.83%"],
  [fact("WPI inflation 1.81% in January 2026 vs 0.83% in December; manufactured 2.86%; fuel and power -4.01%; food "
        "articles 1.55%; 16 February 2026", "eco_wpi_jan_dt"),
   fact("WPI inflation rises to 10-month high of 1.81% in January", "eco_wpi_jan_st")],
  why="2.86% was manufactured products inflation and 1.55% food articles inflation; 2.75% is not the January WPI.",
  current=ca("2026-02-16"))

G(T, FIS, "Basic",
  "According to data released on 1 January 2026, India's gross GST collections for December 2025 grew 6.1% "
  "year-on-year to about how much?",
  ["Over ₹1.74 lakh crore", "Over ₹1.64 lakh crore", "About ₹2.04 lakh crore", "Over ₹1.45 lakh crore"], "*",
  "GST collections",
  "Gross GST collections in December 2025 were over ₹1.74 lakh crore, up 6.1% from over ₹1.64 lakh crore in December "
  "2024. Domestic revenue grew only 1.2%, while import revenue rose 19.7% to ₹51,977 crore. Refunds rose 31%, and net "
  "collections were over ₹1.45 lakh crore.",
  ["December 2025 gross GST: over ₹1.74 lakh crore (+6.1%)", "Net: over ₹1.45 lakh crore"],
  [fact("December 2025 gross GST over ₹1.74 lakh crore, +6.1% from over ₹1.64 lakh crore; domestic +1.2%; imports "
        "₹51,977 crore +19.7%; refunds ₹28,980 crore +31%; net over ₹1.45 lakh crore; 1 January 2026",
        "eco_gst_dec_print"),
   fact("September 2026 gross GST ₹2.04 lakh crore", "eco_gst_sep_bt")],
  why="₹1.64 lakh crore was December 2024's figure and ₹1.45 lakh crore the net figure; ₹2.04 lakh crore was "
      "September 2026.",
  current=ca("2026-01-01"))

# ------------------------------------------------------------------ more Intermediate
G(T, GDP, "Intermediate",
  "On 2 September 2026 the Japan Credit Rating Agency (JCR) upgraded India's long-term foreign and local currency "
  "issuer ratings by one notch, with a stable outlook. What is the new rating?",
  ["A-", "BBB+", "BBB", "A"], "*",
  "Sovereign credit ratings",
  "JCR raised India's rating from BBB+ to A-, with a stable outlook, and raised the country ceiling by a notch to A. It "
  "cited high growth led by private consumption and public investment, digital public infrastructure, GST, and better "
  "fiscal quality, with the central fiscal deficit falling from 4.7% in FY25 to 4.4% in FY26.",
  ["JCR: BBB+ -> A- (stable), 2 Sep 2026", "Country ceiling raised to A"],
  [fact("JCR upgraded India's long-term foreign and local currency issuer ratings from BBB+ to A-, stable outlook; "
        "country ceiling raised to A; fiscal deficit 4.7% FY25 to 4.4% FY26; 2 September 2026", "eco_jcr_air")],
  why="BBB+ was the earlier rating and A is the new country ceiling, not the issuer rating.",
  current=ca("2026-09-02"))

G(T, FIS, "Intermediate",
  "According to Controller General of Accounts data released on 30 January 2026, the Centre's fiscal deficit for "
  "April-December 2025 reached what share of the 2025-26 Budget Estimate?",
  ["54.5%", "62.3%", "66.7%", "70%"], "*",
  "Centre's fiscal deficit (CGA data)",
  "The fiscal deficit in April-December 2025 was ₹8.55 lakh crore, or 54.5% of the Budget Estimate. Total expenditure "
  "was ₹33.8 lakh crore (66.7% of BE), and capital expenditure ₹7.87 lakh crore, about 70% of the ₹11.21 lakh crore "
  "target.",
  ["Fiscal deficit Apr-Dec 2025: ₹8.55 lakh crore = 54.5% of BE"],
  [fact("Fiscal deficit April-December 2025 ₹8.55 lakh crore, 54.5% of BE; total expenditure ₹33.8 lakh crore, 66.7% "
        "of BE; capex ₹7.87 lakh crore, about 70% of ₹11.21 lakh crore; CGA data, 30 January 2026", "eco_fd_dec_bt")],
  why="66.7% was the share of total expenditure and 70% the share of capex; 62.3% is not the April-December figure.",
  current=ca("2026-01-30"))

G(T, FIS, "Intermediate",
  "According to RBI data released on 1 December 2025, India's current account deficit for July-September 2025 (Q2 of "
  "2025-26) was:",
  ["USD 12.3 billion (1.3% of GDP)", "USD 20.8 billion (2.2% of GDP)", "USD 2.7 billion (0.3% of GDP)",
   "USD 7.1 billion (0.7% of GDP)"], "*",
  "Current account deficit",
  "The CAD narrowed to USD 12.3 billion (1.3% of GDP) in Q2 of 2025-26 from USD 20.8 billion (2.2% of GDP) a year "
  "earlier. The merchandise trade deficit eased to USD 87.4 billion, net services receipts rose to USD 50.9 billion and "
  "personal transfer receipts to USD 38.2 billion.",
  ["Q2 FY26 CAD: USD 12.3 bn (1.3% of GDP)", "Q2 FY25: USD 20.8 bn (2.2%)"],
  [fact("CAD Q2 FY26 USD 12.3 bn, 1.3% of GDP, vs USD 20.8 bn (2.2%) in Q2 FY25; trade deficit USD 87.4 bn; net "
        "services USD 50.9 bn; remittances USD 38.2 bn; released Monday 1 December 2025", "eco_cad_q2_mp")],
  why="USD 20.8 billion (2.2%) was the year-earlier figure; the other options are not the Q2 2025-26 deficit.",
  current=ca("2025-12-01"))

# ------------------------------------------------------------------ more Advanced
GS(T, MON, "Advanced", "the RBI's concessional forex swap window of 2026",
   ["It was announced on 5 June 2026 and became operational on 8 June 2026.",
    "Banks could swap foreign currency raised through fresh FCNR(B) deposits, Overseas Foreign Currency Borrowings and "
    "External Commercial Borrowings.",
    "The window for fresh FCNR(B) deposits closed on 31 August 2026, earlier than the 30 September 2026 deadline first "
    "set."],
   [True, True, True],
   "RBI forex swap window",
   "The RBI announced the concessional swap window on 5 June 2026 as part of a package to attract foreign currency "
   "inflows; it became operational on 8 June. Banks could swap with the RBI funds raised through fresh FCNR(B) "
   "deposits, OFCBs and ECBs. Fresh FCNR(B) deposits were first allowed until 30 September 2026, but the window closed "
   "on 31 August; the OFCB/ECB facility runs till 31 December 2026. Total inflows reached about USD 143.5 billion by 18 "
   "September 2026.",
   [fact("Window announced 5 June 2026, operational 8 June 2026; covers fresh FCNR(B), OFCBs and ECBs; FCNR(B) deposits "
         "allowed until 30 September 2026; OFCB/ECB until 31 December 2026; USD 40.816 bn by 31 July", "eco_swap_bt"),
    fact("FCNR(B) window for fresh deposits closed 31 August 2026; total inflows about USD 143.5 bn as of 18 September "
         "2026; operationalised 8 June 2026", "eco_swap_ent")],
   why="All three statements match the reported features of the window.",
   current=ca("2026-06-05"))

# ------------------------------------------------------------------ Government Policies
G("Government Policies", "Regulatory reforms", "Intermediate",
  "The SEBI (Portfolio Managers) Regulations, 2026, approved by the SEBI board on 24 September 2026 and effective from "
  "1 April 2027, create a new PRIM route limited to direct mutual fund plans. What is its minimum ticket size?",
  ["₹25 lakh", "₹50 lakh", "₹10 lakh", "₹2 crore"], "*",
  "Portfolio management services regulation",
  "The SEBI board approved the Portfolio Managers Regulations, 2026 at its meeting of 24 September 2026, superseding "
  "the 2020 Regulations. Under the new rules, effective 1 April 2027, the PRIM route has a minimum ticket size of ₹25 "
  "lakh and is limited to direct mutual fund plans; the standard discretionary PMS minimum is ₹50 lakh per client. "
  "PRIM-only registrants need a minimum net worth of ₹2 crore, against ₹5 crore for general portfolio managers.",
  ["Board approval: 24 Sep 2026 (replaces 2020 Regulations)", "PRIM route: ₹25 lakh, direct MF plans",
   "Standard PMS: ₹50 lakh"],
  [fact("SEBI (Portfolio Managers) Regulations, 2026 replace the 2020 Regulations; effective 1 April 2027; PRIM minimum "
        "ticket ₹25 lakh, direct MF plans only; standard PMS ₹50 lakh; PRIM-only net worth ₹2 crore vs ₹5 crore",
        "eco_pms_om"),
   fact("SEBI board meeting of 24 September 2026 approved the Portfolio Managers Regulations, 2026 in supersession of "
        "the 2020 Regulations", "eco_pms_sebi")],
  why="₹50 lakh is the standard PMS minimum and ₹2 crore the PRIM-only net worth requirement; ₹10 lakh is not stated.",
  current=ca("2026-09-24"))

# ###################################################################### part: sch (schemes)
# ###################################################################### part: sch (Government Schemes)
U.update({
    "sch_ftsc_air": ("https://newsonair.gov.in/cabinet-approves-continuation-of-centrally-sponsored-scheme-for-ftscs-"
                     "for-fast-trial-of-rape-pocso-act-cases/", OPENED),
    "sch_vistar_air": ("https://newsonair.gov.in/cabinet-approves-over-rs-4371-crore-vistar-scheme-to-modernise-indias-"
                       "statistical-system/", OPENED),
    "sch_storage_air": ("https://newsonair.gov.in/cabinet-approves-92-gigawatt-hour-energy-storage-scheme-to-strengthen-"
                        "indias-clean-energy-programme/", OPENED),
    "sch_gobar_air": ("https://newsonair.gov.in/cabinet-approves-gobardhan-scheme-marking-defining-moment-in-indias-clean-"
                      "energy-journey/", OPENED),
    "sch_nsap_air": ("https://newsonair.gov.in/cabinet-approves-53428-crore-rupees-for-social-security-net/", OPENED),
    "sch_nsap_ani": ("https://aninews.in/news/national/general-news/cabinet-approves-continuation-of-national-social-"
                     "assistance-programme-for-five-years-from-2026-27-to-2030-3120261014164532/", SEARCH),
    "sch_bhavya_air": ("https://newsonair.gov.in/cabinet-approves-new-era-of-industrial-development-through-bharat-"
                       "audyogik-vikas-yojna/", OPENED),
    "sch_pmkisan24_air": ("https://newsonair.gov.in/pm-modi-to-visit-gujarat-today/", OPENED),
    "sch_vishwas_air": ("https://newsonair.gov.in/epfo-launches-scheme-vishwas-to-amicable-settlement-of-damages-penalty-"
                        "related-disputes/", OPENED),
    "sch_mitra_ar": ("https://apparelresources.com/business-news/manufacturing/around-rs-70000-crore-investment-"
                     "textiles-sector-come-pm-mitra-parks-says-minister/", OPENED),
    "sch_mitra_rs": ("https://rsdebate.nic.in/bitstream/123456789/758613/1/PQ_267_07022025_U639_p444_p444.pdf", SEARCH),
    "sch_pmayg_print": ("https://theprint.in/economy/cabinet-greenlights-extension-of-pm-awaas-yojna-gramin-2-crore-new-"
                        "homes-to-boost-rural-housing-by-2029/2217429", OPENED),
    "sch_pmayg_pmo": ("https://www.pmindia.gov.in/en/news_updates/cabinet-approves-implementation-of-the-pradhan-mantri-"
                      "awaas-yojana-gramin-pmay-g-during-fy-2024-25-to-2028-29/", SEARCH),
    "sch_janman_ol": ("https://www.outlookindia.com/national/pm-janman-scheme-cabinet-approves-rs-24-104-crore-initiative-"
                      "for-tribal-welfare-news-333625", OPENED),
    "sch_nrlm_pib": ("https://static.pib.gov.in/WriteReadData/userfiles/file/DeendayalAntyodayaYojana-"
                     "NationalRuralLivelihoodMissionMGPN.pdf", OPENED),
    "sch_pmksy_pib": ("https://static.pib.gov.in/WriteReadData/specificdocs/documents/2022/jul/doc20227169101.pdf", OPENED),
    "sch_amrut_pib": ("https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/jun/doc2025624576101.pdf",
                      OPENED),
    "sch_samagra_py": ("https://schooledn.py.gov.in/ssarmsa/introduction.html", OPENED),
    "sch_setu_hit": ("https://www.thehitavada.com/Encyc/2025/10/4/pm-to-unveil-youth-focused-initiatives-worth-over-rs-"
                     "62000-crore-today.html", OPENED),
    "sch_kmy_faq": ("https://PMkisan.gov.in/Documents/PM-KMY - FAQs.pdf", SEARCH),
    "sch_kmy_og": ("https://Pmkisan.Gov.In/Documents/PM-KMY - Operational Guidelines.pdf", SEARCH),
    "sch_shakti_nl": ("https://dsw.nagaland.gov.in/wp-content/uploads/2023/07/Mission_Shakti.pdf", OPENED),
})

T = "Government Schemes"
CEN, CHG = "Central schemes", "Scheme launches and changes"

# ------------------------------------------------------------------ Basic (8)
G(T, CHG, "Basic",
  "On 4 November 2026 the Union Cabinet approved continuing the Centrally Sponsored Scheme for Fast Track Special "
  "Courts (FTSCs), including exclusive POCSO Courts, from 1 April 2026 to 31 March 2031. How many such courts does it "
  "provide for?",
  ["850", "1,023", "790", "1,000"], "*",
  "Fast Track Special Courts scheme",
  "The Cabinet extended the FTSC scheme for five years (1 April 2026 to 31 March 2031) with an outlay of over ₹3,788 "
  "crore, funded from the Nirbhaya Fund. It provides for operationalising 850 FTSCs, including exclusive POCSO Courts, "
  "for speedy trial of rape and POCSO Act cases.",
  ["Continuation approved 4 Nov 2026", "850 FTSCs incl. exclusive POCSO Courts"],
  [fact("Continuation of FTSC scheme from 1 April 2026 to 31 March 2031, outlay over ₹3,788 crore from the Nirbhaya "
        "Fund, provision for 850 FTSCs including exclusive POCSO Courts; approved 4 November 2026", "sch_ftsc_air")],
  why="The source gives 850 courts; the other figures are not the number approved.",
  current=ca("2026-11-04"))

G(T, CHG, "Basic",
  "GOBARdhan, approved by the Union Cabinet in August 2026 as the National Circular Bioenergy Scheme for 2026-27 to "
  "2035-36, aims to raise domestic production of which fuel nearly tenfold?",
  ["Compressed Biogas (CBG)", "Green hydrogen", "Second-generation ethanol", "Sustainable aviation fuel"], "*",
  "GOBARdhan - National Circular Bioenergy Scheme",
  "The Cabinet approved GOBARdhan, the National Circular Bioenergy Scheme, with an outlay of ₹23,731 crore for 2026-27 "
  "to 2035-36. It seeks to raise domestic Compressed Biogas (CBG) production nearly tenfold by converting crop residue, "
  "cattle dung, press mud and municipal organic waste into fuel and organic manure, and is expected to create about 1.5 "
  "lakh jobs.",
  ["GOBARdhan = National Circular Bioenergy Scheme", "Goal: nearly tenfold rise in CBG output"],
  [fact("GOBARdhan, the National Circular Bioenergy Scheme, approved with ₹23,731 crore outlay for 2026-27 to 2035-36; "
        "aims to raise domestic CBG production nearly tenfold; about 1.5 lakh jobs; reported 6 August 2026",
        "sch_gobar_air")],
  why="The source names Compressed Biogas as the fuel; the other fuels are not the scheme's target.",
  current=ca("2026-08-06"))

G(T, CHG, "Basic",
  "On 30 October 2026 the Prime Minister released the 24th instalment of PM-KISAN, about ₹19,000 crore to nearly 10 "
  "crore farmers, during a visit to which district of Gujarat?",
  ["Banaskantha", "Mehsana", "Kutch", "Sabarkantha"], "*",
  "PM-KISAN instalments",
  "The Prime Minister released the 24th PM-KISAN instalment of about ₹19,000 crore to nearly 10 crore farmers in "
  "Banaskantha district, Gujarat, on 30 October 2026, where he also visited Bhildi. He also launched projects worth "
  "over ₹14,000 crore, including Ahmedabad Metro extensions.",
  ["24th instalment: 30 Oct 2026", "Place: Banaskantha district, Gujarat"],
  [fact("24th PM-KISAN instalment of ₹19,000 crore to nearly 10 crore farmers released by the PM in Banaskantha "
        "district, Gujarat (Bhildi visit), on 30 October 2026", "sch_pmkisan24_air")],
  why="The source places the event in Banaskantha district; the other districts are not named.",
  current=ca("2026-10-30"))

G(T, CEN, "Basic",
  "AMRUT 2.0, which extends the Atal Mission for Rejuvenation and Urban Transformation to all urban local bodies with "
  "the aim of making cities 'water secure', was launched on which date?",
  ["1 October 2021", "25 June 2015", "2 October 2019", "15 August 2022"], "*",
  "AMRUT and AMRUT 2.0",
  "The original AMRUT was launched on 25 June 2015 for 500 selected cities. AMRUT 2.0 was launched on 1 October 2021; "
  "it covers all urban local bodies and aims to make cities water secure and self-reliant, with universal sewerage and "
  "septage coverage in the original AMRUT cities.",
  ["AMRUT: 25 June 2015", "AMRUT 2.0: 1 October 2021"],
  [fact("AMRUT launched on 25 June 2015 covering 500 cities; AMRUT 2.0 launched on 1 October 2021, covers all ULBs and "
        "aims to make cities water secure", "sch_amrut_pib")],
  why="25 June 2015 is the launch date of the original AMRUT; the other dates are not given for AMRUT 2.0.")

G(T, CEN, "Basic",
  "Samagra Shiksha, the integrated scheme for school education from pre-school to Class 12, subsumed Sarva Shiksha "
  "Abhiyan, Rashtriya Madhyamik Shiksha Abhiyan and which third scheme?",
  ["Teacher Education", "Mid-Day Meal Scheme", "Rashtriya Uchchatar Shiksha Abhiyan", "Saakshar Bharat"], "*",
  "Samagra Shiksha",
  "Proposed in the Union Budget 2018-19, Samagra Shiksha treats school education as a continuum from pre-school to "
  "Class 12. It subsumed three earlier schemes: Sarva Shiksha Abhiyan (SSA), Rashtriya Madhyamik Shiksha Abhiyan (RMSA) "
  "and Teacher Education (TE).",
  ["Subsumed: SSA, RMSA, Teacher Education"],
  [fact("Samagra Shiksha subsumes SSA, RMSA and Teacher Education; covers pre-school to class 12; proposed in Union "
        "Budget 2018-19", "sch_samagra_py")],
  why="The source lists Teacher Education as the third subsumed scheme; the others are not listed.")

G(T, CEN, "Basic",
  "Under PM-SETU (Pradhan Mantri Skilling and Employability Transformation through Upgraded ITIs), launched in October "
  "2025 with an outlay of ₹60,000 crore, how many government ITIs are to be upgraded?",
  ["1,000", "500", "2,500", "5,000"], "*",
  "PM-SETU",
  "PM-SETU, launched on 4 October 2025 at Vigyan Bhavan, New Delhi, is a centrally sponsored scheme of ₹60,000 crore to "
  "upgrade 1,000 government ITIs in a hub-and-spoke model: 200 hub ITIs linked to 800 spoke ITIs, with co-financing "
  "from the World Bank and the Asian Development Bank.",
  ["1,000 ITIs = 200 hubs + 800 spokes"],
  [fact("PM-SETU: ₹60,000 crore, 1,000 government ITIs upgraded (200 hubs, 800 spokes), World Bank and ADB "
        "co-financing, launched 4 October 2025 at Vigyan Bhavan", "sch_setu_hit")],
  why="The source gives 1,000 ITIs (200 hubs and 800 spokes); the other figures do not match.",
  current=ca("2025-10-04"))

G(T, CEN, "Basic",
  "Pradhan Mantri Kisan Maan-Dhan Yojana (PM-KMY), a pension scheme for small and marginal farmers with up to 2 "
  "hectares of cultivable land, is open to farmers in which entry age group?",
  ["18 to 40 years", "18 to 50 years", "21 to 45 years", "18 to 60 years"], "*",
  "PM Kisan Maan-Dhan Yojana",
  "PM-KMY is a voluntary, contributory pension scheme for small and marginal farmers holding up to 2 hectares of "
  "cultivable land and aged 18 to 40 years at entry. Subscribers receive an assured pension of ₹3,000 a month after "
  "turning 60.",
  ["Entry age 18-40", "Land up to 2 ha", "Pension ₹3,000/month at 60"],
  [fact("PM-KMY eligibility: land up to 2 ha and age between 18 and 40 years; ₹3,000 monthly pension at 60",
        "sch_kmy_og"),
   fact("Small and marginal farmers aged 18-40 with cultivable land up to 2 hectares are eligible", "sch_kmy_faq")],
  why="The scheme documents give 18 to 40 years as the entry age; the other ranges are not its eligibility band.")

G(T, CEN, "Basic",
  "Mission Shakti of the Ministry of Women and Child Development has two sub-schemes. Which of them deals with the "
  "empowerment of women and includes components such as Swadhar Greh, Working Women Hostel and PMMVY?",
  ["Samarthya", "Sambal", "Sakhi", "Saksham"], "*",
  "Mission Shakti",
  "Mission Shakti, an umbrella scheme for the 15th Finance Commission period, has two sub-schemes: 'Sambal' for safety "
  "and security (One Stop Centres, Women Helpline, Beti Bachao Beti Padhao) and 'Samarthya' for empowerment (erstwhile "
  "Ujjwala Homes, Swadhar Greh, Working Women Hostel, National Creche Scheme and PMMVY, plus hubs for empowerment of "
  "women).",
  ["Sambal = safety and security", "Samarthya = empowerment"],
  [fact("Mission Shakti has two sub-schemes: Sambal (safety and security: OSC, WHL, BBBP) and Samarthya (empowerment: "
        "Ujjwala Homes, Swadhar Greh, Working Women Hostel, National Creche Scheme, PMMVY, hubs)", "sch_shakti_nl")],
  why="Sambal is the safety and security sub-scheme; the source names only Sambal and Samarthya as sub-schemes.")

# ------------------------------------------------------------------ Intermediate (2)
G(T, CHG, "Intermediate",
  "The 92 gigawatt-hour (GWh) energy storage scheme approved by the Union Cabinet on 4 November 2026 is split among "
  "battery storage, pumped storage and emerging technologies. How much of it is earmarked for pumped storage?",
  ["60 GWh", "30 GWh", "2 GWh", "46 GWh"], "*",
  "Energy storage scheme 2026",
  "The 92 GWh scheme comprises 30 GWh of battery storage, 60 GWh of pumped storage and 2 GWh for emerging storage "
  "technologies, to be implemented with state governments and distributed across the country.",
  ["92 = 30 (battery) + 60 (pumped) + 2 (emerging)"],
  [fact("92 GWh energy storage scheme approved 4 November 2026: 30 GWh battery storage, 60 GWh pumped storage, 2 GWh "
        "emerging technologies; implemented with states", "sch_storage_air")],
  why="30 GWh is the battery share and 2 GWh the emerging-technology share; 46 GWh is not in the source.",
  current=ca("2026-11-04"))

G(T, CHG, "Intermediate",
  "VISTAR, approved by the Union Cabinet on 4 November 2026 with an outlay of over ₹4,371 crore for 2026-27 to 2030-31, "
  "is meant to modernise what?",
  ["India's official statistical system, under the Ministry of Statistics and Programme Implementation",
   "Agricultural extension services, under the Ministry of Agriculture and Farmers Welfare",
   "Rural broadband networks, under the Department of Telecommunications",
   "Urban bus transport, under the Ministry of Housing and Urban Affairs"], "*",
  "VISTAR scheme",
  "VISTAR (Viksit Bharat Initiative for Statistical Transformation, Analytics & Research) covers all the statistical "
  "and data activities of MoSPI: large-scale surveys, methodological research, digital transformation and national "
  "data governance, aiming at timely, granular, interoperable and AI-ready official statistics.",
  ["VISTAR = statistical transformation", "MoSPI; ₹4,371 crore; 2026-27 to 2030-31"],
  [fact("VISTAR (Viksit Bharat Initiative for Statistical Transformation, Analytics & Research), over ₹4,371 crore, "
        "2026-27 to 2030-31, MoSPI, to modernise the official statistical system; approved 4 November 2026",
        "sch_vistar_air")],
  why="The source describes VISTAR as a MoSPI scheme for the statistical system, not the other sectors.",
  current=ca("2026-11-04"))

# ------------------------------------------------------------------ Advanced (8)
GS(T, CHG, "Advanced", "the decision of 14 October 2026 on the National Social Assistance Programme (NSAP)",
   ["It was continued from 2026-27 to 2030-31 with a total outlay of ₹53,428 crore.",
    "The NSAP was renamed Pradhan Mantri Samajik Sahayata Yojana, and the old age pension component became Pradhan "
    "Mantri Vridhavastha Pension Yojana.",
    "The benchmark disability for the disability pension was raised from 40% to 80%."],
   [True, True, False],
   "National Social Assistance Programme",
   "The Cabinet continued the NSAP for 2026-27 to 2030-31 at ₹53,428 crore and renamed it Pradhan Mantri Samajik "
   "Sahayata Yojana; IGNOAPS became Pradhan Mantri Vridhavastha Pension Yojana, IGNWPS Pradhan Mantri Vidhawa Pension "
   "Yojana, IGNDPS Pradhan Mantri Divyangjan Pension Yojana and NFBS Pradhan Mantri Parivar Labh Yojana. For the "
   "Divyangjan pension the benchmark disability was lowered from 80% to 40%, with ₹375 a month up to age 79 and ₹625 "
   "from age 80. About 3.2 crore people benefit.",
   [fact("NSAP continued 2026-27 to 2030-31, ₹53,428 crore; renamed Pradhan Mantri Samajik Sahayata Yojana; IGNOAPS "
         "renamed Pradhan Mantri Vridhavastha Pension Yojana; disability threshold reduced from 80% to 40%; ₹375/₹625 "
         "per month", "sch_nsap_air"),
    fact("Cabinet approved NSAP continuation on 14 October 2026; benchmark disability criterion to be 40%, down from "
         "80%", "sch_nsap_ani")],
   why="Statement 3 reverses the change: the threshold was lowered from 80% to 40%.",
   current=ca("2026-10-14"))

GS(T, CHG, "Advanced", "the Bharat Audyogik Vikas Yojna (BHAVYA) approved by the Union Cabinet on 18 March 2026",
   ["It provides for 50 plug-and-play industrial parks.",
    "Each park is to be 100 to 1,000 acres in size.",
    "Financial support of up to ₹1 crore per acre is provided."],
   [False, True, True],
   "BHAVYA industrial parks scheme",
   "The Cabinet approved BHAVYA with an outlay of ₹33,660 crore to develop 100 plug-and-play industrial parks of 100 "
   "to 1,000 acres each, with support of up to ₹1 crore per acre, to build world-class industrial infrastructure.",
   [fact("BHAVYA: ₹33,660 crore, 100 plug-and-play industrial parks of 100-1,000 acres, up to ₹1 crore per acre; "
         "approved 18 March 2026", "sch_bhavya_air")],
   why="Statement 1 is wrong: the scheme provides for 100 parks, not 50.",
   current=ca("2026-03-18"))

GS(T, CEN, "Advanced", "the PM MITRA (Mega Integrated Textile Region and Apparel) Parks scheme",
   ["Seven parks have been approved with an outlay of ₹4,445 crore for the period up to 2027-28.",
    "The parks at Warangal (Telangana) and Amravati (Maharashtra) are greenfield sites.",
    "Competitive Incentive Support of up to ₹300 crore per park is available for units in the parks."],
   [True, False, True],
   "PM MITRA Parks",
   "Seven PM MITRA Parks have been approved at Virudhunagar (Tamil Nadu), Warangal (Telangana), Navsari (Gujarat), "
   "Kalaburagi (Karnataka), Dhar (Madhya Pradesh), Lucknow (Uttar Pradesh) and Amravati (Maharashtra), with an outlay "
   "of ₹4,445 crore up to 2027-28. Five are greenfield; the Telangana and Maharashtra parks are brownfield. Units can "
   "get Competitive Incentive Support of up to ₹300 crore per park.",
   [fact("Seven PM MITRA parks, outlay ₹4,445 crore up to 2027-28; sites listed; five greenfield, Telangana and "
         "Maharashtra brownfield; Competitive Incentive Support up to ₹300 crore per park", "sch_mitra_ar"),
    fact("7 PM MITRA Parks approved with scheme outlay of ₹4,445 crore for 2021-22 to 2027-28", "sch_mitra_rs")],
   why="Statement 2 is wrong: the Warangal and Amravati parks are brownfield.",
   current=ca("2024-08-10"))

GS(T, CEN, "Advanced", "the Pradhan Mantri Awaas Yojana-Gramin (PMAY-G) as approved for FY 2024-25 to 2028-29",
   ["It provides for 2 crore additional rural houses.",
    "Unit assistance is ₹1.20 lakh in plain areas and ₹1.30 lakh in the North Eastern and hill States and the UTs of "
    "Jammu & Kashmir and Ladakh.",
    "Of the total outlay of ₹3,06,137 crore, the Central share is ₹2,05,856 crore."],
   [True, True, True],
   "PMAY-Gramin",
   "In August 2024 the Cabinet approved PMAY-G for FY 2024-25 to 2028-29 to build 2 crore more houses, in addition to "
   "completing the earlier cumulative target of 2.95 crore. The total outlay is ₹3,06,137 crore (Centre ₹2,05,856 "
   "crore, States ₹1,00,281 crore). Unit assistance is ₹1.20 lakh in plains and ₹1.30 lakh in NE/hill States and the "
   "UTs of J&K and Ladakh.",
   [fact("PMAY-G FY 2024-25 to 2028-29: 2 crore additional houses; outlay ₹3,06,137 crore (Centre ₹2,05,856 crore, "
         "States ₹1,00,281 crore); ₹1.20 lakh plains, ₹1.30 lakh NE/hill States, J&K and Ladakh", "sch_pmayg_print"),
    fact("Cabinet approved PMAY-G for FY 2024-25 to 2028-29 with unit assistance of ₹1.20 lakh in plains and ₹1.30 lakh "
         "in NE and hill States, J&K and Ladakh", "sch_pmayg_pmo")],
   why="All three statements match the approved scheme.",
   current=ca("2024-08-09"))

GS(T, CEN, "Advanced", "PM-JANMAN (Pradhan Mantri Janjati Adivasi Nyaya Maha Abhiyan)",
   ["Its total outlay is ₹24,104 crore, of which the Central share is ₹15,336 crore.",
    "It covers 75 PVTG communities in 18 States and the UT of Andaman and Nicobar Islands.",
    "It focuses on 11 critical interventions through nine ministries."],
   [True, True, True],
   "PM-JANMAN",
   "The Cabinet approved PM-JANMAN in November 2023 with an outlay of ₹24,104 crore (Centre ₹15,336 crore, States "
   "₹8,768 crore) for 75 Particularly Vulnerable Tribal Group communities in 18 States and the Andaman and Nicobar "
   "Islands, focusing on 11 critical interventions through nine ministries including the Ministry of Tribal Affairs.",
   [fact("PM-JANMAN: ₹24,104 crore (Centre ₹15,336 crore, States ₹8,768 crore); 75 PVTGs in 18 States and A&N "
         "Islands; 11 interventions through nine ministries", "sch_janman_ol")],
   why="All three statements match the approved scheme.",
   current=ca("2023-11-29"))

GS(T, CEN, "Advanced", "the Deendayal Antyodaya Yojana-National Rural Livelihood Mission (DAY-NRLM)",
   ["NRLM was renamed DAY-NRLM with effect from 29 March 2016.",
    "It is a Central Sector scheme funded entirely by the Centre.",
    "It seeks to bring one member, preferably a woman, from each rural poor household into the Self Help Group "
    "network."],
   [True, False, True],
   "DAY-NRLM",
   "The Ministry of Rural Development conceived NRLM in 2010; it was renamed DAY-NRLM with effect from 29 March 2016. "
   "It is a centrally sponsored scheme jointly funded by the Centre and States and implemented through State Rural "
   "Livelihood Missions. One member, preferably a woman, from each rural poor household is brought into the SHG "
   "network.",
   [fact("NRLM renamed DAY-NRLM w.e.f. 29 March 2016; centrally sponsored, jointly funded by Centre and States; one "
         "member (preferably a woman) from each rural poor household brought under SHG network", "sch_nrlm_pib")],
   why="Statement 2 is wrong: it is a centrally sponsored scheme jointly funded by the Centre and the States.")

GS(T, CEN, "Advanced", "the Pradhan Mantri Krishi Sinchayee Yojana (PMKSY)",
   ["The Per Drop More Crop component is still implemented under PMKSY by the Department of Agriculture and Farmers "
    "Welfare.",
    "The Accelerated Irrigation Benefits Programme and Har Khet Ko Pani are implemented by the Department of Water "
    "Resources, River Development and Ganga Rejuvenation.",
    "A Micro Irrigation Fund has been created with NABARD."],
   [False, True, True],
   "PMKSY",
   "PMKSY was launched on 1 July 2015. AIBP and Har Khet Ko Pani are run by the Department of Water Resources, RD&GR, "
   "and Watershed Development by the Department of Land Resources. Per Drop More Crop was run under PMKSY by the "
   "Department of Agriculture and Farmers Welfare during 2015-22 and has since been taken up under RKVY. A Micro "
   "Irrigation Fund has been created with NABARD.",
   [fact("PMKSY launched 1 July 2015; AIBP and HKKP by Department of Water Resources, RD&GR; WD by Department of Land "
         "Resources; PDMC implemented under PMKSY in 2015-22, now under RKVY; Micro Irrigation Fund created with "
         "NABARD", "sch_pmksy_pib")],
   why="Statement 1 is wrong: Per Drop More Crop has moved to the Rashtriya Krishi Vikas Yojana.",
   current=ca("2022-07-01"))

GS(T, CHG, "Advanced", "VISHWAS, 2026, launched by the EPFO in July 2026",
   ["It is meant for amicable settlement of disputes over damages and penalties levied on employers.",
    "It covers defaults made before 14 June 2024, recalculating damages at reduced monthly rates.",
    "It will remain open for 12 months from the date of notification."],
   [True, True, False],
   "EPFO VISHWAS scheme",
   "EPFO's one-time VISHWAS, 2026 scheme allows employers to settle disputes over damages and penalties. For defaults "
   "before 14 June 2024, damages are recalculated at 0.25% a month (up to two months), 0.50% (over two months) and 1% "
   "a month (over four months). It is open for six months from notification; applications are filed on the EPFO "
   "Employer Portal.",
   [fact("EPFO launched VISHWAS, 2026 for amicable settlement of damages and penalty disputes; defaults before 14 June "
         "2024 recalculated at 0.25%/0.50%/1% per month; operational for six months from notification; reported 17 "
         "July 2026", "sch_vishwas_air")],
   why="Statement 3 is wrong: the scheme is open for six months from notification.",
   current=ca("2026-07-17"))

# ###################################################################### part: biz (business)
# ###################################################################### part: biz (business and corporate news)
U.update({
    "biz_tsb_san": ("https://www.santander.co.uk/about-santander/media-centre/press-releases/santander-uk-completes-cash-"
                    "acquisition-of-tsb-banking", OPENED),
    "biz_tsb_sfr": ("https://scottishfinancialreview.com/2026/05/01/santander-completes-tsb-buy-makes-board-changes/",
                    SEARCH),
    "biz_wipro_pr": ("https://www.wipro.com/newsroom/press-releases/2025/wipro-completes-acquisition-of-harmans-digital-"
                     "transformation-solutions-dts-business-unit/", OPENED),
    "biz_wipro_ob": ("https://www.outlookbusiness.com/news/wipro-completes-375-mn-acquisition-of-harmans-digital-"
                     "transformation-solutions-biz-unit", OPENED),
    "biz_hban_p2": ("https://pulse2.com/huntington-closes-cadence-bank-merger-building-279-billion-franchise-and-"
                    "expanding-across-texas-and-the-south/", OPENED),
    "biz_hban_pr": ("https://www.placera.se/pressmeddelanden/huntington-bancshares-huntington-bank-completes-merger-"
                    "with-cadence-bank-expanding-presence-across-texas-and-the-south-20260202", OPENED),
    "biz_airtel_fpj": ("https://www.freepressjournal.in/business/bharti-airtel-increases-airtel-africa-stake-to-79-allots-"
                       "1467-crore-shares-to-icil", OPENED),
    "biz_airtel_sahi": ("https://www.sahi.com/news/bharti-airtel-acquires-16-3-share-in-airtel-africa-boosting-majority-"
                        "stake-to-79-3074-PE1_COR", SEARCH),
    "biz_erste_pr": ("https://www.erstegroup.com/en/news-media/press-releases/2026/01/09/erste-group-completes-acquisition-"
                     "of-controlling-stake-in-santander-bank-polska", OPENED),
    "biz_erste_bf": ("https://businessforum.ro/finance/20260109/erste-group-completes-eur7-billion-santander-bank-polska-"
                     "takeover-2729", SEARCH),
    "biz_itc_print": ("https://theprint.in/economy/itc-completes-100pc-acquisition-in-sproutlife-foods-for-rs-645-crore/"
                      "3056184/", OPENED),
    "biz_itc_fpj": ("https://www.freepressjournal.in/business/itc-completes-sproutlife-foods-acquisition-for-645-crore-"
                    "now-owns-100", SEARCH),
    "biz_wiz_scoop": ("https://www.scoop.co.nz/stories/BU2603/S00191/google-completes-acquisition-of-wiz.htm", OPENED),
    "biz_wiz_jn": ("https://www.jewishnews.co.uk/google-completes-record-32bn-acquisition-of-israeli-cybersecurity-firm-"
                   "wiz/", OPENED),
    "biz_jioaz_bt": ("https://www.businesstoday.in/personal-finance/insurance/story/jio-financial-services-allianz-to-"
                     "form-5050-insurance-jv-target-insurance-for-all-by-2047-526944-2026-04-22", OPENED),
    "biz_hs_hsbc": ("https://www.hsbc.com/investors/hsbc-proposal-to-privatise-hang-seng-bank", OPENED),
    "biz_hs_rns": ("https://www.investegate.co.uk/announcement/rns/hsbc-holdings--hsba/privatisation-of-hang-seng-bank-"
                   "scheme-effective/9386733", OPENED),
    "biz_hs_pr": ("https://www.hsbc.com/news-and-views/news/media-releases/2025/hsbc-proposes-to-privatise-hang-seng-"
                  "bank-by-scheme-of-arrangement", OPENED),
})

T = "Business and Corporate News"
MA, CP = "Mergers and acquisitions", "Corporate partnerships"

# ------------------------------------------------------------------ Intermediate (8)
G(T, MA, "Intermediate",
  "Santander UK completed its all-cash acquisition of TSB on 30 April 2026, after approvals from the PRA and the "
  "European Central Bank. From which banking group did Santander UK buy TSB?",
  ["Banco Sabadell", "BBVA", "Lloyds Banking Group", "CaixaBank"], "*",
  "Bank acquisitions in the UK: Santander UK and TSB",
  "Santander UK completed the acquisition of TSB on 30 April 2026, buying it from Sabadell for £2.65 billion in cash "
  "plus an adjustment of about £213 million for the change in TSB's tangible net asset value. The PRA approved the deal "
  "on 19 March 2026 and the ECB on 14 April 2026. Santander UK says it is now the third-largest UK bank by personal "
  "current account balances and the fourth-largest for mortgages.",
  ["Buyer: Santander UK; seller: Sabadell", "Completed 30 Apr 2026; £2.65 bn cash + NAV adjustment"],
  [fact("Santander UK completed the acquisition of TSB from Sabadell on 30 April 2026; £2.65 billion cash plus about "
        "£213 million NAV adjustment; PRA approval 19 March 2026, ECB 14 April 2026", "biz_tsb_san"),
   fact("Santander completes TSB purchase (report dated 1 May 2026)", "biz_tsb_sfr")],
  why="Santander UK's release names Sabadell as the seller of TSB; the other groups were not party to the deal.",
  current=ca("2026-04-30"))

G(T, MA, "Intermediate",
  "On 2 December 2025 Wipro completed its acquisition of the Digital Transformation Solutions (DTS) business unit of "
  "HARMAN for a cash consideration of up to USD 375 million. HARMAN is a subsidiary of which company?",
  ["Samsung", "LG Electronics", "Sony", "Panasonic"], "*",
  "IT services acquisitions: Wipro and HARMAN DTS",
  "Wipro announced on 2 December 2025 that it had completed the purchase of 100% of HARMAN's DTS business unit, first "
  "announced on 21 August 2025, for up to USD 375 million (about ₹3,270 crore) in cash. HARMAN is described as a "
  "Samsung company. More than 5,600 DTS employees moved to Wipro, and DTS operates as part of Wipro's Engineering "
  "Global Business Line; HARMAN's AI solutions are to be folded into Wipro Intelligence.",
  ["Target: HARMAN DTS (HARMAN = a Samsung company)", "Up to USD 375 mn cash; completed 2 Dec 2025"],
  [fact("Wipro completed the acquisition of HARMAN's DTS business unit; release dated 2 December 2025; DTS to operate "
        "within Wipro's Engineering Global Business Line; AI solutions into Wipro Intelligence", "biz_wipro_pr"),
   fact("Up to USD 375 million (about ₹3,270 crore) cash for 100%; HARMAN described as 'a Samsung company'; over 5,600 "
        "employees; deal first announced 21 August 2025", "biz_wipro_ob")],
  why="The source describes HARMAN as a Samsung company; LG, Sony and Panasonic are not its parent.",
  current=ca("2025-12-02"))

G(T, MA, "Intermediate",
  "Huntington Bancshares announced on 2 February 2026 that it had closed its merger with which US bank, adding 390 "
  "branches and becoming the No. 1 bank in Mississippi by deposit market share?",
  ["Cadence Bank", "Regions Financial", "Trustmark", "Synovus"], "*",
  "US bank mergers: Huntington and Cadence",
  "Huntington announced on 2 February 2026 that it had closed its merger with Cadence Bank, a regional bank "
  "headquartered in Houston (Texas) and Tupelo (Mississippi). Cadence brought 390 branches, taking the network to nearly 1,400 locations in 21 states. As of 31 "
  "December 2025 the combined bank had about USD 279 billion in assets, USD 221 billion in deposits and USD 187 "
  "billion in loans; it is the eighth-largest bank in Texas and No. 1 in Mississippi by deposit market share. Cadence's "
  "chairman and CEO Dan Rollins became non-executive Vice Chairman of Huntington Bancshares.",
  ["Target: Cadence Bank (390 branches)", "Closing announced 2 Feb 2026", "No. 1 in Mississippi, 8th in Texas"],
  [fact("Huntington closed the Cadence Bank merger (report dated 3 February 2026); combined USD 279 billion assets, "
        "USD 221 billion deposits, USD 187 billion loans at 31 Dec 2025; 390 Cadence branches, nearly 1,400 in 21 "
        "states; eighth-largest in Texas, No. 1 in Mississippi by deposits; Dan Rollins non-executive Vice Chairman",
        "biz_hban_p2"),
   fact("Huntington press release (PR Newswire, Columbus, 2 February 2026): merger with Cadence Bank closed; Cadence "
        "headquartered in Houston and Tupelo; USD 279 billion assets; 390 branches; nearly 1,400 locations in 21 "
        "states; eighth-largest in Texas, No. 1 in Mississippi by deposits", "biz_hban_pr")],
  why="The sources name Cadence Bank as the bank Huntington acquired; Regions, Trustmark and Synovus were not.",
  current=ca("2026-02-02"))

G(T, MA, "Intermediate",
  "On 22 June 2026 Bharti Airtel completed the acquisition of about 16.3% of Airtel Africa from Indian Continent "
  "Investment Limited (ICIL) through a share swap. What did Bharti Airtel's effective stake in Airtel Africa rise to?",
  ["About 79%", "About 69%", "About 74%", "About 85%"], "*",
  "Bharti Airtel and Airtel Africa",
  "Bharti Airtel acquired 595,204,251 shares (about 16.3%) of Airtel Africa from ICIL on 22 June 2026, disclosing it "
  "in an exchange filing the next day. Instead of cash, it allotted 146,761,335 of its own equity shares (face value "
  "₹5) to ICIL on a preferential basis, leaving ICIL with about 3.25% of Bharti Airtel. Bharti Airtel's effective "
  "stake in Airtel Africa rose to about 79%.",
  ["16.3% of Airtel Africa from ICIL, 22 Jun 2026", "Paid in Bharti Airtel shares (share swap)",
   "Effective stake now ~79%"],
  [fact("Bharti Airtel completed acquisition of 595,204,251 Airtel Africa shares (about 16.3%) from ICIL on 22 June "
        "2026; allotted 146,761,335 shares of face value ₹5 to ICIL; effective stake about 79%; ICIL about 3.25% of "
        "post-issue capital", "biz_airtel_fpj"),
   fact("Bharti Airtel acquires 16.3% of Airtel Africa, raising majority stake to 79%", "biz_airtel_sahi")],
  why="The filing-based reports give the post-deal effective stake as about 79%; the other figures are not stated.",
  current=ca("2026-06-22"))

G(T, MA, "Intermediate",
  "Which European banking group completed on 9 January 2026 the acquisition of a 49% controlling stake in Santander "
  "Bank Polska from Banco Santander for about €7 billion, calling it the largest cross-border transaction in European "
  "banking in 20 years?",
  ["Erste Group", "UniCredit", "Raiffeisen Bank International", "KBC Group"], "*",
  "Cross-border bank acquisitions in Europe",
  "Erste Group announced on 9 January 2026 that it had completed the acquisition of a 49% controlling stake in "
  "Santander Bank Polska and a 50% stake in its asset manager Santander TFI from Banco Santander, for total cash of "
  "about €7 billion. Erste, founded in 1819 as Austria's first savings bank, described it as the largest cross-border "
  "transaction in the European banking sector in the past 20 years. The bank was to be renamed Erste Bank Polska.",
  ["Buyer: Erste Group (Austria)", "49% of Santander Bank Polska + 50% of Santander TFI; ~€7 bn",
   "Completed 9 Jan 2026"],
  [fact("Erste Group completed acquisition of 49% controlling stake in Santander Bank Polska and 50% of Santander TFI "
        "from Banco Santander for about €7.0 billion; release dated 9 January 2026; 'largest cross-border transaction "
        "in the European banking sector in the past 20 years'; proposed new name Erste Bank Polska", "biz_erste_pr"),
   fact("Erste Group completes €7 billion Santander Bank Polska takeover (9 January 2026)", "biz_erste_bf")],
  why="The release names Erste Group as the buyer; UniCredit, Raiffeisen and KBC were not party to the deal.",
  current=ca("2026-01-09"))

G(T, MA, "Intermediate",
  "On 28 September 2026 ITC made Sproutlife Foods a wholly owned subsidiary by buying the remaining 52.5% stake for "
  "about ₹645 crore in cash. Sproutlife Foods sells its products under which brand?",
  ["Yoga Bar", "Too Yumm", "Epigamia", "The Whole Truth"], "*",
  "FMCG acquisitions: ITC and Sproutlife Foods",
  "ITC bought the remaining 52.5% of Sproutlife Foods Private Ltd through a secondary purchase of 13,445 shares for "
  "about ₹645 crore in cash, raising its holding from about 47.5% to 100% on 28 September 2026. Sproutlife makes "
  "products under the Yoga Bar trademark; its turnover was ₹452 crore in 2025-26. No regulatory approvals were "
  "required.",
  ["Sproutlife Foods = Yoga Bar", "Remaining 52.5% for ~₹645 crore; 100% from 28 Sep 2026"],
  [fact("ITC completed acquisition of the remaining 52.5% of Sproutlife Foods for about ₹645 crore on 28 September "
        "2026, making it wholly owned (from about 47.5%); products under the 'Yoga Bar' trademark; turnover ₹452 crore "
        "in 2025-26; no regulatory approvals required", "biz_itc_print"),
   fact("ITC completes Sproutlife Foods acquisition for ₹645 crore, now owns 100%", "biz_itc_fpj")],
  why="The source states that Sproutlife's products are sold under the Yoga Bar trademark; the other brands are not "
      "Sproutlife's.",
  current=ca("2026-09-28"))

G(T, MA, "Intermediate",
  "Google completed in March 2026 its all-cash acquisition, valued at about USD 32 billion, of which cloud and AI "
  "security company, which joins Google Cloud while keeping its own brand?",
  ["Wiz", "CrowdStrike", "Zscaler", "SentinelOne"], "*",
  "Big-tech acquisitions: Google and Wiz",
  "Google announced in March 2026 that it had completed the acquisition of Wiz, a New York-based cloud and AI "
  "security platform founded in 2020 by Assaf Rappaport, Ami Luttwak, Yinon Costica and Roy Reznik. The USD 32 "
  "billion all-cash deal had been announced in March 2025. Wiz joins Google Cloud but keeps its brand, and its "
  "products remain available on AWS, Microsoft Azure, Oracle Cloud and Google Cloud.",
  ["Target: Wiz (cloud/AI security)", "~USD 32 bn all-cash; completed Mar 2026", "Joins Google Cloud, keeps brand"],
  [fact("Google completes acquisition of Wiz; Wiz (New York) joins Google Cloud, keeps its brand, remains available on "
        "AWS, Azure, Oracle Cloud and Google Cloud; release dated 12 March 2026", "biz_wiz_scoop"),
   fact("Google completes record USD 32 billion all-cash acquisition of Wiz, founded 2020 by Rappaport, Luttwak, "
        "Costica and Reznik; announced March 2025", "biz_wiz_jn")],
  why="The sources name Wiz as the company Google acquired; CrowdStrike, Zscaler and SentinelOne were not acquired.",
  current=ca("2026-03-12", inferred="Google's completion release republished 12 Mar 2026 (NZ time); exact closing "
                                    "day not stated"))

G(T, CP, "Intermediate",
  "On 22 April 2026 Jio Financial Services entered into a binding agreement with the Allianz Group to form a 50:50 "
  "joint venture. Which insurance business is this joint venture meant to cover?",
  ["General and health insurance", "Life insurance", "Pension fund management", "Crop insurance only"], "*",
  "Insurance joint ventures in India",
  "Jio Financial Services (JFSL) signed a binding agreement with the Allianz Group on 22 April 2026 to form a 50:50 "
  "joint venture for general and health insurance, formalising a collaboration first announced in July 2025. The JV "
  "needs regulatory approvals before it starts operations. The two groups said they were working towards a separate "
  "arrangement for life insurance.",
  ["JFSL + Allianz: 50:50", "Binding agreement 22 Apr 2026: general + health insurance",
   "Life insurance: separate arrangement still being worked out"],
  [fact("JFSL entered into a binding agreement with Allianz Group (22 April 2026) for a 50:50 general and health "
        "insurance JV, subject to regulatory approvals; separate arrangement for life insurance being worked on; "
        "collaboration first announced July 2025", "biz_jioaz_bt")],
  why="The source says the binding agreement covers general and health insurance; life insurance is to be handled "
      "under a separate arrangement, and the other businesses are not mentioned.",
  current=ca("2026-04-22"))

# ------------------------------------------------------------------ Advanced (1)
GS(T, MA, "Advanced",
   "HSBC's privatisation of Hang Seng Bank",
   ["The scheme consideration was HK$155 per share, amounting to about HK$106 billion in total.",
    "The scheme became effective on 26 January 2026, and Hang Seng Bank's shares were withdrawn from the Hong Kong "
    "Stock Exchange on 27 January 2026.",
    "HSBC said it would pay the minority shareholders mainly by issuing new HSBC Holdings shares to them."],
   [True, True, False],
   "Bank privatisations: HSBC and Hang Seng Bank",
   "HSBC proposed on 9 October 2025 to take Hang Seng Bank private through a scheme of arrangement at HK$155 per "
   "share, a 33% premium to the 30-day average price, for a total of about HK$106 billion; the offer valued all of "
   "Hang Seng at about HK$290 billion. HSBC said it would fund the consideration from its own financial resources (in "
   "cash), with a day-one CET1 impact of about 125 basis points. The scheme became effective on 26 January 2026, the "
   "shares were withdrawn from the Hong Kong Stock Exchange at 4 pm on 27 January 2026, and Hang Seng is now a wholly "
   "owned subsidiary of HSBC Asia Pacific.",
   [fact("HK$155 per scheme share; 33% premium over 30-day average of HK$116.5; total HK$106 billion; values Hang Seng "
         "at HK$290 billion; funded from HSBC's own financial resources; CET1 impact about 125 bps", "biz_hs_pr"),
    fact("Scheme effective 26 January 2026; shares withdrawn from the Hong Kong Stock Exchange at 4 pm on 27 January "
         "2026; consideration to be paid by electronic transfer or cheque by 4 February 2026", "biz_hs_rns"),
    fact("Privatisation effective 26 January 2026, delisted 27 January 2026; Hang Seng is a wholly owned subsidiary of "
         "HSBC Asia Pacific", "biz_hs_hsbc")],
   why="Statement 3 is wrong: HSBC said it would fund the HK$106 billion cash consideration from its own financial "
       "resources, not by issuing new shares.",
   current=ca("2026-01-26"))


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
        if f"BANK_GA_{first + n:06d}" in INDEPENDENT_CHECK_IDS:
            verified_by.append("ai:independent-check")
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
    assert len(out) == ga["total"] == 150
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
    "notes": "BATCH_007 General Awareness part: 150 original questions. Current-affairs topics (National and "
             "International Current Affairs, Appointments, Awards, Sports, Summits, Economic Affairs, Business) test "
             "events dated 2025-11-01 to 2026-11-04, with event dates from the sources and review_by 2027-05-05. "
             "Other time-sensitive facts also carry current_affairs dates. No fact or event tested in BATCH_000 to "
             "BATCH_006 GA is tested again. Fact checks dated 2026-11-05; verified_by says whether each question's "
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
