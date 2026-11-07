"""Writes batches/parts/BATCH_002_BFA.json: the 200 Banking and Financial Awareness questions of BATCH_002.

Every fact is backed by at least one fact_check whose source was opened on 2026-11-05 (fetched and read), or, where
the official page could not be fetched, confirmed through web search results (those questions carry
web:search-confirmed). Values that can change (rates, limits, office-holders, Budget and Economic Survey figures,
recent directions) carry current_affairs dates taken from the source. Every computable answer is re-derived below
with assertions, the quota per (topic, difficulty) is checked against the batch plan, and the answer keys are
balanced. If any check fails, nothing is written. Facts tested in BATCH_000 / BATCH_001 were not repeated.

    python tools/batch_002/banking.py      (run from anywhere)
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
FIRST_ID = 204
SECONDS = {"Basic": 20, "Intermediate": 30, "Advanced": 60}

_rng = random.Random(2026110502)
_keys = Counter()
questions = []

# ---------------------------------------------------------------- sources
# Opened (fetched and read) on 2026-11-05
PIB_BUDGET = "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc202621776101.pdf"
ES_FISCAL = "https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2220005&reg=3&lang=2"
ES_GROWTH = "https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2219912&reg=3&lang=1"
MPC_OCT26 = "https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=63742"
MPC_DEC25 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=61749"
MP_OVERVIEW = "https://www.rbi.org.in/scripts/FS_Overview.aspx?fn=2752"
CRR99 = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=13736&Mode=0"
CRR_PENAL = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12832"
CRR_SLR_MC = "https://www.rbi.org.in/commonman/english/scripts/Notification.aspx?Id=1476"
IRAC_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13146"
PSL_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12799"
SFB_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13135"
PB_GUIDE = "https://www.rbi.org.in/scripts/bs_viewcontent.aspx?Id=2900"
RTGS_FAQ = "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=275"
NEFT_FAQ = "https://rbi.org.in/Scripts/faqview.aspx?Id=60"
ERUPEE_FAQ = "https://www.rbi.org.in/commonman/English/scripts/FAQs.aspx?Id=3686"
CURRENCY_FAQ = "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=3158"
ORG = "https://www.rbi.org.in/commonman/english/Scripts/Organisation.aspx"
CHRON_68 = "https://rbi.org.in/history/Brief_Chro1968to1985.html"
RBIOS_FAQ = "https://www.rbi.org.in/commonperson/english/scripts/FAQs.aspx?Id=3407"
DL_2025 = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12848"
DBC_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13163"
FAME = "https://www.rbi.org.in/commonman/images/FAME202426022024.pdf"
DEAF_FAQ = "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=3578"
MINOR_2025 = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12835&Mode=0"
NOM_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2181734&reg=48&lang=2"
BLA_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2150371&reg=48&lang=2"
RRB_CAP = "https://www.pib.gov.in/newsite/PrintRelease.aspx?relid=69732&reg=3&lang=2"
RRB_DFS = "https://financialservices.gov.in/regional-rural-banks-0"
BCBS_HIST = "https://www.bis.org/bcbs/history.htm"
CAP_TABLE = "https://www.rbi.org.in/scripts/bs_viewcontent.aspx?Id=4364"
DSIB_2025 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=61729"
IMPS_RBI = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=52368"
PAY_BOOKLET = "https://www.rbi.org.in/scripts/PublicationsView.aspx?Id=20315"
BBPS_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12616"
UPI_CL = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=12532&Mode=0"
DFS_YE25 = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2213154&reg=3&lang=2"
BANK_IN = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=12837&Mode=0"
DPI_PR = "https://rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=62213"
FI_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2298306&reg=48&lang=2"
PMJDY12 = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2303643&reg=3&lang=1"
NSFI = "https://www.rbi.org.in/commonman/Upload/English/Content/PDFs/English12052026.pdf"
GSEC_FAQ = "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=711"
SENSEX = "https://beta.bseindia.com/Sensex/bse_sensex.aspx"
ICDR_FAQ = "https://www.sebi.gov.in/sebi_data/faqfiles/may-2025/1747290561386.pdf"
AMFI_HIST = "https://www.amfiindia.com/investor/knowledge-center-info?zoneName=HistoryOfMutualFundsInIndia"
SIF_FAQ = "https://www.sebi.gov.in/sebi_data/faqfiles/sep-2026/1790074512985.pdf"
INS_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2206011&reg=3&lang=1"
PMJJBY = "https://financialservices.gov.in/pradhan-mantri-jeevan-jyoti-bima-yojana-pmjjby"
PMSBY = "https://financialservices.gov.in/pradhan-mantri-suraksha-bima-yojana-pmsby"
CGSS_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2127843&reg=48&lang=2"
MUDRA_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2249915&reg=3&lang=1"
STANDUP = "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2022/apr/doc20224535701.pdf"
GOLD_MD = "https://rbi.org.in/scripts/NotificationUser.aspx?Mode=0&Id=12859"
PREPAY = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12968&Mode=0"
AFA_MD = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12898"
CPI_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2291051&reg=48&lang=2"
SARFAESI_SC = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=1730&Mode=0"
IBBI_FAQ = "https://ibbi.gov.in/uploads/faqs/CIRPFAQs%20Final2408.pdf"
MERGER3_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=1558218"
MERGER3_EFF = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=1569934&reg=48&lang=2"
FMC_PIB = "https://www.pib.gov.in/newsite/printrelease.aspx?relid=128260"
SBI_ASSOC = "https://www.rbi.org.in/Scripts/bs_viewcontent.aspx?Id=2491"

# Confirmed only through search results (official page not fetchable, e.g. rbidocs PDFs behind a bot check)
MPC_AUG26 = "https://rbidocs.rbi.org.in/rdocs/PressRelease/PDFs/PR80907599DE5FD164918A49085C9D6270116.PDF"
FI_INDEX_25 = "https://rbidocs.rbi.org.in/rdocs/PressRelease/PDFs/PR759945E4AFFA6784A03A696159A59C25F3E.PDF"
NAYAK = "https://rbi.org.in/Scripts/PublicationReportDetails.aspx?ID=784"
BBB_AR = "https://rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1179"
BMB_PR = "https://www.rbi.org.in/commonman/Upload/English/PressRelease/PDFs/PR2535TL22032017.PDF"
T0_SEBI = "https://www.sebi.gov.in/sebi_data/meetingfiles/may-2024/1714651311614_1.pdf"
PMJAY70 = "https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=2053881&lang=2&reg=48"
SEARCH_ONLY = {MPC_AUG26, FI_INDEX_25, NAYAK, BBB_AR, BMB_PR, T0_SEBI, PMJAY70}


def fact(claim, url):
    return {"claim": claim, "source_url": url, "checked_on": TODAY}


AUDIT_DAY = "2026-11-06"  # superseded-rules audit of 2026-11-06


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


def inr(x):
    """Indian digit grouping for whole numbers: 945205 -> 9,45,205."""
    s = str(int(x))
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    return ",".join([head, *parts, tail]) if head else ",".join([*parts, tail])


assert inr(945205) == "9,45,205" and inr(5356) == "5,356"

# Policy rates after the MPC decision of 7 October 2026 (prid=63742; RBI home page on 2026-11-05)
REPO, SDF, MSF, BANK_RATE = 5.50, 5.25, 5.75, 5.75
assert abs(SDF - (REPO - 0.25)) < 1e-9 and abs(MSF - (REPO + 0.25)) < 1e-9 and BANK_RATE == MSF
CORRIDOR = ca("2026-10-07")
BUDGET = ca("2026-02-01")
SURVEY = ca("2026-01-29")

# ================================================================= 1. Banking Fundamentals (5 / 3 / 2)
T = "Banking Fundamentals"
Q(T, "Types of accounts", "Basic",
  "As per RBI, a savings or current account is treated as 'inoperative' when there have been no customer-induced "
  "transactions in it for a period of over:",
  ["Two years", "One year", "Five years", "Ten years"],
  concept="Inoperative accounts",
  explanation="RBI treats a savings or current account as inoperative if there are no customer-induced transactions "
              "in it for over two years. Such accounts are segregated to reduce the risk of fraud, and they can be "
              "reactivated by updating KYC at any branch, free of charge.",
  steps=["No customer-induced transaction for more than 2 years → inoperative"],
  why="Ten years is the period after which the balance goes to the DEA Fund; one and five years are not RBI's "
      "inoperative-account period.",
  facts=[fact("A savings/current account shall be treated as inoperative if there are no customer induced "
              "transactions for a period of over two years", FAME)])
Q(T, "Types of accounts", "Basic",
  "Credit balances in a bank deposit account that has not been operated for how long are transferred to RBI's "
  "Depositor Education and Awareness (DEA) Fund?",
  ["10 years or more", "2 years or more", "5 years or more", "7 years or more"],
  concept="DEA Fund",
  explanation="Under the DEA Fund Scheme, 2014, banks transfer to the DEA Fund the credit balance of any deposit "
              "account not operated for 10 years or more, and any amount unclaimed for 10 years or more. The "
              "depositor can still claim the money from the bank later.",
  steps=["Inoperative/unclaimed for 10 years → transferred to DEA Fund"],
  why="Two years makes an account inoperative but it stays with the bank; 5 and 7 years are not the DEA threshold.",
  facts=[fact("Amounts credited to DEA Fund are credit balances in deposit accounts not operated for 10 years or "
              "more, or unclaimed for 10 years or more", DEAF_FAQ)])
Q(T, "Types of accounts", "Basic",
  "Under RBI's April 2025 instructions on deposit accounts of minors, minors above what minimum age limit may be "
  "allowed by banks to open and operate savings or term deposit accounts independently?",
  ["An age limit fixed by the bank that is not less than 10 years", "Exactly 18 years",
   "An age limit fixed by the bank that is not less than 15 years", "Any age, without a guardian"],
  concept="Minors' accounts",
  explanation="RBI's circular of 21 April 2025 lets banks allow minors above an age limit of not less than 10 years "
              "(and up to the amounts and terms the bank fixes under its risk policy) to open and operate savings "
              "or term deposit accounts independently. Minors' accounts must never be overdrawn.",
  steps=["Bank fixes the age limit", "That limit cannot be below 10 years"],
  why="18 years is majority, when no such permission is needed; the floor is 10, not 15; a minor of any age can "
      "open an account only through a guardian.",
  current=ca("2025-04-21"),
  facts=[fact("Minors above such an age limit not less than 10 years ... may be allowed to open and operate "
              "savings/term deposit accounts independently (circular dated April 21, 2025)", MINOR_2025)])
Q(T, "Types of banks", "Basic",
  "The issued capital of a Regional Rural Bank is subscribed by the Central Government, the State Government and "
  "the sponsor bank in which proportion?",
  ["50% : 15% : 35%", "50% : 35% : 15%", "35% : 15% : 50%", "51% : 24% : 25%"],
  concept="Ownership of RRBs",
  explanation="RRBs, set up under the Regional Rural Banks Act, 1976, are jointly owned by the Government of India, "
              "the State Government concerned and the sponsor bank, which subscribe the issued capital in the "
              "proportion 50%, 15% and 35% respectively.",
  steps=["Centre 50%", "State 15%", "Sponsor bank 35%"],
  why="The sponsor bank holds 35%, not 15%; the Centre holds 50%; 51:24:25 is not the RRB pattern.",
  facts=[fact("The issued capital of RRBs is subscribed by Central Government, State Government and sponsor banks "
              "in the proportion of 50%, 15% and 35%, respectively", RRB_CAP),
         fact("RRBs were established under the provisions of the RRBs Act, 1976", RRB_DFS)])
Q(T, "Types of accounts", "Basic",
  "How often is an individual entitled to one free full credit report, including the credit score, from each credit "
  "information company?",
  ["Once a calendar year", "Once a month", "Once a quarter", "Only once in a lifetime"],
  concept="Credit reports",
  explanation="RBI's financial awareness material states that individuals can access one free full credit report "
              "(FFCR), including the credit score, once a calendar year from the credit information companies. A "
              "higher score usually lets a borrower get loans at a lower rate.",
  steps=["Free full credit report: once every calendar year"],
  why="The free report is annual, not monthly or quarterly, and it is not a one-time facility.",
  facts=[fact("Individuals have access to one free full credit report (FFCR) including credit score, once a "
              "calendar year", FAME)])
Q(T, "Types of accounts", "Intermediate",
  "From 1 November 2025, under the Banking Laws (Amendment) Act, 2025, how many nominees can a depositor name for a "
  "deposit account?",
  ["Up to four", "Only one", "Up to two", "Up to ten"],
  concept="Multiple nominations",
  explanation="Sections 10 to 13 of the Banking Laws (Amendment) Act, 2025, which deal with nomination, came into "
              "force on 1 November 2025. A customer may nominate up to four persons, simultaneously (with shares "
              "adding to 100%) or successively, for deposit accounts.",
  steps=["Nomination provisions effective 1 Nov 2025", "Maximum four nominees"],
  why="Earlier only a single nominee was possible; two and ten are not the limits in the amended law.",
  current=ca("2025-11-01"),
  facts=[fact("Provisions on nomination effective 1st November 2025; customers may nominate up to four persons, "
              "either simultaneously or successively", NOM_PIB)])
Q(T, "Types of banks", "Intermediate",
  "The Banking Laws (Amendment) Act, 2025 redefined the threshold for 'substantial interest' in a company, a limit "
  "unchanged since 1968, from ₹5 lakh to:",
  ["₹2 crore", "₹50 lakh", "₹1 crore", "₹10 crore"],
  concept="Banking Laws (Amendment) Act, 2025",
  explanation="The provisions brought into force from 1 August 2025 raised the 'substantial interest' threshold "
              "from ₹5 lakh to ₹2 crore. The same stage also raised the maximum tenure of directors (other than "
              "the chairperson and whole-time directors) in co-operative banks from 8 to 10 years.",
  steps=["Old threshold ₹5 lakh (since 1968)", "New threshold ₹2 crore"],
  why="₹50 lakh, ₹1 crore and ₹10 crore are not the new threshold.",
  current=ca("2025-08-01"),
  facts=[fact("Redefine the threshold of 'substantial interest' from ₹5 lakh to ₹2 crore, a limit unchanged since "
              "1968; provisions in force from 1st August 2025", BLA_PIB)])
Q(T, "Types of accounts", "Intermediate",
  "The Depositor Education and Awareness (DEA) Fund was established by RBI under which provision?",
  ["Section 26A of the Banking Regulation Act, 1949", "Section 45ZA of the RBI Act, 1934",
   "Section 42 of the RBI Act, 1934", "Section 13 of the SARFAESI Act, 2002"],
  concept="Legal basis of the DEA Fund",
  explanation="RBI framed the DEA Fund Scheme, 2014 using its powers under Section 26A of the Banking Regulation "
              "Act, 1949, and the scheme came into effect on 24 May 2014. The fund receives unclaimed deposits of "
              "10 years or more and is used for depositor education and awareness.",
  steps=["DEA Fund → Section 26A, BR Act", "Scheme effective 24 May 2014"],
  why="Section 45ZA is on the inflation target, Section 42 on CRR, and Section 13 of SARFAESI on enforcement of "
      "security interest.",
  facts=[fact("DEA Fund Scheme, 2014 formulated by RBI under Section 26A of the BR Act, 1949; effective May 24, 2014",
              DEAF_FAQ)])

last_txn = dt.date(2016, 3, 14)
ten_years = last_txn.replace(year=last_txn.year + 10)
transfer_month = (ten_years.month % 12) + 1, ten_years.year + (ten_years.month == 12)
assert transfer_month == (4, 2026)
Q(T, "Types of accounts", "Advanced",
  "The last customer-induced transaction in Meera's savings account was on 14 March 2016, and the account has "
  "remained unoperated and unclaimed since then. Under the DEA Fund Scheme, when must the bank transfer the balance, "
  "and what happens to her right to the money?",
  ["On the last working day of April 2026, with accrued interest; she can still claim it from the bank",
   "On 14 March 2026, without interest; her claim lapses after that",
   "On the last working day of March 2026; she can claim it only from RBI",
   "On 14 March 2018, when the account became inoperative; she can claim it only from RBI"],
  concept="Timing of DEA Fund transfers",
  explanation="An account not operated for 10 years must be transferred, with accrued interest, on the last working "
              "day of the month following the month in which the 10 years are completed. Ten years end on 14 March "
              "2026, so the transfer is due on the last working day of April 2026. The money still belongs to the "
              "depositor, who claims it from the bank; the bank then claims a refund from the DEA Fund.",
  steps=["10 years complete: 14 March 2026", "Month subsequent: April 2026 → last working day",
         "Claim lies with the bank, with no time limit"],
  why="Transfer is not on the anniversary date or in the same month; inoperative status after two years does not "
      "trigger a transfer; claims are made to the bank, not to RBI, and they do not lapse.",
  computed=True,
  facts=[fact("Banks transfer the balance to the DEA Fund on the last working day of the month subsequent to the "
              "month of completing 10 years of continuous inoperative or unclaimed status", DEAF_FAQ),
         fact("A savings/current account is inoperative after two years without customer induced transactions",
              FAME)])
Q(T, "Types of accounts", "Advanced",
  "Consider the following statements about nomination under the Banking Laws (Amendment) Act, 2025:\nI. For a "
  "deposit account, a depositor may choose either simultaneous or successive nomination.\nII. For articles in safe "
  "custody and safety lockers, simultaneous nomination with fixed percentage shares is permitted.\nIII. In "
  "simultaneous nomination, the shares specified for the nominees must add up to 100 per cent.\nWhich of the above "
  "is/are correct?",
  ["I and III only", "I only", "II and III only", "I, II and III"],
  concept="Simultaneous and successive nomination",
  explanation="Depositors may opt for simultaneous or successive nomination for deposit accounts (I is right). In "
              "simultaneous nomination each of up to four nominees gets a specified share, and the shares must "
              "total 100% (III is right). For safe custody articles and lockers, only successive nomination is "
              "permitted (II is wrong).",
  steps=["I: correct", "II: wrong (lockers/safe custody: successive only)", "III: correct"],
  why="Any option including II is wrong, and 'I only' leaves out the correct statement III.",
  current=ca("2025-11-01"),
  facts=[fact("Deposit accounts: simultaneous or successive nominations; safe custody articles and lockers: only "
              "successive nominations; simultaneous shares must total 100 percent", NOM_PIB)])

# ================================================================= 2. History of Banking in India (2 / 3 / 3)
T = "History of Banking in India"
Q(T, "Nationalisation", "Basic",
  "The Lead Bank Scheme, which envisaged an 'area approach' to banking to meet credit gaps, was introduced in:",
  ["December 1969", "July 1955", "April 1980", "July 1982"],
  concept="Lead Bank Scheme",
  explanation="In December 1969, months after the nationalisation of 14 banks, the Lead Bank Scheme was introduced. "
              "It assigned districts to banks under an area approach so that credit gaps could be identified and "
              "met.",
  steps=["Lead Bank Scheme: December 1969"],
  why="July 1955 is the formation of SBI, April 1980 the second nationalisation and July 1982 the setting up of "
      "NABARD.",
  facts=[fact("Dec 1969: Lead Bank Scheme introduced which envisaged an area approach to banking to meet the credit "
              "gaps", CHRON_68)])
Q(T, "Mergers and consolidation", "Basic",
  "The first-ever three-way amalgamation in Indian banking, effective 1 April 2019, merged Vijaya Bank and Dena Bank "
  "into which bank?",
  ["Bank of Baroda", "Punjab National Bank", "Canara Bank", "Union Bank of India"],
  concept="PSB consolidation, 2019",
  explanation="The Union Cabinet approved the amalgamation of Vijaya Bank and Dena Bank (transferor banks) into Bank "
              "of Baroda (transferee bank) in January 2019. It took effect on 1 April 2019 and created India's "
              "second largest bank at the time.",
  steps=["Transferors: Vijaya Bank, Dena Bank", "Transferee: Bank of Baroda", "Effective 1 April 2019"],
  why="PNB, Canara Bank and Union Bank of India were transferee banks in the 2020 consolidation, not in 2019.",
  facts=[fact("Cabinet approves first-ever three way merger with amalgamation of Vijaya, Dena and Bank of Baroda",
              MERGER3_PIB),
         fact("The amalgamation comes into effect from 1st April 2019; the amalgamated bank will be named Bank of "
              "Baroda", MERGER3_EFF)])
Q(T, "Committees", "Intermediate",
  "The 1975 report that shifted bank lending for working capital from a security-based approach to a need-based "
  "approach linked to the borrower's production plans was submitted by the:",
  ["Tandon Committee", "Chore Committee", "Narasimham Committee", "Nayak Committee"],
  concept="Working capital finance norms",
  explanation="The Tandon Committee report (August 1975) emphasised correlating bank credit with borrowers' business "
              "or production plans and own resources. Its norms formed the basis of bank lending for working "
              "capital.",
  steps=["1975 + working capital + need-based lending → Tandon Committee"],
  why="The Chore Committee (1980) dealt with the cash credit system; Narasimham (1991) with financial sector "
      "reforms; Nayak (2014) with governance of bank boards.",
  facts=[fact("09 Aug 1975: Tandon Committee Report emphasized need to correlate bank credit to the business/ "
              "production plans; shift from security based to need based approach", CHRON_68)])
Q(T, "Mergers and consolidation", "Intermediate",
  "Along with five associate banks, which bank was merged with the State Bank of India with effect from 1 April "
  "2017?",
  ["Bharatiya Mahila Bank", "IDBI Bank", "Dena Bank", "Oriental Bank of Commerce"],
  concept="SBI merger, 2017",
  explanation="Under Government orders of February and March 2017, State Bank of Bikaner and Jaipur, State Bank of "
              "Hyderabad, State Bank of Mysore, State Bank of Patiala and State Bank of Travancore, and the "
              "Bharatiya Mahila Bank, merged with SBI with effect from 1 April 2017.",
  steps=["Five associates + Bharatiya Mahila Bank → SBI, 1 April 2017"],
  why="Dena Bank merged into Bank of Baroda (2019); Oriental Bank of Commerce into PNB (2020); IDBI Bank was not "
      "merged with SBI.",
  facts=[fact("Erstwhile associate banks (SBBJ, SBH, SBM, SBP, SBT) merged with SBI as per Government order dated "
              "February 22, 2017", SBI_ASSOC),
         fact("All branches of Bharatiya Mahila Bank Limited will function as branches of SBI from April 1, 2017",
              BMB_PR)])
Q(T, "Committees", "Intermediate",
  "The Banks Board Bureau, which started functioning in April 2016, was set up on the recommendation of the "
  "committee chaired by:",
  ["P. J. Nayak", "M. Narasimham", "Urjit R. Patel", "K. S. Chore"],
  concept="Governance of bank boards",
  explanation="RBI's Committee to Review Governance of Boards of Banks in India (chairman P. J. Nayak, report May "
              "2014) recommended a Bank Boards Bureau to advise on board appointments, as a step towards a Bank "
              "Investment Company. The Banks Board Bureau began functioning on 8 April 2016.",
  steps=["Governance of bank boards → P. J. Nayak Committee (2014)", "BBB functioning from 8 April 2016"],
  why="Narasimham chaired the banking sector reform committees; Urjit Patel the monetary policy framework "
      "committee; Chore the cash credit review.",
  facts=[fact("Committee to Review Governance of Boards of Banks in India report dated 13 May 2014", NAYAK),
         fact("Following the Nayak Committee recommendations, the BBB was set up and started functioning from "
              "April 8, 2016", BBB_AR)])
Q(T, "Nationalisation", "Advanced",
  "Arrange the following in chronological order:\nI. Formation of DICGC by merging the Deposit Insurance "
  "Corporation and the Credit Guarantee Corporation of India\nII. Introduction of the Lead Bank Scheme\nIII. "
  "Establishment of NABARD\nIV. Submission of the Tandon Committee report",
  ["II, IV, I, III", "II, I, IV, III", "IV, II, I, III", "II, IV, III, I"],
  concept="Chronology of banking institutions",
  explanation="Lead Bank Scheme: December 1969. Tandon Committee report: August 1975. DICGC formed with effect "
              "from 15 July 1978. NABARD established on 12 July 1982.",
  steps=["II: Dec 1969", "IV: Aug 1975", "I: Jul 1978", "III: Jul 1982"],
  why="Each other option misplaces either the Tandon report (1975) or NABARD (1982), which is the latest event.",
  facts=[fact("Lead Bank Scheme Dec 1969; Tandon Committee Report 9 Aug 1975; DICGC formed wef July 15, 1978; "
              "NABARD established 12 July 1982", CHRON_68)])
Q(T, "Committees", "Advanced",
  "Match the committee or body with its subject:\n1. Tandon Committee (1975)\n2. Chore Committee (1980)\n3. Banking "
  "Commission (1969)\n4. P. J. Nayak Committee (2014)\nP. Governance of boards of banks\nQ. Working capital "
  "finance on a need-based approach\nR. Review of the cash credit system\nS. Banking costs, banking legislation "
  "and indigenous banking",
  ["1-Q, 2-R, 3-S, 4-P", "1-R, 2-Q, 3-S, 4-P", "1-Q, 2-R, 3-P, 4-S", "1-S, 2-R, 3-Q, 4-P"],
  concept="Committees on Indian banking",
  explanation="Tandon (1975) tied working capital lending to production plans; Chore (recommendations adopted in "
              "December 1980) reviewed the cash credit system; the Banking Commission (set up January 1969) was "
              "to report on banking costs, legislation, indigenous banking and procedures; Nayak (2014) reviewed "
              "governance of bank boards.",
  steps=["1-Q", "2-R", "3-S", "4-P"],
  why="Swapping Tandon and Chore, or the Banking Commission and Nayak, gives the wrong subjects.",
  facts=[fact("Tandon Committee 1975 on need-based working capital; Chore Committee recommendations on the cash "
              "credit system adopted Dec 1980; Banking Commission set up 29 Jan 1969 to report on banking costs, "
              "legislation, indigenous banking", CHRON_68),
         fact("P. J. Nayak committee reviewed governance of boards of banks in India (2014)", NAYAK)])
Q(T, "Mergers and consolidation", "Advanced",
  "Consider the following statements:\nI. The amalgamation of Vijaya Bank and Dena Bank with Bank of Baroda was the "
  "first three-way consolidation of banks in India.\nII. The associate banks of SBI that merged with it in 2017 "
  "included State Bank of Travancore and State Bank of Patiala.\nIII. Vijaya Bank was merged into Canara Bank in "
  "2020.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Bank mergers 2017–2019",
  explanation="The BoB–Vijaya–Dena amalgamation (1 April 2019) was the first three-way consolidation (I right). "
              "SBBJ, SBH, SBM, SBP and SBT merged with SBI from 1 April 2017 (II right). Vijaya Bank became part of "
              "Bank of Baroda in 2019, not Canara Bank (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong"],
  why="Statement III is false, so options containing it are wrong; 'I only' omits the true statement II.",
  facts=[fact("First-ever three-way merger of Vijaya, Dena and Bank of Baroda", MERGER3_PIB),
         fact("State Bank of Bikaner and Jaipur, Hyderabad, Mysore, Patiala and Travancore merged with SBI w.e.f. "
              "April 1, 2017", SBI_ASSOC)])

# ================================================================= 3. Reserve Bank of India (2 / 4 / 2)
T = "Reserve Bank of India"
Q(T, "Establishment and structure", "Basic",
  "For what period are directors appointed or nominated to RBI's Central Board?",
  ["Four years", "Two years", "Three years", "Five years"],
  concept="Central Board of RBI",
  explanation="RBI's affairs are governed by a Central Board appointed by the Government of India under the RBI "
              "Act. Directors are appointed or nominated for a period of four years.",
  steps=["Central Board directors: four-year term"],
  why="Two, three and five years are not the term stated by RBI.",
  facts=[fact("Central Board appointed by the Government of India; appointed/nominated for a period of four years",
              ORG)])
Q(T, "Establishment and structure", "Basic",
  "According to the Preamble of the RBI Act as RBI describes it, the monetary policy framework aims to:",
  ["Maintain price stability while keeping in mind the objective of growth",
   "Maximise employment while keeping inflation below 2%",
   "Maintain a fixed exchange rate of the rupee", "Finance the fiscal deficit of the Government"],
  concept="RBI's mandate",
  explanation="RBI's Preamble describes its functions as regulating the issue of bank notes and keeping reserves "
              "for monetary stability, operating the currency and credit system, and having a modern monetary "
              "policy framework 'to maintain price stability while keeping in mind the objective of growth'.",
  steps=["Objective: price stability, keeping growth in mind"],
  why="A maximum-employment mandate belongs to other central banks; India has no fixed exchange-rate target; "
      "automatic financing of the deficit ended with ad hoc T-bills.",
  facts=[fact("Preamble: to have a modern monetary policy framework ... to maintain price stability while keeping "
              "in mind the objective of growth", ORG)])
Q(T, "Governors and leadership", "Intermediate",
  "Which of the following persons is NOT among RBI's Deputy Governors listed on RBI's Central Board in November "
  "2026?",
  ["Michael Debabrata Patra", "Swaminathan J", "Poonam Gupta", "Rohit Jain"],
  concept="RBI's top management",
  explanation="RBI's Central Board page lists Governor Sanjay Malhotra and four Deputy Governors: Swaminathan J, "
              "Dr. Poonam Gupta, Shirish Chandra Murmu and Rohit Jain. Michael Debabrata Patra is a former Deputy "
              "Governor and is not on the current list.",
  steps=["Current DGs: Swaminathan J, Poonam Gupta, S. C. Murmu, Rohit Jain", "M. D. Patra is not listed"],
  why="Swaminathan J, Poonam Gupta and Rohit Jain are all listed as Deputy Governors.",
  current=ca("2026-11-05"),
  facts=[fact("Central Board: Shri Sanjay Malhotra, Governor; Deputy Governors Shri Swaminathan J, Dr. Poonam Gupta, "
              "Shri Shirish Chandra Murmu, Shri Rohit Jain", ORG)])
Q(T, "Establishment and structure", "Intermediate",
  "Which of the following institutions is fully funded by the Reserve Bank of India?",
  ["Indira Gandhi Institute of Development Research (IGIDR)", "National Institute of Bank Management (NIBM)",
   "Indian Institute of Bank Management (IIBM)", "Indian Institute of Banking and Finance (IIBF)"],
  concept="Institutes funded by RBI",
  explanation="RBI lists CAFRAL and IGIDR as fully funded by it. For IIBM, RBI is a sponsor along with other banks; "
              "for NIBM it is an ordinary member. IDRBT is an autonomous training establishment, not a part of RBI.",
  steps=["Fully funded: CAFRAL, IGIDR", "IIBM: sponsor; NIBM: member; IDRBT: autonomous"],
  why="RBI is only an ordinary member of NIBM and one of the sponsors of IIBM; IIBF is not among the institutes RBI "
      "lists as fully funded by it.",
  facts=[fact("CAFRAL and IGIDR fully funded by RBI; RBI is a sponsor of IIBM and an ordinary member of NIBM; IDRBT "
              "is autonomous", ORG)])
Q(T, "Governors and leadership", "Intermediate",
  "Manmohan Singh, who later became Prime Minister, was appointed Governor of the Reserve Bank of India in:",
  ["September 1982", "May 1977", "February 1985", "June 1970"],
  concept="RBI Governors",
  explanation="RBI's chronology records Manmohan Singh's appointment as Governor on 16 September 1982. He was "
              "followed by A. Ghosh (briefly) and R. N. Malhotra in 1985.",
  steps=["Manmohan Singh: appointed 16 September 1982"],
  why="May 1977 is M. Narasimham's appointment, February 1985 R. N. Malhotra's and June 1970 S. Jagannathan's.",
  facts=[fact("16 Sep 1982: Manmohan Singh appointed Governor; 04 Feb 1985: RN Malhotra appointed Governor; 02 May "
              "1977: M. Narasimham; 16 Jun 1970: S. Jagannathan", CHRON_68)])
Q(T, "Establishment and structure", "Intermediate",
  "RBI's Board for Financial Supervision (BFS), which exercises integrated supervision over banks, financial "
  "institutions and NBFCs, was constituted in:",
  ["November 1994", "April 1935", "January 1949", "July 2016"],
  concept="Board for Financial Supervision",
  explanation="The BFS was constituted in November 1994 as a committee of RBI's Central Board under the RBI (Board "
              "for Financial Supervision) Regulations, 1994. The Department of Supervision provides it secretarial "
              "support.",
  steps=["BFS: November 1994, committee of the Central Board"],
  why="1935 is RBI's establishment, January 1949 its nationalisation, and 2016 relates to the MPC framework.",
  facts=[fact("BFS constituted in November 1994 as a committee of the Central Board under the RBI (BFS) "
              "Regulations, 1994; integrated supervision over commercial banks, FIs and NBFCs", ORG)])
Q(T, "Establishment and structure", "Advanced",
  "Which of the following Acts is NOT among those administered by the Reserve Bank of India, as listed by RBI?",
  ["Negotiable Instruments Act, 1881", "Credit Information Companies (Regulation) Act, 2005",
   "Factoring Regulation Act, 2011", "Payment and Settlement Systems Act, 2007"],
  concept="RBI's legal framework",
  explanation="RBI lists the Acts it administers: the RBI Act, Public Debt Act/Government Securities Act, BR Act, "
              "FEMA, SARFAESI (Chapter II), CIC (Regulation) Act 2005, PSS Act 2007 and Factoring Regulation Act "
              "2011. The Negotiable Instruments Act, 1881 appears only among 'other relevant Acts'.",
  steps=["Administered: CIC Act, PSS Act, Factoring Act, etc.", "NI Act: only 'relevant', not administered"],
  why="The CIC Act, Factoring Regulation Act and PSS Act are all in RBI's list of Acts it administers.",
  facts=[fact("Acts administered by RBI include the CIC (Regulation) Act 2005, PSS Act 2007 and Factoring "
              "Regulation Act 2011; the Negotiable Instruments Act 1881 is listed under other relevant Acts", ORG)])
Q(T, "Governors and leadership", "Advanced",
  "Arrange the following RBI Governors in the order of their appointment:\nI. S. Jagannathan\nII. R. N. Malhotra\n"
  "III. I. G. Patel\nIV. M. Narasimham",
  ["I, IV, III, II", "I, III, IV, II", "IV, I, III, II", "I, IV, II, III"],
  concept="RBI Governors 1970–1985",
  explanation="S. Jagannathan was appointed on 16 June 1970, M. Narasimham on 2 May 1977, I. G. Patel on 1 "
              "December 1977, and R. N. Malhotra on 4 February 1985.",
  steps=["I: Jun 1970", "IV: May 1977", "III: Dec 1977", "II: Feb 1985"],
  why="Narasimham's short tenure (May–November 1977) came just before I. G. Patel's; Malhotra came last.",
  facts=[fact("16 Jun 1970 S. Jagannathan; 02 May 1977 M. Narasimham; 01 Dec 1977 I.G. Patel; 04 Feb 1985 RN "
              "Malhotra appointed Governor", CHRON_68)])

# ================================================================= 4. RBI Functions (2 / 3 / 3)
T = "RBI Functions"
Q(T, "Issuer of currency", "Basic",
  "Rupee coins of one rupee and above are legal tender for any sum not exceeding how much in a single transaction?",
  ["₹1,000", "₹100", "₹10", "₹10,000"],
  concept="Legal tender limits for coins",
  explanation="Under the Coinage Act, 2011, a coin of one rupee or more is legal tender for any sum not exceeding "
              "₹1,000 in a single transaction, and the 50 paise coin for any sum not exceeding ₹10. Accepting more "
              "voluntarily is not prohibited.",
  steps=["₹1 and above: up to ₹1,000", "50 paise: up to ₹10"],
  why="₹10 is the limit for 50 paise coins; ₹100 and ₹10,000 are not legal-tender limits.",
  facts=[fact("Coin of any denomination not lower than one rupee shall be legal tender for any sum not exceeding "
              "one thousand rupee in any single transaction; fifty paise coin not exceeding ten rupee", CURRENCY_FAQ)])
Q(T, "Issuer of currency", "Basic",
  "The two banknote presses owned by RBI through its wholly owned subsidiary Bharatiya Reserve Bank Note Mudran Pvt. "
  "Ltd. (BRBNMPL) are located at:",
  ["Mysuru and Salboni", "Nashik and Dewas", "Mumbai and Hyderabad", "Kolkata and NOIDA"],
  concept="Currency printing",
  explanation="Banknotes are printed at four presses: SPMCIL (Government-owned) runs those at Nashik and Dewas, "
              "and BRBNMPL (RBI-owned) runs those at Mysuru and Salboni. Coins are minted at SPMCIL's mints at "
              "Mumbai, Hyderabad, Kolkata and NOIDA.",
  steps=["BRBNMPL presses: Mysuru, Salboni"],
  why="Nashik and Dewas are SPMCIL presses; Mumbai, Hyderabad, Kolkata and NOIDA are mints for coins.",
  facts=[fact("Two presses of BRBNMPL are at Mysuru and Salboni; SPMCIL presses at Nasik and Dewas; mints at Mumbai, "
              "Hyderabad, Kolkata and NOIDA", CURRENCY_FAQ)])
Q(T, "Issuer of currency", "Intermediate",
  "Under Section 24 of the RBI Act, 1934, bank notes can be issued in such other denominational values as the Central "
  "Government may specify on the Central Board's recommendation, but not exceeding:",
  ["₹10,000", "₹2,000", "₹5,000", "₹1,00,000"],
  concept="Denominations of bank notes",
  explanation="Section 24 lists denominations from ₹2 to ₹10,000 and allows other values the Central Government "
              "may specify on the Central Board's recommendation, 'not exceeding ten thousand rupees'. The highest "
              "note ever printed was the ₹10,000 note, last demonetised in 1978.",
  steps=["Ceiling under Section 24: ₹10,000"],
  why="₹2,000 is the highest note currently issued; ₹5,000 was an old denomination; ₹1 lakh is beyond the ceiling.",
  facts=[fact("Section 24: bank notes of such other denominational values, not exceeding ten thousand rupees, as the "
              "Central Government may specify", CURRENCY_FAQ)])
Q(T, "Issuer of currency", "Intermediate",
  "In January 1978, RBI's records show that banknotes of which denominations were demonetised?",
  ["₹1,000, ₹5,000 and ₹10,000", "₹500 and ₹1,000", "₹100, ₹500 and ₹1,000", "₹2,000 only"],
  concept="Demonetisations",
  explanation="High-denomination notes of ₹1,000, ₹5,000 and ₹10,000, reintroduced in 1954, were demonetised on "
              "16 January 1978 to curb illicit transfer of money. The ₹500 and ₹1,000 notes of the Mahatma Gandhi "
              "series were withdrawn in November 2016.",
  steps=["1978: ₹1,000, ₹5,000, ₹10,000"],
  why="₹500/₹1,000 is the 2016 demonetisation; ₹2,000 notes were withdrawn from circulation in 2023 but remain "
      "legal tender.",
  facts=[fact("Notes of Rs 1,000, Rs 5,000 and Rs 10,000 denominations demonetised on 16 Jan 1978", CHRON_68),
         fact("₹1000, ₹5000 and ₹10000 banknotes reintroduced in 1954 were again demonetized in January 1978",
              CURRENCY_FAQ)])
Q(T, "Banker to government", "Intermediate",
  "Which of the following describes RBI's role as banker to the Government, as stated by RBI?",
  ["It performs merchant banking functions for the Central and State governments and also acts as their banker",
   "It acts as banker only to the Central Government; States must bank with SBI",
   "It lends to the Government without limit to finance the fiscal deficit",
   "It acts as banker to the Government only for foreign exchange transactions"],
  concept="Banker to the Government",
  explanation="RBI describes its related function as banker to the Government: it performs merchant banking "
              "functions for the Central and State governments and also acts as their banker. As banker to banks, "
              "it maintains the banking accounts of all scheduled banks.",
  steps=["Banker to Central and State governments + merchant banking function"],
  why="States also bank with RBI; automatic unlimited financing of deficits does not exist; the role is not limited "
      "to foreign exchange.",
  facts=[fact("Banker to the Government: performs merchant banking function for the central and the state "
              "governments; also acts as their banker. Banker to banks: maintains banking accounts of all scheduled "
              "banks", ORG)])
Q(T, "Issuer of currency", "Advanced",
  "Consider the following statements about bank notes:\nI. 'Star series' notes replace defectively printed notes in "
  "a packet of 100 serially numbered notes.\nII. Two banknotes can carry the same serial number if they differ in "
  "inset letter, year of printing or the Governor's signature.\nIII. Non-sequential numbering of notes in packets "
  "was introduced in 2011.\nWhich of the above is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I only"],
  concept="Numbering of banknotes",
  explanation="RBI adopted the Star series to replace defectively printed notes in a packet of 100 serially numbered "
              "notes (I). Notes with the same serial number are possible if the inset letter, year of printing or "
              "Governor's signature differs (II). Non-sequential numbering was introduced in 2011 for efficiency "
              "(III). All three are correct.",
  steps=["I: correct", "II: correct", "III: correct"],
  why="Each of the other options leaves out at least one correct statement.",
  facts=[fact("Star series used for replacement of defectively printed banknotes in a packet of 100; same serial "
              "number possible with different inset letter, year or signature; non-sequential numbering introduced "
              "in 2011", CURRENCY_FAQ)])
Q(T, "Issuer of currency", "Advanced",
  "A shopkeeper is offered three payments in separate transactions: (P) ₹800 in ₹10 coins, (Q) ₹1,500 in ₹5 coins, "
  "(R) ₹20 in 50 paise coins. Under the Coinage Act, 2011, which of these can the shopkeeper NOT be compelled to "
  "accept?",
  ["Q and R", "Only Q", "Only R", "P, Q and R"],
  concept="Legal tender limits applied",
  explanation="Rupee coins (₹1 and above) are legal tender up to ₹1,000 in a single transaction, so P (₹800) must be "
              "accepted but Q (₹1,500) can be refused. 50 paise coins are legal tender only up to ₹10, so R (₹20) "
              "can be refused. Voluntary acceptance beyond these limits is not prohibited.",
  steps=["P: ₹800 ≤ ₹1,000 → must accept", "Q: ₹1,500 > ₹1,000 → can refuse", "R: ₹20 > ₹10 → can refuse"],
  why="Q alone or R alone misses one refusable payment; P is within the ₹1,000 limit.",
  computed=True,
  facts=[fact("Coins of ₹1 and above legal tender up to ₹1,000 in a single transaction; 50 paise coin up to ₹10; "
              "no one can be forced to accept coins beyond these limits", CURRENCY_FAQ)])
Q(T, "Regulator and supervisor", "Advanced",
  "Under the Specified Bank Notes (Cessation of Liabilities) Act, 2017, after the grace period, a person (not "
  "holding them for study, research or numismatics) may hold old ₹500/₹1,000 specified bank notes up to:",
  ["Ten notes in total, irrespective of denomination", "Twenty-five notes of each denomination",
   "Notes worth ₹10,000 in total", "No notes at all"],
  concept="Specified Bank Notes Act, 2017",
  explanation="Section 5 of the Act prohibits holding, transferring or receiving specified bank notes, but after "
              "the grace period a person may hold not more than ten notes in total irrespective of denomination, "
              "or not more than twenty-five notes for study, research or numismatics.",
  steps=["General holding limit: 10 notes in total", "For study/research/numismatics: 25 notes"],
  why="25 notes is the limit only for study, research or numismatics; the limit is by number, not value; some "
      "holding is permitted.",
  facts=[fact("After the grace period, not more than ten notes in total irrespective of denomination; or not more "
              "than twenty-five notes for study, research, or numismatics", CURRENCY_FAQ)])

# ================================================================= 5. Monetary Policy (4 / 3 / 2)
T = "Monetary Policy"
Q(T, "Transmission", "Basic",
  "In RBI's monetary policy toolkit, Open Market Operations (OMOs) are:",
  ["Outright purchase or sale of government securities to inject or absorb durable liquidity",
   "Overnight lending to banks against their SLR securities at a penal rate",
   "Changes in the share of deposits banks must keep as cash with RBI",
   "Directions to banks to restrict credit to particular sectors"],
  concept="Instruments of monetary policy",
  explanation="RBI describes OMOs as outright purchase or sale of government securities for injection or "
              "absorption of durable liquidity. Purchases inject liquidity; sales absorb it.",
  steps=["OMO = outright G-sec purchase/sale → durable liquidity"],
  why="Overnight penal lending is the MSF; the cash share is the CRR; sectoral restrictions are selective credit "
      "controls.",
  facts=[fact("Open Market Operations include outright purchase/sale of government securities by the Reserve Bank "
              "for injection/absorption of durable liquidity", MP_OVERVIEW)])
Q(T, "MPC structure", "Basic",
  "The first Monetary Policy Committee under Section 45ZB of the RBI Act was constituted on:",
  ["29 September 2016", "1 April 2016", "5 August 2016", "1 October 2024"],
  concept="MPC history",
  explanation="The RBI Act was amended in May 2016 to provide for flexible inflation targeting. The inflation "
              "target was notified on 5 August 2016, and the first MPC was constituted on 29 September 2016. The "
              "present external members were notified on 1 October 2024.",
  steps=["First MPC: 29 September 2016"],
  why="5 August 2016 is the inflation-target notification; 1 October 2024 the notification of the present "
      "members; 1 April 2016 is not an MPC date.",
  facts=[fact("The first such MPC was constituted on September 29, 2016; present members notified in the Gazette of "
              "October 1, 2024; target notified August 5, 2016", MP_OVERVIEW)])
Q(T, "MPC structure", "Basic",
  "One of the three RBI members of the Monetary Policy Committee is an officer of RBI nominated by:",
  ["RBI's Central Board", "The Central Government", "The Governor alone", "The Finance Commission"],
  concept="Composition of the MPC",
  explanation="The MPC has the Governor (chairperson, ex officio), the Deputy Governor in charge of monetary policy "
              "(ex officio), and one officer of RBI nominated by the Central Board (ex officio), plus three "
              "external members appointed by the Central Government.",
  steps=["RBI members: Governor, DG (monetary policy), officer nominated by the Central Board"],
  why="The Central Government appoints the three external members, not the RBI officer; the Governor and Finance "
      "Commission do not nominate members.",
  facts=[fact("MPC: Governor; Deputy Governor in charge of Monetary Policy; one officer of the RBI to be nominated "
              "by the Central Board", MP_OVERVIEW)])
Q(T, "Transmission", "Basic",
  "Which committee of RBI meets daily to review liquidity conditions so that the operating target of monetary policy "
  "stays close to the policy repo rate?",
  ["Financial Markets Committee (FMC)", "Monetary Policy Committee (MPC)", "Board for Financial Supervision (BFS)",
   "Financial Stability and Development Council (FSDC)"],
  concept="Liquidity management",
  explanation="RBI's Financial Markets Committee meets daily to review liquidity so that the operating target "
              "(the weighted average call rate) stays close to the repo rate. The MPC meets at least four times a "
              "year to set the repo rate.",
  steps=["Daily liquidity review → Financial Markets Committee"],
  why="The MPC sets the policy rate at scheduled meetings; BFS supervises; FSDC is a government-chaired council.",
  facts=[fact("The Financial Market Committee (FMC) meets daily to review the liquidity conditions so as to ensure "
              "that the operating target of monetary policy is kept close to the policy repo rate", MP_OVERVIEW)])
Q(T, "MPC structure", "Intermediate",
  "Under the RBI MPC and Monetary Policy Process Regulations, 2016, how much notice is ordinarily given to members for "
  "an MPC meeting, and how much for an emergency meeting?",
  ["Not less than 15 days; 24 hours", "Not less than 7 days; 48 hours", "Not less than 30 days; 7 days",
   "Not less than 14 days; 12 hours"],
  concept="MPC meeting process",
  explanation="Ordinarily not less than fifteen days' notice is given to members for an MPC meeting. For an "
              "emergency meeting, 24 hours' notice is given, with technology-enabled arrangements for even shorter "
              "notice.",
  steps=["Ordinary meeting: ≥ 15 days' notice", "Emergency meeting: 24 hours' notice"],
  why="The other pairs do not match the Regulations; 14 days is the day minutes are published, not a notice period.",
  facts=[fact("Ordinarily, not less than fifteen days' notice is given to members; for an emergency meeting, 24 "
              "hours' notice is given", MP_OVERVIEW)])
Q(T, "Transmission", "Intermediate",
  "What is RBI's main tool for managing short-term (transient) liquidity under its operating framework?",
  ["7-day variable rate repo/reverse repo auctions, with other variable rate operations from overnight up to 14 days",
   "Daily fixed rate reverse repo at the repo rate", "Monthly changes in the Cash Reserve Ratio",
   "Weekly open market purchases of dated government securities"],
  concept="Liquidity management tools",
  explanation="RBI manages transient liquidity primarily through 7-day variable rate repo/reverse repo auctions and "
              "other variable rate operations of tenors from overnight up to 14 days, at its discretion. Durable "
              "liquidity is managed through OMOs, forex swaps and the MSS.",
  steps=["Transient liquidity → 7-day VRR/VRRR + overnight to 14-day variable rate operations"],
  why="Fixed rate reverse repo is now used at RBI's discretion; CRR changes and OMOs address durable liquidity, "
      "not day-to-day liquidity.",
  facts=[fact("Short term/transient liquidity managed primarily through 7-day variable rate repo/reverse repo "
              "auction and other variable rate operations of tenors from overnight up to 14 days", MP_OVERVIEW)])
Q(T, "Policy stance", "Intermediate",
  "At its meeting of 3–5 December 2025, when the MPC cut the repo rate to 5.25%, what did it decide about the policy "
  "stance?",
  ["It continued with the neutral stance; one member wanted it changed to accommodative",
   "It changed the stance from neutral to accommodative unanimously",
   "It changed the stance to calibrated tightening", "It withdrew the stance from its statements"],
  concept="Policy stance, December 2025",
  explanation="At its 58th meeting (3–5 December 2025), the MPC unanimously cut the repo rate by 25 bps to 5.25% "
              "and continued with the neutral stance. Prof. Ram Singh was of the view that the stance be changed "
              "from neutral to accommodative.",
  steps=["Repo cut to 5.25% (unanimous)", "Stance: neutral continued; Prof. Ram Singh preferred accommodative"],
  why="The stance was not changed in December 2025; calibrated tightening was adopted only in October 2026.",
  current=ca("2025-12-05"),
  facts=[fact("MPC unanimously voted to reduce the policy repo rate by 25 bps to 5.25 per cent and to continue with "
              "the neutral stance; Prof. Ram Singh was of the view that the stance be changed to accommodative",
              MPC_DEC25)])
Q(T, "Transmission", "Advanced",
  "Consider the following statements about RBI's liquidity adjustment framework:\nI. Under the MSF, banks can borrow "
  "overnight by dipping into their SLR portfolio up to a predefined limit of 2 per cent.\nII. Since April 2022, the "
  "fixed rate reverse repo rate has been the floor of the LAF corridor.\nIII. Apart from the LAF, instruments of "
  "liquidity management include outright OMOs, forex swaps and the Market Stabilisation Scheme.\nWhich of the above "
  "is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="LAF corridor and liquidity instruments",
  explanation="The MSF lets banks borrow overnight by dipping into SLR up to 2 per cent (I right). With the SDF "
              "introduced in April 2022, the SDF rate replaced the fixed reverse repo rate as the floor of the "
              "corridor (II wrong). OMOs, forex swaps and the MSS are liquidity tools besides the LAF (III right).",
  steps=["I: correct", "II: wrong (SDF is the floor)", "III: correct"],
  why="Any option containing II is wrong because the SDF, not the fixed reverse repo, is the floor.",
  facts=[fact("MSF: borrow overnight by dipping into SLR portfolio up to a predefined limit (2 per cent); with "
              "introduction of SDF in April 2022, the SDF rate replaced the fixed reverse repo rate as the floor; "
              "instruments include OMOs, forex swaps and MSS", MP_OVERVIEW)])

mpc_2026_27 = ["April 6-8, 2026", "June 3-5, 2026", "August 3-5, 2026", "October 5-7, 2026", "December 2-4, 2026",
               "February 3-5, 2027"]
remaining_after_oct = [m for m in mpc_2026_27 if m.startswith(("December", "February"))]
assert len(mpc_2026_27) == 6 and len(remaining_after_oct) == 2
Q(T, "MPC structure", "Advanced",
  "RBI's published schedule for 2026-27 has MPC meetings in April, June, August, October and December 2026 and "
  "February 2027. After the 63rd meeting of 5–7 October 2026, which statement is correct?",
  ["The schedule has six meetings in 2026-27, two more than the statutory minimum of four, with two still to come",
   "The schedule has six meetings, which is the maximum the RBI Act allows in a year",
   "The schedule has five meetings in 2026-27, and only the December meeting remains",
   "The MPC must also hold an extra meeting if the minimum of eight meetings a year is not reached"],
  concept="MPC meeting requirements",
  explanation="The RBI Act requires the MPC to meet at least four times a year; there is no maximum. RBI's schedule "
              "for 2026-27 lists six meetings (April, June, August, October, December 2026 and February 2027). "
              "After the October meeting, the December 2026 and February 2027 meetings remain.",
  steps=["Count: 6 meetings in FY 2026-27", "Statutory minimum: 4 → 2 more than required",
         "After October: December and February remain"],
  why="Six is not a legal maximum; there are six, not five, meetings; the minimum is four, not eight.",
  computed=True, current=ca("2026-10-07"),
  facts=[fact("MPC is required to meet at least four times in a year; meeting schedule April, June, August, October, "
              "December 2026 and February 2027", MP_OVERVIEW),
         fact("The MPC held its 63rd meeting from October 5 to 7, 2026; next meeting December 2 to 4, 2026",
              MPC_OCT26)])

# ================================================================= 6. Repo Rate (1 / 3 / 4)
T = "Repo Rate"
Q(T, "Repo and policy corridor", "Basic",
  "What is the policy repo rate after the Monetary Policy Committee's decision of 7 October 2026?",
  ["5.50%", "5.25%", "5.75%", "6.00%"],
  concept="Current repo rate",
  explanation="At its meeting of 5–7 October 2026, the MPC raised the policy repo rate under the LAF by 25 basis "
              "points to 5.50%. The SDF rate became 5.25% and the MSF rate and Bank Rate 5.75%.",
  steps=["Earlier repo: 5.25%", "Raised by 25 bps → 5.50%"],
  why="5.25% was the repo before the hike (now the SDF rate); 5.75% is the MSF rate and Bank Rate; 6.00% is not a "
      "current rate.",
  current=CORRIDOR,
  facts=[fact("The MPC voted unanimously to increase the policy repo rate under the LAF by 25 bps to 5.50 per cent; "
              "SDF 5.25 per cent; MSF and Bank Rate 5.75 per cent", MPC_OCT26)])
Q(T, "Repo and policy corridor", "Intermediate",
  "How did the members of the Monetary Policy Committee vote on the repo rate increase at the October 2026 meeting?",
  ["All six voted for the 25 bps increase", "Four voted for the increase and two for a pause",
   "Three voted for the increase and the Governor used a casting vote", "Five voted for a 50 bps increase"],
  concept="MPC voting, October 2026",
  explanation="The MPC voted unanimously to raise the repo rate by 25 bps to 5.50%. The division in that meeting "
              "was only on the stance: two members wanted the neutral stance retained.",
  steps=["Rate decision: unanimous 25 bps hike", "Disagreement was on the stance, not the rate"],
  why="No member voted against the rate increase, so there was no tie; the increase was 25 bps, not 50 bps.",
  current=CORRIDOR,
  facts=[fact("The MPC unanimously voted to increase the policy repo rate by 25 basis points to 5.50 per cent",
              MPC_OCT26)])
Q(T, "Repo and policy corridor", "Intermediate",
  "In its resolution of 7 October 2026, what real GDP growth did the MPC project for 2026-27?",
  ["7.1 per cent", "6.8 per cent", "7.8 per cent", "7.3 per cent"],
  concept="RBI growth projection",
  explanation="The MPC projected real GDP growth for 2026-27 at 7.1%, with Q2 at 7.2%, Q3 at 6.9% and Q4 at 6.8%, "
              "after Q1 growth of 7.8% (NSO). Risks were evenly balanced.",
  steps=["2026-27 projection: 7.1%"],
  why="7.8% is Q1:2026-27 actual growth; 6.8% is the Q4 projection; 7.3% was the December 2025 projection for "
      "2025-26.",
  current=CORRIDOR,
  facts=[fact("Real GDP growth for 2026-27 is projected at 7.1 per cent, with Q2 at 7.2, Q3 at 6.9 and Q4 at 6.8 per "
              "cent; Q1:2026-27 growth 7.8 per cent", MPC_OCT26)])
Q(T, "Repo and policy corridor", "Intermediate",
  "The repo rate was 5.25% from the MPC meeting of December 2025 until the October 2026 increase. What did the MPC "
  "decide on the repo rate at its meeting of 3–5 August 2026?",
  ["Kept it unchanged at 5.25% with a unanimous vote", "Raised it to 5.50%", "Cut it to 5.00%",
   "Kept it unchanged at 5.50%"],
  concept="Policy rate path 2025-26",
  explanation="The MPC cut the repo rate to 5.25% in December 2025 and kept it unchanged at 5.25% at its August "
              "2026 meeting, retaining the neutral stance. The 25 bps hike to 5.50% came in October 2026.",
  steps=["Dec 2025: 5.25%", "Aug 2026: unchanged at 5.25%", "Oct 2026: 5.50%"],
  why="The hike to 5.50% came in October, not August; there was no cut to 5.00% (5.00% was the SDF rate).",
  current=ca("2026-08-05"),
  facts=[fact("August 2026: the MPC voted unanimously to keep the policy repo rate under the LAF unchanged at 5.25 "
              "per cent", MPC_AUG26),
         fact("December 2025: repo reduced to 5.25 per cent", MPC_DEC25)])

dec_sdf, dec_msf = 5.25 - 0.25, 5.25 + 0.25
assert (dec_sdf, dec_msf) == (5.00, 5.50)
Q(T, "Repo and policy corridor", "Advanced",
  "After the MPC cut the repo rate to 5.25% in December 2025, keeping the usual corridor, what were the SDF rate and "
  "the MSF rate/Bank Rate?",
  ["SDF 5.00%; MSF and Bank Rate 5.50%", "SDF 5.25%; MSF and Bank Rate 5.75%", "SDF 4.75%; MSF and Bank Rate 5.75%",
   "SDF 5.00%; MSF 5.50% and Bank Rate 5.25%"],
  concept="LAF corridor",
  explanation="The SDF rate is 25 bps below the repo and the MSF rate 25 bps above it; the Bank Rate is aligned with "
              "the MSF rate. With repo at 5.25%: SDF = 5.00%, MSF = Bank Rate = 5.50%.",
  steps=["SDF = 5.25 − 0.25 = 5.00%", "MSF = 5.25 + 0.25 = 5.50%", "Bank Rate = MSF = 5.50%"],
  shortcut="Corridor = repo ± 25 bps; Bank Rate = MSF.",
  why="5.25%/5.75% are the rates after the October 2026 hike; the corridor is ±25 bps, not ±50 bps; the Bank Rate "
      "equals the MSF rate, not the repo.",
  computed=True, current=ca("2025-12-05"),
  facts=[fact("SDF rate stands adjusted to 5.00 per cent and the MSF rate and the Bank Rate to 5.50 per cent",
              MPC_DEC25),
         fact("SDF 25 bps below and MSF 25 bps above the repo rate; Bank Rate aligned with MSF", MP_OVERVIEW)])

loan, spread = 4000000, 2.85
old_rate, new_rate = round(5.25 + spread, 2), round(REPO + spread, 2)
extra = loan * (new_rate - old_rate) / 100
assert (old_rate, new_rate) == (8.10, 8.35) and round(extra) == 10000
Q(T, "Repo and policy corridor", "Advanced",
  "Rakesh has a floating-rate home loan of ₹40 lakh priced at 'repo rate + 2.85%' under the external benchmark "
  "system. After the repo rate change of October 2026 is passed on, what is his new interest rate and the approximate "
  "increase in annual interest on the outstanding amount (ignoring amortisation)?",
  ["8.35%; about ₹10,000 a year", "8.10%; about ₹10,000 a year", "8.35%; about ₹1,00,000 a year",
   "8.60%; about ₹20,000 a year"],
  concept="Repo-linked loan pricing",
  explanation="The repo rate rose by 25 bps from 5.25% to 5.50%. The loan rate moves from 5.25 + 2.85 = 8.10% to "
              "5.50 + 2.85 = 8.35%. Extra interest = 0.25% × ₹40,00,000 = ₹10,000 a year.",
  steps=["Old rate = 5.25 + 2.85 = 8.10%", "New rate = 5.50 + 2.85 = 8.35%", "Increase = 0.25% × ₹40 lakh = ₹10,000"],
  shortcut="25 bps on ₹40 lakh = ₹10,000.",
  why="8.10% is the old rate; ₹1,00,000 confuses 0.25% with 2.5%; 8.60% assumes a 50 bps hike.",
  computed=True, current=CORRIDOR,
  facts=[fact("Policy repo rate increased by 25 bps to 5.50 per cent (from 5.25 per cent)", MPC_OCT26)])

real_rate = round(REPO - 5.2, 2)
assert real_rate == 0.30
Q(T, "Repo and policy corridor", "Advanced",
  "Using the October 2026 MPC resolution, what is the approximate 'real' policy rate, defined as the repo rate minus "
  "the projected CPI inflation for 2026-27?",
  ["About 0.30 percentage points", "About 0.70 percentage points", "About −0.50 percentage points",
   "About 1.10 percentage points"],
  concept="Real policy rate",
  explanation="Repo rate = 5.50%; projected CPI inflation for 2026-27 = 5.2%. Real policy rate ≈ 5.50 − 5.2 = 0.30 "
              "percentage points.",
  steps=["Repo = 5.50%", "Projected CPI 2026-27 = 5.2%", "5.50 − 5.2 = 0.30"],
  why="0.70 uses August CPI (4.8%); −0.50 uses the Q3 projection (6.0%); 1.10 uses core inflation (4.4%).",
  computed=True, current=CORRIDOR,
  facts=[fact("Repo 5.50 per cent; CPI inflation projected at 5.2 per cent for 2026-27; core 4.4 per cent; CPI "
              "August 2026 4.8 per cent; Q3 projection 6.0 per cent", MPC_OCT26)])
Q(T, "Repo and policy corridor", "Advanced",
  "Consider the following statements about the policy repo rate between December 2025 and October 2026:\nI. The "
  "October 2026 increase exactly reversed the December 2025 cut.\nII. Both the December 2025 cut and the October "
  "2026 increase were decided unanimously.\nIII. The December 2025 cut was accompanied by a change of stance to "
  "accommodative.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Policy rate path",
  explanation="December 2025: repo cut by 25 bps (5.50% → 5.25%), unanimous, neutral stance continued. October "
              "2026: repo raised by 25 bps to 5.50%, unanimous, stance changed to calibrated tightening. So I and "
              "II are right; III is wrong.",
  steps=["I: −25 bps then +25 bps → correct", "II: both unanimous → correct", "III: stance stayed neutral → wrong"],
  why="III is false, so options including it are wrong; 'I only' omits the true statement II.",
  current=CORRIDOR,
  facts=[fact("December 2025: MPC unanimously reduced repo by 25 bps to 5.25 per cent and continued with the neutral "
              "stance", MPC_DEC25),
         fact("October 2026: MPC unanimously increased repo by 25 bps to 5.50 per cent; stance changed to calibrated "
              "tightening", MPC_OCT26)])

# ================================================================= 7. Reverse Repo Rate (1 / 1 / 1)
T = "Reverse Repo Rate"
Q(T, "Reverse repo and SDF", "Basic",
  "In which year did RBI introduce the Standing Deposit Facility (SDF), which replaced the fixed rate reverse repo as "
  "the floor of the LAF corridor?",
  ["2022", "2011", "2016", "2020"],
  concept="Standing Deposit Facility",
  explanation="RBI introduced the SDF in April 2022. Since then the SDF rate, placed 25 bps below the repo rate, has "
              "been the floor of the LAF corridor in place of the fixed rate reverse repo.",
  steps=["SDF introduced April 2022"],
  why="2011 is associated with the MSF; 2016 with the MPC; 2020 with pandemic-era measures.",
  facts=[fact("With introduction of SDF in April 2022, the SDF rate replaced the fixed reverse repo rate as the floor "
              "of the LAF corridor", MP_OVERVIEW)])
Q(T, "Reverse repo and SDF", "Intermediate",
  "Following the MPC decision of 5 December 2025, the SDF rate was:",
  ["5.00%", "5.25%", "4.75%", "5.50%"],
  concept="SDF rate, December 2025",
  explanation="When the repo rate was cut to 5.25% on 5 December 2025, the SDF rate was adjusted to 5.00% (25 bps "
              "below the repo). It moved to 5.25% only after the October 2026 hike.",
  steps=["Repo 5.25% − 25 bps = SDF 5.00%"],
  why="5.25% was the repo then (and is the SDF now); 4.75% is too low; 5.50% was the MSF rate then.",
  current=ca("2025-12-05"),
  facts=[fact("The standing deposit facility (SDF) rate shall stand adjusted to 5.00 per cent", MPC_DEC25)])
Q(T, "Reverse repo and SDF", "Advanced",
  "Consider the following statements:\nI. The SDF rate is placed 25 basis points below the policy repo rate.\nII. "
  "Under the reverse repo, RBI absorbs liquidity against the collateral of eligible government securities.\nIII. "
  "Only scheduled commercial banks, and no other LAF participants, can place funds under the SDF.\nWhich of the "
  "above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="SDF versus reverse repo",
  explanation="The SDF rate is 25 bps below the repo (I right). Under the reverse repo, RBI absorbs liquidity "
              "against eligible government securities as collateral (II right). The SDF accepts uncollateralised "
              "overnight deposits from all LAF participants, not only scheduled commercial banks (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (all LAF participants)"],
  why="Any option containing III is wrong; 'I only' omits the true statement II.",
  facts=[fact("SDF: rate at which RBI accepts uncollateralised deposits, on an overnight basis, from all LAF "
              "participants; placed 25 bps below the repo. Reverse repo: RBI absorbs liquidity against the collateral "
              "of eligible government securities", MP_OVERVIEW)])

# ================================================================= 8. CRR (1 / 1 / 0)
T = "CRR"
Q(T, "CRR concept", "Basic",
  "Does RBI pay interest to scheduled commercial banks on the balances they maintain as CRR?",
  ["No; RBI has not paid interest on CRR balances since 2007",
   "Yes, at the repo rate", "Yes, at the SDF rate", "Yes, but only on balances above the required CRR"],
  concept="Remuneration of CRR",
  explanation="After the amendment omitting sub-section (1B) of Section 42 of the RBI Act, RBI stopped paying any "
              "interest on CRR balances maintained by scheduled commercial banks from the fortnight beginning 31 "
              "March 2007.",
  steps=["CRR balances are unremunerated since March 2007"],
  why="No interest is paid at any rate on CRR balances.",
  facts=[fact("The Reserve Bank does not pay any interest on the CRR balances maintained by SCBs with effect from "
              "the fortnight beginning March 31, 2007", CRR_SLR_MC)])
Q(T, "CRR value", "Intermediate",
  "From the fortnight beginning 16 October 2026, what minimum share of the required CRR must a bank maintain on every "
  "day of the reporting fortnight?",
  ["99 per cent", "90 per cent", "95 per cent", "100 per cent"],
  concept="Daily CRR maintenance",
  explanation="CRR is maintained on a fortnightly average basis, subject to a daily minimum. By a circular of 9 "
              "October 2026, RBI raised the minimum daily maintenance from 90% to 99% of the requirement, effective "
              "from the fortnight beginning 16 October 2026, after reviewing liquidity conditions.",
  steps=["Earlier daily minimum: 90%", "From 16 Oct 2026: 99%"],
  why="90% was the earlier floor; 95% and 100% are not the prescribed level.",
  current=ca("2026-10-09"),
  facts=[fact("Decided to increase the minimum daily maintenance of the CRR from 90 per cent of the requirement to 99 "
              "per cent effective from the fortnight beginning October 16, 2026 (circular dated October 09, 2026)",
              CRR99)])

# ================================================================= 9. SLR (1 / 2 / 2)
T = "SLR"
Q(T, "SLR value", "Basic",
  "After the Banking Regulation (Amendment) Act, 2007, up to what maximum percentage of a bank's demand and time "
  "liabilities can RBI prescribe as the Statutory Liquidity Ratio?",
  ["40 per cent", "25 per cent", "18 per cent", "50 per cent"],
  concept="SLR ceiling",
  explanation="Following the amendment of Section 24 of the BR Act effective 23 January 2007, RBI can prescribe SLR "
              "in specified assets at a percentage not exceeding 40% of total demand and time liabilities. The "
              "earlier 25% floor no longer applies.",
  steps=["Section 24 as amended in 2007: SLR ceiling 40%"],
  why="25% was the old statutory floor; 18% is the current SLR, not the ceiling; 50% is not in the law.",
  facts=[fact("Consequent upon amendment to Section 24 of the BR Act through the BR (Amendment) Act, 2007, effective "
              "January 23, 2007, RBI can prescribe SLR ... not exceeding 40 per cent of its total DTL", CRR_SLR_MC)])
Q(T, "SLR concept", "Intermediate",
  "If a bank fails to maintain the required SLR on a day, what penal interest does it pay to RBI on the shortfall "
  "for that day?",
  ["3 per cent per annum above the Bank Rate", "The repo rate", "2 per cent per annum above the repo rate",
   "5 per cent per annum above the MSF rate"],
  concept="Penalty for SLR default",
  explanation="A bank that fails to maintain SLR pays penal interest for that day at 3% per annum above the Bank "
              "Rate on the shortfall. If the default continues on the next working day, the rate may be raised to "
              "5% above the Bank Rate for the days of default.",
  steps=["First day: Bank Rate + 3%", "Continuing default: up to Bank Rate + 5%"],
  why="The penalty is linked to the Bank Rate, not the repo or MSF; repo + 2% is the compensation rate for delayed "
      "NEFT/RTGS credit.",
  facts=[fact("Penal interest for that day at three per cent per annum above the Bank Rate on the shortfall; if the "
              "default continues on the next succeeding working day, may be increased to five per cent above the "
              "Bank Rate", CRR_SLR_MC),
         fact("Penal interest rates on shortfalls in reserve requirements: Bank Rate plus 3.0 or plus 5.0 percentage "
              "points depending on duration", CRR_PENAL)])
Q(T, "SLR concept", "Intermediate",
  "The SLR requirement of a bank is computed as a percentage of its demand and time liabilities as on which date?",
  ["The last Friday of the second preceding fortnight", "The last working day of the previous quarter",
   "31 March of the previous financial year", "The day on which the SLR is maintained"],
  concept="Reference date for reserve requirements",
  explanation="RBI describes SLR as assets of not less than a specified percentage of a bank's total demand and "
              "time liabilities in India 'as on the last Friday of the second preceding fortnight'. CRR uses the "
              "same reference date.",
  steps=["Reference: last Friday of the second preceding fortnight"],
  why="Quarter-end and financial-year-end dates are used for PSL and other norms, not for SLR; the requirement is "
      "not based on the same day's liabilities.",
  facts=[fact("SLR: assets not less than such percentage of total demand and time liabilities in India as on the "
              "last Friday of the second preceding fortnight", MP_OVERVIEW)])

short = 150 * 10**7
day1 = short * (BANK_RATE + 3) / 100 / 365
day2 = short * (BANK_RATE + 5) / 100 / 365
assert round(day1) == 359589 and round(day2) == 441781 and round((day1 + day2) / 1e5, 2) == 8.01
Q(T, "SLR value", "Advanced",
  "With the Bank Rate at 5.75%, a bank's SLR holding falls short by ₹150 crore on two consecutive working days. If "
  "RBI charges the base penal rate on the first day and the higher rate on the second day, what is the total penal "
  "interest (approx.)?",
  ["₹8.01 lakh", "₹7.19 lakh", "₹8.84 lakh", "₹3.60 lakh"],
  concept="Computing SLR penal interest",
  explanation="Day 1: 5.75 + 3 = 8.75% p.a. → ₹150 crore × 8.75% ÷ 365 = ₹3,59,589. Day 2: 5.75 + 5 = 10.75% p.a. "
              "→ ₹150 crore × 10.75% ÷ 365 = ₹4,41,781. Total ≈ ₹8.01 lakh.",
  steps=["Day 1 rate 8.75% → ₹3.60 lakh", "Day 2 rate 10.75% → ₹4.42 lakh", "Total ≈ ₹8.01 lakh"],
  why="₹7.19 lakh applies 8.75% to both days; ₹8.84 lakh applies 10.75% to both days; ₹3.60 lakh is only day 1.",
  computed=True, current=CORRIDOR,
  facts=[fact("SLR penal interest: 3% above Bank Rate for the day; if the default continues on the next succeeding "
              "working day, may be increased to 5% above Bank Rate", CRR_SLR_MC),
         fact("Bank Rate 5.75 per cent after 7 October 2026", MPC_OCT26)])
Q(T, "SLR concept", "Advanced",
  "Consider the following statements:\nI. RBI can prescribe the SLR up to 40 per cent of a bank's demand and time "
  "liabilities.\nII. SLR assets are typically unencumbered government securities, cash and gold.\nIII. SLR, like "
  "CRR, must be maintained wholly as a cash balance with RBI.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="SLR versus CRR",
  explanation="The 2007 amendment allows an SLR of up to 40% (I right). SLR is maintained in assets such as "
              "unencumbered government securities, cash and gold (II right). Only CRR is a cash balance with RBI; "
              "SLR assets are held by the bank itself (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong"],
  why="III confuses SLR with CRR, so any option including III is wrong; 'I only' omits the true statement II.",
  facts=[fact("RBI can prescribe SLR not exceeding 40 per cent of total DTL", CRR_SLR_MC),
         fact("SLR assets typically in unencumbered government securities, cash and gold; CRR is a balance "
              "maintained with the Reserve Bank", MP_OVERVIEW)])

# ================================================================= 10. Bank Rate (1 / 1 / 1)
T = "Bank Rate"
Q(T, "Bank rate and MSF", "Basic",
  "Under which section of the RBI Act, 1934 is the Bank Rate published?",
  ["Section 49", "Section 42", "Section 24", "Section 45ZB"],
  concept="Bank Rate",
  explanation="The Bank Rate is the rate at which RBI is ready to buy or rediscount bills of exchange or other "
              "commercial papers. It is published under Section 49 of the RBI Act and is aligned with the MSF rate.",
  steps=["Bank Rate → Section 49, RBI Act"],
  why="Section 42 deals with CRR; Section 24 of the RBI Act with denominations of notes; Section 45ZB with the MPC.",
  facts=[fact("The Bank Rate is published under Section 49 of the RBI Act, 1934; it is the rate at which RBI is "
              "ready to buy or rediscount bills of exchange", MP_OVERVIEW)])
Q(T, "Bank rate and MSF", "Intermediate",
  "Under the Marginal Standing Facility, banks can borrow overnight from RBI by dipping into their SLR portfolio up "
  "to a predefined limit of:",
  ["2 per cent of NDTL", "1 per cent of NDTL", "5 per cent of NDTL", "No limit"],
  concept="MSF borrowing",
  explanation="MSF is the penal-rate window through which banks borrow overnight by dipping into their SLR "
              "securities up to a predefined limit of 2 per cent. It acts as a safety valve against unexpected "
              "liquidity shocks. Its rate is 25 bps above the repo and the Bank Rate is aligned with it.",
  steps=["MSF: overnight, against SLR securities, up to 2%"],
  why="The predefined limit is 2 per cent, not 1 or 5 per cent, and the facility is not unlimited.",
  facts=[fact("MSF: penal rate at which banks can borrow overnight by dipping into their SLR portfolio up to a "
              "predefined limit (2 per cent)", MP_OVERVIEW)])

ndtl = 30000 * 10**7
msf_amt = ndtl * 0.02
msf_int = msf_amt * MSF / 100 / 365
assert msf_amt == 600 * 10**7 and inr(round(msf_int)) == "9,45,205"
Q(T, "Bank rate and MSF", "Advanced",
  "A bank with NDTL of ₹30,000 crore faces a sudden liquidity shortage after the October 2026 policy. If it borrows "
  "the maximum it can under the MSF by dipping into its SLR, how much can it borrow and what is the interest for one "
  "night (approx.)?",
  ["₹600 crore; about ₹9.45 lakh", "₹600 crore; about ₹9.04 lakh", "₹300 crore; about ₹4.73 lakh",
   "₹900 crore; about ₹14.18 lakh"],
  concept="MSF arithmetic",
  explanation="Maximum MSF = 2% of ₹30,000 crore = ₹600 crore. The MSF rate is 5.75% (repo 5.50% + 25 bps). One "
              "night's interest = ₹600 crore × 5.75% ÷ 365 ≈ ₹9,45,205.",
  steps=["2% × ₹30,000 crore = ₹600 crore", "MSF rate = 5.75%", "₹600 crore × 0.0575 ÷ 365 ≈ ₹9.45 lakh"],
  why="₹9.04 lakh uses the repo rate (5.50%); ₹300 crore uses a 1% limit; ₹900 crore uses 3%.",
  computed=True, current=CORRIDOR,
  facts=[fact("MSF: dip into SLR up to a predefined limit (2 per cent); MSF rate 25 bps above repo", MP_OVERVIEW),
         fact("MSF rate and Bank Rate 5.75 per cent", MPC_OCT26)])

# ================================================================= 11. Inflation (1 / 4 / 1)
T = "Inflation"
Q(T, "CPI and WPI", "Basic",
  "Which ministry compiles the Consumer Price Index (CPI), whose base year was revised to 2024=100 in 2026?",
  ["Ministry of Statistics and Programme Implementation", "Ministry of Commerce and Industry",
   "Ministry of Finance", "Reserve Bank of India"],
  concept="Compiler of CPI",
  explanation="MoSPI compiles the CPI and revised its base from 2012=100 to 2024=100; the revised series was "
              "released on 12 February 2026. The WPI is compiled by the Office of the Economic Adviser in the "
              "Ministry of Commerce and Industry.",
  steps=["CPI → MoSPI"],
  why="Commerce and Industry compiles the WPI; the Finance Ministry and RBI use CPI but do not compile it.",
  current=ca("2026-02-12"),
  facts=[fact("The Ministry of Statistics & Programme Implementation (MoSPI) revised the base year of the CPI from "
              "2012=100 to 2024=100; the revised series was released on 12th February, 2026", CPI_PIB)])
Q(T, "Inflation targeting", "Intermediate",
  "Under Section 45ZA of the RBI Act, who determines India's inflation target, and how often?",
  ["The Central Government, in consultation with RBI, once in five years",
   "The Monetary Policy Committee, every year", "RBI's Central Board, once in three years",
   "Parliament, at every Union Budget"],
  concept="Setting the inflation target",
  explanation="Section 45ZA empowers the Central Government, in consultation with RBI, to determine the inflation "
              "target in terms of CPI once in five years and notify it in the Official Gazette. The MPC sets the "
              "repo rate to achieve the target.",
  steps=["Who: Central Government (with RBI)", "How often: once in five years"],
  why="The MPC sets the policy rate, not the target; neither the Central Board nor Parliament sets the target.",
  facts=[fact("Under Section 45ZA, the Central Government, in consultation with the RBI, determines the inflation "
              "target in terms of CPI, once in five years", MP_OVERVIEW)])
Q(T, "CPI and WPI", "Intermediate",
  "According to the MPC resolution of October 2026, what was CPI inflation in August 2026?",
  ["4.8 per cent", "4.5 per cent", "5.2 per cent", "6.0 per cent"],
  concept="Recent CPI inflation",
  explanation="CPI inflation rose to 4.8% in August 2026 from 4.5% in July, mainly due to food and fuel. Core "
              "inflation rose to 4.2%. The MPC projected CPI inflation at 5.2% for 2026-27, with Q3 at 6.0%.",
  steps=["July 2026: 4.5%", "August 2026: 4.8%"],
  why="4.5% is July's figure; 5.2% is the 2026-27 projection; 6.0% is the Q3 projection.",
  current=ca("2026-10-07"),
  facts=[fact("CPI inflation increased to 4.8 per cent in August 2026 from 4.5 per cent in July; core inflation 4.2 "
              "per cent", MPC_OCT26)])
Q(T, "Inflation targeting", "Intermediate",
  "In December 2025, when the repo rate was cut to 5.25%, what CPI inflation did the MPC project for 2025-26?",
  ["2.0 per cent", "4.0 per cent", "5.2 per cent", "3.9 per cent"],
  concept="Benign inflation outlook, 2025-26",
  explanation="In December 2025 the MPC projected CPI inflation for 2025-26 at 2.0% (Q3 0.6%, Q4 2.9%), well below "
              "the 4% target, which gave room for the rate cut. It projected 3.9% for Q1 and 4.0% for Q2 of "
              "2026-27.",
  steps=["2025-26 CPI projection (Dec 2025): 2.0%"],
  why="3.9% and 4.0% were projections for Q1 and Q2 of 2026-27; 5.2% is the October 2026 projection for 2026-27.",
  current=ca("2025-12-05"),
  facts=[fact("CPI inflation for 2025-26 is now projected at 2.0 per cent with Q3 at 0.6 per cent and Q4 at 2.9 per "
              "cent; Q1:2026-27 3.9 per cent and Q2 4.0 per cent", MPC_DEC25)])
Q(T, "Inflation targeting", "Intermediate",
  "If RBI fails to meet the inflation target, the report it must send to the Central Government must set out which "
  "of the following?",
  ["The reasons for failure, the remedial actions proposed, and an estimate of the time to achieve the target",
   "Only the reasons for failure", "The resignation of the external MPC members",
   "A revised inflation target for the next five years"],
  concept="Accountability under inflation targeting",
  explanation="Where RBI fails to meet the target, it reports to the Central Government (a) the reasons for "
              "failure, (b) the remedial actions proposed, and (c) an estimate of the time within which the target "
              "will be achieved after those actions.",
  steps=["Report contents: reasons + remedial actions + time estimate"],
  why="The report has three elements, not one; it does not require resignations or a new target.",
  facts=[fact("Where the Bank fails to meet the inflation target, it shall set out in a report the reasons, "
              "remedial actions proposed and an estimate of the time-period within which the target shall be "
              "achieved", MP_OVERVIEW)])

nxt3 = [6.0, 5.7, 5.6]
avg3 = sum(nxt3) / 3
assert round(avg3, 2) == 5.77
Q(T, "Inflation targeting", "Advanced",
  "The October 2026 MPC resolution projected CPI inflation at 4.9% (Q2), 6.0% (Q3) and 5.7% (Q4) of 2026-27, and "
  "5.6% for Q1:2027-28. What is the average projected inflation for the three quarters after Q2, and how does it "
  "compare with the inflation target?",
  ["About 5.8%, about 1.8 percentage points above the 4% target but within the 6% upper tolerance",
   "About 5.6%, above the upper tolerance limit of 6%", "About 5.8%, above the upper tolerance limit of 6%",
   "About 5.2%, about 1.2 percentage points above the 4% target"],
  concept="Reading inflation projections",
  explanation="Next three quarters: (6.0 + 5.7 + 5.6) ÷ 3 = 17.3 ÷ 3 ≈ 5.77%, i.e. almost 5.8%, as the resolution "
              "itself notes. That is about 1.8 percentage points above the 4% target and below the 6% upper "
              "tolerance limit.",
  steps=["Sum = 6.0 + 5.7 + 5.6 = 17.3", "Average ≈ 5.77% ≈ 5.8%", "Target 4% (band 2–6%) → above target, within band"],
  why="5.6% is only Q1:2027-28; 5.8% is below, not above, 6%; 5.2% is the full-year 2026-27 projection.",
  computed=True, current=ca("2026-10-07"),
  facts=[fact("CPI inflation projected Q2 4.9, Q3 6.0, Q4 5.7 per cent; Q1:2027-28 5.6 per cent; headline expected "
              "to average almost 5.8 per cent in the next three quarters", MPC_OCT26),
         fact("Target 4 per cent CPI inflation with upper tolerance limit of 6 per cent and lower limit of 2 per "
              "cent", MP_OVERVIEW)])

# ================================================================= 12. NPA (1 / 3 / 1)
T = "NPA"
Q(T, "Classification", "Basic",
  "Under RBI's prudential norms, what general provision must a bank make on the total outstanding of a (secured) "
  "substandard asset?",
  ["15 per cent", "25 per cent", "0.40 per cent", "100 per cent"],
  concept="Provisioning for substandard assets",
  explanation="A general provision of 15% on the total outstanding is required for substandard assets, without "
              "allowing for ECGC cover or securities. Unsecured substandard exposures need an additional 10% (25% "
              "in all).",
  steps=["Substandard: 15% of outstanding"],
  why="25% is for unsecured substandard exposures; 0.40% is a standard-asset rate; 100% is for loss assets.",
  facts=[fact("A general provision of 15 per cent on total outstanding shall be made in respect of substandard "
              "assets", IRAC_MD)])
Q(T, "Classification", "Intermediate",
  "A bank may report a credit card account as 'past due' to credit information companies, or levy late payment "
  "charges, only when the account remains overdue for more than:",
  ["Three days", "Thirty days", "Ninety days", "One day"],
  concept="Credit card overdue reporting",
  explanation="RBI's directions allow banks to report a credit card account as past due to CICs, or levy penal "
              "charges such as late payment charges, only when it remains overdue for more than three days. The "
              "days overdue are still counted from the payment due date in the statement.",
  steps=["Overdue > 3 days → can report/charge"],
  why="90 days relates to NPA classification of credit cards; 30 days and one day are not the threshold.",
  facts=[fact("A bank shall report a credit card account as 'past due' to CICs or levy penal charges only when a "
              "credit card account remains overdue for more than three days", IRAC_MD)])
Q(T, "Resolution and IBC", "Intermediate",
  "Under the Insolvency and Bankruptcy Code, 2016, an operational creditor (for example, a supplier of goods) "
  "initiates a corporate insolvency resolution process under which section?",
  ["Section 9", "Section 7", "Section 10", "Section 14"],
  concept="Who initiates CIRP",
  explanation="A CIRP may be initiated by a financial creditor under Section 7, an operational creditor under "
              "Section 9, and the corporate debtor itself (corporate applicant) under Section 10.",
  steps=["Financial creditor → S.7", "Operational creditor → S.9", "Corporate applicant → S.10"],
  why="Section 7 is for financial creditors such as banks; Section 10 for the debtor itself; Section 14 is the "
      "moratorium.",
  facts=[fact("CIRP may be initiated by a financial creditor under section 7, an operational creditor under section "
              "9 and corporate applicant under section 10 of the Code", IBBI_FAQ)])
Q(T, "SARFAESI", "Intermediate",
  "In Mardia Chemicals Ltd. v. Union of India, the Supreme Court upheld the SARFAESI Act but struck down which "
  "provision?",
  ["The requirement to deposit 75% of the amount claimed before an appeal to the DRT under Section 17",
   "The 60-day notice under Section 13(2)", "The power to take possession of secured assets",
   "The registration of asset reconstruction companies"],
  concept="SARFAESI and the Supreme Court",
  explanation="The Court upheld the Act, including the 60-day notice before measures under Section 13(4) and the "
              "right to approach the DRT under Section 17. It declared sub-section (2) of Section 17, which required "
              "a deposit of 75% of the claim before an appeal, ultra vires Article 14.",
  steps=["Struck down: Section 17(2), the 75% pre-deposit"],
  why="The 60-day notice, possession powers and ARC provisions were upheld.",
  facts=[fact("Supreme Court upheld the validity of the Act except sub-section (2) of section 17; the requirement of "
              "deposit of 75% of amount claimed before an appeal is oppressive and liable to be struck down",
              SARFAESI_SC)])

prov = 40 * 0.15 + 10 * 0.25 + 20 * 0.20
assert round(prov, 2) == 12.5
Q(T, "Classification", "Advanced",
  "A bank's substandard assets consist of (i) secured loans of ₹40 crore, (ii) unsecured exposures of ₹10 crore, and "
  "(iii) an infrastructure loan of ₹20 crore with an escrow mechanism and a first claim on cash flows. What is the "
  "minimum total provision required?",
  ["₹12.5 crore", "₹10.5 crore", "₹13.5 crore", "₹17.5 crore"],
  concept="Substandard provisioning mix",
  explanation="Secured substandard: 15% of ₹40 crore = ₹6 crore. Unsecured substandard: 25% of ₹10 crore = ₹2.5 "
              "crore. Infrastructure substandard with escrow: 20% of ₹20 crore = ₹4 crore. Total = ₹12.5 crore.",
  steps=["40 × 15% = 6", "10 × 25% = 2.5", "20 × 20% = 4", "Total = 12.5"],
  why="₹10.5 crore applies 15% to everything; ₹13.5 crore applies 25% to the infrastructure loan; ₹17.5 crore "
      "applies 25% to all.",
  computed=True,
  facts=[fact("15 per cent general provision on substandard assets; unsecured substandard exposures attract a total "
              "of 25 per cent; infrastructure loans classified substandard attract 20 per cent with escrow "
              "safeguards", IRAC_MD)])

# ================================================================= 13. Basel Norms (4 / 2 / 1)
T = "Basel Norms"
Q(T, "Capital adequacy", "Basic",
  "The Basel Committee was set up at the end of 1974 by the central bank Governors of which group, after the failure "
  "of Bankhaus Herstatt?",
  ["Group of Ten (G10)", "Group of Twenty (G20)", "BRICS", "Group of Seven (G7) finance ministers"],
  concept="Origin of the Basel Committee",
  explanation="The Basel Committee, first called the Committee on Banking Regulations and Supervisory Practices, was "
              "established by the central bank Governors of the G10 countries at the end of 1974, after "
              "disturbances in currency and banking markets such as the failure of Bankhaus Herstatt.",
  steps=["1974, G10 central bank Governors"],
  why="G20 endorsed Basel III in 2010 but did not found the Committee; BRICS and G7 finance ministers did not set it "
      "up.",
  facts=[fact("Established by the central bank Governors of the Group of Ten countries at the end of 1974 in the "
              "aftermath of the failure of Bankhaus Herstatt", BCBS_HIST)])
Q(T, "Capital adequacy", "Basic",
  "The 1988 Basel Capital Accord (Basel I) called for a minimum ratio of capital to risk-weighted assets of:",
  ["8 per cent", "9 per cent", "10.5 per cent", "4 per cent"],
  concept="Basel I",
  explanation="The 1988 Accord required a minimum capital to risk-weighted assets ratio of 8%, to be implemented by "
              "the end of 1992. It focused on credit risk; market risk was added by the 1996 amendment.",
  steps=["Basel I (1988): 8% of RWA"],
  why="9% is India's minimum CRAR excluding buffers; 10.5% is the Basel III total with conservation buffer; 4% is "
      "not the Basel I ratio.",
  facts=[fact("The 1988 Accord called for a minimum ratio of capital to risk-weighted assets of 8% to be implemented "
              "by the end of 1992", BCBS_HIST)])
Q(T, "Capital adequacy", "Basic",
  "The revised capital framework known as 'Basel II', built on three pillars, was released by the Basel Committee in:",
  ["June 2004", "July 1988", "December 2010", "January 1996"],
  concept="Basel II",
  explanation="After a proposal in June 1999, the Committee released the revised capital framework in June 2004. "
              "Generally known as Basel II, it comprised three pillars.",
  steps=["Basel II: June 2004"],
  why="1988 is Basel I; December 2010 is Basel III; January 1996 is the Market Risk Amendment.",
  facts=[fact("Release of a revised capital framework in June 2004, generally known as Basel II, comprising three "
              "pillars", BCBS_HIST)])
Q(T, "Capital adequacy", "Basic",
  "What is the minimum Capital to Risk-weighted Assets Ratio (CRAR) that RBI prescribes for small finance banks and "
  "payments banks?",
  ["15 per cent", "9 per cent", "11.5 per cent", "12 per cent"],
  concept="Capital requirements for differentiated banks",
  explanation="RBI prescribes for both small finance banks and payments banks a minimum CET1 of 6%, minimum Tier 1 "
              "of 7.5% and minimum total capital (CRAR) of 15%.",
  steps=["SFB and PB: CET1 6%, Tier 1 7.5%, CRAR 15%"],
  why="9% is the minimum for RRBs and Local Area Banks; 11.5% is for scheduled commercial banks including CCB; 12% "
      "is not prescribed.",
  facts=[fact("Small Finance Banks and Payments Banks: CET1 6, minimum Tier 1 7.5, minimum total capital (CRAR) 15 "
              "per cent", CAP_TABLE)])
Q(T, "Capital adequacy", "Intermediate",
  "Which bank was added to RBI's list of Domestic Systemically Important Banks in 2017, after SBI and ICICI Bank had "
  "been named in 2015 and 2016?",
  ["HDFC Bank", "Axis Bank", "Bank of Baroda", "Punjab National Bank"],
  concept="D-SIBs in India",
  explanation="RBI named SBI and ICICI Bank as D-SIBs in 2015 and 2016, and HDFC Bank was classified as a D-SIB in "
              "2017. The 2025 list keeps all three, with HDFC Bank in bucket 2 (0.40% additional CET1) and ICICI "
              "Bank in bucket 1 (0.20%).",
  steps=["2015/16: SBI, ICICI Bank", "2017: HDFC Bank added"],
  why="Axis Bank, Bank of Baroda and PNB have not been designated D-SIBs.",
  current=ca("2025-12-02"),
  facts=[fact("SBI and ICICI Bank announced as D-SIBs in 2015 and 2016, while HDFC Bank was classified as D-SIB in "
              "2017; HDFC Bank bucket 2 at 0.40%, ICICI Bank bucket 1 at 0.20%", DSIB_2025)])
Q(T, "Capital adequacy", "Intermediate",
  "What minimum CRAR does RBI require Regional Rural Banks to maintain on an ongoing basis?",
  ["9 per cent", "15 per cent", "11.5 per cent", "8 per cent"],
  concept="Capital adequacy for RRBs",
  explanation="RRBs (and Local Area Banks) must maintain a minimum CRAR of 9% on an ongoing basis. Small finance "
              "banks and payments banks need 15%.",
  steps=["RRBs: minimum CRAR 9%"],
  why="15% is for SFBs and payments banks; 11.5% for SCBs with CCB; 8% is the Basel I global minimum.",
  facts=[fact("RRBs are required to maintain a minimum CRAR of 9 per cent on an ongoing basis", CAP_TABLE)])

rwa, cet1, at1, t2 = 2000, 130, 10, 170
r_cet1, r_t1, r_tot = cet1 / rwa * 100, (cet1 + at1) / rwa * 100, (cet1 + at1 + t2) / rwa * 100
assert (round(r_cet1, 1), round(r_t1, 1), round(r_tot, 1)) == (6.5, 7.0, 15.5)
assert r_cet1 >= 6 and r_t1 < 7.5 and r_tot >= 15
Q(T, "Capital adequacy", "Advanced",
  "A small finance bank has risk-weighted assets of ₹2,000 crore, CET1 capital of ₹130 crore, Additional Tier 1 "
  "capital of ₹10 crore and Tier 2 capital of ₹170 crore. Against RBI's minimum requirements for SFBs, which "
  "statement is correct?",
  ["It meets the CET1 and total CRAR minimums but falls short of the Tier 1 minimum",
   "It meets all three minimums", "It falls short of the CET1 minimum only",
   "It falls short of the total CRAR minimum only"],
  concept="Applying SFB capital ratios",
  explanation="CET1 = 130 ÷ 2,000 = 6.5% (minimum 6%: met). Tier 1 = 140 ÷ 2,000 = 7.0% (minimum 7.5%: not met). "
              "CRAR = 310 ÷ 2,000 = 15.5% (minimum 15%: met).",
  steps=["CET1 6.5% ≥ 6%", "Tier 1 7.0% < 7.5%", "CRAR 15.5% ≥ 15%"],
  why="A high Tier 2 lifts CRAR above 15%, but Tier 1 is still short; CET1 is above 6%.",
  computed=True,
  facts=[fact("SFB minimum capital: CET1 6, Tier 1 7.5, CRAR 15 per cent", CAP_TABLE)])

# ================================================================= 14. Financial Inclusion (3 / 1 / 3)
T = "Financial Inclusion"
Q(T, "PMJDY and allied schemes", "Basic",
  "What was the value of RBI's Financial Inclusion Index (FI-Index) for March 2026?",
  ["70.0", "67.0", "64.2", "43.4"],
  concept="FI-Index",
  explanation="RBI's FI-Index, on a scale of 0 to 100, rose from 43.4 in March 2017 to 67.0 in March 2025 and 70.0 "
              "in March 2026, with improvement across access, usage and quality.",
  steps=["March 2026: 70.0"],
  why="67.0 is March 2025, 64.2 March 2024 and 43.4 March 2017.",
  current=ca("2026-07-16"),
  facts=[fact("The FI Index increased from 43.4 in March 2017 to 70.0 in March 2026", FI_PIB),
         fact("FI-Index for March 2025 stands at 67.0 vis-à-vis 64.2 in March 2024", FI_INDEX_25)])
Q(T, "PMJDY and allied schemes", "Basic",
  "As on 19 August 2026, about how many accounts had been opened under Pradhan Mantri Jan Dhan Yojana?",
  ["59.09 crore", "49.49 crore", "41.29 crore", "32.92 crore"],
  concept="PMJDY coverage",
  explanation="At its 12th anniversary, PMJDY had 59.09 crore accounts (as on 19 August 2026) with deposits of about "
              "₹3.17 lakh crore. 41.29 crore RuPay cards had been issued and 32.92 crore account holders were "
              "women.",
  steps=["PMJDY accounts (19 Aug 2026): 59.09 crore"],
  why="41.29 crore is the number of RuPay cards; 32.92 crore the number of women account holders; 49.49 crore was "
      "an earlier (2023) count.",
  current=ca("2026-08-19"),
  facts=[fact("As on 19th August '26, the total number of PMJDY accounts stands at 59.09 crore; 32.92 crore women; "
              "41.29 crore RuPay cards", PMJDY12)])
Q(T, "PMJDY and allied schemes", "Basic",
  "The five strategic objectives of RBI's National Strategy for Financial Inclusion (NSFI) 2025-30 are together "
  "called:",
  ["Panch-Jyoti", "Panchamrit", "Jan Suraksha", "Saptarishi"],
  concept="NSFI 2025-30",
  explanation="NSFI 2025-30 sets out five strategic objectives called 'Panch-Jyoti', likened to a lamp with five "
              "wicks, to be implemented through 47 action points. The earlier NSFI 2019-24 had six strategic "
              "pillars.",
  steps=["NSFI 2025-30 → five objectives → Panch-Jyoti"],
  why="Panchamrit refers to India's climate commitments; Jan Suraksha to the social security schemes; Saptarishi to "
      "the seven Budget 2023-24 priorities.",
  facts=[fact("NSFI 2025-30 puts forward five strategic objectives (Panch-Jyoti), implemented through 47 action "
              "points", NSFI)])
Q(T, "PMJDY and allied schemes", "Intermediate",
  "RBI's FI-Index is built from three sub-indices. What weights do Access, Usage and Quality carry respectively?",
  ["35%, 45% and 20%", "45%, 35% and 20%", "33%, 33% and 34%", "40%, 40% and 20%"],
  concept="Construction of the FI-Index",
  explanation="The FI-Index (0–100) uses 97 indicators grouped into Access (35%), Usage (45%) and Quality (20%). "
              "Usage carries the highest weight, and recent gains have come mainly from usage.",
  steps=["Access 35%", "Usage 45%", "Quality 20%"],
  why="Usage, not Access, carries 45%; the weights are not equal or 40-40-20.",
  facts=[fact("FI-Index sub-indices Access, Usage and Quality with weights of 35, 45 and 20 per cent respectively; "
              "97 indicators", FI_INDEX_25)])

avg_bal = 316514 / 59.09
assert round(avg_bal) == 5356
Q(T, "PMJDY and allied schemes", "Advanced",
  "As on 19 August 2026, PMJDY accounts numbered 59.09 crore with total deposits of ₹3,16,514 crore. What is the "
  "average balance per account (approx.)?",
  ["₹5,356", "₹535.6", "₹53,560", "₹1,868"],
  concept="Average PMJDY balance",
  explanation="Average balance = ₹3,16,514 crore ÷ 59.09 crore accounts = ₹5,356 (approx.). The crores cancel out.",
  steps=["3,16,514 ÷ 59.09 ≈ 5,356"],
  shortcut="Crore ÷ crore: divide the numbers directly.",
  why="₹535.6 and ₹53,560 are off by a factor of 10; ₹1,868 divides accounts by deposits in lakh crore.",
  computed=True, current=ca("2026-08-19"),
  facts=[fact("Total deposit balances under PMJDY accounts stand at ₹3,16,514 crore; 59.09 crore accounts as on "
              "19th August '26", PMJDY12)])
Q(T, "PMJDY and allied schemes", "Advanced",
  "Consider the following statements about the National Strategies for Financial Inclusion:\nI. NSFI 2025-30 is to "
  "be implemented through 47 action points.\nII. NSFI 2019-24 was built on six strategic pillars.\nIII. NSFI "
  "2025-30 has seven strategic objectives.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="NSFI 2019-24 and 2025-30",
  explanation="NSFI 2025-30 has five strategic objectives (Panch-Jyoti) implemented through 47 action points (I "
              "right, III wrong). The previous strategy, NSFI 2019-24, sought its goals through six strategic "
              "pillars (II right).",
  steps=["I: correct", "II: correct", "III: wrong (five objectives)"],
  why="III is false, so options including it are wrong; 'I only' omits the true statement II.",
  facts=[fact("NSFI 2025-30: five strategic objectives (Panch-Jyoti) implemented through 47 action points; NSFI "
              "2019-24 sought to achieve its goals through six strategic pillars", NSFI)])
Q(T, "Business correspondents", "Advanced",
  "Consider the following statements based on official data released in 2026:\nI. As of 6 March 2026, 99.92% of "
  "villages had a banking outlet within a 5 km radius.\nII. More than 17 lakh Business Correspondents provide "
  "doorstep banking services.\nIII. Business Correspondents are being phased out in favour of bank branches.\nWhich "
  "of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Reach of banking outlets and BCs",
  explanation="PIB reports that 99.92% of villages were covered by banking outlets within 5 km as of 6 March 2026 "
              "(I right) and that over 17.36 lakh BCs support doorstep banking (II right). Access is delivered "
              "through branches, BCs and IPPB outlets together; BCs are not being phased out (III wrong).",
  steps=["I: correct", "II: correct (17.36 lakh)", "III: wrong"],
  why="III contradicts the official description of BCs as a key access channel.",
  current=ca("2026-07-17"),
  facts=[fact("As of 6 March 2026, 99.92% villages covered with banking outlets within a 5 km radius; over 17.36 "
              "lakh BCs supporting doorstep banking services (17 July 2026)", FI_PIB)])

# ================================================================= 15. Priority Sector Lending (2 / 4 / 4)
T = "Priority Sector Lending"
Q(T, "Targets and sub-targets", "Basic",
  "What is the PSL sub-target for lending to Micro Enterprises for domestic commercial banks?",
  ["7.5 per cent of ANBC or CEOBSE, whichever is higher", "10 per cent of ANBC or CEOBSE, whichever is higher",
   "12 per cent of ANBC or CEOBSE, whichever is higher", "18 per cent of ANBC or CEOBSE, whichever is higher"],
  concept="Micro enterprises sub-target",
  explanation="Domestic commercial banks (and foreign banks with 20 or more branches), RRBs, SFBs and UCBs have a "
              "Micro Enterprises sub-target of 7.5% of ANBC or CEOBSE, whichever is higher.",
  steps=["Micro enterprises: 7.5%"],
  why="10% is the small and marginal farmers sub-target, 12% weaker sections and 18% agriculture.",
  facts=[fact("Micro Enterprises: 7.5 per cent of ANBC or CEOBSE, whichever is higher", PSL_MD)])
Q(T, "PSLCs", "Basic",
  "What is the standard lot size in which Priority Sector Lending Certificates (PSLCs) are traded?",
  ["₹25 lakh and multiples thereof", "₹1 crore and multiples thereof", "₹10 lakh and multiples thereof",
   "₹5 crore and multiples thereof"],
  concept="PSLC lot size",
  explanation="PSLCs are traded on RBI's e-Kuber platform in a standard lot size of ₹25 lakh and multiples thereof. "
              "The buyer pays the seller a market-determined fee.",
  steps=["PSLC lot: ₹25 lakh"],
  why="₹10 lakh, ₹1 crore and ₹5 crore are not the prescribed lot size.",
  facts=[fact("The PSLCs would have a standard lot size of ₹25 lakh and multiples thereof", PSL_MD)])
Q(T, "Targets and sub-targets", "Intermediate",
  "Within the 18% agriculture target, what is the sub-target for lending to Small and Marginal Farmers?",
  ["10 per cent of ANBC or CEOBSE", "14 per cent of ANBC or CEOBSE", "8 per cent of ANBC or CEOBSE",
   "12 per cent of ANBC or CEOBSE"],
  concept="Agriculture sub-targets",
  explanation="Within the 18% agriculture target, 14% is prescribed for Non-Corporate Farmers, out of which 10% is "
              "prescribed for Small and Marginal Farmers.",
  steps=["Agriculture 18% → NCF 14% → SMF 10%"],
  why="14% is the NCF sub-target; 12% is weaker sections; 8% is not an agriculture sub-target.",
  facts=[fact("Within this target, 14 percent is prescribed for Non-Corporate Farmers, out of which a target of 10 "
              "percent is prescribed for SMFs", PSL_MD)])
Q(T, "Targets and sub-targets", "Intermediate",
  "For a housing loan to an individual in a centre with population of 50 lakh and above to qualify as priority "
  "sector, what are the limits on the loan amount and the cost of the dwelling unit?",
  ["Loan up to ₹50 lakh and dwelling unit cost up to ₹63 lakh", "Loan up to ₹45 lakh and cost up to ₹57 lakh",
   "Loan up to ₹35 lakh and cost up to ₹44 lakh", "Loan up to ₹50 lakh with no cap on cost"],
  concept="PSL housing limits",
  explanation="In centres with population of 50 lakh and above, a housing loan qualifies if it is up to ₹50 lakh "
              "and the dwelling unit costs up to ₹63 lakh; both criteria must be met. Centres with 10–50 lakh "
              "population: ₹45 lakh/₹57 lakh; below 10 lakh: ₹35 lakh/₹44 lakh.",
  steps=["≥ 50 lakh population: loan ≤ ₹50 lakh AND cost ≤ ₹63 lakh"],
  why="₹45/57 lakh and ₹35/44 lakh are for smaller centres; the cost cap also applies.",
  facts=[fact("Centres with population of 50 lakh and above: loan limit ₹50 lakh, maximum cost of dwelling unit ₹63 "
              "lakh; to be eligible, the loan must satisfy both criteria", PSL_MD)])
Q(T, "Targets and sub-targets", "Intermediate",
  "Loans to individuals for educational purposes, including vocational courses, qualify as priority sector up to:",
  ["₹25 lakh", "₹10 lakh", "₹20 lakh", "₹50 lakh"],
  concept="Education loans under PSL",
  explanation="Under the PSL Directions, 2025, loans to individuals for education, including vocational courses, "
              "not exceeding ₹25 lakh are eligible for priority sector classification.",
  steps=["Education loan ≤ ₹25 lakh → PSL"],
  why="₹10 lakh, ₹20 lakh and ₹50 lakh are not the education-loan ceiling.",
  facts=[fact("Loans to individuals for educational purposes, including vocational courses, not exceeding ₹25 lakh "
              "will be considered as eligible for priority sector", PSL_MD)])
Q(T, "PSLCs", "Intermediate",
  "How are fees on Priority Sector Lending Certificates treated in the accounts of the banks?",
  ["The buyer books the fee as an expense; the seller books it as miscellaneous income",
   "The buyer capitalises the fee as an asset; the seller books it as interest income",
   "Both banks treat it as a provision", "The fee is paid to RBI and not recorded by the banks"],
  concept="Accounting for PSLCs",
  explanation="The buyer pays the seller a market-determined fee. The fee paid for buying a PSLC is an expense, and "
              "the fee received for selling one is miscellaneous income. No loan assets or credit risk are "
              "transferred.",
  steps=["Buyer: expense", "Seller: miscellaneous income"],
  why="The fee is not interest, not a provision and not paid to RBI.",
  facts=[fact("Fee paid for purchase of PSLC treated as Expense and fee received for sale treated as Miscellaneous "
              "Income; buyer pays a market-determined fee to the seller", PSL_MD)])

cities = {"P": (50, 48, 60), "Q": (50, 48, 70), "R": (20, 46, 55), "S": (5, 30, 40)}


def psl_house(pop_lakh, loan, cost):
    lim = (50, 63) if pop_lakh >= 50 else (45, 57) if pop_lakh >= 10 else (35, 44)
    return loan <= lim[0] and cost <= lim[1]


assert [k for k, v in cities.items() if psl_house(*v)] == ["P", "S"]
Q(T, "Targets and sub-targets", "Advanced",
  "Which of these individual housing loans qualify as priority sector?\nP. ₹48 lakh for a ₹60 lakh flat in a city "
  "with population of 1 crore\nQ. ₹48 lakh for a ₹70 lakh flat in the same city\nR. ₹46 lakh for a ₹55 lakh house "
  "in a city with population of 20 lakh\nS. ₹30 lakh for a ₹40 lakh house in a town with population of 5 lakh",
  ["P and S only", "P, Q and S only", "P, R and S only", "P only"],
  concept="Applying PSL housing limits",
  explanation="P: city ≥ 50 lakh, loan ₹48 lakh ≤ 50 and cost ₹60 lakh ≤ 63 → eligible. Q: cost ₹70 lakh > 63 → not "
              "eligible. R: city 10–50 lakh, loan ₹46 lakh > 45 → not eligible. S: town < 10 lakh, loan ₹30 lakh ≤ "
              "35 and cost ₹40 lakh ≤ 44 → eligible.",
  steps=["P: eligible", "Q: cost cap breached", "R: loan cap breached", "S: eligible"],
  why="Q fails the cost test and R fails the loan test; both conditions must hold.",
  computed=True,
  facts=[fact("Housing loan limits: ≥50 lakh population ₹50 lakh/₹63 lakh; 10-50 lakh ₹45 lakh/₹57 lakh; below 10 "
              "lakh ₹35 lakh/₹44 lakh; both criteria to be satisfied", PSL_MD)])

anbc = 10000
target, export_cap, other_min = 0.40 * anbc, 0.32 * anbc, 0.08 * anbc
export, other = 3500, 600
counted = min(export, export_cap) + other
short_total, short_other = target - counted, other_min - other
assert (target, export_cap, other_min, counted, short_total, short_other) == (4000, 3200, 800, 3800, 200, 200)
Q(T, "Targets and sub-targets", "Advanced",
  "A foreign bank with fewer than 20 branches in India has ANBC of ₹10,000 crore (higher than its CEOBSE). It has "
  "export credit of ₹3,500 crore and other priority sector loans of ₹600 crore. What is its position against the PSL "
  "target?",
  ["Short by ₹200 crore, because export credit counts only up to ₹3,200 crore and other sectors must be at least "
   "₹800 crore", "Target met, with ₹100 crore to spare",
   "Short by ₹300 crore, because export credit does not count at all for foreign banks",
   "Short by ₹200 crore in agriculture, which must be 18% of ANBC"],
  concept="PSL for small foreign banks",
  explanation="Foreign banks with fewer than 20 branches have a 40% target (₹4,000 crore), of which up to 32% "
              "(₹3,200 crore) can be export credit and not less than 8% (₹800 crore) must be other priority "
              "sectors. Counted = 3,200 + 600 = ₹3,800 crore → short by ₹200 crore, which is exactly the shortfall "
              "in the 'other sectors' minimum.",
  steps=["Target 40% = ₹4,000 crore", "Export counted up to 32% = ₹3,200 crore", "Other sectors ₹600 vs ₹800 needed",
         "Counted 3,800 → shortfall ₹200 crore"],
  why="Adding all ₹4,100 crore ignores the 32% cap; export credit does count up to 32%; the agriculture sub-target "
      "does not apply to foreign banks with fewer than 20 branches.",
  computed=True,
  facts=[fact("Foreign banks with less than 20 branches: 40 per cent of ANBC or CEOBSE, out of which up to 32% can "
              "be export credit and not less than 8% to any other priority sector; agriculture sub-target not "
              "applicable", PSL_MD)])

prev_ach = 8000
max_no_underlying = prev_ach * 0.5
lots = max_no_underlying / 0.25
assert max_no_underlying == 4000 and lots == 16000
Q(T, "PSLCs", "Advanced",
  "A bank's priority sector achievement last year was ₹8,000 crore. Without holding the underlying loans in its "
  "books, up to what value of PSLCs can it issue this year, and how many standard lots is that?",
  ["₹4,000 crore; 16,000 lots", "₹8,000 crore; 32,000 lots", "₹4,000 crore; 1,600 lots", "₹2,000 crore; 8,000 lots"],
  concept="PSLCs without underlying assets",
  explanation="To deepen the PSLC market, a bank may issue PSLCs up to 50% of its previous year's PSL achievement "
              "without having the underlying in its books (it must still meet its own target on the reporting "
              "date). 50% of ₹8,000 crore = ₹4,000 crore. Lot size ₹25 lakh = ₹0.25 crore → 4,000 ÷ 0.25 = 16,000 "
              "lots.",
  steps=["50% × ₹8,000 crore = ₹4,000 crore", "₹4,000 crore ÷ ₹0.25 crore = 16,000 lots"],
  why="100% overstates the limit; 1,600 lots uses ₹2.5 crore lots; ₹2,000 crore uses 25%.",
  computed=True,
  facts=[fact("A bank is permitted to issue PSLCs upto 50 percent of previous year's PSL achievement without having "
              "the underlying in its books; standard lot size of ₹25 lakh", PSL_MD)])

weighted = 100 * 1.25 + 80 * 0.90 + 50 * 1.00
assert weighted == 247
Q(T, "Targets and sub-targets", "Advanced",
  "In 2026-27 a bank's incremental priority sector credit is ₹100 crore in a district with per capita PSL below "
  "₹9,000, ₹80 crore in a district with per capita PSL above ₹42,000, and ₹50 crore in other districts. For PSL "
  "achievement, what is this incremental credit worth after RBI's district weights?",
  ["₹247 crore", "₹230 crore", "₹265 crore", "₹212 crore"],
  concept="District weights in PSL",
  explanation="From 2024-25, incremental PSL in low-credit districts (per capita PSL < ₹9,000) gets 125% weight and "
              "in high-credit districts (> ₹42,000) gets 90%; others get 100%. 100 × 1.25 + 80 × 0.90 + 50 × 1 = "
              "125 + 72 + 50 = ₹247 crore.",
  steps=["100 × 125% = 125", "80 × 90% = 72", "50 × 100% = 50", "Total = 247"],
  why="₹230 crore ignores the weights; ₹265 crore gives 125% to both special districts; ₹212 crore swaps 125% and "
      "90%.",
  computed=True,
  facts=[fact("Higher weight (125%) to incremental PSL in districts with per capita PSL less than ₹9,000 and lower "
              "weight (90%) where per capita PSL is greater than ₹42,000; others 100%; lists valid up to FY 2026-27",
              PSL_MD)])

# ================================================================= 16. RBI Integrated Ombudsman Scheme (1 / 2 / 2)
T = "RBI Integrated Ombudsman Scheme"
Q(T, "Process and limits", "Basic",
  "Under RB-IOS, 2026, complaints sent by e-mail or in physical form are received and processed by the Centralised "
  "Receipt and Processing Centre located at:",
  ["Chandigarh", "Mumbai", "New Delhi", "Kolkata"],
  concept="CRPC",
  explanation="Online complaints are lodged on cms.rbi.org.in. E-mail and physical complaints go to the "
              "Centralised Receipt and Processing Centre, Reserve Bank of India, Central Vista, Sector 17, "
              "Chandigarh.",
  steps=["CRPC: Sector 17, Chandigarh"],
  why="RBI's central office is in Mumbai, but the CRPC is in Chandigarh.",
  current=ca("2026-07-01"),
  facts=[fact("Physical complaints to Centralised Receipt and Processing Centre, Reserve Bank of India, Central "
              "Vista, Sector 17, Chandigarh - 160017", RBIOS_FAQ)])
Q(T, "Scope and grounds", "Intermediate",
  "Which NBFCs are covered under RB-IOS, 2026?",
  ["NBFCs (other than excluded types such as HFCs and CICs) that accept deposits, or have customer interface with "
   "asset size of ₹100 crore and above", "All NBFCs registered with RBI without exception",
   "Only deposit-taking NBFCs with assets above ₹500 crore", "Only NBFC-Upper Layer entities"],
  concept="Coverage of NBFCs",
  explanation="RB-IOS, 2026 covers NBFCs registered with RBI, excluding HFCs, Core Investment Companies, IDF-NBFCs, "
              "NBFC-IFCs, NOFHCs, Primary Dealers and Mortgage Guarantee Companies, which either are authorised to "
              "accept deposits or have customer interface with an asset size of ₹100 crore and above.",
  steps=["Excluded types removed", "Deposit-taking OR customer interface with assets ≥ ₹100 crore"],
  why="Not all NBFCs are covered; the threshold is ₹100 crore, not ₹500 crore; coverage is not limited to the "
      "upper layer.",
  current=ca("2026-07-01"),
  facts=[fact("NBFCs covered: all NBFCs registered with RBI excluding HFCs, CICs, IDF-NBFCs, NBFC-IFCs, NOFHCs, "
              "Primary Dealers and Mortgage Guarantee Companies, which either are authorized to accept deposits or "
              "have customer interface with asset size of Rs 100 crore and above", RBIOS_FAQ)])
Q(T, "Process and limits", "Intermediate",
  "Can a complaint under RB-IOS, 2026 be filed directly through RBI's Contact Centre (toll-free number 14448)?",
  ["No; the Contact Centre only guides on filing and gives status information",
   "Yes, a complaint registered on the phone call is treated as filed",
   "Yes, but only for digital payment complaints", "Yes, but only on national holidays"],
  concept="RBI Contact Centre",
  explanation="Complaints cannot be filed through the Contact Centre. It helps complainants with the procedure for "
              "filing through CMS, e-mail or physical mode and with complaint status. Its IVRS works 24x7.",
  steps=["Contact Centre: guidance and status only"],
  why="No category of complaint can be lodged by phone through the Contact Centre.",
  current=ca("2026-07-01"),
  facts=[fact("Complaints cannot be filed directly through the Contact Center; it can assist with the procedure and "
              "status; Toll Free No. 14448", RBIOS_FAQ)])
Q(T, "Scope and grounds", "Advanced",
  "Which of the following complaints can be entertained (is maintainable) under RB-IOS, 2026, assuming all other "
  "conditions are met?\nI. A complaint filed on the customer's behalf by an advocate who is not the aggrieved "
  "person\nII. A complaint about a fraudulent debit where a police investigation into the criminal offence has "
  "been initiated\nIII. A complaint against a bank's commercial decision to decline a loan",
  ["II only", "I and II only", "II and III only", "I, II and III"],
  concept="Maintainability under RB-IOS, 2026",
  explanation="Complaints through an advocate (unless the advocate is the aggrieved person) are not maintainable "
              "(I fails). Pending criminal proceedings or a police investigation into a criminal offence are not "
              "treated as the 'same grievance' before another forum, so II can be entertained. Matters of a "
              "regulated entity's commercial judgment are not maintainable (III fails).",
  steps=["I: barred (advocate)", "II: maintainable", "III: barred (commercial judgment)"],
  why="Any option including I or III includes a non-maintainable complaint.",
  current=ca("2026-07-01"),
  facts=[fact("Not maintainable: complaints through an advocate unless the advocate is the aggrieved person; matters "
              "relating to commercial judgment; criminal proceedings or police investigation are not treated as the "
              "same grievance", RBIOS_FAQ)])

award_received = dt.date(2026, 8, 10)
accept_by = award_received + dt.timedelta(days=30)
letter_received_by_re = dt.date(2026, 9, 4)
comply_by = letter_received_by_re + dt.timedelta(days=30)
assert accept_by == dt.date(2026, 9, 9) and comply_by == dt.date(2026, 10, 4)
Q(T, "Process and limits", "Advanced",
  "Asha receives a copy of an RBI Ombudsman's Award on 10 August 2026 and does not appeal. The bank receives her "
  "letter of acceptance on 4 September 2026. Under RB-IOS, 2026, by when must Asha furnish the acceptance, and by "
  "when must the bank comply (or appeal, where permitted)?",
  ["Acceptance by 9 September 2026; bank to act by 4 October 2026",
   "Acceptance by 9 September 2026; bank to act by 9 October 2026",
   "Acceptance by 10 October 2026; bank to act by 4 November 2026",
   "Acceptance by 24 August 2026; bank to act by 19 September 2026"],
  concept="Timelines after an Award",
  explanation="The complainant must furnish a letter of acceptance to the regulated entity within 30 days of "
              "receiving the Award: 10 August + 30 days = 9 September 2026. The regulated entity must comply and "
              "intimate compliance, or appeal where permitted, within 30 days of receiving the acceptance: 4 "
              "September + 30 days = 4 October 2026.",
  steps=["10 Aug + 30 days = 9 Sep", "4 Sep + 30 days = 4 Oct"],
  why="The bank's 30 days run from receipt of the acceptance letter (4 September), not from 9 September; 60-day and "
      "14-day periods are not prescribed.",
  computed=True, current=ca("2026-07-01"),
  facts=[fact("Complainant must furnish a letter of acceptance within 30 days from receipt of the Award; the "
              "Regulated Entity must comply or appeal within 30 days from receipt of the letter of acceptance",
              RBIOS_FAQ)])

# ================================================================= 17. Digital Banking (3 / 6 / 1)
T = "Digital Banking"
Q(T, "CBDC (e-rupee)", "Basic",
  "Is a minimum balance required to open or maintain a retail e-rupee (e₹) wallet?",
  ["No, no minimum balance is required", "Yes, ₹1,000", "Yes, ₹500", "Yes, equal to the bank account's minimum"],
  concept="e₹ wallets",
  explanation="RBI's FAQs state that there is no minimum balance requirement to open or maintain an e₹ wallet, and "
              "no charges or fees for using e₹.",
  steps=["e₹ wallet: no minimum balance, no fees"],
  why="No minimum balance of any amount applies to e₹ wallets.",
  facts=[fact("There is no minimum balance required to open/maintain an e₹ wallet; no charges or fees", ERUPEE_FAQ)])
Q(T, "Mobile and internet banking", "Basic",
  "Which institution has been authorised as the exclusive registrar for the '.bank.in' internet domain that RBI "
  "asked banks to migrate to?",
  ["IDRBT", "NPCI", "CERT-In", "NIXI directly, without any registrar"],
  concept=".bank.in domain",
  explanation="To combat phishing and fraud in digital payments, RBI operationalised the '.bank.in' domain through "
              "the Institute for Development and Research in Banking Technology (IDRBT), authorised by NIXI under "
              "MeitY to be its exclusive registrar.",
  steps=[".bank.in registrar: IDRBT (authorised by NIXI, MeitY)"],
  why="NPCI runs payment systems; CERT-In handles cyber incidents; NIXI authorised IDRBT rather than registering "
      "the domains itself.",
  current=ca("2025-04-22"),
  facts=[fact("'.bank.in' domain operationalised through IDRBT, authorised by NIXI under MeitY to serve as the "
              "exclusive registrar", BANK_IN)])
Q(T, "Mobile and internet banking", "Basic",
  "RBI's Digital Payments Index (RBI-DPI) measures the extent of digitisation of payments with which period as its "
  "base (=100)?",
  ["March 2018", "March 2016", "November 2016", "April 2021"],
  concept="RBI-DPI",
  explanation="RBI has published the composite RBI-DPI since 1 January 2021 with March 2018 as the base. The index "
              "stood at 516.76 for September 2025 against 493.22 for March 2025.",
  steps=["Base: March 2018 = 100"],
  why="The other months are not the index base; 2021 is when publication began.",
  facts=[fact("RBI-DPI published since January 1, 2021 with March 2018 as base; index for September 2025 stands at "
              "516.76", DPI_PR)])
Q(T, "CBDC (e-rupee)", "Intermediate",
  "How does the retail e-rupee (e₹) differ from UPI, according to RBI?",
  ["e₹ is a digital form of the rupee that can also serve as a store of value, whereas UPI is a means of payment",
   "e₹ is a payment app, whereas UPI is legal tender issued by RBI",
   "e₹ payments always settle through the user's bank account, unlike UPI",
   "e₹ can be used only for merchant payments, whereas UPI is only for person-to-person transfers"],
  concept="e₹ versus UPI",
  explanation="e₹ is a digital form of the rupee; UPI is a means of payment. e₹ can be withdrawn from a bank "
              "account and kept in the e₹ wallet as a store of value. Payments at a CBDC QR settle instantly "
              "between e₹ wallets without passing through bank accounts.",
  steps=["e₹ = money (store of value)", "UPI = payment system"],
  why="UPI is not legal tender; e₹ wallet-to-wallet payments do not pass through bank accounts; both support P2P "
      "and P2M.",
  facts=[fact("e₹ is a digital form of ₹ whereas UPI is a means of payment; e₹ also serves as a store of value; "
              "transactions at a CBDC QR happen between two e₹ wallets and settle instantaneously", ERUPEE_FAQ)])
Q(T, "Mobile and internet banking", "Intermediate",
  "By what date did RBI require all banks to complete migration of their existing internet domains to '.bank.in'?",
  ["31 October 2025", "31 March 2025", "1 April 2026", "31 December 2026"],
  concept=".bank.in migration deadline",
  explanation="RBI's circular of 22 April 2025 asked all banks to begin migrating to the '.bank.in' domain and to "
              "complete the process at the earliest and in any case not later than 31 October 2025.",
  steps=["Circular 22 April 2025", "Deadline 31 October 2025"],
  why="The other dates are not the deadline in the circular.",
  current=ca("2025-04-22"),
  facts=[fact("All banks are advised to commence the migration to the '.bank.in' domain and complete the process ... "
              "not later than October 31, 2025 (circular dated April 22, 2025)", BANK_IN)])
Q(T, "Mobile and internet banking", "Intermediate",
  "Under RBI's Digital Banking Channels Authorisation Directions, 2025, what does a bank need before launching a "
  "transactional internet or mobile banking facility?",
  ["Prior approval of RBI, applied for through the PRAVAAH portal", "Only approval of its own Board",
   "Approval of NPCI", "No approval, if it has implemented Core Banking Solution"],
  concept="Authorisation of digital banking channels",
  explanation="Banks with CBS and IPv6-enabled public-facing IT infrastructure can offer view-only digital banking "
              "on their own. A transactional facility needs RBI's prior approval, applied for through PRAVAAH, "
              "subject to eligibility such as minimum CRAR and net worth.",
  steps=["View-only: eligible banks may offer", "Transactional: prior RBI approval via PRAVAAH"],
  why="Board approval alone or CBS alone is enough only for view-only facilities; NPCI does not authorise banks' "
      "channels.",
  facts=[fact("Banks shall require prior approval of the Reserve Bank for launching transactional banking facility; "
              "apply through the PRAVAAH portal; CBS and IPv6-enabled banks eligible for view only facility",
              DBC_MD)])
Q(T, "Digital lending", "Intermediate",
  "Under the RBI (Digital Lending) Directions, 2025, can a lender automatically increase a borrower's credit limit "
  "on a digital loan?",
  ["No; only on an explicit request from the borrower, which is evaluated and recorded",
   "Yes, if the borrower has repaid on time for three months", "Yes, up to 25% of the existing limit",
   "Yes, if the lending service provider recommends it"],
  concept="Credit limits in digital lending",
  explanation="The Directions require regulated entities to ensure there is no automatic increase in credit limit "
              "unless an explicit request is received from the borrower, evaluated and kept on record.",
  steps=["No auto-increase; explicit borrower request needed"],
  why="Repayment history, percentages or LSP recommendations do not permit automatic increases.",
  current=ca("2025-05-08"),
  facts=[fact("RE shall ensure that there is no automatic increase in credit limit unless an explicit request is "
              "received, evaluated and kept on record from the borrower", DL_2025)])
Q(T, "Digital lending", "Intermediate",
  "Under the RBI (Digital Lending) Directions, 2025, regulated entities must report all digital lending apps (DLAs) "
  "they deploy or join on which RBI portal, whose data RBI then publishes on its website?",
  ["Centralised Information Management System (CIMS)", "PRAVAAH", "Complaint Management System (CMS)",
   "e-Kuber"],
  concept="DLA reporting",
  explanation="REs must report all DLAs, their own or their LSPs', on RBI's CIMS portal (by 15 June 2025 for "
              "existing DLAs). The data is published on RBI's website automatically; RBI does not verify it, and "
              "the RE remains responsible for its correctness.",
  steps=["Report DLAs on CIMS", "RBI publishes the list without verifying it"],
  why="PRAVAAH handles regulatory applications; CMS handles complaints; e-Kuber is RBI's core banking platform.",
  current=ca("2025-06-15"),
  facts=[fact("RE shall report all DLAs on the Centralised Information Management System (CIMS) portal of RBI; data "
              "published on RBI website in an automated manner; reporting completed by June 15, 2025", DL_2025)])
Q(T, "Digital lending", "Intermediate",
  "Under the RBI (Digital Lending) Directions, 2025, which mobile phone resources must a digital lending app NOT "
  "access?",
  ["Files and media, contact list and call logs", "The camera, even once for KYC", "The location, even once",
   "The microphone, even once"],
  concept="Data access by lending apps",
  explanation="Data collection by DLAs must be need-based and with explicit prior consent. Apps must desist from "
              "accessing files and media, contact lists, call logs and telephony functions. One-time access to "
              "the camera, microphone or location may be taken where necessary (e.g. for KYC), with consent.",
  steps=["Barred: files/media, contacts, call logs, telephony", "One-time access allowed: camera, microphone, "
                                                                  "location"],
  why="Camera, location and microphone can be accessed once with consent for a necessary purpose such as onboarding "
      "or KYC.",
  facts=[fact("DLA of RE/LSP desist from accessing mobile phone resources like file and media, contact list, call "
              "logs, telephony functions; a one-time access can be taken for camera, microphone, location", DL_2025)])
Q(T, "Digital lending", "Advanced",
  "Under the RBI (Digital Lending) Directions, 2025, a regulated entity may NOT enter into a default loss guarantee "
  "(DLG) arrangement for which of the following?\nI. Revolving credit facilities offered through the digital lending "
  "channel, and credit cards\nII. Loans covered by credit guarantee schemes administered by trust funds such as "
  "CGTMSE\nIII. Term loans to individuals sourced through a lending service provider",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Limits on DLG arrangements",
  explanation="The Directions bar DLG arrangements for revolving credit facilities offered digitally and for credit "
              "cards (I), and for loans already covered by credit guarantee schemes run by trust funds (II). "
              "NBFC-P2P platforms also cannot offer DLG. Ordinary term loans sourced through an LSP can carry DLG "
              "within the 5% cap (III is allowed).",
  steps=["I: barred", "II: barred", "III: permitted (subject to the 5% cap)"],
  why="III is permitted, so options including it are wrong; 'I only' omits the bar on CGS-covered loans.",
  current=ca("2025-05-08"),
  facts=[fact("RE shall not enter into DLG arrangements for revolving credit facilities offered through digital "
              "lending channel and credit cards, nor on loans covered by credit guarantee schemes administered by "
              "trust funds; NBFC-P2P shall not enter into DLG arrangements", DL_2025)])

# ================================================================= 18. UPI (3 / 1 / 1)
T = "UPI"
Q(T, "Features", "Basic",
  "The BHIM app, which also made UPI available on basic phones through the *99# USSD option, was launched on:",
  ["30 December 2016", "11 April 2016", "8 March 2022", "22 November 2010"],
  concept="BHIM",
  explanation="BHIM was launched on 30 December 2016. Along with it, UPI became available on non-internet mobile "
              "devices through the *99# dialling option.",
  steps=["BHIM: 30 December 2016"],
  why="8 March 2022 is UPI123Pay; 22 November 2010 relates to IMPS; 11 April 2016 is not the BHIM launch.",
  facts=[fact("Along with BHIM on December 30, 2016, UPI is now available for non-internet based mobile devices in "
              "the form of dialling option (*99#)", PAY_BOOKLET)])
Q(T, "Features", "Basic",
  "'Hello! UPI', launched in September 2023, enables:",
  ["Conversational, voice-based UPI payments, built with Bhashini and NPCI", "UPI payments by NRIs from abroad",
   "Offline UPI payments only through NFC cards", "UPI payments using a credit card from any network"],
  concept="Conversational payments",
  explanation="Hello! UPI is an AI voice-enabled feature built by Bhashini (under MeitY) with NPCI. It lets users "
              "make conversation-based UPI payments in Hindi and English on feature phones and smartphones.",
  steps=["Hello! UPI = voice/conversational UPI"],
  why="It is not an NRI, NFC-only or credit-card feature.",
  facts=[fact("'Hello! UPI', an AI-voice-enabled payment feature built by Bhashini (under MeitY) along with NPCI, "
              "allows conversation-based UPI transactions in Hindi and English", DFS_YE25)])
Q(T, "Features", "Basic",
  "Under RBI's circular of 4 September 2023, which new type of funding account can be used for UPI payments?",
  ["Pre-sanctioned credit lines issued by scheduled commercial banks to individuals", "Fixed deposits of any bank",
   "Public Provident Fund accounts", "Demat accounts"],
  concept="Credit line on UPI",
  explanation="Savings accounts, overdraft accounts, prepaid wallets and credit cards could already be linked to "
              "UPI. The September 2023 circular added pre-sanctioned credit lines issued by scheduled commercial "
              "banks to individuals, with their prior consent.",
  steps=["New UPI funding account (Sept 2023): bank credit lines"],
  why="FDs, PPF and demat accounts were not added as UPI funding accounts.",
  facts=[fact("Payments through a pre-sanctioned credit line issued by a Scheduled Commercial Bank to individuals, "
              "with prior consent, are enabled for transactions using UPI (September 04, 2023)", UPI_CL)])
Q(T, "UPI Lite and international", "Intermediate",
  "According to the Department of Financial Services' Year Ender 2025, acceptance of Indian UPI apps through QR codes "
  "had been operationalised in which group of countries?",
  ["Bhutan, France, Mauritius, Nepal, Singapore, Sri Lanka, UAE and Qatar",
   "USA, UK, Japan and Germany only", "Only SAARC countries", "Only Singapore and UAE"],
  concept="UPI abroad",
  explanation="DFS reported that UPI QR acceptance had been operationalised in Bhutan, France, Mauritius, Nepal, "
              "Singapore, Sri Lanka, the UAE and Qatar, letting Indian travellers pay merchants with their UPI apps.",
  steps=["UPI QR acceptance: Bhutan, France, Mauritius, Nepal, Singapore, Sri Lanka, UAE, Qatar"],
  why="The list includes non-SAARC countries such as France and Qatar, and is wider than Singapore and the UAE; the "
      "USA, UK, Japan and Germany are not on it.",
  current=ca("2026-01-10"),
  facts=[fact("Acceptance of India's UPI apps via QR Code has been operationalised in Bhutan, France, Mauritius, "
              "Nepal, Singapore, Sri Lanka, the UAE and Qatar", DFS_YE25)])
Q(T, "Features", "Advanced",
  "Which of the following were launched in September 2023 to promote financial inclusion through UPI?\nI. Credit "
  "Line on UPI\nII. Conversational payments (Hello! UPI and BillPay Connect)\nIII. UPI LITE X",
  ["I, II and III", "I and II only", "II and III only", "I only"],
  concept="UPI enhancements, 2023",
  explanation="The Department of Financial Services lists Credit Line on UPI, conversational payments (Hello! UPI "
              "and BillPay Connect) and UPI LITE X as launched in September 2023 to promote financial inclusion. "
              "All three are correct.",
  steps=["I, II and III: all launched September 2023"],
  why="Each other option leaves out at least one of the three launches.",
  facts=[fact("Credit Line on UPI, Conversational Payments (Hello! UPI & BillPay Connect) and UPI LITE X were "
              "launched in September 2023", DFS_YE25)])

# ================================================================= 19. NEFT (1 / 2 / 2)
T = "NEFT"
Q(T, "Settlement and timings", "Basic",
  "Has RBI prescribed any minimum or maximum amount for funds transfer through NEFT?",
  ["No; RBI imposes no limit, though banks may set limits with Board approval", "Yes, a minimum of ₹2 lakh",
   "Yes, a maximum of ₹5 lakh", "Yes, a maximum of ₹10 lakh per day"],
  concept="NEFT limits",
  explanation="RBI imposes no limit on NEFT transfers. A member bank may set amount limits based on its own risk "
              "perception with the approval of its Board. (Only cash-based NEFT remittances by non-account holders "
              "are capped at ₹50,000.)",
  steps=["No RBI limit on NEFT"],
  why="₹2 lakh is the RTGS minimum; ₹5 lakh is an IMPS limit; there is no ₹10 lakh daily NEFT cap.",
  facts=[fact("No, there is no limit imposed by the RBI for funds transfer through NEFT; a member bank may place "
              "amount limits with the approval of its Board", NEFT_FAQ)])
Q(T, "Settlement and timings", "Intermediate",
  "Outbound remittances through India's NEFT system are permitted only to which country?",
  ["Nepal, under the Indo-Nepal Remittance Facility Scheme", "Bhutan", "Bangladesh", "Sri Lanka"],
  concept="NEFT cross-border",
  explanation="Outbound remittances through NEFT are allowed only to Nepal under the Indo-Nepal Remittance Facility "
              "Scheme. The beneficiary in Nepal receives Nepalese rupees and need not have a bank account.",
  steps=["NEFT outbound: Nepal only (INRF)"],
  why="NEFT does not carry outbound remittances to Bhutan, Bangladesh or Sri Lanka.",
  facts=[fact("The outbound remittances through NEFT system are permitted only to Nepal under Indo-Nepal Remittance "
              "Facility (INRF) Scheme", NEFT_FAQ)])
Q(T, "Settlement and timings", "Intermediate",
  "The Indian Financial System Code (IFSC) used in NEFT is an 11-character code in which:",
  ["The first 4 letters identify the bank, the 5th character is 0, and the last 6 identify the branch",
   "The first 6 characters identify the branch and the last 5 the bank", "All 11 characters are digits",
   "It is the same as the 9-digit MICR code with two check letters"],
  concept="IFSC",
  explanation="IFSC is an 11-character alphanumeric code: the first 4 alphabetic characters represent the bank, the "
              "5th character is 0 (zero), and the last 6 characters represent the branch.",
  steps=["4 letters (bank) + 0 + 6 characters (branch)"],
  why="The bank code comes first; IFSC is alphanumeric; the MICR code is a separate 9-digit code.",
  facts=[fact("IFSC is a 11-digit code with the first 4 alpha characters representing the bank, the last 6 "
              "characters representing the branch; the 5th character is 0", NEFT_FAQ)])

amt, days = 400000, 5
penal = amt * (REPO + 2) / 100 * days / 365
assert round(penal) == 411
Q(T, "Settlement and timings", "Advanced",
  "A NEFT transfer of ₹4 lakh is neither credited to the beneficiary nor returned for 5 days beyond the 2-hour limit. "
  "With the repo rate at 5.50%, how much penal interest (approx.) must the bank pay the customer, and must the "
  "customer claim it?",
  ["About ₹411, credited without waiting for a claim", "About ₹301, payable only on a written claim",
   "About ₹411, payable only on a written claim", "About ₹630, credited without waiting for a claim"],
  concept="Compensation for delayed NEFT",
  explanation="If a NEFT transaction is not credited or returned within two hours of batch settlement, the bank "
              "pays penal interest at the current RBI LAF repo rate plus 2% for the period of delay, without the "
              "customer having to claim it. 4,00,000 × 7.5% × 5/365 ≈ ₹411.",
  steps=["Rate = 5.50% + 2% = 7.5%", "4,00,000 × 0.075 × 5 ÷ 365 ≈ ₹411", "Paid without a claim"],
  why="₹301 uses the repo rate without the 2% add-on; ₹630 uses a rate of about 11.5%, far above repo + 2%; "
      "compensation does not require a claim.",
  computed=True, current=CORRIDOR,
  facts=[fact("Penal interest at the current RBI LAF Repo Rate plus two percent for the period of delay, without "
              "waiting for a specific claim to be lodged by the customer", NEFT_FAQ),
         fact("Policy repo rate 5.50 per cent", MPC_OCT26)])
Q(T, "Settlement and timings", "Advanced",
  "Consider the following statements about NEFT:\nI. NEFT is a credit-push system; a customer cannot originate a "
  "NEFT transaction to pull funds from another account.\nII. Banks may not charge savings account holders for NEFT "
  "transfers initiated online.\nIII. Credit to the beneficiary is given on the basis of both the account number and "
  "the beneficiary's name, which must match.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="NEFT features",
  explanation="NEFT is credit-push only (I right). From 1 January 2020 banks may not charge savings account holders "
              "for online NEFT transfers (II right). Credit is given solely on the basis of the account number; "
              "the remitter must ensure it is correct (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (account number only)"],
  why="III is false, so options including it are wrong; 'I only' omits the true statement II.",
  facts=[fact("NEFT is a credit-push system; no charges to savings bank account holders for NEFT transfers initiated "
              "online from January 01, 2020; credit to beneficiary account is released solely based on account "
              "number", NEFT_FAQ)])

# ================================================================= 20. RTGS (1 / 2 / 1)
T = "RTGS"
Q(T, "Limits and timings", "Basic",
  "From which date has RTGS been available round the clock on all days (24x7x365)?",
  ["14 December 2020", "16 December 2019", "26 March 2004", "1 July 2019"],
  concept="RTGS availability",
  explanation="RTGS has been available on a 24x7x365 basis since 14 December 2020. NEFT became 24x7 earlier, on 16 "
              "December 2019.",
  steps=["RTGS 24x7: 14 December 2020"],
  why="16 December 2019 is NEFT's 24x7 date; March 2004 is when RTGS started; 1 July 2019 is when RBI waived its "
      "processing charges.",
  facts=[fact("RTGS is available 24x7x365 basis with effect from December 14, 2020; RBI waived processing charges "
              "from July 01, 2019", RTGS_FAQ)])
Q(T, "Limits and timings", "Intermediate",
  "If funds received through RTGS cannot be credited to the beneficiary, within what time must the receiving bank "
  "return them to the originating bank?",
  ["Within one hour of receipt or before the end of the RTGS business day, whichever is earlier",
   "Within 30 minutes of receipt", "Within two hours of batch settlement", "By the next working day"],
  concept="RTGS returns",
  explanation="Funds that cannot be credited must be returned to the originating bank within one hour of receipt at "
              "the Member Interface or before the end of the RTGS business day, whichever is earlier. (Credit "
              "itself must be given within 30 minutes.)",
  steps=["Return: 1 hour or end of business day, whichever earlier"],
  why="30 minutes is the time to credit, not to return; two hours after batch settlement is the NEFT rule.",
  facts=[fact("Funds will be returned to the originating bank within one hour of receipt of the payment at the "
              "Member Interface or before the end of the RTGS Business Day, whichever is earlier", RTGS_FAQ)])
Q(T, "Limits and timings", "Intermediate",
  "Membership of RTGS, according to RBI's FAQs, is open to which of the following?",
  ["Scheduled/licensed banks, standalone primary dealers, PPI issuers, white label ATM operators and card networks",
   "Only scheduled commercial banks", "Banks and all registered mutual funds", "Any company registered in India"],
  concept="RTGS membership",
  explanation="RBI has opened RTGS membership to all scheduled/licensed banks, standalone primary dealers, PPI "
              "issuers, white label ATM operators and card networks.",
  steps=["RTGS members: banks, standalone PDs, PPI issuers, WLAOs, card networks"],
  why="Membership is wider than scheduled commercial banks, but mutual funds and ordinary companies are not "
      "eligible.",
  facts=[fact("Membership of RTGS shall be open to all scheduled/licensed banks, standalone primary dealers, PPI "
              "issuers, white label ATM operators and card networks", RTGS_FAQ)])
Q(T, "Limits and timings", "Advanced",
  "Consider the following statements about RTGS:\nI. RTGS does not accept future value-dated transactions.\nII. "
  "Compensation for delay in returning a failed RTGS payment is credited to the customer automatically, without a "
  "request.\nIII. Because RTGS is a gross settlement system, the beneficiary's name is matched with the account "
  "number before credit.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="RTGS rules",
  explanation="RTGS does not accept future value-dated transactions (I right). Compensation at repo + 2% for "
              "delays must be credited automatically without a request (II right). Name and account number are "
              "not matched in real time; credit is based solely on the account number (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong"],
  why="III is false, so options including it are wrong; 'I only' omits the true statement II.",
  facts=[fact("RTGS does not accept future value dated transactions; compensation credited automatically without "
              "any request; credit to the beneficiary given solely based on account number", RTGS_FAQ)])

# ================================================================= 21. IMPS (1 / 1 / 1)
T = "IMPS"
Q(T, "Limits and features", "Basic",
  "Through which channels can IMPS, NPCI's 24x7 instant funds transfer service, be accessed?",
  ["Internet banking, mobile banking apps, bank branches, ATMs, SMS and IVRS", "Only mobile banking apps",
   "Only bank branches during working hours", "Only ATMs"],
  concept="IMPS channels",
  explanation="RBI describes IMPS as a 24x7 instant domestic funds transfer facility accessible through internet "
              "banking, mobile banking apps, bank branches, ATMs, SMS and IVRS.",
  steps=["IMPS: multi-channel, 24x7"],
  why="IMPS is not limited to a single channel or to branch hours.",
  facts=[fact("IMPS provides 24x7 instant domestic funds transfer and is accessible through internet banking, mobile "
              "banking apps, bank branches, ATMs, SMS and IVRS", IMPS_RBI)])
Q(T, "Limits and features", "Intermediate",
  "When RBI decided in October 2021 to raise the IMPS per-transaction limit for most channels, what limit applied to "
  "the SMS and IVRS channels?",
  ["₹5,000 per transaction", "₹2 lakh per transaction", "₹5 lakh per transaction", "₹50,000 per transaction"],
  concept="IMPS channel limits",
  explanation="RBI noted that the IMPS limit was ₹2 lakh per transaction for channels other than SMS and IVRS "
              "(since January 2014) and ₹5,000 for the SMS and IVRS channels. It proposed raising only the former "
              "to ₹5 lakh.",
  steps=["SMS/IVRS: ₹5,000", "Other channels: ₹2 lakh → ₹5 lakh"],
  why="₹2 lakh and ₹5 lakh are the old and new limits for other channels; ₹50,000 is the NEFT cash remittance cap.",
  facts=[fact("The per-transaction limit for SMS and IVRS channels is ₹5000; ₹2 lakh for other channels since January "
              "2014, proposed to be increased to ₹5 lakh", IMPS_RBI)])
Q(T, "Limits and features", "Advanced",
  "Consider the following statements about RBI's October 2021 decision on IMPS:\nI. The ₹2 lakh limit for channels "
  "other than SMS and IVRS had applied since January 2014.\nII. RBI linked the increase partly to RTGS becoming "
  "available round the clock, which increased IMPS settlement cycles and reduced risk.\nIII. The limit for SMS and "
  "IVRS channels was also raised to ₹5 lakh.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Rationale for the IMPS limit increase",
  explanation="The ₹2 lakh limit had applied since January 2014 (I right). RBI noted that with RTGS operating round "
              "the clock, IMPS settlement cycles had increased, reducing credit and settlement risks (II right). "
              "The increase to ₹5 lakh was only for channels other than SMS and IVRS (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong"],
  why="III is false, so options including it are wrong; 'I only' omits the true statement II.",
  facts=[fact("Per-transaction limit effective from January 2014 capped at ₹2 lakh for channels other than SMS and "
              "IVRS; with RTGS operational round the clock, increase in settlement cycles of IMPS reduced risks; "
              "increase from ₹2 lakh to ₹5 lakh for channels other than SMS and IVRS", IMPS_RBI)])

# ================================================================= 22. NPCI (1 / 2 / 3)
T = "NPCI"
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Basic",
  "Which entity is the authorised Bharat Bill Payment Central Unit (BBPCU) for the Bharat Bill Payment System?",
  ["NPCI Bharat BillPay Ltd (NBBL), a wholly owned subsidiary of NPCI", "The Reserve Bank of India itself",
   "The Clearing Corporation of India Ltd (CCIL)", "The Indian Banks' Association"],
  concept="Bharat Bill Payment System",
  explanation="BBPS has a tiered structure with a central unit (BBPCU) and operating units (BBPOUs). RBI's directions "
              "name NPCI Bharat BillPay Ltd (NBBL), a wholly owned subsidiary of NPCI, as the BBPCU.",
  steps=["BBPCU = NBBL (NPCI subsidiary)"],
  why="RBI regulates BBPS but is not its central unit; CCIL and IBA have no BBPS role.",
  facts=[fact("NPCI Bharat Bill Pay Ltd (NBBL) as a Central Unit (BBPCU); NBBL - a wholly owned subsidiary of NPCI",
              BBPS_MD)])
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Intermediate",
  "From which institution did NPCI take over the management of the National Financial Switch (NFS) ATM network in "
  "December 2009?",
  ["IDRBT", "RBI's Department of Payment and Settlement Systems", "State Bank of India", "CCIL"],
  concept="National Financial Switch",
  explanation="NFS was developed by IDRBT. In December 2009 NPCI took over from IDRBT the task of managing NFS, then "
              "an ATM network of 37 members with about 50,000 ATMs.",
  steps=["NFS: developed by IDRBT → managed by NPCI from Dec 2009"],
  why="RBI, SBI and CCIL did not run NFS before NPCI.",
  facts=[fact("NPCI took over from IDRBT in December 2009 the task of managing NFS which operated an ATM network "
              "having 37 members with 50,000 ATMs", PAY_BOOKLET)])
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Intermediate",
  "When did live operations of the Bharat Bill Payment System (BBPS) commence, after its pilot launch on 31 August "
  "2016?",
  ["17 October 2017", "1 April 2016", "30 December 2016", "1 January 2019"],
  concept="BBPS timeline",
  explanation="The BBPS pilot was launched on 31 August 2016, and live operations commenced on 17 October 2017.",
  steps=["Pilot: 31 Aug 2016", "Live: 17 Oct 2017"],
  why="30 December 2016 is the BHIM launch; the other dates are not BBPS milestones.",
  facts=[fact("Pilot phase of BBPS was launched on August 31, 2016 and BBPS live operations commenced from October "
              "17, 2017", PAY_BOOKLET)])
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Advanced",
  "Consider the following statements:\nI. NACH, operated by NPCI, was formed to consolidate the multiple ECS systems "
  "into one centralised system.\nII. The last remaining ECS centres were migrated to NACH by 31 January 2020.\nIII. "
  "NACH Credit is used for one-to-many payments such as dividends, salaries and subsidies.\nWhich of the above "
  "is/are correct?",
  ["I, II and III", "I and II only", "I and III only", "II only"],
  concept="ECS to NACH",
  explanation="NACH is NPCI's centralised ECS system, formed to consolidate multiple ECS systems (I). The last ECS "
              "centres moved to NACH by 31 January 2020, ending ECS after about 25 years (II). NACH Credit, like "
              "ECS Credit, handles one-to-many credits such as dividend, interest, salary, pension and subsidies "
              "(III). All are correct.",
  steps=["I: correct", "II: correct", "III: correct"],
  why="Each other option leaves out a correct statement.",
  facts=[fact("NACH was formed to consolidate multiple ECS systems into one centralised system; last remaining ECS "
              "centres fully migrated to NACH by January 31, 2020; NACH credit used for one-to-many credit "
              "transfers such as dividend, interest, salary, pension, subsidies", PAY_BOOKLET)])
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Advanced",
  "Consider the following statements:\nI. The National Common Mobility Card (NCMC) was launched in March 2019 as a "
  "combination of a debit/credit card with a prepaid card for offline use.\nII. FASTag-based toll payments are "
  "facilitated through NPCI's NETC system.\nIII. FASTag uses the Aadhaar biometric of the vehicle owner at the toll "
  "plaza.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="NCMC and NETC",
  explanation="NCMC was launched in March 2019 as a combo card whose prepaid component works offline (I right). "
              "FASTag toll payments run on NETC, which NPCI is authorised to operate (II right). FASTag does not "
              "use Aadhaar biometrics (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong"],
  why="III is false, so options including it are wrong; 'I only' omits II.",
  facts=[fact("NCMC was launched in March 2019 as a combo card ... prepaid component used in the offline environment; "
              "FASTag based toll payments facilitated through NETC; NPCI is authorised to operate the NETC system",
              PAY_BOOKLET)])
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Advanced",
  "Consider the following statements:\nI. RuPay's first international foray was through acceptance and issuance in "
  "Bhutan, by integrating the Bhutan Financial Switch with NFS.\nII. The Clearing Corporation of India Ltd (CCIL) is "
  "a subsidiary of NPCI that settles UPI transactions.\nIII. NPCI took over the NFS ATM network from IDRBT in "
  "December 2009.\nWhich of the above is/are correct?",
  ["I and III only", "I only", "II and III only", "I, II and III"],
  concept="NPCI's network",
  explanation="RuPay's international foray began in Bhutan through integration of the Bhutan Financial Switch with "
              "NFS (I right). CCIL, set up in April 2001, provides guaranteed clearing and settlement in money, "
              "G-sec, forex and derivative markets; it is not an NPCI subsidiary (II wrong). NPCI took over NFS from "
              "IDRBT in December 2009 (III right).",
  steps=["I: correct", "II: wrong", "III: correct"],
  why="II is false, so options containing it are wrong; 'I only' omits III.",
  facts=[fact("RuPay started its international foray through acceptance and issue in Bhutan with the integration of "
              "the Bhutan Financial Switch with NFS; CCIL was set up in April 2001 for money, government securities, "
              "forex and derivative markets; NPCI took over NFS from IDRBT in December 2009", PAY_BOOKLET)])

# ================================================================= 23. Payment Banks (1 / 1 / 1)
T = "Payment Banks"
Q(T, "Permitted activities", "Basic",
  "Which type of deposit is a payments bank NOT allowed to accept?",
  ["Deposits from Non-Resident Indians (NRIs)", "Savings bank deposits from individuals",
   "Current deposits from small businesses", "Demand deposits from resident individuals"],
  concept="Deposits of payments banks",
  explanation="Payments banks accept demand deposits (current and savings) from individuals, small businesses and "
              "other entities as permitted, but no NRI deposits. Eligible deposits are insured by DICGC.",
  steps=["Demand deposits allowed", "NRI deposits not allowed"],
  why="Savings and current deposits from residents are exactly what payments banks are meant to accept.",
  facts=[fact("Acceptance of demand deposits, i.e., current deposits and savings bank deposits ... No NRI deposits "
              "should be accepted", PB_GUIDE)])
Q(T, "Permitted activities", "Intermediate",
  "Under RBI's Guidelines for Licensing of Payments Banks (November 2014), what minimum share of a payments bank's "
  "paid-up equity capital did its promoters have to hold, and for how long?",
  ["At least 40% for the first five years from commencement of business", "At least 51% at all times",
   "At least 26% for the first three years", "There is no minimum promoter holding"],
  concept="Ownership of payments banks",
  explanation="The 2014 licensing guidelines prescribed no maximum promoter holding because payments banks do not "
              "lend, but required promoters to hold at least 40% of the paid-up equity capital for the first five "
              "years from commencement of business.",
  steps=["Promoter minimum: 40% for 5 years"],
  why="51% and 26% are not the payments bank requirement; a minimum (not a maximum) is prescribed.",
  facts=[fact6("Payments bank licensing guidelines: promoters to hold at least 40 per cent of paid-up equity capital "
               "for the first five years from commencement of business", PB_GUIDE)])

nw = 150
max_ol = nw / 0.03
assert round(max_ol) == 5000
Q(T, "Deposit limit", "Advanced",
  "A payments bank has a net worth (paid-up capital and reserves) of ₹150 crore. Applying the leverage requirement "
  "in RBI's November 2014 licensing guidelines for payments banks, what is the maximum level of its outside "
  "liabilities?",
  ["₹5,000 crore", "₹1,000 crore", "₹4,500 crore", "₹2,250 crore"],
  concept="Leverage ratio for payments banks",
  explanation="Because payments banks have few risk-weighted assets, the 2014 licensing guidelines backed their 15% "
              "CRAR with a leverage ratio of at least 3%: outside liabilities could not exceed 33.33 times net worth. "
              "₹150 crore ÷ 3% = ₹5,000 crore.",
  steps=["Leverage ≥ 3% → liabilities ≤ net worth ÷ 0.03", "150 ÷ 0.03 = ₹5,000 crore"],
  shortcut="33.33 × 150 ≈ 5,000.",
  why="₹1,000 crore uses 15% (the CRAR); ₹4,500 crore uses 30 times; ₹2,250 crore uses 15 times.",
  computed=True,
  facts=[fact6("Payments bank licensing guidelines: leverage ratio of not less than 3 per cent, i.e., outside "
               "liabilities not to exceed 33.33 times net worth (paid-up capital and reserves)", PB_GUIDE)])

# ================================================================= 24. Small Finance Banks (1 / 2 / 1)
T = "Small Finance Banks"
Q(T, "Licensing norms", "Basic",
  "Within one year of commencing business, what minimum share of its banking outlets must a small finance bank open "
  "in unbanked rural centres?",
  ["25 per cent", "40 per cent", "50 per cent", "10 per cent"],
  concept="Branch norms for SFBs",
  explanation="An SFB has general permission to open banking outlets but must open at least 25% of them in unbanked "
              "rural centres (population up to 9,999 as per the latest census) within one year of commencement.",
  steps=["SFB: ≥ 25% outlets in unbanked rural centres"],
  why="40% and 50% relate to promoter holding and loan size norms; 10% is not the requirement.",
  facts=[fact("Required to open at least 25 per cent of its banking outlets in unbanked rural centres (population "
              "upto 9,999) within one year from the date of commencement", SFB_MD)])
Q(T, "Licensing norms", "Intermediate",
  "Which existing payments banks are eligible to apply for conversion into small finance banks?",
  ["Those controlled by residents that have completed five years of operations", "Any payments bank after one year",
   "Only payments banks owned by public sector banks", "Payments banks cannot convert into SFBs"],
  concept="Conversion into SFBs",
  explanation="Under the SFB Licensing Guidelines, 2025, existing payments banks controlled by residents and with "
              "five years of operations can convert into SFBs, subject to legal and regulatory requirements.",
  steps=["Resident-controlled PB + 5 years of operations → may convert"],
  why="One year is too short; ownership by public sector banks is not a condition; conversion is permitted.",
  facts=[fact("Existing Payments Banks which are controlled by residents and have completed five years of operations "
              "are also eligible for conversion into small finance banks", SFB_MD)])
Q(T, "Licensing norms", "Intermediate",
  "What minimum net worth must an Urban Co-operative Bank have to be eligible to apply for voluntary transition into a "
  "small finance bank?",
  ["₹50 crore", "₹300 crore", "₹150 crore", "₹100 crore"],
  concept="UCB to SFB transition",
  explanation="UCBs with a minimum net worth of ₹50 crore and meeting the CRAR requirement can apply. The resulting "
              "SFB needs a net worth of ₹150 crore at commencement, to be raised to ₹300 crore within five years.",
  steps=["Eligibility to apply: UCB net worth ≥ ₹50 crore"],
  why="₹150 crore and ₹300 crore are the net worth requirements for the SFB after transition.",
  facts=[fact("UCBs with a minimum net worth of ₹50 crore and maintaining minimal CRAR are eligible to apply for "
              "voluntary transition to SFB", SFB_MD)])
Q(T, "Licensing norms", "Advanced",
  "Consider the following statements about a small finance bank formed by transition of an Urban Co-operative "
  "Bank:\nI. It must have a minimum net worth of ₹150 crore from commencement and ₹300 crore within five years.\nII. "
  "Its promoters must hold at least 26% of the paid-up voting equity at all times during the first five years.\nIII. "
  "It may continue to maintain CRAR at the UCB level instead of the 15% applicable to SFBs.\nWhich of the above "
  "is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Norms for UCB-converted SFBs",
  explanation="A transitioned SFB needs ₹150 crore net worth from commencement, rising to ₹300 crore within five years "
              "(I right). Its promoters must hold at least 26% during the first five years (II right). On "
              "transition it is subject to all SFB norms, including CRAR of 15% on a continuous basis (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong"],
  why="III is false, so options including it are wrong; 'I only' omits II.",
  facts=[fact("Transitioned from a UCB: minimum net worth ₹150 crore from commencement, increased to ₹300 crore within "
              "five years; promoters minimum 26 per cent during the first five years; subjected to all SFB norms "
              "including CRAR of 15% on a continuous basis", SFB_MD)])

# ================================================================= 25. Financial Markets (2 / 3 / 2)
T = "Financial Markets"
Q(T, "Structure and regulators", "Basic",
  "Since the merger of the Forward Markets Commission in September 2015, which body regulates commodity derivatives "
  "markets in India?",
  ["SEBI", "RBI", "Ministry of Consumer Affairs", "PFRDA"],
  concept="Regulation of commodity derivatives",
  explanation="The Forward Markets Commission was merged with SEBI on 28 September 2015, bringing commodity "
              "derivatives under SEBI and converging the regulation of commodity and securities derivatives.",
  steps=["FMC merged into SEBI: 28 Sep 2015"],
  why="RBI regulates money, G-sec and forex markets; the Consumer Affairs ministry earlier oversaw the FMC; PFRDA "
      "regulates pensions.",
  facts=[fact("Finance Minister formalizes merger of Forward Markets Commission (FMC) with SEBI, 28-September-2015",
              FMC_PIB)])
Q(T, "Structure and regulators", "Basic",
  "The Clearing Corporation of India Ltd (CCIL), which provides guaranteed clearing and settlement for money market, "
  "government securities, forex and derivative trades, was set up in:",
  ["April 2001", "March 2004", "December 2009", "June 1992"],
  concept="Market infrastructure",
  explanation="CCIL was set up in April 2001 to provide guaranteed clearing and settlement for transactions in money, "
              "government securities, foreign exchange and derivative markets.",
  steps=["CCIL: April 2001"],
  why="March 2004 is the start of RTGS; December 2009 the NFS takeover by NPCI; 1992 relates to SEBI's statutory "
      "status.",
  facts=[fact("CCIL was setup in April 2001 to provide guaranteed clearing and settlement for transactions in money, "
              "government securities, forex and derivative markets", PAY_BOOKLET)])
Q(T, "Structure and regulators", "Intermediate",
  "Inflation Indexed Bonds (IIBs) linked to the Wholesale Price Index were issued by the Government of India through "
  "RBI in:",
  ["June 2013", "September 1995", "July 2002", "January 2018"],
  concept="Types of government securities",
  explanation="In India, Inflation Indexed Bonds linked to WPI were issued in June 2013; both coupons and principal "
              "are protected against inflation. Floating rate bonds were first issued in September 1995.",
  steps=["WPI-linked IIBs: June 2013"],
  why="September 1995 is the first FRB; July 2002 the first G-sec with call and put options; January 2018 the 7.75% "
      "Savings Bonds.",
  facts=[fact("Government of India through RBI issued IIBs (linked to WPI) in June 2013; FRBs first issued in "
              "September 1995; first G-Sec with call and put option issued July 18, 2002", GSEC_FAQ)])
Q(T, "Structure and regulators", "Intermediate",
  "Legal Entity Identifier India Ltd (LEIL), the Local Operating Unit issuing globally compatible LEIs in India, was "
  "set up in:",
  ["2015", "2001", "2009", "2020"],
  concept="Legal Entity Identifier",
  explanation="LEIL was set up in 2015 as a Local Operating Unit for issuing globally compatible LEIs in the Indian "
              "financial market. LEIs are now required for large-value RTGS and NEFT transactions by eligible "
              "entities.",
  steps=["LEIL: 2015"],
  why="2001 is CCIL's set-up; 2009 NPCI's NFS takeover; 2020 is not LEIL's set-up year.",
  facts=[fact("Legal Entity Identifier India Limited (LEIL) was set up in 2015 as a Local Operating Unit (LOU) for "
              "issuing globally compatible LEI in the Indian financial market", PAY_BOOKLET)])
Q(T, "Structure and regulators", "Intermediate",
  "Floating Rate Bonds issued by the Government of India, such as FRB 2031, have a coupon equal to a base rate plus "
  "a fixed spread. What is that base rate?",
  ["The weighted average yield of the last three auctions of 182-day T-bills",
   "The policy repo rate on the date of issue", "CPI inflation for the previous year",
   "The yield on 10-year G-secs on the date of reset"],
  concept="Floating Rate Bonds",
  explanation="RBI gives the example of FRB 2031, whose coupon is the weighted average yield of the last three "
              "auctions of 182-day T-bills (from the rate-fixing day) plus a fixed spread decided in the auction. "
              "The spread stays fixed for the bond's life.",
  steps=["Base = WAY of last 3 auctions of 182-day T-bills", "Coupon = base + fixed spread"],
  why="FRB coupons are not linked to the repo rate, CPI or 10-year yields.",
  facts=[fact("FRB 2031 carry the coupon with base rate equivalent to Weighted Average Yield of last 3 auctions of "
              "182 Day T-Bills plus a fixed spread decided by way of auction", GSEC_FAQ)])
Q(T, "Structure and regulators", "Advanced",
  "Consider the following statements:\nI. The merger of the Forward Markets Commission with SEBI was meant to bring "
  "convergence of regulation of the commodity and equity derivatives markets.\nII. CCIL provides guaranteed clearing "
  "and settlement in the money, G-sec, forex and derivative markets.\nIII. Commodity derivatives continue to be "
  "regulated by RBI jointly with SEBI.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Market regulators and infrastructure",
  explanation="With the FMC–SEBI merger of 28 September 2015, regulation of commodity derivatives came under SEBI, "
              "with the stated aim of converging the regulation of commodity and equity derivatives markets (I "
              "right, III wrong). CCIL is the guaranteed clearing house for money, G-sec, forex and derivative "
              "markets (II right).",
  steps=["I: correct", "II: correct", "III: wrong (SEBI alone)"],
  why="III is false, so options including it are wrong; 'I only' omits II.",
  facts=[fact("Regulation of commodities derivatives came under SEBI's jurisdiction as the FMC formally merged with "
              "SEBI on 28 September 2015; the amalgamation would bring convergence of regulations in the commodities "
              "and equity derivatives markets", FMC_PIB),
         fact("CCIL provides guaranteed clearing and settlement for money, government securities, forex and "
              "derivative markets", PAY_BOOKLET)])
Q(T, "Structure and regulators", "Advanced",
  "Consider the following statements about government securities:\nI. Cash Management Bills are issued for "
  "maturities of less than 91 days to meet temporary mismatches in the Government's cash flow.\nII. Dated G-secs "
  "pay coupons on a half-yearly basis.\nIII. STRIPS are created by separating the coupon and principal cash flows of "
  "an existing G-sec, so each STRIP is a zero coupon instrument.\nWhich of the above is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I only"],
  concept="G-sec instruments",
  explanation="CMBs, introduced in 2010, have maturities of less than 91 days (I). Dated G-secs pay coupons "
              "half-yearly on face value (II). STRIPS separate each coupon and the principal of an existing "
              "security into zero coupon securities (III). All three are correct.",
  steps=["I: correct", "II: correct", "III: correct"],
  why="Each other option leaves out a correct statement.",
  facts=[fact("CMBs issued for maturities less than 91 days; dated G-Secs carry coupon paid on half-yearly basis; "
              "STRIPS created by separating cash flows of an existing G-Sec, essentially Zero Coupon Bonds",
              GSEC_FAQ)])

# ================================================================= 26. Money Market (1 / 2 / 0)
T = "Money Market"
Q(T, "Instruments: T-bills, CP, CD, call money", "Basic",
  "In which tenors does the Government of India presently issue Treasury Bills?",
  ["91 days, 182 days and 364 days", "14 days, 91 days and 182 days", "30 days, 90 days and 180 days",
   "91 days and 364 days only"],
  concept="T-bill tenors",
  explanation="T-bills are short-term zero coupon instruments presently issued in three tenors: 91 days, 182 days "
              "and 364 days.",
  steps=["T-bills: 91, 182, 364 days"],
  why="14-day and 30/90/180-day T-bills are not issued at present; the 182-day bill is also issued.",
  facts=[fact("Treasury bills are presently issued in three tenors, namely, 91 day, 182 day and 364 day", GSEC_FAQ)])
Q(T, "Instruments: T-bills, CP, CD, call money", "Intermediate",
  "Cash Management Bills (CMBs), introduced in 2010 by the Government in consultation with RBI, have the generic "
  "character of T-bills but are issued for maturities of:",
  ["Less than 91 days", "Exactly one year", "91 to 364 days", "More than one year"],
  concept="Cash Management Bills",
  explanation="CMBs meet temporary mismatches in the Government's cash flow. They are issued at a discount and "
              "redeemed at face value, like T-bills, but for maturities of less than 91 days.",
  steps=["CMB maturity: < 91 days"],
  why="91–364 days is the T-bill range; one year or more would make them dated securities.",
  facts=[fact("CMBs introduced in 2010 ... have the generic character of T-bills but are issued for maturities less "
              "than 91 days", GSEC_FAQ)])
Q(T, "Instruments: T-bills, CP, CD, call money", "Intermediate",
  "On which day does RBI usually conduct auctions of 91-day, 182-day and 364-day Treasury Bills, and when are they "
  "settled?",
  ["Every Wednesday; settlement on T+1", "Every Monday; settlement on T+2", "Every Friday; same-day settlement",
   "Last working day of the month; settlement on T+3"],
  concept="T-bill auctions",
  explanation="RBI usually conducts T-bill auctions every Wednesday, with settlement on T+1 (the next working day). "
              "A quarterly calendar is released in the last week of the preceding quarter.",
  steps=["Auction: Wednesday", "Settlement: T+1"],
  why="The other days and settlement cycles do not match RBI's auction practice.",
  facts=[fact("RBI conducts auctions usually every Wednesday to issue T-bills of 91, 182 and 364 day tenors; "
              "settlement on T+1 day", GSEC_FAQ)])

# ================================================================= 27. Capital Market (4 / 2 / 2)
T = "Capital Market"
Q(T, "Indices", "Basic",
  "The BSE SENSEX, which tracks 30 large companies listed on BSE, was launched on:",
  ["2 January 1986", "3 November 1995", "1 April 1979", "12 April 1988"],
  concept="SENSEX",
  explanation="BSE says the SENSEX, its bellwether index of 30 large, liquid companies, was launched on 2 January "
              "1986.",
  steps=["SENSEX launched: 2 January 1986"],
  why="3 November 1995 is the Nifty 50 base date; 12 April 1988 the non-statutory SEBI's constitution; 1 April "
      "1979 is not the launch date.",
  facts=[fact("The BSE SENSEX ... designed to measure the performance of the 30 largest companies listed at BSE; "
              "it was launched on 2nd January 1986", SENSEX)])
Q(T, "Primary and secondary market", "Basic",
  "In a book-built public issue, the offer document that contains all relevant details except the price and the "
  "number of shares offered is called the:",
  ["Red herring prospectus", "Abridged prospectus", "Letter of offer", "Shelf prospectus"],
  concept="Offer documents",
  explanation="A red herring prospectus is used in book-built issues; it has all details except price or number of "
              "shares, and is filed with the RoC before the issue opens. The final prospectus is registered after "
              "the issue closes.",
  steps=["Book-built issue without price → red herring prospectus"],
  why="A letter of offer is used for rights issues; abridged and shelf prospectuses are different documents.",
  facts=[fact("Red herring prospectus is an offer document used in case of a book built public issue; it contains "
              "all the relevant details except that of price or number of shares being offered", ICDR_FAQ)])
Q(T, "Primary and secondary market", "Basic",
  "In a book-built issue, the option to bid at the 'cut-off' price instead of a specific price is available to:",
  ["Only retail individual investors applying for up to ₹2 lakh", "Only qualified institutional buyers",
   "All investors", "Only anchor investors"],
  concept="Cut-off bidding",
  explanation="The cut-off option is available only to retail individual investors applying for securities worth up "
              "to ₹2,00,000. Cut-off bids always remain valid for allotment at the discovered price.",
  steps=["Cut-off bids: retail individual investors (≤ ₹2 lakh) only"],
  why="QIBs, non-institutional and anchor investors must bid at a specific price.",
  facts=[fact("'Cut-off' option is available for only retail individual investors i.e. investors applying for "
              "securities worth up to Rs 2,00,000", ICDR_FAQ)])
Q(T, "Primary and secondary market", "Basic",
  "In an IPO by an unlisted company, what is the minimum promoters' contribution required under SEBI's ICDR "
  "framework?",
  ["20% of the post-issue capital", "10% of the issue size", "51% of the post-issue capital", "35% of the net offer"],
  concept="Promoters' contribution",
  explanation="In a public issue by an unlisted issuer, promoters must contribute not less than 20% of the post-issue "
              "capital, locked in for 18 months (three years if most proceeds go to capital expenditure).",
  steps=["Minimum promoters' contribution: 20% of post-issue capital"],
  why="35% is the minimum retail allocation; 10% and 51% are not the ICDR requirement.",
  facts=[fact("In a public issue by an unlisted issuer, the promoters shall contribute not less than 20% of the post "
              "issue capital which should be locked in for a period of 1.5 years", ICDR_FAQ)])
Q(T, "Primary and secondary market", "Intermediate",
  "In an IPO made entirely through the book-building process under the profitability route, how is the net offer to "
  "the public allocated among investor categories?",
  ["Retail at least 35%, non-institutional at least 15%, QIBs not more than 50%",
   "Retail at least 50%, non-institutional at least 15%, QIBs not more than 35%",
   "QIBs at least 75%, the rest to others", "Equal one-third shares for each category"],
  concept="Allocation in book-built issues",
  explanation="Under the profitability route with 100% book building: not less than 35% to retail individual "
              "investors, not less than 15% to non-institutional investors, and not more than 50% to QIBs. (Where "
              "book building is compulsory, at least 75% goes to QIBs.)",
  steps=["RII ≥ 35%", "NII ≥ 15%", "QIB ≤ 50%"],
  why="The retail and QIB shares are swapped in the second option; 75% QIB applies to compulsory book building.",
  facts=[fact("Profitability route book building: not less than 35% to retail individual investors; not less than "
              "15% to non-institutional investors; not more than 50% to QIBs; compulsory book built issues at least "
              "75% to QIBs", ICDR_FAQ)])
Q(T, "SEBI", "Intermediate",
  "SEBI introduced a beta version of an optional T+0 rolling settlement cycle in the equity cash market. When did it "
  "go live, and for how many scrips initially?",
  ["28 March 2024, for 25 scrips", "27 January 2023, for all scrips", "1 April 2025, for the top 500 scrips",
   "28 March 2024, for the Nifty 50 scrips only"],
  concept="T+0 settlement",
  explanation="SEBI's circular of 21 March 2024 introduced an optional T+0 settlement cycle alongside T+1, in a beta "
              "version for 25 scrips and a limited number of brokers, which went live on 28 March 2024. Its scope "
              "was later widened in phases towards the top 500 scrips.",
  steps=["Beta T+0 live: 28 March 2024", "Initial scope: 25 scrips"],
  why="27 January 2023 is the full move to T+1; the top-500 expansion came later; the initial list was 25 scrips, "
      "not the Nifty 50.",
  current=ca("2024-03-28"),
  facts=[fact("Beta version of optional T+0 settlement for a limited set of 25 scrips and limited number of brokers "
              "went live on March 28, 2024", T0_SEBI)])

net_offer = 1200
alloc = (0.35 * net_offer, 0.15 * net_offer, 0.50 * net_offer)
assert alloc == (420, 180, 600)
Q(T, "Primary and secondary market", "Advanced",
  "A company makes an IPO entirely through book building under the profitability route, with a net offer to the "
  "public of ₹1,200 crore. What are the minimum retail, minimum non-institutional and maximum QIB portions?",
  ["₹420 crore, ₹180 crore and ₹600 crore", "₹600 crore, ₹180 crore and ₹420 crore",
   "₹420 crore, ₹180 crore and ₹900 crore", "₹360 crore, ₹240 crore and ₹600 crore"],
  concept="Applying IPO allocation norms",
  explanation="Retail ≥ 35% × 1,200 = ₹420 crore; non-institutional ≥ 15% × 1,200 = ₹180 crore; QIB ≤ 50% × 1,200 "
              "= ₹600 crore.",
  steps=["35% × 1,200 = 420", "15% × 1,200 = 180", "50% × 1,200 = 600"],
  why="The second option swaps retail and QIB; ₹900 crore uses 75% for QIBs; ₹360/₹240 crore use 30%/20%.",
  computed=True,
  facts=[fact("Not less than 35% to retail individual investors; not less than 15% to non-institutional investors; "
              "not more than 50% to QIBs", ICDR_FAQ)])
Q(T, "Primary and secondary market", "Advanced",
  "Consider the following statements about public issues:\nI. In an IPO, the floor price or price band must be "
  "announced at least two working days before the issue opens.\nII. In a book-built issue, the final prospectus is "
  "registered with the RoC after the issue closes.\nIII. A cut-off bid by a retail investor becomes invalid if the "
  "discovered price is above the lower end of the price band.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Book-building process",
  explanation="For an IPO, the floor price or price band is announced at least two working days before opening (I "
              "right). In a book-built issue, the prospectus is registered with the RoC after the issue closes (II "
              "right). Cut-off bids always remain valid at the discovered price (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong"],
  why="III is false, so options including it are wrong; 'I only' omits II.",
  facts=[fact("Floor price or price band announced at least two working days before the opening of the issue for an "
              "IPO; prospectus registered with RoC after closure of the issue in a book built issue; cut-off bids "
              "always remain valid", ICDR_FAQ)])

# ================================================================= 28. Insurance (2 / 1 / 2)
T = "Insurance"
Q(T, "IRDAI", "Basic",
  "The Sabka Bima Sabki Raksha (Amendment of Insurance Laws) Bill, 2025, passed by Parliament on 17 December 2025, "
  "amends the Insurance Act, 1938, the IRDA Act, 1999 and which other Act?",
  ["Life Insurance Corporation Act, 1956", "General Insurance Business (Nationalisation) Act, 1972",
   "Banking Regulation Act, 1949", "Employees' State Insurance Act, 1948"],
  concept="Insurance law amendments, 2025",
  explanation="The Bill amends three Acts: the Insurance Act, 1938, the Life Insurance Corporation Act, 1956 and the "
              "Insurance Regulatory and Development Authority Act, 1999.",
  steps=["Acts amended: Insurance Act 1938, LIC Act 1956, IRDA Act 1999"],
  why="The GIBNA, BR Act and ESI Act are not among the three Acts amended.",
  current=ca("2025-12-17"),
  facts=[fact("The bill amends three Acts: The Insurance Act, 1938, The Life Insurance Corporation Act, 1956 and The "
              "IRDA Act, 1999; passed by Parliament on 17.12.2025", INS_PIB)])
Q(T, "IRDAI", "Basic",
  "Which new fund will be set up under the Sabka Bima Sabki Raksha amendments to spread insurance awareness among "
  "policyholders?",
  ["Policyholders' Education and Protection Fund", "Depositor Education and Awareness Fund",
   "Investor Education and Protection Fund", "Insurance Development Fund"],
  concept="Policyholder protection",
  explanation="The 2025 amendments provide for a dedicated Policyholders' Education and Protection Fund to spread "
              "awareness about insurance, and require policyholders' data to be handled in line with the DPDP "
              "Act, 2023.",
  steps=["New fund: Policyholders' Education and Protection Fund"],
  why="The DEA Fund is RBI's (bank deposits); IEPF is under company law; 'Insurance Development Fund' is not the name "
      "used.",
  current=ca("2025-12-17"),
  facts=[fact("A dedicated fund, namely Policyholders' Education and Protection Fund will be set up to spread "
              "awareness about insurance", INS_PIB)])
Q(T, "Life and general insurance", "Intermediate",
  "Under the Sabka Bima Sabki Raksha amendments, the Net Owned Fund requirement for branches of foreign reinsurers "
  "was reduced from ₹5,000 crore to:",
  ["₹1,000 crore", "₹2,500 crore", "₹500 crore", "₹100 crore"],
  concept="Reinsurance branches",
  explanation="To promote ease of doing business, the NOF requirement for foreign reinsurance branches was cut from "
              "₹5,000 crore to ₹1,000 crore. The same Bill allows up to 100% FDI in insurance companies.",
  steps=["Foreign reinsurer branch NOF: ₹5,000 crore → ₹1,000 crore"],
  why="₹2,500 crore, ₹500 crore and ₹100 crore are not the new requirement.",
  current=ca("2025-12-17"),
  facts=[fact("The Net Owned Fund requirement of Foreign Reinsurance Branches has been reduced from Rs 5,000 Crore to "
              "Rs 1,000 Crore", INS_PIB)])
Q(T, "IRDAI", "Advanced",
  "Consider the following statements about the Sabka Bima Sabki Raksha (Amendment of Insurance Laws) Bill, 2025:\nI. "
  "The threshold for seeking prior regulatory approval for transfer of an insurer's share capital was raised from 1% "
  "to 5%.\nII. IRDAI is given the power to disgorge wrongful gains from insurers and intermediaries.\nIII. "
  "Intermediaries' licences, once granted, can only be cancelled, not suspended.\nWhich of the above is/are "
  "correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Regulatory changes in insurance, 2025",
  explanation="The prior-approval limit for share transfers rose from 1% to 5% (I right). IRDAI gets power to "
              "disgorge wrongful gains (II right). The Bill introduces one-time licensing for intermediaries and "
              "provides for suspension of a licence rather than straight away cancellation (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong"],
  why="III reverses the change, so options including it are wrong; 'I only' omits II.",
  current=ca("2025-12-17"),
  facts=[fact("Prior regulatory approval limit for transfer of share capital raised from 1% to 5%; IRDAI given the "
              "power to disgorge wrongful gains; one-time licensing and suspension of license rather than straight "
              "away cancellation", INS_PIB)])
Q(T, "Government insurance schemes", "Advanced",
  "Under the expansion of Ayushman Bharat PM-JAY approved in 2024 for senior citizens aged 70 years and above, "
  "irrespective of income, which statement is correct?",
  ["Seniors in families already covered by AB PM-JAY get an additional top-up of up to ₹5 lakh a year for "
   "themselves; other seniors get up to ₹5 lakh a year on a family basis",
   "Every senior citizen gets ₹10 lakh a year as an individual cover",
   "Only seniors from families below the poverty line are covered",
   "Seniors covered under CGHS are automatically excluded and cannot opt for AB PM-JAY"],
  concept="AB PM-JAY for senior citizens",
  explanation="All senior citizens aged 70 and above, irrespective of income, are covered. Those in families "
              "already under AB PM-JAY get an additional top-up of up to ₹5 lakh a year for themselves; other "
              "seniors get up to ₹5 lakh a year on a family basis. Seniors under CGHS, ECHS or CAPF schemes may "
              "choose their existing scheme or opt for AB PM-JAY.",
  steps=["Coverage: all aged 70+, irrespective of income", "Existing PM-JAY families: extra ₹5 lakh top-up",
         "Others: ₹5 lakh family cover"],
  why="The cover is ₹5 lakh, not ₹10 lakh; it is not income-tested; CGHS beneficiaries may opt for PM-JAY.",
  current=ca("2024-10-29"),
  facts=[fact("Health coverage to all senior citizens of the age 70 years and above irrespective of income; additional "
              "top-up cover upto ₹5 lakh per year for those in families already covered; others up to ₹5 lakh per "
              "year on a family basis; CGHS/ECHS/CAPF beneficiaries may choose", PMJAY70)])

# ================================================================= 29. Mutual Funds (1 / 3 / 3)
T = "Mutual Funds"
Q(T, "Types", "Basic",
  "India's first mutual fund, set up in 1963 at the initiative of the Government of India and RBI, was:",
  ["Unit Trust of India (UTI)", "SBI Mutual Fund", "LIC Mutual Fund", "Kothari Pioneer Mutual Fund"],
  concept="History of mutual funds",
  explanation="The Unit Trust of India was established in 1963 by an Act of Parliament, at the initiative of the "
              "Government and RBI. Its first scheme was Unit Scheme 1964 (US-64).",
  steps=["First MF: UTI (1963)"],
  why="SBI MF (1987) was the first non-UTI fund; LIC MF came in the public sector phase; Kothari Pioneer (1993) was "
      "the first private sector fund.",
  facts=[fact("India's first mutual fund was established in 1963, namely Unit Trust of India (UTI), at the "
              "initiative of the Government of India and Reserve Bank of India", AMFI_HIST)])
Q(T, "Types", "Intermediate",
  "Which was the first 'non-UTI' mutual fund in India, set up in June 1987 when public sector mutual funds were "
  "allowed?",
  ["SBI Mutual Fund", "Canbank Mutual Fund", "Kothari Pioneer Mutual Fund", "Punjab National Bank Mutual Fund"],
  concept="Second phase of mutual funds",
  explanation="1987 saw the entry of public sector mutual funds. SBI Mutual Fund (June 1987) was the first non-UTI "
              "fund, followed by Canbank MF (December 1987) and PNB MF (August 1989).",
  steps=["First non-UTI MF: SBI MF, June 1987"],
  why="Canbank and PNB MFs came later; Kothari Pioneer was the first private sector MF (1993).",
  facts=[fact("SBI Mutual Fund was the first 'non-UTI' mutual fund established in June 1987, followed by Canbank "
              "Mutual Fund (Dec. 1987), Punjab National Bank Mutual Fund (Aug. 1989)", AMFI_HIST)])
Q(T, "Types", "Intermediate",
  "SEBI's Specialized Investment Fund (SIF) framework requires a minimum investment, across all strategies of a SIF, "
  "of:",
  ["₹10 lakh, calculated at the PAN level (accredited investors exempt)", "₹50 lakh per strategy",
   "₹1 crore per investor", "₹5,000, like a regular mutual fund scheme"],
  concept="Specialized Investment Funds",
  explanation="A SIF cannot accept an investment below ₹10 lakh, aggregated at the PAN level across all its "
              "strategies. Holdings in regular mutual fund schemes do not count, and accredited investors are "
              "exempt from the threshold.",
  steps=["SIF minimum: ₹10 lakh at PAN level", "Accredited investors exempt"],
  why="₹50 lakh and ₹1 crore are PMS/AIF-type thresholds; SIF is not a retail ₹5,000 product.",
  current=ca("2026-09-01"),
  facts=[fact("An investor must maintain an aggregate investment value of at least 10 lakhs, calculated at the PAN "
              "level across all investment strategies offered by a particular SIF; an accredited investor is "
              "exempted", SIF_FAQ)])
Q(T, "AMFI", "Intermediate",
  "When did the first set of SEBI Mutual Fund Regulations come into being, applying to all mutual funds except UTI?",
  ["1993", "1987", "1996", "2003"],
  concept="Regulation of mutual funds",
  explanation="In 1993 the first SEBI Mutual Fund Regulations came into being for all mutual funds except UTI, and "
              "private sector funds entered (Kothari Pioneer was the first, in July 1993). The regulations were "
              "fully revised in 1996.",
  steps=["First SEBI MF Regulations: 1993 (except UTI)"],
  why="1987 marks public sector funds; 1996 the revised regulations; 2003 the bifurcation of UTI.",
  facts=[fact("In the year 1993, the first set of SEBI Mutual Fund Regulations came into being for all mutual funds, "
              "except UTI; Kothari Pioneer was the first private sector MF registered in July 1993", AMFI_HIST)])
Q(T, "Types", "Advanced",
  "Consider the following statements about the history of UTI:\nI. UTI was de-linked from RBI in 1978, when IDBI "
  "took over its regulatory and administrative control.\nII. After the repeal of the UTI Act in February 2003, UTI "
  "was bifurcated into the Specified Undertaking of UTI (SUUTI) and UTI Mutual Fund.\nIII. UTI's first scheme was "
  "Unit Scheme 1964 (US-64).\nWhich of the above is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I only"],
  concept="UTI's evolution",
  explanation="UTI functioned under RBI until 1978, when IDBI took over (I). In February 2003, after the repeal of "
              "the UTI Act, 1963, it was split into SUUTI and UTI Mutual Fund, which works under SEBI's regulations "
              "(II). Its first scheme was US-64 (III). All three are correct.",
  steps=["I: correct", "II: correct", "III: correct"],
  why="Each other option leaves out a correct statement.",
  facts=[fact("In 1978, UTI was de-linked from RBI and IDBI took over the regulatory and administrative control; Unit "
              "Scheme 1964 (US '64) was the first scheme; in February 2003 UTI was bifurcated into SUUTI and UTI "
              "Mutual Fund", AMFI_HIST)])

holding = 11.0
active_ok = holding - 2.0 >= 10
assert not active_ok
Q(T, "NAV and SIP", "Advanced",
  "Ravi (not an accredited investor) holds ₹11 lakh in the strategies of one Specialized Investment Fund. Under "
  "SEBI's SIF FAQs, which statement is correct?",
  ["A redemption request of ₹2 lakh may be rejected because it would take him below ₹10 lakh; if only a fall in NAV "
   "takes him below ₹10 lakh, he can stay invested but can then redeem only the entire remaining amount",
   "He can redeem ₹2 lakh freely, since the ₹10 lakh test applies only at the time of first investment",
   "If NAV falls and his holding drops to ₹9.5 lakh, the SIF must compulsorily redeem his units",
   "He can top up through his regular mutual fund holdings to stay above ₹10 lakh"],
  concept="Active and passive breach",
  explanation="An investor-initiated redemption that would take the PAN-level holding below ₹10 lakh is an active "
              "breach and may be rejected (₹11 lakh − ₹2 lakh = ₹9 lakh). A fall due only to NAV movement is a "
              "passive breach and does not force an exit, but while the value stays below ₹10 lakh the investor "
              "may redeem only the entire remaining investment. Regular MF holdings do not count.",
  steps=["11 − 2 = 9 < 10 → active breach → may be rejected", "NAV fall → passive breach → no forced exit",
         "Below ₹10 lakh after passive breach → only full redemption"],
  why="The threshold applies on an ongoing basis; passive breaches do not trigger compulsory redemption; regular "
      "scheme holdings are excluded from the test.",
  computed=True, current=ca("2026-09-01"),
  facts=[fact("Redemption that causes aggregate value to fall below 10 lakhs may be rejected to prevent an active "
              "breach; a fall solely due to decline in NAV is a passive breach; while below 10 lakhs the investor may "
              "redeem only the entire remaining investment; investments in regular schemes not included", SIF_FAQ)])
Q(T, "AMFI", "Advanced",
  "Under SEBI's SIF FAQs, how are the eligibility and the ₹10 lakh minimum threshold assessed for a joint folio, and "
  "can several transactions on one day be combined to meet it?",
  ["With reference to the first holder's PAN; multiple same-day transactions under that PAN can be aggregated",
   "With reference to the PAN of every joint holder, each needing ₹10 lakh; transactions cannot be combined",
   "With reference to the youngest holder's PAN; transactions can be combined only across different days",
   "Joint folios are not permitted in SIFs"],
  concept="SIF threshold for joint holdings",
  explanation="For a joint folio, eligibility and the minimum threshold are assessed with reference to the PAN of "
              "the first holder (principal investor). Multiple transactions under the same PAN on the same day may "
              "be aggregated to meet the ₹10 lakh threshold, if they are credited as required.",
  steps=["Joint folio → first holder's PAN", "Same-day transactions under the same PAN can be aggregated"],
  why="Each joint holder does not need ₹10 lakh; the youngest holder is irrelevant; joint folios are allowed.",
  current=ca("2026-09-01"),
  facts=[fact("For a joint folio, eligibility and the minimum investment threshold are assessed with reference to the "
              "PAN of the first holder; multiple transactions under the same PAN may be aggregated to meet the "
              "threshold", SIF_FAQ)])

# ================================================================= 30. Budget and Economic Survey (2 / 4 / 3)
T = "Budget and Economic Survey"
Q(T, "Union Budget highlights", "Basic",
  "The Union Budget 2026-27, the first prepared in Kartavya Bhawan, was built around how many 'kartavyas'?",
  ["Three", "Four", "Five", "Seven"],
  concept="Theme of Budget 2026-27",
  explanation="The Finance Minister said the Budget was inspired by three kartavyas: to accelerate and sustain "
              "economic growth; to fulfil aspirations of people and build their capacity; and, in line with Sabka "
              "Sath, Sabka Vikas, to ensure that every family has access to resources and opportunities.",
  steps=["Three kartavyas"],
  why="Four, five and seven do not match the Budget speech.",
  current=BUDGET,
  facts=[fact("First Budget prepared in Kartavya Bhawan inspired by 3 kartavya: accelerate and sustain economic "
              "growth; fulfil aspirations of people; Sabka Sath, Sabka Vikas", PIB_BUDGET)])
Q(T, "Fiscal terms", "Basic",
  "What fiscal deficit did the Union Budget 2026-27 estimate for 2026-27 (BE), as a percentage of GDP?",
  ["4.3 per cent", "4.4 per cent", "4.8 per cent", "3.1 per cent"],
  concept="Fiscal deficit target",
  explanation="The fiscal deficit in BE 2026-27 is estimated at 4.3% of GDP. The RE for 2025-26 is 4.4%, the same as "
              "BE 2025-26.",
  steps=["BE 2026-27: 4.3% of GDP"],
  why="4.4% is RE 2025-26; 4.8% was FY25's deficit; 3.1% is central capex as a share of GDP.",
  current=BUDGET,
  facts=[fact("The fiscal deficit in BE 2026-27 is estimated to be 4.3 percent of GDP; RE 2025-26 at 4.4 percent",
              PIB_BUDGET)])
Q(T, "Union Budget highlights", "Intermediate",
  "Which committee did the Union Budget 2026-27 propose to set up to comprehensively review the banking sector and "
  "align it with India's next phase of growth?",
  ["High Level Committee on Banking for Viksit Bharat", "Committee on Financial Sector Reforms 2047",
   "Banking Regulation Review Commission", "Committee on Public Sector Bank Consolidation"],
  concept="Banking announcements in Budget 2026-27",
  explanation="The Budget proposed a 'High Level Committee on Banking for Viksit Bharat' to review the sector "
              "comprehensively while safeguarding financial stability, inclusion and consumer protection. It also "
              "proposed restructuring PFC and REC.",
  steps=["High Level Committee on Banking for Viksit Bharat"],
  why="The other names were not announced in the Budget.",
  current=BUDGET,
  facts=[fact("Government to setup a 'High Level Committee on Banking for Viksit Bharat', to comprehensively review "
              "the sector", PIB_BUDGET)])
Q(T, "Union Budget highlights", "Intermediate",
  "The Union Budget 2026-27 proposed to raise the investment limit for an individual person resident outside India "
  "(PROI) in a listed Indian company under the Portfolio Investment Scheme from 5% to:",
  ["10%, with the overall limit for all individual PROIs raised from 10% to 24%",
   "24%, with the overall limit raised to 49%", "10%, with the overall limit unchanged at 10%",
   "15%, with the overall limit raised to 74%"],
  concept="PROI investment limits",
  explanation="The Budget proposed raising the limit for an individual PROI from 5% to 10%, and the overall limit "
              "for all individual PROIs from 10% to 24%, under the Portfolio Investment Scheme.",
  steps=["Individual PROI: 5% → 10%", "All individual PROIs: 10% → 24%"],
  why="The individual limit becomes 10%, not 24% or 15%, and the overall limit is raised to 24%.",
  current=BUDGET,
  facts=[fact("Increase the investment limit for an individual PROI from 5% to 10%, with an overall investment limit "
              "for all individual PROIs to 24%, from the current 10%", PIB_BUDGET)])
Q(T, "Economic Survey highlights", "Intermediate",
  "What real GDP growth did the Economic Survey 2025-26 project for FY27 (2026-27)?",
  ["6.8 to 7.2 per cent", "7.4 per cent", "6.3 to 6.8 per cent", "7.1 per cent"],
  concept="Economic Survey 2025-26 outlook",
  explanation="The Survey, tabled on 29 January 2026, projected FY27 real GDP growth at 6.8–7.2% and placed India's "
              "potential growth at around 7%. It estimated FY26 growth at 7.4%.",
  steps=["FY27 projection: 6.8–7.2%"],
  why="7.4% is the FY26 estimate; 7.1% is RBI's October 2026 projection; 6.3–6.8% is not the Survey's range.",
  current=SURVEY,
  facts=[fact("The Survey says the real GDP growth for FY27 is projected at 6.8-7.2 per cent; potential growth around "
              "7 per cent; FY26 growth 7.4 per cent", ES_GROWTH)])
Q(T, "Economic Survey highlights", "Intermediate",
  "According to the Economic Survey 2025-26, what is the Government's medium-term goal for the Centre's debt-to-GDP "
  "ratio?",
  ["50 ± 1 per cent by FY31", "40 per cent by FY30", "55.7 per cent by FY27", "60 per cent by FY35"],
  concept="Debt anchor",
  explanation="The Survey states the medium-term goal of a debt-to-GDP ratio of 50±1% by FY31. The ratio stood at "
              "55.7% in FY25, 7.1 percentage points lower than in 2020.",
  steps=["Goal: 50 ± 1% by FY31", "FY25: 55.7%"],
  why="55.7% is the FY25 level; 40% and 60% are not the stated goal.",
  current=SURVEY,
  facts=[fact("The Government's medium-term goal to achieve a debt-to-GDP ratio of 50±1% by FY31; debt-to-GDP ratio "
              "stands at 55.7 % for FY25", ES_FISCAL)])

fd = round(53.5 - 36.5, 1)
share = 11.7 / fd * 100
assert fd == 17.0 and round(share) == 69
Q(T, "Fiscal terms", "Advanced",
  "Budget 2026-27 estimates total expenditure at ₹53.5 lakh crore, non-debt receipts at ₹36.5 lakh crore and net "
  "market borrowings from dated securities at ₹11.7 lakh crore. What is the fiscal deficit, and roughly what share of "
  "it is financed by net market borrowings?",
  ["₹17.0 lakh crore; about 69%", "₹17.0 lakh crore; about 32%", "₹28.7 lakh crore; about 41%",
   "₹17.2 lakh crore; about 100%"],
  concept="Fiscal deficit arithmetic",
  explanation="Fiscal deficit = total expenditure − non-debt receipts = 53.5 − 36.5 = ₹17.0 lakh crore. Net market "
              "borrowings of ₹11.7 lakh crore finance 11.7 ÷ 17.0 ≈ 69% of it; the balance comes from small savings "
              "and other sources.",
  steps=["FD = 53.5 − 36.5 = 17.0", "11.7 ÷ 17.0 ≈ 0.69"],
  why="32% divides borrowings by non-debt receipts; ₹28.7 lakh crore is net tax receipts; ₹17.2 lakh "
      "crore is gross market borrowing, not the deficit.",
  computed=True, current=BUDGET,
  facts=[fact("Non-debt receipts and expenditure estimated as 36.5 lakh crore and 53.5 lakh crore; net market "
              "borrowings from dated securities 11.7 lakh crore; balance from small savings and other sources; gross "
              "market borrowings 17.2 lakh crore; net tax receipts 28.7 lakh crore", PIB_BUDGET)])
Q(T, "Union Budget highlights", "Advanced",
  "Consider the following announcements of the Union Budget 2026-27:\nI. A dedicated ₹10,000 crore SME Growth Fund "
  "to create future champion enterprises.\nII. An incentive of ₹100 crore for a single municipal bond issuance of more "
  "than ₹1,000 crore.\nIII. Merger of the Power Finance Corporation with SBI.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Financial sector announcements, Budget 2026-27",
  explanation="The Budget announced a ₹10,000 crore SME Growth Fund and a ₹2,000 crore top-up of the Self-Reliant "
              "India Fund (I right), and a ₹100 crore incentive for single municipal bond issues above ₹1,000 crore "
              "(II right). It proposed restructuring PFC and REC to improve public sector NBFCs, not merging PFC with "
              "SBI (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (PFC–REC restructuring)"],
  why="III is false, so options including it are wrong; 'I only' omits II.",
  current=BUDGET,
  facts=[fact("Dedicated 10,000 crore SME Growth Fund; incentive of 100 crore for a single bond issuance of more than "
              "1000 crore; restructure the Power Finance Corporation and Rural Electrification Corporation",
              PIB_BUDGET)])
Q(T, "Economic Survey highlights", "Advanced",
  "Consider the following statements based on the Economic Survey 2025-26:\nI. The Centre's revenue deficit, "
  "budgeted at 0.8% of GDP for FY26, is the lowest since FY09.\nII. Income tax return filings rose from 6.9 crore in "
  "FY22 to 9.2 crore in FY25.\nIII. The Centre's fiscal deficit was budgeted to rise from 4.4% of GDP in FY25 to "
  "4.8% in FY26.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Fiscal highlights of the Economic Survey",
  explanation="The Survey notes the revenue deficit at its lowest since FY09, budgeted at 0.8% for FY26 (I right), "
              "and ITR filings rising from 6.9 crore (FY22) to 9.2 crore (FY25) (II right). The fiscal deficit was "
              "budgeted to fall to 4.4% in FY26 from 4.8% in FY25, not rise (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (reversed)"],
  why="III reverses the direction of change, so options including it are wrong; 'I only' omits II.",
  current=SURVEY,
  facts=[fact("Revenue deficit at its lowest since FY09, budgeted at 0.8% in FY26; income tax filing rises to 9.2 "
              "crore in FY25 from 6.9 crore in FY22; fiscal deficit budgeted at 4.4% of GDP in FY26, down from 4.8% "
              "in FY25", ES_FISCAL)])

# ================================================================= 31. Government Financial Schemes (2 / 5 / 3)
T = "Government Financial Schemes"
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Basic",
  "Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY) is available to bank account holders in which age group?",
  ["18 to 50 years", "18 to 70 years", "18 to 40 years", "21 to 60 years"],
  concept="PMJJBY eligibility",
  explanation="PMJJBY is a one-year renewable life insurance scheme giving ₹2 lakh cover for death due to any reason, "
              "available to people aged 18 to 50 years with a bank account.",
  steps=["PMJJBY: 18–50 years"],
  why="18–70 is PMSBY; 18–40 is APY; 21–60 is not a scheme's age band.",
  facts=[fact("PMJJBY ... available to people in the age group of 18 to 50 years having a bank account", PMJJBY)])
Q(T, "Credit guarantee schemes", "Basic",
  "As described in the Government's note of April 2022 (when the scheme had been extended up to 2025), bank loans "
  "under the Stand-Up India scheme for setting up a greenfield enterprise by SC/ST or women entrepreneurs ranged "
  "between:",
  ["₹10 lakh and ₹1 crore", "₹50,000 and ₹10 lakh", "₹1 crore and ₹5 crore", "₹10,000 and ₹50,000"],
  concept="Stand-Up India",
  explanation="Stand-Up India, launched on 5 April 2016 and extended up to 2025, facilitated bank loans between ₹10 "
              "lakh and ₹1 crore to at least one SC/ST borrower and at least one woman borrower per bank branch for a "
              "greenfield enterprise in manufacturing, services, trading or allied agriculture.",
  steps=["Loan range: ₹10 lakh – ₹1 crore"],
  why="₹50,000–₹10 lakh resembles MUDRA bands; the other ranges are not Stand-Up India's.",
  facts=[fact6("Note dated 5 April 2022: Stand Up India facilitates bank loans between 10 lakh and 1 Crore to at least "
               "one SC or ST borrower and at least one woman borrower per bank branch for a greenfield enterprise; "
               "scheme extended up to the year 2025", STANDUP)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Intermediate",
  "Pradhan Mantri MUDRA Yojana was launched on 8 April 2015. What is described as its core objective?",
  ["Funding the Unfunded", "Housing for All", "Sabka Bima Sabki Raksha", "One Nation One Ombudsman"],
  concept="PMMY",
  explanation="PMMY, launched on 8 April 2015, offers collateral-free loans up to ₹20 lakh to non-corporate, non-farm "
              "small and micro enterprises. Its core objective is described as 'Funding the Unfunded'.",
  steps=["PMMY motto: Funding the Unfunded"],
  why="Housing for All relates to PMAY; Sabka Bima Sabki Raksha to insurance law; One Nation One Ombudsman to RB-IOS.",
  current=ca("2026-04-08"),
  facts=[fact("PMMY launched on April 8, 2015; the core objective of the MUDRA Yojana is 'Funding the Unfunded'; "
              "collateral-free loans up to ₹20 lakh", MUDRA_PIB)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Intermediate",
  "What is the risk cover period of Pradhan Mantri Suraksha Bima Yojana (PMSBY), and what is its age eligibility?",
  ["1 June to 31 May; 18 to 70 years", "1 April to 31 March; 18 to 50 years", "1 January to 31 December; 18 to 60 "
   "years", "1 June to 31 May; 18 to 50 years"],
  concept="PMSBY features",
  explanation="PMSBY is a one-year renewable accident insurance scheme for bank account holders aged 18 to 70, with "
              "the risk cover period running from 1 June to 31 May and premium auto-debited.",
  steps=["Cover period: 1 June – 31 May", "Age: 18–70"],
  why="18–50 is PMJJBY's age band; the cover year is June–May, not the financial or calendar year.",
  facts=[fact("PMSBY available to people in the age group of 18 to 70 years having a bank account; risk cover "
              "period: 1st June to 31st May", PMSBY)])
Q(T, "Credit guarantee schemes", "Intermediate",
  "In May 2025, DPIIT notified the expansion of the Credit Guarantee Scheme for Startups (CGSS), raising the ceiling "
  "on guarantee cover per borrower from ₹10 crore to:",
  ["₹20 crore", "₹15 crore", "₹25 crore", "₹50 crore"],
  concept="CGSS",
  explanation="The notified expansion of CGSS raised the guarantee ceiling per borrower from ₹10 crore to ₹20 crore "
              "and increased the extent of guarantee cover, following the Budget 2025-26 announcement.",
  steps=["CGSS ceiling: ₹10 crore → ₹20 crore"],
  why="₹15 crore, ₹25 crore and ₹50 crore are not the new ceiling.",
  current=ca("2025-05-09"),
  facts=[fact("DPIIT notified the expansion of CGSS which increases the ceiling on guarantee cover per borrower from "
              "Rs. 10 crore to Rs. 20 crore", CGSS_PIB)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Intermediate",
  "According to official figures released on PMMY's 11th anniversary, roughly what share of MUDRA loans have been "
  "sanctioned to women entrepreneurs?",
  ["About two-thirds", "About one-fifth", "About one-tenth", "About half"],
  concept="Reach of PMMY",
  explanation="Over 57.79 crore loans amounting to ₹40.07 lakh crore have been sanctioned under PMMY; about "
              "two-thirds of the loans went to women entrepreneurs, and about one-fifth to first-time "
              "entrepreneurs.",
  steps=["Women: about two-thirds of loans"],
  why="About one-fifth is the share of first-time entrepreneurs; one-tenth and half are not the reported shares.",
  current=ca("2026-04-08"),
  facts=[fact("More than 57.79 crore loans sanctioned, ₹40.07 lakh crore disbursed; two-thirds of the loans sanctioned "
              "to women entrepreneurs; approximately one-fifth to first-time entrepreneurs", MUDRA_PIB)])
Q(T, "Credit guarantee schemes", "Intermediate",
  "According to the Government's April 2022 note on the Stand-Up India scheme, what was the maximum repayment period "
  "of a loan, and the maximum moratorium?",
  ["Up to 7 years, with a moratorium of up to 18 months", "Up to 5 years, with a moratorium of up to 6 months",
   "Up to 10 years, with a moratorium of up to 3 years", "Up to 3 years, with no moratorium"],
  concept="Stand-Up India terms",
  explanation="As described in the April 2022 note, Stand-Up India loans were repayable over a maximum of 7 years "
              "with a maximum moratorium of 18 months, and the interest rate was capped at the bank's lowest rate for "
              "the category, not exceeding MCLR + 3% + tenor premium.",
  steps=["Repayment ≤ 7 years", "Moratorium ≤ 18 months"],
  why="The other tenure and moratorium combinations do not match the scheme.",
  facts=[fact6("Note dated 5 April 2022: repayment period a maximum of up to 7 years with a maximum moratorium period "
               "of up to 18 months", STANDUP)])

def cgss_cover(loan, default):
    return default * (0.85 if loan <= 10 else 0.75)


assert round(cgss_cover(8, 6), 2) == 5.10 and round(cgss_cover(16, 12), 2) == 9.00
Q(T, "Credit guarantee schemes", "Advanced",
  "Under the expanded Credit Guarantee Scheme for Startups, two guaranteed loans default: Startup A borrowed ₹8 crore "
  "and ₹6 crore is in default; Startup B borrowed ₹16 crore and ₹12 crore is in default. What guarantee cover is "
  "available on each?",
  ["A: ₹5.1 crore; B: ₹9.0 crore", "A: ₹4.5 crore; B: ₹10.2 crore", "A: ₹6.8 crore; B: ₹12.0 crore",
   "A: ₹5.1 crore; B: ₹10.2 crore"],
  concept="Extent of CGSS cover",
  explanation="Cover is 85% of the amount in default for loans up to ₹10 crore and 75% for loans above ₹10 crore. A "
              "(loan ₹8 crore): 85% × 6 = ₹5.1 crore. B (loan ₹16 crore, within the ₹20 crore ceiling): 75% × 12 = "
              "₹9.0 crore.",
  steps=["A: loan ≤ ₹10 crore → 85% × 6 = 5.1", "B: loan > ₹10 crore → 75% × 12 = 9.0"],
  why="The second option swaps the rates; the third applies 85% to the loan amounts; the fourth applies 85% to B.",
  computed=True, current=ca("2025-05-09"),
  facts=[fact("Extent of guarantee cover increased to 85% of the amount in default for loan amount up to Rs. 10 crore "
              "and 75% of the amount in default for loan amount exceeding Rs. 10 crore; ceiling Rs. 20 crore",
              CGSS_PIB)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Advanced",
  "Suresh, aged 54, has a savings bank account and has never enrolled in any government insurance scheme. Which of "
  "the following can he newly join?",
  ["PMSBY only", "PMJJBY only", "Both PMJJBY and PMSBY", "Neither PMJJBY nor PMSBY"],
  concept="Comparing PMJJBY and PMSBY eligibility",
  explanation="PMJJBY is open to bank account holders aged 18–50, so at 54 Suresh cannot join it. PMSBY is open to "
              "those aged 18–70, so he can join PMSBY.",
  steps=["PMJJBY: 18–50 → 54 is outside", "PMSBY: 18–70 → 54 is inside"],
  why="He is too old for PMJJBY but within PMSBY's band.",
  computed=True,
  facts=[fact("PMJJBY available to people in the age group of 18 to 50 years having a bank account", PMJJBY),
         fact("PMSBY available to people in the age group of 18 to 70 years having a bank account", PMSBY)])
Q(T, "Credit guarantee schemes", "Advanced",
  "Applying the Stand-Up India eligibility conditions as described in the Government's April 2022 note, which of "
  "the following applicants would have been eligible for a loan?",
  ["A woman setting up her first manufacturing unit, seeking ₹60 lakh and bringing 15% of the project cost as margin "
   "money, including 10% as her own contribution",
   "A partnership firm in which an SC entrepreneur holds 45% of the stake, setting up a new unit",
   "A woman entrepreneur seeking a loan to expand her existing shop",
   "An ST entrepreneur seeking ₹1.5 crore for a new unit"],
  concept="Stand-Up India eligibility",
  explanation="Loans are for greenfield (first-time) enterprises, between ₹10 lakh and ₹1 crore. For non-individual "
              "enterprises, at least 51% of the shareholding and controlling stake must be with SC/ST and/or women "
              "entrepreneurs. Margin money is up to 15% of project cost, with at least 10% as own contribution. Only "
              "the first applicant satisfies all conditions.",
  steps=["Greenfield? Amount ₹10 lakh–₹1 crore? 51% stake? Margin ≤ 15% with ≥ 10% own contribution?"],
  why="A 45% stake is below 51%; expansion of an existing shop is not greenfield; ₹1.5 crore exceeds ₹1 crore.",
  facts=[fact6("Note dated 5 April 2022: loans only for green field projects; non-individual enterprises need 51% of "
               "shareholding and controlling stake by SC/ST and/or women; loans between 10 lakh and 1 crore; margin "
               "money up to 15% with at least 10% own contribution", STANDUP)])

# ================================================================= 32. RBI Circulars and Regulatory Updates (2 / 3 / 2)
T = "RBI Circulars and Regulatory Updates"
Q(T, "Recent RBI directions", "Basic",
  "Under RBI's Lending Against Gold and Silver Collateral Directions, 2025, what is the maximum loan-to-value (LTV) "
  "ratio for consumption loans of up to ₹2.5 lakh?",
  ["85 per cent", "75 per cent", "80 per cent", "90 per cent"],
  concept="Gold loan LTV",
  explanation="The Directions set tiered LTV ceilings for consumption loans against gold or silver: 85% for loans up "
              "to ₹2.5 lakh, 80% above ₹2.5 lakh up to ₹5 lakh, and 75% above ₹5 lakh.",
  steps=["≤ ₹2.5 lakh: 85%", "₹2.5–5 lakh: 80%", "> ₹5 lakh: 75%"],
  why="80% and 75% apply to larger loans; 90% is not a tier.",
  current=ca("2026-04-01"),
  facts=[fact("LTV: ≤₹2.5 lakh 85 per cent; > ₹2.5 lakh & ≤ ₹5 lakh 80 per cent; compliance no later than April 1, "
              "2026", GOLD_MD)])
Q(T, "Recent RBI directions", "Basic",
  "RBI's Pre-payment Charges on Loans Directions, 2025 bar pre-payment charges on floating rate loans to individuals "
  "for non-business purposes. To which loans do they apply?",
  ["Loans sanctioned or renewed on or after 1 January 2026", "All loans outstanding on 1 April 2025",
   "Only loans sanctioned after 1 April 2027", "Only housing loans sanctioned before 2020"],
  concept="Pre-payment charges",
  explanation="The Directions, issued on 2 July 2025, apply to loans and advances sanctioned or renewed on or after 1 "
              "January 2026. No pre-payment charges may be levied on floating rate loans to individuals for "
              "non-business purposes, or on floating rate business loans to individuals and MSEs (subject to "
              "lender-specific conditions).",
  steps=["Applies to loans sanctioned/renewed from 1 January 2026"],
  why="The rule is prospective from 1 January 2026; the other dates are wrong.",
  current=ca("2026-01-01"),
  facts=[fact("Pre-payment charges directions apply to loans sanctioned or renewed on or after January 1, 2026; no "
              "pre-payment charges on floating rate loans granted for purposes other than business to individuals",
              PREPAY)])
Q(T, "Recent RBI directions", "Intermediate",
  "Under RBI's Authentication Mechanisms for Digital Payment Transactions Directions, 2025, which requirement applies "
  "to digital payments other than card-present transactions?",
  ["At least two distinct factors of authentication, at least one of which is dynamically created or proven",
   "A biometric factor is compulsory and SMS OTP is no longer allowed",
   "A single static PIN is sufficient", "Two factors are needed only for payments above ₹5,000"],
  concept="Additional factor of authentication",
  explanation="All digital payments need at least two distinct authentication factors unless exempted. For "
              "transactions other than card-present ones, at least one factor must be dynamic, i.e. unique to the "
              "transaction. No specific factor is mandated, so SMS OTP remains usable. Compliance was due by 1 "
              "April 2026.",
  steps=["≥ 2 factors", "≥ 1 dynamic factor (non-card-present)", "Compliance by 1 April 2026"],
  why="No factor such as biometrics is mandated; a static PIN alone is one factor; there is no ₹5,000 threshold in "
      "the general rule.",
  current=ca("2026-04-01"),
  facts=[fact("All digital payment transactions shall be authenticated by at least two distinct factors; for "
              "transactions other than card present, at least one factor is dynamically created or proven; "
              "compliance by April 01, 2026", AFA_MD)])
Q(T, "Recent RBI directions", "Intermediate",
  "Under RBI's 2025 directions on lending against gold and silver, what is the cap on the aggregate weight of coins "
  "a borrower may pledge for all loans?",
  ["50 grams of gold coins and 500 grams of silver coins", "1 kg of gold coins and 10 kg of silver coins",
   "100 grams of gold coins and 1 kg of silver coins", "No cap on coins"],
  concept="Collateral limits",
  explanation="Coins pledged by a borrower for all loans may not exceed 50 grams of gold coins and 500 grams of "
              "silver coins. For ornaments, the caps are 1 kg of gold and 10 kg of silver.",
  steps=["Coins: 50 g gold, 500 g silver", "Ornaments: 1 kg gold, 10 kg silver"],
  why="1 kg/10 kg are the ornament limits; 100 g/1 kg are not prescribed; coins are capped.",
  current=ca("2026-04-01"),
  facts=[fact("Aggregate weight of coin(s) pledged ... shall not exceed 50 grams in case of gold coins and 500 grams "
              "in case of silver coins; ornaments 1 kilogram gold and 10 kilograms silver", GOLD_MD)])
Q(T, "Recent RBI directions", "Intermediate",
  "Under RBI's Authentication Mechanisms Directions, 2025, who bears the loss if a digital payment is put through "
  "without complying with the Directions?",
  ["The issuer must compensate the customer for the loss in full, without demur",
   "The customer bears the loss up to ₹10,000", "The loss is shared equally by issuer and customer",
   "The payment system operator bears it only if the customer reports within 30 days"],
  concept="Liability under the AFA Directions",
  explanation="The Directions state that if any loss arises from transactions effected without complying with them, "
              "the issuer shall compensate the customer for the loss in full without demur.",
  steps=["Non-compliant transaction → issuer compensates in full"],
  why="The Directions place full liability on the issuer, with no sharing or customer threshold.",
  current=ca("2026-04-01"),
  facts=[fact("If any loss arises out of transactions effected without complying with these directions, the issuer "
              "shall compensate the customer for the loss in full without demur", AFA_MD)])


def max_gold_loan(value):
    best = 0
    for cap, ltv in ((2.5, 0.85), (5.0, 0.80), (float("inf"), 0.75)):
        lo = {2.5: 0, 5.0: 2.5}.get(cap, 5.0)
        amt = min(cap, value * ltv)
        if amt > lo:
            best = max(best, amt)
    return round(best, 3)


assert max_gold_loan(3.5) == 2.8
Q(T, "Recent RBI directions", "Advanced",
  "A borrower pledges gold jewellery valued at ₹3.5 lakh for a consumption loan. Under the LTV tiers of RBI's 2025 "
  "gold and silver lending directions, what is the maximum loan he can get?",
  ["₹2.80 lakh", "₹2.975 lakh", "₹2.50 lakh", "₹2.625 lakh"],
  concept="Applying tiered LTV",
  explanation="LTV depends on the loan amount: 85% up to ₹2.5 lakh, 80% above ₹2.5 lakh up to ₹5 lakh. 85% of ₹3.5 "
              "lakh = ₹2.975 lakh, but that exceeds ₹2.5 lakh, so the 80% tier applies: 80% × 3.5 = ₹2.80 lakh, "
              "which lies within the ₹2.5–5 lakh band. So the maximum is ₹2.80 lakh.",
  steps=["85% × 3.5 = 2.975 > 2.5 → 85% tier not available for this amount",
         "80% × 3.5 = 2.80, within ₹2.5–5 lakh → allowed"],
  why="₹2.975 lakh wrongly applies 85% to a loan above ₹2.5 lakh; ₹2.50 lakh stops at the first tier; ₹2.625 lakh "
      "applies 75%.",
  computed=True, current=ca("2026-04-01"),
  facts=[fact("Maximum LTV for consumption loans: 85 per cent up to ₹2.5 lakh; 80 per cent above ₹2.5 lakh and up to "
              "₹5 lakh", GOLD_MD)])
Q(T, "Recent RBI directions", "Advanced",
  "Consider the following statements about RBI's 2025 directions on lending against gold and silver:\nI. Loans "
  "cannot be given against primary gold or silver, or against units of gold ETFs or gold mutual funds.\nII. Loans "
  "cannot be given for the purchase of gold in any form.\nIII. Detailed assessment of repayment capacity is required "
  "for every gold loan, whatever its size.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Restrictions on gold lending",
  explanation="The directions bar lending against primary gold/silver and against financial assets backed by them, "
              "such as ETF or MF units (I right), and bar lending to purchase gold in any form (II right). Detailed "
              "credit assessment is mandatory only where total loans against eligible collateral exceed ₹2.5 lakh "
              "per borrower (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (only above ₹2.5 lakh)"],
  why="III ignores the ₹2.5 lakh threshold, so options including it are wrong; 'I only' omits II.",
  current=ca("2026-04-01"),
  facts=[fact("No lending against primary gold or silver or financial assets backed by them such as ETF or MF units; "
              "no lending for purchase of gold in any form; detailed credit assessment where the total loan amount "
              "against eligible collateral is above ₹2.5 lakh", GOLD_MD)])


# ================================================================= checks and output
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_002_plan.json").read_text(encoding="utf-8"))
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
AUDIT_REVISED = {"BANK_BFA_000342", "BANK_BFA_000343", "BANK_BFA_000388", "BANK_BFA_000393", "BANK_BFA_000396"}
assert AUDIT_REVISED <= {q["question_id"] for q in questions}
for q in questions:
    if q["question_id"] in AUDIT_REVISED:
        v = q["verification"]
        v["verified_by"] = [x for x in v["verified_by"] if x != "ai:independent-check"]
        v["verified_at"] = AUDIT_DAY

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_002",
    "created_at": TODAY,
    "notes": "BATCH_002 Banking and Financial Awareness part: 200 original questions (60 Basic, 80 Intermediate, "
             "60 Advanced) across 32 topics, IDs BANK_BFA_000204 to BANK_BFA_000403. Includes the time-sensitive "
             "topics Repo Rate (MPC decisions of December 2025, August 2026 and October 2026) and Budget and "
             "Economic Survey (Union Budget 2026-27 of 1 February 2026; Economic Survey 2025-26 of 29 January "
             "2026). Every question carries fact checks against primary sources (RBI, PIB, DFS, SEBI, AMFI, BIS, "
             "IBBI, BSE) opened on 2026-11-05, or search-confirmed where the official page could not be fetched "
             "(marked web:search-confirmed). Changeable values carry current_affairs dates. Computed answers are "
             "re-derived in tools/batch_002/banking.py. Facts tested in BATCH_000/BATCH_001 are not repeated.",
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_002_BFA.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions; keys {dict(sorted(_keys.items()))})")
