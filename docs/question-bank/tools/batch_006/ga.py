"""Writes batches/parts/BATCH_006_GA.json: the 150 General Awareness questions of BATCH_006.

Same structure as tools/batch_005/ga.py. Current-affairs topics (National and International Current Affairs,
Appointments, Awards, Sports, Summits, Economic Affairs, Business) test events dated 2025-11-01 to 2026-11-04 with
event dates from the sources; every such question carries current_affairs {event_date, review_by 2027-05-05}. Other
time-sensitive facts (schemes, policies, reports, themes of days) carry current_affairs too. Where a source gives no
exact day, ca(..., inferred=reason) records it and the list is printed and written into the batch notes.

Every question has fact_checks. Each URL is marked OPENED (fetched and read on 2026-11-05, giving "web:fact-check")
or SEARCH (confirmed only from search-result text on 2026-11-05, giving "web:search-confirmed"). Sites that refused a
fetch (e.g. pib.gov.in, business-standard.com, thestatesman.com, pmindia.gov.in) were not worked around.
Explanations and why_others_wrong state only facts backed by the listed sources, or stay neutral.

All earlier GA stems (BATCH_000 sample, BATCH_001_GA to BATCH_005_GA) were read first; no fact or event tested
there is tested again, and no event is used twice in this batch.

Statement questions have their key fixed by the statements (computed from truth values); other questions are written
with the correct option first and answer "*", and are then placed so that keys are balanced A to D.

    python tools/batch_006/ga.py
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
BATCH = "BATCH_006"
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



AI_CHECK = ['ai:independent-check']
# reworded after the independent key-free check; re-solved by the author instead
REWORDED_AFTER_CHECK = ['announced in May 2026 that it would reverse']


# ###################################################################### part: nat (national + static)
# ###################################################################### part: nat (national CA + static)
U.update({
    "nat_suryakiran_trib": ("https://www.tribuneindia.com/news/world/india-nepal-joint-military-exercise-suryakiran-"
                            "underway-in-uttarakhand", OPENED),
    "nat_ekuverin_dr": ("https://www.drishtiias.com/daily-updates/daily-news-analysis/exercise-ekuverin-2/print_manually",
                        OPENED),
    "nat_ekuverin_mm": ("https://www.manoramayearbook.in/current-affairs/india/2025/12/02/india-maldives-ekuverin-"
                        "exercise.html", OPENED),
    "nat_glaw_air": ("https://newsonair.gov.in/glaw-lake-of-arunachal-pradesh-designated-as-101st-ramsar-site-first-in-"
                     "the-state/", OPENED),
    "nat_glaw_fpj": ("https://www.freepressjournal.in/lifestyle/arunachal-pradeshs-glaw-lake-becomes-indias-101st-ramsar-"
                     "site-state-gets-first-international-wetland", OPENED),
    "nat_maitree_air": ("https://newsonair.gov.in/indian-army-contingent-departs-for-thailand-for-joint-military-exercise-"
                        "maitree-xv/", OPENED),
    "nat_maitree_adu": ("https://www.aviation-defence-universe.com/indian-army-contingent-departs-for-india-thailand-"
                        "joint-military-exercise-maitree-xv/", OPENED),
    "nat_garuda_air": ("https://www.newsonair.gov.in/iaf-contingent-arrives-in-france-for-garuda-2025-air-exercise",
                       OPENED),
    "nat_garuda_adu": ("https://www.aviation-defence-universe.com/exercise-garuda-25-concludes-indo-french-air-forces-"
                       "successfully-complete-8th-edition-of-bilateral-air-exercise/", OPENED),
    "nat_dustlik_air": ("https://www.newsonair.gov.in/7th-edition-of-india-uzbekistan-joint-military-exercise-dustlik-"
                        "2026-being-conducted-at-gurumsaray-field-training-area", OPENED),
    "nat_vinbax_trib": ("https://www.tribuneindia.com/news/world/6th-edition-of-india-vietnam-bilateral-exercise-vinbax-"
                        "2025-concludes-in-hanoi/", OPENED),
    "nat_slinex_gkt": ("https://www.gktoday.in/india-and-sri-lanka-conduct-slinex-26-maritime-exercise/", OPENED),
    "nat_veer_air": ("https://newsonair.gov.in/india-japan-conduct-air-exercise-veer-guardian-2026-at-air-force-station-"
                     "jodhpur/", OPENED),
    "nat_udara_ians": ("https://ianslive.in/udara-shakti-exercise-strengthens-interoperability-between-india-and-"
                       "malaysia--20260814192838", OPENED),
    "nat_pralay_etv": ("https://www.etvbharat.com/en/bharat/drdo-successfully-conducts-salvo-launch-of-two-pralay-"
                       "missiles-in-quick-succession-enn25123103873", OPENED),
    "nat_surha_dr": ("https://www.drishtiias.com/daily-updates/daily-news-analysis/jai-prakash-narayan-bird-sanctuary-"
                     "indias-100th-ramsar-site/print_manually", OPENED),
    "nat_shekha_dr": ("https://www.drishtiias.com/daily-updates/daily-news-analysis/shekha-jheel-bird-sanctuary-as-"
                      "indias-99th-ramsar-site/print_manually", OPENED),
    "nat_sukhna_gkt": ("https://www.gktoday.in/india-adds-sukhna-wetland-and-sauj-jheel-to-ramsar-list/", OPENED),
    "nat_hate_tt": ("https://telanganatoday.com/karnataka-assembly-clears-indias-first-anti-hate-speech-law-amid-bjp-"
                    "protest", OPENED),
    "nat_rail_sep_air": ("https://newsonair.gov.in/union-cabinet-approves-railways-8-multitracking-projects-worth-over-"
                         "rs-20800-crore/", OPENED),
    "nat_rail_may_ins": ("https://inshorts.com/en/news/cabinet-approves--23-437-crore-railway-projects-across-6-states-"
                         "1778060605291", OPENED),
    "nat_rail_may_ao": ("https://www.angelone.in/news/economy/union-cabinet-of-india-approves-rs-23437-crore-railway-"
                        "projects-to-boost-capacity", OPENED),
    "nat_kabrai_ians": ("https://ianslive.in/cabinet-approves-rs-7145-crore-project-to-build-new-kanpur-kabrai-highway--"
                        "20260701155104", OPENED),
    "nat_ucc_guj_air": ("https://www.newsonair.gov.in/gujarat-assembly-passes-uniform-civil-code-bill-after-7-hour-debate",
                        OPENED),
    "nat_ucc_asm_sent": ("https://www.sentinelassam.com/breakingnews/assam-passes-uniform-civil-code-bill-becomes-first-"
                         "northeastern-state-and-third-in-india-to-enact-ucc", OPENED),
    "nat_ucc_asm_dr": ("https://www.drishtiias.com/state-pcs-current-affairs/assam-becomes-third-state-to-pass-uniform-"
                       "civil-code-ucc-bill-2026/print_manually", OPENED),
    "nat_ucc_mp_uni": ("https://test.uniindia.com/news/north/assembly-mp-ucc-bill-passed/3916978.html", OPENED),
    "nat_tl_air": ("https://newsonair.gov.in/five-new-heritage-sites-and-proposals-added-to-indias-unesco-tentative-"
                   "list/", OPENED),
    "nat_tl_dr": ("https://www.drishtiias.com/state-pcs-current-affairs/three-indian-sites-added-to-unesco-tentative-"
                  "list-of-world-heritage-sites", OPENED),
    "nat_hp_wiki": ("https://en.wikipedia.org/wiki/Himachal_Pradesh", OPENED),
    "nat_bhitar_wiki": ("https://en.wikipedia.org/wiki/Bhitarkanika_National_Park", OPENED),
    "nat_dong_wiki": ("https://en.wikipedia.org/wiki/Vietnamese_%C4%91%E1%BB%93ng", OPENED),
})

T = "National Current Affairs"
GOV, ST, DEF = "Government decisions", "States and UTs", "Defence"

# ------------------------------------------------------------------ Basic (4)
G(T, DEF, "Basic",
  "The 19th edition of Exercise Suryakiran, held at Pithoragarh (Uttarakhand) from 25 November to 8 December 2025, is "
  "a joint military exercise between the Indian Army and the army of which country?",
  ["Nepal", "Bhutan", "Bangladesh", "Myanmar"], "*",
  "Exercise Suryakiran",
  "Suryakiran is the India-Nepal army exercise. Its 19th edition (Suryakiran XIX) was held at Pithoragarh from 25 "
  "November to 8 December 2025, with 334 personnel on each side, mainly from India's Assam Regiment and Nepal's Devi "
  "Datta Regiment. It covered jungle warfare and counter-terrorism in mountainous terrain under a UN Chapter VII "
  "mandate, along with HADR drills.",
  ["Suryakiran: India-Nepal", "19th edition: Pithoragarh, 25 Nov-8 Dec 2025"],
  [fact("Suryakiran XIX, India-Nepal, Pithoragarh, Uttarakhand, 25 November-8 December 2025; 334 personnel each, Assam "
        "Regiment and Devi Datta Regiment", "nat_suryakiran_trib")],
  why="The source names the Nepal Army as India's partner in Suryakiran; Bhutan, Bangladesh and Myanmar are not.",
  current=ca("2025-11-25"))

G(T, DEF, "Basic",
  "The 14th edition of Exercise Ekuverin, a joint military exercise whose name means 'Friends' in Dhivehi, was held "
  "in Thiruvananthapuram in December 2025. India conducts this exercise with which country?",
  ["Maldives", "Sri Lanka", "Mauritius", "Seychelles"], "*",
  "Exercise Ekuverin",
  "Ekuverin is held between the Indian Army and the Maldives National Defence Force (MNDF); 'Ekuverin' means "
  "'Friends' in Dhivehi, the Maldivian language. The 14th edition began in Thiruvananthapuram, Kerala, in early "
  "December 2025 and was to run till 15 December, focusing on counter-insurgency and counter-terrorism in jungle, "
  "semi-urban and coastal terrain.",
  ["Ekuverin = 'Friends' (Dhivehi)", "India-Maldives (MNDF)", "14th edition: Thiruvananthapuram, Dec 2025"],
  [fact("14th edition of Ekuverin, Indian Army and Maldives National Defence Force, Thiruvananthapuram; name means "
        "'Friends' in Dhivehi", "nat_ekuverin_dr"),
   fact("14th Ekuverin at Thiruvananthapuram, Kerala, concluding 15 December; article dated 2 December 2025",
        "nat_ekuverin_mm")],
  why="Dhivehi is the language of the Maldives, and the source names the MNDF as the partner force.",
  current=ca("2025-12-02", inferred="source article dated 2 Dec 2025 reports the start; exact start day not stated"))

G(T, ST, "Basic",
  "Glaw Lake, designated India's 101st Ramsar site in August 2026, became the first Ramsar site of which state?",
  ["Arunachal Pradesh", "Sikkim", "Nagaland", "Meghalaya"], "*",
  "Ramsar sites in India",
  "Union Environment Minister Bhupender Yadav announced on 3 August 2026 that Glaw Lake had been designated India's "
  "101st Ramsar site. It lies within the Kamlang Tiger Reserve and Wildlife Sanctuary and is Arunachal Pradesh's "
  "first Ramsar site. India had 26 Ramsar sites in 2014.",
  ["Glaw Lake: 101st Ramsar site (3 Aug 2026)", "Within Kamlang Tiger Reserve", "First in Arunachal Pradesh"],
  [fact("Glaw Lake designated India's 101st Ramsar Site, first in Arunachal Pradesh, within Kamlang Tiger Reserve and "
        "Wildlife Sanctuary; announced by Bhupender Yadav on 3 August 2026; India had 26 sites in 2014", "nat_glaw_air"),
   fact("Glaw Lake: Arunachal Pradesh's first Ramsar Site and India's 101st", "nat_glaw_fpj")],
  why="The sources describe Glaw Lake as Arunachal Pradesh's first Ramsar site; it is not in the other states.",
  current=ca("2026-08-03"))

G(T, DEF, "Basic",
  "MAITREE-XV, a joint military exercise held at Vibhavadi Rangsit Camp, Surat Thani, from 18 to 31 August 2026, is "
  "conducted between the Indian Army and the army of which country?",
  ["Thailand", "Malaysia", "Cambodia", "Myanmar"], "*",
  "Exercise Maitree",
  "MAITREE is the India-Thailand joint military exercise. Its 15th edition was held at Vibhavadi Rangsit Camp, Surat "
  "Thani, Thailand, from 18 to 31 August 2026, with 85 personnel from each side; the Indian contingent was drawn mainly "
  "from 9 Gorkha Rifles. The previous edition was held at Umroi, Meghalaya, in September 2025.",
  ["MAITREE: India-Thailand", "15th edition: Surat Thani, 18-31 Aug 2026", "Indian unit: 9 Gorkha Rifles"],
  [fact("MAITREE-XV, 15th India-Thailand exercise, Vibhavadi Rangsit Camp, Surat Thani, 18-31 August 2026; 85 "
        "personnel each; previous edition at Umroi, Meghalaya, September 2025", "nat_maitree_adu"),
   fact("MAITREE-XV ends 31 August 2026; Indian contingent mainly from 9 Gorkha Rifles; Royal Thai Army contingent "
        "from 3rd Battalion, 25th Infantry Brigade", "nat_maitree_air")],
  why="The sources name the Royal Thai Army as the partner; Malaysia, Cambodia and Myanmar are not part of MAITREE.",
  current=ca("2026-08-18"))

# ------------------------------------------------------------------ Intermediate (13)
G(T, DEF, "Intermediate",
  "Exercise Garuda 25, held from 16 to 27 November 2025 with Indian Su-30MKI jets and French Rafales, was conducted at "
  "which French air base?",
  ["Mont-de-Marsan", "Istres", "Saint-Dizier", "Orange"], "*",
  "Exercise Garuda (India-France air exercise)",
  "Garuda is the bilateral air exercise of the Indian Air Force and the French Air and Space Force. Its 8th edition, "
  "Garuda 25, was held at Air Base 118, Mont-de-Marsan, from 16 to 27 November 2025. IL-78 tankers and C-17 Globemaster "
  "III aircraft supported the IAF's Su-30MKI fighters.",
  ["Garuda: IAF + French Air and Space Force", "8th edition: Mont-de-Marsan, 16-27 Nov 2025"],
  [fact("Garuda-2025, 16-27 November 2025, Mont-de-Marsan Air Base, Su-30MKI and Rafale", "nat_garuda_air"),
   fact("Garuda 25, 8th edition, concluded 27 November 2025 at Air Base 118, Mont-de-Marsan; IL-78 and C-17 support",
        "nat_garuda_adu")],
  why="The sources name Mont-de-Marsan as the venue; the other bases were not the venue of Garuda 25.",
  current=ca("2025-11-16"))

G(T, DEF, "Intermediate",
  "The 7th edition of the India-Uzbekistan joint military exercise DUSTLIK, which concluded on 25 April 2026, was held "
  "at the Gurumsaray Field Training Area in which region of Uzbekistan?",
  ["Namangan", "Termez", "Samarkand", "Bukhara"], "*",
  "Exercise Dustlik",
  "DUSTLIK is the India-Uzbekistan joint military exercise. Its 7th edition, DUSTLIK 2026, was held at the Gurumsaray "
  "Field Training Area, Namangan, in semi-mountainous terrain, and concluded on 25 April 2026. It focused on special "
  "operations against unlawful armed groups.",
  ["DUSTLIK: India-Uzbekistan", "7th edition: Gurumsaray, Namangan; ended 25 Apr 2026"],
  [fact("7th edition of India-Uzbekistan exercise DUSTLIK 2026 at Gurumsaray Field Training Area, Namangan, "
        "Uzbekistan, concluding 25 April 2026; semi-mountainous terrain", "nat_dustlik_air")],
  why="The source places Gurumsaray in Namangan; Termez, Samarkand and Bukhara were not the venue.",
  current=ca("2026-04-25"))

G(T, DEF, "Intermediate",
  "VINBAX 2025, the sixth edition of a bilateral army exercise focused on UN peacekeeping and held from 11 to 27 "
  "November 2025 at the Mieu Mon Training Centre, was conducted between India and which country?",
  ["Vietnam", "Cambodia", "Laos", "Indonesia"], "*",
  "Exercise VINBAX",
  "VINBAX is the India-Vietnam bilateral exercise between the Indian Army and the Vietnam People's Army on UN "
  "peacekeeping operations. The sixth edition ran from 11 to 27 November 2025 at the Mieu Mon Training Centre in Hanoi, "
  "with over 300 personnel, including engineer, medical, peacekeeping and military observer elements.",
  ["VINBAX: India-Vietnam (UN peacekeeping)", "6th edition: Mieu Mon, Hanoi, 11-27 Nov 2025"],
  [fact("VINBAX 2025, sixth edition, Indian Army and Vietnam People's Army, Mieu Mon Training Centre, Hanoi, 11-27 "
        "November 2025; UN peacekeeping focus; over 300 personnel", "nat_vinbax_trib")],
  why="The source names the Vietnam People's Army as the partner and Hanoi as the venue.",
  current=ca("2025-11-11"))

G(T, DEF, "Intermediate",
  "SLINEX-26, the 13th edition of a bilateral maritime exercise held at Visakhapatnam from 17 to 21 September 2026 "
  "under the Eastern Naval Command, saw INS Kavaratti and INS Jyoti operate with SLNS Sindurala. With which country's "
  "navy was it held?",
  ["Sri Lanka", "Singapore", "Bangladesh", "Maldives"], "*",
  "Exercise SLINEX",
  "SLINEX is the India-Sri Lanka bilateral maritime exercise. Its 13th edition, SLINEX-26, was held at Visakhapatnam "
  "from 17 to 21 September 2026 under the Eastern Naval Command. The Indian Navy fielded the anti-submarine warfare "
  "corvette INS Kavaratti and the fleet tanker INS Jyoti; the Sri Lanka Navy sent SLNS Sindurala.",
  ["SLINEX: India-Sri Lanka", "13th edition: Visakhapatnam, 17-21 Sep 2026", "Ships: Kavaratti, Jyoti; SLNS Sindurala"],
  [fact("SLINEX-26, 13th edition of India-Sri Lanka maritime exercise, Visakhapatnam, 17-21 September 2026; INS "
        "Kavaratti, INS Jyoti and SLNS Sindurala; Eastern Naval Command", "nat_slinex_gkt")],
  why="'SLNS' marks a Sri Lanka Navy ship and the source names Sri Lanka as the partner.",
  current=ca("2026-09-17"))

G(T, DEF, "Intermediate",
  "Veer Guardian 2026, a 14-day bilateral air exercise at Air Force Station Jodhpur in September 2026, in which the "
  "IAF's Tejas, Su-30MKI and Rafale jets flew with F-2A fighters, was conducted with the air force of which country?",
  ["Japan", "South Korea", "Australia", "Philippines"], "*",
  "Exercise Veer Guardian",
  "Veer Guardian is the bilateral air exercise between the Indian Air Force and the Japan Air Self-Defence Force. The "
  "2026 edition was a 14-day exercise at Air Force Station Jodhpur in September 2026. The IAF fielded Tejas, Su-30MKI "
  "and Rafale; Japan flew F-2A fighters.",
  ["Veer Guardian: IAF + Japan Air Self-Defence Force", "2026: AFS Jodhpur, Sep 2026", "Japan's jets: F-2A"],
  [fact("Veer Guardian 2026, IAF and Japan Air Self-Defence Force, 14-day exercise at Air Force Station Jodhpur; IAF "
        "Tejas, Su-30MKI and Rafale, Japan F-2A; article dated 20 September 2026", "nat_veer_air")],
  why="The source names the Japan Air Self-Defence Force and its F-2A fighters; the other air forces did not take part.",
  current=ca("2026-09-20", inferred="source article dated 20 Sep 2026 describes the ongoing exercise; start date not "
                                    "stated"))

G(T, DEF, "Intermediate",
  "During Exercise Udara Shakti 2026, which culminated in August 2026, the IAF's Rafale fighters operated alongside "
  "Su-30MKM and F/A-18 aircraft from which air base?",
  ["Subang Airbase, Malaysia", "Paya Lebar Air Base, Singapore", "Clark Air Base, Philippines",
   "Korat Air Base, Thailand"], "*",
  "Exercise Udara Shakti (India-Malaysia)",
  "Udara Shakti is the air exercise between the Indian Air Force and the Royal Malaysian Air Force. In the 2026 edition, "
  "reported culminating on 14 August 2026, IAF Rafales, supported by C-17 Globemaster III and IL-78 tankers, operated "
  "from Subang Airbase, Malaysia, with RMAF Su-30MKM and F/A-18 aircraft.",
  ["Udara Shakti: IAF + Royal Malaysian Air Force", "2026 venue: Subang Airbase", "IAF: Rafale; RMAF: Su-30MKM, F/A-18"],
  [fact("Udara Shakti 2026 at Subang Airbase, Malaysia; IAF Rafale with C-17 and IL-78 support; RMAF Su-30MKM and "
        "F/A-18; reported culminating on 14 August 2026", "nat_udara_ians")],
  why="The source names Subang Airbase in Malaysia as the venue; the other bases were not used.",
  current=ca("2026-08-14"))

G(T, DEF, "Intermediate",
  "On 31 December 2025 DRDO carried out a salvo launch of two missiles in quick succession from the same launcher off "
  "the Odisha coast as part of user evaluation trials. Which missile was tested?",
  ["Pralay", "Agni-Prime", "Nirbhay", "Shaurya"], "*",
  "Pralay quasi-ballistic missile",
  "Pralay is an indigenously developed, solid-propellant quasi-ballistic missile designed by the Research Centre Imarat "
  "(RCI), Hyderabad, with other DRDO labs. On 31 December 2025 two Pralay missiles were fired in a salvo from the same "
  "launcher; both followed the intended trajectory, tracked by the Integrated Test Range, Chandipur. Bharat Dynamics "
  "and Bharat Electronics are the development-cum-production partners.",
  ["31 Dec 2025: Pralay salvo (2 missiles, one launcher)", "Type: solid-propellant quasi-ballistic", "Lead lab: RCI"],
  [fact("Salvo launch of two Pralay missiles from the same launcher on 31 December 2025 off Odisha as user evaluation "
        "trials; quasi-ballistic, solid propellant; designed by RCI Hyderabad; BDL and BEL partners", "nat_pralay_etv")],
  why="The source names Pralay as the missile fired in the 31 December 2025 salvo test.",
  current=ca("2025-12-31"))

G(T, ST, "Intermediate",
  "The Jai Prakash Narayan Bird Sanctuary (Surha Tal), whose designation as India's 100th Ramsar site was welcomed by "
  "the Prime Minister on World Environment Day 2026, is located in which district of Uttar Pradesh?",
  ["Ballia", "Aligarh", "Etah", "Mainpuri"], "*",
  "Ramsar sites in India",
  "Surha Tal, an oxbow lake of the Ganga in Ballia district, became India's 100th Ramsar site and Uttar Pradesh's 13th; "
  "the Prime Minister welcomed it on 5 June 2026. The 99th site, designated in April 2026, was Shekha Jheel Bird "
  "Sanctuary in Aligarh, and Patna Bird Sanctuary in Etah district was also added earlier in 2026.",
  ["100th Ramsar site: Surha Tal, Ballia (UP's 13th)", "99th: Shekha Jheel, Aligarh"],
  [fact("Jai Prakash Narayan Bird Sanctuary (Surha Tal), Ballia district, UP, India's 100th Ramsar site and UP's 13th; "
        "PM welcomed it on World Environment Day, 5 June 2026; Patna Bird Sanctuary (Etah) added earlier in 2026",
        "nat_surha_dr"),
   fact("Shekha Jheel Bird Sanctuary, Aligarh, India's 99th Ramsar site, April 2026", "nat_shekha_dr")],
  why="Aligarh has Shekha Jheel (99th site) and Etah has Patna Bird Sanctuary; Surha Tal is in Ballia.",
  current=ca("2026-06-05", inferred="source gives the PM's welcome on 5 Jun 2026; designation day not stated"))

GS(T, ST, "Intermediate", "the Ramsar sites designated in October 2026",
   ["With the addition of Sukhna Wetland and Sauj Jheel, India's count of Ramsar sites reached 105.",
    "Sukhna Wetland became the first Ramsar site of the Union Territory of Chandigarh."],
   [False, True],
   "Ramsar sites in India",
   "Union Environment Minister Bhupender Yadav announced the designation of Sukhna Wetland (Chandigarh) and Sauj Jheel "
   "(Mainpuri, Uttar Pradesh), taking India's tally to 103 on 15 October 2026. Sukhna is Chandigarh's first Ramsar site; "
   "Mainpuri now has two (Sauj Jheel and Saman Bird Sanctuary).",
   [fact("Sukhna Wetland (Chandigarh, its first Ramsar site) and Sauj Jheel (Mainpuri, UP) designated; India's count "
         "reached 103 on 15 October 2026; announced by Bhupender Yadav", "nat_sukhna_gkt")],
   why="Statement 1 is wrong: the count reached 103, not 105.",
   current=ca("2026-10-15"))

GS(T, ST, "Intermediate", "the Hate Speech and Hate Crimes (Prevention) Bill passed by the Karnataka Legislative "
   "Assembly",
   ["It was introduced in the Assembly by Chief Minister Siddaramaiah.",
    "It was passed during the Assembly session held in Bengaluru in December 2025."],
   [False, False],
   "State legislation: Karnataka hate speech bill",
   "The Karnataka Assembly passed the Hate Speech and Hate Crimes (Prevention) Bill in Belagavi on 18 December 2025, "
   "amid BJP protests; it was described as India's first anti-hate speech law. The state cabinet cleared it on 4 "
   "December and Home Minister G. Parameshwara introduced it on 10 December 2025.",
   [fact("Karnataka Assembly passed the Hate Speech and Hate Crimes (Prevention) Bill on 18 December 2025 in Belagavi; "
         "introduced by Home Minister G. Parameshwara on 10 December; cabinet cleared it on 4 December", "nat_hate_tt")],
   why="Both are wrong: Home Minister G. Parameshwara introduced the Bill, and it was passed in Belagavi, not "
       "Bengaluru.",
   current=ca("2025-12-18"))

GS(T, GOV, "Intermediate", "the railway multitracking projects approved by the Union Cabinet on 9 September 2026",
   ["The approved projects include a fourth line between Kharagpur and Jharsuguda.",
    "The approved projects include the doubling of the Hosur-Omalur line."],
   [True, True],
   "Cabinet decisions: railway multitracking",
   "On 9 September 2026 the Union Cabinet approved eight railway multitracking projects worth over ₹20,800 crore. Three "
   "(about ₹10,783 crore, about 656 km, 14 districts in West Bengal, Jharkhand, Odisha, Madhya Pradesh and "
   "Chhattisgarh) include the Kharagpur-Jharsuguda fourth line, the Katni-Pendra Road fourth line and the Bilaspur-"
   "Pendra Road third line. Five (about ₹10,021 crore, about 540 km, 17 districts in Tamil Nadu, Andhra Pradesh, "
   "Karnataka and Telangana) include Arakkonam-Renigunta and Whitefield-Bangarapet third and fourth lines and the "
   "doubling of Hosur-Omalur.",
   [fact("Cabinet (meeting reported on 10 Sep 2026 as 'yesterday') approved 8 multitracking projects over ₹20,800 crore: "
         "Kharagpur-Jharsuguda 4th line, Katni-Pendra Road 4th line, Bilaspur-Pendra Road 3rd line, Arakkonam-"
         "Renigunta and Whitefield-Bangarapet 3rd/4th lines, Hosur-Omalur doubling", "nat_rail_sep_air")],
   why="Both projects are named in the source among the eight approved.",
   current=ca("2026-09-09"))

G(T, GOV, "Intermediate",
  "On 6 May 2026 the Union Cabinet approved three railway multitracking projects worth ₹23,437 crore, adding about "
  "901 km across six states. Which of the following was one of them?",
  ["Nagda-Mathura", "Kharagpur-Jharsuguda", "Whitefield-Bangarapet", "Katni-Pendra Road"], "*",
  "Cabinet decisions: railway multitracking",
  "The three projects approved on 6 May 2026, worth ₹23,437 crore and covering about 901 km, are third and fourth "
  "lines on Nagda-Mathura, Guntakal-Wadi and Burhwal-Sitapur, across Uttar Pradesh, Rajasthan, Madhya Pradesh, "
  "Karnataka, Andhra Pradesh and Telangana. Kharagpur-Jharsuguda, Whitefield-Bangarapet and Katni-Pendra Road were "
  "among the projects approved later, on 9 September 2026.",
  ["6 May 2026: ₹23,437 crore, ~901 km, 6 states", "Projects: Nagda-Mathura, Guntakal-Wadi, Burhwal-Sitapur"],
  [fact("6 May 2026: Cabinet approved ₹23,437 crore for third/fourth lines on Nagda-Mathura, Guntakal-Wadi and "
        "Burhwal-Sitapur; about 901 km; UP, Rajasthan, MP, Karnataka, AP, Telangana", "nat_rail_may_ins"),
   fact("Three projects Nagda-Mathura, Guntakal-Wadi, Burhwal-Sitapur, ₹23,437 crore, about 901 km, 19 districts",
        "nat_rail_may_ao"),
   fact("Kharagpur-Jharsuguda, Katni-Pendra Road and Whitefield-Bangarapet lines were in the September 2026 approvals",
        "nat_rail_sep_air")],
  why="Kharagpur-Jharsuguda, Whitefield-Bangarapet and Katni-Pendra Road were approved on 9 September 2026, not in May.",
  current=ca("2026-05-06"))

G(T, GOV, "Intermediate",
  "The 117.7 km four-lane access-controlled greenfield Kanpur-Kabrai highway, approved by the Cabinet Committee on "
  "Economic Affairs on 1 July 2026 at a cost of about ₹7,145 crore, is a key segment of which corridor?",
  ["Bhopal-Kanpur Economic Corridor", "Delhi-Mumbai Expressway", "Amritsar-Kolkata Industrial Corridor",
   "Raipur-Visakhapatnam Economic Corridor"], "*",
  "Cabinet decisions: highways",
  "The CCEA approved the Kanpur-Kabrai highway on 1 July 2026: 117.7 km, four-lane access-controlled greenfield "
  "(structures built for future six-laning), ₹7,145.14 crore, to be built by NHAI on BOT (Toll) mode, including O&M "
  "of the existing Kanpur-Kabrai section of NH-34. It is a key segment of the Bhopal-Kanpur Economic Corridor and links "
  "NH-35, the Bundelkhand Expressway and the Kanpur Ring Road.",
  ["Approved 1 Jul 2026 by CCEA", "117.7 km, ₹7,145.14 crore, BOT (Toll), NHAI", "Part of Bhopal-Kanpur Economic Corridor"],
  [fact("Kanpur-Kabrai highway approved 1 July 2026 by CCEA; 117.7 km; ₹7,145.14 crore; BOT (Toll), NHAI; segment of "
        "Bhopal-Kanpur Economic Corridor; links NH-35, Bundelkhand Expressway, Kanpur Ring Road", "nat_kabrai_ians")],
  why="The source names the Bhopal-Kanpur Economic Corridor; the other corridors are not mentioned for this project.",
  current=ca("2026-07-01"))

# ------------------------------------------------------------------ Advanced (2)
GS(T, ST, "Advanced", "the Uniform Civil Code (UCC) Bills passed by State Assemblies in 2026",
   ["The Gujarat Assembly passed the Gujarat Uniform Civil Code, 2026 Bill in March 2026, making Gujarat the second "
    "state after Uttarakhand to adopt such a law.",
    "Assam's UCC Bill, passed in May 2026, applies to Scheduled Tribes as well as other residents of the State.",
    "Madhya Pradesh became the fourth state to pass a UCC Bill when its Assembly passed it in July 2026."],
   [True, False, True],
   "State Uniform Civil Code laws",
   "Gujarat's Assembly passed the Gujarat Uniform Civil Code, 2026 Bill by voice vote on 24 March 2026 after a debate "
   "of over seven hours; Uttarakhand had passed its UCC in February 2024. The Assam Assembly passed its UCC Bill, 2026 "
   "on 27 May 2026, making Assam the third state and the first in the Northeast; Scheduled Tribes are kept outside its "
   "ambit. Madhya Pradesh's Assembly passed its UCC Bill on 21 July 2026, making it the fourth state after "
   "Uttarakhand, Gujarat and Assam.",
   [fact("Gujarat Assembly passed the Gujarat Uniform Civil Code, 2026 Bill (article of 25 Mar 2026: 'yesterday'); second "
         "state after Uttarakhand (Feb 2024); STs exempt", "nat_ucc_guj_air"),
    fact("Assam passed UCC Bill 2026 (article 27 May 2026, 'on Wednesday'); third state, first in Northeast; Scheduled "
         "Tribes completely outside the ambit", "nat_ucc_asm_sent"),
    fact("Assam UCC Bill 2026: Scheduled Tribes exempted; third state after Uttarakhand and Gujarat", "nat_ucc_asm_dr"),
    fact("Madhya Pradesh Assembly passed UCC Bill 2026 (Bhopal, 21 July, 'on Tuesday'); fourth state after Uttarakhand, "
         "Gujarat and Assam", "nat_ucc_mp_uni")],
   why="Statement 2 is wrong: Assam's UCC keeps Scheduled Tribes completely outside its ambit.",
   current=ca("2026-07-21"))

GS(T, GOV, "Advanced", "the additions to India's UNESCO World Heritage Tentative List in 2026",
   ["The five entries shared by the Culture Minister on 29 September 2026, including the Bagh Cave paintings and the "
    "Udaigiri Caves, raised India's Tentative List count to 78.",
    "The Sirpur Cultural and Archaeological Landscape, added in October 2026, is in Chhattisgarh on the eastern bank of "
    "the Mahanadi.",
    "The Baratang Karst-Mud Volcano Complex, added in October 2026, is located in Lakshadweep."],
   [True, True, False],
   "UNESCO Tentative List",
   "On 29 September 2026 Culture and Tourism Minister Gajendra Singh Shekhawat shared five new Tentative List entries "
   "(Bagh Cave paintings, a group of temples, the Udaigiri Caves, the tribal legacy of Ginnorgarh and a serial "
   "India-South Africa 'Sites of Satyagraha' proposal), raising the count to 78. In October 2026 three more were added, "
   "taking it to 81: the Baratang Karst-Mud Volcano Complex and the Andaman Subduction Volcanoes (Narcondam and Barren "
   "Islands), both in the Andaman and Nicobar Islands, and the Sirpur landscape in Mahasamund district, Chhattisgarh.",
   [fact("Five additions shared by Gajendra Singh Shekhawat on 29 September 2026 (Bagh Cave paintings, Udaigiri Caves, "
         "Ginnorgarh, Sites of Satyagraha, a temple group); count rises to 78", "nat_tl_air"),
    fact("October 2026: Baratang Karst-Mud Volcano Complex (Baratang Island, Andaman and Nicobar), Andaman Subduction "
         "Volcanoes, Sirpur (Mahasamund, Chhattisgarh, eastern bank of Mahanadi); total 81", "nat_tl_dr")],
   why="Statement 3 is wrong: Baratang Island is in the Andaman and Nicobar Islands, not Lakshadweep.",
   current=ca("2026-10-23", inferred="source item dated 23 Oct 2026; exact day of the UNESCO listing not stated"))

# ------------------------------------------------------------------ Static Awareness, Basic (3)
TS = "Static Awareness"

G(TS, "Capitals and currencies", "Basic",
  "The đồng, issued by its State Bank, is the currency of which country?",
  ["Vietnam", "Cambodia", "Laos", "Thailand"], "*",
  "Currencies of Asian countries",
  "The Vietnamese đồng (ISO code VND) is issued by the State Bank of Vietnam; the unified đồng has been in use since "
  "3 May 1978, after Vietnam's reunification.",
  ["Vietnam -> đồng (VND)", "Issuer: State Bank of Vietnam"],
  [fact("The Vietnamese đồng (VND) is issued by the State Bank of Vietnam; in use since 3 May 1978", "nat_dong_wiki")],
  why="The source identifies the đồng as Vietnam's currency; it is not the currency of the other countries.")

G(TS, "National parks and dams", "Basic",
  "Bhitarkanika National Park, known for its saltwater crocodiles and mangroves, is located in which state?",
  ["Odisha", "West Bengal", "Andhra Pradesh", "Tamil Nadu"], "*",
  "National parks of India",
  "Bhitarkanika National Park lies in Kendrapara district of Odisha and was designated a national park on 16 September "
  "1998. The saltwater crocodile is its signature species. It became a Ramsar site on 19 August 2002, Odisha's second "
  "after Chilika Lake. The Brahmani, Baitarani, Dhamra and Pathsala rivers flow through the area.",
  ["Bhitarkanika: Kendrapara, Odisha", "National park: 1998", "Ramsar site: 2002"],
  [fact("Bhitarkanika National Park, Kendrapara district, Odisha; national park from 16 September 1998; saltwater "
        "crocodile; Ramsar site 19 August 2002, Odisha's second after Chilika", "nat_bhitar_wiki")],
  why="The source places Bhitarkanika in Kendrapara district of Odisha, not in the other states.")

G(TS, "Indian states facts", "Basic",
  "On which date did Himachal Pradesh become a full-fledged state of the Indian Union?",
  ["25 January 1971", "1 November 1966", "21 January 1972", "26 January 1950"], "*",
  "Formation of Indian states",
  "Himachal Pradesh attained full statehood on 25 January 1971, becoming the 18th state of the Indian Union, with "
  "Yashwant Singh Parmar as its first Chief Minister.",
  ["Himachal Pradesh: full state on 25 Jan 1971", "18th state; first CM Y. S. Parmar"],
  [fact("Himachal Pradesh attained full statehood on 25 January 1971 as the 18th state; first CM Yashwant Singh Parmar",
        "nat_hp_wiki")],
  why="The source gives 25 January 1971 for Himachal's statehood; the other dates are not its statehood date.")

# ###################################################################### part: intl (international)
# ###################################################################### part: intl
# ---------------------------------------------------------------- International Current Affairs (B8 / I3 / A10)
U.update({
    "intl_murmu_air": ("https://www.newsonair.gov.in/president-droupadi-murmu-embarks-on-historic-state-visit-to-angola-"
                       "and-botswana-to-strengthen-india-africa-ties/", OPENED),
    "intl_murmu_na": ("https://newsarenaindia.com/nation/prez-murmu-holds-delegation-level-talks-with-botswana-"
                      "counterpart/62023", OPENED),
    "intl_swe_trib": ("https://www.tribuneindia.com/news/india/pm-modis-sweden-visit-yields-strategic-partnership-both-"
                      "sides-unveil-tech-roadmap-aim-to-double-trade-in-5-years/", OPENED),
    "intl_ita_too": ("https://timesofoman.com/article/172085-pm-modi-concludes-italy-visit-shares-outcomes-thanks-meloni-"
                     "and-people-for-friendship", OPENED),
    "intl_ita_ians": ("https://ianslive.in/pm-modi-italian-counterpart-giorgia-meloni-hold-talks-in-rome--20260520153911",
                      SEARCH),
    "intl_aus_etv": ("https://www.etvbharat.com/en/international/india-australia-relationship-has-never-been-more-"
                     "consequential-pm-albanese-enn26070404414", OPENED),
    "intl_aus_air": ("https://newsonair.gov.in/pm-modi-expresses-gratitude-to-australia-for-warm-hospitality/", OPENED),
    "intl_aus_na": ("https://newsarenaindia.com/nation/massive-turnout-at-pm-s-address-to-indian-diaspora-in-melbourne/"
                    "81967", SEARCH),
    "intl_swiss_too": ("https://timesofoman.com/article/177648-indian-pm-modi-swiss-president-guy-parmelin-hold-"
                       "bilateral-talks-at-hyderabad-house", OPENED),
    "intl_sey_na": ("https://newsarenaindia.com/nation/seychelles-president-arrives-in-india-on-first-state-visit/69218",
                    OPENED),
    "intl_sey_nation": ("https://nation.sc/articles/29386/state-visit-to-india-strengthens-strategic-partnership",
                        OPENED),
    "intl_sey_euaf": ("https://eu-africa-chamber.org/india-state-visit-of-prime-minister-to-seychelles-june-27-29-2026/",
                      OPENED),
    "intl_sey_tt": ("https://telanganatoday.com/modi-begins-three-day-seychelles-visit-with-ceremonial-welcome", OPENED),
    "intl_sey_ians": ("https://ianslive.in/india-stands-as-a-beacon-of-excellence-for-democracy-seychelles-speaker--"
                      "20260628182856", OPENED),
    "intl_min_aj": ("https://www.aljazeera.com/amp/economy/2026/5/26/india-us-strike-critical-minerals-deal-whats-in-it-"
                    "why-does-it-matter", OPENED),
    "intl_pax_fpj": ("https://www.freepressjournal.in/india/india-joins-us-led-pax-silica-coalition-to-secure-"
                     "semiconductor-supply-chains", OPENED),
    "intl_start_air": ("https://www.newsonair.gov.in/us-and-russia-exit-new-start-treaty-triggering-fears-over-global-"
                       "nuclear-stability/", OPENED),
    "intl_start_print": ("https://theprint.in/world/new-start-nuclear-treaty-expires-removing-key-constraints-on-russia-"
                         "and-us/2846542", OPENED),
    "intl_shut_pbs": ("https://www.pbs.org/newshour/politics/trump-signs-government-funding-bill-ending-record-43-day-"
                      "shutdown", OPENED),
    "intl_taipo_an": ("https://asianews.network/death-toll-of-hong-kong-blaze-rises-to-168-security-chief/", OPENED),
    "intl_taipo_std": ("https://www.thestandard.com.hk/news/article/317893/Tai-Po-fire-death-toll-rises-to-128", OPENED),
    "intl_ire_rte": ("https://www.rte.ie/news/2025/1111/1543242-connolly-inauguration", OPENED),
    "intl_ire_pres": ("https://president.ie/diary/details/inauguration-of-president-catherine-connolly", SEARCH),
    "intl_bol_merco": ("https://en.mercopress.com/2025/11/10/rodrigo-paz-sworn-in-as-bolivia-s-new-president", OPENED),
    "intl_bol_ny1": ("https://ny1.com/nyc/all-boroughs/ap-top-news/2025/11/08/rodrigo-paz-sworn-in-as-bolivias-new-"
                     "president-ending-20-years-of-one-party-rule", SEARCH),
    "intl_gb_aj": ("https://aljazeera.com/news/2025/11/27/guinea-bissau-military-appoints-general-as-transition-"
                   "president-after-coup", OPENED),
    "intl_gui_aj": ("https://www.aljazeera.com/news/2026/1/18/military-leader-doumbouya-sworn-in-as-guineas-president",
                    OPENED),
    "intl_ben_an": ("https://www.africanews.com/amp/2026/05/24/former-finance-minister-romuald-wadagni-sworn-is-as-"
                    "benins-new-president/", OPENED),
    "intl_pope_wiki": ("https://en.wikipedia.org/wiki/2025_visit_by_Pope_Leo_XIV_to_Turkey_and_Lebanon", OPENED),
    "intl_tc_aj": ("https://www.aljazeera.com/news/2025/12/27/thailand-and-cambodia-agree-on-ceasefire-cambodia-defence-"
                   "ministry-says", OPENED),
    "intl_ecl_sw": ("https://starwalk.space/news/total-solar-eclipse-august-12-2026", OPENED),
    "intl_wal_wiki": ("https://en.wikipedia.org/wiki/2026_Senedd_election", OPENED),
    "intl_wal_c4": ("https://www.channel4.com/news/rhun-ap-iorwerth-named-next-first-minister-of-wales-ending-100-years-"
                    "of-labour-rule", SEARCH),
})

T = "International Current Affairs"
BIL, GLB = "Bilateral relations", "Global events"

# ------------------------------------------------------------------ Basic (8)
G(T, BIL, "Basic",
  "At talks held in Gothenburg on 17 May 2026, India elevated its relations with which country to a Strategic "
  "Partnership and adopted a Joint Action Plan for 2026-2030?",
  ["Sweden", "Denmark", "Finland", "Norway"], "*",
  "India-Sweden Strategic Partnership",
  "Prime Minister Modi and Swedish Prime Minister Ulf Kristersson held talks in Gothenburg on 17 May 2026 and raised "
  "ties to a Strategic Partnership, backed by a Joint Action Plan 2026-2030. They also announced Joint Innovation "
  "Partnership 2.0 and an India-Sweden Technology and AI Corridor, and aimed to double trade and investment in five "
  "years (bilateral trade was USD 7.75 billion in 2025).",
  ["Venue: Gothenburg, 17 May 2026", "Partner: Sweden (PM Ulf Kristersson)", "Outcome: Strategic Partnership, Joint "
   "Action Plan 2026-2030"],
  [fact("Modi and Ulf Kristersson held talks in Gothenburg on 17 May 2026; ties elevated to Strategic Partnership; "
        "joint action plan 2026-2030; aim to double trade; trade USD 7.75 billion in 2025", "intl_swe_trib")],
  why="The source names Sweden as the partner at the Gothenburg talks; Denmark, Finland and Norway were not.",
  current=ca("2026-05-17"))

G(T, BIL, "Basic",
  "Prime Minister Narendra Modi visited which Australian city from 8 to 10 July 2026 for the India-Australia Annual "
  "Leaders' Summit with Prime Minister Anthony Albanese?",
  ["Melbourne", "Sydney", "Canberra", "Brisbane"], "*",
  "India-Australia Annual Leaders' Summit 2026",
  "Albanese announced on 4 July 2026 that Modi would visit Melbourne from 8 to 10 July 2026 for the Annual Leaders' "
  "Summit. Melbourne was the second stop of a three-nation tour that began in Indonesia and ended in New Zealand. "
  "India and Australia have a Comprehensive Strategic Partnership.",
  ["Visit: 8-10 Jul 2026", "City: Melbourne", "Tour: Indonesia -> Australia -> New Zealand"],
  [fact("Modi to visit Melbourne from 8 to 10 July 2026 for the Annual Leaders' Summit; second stop of a three-nation "
        "tour from Indonesia to New Zealand; Comprehensive Strategic Partnership", "intl_aus_etv"),
   fact("Modi thanked Albanese and Australia for hospitality as the visit concluded (10 July 2026)", "intl_aus_air"),
   fact("PM's address to Indian diaspora in Melbourne drew a massive turnout", "intl_aus_na")],
  why="The sources place the 2026 summit visit in Melbourne, not Sydney, Canberra or Brisbane.",
  current=ca("2026-07-08"))

G(T, BIL, "Basic",
  "Patrick Herminie, who arrived in Chennai on 5 February 2026 on his first State visit to India, coinciding with 50 "
  "years of diplomatic ties between the two countries, is the President of which country?",
  ["Seychelles", "Mauritius", "Maldives", "Madagascar"], "*",
  "India-Seychelles relations",
  "Patrick Herminie was sworn in as Seychelles' sixth President in October 2025. His State visit to India (5-10 "
  "February 2026) took him to Chennai, Mumbai and New Delhi and marked 50 years of India-Seychelles diplomatic "
  "relations.",
  ["Visitor: President Patrick Herminie (Seychelles)", "Visit: 5-10 Feb 2026; Chennai, Mumbai, New Delhi",
   "Occasion: 50 years of diplomatic ties"],
  [fact("Herminie arrived in Chennai on his first State visit to India, till 10 February, coinciding with 50 years of "
        "India-Seychelles ties; sworn in as sixth President in October 2025", "intl_sey_na"),
   fact("Herminie's six-day State visit, 5-10 February 2026, covered Chennai, Mumbai and New Delhi", "intl_sey_nation")],
  why="Herminie is President of Seychelles; the other island nations have different heads of state.",
  current=ca("2026-02-05"))

G(T, GLB, "Basic",
  "Catherine Connolly was inaugurated at Dublin Castle on 11 November 2025 as the tenth President of which country?",
  ["Ireland", "Iceland", "Malta", "Austria"], "*",
  "New heads of state 2025-26",
  "Catherine Connolly was inaugurated in St Patrick's Hall, Dublin Castle, as the tenth President of Ireland, "
  "succeeding Michael D Higgins after his 14 years in office. She is the third woman to hold the office.",
  ["Inauguration: 11 Nov 2025, Dublin Castle", "Office: 10th President of Ireland", "Predecessor: Michael D Higgins"],
  [fact("Connolly inaugurated as tenth President at St Patrick's Hall, Dublin Castle; succeeded Michael D Higgins; "
        "third woman president", "intl_ire_rte"),
   fact("Inauguration of President Catherine Connolly at Dublin Castle on 11 November 2025", "intl_ire_pres")],
  why="Dublin Castle is in Ireland; Connolly is Ireland's President, not that of Iceland, Malta or Austria.",
  current=ca("2025-11-11"))

G(T, GLB, "Basic",
  "Rodrigo Paz was sworn in on 8 November 2025 as President of which country, ending about two decades of dominance "
  "by the Movement Towards Socialism (MAS)?",
  ["Bolivia", "Ecuador", "Paraguay", "Peru"], "*",
  "New heads of state 2025-26",
  "Rodrigo Paz, who won Bolivia's runoff of 19 October 2025 with 54.5% of the vote, was sworn in on 8 November 2025 "
  "with Edman Lara as Vice President. He succeeded Luis Arce, ending about 20 years of MAS rule.",
  ["Sworn in: 8 Nov 2025", "Country: Bolivia", "Predecessor: Luis Arce (MAS)"],
  [fact("Rodrigo Paz sworn in as Bolivia's president; VP Edman Lara; succeeded Luis Arce; MAS had about two decades "
        "of dominance; won the 19 October runoff with 54.5%", "intl_bol_merco"),
   fact("Rodrigo Paz sworn in as Bolivia's new president on 8 November 2025, ending 20 years of one-party rule",
        "intl_bol_ny1")],
  why="The MAS is Bolivia's party and Paz succeeded Bolivia's Luis Arce; the other countries had no such change.",
  current=ca("2025-11-08"))

G(T, GLB, "Basic",
  "The fire at Wang Fuk Court, a housing estate in Tai Po, which broke out on 26 November 2025 and killed 168 people, "
  "took place in which city?",
  ["Hong Kong", "Macau", "Taipei", "Singapore"], "*",
  "Tai Po fire 2025",
  "The No. 5-alarm fire at Wang Fuk Court, a Home Ownership Scheme estate in Tai Po, Hong Kong, began on protective "
  "netting outside one block under renovation and spread to other blocks; seven of the eight towers were charred. "
  "Hong Kong's Security Secretary put the final death toll at 168.",
  ["Date: 26 Nov 2025", "Place: Wang Fuk Court, Tai Po, Hong Kong", "Deaths: 168"],
  [fact("Wang Fuk Court, Tai Po: fire on 26 November; death toll 168 announced by Security Secretary Chris Tang; seven "
        "of eight towers charred", "intl_taipo_an"),
   fact("No. 5-alarm fire at Wang Fuk Court, Tai Po, began on protective netting; three arrested for manslaughter",
        "intl_taipo_std")],
  why="Tai Po and Wang Fuk Court are in Hong Kong, not Macau, Taipei or Singapore.",
  current=ca("2025-11-26"))

G(T, GLB, "Basic",
  "Romuald Wadagni, a former finance minister who won the presidential election of 12 April 2026 with about 94% of "
  "the vote, was sworn in on 24 May 2026 as President of which country?",
  ["Benin", "Togo", "Niger", "Ghana"], "*",
  "New heads of state 2025-26",
  "Romuald Wadagni was sworn in at the Palais des Congrès in Cotonou on 24 May 2026, succeeding Patrice Talon as "
  "President of Benin. Under a constitutional reform, the term is now seven years, with a limit of two terms.",
  ["Sworn in: 24 May 2026, Cotonou", "Country: Benin", "Predecessor: Patrice Talon"],
  [fact("Wadagni sworn in on 24 May 2026 at Palais des Congrès, Cotonou; succeeded Patrice Talon; 94 percent in the "
        "12 April election; seven-year term", "intl_ben_an")],
  why="Cotonou and Patrice Talon belong to Benin; Wadagni is not President of Togo, Niger or Ghana.",
  current=ca("2026-05-24"))

G(T, GLB, "Basic",
  "India became a signatory to the Pax Silica Declaration in New Delhi on 20 February 2026. The US-led Pax Silica "
  "initiative seeks to secure supply chains mainly for which of the following?",
  ["Semiconductors, critical minerals and AI technologies", "Food grains and fertilisers",
   "Vaccines and essential medicines", "Crude oil and liquefied natural gas"], "*",
  "Pax Silica",
  "Pax Silica is a US-led initiative, formed in December 2025, to build secure and resilient supply chains for "
  "semiconductors, critical minerals and AI technologies. India signed the declaration on 20 February 2026 in New "
  "Delhi; Union Minister Ashwini Vaishnaw and US Ambassador Sergio Gor were present.",
  ["Joined: 20 Feb 2026, New Delhi", "Led by: United States", "Focus: chips, critical minerals, AI"],
  [fact("India joined the US-led Pax Silica (formed December 2025) on 20 February 2026 in New Delhi; it covers supply "
        "chains for semiconductors, critical minerals and AI technologies", "intl_pax_fpj")],
  why="The source describes Pax Silica as covering semiconductors, critical minerals and AI, not food, medicines or "
      "hydrocarbons.",
  current=ca("2026-02-20"))

# ------------------------------------------------------------------ Intermediate (3)
G(T, BIL, "Intermediate",
  "Swiss President Guy Parmelin's State visit to India (5-7 October 2026) marked the first anniversary of the entry "
  "into force of which agreement?",
  ["India-EFTA Trade and Economic Partnership Agreement (TEPA)", "India-EU Free Trade Agreement",
   "India-UK Comprehensive Economic and Trade Agreement", "India-Switzerland Double Taxation Avoidance Agreement"], "*",
  "India-EFTA TEPA",
  "TEPA, between India and the four EFTA states (Iceland, Liechtenstein, Norway and Switzerland), was signed on 10 "
  "March 2024 and entered into force on 1 October 2025. Parmelin, on his first State visit to India, held talks with "
  "Prime Minister Modi at Hyderabad House on 5 October 2026 and was to attend the second India-EFTA Prosperity Summit "
  "on 7 October.",
  ["TEPA signed 10 Mar 2024; in force 1 Oct 2025", "Parmelin's State visit: 5-7 Oct 2026",
   "First anniversary of TEPA's entry into force"],
  [fact("Parmelin's State visit marks the first anniversary of TEPA's entry into force; TEPA signed 10 March 2024, in "
        "force 1 October 2025; EFTA = Iceland, Liechtenstein, Norway, Switzerland; talks at Hyderabad House on 5 "
        "October 2026", "intl_swiss_too")],
  why="The source links the visit to TEPA's first anniversary, not to the EU or UK pacts or a tax treaty.",
  current=ca("2026-10-05"))

G(T, BIL, "Intermediate",
  "India and the United States signed a framework on securing supplies of critical minerals and rare earths in New "
  "Delhi on 26 May 2026. Who signed it for the US along with External Affairs Minister S. Jaishankar?",
  ["Secretary of State Marco Rubio", "Treasury Secretary Scott Bessent", "Commerce Secretary Howard Lutnick",
   "Ambassador Sergio Gor"], "*",
  "India-US critical minerals framework",
  "Secretary of State Marco Rubio and EAM S. Jaishankar finalised the India-US framework on critical minerals and "
  "rare earths, covering mining and processing, in New Delhi on 26 May 2026, the last day of Rubio's four-day India "
  "trip, when he also attended the Quad foreign ministers' meeting.",
  ["Date: 26 May 2026, New Delhi", "Signatories: S. Jaishankar and Marco Rubio", "Subject: critical minerals, rare "
   "earths"],
  [fact("Jaishankar and US Secretary of State Marco Rubio finalised a framework agreement on critical minerals and rare "
        "earths in New Delhi on 26 May 2026", "intl_min_aj")],
  why="The source names Marco Rubio as the US signatory; the other officials are not named as signatories.",
  current=ca("2026-05-26"))

G(T, GLB, "Intermediate",
  "Mamady Doumbouya, who seized power in Guinea in 2021, was sworn in as elected President on 17 January 2026. Under "
  "the constitution approved in the September 2025 referendum, how long is a presidential term?",
  ["Seven years", "Five years", "Six years", "Four years"], "*",
  "Guinea's return to elected rule",
  "Doumbouya, who toppled Alpha Condé in 2021, won the December 2025 election with 86.7% of the vote as validated by "
  "the Supreme Court, and was sworn in at the General Lansana Conte Stadium near Conakry on 17 January 2026. The new "
  "constitution lengthened the presidential term from five to seven years, with a two-term limit, and allowed "
  "military leaders to stand.",
  ["Sworn in: 17 Jan 2026, Conakry", "Vote share: 86.7%", "Term: 5 -> 7 years, two-term limit"],
  [fact("Doumbouya sworn in on 17 January 2026 at General Lansana Conte Stadium; 86.7%; terms extended from five to "
        "seven years with a two-term limit; 2021 coup against Alpha Condé", "intl_gui_aj")],
  why="The source says the term was extended from five to seven years; six and four years are not stated.",
  current=ca("2026-01-17"))

# ------------------------------------------------------------------ Advanced (10)
GS(T, BIL, "Advanced", "President Droupadi Murmu's State visit to Angola and Botswana in November 2025",
   ["It was described as the first-ever State visit by an Indian Head of State to Angola and Botswana.",
    "In Angola she attended the celebrations of the 50th anniversary of Angola's independence on 11 November 2025.",
    "Botswana announced that it would gift twelve cheetahs to India under Project Cheetah."],
   [True, True, False],
   "India-Africa: Angola and Botswana",
   "The visit (8-13 November 2025) was the first-ever State visit by an Indian Head of State to the two countries. In "
   "Angola she held talks with President João Lourenço and attended the 50th independence anniversary on 11 November; "
   "in Gaborone she held talks with President Duma Boko, and Botswana agreed to gift eight cheetahs under Project "
   "Cheetah.",
   [fact("First-ever State visit by an Indian Head of State to Angola and Botswana; 50th anniversary of Angola's "
         "independence; Botswana leg 11-13 November", "intl_murmu_air"),
    fact("Botswana to gift India eight cheetahs; Angola leg 8-11 November with 50th independence anniversary on 11 "
         "November; talks with Duma Boko in Gaborone", "intl_murmu_na")],
   why="Statement 3 is wrong: Botswana's gift was eight cheetahs, not twelve.",
   current=ca("2025-11-08"))

GS(T, BIL, "Advanced", "Prime Minister Modi's visit to Seychelles from 27 to 29 June 2026",
   ["It was his first visit to Seychelles as Prime Minister.",
    "He attended the National Day celebrations marking the 50th anniversary of Seychelles' independence as Guest of "
    "Honour.",
    "He addressed the National Assembly of Seychelles in Victoria."],
   [False, True, True],
   "India-Seychelles relations",
   "Modi visited Seychelles from 27 to 29 June 2026 at President Patrick Herminie's invitation, attended the golden "
   "jubilee National Day celebrations as Guest of Honour and addressed the National Assembly on 28 June. An Indian "
   "defence contingent and two Navy ships joined the celebrations. He had last visited Seychelles in 2015.",
   [fact("State visit 27-29 June 2026; Guest of Honour at Golden Jubilee National Day; address to National Assembly "
         "planned; Modi last visited Seychelles in 2015", "intl_sey_euaf"),
    fact("Modi arrived on 27 June 2026, welcomed by Herminie; Guest of Honour at National Day", "intl_sey_tt"),
    fact("Modi addressed the National Assembly in Victoria on 28 June 2026; Guest of Honour at the 50th anniversary of "
         "independence", "intl_sey_ians")],
   why="Statement 1 is wrong: Modi had visited Seychelles earlier, in 2015.",
   current=ca("2026-06-27"))

GS(T, BIL, "Advanced", "Prime Minister Modi's visit to Italy in May 2026",
   ["India and Italy elevated their ties to a Special Strategic Partnership.",
    "Italy was the first leg of his five-nation tour.",
    "The two sides set a target of raising bilateral trade to €20 billion by 2029."],
   [True, False, True],
   "India-Italy relations",
   "Italy was the final leg of a tour that also covered the UAE, the Netherlands, Sweden and Norway. After talks with "
   "Prime Minister Giorgia Meloni in Rome on 20 May 2026, ties were raised to a Special Strategic Partnership, a trade "
   "target of €20 billion by 2029 was set and MoUs were signed in areas such as defence, critical technologies and "
   "mobility.",
   [fact("Italy was the last leg of the five-nation tour after the UAE, Netherlands, Sweden and Norway; ties elevated to "
         "Special Strategic Partnership; bilateral trade target €20 billion by 2029", "intl_ita_too"),
    fact("Modi and Meloni held talks in Rome on 20 May 2026", "intl_ita_ians")],
   why="Statement 2 is wrong: Italy was the final leg of the tour, after the UAE, the Netherlands, Sweden and Norway.",
   current=ca("2026-05-20"))

GS(T, GLB, "Advanced", "the coup in Guinea-Bissau in November 2025",
   ["Army officers announced the takeover on 26 November 2025, before the results of the presidential election were "
    "declared.",
    "The military named General Horta Inta-A (also spelt N'Tam) to lead a three-year transition.",
    "Umaro Sissoco Embalo was the President removed in the coup."],
   [True, False, True],
   "Coups and transitions in West Africa",
   "On 26 November 2025, with rivals Umaro Sissoco Embalo and Fernando Dias both claiming victory and provisional "
   "results due the next day, army officers seized power. General Horta Inta-A (N'Tam), earlier the army chief of "
   "staff, was installed on 27 November for a one-year transition. The African Union condemned the coup.",
   [fact("Coup announced 26 November 2025 before provisional results; Gen Horta Inta-A (N'Tam) named; one-year "
         "transition; Embalo deposed; AU condemned it", "intl_gb_aj")],
   why="Statement 2 is wrong: the transition announced was for one year, not three.",
   current=ca("2025-11-26"))

GS(T, GLB, "Advanced", "the New START treaty, which lapsed in February 2026",
   ["It capped each side at 1,550 deployed strategic nuclear warheads.",
    "It was signed in 2015 and entered into force in 2016.",
    "UN Secretary-General António Guterres called its lapse a 'grave moment for international peace and security'."],
   [True, False, True],
   "Arms control",
   "New START, between the United States and Russia, was signed in 2010 and entered into force on 5 February 2011 for "
   "ten years; it was later extended to 5 February 2026. It limited each side to 1,550 strategic warheads. On its "
   "lapse, Guterres said the two countries' strategic arsenals had no binding limits for the first time in over half a "
   "century.",
   [fact("New START signed 2010, in force 5 February 2011, extended to 5 February 2026; Guterres: 'grave moment for "
         "international peace and security'", "intl_start_air"),
    fact("New START capped 1,550 strategic warheads; lapsed on Thursday 5 February 2026", "intl_start_print")],
   why="Statement 2 is wrong: the treaty was signed in 2010 and entered into force in 2011.",
   current=ca("2026-02-05"))

GS(T, GLB, "Advanced", "the end of the US federal government shutdown in November 2025",
   ["The House of Representatives passed the funding bill unanimously.",
    "The shutdown lasted 43 days, a record.",
    "The bill extended funding for most of the government through 30 January."],
   [False, True, True],
   "US government shutdown 2025",
   "President Trump signed the funding bill on the night of 12 November 2025, ending a record 43-day shutdown. The "
   "House passed it by 222-209, largely on party lines. It funded three annual spending bills, extended other funding "
   "through 30 January and reversed shutdown-era firings.",
   [fact("Trump signed the bill on 12 November 2025 ending a record 43-day shutdown; House vote 222-209; funding "
         "extended through 30 January; reversal of firings", "intl_shut_pbs")],
   why="Statement 1 is wrong: the House vote was 222-209, largely along party lines.",
   current=ca("2025-11-12"))

GS(T, GLB, "Advanced", "Pope Leo XIV's apostolic journey of November-December 2025",
   ["It was his first trip abroad since his election in May 2025.",
    "In İznik, Türkiye, he joined Ecumenical Patriarch Bartholomew I to mark the 1,700th anniversary of the First "
    "Council of Nicaea.",
    "In Lebanon he prayed at the Port of Beirut for the victims of the 2020 explosion."],
   [True, True, True],
   "Pope Leo XIV's first foreign trip",
   "Pope Leo XIV visited Türkiye (27-30 November 2025) and Lebanon (30 November-2 December 2025). He prayed with "
   "Bartholomew I at İznik on 28 November for the Nicaea anniversary and signed a joint declaration with him on 29 "
   "November. In Lebanon he prayed at Saint Charbel's tomb and, on 2 December, held a silent prayer at the Port of "
   "Beirut.",
   [fact("First trip abroad since his May 2025 election; Türkiye 27-30 Nov, Lebanon 30 Nov-2 Dec 2025; İznik prayer "
         "with Bartholomew I on 28 Nov for the 1,700th anniversary of Nicaea; silent prayer at Port of Beirut on 2 Dec",
         "intl_pope_wiki")],
   why="All three statements match the source.",
   current=ca("2025-11-27"))

GS(T, GLB, "Advanced", "the Thailand-Cambodia ceasefire agreement of 27 December 2025",
   ["It was signed by the defence ministers of the two countries.",
    "Thailand agreed to return 18 Cambodian soldiers after the ceasefire had held for 72 hours.",
    "An ASEAN observer team was to monitor its implementation."],
   [True, True, True],
   "Thailand-Cambodia border conflict",
   "Thai Defence Minister Natthaphon Narkphanit and Cambodian Defence Minister Tea Seiha signed the ceasefire, which "
   "took effect at noon on 27 December 2025 after about 20 days of fighting that killed more than 100 people. Troops "
   "were to hold positions, Thailand was to return 18 soldiers after 72 hours of ceasefire, and ASEAN observers were "
   "to monitor it. An earlier truce had been signed in Kuala Lumpur in October 2025.",
   [fact("Ceasefire signed 27 December 2025 by defence ministers Natthaphon Narkphanit and Tea Seiha; 18 soldiers "
         "returned after 72 hours; ASEAN observer team; earlier Kuala Lumpur truce in October 2025", "intl_tc_aj")],
   why="All three statements match the source.",
   current=ca("2025-12-27"))

GS(T, GLB, "Advanced", "the total solar eclipse of 12 August 2026",
   ["It was the first total solar eclipse visible from mainland Europe since 1999.",
    "Its path of totality crossed Greenland, Iceland and Spain.",
    "In Spain, totality occurred around midday, with the Sun high in the sky."],
   [True, True, False],
   "Total solar eclipse 2026",
   "The eclipse of 12 August 2026 was the first total solar eclipse visible from mainland Europe since 1999. Its "
   "totality path crossed Greenland, Iceland and Spain (including the Balearic Islands), touching a small part of "
   "Portugal. In Spain totality came in the evening, around 8:26-8:31 p.m. CEST, with the Sun low in the west.",
   [fact("12 August 2026 eclipse: first total eclipse from mainland Europe since 1999; path over Greenland, Iceland and "
         "Spain; totality in Spain around 8:26-8:31 p.m. CEST, Sun 2-11 degrees above the horizon", "intl_ecl_sw")],
   why="Statement 3 is wrong: in Spain totality came in the evening, just before sunset.",
   current=ca("2026-08-12"))

GS(T, GLB, "Advanced", "the Senedd (Welsh Parliament) election of 7 May 2026",
   ["The Senedd continued to have 60 members.",
    "Plaid Cymru won the most seats, 43.",
    "Labour lost its position as the largest party for the first time since devolution began in 1999."],
   [False, True, True],
   "Senedd election 2026",
   "The 2026 Senedd election, held by closed-list proportional representation, filled an enlarged chamber of 96 "
   "members (up from 60). Plaid Cymru won 43 seats, Reform UK 34 and Labour 9; Labour lost government and its "
   "largest-party status for the first time since 1999. Plaid Cymru leader Rhun ap Iorwerth became First Minister.",
   [fact("Election 7 May 2026; Senedd enlarged to 96 from 60; Plaid Cymru 43, Reform UK 34, Labour 9; Labour lost "
         "largest-party status for first time since 1999; Rhun ap Iorwerth First Minister", "intl_wal_wiki"),
    fact("Rhun ap Iorwerth named next First Minister of Wales, ending a century of Labour dominance", "intl_wal_c4")],
   why="Statement 1 is wrong: the Senedd was enlarged from 60 to 96 members for this election.",
   current=ca("2026-05-07"))

# ###################################################################### part: appt (appointments + organizations)
# ###################################################################### part: appt
# ---------------------------------------------------------------- Important Appointments (B2 / I11 / A2)
# ---------------------------------------------------------------- National and International Organizations (B2 / I5 / A2)
U.update({
    "appt_cbic_ob": ("https://www.outlookbusiness.com/economy-and-policy/vivek-chaturvedi-appointed-cbic-chairman", OPENED),
    "appt_cbic_dr": ("https://www.drishtiias.com/state-pcs-current-affairs/vivek-chaturvedi-appointed-as-cbic-chief/"
                     "print_manually", OPENED),
    "appt_bdf": ("https://www.banque-france.fr/en/node/1799034", OPENED),
    "appt_bdf_bw": ("https://www.bworldonline.com/world/2026/02/10/729514/french-central-bank-chief-villeroy-to-leave-"
                    "early-macron-to-pick-successor/", SEARCH),
    "appt_opcw_25": ("https://www.opcw.org/media-centre/news/2025/11/sabrina-dallafior-appointed-next-opcw-director-general",
                     OPENED),
    "appt_opcw_26": ("https://www.opcw.org/media-centre/news/2026/07/sabrina-dallafior-begins-term-new-director-general-"
                     "opcw", OPENED),
    "appt_opcw_si": ("https://www.swissinfo.ch/eng/foreign-affairs/swiss-becomes-first-woman-to-head-chemical-weapons-body/"
                     "90921304", OPENED),
    "appt_al_es": ("https://egyptianstreets.com/2026/03/29/nabil-fahmy-named-next-secretary-general-of-the-arab-league/",
                   OPENED),
    "appt_al_tn": ("https://www.thenationalnews.com/news/mena/2026/06/23/nabil-fahmy-appointed-arab-league-chief-amid-"
                   "regional-distrust/", OPENED),
    "appt_adb_ws": ("https://www.adb.org/news/adb-appoints-wempi-saputra-vice-president-sectors-and-themes", OPENED),
    "appt_adb_hk": ("https://www.adb.org/news/adb-appoints-hae-kyong-hk-yu-vice-president-administration-and-corporate-"
                    "management", OPENED),
    "appt_wb_p2": ("https://pulse2.com/world-bank-group-names-david-vaillant-as-managing-director-and-cfo/", OPENED),
    "appt_wb_dg": ("https://thedailyguardian.com/business/world-bank-appoints-david-vaillant-as-managing-director-cfo-"
                   "764112/", OPENED),
    "appt_axis_fr": ("https://filingreader.com/news-wire/mumbai/2026-07-07/rbi-approves-n-s-vishwanathan-as-axis-bank-"
                     "chairman", OPENED),
    "appt_sbi_ao": ("https://www.angelone.in/news/stocks/sbi-reappoints-ashwini-kumar-tewari-as-managing-director-till-"
                    "december-2027", OPENED),
    "appt_nab_pc": ("https://www.psuconnect.in/bank-news/canara-bank-announces-appointment-of-shri-rakesh-kashyap-as-"
                    "deputy-managing-director-of-nabard", OPENED),
    "appt_un_press": ("https://press.un.org/en/appointments", OPENED),
    "appt_unrwa_pt": ("https://pt1.petra.gov.jo/en/news/un-appoints-christian-saunders-as-acting-head-of-unrwa", OPENED),
    "appt_unrwa_un": ("https://www.un.org/unispal/document/un-secretary-general-designates-christian-saunders-as-unrwa-"
                      "acting-commissioner-general-from-1-july-2026-until-further-notice/", OPENED),
    "appt_irdai_ao": ("https://www.angelone.in/news/economy/government-announces-fresh-appointments-and-reappointments-"
                      "across-insurance-sector", OPENED),
    "appt_ndb_26": ("https://www.ndb.int/?p=39520", OPENED),
    "appt_ndb_25": ("https://www.ndb.int/news/ndb-board-of-governors-appointed-rajiv-ranjan-as-vice-president/", OPENED),
    # organisations
    "appt_colombo": ("https://colombo-plan.org/", OPENED),
    "appt_isa_air": ("https://www.newsonair.gov.in/us-withdraws-from-over-60-global-organizations-including-several-un-"
                     "bodies-and-international-solar-alliance", OPENED),
    "appt_isa_dr": ("https://www.drishtiias.com/daily-updates/daily-news-analysis/us-exit-from-isa/print_manually", OPENED),
    "appt_arg_aj": ("https://www.aljazeera.com/news/2026/3/17/argentina-officially-withdraws-from-world-health-"
                    "organization-following-us", OPENED),
    "appt_iea_ro": ("https://pubt.io/view/6F9683FFE56A1EFF52672C41A60521C7EBBC074F", OPENED),
    "appt_mne_star": ("https://www.thestar.com.my/news/world/2026/04/23/eu-moves-to-start-drafting-montenegro-accession-"
                      "treaty", OPENED),
    "appt_icj": ("https://www.icj-cij.org/court", OPENED),
    "appt_iucn": ("https://www.iucn.org/about-iucn", OPENED),
    "appt_fsb": ("https://www.fsb.org/about/history-of-the-fsb/", OPENED),
    "appt_hu_bt": ("https://www.brusselstimes.com/2148257/prime-minister-magyar-stops-hungarys-withdrawal-from-the-icc",
                   OPENED),
    "appt_hu_dp": ("https://dailypioneer.com/news/hungarys-parliament-votes-to-remain-member-of-icc", OPENED),
})

T = "Important Appointments"
BFH, IB = "Banking and finance heads", "International bodies"

# ------------------------------------------------------------------ Basic (2)
G(T, BFH, "Basic",
  "In November 2025 the Appointments Committee of the Cabinet approved Vivek Chaturvedi, a 1990-batch IRS officer, as "
  "Chairman of which body under the Department of Revenue?",
  ["Central Board of Indirect Taxes and Customs (CBIC)", "Central Board of Direct Taxes (CBDT)",
   "Goods and Services Tax Network (GSTN)", "Enforcement Directorate (ED)"], "*",
  "Head of the indirect tax board",
  "Vivek Chaturvedi, a 1990-batch officer of the IRS (Customs and Indirect Taxes), was appointed Chairman of the Central "
  "Board of Indirect Taxes and Customs with ACC approval in November 2025, succeeding Sanjay Kumar Agarwal. CBIC, "
  "formerly the Central Board of Excise and Customs, is part of the Department of Revenue, Ministry of Finance.",
  ["Post: Chairman, CBIC", "Appointee: Vivek Chaturvedi (IRS 1990)", "Predecessor: Sanjay Kumar Agarwal"],
  [fact("ACC approved Vivek Chaturvedi, 1990-batch IRS (C&IT), as CBIC Chairman; took charge 28 November 2025; "
        "predecessor Sanjay Kumar Agarwal", "appt_cbic_ob"),
   fact("CBIC, formerly Central Board of Excise & Customs, is part of the Department of Revenue, Ministry of Finance; "
        "Chaturvedi succeeded Sanjay Kumar Agarwal", "appt_cbic_dr")],
  why="The sources name CBIC as the board he heads; CBDT, GSTN and the ED are not the posts reported.",
  current=ca("2025-11-28"))

G(T, IB, "Basic",
  "Emmanuel Moulin, whose appointment was approved by the French Council of Ministers on 27 May 2026, took office on "
  "2 June 2026 as the head of which institution?",
  ["Banque de France", "European Central Bank", "European Investment Bank", "Bank for International Settlements"], "*",
  "Central bank heads",
  "Emmanuel Moulin became Governor of the Banque de France on 2 June 2026 for a six-year term, succeeding François "
  "Villeroy de Galhau, who had announced in February 2026 that he would leave early. Moulin was earlier Secretary "
  "General of the Elysée (from April 2025) and Director General of the Treasury (2020).",
  ["Post: Governor, Banque de France", "Approved: 27 May 2026; took office 2 Jun 2026",
   "Predecessor: François Villeroy de Galhau"],
  [fact("Council of Ministers of 27 May 2026 approved Emmanuel Moulin as Governor of the Banque de France; takes office "
        "2 June 2026; six-year term; Villeroy de Galhau becomes honorary governor", "appt_bdf"),
   fact("Villeroy de Galhau to leave the Banque de France early; Macron to pick successor", "appt_bdf_bw")],
  why="The Banque de France release names Moulin as its Governor; the ECB, EIB and BIS are not the bodies he heads.",
  current=ca("2026-05-27"))

# ------------------------------------------------------------------ Intermediate (11)
G(T, IB, "Intermediate",
  "Swiss diplomat Sabrina Dallafior, elected on 27 November 2025 and the first woman to lead the body, took office in "
  "July 2026 as Director-General of which organisation?",
  ["Organisation for the Prohibition of Chemical Weapons (OPCW)", "International Atomic Energy Agency (IAEA)",
   "Comprehensive Nuclear-Test-Ban Treaty Organization (CTBTO)", "World Intellectual Property Organization (WIPO)"],
  "*",
  "Heads of international organisations",
  "The Conference of the States Parties of the OPCW (30th session) appointed Sabrina Dallafior on 27 November 2025 for "
  "a four-year term. She succeeded Fernando Arias of Spain and became the OPCW's fifth Director-General and its first "
  "woman head. She was earlier Switzerland's Ambassador to Finland. The OPCW is based in The Hague.",
  ["Elected: 27 Nov 2025 (CSP-30)", "Took office: July 2026", "Predecessor: Fernando Arias"],
  [fact("Sabrina Dallafior (Swiss) appointed next OPCW Director-General on 27 November 2025 by CSP-30; four-year term; "
        "succeeds Fernando Arias; OPCW HQ The Hague", "appt_opcw_25"),
   fact("Dallafior assumed office as fifth Director-General, first woman to lead the OPCW; earlier Swiss Ambassador "
        "to Finland", "appt_opcw_26"),
   fact("Swiss diplomat Dallafior first woman to head chemical weapons body", "appt_opcw_si")],
  why="The OPCW releases name her as its Director-General; the IAEA, CTBTO and WIPO are not the bodies reported.",
  current=ca("2025-11-27"))

G(T, IB, "Intermediate",
  "Former Egyptian foreign minister Nabil Fahmy, endorsed by its member states' foreign ministers on 29 March 2026, "
  "was chosen to succeed Ahmed Aboul Gheit as Secretary-General of which body?",
  ["League of Arab States", "Organisation of Islamic Cooperation", "Gulf Cooperation Council", "African Union Commission"],
  "*",
  "Heads of regional organisations",
  "Arab foreign ministers endorsed Egypt's nomination of Nabil Fahmy as Arab League Secretary-General on 29 March 2026 "
  "in a virtual session; the council later confirmed him at a meeting in Amman in June 2026. He was set to take office "
  "on 1 July 2026 for five years, succeeding Ahmed Aboul Gheit, who had held the post since 2016. Fahmy was Egypt's "
  "foreign minister in 2013-14 and its ambassador to the US and Japan. The League is headquartered in Cairo.",
  ["Body: League of Arab States (HQ Cairo)", "Endorsed: 29 Mar 2026", "Predecessor: Ahmed Aboul Gheit"],
  [fact("Arab foreign ministers approved Nabil Fahmy as Arab League Secretary-General on 29 March 2026; to take office "
        "1 July 2026 for five years; succeeds Ahmed Aboul Gheit (since 2016); foreign minister 2013-2014", "appt_al_es"),
   fact("Arab League unanimously appointed Nabil Fahmy at a meeting in Amman; predecessor Aboul Gheit; League HQ "
        "Cairo", "appt_al_tn")],
  why="The sources name the Arab League; the OIC, GCC and AU Commission have different heads.",
  current=ca("2026-03-29"))

G(T, IB, "Intermediate",
  "Wempi Saputra, earlier Indonesia's Assistant Minister for Macroeconomic Policy and International Finance, was "
  "appointed on 16 July 2026 as Vice-President (Sectors and Themes) of which institution?",
  ["Asian Development Bank", "Asian Infrastructure Investment Bank", "World Bank", "New Development Bank"], "*",
  "Multilateral development banks",
  "The Asian Development Bank named Wempi Saputra Vice-President for Sectors and Themes for a three-year term, "
  "succeeding Fatima Yasmin, with an expected start in September 2026. He was earlier the World Bank Group executive "
  "director for the Southeast Asia voting group and Indonesia's G20 Finance Deputy in 2022.",
  ["Post: VP (Sectors and Themes), ADB", "Announced: 16 Jul 2026", "Succeeds: Fatima Yasmin"],
  [fact("ADB appoints Wempi Saputra Vice-President for Sectors and Themes, 16 July 2026, three-year term, succeeding "
        "Fatima Yasmin; earlier World Bank Group executive director, AIIB board member (2021-22) and Indonesian Assistant "
        "Minister", "appt_adb_ws")],
  why="The appointment was announced by the ADB; he had earlier served on the World Bank and AIIB boards, not as "
      "their vice-president.",
  current=ca("2026-07-16"))

G(T, IB, "Intermediate",
  "Hae Kyong (HK) Yu, Australia's ambassador to the Philippines, was appointed by the Asian Development Bank in "
  "December 2025 to which post?",
  ["Vice-President (Administration and Corporate Management)", "Vice-President (Sectors and Themes)",
   "Chief Economist", "Vice-President (Private Sector Operations)"], "*",
  "Multilateral development banks",
  "The ADB announced on 12 December 2025 that HK Yu would become Vice-President (Administration and Corporate "
  "Management) for three years, assuming office on 2 February 2026. She succeeded Bruce Gosper, whose term ended on "
  "31 January 2026.",
  ["Post: VP (Administration and Corporate Management)", "Announced: 12 Dec 2025; from 2 Feb 2026",
   "Predecessor: Bruce Gosper"],
  [fact("ADB appoints HK Yu Vice-President (Administration and Corporate Management), announced 12 December 2025, "
        "three-year term from 2 February 2026; predecessor Bruce Gosper; Australian Ambassador to the Philippines",
        "appt_adb_hk")],
  why="Sectors and Themes went to Wempi Saputra in 2026; the ADB release gives Yu the administration portfolio.",
  current=ca("2025-12-12"))

G(T, IB, "Intermediate",
  "In October 2026 the World Bank Group appointed David Vaillant, who spent about two decades at BNP Paribas, to "
  "which post?",
  ["Managing Director and Chief Financial Officer", "Chief Economist", "Managing Director and Chief Knowledge Officer",
   "Executive Vice-President, IFC"], "*",
  "World Bank Group leadership",
  "The World Bank said on 8 October 2026 that David Vaillant had been appointed Managing Director and Chief Financial "
  "Officer. He oversees financial management, treasury and risk management, and bond issuance by the IBRD, IDA and IFC. "
  "He was earlier Global Head of Finance, Strategy and Participations at BNP Paribas Asset Management.",
  ["Post: MD and CFO, World Bank Group", "Announced: 8 Oct 2026", "Background: BNP Paribas"],
  [fact("World Bank appoints David Vaillant as managing director and chief financial officer (8 October 2026)",
        "appt_wb_dg"),
   fact("Vaillant oversees financial management, treasury, risk and bond issuance for IBRD, IDA, IFC; about two "
        "decades at BNP Paribas", "appt_wb_p2")],
  why="The reports give him the MD and CFO post; the Chief Economist, Chief Knowledge Officer and IFC posts are "
      "held by others.",
  current=ca("2026-10-08"))

G(T, BFH, "Intermediate",
  "In July 2026 the RBI approved the re-appointment of N. S. Vishwanathan, a former RBI Deputy Governor, as "
  "non-executive (part-time) Chairman of which bank, for three years from 27 October 2026?",
  ["Axis Bank", "IndusInd Bank", "Yes Bank", "IDFC First Bank"], "*",
  "Chairmen of private banks",
  "Axis Bank disclosed on 7 July 2026 that the RBI had approved N. S. Vishwanathan's re-appointment as its "
  "non-executive (part-time) Chairman from 27 October 2026 to 26 October 2029, subject to shareholders' approval.",
  ["Bank: Axis Bank", "Term: 27 Oct 2026 - 26 Oct 2029", "Background: former RBI Deputy Governor"],
  [fact("RBI approves re-appointment of N. S. Vishwanathan as non-executive (part-time) chairman of Axis Bank, "
        "27 October 2026 to 26 October 2029; former RBI deputy governor; filing 7 July 2026", "appt_axis_fr")],
  why="The filing is by Axis Bank; the other banks are not named in it.",
  current=ca("2026-07-07", inferred="date of the exchange filing; the RBI letter date is not stated"))

G(T, BFH, "Intermediate",
  "The Appointments Committee of the Cabinet re-appointed Ashwini Kumar Tewari as a Managing Director of State Bank "
  "of India. Till when does the re-appointment run?",
  ["31 December 2027", "30 June 2027", "30 September 2028", "26 January 2029"], "*",
  "SBI Managing Directors",
  "SBI received the ACC's approval in December 2025 for Ashwini Kumar Tewari's re-appointment as Managing Director "
  "from 27 January 2026 to 31 December 2027. He joined SBI in 1991 as a probationary officer, was earlier MD and CEO of "
  "SBI Cards and Payment Services, and oversees corporate banking and subsidiaries.",
  ["Re-appointment: 27 Jan 2026 - 31 Dec 2027", "Approved by: ACC (reported 17 Dec 2025)"],
  [fact("ACC approved re-appointment of Ashwini Kumar Tewari as SBI MD from 27 January 2026 to 31 December 2027; "
        "article dated 17 December 2025; earlier MD & CEO of SBI Card", "appt_sbi_ao")],
  why="The SBI disclosure gives 31 December 2027 as the end date; the other dates are not his term end.",
  current=ca("2025-12-17"))

G(T, BFH, "Intermediate",
  "Rakesh Kashyap, a Chief General Manager of Canara Bank, was appointed by the Central Government with effect from "
  "29 June 2026 to which post?",
  ["Deputy Managing Director, NABARD", "Deputy Managing Director, SIDBI", "Managing Director, National Housing Bank",
   "Deputy Managing Director, Exim Bank"], "*",
  "Development finance institutions",
  "Canara Bank told the exchanges on 29 June 2026 that its CGM Rakesh Kashyap had been appointed Deputy Managing "
  "Director of NABARD under the NABARD Act, 1981, by a Gazette notification of the same date, until his "
  "superannuation on 31 January 2029 or further orders.",
  ["Post: DMD, NABARD", "From: 29 Jun 2026", "Earlier: CGM, Canara Bank"],
  [fact("Central Government appointed Rakesh Kashyap, CGM of Canara Bank, as Deputy Managing Director of NABARD under "
        "the NABARD Act, 1981, effective 29 June 2026, till 31 January 2029", "appt_nab_pc")],
  why="The notification names NABARD; SIDBI, NHB and Exim Bank are not mentioned.",
  current=ca("2026-06-29"))

G(T, IB, "Intermediate",
  "On 12 October 2026 the UN General Assembly approved Isabelle Mercier of Canada for a five-year, non-renewable "
  "term as Under-Secretary-General heading which UN office?",
  ["Office of Internal Oversight Services (OIOS)", "Office for the Coordination of Humanitarian Affairs (OCHA)",
   "Office of Legal Affairs", "Department of Safety and Security"], "*",
  "UN senior appointments",
  "The Secretary-General welcomed the General Assembly's approval of Isabelle Mercier (Canada) as Under-Secretary-"
  "General for Internal Oversight Services on 12 October 2026; the post carries a single five-year term. In the same "
  "month Ramiz Alakbarov of Azerbaijan was named an Assistant Secretary-General in the Department of Safety and "
  "Security.",
  ["Post: USG, Internal Oversight Services", "Approved: 12 Oct 2026", "Term: five years, non-renewable"],
  [fact("12 Oct 2026, SG/A/2445: Isabelle Mercier (Canada), Under-Secretary-General for Internal Oversight Services, "
        "approved by the General Assembly for a five-year non-renewable term; Ramiz Alakbarov ASG, Safety and Security",
        "appt_un_press")],
  why="The UN appointments list gives her OIOS; Safety and Security went to Ramiz Alakbarov as ASG.",
  current=ca("2026-10-12"))

G(T, IB, "Intermediate",
  "On 31 March 2026 the UN Secretary-General designated Christian Saunders to lead which agency, first as acting head "
  "from 1 April and then ad interim from 1 July 2026, after the end of Philippe Lazzarini's term?",
  ["UNRWA (UN Relief and Works Agency for Palestine Refugees)", "UNHCR (UN Refugee Agency)",
   "OCHA (Office for the Coordination of Humanitarian Affairs)", "UNOPS (UN Office for Project Services)"], "*",
  "UN agency heads",
  "Philippe Lazzarini's term as UNRWA Commissioner-General ended in 2026. The UN announced on 31 March 2026 that "
  "Christian Saunders would be Acting Commissioner-General from 1 April to 30 June, and Commissioner-General ad "
  "interim from 1 July 2026 until further notice.",
  ["Agency: UNRWA", "Announced: 31 Mar 2026", "Outgoing: Philippe Lazzarini"],
  [fact("UN appoints Christian Saunders as acting head of UNRWA from 1 April to 30 June, then ad interim from 1 July "
        "until further notice, following end of Lazzarini's term; announced 31 March 2026", "appt_unrwa_pt"),
   fact("UN Secretary-General designates Christian Saunders as UNRWA Acting Commissioner-General from 1 July 2026 "
        "until further notice", "appt_unrwa_un")],
  why="The UN statement names UNRWA; UNHCR, OCHA and UNOPS are not the agencies he was designated to lead.",
  current=ca("2026-03-31"))

G(T, IB, "Intermediate",
  "On 24 September 2026 the UN Secretary-General appointed Toily Kurbanov of the Russian Federation as Deputy Special "
  "Representative of which UN peacekeeping mission, also to serve as the UN Resident and Humanitarian Coordinator in "
  "that country, succeeding Anita Kiki Gbeho of Ghana?",
  ["UN Mission in South Sudan (UNMISS)", "UN Organization Stabilization Mission in the DR Congo (MONUSCO)",
   "UN Interim Force in Lebanon (UNIFIL)", "UN Multidimensional Integrated Stabilization Mission in the Central "
   "African Republic (MINUSCA)"], "*",
  "UN senior appointments",
  "Under SG/A/2440 of 24 September 2026, Toily Kurbanov (Russian Federation) was appointed Deputy Special "
  "Representative for the UN Mission in South Sudan (UNMISS), and also Resident Coordinator and Humanitarian "
  "Coordinator in South Sudan. He succeeds Anita Kiki Gbeho of Ghana.",
  ["Appointee: Toily Kurbanov (Russian Federation)", "Post: Deputy SRSG, UNMISS; RC/HC South Sudan",
   "Date: 24 Sep 2026", "Predecessor: Anita Kiki Gbeho (Ghana)"],
  [fact("24 Sep 2026, SG/A/2440: Toily Kurbanov (Russian Federation) appointed Deputy Special Representative, UN "
        "Mission in South Sudan (UNMISS), also Resident Coordinator and Humanitarian Coordinator in South Sudan; "
        "succeeds Anita Kiki Gbeho of Ghana", "appt_un_press")],
  why="The UN appointments list names UNMISS (South Sudan); the other missions are not mentioned.",
  current=ca("2026-09-24"))

# ------------------------------------------------------------------ Advanced (2)
GS(T, BFH, "Advanced",
   "the appointments to the Insurance Regulatory and Development Authority of India (IRDAI) announced in June 2026",
   ["Girija Subramanian was appointed Whole-Time Member (Actuary).",
    "Girija Subramanian was earlier the Chairman-cum-Managing Director of New India Assurance.",
    "Rajay Kumar Sinha was re-appointed Whole-Time Member (Finance and Investment)."],
   [False, True, True],
   "IRDAI whole-time members",
   "In June 2026 the government named Girija Subramanian, former CMD of New India Assurance, IRDAI Whole-Time Member "
   "(Distribution) for five years; the Actuary post went to Dinesh Pant of LIC. Rajay Kumar Sinha was re-appointed "
   "Whole-Time Member (Finance and Investment) until 2029, and Deepak Sood's term as Member (Non-Life) was extended to "
   "2028.",
   [fact("Girija Subramanian, ex-CMD New India Assurance, Whole-Time Member (Distribution), IRDAI, 5 years; Dinesh Pant "
         "WTM (Actuary); Rajay Kumar Sinha re-appointed WTM (Finance and Investment) until 2029; Deepak Sood extended "
         "to 2028; article 18 June 2026", "appt_irdai_ao")],
   why="Statement 1 is wrong: Subramanian's post is Distribution; the Actuary post went to Dinesh Pant.",
   current=ca("2026-06-18", inferred="article date; the source gives no order date"))

GS(T, IB, "Advanced",
   "the changes in the vice-presidents of the New Development Bank (NDB) announced in July 2026",
   ["India's Rajiv Ranjan, earlier Vice-President and Chief Risk Officer, became Vice-President and Chief "
    "Administrative Officer from 7 July 2026.",
    "Daopeng Fu of China was appointed Vice-President and Chief Risk Officer.",
    "Before joining the NDB, Rajiv Ranjan was an Executive Director of the RBI and a member of its Monetary Policy "
    "Committee."],
   [True, False, True],
   "NDB management",
   "On 8 July 2026 the NDB announced two new vice-presidents and a rotation: Daopeng Fu (China) became Vice-President "
   "and Chief Financial Officer and Monale Ratsoma (South Africa) Vice-President and Chief Risk Officer, while India's "
   "Rajiv Ranjan moved from Chief Risk Officer to Chief Administrative Officer from 7 July 2026. Ranjan had been "
   "appointed NDB Vice-President in August 2025 for five years; he was earlier an RBI Executive Director and MPC member.",
   [fact("NDB, 8 July 2026: Daopeng Fu (China) VP and CFO; Monale Ratsoma (South Africa) VP and CRO; Rajiv Ranjan "
         "(India) VP and Chief Administrative Officer from 7 July 2026, previously CRO", "appt_ndb_26"),
    fact("Rajiv Ranjan appointed NDB Vice-President in August 2025 for five years; earlier RBI Executive Director and "
         "MPC member", "appt_ndb_25")],
   why="Statement 2 is wrong: Daopeng Fu became CFO; the Chief Risk Officer is Monale Ratsoma.",
   current=ca("2026-07-08"))


# ====================================================================== organisations
T = "National and International Organizations"
HH, MEM = "Headquarters and heads", "Membership"

# ------------------------------------------------------------------ Basic (2)
G(T, HH, "Basic",
  "The Colombo Plan, a regional intergovernmental organisation established on 1 July 1951, has its secretariat in "
  "which country?",
  ["Sri Lanka", "Nepal", "Bangladesh", "Thailand"], "*",
  "Regional organisations",
  "The Colombo Plan was established on 1 July 1951 and its secretariat is in Colombo, Sri Lanka. It has 26 member "
  "countries.",
  ["Established: 1 Jul 1951", "Secretariat: Colombo, Sri Lanka", "Members: 26"],
  [fact("The Colombo Plan was established on 1 July 1951; secretariat in Colombo, Sri Lanka; 26 member countries",
        "appt_colombo")],
  why="The Colombo Plan's own site gives a Colombo, Sri Lanka address for its secretariat.")

G(T, MEM, "Basic",
  "In January 2026 the United States announced its withdrawal from 66 international organisations, including an "
  "India-France-led body headquartered in Gurugram. Which body is this?",
  ["International Solar Alliance", "Coalition for Disaster Resilient Infrastructure", "Global Biofuels Alliance",
   "International Big Cat Alliance"], "*",
  "Membership changes",
  "A US presidential memorandum of early January 2026 ordered withdrawal from 66 organisations (31 UN entities and 35 "
  "non-UN bodies), including the International Solar Alliance. The ISA was launched by India and France at COP21 in "
  "Paris in 2015 and is headquartered in Gurugram, Haryana; the US had joined it in 2021.",
  ["US exit: 66 bodies (31 UN, 35 non-UN)", "ISA: launched 2015 by India and France; HQ Gurugram",
   "US had joined ISA in 2021"],
  [fact("US withdraws from 66 global organisations (31 UN, 35 non-UN) including the India-France-led International "
        "Solar Alliance; article 8 January 2026, memorandum signed the previous day", "appt_isa_air"),
   fact("ISA launched in 2015 by India and France at COP21 Paris; HQ Gurugram, Haryana; US joined in 2021",
        "appt_isa_dr")],
  why="The reports name the International Solar Alliance, the Gurugram-based India-France initiative.",
  current=ca("2026-01-07", inferred="article of 8 Jan 2026 says the memorandum was signed the previous day"))

# ------------------------------------------------------------------ Intermediate (5)
G(T, MEM, "Intermediate",
  "On 17 March 2026, one year after notifying its exit, which country's withdrawal from the World Health "
  "Organization took legal effect, following the United States?",
  ["Argentina", "Brazil", "Hungary", "Chile"], "*",
  "Membership changes",
  "Argentina's Foreign Minister Pablo Quirno confirmed that the country's withdrawal from the WHO took effect on "
  "17 March 2026. President Javier Milei had announced the exit in February 2025. The US withdrawal had been "
  "formalised in January 2026. The WHO is headquartered in Geneva.",
  ["Exit effective: 17 Mar 2026", "Announced: Feb 2025 (Milei)", "WHO HQ: Geneva"],
  [fact("Argentina's withdrawal from WHO took effect on 17 March 2026, confirmed by Foreign Minister Pablo Quirno; "
        "follows the US, which formalised its withdrawal in January 2026; WHO HQ Geneva", "appt_arg_aj")],
  why="The report is about Argentina; Brazil, Hungary and Chile are not said to have left the WHO.",
  current=ca("2026-03-17"))

G(T, MEM, "Intermediate",
  "On 2 April 2026 the members of the International Energy Agency unanimously agreed to start the accession process "
  "of which European country?",
  ["Romania", "Bulgaria", "Croatia", "Serbia"], "*",
  "Membership changes",
  "The IEA Governing Board agreed on 2 April 2026 to begin Romania's accession process after Romania formally asked "
  "to join in March 2026. The IEA will check that it meets membership criteria, including oil stockholding, emergency "
  "response and data reporting obligations.",
  ["Decision: 2 Apr 2026", "Country: Romania", "Request: March 2026 letter to Fatih Birol"],
  [fact("IEA Members unanimously agreed on 2 April 2026 to start Romania's accession process; Romania requested in "
        "March 2026", "appt_iea_ro")],
  why="The IEA release concerns Romania only.",
  current=ca("2026-04-02"))

G(T, MEM, "Intermediate",
  "On 22 April 2026 EU member states agreed to start drafting an accession treaty for which candidate country, "
  "which hopes to join the European Union by 2028?",
  ["Montenegro", "Albania", "Serbia", "North Macedonia"], "*",
  "EU enlargement",
  "EU countries agreed on 22 April 2026 to set up a working party to draft Montenegro's accession treaty; "
  "Enlargement Commissioner Marta Kos called it a major step. Montenegro's government aims to join by 2028.",
  ["Decision: 22 Apr 2026", "Country: Montenegro", "Target: 2028"],
  [fact("EU agreed on 22 April 2026 to start drafting an accession treaty for Montenegro; Montenegro hopes to join "
        "by 2028", "appt_mne_star")],
  why="The report concerns Montenegro; the other candidates are not covered by the decision.",
  current=ca("2026-04-22"))

G(T, HH, "Intermediate",
  "The International Union for Conservation of Nature (IUCN), founded in 1948, has its headquarters in which place?",
  ["Gland, Switzerland", "Geneva, Switzerland", "Nairobi, Kenya", "Bonn, Germany"], "*",
  "Headquarters",
  "IUCN, founded in 1948, is headquartered at Rue Mauverney 28, Gland, Switzerland. It describes itself as the "
  "world's largest and most diverse environmental network, with over 1,600 member organisations.",
  ["Founded: 1948", "HQ: Gland, Switzerland"],
  [fact("IUCN headquarters Rue Mauverney 28, 1196 Gland, Switzerland; founded 1948; over 1,600 members", "appt_iucn")],
  why="IUCN's own page gives Gland as its headquarters; the other cities are not its seat.")

G(T, HH, "Intermediate",
  "The Financial Stability Board (FSB) was established in April 2009 as the successor to which body?",
  ["Financial Stability Forum", "Basel Committee on Banking Supervision", "Group of Thirty",
   "Committee on the Global Financial System"], "*",
  "Global financial bodies",
  "The FSB was set up in April 2009 as the successor to the Financial Stability Forum, which the G7 finance ministers "
  "and central bank governors had founded in 1999. G20 leaders endorsed its Charter at the Pittsburgh Summit, and in "
  "January 2013 it became a not-for-profit association under Swiss law with its seat in Basel.",
  ["FSF: founded 1999 by G7", "FSB: April 2009", "Seat: Basel"],
  [fact("FSB established in April 2009 as successor to the Financial Stability Forum (founded 1999 by G7 finance "
        "ministers and central bank governors); Swiss association with seat in Basel from 28 January 2013",
        "appt_fsb")],
  why="The FSB's history page names the Financial Stability Forum as its predecessor.")

# ------------------------------------------------------------------ Advanced (2)
GS(T, MEM, "Advanced",
   "Hungary and the International Criminal Court (ICC)",
   ["Hungary's earlier withdrawal from the ICC had been set to take effect on 2 June 2026.",
    "Prime Minister Péter Magyar's government announced in May 2026 that it would reverse the decision, and Parliament later passed the bill by "
    "133 votes to 37.",
    "Hungary ceased to be a party to the ICC on 2 June 2026."],
   [True, True, False],
   "ICC membership",
   "Viktor Orbán's government notified Hungary's withdrawal from the ICC in June 2025, with effect from 2 June 2026. "
   "On 22 May 2026 Prime Minister Péter Magyar announced the reversal, and Parliament passed the bill with 133 votes "
   "in favour, 37 against and 5 abstentions, halting the exit before it took effect, so Hungary remains a party.",
   [fact("Magyar government reversed Orbán's decision to withdraw from the ICC, announced 22 May 2026; withdrawal "
         "had been due to take effect on 2 June 2026", "appt_hu_bt"),
    fact("Hungary's parliament voted 133-37 (5 abstentions) to remain in the ICC; withdrawal had been set to take "
         "effect June 2", "appt_hu_dp")],
   why="Statement 3 is wrong: the withdrawal was reversed before 2 June 2026, so Hungary stayed in the ICC.",
   current=ca("2026-05-22"))

GS(T, HH, "Advanced",
   "the International Court of Justice (ICJ)",
   ["Its seat is at the Peace Palace in The Hague.",
    "It has fifteen judges, each elected for a nine-year term.",
    "Of the six principal organs of the United Nations, it is the only one not located in New York."],
   [True, True, True],
   "International Court of Justice",
   "The ICJ was created in June 1945 by the UN Charter and began work in April 1946. It sits at the Peace Palace in "
   "The Hague, has fifteen judges elected for nine years by the General Assembly and the Security Council, and is the "
   "only one of the six principal UN organs not located in New York.",
   [fact("ICJ seat at the Peace Palace, The Hague; 15 judges with nine-year terms; only principal UN organ not in New "
         "York; created June 1945, began April 1946", "appt_icj")],
   why="All three statements are stated on the Court's own page.")

# ###################################################################### part: awr (awards + reports)
# ###################################################################### part: awr
# ---------------------------------------------------------------- Awards and Honours (B8 / I2 / A6)
# ---------------------------------------------------------------- Important Reports and Indexes (B5 / I1 / A4)
U.update({
    # awards
    "awr_fields_sf": ("https://www.simonsfoundation.org/2026/07/23/2026-fields-medals-awarded-to-four-of-worlds-top-"
                      "mathematicians/", OPENED),
    "awr_tyler_eu": ("https://www.euronews.com/2026/01/15/weve-neglected-the-power-of-carbon-sucking-fungi-meet-the-"
                     "scientist-determined-to-change-t", OPENED),
    "awr_tyler_am": ("https://appliedmicrobiology.org/resource/2026-tyler-prize-for-environmental-achievement-awarded-"
                     "to-soil-star-dr-toby-kiers.html", SEARCH),
    "awr_uzb_ians": ("https://ianslive.in/uzbekistan-confers-its-highest-honour-oliy-darajali-dostlik-order-on-pm-"
                     "modi--20260830143611", OPENED),
    "awr_gal_air": ("https://www.newsonair.gov.in/president-murmu-approves-gallantry-awards-for-70-armed-forces-"
                    "personnel-on-77th-republic-day-eve", OPENED),
    "awr_gal_bt": ("https://www.businesstoday.in/india/story/republic-day-2026-shubhanshu-shukla-awarded-ashoka-chakra-"
                   "who-is-he-and-why-has-he-been-awarded-512835-2026-01-25", SEARCH),
    "awr_mu_eu": ("https://www.euronews.com/2025/11/21/miss-universe-mexicos-fatima-bosch-who-stood-up-to-organisers-"
                  "crowned-2025-winner", OPENED),
    "awr_mu_nat": ("https://www.thenationalnews.com/lifestyle/2025/11/21/miss-universe-winner-2025-mexico-fatima-bosch",
                   OPENED),
    "awr_bob_mp": ("https://www.millenniumpost.in/business/bank-of-baroda-recognised-as-best-bank-in-india-by-the-"
                   "banker-639203", OPENED),
    "awr_bob_adda": ("https://currentaffairs.adda247.com/bank-of-baroda-recognised-as-best-bank-in-india-by-the-banker-"
                     "key-highlights-and-significance/", OPENED),
    "awr_sbi_fbn": ("https://fintechbiznews.com/lenders-banks/-global-finance-names-sbi-worlds-best-consumer-bank-for-a-"
                    "second-year", OPENED),
    "awr_sbi_gf": ("https://gfmag.com/award/award-winners/state-bank-of-india-worlds-best-consumer-bank-2026/", SEARCH),
    "awr_cba_cb": ("https://www.centralbanking.com/awards/7975431/central-banking-awards-2026-the-winners-in-full",
                   OPENED),
    "awr_cba_aa": ("https://allafrica.com/stories/202603230097.html", OPENED),
    "awr_cba_aa2": ("https://allafrica.com/stories/202603300668.html", OPENED),
    "awr_craf_pr": ("https://www.crafoordprize.se/news/crafoord-prize-laureate-showed-that-many-factors-affect-the-"
                    "climate/", OPENED),
    "awr_brk_news": ("https://breakthroughprize.org/News/98", OPENED),
    "awr_kavli_kf": ("https://kavlifoundation.org/news/the-kavli-prize-2026", OPENED),
    "awr_kavli_nas": ("https://www.nasonline.org/news/nas-members-win-2026-kavli-prizes/", OPENED),
    "awr_sakh_if": ("https://www.ilfoglio.it/en/world/2026/10/22/news/the-sakharov-prize-awarded-to-the-international-"
                    "criminal-court-and-its-judges--411338", OPENED),
    "awr_ig_week": ("https://www.theweek.in/news/world/2026/01/21/who-is-graca-machel-african-icon-wins-indira-gandhi-"
                    "prize-for-peace-disarmament-and-development-for-2025.html", OPENED),
    "awr_bt_best": ("https://www.businesstoday.in/latest/economy/story/bt-best-banks-30-nitin-gadkari-honours-winners-"
                    "icici-bank-named-bank-of-the-year-as-sector-discusses-ai-structural-shifts-518603-2026-02-28",
                    OPENED),
    "awr_goldman_tp": ("https://theprint.in/environment/goldman-prize-women-green-nobel/2920664/", OPENED),
    "awr_wolf_jns": ("https://www.jns.org/wire/wolf-foundation/2026-wolf-prize-laureates-announced", OPENED),
    # reports
    "awr_cri_dte": ("https://www.downtoearth.org.in/climate-change/climate-disasters-have-killed-832000-people-and-cost-"
                    "45-trillion-in-30-years-germanwatch-warns-at-cop30", OPENED),
    "awr_gf_rc": ("https://gfmag.com/award/winner-announcements/press-releases/central-banker-report-cards-2026/",
                  OPENED),
    "awr_wmo_ghg": ("https://wmo.int/media/news/greenhouse-gas-levels-once-again-reach-record-high", OPENED),
    "awr_iq_pr": ("https://www.iqair.com/newsroom/waqr-2025-pr", OPENED),
    "awr_iq_dr": ("https://www.drishtiias.com/state-pcs-current-affairs/world-air-quality-report-2025/print_manually",
                  OPENED),
    "awr_iq_wire": ("https://thewire.in/environment/india-is-sixth-most-polluted-country-loni-in-ghaziabad-is-worlds-"
                    "most-polluted-city-report", OPENED),
    "awr_gfp_list": ("https://www.globalfirepower.com/countries-listing.php", OPENED),
    "awr_sipri_week": ("https://www.theweek.in/news/defence/2026/04/28/india-moves-up-to-no5-in-global-defence-spending-"
                       "china-at-no2-where-is-pakistan-decoding-the-sipri-fact-sheet.html", OPENED),
    "awr_sipri_bt": ("https://www.businesstoday.in/india/story/operation-sindoor-drone-procurement-india-becomes-worlds-"
                     "5th-largest-military-spender-at-921bn-527693-2026-04-28", SEARCH),
    "awr_ilo_est": ("https://www.ilo.org/publications/flagship-reports/employment-and-social-trends-2026", OPENED),
    "awr_wto_gtos": ("https://www.wto.org/english/news_e/news26_e/stat_08oct26_510_e.htm", OPENED),
    "awr_sipri_yb": ("https://www.tribuneindia.com/news/india/india-5th-largest-military-spender-in-world-in-2025-sipri-"
                     "report-mentions-may-conflict-with-pak/", OPENED),
    "awr_api_air": ("https://www.newsonair.gov.in/india-secures-third-rank-in-asia-power-index-2025", OPENED),
    "awr_api_trib": ("https://www.tribuneindia.com/news/india/india-crosses-major-power-threshold-in-asia-power-index-"
                     "2025", OPENED),
    "awr_api_tnm": ("https://www.thenewsminute.com/news/india-ranks-third-in-asia-power-index-2025-just-behind-us-and-"
                    "china", SEARCH),
})

AW = "Awards and Honours"
NAT, INTL = "National awards", "International awards"
RP = "Important Reports and Indexes"
PUB, RANK = "Publishing body", "India's rank"

# ------------------------------------------------------------------ Awards: Basic (8)
G(AW, INTL, "Basic",
  "At the opening ceremony of the International Congress of Mathematicians in Philadelphia on 23 July 2026, which of "
  "the following was awarded a Fields Medal?",
  ["Hong Wang", "Graeme Segal", "Yurii Nesterov", "Hannah Fry"], "*",
  "Fields Medal 2026",
  "The International Mathematical Union announced the four 2026 Fields Medallists at ICM 2026 in Philadelphia on 23 "
  "July 2026: Yu Deng, John Pardon, Jacob Tsimerman and Hong Wang (NYU and IHES; harmonic analysis and geometric "
  "measure theory). It was the first ICM held in the United States since 1986.",
  ["Fields Medals 2026: Yu Deng, John Pardon, Jacob Tsimerman, Hong Wang", "Announced: 23 Jul 2026, ICM Philadelphia"],
  [fact("2026 Fields Medals to Yu Deng, John Pardon, Jacob Tsimerman and Hong Wang, announced 23 July 2026 at the ICM "
        "opening ceremony in Philadelphia; Chern Medal to Graeme Segal, Gauss Prize to Yurii Nesterov, Leelavati Prize "
        "to Hannah Fry", "awr_fields_sf")],
  why="At the same ceremony Graeme Segal received the Chern Medal, Yurii Nesterov the Gauss Prize and Hannah Fry the "
      "Leelavati Prize; none of them received a Fields Medal.",
  current=ca("2026-07-23"))

G(AW, INTL, "Basic",
  "Evolutionary biologist Toby Kiers of Vrije Universiteit Amsterdam, known for mapping the underground networks of "
  "mycorrhizal fungi, won which award in January 2026, carrying a prize of USD 250,000?",
  ["Tyler Prize for Environmental Achievement", "Templeton Prize", "World Food Prize", "Stockholm Water Prize"], "*",
  "Tyler Prize 2026",
  "The 2026 Tyler Prize for Environmental Achievement, often called the 'Nobel' for the environment, went to Toby "
  "Kiers for her work on mycorrhizal fungi, which form networks with plant roots and draw down carbon. It carries USD "
  "250,000.",
  ["Tyler Prize 2026: Toby Kiers", "Work: mycorrhizal fungal networks", "Prize: USD 250,000"],
  [fact("Toby Kiers, evolutionary biologist and professor at Vrije University Amsterdam, named winner of the 2026 Tyler "
        "Prize for Environmental Achievement; prize USD 250,000; work on mycorrhizal fungal networks", "awr_tyler_eu"),
   fact("2026 Tyler Prize for Environmental Achievement awarded to Dr Toby Kiers", "awr_tyler_am")],
  why="The sources name the Tyler Prize; the Templeton, World Food and Stockholm Water prizes are not linked to Kiers "
      "in them.",
  current=ca("2026-01-15", inferred="Euronews report dated 15 Jan 2026; exact announcement day not stated"))

G(AW, INTL, "Basic",
  "Chennai-born climate scientist Veerabhadran Ramanathan, honoured for showing how aerosol particles and other "
  "climate pollutants affect the atmosphere, was announced on 29 January 2026 as the winner of which prize awarded by "
  "the Royal Swedish Academy of Sciences?",
  ["Crafoord Prize", "Kyoto Prize", "Japan Prize", "Shaw Prize"], "*",
  "Crafoord Prize 2026",
  "The Royal Swedish Academy of Sciences, with the Crafoord Foundation, gave the 2026 Crafoord Prize in Geosciences "
  "(SEK 8 million) to Veerabhadran Ramanathan, Emeritus Distinguished Professor at the Scripps Institution of "
  "Oceanography, UC San Diego, born in Chennai in 1944.",
  ["Crafoord Prize 2026 (Geosciences): V. Ramanathan", "Announced 29 Jan 2026; SEK 8 million",
   "Awarded by the Royal Swedish Academy of Sciences"],
  [fact("2026 Crafoord Prize in Geosciences to Veerabhadran Ramanathan (born 1944 in Chennai; Scripps Institution of "
        "Oceanography, UC San Diego) for contributions to understanding aerosol particles and other climate "
        "pollutants; announced 29 January 2026; Royal Swedish Academy of Sciences with the Crafoord Foundation; SEK 8 "
        "million", "awr_craf_pr")],
  why="The source names the Crafoord Prize, chosen by the Royal Swedish Academy of Sciences; the Kyoto, Japan and Shaw "
      "prizes are not linked to Ramanathan in it.",
  current=ca("2026-01-29"))

G(AW, INTL, "Basic",
  "On 30 August 2026 in Tashkent, Prime Minister Narendra Modi was conferred the 'Oliy Darajali Do'stlik' Order by "
  "President Shavkat Mirziyoyev. It is the highest honour of which country?",
  ["Uzbekistan", "Kazakhstan", "Kyrgyzstan", "Tajikistan"], "*",
  "Foreign honours to the Prime Minister",
  "Uzbekistan's highest honour, the 'Oliy Darajali Do'stlik' Order, was conferred on PM Modi by President Shavkat "
  "Mirziyoyev in Tashkent on 30 August 2026, during a two-day state visit, for his contribution to bilateral ties.",
  ["Order: Oliy Darajali Do'stlik", "Country: Uzbekistan (President Mirziyoyev)", "Tashkent, 30 Aug 2026"],
  [fact("Uzbekistan's highest honour, the 'Oliy Darajali Do'stlik' Order, conferred on PM Modi by President Shavkat "
        "Mirziyoyev in Tashkent on 30 August 2026", "awr_uzb_ians")],
  why="The source identifies the order as Uzbekistan's highest honour; the other Central Asian countries are not "
      "involved.",
  current=ca("2026-08-30"))

G(AW, NAT, "Basic",
  "Which gallantry award was approved on 25 January 2026, the eve of the 77th Republic Day, for Group Captain "
  "Shubhanshu Shukla of the Indian Air Force?",
  ["Ashoka Chakra", "Kirti Chakra", "Shaurya Chakra", "Param Vishisht Seva Medal"], "*",
  "Gallantry awards 2026",
  "The President approved 70 gallantry awards on 25 January 2026. Group Captain Shubhanshu Shukla, the first Indian to "
  "visit the International Space Station, received the Ashoka Chakra, India's highest peacetime gallantry award.",
  ["Ashoka Chakra (highest peacetime gallantry award)", "Awardee: Gp Capt Shubhanshu Shukla", "Approved: 25 Jan 2026"],
  [fact("On 25 January 2026 President Murmu approved 70 gallantry awards; Ashoka Chakra to Group Captain Shubhanshu "
        "Shukla, first Indian to visit the ISS; three Kirti Chakras (including Major Arshdeep Singh and Group Captain "
        "Prashanth Balakrishnan Nair); 13 Shaurya Chakras; 30 Param Vishisht Seva Medals among other decorations",
        "awr_gal_air"),
   fact("Shubhanshu Shukla awarded Ashoka Chakra on Republic Day 2026", "awr_gal_bt")],
  why="The three Kirti Chakras went to other officers and the Shaurya Chakras and PVSMs are separate lists; Shukla got "
      "the Ashoka Chakra.",
  current=ca("2026-01-25"))

G(AW, INTL, "Basic",
  "Who was crowned Miss Universe 2025 at the final held in Thailand on 21 November 2025?",
  ["Fátima Bosch (Mexico)", "Praveenar Singh (Thailand)", "Stephany Abasali (Venezuela)", "Olivia Yacé (Côte d'Ivoire)"],
  "*",
  "Miss Universe 2025",
  "Fátima Bosch Fernández of Mexico won the 74th Miss Universe pageant, held in Thailand (reported as Bangkok) on 21 "
  "November 2025. Praveenar Singh of Thailand was first runner-up.",
  ["Miss Universe 2025: Fátima Bosch, Mexico", "First runner-up: Praveenar Singh, Thailand"],
  [fact("Fátima Bosch Fernández of Mexico crowned Miss Universe 2025 on Friday 21 November 2025; first runner-up "
        "Praveenar Singh of Thailand; Stephany Abasali (Venezuela) and Olivia Yacé (Ivory Coast) among the finishers",
        "awr_mu_eu"),
   fact("Fatima Bosch of Mexico won the 74th Miss Universe in Bangkok; Veena Praveenar Singh of Thailand second",
        "awr_mu_nat")],
  why="Praveenar Singh was first runner-up, and Stephany Abasali and Olivia Yacé were other finalists.",
  current=ca("2025-11-21"))

G(AW, INTL, "Basic",
  "At The Banker's 'Bank of the Year Awards 2025', announced in December 2025, which bank was named 'Best Bank in "
  "India'?",
  ["Bank of Baroda", "State Bank of India", "ICICI Bank", "HDFC Bank"], "*",
  "The Banker awards 2025",
  "Bank of Baroda was named 'Best Bank in India' at the Bank of the Year Awards 2025 (Asia-Pacific) of The Banker, a "
  "Financial Times publication. MD and CEO Debadatta Chand welcomed the award.",
  ["Award: Best Bank in India 2025 (The Banker, FT group)", "Winner: Bank of Baroda"],
  [fact("Bank of Baroda named 'Best Bank in India' at the Bank of the Year Awards 2025 by The Banker, a Financial Times "
        "publication; article dated 11 December 2025", "awr_bob_mp"),
   fact("Best Bank in India at The Banker's Bank of the Year Awards 2025 - Asia-Pacific: Bank of Baroda",
        "awr_bob_adda")],
  why="The sources name Bank of Baroda; SBI, ICICI Bank and HDFC Bank did not receive this award.",
  current=ca("2025-12-10", inferred="BoB press release dated 10 Dec 2025 per search; awards day not stated"))

G(AW, INTL, "Basic",
  "Which bank was named 'World's Best Consumer Bank 2026' by Global Finance magazine in October 2026, a title it won "
  "for the second year in a row?",
  ["State Bank of India", "HDFC Bank", "DBS Bank", "Banco Santander"], "*",
  "Global Finance bank awards 2026",
  "Global Finance named State Bank of India the World's Best Consumer Bank 2026 (its second straight win) and also Best "
  "Bank in India 2026. The awards were presented on the sidelines of the IMF Annual Meetings 2026, and SBI Chairman "
  "C. S. Setty received them.",
  ["World's Best Consumer Bank 2026: SBI (second year)", "Also: Best Bank in India 2026"],
  [fact("SBI won Global Finance's World's Best Consumer Bank 2026 (second consecutive win) and Best Bank in India 2026, "
        "presented at the World's Best Bank Awards on the sidelines of the IMF Annual Meeting 2026; received by "
        "Chairman Challa Sreenivasulu Setty", "awr_sbi_fbn"),
   fact("State Bank of India - World's Best Consumer Bank 2026", "awr_sbi_gf")],
  why="The sources give the consumer-bank title to SBI; HDFC Bank, DBS and Santander were not named for it.",
  current=ca("2026-10-17", inferred="report dated 17 Oct 2026; ceremony day not stated"))

# ------------------------------------------------------------------ Awards: Intermediate (2)
G(AW, INTL, "Intermediate",
  "In the Central Banking Awards 2026, at which Jerome Powell was named Governor of the Year, which institution won "
  "'Central Bank of the Year'?",
  ["Central Bank of Nigeria", "Bank of Mexico", "Central Bank of Curaçao and Sint Maarten", "Reserve Bank of India"], "*",
  "Central Banking Awards 2026",
  "The 13th Central Banking Awards (2026) named the Central Bank of Nigeria, under Governor Olayemi Cardoso, Central "
  "Bank of the Year. Jerome Powell was Governor of the Year and Mervyn King received the lifetime achievement award.",
  ["Central Bank of the Year 2026: Central Bank of Nigeria", "Governor of the Year: Jerome Powell",
   "Lifetime achievement: Mervyn King"],
  [fact("Central Banking Awards 2026: lifetime achievement Mervyn King; governor of the year Jerome Powell; central bank "
        "of the year Central Bank of Nigeria; digital transformation Bank of Mexico; currency manager Central Bank of "
        "Curaçao and Sint Maarten", "awr_cba_cb"),
   fact("Central Bank of Nigeria named Central Bank of the Year 2026 (report of 23 March 2026)", "awr_cba_aa"),
   fact("CBN won Central Bank of the Year 2026 at the 13th annual Central Banking Awards; Governor Olayemi Cardoso",
        "awr_cba_aa2")],
  why="Bank of Mexico won the digital transformation award and the Central Bank of Curaçao and Sint Maarten the "
      "currency manager award; no RBI award is listed.",
  current=ca("2026-03-23", inferred="earliest report of the award dated 23 Mar 2026; announcement day not stated"))

G(AW, INTL, "Intermediate",
  "The 2026 Breakthrough Prize in Fundamental Physics (USD 3 million), announced on 18 April 2026, was awarded to "
  "whom?",
  ["Muon g-2 Collaborations at CERN, Brookhaven National Laboratory and Fermilab", "David J. Gross", "Frank Merle",
   "Benjamin R. Safdi"], "*",
  "Breakthrough Prize 2026",
  "The 2026 Breakthrough Prizes were announced on 18 April 2026 at a ceremony in Los Angeles. The Fundamental Physics "
  "prize went to the Muon g-2 collaborations at CERN, Brookhaven and Fermilab for decades of precision measurements of "
  "the muon's anomalous magnetic moment. David J. Gross received a Special Breakthrough Prize, and Frank Merle won the "
  "Mathematics prize.",
  ["Fundamental Physics 2026: Muon g-2 Collaborations (CERN, Brookhaven, Fermilab)",
   "Special prize: David J. Gross; Mathematics: Frank Merle", "Announced 18 Apr 2026; USD 3 million each"],
  [fact("2026 Breakthrough Prizes announced 18 April 2026 (ceremony in Los Angeles): Fundamental Physics to Muon g-2 "
        "Collaborations at CERN, Brookhaven National Laboratory and Fermilab; Special Breakthrough Prize in Fundamental "
        "Physics to David J. Gross; Mathematics to Frank Merle; New Horizons in Physics to Benjamin R. Safdi among "
        "others; USD 3 million per Breakthrough Prize", "awr_brk_news")],
  why="David J. Gross got the Special Breakthrough Prize, Frank Merle the Mathematics prize and Benjamin Safdi a New "
      "Horizons in Physics prize.",
  current=ca("2026-04-18"))

# ------------------------------------------------------------------ Awards: Advanced (6)
GS(AW, INTL, "Advanced", "the Kavli Prizes 2026",
   ["The Nanoscience prize went to Eva Andrei, Pablo Jarillo-Herrero and Allan MacDonald for foundational work that "
    "established the field of twistronics.",
    "The Astrophysics prize was awarded for the discovery of the first planet orbiting a Sun-like star.",
    "The Neuroscience prize recognised the discovery of local protein translation in neurons."],
   [True, False, True],
   "Kavli Prize 2026",
   "The 2026 Kavli Prizes were announced on 10 June 2026 by the Norwegian Academy of Science and Letters; each field "
   "shares USD 1 million. Astrophysics went to Vasily Belokurov, Amina Helmi and Rodrigo Ibata for fossil evidence that "
   "the Milky Way was built through mergers (hierarchical accretion). Neuroscience went to Christine Holt, Kelsey "
   "Martin, Erin Schuman and Oswald Steward.",
   [fact("Kavli Prize 2026 announced 10 June 2026 by the Norwegian Academy of Science and Letters; USD 1 million per "
         "field; Astrophysics: Belokurov, Helmi, Ibata for evidence of past mergers building the Milky Way; "
         "Nanoscience: Andrei, Jarillo-Herrero, MacDonald for twistronics; Neuroscience: Holt, Martin, Schuman, "
         "Steward for local protein translation in neurons", "awr_kavli_kf"),
    fact("Nanoscience and Neuroscience laureates 2026 as above; announced week of 10 June 2026", "awr_kavli_nas")],
   why="Statement 2 is wrong: the astrophysics prize was for showing the Milky Way grew by merging with smaller "
       "galaxies, not for an exoplanet discovery.",
   current=ca("2026-06-10"))

GS(AW, INTL, "Advanced", "the Sakharov Prize for Freedom of Thought 2026",
   ["It was awarded to the International Criminal Court and its judges.",
    "The laureate was chosen by the Conference of Presidents of the political groups of the European Parliament.",
    "Tanzanian opposition leader Tundu Lissu was one of the other finalists."],
   [True, True, True],
   "Sakharov Prize 2026",
   "On 22 October 2026 the European Parliament's Conference of Presidents chose the International Criminal Court and "
   "its judges (nominated by the S&D group) for the 2026 Sakharov Prize, to be presented in Strasbourg in December. "
   "The other finalists were Tundu Lissu and the Iranian twins Taraneh and Romina Rahimi.",
   [fact("2026 Sakharov Prize to the International Criminal Court and its judges, announced 22 October 2026 by the "
         "Conference of Presidents of the European Parliament's political groups; other finalists Tundu Lissu and "
         "Taraneh and Romina Rahimi; ceremony in Strasbourg in December", "awr_sakh_if")],
   why="All three statements match the source.",
   current=ca("2026-10-22"))

GS(AW, NAT, "Advanced", "the Indira Gandhi Prize for Peace, Disarmament and Development for 2025",
   ["It is conferred by the Ministry of External Affairs.",
    "It was awarded to Graça Machel of Mozambique.",
    "It carries ₹1 crore along with a trophy and a citation."],
   [False, True, True],
   "Indira Gandhi Peace Prize 2025",
   "The Indira Gandhi Memorial Trust announced on 21 January 2026 that the 2025 prize goes to Mozambican rights activist "
   "Graça Machel. The international jury was chaired by former National Security Adviser Shivshankar Menon. The prize "
   "carries ₹1 crore, a trophy and a citation.",
   [fact("Indira Gandhi Memorial Trust announced the 2025 Indira Gandhi Prize for Peace, Disarmament and Development "
         "for Graça Machel of Mozambique; jury chaired by Shivshankar Menon; Rs 1 crore with trophy and citation; AICC "
         "post dated 21 January 2026", "awr_ig_week")],
   why="Statement 1 is wrong: the prize is given by the Indira Gandhi Memorial Trust, not a ministry.",
   current=ca("2026-01-21"))

GS(AW, NAT, "Advanced", "the 30th Business Today Best Banks awards held in Mumbai in February 2026",
   ["ICICI Bank was named Bank of the Year.",
    "Former RBI Governor Shaktikanta Das received the Lifetime Achievement award.",
    "The awards were presented by Union Finance Minister Nirmala Sitharaman."],
   [True, True, False],
   "BT Best Banks 2026",
   "At the 30th BT Best Banks event in Mumbai (reported 28 February 2026), Union Minister Nitin Gadkari presented 18 "
   "awards. ICICI Bank was Bank of the Year and Best Large Indian Bank, Bank of Maharashtra Best Mid-Sized Bank, "
   "Karur Vysya Bank Best Small Bank, and Shaktikanta Das got the Lifetime Achievement award.",
   [fact("30th BT Best Banks, Mumbai, reported 28 February 2026: Nitin Gadkari presented the awards; ICICI Bank Bank of "
         "the Year; Lifetime Achievement to former RBI Governor Shaktikanta Das; Bank of Maharashtra Best Mid-Sized "
         "Bank", "awr_bt_best")],
   why="Statement 3 is wrong: the awards were presented by Nitin Gadkari.",
   current=ca("2026-02-28"))

GS(AW, INTL, "Advanced", "the Goldman Environmental Prize 2026",
   ["One of the winners was an activist from India.",
    "For the first time, all the winners were women.",
    "Each winner receives USD 200,000."],
   [False, True, True],
   "Goldman Environmental Prize 2026",
   "The 2026 Goldman Environmental Prizes were presented in San Francisco on 20 April 2026 to six women, the first "
   "all-women cohort, from England, the United States, South Korea, Nigeria, Papua New Guinea and Colombia (including "
   "Iroro Tanshi of Nigeria). Each gets USD 200,000.",
   [fact("Goldman Environmental Prize 2026: ceremony in San Francisco on 20 April 2026; six women winners from England, "
         "the US, South Korea, Nigeria, Papua New Guinea and Colombia; first time all winners were women; USD 200,000 "
         "each", "awr_goldman_tp")],
   why="Statement 1 is wrong: the six winners were from England, the US, South Korea, Nigeria, Papua New Guinea and "
       "Colombia.",
   current=ca("2026-04-20"))

GS(AW, INTL, "Advanced", "the Wolf Prizes 2026, announced in October 2026",
   ["The Chemistry prize went to Shankar Balasubramanian, David Klenerman and Pascal Mayer for low-cost, large-scale "
    "DNA sequencing methods.",
    "The Physics prize went to Immanuel Bloch and Jun Ye for advances in the control of ultracold atomic systems.",
    "The Mathematics prize was awarded to a single mathematician from the United States."],
   [True, True, False],
   "Wolf Prize 2026",
   "The Wolf Foundation announced the 2026 laureates in Jerusalem. Chemistry: Indian-born Shankar Balasubramanian and "
   "David Klenerman (Cambridge) with Pascal Mayer, for DNA sequencing for genomic medicine. Physics: Immanuel Bloch and "
   "Jun Ye. Mathematics: Israeli mathematicians David Kazhdan and Joseph Bernstein. Medicine: Charles S. Zuker, for "
   "work on taste.",
   [fact("2026 Wolf Prizes: Chemistry to Shankar Balasubramanian (Indian-born), David Klenerman and Pascal Mayer for "
         "low-cost large-scale DNA sequencing; Physics to Immanuel Bloch and Jun Ye for control of ultracold atomic "
         "systems; Mathematics to David Kazhdan and Joseph Bernstein; Medicine to Charles S. Zuker; dateline 4 October "
         "2026", "awr_wolf_jns")],
   why="Statement 3 is wrong: the Mathematics prize was shared by two Israeli mathematicians, David Kazhdan and Joseph "
       "Bernstein.",
   current=ca("2026-10-04", inferred="wire dateline 4 Oct 2026; a CU Boulder story URL suggests 2-3 Oct, so stem "
                                    "says only 'October 2026'"))

# ------------------------------------------------------------------ Reports: Basic (5)
G(RP, PUB, "Basic",
  "The Climate Risk Index 2026, released at COP30 in Belém in November 2025 and ranking countries by the impact of "
  "extreme weather from 1995 to 2024, is published by which organisation?",
  ["Germanwatch", "Institute for Economics & Peace", "World Resources Institute", "UN Environment Programme"], "*",
  "Climate Risk Index",
  "Germanwatch released the Climate Risk Index 2026 at COP30. Over 1995-2024, Dominica, Myanmar and Honduras were the "
  "most affected; India ranked ninth, with about 80,000 deaths and roughly USD 170 billion in losses.",
  ["CRI 2026: Germanwatch, released at COP30 (Nov 2025)", "Period: 1995-2024; India 9th"],
  [fact("Germanwatch released the Climate Risk Index 2026 at COP30 in Belém (12 November 2025); period 1995-2024; top "
        "three Dominica, Myanmar, Honduras; India ninth", "awr_cri_dte")],
  why="The source names Germanwatch as the publisher; the other bodies are not.",
  current=ca("2025-11-12"))

G(RP, PUB, "Basic",
  "The annual 'Central Banker Report Cards', which grade central bank governors from A+ to F on inflation control, "
  "growth, currency stability, interest rates and independence, are published by which magazine?",
  ["Global Finance", "The Banker", "Euromoney", "Central Banking"], "*",
  "Central Banker Report Cards",
  "Global Finance released its Central Banker Report Cards 2026 on 8 September 2026, covering nearly 100 countries, "
  "territories and districts plus the EU and regional central banks. Grades run from A+ to F.",
  ["Central Banker Report Cards: Global Finance", "2026 edition: 8 Sep 2026; nearly 100 economies"],
  [fact("Global Finance Central Banker Report Cards 2026 released 8 September 2026; grades A+ to F on inflation control, "
        "economic growth, currency stability, interest rate management and independence; nearly 100 countries, "
        "territories and districts plus the EU and regional central banks", "awr_gf_rc")],
  why="The report cards are a Global Finance publication; The Banker, Euromoney and Central Banking are other titles.",
  current=ca("2026-09-08"))

G(RP, PUB, "Basic",
  "The Greenhouse Gas Bulletin No. 22, released on 27 October 2026 and reporting a record CO2 concentration of 426.8 "
  "ppm for 2025, is published by which body?",
  ["World Meteorological Organization", "UN Environment Programme", "Intergovernmental Panel on Climate Change",
   "International Energy Agency"], "*",
  "Greenhouse Gas Bulletin",
  "The WMO's Greenhouse Gas Bulletin No. 22 (27 October 2026) said CO2 reached 426.8 ppm in 2025, 153% of the "
  "pre-industrial (1750) level, and methane and nitrous oxide also hit records.",
  ["Publisher: WMO", "No. 22 (27 Oct 2026): CO2 426.8 ppm in 2025 = 153% of 1750 level"],
  [fact("WMO Greenhouse Gas Bulletin No. 22, 27 October 2026: CO2 426.8 ppm in 2025, 153% of pre-industrial; methane "
        "and nitrous oxide at records", "awr_wmo_ghg")],
  why="The source identifies the bulletin as a WMO publication; UNEP, IPCC and IEA do not publish it.",
  current=ca("2026-10-27"))

G(RP, RANK, "Basic",
  "In IQAir's World Air Quality Report 2025, released in March 2026, what was India's rank among the most polluted "
  "countries?",
  ["6th", "3rd", "5th", "9th"], "*",
  "World Air Quality Report",
  "IQAir's eighth annual report (24 March 2026) covered 9,446 cities in 143 countries. Pakistan, Bangladesh, "
  "Tajikistan, Chad and DR Congo were the five most polluted countries, and India was sixth with a PM2.5 average of "
  "48.9 µg/m³. Loni (Ghaziabad) was the world's most polluted city.",
  ["Top 5: Pakistan, Bangladesh, Tajikistan, Chad, DR Congo", "India: 6th", "Most polluted city: Loni"],
  [fact("IQAir 2025 World Air Quality Report, 24 March 2026: top five Pakistan, Bangladesh, Tajikistan, Chad, DR Congo; "
        "Loni most polluted city", "awr_iq_pr"),
   fact("India 6th most polluted of 143 countries in 2025 (48.9 µg/m3); New Delhi most polluted capital", "awr_iq_dr"),
   fact("India is sixth most polluted country; Loni world's most polluted city", "awr_iq_wire")],
  why="The first five places went to Pakistan, Bangladesh, Tajikistan, Chad and DR Congo, so India was not 3rd or 5th; "
      "the sources give 6th.",
  current=ca("2026-03-24"))

G(RP, RANK, "Basic",
  "In the Global Firepower 2026 military strength ranking of 145 countries, what was India's rank?",
  ["4th", "3rd", "5th", "6th"], "*",
  "Global Firepower 2026",
  "Global Firepower 2026 ranks the United States first, followed by Russia, China and India (4th); South Korea is 5th "
  "and France 6th. Pakistan is 14th. A lower PowerIndex score means greater strength.",
  ["GFP 2026: US, Russia, China, India (4th)", "5th South Korea, 6th France; 145 countries"],
  [fact("Global Firepower 2026: 1 United States, 2 Russia, 3 China, 4 India, 5 South Korea, 6 France; 145 countries; "
        "Pakistan 14th", "awr_gfp_list")],
  why="China is 3rd, South Korea 5th and France 6th in the 2026 list.",
  current=ca("2026-01-01", inferred="Global Firepower page gives only the 2026 edition year, no release day"))

# ------------------------------------------------------------------ Reports: Intermediate (1)
G(RP, RANK, "Intermediate",
  "SIPRI's data on world military expenditure for 2025, released in April 2026, showed India moving up to fifth place "
  "with spending of USD 92.1 billion. Which country did India overtake to reach this rank?",
  ["United Kingdom", "Germany", "Russia", "Saudi Arabia"], "*",
  "SIPRI military expenditure",
  "India's military spending rose 8.9% to USD 92.1 billion in 2025 (3.2% of the world total). It moved from sixth to "
  "fifth, overtaking the United Kingdom. The top five were the US, China, Russia, Germany and India, together 58% of "
  "world spending.",
  ["India: 5th (from 6th), USD 92.1 bn, +8.9%", "Overtook: United Kingdom", "Top 5: US, China, Russia, Germany, India"],
  [fact("SIPRI 2025 data: India 5th largest spender, up from 6th, overtaking the UK; USD 92.1 billion, up 8.9%; top "
        "spenders US, China, Russia, Germany, India (58% of total)", "awr_sipri_week"),
   fact("India becomes world's 5th largest military spender at USD 92.1 bn (28 April 2026)", "awr_sipri_bt")],
  why="Germany and Russia stayed ahead of India in 4th and 3rd place; the country India passed was the UK.",
  current=ca("2026-04-27", inferred="search reports a 27 Apr 2026 release; opened report is dated 28 Apr"))

# ------------------------------------------------------------------ Reports: Advanced (4)
GS(RP, PUB, "Advanced", "the report 'Employment and Social Trends 2026'",
   ["It is a flagship report of the International Labour Organization, released on 14 January 2026.",
    "It projects that the global unemployment rate will remain unchanged at 4.9% in 2026.",
    "It projects that the global jobs gap will reach about 408 million in 2026."],
   [True, True, True],
   "ILO flagship reports",
   "The ILO's 'Employment and Social Trends 2026' (World of Work series, 14 January 2026) projects global unemployment "
   "steady at 4.9% in 2026 and a jobs gap of 408 million. It notes about 2.1 billion informal workers and youth "
   "unemployment of 12.4%.",
   [fact("ILO 'Employment and Social Trends 2026', flagship report, released 14 January 2026; global unemployment to "
         "remain unchanged at 4.9% in 2026; jobs gap 408 million; 2.1 billion in informal employment; youth "
         "unemployment 12.4%", "awr_ilo_est")],
   why="All three statements match the ILO page.",
   current=ca("2026-01-14"))

GS(RP, PUB, "Advanced", "the WTO's 'Global Trade Outlook and Statistics' update of 8 October 2026",
   ["It raised its forecast of world services trade volume growth for 2026 above the 4.8% projected in March.",
    "It forecast world merchandise trade volume growth of 3.9% in 2026, up from 1.9% projected in March.",
    "It found that AI-enabling goods accounted for 47% of global merchandise trade growth in the first half of 2026."],
   [False, True, True],
   "WTO trade forecasts",
   "The WTO's October 2026 update raised the 2026 merchandise trade growth forecast to 3.9% (from 1.9%) with 4.1% for "
   "2027, but cut services trade growth for 2026 to 3.3% from 4.8%, as the Middle East conflict hit transport and "
   "travel. AI-enabling goods such as semiconductors and servers made up 47% of merchandise trade growth in H1 2026.",
   [fact("WTO Global Trade Outlook and Statistics, 8 October 2026: merchandise trade volume growth 3.9% in 2026 (up from "
         "1.9% in March), 4.1% in 2027; services 3.3% in 2026 (down from 4.8%); AI-enabling goods 47% of merchandise "
         "trade growth in H1 2026", "awr_wto_gtos")],
   why="Statement 1 is wrong: the services forecast for 2026 was cut to 3.3%.",
   current=ca("2026-10-08"))

GS(RP, PUB, "Advanced", "the SIPRI Yearbook 2026",
   ["It estimates that India had about 190 nuclear warheads as of January 2026.",
    "It estimates Pakistan's nuclear stockpile to be larger than India's.",
    "It says the nine nuclear-armed states together held about 12,187 nuclear weapons at the start of 2026, of which "
    "9,745 were in military stockpiles."],
   [True, False, True],
   "SIPRI Yearbook",
   "The SIPRI Yearbook 2026, launched in June 2026, estimates about 190 warheads for India and 170 for Pakistan as of "
   "January 2026. The nine nuclear-armed states held about 12,187 weapons, 9,745 of them in military stockpiles.",
   [fact("SIPRI Yearbook 2026: India about 190 nuclear warheads as of January 2026; Pakistan about 170; nine states held "
         "about 12,187 nuclear weapons, 9,745 in military stockpiles", "awr_sipri_yb")],
   why="Statement 2 is wrong: Pakistan's estimated 170 warheads are fewer than India's 190.",
   current=ca("2026-06-08", inferred="source says launched 'on Monday'; page dated 8 Jun 2026 (a Monday)"))

GS(RP, RANK, "Advanced", "India in the Asia Power Index 2025",
   ["The index is published by the Australia-based Lowy Institute.",
    "India ranked third and reached the 40-point threshold for 'major power' status.",
    "The 2025 edition assessed 50 countries and territories."],
   [True, True, False],
   "Asia Power Index",
   "The Lowy Institute's Asia Power Index 2025 (released 28 November 2025) placed India third, behind the US and China, "
   "and India's score reached the 40-point 'major power' threshold. The index covers 27 countries and territories with "
   "131 indicators across eight measures.",
   [fact("Asia Power Index 2025 by Australia-based Lowy Institute; India third; 27 countries and territories, 131 "
         "indicators, eight measures", "awr_api_air"),
   fact("India crosses the 40-point major power threshold in Asia Power Index 2025; third rank", "awr_api_trib"),
   fact("India ranks third in Asia Power Index 2025, behind the US and China", "awr_api_tnm")],
   why="Statement 3 is wrong: the index covers 27 countries and territories.",
   current=ca("2025-11-28"))

# ###################################################################### part: ssd (summits + sports + days)
# ###################################################################### part: ssd (summits, sports, days)
U.update({
    "ssd_sco_cfm": ("https://eng.sectsco.org/20260724/2467622.html", OPENED),
    "ssd_brics_china": ("https://timesofoman.com/article/176867-brics-chairship-passes-to-china-as-pm-modi-extends-best-wishes",
                        OPENED),
    "ssd_brics_fmm": ("https://ianslive.in/brics-foreign-ministers-meet-to-kick-off-in-delhi-today--20260514064713",
                      OPENED),
    "ssd_apec_cd": ("https://regional.chinadaily.com.cn/cppcc/2025-11/02/c_1137331.htm", OPENED),
    "ssd_apec_cgtn": ("https://news.cgtn.com/news/2025-12-13/2026-APEC-meeting-to-be-held-Nov-18-19-in-Shenzhen-China-"
                      "1J43L2Fb2w0/share_amp.html", SEARCH),
    "ssd_cop32_cit": ("https://citizen.digital/article/ethiopia-set-to-host-uns-2027-climate-summit-2026-undecided-n372871",
                      OPENED),
    "ssd_cop32_aa": ("https://allafrica.com/stories/202608060093.html", OPENED),
    "ssd_cop33_chn": ("https://www.climatechangenews.com/2026/04/08/india-withdraws-bid-to-host-cop33-climate-talks/",
                      OPENED),
    "ssd_ai_swi": ("https://www.swissinfo.ch/eng/swiss-ai/switzerland-to-host-the-next-world-summit-on-ai/90966531",
                   OPENED),
    "ssd_ai_scene": ("https://www.scenenow.com/Business/UAE-to-Co-Chair-2027-AI-Summit-With-Switzerland-Host-2028-Edition",
                     OPENED),
    "ssd_gff_air": ("https://newsonair.gov.in/pm-modi-to-inaugurate-and-address-the-global-fintech-fest-gff-2026-in-mumbai/",
                    OPENED),
    "ssd_iew_bt": ("https://www.businesstoday.in/india/story/india-energy-week-2026-set-to-open-in-goa-with-record-"
                   "participation-global-energy-deals-on-the-agenda-512728-2026-01-23", OPENED),
    "ssd_iew_trib": ("https://www.tribuneindia.com/news/business/india-energy-week-2026-to-be-held-in-goa-during-january-"
                     "27-30-with-global-participation/", SEARCH),
    "ssd_g20_uk": ("https://www.gov.uk/government/news/manchester-to-host-world-leaders-at-the-2027-g20-summit", OPENED),
    "ssd_g20_kr": ("https://www.koreajoongangdaily.com/korea/korea-confirmed-as-host-of-2028-g20-summit-as-lee-calls-for-"
                   "predictable-trading-order/12486167", OPENED),
    "ssd_uso_dr": ("https://www.drishtiias.com/state-pcs-current-affairs/alexander-zverev-wins-2026-us-open-title", OPENED),
    "ssd_uso_org": ("https://www.usopen.org/amp/en_US/news/articles/2026-09-12/who_won_the_2026_us_open.html", SEARCH),
    "ssd_atp": ("https://www.atptour.com/en/news/nitto-atp-finals-2025-results", OPENED),
    "ssd_duplantis": ("https://worldathletics.org/news/report/duplantis-breaks-world-pole-vault-record-in-uppsala", OPENED),
    "ssd_hil": ("https://www.orissapost.com/hil-final-vedanta-kalinga-lancers-beat-ranchi-royals-3-2-to-clinch-title/",
                OPENED),
    "ssd_d_nonviol": ("https://www.un.org/en/observances/non-violence-day", OPENED),
    "ssd_d_anticorr": ("https://www.un.org/en/observances/anti-corruption-day", OPENED),
    "ssd_d_soil": ("https://www.fao.org/world-soil-day/en/", OPENED),
    "ssd_d_peace": ("https://www.un.org/en/observances/international-day-peace", OPENED),
    "ssd_d_aids": ("https://www.un.org/en/observances/world-aids-day", OPENED),
    "ssd_d_idpd": ("https://www.un.org/en/observances/day-of-persons-with-disabilities", OPENED),
    "ssd_d_press": ("https://www.un.org/en/observances/press-freedom-day", OPENED),
    "ssd_d_ozone": ("https://www.un.org/en/observances/ozone-day", OPENED),
    "ssd_d_mld": ("https://www.un.org/en/observances/mother-language-day", OPENED),
})

T = "Summits and Conferences"
GBS, HOST = "G20, BRICS, SCO and others", "Hosting countries"

# ------------------------------------------------------------------ Summits: Intermediate (9)
G(T, GBS, "Intermediate",
  "The meeting of the SCO Council of Ministers of Foreign Affairs held on 24 July 2026, which approved the draft "
  "Bishkek Declaration for the organisation's 25th anniversary summit, took place in which city of Kyrgyzstan?",
  ["Cholpon-Ata", "Osh", "Karakol", "Jalal-Abad"], "*",
  "SCO Council of Foreign Ministers 2026",
  "On 24 July 2026 the SCO foreign ministers met in Cholpon-Ata, Kyrgyzstan. They approved draft documents, including "
  "the Bishkek Declaration marking the SCO's 25th anniversary, for the Heads of State meeting in Bishkek on 1 "
  "September 2026, and adopted a CMFA statement. India was represented by Minister of State for External Affairs "
  "Kirti Vardhan Singh.",
  ["Meeting: SCO CMFA, 24 Jul 2026", "Venue: Cholpon-Ata, Kyrgyzstan", "India: MoS Kirti Vardhan Singh"],
  [fact("SCO Council of Ministers of Foreign Affairs met on 24 July 2026 in Cholpon-Ata, Kyrgyz Republic; approved "
        "draft Bishkek Declaration for the 25th anniversary; India represented by MoS Kirti Vardhan Singh",
        "ssd_sco_cfm")],
  why="The SCO page names Cholpon-Ata as the venue; the other Kyrgyz cities did not host the meeting.",
  current=ca("2026-07-24"))

G(T, GBS, "Intermediate",
  "Who chaired the BRICS Foreign Ministers' Meeting held in New Delhi on 14-15 May 2026 under India's BRICS "
  "chairship?",
  ["S. Jaishankar", "Kirti Vardhan Singh", "Ajit Doval", "Pabitra Margherita"], "*",
  "BRICS Foreign Ministers' Meeting 2026",
  "As BRICS chair for 2026, India hosted the two-day BRICS Foreign Ministers' Meeting in New Delhi on 14-15 May 2026. "
  "External Affairs Minister S. Jaishankar chaired it, with foreign ministers and senior representatives of member "
  "and partner countries attending.",
  ["Meeting: BRICS FMM, New Delhi, 14-15 May 2026", "Chair: EAM S. Jaishankar"],
  [fact("BRICS Foreign Ministers' Meeting in New Delhi on 14-15 May 2026 under India's chairship, chaired by EAM S. "
        "Jaishankar", "ssd_brics_fmm")],
  why="The report names External Affairs Minister S. Jaishankar as chair; the others did not chair the meeting.",
  current=ca("2026-05-14"))

G(T, GBS, "Intermediate",
  "What was the theme of the seventh edition of the Global Fintech Fest (GFF 2026), held in Mumbai from 8 to 11 "
  "September 2026?",
  ["Potential to Impact: Agentic AI, Tokenisation, Quantum",
   "Empowering Finance for a Better World: Powered by AI",
   "Blueprint for the Next Decade of Global Fintech",
   "Digital Public Infrastructure for Inclusive Growth"], "*",
  "Global Fintech Fest 2026",
  "GFF 2026, the seventh edition, was a four-day event in Mumbai from 8 to 11 September 2026, scheduled to be "
  "inaugurated by Prime Minister Narendra Modi. Its theme was 'Potential to Impact: Agentic AI, Tokenisation, Quantum - Trusted, "
  "Connected, Global Systems for Inclusive Finance'.",
  ["GFF 2026: 7th edition, Mumbai, 8-11 Sep 2026", "Theme: Potential to Impact (Agentic AI, Tokenisation, Quantum)"],
  [fact("Seventh edition of GFF, Mumbai, 8-11 September 2026; theme 'Potential to Impact: Agentic AI, Tokenisation, "
        "Quantum - Trusted, Connected, Global Systems for Inclusive Finance'; PM Modi to inaugurate", "ssd_gff_air")],
  why="The AIR report gives 'Potential to Impact: Agentic AI, Tokenisation, Quantum' as the 2026 theme; the other "
      "phrases are not the GFF 2026 theme.",
  current=ca("2026-09-08"))

G(T, GBS, "Intermediate",
  "The fourth edition of India Energy Week (IEW 2026), held from 27 to 30 January 2026 at the ONGC Academy for "
  "Training and Innovation, took place in which state?",
  ["Goa", "Gujarat", "Maharashtra", "Karnataka"], "*",
  "India Energy Week 2026",
  "India Energy Week 2026, the fourth edition, was held from 27 to 30 January 2026 at the ONGC Academy for Training "
  "and Innovation (ATI) in Goa, with over 75,000 participants expected. It focused on energy security, investment "
  "and pathways for decarbonisation.",
  ["IEW 2026: 4th edition, 27-30 Jan 2026", "Venue: ONGC ATI, Goa"],
  [fact("IEW 2026, 27-30 January 2026, ONGC Academy for Training and Innovation (ATI), Goa; over 75,000 participants",
        "ssd_iew_bt"),
   fact("India Energy Week 2026 to be held in Goa during January 27-30", "ssd_iew_trib")],
  why="The reports place IEW 2026 in Goa; it was not held in Gujarat, Maharashtra or Karnataka.",
  current=ca("2026-01-27"))

G(T, HOST, "Intermediate",
  "At the close of the 18th BRICS Summit in New Delhi in September 2026, Prime Minister Modi wished which country "
  "well as the next BRICS host, which is to hold the 19th summit in 2027?",
  ["China", "Russia", "South Africa", "Brazil"], "*",
  "BRICS chairship 2027",
  "India hosted the 18th BRICS Summit at Bharat Mandapam, New Delhi. On the closing day, 13 September 2026, Prime "
  "Minister Modi extended his best wishes to China as the next host of BRICS; China will host the 19th BRICS Summit "
  "in 2027.",
  ["BRICS 2026: India (18th summit)", "BRICS 2027: China (19th summit)"],
  [fact("Modi: 'best wishes once again to China as the next host of BRICS'; China to host the 19th BRICS Summit in "
        "2027; report dated 13 September 2026", "ssd_brics_china")],
  why="The report names China as the next BRICS host; Russia, South Africa and Brazil are not the 2027 host.",
  current=ca("2026-09-13"))

G(T, HOST, "Intermediate",
  "At the APEC handover session in Gyeongju on 1 November 2025, President Xi Jinping announced that which Chinese "
  "city will host the APEC Economic Leaders' Meeting in November 2026?",
  ["Shenzhen", "Shanghai", "Guangzhou", "Hangzhou"], "*",
  "APEC 2026",
  "At the handover session of the 32nd APEC Economic Leaders' Meeting in Gyeongju, South Korea, on 1 November 2025, "
  "Xi Jinping announced that Shenzhen would host the APEC Economic Leaders' Meeting in November 2026, the third time "
  "China hosts it. The meeting was later fixed for 18-19 November 2026.",
  ["Announcement: Gyeongju, 1 Nov 2025", "APEC 2026 host city: Shenzhen (China's third time)"],
  [fact("Xi announced on 1 November 2025 in Gyeongju that Shenzhen will host the APEC Economic Leaders' Meeting in "
        "November 2026; third time China hosts it", "ssd_apec_cd"),
   fact("2026 APEC meeting to be held on 18-19 November in Shenzhen", "ssd_apec_cgtn")],
  why="The sources name Shenzhen; Shanghai, Guangzhou and Hangzhou are not the 2026 venue.",
  current=ca("2025-11-01"))

G(T, HOST, "Intermediate",
  "During COP30 in Belém in November 2025, the African Group of Negotiators endorsed which country, ahead of a rival "
  "bid from Nigeria, to host the COP32 climate conference in 2027?",
  ["Ethiopia", "Kenya", "Egypt", "Morocco"], "*",
  "COP32 host",
  "On the second day of COP30, the chair of the African Group of Negotiators said the group had endorsed Ethiopia to "
  "host COP32 in 2027 over Nigeria's bid, and the Brazilian presidency confirmed the choice. Ethiopia's ambassador "
  "said delegates would be welcomed to Addis Ababa. In August 2026 Ethiopia and the AU Commission discussed COP32 "
  "preparations.",
  ["COP32 (2027): Ethiopia, Addis Ababa", "Rival bid: Nigeria", "Endorsed by African Group during COP30"],
  [fact("Africa Group of Negotiators endorsed Ethiopia for COP32 in 2027 over Nigeria; news broke on the second day "
        "of COP30; 'welcoming all of you to Addis Ababa for COP32'", "ssd_cop32_cit"),
   fact("COP32, the 2027 UN Climate Change Conference, which Ethiopia is set to host (5 August 2026)",
        "ssd_cop32_aa")],
  why="The sources name Ethiopia as the endorsed host; Kenya, Egypt and Morocco were not chosen for COP32.",
  current=ca("2025-11-12", inferred="date of the opened source article (12 Nov 2025); it says the news broke on the "
                                    "second day of COP30 but gives no day"))

G(T, HOST, "Intermediate",
  "In April 2026 India withdrew its offer, first announced by Prime Minister Modi at COP28 in Dubai, to host which "
  "UN climate conference in 2028?",
  ["COP33", "COP31", "COP32", "COP34"], "*",
  "India and COP33",
  "Prime Minister Modi offered at COP28 in Dubai (December 2023) to host COP33 in 2028. On 2 April 2026 India told "
  "other countries that it was withdrawing the offer 'following a review of its commitments for the year 2028'. "
  "The 2028 host is to come from the Asia-Pacific Group.",
  ["Offer: COP28 Dubai, Dec 2023", "Withdrawn: 2 Apr 2026", "Conference: COP33 (2028)"],
  [fact("India informed other nations on 2 April 2026 that it was withdrawing its offer to host COP33 in 2028; Modi "
        "first made the offer at COP28 in Dubai in December 2023", "ssd_cop33_chn")],
  why="The 2028 conference is COP33; COP31 (2026), COP32 (2027) and COP34 are other editions.",
  current=ca("2026-04-02"))

G(T, HOST, "Intermediate",
  "At the AI Impact Summit in New Delhi on 19 February 2026, the President of which country announced that it will "
  "host the next global AI summit, in Geneva in 2027?",
  ["Switzerland", "France", "United Arab Emirates", "United Kingdom"], "*",
  "Next AI summit host",
  "Swiss President Guy Parmelin announced in New Delhi on 19 February 2026, in the presence of Prime Minister Modi, "
  "that Switzerland will host the next AI summit in Geneva in 2027. He said Switzerland would work with the United "
  "Arab Emirates, which is to host the 2028 summit; reports describe the UAE as co-chair of the 2027 summit.",
  ["Announced: New Delhi, 19 Feb 2026, by Guy Parmelin", "2027: Geneva, Switzerland", "2028: UAE"],
  [fact("Swiss President Guy Parmelin announced on 19 February 2026 in New Delhi that Switzerland will host the next "
        "AI summit in Geneva in 2027; UAE to host in 2028", "ssd_ai_swi"),
   fact("UAE to co-chair the 2027 AI Summit with Switzerland in Geneva and host the 2028 edition", "ssd_ai_scene")],
  why="The UAE is to co-chair 2027 and host 2028; the 2027 host announced by Parmelin is Switzerland.",
  current=ca("2026-02-19"))

# ------------------------------------------------------------------ Summits: Advanced (1)
GS(T, HOST, "Advanced", "the hosting of future G20 summits",
   ["The G20 Leaders' Summit of 27-28 November 2027 is to be held at the Manchester Central Convention Centre.",
    "The Johannesburg leaders' declaration of November 2025 says the G20 will meet in the Republic of Korea in 2028.",
    "The 2027 summit will be the United Kingdom's first G20 summit since it hosted one in 2010."],
   [True, True, False],
   "G20 hosts 2027 and 2028",
   "The UK government said on 23 September 2026 that the G20 Leaders' Summit will take place on 27-28 November 2027 "
   "at Manchester Central, and that the UK last hosted the G20 summit in 2009. The Johannesburg declaration "
   "(November 2025) says the G20 will meet in the United Kingdom in 2027 and in the Republic of Korea in 2028, Korea's "
   "first since the 2010 Seoul summit.",
   [fact("G20 Leaders' Summit on 27-28 November 2027 at Manchester Central Convention Centre; UK last hosted the G20 "
         "summit in 2009 (published 23 September 2026)", "ssd_g20_uk"),
    fact("Declaration: meet again in the United Kingdom in 2027 and in the Republic of Korea in 2028; first in Korea "
         "since the 2010 Seoul Summit (23 November 2025)", "ssd_g20_kr")],
   why="Statement 3 is wrong: the UK last hosted the G20 summit in 2009; the 2010 summit was in Seoul.",
   current=ca("2026-09-23"))

# ====================================================================== Sports
T = "Sports"
TW, VR = "Tournaments and winners", "Venues and records"

G(T, TW, "Intermediate",
  "Alexander Zverev won the men's singles title at the US Open 2026, his second Grand Slam title of the year. Whom "
  "did he beat in the final?",
  ["Ben Shelton", "Carlos Alcaraz", "Jannik Sinner", "Taylor Fritz"], "*",
  "US Open 2026",
  "Germany's Alexander Zverev beat American Ben Shelton, who was playing his first Grand Slam final, in the US Open "
  "2026 men's singles final on 13 September 2026 (6-3, 7-5, 5-7, 6-2). It was Zverev's second major of 2026 after "
  "Roland Garros.",
  ["Champion: Alexander Zverev (Germany)", "Runner-up: Ben Shelton (USA)", "Zverev's 2nd major of 2026"],
  [fact("Zverev won the 2026 US Open title, beating Ben Shelton in his first Grand Slam final; second Grand Slam of "
        "2026 after Roland Garros", "ssd_uso_dr"),
   fact("Alexander Zverev won the 2026 US Open men's singles title on Sunday, 6-3, 7-5, 5-7, 6-2", "ssd_uso_org")],
  why="The sources name Ben Shelton as the beaten finalist; Alcaraz, Sinner and Fritz did not play the final.",
  current=ca("2026-09-13"))

G(T, TW, "Intermediate",
  "Who won the singles title at the Nitto ATP Finals 2025 in Turin, beating top seed Carlos Alcaraz 7-6(4), 7-5 in "
  "the final on 16 November 2025?",
  ["Jannik Sinner", "Alexander Zverev", "Novak Djokovic", "Taylor Fritz"], "*",
  "ATP Finals 2025",
  "Second seed Jannik Sinner of Italy beat first seed Carlos Alcaraz 7-6(4), 7-5 in the singles final of the Nitto "
  "ATP Finals in Turin on 16 November 2025. The doubles title went to Harri Heliovaara and Henry Patten.",
  ["Winner: Jannik Sinner (ITA, seed 2)", "Runner-up: Carlos Alcaraz (ESP, seed 1)", "Score: 7-6(4), 7-5"],
  [fact("Nitto ATP Finals 2025 singles final, 16 November 2025: [2] Jannik Sinner (ITA) d [1] Carlos Alcaraz (ESP) "
        "76(4) 75; doubles: Heliovaara/Patten", "ssd_atp")],
  why="The ATP results page lists Sinner as the winner; the other players did not win the final.",
  current=ca("2025-11-16"))

G(T, VR, "Intermediate",
  "On 12 March 2026 Armand 'Mondo' Duplantis set his 15th pole vault world record at the Mondo Classic in Uppsala, "
  "Sweden. What height did he clear?",
  ["6.31 m", "6.30 m", "6.28 m", "6.33 m"], "*",
  "Pole vault world record",
  "At the Mondo Classic indoor meeting in Uppsala on 12 March 2026, Duplantis cleared 6.31 m, adding one centimetre "
  "to the 6.30 m he set while winning the world title in Tokyo. It was the 15th world record of his career, subject "
  "to ratification.",
  ["Height: 6.31 m (previous 6.30 m, Tokyo)", "Venue: Mondo Classic, Uppsala, 12 Mar 2026", "15th world record"],
  [fact("Duplantis cleared 6.31m at the Mondo Classic in Uppsala on 12 March 2026, his 15th world record; previous "
        "6.30m set at the world championships in Tokyo", "ssd_duplantis")],
  why="6.30 m was his previous record; 6.28 m and 6.33 m are not the height cleared in Uppsala.",
  current=ca("2026-03-12"))

GS(T, TW, "Advanced", "the final of the men's Hockey India League 2025-26",
   ["Vedanta Kalinga Lancers beat Ranchi Royals 3-2 in the final.",
    "The final was played at the Kalinga Stadium, Bhubaneswar, on 26 January 2026.",
    "Alexander Hendrickx scored two of the winning team's goals in the final."],
   [True, True, True],
   "Hockey India League 2025-26",
   "Vedanta Kalinga Lancers beat Ranchi Royals 3-2 in the men's HIL final at the Kalinga Stadium, Bhubaneswar, on 26 "
   "January 2026. Alexander Hendrickx scored twice and Dilpreet Singh once; the champions received ₹3 crore and "
   "the runners-up ₹2 crore.",
   [fact("HIL final, 26 January 2026, Kalinga Stadium Bhubaneswar: Vedanta Kalinga Lancers 3-2 Ranchi Royals; "
         "Hendrickx (4th, 27th), Dilpreet Singh (25th); prize Rs 3 crore", "ssd_hil")],
   why="All three statements match the match report.",
   current=ca("2026-01-26"))

# ====================================================================== Important Days
T = "Important Days"
DT = "Days and themes"

G(T, DT, "Basic",
  "The International Day of Non-Violence, observed on 2 October (Mahatma Gandhi's birthday), was established by a "
  "UN General Assembly resolution adopted in which year?",
  ["2007", "2004", "2010", "1999"], "*",
  "International Day of Non-Violence",
  "The UN General Assembly established 2 October, Gandhi's birthday, as the International Day of Non-Violence by "
  "resolution A/RES/61/271 adopted on 15 June 2007.",
  ["Date: 2 October (Gandhi's birthday)", "Resolution A/RES/61/271, 15 June 2007"],
  [fact("International Day of Non-Violence, 2 October, Gandhi's birthday; established by UNGA resolution "
        "A/RES/61/271 of 15 June 2007", "ssd_d_nonviol")],
  why="The UN page gives 2007; the other years are not when the Day was established.")

G(T, DT, "Basic",
  "International Anti-Corruption Day is observed on 9 December. It is linked to which convention, adopted by the UN "
  "General Assembly on 31 October 2003?",
  ["United Nations Convention against Corruption",
   "United Nations Convention against Transnational Organized Crime",
   "OECD Anti-Bribery Convention",
   "Inter-American Convention against Corruption"], "*",
  "International Anti-Corruption Day",
  "The UN Convention against Corruption (UNCAC) was adopted by the General Assembly on 31 October 2003 (resolution "
  "58/4) and entered into force in December 2005. The Assembly designated 9 December as International "
  "Anti-Corruption Day to raise awareness of corruption and of the Convention's role.",
  ["Day: 9 December", "UNCAC adopted 31 Oct 2003 (res. 58/4), in force Dec 2005"],
  [fact("9 December International Anti-Corruption Day; UN Convention against Corruption adopted 31 October 2003 by "
        "resolution 58/4, entered into force December 2005", "ssd_d_anticorr")],
  why="The UN page links the Day to the UN Convention against Corruption; the other conventions are different "
      "instruments.")

G(T, DT, "Basic",
  "World Soil Day (5 December) became an official international day, endorsed by the UN General Assembly, in 2014 "
  "under the leadership of which country?",
  ["Thailand", "Brazil", "Kenya", "India"], "*",
  "World Soil Day",
  "World Soil Day is observed on 5 December. With the UN General Assembly's endorsement (resolution A/RES/68/232), "
  "it became an official international day in 2014 under the leadership of the Kingdom of Thailand; FAO runs it "
  "within the framework of the Global Soil Partnership.",
  ["Date: 5 December", "Official since 2014 (A/RES/68/232)", "Leadership: Thailand"],
  [fact("World Soil Day became official in 2014 under the leadership of the Kingdom of Thailand, endorsed by the UN "
        "General Assembly (A/RES/68/232); FAO within the Global Soil Partnership", "ssd_d_soil")],
  why="The FAO page credits Thailand; Brazil, Kenya and India did not lead the initiative.")

G(T, DT, "Basic",
  "The International Day of Peace, observed on 21 September, was established by the UN General Assembly in which "
  "year?",
  ["1981", "1975", "1991", "2001"], "*",
  "International Day of Peace",
  "The UN General Assembly established the International Day of Peace in 1981. In 2001 the Assembly designated the "
  "Day as a period of non-violence and ceasefire. It is observed on 21 September.",
  ["Date: 21 September", "Established: 1981", "2001: designated a day of non-violence and ceasefire"],
  [fact("International Day of Peace, 21 September; established by the General Assembly in 1981; in 2001 designated "
        "as a period of non-violence and cease-fire", "ssd_d_peace")],
  why="1981 is the year of establishment; 2001 is when it was designated a day of ceasefire, and 1975 and 1991 are "
      "not given by the UN page.")

GS(T, DT, "Advanced", "World AIDS Day 2025",
   ["Its theme was 'Take the rights path'.",
    "It was observed on 1 December 2025.",
    "The UN page on the Day cites ending AIDS by 2030 as the Sustainable Development Goal target."],
   [False, True, True],
   "World AIDS Day 2025",
   "World AIDS Day is observed on 1 December. The UN's 2025 theme was 'Overcoming disruption, transforming the AIDS "
   "response', amid funding cuts that disrupted HIV prevention services. The UN page cites ending AIDS by 2030 as the "
   "SDG target.",
   [fact("World AIDS Day observed on 1 December; 2025 theme 'Overcoming disruption, transforming the AIDS response'; "
         "SDG target of ending AIDS by 2030", "ssd_d_aids")],
   why="Statement 1 is wrong: the UN gives the 2025 theme as 'Overcoming disruption, transforming the AIDS response'.",
   current=ca("2025-12-01"))

GS(T, DT, "Advanced", "the International Day of Persons with Disabilities 2025",
   ["It was observed on 3 December 2025.",
    "Its theme was 'Fostering disability inclusive societies for advancing social progress'.",
    "The UN Disability Inclusion Strategy, which the UN page refers to, was launched in June 2019."],
   [True, True, True],
   "International Day of Persons with Disabilities 2025",
   "The Day is observed on 3 December. The 2025 theme was 'Fostering disability inclusive societies for advancing "
   "social progress'. The UN page notes that the UN Disability Inclusion Strategy was launched in June 2019, and that "
   "about 1.3 billion people (about 1 in 6) have a significant disability.",
   [fact("International Day of Persons with Disabilities on 3 December; 2025 theme 'Fostering disability inclusive "
         "societies for advancing social progress'; UN Disability Inclusion Strategy launched June 2019",
         "ssd_d_idpd")],
   why="All three statements match the UN observance page.",
   current=ca("2025-12-03"))

GS(T, DT, "Advanced", "World Press Freedom Day 2026",
   ["Its theme was 'Shaping a Future at Peace'.",
    "Its Global Conference was hosted by Nairobi, Kenya.",
    "The Day was proclaimed by the UN General Assembly in December 1993, following a recommendation of UNESCO's "
    "General Conference."],
   [True, False, True],
   "World Press Freedom Day 2026",
   "World Press Freedom Day, 3 May, marks the anniversary of the Windhoek Declaration. The UN General Assembly "
   "proclaimed it in December 1993 on the recommendation of UNESCO's General Conference. The 2026 theme was 'Shaping "
   "a Future at Peace', and Lusaka, Zambia, hosted the 2026 Global Conference on 4 May 2026.",
   [fact("2026 theme 'Shaping a Future at Peace'; Lusaka, Zambia hosts the WPFD 2026 Global Conference on 4 May 2026; "
         "proclaimed by UNGA in December 1993 following UNESCO General Conference recommendation; 3 May is the "
         "anniversary of the Windhoek Declaration", "ssd_d_press")],
   why="Statement 2 is wrong: the 2026 Global Conference was hosted by Lusaka, Zambia.",
   current=ca("2026-05-03"))

GS(T, DT, "Advanced", "the International Day for the Preservation of the Ozone Layer (World Ozone Day) 2026",
   ["The Day commemorates the signing of the Vienna Convention in 1985.",
    "Its 2026 theme, 'Global action for a cooler planet', marks ten years since the adoption of the Kigali "
    "Amendment.",
    "The UN General Assembly proclaimed the Day in 1994 by resolution 49/114."],
   [False, True, True],
   "World Ozone Day 2026",
   "World Ozone Day, 16 September, commemorates the signing of the Montreal Protocol on Substances that Deplete the "
   "Ozone Layer in 1987. The UN General Assembly proclaimed it in 1994 (resolution 49/114). The 2026 theme, 'Global "
   "action for a cooler planet', marks ten years since the Kigali Amendment was adopted.",
   [fact("World Ozone Day 16 September commemorates the signing of the Montreal Protocol in 1987; proclaimed by UNGA "
         "in 1994 by resolution 49/114; 2026 theme 'Global action for a cooler planet', ten years since the Kigali "
         "Amendment", "ssd_d_ozone")],
   why="Statement 1 is wrong: the Day commemorates the signing of the Montreal Protocol in 1987.",
   current=ca("2026-09-16"))

GS(T, DT, "Advanced", "International Mother Language Day 2026",
   ["Its theme was 'Youth voices on multilingual education'.",
    "The Day, an idea proposed by Bangladesh, was proclaimed by UNESCO's General Conference in November 1999.",
    "The UN General Assembly welcomed the proclamation in 2012."],
   [True, True, False],
   "International Mother Language Day 2026",
   "International Mother Language Day is observed on 21 February. Proposed by Bangladesh, it was proclaimed by "
   "UNESCO's General Conference in November 1999, and the UN General Assembly welcomed the proclamation in resolution "
   "56/262 of 2002. The 2026 theme was 'Youth voices on multilingual education'.",
   [fact("21 February; proclaimed by UNESCO General Conference in November 1999; UNGA welcomed it in 2002 resolution "
         "56/262; 2026 theme 'Youth voices on multilingual education'; idea of Bangladesh", "ssd_d_mld")],
   why="Statement 3 is wrong: the General Assembly welcomed the proclamation in 2002 (resolution 56/262).",
   current=ca("2026-02-21"))

# ###################################################################### part: eco (economy + policies + schemes)
# ###################################################################### part: eco
# Economic Affairs (B1 / I5 / A1), Government Policies (I6 / A1), Government Schemes (B2 / I2 / A4)
U.update({
    "eco_cpi_apr": ("https://theprint.in/economy/retail-inflation-edges-up-to-3-48-pc-in-april-on-costlier-jewellery-"
                    "kitchen-staples/2929283/", OPENED),
    "eco_cpi_apr_ao": ("https://www.angelone.in/news/economy/india-s-retail-inflation-rises-marginally-to-3-48-in-april-"
                       "2026", SEARCH),
    "eco_wpi_dec": ("https://www.tribuneindia.com/news/business/wholesale-inflation-rises-to-0-83-in-december-2025-as-"
                    "manufacturing-and-primary-costs-climb/", OPENED),
    "eco_wpi_dec_st": ("https://www.thestatesman.com/business/wpi-inflation-turns-positive-at-0-83-in-december-2025-"
                       "1503540324.html", SEARCH),
    "eco_moodys": ("https://newsonair.gov.in/indias-real-gdp-growth-forecast-to-7-for-current-financial-year-moody/",
                   OPENED),
    "eco_omo_rbi": ("https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=61751", OPENED),
    "eco_dtax": ("https://theprint.in/economy/net-direct-tax-collection-rises-5-pc-to-rs-23-40-lakh-cr-in-fy26-misses-"
                 "revised-budget-target/2922139/", OPENED),
    "eco_fd_q1": ("https://theprint.in/economy/fiscal-deficit-touches-18-2-pc-of-full-year-target-in-q1-cga-data/"
                  "3002122/", OPENED),
    "eco_fd_q1_dc": ("https://www.deccanchronicle.com/business/economics/indias-fiscal-deficit-touches-182-pc-of-fy27-"
                     "target-in-q1-1975615", SEARCH),
    "eco_wb_oct": ("https://www.goodreturns.in/news/world-bank-raises-india-fy27-growth-forecast-to-7-1-economy-to-"
                   "outpace-regional-peers-1539419.html", OPENED),
    "eco_wb_oct_nb": ("https://www.newsbytesapp.com/news/business/world-bank-raises-india-growth-forecast-to-71-for-2026-"
                      "27/tldr", SEARCH),
    # policies
    "eco_rbios_knn": ("https://knnindia.co.in/news/newsdetails/sectors/financefintech/rbi-lifts-dispute-amount-cap-in-"
                      "ombudsman-cases-sets-rs-30-lakh-compensation-ceiling", OPENED),
    "eco_rbios_vk": ("https://vinodkothari.com/2026/01/rbi-integrated-ombudsman-scheme-2026-key-changes/", SEARCH),
    "eco_itrules": ("https://www.taxmann.com/post/blog/cbdt-notifies-income-tax-rules/", OPENED),
    "eco_stt_bt": ("https://businesstoday.in/markets/story/bt-explainer-how-stt-charges-hike-from-april-1-will-impact-"
                   "investors-fo-traders-old-vs-new-tax-522755-2026-03-27", OPENED),
    "eco_sebi_brk": ("https://newsable.asianetnews.com/amp/business/sebi-overhauls-market-rules-replaces-30yearold-"
                     "broker-regulations-articleshow-v86edfv", OPENED),
    "eco_rbi_oct_sdrp": ("https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63743", OPENED),
    "eco_rbi_aug_sdrp": ("https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63289", OPENED),
    "eco_rbi_policy_idx": ("https://www.rbi.org.in/Scripts/Annualpolicy.aspx", OPENED),
    "eco_nps_exit": ("https://www.theweek.in/wire-updates/business/2025/12/17/dcm100-biz-pfrda-exit-norms.html", OPENED),
    # schemes
    "eco_dfs": ("https://financialservices.gov.in/", OPENED),
    "eco_standup": ("https://www.standupmitra.in/", OPENED),
    "eco_khet": ("https://newsonair.gov.in/centre-prioritises-farmers-dignity-and-better-earnings-says-agriculture-"
                 "minister-shivraj-singh-chouhan/", OPENED),
    "eco_apy_trib": ("https://www.tribuneindia.com/news/india/cabinet-approves-continuation-of-atal-pension-yojana-till-"
                     "2030-31/", OPENED),
    "eco_apy_pfrda": ("https://www.pfrda.org.in/schemes/atal-pension-yojana-apy", OPENED),
    "eco_vatsalya": ("https://www.pfrda.org.in/schemes/national-pension-system/nps-vatsalya", OPENED),
    "eco_vishwa": ("https://pmvishwakarma.gov.in/", OPENED),
    "eco_pmuy": ("https://www.pmuy.gov.in/about.html", OPENED),
})

T = "Economic Affairs"
GDP, INF, FIS, MON = ("GDP and growth projections", "Inflation data", "Fiscal data", "Monetary policy decisions")

# ------------------------------------------------------------------ Basic (1)
G(T, INF, "Basic",
  "According to data released by the National Statistics Office on 12 May 2026, India's headline retail (CPI) "
  "inflation for April 2026 was:",
  ["3.48%", "3.40%", "4.20%", "2.75%"], "*",
  "Retail (CPI) inflation, April 2026",
  "Headline CPI inflation edged up to 3.48% in April 2026 from 3.40% in March 2026, on the new series with base year "
  "2024. Food inflation rose to 4.20% from 3.87%; rural inflation was 3.74% and urban 3.16%.",
  ["April 2026 CPI inflation: 3.48% (released 12 May 2026)", "March 2026: 3.40%; food inflation April: 4.20%"],
  [fact("Headline CPI inflation 3.48% in April 2026, up from 3.40% in March; food inflation 4.20%; rural 3.74%, urban "
        "3.16%; released by NSO on 12 May 2026; base year 2024", "eco_cpi_apr"),
   fact("India's retail inflation rose marginally to 3.48% in April 2026", "eco_cpi_apr_ao")],
  why="3.40% was the March 2026 figure and 4.20% was April's food inflation; 3.48% is the headline April rate.",
  current=ca("2026-05-12"))

# ------------------------------------------------------------------ Intermediate (5)
G(T, INF, "Intermediate",
  "India's wholesale price (WPI) inflation turned positive in December 2025 after two months of deflation. What was "
  "the annual WPI inflation rate for December 2025?",
  ["0.83%", "-0.32%", "1.82%", "2.57%"], "*",
  "WPI inflation, December 2025",
  "Provisional data released on 14 January 2026 put annual WPI inflation for December 2025 at 0.83%. The index rose "
  "0.71% over November, and the food index's annual rate moved from -2.60% in November to 0.00% in December.",
  ["WPI Dec 2025: 0.83% (provisional)", "Released 14 Jan 2026", "Month-on-month rise: 0.71%"],
  [fact("Annual WPI inflation 0.83% (provisional) for December 2025; month-on-month 0.71%; food index rate from -2.60% "
        "in November to 0.00% in December; article dated 14 January 2026", "eco_wpi_dec"),
   fact("WPI inflation turned positive at 0.83% in December 2025", "eco_wpi_dec_st")],
  why="The sources give 0.83% as the December 2025 WPI rate; the other figures are not the headline December rate.",
  current=ca("2026-01-14"))

G(T, GDP, "Intermediate",
  "On 18 September 2026, Moody's revised its forecast of India's real GDP growth for the current financial year "
  "(2026-27), citing the economy's resilience to the West Asia conflict. What is the revised forecast?",
  ["7%", "6%", "6.4%", "7.4%"], "*",
  "Moody's growth forecast for India",
  "Moody's raised its real GDP growth forecast for India for the current financial year to 7% from 6%. It noted that "
  "real GDP grew 8.2% year-on-year in the first half of 2026 against 7.3% in 2025, and expects India to keep growing "
  "faster than other G20 economies.",
  ["Moody's, 18 Sep 2026: India growth raised to 7%", "Earlier forecast: 6%"],
  [fact("Moody's raised India's real GDP growth forecast to 7% for the current financial year, up from 6%; H1 2026 "
        "growth 8.2% vs 7.3% in 2025; reported 18 September 2026", "eco_moodys")],
  why="6% was Moody's earlier forecast, which it raised to 7%; 6.4% and 7.4% are not the figures in the source.",
  current=ca("2026-09-18"))

G(T, MON, "Intermediate",
  "On 5 December 2025, along with open market operation (OMO) purchases of government securities worth ₹1 lakh "
  "crore, the RBI announced a USD/INR buy/sell swap auction to inject durable liquidity. What were its size and tenor?",
  ["USD 5 billion for three years", "USD 10 billion for three years", "USD 5 billion for six months",
   "USD 10 billion for two years"], "*",
  "RBI liquidity measures, December 2025",
  "The RBI's press release of 5 December 2025 announced OMO purchases of ₹1,00,000 crore in two tranches of ₹50,000 "
  "crore (11 and 18 December 2025) and a USD 5 billion USD/INR buy/sell swap of three-year tenor, auctioned on 16 "
  "December 2025.",
  ["OMO purchases: ₹1 lakh crore in two tranches", "Swap: USD 5 billion, 3-year tenor, auction 16 Dec 2025"],
  [fact("RBI press release of 5 December 2025: OMO purchases ₹1,00,000 crore in two tranches of ₹50,000 crore on 11 "
        "and 18 December 2025; USD/INR buy/sell swap of USD 5 billion for three years on 16 December 2025",
        "eco_omo_rbi")],
  why="The RBI release specifies USD 5 billion and a three-year tenor; the other size/tenor pairs do not match it.",
  current=ca("2025-12-05"))

G(T, FIS, "Intermediate",
  "According to provisional CBDT data released in May 2026, India's net direct tax collections for 2025-26 were about "
  "₹23.40 lakh crore. Which of the following is correct about this figure?",
  ["It grew about 5.1% but fell short of the revised estimate of ₹24.21 lakh crore",
   "It grew about 12% and exceeded the budget estimate of ₹25.20 lakh crore",
   "It grew about 5.1% and exceeded the revised estimate of ₹24.21 lakh crore",
   "It fell about 1.1% from 2024-25 and missed both estimates"], "*",
  "Direct tax collections, 2025-26",
  "Net direct tax collections rose 5.12% to ₹23.40 lakh crore in 2025-26 from ₹22.26 lakh crore, missing the revised "
  "estimate of ₹24.21 lakh crore (budget estimate ₹25.20 lakh crore). Gross collections were about ₹28.12 lakh crore "
  "and refunds fell 1.09% to ₹4.71 lakh crore; net corporate tax was ₹10.99 lakh crore.",
  ["Net direct tax 2025-26: ₹23.40 lakh crore, +5.12%", "RE ₹24.21 lakh crore (missed); BE ₹25.20 lakh crore"],
  [fact("Net direct tax ₹23.40 lakh crore in FY26, up 5.12% from ₹22.26 lakh crore; RE ₹24.21 lakh crore missed; BE "
        "₹25.20 lakh crore; refunds down 1.09%; published 4 May 2026", "eco_dtax")],
  why="Collections grew 5.12% and missed the ₹24.21 lakh crore RE; the 1.09% fall relates to refunds, not net "
      "collections.",
  current=ca("2026-05-04"))

G(T, FIS, "Intermediate",
  "According to CGA data released on 31 July 2026, the Centre's fiscal deficit in April-June 2026 (Q1 of 2026-27) "
  "reached what share of the full-year Budget Estimate?",
  ["18.2%", "17.9%", "26.8%", "22.2%"], "*",
  "Centre's fiscal deficit, Q1 2026-27",
  "The fiscal deficit for April-June 2026 was ₹3,07,833 crore, or 18.2% of the 2026-27 Budget Estimate, against 17.9% "
  "in the same quarter a year earlier. Net tax revenue up to June was ₹6.36 lakh crore (22.2% of BE). The full-year "
  "target is 4.3% of GDP (₹16.96 lakh crore).",
  ["Q1 2026-27 fiscal deficit: ₹3,07,833 crore = 18.2% of BE", "Q1 2025-26: 17.9% of BE"],
  [fact("Fiscal deficit April-June 2026 at 18.2% of BE (₹3,07,833 crore); 17.9% a year earlier; net tax revenue 22.2% "
        "of BE; CGA data released 31 July 2026", "eco_fd_q1"),
   fact("India's fiscal deficit touches 18.2% of FY27 target in Q1", "eco_fd_q1_dc")],
  why="17.9% was the year-earlier Q1 share and 22.2% was net tax revenue as a share of BE; Q1 2026-27 deficit was "
      "18.2%.",
  current=ca("2026-07-31"))

# ------------------------------------------------------------------ Advanced (1)
GS(T, GDP, "Advanced",
   "the World Bank's South Asia Economic Update released on 6 October 2026",
   ["It raised India's growth forecast for FY 2026-27 to 7.1%.",
    "Its earlier forecast for India's FY 2026-27 growth, now revised, was 7.4%.",
    "It projected India's growth for FY 2027-28 at 7.2%."],
   [True, False, True],
   "World Bank forecast for India, October 2026",
   "The October 2026 South Asia Economic Update raised India's FY27 growth forecast to 7.1% from 6.6% and put FY28 "
   "growth at 7.2%. It also raised South Asia's 2026 growth forecast to 6.9% from 6.3%.",
   [fact("World Bank October 2026 South Asia Economic Update (6 October 2026): India FY27 forecast 7.1%, up from 6.6%; "
         "FY28 7.2%; South Asia 6.9% in 2026", "eco_wb_oct"),
    fact("World Bank raises India growth forecast to 7.1% for 2026-27", "eco_wb_oct_nb")],
   why="Statement 2 is wrong: the earlier forecast was 6.6%, not 7.4%.",
   current=ca("2026-10-06"))

# ====================================================================== Government Policies
T = "Government Policies"
PC, RR = "Policy changes", "Regulatory reforms"

G(T, RR, "Intermediate",
  "Under the Reserve Bank - Integrated Ombudsman Scheme (RB-IOS), 2026, which came into effect on 1 July 2026, up to "
  "how much compensation can the RBI Ombudsman award for consequential loss suffered by a complainant?",
  ["₹30 lakh", "₹20 lakh", "₹10 lakh", "₹50 lakh"], "*",
  "RBI Integrated Ombudsman Scheme, 2026",
  "RB-IOS 2026, effective 1 July 2026, removes the cap on the value of disputes an Ombudsman can handle, allows "
  "compensation of up to ₹30 lakh for consequential loss (₹20 lakh earlier) and up to ₹3 lakh for loss of time, "
  "expenses, harassment or mental anguish. It covers banks, NBFCs, non-bank PPI issuers and credit information "
  "companies.",
  ["RB-IOS 2026 effective 1 Jul 2026", "Consequential loss: up to ₹30 lakh (earlier ₹20 lakh)",
   "Harassment etc.: up to ₹3 lakh; no cap on dispute value"],
  [fact("RB-IOS 2026 effective 1 July 2026; dispute value cap removed; compensation for consequential loss up to ₹30 "
        "lakh; up to ₹3 lakh for loss of time, expenses, harassment or mental anguish", "eco_rbios_knn"),
   fact("RB-IOS 2026: compensation for consequential loss up to ₹30 lakh (previously ₹20 lakh)", "eco_rbios_vk")],
  why="₹20 lakh was the limit under the earlier scheme; the 2026 scheme raises it to ₹30 lakh.",
  current=ca("2026-07-01"))

G(T, PC, "Intermediate",
  "The Income-tax Rules, 2026, notified by the CBDT on 20 March 2026 under the Income-tax Act, 2025, reduce the number "
  "of rules from 511 under the 1962 Rules to how many?",
  ["333", "190", "399", "298"], "*",
  "Income-tax Rules, 2026",
  "The Income-tax Rules, 2026 (G.S.R. 198(E), 20 March 2026, under Section 533 of the Income-tax Act, 2025) took "
  "effect on 1 April 2026. Rules fell from 511 to 333 and forms from 399 to 190.",
  ["Notified 20 Mar 2026; effective 1 Apr 2026", "Rules: 511 -> 333", "Forms: 399 -> 190"],
  [fact("Income-tax Rules, 2026 notified 20 March 2026 (G.S.R. 198(E)) under Section 533 of the Income-tax Act, 2025; "
        "effective 1 April 2026; rules 511 to 333; forms 399 to 190", "eco_itrules")],
  why="190 is the new number of forms and 399 the old number of forms; the rules fell to 333.",
  current=ca("2026-03-20"))

G(T, PC, "Intermediate",
  "With effect from 1 April 2026, as announced in the Union Budget 2026-27, the Securities Transaction Tax (STT) on "
  "the sale of futures was raised to what rate of the traded value?",
  ["0.05%", "0.02%", "0.15%", "0.10%"], "*",
  "STT on derivatives",
  "The Union Budget 2026-27 raised STT on futures from 0.02% to 0.05%, on options premium from 0.10% to 0.15% and on "
  "exercise of options from 0.125% to 0.15%, effective 1 April 2026. STT in other segments is unchanged.",
  ["Futures: 0.02% -> 0.05%", "Options premium: 0.10% -> 0.15%", "Exercise of options: 0.125% -> 0.15%"],
  [fact("STT from 1 April 2026: futures 0.02% to 0.05%; options premium 0.10% to 0.15%; exercise of options 0.125% to "
        "0.15%; announced in Union Budget 2026-27", "eco_stt_bt")],
  why="0.02% was the old futures rate; 0.15% and 0.10% are the new and old rates on options premium.",
  current=ca("2026-04-01"))

G(T, RR, "Intermediate",
  "At its board meeting of 17 December 2025, SEBI approved new Stock Brokers Regulations. These replace SEBI (Stock "
  "Brokers) Regulations of which year?",
  ["1992", "1996", "2008", "2015"], "*",
  "SEBI Stock Brokers Regulations",
  "SEBI's board on 17 December 2025 approved a new Stock Brokers framework replacing the SEBI (Stock Brokers) "
  "Regulations, 1992, aiming at clearer language, removal of outdated provisions and easier compliance. The same "
  "meeting also lowered mutual fund base expense ratio limits and let issuers offer incentives to certain investor "
  "groups in public issues of non-convertible securities.",
  ["SEBI board: 17 Dec 2025", "New Stock Brokers Regulations replace the 1992 regulations"],
  [fact("SEBI board (published 17 December 2025) approved a new framework replacing the 1992 SEBI (Stock Brokers) "
        "Regulations; also base expense ratio changes and incentives in public issues of non-convertible securities",
        "eco_sebi_brk")],
  why="The source states that the replaced broker regulations date from 1992; the other years do not apply.",
  current=ca("2025-12-17"))

G(T, RR, "Intermediate",
  "In its Statement on Developmental and Regulatory Policies of 7 October 2026, the RBI announced interoperability "
  "among NBFC-Account Aggregators and allowed which entities to include bank deposit information in their "
  "Consolidated Account Statement (CAS) through Account Aggregators?",
  ["SEBI-regulated Depositories", "Credit information companies", "Payments banks", "Pension fund managers"], "*",
  "Account Aggregator framework",
  "The RBI's 7 October 2026 statement provides for interoperability among NBFC-AAs and lets SEBI-regulated "
  "Depositories include bank deposit account information in the CAS through NBFC-AAs, so demat holders can see "
  "holdings and deposits in one place. Implementation is expected by 31 December 2026. The statement also announced "
  "a Technical Consultative Committee for Financial Markets.",
  ["Statement dated 7 Oct 2026", "Depositories' CAS to show bank deposits via NBFC-AAs",
   "Expected implementation: 31 Dec 2026"],
  [fact("RBI Statement on Developmental and Regulatory Policies, 7 October 2026: interoperability among NBFC-AAs; SEBI-"
        "regulated Depositories can include bank deposit account information in the CAS through NBFC-AAs; expected "
        "implementation 31 December 2026; Technical Consultative Committee for Financial Markets", "eco_rbi_oct_sdrp"),
   fact("Statement on Developmental and Regulatory Policies dated 7 October 2026 listed by RBI", "eco_rbi_policy_idx")],
  why="The statement names SEBI-regulated Depositories; the other entities are not mentioned for the CAS change.",
  current=ca("2026-10-07"))

G(T, RR, "Intermediate",
  "In its Statement on Developmental and Regulatory Policies of 5 August 2026, the RBI said it would resume granting "
  "licences 'on tap', ending a pause of about two decades, to which category of banks?",
  ["Urban Co-operative Banks", "Small Finance Banks", "Payments Banks", "Regional Rural Banks"], "*",
  "Licensing of Urban Co-operative Banks",
  "The RBI's 5 August 2026 statement said it would resume issuing licences to Urban Co-operative Banks (UCBs) on an "
  "on-tap basis, after a discussion paper of 13 January 2026; draft guidelines were to follow. The statement also "
  "covered concentration risk for rural co-operative banks and a principle-based framework for interest rates on "
  "advances.",
  ["Statement dated 5 Aug 2026", "UCB licences to resume on tap after about two decades",
   "Discussion paper: 13 Jan 2026"],
  [fact("RBI statement of 5 August 2026: resume issuing UCB licences on tap, ending a two-decade pause; discussion paper "
        "13 January 2026; draft guidelines to follow", "eco_rbi_aug_sdrp")],
  why="The statement concerns Urban Co-operative Banks; it does not deal with licences for the other bank types.",
  current=ca("2026-08-05"))

GS(T, RR, "Advanced",
   "the amendments to the PFRDA (Exits and Withdrawals under the NPS) Regulations dated 12 December 2025",
   ["Non-government NPS subscribers can withdraw up to 80% of the accumulated corpus as a lump sum at exit, against 60% "
    "earlier.",
    "Subscribers can stay invested in the NPS up to the age of 85.",
    "On normal exit, government subscribers can take 60% of their accumulated pension wealth as a lump sum, with the "
    "remaining 40% used to buy an annuity."],
   [True, True, True],
   "NPS exit norms",
   "The amendments (dated 12 December 2025) let non-government subscribers take 80% of the corpus as a lump sum (20% "
   "to annuity), raise the exit age to 85 for all categories, and keep the 60:40 split for government subscribers on "
   "normal exit. Non-government subscribers with a corpus below ₹8 lakh may withdraw it fully.",
   [fact("PFRDA exit norms amended (regulations dated 12 December 2025): non-government lump sum 80% (from 60%), annuity "
         "20%; exit age 85; government subscribers 60% lump sum and 40% annuity on normal exit; corpus below ₹8 lakh "
         "fully withdrawable for non-government subscribers", "eco_nps_exit")],
   why="All three statements match the amended exit norms.",
   current=ca("2025-12-12"))

# ====================================================================== Government Schemes
T = "Government Schemes"
CS, SL = "Central schemes", "Scheme launches and changes"

G(T, SL, "Basic",
  "The LIC Bima Sakhi Yojana was launched by the Prime Minister on 9 December 2024 at which place?",
  ["Panipat, Haryana", "Varanasi, Uttar Pradesh", "Jaipur, Rajasthan", "Bhubaneswar, Odisha"], "*",
  "LIC Bima Sakhi Yojana",
  "The Department of Financial Services lists the LIC Bima Sakhi Yojana as launched by the Prime Minister at Panipat, "
  "Haryana, on 9 December 2024.",
  ["Bima Sakhi Yojana (LIC): launched 9 Dec 2024", "Place: Panipat, Haryana"],
  [fact("LIC Bima Sakhi Yojana launched by the Prime Minister in Panipat, Haryana, on 09.12.2024", "eco_dfs")],
  why="The DFS page names Panipat as the launch place; the other cities are not.")

G(T, CS, "Basic",
  "Stand-Up India facilitates bank loans for greenfield enterprises to at least one Scheduled Caste or Scheduled Tribe "
  "borrower and at least one borrower of which category per bank branch?",
  ["Woman", "Ex-serviceman", "Minority community member", "Person with disability"], "*",
  "Stand-Up India",
  "Stand-Up India facilitates composite loans (term loan plus working capital) of ₹10 lakh to ₹1 crore to at least one "
  "SC or ST borrower and at least one woman borrower per bank branch for setting up a greenfield enterprise.",
  ["Per branch: at least one SC/ST and one woman borrower", "Greenfield enterprises"],
  [fact("Stand-Up India: loans between ₹10 lakh and ₹1 crore to at least one SC/ST borrower and at least one woman "
        "borrower per bank branch for setting up a greenfield enterprise", "eco_standup")],
  why="The scheme's two target groups are SC/ST borrowers and women; the other categories are not specified.")

G(T, SL, "Intermediate",
  "The nationwide Khet Bachao Abhiyan (Rabi 2026), which promotes soil-test-based balanced use of fertilisers, was "
  "launched by Union Agriculture Minister Shivraj Singh Chouhan on 22 October 2026 at which place?",
  ["Karnal, Haryana", "Pusa, Bihar", "Sehore, Madhya Pradesh", "Ludhiana, Punjab"], "*",
  "Khet Bachao Abhiyan (Rabi 2026)",
  "Shivraj Singh Chouhan launched the nationwide Khet Bachao Abhiyan (Rabi 2026) in Karnal, Haryana, to promote "
  "sustainable agriculture, better soil health and judicious use of fertilisers based on soil testing; it runs till "
  "the end of November.",
  ["Launched 22 Oct 2026 at Karnal, Haryana", "Focus: soil health, balanced fertiliser use"],
  [fact("Khet Bachao Abhiyan (Rabi 2026) launched by Shivraj Singh Chouhan in Karnal, Haryana; nationwide; soil health "
        "and judicious fertiliser use; article dated 22 October 2026", "eco_khet")],
  why="The launch was at Karnal; the source does not mention the other places.",
  current=ca("2026-10-22"))

G(T, CS, "Intermediate",
  "Under the Mutual Credit Guarantee Scheme for MSMEs (MCGS-MSME), launched by the Finance Minister on 17 February "
  "2025, collateral-free loans of up to what amount are covered for buying machinery or equipment?",
  ["₹100 crore", "₹10 crore", "₹50 crore", "₹500 crore"], "*",
  "Mutual Credit Guarantee Scheme for MSMEs",
  "The Department of Financial Services lists MCGS-MSME, launched by the Finance Minister on 17 February 2025, as "
  "offering collateral-free loans of up to ₹100 crore for the purchase of machinery or equipment.",
  ["MCGS-MSME launched 17 Feb 2025", "Collateral-free loans up to ₹100 crore for machinery/equipment"],
  [fact("MCGS-MSME launched by the Finance Minister on 17.02.2025; collateral-free loans up to ₹100 crore for "
        "machinery or equipment", "eco_dfs")],
  why="The DFS page gives ₹100 crore as the limit; the other amounts are not.")

GS(T, SL, "Advanced",
   "the Atal Pension Yojana (APY)",
   ["In January 2026 the Union Cabinet approved its continuation up to 2030-31, along with funding for promotional and "
    "developmental activities and gap funding.",
    "Its joining age is 18 to 40 years.",
    "Since 1 October 2022, income-tax payers have been allowed to join it with a higher pension slab."],
   [True, True, False],
   "Atal Pension Yojana",
   "The Cabinet approved continuing APY up to 2030-31 with support for promotion, development and gap funding; over "
   "8.66 crore subscribers had enrolled by 19 January 2026. Joining age is 18-40, and from 1 October 2022 anyone who "
   "is or has been an income-tax payer cannot join. PFRDA administers the scheme.",
   [fact("Cabinet approved continuation of APY up to 2030-31 with funding for promotional/developmental activities and "
         "gap funding; over 8.66 crore subscribers as of 19 January 2026; article updated 21 January 2026",
         "eco_apy_trib"),
    fact("DFS: Cabinet approved continuation of APY with funding support and gap funding till 2030-31", "eco_dfs"),
    fact("APY joining age 18-40; from 1 October 2022 any citizen who is or has been an income-tax payer is not eligible "
         "to join; administered by PFRDA", "eco_apy_pfrda")],
   why="Statement 3 is wrong: since 1 October 2022 income-tax payers are barred from joining APY.",
   current=ca("2026-01-21", inferred="Tribune report updated 21 Jan 2026 says the Cabinet approved it on Wednesday"))

GS(T, CS, "Advanced",
   "NPS Vatsalya, as described by PFRDA",
   ["The account can be continued until the subscriber turns 25.",
    "The minimum contribution is ₹250 at opening and ₹250 in each financial year.",
    "Partial withdrawal is limited to 25% of the subscriber's own contributions, excluding returns."],
   [False, True, True],
   "NPS Vatsalya",
   "NPS Vatsalya, launched on 18 September 2024 and regulated by PFRDA, is opened by a parent or guardian for a minor. "
   "It needs ₹250 at opening and ₹250 each financial year, and can continue until age 21. Partial withdrawal (after a "
   "three-year lock-in) is capped at 25% of own contributions, excluding returns.",
   [fact("NPS Vatsalya launched 18 September 2024; minimum ₹250 at opening and ₹250 each financial year; can continue "
         "until age 21; partial withdrawal limited to 25% of own contributions excluding returns, after 3-year lock-in",
         "eco_vatsalya")],
   why="Statement 1 is wrong: the account can continue only until age 21.")

GS(T, CS, "Advanced",
   "the PM Vishwakarma scheme",
   ["A toolkit incentive of ₹15,000 is given as a grant.",
    "A stipend of ₹1,000 per day is paid during training.",
    "The second tranche of the collateral-free enterprise development loan is ₹2 lakh, repayable over 30 months."],
   [True, False, True],
   "PM Vishwakarma",
   "PM Vishwakarma, run by the Ministry of MSME for 18 family-based traditional trades, gives a ₹15,000 toolkit grant, "
   "a ₹500-a-day training stipend and collateral-free enterprise development loans of ₹1 lakh (18 months) and ₹2 lakh "
   "(30 months); the Government bears the credit guarantee fees.",
   [fact("PM Vishwakarma: Ministry of MSME; toolkit incentive ₹15,000; training stipend ₹500 per day; first tranche ₹1 "
         "lakh (18 months), second tranche ₹2 lakh (30 months); 18 trades", "eco_vishwa")],
   why="Statement 2 is wrong: the training stipend is ₹500 per day.")

GS(T, CS, "Advanced",
   "the Pradhan Mantri Ujjwala Yojana (PMUY)",
   ["It was launched on 1 May 2016 at Ballia, Uttar Pradesh.",
    "After approval of a further 25 lakh connections, its overall target became 10.6 crore connections.",
    "The cash assistance for a 14.2 kg cylinder connection is ₹1,150."],
   [True, True, False],
   "Pradhan Mantri Ujjwala Yojana",
   "PMUY was launched by the Prime Minister on 1 May 2016 at Ballia. Targets grew from 8 crore to 9.6 crore and 10.35 "
   "crore; a further 25 lakh connections raised the overall target to 10.6 crore. Cash assistance is ₹1,600 for a 14.2 "
   "kg connection and ₹1,150 for a 5 kg connection.",
   [fact("PMUY launched 1 May 2016 at Ballia, UP; further 25 lakh connections raise target to 10.6 crore; cash "
         "assistance ₹1,600 for 14.2 kg and ₹1,150 for 5 kg connection", "eco_pmuy")],
   why="Statement 3 is wrong: ₹1,150 is for a 5 kg connection; a 14.2 kg connection gets ₹1,600.")

# ###################################################################### part: biz (business)
# ###################################################################### part: biz
# Business and Corporate News (Basic 6 / Advanced 6): Mergers and acquisitions, Corporate partnerships
U.update({
    "biz_avendus_ob": ("https://www.outlookbusiness.com/corporate/japans-mizuho-securities-to-acquire-majority-stake-in-"
                       "avendus-capital", OPENED),
    "biz_avendus_bs": ("https://www.business-standard.com/amp/companies/news/mizuho-group-acquire-majority-stake-avendus-"
                       "capital-kkr-125121701019_1.html", SEARCH),
    "biz_intel_trib": ("https://www.tribuneindia.com/news/business/tata-intel-sign-mou-to-explore-strategic-collaboration-"
                       "for-semiconductor-and-ai-development", OPENED),
    "biz_fifth_c19": ("https://www.cleveland19.com/2026/02/02/fifth-third-completes-merger-with-comerica-form-9th-largest-"
                      "us-bank/", OPENED),
    "biz_fifth_ab": ("https://www.americanbanker.com/news/fifth-third-closes-comerica-acquisition-in-under-four-months",
                     OPENED),
    "biz_openai_print": ("https://theprint.in/business/openai-partners-tata-group-to-build-100mw-ai-data-centre-in-india/"
                         "2858521", OPENED),
    "biz_hcl_ao": ("https://www.angelone.in/news/stocks/hcltech-share-price-in-focus-completes-acquisition-of-telco-"
                   "solutions-business-from-hpe", OPENED),
    "biz_wipro_pr": ("https://www.wipro.com/newsroom/press-releases/2026/wipro-completes-acquisition-of-olam-groups-it-and-"
                     "digital-services-business-mindsprint/", OPENED),
    "biz_bajaj_week": ("https://www.theweek.in/wire-updates/business/2026/01/08/bajaj-group-completes-23-pc-stake-"
                       "acquisition-from-jv-partner-allianz-for-rs-21-390-cr.html", OPENED),
    "biz_bajaj_fpj": ("https://www.freepressjournal.in/business/bajaj-finserv-completes-allianz-buyout-takes-full-control-"
                      "of-insurance-arms", OPENED),
    "biz_kotak_db": ("https://www.db.com/news/detail/20260630-kotak-mahindra-bank-to-acquire-deutsche-bank-s-retail-"
                     "banking-private-banking-and-wealth-management-business-in-india?language_id=1", OPENED),
    "biz_kotak_open": ("https://openthemagazine.com/business/kotak-buys-deutsche-banks-india-retail-and-wealth-business-in-"
                       "2817-crore-deal", OPENED),
    "biz_kotak_cci": ("https://www.nationpathindia.com/economy/kotak-mahindra-deutsche-bank-india-business-acquisition-cci-"
                      "approval", OPENED),
    "biz_torrent_md": ("https://medicaldialogues.in/amp/news/industry/health-investments/torrent-pharma-completes-jb-"
                       "chemicals-acquisition-becomes-promoter-with-4639-stake-163220", OPENED),
    "biz_torrent_fpj": ("https://www.freepressjournal.in/business/indias-second-most-valued-pharma-torrent-"
                        "pharmaceuticals-acquires-19500-crore-majority-stake-in-jb-chemicals", OPENED),
    "biz_tcs_bt": ("https://www.businesstoday.in/tech-today/news/story/tcs-tpg-join-hands-to-build-ai-data-center-platform-"
                   "hypervault-announce-rs-18000-cr-investment-503087-2025-11-20", OPENED),
    "biz_tcs_ob": ("https://www.outlookbusiness.com/corporate/tcs-signs-up-with-tpg-for-18000-cr-data-centre-play-pe-firm-"
                   "commits-8820-cr", SEARCH),
    "biz_bain_dt": ("https://www.dtnext.in/news/business/bain-capital-gets-rbi-nod-for-control-of-manappuram-finance-its-"
                    "subsidiaries", OPENED),
    "biz_bain_mb": ("https://www.multibagg.ai/market-pulse/articles/manappuram-finance-bain-open-offer-"
                    "cmpe5fswo93exlb0j6fgp255n", OPENED),
    "biz_bain_om": ("https://onmanorama.com/news/business/2025/03/21/bain-capital-acquires-kerala-manappuram-finance-open-"
                    "offer.html", OPENED),
    "biz_ajre_az": ("https://www.allianz.com/en/mediacenter/news/media-releases/financials/260326-allianz-jio-reinsurance-"
                    "limited-commences-operations.html", OPENED),
    "biz_ajre_fpj": ("https://www.freepressjournal.in/business/jio-financial-services-secures-irdai-registration-for-"
                     "allianz-jio-reinsurance-venture-in-march-2026", SEARCH),
})

T = "Business and Corporate News"
MA, CP = "Mergers and acquisitions", "Corporate partnerships"

# ------------------------------------------------------------------ Basic (6)
G(T, MA, "Basic",
  "Mizuho Securities, part of Japan's Mizuho Financial Group, announced on 17 December 2025 that it would acquire a "
  "majority stake in which Indian investment bank, buying out KKR-backed Redpoint Investments?",
  ["Avendus Capital", "JM Financial", "Equirus Capital", "Ambit Capital"], "*",
  "Mizuho-Avendus deal",
  "Mizuho Securities agreed to buy between 61.6% and 78.3% of Avendus Capital from Redpoint Investments (backed by KKR) "
  "and co-founder Ranu Vohra, making Avendus its consolidated subsidiary. Avendus keeps its brand, and founders Gaurav "
  "Deepak and Kaushal Aggarwal continue to lead it.",
  ["Buyer: Mizuho Securities (Japan)", "Target: Avendus Capital, 61.6%-78.3%", "Seller: KKR-backed Redpoint + Ranu Vohra"],
  [fact("Mizuho Securities to acquire 61.6%-78.3% of Avendus Capital; announced 17 Dec 2025; sellers Redpoint Investments "
        "(KKR-backed) and co-founder Ranu Vohra; Avendus retains brand", "biz_avendus_ob"),
   fact("Japan's Mizuho Group to acquire over 60% stake in Avendus Capital from KKR", "biz_avendus_bs")],
  why="The sources name Avendus Capital as the target; the other firms are not part of this deal.",
  current=ca("2025-12-17"))

G(T, CP, "Basic",
  "On 8 December 2025 the Tata Group signed an MoU with which US chipmaker to explore manufacturing and packaging of its "
  "products at Tata Electronics' upcoming semiconductor fab and OSAT facilities in India?",
  ["Intel", "Micron Technology", "Qualcomm", "AMD"], "*",
  "Tata-Intel semiconductor MoU",
  "Tata and Intel signed an exploratory MoU covering manufacturing and packaging of Intel hardware at Tata Electronics' "
  "upcoming fab and OSAT units, advanced packaging in India and scaling AI PC products. It was welcomed by Tata Sons "
  "Chairman N. Chandrasekaran and Intel CEO Lip-Bu Tan.",
  ["Partners: Tata Group + Intel", "Date: 8 Dec 2025", "Scope: fab/OSAT manufacturing, packaging, AI PCs"],
  [fact("Tata Group and Intel sign MoU, announced 8 Dec 2025, to explore manufacturing and packaging of Intel products at "
        "Tata Electronics' upcoming fab and OSAT facilities; quotes from N Chandrasekaran and Lip-Bu Tan",
        "biz_intel_trib")],
  why="The MoU of 8 December 2025 was signed with Intel; the sources do not name Micron, Qualcomm or AMD.",
  current=ca("2025-12-08"))

G(T, MA, "Basic",
  "Fifth Third Bancorp completed its all-stock acquisition of which US bank on 1 February 2026, creating the "
  "ninth-largest bank in the United States with about USD 294 billion in assets?",
  ["Comerica", "KeyCorp", "Zions Bancorporation", "Regions Financial"], "*",
  "Fifth Third-Comerica merger",
  "Fifth Third closed its acquisition of Comerica on Sunday, 1 February 2026, less than four months after the deal was "
  "announced. The deal was worth about USD 10.9 billion at announcement and was the largest US bank merger announced in "
  "2025. The combined bank, headquartered in Cincinnati and led by Tim Spence, has about USD 294 billion in assets.",
  ["Acquirer: Fifth Third", "Target: Comerica", "Closed: 1 Feb 2026; about USD 10.9 billion"],
  [fact("Fifth Third completes merger with Comerica to form 9th largest U.S. bank; about $294 billion assets; $10.9 "
        "billion all-stock; HQ Cincinnati; CEO Tim Spence", "biz_fifth_c19"),
   fact("Fifth Third closed the Comerica acquisition on Sunday, 1 February 2026; $10.9 billion; largest bank merger "
        "announced in 2025", "biz_fifth_ab")],
  why="The sources name Comerica as the bank acquired; KeyCorp, Zions and Regions were not part of the deal.",
  current=ca("2026-02-01"))

G(T, CP, "Basic",
  "Under the OpenAI-Tata Group partnership announced in February 2026, TCS is to build an AI data centre in India with "
  "what initial capacity, which may later be scaled up to 1 GW?",
  ["100 MW", "50 MW", "250 MW", "500 MW"], "*",
  "OpenAI-Tata partnership",
  "OpenAI partnered with the Tata Group while Sam Altman was in India for an AI summit. TCS will build a 100 MW data "
  "centre that may be expanded to 1 GW, and several thousand Tata Group employees will get ChatGPT Enterprise.",
  ["Partners: OpenAI + Tata Group", "TCS data centre: 100 MW, expandable to 1 GW"],
  [fact("OpenAI partners Tata Group; TCS to build 100 MW data centre, may expand to 1 GW; Tata employees get ChatGPT "
        "Enterprise; report dated 19 Feb 2026", "biz_openai_print")],
  why="The initial capacity reported is 100 MW; 1 GW is the possible later scale.",
  current=ca("2026-02-19"))

G(T, MA, "Basic",
  "HCLTech completed on 1 August 2026 its acquisition of the Telco Solutions business of which company, in an all-cash "
  "deal worth up to USD 160 million?",
  ["Hewlett Packard Enterprise", "Nokia", "Ericsson", "Cisco Systems"], "*",
  "HCLTech-HPE Telco Solutions deal",
  "HCLTech first disclosed the deal on 18 December 2025 and completed it on 1 August 2026. It is an all-cash asset "
  "carve-out worth up to USD 160 million (including a USD 15 million performance incentive) that adds OSS, 5G "
  "subscriber data management and AI-driven autonomous networking capabilities and about 1,500 specialists.",
  ["Acquirer: HCLTech", "Seller: HPE (Telco Solutions business)", "Completed: 1 Aug 2026; up to USD 160 million"],
  [fact("HCLTech completed acquisition of Telco Solutions business from Hewlett Packard Enterprise on 1 Aug 2026; "
        "announced 18 Dec 2025; up to $160 million incl. $15 million incentive; all-cash asset carve-out",
        "biz_hcl_ao")],
  why="The sources name Hewlett Packard Enterprise as the seller; Nokia, Ericsson and Cisco were not involved.",
  current=ca("2026-08-01"))

G(T, MA, "Basic",
  "Wipro completed on 15 May 2026 its acquisition of Mindsprint, the IT and digital services business of which "
  "Singapore-headquartered food and agri-business group?",
  ["Olam Group", "Wilmar International", "Sembcorp Industries", "Keppel"], "*",
  "Wipro-Mindsprint deal",
  "Wipro announced the deal on 6 April 2026 and completed it on 15 May 2026 after regulatory approvals. Mindsprint, with "
  "over 3,200 professionals, is now a wholly owned subsidiary ('Mindsprint, a Wipro Company'). The deal is part of an "
  "eight-year transformation engagement Wipro won from Olam Group, whose majority owner is Temasek.",
  ["Acquirer: Wipro", "Target: Mindsprint (Olam Group's IT arm)", "Completed: 15 May 2026"],
  [fact("Wipro completes acquisition of Olam Group's IT and digital services business Mindsprint, 15 May 2026; announced "
        "6 April 2026; Olam Group Singapore-headquartered food and agri-business, majority owned by Temasek; 3,200+ "
        "professionals", "biz_wipro_pr")],
  why="Wipro's release names Olam Group as Mindsprint's parent; the other groups are not involved.",
  current=ca("2026-05-15"))

# ------------------------------------------------------------------ Advanced (6)
GS(T, MA, "Advanced", "the Bajaj group's purchase of Allianz SE's stake in its insurance companies, completed on 8 January 2026",
   ["Bajaj Finserv, Bajaj Holdings & Investment and Jamnalal Sons together bought a 23% stake for about ₹21,390 crore.",
    "The deal raised the Bajaj group's holding in the two insurers from 74% to 97% and ended a 24-year joint venture "
    "with Allianz.",
    "After the deal the two insurers took the names Bajaj Allianz General Insurance and Bajaj Allianz Life Insurance."],
   [True, True, False],
   "Bajaj-Allianz insurance deal",
   "The Bajaj group completed the purchase of Allianz SE's 23% stake (₹12,190 crore for the general insurer and ₹9,200 "
   "crore for the life insurer), taking its holding from 74% to 97%; Bajaj Finserv alone holds 75.01%. Allianz's "
   "remaining 3% was to go through a buyback. Described as the largest transaction in India's insurance sector, it ended "
   "a 24-year joint venture. The insurers had already been rebranded in October 2025 as Bajaj General Insurance and "
   "Bajaj Life Insurance.",
   [fact("8 Jan 2026: Bajaj Finserv with Bajaj Holdings & Investment and Jamnalal Sons completed acquisition of 23% from "
         "Allianz SE; Rs 12,190 crore + Rs 9,200 crore = Rs 21,390 crore; group 74% to 97%; ends 24-year JV; rebranded in "
         "Oct 2025 as Bajaj General Insurance and Bajaj Life Insurance", "biz_bajaj_week"),
    fact("Bajaj Finserv 75.01%; largest transaction in India's insurance sector; remaining 3% via buyback",
         "biz_bajaj_fpj")],
   why="Statement 3 is wrong: the insurers were rebranded in October 2025 as Bajaj General Insurance and Bajaj Life "
       "Insurance, dropping the Allianz name.",
   current=ca("2026-01-08"))

GS(T, MA, "Advanced", "Kotak Mahindra Bank's agreement of 30 June 2026 with Deutsche Bank",
   ["With this sale Deutsche Bank exits all its businesses in India, including its corporate and investment bank.",
    "Kotak is acquiring Deutsche Bank's India retail banking, affluent private banking and wealth management business "
    "through a slump sale for a cash consideration of about ₹281.7 crore.",
    "The Competition Commission of India approved the acquisition on 3 November 2026, and closing is expected by "
    "September 2027."],
   [False, True, True],
   "Kotak-Deutsche Bank India retail deal",
   "Kotak signed a business transfer agreement with Deutsche Bank AG's India branch on 30 June 2026 to buy the retail, "
   "affluent private banking and wealth business as a going concern (slump sale) for about ₹281.7 crore in cash plus "
   "the net funding position at closing. The business has loans of about ₹29,000 crore, deposits of about ₹16,000 "
   "crore, AUM of about ₹10,500 crore, about 1.5 lakh customers and about 1,000 employees. The CCI approved it on 3 "
   "November 2026; closing is expected by September 2027. Deutsche Bank keeps its Corporate Bank, Investment Bank and "
   "other Indian businesses.",
   [fact("30 June 2026 definitive agreement; retail, affluent private banking and wealth business; loans ~INR 29,000 cr, "
         "deposits ~INR 16,000 cr, AUM ~INR 10,500 cr, ~150,000 customers, ~1,000 employees; closing by Sept 2027; "
         "Deutsche Bank continues Corporate Bank, Investment Bank, DWS etc. in India", "biz_kotak_db"),
    fact("Slump sale; consideration about Rs 281.7 crore in cash plus net funding position", "biz_kotak_open"),
    fact("CCI approved Kotak's acquisition on 3 November 2026", "biz_kotak_cci")],
   why="Statement 1 is wrong: Deutsche Bank keeps its Corporate Bank, Investment Bank, DWS and other businesses in India.",
   current=ca("2026-06-30"))

GS(T, MA, "Advanced", "Torrent Pharmaceuticals' acquisition of J B Chemicals & Pharmaceuticals, completed in January 2026",
   ["Torrent acquired a 46.39% stake (fully diluted) from Tau Investment Holdings, at ₹1,600 per share, and was "
    "classified as a promoter.",
    "Under the planned merger, J B Chemicals shareholders are to receive 100 Torrent shares for every 51 J B Chemicals "
    "shares.",
    "The deal is described as the second-biggest in India's pharma sector, after Sun Pharma's acquisition of Ranbaxy."],
   [True, False, True],
   "Torrent-JB Chemicals deal",
   "Torrent bought 46.39% of J B Chemicals (fully diluted) from Tau Investment Holdings under an agreement "
   "of 29 June 2025, at ₹1,600 per share (about ₹11,917 crore), and became a promoter on 21 January 2026. The equity "
   "valuation is ₹25,689 crore. J B Chemicals is to merge into Torrent at 51 Torrent shares for every 100 J B "
   "Chemicals shares. The deal is described as the second-biggest pharma deal after Sun Pharma-Ranbaxy (2015).",
   [fact("Torrent completed acquisition 21 Jan 2026; 46.39% fully diluted from Tau Investment Holdings Pte Ltd; became "
         "promoter; SPA dated 29 June 2025", "biz_torrent_md"),
    fact("Rs 1,600 per share; Rs 11,917 crore for 46.39%; equity valuation Rs 25,689 crore; swap ratio 51 Torrent shares "
         "for 100 JB shares; second-biggest pharma deal after Sun Pharma-Ranbaxy", "biz_torrent_fpj")],
   why="Statement 2 reverses the swap ratio: J B Chemicals shareholders get 51 Torrent shares for every 100 J B "
       "Chemicals shares.",
   current=ca("2026-01-21"))

GS(T, CP, "Advanced", "the partnership between TCS and TPG for HyperVault announced on 20 November 2025",
   ["TCS and TPG together will commit up to ₹18,000 crore over the next few years through equity and debt.",
    "TPG will invest up to ₹8,820 crore and is expected to hold between 27.5% and 49% of the venture.",
    "HyperVault Data Centers was incorporated on 30 October 2025 as a wholly owned subsidiary of TCS."],
   [True, True, True],
   "TCS-TPG HyperVault partnership",
   "TCS brought in TPG as partner for its AI data-centre platform HyperVault, which builds liquid-cooled, high-density "
   "data centres for hyperscalers, AI firms, enterprises and the public sector. The two will commit up to ₹18,000 crore "
   "through a mix of equity and debt; TPG's share is up to ₹8,820 crore for 27.5% to 49%. HyperVault was set up on 30 "
   "October 2025 as a wholly owned TCS subsidiary.",
   [fact("20 Nov 2025: TCS and TPG to commit up to Rs 18,000 crore; TPG up to Rs 8,820 crore for 27.5%-49%; equity and "
         "debt; HyperVault Data Centers incorporated 30 Oct 2025 as wholly owned TCS subsidiary", "biz_tcs_bt"),
    fact("TCS signs up with TPG for Rs 18,000 cr data centre play; PE firm commits Rs 8,820 cr", "biz_tcs_ob")],
   why="All three statements match the reported terms of the partnership.",
   current=ca("2025-11-20"))

GS(T, MA, "Advanced", "Bain Capital's acquisition of joint control of Manappuram Finance, completed in April 2026",
   ["Bain Capital replaced the existing promoters and became the sole promoter of Manappuram Finance.",
    "Bain Capital invested about ₹4,385 crore through a preferential issue of equity shares and warrants.",
    "The mandatory open offer for up to 26% was priced at ₹236 per share."],
   [False, True, True],
   "Bain Capital-Manappuram Finance deal",
   "Bain Capital affiliates (BC Asia Investments XIV and XXV) invested about ₹4,385 crore through a preferential issue of "
   "shares and warrants, completed on 27 March 2026, after RBI approvals in March 2026. The open offer at ₹236 per share "
   "for up to 26% ran from 6 to 20 April 2026, and the investors acquired control on 21 April 2026. Bain holds 18% to "
   "41.66% (fully diluted) and shares joint control with the existing promoters, who hold 28.9%.",
   [fact("Bain Capital to be classified as promoter with joint control with existing promoters; investment about Rs 4,385 "
         "crore; 18.0%-41.66% fully diluted; existing promoters 28.9%; subsidiaries Asirvad Micro Finance and Manappuram "
         "Home Finance", "biz_bain_dt"),
    fact("Preferential issue of equity shares and warrants completed 27 March 2026; open offer 6-20 April 2026; control "
         "acquired 21 April 2026", "biz_bain_mb"),
    fact("Open offer price Rs 236 per share for up to 26%, about Rs 5,764 crore", "biz_bain_om")],
   why="Statement 1 is wrong: Bain Capital holds joint control along with the existing promoters, who keep 28.9%.",
   current=ca("2026-04-21"))

GS(T, CP, "Advanced", "Allianz Jio Reinsurance Limited, which began operations in March 2026",
   ["It is a 50:50 joint venture between Jio Financial Services and the Allianz Group, which holds its stake through "
    "Allianz Europe B.V.",
    "It received its final IRDAI approval in July 2025 and started underwriting in the same month.",
    "It is headquartered in Mumbai and its CEO is Sonia Rawal."],
   [True, False, True],
   "Allianz Jio Re",
   "Allianz Jio Reinsurance Limited, a 50:50 joint venture of Jio Financial Services and Allianz (through Allianz Europe "
   "B.V.), received final IRDAI approval on 12 March 2026 and announced on 26 March 2026 that it had begun underwriting "
   "reinsurance in India. It is based in Mumbai and led by CEO Sonia Rawal. The two partners also signed a non-binding "
   "agreement to explore general and life insurance.",
   [fact("Allianz Jio Re commences operations, 26 Mar 2026; 50:50 JV of JFSL and Allianz via Allianz Europe B.V.; final "
         "IRDAI approval 12 Mar 2026; Mumbai; CEO Sonia Rawal", "biz_ajre_az"),
    fact("Jio Financial Services secures IRDAI registration for Allianz Jio Reinsurance venture in March 2026",
         "biz_ajre_fpj")],
   why="Statement 2 is wrong: final IRDAI approval came on 12 March 2026, and operations began later that month.",
   current=ca("2026-03-26"))


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
    "notes": "BATCH_006 General Awareness part: 150 original questions. Current-affairs topics (National and "
             "International Current Affairs, Appointments, Awards, Sports, Summits, Economic Affairs, Business) test "
             "events dated 2025-11-01 to 2026-11-04, with event dates from the sources and review_by 2027-05-05. "
             "Other time-sensitive facts also carry current_affairs dates. No fact or event tested in BATCH_000 to "
             "BATCH_005 GA is tested again. Fact checks dated 2026-11-05; verified_by says whether each question's "
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
