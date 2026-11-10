"""Package GA_pkg1: writes batches/parts/frag/BATCH_010_GA_pkg1.json, the 149 General Awareness questions of
BATCH_010 (all GA topics of the final batch; IDs BANK_GA_001352 to BANK_GA_001500; no stimuli).

Same structure as tools/batch_009/ga.py: the questions were drafted in helper slices (each with an event log and a
cross-slice repeat check) and assembled here. Current-affairs topics (National and International Current Affairs,
Appointments, Awards, Sports, Summits, Economic Affairs, Business) test events dated 2025-11-01 to 2026-11-04 with
event dates from the sources; every such question carries current_affairs {event_date, review_by 2027-05-05}. Other
time-sensitive facts (schemes, policies, reports, books, current heads) carry current_affairs too. Where a source gives
no exact day, ca(..., inferred=reason) records it and the list is printed and written into the fragment notes.

Every question has fact_checks, and at least one source per question is an official/primary site or a major news
outlet (never only Wikipedia or an exam-prep site). Each URL is marked OPENED (fetched and read, giving
"web:fact-check") or SEARCH (confirmed only from search-result text, giving "web:search-confirmed"). checked_on is the
date the page was actually checked. Sites that refused a fetch were not worked around.
Explanations and why_others_wrong state only facts backed by the listed sources, or stay neutral.

All earlier GA stems (BATCH_000 sample, BATCH_001_GA to BATCH_009_GA, 1,351 questions) and the Banking subject's BFA
stems were read first; no fact or event tested there is tested again, and no event is used twice in this package.

Statement questions have their key fixed by the statements (computed from truth values); other questions are written
with the correct option first and answer "*", and are then placed so that keys are balanced A to D. The build asserts
the package quota per (topic, difficulty), the ID range, the stimulus start, the key balance and the CA date window.
ai:independent-check is given only to questions whose exact stem is in BLIND_MATCHED (a fresh solver's key-free
answers matched the key and the question was not changed afterwards); all others carry ai:self-recheck.

    python tools/packages/GA_pkg1.py
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
BATCH = "BATCH_010"
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
# first 120 characters of every stem that a fresh key-free solver answered correctly (unchanged afterwards)
BLIND_MATCHED = set([
    "On 27 September 2026, Union Home Minister Amit Shah flagged off India's first LNG-powered train, a dual-fuel train runni",
    "For the assembly elections of 2026 in Assam, Kerala, Puducherry, Tamil Nadu and West Bengal, the Election Commission ext",
    "In May 2026, which regulator stated that no cosmetic may be used as an injection by consumers, professionals or aestheti",
    "President Droupadi Murmu attended the Muria Durbar at Jagdalpur on 23 October 2026, a royal-era gathering in which tradi",
    "'Aayakar Sindhu', a new office complex of the Income Tax Department inaugurated by Finance Minister Nirmala Sitharaman o",
    "In July 2026, which state's government announced that it would set up India's first dedicated Employment Cell for Agnive",
    "Consider the following statements about ICGS Samudra Pratap:\n1. It was commissioned by Defence Minister Rajnath Singh on",
    "Consider the following statements about the highway project approved by the Cabinet Committee on Economic Affairs on 10 ",
    "Who was chosen by Iran's Assembly of Experts in March 2026 as the country's new Supreme Leader, after Ayatollah Ali Kham",
    "In September 2026, which country announced that Indian tourists holding ordinary passports could enter visa-free and sta",
    "In Israel's Knesset election of 27 October 2026, Likud emerged as the largest party, while neither bloc reached the 61-s",
    "During Defence Minister Rajnath Singh's visit to Colombo in September 2026, India and Sri Lanka exchanged an MoU to upgr",
    "In the first Security Council straw poll for choosing the next UN Secretary-General, held on 30 July 2026, which candida",
    "In his speech at the Ile Longue submarine base on 2 March 2026, French President Emmanuel Macron ordered an increase in ",
    "WMO's El Nino update of 8 October 2026 forecast an October-December Nino 3.4 anomaly of about +3.7 deg C, above the prev",
    "In May 2026 the Africa Centres for Disease Control and Prevention reported a new Ebola outbreak that had killed 65 peopl",
    "US President Donald Trump concluded a three-day visit to China on 15 May 2026, holding talks with President Xi Jinping. ",
    "In May 2026 the United States announced that Israel and Lebanon had agreed to extend the cessation of hostilities of 16 ",
    "The Boma-Badingilo Migratory Landscape was added to UNESCO's World Heritage List in July 2026 at the World Heritage Comm",
    "The PM SHRI scheme (PM Schools for Rising India), approved by the Union Cabinet on 7 September 2022 with an outlay of Rs",
    "Under the Pradhan Mantri Matru Vandana Yojana as revised under Mission Shakti, how much cash incentive is given for a se",
    "The Namo Drone Didi scheme, with an outlay of Rs 1,261 crore, aims to provide agricultural drones to how many selected w",
    "The National Green Hydrogen Mission, approved by the Union Cabinet on 4 January 2023, aims to develop green hydrogen pro",
    "The Vibrant Villages Programme-II, approved by the Union Cabinet on 4 April 2025 with an outlay of Rs 6,839 crore, cover",
    "Mission Mausam, approved by the Union Cabinet on 11 September 2024 with an outlay of Rs 2,000 crore over two years to ma",
    "The e-Shram portal, the national database of unorganised workers, completed five years on 26 August 2026. About how many",
    "In January 2026 the government provisionally selected five companies, including Godrej & Boyce and Kirloskar Pneumatic, ",
    "The PM GatiShakti National Master Plan for multimodal connectivity, launched on 13 October 2021, runs on a GIS platform ",
    "Consider the following statements about the National Critical Mineral Mission approved by the Union Cabinet in January 2",
    "Consider the following statements about the IndiaAI Mission approved by the Union Cabinet in March 2024:\n1. Its approved",
    "Consider the following statements about the Deep Ocean Mission of the Ministry of Earth Sciences:\n1. It was approved wit",
    "Consider the following statements about the Green Energy Corridor Phase-III approved by the Union Cabinet on 30 Septembe",
    "Consider the following statements about PM-PRANAM (PM Programme for Restoration, Awareness, Nourishment and Amelioration",
    "Consider the following statements about the Anusandhan National Research Foundation (ANRF):\n1. It was set up under an Ac",
    "Consider the following statements about the Sagarmala Programme:\n1. It was launched in 2015 to promote port-led developm",
    "In May 2026, the Bank for International Settlements announced that the Governor of the Bank of Japan would chair its Com",
    "Kenyan diplomat Martin Kimani, Kenya's Permanent Representative to the UN from 2020 to 2024, was appointed by the UN Sec",
    "Ramiz Alakbarov, appointed by the UN Secretary-General in October 2026 as Assistant Secretary-General for Safety and Sec",
    "Dr R. Brian Langrin took charge in August 2026 as Governor of which central bank, succeeding Richard Byles?",
    "In November 2026, the National Payments Corporation of India set up a wholly owned technology subsidiary, NPCI Tech Solu",
    "In October 2026 the UN Secretary-General appointed Russian diplomat Gleb Desyatnikov as Assistant Secretary-General for ",
    "Consider the following statements about the 21st session of the UNIDO General Conference:\n1. It was held in Vienna, Aust",
    "Which show won the Tony Award for Best Musical at the 79th Tony Awards held on 7 June 2026?",
    "The Prix Goncourt 2026, France's top literary prize, was awarded on 3 November 2026 to Philippe Jaenada for which novel,",
    "Which institution was selected in the institutional category for the Subhash Chandra Bose Aapda Prabandhan Puraskar 2026",
    "American astronaut Christina Koch, praised by the jury as the first woman to travel far enough to escape Earth's magneti",
    "The 2026 Balzan Prize for Humanity, Peace and Fraternity among Peoples, announced on 7 September 2026, was awarded to th",
    "Which Hindi writer received the IFFCO Sahitya Samman 2025, presented at Kamani Auditorium, New Delhi, on 30 December 202",
    "Which film won the Golden Peacock for Best Feature Film at the 56th International Film Festival of India (IFFI), which c",
    "At the Rashtriya Vigyan Puraskar 2025 ceremony at Rashtrapati Bhavan on 23 December 2025, the Vigyan Ratna was conferred",
    "The Zayed Sustainability Prize 2026, which awarded about US$5.9 million to 11 organisations and high schools across six ",
    "India's women's football team won the SAFF Championship 2026 at Madgaon, Goa, on 6 June 2026 for a record sixth title. W",
    "Which state was crowned overall champion of the Ladakh leg of the Khelo India Winter Games 2026, which concluded at the ",
    "Which team won its first World Series title on 28 October 2026, beating the Tampa Bay Rays 4-1 in Game 5?",
    "Which club won the UEFA Europa League 2025-26, beating SC Freiburg 3-0 in the final in Istanbul on 20 May 2026?",
    "Who won the PGA Championship 2026 at Aronimink Golf Club, ending on 17 May 2026, his first major title?",
    "Which club won the FA Cup 2025-26, beating Chelsea 1-0 in the final at Wembley on 16 May 2026?",
    "In which city did India's men's 50m pistol team of Saurabh Chaudhary, Ravinder Singh and Amanpreet Singh win gold at the",
    "Rumesh Pathirage won the javelin title at the Diamond League Final 2026 in Brussels with a throw of 89.04 m, becoming th",
    "In September 2026 Satwiksairaj Rankireddy and Chirag Shetty became the first Indians to win which BWF Super 750 tourname",
    "Consider the following statements about the FIDE Candidates Tournament 2026 (open section):\n1. It was held in Toronto, C",
    "Consider the following statements about the 154th Open Championship (golf), won by Ryan Fox in July 2026:\n1. It was play",
    "Consider the following statements about the Irani Cup match of October 2026:\n1. Rest of India beat Jammu and Kashmir by ",
    "Consider the following statements about India's women wrestlers at the 2026 Senior World Wrestling Championships:\n1. Kaj",
    "Consider the following statements about the Giro d'Italia 2026:\n1. Jonas Vingegaard won it, the race finishing in Rome o",
    "Consider the following statements about the Laver Cup 2026:\n1. It was held in San Francisco.\n2. Team Europe won 13-5, wi",
    "Consider the following statements about India at the ISSF Junior World Championship 2026:\n1. It was held in Suhl, German",
    "Consider the following statements about the 2026 Stanley Cup Final (ice hockey):\n1. The Carolina Hurricanes beat the Veg",
    "The 3rd National Space Day, marking the Chandrayaan-3 landing, was celebrated on 23 August 2026 with its main event in A",
    "Desertification and Drought Day 2026 (17 June), linked to the International Year of Rangelands and Pastoralists, had its",
    "WHO's slogan for World Blood Donor Day 2026, inspired by a quote of the Persian poet Rumi, was:",
    "World Cities Day 2026 (31 October), which concludes UN-Habitat's 'Urban October', had its global observance in which cit",
    "'The Everlasting', which won the Hugo Award for Best Novel in 2026 at the 84th World Science Fiction Convention in Anahe",
    "'A Century of Service: The RSS in 100 Acts of Seva', released by Vice-President C. P. Radhakrishnan in New Delhi in Sept",
    "'Sankalp Se Siddhi ka Modi Yug', a book released by Vice-President C. P. Radhakrishnan in August 2026, was written by wh",
    "Omar Musa won Australia's Miles Franklin Literary Award 2026 for which novel, about siblings who return to Malaysian Bor",
    "On 20 January 2026, Vice-President C. P. Radhakrishnan inaugurated the Mahadev Desai Library extension and released the ",
    "Consider the following statements about the Orwell Prize for Political Writing 2026:\n1. It was won by Sam Dalrymple's 'S",
    "Consider the following statements about the Walter Scott Prize for Historical Fiction 2026:\n1. It was won by Alice Jolly",
    "Consider the following statements about the Kirkus Prize 2026, announced on 7 October 2026:\n1. The fiction prize went to",
    "Diene Keita of Guinea was appointed by the UN Secretary-General in August 2025 as the Executive Director of which UN bod",
    "Robert Floyd began his second four-year term as Executive Secretary of the Preparatory Commission for the Comprehensive ",
    "The Green Climate Fund, whose Executive Director Mafalda Duarte was selected by its Board in 2023, is headquartered in w",
    "Consider the following statements about the special session of the UNAIDS Programme Coordinating Board held in October 2",
    "The Living Planet Report 2026, released in October 2026, found an average 73% decline in monitored wildlife populations ",
    "In Swachh Survekshan 2024-25, presented by President Droupadi Murmu on 17 July 2025, which city was named the cleanest b",
    "The Global Report on Food Crises 2026, which found that 266 million people in 47 countries faced acute food insecurity i",
    "In the Global Startup Ecosystem Report (GSER) 2026 of Startup Genome, released in June 2026, what was Bengaluru's global",
    "In the India Justice Report 2025, which ranks states on police, judiciary, prisons and legal aid, which state was ranked",
    "The Annual Status of Education Report (ASER) 2024, released in January 2025, found the highest Class 3 reading levels in",
    "According to WHO's World Malaria Report 2025, released in December 2025, about what share of the estimated malaria cases",
    "The April 2026 edition of the 'Fiscal Monitor', which projected global public debt to reach 100% of GDP by 2029, is a tw",
    "The World Bank's World Development Report 2026, released on 4 August 2026, is devoted to which theme?",
    "According to Ember's Global Electricity Review 2026, released on 21 April 2026, how much solar capacity did India deploy",
    "Consider the following statements about the NFHS-6 (2023-24) India fact sheets released in May 2026:\n1. India's total fe",
    "Consider the following statements about UNODC's World Drug Report 2026, released on 26 June 2026:\n1. An estimated 331 mi",
    "On 16 June 2026 the Bank of Japan raised its policy interest rate to its highest level since 1995. To what level?",
    "On 16 June 2026 the Reserve Bank of Australia kept its cash rate unchanged for the first time in 2026, after three strai",
    "The final HSBC India Manufacturing PMI for September 2026, compiled by S&P Global, showed the strongest improvement in s",
    "According to data released on 1 July 2026, India's gross GST collections for June 2026 grew by about 13.9% year on year ",
    "On 28 October 2026 the Bank of Canada raised its policy rate by 25 basis points, its first increase in more than three y",
    "At the GST Council meeting chaired in New Delhi on 8 October 2026, tax officers' powers of arrest were removed. To what ",
    "In its India Development Update of 9 April 2026, what real GDP growth did the World Bank project for India for FY27, cit",
    "In its Economic Outlook of June 2026, what real GDP growth did the OECD project for India for FY2026-27?",
    "At its meeting ending on 29 July 2026, the US Federal Open Market Committee kept the federal funds rate at 3.50-3.75%. W",
    "At its decision of 30 July 2026, the Bank of England's Monetary Policy Committee held Bank Rate at 3.75% by a 6-3 vote. ",
    "Consider the following statements about India's wholesale price (WPI) inflation for March 2026, released on 15 April 202",
    "Consider the following statements about India's Index of Industrial Production (IIP) for June 2026, released on 28 July ",
    "Consider the following statements about the European Central Bank's monetary policy decision of 29 October 2026:\n1. The ",
    "Consider the following statements about India's GST collections for August 2026, released on 1 September 2026:\n1. Gross ",
    "Consider the following statements about the Index of Core Industries for August 2026:\n1. Core sector output grew 4.8% in",
    "Consider the following statements about India's net direct tax collections for 2026-27 up to 14 October 2026:\n1. Net col",
    "Consider the following statements about the UN's World Economic Situation and Prospects mid-2026 update, released on 19 ",
    "On 30 June 2026 the Ministry of Tourism signed an MoU with which technology company to strengthen digital promotion of I",
    "In August 2026 Inox Clean Energy completed the acquisition of Vena Energy's India platform for about Rs 6,000 crore. Fro",
    "In August 2026 Tata Steel bought an additional 23% stake for about Rs 335 crore in a company, raising its holding to 74%",
    "In August 2026 Piramal Pharma completed the acquisition of a 74% controlling stake in which company, for a cash consider",
    "Hearzap completed in August 2026 the acquisition of the Indian hearing healthcare business of which company, expanding i",
    "In August 2026 Waaree bought a stake in Eppeltone. What does Eppeltone mainly make?",
    "In September 2026 Kalyani Strategic Systems signed an MoU with which company to study a production facility in India and",
    "France's Naval Group signed an MoU on 18 September 2026 with which Indian company to cooperate on naval technology, ship",
    "Tembo Global Industries signed an MoU in September 2026 with Belgium's Lachaussee to set up what in India, valued at abo",
    "What is the currency of Ghana?",
    "What is the currency of Rwanda, whose capital is Kigali?",
    "Kuno National Park, where cheetahs brought from Namibia were released on 17 September 2022 under Project Cheetah, is loc",
    "The Tadoba-Andhari Tiger Reserve, described as Maharashtra's oldest and largest national park, is located in which distr",
    "Which town was designated the headquarters of the merged Union Territory of Dadra and Nagar Haveli and Daman and Diu, wh",
    "The Union Territory of Lakshadweep, with its capital at Kavaratti, was known by which name until 1973?",
    "The Salal hydroelectric power station of NHPC in Reasi district, Jammu and Kashmir, whose reservoir NHPC began desilting",
    "Consider the following statements about the Srisailam Dam:\n1. It is built across the Krishna in a gorge of the Nallamala",
    "Consider the following statements about the Polavaram Irrigation Project:\n1. It is being built on the Krishna river.\n2. ",
    "Consider the following statements about Nagarhole National Park (Rajiv Gandhi National Park):\n1. It spreads over Kodagu ",
    "Consider the following statements about the Tungabhadra Dam:\n1. It was completed in 1953 as a joint project of the erstw",
    "Consider the following statements about the history of Tripura:\n1. It became a Union Territory on 1 November 1956.\n2. It",
    "Consider the following statements about Poland's currency:\n1. Poland adopted the euro in 2014.\n2. The zloty is issued by",
])


# ###################################################################### part: nat (National CA, Government Policies, Summits, Important Days)
U.update({
    "nat_lng_air": ("https://newsonair.gov.in/union-minister-amit-shah-flags-off-countrys-first-lng-powered-train-from-sabarmati/",
                    OPENED, "2026-11-06"),
    "nat_pb_air": ("https://newsonair.gov.in/election-commission-extends-postal-ballot-facility-to-electors-above-85-years-"
                   "and-pwds/", OPENED, "2026-11-06"),
    "nat_cos_air": ("https://newsonair.gov.in/govt-prohibits-use-of-cosmetic-as-injection-by-consumers-professionals-"
                    "aesthetic-clinics/", OPENED, "2026-11-06"),
    "nat_muria_air": ("https://newsonair.gov.in/president-murmu-to-attend-historic-muria-durbar-in-bastar/", OPENED,
                      "2026-11-06"),
    "nat_ayk_air": ("https://newsonair.gov.in/fm-nirmala-sitharaman-inaugurates-new-income-tax-department-office-complex-"
                    "aayakar-sindhu/", OPENED, "2026-11-06"),
    "nat_sp_air": ("https://newsonair.gov.in/indian-coast-guard-inducts-first-pollution-control-vessel-at-goa-shipyard-"
                   "limited/", OPENED, "2026-11-06"),
    "nat_sp_air2": ("https://www.newsonair.gov.in/minister-rajnath-singh-commissions-icgs-first-indigenously-designed-built-"
                    "pollution-control-vessel-samudra-pratap-in-goa", SEARCH, "2026-11-06"),
    "nat_sp_print": ("https://theprint.in/india/rajnath-singh-commissions-icgs-pollution-control-vessel-samudra-pratap-in-"
                     "goa/2818874", OPENED, "2026-11-07"),
    "nat_sp_goan": ("https://www.thegoan.net/goa-news/﻿defence-minister-rajnath-singh-commissions-icgs-samudra-pratap-at-"
                    "goa-shipyard/141463.html", OPENED, "2026-11-07"),
})

NCA = "National Current Affairs"

G(NCA, "States and UTs", "Basic",
  "On 27 September 2026, Union Home Minister Amit Shah flagged off India's first LNG-powered train, a dual-fuel train "
  "running on diesel and liquefied natural gas. From which railway station was it flagged off?",
  ["Sabarmati (Ahmedabad)", "Surat", "Vadodara", "Rajkot"], "*",
  "Railways: cleaner fuels",
  "On Sunday, 27 September 2026, Amit Shah flagged off the country's first LNG-powered train from Sabarmati railway "
  "station in Ahmedabad, Gujarat. It is a dual-fuel train that runs on diesel and LNG and was presented as a step "
  "towards cleaner rail energy. He also launched railway projects worth more than ₹1,500 crore.",
  ["First LNG-powered (diesel + LNG dual-fuel) train", "Flagged off 27 Sep 2026 by Amit Shah", "Sabarmati, Ahmedabad"],
  [fact("Amit Shah flagged off the country's first LNG-powered (dual-fuel diesel and LNG) train from Sabarmati railway "
        "station, Ahmedabad, on Sunday 27 September 2026", "nat_lng_air")],
  why="The source names Sabarmati station in Ahmedabad; the other stations are not mentioned.",
  current=ca("2026-09-27"))

G(NCA, "Government decisions", "Intermediate",
  "For the assembly elections of 2026 in Assam, Kerala, Puducherry, Tamil Nadu and West Bengal, the Election "
  "Commission extended home postal voting to electors above 85 years and persons with disabilities. Which form must "
  "such an elector submit, within five days of the election notification, to use this facility?",
  ["Form 12D", "Form 6", "Form 7", "Form 8"], "*",
  "Elections: postal ballot",
  "News On AIR reported on 19 March 2026 that electors above 85 years and persons with disabilities could vote by "
  "postal ballot from home in the assembly polls of Assam, Kerala, Puducherry, Tamil Nadu and West Bengal and in "
  "by-elections in six states. They had to apply in Form 12D within five days of the election notification, with the "
  "help of the Booth Level Officer; polling teams then visit their homes to collect the votes.",
  ["Who: electors 85+ and PwDs", "Apply: Form 12D, within 5 days of notification, via BLO",
   "Polling team collects the vote at home"],
  [fact("Electors above 85 and PwDs to apply through Form 12D within five days of the election notification, with BLO "
        "help; assembly polls in Assam, Kerala, Puducherry, Tamil Nadu and West Bengal (AIR, 19 March 2026)",
        "nat_pb_air")],
  why="The source names Form 12D for this facility; the other forms are not the postal-ballot application.",
  current=ca("2026-03-19"))

G(NCA, "Government decisions", "Intermediate",
  "In May 2026, which regulator stated that no cosmetic may be used as an injection by consumers, professionals or "
  "aesthetic clinics, since cosmetics under the Cosmetics Rules, 2020 are meant only for external application?",
  ["Central Drugs Standard Control Organisation (CDSCO)", "Food Safety and Standards Authority of India (FSSAI)",
   "Bureau of Indian Standards (BIS)", "National Pharmaceutical Pricing Authority (NPPA)"], "*",
  "Health regulation: cosmetics",
  "On 21 May 2026 the CDSCO prohibited the use of any cosmetic as an injection by consumers, professionals and "
  "aesthetic clinics. It said cosmetics are meant only to be rubbed, poured, sprinkled or sprayed on the body for "
  "cleansing, beautifying or altering appearance, and that their manufacture and import for sale are governed by the "
  "Cosmetics Rules, 2020. Injecting cosmetics, using them for treatment or making misleading label claims are "
  "violations.",
  ["Regulator: CDSCO", "Cosmetics = external application only", "Injection use by anyone prohibited (21 May 2026)"],
  [fact("CDSCO prohibits use of any cosmetic as an injection by consumers, professionals and aesthetic clinics; "
        "cosmetics only for external application; Cosmetics Rules, 2020 (AIR, 21 May 2026)", "nat_cos_air")],
  why="The source names the CDSCO; FSSAI, BIS and NPPA are not mentioned in this decision.",
  current=ca("2026-05-21"))

G(NCA, "States and UTs", "Intermediate",
  "President Droupadi Murmu attended the Muria Durbar at Jagdalpur on 23 October 2026, a royal-era gathering in which "
  "traditional community leaders such as Manjhis and Chalkis meet officials. The Durbar is part of which celebration?",
  ["Bastar Dussehra", "Hornbill Festival", "Rajim Kumbh", "Hampi Utsav"], "*",
  "States: Chhattisgarh, tribal traditions",
  "News On AIR reported on 23 October 2026 that President Murmu would attend the historic Muria Durbar in Jagdalpur, "
  "Chhattisgarh, part of the Bastar Dussehra celebrations. The Durbar dates back to Bastar's royal era and brings "
  "traditional leaders such as Manjhis and Chalkis together with officials to discuss local issues. She was also to "
  "pray at the Maa Danteshwari temple.",
  ["Muria Durbar: Jagdalpur (Bastar), Chhattisgarh", "Part of Bastar Dussehra", "President attended, 23 Oct 2026"],
  [fact("President Murmu to attend the Muria Durbar in Jagdalpur, part of the Bastar Dussehra celebrations; royal-era "
        "gathering of Manjhis, Chalkis and officials (AIR, 23 October 2026)", "nat_muria_air")],
  why="The source links the Muria Durbar to Bastar Dussehra; the other festivals are not mentioned.",
  current=ca("2026-10-23"))

G(NCA, "States and UTs", "Intermediate",
  "'Aayakar Sindhu', a new office complex of the Income Tax Department inaugurated by Finance Minister Nirmala "
  "Sitharaman on 26 July 2026 (Kargil Vijay Diwas), is located in which city?",
  ["Mumbai (Nariman Point)", "Chennai", "Kochi", "Visakhapatnam"], "*",
  "Government buildings: tax administration",
  "On 26 July 2026 Nirmala Sitharaman inaugurated 'Aayakar Sindhu', the Income Tax Department's new office complex at "
  "Nariman Point, Mumbai, in the presence of CBDT Chairperson Ravi Agrawal and the Principal Chief Commissioner of "
  "Income Tax, Mumbai.",
  ["Aayakar Sindhu = I-T office complex", "Nariman Point, Mumbai", "Inaugurated 26 July 2026"],
  [fact("FM Sitharaman inaugurated the new Income Tax Department office complex 'Aayakar Sindhu' at Nariman Point, "
        "Mumbai, on Kargil Vijay Diwas; CBDT Chairperson Ravi Agrawal present (AIR, 26 July 2026)", "nat_ayk_air")],
  why="The source places the complex at Nariman Point, Mumbai; the other cities are not mentioned.",
  current=ca("2026-07-26"))

GS(NCA, "Defence", "Advanced", "ICGS Samudra Pratap",
   ["It was commissioned by Defence Minister Rajnath Singh on 5 January 2026 at Goa Shipyard Limited.",
    "It is the first of two pollution control vessels built by Goa Shipyard Limited for the Indian Coast Guard, with "
    "over 60% indigenous content.",
    "It will be based at Visakhapatnam under the Coast Guard Region (East)."],
   [True, True, False],
   "Defence: Coast Guard ships",
   "Rajnath Singh commissioned ICGS Samudra Pratap at Goa Shipyard Limited, Goa, on 5 January 2026. The vessel, which "
   "had been inducted at GSL in December 2025, is the first of two pollution control vessels built by GSL for the "
   "Coast Guard and India's first indigenously designed and built pollution control vessel, with over 60% indigenous "
   "content. It is based at Kochi under the Coast Guard Region (West), so statement 3 is wrong.",
   [fact("ICG inducts first pollution control vessel 'Samudra Pratap' at Goa Shipyard Limited; indigenously designed "
         "and built; over 60% indigenous content (AIR, 23 Dec 2025)", "nat_sp_air"),
    fact("Rajnath Singh commissions ICG's first indigenously designed and built pollution control vessel Samudra Pratap "
         "in Goa (AIR, 5 January 2026)", "nat_sp_air2"),
    fact("Rajnath Singh commissioned the vessel at Goa Shipyard Limited, Vasco, on Monday (PTI, 5 Jan 2026); over 60 per "
         "cent indigenous content", "nat_sp_print"),
    fact("Samudra Pratap is the first of two Goa-built pollution control vessels; based at Kochi under the operational "
         "control of the Commander, Coast Guard Region (West)", "nat_sp_goan")],
   why="Statement 3 is wrong: the ship is based at Kochi under the Coast Guard Region (West).",
   current=ca("2026-01-05"))


# ====================================================================== Summits and Conferences
U.update({
    "sum_brics_agri_air": ("https://newsonair.gov.in/brics-agriculture-ministers-conference-begins-in-indoremadhya-pradesh/",
                           OPENED, "2026-11-07"),
})

GS("Summits and Conferences", "G20, BRICS, SCO and others", "Advanced",
   "the BRICS Agriculture Ministers' Conference held in June 2026",
   ["It was held in Indore, Madhya Pradesh, under India's BRICS chairship.",
    "Union Agriculture Minister Shivraj Singh Chouhan welcomed the delegates.",
    "India was represented at it by Commerce and Industry Minister Piyush Goyal."],
   [True, True, False],
   "BRICS ministerial meetings under India's 2026 chairship",
   "The BRICS Agriculture Ministers' Conference began in Indore, Madhya Pradesh, on 12 June 2026 under India's BRICS "
   "presidency, with BRICS members and partner countries taking part; AIR described its focus as food security through "
   "small farmers, women and youth. Union Agriculture and Farmers' Welfare Minister Shivraj Singh Chouhan welcomed the "
   "delegates, so statement 3 (Piyush Goyal) is wrong. He noted that food production had reached nearly 376 million "
   "tonnes and that about 87% of India's farmers are small or marginal.",
   [fact("BRICS Agriculture Ministers' Conference began in Indore, Madhya Pradesh, under India's BRICS presidency; theme "
         "'Food Security for the Future through Small Farmers, Women and Youth'; Agriculture Minister Shivraj Singh "
         "Chouhan welcomed delegates (AIR, 12 June 2026)", "sum_brics_agri_air")],
   why="Statement 3 is wrong: India was represented by Agriculture Minister Shivraj Singh Chouhan.",
   current=ca("2026-06-12"))


# ====================================================================== Important Days
U.update({
    "day_wwd_medwet": ("https://medwet.org/world-wetlands-day-2026-celebrating-cultural-heritage/", SEARCH, "2026-11-07"),
    "day_wwd_fao": ("https://www.fao.org/land-water/news-archive/news-detail/en/c/1756744/", SEARCH, "2026-11-07"),
    "day_nspd_isro": ("https://www.isro.gov.in/ISRO_EN/3rd_National_Space_Day_2026.html", OPENED, "2026-11-07"),
    "day_ddd_unccd": ("https://www.unccd.int/index%2ephp/news-stories/press-releases/rangelands-take-centre-stage-"
                      "desertification-and-drought-day-2026-kenya", SEARCH, "2026-11-07"),
    "day_ddd_unccd2": ("https://www.unccd.int/news-events/upcoming-events", SEARCH, "2026-11-07"),
    "day_wbdd_who": ("https://www.who.int/campaigns/world-blood-donor-day/2026/about", OPENED, "2026-11-07"),
    "day_wbdd_afro": ("https://www.afro.who.int/media-centre/events/world-blood-donor-day-2026", SEARCH, "2026-11-07"),
    "day_wcd_unh": ("https://unhabitat.org/news/22-oct-2026/world-cities-day-2026-to-explore-how-urban-regeneration-can-"
                    "advance-adequate", OPENED, "2026-11-07"),
})
DAY, DT = "Important Days", "Days and themes"

G(DAY, DT, "Intermediate",
  "World Wetlands Day, which marks the adoption of the Convention on Wetlands at Ramsar in 1971, was observed on 2 "
  "February 2026 under which theme?",
  ["Wetlands and traditional knowledge: Celebrating cultural heritage", "Wetlands and human wellbeing",
   "Protecting wetlands for our common future", "Wetlands action for people and nature"], "*",
  "Environmental days: wetlands",
  "The theme for World Wetlands Day 2026 (2 February) was 'Wetlands and traditional knowledge: Celebrating cultural "
  "heritage', highlighting the link between wetlands and Indigenous and local knowledge. The day marks the adoption of "
  "the Convention on Wetlands in the Iranian city of Ramsar in 1971.",
  ["Day: 2 February (Ramsar Convention, 1971)", "2026 theme: wetlands and traditional knowledge / cultural heritage"],
  [fact("World Wetlands Day 2026 theme: 'Wetlands and traditional knowledge: Celebrating cultural heritage' (MedWet)",
        "day_wwd_medwet"),
   fact("FAO: celebration of World Wetlands Day 2026 under the theme on wetlands and traditional knowledge; marks the "
        "Ramsar Convention", "day_wwd_fao")],
  why="The sources give the traditional-knowledge theme for 2026; the other wordings are not the 2026 theme.",
  current=ca("2026-02-02"))

G(DAY, DT, "Intermediate",
  "The 3rd National Space Day, marking the Chandrayaan-3 landing, was celebrated on 23 August 2026 with its main event "
  "in Ahmedabad. What was its theme?",
  ["Towards Viksit Bharat: Innovating, Collaborating and Aspiring to Global Space Leadership",
   "Touching Lives while Touching the Moon", "Aryabhata to Gaganyaan: Ancient Wisdom to Infinite Possibilities",
   "Space for All: Reaching the Last Mile"], "*",
  "National days: space",
  "ISRO held the inaugural event of the 3rd National Space Day (NSpD) on 23 August 2026 in Ahmedabad, home of the "
  "Space Applications Centre, with Union Minister Gajendra Singh Shekhawat as chief guest. The theme was 'Towards "
  "Viksit Bharat: Innovating, Collaborating and Aspiring to Global Space Leadership'. The day marks the Chandrayaan-3 "
  "Vikram lander's touchdown near the lunar south pole on 23 August 2023.",
  ["3rd NSpD: 23 Aug 2026, Ahmedabad (SAC)", "Theme: Towards Viksit Bharat ... Global Space Leadership"],
  [fact("3rd National Space Day 2026 celebrated at Ahmedabad on 23 August 2026; theme 'Towards Viksit Bharat: "
        "Innovating, Collaborating and Aspiring to Global Space Leadership'; chief guest Gajendra Singh Shekhawat (ISRO)",
        "day_nspd_isro")],
  why="ISRO's page gives the Viksit Bharat theme for 2026; the other options are not the 2026 theme in the source.",
  current=ca("2026-08-23"))

G(DAY, DT, "Intermediate",
  "Desertification and Drought Day 2026 (17 June), linked to the International Year of Rangelands and Pastoralists, "
  "had its global observance in which country, under the theme 'Rangelands: Recognize. Respect. Restore.'?",
  ["Kenya", "Mongolia", "Saudi Arabia", "Ethiopia"], "*",
  "Environmental days: land degradation",
  "The UNCCD announced that Kenya would host the global observance of Desertification and Drought Day on 17 June 2026 "
  "under the theme 'Rangelands: Recognize. Respect. Restore.', with the event in Kilifi County.",
  ["DDD 2026: 17 June", "Host: Kenya (Kilifi)", "Theme on rangelands"],
  [fact("UNCCD: rangelands to take centre stage on Desertification and Drought Day 2026 in Kenya; theme 'Rangelands: "
        "Recognize. Respect. Restore.'", "day_ddd_unccd"),
   fact("UNCCD events page: Desertification and Drought Day 2026, where: Kilifi (Kenya)", "day_ddd_unccd2")],
  why="The UNCCD names Kenya as the host; the other countries are not named as hosts of the 2026 day.",
  current=ca("2026-06-17"))

G(DAY, DT, "Intermediate",
  "WHO's slogan for World Blood Donor Day 2026, inspired by a quote of the Persian poet Rumi, was:",
  ["One Drop of Humanity. Give Blood. Save Lives.", "Give blood, give hope: together we save lives",
   "20 years of celebrating giving: thank you blood donors", "Donating blood is an act of solidarity"], "*",
  "Health days: blood donation",
  "WHO's campaign page gives the 2026 slogan of World Blood Donor Day (14 June) as 'One Drop of Humanity. Give Blood. "
  "Save Lives.', drawing on Rumi's line that one is not a drop in the ocean but the entire ocean in a drop.",
  ["World Blood Donor Day: 14 June", "2026 slogan: One Drop of Humanity. Give Blood. Save Lives."],
  [fact("WHO: World Blood Donor Day 2026 slogan 'One Drop of Humanity. Give Blood. Save Lives.', inspired by a quote of "
        "Jalal ad-Din Rumi", "day_wbdd_who"),
   fact("WHO AFRO event page: World Blood Donor Day 2026, 14 June 2026", "day_wbdd_afro")],
  why="WHO's page gives the 'One Drop of Humanity' slogan for 2026; the other slogans are not the 2026 slogan.",
  current=ca("2026-06-14"))

G(DAY, DT, "Intermediate",
  "World Cities Day 2026 (31 October), which concludes UN-Habitat's 'Urban October', had its global observance in "
  "which city, under the theme 'Regenerating the City: Adequate Housing for All'?",
  ["Fuzhou", "Nairobi", "Baku", "Shanghai"], "*",
  "UN days: urbanisation",
  "UN-Habitat announced on 22 October 2026 that Fuzhou, China, would host the global observance of World Cities Day "
  "on 31 October 2026 under the theme 'Regenerating the City: Adequate Housing for All'. World Cities Day concludes "
  "Urban October, which begins with World Habitat Day.",
  ["World Cities Day: 31 October; ends Urban October", "2026 host: Fuzhou, China",
   "Theme: Regenerating the City: Adequate Housing for All"],
  [fact("UN-Habitat (22 Oct 2026): Fuzhou will host the global observance of World Cities Day on 31 October; theme "
        "'Regenerating the City: Adequate Housing for All'; World Cities Day concludes Urban October", "day_wcd_unh")],
  why="UN-Habitat names Fuzhou as the 2026 host; the other cities are not named as hosts.",
  current=ca("2026-10-31"))


# ---------------------------------------------------------------- National CA (more)
U.update({
    "nat_agv_fpj": ("https://www.freepressjournal.in/uttar-pradesh/uttarakhand-becomes-first-state-to-set-up-employment-"
                    "cell-for-agniveers", OPENED, "2026-11-07"),
    "nat_agv_nk": ("https://www.newkerala.com/news/a/uttarakhand-establish-countrys-first-agniveer-employment-cell-309.htm",
                   SEARCH, "2026-11-07"),
    "nat_agv_nm": ("https://thenewsmill.com/2026/07/uttarakhand-to-set-up-countrys-first-agniveer-employment-cell/",
                   SEARCH, "2026-11-07"),
    "nat_nh752d_dd": ("https://ddnews.gov.in/en/cabinet-approves-rs-3839-crore-four-lane-highway-project-in-madhya-"
                      "pradesh-to-link-with-delhi-mumbai-expressway/", OPENED, "2026-11-07"),
    "nat_wbpmjay_air": ("https://newsonair.gov.in/ayushman-bharat-health-insurance-scheme-formally-launched-in-west-"
                        "bengal/", OPENED, "2026-11-07"),
    "nat_wbpmjay_air2": ("https://newsonair.gov.in/west-bengal-cm-suvendu-adhikari-to-launch-ayushman-bharat-pm-jay-in-"
                         "the-state-today/", SEARCH, "2026-11-07"),
})

G(NCA, "States and UTs", "Intermediate",
  "In July 2026, which state's government announced that it would set up India's first dedicated Employment Cell for "
  "Agniveers, to help them find jobs after completing their four-year service in the armed forces?",
  ["Uttarakhand", "Himachal Pradesh", "Haryana", "Rajasthan"], "*",
  "States: welfare of Agniveers",
  "Uttarakhand Chief Minister Pushkar Singh Dhami announced on 17 July 2026 that the state would establish the "
  "country's first Agniveer Employment Cell, and the Dhami Cabinet approved it. The cell is to help Agniveers "
  "returning after four years of service find employment; the state had earlier announced a 10% reservation for "
  "Agniveers in government services.",
  ["State: Uttarakhand (CM Pushkar Singh Dhami)", "First dedicated Employment Cell for Agniveers",
   "Earlier: 10% reservation in state government services"],
  [fact("Uttarakhand becomes first state to set up Employment Cell for Agniveers; approved by the Dhami Cabinet; earlier "
        "10% reservation in government services (Free Press Journal)", "nat_agv_fpj"),
   fact("Uttarakhand to establish country's first Agniveer employment cell (NewKerala/IANS, 17 July 2026)", "nat_agv_nk"),
   fact("Uttarakhand to set up country's first Agniveer employment cell (The NewsMill, July 2026)", "nat_agv_nm")],
  why="The sources name Uttarakhand; the other states are not mentioned.",
  current=ca("2026-07-17"))

GS(NCA, "Government decisions", "Advanced",
   "the highway project approved by the Cabinet Committee on Economic Affairs on 10 March 2026 in Madhya Pradesh",
   ["It is the four-laning of the 80.45 km Badnawar-Timarwani section of NH-752D, passing through Dhar and Jhabua "
    "districts.",
    "It is to be built in the Engineering, Procurement and Construction (EPC) mode, fully funded by the government.",
    "It links Ujjain to the Delhi-Mumbai Expressway and is expected to ease traffic during the Simhastha Kumbh Mela of "
    "2028."],
   [True, False, True],
   "Infrastructure: national highways",
   "The CCEA chaired by PM Modi approved on 10 March 2026 the four-laning of the 80.45 km Badnawar-Timarwani stretch of "
   "NH-752D, through Petlawad and Thandla in the tribal districts of Dhar and Jhabua, at ₹3,839.42 crore. It will be "
   "built in the Hybrid Annuity Mode (HAM), not EPC, so statement 2 is wrong. It completes a four-lane link from "
   "Ujjain to the Timarwani interchange of the Delhi-Mumbai Expressway and is expected to ease traffic during the "
   "Simhastha Kumbh Mela in April 2028.",
   [fact("CCEA approved on 10 March 2026 the ₹3,839.42 crore four-laning of the 80.45 km Badnawar-Timarwani section of "
         "NH-752D in Dhar and Jhabua districts under Hybrid Annuity Mode; links Ujjain to the Delhi-Mumbai Expressway; "
         "eases traffic for Simhastha Kumbh Mela in April 2028 (DD News)", "nat_nh752d_dd")],
   why="Statement 2 is wrong: the project is to be built in the Hybrid Annuity Mode.",
   current=ca("2026-03-10"))

GS(NCA, "States and UTs", "Advanced", "the launch of Ayushman Bharat PM-JAY in West Bengal in August 2026",
   ["It was launched by Union Health Minister J. P. Nadda at Netaji Indoor Stadium, Kolkata, without the participation "
    "of the State government.",
    "About 6 crore people, or nearly 1.5 crore families, in the state are to be covered under Ayushman Bharat.",
    "The State's Mukhyamantri Swasthya Bima Yojana, launched at the same event, covers people not covered under "
    "Ayushman Bharat."],
   [False, True, True],
   "States: health insurance",
   "On 16 August 2026, West Bengal Chief Minister Suvendu Adhikari formally launched Ayushman Bharat in the state at "
   "Netaji Indoor Stadium, in the presence of Union Minister of State for Health Anupriya Patel, so statement 1 is "
   "wrong. About 6 crore people (nearly 1.5 crore families) in the state are to be covered, including all those above "
   "70. The State's Mukhyamantri Swasthya Bima Yojana, launched alongside, covers about 80 lakh families not covered "
   "by Ayushman Bharat; about 2,000 hospitals in the state are linked.",
   [fact("Ayushman Bharat formally launched in West Bengal by CM Suvendu Adhikari at Netaji Indoor Stadium with MoS "
         "Anupriya Patel; about 6 crore people (nearly 1.5 crore families); Mukhyamantri Swasthya Bima Yojana covers "
         "those not covered by Ayushman Bharat (AIR, 16 Aug 2026)", "nat_wbpmjay_air"),
    fact("West Bengal CM Suvendu Adhikari to launch Ayushman Bharat PM-JAY in the state today (AIR, 16 Aug 2026)",
         "nat_wbpmjay_air2")],
   why="Statement 1 is wrong: the scheme was launched by Chief Minister Suvendu Adhikari, with MoS Anupriya Patel "
       "present.",
   current=ca("2026-08-16"))


# ====================================================================== Government Policies
U.update({
    "pol_ogr_argus": ("https://www.argus-p.com/updates/updates/promotion-and-regulation-of-online-gaming-rules-2026/",
                      OPENED, "2026-11-07"),
    "pol_ogr_e4m": ("https://www.exchange4media.com/digital-news/govt-notifies-online-gaming-act-officially-bans-all-"
                    "real-money-games-154048.html", SEARCH, "2026-11-07"),
})

GS("Government Policies", "Regulatory reforms", "Advanced", "the Promotion and Regulation of Online Gaming Rules, 2026",
   ["They were notified by the Ministry of Electronics and Information Technology on 22 April 2026 and came into "
    "force on 1 May 2026.",
    "The Online Gaming Authority of India set up under them is to have its head office in Bengaluru.",
    "E-sports must mandatorily undergo determination by the Authority and be registered."],
   [True, False, True],
   "Digital regulation: online gaming",
   "MeitY notified the Promotion and Regulation of Online Gaming Rules, 2026 on 22 April 2026 under the Promotion and "
   "Regulation of Online Gaming Act, 2025; they came into force on 1 May 2026. They set up the Online Gaming Authority "
   "of India, an attached office of MeitY with its head office in the National Capital Territory of Delhi, so "
   "statement 2 is wrong. E-sports must undergo determination and registration; a game determined to be an online "
   "money game can be acted against under the Act. Complaints go first to the service provider, then to the Authority "
   "and then to an appellate authority.",
   [fact("Rules notified by MeitY on April 22, 2026; in force from May 01, 2026; Online Gaming Authority of India with "
         "head office in NCT of Delhi as an attached office of MeitY; e-sports must mandatorily undergo determination "
         "and registration (Argus Partners)", "pol_ogr_argus"),
    fact("Online Gaming Act to kick in on May 1, tightens curbs on online money gaming (exchange4media)", "pol_ogr_e4m")],
   why="Statement 2 is wrong: the Authority's head office is in Delhi.",
   current=ca("2026-04-22"))

# ###################################################################### part: intl (International CA, Organizations)
U.update({
    "int_mk_kt": ("https://www.khaleejtimes.com/story/4Pkb-4_b-od1JZIw2zEWK3VxDxNlRm4Y7qop7bJHzhV6euLJl9qb5Xp0EJhk6NDw",
                  OPENED, "2026-11-07"),
    "int_mk_raz": ("https://report.az/en/region/iran-s-assembly-of-experts-elects-mojtaba-khamenei-as-supreme-leader",
                   SEARCH, "2026-11-07"),
    "int_isr_aj": ("https://aljazeera.com/news/2026/10/28/five-key-takeaways-from-israels-parliamentary-elections", OPENED,
                   "2026-11-07"),
    "int_isr_jns": ("https://jns.org/news/israel-news/right-wing-bloc-wins-israeli-election-with-53-seats-likud-emerges-"
                    "as-largest-party", SEARCH, "2026-11-07"),
    "int_npl_air": ("https://newsonair.gov.in/eam-s-jaishankar-hands-over-72-health-facilities-and-12-heritage-projects-"
                    "to-nepal/", OPENED, "2026-11-06"),
    "int_bel_print": ("https://theprint.in/diplomacy/india-belgium-to-strengthen-defence-ties-deepen-engagement-in-"
                      "critical-mineral-semiconductor-sectors/3032939/", OPENED, "2026-11-07"),
    "int_bel_rep": ("https://www.republicworld.com/world-news/india-belgium-unveil-10-key-outcomes-during-pm-de-wevers-"
                    "visit-mea-says-ties-focused-on-3ts-trade-technology-talent-2026-09-04-136240", SEARCH, "2026-11-07"),
})

ICA = "International Current Affairs"
BR, GE = "Bilateral relations", "Global events"

G(ICA, GE, "Basic",
  "Who was chosen by Iran's Assembly of Experts in March 2026 as the country's new Supreme Leader, after Ayatollah Ali "
  "Khamenei was killed in US-Israeli strikes?",
  ["Mojtaba Khamenei", "Masoud Pezeshkian", "Alireza Arafi", "Mohammad Bagher Ghalibaf"], "*",
  "West Asia: leadership change in Iran",
  "Ali Khamenei, Supreme Leader since 1989, was killed in US-Israeli strikes on Iran at the start of the war that began "
  "at the end of February 2026. Just after midnight Tehran time on 9 March 2026, the 88-member Assembly of Experts "
  "announced that his son, Ayatollah Mojtaba Khamenei, had been chosen as Iran's third Leader.",
  ["Body that selects the Leader: Assembly of Experts (88 clerics)", "Announced 9 March 2026",
   "New Leader: Mojtaba Khamenei, son of Ali Khamenei"],
  [fact("Assembly of Experts named Ayatollah Seyyed Mojtaba Hosseini Khamenei, son of Ali Khamenei, as Iran's third "
        "Leader; statement just after midnight Tehran time on Monday 9 March 2026; Ali Khamenei killed in US-Israeli "
        "strikes (Khaleej Times)", "int_mk_kt"),
   fact("Iran's Assembly of Experts elects Mojtaba Khamenei as supreme leader (Report.az)", "int_mk_raz")],
  why="The sources name Mojtaba Khamenei; Pezeshkian is Iran's President and the others were not chosen.",
  current=ca("2026-03-09"))

G(ICA, GE, "Intermediate",
  "In Israel's Knesset election of 27 October 2026, Likud emerged as the largest party, while neither bloc reached the "
  "61-seat majority. Which party, led by former army chief Gadi Eisenkot, came second?",
  ["Yashar", "Yesh Atid", "National Unity", "Yisrael Beiteinu"], "*",
  "Elections: Israel",
  "Israel voted on Tuesday, 27 October 2026. Likud was the largest party with about 27 seats, followed by Gadi "
  "Eisenkot's Yashar with about 21. Netanyahu's right-wing bloc finished with 53 of the 120 seats in the final count, "
  "short of the 61 needed for a majority, and Arab-led parties emerged as potential kingmakers.",
  ["Election: 27 Oct 2026", "Largest: Likud (~27)", "Second: Yashar (Gadi Eisenkot, ~21)", "Majority mark: 61 of 120"],
  [fact("Tuesday's vote (27 Oct 2026): Likud largest with about 27 seats; Eisenkot's Yashar about 21; majority 61 of "
        "120 (Al Jazeera, 28 Oct 2026)", "int_isr_aj"),
   fact("Right-wing bloc wins Israeli election with 53 seats; Likud emerges as largest party (JNS)", "int_isr_jns")],
  why="The sources name Yashar as Eisenkot's party; the other parties are not the one that finished second.",
  current=ca("2026-10-27"))

G(ICA, BR, "Intermediate",
  "During the visit of Nepal's Foreign Minister Shisir Khanal to New Delhi in June 2026, External Affairs Minister S. "
  "Jaishankar virtually handed over to Nepal 72 health facilities and 12 cultural heritage projects. Under which "
  "programme were these built?",
  ["Nepal's reconstruction programme after the 2015 earthquake", "The Kosi flood-relief programme of 2008",
   "The Pancheshwar Multipurpose Project", "The Lumbini Buddhist circuit development plan"], "*",
  "India-Nepal: development partnership",
  "On 7 June 2026, after talks with Nepal's Foreign Minister Shisir Khanal, who was on a three-day visit to India, S. "
  "Jaishankar virtually handed over 72 health facilities and 12 cultural heritage projects built as part of Nepal's "
  "reconstruction after the 2015 earthquake. Digital India Bhashini and Kathmandu University also signed an MoU on a "
  "'Voice First' language translation platform for Nepal.",
  ["Handed over: 72 health facilities + 12 heritage projects", "Post-2015-earthquake reconstruction",
   "Also: Bhashini-Kathmandu University MoU"],
  [fact("Jaishankar handed over 72 health facilities and 12 cultural heritage projects, part of Nepal's post-2015 "
        "earthquake reconstruction programme, after meeting Nepal FM Shisir Khanal; Bhashini-Kathmandu University MoU "
        "(AIR, 7 June 2026)", "int_npl_air")],
  why="The source links the projects to post-2015-earthquake reconstruction; the other programmes are not mentioned.",
  current=ca("2026-06-07"))

GS(ICA, BR, "Advanced", "Belgian Prime Minister Bart De Wever's visit to India in September 2026",
   ["His talks with Prime Minister Modi were held at Hyderabad House on 3 September 2026, in the first visit by a "
    "Belgian Prime Minister to India in two decades.",
    "The documents signed included a letter of intent on defence cooperation and an MoU on renewable energy.",
    "It was De Wever's second visit to India since he took office in February 2025."],
   [True, True, False],
   "India-Europe: Belgium",
   "Bart De Wever held talks with PM Modi at Hyderabad House, New Delhi, on Thursday, 3 September 2026, during a "
   "three-day visit that also took him to Mumbai. It was the first visit by a Belgian Prime Minister in two decades and "
   "his first visit to India since taking office in February 2025, so statement 3 is wrong. About 10 outcomes were "
   "announced, including a letter of intent on defence cooperation and MoUs on renewable energy and on combating "
   "transnational crime and cybercrime.",
   [fact("Talks at Hyderabad House on Thursday, 3 September 2026; first visit by a Belgian PM in two decades; his first "
         "visit to India since taking office in February 2025; letter of intent on defence cooperation, MoUs on "
         "renewable energy and on transnational crime and cybercrime; also Mumbai (ThePrint)", "int_bel_print"),
    fact("India, Belgium unveil 10 key outcomes during PM De Wever's visit (Republic World, 4 Sep 2026)", "int_bel_rep")],
   why="Statement 3 is wrong: it was his first visit to India since taking office.",
   current=ca("2026-09-03"))


U.update({
    "int_mgl_air": ("https://newsonair.gov.in/former-mongolian-president-lauds-progress-of-india-backed-oil-refinery-"
                    "project/", OPENED, "2026-11-07"),
    "int_mgl_meil": ("https://meil.in/mongolia-oil-refinery-plant", SEARCH, "2026-11-07"),
    "int_tha_air": ("https://newsonair.gov.in/thailand-allows-visa-free-entry-and-stay-up-to-30-days-for-indian-"
                    "tourists/", OPENED, "2026-11-07"),
    "int_iaea_air": ("https://newsonair.gov.in/iaea-refers-iran-to-unsc-over-nuclear-non-compliance/", OPENED,
                     "2026-11-07"),
    "int_l70_air": ("https://newsonair.gov.in/defence-minister-rajnath-singh-meets-sri-lankan-president-anura-kumara-"
                    "dissanayake-in-colombo/", OPENED, "2026-11-07"),
    "int_unsg_aj": ("https://www.aljazeera.com/news/2026/7/30/un-launches-hunt-for-next-chief-amid-rising-challenges",
                    OPENED, "2026-11-07"),
    "int_unsg_nat": ("https://www.thenationalnews.com/news/us/2026/09/29/un-chief-race-costa-ricas-rebeca-grynspan-"
                     "leads-fourth-security-council-straw-poll/", SEARCH, "2026-11-07"),
    "int_fra_aj": ("https://www.aljazeera.com/news/2026/3/2/france-to-increase-nuclear-warheads-lend-nuclear-aircraft-"
                   "to-europe-allies", SEARCH, "2026-11-07"),
    "int_fra_ctv": ("https://www.ctvnews.ca/world/article/macron-says-france-will-increase-its-nuclear-warheads-for-the-"
                    "first-time-in-decades/", SEARCH, "2026-11-07"),
    "int_eln_wmo": ("https://wmo.int/node/39068", OPENED, "2026-11-07"),
})

G(ICA, BR, "Basic",
  "Mongolia's first oil refinery, in Dornogovi province, whose progress was praised in July 2026 by former Mongolian "
  "President Nambaryn Enkhbayar, is being built with a Line of Credit of about how much from the Government of India?",
  ["US$ 1.7 billion", "US$ 500 million", "US$ 3 billion", "US$ 900 million"], "*",
  "India-Mongolia: development partnership",
  "News On AIR reported on 7 July 2026 that former President Nambaryn Enkhbayar lauded the progress of the Mongol "
  "Refinery project in Dornogovi, built with a US$ 1.7 billion Line of Credit extended by the Government of India. "
  "Engineers India Limited and Megha Engineering and Infrastructures Limited (MEIL) are working at the site.",
  ["Refinery: Dornogovi, Mongolia", "Indian LoC: US$ 1.7 billion", "Indian firms: EIL, MEIL"],
  [fact("Former Mongolian President Nambaryn Enkhbayar lauded the India-backed refinery in Dornogovi; US$ 1.7 billion "
        "Line of Credit from the Government of India; EIL and MEIL at the site (AIR, 7 July 2026)", "int_mgl_air"),
   fact("MEIL page: Mongolia oil refinery plant, built under an Indian Government line of credit", "int_mgl_meil")],
  why="The source gives a US$ 1.7 billion Line of Credit; the other amounts are not stated.",
  current=ca("2026-07-07"))

G(ICA, BR, "Basic",
  "In September 2026, which country announced that Indian tourists holding ordinary passports could enter visa-free "
  "and stay for up to 30 days, with effect from 15 September?",
  ["Thailand", "Malaysia", "Sri Lanka", "Vietnam"], "*",
  "Visa facilitation for Indian travellers",
  "News On AIR reported on 9 September 2026 that Thailand's Ministry of Interior had exempted Indian tourists with "
  "ordinary passports from visas for stays not exceeding 30 days, with effect from the 15th of that month.",
  ["Country: Thailand (Ministry of Interior)", "Visa-free stay up to 30 days", "From 15 Sep 2026"],
  [fact("Thailand's Ministry of Interior: Indian tourists with ordinary passports exempt from visas for stays not "
        "exceeding 30 days, with effect from the 15th of the month (AIR, 9 September 2026)", "int_tha_air")],
  why="The source names Thailand; the other countries are not mentioned.",
  current=ca("2026-09-09"))

G(ICA, GE, "Basic",
  "In September 2026, the 35-member board of the International Atomic Energy Agency (IAEA) referred which country to "
  "the UN Security Council over nuclear non-compliance, the first such referral of that country in 20 years?",
  ["Iran", "North Korea", "Syria", "Saudi Arabia"], "*",
  "Nuclear non-proliferation",
  "On 10 September 2026 the IAEA's board referred Iran to the UN Security Council over its lack of cooperation with a "
  "long-running probe into uranium traces found at undeclared sites. It was the first referral of Iran to the "
  "Security Council in 20 years; Russia, China and Niger voted against.",
  ["IAEA board -> UNSC referral", "Country: Iran (first in 20 years)", "Issue: uranium traces at undeclared sites"],
  [fact("IAEA's 35-member board refers Iran to the UNSC over nuclear non-compliance; first referral of Iran in 20 years; "
        "uranium traces at undeclared sites (AIR, 10 Sep 2026)", "int_iaea_air")],
  why="The source names Iran; the other countries are not mentioned.",
  current=ca("2026-09-10"))

G(ICA, BR, "Intermediate",
  "During Defence Minister Rajnath Singh's visit to Colombo in September 2026, India and Sri Lanka exchanged an MoU to "
  "upgrade which equipment of the Sri Lankan Air Force?",
  ["L70 air defence guns", "Dornier maritime patrol aircraft", "Advanced Light Helicopters", "Akash missile batteries"],
  "*",
  "India-Sri Lanka: defence cooperation",
  "On 9 September 2026 Rajnath Singh met President Anura Kumara Dissanayake in Colombo. India and Sri Lanka exchanged an "
  "MoU on upgrading the Sri Lankan Air Force's L70 air defence guns, and an academic MoU between the NCC and the "
  "National Defence Colleges; three Bailey bridges built by Indian defence forces were virtually inaugurated.",
  ["Visit: Colombo, 9 Sep 2026", "MoU: upgrade of SLAF L70 air defence guns", "Also: NCC/NDC MoU, 3 Bailey bridges"],
  [fact("India and Sri Lanka exchanged an MoU on upgradation of L70 air defence guns for the Sri Lankan Air Force during "
        "Rajnath Singh's Colombo visit (AIR, 9 Sep 2026)", "int_l70_air")],
  why="The source names the L70 air defence guns; the other equipment is not mentioned.",
  current=ca("2026-09-09"))

G(ICA, GE, "Intermediate",
  "In the first Security Council straw poll for choosing the next UN Secretary-General, held on 30 July 2026, which "
  "candidate emerged as the early frontrunner?",
  ["Rebeca Grynspan (Costa Rica)", "Rafael Grossi (Argentina)", "Michelle Bachelet (Chile)", "Macky Sall (Senegal)"],
  "*",
  "UN: selection of the Secretary-General",
  "The Security Council held its first straw poll on 30 July 2026 to choose a successor to Antonio Guterres. In these "
  "non-binding secret ballots, members 'encourage', 'discourage' or express 'no opinion' on each candidate. Costa "
  "Rica's Rebeca Grynspan emerged as the early frontrunner with 10 'encourage' votes, ahead of Guyana's Carolyn "
  "Rodrigues Birkett and Argentina's Rafael Grossi; she also led the fourth poll in late September.",
  ["First straw poll: 30 July 2026", "Early frontrunner: Rebeca Grynspan (10 'encourage')", "Seven candidates"],
  [fact("First straw poll on 30 July 2026: Rebeca Grynspan (Costa Rica) early frontrunner with 10 'encourage' votes; "
        "Rodrigues Birkett 9; Grossi third; also Sall, Bachelet, Espinosa, Otunnu (Al Jazeera)", "int_unsg_aj"),
   fact("Costa Rica's Rebeca Grynspan leads fourth Security Council straw poll (The National, 29 Sep 2026)",
        "int_unsg_nat")],
  why="The source names Grynspan as the frontrunner; Grossi was third and the others trailed.",
  current=ca("2026-07-30"))

G(ICA, GE, "Intermediate",
  "In his speech at the Ile Longue submarine base on 2 March 2026, French President Emmanuel Macron ordered an "
  "increase in France's nuclear warheads and set out an 'advanced deterrence' offer to European partners. What did he "
  "say France would allow under it?",
  ["Temporary deployment of French nuclear-armed aircraft to allied countries",
   "Permanent stationing of French ballistic-missile submarines in allied ports",
   "Joint French-EU control over the launch of French nuclear weapons",
   "Transfer of French nuclear warheads to the stockpiles of allied countries"], "*",
  "Europe: nuclear deterrence",
  "On 2 March 2026 Macron said an upgrade of the arsenal was essential and that he had ordered an increase in the "
  "number of warheads, the first in decades. Under his 'advanced' (forward) deterrence, France would allow the "
  "temporary deployment of its nuclear-armed aircraft to allied countries, with talks begun with countries such as "
  "Britain, Germany and Poland.",
  ["Speech: Ile Longue, 2 March 2026", "More nuclear warheads", "Allies: temporary deployment of nuclear-armed jets"],
  [fact("France to increase nuclear warheads, lend nuclear aircraft to Europe allies (Al Jazeera, 2 March 2026)",
        "int_fra_aj"),
   fact("Macron says France will increase its nuclear warheads for the first time in decades; temporary deployment of "
        "nuclear-armed jets to European allies (CTV/AP)", "int_fra_ctv")],
  why="The sources describe temporary deployment of nuclear-armed aircraft; the other arrangements were not offered.",
  current=ca("2026-03-02"))

G(ICA, GE, "Intermediate",
  "WMO's El Nino update of 8 October 2026 forecast an October-December Nino 3.4 anomaly of about +3.7 deg C, above the "
  "previous record of +2.6 deg C. During which period was that earlier record set?",
  ["November 2015 to January 2016", "November 1997 to January 1998", "December 1982 to February 1983",
   "November 2023 to January 2024"], "*",
  "Climate: El Nino",
  "In its update of 8 October 2026, WMO said the El Nino was strengthening, with a near-100% likelihood of persisting "
  "through February 2027 and a forecast peak in December. The October-December Nino 3.4 anomaly was forecast at about "
  "+3.7 deg C, above the previous record of +2.6 deg C from November 2015 to January 2016, so it could be one of the "
  "strongest El Nino events since at least 1950.",
  ["Forecast: about +3.7 deg C (OND 2026), peak in December", "Previous record: +2.6 deg C, Nov 2015-Jan 2016"],
  [fact("WMO, 8 October 2026: OND Nino 3.4 anomaly forecast at approximately +3.7 deg C, peaking around December; "
        "previous record +2.6 deg C from November 2015 to January 2016; near-100 per cent likelihood of persisting "
        "through February 2027", "int_eln_wmo")],
  why="WMO gives November 2015-January 2016 as the period of the previous record; the other periods are not cited.",
  current=ca("2026-10-08"))


U.update({
    "int_ebo_air": ("https://newsonair.gov.in/new-outbreak-of-ebola-kills-65-in-eastern-dr-congo/", OPENED, "2026-11-07"),
    "int_trump_air": ("https://newsonair.gov.in/us-china-stress-cooperation-despite-tensions-over-trade-and-security-"
                      "issues/", OPENED, "2026-11-07"),
    "int_lbn_air": ("https://newsonair.gov.in/israel-and-lebanon-extend-ceasefire-for-45-days/", OPENED, "2026-11-07"),
    "int_whc_air": ("https://newsonair.gov.in/four-more-international-sites-added-to-unesco-world-heritage-list/", OPENED,
                    "2026-11-07"),
})

G(ICA, GE, "Intermediate",
  "In May 2026 the Africa Centres for Disease Control and Prevention reported a new Ebola outbreak that had killed 65 "
  "people, with suspected cases also in the city of Bunia. In which province of the Democratic Republic of the Congo "
  "did it occur?",
  ["Ituri", "Equateur", "North Kivu", "Kasai"], "*",
  "Global health: Ebola",
  "On 15 May 2026 the Africa CDC reported a new Ebola outbreak in Ituri province in north-eastern DR Congo, with 65 "
  "deaths (four among laboratory-confirmed cases), about 246 suspected cases and suspected cases also in the city of "
  "Bunia; sequencing was under way to determine the strain.",
  ["Reported by Africa CDC, 15 May 2026", "Ituri province (Bunia), north-eastern DR Congo", "65 deaths"],
  [fact("Africa CDC: new Ebola outbreak in Ituri province, north-eastern DR Congo; 65 deaths; about 246 suspected "
        "cases; suspected cases also in Bunia (AIR, 15 May 2026)", "int_ebo_air")],
  why="The source places the outbreak in Ituri province; the other provinces are not mentioned.",
  current=ca("2026-05-15"))

G(ICA, BR, "Intermediate",
  "US President Donald Trump concluded a three-day visit to China on 15 May 2026, holding talks with President Xi "
  "Jinping. In which city were these talks held?",
  ["Beijing", "Shanghai", "Shenzhen", "Hangzhou"], "*",
  "US-China relations",
  "News On AIR reported on 15 May 2026 that Trump had concluded his three-day China visit with talks with Xi Jinping "
  "in Beijing on trade, the Iran conflict and regional issues. Xi said the two sides agreed to maintain stable economic "
  "ties; no major agreements were announced on Taiwan, rare-earth exports or semiconductors, and Trump said he looked "
  "forward to hosting Xi at the White House.",
  ["Trump's 3-day China visit ended 15 May 2026", "Talks with Xi in Beijing", "Agreed to keep economic ties stable"],
  [fact("Xi Jinping and Donald Trump held talks in Beijing; Trump concluded his three-day China visit; agreed to "
        "maintain stable economic ties (AIR, 15 May 2026)", "int_trump_air")],
  why="The source places the talks in Beijing; the other cities are not mentioned.",
  current=ca("2026-05-15"))

G(ICA, GE, "Intermediate",
  "In May 2026 the United States announced that Israel and Lebanon had agreed to extend the cessation of hostilities "
  "of 16 April 2026 by 45 days, after talks it hosted. Where were these talks held?",
  ["Washington", "Doha", "Cairo", "Paris"], "*",
  "West Asia: Israel-Lebanon",
  "On 16 May 2026 US State Department spokesperson Tommy Pigott announced a 45-day extension of the 16 April cessation "
  "of hostilities between Israel and Lebanon, after 'highly productive' talks hosted by the US in Washington that "
  "concluded on 15 May. A security track at the Pentagon was set for 29 May and the political track for 2-3 June.",
  ["Extension: 45 days of the 16 April 2026 truce", "Talks hosted by the US in Washington (ended 15 May)",
   "Announced by State Dept spokesperson Tommy Pigott"],
  [fact("US State Department spokesperson Tommy Pigott: Israel-Lebanon cessation of hostilities of April 16 extended by "
        "45 days after US-hosted talks in Washington concluded on May 15 (AIR, 16 May 2026)", "int_lbn_air")],
  why="The source says the talks were hosted by the US in Washington; the other cities are not mentioned.",
  current=ca("2026-05-16"))

G(ICA, GE, "Intermediate",
  "The Boma-Badingilo Migratory Landscape was added to UNESCO's World Heritage List in July 2026 at the World Heritage "
  "Committee meeting in Busan. In which country is it located?",
  ["South Sudan", "Kenya", "Tanzania", "Uganda"], "*",
  "UNESCO World Heritage: 2026 inscriptions",
  "News On AIR reported on 26 July 2026 that four more international sites were inscribed at the UNESCO committee "
  "meeting in Busan, South Korea: the D-Day landing beaches (France), Mount Olympus (Greece), the ancient imperial "
  "capitals of Asuka and Fujiwara (Japan) and the Boma-Badingilo Migratory Landscape (South Sudan).",
  ["Inscribed July 2026, Busan", "Boma-Badingilo Migratory Landscape -> South Sudan"],
  [fact("Four sites added at the UNESCO committee meeting in Busan: D-Day landing beaches (France), Mount Olympus "
        "(Greece), Asuka and Fujiwara (Japan), Boma-Badingilo Migratory Landscape (South Sudan) (AIR, 26 July 2026)",
        "int_whc_air")],
  why="The source places Boma-Badingilo in South Sudan; the other countries are not mentioned.",
  current=ca("2026-07-26"))


# ====================================================================== National and International Organizations
U.update({
    "org_keita_unfpa": ("https://www.unfpa.org/press/diene-keita-appointed-executive-director-united-nations-population-"
                        "fund-unfpa", SEARCH, "2026-11-07"),
    "org_keita_qna": ("https://qna.org.qa/en/News-Area/News/2025-8/30/un-appoints-new-unfpa-executive-director", SEARCH,
                      "2026-11-07"),
    "org_floyd_ctbto": ("https://ctbto.org/news-and-events/news/member-states-reappoint-robert-floyd-ctbto-executive-"
                        "secretary", SEARCH, "2026-11-07"),
    "org_floyd_aca": ("https://www.armscontrol.org/act/2024-12/news-briefs/floyd-reappointed-head-test-ban-organization",
                      SEARCH, "2026-11-07"),
    "org_hcch": ("https://www.hcch.net/de/news-archive/details/?varevent=1167", OPENED, "2026-11-07"),
    "org_gcf_news": ("https://www.greenclimate.fund/news/green-climate-fund-names-mafalda-duarte-new-executive-director",
                     SEARCH, "2026-11-07"),
    "org_gcf_inc": ("https://www.incheon.go.kr/en/EN020201", SEARCH, "2026-11-07"),
    "org_unaids_pr": ("https://www.unaids.org/en/resources/presscentre/pressreleaseandstatementarchive/2026/october/"
                      "20261027_PR_PCBSpecial", OPENED, "2026-11-07"),
})
ORG = "National and International Organizations"
HH, MEM = "Headquarters and heads", "Membership"

G(ORG, HH, "Basic",
  "Diene Keita of Guinea was appointed by the UN Secretary-General in August 2025 as the Executive Director of which "
  "UN body, succeeding Natalia Kanem?",
  ["United Nations Population Fund (UNFPA)", "UN Women", "UNICEF", "UN Development Programme (UNDP)"], "*",
  "UN agencies: heads",
  "UN Secretary-General Antonio Guterres appointed Diene Keita of Guinea as Executive Director of the United Nations "
  "Population Fund (UNFPA), effective 29 August 2025, succeeding Natalia Kanem of Panama. She had been Acting Executive "
  "Director since 16 July 2025 and Deputy Executive Director (Programme) since 2020.",
  ["Diene Keita (Guinea)", "UNFPA Executive Director from 29 Aug 2025", "Succeeded Natalia Kanem"],
  [fact("Diene Keita appointed Executive Director of the United Nations Population Fund (UNFPA) (UNFPA press release)",
        "org_keita_unfpa"),
   fact("UN appoints new UNFPA Executive Director Diene Keita, succeeding Natalia Kanem (QNA, 30 Aug 2025)",
        "org_keita_qna")],
  why="The sources name UNFPA; the other bodies have different heads.",
  current=ca("2025-08-29"))

G(ORG, HH, "Intermediate",
  "Robert Floyd began his second four-year term as Executive Secretary of the Preparatory Commission for the "
  "Comprehensive Nuclear-Test-Ban Treaty Organization (CTBTO) in August 2025. He is a national of which country?",
  ["Australia", "Canada", "New Zealand", "Ireland"], "*",
  "International organisations: heads",
  "Member States of the CTBTO Preparatory Commission reappointed Robert Floyd for a second term in November 2024, by "
  "acclamation; the second four-year term began on 1 August 2025. Floyd, an Australian national, has led the CTBTO "
  "since August 2021 and earlier headed Australia's Safeguards and Non-Proliferation Office.",
  ["CTBTO Executive Secretary: Robert Floyd (Australia)", "Reappointed Nov 2024; 2nd term from 1 Aug 2025"],
  [fact("Member States reappoint Robert Floyd as CTBTO Executive Secretary for a second term (CTBTO, Nov 2024)",
        "org_floyd_ctbto"),
   fact("Floyd reappointed head of test ban organisation; Australian; led CTBTO since August 2021 (Arms Control "
        "Association, Dec 2024)", "org_floyd_aca")],
  why="The sources describe Floyd as Australian; the other nationalities are wrong.",
  current=ca("2025-08-01"))

G(ORG, MEM, "Intermediate",
  "On 17 September 2026, Qatar deposited its instrument of acceptance of the Statute of which organisation, becoming "
  "its 95th Member?",
  ["Hague Conference on Private International Law (HCCH)", "Permanent Court of Arbitration (PCA)",
   "Organisation for the Prohibition of Chemical Weapons (OPCW)", "International Institute for the Unification of "
   "Private Law (UNIDROIT)"], "*",
  "International organisations: membership",
  "The HCCH announced that Qatar became its 95th Member on 17 September 2026 by depositing its instrument of acceptance "
  "of the HCCH Statute with the Netherlands Ministry of Foreign Affairs, the depositary. With this, 160 States and "
  "Parties are connected to the HCCH.",
  ["Qatar -> 95th Member of the HCCH (17 Sep 2026)", "Instrument of acceptance of the HCCH Statute",
   "160 connected States and Parties"],
  [fact("Qatar becomes the 95th Member of the HCCH and its 160th Connected Party on 17 September 2026 by depositing its "
        "instrument of acceptance of the Statute; Netherlands Ministry of Foreign Affairs is depositary (HCCH)",
        "org_hcch")],
  why="The source names the HCCH; the other bodies are not mentioned.",
  current=ca("2026-09-17"))

G(ORG, HH, "Intermediate",
  "The Green Climate Fund, whose Executive Director Mafalda Duarte was selected by its Board in 2023, is "
  "headquartered in which city?",
  ["Songdo, Incheon (Republic of Korea)", "Bonn (Germany)", "Geneva (Switzerland)", "Nairobi (Kenya)"], "*",
  "Climate finance institutions",
  "The Green Climate Fund's Board named Mafalda Duarte, earlier CEO of the Climate Investment Funds, as Executive "
  "Director at a meeting at the GCF headquarters in Songdo, Incheon, Republic of Korea. The Incheon city government's "
  "page places the GCF in the G-Tower in Yeonsu-gu, Songdo.",
  ["GCF HQ: Songdo, Incheon, Republic of Korea", "Executive Director: Mafalda Duarte (from 2023)"],
  [fact("GCF names Mafalda Duarte as new Executive Director at a Board meeting at the GCF headquarters in Songdo, "
        "Incheon, Republic of Korea (GCF)", "org_gcf_news"),
   fact("Incheon Metropolitan City: About the GCF, G-Tower, Yeonsu-gu, Incheon", "org_gcf_inc")],
  why="The sources place the GCF in Songdo, Incheon; the other cities are not its headquarters.")

GS(ORG, HH, "Advanced", "the special session of the UNAIDS Programme Coordinating Board held in October 2026",
   ["Executive Director Winnie Byanyima will complete her term on 31 December 2026.",
    "The Board accepted the proposal to sunset UNAIDS by the end of 2026.",
    "The UN Secretary-General will appoint an interim Executive Director from 1 January 2027 while the Board selects "
    "the next Executive Director."],
   [True, False, True],
   "UN bodies: leadership and reform",
   "At a special session of the UNAIDS Programme Coordinating Board (Geneva, 26 October 2026), the Board rejected "
   "sunsetting UNAIDS, so statement 2 is wrong; it backed a streamlined Joint Programme and sent the strategic direction "
   "of the transition to ECOSOC. Winnie Byanyima will complete her term on 31 December 2026, and the Secretary-General "
   "will appoint an interim Executive Director from 1 January 2027 while the Board selects the next one.",
   [fact("UNAIDS PCB special session (Geneva, 26 Oct 2026): 'UNAIDS will not be sunset'; Byanyima completes her term on "
         "31 December 2026; SG to appoint interim Executive Director from 1 January 2027 (UNAIDS, 27 Oct 2026)",
         "org_unaids_pr")],
   why="Statement 2 is wrong: the Board rejected sunsetting UNAIDS.",
   current=ca("2026-10-26"))

# ###################################################################### part: pol (Government Schemes)
U.update({
    "sc_shri_tr": ("https://www.tribuneindia.com/news/nation/cabinet-approves-rs-27-360-crore-scheme-for-development-of-"
                   "over-14-000-pm-shri-schools-429512", SEARCH, "2026-11-07"),
    "sc_shri_dh": ("https://www.deccanherald.com/national/cabinet-approves-rs-27360-crore-scheme-for-setting-up-over-14000-"
                   "pm-shri-schools-1143035", SEARCH, "2026-11-07"),
    "sc_pmmvy_pib": ("https://pib.gov.in/PressReleasePage.aspx?PRID=1846142", SEARCH, "2026-11-07"),
    "sc_pmmvy_wcd": ("https://wcd.delhi.gov.in/hi/node/47312", SEARCH, "2026-11-07"),
    "sc_ndd_rs": ("https://rsdebate.nic.in/bitstream/123456789/751744/1/PQ_266_06122024_U1289_p130_p130.pdf", SEARCH,
                  "2026-11-07"),
    "sc_ndd_vnd": ("https://www.voicendata.com/news/government-launches-namo-drone-didi-scheme-to-empower-women-shgs-"
                   "8447366", SEARCH, "2026-11-07"),
    "sc_nghm_nm": ("https://www.narendramodi.in/cabinet-approves-national-green-hydrogen-mission", SEARCH, "2026-11-07"),
    "sc_nghm_pv": ("https://pv-magazine-india.com/2023/01/04/india-approves-national-green-hydrogen-mission", SEARCH,
                   "2026-11-07"),
    "sc_vvp_tr": ("https://www.tribuneindia.com/news/business/vibrant-border-villages-programme-2-0-approved-with-total-"
                  "outlay-of-rs-6839-crore", SEARCH, "2026-11-07"),
    "sc_vvp_print": ("https://theprint.in/india/union-cabinet-approves-phase-2-of-vibrant-villages-programme/2578228",
                     SEARCH, "2026-11-07"),
    "sc_maus_imd": ("https://mausam.imd.gov.in/event/mission_mausam.pdf", SEARCH, "2026-11-07"),
    "sc_maus_nm": ("https://www.narendramodi.in/cabinet-approves-mission-mausam-to-create-a-more-weather-ready-and-climate-"
                   "smart-bharat-with-an-outlay-of-rs-2-000-crore-over-two-years", SEARCH, "2026-11-07"),
    "sc_eshram_fpj": ("https://www.freepressjournal.in/tech/e-shram-portal-completes-five-years-over-3189-crore-"
                      "unorganised-workers-registered", SEARCH, "2026-11-07"),
    "sc_eshram_ians": ("https://ianslive.in/e-shram-portal-marks-five-years-with-3189-crore-registrations--"
                       "20260825162201", SEARCH, "2026-11-07"),
    "sc_plw_air": ("https://www.newsonair.gov.in/govt-selects-five-companies-in-fourth-round-of-pli-scheme-for-white-"
                   "goods", SEARCH, "2026-11-07"),
    "sc_plw_ians": ("https://ianslive.in/pli-white-goods-scheme-5-firms-selected-to-achieve-rs-8337-crore-in-production-"
                    "says-govt--20260123175829", SEARCH, "2026-11-07"),
    "sc_gs_fpj": ("https://www.freepressjournal.in/india/see-pics-pm-narendra-modi-launches-pm-gatishakti-master-plan-for-"
                  "multi-modal-connectivity-heres-all-you-need-to-know", SEARCH, "2026-11-07"),
    "sc_gs_di": ("https://www.digitalindia.gov.in/initiative/gati-shakti/", SEARCH, "2026-11-07"),
    "sc_ncmm_print": ("https://theprint.in/india/cabinet-approves-national-critical-mineral-mission-anticipates-"
                      "investments-of-rs-18000-cr-from-psus/2468642", SEARCH, "2026-11-07"),
    "sc_ncmm_pmi": ("https://www.pmindia.gov.in/en/news_updates/cabinet-approves-national-critical-mineral-mission-to-"
                    "build-a-resilient-value-chain-for-critical-mineral-resources-vital-to-green-technologies-with-an-"
                    "outlay-of-rs-34300-crore-over-seven-years", SEARCH, "2026-11-07"),
    "sc_ecms_tr": ("https://www.tribuneindia.com/news/business/third-tranche-of-ecms-approved-with-rs-41863-crore-"
                   "investment-covering-22-applications/", SEARCH, "2026-11-07"),
    "sc_ecms_bt": ("https://www.businesstoday.in/latest/policy/story/meity-clears-22-electronics-pli-projects-worth-"
                   "rs41863-crore-eyes-supply-chain-self-reliance-509135-2026-01-02", SEARCH, "2026-11-07"),
    "sc_ai_pmi": ("https://www.pmindia.gov.in/en/news_updates/cabinet-approves-ambitious-indiaai-mission-to-strengthen-"
                  "the-ai-innovation-ecosystem/", SEARCH, "2026-11-07"),
    "sc_ai_itv": ("https://www.indiatvnews.com/technology/news/government-approves-indiaai-mission-with-outlay-of-rs-10-"
                  "372-crore-here-s-everything-you-need-to-know-2024-03-07-920395", SEARCH, "2026-11-07"),
    "sc_dam_print": ("https://theprint.in/economy/cabinet-approves-digital-agriculture-mission-with-rs-2817-crore-outlay/"
                     "2249769", SEARCH, "2026-11-07"),
    "sc_dam_bw": ("https://businessworld.in/article/cabinet-approves-digital-agri-mission-with-rs-2817-cr-outlay-531676",
                  SEARCH, "2026-11-07"),
    "sc_dom_bs": ("https://bsppd.business-standard.com/article/current-affairs/samudrayaan-india-s-first-manned-mission-to-"
                  "send-humans-6k-m-deep-in-ocean-122080600776_1.html", SEARCH, "2026-11-07"),
    "sc_dom_tbs": ("https://www.tbsnews.net/world/south-asia/samudrayaan-indias-first-mission-send-humans-6000-metres-"
                   "deep-ocean-472594", SEARCH, "2026-11-07"),
    "sc_gec_rw": ("https://renewablewatch.in/2026/10/01/cabinet-approves-green-energy-corridor-phase-iii-scheme/", SEARCH,
                  "2026-11-07"),
    "sc_gec_sw": ("https://swarajyamag.com/infrastructure/india-clears-rs-186-lakh-crore-green-energy-corridor-iii-to-"
                  "evacuate-135-gw-renewables-deploy-50-gwh-battery-energy-storage-systems", SEARCH, "2026-11-07"),
    "sc_pran_ls": ("https://eparlib.nic.in/bitstream/123456789/2973778/1/AS14.pdf", SEARCH, "2026-11-07"),
    "sc_pran_dte": ("https://www.downtoearth.org.in/agriculture/dedicated-efforts-needed-to-effectively-implement-pm-"
                    "pranam-ensure-balanced-use-of-fertilisers", SEARCH, "2026-11-07"),
    "sc_anrf_dst": ("https://dst.gov.in/parliament-passes-anusandhan-national-research-foundation-nrf-bill-2023-rajya-"
                    "sabha-adopting-bill", SEARCH, "2026-11-07"),
    "sc_anrf_dte": ("https://www.downtoearth.org.in/science-technology/budget-2024-25-operationalisation-of-anrf-may-be-"
                    "too-little-too-late", SEARCH, "2026-11-07"),
    "sc_sag_ii": ("https://indianinfrastructure.com/2022/02/14/sagarmala-programme-aims-to-reduce-logistics-costs/",
                  SEARCH, "2026-11-07"),
    "sc_sag_mp": ("https://www.maritimeprofessional.com/amp/news/sagarmala-aims-promote-port-development-293230", SEARCH,
                  "2026-11-07"),
})
GSC = "Government Schemes"
CS, SL = "Central schemes", "Scheme launches and changes"

# ------------------------------------------------------------------ Basic (7)
G(GSC, CS, "Basic",
  "The PM SHRI scheme (PM Schools for Rising India), approved by the Union Cabinet on 7 September 2022 with an outlay of "
  "Rs 27,360 crore, aims to develop roughly how many existing schools as exemplar schools under NEP 2020?",
  ["Over 14,500", "Over 1,45,000", "About 5,000", "About 50,000"], "*",
  "Education schemes",
  "The Cabinet approved PM SHRI on 7 September 2022 as a Centrally Sponsored Scheme with an outlay of Rs 27,360 crore "
  "(central share Rs 18,128 crore) for 2022-23 to 2026-27, to upgrade more than 14,500 existing schools run by the "
  "Centre, States, UTs and local bodies into exemplar schools showcasing the National Education Policy 2020.",
  ["PM SHRI: approved 7 Sep 2022; Rs 27,360 crore", "Target: 14,500+ existing schools as exemplar schools"],
  [fact("Cabinet approves Rs 27,360 crore scheme for development of over 14,000 PM SHRI schools (Tribune, 7 Sep 2022)",
        "sc_shri_tr"),
   fact("Cabinet approves Rs 27,360 crore scheme for setting up over 14,000 (14,500+) PM SHRI schools (Deccan Herald)",
        "sc_shri_dh")],
  why="The scheme targets about 14,500 schools; the other numbers are not its target.",
  current=ca("2022-09-07"))

G(GSC, CS, "Basic",
  "Under the Pradhan Mantri Matru Vandana Yojana as revised under Mission Shakti, how much cash incentive is given for "
  "a second child if the child is a girl?",
  ["Rs 6,000", "Rs 5,000", "Rs 3,000", "Rs 11,000"], "*",
  "Maternity benefit schemes",
  "PMMVY gives Rs 5,000 for the first living child. Under the revised scheme (Mission Shakti, from 1 April 2022), Rs "
  "6,000 is given in one instalment after birth for a second child, but only if the second child is a girl.",
  ["First child: Rs 5,000", "Second child (girl only): Rs 6,000", "Part of Mission Shakti (from 1 Apr 2022)"],
  [fact("PMMVY under Mission Shakti: Rs 5,000 for the first child; Rs 6,000 for the second child if a girl (PIB release "
        "PRID 1846142)", "sc_pmmvy_pib"),
   fact("Delhi WCD Department page on PMMVY benefits", "sc_pmmvy_wcd")],
  why="Rs 5,000 is the first-child benefit; the other amounts are not PMMVY benefits.",
  current=ca("2022-04-01"))

G(GSC, CS, "Basic",
  "The Namo Drone Didi scheme, with an outlay of Rs 1,261 crore, aims to provide agricultural drones to how many "
  "selected women Self-Help Groups?",
  ["15,000", "1,50,000", "5,000", "50,000"], "*",
  "Agriculture and women's empowerment",
  "Namo Drone Didi is a Central Sector Scheme with an outlay of Rs 1,261 crore (2023-24 to 2025-26) to give drones to "
  "15,000 selected women SHGs for rental agricultural services. Central assistance covers 80% of the drone package "
  "cost, up to Rs 8 lakh per SHG, and it is implemented under DAY-NRLM.",
  ["Target: 15,000 women SHGs", "80% of drone cost, up to Rs 8 lakh", "Outlay Rs 1,261 crore"],
  [fact("Rajya Sabha reply (6 Dec 2024): Namo Drone Didi, outlay Rs 1,261 crore for 2023-24 to 2025-26, drones to 15,000 "
        "selected women SHGs", "sc_ndd_rs"),
   fact("Government launches Namo Drone Didi scheme to empower women SHGs; 80% assistance up to Rs 8 lakh (Voice&Data)",
        "sc_ndd_vnd")],
  why="The scheme targets 15,000 SHGs; the other numbers are not its target.",
  current=ca("2024-12-06"))

G(GSC, CS, "Basic",
  "The National Green Hydrogen Mission, approved by the Union Cabinet on 4 January 2023, aims to develop green hydrogen "
  "production capacity of at least how much per annum by 2030?",
  ["5 million metric tonnes", "50 million metric tonnes", "1 million metric tonnes", "125 million metric tonnes"], "*",
  "Clean energy missions",
  "The Cabinet approved the National Green Hydrogen Mission on 4 January 2023 with an outlay of Rs 19,744 crore "
  "(including Rs 17,490 crore for the SIGHT programme). It targets at least 5 MMT per annum of green hydrogen capacity "
  "by 2030, with about 125 GW of associated renewable capacity, and expects to abate nearly 50 MMT of CO2 a year.",
  ["Target: 5 MMT per annum by 2030", "Outlay Rs 19,744 crore (SIGHT Rs 17,490 crore)", "About 125 GW RE capacity"],
  [fact("Cabinet approves National Green Hydrogen Mission: Rs 19,744 crore; at least 5 MMT per annum by 2030; ~125 GW RE; "
        "~50 MMT CO2 abated (narendramodi.in, 4 Jan 2023)", "sc_nghm_nm"),
   fact("India approves National Green Hydrogen Mission (pv magazine India, 4 Jan 2023)", "sc_nghm_pv")],
  why="The target is 5 MMT; 125 GW is the associated RE capacity and 50 MMT the CO2 abatement.",
  current=ca("2023-01-04"))

G(GSC, SL, "Basic",
  "The Vibrant Villages Programme-II, approved by the Union Cabinet on 4 April 2025 with an outlay of Rs 6,839 crore, "
  "covers villages along which borders?",
  ["International land borders other than the Northern border", "Only the Northern border with China",
   "Only the coastline and island territories", "Only the Line of Control in Jammu and Kashmir"], "*",
  "Border area development",
  "VVP-II, a Central Sector Scheme (100% central funding) for 2024-25 to 2028-29 with Rs 6,839 crore, covers villages "
  "in blocks abutting international land borders other than the Northern border, which is already covered under VVP-I. "
  "It seeks saturation of all-weather roads, telecom, television connectivity and electrification.",
  ["VVP-II: approved 4 Apr 2025, Rs 6,839 crore", "Coverage: land-border villages other than Northern border (VVP-I)"],
  [fact("Vibrant (border) Villages Programme 2.0 approved with total outlay of Rs 6,839 crore (Tribune, Apr 2025)",
        "sc_vvp_tr"),
   fact("Union Cabinet approves phase 2 of Vibrant Villages Programme for villages along international land borders other "
        "than the Northern border (ThePrint)", "sc_vvp_print")],
  why="The Northern border is covered by VVP-I; coastline and LoC-only coverage is not what VVP-II does.",
  current=ca("2025-04-04"))

G(GSC, CS, "Basic",
  "Mission Mausam, approved by the Union Cabinet on 11 September 2024 with an outlay of Rs 2,000 crore over two years "
  "to make India 'weather-ready and climate-smart', is implemented mainly by which ministry?",
  ["Ministry of Earth Sciences", "Ministry of Environment, Forest and Climate Change",
   "Ministry of Agriculture and Farmers Welfare", "Ministry of Home Affairs"], "*",
  "Science missions: weather",
  "The Cabinet approved Mission Mausam on 11 September 2024 with Rs 2,000 crore over two years. The Ministry of Earth "
  "Sciences implements it mainly through the IMD, IITM and NCMRWF, supported by INCOIS and NIOT.",
  ["Mission Mausam: 11 Sep 2024, Rs 2,000 crore", "Ministry of Earth Sciences (IMD, IITM, NCMRWF)"],
  [fact("IMD: Mission Mausam, Ministry of Earth Sciences, implemented by IMD, IITM and NCMRWF", "sc_maus_imd"),
   fact("Cabinet approves Mission Mausam to create a more weather-ready and climate-smart Bharat with an outlay of Rs "
        "2,000 crore over two years", "sc_maus_nm")],
  why="The mission is run by the Ministry of Earth Sciences; the other ministries do not implement it.",
  current=ca("2024-09-11"))

G(GSC, SL, "Basic",
  "The e-Shram portal, the national database of unorganised workers, completed five years on 26 August 2026. About how "
  "many registrations had it recorded by then?",
  ["31.89 crore", "3.19 crore", "89 crore", "11.5 crore"], "*",
  "Labour welfare",
  "Launched by the Ministry of Labour and Employment on 26 August 2021, e-Shram had about 31.89 crore registrations "
  "when it completed five years in August 2026, including around 11.5 lakh platform workers.",
  ["Launched 26 Aug 2021 (Labour Ministry)", "About 31.89 crore registrations by Aug 2026"],
  [fact("e-Shram portal completes five years; over 31.89 crore unorganised workers registered (Free Press Journal)",
        "sc_eshram_fpj"),
   fact("e-Shram portal marks five years with 31.89 crore registrations (IANS, 25 Aug 2026)", "sc_eshram_ians")],
  why="The reported figure is 31.89 crore; 11.5 lakh was the number of platform workers.",
  current=ca("2026-08-25"))

# ------------------------------------------------------------------ Intermediate (2)
G(GSC, SL, "Intermediate",
  "In January 2026 the government provisionally selected five companies, including Godrej & Boyce and Kirloskar "
  "Pneumatic, in the fourth round of the PLI scheme for white goods. Which product's components will all five make?",
  ["Air conditioners", "LED lights", "Washing machines", "Refrigerators"], "*",
  "Production Linked Incentive schemes",
  "On 23 January 2026 the government provisionally selected five of 13 applicants in the fourth round of the PLI scheme "
  "for white goods, committing about Rs 863 crore. All five will make air conditioner components such as compressors, "
  "copper tubes, heat exchangers and BLDC motors. With this round 85 companies have been selected under the scheme.",
  ["4th round: 5 firms, ~Rs 863 crore", "All AC components", "85 firms selected overall"],
  [fact("Govt selects five companies in fourth round of PLI scheme for white goods (AIR, 24 Jan 2026)", "sc_plw_air"),
   fact("PLI White Goods: 5 selected firms (AC components) to achieve Rs 8,337 crore production; 85 companies selected "
        "overall (IANS, 23 Jan 2026)", "sc_plw_ians")],
  why="The five firms will make AC components; the scheme also covers LED lights, but none of these five.",
  current=ca("2026-01-23"))

G(GSC, CS, "Intermediate",
  "The PM GatiShakti National Master Plan for multimodal connectivity, launched on 13 October 2021, runs on a GIS "
  "platform developed by which institute?",
  ["BISAG-N (Bhaskaracharya National Institute for Space Applications and Geo-informatics)",
   "National Remote Sensing Centre (NRSC)", "Centre for Development of Advanced Computing (C-DAC)",
   "National Informatics Centre (NIC)"], "*",
  "Infrastructure planning",
  "PM GatiShakti NMP was launched on 13 October 2021 to integrate infrastructure planning across ministries. Its GIS "
  "platform was developed by BISAG-N, the technical developer and data integrator; at launch 16 ministries were to "
  "share data, and later the platform grew to over 1,600 data layers.",
  ["Launch: 13 Oct 2021", "GIS platform: BISAG-N", "Initially 16 ministries"],
  [fact("PM Narendra Modi launches PM GatiShakti Master Plan for multimodal connectivity (Free Press Journal, 13 Oct "
        "2021)", "sc_gs_fpj"),
   fact("Digital India: PM GatiShakti platform developed by BISAG-N", "sc_gs_di")],
  why="The sources name BISAG-N; NRSC, C-DAC and NIC did not develop the platform.",
  current=ca("2021-10-13"))

# ------------------------------------------------------------------ Advanced (9)
GS(GSC, CS, "Advanced", "the National Critical Mineral Mission approved by the Union Cabinet in January 2025",
   ["Its government outlay is Rs 16,300 crore, with an expected Rs 18,000 crore more from PSUs.",
    "It is to be implemented over three years.",
    "Its total envisaged outlay is Rs 34,300 crore."],
   [True, False, True],
   "Mineral security",
   "The Cabinet approved the NCMM on 29 January 2025 with Rs 16,300 crore of government outlay and an expected Rs "
   "18,000 crore investment by PSUs, a total of Rs 34,300 crore over seven years, so statement 2 is wrong. It covers "
   "exploration, processing, recycling and overseas acquisition of critical minerals.",
   [fact("Cabinet approves National Critical Mineral Mission; anticipates investments of Rs 18,000 crore from PSUs "
         "(ThePrint, 29 Jan 2025)", "sc_ncmm_print"),
    fact("Cabinet approves NCMM with an outlay of Rs 34,300 crore over seven years (PM India)", "sc_ncmm_pmi")],
   why="Statement 2 is wrong: the mission runs over seven years.",
   current=ca("2025-01-29"))

GS(GSC, SL, "Advanced", "the Electronics Component Manufacturing Scheme (ECMS)",
   ["It was notified in April 2025.",
    "In January 2026 its third tranche approved 22 proposals with an expected investment of about Rs 41,863 crore.",
    "It is administered by the Department of Telecommunications."],
   [True, True, False],
   "Electronics manufacturing",
   "ECMS was notified on 8 April 2025. MeitY cleared its third tranche on 2 January 2026: 22 proposals with expected "
   "investment of Rs 41,863 crore. The scheme is administered by the Ministry of Electronics and Information Technology "
   "(MeitY), not the Department of Telecommunications, so statement 3 is wrong.",
   [fact("Third tranche of ECMS approved with Rs 41,863 crore investment covering 22 applications; scheme notified in "
         "April 2025 (Tribune/ANI, Jan 2026)", "sc_ecms_tr"),
    fact("MeitY clears 22 electronics component projects worth Rs 41,863 crore (Business Today, 2 Jan 2026)",
         "sc_ecms_bt")],
   why="Statement 3 is wrong: ECMS is administered by MeitY.",
   current=ca("2026-01-02"))

GS(GSC, CS, "Advanced", "the IndiaAI Mission approved by the Union Cabinet in March 2024",
   ["Its approved outlay is Rs 10,371.92 crore.",
    "It plans AI compute infrastructure of 10,000 or more GPUs through public-private partnership.",
    "It is implemented by the Department of Science and Technology through the Indian Statistical Institute."],
   [True, True, False],
   "Digital technology missions",
   "The Cabinet approved the IndiaAI Mission on 7 March 2024 with Rs 10,371.92 crore. It plans AI compute capacity of "
   "10,000 or more GPUs through public-private partnership. It is run by the IndiaAI Independent Business Division "
   "under Digital India Corporation (MeitY), so statement 3 is wrong.",
   [fact("Cabinet approves IndiaAI Mission; Rs 10,371.92 crore; AI compute of 10,000 or more GPUs via PPP (PM India, "
         "7 Mar 2024)", "sc_ai_pmi"),
    fact("Government approves IndiaAI Mission with outlay of Rs 10,372 crore; IndiaAI IBD under Digital India "
         "Corporation (India TV, 7 Mar 2024)", "sc_ai_itv")],
   why="Statement 3 is wrong: the mission is implemented through the IndiaAI IBD under Digital India Corporation.",
   current=ca("2024-03-07"))

GS(GSC, CS, "Advanced", "the Digital Agriculture Mission approved by the Union Cabinet in September 2024",
   ["Its total outlay is Rs 2,817 crore, including a central share of Rs 1,940 crore.",
    "AgriStack, the Krishi Decision Support System and Soil Profile Mapping are its digital public infrastructure "
    "components.",
    "AgriStack gives farmers an Aadhaar-linked unique Farmer ID linked to land records."],
   [True, True, True],
   "Digital agriculture",
   "The Cabinet approved the Digital Agriculture Mission on 2 September 2024 with an outlay of Rs 2,817 crore (central "
   "share Rs 1,940 crore). Its DPI components are AgriStack, the Krishi Decision Support System and Soil Profile "
   "Mapping; AgriStack's Farmer Registry gives each farmer an Aadhaar-linked Farmer ID linked to land records. All "
   "three statements are correct.",
   [fact("Cabinet approves Digital Agriculture Mission with Rs 2,817 crore outlay (central share Rs 1,940 crore); "
         "AgriStack, Krishi DSS, soil profile mapping (ThePrint, 2 Sep 2024)", "sc_dam_print"),
    fact("Cabinet approves digital agri mission with Rs 2,817 cr outlay (BW Businessworld)", "sc_dam_bw")],
   why="All three statements are correct.",
   current=ca("2024-09-02"))

GS(GSC, CS, "Advanced", "the Deep Ocean Mission of the Ministry of Earth Sciences",
   ["It was approved with an outlay of about Rs 4,077 crore over five years.",
    "Its crewed submersible MATSYA 6000 is being developed by ISRO's Vikram Sarabhai Space Centre.",
    "Under 'Samudrayaan' it aims to take humans to a depth of 6,000 metres."],
   [True, False, True],
   "Science missions: oceans",
   "The Deep Ocean Mission was approved with about Rs 4,077 crore for five years. Its Samudrayaan component aims to take "
   "humans to 6,000 m in the submersible MATSYA 6000, which is designed and developed by the National Institute "
   "of Ocean Technology (NIOT), Chennai, so statement 2 is wrong.",
   [fact("Samudrayaan: India's first manned mission to send humans 6,000 m deep in ocean; Deep Ocean Mission Rs 4,077 "
         "crore; NIOT Chennai developing MATSYA 6000 (Business Standard, Aug 2022)", "sc_dom_bs"),
    fact("Samudrayaan: India's first mission to send humans 6,000 metres deep in ocean (TBS News)", "sc_dom_tbs")],
   why="Statement 2 is wrong: MATSYA 6000 is developed by NIOT, Chennai.")

GS(GSC, SL, "Advanced", "the Green Energy Corridor Phase-III approved by the Union Cabinet on 30 September 2026",
   ["Its total outlay is about Rs 1.86 lakh crore, including Rs 50,000 crore for 50 GWh of battery energy storage.",
    "It aims to enable evacuation of up to 135 GW of renewable energy.",
    "It focuses only on inter-State transmission lines built by central PSUs."],
   [True, True, False],
   "Power transmission",
   "GEC-III, approved on 30 September 2026, has an outlay of about Rs 1,86,405 crore: Rs 1,36,378 crore for intra-State "
   "transmission systems and Rs 50,000 crore for 50 GWh of battery storage. It aims to evacuate up to 135 GW of "
   "renewable energy by FY 2032-33. It focuses on intra-State transmission, so statement 3 is wrong.",
   [fact("Cabinet approves Green Energy Corridor Phase-III scheme (Renewable Watch, 1 Oct 2026)", "sc_gec_rw"),
    fact("India clears Rs 1.86 lakh crore Green Energy Corridor III to evacuate 135 GW renewables, deploy 50 GWh BESS; "
         "intra-State transmission (Swarajya)", "sc_gec_sw")],
   why="Statement 3 is wrong: GEC-III is for intra-State transmission (with battery storage).",
   current=ca("2026-09-30"))

GS(GSC, CS, "Advanced", "PM-PRANAM (PM Programme for Restoration, Awareness, Nourishment and Amelioration of Mother "
   "Earth)",
   ["It has a separate budgetary allocation of Rs 10,000 crore a year.",
    "States and UTs get a grant of 50% of the fertiliser subsidy saved by reducing chemical fertiliser use compared "
    "with the previous three years' average.",
    "It was approved in June 2023."],
   [False, True, True],
   "Sustainable agriculture",
   "PM-PRANAM, approved in June 2023, rewards States and UTs that reduce chemical fertiliser use: they get 50% of the "
   "subsidy saved compared with the previous three years' average consumption. It has no separate budget and is "
   "financed from savings in existing fertiliser subsidy, so statement 1 is wrong.",
   [fact("Lok Sabha answer: PM-PRANAM grant of 50% of fertiliser subsidy saved by a State/UT versus previous 3 years' "
         "average consumption", "sc_pran_ls"),
    fact("PM-PRANAM approved in June 2023; no separate budget, financed from fertiliser subsidy savings (Down To Earth)",
         "sc_pran_dte")],
   why="Statement 1 is wrong: the scheme has no separate budget.")

GS(GSC, CS, "Advanced", "the Anusandhan National Research Foundation (ANRF)",
   ["It was set up under an Act passed by Parliament in 2023.",
    "Its estimated funding for 2023-28 is about Rs 50,000 crore, of which most is expected from non-government sources.",
    "Its Governing Board is chaired by the Union Minister of Science and Technology."],
   [True, True, False],
   "Research funding",
   "Parliament passed the Anusandhan National Research Foundation Bill in 2023. The ANRF's estimated cost for 2023-28 is "
   "about Rs 50,000 crore, with roughly 70% expected from non-government (mainly private) sources and about Rs 10,000 "
   "crore from the government. Its Governing Board is headed by the Prime Minister, so statement 3 is wrong.",
   [fact("Parliament passes Anusandhan National Research Foundation (NRF) Bill, 2023 (DST)", "sc_anrf_dst"),
    fact("ANRF: Rs 50,000 crore over five years, about 72% from private sources; only Rs 10,000 crore from the exchequer "
         "(Down To Earth)", "sc_anrf_dte")],
   why="Statement 3 is wrong: the ANRF Governing Board is chaired by the Prime Minister.")

GS(GSC, CS, "Advanced", "the Sagarmala Programme",
   ["It was launched in 2015 to promote port-led development.",
    "It is implemented by the Ministry of Ports, Shipping and Waterways.",
    "The Sagarmala Development Company Ltd. invests through equity in project-specific SPVs."],
   [True, True, True],
   "Maritime infrastructure",
   "The Sagarmala Programme was launched in March 2015 to promote port-led development, with pillars covering port "
   "modernisation, port connectivity, port-led industrialisation, coastal community development and coastal shipping/"
   "inland water transport. It is implemented by the Ministry of Ports, Shipping and Waterways, and the Sagarmala "
   "Development Company provides equity support to project SPVs. All three statements are correct.",
   [fact("Sagarmala Programme aims to reduce logistics costs: views of the MD, Sagarmala Development Company; equity in "
         "project SPVs (Indian Infrastructure, Feb 2022)", "sc_sag_ii"),
    fact("Sagarmala aims to promote port-led development in India; launched 2015 (Maritime Professional)", "sc_sag_mp")],
   why="All three statements are correct.")

# ###################################################################### part: appt (Appointments, Awards)
U.update({
    "ap_bis": ("https://www.bis.org/press/p260512.htm", OPENED, "2026-11-07"),
    "ap_bis_gbf": ("https://www.globalbankingandfinance.com/italys-panetta-chair-central-bank-group-bis-board-directors/",
                   SEARCH, "2026-11-07"),
    "ap_kim_aa": ("https://allafrica.com/stories/202609150262.html", SEARCH, "2026-11-07"),
    "ap_kim_nation": ("https://nation.africa/kenya/news/martin-kimani-lands-senior-un-job-on-africa-affairs-5595434",
                      SEARCH, "2026-11-07"),
    "ap_ntsl": ("https://www.medianews4u.com/npci-sets-up-wholly-owned-technology-subsidiary-ntsl-appoints-vishal-kanvaty-"
                "as-md-ceo/", OPENED, "2026-11-07"),
    "ap_unido_it": ("https://italiarappvienna.esteri.it/en/news/dalla_rappresentanza/2025/11/italy-at-the-21st-unido-"
                    "general-conference-global-industry-summit-2025/", OPENED, "2026-11-07"),
    "ap_unido_g77": ("https://www.g77.org/vienna/wp-content/uploads/2025/11/G-77-and-China-Item-6-Appointment-of-the-DG-"
                     "LONG-VERSION-adopted-.pdf", SEARCH, "2026-11-07"),
})
APP = "Important Appointments"
BFH, IB = "Banking and finance heads", "International bodies"

G(APP, BFH, "Basic",
  "In May 2026, the Bank for International Settlements announced that the Governor of the Bank of Japan would chair "
  "its Committee on the Global Financial System for three years, succeeding Chang Yong Rhee. Who is he?",
  ["Kazuo Ueda", "Haruhiko Kuroda", "Masayoshi Amamiya", "Shunichi Suzuki"], "*",
  "Central bankers in international bodies",
  "The BIS announced on 12 May 2026 that Kazuo Ueda, Governor of the Bank of Japan, had been appointed Chair of the "
  "Committee on the Global Financial System for three years from 12 May, succeeding Chang Yong Rhee.",
  ["CGFS chair: Kazuo Ueda (BoJ Governor)", "From 12 May 2026, three years", "Succeeds Chang Yong Rhee"],
  [fact("BIS release of 12 May 2026: Kazuo Ueda, Governor of the Bank of Japan, appointed Chair of the CGFS for three "
        "years from 12 May, succeeding Chang Yong Rhee", "ap_bis")],
  why="The BIS release names Kazuo Ueda; the others are not the current Governor of the Bank of Japan named there.",
  current=ca("2026-05-12"))

G(APP, IB, "Basic",
  "Kenyan diplomat Martin Kimani, Kenya's Permanent Representative to the UN from 2020 to 2024, was appointed by the "
  "UN Secretary-General on 14 September 2026 as Assistant Secretary-General for which region in the UN's political "
  "and peace operations departments?",
  ["Africa", "Middle East and Asia-Pacific", "Europe and Central Asia", "the Americas"], "*",
  "UN appointments",
  "On 14 September 2026 UN Secretary-General Antonio Guterres appointed Martin Kimani of Kenya as Assistant "
  "Secretary-General for Africa in the Departments of Political and Peacebuilding Affairs and Peace Operations, "
  "replacing Martha Ama Akyaa Pobee of Ghana.",
  ["Martin Kimani (Kenya)", "UN ASG for Africa (DPPA-DPO)", "Appointed 14 Sep 2026; succeeds Martha Pobee"],
  [fact("Martin Kimani named UN Assistant Secretary-General for Africa (AllAfrica, 15 Sep 2026)", "ap_kim_aa"),
   fact("Ex-envoy Martin Kimani lands senior UN job on Africa affairs (Nation)", "ap_kim_nation")],
  why="The sources name the Africa portfolio; the other regions are not his responsibility.",
  current=ca("2026-09-14"))

G(APP, BFH, "Intermediate",
  "In November 2026, the National Payments Corporation of India set up a wholly owned technology subsidiary, NPCI Tech "
  "Solutions Limited (NTSL). Who was appointed its MD and CEO?",
  ["Vishal Kanvaty", "Dilip Asbe", "Praveena Rai", "Ritesh Shukla"], "*",
  "Payments infrastructure: leadership",
  "NPCI set up NPCI Tech Solutions Limited (NTSL) as its technology and innovation arm, to build capabilities in AI, "
  "blockchain and digital financial infrastructure and to run services such as eKYC Setu and the Unified Ticketing "
  "Platform. Vishal Kanvaty, associated with NPCI for nearly a decade, was appointed its MD and CEO.",
  ["NTSL: wholly owned NPCI subsidiary (tech arm)", "MD & CEO: Vishal Kanvaty"],
  [fact("NPCI sets up wholly owned technology subsidiary NTSL; appoints Vishal Kanvaty as MD & CEO (MediaNews4U, 4 Nov "
        "2026)", "ap_ntsl")],
  why="The source names Vishal Kanvaty; the others are not named for this post.",
  current=ca("2026-11-04"))

U.update({
    "ap_ala_trend": ("https://www.trend.az/azerbaijan/4230743.html", SEARCH, "2026-11-07"),
    "ap_ala_un": ("https://press.un.org/en/2026/sga2443.doc.htm", SEARCH, "2026-11-07"),
    "ap_des_tass": ("https://tass.com/world/2209127", SEARCH, "2026-11-07"),
    "ap_des_pr": ("https://www.pravda.com.ua/eng/news/2026/10/28/8060013/", SEARCH, "2026-11-07"),
    "ap_jam_gl": ("https://jamaica-gleaner.com/article/news/20260818/dr-brian-langrin-appointed-new-bank-jamaica-governor",
                  SEARCH, "2026-11-07"),
    "ap_jam_gl2": ("https://jamaica-gleaner.com/article/news/20260818/langrin-takes-helm", SEARCH, "2026-11-07"),
})

G(APP, IB, "Basic",
  "Ramiz Alakbarov, appointed by the UN Secretary-General in October 2026 as Assistant Secretary-General for Safety and "
  "Security from January 2027, is a national of which country?",
  ["Azerbaijan", "Kazakhstan", "Turkiye", "Georgia"], "*",
  "UN appointments",
  "The UN announced in early October 2026 that Ramiz Alakbarov of Azerbaijan would become Assistant Secretary-General "
  "for Safety and Security in January 2027, succeeding Unaisi Vuniwaqa of Fiji. He earlier served as the UN's Deputy "
  "Special Representative for Afghanistan and Resident Coordinator in Ethiopia.",
  ["Ramiz Alakbarov (Azerbaijan)", "UN ASG, Department of Safety and Security, from Jan 2027"],
  [fact("UN appoints Ramiz Alakbarov of Azerbaijan as Assistant Secretary-General for Security (Trend, 3 Oct 2026)",
        "ap_ala_trend"),
   fact("UN press release SG/A/2443: Ramiz Alakbarov of Azerbaijan, Assistant Secretary-General for Safety and Security, "
        "succeeding Unaisi Vuniwaqa", "ap_ala_un")],
  why="The sources identify him as Azerbaijani.",
  current=ca("2026-10-02", inferred="UN release reported on 2-3 October 2026; exact day not stated in the sources"))

G(APP, BFH, "Basic",
  "Dr R. Brian Langrin took charge in August 2026 as Governor of which central bank, succeeding Richard Byles?",
  ["Bank of Jamaica", "Central Bank of Trinidad and Tobago", "Central Bank of The Bahamas", "Bank of Guyana"], "*",
  "Central bank governors",
  "Dr R. Brian Langrin was appointed Governor of the Bank of Jamaica, succeeding Richard Byles, whose seven-year tenure "
  "ended on 18 August 2026; he took the helm that week.",
  ["Bank of Jamaica Governor: Brian Langrin (Aug 2026)", "Succeeded Richard Byles"],
  [fact("Dr Brian Langrin appointed new Bank of Jamaica governor, succeeding Richard Byles (Jamaica Gleaner, 18 Aug 2026)",
        "ap_jam_gl"),
   fact("Langrin takes helm (Jamaica Gleaner, 18 Aug 2026)", "ap_jam_gl2")],
  why="The source names the Bank of Jamaica; the other central banks are not involved.",
  current=ca("2026-08-18"))

G(APP, IB, "Intermediate",
  "In October 2026 the UN Secretary-General appointed Russian diplomat Gleb Desyatnikov as Assistant Secretary-General "
  "for which portfolio in the Department of Peace Operations?",
  ["Mine Action and Police", "Political Affairs for Europe", "Disarmament Affairs", "Peacebuilding Support"], "*",
  "UN appointments",
  "UN Secretary-General Antonio Guterres appointed Gleb Desyatnikov of Russia as Assistant Secretary-General for Mine "
  "Action and Police in the Department of Peace Operations, as reported on 28 October 2026; the UN said he had more than "
  "35 years of experience in international relations and security.",
  ["Gleb Desyatnikov (Russia)", "UN ASG for Mine Action and Police, DPO (Oct 2026)"],
  [fact("Guterres appoints Gleb Desyatnikov as Assistant Secretary General for Mine Action and Police in the Department "
        "of Peace Operations (TASS)", "ap_des_tass"),
   fact("UN chief appoints Russian diplomat to oversee mine action and police (Ukrainska Pravda, 28 Oct 2026)",
        "ap_des_pr")],
  why="The sources name the Mine Action and Police portfolio.",
  current=ca("2026-10-28"))

GS(APP, IB, "Advanced", "the 21st session of the UNIDO General Conference",
   ["It was held in Vienna, Austria, in November 2025.",
    "It confirmed Director General Gerd Mueller for an additional four-year term.",
    "A resolution adopted there created an International Day of Women in Industry, to be marked on 21 April."],
   [False, True, True],
   "UN agencies: leadership",
   "The 21st UNIDO General Conference was held in Riyadh, Saudi Arabia, from 23 to 27 November 2025, so statement 1 is "
   "wrong. It confirmed Director General Gerd Mueller for an additional four-year term, adopted the Riyadh Declaration "
   "by acclamation and approved four resolutions; the gender resolution created an International Day of Women in "
   "Industry on 21 April.",
   [fact("21st UNIDO General Conference in Riyadh, 23-27 November 2025; DG Gerd Mueller confirmed for an additional "
         "four-year term; Riyadh Declaration; International Day of Women in Industry on 21 April (Italian Permanent "
         "Mission, Vienna, 28 Nov 2025)", "ap_unido_it"),
    fact("G-77 and China statement on Item 6: appointment of the Director General (Nov 2025)", "ap_unido_g77")],
   why="Statement 1 is wrong: the session was held in Riyadh, Saudi Arabia.",
   current=ca("2025-11-27", inferred="source gives the session dates 23-27 Nov 2025, not the day of the decision"))


# ====================================================================== Awards and Honours
U.update({
    "aw_tony_bd": ("https://broadwaydirect.com/the-2026-tony-award-winners/", SEARCH, "2026-11-07"),
    "aw_tony_ams": ("https://amsterdamnews.com/news/2026/06/08/a-select-list-of-winners-at-the-2026-tony-awards/", SEARCH,
                    "2026-11-07"),
    "aw_gon_eu": ("https://www.euronews.com/2026/11/03/philippe-jaenada-wins-2026-prix-goncourt-for-novel-linconnue-du-"
                  "quai-de-javel", SEARCH, "2026-11-07"),
    "aw_gon_cf": ("https://www.connexionfrance.com/news/prix-goncourt-2026-frances-top-literary-prize-awarded-to-"
                  "philippe-jaenada/826090", SEARCH, "2026-11-07"),
    "aw_aapda_st": ("https://www.thestatesman.com/india/ssdma-lt-col-seeta-ashok-shelke-selected-for-subhash-chandra-"
                    "bose-aapda-prabandhan-puraskar-2026-1503545287.html", SEARCH, "2026-11-07"),
    "aw_aapda_nis": ("https://newindiasamachar.pib.gov.in/WriteReadData/flipbook/2026/Feb/2nd/English/files/basic-html/"
                     "page53.html", SEARCH, "2026-11-07"),
    "aw_koch_fpa": ("https://www.fpa.es/en/area-of-communication-and-media/press-releases/christina-koch-2026-princess-of-"
                    "asturias-award-for-concord/", OPENED, "2026-11-07"),
    "aw_balzan": ("https://www.balzan.org/en/updates/the-2026-balzan-prizewinners", OPENED, "2026-11-07"),
    "aw_iffco_pio": ("https://dailypioneer.com/news/maitreyi-pushpa-gets-iffco-sahitya-samman-ankita-jain-wins-yuva-prize",
                     SEARCH, "2026-11-07"),
    "aw_iffco_ic": ("https://www.indiancooperative.com/featured/iffco-names-maitreyi-pushpa-ankita-jain-for-2025-literary-"
                    "honours/", SEARCH, "2026-11-07"),
    "aw_gep_kyodo": ("https://kyodonewsprwire.jp/release/202607142541", SEARCH, "2026-11-07"),
    "aw_gep_renew": ("https://www.iamrenew.com/environment/news-pollution-fight/global-energy-prize-2026-celebrates-three-"
                     "energy-innovators/amp/", SEARCH, "2026-11-07"),
    "aw_iffi_air": ("https://www.newsonair.gov.in/56th-iffi-concludes-in-goa-skin-of-youth-wins-golden-peacock-for-best-"
                    "feature-film", SEARCH, "2026-11-07"),
    "aw_iffi_cin": ("https://cineuropa.org/en/newsdetail/486631", SEARCH, "2026-11-07"),
    "aw_rvp_air": ("https://www.newsonair.gov.in/president-droupadi-murmu-confers-rashtriya-vigyan-puraskar-2025", SEARCH,
                   "2026-11-07"),
    "aw_rvp_st": ("https://www.thestatesman.com/india/prez-murmu-presents-rashtriya-vigyan-puraskar-2025-1503529794.html",
                  SEARCH, "2026-11-07"),
    "aw_zsp_bw": ("https://businesswire.com/news/home/20260113958706/en/Zayed-Sustainability-Prize-Honours-Global-Pioneers-"
                  "Advancing-Progress", SEARCH, "2026-11-07"),
    "aw_zsp_kt": ("https://www.khaleejtimes.com/uae/zayed-sustainability-prize-2026-winners", SEARCH, "2026-11-07"),
    "aw_ab_air": ("https://newsonair.gov.in/pm-narendra-modi-congratulates-major-abhilasha-barak-on-un-honour/", OPENED,
                  "2026-11-06"),
    "aw_ab_print": ("https://theprint.in/world/major-abhilasha-barak-of-india-to-receive-2025-un-military-gender-advocate-"
                    "of-the-year-award/2939211/", OPENED, "2026-11-07"),
})
AW = "Awards and Honours"
NA, IA = "National awards", "International awards"

G(AW, IA, "Basic",
  "Which show won the Tony Award for Best Musical at the 79th Tony Awards held on 7 June 2026?",
  ["Schmigadoon!", "Ragtime", "Death of a Salesman", "Liberation"], "*",
  "Theatre awards",
  "At the 79th Tony Awards at Radio City Music Hall on 7 June 2026, 'Schmigadoon!' won Best Musical (also Best Book and "
  "Best Original Score) and Bess Wohl's 'Liberation' won Best Play; 'Ragtime' won Best Revival of a Musical and "
  "'Death of a Salesman' Best Revival of a Play.",
  ["Best Musical: Schmigadoon!", "Best Play: Liberation", "Revivals: Ragtime (musical), Death of a Salesman (play)"],
  [fact("2026 Tony Award winners: Best Musical Schmigadoon!; Best Play Liberation (Broadway Direct)", "aw_tony_bd"),
   fact("A select list of winners at the 2026 Tony Awards (Amsterdam News/AP, 8 June 2026)", "aw_tony_ams")],
  why="'Ragtime' and 'Death of a Salesman' won revival awards and 'Liberation' won Best Play, not Best Musical.",
  current=ca("2026-06-07"))

G(AW, IA, "Intermediate",
  "The Prix Goncourt 2026, France's top literary prize, was awarded on 3 November 2026 to Philippe Jaenada for which "
  "novel, about the killing of a young artists' model in postwar Paris?",
  ["L'Inconnue du quai de Javel", "La Maison vide", "De l'autre cote du lac", "Le Palais"], "*",
  "Literary awards: France",
  "The Academie Goncourt awarded the 2026 prize on 3 November 2026 to Philippe Jaenada for 'L'Inconnue du quai de "
  "Javel' (Flammarion), a crime story set in postwar Paris; he succeeds Laurent Mauvignier, the 2025 winner.",
  ["Goncourt 2026: Philippe Jaenada", "Novel: L'Inconnue du quai de Javel (Flammarion)"],
  [fact("Philippe Jaenada wins 2026 Prix Goncourt for novel L'Inconnue du quai de Javel (Euronews, 3 Nov 2026)",
        "aw_gon_eu"),
   fact("Prix Goncourt 2026, France's top literary prize, awarded to Philippe Jaenada (Connexion France)", "aw_gon_cf")],
  why="The sources name 'L'Inconnue du quai de Javel'; the other titles did not win the 2026 Goncourt.",
  current=ca("2026-11-03"))

G(AW, NA, "Intermediate",
  "Which institution was selected in the institutional category for the Subhash Chandra Bose Aapda Prabandhan Puraskar "
  "2026, announced on 23 January 2026?",
  ["Sikkim State Disaster Management Authority", "Odisha State Disaster Management Authority",
   "National Disaster Response Force", "Kerala State Disaster Management Authority"], "*",
  "National awards: disaster management",
  "Announced on 23 January 2026, Netaji Subhas Chandra Bose's birth anniversary, the 2026 Subhash Chandra Bose Aapda "
  "Prabandhan Puraskar went to the Sikkim State Disaster Management Authority (institutional category) and Lt Col "
  "Seeta Ashok Shelke of the Army (individual category).",
  ["Announced every 23 January", "2026 institution: Sikkim SDMA", "2026 individual: Lt Col Seeta Ashok Shelke"],
  [fact("SSDMA, Lt Col Seeta Ashok Shelke selected for Subhash Chandra Bose Aapda Prabandhan Puraskar 2026 (The "
        "Statesman)", "aw_aapda_st"),
   fact("New India Samachar (16-28 Feb 2026): Subhash Chandra Bose Aapda Prabandhan Puraskar 2026 winners",
        "aw_aapda_nis")],
  why="The sources name the Sikkim SDMA; the other bodies were not selected for 2026.",
  current=ca("2026-01-23"))

G(AW, IA, "Intermediate",
  "American astronaut Christina Koch, praised by the jury as the first woman to travel far enough to escape Earth's "
  "magnetic field and reach deep space on the Artemis II mission, won which 2026 Princess of Asturias Award?",
  ["Concord", "Technical and Scientific Research", "International Cooperation", "Communication and Humanities"], "*",
  "International awards: Spain",
  "On 17 June 2026 the Princess of Asturias Foundation announced Christina Koch as the 2026 laureate of the Award for "
  "Concord, the eighth and last of that year's awards. The award carries EUR 50,000 and a Joan Miro sculpture.",
  ["Princess of Asturias Award for Concord 2026: Christina Koch", "Announced 17 June 2026 (8th and last of 2026)"],
  [fact("Christina Koch, 2026 Princess of Asturias Award for Concord; first woman to reach deep space on Artemis II; "
        "eighth and last award of the year; EUR 50,000 and a Joan Miro sculpture (FPA, 17 June 2026)", "aw_koch_fpa")],
  why="The Foundation's release names the Concord award; the other categories went to others.",
  current=ca("2026-06-17"))

G(AW, IA, "Intermediate",
  "The 2026 Balzan Prize for Humanity, Peace and Fraternity among Peoples, announced on 7 September 2026, was awarded "
  "to the Emergency Response Rooms of which country?",
  ["Sudan", "Gaza (Palestine)", "Ukraine", "Myanmar"], "*",
  "International awards: Balzan Prize",
  "The International Balzan Prize Foundation announced its 2026 prizewinners on 7 September 2026. Besides the four "
  "subject prizes (to Elena Esposito; Rasmus Nielsen and Ziheng Yang; David Nirenberg; and Geoffrey Coates and Marc "
  "Hillmyer), the Prize for Humanity, Peace and Fraternity among Peoples went to Sudan's Emergency Response Rooms. "
  "Each prize is worth 750,000 Swiss francs.",
  ["Balzan 2026 announced 7 Sep 2026", "Humanity prize: Emergency Response Rooms (Sudan)", "CHF 750,000 per prize"],
  [fact("The 2026 Balzan Prizewinners: Esposito; Nielsen and Yang; Nirenberg; Coates and Hillmyer; Emergency Response "
        "Rooms (Sudan) - Prize for Humanity, Peace and Fraternity among Peoples; CHF 750,000 each (Balzan Foundation, "
        "7 Sep 2026)", "aw_balzan")],
  why="The Foundation names Sudan's Emergency Response Rooms; the other places are not mentioned.",
  current=ca("2026-09-07"))

G(AW, NA, "Intermediate",
  "Which Hindi writer received the IFFCO Sahitya Samman 2025, presented at Kamani Auditorium, New Delhi, on 30 "
  "December 2025?",
  ["Maitreyi Pushpa", "Ankita Jain", "Chandrakishore Jaiswal", "Madhu Kankariya"], "*",
  "Literary awards: Hindi",
  "IFFCO Chairman Dilip Sanghani presented the IFFCO Sahitya Samman 2025 to Maitreyi Pushpa and the IFFCO Yuva Sahitya "
  "Samman 2025 to Ankita Jain (for 'Oh Re! Kisan') on 30 December 2025 in New Delhi. The jury was chaired by "
  "Chandrakanta; the award, instituted in 2011, carries Rs 11 lakh.",
  ["IFFCO Sahitya Samman 2025: Maitreyi Pushpa", "Yuva Samman 2025: Ankita Jain", "Presented 30 Dec 2025"],
  [fact("Maitreyi Pushpa gets IFFCO Sahitya Samman; Ankita Jain wins Yuva prize (The Pioneer)", "aw_iffco_pio"),
   fact("IFFCO names Maitreyi Pushpa, Ankita Jain for 2025 literary honours (Indian Cooperative)", "aw_iffco_ic")],
  why="Ankita Jain won the Yuva award; Jaiswal and Kankariya were earlier winners.",
  current=ca("2025-12-30"))

G(AW, IA, "Intermediate",
  "The laureates of the Global Energy Prize 2026, announced on 14 July 2026, were Yilu Liu and Yushan Yan of the United "
  "States and Johann W. Kolar, a researcher based in which country?",
  ["Switzerland", "Germany", "Sweden", "Netherlands"], "*",
  "International awards: energy",
  "The Global Energy Prize 2026 laureates were announced on 14 July 2026 at the Oil Summit of the Republic of "
  "Tatarstan: two scientists from the United States, Yilu Liu and Yushan Yan, and a researcher from Switzerland, "
  "Johann W. Kolar.",
  ["Global Energy Prize 2026 (14 July 2026)", "Laureates: Yilu Liu, Yushan Yan (USA); Johann W. Kolar (Switzerland)"],
  [fact("Yilu Liu, Yushan Yan, Johann W. Kolar chosen as laureates of the Global Energy Prize 2026; two scientists from "
        "the United States and a researcher from Switzerland (PR Newswire/Kyodo, 14 July 2026)", "aw_gep_kyodo"),
   fact("Global Energy Prize 2026 celebrates three energy innovators (iamrenew)", "aw_gep_renew")],
  why="The release describes Kolar as a researcher from Switzerland (he works at ETH Zurich); the other countries are "
      "not named.",
  current=ca("2026-07-14"))

G(AW, IA, "Intermediate",
  "Which film won the Golden Peacock for Best Feature Film at the 56th International Film Festival of India (IFFI), "
  "which concluded in Goa on 28 November 2025?",
  ["Skin of Youth", "Gondhal", "Safe House", "My Father's Shadow"], "*",
  "Film awards: IFFI",
  "The Vietnamese film 'Skin of Youth', directed by Ash Mayfair, won the Golden Peacock at the 56th IFFI (Goa, 20-28 "
  "November 2025). Santosh Davakhar won the Silver Peacock for Best Director for the Marathi film 'Gondhal', 'Safe "
  "House' won the Gandhi Medal, and Akinola Davies Jr won the Special Jury Award for 'My Father's Shadow'.",
  ["Golden Peacock: Skin of Youth (Vietnam)", "Best Director: Santosh Davakhar (Gondhal)", "Gandhi Medal: Safe House"],
  [fact("56th IFFI concludes in Goa; 'Skin of Youth' wins Golden Peacock for Best Feature Film (AIR, 28-29 Nov 2025)",
        "aw_iffi_air"),
   fact("IFFI 2025 awards: Skin of Youth wins the Golden Peacock (Cineuropa)", "aw_iffi_cin")],
  why="'Gondhal', 'Safe House' and 'My Father's Shadow' won other IFFI awards, not the Golden Peacock.",
  current=ca("2025-11-28"))

G(AW, NA, "Intermediate",
  "At the Rashtriya Vigyan Puraskar 2025 ceremony at Rashtrapati Bhavan on 23 December 2025, the Vigyan Ratna was "
  "conferred posthumously on which astrophysicist?",
  ["Jayant Vishnu Narlikar", "Govindarajan Padmanabhan", "C. N. R. Rao", "K. Kasturirangan"], "*",
  "National science awards",
  "President Droupadi Murmu presented the Rashtriya Vigyan Puraskar 2025 on 23 December 2025, the second edition of "
  "these awards. The Vigyan Ratna went posthumously to astrophysicist Jayant Vishnu Narlikar, known for the "
  "Hoyle-Narlikar theory, and the Vigyan Team award to the CSIR Aroma Mission. The first Vigyan Ratna (2024) went to "
  "biochemist G. Padmanabhan.",
  ["RVP 2025 presented 23 Dec 2025", "Vigyan Ratna (posthumous): Jayant Narlikar", "Vigyan Team: CSIR Aroma Mission"],
  [fact("President Droupadi Murmu confers Rashtriya Vigyan Puraskar 2025 (AIR, 23 Dec 2025)", "aw_rvp_air"),
   fact("Prez Murmu presents Rashtriya Vigyan Puraskar 2025; Vigyan Ratna posthumously to Jayant Vishnu Narlikar (The "
        "Statesman)", "aw_rvp_st")],
  why="Padmanabhan received the first Vigyan Ratna in 2024; the others were not honoured at this ceremony.",
  current=ca("2025-12-23"))

G(AW, IA, "Intermediate",
  "The Zayed Sustainability Prize 2026, which awarded about US$5.9 million to 11 organisations and high schools across "
  "six categories, was presented by UAE President Sheikh Mohamed bin Zayed during which event?",
  ["Abu Dhabi Sustainability Week", "World Government Summit", "COP31", "World Future Energy Summit in Riyadh"], "*",
  "International awards: sustainability",
  "The 2026 Zayed Sustainability Prize winners were honoured at an awards ceremony held during Abu Dhabi Sustainability "
  "Week in January 2026, where UAE President Sheikh Mohamed bin Zayed Al Nahyan presented about US$5.9 million to 11 "
  "winners from the UAE, Brazil, Canada, Nepal, Switzerland, Uganda and other countries across Health, Food, Energy, "
  "Water, Climate Action and Global High Schools.",
  ["Zayed Sustainability Prize 2026: Abu Dhabi Sustainability Week", "US$5.9 million to 11 winners, 6 categories"],
  [fact("Zayed Sustainability Prize honours global pioneers advancing progress; ceremony during Abu Dhabi Sustainability "
        "Week; US$5.9M to 11 winners (Business Wire, 13 Jan 2026)", "aw_zsp_bw"),
   fact("Meet UAE's Zayed Sustainability Prize 2026 winners (Khaleej Times)", "aw_zsp_kt")],
  why="The sources place the ceremony at Abu Dhabi Sustainability Week; the other events are not mentioned.",
  current=ca("2026-01-13"))

GS(AW, IA, "Advanced", "Major Abhilasha Barak and the 2025 UN Military Gender Advocate of the Year Award",
   ["She serves with the Indian Battalion in UNIFIL, Lebanon, as Commander of the Female Engagement Team.",
    "She is the first Indian peacekeeper to receive this award.",
    "The award was created in 2016 by the Office of Military Affairs in the UN Department of Peace Operations."],
   [True, False, True],
   "International awards: UN peacekeeping",
   "Major Abhilasha Barak of the Indian Army, serving with the Indian Battalion in UNIFIL, Lebanon, as Commander of the "
   "Female Engagement Team, was chosen for the 2025 UN Military Gender Advocate of the Year Award, to be presented on the "
   "International Day of UN Peacekeepers (29 May 2026). She is not the first Indian winner: Major Suman Gawani (2019, "
   "UNMISS) and Major Radhika Sen (2023, MONUSCO) won earlier, so statement 2 is wrong. The award was created in 2016 by "
   "the Office of Military Affairs in the Department of Peace Operations.",
   [fact("Major Abhilasha Barak, Commander of the Female Engagement Team with the Indian Battalion in UNIFIL; earlier "
         "Indian winners Maj Suman Gawani (2019) and Maj Radhika Sen (2023); award created in 2016 by the Office of "
         "Military Affairs, DPO (ThePrint/PTI, 23 May 2026)", "aw_ab_print"),
    fact("PM congratulates Major Abhilasha Barak on the UN Military Gender Advocate of the Year Award; UNIFIL (AIR, 7 June "
         "2026)", "aw_ab_air")],
   why="Statement 2 is wrong: Majors Suman Gawani (2019) and Radhika Sen (2023) won it earlier.",
   current=ca("2026-05-23"))

# ###################################################################### part: sport (Sports)
U.update({
    "sp_saff_air": ("https://newsonair.gov.in/pm-modi-congratulates-indian-womens-football-team-on-saff-2026-win/", OPENED,
                    "2026-11-06"),
    "sp_kiwg_ol": ("https://www.outlookindia.com/sports/khelo-india-winder-games-2026-army-retain-ice-hockey-gold-haryana-"
                   "champions", OPENED, "2026-11-07"),
    "sp_ws_flash": ("https://www.flashscore.com/news/milwaukee-brewers-win-first-world-series-in-franchise-s-57-year-"
                    "history/GprKB5C4/", SEARCH, "2026-11-07"),
    "sp_ws_n3": ("https://news3lv.com/news/nation-world/brewers-win-the-world-series", SEARCH, "2026-11-07"),
    "sp_uel_rte": ("https://www.rte.ie/sport/soccer/2026/0520/1574268-aston-villa-cruise-to-europa-league-final-triumph/",
                   SEARCH, "2026-11-07"),
    "sp_uel_wam": ("https://www.wam.ae/en/article/178da11-aston-villa-claim-europa-league-crown-with", SEARCH,
                   "2026-11-07"),
    "sp_pga_sky": ("https://www.skysports.com/golf/news/12040/13545201/pga-championship-englands-aaron-rai-storms-to-"
                   "maiden-major-with-three-shot-win-over-jon-rahm-at-aronimink-golf-club", SEARCH, "2026-11-07"),
    "sp_pga_ajc": ("https://www.ajc.com/news/2026/05/aaron-rai-runs-away-with-the-pga-championship-first-english-born-"
                   "winner-in-more-than-a-century/", SEARCH, "2026-11-07"),
    "sp_fac_ajc": ("https://www.ajc.com/news/2026/05/man-city-beats-chelsea-1-0-in-fa-cup-final/", SEARCH, "2026-11-07"),
    "sp_fac_fox": ("https://www.foxsports.com/stories/soccer/man-city-beats-chelsea-fa-cup-final-after-1-100-antoine-"
                   "semenyo-goal", SEARCH, "2026-11-07"),
    "sp_issf_air": ("https://newsonair.gov.in/shooting-indian-troika-clinches-team-gold-in-mens-50m-pistol/", SEARCH,
                    "2026-11-07"),
    "sp_dl_ol": ("https://www.outlookindia.com/sports/others/diamond-league-2026-final-rumesh-pathirage-sri-lanka-javelin-"
                 "throw-brussels", SEARCH, "2026-11-07"),
    "sp_dl_pap": ("https://www.thepapare.com/?p=2629167", SEARCH, "2026-11-07"),
    "sp_cm_fpj": ("https://www.freepressjournal.in/sports/satwiksairaj-rankiredd-chirag-shetty-script-history-in-shenzhen-"
                  "become-first-indians-to-win-china-masters", SEARCH, "2026-11-07"),
    "sp_cm_tt": ("https://telanganatoday.com/satwiksairaj-chirag-shetty-win-china-masters-after-stunning-comeback-in-"
                 "final", SEARCH, "2026-11-07"),
    "sp_cand_fide": ("https://www.fide.com/2026/04/14/", SEARCH, "2026-11-07"),
    "sp_cand_cm": ("https://cyprus-mail.com/2026/04/17/closing-ceremony-of-the-fide-candidates-tournament-2026-at-cap-st-"
                   "georges-hotel-resort", SEARCH, "2026-11-07"),
    "sp_cand_ol": ("https://www.outlookindia.com/sports/others/fide-candidates-2026-javokhir-sindarov-wins-title-sets-up-"
                   "world-championship-clash-vs-d-gukesh", SEARCH, "2026-11-07"),
    "sp_open_gd": ("https://www.golfdigest.com/story/openchampionship2026-ryan-fox-wins-at-royal-birkdale-cameron-young",
                   SEARCH, "2026-11-07"),
    "sp_open_ctv": ("https://www.ctvnews.ca/sports/article/ryan-fox-wins-first-career-major-at-2026-open-championship/",
                    SEARCH, "2026-11-07"),
    "sp_irani_print": ("https://theprint.in/sport/pacers-mukesh-akash-deep-shine-as-rest-of-india-outclass-jk-by-167-"
                       "runs-to-lift-irani-cup/3061522/", OPENED, "2026-11-07"),
    "sp_wr_ol": ("https://www.outlookindia.com/sports/others/kajal-dhochak-neelam-sirohi-double-silver-world-wrestling-"
                 "championships-2026", OPENED, "2026-11-07"),
    "sp_giro_ap": ("https://www.news4jax.com/sports/2026/05/31/jonas-vingegaard-wins-giro-ditalia-to-become-the-eighth-"
                   "male-rider-to-win-all-3-grand-tours/", SEARCH, "2026-11-07"),
    "sp_giro_rou": ("https://rouleur.cc/racing/giro-ditalia-2026-stage-21-results", SEARCH, "2026-11-07"),
    "sp_laver_tm": ("https://www.tennismajors.com/others-news/laver-cup/zverev-secures-laver-cup-for-team-europe-"
                    "reclaiming-trophy-13-5-861938.html", SEARCH, "2026-11-07"),
    "sp_laver_star": ("https://www.thestar.com.my/sport/tennis/2026/09/28/tennis-team-europe-cruise-past-team-world-to-"
                      "win-sixth-laver-cup-title", SEARCH, "2026-11-07"),
    "sp_suhl_fpj": ("https://www.freepressjournal.in/amp/sports/issf-junior-world-championship-2026-india-tops-medal-"
                    "table-with-24-medals-in-suhl", OPENED, "2026-11-07"),
    "sp_nhl_ksl": ("https://www.ksl.com/article/sports/nhl/carolinas-jordan-staal-wins-the-conn-smythe-trophy-as-playoff-"
                   "mvp-oldest-on-record-at-age-37/51511203", SEARCH, "2026-11-07"),
    "sp_nhl_sg": ("https://sundayguardianlive.com/sports/nhl-stanley-cup-2026-final-jordan-staal-wins-conn-smythe-trophy-"
                  "after-leading-carolina-hurricanes-to-championship-207318/", SEARCH, "2026-11-07"),
    "sp_nhl_nhl": ("https://www.nhl.com/news/topic/playoffs/jordan-staal-cements-legendary-status-with-play-in-stanley-"
                   "cup-final", SEARCH, "2026-11-07"),
})
SP = "Sports"
TW, VR = "Tournaments and winners", "Venues and records"

# ------------------------------------------------------------------ Basic (7)
G(SP, TW, "Basic",
  "India's women's football team won the SAFF Championship 2026 at Madgaon, Goa, on 6 June 2026 for a record sixth "
  "title. Which defending champion did India beat 3-1 in the final?",
  ["Bangladesh", "Nepal", "Bhutan", "Sri Lanka"], "*",
  "Football: South Asian championships",
  "India beat defending champions Bangladesh 3-1 in the final of the SAFF Championship 2026 at Madgaon, Goa, on 6 June "
  "2026, winning a record sixth title. The President, Vice-President and Prime Minister congratulated the team.",
  ["Final: 6 June 2026, Madgaon (Goa)", "India 3-1 Bangladesh (defending champions)", "India's record 6th title"],
  [fact("India beat defending champions Bangladesh 3-1 in the SAFF Championship 2026 final at Madgaon, Goa, for a record "
        "sixth title (AIR, 7 June 2026, 'yesterday')", "sp_saff_air")],
  why="The source names Bangladesh as the opponent; the other teams did not play the final.",
  current=ca("2026-06-06"))

G(SP, TW, "Basic",
  "Which state was crowned overall champion of the Ladakh leg of the Khelo India Winter Games 2026, which concluded at "
  "the NDS Stadium in Leh in January 2026?",
  ["Haryana", "Ladakh", "Maharashtra", "Telangana"], "*",
  "Khelo India: winter sports",
  "Haryana finished as overall champion of the Ladakh leg of the Khelo India Winter Games 2026 with four gold medals "
  "from figure skating and ice skating. Hosts Ladakh were second, ahead of Maharashtra and Telangana on silvers, and "
  "the Army retained the men's ice hockey gold by beating Chandigarh 3-2.",
  ["KIWG 2026 (Ladakh leg), NDS Stadium, Leh", "Champion: Haryana (4 golds)", "Runner-up: Ladakh"],
  [fact("KIWG 2026 Ladakh leg at NDS Stadium, Leh: Haryana overall champions with four golds; Ladakh second; Army beat "
        "Chandigarh 3-2 in ice hockey (Outlook, 26 Jan 2026)", "sp_kiwg_ol")],
  why="The source names Haryana as champion; Ladakh was second and Maharashtra and Telangana followed.",
  current=ca("2026-01-26"))

G(SP, TW, "Basic",
  "Which team won its first World Series title on 28 October 2026, beating the Tampa Bay Rays 4-1 in Game 5?",
  ["Milwaukee Brewers", "Seattle Mariners", "San Diego Padres", "Los Angeles Dodgers"], "*",
  "Baseball: World Series",
  "The Milwaukee Brewers won the first World Series title in their franchise history on 28 October 2026, beating the "
  "Tampa Bay Rays 4-1 in Game 5 at Tropicana Field.",
  ["World Series 2026: Brewers beat Rays (Game 5, 4-1)", "Brewers' first title"],
  [fact("Milwaukee Brewers win first World Series in franchise's 57-year history, beating the Tampa Bay Rays 4-1 in Game "
        "5 on 28 October (Flashscore)", "sp_ws_flash"),
   fact("Brewers win the World Series (News 3 LV)", "sp_ws_n3")],
  why="The sources name the Milwaukee Brewers; the other teams did not play the 2026 final.",
  current=ca("2026-10-28"))

G(SP, TW, "Basic",
  "Which club won the UEFA Europa League 2025-26, beating SC Freiburg 3-0 in the final in Istanbul on 20 May 2026?",
  ["Aston Villa", "Nottingham Forest", "Real Betis", "AS Roma"], "*",
  "Football: European club competitions",
  "Aston Villa beat Freiburg 3-0 at the Besiktas Stadium in Istanbul on 20 May 2026, with goals from Youri Tielemans, "
  "Emiliano Buendia and Morgan Rogers. It was Villa's first European trophy since 1982 and first major trophy since "
  "1996, and a record fifth Europa League title for manager Unai Emery.",
  ["Final: Istanbul, 20 May 2026", "Aston Villa 3-0 Freiburg", "Emery's record 5th Europa League"],
  [fact("Aston Villa cruise to Europa League final triumph over Freiburg in Istanbul (RTE, 20 May 2026)", "sp_uel_rte"),
   fact("Aston Villa claim Europa League crown with dominant victory in Istanbul (WAM)", "sp_uel_wam")],
  why="The sources name Aston Villa as winners; the other clubs did not play the final.",
  current=ca("2026-05-20"))

G(SP, TW, "Basic",
  "Who won the PGA Championship 2026 at Aronimink Golf Club, ending on 17 May 2026, his first major title?",
  ["Aaron Rai", "Jon Rahm", "Justin Thomas", "Ludvig Aberg"], "*",
  "Golf: majors",
  "England's Aaron Rai won the 2026 PGA Championship at Aronimink by three strokes at nine under par (271), ahead of "
  "Jon Rahm and Alex Smalley, for his first major. He was described as the first English-born winner of the event in "
  "more than a century.",
  ["PGA Championship 2026: Aronimink", "Winner: Aaron Rai (England), -9", "Runners-up: Rahm, Smalley"],
  [fact("England's Aaron Rai storms to maiden major with three-shot win over Jon Rahm at Aronimink Golf Club (Sky "
        "Sports)", "sp_pga_sky"),
   fact("Aaron Rai runs away with the PGA Championship, first English-born winner in more than a century (AJC/AP, May "
        "2026)", "sp_pga_ajc")],
  why="The sources name Aaron Rai; Rahm was joint runner-up and Thomas and Aberg tied for fourth.",
  current=ca("2026-05-17"))

G(SP, TW, "Basic",
  "Which club won the FA Cup 2025-26, beating Chelsea 1-0 in the final at Wembley on 16 May 2026?",
  ["Manchester City", "Arsenal", "Liverpool", "Newcastle United"], "*",
  "Football: English domestic cups",
  "Manchester City beat Chelsea 1-0 at Wembley on 16 May 2026, Antoine Semenyo scoring the only goal with a back-heel "
  "flick from Erling Haaland's cross.",
  ["FA Cup final: 16 May 2026, Wembley", "Man City 1-0 Chelsea (Semenyo)"],
  [fact("Man City beats Chelsea 1-0 in FA Cup final (AJC/AP, 16 May 2026)", "sp_fac_ajc"),
   fact("Man City beats Chelsea in FA Cup final after audacious Antoine Semenyo goal (Fox Sports)", "sp_fac_fox")],
  why="The sources name Manchester City as the winner; the other clubs did not play the final.",
  current=ca("2026-05-16"))

G(SP, VR, "Basic",
  "In which city did India's men's 50m pistol team of Saurabh Chaudhary, Ravinder Singh and Amanpreet Singh win gold "
  "at the ISSF World Championships on 3 November 2026?",
  ["Doha", "Cairo", "Lima", "Baku"], "*",
  "Shooting: world championships",
  "News On AIR reported on 3 November 2026 that the Indian troika won the men's 50m pistol team gold at the ISSF World "
  "Championships in Doha, Qatar.",
  ["ISSF World Championships 2026: Doha", "Men's 50m pistol team gold: Saurabh, Ravinder, Amanpreet"],
  [fact("Indian troika clinches team gold in men's 50m pistol at the ISSF World Championships in Doha (AIR, 3 Nov 2026)",
        "sp_issf_air")],
  why="The source places the championships in Doha; the other cities are not mentioned.",
  current=ca("2026-11-03"))

# ------------------------------------------------------------------ Intermediate (2)
G(SP, VR, "Intermediate",
  "Rumesh Pathirage won the javelin title at the Diamond League Final 2026 in Brussels with a throw of 89.04 m, "
  "becoming the first athlete from his country to win a Diamond League Final. Which country does he represent?",
  ["Sri Lanka", "Pakistan", "Grenada", "Kenya"], "*",
  "Athletics: Diamond League",
  "Sri Lanka's Rumesh Pathirage won the Diamond League Final javelin at the King Baudouin Stadium, Brussels, on 5 "
  "September 2026 with 89.04 m, his fifth Diamond League win of the season, and became the first Sri Lankan to win a "
  "Diamond League Final.",
  ["Diamond League Final 2026: Brussels", "Javelin: Rumesh Pathirage (Sri Lanka), 89.04 m"],
  [fact("Rumesh Pathirage clinches Diamond League Final title at Brussels with 89.04m javelin throw (Outlook)",
        "sp_dl_ol"),
   fact("Rumesh Tharanga etches history as first Sri Lankan to clinch Diamond League Final (ThePapare)", "sp_dl_pap")],
  why="The sources identify Pathirage as Sri Lankan; the other countries are wrong.",
  current=ca("2026-09-05"))

G(SP, TW, "Intermediate",
  "In September 2026 Satwiksairaj Rankireddy and Chirag Shetty became the first Indians to win which BWF Super 750 "
  "tournament, held in Shenzhen?",
  ["China Masters", "China Open", "Japan Open", "Denmark Open"], "*",
  "Badminton: BWF World Tour",
  "On 6 September 2026 in Shenzhen, Satwik and Chirag beat China's He Ji Ting and Ren Xiang Yu 11-21, 21-13, 21-17 to "
  "win the China Masters Super 750, their 10th BWF World Tour title. They became the first Indians to win the "
  "tournament since it began in 2005; they had been runners-up in 2023 and 2025.",
  ["China Masters (Shenzhen), 6 Sep 2026", "First Indian winners", "Pair's 10th World Tour title"],
  [fact("Satwiksairaj Rankireddy and Chirag Shetty script history in Shenzhen, become first Indians to win China Masters "
        "(Free Press Journal)", "sp_cm_fpj"),
   fact("Satwik-Chirag win China Masters after stunning comeback in final (Telangana Today, 6 Sep 2026)", "sp_cm_tt")],
  why="The sources name the China Masters in Shenzhen; the other tournaments are not involved.",
  current=ca("2026-09-06"))

# ------------------------------------------------------------------ Advanced (8)
GS(SP, TW, "Advanced", "the FIDE Candidates Tournament 2026 (open section)",
   ["It was held in Toronto, Canada.",
    "Javokhir Sindarov of Uzbekistan clinched first place with a round to spare.",
    "The winner earned the right to challenge world champion D. Gukesh."],
   [False, True, True],
   "Chess: world championship cycle",
   "The 2026 Candidates was held from 28 March to 16 April 2026 at the Cap St Georges Hotel and Resort in Cyprus, the "
   "first time Cyprus hosted it, so statement 1 is wrong. Uzbekistan's Javokhir Sindarov clinched first place in round "
   "13 with a round to spare, earning a world title match against D. Gukesh. R. Vaishali won the parallel Women's "
   "Candidates.",
   [fact("Sindarov storms to Candidates victory; will challenge Gukesh (FIDE, 14 April 2026)", "sp_cand_fide"),
    fact("Closing ceremony of the FIDE Candidates Tournament 2026 at Cap St Georges Hotel and Resort, Cyprus (Cyprus "
         "Mail, 17 April 2026)", "sp_cand_cm"),
    fact("FIDE Candidates 2026: Javokhir Sindarov wins title, sets up world championship clash with D Gukesh (Outlook)",
         "sp_cand_ol")],
   why="Statement 1 is wrong: the tournament was held in Cyprus.",
   current=ca("2026-04-14"))

GS(SP, VR, "Advanced", "the 154th Open Championship (golf), won by Ryan Fox in July 2026",
   ["It was played at Royal Birkdale.",
    "It was Fox's second major title.",
    "Fox became the second New Zealander to win the Open, after Bob Charles in 1963."],
   [True, False, True],
   "Golf: majors",
   "Ryan Fox won the 154th Open at Royal Birkdale on 19 July 2026 at 10 under par, a birdie on the 72nd hole giving him "
   "a one-stroke win over Cameron Young. It was his first major, so statement 2 is wrong. He became the second New "
   "Zealander to win the Open, the first since Bob Charles in 1963.",
   [fact("Ryan Fox wins at Royal Birkdale, beating Cameron Young (Golf Digest)", "sp_open_gd"),
    fact("Ryan Fox wins first career major at 2026 Open Championship; second New Zealander to win, after Bob Charles "
         "(1963) (CTV/AP)", "sp_open_ctv")],
   why="Statement 2 is wrong: the 2026 Open was Fox's first major title.",
   current=ca("2026-07-19"))

GS(SP, TW, "Advanced", "the Irani Cup match of October 2026",
   ["Rest of India beat Jammu and Kashmir by 167 runs in Srinagar.",
    "Jammu and Kashmir were bowled out for 111 in their second innings.",
    "Mukesh Kumar's bowling figures in that innings were 6/33."],
   [True, True, True],
   "Cricket: Indian domestic",
   "Rest of India beat Ranji Trophy champions Jammu and Kashmir by 167 runs in Srinagar on 4 October 2026. J&K were "
   "bowled out for 111 in 28.4 overs in their second innings, with Mukesh Kumar taking 6/33 and Akash Deep 3/25. All "
   "three statements are correct.",
   [fact("Rest of India beat J&K by 167 runs in Srinagar (4 Oct 2026); J&K 111 all out in 28.4 overs; Mukesh Kumar 6/33, "
         "Akash Deep 3/25 (ThePrint/PTI)", "sp_irani_print")],
   why="All three statements match the match report.",
   current=ca("2026-10-04"))

GS(SP, TW, "Advanced", "India's women wrestlers at the 2026 Senior World Wrestling Championships",
   ["Kajal Dhochak won the 76kg gold, beating Ukraine's Anastasiya Alpyeyeva in the final.",
    "Neelam Sirohi won silver at 50kg after losing the final to Japan's Yui Susaki.",
    "It was the first time two Indian women reached finals at the same senior World Championships."],
   [False, True, True],
   "Wrestling: world championships",
   "Kajal Dhochak won silver at 76kg, losing 6-8 to Ukraine's Anastasiya Alpyeyeva in the final, so statement 1 is "
   "wrong; she became the first Indian heavyweight wrestler to win a senior World Championships medal. Neelam Sirohi "
   "won silver at 50kg after losing to Japan's Yui Susaki. It was the first time two Indian women reached finals at the "
   "same senior Worlds.",
   [fact("Kajal Dhochak (76kg) lost 6-8 to Ukraine's Anastasiya Alpyeyeva in the final; Neelam Sirohi (50kg) lost to "
         "Japan's Yui Susaki; first time two Indian women reached finals at the same senior Worlds; Kajal first Indian "
         "heavyweight to win a medal (Outlook, 28 Oct 2026)", "sp_wr_ol")],
   why="Statement 1 is wrong: Kajal Dhochak won silver, losing the final to Alpyeyeva.",
   current=ca("2026-10-28"))

GS(SP, TW, "Advanced", "the Giro d'Italia 2026",
   ["Jonas Vingegaard won it, the race finishing in Rome on 31 May 2026.",
    "With it Vingegaard became the eighth male rider to win all three Grand Tours.",
    "Felix Gall finished second overall and Jai Hindley third."],
   [True, True, True],
   "Cycling: Grand Tours",
   "Jonas Vingegaard of Visma-Lease a Bike won the Giro d'Italia 2026, which ended in Rome on 31 May, finishing 5 min "
   "22 s ahead of Felix Gall with Jai Hindley third. He won five stages and became the eighth male rider to win all "
   "three Grand Tours; Jonathan Milan won the final stage. All three statements are correct.",
   [fact("Jonas Vingegaard wins Giro d'Italia to become the eighth male rider to win all 3 Grand Tours (AP, 31 May 2026)",
         "sp_giro_ap"),
    fact("Giro d'Italia 2026 stage 21 in Rome; final GC: Vingegaard, Gall, Hindley (Rouleur)", "sp_giro_rou")],
   why="All three statements match the reports.",
   current=ca("2026-05-31"))

GS(SP, VR, "Advanced", "the Laver Cup 2026",
   ["It was held in San Francisco.",
    "Team Europe won 13-5, with Alexander Zverev clinching the decisive point.",
    "It was Team Europe's sixth Laver Cup title."],
   [False, True, True],
   "Tennis: team events",
   "Team Europe beat Team World 13-5 at The O2 in London; Alexander Zverev clinched it on 27 September 2026 by beating "
   "Learner Tien. It was Europe's sixth title, regaining the trophy Team World had won in San Francisco in 2025, so "
   "statement 1 is wrong.",
   [fact("Zverev secures Laver Cup for Team Europe, reclaiming trophy 13-5 (Tennis Majors)", "sp_laver_tm"),
    fact("Team Europe cruise past Team World to win sixth Laver Cup title (Reuters via The Star, 28 Sep 2026)",
         "sp_laver_star")],
   why="Statement 1 is wrong: the 2026 Laver Cup was held in London.",
   current=ca("2026-09-27"))

GS(SP, VR, "Advanced", "India at the ISSF Junior World Championship 2026",
   ["It was held in Suhl, Germany.",
    "India won 24 medals, 12 of them gold.",
    "Sameer won the gold in the men's junior 25m rapid fire pistol."],
   [True, False, True],
   "Shooting: junior world championships",
   "At the ISSF Junior World Championship 2026 in Suhl, Germany, India topped the medal table with 24 medals: 7 gold, "
   "8 silver and 9 bronze, so statement 2 is wrong. Gold medallists included Sejal Kamble (10m air pistol), Sameer (25m "
   "rapid fire pistol), Rohit Kanyan, Pritam Kendre and Abhinav Deshwal.",
   [fact("ISSF Junior World Championship 2026 in Suhl: India tops medal table with 24 medals (7 gold, 8 silver, 9 "
         "bronze); Sameer gold in 25m rapid fire pistol men junior (Free Press Journal, 26 June 2026)", "sp_suhl_fpj")],
   why="Statement 2 is wrong: India won 7 gold medals, not 12.",
   current=ca("2026-06-26"))

GS(SP, TW, "Advanced", "the 2026 Stanley Cup Final (ice hockey)",
   ["The Carolina Hurricanes beat the Vegas Golden Knights in six games.",
    "Hurricanes captain Jordan Staal, aged 37, became the oldest winner of the Conn Smythe Trophy.",
    "It was the Hurricanes' first Stanley Cup."],
   [True, True, False],
   "Ice hockey: NHL",
   "The Carolina Hurricanes beat the Vegas Golden Knights 3-0 in Game 6 on 14 June 2026 to win the Final in six games. "
   "It was their second Stanley Cup, so statement 3 is wrong. Captain Jordan Staal won the Conn Smythe Trophy as playoff "
   "MVP, the oldest on record at 37.",
   [fact("Carolina's Jordan Staal wins the Conn Smythe Trophy as playoff MVP, oldest on record at age 37 (AP via KSL, "
         "June 2026)", "sp_nhl_ksl"),
    fact("Jordan Staal won the Conn Smythe after leading the Hurricanes to their second Stanley Cup championship by "
         "defeating the Vegas Golden Knights in six games (Sunday Guardian)", "sp_nhl_sg"),
    fact("Jordan Staal cements legendary status with play in Stanley Cup Final (NHL.com)", "sp_nhl_nhl")],
   why="Statement 3 is wrong: it was Carolina's second Stanley Cup.",
   current=ca("2026-06-14"))

# ###################################################################### part: eco (Economic Affairs)
U.update({
    "ec_boj_aj": ("https://www.aljazeera.com/economy/2026/6/16/japans-central-bank-raises-interest-rates-to-highest-level-"
                  "since-1995", SEARCH, "2026-11-07"),
    "ec_boj_air": ("https://newsonair.gov.in/bank-of-japan-raises-interest-rate-to-1-amid-weak-yen-and-higher-prices/",
                   SEARCH, "2026-11-07"),
    "ec_rba_ind": ("https://www.indailysa.com.au/news/just-in/2026/06/16/rba-keeps-interest-rates-on-hold-for-first-time-"
                   "this-year", SEARCH, "2026-11-07"),
    "ec_rba_cba": ("https://www.commbank.com.au/articles/newsroom/2026/06/reserve-bank-june-2026-rates-decision.html",
                   SEARCH, "2026-11-07"),
    "ec_pmi_print": ("https://theprint.in/economy/indias-manufacturing-sector-growth-hits-7-month-high-in-sep-on-strong-"
                     "demand/3058775/", SEARCH, "2026-11-07"),
    "ec_pmi_kt": ("https://www.khaleejtimes.com/business/indias-factory-growth-climbs-to-7-month-high-on-surging-demand-"
                  "pmi-shows", SEARCH, "2026-11-07"),
    "ec_gstjun_tr": ("https://www.tribuneindia.com/news/business/indias-gross-gst-collections-surge-13-9-yoy-to-rs-1-94-"
                     "lakh-crore-in-june-2026/", SEARCH, "2026-11-07"),
    "ec_gstjun_rw": ("https://www.republicworld.com/business/india-s-gross-gst-collections-surge-139-yoy-to-rs-194-lakh-"
                     "crore-in-june-2026-07-01-130769", SEARCH, "2026-11-07"),
    "ec_boc_adv": ("https://www.advisor.ca/economy/policy/bank-of-canada-delivers-1st-hike-in-three-years/", SEARCH,
                   "2026-11-07"),
    "ec_boc_boe": ("https://boereport.com/2026/10/28/text-of-the-bank-of-canadas-latest-policy-interest-rate-decision/",
                   SEARCH, "2026-11-07"),
    "ec_gstc_air": ("https://newsonair.gov.in/gst-council-meeting-arresting-powers-of-tax-officers-scrapped-prosecution-"
                    "threshold-raised-to-rs-5-crore/", OPENED, "2026-11-07"),
    "ec_gstc_air2": ("https://newsonair.gov.in/57th-gst-council-meeting-to-be-held-in-new-delhi-today/", SEARCH,
                     "2026-11-07"),
    "ec_wb_pr": ("https://www.worldbank.org/en/news/press-release/2026/04/09/india-remains-among-the-fastest-growing-"
                 "economies", SEARCH, "2026-11-07"),
    "ec_wb_week": ("https://www.theweek.in/news/biz-tech/2026/04/09/india-economic-growth-outlook-world-bank.html", SEARCH,
                   "2026-11-07"),
    "ec_oecd_ians": ("https://ianslive.in/oecd-predicts-india-to-register-63-pc-growth-in-fy27-64-pc-in-fy28-amid-global-"
                     "shocks--20260603141840", SEARCH, "2026-11-07"),
    "ec_oecd_bt": ("https://www.businesstoday.in/world/story/oecd-cuts-global-growth-forecast-to-2-8-for-2026-as-energy-"
                   "shock-threatens-recovery-535232-2026-06-05", SEARCH, "2026-11-07"),
    "ec_fed_eu": ("https://euronews.com/business/2026/07/29/us-federal-reserve-holds-interest-rates-steady-as-three-"
                  "policymakers-back-hike", SEARCH, "2026-11-07"),
    "ec_fed_inv": ("https://www.investing.com/news/economic-indicators/instant-view-fed-holds-rates-steady-as-three-"
                   "policymakers-dissent-for-a-hike-4821495", SEARCH, "2026-11-07"),
    "ec_boe_aj": ("https://www.ajbell.co.uk/news/articles/bank-england-votes-6-3-leave-bank-rate-unchanged-375", SEARCH,
                  "2026-11-07"),
    "ec_boe_fr": ("https://www.financialreporter.co.uk/bank-of-england-holds-interest-rates-at-375-in-6-3-vote.html",
                  SEARCH, "2026-11-07"),
    "ec_wpi_print": ("https://theprint.in/economy/wholesale-price-inflation-rises-3-88-pc-in-march-on-surge-in-crude-"
                     "rates/2905361/", SEARCH, "2026-11-07"),
    "ec_wpi_tr": ("https://www.tribuneindia.com/news/business/indias-wholesale-inflation-rises-to-3-88-in-march-as-energy-"
                  "and-manufacturing-costs-climb/", OPENED, "2026-11-07"),
    "ec_wpi_fpj": ("https://www.freepressjournal.in/business/wpi-inflation-rises-to-388-in-march-up-from-213-in-february-"
                   "govt-data-shows-steady-price-pressure", SEARCH, "2026-11-07"),
    "ec_iip_print": ("https://theprint.in/economy/industrial-production-rises-by-7-3-pc-in-june-govt-data/2999016/", SEARCH,
                     "2026-11-07"),
    "ec_iip_icra": ("https://www.icra.in/Research/ViewResearchReport/iip-growth-spiked-to-23-month-high-7-3-in-june-2026-"
                    "volumes-healthy-in-q1-fy2027-although-surge-in-input-costs-will-hurt-gva-growth/7041", SEARCH,
                    "2026-11-07"),
    "ec_ecb_ecb": ("https://ecb.europa.eu/press/pr/date/2026/html/ecb.mp261029~9a493adf17.en.html", SEARCH, "2026-11-07"),
    "ec_ecb_cm": ("https://cyprus-mail.com/2026/10/29/ecb-holds-interest-rates-steady-as-energy-shock-threatens-inflation-"
                  "and-growth", SEARCH, "2026-11-07"),
    "ec_gstaug_print": ("https://theprint.in/india/gross-gst-mop-up-rises-15-pc-to-about-rs-2-lakh-cr-in-aug-on-higher-"
                        "domestic-transactions-imports/3030711/", SEARCH, "2026-11-07"),
    "ec_gstaug_bt": ("https://www.businesstoday.in/latest/economy/story/gst-mop-up-rises-14-8-to-nearly-rs2-lakh-crore-in-"
                     "august-refunds-climb-68-552515-2026-09-01", SEARCH, "2026-11-07"),
    "ec_core_dd": ("https://ddnews.gov.in/en/core-sector-output-grows-4-8-in-august-2026/", SEARCH, "2026-11-07"),
    "ec_core_pe": ("https://www.policyedge.in/p/core-industries-grow-48-in-august-led-by-electricity-and-cement", SEARCH,
                   "2026-11-07"),
    "ec_ndt_dd": ("https://www.devdiscourse.com/article/business/3992785-net-direct-tax-collections-rise-1321-to-rs-1338-"
                  "lakh-crore-so-far-in-fy27", SEARCH, "2026-11-07"),
    "ec_ndt_sc": ("https://studycafe.in/income-tax-dept-releases-data-for-direct-tax-collection-for-fy-2026-27-as-of-"
                  "october-14-2026-427446.html", SEARCH, "2026-11-07"),
    "ec_un_india": ("https://india.un.org/en/node/315971", SEARCH, "2026-11-07"),
    "ec_un_air": ("https://newsonair.gov.in/un-projects-indias-growth-rate-at-6-4-this-year-despite-global-crisis/",
                  SEARCH, "2026-11-07"),
    "ec_un_ups": ("https://upstox.com/news/business-news/latest-updates/un-trims-india-s-2026-gdp-forecast-to-6-4-says-"
                  "better-placed-than-neighbours-to-weather-oil-shock/article-194027/", SEARCH, "2026-11-07"),
})
EC = "Economic Affairs"
GDPS, INF, FIS, MON = ("GDP and growth projections", "Inflation data", "Fiscal data", "Monetary policy decisions")

# ------------------------------------------------------------------ Basic (5)
G(EC, MON, "Basic",
  "On 16 June 2026 the Bank of Japan raised its policy interest rate to its highest level since 1995. To what level?",
  ["1%", "0.75%", "1.25%", "0.5%"], "*",
  "Global central banks: Japan",
  "On 16 June 2026 the Bank of Japan voted 7-1 to raise its short-term policy rate by 25 basis points to 1%, the "
  "highest since 1995 and its first increase since December, citing a weak yen and higher prices.",
  ["BoJ, 16 June 2026: 0.75% -> 1%", "Highest since 1995; vote 7-1"],
  [fact("Japan's central bank raises interest rates to highest level since 1995 (1%) (Al Jazeera, 16 June 2026)",
        "ec_boj_aj"),
   fact("Bank of Japan raises interest rate to 1% amid weak yen and higher prices (AIR)", "ec_boj_air")],
  why="The sources give 1%; 0.75% was the earlier rate and the other values were not set.",
  current=ca("2026-06-16"))

G(EC, MON, "Basic",
  "On 16 June 2026 the Reserve Bank of Australia kept its cash rate unchanged for the first time in 2026, after three "
  "straight rises. At what level did it hold the rate?",
  ["4.35%", "3.85%", "4.10%", "3.60%"], "*",
  "Global central banks: Australia",
  "The Reserve Bank of Australia, led by Governor Michele Bullock, held the cash rate at 4.35% on 16 June 2026, its "
  "first hold of the year after three consecutive 25-basis-point rises that began in February 2026 (to 3.85%).",
  ["RBA hold, 16 June 2026: 4.35%", "After three hikes in 2026 (first to 3.85% in February)"],
  [fact("RBA keeps interest rates on hold for first time this year (InDaily, 16 June 2026)", "ec_rba_ind"),
   fact("Reserve Bank of Australia holds rates (4.35%) after three straight rises (CommBank, June 2026)", "ec_rba_cba")],
  why="3.85% was the level after the February hike; the other values were not the June level.",
  current=ca("2026-06-16"))

G(EC, GDPS, "Basic",
  "The final HSBC India Manufacturing PMI for September 2026, compiled by S&P Global, showed the strongest improvement "
  "in seven months. What was the reading?",
  ["55.1", "52.8", "58.4", "49.6"], "*",
  "Economic indicators: PMI",
  "The HSBC India Manufacturing PMI rose to 55.1 in September 2026 from 52.8 in August, a seven-month high, as new "
  "orders grew at the fastest pace since February. (A reading above 50 indicates expansion.)",
  ["Sep 2026 manufacturing PMI: 55.1 (Aug: 52.8)", "Seven-month high"],
  [fact("India's manufacturing sector growth hits 7-month high in September (PMI 55.1) on strong demand (ThePrint/PTI)",
        "ec_pmi_print"),
   fact("India's factory growth climbs to 7-month high on surging demand, PMI shows (Khaleej Times/Reuters)",
        "ec_pmi_kt")],
  why="52.8 was August's reading; the other values are not reported.",
  current=ca("2026-10-01"))

G(EC, FIS, "Basic",
  "According to data released on 1 July 2026, India's gross GST collections for June 2026 grew by about 13.9% year on "
  "year to roughly how much?",
  ["Rs 1.95 lakh crore", "Rs 2.43 lakh crore", "Rs 1.62 lakh crore", "Rs 1.35 lakh crore"], "*",
  "Tax collections: GST",
  "Gross GST collections for June 2026 were Rs 1,94,812 crore (about Rs 1.95 lakh crore), up 13.9%. Import GST rose "
  "34.6% to Rs 60,038 crore while domestic collections grew 6.5% to about Rs 1.35 lakh crore; net collections after "
  "refunds were about Rs 1.62 lakh crore. April 2026's record was about Rs 2.43 lakh crore.",
  ["June 2026 gross GST: about Rs 1.95 lakh crore (+13.9%)", "Imports +34.6%; domestic +6.5%"],
  [fact("India's gross GST collections surge 13.9% YoY to Rs 1.94 lakh crore (Rs 1,94,812 crore) in June 2026 (Tribune)",
        "ec_gstjun_tr"),
   fact("India's gross GST collections surge 13.9% YoY in June 2026 (Republic, 1 July 2026)", "ec_gstjun_rw")],
  why="Rs 1.62 lakh crore was the net figure, Rs 1.35 lakh crore the domestic part and Rs 2.43 lakh crore April's record.",
  current=ca("2026-07-01"))

G(EC, MON, "Basic",
  "On 28 October 2026 the Bank of Canada raised its policy rate by 25 basis points, its first increase in more than "
  "three years. What is the new policy rate?",
  ["2.5%", "2.25%", "2.75%", "3%"], "*",
  "Global central banks: Canada",
  "The Bank of Canada raised its policy rate by a quarter point to 2.5% from 2.25% on 28 October 2026, the first hike "
  "in more than three years, with the Bank Rate at 2.75% and the deposit rate at 2.45%.",
  ["BoC, 28 Oct 2026: 2.25% -> 2.5%", "First hike in 3+ years"],
  [fact("Bank of Canada delivers first hike in three years (Advisor.ca, Oct 2026)", "ec_boc_adv"),
   fact("Text of the Bank of Canada's policy interest rate decision of 28 October 2026: policy rate raised to 2.5%",
        "ec_boc_boe")],
  why="2.25% was the old rate and 2.75% is the Bank Rate, not the policy rate.",
  current=ca("2026-10-28"))

# ------------------------------------------------------------------ Intermediate (5)
G(EC, FIS, "Intermediate",
  "At the GST Council meeting chaired in New Delhi on 8 October 2026, tax officers' powers of arrest were removed. To "
  "what amount was the monetary threshold for prosecution under GST raised?",
  ["Rs 5 crore", "Rs 2 crore", "Rs 10 crore", "Rs 50 lakh"], "*",
  "GST: compliance reforms",
  "Finance Minister Nirmala Sitharaman said after the GST Council meeting of 8 October 2026 that tax officers would no "
  "longer have powers of arrest and that the prosecution threshold was raised from Rs 1 crore to Rs 5 crore. No "
  "notices would be issued for amounts of Rs 10,000 or less, and the rate structure was described as settled.",
  ["Arrest powers of GST officers scrapped", "Prosecution threshold: Rs 1 crore -> Rs 5 crore",
   "No notices for Rs 10,000 or less"],
  [fact("GST Council meeting (8 Oct 2026): arresting powers of tax officers scrapped; prosecution threshold raised from "
        "Rs 1 crore to Rs 5 crore (AIR)", "ec_gstc_air"),
   fact("FM Nirmala Sitharaman chairs 57th GST Council meeting in New Delhi (AIR, 8 Oct 2026)", "ec_gstc_air2")],
  why="The source gives Rs 5 crore (up from Rs 1 crore); the other amounts are not mentioned.",
  current=ca("2026-10-08"))

G(EC, GDPS, "Intermediate",
  "In its India Development Update of 9 April 2026, what real GDP growth did the World Bank project for India for "
  "FY27, citing higher energy prices from the Middle East conflict?",
  ["6.6%", "7.2%", "6.3%", "7.6%"], "*",
  "Growth projections: World Bank",
  "The World Bank's India Development Update of 9 April 2026 projected India's growth at 6.6% in FY27, as higher energy "
  "prices from the Middle East conflict and supply-chain disruptions weighed on activity. It projected South Asia's "
  "growth at 6.3% in 2026.",
  ["World Bank IDU (9 Apr 2026): India FY27 6.6%", "South Asia 2026: 6.3%"],
  [fact("World Bank press release, 9 April 2026: growth in India projected at 6.6% in FY27; South Asia 6.3% in 2026",
        "ec_wb_pr"),
   fact("India still fastest-growing economy, but set for a steep GDP fall this year (The Week, 9 Apr 2026)",
        "ec_wb_week")],
  why="The World Bank gave 6.6% for FY27; 6.3% was its South Asia figure and the others are not its FY27 projection.",
  current=ca("2026-04-09"))

G(EC, GDPS, "Intermediate",
  "In its Economic Outlook of June 2026, what real GDP growth did the OECD project for India for FY2026-27?",
  ["6.3%", "7.6%", "6.1%", "2.8%"], "*",
  "Growth projections: OECD",
  "The OECD's Economic Outlook released on 3 June 2026 projected India's growth at 6.3% in FY2026-27 and 6.4% in "
  "FY2027-28, after 7.6% in FY2025-26, citing the energy shock. It cut its global growth forecast for 2026 to 2.8%.",
  ["OECD (3 June 2026): India 6.3% (FY27), 6.4% (FY28)", "FY26: 7.6%; global 2026: 2.8%"],
  [fact("OECD predicts India to register 6.3% growth in FY27, 6.4% in FY28 amid global shocks (IANS, 3 June 2026)",
        "ec_oecd_ians"),
   fact("OECD cuts global growth forecast to 2.8% for 2026 as energy shock threatens recovery (Business Today)",
        "ec_oecd_bt")],
  why="7.6% was FY26, 6.1% the earlier March projection and 2.8% the global forecast.",
  current=ca("2026-06-03"))

G(EC, MON, "Intermediate",
  "At its meeting ending on 29 July 2026, the US Federal Open Market Committee kept the federal funds rate at "
  "3.50-3.75%. What was notable about the vote?",
  ["Three members dissented in favour of a rate hike", "Three members dissented in favour of a rate cut",
   "It was a unanimous vote to cut rates by 25 basis points", "The Chair cast the only dissenting vote"], "*",
  "Global central banks: US Federal Reserve",
  "The FOMC voted 9-3 on 29 July 2026 to hold the federal funds rate at 3.50-3.75%; Beth Hammack, Neel Kashkari and "
  "Lorie Logan dissented, preferring a quarter-point increase.",
  ["Fed, 29 July 2026: hold at 3.50-3.75%", "Vote 9-3; three dissents for a hike"],
  [fact("US Federal Reserve holds interest rates steady as three policymakers back hike (Euronews, 29 July 2026)",
        "ec_fed_eu"),
   fact("Fed holds rates steady as three policymakers dissent for a hike (Investing.com/Reuters)", "ec_fed_inv")],
  why="The three dissents favoured a hike; rates were not cut.",
  current=ca("2026-07-29"))

G(EC, MON, "Intermediate",
  "At its decision of 30 July 2026, the Bank of England's Monetary Policy Committee held Bank Rate at 3.75% by a 6-3 "
  "vote. What did the three dissenting members want?",
  ["An immediate rise to 4%", "A cut to 3.5%", "A cut to 3.25%", "A pause in quantitative tightening only"], "*",
  "Global central banks: UK",
  "On 30 July 2026 the Bank of England's MPC voted 6-3 to keep Bank Rate at 3.75%, with three of the nine members "
  "voting for an immediate rise to 4%.",
  ["BoE, 30 July 2026: Bank Rate held at 3.75% (6-3)", "Three votes for a rise to 4%"],
  [fact("Bank of England votes 6-3 to leave bank rate unchanged at 3.75%; three wanted a rise (AJ Bell)", "ec_boe_aj"),
   fact("Bank of England holds interest rates at 3.75% in 6-3 vote (Financial Reporter)", "ec_boe_fr")],
  why="The dissenters wanted a rise to 4%, not a cut.",
  current=ca("2026-07-30"))

# ------------------------------------------------------------------ Advanced (7)
GS(EC, INF, "Advanced", "India's wholesale price (WPI) inflation for March 2026, released on 15 April 2026",
   ["Headline WPI inflation rose to 3.88% from 2.13% in February 2026, the highest in more than three years.",
    "Fuel and power moved from deflation in February to positive inflation of 1.05% in March.",
    "The food articles index rose sharply over February, making food the main driver of the increase."],
   [True, True, False],
   "Inflation: wholesale prices",
   "WPI inflation rose to 3.88% in March 2026 from 2.13% in February, the highest in over three years. Fuel and power "
   "turned from a deflation of 3.78% in February to 1.05% in March on higher petrol and diesel prices, the main "
   "driver. Food articles prices actually fell 0.85% month-on-month, so statement 3 is wrong.",
   [fact("WPI inflation rises to 3.88% in March on surge in crude rates (ThePrint/PTI, 15 Apr 2026)", "ec_wpi_print"),
    fact("WPI inflation 3.88% in March 2026 (ANI, 15 April 2026); food articles prices fell 0.85% month-on-month; fuel "
         "and power index rose 4.13% m-o-m on mineral oils (Tribune)", "ec_wpi_tr"),
    fact("WPI inflation rises to 3.88% in March, up from 2.13% in February; fuel and power at 1.05% in March from a "
         "deflation of 3.78% in February (Free Press Journal / search results)", "ec_wpi_fpj")],
   why="Statement 3 is wrong: food articles prices fell month-on-month; fuel and power drove the rise.",
   current=ca("2026-04-15"))

GS(EC, GDPS, "Advanced", "India's Index of Industrial Production (IIP) for June 2026, released on 28 July 2026",
   ["Industrial output grew 7.3%, the slowest pace in two years.",
    "Electricity was the fastest-growing sector, at 10.6%.",
    "Manufacturing grew 7.8%, while mining grew only about 1%."],
   [False, True, True],
   "Industrial output",
   "IIP grew 7.3% in June 2026, a 23-month high (not a two-year low), so statement 1 is wrong. Electricity grew 10.6%, "
   "manufacturing 7.8% and mining 1%, the last snapping a four-month contraction.",
   [fact("Industrial production rises by 7.3% in June: govt data; electricity 10.6%, manufacturing 7.8%, mining 1% "
         "(ThePrint/PTI, 28 July 2026)", "ec_iip_print"),
    fact("ICRA: IIP growth spiked to 23-month high of 7.3% in June 2026", "ec_iip_icra")],
   why="Statement 1 is wrong: 7.3% was a 23-month high.",
   current=ca("2026-07-28"))

GS(EC, MON, "Advanced", "the European Central Bank's monetary policy decision of 29 October 2026",
   ["The deposit facility rate was kept unchanged at 2.50%.",
    "The rate on the main refinancing operations was raised to 2.90%.",
    "The marginal lending facility rate stands at 2.90%."],
   [True, False, True],
   "Global central banks: euro area",
   "On 29 October 2026 the ECB left its three key rates unchanged: deposit facility 2.50%, main refinancing operations "
   "2.65% and marginal lending facility 2.90%. So statement 2 is wrong (2.90% is the marginal lending rate, and it was "
   "unchanged).",
   [fact("ECB press release, 29 Oct 2026: deposit facility, MRO and marginal lending rates unchanged at 2.50%, 2.65% and "
         "2.90%", "ec_ecb_ecb"),
    fact("ECB holds interest rates steady as energy shock threatens inflation and growth (Cyprus Mail, 29 Oct 2026)",
         "ec_ecb_cm")],
   why="Statement 2 is wrong: the MRO rate stayed at 2.65%; 2.90% is the unchanged marginal lending rate.",
   current=ca("2026-10-29"))

GS(EC, FIS, "Advanced", "India's GST collections for August 2026, released on 1 September 2026",
   ["Gross collections were about Rs 1.99 lakh crore, up 14.8% year on year.",
    "Gross GST revenue from imports grew faster (about 29%) than domestic gross revenue (about 9.3%).",
    "Refunds rose sharply, so net GST revenue grew more slowly (about 8.3%) than gross revenue."],
   [True, True, True],
   "Tax collections: GST",
   "Gross GST revenue in August 2026 was Rs 1,99,853 crore, up 14.8%. Import GST rose 29% to Rs 62,604 crore and "
   "domestic gross revenue 9.3% to Rs 1,37,249 crore. Refunds jumped about 68% to Rs 31,795 crore, so net revenue rose "
   "8.3% to Rs 1,68,057 crore. All three statements are correct.",
   [fact("Gross GST mop-up rises about 15% to about Rs 2 lakh crore in August on higher domestic transactions, imports "
         "(ThePrint/PTI, 1 Sep 2026)", "ec_gstaug_print"),
    fact("GST mop-up rises 14.8% to nearly Rs 2 lakh crore in August; refunds climb 68%; net revenue up 8.3% (Business "
         "Today, 1 Sep 2026)", "ec_gstaug_bt")],
   why="All three statements match the reported data.",
   current=ca("2026-09-01"))

GS(EC, GDPS, "Advanced", "the Index of Core Industries for August 2026",
   ["Core sector output grew 4.8% in August 2026.",
    "Growth for July 2026 was revised to 5.0%.",
    "Cumulative growth in April-August 2026 was lower than in April-August 2025."],
   [True, True, False],
   "Industrial output: core sector",
   "Core industries grew 4.8% year on year in August 2026, easing from a revised 5.0% in July, with cement, electricity, "
   "iron ore, steel and refinery products growing. Cumulative growth in April-August 2026 was 4.3%, higher than 2.4% a "
   "year earlier, so statement 3 is wrong.",
   [fact("Core sector output grows 4.8% in August 2026 (DD News)", "ec_core_dd"),
    fact("Core industries grow 4.8% in August, easing from revised 5.0% in July; April-August 4.3% vs 2.4% a year ago "
         "(Policy Edge)", "ec_core_pe")],
   why="Statement 3 is wrong: April-August growth was 4.3%, up from 2.4% a year earlier.",
   current=ca("2026-09-22", inferred="sources date the release to 21 or 22 September 2026"))

GS(EC, FIS, "Advanced", "India's net direct tax collections for 2026-27 up to 14 October 2026",
   ["Net collections were about Rs 13.38 lakh crore, up about 13.2% year on year.",
    "Refunds fell compared with the same period of the previous year.",
    "Gross collections grew faster, by about 14.9%, to about Rs 16.03 lakh crore."],
   [True, False, True],
   "Tax collections: direct taxes",
   "Income Tax Department data as on 14 October 2026 showed net direct tax collections of Rs 13,37,866.98 crore, up "
   "13.21%, and gross collections of about Rs 16.03 lakh crore, up 14.89%. Refunds rose about 24%, so statement 2 is "
   "wrong; that is why net collections grew more slowly than gross.",
   [fact("Net direct tax collections rise 13.21% to Rs 13.38 lakh crore so far in FY27 (Devdiscourse/PTI)", "ec_ndt_dd"),
    fact("Direct tax collection FY 2026-27 as of 14 Oct 2026: gross Rs 16.03 lakh crore (+14.89%); refunds +24.22% "
         "(StudyCafe, citing Income Tax Department)", "ec_ndt_sc")],
   why="Statement 2 is wrong: refunds rose about 24%.",
   current=ca("2026-10-15"))

GS(EC, GDPS, "Advanced", "the UN's World Economic Situation and Prospects mid-2026 update, released on 19 May 2026",
   ["It raised India's 2026 growth forecast from its January estimate.",
    "It projected India's growth in 2026 at 6.4%.",
    "It cut the global growth forecast for 2026 to 2.5% from 2.7%."],
   [False, True, True],
   "Growth projections: United Nations",
   "The UN's mid-2026 WESP update projected India's growth at 6.4% in 2026, down 0.2 percentage point from 6.6% in "
   "January, so statement 1 is wrong. India remained the fastest-growing major economy. The UN cut its global 2026 "
   "growth forecast to 2.5% from 2.7%, citing energy-market disruption from the Middle East conflict.",
   [fact("UN India: India's 2026 growth projected at 6.4%, 0.2 percentage point below the January forecast "
         "(india.un.org)", "ec_un_india"),
    fact("UN projects India's growth rate at 6.4% this year despite global crisis (AIR, 20 May 2026)", "ec_un_air"),
    fact("UN trims India's 2026 GDP forecast to 6.4%; global 2026 growth cut to 2.5% from 2.7% (Upstox)", "ec_un_ups")],
   why="Statement 1 is wrong: India's forecast was cut from 6.6% to 6.4%.",
   current=ca("2026-05-19"))

# ###################################################################### part: rep (Reports and Indexes)
U.update({
    "rp_ember": ("https://ember-energy.org/latest-insights/global-electricity-review-2026/", SEARCH, "2026-11-07"),
    "rp_ember_csr": ("https://thecsrjournal.in/india-emerges-as-key-driver-of-global-clean-energy-growth-says-ember-report/",
                     SEARCH, "2026-11-07"),
    "rp_lpr_wwf": ("https://www.worldwildlife.org/news/press-releases/wildlife-population-sizes-decline-73-on-average-but-"
                   "tiger-elephant-turtle-and-tuna-recoveries-offer-hope/", SEARCH, "2026-11-07"),
    "rp_lpr_pub": ("https://www.worldwildlife.org/publications/2026-living-planet-report/", SEARCH, "2026-11-07"),
    "rp_ss_print": ("https://theprint.in/india/swachh-survekshan-2024-25-indore-named-cleanest-city-for-8th-time-surat-"
                    "ranks-2nd/2693099", SEARCH, "2026-11-07"),
    "rp_ss_gs": ("https://english.gujaratsamachar.com/news/gujarat/swachh-survekshan-2024-25-ahmedabad-awarded-cleanest-big-"
                 "city-of-india", SEARCH, "2026-11-07"),
    "rp_grfc_dte": ("https://www.downtoearth.org.in/food/more-than-266-million-people-face-acute-food-insecurity-conflict-"
                    "main-driver", SEARCH, "2026-11-07"),
    "rp_grfc_wfp": ("https://wfpusa.org/news/new-report-signals-hunger-malnutrition-remain-alarmingly-high/", SEARCH,
                    "2026-11-07"),
    "rp_gser_yr": ("https://yourstory.com/2026/06/bengaluru-ranks-second-in-asia-for-ai-innovation", SEARCH, "2026-11-07"),
    "rp_gser_sg": ("https://startupgenome.com/insights/gser-2026-ecosystem-leaders-must-prioritize-startup-policy-or-risk-"
                   "being-left-behind", SEARCH, "2026-11-07"),
    "rp_ijr_is": ("https://www.indiaspend.com/governance/southern-states-best-in-justice-delivery-vacancies-persist-"
                  "nationwide-949345", SEARCH, "2026-11-07"),
    "rp_ijr_ol": ("https://www.outlookindia.com/national/up-bihar-maharashtra-make-up-42-of-undertrials-southern-states-best-"
                  "in-justice-delivery-details-from-india-justice-report-2025", SEARCH, "2026-11-07"),
    "rp_aser_print": ("https://theprint.in/india/education/govt-schools-in-rural-india-outperform-private-in-bouncing-back-"
                      "from-covid-19-learning-loss/2467287", SEARCH, "2026-11-07"),
    "rp_aser_ol": ("https://www.outlookindia.com/national/aser-report-2024-rural-india-shows-recovery-from-post-pandemic-"
                   "educational-losses", SEARCH, "2026-11-07"),
    "rp_wmr_who": ("https://www.who.int/teams/global-Malaria-programme/reports/world-Malaria-report-2025", SEARCH,
                   "2026-11-07"),
    "rp_wmr_week": ("https://www.theweek.in/news/health/2025/12/09/malaria-claimed-over-6-lakh-lives-in-2024-drug-"
                    "resistance-threatens-progress-who-report-explained.html", SEARCH, "2026-11-07"),
    "rp_fm_imf": ("https://www.imf.org/en/Publications/FM/Issues/2026/04/15/fiscal-monitor-april-2026", SEARCH,
                  "2026-11-07"),
    "rp_fm_aa": ("https://aa.com.tr/en/economy/imf-sees-global-public-debt-at-100-of-gdp-by-2029-level-last-seen-after-"
                 "world-war-ii/3906879", SEARCH, "2026-11-07"),
    "rp_wdr_wb": ("https://www.worldbank.org/en/news/press-release/2026/08/04/ai-offers-lifeline-to-developing-economies-in-"
                  "an-era-of-weak-growth", SEARCH, "2026-11-07"),
    "rp_wdr_pub": ("https://www.worldbank.org/en/publication/wdr2026", SEARCH, "2026-11-07"),
    "rp_nfhs_air": ("https://newsonair.gov.in/nfhs-6-fact-sheets-mark-significant-milestone-in-indias-evolving-health-and-"
                    "statistical-ecosystem/", OPENED, "2026-11-06"),
    "rp_nfhs_md": ("https://medicaldialogues.in/amp/news/health/india-sees-progress-in-maternal-and-child-health-"
                   "immunisation-and-nutrition-nfhs-6-finds-171705", SEARCH, "2026-11-07"),
    "rp_nfhs_pari": ("https://ruralindiaonline.org/en/library/resource/national-family-health-survey-nfhs-6-2023-24-fact-"
                     "sheets/", SEARCH, "2026-11-07"),
    "rp_wdrg_un": ("https://news.un.org/en/story/2026/06/1167817", SEARCH, "2026-11-07"),
    "rp_wdrg_unodc": ("https://www.unodc.org/unodc/frontpage/2026/june/wdr26-findings.html", SEARCH, "2026-11-07"),
})
RPT = "Important Reports and Indexes"
PB, IR = "Publishing body", "India's rank"

G(RPT, PB, "Basic",
  "The Living Planet Report 2026, released in October 2026, found an average 73% decline in monitored wildlife "
  "populations since 1970. It is published by WWF together with which institution?",
  ["Zoological Society of London", "International Union for Conservation of Nature",
   "UN Environment Programme", "Wildlife Conservation Society"], "*",
  "Environment reports",
  "WWF and the Zoological Society of London (ZSL) published the Living Planet Report 2026 on 7 October 2026. Its Living "
  "Planet Index showed an average 73% decline in monitored populations of vertebrates between 1970 and 2022, the "
  "steepest in freshwater populations (85%).",
  ["Living Planet Report: WWF + ZSL", "2026: average 73% decline since 1970"],
  [fact("WWF: wildlife population sizes decline 73% on average (Living Planet Report 2026, WWF and ZSL)", "rp_lpr_wwf"),
   fact("WWF publication page: 2026 Living Planet Report", "rp_lpr_pub")],
  why="The report is produced by WWF and ZSL; the other bodies are not its publishers.",
  current=ca("2026-10-07"))

G(RPT, IR, "Basic",
  "In Swachh Survekshan 2024-25, presented by President Droupadi Murmu on 17 July 2025, which city was named the "
  "cleanest big city (population over 10 lakh)?",
  ["Ahmedabad", "Bhopal", "Lucknow", "Pune"], "*",
  "Urban cleanliness rankings",
  "In Swachh Survekshan 2024-25, Indore, Surat and Navi Mumbai were placed in a new 'Super Swachh League'. Among cities "
  "with more than 10 lakh people, Ahmedabad was named the cleanest big city, followed by Bhopal and Lucknow.",
  ["Super Swachh League: Indore, Surat, Navi Mumbai", "Cleanest big city (10 lakh+): Ahmedabad"],
  [fact("Swachh Survekshan 2024-25: Indore named cleanest city for 8th time; Super Swachh League (ThePrint, 17 July "
        "2025)", "rp_ss_print"),
   fact("Swachh Survekshan 2024-25: Ahmedabad awarded 'Cleanest Big City' of India; Bhopal and Lucknow follow (Gujarat "
        "Samachar)", "rp_ss_gs")],
  why="Bhopal and Lucknow followed Ahmedabad; Pune was not named.",
  current=ca("2025-07-17"))

G(RPT, PB, "Intermediate",
  "The Global Report on Food Crises 2026, which found that 266 million people in 47 countries faced acute food "
  "insecurity in 2025, is published by FAO, WFP and which network?",
  ["Global Network Against Food Crises", "Global Alliance for Improved Nutrition", "Scaling Up Nutrition Movement",
   "Committee on World Food Security"], "*",
  "Food security reports",
  "The 2026 Global Report on Food Crises, released on 24 April 2026 by FAO, WFP and the Global Network Against Food "
  "Crises, found 266 million people in 47 countries/territories in acute food insecurity in 2025, with conflict the "
  "main driver.",
  ["GRFC 2026: FAO, WFP, Global Network Against Food Crises", "266 million people, 47 countries (2025)"],
  [fact("More than 266 million people face acute food insecurity, conflict main driver: Global Report on Food Crises 2026 "
        "(Down To Earth)", "rp_grfc_dte"),
   fact("UN, EU and partners warn in new report (GRFC 2026) that acute food insecurity remains alarmingly high (WFP USA)",
        "rp_grfc_wfp")],
  why="The GRFC is a product of the Global Network Against Food Crises with FAO and WFP; the others are not publishers.",
  current=ca("2026-04-24"))

G(RPT, IR, "Intermediate",
  "In the Global Startup Ecosystem Report (GSER) 2026 of Startup Genome, released in June 2026, what was Bengaluru's "
  "global rank among startup ecosystems?",
  ["15th", "5th", "31st", "40th"], "*",
  "Startup ecosystem rankings",
  "GSER 2026, released by Startup Genome with the Global Entrepreneurship Network at VivaTech in Paris in June 2026, "
  "ranked Bengaluru the 15th global startup ecosystem, with an ecosystem value of about USD 152.8 billion, and second "
  "in Asia among AI-native clusters after Beijing.",
  ["GSER 2026 (Startup Genome + GEN)", "Bengaluru: #15 globally, ~USD 152.8 bn"],
  [fact("Bengaluru ranked #15 global startup ecosystem in GSER 2026; ecosystem value USD 152.8 billion; #2 in Asia for "
        "AI (YourStory, June 2026)", "rp_gser_yr"),
   fact("GSER 2026 (Startup Genome)", "rp_gser_sg")],
  why="The report places Bengaluru 15th; the other ranks are not Bengaluru's.",
  current=ca("2026-06-17"))

G(RPT, IR, "Intermediate",
  "In the India Justice Report 2025, which ranks states on police, judiciary, prisons and legal aid, which state was "
  "ranked first among large and mid-sized states?",
  ["Karnataka", "Andhra Pradesh", "Telangana", "Kerala"], "*",
  "Governance indices",
  "The fourth India Justice Report (2025) ranked Karnataka first among large and mid-sized states, "
  "followed by Andhra Pradesh and Telangana, with West Bengal last; Sikkim topped the small states.",
  ["IJR 2025: Karnataka 1st (large/mid states)", "Then Andhra Pradesh, Telangana; West Bengal last"],
  [fact("India Justice Report 2025: southern states best in justice delivery; Karnataka first (IndiaSpend)", "rp_ijr_is"),
   fact("India Justice Report 2025: southern states best in justice delivery (Outlook)", "rp_ijr_ol")],
  why="Andhra Pradesh and Telangana were second and third; Kerala did not top the list.",
  current=ca("2025-04-15", inferred="IJR 2025 reported in April 2025; exact release day not given in the sources"))

G(RPT, PB, "Intermediate",
  "The Annual Status of Education Report (ASER) 2024, released in January 2025, found the highest Class 3 reading levels "
  "in government schools since the survey began. Which organisation facilitates the ASER survey?",
  ["Pratham", "NCERT", "NITI Aayog", "UNICEF India"], "*",
  "Education reports",
  "ASER is a rural household survey facilitated by Pratham. ASER 2024 (released 28 January 2025) found the share of "
  "Class 3 government-school children able to read a Class 2 text rose from 16.3% in 2022 to 23.4% in 2024.",
  ["ASER: Pratham (rural household survey)", "ASER 2024: Std III govt reading 23.4%"],
  [fact("ASER 2024: government schools in rural India outperform private in bouncing back from Covid learning loss "
        "(ThePrint, Jan 2025)", "rp_aser_print"),
   fact("ASER Report 2024 (Pratham): rural India shows recovery from post-pandemic educational losses (Outlook)",
        "rp_aser_ol")],
  why="ASER is facilitated by Pratham, not by NCERT, NITI Aayog or UNICEF.",
  current=ca("2025-01-28"))

G(RPT, IR, "Intermediate",
  "According to WHO's World Malaria Report 2025, released in December 2025, about what share of the estimated malaria "
  "cases in the WHO South-East Asia Region in 2024 were in India?",
  ["About 73%", "About 25%", "About 94%", "About 50%"], "*",
  "Health reports",
  "WHO's World Malaria Report 2025 (4 December 2025) estimated 282 million cases and 610,000 deaths worldwide in 2024, "
  "with the African Region accounting for 94% of cases. India accounted for about 73.3% of estimated cases and nearly "
  "89% of malaria deaths in the South-East Asia Region.",
  ["WMR 2025: 282 million cases, 610,000 deaths (2024)", "India: ~73.3% of SEAR cases, ~89% of SEAR deaths"],
  [fact("WHO World Malaria Report 2025", "rp_wmr_who"),
   fact("Malaria claimed over 6 lakh lives in 2024; India accounted for 73.3% of estimated cases in the South-East Asia "
        "Region (The Week, 9 Dec 2025)", "rp_wmr_week")],
  why="94% is the African Region's share of global cases; the other shares are not given for India.",
  current=ca("2025-12-04"))

G(RPT, PB, "Intermediate",
  "The April 2026 edition of the 'Fiscal Monitor', which projected global public debt to reach 100% of GDP by 2029, "
  "is a twice-yearly report of which institution?",
  ["International Monetary Fund", "World Bank", "Bank for International Settlements", "OECD"], "*",
  "Global economic reports",
  "The IMF's Fiscal Monitor of 15 April 2026, 'Fiscal Policy under Pressure: High Debt, Rising Risks', projected global "
  "public debt to reach 100% of GDP by 2029 and urged countries to avoid broad-based energy subsidies.",
  ["Fiscal Monitor: IMF (twice a year)", "April 2026: global public debt to 100% of GDP by 2029"],
  [fact("IMF Fiscal Monitor, April 2026 (15 April 2026)", "rp_fm_imf"),
   fact("IMF sees global public debt at 100% of GDP by 2029 (Anadolu Agency)", "rp_fm_aa")],
  why="The Fiscal Monitor is an IMF publication.",
  current=ca("2026-04-15"))

G(RPT, PB, "Intermediate",
  "The World Bank's World Development Report 2026, released on 4 August 2026, is devoted to which theme?",
  ["The promise of artificial intelligence", "Climate adaptation and resilience", "Jobs and the middle-income trap",
   "Data for better lives"], "*",
  "Global development reports",
  "The World Bank released the World Development Report 2026, 'The Promise of Artificial Intelligence', on 4 August "
  "2026, examining how developing economies can use AI.",
  ["WDR 2026: The Promise of Artificial Intelligence (4 Aug 2026)"],
  [fact("World Bank press release, 4 Aug 2026: AI offers lifeline to developing economies in an era of weak growth (WDR "
        "2026)", "rp_wdr_wb"),
   fact("World Development Report 2026 page (World Bank)", "rp_wdr_pub")],
  why="WDR 2026 is on AI; the other themes are not its subject.",
  current=ca("2026-08-04"))

GS(RPT, PB, "Advanced", "the NFHS-6 (2023-24) India fact sheets released in May 2026",
   ["India's total fertility rate was 2.0 children per woman.",
    "Stunting among children under five rose to 35.5% from 29.3% in NFHS-5.",
    "The first-phase fact sheets cover 101 indicators, with a fuller national report to follow."],
   [True, False, True],
   "Health surveys",
   "The NFHS-6 (2023-24) fact sheets, covering 101 indicators, showed India's TFR at 2.0 and under-5 stunting down to "
   "29.3% from 35.5% (it fell, so statement 2 is wrong). The fact sheets are the first phase of dissemination; a "
   "fuller National Report with more indicators is to follow.",
   [fact("NFHS-6 finds progress in maternal and child health: TFR 2.0; stunting 35.5% -> 29.3% (Medical Dialogues)",
         "rp_nfhs_md"),
    fact("National Family Health Survey (NFHS-6), 2023-24 Fact Sheets (PARI library)", "rp_nfhs_pari"),
    fact("NFHS-6 fact sheets cover 101 indicators; first phase, fuller National Report to follow (AIR, 7 June 2026)",
         "rp_nfhs_air")],
   why="Statement 2 is wrong: stunting fell from 35.5% to 29.3%.",
   current=ca("2026-05-29"))

GS(RPT, PB, "Advanced", "UNODC's World Drug Report 2026, released on 26 June 2026",
   ["An estimated 331 million people used drugs in 2024.",
    "This was about 6.2% of the world's population aged 15-64.",
    "Opioids were the most widely used drug worldwide."],
   [True, True, False],
   "Global drug reports",
   "The World Drug Report 2026 estimated that 331 million people used drugs in 2024, about 6.2% of people aged 15-64, up "
   "from 5.2% a decade earlier. Cannabis remained the most widely used drug (about 256 million users), followed by "
   "opioids (63 million), so statement 3 is wrong.",
   [fact("UNODC World Drug Report 2026 findings: 331 million people used drugs in 2024; 6.2% of 15-64 population; "
         "cannabis most used", "rp_wdrg_unodc"),
    fact("Global drug use reaches record high (UN News, June 2026)", "rp_wdrg_un")],
   why="Statement 3 is wrong: cannabis, not opioids, is the most widely used drug.",
   current=ca("2026-06-26"))

G(RPT, IR, "Intermediate",
  "According to Ember's Global Electricity Review 2026, released on 21 April 2026, how much solar capacity did India "
  "deploy in 2025, a record?",
  ["About 37.9 GW", "About 6.3 GW", "About 98 GW", "About 125 GW"], "*",
  "Energy reports",
  "Ember's Global Electricity Review 2026 said India deployed a record 37.9 GW(AC) of solar and 6.3 GW of wind in 2025; "
  "with strong hydro output and slower demand growth, India's fossil generation fell by 52 TWh (-3.3%).",
  ["Ember GER 2026: India solar 37.9 GW(AC) in 2025 (record)", "Wind 6.3 GW; fossil generation -52 TWh"],
  [fact("Ember Global Electricity Review 2026: India deployed a record 37.9 GW(AC) of solar and 6.3 GW of wind in 2025; "
        "fossil generation fell 52 TWh (-3.3%)", "rp_ember"),
   fact("India emerges as key driver of global clean energy growth, says Ember report (CSR Journal)", "rp_ember_csr")],
  why="6.3 GW was the wind addition; the other figures are not the solar addition.",
  current=ca("2026-04-21"))

# ###################################################################### part: book (Books and Authors)
U.update({
    "bk_hugo_br": ("https://bookriot.com/2026-hugo-awards-winners/", SEARCH, "2026-11-07"),
    "bk_hugo_sa": ("https://shelf-awareness.com/theshelf/2026-09-01/awards:_hugo_winners.html", SEARCH, "2026-11-07"),
    "bk_nba_npr": ("https://www.npr.org/2025/11/20/nx-s1-5607997/here-are-the-winners-of-the-2025-national-book-awards",
                   SEARCH, "2026-11-07"),
    "bk_nba_prh": ("https://global.penguinrandomhouse.com/announcements/our-76th-national-book-awards-winner-omar-el-"
                   "akkads-one-day-everyone-will-have-always-been-against-this/", SEARCH, "2026-11-07"),
    "bk_orw_fdn": ("https://www.orwellfoundation.com/the-orwell-foundation/news-events/news-events/news/orwell-prize-"
                   "winners-announced-at-ceremony-at-university-college-london/", SEARCH, "2026-11-07"),
    "bk_orw_bp": ("https://www.booksandpublishing.com.au/articles/2026/06/29/333414/karen-bartlett-ben-lerner-win-2026-"
                  "orwell-prizes/", SEARCH, "2026-11-07"),
    "bk_tiw_air": ("https://newsonair.gov.in/education-tool-for-empowerment-says-vp-radhakrishnan-at-book-release/", OPENED,
                   "2026-11-07"),
    "bk_mf_bp": ("https://www.booksandpublishing.com.au/articles/2026/08/05/336214/omar-musa-wins-2026-miles-franklin-"
                 "literary-award-for-fierceland/", SEARCH, "2026-11-07"),
    "bk_mf_perp": ("https://www.perpetual.com.au/insights/omar-musa-wins-miles-franklin-literary-award/", SEARCH,
                   "2026-11-07"),
    "bk_gan_air": ("https://www.newsonair.gov.in/vp-radhakrishnan-inaugurates-mahadev-desai-library-extension-releases-"
                   "book-on-gandhis-vision-age-of-enlightenment/", OPENED, "2026-11-07"),
    "bk_rss_vp": ("https://vicepresidentofindia.nic.in/gallery/vice-president-shri-c-p-radhakrishnan-released-the-book-rss-"
                  "100-a-century-of-service-unity-sacrifice-authored-by-shri-shyam-jaju-and-shri-anupam-trivedi-at-"
                  "uprashtrapati-bhavan/", SEARCH, "2026-11-07"),
    "bk_rss_air": ("https://newsonair.gov.in/journey-of-rss-testifies-enduring-value-of-service-before-self-says-vp-"
                   "radhakrishnan/", SEARCH, "2026-11-07"),
    "bk_rss_pb": ("https://www.prabhatbooks.com/rss-100-a-century-of-service-unity-sacrifice.htm", SEARCH, "2026-11-07"),
    "bk_ws_site": ("https://www.walterscottprize.co.uk/alice-jolly-wins-2026-walter-scott-prize/", SEARCH, "2026-11-07"),
    "bk_ws_stv": ("https://news.stv.tv/scotland/historical-fiction-prize-announces-first-all-british-shortlist", SEARCH,
                  "2026-11-07"),
    "bk_kir_br": ("https://www.bookreporter.com/features/awards/the-2026-kirkus-prize", SEARCH, "2026-11-07"),
    "bk_kir_ny1": ("https://ny1.com/nyc/all-boroughs/ap-top-news/2026/10/08/tayari-jones-novel-kin-wins-the-kirkus-prize-"
                   "for-fiction-earning-a-50000-award", SEARCH, "2026-11-07"),
})
BK, RB = "Books and Authors", "Recent books"

G(BK, RB, "Basic",
  "'The Everlasting', which won the Hugo Award for Best Novel in 2026 at the 84th World Science Fiction Convention in "
  "Anaheim, was written by whom?",
  ["Alix E. Harrow", "Robert Jackson Bennett", "Nnedi Okorafor", "Adrian Tchaikovsky"], "*",
  "Literary prizes: science fiction and fantasy",
  "The 2026 Hugo Awards were announced on 30 August 2026 at LAcon V, the 84th Worldcon, in Anaheim, California. Alix E. "
  "Harrow won Best Novel for 'The Everlasting'; finalists included Robert Jackson Bennett, Nnedi Okorafor and Adrian "
  "Tchaikovsky.",
  ["Hugo Best Novel 2026: Alix E. Harrow, 'The Everlasting'", "LAcon V (84th Worldcon), Anaheim, 30 Aug 2026"],
  [fact("Here are the winners of the 2026 Hugo Awards: Best Novel, The Everlasting by Alix E. Harrow (Book Riot)",
        "bk_hugo_br"),
   fact("Awards: Hugo winners announced at LAcon V (Shelf Awareness, 1 Sep 2026)", "bk_hugo_sa")],
  why="Bennett, Okorafor and Tchaikovsky were finalists, not the winner.",
  current=ca("2026-08-30"))

U.update({
    "bk_tam_print": ("https://theprint.in/india/vice-president-releases-book-a-century-of-service-the-rss-in-100-acts-of-"
                     "seva/3043702/", SEARCH, "2026-11-07"),
    "bk_tam_air": ("https://newsonair.gov.in/hi/vice-president-c-p-radhakrishnan-released-the-book-of-former-telangana-"
                   "governor-dr-tamilisai/", SEARCH, "2026-11-07"),
})

G(BK, RB, "Basic",
  "'A Century of Service: The RSS in 100 Acts of Seva', released by Vice-President C. P. Radhakrishnan in New Delhi in "
  "September 2026, was written by which former Governor of Telangana?",
  ["Tamilisai Soundararajan", "C. P. Radhakrishnan", "Jishnu Dev Varma", "E. S. L. Narasimhan"], "*",
  "Books released by dignitaries",
  "Vice-President C. P. Radhakrishnan released 'A Century of Service: The RSS in 100 Acts of Seva', written by former "
  "Telangana Governor Tamilisai Soundararajan, in New Delhi in mid-September 2026; the book recounts 100 acts of seva "
  "(service) over the RSS's century.",
  ["Book: A Century of Service: The RSS in 100 Acts of Seva", "Author: Tamilisai Soundararajan"],
  [fact("Vice-President releases book 'A Century of Service: The RSS in 100 Acts of Seva' by Tamilisai Soundararajan "
        "(ThePrint/PTI, 16 Sep 2026, 'on Tuesday')", "bk_tam_print"),
   fact("Vice-President released the book of former Telangana Governor Dr Tamilisai (AIR Hindi, 16 Sep 2026)",
        "bk_tam_air")],
  why="The sources name Tamilisai Soundararajan; the others did not write this book.",
  current=ca("2026-09-15", inferred="PTI report of 16 Sep 2026 says the release was 'on Tuesday'"))

G(BK, RB, "Basic",
  "'Sankalp Se Siddhi ka Modi Yug', a book released by Vice-President C. P. Radhakrishnan in August 2026, was written "
  "by which Rajya Sabha MP?",
  ["Ghanshyam Tiwari", "Sudhanshu Trivedi", "Ram Chander Jangra", "Rajeev Shukla"], "*",
  "Books released by dignitaries",
  "News On AIR reported on 27 August 2026 that the Vice-President released 'Sankalp Se Siddhi ka Modi Yug', written by "
  "Rajya Sabha MP Ghanshyam Tiwari, describing education as a tool for empowerment.",
  ["Book: Sankalp Se Siddhi ka Modi Yug", "Author: Ghanshyam Tiwari (Rajya Sabha MP)"],
  [fact("VP Radhakrishnan releases 'Sankalp Se Siddhi ka Modi Yug' by Rajya Sabha MP Ghanshyam Tiwari (AIR, 27 Aug "
        "2026)", "bk_tiw_air")],
  why="The source names Ghanshyam Tiwari; the other MPs are not mentioned.",
  current=ca("2026-08-27"))

G(BK, RB, "Basic",
  "Omar Musa won Australia's Miles Franklin Literary Award 2026 for which novel, about siblings who return to Malaysian "
  "Borneo after their father's death?",
  ["Fierceland", "Here Come the Dogs", "Benbecula", "Seascraper"], "*",
  "Literary prizes: Australia",
  "Omar Musa won the 2026 Miles Franklin Literary Award, announced in Sydney on 5 August 2026, for his second novel "
  "'Fierceland'; his debut 'Here Come the Dogs' was longlisted in 2015.",
  ["Miles Franklin 2026: Omar Musa, 'Fierceland'", "Debut: 'Here Come the Dogs' (longlisted 2015)"],
  [fact("Omar Musa wins 2026 Miles Franklin Literary Award for 'Fierceland' (Books+Publishing, 5 Aug 2026)",
        "bk_mf_bp"),
   fact("Perpetual: Omar Musa wins Miles Franklin Literary Award", "bk_mf_perp")],
  why="'Here Come the Dogs' is his debut; 'Benbecula' and 'Seascraper' are by other authors.",
  current=ca("2026-08-05"))

G(BK, RB, "Basic",
  "On 20 January 2026, Vice-President C. P. Radhakrishnan inaugurated the Mahadev Desai Library extension and released "
  "the book 'Age of Enlightenment: Mahatma Gandhi's Vision' at which institution in New Delhi?",
  ["Harijan Sevak Sangh (Gandhi Ashram)", "Gandhi Smriti", "National Gandhi Museum, Rajghat",
   "Gandhi Peace Foundation"], "*",
  "Books released by dignitaries",
  "On 20 January 2026 the Vice-President inaugurated the Mahadev Desai Library extension and released 'Age of "
  "Enlightenment: Mahatma Gandhi's Vision' at the Harijan Sevak Sangh, Gandhi Ashram, New Delhi, where he also visited "
  "the Kasturba Museum.",
  ["Book: Age of Enlightenment: Mahatma Gandhi's Vision", "Venue: Harijan Sevak Sangh, Gandhi Ashram, New Delhi"],
  [fact("VP inaugurates Mahadev Desai Library extension and releases 'Age of Enlightenment: Mahatma Gandhi's Vision' at "
        "Harijan Sevak Sangh, Gandhi Ashram, New Delhi (AIR, 20 Jan 2026)", "bk_gan_air")],
  why="The source names the Harijan Sevak Sangh; the other institutions are not mentioned.",
  current=ca("2026-01-20"))

GS(BK, RB, "Advanced", "the book 'RSS @100: A Century of Service, Unity & Sacrifice'",
   ["It was written by Shyam Jaju and Anupam Trivedi.",
    "Vice-President C. P. Radhakrishnan released it at Uprashtrapati Bhavan on 17 July 2026.",
    "It is published by Penguin Random House India."],
   [True, True, False],
   "Books released by dignitaries",
   "Vice-President C. P. Radhakrishnan released 'RSS @100: A Century of Service, Unity & Sacrifice', written by Shyam "
   "Jaju and Anupam Trivedi, at Uprashtrapati Bhavan on 17 July 2026; it includes a chapter 'A Swayamsevak as PM: The "
   "Modi Era'. It is published by Prabhat Prakashan, so statement 3 is wrong.",
   [fact("Vice-President released 'RSS @ 100: A Century of Service, Unity & Sacrifice', authored by Shyam Jaju and Anupam "
         "Trivedi, at Uprashtrapati Bhavan on 17.07.2026 (Vice-President's Secretariat)", "bk_rss_vp"),
    fact("Journey of RSS testifies enduring value of service before self, says VP (AIR, 17 July 2026)", "bk_rss_air"),
    fact("Prabhat Prakashan listing: RSS @100: A Century of Service, Unity & Sacrifice", "bk_rss_pb")],
   why="Statement 3 is wrong: the book is published by Prabhat Prakashan.",
   current=ca("2026-07-17"))

GS(BK, RB, "Advanced", "the Orwell Prize for Political Writing 2026",
   ["It was won by Sam Dalrymple's 'Shattered Lands'.",
    "The winners were announced at a ceremony at University College London on 26 June 2026.",
    "The judging panel was chaired by Rohan Silva."],
   [False, True, True],
   "Literary prizes: UK",
   "The 2026 Orwell Prize for Political Writing went to Karen Bartlett's 'The Escape from Kabul', an account of the 2021 "
   "evacuation from Kabul; Sam Dalrymple's 'Shattered Lands' was a finalist, so statement 1 is wrong. The winners were "
   "announced at University College London on 26 June 2026, and the panel was chaired by Rohan Silva.",
   [fact("Orwell Prize winners announced at ceremony at University College London; Political Writing: Karen Bartlett, "
         "'The Escape from Kabul'; judges chaired by Rohan Silva (Orwell Foundation, June 2026)", "bk_orw_fdn"),
    fact("Karen Bartlett, Ben Lerner win 2026 Orwell Prizes (Books+Publishing)", "bk_orw_bp")],
   why="Statement 1 is wrong: Karen Bartlett's 'The Escape from Kabul' won; 'Shattered Lands' was a finalist.",
   current=ca("2026-06-26"))

GS(BK, RB, "Advanced", "the Walter Scott Prize for Historical Fiction 2026",
   ["It was won by Alice Jolly for 'The Matchbox Girl'.",
    "The winning novel is set in Victorian London.",
    "Its shortlist was the first in the prize's history made up entirely of British authors."],
   [True, False, True],
   "Literary prizes: historical fiction",
   "Alice Jolly won the 2026 Walter Scott Prize (GBP 25,000) for 'The Matchbox Girl', set in 1930s Vienna and following a "
   "patient of Dr Hans Asperger, so statement 2 is wrong. The 2026 shortlist was the prize's first all-British "
   "shortlist.",
   [fact("Alice Jolly wins 2026 Walter Scott Prize for 'The Matchbox Girl', set in 1930s Vienna (Walter Scott Prize)",
         "bk_ws_site"),
    fact("Historical fiction prize announces first all-British shortlist (STV News)", "bk_ws_stv")],
   why="Statement 2 is wrong: the novel is set in 1930s Vienna.",
   current=ca("2026-06-12"))

GS(BK, RB, "Advanced", "the Kirkus Prize 2026, announced on 7 October 2026",
   ["The fiction prize went to Tayari Jones for 'Kin'.",
    "The nonfiction prize went to Pamela Colloff for 'Catch the Devil'.",
    "Each category winner receives USD 50,000."],
   [True, True, True],
   "Literary prizes: US",
   "At the Kirkus Prize ceremony in New York on 7 October 2026, Tayari Jones won the fiction prize for 'Kin' and Pamela "
   "Colloff the nonfiction prize for 'Catch the Devil'; Elizabeth Acevedo won for young readers' literature. Each "
   "winner receives USD 50,000. All three statements are correct.",
   [fact("The 2026 Kirkus Prize: fiction Tayari Jones, 'Kin'; nonfiction Pamela Colloff, 'Catch the Devil' (Bookreporter)",
         "bk_kir_br"),
    fact("Tayari Jones' novel 'Kin' wins the Kirkus Prize for fiction, earning a $50,000 award (AP via NY1, 8 Oct 2026)",
         "bk_kir_ny1")],
   why="All three statements are correct.",
   current=ca("2026-10-07"))

# ###################################################################### part: biz (Business and Corporate News)
U.update({
    "bz_goog_air": ("https://newsonair.gov.in/tourism-ministry-signs-mou-with-google-india-to-boost-digital-promotion-of-"
                    "tourism-destinations/", OPENED, "2026-11-07"),
    "bz_inox_fpj": ("https://www.freepressjournal.in/business/inox-clean-energy-completes-6000-crore-acquisition-of-gips-"
                    "vena-energy-india-from-blackrock", SEARCH, "2026-11-07"),
    "bz_inox_en": ("https://www.energetica-india.net/news/inox-clean-energy-completes-inr-6000-crore-acquisition-of-vena-"
                   "energy-india-platform", SEARCH, "2026-11-07"),
    "bz_tmill_dr": ("https://dealroom.co/news/146235-tata-steel-completes-tm-international-logistics-stake-acquisition/",
                    SEARCH, "2026-11-07"),
    "bz_tmill_iw": ("https://www.investywise.com/?p=109734", SEARCH, "2026-11-07"),
    "bz_yap_pt": ("https://www.pharmaceutical-tech.com/news/piramal-pharma-completes-acquisition-of-controlling", SEARCH,
                  "2026-11-07"),
    "bz_yap_mc": ("https://manufacturingchemist.com/piramal-pharma-completes-acquisition-of-controlling-stake-in", SEARCH,
                  "2026-11-07"),
    "bz_hz_ipp": ("https://www.indianpharmapost.com/news/hearzap-completes-acquisition-of-amplifon-indias-hearing-"
                  "healthcare-business-21423", SEARCH, "2026-11-07"),
    "bz_wa_mer": ("https://mercomindia.com/waaree-buys-stake-in-smart-meter-company-eppeltone-for-₹218-million", SEARCH,
                  "2026-11-07"),
    "bz_fn_adu": ("https://www.aviation-defence-universe.com/kalyani-strategic-systems-partners-with-fn-herstal-to-build-"
                  "small-arms-and-counter-uas-capability-in-india/", SEARCH, "2026-11-07"),
    "bz_ng_sw": ("https://swarajyamag.com/defence/frances-naval-group-nibe-sign-mou-to-strengthen-indias-naval-"
                 "shipbuilding-and-maritime-technology-capabilities", SEARCH, "2026-11-07"),
    "bz_ng_ra": ("https://raksha-anirveda.com/naval-group-and-nibe-limited-with-its-group-companies-sign-strategic-mou-for-"
                 "high-tech-solution-and-expertise-for-indian-shipbuilding/", SEARCH, "2026-11-07"),
    "bz_tem_adu": ("https://www.aviation-defence-universe.com/tembo-global-industries-signs-mou-with-belgiums-lachaussee-"
                   "sa-to-establish-advanced-ammunition-production-line-in-india/", SEARCH, "2026-11-07"),
})
BZ = "Business and Corporate News"
MA, CP = "Mergers and acquisitions", "Corporate partnerships"

G(BZ, CP, "Basic",
  "On 30 June 2026 the Ministry of Tourism signed an MoU with which technology company to strengthen digital promotion "
  "of India's tourism destinations under the Incredible India initiative?",
  ["Google India", "Microsoft India", "Meta India", "Amazon Web Services India"], "*",
  "Government-industry partnerships",
  "The Ministry of Tourism and Google India exchanged an MoU in New Delhi on 30 June 2026, in the presence of Tourism "
  "Minister Gajendra Singh Shekhawat. Google India will share insights on travel trends and traveller behaviour and "
  "train ministry officials in digital marketing, content and AI skills.",
  ["MoU: Ministry of Tourism + Google India (30 June 2026)", "Digital promotion; Incredible India; AI training"],
  [fact("Tourism Ministry signs MoU with Google India to boost digital promotion of tourism destinations (AIR, 30 June "
        "2026)", "bz_goog_air")],
  why="The source names Google India; the other companies are not mentioned.",
  current=ca("2026-06-30"))

G(BZ, MA, "Intermediate",
  "In August 2026 Inox Clean Energy completed the acquisition of Vena Energy's India platform for about Rs 6,000 crore. "
  "From which investor was it bought?",
  ["Global Infrastructure Partners (GIP), part of BlackRock", "Brookfield Asset Management",
   "Abu Dhabi Investment Authority", "KKR"], "*",
  "Acquisitions: renewable energy",
  "Inox Clean Energy said on 18 August 2026 that it had completed the roughly Rs 6,000 crore acquisition of Vena Energy "
  "India from Global Infrastructure Partners (GIP), owned by BlackRock, within about two months of signing.",
  ["Buyer: Inox Clean Energy", "Target: Vena Energy India (~Rs 6,000 crore)", "Seller: GIP (BlackRock)"],
  [fact("Inox Clean Energy completes Rs 6,000-crore acquisition of GIP's Vena Energy India from BlackRock (Free Press "
        "Journal, Aug 2026)", "bz_inox_fpj"),
   fact("Inox Clean Energy completes INR 6,000 crore acquisition of Vena Energy India platform (Energetica India)",
        "bz_inox_en")],
  why="The sources name GIP/BlackRock as the seller; the other investors are not involved.",
  current=ca("2026-08-18"))

G(BZ, MA, "Intermediate",
  "In August 2026 Tata Steel bought an additional 23% stake for about Rs 335 crore in a company, raising its holding to "
  "74% and making it a subsidiary. Which company?",
  ["TM International Logistics", "Tata Metaliks", "Tinplate Company of India", "Bhushan Steel"], "*",
  "Acquisitions: steel and logistics",
  "On 20 August 2026 Tata Steel completed the acquisition of an additional 23% of TM International Logistics (TMILL) "
  "for about Rs 335 crore, taking its stake to 74% and making TMILL a subsidiary.",
  ["Tata Steel + 23% of TMILL (~Rs 335 crore)", "Holding now 74%; TMILL becomes subsidiary"],
  [fact("Tata Steel completes TM International Logistics stake acquisition (Dealroom, Aug 2026)", "bz_tmill_dr"),
   fact("Tata Steel completes 23% stake acquisition in TM International Logistics for Rs 335 crore; stake now 74% "
        "(InvestyWise)", "bz_tmill_iw")],
  why="The sources name TM International Logistics; the other companies are not involved.",
  current=ca("2026-08-20"))

G(BZ, MA, "Intermediate",
  "In August 2026 Piramal Pharma completed the acquisition of a 74% controlling stake in which company, for a cash "
  "consideration of about Rs 76 crore?",
  ["Yapan Bio", "Biocon Biologics", "Syngene International", "Panacea Biotec"], "*",
  "Acquisitions: pharmaceuticals",
  "Piramal Pharma completed the acquisition of a controlling stake in Yapan Bio in August 2026 for a cash consideration "
  "of Rs 76 crore; with 74% ownership, Yapan Bio became its subsidiary.",
  ["Piramal Pharma -> 74% of Yapan Bio", "Cash ~Rs 76 crore; now a subsidiary"],
  [fact("Piramal Pharma completes acquisition of controlling stake in Yapan Bio (Pharmaceutical Technology)",
        "bz_yap_pt"),
   fact("Piramal Pharma completes acquisition of controlling stake in Yapan Bio; Rs 76 crore; 74% (Manufacturing "
        "Chemist)", "bz_yap_mc")],
  why="The sources name Yapan Bio; the other companies are not involved.",
  current=ca("2026-08-18"))

G(BZ, MA, "Intermediate",
  "Hearzap completed in August 2026 the acquisition of the Indian hearing healthcare business of which company, "
  "expanding its network to about 420 centres?",
  ["Amplifon", "Sonova", "Demant", "GN Hearing"], "*",
  "Acquisitions: healthcare",
  "Hearzap completed the acquisition of Amplifon India's hearing healthcare business in August 2026, expanding its "
  "network to about 420 centres across India.",
  ["Hearzap acquires Amplifon India's hearing business", "Network ~420 centres"],
  [fact("Hearzap completes acquisition of Amplifon India's hearing healthcare business; network to 420 centres (Indian "
        "Pharma Post)", "bz_hz_ipp")],
  why="The source names Amplifon; the other hearing-care companies are not involved.",
  current=ca("2026-08-18"))

G(BZ, MA, "Intermediate",
  "In August 2026 Waaree bought a stake in Eppeltone. What does Eppeltone mainly make?",
  ["Smart electricity meters", "Solar inverters", "Lithium-ion battery cells", "Wind turbine blades"], "*",
  "Acquisitions: energy equipment",
  "Waaree acquired a stake in Eppeltone, a smart meter company, in August 2026.",
  ["Waaree -> stake in Eppeltone", "Eppeltone: smart meters"],
  [fact("Waaree buys stake in smart meter company Eppeltone (Mercom India, Aug 2026)", "bz_wa_mer")],
  why="The source describes Eppeltone as a smart meter company.",
  current=ca("2026-08-07"))

G(BZ, CP, "Intermediate",
  "In September 2026 Kalyani Strategic Systems signed an MoU with which company to study a production facility in "
  "India and a possible joint venture for small arms and counter-drone capability?",
  ["FN Herstal (Belgium)", "Rheinmetall (Germany)", "Thales (France)", "Elbit Systems (Israel)"], "*",
  "Defence-industry partnerships",
  "On 3 September 2026 Kalyani Strategic Systems signed an MoU with Belgium's FN Herstal to study a production "
  "facility in India, technology cooperation and a possible strategic alliance or joint venture for FN Herstal "
  "products for Indian forces, including small arms and counter-UAS capability.",
  ["KSSL + FN Herstal MoU (3 Sep 2026)", "Possible JV: small arms, counter-UAS"],
  [fact("Kalyani Strategic Systems partners with FN Herstal to build small arms and counter-UAS capability in India "
        "(Aviation & Defence Universe, Sep 2026)", "bz_fn_adu")],
  why="The source names FN Herstal; the other firms are not party to this MoU.",
  current=ca("2026-09-03"))

G(BZ, CP, "Intermediate",
  "France's Naval Group signed an MoU on 18 September 2026 with which Indian company to cooperate on naval technology, "
  "shipbuilding and autonomous systems?",
  ["Nibe Limited", "Mazagon Dock Shipbuilders", "Cochin Shipyard", "Larsen & Toubro"], "*",
  "Defence-industry partnerships",
  "Naval Group and Nibe Limited (with its group companies) signed an MoU on 18 September 2026 setting a framework for "
  "cooperation in modern naval technologies, shipbuilding, defence platforms and autonomous systems.",
  ["Naval Group (France) + Nibe Ltd MoU, 18 Sep 2026", "Naval technology, shipbuilding, autonomous systems"],
  [fact("France's Naval Group, Nibe sign MoU to strengthen India's naval shipbuilding and maritime technology "
        "capabilities (Swarajya)", "bz_ng_sw"),
   fact("Naval Group and Nibe Limited sign strategic MoU on 18 September 2026 (Raksha Anirveda)", "bz_ng_ra")],
  why="The sources name Nibe Limited; the shipyards listed are not party to this MoU.",
  current=ca("2026-09-18"))

G(BZ, CP, "Intermediate",
  "Tembo Global Industries signed an MoU in September 2026 with Belgium's Lachaussee to set up what in India, valued at "
  "about EUR 50 million?",
  ["An advanced ammunition production line", "A satellite assembly plant", "A rail coach factory",
   "A green hydrogen electrolyser plant"], "*",
  "Defence-industry partnerships",
  "Tembo Global Industries signed an MoU with Belgium's Lachaussee SA on 7 September 2026 to set up an advanced "
  "ammunition production line in India, a project valued at about EUR 50 million with capacity of about 100 million "
  "rounds a year.",
  ["Tembo Global + Lachaussee (Belgium)", "Ammunition line, ~EUR 50 million, ~100 million rounds/yr"],
  [fact("Tembo Global Industries signs MoU with Belgium's Lachaussee SA to establish advanced ammunition production line "
        "in India (Aviation & Defence Universe, Sep 2026)", "bz_tem_adu")],
  why="The MoU is for an ammunition line; the other projects are not involved.",
  current=ca("2026-09-07"))

# ###################################################################### part: static (Static Awareness)
U.update({
    "st_gh_cn": ("https://citinewsroom.com/2019/12/the-evolution-of-the-ghana-cedi-opinion/", SEARCH, "2026-11-07"),
    "st_gh_pwc": ("https://www.pwc.com/gh/en/pdf/re-denomination-of-the-cedi.pdf", SEARCH, "2026-11-07"),
    "st_rw_brit": ("https://www.britannica.com/facts/Rwanda", SEARCH, "2026-11-07"),
    "st_rw_gov": ("https://www.gov.rw/about", SEARCH, "2026-11-07"),
    "st_kuno_dte": ("https://www.downtoearth.org.in/wildlife-biodiversity/dte-exclusive-two-namibian-cheetahs-released-"
                    "into-the-wild-at-kuno-national-park-88182", SEARCH, "2026-11-07"),
    "st_kuno_scmp": ("https://www.scmp.com/news/asia/south-asia/article/3192870/cheetahs-return-india-after-becoming-"
                     "extinct-1952", SEARCH, "2026-11-07"),
    "st_tad_mt": ("https://maharashtratourism.gov.in/wildlife/tadoba-andhari-tiger-reserve/", SEARCH, "2026-11-07"),
    "st_tad_ii": ("https://www.incredibleindia.gov.in/en/maharashtra/nagpur/tadoba-tiger-reserve", SEARCH, "2026-11-07"),
    "st_dnh_dh": ("https://www.deccanherald.com/india/centre-designates-daman-as-headquarters-of-2-merged-uts-of-daman-"
                  "diu-and-dadra-nagar-haveli-797100", SEARCH, "2026-11-07"),
    "st_dnh_bs": ("https://www.business-standard.com/article/pti-stories/centre-designates-daman-as-hqs-of-2-merged-uts-"
                  "120012200997_1.html", SEARCH, "2026-11-07"),
    "st_lak_ki": ("https://knowindia.india.gov.in/states-uts/lakshadweep.php", SEARCH, "2026-11-07"),
    "st_lak_mp": ("https://www.millenniumpost.in/mapping-the-states-of-india/a-hundred-thousand-islands-422026", SEARCH,
                  "2026-11-07"),
    "st_sal_de": ("https://www.dailyexcelsior.com/?p=2163359", SEARCH, "2026-11-07"),
    "st_sal_pl": ("https://powerline.net.in/2026/02/24/nhpc-plans-to-expedite-desilting-at-salal-dam-in-jk-to-restore-"
                  "reservoir-capacity/", SEARCH, "2026-11-07"),
    "st_sri_aa": ("https://currentaffairs.adda247.com/srisailam-project-location-river-water-supply-features-significance-"
                  "and-hydroelectric-power-generation/amp/", SEARCH, "2026-11-07"),
    "st_sri_np": ("https://www.nativeplanet.com/srisailam/attractions/srisailam-dam", SEARCH, "2026-11-07"),
    "st_sri_wiki": ("https://www.wikipedia.org/wiki/Srisailam_Dam", SEARCH, "2026-11-07"),
    "st_sri_tt": ("https://telanganatoday.com/srisailam-dam-gates-opened-as-krishna-floodwaters-rise", SEARCH,
                  "2026-11-07"),
    "st_sri_dh": ("https://www.deccanherald.com/india/centre-announces-iconic-bridge-on-krishna-to-connect-andhra-"
                  "telangana-1153706.html", SEARCH, "2026-11-07"),
    "st_pol_ls": ("https://eparlib.nic.in/bitstream/123456789/804595/1/AU3889.pdf", SEARCH, "2026-11-07"),
    "st_pol_cag": ("https://cag.gov.in/webroot/uploads/download_audit_report/2025/PA-on-Polavaram-Irrigation-Project-"
                   "069aaece202fa02.61046831.pdf", SEARCH, "2026-11-07"),
    "st_pol_hans": ("https://hanssite.hocalwire.in/hans/opinion/news-analysis/polavaram-decades-of-delay-emerging-progress-"
                    "and-the-road-ahead-1063567", SEARCH, "2026-11-07"),
    "st_nag_kba": ("https://www.keybiodiversityareas.org/site/factsheet/18225", SEARCH, "2026-11-07"),
    "st_nag_ip": ("https://www.internationalparks.org/india/Nagarhole", SEARCH, "2026-11-07"),
    "st_tb_tt": ("https://telanganatoday.com/tungabhadra-dam-gate-washed-away-srisailam-and-nsp-officials-on-alert",
                 SEARCH, "2026-11-07"),
    "st_tb_sandrp": ("https://sandrp.in/2024/08/11/tungabhadra-dam-a-crest-gate-washed-away-in-august-2024/", SEARCH,
                     "2026-11-07"),
    "st_tb_dh": ("https://www.deccanherald.com/amp/story/india%2Fkarnataka%2Ftungabhadra-dam-gate-washed-away-downstream-"
                 "on-alert-3146596", SEARCH, "2026-11-07"),
    "st_tri_asm": ("https://tripuraassembly.nic.in/historicalbackground.html", SEARCH, "2026-11-07"),
    "st_tri_itv": ("https://www.indiatvnews.com/explainers/manipur-meghalaya-and-tripura-celebrate-statehood-day-know-their-"
                   "history-and-importance-pm-narendra-modi-latest-updates-2024-01-21-912918", SEARCH, "2026-11-07"),
    "st_pln_nbp": ("https://nbp.pl/polski-zloty-i-niezaleznosc-nbp", SEARCH, "2026-11-07"),
    "st_pln_mf": ("https://mf-arch2.mf.gov.pl/en/web/bip/ministry-of-finance/poland-in-eu/euro-in-poland", SEARCH,
                  "2026-11-07"),
    "st_pln_pap": ("https://www.pap.pl/en/news/poland-may-mull-euro-adoption-8-10-years-central-bank-head-says", SEARCH,
                   "2026-11-07"),
})
STA = "Static Awareness"
CC, NPD, ISF = "Capitals and currencies", "National parks and dams", "Indian states facts"

# ------------------------------------------------------------------ Basic (6)
G(STA, CC, "Basic", "What is the currency of Ghana?",
  ["Cedi", "Naira", "Shilling", "Dalasi"], "*",
  "Currencies of Africa",
  "Ghana's currency is the cedi. On 1 July 2007 the Bank of Ghana redenominated it, with 10,000 old cedis becoming one "
  "Ghana cedi (GH¢1), divided into 100 pesewas.",
  ["Ghana: cedi (GH¢), 100 pesewas", "Redenominated 1 July 2007 (10,000 old = 1 new)"],
  [fact("The evolution of the Ghana cedi: redenomination of 2007 (Citi Newsroom)", "st_gh_cn"),
   fact("PwC Ghana: re-denomination of the cedi", "st_gh_pwc")],
  why="The naira is Nigeria's currency; the shilling and dalasi belong to other countries.")

G(STA, CC, "Basic", "What is the currency of Rwanda, whose capital is Kigali?",
  ["Rwandan franc", "Rwandan shilling", "Rwandan birr", "Rwandan kwacha"], "*",
  "Currencies of Africa",
  "Rwanda's capital is Kigali and its monetary unit is the Rwandan franc, issued by the National Bank of Rwanda.",
  ["Rwanda: capital Kigali", "Currency: Rwandan franc (RWF)"],
  [fact("Britannica, Rwanda facts and stats: capital Kigali; monetary unit Rwandan franc", "st_rw_brit"),
   fact("Government of Rwanda: About Rwanda", "st_rw_gov")],
  why="Rwanda uses the franc; the shilling, birr and kwacha are currencies of other African countries.")

G(STA, NPD, "Basic",
  "Kuno National Park, where cheetahs brought from Namibia were released on 17 September 2022 under Project Cheetah, is "
  "located in which state?",
  ["Madhya Pradesh", "Rajasthan", "Gujarat", "Chhattisgarh"], "*",
  "National parks: wildlife reintroduction",
  "On 17 September 2022 the Prime Minister released cheetahs flown in from Namibia into an enclosure at Kuno National "
  "Park in Sheopur district, Madhya Pradesh, about seven decades after the cheetah went extinct in India.",
  ["Kuno NP: Sheopur district, Madhya Pradesh", "Namibian cheetahs released 17 Sep 2022"],
  [fact("DTE: Namibian cheetahs released into the wild at Kuno National Park, Madhya Pradesh", "st_kuno_dte"),
   fact("Cheetahs return to India after becoming extinct in 1952; released at Kuno National Park, Madhya Pradesh (SCMP, "
        "Sep 2022)", "st_kuno_scmp")],
  why="Kuno is in Madhya Pradesh; it is not in the other states.")

G(STA, NPD, "Basic",
  "The Tadoba-Andhari Tiger Reserve, described as Maharashtra's oldest and largest national park, is located in which "
  "district?",
  ["Chandrapur", "Gadchiroli", "Amravati", "Nashik"], "*",
  "National parks: Maharashtra",
  "Tadoba-Andhari Tiger Reserve lies in Chandrapur district, Maharashtra. Tadoba was declared a national park in 1955; "
  "the adjoining Andhari Wildlife Sanctuary was created in 1986, and the two were merged in 1995 to form the tiger "
  "reserve.",
  ["Tadoba-Andhari TR: Chandrapur district", "National park 1955; merged with Andhari WLS 1995"],
  [fact("Maharashtra Tourism: Tadoba Andhari Tiger Reserve, Chandrapur", "st_tad_mt"),
   fact("Incredible India: Tadoba Tiger Reserve, Maharashtra's oldest and largest national park", "st_tad_ii")],
  why="The reserve is in Chandrapur district; the other districts are not its location.")

G(STA, ISF, "Basic",
  "Which town was designated the headquarters of the merged Union Territory of Dadra and Nagar Haveli and Daman and "
  "Diu, which came into existence on 26 January 2020?",
  ["Daman", "Silvassa", "Diu", "Vapi"], "*",
  "Union Territories: reorganisation",
  "The Dadra and Nagar Haveli and Daman and Diu (Merger of Union Territories) Act, 2019 took effect on 26 January "
  "2020. On 22 January 2020 the Union Cabinet designated Daman as the headquarters of the merged UT; Silvassa had been "
  "the capital of the former UT of Dadra and Nagar Haveli.",
  ["Merger effective 26 Jan 2020", "HQ: Daman (Silvassa was DNH's capital)"],
  [fact("Centre designates Daman as headquarters of 2 merged UTs of Daman & Diu and Dadra & Nagar Haveli (Deccan "
        "Herald/PTI, 22 Jan 2020)", "st_dnh_dh"),
   fact("Centre designates Daman as HQs of 2 merged UTs (Business Standard/PTI)", "st_dnh_bs")],
  why="Silvassa was the earlier capital of Dadra and Nagar Haveli; Diu and Vapi are not the headquarters.")

G(STA, ISF, "Basic",
  "The Union Territory of Lakshadweep, with its capital at Kavaratti, was known by which name until 1973?",
  ["Laccadive, Minicoy and Amindivi Islands", "Andaman and Nicobar Islands", "Malabar Islands",
   "Maldive-Minicoy Islands"], "*",
  "Union Territories: names",
  "The islands became a Union Territory in 1956 as the Laccadive, Minicoy and Amindivi Islands and were renamed "
  "Lakshadweep on 1 November 1973 by an Act of Parliament. Kavaratti is the capital.",
  ["UT formed 1956: Laccadive, Minicoy and Amindivi Islands", "Renamed Lakshadweep in 1973; capital Kavaratti"],
  [fact("Know India: Lakshadweep (Kavaratti)", "st_lak_ki"),
   fact("A hundred thousand islands: Laccadive, Minicoy and Amindivi Islands renamed Lakshadweep in 1973 (Millennium "
        "Post)", "st_lak_mp")],
  why="The other names never applied to this Union Territory.")

# ------------------------------------------------------------------ Intermediate (1)
G(STA, NPD, "Intermediate",
  "The Salal hydroelectric power station of NHPC in Reasi district, Jammu and Kashmir, whose reservoir NHPC began "
  "desilting after it lost most of its storage to sediment, is on which river?",
  ["Chenab", "Jhelum", "Ravi", "Tawi"], "*",
  "Dams of India: Jammu and Kashmir",
  "Salal is a 690 MW run-of-the-river station of NHPC on the Chenab in Reasi district. Sedimentation reduced its "
  "reservoir from about 284 MCM to under 10 MCM, and NHPC planned dredging, flushing and revival of under-sluice gates.",
  ["Salal (690 MW, NHPC): Chenab, Reasi district", "Reservoir lost most storage to silt"],
  [fact("Salal power station reservoir suffers dramatic loss of storage up to 96% (Daily Excelsior)", "st_sal_de"),
   fact("NHPC plans to expedite desilting at Salal Dam in J&K (Power Line, Feb 2026)", "st_sal_pl")],
  why="Salal is on the Chenab; the other rivers are not its site.",
  current=ca("2026-02-24"))

# ------------------------------------------------------------------ Advanced (6)
GS(STA, NPD, "Advanced", "the Srisailam Dam",
   ["It is built across the Krishna in a gorge of the Nallamala Hills.",
    "It lies on the border of Andhra Pradesh and Telangana.",
    "It is built on the Godavari, upstream of the Sir Arthur Cotton Barrage."],
   [True, True, False],
   "Dams of India: Krishna basin",
   "The Srisailam Dam, officially the Neelam Sanjeeva Reddy Srisailam Project, is built across the Krishna in a deep "
   "gorge of the Nallamala Hills on the Andhra Pradesh-Telangana border, with Nagarjuna Sagar downstream. It is not on "
   "the Godavari, so statement 3 is wrong.",
   [fact("Srisailam Dam, built in 1981 across the Krishna River, on the Andhra Pradesh-Telangana border; Nagarjuna Sagar "
         "downstream (Telangana Today)", "st_sri_tt"),
    fact("Iconic bridge across the Krishna (Srisailam backwaters) in the Nallamala range linking Telangana and Andhra "
         "Pradesh (Deccan Herald)", "st_sri_dh"),
    fact("Srisailam Dam (Wikipedia): Krishna river, Nandyal (AP) and Nagarkurnool (Telangana)", "st_sri_wiki")],
   why="Statement 3 is wrong: Srisailam is on the Krishna, not the Godavari.")

GS(STA, NPD, "Advanced", "the Polavaram Irrigation Project",
   ["It is being built on the Krishna river.",
    "It was declared a National Project under Section 90 of the Andhra Pradesh Reorganisation Act, 2014.",
    "It is located near Polavaram in Eluru district (formerly part of West Godavari district)."],
   [False, True, True],
   "Dams of India: Godavari basin",
   "The Polavaram project is on the Godavari, about 42 km upstream of the Sir Arthur Cotton Barrage at Dowlaiswaram, so "
   "statement 1 is wrong. It was declared a National Project under Section 90 of the AP Reorganisation Act, 2014, and "
   "lies near Polavaram mandal of Eluru district (formerly West Godavari).",
   [fact("Lok Sabha answer: Polavaram declared a National Project under Section 90 of the AP Reorganisation Act, 2014",
         "st_pol_ls"),
    fact("CAG performance audit of the Polavaram Irrigation Project (2025)", "st_pol_cag"),
    fact("Polavaram, 42 km upstream of the Sir Arthur Cotton Barrage, near Polavaram mandal of Eluru district (The Hans "
         "India)", "st_pol_hans")],
   why="Statement 1 is wrong: Polavaram is on the Godavari.")

GS(STA, NPD, "Advanced", "Nagarhole National Park (Rajiv Gandhi National Park)",
   ["It spreads over Kodagu and Mysuru districts of Karnataka.",
    "It is located in Kerala's Wayanad district.",
    "It was declared a Tiger Reserve in 1999 and is part of the Nilgiri Biosphere Reserve."],
   [True, False, True],
   "National parks: Karnataka",
   "Nagarhole (Rajiv Gandhi) National Park spreads over Kodagu and Mysuru districts of Karnataka, not Wayanad, so "
   "statement 2 is wrong. It was declared a Tiger Reserve in 1999 and forms part of the Nilgiri Biosphere Reserve; the "
   "Kabini reservoir separates it from Bandipur.",
   [fact("Key Biodiversity Areas: Nagarhole National Park, Kodagu and Mysuru districts, Karnataka", "st_nag_kba"),
    fact("International Parks: Nagarhole, declared a Tiger Reserve in 1999, part of the Nilgiri Biosphere Reserve",
         "st_nag_ip")],
   why="Statement 2 is wrong: Nagarhole is in Karnataka (Kodagu and Mysuru).")

GS(STA, NPD, "Advanced", "the Tungabhadra Dam",
   ["It was completed in 1953 as a joint project of the erstwhile Hyderabad State and Madras Presidency.",
    "It is near Hosapete in Vijayanagara district of Karnataka.",
    "In August 2024 one of its crest gates (gate no. 19) was washed away after its chain snapped."],
   [True, True, True],
   "Dams of India: Karnataka",
   "Construction of the Tungabhadra Dam began in 1949 and ended in 1953, as a joint project of the Kingdom of Hyderabad "
   "and the Madras Presidency. It stands near Hosapete in Vijayanagara district, Karnataka. On the night of 10-11 "
   "August 2024 its 19th crest gate (of 33) was washed away after its chain snapped. All three statements are correct.",
   [fact("Tungabhadra dam: construction began 1949, completed 1953; joint project of Hyderabad and Madras Presidency "
         "(Telangana Today)", "st_tb_tt"),
    fact("SANDRP: Tungabhadra Dam near Hospete, Vijayanagara district; crest gate washed away in August 2024",
         "st_tb_sandrp"),
    fact("Tungabhadra dam gate (19th of 33) washed away; downstream on alert (Deccan Herald, Aug 2024)", "st_tb_dh")],
   why="All three statements are correct.")

GS(STA, ISF, "Advanced", "the history of Tripura",
   ["It became a Union Territory on 1 November 1956.",
    "It became a full-fledged State on 15 August 1947.",
    "It attained statehood under the North-Eastern Areas (Reorganisation) Act, 1971, on 21 January 1972."],
   [True, False, True],
   "Statehood of north-eastern States",
   "Tripura, given Part 'C' status in 1950, became a Union Territory on 1 November 1956 and a full-fledged State on 21 "
   "January 1972 under the North-Eastern Areas (Reorganisation) Act, 1971, together with Manipur and Meghalaya. It was "
   "not a State in 1947, so statement 2 is wrong.",
   [fact("Tripura Legislative Assembly: historical background - Part C status 1950, Union Territory 1 November 1956, "
         "statehood 21 January 1972", "st_tri_asm"),
    fact("Manipur, Meghalaya and Tripura celebrate Statehood Day (21 January); North-Eastern Areas (Reorganisation) Act, "
         "1971 (India TV)", "st_tri_itv")],
   why="Statement 2 is wrong: Tripura became a State only on 21 January 1972.")

GS(STA, CC, "Advanced", "Poland's currency",
   ["Poland adopted the euro in 2014.",
    "The zloty is issued by Narodowy Bank Polski (the National Bank of Poland).",
    "Under its EU accession treaty Poland is committed to adopting the euro eventually, but no date has been set."],
   [False, True, True],
   "Currencies of Europe",
   "Poland's currency is the zloty, issued by Narodowy Bank Polski. Poland has not adopted the euro, so statement 1 is "
   "wrong; it is committed under its accession treaty to adopt the euro eventually, but no target date has been set, and "
   "the NBP governor has said adoption could be discussed only years from now.",
   [fact("NBP: the Polish zloty and the independence of NBP", "st_pln_nbp"),
    fact("Ministry of Finance (Poland): euro in Poland - accession treaty commitment, no target date", "st_pln_mf"),
    fact("Poland may mull euro adoption in 8-10 years, central bank head says (PAP)", "st_pln_pap")],
   why="Statement 1 is wrong: Poland still uses the zloty.")


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
    pkg = json.loads((ROOT / "batches" / "plans" / "packages" / "GA_pkg1.json").read_text(encoding="utf-8"))
    assert pkg["prefix"] == "GA" and pkg["package"] == 1 and list(pkg["batches"]) == ["010"]
    ga = pkg["batches"]["010"]
    assert ga["batch_id"] == BATCH and ga["count"] == 149 and ga["stimulus_id_start"] == "STIM_GA_010101"
    first = int(ga["question_ids"][0].rsplit("_", 1)[1])
    assert len({it["text"][:120] for it in items}) == len(items), "stem prefixes must be unique"
    assert BLIND_MATCHED <= {it["text"][:120] for it in items}, "stale blind-check entry"
    counts = place_answers(items)
    out = []
    for n, it in enumerate(items):
        ans = it["answer"]
        opts = it["options"]
        hows = {f.pop("_how") for f in it["facts"]}
        verified_by = list(AI_CHECK) if it["text"][:120] in BLIND_MATCHED else ["ai:self-recheck"]
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

    # quota, ID range, stimulus start and balance checks against the package before writing
    have = Counter((q["topic"], q["difficulty"]) for q in out)
    for t in ga["topics"]:
        for d, k in t["quota"].items():
            assert have[(t["topic"], d)] == k, (t["topic"], d, have[(t["topic"], d)], k)
        assert all(q["subtopic"] in t["subtopics"] for q in out if q["topic"] == t["topic"]), t["topic"]
    assert {q["topic"] for q in out} == {t["topic"] for t in ga["topics"]}
    assert dict(Counter(q["difficulty"] for q in out)) == ga["by_difficulty"]
    assert len(out) == ga["count"] == 149
    assert out[0]["question_id"] == ga["question_ids"][0] and out[-1]["question_id"] == ga["question_ids"][1]
    for q in out:
        if q["topic"] in CA_TOPICS:
            assert CA_FROM <= q["current_affairs"]["event_date"] <= CA_TO, q["question_id"]
        texts = [o["text"] for o in q["options"]]
        if texts in (S12, S123):
            assert q["correct_answer"] in LETTERS
    assert len({q["question_text"] for q in out}) == len(out)
    assert max(counts.values()) - min(counts.values()) <= 2, counts
    # balance: National CA at most about a quarter on defence
    assert sum(q["subtopic"] == "Defence" for q in out if q["topic"] == "National Current Affairs") <= 2
    return out, counts, ga


_pkg = json.loads((ROOT / "batches" / "plans" / "packages" / "GA_pkg1.json").read_text(encoding="utf-8"))
_order = [t["topic"] for t in _pkg["batches"]["010"]["topics"]]
_rank = {"Basic": 0, "Intermediate": 1, "Advanced": 2}
QUESTIONS.sort(key=lambda it: (_order.index(it["topic"]), _rank[it["difficulty"]]))

STIMULI = []  # no shared stimuli in this package; stimulus IDs would start at STIM_GA_010101
questions, keys, _ga = build(QUESTIONS)
print("inferred dates:", len(INFERRED))
for d, why in INFERRED:
    print("  ", d, why)
print("blind-check matched:", sum("ai:independent-check" in q["verification"]["verified_by"] for q in questions))
batch = {
    "schema_version": "1.0",
    "batch_id": BATCH,
    "created_at": TODAY,
    "notes": "BATCH_010 General Awareness, package GA_pkg1 (all GA topics of the batch): 149 original questions. "
             "Current-affairs topics (National and International Current Affairs, Appointments, Awards, Sports, "
             "Summits, Economic Affairs, Business) test events dated 2025-11-01 to 2026-11-04, with event dates from "
             "the sources and review_by 2027-05-05. Other time-sensitive facts also carry current_affairs dates. No "
             "fact or event tested in BATCH_000 to BATCH_009 GA (or in the Banking stems) is tested again. checked_on "
             "is the day each page was actually checked; verified_by says whether each question's sources were opened "
             "(web:fact-check) or confirmed only in search results (web:search-confirmed); ai:independent-check only "
             "on questions a fresh solver answered key-free and matched, unchanged afterwards. Pending human review. "
             "Event dates inferred (source gives no exact day): " +
             ("; ".join(f"{d} ({why})" for d, why in INFERRED) or "none") + ".",
    "stimuli": STIMULI,
    "questions": questions,
}
out = ROOT / _ga["output"]
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions; keys {dict(sorted(keys.items()))})")
