"""Writes batches/parts/BATCH_003_BFA.json: the 200 Banking and Financial Awareness questions of BATCH_003.

Every fact is backed by at least one fact_check whose source was opened on 2026-11-05 (fetched with a plain client and
read), or, where the official page could not be fetched (NPCI and PIB return 403; no workaround was attempted),
confirmed through web search results (those questions carry web:search-confirmed). Values that can change carry
current_affairs dates taken from the source. Every computable answer is re-derived below with assertions, the quota
per (topic, difficulty) is checked against the batch plan, and the answer keys are balanced. If any check fails,
nothing is written. Facts tested in BATCH_000, BATCH_001 and BATCH_002 were read first and are not repeated.

    python tools/batch_003/banking.py      (run from anywhere)
"""

import datetime as dt
import json
import random
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-05"
REVIEW_BY = "2027-05-05"
LETTERS = "ABCD"
BF = "Banking and Financial Awareness"
FIRST_ID = 404
SECONDS = {"Basic": 20, "Intermediate": 30, "Advanced": 60}

_rng = random.Random(2026110503)
_keys = Counter()
questions = []

# ---------------------------------------------------------------- sources
# Opened (fetched and read) on 2026-11-05
CHRON_26 = "https://rbi.org.in/history/Brief_Chro1926to1935.html"
CHRON_35 = "https://rbi.org.in/history/Brief_Chro1935to1949.html"
CHRON_50 = "https://rbi.org.in/history/Brief_Chro1950to1960.html"
CHRON_60 = "https://rbi.org.in/history/Brief_Chro1960to1971.html"
CHRON_85 = "https://rbi.org.in/history/Brief_Chro1985to1991.html"
CHRON_91 = "https://rbi.org.in/history/Brief_Chro1991to2000.html"
CHRON_00 = "https://rbi.org.in/history/Brief_Chro2000_Onwards.html"
ORG = "https://www.rbi.org.in/commonman/english/Scripts/Organisation.aspx"
CURRENCY_FAQ = "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=3158"
GOVT_BANKER = "https://www.rbi.org.in/scripts/FS_Overview.aspx?fn=2758"
MP_OVERVIEW = "https://www.rbi.org.in/scripts/FS_Overview.aspx?fn=2752"
MPC_OCT26 = "https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=63742"
MIN_OCT26 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63839"
SDRP_OCT26 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63743"
MPC_AUG26 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63287"
SDRP_AUG26 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63289"
MPC_JUN26 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=62863"
MPC_APR26 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=62514"
SDRP_APR26 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=62516"
MPC_SCHED = "https://www.rbi.org.in/Scripts/AnnualPolicy.aspx"
EBLR = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11677&Mode=0"
SDF_PR = "https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=53539"
MSF_2011 = "https://rbi.org.in/scripts/NotificationUser.aspx?Id=6394&Mode=0"
CRR_CUT = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12858&Mode=0"
DICGC_FAQ = "https://www.dicgc.org.in/FAQs"
NRI_FAQ = "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=3"
RRB_DFS = "https://financialservices.gov.in/regional-rural-banks-0"
NABARD = "https://www.nabard.org/ftrcontent.aspx?id=492"
PAY_BOOKLET = "https://www.rbi.org.in/scripts/PublicationsView.aspx?Id=20315"
PSR_MAY26 = "https://www.rbi.org.in/Scripts/PublicationsView.aspx?id=23813"
RTGS_FAQ = "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=275"
NEFT_FAQ = "https://rbi.org.in/Scripts/faqview.aspx?Id=60"
LEI_FAQ = "https://www.rbi.org.in/Scripts/FAQView.aspx?Id=140"
CTS_CC = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12891"
IRAC_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13146"
IBBI_FAQ = "https://ibbi.gov.in/uploads/faqs/CIRPFAQs%20Final2408.pdf"
BCBS_HIST = "https://www.bis.org/bcbs/history.htm"
LEV_GSIB = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13743&Mode=0"
OPRISK = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13744&Mode=0"
PMJDY_DFS = "https://financialservices.gov.in/index.php/pradhan-mantri-jan-dhan-yojana-pmjdy"
DELHI_LB = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13746&Mode=0"
NSFI = "https://www.rbi.org.in/commonman/Upload/English/Content/PDFs/English12052026.pdf"
PSL_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12799"
RBIOS_FAQ = "https://www.rbi.org.in/commonperson/english/scripts/FAQs.aspx?Id=3407"
ERUPEE_FAQ = "https://www.rbi.org.in/commonman/English/scripts/FAQs.aspx?Id=3686"
DL_2025 = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12848"
DBC_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13163"
PB_GUIDE = "https://www.rbi.org.in/scripts/bs_viewcontent.aspx?Id=2900"
PB_MISC = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13087"
SFB_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13135"
FX_RM = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13737&Mode=0"
FERR = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13738&Mode=0"
SEBI_ABOUT = "https://www.sebi.gov.in/about-sebi.html"
IRDAI = "https://irdai.gov.in/what-we-do"
LIC_HIST = "https://www.licindia.in/history"
DFS_PSI = "https://financialservices.gov.in/public-sector-insurers"
PMJJBY = "https://financialservices.gov.in/pradhan-mantri-jeevan-jyoti-bima-yojana-pmjjby"
PMSBY = "https://financialservices.gov.in/pradhan-mantri-suraksha-bima-yojana-pmsby"
MF_CAT = "https://www.amfiindia.com/Themes/Theme1/downloads/1507291273374.pdf"
BUDGET = "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc202621776101.pdf"
APY_FAQ = "https://www.pfrda.org.in/w/faqs/atal-pension-yojana"
CGFMU_FAQ = "https://www.ncgtc.in/content/products/0/20250218/FAQ_updated_18_Feb_2025_3e257c4981.pdf"

# Confirmed only through search results (official page not fetchable, or only news coverage found)
MERGER_BS = ("https://www.business-standard.com/amp/article/pti-stories/union-bank-becomes-5th-largest-psb-post-"
             "merger-with-andhra-bank-corporation-bank-120040101387_1.html")
CTS_DEFER = ("https://www.business-standard.com/finance/news/implementation-of-cheque-clearing-phase-2-postponed-"
             "until-further-notice-rbi-125122401018_1.html")
MPC_FEB26 = ("https://www.business-standard.com/finance/news/rbi-mpc-meet-what-stayed-the-same-what-changed-in-"
             "february-policy-review-126020600625_1.html")
ES_POT = "https://www.taxmann.com/post/blog/economic-survey-indias-potential-growth-raised-to-7/"
ES_GDP = ("https://www.businesstoday.in/amp/union-budget/story/economic-survey-tabled-in-lok-sabha-fy27-growth-seen-"
          "at-68-72-ahead-of-budget-513403-2026-01-29")
AMFI_SIP = "https://www.amfiindia.com/articles/mutual-fund"
SEARCH_ONLY = {MERGER_BS, CTS_DEFER, MPC_FEB26, ES_POT, ES_GDP, AMFI_SIP}


def fact(claim, url):
    return {"claim": claim, "source_url": url, "checked_on": TODAY}


AUDIT_DAY = "2026-11-06"  # superseded-rules audit of 2026-11-06
SDF_TIME = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=60740"


def fact6(claim, url):
    return {"claim": claim, "source_url": url, "checked_on": AUDIT_DAY}


def ca(event_date, review_by=REVIEW_BY):
    return {"event_date": event_date, "review_by": review_by}


def Q(topic, subtopic, difficulty, text, options, answer=None, *, concept, explanation, steps, facts, why,
      seconds=None, computed=False, current=None, shortcut=None):
    """Adds one question. With answer=None, options[0] is the correct text and it is placed at the least-used key
    so far (random tie-break, fixed seed)."""
    assert len(options) == 4 and len(set(options)) == 4, text
    assert facts and why, text
    if answer is None:
        low = min(_keys[k] for k in LETTERS)
        pos = LETTERS.index(_rng.choice([k for k in LETTERS if _keys[k] == low]))
        correct, wrongs = options[0], list(options[1:])
        options = wrongs[:pos] + [correct] + wrongs[pos:]
        answer = LETTERS[pos]
    assert answer in LETTERS
    _keys[answer] += 1
    urls = {f["source_url"] for f in facts}
    web = (["web:fact-check"] if urls - SEARCH_ONLY else []) + (["web:search-confirmed"] if urls & SEARCH_ONLY else [])
    out = {
        "question_id": f"BANK_BFA_{FIRST_ID + len(questions):06d}",
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
    }
    if current:
        out["current_affairs"] = current
    out["source"] = {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                     "original_exam_year": None, "license_note": None}
    out["verification"] = {"answer_verified": True, "solution_verified": True, "review_status": "Pending Human Review",
                           "verified_by": ["ai:author-solve", *web] + (["script:recompute"] if computed else []),
                           "verified_at": TODAY, "fact_checks": facts}
    questions.append(out)


def capped(x, cap=5.0):
    return min(x, cap)


# ================================================================= 1. Banking Fundamentals (3 / 5 / 4)
T = "Banking Fundamentals"
Q(T, "Types of banks", "Basic",
  "Deposits in which of the following are NOT insured by the Deposit Insurance and Credit Guarantee Corporation "
  "(DICGC)?",
  ["Primary co-operative societies", "Regional Rural Banks", "Branches of foreign banks functioning in India",
   "Local Area Banks"],
  concept="Coverage of deposit insurance",
  explanation="DICGC insures all commercial banks (including branches of foreign banks in India), local area banks "
              "and regional rural banks, and eligible co-operative banks. Primary co-operative societies are not "
              "insured by DICGC.",
  steps=["Commercial banks, foreign bank branches, LABs, RRBs → insured", "Primary co-operative societies → not insured"],
  why="RRBs, foreign bank branches in India and local area banks are all expressly covered by DICGC.",
  facts=[fact("All commercial banks including branches of foreign banks functioning in India, local area banks and "
              "regional rural banks are insured by the DICGC; primary cooperative societies are not insured",
              DICGC_FAQ)])
Q(T, "Cheques and instruments", "Basic",
  "Magnetic Ink Character Recognition (MICR) technology, as part of efforts to mechanise cheque clearing, was "
  "introduced in India in:",
  ["March 1987", "January 1952", "December 2013", "July 2014"],
  concept="Evolution of cheque clearing",
  explanation="RBI's chronology records that MICR technology was introduced for cheque clearing in March 1987. MICR "
              "clearing was later discontinued from July 2014, when all MICR centres were subsumed into grid-based "
              "Cheque Truncation System clearing.",
  steps=["MICR introduced: March 1987", "MICR clearing discontinued: July 2014 (moved to CTS)"],
  why="January 1952 is the Bill Market Scheme; December 2013 is when NPCI began operating CTS; July 2014 is when "
      "MICR clearing ended.",
  facts=[fact("Mar 1987: Magnetic Ink Character Recognition (MICR) technology introduced for cheque clearing",
              CHRON_85),
         fact("MICR clearing was discontinued with effect from July 2014", PAY_BOOKLET)])
Q(T, "Types of banks", "Basic",
  "Regional Rural Banks in India began in 1975 with how many banks, the first being set up on 2 October 1975 under an "
  "Ordinance?",
  ["5", "14", "28", "43"],
  concept="Origin of RRBs",
  explanation="According to the Department of Financial Services, the RRB system started with 5 RRBs in 1975; the "
              "first RRB was set up on 2 October 1975 under an Ordinance, later replaced by the Regional Rural Banks "
              "Act, 1976. RRBs were created as an alternative channel to the co-operative credit structure.",
  steps=["1975: 5 RRBs", "First RRB: 2 October 1975 (Ordinance)", "Statute: RRBs Act, 1976"],
  why="14 is the number of banks nationalised in 1969; 28 is the present number of RRBs; 43 was the number before "
      "the 2025 amalgamation.",
  facts=[fact("It started with 5 RRBs in the year 1975, first RRB was setup on 02nd October, 1975 under the "
              "provisions of the Ordinance", RRB_DFS)])
Q(T, "Types of accounts", "Intermediate",
  "Which of the following deposits is NOT covered by DICGC deposit insurance?",
  ["Deposits of a State Government", "A recurring deposit of an individual",
   "A current account of a partnership firm", "A fixed deposit of a trust"],
  concept="Deposits excluded from insurance",
  explanation="DICGC insures savings, fixed, current, recurring and other deposits, but excludes deposits of foreign "
              "Governments, deposits of the Central and State Governments, inter-bank deposits, deposits received "
              "outside India and amounts specifically exempted with RBI's approval.",
  steps=["Excluded: foreign/Central/State Government deposits, inter-bank deposits, deposits received outside India",
         "A State Government deposit → excluded"],
  why="Recurring deposits of individuals, current accounts of firms and fixed deposits of trusts are ordinary "
      "insured deposits.",
  facts=[fact("DICGC insures all deposits except deposits of foreign Governments, deposits of Central/State "
              "Governments, inter-bank deposits and deposits received outside India", DICGC_FAQ)])
Q(T, "Types of accounts", "Intermediate",
  "A Foreign Currency (Non-Resident) Account (Banks) [FCNR(B)] can be opened only as which type of account, and for "
  "what period?",
  ["Term deposit only, for not less than 1 year and not more than 5 years",
   "Savings or current account, without any fixed period", "Term deposit only, for 1 to 3 years",
   "Recurring deposit only, for up to 10 years"],
  concept="FCNR(B) deposits",
  explanation="RBI's FAQs on NRI accounts state that FCNR(B) accounts are held in a freely convertible foreign "
              "currency and only as term deposits, for terms of not less than 1 year and not more than 5 years. NRE "
              "fixed deposits are generally for one to three years.",
  steps=["FCNR(B): foreign currency, term deposit only", "Tenor: 1 to 5 years"],
  why="Savings/current options apply to NRE and NRO accounts; 1–3 years is the NRE fixed deposit period; recurring "
      "deposits are not the FCNR(B) form.",
  facts=[fact("FCNR(B): Term Deposit only; for terms not less than 1 year and not more than 5 years; NRE fixed "
              "deposits from one to three years", NRI_FAQ)])
Q(T, "Types of banks", "Intermediate",
  "If an insured bank goes into liquidation, within what time must DICGC pay the claim amount of each depositor (up "
  "to ₹5 lakh), and to whom?",
  ["Within two months of receiving the claim list, to the liquidator",
   "Within 90 days of the bank's closure, directly to each depositor", "Within six months, to RBI",
   "Within one month, to the transferee bank"],
  concept="Payment of deposit insurance claims",
  explanation="DICGC is liable to pay the liquidator the claim amount of each depositor up to ₹5 lakh within two "
              "months from the date of receipt of the claim list from the liquidator. DICGC does not deal directly "
              "with depositors; the liquidator disburses the amounts.",
  steps=["Liquidator prepares depositor-wise claim list", "DICGC pays the liquidator within two months",
         "Liquidator pays depositors"],
  why="DICGC pays through the liquidator, not directly; RBI is not the payee; payment to a transferee bank applies to "
      "amalgamation cases.",
  facts=[fact("If a bank goes into liquidation, DICGC is liable to pay to the liquidator the claim amount of each "
              "depositor up to Rupees five lakhs within two months from the date of receipt of claim list; DICGC "
              "does not directly deal with the depositors", DICGC_FAQ)])
Q(T, "Cheques and instruments", "Intermediate",
  "Phase 2 of continuous clearing and settlement on realisation in the Cheque Truncation System, which would have cut "
  "the item expiry time to T+3 clear hours, was scheduled for 3 January 2026. What did RBI decide in December 2025?",
  ["Phase 2 was deferred until further notice, with Phase 1 continuing",
   "Phase 2 was implemented on 3 January 2026 as planned", "Phase 1 was withdrawn and batch clearing restored",
   "Phase 2 was advanced to 1 December 2025"],
  concept="Cheque clearing reforms",
  explanation="RBI's August 2025 circular moved CTS to continuous clearing in two phases: Phase 1 from 4 October 2025 "
              "and Phase 2 from 3 January 2026 (item expiry time of T+3 clear hours). In December 2025 RBI postponed "
              "Phase 2 until further notice, while Phase 1 continues to operate.",
  steps=["Phase 1: 4 October 2025 (continuing)", "Phase 2 (T+3 clear hours): deferred until further notice"],
  why="Phase 2 did not go live on 3 January 2026; Phase 1 was not withdrawn; it was not advanced.",
  current=ca("2025-12-24"),
  facts=[fact("Phase 1 on October 4, 2025 and Phase 2 on January 3, 2026; in Phase 2 the item expiry time changes to "
              "T+3 clear hours", CTS_CC),
         fact("Implementation of cheque clearing Phase 2 postponed until further notice (December 24, 2025)",
              CTS_DEFER)])
Q(T, "Types of banks", "Intermediate",
  "DICGC may cancel the registration of an insured bank if it fails to pay the deposit insurance premium for:",
  ["Three consecutive periods", "One period", "Two consecutive years", "Five consecutive periods"],
  concept="Compulsory deposit insurance",
  explanation="Deposit insurance is compulsory and no bank can withdraw from it. DICGC may cancel an insured bank's "
              "registration if it fails to pay the premium for three consecutive periods, and the public is "
              "informed through newspapers. Deposits remain covered up to the date of cancellation.",
  steps=["Premium default for three consecutive periods → registration may be cancelled"],
  why="One period, two years and five periods are not the trigger stated by DICGC.",
  facts=[fact("The Corporation may cancel the registration of an insured bank if it fails to pay the premium for "
              "three consecutive periods; no bank can withdraw from the deposit insurance scheme", DICGC_FAQ)])

joint = {("A", "B"): [3.0, 2.5], ("B", "A"): [4.0]}
insured = sum(capped(sum(v)) for v in joint.values())
assert insured == 9.0
Q(T, "Types of accounts", "Advanced",
  "Anil and Bina hold three joint deposit accounts in the same bank: two in the order 'Anil, Bina' with ₹3 lakh and "
  "₹2.5 lakh, and one in the order 'Bina, Anil' with ₹4 lakh (all amounts include interest). If the bank goes into "
  "liquidation, what is the total insured amount for these accounts?",
  ["₹9 lakh", "₹5 lakh", "₹9.5 lakh", "₹10 lakh"],
  concept="Same right and same capacity for joint accounts",
  explanation="Joint accounts in which the names appear in the same order are treated as held in the same right and "
              "capacity, so they are aggregated: ₹3 lakh + ₹2.5 lakh = ₹5.5 lakh, insured up to ₹5 lakh. The account "
              "with the names in a different order is a different capacity and is separately insured: ₹4 lakh. "
              "Total insured = ₹9 lakh.",
  steps=["Order 'Anil, Bina': 3 + 2.5 = 5.5 → capped at 5", "Order 'Bina, Anil': 4 → fully insured", "Total = 9"],
  why="₹5 lakh treats all three as one capacity; ₹9.5 lakh ignores the cap; ₹10 lakh gives ₹5 lakh to each order.",
  computed=True,
  facts=[fact("Joint accounts with names in the same order are aggregated; if names are not in the same order, cover "
              "is available separately up to Rupees Five Lakhs", DICGC_FAQ)])

dep, dues = 6.0, 1.5
assert capped(dep - dues) == 4.5
Q(T, "Types of accounts", "Advanced",
  "Kiran has deposits of ₹6 lakh (principal and interest) in his own name in a bank that goes into liquidation. He "
  "also owes the same bank ₹1.5 lakh on a loan, which the bank sets off. What deposit insurance amount is payable for "
  "him?",
  ["₹4.5 lakh", "₹5 lakh", "₹3.5 lakh", "₹6 lakh"],
  concept="Set-off before deposit insurance",
  explanation="Banks have the right to set off their dues from deposits as on the cut-off date, and deposit insurance "
              "applies after netting. Net deposit = ₹6 lakh − ₹1.5 lakh = ₹4.5 lakh, which is within the ₹5 lakh "
              "limit, so ₹4.5 lakh is insured.",
  steps=["Net deposit = 6 − 1.5 = 4.5", "4.5 ≤ 5 → insured 4.5"],
  shortcut="Net first, then cap at ₹5 lakh.",
  why="₹5 lakh ignores the set-off; ₹3.5 lakh deducts the dues from the cap instead of the deposit; ₹6 lakh ignores "
      "both the set-off and the cap.",
  computed=True,
  facts=[fact("Banks have the right to set off their dues from the amount of deposits as on cut off date; deposit "
              "insurance is available after netting of such dues", DICGC_FAQ)])

prop = {"individual+proprietary": [2.0, 1.5, 2.5], "firm (partner)": [4.0]}
assert sum(capped(sum(v)) for v in prop.values()) == 9.0
Q(T, "Types of accounts", "Advanced",
  "In one bank, Suresh has a savings account of ₹2 lakh and a fixed deposit of ₹1.5 lakh in his own name, a current "
  "account of ₹2.5 lakh in the name of his sole proprietorship, and a ₹4 lakh deposit of a partnership firm in which "
  "he is a partner. If the bank is liquidated, what is the total insured amount for these deposits?",
  ["₹9 lakh", "₹10 lakh", "₹5 lakh", "₹10.5 lakh"],
  concept="Proprietary versus partnership capacity",
  explanation="Deposits of a sole proprietary concern are aggregated with the proprietor's individual deposits: 2 + "
              "1.5 + 2.5 = ₹6 lakh → insured ₹5 lakh. Deposits held as a partner of a firm are in a different "
              "capacity and are separately insured: ₹4 lakh. Total = ₹9 lakh.",
  steps=["Individual + proprietorship = 6 → capped at 5", "Firm (different capacity) = 4", "Total = 9"],
  why="₹10 lakh treats the proprietorship separately; ₹5 lakh aggregates the firm's deposit too; ₹10.5 lakh ignores "
      "the cap.",
  computed=True,
  facts=[fact("Deposit held in the name of a proprietary concern where the depositor is the sole proprietor and his "
              "individual deposits are aggregated; deposits as partner of a firm are a different capacity and are "
              "separately covered", DICGC_FAQ)])
Q(T, "Types of accounts", "Advanced",
  "Consider the following statements about non-resident accounts as described in RBI's FAQs:\nI. An NRE account may "
  "be held jointly with a resident relative on a 'former or survivor' basis, and the resident relative can operate "
  "it as a Power of Attorney holder during the NRI's lifetime.\nII. Current income such as rent, dividend and pension "
  "is a permissible credit to an NRE account.\nIII. An FCNR(B) account can be maintained as a savings account in any "
  "freely convertible currency.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="NRE and FCNR(B) features",
  explanation="Statement I is correct: NRIs/PIOs may hold an NRE account jointly with a resident relative on a "
              "former-or-survivor basis, with the resident operating it as a Power of Attorney holder. Statement II "
              "is correct: RBI's FAQ states that current income like rent, dividend, pension and interest will be "
              "construed as a permissible credit to the NRE account. Statement III is wrong: an FCNR(B) account can "
              "only be a term deposit.",
  steps=["I: correct", "II: correct (current income is a permissible NRE credit)", "III: wrong (term deposit only)"],
  why="Option with III is wrong because FCNR(B) cannot be a savings account; 'I only' omits the correct II.",
  facts=[fact("NRE: NRIs/PIOs can hold jointly with a resident relative on 'former or survivor' basis; the resident "
              "relative can operate the account as a Power of Attorney holder; current income like rent, dividend, "
              "pension, interest will be construed as a permissible credit to the NRE account; FCNR(B): term "
              "deposit only", NRI_FAQ)])

# ================================================================= 2. History of Banking in India (3 / 2 / 2)
T = "History of Banking in India"
Q(T, "Nationalisation", "Basic",
  "According to RBI's chronology, the failure of which banks in 1960 catalysed the introduction of deposit insurance "
  "in India?",
  ["Laxmi Bank and Palai Central Bank", "Travancore National and Quilon Bank and Imperial Bank",
   "Global Trust Bank and Bank of Karad", "Bank of Bengal and Bank of Madras"],
  concept="Origin of deposit insurance",
  explanation="RBI records that the failure of Laxmi Bank in May 1960 and the subsequent failure of the Palai Central "
              "Bank catalysed the introduction of deposit insurance. Deposit insurance was introduced on 7 December "
              "1961 as a depositor protection measure.",
  steps=["1960: Laxmi Bank and Palai Central Bank fail", "7 Dec 1961: deposit insurance introduced"],
  why="The Travancore National and Quilon Bank failed in 1938 and led to calls for banking legislation; the other "
      "pairs are unrelated to the 1961 scheme.",
  facts=[fact("May 1960: The failure of Laxmi Bank and the subsequent failure of the Palai Central Bank catalyzed the "
              "introduction of deposit insurance in India; 7 Dec 1961: Deposit Insurance introduced", CHRON_60)])
Q(T, "Committees", "Basic",
  "The report of which committee, submitted in August 1954, brought rural credit to the centre stage and led to the "
  "formation of the State Bank of India?",
  ["All-India Rural Credit Survey Committee", "Hilton Young Commission", "Tandon Committee",
   "Indian Central Banking Enquiry Committee"],
  concept="Rural credit and SBI",
  explanation="The All-India Rural Credit Survey Committee submitted its report in August 1954. Its recommendations "
              "brought rural credit to the centre of central bank activism and led to the conversion of the "
              "Imperial Bank of India into the State Bank of India on 1 July 1955.",
  steps=["Aug 1954: AIRCS Committee report", "1 July 1955: SBI formed"],
  why="The Hilton Young Commission (1926) recommended a central bank; the Tandon Committee (1975) dealt with working "
      "capital; the Central Banking Enquiry Committee (1931) revived the idea of RBI.",
  facts=[fact("Aug 1954: All-India Rural Credit Survey Committee Report submitted... Led to the formation of the State "
              "Bank of India", CHRON_50)])
Q(T, "Mergers and consolidation", "Basic",
  "In the public sector bank consolidation effective 1 April 2020, Andhra Bank and Corporation Bank were amalgamated "
  "into:",
  ["Union Bank of India", "Canara Bank", "Punjab National Bank", "Bank of Baroda"],
  concept="PSB consolidation, 2020",
  explanation="Andhra Bank and Corporation Bank were amalgamated into Union Bank of India with effect from 1 April "
              "2020, making Union Bank of India the fifth largest public sector bank at the time.",
  steps=["Andhra Bank + Corporation Bank → Union Bank of India (1 April 2020)"],
  why="Syndicate Bank merged into Canara Bank, OBC and United Bank into PNB, and Bank of Baroda's merger (Vijaya and "
      "Dena) was in 2019.",
  facts=[fact("Union Bank becomes 5th largest PSB post merger with Andhra Bank, Corporation Bank (April 1, 2020)",
              MERGER_BS)])
Q(T, "Mergers and consolidation", "Intermediate",
  "According to RBI's chronology, in which year were guidelines for the establishment of new private sector banks "
  "issued, heralding a policy aimed at fostering greater competition?",
  ["1993", "1969", "1980", "2001"],
  concept="Entry of new private banks",
  explanation="In 1993, guidelines for the establishment of private sector banks were issued, a new policy approach "
              "aimed at fostering greater competition after the 1991 reforms. In July 1994 nationalised banks were "
              "allowed to tap the capital market.",
  steps=["1993: private sector bank guidelines", "1994: nationalised banks allowed to raise capital from the market"],
  why="1969 and 1980 are nationalisation years; 2001 is not the year of the first private bank guidelines.",
  facts=[fact("1993: Guidelines for the establishment of private sector banks issued. This heralds a new policy "
              "approach aimed at fostering greater competition", CHRON_91)])
Q(T, "Committees", "Intermediate",
  "The committee set up on 10 April 1985 to review the working of the monetary system, whose recommendations had "
  "far-reaching consequences, was chaired by:",
  ["S. Chakravarty", "M. Narasimham", "R. N. Malhotra", "P. J. Nayak"],
  concept="Review of the monetary system",
  explanation="RBI's chronology records that the S. Chakravarty Committee was set up on 10 April 1985 to review the "
              "working of the monetary system and that its recommendations had far-reaching consequences.",
  steps=["1985 + working of the monetary system → S. Chakravarty Committee"],
  why="Narasimham chaired the 1991 financial sector committee; R. N. Malhotra the 1994 insurance reform committee; "
      "P. J. Nayak the 2014 committee on bank boards.",
  facts=[fact("10 Apr 1985: S. Chakravarty Committee was set up to review the working of monetary system. Its "
              "recommendations had far reaching consequences", CHRON_85)])
Q(T, "Nationalisation", "Advanced",
  "Arrange the following in chronological order:\nI. Selective credit controls deployed for the first time\nII. "
  "Introduction of the Bill Market Scheme\nIII. Hali Sicca rupees ceasing to be legal tender in the erstwhile "
  "Hyderabad State\nIV. Conversion of the Imperial Bank of India into the State Bank of India",
  ["II, III, IV, I", "II, IV, III, I", "III, II, I, IV", "II, I, III, IV"],
  concept="RBI in the 1950s",
  explanation="Bill Market Scheme: 1 January 1952. Hali Sicca rupees ceased to be legal tender: 1 April 1955. SBI "
              "formed: 1 July 1955. Selective credit controls first used: 17 May 1956. Order: II, III, IV, I.",
  steps=["II: Jan 1952", "III: Apr 1955", "IV: Jul 1955", "I: May 1956"],
  why="The other orders misplace the April 1955 currency change or put selective credit controls (1956) too early.",
  facts=[fact("1 Jan 1952: Bill Market Scheme introduced; 1 Apr 1955: Hali Sicca Rupees ceased to be legal tender; 1 "
              "Jul 1955: Imperial Bank converted to SBI; 17 May 1956: Selective Credit Controls deployed for first "
              "time", CHRON_50)])
Q(T, "Committees", "Advanced",
  "Arrange the following in chronological order:\nI. Office of the Banking Ombudsman established\nII. Interim "
  "Liquidity Adjustment Facility introduced\nIII. Maximum lending rate abolished, leaving banks free to price loans "
  "by credit record\nIV. RBI website made operational",
  ["III, I, IV, II", "I, III, IV, II", "III, IV, I, II", "III, I, II, IV"],
  concept="Reforms of 1985–2000",
  explanation="Maximum lending rate abolished: October 1988. Banking Ombudsman office: June 1995. RBI website "
              "operational: 17 September 1996. Interim LAF: 20 April 1999. Order: III, I, IV, II.",
  steps=["III: Oct 1988", "I: Jun 1995", "IV: Sep 1996", "II: Apr 1999"],
  why="The other orders place the 1995 Ombudsman office, the 1996 website or the 1999 interim LAF out of sequence.",
  facts=[fact("Oct 1988: Maximum lending rate abolished", CHRON_85),
         fact("Jun 1995: Office of the Banking Ombudsman established; 17 Sep 1996: RBI Web site made operational; 20 "
              "Apr 1999: Interim Liquidity Adjustment Facility introduced", CHRON_91)])

# ================================================================= 3. Reserve Bank of India (3 / 3 / 3)
T = "Reserve Bank of India"
Q(T, "Establishment and structure", "Basic",
  "Which body recommended in 1926 the establishment of a central bank to be called the 'Reserve Bank of India'?",
  ["Royal Commission on Indian Currency (Hilton Young Commission)", "Indian Central Banking Enquiry Committee",
   "All-India Rural Credit Survey Committee", "Banking Commission"],
  concept="Origin of RBI",
  explanation="In 1926 the Royal Commission on Indian Currency, known as the Hilton Young Commission, recommended a "
              "central bank called the Reserve Bank of India. The Indian Central Banking Enquiry Committee revived "
              "the issue in 1931, and the RBI Act was passed in 1934.",
  steps=["1926: Hilton Young Commission", "1931: revived by Central Banking Enquiry Committee", "1934: RBI Act"],
  why="The Central Banking Enquiry Committee came in 1931; the AIRCS Committee (1954) led to SBI; the Banking "
      "Commission was set up much later.",
  facts=[fact("1926: Royal Commission on Indian Currency (Hilton Young Commission) recommends the establishment of a "
              "central bank to be called the 'Reserve Bank of India'", CHRON_26)])
Q(T, "Governors and leadership", "Basic",
  "Who was the first Governor of the Reserve Bank of India when it commenced operations on 1 April 1935?",
  ["Sir Osborne Smith", "Sir James Braid Taylor", "Sir C. D. Deshmukh", "Sir Benegal Rama Rau"],
  concept="RBI's first Governor",
  explanation="RBI commenced operations on 1 April 1935 as a shareholders' bank with Sir Osborne Smith as its first "
              "Governor. He resigned with effect from 1 July 1937, when Sir James Braid Taylor took over.",
  steps=["1 Apr 1935: Osborne Smith", "1 Jul 1937: James Braid Taylor"],
  why="Taylor was the second Governor; Deshmukh took office in 1943 and Rama Rau in 1949.",
  facts=[fact("1 Apr 1935: Reserve Bank of India commences operations. Sir Osborne Smith the first Governor of the "
              "Bank", CHRON_35)])
Q(T, "Establishment and structure", "Basic",
  "The first Reserve Bank of India banknotes were issued in:",
  ["January 1938", "April 1935", "January 1949", "July 1955"],
  concept="RBI's note issue",
  explanation="RBI's chronology records that the first Reserve Bank notes were issued in January 1938, almost three "
              "years after the Bank began operations on 1 April 1935.",
  steps=["Operations began: April 1935", "First RBI notes: January 1938"],
  why="April 1935 is when RBI started; January 1949 is nationalisation; July 1955 is the formation of SBI.",
  facts=[fact("Jan 1938: First Reserve Bank notes issued", CHRON_35)])
Q(T, "Governors and leadership", "Intermediate",
  "Sir C. D. Deshmukh, the first Indian to be Governor of RBI, assumed office on:",
  ["11 August 1943", "1 July 1937", "1 July 1949", "1 March 1957"],
  concept="Early RBI Governors",
  explanation="RBI's chronology records that Sir C. D. Deshmukh assumed office as Governor on 11 August 1943, after "
              "Sir Osborne Smith and Sir James Braid Taylor. He was followed by Sir Benegal Rama Rau, who assumed "
              "office on 1 July 1949.",
  steps=["11 Aug 1943: C. D. Deshmukh assumes office"],
  why="1 July 1937 is J. B. Taylor; 1 July 1949 is Benegal Rama Rau; 1 March 1957 is H. V. R. Iengar.",
  facts=[fact("11 Aug 1943: Sir C. D. Deshmukh assumes office of Governor; 1 Jul 1949: Sir Benegal Rama Rau assumes "
              "office", CHRON_35)])
Q(T, "Establishment and structure", "Intermediate",
  "The Industrial Development Bank of India (IDBI), established on 1 July 1964 to provide long-term industrial "
  "finance, was initially set up as:",
  ["A subsidiary of the Reserve Bank of India", "A subsidiary of the State Bank of India",
   "A department of the Ministry of Finance", "A co-operative bank under NABARD"],
  concept="RBI's institution building",
  explanation="RBI's chronology records that IDBI was established on 1 July 1964 as a subsidiary of the Reserve Bank "
              "of India to provide long-term industrial finance; it took over the business of the Refinance "
              "Corporation for Industry in September 1964.",
  steps=["1 Jul 1964: IDBI set up as RBI subsidiary"],
  why="IDBI was not an SBI subsidiary or a ministry department; NABARD was set up only in 1982.",
  facts=[fact("1 Jul 1964: IDBI established as a subsidiary of the Reserve Bank of India with the purpose of providing "
              "long term industrial finance", CHRON_60)])
Q(T, "Establishment and structure", "Intermediate",
  "After the Hilton Young Commission's recommendation, which body revived the issue of establishing the Reserve Bank "
  "of India as the central bank in 1931?",
  ["Indian Central Banking Enquiry Committee", "Royal Commission on Agriculture", "Imperial Legislative Council",
   "Banking Commission"],
  concept="Road to the RBI Act",
  explanation="The Indian Central Banking Enquiry Committee revived the issue in 1931. The Reserve Bank of India Act, "
              "1934 (Act II of 1934), dated 5 March 1934, then provided the statutory basis for the Bank.",
  steps=["1926: Hilton Young", "1931: Central Banking Enquiry Committee", "5 Mar 1934: RBI Act"],
  why="The other bodies did not revive the central bank proposal in 1931 according to RBI's chronology.",
  facts=[fact("1931: Indian Central Banking Enquiry Committee revives the issue of the establishment of the Reserve "
              "Bank of India as the Central Bank for India; 5 March 1934: RBI Act, 1934 (II of 1934)", CHRON_26)])
Q(T, "Establishment and structure", "Advanced",
  "RBI also served as the central bank of Pakistan for a time after Partition. Which statement about this is "
  "correct?",
  ["RBI ceased to function as Pakistan's central bank on 30 June 1948, and the State Bank of Pakistan began "
   "operations from 1 July 1949",
   "RBI ceased to function as Pakistan's central bank on 15 August 1947",
   "The State Bank of Pakistan began on 1 January 1949, the day RBI was nationalised",
   "RBI continued as Pakistan's central bank until 1956"],
  concept="RBI after Partition",
  explanation="RBI's chronology records that RBI ceased to function as the Central Bank of Pakistan on 30 June 1948, "
              "and the State Bank of Pakistan commenced operations with effect from 1 July 1949.",
  steps=["30 Jun 1948: RBI ceases to be Pakistan's central bank", "1 Jul 1949: State Bank of Pakistan"],
  why="RBI did not stop on Independence Day itself; 1 January 1949 is RBI's nationalisation; 1956 is wrong.",
  facts=[fact("30 Jun 1948: RBI ceased to function as the Central Bank of Pakistan. State Bank of Pakistan commenced "
              "operations wef July 1, 1949", CHRON_35)])
Q(T, "Establishment and structure", "Advanced",
  "As listed on RBI's Organisation page in November 2026, which two persons are the Government officials nominated "
  "to RBI's Central Board under Section 8(1)(d) of the RBI Act?",
  ["Anuradha Thakur and Sanjay Lohiya", "Anand Gopal Mahindra and Syed Akbaruddin",
   "Swaminathan J and Rohit Jain", "Annie George Mathew and Janmejaya Kumar Sinha"],
  concept="Composition of the Central Board",
  explanation="RBI's Central Board lists the Governor and Deputy Governors under Section 8(1)(a), Government-nominated "
              "directors from various fields under Section 8(1)(c), and two Government officials under Section "
              "8(1)(d): Ms. Anuradha Thakur and Shri Sanjay Lohiya.",
  steps=["8(1)(a): Governor and Deputy Governors", "8(1)(c): nominated directors",
         "8(1)(d): Anuradha Thakur, Sanjay Lohiya"],
  why="Mahindra, Akbaruddin, Mathew and Sinha are 8(1)(c) directors; Swaminathan J and Rohit Jain are Deputy "
      "Governors.",
  current=ca("2026-11-05"),
  facts=[fact("Central Board: 8(1)(a) Governor and Deputy Governors including Swaminathan J and Rohit Jain; 8(1)(c) "
              "Anand Gopal Mahindra, Janmejaya Kumar Sinha, Syed Akbaruddin, Annie George Mathew; 8(1)(d) Anuradha "
              "Thakur, Sanjay Lohiya", ORG)])
Q(T, "Establishment and structure", "Advanced",
  "Consider the following statements from RBI's chronology of its early years:\nI. RBI's London Office, set up in "
  "October 1935, was closed on 30 September 1963.\nII. Exchange controls were introduced in India in September 1939 "
  "under the Defence of India Rules.\nIII. In 1937 RBI acted as banker to the Government of Burma and was also "
  "responsible for note issue in Burma.\nWhich of the above is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I only"],
  concept="RBI's early functions",
  explanation="All three are recorded by RBI: the London Office (October 1935) closed on 30 September 1963; exchange "
              "controls were introduced on 3 September 1939 under the Defence of India Rules; and in 1937 RBI acted "
              "as banker to the Government of Burma and handled its note issue.",
  steps=["I: correct", "II: correct", "III: correct"],
  why="Each of the other options leaves out at least one correct statement.",
  facts=[fact("Oct 1935: London Office of the Reserve Bank set up. This was closed on September 30, 1963; 1937: RBI "
              "acts as banker to the Government of Burma and also responsible for note issue in Burma; 3 Sep 1939: "
              "Introduction of Exchange Controls in India under Defence of India Rules", CHRON_35)])

# ================================================================= 4. RBI Functions (2 / 4 / 2)
T = "RBI Functions"
Q(T, "Issuer of currency", "Basic",
  "Coins in India are minted at four mints owned by SPMCIL. Which of the following is NOT one of those mint "
  "locations?",
  ["Nashik", "Mumbai", "Hyderabad", "NOIDA"],
  concept="Minting of coins",
  explanation="Coins are minted at four mints of the Security Printing and Minting Corporation of India Ltd (SPMCIL) "
              "located at Mumbai, Hyderabad, Kolkata and NOIDA. Nashik (Nasik) has an SPMCIL currency note press, not "
              "a mint.",
  steps=["Mints: Mumbai, Hyderabad, Kolkata, NOIDA", "Nashik: note press"],
  why="Mumbai, Hyderabad and NOIDA are all mint locations.",
  facts=[fact("Coins are minted in four mints owned by SPMCIL located at Mumbai, Hyderabad, Kolkata and NOIDA; the "
              "currency presses of SPMCIL are at Nasik and Dewas", CURRENCY_FAQ)])
Q(T, "Issuer of currency", "Basic",
  "According to RBI, the paper currently used for printing banknotes in India is made from:",
  ["100% cotton", "Polymer", "A blend of wood pulp and cotton", "Recycled paper"],
  concept="Banknote material",
  explanation="RBI states that the paper currently used for printing banknotes in India is made using 100% cotton.",
  steps=["Banknote paper: 100% cotton"],
  why="Indian banknotes in circulation are not polymer, wood-pulp blends or recycled paper.",
  facts=[fact("The paper currently being used for printing of banknotes in India is made by using 100% cotton",
              CURRENCY_FAQ)])
Q(T, "Issuer of currency", "Intermediate",
  "Under which section of the RBI Act, 1934 are all banknotes issued by RBI backed by assets such as gold coin, gold "
  "bullion, foreign securities, rupee coin and rupee securities?",
  ["Section 33", "Section 22", "Section 26", "Section 38"],
  concept="Assets backing the note issue",
  explanation="RBI states that, in terms of Section 33 of the RBI Act, all banknotes it issues are backed by assets "
              "such as gold coin, gold bullion, foreign securities, rupee coin and rupee securities.",
  steps=["Backing assets of note issue → Section 33"],
  why="Section 22 gives the sole right to issue notes; Section 26 makes notes legal tender; Section 38 deals with "
      "issuing coins through RBI.",
  facts=[fact("In terms of Section 33 of the RBI Act, 1934, all banknotes issued by RBI are backed by assets such as "
              "gold coin, gold bullion, foreign securities, rupee coin and rupee securities", CURRENCY_FAQ)])
Q(T, "Issuer of currency", "Intermediate",
  "Why is the one-rupee note a liability of the Government of India and not of RBI?",
  ["It is issued under the Coinage Act, 2011 and counts as 'rupee coin', which is a Government liability",
   "It is printed only by SPMCIL presses", "It is not legal tender", "It carries the RBI Governor's signature"],
  concept="One-rupee note",
  explanation="One-rupee notes are issued under the Coinage Act, 2011, are legal tender and are included in the "
              "expression 'rupee coin' for the RBI Act. Since rupee coins issued by the Government are its "
              "liabilities, the one-rupee note is also a liability of the Government of India.",
  steps=["₹1 note issued under Coinage Act → treated as rupee coin", "Rupee coin = Government liability"],
  why="Which press prints it does not decide liability; it is legal tender; it is not signed by the RBI Governor.",
  facts=[fact("The One Rupee notes issued under the Coinage Act, 2011 are legal tender and included in the expression "
              "Rupee coin; since rupee coins issued by Government constitute the liabilities of the Government, one "
              "rupee Note is also liability of the Government of India", CURRENCY_FAQ)])
Q(T, "Banker to government", "Intermediate",
  "Where is the final compilation of the Government accounts of the Centre and the States done by RBI?",
  ["Central Accounts Section, Nagpur", "Central Office, Mumbai", "Regional Office, New Delhi",
   "Department of Government and Bank Accounts, Kolkata"],
  concept="RBI as banker to Government",
  explanation="RBI carries out Government banking through its offices and agency banks. Final compilation of the "
              "Government accounts of the Centre and the States is done at the Central Accounts Section of RBI's "
              "Nagpur office, where the principal accounts of the Central Government are also kept.",
  steps=["Government accounts compiled at CAS, Nagpur"],
  why="The compilation is not done at the Central Office in Mumbai or at the New Delhi or Kolkata offices.",
  facts=[fact("Final compilation of Government accounts, of the Centre and the States, is done at Central Accounts "
              "Section, Nagpur office of the Reserve Bank", GOVT_BANKER)])
Q(T, "Banker to government", "Intermediate",
  "By agreement under the RBI Act, RBI is banker to all the States and Union Territories EXCEPT:",
  ["Sikkim", "Jammu and Kashmir", "Goa", "Puducherry"],
  concept="Banker to State Governments",
  explanation="Under Section 21A, RBI may by agreement act as banker to a State Government. RBI states that it is "
              "now banker to all the States and Union Territories except the State of Sikkim.",
  steps=["Banker to all States/UTs by agreement", "Exception: Sikkim"],
  why="Jammu and Kashmir, Goa and Puducherry are not the exception named by RBI.",
  facts=[fact("Accordingly, as of now, the Bank is banker to all the States and the Union Territories in the country, "
              "except for the State of Sikkim", GOVT_BANKER)])
Q(T, "Issuer of currency", "Advanced",
  "On 6 October 1956, India's system of note issue changed. What was the change?",
  ["From a proportional reserve system requiring 40% gold and foreign exchange reserves to a minimum reserve system",
   "From a minimum reserve system to a proportional reserve system with 40% gold backing",
   "From a fixed fiduciary system to a fully gold-backed system",
   "From note issue by the Government to note issue by RBI"],
  concept="Note issue systems",
  explanation="RBI records that on 6 October 1956 the system of note issue was changed from the Proportional Reserve "
              "System, which required RBI to keep 40% gold and foreign exchange reserves against note issue, to a "
              "minimum reserve system, so that expanding currency requirements could be met. Minimum reserves were "
              "relaxed further on 31 October 1957.",
  steps=["Before: proportional reserve (40% gold + forex)", "After: minimum reserve system"],
  why="The change was the reverse of the second option; India did not move to full gold backing; RBI had issued notes "
      "since 1938.",
  facts=[fact("6 Oct 1956: System of Note Issue changed from Proportional Reserve System requiring the Reserve Bank to "
              "maintain 40% gold and forex reserves against note issue to a minimum reserve system", CHRON_50)])
Q(T, "Banker to government", "Advanced",
  "Consider the following statements about RBI's agency banks for Government business:\nI. RBI appoints scheduled "
  "banks as its agents under Section 45(1) of the RBI Act.\nII. RBI pays commission to agency banks for the "
  "Government business they handle.\nIII. Only public sector banks can be appointed as agency banks.\nWhich of the "
  "above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Agency banks",
  explanation="Under Section 45(1), RBI may appoint any scheduled bank as its agent (I correct), and it pays "
              "commission to agency banks (II correct). RBI has appointed 12 public sector banks, 20 private sector "
              "banks and one foreign bank (wholly owned subsidiary) as agency banks, so III is wrong.",
  steps=["I: correct", "II: correct", "III: wrong (private and one foreign bank too)"],
  why="Options with III are wrong; 'I only' omits the commission paid to agency banks.",
  current=ca("2026-11-05"),
  facts=[fact("Under section 45(1) of RBI Act 1934, the Reserve Bank may appoint any scheduled bank as its agent; "
              "presently 12 public sector banks, 20 private sector banks and 01 foreign sector bank (WOS); the "
              "Reserve Bank pays commission to the agency banks", GOVT_BANKER)])

# ================================================================= 5. Monetary Policy (3 / 3 / 3)
T = "Monetary Policy"
OCT26 = ca("2026-10-07")
Q(T, "MPC structure", "Basic",
  "Which of the following attended the October 2026 MPC meeting as one of its external (Government-appointed) "
  "members?",
  ["Dr. Nagesh Kumar", "Dr. Poonam Gupta", "Shri Indranil Bhattacharyya", "Shri Swaminathan J"],
  concept="Members of the MPC",
  explanation="The MPC that met on 5–7 October 2026 was chaired by Governor Sanjay Malhotra and attended by Dr. "
              "Nagesh Kumar, Shri Saugata Bhattacharya, Prof. Ram Singh, Dr. Poonam Gupta and Shri Indranil "
              "Bhattacharyya. Nagesh Kumar (Director, ISID), Saugata Bhattacharya and Ram Singh are the external "
              "members notified by the Government on 1 October 2024; Poonam Gupta (Deputy Governor in charge of "
              "monetary policy) and Indranil Bhattacharyya (RBI officer) are RBI members.",
  steps=["External members: Nagesh Kumar, Saugata Bhattacharya, Ram Singh", "RBI members: Governor, Poonam Gupta, "
         "Indranil Bhattacharyya"],
  why="Poonam Gupta and Indranil Bhattacharyya are RBI's ex officio members; Swaminathan J is a Deputy Governor but "
      "not an MPC member.",
  current=OCT26,
  facts=[fact("The MPC members Dr. Nagesh Kumar, Shri Saugata Bhattacharya, Prof. Ram Singh, Dr. Poonam Gupta and Shri "
              "Indranil Bhattacharyya attended the meeting", MPC_OCT26),
         fact("Members notified on October 1, 2024: Deputy Governor in charge of Monetary Policy; one RBI officer "
              "nominated by the Central Board; Dr. Nagesh Kumar; Shri Saugata Bhattacharya; Prof. Ram Singh",
              MP_OVERVIEW)])
Q(T, "Transmission", "Basic",
  "In October 1994, when lending rates of commercial banks were deregulated, banks were required to declare their:",
  ["Prime Lending Rates (PLR)", "Base Rates", "MCLRs", "External benchmark rates"],
  concept="Evolution of loan pricing",
  explanation="RBI's chronology records that in October 1994 lending rates of commercial banks were deregulated and "
              "banks were required to declare their Prime Lending Rates. The Base Rate came in July 2010, MCLR in "
              "April 2016 and external benchmarks in October 2019.",
  steps=["1994: PLR", "2010: Base Rate", "2016: MCLR", "2019: external benchmark"],
  why="Base Rate, MCLR and external benchmarks came much later.",
  facts=[fact("Oct 1994: Lending rates of commercial banks deregulated. Banks required to declare their Prime Lending "
              "Rates (PLR)", CHRON_91)])
Q(T, "MPC structure", "Basic",
  "Under the MPC framework, what must each member of the Monetary Policy Committee do in respect of the proposed "
  "resolution?",
  ["Write a statement specifying the reasons for voting in favour of, or against, it",
   "Sign it only if the Governor agrees", "Abstain unless there is a tie",
   "Submit it to the Central Board for approval"],
  concept="Accountability of MPC members",
  explanation="Each MPC member has one vote, and each member writes a statement specifying the reasons for voting in "
              "favour of, or against, the proposed resolution. These statements form part of the published minutes.",
  steps=["One vote per member", "Each member records reasons for the vote"],
  why="Members vote independently; there is no abstention rule or Central Board approval of MPC resolutions.",
  facts=[fact("Each Member of the Monetary Policy Committee writes a statement specifying the reasons for voting in "
              "favour of, or against the proposed resolution", MP_OVERVIEW)])
Q(T, "Policy stance", "Intermediate",
  "When the MPC changed its stance to 'calibrated tightening' in October 2026, what did it say the new stance "
  "signals?",
  ["Rate cuts are off the table in the near term; the next action can only be a hike or a pause",
   "Rates will be raised at every meeting until inflation reaches 4%",
   "The MPC may cut or raise rates depending on data", "Liquidity will be kept in deficit through CRR increases"],
  concept="Meaning of the policy stance",
  explanation="The October 2026 resolution said that calibrated tightening only signals that, given current "
              "conditions, rate cuts are off the table in the near term, and policy action ahead can only be a rate "
              "hike or a pause, depending on evolving conditions.",
  steps=["Calibrated tightening → no cuts in the near term", "Next move: hike or pause"],
  why="The stance does not commit to a hike at every meeting; cuts are excluded; it says nothing about raising CRR.",
  current=OCT26,
  facts=[fact("It only signals that given the current conditions, rate cuts are off the table in the near term and "
              "policy action ahead can only be a rate hike or a pause", MPC_OCT26)])
Q(T, "MPC structure", "Intermediate",
  "The minutes of the MPC meeting of 5–7 October 2026, released on 21 October 2026, were published under which "
  "section of the RBI Act, 1934?",
  ["Section 45ZL", "Section 45ZB", "Section 45ZA", "Section 7"],
  concept="Publication of MPC minutes",
  explanation="RBI publishes the minutes of MPC meetings under Section 45ZL of the RBI Act. The MPC itself is "
              "constituted under Section 45ZB, and the inflation target is set under Section 45ZA.",
  steps=["Minutes → Section 45ZL", "MPC constitution → 45ZB", "Inflation target → 45ZA"],
  why="45ZB constitutes the MPC, 45ZA covers the inflation target, and Section 7 concerns Government directions to "
      "RBI.",
  current=ca("2026-10-21"),
  facts=[fact("Minutes of the Monetary Policy Committee Meeting, October 5 to 7, 2026 [Under Section 45ZL of the "
              "Reserve Bank of India Act, 1934]; MPC constituted under Section 45ZB", MIN_OCT26)])
Q(T, "Transmission", "Intermediate",
  "In August 2026, RBI proposed to rationalise the framework on interest rates on advances. Which of the following "
  "was among the stated aims?",
  ["Standardising divergent practices such as the day count convention and benchmark reset dates",
   "Abolishing the external benchmark system for retail loans",
   "Fixing a uniform maximum lending rate for all banks", "Replacing the repo rate with MCLR as the policy rate"],
  concept="Loan pricing and transmission",
  explanation="RBI's Statement on Developmental and Regulatory Policies of 5 August 2026 proposed a principle-based "
              "framework to harmonise guidelines across regulated entities, address operational aspects of MCLR and "
              "EBLR, and standardise divergent market practices on interest charging, including day count convention "
              "and benchmark reset dates, to strengthen monetary transmission and consumer protection.",
  steps=["Harmonise across REs", "Fix MCLR/EBLR operational issues", "Standardise day count and reset dates"],
  why="RBI did not propose abolishing EBLR, fixing a maximum lending rate (abolished in 1988) or changing the policy "
      "rate.",
  current=ca("2026-08-05"),
  facts=[fact("Rationalise the regulatory framework on interest rates: harmonise guidelines across REs; address "
              "operational aspects of MCLR and EBLR; standardise market practices including day count convention and "
              "benchmark reset dates", SDRP_AUG26)])

gdp = {"Jun": 6.6, "Aug": 6.7, "Oct": 7.1}
q1_proj_aug, q1_actual = 7.0, 7.8
assert round(gdp["Oct"] - gdp["Jun"], 1) == 0.5 and round(q1_actual - q1_proj_aug, 1) == 0.8
Q(T, "Policy stance", "Advanced",
  "The MPC projected real GDP growth for 2026-27 at 6.6% in June 2026, 6.7% in August 2026 (with Q1 at 7.0%) and 7.1% "
  "in October 2026, after the NSO estimated Q1:2026-27 growth at 7.8%. Which statement is correct?",
  ["The full-year projection rose by 0.5 percentage point from June to October, and Q1 growth beat the August "
   "projection by 0.8 percentage point",
   "The full-year projection rose by 0.4 percentage point from June to October, and Q1 beat the August projection "
   "by 0.7 percentage point",
   "The full-year projection fell from June to October, though Q1 beat the projection",
   "The full-year projection rose by 0.5 percentage point, but Q1 fell short of the August projection"],
  concept="Tracking projections",
  explanation="Full-year projection: 7.1 − 6.6 = 0.5 percentage point higher in October than in June. Q1 outcome: 7.8 "
              "− 7.0 = 0.8 percentage point above the August projection. The October resolution called Q1 growth "
              "higher than expected.",
  steps=["7.1 − 6.6 = 0.5", "7.8 − 7.0 = 0.8"],
  why="0.4 and 0.7 are arithmetic slips; the projection rose, not fell; Q1 exceeded the projection.",
  computed=True, current=OCT26,
  facts=[fact("Real GDP growth for 2026-27 is projected at 6.6 per cent (June 2026)", MPC_JUN26),
         fact("Real GDP growth for 2026-27 is projected at 6.7 per cent, with Q1 at 7.0 per cent (August 2026)",
              MPC_AUG26),
         fact("Real GDP growth in Q1:2026-27 at 7.8 per cent was higher than expected; projected at 7.1 per cent for "
              "2026-27", MPC_OCT26)])
Q(T, "Transmission", "Advanced",
  "Consider the following statements about RBI's liquidity operations as described in its monetary policy "
  "framework:\nI. The LAF includes overnight as well as term repos and reverse repos, at fixed and variable rates, "
  "along with the SDF and MSF.\nII. Outright open market operations, forex swaps and the market stabilisation "
  "scheme are liquidity instruments outside the LAF.\nIII. The operating target of monetary policy is the 10-year "
  "government bond yield.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Liquidity management toolkit",
  explanation="RBI describes the LAF as consisting of overnight and term repos/reverse repos (fixed and variable), "
              "SDF and MSF (I correct), and lists outright OMOs, forex swaps and MSS as liquidity instruments apart "
              "from the LAF (II correct). The operating target is the weighted average call rate, not the 10-year "
              "yield (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (operating target is WACR)"],
  why="Options including III are wrong; 'I only' leaves out II.",
  facts=[fact("LAF consists of overnight as well as term repo/reverse repos (fixed as well as variable rates), SDF and "
              "MSF. Apart from LAF, instruments of liquidity management include outright OMOs, forex swaps and MSS; "
              "operating target is the weighted average call rate (WACR)", MP_OVERVIEW)])
Q(T, "Transmission", "Advanced",
  "RBI's Internal Study Group on the MCLR system, whose final report was published in October 2017, observed that:",
  ["Internal benchmarks such as the Base Rate and MCLR had not delivered effective transmission of monetary policy",
   "MCLR transmitted policy changes faster than any external benchmark",
   "Floating-rate loans should be linked only to the Bank Rate",
   "Banks should return to the Prime Lending Rate system"],
  concept="Why external benchmarks were introduced",
  explanation="RBI's external benchmark circular recalls that the Internal Study Group on MCLR (final report October "
              "2017) observed that internal benchmarks such as the Base Rate and MCLR had not delivered effective "
              "transmission. This led to linking new floating-rate retail and MSE loans to external benchmarks from "
              "1 October 2019. MCLR itself had applied to floating rate loans sanctioned or renewed from 1 April 2016.",
  steps=["2016: MCLR", "2017: ISG finds weak transmission", "2019: external benchmark linkage"],
  why="The ISG found MCLR weak, not fast; it did not recommend the Bank Rate or a return to PLR.",
  facts=[fact("The ISG observed that internal benchmarks such as the Base rate/MCLR have not delivered effective "
              "transmission of monetary policy; floating rate rupee loans sanctioned and renewed w.e.f. April 1, 2016 "
              "shall be priced with reference to MCLR", EBLR)])

# ================================================================= 6. Repo Rate (3 / 1 / 1)
T = "Repo Rate"
Q(T, "Repo and policy corridor", "Basic",
  "As defined by RBI, the repo rate is the interest rate at which RBI:",
  ["Provides liquidity under the LAF to participants against the collateral of government and other approved "
   "securities",
   "Accepts uncollateralised overnight deposits from banks",
   "Rediscounts bills of exchange and commercial papers",
   "Lends to banks overnight by letting them dip into their SLR portfolio"],
  concept="Definition of the repo rate",
  explanation="RBI defines the repo rate as the rate at which it provides liquidity under the liquidity adjustment "
              "facility (LAF) to all LAF participants against the collateral of government and other approved "
              "securities.",
  steps=["Repo = RBI lends against eligible securities under LAF"],
  why="Uncollateralised deposits describe the SDF; rediscounting bills describes the Bank Rate; dipping into SLR "
      "describes the MSF.",
  current=OCT26,
  facts=[fact("Repo Rate: The interest rate at which the Reserve Bank provides liquidity under the LAF to all LAF "
              "participants against the collateral of government and other approved securities", MP_OVERVIEW)])
Q(T, "Repo and policy corridor", "Basic",
  "According to RBI's chronology, fixed rate repos in government securities were introduced to improve liquidity "
  "management and bring orderly conditions in money and forex markets in:",
  ["November 1997", "April 1999", "May 2011", "April 2022"],
  concept="History of repo operations",
  explanation="On 28 November 1997, as part of measures responding to the Asian currency crisis, RBI introduced fixed "
              "rate repos in G-secs to give manoeuvrability in liquidity management. The interim LAF followed in "
              "April 1999.",
  steps=["28 Nov 1997: fixed rate repos in G-secs"],
  why="April 1999 is the interim LAF; May 2011 is the MSF; April 2022 is the SDF.",
  current=OCT26,
  facts=[fact("28 Nov 1997: Fixed rate repos in G-Secs introduced to give maneuverability in liquidity management; and "
              "to bring orderly conditions in money and forex markets", CHRON_91)])
Q(T, "Repo and policy corridor", "Basic",
  "At its 60th meeting on 6–8 April 2026, the first of 2026-27, what did the MPC decide on the policy repo rate?",
  ["Kept it unchanged at 5.25% by a unanimous vote, with a neutral stance", "Cut it to 5.00%",
   "Raised it to 5.50%", "Kept it unchanged at 5.25% by a 4–2 vote"],
  concept="Policy decisions of 2026",
  explanation="At its 60th meeting (6–8 April 2026) the MPC voted unanimously to keep the policy repo rate unchanged "
              "at 5.25%, with the SDF at 5.00% and the MSF and Bank Rate at 5.50%, and continued with the neutral "
              "stance, citing the supply shock from the West Asia conflict.",
  steps=["Repo 5.25% unchanged", "Vote unanimous", "Stance neutral"],
  why="There was no cut or hike in April 2026; the vote was unanimous.",
  current=ca("2026-04-08"),
  facts=[fact("The MPC held its 60th meeting from April 6 to 8, 2026; voted unanimously to keep the policy repo rate "
              "unchanged at 5.25 per cent; continue with the neutral stance", MPC_APR26)])

meetings_unchanged = ["Feb 2026", "Apr 2026", "Jun 2026", "Aug 2026"]
assert len(meetings_unchanged) == 4
Q(T, "Repo and policy corridor", "Intermediate",
  "The MPC cut the repo rate to 5.25% in December 2025 and raised it to 5.50% in October 2026. At how many MPC "
  "meetings in between was the repo rate left unchanged?",
  ["4", "3", "5", "2"],
  concept="Counting policy meetings",
  explanation="Between December 2025 and October 2026 the MPC met in February 2026 (59th), April 2026 (60th), June "
              "2026 (61st) and August 2026 (62nd), and kept the repo rate at 5.25% each time. That is four meetings.",
  steps=["Feb, Apr, Jun, Aug 2026 → unchanged", "Count = 4"],
  why="3 or 2 miss some of these meetings; 5 wrongly counts the October meeting, which raised the rate.",
  computed=True, current=OCT26,
  facts=[fact("RBI kept the repo rate unchanged at 5.25% in February 2026", MPC_FEB26),
         fact("April 2026 (60th meeting): repo unchanged at 5.25 per cent", MPC_APR26),
         fact("June 2026 (61st meeting): repo unchanged at 5.25 per cent", MPC_JUN26),
         fact("August 2026 (62nd meeting): repo unchanged at 5.25 per cent", MPC_AUG26),
         fact("October 2026 (63rd meeting): repo increased by 25 bps to 5.50 per cent", MPC_OCT26)])

before_feb25 = 5.25 + 1.25
net_bps = round((5.50 - before_feb25) * 100)
assert before_feb25 == 6.50 and net_bps == -100
Q(T, "Repo and policy corridor", "Advanced",
  "By February 2026 the repo rate (5.25%) reflected cumulative cuts of 125 basis points made since February 2025. "
  "After the October 2026 increase, what is the net change in the repo rate compared with its level just before the "
  "February 2025 cut?",
  ["100 bps lower (6.50% to 5.50%)", "125 bps lower (6.75% to 5.50%)", "150 bps lower (7.00% to 5.50%)",
   "75 bps lower (6.25% to 5.50%)"],
  concept="Cumulative policy moves",
  explanation="Level before February 2025 = 5.25% + 1.25% = 6.50%. After the 25 bps increase of October 2026 the "
              "repo is 5.50%. Net change = 5.50 − 6.50 = −1.00 percentage point, i.e. 100 bps lower.",
  steps=["Pre-Feb 2025 level = 5.25 + 1.25 = 6.50%", "Now 5.50%", "Net = −100 bps"],
  why="125 bps ignores the October 2026 increase; 150 and 75 bps start from wrong levels.",
  computed=True, current=OCT26,
  facts=[fact("The decision came after cumulative cuts of 125 basis points since February 2025; repo unchanged at "
              "5.25% in February 2026", MPC_FEB26),
         fact("The MPC voted unanimously to increase the policy repo rate by 25 bps to 5.50 per cent", MPC_OCT26)])

# ================================================================= 7. Reverse Repo Rate (0 / 2 / 1)
T = "Reverse Repo Rate"
Q(T, "Reverse repo and SDF", "Intermediate",
  "Since 1 July 2025, during which hours, and on which days, is the overnight Standing Deposit Facility (SDF) window "
  "available?",
  ["19:00 hrs to 23:59 hrs on all days, including Sundays and holidays", "09:00 hrs to 17:00 hrs on working days only",
   "Only at the end of each reporting fortnight", "10:00 hrs to 16:00 hrs, Monday to Friday"],
  concept="Operation of the SDF",
  explanation="When the SDF was operationalised on 8 April 2022, the overnight window ran from 17:30 hrs to 23:59 hrs "
              "on all days, including Sundays and holidays, with reversal on the following working day in Mumbai. "
              "After call money market hours were extended to 7:00 PM, RBI moved the SDF and MSF window to 7:00 PM "
              "– 11:59 PM with effect from 1 July 2025, keeping all other terms unchanged.",
  steps=["2022–June 2025: 17:30–23:59", "From 1 July 2025: 19:00–23:59",
         "All days including Sundays and holidays; reversed next working day"],
  why="The SDF is not limited to working days, business hours or fortnight-ends.",
  facts=[fact6("SDF and MSF available between 7:00 PM and 11:59 PM with effect from July 01, 2025 (earlier 5:30 PM to "
               "11:59 PM), after call money timings were extended to 7:00 PM; all other terms unchanged", SDF_TIME),
         fact("The overnight SDF facility will be available between 17:30 hrs to 23:59 hrs on all days, including "
              "Sundays and holidays and would be reversed on the following working day in Mumbai", SDF_PR)])
Q(T, "Reverse repo and SDF", "Intermediate",
  "What is the minimum bid size under the Standing Deposit Facility, and is there a ceiling on the amount?",
  ["₹1 crore and multiples thereof; no ceiling", "₹5 crore; ceiling of 2% of NDTL", "₹25 lakh; ceiling of ₹500 crore",
   "₹10 crore; ceiling equal to excess CRR balance"],
  concept="SDF bids",
  explanation="RBI's SDF scheme sets the minimum bid size at ₹1 crore and multiples thereof, with no ceiling on the "
              "bid amount. Overnight SDF operates in straight-through processing mode on e-Kuber, and bids are "
              "settled immediately.",
  steps=["Minimum ₹1 crore (multiples of ₹1 crore)", "No ceiling"],
  why="The 2% of NDTL limit relates to the MSF; the other sizes and ceilings are not in the scheme.",
  facts=[fact("The minimum bid size under SDF is Rupees one crore and in multiples thereof. There is no ceiling on the "
              "bid amount", SDF_PR)])
Q(T, "Reverse repo and SDF", "Advanced",
  "Consider the following statements about the Standing Deposit Facility:\nI. Apart from liquidity management, RBI "
  "describes the SDF as a financial stability tool.\nII. Deposits under the SDF are eligible assets for maintaining "
  "SLR but are not reckoned for CRR.\nIII. RBI can use the SDF only for overnight deposits and never for longer "
  "tenors.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Features of the SDF",
  explanation="RBI states that the SDF is also a financial stability tool (I correct). SDF deposits are not reckoned "
              "for CRR under Section 42 of the RBI Act but are eligible for SLR under Section 24 of the BR Act (II "
              "correct). RBI retains the flexibility to absorb liquidity for longer tenors under the SDF with "
              "appropriate pricing (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (longer tenors possible)"],
  why="III contradicts the scheme, so options with III fail; 'I only' omits II.",
  facts=[fact("The SDF is also a financial stability tool in addition to its role in liquidity management",
              MP_OVERVIEW),
         fact("Deposits under the SDF shall not be reckoned as balances eligible for the maintenance of CRR but shall be "
              "an eligible asset for maintenance of SLR; RBI retains the flexibility to absorb liquidity for longer "
              "tenors under the SDF", SDF_PR)])

# ================================================================= 8. CRR (2 / 2 / 2)
T = "CRR"
Q(T, "CRR value", "Basic",
  "To what level did RBI raise the Cash Reserve Ratio on 1 July 1989, taking the combined pre-emption of banks' "
  "resources through SLR and CRR to over 53%?",
  ["15 per cent", "10 per cent", "20 per cent", "38.5 per cent"],
  concept="CRR in the pre-reform era",
  explanation="RBI's chronology records that the CRR was raised to 15% on 1 July 1989, taking statutory pre-emption "
              "through SLR and CRR to over 53% of banks' resources. The 1991 Narasimham Committee later recommended a "
              "phased reduction.",
  steps=["1 Jul 1989: CRR = 15%", "CRR + SLR pre-emption > 53%"],
  why="10% and 20% are not the 1989 level; 38.5% is near the then SLR level, not CRR.",
  facts=[fact("1 Jul 1989: CRR raised to 15 per cent taking statutory preemptions of banks' resources in the form of "
              "SLR and CRR to over 53%", CHRON_85)])
Q(T, "CRR value", "Basic",
  "Under RBI's phased CRR reduction of 2025, what CRR did banks have to maintain during the reporting fortnight "
  "beginning 1 November 2025?",
  ["3.25 per cent of NDTL", "3.75 per cent of NDTL", "3.5 per cent of NDTL", "4.0 per cent of NDTL"],
  concept="Phased CRR cut",
  explanation="RBI cut the CRR by 100 bps in four equal tranches of 25 bps: 3.75%, 3.5%, 3.25% and 3.0% of NDTL from "
              "the reporting fortnights beginning 6 September, 4 October, 1 November and 29 November 2025. So the "
              "fortnight beginning 1 November 2025 required 3.25%.",
  steps=["6 Sep: 3.75%", "4 Oct: 3.5%", "1 Nov: 3.25%", "29 Nov: 3.0%"],
  why="3.75% and 3.5% applied to the September and October fortnights; 4.0% was the level before the cuts.",
  facts=[fact("Banks are required to maintain the CRR at 3.75 per cent, 3.5 per cent, 3.25 per cent and 3.0 per cent "
              "of their NDTL effective from the reporting fortnight beginning September 6, October 4, November 1 and "
              "November 29, 2025, respectively", CRR_CUT)])
Q(T, "CRR value", "Intermediate",
  "In September 1962, RBI fixed the Cash Reserve Ratio uniformly at what level, and with what flexibility to vary it?",
  ["3% of demand and time liabilities, variable between 3% and 15%", "5% of demand liabilities and 2% of time "
   "liabilities, fixed", "10%, variable between 5% and 20%", "3%, with no power to vary it"],
  concept="CRR range",
  explanation="On 16 September 1962 the CRR of banks was fixed uniformly at 3% of their demand and time liabilities, "
              "with flexibility to vary it between 3% and 15%. (The original 1935 requirement was 5% of demand and "
              "2% of time liabilities.)",
  steps=["16 Sep 1962: CRR 3% of DTL", "Range: 3% to 15%"],
  why="5%/2% was the 1935 requirement; 10% with 5–20% and a fixed 3% are not the 1962 provision.",
  facts=[fact("16 Sep 1962: Cash Reserve Ratio of banks was fixed uniformly at 3 % of their Demand and Time "
              "Liabilities with the flexibility to vary it between 3 and 15%", CHRON_60)])
Q(T, "CRR concept", "Intermediate",
  "RBI's CRR notification of June 2025 was issued under Section 42(1) of the RBI Act, 1934 and which other "
  "provision, which applies to banks that are not scheduled banks?",
  ["Section 18(1) of the Banking Regulation Act, 1949", "Section 24 of the Banking Regulation Act, 1949",
   "Section 45ZA of the RBI Act, 1934", "Section 35A of the Banking Regulation Act, 1949"],
  concept="Legal basis of CRR",
  explanation="RBI prescribes CRR for scheduled banks under Section 42(1) of the RBI Act and for other banks under "
              "Section 18(1) of the Banking Regulation Act, read with Section 56. The June 2025 notification cites "
              "both provisions.",
  steps=["Scheduled banks: Section 42(1) RBI Act", "Non-scheduled banks: Section 18(1) BR Act (with Section 56)"],
  why="Section 24 of the BR Act deals with SLR; 45ZA with the inflation target; 35A with RBI's power to give "
      "directions.",
  facts=[fact("In exercise of the powers conferred under sub-section (1) of Section 42 of the RBI Act, 1934 and "
              "sub-section (1) of Section 18 of the Banking Regulation Act, 1949, read with Section 56 thereof",
              CRR_CUT)])

dl35, tl35 = 400, 600
crr35 = 0.05 * dl35 + 0.02 * tl35
crr_now = 0.03 * (dl35 + tl35)
assert round(crr35, 2) == 32.0 and round(crr35 - crr_now, 2) == 2.0
Q(T, "CRR concept", "Advanced",
  "A bank has demand liabilities of ₹400 crore and time liabilities of ₹600 crore. What cash reserve would it have "
  "needed under the requirement applied to scheduled banks from 5 July 1935, and how does that compare with a 3% CRR "
  "on its total liabilities?",
  ["₹32 crore, which is ₹2 crore more than under a 3% CRR", "₹50 crore, which is ₹20 crore more than under a 3% CRR",
   "₹20 crore, which is ₹10 crore less than under a 3% CRR", "₹30 crore, the same as under a 3% CRR"],
  concept="Original CRR formula",
  explanation="From 5 July 1935 scheduled banks had to hold cash with RBI equal to 5% of demand liabilities and 2% of "
              "time liabilities: 5% × 400 + 2% × 600 = 20 + 12 = ₹32 crore. A 3% CRR on ₹1,000 crore = ₹30 crore. "
              "Difference = ₹2 crore more under the 1935 rule.",
  steps=["5% × 400 = 20", "2% × 600 = 12", "Total = 32", "3% × 1,000 = 30 → difference 2"],
  why="₹50 crore applies 5% to everything; ₹20 crore counts only demand liabilities; ₹30 crore is the 3% figure.",
  computed=True,
  facts=[fact("5 Jul 1935: Scheduled banks required to maintain the Cash Reserve Ratio, i.e., hold cash balances with "
              "the RBI equivalent to 5% of their Demand Liabilities and 2% of their Time Liabilities", CHRON_35)])

req, cur_ac, sdf_dep = 900, 850, 100
shortfall = req - cur_ac  # SDF balances do not count for CRR
assert shortfall == 50
Q(T, "CRR concept", "Advanced",
  "A bank's required average CRR balance for a fortnight is ₹900 crore. Its average balance in its current account "
  "with RBI was ₹850 crore, and it also kept an average of ₹100 crore overnight under the Standing Deposit Facility. "
  "What is its CRR position?",
  ["Short by ₹50 crore, because SDF deposits are not reckoned for CRR",
   "Surplus of ₹50 crore, because SDF deposits count towards CRR", "Exactly compliant",
   "Short by ₹150 crore, because SDF deposits are deducted from the CRR balance"],
  concept="What counts as CRR balance",
  explanation="Deposits under the SDF are not reckoned as balances eligible for CRR maintenance under Section 42 of "
              "the RBI Act (they are eligible for SLR). So only ₹850 crore counts: 900 − 850 = ₹50 crore shortfall.",
  steps=["Eligible CRR balance = 850", "Shortfall = 900 − 850 = 50"],
  why="Counting the SDF gives a false surplus; it is neither compliant nor penalised by deducting the SDF amount.",
  computed=True,
  facts=[fact("Deposits under the SDF shall not be reckoned as balances eligible for the maintenance of the cash "
              "reserve ratio (CRR) under Section 42 of the RBI Act, 1934", SDF_PR)])

# ================================================================= 9. SLR (1 / 1 / 0)
T = "SLR"
Q(T, "SLR concept", "Basic",
  "The Statutory Liquidity Ratio, requiring banks to maintain liquid assets, was introduced for the first time "
  "through which law?",
  ["Banking Companies Act, 1949", "Reserve Bank of India Act, 1934", "Indian Companies (Amendment) Act, 1936",
   "Banking Laws (Amendment) Act, 2025"],
  concept="Origin of SLR",
  explanation="RBI's chronology records that the Banking Companies Act, 1949, which came into force on 16 March 1949, "
              "introduced the SLR for the first time. The Act was later renamed the Banking Regulation Act.",
  steps=["16 Mar 1949: Banking Companies Act → SLR introduced"],
  why="The RBI Act, 1934 provides for CRR; the 1936 Companies amendment added a chapter on banks; the 2025 Act deals "
      "with governance and nomination.",
  facts=[fact("16 Mar 1949: Coming into force of the Banking Companies Act, 1949... The Statutory Liquidity Ratio (SLR) "
              "requiring banks to maintain liquid assets was introduced for the first time", CHRON_35)])
Q(T, "SLR value", "Intermediate",
  "Under the 1962 amendment of the Banking Regulation Act, scheduled banks had to maintain minimum liquid assets (SLR) "
  "of not less than what share of their demand and time liabilities?",
  ["25 per cent", "18 per cent", "40 per cent", "15 per cent"],
  concept="SLR floor of 1962",
  explanation="RBI's chronology records that the Banking Regulation Act was amended in 1962 to require scheduled banks "
              "to maintain minimum liquid assets (SLR) of not less than 25% of their demand and time liabilities.",
  steps=["1962 BR Act amendment → SLR not less than 25%"],
  why="18% is today's SLR; 40% is the present ceiling; 15% is not the 1962 floor.",
  facts=[fact("1962: The Banking Regulation Act amended. Scheduled Banks to maintain minimum liquid assets (SLR) of not "
              "less than 25% of the Demand and Time Liabilities", CHRON_60)])

# ================================================================= 10. Bank Rate (1 / 1 / 1)
T = "Bank Rate"
Q(T, "Bank rate and MSF", "Basic",
  "As defined by RBI, the Bank Rate is the rate at which RBI is ready to:",
  ["Buy or rediscount bills of exchange or other commercial papers",
   "Lend overnight to banks against government securities under the LAF",
   "Accept overnight deposits from banks without collateral", "Pay interest on banks' CRR balances"],
  concept="Definition of the Bank Rate",
  explanation="RBI defines the Bank Rate as the rate at which it is ready to buy or rediscount bills of exchange or "
              "other commercial papers. It now acts as the penal rate for reserve shortfalls and is aligned with the "
              "MSF rate.",
  steps=["Bank Rate = rediscount rate for bills of exchange/commercial papers"],
  why="LAF lending is the repo; uncollateralised deposits are the SDF; RBI pays no interest on CRR balances.",
  facts=[fact("Bank Rate: The rate at which the Reserve Bank is ready to buy or rediscount bills of exchange or other "
              "commercial papers", MP_OVERVIEW)])
Q(T, "Bank rate and MSF", "Intermediate",
  "How does RBI describe the role of the Marginal Standing Facility (MSF) in the liquidity framework?",
  ["A penal-rate overnight window that acts as a safety valve against unanticipated liquidity shocks",
   "The floor of the LAF corridor for absorbing surplus liquidity", "A long-term refinance window for priority sectors",
   "The operating target of monetary policy"],
  concept="Purpose of the MSF",
  explanation="RBI describes the MSF rate as the penal rate at which banks can borrow overnight by dipping into their "
              "SLR portfolio up to a predefined limit, and says it provides a safety valve against unanticipated "
              "liquidity shocks to the banking system. It forms the ceiling of the LAF corridor.",
  steps=["MSF = penal overnight borrowing", "Purpose: safety valve against liquidity shocks"],
  why="The floor is the SDF; the MSF is not long-term refinance; the operating target is the WACR.",
  facts=[fact("MSF Rate: The penal rate at which banks can borrow, on an overnight basis... This provides a safety "
              "valve against unanticipated liquidity shocks to the banking system", MP_OVERVIEW)])
Q(T, "Bank rate and MSF", "Advanced",
  "The MSF was introduced with effect from 9 May 2011. How did its design at launch differ from the present one?",
  ["At launch it was priced 100 bps above the repo rate with access up to 1% of NDTL; now it is 25 bps above the "
   "repo rate with a 2% limit",
   "At launch it was priced 25 bps above the repo rate with a 2% limit; now it is 100 bps above with 1%",
   "At launch it was below the repo rate; now it is above it", "Its design has not changed since 2011"],
  concept="Evolution of the MSF",
  explanation="RBI's circular of 9 May 2011 set the MSF rate at 100 basis points above the LAF repo rate, with "
              "eligible entities able to borrow overnight up to 1% of their NDTL. Today RBI places the MSF rate 25 "
              "bps above the repo rate and the dip into the SLR portfolio is up to 2%.",
  steps=["2011: repo + 100 bps, up to 1% of NDTL", "Now: repo + 25 bps, up to 2%"],
  why="The second option reverses the two designs; the MSF was never below repo; the design has changed.",
  facts=[fact("MSF introduced with effect from May 9, 2011; up to one per cent of NDTL; rate 100 basis points above "
              "the LAF repo rate", MSF_2011),
         fact("MSF: borrow overnight by dipping into SLR portfolio up to a predefined limit (2 per cent); MSF rate "
              "placed at 25 basis points above the policy repo rate", MP_OVERVIEW)])

# ================================================================= 11. Inflation (1 / 2 / 4)
T = "Inflation"
Q(T, "CPI and WPI", "Basic",
  "According to the MPC's October 2026 resolution, what was core CPI inflation in August 2026?",
  ["4.2 per cent", "4.8 per cent", "2.9 per cent", "4.4 per cent"],
  concept="Core inflation",
  explanation="The October 2026 resolution said core inflation increased to 4.2% in August 2026, while core inflation "
              "excluding precious metals was 2.9%. Headline CPI inflation was 4.8% in August.",
  steps=["Core (Aug 2026) = 4.2%", "Core ex-precious metals = 2.9%", "Headline = 4.8%"],
  why="4.8% is headline inflation; 2.9% excludes precious metals; 4.4% is the core projection for 2026-27.",
  current=OCT26,
  facts=[fact("Core inflation increased to 4.2 per cent and core inflation, excluding precious metals, increased to "
              "2.9 per cent in August", MPC_OCT26)])
Q(T, "Inflation targeting", "Intermediate",
  "In June 2026 headline CPI inflation rose to 4.4%. According to the August 2026 MPC resolution, for how many "
  "consecutive months had it been below the 4% target before that?",
  ["16 months", "12 months", "6 months", "24 months"],
  concept="Inflation relative to target",
  explanation="The August 2026 resolution said CPI inflation increased to 4.4% in June 2026 after remaining below the "
              "target for 16 consecutive months, and that it was 30 bps lower than projected for Q1:2026-27.",
  steps=["June 2026 CPI: 4.4%", "Previously below target for 16 consecutive months"],
  why="12, 6 and 24 months do not match the resolution.",
  current=ca("2026-08-05"),
  facts=[fact("CPI inflation increased to 4.4 per cent in June 2026 after remaining below the target for 16 "
              "consecutive months", MPC_AUG26)])
Q(T, "CPI and WPI", "Intermediate",
  "As per the new CPI series (2024=100) cited in the April 2026 MPC resolution, headline inflation in February 2026 "
  "was:",
  ["3.2 per cent, up from 2.7 per cent in January", "2.7 per cent, down from 3.2 per cent in January",
   "4.6 per cent, up from 4.0 per cent in January", "1.7 per cent, unchanged from January"],
  concept="Early prints of the new CPI",
  explanation="The April 2026 resolution said that, as per the new CPI series (2024=100), headline inflation rose to "
              "3.2% in February 2026 from 2.7% in January, mainly due to unfavourable base effects; core inflation "
              "excluding precious metals stayed at 2.1%.",
  steps=["Jan 2026: 2.7%", "Feb 2026: 3.2%"],
  why="The second option reverses the months; 4.6% and 4.0% are the 2026-27 and Q1 projections.",
  current=ca("2026-04-08"),
  facts=[fact("As per the new CPI series (2024=100), headline inflation increased to 3.2 per cent in February 2026 "
              "from 2.7 per cent in January", MPC_APR26)])

proj = {"Apr": 4.6, "Jun": 5.1, "Aug": 5.0, "Oct": 5.2}
assert proj["Jun"] > proj["Apr"] and proj["Aug"] < proj["Jun"] and proj["Oct"] > proj["Aug"]
Q(T, "Inflation targeting", "Advanced",
  "The MPC's CPI inflation projection for 2026-27 was 4.6% in April 2026, 5.1% in June, 5.0% in August and 5.2% in "
  "October. Which statement is correct?",
  ["It was raised in June, trimmed slightly in August and raised again in October, ending 0.6 percentage point above "
   "the April projection",
   "It was raised at every meeting, ending 0.6 percentage point above the April projection",
   "It was raised in June and October only, ending 0.4 percentage point above April",
   "It was cut in June and raised in August and October"],
  concept="Revisions to the inflation outlook",
  explanation="April 4.6 → June 5.1 (up 0.5) → August 5.0 (down 0.1) → October 5.2 (up 0.2). Net change from April "
              "to October = 5.2 − 4.6 = 0.6 percentage point.",
  steps=["Jun: +0.5", "Aug: −0.1", "Oct: +0.2", "Net: +0.6"],
  why="August was a small cut, not a rise; the net change is 0.6, not 0.4; June was a rise, not a cut.",
  computed=True, current=OCT26,
  facts=[fact("CPI inflation for 2026-27 is projected to be at 4.6 per cent (April 2026)", MPC_APR26),
         fact("CPI inflation for 2026-27 is projected to be 5.1 per cent (June 2026)", MPC_JUN26),
         fact("CPI inflation for 2026-27 is projected to be 5.0 per cent (August 2026)", MPC_AUG26),
         fact("CPI inflation is projected to be 5.2 per cent for 2026-27 (October 2026)", MPC_OCT26)])

q1_proj_jun = 4.2
q1_realised = round(q1_proj_jun - 0.30, 2)
assert q1_realised == 3.9
Q(T, "Inflation targeting", "Advanced",
  "In June 2026 the MPC projected Q1:2026-27 CPI inflation at 4.2%. In August it said realised Q1 inflation turned "
  "out 30 basis points lower than earlier projected. What was realised Q1 inflation, and was it within the tolerance "
  "band?",
  ["About 3.9%, below the 4% target but within the 2–6% band", "About 4.5%, above the target but within the band",
   "About 3.9%, below the lower tolerance limit", "About 1.2%, below the lower tolerance limit"],
  concept="Projection errors",
  explanation="Realised Q1 inflation ≈ 4.2% − 0.30 percentage point = 3.9%. This is just below the 4% target and well "
              "inside the 2–6% tolerance band.",
  steps=["4.2 − 0.3 = 3.9", "2 ≤ 3.9 ≤ 6 → within band"],
  why="4.5% adds the gap instead of subtracting; 3.9% is above the 2% lower limit; 1.2% treats 30 bps as 3 points.",
  computed=True, current=ca("2026-08-05"),
  facts=[fact("CPI inflation for 2026-27 is projected with Q1 at 4.2 per cent (June 2026)", MPC_JUN26),
         fact("It turned out to be lower by 30 basis points (bps) than what was earlier projected for Q1:2026-27",
              MPC_AUG26)])
Q(T, "CPI and WPI", "Advanced",
  "Consider the following statements about the MPC's projections of core CPI inflation for 2026-27:\nI. It was "
  "projected at 4.7% in June 2026.\nII. It was revised down to 4.3% in August 2026.\nIII. It was put at 4.4% in "
  "October 2026.\nWhich of the above is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I only"],
  concept="Core inflation outlook",
  explanation="The June 2026 resolution projected core inflation at 4.7% for 2026-27, the August resolution at 4.3%, "
              "and the October resolution at 4.4%. All three statements are correct.",
  steps=["June: 4.7%", "August: 4.3%", "October: 4.4%"],
  why="Each of the other options leaves out a correct statement.",
  current=OCT26,
  facts=[fact("Core inflation is projected at 4.7 per cent for 2026-27", MPC_JUN26),
         fact("Core inflation is projected at 4.3 per cent for 2026-27", MPC_AUG26),
         fact("Core inflation is projected at 4.4 per cent for 2026-27", MPC_OCT26)])
Q(T, "Inflation targeting", "Advanced",
  "According to the MPC's October 2026 resolution, how does monetary policy primarily act on inflation that arises "
  "from supply-side shocks?",
  ["By curtailing second-round effects such as inflation expectations and firm-level pricing behaviour",
   "By directly lowering the prices of food and fuel", "By raising the CRR to absorb the supply shock",
   "It cannot act on supply-side inflation at all"],
  concept="Monetary policy and supply shocks",
  explanation="The resolution said that, for supply-side inflation, monetary policy primarily acts by curtailing "
              "second-round effects (inflation expectations, firm-level pricing behaviour), which take time to "
              "appear. Indicators of generalisation such as core inflation and diffusion indices are used to judge "
              "them.",
  steps=["Supply shock → watch second-round effects", "Policy targets expectations and pricing behaviour"],
  why="Policy does not directly set food or fuel prices; the resolution does not mention CRR; it says policy does act, "
      "through second-round effects.",
  current=OCT26,
  facts=[fact("As regards supply side inflation, monetary policy primarily acts by curtailing second round effects "
              "(inflation expectations and firm level pricing behaviour, etc.)", MPC_OCT26)])

# ================================================================= 12. NPA (1 / 6 / 1)
T = "NPA"
Q(T, "Classification", "Basic",
  "A cash credit account is treated as 'out of order' (and can become an NPA) if its outstanding balance remains "
  "continuously in excess of the sanctioned limit or drawing power for:",
  ["90 days", "30 days", "60 days", "180 days"],
  concept="Out-of-order accounts",
  explanation="Under RBI's asset classification directions, a CC/OD account is 'out of order' if the outstanding "
              "balance remains continuously above the sanctioned limit/drawing power for 90 days, or if it is within "
              "the limit but there are no credits for 90 days, or credits do not cover the interest debited during "
              "the previous 90 days.",
  steps=["Balance above limit/DP continuously for 90 days → out of order"],
  why="30 and 60 days mark SMA stages for loans; 180 days is not the test.",
  facts=[fact("A CC/OD account shall be treated as 'out of order' if the outstanding balance remains continuously in "
              "excess of the sanctioned limit / drawing power for 90 days", IRAC_MD)])
Q(T, "Classification", "Intermediate",
  "Under RBI's prudential norms, a 'loss asset' is one where:",
  ["Loss has been identified by the bank, its auditors or RBI inspection, but the amount has not been written off "
   "wholly",
   "The asset has been substandard for 12 months", "The account has been written off fully",
   "Interest is overdue for more than 90 days"],
  concept="Loss assets",
  explanation="RBI defines a loss asset as an asset where loss has been identified by the bank or internal or "
              "external auditors or RBI inspection, but the amount has not been written off wholly. It is considered "
              "uncollectible and of such little value that its continuance as a bankable asset is not warranted.",
  steps=["Loss identified + not fully written off → loss asset"],
  why="12 months as substandard makes an asset doubtful; a fully written-off asset is off the books; 90 days overdue "
      "is the NPA test.",
  facts=[fact("'loss asset' shall mean an asset where loss has been identified by a bank or internal or external "
              "auditors or the inspection conducted by the Reserve Bank, but the amount has not been written off "
              "wholly by the bank", IRAC_MD)])
Q(T, "Classification", "Intermediate",
  "When does a credit card account become a non-performing asset under RBI's norms?",
  ["When the minimum amount due is not paid fully within 90 days from the payment due date in the statement",
   "When the account is overdue for more than three days", "When the full outstanding is not paid by the due date",
   "When the card is not used for 90 days"],
  concept="NPA rule for credit cards",
  explanation="A credit card account is an NPA if the minimum amount due, as mentioned in the statement, is not paid "
              "fully within 90 days from the payment due date. Separately, a card can be reported as 'past due' or "
              "charged late fees only after it is overdue for more than three days.",
  steps=["NPA: minimum amount due unpaid for 90 days from due date", "Past due reporting: > 3 days overdue"],
  why="Three days is the past-due reporting threshold, not NPA; non-payment of the full outstanding or non-use is not "
      "the test.",
  facts=[fact("A credit card account where the minimum amount due, as mentioned in the statement, is not paid fully "
              "within 90 days from the payment due date mentioned in the statement", IRAC_MD)])
Q(T, "Classification", "Intermediate",
  "For a crop loan for a short-duration crop, when is the account classified as an NPA?",
  ["When the instalment of principal or interest remains overdue for two crop seasons",
   "When it remains overdue for one crop season", "When it remains overdue for 90 days",
   "When it remains overdue for 12 months"],
  concept="Agricultural NPAs",
  explanation="Agricultural loans follow crop seasons: for short-duration crops, an account becomes an NPA when the "
              "instalment of principal or interest remains overdue for two crop seasons; for long-duration crops, one "
              "crop season.",
  steps=["Short-duration crop → two crop seasons", "Long-duration crop → one crop season"],
  why="One crop season applies to long-duration crops; 90 days and 12 months are not the agricultural tests.",
  facts=[fact("The instalment of principal or interest thereon remains overdue for two crop seasons for short "
              "duration crops", IRAC_MD)])
Q(T, "Classification", "Intermediate",
  "For determining drawing power in working capital accounts of large borrowers, stock statements relied upon by a "
  "bank should not be older than:",
  ["Three months", "One month", "Six months", "One year"],
  concept="Drawing power",
  explanation="Drawing power must be based on a current stock statement; considering the difficulties of large "
              "borrowers, statements should not be older than three months. Outstanding based on drawing power "
              "from older stock statements is deemed irregular.",
  steps=["Stock statement ≤ 3 months old", "Older → outstanding deemed irregular"],
  why="One month, six months and one year are not the limit set in the directions.",
  facts=[fact("Stock statements relied upon by a bank for determining drawing power should not be older than three "
              "months; outstanding based on drawing power calculated from stock statements older than three months "
              "shall be deemed as irregular", IRAC_MD)])
Q(T, "Resolution and IBC", "Intermediate",
  "Under the Insolvency and Bankruptcy Code, 2016, a financial creditor (such as a bank) initiates the corporate "
  "insolvency resolution process under which section?",
  ["Section 7", "Section 9", "Section 10", "Section 12"],
  concept="Initiating CIRP",
  explanation="IBBI's FAQs state that CIRP may be initiated by a financial creditor under Section 7, an operational "
              "creditor under Section 9 and the corporate applicant (the corporate debtor itself) under Section 10.",
  steps=["Financial creditor → Section 7", "Operational creditor → Section 9", "Corporate applicant → Section 10"],
  why="Section 9 is for operational creditors; Section 10 for the corporate applicant; Section 12 sets the time limit.",
  facts=[fact("CIRP may be initiated by a financial creditor under section 7, an operational creditor under section 9 "
              "and corporate applicant of corporate debtor under section 10 of the Code", IBBI_FAQ)])
Q(T, "Resolution and IBC", "Intermediate",
  "Under the IBC, what is the maximum time within which a CIRP must mandatorily be completed, including any extension "
  "and litigation period, and what vote of the committee of creditors is needed to seek the extension?",
  ["330 days; 66% of the voting share", "270 days; 51% of the voting share", "180 days; 90% of the voting share",
   "365 days; 75% of the voting share"],
  concept="CIRP timelines",
  explanation="CIRP must be completed within 180 days, extendable once by up to 90 days if the committee of creditors "
              "resolves with 66% of the voting share. The outer limit, including extension and litigation, is 330 "
              "days.",
  steps=["Normal: 180 days", "Extension: once, up to 90 days (66% CoC)", "Outer limit: 330 days"],
  why="270 days omits litigation time; 90% is the vote needed for withdrawal of an application; 365 days/75% are not "
      "in the Code.",
  facts=[fact("CIRP shall be completed within 180 days; one-time extension of 90 days; maximum time including any "
              "extension or litigation period is 330 days; committee of creditors to pass a resolution with sixty-six "
              "percent of the total voting share to extend", IBBI_FAQ)])
Q(T, "Classification", "Advanced",
  "Banks P, Q and R lend to a borrower under a consortium. The borrower pools all remittances with lead bank P, which "
  "keeps paying itself but does not pass on the shares of Q and R. How should the account be classified in Q's and "
  "R's books?",
  ["As NPA, because the account is treated as not serviced in their books",
   "As standard, because the borrower is paying the consortium",
   "As NPA in P's books only", "As SMA-2, until P transfers the funds"],
  concept="Consortium accounts",
  explanation="Asset classification under consortium lending depends on each member's own record of recovery. Where "
              "remittances are pooled with one member that does not part with the others' shares, the account is "
              "treated as not serviced in the books of the other members and therefore as NPA. Members should get "
              "their share transferred from the lead bank or obtain its express consent.",
  steps=["Classification follows each member's own recovery", "No share received → not serviced → NPA for Q and R"],
  why="Payment to the lead bank alone does not service Q's and R's loans; P is being paid; SMA-2 is not the rule here.",
  facts=[fact("Where the remittances by the borrower under consortium lending arrangements are pooled with one "
              "consortium member and/or the member receiving remittances is not parting with the share of other "
              "members, the account will be treated as not serviced in the books of the other members and therefore "
              "be treated as NPA", IRAC_MD)])

# ================================================================= 13. Basel Norms (1 / 3 / 1)
T = "Basel Norms"
Q(T, "Capital adequacy", "Basic",
  "The Basel III capital and liquidity standards were endorsed in November 2010 at the G20 Leaders' Summit held in:",
  ["Seoul", "Basel", "Toronto", "London"],
  concept="Basel III",
  explanation="After the GHOS announced higher capital standards in September 2010, the new capital and liquidity "
              "standards were endorsed at the G20 Leaders' Summit in Seoul in November 2010. The Basel Committee "
              "issued the Basel III texts in mid-December 2010.",
  steps=["Sep 2010: GHOS announcement", "Nov 2010: G20 Seoul endorsement", "Dec 2010: Basel III texts issued"],
  why="Basel hosts the BCBS secretariat, not that summit; Toronto and London were earlier G20 summits.",
  facts=[fact("In November 2010, the new capital and liquidity standards were endorsed at the G20 Leaders' Summit in "
              "Seoul; the proposed standards were issued by the Committee in mid-December 2010", BCBS_HIST)])
Q(T, "Capital adequacy", "Intermediate",
  "Under RBI's directions on minimum capital requirements for operational risk (effective 1 April 2027), the Business "
  "Indicator is built from which three components?",
  ["Interest, lease and dividend component; services component; financial component",
   "Credit, market and liquidity components", "CET1, AT1 and Tier 2 components",
   "Gross income of the last three years only"],
  concept="Operational risk capital",
  explanation="RBI's October 2026 amendment to the operational risk chapter (coming into effect from 1 April 2027) "
              "describes the Business Indicator's constituents as the Interest, Lease and Dividend Component (ILDC), "
              "the Services Component (SC) and the Financial Component (FC), mapped to items of banks' financial "
              "statements.",
  steps=["BI = ILDC + SC + FC"],
  why="Credit/market/liquidity are risk types; CET1/AT1/Tier 2 are capital tiers; average gross income was the old "
      "basic indicator approach.",
  current=ca("2026-10-23"),
  facts=[fact("The description for each of these constituents of the BI (i.e., ILDC, SC, and FC); Chapter IV on "
              "Minimum Capital Requirements for Operational Risk shall come into effect from April 1, 2027", OPRISK)])
Q(T, "Leverage ratio", "Intermediate",
  "Under RBI's October 2026 amendment aligning with the Basel 'leverage ratio 2017 standard', what leverage ratio must "
  "a branch of a global systemically important bank (G-SIB) in India maintain?",
  ["3.5% plus the leverage ratio buffer applicable to it as a G-SIB", "4%, the same as a D-SIB", "3% only",
   "5% plus the countercyclical buffer"],
  concept="Leverage ratio for G-SIB branches",
  explanation="The amended directions keep 4% for D-SIBs and 3.5% for other banks, and require a G-SIB branch in "
              "India to maintain 3.5% plus the leverage ratio buffer applicable to it as a G-SIB (including any "
              "additional buffer prescribed by its home regulator).",
  steps=["D-SIB: 4%", "Others: 3.5%", "G-SIB branch: 3.5% + G-SIB leverage buffer"],
  why="4% applies to D-SIBs; 3% was the Basel minimum, not RBI's; 5% plus CCyB is not prescribed.",
  current=ca("2026-10-23"),
  facts=[fact("Branch of a G-SIB in India shall maintain a leverage ratio of 3.5 per cent plus the leverage ratio "
              "buffer applicable to it as a G-SIB", LEV_GSIB)])
Q(T, "Leverage ratio", "Intermediate",
  "How often must banks calculate the capital measure and the exposure measure of the leverage ratio under RBI's "
  "amended directions?",
  ["On a quarter-end basis, though more frequent averaging may be used consistently with RBI's approval",
   "Only at the end of each financial year", "Daily, with no exceptions",
   "Once in six months, on 30 September and 31 March"],
  concept="Measuring the leverage ratio",
  explanation="Both the capital measure and the exposure measure are calculated on a quarter-end basis. A bank may, "
              "with RBI's approval, use more frequent calculations such as daily or monthly averaging, provided it "
              "does so consistently. The minimum must be met at all times.",
  steps=["Quarter-end basis", "More frequent averaging allowed with RBI approval", "Minimum to be met at all times"],
  why="Annual and half-yearly calculation are not prescribed; daily averaging is optional, not mandatory.",
  current=ca("2026-10-23"),
  facts=[fact("Both the capital measure and the exposure measure are to be calculated on a quarter-end basis. However, "
              "a bank may, subject to the Reserve Bank's approval, use more frequent calculations (e.g., daily or "
              "monthly averaging) as long as it does so consistently", LEV_GSIB)])


def ccs_ratio(cet1, lev):
    c = 100 if cet1 <= 6.375 else 80 if cet1 <= 7.25 else 60 if cet1 <= 8.125 else 40 if cet1 <= 9.0 else 0
    lv = 100 if lev <= 3.625 else 80 if lev <= 3.75 else 60 if lev <= 3.875 else 40 if lev <= 4.0 else 0
    return c, lv, max(c, lv)


assert ccs_ratio(7.5, 3.6) == (60, 100, 100)
Q(T, "Leverage ratio", "Advanced",
  "A G-SIB branch in India in the first bucket of higher loss absorbency has a CET1 risk-based ratio of 7.5% and a "
  "Tier 1 leverage ratio of 3.6%, so it meets neither requirement. Using RBI's table of minimum capital conservation "
  "ratios, what share of earnings must it conserve?",
  ["100%, the higher of the two applicable standards", "60%, based on its CET1 ratio",
   "80%, the average of the two standards", "0%, because both ratios exceed the 3.5% and 5.5% minimums"],
  concept="Capital conservation for G-SIB branches",
  explanation="RBI's table: CET1 of 7.5% falls in the band >7.25%–8.125% → 60%; a Tier 1 leverage ratio of 3.6% "
              "falls in the band 3.5%–3.625% → 100%. A branch that does not meet both requirements is subject to the "
              "higher of the associated standards, so it must conserve 100% of earnings.",
  steps=["CET1 7.5% → 60%", "Leverage 3.6% → 100%", "Fails both → higher = 100%"],
  why="60% ignores the leverage standard; standards are not averaged; meeting the bare minimums does not avoid "
      "conservation when buffers are not met.",
  computed=True, current=ca("2026-10-23"),
  facts=[fact("CET1 >7.25%–8.125% → 60%; Tier 1 leverage 3.5%–3.625% → 100%; a G-SIB branch which does not meet "
              "both requirements will be subject to the higher minimum capital conservation standard", LEV_GSIB)])

# ================================================================= 14. Financial Inclusion (4 / 2 / 1)
T = "Financial Inclusion"
Q(T, "PMJDY and allied schemes", "Basic",
  "When PMJDY was extended beyond 14 August 2018, its focus for opening accounts shifted from 'every household' to:",
  ["Every unbanked adult", "Every woman in rural areas", "Every farmer with a Kisan Credit Card",
   "Every Aadhaar holder above 10 years"],
  concept="PMJDY's second phase",
  explanation="The Department of Financial Services states that PMJDY was extended beyond 14.8.2018 with the focus "
              "of account opening shifting from 'every household' to 'every unbanked adult'.",
  steps=["Phase 1 (2014): every household", "Beyond 14.8.2018: every unbanked adult"],
  why="The extension did not restrict the focus to rural women, KCC farmers or minors.",
  facts=[fact("PMJDY has been extended beyond 14.8.2018 with the focus on opening of accounts shifting from 'every "
              "household' to 'every unbanked adult'", PMJDY_DFS)])
Q(T, "Business correspondents", "Basic",
  "The 'Service Area Approach' for rural lending became operational in:",
  ["April 1989", "December 1969", "July 1982", "March 2001"],
  concept="Area approach to rural credit",
  explanation="RBI's chronology records that the Service Area Approach for rural lending became operational in April "
              "1989, building on the area approach of the Lead Bank Scheme of December 1969.",
  steps=["Lead Bank Scheme: Dec 1969", "Service Area Approach: Apr 1989"],
  why="December 1969 is the Lead Bank Scheme; July 1982 is NABARD; March 2001 is not the SAA date.",
  facts=[fact("Apr 1989: Service Area Approach for rural lending became operational", CHRON_85)])
Q(T, "Business correspondents", "Basic",
  "After the reorganisation of districts in the NCT of Delhi, RBI's circular of 26 October 2026 assigned lead bank "
  "responsibility for the new district of Old Delhi to:",
  ["Canara Bank", "State Bank of India", "Punjab National Bank", "Bank of Baroda"],
  concept="Lead Bank Scheme",
  explanation="Delhi formed three new districts — Old Delhi, Central North and Outer North — and Shahdara district "
              "ceased to exist. RBI assigned lead bank responsibility for Old Delhi to Canara Bank, Central North to "
              "SBI and Outer North to PNB.",
  steps=["Old Delhi → Canara Bank", "Central North → SBI", "Outer North → PNB"],
  why="SBI and PNB got Central North and Outer North; Bank of Baroda's responsibility for Shahdara was revoked.",
  current=ca("2026-10-26"),
  facts=[fact("Lead Bank responsibilities in the newly created districts: Old Delhi - Canara Bank; Central North - "
              "State Bank of India; Outer North - Punjab National Bank", DELHI_LB)])
Q(T, "PMJDY and allied schemes", "Basic",
  "Which free card, with in-built accident insurance cover, is provided to PMJDY account holders?",
  ["RuPay debit card", "Visa credit card", "Kisan Credit Card", "National Common Mobility Card only"],
  concept="PMJDY features",
  explanation="PMJDY offers a BSBD account with no minimum balance, a free RuPay debit card with in-built accident "
              "insurance cover, an overdraft of up to ₹10,000 subject to eligibility, and financial literacy.",
  steps=["PMJDY card = free RuPay debit card with accident cover"],
  why="PMJDY does not give credit cards, KCCs or only NCMC cards.",
  facts=[fact("Free RuPay debit card, with in-built accident insurance cover of Rs. 2 lakh", PMJDY_DFS)])
Q(T, "PMJDY and allied schemes", "Intermediate",
  "The National Strategy for Financial Inclusion 2019-24, released in January 2020, set out its goals through six "
  "strategic pillars and how many milestones?",
  ["18", "47", "5", "24"],
  concept="NSFI 2019-24",
  explanation="RBI's NSFI 2025-30 document recalls that NSFI 2019-24, released in January 2020, aimed to achieve its "
              "goals through six strategic pillars and 18 milestones. NSFI 2025-30 instead has five strategic "
              "objectives and 47 action points.",
  steps=["NSFI 2019-24: 6 pillars, 18 milestones", "NSFI 2025-30: 5 objectives, 47 action points"],
  why="47 is the number of action points in NSFI 2025-30; 5 is its number of objectives; 24 is not a figure in "
      "either.",
  facts=[fact("NSFI 2019-24... to achieve through a set of six strategic pillars and 18 milestones; released in "
              "January 2020", NSFI)])
Q(T, "Business correspondents", "Intermediate",
  "Under RBI's October 2026 circular on Delhi's reorganised districts, what happened to Shahdara district's lead bank "
  "arrangement?",
  ["Shahdara ceased to exist, so Bank of Baroda's lead bank responsibility for it was revoked",
   "Shahdara was renamed Old Delhi and kept Bank of Baroda", "Shahdara was transferred to Canara Bank",
   "Shahdara was merged with Central district under SBI"],
  concept="Reassignment of lead bank responsibility",
  explanation="Since Shahdara district ceased to exist under Delhi's December 2025 gazette notification, the lead bank "
              "responsibility notified for it in 2013 (Bank of Baroda, district working code 369) stands revoked. "
              "Other existing districts keep their lead banks unless specifically changed.",
  steps=["Shahdara ceased to exist", "Bank of Baroda's responsibility revoked"],
  why="Old Delhi is a new district under Canara Bank; Shahdara was not transferred or merged in the circular.",
  current=ca("2026-10-26"),
  facts=[fact("As Shahdara district has ceased to exist, the Lead Bank responsibility notified in respect of the "
              "district (Bank of Baroda, District Working Code 369) stands revoked", DELHI_LB)])
Q(T, "Business correspondents", "Advanced",
  "Match the Delhi district with the lead bank assigned or newly assigned by RBI's circular of 26 October 2026:\n1. "
  "Central North   2. Outer North   3. Central   4. Northwest\nP. Union Bank of India   Q. State Bank of India   R. "
  "Punjab National Bank",
  ["1-Q, 2-R, 3-Q, 4-P", "1-R, 2-Q, 3-Q, 4-P", "1-Q, 2-R, 3-P, 4-Q", "1-Q, 2-P, 3-R, 4-Q"],
  concept="Lead bank assignments",
  explanation="New districts: Central North → SBI; Outer North → PNB. Reviewed existing districts: Central moved from "
              "Canara Bank to SBI; Northwest moved from PNB to Union Bank of India. So 1-Q, 2-R, 3-Q, 4-P.",
  steps=["Central North: SBI", "Outer North: PNB", "Central: SBI (was Canara)", "Northwest: Union Bank (was PNB)"],
  why="The other matchings swap SBI and PNB for the new districts or misplace Union Bank.",
  current=ca("2026-10-26"),
  facts=[fact("Central North - State Bank of India; Outer North - Punjab National Bank; Central: existing Canara Bank, "
              "newly assigned State Bank of India; Northwest: existing Punjab National Bank, newly assigned Union Bank "
              "of India", DELHI_LB)])

# ================================================================= 15. Priority Sector Lending (3 / 1 / 3)
T = "Priority Sector Lending"
Q(T, "Targets and sub-targets", "Basic",
  "Within the 18% agriculture target for domestic commercial banks, what sub-target is prescribed for lending to "
  "Non-Corporate Farmers (NCFs)?",
  ["14 per cent of ANBC or CEOBSE", "10 per cent of ANBC or CEOBSE", "8 per cent of ANBC or CEOBSE",
   "12 per cent of ANBC or CEOBSE"],
  concept="NCF sub-target",
  explanation="Under the PSL Directions, 2025, within the 18% agriculture target, 14% is prescribed for Non-Corporate "
              "Farmers, out of which 10% is for Small and Marginal Farmers.",
  steps=["Agriculture: 18%", "NCF: 14% (within 18%)", "SMF: 10% (within 14%)"],
  why="10% is the SMF sub-target; 12% is the weaker sections target; 8% is not a PSL sub-target for domestic banks.",
  facts=[fact("Agriculture 18 per cent of ANBC or CEOBSE; within this target, 14 percent is prescribed for "
              "Non-Corporate Farmers (NCFs), out of which a target of 10 percent is prescribed for SMFs", PSL_MD)])
Q(T, "Targets and sub-targets", "Basic",
  "Bank loans to borrowers for renewable energy-based power generators and public utilities qualify as priority "
  "sector up to what limit?",
  ["₹35 crore", "₹10 crore", "₹50 crore", "₹100 crore"],
  concept="Renewable energy under PSL",
  explanation="Loans up to ₹35 crore to borrowers for renewable energy-based power generators and renewable "
              "energy-based public utilities (such as street lighting and remote village electrification) are "
              "eligible for PSL. For individual households, the limit is ₹10 lakh.",
  steps=["Borrowers: up to ₹35 crore", "Individual households: up to ₹10 lakh"],
  why="₹10 crore is not the limit; ₹50 crore applies to start-ups; ₹100 crore to agri-infrastructure and food "
      "processing.",
  facts=[fact("Bank loans up to a limit of ₹35 crore to borrowers for renewable energy based power generators and for "
              "renewable energy based public utilities; for individual households, the loan limit will be ₹10 lakh",
              PSL_MD)])
Q(T, "PSLCs", "Basic",
  "Priority Sector Lending Certificates (PSLCs) are traded through:",
  ["RBI's CBS portal, e-Kuber", "NSE's debt segment", "NPCI's NACH platform", "Over the counter between bank branches"],
  concept="PSLC trading",
  explanation="The PSLC scheme states that PSLCs are traded through RBI's CBS portal (e-Kuber), where settlement of "
              "funds also takes place. There is no transfer of risks or loan assets.",
  steps=["Trading and settlement: e-Kuber"],
  why="PSLCs are not exchange-traded, not processed through NACH and not traded over the counter.",
  facts=[fact("The PSLCs will be traded through the CBS portal (e-Kuber) of RBI", PSL_MD)])
Q(T, "PSLCs", "Intermediate",
  "A bank buys a PSLC – SF/MF (small and marginal farmers). Towards which targets does it count?",
  ["SF/MF, weaker sections and NCF sub-targets, the agriculture target and the overall PSL target",
   "Only the SF/MF sub-target", "Only the overall PSL target", "The micro-enterprise sub-target and the overall target"],
  concept="Types of PSLCs",
  explanation="RBI's table on PSLCs states that PSLC – SF/MF counts for achievement of the SF/MF sub-target, weaker "
              "sections sub-target, NCF sub-target, agriculture target and the overall PSL target. PSLC – Agriculture "
              "counts for agriculture and overall; PSLC – Micro Enterprises for the micro sub-target and overall; PSLC "
              "– General for the overall target only.",
  steps=["PSLC-SF/MF → SF/MF + weaker sections + NCF + agriculture + overall"],
  why="It counts for more than the SF/MF sub-target alone; 'overall only' describes PSLC-General; micro enterprises is "
      "a different PSLC.",
  facts=[fact("PSLC - SF/MF: Achievement of SF/MF sub-target, Weaker Sections sub-target, NCF sub-target, agriculture "
              "target and overall PSL target", PSL_MD)])

anbc, ceobse = 80000, 85000
base = max(anbc, ceobse)
ncf, smf = 0.14 * base, 0.10 * base
assert (round(ncf), round(smf)) == (11900, 8500)
Q(T, "Targets and sub-targets", "Advanced",
  "A domestic commercial bank has ANBC of ₹80,000 crore and CEOBSE of ₹85,000 crore for the relevant date. What are "
  "its Non-Corporate Farmers (NCF) and Small and Marginal Farmers (SMF) sub-targets?",
  ["NCF ₹11,900 crore; SMF ₹8,500 crore", "NCF ₹11,200 crore; SMF ₹8,000 crore", "NCF ₹15,300 crore; SMF ₹8,500 crore",
   "NCF ₹8,500 crore; SMF ₹11,900 crore"],
  concept="Computing PSL sub-targets",
  explanation="Targets are computed on ANBC or CEOBSE, whichever is higher: ₹85,000 crore. NCF = 14% × 85,000 = "
              "₹11,900 crore; SMF = 10% × 85,000 = ₹8,500 crore.",
  steps=["Base = max(80,000, 85,000) = 85,000", "NCF = 14% → 11,900", "SMF = 10% → 8,500"],
  why="₹11,200/₹8,000 crore use ANBC; ₹15,300 crore is the 18% agriculture target; the last option swaps the two.",
  computed=True,
  facts=[fact("18 per cent of ANBC or CEOBSE, whichever is higher; within this target, 14 percent for NCFs, out of "
              "which 10 percent for SMFs", PSL_MD)])

rrb_anbc, rrb_capped_loans, rrb_other = 10000, 2200, 5600
counted = min(rrb_capped_loans, 0.15 * rrb_anbc) + rrb_other
assert counted == 7100 and 0.75 * rrb_anbc - counted == 400
Q(T, "Targets and sub-targets", "Advanced",
  "An RRB has ANBC of ₹10,000 crore (higher than its CEOBSE). Its priority sector loans include ₹2,200 crore to medium "
  "enterprises, social infrastructure and renewable energy taken together, and ₹5,600 crore to other priority "
  "sectors. What is its position against the overall PSL target?",
  ["Short by ₹400 crore", "Surplus of ₹300 crore", "Exactly on target", "Short by ₹1,900 crore"],
  concept="RRB target and its cap",
  explanation="RRBs must lend 75% of ANBC = ₹7,500 crore. Loans to medium enterprises, social infrastructure and "
              "renewable energy count only up to 15% of ANBC = ₹1,500 crore. Achievement = 1,500 + 5,600 = ₹7,100 "
              "crore, so the shortfall is ₹400 crore.",
  steps=["Target = 75% × 10,000 = 7,500", "Capped portion = min(2,200, 1,500) = 1,500",
         "Achievement = 1,500 + 5,600 = 7,100", "Shortfall = 400"],
  why="A ₹300 crore surplus ignores the 15% cap; the bank is not on target; ₹1,900 crore excludes the capped loans "
      "entirely.",
  computed=True,
  facts=[fact("RRBs: 75 per cent of ANBC or CEOBSE; lending to Medium Enterprises, Social Infrastructure and Renewable "
              "Energy shall be reckoned for priority sector achievement up to 15 per cent of ANBC only", PSL_MD)])

loans = {"P": (80, "eNWR"), "Q": (70, "WR"), "R": (55, "WR"), "S": (95, "NWR")}
ok = [k for k, (amt, kind) in loans.items() if amt <= (90 if kind in ("NWR", "eNWR") else 60)]
assert ok == ["P", "R"]
Q(T, "Targets and sub-targets", "Advanced",
  "Four individual farmers take six-month loans against pledge of their agricultural produce: (P) ₹80 lakh against an "
  "electronic negotiable warehouse receipt (eNWR); (Q) ₹70 lakh against an ordinary warehouse receipt; (R) ₹55 lakh "
  "against an ordinary warehouse receipt; (S) ₹95 lakh against a negotiable warehouse receipt (NWR). Which qualify "
  "as priority sector (agriculture)?",
  ["P and R only", "P, R and S only", "R only", "P, Q, R and S"],
  concept="Loans against warehouse receipts",
  explanation="For farmers, loans against pledge of produce for up to 12 months qualify up to ₹90 lakh against "
              "NWRs/eNWRs and up to ₹60 lakh against other warehouse receipts. P (₹80 lakh, eNWR) and R (₹55 lakh, "
              "ordinary) qualify; Q (₹70 lakh > ₹60 lakh) and S (₹95 lakh > ₹90 lakh) do not.",
  steps=["NWR/eNWR cap ₹90 lakh: P yes, S no", "Other WR cap ₹60 lakh: R yes, Q no"],
  why="S exceeds the ₹90 lakh limit; P also qualifies; Q exceeds the ₹60 lakh limit.",
  computed=True,
  facts=[fact("Loans against pledge/hypothecation of agricultural produce (including warehouse receipts) for a period "
              "not exceeding 12 months subject to a limit up to ₹90 lakh against NWRs/eNWRs and up to ₹60 lakh against "
              "warehouse receipts other than NWRs/eNWRs", PSL_MD)])

# ================================================================= 16. RBI Integrated Ombudsman Scheme (2 / 3 / 3)
T = "RBI Integrated Ombudsman Scheme"
RBIOS = ca("2026-07-01")
Q(T, "Scope and grounds", "Basic",
  "Complaints under RB-IOS, 2026 are handled jurisdiction-neutrally under which approach?",
  ["One Nation One Ombudsman", "One District One Ombudsman", "Single Window Banking", "Digital India Grievance"],
  concept="Jurisdiction-neutral handling",
  explanation="RBI lists among the benefits of RB-IOS, 2026 the jurisdiction-neutral handling of complaints under the "
              "'One Nation One Ombudsman' approach, with a single portal (cms.rbi.org.in) for online complaints and "
              "the CRPC for e-mail and physical complaints.",
  steps=["Jurisdiction-neutral → 'One Nation One Ombudsman'"],
  why="The other phrases are not the approach named in the Scheme's FAQs.",
  current=RBIOS,
  facts=[fact("Jurisdiction-neutral handling of complaints under the 'One Nation One Ombudsman' approach", RBIOS_FAQ)])
Q(T, "Process and limits", "Basic",
  "Under which scheme will a complaint received by the RBI Ombudsman before 1 July 2026 continue to be governed?",
  ["Reserve Bank – Integrated Ombudsman Scheme, 2021", "Reserve Bank – Integrated Ombudsman Scheme, 2026",
   "Banking Ombudsman Scheme, 2006", "Consumer Protection Act, 2019"],
  concept="Transition to RB-IOS, 2026",
  explanation="RB-IOS, 2026 replaces RB-IOS, 2021 from 1 July 2026. Complaints received before 1 July 2026, appeals "
              "arising from decisions under RB-IOS, 2021, and execution of awards under it continue to be governed by "
              "RB-IOS, 2021.",
  steps=["Received before 1 Jul 2026 → RB-IOS, 2021", "From 1 Jul 2026 → RB-IOS, 2026"],
  why="The 2026 Scheme applies to complaints from 1 July 2026; the 2006 scheme and the Consumer Protection Act do not "
      "govern these complaints.",
  current=RBIOS,
  facts=[fact("RB-IOS, 2026 replaces RB-IOS, 2021. Complaints received before July 1, 2026... will continue to be "
              "governed by RB-IOS, 2021", RBIOS_FAQ)])
Q(T, "Process and limits", "Intermediate",
  "Under RB-IOS, 2026, what can an RBI Deputy Ombudsman do?",
  ["Consider complaints and close or reject them to the extent permitted, and help the parties reach a settlement",
   "Pass Awards with compensation up to ₹30 lakh", "Hear appeals against Awards of the Ombudsman",
   "Impose monetary penalties on banks"],
  concept="Role of the Deputy Ombudsman",
  explanation="A Deputy Ombudsman assists in carrying out the Scheme: it can consider complaints of deficiency in "
              "service, close or reject them to the extent permitted, and the Ombudsman or Deputy Ombudsman may help "
              "the parties reach a settlement through facilitation, advice or conciliation. Awards are passed by the "
              "RBI Ombudsman.",
  steps=["Deputy Ombudsman: consider, close/reject, facilitate settlement", "Award: RBI Ombudsman only"],
  why="Awards are the Ombudsman's power; appeals go to the Appellate Authority; penalties are not imposed under the "
      "Scheme.",
  current=RBIOS,
  facts=[fact("The RBI Deputy Ombudsman can consider complaints relating to deficiency in service and can close/reject "
              "complaints to the extent permitted under the Scheme; the RBI Ombudsman or RBI Deputy Ombudsman may help "
              "the complainant and the RE arrive at a mutually acceptable resolution; if not settled, an Award may be "
              "passed by the RBI Ombudsman", RBIOS_FAQ)])
Q(T, "Process and limits", "Intermediate",
  "Within RBI's Alternate Grievance Redress (AGR) Framework, which unit assists the Appellate Authority and processes "
  "appeal cases?",
  ["Consumer Education and Protection Department (CEPD)", "Centralised Receipt and Processing Centre (CRPC)",
   "Department of Supervision", "The Contact Centre (14448)"],
  concept="AGR Framework",
  explanation="The AGR Framework comprises the Offices of RBI Ombudsman, the CRPC, Consumer Education and Protection "
              "Cells and the Consumer Education and Protection Department. CEPD provides assistance to the Appellate "
              "Authority and processes the appeal cases.",
  steps=["AGR = Ombudsman offices + CRPC + CEPCs + CEPD", "Appeals → CEPD assists the Appellate Authority"],
  why="The CRPC receives e-mail and physical complaints; the Contact Centre only guides; the Department of Supervision "
      "is not part of the AGR appeal process.",
  current=RBIOS,
  facts=[fact("The AGR Framework comprises the Offices of RBI Ombudsman, CRPC, CEPCs and CEPD. CEPD provides "
              "assistance to the Appellate Authority (AA) and processes the appeal cases", RBIOS_FAQ)])
Q(T, "Scope and grounds", "Intermediate",
  "Which of the following complaints would be non-maintainable under RB-IOS, 2026?",
  ["A grievance that the bank rejected a loan application as a matter of its commercial judgment",
   "A grievance that the bank did not reverse a failed ATM debit within the prescribed time",
   "A grievance about charges levied without prior notice",
   "A grievance that a cheque was returned without a valid reason"],
  concept="Grounds of non-maintainability",
  explanation="Matters relating to the commercial judgment or commercial decision of a Regulated Entity are "
              "non-maintainable, as are grievances against the management or executives, employer-employee disputes "
              "and actions taken in compliance with orders of authorities. The other three are deficiencies in "
              "service that can be examined.",
  steps=["Commercial judgment/decision → not maintainable", "Service deficiencies → maintainable"],
  why="Failed-transaction reversal, undisclosed charges and wrongful cheque returns are deficiencies in service.",
  current=RBIOS,
  facts=[fact("Not maintainable: matters relating to commercial judgment or decision of a Regulated Entity; grievances "
              "against Management or Executives; disputes involving employee-employer relationship", RBIOS_FAQ)])
Q(T, "Scope and grounds", "Advanced",
  "Meena's grievance about an unauthorised debit is the subject of a police investigation that she started against an "
  "unknown fraudster. Separately, Ravi's grievance on the same issue with his bank is pending before a civil court. "
  "Under RB-IOS, 2026, which complaint can be maintainable before the RBI Ombudsman (other conditions being met)?",
  ["Meena's only", "Ravi's only", "Both", "Neither"],
  concept="Same grievance before other forums",
  explanation="A complaint is non-maintainable if the same grievance is pending before, or settled on merits by, a "
              "court, tribunal, arbitrator or other judicial/quasi-judicial forum. But criminal proceedings pending "
              "or decided, or a police investigation into a criminal offence, are not treated as the same grievance. "
              "So Meena's complaint can proceed; Ravi's cannot.",
  steps=["Ravi: same grievance pending in civil court → not maintainable",
         "Meena: police investigation → not treated as same grievance → maintainable"],
  why="Ravi's civil case bars his complaint; Meena's police case does not bar hers.",
  current=RBIOS,
  facts=[fact("Complaints relating to the same grievance pending before, or settled/dealt with on merits by, any "
              "Court, Tribunal, Arbitrator or other judicial/quasi-judicial forum are not maintainable. Criminal "
              "proceedings pending or decided before a Court or Tribunal or police investigation initiated in a "
              "criminal offence are not treated as the same grievance", RBIOS_FAQ)])
Q(T, "Scope and grounds", "Advanced",
  "Consider the following statements about RB-IOS, 2026:\nI. 'Deficiency in service' covers a shortcoming in a service "
  "the RE must provide, whether or not it causes financial loss to the customer.\nII. Conciliation meetings may be "
  "attended by the parties in person or online.\nIII. A complaint is maintainable even if the customer first "
  "complained to the RE after the limitation period under the Limitation Act, 1963 had expired.\nWhich of the above "
  "is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Definitions and procedure",
  explanation="RB-IOS, 2026 defines deficiency in service as a shortcoming or inadequacy in a service the RE must "
              "provide, which may or may not result in financial loss (I correct). Conciliation meetings may be held "
              "with parties participating in person or online (II correct). A complaint where the complaint to the RE "
              "was made after the limitation period is not maintainable (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong"],
  why="III is a ground for non-maintainability, so options with III fail; 'I only' omits II.",
  current=RBIOS,
  facts=[fact("'Deficiency in service' means a shortcoming or inadequacy in any service... which may or may not result "
              "in financial loss; a conciliation meeting may be held with the parties participating in person or "
              "online; complaints where the complaint to the RE was made after expiry of the limitation period under "
              "the Limitation Act, 1963 are not maintainable", RBIOS_FAQ)])

lodged = dt.date(2026, 8, 1)
can_approach = lodged + dt.timedelta(days=45)
last_day = can_approach + dt.timedelta(days=90)
assert (can_approach, last_day) == (dt.date(2026, 9, 15), dt.date(2026, 12, 14))
Q(T, "Process and limits", "Advanced",
  "Arjun complained to his card issuer on 1 August 2026 about a disputed card transaction for which the card "
  "network's guidelines allow 45 days for resolution. He gets no reply. Under RB-IOS, 2026, from when can he approach "
  "the RBI Ombudsman, and by when must he do so?",
  ["After 15 September 2026; by 14 December 2026", "After 31 August 2026; by 29 November 2026",
   "After 15 September 2026; by 15 October 2026", "Immediately; by 30 October 2026"],
  concept="Timelines when a network TAT applies",
  explanation="A complaint can be filed if no reply is received within 30 days or the time specified by RBI, NPCI or "
              "card network guidelines, whichever is higher — here 45 days, ending 15 September 2026. It must be filed "
              "within 90 days from the date that timeline expires: 15 September + 90 days = 14 December 2026.",
  steps=["max(30, 45) = 45 days → 15 Sep 2026", "15 Sep + 90 days = 14 Dec 2026"],
  why="The 30-day dates ignore the longer network timeline; 30 days after expiry is not the limit; he must first wait "
      "for the timeline.",
  computed=True, current=RBIOS,
  facts=[fact("A complaint can be filed if the complainant has not received any reply within 30 days or within the "
              "time specified by RBI, NPCI or Card Network guidelines, whichever is higher; the complaint must be "
              "made within 90 days from the date on which the above timeline expires", RBIOS_FAQ)])

# ================================================================= 17. Digital Banking (1 / 3 / 3)
T = "Digital Banking"
Q(T, "CBDC (e-rupee)", "Basic",
  "In which denominations is the retail digital rupee (e₹) available in a user's wallet?",
  ["The same denominations as physical currency", "Only ₹1 units", "Only ₹100 and ₹500 units",
   "Any amount, with no denominations"],
  concept="e₹ denominations",
  explanation="RBI states that, for ease of use, e₹ is available in the same denominations as physical currency, "
              "giving users the familiarity of currency notes. Wallets automatically handle change, and payments can "
              "be made up to two decimal places.",
  steps=["e₹ denominations = physical currency denominations"],
  why="e₹ is not limited to ₹1 units or to high denominations; it does have denominations, like cash.",
  facts=[fact("For ease of use, e₹ is available in the same denominations as physical currency", ERUPEE_FAQ)])
Q(T, "CBDC (e-rupee)", "Intermediate",
  "RBI's 'CAT Sandbox', which gives entities a non-live environment to test CBDC-related use cases, stands for:",
  ["CBDC and Asset Tokenisation Sandbox", "Card and Authentication Testing Sandbox",
   "Central Accounts and Treasury Sandbox", "Cross-border Automated Transfer Sandbox"],
  concept="Innovation around the e₹",
  explanation="The CBDC and Asset Tokenisation (CAT) Sandbox aims to foster innovation in payments, settlements and "
              "CBDC-enabled services across retail, wholesale, cross-border and asset tokenisation domains, in a "
              "secure non-live environment. Requests go to RBI's FinTech Department.",
  steps=["CAT = CBDC and Asset Tokenisation"],
  why="The other expansions are not RBI's sandbox.",
  facts=[fact("The CBDC and Asset Tokenisation (CAT) Sandbox aims to foster innovation in payments, settlements, and "
              "CBDC-enabled financial services... secure, non-live environment; requests to the FinTech Department, "
              "RBI", ERUPEE_FAQ)])
Q(T, "Mobile and internet banking", "Intermediate",
  "What did RBI announce on 7 October 2026 regarding the Account Aggregator (AA) framework, to be implemented by 31 "
  "December 2026?",
  ["Interoperability among NBFC-AAs, and inclusion of bank deposit information in depositories' Consolidated Account "
   "Statement through AAs",
   "Merger of all NBFC-AAs into a single RBI-run aggregator", "A ban on sharing deposit data with depositories",
   "Mandatory AA registration for every savings account holder"],
  concept="Account Aggregators",
  explanation="RBI decided to implement interoperability among NBFC-AAs so customers can share financial information "
              "across providers through any AA of their choice, and to let SEBI-regulated depositories include bank "
              "deposit information in the Consolidated Account Statement through AAs. Both are to be implemented by "
              "31 December 2026.",
  steps=["Interoperability among NBFC-AAs", "Bank deposit data in CAS via AAs", "Target: 31 Dec 2026"],
  why="AAs are not being merged; deposit data sharing is being enabled, not banned; AA use is not made mandatory.",
  current=ca("2026-10-07"),
  facts=[fact("It has been decided to implement interoperability among NBFC-AAs; Depositories regulated by SEBI are "
              "being facilitated to include information related to bank deposit accounts in their CAS through the "
              "NBFC-AAs; expected to be implemented by December 31, 2026", SDRP_OCT26)])
Q(T, "Digital lending", "Intermediate",
  "Under the RBI (Digital Lending) Directions, 2025, when a lending service provider (LSP) has arrangements with "
  "several lenders, what must its digital view of loan offers show?",
  ["All matching loan offers, with the names of unmatched lenders also disclosed",
   "Only the offer of the lender paying the highest fee", "Only the lowest-rate offer, without lender names",
   "Offers ranked solely by the LSP's commission"],
  concept="Multi-lender LSPs",
  explanation="An LSP with multiple lenders must provide a digital view of all loan offers matching the borrower's "
              "request, disclose the names of unmatched lenders, show details such as APR and monthly repayment, and "
              "keep the content unbiased, without dark patterns that push a particular lender.",
  steps=["Show all matching offers", "Disclose unmatched lenders", "No dark patterns"],
  why="Promoting the highest-fee or commission-based offer is prohibited; lender names must be shown.",
  facts=[fact("LSP shall provide a digital view of all the loan offers matching the borrower's request; the name of the "
              "unmatched lenders shall also be disclosed; content shall be unbiased and shall not use dark patterns",
              DL_2025)])
Q(T, "CBDC (e-rupee)", "Advanced",
  "Consider the following statements about the retail e₹ as described in RBI's FAQs:\nI. A P2P or P2M payment made "
  "at a CBDC QR code moves between two e₹ wallets and settles instantly without passing through the users' bank "
  "accounts.\nII. When a UPI QR is scanned from an e₹ app, settlement follows UPI settlement timelines.\nIII. e₹ "
  "payments must be in whole rupees.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Settlement of e₹ payments",
  explanation="RBI states that P2P and P2M payments at a CBDC QR happen between two e₹ wallets and settle "
              "instantaneously without passing through bank accounts (I correct); payments made by scanning a UPI QR "
              "from an e₹ app settle on UPI timelines (II correct); e₹ supports payments up to two decimal places "
              "(III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (decimals allowed)"],
  why="III is false, so options including it are wrong; 'I only' omits II.",
  facts=[fact("Payments at any CBDC QR happen between two e₹ wallets and are settled instantaneously without passing "
              "through user's bank accounts; scanning a UPI QR from an e₹ app settles on UPI settlement timelines; "
              "e₹ supports payments up to two decimal places", ERUPEE_FAQ)])
Q(T, "Digital lending", "Advanced",
  "Consider the following statements under the RBI (Digital Lending) Directions, 2025:\nI. Lending through digital "
  "lending apps must be reported to credit information companies irrespective of its nature or tenor.\nII. "
  "Short-term deferred payment ('buy now, pay later') products offered over merchant platforms need not be reported "
  "to CICs.\nIII. If a borrower's complaint gets no reply from the lender within 30 days, the borrower can complain "
  "under the RB-IOS.\nWhich of the above is/are correct?",
  ["I and III only", "I only", "II and III only", "I, II and III"],
  concept="Credit reporting and grievances in digital lending",
  explanation="Lending through DLAs must be reported to CICs irrespective of nature or tenor (I correct). Structured "
              "digital lending products over merchant platforms involving short-term credits or deferred payments "
              "must also be reported to CICs (II wrong). If the RE rejects a complaint or does not reply within 30 "
              "days, the borrower can complain under RB-IOS (III correct).",
  steps=["I: correct", "II: wrong (must be reported)", "III: correct"],
  why="II contradicts the Directions; 'I only' omits III.",
  facts=[fact("RE shall ensure that any lending done through DLAs is reported to CICs irrespective of its nature/tenor; "
              "structured digital lending products over a merchant platform involving short term credits or deferred "
              "payments need to be reported to CICs; if no reply within 30 days, the borrower can lodge a complaint "
              "under RB-IOS", DL_2025)])
Q(T, "Mobile and internet banking", "Advanced",
  "Under RBI's Digital Banking Channels Authorisation Directions, 2025, which statement about a 'view only' digital "
  "banking facility is correct?",
  ["A bank with CBS and IPv6-enabled public-facing IT may launch it without prior approval, intimating RBI within 30 "
   "days with a GAICA report",
   "It needs RBI's prior approval through PRAVAAH, like a transactional facility",
   "It may offer fund transfers but not loans", "Only banks with a net worth above ₹1,000 crore may offer it"],
  concept="View-only versus transactional facilities",
  explanation="View-only facilities allow only services that do not change the customer's assets or liabilities "
              "(balance, statements). Banks with CBS and IPv6-enabled public-facing IT are eligible, and must "
              "intimate RBI through PRAVAAH, with a Gap Assessment and Internal Controls Adequacy (GAICA) report, "
              "within 30 days of deciding to launch. Prior approval is needed only for transactional facilities.",
  steps=["Eligibility: CBS + IPv6", "Intimation within 30 days with GAICA report", "No funds transfer or loans"],
  why="Prior approval applies to transactional facilities; fund transfers are excluded from view-only; no ₹1,000 "
      "crore net worth test exists.",
  facts=[fact("All banks which have implemented CBS and have enabled their public facing IT infrastructure to handle "
              "IPv6 traffic are eligible to provide view only banking facility; shall intimate the Department of "
              "Regulation through PRAVAAH, along with a copy of the GAICA report, within thirty days; loans and funds "
              "transfers cannot be provided with view only facility", DBC_MD)])

# ================================================================= 18. UPI (2 / 5 / 1)
T = "UPI"
PSR = ca("2026-05-18")
Q(T, "Features", "Basic",
  "According to RBI's Payment System Report of May 2026, what share of the total volume of payment transactions in "
  "the second half of calendar year 2025 was accounted for by UPI?",
  ["85.5 per cent", "68.6 per cent", "9.5 per cent", "3.6 per cent"],
  concept="UPI's dominance by volume",
  explanation="In H2 of CY 2025, UPI accounted for 85.5% of transaction volume, followed by NEFT and PPIs (3.6% each), "
              "with RTGS at 0.1%. By value, RTGS dominated with 68.6%, NEFT 14.9% and UPI 9.5%.",
  steps=["UPI volume share: 85.5%", "UPI value share: 9.5%"],
  why="68.6% is RTGS's value share; 9.5% is UPI's value share; 3.6% is NEFT's or PPIs' volume share.",
  current=PSR,
  facts=[fact("In H2 of CY 2025, UPI commanded the largest share of transaction volume at 85.5 per cent... RTGS "
              "dominated value with 68.6 per cent... UPI at 9.5 per cent", PSR_MAY26)])
Q(T, "Features", "Basic",
  "Which UPI-based innovation, listed by RBI alongside UPI 123Pay and UPI Circle, enables cardless cash withdrawals?",
  ["UPI-ATM", "Hello UPI", "UPI Lite", "BHIM Aadhaar Pay"],
  concept="UPI innovations",
  explanation="RBI's Payment System Report lists innovations that expanded UPI: UPI 123Pay for feature phones, Hello "
              "UPI for voice payments, UPI-ATM for cardless cash withdrawals, Credit Card on UPI and UPI Circle.",
  steps=["Cardless cash withdrawal → UPI-ATM"],
  why="Hello UPI is voice-based payments; UPI Lite is for small-value on-device payments; BHIM Aadhaar Pay is a "
      "merchant payment mode.",
  current=PSR,
  facts=[fact("Innovations such as UPI 123Pay (for feature phones), Hello UPI (voice-enabled payments), UPI-ATM "
              "(cardless cash withdrawals), Credit Card on UPI, and UPI Circle", PSR_MAY26)])
Q(T, "Features", "Intermediate",
  "According to RBI's Payment System Report of May 2026, the number of UPI transactions rose from 3,873 crore in CY "
  "2021 to how many in CY 2025?",
  ["22,828 crore", "12,828 crore", "30,000 crore", "8,500 crore"],
  concept="Growth of UPI",
  explanation="UPI volumes grew from 3,873 crore transactions in CY 2021 to 22,828 crore in CY 2025, and value from "
              "₹72 lakh crore to ₹300 lakh crore — a CAGR of 55.8% in volume and 43% in value.",
  steps=["CY 2021: 3,873 crore", "CY 2025: 22,828 crore"],
  why="The other figures do not match RBI's data.",
  current=PSR,
  facts=[fact("The volume of UPI transactions has increased from 3,873 crore transactions in CY 2021 to 22,828 crore "
              "transactions in CY 2025; value grew from ₹72 lakh crore to ₹300 lakh crore", PSR_MAY26)])
Q(T, "UPI Lite and international", "Intermediate",
  "Which multilateral initiative for international remittances does RBI mention alongside bilateral links between UPI "
  "and other countries' fast payment systems?",
  ["Project Nexus", "Project mBridge only for CBDCs", "SWIFT gpi", "Project Hertha"],
  concept="Cross-border UPI",
  explanation="RBI's report says UPI and Singapore's PayNow have been linked since February 2023, similar bilateral "
              "integrations are under way, and the multilateral Project Nexus is ongoing for international "
              "remittances.",
  steps=["Bilateral: UPI–PayNow (Feb 2023)", "Multilateral: Project Nexus"],
  why="The other names are not the multilateral fast-payment initiative named by RBI.",
  current=PSR,
  facts=[fact("Similar integrations with other national fast payment systems are currently underway, alongside the "
              "ongoing multilateral Project Nexus for international remittances", PSR_MAY26)])
Q(T, "Features", "Intermediate",
  "What compound annual growth rates did UPI record from CY 2021 to CY 2025, according to RBI?",
  ["55.8% in volume and 43% in value", "43% in volume and 55.8% in value", "33% in volume and 17% in value",
   "18.1% in volume and 4.5% in value"],
  concept="UPI growth rates",
  explanation="RBI's report gives UPI's CAGR over CY 2021–2025 as 55.8% in volume and 43% in value. The 43%/17% pair "
              "is the CAGR for all digital payments over the last five years, and 4.5%/18.1% is IMPS.",
  steps=["UPI CAGR: volume 55.8%, value 43%"],
  why="The second option swaps the two; the other pairs belong to overall digital payments or IMPS.",
  current=PSR,
  facts=[fact("The CAGR of the UPI transaction during this period is 55.8 per cent in terms of volume and 43 per cent "
              "in terms of value", PSR_MAY26)])
Q(T, "Features", "Intermediate",
  "In UPI and IMPS, funds reach the beneficiary immediately. How is the inter-bank settlement done?",
  ["Later, on a deferred net basis according to a pre-defined settlement cycle",
   "Gross and in real time in RBI's books for each transaction", "Once a month through NACH",
   "Only when the beneficiary withdraws cash"],
  concept="Deferred net settlement",
  explanation="RBI explains that in systems like UPI and IMPS the beneficiary is credited immediately, while the "
              "inter-bank settlement happens later according to a pre-defined settlement cycle — deferred net "
              "settlement. In RTGS, by contrast, each transaction settles gross and in real time.",
  steps=["Customer credit: immediate", "Bank-to-bank settlement: deferred, netted"],
  why="Gross real-time settlement describes RTGS; NACH and cash withdrawal are irrelevant.",
  facts=[fact("In a few systems like UPI and IMPS, while funds are credited to the beneficiary customer immediately, "
              "the inter-bank settlement is done later according to a pre-defined settlement cycle... Deferred "
              "Settlement", PAY_BOOKLET)])

upi_value_lakh_cr, upi_vol_cr = 300, 22828
ticket = upi_value_lakh_cr * 1e5 / upi_vol_cr
assert round(ticket) == 1314 and abs(ticket - 1313) < 2
Q(T, "Features", "Advanced",
  "UPI processed 22,828 crore transactions worth ₹300 lakh crore in CY 2025. What is the approximate average ticket "
  "size, and how does it compare with CY 2021, when it was ₹1,848?",
  ["About ₹1,314, lower than in 2021", "About ₹13,140, higher than in 2021", "About ₹1,314, higher than in 2021",
   "About ₹131, lower than in 2021"],
  concept="Average ticket size",
  explanation="₹300 lakh crore = 300 × 10⁵ crore = 3,00,00,000 crore rupees. Dividing by 22,828 crore transactions "
              "gives ≈ ₹1,314 per transaction (RBI reports ₹1,313). This is below ₹1,848 in CY 2021, showing UPI's "
              "growing use for small payments.",
  steps=["300 lakh crore ÷ 22,828 crore = 3,00,00,000 ÷ 22,828 ≈ 1,314", "1,314 < 1,848 → lower"],
  why="₹13,140 and ₹131 misplace the decimal; ₹1,314 is lower, not higher, than ₹1,848.",
  computed=True, current=PSR,
  facts=[fact("Total value ₹300 lakh crore in CY 2025; 22,828 crore transactions; average ticket size declined from "
              "₹1,848 in CY 2021 to ₹1313 in CY 2025", PSR_MAY26)])
Q(T, "Features", "Intermediate",
  "By value, UPI accounted for only 9.5% of payment transactions in H2 of CY 2025. Which systems ranked above it by "
  "value?",
  ["RTGS (68.6%) and NEFT (14.9%)", "IMPS and NACH", "PPIs and cards", "No system; UPI ranked first by value too"],
  concept="Volume versus value",
  explanation="RBI's report shows that by value RTGS dominated with 68.6%, followed by NEFT at 14.9% and UPI at 9.5%, "
              "with PPIs at 0.1%. UPI leads by volume (85.5%) because it handles mass, small-value retail payments.",
  steps=["Value: RTGS 68.6% > NEFT 14.9% > UPI 9.5%"],
  why="IMPS, NACH, PPIs and cards were not ranked above UPI by value; UPI leads only by volume.",
  current=PSR,
  facts=[fact("In terms of transaction value, RTGS dominated with 68.6 per cent of the total transaction value, "
              "followed by NEFT at 14.9 per cent and UPI at 9.5 per cent, with PPIs contributing only 0.1 per cent",
              PSR_MAY26)])

# ================================================================= 19. NEFT (1 / 1 / 1)
T = "NEFT"
Q(T, "Settlement and timings", "Basic",
  "Who owns and operates the National Electronic Funds Transfer (NEFT) system?",
  ["Reserve Bank of India", "National Payments Corporation of India", "Indian Banks' Association", "IDRBT"],
  concept="Ownership of NEFT",
  explanation="RBI's FAQs describe NEFT as a nation-wide centralised payment system owned and operated by the Reserve "
              "Bank of India. NPCI operates retail systems such as IMPS and UPI.",
  steps=["NEFT → owned and operated by RBI"],
  why="NPCI runs IMPS/UPI/NACH; IBA and IDRBT do not operate NEFT.",
  facts=[fact("National Electronic Funds Transfer (NEFT) is a nation-wide centralised payment system owned and "
              "operated by the Reserve Bank of India (RBI)", NEFT_FAQ)])
Q(T, "Settlement and timings", "Intermediate",
  "In the NEFT transaction flow, after the originating bank prepares the payment message, where does it send it "
  "first?",
  ["To its pooling centre (NEFT Service Centre), which forwards it to RBI's NEFT Processing Centre",
   "Directly to the beneficiary bank branch", "To NPCI's central switch", "To the RTGS Member Interface for gross "
   "settlement"],
  concept="How NEFT works",
  explanation="RBI's FAQs set out the flow: the originating bank sends the message to its pooling centre (NEFT Service "
              "Centre), which forwards it to the NEFT Processing Centre operated by RBI for the next batch. The "
              "Processing Centre sorts transactions beneficiary bank-wise, passes accounting entries, and sends "
              "remittance messages to beneficiary banks through their pooling centres.",
  steps=["Bank → its NEFT Service Centre", "→ RBI's NEFT Processing Centre (batch)", "→ beneficiary bank"],
  why="Messages do not go directly to the beneficiary branch, to NPCI, or through RTGS.",
  facts=[fact("Step-2: The originating bank prepares a message and sends the message to its pooling centre, also "
              "called the NEFT Service Centre. Step-3: The pooling centre forwards the message to the NEFT Processing "
              "Centre, operated by the RBI", NEFT_FAQ)])
Q(T, "Settlement and timings", "Advanced",
  "Consider the following statements about NEFT and IFSC:\nI. NEFT can be used for transfers from and to NRE and NRO "
  "accounts, subject to FEMA and wire transfer guidelines.\nII. The remitter's name must be printed in the "
  "beneficiary's account statement or passbook.\nIII. RBI allocates every branch-level IFSC itself; banks cannot "
  "create additional IFSCs.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="NEFT features and IFSC allocation",
  explanation="NEFT may be used for NRE/NRO accounts subject to FEMA (I correct), and the remitter's name shall be "
              "printed in the beneficiary's statement/passbook (II correct). Since core banking, RBI allocates only "
              "the primary IFSC (bank code); banks create, modify or delete additional IFSCs for their branches "
              "through IFTAS (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (banks create branch IFSCs via IFTAS)"],
  why="III is false, so options including it are wrong; 'I only' omits II.",
  facts=[fact("NEFT can be used to transfer funds from/to NRE and NRO accounts subject to FEMA and Wire Transfer "
              "Guidelines; the remitter's name shall be printed in the Account Statement / Pass Book of the "
              "beneficiary", NEFT_FAQ),
         fact("RBI now allocates only the primary IFSC representing bank code, and banks can create / modify / delete "
              "additional IFSCs for their own branches through IFTAS", PAY_BOOKLET)])

# ================================================================= 20. RTGS (1 / 2 / 2)
T = "RTGS"
Q(T, "Limits and timings", "Basic",
  "Why are payments through RTGS final and irrevocable?",
  ["Because funds settlement takes place in the books of RBI", "Because NPCI guarantees them",
   "Because the beneficiary must confirm each payment", "Because they are netted at the end of the day"],
  concept="Finality in RTGS",
  explanation="RBI's FAQs state that since the funds settlement takes place in the books of the Reserve Bank of "
              "India, RTGS payments are final and irrevocable.",
  steps=["Settlement in RBI's books → final and irrevocable"],
  why="NPCI does not run RTGS; beneficiaries do not confirm; RTGS settles gross, without netting.",
  facts=[fact("Considering that the funds settlement takes place in the books of the RBI, the payments are final and "
              "irrevocable", RTGS_FAQ)])
Q(T, "Limits and timings", "Intermediate",
  "What is the 'positive confirmation' feature in RTGS?",
  ["The beneficiary bank sends an acknowledgement of credit, passed to the remitting bank through RTGS/SFMS so it can "
   "inform its customer",
   "The remitter confirms the beneficiary's name before sending", "RBI confirms every payment by SMS to the "
   "beneficiary", "The receiving bank confirms the payment before it is settled"],
  concept="Credit confirmation",
  explanation="Positive confirmation is a facility under which the beneficiary bank sends an acknowledgement of credit "
              "to the beneficiary account; it is communicated to the remitting bank through the RTGS/SFMS messaging "
              "arrangement, so the remitting bank can tell its customer the money has been credited.",
  steps=["Beneficiary bank credits account", "Acknowledgement → remitting bank", "Remitter informed"],
  why="Name verification before sending is the account name look-up facility; RBI does not SMS beneficiaries; "
      "confirmation follows the credit, not settlement.",
  facts=[fact("Positive confirmation is a facility under which the beneficiary bank sends an acknowledgement of credit "
              "to the beneficiary account. The acknowledgement is communicated to the remitting bank through the "
              "RTGS/SFMS messaging arrangement", RTGS_FAQ)])
Q(T, "Limits and timings", "Intermediate",
  "According to RBI's Payment System Report (May 2026), RTGS accounted for what share of payment transaction value "
  "and volume in H2 of CY 2025?",
  ["68.6% of value but only 0.1% of volume", "85.5% of value and 68.6% of volume", "14.9% of value and 3.6% of volume",
   "9.5% of value and 85.5% of volume"],
  concept="RTGS as a high-value system",
  explanation="RTGS handled 68.6% of the value of payment transactions in H2 2025 but only 0.1% of volume, reflecting "
              "its role as a high-value, low-volume system.",
  steps=["Value share 68.6%", "Volume share 0.1%"],
  why="85.5% is UPI's volume; 14.9%/3.6% are NEFT's shares; 9.5%/85.5% are UPI's.",
  current=PSR,
  facts=[fact("RTGS accounted for a mere 0.1 per cent [of volume]... in terms of transaction value, RTGS dominated with "
              "68.6 per cent of the total transaction value", PSR_MAY26)])
Q(T, "Limits and timings", "Advanced",
  "Consider the following statements from RBI's RTGS FAQs:\nI. The beneficiary bank account name look-up facility "
  "lets a remitter verify the beneficiary's name as registered in the bank's CBS before transferring funds, and it is "
  "free.\nII. RTGS members must use prescribed transaction type codes for transactions under the Foreign Contribution "
  "(Regulation) Act, 2010.\nIII. Compensation for a delayed return of an RTGS payment is calculated at the Bank Rate "
  "plus 2%.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="RTGS safeguards",
  explanation="The name look-up facility is free and lets a remitter verify the account holder's name before "
              "transferring (I correct). Prescribed transaction type codes must be used for FCRA transactions (II "
              "correct). Compensation for delay is at the current repo rate plus 2%, not the Bank Rate plus 2% (III "
              "wrong).",
  steps=["I: correct", "II: correct", "III: wrong (repo + 2%)"],
  why="III uses the wrong benchmark, so options including it fail; 'I only' omits II.",
  facts=[fact("Beneficiary bank account name look-up facility is a free facility which allows a remitter to verify the "
              "beneficiary bank's account holder's name before initiating a fund transfer; RTGS members must use the "
              "prescribed transaction type codes for FCRA transactions; compensation at current repo rate plus 2%",
              RTGS_FAQ)])
Q(T, "Limits and timings", "Advanced",
  "Which of the following single RTGS payments must carry the Legal Entity Identifier (LEI) of both the remitter and "
  "the beneficiary?\nP. ₹60 crore from a company to another company\nQ. ₹75 crore from one individual to another "
  "individual\nR. ₹55 crore from a Government-owned corporation to a supplier firm\nS. ₹40 crore from a company to a "
  "partnership firm",
  ["P and R only", "P, Q and R only", "P only", "P, R and S only"],
  concept="LEI for large-value payments",
  explanation="All single NEFT/RTGS payments of ₹50 crore and above undertaken by entities (non-individuals) must "
              "include remitter and beneficiary LEI. It is not needed where both parties are individuals (Q), or "
              "below ₹50 crore (S). Government departments are exempt, but Government corporations and undertakings "
              "must obtain LEI (R needs it).",
  steps=["P: ₹60 cr, entities → yes", "Q: both individuals → no", "R: ₹55 cr, Govt corporation → yes",
         "S: below ₹50 cr → no"],
  why="Q involves only individuals; S is below the ₹50 crore threshold; P alone misses R.",
  facts=[fact("All single payment transactions of ₹50 crore and above undertaken by entities (non-individuals) should "
              "include remitter and beneficiary LEI; not required where both remitter and beneficiary are "
              "individuals; Corporations / Undertakings, including those fully owned by the Government, shall need to "
              "obtain LEI", LEI_FAQ)])

# ================================================================= 21. IMPS (1 / 2 / 1)
T = "IMPS"
Q(T, "Limits and features", "Basic",
  "IMPS, introduced in 2010, made India which country in the world to introduce such a 24x7 fast payment system?",
  ["Fourth, after South Korea, the UK and South Africa", "First", "Second, after Singapore",
   "Tenth, after the G7 countries"],
  concept="IMPS as a fast payment system",
  explanation="RBI's payments booklet says IMPS is a 24x7 'fast payments' system introduced in 2010, and India was "
              "the fourth country, after South Korea, the UK and South Africa, to introduce such a system.",
  steps=["IMPS: 2010", "India: fourth, after South Korea, UK, South Africa"],
  why="India was not the first; the other rankings are not what RBI records.",
  facts=[fact("IMPS is a 24*7 'fast payments' system that was introduced in 2010. India was the fourth country after "
              "South Korea, UK and South Africa to introduce such a payment system", PAY_BOOKLET)])
Q(T, "Limits and features", "Intermediate",
  "Which of the following is true of participation in IMPS, as described by RBI?",
  ["Besides banks, non-bank entities such as PPI issuers can participate, enabling remittances from wallets to bank "
   "accounts",
   "Only scheduled commercial banks can participate", "It can be used only through mobile phones",
   "Both remitter and beneficiary must still be registered for mobile banking"],
  concept="IMPS ecosystem",
  explanation="IMPS is multi-channel (mobile, ATM, internet banking, branches, BCs). Besides banks, it allows non-bank "
              "entities such as PPI issuers to participate. The early requirement that both parties register for "
              "mobile banking was later removed.",
  steps=["Multi-channel", "Banks + PPI issuers", "Mobile banking registration no longer needed for both parties"],
  why="Non-banks can participate; channels go beyond mobile; the dual-registration requirement was an early feature.",
  facts=[fact("IMPS is a multi-channel system that can be accessed using mobile, ATM, internet banking, bank branches, "
              "BCs, etc. Besides banks, the system allows non-bank entities such as PPI issuers to participate", PAY_BOOKLET)])
Q(T, "Limits and features", "Intermediate",
  "According to RBI's Payment System Report (May 2026), how did the value of IMPS transactions change between CY "
  "2021 and CY 2025?",
  ["It roughly doubled, from ₹38 lakh crore to ₹75 lakh crore", "It fell from ₹75 lakh crore to ₹38 lakh crore",
   "It rose from ₹72 lakh crore to ₹300 lakh crore", "It stayed flat at about ₹50 lakh crore"],
  concept="IMPS trends",
  explanation="IMPS volume rose from 434 crore in CY 2021 to 518 crore in CY 2025, while value doubled from ₹38 lakh "
              "crore to ₹75 lakh crore (CAGR 4.5% in volume and 18.1% in value). Its larger average size shows it is "
              "preferred for medium- to large-value transfers.",
  steps=["Value: 38 → 75 lakh crore", "CAGR: volume 4.5%, value 18.1%"],
  why="The second option reverses the trend; 72 → 300 lakh crore is UPI; value did not stay flat.",
  current=PSR,
  facts=[fact("IMPS transactions volume rose from 434 crore in CY 2021 to 518 crore in CY 2025... transaction value "
              "doubled from ₹38 lakh crore to ₹75 lakh crore", PSR_MAY26)])

imps_ticket = 75 * 1e5 / 518
ratio = imps_ticket / 1313
assert round(imps_ticket, -2) == 14500 and 10.5 < ratio < 11.5
Q(T, "Limits and features", "Advanced",
  "In CY 2025, IMPS handled 518 crore transactions worth ₹75 lakh crore, while UPI's average ticket size was ₹1,313. "
  "What was IMPS's approximate average ticket size, and about how many times UPI's was it?",
  ["About ₹14,500; about 11 times", "About ₹1,450; about the same", "About ₹1,45,000; about 110 times",
   "About ₹14,500; about 5 times"],
  concept="Comparing ticket sizes",
  explanation="₹75 lakh crore = 75 × 10⁵ crore rupees. Divide by 518 crore transactions: 75,00,000 ÷ 518 ≈ ₹14,479, "
              "about ₹14,500. Ratio to UPI: 14,479 ÷ 1,313 ≈ 11. RBI notes IMPS is preferred for medium- to "
              "large-value transfers.",
  steps=["75,00,000 ÷ 518 ≈ 14,479", "14,479 ÷ 1,313 ≈ 11"],
  why="₹1,450 and ₹1,45,000 misplace the decimal; 5 times is an arithmetic slip.",
  computed=True, current=PSR,
  facts=[fact("IMPS: 518 crore transactions, ₹75 lakh crore in CY 2025; average transaction size under IMPS is higher "
              "than that of UPI; UPI average ticket size ₹1313 in CY 2025", PSR_MAY26)])

# ================================================================= 22. NPCI (3 / 1 / 1)
T = "NPCI"
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Basic",
  "Since December 2013, NPCI has operated which system on behalf of RBI?",
  ["Cheque Truncation System (CTS)", "Real Time Gross Settlement (RTGS)", "National Electronic Funds Transfer (NEFT)",
   "e-Kuber"],
  concept="NPCI's role",
  explanation="RBI's payments booklet records that in December 2013 NPCI was entrusted with operating CTS on behalf of "
              "RBI; CTS and the NFS ATM network are NPCI's main revenue sources on the switching side. RTGS, NEFT and "
              "e-Kuber are run by RBI.",
  steps=["Dec 2013: NPCI operates CTS for RBI"],
  why="RTGS, NEFT and e-Kuber are RBI systems.",
  facts=[fact("In December 2013, NPCI was entrusted with the task of operating CTS on behalf of RBI", PAY_BOOKLET)])
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Basic",
  "The Aadhaar Payments Bridge System (APBS), implemented in 2012, is used mainly for:",
  ["Crediting government subsidies and benefits to Aadhaar-linked bank accounts",
   "Cash withdrawal at micro-ATMs using biometrics", "Electronic toll collection", "Cross-border card payments"],
  concept="APBS",
  explanation="APBS, a component of NACH implemented in 2012, uses the Aadhaar number to electronically credit "
              "government subsidies and benefits to Aadhaar-linked bank accounts. Biometric cash withdrawal at BC "
              "points is AePS; toll collection is NETC.",
  steps=["APBS → DBT credits using Aadhaar number"],
  why="Biometric withdrawals are AePS; tolls are NETC/FASTag; cross-border card payments are not APBS.",
  facts=[fact("APBS, a component of NACH, which uses Aadhaar number for electronic crediting of government subsidies "
              "and benefits in Aadhaar-linked bank account, was implemented in 2012", PAY_BOOKLET)])
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Basic",
  "Which of the following payment systems is NOT operated by NPCI?",
  ["RTGS", "IMPS", "NACH", "BBPS"],
  concept="NPCI's product range",
  explanation="NPCI operates retail systems such as IMPS, RuPay, UPI, NACH, AePS, APBS, NETC, *99# and BBPS. RTGS is "
              "owned and operated by RBI, with settlement in RBI's books.",
  steps=["NPCI: IMPS, UPI, NACH, AePS, NETC, BBPS, RuPay", "RBI: RTGS, NEFT"],
  why="IMPS, NACH and BBPS are NPCI products.",
  facts=[fact("NPCI has rolled out a variety of innovative retail payment products viz., IMPS, RuPay card scheme, UPI, "
              "NACH, AePS, APBS, NETC, *99# (USSD based) and BBPS", PAY_BOOKLET),
         fact("RTGS funds settlement takes place in the books of the RBI", RTGS_FAQ)])
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Intermediate",
  "To widen acceptance abroad, RuPay has tied up with other card networks. With which country's network 'Elo' is it "
  "linked?",
  ["Brazil", "Serbia", "Japan", "South Korea"],
  concept="RuPay's international partners",
  explanation="RBI's booklet lists RuPay's tie-ups with Union Pay (China), JCB (Japan), NETS (Singapore), BC Card "
              "(South Korea), Elo (Brazil) and DinaCard (Serbia), besides Discover and Diners.",
  steps=["Elo → Brazil", "DinaCard → Serbia", "JCB → Japan", "BC Card → South Korea"],
  why="Serbia's network is DinaCard; Japan's is JCB; South Korea's is BC Card.",
  facts=[fact("RuPay has tied up with Union Pay (China), JCB (Japan), NETS (Singapore), BC Card (South Korea), Elo "
              "(Brazil) and DinaCard (Serbia)", PAY_BOOKLET)])
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Advanced",
  "How are APBS transactions routed to the destination bank?",
  ["Through the Aadhaar mapper, a repository of Aadhaar numbers managed by NPCI, using the destination bank's unique "
   "Institution Identification Number (IIN)",
   "Through the IFSC of the beneficiary branch entered by the government department",
   "Through UIDAI, which settles the funds directly", "Through the beneficiary's mobile number linked to UPI"],
  concept="Aadhaar mapper",
  explanation="APBS uses the Aadhaar mapper, a repository of Aadhaar numbers managed by NPCI, to route transactions to "
              "the destination bank based on its unique IIN. The sponsoring government department needs only the "
              "beneficiary's Aadhaar number, not the IFSC or account number.",
  steps=["Aadhaar number → Aadhaar mapper (NPCI)", "Mapper gives bank's IIN → routing"],
  why="APBS does not need the IFSC; UIDAI does not settle funds; UPI mobile linkage is unrelated.",
  facts=[fact("Aadhaar mapper, a repository of Aadhaar numbers managed by NPCI, is used for routing the APBS "
              "transactions to the destination banks based on the unique IIN (Institution Identification Number) of "
              "destination bank", PAY_BOOKLET)])

# ================================================================= 23. Payment Banks (1 / 2 / 1)
T = "Payment Banks"
Q(T, "Permitted activities", "Basic",
  "What minimum paid-up equity capital did RBI's Guidelines for Licensing of Payments Banks (November 2014) "
  "prescribe for a payments bank?",
  ["₹100 crore", "₹300 crore", "₹500 crore", "₹200 crore"],
  concept="Capital of payments banks",
  explanation="The 2014 licensing guidelines set the minimum paid-up equity capital of a payments bank at ₹100 "
              "crore, mainly to buffer operational risk and fund technology, along with a minimum CRAR of 15%.",
  steps=["Minimum paid-up equity: ₹100 crore", "Minimum CRAR: 15%"],
  why="₹300 crore is the SFB requirement; ₹500 crore and ₹200 crore are not payments bank figures.",
  facts=[fact6("Payments bank licensing guidelines: minimum paid-up equity capital Rs. 100 crore", PB_GUIDE)])
Q(T, "Permitted activities", "Intermediate",
  "Since payments banks work mostly through BCs and ATMs, what outreach requirement did RBI's November 2014 "
  "licensing guidelines lay down for them instead of the 25% unbanked rural branch norm?",
  ["At least 25% of physical access points, including BCs, must be in rural centres",
   "At least 50% of branches must be in metropolitan centres", "No outreach requirement at all",
   "All branches must be in unbanked villages"],
  concept="Payments bank outreach",
  explanation="The 2014 licensing guidelines did not stipulate that 25% of branches be in unbanked rural centres for "
              "payments banks. Instead they required at least 25% of physical access points, including BCs, in rural "
              "centres, and a controlling office for clusters of access points.",
  steps=["25% unbanked rural branch norm: not stipulated", "25% of physical access points in rural centres: required"],
  why="There is a requirement; it does not concern metro branches or require all branches in villages.",
  facts=[fact6("Payments bank licensing guidelines: 25 per cent unbanked rural branch norm not stipulated; at least 25 "
               "per cent of physical access points including BCs to be in rural centres", PB_GUIDE)])
Q(T, "Permitted activities", "Intermediate",
  "Under RBI's Guidelines for Licensing of Payments Banks (November 2014), could a payments bank distribute mutual "
  "fund units and insurance products?",
  ["Yes, as non-risk-sharing simple services not requiring its own funds, with RBI's prior approval",
   "No, payments banks may only accept deposits", "Yes, and it may also underwrite insurance risk",
   "Only if it first converts into a small finance bank"],
  concept="Third-party products",
  explanation="The 2014 guidelines allowed payments banks to undertake other non-risk-sharing simple financial "
              "services that do not require commitment of their own funds, such as distribution of mutual fund "
              "units, insurance and pension products, with RBI's prior approval and compliance with the sectoral "
              "regulator's rules.",
  steps=["Distribution allowed (no own funds, no risk sharing)", "Prior RBI approval needed"],
  why="Distribution is permitted; underwriting risk is not; conversion into an SFB is not required.",
  facts=[fact6("Payments bank licensing guidelines: non-risk-sharing simple financial services not requiring own funds, "
               "such as distribution of mutual fund units, insurance and pension products, with prior RBI approval",
               PB_GUIDE)])
Q(T, "Deposit limit", "Advanced",
  "Consider the following statements about payments banks:\nI. Under RBI's Payments Banks directions of 2025, they "
  "can act as business correspondents of other banks and, with customer consent, transfer deposits above the limit "
  "to an account with another bank.\nII. RBI's 2014 licensing guidelines allowed them to hold up to 25% of their "
  "demand deposit balances in current and time deposits with other scheduled commercial banks.\nIII. The 2014 "
  "licensing guidelines permitted them to handle cross-border personal remittances on the current account.\nWhich "
  "of the above is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I only"],
  concept="Operations of payments banks",
  explanation="Payments banks may act as BCs of other banks and, with customer consent, move funds to the customer's "
              "account with another bank (I correct). The 2014 licensing guidelines required at least 75% of demand "
              "deposit balances in SLR securities and allowed up to 25% in current and time deposits with other SCBs "
              "(II correct), and permitted cross-border personal remittances on current account (III correct).",
  steps=["I: correct", "II: correct", "III: correct"],
  why="Each other option leaves out a correct statement.",
  facts=[fact("PBs are permitted to act as Business Correspondents (BCs) of other banks... may effect the transfer of "
              "funds deposited by them into their account with another eligible bank", PB_MISC),
         fact6("Payments bank licensing guidelines: minimum 75 per cent of demand deposit balances in SLR securities, "
               "maximum 25 per cent in deposits with other SCBs; cross-border remittances only for personal "
               "payments/remittances on the current account", PB_GUIDE)])

# ================================================================= 24. Small Finance Banks (1 / 1 / 1)
T = "Small Finance Banks"
Q(T, "Licensing norms", "Basic",
  "In foreign exchange business, a small finance bank can initially become which category of Authorised Dealer for "
  "its clients' requirements?",
  ["Category II", "Category I", "Category III", "Full-fledged money changer only"],
  concept="SFBs and forex",
  explanation="The SFB licensing guidelines allow an SFB to become a Category II Authorised Dealer in foreign exchange "
              "for its clients. A scheduled SFB with at least two years as AD Category II may then apply for AD "
              "Category I, subject to conditions.",
  steps=["Start: AD Category II", "Later (conditions): AD Category I"],
  why="Category I needs two years as Category II first; Category III and money changer are not the provision.",
  facts=[fact("A small finance bank can also become a Category II Authorised Dealer in foreign exchange business for "
              "its clients' requirements", SFB_MD)])
Q(T, "Licensing norms", "Intermediate",
  "Promoters of a small finance bank holding more than 40% (or 26%, as applicable) must submit a dilution schedule to "
  "bring their stake down to what level, and within what period?",
  ["26% within 15 years", "40% within 5 years", "15% within 12 years", "10% within 10 years"],
  concept="Promoter dilution",
  explanation="At the time of licensing, promoters holding more than 40% or 26%, as applicable, must submit a "
              "dilution schedule to bring the stake down to 26% within 15 years, which RBI examines, approves and "
              "monitors.",
  steps=["Lock-in: minimum 40% for first 5 years", "Dilution target: 26% within 15 years"],
  why="40% for five years is the lock-in; the other combinations are not in the guidelines.",
  facts=[fact("Promoters having shareholding in excess of 40 per cent or 26 per cent... shall submit a dilution "
              "schedule for bringing down the stake to 26 per cent within 15 years", SFB_MD)])
Q(T, "Licensing norms", "Advanced",
  "Which of these scheduled small finance banks, each an AD Category II for over two years, is eligible to apply for "
  "an Authorised Dealer Category I licence?",
  ["SFB-P: net worth ₹650 crore, CRAR 17%, net NPA 5.2% in each of the last four quarters, profits in both preceding "
   "years, no CRR/SLR default",
   "SFB-Q: net worth ₹450 crore, CRAR 18%, net NPA 3%, profitable, no CRR/SLR default",
   "SFB-R: net worth ₹800 crore, CRAR 14%, net NPA 2%, profitable, no CRR/SLR default",
   "SFB-S: net worth ₹700 crore, CRAR 16%, net NPA 6.5% in one of the last four quarters, profitable"],
  concept="AD Category I eligibility",
  explanation="A scheduled SFB with at least two years as AD Category II needs net worth of at least ₹500 crore, CRAR "
              "not below 15%, net NPAs not above 6% during the previous four quarters, profits in the preceding two "
              "years and no CRR/SLR default in the previous two years. Only SFB-P meets all of these.",
  steps=["Q: net worth < ₹500 crore", "R: CRAR < 15%", "S: net NPA > 6% in a quarter", "P: meets all"],
  why="Q fails net worth, R fails CRAR and S fails the net NPA test.",
  facts=[fact("Eligibility for AD Category-I: at least two years as AD Category-II; included in Second Schedule; "
              "minimum net worth ₹500 crore; CRAR not less than 15%; net NPAs not exceeding 6% during previous four "
              "quarters; profit in preceding two years; no default in CRR/SLR during previous two years", SFB_MD)])

# ================================================================= 25. Financial Markets (1 / 2 / 3)
T = "Financial Markets"
Q(T, "Structure and regulators", "Basic",
  "The National Housing Bank, established as the apex body of housing finance, was set up in:",
  ["July 1988", "April 1988", "July 1982", "April 1990"],
  concept="Apex financial institutions",
  explanation="RBI's chronology records that the National Housing Bank was established in July 1988 as an apex body of "
              "housing finance and to promote housing development.",
  steps=["NHB: July 1988"],
  why="April 1988 is SEBI and DFHI; July 1982 is NABARD; April 1990 is not the NHB date.",
  facts=[fact("Jul 1988: The National Housing Bank established as an apex body of housing finance", CHRON_85)])
Q(T, "Structure and regulators", "Intermediate",
  "What did RBI decide to constitute on 7 October 2026 as a forum for structured engagement with market participants "
  "on money, government securities and foreign exchange markets?",
  ["A Technical Consultative Committee for Financial Markets", "A Financial Stability and Development Council",
   "A Monetary Policy Committee for markets", "A Self-Regulatory Organisation for primary dealers"],
  concept="Market consultation",
  explanation="RBI's Statement on Developmental and Regulatory Policies of 7 October 2026 announced a Technical "
              "Consultative Committee for Financial Markets, a forum for engaging with market participants on policy "
              "and operational matters in money, G-sec and forex markets, their derivatives and infrastructure. Its "
              "composition and terms of reference are to be notified separately.",
  steps=["Oct 2026: Technical Consultative Committee for Financial Markets"],
  why="FSDC is a Government body chaired by the Finance Minister; the other two were not announced.",
  current=ca("2026-10-07"),
  facts=[fact("The Reserve Bank has decided to constitute a Technical Consultative Committee for Financial Markets... "
              "money, government securities and foreign exchange markets as well as the respective derivative "
              "markets", SDRP_OCT26)])
Q(T, "Structure and regulators", "Intermediate",
  "In August 1994 the rupee was made convertible on the current account. This followed India's acceptance of which "
  "IMF provision?",
  ["Article VIII of the Articles of Agreement", "Article IV", "Article XIV", "Article I"],
  concept="Current account convertibility",
  explanation="RBI's chronology records that in August 1994 the rupee was made convertible on the current account, "
              "with India accepting Article VIII of the IMF's Articles of Agreement.",
  steps=["Aug 1994: current account convertibility", "IMF Article VIII accepted"],
  why="Article IV covers surveillance; Article XIV allows transitional restrictions; Article I states purposes.",
  facts=[fact("Aug 1994: Rupee made convertible on the Current Account. Acceptance of Article VIII of the Articles of "
              "Agreement of the IMF", CHRON_91)])
Q(T, "Structure and regulators", "Advanced",
  "Consider the following statements about India's exchange rate reforms:\nI. In March 1992 a dual exchange rate "
  "system, the Liberalised Exchange Rate Management System (LERMS), was introduced as the first step towards a "
  "market-determined rate.\nII. The exchange rate was unified in 1993.\nIII. In July 1991 the rupee was devalued in "
  "two stages, by about 18% cumulatively in US dollar terms.\nWhich of the above is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I only"],
  concept="Move to a market-determined exchange rate",
  explanation="RBI records the two-stage devaluation of 1 and 3 July 1991 (about 18% cumulatively in USD terms), "
              "LERMS in March 1992 as a dual exchange rate system and the initial step to a market-determined rate, "
              "and a unified exchange rate in 1993. All three are correct.",
  steps=["Jul 1991: devaluation ~18%", "Mar 1992: LERMS", "1993: unified rate"],
  why="Each other option omits a correct statement.",
  facts=[fact("1 & 3 Jul 1991: Rupee Devalued in two stages. Cumulative devaluation about 18 percent in USD terms; Mar "
              "1992: LERMS introduced... initial step to enable a transition to a market determined exchange rate "
              "system; 1993: Unified Exchange rate", CHRON_91)])
Q(T, "Structure and regulators", "Advanced",
  "Under RBI's directions of 10 October 2026 on foreign exchange derivative contracts involving the INR, which "
  "statement is correct?",
  ["A cancelled contract cannot be rebooked with any Authorised Dealer, but contracts may still be rolled over on "
   "maturity",
   "Both rebooking of cancelled contracts and rollovers are prohibited",
   "Rebooking is allowed only with a different Authorised Dealer",
   "Users need not give any undertaking about hedging the same exposure elsewhere"],
  concept="Forex derivative rules",
  explanation="ADs may not permit users to rebook any INR forex derivative contract, deliverable or not, that has "
              "been cancelled with any AD after the directions, but may continue to allow rollovers on maturity. ADs "
              "must also obtain an undertaking that the same exposure has not been hedged with another AD.",
  steps=["Rebooking after cancellation: barred", "Rollover on maturity: allowed", "Undertaking on multiple hedges: "
         "required"],
  why="Rollovers remain allowed; rebooking is barred with every AD; an undertaking is required.",
  current=ca("2026-10-10"),
  facts=[fact("An Authorised Dealer shall not permit users to rebook any foreign exchange derivative contract involving "
              "the INR... which has been cancelled with any of the Authorised Dealers; may continue to permit users to "
              "rollover on maturity; obtain an undertaking from the user that the same underlying exposure has not "
              "been hedged with any other Authorised Dealer", FX_RM)])
Q(T, "Structure and regulators", "Advanced",
  "In its Payment System Report of May 2026, why does RBI consider stablecoins an unsuitable payment medium?",
  ["They fail the tests of singleness of money, elasticity and integrity, while a CBDC offers similar efficiency "
   "without those risks",
   "They cannot be transferred across borders", "They are already banned by the Basel Committee",
   "They settle more slowly than cheques"],
  concept="Stablecoins versus CBDC",
  explanation="RBI argues that stablecoins do not pass the tests of singleness, elasticity and integrity of money; "
              "they pose de-pegging, run and disintermediation risks and can weaken monetary sovereignty, whereas "
              "CBDCs offer similar efficiency without those risks.",
  steps=["Tests: singleness, elasticity, integrity → stablecoins fail", "CBDC: fiat, preserves singleness"],
  why="Stablecoins can move across borders (that is a concern); the other reasons are not RBI's.",
  current=PSR,
  facts=[fact("The stablecoins do not pass the said tests of singleness, elasticity and integrity... do not serve a "
              "purpose that cannot be better fulfilled by a CBDC. CBDCs offer similar level of efficiency without the "
              "risks", PSR_MAY26)])

# ================================================================= 26. Money Market (2 / 3 / 2)
T = "Money Market"
Q(T, "Instruments: T-bills, CP, CD, call money", "Basic",
  "The Discount and Finance House of India (DFHI), set up as a money market institution, commenced operations in:",
  ["April 1988", "March 1989", "April 2001", "July 1964"],
  concept="Money market institutions",
  explanation="RBI's chronology records that DFHI, set up as a money market institution, commenced operations in April "
              "1988.",
  steps=["DFHI: April 1988"],
  why="April 2001 is CCIL; July 1964 is IDBI; March 1989 is not DFHI's start.",
  facts=[fact("Apr 1988: The Discount and Finance House of India, set up as a money market institution, commenced "
              "operations", CHRON_85)])
Q(T, "Instruments: T-bills, CP, CD, call money", "Basic",
  "Which Treasury Bill was introduced in November 1986?",
  ["182-day T-bill", "91-day T-bill", "364-day T-bill", "14-day T-bill"],
  concept="T-bill history",
  explanation="RBI's chronology records the introduction of the 182-day Treasury Bill in November 1986. Auctions of "
              "14-day T-bills began in June 1997 and 28-day T-bills in October 1997.",
  steps=["Nov 1986: 182-day T-bill"],
  why="The 91-day bill existed earlier; 14-day auctions started in 1997; 364-day is not the 1986 bill.",
  facts=[fact("Nov 1986: 182 day TB introduced", CHRON_85)])
Q(T, "Instruments: T-bills, CP, CD, call money", "Intermediate",
  "In April 2026, RBI decided to deepen the term money market. What change was announced?",
  ["Non-bank participants such as AIFIs, NBFCs (including HFCs) and companies were allowed to participate, and the "
   "borrowing limit of standalone primary dealers was raised",
   "Term money was restricted to scheduled commercial banks only", "The call money market was abolished",
   "Mutual funds were allowed to borrow in the call market"],
  concept="Term money market",
  explanation="Until then only banks and standalone primary dealers could participate in the term money market. RBI "
              "decided to expand the participant base to non-bank participants (AIFIs, NBFCs including housing "
              "finance companies, companies, etc.) and to raise standalone PDs' borrowing limit, to improve "
              "transmission by linking overnight and longer-term rates.",
  steps=["Before: banks + standalone PDs", "After: + AIFIs, NBFCs, HFCs, companies", "PD borrowing limit raised"],
  why="Participation was widened, not narrowed; the call market was not abolished; MF borrowing in call money was "
      "not announced.",
  current=ca("2026-04-08"),
  facts=[fact("At present, only banks and standalone primary dealers are eligible to participate in the term money "
              "market; decided to expand the participant base to include non-bank participants viz., AIFIs, NBFCs, "
              "including housing finance companies, companies, etc.; and enhance the borrowing limit for standalone "
              "primary dealers", SDRP_APR26)])
Q(T, "Instruments: T-bills, CP, CD, call money", "Intermediate",
  "According to RBI's chronology, RBI conducted the first auction of which Treasury Bill on 6 June 1997?",
  ["14-day T-bill", "28-day T-bill", "182-day T-bill", "Cash Management Bill"],
  concept="Short-dated T-bills",
  explanation="RBI conducted the first auction of 14-day Treasury Bills on 6 June 1997; auctions of 28-day T-bills "
              "were introduced in October 1997. Cash Management Bills came in 2010.",
  steps=["6 Jun 1997: 14-day TB", "Oct 1997: 28-day TB"],
  why="28-day auctions began in October; 182-day bills date from 1986; CMBs from 2010.",
  facts=[fact("6 Jun 1997: RBI Conducts first auction of 14 day Treasury Bills. In October, auction of 28 day Treasury "
              "Bills was introduced", CHRON_91)])
Q(T, "Instruments: T-bills, CP, CD, call money", "Intermediate",
  "Which institution acts as a trade repository for secondary market trades in Certificates of Deposit and Commercial "
  "Paper and for primary issuances of CP?",
  ["Clearing Corporation of India Ltd (CCIL)", "NPCI", "SEBI", "IDRBT"],
  concept="Trade repository",
  explanation="RBI's booklet says CCIL acts as a trade repository for OTC forex, interest rate and credit derivatives, "
              "and also for secondary market trades in CDs and CPs, market repo in corporate bonds/CDs/CPs/short NCDs, "
              "and primary market issuances of CP reported by issuing and paying agents.",
  steps=["CD/CP trades and CP issuances → reported to CCIL as TR"],
  why="NPCI runs retail payments; SEBI is a regulator; IDRBT is a technology institute.",
  facts=[fact("CCIL also acts as a TR for (i) secondary market trades in Certificates of Deposit / Commercial Papers... "
              "and (iii) primary market issuances of Commercial Paper", PAY_BOOKLET)])
Q(T, "Instruments: T-bills, CP, CD, call money", "Advanced",
  "Consider the following statements about the wholesale digital rupee (e₹-W) pilot as described by RBI:\nI. Its use "
  "cases include settlement of inter-bank lending and borrowing in the call money market.\nII. Its use cases include "
  "tokenised issuance and settlement of Certificates of Deposit.\nIII. It is open to retail individuals for P2P "
  "payments.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="e₹-W in money markets",
  explanation="RBI lists four e₹-W use cases: settlement of secondary market G-sec trades, settlement of inter-bank "
              "call money lending/borrowing, tokenised issuance and settlement of CDs, and tokenised corporate bonds "
              "(I and II correct). e₹-W is for financial institutions in a restricted ecosystem, not retail P2P (III "
              "wrong).",
  steps=["I: correct", "II: correct", "III: wrong (retail use is e₹-R)"],
  why="III describes the retail e₹; 'I only' omits II.",
  facts=[fact("Presently, there are four use cases of e₹-W – (i) funds settlement of secondary market transactions in "
              "Government Securities, (ii) settlement of inter-bank lending and borrowing in call money market, (iii) "
              "tokenised issuances and settlements of Certificates of Deposit, and (iv) tokenised issuance and "
              "settlement of Corporate Bonds; Wholesale CBDC is designed for use by financial institutions", ERUPEE_FAQ)])
Q(T, "Instruments: T-bills, CP, CD, call money", "Advanced",
  "Match the trade type with the order-matching platform on which it is undertaken:\n1. Secondary market outright "
  "G-sec trades   2. Market repo trades   3. Tri-party repo trades\nP. TREPS   Q. NDS-OM   R. CROMS",
  ["1-Q, 2-R, 3-P", "1-R, 2-Q, 3-P", "1-P, 2-R, 3-Q", "1-Q, 2-P, 3-R"],
  concept="Money and G-sec market platforms",
  explanation="Outright secondary market trades are undertaken on the Negotiated Dealing System-Order Matching "
              "(NDS-OM), repo trades on the Clearcorp Repo Order Matching System (CROMS) and tri-party repo on the "
              "Triparty Repo Dealing System (TREPS). Trades are cleared and settled by CCIL.",
  steps=["Outright → NDS-OM", "Repo → CROMS", "Tri-party repo → TREPS"],
  why="The other matchings swap the repo and outright platforms.",
  facts=[fact("The secondary market outright, repo and tri-party repo trades are undertaken on NDS-OM, CROMS and TREPS, "
              "respectively", PAY_BOOKLET)])

# ================================================================= 27. Capital Market (1 / 2 / 0)
T = "Capital Market"
Q(T, "SEBI", "Basic",
  "According to its Preamble, the basic functions of SEBI are to:",
  ["Protect the interests of investors in securities, and promote the development of and regulate the securities "
   "market",
   "Regulate banks and NBFCs", "Manage the public debt of the Government", "Regulate insurance and pension funds"],
  concept="SEBI's mandate",
  explanation="SEBI's Preamble describes its functions as protecting the interests of investors in securities and "
              "promoting the development of, and regulating, the securities market and connected matters.",
  steps=["SEBI: investor protection + development + regulation of securities market"],
  why="Banks/NBFCs and public debt fall under RBI; insurance under IRDAI; pensions under PFRDA.",
  facts=[fact("...to protect the interests of investors in securities and to promote the development of, and to "
              "regulate the securities market and for matters connected therewith or incidental thereto", SEBI_ABOUT)])
Q(T, "SEBI", "Intermediate",
  "According to RBI's chronology, in which year did SEBI formulate its 'Insider Trading Regulations'?",
  ["1992", "1988", "2000", "1996"],
  concept="Early SEBI regulations",
  explanation="RBI's chronology records that SEBI formulated its Insider Trading Regulations in 1992, the year the SEBI "
              "Act gave it statutory status.",
  steps=["1992: Insider Trading Regulations"],
  why="1988 is SEBI's non-statutory constitution; 2000 is index futures; 1996 is not the date.",
  facts=[fact("1992: SEBI formulated 'Insider Trading Regulations'", CHRON_91)])
Q(T, "Primary and secondary market", "Intermediate",
  "Stock index futures were introduced in India as an exchange-traded derivative in:",
  ["June 2000", "June 1994", "January 2003", "July 1999"],
  concept="Equity derivatives",
  explanation="RBI's chronology records that stock index futures were introduced as an exchange-traded derivative in "
              "June 2000. Interest rate swaps and FRAs (OTC derivatives) came in July 1999.",
  steps=["Jun 2000: stock index futures"],
  why="June 1994 is when NSE began; July 1999 is IRS/FRAs; January 2003 is retail G-sec trading on exchanges.",
  facts=[fact("Jun 2000: Stock Index Futures introduced by as an exchange traded derivative", CHRON_00)])

# ================================================================= 28. Insurance (3 / 2 / 2)
T = "Insurance"
Q(T, "Government insurance schemes", "Basic",
  "Pradhan Mantri Suraksha Bima Yojana (PMSBY) is offered by:",
  ["Public sector general insurance companies or any other general insurer willing to offer it on similar terms",
   "LIC alone", "Only private life insurers", "EPFO"],
  concept="Insurers of the social security schemes",
  explanation="DFS states that PMSBY is offered by public sector general insurance companies or any other general "
              "insurer willing to offer the product on similar terms, while PMJJBY is offered by LIC and other life "
              "insurers.",
  steps=["PMSBY (accident) → general insurers", "PMJJBY (life) → LIC and life insurers"],
  why="LIC offers PMJJBY; PMSBY is not limited to private life insurers; EPFO has no role.",
  facts=[fact("The Scheme is being offered by Public Sector General Insurance Companies or any other General Insurance "
              "Company willing to offer the product on similar terms", PMSBY),
         fact("PMJJBY is being offered by the Life Insurance Corporation and all other life insurers", PMJJBY)])
Q(T, "Life and general insurance", "Basic",
  "The General Insurance Business (Nationalisation) Act, 1972 nationalised general insurance with effect from 1 "
  "January 1973 and grouped 107 insurers into how many companies?",
  ["Four", "Two", "Six", "Eight"],
  concept="Nationalisation of general insurance",
  explanation="The Act nationalised general insurance from 1 January 1973; 107 insurers were amalgamated into four "
              "companies — National Insurance, New India Assurance, Oriental Insurance and United India Insurance — "
              "with GIC incorporated as a company.",
  steps=["107 insurers → 4 companies", "GIC incorporated"],
  why="Two, six and eight are not the number of companies formed.",
  facts=[fact("1972: The General Insurance Business (Nationalisation) Act, 1972 nationalised the general insurance "
              "business with effect from 1st January 1973. 107 insurers amalgamated and grouped into four companies",
              LIC_HIST)])
Q(T, "IRDAI", "Basic",
  "'Saral Suraksha Bima', for which IRDAI has issued guidelines, is a standard product of which type?",
  ["Personal accident insurance", "Term life insurance", "Crop insurance", "Health insurance for senior citizens only"],
  concept="Standard insurance products",
  explanation="IRDAI's page carries FAQs on 'Guidelines on Standard Personal Accident Insurance Product: Saral Suraksha "
              "Bima', a standardised personal accident cover.",
  steps=["Saral Suraksha Bima → standard personal accident product"],
  why="It is not a term life, crop or senior-citizen health product.",
  facts=[fact("FAQs on Guidelines on Standard Personal Accident Insurance Product: Saral Suraksha Bima", IRDAI)])
Q(T, "Life and general insurance", "Intermediate",
  "In November 2000, the General Insurance Corporation of India (GIC) was notified as:",
  ["The Indian Reinsurer, ending its supervisory role over its subsidiaries",
   "The holding company of LIC", "The insurance regulator", "A non-life insurer for agriculture only"],
  concept="GIC Re",
  explanation="DFS records that in November 2000 GIC was notified as the Indian Reinsurer and its supervisory role "
              "over its subsidiaries ended; from 21 March 2003 its role as holding company also ended and ownership of "
              "the subsidiaries passed to the Government.",
  steps=["Nov 2000: GIC = Indian Reinsurer", "Mar 2003: holding company role ends"],
  why="GIC never held LIC; IRDAI is the regulator; agriculture insurance is AICIL's role.",
  facts=[fact("In November 2000, GIC was notified as the Indian Reinsurer, and its supervisory role over its "
              "subsidiaries was brought to an end", DFS_PSI)])
Q(T, "Life and general insurance", "Intermediate",
  "Agriculture Insurance Company of India Ltd (AICIL), incorporated on 20 December 2002, was promoted with share "
  "capital from:",
  ["GIC, NABARD and the four public sector general insurance companies", "LIC and SBI", "RBI and NABARD",
   "IRDAI and the Ministry of Agriculture"],
  concept="Specialised insurers",
  explanation="DFS states that AICIL was incorporated on 20 December 2002 to cater exclusively to the insurance needs "
              "of people in agriculture and allied activities, with GIC, NABARD and the four public sector general "
              "insurers contributing to its share capital.",
  steps=["AICIL shareholders: GIC + NABARD + 4 PSGICs"],
  why="LIC, SBI, RBI and IRDAI are not its promoters.",
  facts=[fact("AICIL was incorporated... on 20th December 2002. General Insurance Corporation of India (GIC), NABARD "
              "and four public sector general insurance companies have contributed towards the share capital", DFS_PSI)])
Q(T, "Life and general insurance", "Advanced",
  "Consider the following statements about the history of insurance in India:\nI. In 1956, 245 Indian and foreign "
  "insurers and provident societies were nationalised, and LIC was formed with a capital contribution of ₹5 crore "
  "from the Government.\nII. New India Assurance was founded by Sir Dorabji Tata in 1919.\nIII. The Insurance Act, "
  "1938 was the first legislation in India to regulate insurance business.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Insurance milestones",
  explanation="LIC's history records the 1956 takeover of 245 insurers and provident societies and LIC's formation with "
              "₹5 crore capital (I correct). DFS records New India Assurance's founding by Sir Dorabji Tata on 23 July "
              "1919 (II correct). LIC's history says India had no insurance legislation before "
              "1912, when the Life Insurance Companies Act was passed; the 1938 Act was the first to govern both life "
              "and non-life insurance (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (Life Insurance Companies Act, 1912 came first)"],
  why="Options with III are wrong; 'I only' omits II.",
  facts=[fact("1956: 245 Indian and foreign insurers and provident societies are taken over by the central government "
              "and nationalised. LIC formed by the LIC Act, 1956, with a capital contribution of Rs. 5 crore; prior to 1912 India "
              "had no legislation to regulate insurance business; in the year 1912, the Life Insurance Companies Act "
              "was passed", LIC_HIST),
         fact("The company was founded by Sir Dorabji Tata on July 23rd, 1919 (New India Assurance)", DFS_PSI)])
Q(T, "IRDAI", "Advanced",
  "Consider the following statements about IRDAI:\nI. Section 14 of the IRDA Act, 1999 specifies the duties, powers "
  "and functions of the Authority.\nII. The Insurance Act, 1938 gives IRDAI powers to frame regulations for entities "
  "in the insurance sector.\nIII. Speedy settlement of genuine claims is one of IRDAI's stated objectives.\nWhich of "
  "the above is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I only"],
  concept="IRDAI's legal framework",
  explanation="IRDAI states that Section 14 of the IRDA Act specifies its duties, powers and functions (I); that the "
              "Insurance Act, 1938 is the principal Act and gives it powers to frame regulations (II); and lists "
              "speedy settlement of genuine claims among its key objectives (III).",
  steps=["I: correct", "II: correct", "III: correct"],
  why="Each other option leaves out a correct statement.",
  facts=[fact("Section 14 of the IRDA Act, 1999 specifies the Duties, Powers and Functions of the Authority; the "
              "Insurance Act, 1938... provides the powers to IRDAI to frame regulations; key objectives include speedy "
              "settlement of genuine claims", IRDAI)])

# ================================================================= 29. Mutual Funds (2 / 1 / 1)
T = "Mutual Funds"
Q(T, "Types", "Basic",
  "Under SEBI's categorisation of mutual fund schemes, a liquid fund invests in debt and money market securities with "
  "maturity of:",
  ["Up to 91 days only", "Exactly 1 day", "Up to 1 year", "3 to 5 years"],
  concept="Debt fund categories",
  explanation="SEBI's 2017 categorisation defines a liquid fund as investing in debt and money market securities with "
              "maturity of up to 91 days only, and an overnight fund as investing in overnight securities with "
              "maturity of 1 day.",
  steps=["Liquid fund: ≤ 91 days", "Overnight fund: 1 day"],
  why="1 day is the overnight fund; 1 year and 3–5 years describe other duration categories.",
  facts=[fact("Liquid Fund: Investment in Debt and money market securities with maturity of upto 91 days only",
              MF_CAT)])
Q(T, "Types", "Basic",
  "Which category of mutual fund scheme invests in overnight securities having a maturity of 1 day?",
  ["Overnight Fund", "Liquid Fund", "Ultra Short Duration Fund", "Money Market Fund"],
  concept="Overnight funds",
  explanation="SEBI's categorisation describes an Overnight Fund as an open-ended debt scheme investing in overnight "
              "securities with a maturity of 1 day.",
  steps=["1-day securities → Overnight Fund"],
  why="Liquid funds go up to 91 days; ultra short and money market funds hold longer instruments.",
  facts=[fact("Overnight Fund: Investment in overnight securities having maturity of 1 day", MF_CAT)])
Q(T, "Types", "Intermediate",
  "Under SEBI's scheme categorisation, a Large Cap Fund must invest at least what share of its total assets in equity "
  "and equity-related instruments of large cap companies?",
  ["80%", "65%", "35%", "100%"],
  concept="Equity fund categories",
  explanation="SEBI requires a Large Cap Fund to invest at least 80% of total assets in large cap equity. Mid cap and "
              "small cap funds need 65% in their segments, and a Large & Mid Cap Fund at least 35% in each.",
  steps=["Large cap: ≥ 80%", "Mid/small cap: ≥ 65%", "Large & mid: ≥ 35% each"],
  why="65% applies to mid and small cap funds; 35% to each leg of a large & mid cap fund; 100% is not required.",
  facts=[fact("Large Cap Fund: Minimum investment in equity & equity related instruments of large cap companies - 80% "
              "of total assets", MF_CAT)])

sip_amt, navs = 6000, [20, 30, 24]
units = sum(sip_amt / n for n in navs)
avg_cost = sip_amt * len(navs) / units
assert units == 750 and avg_cost == 24.0 and round(sum(navs) / 3, 2) == 24.67
Q(T, "NAV and SIP", "Advanced",
  "An investor puts ₹6,000 a month through a SIP in an equity scheme for three months, when the NAVs are ₹20, ₹30 and "
  "₹24. What is the average cost per unit, and how does it compare with the simple average of the three NAVs?",
  ["₹24.00, lower than the simple average NAV of about ₹24.67", "₹24.67, equal to the simple average NAV",
   "₹25.00, higher than the simple average NAV", "₹22.00, lower than the simple average NAV of ₹24.67"],
  concept="Rupee cost averaging",
  explanation="Units bought: 6,000/20 = 300, 6,000/30 = 200, 6,000/24 = 250; total 750 units for ₹18,000. Average cost "
              "= 18,000/750 = ₹24.00. The simple average of NAVs is (20+30+24)/3 ≈ ₹24.67. A fixed SIP buys more "
              "units when the NAV is low, so the average cost is below the simple average.",
  steps=["Units: 300 + 200 + 250 = 750", "Cost: 18,000 / 750 = 24.00", "Simple average NAV ≈ 24.67"],
  shortcut="Average cost of a fixed SIP = harmonic mean of the NAVs.",
  why="₹24.67 is the simple average, not the cost; ₹25.00 and ₹22.00 are arithmetic slips.",
  computed=True,
  facts=[fact("SIP helps in Rupee Cost Averaging and in investing in a disciplined manner without worrying about "
              "market volatility and timing the market", AMFI_SIP)])

# ================================================================= 30. Budget and Economic Survey (3 / 4 / 4)
T = "Budget and Economic Survey"
BUD = ca("2026-02-01")
SURV = ca("2026-01-29")
Q(T, "Union Budget highlights", "Basic",
  "To what level did the Union Budget 2026-27 propose to raise public capital expenditure for FY 2026-27?",
  ["₹12.2 lakh crore", "₹11.2 lakh crore", "₹17.15 lakh crore", "₹10 lakh crore"],
  concept="Capital expenditure",
  explanation="The Finance Minister said public capex had risen from ₹2 lakh crore in FY 2014-15 to ₹11.2 lakh crore "
              "in BE 2025-26, and proposed ₹12.2 lakh crore for FY 2026-27 to continue the momentum.",
  steps=["BE 2025-26: ₹11.2 lakh crore", "FY 2026-27: ₹12.2 lakh crore"],
  why="₹11.2 lakh crore is the previous year's BE; ₹17.15 lakh crore is effective capex; ₹10 lakh crore is not a "
      "Budget figure.",
  current=BUD,
  facts=[fact("Public capex enhanced from ₹11.2 lakh crore in BE 2025-26 to ₹12.2 lakh crore in FY 2026-27", BUDGET)])
Q(T, "Union Budget highlights", "Basic",
  "The Union Budget 2026-27 proposed to raise the Securities Transaction Tax (STT) on futures to:",
  ["0.05% from 0.02%", "0.02% from 0.0125%", "0.1% from 0.05%", "0.0625% from 0.05%"],
  concept="Tax on derivatives trading",
  explanation="The Budget summary states that STT on futures was to be raised to 0.05% from the present 0.02%.",
  steps=["STT on futures: 0.02% → 0.05%"],
  why="The other pairs do not match the Budget proposal.",
  current=BUD,
  facts=[fact("STT on futures to be raised to 0.05% from present 0.02%", BUDGET)])
Q(T, "Union Budget highlights", "Basic",
  "'Biopharma Shakti', announced in the Union Budget 2026-27 with an outlay of ₹10,000 crore, aims to:",
  ["Build an ecosystem for domestic production of biologics and biosimilars", "Fund rural primary health centres",
   "Provide health insurance to gig workers", "Subsidise generic medicine stores"],
  concept="Sectoral initiatives",
  explanation="The Budget proposed Biopharma Shakti with an outlay of ₹10,000 crore to build the ecosystem for domestic "
              "production of biologics and biosimilars.",
  steps=["Biopharma Shakti: ₹10,000 crore, biologics and biosimilars"],
  why="The scheme is about biologics manufacturing, not PHCs, gig-worker insurance or medicine stores.",
  current=BUD,
  facts=[fact("Biopharma Shakti with an outlay of ₹10,000 crores to build the ecosystem for domestic production of "
              "biologics and biosimilars", BUDGET)])
Q(T, "Fiscal terms", "Intermediate",
  "What debt-to-GDP ratio of the Central Government did the Union Budget 2026-27 estimate for BE 2026-27?",
  ["55.6 per cent, down from 56.1 per cent in RE 2025-26", "56.1 per cent, up from 55.6 per cent",
   "50 per cent, the medium-term target", "60 per cent, unchanged"],
  concept="Debt-to-GDP path",
  explanation="The Budget estimated the debt-to-GDP ratio at 55.6% of GDP in BE 2026-27 compared with 56.1% in RE "
              "2025-26, saying a declining ratio frees resources for priority spending. The medium-term goal is 50 ± "
              "1% by 2030-31.",
  steps=["RE 2025-26: 56.1%", "BE 2026-27: 55.6%"],
  why="The second option reverses the figures; 50% is the 2030-31 goal; 60% is not the estimate.",
  current=BUD,
  facts=[fact("The debt-to-GDP ratio is estimated to be 55.6 percent of GDP in BE 2026-27, compared to 56.1 percent of "
              "GDP in RE 2025-26", BUDGET)])
Q(T, "Fiscal terms", "Intermediate",
  "What gross market borrowings did the Union Budget 2026-27 estimate for 2026-27?",
  ["₹17.2 lakh crore", "₹11.7 lakh crore", "₹12.2 lakh crore", "₹15.26 lakh crore"],
  concept="Government borrowing",
  explanation="The Budget estimated gross market borrowings at ₹17.2 lakh crore, with net market borrowings from dated "
              "securities at ₹11.7 lakh crore; the balance of the fiscal deficit is financed by small savings and "
              "other sources.",
  steps=["Gross: ₹17.2 lakh crore", "Net (dated securities): ₹11.7 lakh crore"],
  why="₹11.7 lakh crore is net borrowing; ₹12.2 lakh crore is capex; ₹15.26 lakh crore is tax devolution to States.",
  current=BUD,
  facts=[fact("The gross market borrowings are estimated at ₹17.2 lakh crore and the net market borrowings from dated "
              "securities are estimated at ₹11.7 lakh crore", BUDGET)])
Q(T, "Fiscal terms", "Intermediate",
  "As used in the Union Budget 2026-27, 'effective capital expenditure' of the Union Government includes:",
  ["Its own capital expenditure plus grants-in-aid to States for creation of capital assets",
   "Its capital expenditure minus loans to States", "Revenue expenditure on salaries plus capital expenditure",
   "Only capital expenditure of public sector enterprises"],
  concept="Effective capital expenditure",
  explanation="The Budget explains that effective capital expenditure of the Union Government includes GoI's capital "
              "expenditure (₹12.22 lakh crore) and grants-in-aid to States for creation of capital assets (₹4.93 lakh "
              "crore), totalling ₹17.15 lakh crore, 4.4% of GDP, in FY 2026-27.",
  steps=["Effective capex = capex + grants for capital assets"],
  why="Loans are not deducted; salaries are revenue spending; PSE capex is not the definition.",
  current=BUD,
  facts=[fact("Effective capital expenditure of the Union Government includes GoI's capital expenditure (₹12.22 lakh "
              "crore) and grants-in-aid to States (₹4.93 lakh crore) for creation of capital assets", BUDGET)])
Q(T, "Economic Survey highlights", "Intermediate",
  "What real GDP growth did the Economic Survey 2025-26 estimate for FY26 (2025-26), based on the first advance "
  "estimates?",
  ["7.4 per cent", "6.5 per cent", "8.2 per cent", "6.8 per cent"],
  concept="Economic Survey growth estimate",
  explanation="The Economic Survey 2025-26, tabled on 29 January 2026, put FY26 growth at 7.4% and projected FY27 "
              "growth in a range of 6.8–7.2%.",
  steps=["FY26: 7.4%", "FY27 projection: 6.8–7.2%"],
  why="6.8% is the lower end of the FY27 range; 6.5% was the earlier potential growth estimate; 8.2% is not the "
      "estimate.",
  current=SURV,
  facts=[fact("GDP expected to grow 6.8 to 7.2 per cent in 2026-27, slightly lower than 7.4 per cent expansion "
              "estimated for the current fiscal", ES_GDP)])

eff = 12.22 + 4.93
gdp_impl = eff / 0.044
assert round(eff, 2) == 17.15 and 385 < gdp_impl < 395
Q(T, "Fiscal terms", "Advanced",
  "The Union Budget 2026-27 put the Centre's capital expenditure at ₹12.22 lakh crore and grants-in-aid to States "
  "for capital assets at ₹4.93 lakh crore, and said effective capital expenditure equals 4.4% of GDP. What nominal "
  "GDP does this imply for 2026-27 (approx.)?",
  ["₹390 lakh crore", "₹278 lakh crore", "₹450 lakh crore", "₹520 lakh crore"],
  concept="Back-calculating GDP from a ratio",
  explanation="Effective capex = 12.22 + 4.93 = ₹17.15 lakh crore. If this is 4.4% of GDP, GDP ≈ 17.15 ÷ 0.044 ≈ "
              "₹390 lakh crore.",
  steps=["17.15 = 12.22 + 4.93", "GDP = 17.15 / 0.044 ≈ 390"],
  why="₹278 lakh crore uses only the ₹12.22 lakh crore capex; the other values do not fit the ratio.",
  computed=True, current=BUD,
  facts=[fact("The effective capital expenditure of Union Government in FY 2026-27 estimated at ₹17.15 lakh crore, that "
              "is 4.4% of GDP; includes GoI's capital expenditure (₹12.22 lakh crore) and grants-in-aid to States "
              "(₹4.93 lakh crore)", BUDGET)])

exp_g = (53.5 - 49.6) / 49.6 * 100
tax_g = (28.7 - 26.7) / 26.7 * 100
assert round(exp_g, 1) == 7.9 and round(tax_g, 1) == 7.5
Q(T, "Union Budget highlights", "Advanced",
  "The Budget put total expenditure at ₹49.6 lakh crore in RE 2025-26 and ₹53.5 lakh crore in BE 2026-27, and the "
  "Centre's net tax receipts at ₹26.7 lakh crore (RE) and ₹28.7 lakh crore (BE). Which statement is correct?",
  ["Expenditure grows about 7.9% and net tax receipts about 7.5%", "Expenditure grows about 7.5% and net tax receipts "
   "about 7.9%", "Both grow about 3.9%", "Net tax receipts grow faster, at about 10%"],
  concept="Growth rates in Budget numbers",
  explanation="Expenditure growth = (53.5 − 49.6)/49.6 ≈ 7.9%. Net tax growth = (28.7 − 26.7)/26.7 ≈ 7.5%. So "
              "spending is budgeted to grow slightly faster than net tax receipts.",
  steps=["(53.5 − 49.6)/49.6 ≈ 7.9%", "(28.7 − 26.7)/26.7 ≈ 7.5%"],
  why="The second option swaps the rates; 3.9 is the absolute rise in expenditure, not a percentage; tax growth is "
      "not 10%.",
  computed=True, current=BUD,
  facts=[fact("RE of total expenditure ₹49.6 lakh crore; Centre's net tax receipts RE ₹26.7 lakh crore; BE total "
              "expenditure ₹53.5 lakh crore; Centre's net tax receipts BE ₹28.7 lakh crore", BUDGET)])
Q(T, "Union Budget highlights", "Advanced",
  "Consider the following tax proposals in the Union Budget 2026-27:\nI. A single category of IT services with a "
  "common safe harbour margin of 15.5%, and the safe harbour threshold raised to ₹2,000 crore from ₹300 crore.\nII. "
  "The tariff rate on all dutiable goods imported for personal use cut from 20% to 10%.\nIII. Exemption from Minimum "
  "Alternate Tax for all resident companies.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Budget tax measures",
  explanation="The Budget proposed a single IT services category with a 15.5% safe harbour margin and a ₹2,000 crore "
              "threshold (up from ₹300 crore) (I correct), and a cut in the tariff on dutiable goods imported for "
              "personal use from 20% to 10% (II correct). The MAT exemption was for non-residents paying tax on a "
              "presumptive basis, not all resident companies (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (non-residents on presumptive basis)"],
  why="III misstates the MAT proposal; 'I only' omits II.",
  current=BUD,
  facts=[fact("Single category of information technology services with common safe harbour margin of 15.5%; 2000 crore "
              "threshold for availing safe harbour for IT services, up from 300 crore; tariff rate on all dutiable "
              "goods imported for personal use to be reduced from 20% to 10%; exemption from Minimum Alternate Tax to "
              "all non-residents paying tax on presumptive basis", BUDGET)])
Q(T, "Economic Survey highlights", "Advanced",
  "According to reports on the Economic Survey 2025-26, how did the Survey revise its estimate of India's medium-term "
  "potential real GDP growth (FY26–FY30)?",
  ["Raised to about 7 per cent from 6.5 per cent", "Lowered to 6.5 per cent from 7 per cent",
   "Raised to 8 per cent from 7 per cent", "Kept unchanged at 6.5 per cent"],
  concept="Potential growth",
  explanation="The Survey estimated that improvements in capital accumulation, labour inputs and total factor "
              "productivity have pushed potential real GDP growth to about 7% for the medium term (FY26–FY30), up "
              "from 6.5% earlier. The CEA said further reforms could lift it towards 7.5–8%.",
  steps=["Earlier: 6.5%", "Now: about 7% (FY26–FY30)"],
  why="It was raised, not lowered or kept unchanged; 8% was mentioned only as a possibility with further reforms.",
  current=SURV,
  facts=[fact("Calibrated improvements in capital accumulation, labour inputs, and trends in total factor productivity "
              "growth have pushed the potential real GDP growth to about 7 per cent for the medium term (FY26-FY30) "
              "from 6.5 per cent earlier", ES_POT)])

# ================================================================= 31. Government Financial Schemes (2 / 3 / 2)
T = "Government Financial Schemes"
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Basic",
  "The three social security schemes in insurance and pension — PMJJBY, PMSBY and APY — were launched by the Prime "
  "Minister on:",
  ["9 May 2015", "28 August 2014", "8 April 2015", "1 June 2015"],
  concept="Jan Suraksha schemes",
  explanation="DFS records that three social security schemes in the insurance and pension sectors were launched by "
              "the Prime Minister on 9 May 2015, to build a universal social security system, especially for the "
              "poor.",
  steps=["9 May 2015: PMJJBY, PMSBY, APY launched"],
  why="28 August 2014 is PMJDY; 8 April 2015 is PMMY; 1 June is the start of the insurance cover year.",
  facts=[fact("Three Social Security Schemes in the Insurance and Pension sectors were launched on 9th of May, 2015 by "
              "the Hon'ble Prime Minister", PMJDY_DFS)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Basic",
  "Under Atal Pension Yojana, what happens to the pension after the subscriber's death?",
  ["The spouse receives the same pension until the spouse's death", "The pension stops immediately",
   "The nominee receives half the pension for 10 years", "The pension is converted into a lump sum for the Government"],
  concept="APY family benefits",
  explanation="PFRDA's FAQs state that after the subscriber's death, the spouse is entitled to the same pension amount "
              "until the spouse's death; after both die, the nominee receives the pension wealth accumulated up to "
              "the subscriber's age 60.",
  steps=["Subscriber dies → spouse gets same pension", "Both die → nominee gets corpus"],
  why="The pension continues to the spouse; there is no half-pension rule; the corpus goes to the nominee, not the "
      "Government.",
  facts=[fact("After the subscriber's demise, the spouse of the subscriber shall be entitled to receive the same "
              "pension amount as that of the subscriber until the death of the spouse; after the demise of both, the "
              "nominee shall be entitled to receive the pension wealth", APY_FAQ)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Intermediate",
  "At what intervals can an Atal Pension Yojana subscriber choose to make contributions?",
  ["Monthly, quarterly or half-yearly, through auto-debit", "Only monthly, in cash",
   "Only annually, through a demand draft", "Weekly or monthly, through UPI only"],
  concept="APY contributions",
  explanation="APY contributions can be made monthly, quarterly or half-yearly through auto-debit from the "
              "subscriber's savings bank or post office savings account, and the frequency can be changed to suit "
              "the subscriber's earnings.",
  steps=["Frequencies: monthly / quarterly / half-yearly", "Mode: auto-debit"],
  why="APY is not limited to monthly cash, annual DD or weekly UPI payments.",
  facts=[fact("The contributions can be made at monthly / quarterly / half yearly intervals through auto debit facility "
              "from savings bank account/ post office savings bank account of the subscriber", APY_FAQ)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Intermediate",
  "If an Atal Pension Yojana subscriber dies before age 60, what option does the spouse have?",
  ["Continue the APY account under a new PRAN, contributing the same amount until the date the subscriber would have "
   "turned 60",
   "Only take back the contributions without interest", "Open a fresh account with a new pension amount of choice",
   "Transfer the corpus to PMJJBY"],
  concept="Continuation by spouse",
  explanation="Under PFRDA's exit guidelines, the spouse may continue the APY account: a new PRAN is generated, the "
              "spouse contributes the same amount as the deceased subscriber until the date the subscriber would "
              "have attained 60, and the balance units are transferred to the spouse's account.",
  steps=["New PRAN for spouse", "Same contribution", "Until subscriber's 60th birthday date", "Units transferred"],
  why="The spouse can continue rather than only exit; the pension amount stays the same; there is no transfer to "
      "PMJJBY.",
  facts=[fact("In case of death of the subscriber before 60 years, new PRAN will be generated in the name of the spouse "
              "and spouse will be allowed to contribute for the remaining period; spouse will be allowed to contribute "
              "same amount; the balance units will be transferred", APY_FAQ)])
Q(T, "Credit guarantee schemes", "Intermediate",
  "The Credit Guarantee Fund for Micro Units (CGFMU), managed by NCGTC as trustee, also covers which of the "
  "following?",
  ["Overdrafts of ₹10,000 sanctioned in PMJDY accounts", "Purely agricultural crop loans",
   "Home loans up to ₹50 lakh", "Education loans for study abroad"],
  concept="CGFMU coverage",
  explanation="NCGTC's FAQs state that CGFMU, a Government trust fund managed by NCGTC, guarantees micro loans up to "
              "₹20 lakh (above ₹10 lakh only for borrowers who repaid an earlier Tarun loan), and that overdrafts of "
              "₹10,000 under PMJDY are also eligible. Loans for purely agricultural activities are not covered.",
  steps=["CGFMU: micro loans (PMMY), PMJDY ODs", "Not: purely agricultural loans"],
  why="Purely agricultural loans are excluded; home and education loans are covered by other schemes.",
  facts=[fact("CGFMU is the Trust Fund set up by Government of India, managed by NCGTC as a Trustee; Overdraft facility "
              "of ₹10,000/- sanctioned under PMJDY accounts shall also be eligible to be covered; loan extended for "
              "purely agricultural activities are not eligible", CGFMU_FAQ)])

contrib = 210
per_month = -(-contrib // 100)  # ₹1 per ₹100 or part thereof
delays = [3, 2, 1]
penalty = per_month * sum(delays)
assert per_month == 3 and penalty == 18
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Advanced",
  "An APY subscriber's monthly contribution is ₹210. His June, July and August contributions are not debited for lack "
  "of balance and are all recovered in September, when June's is 3 months overdue, July's 2 and August's 1. Under "
  "the rule of ₹1 for every ₹100 of contribution (or part thereof) per month of delay, what overdue interest is "
  "collected?",
  ["₹18", "₹6", "₹12.60", "₹9"],
  concept="APY overdue interest",
  explanation="₹210 is three parts of ₹100 (two full and one part), so the charge is ₹3 per month of delay per "
              "contribution. Months of delay = 3 + 2 + 1 = 6. Overdue interest = ₹3 × 6 = ₹18, which is credited to "
              "the subscriber's pension corpus.",
  steps=["₹210 → 3 units of ₹100 or part → ₹3 per month", "Delay months = 6", "₹3 × 6 = ₹18"],
  why="₹6 counts one rupee per month; ₹12.60 uses exactly 1% of ₹210; ₹9 counts each contribution once.",
  computed=True,
  facts=[fact("For each delayed monthly contribution, the Banks are required to collect Rs.1 of every Rs.100 "
              "contribution, or part thereof, per month. The overdue interest collected will be credited to the APY "
              "account of the subscriber", APY_FAQ)])
Q(T, "Credit guarantee schemes", "Advanced",
  "Consider the following statements about the Credit Guarantee Fund for Micro Units (CGFMU):\nI. Micro loans above "
  "₹10 lakh and up to ₹20 lakh are eligible only for borrowers who earlier availed and repaid a Tarun loan.\nII. "
  "Guarantee cover is available for the base year plus three subsequent financial years.\nIII. Loans for purely "
  "agricultural activities are covered.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="CGFMU rules",
  explanation="NCGTC's FAQs say loans above ₹10 lakh up to ₹20 lakh are covered only for borrowers who repaid an "
              "earlier Tarun loan (I correct) and that guarantee cover runs for the base year plus three subsequent "
              "financial years, renewable for standard accounts (II correct). Purely agricultural loans are not "
              "eligible (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong"],
  why="III is false, so options with III fail; 'I only' omits II.",
  facts=[fact("Loans above Rs.10 lakh to Rs.20 lakh would be eligible to only such borrowers who had earlier availed "
              "loan in Tarun category and successfully repaid the same; tenure of guarantee cover is base year plus "
              "three subsequent financial years; loan extended for purely agricultural activities are not eligible",
              CGFMU_FAQ)])

# ================================================================= 32. RBI Circulars and Regulatory Updates (2 / 5 / 3)
T = "RBI Circulars and Regulatory Updates"
Q(T, "Recent RBI directions", "Basic",
  "In August 2026, RBI decided to resume licensing of which entities on an 'on tap' basis after a pause of about two "
  "decades?",
  ["Urban Co-operative Banks", "Payments banks", "Local Area Banks", "Regional Rural Banks"],
  concept="New UCB licences",
  explanation="RBI published a discussion paper on licensing of UCBs on 13 January 2026, following a two-decade pause "
              "on fresh licences. On 5 August 2026 it decided to resume licensing of UCBs on an 'on tap' basis, with "
              "draft guidelines to follow for consultation.",
  steps=["Jan 2026: discussion paper", "Aug 2026: on-tap licensing of UCBs to resume"],
  why="The announcement concerned UCBs, not payments banks, LABs or RRBs.",
  current=ca("2026-08-05"),
  facts=[fact("A discussion paper on Licensing of UCBs was published on January 13, 2026 following a two decade pause "
              "on issuance of fresh licenses... decided to resume licensing of UCBs on 'on tap' basis", SDRP_AUG26)])
Q(T, "Recent RBI directions", "Basic",
  "In August 2026, RBI said it would review the prudential norms on concentration risk for Rural Co-operative Banks. "
  "Under which instructions are these norms currently governed?",
  ["The Credit Monitoring Arrangement (CMA) instructions issued in 2008", "The Basel III framework of 2010",
   "The RB-IOS, 2026", "The SARFAESI Act, 2002"],
  concept="Concentration risk in rural co-operatives",
  explanation="RBI noted that concentration risk norms for Rural Co-operative Banks are governed by the Credit "
              "Monitoring Arrangement instructions of 2008 and, given changes in the sector, it would review them, "
              "issuing draft amendment directions for consultation.",
  steps=["Current basis: CMA instructions (2008)", "Aug 2026: review announced"],
  why="Basel III, RB-IOS and SARFAESI do not govern RCB concentration norms.",
  current=ca("2026-08-05"),
  facts=[fact("Prudential norms on Concentration Risk Management of Rural Co-operative Banks (RCBs) are governed by the "
              "Credit Monitoring Arrangement (CMA) instructions issued in 2008... decided to review", SDRP_AUG26)])
Q(T, "Recent RBI directions", "Intermediate",
  "To make it easier for MSMEs to join the Trade Receivables Discounting System (TReDS), what did RBI propose in April "
  "2026?",
  ["Dispensing with the requirement of due diligence of MSMEs while onboarding them on TReDS platforms",
   "Making TReDS registration compulsory for all MSMEs", "Allowing only banks to participate in TReDS",
   "Capping invoice discounting at ₹10 lakh"],
  concept="TReDS",
  explanation="TReDS guidelines were issued in 2014, updated in 2018, and expanded in 2023 to include insurance "
              "companies as a fourth participant. In April 2026 RBI proposed to dispense with due diligence of MSMEs "
              "while onboarding them on TReDS, to promote ease of doing business.",
  steps=["2014: guidelines", "2023: insurers added as fourth participant", "Apr 2026: drop MSME due diligence"],
  why="RBI did not make registration compulsory, restrict participants or cap invoices.",
  current=ca("2026-04-08"),
  facts=[fact("Scope of TReDS was further expanded in 2023 with the inclusion of insurance companies as the fourth "
              "participant... proposed to dispense with the requirement of due diligence of MSMEs while onboarding "
              "on TReDS platforms", SDRP_APR26)])
Q(T, "Recent RBI directions", "Intermediate",
  "In April 2026, RBI proposed to dispense with the Investment Fluctuation Reserve (IFR) requirement for which "
  "banks?",
  ["Commercial banks including Local Area Banks, but excluding SFBs, payments banks and RRBs",
   "Only Regional Rural Banks", "Only small finance banks and payments banks", "All co-operative banks"],
  concept="Investment Fluctuation Reserve",
  explanation="Since commercial banks (including LABs, but excluding SFBs, payments banks and RRBs) already maintain a "
              "capital charge for market risk and follow revised investment norms, RBI proposed to dispense with IFR "
              "for them, and to revise IFR rules for other bank categories.",
  steps=["IFR dropped (proposal): commercial banks incl. LABs", "Excluded: SFBs, PBs, RRBs (rules to be revised)"],
  why="RRBs, SFBs and payments banks are the excluded categories; co-operative banks are not the target.",
  current=ca("2026-04-08"),
  facts=[fact("Commercial banks (including Local Area Banks, but excluding Small Finance Banks, Payment Banks and "
              "Regional Rural Banks) already maintain capital charge for market risk... proposed to dispense with the "
              "IFR requirement for such commercial banks", SDRP_APR26)])
Q(T, "Recent RBI directions", "Intermediate",
  "Commercial banks may include quarterly net profits in CRAR only if incremental NPA provisions at the end of any "
  "quarter of the previous year did not deviate by more than 25% from the four-quarter average. What did RBI propose "
  "about this condition in April 2026?",
  ["To dispense with it", "To tighten it to 10%", "To extend it to RRBs and LABs", "To make it a monthly test"],
  concept="Quarterly profits in capital",
  explanation="RBI noted that commercial banks (excluding RRBs and LABs) can count quarterly net profits in CRAR "
              "subject to the 25% deviation condition on incremental NPA provisions, and proposed to dispense with "
              "this condition, with draft directions to follow.",
  steps=["Existing: 25% deviation test", "April 2026 proposal: dispense with the condition"],
  why="RBI proposed removing the test, not tightening, extending or making it monthly.",
  current=ca("2026-04-08"),
  facts=[fact("Permitted to include quarterly net profits in the calculation of CRAR provided that the incremental "
              "provisions made for NPAs... have not deviated more than 25 per cent of the average of the four "
              "quarters. On a review, it is proposed to dispense with this condition", SDRP_APR26)])
Q(T, "Recent RBI directions", "Intermediate",
  "After consolidating its regulatory instructions in 2025, RBI carried out a similar exercise for supervisory "
  "instructions. How many draft Master Directions did it publish for comments in April 2026?",
  ["64", "238", "244", "9"],
  concept="Consolidation of supervisory instructions",
  explanation="RBI's April 2026 statement said the drafts of 64 Master Directions consolidating supervisory "
              "instructions on up to nine functional areas were being published for public comments.",
  steps=["Supervisory consolidation: 64 draft MDs", "Up to nine functional areas"],
  why="238 and 244 relate to the regulatory consolidation; 9 is the number of functional areas.",
  current=ca("2026-04-08"),
  facts=[fact("The drafts of 64 Master Directions consolidating extant supervisory instructions on up to nine "
              "functional areas are being published today on RBI website for public comments", SDRP_APR26)])
Q(T, "Recent RBI directions", "Intermediate",
  "Under RBI's directions of 15 September 2025 on Payment Aggregators – Cross-Border (PA-CB), what net worth must an "
  "applicant have?",
  ["₹15 crore when applying and ₹25 crore by the third financial year of authorisation",
   "₹25 crore when applying and ₹50 crore by the third year", "₹5 crore throughout", "₹100 crore when applying"],
  concept="Payment aggregators",
  explanation="RBI's Payment System Report notes that the PA-CB directions require a minimum net worth of ₹15 crore "
              "when applying and ₹25 crore by the third financial year after authorisation, no co-mingling of "
              "inward and outward funds, and a cap of ₹25 lakh per inward or outward transaction.",
  steps=["Application: ₹15 crore", "By 3rd FY: ₹25 crore", "Per transaction cap: ₹25 lakh"],
  why="The other net worth figures are not in the directions.",
  current=PSR,
  facts=[fact("The directions on PAs-CB require entities to have a minimum net worth of ₹15 crore at the time of "
              "tendering application for authorisation and ₹25 crore by the third financial year; maximum value of "
              "₹25 lakh per transaction", PSR_MAY26)])

usd_mn, inr_per_usd = 4, 88
notional_cr = usd_mn * 1e6 * inr_per_usd / 1e7
ferr_cr = 0.20 * notional_cr
assert round(notional_cr, 2) == 35.2 and round(ferr_cr, 2) == 7.04
Q(T, "Recent RBI directions", "Advanced",
  "On 15 October 2026 an importer buys USD 4 million forward against INR from an Authorised Dealer to hedge import "
  "payments (a current account transaction). If the exchange rate is ₹88 per USD, what Foreign Exchange Risk Reserve "
  "(FERR) must the AD maintain with RBI under the directions of 10 October 2026?",
  ["₹7.04 crore in cash with RBI, until the contract ends", "₹3.52 crore", "Nil, because the contract is below USD 5 "
   "million", "₹35.2 crore"],
  concept="Foreign Exchange Risk Reserve",
  explanation="FERR applies to INR forex derivative contracts with users above USD 2 million notional, for hedging "
              "current account transactions where the user buys foreign currency. It equals 20% of the INR notional: "
              "USD 4 million × ₹88 = ₹35.2 crore; 20% = ₹7.04 crore, kept in cash with RBI daily until the contract "
              "terminates.",
  steps=["Notional = 4,000,000 × 88 = ₹35.2 crore", "FERR = 20% × 35.2 = ₹7.04 crore"],
  why="₹3.52 crore uses 10%; the threshold is USD 2 million, not 5 million; ₹35.2 crore is the whole notional.",
  computed=True, current=ca("2026-10-10"),
  facts=[fact("FERR applicable to all foreign exchange derivative contracts involving INR of notional value exceeding "
              "USD two million equivalent undertaken for hedging current account transactions where the user is "
              "purchasing foreign currency against INR; equal to 20 per cent of the INR equivalent of the notional "
              "amount; maintained by way of cash with the Reserve Bank on a daily basis until termination", FERR)])
Q(T, "Recent RBI directions", "Advanced",
  "Consider the following statements about RBI's Foreign Exchange Risk Reserve (FERR) directions of October 2026:\n"
  "I. Splitting a hedge into several smaller contracts with different ADs to stay below the threshold is treated as a "
  "violation.\nII. ADs report the FERR maintained daily through RBI's CIMS portal.\nIII. The FERR applies to "
  "contracts where an exporter sells foreign currency against INR.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="FERR safeguards",
  explanation="Attempts to circumvent the threshold through multiple transactions with one or more ADs are a violation "
              "(I correct); ADs report FERR daily through CIMS (II correct). FERR applies where the user is purchasing "
              "foreign currency against INR, not selling it (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (applies to purchases of foreign currency)"],
  why="III reverses the direction, so options with III fail; 'I only' omits II.",
  current=ca("2026-10-10"),
  facts=[fact("Any attempt by users to circumvent the requirements through undertaking multiple transactions with one "
              "or more Authorised Dealers shall be considered as a violation; ADs shall report the details of the FERR "
              "maintained on a daily basis through CIMS; applies where the user is purchasing foreign currency against "
              "INR", FERR)])

claim, cover = 6.0, 5.0
assert min(claim, cover) == 5.0
Q(T, "Recent RBI directions", "Advanced",
  "A depositor's unclaimed deposit of ₹6 lakh (with interest), insured by DICGC, was transferred to the DEA Fund. The "
  "bank later goes into liquidation and the depositor claims the money. Under RBI's 2025 directions on the DEA Fund, "
  "how much does the Fund pay, and to whom?",
  ["₹5 lakh, to the liquidator", "₹6 lakh, directly to the depositor", "₹5 lakh, directly to the depositor",
   "Nothing, because the bank is under liquidation"],
  concept="DEA Fund claims in liquidation",
  explanation="For a bank under liquidation, if the deposit was covered by DICGC when transferred, the Fund pays the "
              "liquidator an amount equal to the insured deposit. With cover of ₹5 lakh and a claim of ₹6 lakh, the "
              "Fund pays ₹5 lakh to the liquidator, who pays the depositor.",
  steps=["Claim 6 > cover 5 → insured amount 5", "Paid to the liquidator"],
  why="The Fund pays the liquidator, not the depositor, and only up to the insured amount; liquidation does not bar "
      "the claim.",
  computed=True,
  facts=[fact("Illustration 2 (DICGC Insurance Cover is up to ₹5 lakh): deposit claim of ₹6 lakh in a bank under "
              "liquidation... The Fund shall pay an amount equal to the insured deposit to the Liquidator (₹5 lakh)",
              PB_MISC)])


# ================================================================= checks and output
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_003_plan.json").read_text(encoding="utf-8"))
spec = next(s for s in plan["subjects"] if s["subject"] == BF)
planned = {(t["topic"], d): n for t in spec["topics"] for d, n in t["quota"].items() if n}
subtopics = {t["topic"]: set(t["subtopics"]) for t in spec["topics"]}
have = Counter((q["topic"], q["difficulty"]) for q in questions)
assert have == Counter(planned), sorted(set(have.items()) ^ set(planned.items()))
assert all(q["subtopic"] in subtopics[q["topic"]] for q in questions), \
    [(q["topic"], q["subtopic"]) for q in questions if q["subtopic"] not in subtopics[q["topic"]]]
assert len(questions) == spec["total"] == 200
lo, hi = spec["question_ids"]
assert questions[0]["question_id"] == lo and questions[-1]["question_id"] == hi
assert len({q["question_text"] for q in questions}) == len(questions)
assert all(q["verification"]["fact_checks"] for q in questions)
assert all(q.get("current_affairs") for q in questions if q["topic"] in ("Repo Rate", "Budget and Economic Survey"))
for q in questions:
    ev = q.get("current_affairs", {}).get("event_date")
    assert ev is None or ev <= TODAY, (q["question_id"], ev)
assert max(_keys.values()) - min(_keys.values()) <= 4, _keys

# ---------------------------------------------------------------- superseded-rules audit (2026-11-06)
# These questions were rewritten to the current rule, or reframed as historical (dated, past tense), after checking
# current RBI/SEBI/Government texts on 2026-11-06. IDs, topics, subtopics, difficulty and keys are unchanged. Any
# earlier ai:independent-check is dropped because the revised wording has not been re-solved blind.
AUDIT_REVISED = {"BANK_BFA_000454", "BANK_BFA_000542", "BANK_BFA_000543", "BANK_BFA_000544", "BANK_BFA_000545"}
assert AUDIT_REVISED <= {q["question_id"] for q in questions}
for q in questions:
    if q["question_id"] in AUDIT_REVISED:
        v = q["verification"]
        v["verified_by"] = [x for x in v["verified_by"] if x != "ai:independent-check"]
        v["verified_at"] = AUDIT_DAY

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_003",
    "created_at": TODAY,
    "notes": "BATCH_003 Banking and Financial Awareness part: 200 original questions (60 Basic, 80 Intermediate, "
             "60 Advanced) across 32 topics, IDs BANK_BFA_000404 to BANK_BFA_000603. Built mostly from primary texts "
             "opened on 2026-11-05: RBI history chronology, RBI FAQs (currency, NRI, RTGS, NEFT, LEI, e-rupee, "
             "RB-IOS 2026), Master Directions (IRAC, PSL, SFB, digital lending, digital banking channels), MPC "
             "resolutions and Statements on Developmental and Regulatory Policies of April–October 2026, October 2026 "
             "circulars (FERR, forex derivatives, Delhi lead banks, leverage ratio, operational risk), RBI Payment "
             "System Report (May 2026) and payments booklet, DICGC, IBBI, BIS, DFS, PFRDA, NCGTC, NABARD, LIC, SEBI, "
             "IRDAI, AMFI and the PIB Budget 2026-27 summary. Facts available only through search results (NPCI and "
             "PIB pages return 403; no workaround attempted) are marked web:search-confirmed. Changeable values carry "
             "current_affairs dates. Computed answers are re-derived in tools/batch_003/banking.py. Facts tested in "
             "BATCH_000–BATCH_002 are not repeated.",
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_003_BFA.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions; keys {dict(sorted(_keys.items()))})")
