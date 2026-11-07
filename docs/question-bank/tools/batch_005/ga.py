"""Writes batches/parts/BATCH_005_GA.json: the 150 General Awareness questions of BATCH_005.

Same structure as tools/batch_004/ga.py. Current-affairs topics (National and International Current Affairs,
Appointments, Awards, Sports, Summits, Economic Affairs, Business) test events dated 2025-11-01 to 2026-11-04 with
event dates from the sources; every such question carries current_affairs {event_date, review_by 2027-05-05}. Other
time-sensitive facts (schemes, policies, books, reports) carry current_affairs too.

Every question has fact_checks. Each URL is marked OPENED (fetched and read on 2026-11-05, giving "web:fact-check")
or SEARCH (confirmed only from search-result text on 2026-11-05, giving "web:search-confirmed"). Sites that refused a
fetch (HTTP 403 or timeouts, e.g. pib.gov.in, thestatesman.com, deccanherald.com, espncricinfo.com, unep.org,
unido.org, oecd.org, unccd.int, pmindia.gov.in) were not worked around; other pages that stated the fact were opened
instead, or the fact rests on search results.

All earlier GA stems (BATCH_000 sample, BATCH_001_GA to BATCH_004_GA) were read first; no fact or event tested
there is tested again here.

Statement questions have their key fixed by the statements (computed from truth values); other questions are written
with the correct option first and answer "*", and are then placed so that keys are balanced A to D.

    python tools/batch_005/ga.py
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
BATCH = "BATCH_005"
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


def ca(event_date):
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



# ###################################################################### part: national
# ---------------------------------------------------------------- National Current Affairs (B9 / I5 / A11)
U.update({
    "n_mguard": ("https://www.newkerala.com/news/a/troops-from-india-uae-focus-tactical-drills-operational-939.htm",
                 OPENED),
    "n_mahen_ao": ("https://www.angelone.in/news/economy/mazagon-dock-share-price-in-focus-as-ins-mahendragiri-built-by-"
                   "it-commissioned-into-indian-navy-on-july-11-2026", OPENED),
    "n_mahen_wiki": ("https://en.wikipedia.org/wiki/INS_Mahendragiri", SEARCH),
    "n_harimau_dr": ("https://www.drishtiias.com/daily-updates/daily-news-analysis/exercise-harimau-shakti-2025/"
                     "print_manually", OPENED),
    "n_harimau_cr": ("https://www.chronicleindia.in/online-magazine/csce-february-2026/harimau-shakti-exercise-2025",
                     OPENED),
    "n_garuda_cr": ("https://www.chronicleindia.in/online-magazine/csce-february-2026/garuda-shakti-2025", OPENED),
    "n_gov_oct": ("https://www.businesstoday.in/india/story/president-murmu-names-new-governors-for-kerala-tamil-nadu-"
                  "odisha-and-3-other-states-561140-2026-10-12", OPENED),
    "n_gov_mar": ("https://www.drishtiias.com/state-pcs-current-affairs/president-approves-governor-reshuffle-across-9-"
                  "states-and-uts/print_manually", OPENED),
    "n_armyday": ("https://newsonair.gov.in/a-grand-parade-to-mark-78th-army-day-held-in-jaipur/", OPENED),
    "n_noida_ians": ("https://ianslive.in/noida-international-airport-set-to-begin-commercial-flight-operations-today--"
                     "20260615065342", OPENED),
    "n_khanjar_fi": ("https://forceindia.net/blog/india-kyrgyzstan-joint-special-forces-exercise-khanjar-commences-in-"
                     "assam", OPENED),
    "n_khanjar_cr": ("https://www.chronicleindia.in/online-magazine/csce-april-2026/exercise-khanjar-2026", OPENED),
    "n_anjadip_tt": ("https://telanganatoday.com/ins-anjadip-commissioned-to-boost-navys-anti-submarine-strength",
                     OPENED),
    "n_anjadip_trib": ("https://www.tribuneindia.com/news/india/dolphin-hunter-ins-anjadip-commissioned-to-enhance-"
                       "navys-anti-submarine-warfare-capabilities/", OPENED),
    "n_konkan_dd": ("https://ddindia.co.in/2026/10/india-uk-maritime-exercise-konkan-26-concludes-off-plymouth/",
                    OPENED),
    "n_nasm_tt": ("https://telanganatoday.com/drdo-successfully-tests-multi-layered-missile-defence-system-and-naval-"
                  "anti-ship-missile", OPENED),
    "n_rudram_air": ("https://newsonair.gov.in/india-successfully-flight-tests-indigenous-rudram-ii-air-to-surface-"
                     "missile/", OPENED),
    "n_gi_tnpsc": ("https://www.tnpscthervupettagam.com/currentaffairs-detail/125-new-geographical-indications-gi-in-"
                   "2025-26?cat=state", OPENED),
    "n_sarnath_fpj": ("https://www.freepressjournal.in/uttar-pradesh/uttar-pradesh-sarnath-added-to-unesco-world-"
                      "heritage-list-becomes-states-fourth-heritage-site", OPENED),
    "n_sarnath_dr": ("https://www.drishtiias.com/state-pcs-current-affairs/sarnath-becomes-indias-45th-unesco-world-"
                     "heritage-site/print_manually", OPENED),
    "n_pinaka_air": ("https://newsonair.gov.in/drdo-successfully-flight-tests-pinaka-long-range-guided-rocket/", OPENED),
    "n_pinaka_na": ("https://newsarenaindia.com/nation/india-successfully-tests-120-km-pinaka-guided-rocket/66070",
                    OPENED),
    "n_bihar_air": ("https://www.newsonair.gov.in/ruling-nda-sweeps-bihar-assembly-elections-with-massive-mandate/",
                    OPENED),
    "n_bihar_bt": ("https://www.businesstoday.in/india/story/bihar-assembly-election-result-2025-live-updates-vote-"
                   "counting-nda-mahagathbandhan-jdu-bjp-rjd-congress-jan-suraaj-party-nitish-kumar-tejashwi-yadav-tej-"
                   "pratap-yadav-prashant-kishor-samrat-chaudhary-502041-2025-11-14", SEARCH),
    "n_assam_air": ("https://www.newsonair.gov.in/assam-assembly-passes-strict-anti-polygamy-bill-2025", OPENED),
    "n_simbex_sg": ("https://www.mindef.gov.sg/news-and-events/latest-releases/26oct26-nr/", OPENED),
    "n_scram_org": ("https://organiser.org/2026/01/10/334344/bharat/india-achieves-major-hypersonic-milestone-with-"
                    "drdos-successful-full-scale-scramjet-engine-test/", OPENED),
    "n_scram_nk": ("https://www.newkerala.com/news/a/drdo-successfully-carries-out-long-duration-test-full-scale-"
                   "scramjet-636.htm", OPENED),
    "n_lamitiye_air": ("https://newsonair.gov.in/11th-edition-of-india-seychelles-joint-military-exercise-lamitiye-2026-"
                       "being-conducted-at-seychelles-defence-academy/", OPENED),
    "n_cyclone_vaj": ("https://vajiramandravi.com/current-affairs/exercise-cyclone-2026/", OPENED),
    "n_dcyclone_gk": ("https://gknow.in/?p=49080", OPENED),
    "n_dac_air": ("https://www.newsonair.gov.in/defence-minister-rajnath-singh-clears-proposals-worth-over-two-lakh-crore-"
                  "to-augment-defence-capabilities", OPENED),
    "n_metro_ians": ("https://ianslive.in/cabinet-okays-rs-12015-crore-project-to-expand-delhi-metro-across-13-new-"
                     "stations--20251224155104", OPENED),
    "n_amaravati_air": ("https://newsonair.gov.in/amaravati-to-now-be-permanent-capital-of-andhra-pradesh-parliament-"
                        "passes-reorganisation-bill-2026/", OPENED),
})

T = "National Current Affairs"
GOV, ST, DEF = "Government decisions", "States and UTs", "Defence"

# ------------------------------------------------------------------ Basic (9)
G(T, DEF, "Basic",
  "Mountain Guardian 2026, the third edition of a joint military exercise held at the Foreign Training Node, "
  "Chaubatia (Uttarakhand), from 5 to 18 October 2026, was conducted between the Indian Army and the land forces of "
  "which country?",
  ["United Arab Emirates", "Oman", "Saudi Arabia", "Qatar"], "*",
  "Exercise Mountain Guardian",
  "Mountain Guardian is an India-UAE army exercise. Its third edition, between the Indian Army and the UAE Land "
  "Forces, ran at the Foreign Training Node, Chaubatia, from 5 to 18 October 2026, with a focus on sub-conventional "
  "operations.",
  ["Exercise: Mountain Guardian, 3rd edition", "Partners: Indian Army and UAE Land Forces",
   "Venue: Chaubatia, Uttarakhand, 5-18 Oct 2026"],
  [fact("Mountain Guardian 2026, third edition, Indian Army and UAE Land Forces, Foreign Training Node Chaubatia, "
        "5-18 October 2026", "n_mguard")],
  why="Oman (Al Najah), Saudi Arabia (Sada Tanseeq) and Qatar (Zair-Al-Bahr, naval) have differently named exercises "
      "with India; Mountain Guardian is with the UAE.",
  current=ca("2026-10-05"))

G(T, DEF, "Basic",
  "INS Mahendragiri, a Project 17A (Nilgiri-class) stealth frigate commissioned at Visakhapatnam on 11 July 2026, was "
  "built by which shipyard?",
  ["Mazagon Dock Shipbuilders Limited", "Garden Reach Shipbuilders and Engineers", "Cochin Shipyard Limited",
   "Goa Shipyard Limited"], "*",
  "Project 17A frigates",
  "INS Mahendragiri was commissioned at Visakhapatnam on 11 July 2026. Mazagon Dock Shipbuilders Limited (MDL), "
  "Mumbai, did its detailed design and construction on a basic design by the Navy's Warship Design Bureau; it has "
  "about 75% indigenous content. Project 17A ships are split between MDL and GRSE, Kolkata.",
  ["Ship: INS Mahendragiri (Project 17A)", "Commissioned: 11 Jul 2026, Visakhapatnam", "Builder: MDL, Mumbai"],
  [fact("INS Mahendragiri commissioned on 11 July 2026 at Visakhapatnam; built by Mazagon Dock Shipbuilders; Nilgiri "
        "class, Project 17A; about 75% indigenous", "n_mahen_ao"),
   fact("INS Mahendragiri commissioned at Visakhapatnam on 11 July 2026", "n_mahen_wiki")],
  why="GRSE built the other Project 17A ships (such as Dunagiri); Cochin Shipyard and Goa Shipyard did not build "
      "Mahendragiri.",
  current=ca("2026-07-11"))

G(T, DEF, "Basic",
  "The fifth edition of Exercise Harimau Shakti, held in Rajasthan from 5 to 18 December 2025, is a joint military "
  "exercise between India and which country?",
  ["Malaysia", "Indonesia", "Thailand", "Vietnam"], "*",
  "Exercise Harimau Shakti",
  "Harimau Shakti is the India-Malaysia army exercise ('harimau' is Malay for tiger). The fifth edition, with the "
  "Dogra Regiment and the 25th Battalion of the Royal Malaysian Army, was held in Rajasthan from 5 to 18 December "
  "2025; the previous edition was in Pahang, Malaysia.",
  ["Harimau Shakti: India-Malaysia", "5th edition: Rajasthan, 5-18 Dec 2025"],
  [fact("Harimau Shakti 2025, 5th edition, India and Malaysia, Rajasthan, 5-18 December 2025; previous edition in "
        "Pahang, Malaysia", "n_harimau_cr"),
   fact("Harimau Shakti 2025: Dogra Regiment and 25th Battalion, Royal Malaysian Army", "n_harimau_dr")],
  why="Indonesia's exercise with India is Garuda Shakti, Thailand's is Maitree and Vietnam's is VINBAX.",
  current=ca("2025-12-05"))

G(T, DEF, "Basic",
  "The 10th edition of Exercise Garuda Shakti, a joint special forces exercise held at Bakloh, Himachal Pradesh, "
  "from 3 to 12 December 2025, was conducted between India and which country?",
  ["Indonesia", "Malaysia", "Singapore", "Philippines"], "*",
  "Exercise Garuda Shakti",
  "Garuda Shakti is the India-Indonesia special forces exercise. Its 10th edition was held at Bakloh in Himachal "
  "Pradesh from 3 to 12 December 2025.",
  ["Garuda Shakti: India-Indonesia (special forces)", "10th edition: Bakloh, HP, 3-12 Dec 2025"],
  [fact("Garuda Shakti 2025, 10th edition, India-Indonesia joint special forces exercise, Bakloh, Himachal Pradesh, "
        "3-12 December 2025", "n_garuda_cr")],
  why="Malaysia's exercise is Harimau Shakti, Singapore's army exercise is Bold Kurukshetra/Agni Warrior; Garuda "
      "Shakti is with Indonesia.",
  current=ca("2025-12-03"))

G(T, GOV, "Basic",
  "Under a Rashtrapati Bhavan communique of 12 October 2026, Om Prakash Mathur, until then Governor of Sikkim, was "
  "appointed Governor of which state?",
  ["Kerala", "Karnataka", "Odisha", "Uttarakhand"], "*",
  "Governors appointed in October 2026",
  "The communique of 12 October 2026 named six Governors: Om Prakash Mathur (Kerala), Rajendra Vishwanath Arlekar "
  "(Tamil Nadu), Braj Mohan Ram (Odisha), Sudha Yadav (Karnataka), Dhal Singh Bisen (Uttarakhand) and Dushyant "
  "Gautam (Sikkim).",
  ["Om Prakash Mathur: Sikkim -> Kerala", "Communique: 12 Oct 2026"],
  [fact("12 Oct 2026 communique: Om Prakash Mathur (earlier Governor of Sikkim) to Kerala; Sudha Yadav Karnataka; Braj "
        "Mohan Ram Odisha; Dhal Singh Bisen Uttarakhand", "n_gov_oct")],
  why="Karnataka went to Sudha Yadav, Odisha to Braj Mohan Ram and Uttarakhand to Dhal Singh Bisen.",
  current=ca("2026-10-12"))

G(T, DEF, "Basic",
  "The parade marking the 78th Army Day on 15 January 2026 was held on Mahal Road, Jagatpura, in which city?",
  ["Jaipur", "Pune", "Lucknow", "Bengaluru"], "*",
  "Army Day 2026",
  "Army Day (15 January) marks the day in 1949 when General K. M. Cariappa took over as the first Indian "
  "Commander-in-Chief. The 78th Army Day parade was held on Mahal Road in Jagatpura, Jaipur, and featured BrahMos, "
  "drones and robotic dogs; the Nepal Army Band also took part.",
  ["78th Army Day: 15 Jan 2026", "Parade venue: Mahal Road, Jagatpura, Jaipur"],
  [fact("78th Army Day parade held on 15 January 2026 on Mahal Road, Jagatpura, Jaipur", "n_armyday")],
  why="The 2026 parade was held in Jaipur; Pune, Lucknow and Bengaluru were not the venue that year.",
  current=ca("2026-01-15"))

G(T, ST, "Basic",
  "Noida International Airport, which began commercial flight operations on 15 June 2026 with an IndiGo flight from "
  "Lucknow, is located in which district of Uttar Pradesh?",
  ["Gautam Buddh Nagar", "Ghaziabad", "Bulandshahr", "Aligarh"], "*",
  "Noida International Airport (Jewar)",
  "The airport at Jewar lies in Gautam Buddh Nagar district, in the Yamuna Expressway Industrial Development Authority "
  "area. Commercial operations began on 15 June 2026 with IndiGo's inaugural flight from Lucknow; the Prime Minister "
  "had inaugurated it earlier in 2026.",
  ["Airport: Noida International Airport, Jewar", "District: Gautam Buddh Nagar (YEIDA area)",
   "Commercial flights from 15 Jun 2026"],
  [fact("Noida International Airport begins commercial operations on Monday 15 June 2026 with IndiGo flight from "
        "Lucknow; located in Gautam Buddh Nagar district in the YEIDA area", "n_noida_ians")],
  why="Jewar is in Gautam Buddh Nagar, not in Ghaziabad (which has Hindon airport), Bulandshahr or Aligarh.",
  current=ca("2026-06-15"))

G(T, DEF, "Basic",
  "The 13th edition of Exercise Khanjar, a joint special forces exercise held at Missamari, Assam, from 4 to 17 "
  "February 2026, is conducted between India and which country?",
  ["Kyrgyzstan", "Kazakhstan", "Uzbekistan", "Tajikistan"], "*",
  "Exercise Khanjar",
  "Khanjar is the annual India-Kyrgyzstan special forces exercise, held alternately in the two countries. The 13th "
  "edition (4-17 February 2026) at Missamari, Sonitpur district, Assam, involved Parachute Regiment (Special Forces) "
  "troops and Kyrgyzstan's ILBRIS Special Forces Brigade; the previous edition was in Kyrgyzstan in March 2025.",
  ["Khanjar: India-Kyrgyzstan (special forces)", "13th edition: Missamari, Assam, 4-17 Feb 2026"],
  [fact("13th India-Kyrgyzstan Exercise Khanjar, 4-17 February 2026, Missamari, Assam; Parachute Regiment (SF) and "
        "ILBRIS brigade", "n_khanjar_fi"),
   fact("Exercise Khanjar 2026: 13th edition, 4-17 Feb 2026, Missamari, Sonitpur, Assam", "n_khanjar_cr")],
  why="Kazakhstan's exercise with India is Prabal Dostyk, Uzbekistan's is Dustlik; Khanjar is with Kyrgyzstan.",
  current=ca("2026-02-04"))

G(T, GOV, "Basic",
  "In the reshuffle of Governors and Lieutenant Governors announced in March 2026, former diplomat Taranjit Singh "
  "Sandhu was appointed Lieutenant Governor of which Union Territory?",
  ["Delhi", "Ladakh", "Puducherry", "Jammu and Kashmir"], "*",
  "Lieutenant Governor of Delhi",
  "In the March 2026 reshuffle, Taranjit Singh Sandhu, a former diplomat, became Lieutenant Governor of Delhi, "
  "replacing Vinai Kumar Saxena, who moved to Ladakh as Lieutenant Governor.",
  ["Taranjit Singh Sandhu: LG, Delhi", "V. K. Saxena: Delhi -> Ladakh"],
  [fact("March 2026 reshuffle: Taranjit Singh Sandhu (former diplomat) LG Delhi; Vinai Kumar Saxena from Delhi to LG "
        "Ladakh", "n_gov_mar")],
  why="Ladakh went to V. K. Saxena; Puducherry and Jammu and Kashmir were not part of Sandhu's appointment.",
  current=ca("2026-03-06"))

# ------------------------------------------------------------------ Intermediate (5)
G(T, DEF, "Intermediate",
  "INS Anjadip, the third of eight Anti-Submarine Warfare Shallow Water Craft built by GRSE, was commissioned at "
  "Chennai on 27 February 2026. It is named after an island off the coast of which state?",
  ["Karnataka", "Goa", "Kerala", "Maharashtra"], "*",
  "INS Anjadip",
  "INS Anjadip, built by Garden Reach Shipbuilders and Engineers, Kolkata, was commissioned by Admiral Dinesh K. "
  "Tripathi at Chennai Port on 27 February 2026. It is named after Anjadip island off Karwar in Karnataka, which "
  "played a role in the 1961 liberation of Goa.",
  ["Ship: INS Anjadip (ASW SWC, GRSE)", "Commissioned: 27 Feb 2026, Chennai", "Named after: island off Karwar, Karnataka"],
  [fact("INS Anjadip commissioned 27 Feb 2026 at Chennai Port; built by GRSE; third of eight ASW SWC; named after an "
        "island off Karwar, Karnataka", "n_anjadip_trib"),
   fact("INS Anjadip named after island off Karwar, Karnataka; role in 1961 liberation of Goa", "n_anjadip_tt")],
  why="Anjadip island lies off Karwar in Karnataka; its link to Goa is historical (1961), not territorial.",
  current=ca("2026-02-27"))

G(T, DEF, "Intermediate",
  "KONKAN-26, held off Plymouth from 8 to 15 October 2026 with INS Trishul taking part, is a maritime exercise "
  "between the Indian Navy and the navy of which country?",
  ["United Kingdom", "France", "United States", "Portugal"], "*",
  "Exercise KONKAN",
  "KONKAN is the India-UK naval exercise. KONKAN-26 (8-15 October 2026, sea phase 12-15 October) off Plymouth paired "
  "the stealth frigate INS Trishul with HMS Sutherland, under the Royal Navy's Fleet Operational Standards and "
  "Training organisation.",
  ["KONKAN: India-UK", "KONKAN-26: off Plymouth, 8-15 Oct 2026", "Ships: INS Trishul, HMS Sutherland"],
  [fact("KONKAN-26 India-UK, 8-15 October 2026 off Plymouth; INS Trishul and HMS Sutherland", "n_konkan_dd")],
  why="India's naval exercise with France is Varuna and with the US is Malabar/others; Lisbon was only a later port "
      "call for INS Trishul.",
  current=ca("2026-10-08"))

G(T, DEF, "Intermediate",
  "During three consecutive flight tests on 10 and 11 June 2026, DRDO validated a multi-layered ballistic missile "
  "defence system and carried out the maiden flight test of which missile?",
  ["Naval Anti-Ship Missile-Medium Range (NASM-MR)", "BrahMos-NG", "Astra Mk-3", "Nirbhay"], "*",
  "DRDO tests, June 2026",
  "On 10-11 June 2026 DRDO conducted three consecutive flight tests: interceptors of the multi-layered BMD system "
  "engaged their targets, and the Naval Anti-Ship Missile-Medium Range (NASM-MR) flew for the first time.",
  ["Dates: 10-11 Jun 2026", "BMD interceptors engaged targets", "Maiden flight: NASM-MR"],
  [fact("DRDO three consecutive flight tests on 10-11 June 2026: multi-layered BMD and maiden flight test of NASM-MR",
        "n_nasm_tt")],
  why="BrahMos-NG, Astra Mk-3 and Nirbhay were not the missiles whose maiden flight was reported on these dates.",
  current=ca("2026-06-10"))

G(T, DEF, "Intermediate",
  "RudraM-II, which DRDO and the Indian Air Force flight-tested under extreme release conditions in June 2026, is "
  "which type of missile?",
  ["Air-to-surface missile", "Surface-to-air missile", "Submarine-launched ballistic missile",
   "Anti-tank guided missile"], "*",
  "RudraM-II",
  "RudraM-II is an indigenous air-to-surface missile. In tests reported on 2 June 2026, it was released from an "
  "airborne platform under extreme release conditions and guided to its target; range instruments of ITR Chandipur "
  "tracked the flights.",
  ["RudraM-II: air-to-surface", "Tests by DRDO and IAF (reported 2 Jun 2026)"],
  [fact("DRDO and IAF flight-test indigenous RudraM-II air-to-surface missile from an airborne platform under extreme "
        "release conditions; reported 2 June 2026", "n_rudram_air")],
  why="It is launched from aircraft at ground targets, so it is not surface-to-air, submarine-launched or anti-tank.",
  current=ca("2026-06-02"))

G(T, ST, "Intermediate",
  "Of the 125 new Geographical Indication (GI) registrations granted in India in 2025-26, which state received the "
  "largest number?",
  ["Madhya Pradesh", "West Bengal", "Himachal Pradesh", "Uttar Pradesh"], "*",
  "GI registrations 2025-26",
  "Of 125 new GIs registered from April 2025 to March 2026, Madhya Pradesh got 26, West Bengal 24 and Himachal Pradesh "
  "13. Uttar Pradesh still has the most GIs overall (79), but got only 5 new ones in the year. India's cumulative "
  "total is 822.",
  ["2025-26: 125 new GIs", "MP 26, WB 24, HP 13", "UP leads cumulative (79), not the year"],
  [fact("125 new GIs in 2025-26; Madhya Pradesh 26, West Bengal 24, Himachal Pradesh 13; UP 5; UP leads cumulative with "
        "79; total 822", "n_gi_tnpsc")],
  why="West Bengal (24) and Himachal Pradesh (13) were second and third; Uttar Pradesh leads only the cumulative "
      "count.",
  current=ca("2026-07-09"))

# ------------------------------------------------------------------ Advanced (11)
GS(T, GOV, "Advanced", "the reshuffle of Governors and Lieutenant Governors announced in March 2026",
   ["Kavinder Gupta, earlier Governor of Himachal Pradesh, was appointed Lieutenant Governor of Ladakh.",
    "R. N. Ravi, earlier Governor of Tamil Nadu, was appointed Governor of West Bengal.",
    "Retired Lt Gen Syed Ata Hasnain was appointed Governor of Bihar."],
   [False, True, True],
   "Governor reshuffle, March 2026",
   "In the reshuffle announced on 6 March 2026, R. N. Ravi moved from Tamil Nadu to West Bengal after C. V. Ananda "
   "Bose's resignation was accepted, and retired Lt Gen Syed Ata Hasnain became Governor of Bihar. Kavinder Gupta moved "
   "the other way: from Lieutenant Governor of Ladakh to Governor of Himachal Pradesh, while V. K. Saxena went to "
   "Ladakh.",
   [fact("March 2026: R. N. Ravi Tamil Nadu -> West Bengal; Syed Ata Hasnain Governor of Bihar; Kavinder Gupta from LG "
         "Ladakh to Governor of Himachal Pradesh; V. K. Saxena to Ladakh", "n_gov_mar")],
   why="Statement 1 reverses the move: Kavinder Gupta went from Ladakh to Himachal Pradesh.",
   current=ca("2026-03-06"))

GS(T, ST, "Advanced", "the inscription of Sarnath on UNESCO's World Heritage List",
   ["It was inscribed at the 48th session of the World Heritage Committee held in Busan, South Korea.",
    "It became India's 45th World Heritage Site.",
    "It is the first World Heritage Site in Uttar Pradesh."],
   [True, True, False],
   "Sarnath, World Heritage Site",
   "On 25 July 2026, at the 48th session of the World Heritage Committee in Busan, the Ancient Buddhist Site of "
   "Sarnath (the Chaukhandi Stupa and the archaeological remains, including the Dhamek Stupa and the Ashoka Pillar) "
   "was inscribed as India's 45th World Heritage Site. It is Uttar Pradesh's fourth, after the Taj Mahal, Agra Fort and "
   "Fatehpur Sikri. It had been on the Tentative List since 1998.",
   [fact("Sarnath inscribed 25 July 2026 at 48th session in Busan; India's 45th; UP's fourth after Taj Mahal, Agra Fort, "
         "Fatehpur Sikri; tentative list 1998", "n_sarnath_fpj"),
    fact("Sarnath becomes India's 45th UNESCO World Heritage property; 48th session, Busan", "n_sarnath_dr")],
   why="Statement 3 is wrong: Sarnath is Uttar Pradesh's fourth World Heritage Site.",
   current=ca("2026-07-25"))

GS(T, DEF, "Advanced", "the Pinaka Long Range Guided Rocket (LRGR)",
   ["Its maiden flight test on 29 December 2025 was to its maximum range of 120 km.",
    "It was designed by the Defence Research and Development Laboratory (DRDL), Hyderabad.",
    "On 8 July 2026 it was flight-tested to a user-defined minimum range of 60 km at ITR, Chandipur."],
   [True, False, True],
   "Pinaka LRGR",
   "The LRGR-120 first flew on 29 December 2025 at ITR Chandipur, reaching its 120 km maximum range. On 8 July 2026 it "
   "was fired to a minimum range of 60 km from an in-service Pinaka launcher. It was designed by the Armament Research "
   "and Development Establishment (ARDE), Pune, with HEMRL; DRDL and RCI only supported the project.",
   [fact("Maiden flight test of Pinaka LRGR 120 on 29 December 2025, 120 km, ITR Chandipur; designed by ARDE with HEMRL, "
         "supported by DRDL and RCI", "n_pinaka_na"),
    fact("Pinaka LRGR flight-tested on 8 July 2026 to a user-defined minimum range of 60 km at ITR Chandipur; designed "
         "by ARDE", "n_pinaka_air")],
   why="Statement 2 is wrong: ARDE designed the rocket; DRDL only provided support.",
   current=ca("2026-07-08"))

GS(T, ST, "Advanced", "the Bihar Assembly election results of November 2025",
   ["The NDA won 202 of the 243 seats.",
    "The JD(U) emerged as the single largest party.",
    "Polling was held in two phases, on 6 and 11 November 2025."],
   [True, False, True],
   "Bihar election 2025",
   "Results declared on 14 November 2025 gave the NDA 202 of 243 seats. The BJP was the single largest party with 89, "
   "ahead of the JD(U) with 85; LJP(RV) won 19. The RJD-led Mahagathbandhan won 35. Polling was held in two phases, "
   "on 6 and 11 November, with a record turnout of 67.13%.",
   [fact("NDA 202 of 243; BJP 89 largest party; JD(U) 85; LJP(RV) 19; two phases 6 and 11 November; turnout 67.13%",
         "n_bihar_air"),
    fact("Bihar results counted on 14 November 2025", "n_bihar_bt")],
   why="Statement 2 is wrong: the BJP (89) was the largest party, not the JD(U) (85).",
   current=ca("2025-11-14"))

GS(T, ST, "Advanced", "the Assam Prohibition of Polygamy Bill, 2025, passed by the Assam Legislative Assembly on "
   "27 November 2025",
   ["It applies uniformly to Sixth Schedule areas and to the State's tribal communities.",
    "Entering a second marriage while concealing an existing one is punishable with up to 10 years' imprisonment.",
    "Repeat offenders face double the punishment."],
   [False, True, True],
   "Assam anti-polygamy law",
   "The Bill passed on 27 November 2025 punishes a second marriage without dissolving the first with up to 7 years, "
   "and up to 10 years if the earlier marriage is concealed; repeat offenders get double the punishment, and clerics "
   "who solemnise such marriages can be fined. It does not apply to Sixth Schedule areas or to the State's tribal "
   "communities.",
   [fact("Assam Assembly passed Prohibition of Polygamy Bill on 27 Nov 2025: up to 10 years for concealing a marriage, "
         "7 years otherwise, double for repeat offenders; not applicable to Sixth Schedule areas and tribal communities",
         "n_assam_air")],
   why="Statement 1 is wrong: Sixth Schedule areas and tribal communities are excluded.",
   current=ca("2025-11-27"))

GS(T, DEF, "Advanced", "SIMBEX-2026",
   ["It was the 33rd edition of the India-Singapore maritime exercise, first held in 1994.",
    "Its sea phase was held in the South China Sea off Singapore."],
   [True, False],
   "SIMBEX",
   "The 33rd SIMBEX was held from 21 to 26 October 2026. Its sea phase was in the Bay of Bengal off Visakhapatnam, "
   "with RSS Supreme and the Indian ships INS Nilgiri, INS Kamorta and the submarine INS Sindhukirti. SIMBEX began in "
   "1994.",
   [fact("SIMBEX 33rd edition (first held 1994), 21-26 October 2026, sea phase in the Bay of Bengal off Visakhapatnam; "
         "RSS Supreme, INS Nilgiri, INS Kamorta, INS Sindhukirti", "n_simbex_sg")],
   why="Statement 2 is wrong: the 2026 sea phase was off Visakhapatnam in the Bay of Bengal.",
   current=ca("2026-10-21"))

GS(T, DEF, "Advanced", "DRDO's scramjet tests for the hypersonic cruise missile programme",
   ["A long-duration ground test of an actively cooled full-scale scramjet combustor, run for over 12 minutes, was "
    "reported in January 2026.",
    "In the test of 9 May 2026 the combustor ran for over 1,200 seconds.",
    "The tests were carried out by DRDL at its Scramjet Connect Pipe Test facility in Hyderabad."],
   [True, True, True],
   "Scramjet combustor tests",
   "DRDL Hyderabad tested its actively cooled full-scale scramjet combustor at the Scramjet Connect Pipe Test (SCPT) "
   "facility: a run of over 12 minutes (reported 10 January 2026) and a second long-duration run of over 1,200 "
   "seconds on 9 May 2026. The work supports India's hypersonic cruise missile programme.",
   [fact("Actively cooled full-scale scramjet combustor test of over 12 minutes at SCPT facility, DRDL Hyderabad; "
         "reported 10 January 2026", "n_scram_org"),
    fact("9 May 2026 test of over 1,200 seconds at the SCPT facility, Hyderabad, by DRDL", "n_scram_nk")],
   why="All three statements are correct.",
   current=ca("2026-05-09"))

GS(T, DEF, "Advanced", "India's joint military exercises held between December 2025 and April 2026",
   ["The second edition of Desert Cyclone with the UAE was held at the Mahajan Field Firing Range, Rajasthan.",
    "The 11th edition of LAMITIYE with Seychelles was held at the Seychelles Defence Academy.",
    "The fourth edition of Cyclone, a special forces exercise with Egypt, was held at Anshas, Egypt."],
   [False, True, True],
   "India's bilateral exercises",
   "Desert Cyclone-II (18-30 December 2025) was held at Al-Hamra Training City, Abu Dhabi. LAMITIYE 2026, the 11th "
   "India-Seychelles edition and its first tri-service one, was under way at the Seychelles Defence Academy in March "
   "2026. Cyclone-IV with Egypt was held at Anshas, Egypt, in April 2026; the third edition had been at Mahajan.",
   [fact("Desert Cyclone II, India-UAE, 18-30 December 2025, Al-Hamra Training City, Abu Dhabi", "n_dcyclone_gk"),
    fact("11th India-Seychelles LAMITIYE 2026 at Seychelles Defence Academy (13 March 2026)", "n_lamitiye_air"),
    fact("Exercise Cyclone 2026 (fourth edition), India-Egypt special forces, Anshas, Egypt; third edition at Mahajan",
         "n_cyclone_vaj")],
   why="Statement 1 is wrong: Desert Cyclone-II was held in Abu Dhabi; Mahajan hosted the third Cyclone with Egypt.",
   current=ca("2025-12-18"))

GS(T, DEF, "Advanced", "the Defence Acquisition Council (DAC) meeting of 27 March 2026",
   ["It cleared proposals worth about ₹2.38 lakh crore, including the S-400 long-range surface-to-air missile system "
    "for the Indian Air Force.",
    "It approved Heavy Duty Air Cushion Vehicles for the Indian Coast Guard."],
   [True, True],
   "DAC approvals, March 2026",
   "The DAC chaired by Defence Minister Rajnath Singh on 27 March 2026 cleared proposals worth ₹2,38,000 crore: for "
   "the Army, items such as the Dhanush gun system; for the IAF, Medium Transport Aircraft, the S-400 system and "
   "Remotely Piloted Strike Aircraft; and Heavy Duty Air Cushion Vehicles for the Coast Guard.",
   [fact("DAC on 27 March 2026 cleared ₹2,38,000 crore: S-400 and Medium Transport Aircraft for IAF, Dhanush for Army, "
         "Heavy Duty Air Cushion Vehicles for Coast Guard", "n_dac_air")],
   why="Both statements are correct.",
   current=ca("2026-03-27"))

GS(T, GOV, "Advanced", "Delhi Metro Phase V(A), approved by the Union Cabinet on 24 December 2025",
   ["It has three corridors with a total length of about 16 km.",
    "All its 13 stations are elevated.",
    "Its approved cost is about ₹12,015 crore."],
   [True, False, True],
   "Delhi Metro Phase V(A)",
   "Phase V(A) has three corridors, R.K. Ashram Marg-Indraprastha (9.913 km), Aerocity-IGD Airport T-1 (2.263 km) and "
   "Tughlakabad-Kalindi Kunj (3.9 km), totalling 16.076 km, at about ₹12,015 crore. Of its 13 stations, 10 are "
   "underground and 3 elevated; it is to be completed within three years.",
   [fact("Cabinet approved Delhi Metro Phase V(A) on 24 Dec 2025: three corridors, 16.076 km, 13 stations (10 "
         "underground, 3 elevated), Rs 12,015 crore", "n_metro_ians")],
   why="Statement 2 is wrong: 10 of the 13 stations are underground.",
   current=ca("2025-12-24"))

GS(T, ST, "Advanced", "the Andhra Pradesh Reorganisation (Amendment) Bill, 2026",
   ["It amends Section 5(2) of the Andhra Pradesh Reorganisation Act, 2014 to name Amaravati as the capital.",
    "The Rajya Sabha passed it by voice vote in April 2026.",
    "The Andhra Pradesh Legislative Assembly had passed a resolution in March 2026 asking for this amendment."],
   [True, True, True],
   "Amaravati as capital",
   "Parliament completed passage of the Bill when the Rajya Sabha passed it by voice vote on 2 April 2026, a day after "
   "the Lok Sabha. It amends Section 5(2) of the 2014 Act to make Amaravati the capital. The State Assembly had asked "
   "for it by a resolution of 28 March 2026.",
   [fact("Rajya Sabha passed AP Reorganisation (Amendment) Bill 2026 by voice vote on 2 April 2026; amends Section 5(2); "
         "AP Assembly resolution of 28 March 2026", "n_amaravati_air")],
   why="All three statements are correct.",
   current=ca("2026-04-02"))


# ###################################################################### part: intl
# BATCH_005 GA part: International Current Affairs (3/3/4) and Summits and Conferences (6/0/7).
# All URLs checked 2026-11-05. OPENED = fetched and read; SEARCH = search-result text only.

U.update({
    # ---------------- International
    "i_artemis": ("https://www.sciencedaily.com/releases/2026/04/260402004721.htm", OPENED),
    "i_my_nst": ("https://www.nst.com.my/amp/news/nation/2026/02/1373157/indian-pm-modi-arrives-malaysia-two-day-"
                 "official-visit", OPENED),
    "i_uae_kt": ("https://www.khaleejtimes.com/uae/president-sheikh-mohamed-india-pm-modi-discussions-agreements-state-"
                 "visit", OPENED),
    "i_cy_politis": ("https://en.politis.com.cy/news/politics/1007121/christodoulides-and-modi-upgrade-cyprus-india-ties-"
                     "to-strategic-partnership", OPENED),
    "i_cy_pmi": ("https://www.pmindia.gov.in/en/news_updates/joint-statement-on-the-state-visit-of-the-president-of-the-"
                 "republic-of-cyprus/", SEARCH),
    "i_jp_wion": ("https://www.wionews.com/india-news/live-blog-india-japan-annual-summit-2026-live-updates-modi-sanae-"
                  "takaichi-meeting-strategic-partnership-summit-bullet-train-energy-crisis-china-iranus-war-"
                  "1782964181685", OPENED),
    "i_br_star": ("https://www.thestar.com.my/news/world/2026/02/21/india-brazil-sign-mining-pact-as-modi-targets-20-"
                  "billion-trade-in-five-years", OPENED),
    "i_fr_myind": ("https://myind.net/Home/viewArticle/india-france-announce-special-global-strategic-partnership-pm-"
                   "modi-and-macron-inaugurate-innovation-year-2026", OPENED),
    "i_sk_ians": ("https://ianslive.in/pm-modi-makes-history-in-bratislava-as-india-and-slovakia-sign-agreements-mea--"
                  "20260616024333", OPENED),
    "i_who_pabs": ("https://www.who.int/news/item/01-05-2026-who-member-states-agree-to-extend-negotiations-on-pathogen-"
                   "access-and-benefit-sharing-annex", OPENED),
    "i_bbnj_ec": ("https://oceans-and-fisheries.ec.europa.eu/news/high-seas-treaty-enters-force-milestone-ocean-"
                  "conservation-2026-01-16_en", OPENED),
    # ---------------- Summits
    "i_adb": ("https://www.adb.org/news/uzbekistan-host-59th-adb-annual-meeting-2026", OPENED),
    "i_unccd_star": ("https://www.thestar.com.my/aseanplus/aseanplus-news/2026/08/31/unccd-cop17-concludes-successfully-"
                     "in-mongolia", OPENED),
    "i_unccd_site": ("https://www.unccd.int/index%2Ephp/events/governing-bodies-meetings/unccd-cop17", SEARCH),
    "i_sld": ("https://www.mindef.gov.sg/news-and-events/latest-releases/28may26-nr/", OPENED),
    "i_wuf": ("https://www.euronews.com/2026/05/22/bigger-than-ever-wuf13-ends-with-global-call-for-action", OPENED),
    "i_wgs": ("https://www.tribuneindia.com/news/world/world-governments-summit-to-hold-next-edition-from-3-5-february-"
              "2026", OPENED),
    "i_scochg26": ("https://www.manoramayearbook.in/current-affairs/india/2026/10/21/rajnath-singh-sco-meeting-in-"
                   "dushanbe.html", OPENED),
    "i_scochg25": ("https://eng.sectsco.org/20251118/2057714.html", OPENED),
    "i_msc": ("https://www.tribuneindia.com/news/world/eam-jaishankar-meets-g7-foreign-ministers-in-munich-security-"
              "conference-2026/", OPENED),
    "i_cites_uz": ("https://gov.uz/en/news/view/109005", OPENED),
    "i_cites_dte": ("https://www.downtoearth.org.in/wildlife-biodiversity/cites-cop20-global-south-drives-critical-"
                    "changes-and-shapes-global-wildlife-trade-policies", OPENED),
    "i_cites_tr": ("https://www.traffic.org/news/traffic-hails-landmark-decisions-at-cites-cop20-but-urges-continued-"
                   "action/", OPENED),
    "i_cbd_dte": ("https://www.downtoearth.org.in/wildlife-biodiversity/yerevan-pathway-cop17-ends-with-decisions-on-50-"
                  "agenda-items", OPENED),
    "i_cbd_lnb": ("https://www.lexisnexis.co.uk/legal/news/cop17-adopts-yerevan-pathway-to-accelerate-global-"
                  "biodiversity-protection", OPENED),
    "i_g20_wiki": ("https://en.wikipedia.org/wiki/2026_G20_Miami_summit", OPENED),
    "i_unga_photo": ("https://media.un.org/photo/en/asset/oun7/oun71152374", OPENED),
    "i_unga_cgtn": ("https://news.cgtn.com/news/2026-09-29/UN-General-Assembly-concludes-General-Debate-1QPcgWktrqM/"
                    "p.html", OPENED),
    "i_au_aa": ("https://allafrica.com/stories/202602160070.html", OPENED),
    "i_au_ol": ("https://www.outlookindia.com/international/burundi-assumes-african-union-chairmanship-for-2026", OPENED),
    "i_chogm_wiki": ("https://en.wikipedia.org/wiki/2026_Commonwealth_Heads_of_Government_Meeting", OPENED),
})

# ====================================================================== International Current Affairs (3 / 3 / 4)
T = "International Current Affairs"
BIL, GLO = "Bilateral relations", "Global events"

G(T, GLO, "Basic",
  "Jeremy Hansen was one of the four astronauts on NASA's Artemis II mission, launched on 1 April 2026 on the first "
  "crewed flight around the Moon in more than 50 years. Which space agency does he belong to?",
  ["Canadian Space Agency", "European Space Agency", "Japan Aerospace Exploration Agency", "UK Space Agency"], "*",
  "Artemis II crew",
  "Artemis II lifted off from Launch Pad 39B at Kennedy Space Center on 1 April 2026 on the SLS rocket, with the Orion "
  "capsule (named 'Integrity' by its crew). The crew was NASA's Reid Wiseman, Victor Glover and Christina Koch and the "
  "Canadian Space Agency's Jeremy Hansen.",
  ["Launch: 1 Apr 2026, Kennedy Space Center", "Crew: Wiseman, Glover, Koch (NASA) + Hansen (CSA)"],
  [fact("Artemis II launched 1 April 2026 from Pad 39B; crew Wiseman, Glover, Koch (NASA) and Jeremy Hansen (Canadian "
        "Space Agency); first crewed flight around the Moon in more than 50 years", "i_artemis")],
  why="Hansen is a Canadian Space Agency astronaut, not from ESA, JAXA or the UK Space Agency.",
  current=ca("2026-04-01"))

G(T, BIL, "Basic",
  "Prime Minister Narendra Modi made a two-day official visit to which country on 7-8 February 2026, at the "
  "invitation of Prime Minister Anwar Ibrahim?",
  ["Malaysia", "Indonesia", "Brunei", "Singapore"], "*",
  "PM's visit to Malaysia",
  "Modi arrived in Malaysia on 7 February 2026 for a two-day official visit at the invitation of Prime Minister Anwar "
  "Ibrahim. It was his third trip to Malaysia and the first since the two countries raised their ties to a "
  "Comprehensive Strategic Partnership.",
  ["Host: PM Anwar Ibrahim", "Country: Malaysia", "Visit: 7-8 Feb 2026"],
  [fact("Modi arrived in Malaysia on 7 February 2026 for a two-day official visit at Anwar Ibrahim's invitation; third "
        "trip; first since ties became a Comprehensive Strategic Partnership", "i_my_nst")],
  why="Anwar Ibrahim is the Prime Minister of Malaysia, not of Indonesia, Brunei or Singapore.",
  current=ca("2026-02-07"))

G(T, BIL, "Basic",
  "During the UAE President Sheikh Mohamed bin Zayed Al Nahyan's visit to India on 19 January 2026, the two leaders "
  "announced a 'House of India', a cultural space with a museum of Indian art and heritage. In which city will it be "
  "set up?",
  ["Abu Dhabi", "Dubai", "Sharjah", "Ras Al Khaimah"], "*",
  "India-UAE: House of India",
  "Sheikh Mohamed bin Zayed arrived in New Delhi on 19 January 2026. The outcomes included a 'House of India' in Abu "
  "Dhabi with a museum of Indian art, heritage and archaeology, and a target of doubling bilateral trade to USD 200 "
  "billion by 2032.",
  ["Visit: 19 Jan 2026", "House of India: Abu Dhabi", "Trade target: USD 200 bn by 2032"],
  [fact("UAE President's visit to India on 19 January 2026; House of India to be set up in Abu Dhabi with a museum of "
        "Indian art, heritage and archaeology; trade target USD 200 billion by 2032", "i_uae_kt")],
  why="The House of India is planned for Abu Dhabi, the UAE capital, not Dubai, Sharjah or Ras Al Khaimah.",
  current=ca("2026-01-19"))

G(T, BIL, "Intermediate",
  "During Cypriot President Nikos Christodoulides' state visit to India in May 2026, to what level did India and "
  "Cyprus upgrade their bilateral relationship?",
  ["Strategic Partnership", "Comprehensive Strategic Partnership", "Special Global Strategic Partnership",
   "Privileged Partnership"], "*",
  "India-Cyprus relations",
  "The Joint Declaration of May 2026 upgraded the India-Cyprus Comprehensive Partnership to a Strategic Partnership. "
  "The visit (20-23 May 2026) produced 11 deliverables, including a defence cooperation roadmap for 2026-2031 and an "
  "MoU on a counter-terrorism joint working group.",
  ["Earlier: Comprehensive Partnership", "May 2026: upgraded to Strategic Partnership",
   "Also: Defence Roadmap 2026-2031"],
  [fact("Leaders agreed to upgrade the bilateral Comprehensive Partnership to a Strategic Partnership; 11 deliverables; "
        "defence cooperation roadmap 2026-2031", "i_cy_politis"),
   fact("President of Cyprus paid a State Visit to India from 20-23 May 2026; relations upgraded to a Strategic "
        "Partnership", "i_cy_pmi")],
  why="'Comprehensive Partnership' was the earlier level; 'Special Global Strategic Partnership' describes India-France "
      "ties; 'Privileged Partnership' is not the term used.",
  current=ca("2026-05-22"))

G(T, BIL, "Intermediate",
  "Japanese Prime Minister Sanae Takaichi's visit to New Delhi in July 2026, her first to India as Prime Minister, was "
  "for which edition of the India-Japan Annual Summit?",
  ["16th", "15th", "17th", "14th"], "*",
  "India-Japan Annual Summit",
  "Takaichi arrived in New Delhi on 1 July 2026 and the summit talks were held on 2 July 2026; it was the 16th "
  "India-Japan Annual Summit. Outcomes included a joint declaration on economic security, joint statements on AI and "
  "energy resilience, and MoUs on critical minerals and batteries, pharma and next-generation mobility. The 15th "
  "summit had been held in Japan in August 2025.",
  ["15th summit: Japan, Aug 2025 (PM Modi's visit)", "16th summit: New Delhi, 2 Jul 2026"],
  [fact("16th India-Japan Annual Summit; Takaichi arrived New Delhi 1 July 2026, talks 2 July 2026; her first visit "
        "to India as PM; economic security declaration, AI and energy statements", "i_jp_wion")],
  why="The 15th summit was Modi's August 2025 visit to Japan; 14th and 17th are wrong editions.",
  current=ca("2026-07-02"))

G(T, BIL, "Intermediate",
  "After talks with Brazilian President Luiz Inácio Lula da Silva in New Delhi on 21 February 2026, what bilateral "
  "trade goal did Prime Minister Modi announce?",
  ["Taking trade well beyond USD 20 billion in the next five years",
   "Doubling trade to USD 100 billion by 2030",
   "Reaching USD 50 billion of trade by 2028",
   "Settling all bilateral trade in national currencies by 2027"], "*",
  "India-Brazil relations",
  "During Lula's state visit, the two sides signed a mining and minerals cooperation agreement on 21 February 2026. "
  "Modi said India was committed to taking bilateral trade much beyond USD 20 billion in the next five years, from about "
  "USD 15 billion now. Brazil is India's largest trading partner in Latin America and the Caribbean.",
  ["Current trade: about USD 15 bn", "Goal: well beyond USD 20 bn in five years", "Pact: mining and minerals"],
  [fact("21 Feb 2026, New Delhi: India and Brazil sign mining pact; Modi: 'committed to taking bilateral trade much "
        "beyond $20 billion in the next five years'; current trade about $15 billion", "i_br_star")],
  why="The other figures were not announced; Lula urged trade in national currencies but no deadline was set.",
  current=ca("2026-02-21"))

GS(T, BIL, "Advanced", "French President Emmanuel Macron's visit to India in February 2026",
   ["He and Prime Minister Modi inaugurated the 'India-France Year of Innovation 2026' in Mumbai on 17 February 2026.",
    "India and France announced that their ties had been raised to a 'Special Global Strategic Partnership'.",
    "It was Macron's first visit to India as President."],
   [True, True, False],
   "India-France relations",
   "Macron's visit (17-19 February 2026) began in Mumbai, where talks were held at Lok Bhavan and the India-France Year "
   "of Innovation 2026 was inaugurated; ties were described as a 'Special Global Strategic Partnership'. He then went "
   "to New Delhi for the AI Impact Summit. It was his fourth visit to India (and his first to Mumbai).",
   [fact("17 Feb 2026, Mumbai: India-France Year of Innovation 2026 inaugurated; 'Special Global Strategic "
         "Partnership'; Macron's fourth visit to India and first to Mumbai, 17-19 Feb", "i_fr_myind")],
   why="Statement 3 is wrong: it was Macron's fourth visit to India.",
   current=ca("2026-02-17"))

GS(T, BIL, "Advanced", "Prime Minister Modi's visit to Slovakia in June 2026",
   ["It was the first visit by an Indian Prime Minister to Slovakia since its independence in 1993.",
    "India and Slovakia raised their ties to a Strategic Partnership.",
    "Modi was conferred the Order of the White Double Cross, First Class, Slovakia's highest civilian honour."],
   [True, False, True],
   "India-Slovakia relations",
   "Modi visited Bratislava on 15-16 June 2026 at the invitation of Prime Minister Robert Fico, the first visit by an "
   "Indian PM since Slovakia's independence in 1993. The two sides agreed on a 'Comprehensive Partnership', and "
   "President Peter Pellegrini conferred the Order of the White Double Cross, First Class, on Modi. He then went on "
   "to the G7 summit in France.",
   [fact("First ever visit by an Indian PM to Slovakia since its independence in 1993; ties raised to a 'Comprehensive "
         "Partnership'; Order of the White Double Cross First Class conferred; Bratislava, June 2026", "i_sk_ians")],
   why="Statement 2 is wrong: the new level is a Comprehensive Partnership, not a Strategic Partnership.",
   current=ca("2026-06-15"))

GS(T, GLO, "Advanced", "the WHO Pandemic Agreement",
   ["The World Health Assembly adopted the Pandemic Agreement in May 2025.",
    "In May 2026 member states finalised the Pathogen Access and Benefit Sharing (PABS) annex, opening the agreement "
    "for signature."],
   [True, False],
   "WHO Pandemic Agreement",
   "The WHA adopted the Pandemic Agreement in May 2025 (resolution WHA78.1), but it cannot be signed or ratified until "
   "the PABS annex is finalised. On 1 May 2026 the Intergovernmental Working Group (IGWG) agreed it needed more time; "
   "the outcome is to go to the WHA in May 2027 or to a special session in 2026.",
   [fact("WHA adopted the Pandemic Agreement in May 2025; on 1 May 2026 member states agreed to extend PABS annex "
         "negotiations; signature and ratification wait for the annex", "i_who_pabs")],
   why="Statement 2 is wrong: the PABS annex was not finalised; negotiations were extended.",
   current=ca("2026-05-01"))

GS(T, GLO, "Advanced", "the Agreement on Biodiversity Beyond National Jurisdiction (BBNJ, the 'High Seas Treaty')",
   ["It was adopted at the UN Ocean Conference held in Nice in 2025.",
    "It entered into force on 17 January 2026, 120 days after the threshold of 60 ratifications was reached.",
    "It covers ocean areas beyond national jurisdiction, about half of the planet's surface."],
   [False, True, True],
   "High Seas Treaty",
   "The BBNJ Agreement was concluded and adopted in 2023. The 60-ratification threshold was reached on 19 September "
   "2025 and the treaty entered into force 120 days later, on 17 January 2026. It covers the high seas, about half of "
   "the planet's surface and 95% of the ocean's volume; its first COP is due within a year of entry into force.",
   [fact("BBNJ concluded and adopted in 2023; 60 ratifications reached 19 Sep 2025; entry into force 17 Jan 2026; covers "
         "about half of the planet's surface and 95% of ocean volume", "i_bbnj_ec")],
   why="Statement 1 is wrong: the agreement was adopted in 2023, not at the 2025 Nice conference.",
   current=ca("2026-01-17"))

# ====================================================================== Summits and Conferences (6 / 0 / 7)
T = "Summits and Conferences"
GRP, HOST = "G20, BRICS, SCO and others", "Hosting countries"

G(T, HOST, "Basic",
  "The 59th Annual Meeting of the Asian Development Bank was held from 3 to 6 May 2026 in which city?",
  ["Samarkand", "Tashkent", "Tbilisi", "Baku"], "*",
  "ADB Annual Meeting 2026",
  "Uzbekistan hosted the 59th ADB Annual Meeting in Samarkand from 3 to 6 May 2026. It was the country's second time "
  "as host: Tashkent hosted the 43rd Annual Meeting in 2010.",
  ["59th meeting: Samarkand, 3-6 May 2026", "Uzbekistan's earlier hosting: Tashkent, 43rd meeting, 2010"],
  [fact("59th ADB Annual Meeting in Samarkand, Uzbekistan, 3-6 May 2026; Uzbekistan's second time after Tashkent "
        "(43rd, 2010)", "i_adb")],
  why="Tashkent hosted in 2010; Tbilisi and Baku did not host the 2026 meeting.",
  current=ca("2026-05-03"))

G(T, HOST, "Basic",
  "The 17th session of the Conference of the Parties to the UN Convention to Combat Desertification (UNCCD COP17), "
  "held from 17 to 28 August 2026 under the theme 'Restoring Land, Restoring Hope', was hosted by which country?",
  ["Mongolia", "Saudi Arabia", "Kazakhstan", "Egypt"], "*",
  "UNCCD COP17",
  "UNCCD COP17 was held in Ulaanbaatar, Mongolia, from 17 to 28 August 2026, during the International Year of "
  "Rangelands and Pastoralists. COP16 had been held in Riyadh, Saudi Arabia, in 2024.",
  ["COP16: Riyadh (2024)", "COP17: Ulaanbaatar, Mongolia, 17-28 Aug 2026"],
  [fact("UNCCD COP17 held 17-28 August 2026 in Ulaanbaatar, Mongolia; theme 'Restoring Land, Restoring Hope'",
        "i_unccd_star"),
   fact("UNCCD COP17, Ulaanbaatar, Mongolia, 17-28 August 2026", "i_unccd_site")],
  why="Saudi Arabia hosted COP16; Kazakhstan and Egypt did not host COP17.",
  current=ca("2026-08-17"))

G(T, GRP, "Basic",
  "At the 23rd Shangri-La Dialogue, held in Singapore from 29 to 31 May 2026, the keynote address was delivered by the "
  "leader of which country?",
  ["Vietnam", "Indonesia", "Timor-Leste", "Philippines"], "*",
  "Shangri-La Dialogue 2026",
  "The Shangri-La Dialogue is Asia's top defence forum, organised by the International Institute for Strategic Studies "
  "(IISS) in Singapore. In 2026 the keynote was given on 29 May by To Lam, General Secretary of the Communist Party of "
  "Vietnam and President of Vietnam; Timor-Leste's President José Ramos-Horta gave a special address on 30 May.",
  ["Organiser: IISS", "23rd edition: 29-31 May 2026", "Keynote: To Lam (Vietnam)"],
  [fact("23rd Shangri-La Dialogue, 29-31 May 2026, organised by IISS; keynote address by To Lam of Vietnam on 29 May; "
        "special address by Timor-Leste's President on 30 May; 44 countries", "i_sld")],
  why="Timor-Leste's President gave a special address, not the keynote; Indonesia and the Philippines did not deliver it.",
  current=ca("2026-05-29"))

G(T, HOST, "Basic",
  "The thirteenth session of the World Urban Forum (WUF13), convened by UN-Habitat, ended on 22 May 2026 with the "
  "adoption of a 'Call to Action'. In which city was it held?",
  ["Baku", "Cairo", "Nairobi", "Abu Dhabi"], "*",
  "World Urban Forum 13",
  "WUF13 was held in Baku, Azerbaijan, with housing at the centre of its agenda, and closed on 22 May 2026 with the Baku "
  "Call to Action. It drew over 57,000 attendees from more than 176 countries. Mexico is preparing to host WUF14.",
  ["WUF13: Baku, Azerbaijan", "Outcome: Baku Call to Action", "Organiser: UN-Habitat"],
  [fact("WUF13 in Baku ended 22 May 2026 with the Baku Call to Action; housing focus; over 57,000 attendees; UN-Habitat",
        "i_wuf")],
  why="Cairo hosted WUF12 (2024) and Abu Dhabi WUF10 (2020); Nairobi is UN-Habitat's headquarters, not the WUF13 host.",
  current=ca("2026-05-22"))

G(T, HOST, "Basic",
  "The World Governments Summit 2026 was held from 3 to 5 February 2026 in which city?",
  ["Dubai", "Abu Dhabi", "Doha", "Riyadh"], "*",
  "World Governments Summit",
  "The World Governments Summit is held every year in Dubai, UAE; it is chaired by the UAE's Minister of Cabinet Affairs "
  "Mohammad Al Gergawi. The 2026 edition was held from 3 to 5 February 2026.",
  ["WGS 2026: 3-5 Feb 2026", "Venue city: Dubai"],
  [fact("Next edition of the World Governments Summit to take place in Dubai from February 3 to February 5, 2026",
        "i_wgs")],
  why="The summit is held in Dubai, not Abu Dhabi, Doha or Riyadh.",
  current=ca("2026-02-03"))

G(T, GRP, "Basic",
  "Who represented India at the 25th meeting of the SCO Council of Heads of Government held in Dushanbe, Tajikistan, "
  "on 20 October 2026?",
  ["Rajnath Singh", "S. Jaishankar", "Amit Shah", "Nirmala Sitharaman"], "*",
  "SCO Council of Heads of Government",
  "Defence Minister Rajnath Singh represented India at the 25th SCO Council of Heads of Government meeting in Dushanbe "
  "on 20 October 2026. The meeting adopted a joint communique with the SCO budget for 2027, and Uzbekistan took over "
  "the rotating presidency of the Council. At the previous meeting, in Moscow on 18 November 2025, India was "
  "represented by External Affairs Minister S. Jaishankar.",
  ["25th CHG: Dushanbe, 20 Oct 2026", "India: Rajnath Singh", "Previous (Moscow, 2025): S. Jaishankar"],
  [fact("25th SCO CHG meeting in Dushanbe on 20 October; India represented by Defence Minister Rajnath Singh; previous "
        "meeting in Moscow on 18 Nov 2025 attended by Jaishankar; Uzbekistan assumed CHG presidency", "i_scochg26")],
  why="Jaishankar represented India at the 2025 Moscow meeting, not at Dushanbe; Shah and Sitharaman did not attend.",
  current=ca("2026-10-20"))

GS(T, GRP, "Advanced", "the 62nd Munich Security Conference",
   ["It was held from 13 to 15 February 2026 at the Hotel Bayerischer Hof and the Rosewood Munich.",
    "External Affairs Minister S. Jaishankar met the G7 foreign ministers on its sidelines."],
   [True, True],
   "Munich Security Conference 2026",
   "The 62nd MSC took place in Munich on 13-15 February 2026. On 14 February Jaishankar met the G7 foreign ministers "
   "and held bilateral meetings, backed the UN80 agenda and Security Council reform, and stressed India's maritime "
   "security role.",
   [fact("62nd Munich Security Conference, 13-15 February 2026, Hotel Bayerischer Hof and Rosewood Munich; Jaishankar "
         "met G7 foreign ministers on 14 February", "i_msc")],
   why="Both statements are correct.",
   current=ca("2026-02-13"))

GS(T, HOST, "Advanced", "the 20th Conference of the Parties to CITES (CoP20)",
   ["It was held in Tashkent, Uzbekistan.",
    "It was the first CITES Conference of the Parties held in Central Asia and marked the 50th anniversary of the "
    "Convention.",
    "It added 77 species to the CITES appendices."],
   [False, True, True],
   "CITES CoP20",
   "CITES CoP20 was held in Samarkand, Uzbekistan, and ended in early December 2025. It was the first CoP held in "
   "Central Asia and coincided with the Convention's 50th anniversary. Delegates adopted 353 decisions and added 77 "
   "species to the appendices, moving whale sharks, oceanic whitetip sharks and all manta and devil rays to Appendix I; "
   "proposals to reopen rhino horn and ivory trade were rejected. CoP21 is to be held in Panama.",
   [fact("CoP20 in Samarkand marked the 50th anniversary of the Convention; first CoP in Central Asia; 353 decisions; "
         "77 species added", "i_cites_dte"),
    fact("First CITES CoP in Central Asia, held in Samarkand; 77 new species in the appendices; CoP21 in Panama",
         "i_cites_uz"),
    fact("CoP20 in Samarkand concluded on a Friday; article dated 8 December 2025; CITES marks 50 years", "i_cites_tr")],
   why="Statement 1 is wrong: CoP20 was held in Samarkand, not Tashkent.",
   current=ca("2025-12-05"))

GS(T, HOST, "Advanced", "COP17 of the Convention on Biological Diversity (CBD)",
   ["It was held in Yerevan, Armenia, and adopted an outcome called the 'Yerevan Pathway'.",
    "Its first global review found the world on track to meet all 23 targets of the Kunming-Montreal Global "
    "Biodiversity Framework by 2030.",
    "The next COP is to be held in Ecuador in 2028."],
   [True, False, True],
   "CBD COP17",
   "CBD COP17 in Yerevan, presided over by Armenia's Environment Minister, ended on 31 October 2026 with about 50 "
   "decisions grouped as the Yerevan Pathway. Its first review of the Kunming-Montreal framework found the world off "
   "track to meet the 23 targets by 2030. COP18 will be held in Ecuador in 2028.",
   [fact("COP17 in Yerevan, Armenia, adopted the Yerevan Pathway (about 50 agenda items); next COP in Ecuador in 2028",
         "i_cbd_dte"),
    fact("COP17 concluded 31 October 2026 in Yerevan; first review found the world off track to meet its 23 targets by "
         "2030", "i_cbd_lnb")],
   why="Statement 2 is wrong: the review found the world off track.",
   current=ca("2026-10-31"))

GS(T, GRP, "Advanced", "the G20 under the presidency of the United States",
   ["The 21st G20 summit is scheduled for 14-15 December 2026 at Trump National Doral Miami in Florida.",
    "On 27 November 2025 President Trump announced that South Africa would not be invited to the 2026 summit.",
    "Poland is among the countries invited as guests."],
   [True, True, True],
   "G20 2026",
   "The US took over the G20 presidency after the Johannesburg summit. The 21st summit is set for 14-15 December 2026 "
   "at Trump National Doral Miami. On 27 November 2025 Trump said South Africa would not be invited; Poland is among "
   "the invited guest countries.",
   [fact("21st G20 summit, 14-15 December 2026, Trump National Doral Miami; on 27 November 2025 Trump announced South "
         "Africa would not be invited; Poland an invited guest", "i_g20_wiki")],
   why="All three statements are correct.",
   current=ca("2025-11-27"))

GS(T, GRP, "Advanced", "the general debate of the 81st session of the UN General Assembly",
   ["Its theme was 'Restoring trust, managing transformation: a United Nations that delivers for all'.",
    "It concluded on 28 September 2026 with closing remarks by UN Secretary-General António Guterres."],
   [True, False],
   "UNGA 81 general debate",
   "The general debate opened on 22 September 2026 under the theme 'Restoring trust, managing transformation: a United "
   "Nations that delivers for all'. It concluded on 28 September 2026 after 194 delegations had spoken; the closing "
   "remarks were given by the President of the General Assembly, Khalilur Rahman of Bangladesh.",
   [fact("Theme of the 81st session general debate: 'Restoring trust, managing transformation: a United Nations that "
         "delivers for all' (22 September 2026)", "i_unga_photo"),
    fact("General Debate concluded on 28 September 2026; 194 delegations; closing remarks by GA President Khalilur "
         "Rahman", "i_unga_cgtn")],
   why="Statement 2 is wrong: the closing remarks were given by the President of the General Assembly.",
   current=ca("2026-09-22"))

GS(T, GRP, "Advanced", "the 39th Ordinary Session of the African Union Assembly held in February 2026",
   ["It was held at the AU headquarters in Addis Ababa, where Burundi's President Évariste Ndayishimiye became AU "
    "Chairperson for 2026.",
    "He succeeded Angola's President João Lourenço.",
    "Ghana's President John Dramani Mahama was elected Second Vice-Chairperson."],
   [True, True, False],
   "African Union summit 2026",
   "The 39th Ordinary Session began on 14 February 2026 in Addis Ababa under the theme of sustainable water availability "
   "and safe sanitation for Agenda 2063. Burundi's Ndayishimiye took over from Angola's Lourenço. Ghana took the First "
   "Vice-Chair, Tanzania the Second Vice-Chair, and Angola became Rapporteur.",
   [fact("39th Ordinary Session began 14 Feb 2026, Addis Ababa; Ndayishimiye of Burundi chair for 2026, succeeding "
         "Lourenço of Angola; Ghana First Vice, Tanzania Second Vice; theme on water and sanitation", "i_au_aa"),
    fact("Burundi's President Ndayishimiye took over as AU Chairperson at AU headquarters, Addis Ababa, from Angola's "
         "Lourenço", "i_au_ol")],
   why="Statement 3 is wrong: Ghana was elected First Vice-Chair; Tanzania holds the Second Vice-Chair.",
   current=ca("2026-02-14"))

GS(T, HOST, "Advanced", "the Commonwealth Heads of Government Meeting (CHOGM) 2026",
   ["It was held in Bridgetown, Barbados.",
    "The host country is described as the smallest country to have hosted a CHOGM, and its Prime Minister Gaston "
    "Browne became Chair-in-Office.",
    "Its theme was 'Accelerating Partnerships and Investment for a Prosperous Commonwealth'."],
   [False, True, True],
   "CHOGM 2026",
   "CHOGM 2026 was held in St John's, Antigua and Barbuda, on 3-4 November 2026, with linked events from 1 November. "
   "Antigua and Barbuda, chosen at the 2024 meeting in Samoa, is described as the smallest country to host a CHOGM; "
   "its Prime Minister Gaston Browne is the Chair-in-Office.",
   [fact("CHOGM 2026 in St John's, Antigua and Barbuda, 3-4 November 2026; theme 'Accelerating Partnerships and "
         "Investment for a Prosperous Commonwealth'; Chair-in-Office PM Gaston Browne; smallest country to host",
         "i_chogm_wiki")],
   why="Statement 1 is wrong: the host was St John's, Antigua and Barbuda.",
   current=ca("2026-11-03"))


# ###################################################################### part: appt
# BATCH_005 GA fragment: Important Appointments (8/3/7) and National and International Organizations (5/1/4).
# Exec'd inside tools/batch_005/ga.py. All URLs below were checked on 2026-11-05.

U.update({
    # ---------------- Appointments
    "a_nowais_wiki": ("https://en.wikipedia.org/wiki/Shaikha_Al_Nowais", OPENED),
    "a_nowais_vs": ("https://voyagesafriq.com/2025/05/30/shaikha-al-nowais-elected-as-un-tourism-secretary-general-"
                    "becoming-first-woman-to-lead-the-organisation/", SEARCH),
    "a_bb_print": ("https://theprint.in/world/mostaqur-rahman-appointed-bangladesh-cenbank-head-government-says/2863689",
                   OPENED),
    "a_wfp_gk": ("https://www.gktoday.in/un-appoints-luke-lindberg-to-head-world-food-programme/", OPENED),
    "a_hrc_un": ("https://news.un.org/en/story/2026/01/1166720", OPENED),
    "a_fsib_gk": ("https://www.gktoday.in/scl-das-to-lead-financial-services-institutions-bureau/", OPENED),
    "a_niacl_psu": ("https://psuwatch.com/amp/story/psu-appointments/lavanya-r-mundayur-appointed-new-india-assurance-"
                    "cmd-till-may-2029", OPENED),
    "a_niacl_nse": ("https://nsearchives.nseindia.com/corporate/NIACL_30092026181625_CMD_appointment.pdf", SEARCH),
    "a_gic_rn": ("https://www.reinsurancene.ws/hitesh-joshi-appointed-gic-re-chairman-and-managing-director/", OPENED),
    "a_au_psu": ("https://www.psuconnect.in/bank-news/rbi-approves-sanjay-agarwal-reappointment-as-au-small-finance-bank-"
                 "md-ceo", OPENED),
    "a_malli_rbi": ("https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63719", OPENED),
    "a_rshankar_rbi": ("https://rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=63064", OPENED),
    "a_monisha_rbi": ("https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63279", OPENED),
    "a_cbdt_air": ("https://newsonair.gov.in/ravi-agrawal-re-appointed-as-cbdt-chairman/", OPENED),
    "a_juma_star": ("https://www.the-star.co.ke/news/2026-03-07-monica-juma-lands-top-un-job", OPENED),
    "a_shin_mv": ("https://mondovisione.com/news/bis-statement-on-the-appointment-of-hyun-song-shin-as-governor-of-the-"
                  "bank-of-k-2026420/", OPENED),
    "a_turk_kas": ("https://www.kas.de/en/web/multilateraler-dialog-genf/map-of-the-month/detail/-/content/abstimmung-der-"
                   "un-generalversammlung-zu-mandatsverlaengerung-von-volker-tuerk-un-hochkommissar-fuer-", OPENED),
    "a_turk_aaw": ("https://english.aawsat.com/node/5299861", OPENED),
    "a_unido_aa": ("https://allafrica.com/stories/202511240176.html", OPENED),
    "a_unido_un": ("https://www.unido.org/news/unido-gerd-muller-appointed-second-term-director-general", SEARCH),
    "a_ifsca_sec": ("https://thesecretariat.in/article/centre-extends-k-rajaraman-s-tenure-as-ifsca-chairperson-till-"
                    "october-2028", OPENED),
    "a_uco_hb": ("https://hellobanker.in/uco-bank-md-ceo-post-falls-vacant-ed-rajendra-saboo-gets-additional-charge/",
                 OPENED),
    # ---------------- Organisations
    "a_escap_wiki": ("https://en.wikipedia.org/wiki/United_Nations_Economic_and_Social_Commission_for_Asia_and_the_"
                     "Pacific", OPENED),
    "a_pif_wiki": ("https://en.wikipedia.org/wiki/Pacific_Islands_Forum", OPENED),
    "a_cdri_wiki": ("https://en.wikipedia.org/wiki/Coalition_for_Disaster_Resilient_Infrastructure", OPENED),
    "a_oic_wiki": ("https://en.wikipedia.org/wiki/Organisation_of_Islamic_Cooperation", OPENED),
    "a_iea_dd": ("https://www.devdiscourse.com/article/headlines/3810743-colombia-joins-the-iea-a-new-era-in-energy-policy",
                 OPENED),
    "a_eaeu_wiki": ("https://en.wikipedia.org/wiki/Eurasian_Economic_Union", OPENED),
    "a_iora_wiki": ("https://en.wikipedia.org/wiki/Indian_Ocean_Rim_Association", OPENED),
    "a_nato_wiki": ("https://en.wikipedia.org/wiki/NATO", OPENED),
    "a_apec_wiki": ("https://en.wikipedia.org/wiki/Asia-Pacific_Economic_Cooperation", OPENED),
})

# ====================================================================== Important Appointments (8 / 3 / 7)
T = "Important Appointments"
BF, IB = "Banking and finance heads", "International bodies"

G(T, IB, "Basic",
  "Shaikha Al Nowais of the UAE, who took office on 1 January 2026 as the first woman to lead it, is the "
  "Secretary-General of which UN agency?",
  ["UN Tourism (World Tourism Organization)", "International Maritime Organization",
   "International Telecommunication Union", "Universal Postal Union"], "*",
  "UN Tourism leadership",
  "Shaikha Al Nowais, an Emirati hospitality executive, became the seventh Secretary-General of UN Tourism (formerly "
  "UNWTO) on 1 January 2026. She succeeded Zurab Pololikashvili, who served from 2018 to 2025, and is the first woman "
  "to hold the post.",
  ["Agency: UN Tourism (UNWTO)", "Term began 1 January 2026", "Predecessor: Zurab Pololikashvili"],
  [fact("Shaikha Al Nowais: Secretary-General of UN Tourism from 1 January 2026, first woman; predecessor Zurab "
        "Pololikashvili", "a_nowais_wiki"),
   fact("Shaikha Al Nowais elected UN Tourism Secretary-General, first woman to lead the organisation", "a_nowais_vs")],
  why="The IMO, ITU and UPU are led by other people; she heads UN Tourism.",
  current=ca("2026-01-01"))

G(T, BF, "Basic",
  "Md Mostaqur Rahman was appointed in February 2026 for a four-year term as Governor of which central bank?",
  ["Bangladesh Bank", "Nepal Rastra Bank", "Central Bank of Sri Lanka", "State Bank of Pakistan"], "*",
  "Central bank governors in South Asia",
  "On 25 February 2026 the government of Bangladesh appointed Md Mostaqur Rahman, a corporate finance and governance "
  "specialist, as Governor of Bangladesh Bank for four years. He replaced Ahsan H. Mansur. The change came soon after "
  "Tarique Rahman's government took office.",
  ["Bank: Bangladesh Bank", "Announced 25 Feb 2026", "Term: four years; predecessor Ahsan H. Mansur"],
  [fact("Mostaqur Rahman appointed Bangladesh central bank governor for a four-year term (25 Feb 2026), replacing "
        "Ahsan H. Mansur", "a_bb_print")],
  why="The appointment was to Bangladesh Bank, not the central banks of Nepal, Sri Lanka or Pakistan.",
  current=ca("2026-02-25"))

G(T, IB, "Basic",
  "On 18 September 2026 the UN appointed US agriculture official Luke Lindberg as the Executive Director of which "
  "agency?",
  ["World Food Programme", "Food and Agriculture Organization", "International Fund for Agricultural Development",
   "UNICEF"], "*",
  "WFP leadership",
  "Luke Lindberg, earlier the US Department of Agriculture's Undersecretary for Trade and Foreign Agricultural "
  "Affairs, was appointed Executive Director of the World Food Programme after confirmation by the WFP Executive "
  "Board, in a joint announcement by the UN Secretary-General and the FAO Director-General. He was nominated by "
  "President Donald Trump.",
  ["Agency: World Food Programme (WFP)", "Appointed 18 Sep 2026", "Earlier: USDA Undersecretary"],
  [fact("UN appoints Luke Lindberg as Executive Director of the World Food Programme (18 September 2026); earlier "
        "USDA Undersecretary for Trade and Foreign Agricultural Affairs", "a_wfp_gk")],
  why="FAO and IFAD have Directors-General/Presidents, and UNICEF was not involved; Lindberg heads the WFP.",
  current=ca("2026-09-18"))

G(T, IB, "Basic",
  "Ambassador Sidharto Reza Suryodipuro was elected President of the UN Human Rights Council for 2026, the first time "
  "his country has held the post. Which country does he represent?",
  ["Indonesia", "Malaysia", "Thailand", "Philippines"], "*",
  "UN Human Rights Council presidency",
  "On 8 January 2026 the Human Rights Council in Geneva confirmed Indonesia's ambassador Sidharto Reza Suryodipuro, "
  "the sole Asia-Pacific candidate, as its President for 2026. It is Indonesia's first Council presidency. Ecuador's "
  "Marcelo Vázquez Bermúdez was elected Vice-President.",
  ["Elected 8 Jan 2026", "President: Sidharto Reza Suryodipuro (Indonesia)", "First Indonesian presidency"],
  [fact("Indonesia's Sidharto Reza Suryodipuro confirmed as Human Rights Council President for 2026 on 8 January 2026; "
        "first Indonesian presidency", "a_hrc_un")],
  why="He is Indonesia's ambassador; Malaysia, Thailand and the Philippines did not hold the 2026 presidency.",
  current=ca("2026-01-08"))

G(T, BF, "Basic",
  "When the government reconstituted it on 16 October 2026, SCL Das, a former Secretary of the MSME Ministry, was "
  "named chairman of which body?",
  ["Financial Services Institutions Bureau (FSIB)", "Insurance Regulatory and Development Authority of India",
   "Pension Fund Regulatory and Development Authority", "National Bank for Financing Infrastructure and Development"],
  "*",
  "FSIB",
  "The Financial Services Institutions Bureau, which recommends candidates for top posts in public sector banks, "
  "financial institutions and public sector insurers, was reconstituted on 16 October 2026 with SCL Das as chairman "
  "for three years. FSIB replaced the Banks Board Bureau in 2022 and works under the Department of Financial "
  "Services.",
  ["Body: FSIB (successor of Banks Board Bureau, 2022)", "Reconstituted 16 Oct 2026", "Chairman: SCL Das"],
  [fact("FSIB reconstituted on 16 October 2026 with SCL Das, former MSME Secretary, as chairman; FSIB replaced the "
        "Banks Board Bureau in 2022", "a_fsib_gk")],
  why="SCL Das heads the FSIB, not IRDAI, PFRDA or NaBFID.",
  current=ca("2026-10-16"))

G(T, BF, "Basic",
  "Lavanya R. Mundayur, earlier the CMD of Agriculture Insurance Company of India, was appointed Chairman-cum-Managing "
  "Director of which public sector insurer in September 2026?",
  ["New India Assurance Company", "Life Insurance Corporation of India", "General Insurance Corporation of India (GIC Re)",
   "United India Insurance Company"], "*",
  "Heads of public sector insurers",
  "On 30 September 2026 the Central Government approved Lavanya R. Mundayur as CMD of The New India Assurance Company "
  "Ltd, until 31 May 2029. She had been CMD of Agriculture Insurance Company of India (AICIL).",
  ["Insurer: New India Assurance", "Approved 30 Sep 2026; term to 31 May 2029", "Earlier: CMD, AICIL"],
  [fact("Lavanya R Mundayur appointed CMD of New India Assurance until 31 May 2029; currently CMD of AICIL (report of "
        "30 Sep 2026)", "a_niacl_psu"),
   fact("NIACL stock exchange filing on CMD appointment, 30 Sep 2026", "a_niacl_nse")],
  why="LIC, GIC Re and United India Insurance were not the insurer concerned.",
  current=ca("2026-09-30"))

G(T, BF, "Basic",
  "Hitesh Rameshchandra Joshi, who had held the post on an interim basis since 1 October 2025, was appointed regular "
  "Chairman-cum-Managing Director of which company from 16 June 2026?",
  ["General Insurance Corporation of India (GIC Re)", "New India Assurance Company", "ECGC Limited",
   "Agriculture Insurance Company of India"], "*",
  "India's national reinsurer",
  "GIC Re, India's state-owned reinsurer, said the Ministry of Finance approved Hitesh Joshi's appointment as CMD with "
  "effect from 16 June 2026, until his superannuation on 30 September 2028. He had been an Executive Director and had "
  "held the CMD post on an interim basis from 1 October 2025.",
  ["Company: GIC Re", "Effective 16 Jun 2026", "Term to 30 Sep 2028"],
  [fact("Hitesh Joshi appointed GIC Re CMD effective 16 June 2026 until 30 September 2028; interim since 1 October 2025",
        "a_gic_rn")],
  why="Joshi heads GIC Re; the other companies have different heads.",
  current=ca("2026-06-16"))

G(T, BF, "Basic",
  "In February 2026 the RBI approved the re-appointment of Sanjay Agarwal as MD and CEO for three years from "
  "19 April 2026. Which bank does he lead?",
  ["AU Small Finance Bank", "Equitas Small Finance Bank", "Ujjivan Small Finance Bank", "Bandhan Bank"], "*",
  "Private and small finance bank heads",
  "AU Small Finance Bank received RBI approval (reported 12 February 2026) for the re-appointment of Sanjay Agarwal as "
  "MD and CEO for three years starting 19 April 2026, after board and shareholder approvals in late 2025.",
  ["Bank: AU Small Finance Bank", "Re-appointment: 3 years from 19 Apr 2026", "RBI nod reported 12 Feb 2026"],
  [fact("RBI approves Sanjay Agarwal's re-appointment as AU Small Finance Bank MD & CEO for three years starting 19 April "
        "2026", "a_au_psu")],
  why="Equitas, Ujjivan and Bandhan are led by other people; Agarwal leads AU Small Finance Bank.",
  current=ca("2026-04-19"))

G(T, BF, "Intermediate",
  "Sudhakar Malli, appointed an Executive Director of the RBI with effect from 1 October 2026, oversees which "
  "department?",
  ["Department of Supervision (Supervisory Assessment)", "Department of Payment and Settlement Systems",
   "Foreign Exchange Department", "Department of Statistics and Information Management"], "*",
  "RBI Executive Directors",
  "The RBI's press release of 2 October 2026 says Sudhakar Malli, earlier Chief General Manager-in-Charge of the "
  "Department of Supervision, became Executive Director from 1 October 2026 and will look after the Department of "
  "Supervision (Supervisory Assessment). He has about 25 years of experience in supervising banks, NBFCs and "
  "co-operative banks.",
  ["ED from 1 Oct 2026", "Portfolio: Department of Supervision (Supervisory Assessment)"],
  [fact("RBI appoints Sudhakar Malli as Executive Director effective 1 October 2026; he will oversee the Department of "
        "Supervision (Supervisory Assessment)", "a_malli_rbi")],
  why="Payment systems is under Gunveer Singh, foreign exchange under Monisha Chakraborty and statistics under Ravi "
      "Shankar.",
  current=ca("2026-10-01"))

G(T, BF, "Intermediate",
  "Ravi Shankar, a statistician appointed Executive Director of the RBI from 1 July 2026, oversees which department?",
  ["Department of Statistics and Information Management", "Department of Economic and Policy Research",
   "Department of Currency Management", "Department of Government and Bank Accounts"], "*",
  "RBI Executive Directors",
  "The RBI appointed Ravi Shankar as Executive Director with effect from 1 July 2026. He had been Adviser-in-Charge of "
  "the Department of Statistics and Information Management (DSIM) and continues to oversee DSIM as ED.",
  ["ED from 1 Jul 2026", "Earlier: Adviser-in-Charge, DSIM", "Portfolio: DSIM"],
  [fact("RBI appoints Ravi Shankar as Executive Director effective 1 July 2026; he will oversee the Department of "
        "Statistics and Information Management", "a_rshankar_rbi")],
  why="The RBI release names only DSIM as his portfolio.",
  current=ca("2026-07-01"))

G(T, BF, "Intermediate",
  "In June 2026 the Appointments Committee of the Cabinet approved Ravi Agrawal's re-appointment, on contract for "
  "six months until 31 December 2026, as chairman of which body?",
  ["Central Board of Direct Taxes (CBDT)", "Central Board of Indirect Taxes and Customs (CBIC)",
   "GST Appellate Tribunal", "Income Tax Appellate Tribunal"], "*",
  "Revenue boards",
  "Ravi Agrawal, an IRS officer due to retire on 30 June 2026, was re-appointed CBDT chairman on contract for six "
  "months, until 31 December 2026 or further orders. The ACC approval was reported on 30 June 2026.",
  ["Body: CBDT", "Re-appointment: six months, to 31 Dec 2026", "Approved by ACC (30 Jun 2026)"],
  [fact("Ravi Agrawal re-appointed CBDT chairman on contract basis for six months, till 31 December 2026; approved by "
        "the ACC (30 June 2026)", "a_cbdt_air")],
  why="He heads the CBDT, which administers direct taxes; CBIC and the tribunals have other heads.",
  current=ca("2026-06-30"))

GS(T, IB, "Advanced", "Monica Kathina Juma's UN appointment of March 2026",
   ["She succeeded Catherine Russell as Executive Director of the UN Office on Drugs and Crime (UNODC).",
    "She was also appointed Director-General of the UN Office at Vienna.",
    "Before this she was National Security Adviser to Kenya's President."],
   [False, True, True],
   "UNODC leadership",
   "On 6 March 2026 the UN Secretary-General appointed Monica Kathina Juma of Kenya as Executive Director of UNODC and "
   "Director-General of the UN Office at Vienna. She succeeded Ghada Fathi Waly of Egypt (Catherine Russell heads "
   "UNICEF). Juma had been Kenya's National Security Adviser since 2022.",
   [fact("Monica Juma appointed UNODC Executive Director and UNOV Director-General (6 March 2026), succeeding Ghada "
         "Fathi Waly; Kenya's National Security Adviser since 2022", "a_juma_star")],
   why="Statement 1 is wrong: her predecessor was Ghada Fathi Waly.",
   current=ca("2026-03-06"))

GS(T, IB, "Advanced", "Hyun Song Shin",
   ["He was appointed Governor of the Bank of Korea, as noted in a BIS statement of 20 April 2026.",
    "At the Bank for International Settlements, where he had worked since 2014, Hélène Rey is to succeed him from "
    "September 2026."],
   [True, True],
   "Bank of Korea and the BIS",
   "Hyun Song Shin, who joined the BIS in 2014 and led its research as head of the Monetary and Economic Department, "
   "was appointed Governor of the Bank of Korea. The BIS statement of 20 April 2026 said Hélène Rey would succeed him "
   "from September 2026, with Frank Smets as acting head in the interim.",
   [fact("BIS statement (20 April 2026) on the appointment of Hyun Song Shin as Governor of the Bank of Korea; joined BIS "
         "in 2014; Hélène Rey to succeed him from September 2026", "a_shin_mv")],
   why="Both statements are correct.",
   current=ca("2026-04-20"))

GS(T, IB, "Advanced", "the renewal of Volker Türk's term as UN High Commissioner for Human Rights",
   ["The UN General Assembly approved it on 24 July 2026 by a recorded vote of 144 in favour and 10 against.",
    "The new four-year term runs from 12 October 2026 to 11 October 2030.",
    "Türk is a German diplomat who had earlier headed UNHCR."],
   [True, True, False],
   "UN human rights chief",
   "On 24 July 2026 the General Assembly renewed Volker Türk's mandate by 144 votes to 10, with 13 abstentions, "
   "rejecting a US request to postpone and a Russian proposal to extend him only to the end of 2026. His second term "
   "runs from 12 October 2026 to 11 October 2030. Türk is an Austrian jurist.",
   [fact("UNGA voted on 24 July 2026: 144 in favour, 10 against, 13 abstentions; term 12 October 2026 to 11 October "
         "2030", "a_turk_kas"),
    fact("Austrian jurist Volker Türk's term extended; US and Russia opposed", "a_turk_aaw")],
   why="Statement 3 is wrong: Türk is Austrian.",
   current=ca("2026-07-24"))

GS(T, IB, "Advanced", "the leadership of the UN Industrial Development Organization (UNIDO)",
   ["Gerd Müller was reappointed Director General at the General Conference held in Vienna in November 2025.",
    "His new term as Director General is his second, and runs for four years."],
   [False, True],
   "UNIDO Director General",
   "The 21st session of UNIDO's General Conference, held in Riyadh, Saudi Arabia, from 23 November 2025, reappointed "
   "Gerd Müller as Director General for a second four-year term. UNIDO's headquarters is in Vienna, but this "
   "conference met in Riyadh.",
   [fact("Gerd Müller re-elected for a second four-year term as UNIDO Director-General at the summit opened in Riyadh "
         "(23 Nov 2025)", "a_unido_aa"),
    fact("UNIDO: Gerd Müller appointed for a second term as Director General, Riyadh, 23 November 2025", "a_unido_un")],
   why="Statement 1 is wrong: the conference was held in Riyadh, not Vienna.",
   current=ca("2025-11-23"))

GS(T, BF, "Advanced", "Monisha Chakraborty",
   ["She became an Executive Director of the RBI on 3 August 2026, in charge of the Foreign Exchange Department and "
    "the Financial Markets Regulation Department.",
    "Before her promotion she was the RBI's Regional Director for Maharashtra."],
   [True, False],
   "RBI Executive Directors",
   "The RBI appointed Monisha Chakraborty as Executive Director from 3 August 2026 to oversee the Foreign Exchange "
   "Department and the Financial Markets Regulation Department. She was earlier Chief General Manager-in-Charge of the "
   "Department of Supervision (it was Suman Ray who had been Regional Director, Maharashtra).",
   [fact("RBI appoints Monisha Chakraborty as Executive Director effective 3 August 2026; earlier CGM-in-Charge, "
         "Department of Supervision; will oversee FED and FMRD", "a_monisha_rbi")],
   why="Statement 2 is wrong: she came from the Department of Supervision.",
   current=ca("2026-08-03"))

GS(T, BF, "Advanced", "K. Rajaraman, Chairperson of the International Financial Services Centres Authority (IFSCA)",
   ["In July 2026 his tenure was extended beyond 31 July 2026, until he turns 65 in October 2028 or until further "
    "orders.",
    "Before joining IFSCA he was Revenue Secretary.",
    "He is a retired 1989-batch IAS officer of the Tamil Nadu cadre."],
   [True, False, True],
   "IFSCA",
   "The Department of Economic Affairs extended Rajaraman's tenure as IFSCA Chairperson beyond 31 July 2026 until he "
   "attains 65 in October 2028. He took charge on 1 August 2023; earlier he was Secretary, Department of "
   "Telecommunications. He is a 1989-batch IAS officer of the Tamil Nadu cadre.",
   [fact("Rajaraman to serve until he attains 65 in October 2028; extension beyond 31 July 2026; earlier Secretary, DoT; "
         "1989-batch IAS, Tamil Nadu cadre (article of 31 July 2026)", "a_ifsca_sec")],
   why="Statement 2 is wrong: he was Telecom Secretary, not Revenue Secretary.",
   current=ca("2026-07-31"))

GS(T, BF, "Advanced", "the leadership of UCO Bank in 2026",
   ["Executive Director Rajendra Kumar Saboo was given a regular three-year appointment as MD and CEO from 1 June 2026.",
    "The MD and CEO post fell vacant on 1 June 2026 after Ashwani Kumar's tenure ended on 31 May 2026."],
   [False, True],
   "Public sector bank heads",
   "Ashwani Kumar's tenure as MD and CEO of UCO Bank ended on 31 May 2026. The Department of Financial Services gave "
   "Executive Director Rajendra Kumar Saboo additional charge of MD and CEO, initially until 31 August 2026 or until a "
   "regular appointment, so his was an interim charge, not a regular appointment.",
   [fact("UCO Bank MD & CEO post vacant from 1 June 2026 after Ashwani Kumar's tenure ended 31 May 2026; ED Rajendra "
         "Saboo gets additional charge until 31 August 2026", "a_uco_hb")],
   why="Statement 1 is wrong: Saboo holds only additional (interim) charge.",
   current=ca("2026-06-01"))

# ====================================================================== National and International Organizations (5 / 1 / 4)
T = "National and International Organizations"
HQ, MEM = "Headquarters and heads", "Membership"

G(T, HQ, "Basic",
  "The UN Economic and Social Commission for Asia and the Pacific (ESCAP), founded in 1947 as ECAFE, is headquartered "
  "in which city?",
  ["Bangkok", "Manila", "Jakarta", "Kuala Lumpur"], "*",
  "UN regional commissions",
  "ESCAP began in 1947 as the Economic Commission for Asia and the Far East (ECAFE) and was renamed in 1974. It is "
  "headquartered in Bangkok, Thailand.",
  ["ESCAP (ECAFE until 1974)", "HQ: Bangkok"],
  [fact("ESCAP headquartered in Bangkok; founded 1947 as ECAFE; renamed 1974", "a_escap_wiki")],
  why="Manila hosts the ADB, Jakarta the ASEAN Secretariat; Kuala Lumpur is not ESCAP's seat.")

G(T, HQ, "Basic",
  "The secretariat of the Pacific Islands Forum, founded in 1971 as the South Pacific Forum, is located in which city?",
  ["Suva", "Wellington", "Port Moresby", "Apia"], "*",
  "Regional organisations",
  "The Pacific Islands Forum, an 18-member regional body founded in 1971 as the South Pacific Forum, has its "
  "secretariat in Suva, Fiji.",
  ["Founded 1971 (South Pacific Forum)", "Secretariat: Suva, Fiji", "18 members"],
  [fact("Pacific Islands Forum secretariat in Suva, Fiji; founded 1971 as South Pacific Forum; 18 members",
        "a_pif_wiki")],
  why="Wellington, Port Moresby and Apia are capitals of member states, not the secretariat seat.")

G(T, HQ, "Basic",
  "The Coalition for Disaster Resilient Infrastructure (CDRI), launched by India at the UN Climate Action Summit in "
  "2019, has its headquarters in which city?",
  ["New Delhi", "Geneva", "Gurugram", "Bengaluru"], "*",
  "India-led global initiatives",
  "CDRI was launched on 23 September 2019 at the UN Climate Action Summit in New York, on a proposal first made by "
  "Prime Minister Modi in 2016. Its headquarters is in New Delhi; the interim secretariat was set up at the National "
  "Disaster Management Authority.",
  ["Launched 23 Sep 2019, New York", "HQ: New Delhi"],
  [fact("CDRI launched 23 September 2019 at the UN Climate Action Summit; headquarters New Delhi", "a_cdri_wiki")],
  why="Gurugram hosts the International Solar Alliance, not CDRI; Geneva and Bengaluru are wrong.")

G(T, HQ, "Basic",
  "The Organisation of Islamic Cooperation (OIC), founded in 1969 and having 57 member states, is headquartered in "
  "which city?",
  ["Jeddah", "Riyadh", "Cairo", "Doha"], "*",
  "Headquarters of international organisations",
  "The OIC, set up in 1969 and renamed from the Organisation of the Islamic Conference in 2011, has 57 member states "
  "and its headquarters in Jeddah, Saudi Arabia. India is not a member.",
  ["OIC: founded 1969, 57 members", "HQ: Jeddah"],
  [fact("OIC headquarters Jeddah; founded 1969; 57 member states; India not a member", "a_oic_wiki")],
  why="Riyadh hosts the GCC secretariat and Cairo the Arab League; Doha is not the OIC seat.")

G(T, HQ, "Basic",
  "The World Food Programme, the food-assistance arm of the United Nations, is headquartered in which city?",
  ["Rome", "Geneva", "New York", "Nairobi"], "*",
  "UN agencies' headquarters",
  "The WFP is headquartered in Rome, Italy, like the FAO and IFAD, the other two Rome-based UN food agencies.",
  ["WFP HQ: Rome"],
  [fact("The World Food Programme is the food-assistance arm of the UN, headquartered in Rome, Italy", "a_wfp_gk")],
  why="Geneva, New York and Nairobi host other UN bodies.")

G(T, MEM, "Intermediate",
  "In February 2026 Colombia was accepted as a full member of which organisation, becoming its 33rd member?",
  ["International Energy Agency", "OECD", "OPEC", "International Solar Alliance"], "*",
  "Membership changes",
  "Colombia's Energy Ministry announced on 19 February 2026 that the country had been accepted as a full member of "
  "the International Energy Agency, its 33rd member, after a process begun in 2021.",
  ["Colombia joined the IEA (announced 19 Feb 2026)", "33rd IEA member"],
  [fact("Colombia accepted as a full member of the IEA, its 33rd member; announced 19 February 2026", "a_iea_dd")],
  why="Colombia's 2026 accession was to the IEA; it is not an OPEC member, and the ISA has over 100 members.",
  current=ca("2026-02-19"))

GS(T, MEM, "Advanced", "the Eurasian Economic Union (EAEU)",
   ["The treaty establishing it was signed in Astana on 29 May 2014 and came into force on 1 January 2015.",
    "The Eurasian Economic Commission, its executive body, is headquartered in Minsk.",
    "Armenia and Kyrgyzstan joined it in 2015."],
   [True, False, True],
   "Eurasian Economic Union",
   "The EAEU Treaty was signed in Astana on 29 May 2014 by Belarus, Kazakhstan and Russia and came into force on "
   "1 January 2015. Armenia and Kyrgyzstan joined in 2015, giving five members. The Eurasian Economic Commission sits "
   "in Moscow; the EAEU Court is in Minsk.",
   [fact("EAEU Treaty signed 29 May 2014 in Astana, in force 1 January 2015; Armenia (2 Jan 2015) and Kyrgyzstan "
         "(Aug 2015) joined; Commission HQ Moscow; Court in Minsk", "a_eaeu_wiki")],
   why="Statement 2 is wrong: the Commission is in Moscow.")

GS(T, MEM, "Advanced", "the Indian Ocean Rim Association (IORA)",
   ["Its secretariat is at Ebene, Mauritius.",
    "Pakistan is one of its member states."],
   [True, False],
   "IORA",
   "IORA, whose charter was adopted in 1997, has 23 member states and its secretariat at Ebene, Mauritius. India, a "
   "founding member, currently chairs it; Pakistan is not a member.",
   [fact("IORA secretariat in Ebene, Mauritius; 23 member states; India chair; Pakistan kept out of membership",
         "a_iora_wiki")],
   why="Statement 2 is wrong: Pakistan is not an IORA member.")

GS(T, MEM, "Advanced", "the North Atlantic Treaty Organization (NATO)",
   ["It has 32 member states.",
    "Its headquarters is in Brussels.",
    "The North Atlantic Treaty was signed on 4 April 1949."],
   [True, True, True],
   "NATO",
   "NATO was founded by the North Atlantic Treaty of 4 April 1949. With Finland and Sweden joining after "
   "Russia's 2022 invasion of Ukraine, it has 32 members. Its headquarters is in Brussels.",
   [fact("NATO: 32 member states; headquarters Brussels; North Atlantic Treaty signed 4 April 1949", "a_nato_wiki")],
   why="All three statements are correct.")

GS(T, MEM, "Advanced", "Asia-Pacific Economic Cooperation (APEC)",
   ["It has 21 member economies.",
    "Its secretariat is in Singapore.",
    "India became a full member economy in 2025."],
   [True, True, False],
   "APEC",
   "APEC was set up in 1989 at a meeting in Canberra and now has 21 member economies. Its secretariat is in "
   "Singapore. India is not an APEC member.",
   [fact("APEC: established 1989 (Canberra); 21 member economies; secretariat Singapore; India not a member",
         "a_apec_wiki")],
   why="Statement 3 is wrong: India is not an APEC member.")


# ###################################################################### part: mine
U.update({
    # ---------------- Schemes
    "g_vistaar_ag": ("https://agrospectrumindia.com/news/158/33355/union-budget-2026-bharat-vistaar-and-she-mart-empower-"
                     "farmers-and-rural-entrepreneurs.html", OPENED),
    "g_budget_adda": ("https://currentaffairs.adda247.com/union-budget-2026-list-of-new-and-existing-schemes-initiatives",
                      OPENED),
    "g_ssy_air": ("https://newsonair.gov.in/pradhan-mantri-surya-sarovar-yojana-to-use-existing-reservoirs-canals-and-"
                  "industrial-ponds-mib/", OPENED),
    "g_ssy_ener": ("https://www.energetica-india.net/news/cabinet-approves-inr-5070-cr-pm-surya-sarovar-yojana-for-5-gw-"
                   "floating-solar-with-10-gwh-ess", OPENED),
    "g_bps_bt": ("https://www.businesstoday.in/union-budget/news/story/union-budget-2026-bio-pharma-shakti-gets-rs-10000-"
                 "crore-over-five-years-fm-sitharamans-big-push-513892-2026-02-01", OPENED),
    "g_coal_an": ("https://newsable.asianetnews.com/amp/business/india-approves-rs-37500-crore-coal-gasification-"
                  "promotion-scheme-articleshow-cdym1k4", OPENED),
    "g_bhavya_uni": ("https://test.uniindia.com/news/india/cabinet-bhavya-rasayan-scheme-chemical-parks/3920391.html",
                     OPENED),
    "g_cmps_gk": ("https://www.gktoday.in/cabinet-approves-%e2%82%b910000-crore-shipping-container-manufacturing-"
                  "programme/", OPENED),
    "g_cab_ssj": ("https://www.sahisarkarijobs.in/current-affairs/28-october-2026/", OPENED),
    "g_kisgms_dd": ("https://ddindia.co.in/2026/10/cabinet-approves-rs-1856-67-crore-khelo-india-sports-goods-"
                    "manufacturing-scheme-to-boost-sports-manufacturing-ecosystem/", OPENED),
    "g_kisgms_dp": ("https://dailypioneer.com/amp/story/india/cabinet-approves-khelo-india-sports-goods-manufacturing-"
                    "scheme-with-outlay-of-over-rs-1800-crore", OPENED),
    "g_vgsy_sw": ("https://swarajyamag.com/infrastructure/union-cabinet-approves-rs-7395-crore-pm-viksit-gram-swaraj-"
                  "yojana-to-strengthen-panchayati-raj-institutions-across-india", OPENED),
    "g_ucf_bt": ("https://www.businesstoday.in/india/story/rs1-lakh-crore-boost-cabinet-approves-urban-challenge-fund-to-"
                 "finance-next-gen-cities-check-details-516167-2026-02-14", OPENED),
    "g_ucf_trib": ("https://www.tribuneindia.com/news/business/cabinet-approves-rs-1-lakh-crore-fund-to-overhaul-indian-"
                   "cities/", OPENED),
    "g_cotton_ao": ("https://www.angelone.in/news/economy/cabinet-approves-5-659-crore-mission-for-cotton-productivity-"
                    "till-2030-31", OPENED),
    "g_cotton_air": ("https://newsonair.gov.in/centre-approves-%e2%82%b95600-crore-cotton-productivity-mission-clears-two-"
                     "semiconductor-units-in-gujarat/", OPENED),
    "g_sme_ians": ("https://ianslive.in/smes-get-big-push-with-rs-10000-crore-growth-fund-in-budget-2026-27--"
                   "20260201143012", OPENED),
    "g_ccus_dte": ("https://www.downtoearth.org.in/climate-change/budget-2026-27-sets-aside-rs-20000-crore-to-accelerate-"
                   "carbon-capture-in-heavy-industry", OPENED),
    # ---------------- Static
    "g_dram_wiki": ("https://en.wikipedia.org/wiki/Armenian_dram", OPENED),
    "g_mnt_wiki": ("https://en.wikipedia.org/wiki/Mongolian_t%C3%B6gr%C3%B6g", OPENED),
    "g_svk_wiki": ("https://en.wikipedia.org/wiki/Slovakia", OPENED),
    "g_atg_wiki": ("https://en.wikipedia.org/wiki/Antigua_and_Barbuda", OPENED),
    "g_kanha_wiki": ("https://en.wikipedia.org/wiki/Kanha_Tiger_Reserve", OPENED),
    "g_rihand_wiki": ("https://en.wikipedia.org/wiki/Rihand_Dam", OPENED),
    "g_eravi_wiki": ("https://en.wikipedia.org/wiki/Eravikulam_National_Park", OPENED),
    "g_andhra_wiki": ("https://en.wikipedia.org/wiki/Andhra_State", OPENED),
    "g_har_wiki": ("https://en.wikipedia.org/wiki/Haryana", OPENED),
})

# ====================================================================== Government Schemes (2 / 11 / 2)
T = "Government Schemes"
CS, SL = "Central schemes", "Scheme launches and changes"

G(T, SL, "Basic",
  "Bharat-VISTAAR, announced in the Union Budget 2026-27, is meant to serve which group?",
  ["Farmers, through an AI-based agricultural advisory system", "MSMEs, through a credit guarantee platform",
   "Students, through a national scholarship portal", "Exporters, through a single-window trade platform"], "*",
  "Bharat-VISTAAR",
  "The Union Budget 2026-27, presented on 1 February 2026, announced Bharat-VISTAAR, which couples AI-driven systems "
  "with the ICAR package of practices to give farmers advisory support, aiming at higher farm productivity and lower "
  "risk.",
  ["Announced: Union Budget 2026-27 (1 Feb 2026)", "Users: farmers", "Tool: AI-based advisory linked to ICAR practices"],
  [fact("Budget 2026 launches Bharat Vistaar: AI-driven systems coupled with the ICAR package to enhance farm "
        "productivity; published 1 Feb 2026", "g_vistaar_ag"),
   fact("Bharat-VISTAAR: multilingual AI-based farmer advisory system announced in Union Budget 2026-27",
        "g_budget_adda")],
  why="It is a farm advisory tool, not a credit, scholarship or trade platform.",
  current=ca("2026-02-01"))

G(T, SL, "Basic",
  "The Pradhan Mantri Surya Sarovar Yojana (PM-SSY), approved by the Union Cabinet on 31 July 2026, supports which "
  "type of projects?",
  ["Floating solar PV projects with energy storage", "Rooftop solar on residential houses",
   "Solar-powered irrigation pumps for farmers", "Solar parks on wasteland in desert districts"], "*",
  "PM Surya Sarovar Yojana",
  "PM-SSY (outlay ₹5,070 crore) supports floating solar photovoltaic projects with co-located energy storage, built "
  "on existing reservoirs, canals and industrial ponds, so no additional land has to be acquired.",
  ["Scheme: PM-SSY, ₹5,070 crore", "Projects: floating solar PV with storage", "Sites: reservoirs, canals, ponds"],
  [fact("Union Cabinet approved PM-SSY for floating solar PV projects with energy storage; uses existing reservoirs, "
        "canals and industrial ponds; no additional land acquisition (31 July 2026)", "g_ssy_air"),
   fact("PM Surya Sarovar Yojana: INR 5,070 crore for 5 GW floating solar with storage", "g_ssy_ener")],
  why="Rooftop solar is PM-Surya Ghar, solar pumps are PM-KUSUM; PM-SSY is for floating solar on water bodies.",
  current=ca("2026-07-31"))

G(T, SL, "Intermediate",
  "SHE-Marts, announced in the Union Budget 2026-27 as community-owned retail outlets for rural women's enterprises, "
  "build on the success of which programme?",
  ["Lakhpati Didi", "Stand-Up India", "PM Vishwakarma", "Mahila Samman Savings Certificate"], "*",
  "SHE-Marts",
  "The Budget of 1 February 2026 announced SHE-Marts to help rural women move into enterprise ownership, building on "
  "the Lakhpati Didi programme of self-help-group women, with financing instruments and working capital support.",
  ["Initiative: SHE-Marts (Budget 2026-27)", "Builds on: Lakhpati Didi"],
  [fact("Building on the success of Lakhpati Didi, the Budget launches SHE-MART (1 Feb 2026)", "g_vistaar_ag"),
   fact("SHE-Marts help rural women move into enterprise ownership (Budget 2026-27)", "g_budget_adda")],
  why="Stand-Up India, PM Vishwakarma and the Mahila Samman certificate are separate schemes.",
  current=ca("2026-02-01"))

G(T, SL, "Intermediate",
  "Biopharma SHAKTI, announced in the Union Budget 2026-27 to make India a hub for biologics manufacturing, has what "
  "proposed outlay?",
  ["₹10,000 crore over five years", "₹5,000 crore over three years", "₹20,000 crore over five years",
   "₹40,000 crore over six years"], "*",
  "Biopharma SHAKTI",
  "Finance Minister Nirmala Sitharaman proposed Biopharma SHAKTI with ₹10,000 crore for the next five years on "
  "1 February 2026. ₹20,000 crore over five years is the Budget's CCUS outlay.",
  ["Biopharma SHAKTI: ₹10,000 crore", "Period: five years"],
  [fact("I propose Bio Pharma Shakti with a proposal of Rs 10,000 crore for next 5 years (1 Feb 2026)", "g_bps_bt"),
   fact("Biopharma SHAKTI: global hub for biologics and biosimilars, ₹10,000 crore over five years", "g_budget_adda")],
  why="₹20,000 crore is the CCUS outlay; the other figures are not Biopharma SHAKTI's.",
  current=ca("2026-02-01"))

G(T, SL, "Intermediate",
  "The Union Budget 2026-27 announced an outlay of ₹20,000 crore over five years for which of the following?",
  ["Carbon capture, utilisation and storage (CCUS) technologies", "Biopharma SHAKTI",
   "SME Growth Fund", "Self-Reliant India Fund top-up"], "*",
  "CCUS outlay",
  "The Budget of 1 February 2026 proposed ₹20,000 crore over five years for CCUS in hard-to-abate sectors (power, "
  "steel, cement, refineries and chemicals). Biopharma SHAKTI and the SME Growth Fund got ₹10,000 crore each, and the "
  "Self-Reliant India Fund a ₹2,000 crore top-up.",
  ["CCUS: ₹20,000 crore / 5 years", "Biopharma SHAKTI: ₹10,000 crore", "SME Growth Fund: ₹10,000 crore",
   "SRI Fund top-up: ₹2,000 crore"],
  [fact("Budget 2026-27: outlay of Rs 20,000 crore over the next five years for CCUS; power, steel, cement, refineries "
        "and chemicals", "g_ccus_dte"),
   fact("SME Growth Fund Rs 10,000 crore; Self-Reliant India Fund top-up Rs 2,000 crore (1 Feb 2026)", "g_sme_ians")],
  why="The other three items received ₹10,000 crore, ₹10,000 crore and ₹2,000 crore respectively.",
  current=ca("2026-02-01"))

G(T, SL, "Intermediate",
  "The ₹10,000 crore SME Growth Fund announced in the Union Budget 2026-27 is meant mainly to:",
  ["Create future 'Champion' MSMEs by incentivising enterprises on select criteria",
   "Write off overdue loans of micro enterprises",
   "Fund MSME stalls at international trade fairs",
   "Give interest-free loans to first-time women entrepreneurs"], "*",
  "SME Growth Fund",
  "On 1 February 2026 the Budget proposed a dedicated ₹10,000 crore SME Growth Fund to create future champions by "
  "incentivising enterprises based on select criteria, plus a ₹2,000 crore top-up for the Self-Reliant India Fund.",
  ["Fund: SME Growth Fund, ₹10,000 crore", "Aim: create Champion MSMEs (equity support)"],
  [fact("SME Growth Fund Rs 10,000 crore to create future champions by incentivising enterprises based on select "
        "criteria", "g_sme_ians"),
   fact("SME Growth Fund: creates future Champion MSMEs; ₹10,000 crore", "g_budget_adda")],
  why="The fund is equity support for growth, not loan write-offs, trade-fair stalls or women-only loans.",
  current=ca("2026-02-01"))

G(T, SL, "Intermediate",
  "Under the Scheme for Promotion of Surface Coal/Lignite Gasification Projects, approved by the Union Cabinet on "
  "13 May 2026 with an outlay of ₹37,500 crore, what is the national goal for coal gasification by 2030?",
  ["100 million tonnes", "50 million tonnes", "75 million tonnes", "150 million tonnes"], "*",
  "Coal gasification scheme",
  "The ₹37,500 crore scheme aims to gasify about 75 million tonnes of coal through supported projects and supports "
  "the national goal of gasifying 100 million tonnes of coal by 2030. Incentives are capped at ₹5,000 crore per "
  "project.",
  ["Outlay: ₹37,500 crore", "Under the scheme: ~75 MT", "National goal: 100 MT by 2030"],
  [fact("Cabinet approved Rs 37,500 crore Scheme for Promotion of Surface Coal/Lignite Gasification Projects on "
        "13 May 2026; ~75 MT under the scheme; national goal 100 MT by 2030; cap Rs 5,000 crore per project",
        "g_coal_an")],
  why="75 MT is what the scheme itself is expected to gasify; the national 2030 goal is 100 MT.",
  current=ca("2026-05-13"))

G(T, SL, "Intermediate",
  "The Bharat Audyogik Vikas Yojana Rasayan (BHAVYA Rasayan) scheme, approved by the Union Cabinet on 24 July 2026 "
  "with an outlay of ₹3,030 crore, provides for how many dedicated chemical parks?",
  ["Three", "Five", "Seven", "Ten"], "*",
  "BHAVYA Rasayan",
  "BHAVYA Rasayan, announced in the Union Budget 2026-27, will set up three dedicated chemical parks over FY 2026-27 "
  "to FY 2030-31; ₹3,000 crore of the ₹3,030 crore is for common infrastructure and utilities in the parks.",
  ["Scheme: BHAVYA Rasayan, ₹3,030 crore", "Parks: three", "Period: FY 2026-27 to 2030-31"],
  [fact("Cabinet approved BHAVYA Rasayan on 24 July 2026: Rs 3,030 crore, three dedicated Chemical Parks, FY 2026-27 "
        "to FY 2030-31", "g_bhavya_uni"),
   fact("Chemical Parks Scheme: three parks selected through challenge mode (Budget 2026-27)", "g_budget_adda")],
  why="The scheme provides for three parks.",
  current=ca("2026-07-24"))

G(T, SL, "Intermediate",
  "The Container Manufacturing Promotion Scheme, approved by the Union Cabinet on 28 October 2026 with an outlay of "
  "₹10,000 crore, targets raising India's annual container manufacturing capacity to about how much?",
  ["7.5 lakh TEUs", "75,000 TEUs", "25 lakh TEUs", "1.5 lakh TEUs"], "*",
  "Container Manufacturing Promotion Scheme",
  "The scheme, with outlay up to FY 2039-40, targets a roughly ten-fold rise in annual domestic container "
  "manufacturing capacity to 7.5 lakh TEUs, through interest subvention (3% a year), operational expenditure "
  "assistance and support for testing and certification.",
  ["Outlay: ₹10,000 crore (to FY 2039-40)", "Target: ~10x, to 7.5 lakh TEUs"],
  [fact("Container Manufacturing Promotion Scheme, Rs 10,000 crore, approved 28 Oct 2026; target 750,000 TEUs a year; "
        "3% interest subvention", "g_cmps_gk"),
   fact("It targets increasing annual domestic capacity around ten-fold to 7.5 lakh TEUs", "g_cab_ssj")],
  why="75,000 TEUs is roughly the present level implied by a ten-fold rise; the other figures are not the target.",
  current=ca("2026-10-28"))

G(T, SL, "Intermediate",
  "What is the outlay of the Khelo India Sports Goods Manufacturing Scheme approved by the Union Cabinet on "
  "28 October 2026 for the period 2026 to 2033-34?",
  ["₹1,856.67 crore", "₹36,441 crore", "₹3,030 crore", "₹7,395.55 crore"], "*",
  "Sports goods manufacturing scheme",
  "The scheme, announced in the Union Budget 2026-27, has an outlay of ₹1,856.67 crore, including ₹1,130 crore for "
  "anchor investment and turnover-linked support and ₹105 crore for certification by international sports "
  "federations, along with dedicated Sports Goods Manufacturing Zones.",
  ["Outlay: ₹1,856.67 crore", "Period: 2026 to 2033-34", "Approved: 28 Oct 2026"],
  [fact("Union Cabinet on Wednesday approved the Khelo India Sports Goods Manufacturing Scheme with outlay of "
        "₹1,856.67 crore for 2026 to 2033-34 (28 Oct 2026)", "g_kisgms_dd"),
   fact("Khelo India Sports Goods Manufacturing Scheme, Rs 1,856.67 crore", "g_kisgms_dp")],
  why="₹36,441 crore is the expanded Khelo India Scheme, ₹3,030 crore BHAVYA Rasayan and ₹7,395.55 crore PM Viksit "
      "Gram Swaraj Yojana.",
  current=ca("2026-10-28"))

G(T, SL, "Intermediate",
  "The Pradhan Mantri Viksit Gram Swaraj Yojana, approved by the Union Cabinet on 28 October 2026 as a Centrally "
  "Sponsored Scheme with an outlay of about ₹7,395 crore, focuses on which institutions?",
  ["Panchayats and other rural local bodies", "Urban local bodies in million-plus cities",
   "Primary agricultural credit societies", "Regional Rural Banks"], "*",
  "PM Viksit Gram Swaraj Yojana",
  "The scheme (2026-27 to 2030-31) covers more than 2.55 lakh rural local bodies and traditional bodies, with capacity "
  "building of elected representatives and support for Gram Panchayat Development Plans.",
  ["Outlay: ~₹7,395 crore (CSS)", "Covers: 2.55 lakh+ rural local bodies", "Period: 2026-27 to 2030-31"],
  [fact("Cabinet approved PM Viksit Gram Swaraj Yojana as a Centrally Sponsored Scheme, Rs 7,395 crore, 2026-27 to "
        "2030-31, covering more than 2.55 lakh rural local bodies (28 Oct 2026)", "g_vgsy_sw"),
   fact("Centre Rs 4,869.48 crore, State Rs 2,526.07 crore; Gram Panchayat Development Plans", "g_cab_ssj")],
  why="It targets panchayats, not urban bodies, PACS or RRBs.",
  current=ca("2026-10-28"))

G(T, SL, "Intermediate",
  "Under the Urban Challenge Fund approved by the Union Cabinet in February 2026, what share of a project's cost does "
  "the Centre provide?",
  ["25%", "50%", "60%", "75%"], "*",
  "Urban Challenge Fund",
  "The ₹1 lakh crore Urban Challenge Fund (approved 14 February 2026) funds 25% of project cost; cities must raise at "
  "least 50% from market sources such as municipal bonds, bank loans and PPPs, and the rest can come from states or "
  "city bodies.",
  ["Centre: 25%", "Market sources: at least 50%", "State/ULB: remainder"],
  [fact("Urban Challenge Fund: Centre's share 25% of project cost; cities must mobilise at least 50% from market "
        "sources (14 Feb 2026)", "g_ucf_bt"),
   fact("Centre funds 25 per cent; cities raise at least 50 per cent from market sources", "g_ucf_trib")],
  why="50% is the minimum market-raised share, not the Centre's share.",
  current=ca("2026-02-14"))

G(T, SL, "Intermediate",
  "The Mission for Cotton Productivity, approved by the Union Cabinet on 5 May 2026 with an outlay of ₹5,659.22 "
  "crore, aims to raise cotton production to how much by 2030-31?",
  ["498 lakh bales", "350 lakh bales", "755 lakh bales", "250 lakh bales"], "*",
  "Mission for Cotton Productivity",
  "The mission (2026-27 to 2030-31) targets 498 lakh bales of cotton and a rise in lint productivity from 440 to "
  "755 kg per hectare, through high-yielding, pest-resistant seed varieties and modern practices.",
  ["Outlay: ₹5,659.22 crore", "Target: 498 lakh bales by 2030-31", "Lint yield: 440 to 755 kg/ha"],
  [fact("Cabinet approved Mission for Cotton Productivity, ₹5,659.22 crore, 2026-27 to 2030-31; 498 lakh bales by "
        "2031; lint yield 440 to 755 kg/ha", "g_cotton_ao"),
   fact("Mission for Cotton Productivity, Kapas Kanti; 498 lakh bales by 2030-31 (5 May 2026)", "g_cotton_air")],
  why="755 is the target lint yield in kg/ha; the other figures are not the mission's target.",
  current=ca("2026-05-05"))

GS(T, SL, "Advanced", "the Urban Challenge Fund approved by the Union Cabinet in February 2026",
   ["It provides central assistance of ₹4 lakh crore over five years.",
    "Cities must raise at least 50% of project cost from market sources such as municipal bonds, bank loans and PPPs.",
    "A ₹5,000 crore corpus provides credit guarantees to help smaller and north-eastern/hilly urban local bodies get "
    "first-time access to market finance."],
   [False, True, True],
   "Urban Challenge Fund",
   "The Fund gives ₹1 lakh crore of central assistance, expected to mobilise about ₹4 lakh crore of total urban "
   "investment over five years. The Centre funds 25% of project cost, cities raise at least 50% from markets, and a "
   "₹5,000 crore guarantee corpus helps smaller and north-eastern/hilly ULBs.",
   [fact("₹1 lakh crore central assistance; ₹4 lakh crore total investment; at least 50% from market sources; ₹5,000 "
         "crore guarantee scheme for smaller municipalities (14 Feb 2026)", "g_ucf_bt"),
    fact("Rs 5,000 crore corpus as credit guarantee to facilitate first-time access to market finance for NE and hilly "
         "states and smaller ULBs", "g_ucf_trib")],
   why="Statement 1 is wrong: central assistance is ₹1 lakh crore; ₹4 lakh crore is the total investment expected.",
   current=ca("2026-02-14"))

GS(T, SL, "Advanced", "the Pradhan Mantri Surya Sarovar Yojana (PM-SSY)",
   ["It has a total outlay of ₹5,070 crore.",
    "Projects can be sanctioned up to FY 2035-36.",
    "Eligible projects get Central Financial Assistance of ₹1 crore per MW after successful commissioning."],
   [True, False, True],
   "PM-SSY",
   "PM-SSY (approved 31 July 2026) has an outlay of ₹5,070 crore for about 5,000 MW of floating solar with at least two "
   "hours of storage (10,000 MWh). Projects are sanctioned during FY 2026-27 to FY 2030-31, with disbursement up to "
   "FY 2032-33, and get CFA of ₹1 crore per MW after commissioning.",
   [fact("PM-SSY: INR 5,070 crore; CFA INR 1 crore/MW after commissioning; sanctioned FY 2026-27 to FY 2030-31, "
         "disbursement to FY 2032-33; 5,000 MW, 10,000 MWh", "g_ssy_ener"),
    fact("Union Cabinet approved PM-SSY, ₹5,070 crore (31 July 2026)", "g_ssy_air")],
   why="Statement 2 is wrong: sanctions run only from FY 2026-27 to FY 2030-31.",
   current=ca("2026-07-31"))

# ====================================================================== Static Awareness (0 / 9 / 0)
T = "Static Awareness"
CC, NP, SF = "Capitals and currencies", "National parks and dams", "Indian states facts"

G(T, CC, "Intermediate",
  "Yerevan hosted the biodiversity COP17 in 2026. The dram, issued by its central bank, is the currency of which "
  "country?",
  ["Armenia", "Azerbaijan", "Georgia", "Kazakhstan"], "*",
  "Armenian dram",
  "The dram, introduced in 1993 to replace the Soviet rouble, is Armenia's currency, issued by the Central Bank of "
  "Armenia. Azerbaijan uses the manat, Georgia the lari and Kazakhstan the tenge.",
  ["Dram: Armenia (since 1993)", "Issuer: Central Bank of Armenia"],
  [fact("Armenian dram, issued by the Central Bank of Armenia, introduced 1993", "g_dram_wiki")],
  why="Azerbaijan (manat), Georgia (lari) and Kazakhstan (tenge) have other currencies.")

G(T, CC, "Intermediate",
  "The tögrög (tugrik) is the currency of which country?",
  ["Mongolia", "Kyrgyzstan", "Uzbekistan", "Turkmenistan"], "*",
  "Mongolian tögrög",
  "The tögrög is Mongolia's official currency, issued by the Bank of Mongolia. Kyrgyzstan uses the som, Uzbekistan "
  "the sum and Turkmenistan the manat.",
  ["Tögrög: Mongolia", "Issuer: Bank of Mongolia"],
  [fact("The tögrög is the official currency of Mongolia, issued by the Bank of Mongolia", "g_mnt_wiki")],
  why="Kyrgyzstan (som), Uzbekistan (sum) and Turkmenistan (manat) use other currencies.")

G(T, CC, "Intermediate",
  "Prime Minister Modi visited Slovakia in June 2026. What is the capital of Slovakia?",
  ["Bratislava", "Ljubljana", "Prague", "Budapest"], "*",
  "Slovakia",
  "Bratislava is Slovakia's capital and largest city. Slovakia became independent on 1 January 1993 when "
  "Czechoslovakia dissolved, and uses the euro.",
  ["Capital: Bratislava", "Independent: 1 Jan 1993", "Currency: euro"],
  [fact("Slovakia: capital and largest city Bratislava; currency euro; independent 1 January 1993", "g_svk_wiki")],
  why="Ljubljana is Slovenia's capital, Prague the Czech Republic's and Budapest Hungary's.")

G(T, CC, "Intermediate",
  "What is the capital of Antigua and Barbuda, host of the Commonwealth Heads of Government Meeting 2026?",
  ["St. John's", "Castries", "Bridgetown", "Kingstown"], "*",
  "Antigua and Barbuda",
  "St. John's is the capital of Antigua and Barbuda, which became independent on 1 November 1981 and uses the Eastern "
  "Caribbean dollar.",
  ["Capital: St. John's", "Currency: Eastern Caribbean dollar", "Independence: 1 Nov 1981"],
  [fact("Antigua and Barbuda: capital St. John's; currency Eastern Caribbean dollar; independence 1 November 1981",
        "g_atg_wiki")],
  why="Castries is the capital of Saint Lucia, Bridgetown of Barbados and Kingstown of Saint Vincent and the "
      "Grenadines.")

G(T, NP, "Intermediate",
  "Kanha Tiger Reserve, the first tiger reserve in India to introduce an official mascot (Bhoorsingh the Barasingha), "
  "is located in which state?",
  ["Madhya Pradesh", "Chhattisgarh", "Maharashtra", "Odisha"], "*",
  "Kanha Tiger Reserve",
  "Kanha lies in the Mandla and Balaghat districts of Madhya Pradesh. It became a wildlife sanctuary in 1933, a "
  "national park in 1955 and a tiger reserve in 1973, and is known for the hard-ground barasingha.",
  ["State: Madhya Pradesh (Mandla, Balaghat)", "NP 1955; tiger reserve 1973", "Mascot: Bhoorsingh"],
  [fact("Kanha Tiger Reserve in Mandla and Balaghat, Madhya Pradesh; NP 1955, TR 1973; first tiger reserve with a "
        "mascot, Bhoorsingh the Barasingha", "g_kanha_wiki")],
  why="Kanha is in Madhya Pradesh, not in the neighbouring states.")

G(T, NP, "Intermediate",
  "Govind Ballabh Pant Sagar is the reservoir of which dam in Sonbhadra district, Uttar Pradesh?",
  ["Rihand Dam", "Matatila Dam", "Bansagar Dam", "Gandhi Sagar Dam"], "*",
  "Rihand Dam",
  "The Rihand Dam is a concrete gravity dam at Pipri in Sonbhadra district, Uttar Pradesh, on the Rihand river, a "
  "tributary of the Son. Its reservoir is Govind Ballabh Pant Sagar.",
  ["Dam: Rihand (Pipri, Sonbhadra)", "River: Rihand (tributary of the Son)", "Reservoir: Govind Ballabh Pant Sagar"],
  [fact("Rihand Dam: concrete gravity dam at Pipri, Sonbhadra, UP, on the Rihand (Son tributary); reservoir Govind "
        "Ballabh Pant Sagar", "g_rihand_wiki")],
  why="Matatila is on the Betwa, Bansagar on the Son in MP and Gandhi Sagar on the Chambal in MP.")

G(T, NP, "Intermediate",
  "Eravikulam National Park in Kerala, which contains Anamudi, the highest peak in South India, is best known for "
  "protecting which animal?",
  ["Nilgiri tahr", "Lion-tailed macaque", "One-horned rhinoceros", "Hangul"], "*",
  "Eravikulam National Park",
  "Eravikulam, in the Idukki and Ernakulam districts of Kerala and a national park since 1978, holds the largest "
  "population of the Nilgiri tahr. Anamudi (2,695 m) lies inside it.",
  ["Park: Eravikulam (Kerala), NP 1978", "Animal: Nilgiri tahr", "Peak: Anamudi"],
  [fact("Eravikulam NP, Kerala (Idukki and Ernakulam); Nilgiri tahr; Anamudi 2,695 m; NP in 1978",
        "g_eravi_wiki")],
  why="The lion-tailed macaque is linked to Silent Valley, the rhino to Kaziranga and the hangul to Dachigam.")

G(T, SF, "Intermediate",
  "Andhra State, formed on 1 October 1953 as the first state of independent India created on a linguistic basis, was "
  "carved out of which state, and what was its capital?",
  ["Madras State; Kurnool", "Hyderabad State; Hyderabad", "Madras State; Visakhapatnam",
   "Mysore State; Guntur"], "*",
  "Andhra State",
  "Andhra State was formed on 1 October 1953 from the Telugu-speaking districts of Madras State, with Kurnool as its "
  "capital. It was the first state in independent India formed for linguistic reasons; it merged with the Telugu "
  "areas of Hyderabad State in 1956 to form Andhra Pradesh.",
  ["Formed: 1 Oct 1953", "From: Madras State", "Capital: Kurnool"],
  [fact("Andhra State formed 1 October 1953 from Madras State; capital Kurnool; first state formed in independent "
        "India for linguistic reason", "g_andhra_wiki")],
  why="It was carved from Madras State, and its capital was Kurnool, not Hyderabad, Visakhapatnam or Guntur.")

G(T, SF, "Intermediate",
  "Haryana was formed on 1 November 1966 under which law?",
  ["Punjab Reorganisation Act, 1966", "States Reorganisation Act, 1956", "Bombay Reorganisation Act, 1960",
   "North-Eastern Areas (Reorganisation) Act, 1971"], "*",
  "Formation of Haryana",
  "Haryana was carved out of Punjab on 1 November 1966 under the Punjab Reorganisation Act, 1966. It shares its "
  "capital, Chandigarh, with Punjab.",
  ["Formed: 1 Nov 1966", "Law: Punjab Reorganisation Act, 1966", "Capital: Chandigarh (shared)"],
  [fact("Haryana formed on 1 November 1966 after the Punjab Reorganisation Act was passed; shares capital Chandigarh "
        "with Punjab", "g_har_wiki")],
  why="The 1956 Act reorganised states on linguistic lines, the 1960 Act split Bombay State and the 1971 Act created "
      "north-eastern states.")


# ###################################################################### part: asbr
# BATCH_005 GA fragment: Awards and Honours (0/3/1), Sports (1/10/1), Books and Authors (0/5/0),
# Important Reports and Indexes (0/3/0). Sources checked 2026-11-05.
U.update({
    # ---------------- Awards
    "s_infosys_print": ("https://theprint.in/science/infosys-prize-2025-winners-prakrit-languages-scholar-to-scientist-"
                        "who-identified-dna-repair-technique/2782591", OPENED),
    "s_infosys_dh": ("https://www.deccanherald.com/india/karnataka/bengaluru/infosys-science-foundation-announces-"
                     "winners-of-infosys-prize-2025-3795364", SEARCH),
    "s_coe_mongabay": ("https://news.mongabay.com/short-article/2025/12/un-honors-five-climate-champions-of-the-earth/",
                       OPENED),
    "s_coe_unep": ("https://www.unep.org/news-and-stories/press-release/uneps-2025-champions-earth-award-recognizes-"
                   "five-climate", SEARCH),
    "s_gtp_wgs": ("https://www.worldgovernmentssummit.org/media-hub/news/detail/indian-teacher-wins-global-teacher-"
                  "prize-2026-at-world-government-summit", OPENED),
    "s_gtp_mo": ("https://mediaoffice.ae/en/news/2026/february/05-02/hamdan-bin-mohammed-presents-indian-teacher-"
                 "rouble-nagi", OPENED),
    "s_swp_dte": ("https://www.downtoearth.org.in/water/from-water-terrorist-to-water-laureate-irans-eco-warrior-in-"
                  "exile-kaveh-madani-wins-2026-stockholm-water-prize", OPENED),
    # ---------------- Sports
    "s_tdf_kutv": ("https://kutv.com/sports/gallery/tadej-pogacar-cements-cycling-legacy-with-record-equaling-fifth-"
                   "tour-de-france-title?photo=1", OPENED),
    "s_uber_ba": ("https://badmintonasia.org/2026/05/03/uber-cup-2026-korea-topple-china-to-reclaim-uber-cup-glory-in-"
                  "horsens/", OPENED),
    "s_smat_espn": ("https://africa.espn.com/cricket/series/8661/report/1492665/haryana-vs-jharkhand-final-india-dom-"
                    "t20", OPENED),
    "s_vht_tv": ("https://www.indiatvnews.com/sports/cricket/vidarbha-beat-saurashtra-in-to-lift-maiden-vijay-hazare-"
                 "trophy-trophy-as-atharva-taide-slams-hundred-in-final-2026-01-19-1026425", OPENED),
    "s_vht_cric": ("https://www.espncricinfo.com/series/8890/report/1492800/vidarbha-vs-saurashtra-final-vijay-hazare-"
                   "trophy-2025-26", SEARCH),
    "s_santosh_aiff": ("https://www.the-aiff.com/article/services-defeat-kerala-to-clinch-eighth-santosh-trophy-title",
                       OPENED),
    "s_wimb_aj": ("https://www.aljazeera.com/amp/sports/2026/7/11/noskova-defeats-muchova-in-wimbledon-final-to-record-"
                  "first-grand-slam-title", OPENED),
    "s_norway_ians": ("https://ianslive.in/norway-chess-2026-praggnanandhaa-assaubayeva-claim-top-honours-ld--"
                      "20260606101216", OPENED),
    "s_norway_wiki": ("https://en.wikipedia.org/wiki/Norway_Chess_2026", SEARCH),
    "s_isl_ol": ("https://www.outlookindia.com/sports/football/east-bengal-isl-2025-26-champion", OPENED),
    "s_isl_nk": ("https://www.newkerala.com/news/a/painted-red-gold-east-bengal-won-maiden-isl-605.htm", OPENED),
    "s_duleep_etv": ("https://www.etvbharat.com/en/sports/east-zone-win-duleep-trophy-beating-south-zone-in-title-"
                     "clash-enn26091004001", OPENED),
    "s_wac_star": ("https://www.thestar.com.my/aseanplus/aseanplus-news/2026/03/21/it039s-nippon-power039---japan-beat-"
                   "australia-1-0-to-win-the-women039s-asian-cup", OPENED),
    "s_fo_fpj": ("https://www.freepressjournal.in/sports/french-open-2026-mirra-andreeva-becomes-youngest-womens-"
                 "champion-since-monica-seles-with-maiden-grand-slam-triumph", OPENED),
    "s_ballon_dr": ("https://www.drishtiias.com/state-pcs-current-affairs/harry-kane-wins-mens-ballon-dor-2026", OPENED),
    "s_ballon_bp": ("https://blueprint.ng/?p=856898", SEARCH),
    # ---------------- Books
    "s_tharoor_print": ("https://theprint.in/india/v-p-radhakrishnan-releases-tharoors-book-on-sree-narayan-guru-calls-"
                        "it-bridge-between-generations/2859112", OPENED),
    "s_gavai_ll": ("https://www.livelaw.in/top-stories/vice-president-launches-ex-cji-br-gavais-book-the-voice-of-"
                   "justice-justice-gavai-speaks-541216", OPENED),
    "s_sa_air": ("https://www.newsonair.gov.in/sahitya-akademi-announces-winners-of-sahitya-akademi-awards-2025-in-24-"
                 "indian-languages", OPENED),
    "s_goncourt_eu": ("https://www.euronews.com/culture/2025/11/04/prix-goncourt-2025-frances-top-literary-prize-"
                      "awarded-to-laurent-mauvignier-for-la-maison-", OPENED),
    "s_giller_uoft": ("https://www.utoronto.ca/celebrates/souvankham-thammavongsa-wins-2025-giller-prize", OPENED),
    # ---------------- Reports
    "s_sdg_dte": ("https://www.downtoearth.org.in/governance/hamburg-sustainability-conference-india-climbs-to-its-"
                  "highest-ever-rank-in-the-2026-un-sdg-index-but-hunger-remains-a-major-challenge", OPENED),
    "s_qs_air": ("https://newsonair.gov.in/iit-delhi-remains-indias-highest-ranked-institution-in-qs-world-university-"
                 "rankings-2027/", OPENED),
    "s_gti_dr": ("https://www.drishtiias.com/state-pcs-current-affairs/global-terrorism-index-gti-2026/print_manually",
                 OPENED),
})

# ====================================================================== Awards and Honours (0 / 3 / 1)
T = "Awards and Honours"
NAT, INTL = "National awards", "International awards"

G(T, NAT, "Intermediate",
  "The Infosys Prize 2025, announced on 12 November 2025, was awarded in the Mathematical Sciences category to "
  "which researcher?",
  ["Sabyasachi Mukherjee", "Andrew Ollett", "Anjana Badrinarayanan", "Karthish Manthiram"], "*",
  "Infosys Prize 2025",
  "The Infosys Science Foundation announced the Infosys Prize 2025 on 12 November 2025 in six categories. "
  "Sabyasachi Mukherjee of TIFR won Mathematical Sciences. Andrew Ollett (Humanities and Social Sciences), Anjana "
  "Badrinarayanan of NCBS (Life Sciences) and Karthish Manthiram of Caltech (Physical Sciences) won other categories. "
  "Each prize carries a gold medal, a citation and USD 100,000.",
  ["Announced: 12 Nov 2025", "Mathematical Sciences: Sabyasachi Mukherjee (TIFR)",
   "Other winners: Ollett (Humanities), Badrinarayanan (Life Sciences), Manthiram (Physical Sciences)"],
  [fact("Infosys Prize 2025 announced 12 Nov 2025; Mathematical Sciences: Sabyasachi Mukherjee, TIFR; Humanities: "
        "Andrew Ollett; Life Sciences: Anjana Badrinarayanan; Physical Sciences: Karthish Manthiram; USD 100,000",
        "s_infosys_print"),
   fact("Infosys Science Foundation announces winners of Infosys Prize 2025", "s_infosys_dh")],
  why="Ollett, Badrinarayanan and Manthiram won the Humanities, Life Sciences and Physical Sciences prizes.",
  current=ca("2025-11-12"))

G(T, INTL, "Intermediate",
  "Which Indian officer was named a UNEP 'Champion of the Earth' 2025 in the 'Inspiration and Action' category, "
  "for climate-resilient schools and housing and for restoring forest and mangrove cover?",
  ["Supriya Sahu", "Rouble Nagi", "Sunita Narain", "Bhumi Pednekar"], "*",
  "UNEP Champions of the Earth 2025",
  "UNEP announced its 2025 Champions of the Earth on 10 December 2025. The five laureates were Pacific Islands "
  "Students Fighting Climate Change, Supriya Sahu of India (Inspiration and Action), architect Mariam Issoufou, "
  "the Brazilian institute Imazon, and Manfredi Caltagirone (posthumous, lifetime contribution).",
  ["Award: UNEP Champions of the Earth 2025 (announced 10 Dec 2025)",
   "Indian laureate: Supriya Sahu, Inspiration and Action category"],
  [fact("UNEP named 2025 Champions of the Earth on 10 Dec 2025; Supriya Sahu (India), inspiration and action, forest "
        "official, climate-resilient schools, social housing, forest and mangrove restoration", "s_coe_mongabay"),
   fact("UNEP's 2025 Champions of the Earth award recognizes five climate trailblazers", "s_coe_unep")],
  why="Rouble Nagi won the Global Teacher Prize 2026; Sunita Narain and Bhumi Pednekar were not 2025 laureates.",
  current=ca("2025-12-10"))

G(T, INTL, "Intermediate",
  "Indian educator Rouble Nagi, known for turning walls in slums into learning spaces, won which USD 1 million "
  "award at the World Governments Summit in Dubai in February 2026?",
  ["Global Teacher Prize", "Zayed Sustainability Prize", "Yidan Prize", "Ramon Magsaysay Award"], "*",
  "Global Teacher Prize 2026",
  "Rouble Nagi won the tenth Global Teacher Prize, worth USD 1 million, presented at the World Governments Summit 2026 "
  "by Sheikh Hamdan bin Mohammed, Crown Prince of Dubai (reported 5 February 2026). The prize is presented by GEMS "
  "Education and organised by the Varkey Foundation with UNESCO. Her foundation has set up over 800 learning centres.",
  ["Prize: Global Teacher Prize (10th edition), USD 1 million", "Winner: Rouble Nagi (India)",
   "Presented at the World Governments Summit, Dubai"],
  [fact("Indian teacher Rouble Nagi wins Global Teacher Prize 2026 at World Government Summit; $1 million; 10th "
        "edition; GEMS Education, Varkey Foundation with UNESCO", "s_gtp_wgs"),
   fact("Hamdan bin Mohammed presents Indian teacher Rouble Nagi with Global Teacher Prize 2026, dated 5 Feb 2026",
        "s_gtp_mo")],
  why="The other three are different awards; none was presented to her at the summit.",
  current=ca("2026-02-05"))

GS(T, INTL, "Advanced", "the Stockholm Water Prize 2026",
   ["It was awarded to Kaveh Madani, Director of the UN University Institute for Water, Environment and Health "
    "(UNU-INWEH).",
    "The laureate was announced at UNESCO headquarters in Paris in March 2026.",
    "The prize is presented by the King of Norway during World Water Week in Oslo."],
   [True, True, False],
   "Stockholm Water Prize 2026",
   "On 18 March 2026, ahead of World Water Day, the 2026 Stockholm Water Prize was announced at UNESCO headquarters "
   "in Paris for Kaveh Madani, Director of UNU-INWEH. At 44 he is the youngest laureate and the first UN official to "
   "receive it. The prize is presented by Sweden's King Carl XVI Gustaf during World Water Week in Stockholm.",
   [fact("Kaveh Madani, Director of UNU-INWEH, named 2026 Stockholm Water Prize laureate on 18 March 2026 at UNESCO HQ "
         "Paris; King Carl XVI Gustaf of Sweden to present it during World Water Week in Stockholm", "s_swp_dte")],
   why="Statement 3 is wrong: the King of Sweden presents it in Stockholm.",
   current=ca("2026-03-18"))

# ====================================================================== Sports (1 / 10 / 1)
T = "Sports"
TW, VR = "Tournaments and winners", "Venues and records"

G(T, TW, "Basic",
  "Who won the Tour de France 2026, which ended in Paris on 26 July 2026?",
  ["Tadej Pogačar", "Jonas Vingegaard", "Remco Evenepoel", "Isaac del Toro"], "*",
  "Tour de France 2026",
  "Slovenia's Tadej Pogačar won the 2026 Tour de France, his fifth title, equalling the record of five wins. Remco "
  "Evenepoel of Belgium was second overall.",
  ["Winner: Tadej Pogačar (Slovenia), 5th title", "Runner-up: Remco Evenepoel"],
  [fact("Tadej Pogacar (Slovenia) wins record-equalling fifth Tour de France title on 26 July 2026; Remco Evenepoel "
        "second", "s_tdf_kutv")],
  why="Evenepoel was runner-up; Vingegaard and del Toro did not win the 2026 Tour.",
  current=ca("2026-07-26"))

G(T, TW, "Intermediate",
  "Which country won the Uber Cup 2026 (women's world team badminton championship), beating defending champions "
  "China 3-1 in the final at Horsens, Denmark, on 3 May 2026?",
  ["South Korea", "Japan", "Indonesia", "Thailand"], "*",
  "Uber Cup 2026",
  "South Korea beat China 3-1 in the Uber Cup final at Forum Horsens on 3 May 2026, its third title after 2010 and "
  "2022. An Se Young won the opening singles. China won the men's Thomas Cup at the same event.",
  ["Uber Cup 2026 winner: South Korea", "Score: 3-1 over China", "Korea's titles: 2010, 2022, 2026"],
  [fact("Korea beat defending champion China 3-1 at Forum Horsens on 3 May 2026; third Uber Cup after 2010 and 2022",
        "s_uber_ba")],
  why="Japan, Indonesia and Thailand did not reach the 2026 final.",
  current=ca("2026-05-03"))

G(T, TW, "Intermediate",
  "Which team won its first Syed Mushtaq Ali Trophy in December 2025, beating Haryana by 69 runs in the final at Pune "
  "after its captain Ishan Kishan scored a century?",
  ["Jharkhand", "Bihar", "Odisha", "Assam"], "*",
  "Syed Mushtaq Ali Trophy 2025-26",
  "Jharkhand made 262/3 in the final at Pune on 18 December 2025 and bowled Haryana out for 193 to win by 69 runs. "
  "Ishan Kishan was Player of the Match. It was Jharkhand's first title, in its first final.",
  ["Final: Jharkhand v Haryana, Pune, 18 Dec 2025", "Jharkhand won by 69 runs", "Maiden T20 title"],
  [fact("SMAT final, Pune, 18 Dec 2025: Jharkhand 262/3 beat Haryana 193 by 69 runs; Ishan Kishan Player of the "
        "Match; maiden title", "s_smat_espn")],
  why="Bihar, Odisha and Assam did not win the 2025-26 Syed Mushtaq Ali Trophy.",
  current=ca("2025-12-18"))

G(T, TW, "Intermediate",
  "Which team won its first Vijay Hazare Trophy in January 2026, beating Saurashtra by 38 runs in the final?",
  ["Vidarbha", "Karnataka", "Punjab", "Mumbai"], "*",
  "Vijay Hazare Trophy 2025-26",
  "Vidarbha scored 317/8, built on Atharva Taide's 128, and bowled Saurashtra out for 279 to win the final by 38 runs "
  "on 18 January 2026. It was Vidarbha's maiden Vijay Hazare (List A) title.",
  ["Final: Vidarbha v Saurashtra", "Vidarbha won by 38 runs", "Atharva Taide 128"],
  [fact("Vidarbha beat Saurashtra by 38 runs to seal maiden Vijay Hazare Trophy title; Atharva Taide 128; article "
        "19 Jan 2026 says the final was on Sunday", "s_vht_tv"),
   fact("Vidarbha vs Saurashtra, Final, Vijay Hazare Trophy 2025-26", "s_vht_cric")],
  why="Karnataka, Punjab and Mumbai were not in the 2025-26 final.",
  current=ca("2026-01-18"))

G(T, TW, "Intermediate",
  "Which team won the 79th Santosh Trophy (2025-26), beating Kerala 1-0 in extra time in the final at Dhakuakhana, "
  "Assam, on 8 February 2026?",
  ["Services", "West Bengal", "Goa", "Manipur"], "*",
  "Santosh Trophy 2025-26",
  "Services beat Kerala 1-0 in the final at Dhakuakhana Football Stadium on 8 February 2026, with Abhishek Pawar "
  "scoring in the 109th minute. It was Services' eighth Santosh Trophy title.",
  ["Final: Services 1-0 Kerala (a.e.t.)", "Scorer: Abhishek Pawar (109')", "Services' 8th title"],
  [fact("Services defeated Kerala 1-0 at Dhakuakhana, Assam, on 8 Feb 2026; Abhishek Pawar 109th minute; eighth "
        "title; 79th edition", "s_santosh_aiff")],
  why="West Bengal, Goa and Manipur did not play the final.",
  current=ca("2026-02-08"))

G(T, TW, "Intermediate",
  "Who won the women's singles title at Wimbledon 2026, her first Grand Slam title, by beating fellow Czech Karolina "
  "Muchová in the final?",
  ["Linda Nosková", "Barbora Krejčíková", "Markéta Vondroušová", "Petra Kvitová"], "*",
  "Wimbledon 2026 women's singles",
  "Ninth seed Linda Nosková beat Karolina Muchová 6-2, 5-7, 6-3 in an all-Czech final on 11 July 2026 to win her "
  "first Grand Slam title.",
  ["Final: Nosková d. Muchová 6-2, 5-7, 6-3", "Date: 11 July 2026", "Nosková's first Grand Slam"],
  [fact("Linda Noskova beat Karolina Muchova 6-2, 5-7, 6-3 on 11 July 2026 for her first Grand Slam title; both "
        "Czech", "s_wimb_aj")],
  why="Krejčíková, Vondroušová and Kvitová are earlier Czech Wimbledon champions, not the 2026 winner.",
  current=ca("2026-07-11"))

G(T, TW, "Intermediate",
  "Which Indian grandmaster won the open section of Norway Chess 2026 in Oslo, finishing ahead of Wesley So?",
  ["R. Praggnanandhaa", "D. Gukesh", "Arjun Erigaisi", "Nihal Sarin"], "*",
  "Norway Chess 2026",
  "R. Praggnanandhaa won Norway Chess 2026 with 18 points, ahead of Wesley So (17) and Alireza Firouzja (15.5), "
  "sealing it with a classical win in the final round. Bibisara Assaubayeva won the women's section.",
  ["Open winner: R. Praggnanandhaa (18 pts)", "Second: Wesley So", "Women: Bibisara Assaubayeva"],
  [fact("Norway Chess 2026: Praggnanandhaa won with 18 points, So 17, Firouzja 15.5; Assaubayeva won women's event",
        "s_norway_ians"),
   fact("Norway Chess 2026 held 25 May to 5 June 2026 in Oslo", "s_norway_wiki")],
  why="Gukesh, Arjun Erigaisi and Nihal Sarin did not win the 2026 open event.",
  current=ca("2026-06-05"))

G(T, TW, "Intermediate",
  "Which club won its first Indian Super League (ISL) title in the 2025-26 season, finishing level on points with "
  "Mohun Bagan Super Giant but ahead on goal difference?",
  ["East Bengal", "FC Goa", "Bengaluru FC", "Kerala Blasters"], "*",
  "ISL 2025-26",
  "On the final matchday, 21 May 2026, East Bengal beat Inter Kashi 2-1 at Kishore Bharati Krirangan. Both East "
  "Bengal and Mohun Bagan Super Giant finished on 26 points, and East Bengal won the title on goal difference (+19 "
  "to +14), ending a 22-year wait for a national league title.",
  ["Both teams on 26 points", "Goal difference: East Bengal +19, Mohun Bagan +14", "Maiden ISL title"],
  [fact("East Bengal won ISL 2025-26 on goal difference over Mohun Bagan Super Giant, both on 26 points; beat Inter "
        "Kashi 2-1", "s_isl_ol"),
   fact("East Bengal won maiden ISL title on 21 May 2026", "s_isl_nk")],
  why="FC Goa, Bengaluru FC and Kerala Blasters did not win the 2025-26 ISL.",
  current=ca("2026-05-21"))

G(T, TW, "Intermediate",
  "East Zone, captained by Ishan Kishan (who scored 270), won the Duleep Trophy 2026 on first-innings lead after the "
  "final was drawn. Which team did it face in the final?",
  ["South Zone", "Central Zone", "West Zone", "North Zone"], "*",
  "Duleep Trophy 2026",
  "The final between East Zone and South Zone ended in a draw on 10 September 2026, and East Zone took the title on "
  "first-innings lead after making 708, with Ishan Kishan scoring 270. Its previous title had come in 2012-13.",
  ["Final: East Zone v South Zone", "Result: drawn; East Zone won on first-innings lead", "Ishan Kishan 270"],
  [fact("East Zone beat South Zone on first-innings lead after draw on 10 Sep 2026; Ishan Kishan 270 in 708",
        "s_duleep_etv")],
  why="South Zone was East Zone's opponent in the final; the other zones did not reach it.",
  current=ca("2026-09-10"))

G(T, VR, "Intermediate",
  "Japan won the AFC Women's Asian Cup 2026 by beating hosts Australia 1-0 in the final on 21 March 2026. In which "
  "city was the final played?",
  ["Sydney", "Melbourne", "Brisbane", "Perth"], "*",
  "AFC Women's Asian Cup 2026",
  "The final was played at Stadium Australia, Sydney, on 21 March 2026. Maika Hamano scored the only goal in the "
  "17th minute, giving Japan its third Women's Asian Cup after 2014 and 2018.",
  ["Venue: Stadium Australia, Sydney", "Japan 1-0 Australia (Hamano 17')", "Japan's 3rd title"],
  [fact("Japan beat Australia 1-0 at Stadium Australia, Sydney, on 21 March 2026; Maika Hamano 17th minute; third "
        "title after 2014 and 2018", "s_wac_star")],
  why="The final was not played in Melbourne, Brisbane or Perth.",
  current=ca("2026-03-21"))

G(T, VR, "Intermediate",
  "Russian teenager Mirra Andreeva won the French Open women's singles title on 6 June 2026. She became the youngest "
  "women's champion at Roland Garros since whom?",
  ["Monica Seles (1992)", "Iga Świątek (2020)", "Arantxa Sánchez Vicario (1989)", "Steffi Graf (1987)"], "*",
  "French Open 2026 women's singles",
  "Mirra Andreeva, 19, beat Polish qualifier Maja Chwalińska 6-3, 6-2 in the final on 6 June 2026 for her first Grand "
  "Slam title. She is the youngest women's champion in Paris since Monica Seles in 1992.",
  ["Winner: Mirra Andreeva (19, Russia)", "Final: d. Maja Chwalińska 6-3, 6-2",
   "Youngest since Monica Seles (1992)"],
  [fact("Mirra Andreeva, 19, beat Maja Chwalinska 6-3, 6-2 on 6 June 2026; maiden Grand Slam; youngest women's "
        "champion since Monica Seles in 1992", "s_fo_fpj")],
  why="The report names Seles (1992) as the last younger champion; the others won at older ages or earlier.",
  current=ca("2026-06-06"))

GS(T, TW, "Advanced", "the men's Ballon d'Or 2026",
   ["Harry Kane won it at the ceremony held on 26 October 2026.",
    "It was the first time the Ballon d'Or ceremony was held in London.",
    "Lamine Yamal finished as runner-up."],
   [True, True, False],
   "Ballon d'Or 2026",
   "England captain and Bayern Munich striker Harry Kane won the men's Ballon d'Or at the London Palladium on "
   "26 October 2026, the first ceremony held in London. Kylian Mbappé was runner-up, and Paris Saint-Germain won "
   "Men's Club of the Year.",
   [fact("Harry Kane won the 2026 men's Ballon d'Or in London on 26 Oct 2026 at the London Palladium, first time in "
         "London; runner-up Kylian Mbappe; PSG club of the year", "s_ballon_dr"),
    fact("Harry Kane wins 2026 Men's Ballon d'Or", "s_ballon_bp")],
   why="Statement 3 is wrong: the runner-up was Kylian Mbappé.",
   current=ca("2026-10-26"))

# ====================================================================== Books and Authors (0 / 5 / 0)
T = "Books and Authors"
RB = "Recent books"

G(T, RB, "Intermediate",
  "'The Sage Who Reimagined Hinduism', released by Vice-President C. P. Radhakrishnan in New Delhi on 19 February "
  "2026, is Shashi Tharoor's book about which reformer?",
  ["Sree Narayana Guru", "Swami Vivekananda", "Chattampi Swamikal", "Ayyankali"], "*",
  "Recent books: Shashi Tharoor",
  "The book, 'The Sage Who Reimagined Hinduism: The Life, Lessons, and Legacy of Sree Narayana Guru', published by "
  "Aleph, is about the Kerala reformer who opposed caste discrimination. It was released at the India International "
  "Centre on 19 February 2026.",
  ["Author: Shashi Tharoor", "Subject: Sree Narayana Guru", "Released by VP C. P. Radhakrishnan, 19 Feb 2026"],
  [fact("VP Radhakrishnan released Tharoor's 'The Sage Who Reimagined Hinduism: The Life, Lessons, and Legacy of "
        "Sree Narayana Guru' on 19 Feb 2026 at IIC, New Delhi; Aleph", "s_tharoor_print")],
  why="The book's subtitle names Sree Narayana Guru; it is not about the other reformers.",
  current=ca("2026-02-19"))

G(T, RB, "Intermediate",
  "'The Voice of Justice', launched by Vice-President C. P. Radhakrishnan in July 2026, is a collection of the speeches "
  "of which former Chief Justice of India?",
  ["B. R. Gavai", "D. Y. Chandrachud", "Sanjiv Khanna", "U. U. Lalit"], "*",
  "Recent books: The Voice of Justice",
  "'The Voice of Justice: Justice Gavai Speaks', a curated collection of former CJI B. R. Gavai's speeches edited by "
  "Prof. S. Sivakumar and published by Thomson Reuters, was launched at the Vice-President's Enclave on 14 July "
  "2026, with CJI Surya Kant presiding.",
  ["Book: The Voice of Justice: Justice Gavai Speaks", "Launched 14 July 2026 by VP Radhakrishnan"],
  [fact("VP launches ex-CJI B.R. Gavai's book 'The Voice of Justice: Justice Gavai Speaks', collection of speeches, "
        "Thomson Reuters, edited by S. Sivakumar; article 14 July 2026", "s_gavai_ll")],
  why="The title itself names Justice Gavai; the others are different former CJIs.",
  current=ca("2026-07-14"))

G(T, RB, "Intermediate",
  "Hindi writer Mamta Kalia won the Sahitya Akademi Award 2025, announced on 16 March 2026, for which work?",
  ["Jeete Jee Allahabad", "Crimson Spring", "Safar Jaari Hai", "Shrestha Kabita"], "*",
  "Sahitya Akademi Award 2025 (Hindi)",
  "The Sahitya Akademi announced its 2025 awards in 24 languages on 16 March 2026. Mamta Kalia won in Hindi for her "
  "memoir 'Jeete Jee Allahabad'. 'Crimson Spring' (Navtej Sarna) won in English, 'Safar Jaari Hai' (Pritpal Singh "
  "Betab) in Urdu and 'Shrestha Kabita' (Prasun Bandyopadhyay) in Bengali.",
  ["Hindi: Mamta Kalia, 'Jeete Jee Allahabad' (memoir)", "Announced 16 March 2026"],
  [fact("Sahitya Akademi Awards 2025 announced 16 March 2026: Hindi Mamta Kalia, memoir Jeete Jee Allahabad; English "
        "Navtej Sarna, Crimson Spring; Urdu Safar Jaari Hai; Bengali Shrestha Kabita", "s_sa_air")],
  why="The other three won in English, Urdu and Bengali.",
  current=ca("2026-03-16"))

G(T, RB, "Intermediate",
  "Laurent Mauvignier won France's Prix Goncourt 2025 on 4 November 2025 for which novel?",
  ["La Maison vide (The Empty House)", "Houris", "Veiller sur elle", "Je voulais vivre"], "*",
  "Prix Goncourt 2025",
  "The Goncourt, France's top literary prize, went to Laurent Mauvignier for 'La Maison vide', published by Éditions "
  "de Minuit, on 4 November 2025. The prize money is a symbolic 10 euros. 'Houris' (Kamel Daoud) won in 2024.",
  ["Prix Goncourt 2025: Laurent Mauvignier", "Novel: La Maison vide (The Empty House)"],
  [fact("Prix Goncourt 2025 awarded on 4 Nov 2025 to Laurent Mauvignier for 'La Maison vide' (The Empty House), "
        "Editions de Minuit, symbolic 10 euros", "s_goncourt_eu")],
  why="'Houris' won in 2024 and 'Veiller sur elle' in 2023; 'Je voulais vivre' won the Renaudot 2025.",
  current=ca("2025-11-04"))

G(T, RB, "Intermediate",
  "Souvankham Thammavongsa won Canada's Giller Prize 2025 in November 2025, her second Giller, for which book?",
  ["Pick a Colour", "How to Pronounce Knife", "The Loneliness of Sonia and Sunny", "Flesh"], "*",
  "Giller Prize 2025",
  "Thammavongsa won the 2025 Giller Prize (CAD 100,000) in Toronto on 17 November 2025 for her debut novel 'Pick a "
  "Colour'. Her first Giller, in 2020, was for the story collection 'How to Pronounce Knife'.",
  ["Giller 2025: 'Pick a Colour' (17 Nov 2025)", "Giller 2020: 'How to Pronounce Knife'"],
  [fact("Souvankham Thammavongsa won 2025 Giller Prize for debut novel Pick a Colour, accepted in Toronto on 17 Nov; "
        "second Giller after How to Pronounce Knife (2020)", "s_giller_uoft")],
  why="'How to Pronounce Knife' won in 2020; the other two are Booker 2025 titles by other authors.",
  current=ca("2025-11-17"))

# ====================================================================== Important Reports and Indexes (0 / 3 / 0)
T = "Important Reports and Indexes"
PB, RANK = "Publishing body", "India's rank"

G(T, PB, "Intermediate",
  "India reached its best-ever rank, 94th of 167 countries, in the SDG Index of the Sustainable Development Report "
  "2026. Which body publishes this report?",
  ["UN Sustainable Development Solutions Network (SDSN)", "NITI Aayog", "UN Department of Economic and Social Affairs",
   "World Economic Forum"], "*",
  "Sustainable Development Report 2026",
  "The Sustainable Development Report, with its SDG Index, is published by the UN Sustainable Development Solutions "
  "Network. In the 2026 edition (reported 28 June 2026) India rose from 99th to 94th of 167 countries, with a score "
  "of 68.3. NITI Aayog publishes the separate SDG India Index.",
  ["Publisher: SDSN", "India 2026: 94th of 167 (score 68.3), up from 99th"],
  [fact("India climbed to 94th among 167 countries in the 2026 SDG Index (score 68.3), up from 99th; Sustainable "
        "Development Report 2026 by the UN SDSN", "s_sdg_dte")],
  why="NITI Aayog publishes the national SDG India Index; UN DESA and the WEF do not publish this report.",
  current=ca("2026-06-28"))

G(T, RANK, "Intermediate",
  "In the QS World University Rankings 2027, released in June 2026, which was India's highest-ranked institution, at "
  "118th?",
  ["IIT Delhi", "IIT Bombay", "IISc Bengaluru", "IIT Madras"], "*",
  "QS World University Rankings 2027",
  "IIT Delhi was India's top institution at 118th in the QS World University Rankings 2027 (announced 18 June 2026). "
  "A record 52 Indian institutions featured; IIT Bombay and IIT Madras were also in the top 200.",
  ["Top Indian: IIT Delhi, 118th", "52 Indian institutions ranked"],
  [fact("IIT Delhi India's highest-ranked institution at 118th in QS World University Rankings 2027; 52 Indian "
        "institutions; 18 June 2026", "s_qs_air")],
  why="IIT Delhi was the highest-ranked Indian institution; IIT Bombay, IISc and IIT Madras ranked below it.",
  current=ca("2026-06-18"))

G(T, RANK, "Intermediate",
  "What was India's rank in the Global Terrorism Index 2026, released by the Institute for Economics and Peace in "
  "March 2026, in which Pakistan was ranked first?",
  ["13th", "8th", "20th", "5th"], "*",
  "Global Terrorism Index 2026",
  "The GTI 2026, released on 25 March 2026 by the Sydney-based Institute for Economics and Peace, ranked India 13th "
  "with a score of 6.428. Pakistan was ranked first, i.e. most affected by terrorism.",
  ["GTI 2026: India 13th (score 6.428)", "Rank 1: Pakistan"],
  [fact("GTI 2026 released 25 March 2026 by IEP; India 13th with score 6.428; Pakistan first", "s_gti_dr")],
  why="India was 13th; the other ranks are not India's.",
  current=ca("2026-03-25"))


# ###################################################################### part: econ
# part_econ.py: Economic Affairs (4/7/3), Government Policies (5/0/5), Business and Corporate News (2/0/0).
# All URLs checked on 2026-11-05. OPENED = fetched and read; SEARCH = confirmed only in search-result text.

U.update({
    # ---------------- Economic Affairs
    "e_cpi_oct_bt": ("https://www.businesstoday.in/latest/economy/story/indias-retail-inflation-eases-record-low-october-gst-"
                     "cuts-food-price-drop-501928-2025-11-12", OPENED),
    "e_cpi_oct_ao": ("https://www.angelone.in/news/economy/indias-consumer-inflation-cools-to-record-low-in-october-driven-"
                     "by-falling-food-prices", SEARCH),
    "e_gst_oct_air": ("https://newsonair.gov.in/indias-gross-gst-collections-rise-23-to-%E2%82%B92-31-lakh-crore-in-oct/",
                      OPENED),
    "e_japan_fpj": ("https://www.freepressjournal.in/india/india-overtakes-japan-to-become-worlds-fourth-largest-economy",
                    OPENED),
    "e_japan_om": ("https://www.outlookmoney.com/news/india-surpasses-japan-to-become-worlds-4th-largest-economy-says-govt",
                   SEARCH),
    "e_wesp_air": ("https://www.newsonair.gov.in/united-nations-pegs-indias-gdp-growth-at-6-6-per-cent-in-current-"
                   "financial-year-due-to-resilient-domestic-demand/", OPENED),
    "e_wesp_dte": ("https://www.downtoearth.org.in/economy/global-economic-growth-to-slow-to-27-in-2026-but-east-and-south-"
                   "asia-set-to-outperform-says-un", SEARCH),
    "e_oecd_pe": ("https://www.policyedge.in/p/oecd-raises-indias-fy-202627-growth-forecast-to-71-despite-energy-shock",
                  OPENED),
    "e_oecd_ibef": ("https://www.ibef.org/news/oecd-raises-india-s-fy27-gdp-growth-forecast-by-80-bps-to-7-1", SEARCH),
    "e_cpi_jul_dd": ("https://ddindia.co.in/2026/08/indias-retail-inflation-rises-to-4-45-in-july-food-inflation-at-5-52/",
                     OPENED),
    "e_target_print": ("https://theprint.in/economy/govt-asks-rbi-to-maintain-retail-inflation-at-4-pc-till-mar-2031/"
                       "2888807", OPENED),
    "e_target_bt": ("https://www.businesstoday.in/latest/economy/story/govt-retains-inflation-target-at-4-with-2-6-band-for-"
                    "next-five-years-522390-2026-03-25", SEARCH),
    "e_wpi_oct_trib": ("https://www.tribuneindia.com/news/business/indias-wholesale-inflation-stays-negative-for-fourth-"
                       "month-wpi-falls-1-21-in-october-2025", OPENED),
    "e_wpi_oct_etv": ("https://www.etvbharat.com/en/business/wholesale-price-inflation-in-october-enn25111402147", OPENED),
    "e_core_bt": ("https://www.businesstoday.in/latest/economy/story/indias-core-sector-growth-accelerates-to-7-9-in-"
                  "september-refinery-output-jumps-10-3-562873-2026-10-21", OPENED),
    "e_core_dd": ("https://www.devdiscourse.com/article/business/3995751-indias-core-sector-growth-accelerates-to-79-in-"
                  "september-from-59-in-august", OPENED),
    "e_fitch_air": ("https://newsonair.gov.in/fitch-ratings-raises-indias-fy27-gdp-growth-forecast-from-6-4-to-6-9/",
                    OPENED),
    "e_fitch_org": ("https://organiser.org/2026/09/25/382554/bharat/fitch-raises-indias-fy27-growth-forecast-to-6-9-per-"
                    "cent-on-strong-economic-momentum/", SEARCH),
    "e_surplus_rep": ("https://www.republicworld.com/business/rbi-dividend-payout-fy26-record-surplus-transfer-government-"
                      "2026-05-22-125326", OPENED),
    "e_surplus_bt": ("https://www.businesstoday.in/latest/economy/story/rbi-transfers-record-rs2-87-lakh-cr-surplus-to-"
                     "government-but-falls-short-of-budget-target-532917-2026-05-22", OPENED),
    "e_h2_dt": ("https://www.dtnext.in/news/national/centre-to-borrow-rs-786-lakh-cr-in-oct-mar-fy27-borrowing-slashed-"
                "by-rs-12-lakh-cr", OPENED),
    "e_h2_dd": ("https://www.devdiscourse.com/article/business/3982558-govt-to-borrow-rs-786-lakh-crore-through-dated-"
                "securities-in-second-half-of-fy27", OPENED),
    "e_wpi_new_ians": ("https://ianslive.in/wholesale-inflation-at-968-pc-in-may-new-wpi-series-launched-with-2022-23-"
                       "base-year--20260615121957", OPENED),
    "e_wpi_new_fpj": ("https://www.freepressjournal.in/business/wpi-inflation-at-968-govt-launches-new-wholesale-price-"
                      "series-with-2022-23-base-year", OPENED),
    "e_wpi_new_eaind": ("https://www.eaindustry.nic.in/press_release/press_release_202606.pdf", SEARCH),
    "e_iip_fpj": ("https://www.freepressjournal.in/amp/business/indias-industrial-output-grows-49-in-april-manufacturing-"
                  "sector-leads-growth-under-new-iip-series", OPENED),
    "e_iip_drishti": ("https://www.drishtiias.com/daily-updates/daily-news-analysis/index-of-industrial-production-and-"
                      "revision-of-base-year/print_manually", OPENED),
    # ---------------- Government Policies
    "e_monsoon_scc": ("https://www.scconline.com/blog/post/2026/08/21/parliament-monsoon-session-2026-key-acts-bills/",
                      OPENED),
    "e_sc_bb": ("https://www.barandbench.com/news/law-policy/president-promulgates-ordinance-to-increase-supreme-court-"
                "judge-strength-to-38", OPENED),
    "e_bbe_livelaw": ("https://www.livelaw.in/news-updates/lok-sabha-passes-bankers-book-evidence-bill-2026-544611",
                      SEARCH),
    "e_honour_om": ("https://www.onmanorama.com/news/india/2026/07/30/lok-sabha-vande-mataram-bill-passed.html", OPENED),
    "e_sebi_upstox": ("https://upstox.com/news/market-news/financial-regulations/sebi-board-meet-outcome-from-buyback-"
                      "revival-via-exchanges-to-relaxed-intraday-borrowing-for-m-fs-everything-you-need-to-know/article-"
                      "195689/", OPENED),
    "e_sebi_elp": ("https://elplaw.in/leadership/key-decisions-of-the-sebi-board-meeting-dated-june-19-2026/", OPENED),
    "e_rbd_livelaw": ("https://www.livelaw.in/news-updates/president-assents-to-registration-of-births-deaths-amendment-"
                      "act-2026-544755", OPENED),
    "e_fdi_taxmann": ("https://www.taxmann.com/post/blog/cabinet-approves-fdi-policy-changes-for-bordering-countries/",
                      OPENED),
    "e_fdi_5p": ("https://www.5paisa.com/news/cabinet-eases-press-note-3-rules-allows-up-to-10-border-country-fdi-through-"
                 "automatic-route", OPENED),
    # ---------------- Business
    "e_haier_wp": ("https://warburgpincus.com/2025/12/24/bharti-enterprises-and-warburg-pincus-announce-strategic-"
                   "investment-in-haier-india/", OPENED),
    "e_haier_week": ("https://www.theweek.in/wire-updates/business/2025/12/24/dcm37-biz-bharti-haier-investment.html",
                     SEARCH),
    "e_coforge_ians": ("https://ianslive.in/coforge-to-acquire-us-based-encora-in-235-billion-all-stock-deal--"
                       "20251226205227", OPENED),
})

# ====================================================================== Economic Affairs (4 / 7 / 3)
T = "Economic Affairs"
GDP, INF, FIS, MON = ("GDP and growth projections", "Inflation data", "Fiscal data", "Monetary policy decisions")

G(T, INF, "Basic",
  "India's headline retail (CPI) inflation for October 2025, released on 12 November 2025, was the lowest since the "
  "series began. What was it?",
  ["0.25%", "0.71%", "1.44%", "2.07%"], "*",
  "CPI inflation, October 2025",
  "MoSPI data released on 12 November 2025 put CPI inflation for October 2025 at 0.25%, a record low for the series "
  "that began in 2015. Falling food prices (food inflation about -5%) and the GST rate cuts of 22 September 2025 "
  "pulled it down; September 2025 was revised to 1.44%.",
  ["October 2025 CPI inflation: 0.25%", "Lowest in the series", "Drivers: food deflation, GST rate cuts"],
  [fact("India's retail inflation hits record low of 0.25% in October 2025, released 12 Nov 2025; lowest since the "
        "current series began; September revised to 1.44%", "e_cpi_oct_bt"),
   fact("India's consumer inflation cools to record low of 0.25% in October", "e_cpi_oct_ao")],
  why="1.44% was the revised September 2025 figure; 0.71% and 2.07% were not the October 2025 reading.",
  current=ca("2025-11-12"))

G(T, FIS, "Basic",
  "According to data released on 1 November 2026, India's gross GST collections for October 2026 were about how much?",
  ["₹2.31 lakh crore", "₹1.87 lakh crore", "₹2.03 lakh crore", "₹2.58 lakh crore"], "*",
  "GST collections, October 2026",
  "Gross GST collections for October 2026 were about ₹2.31 lakh crore, up about 23% year-on-year, with domestic "
  "revenue of ₹1.59 lakh crore and import revenue of ₹72,246 crore. After refunds of ₹27,934 crore, net collections "
  "were about ₹2.03 lakh crore.",
  ["Gross GST, Oct 2026: about ₹2.31 lakh crore (+23%)", "Net GST: about ₹2.03 lakh crore"],
  [fact("India's gross GST collections rise 23% to ₹2.31 lakh crore in October 2026; net about ₹2.03 lakh crore; "
        "reported 1 Nov 2026", "e_gst_oct_air")],
  why="₹2.03 lakh crore is the net (after refunds) figure; ₹1.87 lakh crore and ₹2.58 lakh crore are not the October "
      "2026 gross figure.",
  current=ca("2026-11-01"))

G(T, GDP, "Basic",
  "According to a government release of 30 December 2025, India, with GDP of about USD 4.18 trillion, overtook which "
  "country to become the world's fourth-largest economy?",
  ["Japan", "Germany", "United Kingdom", "France"], "*",
  "India's economic size",
  "A government release on 30 December 2025 said India's GDP of about USD 4.18 trillion had made it the fourth-largest "
  "economy, overtaking Japan, behind the US and China. It projected India to pass Germany for third place in about "
  "2.5 to 3 years, with GDP of USD 7.3 trillion by 2030.",
  ["India: about USD 4.18 trillion", "Overtook Japan; now 4th after US and China", "Germany next (3rd place)"],
  [fact("India overtakes Japan to become world's fourth-largest economy at USD 4.18 trillion; government release; "
        "updated 30 Dec 2025; Germany expected to be passed in 2.5-3 years", "e_japan_fpj"),
   fact("India surpasses Japan to become world's 4th largest economy, says govt", "e_japan_om")],
  why="Germany is still ahead (India aims to pass it next); the UK and France were overtaken earlier.",
  current=ca("2025-12-30"))

G(T, GDP, "Basic",
  "In its 'World Economic Situation and Prospects 2026' report released in January 2026, what GDP growth did the "
  "United Nations project for India for 2026?",
  ["6.6%", "7.4%", "6.2%", "5.6%"], "*",
  "UN WESP 2026",
  "The UN's World Economic Situation and Prospects 2026 (January 2026) projected India's growth at 6.6% in 2026, "
  "edging up to 6.7% in 2027, supported by resilient consumption and public investment. It projected world growth of "
  "2.7% in 2026.",
  ["Report: UN WESP 2026 (January 2026)", "India 2026: 6.6%", "India 2027: 6.7%"],
  [fact("UN World Economic Situation and Prospects 2026 pegs India's GDP growth at 6.6% in 2026 and 6.7% in 2027; "
        "published 9 January 2026", "e_wesp_air"),
   fact("Global economic growth to slow to 2.7% in 2026; India 6.6%, says UN", "e_wesp_dte")],
  why="7.4%, 6.2% and 5.6% are not the UN's 2026 projection for India, which was 6.6%.",
  current=ca("2026-01-09"))

G(T, GDP, "Intermediate",
  "In its Interim Economic Outlook released in September 2026, what real GDP growth did the OECD project for India "
  "for 2026-27?",
  ["7.1%", "6.3%", "6.5%", "7.6%"], "*",
  "OECD Interim Outlook, September 2026",
  "The OECD's September 2026 Interim Economic Outlook (released 23 September) raised India's 2026-27 growth forecast "
  "to 7.1%, up 0.8 percentage points from its June forecast of 6.3%. It projected 6.5% for 2027-28 and inflation of "
  "4.7% in 2026-27.",
  ["June 2026 OECD forecast for FY27: 6.3%", "September 2026 forecast: 7.1% (+0.8 pp)", "FY28: 6.5%"],
  [fact("OECD Interim Report September 2026 raises India's FY2026-27 growth forecast to 7.1%, up 0.8 pp from June; "
        "FY2027-28 6.5%; inflation 4.7%", "e_oecd_pe"),
   fact("OECD raises India's FY27 GDP growth forecast by 80 bps to 7.1%; interim outlook released 23 September",
        "e_oecd_ibef")],
  why="6.3% was the OECD's June 2026 forecast; 6.5% is its 2027-28 projection; 7.6% is not the September figure.",
  current=ca("2026-09-23"))

G(T, INF, "Intermediate",
  "What was India's headline CPI (retail) inflation for July 2026, released on 12 August 2026 on the 2024=100 series?",
  ["4.45%", "4.38%", "4.82%", "5.52%"], "*",
  "CPI inflation, July 2026",
  "MoSPI put July 2026 CPI inflation at 4.45%, up from 4.38% in June. Food inflation (CFPI) rose to 5.52%. Rural "
  "inflation (4.84%) was higher than urban inflation (3.96%), and Telangana had the highest inflation among large "
  "states (6.32%).",
  ["July 2026 CPI: 4.45%", "June 2026: 4.38%", "Food inflation July 2026: 5.52%"],
  [fact("India's retail inflation rises to 4.45% in July 2026 from 4.38% in June; food inflation 5.52%; rural 4.84%, "
        "urban 3.96%; base 2024=100; released 12 Aug 2026", "e_cpi_jul_dd")],
  why="4.38% was June 2026 and 4.82% was August 2026; 5.52% was food inflation, not headline CPI.",
  current=ca("2026-08-12"))

G(T, MON, "Intermediate",
  "By a gazette notification of 25 March 2026, the Central Government set the RBI's inflation target for the period "
  "1 April 2026 to 31 March 2031. What is it?",
  ["4% CPI inflation, with an upper tolerance of 6% and a lower tolerance of 2%",
   "4% CPI inflation, with an upper tolerance of 5% and a lower tolerance of 3%",
   "4.5% CPI inflation, with an upper tolerance of 6.5% and a lower tolerance of 2.5%",
   "4% WPI inflation, with an upper tolerance of 6% and a lower tolerance of 2%"], "*",
  "Flexible inflation targeting",
  "The Department of Economic Affairs notified on 25 March 2026 that the inflation target for 1 April 2026 to "
  "31 March 2031 stays at 4% CPI inflation, with tolerance levels of 6% (upper) and 2% (lower). This is the second "
  "time the target has been retained since the framework began in 2016 (it was first renewed in March 2021).",
  ["Target: 4% (CPI)", "Band: 2% to 6%", "Period: 1 Apr 2026 to 31 Mar 2031", "Notified: 25 Mar 2026"],
  [fact("Gazette notification of 25 March 2026: inflation target 4% with upper tolerance 6% and lower tolerance 2% for "
        "1 April 2026 to 31 March 2031; issued by Department of Economic Affairs", "e_target_print"),
   fact("Govt retains inflation target at 4% with 2-6% band for next five years", "e_target_bt")],
  why="The band is 2% to 6%, not 3% to 5%; the target is 4%, not 4.5%; it is set in terms of CPI, not WPI.",
  current=ca("2026-03-25"))

G(T, INF, "Intermediate",
  "India's wholesale price (WPI) inflation for October 2025, released on 14 November 2025, stayed in negative territory "
  "for the fourth straight month. What was it?",
  ["-1.21%", "0.13%", "-0.13%", "-2.55%"], "*",
  "WPI inflation, October 2025",
  "WPI inflation for October 2025 was (-)1.21%, down from 0.13% in September 2025, mainly because of lower prices of "
  "food articles (deflation of 8.31%), fuel and manufactured goods. Fuel and power showed deflation of 2.55%.",
  ["October 2025 WPI: -1.21%", "September 2025 WPI: 0.13%", "Fuel and power: -2.55%"],
  [fact("WPI inflation of (-)1.21% in October 2025; negative for the fourth straight month", "e_wpi_oct_trib"),
   fact("October 2025 WPI -1.21% vs 0.13% in September; released Friday 14 Nov 2025; fuel and power -2.55%",
        "e_wpi_oct_etv")],
  why="0.13% was September 2025; -0.13% is a misreading; -2.55% was the fuel and power group, not headline WPI.",
  current=ca("2025-11-14"))

G(T, GDP, "Intermediate",
  "India's index of core industries grew 7.9% in September 2026 (data released on 21 October 2026). Which industry "
  "recorded the highest year-on-year growth in that month?",
  ["Iron ore", "Electricity", "Coal", "Refinery products"], "*",
  "Core industries, September 2026",
  "Core sector growth accelerated to 7.9% in September 2026 from 5.9% in August. Iron ore led with 18.4% growth, "
  "followed by electricity (11.4%), coal (10.7%) and refinery products (10.3%); fertilisers, natural gas and crude oil "
  "declined.",
  ["Core sector, Sep 2026: +7.9%", "Iron ore: +18.4% (highest)", "Electricity 11.4%, coal 10.7%, refinery 10.3%"],
  [fact("Core sector growth 7.9% in September 2026; iron ore recorded the highest growth (18.4%); refinery products "
        "10.3%; fertiliser -11.7%", "e_core_bt"),
   fact("Core sector growth accelerated to 7.9% in September from 5.9% in August; data released 21 Oct 2026; iron ore "
        "18.4%", "e_core_dd")],
  why="Electricity, coal and refinery products grew strongly but less than iron ore's 18.4%.",
  current=ca("2026-10-21"))

G(T, GDP, "Intermediate",
  "On 23 September 2026 Fitch Ratings revised its forecast of India's GDP growth for 2026-27. What is the revised "
  "figure?",
  ["6.9%", "6.4%", "7.0%", "6.5%"], "*",
  "Fitch growth forecast",
  "Fitch raised its FY27 growth forecast for India to 6.9% from 6.4%, citing a strong June quarter. It expects growth "
  "to ease to 6.5% in FY28 and inflation to rise to 5.5% by December 2026.",
  ["Earlier Fitch FY27 forecast: 6.4%", "Revised (23 Sep 2026): 6.9%", "FY28: 6.5%"],
  [fact("Fitch Ratings raises India's FY27 GDP growth forecast from 6.4% to 6.9%; FY28 6.5%; dated 23 Sep 2026",
        "e_fitch_air"),
   fact("Fitch raises India's FY27 growth forecast to 6.9 per cent", "e_fitch_org")],
  why="6.4% was Fitch's earlier FY27 forecast and 6.5% is its FY28 forecast; 7.0% is not Fitch's figure.",
  current=ca("2026-09-23"))

G(T, FIS, "Intermediate",
  "On 22 May 2026 the RBI's Central Board approved a record transfer of surplus to the Central Government for the "
  "accounting year 2025-26. About how much was it?",
  ["₹2.87 lakh crore", "₹2.69 lakh crore", "₹3.16 lakh crore", "₹2.11 lakh crore"], "*",
  "RBI surplus transfer",
  "At its 623rd meeting in Mumbai, the RBI Central Board approved a surplus transfer of ₹2,86,588.46 crore (about "
  "₹2.87 lakh crore) for 2025-26, above the ₹2.69 lakh crore of the previous year. It kept the Contingent Risk Buffer "
  "at 6.5% of the balance sheet. The payout was below the Budget's ₹3.16 lakh crore estimate for dividends and surplus.",
  ["FY26 surplus: ₹2,86,588.46 crore (about ₹2.87 lakh crore)", "FY25: about ₹2.69 lakh crore",
   "Budget estimate (dividends and surplus): ₹3.16 lakh crore"],
  [fact("RBI Central Board, 623rd meeting in Mumbai, approved surplus transfer of Rs 2,86,588.46 crore for FY2025-26; "
        "CRB at 6.5% of balance sheet; CRB range 4.5%-7.5%", "e_surplus_rep"),
   fact("RBI transfers record ₹2.87 lakh crore surplus, approved Friday 22 May 2026; previous year ₹2.69 lakh crore; "
        "Budget estimate ₹3.16 lakh crore", "e_surplus_bt")],
  why="₹2.69 lakh crore was the previous year's transfer, ₹2.11 lakh crore the one before; ₹3.16 lakh crore was the "
      "Budget estimate.",
  current=ca("2026-05-22"))

GS(T, FIS, "Advanced", "the Centre's borrowing calendar for October 2026-March 2027 (H2 of 2026-27)",
   ["The Centre plans to borrow ₹7.86 lakh crore through dated securities in the second half of 2026-27.",
    "The borrowing will be completed through 23 weekly auctions and includes Sovereign Green Bonds of ₹15,000 crore.",
    "The Ways and Means Advances (WMA) limit for the second half was fixed at ₹1.5 lakh crore."],
   [True, True, False],
   "H2 FY27 borrowing calendar",
   "The calendar released by the Finance Ministry on 25 September 2026 plans ₹7.86 lakh crore of dated-securities "
   "borrowing in October-March through 23 weekly auctions (tenors of 3 to 50 years), including ₹15,000 crore of "
   "Sovereign Green Bonds. The RBI fixed the WMA limit for H2 at ₹50,000 crore.",
   [fact("Centre to borrow Rs 7,86,000 crore in H2 of FY 2026-27 through 23 weekly auctions; includes SGrBs of Rs 15,000 "
         "crore; WMA limit for H2 Rs 50,000 crore", "e_h2_dt"),
    fact("Borrowing calendar released by the Ministry of Finance on Friday 25 Sep 2026: Rs 7.86 lakh crore through "
         "dated securities, 23 weekly auctions, maturities 3 to 50 years", "e_h2_dd")],
   why="Statement 3 is wrong: the WMA limit for H2 is ₹50,000 crore.",
   current=ca("2026-09-25"))

GS(T, INF, "Advanced", "the new Wholesale Price Index (WPI) series launched on 15 June 2026",
   ["It was released by the National Statistics Office of the Ministry of Statistics and Programme Implementation.",
    "Its base year is 2022-23, replacing 2011-12, and its basket has 957 items against 697 earlier.",
    "Producer Price Indices were launched alongside it, and the WPI is to continue for five years during the move to "
    "the PPI framework."],
   [False, True, True],
   "New WPI series",
   "The Ministry of Commerce and Industry (Office of the Economic Adviser, DPIIT) launched the revised WPI with base "
   "2022-23 on 15 June 2026; the first print showed 9.68% inflation for May 2026. The basket grew from 697 to 957 "
   "items. An Output PPI, a trial Input PPI and Service PPIs were released alongside, and the WPI will continue for "
   "five years while users move to the PPI framework.",
   [fact("New WPI series launched Monday 15 June 2026 by Ministry of Commerce and Industry; base 2022-23 replaces "
         "2011-12; items 697 to 957; WPI to continue for five years; PPIs launched", "e_wpi_new_fpj"),
    fact("Wholesale inflation 9.68% in May; new WPI series launched with 2022-23 base; Output PPI, trial Input PPI and "
         "Service PPIs", "e_wpi_new_ians"),
    fact("Office of the Economic Adviser, DPIIT press release on revised WPI series (2022-23=100)", "e_wpi_new_eaind")],
   why="Statement 1 is wrong: WPI is compiled by the Office of the Economic Adviser, DPIIT (Ministry of Commerce and "
       "Industry), not by MoSPI.",
   current=ca("2026-06-15"))

GS(T, GDP, "Advanced", "the revised Index of Industrial Production (IIP) series released in June 2026",
   ["Under the new series, industrial output grew 4.9% in April 2026.",
    "Manufacturing accounts for more than three-fourths of the index.",
    "The new base year 2022-23 replaces the base year 2004-05."],
   [True, True, False],
   "New IIP series",
   "The IIP was rebased to 2022-23 (from 2011-12) and the first release showed 4.9% growth for April 2026, with "
   "manufacturing up 6.2% and mining down about 5%. Manufacturing carries about 76% weight. The basket grew to 1,042 "
   "products in 463 item groups.",
   [fact("Industrial output grows 4.9% in April under new IIP series with 2022-23 base; manufacturing more than "
         "three-fourths of IIP; article dated 1 June 2026", "e_iip_fpj"),
    fact("IIP growth 4.9% in April 2026; new base 2022-23 replaces 2011-12; manufacturing about 76% weight; compiled by "
         "NSO, MoSPI", "e_iip_drishti")],
   why="Statement 3 is wrong: the previous IIP base year was 2011-12, not 2004-05.",
   current=ca("2026-06-01"))

# ====================================================================== Government Policies (5 / 0 / 5)
T = "Government Policies"
PC, RR = "Policy changes", "Regulatory reforms"

G(T, PC, "Basic",
  "Under the Supreme Court (Number of Judges) Amendment Ordinance of 16 May 2026, later replaced by an Act, what is the "
  "sanctioned strength of the Supreme Court including the Chief Justice of India?",
  ["38", "34", "37", "35"], "*",
  "Strength of the Supreme Court",
  "The ordinance, promulgated under Article 123 on 16 May 2026, amended Section 2 of the Supreme Court (Number of "
  "Judges) Act, 1956 to raise the number of judges other than the CJI from 33 to 37, i.e. 38 including the CJI. The "
  "Supreme Court (Number of Judges) Amendment Act, 2026 (assent 11 August 2026) replaced the ordinance. The previous "
  "increase was in 2019 (31 to 34).",
  ["Old: 33 + CJI = 34", "New: 37 + CJI = 38", "Ordinance 16 May 2026; Act assent 11 Aug 2026"],
  [fact("Ordinance notified 16 May 2026 under Article 123; strength raised from 33 to 37 judges excluding CJI (38 "
        "including CJI); last increase 2019", "e_sc_bb"),
   fact("Supreme Court (Number of Judges) Amendment Act, 2026: total strength including CJI from 34 to 38; assent "
        "11 August 2026", "e_monsoon_scc")],
  why="34 was the earlier strength; 37 is the number excluding the CJI; 35 is not a figure in the law.",
  current=ca("2026-05-16"))

G(T, RR, "Basic",
  "The Bankers' Books Evidence Act, 2026, which received Presidential assent on 13 August 2026 and recognises digital "
  "banking records as evidence, replaces a law of which year?",
  ["1891", "1872", "1949", "1934"], "*",
  "Bankers' Books Evidence Act, 2026",
  "The Bankers' Books Evidence Act, 2026 repeals and replaces the Bankers' Books Evidence Act, 1891. It recognises "
  "electronic and digital banking records as evidence. It received assent on 13 August 2026.",
  ["Old law: Bankers' Books Evidence Act, 1891", "New law: 2026 Act (assent 13 Aug 2026)"],
  [fact("Bankers' Books Evidence Act, 2026; Ministry of Finance; assent 13 August 2026; replaces the 1891 law; "
        "recognises electronic and digital banking records", "e_monsoon_scc"),
   fact("Lok Sabha passes Bankers' Books Evidence Bill 2026", "e_bbe_livelaw")],
  why="1872 is the Indian Evidence Act, 1949 the Banking Regulation Act and 1934 the RBI Act.",
  current=ca("2026-08-13"))

G(T, RR, "Basic",
  "The MSME Development (Amendment) Act, 2026 provides for mandatory routing of certain MSME receivable settlements "
  "through which platform?",
  ["TReDS (Trade Receivables Discounting System)", "ONDC (Open Network for Digital Commerce)",
   "GeM (Government e-Marketplace)", "Udyam Assist Platform"], "*",
  "MSME Development (Amendment) Act, 2026",
  "The Act, which received assent on 13 August 2026, amends the MSME Development framework with mandatory routing of "
  "certain receivable settlements through TReDS, tighter dispute-resolution timelines, stronger enforcement of awards "
  "and revised penalties.",
  ["Act: MSME Development (Amendment) Act, 2026 (assent 13 Aug 2026)", "Receivables: through TReDS"],
  [fact("MSME Development (Amendment) Act, 2026: mandatory routing of certain MSME receivable settlements through "
        "TReDS; assent 13 August 2026", "e_monsoon_scc")],
  why="ONDC is an e-commerce network, GeM a procurement portal and Udyam Assist a registration platform; none is "
      "named for receivables.",
  current=ca("2026-08-13"))

G(T, RR, "Basic",
  "At its board meeting of 19 June 2026, SEBI approved 'GARUDA'. What is it?",
  ["A green-channel mechanism to speed up the launch of schemes by Alternative Investment Funds",
   "A framework for intraday borrowing by mutual funds",
   "A new route for open-market buybacks through stock exchanges",
   "A quick process for transmission of small-value securities claims"], "*",
  "SEBI's GARUDA",
  "GARUDA stands for 'Green-Channel: AIF Rollout Upon Document Acknowledgement'. It lets AIFs begin fund-raising for "
  "Non-Accredited Investor schemes within 10 working days of filing their placement memorandum, instead of 30 days. "
  "The same meeting also approved MF intraday borrowing, stock-exchange buybacks and Quick Transmission Processing.",
  ["GARUDA: Green-Channel: AIF Rollout Upon Document Acknowledgement", "Fund-raising in 10 working days (from 30)"],
  [fact("SEBI board meeting 19 June 2026: GARUDA = Green-Channel: AIF Rollout Upon Document Acknowledgement, to speed "
        "AIF scheme launches; also MF intraday borrowing, exchange buybacks, QTP", "e_sebi_upstox"),
   fact("214th SEBI Board meeting of 19 June 2026: GARUDA mechanism for AIFs", "e_sebi_elp")],
  why="Intraday borrowing, exchange buybacks and Quick Transmission Processing were separate decisions of the same "
      "meeting.",
  current=ca("2026-06-19"))

G(T, PC, "Basic",
  "Parliament passed the Prevention of Insults to National Honour (Amendment) Bill, 2026 in July 2026. What does it "
  "extend the 1971 Act's protection to?",
  ["The National Song, Vande Mataram", "The National Emblem", "The National Calendar", "The National Pledge"], "*",
  "Prevention of Insults to National Honour (Amendment) Act, 2026",
  "The amendment extends to the National Song the protection that the 1971 Act gives the National Anthem: insulting "
  "Vande Mataram or obstructing its singing becomes punishable with imprisonment of up to three years, a fine, or "
  "both. The Rajya Sabha passed it on 29 July and the Lok Sabha on 30 July 2026; assent was on 6 August 2026.",
  ["Act amended: Prevention of Insults to National Honour Act, 1971", "New protection: National Song",
   "Penalty: up to 3 years, fine, or both"],
  [fact("Prevention of Insults to National Honour (Amendment) Act, 2026: extends similar protection to the National "
        "Song; up to three years; assent 6 August 2026", "e_monsoon_scc"),
   fact("Parliament passes bill criminalising insults to Vande Mataram; Lok Sabha passed it on 30 July 2026",
        "e_honour_om")],
  why="The bill concerns the National Song, not the Emblem, Calendar or Pledge.",
  current=ca("2026-07-30"))

GS(T, RR, "Advanced", "the Registration of Births and Deaths (Amendment) Act, 2026",
   ["It amends Section 13 of the Registration of Births and Deaths Act, 1969.",
    "Registration of a birth or death delayed beyond two years needs an order of a Judicial Magistrate of the First "
    "Class.",
    "Registration delayed by more than one year but less than two years needs an order of a Sessions Judge."],
   [True, True, False],
   "Delayed registration of births and deaths",
   "Act No. 12 of 2026 amends Section 13 of the 1969 Act. A registration delayed by one to two years needs an order of "
   "the District Magistrate, Sub-Divisional Magistrate or an Executive Magistrate authorised by the DM; one delayed "
   "beyond two years needs an order of a Judicial Magistrate of the First Class, after verification and payment of the "
   "fee. Assent was given on 6 August 2026.",
   [fact("Act No. 12 of 2026 amends Section 13 of the RBD Act, 1969; one to two years: DM/SDM/authorised Executive "
         "Magistrate; beyond two years: Judicial Magistrate of the First Class", "e_rbd_livelaw"),
    fact("Registration of Births and Deaths (Amendment) Act, 2026; assent 6 August 2026", "e_monsoon_scc")],
   why="Statement 3 is wrong: one-to-two-year delays need an executive magistrate's order (DM, SDM or authorised "
       "Executive Magistrate), not a Sessions Judge.",
   current=ca("2026-08-06"))

GS(T, RR, "Advanced", "the Public Examinations (Prevention of Unfair Means) Amendment Act, 2026",
   ["States and Union Territories must designate Special Fast Track Courts for offences under it.",
    "Investigations are generally to be completed within six months.",
    "Trials are to be held day-to-day and concluded within three months of the chargesheet."],
   [True, False, True],
   "Public examinations law",
   "The amendment (assent 31 July 2026) raises jail terms and fines, provides for Special Task Forces, requires States "
   "and UTs to designate Special Fast Track Courts, sets a general two-month limit for investigations, and requires "
   "day-to-day trials concluded within three months of the chargesheet.",
   [fact("Public Examinations (Prevention of Unfair Means) Amendment Act, 2026; assent 31 July 2026; Special Fast Track "
         "Courts; investigation generally within two months; trials within three months of chargesheet",
         "e_monsoon_scc")],
   why="Statement 2 is wrong: investigations are generally due within two months, not six.",
   current=ca("2026-07-31"))

GS(T, PC, "Advanced", "the Taxation and Other Laws (Amendment) Act, 2026, which received assent on 17 August 2026",
   ["It amends the Payment and Settlement Systems Act, 2007.",
    "It amends the Income-tax Act, 2025.",
    "It amends the Finance Act, 2026."],
   [True, True, True],
   "Taxation and Other Laws (Amendment) Act, 2026",
   "The Act amends three laws, the Payment and Settlement Systems Act, 2007, the Income-tax Act, 2025 and the Finance "
   "Act, 2026, to support digital payments, refine income-tax provisions and give targeted incentives, including to "
   "specified sectors and foreign investors.",
   [fact("Taxation and Other Laws (Amendment) Act, 2026; assent 17 August 2026; amends Payment and Settlement Systems "
         "Act 2007, Income-tax Act 2025 and Finance Act 2026", "e_monsoon_scc")],
   why="All three laws are amended by the Act.",
   current=ca("2026-08-17"))

GS(T, RR, "Advanced", "the decisions of the SEBI board meeting held on 19 June 2026",
   ["The meeting was chaired by Madhabi Puri Buch.",
    "Open-market buybacks through the stock exchange route were reintroduced with effect from 1 August 2026.",
    "Quick Transmission Processing covers claims of up to ₹10,000 for physical securities and ₹30,000 for demat "
    "securities."],
   [False, True, True],
   "SEBI reforms, June 2026",
   "The 214th board meeting, chaired by Tuhin Kanta Pandey, reintroduced open-market buybacks through exchanges from "
   "1 August 2026 (to be completed within 66 working days), created Quick Transmission Processing for small claims "
   "(₹10,000 physical, ₹30,000 demat), allowed MF intraday borrowing and approved the GARUDA green channel for AIFs.",
   [fact("SEBI board 19 June 2026, chairman Tuhin Kanta Pandey; exchange buybacks from 1 August 2026; QTP up to "
         "₹10,000 physical and ₹30,000 demat", "e_sebi_upstox"),
    fact("214th SEBI Board meeting, 19 June 2026: re-introduction of the stock exchange buy-back route",
         "e_sebi_elp")],
   why="Statement 1 is wrong: the meeting was chaired by SEBI Chairman Tuhin Kanta Pandey.",
   current=ca("2026-06-19"))

GS(T, PC, "Advanced", "the changes to the Press Note 3 (2020) FDI rules approved by the Union Cabinet on 10 March 2026",
   ["Investments with up to 10% non-controlling beneficial ownership from entities of land-border countries are "
    "permitted under the automatic route.",
    "Proposals in specified manufacturing sectors get a 90-day approval timeline.",
    "Majority ownership and control of the investee company must remain with resident Indian citizens or "
    "Indian-owned entities."],
   [True, False, True],
   "Press Note 3 relaxation",
   "Press Note 3 of April 2020 required government approval for any FDI from countries sharing a land border with "
   "India. On 10 March 2026 the Cabinet allowed up to 10% non-controlling beneficial ownership through the automatic "
   "route (with reporting to DPIIT) and a 60-day approval window for specified manufacturing sectors such as capital "
   "goods, electronic components and polysilicon, with majority ownership and control staying with resident Indians.",
   [fact("Cabinet press release dated 10.03.2026: up to 10% non-controlling beneficial ownership from land-border "
         "countries under automatic route; 60-day timeline for specified manufacturing sectors", "e_fdi_taxmann"),
    fact("Press Note 3 of 2020; 10% route only for non-controlling investments; majority ownership and control with "
         "resident Indian citizens or Indian-owned entities; 60-day fast-track for manufacturing", "e_fdi_5p")],
   why="Statement 2 is wrong: the fast-track approval timeline is 60 days.",
   current=ca("2026-03-10"))

# ====================================================================== Business and Corporate News (2 / 0 / 0)
T = "Business and Corporate News"
MA = "Mergers and acquisitions"

G(T, MA, "Basic",
  "On 24 December 2025 Bharti Enterprises and Warburg Pincus announced that they would together acquire a 49% stake in "
  "the Indian arm of which home-appliance company?",
  ["Haier", "LG Electronics", "Whirlpool", "Samsung"], "*",
  "Haier India deal",
  "Bharti Enterprises and Warburg Pincus announced a strategic investment under which they will jointly hold 49% of "
  "Haier India; Haier Group keeps 49% and the management team 2%. Haier India, set up in 2003, makes appliances at "
  "Pune and Greater Noida.",
  ["Buyers: Bharti Enterprises + Warburg Pincus (49%)", "Haier Group retains 49%; management 2%"],
  [fact("Bharti Enterprises and Warburg Pincus announce strategic investment in Haier India, 24 Dec 2025; together 49%; "
        "Haier Group 49%; management 2%", "e_haier_wp"),
   fact("Bharti, Warburg Pincus pick up 49% stake in Haier India", "e_haier_week")],
  why="The deal is for Haier India, not LG, Whirlpool or Samsung.",
  current=ca("2025-12-24"))

G(T, MA, "Basic",
  "IT services company Coforge announced on 26 December 2025 that it would acquire which US-based engineering services "
  "firm in an all-stock deal valued at about USD 2.35 billion?",
  ["Encora", "Confluent", "Nagarro", "Endava"], "*",
  "Coforge-Encora deal",
  "Coforge agreed to buy Encora, founded in Silicon Valley, for an enterprise value of about USD 2.35 billion through a "
  "share swap: it will issue 93.8 million shares at ₹1,815.91 each (about ₹17,032 crore), giving Encora's shareholders "
  "about 21.25% of Coforge's expanded equity.",
  ["Acquirer: Coforge", "Target: Encora (US)", "All-stock, about USD 2.35 billion"],
  [fact("Coforge to acquire US-based Encora in $2.35 billion all-stock deal; 26 Dec 2025; 93.8 million shares at "
        "Rs 1,815.91; sellers to hold 21.25%", "e_coforge_ians")],
  why="Confluent was bought by IBM and Nagarro was the target of Persistent Systems; Endava was not part of this deal.",
  current=ca("2025-12-26"))


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
        verified_by = ["ai:author-solve"]
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
batch = {
    "schema_version": "1.0",
    "batch_id": BATCH,
    "created_at": TODAY,
    "notes": "BATCH_005 General Awareness part: 150 original questions. Current-affairs topics (National and "
             "International Current Affairs, Appointments, Awards, Sports, Summits, Economic Affairs, Business) test "
             "events dated 2025-11-01 to 2026-11-04, with event dates from the sources and review_by 2027-05-05. "
             "Other time-sensitive facts also carry current_affairs dates. No fact or event tested in BATCH_000 to "
             "BATCH_004 GA is tested again. Fact checks dated 2026-11-05; verified_by says whether each question's "
             "sources were opened (web:fact-check) or confirmed only in search results (web:search-confirmed). "
             "Pending human review.",
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / f"{BATCH}_GA.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions; keys {dict(sorted(keys.items()))})")
