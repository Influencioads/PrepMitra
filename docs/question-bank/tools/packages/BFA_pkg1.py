"""Writes the three fragment files of Banking and Financial Awareness topic package 1 (batches 008, 009 and 010):
    batches/parts/frag/BATCH_008_BFA_pkg1.json   (64 questions, BANK_BFA_001404 - 001467)
    batches/parts/frag/BATCH_009_BFA_pkg1.json   (65 questions, BANK_BFA_001603 - 001667)
    batches/parts/frag/BATCH_010_BFA_pkg1.json   (68 questions, BANK_BFA_001802 - 001869)
Topics: Banking Fundamentals, History of Banking in India, Reserve Bank of India, RBI Functions, Monetary Policy, Repo
Rate, Reverse Repo Rate, CRR, SLR, Bank Rate, Inflation.

Structure follows tools/batch_006/banking.py. Every fact is backed by a fact_check whose source was opened on
2026-11-06 (HTML pages fetched with a plain client and read; PDFs downloaded and their text extracted), or, where only
search results stated it (no block was worked around: rbidocs PDFs that show a bot check were not used), by search
results, in which case the question carries web:search-confirmed. Only rules in force on 2026-11-06 are tested: the
consolidated Commercial Banks Directions of 28 November 2025 (Interest Rate on Deposits, Interest Rates on Advances,
Voluntary Amalgamation), the liquidity management framework of 30 September 2025, the current RBI FAQs; older rules
appear only as explicitly historical facts (RBI's chronology and rate tables). No draft is tested. Questions on a dated
event or a value that can change carry current_affairs with the date stated by the source (every Repo Rate question
carries one, as the validator requires). Every computable answer is re-derived below with assertions; the per-batch
quota per (topic, difficulty), the ID ranges and the key balance are checked against
batches/plans/packages/BFA_pkg1.json before anything is written. All earlier questions of these topics (BATCH_000
sample and BATCH_001-006 Banking parts, plus BATCH_007 if its part file exists) were read first; their facts are not
repeated. ai:independent-check is added only to questions in INDEPENDENT, which a separate fresh solver answered blind
(stem and options only) and matched with confidence.

    python tools/packages/BFA_pkg1.py      (run from anywhere)
"""

import json
import random
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-05"      # verified_at / created_at, as the brief fixes
CHECKED = "2026-11-06"    # the day the sources were actually opened
REVIEW_BY = "2027-05-05"
LETTERS = "ABCD"
BF = "Banking and Financial Awareness"
SECONDS = {"Basic": 20, "Intermediate": 30, "Advanced": 60}
PKG = json.loads((ROOT / "batches" / "plans" / "packages" / "BFA_pkg1.json").read_text(encoding="utf-8"))
BATCHES = ("008", "009", "010")

_rng = random.Random(2026110601)
_keys = {b: Counter() for b in BATCHES}
QS = {b: [] for b in BATCHES}

# Question IDs that a separate fresh solver answered blind (stem and options only, every second question of each
# fragment: 99 questions) and matched with high confidence. All 99 answers matched the key; 83 were high confidence
# (tagged); the 16 medium-confidence matches are not tagged. No question was changed after the check.
INDEPENDENT = {f"BANK_BFA_{n:06d}" for n in (
    1404, 1406, 1410, 1414, 1416, 1418, 1420, 1422, 1424, 1426, 1428, 1430, 1436, 1438, 1440, 1444, 1446, 1448,
    1450, 1452, 1456, 1460, 1462, 1464, 1466, 1603, 1605, 1607, 1609, 1611, 1615, 1617, 1619, 1621, 1625, 1627,
    1629, 1631, 1633, 1635, 1637, 1639, 1641, 1643, 1647, 1649, 1651, 1655, 1657, 1659, 1661, 1665, 1667, 1802,
    1804, 1806, 1808, 1810, 1812, 1814, 1816, 1820, 1822, 1824, 1826, 1828, 1830, 1832, 1836, 1838, 1840, 1842,
    1846, 1848, 1850, 1852, 1854, 1856, 1860, 1862, 1864, 1866, 1868)}

# URLs confirmed only through search results.
SEARCH_ONLY = set()


def fact(claim, url):
    return {"claim": claim, "source_url": url, "checked_on": CHECKED}


def ca(event_date, review_by=REVIEW_BY):
    return {"event_date": event_date, "review_by": review_by}


def Q(b, topic, subtopic, difficulty, text, options, answer=None, *, concept, explanation, steps, facts, why,
      seconds=None, computed=False, current=None, shortcut=None):
    """Adds one question to batch b. With answer=None, options[0] is the correct text and it is placed at the
    least-used key of that batch so far (random tie-break, fixed seed)."""
    assert b in BATCHES
    assert len(options) == 4 and len(set(options)) == 4, text
    assert facts and why and steps, text
    keys = _keys[b]
    if answer is None:
        low = min(keys[k] for k in LETTERS)
        pos = LETTERS.index(_rng.choice([k for k in LETTERS if keys[k] == low]))
        correct, wrongs = options[0], list(options[1:])
        options = wrongs[:pos] + [correct] + wrongs[pos:]
        answer = LETTERS[pos]
    assert answer in LETTERS
    keys[answer] += 1
    QS[b].append({
        "exam_mappings": default_mappings(BF, difficulty),
        "subject": BF, "topic": topic, "subtopic": subtopic, "difficulty": difficulty,
        "question_type": "MCQ", "language": "en",
        "question_text": text,
        "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(options)],
        "correct_answer": answer,
        "solution": {"concept": concept, "explanation": explanation, "steps": steps, "shortcut": shortcut,
                     "why_others_wrong": why,
                     "final_answer": f"Option {answer}: {options[LETTERS.index(answer)]}"},
        "suggested_time_seconds": seconds or (90 if computed and difficulty == "Advanced" else SECONDS[difficulty]),
        "_current": current, "_computed": computed, "_facts": facts,
    })


# ============================================================================================ sources
# All fetched with a plain client and read on 2026-11-06 unless added to SEARCH_ONLY.
_P = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid="
_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id="
CH26 = "https://rbi.org.in/history/Brief_Chro1926to1935.html"
CH35 = "https://rbi.org.in/history/Brief_Chro1935to1949.html"
CH50 = "https://rbi.org.in/history/Brief_Chro1950to1960.html"
CH60 = "https://rbi.org.in/history/Brief_Chro1960to1971.html"
CH68 = "https://rbi.org.in/history/Brief_Chro1968to1985.html"
CH85 = "https://rbi.org.in/history/Brief_Chro1985to1991.html"
CH91 = "https://rbi.org.in/history/Brief_Chro1991to2000.html"
CH00 = "https://rbi.org.in/history/Brief_Chro2000_Onwards.html"
RATES = "https://www.rbi.org.in/commonman/english/history/Scripts/BankrateCRRandSLRChanges.aspx"
GOVS = "https://www.rbi.org.in/Scripts/governors.aspx"
ANEC = "https://www.rbi.org.in/Scripts/Anecdotes.aspx"
MPF = "https://www.rbi.org.in/scripts/FS_Overview.aspx?fn=2752"          # Monetary Policy overview page
HOME = "https://www.rbi.org.in/"                                          # Current Rates panel
ORG = "https://www.rbi.org.in/commonman/english/Scripts/Organisation.aspx"
CUR = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id=136"            # FAQs on Indian currency
GOVB = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id=61"            # RBI as banker to Government
CHQ = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id=175"            # FAQs on cheque clearing (Jan 2026)
DEP = _MD + "13157"       # CB - Interest Rate on Deposits Directions, 2025 (updated 1 Oct 2026)
ADV = _MD + "13149"       # CB - Interest Rates on Advances Directions, 2025
AMAL = _MD + "13165"      # CB - Voluntary Amalgamation Directions, 2025
CONSOL = _P + "61705"     # Consolidated Master Directions, 28 Nov 2025
LMF = _P + "61317"        # Revised Liquidity Management Framework, 30 Sep 2025
CRR25 = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12858&Mode=0"   # CRR cut notification, June 2025
MPC_OCT25 = _P + "61332"
MPC_DEC25 = _P + "61749"
LIQ_DEC5 = _P + "61751"
LIQ_DEC23 = _P + "61875"
MIN_FEB26 = _P + "62261"  # minutes (with resolution) of the 59th MPC meeting
MPC_APR26 = _P + "62514"
MPC_JUN26 = _P + "62863"
MPC_AUG26 = _P + "63287"
MPC_OCT26 = _P + "63742"
GOV_OCT26 = _P + "63744"
WMA_H2 = _P + "63670"
ED_USHA = _P + "61718"
BOARD620 = _P + "61854"
RRB_SCHED = _P + "61728"
MODEL_COOP = _P + "61726"
CPI_SEP26 = ("https://www.mospi.gov.in/uploads/latestreleasesfiles/1791801549227-Press%20Release%20for%20the%20month%20"
             "of%20September,%202026.pdf")
WPI_SEP26 = "https://eaindustry.nic.in/press_release/press_release_202609.pdf"
WPI_AUG26 = "https://eaindustry.nic.in/press_release/press_release_202608.pdf"

JALAN = _P + "47983"      # Central Board accepts Bimal Jalan Committee recommendations, 26 Aug 2019
BOARD621 = _P + "62270"
BOARD622 = _P + "62408"
DG_PORTF = _P + "62682"
DG_JAIN = _P + "62670"
ED_GUNVEER = _P + "62763"
GNCTD = _P + "61973"
WMA_STATES = _P + "62011"
RRB_SCHED2 = _P + "62181"

# ============================================================================================ History of Banking
T = "History of Banking in India"
Q("008", T, "Nationalisation", "Basic",
  "According to RBI's profile of its Governors, during whose tenure as Governor were six private sector banks "
  "nationalised (April 1980) and priority sector lending targets introduced?",
  ["Dr. I. G. Patel", "M. Narasimham", "Dr. Manmohan Singh", "K. R. Puri"],
  concept="Second round of bank nationalisation",
  explanation="Dr. I. G. Patel was Governor from 1 December 1977 to 15 September 1982. RBI's profile records that his "
              "tenure saw the nationalisation of six private sector banks (15 April 1980), the introduction of "
              "priority sector lending targets and the merger of the Deposit Insurance and Credit Guarantee "
              "Corporations.",
  steps=["April 1980 lies in 1977–1982", "Governor then: Dr. I. G. Patel"],
  why="M. Narasimham served only May–November 1977; Dr. Manmohan Singh took over in September 1982; K. R. Puri served "
      "1975–77, when RRBs were set up.",
  facts=[fact("Dr. I G Patel, 01-12-1977 to 15-09-1982: During his tenure six private sector banks were nationalised, "
              "targets for priority sector lending introduced", GOVS),
         fact("15 Apr 1980: Six private sector banks nationalised", CH68)])
Q("008", T, "Committees", "Basic",
  "The 'Committee on Reform of the Insurance Sector', set up in 1994, was chaired by:",
  ["R. N. Malhotra", "M. Narasimham", "S. Chakravarty", "C. Rangarajan"],
  concept="Committees of the reform era",
  explanation="RBI's chronology for 1991–2000 lists the 1994 'Committee on Reform of the Insurance Sector' under R. N. "
              "Malhotra, a former RBI Governor (1985–1990). Its report paved the way for opening insurance to the "
              "private sector.",
  steps=["1994, insurance sector reform → R. N. Malhotra Committee"],
  why="Narasimham chaired the financial-system committees of 1991 and 1998; Chakravarty reviewed the monetary system "
      "(1985); Rangarajan was RBI Governor in 1994.",
  facts=[fact("1994: 'Committee on Reform of the Insurance Sector', RN Malhotra", CH91)])
Q("008", T, "Mergers and consolidation", "Basic",
  "RBI's Commercial Banks – Voluntary Amalgamation Directions, 2025, which govern the merger of one banking company "
  "with another, are issued under which section of the Banking Regulation Act, 1949 (along with Section 35A)?",
  ["Section 44A", "Section 45", "Section 22", "Section 26A"],
  concept="Statutory basis of voluntary bank mergers",
  explanation="Voluntary amalgamation of banking companies is governed by Section 44A of the Banking Regulation Act, "
              "1949. RBI's 2025 Directions are issued under Sections 44A and 35A, and the scheme approved by "
              "shareholders is submitted to RBI for sanction.",
  steps=["Voluntary amalgamation of banking companies → BR Act Section 44A"],
  why="Section 45 deals with RBI-framed (compulsory) schemes of reconstruction or amalgamation; Section 22 is "
      "licensing; Section 26A is the DEA Fund.",
  facts=[fact("In exercise of the powers conferred by Section 44A and Section 35A of the Banking Regulation Act, 1949 ... "
              "RBI ... hereby issues the Directions (Commercial Banks - Voluntary Amalgamation Directions, 2025)", AMAL)])
Q("008", T, "Mergers and consolidation", "Intermediate",
  "Under Section 44A(3) of the Banking Regulation Act, 1949, as set out in RBI's Voluntary Amalgamation Directions, "
  "2025, what is a shareholder who voted against a bank merger entitled to once RBI sanctions the scheme?",
  ["To claim, within three months of the sanction, the value of his shares as determined by RBI, which is final",
   "To block the merger if he holds more than 10% of the shares",
   "To claim, within one year, the market price of his shares on the date of sanction",
   "To approach the NCLT within 30 days to have the share value fixed afresh"],
  concept="Rights of dissenting shareholders",
  explanation="A dissenting shareholder may, within three months from the date of RBI's sanction, claim from the bank "
              "concerned the value of his shares as determined by RBI while sanctioning the scheme. RBI's "
              "determination is final for all purposes.",
  steps=["Scheme sanctioned by RBI", "Dissenter claims value within 3 months", "Value fixed by RBI – final"],
  why="A single dissenter cannot block a scheme passed by the required majority; the period is three months, not a "
      "year; the value is fixed by RBI, not re-fixed by the NCLT.",
  facts=[fact("In terms of Section 44A (3) of the Banking Regulation Act, 1949, a dissenting shareholder is entitled, in "
              "the event of the scheme being sanctioned by RBI, to claim within three months from the date of sanction "
              "... the value of the shares ... as determined by RBI when sanctioning the scheme. Such determination by "
              "the RBI of the value of the shares shall be final for all purposes", AMAL)])
Q("008", T, "Nationalisation", "Advanced",
  "Consider the following statements based on RBI's history of its Governors and its chronology:\n"
  "I. The nationalisation of 14 major commercial banks in 1969 did not have the endorsement of the Reserve Bank.\n"
  "II. An Agricultural Credit Board, with the RBI Governor as Chairman, was set up in 1970 to formulate and review "
  "rural credit policies.\n"
  "III. The Credit Guarantee Corporation of India was set up before the 1969 nationalisation to guarantee bank loans "
  "to small borrowers.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="The nationalisation era",
  explanation="RBI's profile of Governor L. K. Jha says the 1969 nationalisation was 'a step which did not have the "
              "endorsement of the Reserve Bank' (I). The Agricultural Credit Board, chaired by the Governor, was set up "
              "in February 1970 (II). The Credit Guarantee Corporation of India was established on 14 January 1971, "
              "after nationalisation, so III is wrong.",
  steps=["I: true (Jha profile)", "II: true (Feb 1970)", "III: false – CGCI set up 14 Jan 1971"],
  why="Any option containing III is wrong; 'I only' leaves out the true statement II.",
  facts=[fact("14 major commercial banks were nationalised in 1969, a step which did not have the endorsement of the "
              "Reserve Bank", GOVS),
         fact("Feb 1970: The Agricultural Credit Board set up with Governor as Chairman to formulate and review policies "
              "in the sphere of rural credit; 14 Jan 1971: Credit Guarantee Corporation of India Ltd. established", CH68)])

Q("009", T, "Committees", "Basic",
  "RBI's Expert Committee to Review the Extant Economic Capital Framework, whose recommendations the Central Board "
  "accepted in August 2019, was chaired by:",
  ["Dr. Bimal Jalan", "Dr. Urjit R. Patel", "Dr. Y. V. Reddy", "M. Narasimham"],
  concept="Committee on RBI's economic capital",
  explanation="The Expert Committee to Review the Extant Economic Capital Framework of RBI was chaired by former Governor "
              "Dr. Bimal Jalan. On 26 August 2019 the Central Board accepted all its recommendations and finalised the "
              "2018-19 accounts under the revised framework.",
  steps=["Economic Capital Framework review (2019) → Bimal Jalan Committee"],
  why="Dr. Urjit Patel chaired the 2014 committee on the monetary policy framework; Narasimham chaired the 1991 and "
      "1998 banking committees; Dr. Reddy did not chair this committee.",
  facts=[fact("An Expert Committee to Review the Extant Economic Capital Framework of the Reserve Bank of India "
              "(Chairman: Dr. Bimal Jalan) ... The Central Board accepted all the recommendations of the Committee", JALAN)])
Q("009", T, "Mergers and consolidation", "Basic",
  "Under RBI's Voluntary Amalgamation Directions, 2025, by what majority must the Board of Directors of each bank "
  "approve a decision to amalgamate?",
  ["Two-thirds of the total number of Board members, not merely of those present and voting",
   "A simple majority of the directors present and voting",
   "Three-fourths of the directors present and voting",
   "Unanimous approval of all independent directors only"],
  concept="Board approval of a bank merger",
  explanation="The amalgamation decision must be approved by a two-thirds majority of the total strength of the Board "
              "(not just of those present and voting) of both the amalgamating and the amalgamated banks, after "
              "considering due diligence, swap ratio, capital adequacy and similar matters.",
  steps=["Board approval = 2/3 of total Board strength, in both banks"],
  why="A simple or three-fourths majority of those present is not the rule; unanimity of independent directors is not "
      "required.",
  facts=[fact("The decision of amalgamation shall be approved by two-third majority of the total number of Board members "
              "(not merely of those present and voting) of both the amalgamating and the amalgamated banks", AMAL)])
Q("009", T, "Nationalisation", "Intermediate",
  "After the 1969 nationalisation, which scheme introduced on 25 March 1972 provided concessional interest rates on "
  "advances by public sector banks to selected low-income groups?",
  ["Differential Interest Rate (DRI) Scheme", "Lead Bank Scheme", "Village Adoption Scheme", "Service Area Approach"],
  concept="Social banking after nationalisation",
  explanation="RBI's chronology records the Differential Interest Rate Scheme of 25 March 1972, which envisaged "
              "concessional interest rates on advances by public sector banks to selected low-income groups.",
  steps=["Concessional lending to weaker sections, 1972 → DRI Scheme"],
  why="The Lead Bank Scheme (1969) assigned districts to banks; the Village Adoption Scheme came in 1976; the Service "
      "Area Approach became operational in April 1989.",
  facts=[fact("25 Mar 1972: Differential Interest Rate Scheme introduced which envisaged concessional interest rates on "
              "advances made by Public Sector Banks to selected low income groups; 1976: Village Adoption Scheme for "
              "banks introduced", CH68),
         fact("Apr 1989: Service Area Approach for rural lending became operational", CH85)])
Q("009", T, "Committees", "Intermediate",
  "The Bimal Jalan Committee (2019) recommended a change in the method of measuring RBI's market risk. What did it "
  "recommend?",
  ["Expected Shortfall under stressed conditions at a 99.5% confidence level, in place of Stressed Value-at-Risk",
   "Stressed Value-at-Risk at a 95% confidence level, in place of Expected Shortfall",
   "A flat buffer of 10% of the balance sheet, in place of any model",
   "Expected Shortfall at a 90% confidence level for all RBI assets"],
  concept="Jalan Committee on RBI's economic capital",
  explanation="The Committee recommended the Expected Shortfall (ES) method under stressed conditions instead of the "
              "existing Stressed-VaR, with a target of ES at 99.5% confidence (higher than the 99% used by many central "
              "banks), and a downward risk tolerance limit of 97.5%.",
  steps=["Old: Stressed VaR", "New: ES at 99.5% CL (RTL 97.5%)"],
  why="The other options reverse the change or give confidence levels and methods the Committee did not recommend.",
  facts=[fact("The Committee has recommended the adoption of Expected Shortfall (ES) methodology under stressed "
              "conditions (in place of the extant Stressed-Value at Risk) ... the Committee has recommended the "
              "adoption of a target of ES 99.5 per cent CL", JALAN)])

surplus_1819, excess_prov = 123414, 52637
assert surplus_1819 + excess_prov == 176051 and surplus_1819 - excess_prov == 70777
Q("009", T, "Committees", "Advanced",
  "On 26 August 2019, applying the Bimal Jalan Committee's framework, RBI's Central Board decided to keep realised "
  "equity at 5.5% of the balance sheet (the lower bound of the Contingent Risk Buffer range of 5.5%–6.5%). The 2018-19 "
  "net income was ₹1,23,414 crore and excess risk provisions of ₹52,637 crore were written back. What was the total "
  "transfer to the Government, and why was there an excess?",
  ["₹1,76,051 crore; realised equity stood at 6.8% of the balance sheet, above the chosen 5.5% level",
   "₹1,23,414 crore; the excess provisions were retained as a buffer",
   "₹1,76,051 crore; realised equity had fallen below 5.5%, so provisions were released",
   "₹70,777 crore; the excess was deducted from the year's surplus"],
  concept="Surplus distribution under the revised Economic Capital Framework",
  explanation="Available realised equity was 6.8% of the balance sheet. Keeping it at the lower bound of 5.5% released "
              "excess provisions of ₹52,637 crore, written back. The entire net income of ₹1,23,414 crore was also "
              "transferable, so the transfer was 1,23,414 + 52,637 = ₹1,76,051 crore.",
  steps=["Realised equity 6.8% > chosen 5.5% → excess ₹52,637 crore written back",
         "Total = 1,23,414 + 52,637 = ₹1,76,051 crore"],
  why="₹1,23,414 crore omits the write-back; realised equity was above, not below, the range; ₹70,777 crore subtracts "
      "instead of adding.",
  computed=True,
  facts=[fact("decided to transfer a sum of ₹1,76,051 crore to the Government of India comprising of ₹1,23,414 crore of "
              "surplus for the year 2018-19 and ₹52,637 crore of excess provisions", JALAN),
         fact("Given that the available realized equity stood at 6.8 per cent of balance sheet ... The Central Board "
              "decided to maintain the realized equity level at 5.5 per cent of balance sheet", JALAN)])
Q("009", T, "Mergers and consolidation", "Advanced",
  "Under RBI's Voluntary Amalgamation Directions, 2025, which of the following is/are correct?\n"
  "I. The scheme must be approved by shareholders of each bank by a resolution passed by a majority in number "
  "representing two-thirds in value of the shareholders present in person or by proxy.\n"
  "II. Notice of the shareholders' meeting must be published at least once a week for three consecutive weeks in not "
  "less than two newspapers, one in a language understood locally.\n"
  "III. For the amalgamation of an NBFC with a bank, no approval of the NCLT is needed once RBI sanctions the scheme.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Shareholder approval and procedure for bank mergers",
  explanation="Shareholders approve by a majority in number representing two-thirds in value (I), and the notice must "
              "be published once a week for three consecutive weeks in at least two newspapers (II). For an NBFC–bank "
              "amalgamation the scheme needs the Tribunal's (NCLT) approval under Sections 230–234 of the Companies Act, "
              "2013, with a No-Objection Certificate from RBI obtained first, so III is wrong.",
  steps=["I: true", "II: true", "III: false – NBFC–bank merger goes to NCLT after RBI's NOC"],
  why="Options including III are wrong; 'I only' leaves out the true statement II.",
  facts=[fact("shall be approved by the shareholders ... by a resolution passed by a majority in number, representing "
              "two-thirds in value of the shareholders of the said bank, present in person or by proxy", AMAL),
         fact("notices ... shall be published in newspapers at least once a week for three consecutive weeks in not less "
              "than two newspapers ... and one of the newspapers shall be in a language commonly understood in the "
              "locality", AMAL),
         fact("for voluntary amalgamation of an NBFC with a bank or vice versa, scheme of amalgamation shall require "
              "approval by the Tribunal in terms of Sections 230 to 234 of the Companies Act, 2013. However, "
              "No-Objection Certificate from RBI shall be obtained before approaching any Court or Tribunal", AMAL)])

Q("010", T, "Nationalisation", "Basic",
  "In November 1973, after the nationalisation of the major banks, what change did RBI's chronology record for the "
  "State Bank of India and its subsidiaries?",
  ["Restrictions on them were removed to bring them on par with other commercial banks",
   "They were merged into a single bank", "They were brought under the Lead Bank Scheme for the first time",
   "They were barred from opening rural branches"],
  concept="SBI group after nationalisation",
  explanation="RBI's chronology for November 1973 records that restrictions on SBI and its subsidiaries were removed "
              "to bring them on par with other commercial banks.",
  steps=["Nov 1973 → restrictions on SBI group removed (parity with other banks)"],
  why="The associates merged with SBI only in 2017; the Lead Bank Scheme dates from 1969; rural branch expansion was "
      "encouraged, not barred.",
  facts=[fact("Nov 1973: Restrictions on SBI and its subsidiaries removed to bring them on par with other commercial "
              "banks", CH68)])
Q("010", T, "Mergers and consolidation", "Intermediate",
  "Through which portal must banks submit the information and documents required for RBI's approval of a voluntary "
  "amalgamation under the Voluntary Amalgamation Directions, 2025?",
  ["PRAVAAH", "CIMS", "Sachet", "Daksh"],
  concept="Procedure for bank merger applications",
  explanation="After shareholders approve the scheme, it is submitted to RBI for sanction; the information and "
              "documents are filed through RBI's PRAVAAH portal (pravaah.rbi.org.in).",
  steps=["Scheme approved by Boards and shareholders", "Filed with RBI on PRAVAAH"],
  why="CIMS is RBI's statistical returns system; Sachet is for complaints about unauthorised deposit-taking; Daksh is "
      "RBI's supervisory application.",
  facts=[fact("information and documents shall be submitted to RBI through the PRAVAAH portal "
              "(https://pravaah.rbi.org.in)", AMAL)])
Q("010", T, "Committees", "Intermediate",
  "In his statement of 7 October 2026, the RBI Governor announced a new committee to serve as a forum for structured "
  "engagement with market participants and other stakeholders on policy and operational matters relating to financial "
  "markets. What is it called?",
  ["Technical Consultative Committee for Financial Markets", "Financial Markets Committee",
   "Standing Advisory Committee on Money Markets", "Financial Stability and Development Council Sub-Committee"],
  concept="RBI's consultative committees",
  explanation="Citing rapidly evolving financial market dynamics, the Governor said RBI would constitute a Technical "
              "Consultative Committee for Financial Markets as a forum for structured engagement with market "
              "participants and other stakeholders on policy and operational matters related to financial markets.",
  steps=["October 2026 announcement → Technical Consultative Committee for Financial Markets"],
  why="The Financial Markets Committee is RBI's internal committee that reviews liquidity daily; the other two are "
      "not what was announced.",
  current=ca("2026-10-07"),
  facts=[fact("we shall constitute a Technical Consultative Committee for Financial Markets. The Committee will serve as "
              "a forum for structured engagement with market participants and other stakeholders on policy and "
              "operational matters related to financial markets", GOV_OCT26)])
Q("010", T, "Nationalisation", "Intermediate",
  "RBI's profile of Governor S. Jagannathan (1970–1975) links his tenure to which development flowing from one of the "
  "important objectives of bank nationalisation?",
  ["An exponential expansion of banking offices", "The merger of the SBI associate banks",
   "The introduction of the Base Rate system", "The first issue of RBI's own banknotes"],
  concept="Branch expansion after nationalisation",
  explanation="RBI notes that S. Jagannathan's tenure saw 'an exponential expansion of banking offices in pursuance of "
              "one of the important objectives of nationalisation', along with the setting up of the Credit Guarantee "
              "Corporation of India and State Level Bankers' Committees.",
  steps=["Nationalisation objective → wider branch network", "Achieved during Jagannathan's tenure"],
  why="SBI associates merged in 2017; the Base Rate came in 2010; RBI issued its first notes in 1938.",
  facts=[fact("His tenure of office was characterised by ... an exponential expansion of banking offices in pursuance of "
              "one of the important objectives of nationalisation; the establishment of Credit Guarantee Corporation of "
              "India", GOVS)])

rrb_in, rrb_out = [8, 3], [19, 7]
assert sum(rrb_out) - sum(rrb_in) == 15 and sum(rrb_out) + sum(rrb_in) == 37
Q("010", T, "Mergers and consolidation", "Advanced",
  "Under the 'One State-One RRB' amalgamation, RBI notified (Gazette of 11 November 2025) that 8 Regional Rural Banks "
  "were included in and 19 erstwhile RRBs excluded from the Second Schedule to the RBI Act, and (Gazette of 3 February "
  "2026) that 3 RRBs were included and 7 erstwhile RRBs excluded. What was the net reduction in the number of RRBs in "
  "the Second Schedule from these two notifications?",
  ["15", "11", "4", "37"],
  concept="Second Schedule changes from RRB amalgamation",
  explanation="Each amalgamation removes the erstwhile RRBs from the Second Schedule and adds the new amalgamated RRB. "
              "Net reduction = (19 − 8) + (7 − 3) = 11 + 4 = 15.",
  steps=["Round 1: 19 out − 8 in = 11", "Round 2: 7 out − 3 in = 4", "Total = 15"],
  why="11 and 4 are each notification alone; 37 adds inclusions instead of subtracting them.",
  computed=True, current=ca("2026-02-03"),
  facts=[fact("The names of the following eight Regional Rural Banks (RRBs) have been included ... the names of the "
              "following nineteen erstwhile RRBs have been excluded from the Second Schedule ... published in the Gazette "
              "of India dated November 11, 2025", RRB_SCHED),
         fact("The names of the following three Regional Rural Banks (RRBs) have been included ... the names of the "
              "following seven erstwhile RRBs have been excluded from the Second Schedule ... published in the Gazette of "
              "India dated February 03, 2026", RRB_SCHED2)])


# ============================================================================================ Reserve Bank of India
T = "Reserve Bank of India"
Q("008", T, "Governors and leadership", "Basic",
  "Who was the twenty-first Governor of the Reserve Bank of India, serving from September 2003 to September 2008?",
  ["Dr. Y. V. Reddy", "Dr. Bimal Jalan", "Dr. D. Subbarao", "Dr. C. Rangarajan"],
  concept="RBI Governors in order",
  explanation="RBI's list of Governors shows Dr. Yaga Venugopal Reddy, described as 'the twenty-first Governor', in "
              "office from 6 September 2003 to 5 September 2008. He was preceded by Dr. Bimal Jalan and succeeded by "
              "Dr. D. Subbarao (the 22nd).",
  steps=["2003–2008 → Dr. Y. V. Reddy (21st)"],
  why="Dr. Jalan served 1997–2003, Dr. Subbarao 2008–2013 (22nd) and Dr. Rangarajan 1992–1997.",
  facts=[fact("Dr. Y V Reddy, 06-09-2003 to 05-09-2008: Dr. Yaga Venugopal Reddy the twenty-first Governor", GOVS)])
Q("008", T, "Governors and leadership", "Intermediate",
  "Which RBI Governor had served as India's Ambassador to the United States before joining the Bank?",
  ["Sir Benegal Rama Rau", "L. K. Jha", "Sir C. D. Deshmukh", "H. V. R. Iengar"],
  concept="Backgrounds of RBI Governors",
  explanation="RBI's profile says Sir Benegal Rama Rau (Governor 1949–1957) 'served as the Indian Ambassador to the "
              "United States' before joining the Bank. L. K. Jha went the other way: he left the Governorship in 1970 "
              "on being appointed Ambassador to the US.",
  steps=["Ambassador to US before RBI → Rama Rau", "Ambassador to US after RBI → L. K. Jha"],
  why="L. K. Jha became Ambassador after his tenure; Deshmukh and Iengar were ICS officers who did not hold that post "
      "before joining.",
  facts=[fact("Sir Benegal Rama Rau ... Prior to joining the Bank he served as the Indian Ambassador to the United "
              "States", GOVS),
         fact("L K Jha was appointed India's Ambassador to the United States in May 1970 prior to the completion of his "
              "term as Governor", GOVS)])
Q("008", T, "Establishment and structure", "Intermediate",
  "RBI appointed Smt. Usha Janakiraman as Executive Director with effect from 1 December 2025. Which department was "
  "she assigned to look after?",
  ["Department of Supervision (Risk, Analytics and Vulnerability Assessment)", "Department of Currency Management",
   "Monetary Policy Department", "Department of Payment and Settlement Systems"],
  concept="RBI's top management: Executive Directors",
  explanation="Before promotion she was Chief General Manager-in-Charge, Department of Regulation. As Executive "
              "Director she was to look after the Department of Supervision (Risk, Analytics and Vulnerability "
              "Assessment).",
  steps=["ED from 1 Dec 2025 → Department of Supervision (RAVA)"],
  why="The other departments were not assigned to her in the announcement.",
  current=ca("2025-12-01"),
  facts=[fact("The Reserve Bank of India (RBI) has appointed Smt. Usha Janakiraman as Executive Director (ED) with effect "
              "from December 1, 2025 ... will look after the Department of Supervision (Risk, Analytics and "
              "Vulnerability Assessment)", ED_USHA)])
Q("008", T, "Establishment and structure", "Intermediate",
  "RBI's College of Agricultural Banking at Pune was set up in September 1969 under a different name. What was it "
  "originally called?",
  ["Cooperative Bankers Training College", "Bankers' Training College", "Staff Training College",
   "National Institute of Bank Management"],
  concept="RBI's training establishments",
  explanation="RBI's chronology records the Cooperative Bankers Training College (CBTC), established at Poona (Pune) on "
              "29 September 1969 to train the cooperative sector, which was renamed the College of Agricultural Banking "
              "in 1974.",
  steps=["CBTC, Pune (1969) → renamed College of Agricultural Banking (1974)"],
  why="The Bankers' Training College (1954) was at Bombay; the Staff Training College (1963) at Madras; NIBM (1969) is "
      "a separate institute set up at Bombay.",
  facts=[fact("29 Sep 1969: Cooperative Bankers Training College (CBTC) established at Poona (Pune) to provide training "
              "to the cooperative sector. Later renamed College of Agricultural Banking (CAB) in 1974", CH68)])
Q("008", T, "Governors and leadership", "Advanced",
  "Consider the following statements based on RBI's profiles of its Governors:\n"
  "I. Dr. D. Subbarao took over on 5 September 2008 as the 22nd Governor and was appointed for a three-year term.\n"
  "II. Dr. Raghuram Rajan was Chief Economist and Director of Research at the International Monetary Fund between 2003 "
  "and 2006.\n"
  "III. Dr. D. Subbarao had been a lead economist at the International Monetary Fund before becoming Finance "
  "Secretary.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Profiles of recent Governors",
  explanation="RBI's profile says Dr. Subbarao took over on 5 September 2008 as the 22nd Governor for a three-year term "
              "(I), and that Dr. Rajan was the IMF's Chief Economist and Director of Research in 2003–2006 (II). Dr. "
              "Subbarao was a lead economist at the World Bank (1999–2004), not the IMF, so III is wrong.",
  steps=["I: true", "II: true", "III: false – World Bank, not IMF"],
  why="Options with III are wrong; 'I only' leaves out the true statement II.",
  facts=[fact("Dr. D. Subbarao took over on September 5, 2008 as the 22nd Governor of the Reserve Bank of India. Dr. "
              "Subbarao has been appointed for a three-year term ... lead economist in the World Bank (1999-2004)", GOVS),
         fact("Between 2003 and 2006, Dr. Rajan was the Chief Economist and Director of Research at the International "
              "Monetary Fund", GOVS)])
Q("008", T, "Governors and leadership", "Advanced",
  "Consider the following statements about Shri Sanjay Malhotra, as given in RBI's profile:\n"
  "I. Immediately before his appointment as Governor he was Secretary, Department of Revenue, Ministry of Finance.\n"
  "II. He had earlier served on RBI's Central Board as a Government nominee director in 2022.\n"
  "III. He is an Indian Police Service officer of the 1990 batch.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Profile of the current Governor",
  explanation="RBI's profile says that immediately before his appointment he was Secretary, Department of Revenue "
              "(earlier Secretary, Department of Financial Services) (I), and that he served on the Central Board as a "
              "Government nominee director from 16 February 2022 to 14 November 2022 (II). He is an IAS officer of the "
              "1990 batch, Rajasthan cadre, so III is wrong.",
  steps=["I: true", "II: true (Feb–Nov 2022)", "III: false – IAS, not IPS"],
  why="Options with III are wrong; 'I only' leaves out the true statement II.",
  facts=[fact("Shri Sanjay Malhotra, an Indian Administrative Service Officer of 1990 Batch Rajasthan Cadre ... Immediately "
              "prior to this appointment, Shri Malhotra was Secretary, Department of Revenue (DOR) in the Ministry of "
              "Finance", GOVS),
         fact("Shri Malhotra served on the Central Board of Reserve Bank of India as a Government Nominee Director from "
              "February 16, 2022 to November 14, 2022", GOVS)])
Q("008", T, "Establishment and structure", "Advanced",
  "Arrange the following institutions in the order in which they were set up, according to RBI's chronology:\n"
  "I. Indira Gandhi Institute of Development Research (IGIDR)\n"
  "II. Bankers' Training College, Bombay\n"
  "III. National Institute of Bank Management (NIBM), Bombay\n"
  "IV. Staff Training College, Madras",
  ["II, IV, III, I", "II, III, IV, I", "IV, II, III, I", "II, IV, I, III"],
  concept="Institution building by RBI",
  explanation="Bankers' Training College, Bombay: inaugurated 14 September 1954. Staff Training College, Madras: 26 "
              "August 1963. NIBM: established at Bombay on 24 September 1969 (later moved to Pune). IGIDR: established "
              "by RBI on 28 December 1987. Order: II, IV, III, I.",
  steps=["1954 BTC", "1963 STC Madras", "1969 NIBM", "1987 IGIDR"],
  why="The other orders misplace the 1963 Staff Training College or put IGIDR (1987) before NIBM (1969).",
  facts=[fact("14 Sep 1954: Bankers' Training College to provide training to banking personnel established at Bombay "
              "(Mumbai) inaugurated", CH50),
         fact("26 Aug 1963: Staff Training College established at Madras", CH60),
         fact("24 Sep 1969: National Institute of Bank Management (NIBM) established at Bombay (Mumbai)", CH68),
         fact("28 Dec 1987: Indira Gandhi Institute of Development Research (IGIDR) was established by Reserve Bank", CH85)])

from datetime import date as _date
_t_sub = (_date(2013, 9, 4) - _date(2008, 9, 5)).days
_t_raj = (_date(2016, 9, 4) - _date(2013, 9, 4)).days
_t_pat = (_date(2018, 12, 11) - _date(2016, 9, 4)).days
assert (_t_sub, _t_raj, _t_pat) == (1825, 1096, 828) and _t_pat < _t_raj < _t_sub
Q("008", T, "Governors and leadership", "Advanced",
  "RBI's list of Governors gives these terms: Dr. D. Subbarao 05-09-2008 to 04-09-2013; Dr. Raghuram Rajan 04-09-2013 "
  "to 04-09-2016; Dr. Urjit R. Patel 04-09-2016 to 11-12-2018. Which statement is correct?",
  ["Dr. Patel's tenure was the shortest, about 2 years and 3 months, roughly 9 months less than Dr. Rajan's",
   "Dr. Rajan's tenure was the shortest, exactly 3 years",
   "Dr. Patel's tenure was about 3 years and 3 months, the longest after Dr. Subbarao's",
   "All three served exactly one five-year term each"],
  concept="Comparing tenures",
  explanation="Subbarao: Sep 2008 → Sep 2013 ≈ 5 years (1,825 days). Rajan: Sep 2013 → Sep 2016 = 3 years (1,096 days). "
              "Patel: 4 Sep 2016 → 11 Dec 2018 ≈ 2 years 3 months (828 days), about 268 days (≈9 months) less than "
              "Rajan's. Patel's was the shortest.",
  steps=["Subbarao ≈ 5 yr", "Rajan = 3 yr", "Patel ≈ 2 yr 3 m → shortest"],
  why="Rajan's 3 years exceeds Patel's; Patel's tenure was not 3 years 3 months; the three terms differ.",
  computed=True,
  facts=[fact("Dr. D. Subbarao 05-09-2008 to 04-09-2013; Dr. Raghuram Rajan 04-09-2013 to 04-09-2016; Dr. Urjit R. Patel "
              "04-09-2016 to 11-12-2018", GOVS)])

Q("009", T, "Governors and leadership", "Basic",
  "Governor Sanjay Malhotra, an engineering graduate of IIT Kanpur, holds a Master in Public Policy from which "
  "university?",
  ["Princeton University", "Harvard University", "University of Chicago", "London School of Economics"],
  concept="Profile of the current Governor",
  explanation="RBI's profile states that Shri Malhotra is a graduate in Computer Science and Engineering from IIT Kanpur "
              "and holds a Master in Public Policy from Princeton University, USA.",
  steps=["B.Tech (CSE) IIT Kanpur; MPP Princeton"],
  why="The other universities are not named in his profile.",
  facts=[fact("Shri Malhotra is a graduate in Computer Science and Engineering from the Indian Institute of Technology, "
              "Kanpur and a Master in Public Policy from the Princeton University, USA", GOVS)])
Q("009", T, "Governors and leadership", "Basic",
  "During the tenure of which RBI Governor was the 'historic memorandum' signed between RBI and the Government that "
  "capped automatic financing of the Government through ad hoc Treasury Bills?",
  ["Dr. C. Rangarajan", "Dr. Bimal Jalan", "S. Venkitaramanan", "Dr. Y. V. Reddy"],
  concept="Governors and monetary reforms",
  explanation="RBI's profile of Dr. C. Rangarajan (1992–1997) notes that his tenure saw the historic memorandum between "
              "RBI and the Government putting a cap on automatic finance to the Government through ad hoc Treasury "
              "Bills, a key step toward monetary autonomy.",
  steps=["Cap on ad hoc T-bills (memorandum) → Rangarajan's tenure"],
  why="Dr. Jalan took over in November 1997; Venkitaramanan (1990–92) handled the BoP crisis; Dr. Reddy served "
      "2003–08.",
  facts=[fact("In the field of monetary policy, his tenure saw the historic memorandum signed between the Bank and the "
              "Government whereby a cap was put on the automatic finance by the Bank to the Government in the form of "
              "ad hoc treasury bills", GOVS)])
Q("009", T, "Governors and leadership", "Basic",
  "Who was the Governor of RBI when India faced the external payments (balance of payments) crisis of 1991 and adopted "
  "the IMF's stabilisation programme?",
  ["S. Venkitaramanan", "R. N. Malhotra", "Dr. C. Rangarajan", "Dr. Manmohan Singh"],
  concept="RBI leadership during the 1991 crisis",
  explanation="S. Venkitaramanan was Governor from 22 December 1990 to 21 December 1992. RBI's profile credits his "
              "'adroit management' with helping the country tide over the balance of payments crisis, when the rupee was "
              "devalued and economic reforms were launched.",
  steps=["1991 crisis → Governor S. Venkitaramanan (Dec 1990–Dec 1992)"],
  why="R. N. Malhotra left in December 1990; Dr. Rangarajan took over in December 1992; Dr. Manmohan Singh was then "
      "Finance Minister, not Governor.",
  facts=[fact("Venkitaramanan 22-12-1990 to 21-12-1992 ... His adroit management saw the country tide over the balance of "
              "payments crisis. His term also saw India adopt the IMF's stabilisation programme", GOVS)])
Q("009", T, "Governors and leadership", "Intermediate",
  "Which RBI Governor had been closely associated with the preparation and piloting of the Reserve Bank of India Bill, "
  "served as Deputy Governor before becoming Governor, and saw his second term end with his sudden demise?",
  ["Sir James Braid Taylor", "Sir Osborne Smith", "Sir C. D. Deshmukh", "Sir Benegal Rama Rau"],
  concept="Early Governors of RBI",
  explanation="Sir James Taylor (Governor 1937–1943), an ICS officer who had been Controller of the Currency, was "
              "associated with piloting the RBI Bill and was Deputy Governor before becoming Governor. His second term "
              "ended with his sudden death in February 1943, after which C. D. Deshmukh took over.",
  steps=["Piloted RBI Bill + DG → Governor; died in office → James Taylor"],
  why="Osborne Smith resigned early; Deshmukh and Rama Rau did not die in office.",
  facts=[fact("He was closely associated with the preparation and piloting of the Reserve Bank of India Bill. He served "
              "as Deputy Governor of the Bank prior to his appointment as the Governor ... His second term came to an end "
              "with his sudden demise", GOVS)])
Q("009", T, "Governors and leadership", "Intermediate",
  "A. Ghosh, who was RBI Governor for about 15 days in 1985, had earlier been the chairman of which bank before "
  "becoming Deputy Governor?",
  ["Allahabad Bank", "State Bank of India", "Punjab National Bank", "Bank of Baroda"],
  concept="Backgrounds of RBI Governors",
  explanation="RBI's profile says A. Ghosh had been Deputy Governor since 1982 and earlier chairman of Allahabad Bank; he "
              "was also a director of IDBI and on NIBM's governing body.",
  steps=["A. Ghosh: Allahabad Bank chairman → DG (1982) → Governor (Jan–Feb 1985)"],
  why="The other banks are not mentioned in his profile.",
  facts=[fact("A Ghosh was the Deputy Governor of the Bank since 1982 when he was appointed Governor for a brief period "
              "of 15 days ... He was earlier the chairman of Allahabad Bank", GOVS)])
Q("009", T, "Establishment and structure", "Intermediate",
  "Where was the 620th meeting of RBI's Central Board held on 19 December 2025, and what framework did it approve?",
  ["Hyderabad; the risk-based deposit insurance framework for banks", "Mumbai; the revised Economic Capital Framework",
   "New Delhi; the Medium Term Strategy Framework 'Utkarsh 3.0'", "Kolkata; the National Strategy for Financial "
   "Inclusion"],
  concept="Central Board meetings",
  explanation="The 620th Central Board meeting, chaired by Governor Sanjay Malhotra, was held in Hyderabad. It approved "
              "the risk-based deposit insurance framework for banks and reviewed the draft Report on Trend and Progress "
              "of Banking in India, 2024-25.",
  steps=["620th meeting → Hyderabad → risk-based deposit insurance framework"],
  why="Utkarsh 3.0 was approved at the 622nd meeting (Patna, March 2026); the other pairings are not what this meeting "
      "did.",
  current=ca("2025-12-19"),
  facts=[fact("The 620 th meeting of the Central Board of Directors of Reserve Bank of India was held today in Hyderabad "
              "... It approved the risk-based deposit insurance framework for banks", BOARD620)])
Q("009", T, "Governors and leadership", "Advanced",
  "Match the RBI Governor with the background RBI's profile gives for him:\n"
  "1. Dr. Bimal Jalan\n2. Shri Shaktikanta Das\n3. Dr. D. Subbarao\n4. Dr. C. Rangarajan\n"
  "P. Member of the 15th Finance Commission and G20 Sherpa of India immediately before appointment\n"
  "Q. Deputy Governor for over a decade, and a member of the Tenth Finance Commission\n"
  "R. Finance Secretary immediately before appointment; earlier Secretary to the PM's Economic Advisory Council\n"
  "S. Chief Economic Advisor, Banking Secretary, Finance Secretary and Chairman of the PM's Economic Advisory Council",
  ["1-S, 2-P, 3-R, 4-Q", "1-R, 2-P, 3-S, 4-Q", "1-S, 2-Q, 3-R, 4-P", "1-Q, 2-P, 3-R, 4-S"],
  concept="Backgrounds of RBI Governors",
  explanation="Jalan had been CEA, Banking Secretary, Finance Secretary and Chairman of the EAC to the PM (S). Das was "
              "Member, 15th Finance Commission and G20 Sherpa just before taking charge (P). Subbarao was Finance "
              "Secretary, and earlier Secretary to the PM's EAC (R). Rangarajan was Deputy Governor for over a decade "
              "and a member of the Tenth Finance Commission (Q).",
  steps=["Jalan–S", "Das–P", "Subbarao–R", "Rangarajan–Q"],
  why="The other options swap Jalan with Subbarao or Rangarajan with Das.",
  facts=[fact("Dr. Bimal Jalan, served as Chief Economic Advisor to Government of India, Banking Secretary, Finance "
              "Secretary, Member Secretary of Planning Commission, and Chairman of the Economic Advisory Council to the "
              "Prime Minister prior to being appointed as Governor", GOVS),
         fact("Shri Shaktikanta Das ... Immediately prior to his current assignment, he was acting as Member, 15th Finance "
              "Commission and G20 Sherpa of India", GOVS),
         fact("Prior to this appointment, Dr. Subbarao was the Finance Secretary ... earlier been Secretary to the Prime "
              "Minister's Economic Advisory Council (2005-2007)", GOVS),
         fact("Dr. C Rangarajan ... held charge as Deputy Governor for over a decade. He was also a member of the Planning "
              "Commission and a member of the Tenth Finance Commission", GOVS)])

Q("010", T, "Establishment and structure", "Basic",
  "According to RBI's chronology, the Reserve Bank of India Act, 1934 (II of 1934), which constitutes the statutory "
  "basis of the Bank, is dated:",
  ["5 March 1934", "1 April 1935", "1 January 1949", "26 January 1934"],
  concept="Statutory basis of RBI",
  explanation="RBI's chronology lists 5 March 1934 for the RBI Act, 1934 (II of 1934), 'the statutory basis on which "
              "the Bank is established'. The Bank commenced operations on 1 April 1935 and was nationalised on "
              "1 January 1949.",
  steps=["Act: 5 March 1934", "Operations: 1 April 1935"],
  why="1 April 1935 is when operations began; 1 January 1949 is nationalisation; 26 January 1934 is not a date in the "
      "chronology.",
  facts=[fact("5 March 1934: Reserve Bank of India Act, 1934, (II of 1934) constitutes the statutory basis on which the "
              "Bank is established", CH26)])
Q("010", T, "Governors and leadership", "Basic",
  "Which former RBI Governor wrote 'Fault Lines: How Hidden Fractures Still Threaten the World Economy', which won the "
  "Financial Times–Goldman Sachs prize for best business book in 2010?",
  ["Dr. Raghuram Rajan", "Dr. D. Subbarao", "Dr. Urjit R. Patel", "Dr. Y. V. Reddy"],
  concept="Profiles of Governors",
  explanation="RBI's profile of Dr. Raghuram Rajan, the 23rd Governor, notes that he co-authored 'Saving Capitalism from "
              "the Capitalists' (2003) and wrote 'Fault Lines', which won the FT–Goldman Sachs prize for best business "
              "book in 2010.",
  steps=["'Fault Lines' (FT–Goldman Sachs prize 2010) → Raghuram Rajan"],
  why="The book is not by the other Governors.",
  facts=[fact("He then wrote Fault Lines: How Hidden Fractures Still Threaten the World Economy, for which he was awarded "
              "the Financial Times-Goldman Sachs prize for best business book in 2010", GOVS)])
Q("010", T, "Establishment and structure", "Intermediate",
  "RBI appointed Shri Gunveer Singh as Executive Director with effect from 18 May 2026. Which department was he to look "
  "after?",
  ["Department of Payment and Settlement Systems", "Department of Regulation", "Department of Currency Management",
   "Foreign Exchange Department"],
  concept="RBI's Executive Directors",
  explanation="Before promotion Shri Singh was Chief General Manager-in-Charge of the Department of Payment and "
              "Settlement Systems; as ED he continues to look after that department. He is a Chartered Accountant and "
              "a Cost and Works Accountant and has served as a payment systems expert at the Central Bank of Oman.",
  steps=["ED from 18 May 2026 → DPSS"],
  why="The other departments were not assigned to him.",
  current=ca("2026-05-18"),
  facts=[fact("The Reserve Bank of India (RBI) has appointed Shri Gunveer Singh as Executive Director (ED) with effect from "
              "May 18, 2026 ... As Executive Director, Shri Singh will look after the Department of Payment and "
              "Settlement Systems", ED_GUNVEER)])
Q("010", T, "Governors and leadership", "Intermediate",
  "In the distribution of portfolios among RBI's Deputy Governors effective 4 May 2026, who was to look after "
  "co-ordination as the senior-most Deputy Governor?",
  ["Shri Swaminathan Janakiraman", "Dr. Poonam Gupta", "Shri Shirish Chandra Murmu", "Shri Rohit Jain"],
  concept="Deputy Governors' portfolios",
  explanation="After Shri Rohit Jain took charge as Deputy Governor, RBI redistributed portfolios from 4 May 2026. "
              "Co-ordination is looked after by the senior-most Deputy Governor, Shri Swaminathan Janakiraman, whose "
              "portfolios include the Consumer Education and Protection Department and DICGC.",
  steps=["Co-ordination → senior-most DG → Swaminathan Janakiraman"],
  why="Dr. Gupta handles economic research, statistics and financial markets operations; Shri Murmu handles payment "
      "systems and communication; Shri Jain is the newest Deputy Governor.",
  current=ca("2026-05-04"),
  facts=[fact("Co-ordination shall be looked after by the senior most Deputy Governor, Shri Swaminathan Janakiraman", DG_PORTF)])
Q("010", T, "Governors and leadership", "Intermediate",
  "N. C. Sen Gupta was RBI Governor for about three months in 1975 until K. R. Puri could take over. What post was he "
  "holding before his appointment?",
  ["Secretary to the Department of Banking, Ministry of Finance", "Chairman of the State Bank of India",
   "India's Executive Director at the IMF", "Deputy Governor of RBI"],
  concept="Interim Governors",
  explanation="RBI's profile says N. C. Sen Gupta (19 May 1975 – 19 August 1975) was working as Secretary to the "
              "Department of Banking of the Ministry of Finance before his appointment.",
  steps=["N. C. Sen Gupta: Secretary, Department of Banking → interim Governor (1975)"],
  why="SBI chairmanship applies to Iengar and Bhattacharya; IMF ED to Adarkar, Jagannathan and others; he was not a DG.",
  facts=[fact("N C Sen Gupta was appointed Governor for three months till K R Puri could assume office. Prior to his "
              "appointment as the Governor, he was working as Secretary to the Department of Banking of the Ministry of "
              "Finance", GOVS)])
Q("010", T, "Governors and leadership", "Advanced",
  "Consider the following statements about Shri Rohit Jain's appointment as Deputy Governor of RBI in May 2026:\n"
  "I. The Government appointed him under Section 8(1)(a) read with Section 8(4) of the RBI Act, 1934, for three years "
  "from the date of joining on or after 3 May 2026, or until further orders.\n"
  "II. He was an Executive Director of RBI at the time of his appointment.\n"
  "III. In the portfolio distribution effective 4 May 2026 he was given the Department of Payment and Settlement "
  "Systems.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I and III only", "II only", "I, II and III"],
  concept="Appointment of Deputy Governors",
  explanation="The Government's notification of 2 May 2026 appointed 'Shri Rohit Jain, Executive Director' as Deputy "
              "Governor under Section 8(1)(a) read with 8(4), for three years from joining on or after 3 May 2026 (I, "
              "II). In the portfolio list of 4 May 2026 the Department of Payment and Settlement Systems is with Shri "
              "Shirish Chandra Murmu; Shri Jain's portfolios include the Department of Government and Bank Accounts and "
              "the Financial Markets Regulation Department, so III is wrong.",
  steps=["I: true", "II: true", "III: false – DPSS is with Shri Murmu"],
  why="Options with III are wrong; 'II only' leaves out the true statement I.",
  current=ca("2026-05-04"),
  facts=[fact("in exercise of the powers conferred by clause (a) of sub-section (1) of section 8 of the Reserve Bank of "
              "India Act 1934, read with sub-section (4) of section 8 thereof, has appointed Shri Rohit Jain, Executive "
              "Director as Deputy Governor ... for a period of three years from the date of joining the post on or after "
              "May 03, 2026 or until further orders", DG_JAIN),
         fact("Shri Shirish Chandra Murmu: Department of Communication; Department of Payment and Settlement Systems. Shri "
              "Rohit Jain: Corporate Strategy and Budget Department; Department of Government and Bank Accounts; "
              "Financial Markets Regulation Department", DG_PORTF)])
Q("010", T, "Establishment and structure", "Advanced",
  "Consider the following statements about meetings of RBI's Central Board in 2026:\n"
  "I. The 621st meeting was held in New Delhi in February 2026, after which the Union Finance Minister addressed the "
  "Directors on the Union Budget 2026-27.\n"
  "II. The 622nd meeting, held in Patna in March 2026, approved RBI's budget for 2026-27 and its Medium Term Strategy "
  "Framework 'Utkarsh 3.0' for 2026-29.\n"
  "III. Both meetings were chaired by the Union Finance Minister.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II only", "I and III only", "I, II and III"],
  concept="RBI's Central Board",
  explanation="The 621st meeting (New Delhi, 23 February 2026) was followed by the Finance Minister's address on the "
              "Budget (I). The 622nd meeting (Patna, 20 March 2026) approved the Bank's 2026-27 budget and Utkarsh 3.0 "
              "for 2026-29 (II). Both were chaired by Governor Sanjay Malhotra; the Finance Minister only addressed the "
              "Directors after the 621st meeting, so III is wrong.",
  steps=["I: true", "II: true", "III: false – the Governor chairs the Central Board"],
  why="The Central Board is chaired by the Governor, so options with III are wrong; 'II only' leaves out I.",
  current=ca("2026-03-20"),
  facts=[fact("The 621 st meeting of the Central Board of Directors of the Reserve Bank of India was held today at New "
              "Delhi under the Chairmanship of Shri Sanjay Malhotra, Governor ... Smt. Nirmala Sitharaman, Hon'ble Union "
              "Minister of Finance ... addressed and interacted with the Directors of the Central Board, after the Board "
              "meeting", BOARD621),
         fact("The 622 nd meeting of the Central Board ... was held today in Patna under the Chairmanship of Shri Sanjay "
              "Malhotra, Governor ... The Board approved the Bank's budget for the accounting year 2026-27 and also the "
              "Bank's Medium Term Strategy Framework (Utkarsh 3.0) for the period 2026-29", BOARD622)])
Q("010", T, "Governors and leadership", "Advanced",
  "Consider the following statements based on RBI's profiles of its Governors:\n"
  "I. R. N. Malhotra had served as an Executive Director of the IMF before he became Governor.\n"
  "II. S. Jagannathan relinquished the Governorship to take up the post of India's Executive Director at the IMF.\n"
  "III. Dr. Y. V. Reddy was India's Executive Director at the World Bank immediately before becoming Governor.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Governors and the Bretton Woods institutions",
  explanation="R. N. Malhotra served as Secretary, Finance and Executive Director of the IMF before his appointment (I). "
              "S. Jagannathan 'relinquished office to take up the post of the Indian Executive Director at the IMF' (II). "
              "Dr. Reddy was India's Executive Director on the Board of the IMF, not the World Bank, before becoming "
              "Governor, so III is wrong.",
  steps=["I: true", "II: true", "III: false – IMF, not World Bank"],
  why="Options with III are wrong; 'I only' leaves out the true statement II.",
  facts=[fact("R.N. Malhotra, a member of the Indian Administrative Service, served as Secretary, Finance and Executive "
              "Director of the IMF. prior to his appointment as Governor", GOVS),
         fact("He relinquished office to take up the post of the Indian Executive Director at the IMF (S Jagannathan)", GOVS),
         fact("Prior to his appointment as the Governor, Dr. Reddy was India's Executive Director on the Board of the "
              "International Monetary Fund", GOVS)])


# ============================================================================================ RBI Functions
T = "RBI Functions"
Q("008", T, "Issuer of currency", "Basic",
  "On the Mahatma Gandhi (New) Series banknotes, the raised (intaglio) identification mark for the visually challenged "
  "on the ₹500 note has which shape?",
  ["Circle", "Triangle", "Horizontal rectangle", "The letter 'H'"],
  concept="Features of MG (New) Series banknotes",
  explanation="RBI's currency FAQs list the identification marks in raised print: a horizontal rectangle for ₹2000, a "
              "circle for ₹500, a raised 'H' for ₹200 and a triangle for ₹100.",
  steps=["₹500 → circle"],
  why="The triangle is on ₹100, the horizontal rectangle on ₹2000 and 'H' on ₹200.",
  facts=[fact("There is an identification mark on the front side of each note which is in raised print (intaglio) and "
              "has different shapes for different denominations for e.g. Horizontal rectangle for ₹2000, circle for "
              "₹500, raised Identification mark H for ₹200, triangle for ₹100", CUR)])
Q("008", T, "Issuer of currency", "Basic",
  "Banknotes are printed at four presses. Where are the two presses owned by the Government of India through the "
  "Security Printing and Minting Corporation of India Ltd (SPMCIL)?",
  ["Nashik and Dewas", "Mysuru and Salboni", "Mumbai and Hyderabad", "Kolkata and Noida"],
  concept="Printing of banknotes",
  explanation="Of the four currency presses, SPMCIL's are at Nashik (western India) and Dewas (central India); RBI's "
              "subsidiary BRBNMPL runs the presses at Mysuru and Salboni. Mumbai, Hyderabad, Kolkata and Noida host "
              "SPMCIL's coin mints.",
  steps=["SPMCIL note presses → Nashik, Dewas"],
  why="Mysuru and Salboni are BRBNMPL presses; the other cities are mints.",
  facts=[fact("The currency presses of SPMCIL are at Nasik (Western India) and Dewas (Central India). The two presses of "
              "BRBNMPL are at Mysuru (Southern India) and Salboni (Eastern India)", CUR)])
Q("008", T, "Issuer of currency", "Intermediate",
  "What is a 'currency chest', as described in RBI's FAQs on currency management?",
  ["A storehouse at a select scheduled bank where banknotes and rupee coins are stocked on behalf of RBI for "
   "distribution to bank branches in its area",
   "A vault at an RBI Issue Office where soiled notes are destroyed",
   "A Government treasury where coins are minted",
   "A locker in which customers keep foreign currency"],
  concept="Currency distribution network",
  explanation="RBI authorises select scheduled banks to set up currency chests — storehouses where banknotes and rupee "
              "coins are stocked on RBI's behalf for distribution to bank branches in their area (2,691 as on 28 "
              "February 2025). Small Coin Depots stock coins below one rupee.",
  steps=["Currency chest = bank-run store of RBI's notes and rupee coins for local distribution"],
  why="Note destruction happens at RBI; minting is done by SPMCIL; it is not a customer locker.",
  facts=[fact("the Reserve Bank has authorised select scheduled banks to establish currency chests. These are storehouses "
              "where banknotes and rupee coins are stocked on behalf of the Reserve Bank for distribution to bank branches "
              "in their area of operation. As on February 28, 2025, there were 2691 currency chests", CUR)])
Q("008", T, "Issuer of currency", "Intermediate",
  "Which RBI offices, known as 'Mint Linked Offices', receive coins directly from the mints for onward distribution?",
  ["Hyderabad, Kolkata, Mumbai and New Delhi", "Mumbai, Nashik, Dewas and Kolkata",
   "Mysuru, Salboni, Mumbai and Chennai", "Nagpur, Chennai, Kolkata and Jaipur"],
  concept="Distribution of coins",
  explanation="Coins minted by SPMCIL are received by RBI's offices at Hyderabad, Kolkata, Mumbai and New Delhi (Mint "
              "Linked Offices), which send them to other RBI offices and then to currency chests and small coin depots.",
  steps=["Mints → Mint Linked Offices (Hyderabad, Kolkata, Mumbai, New Delhi) → other offices → chests/depots"],
  why="Nashik and Dewas are note presses; Mysuru and Salboni are BRBNMPL note presses; the last set is not the list.",
  facts=[fact("The Reserve Bank offices located at Hyderabad, Kolkata, Mumbai and New Delhi (Mint Linked Offices) receive "
              "coins from the mints", CUR)])
Q("008", T, "Regulator and supervisor", "Intermediate",
  "In February 1964, a new Chapter IIIB was inserted in the RBI Act, 1934. What power did it give RBI?",
  ["To regulate the deposit acceptance activities of non-banking institutions",
   "To collect credit information from banks about their borrowers",
   "To supervise urban co-operative banks", "To manage the foreign exchange reserves"],
  concept="Growth of RBI's regulatory powers",
  explanation="RBI's chronology records that on 1 February 1964 RBI was empowered to regulate the deposit acceptance "
              "activities of non-banking institutions through the new Chapter IIIB of the RBI Act — the base of its "
              "regulation of NBFCs.",
  steps=["Chapter IIIB (1964) → deposit-taking by non-banking institutions"],
  why="Credit information powers came under Chapter IIIA (1962); co-operative banks came under RBI in 1966; forex "
      "management is unrelated to Chapter IIIB.",
  facts=[fact("1 Feb 1964: RBI empowered to regulate the deposit acceptance activities of non banking institutions. New "
              "chapter IIIB inserted in RBI Act", CH60),
         fact("1962: Chapter IIIA incorporated in RBI Act empowered the Bank to collect information in regard to credit "
              "facilities granted by individual banks", CH60)])
Q("008", T, "Issuer of currency", "Intermediate",
  "On 12 January 1946, high denomination banknotes were demonetised to curb unaccounted money. Which denominations?",
  ["₹500, ₹1000 and ₹10,000", "₹1000, ₹5000 and ₹10,000", "₹100, ₹500 and ₹1000", "₹1000 and ₹10,000 only"],
  concept="Demonetisations in India",
  explanation="RBI's chronology and currency FAQs record that ₹500, ₹1000 and ₹10,000 notes were demonetised in January "
              "1946. Notes of ₹1000, ₹5000 and ₹10,000 were reintroduced in 1954 and demonetised again in January 1978.",
  steps=["1946: ₹500, ₹1000, ₹10,000", "1978: ₹1000, ₹5000, ₹10,000"],
  why="₹1000/₹5000/₹10,000 is the 1978 set; ₹5000 notes did not exist in 1946; ₹100 notes were not demonetised.",
  facts=[fact("12 Jan 1946: High Denomination Bank Notes of Rs 500, Rs 1000 and Rs 10,000 Demonetised to curb unaccounted "
              "money", CH35),
         fact("₹500, ₹1000 and ₹10000 banknotes, which were then in circulation were demonetized in January 1946", CUR)])

Q("008", T, "Issuer of currency", "Advanced",
  "Consider the following statements about pre-2005 series banknotes, according to RBI's currency FAQs:\n"
  "I. Notes issued after the introduction of the MG series-2005 carry the year of printing on the reverse, which "
  "pre-2005 notes do not.\n"
  "II. RBI's facility for exchanging pre-2005 notes is available only at specified offices of the Reserve Bank.\n"
  "III. Banks cannot accept pre-2005 notes as deposits for credit to customers' accounts.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Withdrawal of old-series notes",
  explanation="MG series-2005 and later notes show the year of printing on the reverse (I). RBI's exchange facility for "
              "pre-2005 notes is available only at listed RBI offices (II). RBI clarifies that this does not mean banks "
              "cannot accept pre-2005 notes as deposits for crediting customers' accounts, so III is wrong.",
  steps=["I: true", "II: true", "III: false – banks may accept them as deposits"],
  why="Options with III are wrong; 'I only' leaves out the true statement II.",
  facts=[fact("banknotes issued after introduction of MG series-2005 have the year of printing on the reverse of the "
              "banknotes which is not present in the pre-2005 series", CUR),
         fact("The exchange facility for pre-2005 banknotes is available only at the following offices of the Reserve "
              "Bank ... This, however, does not imply that banks cannot accept deposits of pre-2005 banknotes for "
              "crediting to the customers' accounts", CUR)])
Q("009", T, "Issuer of currency", "Basic",
  "According to RBI's chronology, in which year was a security thread introduced on Indian banknotes for the first "
  "time as a security feature?",
  ["1944", "1938", "1950", "1967"],
  concept="History of banknote security features",
  explanation="RBI's chronology for 1935–1949 records that in 1944 'the security thread on notes [was] introduced for "
              "the first time in India as a security feature'.",
  steps=["Security thread → 1944"],
  why="1938 is when RBI issued its first notes; 1950 and 1967 are not the year of this feature.",
  facts=[fact("1944: The security thread on notes introduced for the first time in India as a security feature", CH35)])
Q("009", T, "Issuer of currency", "Intermediate",
  "On the ₹200, ₹500 and ₹2000 banknotes, the numeral of the denomination is printed in colour-shifting ink. How does "
  "it change?",
  ["Green when the note is held flat, changing to blue when the note is tilted",
   "Blue when held flat, changing to green when tilted", "Silver when held flat, changing to gold when tilted",
   "It glows yellow only under ultraviolet light"],
  concept="Security features of banknotes",
  explanation="RBI's FAQs say the numerals 200, 500 and 2000 are printed in colour-shifting ink: green when the note is "
              "held flat, changing to blue when held at an angle.",
  steps=["Flat → green", "Tilted → blue"],
  why="The colours are reversed in the second option; silver/gold is not the feature; yellow fluorescence under UV "
      "describes the security thread.",
  facts=[fact("The numeral 200, 500 & 2000 on the ₹200, ₹500, and ₹2000* banknotes are printed in a colour-shifting ink. "
              "The colour of these numerals appears green when the banknotes are held flat but would change to blue "
              "when the banknotes are held at an angle", CUR)])
Q("009", T, "Regulator and supervisor", "Intermediate",
  "In 1978 RBI introduced the 'Annual Appraisal of Banks'. What was it in the nature of?",
  ["A management audit of banks' organisation, manpower planning, systems, funds and credit management",
   "A stress test of banks' capital against market shocks",
   "A credit rating of banks for deposit insurance premium",
   "An audit of banks' foreign exchange transactions under FERA"],
  concept="Evolution of bank supervision",
  explanation="RBI's chronology records that the Annual Appraisal of Banks, introduced in 1978, was in the nature of a "
              "management audit, examining organisational set-up, manpower planning, supervision of branches, systems "
              "and procedures, funds management and credit management.",
  steps=["1978 Annual Appraisal → management audit"],
  why="Stress tests, risk-based deposit insurance ratings and FERA audits were not its purpose.",
  facts=[fact("1978: Annual Appraisal of Banks introduced in the nature of management audit introduced. Emphasis mainly "
              "on the examination of the organizational set-up, manpower planning, machinery for supervision and "
              "control over branches, systems & procedures in key areas, funds management and management of credit",
              CH68)])
Q("009", T, "Banker to government", "Intermediate",
  "In 1944, the laws relating to Government securities and the management of public debt by RBI were consolidated on "
  "the basis of which Act, now listed by RBI along with the Government Securities Act, 2006?",
  ["The Public Debt Act, 1944", "The Indian Coinage Act, 1906", "The Defence of India Act, 1939",
   "The Securities Contracts (Regulation) Act, 1956"],
  concept="Public debt management by RBI",
  explanation="RBI's chronology records that in 1944 the laws relating to Government securities and RBI's management of "
              "public debt were consolidated on the basis of the Public Debt Act, 1944. RBI lists 'Public Debt Act, "
              "1944 / Government Securities Act, 2006' among the Acts it administers.",
  steps=["Public debt law consolidated (1944) → Public Debt Act, 1944 → now Government Securities Act, 2006"],
  why="The Coinage Act concerned coins; the Defence of India Rules were wartime powers; SCRA 1956 concerns securities "
      "markets generally.",
  facts=[fact("1944: Laws relating to Government securities and to the management of Public Debt by the Reserve Bank of "
              "India consolidated on the basis of the Public Debt Act, 1944", CH35),
         fact("Acts administered by Reserve Bank of India: Public Debt Act, 1944 / Government Securities Act, 2006", ORG)])
Q("009", T, "Issuer of currency", "Advanced",
  "Consider the following definitions given in RBI's currency FAQs:\n"
  "I. A 'soiled note' includes a two-piece note pasted together where both pieces belong to the same note and form the "
  "entire note with no essential feature missing.\n"
  "II. A 'mutilated banknote' is one of which a portion is missing or which is composed of more than two pieces.\n"
  "III. An 'imperfect banknote' is one that is obliterated, shrunk, washed, altered or indecipherable, and includes a "
  "mutilated note.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Soiled, mutilated and imperfect notes",
  explanation="A soiled note includes a two-piece note pasted together with both pieces of the same note and no "
              "essential feature missing (I). A mutilated note has a portion missing or more than two pieces (II). An "
              "imperfect note is wholly or partially obliterated, shrunk, washed, altered or indecipherable but does "
              "NOT include a mutilated note, so III is wrong.",
  steps=["I: true", "II: true", "III: false – imperfect excludes mutilated"],
  why="Options with III are wrong; 'I only' leaves out the true statement II.",
  facts=[fact("A 'soiled note' means a note which has become dirty due to normal wear and tear and includes a two-piece "
              "note pasted together wherein both the pieces presented belong to the same note and form the entire note "
              "with no essential feature missing", CUR),
         fact("'Mutilated banknote' is a banknote, of which a portion is missing, or which is composed of more than two "
              "pieces. 'Imperfect banknote' means any banknote, which is wholly or partially, obliterated, shrunk, "
              "washed, altered or indecipherable but does not include a mutilated banknote", CUR)])

_crar, _gnpa, _gnpa0, _nim, _nim0 = 17.87, 1.67, 2.22, 3.22, 3.26
assert _gnpa < _gnpa0 and _nim < _nim0 and round(_gnpa0 - _gnpa, 2) == 0.55
Q("009", T, "Regulator and supervisor", "Advanced",
  "The RBI Governor's statement of 7 October 2026 reported these system-level parameters of scheduled commercial banks "
  "for June 2026 (June 2025 in brackets): CRAR 17.87%; GNPA ratio 1.67% (2.22%); NNPA ratio 0.39% (0.51%); net "
  "interest margin 3.22% (3.26%); LCR 126.74%. Consider:\n"
  "I. The GNPA ratio improved by 55 basis points over the year.\n"
  "II. The net interest margin widened over the year.\n"
  "III. Both CRAR and LCR were above their regulatory minimums.\n"
  "Which of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="Reading supervisory indicators",
  explanation="GNPA fell from 2.22% to 1.67%, an improvement of 0.55 percentage point (I). NIM slipped from 3.26% to "
              "3.22%, i.e. it narrowed, so II is wrong. The Governor described CRAR of 17.87% as well above the "
              "regulatory minimum, and LCR of 126.74% is above the 100% requirement (III).",
  steps=["I: 2.22 − 1.67 = 0.55 → true", "II: 3.26 → 3.22 narrowed → false", "III: true"],
  why="Options with II are wrong; the remaining option with I and III is correct.",
  computed=True, current=ca("2026-10-07"),
  facts=[fact("The system-level Capital to Risk Weighted Assets Ratio (CRAR) of 17.87 per cent in June 2026 was well above "
              "the regulatory minimum level ... GNPA ratio at 1.67 per cent in June 2026 vis-à-vis 2.22 per cent in June "
              "2025, NNPA Ratio at 0.39 per cent in June 2026 vis-à-vis 0.51 per cent in June 2025). Liquidity buffers "
              "were robust, with an LCR of 126.74 per cent ... Net Interest Margin was 3.22 per cent for June 2026 (3.26 "
              "per cent in June 2025)", GOV_OCT26)])
Q("009", T, "Issuer of currency", "Advanced",
  "Consider the following statements about coins, according to RBI's currency FAQs:\n"
  "I. Coins are issued for circulation only through the Reserve Bank, in terms of Section 38 of the RBI Act.\n"
  "II. The Government of India is responsible for designing and minting coins under the Coinage Act, 2011.\n"
  "III. Small Coin Depots stock and distribute coins of one rupee and above.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Roles of RBI and Government in coinage",
  explanation="Coins are minted by SPMCIL and issued for circulation only through RBI under Section 38 (I). The "
              "Government designs and mints coins under the Coinage Act, 2011; RBI's role is limited to distribution "
              "(II). Small Coin Depots stock small coins, i.e. coins of value below one rupee, so III is wrong.",
  steps=["I: true", "II: true", "III: false – small coins = below ₹1"],
  why="Options with III are wrong; 'I only' leaves out the true statement II.",
  facts=[fact("The coins are issued for circulation only through the Reserve Bank in terms of Section 38 of the RBI Act",
              CUR),
         fact("In respect of coins, the role of RBI is limited to distribution of coins that are supplied by Government of "
              "India (GoI). The GoI is responsible for designing and minting of coins in various denominations as per "
              "the Coinage Act, 2011", CUR),
         fact("Some banks are authorised to establish Small Coin Depots to stock and distribute small coins i.e. coins of "
              "value below Rupee One", CUR)])

Q("010", T, "Issuer of currency", "Basic",
  "What is the purpose of RBI's Mobile Aided Note Identifier (MANI) app?",
  ["To help visually impaired persons identify the denomination of a banknote; it does not check genuineness",
   "To verify whether a banknote is genuine or counterfeit", "To report counterfeit notes to the police",
   "To locate the nearest currency chest"],
  concept="RBI's tools for the visually impaired",
  explanation="MANI is a free RBI app that identifies the denomination of MG Series and MG (New) Series notes, even "
              "half-folded and in low light, without needing the internet. RBI notes that it does not authenticate a "
              "note as genuine or counterfeit.",
  steps=["MANI → denomination identification only"],
  why="It does not authenticate notes, report counterfeits or locate currency chests.",
  facts=[fact("Mobile Aided Note Identifier (MANI) is a mobile application launched by the Reserve Bank for aiding "
              "visually impaired persons to identify the denomination of Indian Banknotes ... This mobile application "
              "does not authenticate a note as being either genuine or counterfeit", CUR)])
Q("010", T, "Issuer of currency", "Basic",
  "Under the old Indian coinage system recalled in RBI's 'Anecdotes and Trivia', how many pies made one rupee?",
  ["192", "64", "100", "16"],
  concept="Old Indian coinage",
  explanation="3 pies made a pice, 4 pice an anna and 16 annas a rupee, so a rupee was 3 × 4 × 16 = 192 pies. Minting "
              "of the copper pie was discontinued after 1942.",
  steps=["3 × 4 × 16 = 192"],
  why="64 is the number of pice in a rupee; 16 the number of annas; 100 paise came with decimal coinage.",
  facts=[fact("3 pies made a pice; 4 pice made an anna and 16 annas made a rupee. One rupee, thus consisted of 192 pies",
              ANEC)])
Q("010", T, "Regulator and supervisor", "Basic",
  "The Banking Companies Act, 1949, which formed the statutory basis of bank supervision and regulation in India, was "
  "later renamed as the:",
  ["Banking Regulation Act", "Reserve Bank of India Act", "Banking Laws (Amendment) Act",
   "Banking Companies (Acquisition and Transfer of Undertakings) Act"],
  concept="Statutory basis of bank regulation",
  explanation="RBI's chronology says the Banking Companies Act, 1949, which came into force on 16 March 1949, formed the "
              "statutory basis of bank supervision and regulation and was later renamed the Banking Regulation Act.",
  steps=["Banking Companies Act, 1949 → renamed Banking Regulation Act"],
  why="The RBI Act (1934) is a separate law; the other two are different statutes.",
  facts=[fact("Coming into force of the Banking Companies Act, 1949. This formed the statutory basis of bank supervision "
              "and regulation in India ... The Banking Companies Act was later renamed the Banking Regulation Act", CH35)])
Q("010", T, "Issuer of currency", "Intermediate",
  "According to RBI's currency FAQs, in which year were banknotes with the legend 'Satyameva Jayate' introduced for the "
  "first time?",
  ["1970", "1949", "1954", "1996"],
  concept="History of Indian banknotes",
  explanation="The first note of independent India was the one-rupee note of 1949; names and the guarantee clause "
              "appeared in Hindi from 1951; high denominations returned in 1954; notes with 'Satyameva Jayate' (truth "
              "alone shall prevail) were introduced for the first time in 1970; the Mahatma Gandhi series came in 1996.",
  steps=["'Satyameva Jayate' legend → 1970"],
  why="1949 is the first one-rupee note of independent India; 1954 the return of ₹1000/₹5000/₹10000; 1996 the MG "
      "series.",
  facts=[fact("In the year 1970, banknotes with the legend \"Satyameva Jayate\", i.e., truth alone shall prevail were "
              "introduced for the first time", CUR)])
Q("010", T, "Issuer of currency", "Intermediate",
  "What does the 'I promise to pay the bearer the sum of …' clause on a banknote signify, according to RBI?",
  ["RBI's obligation, under Section 26 of the RBI Act, to pay the value of the note to the holder on demand",
   "A promise by the Government to redeem the note in gold",
   "The personal guarantee of the Governor who signed it",
   "That the note can be exchanged only at the bank that issued it"],
  concept="Promissory clause",
  explanation="Under Section 26 of the RBI Act, RBI is liable to pay the value of a banknote, payable on demand by RBI as "
              "the issuer. The promissory clause denotes this obligation towards the holder.",
  steps=["Section 26 → RBI liable for value of note → promissory clause"],
  why="There is no gold convertibility; the signature is official, not a personal guarantee; notes are not tied to "
      "any particular bank.",
  facts=[fact("As per Section 26 of Reserve Bank of India Act, 1934, the Bank is liable to pay the value of banknote. This "
              "is payable on demand by RBI, being the issuer. The promissory clause ... denotes the obligation on the "
              "part of the Bank towards the holder of the bank note", CUR)])
Q("010", T, "Regulator and supervisor", "Intermediate",
  "Model Co-op. Bank Ltd. was included in the Second Schedule to the RBI Act, 1934 by a notification published in the "
  "Gazette on 11 November 2025. What does inclusion in the Second Schedule make a bank?",
  ["A scheduled bank", "A systemically important bank", "A Small Finance Bank", "A bank exempt from CRR"],
  concept="Scheduled banks",
  explanation="Banks included in the Second Schedule to the RBI Act are 'scheduled banks'. RBI announced on 2 December "
              "2025 that Model Co-op. Bank Ltd. had been included by its notification of 20 October 2025, published in "
              "the Gazette on 11 November 2025.",
  steps=["Second Schedule inclusion → scheduled bank"],
  why="Systemic importance is a separate (D-SIB) framework; inclusion does not change the bank's type or exempt it from "
      "CRR.",
  current=ca("2025-11-11"),
  facts=[fact("\"Model Co-op. Bank Ltd.\" has been included in the Second Schedule to the Reserve Bank of India Act, 1934 "
              "vide Notification ... dated October 20, 2025 and published in the Gazette of India ... dated November 11, "
              "2025", MODEL_COOP)])
Q("010", T, "Issuer of currency", "Advanced",
  "Consider the following statements about the angular bleed lines and identification marks on Mahatma Gandhi (New) "
  "Series banknotes, according to RBI's FAQs:\n"
  "I. The ₹100 note has 4 angular bleed lines in 2 blocks.\n"
  "II. The ₹500 note has 5 angular bleed lines in 3 blocks.\n"
  "III. The size of the identification marks on notes of ₹100 and above was increased by 25 per cent.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Features for the visually challenged",
  explanation="Angular bleed lines: 4 lines in 2 blocks on ₹100, 4 lines with two circles in between on ₹200, 5 lines in "
              "3 blocks on ₹500 and 7 on ₹2000 (I, II). The identification marks on ₹100 and above were enlarged by 50 "
              "per cent, not 25, so III is wrong.",
  steps=["I: true", "II: true", "III: false – increased by 50%"],
  why="Options with III are wrong; 'I only' leaves out the true statement II.",
  facts=[fact("Angular Bleed Lines have been introduced in banknotes - 4 lines in 2 blocks in ₹100, 4 angular bleed lines "
              "with two circles in between in ₹200, 5 lines in 3 blocks in ₹500, 7 in ₹2000*. In addition, the size of "
              "the identification marks in denominations ₹100 and above have been increased by 50 percent", CUR)])

WMA_ADV = _P + "63689"
Q("009", "RBI Functions", "Banker to government", "Advanced",
  "Consider the following statements about the Report of the Advisory Committee on Ways and Means Advances to State "
  "Governments, placed on RBI's website on 29 September 2026:\n"
  "I. The Committee was chaired by Shri I. S. N. Prasad, former Additional Chief Secretary, Government of Karnataka.\n"
  "II. Its terms of reference included a review of State-wise WMA limits and other financial accommodation facilities "
  "available to the States.\n"
  "III. RBI announced that the Committee's recommendations had come into force on the date of the report.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I and III only", "II only", "I, II and III"],
  concept="RBI's financial accommodation to States",
  explanation="RBI constituted the Advisory Committee under Shri I. S. N. Prasad (I); its terms of reference included "
              "reviewing State-wise WMA limits and other facilities (II). RBI said the recommendations 'shall be "
              "examined by the Reserve Bank'; they were not put into force with the report, so III is wrong.",
  steps=["I: true", "II: true", "III: false – recommendations to be examined"],
  why="Options with III are wrong; 'II only' leaves out the true statement I.",
  current=ca("2026-09-29"),
  facts=[fact("The Reserve Bank had constituted an Advisory Committee, under the Chairmanship of Shri I S N Prasad, former "
              "Additional Chief Secretary, Government of Karnataka. The terms of reference of the Advisory Committee "
              "included, inter alia, review of State-wise WMA limits and other financial accommodation facilities "
              "available to the States. The Committee has made various recommendations which shall be examined by the "
              "Reserve Bank", WMA_ADV)])


MISC = _MD + "13136"      # CB - Miscellaneous Directions, 2025 (updated 19 Oct 2026): DEA Fund chapter
ASSAM_APEX = _P + "62180"
MIZO_APEX = _P + "62638"
RABO_EXCL = _P + "63239"
RABO_CEASE = _P + "63238"
COASTAL_LAB = _P + "63518"
PAYTM_EXCL = _P + "63751"

# ============================================================================================ Banking Fundamentals
T = "Banking Fundamentals"
Q("008", T, "Types of accounts", "Basic",
  "Under RBI's Commercial Banks – Interest Rate on Deposits Directions, 2025, on what basis must a bank calculate "
  "interest on domestic rupee savings deposits?",
  ["On a daily product basis", "On the minimum balance between the 10th and the last day of the month",
   "On the average monthly balance", "On the balance at the end of each quarter"],
  concept="Interest on savings accounts",
  explanation="The Directions require interest on savings deposits to be calculated on a daily product basis, i.e. on "
              "the end-of-day balance. The older 'minimum balance between the 10th and last day' method survives only as "
              "a discretion for the composite cash credit account of a farmer.",
  steps=["Savings deposit interest → daily product (end-of-day balance)"],
  why="The 10th-to-last-day minimum balance applies only to farmers' composite cash credit accounts; average monthly or "
      "quarter-end balances are not the rule.",
  facts=[fact("Interest shall be calculated on a daily product basis", DEP),
         fact("'Daily Product' means the interest applied on the end of day balance", DEP)])
Q("008", T, "Cheques and instruments", "Basic",
  "From which date were banks advised to issue only CTS-2010 standard compliant cheques?",
  ["30 September 2012", "1 February 2008", "31 December 2018", "13 October 2023"],
  concept="CTS-2010 standard cheques",
  explanation="RBI advised banks to issue only CTS-2010 compliant cheques from 30 September 2012. Separate clearing "
              "sessions for non-CTS cheques continued until 31 December 2018. CTS began in New Delhi on 1 February 2008, "
              "and the three grids merged into a National Grid on 13 October 2023.",
  steps=["CTS-2010-only cheques from 30 Sep 2012"],
  why="1 Feb 2008 is the start of the New Delhi grid; 31 Dec 2018 the end of non-CTS clearing; 13 Oct 2023 the National "
      "Grid.",
  facts=[fact("Banks have been advised to issue only CTS-2010 standard compliant cheques from September 30, 2012", CHQ)])
Q("008", T, "Types of accounts", "Basic",
  "As defined in RBI's Interest Rate on Deposits Directions, 2025, a 'Notice Deposit' is a term deposit for a specific "
  "period that can be withdrawn on giving at least:",
  ["One complete banking day's notice", "Seven days' notice", "One month's notice", "Fifteen days' notice"],
  concept="Types of deposits",
  explanation="A Notice Deposit is a term deposit for a specific period but withdrawable on giving at least one complete "
              "banking day's notice.",
  steps=["Notice deposit → withdrawable after ≥ 1 complete banking day's notice"],
  why="Seven days is the minimum tenor of a domestic term deposit, not the notice period; the other periods are not in "
      "the definition.",
  facts=[fact("'Notice Deposit' means term deposit for specific period but withdrawable on giving at least one complete "
              "banking day's notice", DEP)])
Q("008", T, "Cheques and instruments", "Basic",
  "According to RBI's FAQs on cheque clearing, can a bank branch refuse to give an acknowledgement when a customer "
  "tenders a cheque for collection at its counter and asks for one?",
  ["No; banks must provide both a drop-box facility and an acknowledgement facility, and cannot refuse an "
   "acknowledgement at the counter",
   "Yes; acknowledgements are given only for cheques above ₹1 lakh",
   "Yes; if the bank has a cheque drop box, it need not give acknowledgements",
   "No; but the bank may charge a fee for each acknowledgement"],
  concept="Customer rights in cheque collection",
  explanation="Banks are required to provide both the cheque drop box facility and the acknowledgement facility at "
              "collection counters, and no branch can refuse an acknowledgement if the customer asks for it while "
              "tendering a cheque at the counter.",
  steps=["Drop box AND acknowledgement facility both required", "Refusal not allowed"],
  why="There is no value threshold, the drop box does not replace the acknowledgement, and RBI does not mention a fee.",
  facts=[fact("Banks are required to provide both the cheque drop box facility and the acknowledgement facility at their "
              "collection counters. No bank branch can refuse to give an acknowledgement to the customer if the latter "
              "asks for the same while tendering cheque for collection at the bank branch's counter", CHQ)])
Q("008", T, "Types of accounts", "Intermediate",
  "A bank runs a term deposit scheme for resident Indian senior citizens offering higher, fixed rates. Under RBI's "
  "Interest Rate on Deposits Directions, 2025, which of the following deposits is NOT eligible for it?",
  ["A term deposit in the name of an HUF whose Karta is a resident senior citizen",
   "A term deposit of a resident Indian aged 62 held singly",
   "A term deposit of a resident Indian aged 70 held jointly with his spouse",
   "A term deposit of a retired staff member of the bank who is a resident senior citizen"],
  concept="Senior citizen deposit schemes",
  explanation="Banks may at their discretion run term deposit schemes for resident Indian senior citizens, but the "
              "facility is not offered on a term deposit in the name of an HUF or its Karta (as Karta), even if the "
              "Karta is a resident senior citizen. Retired staff who are senior citizens may even get the senior-citizen "
              "rate over and above their staff benefit.",
  steps=["Senior citizen scheme → individuals, not HUF/Karta"],
  why="Individual resident senior citizens (single or joint) qualify, and retired staff senior citizens may get both "
      "benefits.",
  facts=[fact("A bank may, at its discretion, formulate term deposit schemes specifically for resident Indian senior "
              "citizens ... Provided that this facility is not offered on the term deposit standing in the name of an HUF "
              "or the Karta of the HUF, even if the Karta is a resident Indian senior citizen", DEP),
         fact("A bank may, at its discretion, give its resident Indian retired staffs, who are senior citizens, the "
              "benefit of additional interest rates as admissible to senior citizens over and above the additional "
              "interest payable to them by virtue of their being retired members of the bank's staff", DEP)])
Q("008", T, "Types of accounts", "Intermediate",
  "Banks may offer term deposits without a premature withdrawal option. Under RBI's Interest Rate on Deposits "
  "Directions, 2025, which deposits must nevertheless carry a premature withdrawal facility?",
  ["All term deposits from individuals (single or joint) of ₹1 crore and below",
   "All term deposits of ₹3 crore and above (bulk deposits)",
   "All term deposits of companies and trusts, whatever the amount",
   "Only term deposits of senior citizens"],
  concept="Non-callable term deposits",
  explanation="Banks are free to offer term deposits without a premature withdrawal option, but every term deposit "
              "accepted from individuals, held singly or jointly, for ₹1 crore and below must have the premature "
              "withdrawal facility.",
  steps=["Non-callable deposits allowed", "Exception: individuals' deposits ≤ ₹1 crore must be callable"],
  why="Bulk deposits (₹3 crore+) and deposits of companies can be non-callable; the protection is not limited to "
      "senior citizens.",
  facts=[fact("A bank shall have the freedom to offer term deposits without premature withdrawal option. Provided that all "
              "term deposits accepted by a bank from individuals (held singly or jointly) for amount of ₹1 crore and "
              "below shall have premature withdrawal facility", DEP)])
Q("008", T, "Cheques and instruments", "Intermediate",
  "Banks must enable the Positive Pay System for account holders issuing cheques of ₹50,000 and above. According to "
  "RBI's FAQs, for cheques of what value may banks consider making Positive Pay mandatory?",
  ["₹5,00,000 and above", "₹1,00,000 and above", "₹10,00,000 and above", "₹2,00,000 and above"],
  concept="Positive Pay System",
  explanation="Under Positive Pay, the drawer sends key cheque details to the bank in advance, and CTS cross-checks "
              "them. Availing it is at the account holder's discretion, but banks may consider making it mandatory for "
              "cheques of ₹5,00,000 and above.",
  steps=["Enable for ≥ ₹50,000 (customer's choice)", "May be mandatory for ≥ ₹5 lakh"],
  why="₹1 lakh is the free-collection limit for savings accounts; ₹2 lakh and ₹10 lakh are not RBI's thresholds here.",
  facts=[fact("Banks have been advised to enable PPS facility for all account holders issuing cheques for amount of "
              "₹50,000 and above. While availing of this facility is at the discretion of the account holder, banks may "
              "consider making it mandatory in case of cheques for amounts of ₹5,00,000 and above", CHQ)])
Q("008", T, "Types of banks", "Intermediate",
  "On 2 July 1966, soon after co-operative banks were brought under RBI's regulatory ambit, what change did RBI's "
  "chronology record for State Co-operative Banks?",
  ["12 State Co-operative Banks were included in the Second Schedule to the RBI Act",
   "All State Co-operative Banks were converted into Regional Rural Banks",
   "State Co-operative Banks were brought under DICGC deposit insurance",
   "State Co-operative Banks were merged with NABARD"],
  concept="Co-operative banks as scheduled banks",
  explanation="RBI's chronology records that co-operative banks came under RBI's regulatory ambit on 1 March 1966, and "
              "on 2 July 1966, 12 State Co-operative Banks were included in the Second Schedule to the RBI Act.",
  steps=["1 Mar 1966 → co-op banks under RBI regulation", "2 Jul 1966 → 12 StCBs scheduled"],
  why="RRBs came only in 1975; deposit insurance reached co-operative banks in 1971; NABARD was set up in 1982.",
  facts=[fact("2 Jul 1966: 12 State Cooperative Banks included in Second Schedule of RBI Act", CH60),
         fact("01 Jul 1971: Deposit Insurance cover extended to cooperative banks", CH68)])
Q("008", T, "Types of accounts", "Intermediate",
  "Under RBI's Interest Rate on Deposits Directions, 2025, by what time on each business day must a bank disclose on "
  "its website the interest rates it pays on bulk deposits?",
  ["10:00 am, with a grace time up to 10:10 am", "9:00 am, with no grace time",
   "At the close of business of the previous day", "12:00 noon, with a grace time up to 12:30 pm"],
  concept="Transparency in bulk deposit pricing",
  explanation="Deposit rates, including on bulk deposits, must follow the schedule disclosed in advance on the bank's "
              "website. Bulk deposit rates must be disclosed at 10:00 am, with a grace time of 10 minutes (latest 10:10 "
              "am), on each business day, and the bulk deposit rate card must be kept in the Core Banking System.",
  steps=["Bulk deposit rate disclosure → 10:00 am (latest 10:10 am) daily"],
  why="The other timings are not in the Directions.",
  facts=[fact("interest rates payable on bulk deposits shall be disclosed on the bank's website at 10:00 am with a grace "
              "time of 10 minutes, latest by 10:10 am, on each business day", DEP)])

arr = 4.30
c_2y, c_4y = round(arr + 2.50, 2), round(arr + 3.50, 2)
assert (c_2y, c_4y) == (6.80, 7.80)
Q("008", T, "Types of accounts", "Advanced",
  "A bank sets fixed rates for FCNR(B) US dollar deposits for December 2026. The overnight Alternative Reference Rate "
  "for USD on the last working day of November is 4.30% (assume). Under RBI's Interest Rate on Deposits Directions, "
  "2025, what are the maximum rates it can offer on a 2-year and on a 4-year deposit?",
  ["6.80% and 7.80%", "6.80% and 6.80%", "7.30% and 8.30%", "5.30% and 6.30%"],
  concept="Interest rate ceilings on FCNR(B) deposits",
  explanation="Fixed-rate FCNR(B) deposits are capped with reference to the overnight ARR for the currency as on the "
              "last working day of the preceding month: ARR + 250 bps for 1 year to less than 3 years and ARR + 350 bps "
              "for 3 to 5 years. 4.30 + 2.50 = 6.80%; 4.30 + 3.50 = 7.80%.",
  steps=["2-year (1 to <3 yr): 4.30 + 2.50 = 6.80%", "4-year (3 to 5 yr): 4.30 + 3.50 = 7.80%"],
  why="6.80% for both ignores the higher ceiling for 3–5 years; 7.30%/8.30% and 5.30%/6.30% use wrong spreads.",
  computed=True,
  facts=[fact("One year to less than three years: Overnight ARR for the respective currency / Swap plus 250 basis points; "
              "Three years and above upto and including five years: Overnight ARR for the respective currency / Swap plus "
              "350 basis points", DEP),
         fact("The Overnight ARR for the respective currency / SWAP rates as on the last working day of the preceding "
              "month shall form the base for fixing ceiling rates for the interest rates offered effective in the "
              "following month", DEP)])

dea_claim, cover = 7.5, 5.0
assert min(dea_claim, cover) == 5.0 and dea_claim - cover == 2.5
Q("008", T, "Types of accounts", "Advanced",
  "A depositor's unclaimed deposit of ₹7.5 lakh (with interest) had been moved to the DEA Fund when it was insured by "
  "DICGC (cover ₹5 lakh). The bank is now in liquidation and she claims the money. Under RBI's Miscellaneous "
  "Directions, how is the claim settled?",
  ["The Fund pays ₹5 lakh to the liquidator, who pays her; the liquidator pays the remaining ₹2.5 lakh first and then "
   "seeks reimbursement from the Fund",
   "The Fund pays the entire ₹7.5 lakh to the liquidator in advance",
   "DICGC pays her ₹5 lakh directly and the remaining ₹2.5 lakh is forfeited",
   "She must claim from the bank's assets only, since the money is no longer in the bank"],
  concept="DEA Fund claims when a bank is in liquidation",
  explanation="If the deposit was DICGC-insured when transferred, the liquidator claims from the Fund an amount equal to "
              "what could have been claimed from DICGC (₹5 lakh) and pays the depositor. The excess (₹2.5 lakh) is paid "
              "by the liquidator first and claimed from the Fund only by way of reimbursement.",
  steps=["Insured part: min(7.5, 5) = ₹5 lakh paid by Fund upfront", "Excess ₹2.5 lakh: liquidator pays, then is "
         "reimbursed"],
  why="The Fund does not prefund the excess; the amount is not forfeited; the claim is routed through the liquidator "
      "and the Fund, not the bank's assets alone.",
  computed=True,
  facts=[fact("If the deposits of a customer / depositor were covered by DICGC insurance at the time of transfer to the DEA "
              "Fund, then the Liquidator can claim an amount equivalent to what could have been claimed from DICGC ... "
              "If the above deposit amount is more than the insurance cover of DICGC, then the Liquidator shall claim the "
              "amount in excess of DICGC insurance cover only on reimbursement basis", MISC)])

td, sb, contract, days = 200000, 2.5, 7.0, 73
interest = td * min(sb, contract) / 100 * days / 365
assert round(interest) == 1000 and round(td * contract / 100 * days / 365) == 2800
Q("008", T, "Types of accounts", "Advanced",
  "Anu's term deposit of ₹2,00,000 at 7.00% matured, but she collected the proceeds only 73 days later. The bank's "
  "savings deposit rate is 2.50%. Under RBI's Interest Rate on Deposits Directions, 2025, what interest (simple, 365-day "
  "year) is due for the 73 days after maturity?",
  ["₹1,000", "₹2,800", "Nil", "₹1,900"],
  concept="Interest on matured but unclaimed term deposits",
  explanation="A matured, unpaid term deposit attracts the savings account rate or the contracted rate, whichever is "
              "lower. min(2.50%, 7.00%) = 2.50%: 2,00,000 × 2.5% × 73/365 = ₹1,000.",
  steps=["Rate = lower of SB rate and contracted rate = 2.50%", "2,00,000 × 0.025 × 73/365 = ₹1,000"],
  why="₹2,800 uses the contracted 7%; interest is not nil; ₹1,900 uses neither rate.",
  computed=True,
  facts=[fact("If a Term Deposit (TD) matures and proceeds are unpaid, the amount left unclaimed with a bank, shall attract "
              "rate of interest as applicable to savings account or the contracted rate of interest on the matured TD, "
              "whichever is lower", DEP)])

Q("009", T, "Types of accounts", "Basic",
  "Under RBI's Interest Rate on Deposits Directions, 2025, which of the following may a bank NOT do with an NRE "
  "savings deposit?",
  ["Mark any lien, direct or indirect, against it", "Pay interest on it at quarterly intervals",
   "Calculate interest on it on a daily product basis", "Accept it only if authorised under FEMA"],
  concept="NRE savings deposits",
  explanation="The Directions prohibit banks from marking any type of lien, direct or indirect, against NRE savings "
              "deposits. Interest on NRE/NRO savings deposits follows the domestic savings rules (daily product, credited "
              "quarterly or more often), and only FEMA-authorised banks may accept NRE/NRO deposits.",
  steps=["NRE savings → no lien of any kind"],
  why="Quarterly crediting and daily-product calculation are required, and FEMA authorisation is a condition, so those "
      "are all permitted or required.",
  facts=[fact("A bank shall not mark any type of lien, direct or indirect, against NRE saving deposits", DEP),
         fact("Rupee deposits of non-residents under NRE and NRO deposits shall be accepted only by those banks that are "
              "authorised under Foreign Exchange Management Act,1999", DEP)])
Q("009", T, "Cheques and instruments", "Basic",
  "In the Cheque Truncation System, what does 'cheque truncation' mean?",
  ["Stopping the flow of the physical cheque during clearing, once an electronic image is generated, at the "
   "presenting bank",
   "Cancelling a cheque that has crossed its validity period", "Converting a cheque into a demand draft",
   "Returning a dishonoured cheque to the drawer"],
  concept="Cheque truncation",
  explanation="Cheque truncation is the stopping of the physical cheque's flow in the clearing cycle as soon as an "
              "electronic image is generated for transmission. In India the presenting bank truncates the cheque, so "
              "physical instruments need not move across branches.",
  steps=["Image generated → physical cheque stops at presenting bank"],
  why="Truncation has nothing to do with stale cheques, demand drafts or returns.",
  facts=[fact("Cheque truncation means stopping the flow of a physical cheque during the course of a clearing cycle, "
              "immediately on generation of an electronic image for transmission. In the extant Cheque Truncation System "
              "(CTS) of India, physical cheques are truncated by the presenting bank", CHQ)])
Q("009", T, "Types of accounts", "Intermediate",
  "Under RBI's Interest Rate on Deposits Directions, 2025, a bank may, at its discretion, pay additional interest over "
  "its card rate on savings and term deposits of its staff (and of executives such as the Chairman and Executive "
  "Directors). How much?",
  ["One per cent per annum", "Half a per cent per annum", "Two per cent per annum", "Any amount the Board decides"],
  concept="Additional interest on staff deposits",
  explanation="Banks may allow additional interest of one per cent per annum over the scheduled rate on savings or term "
              "deposits of staff, their exclusive associations, and the Chairman, CMD, ED or other fixed-tenure "
              "executives. Bank employees' federations whose members are not direct members are not eligible, and the "
              "benefit is not available on NRE/NRO deposits.",
  steps=["Staff deposits → +1% p.a. (discretionary)"],
  why="The rate is fixed at one per cent; it is not half or two per cent or open-ended.",
  facts=[fact("A bank shall, at its discretion, allow additional interest of one per cent per annum, over and above the "
              "rate of interest mentioned in the schedule of interest rates on savings or term deposits to bank's staff "
              "and their exclusive associations as well as on deposits of Chairman, Chairman & Managing Director, "
              "Executive Director", DEP)])
Q("009", T, "Types of accounts", "Intermediate",
  "Under RBI's Interest Rate on Deposits Directions, 2025, what is the minimum tenor of an NRE term deposit, compared "
  "with that of an NRO term deposit?",
  ["NRE: one year; NRO: seven days", "NRE: seven days; NRO: one year", "Both: seven days", "Both: one year"],
  concept="Tenor of non-resident rupee deposits",
  explanation="Banks are free to set tenors, but the minimum tenor of NRE term deposits is one year and that of NRO "
              "term deposits seven days.",
  steps=["NRE ≥ 1 year", "NRO ≥ 7 days"],
  why="The second option reverses them; the others apply one rule to both.",
  facts=[fact("minimum tenor of NRE term deposits shall be one year and that of NRO term deposits shall be seven days", DEP)])
Q("009", T, "Types of accounts", "Intermediate",
  "How is interest on FCNR(B) deposits calculated and paid under RBI's Interest Rate on Deposits Directions, 2025?",
  ["On a 360-day year, paid at intervals of 180 days (with the option of receiving it on maturity with compounding)",
   "On a 365-day year, paid quarterly", "On a 360-day year, paid only on maturity", "On a 365-day year, paid monthly"],
  concept="FCNR(B) interest mechanics",
  explanation="Interest on FCNR(B) deposits is calculated on the basis of 360 days to a year and paid at intervals of 180 "
              "days each (and then for the remaining actual days); the depositor may opt to receive it on maturity with "
              "compounding. Floating-rate FCNR(B) deposits reset every six months.",
  steps=["Day count: 360", "Payment: every 180 days (or cumulative on maturity at depositor's option)"],
  why="FCNR(B) follows a 360-day convention and 180-day payment intervals, not quarterly or monthly payment.",
  facts=[fact("Interest on the deposits accepted under the Scheme shall be calculated on the basis of 360 days to a year",
              DEP),
         fact("The interest on FCNR (B) deposits shall be calculated and paid at intervals of 180 days each and thereafter "
              "for the remaining actual number of days. Provided that the option to receive the interest on maturity "
              "with compounding effect shall vest with the depositor", DEP)])
Q("009", T, "Types of accounts", "Intermediate",
  "A farmer has a composite cash credit account (a cash credit limit with a full savings module). Under RBI's Interest "
  "Rate on Deposits Directions, 2025, on what balance may the bank pay interest?",
  ["The minimum credit balance during the period from the 10th to the last day of each calendar month",
   "The average daily credit balance of the quarter", "The highest credit balance in the month",
   "No interest can ever be paid on such an account"],
  concept="Composite cash credit account",
  explanation="Interest, if any, on the minimum credit balance maintained in a farmer's composite cash credit account "
              "during the 10th to the last day of each calendar month may be paid, subject to the general conditions "
              "of the Directions.",
  steps=["Composite CC (farmer) → interest on minimum credit balance, 10th to month-end"],
  why="Quarterly averages and maximum balances are not the basis, and interest is permitted.",
  facts=[fact("Interest, if any, on the minimum credit balance in the composite cash credit account of a farmer maintained "
              "with a bank during the period from the 10th to the last day of each calendar month shall be paid", DEP),
         fact("'Composite Cash Credit' means a type of loan product having a cash credit limit with a fully savings "
              "module designed to take care of farmer's interest", DEP)])
Q("009", T, "Cheques and instruments", "Intermediate",
  "Which law, enacted in April 1989 according to RBI's chronology, introduced penalties for the dishonour of cheques "
  "to encourage the use of cheques in India?",
  ["Banking, Public Financial Institutions and Negotiable Instruments Laws (Amendment) Act, 1988",
   "Banking Laws (Amendment) Act, 1983", "Payment and Settlement Systems Act, 2007",
   "Banking Regulation (Amendment) Act, 2007"],
  concept="Legal backing for cheques",
  explanation="RBI's chronology records the Banking, Public Financial Institution and Negotiable Instruments Laws "
              "(Amendment) Act, 1988 (April 1989), enacted to encourage the use of cheques; it introduced penalties for "
              "the dishonour of cheques (the origin of Section 138 of the NI Act).",
  steps=["Penalties for cheque dishonour → 1988 amendment Act (Apr 1989)"],
  why="The 1983 Act dealt with nomination and leasing; the PSS Act governs payment systems; the 2007 BR amendment was "
      "about SLR and other matters.",
  facts=[fact("Apr 1989: Banking, Public Financial Institution and Negotiable Instruments Laws (Amendment) Act, 1988 "
              "enacted to encourage the culture of use of cheques in India. It introduced penalties for the dishonour of "
              "cheques", CH85)])
Q("009", T, "Types of accounts", "Intermediate",
  "At what rate of interest must a bank pay a claimant whose interest-bearing deposit had been transferred to the DEA "
  "Fund, for the period from the transfer, under the rate in force since 11 May 2021?",
  ["3 per cent per annum", "3.5 per cent per annum", "4 per cent per annum", "The savings bank rate of the bank"],
  concept="Interest on deposits transferred to the DEA Fund",
  explanation="The Miscellaneous Directions prescribe interest on the principal of unclaimed interest-bearing deposits "
              "transferred to the Fund at 4% up to 30 June 2018, 3.5% from 1 July 2018 to 10 May 2021, and 3% from 11 "
              "May 2021 till payment. Interest accrues only from the date of transfer to the Fund.",
  steps=["From 11 May 2021 → 3% p.a.", "Accrues from date of transfer to date of payment"],
  why="3.5% and 4% are the earlier rates; the bank's own savings rate does not apply.",
  facts=[fact("A bank shall calculate the interest payable ... on principal amount of unclaimed interest bearing deposits "
              "transferred to the Fund at the rate of 4 percent per annum up to June 30, 2018, 3.5 percent w.e.f. July "
              "1, 2018 up to May 10, 2021 and at 3 percent with effect from May 11, 2021 till the time of payment", MISC)])
Q("009", T, "Types of accounts", "Advanced",
  "An NRI's FCNR(B) deposit matured on 1 August. The bank's rate for the renewal period was 5.10% on 1 August and "
  "5.40% on 10 August. Under RBI's Interest Rate on Deposits Directions, 2025, which statement is correct?",
  ["If renewed on 10 August, the rate is 5.10%; if renewed after more than 14 days, interest for the overdue period is "
   "set by treating it as a fresh term deposit",
   "If renewed on 10 August, the rate is 5.40%, the rate on the date of renewal",
   "Renewal after maturity is not allowed for FCNR(B) deposits; a fresh deposit must be opened",
   "If renewed on 10 August, the depositor gets the higher of the two rates plus interest for the overdue days at 5.40%"],
  concept="Renewal of overdue FCNR(B) deposits",
  explanation="If the period from maturity to renewal (both days inclusive) does not exceed 14 days, the renewal rate is "
              "the rate prevailing on the date of maturity or on the date of renewal, whichever is lower: 1–10 August is "
              "10 days, so min(5.10%, 5.40%) = 5.10%. In other cases, interest for the overdue period is determined by "
              "treating it as a fresh term deposit.",
  steps=["1 Aug to 10 Aug inclusive = 10 days ≤ 14", "Rate = lower of 5.10% and 5.40% = 5.10%"],
  why="The rule gives the lower rate, not the renewal-date or higher rate; renewal of overdue deposits is permitted.",
  computed=True,
  facts=[fact("If the period from the date of maturity till the date of renewal (both days inclusive) does not exceed 14 "
              "days, the rate of interest payable on the amount of the deposit so renewed shall be the appropriate rate "
              "of interest for the period of renewal as prevailing on the date of maturity or on the date when the "
              "depositor seeks renewal, whichever is lower. In all other cases of renewal, interest rates for the overdue "
              "period on the renewed amount shall be determined by treating it as a fresh term deposit", DEP)])
Q("009", T, "Types of accounts", "Advanced",
  "Consider the following statements about RBI's temporary relaxation for non-resident deposits in 2026, as recorded "
  "in the Interest Rate on Deposits Directions, 2025:\n"
  "I. The rule that NRE deposit rates cannot exceed those on comparable domestic rupee term deposits was withdrawn for "
  "fresh and renewed NRE deposits of three years and above, from 17 June 2026 until 31 August 2026.\n"
  "II. The interest rate ceiling on fresh and renewed FCNR(B) deposits of three to five years was withdrawn for the same "
  "period.\n"
  "III. Transfers from NRO accounts to NRE accounts also qualified for the NRE exemption.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I and III only", "II only", "I, II and III"],
  concept="Measures to attract non-resident deposits",
  explanation="Footnotes to the Directions record that, from 17 June 2026 to 31 August 2026, the cap tying NRE rates to "
              "domestic rates was lifted for fresh/renewed NRE deposits of three years and above (I), and the ceiling on "
              "fresh/renewed FCNR(B) deposits of three to five years was withdrawn (II). Transfers from NRO to NRE "
              "accounts were expressly excluded from the exemption, so III is wrong.",
  steps=["I: true", "II: true", "III: false – NRO→NRE transfers excluded"],
  why="Options with III are wrong; 'II only' leaves out the true statement I.",
  current=ca("2026-06-17"),
  facts=[fact("The said restriction with respect to interest rates offered on fresh NRE deposits mobilised by banks, "
              "including the deposits that are renewed upon maturity, for three years and above tenors, is temporarily "
              "withdrawn with effect from June 17, 2026, for the period until August 31, 2026. Any transfer from NRO "
              "accounts to NRE accounts shall not qualify for such exemption", DEP),
         fact("The interest rate ceiling applicable to fresh FCNR(B) deposits mobilised by banks, including the deposits "
              "that are renewed upon maturity, for three years and above-upto and including five years tenors, is "
              "temporarily withdrawn with effect from June 17, 2026, for the period until August 31, 2026", DEP)])
Q("009", T, "Types of accounts", "Advanced",
  "Consider the following statements about penalties on premature withdrawal of term deposits under RBI's Interest "
  "Rate on Deposits Directions, 2025:\n"
  "I. If the components of the penalty were not brought to the depositor's notice when the deposit was accepted, no "
  "penalty can be levied.\n"
  "II. When claimants of a deceased depositor ask for the deposit to be split, no premature withdrawal penalty is "
  "levied if the period and aggregate amount do not change.\n"
  "III. When a rural branch is taken over by another bank, depositors who withdraw prematurely because of the transfer "
  "must pay the usual premature withdrawal penalty.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Premature withdrawal penalties",
  explanation="The Directions say penalty components must be disclosed when the deposit is accepted, failing which no "
              "penalty is levied (I), and no penalty applies when a deceased depositor's deposit is split at the "
              "claimants' request without changing period or aggregate amount (II). No penalty is levied where depositors of a "
              "rural or semi-urban branch taken over by another bank withdraw prematurely because of the transfer, so "
              "III is wrong.",
  steps=["I: true", "II: true", "III: false – no penalty on withdrawal due to branch transfer"],
  why="Options with III are wrong; 'I only' leaves out the true statement II.",
  facts=[fact("The components of penalty shall be clearly brought to the notice of the depositors at the time of "
              "acceptance of deposits. If not, no penalty shall be levied", DEP),
         fact("In case of splitting of the amount of term deposit at the request from the claimant(s) of deceased "
              "depositors or joint account holders, no penalty for premature withdrawal of the term deposit shall be "
              "levied if the period and aggregate amount of the deposit do not undergo any change", DEP),
         fact("No penalty for premature withdrawal shall be levied, where depositors of the branch of a bank as mentioned "
              "in paragraph 7(9) of these Directions desire premature withdrawal of deposit consequent to the transfer of "
              "business to another bank", DEP)])

Q("010", T, "Types of accounts", "Basic",
  "A term deposit matures on a Sunday and is paid on Monday. Under RBI's Interest Rate on Deposits Directions, 2025, "
  "what interest is due for the Sunday?",
  ["Interest at the originally contracted rate on the original principal for that day",
   "No interest, since the deposit had matured", "Interest at the savings deposit rate",
   "Interest at the bank's current term deposit rate for one day"],
  concept="Deposits maturing on non-business days",
  explanation="If a term deposit matures on a non-business working day, the bank pays interest at the originally "
              "contracted rate on the original principal for the intervening non-business day(s) up to payment on the "
              "next working day. For reinvestment and recurring deposits, such interest is paid on the maturity value.",
  steps=["Maturity on holiday → contracted rate for the gap day(s)"],
  why="Interest is not nil, nor at the savings rate or a new card rate.",
  facts=[fact("If a term deposit is maturing for payment on a non-business working day, a bank shall pay interest at the "
              "originally contracted rate on the original principal deposit amount for the non-business working day, "
              "intervening between the date of the maturity ... and the date of payment ... on the succeeding working "
              "day", DEP)])
Q("010", T, "Types of banks", "Basic",
  "Which institution, established in July 1988 according to RBI's chronology, is the apex body of housing finance in "
  "India?",
  ["National Housing Bank", "Housing and Urban Development Corporation", "Discount and Finance House of India",
   "Small Industries Development Bank of India"],
  concept="Specialised financial institutions",
  explanation="RBI's chronology records that the National Housing Bank was established in July 1988 as an apex body of "
              "housing finance and to promote housing development.",
  steps=["Apex housing finance body (July 1988) → NHB"],
  why="HUDCO is a Government company for housing projects; DFHI (April 1988) is a money market institution; SIDBI "
      "serves small industries.",
  facts=[fact("Jul 1988: The National Housing Bank established as an apex body of housing finance and to promote "
              "activities in housing development", CH85),
         fact("Apr 1988: The Discount and Finance House of India, set up as a money market institution, commenced "
              "operations", CH85)])
Q("010", T, "Types of banks", "Basic",
  "The State Financial Corporations Act, 1951, which came into effect on 1 August 1952, enabled State Governments to "
  "set up financial corporations mainly for meeting the credit needs of:",
  ["Medium and small scale industries", "Large public sector undertakings", "Agricultural co-operatives",
   "Importers and exporters"],
  concept="State-level development finance institutions",
  explanation="According to RBI's chronology, the SFC Act enabled States to establish financial corporations for the "
              "credit needs of medium and small scale industries; RBI's holdings in SFC capital were taken over by IDBI "
              "in 1976.",
  steps=["SFCs → medium and small industry credit"],
  why="SFCs were not meant for large PSUs, co-operatives or foreign trade finance.",
  facts=[fact("1 Aug 1952: State Financial Corporations Act, 1951 came into effect. It Enabled state governments to "
              "establish Financial corporations for meeting the credit needs of medium and small scale industries", CH50)])
Q("010", T, "Types of accounts", "Basic",
  "Under RBI's Interest Rate on Deposits Directions, 2025, floating rate domestic term deposits must be linked to:",
  ["A directly observable and transparent market-determined external benchmark", "The bank's own MCLR",
   "The bank's savings deposit rate", "The Bank Rate published by RBI"],
  concept="Floating rate deposits",
  explanation="The Directions require floating rate domestic term deposits to be linked to a directly observable and "
              "transparent market-determined external benchmark.",
  steps=["Floating rate TD → external, market-determined benchmark"],
  why="Internal rates such as MCLR or the bank's savings rate are not allowed; the Bank Rate is not specified.",
  facts=[fact("Floating rate domestic term deposits shall be linked to a directly observable and transparent market "
              "determined external benchmark", DEP)])
Q("010", T, "Cheques and instruments", "Intermediate",
  "Under continuous clearing in CTS, a drawee bank must confirm a presented cheque before its 'Item Expiry Time'. "
  "According to RBI's FAQs, can this time be extended?",
  ["Yes, by one or more hours or days in extraordinary circumstances, with RBI's approval",
   "Yes, by the drawee bank at its own discretion for any cheque above ₹5 lakh",
   "No, it can never be extended", "Yes, at the request of the payee"],
  concept="Item Expiry Time in continuous clearing",
  explanation="Item Expiry Time is the latest time for the drawee bank's confirmation, after which the cheque is "
              "deemed approved. RBI's FAQs say it may be extended for one or more hours/days in extraordinary "
              "circumstances with the approval of the Reserve Bank.",
  steps=["Extension possible only in extraordinary circumstances + RBI approval"],
  why="Drawee banks and payees cannot extend it themselves, and it is not absolutely fixed.",
  facts=[fact("Item Expiry Time of cheque/s may be extended for one or more hours / days in extraordinary circumstances "
              "with approval of the Reserve Bank of India", CHQ)])
Q("010", T, "Cheques and instruments", "Intermediate",
  "If a cheque is lost in transit or in the clearing process, what should the collecting bank do, according to RBI's "
  "FAQs on cheque clearing?",
  ["Immediately inform the presenting customer (beneficiary), so that he can ask the drawer to record stop payment",
   "Wait 30 days before informing anyone", "Debit the drawer's account using the cheque's image",
   "Ask the drawee bank to pay the cheque without the instrument"],
  concept="Lost cheques",
  explanation="RBI's FAQs say the bank should immediately bring the loss to the beneficiary's notice, so that the "
              "customer can inform the drawer to record stop payment and can take care that other cheques issued in "
              "anticipation of the credit are not dishonoured.",
  steps=["Inform beneficiary at once → drawer records stop payment"],
  why="Delay is not allowed, and the bank cannot collect on a lost instrument by itself.",
  facts=[fact("If cheques are lost in transit or in the clearing process, the bank should immediately bring the same to the "
              "notice of the presenting customer (beneficiary)'s notice so that the customer can inform the drawer to "
              "record stop payment", CHQ)])
Q("010", T, "Types of banks", "Intermediate",
  "Which apex co-operative banks were included in the Second Schedule to the RBI Act, 1934 by notifications published "
  "in the Gazette in January and April 2026?",
  ["The Assam Co-operative Apex Bank Ltd and Mizoram Co-operative Apex Bank Ltd",
   "Model Co-op. Bank Ltd and Coastal Local Area Bank Ltd",
   "The Assam Co-operative Apex Bank Ltd and Coöperatieve Rabobank U.A.",
   "Mizoram Co-operative Apex Bank Ltd and Paytm Payments Bank Ltd"],
  concept="Scheduled co-operative banks",
  explanation="The Assam Co-operative Apex Bank Ltd was included by notification of 12 January 2026 (Gazette 29 January "
              "2026), and Mizoram Co-operative Apex Bank Ltd by notification of 12 March 2026 (Gazette 10 April 2026). "
              "Model Co-op. Bank is an urban co-operative bank scheduled in 2025; Coastal Local Area Bank was included in "
              "August 2026; Rabobank and Paytm Payments Bank were excluded in 2026.",
  steps=["Jan 2026: Assam Co-operative Apex Bank", "Apr 2026: Mizoram Co-operative Apex Bank"],
  why="The other pairs include banks that are not apex co-operative banks or that were excluded, not included.",
  current=ca("2026-04-10"),
  facts=[fact("The Assam Co-operative Apex Bank Ltd has been included in the Second Schedule to the Reserve Bank of India "
              "Act, 1934 vide Notification ... dated January 12, 2026 and published in the Gazette of India ... dated "
              "January 29, 2026", ASSAM_APEX),
         fact("Mizoram Co-operative Apex Bank Ltd. has been included in the Second Schedule ... published in the Gazette "
              "of India ... dated April 10, 2026", MIZO_APEX)])
Q("010", T, "Cheques and instruments", "Intermediate",
  "In November 1983, which body did RBI set up to introduce mechanised cheque processing and national clearing of "
  "cheques?",
  ["National Clearing Cell", "National Payments Corporation of India", "Clearing Corporation of India Ltd",
   "National Grid Clearing House"],
  concept="Evolution of cheque clearing",
  explanation="RBI's chronology records the National Clearing Cell (NCC), set up in November 1983 to introduce "
              "mechanised cheque processing and national clearing; MICR technology followed in March 1987.",
  steps=["Nov 1983 → National Clearing Cell"],
  why="NPCI came in 2008; CCIL was established in 2001 for securities/forex/money market settlement; the National "
      "Grid Clearing House (Chennai) dates from 2023.",
  facts=[fact("Nov 1983: National Clearing Cell (NCC) set up by the bank to introduce mechanised cheque processing and the "
              "national clearing of cheques", CH68),
         fact("30 Apr 2001: Clearing Corporation of India established", CH00)])
Q("010", T, "Types of accounts", "Advanced",
  "An FCNR(B) depositor died on 10 March, before his deposit matured on 30 June. His heirs claimed the money on 30 "
  "August. Under RBI's Interest Rate on Deposits Directions, 2025, what interest is payable?",
  ["The contracted rate up to 30 June, and simple interest at the rate operative on 30 June for 1 July–30 August",
   "The contracted rate up to 10 March only, and nothing after the death",
   "The RFC savings rate from 10 March to 30 August",
   "The contracted rate for the whole period up to 30 August"],
  concept="Deceased FCNR(B) depositors",
  explanation="If the depositor dies before maturity but the deposit is claimed after maturity, interest is paid at the "
              "contracted rate till maturity and simple interest at the applicable rate operative on the maturity date "
              "for the period beyond maturity. (The RFC savings rate applies only if death occurs after maturity.)",
  steps=["Death before maturity, claim after maturity", "Contracted rate to 30 June; simple interest at rate on 30 June "
         "for the overdue period"],
  why="Interest does not stop at death; the RFC savings rate applies when death is after maturity; the contracted rate "
      "does not run beyond maturity.",
  facts=[fact("In case the depositor dies before the date of maturity of the deposit, but the amount of the deposit is "
              "claimed after the date of maturity, interest shall be paid at the contracted rate till the date of "
              "maturity and simple interest at the applicable rate operative on the date of maturity for the period for "
              "which the deposit remained with the bank beyond the date of maturity", DEP),
         fact("In case of death of the depositor after the date of maturity of the deposit, the interest rate operative on "
              "the date of maturity in respect of savings deposit held under RFC Account Scheme shall be paid", DEP)])
Q("010", T, "Types of accounts", "Advanced",
  "Consider the following statements about premature withdrawal of FCNR(B) deposits under RBI's Interest Rate on "
  "Deposits Directions, 2025:\n"
  "I. A bank must, on the depositor's request, permit premature withdrawal of an FCNR(B) deposit.\n"
  "II. If the deposit is withdrawn before completing the minimum period of one year, no interest is paid.\n"
  "III. A penalty must be levied when an NRI returning to India prematurely converts his FCNR(B) balance into an RFC "
  "account.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Premature withdrawal of FCNR(B) deposits",
  explanation="Banks must permit premature withdrawal of FCNR(B) deposits on request (I), and no interest is paid if the "
              "withdrawal is before the minimum stipulated period (II). No penalty is levied on premature conversion of "
              "FCNR(B) balances into RFC accounts by NRIs on return, so III is wrong (penalties do apply to conversion "
              "between FCNR(B) and NRE).",
  steps=["I: true", "II: true", "III: false – conversion into RFC on return is penalty-free"],
  why="Options with III are wrong; 'I only' leaves out the true statement II.",
  facts=[fact("A bank shall, on request from the depositor, permit premature withdrawal of deposits under the FCNR(B) "
              "Scheme. If the premature withdrawal of FCNR(B) deposits takes place before completion of the minimum "
              "stipulated period ... no interest shall be paid", DEP),
         fact("No penalties shall be levied in the case of premature conversion of balances held in FCNR(B) deposits into "
              "RFC Accounts by Non-Resident Indians on their return to India", DEP)])
Q("010", T, "Types of accounts", "Advanced",
  "Two NRIs return to India for good and immediately ask their banks to convert NRE term deposits into Resident Foreign "
  "Currency (RFC) accounts: X's deposit has run for 8 months, Y's for 18 months. Under RBI's Interest Rate on Deposits "
  "Directions, 2025, what interest do they get on the NRE deposits?",
  ["X: at most the rate on RFC savings deposits; Y: the contracted rate — and no premature withdrawal penalty for either",
   "X: the contracted rate less a penalty; Y: the contracted rate",
   "X: nothing; Y: the RFC savings rate",
   "Both: the contracted rate, plus a penalty for premature withdrawal"],
  concept="NRE deposits of returning NRIs",
  explanation="If the NRE deposit has not run for the minimum period of one year, interest on conversion into RFC is "
              "paid at a rate not exceeding the RFC savings rate (X); otherwise at the contracted rate (Y). No premature "
              "withdrawal penalty is levied on NRE deposits converted into RFC accounts.",
  steps=["X: < 1 year → ≤ RFC savings rate", "Y: ≥ 1 year → contracted rate", "Conversion to RFC: no penalty"],
  why="No penalty applies to NRE → RFC conversion; X is not denied interest; Y gets the contracted rate.",
  facts=[fact("If an NRE account holder, immediately on return to India, requests for conversion of the NRE term deposit "
              "into Resident Foreign Currency (RFC) account ... If the NRE deposit has not run for a minimum period of one "
              "year, interest shall be paid at a rate not exceeding the rate payable on savings deposits held in RFC "
              "accounts. In all other cases, interest shall be paid at the contracted rate", DEP),
         fact("No penalty shall be levied for premature withdrawal of NRE term deposits for conversion into RFC account",
              DEP)])
Q("010", T, "Types of accounts", "Advanced",
  "Consider the following statements about the DEA Fund procedures in RBI's Commercial Banks – Miscellaneous "
  "Directions, 2025:\n"
  "I. A bank may designate up to 10 officers as authorised signatories to operate its DEA Fund account jointly.\n"
  "II. A bank submits only one consolidated claim per month to the Fund, during the first 10 working days.\n"
  "III. Interest payable from the Fund on a claim accrues from the date the depositor opened the account.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="DEA Fund operations",
  explanation="Banks may designate a maximum of 10 officers as joint authorised signatories (I) and submit one "
              "consolidated claim a month during the first 10 working days (II). Interest from the Fund accrues only "
              "from the date the balance was transferred to the Fund to the date of payment, so III is wrong.",
  steps=["I: true", "II: true", "III: false – from date of transfer to the Fund"],
  why="Options with III are wrong; 'I only' leaves out the true statement II.",
  facts=[fact("A bank shall designate up to a maximum of 10 officers as authorised signatories to operate the bank's DEA "
              "Fund account jointly", MISC),
         fact("A bank shall ... submit claim from the Fund in e-Kuber system during the first 10 working days of every "
              "month. A bank shall submit only one consolidated claim per month", MISC),
         fact("The interest payable, if any, from the Fund on a claim shall accrue only from the date on which the balance "
              "in an account was transferred to the Fund to the date of payment", MISC)])
Q("010", T, "Types of banks", "Advanced",
  "Consider the following changes to the Second Schedule to the RBI Act, 1934 announced by RBI in 2026:\n"
  "I. Coastal Local Area Bank Limited was included in the Second Schedule (Gazette of 11 August 2026).\n"
  "II. Coöperatieve Rabobank U.A. ceased to be a banking company within the meaning of Section 36A(2) of the Banking "
  "Regulation Act and was excluded from the Second Schedule (Gazette of 2 July 2026).\n"
  "III. Paytm Payments Bank Limited was included in the Second Schedule (Gazette of 7 September 2026).\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Scheduled banks: inclusions and exclusions",
  explanation="Coastal Local Area Bank was included by notification of 28 July 2026, published on 11 August 2026 (I). "
              "Rabobank, a foreign bank, ceased to be a banking company under Section 36A(2) and was excluded from the "
              "Second Schedule, both notified on 24 June 2026 and published on 2 July 2026 (II). Paytm Payments Bank was "
              "excluded from, not included in, the Second Schedule by the notification published on 7 September 2026, so "
              "III is wrong.",
  steps=["I: true", "II: true", "III: false – Paytm Payments Bank was excluded"],
  why="Options with III are wrong; 'I only' leaves out the true statement II.",
  current=ca("2026-09-07"),
  facts=[fact("Coastal Local Area Bank Limited has been included in the Second Schedule to the Reserve Bank of India Act, "
              "1934 vide Notification ... dated July 28, 2026 and published in the Gazette of India ... dated August 11, "
              "2026", COASTAL_LAB),
         fact("Coöperatieve Rabobank U.A. has ceased to be a banking company within the meaning of the Banking Regulation "
              "Act, 1949 vide Notification ... dated June 24, 2026 which is published in the Gazette of India ... dated "
              "July 02, 2026", RABO_CEASE),
         fact("Coöperatieve Rabobank U.A. has been excluded from the Second Schedule to the Reserve Bank of India Act, 1934 "
              "vide Notification ... dated June 24, 2026", RABO_EXCL),
         fact("Paytm Payments Bank Limited has been excluded from the Second Schedule to the Reserve Bank of India Act, "
              "1934 vide Notification ... dated July 31, 2026 and published in the Gazette of India ... dated September "
              "07, 2026", PAYTM_EXCL)])


SWAP_MAY26 = _P + "62775"
SWAP_DEC25 = _P + "61773"
LIQ_JAN23 = _P + "62100"
MPC_RESCHED = _P + "60612"
MPC_FEB25 = _P + "59692"
MPC_APR25 = _P + "60176"
MPC_JUN25 = _P + "60604"
MPC_AUG25 = _P + "60957"
CRR99 = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=13736&Mode=0"

# ============================================================================================ Monetary Policy
T = "Monetary Policy"
Q("008", T, "MPC structure", "Basic",
  "Prof. Ram Singh, one of the three Government-appointed members of the Monetary Policy Committee, is the Director of:",
  ["Delhi School of Economics, University of Delhi", "Institute for Studies in Industrial Development, New Delhi",
   "Indira Gandhi Institute of Development Research, Mumbai", "National Institute of Public Finance and Policy"],
  concept="Members of the MPC",
  explanation="RBI's monetary policy page lists the external members notified in the Gazette of 1 October 2024: Dr. "
              "Nagesh Kumar (Director and Chief Executive, ISID, New Delhi), Shri Saugata Bhattacharya (Economist) and "
              "Prof. Ram Singh (Director, Delhi School of Economics, University of Delhi).",
  steps=["Prof. Ram Singh → Delhi School of Economics"],
  why="ISID is headed by Dr. Nagesh Kumar; IGIDR and NIPFP are not linked to Prof. Singh in RBI's list.",
  facts=[fact("Prof. Ram Singh, Director, Delhi School of Economics, University of Delhi — Member", MPF)])
Q("008", T, "Transmission", "Basic",
  "In a USD/INR buy/sell swap auction conducted by RBI (such as the USD 5 billion, three-year swap of May 2026), what "
  "does a participating bank do?",
  ["Sells US dollars to RBI now and agrees to buy the same amount back at the end of the swap, so rupee liquidity is "
   "injected for the tenor", "Buys US dollars from RBI now and sells them back later, absorbing rupee liquidity",
   "Lends rupees to RBI against government securities", "Borrows dollars from RBI to repay external loans"],
  concept="FX swaps as a liquidity tool",
  explanation="In a buy/sell swap from RBI's side, a bank sells US dollars to RBI and simultaneously agrees to buy the "
              "same amount back at the end of the swap period. RBI pays rupees in the near leg, injecting durable rupee "
              "liquidity for the swap's tenor; banks bid the premium they will pay to RBI.",
  steps=["Near leg: bank sells USD, gets ₹ → liquidity injected", "Far leg: bank buys back USD"],
  why="The second option describes a sell/buy (absorbing) swap; the others are not swaps.",
  current=ca("2026-05-26"),
  facts=[fact("The swap is in the nature of a simple buy/sell foreign exchange swap from the Reserve Bank side. A bank "
              "shall sell US dollars to the Reserve Bank and simultaneously agree to buy the same amount of US dollars at "
              "the end of the swap period", SWAP_MAY26)])
Q("008", T, "Transmission", "Intermediate",
  "Under RBI's Commercial Banks – Interest Rates on Advances Directions, 2025, which floating rate loans must be linked "
  "to an external benchmark, and what restriction applies to the choice of benchmark?",
  ["All floating rate personal or retail loans and floating rate loans to MSMEs; a bank must use one uniform external "
   "benchmark within a loan category",
   "Only floating rate home loans; a bank may use different benchmarks for different borrowers in a category",
   "All loans of all borrowers; the benchmark must be the bank's own MCLR",
   "Only loans to micro enterprises; the benchmark must be the 91-day T-bill yield"],
  concept="External benchmark lending rates",
  explanation="The Directions require all floating rate personal or retail loans (housing, auto, etc.) and floating "
              "rate loans to MSMEs to be benchmarked to an external benchmark. To ensure transparency and "
              "standardisation, a bank must adopt a uniform external benchmark within a loan category; multiple "
              "benchmarks within a category are not allowed.",
  steps=["Coverage: retail/personal + MSME floating loans", "One external benchmark per loan category"],
  why="Coverage is wider than home loans and narrower than all loans; MCLR is internal; there is no single mandated "
      "benchmark such as the 91-day T-bill.",
  facts=[fact("All floating rate personal or retail loans (housing, auto, etc.), and floating rate loans extended by banks "
              "to Micro, Small and Medium Enterprises (MSME) shall be benchmarked to an External Benchmark Rate", ADV),
         fact("a bank must adopt a uniform external benchmark within a loan category; in other words, the adoption of "
              "multiple benchmarks by the same bank is not allowed within a loan category", ADV)])
Q("008", T, "Transmission", "Intermediate",
  "On 23 December 2025 RBI announced further measures to inject durable liquidity. What were they?",
  ["OMO purchases of ₹2,00,000 crore in four tranches and a three-year USD/INR buy/sell swap of USD 10 billion",
   "OMO purchases of ₹1,00,000 crore in two tranches and a USD 5 billion swap",
   "A 100 bps cut in CRR and OMO sales of ₹50,000 crore", "A 90-day VRR of ₹25,000 crore only"],
  concept="Durable liquidity injection",
  explanation="The 23 December 2025 announcement provided OMO purchase auctions of ₹2,00,000 crore in four tranches of "
              "₹50,000 crore (29 December 2025 to 22 January 2026) and a USD 10 billion, 3-year buy/sell swap on 13 "
              "January 2026. The ₹1 lakh crore OMO and USD 5 billion swap were the earlier package of 5 December.",
  steps=["23 Dec 2025: OMO ₹2 lakh crore (4 × ₹50,000 crore) + USD 10 bn 3-yr swap"],
  why="The second option is the 5 December package; there was no CRR cut or OMO sale; the 90-day VRR came in January.",
  current=ca("2025-12-23"),
  facts=[fact("OMO purchase auctions of Government of India securities for an aggregate amount of ₹2,00,000 crore in four "
              "tranches of ₹50,000 crore each to be held on December 29, 2025, January 05, 2026, January 12, 2026, and "
              "January 22, 2026. USD/INR Buy/Sell Swap auction of USD 10 billion for a tenor of 3 years to be held on "
              "January 13, 2026", LIQ_DEC23)])
Q("008", T, "MPC structure", "Intermediate",
  "Under the RBI MPC and Monetary Policy Process Regulations, 2016, at what time are the minutes of an MPC meeting "
  "released?",
  ["At 5 pm on the 14th day from the policy day (or the next working day if it is a holiday in Mumbai)",
   "At 10 am on the 7th day after the meeting", "At noon on the day of the policy announcement",
   "At 5 pm on the last working day of the month"],
  concept="Release of MPC minutes",
  explanation="Minutes, containing the resolution, each member's vote and their written statements (Section 45ZL), are "
              "released at 5 pm on the 14th day from the policy day, or the next earliest working day if that is a "
              "holiday in Mumbai.",
  steps=["Minutes: 14th day, 5 pm (next working day if Mumbai holiday)"],
  why="The resolution (not the minutes) is released on the policy day; 7th day and month-end are not the rule.",
  facts=[fact("Minutes shall be released at 5 pm on the 14th day from the date of the policy day (or next earliest working "
              "day, if a holiday in Mumbai)", MPF)])
Q("008", T, "MPC structure", "Intermediate",
  "The MPC meeting originally scheduled for 5–7 August 2025 was rescheduled to 4–6 August 2025 'due to administrative "
  "exigencies'. Under which provision of the RBI Act was this announcement made?",
  ["Section 45ZI(4)", "Section 45ZA(1)", "Section 45ZL", "Section 45ZN"],
  concept="Rules on MPC meetings",
  explanation="RBI announced the rescheduling under Section 45ZI(4) of the RBI Act, which deals with the meetings of the "
              "MPC (including publication of the meeting schedule). Section 45ZA concerns the inflation target, 45ZL the "
              "minutes and 45ZN the report on failure to meet the target.",
  steps=["MPC meetings/schedule → Section 45ZI"],
  why="45ZA (target), 45ZL (minutes) and 45ZN (failure report) do not deal with meeting dates.",
  current=ca("2025-06-06"),
  facts=[fact("Due to administrative exigencies, the MPC meeting has been rescheduled to August 4 – 6, 2025. This "
              "announcement is made under Section 45ZI(4) of the Reserve Bank of India Act, 1934", MPC_RESCHED)])

buckets = [15.1, 11.8, 9.3, 16.9, 24.3, 10.5]
cum, n = 0.0, 0
for b_ in buckets:
    cum += b_
    n += 1
    if cum > 30:
        break
assert n == 3 and round(cum, 1) == 36.2 and max(buckets) < 30
Q("008", T, "Transmission", "Advanced",
  "A bank's funds (other than equity) for computing MCLR are spread, from the longest maturity bucket down, as 15.1%, "
  "11.8%, 9.3%, 16.9%, 24.3% and 10.5%. No single bucket exceeds 30%. Under RBI's Interest Rates on Advances "
  "Directions, 2025, to what tenor must its MCLR correspond?",
  ["The weighted average tenor of the first three maturity buckets, which together first exceed 30% (36.2%)",
   "The tenor of the largest bucket (24.3%)", "The weighted average tenor of all six buckets",
   "The tenor of the first two buckets (26.9%)"],
  concept="Tenor of MCLR",
  explanation="MCLR corresponds to the tenor of the single largest maturity bucket if it exceeds 30% of funds; otherwise "
              "to the weighted average tenor of two or more buckets that together account for more than 30%, taken "
              "cumulatively in descending order of maturity. Cumulative: 15.1, 26.9, 36.2 → the first three buckets.",
  steps=["No bucket > 30%", "Cumulate from longest: 15.1 → 26.9 → 36.2 (>30%)", "Use first three buckets"],
  why="24.3% is below 30%; all six buckets are not needed; two buckets give only 26.9%.",
  computed=True,
  facts=[fact("the weighted average tenor of two or more maturity buckets that together account for more than 30 percent, "
              "if no single maturity bucket accounts for more than 30 percent of the funds. The maturity bucket shall be "
              "arrived at by calculating the cumulative weightage based on the descending order of the maturity time "
              "buckets", ADV),
         fact("For above-mentioned maturity profile of borrowings, the MCLR shall correspond to the weighted average of "
              "tenor of the first three time buckets", ADV)])

tb, cd, cp = (5.29, 5.28), (6.33, 6.73), (6.91, 7.08)
d_tb, d_cd, d_cp = [round((a - b) * 100) for a, b in (tb, cd, cp)]
assert (d_tb, d_cd, d_cp) == (1, -40, -17)
Q("008", T, "Transmission", "Advanced",
  "The Governor's statement of 7 October 2026 said the 3-month T-bill, certificate of deposit (CD) and commercial paper "
  "(CP) rates averaged 5.29%, 6.33% and 6.91% since the August 2026 policy, against 5.28%, 6.73% and 7.08% between the "
  "June and August policies. Which statement is correct?",
  ["CD rates fell about 40 bps and CP rates about 17 bps, while the T-bill rate was almost unchanged (+1 bp)",
   "All three rates fell by about 40 bps", "CP rates fell the most, by about 40 bps",
   "The T-bill rate rose about 17 bps while CD rates were unchanged"],
  concept="Money market rates and liquidity",
  explanation="Changes: T-bill 5.29 − 5.28 = +1 bp; CD 6.33 − 6.73 = −40 bps; CP 6.91 − 7.08 = −17 bps. With large "
              "surplus liquidity after August, private money market rates (CDs, CPs) moderated significantly.",
  steps=["T-bill +1 bp", "CD −40 bps", "CP −17 bps"],
  why="Only the CD rate fell by 40 bps; CP fell 17 bps; the T-bill rate barely moved.",
  computed=True, current=ca("2026-10-07"),
  facts=[fact("The rates on 3-month treasury bill, 3-month certificates of deposit and 3-month commercial paper averaged "
              "5.29 per cent, 6.33 per cent and 6.91 per cent respectively since August policy compared to 5.28 per cent, "
              "6.73 per cent and 7.08 per cent, respectively during June and August policy", GOV_OCT26)])

Q("009", T, "Transmission", "Basic",
  "Under RBI's Interest Rates on Advances Directions, 2025, how often must a bank review and publish its Marginal Cost "
  "of Funds based Lending Rate (MCLR) of different maturities?",
  ["Every month, on a pre-announced date", "Once a quarter", "Once a year", "Only when the repo rate changes"],
  concept="MCLR review",
  explanation="Banks must review and publish MCLR of different maturities every month on a pre-announced date, with the "
              "approval of the Board or a delegated committee. (The older Base Rate is reviewed at least once a "
              "quarter.)",
  steps=["MCLR → monthly, pre-announced date"],
  why="Quarterly review applies to the Base Rate; MCLR is not annual or tied only to repo changes.",
  facts=[fact("A bank shall review and publish its MCLR of different maturities every month on a pre-announced date", ADV),
         fact("A bank shall review the Base Rate at least once in a quarter", ADV)])
Q("009", T, "Transmission", "Basic",
  "Under RBI's Interest Rates on Advances Directions, 2025, at what rests must banks generally charge interest on "
  "advances?",
  ["Monthly rests", "Quarterly rests", "Half-yearly rests", "Annual rests"],
  concept="Periodicity of charging interest",
  explanation="Interest is to be charged on all advances at monthly rests. Special rules apply to agricultural "
              "advances: annual rests are allowed for long-duration crops, and for short-term loans to small and "
              "marginal farmers total interest debited should not exceed the principal.",
  steps=["General rule: monthly rests"],
  why="Quarterly or half-yearly rests are not the general rule; annual rests apply only to long-duration crop loans.",
  facts=[fact("Interest shall be charged on all advances at monthly rests", ADV)])
Q("009", T, "Transmission", "Basic",
  "Which entities were eligible to bid in RBI's three-year USD/INR buy/sell swap auction of 26 May 2026?",
  ["Authorised Dealer Category-I banks", "All scheduled commercial banks and NBFCs",
   "Standalone primary dealers only", "Any resident individual with an EEFC account"],
  concept="FX swap auctions",
  explanation="RBI's operational guidelines made Authorised Dealer Category-I banks the eligible participants; bids were "
              "in terms of the premium (in paisa) payable to RBI, with multiple-price allotment.",
  steps=["Eligible: AD Category-I banks"],
  why="NBFCs, PDs and individuals were not eligible.",
  current=ca("2026-05-26"),
  facts=[fact("Authorized Dealers Category – I (AD Category- I) banks will be the eligible entities to participate in the "
              "auction", SWAP_MAY26)])
Q("009", T, "Transmission", "Intermediate",
  "Which internal benchmark rate, as defined in RBI's Interest Rates on Advances Directions, 2025, was used to price "
  "loans sanctioned up to 30 June 2010?",
  ["Benchmark Prime Lending Rate (BPLR)", "Base Rate", "MCLR", "External Benchmark Lending Rate"],
  concept="Evolution of loan pricing benchmarks",
  explanation="BPLR was the internal benchmark for loans sanctioned up to 30 June 2010. Loans from 1 July 2010 to 31 "
              "March 2016 used the Base Rate, loans from 1 April 2016 the MCLR, and retail/MSME floating loans from "
              "October 2019 an external benchmark. Existing BPLR loans continue till repayment or renewal.",
  steps=["Up to 30 Jun 2010 → BPLR", "Then Base Rate → MCLR → external benchmark"],
  why="Base Rate, MCLR and EBLR came later.",
  facts=[fact("'Benchmark Prime Lending Rate (BPLR)' means internal benchmark rate used to determine the interest rates on "
              "advances / loans sanctioned upto June 30, 2010", ADV)])
Q("009", T, "Transmission", "Intermediate",
  "Under RBI's Interest Rates on Advances Directions, 2025, what special rule applies to interest on short-term loans "
  "to small and marginal farmers?",
  ["Total interest debited should not exceed the principal amount",
   "Interest must be charged at monthly rests with compounding", "No interest can be charged for the first year",
   "Interest must be the same as the bank's MCLR, with no spread"],
  concept="Interest on agricultural advances",
  explanation="While advances generally attract interest at monthly rests, for short-term loans to small and marginal "
              "farmers the total interest debited should not exceed the principal; annual rests may be used for "
              "long-duration crops, and for short-duration crops interest is linked to due dates fixed around harvest "
              "and marketing.",
  steps=["Small/marginal farmers' short-term loans → interest ≤ principal"],
  why="Monthly compounding, an interest holiday or MCLR-without-spread are not the rule.",
  facts=[fact("Total interest debited in short term loan should not exceed the principal amount for advances to small and "
              "marginal farmers. A bank may charge interest on agricultural advances at annual rests for long duration "
              "crop only", ADV)])
Q("009", T, "Transmission", "Intermediate",
  "Under the liquidity management framework finalised on 30 September 2025, which instruments are used to manage "
  "durable liquidity?",
  ["Open market operations, long-term variable rate repo/reverse repo operations and forex swap auctions",
   "Only the Standing Deposit Facility and the Marginal Standing Facility",
   "Only 7-day variable rate repo/reverse repo auctions", "Changes in the Bank Rate"],
  concept="Durable vs transient liquidity tools",
  explanation="The framework keeps OMOs, long-term VRR/VRRR operations (tenor beyond a fortnight) and forex swap "
              "auctions as the instruments for durable liquidity. Transient liquidity is handled mainly by 7-day VRR/VRRR "
              "and other operations up to 14 days, with the SDF and MSF as standing facilities.",
  steps=["Durable → OMOs, long-term VRR/VRRR, FX swaps"],
  why="SDF/MSF and 7-day operations address short-term (transient) liquidity; the Bank Rate is a penal reference rate.",
  facts=[fact("Instruments under the extant liquidity management framework for managing durable liquidity viz. open market "
              "operations (OMOs), long-term variable rate repo/reverse repo operations and forex swap auctions will "
              "continue to be part of the revised liquidity management framework", LMF)])

omo = [1.0, 2.0, 1.0]
swaps = [5, 10, 10]
assert sum(omo) == 4.0 and sum(swaps) == 25
Q("009", T, "Transmission", "Advanced",
  "RBI announced liquidity measures on 5 December 2025 (OMO purchases of ₹1,00,000 crore; a USD 5 billion three-year "
  "buy/sell swap), 23 December 2025 (OMO purchases of ₹2,00,000 crore; a USD 10 billion swap) and 23 January 2026 (OMO "
  "purchases of ₹1,00,000 crore; a USD 10 billion swap; and a 90-day VRR). What were the total OMO purchases and swaps "
  "announced in these three packages?",
  ["₹4 lakh crore of OMO purchases and USD 25 billion of swaps", "₹3 lakh crore and USD 20 billion",
   "₹4 lakh crore and USD 20 billion", "₹2 lakh crore and USD 25 billion"],
  concept="Durable liquidity injection in 2025-26",
  explanation="OMO purchases: 1 + 2 + 1 = ₹4 lakh crore. Swaps: 5 + 10 + 10 = USD 25 billion. Both instruments add "
              "durable rupee liquidity, unlike short-term VRR operations.",
  steps=["OMO: 1 + 2 + 1 = ₹4 lakh crore", "Swaps: 5 + 10 + 10 = USD 25 billion"],
  why="The other options drop one of the packages.",
  computed=True, current=ca("2026-01-23"),
  facts=[fact("OMO purchase auctions of Government of India securities for an aggregate amount of ₹1,00,000 crore ... "
              "USD/INR Buy/Sell Swap auction of USD 5 billion for a tenor of three years", LIQ_DEC5),
         fact("OMO purchase auctions ... aggregate amount of ₹2,00,000 crore ... USD/INR Buy/Sell Swap auction of USD 10 "
              "billion for a tenor of 3 years", LIQ_DEC23),
         fact("90-day Variable Rate Repo (VRR) operation for an amount of ₹25,000 crore ... USD/INR Buy/Sell Swap auction "
              "of USD 10 billion for a tenor of 3 years ... OMO purchase auctions ... aggregate amount of ₹1,00,000 crore",
              LIQ_JAN23)])
Q("009", T, "Transmission", "Advanced",
  "Consider the following statements about interest reset on floating rate loans under RBI's Interest Rates on "
  "Advances Directions, 2025:\n"
  "I. Under MCLR, the periodicity of reset must be one year or lower and must form part of the loan contract.\n"
  "II. Under MCLR, the rate prevailing on the date of first disbursement applies till the next reset date, whatever "
  "happens to the benchmark in between.\n"
  "III. Under an external benchmark, the interest rate may be reset as rarely as once a year.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Reset of floating lending rates",
  explanation="MCLR reset periodicity is one year or lower, corresponds to the MCLR tenor and is in the loan contract "
              "(I); the MCLR on first disbursement applies until the next reset, irrespective of interim changes (II). "
              "External-benchmark loans must be reset at least once in three months, so III is wrong.",
  steps=["I: true", "II: true", "III: false – EBLR reset at least quarterly"],
  why="Options with III are wrong; 'I only' leaves out the true statement II.",
  facts=[fact("The MCLR prevailing on the date of first disbursement, whether partial or full, shall be applicable till the "
              "next reset date, irrespective of the changes in the benchmark during the interim ... The periodicity of "
              "reset shall be one year or lower. The exact periodicity of reset shall form part of the terms of the loan "
              "contract", ADV),
         fact("The interest rate under external benchmark shall be reset at least once in three months", ADV)])

Q("010", T, "MPC structure", "Basic",
  "Dr. Nagesh Kumar, a Government-appointed member of the Monetary Policy Committee, heads which institution?",
  ["Institute for Studies in Industrial Development (ISID), New Delhi", "Delhi School of Economics",
   "National Council of Applied Economic Research", "Indian Statistical Institute, Kolkata"],
  concept="Members of the MPC",
  explanation="RBI lists Dr. Nagesh Kumar as Director and Chief Executive, Institute for Studies in Industrial "
              "Development, New Delhi. Prof. Ram Singh heads the Delhi School of Economics.",
  steps=["Dr. Nagesh Kumar → ISID, New Delhi"],
  why="DSE is Prof. Ram Singh's institution; NCAER and ISI are not named.",
  facts=[fact("Dr. Nagesh Kumar, Director and Chief Executive, Institute for Studies in Industrial Development, New Delhi "
              "— Member", MPF)])
Q("010", T, "Transmission", "Intermediate",
  "Under RBI's Interest Rates on Advances Directions, 2025, what floor applies to interest rates on fixed rate loans of "
  "tenor below three years?",
  ["They cannot be lower than the benchmark rate for a similar tenor",
   "They must equal the policy repo rate plus 2 per cent", "There is no floor; banks may price them freely",
   "They cannot be lower than the Bank Rate"],
  concept="Pricing of fixed rate loans",
  explanation="Banks may offer fixed or floating rates, but interest on fixed rate loans of tenor below three years "
              "must not be less than the benchmark rate for similar tenor; and there can be no lending below the "
              "benchmark for loans linked to it.",
  steps=["Fixed rate, tenor < 3 years → ≥ benchmark for similar tenor"],
  why="No repo-plus-2% rule exists; there is a floor; the Bank Rate is not the reference.",
  facts=[fact("Interest rates on fixed rate loans of tenor below three years shall not be less than the benchmark rate for "
              "similar tenor", ADV)])
Q("010", T, "Transmission", "Intermediate",
  "Under the MCLR system in RBI's Interest Rates on Advances Directions, 2025, the spread over MCLR consists of business "
  "strategy and credit risk premium. What restriction applies to these components?",
  ["They can be positive or zero, but cannot be negative",
   "They must each be at least 1 percentage point", "They can be negative to win large borrowers",
   "They must be identical for all borrowers"],
  concept="Spread over MCLR",
  explanation="The spread components — business strategy and credit risk premium — must have either a positive value or "
              "be zero; they cannot be negative, so loans cannot be priced below MCLR through a negative spread.",
  steps=["Spread components ≥ 0"],
  why="There is no 1-point minimum; negative spreads are barred; spreads vary across borrowers by risk.",
  facts=[fact("The components of the spread i.e. business strategy and Credit risk premium shall have either a positive "
              "value or be zero. In other words, the spread components cannot be negative", ADV)])
Q("010", T, "Transmission", "Intermediate",
  "Under the liquidity management framework of 30 September 2025, how much advance notice does RBI ordinarily give "
  "market participants before conducting a repo/reverse repo liquidity operation?",
  ["At least one day, though it may announce an operation on the same day when circumstances warrant",
   "At least one week", "No notice; all operations are announced at the start of the auction window",
   "At least one fortnight, matching the reserve maintenance period"],
  concept="Predictability of liquidity operations",
  explanation="To reduce uncertainty about the tenor, quantum and timing of operations, RBI gives participants at least "
              "one day's advance notice, while retaining the option of same-day operations when warranted.",
  steps=["Ordinarily ≥ 1 day notice; same-day possible when warranted"],
  why="One week or a fortnight is not the rule; operations are not announced only at the window.",
  facts=[fact("the Reserve Bank will provide sufficient advance notice to market participants, at least by one day, while "
              "conducting any such liquidity operation. However, when circumstances warrant, the Reserve Bank would "
              "conduct operations by announcing on the same day", LMF)])
Q("010", T, "Policy stance", "Intermediate",
  "At its 57th meeting (29 September–1 October 2025), the MPC kept the repo rate at 5.50% even though inflation had "
  "turned 'even more benign'. What reason did it give?",
  ["It was prudent to let the front-loaded monetary policy actions and recent fiscal measures play out and wait for "
   "clarity on trade uncertainties",
   "Inflation was above the upper tolerance limit", "The Government had asked RBI not to cut rates",
   "Liquidity was in deficit, so a cut would not be transmitted"],
  concept="Rationale for a pause",
  explanation="The MPC noted that the impact of front-loaded rate cuts and recent fiscal measures (including GST "
              "rationalisation) was still playing out and trade uncertainties were unfolding, so it considered it prudent "
              "to wait before charting the next course; it continued with the neutral stance.",
  steps=["Space existed, but waited for past actions to play out"],
  why="Inflation was low (2.1% in August 2025); the Government does not direct the MPC's vote; liquidity was not cited.",
  facts=[fact("the MPC noted that the impact of the front-loaded monetary policy actions and the recent fiscal measures is "
              "still playing out. The trade related uncertainties are also unfolding. The MPC, therefore, considered it "
              "prudent to wait for the impact of policy actions to play out and greater clarity to emerge", MPC_OCT25)])
Q("010", T, "Transmission", "Intermediate",
  "Under the liquidity management framework of 30 September 2025, which participants were given access to the SDF, "
  "overnight reverse repo operations and all repo operations irrespective of tenor?",
  ["Standalone Primary Dealers", "Non-Banking Financial Companies", "Mutual funds", "Payments system operators"],
  concept="Access to RBI's liquidity facilities",
  explanation="The revised framework allows Standalone Primary Dealers (SPDs) access to the SDF, overnight reverse repo "
              "operations and all repo operations, irrespective of tenor. (They had been allowed into all repo "
              "operations from March 2025.)",
  steps=["SPDs → SDF + overnight reverse repo + all repos"],
  why="NBFCs, mutual funds and payment operators are not LAF participants.",
  facts=[fact("Standalone Primary Dealers (SPDs) will have access to SDF, overnight reverse repo operations, and all repo "
              "operations, irrespective of their tenor", LMF)])
Q("010", T, "Policy stance", "Advanced",
  "Consider the following statements about MPC decisions in 2025:\n"
  "I. At its April 2025 meeting the MPC changed the stance from neutral to accommodative.\n"
  "II. At its August 2025 meeting the MPC unanimously kept the repo rate at 5.50% and all members decided to continue "
  "with the neutral stance.\n"
  "III. At its meeting ending 1 October 2025 the MPC changed the stance to accommodative.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Stance of monetary policy in 2025",
  explanation="April 2025: along with a 25 bps cut, the MPC changed the stance from neutral to accommodative (I). August 2025: unanimous pause at "
              "5.50% with all members for neutral (II). October 2025: the MPC continued with the neutral stance, so III "
              "is wrong.",
  steps=["I: true (April 2025)", "II: true", "III: false – neutral continued"],
  why="Options with III are wrong; 'I only' leaves out the true statement II.",
  facts=[fact("Moreover, it also decided to change the stance from neutral to accommodative", MPC_APR25),
         fact("the MPC unanimously voted to keep the repo rate unchanged ... all members decided to continue with the "
              "neutral stance", MPC_AUG25),
         fact("The MPC also decided to continue with the neutral stance", MPC_OCT25)])
Q("010", T, "MPC structure", "Advanced",
  "Compare the members who attended the MPC meeting of February 2025 (Malhotra, Nagesh Kumar, Saugata Bhattacharya, Ram "
  "Singh, Rajiv Ranjan, M. Rajeshwar Rao) with those of February 2026. Which statement is correct?",
  ["The three Government-appointed members were the same, while Dr. Poonam Gupta and Shri Indranil Bhattacharyya had "
   "replaced Dr. Rajiv Ranjan and Shri M. Rajeshwar Rao",
   "All six members were the same", "Two of the three Government-appointed members had changed",
   "Dr. Poonam Gupta had replaced Prof. Ram Singh as a Government-appointed member"],
  concept="Composition of the MPC",
  explanation="Both meetings had Dr. Nagesh Kumar, Shri Saugata Bhattacharya and Prof. Ram Singh as the external members "
              "(appointed for four years from October 2024). The RBI side changed: in February 2026 the members were "
              "Governor Malhotra, Deputy Governor Dr. Poonam Gupta and Executive Director Shri Indranil Bhattacharyya "
              "(nominated by the Central Board), in place of Shri Rajeshwar Rao and Dr. Rajiv Ranjan.",
  steps=["External members unchanged", "RBI members: Gupta and Bhattacharyya in place of Rao and Ranjan"],
  why="The RBI members changed; the external members did not; Dr. Gupta is an RBI (Deputy Governor) member.",
  current=ca("2026-02-06"),
  facts=[fact("The MPC members Dr. Nagesh Kumar, Shri Saugata Bhattacharya, Prof. Ram Singh, Dr. Rajiv Ranjan, and Shri M. "
              "Rajeshwar Rao attended the meeting (February 5 to 7, 2025)", MPC_FEB25),
         fact("attended by all the members – Dr. Nagesh Kumar ...; Shri Saugata Bhattacharya ...; Professor Ram Singh ...; "
              "Dr. Poonam Gupta, Deputy Governor in charge of monetary policy and Shri Indranil Bhattacharyya, Executive "
              "Director (the officer of the Reserve Bank nominated by the Central Board under Section 45ZB(2)(c))",
              MIN_FEB26)])
Q("010", T, "Transmission", "Advanced",
  "Consider the following statements about loans exempted from the benchmark-linked pricing rules (Base Rate, MCLR, "
  "external benchmark) in RBI's Interest Rates on Advances Directions, 2025:\n"
  "I. Advances to a bank's depositors against their own deposits are exempt.\n"
  "II. Advances to the bank's own employees, including retired employees, are exempt.\n"
  "III. Loans under Government schemes that prescribe the interest rate must still be priced at or above the bank's "
  "MCLR.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Exemptions from benchmark pricing",
  explanation="The Directions exempt, among others, loans under Government schemes where the bank must charge the "
              "scheme's rate, WCTL/FITL under restructuring, refinance-scheme loans (to the extent refinanced), advances "
              "to depositors against their own deposits (I), advances to employees including retired employees (II), and "
              "advances to the CEO/whole-time directors. Scheme loans are exempt, so III is wrong.",
  steps=["I: exempt – true", "II: exempt – true", "III: scheme-rate loans are exempt – false"],
  why="Options with III are wrong; 'I only' leaves out the true statement II.",
  facts=[fact("The following types of loans shall be exempted from the provisions contained under paragraphs 10 to 41 of "
              "these Directions: (1) Loans covered by schemes specially formulated by Government of India wherein a bank "
              "has to charge interest rates as per the scheme ... (i) Advances to banks' depositors against their own "
              "deposits. (ii) Advances to banks' own employees including retired employees", ADV)])
Q("010", T, "Transmission", "Advanced",
  "Consider the following statements about RBI's USD/INR buy/sell swap auction of December 2025 (USD 5 billion, 36 "
  "months):\n"
  "I. Bids were quoted as the premium, in paisa, that banks were willing to pay RBI for the tenor of the swap.\n"
  "II. It was a multiple-price auction: successful bids were accepted at their own quoted premium.\n"
  "III. Bids were arranged in ascending order of premium, and those below the cut-off were accepted.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I and III only", "II only", "I, II and III"],
  concept="Mechanics of swap auctions",
  explanation="Participants bid the premium (paisa, two decimals) they would pay RBI (I); the auction was multiple-price, "
              "with successful bids accepted at their quoted premium (II). Bids were arranged in descending order, and "
              "those at or above the cut-off premium succeeded while lower bids were rejected, so III is wrong.",
  steps=["I: true", "II: true", "III: false – descending order; bids at/above cut-off succeed"],
  why="Options with III are wrong; 'II only' leaves out the true statement I.",
  current=ca("2025-12-16"),
  facts=[fact("The market participants would be required to place their bids in terms of the premium that they are willing "
              "to pay to the Reserve Bank for the tenor of the swap, expressed in paisa terms up to two decimal places ... "
              "The auction would be a multiple-price based auction, i.e., successful bids will get accepted at their "
              "respective quoted premium", SWAP_DEC25),
         fact("all the bids would be arranged in descending order of the swap premium quoted ... Successful bidders would "
              "be those who have placed their bids at or above the cut-off premium. All bids lower than the cut-off "
              "premium would be rejected", SWAP_DEC25)])
Q("010", T, "Transmission", "Advanced",
  "Consider the following statements about RBI's liquidity framework as it stands in November 2026:\n"
  "I. The symmetric corridor finalised in September 2025 is retained, with the SDF and MSF 25 bps on either side of the "
  "repo rate.\n"
  "II. The weighted average call rate remains the operating target, while RBI also tracks rates in other overnight "
  "money market segments.\n"
  "III. The 14-day variable rate repo/reverse repo remains the main operation for managing transient liquidity.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Current liquidity management framework",
  explanation="The September 2025 framework retained the symmetric corridor (I) and the WACR as operating target, with "
              "RBI also tracking other overnight segments (II). The 14-day VRR/VRRR was discontinued as the main "
              "operation; transient liquidity is managed mainly through 7-day operations, so III is wrong.",
  steps=["I: true", "II: true", "III: false – 7-day operations are now the main tool"],
  why="Options with III are wrong; 'I only' leaves out the true statement II.",
  current=ca("2025-09-30"),
  facts=[fact("The existing symmetric corridor system is retained, with policy repo rate at the middle of the corridor and "
              "standing deposit facility (SDF) and marginal standing facility (MSF), which are 25 bps on either side of "
              "the policy repo rate ... The overnight weighted average call rate (WACR) will continue to be the operating "
              "target of the monetary policy. The Reserve Bank will, however, continue to keep track of rates in other "
              "overnight money market segments", LMF),
         fact("The 14-day variable rate repo (VRR)/ variable rate reverse repo (VRRR) operation will be discontinued as "
              "the main operation for managing short-term/transient liquidity", LMF)])
Q("009", T, "Transmission", "Intermediate",
  "Under RBI's Interest Rates on Advances Directions, 2025, a borrower with an MCLR-linked floating rate term loan who "
  "is eligible to prepay it without prepayment charges wants to switch to the external benchmark. On what terms?",
  ["Without charges or fees except reasonable administrative/legal costs, at the rate the bank charges a new loan of "
   "the same category, type, tenor and amount",
   "Only after paying a 2% foreclosure charge", "Only at the bank's discretion, with the switch treated as foreclosure",
   "Only at the original MCLR plus 1 percentage point"],
  concept="Switching existing loans to the external benchmark",
  explanation="Existing MCLR/Base Rate/BPLR loans continue till repayment or renewal, but floating rate term loans of "
              "borrowers eligible to prepay without charges may switch to the external benchmark without charges or "
              "fees except reasonable administrative/legal costs. The rate after switchover must equal that for a new "
              "loan of the same category, type, tenor and amount, and the switch is not treated as foreclosure.",
  steps=["Eligible borrower → free switch (bar admin/legal costs)", "Rate = new-loan rate for same loan profile"],
  why="No foreclosure charge applies, the switch is not treated as foreclosure, and there is no MCLR-plus formula.",
  facts=[fact("floating rate term loans sanctioned to borrowers who, in terms of extant guidelines, are eligible to prepay "
              "a floating rate loan without pre-payment charges, shall be eligible for switchover to External Benchmark "
              "without any charges / fees, except reasonable administrative / legal costs. The final rate charged to this "
              "category of borrowers, post switchover to external benchmark, shall be same as the rate charged for a new "
              "loan of the same category, type, tenor and amount", ADV)])


_RES = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid="
SPD_SLF = _RES + "60105"
SPD_VRR = _RES + "60068"
VRR_OCT19 = _RES + "63823"
VRR_OCT21 = _RES + "63835"
VRR_YE = _RES + "62435"
VRR_YE1, VRR_YE2, VRR_YE3 = _RES + "62445", _RES + "62461", _RES + "62465"
VRRR_AUG17 = _RES + "63383"
VRRR_SEP7N, VRRR_SEP7 = _RES + "63528", _RES + "63530"
VRRR_SEP11N, VRRR_SEP11 = _RES + "63570", _RES + "63574"
VRRR_OCT1N, VRRR_OCT1 = _RES + "63703", _RES + "63706"
VRRR_OCT9 = _RES + "63769"
DISC_MPF = _RES + "61067"

# ============================================================================================ Repo Rate
T = "Repo Rate"
S = "Repo and policy corridor"
Q("008", T, S, "Basic",
  "At its 53rd meeting (5–7 February 2025), the first cut of the 2025 easing cycle, the MPC reduced the policy repo rate "
  "by 25 basis points to:",
  ["6.25%", "6.00%", "6.50%", "5.50%"],
  concept="Repo rate decisions of 2025",
  explanation="On 7 February 2025 the MPC unanimously cut the repo rate by 25 bps to 6.25%. Further cuts followed in "
              "April 2025 (to 6.00%) and June 2025 (50 bps, to 5.50%).",
  steps=["Feb 2025: 6.50% − 0.25 = 6.25%"],
  why="6.00% came in April 2025, 5.50% in June 2025; 6.50% was the rate before the cut.",
  current=ca("2025-02-07"),
  facts=[fact("reduce the policy repo rate under the liquidity adjustment facility (LAF) by 25 basis points to 6.25 per "
              "cent with immediate effect", MPC_FEB25)])
Q("008", T, S, "Basic",
  "What did the MPC decide on the policy repo rate at its 59th meeting, held on 4–6 February 2026?",
  ["Kept it unchanged at 5.25% by a unanimous vote", "Cut it by 25 bps to 5.00%",
   "Raised it by 25 bps to 5.50%", "Kept it at 5.25% by a 4–2 vote"],
  concept="MPC decisions in 2026",
  explanation="In February 2026 the MPC voted unanimously to keep the repo rate at 5.25% (SDF 5.00%, MSF and Bank Rate "
              "5.50%) and to continue with the neutral stance.",
  steps=["Feb 2026 → unanimous pause at 5.25%"],
  why="There was no cut or hike in February 2026, and the vote was unanimous.",
  current=ca("2026-02-06"),
  facts=[fact("the MPC voted unanimously to keep the policy repo rate under the liquidity adjustment facility (LAF) "
              "unchanged at 5.25 per cent", MIN_FEB26)])
Q("008", T, S, "Intermediate",
  "When the MPC cut the repo rate by 50 bps to 5.50% in June 2025, how did the members vote on the size of the cut?",
  ["Five members voted for 50 bps; Shri Saugata Bhattacharya voted for a 25 bps cut",
   "All six voted for 50 bps", "Four voted for 50 bps and two for no change",
   "Five voted for 50 bps; Prof. Ram Singh voted for 75 bps"],
  concept="Voting in the MPC",
  explanation="The June 2025 resolution records that Dr. Nagesh Kumar, Prof. Ram Singh, Dr. Rajiv Ranjan, Dr. Poonam "
              "Gupta and Governor Sanjay Malhotra voted for a 50 bps cut, while Shri Saugata Bhattacharya voted for a "
              "25 bps cut.",
  steps=["5 votes: 50 bps", "1 vote (Saugata Bhattacharya): 25 bps"],
  why="The decision was not unanimous, nobody voted for no change, and nobody voted for 75 bps.",
  current=ca("2025-06-06"),
  facts=[fact("Dr. Nagesh Kumar, Prof. Ram Singh, Dr. Rajiv Ranjan, Dr. Poonam Gupta and Shri Sanjay Malhotra, voted to "
              "decrease the policy repo rate by 50 bps. Shri Saugata Bhattacharya voted for a 25 bps cut in repo rate",
              MPC_JUN25)])

cuts_2025 = {"Feb": 25, "Apr": 25, "Jun": 50, "Aug": 0, "Oct": 0, "Dec": 25}
assert sum(1 for v in cuts_2025.values() if v) == 4 and max(cuts_2025.values()) == 50
Q("008", T, S, "Advanced",
  "The MPC met six times in calendar year 2025 (February, April, June, August, October and December). Based on its "
  "resolutions, in how many of these meetings was the repo rate cut, and what was the largest single cut?",
  ["Four meetings; 50 bps (June)", "Three meetings; 50 bps (June)", "Four meetings; 25 bps each",
   "Five meetings; 50 bps (December)"],
  concept="Tracking the policy rate path",
  explanation="Feb 2025: −25 bps (6.25%); Apr: −25 bps (6.00%); Jun: −50 bps (5.50%); Aug and Oct: unchanged at 5.50%; "
              "Dec: −25 bps (5.25%). So four cuts, the largest being 50 bps in June.",
  steps=["Cuts: Feb, Apr, Jun, Dec = 4", "Largest: June, 50 bps"],
  why="August and October were pauses; the December cut was 25 bps.",
  computed=True, current=ca("2025-12-05"),
  facts=[fact("reduce the policy repo rate ... by 25 basis points to 6.25 per cent", MPC_FEB25),
         fact("the MPC unanimously voted to reduce the policy repo rate by 25 basis points to 6.00 per cent", MPC_APR25),
         fact("the MPC voted to reduce the policy repo rate by 50 basis points (bps) to 5.50 per cent", MPC_JUN25),
         fact("the MPC voted to maintain the policy repo rate at 5.50 per cent", MPC_AUG25),
         fact("the MPC voted unanimously to keep the policy repo rate ... unchanged at 5.50 per cent", MPC_OCT25),
         fact("the MPC voted unanimously to reduce the policy repo rate ... to 5.25 per cent", MPC_DEC25)])

Q("009", T, S, "Basic",
  "At its 57th meeting (29 September–1 October 2025), what did the MPC decide on the policy repo rate?",
  ["Kept it unchanged at 5.50% by a unanimous vote", "Cut it by 25 bps to 5.25%",
   "Cut it by 50 bps to 5.00%", "Raised it by 25 bps to 5.75%"],
  concept="MPC decisions of 2025",
  explanation="In October 2025 the MPC unanimously kept the repo rate at 5.50% (SDF 5.25%, MSF and Bank Rate 5.75%) and "
              "continued with the neutral stance; the next cut, to 5.25%, came in December 2025.",
  steps=["Oct 2025 → pause at 5.50%"],
  why="The cut to 5.25% was in December 2025; there was no 50 bps cut or hike then.",
  current=ca("2025-10-01"),
  facts=[fact("the MPC voted unanimously to keep the policy repo rate under the liquidity adjustment facility (LAF) "
              "unchanged at 5.50 per cent", MPC_OCT25)])
Q("009", T, S, "Intermediate",
  "From 26 March 2025, what change did RBI make to Standalone Primary Dealers' (SPDs') participation in its repo "
  "operations?",
  ["SPDs were allowed to participate in all repo operations, irrespective of tenor",
   "SPDs were barred from all repo operations",
   "SPDs could participate only in the Marginal Standing Facility",
   "SPDs could participate only in overnight repo auctions"],
  concept="Participants in repo operations",
  explanation="Since February 2020 SPDs could take part in overnight operations (except the MSF) and in long-term or "
              "daily VRRs case by case. In March 2025 RBI allowed them to participate in all repo operations, "
              "irrespective of tenor.",
  steps=["Before: overnight ops + case-by-case VRRs", "From 26 Mar 2025: all repo operations"],
  why="SPDs were not barred, and they are excluded from the MSF; overnight-only was the earlier position.",
  current=ca("2025-03-26"),
  facts=[fact("On a review, it has now been decided to allow SPDs to participate in all Repo operations, irrespective of "
              "the tenor, conducted by the Reserve Bank", SPD_VRR)])
Q("009", T, S, "Intermediate",
  "Twelve days after the repo rate was raised to 5.50%, RBI conducted a Variable Rate Repo auction on 19 October 2026. "
  "What were its notified amount and tenor?",
  ["₹1,00,000 crore for 7 days, reversing on 26 October 2026", "₹50,000 crore overnight",
   "₹25,000 crore for 90 days", "₹1,00,000 crore for 14 days"],
  concept="Variable rate repo operations",
  explanation="RBI announced a 7-day VRR auction on 19 October 2026 for a notified amount of ₹1,00,000 crore, with "
              "reversal on 26 October 2026 — consistent with 7-day operations being the main tool for transient "
              "liquidity.",
  steps=["19 Oct 2026 VRR: ₹1 lakh crore, 7 days → 26 Oct"],
  why="The overnight ₹50,000 crore VRR was on 21 October; the 90-day VRR was in January 2026.",
  current=ca("2026-10-19"),
  facts=[fact("it has been decided to conduct a Variable Rate Repo (VRR) auction on Monday, October 19, 2026, as under: "
              "1 | 1,00,000 | 7 | 09:30 AM to 10:00 AM | October 26, 2026", VRR_OCT19)])
Q("009", T, S, "Intermediate",
  "When the MPC cut the repo rate to 5.25% in December 2025, what had the latest GDP data shown?",
  ["Real GDP growth of 8.2% in Q2:2025-26, a six-quarter high", "A contraction in Q2:2025-26",
   "Real GDP growth of 5.4% in Q2:2025-26, a multi-year low", "Real GDP growth of 7.8% in Q2:2025-26"],
  concept="Growth backdrop to a rate cut",
  explanation="The December 2025 resolution noted a six-quarter high growth of 8.2% in Q2:2025-26 (GVA 8.1%). The MPC "
              "still cut the repo rate because inflation was exceptionally benign, giving policy space to support "
              "growth momentum.",
  steps=["Q2 2025-26 GDP 8.2% (six-quarter high)", "Cut justified by benign inflation"],
  why="Growth was strong, not contracting or at a low; 7.8% was the Q1:2025-26 figure.",
  current=ca("2025-12-05"),
  facts=[fact("real gross domestic product (GDP) registered a six-quarter high growth of 8.2 per cent in Q2:2025-26", MPC_DEC25)])

ye = [65322, 50001, 34581]
assert sum(ye) == 149904 and ye[0] < 75000
Q("009", T, S, "Advanced",
  "For year-end liquidity in March 2026 (repo rate 5.25%), RBI held a 6-day VRR on 27 March (notified ₹75,000 crore; "
  "bids and allotment ₹65,322 crore) and two 3-day VRRs on 30 March (₹50,001 crore and ₹34,581 crore allotted). All "
  "reversed on 2 April 2026. Which statement is correct?",
  ["About ₹1.50 lakh crore (₹1,49,904 crore) was outstanding under these VRRs until 2 April, and the 27 March auction "
   "was undersubscribed",
   "About ₹1.75 lakh crore was outstanding, and all three auctions were oversubscribed",
   "About ₹1.15 lakh crore was outstanding, since the 27 March VRR had matured by 30 March",
   "About ₹1.25 lakh crore was outstanding, equal to the notified amounts"],
  concept="Year-end repo operations",
  explanation="All three VRRs reversed on 2 April, so on 30 March–1 April the outstanding amount was 65,322 + 50,001 + "
              "34,581 = ₹1,49,904 crore. The 27 March auction drew bids of only ₹65,322 crore against ₹75,000 crore "
              "notified.",
  steps=["65,322 + 50,001 + 34,581 = 1,49,904", "27 Mar: 65,322 < 75,000 → undersubscribed"],
  why="The 6-day VRR reversed on 2 April, not before 30 March; allotments did not equal or exceed all notified amounts.",
  computed=True, current=ca("2026-03-30"),
  facts=[fact("March 27, 2026 (Friday) | 75,000 | 6 | ... | April 02, 2026 (Thursday); March 30, 2026 (Monday) | 50,000 | 3 "
              "| ... | April 02, 2026 (Thursday)", VRR_YE),
         fact("6-day VRR: Notified Amount 75,000; Total amount of bids received 65,322; Amount allotted 65,322", VRR_YE1),
         fact("3-day VRR (March 30, 2026): Amount allotted 50,001", VRR_YE2),
         fact("Second 3-day VRR (March 30, 2026): Amount allotted 34,581", VRR_YE3)])

Q("010", T, S, "Basic",
  "At its 54th meeting (7–9 April 2025), the MPC cut the policy repo rate by 25 bps. To what level?",
  ["6.00%", "6.25%", "5.75%", "5.50%"],
  concept="Repo rate decisions of 2025",
  explanation="In April 2025 the MPC unanimously cut the repo rate by 25 bps to 6.00%, with the SDF at 5.75% and the MSF "
              "and Bank Rate at 6.25%.",
  steps=["6.25% − 0.25 = 6.00%"],
  why="6.25% was the rate after February; 5.75% is the SDF; 5.50% came in June.",
  current=ca("2025-04-09"),
  facts=[fact("the MPC unanimously voted to reduce the policy repo rate by 25 basis points to 6.00 per cent with immediate "
              "effect. Consequently, the standing deposit facility (SDF) rate ... 5.75 per cent", MPC_APR25)])
Q("010", T, S, "Intermediate",
  "Why did the MPC opt for a larger 50 bps repo cut in June 2025, according to its resolution?",
  ["The changed growth-inflation dynamics called for frontloading rate cuts to stimulate private consumption and "
   "investment", "Inflation had risen above the 6% upper tolerance limit",
   "The Government had cut the fiscal deficit target", "The US Federal Reserve had cut rates by 50 bps"],
  concept="Frontloading of policy easing",
  explanation="The MPC said it was imperative to stimulate domestic private consumption and investment, and the changed "
              "growth-inflation dynamics called for not only continuing easing but also frontloading the rate cuts to "
              "support growth.",
  steps=["Benign inflation + need to support growth → frontload (50 bps)"],
  why="Inflation was low, not above 6%; fiscal and Fed actions were not the reason given.",
  current=ca("2025-06-06"),
  facts=[fact("This changed growth-inflation dynamics calls for not only continuing with the policy easing but also "
              "frontloading the rate cuts to support growth. Accordingly, the MPC voted to reduce the policy repo rate by "
              "50 bps to 5.50 per cent", MPC_JUN25)])
Q("010", T, S, "Intermediate",
  "In RBI's overnight Variable Rate Repo auction of 21 October 2026 (notified ₹50,000 crore; repo rate 5.50%), bids "
  "of ₹93,241 crore were received and ₹50,007 crore was allotted at a cut-off rate of 5.52%. What does this indicate?",
  ["Banks' demand for funds exceeded the amount RBI offered, so the cut-off settled slightly above the repo rate",
   "Banks had surplus funds, so the auction was undersubscribed",
   "RBI lent at the SDF rate because demand was weak",
   "The auction failed and RBI lent nothing"],
  concept="Reading repo auction results",
  explanation="Bids (₹93,241 crore) far exceeded the notified ₹50,000 crore, showing demand for liquidity; with "
              "competitive bidding the cut-off settled at 5.52%, 2 bps above the 5.50% repo rate, below the 5.75% MSF.",
  steps=["Bids 93,241 > notified 50,000 → excess demand", "Cut-off 5.52% > repo 5.50%"],
  why="It was oversubscribed, not under; the rate was above repo, not the SDF; ₹50,007 crore was allotted.",
  current=ca("2026-10-21"),
  facts=[fact("Tenor 1-day; Notified Amount 50,000; Total amount of bids received 93,241; Amount allotted 50,007; Cut off "
              "Rate (%) 5.52", VRR_OCT21)])
Q("010", T, S, "Advanced",
  "Consider the following statements about the MPC's decision of 7 February 2025:\n"
  "I. The 25 bps cut in the repo rate was decided unanimously.\n"
  "II. The MPC continued with the neutral stance.\n"
  "III. As a result, the SDF rate became 6.25%.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Repo, SDF and MSF move together",
  explanation="The MPC unanimously cut the repo rate by 25 bps (I) and continued with the neutral stance (II). With the "
              "repo at 6.25%, the SDF (25 bps below) became 6.00% and the MSF/Bank Rate 6.50%, so III is wrong.",
  steps=["I: true", "II: true", "III: SDF = 6.25 − 0.25 = 6.00% → false"],
  why="Options with III are wrong; 'I only' leaves out the true statement II.",
  current=ca("2025-02-07"),
  facts=[fact("the MPC unanimously decided to: reduce the policy repo rate ... by 25 basis points to 6.25 per cent ... "
              "consequently, the standing deposit facility (SDF) rate shall stand adjusted to 6.00 per cent and the "
              "marginal standing facility (MSF) rate and the Bank Rate to 6.50 per cent; continue with the neutral "
              "monetary policy stance", MPC_FEB25)])

# ============================================================================================ Reverse Repo Rate
T = "Reverse Repo Rate"
S = "Reverse repo and SDF"
Q("008", T, S, "Basic",
  "RBI's 'Current Rates' panel in November 2026 shows the policy repo rate at 5.50% and the SDF at 5.25%. At what level "
  "does it show the fixed reverse repo rate?",
  ["3.35%", "5.25%", "5.00%", "4.00%"],
  concept="Fixed reverse repo after the SDF",
  explanation="The fixed reverse repo rate has stayed at 3.35%; since April 2022 the SDF (now 5.25%) is the floor of the "
              "LAF corridor, and fixed rate reverse repo operations are at RBI's discretion.",
  steps=["Fixed reverse repo = 3.35% (no longer the corridor floor)"],
  why="5.25% is the SDF rate; 5.00% was the SDF before October 2026; 4.00% is not shown.",
  current=ca("2026-10-07"),
  facts=[fact("Policy Repo Rate : 5.50%; Standing Deposit Facility Rate : 5.25%; Fixed Reverse Repo Rate : 3.35%", HOME)])
Q("008", T, S, "Intermediate",
  "RBI's 30-day VRRR of 7 September 2026 and 26-day VRRR of 11 September 2026 were both timed to reverse on the same "
  "date. Which date?",
  ["7 October 2026, the day of the MPC's policy decision", "15 September 2026", "30 September 2026",
   "16 October 2026"],
  concept="Term reverse repo operations",
  explanation="RBI notified a 30-day VRRR (₹7,00,000 crore) for 7 September and a 26-day VRRR (₹5,00,000 crore) for 11 "
              "September 2026; both had 7 October 2026 as the date of reversal — the day the MPC announced its "
              "decision.",
  steps=["7 Sep + 30 days = 7 Oct", "11 Sep + 26 days = 7 Oct"],
  why="15 September was the reversal of the 15-day VRRR of 31 August; the other dates are not reversal dates.",
  current=ca("2026-09-11"),
  facts=[fact("Variable Rate Reverse Repo (VRRR) auction on Monday, September 07, 2026: 7,00,000 | 30 | ... | October 07, "
              "2026 (Wednesday)", VRRR_SEP7N),
         fact("VRRR auction on Friday, September 11, 2026: 5,00,000 | 26 | ... | October 07, 2026 (Wednesday)",
              VRRR_SEP11N)])

aug_share = 98945 / 200000 * 100
oct_share = 18170 / 150000 * 100
assert round(aug_share, 1) == 49.5 and round(oct_share, 1) == 12.1
Q("008", T, S, "Advanced",
  "RBI's 7-day VRRR of 17 August 2026 (notified ₹2,00,000 crore) drew offers of ₹98,945 crore, all accepted at 5.24%; "
  "its 10-day VRRR of 9 October 2026 (notified ₹1,50,000 crore) drew ₹18,170 crore, all accepted at 5.49%. Which "
  "statement is correct?",
  ["About 49% of the notified amount was absorbed in August against about 12% in October, and the higher October rate "
   "reflects the repo rate having risen to 5.50%",
   "Both auctions were oversubscribed, so partial acceptance applied",
   "The October rate was higher because the SDF had been cut",
   "About 12% was absorbed in August against 49% in October"],
  concept="Variable rate reverse repo auctions",
  explanation="August: 98,945 ÷ 2,00,000 ≈ 49.5%; October: 18,170 ÷ 1,50,000 ≈ 12.1%. Both were undersubscribed, so all "
              "offers were accepted. Cut-offs sit just below the repo rate: 5.24% when repo was 5.25% (August) and 5.49% "
              "after the repo was raised to 5.50% on 7 October.",
  steps=["Aug: 49.5% of notified", "Oct: 12.1% of notified", "Rates track the repo: 5.25 → 5.50"],
  why="Neither auction was oversubscribed; the SDF was raised, not cut; the shares are reversed in the last option.",
  computed=True, current=ca("2026-10-09"),
  facts=[fact("7-day VRRR (17 Aug 2026): Notified Amount 2,00,000; Total amount of offers received 98,945; Amount accepted "
              "98,945; Cut off Rate 5.24", VRRR_AUG17),
         fact("10-day VRRR (9 Oct 2026): Notified Amount 1,50,000; Total amount of offers received 18,170; Amount accepted "
              "18,170; Cut off Rate 5.49", VRRR_OCT9)])

Q("009", T, S, "Basic",
  "According to RBI's monetary policy page, what is the position of fixed rate reverse repo operations since the "
  "Standing Deposit Facility was introduced?",
  ["They are conducted at RBI's discretion for purposes specified from time to time",
   "They are conducted daily as the floor of the corridor", "They have been abolished by law",
   "They are available only to Regional Rural Banks"],
  concept="Reverse repo after the SDF",
  explanation="RBI defines the reverse repo rate as the rate at which it absorbs liquidity against eligible government "
              "securities under the LAF, and states that, following the SDF's introduction, fixed rate reverse repo "
              "operations will be at RBI's discretion for purposes specified from time to time.",
  steps=["SDF = floor", "Fixed reverse repo → discretionary"],
  why="The SDF, not the reverse repo, is the floor; it was not abolished or limited to RRBs.",
  facts=[fact("Following the introduction of SDF, the fixed rate reverse repo operations will be at the discretion of the "
              "RBI for purposes specified from time to time", MPF)])
Q("009", T, S, "Intermediate",
  "Under the liquidity framework of September 2025, transient liquidity is managed through VRR/VRRR operations of "
  "tenor from overnight up to 14 days. How do RBI's 30-day and 26-day VRRRs of September 2026 fit into this "
  "framework?",
  ["As long-term reverse repo operations (tenor beyond a fortnight), an instrument for managing durable liquidity",
   "As the 7-day main operation", "As Standing Deposit Facility deposits", "As Marginal Standing Facility operations"],
  concept="Tenor of liquidity operations",
  explanation="The framework's annex lists VRR/VRRR of overnight to a fortnight for transient liquidity and long-term "
              "VRR/VRRR (tenor beyond a fortnight) among durable liquidity instruments. 26- and 30-day VRRRs therefore "
              "fall in the long-term category.",
  steps=["Tenor > 14 days → long-term VRRR → durable liquidity tool"],
  why="They are not 7-day operations; the SDF and MSF are standing facilities.",
  current=ca("2026-09-11"),
  facts=[fact("Instruments ... for managing durable liquidity viz. open market operations (OMOs), long-term variable rate "
              "repo/reverse repo operations and forex swap auctions will continue", LMF),
         fact("Variable Rate Repo (VRR)/Variable Rate Reverse Repo (VRRR) auction Tenor: overnight to a fortnight ... "
              "Tenor: beyond a fortnight", LMF)])

sep_ratio = 60449 / 259276 * 100
assert round(sep_ratio, 1) == 23.3
Q("009", T, S, "Advanced",
  "RBI's 30-day VRRR of 7 September 2026 (notified ₹7,00,000 crore) drew ₹2,59,276 crore and its 26-day VRRR of 11 "
  "September (notified ₹5,00,000 crore) drew ₹60,449 crore, all accepted at 5.24% (repo 5.25%, SDF 5.00%). Consider:\n"
  "I. The 26-day auction drew less than a quarter of the amount offered in the 30-day auction.\n"
  "II. Both cut-off rates lay inside the LAF corridor, 1 bp below the repo rate.\n"
  "III. Both auctions were fully subscribed.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Term VRRR outcomes",
  explanation="60,449 ÷ 2,59,276 ≈ 23.3%, less than a quarter (I). 5.24% lies between the SDF (5.00%) and MSF (5.50%), "
              "1 bp below the 5.25% repo rate (II). Both drew far less than notified, so III is wrong.",
  steps=["I: 23.3% < 25% → true", "II: 5.24% inside 5.00–5.50 → true", "III: false"],
  why="Options with III are wrong; 'I only' leaves out II.",
  computed=True, current=ca("2026-09-11"),
  facts=[fact("30-day VRRR: Notified Amount 7,00,000; Total amount of offers received 2,59,276; Amount accepted 2,59,276; "
              "Cut off Rate 5.24", VRRR_SEP7),
         fact("26-day VRRR: Notified Amount 5,00,000; Total amount of offers received 60,449; Amount accepted 60,449; Cut "
              "off Rate 5.24", VRRR_SEP11)])

Q("010", T, S, "Basic",
  "After the MPC's repo rate cut of April 2025, at what level did the Standing Deposit Facility (SDF) rate stand?",
  ["5.75%", "6.00%", "6.25%", "5.50%"],
  concept="SDF as the corridor floor",
  explanation="The SDF is 25 bps below the repo rate. With the repo cut to 6.00% in April 2025, the SDF stood at 5.75% "
              "(and the MSF/Bank Rate at 6.25%).",
  steps=["SDF = 6.00 − 0.25 = 5.75%"],
  why="6.00% was the repo rate; 6.25% the MSF; 5.50% came later.",
  current=ca("2025-04-09"),
  facts=[fact("Consequently, the standing deposit facility (SDF) rate under the liquidity adjustment facility (LAF) shall "
              "stand adjusted to 5.75 per cent", MPC_APR25)])
Q("010", T, S, "Intermediate",
  "RBI conducted a 4-day VRRR on Thursday, 1 October 2026 (notified ₹2,00,000 crore). Offers of ₹1,68,055 crore were "
  "all accepted at 5.24%. On which day was it reversed?",
  ["Monday, 5 October 2026", "Friday, 2 October 2026", "Wednesday, 7 October 2026", "Thursday, 8 October 2026"],
  concept="Reverse repo tenor",
  explanation="A 4-day VRRR from Thursday 1 October reverses on Monday 5 October 2026, as RBI's notice stated — two days "
              "before the MPC raised the repo rate.",
  steps=["1 Oct + 4 days = 5 Oct (Monday)"],
  why="The other dates do not match a 4-day tenor.",
  current=ca("2026-10-01"),
  facts=[fact("VRRR auction on Thursday, October 01, 2026: 2,00,000 | 4 | 09:30 AM to 10:00 AM | October 05, 2026 "
              "(Monday)", VRRR_OCT1N),
         fact("Total amount of offers received 1,68,055; Amount accepted 1,68,055; Cut off Rate 5.24", VRRR_OCT1)])

# ============================================================================================ CRR
T = "CRR"
Q("008", T, "CRR value", "Basic",
  "Under the phased CRR reduction announced in June 2025, what CRR did banks have to maintain from the reporting "
  "fortnight beginning 6 September 2025, the first tranche?",
  ["3.75% of NDTL", "3.50% of NDTL", "4.00% of NDTL", "3.25% of NDTL"],
  concept="Phased CRR cut of 2025",
  explanation="RBI cut the CRR by 100 bps in four equal tranches of 25 bps: 3.75% from 6 September, 3.5% from 4 October, "
              "3.25% from 1 November and 3.0% from 29 November 2025.",
  steps=["4.00 − 0.25 = 3.75% from 6 Sep 2025"],
  why="3.50% and 3.25% were later tranches; 4.00% was the level before the cut.",
  current=ca("2025-09-06"),
  facts=[fact("banks are required to maintain the CRR at 3.75 per cent, 3.5 per cent, 3.25 per cent and 3.0 per cent of "
              "their NDTL effective from the reporting fortnight beginning September 6, October 4, November 1 and "
              "November 29, 2025, respectively", CRR25)])
Q("008", T, "CRR value", "Intermediate",
  "After peaking at 15% in July 1989, when was the CRR first reduced, according to RBI's table of CRR changes?",
  ["17 April 1993, to 14.5%", "4 July 1991, to 14%", "25 October 1997, to 9.75%", "1 July 1974, to 5%"],
  concept="History of CRR",
  explanation="RBI's table shows CRR at 15% from 1 July 1989 (with additional incremental requirements) until it was cut "
              "to 14.5% on 17 April 1993, and 14% on 15 May 1993.",
  steps=["15% (1989–1993) → 14.5% on 17 Apr 1993"],
  why="4 July 1991 was a Bank Rate change; 25 October 1997 and 1 July 1974 are other CRR changes.",
  facts=[fact("Cash Reserve Ratio: 15 @ 1/7/1989 ... 14.5 17-04-1993; 14 15-05-1993", RATES)])
Q("008", T, "CRR concept", "Intermediate",
  "According to a footnote in RBI's table of CRR changes, what special relief was given to banks for the 'millennium "
  "change' (Y2K)?",
  ["Cash in hand could be counted for CRR from 1 December 1999 to 31 January 2000, but not simultaneously for SLR",
   "CRR was suspended for December 1999", "CRR was reduced to zero for one fortnight",
   "Banks could count their SLR securities towards CRR"],
  concept="CRR eligible balances",
  explanation="To help banks tide over the millennium change, cash in hand maintained for CRR was treated as eligible "
              "for CRR for two months (1 December 1999–31 January 2000); that cash could not simultaneously count as an "
              "SLR asset. Normally CRR is a balance with RBI.",
  steps=["Normally CRR = balance with RBI", "Y2K: cash in hand counted for 2 months, not double-counted for SLR"],
  why="CRR was not suspended or cut to zero, and SLR securities never count for CRR.",
  facts=[fact("to facilitate banks to tide over the contingency during the millennium change, it has been decided to treat "
              "cash in hand maintained by banks for compliance of CRR for a limited period of two months commencing from "
              "December 1,1999 to January 31, 2000. The cash in hand which will be counted for CRR purpose, during the "
              "above period cannot be treatrd as eligible asset for SLR purpose simulataneously", RATES)])
Q("008", T, "CRR value", "Intermediate",
  "RBI's table of CRR changes shows a series of increases in 1981–82. What was the highest CRR reached in that phase, "
  "before cuts later in 1982?",
  ["7.75%, from 29 January 1982", "7.5%, from 25 December 1981", "8.5%, from 27 August 1983", "15%, from 1 July 1989"],
  concept="History of CRR",
  explanation="CRR rose from 6.5% (July 1981) through 7%, 7.25% and 7.5% to 7.75% on 29 January 1982, and was then cut "
              "to 7.25% (April 1982) and 7% (June 1982).",
  steps=["1981–82 peak = 7.75% (29 Jan 1982)"],
  why="7.5% was the preceding step; 8.5% (1983) and 15% (1989) belong to later phases.",
  facts=[fact("Cash Reserve Ratio: 6.5 31-07-1981; 7 21-08-1981; 7.25 27-11-1981; 7.5 25-12-1981; 7.75 29-01-1982; 7.25 "
              "9/4/1982; 7 11/6/1982", RATES)])

ndtl73 = 1000
assert ndtl73 * (7 - 3) / 100 == 40
Q("008", T, "CRR value", "Advanced",
  "RBI's table shows the CRR raised in 1973 from 3% to 5% (29 June), 6% (8 September) and 7% (22 September). For a "
  "bank with net demand and time liabilities of ₹1,000 crore, how much additional cash had to be kept with RBI by the "
  "end of September 1973 compared with June 1973?",
  ["₹40 crore", "₹20 crore", "₹70 crore", "₹10 crore"],
  concept="Impact of CRR changes",
  explanation="CRR went from 3% to 7%, an increase of 4 percentage points: 4% × ₹1,000 crore = ₹40 crore of additional "
              "impounded cash.",
  steps=["7% − 3% = 4%", "4% × 1,000 = ₹40 crore"],
  why="₹20 crore counts only the first step; ₹70 crore is the total CRR, not the increase; ₹10 crore one 1% step.",
  computed=True,
  facts=[fact("Cash Reserve Ratio: 3 16-09-1962; 5 29-06-1973; 6 8/9/1973; 7 22-09-1973", RATES)])

Q("009", T, "CRR value", "Basic",
  "Under the phased CRR cut of 2025, what CRR applied from the reporting fortnight beginning 4 October 2025?",
  ["3.5% of NDTL", "3.75% of NDTL", "3.0% of NDTL", "4.0% of NDTL"],
  concept="Phased CRR cut of 2025",
  explanation="The tranches were 3.75% (6 September), 3.5% (4 October), 3.25% (1 November) and 3.0% (29 November 2025).",
  steps=["Second tranche → 3.5% from 4 Oct 2025"],
  why="3.75% was the first tranche, 3.0% the last; 4.0% the starting level.",
  current=ca("2025-10-04"),
  facts=[fact("the average Cash Reserve Ratio (CRR) required to be maintained by every bank shall be 3.75 per cent, 3.5 per "
              "cent, 3.25 per cent and 3.0 per cent of its net demand and time liabilities effective from the reporting "
              "fortnight beginning September 6, October 4, November 1 and November 29, 2025, respectively", CRR25)])
Q("009", T, "CRR concept", "Intermediate",
  "According to RBI's profile of its Governors, during whose tenure was the variable cash reserve ratio used as a "
  "monetary policy instrument for the first time?",
  ["H. V. R. Iengar (1957–1962)", "Sir C. D. Deshmukh (1943–1949)", "L. K. Jha (1967–1970)", "I. G. Patel (1977–1982)"],
  concept="CRR as a monetary tool",
  explanation="RBI's profile of H. V. R. Iengar says that in monetary policy 'the variable cash reserve ratio was used "
              "for the first time as were the selective credit controls'. The CRR was fixed uniformly at 3% with "
              "flexibility of 3–15% from September 1962.",
  steps=["First use of variable CRR → Iengar's tenure"],
  why="The other Governors served before or after this development.",
  facts=[fact("In the sphere of monetary policy, the variable cash reserve ratio was used for the first time as were the "
              "selective credit controls (H V R Iengar)", GOVS)])
Q("009", T, "CRR value", "Advanced",
  "Consider the following statements about the CRR reduction of 2025:\n"
  "I. CRR was cut by 100 basis points in four equal tranches of 25 basis points.\n"
  "II. The reduction was announced in the Governor's statement of 6 June 2025.\n"
  "III. The first tranche took effect in August 2025.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Phased CRR cut of 2025",
  explanation="RBI's circular says that, as announced in the Governor's statement of 6 June 2025 (II), CRR was cut by "
              "100 bps in four equal tranches of 25 bps (I). The first tranche took effect from the fortnight beginning "
              "6 September 2025, so III is wrong.",
  steps=["I: true", "II: true", "III: false – first tranche 6 Sep 2025"],
  why="Options with III are wrong; 'I only' leaves out II.",
  current=ca("2025-06-06"),
  facts=[fact("As announced in the Governor's Statement dated June 06, 2025, it has been decided to reduce the Cash Reserve "
              "Ratio (CRR) of all banks by 100 basis points in four equal tranches of 25 basis points each to 3.0 per cent "
              "of net demand and time Liabilities (NDTL) ... effective from the reporting fortnight beginning September "
              "6", CRR25)])

Q("010", T, "CRR value", "Basic",
  "In November 2001 RBI cut the CRR sharply in a single step. According to RBI's table, from 7.5% to what level (3 "
  "November 2001)?",
  ["5.75%", "5.5%", "4.75%", "7%"],
  concept="History of CRR",
  explanation="RBI's table shows CRR at 7.5% from 19 May 2001, cut to 5.75% on 3 November 2001, then 5.5% (29 December "
              "2001), 5% (1 June 2002) and 4.75% (16 November 2002).",
  steps=["7.5% → 5.75% (3 Nov 2001)"],
  why="5.5% and 4.75% came later; 7% is not the November 2001 level.",
  facts=[fact("Cash Reserve Ratio: 7.5 19-05-2001; 5.75 3/11/2001; 5.5 29-12-2001; 5 01.06.2002; 4.75 16.11.2002", RATES)])
Q("010", T, "CRR value", "Intermediate",
  "After being cut to 14% in May 1993, the CRR was raised again in 1994. According to RBI's table, it returned to 15% "
  "on:",
  ["6 August 1994", "1 July 1989", "11 November 1995", "17 April 1993"],
  concept="History of CRR",
  explanation="CRR went 14.5% (11 June 1994) → 14.75% (9 July 1994) → 15% (6 August 1994), and was cut again to 14.5% "
              "on 11 November 1995.",
  steps=["1994: 14.5 → 14.75 → 15% (6 Aug 1994)"],
  why="1 July 1989 was the first time it reached 15%; 11 Nov 1995 and 17 Apr 1993 were cuts.",
  facts=[fact("Cash Reserve Ratio: 14.5 11/6/1994; 14.75 9/7/1994; 15 6/8/1994; 14.5 11/11/1995", RATES)])
Q("010", T, "CRR value", "Intermediate",
  "RBI's table of CRR changes shows three increases in 1983. What level did CRR reach on 27 August 1983?",
  ["8.5%", "8%", "7.5%", "9%"],
  concept="History of CRR",
  explanation="CRR was raised to 7.5% (27 May 1983), 8% (29 July 1983) and 8.5% (27 August 1983); it reached 9% in "
              "February 1984.",
  steps=["1983: 7.5 → 8 → 8.5% (27 Aug)"],
  why="7.5% and 8% were the earlier steps of 1983; 9% came in 1984.",
  facts=[fact("Cash Reserve Ratio: 7.5 27-05-1983; 8 29-07-1983; 8.5 27-08-1983; ... 9 @ 4/2/1984", RATES)])
Q("010", T, "CRR value", "Advanced",
  "Consider the following statements based on RBI's table of CRR changes:\n"
  "I. CRR fell below 10% for the first time in that reform phase on 25 October 1997, when it was cut to 9.75%.\n"
  "II. CRR was raised to 11% on 29 August 1998.\n"
  "III. CRR first fell below 5% only in 2003.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="History of CRR",
  explanation="CRR was 10% from 18 January 1997 and cut to 9.75% on 25 October 1997 (I). It was raised to 11% on 29 "
              "August 1998 (II). It fell to 4.75% on 16 November 2002, so III is wrong.",
  steps=["I: true", "II: true", "III: false – 4.75% in Nov 2002"],
  why="Options with III are wrong; 'I only' leaves out II.",
  facts=[fact("Cash Reserve Ratio: 10 18-01-1997; 9.75 25-10-1997; ... 11 29-08-1998; ... 4.75 16.11.2002", RATES)])

crr_9911, crr_0004, nd = 9.5, 8.0, 10000
assert nd * (crr_9911 - crr_0004) / 100 == 150
Q("010", T, "CRR value", "Advanced",
  "RBI's table shows CRR at 9.5% from 6 November 1999, 9% from 20 November 1999, 8.5% from 8 April 2000 and 8% from 22 "
  "April 2000. How much cash was released for a bank with NDTL of ₹10,000 crore between November 1999 and end-April "
  "2000?",
  ["₹150 crore", "₹100 crore", "₹50 crore", "₹950 crore"],
  concept="Impact of CRR cuts",
  explanation="CRR fell from 9.5% to 8%, a cut of 1.5 percentage points: 1.5% × ₹10,000 crore = ₹150 crore released.",
  steps=["9.5 − 8.0 = 1.5%", "1.5% × 10,000 = ₹150 crore"],
  why="₹100 crore uses only 1 point; ₹50 crore one step; ₹950 crore is the whole 9.5% requirement.",
  computed=True,
  facts=[fact("Cash Reserve Ratio: 9.5 @@ 6/11/1999; 9 20-11-1999; 8.5 8/4/2000; 8 22-04-2000", RATES)])

# ============================================================================================ SLR
T = "SLR"
Q("008", T, "SLR value", "Basic",
  "According to RBI's table of reserve requirement changes, at what level was the Statutory Liquidity Ratio first "
  "prescribed, from 16 March 1949?",
  ["20%", "25%", "38.5%", "18%"],
  concept="History of SLR",
  explanation="SLR was introduced with the Banking Companies Act, 1949, which came into force on 16 March 1949; RBI's "
              "table shows the first SLR at 20% from that date.",
  steps=["16 Mar 1949 → SLR 20%"],
  why="25% came later; 38.5% was the 1990 peak; 18% is today's level.",
  facts=[fact("Statutory Liquidity Ratio: 20 16-03-1949", RATES)])
Q("008", T, "SLR value", "Basic",
  "According to RBI's table, the SLR was raised to 30% in which year?",
  ["1972 (17 November)", "1970 (28 August)", "1978 (1 December)", "1990 (22 September)"],
  concept="History of SLR",
  explanation="RBI's table shows SLR at 29% from 4 August 1972 and 30% from 17 November 1972, then 32% (December 1973) "
              "and 33% (July 1974).",
  steps=["SLR 30% → 17 Nov 1972"],
  why="28 Aug 1970 was 28%; 1 Dec 1978 was 34%; 22 Sep 1990 was 38.5%.",
  facts=[fact("Statutory Liquidity Ratio: 29 4/8/1972; 30 17-11-1972; 32 8/12/1973; 33 1/7/1974", RATES)])
Q("008", T, "SLR concept", "Intermediate",
  "According to RBI's chronology, by mid-1985 the statutory pre-emption of banks' resources through SLR and CRR "
  "together had exceeded:",
  ["45%", "53%", "25%", "60%"],
  concept="Pre-emption of bank resources",
  explanation="RBI's chronology records that by mid-1985 the combined SLR and CRR pre-emption exceeded 45%; after the "
              "CRR was raised to 15% in July 1989, it went above 53%.",
  steps=["Mid-1985 → over 45%", "July 1989 → over 53%"],
  why="53% was the 1989 level; 25% and 60% are not in the chronology.",
  facts=[fact("By mid-1985, the statutory preemption on banks' resources in the form of the Statutory Liquidity Ratio (SLR) "
              "and the Cash Reserve Ratio (CRR) exceeded 45%", CH85)])

base_ndtl, now_ndtl = 1000, 1200
slr_req = base_ndtl * 0.385 + (now_ndtl - base_ndtl) * 0.30
assert round(slr_req) == 445 and round(now_ndtl * 0.385) == 462
Q("008", T, "SLR value", "Advanced",
  "In 1992 SLR was 38.5% of net DTL as on 3 April 1992, plus 30% on any increase in net DTL over that level. A bank's "
  "net DTL was ₹1,000 crore on 3 April 1992 and ₹1,200 crore later in the year. What SLR assets did it need?",
  ["₹445 crore", "₹462 crore", "₹360 crore", "₹385 crore"],
  concept="Incremental SLR",
  explanation="Base: 38.5% × 1,000 = ₹385 crore. Increment: 30% × (1,200 − 1,000) = ₹60 crore. Total ₹445 crore — less "
              "than 38.5% on the whole ₹1,200 crore (₹462 crore), easing the burden on new liabilities.",
  steps=["385 + 0.30 × 200 = 385 + 60 = ₹445 crore"],
  why="₹462 crore applies 38.5% to all liabilities; ₹360 crore applies 30% to all; ₹385 crore ignores the increase.",
  computed=True,
  facts=[fact("38.5 + # (29-02-1992); + : SLR on net DTL as on April 3, 1992. # : In addition there was 30% SLR on the "
              "increase in net DTL over April 3, 1992 level", RATES)])

Q("009", T, "SLR value", "Basic",
  "According to RBI's table, the SLR was raised to 38% (just below its 1990 peak of 38.5%) on:",
  ["2 January 1988", "25 April 1987", "6 July 1985", "22 September 1990"],
  concept="History of SLR",
  explanation="The table shows 37.5% from 25 April 1987, 38% from 2 January 1988 and 38.5% from 22 September 1990.",
  steps=["38% → 2 Jan 1988"],
  why="25 Apr 1987 was 37.5%; 6 Jul 1985 was 37%; 22 Sep 1990 was 38.5%.",
  facts=[fact("Statutory Liquidity Ratio: 37 6/7/1985; 37.5 25-04-1987; 38 2/1/1988; 38.5 22-09-1990", RATES)])
Q("009", T, "SLR concept", "Intermediate",
  "According to a footnote in RBI's table of reserve requirements, how did the basis of computing SLR change after 29 "
  "March 1985?",
  ["From gross DTL as on every Friday (maintained daily the next week) to net DTL as on the last Friday of the second "
   "preceding fortnight (maintained daily on a fortnightly basis)",
   "From net DTL to gross DTL", "From weekly to annual maintenance", "From cash only to government securities only"],
  concept="Basis of SLR computation (historical)",
  explanation="Till 29 March 1985 SLR was a proportion of gross DTL as on every Friday, maintained daily in the following "
              "week; thereafter it was maintained daily on a fortnightly basis as a proportion of net DTL as on the last "
              "Friday of the second preceding fortnight. (The fortnight was later redefined from December 2025.)",
  steps=["Before 1985: gross DTL, weekly", "After: net DTL, fortnightly"],
  why="The change was from gross to net, not the reverse; maintenance did not become annual; eligible assets did not "
      "change this way.",
  facts=[fact("Till March 29, 1985 the banks were required to maintain statutory liquidity ratio as a prescribed "
              "proportion of gross DTL as on every Friday in the following week on daily basis. Thereafter, it is "
              "maintained daily on a fortnightly basis as a prescribed portion of net DTL as on last Friday of second "
              "preceding fortnight", RATES)])
Q("009", T, "SLR value", "Intermediate",
  "From 16 October 1993, SLR was 34.75% of net DTL as on 17 September 1993. What applied to the increase in net DTL "
  "over that date's level?",
  ["An SLR of 25% on the increase", "An SLR of 30% on the increase", "No SLR on the increase",
   "An SLR of 38.5% on the increase"],
  concept="Incremental SLR in the 1990s",
  explanation="RBI's footnotes say that alongside 34.75% on the base, there was an additional 25% SLR on the increase in "
              "net DTL over the 17 September 1993 level. (The 1992 rule had 30% on the increase over 3 April 1992.)",
  steps=["Base 34.75%; increment 25%"],
  why="30% was the 1992 incremental rate; the increase was not exempt; 38.5% was the earlier base.",
  facts=[fact("34.75 ^ $ 16-10-1993; ^ : SLR on net DTL as on September 17, 1993. $ : In addition there was 25% SLR on the "
              "increase in net DTL over September 17, 1993 level", RATES)])
Q("009", T, "SLR value", "Intermediate",
  "RBI's table shows the SLR at 33% from 1 July 1974. To what level was it next raised, on 1 December 1978?",
  ["34%", "35%", "32%", "36%"],
  concept="History of SLR",
  explanation="SLR moved from 33% (1 July 1974) to 34% (1 December 1978), then 34.5% and 35% in 1981.",
  steps=["33% (1974) → 34% (Dec 1978)"],
  why="35% came in October 1981; 32% was the 1973 level; 36% came in 1984.",
  facts=[fact("Statutory Liquidity Ratio: 33 1/7/1974; 34 1/12/1978; 34.5 25-09-1981; 35 30-10-1981", RATES)])
Q("009", T, "SLR value", "Advanced",
  "Consider the following statements based on RBI's table of SLR changes:\n"
  "I. From 29 October 1994, SLR was 31.5% of net DTL as on 30 September 1994.\n"
  "II. In addition, a 25% SLR applied to the increase in net DTL over the 30 September 1994 level.\n"
  "III. SLR was raised to 40% in 1997.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="SLR in the reform period",
  explanation="The table and footnotes show 31.5% on net DTL as on 30 September 1994 (I) plus 25% on the increase over "
              "that level (II). SLR was reduced, not raised, by 1997 — to 25% from 25 October 1997 — so III is wrong.",
  steps=["I: true", "II: true", "III: false – SLR cut to 25% in Oct 1997"],
  why="Options with III are wrong; 'I only' leaves out II.",
  facts=[fact("31.5 ! & 29-10-1994; ! : SLR on net DTL as on September 30,1994. & : In addition there was 25% SLR on the "
              "increase in net DTL over September 30, 1994 level", RATES),
         fact("Statutory Liquidity Ratio: 25 25-10-1997", RATES)])

Q("010", T, "SLR value", "Basic",
  "According to RBI's table, on 1 July 1974 the SLR was raised to 33%. What happened to the CRR on the same day?",
  ["It was cut from 7% to 5%", "It was raised from 5% to 7%", "It was left at 3%", "It was raised to 15%"],
  concept="SLR and CRR moving together",
  explanation="RBI's table shows SLR raised to 33% and CRR reduced to 5% (from 7%) with effect from 1 July 1974.",
  steps=["1 Jul 1974: SLR 33%; CRR 7% → 5%"],
  why="CRR was cut, not raised; 3% applied before 1973; 15% came in 1989.",
  facts=[fact("Statutory Liquidity Ratio: 33 1/7/1974; Cash Reserve Ratio: 7 22-09-1973; 5 1/7/1974", RATES)])
Q("010", T, "SLR value", "Intermediate",
  "In which year did the SLR first reach 36% of DTL, according to RBI's table?",
  ["1984 (1 September)", "1985 (8 June)", "1981 (30 October)", "1987 (25 April)"],
  concept="History of SLR",
  explanation="SLR was 35.5% from 28 July 1984 and 36% from 1 September 1984; it was 36.5% from 8 June 1985 and 37% from "
              "6 July 1985.",
  steps=["36% → 1 Sep 1984"],
  why="8 June 1985 was 36.5%; 30 Oct 1981 was 35%; 25 Apr 1987 was 37.5%.",
  facts=[fact("Statutory Liquidity Ratio: 35.5 28-07-1984; 36 1/9/1984; 36.5 8/6/1985; 37 6/7/1985", RATES)])

slr70, slr74, nd2 = 28, 33, 2000
assert nd2 * (slr74 - slr70) / 100 == 100
Q("010", T, "SLR value", "Advanced",
  "RBI's table shows SLR at 28% from 28 August 1970 and 33% from 1 July 1974. For a bank with DTL of ₹2,000 crore, by "
  "how much did its required SLR holdings rise between these dates (DTL unchanged)?",
  ["₹100 crore", "₹50 crore", "₹660 crore", "₹560 crore"],
  concept="Impact of SLR changes",
  explanation="SLR rose by 5 percentage points (28% → 33%): 5% × ₹2,000 crore = ₹100 crore of additional SLR assets.",
  steps=["33 − 28 = 5%", "5% × 2,000 = ₹100 crore"],
  why="₹50 crore uses 2.5%; ₹660 crore and ₹560 crore are total requirements at 33% and 28%.",
  computed=True,
  facts=[fact("Statutory Liquidity Ratio: 28 28-08-1970; ... 33 1/7/1974", RATES)])

# ============================================================================================ Bank Rate
T = "Bank Rate"
S = "Bank rate and MSF"
Q("008", T, S, "Basic",
  "RBI's first Bank Rate (5 July 1935) was 3.5%. According to RBI's table, to what was it cut on 28 November 1935, a "
  "level that lasted until November 1951?",
  ["3%", "4%", "2.5%", "3.25%"],
  concept="History of the Bank Rate",
  explanation="The Bank Rate was cut to 3% on 28 November 1935 and raised back to 3.5% only on 15 November 1951.",
  steps=["3.5% → 3% (28 Nov 1935) → 3.5% (15 Nov 1951)"],
  why="The other levels do not appear for that period.",
  facts=[fact("Bank Rate: 3.5 5/7/1935; 3 28-11-1935; 3.5 15-11-1951", RATES)])
Q("008", T, S, "Intermediate",
  "Amid the inflation of the oil-shock years, RBI's table shows the Bank Rate raised from 7% (31 May 1973) to what level "
  "on 23 July 1974?",
  ["9%", "8%", "10%", "12%"],
  concept="History of the Bank Rate",
  explanation="The Bank Rate went from 7% (31 May 1973) to 9% (23 July 1974) and stayed there until it was raised to 10% "
              "in July 1981.",
  steps=["1974: 7% → 9%"],
  why="10% came in 1981 and 12% in 1991; 8% is not the 1974 level.",
  facts=[fact("Bank Rate: 7 31-05-1973; 9 23-07-1974; 10 12/7/1981", RATES)])

br97 = [12, 11, 10, 9]
assert (br97[0] - br97[-1]) * 100 == 300
Q("008", T, S, "Advanced",
  "RBI's table shows the Bank Rate at 12% from 9 October 1991, then 11% (16 April 1997), 10% (26 June 1997) and 9% (22 "
  "October 1997). What was the total cut in 1997, and what happened next?",
  ["300 bps; it was raised by 200 bps to 11% in January 1998", "300 bps; it was cut further to 8% in January 1998",
   "200 bps; it stayed at 9% until 2003", "100 bps; it was raised to 12% in 1998"],
  concept="Bank Rate in the 1990s",
  explanation="12% → 9% in 1997 = 300 bps of cuts. On 17 January 1998, amid the Asian crisis, it was raised to 11%.",
  steps=["12 − 9 = 3 points = 300 bps", "Jan 1998: 9% → 11%"],
  why="The January 1998 move was an increase; the 1997 cut was 300 bps.",
  computed=True,
  facts=[fact("Bank Rate: 12 9/10/1991; 11 16-04-1997; 10 26-06-1997; 9 22-10-1997; 11 17-01-1998", RATES)])

Q("009", T, S, "Basic",
  "According to RBI's table, the Bank Rate was raised to 4% on which date?",
  ["16 May 1957", "15 November 1951", "3 January 1963", "26 September 1964"],
  concept="History of the Bank Rate",
  explanation="The Bank Rate was 3.5% from 15 November 1951 and 4% from 16 May 1957; it was 4.5% from 3 January 1963 and "
              "5% from 26 September 1964.",
  steps=["4% → 16 May 1957"],
  why="The other dates correspond to 3.5%, 4.5% and 5%.",
  facts=[fact("Bank Rate: 3.5 15-11-1951; 4 16-05-1957; 4.5 3/1/1963; 5 26-09-1964", RATES)])
Q("009", T, S, "Intermediate",
  "During the 1991 crisis the Bank Rate was raised to 12% on 9 October 1991. What had it been raised to earlier, on 4 "
  "July 1991?",
  ["11%", "10%", "10.5%", "9%"],
  concept="Bank Rate in the 1991 crisis",
  explanation="RBI's table shows 10% (from July 1981), 11% (4 July 1991) and 12% (9 October 1991).",
  steps=["10% → 11% (4 Jul 1991) → 12% (9 Oct 1991)"],
  why="10% was the level before July 1991; the others are not in the sequence.",
  facts=[fact("Bank Rate: 10 12/7/1981; 11 4/7/1991; 12 9/10/1991", RATES)])

br = [8.0, 7.5, 7.0, 6.5, 6.25]
assert round((br[0] - br[-1]) * 100) == 175
Q("009", T, S, "Advanced",
  "RBI's table shows the Bank Rate at 8% (22 July 2000), 7.5% (17 February 2001), 7% (2 March 2001), 6.5% (23 October "
  "2001) and 6.25% (30 October 2002). How large was the total reduction, and over how many cuts?",
  ["175 bps over four cuts", "150 bps over three cuts", "175 bps over five cuts", "200 bps over four cuts"],
  concept="Bank Rate in the early 2000s",
  explanation="8.00 → 6.25 = 1.75 points = 175 bps, through four cuts (Feb 2001, Mar 2001, Oct 2001, Oct 2002).",
  steps=["8.00 − 6.25 = 1.75 → 175 bps", "Cuts: 4"],
  why="The other options miscount the cuts or the total.",
  computed=True,
  facts=[fact("Bank Rate: 8 22-07-2000; 7.5 17-02-2001; 7 2/3/2001; 6.5 23-10-2001; 6.25 30.10.2002", RATES)])

Q("010", T, S, "Basic",
  "Following the MPC's repo rate cut of April 2025, at what level did the Bank Rate stand?",
  ["6.25%", "6.00%", "6.50%", "5.75%"],
  concept="Bank Rate aligned with the MSF",
  explanation="The Bank Rate moves with the MSF rate, 25 bps above the repo rate. With the repo at 6.00% in April 2025, "
              "the MSF rate and Bank Rate were 6.25%.",
  steps=["Repo 6.00% + 0.25 = 6.25%"],
  why="6.00% was the repo; 6.50% the Bank Rate after February 2025; 5.75% the SDF in April.",
  current=ca("2025-04-09"),
  facts=[fact("the marginal standing facility (MSF) rate and the Bank Rate to 6.25 per cent", MPC_APR25)])
Q("010", T, S, "Intermediate",
  "According to RBI's table, the Bank Rate reached 6% for the first time on:",
  ["17 February 1965", "26 September 1964", "9 January 1971", "2 March 1968"],
  concept="History of the Bank Rate",
  explanation="The Bank Rate went 5% (26 September 1964) → 6% (17 February 1965); it was cut to 5% on 2 March 1968 and "
              "restored to 6% on 9 January 1971.",
  steps=["First 6% → 17 Feb 1965"],
  why="26 Sep 1964 was 5%; 9 Jan 1971 was a return to 6%; 2 Mar 1968 was a cut to 5%.",
  facts=[fact("Bank Rate: 5 26-09-1964; 6 17-02-1965; 5 2/3/1968; 6 9/1/1971", RATES)])
Q("010", T, S, "Intermediate",
  "Under the liquidity management framework of September 2025, how much can an individual bank draw under the Marginal "
  "Standing Facility, whose rate is the same as the Bank Rate?",
  ["Against its excess SLR holdings plus up to 2% of its NDTL (as at the end of the second preceding fortnight) below "
   "the stipulated SLR", "Up to 2% of NDTL only, with no use of excess SLR", "Any amount, without collateral",
   "Up to 1% of NDTL"],
  concept="MSF access",
  explanation="The annex to the framework says banks can draw MSF funds against their excess SLR holdings plus up to 2% "
              "of NDTL outstanding at the end of the second preceding fortnight, below the stipulated SLR.",
  steps=["MSF = excess SLR + dip of up to 2% of NDTL"],
  why="Excess SLR also counts; MSF is collateralised; 1% was the 2011 limit.",
  facts=[fact("Marginal Standing Facility (MSF) | Individual banks can draw funds against their excess SLR holdings + up to "
              "2 per cent of their respective NDTL outstanding as at the end of the second preceding fortnight, below the "
              "stipulated SLR", LMF)])

br_feb, br_jun = 6.50, 5.75
assert round((br_feb - br_jun) * 100) == 75
Q("010", T, S, "Advanced",
  "The Bank Rate was 6.50% after the MPC decision of February 2025. After the June 2025 decision it was 5.75%. Consider:\n"
  "I. The Bank Rate fell by 75 bps between these two decisions.\n"
  "II. The Bank Rate moved automatically with the MSF rate as the repo rate was cut.\n"
  "III. The Bank Rate remained 50 bps above the repo rate throughout.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Bank Rate and the corridor",
  explanation="6.50 − 5.75 = 0.75 → 75 bps (I). The Bank Rate is aligned with the MSF rate and changes automatically "
              "with it (II). The MSF/Bank Rate is 25 bps above the repo rate (6.50 vs 6.25; 5.75 vs 5.50), so III is "
              "wrong.",
  steps=["I: 75 bps → true", "II: true", "III: 25 bps, not 50 → false"],
  why="Options with III are wrong; 'I only' leaves out II.",
  computed=True,
  facts=[fact("the marginal standing facility (MSF) rate and the Bank Rate to 6.50 per cent", MPC_FEB25),
         fact("the marginal standing facility (MSF) rate and the Bank Rate to 5.75 per cent", MPC_JUN25),
         fact("This rate has been aligned with the MSF rate and, changes automatically as and when the MSF rate changes "
              "alongside policy repo rate changes", MPF)])

# ============================================================================================ Inflation
T = "Inflation"
Q("008", T, "CPI and WPI", "Basic",
  "According to MoSPI's CPI (base 2024=100) release for September 2026, from how many markets are real-time prices "
  "collected?",
  ["1,407 urban markets (including online markets) and 1,465 villages", "1,181 urban markets and 1,114 villages",
   "2,000 urban markets and 2,000 villages", "All 1.2 lakh bank branches"],
  concept="Compilation of the CPI",
  explanation="Prices are collected from 1,407 urban markets (including online markets) and 1,465 villages covering all "
              "States/UTs, by NSO field staff on a weekly roster; the response rate in September 2026 was 100%.",
  steps=["1,407 urban + 1,465 rural"],
  why="The other numbers are not in the release.",
  current=ca("2026-10-12"),
  facts=[fact("Real time price data are collected from selected 1407 urban Markets (including online markets) and 1465 "
              "villages covering all States/UTs", CPI_SEP26)])
Q("008", T, "Inflation targeting", "Basic",
  "On which date did the Central Government first notify the 4% CPI inflation target (with 2%–6% tolerance band)?",
  ["5 August 2016", "29 September 2016", "31 March 2021", "1 April 2016"],
  concept="Flexible inflation targeting",
  explanation="On 5 August 2016 the Government notified 4% CPI inflation as the target for 5 August 2016 to 31 March "
              "2021. The first MPC was constituted on 29 September 2016; the first review was on 31 March 2021.",
  steps=["First notification → 5 Aug 2016"],
  why="29 Sep 2016 is the MPC's constitution; 31 Mar 2021 the first review.",
  facts=[fact("on August 5, 2016, the Central Government notified in the Official Gazette 4 per cent Consumer Price Index "
              "(CPI) inflation as the target for the period from August 5, 2016 to March 31, 2021", MPF)])
Q("008", T, "CPI and WPI", "Intermediate",
  "The June 2026 MPC resolution noted that petrol and diesel prices had been raised cumulatively since May by 7.4% and "
  "8.4%. What direct impact on headline CPI inflation did it estimate?",
  ["About 36 basis points", "About 100 basis points", "About 8 basis points", "About 60–70 basis points"],
  concept="Fuel prices and CPI",
  explanation="The resolution estimated a direct impact of about 36 bps on headline inflation from the fuel price "
              "increases, with second-order effects to follow.",
  steps=["Fuel price hikes → ~36 bps direct impact"],
  why="60–70 bps was the precious-metals effect cited in February 2026; the others are not stated.",
  current=ca("2026-06-05"),
  facts=[fact("Since May, however, retail fuel prices have been raised cumulatively by 7.4 per cent for petrol and 8.4 per "
              "cent for diesel. The increase implies a direct impact of about 36 basis points on headline inflation",
              MPC_JUN26)])
Q("008", T, "Inflation targeting", "Advanced",
  "Consider the following statements about reviews of India's inflation target:\n"
  "I. In its first review, on 31 March 2021, the Government retained the target and tolerance band for 1 April 2021 to "
  "31 March 2026.\n"
  "II. The second review was made on 25 March 2026.\n"
  "III. RBI's Discussion Paper on the Review of the Monetary Policy Framework invited comments until 18 September "
  "2026.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Reviews of the inflation target",
  explanation="RBI records the first review on 31 March 2021 (I) and the second on 25 March 2026 (II). The Discussion "
              "Paper was placed on 21 August 2025 with comments invited by 18 September 2025, not 2026, so III is wrong.",
  steps=["I: true", "II: true", "III: false – 2025"],
  why="Options with III are wrong; 'I only' leaves out II.",
  current=ca("2026-03-25"),
  facts=[fact("In its first review, on March 31, 2021, the Central Government retained the inflation target and the "
              "tolerance band for the next 5-year period – April 1, 2021 to March 31, 2026. In its second review, on March "
              "25, 2026", MPF),
         fact("Comments are invited on the questions raised in the Discussion Paper, from stakeholders and members of the "
              "public by September 18, 2025", DISC_MPF)])

p_jun, p_aug, p_oct, p_feb = 3.7, 3.1, 2.6, 2.1
assert round((p_jun - p_oct) * 100) == 110 and round((p_jun - p_feb) * 100) == 160
Q("008", T, "Inflation targeting", "Advanced",
  "The MPC's projection of average CPI inflation for 2025-26 was 3.7% in June 2025, 3.1% in August 2025, 2.6% in "
  "October 2025 and 2.1% in February 2026. Which statement is correct?",
  ["It was cut by 110 bps between June and October 2025, and by 160 bps in all by February 2026",
   "It was cut by 60 bps between June and October and by 110 bps by February",
   "It was raised in every review", "It fell by 160 bps between June and October 2025"],
  concept="Revisions of inflation projections",
  explanation="3.7 − 2.6 = 1.1 points (110 bps) by October 2025; 3.7 − 2.1 = 1.6 points (160 bps) by February 2026.",
  steps=["3.7 − 2.6 = 1.1", "3.7 − 2.1 = 1.6"],
  why="The other options misread the revisions; projections fell, not rose.",
  computed=True, current=ca("2026-02-06"),
  facts=[fact("The average headline inflation for 2025-26 is now revised lower from 3.7 per cent and 3.1 per cent projected "
              "in June and August policy, respectively, to 2.6 per cent", MPC_OCT25),
         fact("CPI inflation for 2025-26 is now projected at 2.1 per cent with Q4 at 3.2 per cent", MIN_FEB26)])

Q("009", T, "CPI and WPI", "Basic",
  "In MoSPI's CPI (base 2024=100), petrol, diesel and LPG prices are taken as of which reference date of each month?",
  ["The 15th of the month", "The 1st of the month", "The last day of the month", "The average of all days"],
  concept="Compilation of the CPI",
  explanation="MoSPI's release states that the reference period for petrol, diesel and LPG prices is the 15th of the "
              "corresponding month.",
  steps=["Fuel price reference → 15th"],
  why="The other dates are not the reference.",
  current=ca("2026-10-12"),
  facts=[fact("The reference period for price reporting for petrol, diesel and LPG prices are 15th of the corresponding "
              "month", CPI_SEP26)])
Q("009", T, "CPI and WPI", "Basic",
  "In the WPI (base 2022-23), the 'WPI Food Index' combines which components?",
  ["'Food Articles' from Primary Articles and 'Manufacture of Food Products' from Manufactured Products",
   "Only 'Food Articles' from Primary Articles", "Food Articles and Fuel and Power",
   "All items of the CPI food and beverages division"],
  concept="WPI Food Index",
  explanation="The WPI Food Index (weight 24.99%) consists of 'Food Articles' from the Primary Articles group and "
              "'Manufacture of Food Products' from the Manufactured Products group.",
  steps=["Food Articles + Manufactured Food Products"],
  why="It is not only primary food; fuel is excluded; it is a WPI, not CPI, index.",
  current=ca("2026-10-14"),
  facts=[fact("WPI Food Index (weight=24.99 per cent): The Food Index consists of 'Food Articles' from Primary Articles "
              "major group, and 'Manufacture of Food Products' from Manufactured Products major group", WPI_SEP26)])
Q("009", T, "CPI and WPI", "Basic",
  "According to the MPC's October 2025 resolution, what was headline CPI inflation in July 2025?",
  ["1.6%, an eight-year low", "2.1%, the highest of the year", "0.3%, an all-time low", "3.4%"],
  concept="Inflation trends in 2025",
  explanation="Headline CPI inflation fell to an eight-year low of 1.6% in July 2025 before rising to 2.1% in August.",
  steps=["July 2025: 1.6% (eight-year low)"],
  why="2.1% was August 2025; the other figures are not July 2025.",
  current=ca("2025-10-01"),
  facts=[fact("Headline CPI inflation declined to its eight-year low of 1.6 per cent (y-o-y) in July 2025 before rising to "
              "2.1 per cent in August", MPC_OCT25)])
Q("009", T, "CPI and WPI", "Intermediate",
  "According to the Governor's statement of 7 October 2026, core CPI inflation rose to 4.2% in August 2026. How had it "
  "behaved in the preceding months?",
  ["It had stayed unchanged at 3.9% for three consecutive months", "It had fallen steadily from 5%",
   "It had been negative", "It had risen every month since January"],
  concept="Core inflation",
  explanation="The Governor said core inflation increased to 4.2% in August 2026 after remaining unchanged at 3.9% for "
              "three consecutive months.",
  steps=["3.9% (3 months) → 4.2% (Aug 2026)"],
  why="The other patterns do not match.",
  current=ca("2026-10-07"),
  facts=[fact("Core inflation also increased to 4.2 per cent in August after remaining unchanged at 3.9 per cent for three "
              "consecutive months", GOV_OCT26)])

dec = {"q4_2526": 2.9, "q1": 3.9, "q2": 4.0}
feb = {"q4_2526": 3.2, "q1": 4.0, "q2": 4.2}
chg = {k: round((feb[k] - dec[k]) * 100) for k in dec}
assert chg == {"q4_2526": 30, "q1": 10, "q2": 20}
Q("009", T, "Inflation targeting", "Advanced",
  "In December 2025 the MPC projected CPI inflation at 2.9% for Q4:2025-26, 3.9% for Q1:2026-27 and 4.0% for Q2. In "
  "February 2026 it projected 3.2%, 4.0% and 4.2%. Which statement is correct?",
  ["All three were raised; the largest revision (30 bps) was for Q4:2025-26",
   "All three were cut; the largest revision was for Q2", "Only Q1 was raised, by 10 bps",
   "All three were raised by 20 bps each"],
  concept="Revisions of inflation projections",
  explanation="Q4:2025-26: +30 bps; Q1:2026-27: +10 bps; Q2: +20 bps. All were raised, most for Q4 (the MPC attributed "
              "the slight upward revision mainly to precious metals).",
  steps=["3.2 − 2.9 = 0.3", "4.0 − 3.9 = 0.1", "4.2 − 4.0 = 0.2"],
  why="The projections rose; revisions differed across quarters.",
  computed=True, current=ca("2026-02-06"),
  facts=[fact("CPI inflation for 2025-26 is now projected at 2.0 per cent with Q3 at 0.6 per cent; and Q4 at 2.9 per cent. "
              "CPI inflation for Q1:2026-27 and Q2 are projected at 3.9 per cent and 4.0 per cent", MPC_DEC25),
         fact("CPI inflation for 2025-26 is now projected at 2.1 per cent with Q4 at 3.2 per cent. CPI inflation for "
              "Q1:2026-27 and Q2 are projected at 4.0 per cent and 4.2 per cent", MIN_FEB26)])

Q("010", T, "CPI and WPI", "Basic",
  "Among the CPI (base 2024=100) divisions in September 2026, which recorded the LOWEST year-on-year inflation at the "
  "all-India combined level?",
  ["Health (1.40%)", "Recreation, sport and culture (2.16%)", "Information and communication (2.44%)",
   "Housing, water, electricity, gas and other fuels (2.74%)"],
  concept="Division-wise CPI inflation",
  explanation="MoSPI's annexure for September 2026 shows Health at 1.40%, the lowest; Recreation 2.16%, Information and "
              "communication 2.44%, Housing etc. 2.74%.",
  steps=["Lowest division → Health 1.40%"],
  why="The other divisions recorded higher inflation.",
  current=ca("2026-10-12"),
  facts=[fact("Health 1.40; Information and communication 2.44; Recreation, sport and culture 2.16; Housing, water, "
              "electricity, gas and other fuels 2.74 (combined, September 2026)", CPI_SEP26)])
Q("010", T, "Inflation targeting", "Intermediate",
  "In August 2026, when CPI inflation had moved above the 4% target, when did the MPC expect headline inflation to "
  "peak?",
  ["In Q3:2026-27, mainly due to food and fuel, before moderating", "In Q1:2026-27", "In Q1:2027-28",
   "It expected inflation to keep rising through 2027-28"],
  concept="Inflation outlook",
  explanation="The August 2026 resolution said headline inflation was expected to rise further in the near term and "
              "peak in Q3:2026-27, primarily due to food and fuel, before moderating.",
  steps=["Peak expected → Q3:2026-27"],
  why="The other periods are not what the MPC stated.",
  current=ca("2026-08-05"),
  facts=[fact("headline inflation is expected to rise further in the near term and peak in Q3:2026-27, primarily due to "
              "food and fuel, before moderating thereafter", MPC_AUG26)])
Q("010", T, "CPI and WPI", "Intermediate",
  "According to the December 2025 MPC resolution, what was core inflation excluding gold in October 2025, and how much "
  "did the rise in precious metal prices add to underlying inflation?",
  ["2.6%; about 50 basis points", "4.2%; about 100 basis points", "2.6%; about 60–70 basis points",
   "3.0%; about 36 basis points"],
  concept="Core inflation and precious metals",
  explanation="The December 2025 resolution said core inflation excluding gold moderated to 2.6% in October, and that "
              "the impact of the rise in precious metal prices was about 50 bps. (In February 2026 it put the effect on "
              "the outlook at 60–70 bps.)",
  steps=["Core ex-gold Oct 2025 = 2.6%", "Precious metals effect ≈ 50 bps"],
  why="60–70 bps was the February 2026 figure; the other pairs are not from this resolution.",
  current=ca("2025-12-05"),
  facts=[fact("Excluding gold, core inflation moderated to 2.6 per cent in October ... the impact of increase in price of "
              "precious metals is about 50 basis points (bps)", MPC_DEC25)])
Q("010", T, "CPI and WPI", "Intermediate",
  "The Governor's statement of 7 October 2026 cited sugar as one item behind broad-based food price pressures. What "
  "did it say about sugar prices?",
  ["They rose about 34% from early July to ₹64/kg by end-August, before retreating in September",
   "They fell 34% because of a bumper crop", "They doubled to ₹128/kg",
   "They were unchanged due to export restrictions"],
  concept="Food inflation drivers",
  explanation="Sugar prices rose about 34% from early July to ₹64/kg by end-August on a tight demand-supply balance and "
              "precautionary stocking; Government measures (export restrictions, stock limits, duty-free imports of 10 "
              "lakh tonnes of raw sugar) eased them, and prices retreated in September.",
  steps=["Sugar: +34% to ₹64/kg by end-Aug 2026"],
  why="Prices rose, not fell; they did not double; they were not unchanged.",
  current=ca("2026-10-07"),
  facts=[fact("Sugar prices rose by about 34 per cent from early July to ₹64/kg by end-August, due to tight demand-supply "
              "balance and precautionary stocking ... Prices have since retreated gradually in September", GOV_OCT26)])

w_aug, w_sep = 110.8, 112.5
mom = (w_sep / w_aug - 1) * 100
assert round(mom, 2) == 1.53
Q("010", T, "CPI and WPI", "Advanced",
  "The WPI (base 2022-23) for all commodities was 110.8 in August 2026 and 112.5 in September 2026, when year-on-year "
  "WPI inflation was 11.39% (9.92% in August). Which statement is correct?",
  ["The index rose about 1.5% month-on-month, and year-on-year inflation rose by about 1.5 percentage points",
   "The index rose 11.39% month-on-month", "The index fell month-on-month while year-on-year inflation rose",
   "The index rose about 1.7% month-on-month, and year-on-year inflation rose by 1.7 percentage points"],
  concept="Month-on-month vs year-on-year inflation",
  explanation="Month-on-month: 112.5 ÷ 110.8 − 1 ≈ 1.53%. Year-on-year inflation rose from 9.92% to 11.39%, i.e. 1.47 "
              "percentage points. The 11.39% compares September 2026 with September 2025, not with August.",
  steps=["112.5/110.8 − 1 ≈ 1.53%", "11.39 − 9.92 = 1.47 pp"],
  why="11.39% is the y-o-y rate; the index rose; 1.7 points is the index-point change, not a percentage.",
  computed=True, current=ca("2026-10-14"),
  facts=[fact("All India Wholesale Price Index (WPI) inflation for September 2026 is 11.39 per cent on year-on-year (YoY) "
              "basis, compared to 9.92 per cent in August 2026. The index for All Commodities for September 2026 stands "
              "at 112.5, whereas it was 110.8 in August 2026", WPI_SEP26)])


Q("010", "Repo Rate", "Repo and policy corridor", "Intermediate",
  "RBI provides a Standing Liquidity Facility to Standalone Primary Dealers at the prevailing repo rate. From 2 April "
  "2025, to what level did it raise the aggregate limit of this facility?",
  ["₹15,000 crore, from ₹10,000 crore", "₹10,000 crore, from ₹5,000 crore", "₹25,000 crore, from ₹15,000 crore",
   "₹50,000 crore, from ₹25,000 crore"],
  concept="Repo-rate linked facilities",
  explanation="Based on liquidity conditions, RBI raised the aggregate Standing Liquidity Facility limit for SPDs, "
              "available at the prevailing repo rate, from ₹10,000 crore to ₹15,000 crore from 2 April 2025; individual "
              "limits were conveyed separately.",
  steps=["SLF for SPDs (at repo): ₹10,000 → ₹15,000 crore"],
  why="The other figures are not the old or new limits.",
  current=ca("2025-04-02"),
  facts=[fact("increase the aggregate limit, made available to the Standalone Primary Dealers (SPDs) under the Standing "
              "Liquidity Facility at the prevailing repo rate, from ₹10,000 crore to ₹15,000 crore, starting from April "
              "02, 2025", SPD_SLF)])


# ============================================================================================ checks and output
def finish(b):
    spec = PKG["batches"][b]
    qs = QS[b]
    planned = {(t["topic"], d): n for t in spec["topics"] for d, n in t["quota"].items() if n}
    subtopics = {t["topic"]: set(t["subtopics"]) for t in spec["topics"]}
    have = Counter((q["topic"], q["difficulty"]) for q in qs)
    assert have == Counter(planned), (b, sorted(set(have.items()) ^ set(planned.items())))
    assert all(q["subtopic"] in subtopics[q["topic"]] for q in qs), b
    assert len(qs) == spec["count"]
    first = int(spec["question_ids"][0].split("_")[-1])
    out_q = []
    for i, q in enumerate(qs):
        qid = f"BANK_BFA_{first + i:06d}"
        facts, current, computed = q.pop("_facts"), q.pop("_current"), q.pop("_computed")
        urls = {f["source_url"] for f in facts}
        web = (["web:fact-check"] if urls - SEARCH_ONLY else []) + (["web:search-confirmed"] if urls & SEARCH_ONLY else [])
        rec = {"question_id": qid, **q}
        if current:
            assert current["event_date"] <= CHECKED, (qid, current)
            rec = {k: v for k, v in rec.items() if k not in ("source", "verification")}
            rec["current_affairs"] = current
        if q["topic"] == "Repo Rate":
            assert current, qid
        rec["source"] = {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                         "original_exam_year": None, "license_note": None}
        rec["verification"] = {"answer_verified": True, "solution_verified": True,
                               "review_status": "Pending Human Review",
                               "verified_by": ["ai:author-solve", *web] + (["script:recompute"] if computed else [])
                               + (["ai:independent-check"] if qid in INDEPENDENT else []),
                               "verified_at": TODAY, "fact_checks": facts}
        out_q.append(rec)
    assert out_q[0]["question_id"] == spec["question_ids"][0] and out_q[-1]["question_id"] == spec["question_ids"][1]
    assert len({q["question_text"] for q in out_q}) == len(out_q)
    k = _keys[b]
    assert max(k.values()) - min(k.values()) <= 3, (b, k)
    notes = (f"{spec['batch_id']} Banking and Financial Awareness, topic package 1 (Banking Fundamentals, History of "
             f"Banking in India, Reserve Bank of India, RBI Functions, Monetary Policy, Repo Rate, Reverse Repo Rate, CRR, "
             f"SLR, Bank Rate, Inflation): {len(out_q)} original questions, IDs {spec['question_ids'][0]} to "
             f"{spec['question_ids'][1]}. Built from RBI pages opened on 2026-11-06 (consolidated Commercial Banks "
             f"Directions of 28 Nov 2025 on deposits, advances and voluntary amalgamation, the Miscellaneous Directions' "
             f"DEA Fund chapter, the liquidity management framework of 30 Sep 2025, MPC resolutions Feb 2025-Oct 2026, "
             f"RBI press releases and auction results, FAQs on currency, cheque clearing and Government banking, RBI's "
             f"history chronology, Governors' profiles and Bank Rate/CRR/SLR table) and MoSPI/DPIIT price releases. Only "
             f"current rules are tested; older rules appear only as explicit history. Computed answers are re-derived "
             f"with asserts in tools/packages/BFA_pkg1.py. ai:independent-check marks only questions a separate fresh "
             f"solver answered blind and matched with confidence.")
    doc = {"schema_version": "1.0", "batch_id": spec["batch_id"], "created_at": TODAY, "notes": notes,
           "stimuli": [], "questions": out_q}
    out = ROOT / spec["output"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out.name}: {len(out_q)} questions; keys {dict(sorted(k.items()))}; "
          f"current_affairs {sum('current_affairs' in q for q in out_q)}; "
          f"independent {sum(q['question_id'] in INDEPENDENT for q in out_q)}")


for _b in BATCHES:
    finish(_b)
