"""Writes batches/parts/BATCH_001_BFA.json: the 200 Banking and Financial Awareness questions of BATCH_001.

Every fact is backed by at least one fact_check whose source page was opened (WebFetch) or confirmed through a web
search on 2026-11-05. Values that can change (rates, limits, thresholds, office-holders) carry current_affairs dates.
Every computable answer (CRR/SLR requirements, CRAR, provisioning, PSL targets, T-bill yield, NAV, compensation
limits, NPA dates, corridor rates) is re-derived below with assertions before the file is written. The quota per
(topic, difficulty) is checked against the batch plan and the answer keys are balanced. If any check fails, nothing
is written.

    python tools/batch_001/banking.py      (run from docs/question-bank, or from anywhere)
"""

import datetime as dt
import json
import random
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-05"
REVIEW_BY = "2027-05-05"
LETTERS = "ABCD"
BF = "Banking and Financial Awareness"
FIRST_ID = 4
TEXT = ("ai:author-solve", "web:fact-check")
CALC = ("ai:author-solve", "web:fact-check", "script:recompute")
SECONDS = {"Basic": 20, "Intermediate": 30, "Advanced": 60}

_rng = random.Random(20261105)
_keys = Counter()
questions = []


def fact(claim, url):
    return {"claim": claim, "source_url": url, "checked_on": TODAY}


AUDIT_DAY = "2026-11-06"  # superseded-rules audit of 2026-11-06


def fact6(claim, url):
    return {"claim": claim, "source_url": url, "checked_on": AUDIT_DAY}


def ca(event_date, review_by=REVIEW_BY):
    return {"event_date": event_date, "review_by": review_by}


def Q(topic, subtopic, difficulty, text, options, answer=None, *, concept, explanation, steps, facts, why=None,
      seconds=None, computed=False, current=None, shortcut=None):
    """Adds one question. With answer=None, options[0] is the correct text and it is placed at the least-used key
    so far (random tie-break, fixed seed). Ordered options (numbers) pass an explicit answer letter."""
    assert len(options) == 4 and len(set(options)) == 4, text
    assert facts, text
    if answer is None:
        low = min(_keys[k] for k in LETTERS)
        pos = LETTERS.index(_rng.choice([k for k in LETTERS if _keys[k] == low]))
        correct, wrongs = options[0], list(options[1:])
        options = wrongs[:pos] + [correct] + wrongs[pos:]
        answer = LETTERS[pos]
    assert answer in LETTERS
    _keys[answer] += 1
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
                           "verified_by": list(CALC if computed else TEXT), "verified_at": TODAY,
                           "fact_checks": facts}
    questions.append(out)


def inr(x):
    """Indian digit grouping for whole rupee/crore figures: 210000 -> 2,10,000."""
    s = str(int(x))
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    return ",".join([head, *parts, tail]) if head else ",".join([*parts, tail])


assert inr(210000) == "2,10,000" and inr(37800) == "37,800" and inr(500) == "500"

# ---------------------------------------------------------------- sources (all opened or search-confirmed 2026-11-05)
RBI_HOME = "https://www.rbi.org.in/"
MPC_OCT26 = "https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=63742"
MP_OVERVIEW = "https://www.rbi.org.in/scripts/FS_Overview.aspx?fn=2752"
STANCE_PR = "https://rbidocs.rbi.org.in/rdocs/PressRelease/PDFs/PR62DB3C24380A9D40B886CB92FC3E63474D.PDF"
EBLR = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11677&Mode=0"
SDF_PR = "https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=53539"
CRR_CUT = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12858&Mode=0"
EXPLAIN_NOTES = "https://www.rbi.org.in/annualdata/explanatorynotes.html"
SLR_2020 = "https://www.rbi.org.in/commonman/Upload/English/Notification/PDFs/NT2170558BB99816C46E1993A0920861FCCC7.PDF"
RTGS_FAQ = "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=275"
NEFT_FAQ = "https://rbi.org.in/Scripts/faqview.aspx?Id=60"
NEFT_247 = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11750&Mode=0"
IMPS_NPCI = "https://www.npci.org.in/product/imps/about-imps"
IMPS_RBI = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=52368"
PSR_DEC24 = "https://www.rbi.org.in/scripts/PublicationsView.aspx?Id=23127"
PSR_DEC25 = "https://www.rbi.org.in/Scripts/PublicationsView.aspx?id=23813"
OFFLINE_FW = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12215"
UPI_LITE_NPCI = "https://www.npci.org.in/product/upi/upi-lite"
UPI123_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=1810601&reg=48&lang=2"
UPI_CIRCLE_NPCI = "https://www.npci.org.in/product/upi-circle"
RBI_AR_2425 = "https://www.rbi.org.in/scripts/AnnualReportPublications.aspx?Id=1439"
PAYNOW_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=1911736&reg=3&lang=2"
UPI_PIB_FACT = "https://www.pib.gov.in/FactsheetDetails.aspx?Id=150962&reg=48&lang=2"
NPCI_RBI_PUB = "https://www.rbi.org.in/scripts/PublicationsView.aspx?Id=20315"
NACH_NPCI = "https://www.npci.org.in/product/nach/about-nach"
AEPS_NPCI = "https://www.npci.org.in/product/aeps/about-aeps"
NETC_NPCI = "https://www.npci.org.in/product/netc"
FASTAG_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2287760&amp=&lang=2&amp=&reg=48"
RBIOS_FAQ = "https://www.rbi.org.in/commonperson/english/scripts/FAQs.aspx?Id=3407"
RBIOS_2021 = "https://rbidocs.rbi.org.in/rdocs/content/pdfs/RBIOS2021_121121.pdf"
PSL_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12799"
SFB_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13135"
PB_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13087"
PB_GUIDE = "https://www.rbi.org.in/scripts/bs_viewcontent.aspx?Id=2900"
PB_LIMIT_PR = "https://www.rbi.org.in/commonman/english/scripts/PressReleases.aspx?Id=3289"
IRAC_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13146"
ECL_MD = "https://rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13400"
ECL_PR = "https://rbidocs.rbi.org.in/rdocs/PressRelease/PDFs/PR150994739A099E843668A75A7F92C9E9BD1.PDF"
CAP_TABLE = "https://www.rbi.org.in/scripts/bs_viewcontent.aspx?Id=4364"
LEV_2019 = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=11606&Mode=0"
LEV_2017_PR = "https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=63854"
LCR_2025 = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12836&Mode=0"
NSFR_2021 = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12025&Mode=0"
NSFR_2018 = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11278"
DSIB_2025 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=61729"
BCBS_HIST = "https://www.bis.org/bcbs/history.htm"
BASEL3 = "https://www.bis.org/publ/bcbs189.pdf"
PCA_2021 = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12186"
ORG = "https://www.rbi.org.in/commonman/english/Scripts/Organisation.aspx"
OUR_HISTORY = "https://www.rbi.org.in/Scripts/OurHistory.aspx"
CHRON_50 = "https://rbi.org.in/history/Brief_Chro1950to1960.html"
CHRON_68 = "https://rbi.org.in/history/Brief_Chro1968to1985.html"
CHRON_91 = "https://rbi.org.in/history/Brief_Chro1991to2000.html"
GOV_PR = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=59281"
RBI_FY = "https://www.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1325"
CURRENCY_FAQ = "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=3158"
RBI_ACT = "https://rbidocs.rbi.org.in/rdocs/publications/pdfs/rbia1934170510.pdf"
WMA_OVERVIEW = "https://www.rbi.org.in/scripts/FS_Overview.aspx?fn=2758"
IDMD = "https://www.rbi.org.in/commonman/Upload/English/Content/PDFs/RIA160609.pdf"
FSDC_PIB = "https://www.pib.gov.in/newsite/PrintRelease.aspx?relid=95543&reg=48&lang=2"
MERGER_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=1605147&reg=3&lang=2"
RRB_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2120016"
RRB_DFS = "https://financialservices.gov.in/regional-rural-banks-0"
URJIT_SPEECH = "https://rbidocs.rbi.org.in/rdocs/Speeches/PDFs/ITNCAER05052026D577FDFF9E9D4BA7913E41BAD5F00A93.PDF"
CPI_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2291051&reg=48&lang=2"
WPI_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2267963&reg=3&lang=1"
WPI_PIB2 = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2272872&reg=48&lang=1"
IBBI_FAQ = "https://ibbi.gov.in/uploads/faqs/CIRPFAQs%20Final2408.pdf"
SARFAESI_RBI = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=1730&Mode=0"
ARC_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12669"
PMJDY_PIB = "https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2161401&reg=48&lang=2"
PMJDY_DFS = "https://financialservices.gov.in/index.php/pradhan-mantri-jan-dhan-yojana-pmjdy"
BC_2006 = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=2718&Mode=0"
BC_2010 = "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/CPC28092010.pdf"
BC_MC = "https://www.rbi.org.in/scripts/BS_ViewMasCirculardetails.aspx?Id=5108&Mode=0"
BC_ELIG = "https://www.rbi.org.in/scripts/bs_viewcontent.aspx?Id=2234"
DL_2025 = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12848"
DBC_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13163"
ERUPEE_FAQ = "https://www.rbi.org.in/commonman/English/scripts/FAQs.aspx?Id=3686"
EW_PR = "https://rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=54616"
CTS_CC = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12891"
POSPAY = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=11969"
CHEQUE_3M = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=6805&Mode=0"
AC_PAYEE = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=6022&Mode=0"
DICGC_FAQ = "https://www.dicgc.org.in/FAQs"
DICGC_PR = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=49330"
BSBDA = "https://www.rbi.org.in/commonman/english/scripts/Notification.aspx?Id=2979"
BSBD_2025 = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=13173"
NRI_FAQ = "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=3"
SEBI_ABOUT = "https://www.sebi.gov.in/about-sebi.html"
IFSCA = "https://ifsca.gov.in/Pages/Contents/About_Us"
IFSCA_CP = ("https://ifsca.gov.in/Document/ReportandPublication/"
            "consultation_paper_on_cybersecurity_framework_28092024_final28092024012331.pdf")
MM_2016 = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=10495"
CP_2025 = "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/142MD1111202598527CBD7B6D4BFC9792D568AD07F27D.PDF"
GSEC_FAQ = "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=711"
SENSEX = "https://beta.bseindia.com/Sensex/bse_sensex.aspx"
NIFTY = "https://archives.nseindia.com/content/indices/ind_nifty50.pdf"
NIFTY_FAQ = "https://www.nseindia.com/static/products-services/indices-faqs"
T1_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=1990745&reg=3&lang=2"
ICDR_FAQ = "https://www.sebi.gov.in/sebi_data/faqfiles/may-2025/1747290561386.pdf"
IRDAI = "https://irdai.gov.in/what-we-do"
IRDAI_ADDR = "https://irdai.gov.in/address-for-communication"
FDI_INS = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2206011&reg=3&lang=1"
FDI_BUDGET = "https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2098394&reg=48&lang=2"
PMJJBY = "https://financialservices.gov.in/pradhan-mantri-jeevan-jyoti-bima-yojana-pmjjby"
PMSBY = "https://financialservices.gov.in/pradhan-mantri-suraksha-bima-yojana-pmsby"
AMFI = "https://www.amfiindia.com/aboutamfi"
NAV_AMFI = "https://www.amfiindia.com/investor/knowledge-center-info?zoneName=NetAssetValueNAV"
NAV_SEBI = "https://www.sebi.gov.in/sebi_data/faqfiles/sep-2024/1727242783639.pdf"
ELSS_SID = "https://www.sebi.gov.in/sebi_data/mutualfundfile/feb-2026/1771312099447.pdf"
MF_CAT = "https://www.amfiindia.com/Themes/Theme1/downloads/1507291273374.pdf"
APY_FAQ = "https://www.pfrda.org.in/w/faqs/atal-pension-yojana"
MUDRA_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2249915&reg=3&lang=1"
MUDRA_GAZ = "https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2069170&reg=3&lang=2"
CGTMSE_PIB = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2288366&reg=48&lang=1"
CONSOL_PR = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=61705"
CONSOL_NOTE = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=13170"
MD_INDEX = "https://rbi.org.in/scripts/bs_viewmasterdirections.aspx"
NABARD = "https://www.nabard.org/ftrcontent.aspx?id=492"

# ================================================================= 1. Banking Fundamentals (4 / 5 / 4)
T = "Banking Fundamentals"
Q(T, "Types of accounts", "Basic",
  "What is the maximum deposit insurance cover that DICGC provides to a depositor of an insured bank?",
  ["₹5 lakh per depositor per bank, for principal and interest together", "₹1 lakh per depositor per bank",
   "₹5 lakh per account, so each account of the depositor is covered separately",
   "₹10 lakh per depositor across all banks"],
  concept="Deposit insurance by DICGC",
  explanation="The Deposit Insurance and Credit Guarantee Corporation (DICGC), a wholly owned subsidiary of RBI, "
              "insures each depositor in an insured bank up to ₹5,00,000 for principal and interest together. "
              "Deposits held in the same right and capacity in all branches of a bank are added up for this limit. "
              "The cover was raised from ₹1 lakh to ₹5 lakh with effect from 4 February 2020.",
  steps=["DICGC cover = ₹5 lakh", "It is per depositor per bank (all branches combined), not per account",
         "Principal and interest are covered together within ₹5 lakh"],
  why="₹1 lakh was the limit before 4 February 2020. The limit is per depositor per bank, not per account, and "
      "deposits in different banks are covered separately rather than under one combined cap.",
  current=ca("2020-02-04"),
  facts=[fact("Each depositor is insured up to ₹5,00,000 for principal and interest; deposits in all branches of a "
              "bank are aggregated", DICGC_FAQ),
         fact("DICGC raised the cover from ₹1 lakh to ₹5 lakh per depositor with effect from 4 February 2020",
              DICGC_PR)])
Q(T, "Types of accounts", "Basic",
  "Which of the following is a feature of a Basic Savings Bank Deposit Account (BSBDA) as prescribed by RBI?",
  ["No minimum balance needs to be maintained", "An initial deposit of ₹1,000 is needed to open it",
   "Only two deposits are allowed in a month", "It can be opened only by persons with income below ₹1 lakh"],
  concept="Basic Savings Bank Deposit Account",
  explanation="Under RBI's Commercial Banks – Responsible Business Conduct Directions, 2025 (BSBD paragraphs as "
              "amended on 4 December 2025, effective 1 April 2026), the BSBD account is a normal banking service "
              "available to all. Its facilities are free without any minimum balance, no initial deposit is needed, "
              "deposits are unlimited in number and value, and at least four free withdrawals a month are given.",
  steps=["BSBDA is RBI's no-frills account for financial inclusion",
         "Key feature: no minimum balance and no initial deposit"],
  why="No initial deposit is required; deposits are unlimited in number and value; there is no income condition.",
  facts=[fact6("BSBD account (commercial banks, effective 1 April 2026): facilities free without any minimum balance; "
               "no initial deposit; no limit on number and value of deposits; minimum four free withdrawals a month; "
               "available to all", BSBD_2025)])
Q(T, "Types of banks", "Basic",
  "A 'scheduled bank' in India is a bank that is included in:",
  ["The Second Schedule to the Reserve Bank of India Act, 1934",
   "The Third Schedule to the Banking Regulation Act, 1949",
   "The First Schedule to the Negotiable Instruments Act, 1881",
   "The Schedule to the Banking Companies (Acquisition and Transfer of Undertakings) Act, 1970"],
  concept="Scheduled and non-scheduled banks",
  explanation="Banks listed in the Second Schedule to the RBI Act, 1934 are scheduled banks. A bank qualifies if "
              "its paid-up capital and reserves are at least ₹5 lakh and RBI is satisfied that its affairs are not "
              "conducted against depositors' interests. Scheduled banks must keep CRR with RBI and can access RBI "
              "liquidity.",
  steps=["'Scheduled' refers to the Second Schedule of the RBI Act, 1934",
         "Inclusion is under Section 42(6)(a) of the RBI Act"],
  why="The Third Schedule of the BR Act prescribes balance-sheet forms; the other Acts do not define scheduled "
      "status.",
  facts=[fact("Banks included in the Second Schedule to the RBI Act, 1934 are scheduled banks; criteria: paid-up "
              "capital and reserves of at least ₹5 lakh and affairs not detrimental to depositors", EXPLAIN_NOTES)])
Q(T, "Cheques and instruments", "Basic",
  "For how long from the date of issue is a cheque, draft or pay order valid for payment, as per RBI instructions?",
  ["3 months", "6 months", "1 month", "1 year"],
  concept="Validity of cheques and bank instruments",
  explanation="From 1 April 2012, RBI reduced the validity of cheques, drafts, pay orders and banker's cheques from "
              "six months to three months from the date of issue. An instrument presented after three months is "
              "'stale' and is not paid.",
  steps=["RBI circular of 4 November 2011, effective 1 April 2012", "Validity = 3 months from the date of issue"],
  why="Six months was the validity before 1 April 2012; one month and one year were never the rule.",
  facts=[fact("Cheques/drafts/pay orders presented beyond three months from date of issue shall not be paid "
              "(effective 1 April 2012)", CHEQUE_3M)])
Q(T, "Cheques and instruments", "Intermediate",
  "Under RBI's Positive Pay System for cheques, banks must enable the facility for all account holders issuing "
  "cheques of what amount?",
  ["₹50,000 and above", "₹5 lakh and above", "₹10,000 and above", "₹2 lakh and above"],
  concept="Positive Pay System (PPS) in CTS",
  explanation="Under Positive Pay (from 1 January 2021), the drawer sends key cheque details such as date, payee "
              "and amount to the bank in advance; CTS cross-checks them when the cheque is presented. Banks must "
              "enable it for cheques of ₹50,000 and above. Using it is the customer's choice, but banks may make it "
              "mandatory for cheques of ₹5 lakh and above.",
  steps=["PPS threshold for enabling: ₹50,000", "₹5 lakh is only the level at which banks MAY make it mandatory"],
  why="₹5 lakh is the optional mandatory level for banks, not the threshold for enabling the facility. ₹10,000 and "
      "₹2 lakh are not PPS thresholds.",
  facts=[fact("Banks to enable Positive Pay for all account holders issuing cheques of ₹50,000 and above; may make "
              "it mandatory for ₹5 lakh and above; implemented from 1 January 2021", POSPAY)])
Q(T, "Cheques and instruments", "Intermediate",
  "Under 'continuous clearing and settlement on realisation' in the Cheque Truncation System (Phase 1 from "
  "4 October 2025), what happens to a cheque that the drawee bank does not confirm within the prescribed time?",
  ["It is treated as deemed approved and included in settlement", "It is automatically returned unpaid",
   "It is carried over to the next working day's clearing", "It is referred to RBI for a decision"],
  concept="CTS continuous clearing (2025)",
  explanation="RBI moved CTS from batch clearing to continuous clearing in two phases (Phase 1 on 4 October 2025, "
              "Phase 2 announced for 3 January 2026). Cheques are scanned and presented continuously in one "
              "session; the drawee bank must confirm (positive or negative) within the prescribed window, failing "
              "which the cheque is deemed approved and settled. Settlement runs hourly, and banks credit customers "
              "within one hour of settlement.",
  steps=["Drawee bank must send a positive or negative confirmation",
         "No confirmation in time → deemed approved → settled"],
  why="An unconfirmed cheque is not returned or carried over; RBI does not decide individual cheques.",
  current=ca("2025-10-04"),
  facts=[fact("CTS moves to continuous clearing and settlement on realisation: Phase 1 on 4 October 2025; cheques "
              "not confirmed within the prescribed time are deemed approved", CTS_CC),
         fact("Banks are required to credit customer accounts within one hour of settlement", PSR_DEC25)])
Q(T, "Types of accounts", "Intermediate",
  "Which non-resident account is maintained in Indian rupees and allows the funds in it to be repatriated abroad "
  "freely without RBI approval?",
  ["Non-Resident External (NRE) account", "Non-Resident Ordinary (NRO) account",
   "Foreign Currency Non-Resident (Bank) [FCNR(B)] account", "Resident Foreign Currency (RFC) account"],
  concept="Accounts of non-residents in India",
  explanation="An NRE account is a rupee account whose funds can be repatriated outside India without RBI "
              "approval. An NRO account is also in rupees but is meant for income earned in India, and remittance "
              "of its balances is capped. FCNR(B) deposits are held in foreign currency, not rupees.",
  steps=["Rupee account + freely repatriable → NRE", "NRO: rupee, repatriation capped",
         "FCNR(B): foreign currency term deposit"],
  why="NRO is not freely repatriable; FCNR(B) is a foreign-currency account; RFC accounts are for returning "
      "residents, not non-residents.",
  facts=[fact("NRE account funds may be repatriated outside India without RBI approval", NRI_FAQ)])
Q(T, "Types of banks", "Intermediate",
  "To be included in the Second Schedule to the RBI Act, a bank's paid-up capital and reserves must in aggregate "
  "be at least:",
  ["₹5 lakh", "₹50 lakh", "₹100 crore", "₹1 crore"],
  concept="Criteria for scheduled bank status",
  explanation="Under Section 42(6)(a) of the RBI Act, a bank can be included in the Second Schedule if its paid-up "
              "capital and reserves are not less than ₹5 lakh in aggregate and RBI is satisfied that its affairs "
              "are not being conducted in a manner detrimental to the interests of its depositors.",
  steps=["Recall the RBI Act criterion: paid-up capital + reserves ≥ ₹5 lakh",
         "Plus RBI's satisfaction about depositor interests"],
  why="₹100 crore and similar figures are licensing capital norms for new banks, not the scheduling criterion.",
  facts=[fact("Inclusion in the Second Schedule requires paid-up capital and reserves of at least ₹5 lakh and "
              "affairs not detrimental to depositors' interests", EXPLAIN_NOTES)])
Q(T, "Types of accounts", "Intermediate",
  "Who bears the deposit insurance premium payable to DICGC?",
  ["The insured bank, which cannot pass it on to depositors", "The depositor, through an annual deduction",
   "The Government of India", "RBI, out of its surplus"],
  concept="Deposit insurance premium",
  explanation="Deposit insurance is mandatory for insured banks. The premium is borne entirely by the insured bank "
              "and cannot be passed on to depositors; it is paid half-yearly on the bank's assessable deposits.",
  steps=["Insured entity = the bank", "Premium is the bank's cost, not the depositor's"],
  why="Depositors pay nothing for the cover; neither the Government nor RBI pays the premium.",
  facts=[fact("Deposit insurance premium is borne entirely by the insured bank and cannot be passed on to "
              "depositors", DICGC_FAQ)])

dicgc_x = [F(32, 10), F(25, 10)]   # ₹ lakh, Bank X, same capacity, two branches
assert sum(dicgc_x) == F(57, 10) and min(sum(dicgc_x), 5) == 5
Q(T, "Types of accounts", "Advanced",
  "Ravi holds, in his individual name, a savings account of ₹3.2 lakh at one branch of Bank X and a fixed deposit of "
  "₹2.5 lakh (including interest) at another branch of Bank X. He also has a fixed deposit of ₹4 lakh in Bank Y. If "
  "Bank X goes into liquidation, how much will DICGC pay Ravi in respect of Bank X?",
  ["₹3.2 lakh", "₹5 lakh", "₹5.7 lakh", "₹9.7 lakh"],
  answer="B",
  concept="DICGC cover: per depositor, per bank, same right and capacity",
  explanation="Deposits held in the same right and capacity in all branches of the same bank are added together: "
              "3.2 + 2.5 = ₹5.7 lakh. The cover is capped at ₹5 lakh per depositor per bank, so Ravi receives ₹5 "
              "lakh for Bank X. His deposit in Bank Y is in a separate bank and is not affected.",
  steps=["Aggregate Bank X deposits: 3.2 + 2.5 = ₹5.7 lakh", "Apply cap: min(5.7, 5) = ₹5 lakh",
         "Bank Y deposits are irrelevant to Bank X's claim"],
  why="₹5.7 lakh ignores the cap; ₹9.7 lakh wrongly adds Bank Y; ₹3.2 lakh treats branches separately.",
  computed=True, current=ca("2020-02-04"),
  facts=[fact("Each depositor insured up to ₹5,00,000; deposits in all branches of a bank held in the same "
              "capacity are aggregated", DICGC_FAQ)])

cheque_issue, presented = dt.date(2026, 1, 10), dt.date(2026, 4, 15)
assert presented > dt.date(2026, 4, 10) > cheque_issue
Q(T, "Cheques and instruments", "Advanced",
  "Consider the following statements:\nI. A cheque dated 10 January 2026 presented for payment on 15 April 2026 "
  "should not be paid by the bank.\nII. A bank may collect an 'account payee' cheque into the account of a third "
  "party if the payee requests it in writing.\nIII. RBI requires the Positive Pay System to be used for every "
  "cheque, whatever its amount.\nWhich of the above is/are correct?",
  ["I only", "I and II only", "II and III only", "I, II and III"],
  concept="Cheque validity, account payee crossing and Positive Pay",
  explanation="I is correct: a cheque is valid for three months, so a cheque dated 10 January 2026 is stale after "
              "10 April 2026. II is wrong: account payee cheques must be collected only for the named payee (the "
              "drawer should instead withdraw the account payee mandate). III is wrong: banks must enable Positive "
              "Pay for cheques of ₹50,000 and above, and its use is at the customer's discretion.",
  steps=["I: 10 Jan + 3 months = 10 Apr; 15 Apr is beyond → not payable (correct)",
         "II: account payee cheques are not collected for third parties (wrong)",
         "III: PPS is enabled for ₹50,000+ and is not compulsory for every cheque (wrong)"],
  computed=True,
  facts=[fact("Instruments presented beyond three months from the date of issue shall not be paid", CHEQUE_3M),
         fact("Account payee cheques payable to third parties should not be collected", AC_PAYEE),
         fact("Positive Pay to be enabled for cheques of ₹50,000 and above; availing it is at the account holder's "
              "discretion", POSPAY)])

bsbda = {"atm_cash": 3, "branch_cash": 2, "upi": 4, "neft": 1}
withdrawals = bsbda["atm_cash"] + bsbda["branch_cash"]  # UPI/NEFT (digital) are not counted from 1 April 2026
assert withdrawals == 5 and withdrawals - 4 == 1
Q(T, "Types of accounts", "Advanced",
  "In a month in 2026-27, a BSBD account holder of a commercial bank makes 3 ATM cash withdrawals, 2 cash withdrawals "
  "at the branch, 4 UPI payments and 1 NEFT transfer. Under RBI's BSBD rules in force from 1 April 2026, which "
  "statement is correct?",
  ["5 transactions count as withdrawals; at least 4 must be free and the bank decides on the fifth",
   "10 transactions count as withdrawals and all must be free",
   "Only the 3 ATM cash withdrawals count, so all of them must be free",
   "5 transactions count as withdrawals and all 5 must be free because a BSBDA carries no charges"],
  concept="Free withdrawals in a BSBDA",
  explanation="Under RBI's Commercial Banks – Responsible Business Conduct Directions, 2025 (BSBD paragraphs as "
              "amended on 4 December 2025, effective 1 April 2026), a BSBD account gets a minimum of four free "
              "withdrawals a month, including transfers and ATM transactions. Digital payments other than ATM "
              "transactions (POS, NEFT, RTGS, UPI, IMPS) are not counted as withdrawals. Here 3 ATM + 2 branch = 5 "
              "withdrawals: four must be free; whether the fifth is charged is the bank's decision. (Before April "
              "2026, NEFT and other modes also counted towards the four.)",
  steps=["Withdrawals: 3 ATM cash + 2 branch cash = 5", "UPI (4) and NEFT (1) are digital payments, not counted",
         "Minimum free = 4; the fifth is at the bank's discretion"],
  why="UPI and NEFT payments are not counted as withdrawals; RBI mandates a minimum of four free, not all.",
  computed=True,
  facts=[fact6("BSBD (commercial banks, effective 1 April 2026): minimum four free withdrawals a month including "
               "transfers and ATM transactions; POS, NEFT, RTGS, UPI, IMPS etc. not counted as withdrawals",
               BSBD_2025)])
Q(T, "Types of accounts", "Advanced",
  "An NRI has ₹12 crore in his NRO account from the sale of inherited property and wants to remit the equivalent of "
  "USD 1.2 million abroad in the current financial year. Under the NRO rules, what is permitted?",
  ["He can remit up to USD 1 million this financial year; the balance must wait for a later year",
   "He can remit the full USD 1.2 million because NRO funds are freely repatriable",
   "He cannot remit anything because NRO balances are fully non-repatriable",
   "He must first convert the NRO balance into an FCNR(B) deposit, after which there is no limit"],
  concept="Repatriation from NRO accounts",
  explanation="NRO balances of NRIs/PIOs can be remitted up to USD 1 million per financial year (April–March), "
              "together with other eligible assets, subject to tax and FEMA conditions. So only USD 1 million can "
              "go out this year; the remaining USD 0.2 million can be remitted in a later financial year.",
  steps=["NRO repatriation cap: USD 1 million per financial year",
         "Requested 1.2 million > 1 million → only 1 million this year"],
  why="NRO funds are not freely repatriable (that is NRE), but they are not fully blocked either. Shifting money "
      "from NRO to FCNR(B) is not a route around the cap.",
  facts=[fact("Balances in an NRO account of NRIs/PIOs are remittable up to USD 1 million per financial year "
              "(April-March)", NRI_FAQ)])

# ================================================================= 2. History of Banking in India (2 / 3 / 2)
T = "History of Banking in India"
Q(T, "Nationalisation", "Basic",
  "How many major commercial banks were nationalised on 19 July 1969?",
  ["6", "10", "14", "20"],
  answer="C",
  concept="Bank nationalisation, 1969",
  explanation="On 19 July 1969, 14 major scheduled commercial banks, each with deposits of over ₹50 crore, were "
              "nationalised. Six more private banks were nationalised on 15 April 1980.",
  steps=["1969: 14 banks (deposits above ₹50 crore)", "1980: 6 more banks"],
  why="6 is the 1980 round; 20 is the total of both rounds; 10 has no basis.",
  facts=[fact("19 July 1969: 14 major scheduled commercial banks with deposits over ₹50 crore nationalised",
              CHRON_68)])
Q(T, "Nationalisation", "Basic",
  "State Bank of India was constituted on 1 July 1955 by converting which bank into a state-owned institution?",
  ["Imperial Bank of India", "Presidency Bank of Bombay", "Allahabad Bank", "Bank of Hindustan"],
  concept="Origin of SBI",
  explanation="The Imperial Bank of India, formed in 1921 by merging the three Presidency banks, was converted into "
              "the state-owned State Bank of India on 1 July 1955.",
  steps=["Imperial Bank of India → State Bank of India (1 July 1955)"],
  why="The Presidency Bank of Bombay had already merged into the Imperial Bank; Allahabad Bank merged into Indian "
      "Bank in 2020; Bank of Hindustan was an early private bank.",
  facts=[fact("Imperial Bank of India converted into a state-owned institution, State Bank of India, on 1 July "
              "1955", CHRON_50)])
Q(T, "Mergers and consolidation", "Intermediate",
  "Under the consolidation of public sector banks effective 1 April 2020, Allahabad Bank was amalgamated into:",
  ["Indian Bank", "Punjab National Bank", "Union Bank of India", "Canara Bank"],
  concept="PSB mega-merger, 2020",
  explanation="From 1 April 2020: Oriental Bank of Commerce and United Bank of India merged into Punjab National "
              "Bank; Syndicate Bank into Canara Bank; Andhra Bank and Corporation Bank into Union Bank of India; "
              "and Allahabad Bank into Indian Bank.",
  steps=["Recall the four anchor banks and their merging partners", "Allahabad Bank → Indian Bank"],
  why="PNB took OBC and United Bank; Union Bank took Andhra and Corporation Bank; Canara took Syndicate Bank.",
  facts=[fact("Cabinet approved amalgamation w.e.f. 1.4.2020 including Allahabad Bank into Indian Bank", MERGER_PIB)])
Q(T, "Mergers and consolidation", "Intermediate",
  "Under the fourth phase of RRB amalgamation based on 'One State-One RRB', effective 1 May 2025, the number of "
  "Regional Rural Banks was reduced from 43 to:",
  ["26", "28", "30", "33"],
  answer="B",
  concept="RRB consolidation",
  explanation="The Department of Financial Services notified the amalgamation of 26 RRBs in the fourth phase, "
              "effective 1 May 2025, reducing the number of RRBs from 43 to 28. RRBs were first set up in 1975 "
              "(the first on 2 October 1975) and function under the RRBs Act, 1976.",
  steps=["Phase IV: 26 RRBs amalgamated", "43 → 28 RRBs w.e.f. 1 May 2025"],
  why="26 is the number of RRBs amalgamated, not the number left; 30 and 33 are not the official counts.",
  current=ca("2025-05-01"),
  facts=[fact("Phase IV amalgamation of 26 RRBs; number of RRBs reduced from 43 to 28 w.e.f. 1 May 2025", RRB_PIB),
         fact("28 RRBs operate; RRBs established under the RRBs Act, 1976; first RRB set up on 2 October 1975",
              RRB_DFS)])
Q(T, "Committees", "Intermediate",
  "The committee whose November 1991 report recommended a phased reduction of SLR and CRR and the introduction of "
  "income recognition and capital adequacy norms was chaired by:",
  ["M. Narasimham", "Raja J. Chelliah", "Urjit R. Patel", "Nachiket Mor"],
  concept="Banking sector reform committees",
  explanation="The Narasimham Committee on the Financial System (1991) laid the foundation of banking reforms: "
              "phased reduction of SLR and CRR, prudential norms for income recognition and asset classification, "
              "and capital adequacy. RBI introduced income recognition and asset classification norms in April "
              "1992.",
  steps=["1991 report on the financial system → M. Narasimham"],
  why="Raja Chelliah headed tax reforms; Urjit Patel headed the 2014 monetary policy framework committee; Nachiket "
      "Mor headed a 2013 committee on financial services for small businesses and low-income households.",
  facts=[fact("Nov 1991: Narasimham Committee report recommended phased SLR/CRR reduction, accounting standards, "
              "income recognition and capital adequacy norms; IRAC norms introduced April 1992", CHRON_91)])

events = {"III": 1955, "II": 1975, "I": 1980, "IV": 1982}
assert ", ".join(sorted(events, key=events.get)) == "III, II, I, IV"
Q(T, "Nationalisation", "Advanced",
  "Arrange the following events in chronological order:\nI. Nationalisation of six private sector banks\n"
  "II. Setting up of Regional Rural Banks\nIII. Conversion of the Imperial Bank of India into State Bank of India\n"
  "IV. Establishment of NABARD",
  ["III, II, I, IV", "III, I, II, IV", "II, III, IV, I", "III, II, IV, I"],
  concept="Chronology of Indian banking",
  explanation="Imperial Bank became SBI on 1 July 1955; RRBs were set up from 26 September 1975; six banks were "
              "nationalised on 15 April 1980; NABARD was established on 12 July 1982.",
  steps=["III: 1955", "II: 1975", "I: 1980", "IV: 1982", "Order: III, II, I, IV"],
  why="The other sequences misplace the 1980 nationalisation relative to RRBs (1975) or NABARD (1982).",
  computed=True,
  facts=[fact("RRBs set up 26 Sep 1975; six private banks nationalised 15 Apr 1980; NABARD established 12 Jul 1982",
              CHRON_68),
         fact("SBI constituted 1 July 1955 from Imperial Bank of India", CHRON_50)])
Q(T, "Committees", "Advanced",
  "Consider the following statements:\nI. The Expert Committee chaired by Urjit R. Patel (report January 2014) "
  "recommended adopting the new CPI (combined) as the key measure of inflation.\nII. The RBI Act was amended in "
  "2016 to give a statutory basis to flexible inflation targeting.\nIII. Under the amended Act, the inflation "
  "target is fixed by the Monetary Policy Committee itself.\nWhich of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="From the Urjit Patel Committee to flexible inflation targeting",
  explanation="The Urjit Patel Committee recommended CPI (combined) as the key measure of inflation and a "
              "disinflation glide path. The RBI Act was amended in May 2016 to provide a statutory basis for "
              "flexible inflation targeting. The target itself (4% CPI, band 2–6%) is set by the Central Government "
              "in consultation with RBI, not by the MPC; the MPC sets the policy rate to achieve it.",
  steps=["I: correct (CPI combined as key measure)", "II: correct (May 2016 amendment)",
         "III: wrong — the Central Government sets the target"],
  facts=[fact("Urjit Patel Committee (report January 2014): recommendations included adopting CPI (combined) as the "
              "key measure of inflation", URJIT_SPEECH),
         fact("RBI Act amended in May 2016 for flexible inflation targeting; Central Government sets the 4% target "
              "with 2-6% band", MP_OVERVIEW)])

# ================================================================= 3. Reserve Bank of India (3 / 3 / 3)
T = "Reserve Bank of India"
Q(T, "Establishment and structure", "Basic",
  "The Reserve Bank of India was established on 1 April 1935 under which law?",
  ["Reserve Bank of India Act, 1934", "Banking Regulation Act, 1949", "Reserve Bank of India Act, 1935",
   "Government of India Act, 1935"],
  concept="Establishment of RBI",
  explanation="RBI was established on 1 April 1935 under the Reserve Bank of India Act, 1934. It started as a "
              "privately owned bank and has been fully owned by the Government of India since nationalisation in "
              "1949.",
  steps=["Act passed in 1934; RBI began operations on 1 April 1935"],
  why="The Act is of 1934, not 1935; the BR Act, 1949 regulates banks; the GoI Act, 1935 is a constitutional statute.",
  facts=[fact("RBI established on April 1, 1935 under the Reserve Bank of India Act, 1934", ORG)])
Q(T, "Establishment and structure", "Basic",
  "RBI's central office was initially located in Kolkata (Calcutta). In which year was it permanently moved to "
  "Mumbai?",
  ["1935", "1937", "1949", "1951"],
  answer="B",
  concept="RBI central office",
  explanation="The central office was set up in Kolkata in 1935 and permanently shifted to Mumbai in 1937. The "
              "Governor sits at the central office, where policy is formulated.",
  steps=["1935: Kolkata", "1937: moved permanently to Mumbai"],
  why="1935 is the year of establishment; 1949 is nationalisation; 1951 has no link.",
  facts=[fact("Central office set up in Kolkata, permanently moved to Mumbai in 1937", ORG)])
Q(T, "Governors and leadership", "Basic",
  "Who is the Governor of the Reserve Bank of India as of November 2026?",
  ["Sanjay Malhotra", "Shaktikanta Das", "Poonam Gupta", "Urjit Patel"],
  concept="RBI leadership",
  explanation="Sanjay Malhotra, an IAS officer of the 1990 Rajasthan cadre and earlier Revenue Secretary, took "
              "charge as the 26th Governor of RBI on 11 December 2024 for three years. He succeeded Shaktikanta Das "
              "and chaired the Central Board's 625th meeting on 30 October 2026.",
  steps=["Took charge 11 December 2024 as 26th Governor", "Term: three years"],
  why="Shaktikanta Das was the previous Governor (to 10 December 2024); Poonam Gupta is a Deputy Governor; Urjit "
      "Patel was Governor in 2016–2018.",
  current=ca("2024-12-11"),
  facts=[fact("Sanjay Malhotra took charge as the 26th Governor of RBI for a three-year period effective "
              "December 11, 2024", GOV_PR)])
Q(T, "Establishment and structure", "Intermediate",
  "RBI was set up as a shareholders' bank. In which year was it nationalised, making it fully owned by the "
  "Government of India?",
  ["1949", "1947", "1955", "1969"],
  concept="Ownership of RBI",
  explanation="RBI was privately owned when it began in 1935. It was nationalised in 1949 and has since been fully "
              "owned by the Government of India.",
  steps=["Private shareholders' bank (1935) → nationalised 1949"],
  why="1947 is Independence; 1955 is the creation of SBI; 1969 is the nationalisation of 14 commercial banks.",
  facts=[fact("RBI was initially privately owned; since nationalisation in 1949 it is fully owned by the Government "
              "of India", ORG)])
Q(T, "Governors and leadership", "Intermediate",
  "Apart from the Governor, how many Deputy Governors at most can be official directors on RBI's Central Board?",
  ["Two", "Three", "Four", "Five"],
  answer="C",
  concept="Central Board of Directors",
  explanation="The official directors on RBI's Central Board are the full-time Governor and not more than four "
              "Deputy Governors. Non-official directors are nominated by the Government (ten from various fields, "
              "four from the local boards, and two government officials).",
  steps=["Official directors = Governor + up to 4 Deputy Governors"],
  why="RBI's structure provides for up to four Deputy Governors.",
  facts=[fact("Official directors: Governor and not more than four Deputy Governors (full-time)", ORG)])
Q(T, "Establishment and structure", "Intermediate",
  "Which of the following is NOT a wholly owned subsidiary of RBI?",
  ["National Bank for Agriculture and Rural Development (NABARD)",
   "Deposit Insurance and Credit Guarantee Corporation (DICGC)",
   "Bharatiya Reserve Bank Note Mudran Private Limited (BRBNMPL)",
   "Reserve Bank Innovation Hub (RBIH)"],
  concept="RBI subsidiaries",
  explanation="RBI's fully owned subsidiaries are DICGC, BRBNMPL, ReBIT, IFTAS and RBIH. NABARD is a statutory "
              "development bank established in 1982 under its own Act and is not listed as an RBI subsidiary.",
  steps=["List RBI subsidiaries: DICGC, BRBNMPL, ReBIT, IFTAS, RBIH", "NABARD is not among them"],
  why="DICGC, BRBNMPL and RBIH are all listed by RBI as fully owned subsidiaries.",
  facts=[fact("RBI's fully owned subsidiaries: DICGC, BRBNMPL, ReBIT, IFTAS and RBIH", ORG)])
Q(T, "Establishment and structure", "Advanced",
  "Consider the following statements about RBI's accounting year:\nI. From 2020-21, RBI changed its accounting "
  "year from July–June to April–March.\nII. The year 2020-21 was a transition year covering only nine months "
  "(July 2020 to March 2021).\nIII. The change was meant to align RBI's year with the Government's fiscal year.\n"
  "Which of the above is/are correct?",
  ["I, II and III", "I and II only", "I and III only", "II only"],
  concept="RBI's accounting year",
  explanation="On the recommendation of the Expert Committee on the Economic Capital Framework (chaired by Bimal "
              "Jalan), RBI moved from a July–June to an April–March year from 2020-21, in sync with the "
              "Government's fiscal year. The transition year 2020-21 ran from July 2020 to March 2021, i.e. nine "
              "months.",
  steps=["I: correct", "II: correct (July 2020–March 2021 = 9 months)", "III: correct (alignment with GoI)"],
  facts=[fact("RBI's accounting year changed from July-June to April-March from 2020-21 on the Bimal Jalan "
              "committee's recommendation; 2020-21 covered nine months", RBI_FY)])
Q(T, "Governors and leadership", "Advanced",
  "Consider the following statements about the RBI Governor's roles:\nI. The Governor chairs the Monetary Policy "
  "Committee and has a second or casting vote in case of a tie.\nII. The Governor chairs the Sub-Committee of the "
  "Financial Stability and Development Council (FSDC).\nIII. The Governor chairs the FSDC itself.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Governor's chairmanships",
  explanation="The Governor is the ex-officio chairperson of the MPC and has a casting vote if votes are equal. The "
              "FSDC is chaired by the Union Finance Minister; its Sub-Committee, the primary operating arm, is "
              "chaired by the RBI Governor.",
  steps=["I: correct", "II: correct (FSDC Sub-Committee chaired by Governor)",
         "III: wrong (FSDC chaired by the Finance Minister)"],
  facts=[fact("Each MPC member has one vote; in case of equality the Governor has a second or casting vote",
              MP_OVERVIEW),
         fact("FSDC is chaired by the Union Finance Minister; its Sub-Committee is chaired by the RBI Governor",
              FSDC_PIB)])

board = {"Governor": 1, "Deputy Governors (max)": 4, "from local boards": 4, "nominated experts": 10,
         "government officials": 2}
assert sum(board.values()) == 21
Q(T, "Establishment and structure", "Advanced",
  "RBI's Central Board consists of the Governor, Deputy Governors (at most four), one director from each of the four "
  "local boards, ten directors nominated by the Government from various fields and two Government officials. What "
  "is the maximum strength of the Central Board?",
  ["17", "19", "20", "21"],
  answer="D",
  concept="Composition of RBI's Central Board",
  explanation="Adding the maximum in each category: 1 Governor + 4 Deputy Governors + 4 local-board directors + 10 "
              "nominated directors + 2 Government officials = 21.",
  steps=["Official: 1 + 4 = 5", "Non-official: 4 + 10 + 2 = 16", "Total = 21"],
  why="17 omits the Deputy Governors; 19 omits the Government officials; 20 drops one category member.",
  computed=True,
  facts=[fact("Central Board: Governor and up to four Deputy Governors; ten government-nominated directors, two "
              "government officials and four directors, one each from the four local boards", ORG)])

# ================================================================= 4. RBI Functions (3 / 3 / 3)
T = "RBI Functions"
Q(T, "Regulator and supervisor", "Basic",
  "RBI manages foreign exchange in India under which Act?",
  ["Foreign Exchange Management Act, 1999", "Foreign Exchange Regulation Act, 1973",
   "Prevention of Money Laundering Act, 2002", "Banking Regulation Act, 1949"],
  concept="RBI as manager of foreign exchange",
  explanation="RBI manages foreign exchange under FEMA, 1999, which replaced FERA, 1973 and became operative in June "
              "2000 with the aim of facilitating external trade and payments.",
  steps=["Forex management law: FEMA, 1999 (replaced FERA)"],
  why="FERA was repealed; PMLA deals with money laundering; the BR Act regulates banking companies.",
  facts=[fact("RBI manages foreign exchange under the Foreign Exchange Management Act, 1999", ORG),
         fact("FEMA replaced FERA, 1973 and became operative in June 2000", CHRON_91)])
Q(T, "Issuer of currency", "Basic",
  "Under which law are coins issued in India?",
  ["The Coinage Act, 2011", "Section 22 of the RBI Act, 1934", "The Indian Coinage Act, 1906",
   "The Banking Regulation Act, 1949"],
  concept="Issue of coins versus bank notes",
  explanation="Bank notes are issued by RBI under the RBI Act, 1934, while coins (and one-rupee notes) are issued "
              "under the Coinage Act, 2011 by the Government of India and put into circulation through RBI. One-rupee "
              "notes issued under the Coinage Act are legal tender and treated as rupee coin.",
  steps=["Notes → RBI Act, 1934", "Coins → Coinage Act, 2011"],
  why="Section 22 of the RBI Act covers bank notes; the 1906 Act was replaced by the 2011 Act; the BR Act is unrelated.",
  facts=[fact("The statutory provisions for issue of bank notes and coins are the RBI Act, 1934 and the Coinage Act, "
              "2011", CURRENCY_FAQ)])
Q(T, "Banker to government", "Basic",
  "What are Ways and Means Advances (WMA) given by RBI to the governments?",
  ["Temporary advances to bridge mismatches between receipts and payments",
   "Long-term loans to finance capital expenditure", "Grants to state governments for welfare schemes",
   "Refinance to banks for priority sector lending"],
  concept="RBI as banker to government",
  explanation="As banker to the Centre and the States, RBI gives Ways and Means Advances to cover temporary "
              "mismatches between government receipts and payments. They are short-term (repayable within three "
              "months each); WMA limits for the Centre are fixed in consultation with the Government.",
  steps=["WMA = short-term advance for timing gaps in cash flows"],
  why="WMA is not long-term finance, a grant, or bank refinance.",
  facts=[fact("WMA are temporary advances to bridge mismatches in receipts and payments, repayable within three "
              "months", WMA_OVERVIEW)])
Q(T, "Banker to government", "Intermediate",
  "From 1 April 1997, the Ways and Means Advances arrangement for the Central Government replaced which system, "
  "ending automatic monetisation of the fiscal deficit?",
  ["Ad hoc Treasury Bills", "Open market operations", "Market Stabilisation Scheme",
   "Liquidity Adjustment Facility"],
  concept="End of automatic monetisation",
  explanation="Before 1997, the Centre's deficits were financed automatically through ad hoc Treasury Bills issued "
              "to RBI. RBI and the Government agreed to replace them with WMA from 1 April 1997, ending automatic "
              "monetisation.",
  steps=["Pre-1997: ad hoc T-bills", "1 April 1997: WMA introduced"],
  why="OMOs and LAF are liquidity tools; MSS was introduced in 2004 for sterilisation.",
  facts=[fact("1 Apr 1997: ad hoc Treasury Bills replaced by Ways and Means Advances, ending automatic monetisation",
              CHRON_91)])
Q(T, "Banker to government", "Intermediate",
  "RBI manages the public debt of a State Government:",
  ["By agreement with that State Government under Section 21A of the RBI Act",
   "Automatically under Section 22 of the RBI Act",
   "Only if the Finance Commission directs it",
   "Under Section 35A of the Banking Regulation Act"],
  concept="RBI as debt manager for States",
  explanation="Sections 20 and 21 make RBI the banker and debt manager of the Central Government by statute. For "
              "States, Section 21A allows RBI to take up banking and debt management by agreement with each State "
              "Government.",
  steps=["Centre: Sections 20/21 (obligatory)", "States: Section 21A (by agreement)"],
  why="Section 22 deals with issue of bank notes; Section 35A of the BR Act gives RBI power to issue directions to "
      "banks; the Finance Commission has no such role.",
  facts=[fact("Under Section 21A, RBI may by agreement with the Government of any State undertake management of "
              "that State's public debt", IDMD)])
Q(T, "Regulator and supervisor", "Intermediate",
  "Under the revised Prompt Corrective Action (PCA) framework for scheduled commercial banks laid down in RBI's "
  "circular of 2 November 2021 (effective 1 January 2022), which of the following was NOT one of the key areas "
  "monitored?",
  ["Profitability", "Capital", "Asset quality", "Leverage"],
  concept="PCA framework",
  explanation="The revised PCA framework (circular of 2 November 2021) monitors capital (CRAR/CET1), asset quality "
              "(Net NPA ratio) and leverage (Tier 1 leverage ratio). Profitability (return on assets) was dropped as "
              "a trigger; it is considered only while assessing exit.",
  steps=["Indicators: CRAR/CET1, Net NPA ratio, Tier 1 leverage ratio", "Profitability is not a trigger"],
  why="Capital, asset quality and leverage were exactly the three monitored areas.",
  facts=[fact6("Revised PCA (2 Nov 2021, effective 1 Jan 2022): key areas capital, asset quality and leverage",
               PCA_2021)])

nnpa = F(72, 10)
assert 6 <= nnpa < 9
Q(T, "Regulator and supervisor", "Advanced",
  "A scheduled commercial bank meets its CRAR (including CCB) and leverage ratio requirements, but its Net NPA ratio "
  "has risen to 7.2%. Under the risk thresholds in RBI's PCA circular of 2 November 2021, what was its position?",
  ["It breaches Risk Threshold 1 on asset quality, which can trigger PCA",
   "There is no breach, because the asset-quality trigger starts at a Net NPA ratio of 10%",
   "There is no breach, because asset quality is not a PCA indicator",
   "It is automatically placed under Risk Threshold 3"],
  concept="Applying PCA risk thresholds",
  explanation="Under the 2021 framework, Risk Threshold 1 for asset quality is a Net NPA ratio of 6.0% or more but "
              "less than 9.0%. A Net NPA of 7.2% falls in this band, so the bank breaches Risk Threshold 1 and can "
              "be placed under PCA even though capital and leverage are fine.",
  steps=["Asset quality indicator = Net NPA ratio", "Threshold 1: 6.0% ≤ NNPA < 9.0%",
         "7.2% lies in this band → breach of Risk Threshold 1"],
  why="Asset quality is one of the three indicators, and 7.2% is below the higher thresholds, so it is not "
      "Threshold 3.",
  computed=True,
  facts=[fact6("PCA (circular of 2 Nov 2021) asset quality Risk Threshold 1: Net NPA ratio ≥ 6.0% but < 9.0%",
               PCA_2021)])
Q(T, "Regulator and supervisor", "Advanced",
  "As laid down in RBI's circular of 2 November 2021, the revised PCA framework applied to which of the following?\nI. Foreign banks operating in "
  "India through branches\nII. Small Finance Banks\nIII. Regional Rural Banks",
  ["I only", "I and II only", "II and III only", "I, II and III"],
  concept="Scope of the PCA framework",
  explanation="The 2021 circular applied the PCA framework to all scheduled commercial banks operating in India, "
              "including foreign banks operating through branches or subsidiaries. Small Finance Banks, Payments "
              "Banks and Regional Rural Banks were excluded. A bank could exit PCA after four continuous quarterly "
              "financial statements (one audited) showed no breach of any risk threshold.",
  steps=["Included: SCBs incl. foreign banks", "Excluded: SFBs, PBs, RRBs"],
  facts=[fact6("PCA circular of 2 Nov 2021: applies to all banks operating in India including foreign banks "
               "operating through branches or subsidiaries; addressed to SCBs excluding Small Finance Banks, "
               "Payments Banks and RRBs", PCA_2021)])
Q(T, "Issuer of currency", "Advanced",
  "Consider the following statements:\nI. Under Section 22 of the RBI Act, RBI has the sole right to issue bank "
  "notes in India.\nII. The design, form and material of bank notes are approved by the Central Government after "
  "considering the recommendations of RBI's Central Board.\nIII. Every bank note issued by RBI, unless withdrawn "
  "from circulation, is legal tender anywhere in India.\nWhich of the above is/are correct?",
  ["I, II and III", "I and II only", "I and III only", "II and III only"],
  concept="Note issue: legal provisions",
  explanation="Section 22 gives RBI the sole right to issue bank notes; Section 25 says the design, form and "
              "material are approved by the Central Government after considering the Central Board's "
              "recommendations; and every RBI bank note, unless withdrawn from circulation, is legal tender at any "
              "place in India.",
  steps=["I: Section 22 — correct", "II: Section 25 — correct", "III: legal tender unless withdrawn — correct"],
  facts=[fact("Section 22: RBI has the sole right to issue bank notes; every bank note issued by RBI, unless "
              "withdrawn, is legal tender anywhere in India", CURRENCY_FAQ),
         fact("Section 25: design, form and material of bank notes approved by the Central Government after "
              "considering the Central Board's recommendations", RBI_ACT)])

# ================================================================= 5. Monetary Policy (3 / 4 / 3)
T = "Monetary Policy"
Q(T, "MPC structure", "Basic",
  "How many members does the Monetary Policy Committee (MPC) constituted under Section 45ZB of the RBI Act have?",
  ["Four", "Five", "Six", "Seven"],
  answer="C",
  concept="Composition of the MPC",
  explanation="The MPC has six members: three from RBI (the Governor as chairperson, the Deputy Governor in charge "
              "of monetary policy, and one RBI officer nominated by the Central Board) and three external members "
              "appointed by the Central Government.",
  steps=["3 RBI members + 3 external members = 6"],
  why="Four is the quorum, not the strength.",
  facts=[fact("Section 45ZB provides for a six-member MPC: Governor (chair), DG in charge of monetary policy, one RBI "
              "officer and three external members", MP_OVERVIEW)])
Q(T, "MPC structure", "Basic",
  "If the votes in the Monetary Policy Committee are equally divided, who has the second or casting vote?",
  ["The RBI Governor", "The Union Finance Minister", "The senior-most external member",
   "The Deputy Governor in charge of monetary policy"],
  concept="Voting in the MPC",
  explanation="Each MPC member has one vote. In the event of an equality of votes, the Governor, who chairs the "
              "MPC, has a second or casting vote.",
  steps=["One member, one vote", "Tie → Governor's casting vote"],
  why="The Finance Minister is not an MPC member; external members and the Deputy Governor have only one vote each.",
  facts=[fact("In the event of an equality of votes, the Governor has a second or casting vote", MP_OVERVIEW)])
Q(T, "Policy stance", "Basic",
  "In RBI's monetary policy statements, what does the 'stance' of monetary policy indicate?",
  ["The likely direction of future policy rate moves", "The current level of the CRR",
   "The inflation target set by the Government", "The volume of government borrowing for the year"],
  concept="Monetary policy stance",
  explanation="The stance signals the intended direction of policy going forward. It is broadly accommodative "
              "(inclined to ease), neutral (could move either way depending on data) or tightening (inclined to "
              "raise rates).",
  steps=["Stance = forward guidance on the direction of policy rates"],
  why="The CRR level, inflation target and borrowing programme are not what the stance communicates.",
  facts=[fact("The stance signals the intended direction of the policy rate going forward: accommodative, neutral "
              "or tightening", STANCE_PR)])
Q(T, "MPC structure", "Intermediate",
  "What is the quorum for a meeting of the Monetary Policy Committee?",
  ["Three members", "Four members", "Five members", "All six members"],
  answer="B",
  concept="MPC meetings",
  explanation="The quorum for an MPC meeting is four members. The MPC must meet at least four times a year, and "
              "minutes are published on the 14th day after each meeting.",
  steps=["Quorum = 4"],
  why="Three is too few; five or six are not required.",
  facts=[fact("The quorum for an MPC meeting is four members", MP_OVERVIEW)])
Q(T, "MPC structure", "Intermediate",
  "On which day after a meeting are the minutes of the MPC's proceedings published?",
  ["The 14th day", "The 7th day", "The 21st day", "The 30th day"],
  concept="Transparency of MPC decisions",
  explanation="RBI publishes the MPC minutes on the 14th day after each meeting. They include the resolution, the "
              "vote of each member and each member's statement.",
  steps=["Minutes = 14th day after the meeting"],
  why="7, 21 and 30 days are not the statutory timeline.",
  facts=[fact("Minutes of MPC proceedings are published on the 14th day after the meeting", MP_OVERVIEW)])
Q(T, "Transmission", "Intermediate",
  "What is the operating target of RBI's monetary policy, which it aligns with the policy repo rate through "
  "liquidity management?",
  ["Weighted average call rate (WACR)", "10-year government bond yield", "Marginal cost of funds based lending rate",
   "Savings deposit rate"],
  concept="Operating framework of monetary policy",
  explanation="RBI's operating framework aims to keep the operating target, the weighted average call rate (WACR), "
              "aligned with the policy repo rate by managing liquidity through the LAF and other instruments. "
              "Changes then pass through to other money market rates, bank deposit and lending rates.",
  steps=["Operating target = WACR (overnight call money rate)"],
  why="The 10-year yield and MCLR respond to policy but are not the operating target; the savings rate is "
      "deregulated.",
  facts=[fact("The operating framework aligns the operating target, the weighted average call rate (WACR), with "
              "the policy repo rate", MP_OVERVIEW)])
Q(T, "Transmission", "Intermediate",
  "Under RBI's external benchmark framework (from 1 October 2019) for floating-rate retail and MSE loans, how often "
  "must the interest rate be reset at a minimum?",
  ["At least once in three months", "At least once a month", "At least once in six months", "At least once a year"],
  concept="External benchmark-based lending rate (EBLR)",
  explanation="To improve transmission, RBI made it mandatory from 1 October 2019 for banks to link all new "
              "floating-rate personal/retail loans and loans to micro and small enterprises to an external "
              "benchmark (policy repo rate, FBIL 3- or 6-month T-bill yield, or another FBIL benchmark). The rate "
              "must be reset at least once in three months. MCLR-linked loans, by contrast, usually reset yearly.",
  steps=["EBLR from 1 Oct 2019", "Reset frequency: at least once in three months"],
  why="Monthly is not required; six-monthly or yearly resets are typical of MCLR, not EBLR.",
  facts=[fact("From 1 Oct 2019 new floating-rate personal/retail and MSE loans linked to an external benchmark; "
              "interest rate to be reset at least once in three months", EBLR)])
Q(T, "MPC structure", "Advanced",
  "Consider the following statements about the MPC framework:\nI. External members hold office for four years or "
  "until further orders, whichever is earlier.\nII. The MPC is required to meet at least four times a year.\n"
  "III. RBI publishes a Monetary Policy Report every quarter.\nWhich of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="MPC: tenure, meetings and reporting",
  explanation="External MPC members are appointed by the Central Government for four years or until further "
              "orders, whichever is earlier. The MPC must meet at least four times a year (in practice six). RBI "
              "publishes the Monetary Policy Report once every six months, not quarterly.",
  steps=["I: correct", "II: correct", "III: wrong — the MPR is half-yearly"],
  facts=[fact("External members hold office for four years or until further orders; MPC meets at least four times "
              "a year; Monetary Policy Report published once in every six months", MP_OVERVIEW)])
Q(T, "MPC structure", "Advanced",
  "All six MPC members attend a meeting. Three, including the Governor, vote for a 25 basis point increase in the "
  "repo rate and three vote to keep it unchanged. What is the outcome?",
  ["The repo rate is raised by 25 basis points because the Governor has a casting vote",
   "The repo rate stays unchanged because there is no majority",
   "The decision is referred to the Central Government",
   "The meeting is adjourned until an external member changes the vote"],
  concept="Decision rule of the MPC",
  explanation="MPC decisions are taken by a majority of members present and voting. With a 3–3 tie, the Governor "
              "has a second or casting vote, so the side the Governor supports prevails: the rate is raised by 25 "
              "bps.",
  steps=["Votes: 3 for hike (incl. Governor) vs 3 for status quo", "Tie → Governor's casting vote",
         "Governor favours the hike → hike carried"],
  why="A tie does not default to status quo, and neither the Government nor an adjournment decides it.",
  facts=[fact("Each member has one vote; in the event of an equality of votes, the Governor has a second or casting "
              "vote", MP_OVERVIEW)])
Q(T, "Policy stance", "Advanced",
  "At its meeting of 5–7 October 2026, what stance did the MPC adopt, and how did members vote on it?",
  ["Calibrated tightening; two members preferred to retain the neutral stance",
   "Neutral; all members voted unanimously for it",
   "Accommodative; two members preferred a neutral stance",
   "Withdrawal of accommodation; one member dissented"],
  concept="Recent change in monetary policy stance",
  explanation="In October 2026 the MPC unanimously raised the policy repo rate by 25 bps and changed its stance to "
              "'calibrated tightening'. Two external members, Dr. Nagesh Kumar and Prof. Ram Singh, preferred to "
              "keep the neutral stance. The SDF rate became 5.25% and the MSF rate and Bank Rate 5.75%.",
  steps=["Rate decision: unanimous 25 bps hike", "Stance: neutral → calibrated tightening",
         "Two members preferred to retain neutral"],
  why="The earlier stance was neutral; accommodative and 'withdrawal of accommodation' are older stances.",
  current=ca("2026-10-07"),
  facts=[fact("MPC (Oct 5-7, 2026): stance changed to calibrated tightening; Dr. Nagesh Kumar and Prof. Ram Singh "
              "preferred retaining the neutral stance; SDF 5.25%, MSF and Bank Rate 5.75%", MPC_OCT26)])

# Policy corridor in force from 7 October 2026 (MPC resolution, prid=63742; also RBI home page on 2026-11-05)
REPO, SDF, MSF, BANK_RATE, FRRR = F(550, 100), F(525, 100), F(575, 100), F(575, 100), F(335, 100)
assert SDF == REPO - F(25, 100) and MSF == REPO + F(25, 100) == BANK_RATE
CORRIDOR = ca("2026-10-07")

# ================================================================= 6. Reverse Repo Rate (1 / 1 / 1)
T = "Reverse Repo Rate"
Q(T, "Reverse repo and SDF", "Basic",
  "What is the key difference between RBI's Standing Deposit Facility (SDF) and the fixed rate reverse repo?",
  ["The SDF absorbs liquidity without RBI having to give collateral",
   "The SDF lends money to banks against government securities",
   "The SDF is available only to non-bank financial companies",
   "The SDF rate is always fixed at 3.35%"],
  concept="Standing Deposit Facility",
  explanation="Under a reverse repo, RBI absorbs liquidity by giving government securities as collateral. The SDF, "
              "operationalised on 8 April 2022 under powers added to Section 17 of the RBI Act in 2018, lets RBI "
              "absorb liquidity without collateral. It replaced the fixed rate reverse repo as the floor of the LAF "
              "corridor; the fixed rate reverse repo rate was retained at 3.35%.",
  steps=["Reverse repo: RBI borrows against collateral", "SDF: RBI accepts deposits with no collateral"],
  why="Lending against securities is the repo/MSF; the SDF is for LAF participants (banks), and 3.35% is the "
      "fixed rate reverse repo rate, not the SDF rate.",
  facts=[fact("SDF operationalised April 8, 2022 as the floor of the LAF corridor; an uncollateralised liquidity "
              "absorption tool; fixed rate reverse repo retained at 3.35%", SDF_PR)])
Q(T, "Reverse repo and SDF", "Intermediate",
  "Following the MPC decision of 7 October 2026, the Standing Deposit Facility rate, which forms the floor of the "
  "LAF corridor, is:",
  ["5.00%", "5.25%", "5.50%", "5.75%"],
  answer="B",
  concept="Floor of the LAF corridor",
  explanation="The SDF rate is set 25 bps below the policy repo rate. With the repo rate raised to 5.50% on "
              "7 October 2026, the SDF rate is 5.25%; the MSF rate and Bank Rate (the ceiling) are 5.75%.",
  steps=["Repo = 5.50%", "SDF = repo − 0.25 = 5.25%"],
  why="5.00% was the SDF before the October 2026 hike; 5.50% is the repo rate; 5.75% is the MSF/Bank Rate.",
  current=CORRIDOR,
  facts=[fact("Policy rates after Oct 7, 2026: repo 5.50%, SDF 5.25%, MSF 5.75%, Bank Rate 5.75%", MPC_OCT26),
         fact("SDF is set 25 basis points below the policy repo rate", MP_OVERVIEW)])

amount = 500 * 10**7   # ₹500 crore in rupees
sdf_day = amount * SDF / 100 / 365
frrr_day = amount * FRRR / 100 / 365
gain_lakh = (sdf_day - frrr_day) / 10**5
assert round(float(sdf_day) / 1e5, 2) == 7.19 and round(float(frrr_day) / 1e5, 2) == 4.59
assert round(float(gain_lakh), 2) == 2.60
Q(T, "Reverse repo and SDF", "Advanced",
  "A bank has surplus funds of ₹500 crore overnight. It can place them with RBI either under the SDF or under the "
  "fixed rate reverse repo. Using the rates on RBI's website in November 2026, how much more interest (approx.) does "
  "the bank earn for one day by choosing the SDF? (Use a 365-day year.)",
  ["₹2.60 lakh", "₹4.59 lakh", "₹7.19 lakh", "₹26.03 lakh"],
  answer="A",
  concept="SDF versus fixed rate reverse repo",
  explanation="SDF rate = 5.25% and fixed rate reverse repo = 3.35%. Daily interest = principal × rate ÷ 365. SDF: "
              "500 crore × 5.25% ÷ 365 ≈ ₹7.19 lakh. Reverse repo: 500 crore × 3.35% ÷ 365 ≈ ₹4.59 lakh. Extra "
              "= 500 crore × 1.90% ÷ 365 ≈ ₹2.60 lakh. This is why the SDF, not the reverse repo, is the effective "
              "floor of the corridor.",
  steps=["Rate gap = 5.25 − 3.35 = 1.90%", "500 crore × 1.90% = ₹9.5 crore a year",
         "₹9.5 crore ÷ 365 ≈ ₹2.60 lakh a day"],
  why="₹4.59 lakh and ₹7.19 lakh are the full daily interest under each facility; ₹26.03 lakh misplaces the "
      "decimal.",
  computed=True, current=CORRIDOR,
  facts=[fact("SDF 5.25% and fixed reverse repo rate 3.35% (RBI home page, read 2026-11-05)", RBI_HOME),
         fact("SDF 5.25% after the October 7, 2026 MPC decision", MPC_OCT26)])

# ================================================================= 7. CRR (1 / 2 / 1)
T = "CRR"
Q(T, "CRR concept", "Basic",
  "The Cash Reserve Ratio (CRR) is the share of which liabilities of a bank that must be kept as a cash balance "
  "with RBI?",
  ["Net demand and time liabilities (NDTL)", "Total advances", "Paid-up capital and reserves",
   "Risk-weighted assets"],
  concept="Cash Reserve Ratio",
  explanation="CRR is the share of a bank's net demand and time liabilities that it must keep as a cash balance "
              "with RBI. It is a monetary policy instrument: a cut releases lendable funds, a rise absorbs them.",
  steps=["CRR base = NDTL", "Kept as cash balance with RBI"],
  why="Advances, capital and risk-weighted assets are bases for other ratios (credit-deposit ratio, CRAR).",
  facts=[fact("CRR is the share of net demand and time liabilities that banks must maintain as cash with RBI",
              MP_OVERVIEW)])
Q(T, "CRR value", "Intermediate",
  "After RBI's phased reduction announced in June 2025, the Cash Reserve Ratio has been ____ of NDTL from the "
  "reporting fortnight beginning 29 November 2025.",
  ["3.00%", "3.25%", "3.50%", "4.00%"],
  answer="A",
  concept="Current CRR",
  explanation="On 6 June 2025 RBI announced a 100 bps CRR cut in four equal steps: 3.75% (from 6 September 2025), "
              "3.50% (4 October), 3.25% (1 November) and 3.00% from the fortnight beginning 29 November 2025. RBI's "
              "website shows CRR at 3.00% in November 2026.",
  steps=["Start: 4.00%", "Four cuts of 25 bps = 100 bps", "Final: 3.00% from 29 November 2025"],
  why="3.25% and 3.50% were intermediate steps; 4.00% was the level before the cuts.",
  current=ca("2025-11-29"),
  facts=[fact("CRR cut in four 25 bps steps to 3.00% of NDTL from the fortnight beginning November 29, 2025",
              CRR_CUT),
         fact("CRR 3.00% (RBI home page, read 2026-11-05)", RBI_HOME)])
Q(T, "CRR concept", "Intermediate",
  "Scheduled commercial banks maintain the Cash Reserve Ratio with RBI under which provision?",
  ["Section 42 of the RBI Act, 1934", "Section 24 of the Banking Regulation Act, 1949",
   "Section 45ZB of the RBI Act, 1934", "Section 17 of the Banking Regulation Act, 1949"],
  concept="Legal basis of CRR",
  explanation="Under Section 42 of the RBI Act, every scheduled bank must maintain a minimum cash balance with RBI "
              "as CRR. SLR, by contrast, is prescribed under Section 24 of the Banking Regulation Act.",
  steps=["CRR → Section 42, RBI Act", "SLR → Section 24, BR Act"],
  why="Section 24 of the BR Act is for SLR; Section 45ZB of the RBI Act sets up the MPC; Section 17 of the BR Act "
      "deals with reserve funds.",
  facts=[fact("Under Section 42 of the RBI Act each scheduled commercial bank has to maintain a minimum cash balance "
              "with RBI as CRR", EXPLAIN_NOTES)])

ndtl = 80000
before, after = ndtl * 4 // 100, ndtl * 3 // 100
assert (before, after, before - after) == (3200, 2400, 800)
Q(T, "CRR value", "Advanced",
  "A bank has net demand and time liabilities of ₹80,000 crore. How much cash was released for this bank when CRR "
  "moved from its pre-September 2025 level to the current level of 3.00% of NDTL?",
  ["₹200 crore", "₹800 crore", "₹2,400 crore", "₹3,200 crore"],
  answer="B",
  concept="Computing CRR requirements",
  explanation="Before September 2025 CRR was 4.00%; after the four 25 bps cuts it is 3.00%. Requirement at 4% = "
              "80,000 × 4% = ₹3,200 crore; at 3% = ₹2,400 crore. Cash released = 3,200 − 2,400 = ₹800 crore.",
  steps=["At 4%: 80,000 × 0.04 = ₹3,200 crore", "At 3%: 80,000 × 0.03 = ₹2,400 crore",
         "Released = ₹800 crore"],
  why="₹200 crore is a single 25 bps step; ₹2,400 and ₹3,200 crore are the requirements themselves.",
  computed=True, current=ca("2025-11-29"),
  facts=[fact("CRR reduced by 100 bps in four steps to 3.0% of NDTL from November 29, 2025", CRR_CUT)])

# ================================================================= 8. SLR (1 / 2 / 1)
T = "SLR"
Q(T, "SLR concept", "Basic",
  "In which form can banks maintain their Statutory Liquidity Ratio (SLR)?",
  ["Cash, gold and unencumbered approved (government) securities", "Only cash balances kept with RBI",
   "Corporate bonds and listed equity shares", "Deposits placed with foreign banks abroad"],
  concept="Statutory Liquidity Ratio",
  explanation="SLR is the share of NDTL that banks must hold in liquid assets: cash, gold and unencumbered "
              "approved securities, mainly government securities. Unlike CRR, it is held by the bank itself, not "
              "as a balance with RBI.",
  steps=["SLR assets = cash + gold + approved (government) securities"],
  why="Balances with RBI are CRR; corporate bonds, equities and foreign deposits are not SLR assets.",
  facts=[fact("SLR is the share of liabilities that banks must hold in specified assets such as government "
              "securities, cash and gold", MP_OVERVIEW)])
Q(T, "SLR value", "Intermediate",
  "What is the current Statutory Liquidity Ratio prescribed for scheduled commercial banks?",
  ["18.00% of NDTL", "19.50% of NDTL", "21.00% of NDTL", "23.00% of NDTL"],
  concept="Current SLR",
  explanation="SLR was reduced by 25 bps every quarter from 19.50% and reached 18.00% of NDTL from 11 April 2020. "
              "RBI's website shows SLR at 18.00% in November 2026.",
  steps=["Recall: SLR = 18% since 11 April 2020 (unchanged)"],
  why="19.50% was the starting point of the 2019-20 glide path; 21% and 23% are older levels.",
  current=ca("2020-04-11"),
  facts=[fact("SLR has been reduced to 18 per cent of NDTL from April 11, 2020", SLR_2020),
         fact("SLR 18.00% (RBI home page, read 2026-11-05)", RBI_HOME)])
Q(T, "SLR concept", "Intermediate",
  "The Statutory Liquidity Ratio is prescribed by RBI under which provision?",
  ["Section 24 of the Banking Regulation Act, 1949", "Section 42 of the RBI Act, 1934",
   "Section 22 of the RBI Act, 1934", "Section 35A of the Banking Regulation Act, 1949"],
  concept="Legal basis of SLR",
  explanation="SLR is prescribed under Section 24 of the Banking Regulation Act; RBI's SLR notification is issued "
              "under Section 24(2A). CRR, in contrast, is under Section 42 of the RBI Act.",
  steps=["SLR → Section 24 (2A), BR Act"],
  why="Section 42 of the RBI Act is for CRR; Section 22 is for note issue; Section 35A is RBI's power to give "
      "directions.",
  facts=[fact("SLR notification issued under Section 24(2A) of the Banking Regulation Act; banks to hold SLR assets "
              "of 18 per cent of NDTL", SLR_2020)])

ndtl = 50000
crr_amt, slr_amt = ndtl * 3 // 100, ndtl * 18 // 100
assert (crr_amt, slr_amt, crr_amt + slr_amt) == (1500, 9000, 10500)
Q(T, "SLR value", "Advanced",
  "A bank's NDTL is ₹50,000 crore. At the current CRR and SLR, how much must it hold in total as CRR balance with RBI "
  "plus SLR assets?",
  ["₹9,000 crore", "₹10,000 crore", "₹10,500 crore", "₹11,500 crore"],
  answer="C",
  concept="Computing reserve requirements",
  explanation="CRR = 3% of 50,000 = ₹1,500 crore (cash with RBI). SLR = 18% of 50,000 = ₹9,000 crore (in cash, "
              "gold or approved securities). Total = ₹10,500 crore.",
  steps=["CRR: 50,000 × 3% = ₹1,500 crore", "SLR: 50,000 × 18% = ₹9,000 crore", "Total = ₹10,500 crore"],
  why="₹9,000 crore is SLR alone; ₹10,000 crore takes 20%; ₹11,500 crore uses the old 5% CRR.",
  computed=True, current=ca("2025-11-29"),
  facts=[fact("CRR 3.00% and SLR 18.00% (RBI home page, read 2026-11-05)", RBI_HOME)])

# ================================================================= 9. Bank Rate (1 / 1 / 1)
T = "Bank Rate"
Q(T, "Bank rate and MSF", "Basic",
  "In RBI's current operating framework, the Bank Rate is aligned with which rate?",
  ["Marginal Standing Facility (MSF) rate", "Standing Deposit Facility (SDF) rate", "Policy repo rate",
   "Fixed rate reverse repo rate"],
  concept="Bank Rate",
  explanation="The Bank Rate is aligned with the MSF rate and changes automatically when the MSF rate changes. Both "
              "are 25 bps above the policy repo rate and form the ceiling of the LAF corridor.",
  steps=["Bank Rate = MSF rate = repo + 25 bps"],
  why="The SDF is the floor, the repo is the middle, and the fixed reverse repo is a residual rate.",
  facts=[fact("Bank Rate is aligned with the MSF rate and changes automatically as and when the MSF rate changes",
              MP_OVERVIEW)])
Q(T, "Bank rate and MSF", "Intermediate",
  "For what purpose is the Bank Rate mainly used at present?",
  ["As the reference for penal interest on shortfalls in CRR and SLR",
   "As the rate at which RBI absorbs surplus liquidity from banks",
   "As the minimum rate banks can charge on loans",
   "As the interest rate paid on savings deposits"],
  concept="Use of the Bank Rate",
  explanation="The Bank Rate acts as the penal rate charged on banks for shortfalls in meeting reserve "
              "requirements (CRR and SLR). It is aligned with the MSF rate.",
  steps=["Bank Rate → penal rate for CRR/SLR shortfalls"],
  why="Liquidity absorption is through SDF/reverse repo; lending rates are linked to EBLR/MCLR; savings rates are "
      "deregulated.",
  facts=[fact("Bank Rate acts as the penal rate charged on banks for shortfalls in meeting their reserve "
              "requirements (CRR and SLR)", MP_OVERVIEW)])

next_repo = REPO + F(25, 100)
assert next_repo + F(25, 100) == F(600, 100)
Q(T, "Bank rate and MSF", "Advanced",
  "The Bank Rate is 5.75% after the MPC decision of 7 October 2026. If the MPC raises the policy repo rate by a "
  "further 25 basis points and keeps the corridor unchanged, what will the Bank Rate become?",
  ["5.75%", "6.00%", "6.25%", "5.50%"],
  answer="B",
  concept="Linkage between repo, MSF and Bank Rate",
  explanation="Repo is 5.50% now. A 25 bps hike takes it to 5.75%. The MSF rate is repo + 25 bps = 6.00%, and the "
              "Bank Rate, aligned with the MSF, also becomes 6.00%. (The SDF would move to 5.50%.)",
  steps=["New repo = 5.50 + 0.25 = 5.75%", "MSF = 5.75 + 0.25 = 6.00%", "Bank Rate = MSF = 6.00%"],
  why="5.75% is the current Bank Rate (or the new repo); 6.25% double-counts the hike; 5.50% is today's repo.",
  computed=True, current=CORRIDOR,
  facts=[fact("Bank Rate 5.75%, MSF 5.75%, repo 5.50% after the October 7, 2026 MPC decision", MPC_OCT26),
         fact("MSF is set 25 bps above the repo rate; Bank Rate is aligned with the MSF rate", MP_OVERVIEW)])

# ================================================================= 10. Inflation (2 / 3 / 2)
T = "Inflation"
Q(T, "CPI and WPI", "Basic",
  "Which office compiles and releases the Wholesale Price Index (WPI) in India?",
  ["Office of the Economic Adviser, DPIIT, Ministry of Commerce and Industry",
   "National Statistics Office, Ministry of Statistics and Programme Implementation",
   "Reserve Bank of India", "Labour Bureau, Ministry of Labour and Employment"],
  concept="Price indices in India",
  explanation="WPI is compiled by the Office of the Economic Adviser, Department for Promotion of Industry and "
              "Internal Trade (DPIIT). The all-India CPI is compiled by the National Statistics Office (MoSPI); the "
              "Labour Bureau compiles CPI for industrial workers.",
  steps=["WPI → Office of the Economic Adviser, DPIIT", "CPI → NSO, MoSPI"],
  why="NSO compiles CPI; RBI uses CPI for targeting but does not compile it; the Labour Bureau compiles CPI-IW.",
  facts=[fact("The new WPI series (base 2022-23) was released by the Office of the Economic Adviser, DPIIT", WPI_PIB2)])
Q(T, "Inflation targeting", "Basic",
  "What is India's inflation target under the flexible inflation targeting framework?",
  ["4% CPI inflation with a tolerance band of 2% to 6%", "4% WPI inflation with a band of 2% to 6%",
   "2% CPI inflation with a band of 1% to 3%", "6% CPI inflation with a band of 4% to 8%"],
  concept="Flexible inflation targeting",
  explanation="The Central Government, in consultation with RBI, has set the target at 4% CPI (combined) inflation "
              "with a tolerance band of +/- 2% (i.e. 2% to 6%). The target is defined on CPI, not WPI.",
  steps=["Index: CPI (combined)", "Target 4%, band 2–6%"],
  why="WPI is not the target index; 2% and 6% are the band limits, not the target.",
  facts=[fact("Inflation target of 4% CPI inflation with a tolerance band of 2% to 6%", MP_OVERVIEW)])
Q(T, "CPI and WPI", "Intermediate",
  "MoSPI revised the base year of the Consumer Price Index in 2026. What is the base year of the new CPI series, "
  "whose inflation data begins with January 2026?",
  ["2024", "2012", "2022-23", "2011-12"],
  concept="New CPI series",
  explanation="MoSPI moved CPI from base 2012=100 to base 2024=100. Inflation under the new series starts with "
              "January 2026; the 2012 series ran till December 2025. Weights come from the Household Consumption "
              "Expenditure Survey 2023-24.",
  steps=["Old CPI base: 2012", "New CPI base: 2024 (first release February 2026)"],
  why="2012 is the old CPI base; 2022-23 is the new WPI base; 2011-12 is the old WPI base.",
  current=ca("2026-02-12"),
  facts=[fact("MoSPI revised the CPI base year from 2012=100 to 2024=100; new series inflation begins January 2026",
              CPI_PIB)])
Q(T, "CPI and WPI", "Intermediate",
  "The new series of the Wholesale Price Index, released on 15 June 2026, has which base year?",
  ["2011-12", "2022-23", "2024", "2017-18"],
  answer="B",
  concept="New WPI series",
  explanation="The Office of the Economic Adviser revised WPI's base year from 2011-12 to 2022-23 and released the "
              "new series on 15 June 2026, along with new Producer Price Indices. The number of items rose from 697 "
              "to 957, and the old series was discontinued.",
  steps=["Old WPI base: 2011-12", "New WPI base: 2022-23 (released 15 June 2026)"],
  why="2011-12 is the discontinued base; 2024 is the new CPI base; 2017-18 was never a WPI base.",
  current=ca("2026-06-15"),
  facts=[fact("Base year of WPI revised from 2011-12 to 2022-23", WPI_PIB),
         fact("New WPI series (base 2022-23) released on 15 June 2026; items increased from 697 to 957", WPI_PIB2)])
Q(T, "Inflation targeting", "Intermediate",
  "In March 2026 the Government retained the inflation target and tolerance band for the next five years. Until "
  "when is the current target period?",
  ["31 March 2031", "31 March 2026", "31 March 2029", "31 December 2030"],
  concept="Renewal of the inflation target",
  explanation="The 4% (2–6%) target was first set for 5 August 2016 to 31 March 2021, retained for 1 April 2021 to "
              "31 March 2026, and on 25 March 2026 retained again for 1 April 2026 to 31 March 2031.",
  steps=["2016–2021, 2021–2026, 2026–2031", "Current period ends 31 March 2031"],
  why="31 March 2026 was the end of the previous period; the other dates do not match a five-year period.",
  current=ca("2026-04-01"),
  facts=[fact("On March 25, 2026 the Government retained the inflation target and band for April 1, 2026 to "
              "March 31, 2031", MP_OVERVIEW)])

quarters = [F(64, 10), F(61, 10), F(58, 10), F(65, 10), F(62, 10)]
run = best = 0
for x in quarters:
    run = run + 1 if x > 6 else 0
    best = max(best, run)
assert best == 2
Q(T, "Inflation targeting", "Advanced",
  "Average CPI inflation in five consecutive quarters was 6.4%, 6.1%, 5.8%, 6.5% and 6.2%. Has RBI failed to meet "
  "the inflation target under the RBI Act framework?",
  ["No; inflation stayed above 6% for at most two consecutive quarters",
   "Yes; inflation was above 6% in four of the five quarters",
   "Yes; any single quarter above 6% is a failure",
   "No; failure arises only if inflation exceeds 8%"],
  concept="Definition of failure to meet the target",
  explanation="Failure means average inflation above the upper tolerance level (6%) or below the lower level (2%) "
              "for any three consecutive quarters. Here the run above 6% is 6.4, 6.1 (two quarters), broken by "
              "5.8, followed by 6.5, 6.2 (two quarters). There is no run of three, so there is no failure. If there "
              "were, RBI would have to report the reasons, remedial actions and time frame to the Government.",
  steps=["Mark quarters above 6%: Q1, Q2, Q4, Q5", "Q3 = 5.8% breaks the run", "Longest run = 2 < 3 → no failure"],
  why="The count of quarters does not matter, only three in a row; one quarter is not enough; 8% is not a "
      "threshold.",
  computed=True,
  facts=[fact("Failure: average inflation above the upper tolerance level or below the lower level for any three "
              "consecutive quarters", MP_OVERVIEW)])
Q(T, "CPI and WPI", "Advanced",
  "Consider the following statements about the price indices revised in 2026:\nI. The new WPI series uses Gross "
  "Value of Output for weights instead of Net Traded Value.\nII. Weights for the new CPI (2024=100) are derived from "
  "the Household Consumption Expenditure Survey 2023-24.\nIII. The new CPI follows the COICOP 2018 classification.\n"
  "Which of the above is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I only"],
  concept="Methodology of the new CPI and WPI",
  explanation="All three are correct. WPI 2022-23 uses Gross Value of Output for weights (the 2011-12 series used "
              "Net Traded Value = GVO + imports − exports). CPI 2024 draws weights from HCES 2023-24 and follows "
              "COICOP 2018 (12 divisions).",
  steps=["I: correct (GVO weights)", "II: correct (HCES 2023-24)", "III: correct (COICOP 2018)"],
  current=ca("2026-06-15"),
  facts=[fact("WPI 2022-23 weights use Gross Value of Output instead of Net Traded Value", WPI_PIB2),
         fact("CPI 2024 series: weights from HCES 2023-24; classification follows COICOP 2018", CPI_PIB)])

# ================================================================= 11. NPA (3 / 3 / 3)
T = "NPA"
Q(T, "Classification", "Basic",
  "A term loan becomes a non-performing asset (NPA) when interest or an instalment of principal remains overdue "
  "for more than:",
  ["90 days", "30 days", "60 days", "180 days"],
  concept="Definition of NPA",
  explanation="Under RBI's prudential norms, a term loan is an NPA if interest and/or an instalment of principal "
              "remains overdue for more than 90 days. Accounts overdue for shorter periods are tagged as Special "
              "Mention Accounts (SMA).",
  steps=["NPA trigger for term loans: overdue > 90 days"],
  why="30 and 60 days relate to SMA-1/SMA-2 tagging; 180 days was an old norm before the 90-day rule.",
  facts=[fact("An NPA is a loan where interest and/or instalment of principal remains overdue for more than 90 days "
              "in respect of a term loan", IRAC_MD)])
Q(T, "Resolution and IBC", "Basic",
  "Within how many days from the admission of the application must a corporate insolvency resolution process (CIRP) "
  "under the Insolvency and Bankruptcy Code normally be completed?",
  ["180 days", "90 days", "270 days", "365 days"],
  concept="CIRP timeline under IBC",
  explanation="Section 12 of the IBC requires the CIRP to be completed within 180 days of admission. The "
              "Adjudicating Authority may grant a one-time extension of 90 days, and the whole process including "
              "litigation must end within 330 days.",
  steps=["Base period: 180 days", "One-time extension: 90 days", "Outer limit: 330 days"],
  why="90 days is the extension; 270 days is base plus extension; 365 days is not the statutory limit.",
  facts=[fact("CIRP shall be completed within 180 days of admission; one-time extension of 90 days; must conclude "
              "within 330 days", IBBI_FAQ)])
Q(T, "SARFAESI", "Basic",
  "Under Section 13(2) of the SARFAESI Act, 2002, how many days' notice must a secured creditor give the borrower "
  "before taking measures to enforce the security?",
  ["60 days", "30 days", "90 days", "15 days"],
  concept="Enforcement under SARFAESI",
  explanation="The SARFAESI Act lets secured creditors enforce security without court intervention. Before taking "
              "measures under Section 13(4), such as taking possession, the creditor must give the borrower 60 "
              "days' notice under Section 13(2). The borrower can appeal to the Debt Recovery Tribunal under "
              "Section 17.",
  steps=["Section 13(2) notice = 60 days", "Then measures under Section 13(4)"],
  why="30, 90 and 15 days are not the Section 13(2) notice period.",
  facts=[fact("Under section 13(2) the secured creditor must serve 60 days notice before taking measures under "
              "section 13(4)", SARFAESI_RBI)])
Q(T, "Classification", "Intermediate",
  "An asset that has remained in the substandard category for 12 months is classified as:",
  ["Doubtful asset", "Loss asset", "Special Mention Account", "Standard asset"],
  concept="Asset classification",
  explanation="A substandard asset is one that has been an NPA for up to 12 months. Once it has remained "
              "substandard for 12 months, it becomes a doubtful asset. A loss asset is one where loss has been "
              "identified by the bank or auditors but not written off.",
  steps=["NPA ≤ 12 months → substandard", "Substandard for 12 months → doubtful"],
  why="Loss classification depends on identified loss, not ageing; SMA and standard are pre-NPA categories.",
  facts=[fact("Substandard asset: NPA for a period ≤ 12 months; doubtful asset: remained in the substandard category "
              "for 12 months", IRAC_MD)])
Q(T, "Resolution and IBC", "Intermediate",
  "What is the minimum amount of default for initiating a corporate insolvency resolution process under the IBC?",
  ["₹1 crore", "₹1 lakh", "₹10 lakh", "₹50 crore"],
  concept="Threshold for CIRP",
  explanation="The minimum default for initiating CIRP was ₹1 lakh. The Government raised it to ₹1 crore by "
              "notification dated 24 March 2020.",
  steps=["Earlier threshold: ₹1 lakh", "From 24 March 2020: ₹1 crore"],
  why="₹1 lakh is the old threshold; ₹10 lakh and ₹50 crore have no basis.",
  current=ca("2020-03-24"),
  facts=[fact("Minimum default for CIRP increased from ₹1 lakh to ₹1 crore by notification dated 24 March 2020",
              IBBI_FAQ)])
Q(T, "SARFAESI", "Intermediate",
  "Asset Reconstruction Companies (ARCs) registered with RBI under Section 3 of the SARFAESI Act must maintain a "
  "minimum Net Owned Fund of:",
  ["₹300 crore", "₹100 crore", "₹2 crore", "₹500 crore"],
  concept="Regulation of ARCs",
  explanation="ARCs buy stressed assets from lenders and are registered and regulated by RBI under the SARFAESI "
              "Act. RBI raised the minimum NOF from ₹100 crore to ₹300 crore on an ongoing basis (for new "
              "registrations from 11 October 2022, with a glide path for existing ARCs).",
  steps=["ARC NOF: earlier ₹100 crore", "Now ₹300 crore on an ongoing basis"],
  why="₹100 crore is the earlier requirement; ₹2 crore and ₹500 crore are not ARC norms.",
  current=ca("2022-10-11"),
  facts=[fact("An ARC needs a minimum net owned fund of ₹300 crore and thereafter on an ongoing basis", ARC_MD)])
Q(T, "Classification", "Advanced",
  "A farmer took a crop loan for sugarcane, a long-duration crop. The instalment due at harvest has remained overdue "
  "for one crop season. Under RBI's norms, how should the bank classify the loan?",
  ["As an NPA, because for long-duration crops one crop season overdue is enough",
   "As standard, because farm loans become NPA only after two crop seasons",
   "As standard until it is overdue for more than 90 days from the next harvest",
   "As a loss asset, because agricultural loans are unsecured"],
  concept="NPA norms for agricultural loans",
  explanation="For agricultural loans, the NPA test is linked to crop seasons: overdue for two crop seasons for "
              "short-duration crops and one crop season for long-duration crops (those with a season longer than "
              "one year, like sugarcane). So the sugarcane loan is an NPA.",
  steps=["Sugarcane = long-duration crop", "Rule: one crop season overdue → NPA",
         "Loan has been overdue one season → NPA"],
  why="Two crop seasons applies to short-duration crops; the 90-day rule does not govern crop loans; loss "
      "classification needs identified loss.",
  facts=[fact("Agricultural loans: NPA if overdue for two crop seasons (short duration crops) or one crop season "
              "(long duration crops)", IRAC_MD)])

out_lakh, security = 100, 70
unsecured = out_lakh - security
provision = unsecured * 100 // 100 + security * 40 // 100
assert (unsecured, provision) == (30, 58)
Q(T, "Classification", "Advanced",
  "A loan of ₹100 lakh has been in the doubtful category for two years. The realisable value of the security is "
  "₹70 lakh. Under RBI's current provisioning norms (Directions, 2025), what is the minimum provision required?",
  ["₹28 lakh", "₹40 lakh", "₹58 lakh", "₹100 lakh"],
  answer="C",
  concept="Provisioning for doubtful assets",
  explanation="For doubtful assets, the unsecured portion (not covered by the realisable value of security) needs "
              "100% provision. The secured portion needs 25% (doubtful up to 1 year), 40% (1–3 years) or 100% "
              "(over 3 years). Unsecured = 100 − 70 = 30 → ₹30 lakh. Secured (doubtful for 2 years) = 70 × 40% = "
              "₹28 lakh. Total = ₹58 lakh. Note: from 1 April 2027 these norms are replaced by RBI's expected "
              "credit loss framework.",
  steps=["Unsecured portion = 100 − 70 = 30 → 100% = ₹30 lakh", "Secured portion: 70 × 40% = ₹28 lakh",
         "Total provision = ₹58 lakh"],
  why="₹28 lakh ignores the unsecured portion; ₹40 lakh applies 40% to the whole loan; ₹100 lakh treats it as a "
      "loss asset.",
  computed=True, current=ca("2025-11-28", "2027-03-31"),
  facts=[fact("Doubtful assets: 100% of the unsecured portion; secured portion 25% (up to 1 year), 40% (1-3 years), "
              "100% (more than 3 years)", IRAC_MD),
         fact("ECL-based Asset Classification, Provisioning and Income Recognition Directions, 2026 take effect from "
              "April 1, 2027", ECL_MD)])

due = dt.date(2026, 3, 31)
sma1, sma2, npa = (due + dt.timedelta(days=d) for d in (30, 60, 90))
assert (sma1, sma2, npa) == (dt.date(2026, 4, 30), dt.date(2026, 5, 30), dt.date(2026, 6, 29))
Q(T, "Classification", "Advanced",
  "An instalment of a term loan was due on 31 March 2026 and remains unpaid. Under RBI's day-end classification "
  "process, on which date will the account be classified as an NPA if nothing is paid?",
  ["29 June 2026", "30 May 2026", "30 June 2026", "1 July 2026"],
  answer="A",
  concept="SMA and NPA tagging by days past due",
  explanation="Following RBI's illustration: an amount due on 31 March is tagged SMA-1 on completion of 30 days "
              "(30 April), SMA-2 on completion of 60 days (30 May) and NPA on completion of 90 days, i.e. in the "
              "day-end process of 29 June. (April has 30 days, May 31, so 31 March + 90 days = 29 June.)",
  steps=["31 Mar + 30 days = 30 Apr → SMA-1", "31 Mar + 60 days = 30 May → SMA-2",
         "31 Mar + 90 days = 29 Jun → NPA"],
  why="30 May is the SMA-2 date; 30 June and 1 July count one or two days too many.",
  computed=True,
  facts=[fact("RBI illustration: due date March 31 → SMA-1 on April 30, SMA-2 on May 30, NPA on June 29 in the "
              "day-end process", IRAC_MD)])

# ================================================================= 12. Basel Norms (3 / 3 / 3)
T = "Basel Norms"
Q(T, "Capital adequacy", "Basic",
  "The Basel Committee on Banking Supervision, which frames the Basel norms, has its secretariat at:",
  ["The Bank for International Settlements, Basel", "The IMF, Washington DC", "The World Bank, Washington DC",
   "The European Central Bank, Frankfurt"],
  concept="Basel Committee on Banking Supervision",
  explanation="The BCBS was set up by the central bank Governors of the G10 countries at the end of 1974, after "
              "disruptions such as the failure of Bankhaus Herstatt. Its secretariat is at the Bank for "
              "International Settlements (BIS) in Basel, Switzerland.",
  steps=["BCBS → housed at BIS, Basel (est. end-1974)"],
  why="The IMF, World Bank and ECB are separate institutions.",
  facts=[fact("BCBS established by G10 central bank Governors at the end of 1974; secretariat at the BIS in Basel",
              BCBS_HIST)])
Q(T, "Capital adequacy", "Basic",
  "Under the Basel framework, Pillar 3 refers to:",
  ["Market discipline through disclosures", "Minimum capital requirements", "Supervisory review process",
   "Liquidity coverage"],
  concept="Three pillars of Basel",
  explanation="Basel II introduced three pillars, which Basel III strengthened: Pillar 1 minimum capital "
              "requirements, Pillar 2 supervisory review, and Pillar 3 market discipline through public "
              "disclosures.",
  steps=["Pillar 1: capital", "Pillar 2: supervisory review", "Pillar 3: market discipline"],
  why="Minimum capital is Pillar 1; supervisory review is Pillar 2; liquidity ratios are separate Basel III "
      "standards.",
  facts=[fact("Basel III revises and strengthens the three pillars of Basel II: minimum capital requirements, "
              "supervisory review and market discipline", BASEL3)])
Q(T, "Capital adequacy", "Basic",
  "What is the Capital Conservation Buffer (CCB) that commercial banks in India must maintain over the minimum "
  "capital requirement?",
  ["2.5% of risk-weighted assets, in CET1", "1% of risk-weighted assets, in Tier 2", "5.5% of total assets",
   "0.8% of risk-weighted assets, in AT1"],
  concept="Capital Conservation Buffer",
  explanation="Banks must hold a CCB of 2.5% of RWAs in the form of Common Equity Tier 1, over and above the minimum "
              "CET1 of 5.5%. CET1 plus CCB is therefore 8%, and total capital including CCB is 11.5%.",
  steps=["CCB = 2.5% of RWAs", "Must be met with CET1"],
  why="5.5% is the minimum CET1; 0.8% is SBI's D-SIB surcharge; Tier 2 cannot meet the CCB.",
  facts=[fact("Commercial banks: CET1 5.5%, CCB 2.5%, CET1 plus CCB 8%, total capital including CCB 11.5%",
              CAP_TABLE)])
Q(T, "Capital adequacy", "Intermediate",
  "What is the minimum total capital ratio, including the Capital Conservation Buffer, required of scheduled "
  "commercial banks in India?",
  ["9%", "10.5%", "11.5%", "15%"],
  answer="C",
  concept="Minimum CRAR in India",
  explanation="RBI requires a minimum total capital of 9% of RWAs (stricter than the Basel minimum of 8%), plus the "
              "2.5% CCB, giving 11.5%. Small Finance Banks and Payments Banks must keep a CRAR of 15%.",
  steps=["Minimum total capital = 9%", "Add CCB 2.5%", "Required = 11.5%"],
  why="9% excludes the CCB; 10.5% is the Basel global figure (8% + 2.5%); 15% applies to SFBs and Payments Banks.",
  facts=[fact("Commercial banks: total capital 9%, total capital including CCB (CRAR) 11.5%; SFBs and Payments Banks "
              "15%", CAP_TABLE)])
Q(T, "Leverage ratio", "Intermediate",
  "What is the minimum leverage ratio RBI prescribes for Domestic Systemically Important Banks (D-SIBs) and for "
  "other scheduled commercial banks respectively?",
  ["4% and 3.5%", "3% and 3%", "5% and 4%", "3.5% and 3%"],
  concept="Leverage ratio",
  explanation="The leverage ratio is Tier 1 capital divided by total exposure (on- and off-balance sheet). Since "
              "the quarter beginning 1 October 2019, RBI requires at least 4% for D-SIBs and 3.5% for other banks. "
              "Basel's own minimum is 3%.",
  steps=["D-SIBs: 4%", "Other SCBs: 3.5%"],
  why="3% is the Basel minimum (and the payments bank norm); the other pairs are not RBI's figures.",
  current=ca("2019-10-01", "2027-03-31"),
  facts=[fact("Minimum leverage ratio 4% for D-SIBs and 3.5% for other banks, effective from the quarter commencing "
              "October 1, 2019", LEV_2019)])
Q(T, "LCR and NSFR", "Intermediate",
  "How is the Net Stable Funding Ratio (NSFR) defined, and what minimum must banks in India maintain?",
  ["Available stable funding ÷ required stable funding; at least 100%",
   "High-quality liquid assets ÷ net cash outflows over 30 days; at least 100%",
   "Tier 1 capital ÷ total exposure; at least 3.5%",
   "Available stable funding ÷ total deposits; at least 75%"],
  concept="Net Stable Funding Ratio",
  explanation="NSFR = available stable funding ÷ required stable funding, to be at least 100% on an ongoing basis. "
              "It promotes stable funding over a one-year horizon; RBI's NSFR guidelines took effect on 1 October "
              "2021. The LCR, by contrast, compares HQLA with 30-day net cash outflows.",
  steps=["NSFR = ASF ÷ RSF ≥ 100%", "In force in India from 1 October 2021"],
  why="HQLA ÷ 30-day outflows is the LCR; Tier 1 ÷ exposure is the leverage ratio.",
  facts=[fact("NSFR is the amount of available stable funding relative to required stable funding; should be at "
              "least 100% on an ongoing basis", NSFR_2018),
         fact("NSFR guidelines came into effect from October 1, 2021", NSFR_2021)])

cet1, at1, t2, rwa = 600, 100, 200, 8000
cet1_r, t1_r, crar = (F(x * 100, rwa) for x in (cet1, cet1 + at1, cet1 + at1 + t2))
assert (cet1_r, t1_r, crar) == (F(75, 10), F(875, 100), F(1125, 100)) and crar < F(115, 10) and cet1_r < 8
Q(T, "Capital adequacy", "Advanced",
  "A scheduled commercial bank (not a D-SIB) has CET1 capital of ₹600 crore, Additional Tier 1 of ₹100 crore, Tier 2 "
  "of ₹200 crore and risk-weighted assets of ₹8,000 crore. Which statement is correct?",
  ["CRAR is 11.25%, which is short of the 11.5% required including CCB",
   "CRAR is 11.25%, which meets the requirement because the minimum is 9%",
   "CRAR is 8.75%, which is short of the 9% minimum",
   "CET1 is 7.5%, which meets the CET1 plus CCB requirement of 7%"],
  concept="Computing capital ratios",
  explanation="CET1 ratio = 600 ÷ 8,000 = 7.5%; Tier 1 = 700 ÷ 8,000 = 8.75%; CRAR = 900 ÷ 8,000 = 11.25%. "
              "Including the 2.5% CCB, RBI requires CRAR of 11.5% and CET1 of 8%, so the bank falls short on both, "
              "which will restrict its dividend payouts.",
  steps=["CET1 = 600/8,000 = 7.5%", "Tier 1 = 700/8,000 = 8.75%", "CRAR = 900/8,000 = 11.25% < 11.5%"],
  why="The 9% minimum ignores the CCB; 8.75% is the Tier 1 ratio, not CRAR; CET1 plus CCB is 8%, not 7%.",
  computed=True,
  facts=[fact("Commercial banks: CET1 5.5%, CCB 2.5%, CET1+CCB 8%, Tier 1 7%, total capital 9%, CRAR including "
              "CCB 11.5%", CAP_TABLE)])

deposits = 1000
old_out, new_out = deposits * F(5, 100), deposits * F(75, 1000)
assert (old_out, new_out, new_out - old_out) == (50, 75, 25)
Q(T, "LCR and NSFR", "Advanced",
  "A bank has ₹1,000 crore of stable retail deposits from customers who use internet and mobile banking. Under RBI's "
  "amended LCR rules effective 1 April 2026, by how much do the expected 30-day cash outflows on these deposits "
  "increase compared with the earlier rules?",
  ["₹25 crore", "₹50 crore", "₹75 crore", "₹125 crore"],
  answer="A",
  concept="LCR run-off rates for digitally enabled deposits",
  explanation="RBI's April 2025 circular added a 2.5 percentage point run-off for internet and mobile banking (IMB, "
              "including UPI) enabled retail deposits from 1 April 2026: stable deposits move from 5% to 7.5%, less "
              "stable from 10% to 12.5%. Earlier outflow = 1,000 × 5% = ₹50 crore; now 1,000 × 7.5% = ₹75 crore; "
              "increase = ₹25 crore. Higher outflows mean a bank needs more HQLA for the same LCR.",
  steps=["Old run-off 5%: ₹50 crore", "New run-off 7.5%: ₹75 crore", "Increase = ₹25 crore"],
  why="₹50 crore and ₹75 crore are the old and new outflows; ₹125 crore uses the less-stable 12.5% rate.",
  computed=True, current=ca("2026-04-01"),
  facts=[fact("IMB-enabled stable retail deposits: run-off raised from 5% to 7.5%; less stable from 10% to 12.5%; "
              "effective April 1, 2026", LCR_2025)])

sbi_req = F(55, 10) + F(25, 10) + F(8, 10)
assert sbi_req == F(88, 10)
Q(T, "Capital adequacy", "Advanced",
  "In RBI's 2025 list of Domestic Systemically Important Banks, SBI is in bucket 4. What is SBI's minimum CET1 "
  "requirement including the Capital Conservation Buffer and the D-SIB surcharge?",
  ["8.0% of RWAs", "8.6% of RWAs", "8.8% of RWAs", "9.0% of RWAs"],
  answer="C",
  concept="D-SIB additional CET1",
  explanation="Minimum CET1 is 5.5% and the CCB 2.5%, i.e. 8%. D-SIBs hold additional CET1 on top of the CCB: "
              "bucket 4 (SBI) 0.80%, bucket 2 (HDFC Bank) 0.40%, bucket 1 (ICICI Bank) 0.20%. SBI: 5.5 + 2.5 + 0.8 "
              "= 8.8%.",
  steps=["Base CET1 + CCB = 5.5 + 2.5 = 8.0%", "Bucket 4 surcharge = 0.80%", "Total = 8.8%"],
  why="8.0% omits the surcharge; 8.6% uses SBI's old 0.60% surcharge; 9.0% uses the bucket 5 rate of 1%.",
  computed=True, current=ca("2025-12-02"),
  facts=[fact("2025 D-SIB list: SBI bucket 4 (0.80%), HDFC Bank bucket 2 (0.40%), ICICI Bank bucket 1 (0.20%); "
              "additional CET1 over and above the CCB", DSIB_2025),
         fact("Minimum CET1 5.5% and CCB 2.5% for commercial banks", CAP_TABLE)])

# ================================================================= 13. Financial Inclusion (3 / 3 / 3)
T = "Financial Inclusion"
Q(T, "PMJDY and allied schemes", "Basic",
  "Pradhan Mantri Jan Dhan Yojana (PMJDY), the National Mission for Financial Inclusion, was launched on:",
  ["28 August 2014", "15 August 2014", "2 October 2014", "1 April 2015"],
  concept="PMJDY",
  explanation="PMJDY was launched on 28 August 2014 to give every unbanked person a basic bank account, along with "
              "access to credit, insurance and pension and financial literacy.",
  steps=["PMJDY launch date: 28 August 2014"],
  why="15 August 2014 is when the mission was announced from the Red Fort; the other dates are unrelated.",
  facts=[fact("PMJDY, the National Mission for Financial Inclusion, was launched on 28 August 2014", PMJDY_PIB)])
Q(T, "PMJDY and allied schemes", "Basic",
  "What is the maximum overdraft facility available to an eligible PMJDY account holder?",
  ["₹10,000", "₹5,000", "₹2,000", "₹50,000"],
  concept="PMJDY overdraft",
  explanation="Eligible PMJDY account holders can get an overdraft of up to ₹10,000. The limit was doubled from "
              "₹5,000 to ₹10,000 when the scheme was extended in 2018.",
  steps=["OD limit: ₹5,000 originally → ₹10,000 since 2018"],
  why="₹5,000 was the original limit; ₹2,000 and ₹50,000 are not PMJDY limits.",
  current=ca("2018-08-28"),
  facts=[fact("Overdraft facility up to ₹10,000 available to eligible PMJDY account holders", PMJDY_PIB)])
Q(T, "Business correspondents", "Basic",
  "In which year did RBI first permit banks to use Business Correspondents (BCs) and Business Facilitators as "
  "intermediaries to extend banking services?",
  ["2006", "2000", "2011", "2014"],
  concept="Business Correspondent model",
  explanation="RBI's circular of 25 January 2006 allowed banks to use intermediaries such as NGOs, MFIs and other "
              "civil society organisations as Business Facilitators and Business Correspondents to widen the "
              "reach of banking, especially in unbanked areas.",
  steps=["BC/BF model: RBI circular of January 2006"],
  why="2011 and 2014 relate to later financial inclusion drives (e.g. PMJDY in 2014), not the BC model's start.",
  facts=[fact("RBI circular of January 25, 2006 permitted banks to use BFs and BCs as intermediaries", BC_2006)])
Q(T, "PMJDY and allied schemes", "Intermediate",
  "Which of the following was a stated aim of PMJDY at its launch?",
  ["At least one basic bank account for every household", "A guaranteed pension for every adult",
   "A collateral-free business loan for every household", "A health insurance cover of ₹5 lakh for every family"],
  concept="Objectives of PMJDY",
  explanation="PMJDY aimed at universal access to banking, with at least one basic bank account for every "
              "household, plus financial literacy, access to credit, insurance and pension.",
  steps=["Core aim: universal banking access, one basic account per household"],
  why="Guaranteed pension is APY; collateral-free business loans are PMMY; ₹5 lakh health cover is a separate "
      "health scheme.",
  facts=[fact("PMJDY aimed at providing at least one basic bank account to every household, with financial "
              "literacy, access to credit, insurance and pension", PMJDY_DFS)])
Q(T, "Business correspondents", "Intermediate",
  "Under RBI's guidelines on the Business Correspondent model, who is responsible for the actions of a BC?",
  ["The bank that engages the BC", "The BC alone", "The customer who deals with the BC", "RBI"],
  concept="Liability in the BC model",
  explanation="A BC acts as the agent of the bank, so the bank remains fully responsible for the BC's acts and "
              "omissions. Banks must set cash-holding and transaction limits and ensure transactions are recorded "
              "in their books promptly.",
  steps=["BC = agent of the bank", "Principal (bank) is liable for the agent"],
  why="The BC is not a separate regulated entity, customers are not liable, and RBI is the regulator, not the "
      "principal.",
  facts=[fact("Banks will be fully responsible for the actions of the BCs and their retail outlets/sub-agents",
              BC_2010)])
Q(T, "Business correspondents", "Intermediate",
  "Which of the following was NOT envisaged as a service to be offered through Business Correspondents?",
  ["Accepting large NRE/NRO/FCNR(B) deposits", "Collecting small-value deposits",
   "Disbursing small-value credit and recovering it", "Receiving and delivering small-value remittances"],
  concept="Scope of BC services",
  explanation="BCs were allowed to identify borrowers, collect small deposits, disburse and recover small loans, "
              "sell micro-insurance, mutual fund and pension products and handle small remittances. The BC model "
              "is meant for small savings and loans for the unbanked, not for large non-resident deposits.",
  steps=["BC scope: small deposits, small credit, small remittances, third-party products",
         "Large NRE/NRO/FCNR(B) deposits are outside the model's purpose"],
  why="Small deposits, small credit and small remittances are all permitted BC activities.",
  facts=[fact("BCs permitted for small-value credit, collection of small deposits, sale of micro-insurance/MF/pension "
              "and small remittances", BC_2006),
         fact("The BC model is not intended for mobilising large NRE/NRO/FCNR(B) deposits", BC_MC)])
Q(T, "PMJDY and allied schemes", "Advanced",
  "A husband and wife each opened a PMJDY account three months ago and have operated them satisfactorily. Both now "
  "ask for the PMJDY overdraft. What is the correct position?",
  ["Neither is eligible yet; the OD needs six months of satisfactory operation and is for one person per household",
   "Both can get ₹10,000 each immediately",
   "Only the wife is eligible immediately because women get priority",
   "Both can get ₹5,000 each immediately because the household limit is ₹10,000"],
  concept="Eligibility for the PMJDY overdraft",
  explanation="The PMJDY overdraft (up to ₹10,000) is available to one account holder per household, and only "
              "after six months of satisfactory operation of the account, subject to the bank's eligibility "
              "criteria. Three months is too early, and in any case only one of them could get it.",
  steps=["Condition 1: six months of satisfactory operation — not met (3 months)",
         "Condition 2: one account holder per household",
         "→ Neither eligible now; later, only one of them"],
  why="The OD cannot be given to both spouses or split; there is no automatic priority that waives the six-month "
      "condition.",
  facts=[fact("PMJDY OD up to ₹10,000 available to one account holder per household after six months of "
              "satisfactory operation", PMJDY_PIB)])
Q(T, "Business correspondents", "Advanced",
  "Under RBI's original January 2006 guidelines, which of the following could be engaged as Business "
  "Correspondents?\nI. Post offices\nII. Section 25 (not-for-profit) companies\nIII. Individual petrol pump owners",
  ["I and II only", "I, II and III", "II and III only", "III only"],
  concept="Eligible BC entities",
  explanation="The 2006 guidelines allowed NGOs/MFIs set up under the Societies or Trust Acts, cooperative "
              "societies, Section 25 companies and post offices to act as BCs. Individuals such as retired bank "
              "employees, kirana and petrol pump owners and CSC operators were added in later expansions of the "
              "list.",
  steps=["2006 list: NGOs/MFIs, cooperative societies, Section 25 companies, post offices",
         "Individuals (e.g. petrol pump owners) came later"],
  facts=[fact("Initially eligible BCs: NGOs/MFIs under Societies/Trust Acts, cooperative societies, Section 25 "
              "companies, post offices; individuals such as petrol pump owners were permitted later", BC_ELIG)])
Q(T, "PMJDY and allied schemes", "Advanced",
  "Asha opened her PMJDY account on 10 May 2018 and Rahul opened his on 5 October 2019. Both hold RuPay debit cards. "
  "What accident insurance cover is attached to their accounts?",
  ["Asha ₹1 lakh; Rahul ₹2 lakh", "₹2 lakh each", "₹1 lakh each", "Asha ₹2 lakh; Rahul ₹1 lakh"],
  concept="RuPay accident cover under PMJDY",
  explanation="The accident insurance cover on the RuPay card was raised from ₹1 lakh to ₹2 lakh for PMJDY accounts "
              "opened after 28 August 2018. Asha's account (May 2018) predates the cut-off, so she has ₹1 lakh; "
              "Rahul's (October 2019) carries ₹2 lakh.",
  steps=["Cut-off: accounts opened after 28 August 2018 → ₹2 lakh", "Asha (10 May 2018): before → ₹1 lakh",
         "Rahul (5 Oct 2019): after → ₹2 lakh"],
  why="The cover depends on the opening date, so it is neither uniform nor reversed.",
  computed=True,
  facts=[fact("Accident cover on RuPay card increased from ₹1 lakh to ₹2 lakh for PMJDY accounts opened after "
              "28.08.2018", PMJDY_PIB)])

# ================================================================= 14. Priority Sector Lending (2 / 3 / 2)
T = "Priority Sector Lending"
Q(T, "Targets and sub-targets", "Basic",
  "What is the agriculture sub-target under priority sector lending for domestic scheduled commercial banks?",
  ["18% of ANBC or CEOBSE, whichever is higher", "10% of ANBC or CEOBSE, whichever is higher",
   "7.5% of ANBC or CEOBSE, whichever is higher", "12% of ANBC or CEOBSE, whichever is higher"],
  concept="PSL sub-targets",
  explanation="Within the 40% total PSL target, agriculture must get 18% of ANBC or CEOBSE (whichever is higher). "
              "Within agriculture, 14% is for non-corporate farmers, of which 10% is for small and marginal farmers.",
  steps=["Total PSL 40%", "Agriculture 18%"],
  why="10% is the small and marginal farmers sub-target; 7.5% is micro enterprises; 12% is weaker sections.",
  current=ca("2025-04-01"),
  facts=[fact("PSL Directions 2025: agriculture 18% of ANBC or CEOBSE, whichever is higher (of which 10% for small "
              "and marginal farmers)", PSL_MD)])
Q(T, "PSLCs", "Basic",
  "How many types of Priority Sector Lending Certificates (PSLCs) are traded?",
  ["Four", "Two", "Three", "Five"],
  concept="Priority Sector Lending Certificates",
  explanation="There are four PSLCs: PSLC-Agriculture, PSLC-Small and Marginal Farmers, PSLC-Micro Enterprises and "
              "PSLC-General. Banks with a surplus sell them to banks with a shortfall, through RBI's e-Kuber portal.",
  steps=["PSLC types: Agriculture, SF/MF, Micro Enterprises, General = 4"],
  why="Weaker sections, housing and education have no separate PSLC.",
  facts=[fact("Four PSLCs: Agriculture, SF/MF, Micro Enterprises and General; traded on e-Kuber", PSL_MD)])
Q(T, "Targets and sub-targets", "Intermediate",
  "What is the weaker sections sub-target for domestic scheduled commercial banks under the PSL Directions, 2025?",
  ["12% of ANBC or CEOBSE, whichever is higher", "10% of ANBC or CEOBSE, whichever is higher",
   "15% of ANBC or CEOBSE, whichever is higher", "7.5% of ANBC or CEOBSE, whichever is higher"],
  concept="Weaker sections target",
  explanation="Domestic SCBs must lend 12% of ANBC or CEOBSE (whichever is higher) to weaker sections. For RRBs the "
              "weaker sections target is 15%.",
  steps=["Weaker sections: 12% for domestic SCBs", "15% applies to RRBs"],
  why="15% is the RRB figure; 10% is the SF/MF sub-target; 7.5% is the micro enterprises sub-target.",
  current=ca("2025-04-01"),
  facts=[fact("Weaker sections target 12% for domestic banks and 15% for RRBs", PSL_MD)])
Q(T, "PSLCs", "Intermediate",
  "On which date do all Priority Sector Lending Certificates expire, irrespective of when they were bought?",
  ["31 March of each year", "30 June of each year", "30 September of each year", "One year from the date of issue"],
  concept="Validity of PSLCs",
  explanation="PSLCs are traded on the e-Kuber portal in lots of ₹25 lakh and all of them expire on 31 March, the "
              "reporting date for PSL achievement. They are not valid beyond that date, whatever the date of issue.",
  steps=["All PSLCs expire on 31 March"],
  why="PSLCs do not run for a full year from issue; 30 June and 30 September are not expiry dates.",
  facts=[fact("PSLCs expire on March 31 of each year; lot size ₹25 lakh; traded on e-Kuber", PSL_MD)])
Q(T, "Targets and sub-targets", "Intermediate",
  "What is the overall priority sector lending target for Regional Rural Banks?",
  ["75% of ANBC or CEOBSE, whichever is higher", "40% of ANBC or CEOBSE, whichever is higher",
   "60% of ANBC or CEOBSE, whichever is higher", "50% of ANBC or CEOBSE, whichever is higher"],
  concept="PSL targets by bank category",
  explanation="RRBs have an overall PSL target of 75% (medium enterprises, social infrastructure and renewable "
              "energy together capped at 15%). Domestic SCBs have 40%, and SFBs and UCBs 60%.",
  steps=["Domestic SCBs 40%", "SFBs and UCBs 60%", "RRBs 75%"],
  why="40% is for domestic SCBs and large foreign banks; 60% is for SFBs and UCBs; 50% is not a PSL target.",
  current=ca("2025-04-01"),
  facts=[fact("Total PSL target for RRBs: 75% of ANBC or CEOBSE, whichever is higher", PSL_MD)])

anbc, ceobse = 200000, 210000
base = max(anbc, ceobse)
agri = base * 18 // 100
assert (base, agri, anbc * 18 // 100, base * 40 // 100, base * 10 // 100) == (210000, 37800, 36000, 84000, 21000)
Q(T, "Targets and sub-targets", "Advanced",
  f"A domestic scheduled commercial bank has Adjusted Net Bank Credit (ANBC) of ₹{inr(anbc)} crore and Credit "
  f"Equivalent of Off-Balance Sheet Exposures (CEOBSE) of ₹{inr(ceobse)} crore for the relevant date. What is its "
  "agriculture lending target?",
  [f"₹{inr(21000)} crore", f"₹{inr(36000)} crore", f"₹{inr(37800)} crore", f"₹{inr(84000)} crore"],
  answer="C",
  concept="Computing PSL targets",
  explanation="PSL targets are computed on ANBC or CEOBSE, whichever is higher. Here CEOBSE (2,10,000) is higher. "
              "Agriculture target = 18% × 2,10,000 = ₹37,800 crore. (Total PSL target = 40% = ₹84,000 crore; SF/MF "
              "= 10% = ₹21,000 crore.)",
  steps=["Base = max(2,00,000, 2,10,000) = 2,10,000", "Agriculture = 18% × 2,10,000 = ₹37,800 crore"],
  why="₹36,000 crore uses ANBC (the lower base); ₹84,000 crore is the total PSL target; ₹21,000 crore is the small "
      "and marginal farmers target.",
  computed=True, current=ca("2025-04-01"),
  facts=[fact("Targets computed on ANBC or CEOBSE, whichever is higher; agriculture 18%, SF/MF 10%, total 40%",
              PSL_MD)])

shortfall_pp = 6
rate = BANK_RATE - (2 if shortfall_pp < 5 else 3 if shortfall_pp < 10 else 4)
assert rate == F(275, 100)
Q(T, "Targets and sub-targets", "Advanced",
  "A domestic bank's overall PSL achievement falls short of the target by 6 percentage points. Its shortfall is "
  "allocated to RIDF with NABARD. With the Bank Rate at 5.75%, at what interest rate will the bank earn on this "
  "deposit?",
  ["1.75%", "2.75%", "3.75%", "5.75%"],
  answer="B",
  concept="Penalty for PSL shortfall",
  explanation="Shortfall amounts are deposited in RIDF and similar funds at rates linked to the Bank Rate: Bank "
              "Rate − 2 for an overall shortfall below 5 percentage points, Bank Rate − 3 for 5 to below 10 points, "
              "and Bank Rate − 4 for 10 points or more. A 6-point shortfall earns 5.75 − 3 = 2.75%.",
  steps=["Shortfall 6 pp → band '5 to below 10' → Bank Rate − 3", "5.75 − 3 = 2.75%"],
  why="3.75% is the rate for a shortfall below 5 points; 1.75% is for 10 points or more; 5.75% is the Bank Rate "
      "itself.",
  computed=True, current=CORRIDOR,
  facts=[fact("PSL shortfall deposits: Bank Rate minus 2 (<5 pp), minus 3 (5 to <10 pp), minus 4 (≥10 pp)", PSL_MD),
         fact("Bank Rate 5.75% after the October 7, 2026 MPC decision", MPC_OCT26)])

# ================================================================= 15. RBI Integrated Ombudsman Scheme (2 / 3 / 2)
T = "RBI Integrated Ombudsman Scheme"
RBIOS26 = ca("2026-07-01")
Q(T, "Scope and grounds", "Basic",
  "The Reserve Bank – Integrated Ombudsman Scheme, 2026 came into force on:",
  ["1 July 2026", "1 April 2026", "12 November 2021", "1 January 2027"],
  concept="RB-IOS, 2026",
  explanation="RB-IOS, 2026 came into force on 1 July 2026 and replaced the Reserve Bank – Integrated Ombudsman "
              "Scheme, 2021. Complaints received before 1 July 2026, and appeals and awards under the 2021 scheme, "
              "continue to be handled under the 2021 scheme.",
  steps=["RB-IOS 2021 → replaced by RB-IOS 2026 from 1 July 2026"],
  why="12 November 2021 was when the 2021 scheme was launched; the other dates are not commencement dates.",
  current=RBIOS26,
  facts=[fact("RB-IOS, 2026 comes into force with effect from July 1, 2026 and replaces RB-IOS, 2021", RBIOS_FAQ)])
Q(T, "Process and limits", "Basic",
  "What fee does a customer have to pay to file a complaint under the RBI Integrated Ombudsman Scheme?",
  ["No fee at all", "₹100 per complaint", "1% of the disputed amount", "₹500 per complaint"],
  concept="Cost of using the Ombudsman",
  explanation="There is no charge or fee for filing or resolving a complaint under RB-IOS. Complaints can be filed "
              "online on the CMS portal (cms.rbi.org.in), by email, or by post to the Centralised Receipt and "
              "Processing Centre at Chandigarh.",
  steps=["Filing and resolution are free"],
  why="The scheme charges nothing, either as a flat fee or as a percentage of the amount.",
  current=RBIOS26,
  facts=[fact("There is no charge or fee for filing or resolving complaints under RB-IOS, 2026", RBIOS_FAQ)])
Q(T, "Process and limits", "Intermediate",
  "A customer complained to her bank, which has not replied. After how many days without a reply can she approach "
  "the RBI Ombudsman (assuming no longer timeline is prescribed for that service)?",
  ["30 days", "15 days", "60 days", "90 days"],
  concept="When a complaint can be filed",
  explanation="The customer must first complain to the regulated entity. If the RE does not reply within 30 days "
              "(or a longer period prescribed by RBI, NPCI or card network rules, whichever is higher), or she is "
              "not satisfied with the reply, she can approach the RBI Ombudsman.",
  steps=["Step 1: complain to the RE", "Step 2: no reply in 30 days → Ombudsman"],
  why="15 and 60 days are not the scheme's waiting period; 90 days is the window for filing with the Ombudsman.",
  current=RBIOS26,
  facts=[fact("A complaint may be filed with the Ombudsman if the RE does not reply within 30 days (or longer "
              "prescribed period, whichever is higher)", RBIOS_FAQ)])
Q(T, "Process and limits", "Intermediate",
  "Under RB-IOS, 2026, within what period must a complaint be lodged with the RBI Ombudsman?",
  ["Within 90 days of the expiry of the RE's reply period or its last communication, whichever is later",
   "Within one year of receiving the RE's reply",
   "Within 30 days of the transaction",
   "Within three years of the cause of action"],
  concept="Time limit for approaching the Ombudsman",
  explanation="Under the 2026 scheme the complaint must be made to the RBI Ombudsman within 90 days of the expiry "
              "of the timeline for the RE's reply or of the RE's last communication, whichever is later. (The 2021 "
              "scheme allowed one year from the RE's reply.) The original complaint to the RE must be made within "
              "the Limitation Act period.",
  steps=["2026 scheme window: 90 days", "Counted from the later of: reply-timeline expiry or last communication"],
  why="One year was the rule under RB-IOS 2021; 30 days and three years are not the scheme's limits.",
  current=RBIOS26,
  facts=[fact("Complaint to the Ombudsman must be made within 90 days of the expiry of the timeline or the last "
              "communication from the RE, whichever is later", RBIOS_FAQ)])
Q(T, "Scope and grounds", "Intermediate",
  "Which Primary (Urban) Co-operative Banks are covered by the RBI Integrated Ombudsman Scheme, 2026?",
  ["All scheduled UCBs, and non-scheduled UCBs with deposits of ₹50 crore and above",
   "All UCBs, whatever their size", "Only scheduled UCBs", "Only UCBs with deposits of ₹500 crore and above"],
  concept="Regulated entities covered",
  explanation="RB-IOS covers commercial banks, RRBs, State and Central Co-operative Banks, all scheduled "
              "Primary (Urban) Co-operative Banks, non-scheduled UCBs with deposits of ₹50 crore and above (as per "
              "the previous year's audited balance sheet), deposit-taking NBFCs and NBFCs with customer interface "
              "and assets of ₹100 crore and above, non-bank PPI issuers and credit information companies.",
  steps=["Scheduled UCBs: all covered, whatever their size",
         "Non-scheduled UCBs: covered only if deposits are ₹50 crore or more",
         "So the covered set is all scheduled UCBs plus non-scheduled UCBs with deposits of ₹50 crore and above"],
  why="'All UCBs' wrongly includes small non-scheduled UCBs; 'only scheduled UCBs' leaves out large non-scheduled "
      "ones; ₹500 crore is not the threshold.",
  current=RBIOS26,
  facts=[fact("All Scheduled Primary (Urban) Co-operative Banks are covered; Non-Scheduled UCBs with deposit size "
              "of Rs 50 crore and above are covered", RBIOS_FAQ)])

disputed, conseq_claim = 8, 35
award_2026 = disputed + min(conseq_claim, 30) + 3
award_2021 = disputed + min(conseq_claim, 20) + 1
assert (award_2026, award_2021) == (41, 29)
Q(T, "Process and limits", "Advanced",
  "A complaint under RB-IOS, 2026 involves an unauthorised debit of ₹8 lakh. The customer also claims ₹35 lakh of "
  "consequential loss and compensation for harassment. What is the maximum the Ombudsman can award in total?",
  ["₹29 lakh", "₹33 lakh", "₹41 lakh", "₹46 lakh"],
  answer="C",
  concept="Compensation limits under RB-IOS, 2026",
  explanation="There is no limit on the disputed amount itself (₹8 lakh). For consequential loss the Ombudsman can "
              "award up to ₹30 lakh, and for loss of time, expenses, harassment and mental anguish up to ₹3 lakh. "
              "Maximum = 8 + 30 + 3 = ₹41 lakh. (Under the 2021 scheme the caps were ₹20 lakh and ₹1 lakh.)",
  steps=["Disputed amount: no cap → ₹8 lakh", "Consequential loss: min(35, 30) = ₹30 lakh",
         "Harassment/time: up to ₹3 lakh", "Total = ₹41 lakh"],
  why="₹46 lakh ignores the ₹30 lakh cap; ₹29 lakh uses the 2021 caps; ₹33 lakh leaves out the disputed amount.",
  computed=True, current=RBIOS26,
  facts=[fact("No limit on the amount in dispute; compensation up to ₹30 lakh for consequential loss and up to ₹3 "
              "lakh for time, expenses, harassment/mental anguish", RBIOS_FAQ),
         fact("Under RB-IOS 2021 the caps were ₹20 lakh (consequential loss) and ₹1 lakh (time, expenses, "
              "harassment)", RBIOS_2021)])
Q(T, "Process and limits", "Advanced",
  "Consider the following statements about appeals under RB-IOS, 2026:\nI. A complainant can appeal to the "
  "Appellate Authority against the rejection of a complaint.\nII. A complainant may appeal against an Award within "
  "30 days of receiving it, and the Appellate Authority may allow a further period of up to 30 days for sufficient "
  "cause.\nIII. A regulated entity cannot appeal against an Award passed because it failed to furnish the required "
  "information or documents.\nWhich of the above is/are correct?",
  ["II and III only", "I and II only", "I and III only", "I, II and III"],
  concept="Appellate mechanism",
  explanation="An appeal lies only against an Award, not against a settlement or a rejection, so I is wrong. The "
              "complainant may appeal within 30 days of receiving the Award, extendable by up to 30 more days, so II "
              "is right. An RE cannot appeal against an Award passed for its failure to furnish information or "
              "documents, so III is right.",
  steps=["I: wrong (no appeal against rejection)", "II: correct (30 + up to 30 days)", "III: correct"],
  current=RBIOS26,
  facts=[fact("Appeals lie only against an Award; complainant may appeal within 30 days of the Award, extendable by "
              "up to 30 days; no RE appeal against an Award passed for failure to furnish information", RBIOS_FAQ)])

# ================================================================= 16. Digital Banking (3 / 3 / 3)
T = "Digital Banking"
Q(T, "CBDC (e-rupee)", "Basic",
  "Does a customer earn interest on the balance held in a retail e-rupee (e₹) wallet?",
  ["No, no interest is payable on e₹ wallet balances", "Yes, at the savings deposit rate",
   "Yes, at the policy repo rate", "Yes, but only on balances above ₹1 lakh"],
  concept="Digital Rupee (e₹)",
  explanation="The e₹ is RBI's central bank digital currency, a digital form of the rupee bank note. Like cash, it "
              "does not pay interest. It can be loaded from and redeemed to a bank account at any time.",
  steps=["e₹ = digital form of cash", "Cash earns no interest → e₹ wallet balances earn no interest"],
  why="e₹ is not a deposit, so neither the savings rate nor any policy rate applies to it.",
  facts=[fact("There is no interest payable on e₹ wallet balances", ERUPEE_FAQ)])
Q(T, "Digital lending", "Basic",
  "Under the RBI (Digital Lending) Directions, 2025, how must a digital loan be disbursed?",
  ["Directly into the borrower's bank account", "Into a pool account of the lending service provider",
   "In cash through the lending service provider's agent", "Into the digital lending app's wallet"],
  concept="Fund flow in digital lending",
  explanation="Loan disbursals must go directly into the borrower's bank account, and repayments must go directly "
              "into the regulated entity's account, without any pass-through or pool account of a lending service "
              "provider or other third party.",
  steps=["Disbursal: RE → borrower's own bank account", "No LSP pool or pass-through accounts"],
  why="Pool accounts of LSPs, cash disbursal through agents and app wallets are what the rule prohibits.",
  facts=[fact("Loans are disbursed into the borrower's bank account and repaid directly to the RE without any pass-"
              "through or pool account of an LSP", DL_2025)])
Q(T, "Mobile and internet banking", "Basic",
  "Under RBI's Digital Banking Channels Authorisation Directions, 2025, can a bank make it compulsory for a customer "
  "to opt for internet or mobile banking in order to get a debit card?",
  ["No, banks cannot make any digital banking channel mandatory for other facilities",
   "Yes, for all new accounts", "Yes, but only for savings accounts", "Yes, if the customer is below 60 years"],
  concept="Customer choice in digital banking",
  explanation="Banks must obtain explicit customer consent to register for digital banking and shall not make it "
              "mandatory for a customer to opt for any digital banking channel to avail other facilities such as "
              "debit cards. Banks offering transactional digital banking need RBI's prior approval.",
  steps=["Digital banking is opt-in with explicit consent", "Cannot be bundled as a precondition"],
  why="The Directions allow no exception by account type or age.",
  current=ca("2026-01-01"),
  facts=[fact("Banks shall not make it mandatory for the customer to opt for any digital banking channel to avail "
              "other facilities such as debit cards; explicit consent required", DBC_MD)])
Q(T, "Digital lending", "Intermediate",
  "What is the minimum 'cooling-off' period during which a borrower can exit a digital loan without penalty under "
  "the RBI (Digital Lending) Directions, 2025?",
  ["One day", "Three days", "Seven days", "Fifteen days"],
  concept="Cooling-off period",
  explanation="A borrower can exit a digital loan during the cooling-off period by repaying the principal and the "
              "proportionate APR without any penalty. The period is fixed by the RE's Board but cannot be less "
              "than one day. The RE may retain a reasonable one-time processing fee if disclosed upfront in the KFS.",
  steps=["Cooling-off period set by the Board", "Floor: not less than one day"],
  why="Three days was the minimum under the 2022 guidelines for loans of seven days or more; seven and fifteen "
      "days are not prescribed.",
  current=ca("2025-05-08"),
  facts=[fact("Cooling-off period determined by the RE's Board, not less than one day; exit by paying principal and "
              "proportionate APR without penalty", DL_2025)])
Q(T, "CBDC (e-rupee)", "Intermediate",
  "The first pilot of the wholesale digital rupee (e₹-W), launched on 1 November 2022, was used for:",
  ["Settlement of secondary market transactions in government securities",
   "Payment of salaries to government employees", "Merchant payments at retail stores",
   "Cross-border remittances by individuals"],
  concept="Wholesale CBDC pilot",
  explanation="RBI began the e₹-W pilot on 1 November 2022 with nine banks; its use case was settling secondary "
              "market transactions in government securities in central bank money. The retail pilot (e₹-R) began "
              "on 1 December 2022.",
  steps=["e₹-W pilot: 1 Nov 2022", "Use case: G-sec secondary market settlement"],
  why="Merchant payments belong to the retail pilot; salaries and remittances were not the e₹-W use case.",
  facts=[fact("First e₹-W pilot from November 1, 2022 for settlement of secondary market transactions in government "
              "securities; nine banks", EW_PR)])
Q(T, "Digital lending", "Intermediate",
  "Under the RBI (Digital Lending) Directions, 2025, where must data collected by digital lending apps be stored?",
  ["On servers located in India; data processed abroad must be brought back within 24 hours",
   "Anywhere, provided it is encrypted", "Only with RBI's data centre",
   "In India or any G20 country"],
  concept="Data localisation in digital lending",
  explanation="REs must ensure that borrower data is stored only on servers located in India. If data is processed "
              "outside India, it must be deleted there and brought back to India within 24 hours. Data collection "
              "must be need-based and with the borrower's explicit consent.",
  steps=["Storage: servers in India", "Processing abroad: bring back within 24 hours"],
  why="Encryption alone is not enough; RBI does not store lender data; G20 countries are not permitted locations.",
  current=ca("2025-05-08"),
  facts=[fact("Data to be stored on servers in India; data processed abroad to be brought back within 24 hours",
              DL_2025)])
Q(T, "Digital lending", "Advanced",
  "Consider the following statements under the RBI (Digital Lending) Directions, 2025:\nI. A lending service provider "
  "(LSP) may collect its fee directly from the borrower if it is disclosed in the Key Fact Statement.\nII. A "
  "regulated entity cannot increase a borrower's credit limit automatically without the borrower's explicit "
  "consent.\nIII. Repayments may be routed through the LSP's pool account for up to one day.\n"
  "Which of the above is/are correct?",
  ["II only", "I and II only", "II and III only", "I, II and III"],
  concept="Borrower protection in digital lending",
  explanation="Fees of LSPs are paid by the RE, not charged to the borrower, so I is wrong. Automatic increase of "
              "credit limits is prohibited without the borrower's explicit, recorded consent, so II is right. "
              "Repayments must go directly to the RE's account with no pass-through or pool account, so III is "
              "wrong.",
  steps=["I: wrong (RE pays the LSP)", "II: correct", "III: wrong (no pool accounts)"],
  current=ca("2025-05-08"),
  facts=[fact("REs pay LSP fees directly and LSPs cannot charge borrowers; no automatic increase in credit limits "
              "without explicit consent; no pass-through or pool accounts", DL_2025)])

disbursed, offered = 200, 14
cap = disbursed * 5 // 100
assert (cap, min(offered, cap)) == (10, 10)
Q(T, "Digital lending", "Advanced",
  "A bank has disbursed ₹200 crore through a digital lending portfolio. Its LSP offers a default loss guarantee (DLG) "
  "of ₹14 crore on this portfolio. Under RBI's Digital Lending Directions, what is the maximum DLG cover the bank "
  "can accept?",
  ["₹5 crore", "₹10 crore", "₹14 crore", "₹20 crore"],
  answer="B",
  concept="Default loss guarantee cap",
  explanation="A DLG is an arrangement where an entity such as an LSP compensates the RE for losses due to default "
              "up to a specified percentage of the portfolio. The total DLG cover on any outstanding portfolio "
              "cannot exceed 5% of the amount disbursed out of it: 5% × 200 = ₹10 crore. So only ₹10 crore of the "
              "₹14 crore offer can be accepted.",
  steps=["DLG cap = 5% of amount disbursed", "5% × ₹200 crore = ₹10 crore", "Offer of ₹14 crore exceeds the cap"],
  why="₹14 crore exceeds the cap; ₹20 crore applies 10%; ₹5 crore applies 2.5%.",
  computed=True, current=ca("2025-05-08"),
  facts=[fact("Total DLG cover on any outstanding portfolio shall not exceed five per cent of the amount disbursed "
              "out of that loan portfolio", DL_2025)])
Q(T, "CBDC (e-rupee)", "Advanced",
  "Consider the following statements about the retail digital rupee (e₹):\nI. e₹ is legal tender and a liability "
  "of the Reserve Bank of India.\nII. e₹ can be made programmable, for example with an expiry date, geo-location or "
  "merchant category restrictions.\nIII. e₹ wallets can be offered only by banks; non-banks are not allowed.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I, II and III", "II and III only", "I only"],
  concept="Features of the e₹",
  explanation="e₹ is the digital form of the rupee bank note, so it is legal tender and RBI's liability (I is "
              "right). Programmability with conditions such as expiry, geo-location, merchant category codes or "
              "merchant VPA is available, mainly for government and corporate use (II is right). e₹ wallets are "
              "offered by banks and non-banks (III is wrong).",
  steps=["I: correct", "II: correct", "III: wrong (non-bank wallets are allowed)"],
  facts=[fact("e₹ is legal tender and a liability of RBI; programmable by expiry, geo-location, MCC, merchant VPA; "
              "e₹ wallets offered by banks and non-banks", ERUPEE_FAQ)])

# ================================================================= 17. UPI (2 / 3 / 2)
T = "UPI"
Q(T, "Features", "Basic",
  "In which year was the Unified Payments Interface (UPI) implemented by NPCI?",
  ["2014", "2016", "2018", "2010"],
  answer="B",
  concept="UPI",
  explanation="UPI was implemented by the National Payments Corporation of India in April 2016. It lets users link "
              "bank accounts to a mobile app and pay instantly using a virtual payment address, 24x7.",
  steps=["UPI launched by NPCI in April 2016"],
  why="2010 is when IMPS was launched; 2014 and 2018 are not UPI's launch year.",
  facts=[fact("UPI was implemented by NPCI in April 2016", PSR_DEC24)])
Q(T, "UPI Lite and international", "Basic",
  "What is the maximum amount of a single UPI Lite payment?",
  ["₹500", "₹1,000", "₹2,000", "₹5,000"],
  answer="B",
  concept="UPI Lite",
  explanation="UPI Lite is an on-device wallet for small, PIN-less payments. Each payment can be up to ₹1,000 and "
              "the total balance at any time up to ₹5,000 (raised from ₹500 and ₹2,000).",
  steps=["Per transaction: ₹1,000", "Wallet limit: ₹5,000"],
  why="₹500 and ₹2,000 were the earlier per-transaction and wallet limits; ₹5,000 is the current wallet limit.",
  current=ca("2024-12-04"),
  facts=[fact("UPI Lite: per transaction ₹1,000 and total limit ₹5,000", OFFLINE_FW),
         fact("UPI LITE processes low-value transactions in a faster, pin-less manner", UPI_LITE_NPCI)])
Q(T, "Features", "Intermediate",
  "UPI123Pay, launched by RBI on 8 March 2022, is designed mainly for:",
  ["Users of feature phones", "Payments by foreign tourists", "Large-value corporate payments",
   "Payments using credit cards only"],
  concept="UPI123Pay",
  explanation="UPI123Pay brings UPI to feature phone users. It offers options such as IVR calls, missed calls, "
              "app-based payments on feature phones and proximity sound-based payments, without needing a "
              "smartphone or the cumbersome USSD (*99#) route.",
  steps=["UPI123Pay = UPI for feature phones (no internet needed)"],
  why="It is not targeted at tourists, corporates or credit cards.",
  facts=[fact("UPI123Pay launched on 8 March 2022 for feature phone users", UPI123_PIB),
         fact("UPI123Pay offers IVR, missed call, app-based and sound-based payment options", PSR_DEC24)])
Q(T, "Features", "Intermediate",
  "'UPI Circle', introduced in August 2024, allows:",
  ["A primary user to let a secondary user make UPI payments from the primary user's bank account within set limits",
   "Friends to split a restaurant bill automatically", "Merchants to accept UPI payments without a bank account",
   "Users to send UPI payments to any country without limits"],
  concept="Delegated payments on UPI",
  explanation="UPI Circle (delegated payments) lets a primary user allow a secondary user, such as a family member, "
              "to make UPI transactions up to a limit from the primary user's bank account. It offers partial and "
              "full delegation.",
  steps=["Primary user delegates", "Secondary user pays from primary's account within limits"],
  why="Bill-splitting, account-less merchants and unlimited international payments are not what UPI Circle does.",
  facts=[fact("Delegated Payments / UPI Circle (introduced August 2024) let a primary user allow a secondary user to "
              "make UPI transactions up to a limit from the primary user's account", RBI_AR_2425)])
Q(T, "UPI Lite and international", "Intermediate",
  "India linked UPI with the fast payment system of which country, allowing users to send money using a UPI ID or "
  "mobile number across the two systems?",
  ["Singapore (PayNow)", "United Kingdom (Faster Payments)", "United States (FedNow)", "Japan (Zengin)"],
  concept="UPI international linkages",
  explanation="India and Singapore launched a cross-border linkage between UPI and PayNow in 2023, letting users of "
              "both systems send and receive money using UPI IDs, mobile numbers or VPAs. UPI is also accepted in "
              "countries such as Bhutan, Nepal, the UAE, France, Sri Lanka and Mauritius through NPCI "
              "International (NIPL).",
  steps=["Fast payment system linkage: UPI–PayNow (Singapore)"],
  why="No such linkage exists with UK Faster Payments, FedNow or Zengin.",
  facts=[fact("India and Singapore launched cross-border linkage using UPI and PayNow", PAYNOW_PIB)])

lite_txn, lite_bal = 1000, 5000
assert 1200 > lite_txn and 3000 <= lite_bal
Q(T, "UPI Lite and international", "Advanced",
  "Meena has ₹3,000 in her UPI Lite wallet and wants to pay a shopkeeper ₹1,200. Which statement is correct?",
  ["She cannot pay ₹1,200 from UPI Lite; she must use regular UPI with her PIN",
   "She can pay from UPI Lite because her balance exceeds ₹1,200",
   "She can pay from UPI Lite after topping the wallet up to ₹5,000",
   "She can pay ₹1,000 from UPI Lite and ₹200 must be paid in cash"],
  concept="Applying UPI Lite limits",
  explanation="UPI Lite allows a maximum of ₹1,000 per transaction (wallet limit ₹5,000). A ₹1,200 payment exceeds "
              "the per-transaction limit, whatever the balance, so she must use regular UPI authenticated with her "
              "UPI PIN (she could also split the payment, but cash is not required).",
  steps=["Per-transaction limit = ₹1,000", "₹1,200 > ₹1,000 → not allowed in UPI Lite", "Use regular UPI"],
  why="The balance and top-ups do not change the per-transaction limit; nothing forces part payment in cash.",
  computed=True, current=ca("2024-12-04"),
  facts=[fact("UPI Lite: ₹1,000 per transaction, ₹5,000 total limit", OFFLINE_FW)])
Q(T, "UPI Lite and international", "Advanced",
  "Consider the following statements:\nI. NPCI International Payments Ltd (NIPL), a wholly owned subsidiary of NPCI, "
  "takes UPI and RuPay to other countries.\nII. UPI Lite processes low-value payments without a UPI PIN.\nIII. In "
  "UPI Circle, the secondary user can transact from the primary user's account only within limits set by the "
  "primary user.\nWhich of the above is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I and III only"],
  concept="UPI ecosystem",
  explanation="All three are correct. NIPL, set up by NPCI in 2020, takes UPI and RuPay abroad. UPI Lite handles "
              "low-value payments in a faster, PIN-less manner. In UPI Circle the primary user sets the limits "
              "within which the secondary user can pay.",
  steps=["I: correct", "II: correct", "III: correct"],
  facts=[fact("NIPL is a wholly owned subsidiary of NPCI set up to take UPI and RuPay abroad", UPI_PIB_FACT),
         fact("UPI LITE processes low-value transactions in a faster and pin-less manner", UPI_LITE_NPCI),
         fact("UPI Circle allows a secondary user to transact up to a limit set by the primary user", UPI_CIRCLE_NPCI)])

# ================================================================= 18. NEFT (1 / 2 / 1)
T = "NEFT"
Q(T, "Settlement and timings", "Basic",
  "How does NEFT settle transactions since it became available 24x7 on 16 December 2019?",
  ["In 48 half-hourly batches every day", "Individually in real time", "In 12 hourly batches on working days only",
   "Once at the end of each day"],
  concept="NEFT settlement",
  explanation="NEFT is a deferred net settlement system owned and operated by RBI. Since 16 December 2019 it runs "
              "24x7x365 in 48 half-hourly batches, the first after 00:30 and the last ending at 00:00 hours.",
  steps=["NEFT = deferred net settlement", "48 half-hourly batches, 24x7"],
  why="Real-time individual settlement is RTGS; NEFT is not limited to working days or one daily batch.",
  facts=[fact("NEFT available 24x7 from December 16, 2019 with 48 half-hourly batches", NEFT_247)])
Q(T, "Settlement and timings", "Intermediate",
  "In NEFT, within what time must the beneficiary bank credit the beneficiary's account (or return the money) after "
  "the batch is settled?",
  ["Within 2 hours", "Within 30 minutes", "Within 1 hour", "By the end of the next working day"],
  concept="NEFT credit timelines",
  explanation="The beneficiary bank must credit the account within two hours of settlement of the batch; otherwise "
              "it must return the funds within two hours of batch completion. Delays attract penal interest at the "
              "LAF repo rate plus 2%.",
  steps=["NEFT credit or return: within 2 hours of batch settlement"],
  why="30 minutes is the RTGS credit time; one hour is the RTGS return window; next-day credit is not allowed.",
  facts=[fact("Beneficiary to be credited within two hours of batch settlement, failing which funds returned; "
              "penal interest at LAF repo + 2%", NEFT_FAQ)])
Q(T, "Settlement and timings", "Intermediate",
  "A person without a bank account wants to send money through NEFT by depositing cash at an NEFT-enabled branch. "
  "What is the maximum amount per transaction?",
  ["₹50,000", "₹10,000", "₹2 lakh", "There is no limit"],
  concept="Walk-in cash remittance in NEFT",
  explanation="NEFT can be used by persons without a bank account by depositing cash at an NEFT-enabled branch, "
              "subject to a limit of ₹50,000 per transaction (with KYC details). Otherwise RBI places no limit on "
              "NEFT amounts.",
  steps=["Walk-in cash NEFT cap: ₹50,000 per transaction"],
  why="RBI sets no general NEFT limit, but the walk-in cash route is capped at ₹50,000.",
  facts=[fact("Non-account holders can remit through NEFT by depositing cash up to ₹50,000 per transaction",
              NEFT_FAQ)])

charge = lambda amt: F(5, 2) if amt <= 10000 else 5 if amt <= 100000 else 15 if amt <= 200000 else 25
assert charge(150000) == 15
Q(T, "Settlement and timings", "Advanced",
  "A current account holder sends ₹1.5 lakh by NEFT at a branch, and a savings account holder sends ₹1.5 lakh by "
  "NEFT through internet banking. What is the maximum each bank may charge (excluding GST)?",
  ["₹15 for the current account holder; nothing for the savings account holder", "₹15 for each of them",
   "₹25 for the current account holder; nothing for the savings account holder", "Nothing for either of them"],
  concept="NEFT charges",
  explanation="Inward NEFT is free, and online NEFT from savings accounts is free. For other outward NEFT, banks "
              "may charge at most ₹2.50 (up to ₹10,000), ₹5 (₹10,000 to ₹1 lakh), ₹15 (₹1 lakh to ₹2 lakh) and ₹25 "
              "(above ₹2 lakh), plus GST. ₹1.5 lakh at a branch from a current account → up to ₹15; online from "
              "a savings account → nil.",
  steps=["Branch NEFT of ₹1.5 lakh → slab ₹1–2 lakh → max ₹15", "Online NEFT by savings account holder → free"],
  why="₹25 applies above ₹2 lakh; online savings-account NEFT is free; branch NEFT for a current account is not "
      "automatically free.",
  computed=True,
  facts=[fact("Savings account holders pay nothing for online NEFT; outward charges capped at ₹2.50/₹5/₹15/₹25 by "
              "amount slab plus GST", NEFT_FAQ)])

# ================================================================= 19. RTGS (1 / 2 / 1)
T = "RTGS"
Q(T, "Limits and timings", "Basic",
  "In the RTGS system, 'gross settlement' means that:",
  ["Each transaction is settled individually, without netting against other transactions",
   "Transactions are added up and settled once a day", "Only transactions above ₹1 crore are settled",
   "The transfer amount includes charges and taxes"],
  concept="Real Time Gross Settlement",
  explanation="In RTGS, funds are transferred continuously on a real-time basis and each transaction is settled "
              "individually (gross), not netted. Settlement takes place in the books of RBI, which makes it final "
              "and irrevocable.",
  steps=["Real time = immediate processing", "Gross = transaction-by-transaction, no netting"],
  why="Batch/net settlement describes NEFT; RTGS's minimum is ₹2 lakh, not ₹1 crore; 'gross' is unrelated to "
      "charges.",
  facts=[fact("RTGS is continuous, transaction-by-transaction (gross) settlement in real time in the books of RBI",
              RTGS_FAQ)])
Q(T, "Limits and timings", "Intermediate",
  "Within how much time must the beneficiary bank credit the beneficiary's account after receiving an RTGS fund "
  "transfer message?",
  ["30 minutes", "2 hours", "1 hour", "Same working day"],
  concept="RTGS credit timeline",
  explanation="The beneficiary bank must credit the beneficiary's account within 30 minutes of receiving the RTGS "
              "message. If it cannot, it must return the funds within one hour of receipt or before the end of the "
              "RTGS business day, whichever is earlier.",
  steps=["Credit: within 30 minutes", "If not possible: return within 1 hour"],
  why="Two hours is the NEFT timeline; one hour is the return window, not the credit window.",
  facts=[fact("The beneficiary bank must credit the beneficiary's account within 30 minutes of receiving the funds "
              "transfer message", RTGS_FAQ)])
Q(T, "Limits and timings", "Intermediate",
  "The Unique Transaction Reference (UTR) number that identifies each RTGS transaction is:",
  ["A 22-character code", "A 12-digit number", "An 11-character IFSC", "A 16-digit number"],
  concept="Identification of RTGS transactions",
  explanation="Every RTGS transaction carries a 22-character Unique Transaction Reference (UTR) number. The IFSC, "
              "by contrast, is an 11-character code identifying the bank branch.",
  steps=["RTGS UTR = 22 characters"],
  why="IFSC has 11 characters and identifies a branch, not a transaction; 12 and 16 digits are other formats.",
  facts=[fact("Unique Transaction Reference (UTR) number is a 22-character code that uniquely identifies an RTGS "
              "transaction", RTGS_FAQ)])

rtgs_cap = lambda amt: None if amt < 200000 else 25 if amt <= 500000 else 50
assert rtgs_cap(150000) is None and rtgs_cap(300000) + rtgs_cap(700000) == 75
Q(T, "Limits and timings", "Advanced",
  "A customer wants to send three separate payments of ₹1.5 lakh, ₹3 lakh and ₹7 lakh through RTGS. Which statement "
  "is correct?",
  ["The ₹1.5 lakh payment cannot go through RTGS; outward charges on the other two can be at most ₹75 plus tax",
   "All three can go through RTGS; total charges can be at most ₹75 plus tax",
   "The ₹1.5 lakh payment cannot go through RTGS; the other two must be free because RTGS is 24x7",
   "All three can go through RTGS and each can be charged up to ₹50 plus tax"],
  concept="RTGS minimum and charges",
  explanation="RTGS has a minimum of ₹2 lakh, so ₹1.5 lakh must use NEFT or IMPS. Outward RTGS charges are capped "
              "at ₹25 for ₹2–5 lakh and ₹50 above ₹5 lakh (excluding tax); inward RTGS is free. So the ₹3 lakh and "
              "₹7 lakh payments can cost at most 25 + 50 = ₹75 plus tax.",
  steps=["₹1.5 lakh < ₹2 lakh minimum → not RTGS", "₹3 lakh → cap ₹25", "₹7 lakh → cap ₹50", "Total cap = ₹75"],
  why="The ₹1.5 lakh payment is below the minimum; 24x7 availability does not make outward RTGS free; the ₹50 cap "
      "applies only above ₹5 lakh.",
  computed=True,
  facts=[fact("RTGS minimum ₹2,00,000; outward charges up to ₹25 (₹2-5 lakh) and ₹50 (above ₹5 lakh) excluding tax; "
              "inward free", RTGS_FAQ)])

# ================================================================= 20. IMPS (1 / 1 / 1)
T = "IMPS"
Q(T, "Limits and features", "Basic",
  "Immediate Payment Service (IMPS), an instant 24x7 interbank fund transfer service, is operated by:",
  ["National Payments Corporation of India (NPCI)", "Reserve Bank of India",
   "Clearing Corporation of India Ltd (CCIL)", "State Bank of India"],
  concept="IMPS",
  explanation="IMPS is operated by NPCI. It was publicly launched on 22 November 2010 and offers instant 24x7 "
              "interbank transfers through mobile, internet banking, ATMs, branches and other channels. NEFT and "
              "RTGS, by contrast, are owned and operated by RBI.",
  steps=["IMPS → NPCI (launched 22 November 2010)", "NEFT/RTGS → RBI"],
  why="RBI runs NEFT and RTGS; CCIL settles money market and G-sec trades; SBI is a bank, not a system operator.",
  facts=[fact("IMPS is NPCI's instant 24x7 interbank electronic fund transfer service, publicly launched on 22 "
              "November 2010", IMPS_NPCI)])
Q(T, "Limits and features", "Intermediate",
  "What is the per-transaction limit for IMPS through channels other than SMS and IVRS?",
  ["₹5 lakh", "₹2 lakh", "₹1 lakh", "₹10 lakh"],
  concept="IMPS limit",
  explanation="RBI raised the IMPS per-transaction limit from ₹2 lakh to ₹5 lakh for all channels other than SMS "
              "and IVRS (announced in October 2021). For SMS and IVRS the limit is ₹5,000.",
  steps=["Earlier ₹2 lakh", "Now ₹5 lakh (except SMS/IVRS)"],
  why="₹2 lakh is the earlier limit; ₹1 lakh and ₹10 lakh are not IMPS limits.",
  current=ca("2021-10-08"),
  facts=[fact("Per transaction limit on IMPS is ₹5 lakh for all channels except SMS and IVR", IMPS_NPCI),
         fact("RBI proposed enhancing the IMPS limit from ₹2 lakh to ₹5 lakh (October 8, 2021)", IMPS_RBI)])
Q(T, "Limits and features", "Advanced",
  "On a Sunday night, a customer wants to transfer ₹6 lakh to another bank account so that the beneficiary is "
  "credited almost immediately. Which payment system is suitable?",
  ["RTGS", "IMPS", "NEFT", "Cheque Truncation System"],
  concept="Choosing between IMPS, NEFT and RTGS",
  explanation="RTGS is available 24x7, has a ₹2 lakh minimum and no upper limit, settles in real time, and the "
              "beneficiary bank must credit within 30 minutes. IMPS is instant but capped at ₹5 lakh per "
              "transaction. NEFT is 24x7 but settles in half-hourly batches with credit within two hours. Cheques "
              "take longer and are not cleared on a Sunday night.",
  steps=["₹6 lakh > IMPS limit of ₹5 lakh", "NEFT is batch-based (not immediate)",
         "RTGS: 24x7, ≥ ₹2 lakh, credit within 30 minutes → suitable"],
  why="IMPS exceeds its ₹5 lakh limit; NEFT is not immediate; CTS is not an instant channel.",
  current=ca("2021-10-08"),
  facts=[fact("IMPS per transaction limit ₹5 lakh (except SMS/IVR)", IMPS_NPCI),
         fact("RTGS 24x7 from Dec 14, 2020; minimum ₹2 lakh with no maximum; credit within 30 minutes", RTGS_FAQ)])

# ================================================================= 21. NPCI (2 / 3 / 2)
T = "NPCI"
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Basic",
  "The National Payments Corporation of India (NPCI) was set up in 2008 under the guidance and support of:",
  ["RBI and the Indian Banks' Association (IBA)", "SEBI and the stock exchanges",
   "The Ministry of Electronics and IT", "NABARD and SIDBI"],
  concept="NPCI",
  explanation="NPCI was incorporated in December 2008 as a not-for-profit company (Section 25 of the Companies Act, "
              "1956, now Section 8 of the 2013 Act) with the guidance and support of RBI and IBA, as an umbrella "
              "organisation for retail payment systems in India.",
  steps=["NPCI promoters/guidance: RBI + IBA (2008)"],
  why="SEBI, MeitY, NABARD and SIDBI did not set up NPCI.",
  facts=[fact("NPCI incorporated in December 2008 as a Section 25 not-for-profit company, set up with guidance and "
              "support of RBI and IBA as umbrella organisation for retail payments", NPCI_RBI_PUB)])
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Basic",
  "FASTag, used for electronic toll collection under NPCI's NETC programme, works on which technology?",
  ["Radio Frequency Identification (RFID)", "QR codes", "Near Field Communication (NFC) only", "Bluetooth"],
  concept="National Electronic Toll Collection (NETC)",
  explanation="NETC uses RFID tags (FASTag) so that vehicles can pay at toll plazas without stopping, from prepaid "
              "accounts linked to the FASTag. NPCI acts as the central clearing house between the acquirer bank at "
              "the toll plaza and the FASTag issuer bank.",
  steps=["FASTag = RFID tag linked to a prepaid account"],
  why="QR, NFC and Bluetooth are not the NETC technology.",
  facts=[fact("NETC uses RFID technology to make payments at toll plazas without stopping, from prepaid accounts "
              "linked to FASTag", PSR_DEC25),
         fact("NETC FASTag offers nationwide toll payment interoperability with RFID-enabled transactions",
              NETC_NPCI)])
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Intermediate",
  "RuPay, India's domestic card payment network, was introduced by NPCI in:",
  ["2012", "2008", "2016", "2019"],
  concept="RuPay",
  explanation="RuPay is a home-grown card payment network introduced through NPCI in 2012. RuPay credit cards can "
              "now also be linked to UPI.",
  steps=["RuPay introduced in 2012"],
  why="2008 is NPCI's incorporation; 2016 is UPI's launch; 2019 has no link to RuPay's launch.",
  facts=[fact("RuPay is a home-grown card payment network introduced in 2012 through NPCI", NPCI_RBI_PUB)])
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Intermediate",
  "Which of the following is a typical use of NACH Debit?",
  ["Collecting loan EMIs from many borrowers' accounts", "Paying salaries to many employees",
   "Paying dividends to shareholders", "Disbursing government subsidies to beneficiaries"],
  concept="National Automated Clearing House",
  explanation="NACH handles bulk, repetitive payments. NACH Credit is one debit and many credits (salaries, "
              "pensions, dividends, subsidies). NACH Debit is many debits and one credit, used to collect EMIs, "
              "utility bills and insurance premiums. NACH consolidated the earlier regional ECS systems.",
  steps=["NACH Debit: many accounts debited → one institution credited", "Example: loan EMIs"],
  why="Salaries, dividends and subsidies are NACH Credit uses.",
  facts=[fact("NACH Credit: one debit, multiple credits (salaries, pensions, dividends, subsidies); NACH Debit: "
              "multiple debits, one credit (bills, loan EMIs, insurance premiums)", PSR_DEC24),
         fact("NACH was launched to consolidate multiple ECS systems running across the country", NACH_NPCI)])
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Intermediate",
  "How are transactions authenticated in the Aadhaar Enabled Payment System (AePS)?",
  ["Through Aadhaar-based biometric authentication of the customer", "Through a 4-digit card PIN",
   "Through a one-time password sent to e-mail", "Through the customer's signature on a slip"],
  concept="AePS",
  explanation="AePS is a bank-led model that lets customers use their Aadhaar-linked bank accounts at micro-ATMs/BC "
              "points with Aadhaar biometric authentication. Services include cash withdrawal, cash deposit, fund "
              "transfer, balance enquiry and mini statement.",
  steps=["AePS = Aadhaar number + biometric authentication via BC/micro-ATM"],
  why="Card PINs, e-mail OTPs and signatures are not the AePS authentication method.",
  facts=[fact("AePS services include cash withdrawal, cash deposit, fund transfer, balance inquiry and mini "
              "statement using Aadhaar authentication", AEPS_NPCI)])
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Advanced",
  "Consider the following statements about NPCI:\nI. NPCI is a not-for-profit company, now under Section 8 of the "
  "Companies Act, 2013.\nII. NPCI is a statutory body created by an Act of Parliament.\nIII. NPCI acts as the "
  "central clearing house for FASTag transactions.\nWhich of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="Legal status and roles of NPCI",
  explanation="NPCI was incorporated in 2008 as a Section 25 (now Section 8) not-for-profit company, not by an Act "
              "of Parliament, so II is wrong. It operates retail payment systems authorised under the Payment and "
              "Settlement Systems Act, 2007, and in NETC it is the central clearing house between acquirer and "
              "issuer banks.",
  steps=["I: correct", "II: wrong (a company, not a statutory body)", "III: correct"],
  facts=[fact("NPCI incorporated in December 2008 as a Section 25 (now Section 8) not-for-profit company",
              NPCI_RBI_PUB),
         fact("FASTag transactions involve the acquirer bank, NPCI as Central Clearing House, and the issuer bank",
              FASTAG_PIB)])
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Advanced",
  "Match the NPCI product with its use:\n1. NACH   2. AePS   3. NETC   4. RuPay\n"
  "P. Toll payment without stopping the vehicle\nQ. Bulk and repetitive payments such as salaries and EMIs\n"
  "R. Domestic card payment network\nS. Banking at a BC point using Aadhaar biometrics",
  ["1-Q, 2-S, 3-P, 4-R", "1-S, 2-Q, 3-P, 4-R", "1-Q, 2-S, 3-R, 4-P", "1-P, 2-S, 3-Q, 4-R"],
  concept="NPCI product portfolio",
  explanation="NACH handles bulk, repetitive interbank payments (salaries, dividends, EMIs). AePS lets customers "
              "bank at BC points with Aadhaar biometrics. NETC (FASTag) handles toll payments without stopping. "
              "RuPay is the domestic card network.",
  steps=["NACH → Q", "AePS → S", "NETC → P", "RuPay → R"],
  why="The other options swap NACH with AePS, or NETC with RuPay.",
  facts=[fact("NACH facilitates high-volume, repetitive, periodic electronic transactions", NACH_NPCI),
         fact("AePS lets customers access Aadhaar-linked accounts via biometric authentication through BCs",
              AEPS_NPCI),
         fact("NETC enables toll payments via RFID at toll plazas without stopping", PSR_DEC25),
         fact("RuPay is a home-grown card payment network introduced in 2012 through NPCI", NPCI_RBI_PUB)])

# ================================================================= 22. Payment Banks (1 / 2 / 1)
T = "Payment Banks"
Q(T, "Deposit limit", "Basic",
  "What is the maximum end-of-day balance a payments bank can hold for an individual customer?",
  ["₹2 lakh", "₹1 lakh", "₹5 lakh", "₹10 lakh"],
  concept="Payments bank deposit limit",
  explanation="Payments banks may hold a maximum balance of ₹2,00,000 per individual customer at the end of the "
              "day. The limit was ₹1 lakh in the 2014 licensing guidelines and was raised to ₹2 lakh in April 2021.",
  steps=["2014: ₹1 lakh", "April 2021 onwards: ₹2 lakh"],
  why="₹1 lakh is the original limit; ₹5 lakh is the DICGC cover; ₹10 lakh has no basis.",
  current=ca("2021-04-07"),
  facts=[fact("Payments banks may hold a maximum balance of ₹2,00,000 per individual customer at the end of the day",
              PB_MD),
         fact("RBI enhanced the end-of-day maximum balance for payments banks from ₹1 lakh to ₹2 lakh (7 April "
              "2021)", PB_LIMIT_PR)])
Q(T, "Permitted activities", "Intermediate",
  "Which of the following activities is a payments bank NOT permitted to undertake?",
  ["Issuing credit cards", "Issuing ATM/debit cards", "Acting as a Business Correspondent of another bank",
   "Accepting savings and current account deposits"],
  concept="Scope of payments banks",
  explanation="Payments banks can accept demand deposits (savings and current), issue ATM/debit cards, provide "
              "payments and remittance services, and act as BCs of other banks. They cannot lend, issue credit "
              "cards or accept NRI deposits.",
  steps=["No lending → no credit cards"],
  why="Debit cards, BC work and demand deposits are all permitted activities.",
  facts=[fact("Payments banks cannot undertake lending or issue credit cards; may issue ATM/debit cards, accept "
              "current and savings deposits and act as BC of another bank", PB_GUIDE)])
Q(T, "Permitted activities", "Intermediate",
  "Under RBI's Guidelines for Licensing of Payments Banks (November 2014), what minimum share of its demand deposit "
  "balances was a payments bank required to invest in SLR-eligible government securities or Treasury Bills of up "
  "to one year?",
  ["75%", "25%", "50%", "100%"],
  concept="Deployment of payments bank funds",
  explanation="Since payments banks cannot lend, the 2014 licensing guidelines required them to invest at least 75% "
              "of their demand deposit balances in SLR-eligible government securities or T-bills with maturity up to "
              "one year, and allowed at most 25% in current and time deposits with other scheduled commercial banks.",
  steps=["≥ 75% in SLR-eligible G-secs/T-bills (≤ 1 year)", "≤ 25% in deposits with other banks"],
  why="25% is the maximum in bank deposits; 50% and 100% are not the prescribed figures.",
  facts=[fact6("Payments bank licensing guidelines: invest minimum 75% of demand deposit balances in SLR-eligible "
               "G-secs/T-bills with maturity up to one year and hold maximum 25% in deposits with other SCBs",
               PB_GUIDE)])

assert 180000 + 50000 > 200000
Q(T, "Deposit limit", "Advanced",
  "A customer of a payments bank has a balance of ₹1.8 lakh and receives a credit of ₹50,000 during the day. What "
  "must the payments bank ensure?",
  ["Not more than ₹2 lakh remains at the end of the day; the excess may be swept to a partner bank account with the "
   "customer's prior consent",
   "It must reject the ₹50,000 credit, because the balance can never exceed ₹2 lakh even during the day",
   "It can keep ₹2.3 lakh, because the limit applies only to savings accounts opened after 2021",
   "It must convert the excess into a fixed deposit with the payments bank"],
  concept="Applying the end-of-day balance limit",
  explanation="The ₹2 lakh limit applies to the balance at the end of the day, not to intraday credits. 1.8 + 0.5 = "
              "₹2.3 lakh, so ₹30,000 cannot stay overnight. A payments bank may act as a BC of another bank and, "
              "with the customer's prior written consent, sweep the excess into the customer's account with that "
              "bank. Payments banks cannot accept term deposits, so a fixed deposit is not possible.",
  steps=["End-of-day balance would be ₹2.3 lakh > ₹2 lakh", "Excess ₹30,000 must leave by end of day",
         "Route: sweep to partner bank with prior consent"],
  why="The cap is an end-of-day limit, applies to all individual customers, and payments banks cannot take fixed "
      "deposits.",
  computed=True, current=ca("2021-04-07"),
  facts=[fact("Maximum balance of ₹2,00,000 per individual customer at the end of the day; PBs may act as BCs of "
              "other banks; sweep arrangements need the customer's prior written consent", PB_MD),
         fact("Payments banks may accept current and savings deposits; lending is not permitted", PB_GUIDE)])

# ================================================================= 23. Small Finance Banks (1 / 2 / 1)
T = "Small Finance Banks"
SFB25 = ca("2025-11-28")
Q(T, "Licensing norms", "Basic",
  "Under the RBI (Small Finance Banks – Licensing) Guidelines, 2025, what is the minimum paid-up voting equity "
  "capital/net worth for a small finance bank?",
  ["₹300 crore", "₹200 crore", "₹100 crore", "₹500 crore"],
  concept="SFB licensing: capital",
  explanation="The 2025 guidelines (28 November 2025) set the minimum paid-up voting equity capital/net worth of an "
              "SFB at ₹300 crore. The 2019 on-tap guidelines had prescribed ₹200 crore. UCBs converting into SFBs "
              "may start with ₹150 crore and must reach ₹300 crore within five years.",
  steps=["2019 guidelines: ₹200 crore", "2025 guidelines: ₹300 crore"],
  why="₹200 crore is the superseded 2019 figure; ₹100 crore is the payments bank figure; ₹500 crore is not an SFB "
      "norm.",
  current=SFB25,
  facts=[fact("Minimum paid-up voting equity share capital/net worth for SFBs shall be ₹300 crore (Guidelines, 2025)",
              SFB_MD)])
Q(T, "PSL targets", "Intermediate",
  "What is the overall priority sector lending requirement for small finance banks under the current framework?",
  ["60% of ANBC or CEOBSE, whichever is higher", "75% of ANBC", "40% of ANBC or CEOBSE, whichever is higher",
   "50% of ANBC"],
  concept="PSL for SFBs",
  explanation="SFBs must extend 60% of ANBC or CEOBSE (whichever is higher) to the priority sector: 40% is "
              "allocated to the various PSL sub-sectors as for other banks, and the remaining 20% can go to any one "
              "or more sub-sectors where the bank has a competitive advantage. The earlier on-tap guidelines "
              "required 75% of ANBC.",
  steps=["Current SFB PSL: 60%", "Split: 40% as per sub-targets + 20% flexible"],
  why="75% of ANBC was the earlier SFB requirement (and is the current RRB target); 40% is for domestic SCBs.",
  current=SFB25,
  facts=[fact("SFB to extend 60 per cent of ANBC or CEOBSE to PSL sectors; 40% to sub-sectors and balance 20% to "
              "any sub-sector of competitive advantage", SFB_MD),
         fact("PSL Directions 2025: total PSL target for SFBs 60%", PSL_MD)])
Q(T, "Licensing norms", "Intermediate",
  "What minimum share of a small finance bank's loan portfolio must consist of loans and advances of up to ₹25 lakh?",
  ["50%", "25%", "40%", "75%"],
  concept="Small-ticket lending by SFBs",
  explanation="To keep SFBs focused on small borrowers, at least 50% of their loan portfolio must consist of loans "
              "and advances of up to ₹25 lakh, on an ongoing basis.",
  steps=["Loans ≤ ₹25 lakh must be ≥ 50% of the portfolio"],
  why="25%, 40% and 75% are not the prescribed share.",
  current=SFB25,
  facts=[fact("At least 50 per cent of an SFB's loan portfolio should constitute loans and advances of up to ₹25 "
              "lakh on an ongoing basis", SFB_MD)])
Q(T, "Licensing norms", "Advanced",
  "Consider the following statements under the SFB Licensing Guidelines, 2025:\nI. Promoters must hold at least 40% "
  "of the paid-up voting equity capital for the first five years.\nII. Listing is mandatory within eight years of "
  "the SFB commencing operations.\nIII. An SFB gets scheduled bank status only after completing five years of "
  "operations.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="SFB ownership and status",
  explanation="Promoters must hold at least 40% for the first five years, bringing it down to 26% within 15 years "
              "(I is right). Listing is mandatory within eight years of commencing operations (II is right). SFBs "
              "get scheduled bank status once they commence operations, not after five years (III is wrong).",
  steps=["I: correct", "II: correct", "III: wrong (scheduled status on commencement)"],
  current=SFB25,
  facts=[fact("Promoters to hold minimum 40% for first five years, reduce to 26% within 15 years; listing mandatory "
              "within eight years; scheduled bank status once they commence operations", SFB_MD)])

# ================================================================= 24. Financial Markets (2 / 3 / 2)
T = "Financial Markets"
Q(T, "Structure and regulators", "Basic",
  "Which body regulates the pension sector, including the National Pension System and Atal Pension Yojana?",
  ["PFRDA", "IRDAI", "SEBI", "NABARD"],
  concept="Financial sector regulators",
  explanation="The Pension Fund Regulatory and Development Authority (PFRDA) regulates the pension sector. It "
              "administers APY under the architecture of the National Pension System. Insurance is regulated by "
              "IRDAI, securities markets by SEBI, and banking and money markets by RBI.",
  steps=["Pensions → PFRDA"],
  why="IRDAI regulates insurance, SEBI securities markets, and NABARD is a development bank.",
  facts=[fact("APY is administered by PFRDA under the overall architecture of the National Pension System",
              APY_FAQ)])
Q(T, "Structure and regulators", "Basic",
  "The Financial Stability and Development Council (FSDC) is chaired by:",
  ["The Union Finance Minister", "The RBI Governor", "The Chairman of SEBI", "The Prime Minister"],
  concept="FSDC",
  explanation="The FSDC was set up by Government notification on 30 December 2010 to strengthen financial "
              "stability, financial sector development and inter-regulatory coordination. It is chaired by the "
              "Union Finance Minister; its members include the RBI Governor and the heads of SEBI, IRDAI and PFRDA. "
              "Its Sub-Committee is chaired by the RBI Governor.",
  steps=["FSDC chair = Finance Minister", "FSDC Sub-Committee chair = RBI Governor"],
  why="The RBI Governor chairs the Sub-Committee, not the Council; SEBI's chairman is a member.",
  facts=[fact("FSDC set up by notification of 30 December 2010, chaired by the Union Finance Minister", FSDC_PIB)])
Q(T, "Structure and regulators", "Intermediate",
  "SEBI was first constituted as a non-statutory body in 1988. When did it become a statutory body?",
  ["When the SEBI Act, 1992 came into force on 30 January 1992", "In 1988 itself, by an Act of Parliament",
   "On 1 April 1995, when NSE began trading", "In 1999, along with IRDA"],
  concept="Evolution of SEBI",
  explanation="SEBI was constituted on 12 April 1988 by a Government resolution as a non-statutory body. It became "
              "a statutory body when the SEBI Act, 1992 came into force on 30 January 1992, with the mandate to "
              "protect investors and develop and regulate the securities market.",
  steps=["1988: non-statutory (Government resolution)", "30 January 1992: statutory under SEBI Act"],
  why="The 1988 body was created by resolution, not by an Act; NSE and IRDA dates are unrelated.",
  facts=[fact("SEBI constituted as a non-statutory body on April 12, 1988; SEBI Act, 1992 came into force on January "
              "30, 1992", SEBI_ABOUT)])
Q(T, "Structure and regulators", "Intermediate",
  "Where is the headquarters of the International Financial Services Centres Authority (IFSCA), the unified "
  "regulator for India's IFSC?",
  ["GIFT City, Gandhinagar", "Bandra-Kurla Complex, Mumbai", "New Delhi", "Hyderabad"],
  concept="IFSCA",
  explanation="IFSCA was established on 27 April 2020 under the IFSCA Act, 2019 and is headquartered at GIFT City, "
              "Gandhinagar (Gujarat). It regulates financial products, services and institutions in the IFSC.",
  steps=["IFSCA HQ: GIFT City, Gandhinagar"],
  why="Mumbai hosts SEBI and RBI; Hyderabad hosts IRDAI's head office.",
  facts=[fact("IFSCA established on April 27, 2020 under the IFSCA Act, 2019; headquartered at GIFT City, "
              "Gandhinagar", IFSCA)])
Q(T, "Structure and regulators", "Intermediate",
  "In which year did the National Stock Exchange commence operations?",
  ["1994", "1992", "1988", "2000"],
  concept="Development of Indian capital markets",
  explanation="NSE commenced operations in June 1994 (its equity segment in November 1994), introducing "
              "screen-based nationwide trading. 1992 is when the SEBI Act came into force.",
  steps=["NSE: June 1994"],
  why="1992 is the SEBI Act; 1988 is SEBI's non-statutory start; 2000 has no link to NSE's start.",
  facts=[fact("Jun 1994: National Stock Exchange commenced operations", CHRON_91)])
Q(T, "Structure and regulators", "Advanced",
  "Which of the following pairs of a financial activity and its regulator is INCORRECTLY matched?",
  ["Issue of commercial paper – SEBI", "Mutual funds – SEBI", "Pension funds under NPS – PFRDA",
   "Life insurance companies – IRDAI"],
  concept="Division of regulatory jurisdiction",
  explanation="Commercial paper is a money market instrument; RBI issues the directions governing its issue, so "
              "matching CP with SEBI is incorrect. Mutual funds are regulated by SEBI, pension funds under NPS by "
              "PFRDA and insurers by IRDAI.",
  steps=["CP → RBI (money market)", "MFs → SEBI", "NPS → PFRDA", "Insurance → IRDAI"],
  why="The other three pairs are correctly matched.",
  facts=[fact("RBI's directions define commercial paper as an unsecured money market instrument with tenor of seven "
              "days to one year", CP_2025),
         fact("SEBI's mandate: protect investors and develop and regulate the securities market", SEBI_ABOUT),
         fact("IRDAI is the statutory regulator of the insurance sector", IRDAI)])
Q(T, "Structure and regulators", "Advanced",
  "Consider the following statements:\nI. Before IFSCA, financial business in GIFT IFSC was regulated separately "
  "by RBI, SEBI, IRDAI and PFRDA.\nII. IFSCA was established under the International Financial Services Centres "
  "Authority Act, 2019.\nIII. IFSCA functions as a department of SEBI.\nWhich of the above is/are correct?",
  ["I and II only", "II only", "I and III only", "I, II and III"],
  concept="Unified regulation of IFSCs",
  explanation="Earlier, the domestic regulators (RBI, SEBI, PFRDA and IRDAI) each regulated business in the IFSC. "
              "IFSCA, set up under the IFSCA Act, 2019, became the unified regulator, with their powers vested in it "
              "for IFSC entities. It is an independent statutory authority, not a part of SEBI.",
  steps=["I: correct", "II: correct", "III: wrong (independent statutory authority)"],
  facts=[fact("IFSCA established under the IFSCA Act, 2019", IFSCA),
         fact("Domestic regulators RBI, SEBI, PFRDA and IRDAI regulated business in IFSC before IFSCA; IFSCA became "
              "the unified regulator", IFSCA_CP)])

# ================================================================= 25. Money Market (2 / 3 / 2)
T = "Money Market"
Q(T, "Instruments: T-bills, CP, CD, call money", "Basic",
  "In the inter-bank money market, 'call money' refers to borrowing and lending of funds for:",
  ["Overnight", "2 to 14 days", "15 days to one year", "More than one year"],
  concept="Call, notice and term money",
  explanation="Call money is for overnight funds; notice money for 2–14 days; term money for 15 days to one year. "
              "Participants are scheduled commercial banks (excluding RRBs), co-operative banks and primary "
              "dealers.",
  steps=["Call = overnight", "Notice = 2–14 days", "Term = 15 days–1 year"],
  why="2–14 days is notice money; 15 days–1 year is term money; over one year is not the money market.",
  facts=[fact("Call money: deals in overnight funds; notice money: 2-14 days; term money: 15 days-1 year", MM_2016)])
Q(T, "Instruments: T-bills, CP, CD, call money", "Basic",
  "How are Treasury Bills issued and redeemed?",
  ["Issued at a discount and redeemed at face value", "Issued at face value and pay half-yearly interest",
   "Issued at a premium and redeemed at a discount", "Issued at face value and redeemed at a premium"],
  concept="Treasury Bills",
  explanation="T-bills are zero-coupon short-term instruments of the Government of India, issued in 91-day, "
              "182-day and 364-day tenors. They pay no interest; the investor's return is the difference between "
              "the discounted issue price and the face value received at maturity.",
  steps=["No coupon", "Buy below face value, receive face value at maturity"],
  why="Half-yearly coupons are paid on dated securities, not T-bills; premium issue/discount redemption makes no "
      "sense for a zero-coupon bill.",
  facts=[fact("Treasury bills are zero coupon securities issued at a discount and redeemed at face value; tenors 91, "
              "182 and 364 days", GSEC_FAQ)])
Q(T, "Instruments: T-bills, CP, CD, call money", "Intermediate",
  "'Notice money' in the inter-bank market refers to unsecured borrowing and lending for a period of:",
  ["2 to 14 days", "Overnight", "15 days to 90 days", "91 days to one year"],
  concept="Notice money",
  explanation="Deals for 2 to 14 days are notice money; overnight deals are call money; 15 days to one year is term "
              "money. Interest rates in these segments are decided freely by the participants.",
  steps=["Notice money tenor: 2–14 days"],
  why="Overnight is call money; 15 days and above is term money.",
  facts=[fact("Notice money: deals in funds for 2-14 days", MM_2016)])
Q(T, "Instruments: T-bills, CP, CD, call money", "Intermediate",
  "What is the permitted original tenor of Commercial Paper (CP) under RBI's directions?",
  ["7 days to one year", "1 day to 90 days", "15 days to 3 years", "91 days to 364 days only"],
  concept="Commercial Paper",
  explanation="CP is an unsecured money market instrument issued as a promissory note by companies and other "
              "eligible issuers. Its original tenor must be between seven days and one year.",
  steps=["CP tenor: minimum 7 days, maximum 1 year"],
  why="The other ranges are not CP tenors; 91–364 days describes T-bills.",
  facts=[fact("CP is an unsecured money market instrument issued as a promissory note; original tenor between seven "
              "days and one year", CP_2025)])
Q(T, "Instruments: T-bills, CP, CD, call money", "Intermediate",
  "Which of the following CANNOT issue Certificates of Deposit (CDs)?",
  ["Local Area Banks", "Scheduled commercial banks", "Regional Rural Banks", "Small Finance Banks"],
  concept="Certificates of Deposit",
  explanation="CDs are negotiable money market instruments issued against funds deposited for a specified period. "
              "Under RBI's Certificate of Deposit Directions, 2021, they may be issued by Scheduled Commercial Banks, "
              "Regional Rural Banks and Small Finance Banks (All-India Financial Institutions under a separate "
              "circular). Local Area Banks are not among the eligible issuers. The earlier 2016 rule had excluded "
              "RRBs too; the 2021 Directions added them.",
  steps=["CD issuers (2021 Directions, clause 3): SCBs, RRBs, SFBs; AIFIs as separately permitted",
         "Local Area Banks are not listed"],
  why="Scheduled commercial banks, RRBs and small finance banks are all eligible issuers under the 2021 Directions.",
  facts=[{"claim": "CD Directions 2021, clause 3(a): CDs may be issued by Scheduled Commercial Banks, Regional Rural "
                   "Banks and Small Finance Banks; Local Area Banks are not listed",
          "source_url": "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12108&Mode=0",
          "checked_on": "2026-11-07"}])

price, days = F(985, 10), 91
yld = (100 - price) / price * F(365, days) * 100
disc = (100 - price) / 100 * F(365, days) * 100
assert round(float(yld), 2) == 6.11 and round(float(disc), 2) == 6.02 and round(float((100 - price) / price * 100), 2) == 1.52
Q(T, "Instruments: T-bills, CP, CD, call money", "Advanced",
  "A 91-day Treasury Bill with a face value of ₹100 is bought at ₹98.50 and held to maturity. What is the annualised "
  "yield (approx.), using a 365-day year?",
  ["1.52%", "6.02%", "6.11%", "6.25%"],
  answer="C",
  concept="Yield on a discounted instrument",
  explanation="Return = face value − price = ₹1.50 over 91 days on an investment of ₹98.50. Yield = (1.50 ÷ 98.50) × "
              "(365 ÷ 91) × 100 ≈ 6.11%. Dividing by the face value instead of the price gives the discount rate "
              "(≈ 6.02%), which understates the investor's yield.",
  steps=["Gain = 100 − 98.50 = ₹1.50", "Period return = 1.50 ÷ 98.50 = 1.523%", "Annualised = 1.523% × 365/91 ≈ 6.11%"],
  why="1.52% is not annualised; 6.02% divides by face value (discount rate); 6.25% has no basis.",
  computed=True,
  facts=[fact("T-bills are issued at a discount and redeemed at face value; 91-day tenor", GSEC_FAQ)])
Q(T, "Instruments: T-bills, CP, CD, call money", "Advanced",
  "Consider the following statements:\nI. Commercial paper is an unsecured instrument issued in the form of a "
  "promissory note.\nII. Term money refers to inter-bank deals for 15 days to one year.\nIII. Mutual funds and "
  "insurance companies can borrow in the call money market.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Money market instruments and participants",
  explanation="I is right: CP is unsecured and issued as a promissory note. II is right: term money covers 15 days "
              "to one year. III is wrong: only scheduled commercial banks (excluding RRBs), co-operative banks and "
              "primary dealers can borrow and lend in the call/notice money market; other non-bank institutions "
              "are not permitted.",
  steps=["I: correct", "II: correct", "III: wrong (non-banks other than PDs are not permitted)"],
  facts=[fact("CP is an unsecured money market instrument issued as a promissory note", CP_2025),
         fact("Term money: 15 days-1 year; call/notice money participants are SCBs (excluding RRBs), co-operative "
              "banks and PDs; non-bank institutions other than PDs not permitted", MM_2016)])

# ================================================================= 26. Capital Market (2 / 3 / 2)
T = "Capital Market"
Q(T, "Indices", "Basic",
  "How many companies make up the BSE Sensex?",
  ["30", "50", "100", "500"],
  concept="Stock market indices",
  explanation="The Sensex tracks 30 large, liquid and financially sound companies listed on BSE, across key sectors. "
              "The Nifty 50 of NSE has 50 companies.",
  steps=["Sensex = 30 stocks", "Nifty = 50 stocks"],
  why="50 is the Nifty; 100 and 500 are other broader indices.",
  facts=[fact("Sensex tracks the 30 largest, most liquid and financially sound companies listed on BSE", SENSEX)])
Q(T, "Primary and secondary market", "Basic",
  "An Initial Public Offering (IPO) by a company is a transaction in the:",
  ["Primary market", "Secondary market", "Money market", "Derivatives market"],
  concept="Primary versus secondary market",
  explanation="In the primary market, securities are issued for the first time and the money goes to the issuer, as "
              "in an IPO. In the secondary market, existing securities are traded between investors on stock "
              "exchanges. In public issues, payment is made through ASBA, so the amount is only blocked in the "
              "investor's bank account until allotment.",
  steps=["New issue → primary market"],
  why="The secondary market trades already-issued shares; the money market deals in short-term debt; derivatives "
      "are contracts on underlying assets.",
  facts=[fact("In all public issues like IPOs, FPOs and rights issues, ASBA is the mandatory mode of payment",
              ICDR_FAQ)])
Q(T, "Indices", "Intermediate",
  "What are the base date and base value of the Nifty 50 index?",
  ["3 November 1995; 1,000", "1 April 1979; 100", "3 November 1995; 100", "1978-79; 1,000"],
  concept="Base of the Nifty 50",
  explanation="The Nifty 50 has a base date of 3 November 1995 (the start of equity trading on NSE) and a base value "
              "of 1,000. It was launched on 22 April 1996 and uses free-float market capitalisation. The Sensex has "
              "a base of 1978-79 = 100.",
  steps=["Nifty 50: base 3 Nov 1995 = 1,000", "Sensex: base 1978-79 = 100"],
  why="Base 100 and 1978-79 belong to the Sensex.",
  facts=[fact("Nifty 50: base date November 3, 1995, base value 1000, 50 constituents", NIFTY)])
Q(T, "SEBI", "Intermediate",
  "From which date did all securities in India's equity cash market move to the T+1 rolling settlement cycle?",
  ["27 January 2023", "1 April 2021", "25 February 2022", "1 January 2025"],
  concept="Settlement cycle",
  explanation="SEBI introduced T+1 in a phased manner from 2021-22; all scrips moved to T+1 rolling settlement from "
              "27 January 2023, making India one of the first major markets to adopt T+1.",
  steps=["Phased roll-out from 2021-22", "Fully on T+1 from 27 January 2023"],
  why="The other dates do not mark the completion of the T+1 transition.",
  facts=[fact("The transition to T+1 settlement was completed in January 2023 after a phased implementation that "
              "began in November 2021", T1_PIB)])
Q(T, "Primary and secondary market", "Intermediate",
  "In a public issue, individual investors applying through intermediaries can use UPI as the payment mechanism "
  "under ASBA for application amounts up to:",
  ["₹5 lakh", "₹2 lakh", "₹1 lakh", "₹10 lakh"],
  concept="ASBA and UPI in public issues",
  explanation="ASBA is mandatory in public issues. For individual investors applying through intermediaries "
              "(brokers, depository participants, RTAs, syndicate members), UPI is one of the ASBA mechanisms for "
              "applications up to ₹5 lakh (raised from ₹2 lakh from April 2022). The retail individual investor "
              "category remains capped at ₹2 lakh.",
  steps=["ASBA mandatory", "UPI with ASBA: up to ₹5 lakh for individuals"],
  why="₹2 lakh is the retail investor category cap, not the UPI limit; ₹1 lakh and ₹10 lakh are not the limits.",
  current=ca("2022-04-05"),
  facts=[fact("ASBA includes UPI as a mechanism for individual investors through intermediaries for applications up "
              "to ₹5 lakh", ICDR_FAQ)])
Q(T, "Primary and secondary market", "Advanced",
  "An individual investor applies for shares worth ₹3 lakh in an IPO through her broker, paying through UPI. In which "
  "investor category will her application be considered?",
  ["Non-Institutional Investors (NII)", "Retail Individual Investors (RII)", "Qualified Institutional Buyers (QIB)",
   "Anchor investors"],
  concept="Investor categories in IPOs",
  explanation="The retail individual investor category is capped at applications of up to ₹2 lakh. An individual's "
              "application above ₹2 lakh and up to ₹5 lakh (which can still be paid through UPI under ASBA) falls "
              "in the Non-Institutional Investors category.",
  steps=["RII cap = ₹2 lakh", "₹3 lakh > ₹2 lakh → NII", "UPI is still allowed up to ₹5 lakh"],
  why="RII is only up to ₹2 lakh; QIBs and anchor investors are institutional categories.",
  current=ca("2022-04-05"),
  facts=[fact("Retail individual investors limit continues up to ₹2 lakh; applications above ₹2 lakh and up to ₹5 "
              "lakh are considered under the Non-Institutional Investors category", ICDR_FAQ)])
Q(T, "Indices", "Advanced",
  "Consider the following statements:\nI. The base year of the BSE Sensex is 1978-79, with a base value of 100.\n"
  "II. The Nifty 50 has been computed using the free-float market capitalisation method since June 2009.\nIII. The "
  "Nifty 50 is rebalanced every quarter.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Construction of major indices",
  explanation="The Sensex has base year 1978-79 = 100 (I is right). Nifty 50 constituents were originally weighted "
              "by full market capitalisation; from 26 June 2009 the free-float method has been used (II is right). "
              "The Nifty 50 is rebalanced semi-annually, with cut-off dates of 31 January and 31 July (III is "
              "wrong).",
  steps=["I: correct", "II: correct", "III: wrong (semi-annual rebalancing)"],
  facts=[fact("Sensex base year 1978-79 with base value 100", SENSEX),
         fact("Nifty 50 moved to free float methodology from June 26, 2009; rebalanced semi-annually", NIFTY)])

# ================================================================= 27. Insurance (2 / 3 / 2)
T = "Insurance"
Q(T, "IRDAI", "Basic",
  "Where is the head office of the Insurance Regulatory and Development Authority of India (IRDAI)?",
  ["Hyderabad", "Mumbai", "New Delhi", "Chennai"],
  concept="IRDAI",
  explanation="IRDAI's head office is in Hyderabad (Financial District, Nanakramguda, Gachibowli). It regulates and "
              "develops the insurance sector in India.",
  steps=["IRDAI HQ = Hyderabad"],
  why="Mumbai hosts RBI and SEBI; New Delhi and Chennai are not IRDAI's head office.",
  facts=[fact("IRDAI head office: Sy No. 115/1, Financial District, Nanakramguda, Gachibowli, Hyderabad",
              IRDAI_ADDR)])
Q(T, "IRDAI", "Basic",
  "IRDAI is a statutory body set up under which Act?",
  ["Insurance Regulatory and Development Authority Act, 1999", "Insurance Act, 1938",
   "Life Insurance Corporation Act, 1956", "General Insurance Business (Nationalisation) Act, 1972"],
  concept="Legal basis of IRDAI",
  explanation="IRDAI is a statutory body created under the IRDA Act, 1999 for the overall supervision and "
              "development of the insurance sector. Its powers and functions derive from the IRDA Act, 1999 and the "
              "Insurance Act, 1938.",
  steps=["IRDAI → IRDA Act, 1999"],
  why="The Insurance Act, 1938 is the main insurance law but did not create IRDAI; the 1956 and 1972 Acts "
      "nationalised life and general insurance.",
  facts=[fact("IRDAI is a statutory body created under the IRDA Act, 1999; powers from the IRDA Act and the "
              "Insurance Act, 1938", IRDAI)])
Q(T, "Government insurance schemes", "Intermediate",
  "Under Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY), what life cover is given and at what annual premium?",
  ["₹2 lakh for ₹436 a year", "₹2 lakh for ₹20 a year", "₹1 lakh for ₹330 a year", "₹5 lakh for ₹436 a year"],
  concept="PMJJBY",
  explanation="PMJJBY offers a one-year renewable life cover of ₹2 lakh for death due to any cause, at a premium of "
              "₹436 a year, for people aged 18–50 with a bank or post office account. The cover period is 1 June "
              "to 31 May.",
  steps=["Cover: ₹2 lakh (death from any cause)", "Premium: ₹436 per year", "Age: 18–50"],
  why="₹20 is the PMSBY premium; ₹330 was PMJJBY's premium before June 2022; ₹5 lakh is not the cover.",
  current=ca("2022-06-01"),
  facts=[fact("PMJJBY: life cover ₹2 lakh, age 18-50, annual premium ₹436", PMJJBY)])
Q(T, "Government insurance schemes", "Intermediate",
  "What is the annual premium under Pradhan Mantri Suraksha Bima Yojana (PMSBY)?",
  ["₹20", "₹12", "₹436", "₹330"],
  concept="PMSBY",
  explanation="PMSBY is a one-year renewable accident insurance scheme for people aged 18–70 with a bank account. "
              "The premium is ₹20 a year (revised from ₹12 in June 2022).",
  steps=["PMSBY premium = ₹20 a year"],
  why="₹12 was the earlier premium; ₹436 is PMJJBY's premium (₹330 earlier).",
  current=ca("2022-06-01"),
  facts=[fact("PMSBY: age 18-70 with bank account; annual premium ₹20", PMSBY)])
Q(T, "Life and general insurance", "Intermediate",
  "Besides the IRDA Act, 1999, which older Act is the principal law governing the business of insurance in India "
  "and the source of many of IRDAI's powers?",
  ["Insurance Act, 1938", "Indian Contract Act, 1872", "Companies Act, 2013", "Banking Regulation Act, 1949"],
  concept="Insurance law",
  explanation="The Insurance Act, 1938 is the principal legislation for insurance business (life and general). "
              "IRDAI's powers and functions are laid down in the IRDA Act, 1999 and the Insurance Act, 1938.",
  steps=["Principal insurance law: Insurance Act, 1938"],
  why="The Contract Act and Companies Act are general laws; the BR Act governs banks.",
  facts=[fact("IRDAI's powers and functions are derived from the IRDA Act, 1999 and the Insurance Act, 1938",
              IRDAI)])
Q(T, "Government insurance schemes", "Advanced",
  "Two PMSBY subscribers meet with accidents. Arun suffers irrecoverable loss of sight of one eye (partial "
  "disability); Bina suffers permanent total disability. What do they receive?",
  ["Arun ₹1 lakh; Bina ₹2 lakh", "₹2 lakh each", "Arun ₹2 lakh; Bina ₹1 lakh", "Nothing, as PMSBY covers only death"],
  concept="PMSBY benefits",
  explanation="PMSBY pays ₹2 lakh on accidental death or permanent total disability and ₹1 lakh on permanent partial "
              "disability. So Arun (partial) gets ₹1 lakh and Bina (total) gets ₹2 lakh.",
  steps=["Death or total disability → ₹2 lakh", "Partial disability → ₹1 lakh"],
  why="PMSBY is an accident cover for both death and disability, with a lower amount for partial disability.",
  computed=True,
  facts=[fact("PMSBY: ₹2 lakh on death or permanent total disability and ₹1 lakh on partial disability", PMSBY)])
Q(T, "Life and general insurance", "Advanced",
  "Consider the following statements:\nI. The Sabka Bima Sabki Raksha (Amendment of Insurance Laws) Act, 2025 raised "
  "the FDI limit in Indian insurance companies from 74% to 100%.\nII. As announced in the Union Budget 2025-26, the "
  "higher limit is for companies that invest the entire premium in India.\nIII. IRDAI's head office is in Mumbai.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Insurance sector reforms, 2025",
  explanation="Parliament passed the Sabka Bima Sabki Raksha (Amendment of Insurance Laws) Bill on 17 December 2025, "
              "allowing up to 100% FDI in insurance companies (from 74%), and the related foreign investment rules "
              "were notified on 30 December 2025. The Budget had said the enhanced limit is for companies investing "
              "the entire premium in India. IRDAI's head office is in Hyderabad, so III is wrong.",
  steps=["I: correct", "II: correct", "III: wrong (Hyderabad)"],
  current=ca("2025-12-30"),
  facts=[fact("Sabka Bima Sabki Raksha (Amendment of Insurance Laws) Bill, 2025 passed by Parliament; allows up to "
              "100% FDI in insurance companies", FDI_INS),
         fact("Budget 2025-26: FDI limit for insurance raised from 74 to 100 per cent for companies that invest the "
              "entire premium in India", FDI_BUDGET),
         fact("IRDAI head office is in Hyderabad", IRDAI_ADDR)])

# ================================================================= 28. Mutual Funds (2 / 2 / 2)
T = "Mutual Funds"
Q(T, "AMFI", "Basic",
  "The Association of Mutual Funds in India (AMFI), the industry body of SEBI-registered asset management companies, "
  "was incorporated in:",
  ["1995", "1963", "1992", "2003"],
  concept="AMFI",
  explanation="AMFI was incorporated on 22 August 1995 as a not-for-profit organisation under Section 25 of the "
              "Companies Act, 1956 (now Section 8 of the 2013 Act), to develop the mutual fund industry on "
              "professional, healthy and ethical lines.",
  steps=["AMFI: 22 August 1995"],
  why="1963 is when UTI was set up; 1992 is the SEBI Act; 2003 is unrelated.",
  facts=[fact("AMFI was incorporated on August 22, 1995 as a non-profit organisation under Section 25 of the "
              "Companies Act, 1956", AMFI)])
Q(T, "Types", "Basic",
  "What is the lock-in period of an Equity Linked Savings Scheme (ELSS) of a mutual fund?",
  ["3 years", "1 year", "5 years", "No lock-in"],
  concept="ELSS",
  explanation="ELSS is an open-ended equity scheme with a statutory lock-in of three years from the date of "
              "allotment, carrying a tax benefit. Units cannot be redeemed or switched out before the lock-in ends.",
  steps=["ELSS lock-in = 3 years from allotment"],
  why="One and five years are not the ELSS lock-in, and an ELSS does have a statutory lock-in.",
  facts=[fact("ELSS: open-ended equity linked saving scheme with a statutory lock-in of 3 years from the date of "
              "allotment", ELSS_SID)])
Q(T, "AMFI", "Intermediate",
  "Under SEBI's mutual fund regulations, mutual fund agents and distributors must register with which body and "
  "obtain which number?",
  ["AMFI; AMFI Registration Number (ARN)", "SEBI; Legal Entity Identifier (LEI)", "NSDL; Client ID",
   "RBI; Unique Transaction Reference (UTR)"],
  concept="Mutual fund distribution",
  explanation="As per SEBI's mutual fund regulations, all mutual fund agents and distributors must be registered "
              "with AMFI and obtain an AMFI Registration Number (ARN) before selling mutual fund schemes.",
  steps=["Distributor registration: AMFI → ARN"],
  why="LEI identifies legal entities in financial transactions; Client IDs are depository accounts; UTR identifies "
      "RTGS transactions.",
  facts=[fact("As per SEBI MF regulations, all mutual fund agents/distributors need to be registered with AMFI and "
              "obtain an AMFI Registration Number (ARN)", AMFI)])
Q(T, "Types", "Intermediate",
  "Under SEBI's scheme categorisation, a 'mid cap' company is one ranked between ____ in terms of full market "
  "capitalisation.",
  ["101st and 250th", "1st and 100th", "51st and 150th", "251st and 500th"],
  concept="Large, mid and small cap",
  explanation="SEBI defines large caps as the 1st–100th companies by full market capitalisation, mid caps as the "
              "101st–250th, and small caps as the 251st onwards. AMFI publishes the list, and funds rebalance "
              "within a month of each update.",
  steps=["Large: 1–100", "Mid: 101–250", "Small: 251 onwards"],
  why="1–100 is large cap; 251st onwards is small cap; 51–150 is not a SEBI band.",
  facts=[fact("Large cap: 1st-100th; mid cap: 101st-250th; small cap: 251st company onwards in terms of full market "
              "capitalisation", MF_CAT)])

assets, liabilities, units = 250, 10, 12
nav = F(assets - liabilities, units)
assert nav == 20 and round(float(F(assets, units)), 2) == 20.83
Q(T, "NAV and SIP", "Advanced",
  "A mutual fund scheme holds securities with a market value of ₹250 crore and has liabilities (including accrued "
  "expenses) of ₹10 crore. It has 12 crore units outstanding. What is its NAV per unit?",
  ["₹19.17", "₹20.00", "₹20.83", "₹24.00"],
  answer="B",
  concept="Net Asset Value",
  explanation="NAV per unit = (market value of assets − liabilities) ÷ units outstanding = (250 − 10) ÷ 12 = "
              "240 ÷ 12 = ₹20.00. NAV is computed for every business day.",
  steps=["Net assets = 250 − 10 = ₹240 crore", "NAV = 240 ÷ 12 = ₹20.00"],
  why="₹20.83 ignores liabilities; ₹19.17 subtracts liabilities twice; ₹24.00 divides by 10 crore units.",
  computed=True,
  facts=[fact("NAV per unit = (assets − liabilities) ÷ number of units outstanding (SEBI example: ₹200 lakh − ₹10 "
              "lakh over 10 lakh units = ₹19)", NAV_SEBI),
         fact("NAV is the market value of the scheme's securities per unit, computed for each business day",
              NAV_AMFI)])

first_sip, april_sip = dt.date(2026, 1, 10), dt.date(2026, 4, 10)
unlock = april_sip.replace(year=april_sip.year + 3)
assert unlock == dt.date(2029, 4, 10)
Q(T, "NAV and SIP", "Advanced",
  "An investor started a monthly SIP in an ELSS on 10 January 2026. When can the units allotted from the instalment "
  "of 10 April 2026 be redeemed?",
  ["On or after 10 April 2029", "On or after 10 January 2029", "On or after 10 April 2027",
   "At any time, because SIP units carry no lock-in"],
  concept="ELSS lock-in for SIP instalments",
  explanation="The three-year ELSS lock-in runs from the allotment date of each set of units. In an SIP, every "
              "instalment is a separate allotment, so units allotted on 10 April 2026 are locked in until 10 April "
              "2029, regardless of when the SIP began.",
  steps=["Lock-in counted per allotment", "10 April 2026 + 3 years = 10 April 2029"],
  why="The SIP start date does not govern later instalments; one year is not the ELSS lock-in; SIP units are not "
      "exempt.",
  computed=True,
  facts=[fact("ELSS investments are subject to a statutory lock-in of 3 years from the date of allotment", ELSS_SID)])

# ================================================================= 29. Government Financial Schemes (2 / 3 / 2)
T = "Government Financial Schemes"
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Basic",
  "What range of guaranteed monthly pension can a subscriber choose under Atal Pension Yojana (APY)?",
  ["₹1,000 to ₹5,000", "₹500 to ₹3,000", "₹3,000 fixed", "₹1,000 to ₹10,000"],
  concept="Atal Pension Yojana",
  explanation="APY gives a guaranteed monthly pension of ₹1,000, 2,000, 3,000, 4,000 or 5,000 from age 60, as "
              "chosen by the subscriber. After the subscriber's death the spouse gets the same pension, and the "
              "nominee then receives the accumulated corpus.",
  steps=["APY pension options: ₹1,000–₹5,000 a month from age 60"],
  why="₹3,000 fixed is the PM-SYM pension; the other ranges are not APY options.",
  facts=[fact("APY: guaranteed pension of ₹1,000 to ₹5,000 per month from age 60; spouse gets the same pension",
              APY_FAQ)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Basic",
  "Under Pradhan Mantri MUDRA Yojana (PMMY), 'Shishu' loans are for amounts up to:",
  ["₹50,000", "₹5 lakh", "₹10 lakh", "₹20 lakh"],
  concept="PMMY categories",
  explanation="PMMY gives collateral-free loans to micro enterprises in four categories: Shishu (up to ₹50,000), "
              "Kishor (above ₹50,000 to ₹5 lakh), Tarun (above ₹5 lakh to ₹10 lakh) and Tarun Plus (above ₹10 lakh "
              "to ₹20 lakh).",
  steps=["Shishu ≤ ₹50,000"],
  why="₹5 lakh, ₹10 lakh and ₹20 lakh are the upper limits of Kishor, Tarun and Tarun Plus.",
  facts=[fact("Shishu covers loans up to ₹50,000; Kishor above ₹50,000 to ₹5 lakh; Tarun above ₹5 lakh to ₹10 lakh",
              MUDRA_PIB)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Intermediate",
  "Who is eligible for the 'Tarun Plus' category of PMMY loans (above ₹10 lakh and up to ₹20 lakh)?",
  ["Entrepreneurs who have availed and successfully repaid a previous loan under the Tarun category",
   "Any new entrepreneur with a project above ₹10 lakh", "Only women entrepreneurs",
   "Only enterprises in the manufacturing sector"],
  concept="Tarun Plus",
  explanation="Following the Union Budget 2024-25, the PMMY limit was raised from ₹10 lakh to ₹20 lakh with effect "
              "from 24 October 2024 through a new Tarun Plus category, available to entrepreneurs who have availed "
              "and successfully repaid previous loans under Tarun. Guarantee cover for these loans is given under "
              "the Credit Guarantee Fund for Micro Units (CGFMU).",
  steps=["Tarun Plus: ₹10–20 lakh", "Eligibility: successful repayment of an earlier Tarun loan"],
  why="New entrepreneurs, gender and sector are not the criteria for Tarun Plus.",
  current=ca("2024-10-24"),
  facts=[fact("Tarun Plus (₹10-20 lakh) for entrepreneurs who have availed and successfully repaid previous loans "
              "under Tarun, w.e.f. 24.10.2024; guarantee under CGFMU", MUDRA_GAZ)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Intermediate",
  "From 1 October 2022, which of the following persons is NOT eligible to open a new Atal Pension Yojana account?",
  ["A person who is or has been an income-tax payer", "A self-employed person aged 25",
   "A farm worker aged 39 with a savings account", "A woman homemaker aged 30 with a savings account"],
  concept="APY eligibility",
  explanation="APY is open to Indian citizens aged 18–40 with a savings bank account. From 1 October 2022, anyone "
              "who is or has been an income-tax payer cannot open a new APY account. Those who joined on or before "
              "30 September 2022 are not affected if they later pay income tax.",
  steps=["Age 18–40 + savings account", "Exclusion from 1 Oct 2022: income-tax payers"],
  why="The other three are within 18–40, have (or can have) savings accounts and are not stated to be taxpayers.",
  current=ca("2022-10-01"),
  facts=[fact("From 1 October 2022, any citizen who is or has been an income-tax payer is not eligible to open a new "
              "APY account", APY_FAQ)])
Q(T, "Credit guarantee schemes", "Intermediate",
  "Under the Credit Guarantee Scheme for Micro and Small Enterprises (CGTMSE), the guarantee ceiling was raised from "
  "₹5 crore to ____ with effect from 1 April 2025.",
  ["₹10 crore", "₹7.5 crore", "₹20 crore", "₹50 crore"],
  concept="Credit guarantee for MSEs",
  explanation="The Ministry of MSME's CGTMSE guarantees collateral-free credit to micro and small enterprises. Its "
              "guarantee ceiling was enhanced from ₹5 crore to ₹10 crore with effect from 1 April 2025, following "
              "the Union Budget 2025-26 announcement, and the annual guarantee fee was reduced.",
  steps=["Earlier ceiling ₹5 crore", "From 1 April 2025: ₹10 crore"],
  why="₹7.5 crore is the maximum risk borne on a ₹10 crore facility at 75% cover, not the ceiling; ₹20 crore and "
      "₹50 crore are not CGTMSE ceilings.",
  current=ca("2025-04-01"),
  facts=[fact("CGTMSE guarantee ceiling enhanced from ₹5 crore to ₹10 crore w.e.f. 01.04.2025", CGTMSE_PIB)])

loans = {40000: "Shishu", 300000: "Kishor", 800000: "Tarun", 1500000: "Tarun Plus"}
cat = lambda a: "Shishu" if a <= 50000 else "Kishor" if a <= 500000 else "Tarun" if a <= 1000000 else "Tarun Plus"
assert all(cat(a) == c for a, c in loans.items())
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Advanced",
  "Classify the following PMMY loans: (P) ₹40,000 to a vegetable vendor; (Q) ₹3 lakh to a tailoring unit; (R) ₹8 lakh "
  "to a small food-processing unit; (S) ₹15 lakh to an entrepreneur who has repaid an earlier Tarun loan.",
  ["P-Shishu, Q-Kishor, R-Tarun, S-Tarun Plus", "P-Shishu, Q-Tarun, R-Tarun, S-Tarun Plus",
   "P-Kishor, Q-Kishor, R-Tarun, S-Tarun", "P-Shishu, Q-Kishor, R-Tarun Plus, S-Tarun Plus"],
  concept="PMMY loan categories",
  explanation="Shishu: up to ₹50,000 → P. Kishor: above ₹50,000 to ₹5 lakh → Q (₹3 lakh). Tarun: above ₹5 lakh to "
              "₹10 lakh → R (₹8 lakh). Tarun Plus: above ₹10 lakh to ₹20 lakh for those who repaid a Tarun loan → S.",
  steps=["P ₹40,000 ≤ ₹50,000 → Shishu", "Q ₹3 lakh ≤ ₹5 lakh → Kishor", "R ₹8 lakh ≤ ₹10 lakh → Tarun",
         "S ₹15 lakh, earlier Tarun repaid → Tarun Plus"],
  why="₹3 lakh is Kishor, not Tarun; ₹8 lakh is Tarun, not Tarun Plus; ₹40,000 is Shishu.",
  computed=True, current=ca("2024-10-24"),
  facts=[fact("PMMY: Shishu up to ₹50,000; Kishor above ₹50,000 to ₹5 lakh; Tarun above ₹5 lakh to ₹10 lakh; Tarun "
              "Plus ₹10-20 lakh for those who repaid Tarun loans", MUDRA_PIB)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Advanced",
  "Which of the following persons can open a NEW Atal Pension Yojana account in November 2026?",
  ["Ramesh, 38, a daily-wage worker with a savings account, who has never paid income tax",
   "Sunita, 42, a homemaker with a savings account, who has never paid income tax",
   "Imran, 30, with a savings account, who paid income tax for 2024-25",
   "Kavya, 25, who has never paid income tax and has no bank or post office savings account"],
  concept="Applying APY eligibility",
  explanation="To join APY a person must be an Indian citizen aged 18–40, have a savings bank account, and (since "
              "1 October 2022) must not be or have been an income-tax payer. Ramesh meets all conditions. Sunita "
              "is over 40, Imran is a past income-tax payer, and Kavya has no savings account.",
  steps=["Check age 18–40", "Check savings account", "Check never an income-tax payer", "Only Ramesh qualifies"],
  why="Each of the others fails exactly one condition: age, tax status or savings account.",
  current=ca("2022-10-01"),
  facts=[fact("APY open to citizens aged 18-40 with a savings bank account; from 1 Oct 2022 income-tax payers are not "
              "eligible to open new accounts", APY_FAQ)])

# ================================================================= 30. RBI Circulars and Regulatory Updates (2 / 3 / 2)
T = "RBI Circulars and Regulatory Updates"
Q(T, "Recent RBI directions", "Basic",
  "On 28 November 2025, RBI consolidated its regulatory instructions into how many Master Directions?",
  ["244", "238", "100", "9,445"],
  concept="Consolidation of RBI regulations (2025)",
  explanation="RBI issued 244 consolidated Master Directions on 28 November 2025, organised by type of regulated "
              "entity, to serve as the single library of its regulations. About 9,445 circulars were withdrawn as "
              "a result. Draft versions (238) had been released on 10 October 2025 for comments.",
  steps=["Final: 244 Master Directions", "Circulars withdrawn: 9,445", "Drafts (Oct 2025): 238"],
  why="238 is the draft count; 9,445 is the number of circulars withdrawn.",
  facts=[fact("RBI issued 244 consolidated Master Directions on November 28, 2025; 9,445 circulars repealed or "
              "withdrawn; drafts of 238 directions issued in October 2025", CONSOL_PR)])
Q(T, "Recent RBI directions", "Basic",
  "In October 2026, RBI issued final directions to implement which Basel Committee standard, effective 1 April 2027?",
  ["The Leverage Ratio 2017 Standard", "The Basel I Accord", "The Liquidity Coverage Ratio 2013 Standard",
   "The Net Stable Funding Ratio 2014 Standard"],
  concept="Recent prudential updates",
  explanation="On 23 October 2026 RBI issued the Commercial Banks – Prudential Norms on Capital Adequacy Eleventh "
              "Amendment Directions, 2026, implementing the Basel Committee's Leverage Ratio 2017 Standard, after a "
              "draft on 7 August 2026. The instructions apply from 1 April 2027.",
  steps=["Oct 2026: final directions on Leverage Ratio 2017 Standard", "Effective 1 April 2027"],
  why="LCR and NSFR were implemented earlier (2015 onwards and 1 October 2021); Basel I dates from 1988.",
  facts=[fact("RBI issues guidelines on the implementation of the Leverage Ratio 2017 Standard; effective April 1, "
              "2027", LEV_2017_PR)])
Q(T, "Recent RBI directions", "Intermediate",
  "From which date will RBI's expected credit loss (ECL) based Commercial Banks (Asset Classification, Provisioning "
  "and Income Recognition) Directions, 2026 take effect?",
  ["1 April 2027", "1 April 2026", "1 October 2026", "1 January 2027"],
  concept="ECL framework",
  explanation="RBI issued the ECL-based directions on 27 April 2026. They take effect from 1 April 2027, replacing "
              "the incurred-loss IRACP norms; until then banks follow the 2025 IRACP Directions. The Standardised "
              "Approach for credit risk capital directions issued the same day also apply from 1 April 2027.",
  steps=["Issued 27 April 2026", "Effective 1 April 2027"],
  why="The other dates are not the commencement date.",
  current=ca("2026-04-27"),
  facts=[fact("Commercial Banks (Asset Classification, Provisioning and Income Recognition) Directions, 2026 issued "
              "April 27, 2026; effective April 1, 2027", ECL_MD)])
Q(T, "Recent RBI directions", "Intermediate",
  "Under an expected credit loss framework of the kind RBI has adopted for banks from April 2027, Stage 1 (performing) "
  "assets carry an allowance equal to:",
  ["12-month expected credit loss", "Lifetime expected credit loss", "100% of the outstanding amount",
   "No allowance at all"],
  concept="Staging under ECL",
  explanation="Under ECL, Stage 1 assets carry a 12-month ECL allowance; Stage 2 assets (significant increase in "
              "credit risk but not impaired) and Stage 3 assets (credit-impaired) carry lifetime ECL. RBI links "
              "Stage 3 to its existing NPA definition.",
  steps=["Stage 1 → 12-month ECL", "Stage 2 and 3 → lifetime ECL"],
  why="Lifetime ECL is for Stages 2 and 3; 100% is a loss-asset style provision; Stage 1 is not provision-free.",
  current=ca("2026-04-27"),
  facts=[fact("ECL framework: Stage 1 12-month ECL; Stage 2 and Stage 3 lifetime ECL; Stage 3 linked to NPA rules",
              ECL_PR)])
Q(T, "Recent RBI directions", "Intermediate",
  "Under RBI's April 2025 amendments to the Liquidity Coverage Ratio framework (effective 1 April 2026), funding from "
  "non-financial entities such as trusts, partnerships and LLPs now attracts a run-off rate of:",
  ["40%, instead of 100% earlier", "100%, instead of 40% earlier", "25%, instead of 50% earlier",
   "10%, instead of 5% earlier"],
  concept="LCR amendments, 2025",
  explanation="RBI narrowed the 'other legal entities' category to banks, insurers, financial institutions and "
              "financial-services entities. Non-financial entities such as trusts, partnerships and LLPs moved to "
              "the non-financial corporates category with a 40% run-off rate instead of 100%. The same circular "
              "added 2.5 percentage points of run-off on internet and mobile banking enabled retail deposits.",
  steps=["Earlier: 100% run-off", "From 1 April 2026: 40% run-off"],
  why="The direction of change is from 100% to 40%, not the reverse; 25%/50% and 10%/5% are not these rates.",
  current=ca("2026-04-01"),
  facts=[fact("Non-financial entities such as trusts, partnerships and LLPs moved to non-financial corporates with "
              "a 40% run-off rate (previously 100%); effective April 1, 2026", LCR_2025)])
Q(T, "Recent RBI directions", "Advanced",
  "Consider the following statements about RBI's expected credit loss (ECL) directions issued in April 2026:\nI. "
  "Stage 3 under the new framework is linked to the existing NPA definition.\nII. Until the new directions commence, "
  "banks continue to follow the IRACP Directions, 2025.\nIII. The ECL directions apply from 1 April 2026.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Transition to ECL",
  explanation="RBI kept its NPA classification rules and tied the Stage 3 definition to them (I is right). Banks "
              "follow the 2025 IRACP Directions until the new directions commence, at which point the 2025 "
              "directions are repealed (II is right). The directions were issued in April 2026 but apply from "
              "1 April 2027 (III is wrong).",
  steps=["I: correct", "II: correct", "III: wrong (1 April 2027)"],
  current=ca("2026-04-27"),
  facts=[fact("Stage 3 definition tied to NPA rules; banks follow IRACP Directions 2025 until commencement on April "
              "1, 2027", ECL_PR)])
Q(T, "Recent RBI directions", "Advanced",
  "Consider the following statements about RBI's consolidation of regulations in November 2025:\nI. The Master "
  "Directions are organised separately for each type of regulated entity, such as commercial banks, payments banks, "
  "NBFCs and co-operative banks.\nII. Actions taken under the withdrawn circulars continue to be governed by those "
  "circulars.\nIII. The draft Master Directions were issued without inviting public comments.\nWhich of the above "
  "is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Consolidated Master Directions",
  explanation="The 244 Master Directions are organised separately for 11 types of regulated entities (I is right). "
              "The withdrawal notice keeps actions taken under the repealed instructions governed by them (II is "
              "right). The 238 drafts released on 10 October 2025 were put out for comments and RBI received over "
              "770 comments (III is wrong).",
  steps=["I: correct", "II: correct", "III: wrong (drafts were open for comments)"],
  facts=[fact("Master Directions organised for 11 types of regulated entities; drafts issued for comments, over 770 "
              "comments received", CONSOL_PR),
         fact("Actions taken under repealed instructions continue to be governed by them", CONSOL_NOTE)])


# ================================================================= checks and output
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_001_plan.json").read_text(encoding="utf-8"))
spec = next(s for s in plan["subjects"] if s["subject"] == BF)
planned = {(t["topic"], d): n for t in spec["topics"] for d, n in t["quota"].items() if n}
subtopics = {t["topic"]: set(t["subtopics"]) for t in spec["topics"]}
have = Counter((q["topic"], q["difficulty"]) for q in questions)
assert have == Counter(planned), sorted(set(have.items()) ^ set(planned.items()))
assert all(q["subtopic"] in subtopics[q["topic"]] for q in questions)
assert len(questions) == spec["total"] == 200
lo, hi = spec["question_ids"]
assert questions[0]["question_id"] == lo and questions[-1]["question_id"] == hi
assert len({q["question_text"] for q in questions}) == len(questions)
assert all(q["verification"]["fact_checks"] for q in questions)
assert max(_keys.values()) - min(_keys.values()) <= 6, _keys

# ---------------------------------------------------------------- superseded-rules audit (2026-11-06)
# These questions were rewritten to the current rule, or reframed as historical (dated, past tense), after checking
# current RBI/SEBI/Government texts on 2026-11-06. IDs, topics, subtopics, difficulty and keys are unchanged. Any
# earlier ai:independent-check is dropped because the revised wording has not been re-solved blind.
AUDIT_REVISED = {"BANK_BFA_000005", "BANK_BFA_000015", "BANK_BFA_000038", "BANK_BFA_000039", "BANK_BFA_000040", "BANK_BFA_000150",
                 "BANK_BFA_000167"}  # 000167: RRBs became eligible CD issuers in 2021 (review of 2026-11-07)
assert AUDIT_REVISED <= {q["question_id"] for q in questions}
for q in questions:
    if q["question_id"] in AUDIT_REVISED:
        v = q["verification"]
        v["verified_by"] = [x for x in v["verified_by"] if x != "ai:independent-check"]
        v["verified_at"] = AUDIT_DAY

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_001",
    "created_at": TODAY,
    "notes": "BATCH_001 Banking and Financial Awareness part: 200 original questions (60 Basic, 80 Intermediate, "
             "60 Advanced) across 30 topics, IDs BANK_BFA_000004 to BANK_BFA_000203. Every question carries fact "
             "checks against primary sources (RBI, NPCI, SEBI, IRDAI, PFRDA, PIB/DFS, BIS, IBBI, exchanges) opened "
             "or search-confirmed on 2026-11-05; changeable values carry current_affairs dates. Computed answers are "
             "re-derived in tools/batch_001/banking.py. Repo Rate and Budget/Economic Survey topics are excluded.",
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_001_BFA.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions; keys {dict(sorted(_keys.items()))})")
