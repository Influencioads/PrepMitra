"""Writes batches/parts/BATCH_004_BFA.json: the 200 Banking and Financial Awareness questions of BATCH_004.

Every fact is backed by at least one fact_check whose source was opened on 2026-11-05 (fetched with a plain client and
read; PDFs were downloaded and their text extracted), or, where the official page could not be fetched (NPCI, PIB,
pmindia and rbidocs PDFs return 403 or a bot check; no workaround was attempted) or only news coverage was found,
confirmed through web search results (those questions carry web:search-confirmed). Only questions whose answer can
change or that report a dated event carry a current_affairs block, and its event_date is the date of that event or
release as stated by the source (Repo Rate and Budget questions always carry one, as the validator requires).
Every computable answer is re-derived below with assertions, the quota per (topic, difficulty) is checked against
the batch plan, and the answer keys are balanced. ai:independent-check is added only to the questions listed in
INDEPENDENT, which a separate solver answered blind (stem and options only, no key) and got right. If any check
fails, nothing is written. All ~600 earlier Banking stems (BATCH_000 to BATCH_003) were read first and their facts
are not repeated.

    python tools/batch_004/banking.py      (run from anywhere)
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
FIRST_ID = 604
SECONDS = {"Basic": 20, "Intermediate": 30, "Advanced": 60}

_rng = random.Random(2026110504)
_keys = Counter()
questions = []

# Question numbers (offset from BANK_BFA_000604, i.e. 0 = 000604) re-answered blind by a separate solver (stem and
# options only, no key or solution; 75 questions given, all 75 matched the key). Four matches the solver marked as
# low-confidence or plausibility guesses (28, 125, 132, 137) are NOT tagged; the remaining 71 are.
INDEPENDENT = {2, 4, 6, 8, 9, 10, 11, 14, 19, 21, 22, 23, 30, 31, 32, 33, 38, 40, 42, 43, 44, 48, 49, 50, 51, 53, 54,
               56, 57, 61, 62, 63, 69, 70, 73, 75, 76, 77, 79, 81, 83, 85, 87, 89, 91, 92, 98, 101, 103, 108, 110,
               111, 112, 114, 117, 119, 120, 121, 128, 129, 135, 139, 140, 143, 146, 147, 152, 154, 156, 157, 158}

# ---------------------------------------------------------------- sources
# Opened (fetched and read) on 2026-11-05
CHRON_91 = "https://rbi.org.in/history/Brief_Chro1991to2000.html"
CHRON_00 = "https://rbi.org.in/history/Brief_Chro2000_Onwards.html"
RATES_HIST = "https://www.rbi.org.in/commonman/english/history/Scripts/BankrateCRRandSLRChanges.aspx"
GOVS = "https://www.rbi.org.in/Scripts/Governors.aspx"
ORG = "https://www.rbi.org.in/commonman/english/Scripts/Organisation.aspx"
KYC_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=11566"
LIAB = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11040&Mode=0"
NBFC_FAQ = "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=1167"
PAY_BOOKLET = "https://www.rbi.org.in/scripts/PublicationsView.aspx?Id=20315"
PSR = "https://www.rbi.org.in/Scripts/PublicationsView.aspx?id=23813"
NEFT_FAQ = "https://rbi.org.in/Scripts/faqview.aspx?Id=60"
RTGS_FAQ = "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=275"
IRAC_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13146"
PSL_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12799"
STRESS = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11580&Mode=0"
IBBI_FAQ = "https://ibbi.gov.in/uploads/faqs/CIRPFAQs%20Final2408.pdf"
RBIOS_FAQ = "https://www.rbi.org.in/commonperson/english/scripts/FAQs.aspx?Id=3407"
ERUPEE_FAQ = "https://www.rbi.org.in/commonman/English/scripts/FAQs.aspx?Id=3686"
DBU = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12285"
DSIB_25 = "https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=61729"
MFI_RW = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12786"
BCBS_HIST = "https://www.bis.org/bcbs/history.htm"
SDRP_DEC23 = "https://www.rbi.org.in/scripts/BS_ViewBulletin.aspx?Id=22250"
SDRP_APR26 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=62516"
GOV_JUN26 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=62864"
MPC_JUN26 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=62863"
GOV_OCT26 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63744"
MMO_OCT6 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63741"
VRRR_OCT7 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63740"
GOV_MAY22 = "https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=53651"
MCIR_JUN25 = "https://www.rbi.org.in/scripts/PublicationsView.aspx?Id=23161"
MOHANTY = "https://www.rbi.org.in/scripts/BS_ViewBulletin.aspx?Id=12420"
EBLR = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11677&Mode=0"
SLR_2018 = "https://www.rbi.org.in/scripts/FS_Notification.aspx?Id=11427&fn=2&Mode=0"
WMA_26 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=62458"
NOTE2000 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=61942"
PB_2015 = "https://www.rbi.org.in/scripts/bs_pressreleasedisplay.aspx?prid=34754"
SFB_COMP = "https://www.rbi.org.in/commonperson/English/Scripts/Notification.aspx?Id=2334"
SFB_UB = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12676"
CALL_MD = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12061&Mode=0"
BC_2010 = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Mode=0&Id=6017"
FLW_26 = "https://www.rbi.org.in/financialeducation/"
PMJDY_DFS = "https://financialservices.gov.in/index.php/pradhan-mantri-jan-dhan-yojana-pmjdy"
FEMA_EXP = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13750&Mode=0"
CB_MISC = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13740&Mode=0"
SFB_MISC = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13741&Mode=0"
COMPOUND = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13745&Mode=0"
SEBI_DEP = "https://investor.sebi.gov.in/depositories.html"
SEBI_MII = "https://investor.sebi.gov.in/miis.html"
MF_CAT = "https://www.amfiindia.com/Themes/Theme1/downloads/1507291273374.pdf"
LIC_HIST = "https://www.licindia.in/history"
BUDGET = "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc202621776101.pdf"
VISHWA = "https://indianbank.bank.in/departments/ind-pm-vishwakarma/"

# Confirmed only through search results (official page not fetchable, or only news/secondary coverage found)
LOCKER = ("https://www.businesstoday.in/industry/banks/story/rbi-revises-guidelines-for-locker-facility-banks-"
          "liability-to-be-100-times-of-annual-rent-304528-2021-08-18")
SBI_ABOUT = "https://sbi.co.in/web/about-us"
MERGER_2020 = ("https://www.scconline.com/blog/post/2020/04/03/bank-mergers-rbi-schemes-of-amalgamation-enforced-w-"
               "e-f-1st-april-2020/")
CONSUMER_RW = ("https://rbidocs.rbi.org.in/rdocs/notification/PDFs/REGULATORYMEASURES8785E7886A044B678FB8AF2C6C051807"
               ".PDF")
ICRR = "https://rbi.org.in/scripts/BS_ViewBulletin.aspx?Id=21986"
FALLCR = "https://www.rbi.org.in/scripts/PublicationsView.aspx?id=21043"
SLR_MD25 = "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/150MD.PDF"
SLR_PEAK = "https://website.rbi.org.in/web/rbi/-/publications/table-46-major-monetary-policy-measures-bank-rate-crr-and-slr-11631"
CORRIDOR = "https://rbi.org.in/Scripts/PublicationsView.aspx?id=23217"
MCLR_MD = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=10295"
CPI_SEP26 = "https://telanganatoday.com/india-retail-inflation-rises-to-5-54pc-in-september-food-prices-drive-increase"
CPI_IW = "https://labourbureau.gov.in/consumer-price-index-numbers-for-industrial-workers"
UPI_2016 = "https://www.npci.org.in/what-we-do/imps/product-overview"
IMPS_SIMPLE = ("https://www.business-standard.com/amp/finance/personal-finance/new-imps-fund-transfer-rules-coming-soon-"
               "here-is-all-you-need-to-know-124013000204_1.html")
PSR_PR = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=62757"
NSE_MWCB = "https://www.nseindia.com/products-services/equity-market-circuit-breakers"
NSDL_ABOUT = "https://nsdl.co.in/about/index.php"
FREELOOK = ("https://www.businesstoday.in/personal-finance/insurance/story/irdai-says-facility-of-policy-loan-is-"
            "mandatory-for-life-insurance-savings-products-433084-2024-06-12")
KCC_MISS = ("https://www.business-standard.com/budget/news/budget-fy26-govt-increases-kcc-loan-limit-to-rs-5-lakh-from-"
            "3-lakh-125020100834_1.html")
CGSE = "https://www.pmindia.gov.in/en/news_updates/cabinet-approves-credit-guarantee-scheme-for-exporters-cgse/"
MCGS_26 = ("https://ianslive.in/centre-modifies-credit-guarantee-scheme-to-bolster-msme-manufacturers-exporters--"
           "20260321183342")
SEARCH_ONLY = {LOCKER, SBI_ABOUT, MERGER_2020, CONSUMER_RW, ICRR, FALLCR, SLR_MD25, SLR_PEAK, CORRIDOR, MCLR_MD,
               CPI_SEP26, CPI_IW, UPI_2016, IMPS_SIMPLE, PSR_PR, NSE_MWCB, NSDL_ABOUT, FREELOOK, KCC_MISS, CGSE,
               MCGS_26}

# Release / event dates taken from the sources
PSR_DATE = "2026-05-18"      # Payment System Report (December 2025) released, RBI press release
OCT26 = "2026-10-07"         # MPC resolution and Governor's statement
JUN26 = "2026-06-05"
BUDGET_DAY = "2026-02-01"


def fact(claim, url):
    return {"claim": claim, "source_url": url, "checked_on": TODAY}


AUDIT_DAY = "2026-11-06"  # superseded-rules audit of 2026-11-06
LOCKER_RBI = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12146"
EBLR_2025 = "https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=61313"
CALL_TIME = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=60740"
SEBI_CAT26 = ("https://www.sebi.gov.in/legal/circulars/feb-2026/categorization-and-rationalization-of-mutual-fund-"
              "schemes_99983.html")
ELP_CAT26 = ("https://elplaw.in/wp-content/uploads/2026/03/SEBIs-Revised-Categorisation-and-Rationalisation-of-Mutual-"
             "Fund-Schemes.pdf")
MISS_2526 = ("https://www.pmindia.gov.in/en/news_updates/cabinet-approves-continuation-of-modified-interest-subvention-"
             "scheme-miss-for-fy-2025-26-with-existing-1-5-interest-subvention-is/")


def fact6(claim, url):
    return {"claim": claim, "source_url": url, "checked_on": AUDIT_DAY}


SEARCH_ONLY.add(MISS_2526)  # Cabinet decision seen only through search results (PIB returns 403)


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
    n = len(questions)
    out = {
        "question_id": f"BANK_BFA_{FIRST_ID + n:06d}",
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
                           "verified_by": ["ai:author-solve", *web] + (["script:recompute"] if computed else [])
                           + (["ai:independent-check"] if n in INDEPENDENT else []),
                           "verified_at": TODAY, "fact_checks": facts}
    questions.append(out)


def days(a, b):
    return (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days


# ================================================================= 1. Banking Fundamentals (2 / 6 / 4)
T = "Banking Fundamentals"
Q(T, "Types of accounts", "Basic",
  "Under RBI's Master Direction on KYC, which of the following is NOT listed as an 'Officially Valid Document' (OVD) "
  "for proof of identity and address?",
  ["PAN card", "Passport", "Voter's Identity Card issued by the Election Commission of India",
   "Job card issued by NREGA duly signed by an officer of the State Government"],
  concept="Officially Valid Documents under KYC",
  explanation="The KYC Direction lists the passport, the driving licence, proof of possession of Aadhaar, the Voter's "
              "Identity Card, the NREGA job card signed by a State Government officer and the letter of the National "
              "Population Register as OVDs. The PAN is collected separately (or Form 60) but is not an OVD for "
              "address.",
  steps=["OVD list: passport, driving licence, Aadhaar possession proof, Voter ID, NREGA job card, NPR letter",
         "PAN card is not on the list"],
  why="Passport, Voter ID and the signed NREGA job card are all named OVDs.",
  facts=[fact("OVD means the passport, the driving licence, proof of possession of Aadhaar number, the Voter's "
              "Identity Card issued by the Election Commission of India, job card issued by NREGA duly signed by an "
              "officer of the State Government and letter issued by the National Population Register", KYC_MD)])
Q(T, "Types of accounts", "Basic",
  "According to RBI's chronology, from which year were banks allowed to formulate special fixed deposit schemes for "
  "senior citizens offering higher rates of interest?",
  ["2001", "1991", "2010", "2016"],
  concept="Deregulation of deposit products",
  explanation="RBI's chronology records that in April 2001 banks were allowed to formulate special fixed deposit "
              "schemes for senior citizens with higher interest rates than for other depositors.",
  steps=["April 2001 → special FD schemes for senior citizens permitted"],
  why="1991 is the year of the external payments crisis; 2010 is the Base Rate year; 2016 is the MCLR year.",
  facts=[fact("April 2001: Banks allowed to formulate special Fixed Deposit Schemes for senior citizen offering "
              "higher rates of interest", CHRON_00)])
Q(T, "Types of accounts", "Intermediate",
  "Under RBI's KYC Direction, how often must periodic updation of KYC be carried out for high-risk, medium-risk and "
  "low-risk customers respectively?",
  ["At least once in 2 years, 8 years and 10 years", "Every year, every 5 years and every 10 years",
   "At least once in 2 years, 5 years and 8 years", "At least once in 3 years, 8 years and 12 years"],
  concept="Risk-based periodic updation of KYC",
  explanation="Regulated entities follow a risk-based approach: KYC is updated at least once every two years for "
              "high-risk customers, once every eight years for medium-risk customers and once every ten years for "
              "low-risk customers.",
  steps=["High risk → 2 years", "Medium risk → 8 years", "Low risk → 10 years"],
  why="The other combinations do not match the 2/8/10-year schedule in the Direction.",
  facts=[fact("Periodic updation at least once in every two years for high-risk customers, once in every eight years "
              "for medium risk customers and once in every ten years for low-risk customers", KYC_MD)])
Q(T, "Types of accounts", "Intermediate",
  "How does RBI's KYC Direction treat Video-based Customer Identification Process (V-CIP)?",
  ["As an alternate method of identification with facial recognition through live audio-visual interaction, "
   "treated on par with face-to-face identification",
   "As permissible only for customers who already hold another account with the same bank",
   "As a method usable only for opening small accounts with limited credits",
   "As valid only when the customer is physically present at a branch"],
  concept="V-CIP",
  explanation="V-CIP is defined as an alternate method of customer identification with facial recognition and "
              "customer due diligence by an authorised official through seamless, secure, live, informed-consent "
              "based audio-visual interaction, and it is treated as on par with face-to-face identification.",
  steps=["V-CIP = live audio-visual interaction + facial recognition", "Treated as face-to-face CIP"],
  why="V-CIP is not restricted to existing customers or to small accounts, and it does not require branch presence.",
  facts=[fact("V-CIP: an alternate method of customer identification with facial recognition and customer due "
              "diligence by an authorised official through live audio-visual interaction; treated on par with "
              "face-to-face CIP", KYC_MD)])
Q(T, "Types of accounts", "Intermediate",
  "Under RBI's KYC framework, what is the 'KYC Identifier'?",
  ["The unique number or code assigned to a customer by the Central KYC Records Registry",
   "The account number of the customer's first bank account", "The customer's Aadhaar number",
   "The Legal Entity Identifier of the bank that did the KYC"],
  concept="CKYCR",
  explanation="The Central KYC Records Registry (CKYCR) receives, stores, safeguards and retrieves KYC records in "
              "digital form. The KYC Identifier is the unique number or code it assigns to a customer, which other "
              "regulated entities can use to fetch the KYC records.",
  steps=["CKYCR stores KYC records digitally", "KYC Identifier = unique code assigned by CKYCR"],
  why="It is not an account number, the Aadhaar number or an LEI.",
  facts=[fact("KYC Identifier means the unique number or code assigned to a customer by the Central KYC Records "
              "Registry; CKYCR receives, stores, safeguards and retrieves KYC records in digital form", KYC_MD)])
Q(T, "Types of banks", "Intermediate",
  "According to RBI, which of the following is NOT a difference between a bank and a Non-Banking Financial Company "
  "(NBFC)?",
  ["NBFCs cannot lend to individuals",
   "NBFCs cannot accept demand deposits",
   "NBFCs do not form part of the payment and settlement system and cannot issue cheques drawn on themselves",
   "Deposit insurance from DICGC is not available to depositors of NBFCs"],
  concept="Banks versus NBFCs",
  explanation="RBI lists three differences: an NBFC cannot accept demand deposits; it is not part of the payment and "
              "settlement system and cannot issue cheques drawn on itself; and its depositors do not get DICGC "
              "deposit insurance. NBFCs do lend to individuals.",
  steps=["Differences: no demand deposits; no cheques/payment system; no DICGC cover",
         "Lending to individuals is permitted → not a difference"],
  why="The other three are exactly the differences RBI lists.",
  facts=[fact("NBFCs cannot accept demand deposits; do not form part of the payment and settlement system and cannot "
              "issue cheques drawn on itself; deposit insurance facility of DICGC is not available to depositors of "
              "NBFCs", NBFC_FAQ)])
Q(T, "Types of banks", "Intermediate",
  "From September 2002, RBI allowed banks to open Offshore Banking Units (OBUs). Where can they be set up, and how "
  "do they function?",
  ["In Special Economic Zones, functioning as virtual foreign branches located in India",
   "Only outside India, as overseas subsidiaries", "In every district headquarters, as rural branches",
   "In GIFT City only, as branches of foreign central banks"],
  concept="Offshore Banking Units",
  explanation="RBI's chronology records that schemes introduced in September 2002 allowed banks to open Offshore "
              "Banking Units in Special Economic Zones; they function as virtual foreign branches located in India.",
  steps=["Location: SEZs", "Nature: virtual foreign branches in India"],
  why="OBUs are located in India (not abroad), are not rural branches, and are not branches of foreign central banks.",
  facts=[fact("Sep 2002: banks allowed to open Offshore Banking Units in Special Economic Zones, which function as "
              "virtual foreign branches located in India", CHRON_00)])
Q(T, "Cheques and instruments", "Intermediate",
  "The Cheque Truncation System (CTS) was introduced in grids. In which order were the three grids set up?",
  ["New Delhi (2008), Chennai (2011), Mumbai (2013)", "Mumbai (2008), New Delhi (2011), Chennai (2013)",
   "Chennai (2008), Mumbai (2011), New Delhi (2013)", "New Delhi (2008), Mumbai (2011), Chennai (2013)"],
  concept="Grid-based CTS",
  explanation="RBI's payments booklet records that CTS was introduced in New Delhi after a pilot in 2008, extended to "
              "Chennai in September 2011 and to Mumbai in April 2013. All MICR centres were later subsumed into "
              "grid-based CTS.",
  steps=["New Delhi: 2008", "Chennai: September 2011", "Mumbai: April 2013"],
  why="Only the first option has both the correct order and the correct years.",
  facts=[fact("CTS was introduced in New Delhi after a pilot in 2008, extended to Chennai in September 2011 and to "
              "Mumbai in April 2013", PAY_BOOKLET)])

credits_fy, wd_month, bal = 95_000, 12_000, 40_000
assert credits_fy <= 100_000 and bal <= 50_000 and wd_month > 10_000
Q(T, "Types of accounts", "Advanced",
  "Ravi holds a 'small account' opened under RBI's KYC Direction. In the current financial year the aggregate credits "
  "are ₹95,000, his balance has never exceeded ₹40,000, and in October his withdrawals and transfers add up to "
  "₹12,000. Which statement is correct?",
  ["The October withdrawals breach the ₹10,000 monthly limit; the credit and balance limits are respected",
   "All limits are respected, since the annual credit limit is ₹2 lakh",
   "The balance breaches the ₹25,000 limit for small accounts",
   "Only the credits breach the limit, which is ₹50,000 a year"],
  concept="Limits on small accounts",
  explanation="A small account allows aggregate credits of up to ₹1 lakh in a financial year, aggregate withdrawals "
              "and transfers of up to ₹10,000 in a month, and a balance of up to ₹50,000 at any time. Credits of "
              "₹95,000 and a balance of ₹40,000 are within limits; withdrawals of ₹12,000 in a month exceed ₹10,000.",
  steps=["Credits 95,000 ≤ 1,00,000 ✓", "Balance 40,000 ≤ 50,000 ✓", "Withdrawals 12,000 > 10,000 ✗"],
  why="The annual credit limit is ₹1 lakh (not ₹2 lakh or ₹50,000), and the balance limit is ₹50,000 (not ₹25,000).",
  computed=True,
  facts=[fact("Small account: aggregate of all credits in a financial year does not exceed rupees one lakh; aggregate "
              "of all withdrawals and transfers in a month does not exceed rupees ten thousand; balance at any point "
              "of time does not exceed rupees fifty thousand", KYC_MD)])

bal_cap, credit_cap, loan_cap = 100_000, 200_000, 60_000
asks = {"balance": 120_000, "credits": 180_000, "loan": 50_000}
ok = {k: v <= {"balance": bal_cap, "credits": credit_cap, "loan": loan_cap}[k] for k, v in asks.items()}
assert ok == {"balance": False, "credits": True, "loan": True}
Q(T, "Types of accounts", "Advanced",
  "A customer opened a deposit account and a term-loan account with a bank through Aadhaar OTP-based e-KYC in "
  "non-face-to-face mode. Under RBI's KYC Direction, which of the following is permitted?\n"
  "P. Keeping an aggregate balance of ₹1.2 lakh in the deposit account\n"
  "Q. Aggregate credits of ₹1.8 lakh in the deposit account in the financial year\n"
  "R. A term loan of ₹50,000 sanctioned in the year",
  ["Q and R only", "P, Q and R", "P and R only", "R only"],
  concept="Limits on accounts opened by OTP-based e-KYC",
  explanation="For accounts opened with OTP-based e-KYC in non-face-to-face mode, the aggregate deposit balance cannot "
              "exceed ₹1 lakh, aggregate credits in a financial year cannot exceed ₹2 lakh, and term loans "
              "sanctioned cannot exceed ₹60,000 in a year. P breaches the balance cap; Q and R are within limits.",
  steps=["P: 1.2 lakh > 1 lakh ✗", "Q: 1.8 lakh ≤ 2 lakh ✓", "R: 50,000 ≤ 60,000 ✓"],
  why="Any option containing P is wrong; 'R only' wrongly excludes Q.",
  computed=True,
  facts=[fact("OTP-based e-KYC accounts: aggregate balance of all deposit accounts shall not exceed rupees one lakh; "
              "aggregate of all credits in a financial year shall not exceed rupees two lakh; aggregate amount of term "
              "loans sanctioned shall not exceed rupees sixty thousand in a year", KYC_MD)])

rent, contents = 4_500, 6_00_000
liability = min(100 * rent, contents)
assert liability == 4_50_000
Q(T, "Types of accounts", "Advanced",
  "Meena pays an annual locker rent of ₹4,500. A fire at the branch, caused by the bank's negligence, destroys locker "
  "contents worth ₹6 lakh. Applying RBI's revised locker instructions of 18 August 2021 (in force from 1 January "
  "2022), what is the most the bank is liable to pay?",
  ["₹4.5 lakh", "₹6 lakh", "₹45,000", "Nothing, because lockers are at the hirer's risk"],
  concept="Bank's liability for locker contents",
  explanation="Under the August 2021 instructions, for loss of locker contents due to fire, theft, burglary, building "
              "collapse or fraud by employees, the bank's liability is limited to 100 times the prevailing annual rent. 100 × ₹4,500 = ₹4.5 lakh, which is "
              "less than the ₹6 lakh lost.",
  steps=["Cap = 100 × annual rent = 100 × 4,500 = ₹4,50,000", "Loss ₹6,00,000 > cap → pay ₹4.5 lakh"],
  why="The bank does not pay the full value beyond the cap; ₹45,000 uses 10 times the rent; banks are liable for fire "
      "losses caused by their negligence.",
  computed=True,
  facts=[fact6("RBI circular of 18 August 2021 (in force from 1 January 2022): liability for loss of locker contents due "
               "to fire, theft, burglary, dacoity, robbery, building collapse or employee fraud is one hundred times "
               "the prevailing annual rent", LOCKER_RBI)])

rent2, break_open = 3_200, 2_400
td = 3 * rent2 + break_open
assert td == 12_000
Q(T, "Types of accounts", "Advanced",
  "At the time of allotting a locker with annual rent of ₹3,200, a bank asks the new hirer for a term deposit as "
  "security. If the charges for breaking open the locker are ₹2,400, what is the largest term deposit the bank can "
  "ask for under RBI's revised locker instructions of 18 August 2021?",
  ["₹12,000", "₹9,600", "₹5,600", "₹3,20,000"],
  concept="Term deposit for locker allotment",
  explanation="Banks may obtain a term deposit at the time of allotment that covers three years' rent and the charges "
              "for breaking open the locker in case of need: 3 × 3,200 + 2,400 = ₹12,000.",
  steps=["Three years' rent = 3 × 3,200 = 9,600", "Add break-open charges 2,400 → ₹12,000"],
  why="₹9,600 omits break-open charges; ₹5,600 is one year's rent plus charges; ₹3.2 lakh is the 100-times liability "
      "cap, not the deposit.",
  computed=True,
  facts=[fact6("RBI circular of 18 August 2021: banks may obtain a Term Deposit at the time of allotment covering three "
               "years' rent and the charges for breaking open the locker", LOCKER_RBI)])

# ================================================================= 2. History of Banking in India (2 / 1 / 1)
T = "History of Banking in India"
Q(T, "Mergers and consolidation", "Basic",
  "On 27 January 1921, three Presidency banks were merged to form which bank?",
  ["Imperial Bank of India", "State Bank of India", "Punjab National Bank", "Bank of India"],
  concept="Origin of the Imperial Bank",
  explanation="SBI traces its origin to the Bank of Calcutta (1806). On 27 January 1921 the three Presidency banks "
              "(Bengal, Bombay and Madras) were merged to form the Imperial Bank of India, which became SBI in 1955.",
  steps=["Bank of Bengal + Bank of Bombay + Bank of Madras → Imperial Bank of India (1921)"],
  why="SBI was created from the Imperial Bank only in 1955; PNB and Bank of India were separate banks.",
  facts=[fact("On 27 January 1921, the three banks were merged to form the Imperial Bank of India", SBI_ABOUT)])
Q(T, "Mergers and consolidation", "Basic",
  "In the consolidation of public sector banks effective 1 April 2020, Syndicate Bank was amalgamated into:",
  ["Canara Bank", "Punjab National Bank", "Indian Bank", "Bank of Baroda"],
  concept="2020 consolidation of PSBs",
  explanation="Under the schemes of amalgamation effective 1 April 2020, Syndicate Bank merged into Canara Bank; "
              "Oriental Bank of Commerce and United Bank of India merged into Punjab National Bank.",
  steps=["Syndicate → Canara", "OBC + United → PNB"],
  why="PNB absorbed OBC and United Bank; Indian Bank absorbed Allahabad Bank; Bank of Baroda absorbed Vijaya and Dena "
      "in 2019.",
  facts=[fact("Schemes of amalgamation enforced w.e.f. 1 April 2020: Syndicate Bank into Canara Bank; Oriental Bank of "
              "Commerce and United Bank of India into Punjab National Bank", MERGER_2020)])
Q(T, "Committees", "Intermediate",
  "In May 2011 RBI moved to a single independently varying policy rate (the repo rate), with the reverse repo pegged "
  "below it and a new MSF above it. This followed the recommendations of the Working Group on Operating Procedure "
  "of Monetary Policy chaired by:",
  ["Deepak Mohanty", "Urjit R. Patel", "Raghuram G. Rajan", "Bimal Jalan"],
  concept="Committees and the operating procedure of monetary policy",
  explanation="RBI's Bulletin notes that the new operating procedure, operational from May 2011, followed the Working "
              "Group on Operating Procedures of Monetary Policy chaired by Deepak Mohanty: the repo became the only "
              "independently varying policy rate, the reverse repo was pegged 100 bps below it and the MSF was set "
              "100 bps above it.",
  steps=["Mohanty Working Group → single policy rate (repo), May 2011"],
  why="Urjit Patel chaired the 2014 committee on the monetary policy framework; Rajan chaired the 2008 committee on "
      "financial sector reforms; Jalan chaired the committee on RBI's economic capital framework.",
  facts=[fact("Following the recommendations of the Working Group on Operating Procedures of Monetary Policy "
              "(Chairman: Shri Deepak Mohanty), the repo rate has become the only independently varying policy rate; "
              "operational from May 2011", MOHANTY)])
Q(T, "Mergers and consolidation", "Advanced",
  "Consider the following statements about the origins of the State Bank of India:\n"
  "I. SBI's origin goes back to the Bank of Calcutta, established in June 1806, which became the Bank of Bengal on "
  "receiving its charter.\n"
  "II. The Imperial Bank of India was formed in 1921 by merging three Presidency banks.\n"
  "III. The Bank of Bombay was the oldest of the three Presidency banks.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II only", "I, II and III", "II and III only"],
  concept="Presidency banks",
  explanation="SBI's history begins with the Bank of Calcutta (2 June 1806), redesignated the Bank of Bengal when it "
              "received its charter. The Imperial Bank of India was formed on 27 January 1921 by merging the three "
              "Presidency banks. The Bank of Bombay (1840) was younger than the Bank of Calcutta/Bengal, so III is "
              "wrong.",
  steps=["I: correct", "II: correct", "III: wrong (Bank of Calcutta/Bengal, 1806, was the oldest)"],
  why="III is false, which eliminates the options containing it; 'II only' omits the correct statement I.",
  facts=[fact("Origin of SBI goes back to the establishment of the Bank of Calcutta in Calcutta on 2 June 1806; three "
              "years later it received its charter and was redesigned as the Bank of Bengal; on 27 January 1921 the "
              "three banks were merged to form the Imperial Bank of India", SBI_ABOUT)])

# ================================================================= 3. Reserve Bank of India (3 / 3 / 3)
T = "Reserve Bank of India"
Q(T, "Governors and leadership", "Basic",
  "Who succeeded Sir Osborne Smith as the second Governor of the Reserve Bank of India in July 1937?",
  ["Sir James Taylor", "Sir C. D. Deshmukh", "Sir Benegal Rama Rau", "H. V. R. Iengar"],
  concept="Early RBI Governors",
  explanation="RBI's list of Governors shows Sir Osborne Smith (1935–37), followed by Sir James Taylor (1 July 1937 to "
              "17 February 1943), then Sir C. D. Deshmukh from 1943.",
  steps=["1st: Osborne Smith", "2nd: James Taylor (1937–43)", "3rd: C. D. Deshmukh"],
  why="Deshmukh was the third Governor, Rama Rau the fourth and Iengar the sixth.",
  facts=[fact("Sir James Taylor: 01-07-1937 to 17-02-1943, after Sir Osborne Smith (01-04-1935 to 30-06-1937)",
              GOVS)])
Q(T, "Governors and leadership", "Basic",
  "Sanjay Malhotra, who took charge on 11 December 2024, is which Governor of the Reserve Bank of India in order?",
  ["26th", "25th", "24th", "27th"],
  concept="RBI Governors",
  explanation="RBI's list numbers Shaktikanta Das as the 25th Governor (12 December 2018 to 10 December 2024) and "
              "Sanjay Malhotra as the 26th, from 11 December 2024.",
  steps=["25th: Shaktikanta Das (2018–2024)", "26th: Sanjay Malhotra (from 11-12-2024)"],
  why="25th is Das and 24th is Urjit Patel; there is no 27th Governor yet.",
  facts=[fact("26: Shri Sanjay Malhotra, 11-12-2024 onwards; 25: Shri Shaktikanta Das, 12-12-2018 to 10-12-2024",
              GOVS)])
Q(T, "Establishment and structure", "Basic",
  "Which of the following is a wholly owned subsidiary of the Reserve Bank of India?",
  ["Indian Financial Technology and Allied Services (IFTAS)", "National Payments Corporation of India (NPCI)",
   "Clearing Corporation of India Ltd (CCIL)", "Small Industries Development Bank of India (SIDBI)"],
  concept="RBI's subsidiaries",
  explanation="RBI's fully owned subsidiaries are DICGC, BRBNMPL, ReBIT, IFTAS and the Reserve Bank Innovation Hub "
              "(RBIH). NPCI is owned by banks; CCIL and SIDBI are not RBI subsidiaries.",
  steps=["Subsidiaries: DICGC, BRBNMPL, ReBIT, IFTAS, RBIH", "IFTAS → wholly owned"],
  why="NPCI is a bank-promoted not-for-profit company; CCIL is promoted by banks and institutions; SIDBI is a "
      "separate development financial institution.",
  facts=[fact("Fully owned subsidiaries: DICGC, BRBNMPL, ReBIT, Indian Financial Technology and Allied Services "
              "(IFTAS), Reserve Bank Innovation Hub (RBIH)", ORG)])
Q(T, "Establishment and structure", "Intermediate",
  "RBI lists five training establishments. Which one of them is an autonomous institute rather than part of RBI?",
  ["Institute for Development and Research in Banking Technology (IDRBT)", "College of Agricultural Banking (CAB)",
   "Reserve Bank of India Staff College (RBSC)", "College of Supervisors (CoS)"],
  concept="RBI's training establishments",
  explanation="RBI has five training establishments. Four are part of RBI — RBSC, CAB, the Enterprise Computing and "
              "Cybersecurity Training Institute (ECCTI) and the College of Supervisors — while IDRBT is autonomous.",
  steps=["Part of RBI: RBSC, CAB, ECCTI, CoS", "Autonomous: IDRBT"],
  why="CAB, RBSC and CoS are RBI's own establishments.",
  facts=[fact("Training establishments: four part of RBI (RBSC, CAB, ECCTI, College of Supervisors); IDRBT is "
              "autonomous", ORG)])
Q(T, "Governors and leadership", "Intermediate",
  "Who was Governor of RBI immediately before Dr. C. Rangarajan, who took office on 22 December 1992?",
  ["S. Venkitaramanan", "R. N. Malhotra", "Bimal Jalan", "Amitav Ghosh"],
  concept="Sequence of RBI Governors",
  explanation="RBI's list shows R. N. Malhotra (1985–1990), S. Venkitaramanan (22 December 1990 to 21 December 1992), "
              "C. Rangarajan (1992–1997) and then Bimal Jalan (from 22 November 1997).",
  steps=["Malhotra → Venkitaramanan → Rangarajan → Jalan"],
  why="Malhotra preceded Venkitaramanan; Jalan succeeded Rangarajan; A. Ghosh served briefly in 1985.",
  facts=[fact("S Venkitaramanan 22-12-1990 to 21-12-1992; Dr. C Rangarajan 22-12-1992 to 22-11-1997", GOVS)])
Q(T, "Establishment and structure", "Intermediate",
  "Which of the following is NOT one of the four training establishments that are part of RBI itself?",
  ["National Institute of Bank Management (NIBM)",
   "Enterprise Computing and Cybersecurity Training Institute (ECCTI)", "College of Agricultural Banking (CAB)",
   "College of Supervisors (CoS)"],
  concept="RBI's training establishments and funded institutes",
  explanation="The four establishments that are part of RBI are RBSC, CAB, ECCTI and CoS. NIBM is a separate "
              "institute in which RBI is only an ordinary member, alongside other banks and financial institutions.",
  steps=["RBI's own: RBSC, CAB, ECCTI, CoS", "NIBM: RBI is an ordinary member"],
  why="ECCTI, CAB and CoS are all RBI's own training establishments.",
  facts=[fact("Four training establishments are part of RBI: RBSC, CAB, ECCTI and College of Supervisors; NIBM: RBI is "
              "an ordinary member alongside other banks and FIs", ORG)])

ghosh = days("1985-01-15", "1985-02-04")
assert ghosh == 20
Q(T, "Governors and leadership", "Advanced",
  "RBI's list of Governors shows A. Ghosh serving from 15 January 1985 to 4 February 1985, when R. N. Malhotra took "
  "over. For how many days did Ghosh hold office (counting from his first day up to, but not including, 4 "
  "February)?",
  ["20 days", "31 days", "45 days", "14 days"],
  concept="Shortest tenure as RBI Governor",
  explanation="From 15 January to 4 February 1985 there are 16 days left in January after the 15th plus 4 days in "
              "February, i.e. 20 days — the shortest tenure in RBI's list.",
  steps=["15 Jan → 31 Jan = 16 days", "1 Feb → 4 Feb = 4 days", "Total = 20 days"],
  why="31, 45 and 14 days do not match the dates.",
  computed=True,
  facts=[fact("A Ghosh: 15-01-1985 to 04-02-1985; R N Malhotra: 04-02-1985 to 22-12-1990", GOVS)])

rau = days("1949-07-01", "1957-01-14") / 365.25
das = days("2018-12-12", "2024-12-10") / 365.25
assert round(rau, 1) == 7.5 and round(das, 1) == 6.0 and round(rau - das, 1) == 1.5
Q(T, "Governors and leadership", "Advanced",
  "Sir Benegal Rama Rau was Governor from 1 July 1949 to 14 January 1957, and Shaktikanta Das from 12 December 2018 "
  "to 10 December 2024. Which statement is correct?",
  ["Rama Rau served about 7.5 years, roughly 1.5 years longer than Das's 6 years",
   "Das served longer, by about one year", "Both served almost exactly six years",
   "Rama Rau served about 5.5 years, half a year less than Das"],
  concept="Tenures of RBI Governors",
  explanation="1 July 1949 to 14 January 1957 is about 7 years 6½ months (≈7.5 years). 12 December 2018 to 10 December "
              "2024 is just under 6 years. Rama Rau's tenure, the longest in RBI's list, exceeds Das's by about 1.5 "
              "years.",
  steps=["Rama Rau: 2,754 days ≈ 7.5 years", "Das: 2,190 days ≈ 6.0 years", "Difference ≈ 1.5 years"],
  why="The other options misstate one or both tenures.",
  computed=True,
  facts=[fact("Sir Benegal Rama Rau 01-07-1949 to 14-01-1957; Shri Shaktikanta Das 12-12-2018 to 10-12-2024", GOVS)])
Q(T, "Establishment and structure", "Advanced",
  "Consider the following statements about institutes linked to RBI, as listed by RBI:\n"
  "I. RBI fully funds the Centre for Advanced Financial Research and Learning (CAFRAL).\n"
  "II. RBI is a sponsor bank of the Indian Institute of Bank Management (IIBM), along with other banks and FIs.\n"
  "III. RBI fully funds the National Institute of Bank Management (NIBM).\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Institutes funded by RBI",
  explanation="RBI fully funds CAFRAL and IGIDR. For IIBM, RBI is a sponsor bank alongside other banks and FIs. For "
              "NIBM, RBI is only an ordinary member, so III is wrong.",
  steps=["I: correct", "II: correct", "III: wrong (ordinary member only)"],
  why="III is false; 'I only' omits II.",
  facts=[fact("Fully funded by the Bank: CAFRAL and IGIDR; IIBM: RBI is a sponsor bank along with other banks and FIs; "
              "NIBM: RBI is an ordinary member", ORG)])

# ================================================================= 4. RBI Functions (3 / 3 / 3)
T = "RBI Functions"
Q(T, "Issuer of currency", "Basic",
  "Bharatiya Reserve Bank Note Mudran Limited, RBI's banknote-printing subsidiary, was established in:",
  ["February 1995", "April 1935", "November 1994", "September 1996"],
  concept="Currency printing",
  explanation="RBI's chronology records the establishment of Bharatiya Reserve Bank Note Mudran Limited on 3 February "
              "1995.",
  steps=["BRBNMPL established: 3 February 1995"],
  why="April 1935 is RBI's own establishment; November 1994 is the Board for Financial Supervision; September 1996 is "
      "when RBI's website went live.",
  facts=[fact("Feb 1995: Bharatiya Reserve Bank Note Mudran Limited established (3 February)", CHRON_91)])
Q(T, "Regulator and supervisor", "Basic",
  "According to RBI's chronology, risk-based supervision of banks was introduced in:",
  ["April 2003", "June 1995", "April 1992", "July 2014"],
  concept="Supervisory approach",
  explanation="RBI's chronology lists April 2003 as the month risk-based supervision of banks was introduced.",
  steps=["Risk-based supervision: April 2003"],
  why="June 1995 is the Banking Ombudsman office; April 1992 is when prudential norms were specified; July 2014 is when "
      "MICR clearing ended.",
  facts=[fact("April 2003: Risk based supervision of Banks introduced", CHRON_00)])
Q(T, "Regulator and supervisor", "Basic",
  "RBI's oversight of payment and settlement systems is led by the Board for Regulation and Supervision of Payment "
  "and Settlement Systems (BPSS). Who chairs the BPSS?",
  ["The Governor of RBI", "The Union Finance Minister", "The Chief Executive of NPCI",
   "The Secretary, Department of Financial Services"],
  concept="Regulator of payment systems",
  explanation="Under the Payment and Settlement Systems Act, 2007, RBI is the designated authority. Its oversight is "
              "spearheaded by the BPSS, chaired by the RBI Governor.",
  steps=["PSS Act, 2007 → RBI is the authority", "BPSS chaired by the Governor"],
  why="The Finance Minister chairs the FSDC, not the BPSS; NPCI is an operator regulated by RBI; DFS is a Government "
      "department.",
  facts=[fact("The Board for Regulation and Supervision of Payment and Settlement Systems (BPSS), chaired by the "
              "Governor, spearheads RBI's oversight of payment and settlement systems", PAY_BOOKLET)])
Q(T, "Issuer of currency", "Intermediate",
  "According to RBI's status release of 1 January 2026, what share of the ₹2000 banknotes in circulation on 19 May "
  "2023 (when their withdrawal was announced) had been returned by 31 December 2025?",
  ["98.41%", "93.10%", "100%; the notes are no longer legal tender", "76.20%"],
  concept="Withdrawal of ₹2000 notes",
  explanation="₹2000 notes worth ₹3.56 lakh crore were in circulation on 19 May 2023; by the close of 31 December 2025 "
              "only ₹5,669 crore remained, so 98.41% had been returned. The notes continue to be legal tender.",
  steps=["In circulation 19-05-2023: ₹3.56 lakh crore", "Outstanding 31-12-2025: ₹5,669 crore", "Returned: 98.41%"],
  why="The notes are still legal tender, so '100%' is wrong; the other percentages do not match the release.",
  current=ca("2026-01-01"),
  facts=[fact("98.41% of the ₹2000 banknotes in circulation as on May 19, 2023 has been returned; ₹5,669 crore "
              "outstanding at close of business on December 31, 2025; the notes continue to be legal tender",
              NOTE2000)])
Q(T, "Banker to government", "Intermediate",
  "In March 2026, RBI fixed the Ways and Means Advances (WMA) limit for the Government of India for April–September "
  "2026 at:",
  ["₹2,50,000 crore", "₹1,50,000 crore", "₹1,00,000 crore", "₹3,50,000 crore"],
  concept="WMA limit for the Centre",
  explanation="RBI's press release of 27 March 2026 set the WMA limit for H1 2026-27 at ₹2,50,000 crore, fixed in "
              "consultation with the Government. RBI may trigger fresh market borrowing when 75% of the limit is "
              "used.",
  steps=["H1 2026-27 WMA limit: ₹2.5 lakh crore"],
  why="₹1,50,000 crore was the limit for the first half of earlier years; the others do not match.",
  current=ca("2026-03-27"),
  facts=[fact("WMA limit for the first half of 2026-27 (April to September 2026) fixed at ₹2,50,000 crore; RBI may "
              "trigger fresh floatation of market loans when the Government utilises 75 per cent of the WMA limit",
              WMA_26)])
Q(T, "Regulator and supervisor", "Intermediate",
  "According to RBI, what minimum Net Owned Fund (NOF) is now required for registration as an NBFC, and by when must "
  "existing NBFCs reach it?",
  ["₹10 crore; existing NBFCs by 31 March 2027", "₹2 crore; existing NBFCs by 31 March 2025",
   "₹25 lakh; no deadline for existing NBFCs", "₹100 crore; existing NBFCs by 31 March 2030"],
  concept="Entry norms for NBFCs",
  explanation="RBI's NBFC FAQs state that a company needs a minimum NOF of ₹10 crore to register as an NBFC; new "
              "applicants must have it from the start and existing NBFCs must reach it by 31 March 2027.",
  steps=["Minimum NOF: ₹10 crore", "Existing NBFCs: by 31 March 2027"],
  why="₹25 lakh and ₹2 crore are older entry thresholds; ₹100 crore is not the NBFC norm.",
  facts=[fact("Minimum Net Owned Fund for registration is ₹10 crore; existing NBFCs to reach it by March 31, 2027",
              NBFC_FAQ)])

circ, outstanding = 356_000, 5_669
ret = (1 - outstanding / circ) * 100
assert round(ret, 2) == 98.41
Q(T, "Issuer of currency", "Advanced",
  "Consider the following statements about the withdrawal of ₹2000 banknotes, as described in RBI's status release "
  "of 1 January 2026:\n"
  "I. The ₹2000 banknotes continue to be legal tender.\n"
  "II. The notes can still be exchanged or deposited at any bank branch.\n"
  "III. People can send ₹2000 notes through India Post from any post office to an RBI Issue Office for credit to their "
  "bank accounts.\n"
  "Which of the above is/are correct?",
  ["I and III only", "I only", "II and III only", "I, II and III"],
  concept="Withdrawal of ₹2000 notes",
  explanation="The notes remain legal tender (I). The exchange/deposit facility at bank branches ended on 7 October "
              "2023; the facility is now available only at RBI's 19 Issue Offices (II wrong). Notes can be sent "
              "through India Post to an RBI Issue Office for credit to a bank account (III). Of ₹3.56 lakh crore in "
              "circulation, ₹5,669 crore was outstanding, i.e. 98.41% returned.",
  steps=["I: correct", "II: wrong (branch facility ended 7 October 2023)", "III: correct"],
  why="Options with II are wrong; 'I only' omits the India Post route.",
  current=ca("2026-01-01"), computed=True,
  facts=[fact("The ₹2000 banknotes continue to be legal tender; facility at bank branches discontinued from October 7, "
              "2023; 19 RBI Issue Offices accept the notes; the public can send them through India Post from any post "
              "office to an RBI Issue Office for credit to their bank accounts", NOTE2000)])

limit = 250_000
trigger = 0.75 * limit
od_rate = 5.50 + 2
assert trigger == 187_500 and od_rate == 7.5
Q(T, "Banker to government", "Advanced",
  "With a WMA limit of ₹2,50,000 crore for April–September 2026, at what level of WMA use may RBI trigger fresh market "
  "borrowing, and at what rate would an overdraft beyond the limit be charged when the repo rate is 5.50%?",
  ["₹1,87,500 crore; 7.50%", "₹2,50,000 crore; 5.50%", "₹1,25,000 crore; 6.50%", "₹1,87,500 crore; 5.75%"],
  concept="WMA and overdraft",
  explanation="RBI may trigger fresh floatation of market loans when the Government uses 75% of the WMA limit: 0.75 × "
              "2,50,000 = ₹1,87,500 crore. WMA is charged at the repo rate and overdraft at 2 percentage points above "
              "it: 5.50% + 2% = 7.50%.",
  steps=["Trigger = 75% × 2,50,000 = 1,87,500", "Overdraft rate = repo + 2 = 7.50%"],
  why="The trigger is 75%, not 100% or 50%; 5.75% is the MSF rate, not the overdraft rate.",
  computed=True, current=ca("2026-03-27"),
  facts=[fact("WMA limit ₹2,50,000 crore; RBI may trigger fresh floatation of market loans when the Government "
              "utilises 75 per cent of the WMA limit; WMA at repo rate and overdraft at two percent above repo rate",
              WMA_26)])

fin_assets, total_assets, intangible = 620, 1_100, 60
fin_income, gross_income = 48, 90
share_a = fin_assets / (total_assets - intangible) * 100
share_i = fin_income / gross_income * 100
assert round(share_a, 1) == 59.6 and round(share_i, 1) == 53.3
Q(T, "Regulator and supervisor", "Advanced",
  "A company has total assets of ₹1,100 crore, including intangible assets of ₹60 crore, of which financial assets are "
  "₹620 crore. Its gross income is ₹90 crore, of which ₹48 crore comes from financial assets. Under RBI's principal "
  "business test, must it register with RBI as an NBFC?",
  ["Yes; financial assets are about 59.6% of total assets (net of intangibles) and financial income about 53.3% of "
   "gross income, both above 50%",
   "No; financial assets are only about 56.4% of total assets, below the 60% threshold",
   "No; the income test is met but the asset test is not",
   "Yes, but only because its financial income exceeds ₹25 crore"],
  concept="Principal business criteria ('50-50 test')",
  explanation="A company is an NBFC if its financial assets exceed 50% of total assets (netted off by intangible "
              "assets) and income from financial assets exceeds 50% of gross income. 620 ÷ (1,100 − 60) = 59.6% and "
              "48 ÷ 90 = 53.3%; both exceed 50%.",
  steps=["Asset test: 620 ÷ 1,040 = 59.6% > 50%", "Income test: 48 ÷ 90 = 53.3% > 50%", "Both met → NBFC"],
  why="The threshold is 50%, not 60%, and intangibles are excluded; both tests are met; there is no ₹25 crore income "
      "rule.",
  computed=True,
  facts=[fact("A company is treated as an NBFC when its financial assets are more than 50 per cent of its total assets "
              "(netted off by intangible assets) and income from financial assets is more than 50 per cent of gross "
              "income", NBFC_FAQ)])

# ================================================================= 5. Monetary Policy (3 / 6 / 3)
T = "Monetary Policy"
Q(T, "MPC structure", "Basic",
  "Which Deputy Governor of RBI was a member of the Monetary Policy Committee at its meeting of 3–5 June 2026?",
  ["Dr. Poonam Gupta", "Dr. Nagesh Kumar", "Prof. Ram Singh", "Shri Saugata Bhattacharya"],
  concept="Composition of the MPC",
  explanation="The June 2026 resolution lists the members as Dr. Nagesh Kumar, Shri Saugata Bhattacharya, Prof. Ram "
              "Singh, Dr. Poonam Gupta, Shri Indranil Bhattacharyya and the Governor. Dr. Poonam Gupta is the Deputy "
              "Governor on the MPC; Nagesh Kumar, Saugata Bhattacharya and Ram Singh are the external members.",
  steps=["RBI members: Governor, Deputy Governor (Poonam Gupta), RBI officer", "Others are external members"],
  why="Nagesh Kumar, Ram Singh and Saugata Bhattacharya are Government-appointed external members, not Deputy "
      "Governors.",
  current=ca(JUN26),
  facts=[fact("MPC meeting June 3-5, 2026 attended by Dr. Nagesh Kumar, Shri Saugata Bhattacharya, Prof. Ram Singh, "
              "Dr. Poonam Gupta, Shri Indranil Bhattacharyya and the Governor", MPC_JUN26),
         fact("Deputy Governors on RBI's Central Board include Dr. Poonam Gupta", ORG)])
Q(T, "Transmission", "Basic",
  "Under RBI's external benchmark framework for floating-rate retail and MSE loans (from 1 October 2019), which of "
  "the following could NOT be used as the external benchmark?",
  ["The lending bank's own MCLR", "RBI's policy repo rate",
   "Government of India 3-month Treasury Bill yield published by FBIL",
   "Government of India 6-month Treasury Bill yield published by FBIL"],
  concept="External benchmarks",
  explanation="Banks had to link such loans to one of: RBI's policy repo rate, the 3-month or 6-month T-bill yield "
              "published by FBIL, or any other benchmark market interest rate published by FBIL. MCLR is an internal "
              "benchmark computed by the bank itself.",
  steps=["Allowed: repo, 3-month T-bill (FBIL), 6-month T-bill (FBIL), other FBIL rate", "MCLR → internal, not allowed"],
  why="The repo rate and both FBIL T-bill yields are expressly allowed.",
  facts=[fact("External benchmarks: RBI policy repo rate; GoI 3-month T-bill yield published by FBIL; GoI 6-month "
              "T-bill yield published by FBIL; any other benchmark market interest rate published by FBIL", EBLR)])
Q(T, "Transmission", "Basic",
  "Floating-rate rupee loans sanctioned or renewed between 1 July 2010 and 31 March 2016 were priced with reference to "
  "which internal benchmark?",
  ["Base Rate", "Benchmark Prime Lending Rate (BPLR)", "MCLR", "Repo-linked lending rate"],
  concept="Evolution of lending benchmarks",
  explanation="RBI's external benchmark circular notes that loans sanctioned between 1 July 2010 and 31 March 2016 "
              "were priced with reference to the Base Rate, and those from 1 April 2016 against the MCLR.",
  steps=["Till June 2010: BPLR", "July 2010 – March 2016: Base Rate", "From April 2016: MCLR", "From Oct 2019: external "
         "benchmarks for retail/MSE floating loans"],
  why="BPLR preceded July 2010; MCLR began in April 2016; repo-linked rates came with the external benchmark system.",
  facts=[fact("Loans sanctioned between July 1, 2010 and March 31, 2016 are priced with reference to the Base Rate; "
              "from April 1, 2016 with reference to the MCLR", EBLR)])
Q(T, "Transmission", "Intermediate",
  "Under RBI's external benchmark framework, how can a bank change the spread over the external benchmark on an "
  "existing loan?",
  ["The credit risk premium only on a substantial change in the borrower's credit assessment; other components such "
   "as operating cost may be raised only once in three years, though they may be cut earlier for the borrower's "
   "benefit",
   "Any component at any time, with one month's notice", "Only when the repo rate changes",
   "Never during the life of the loan"],
  concept="Spread over external benchmark",
  explanation="The credit risk premium may change only when the borrower's credit assessment undergoes a substantial "
              "change, as agreed in the loan contract. Other components of the spread, such as operating cost, could "
              "originally be altered only once in three years; RBI's amendment directions of 29 September 2025 "
              "(effective 1 October 2025) let banks reduce these other components earlier than three years for the "
              "borrower's benefit.",
  steps=["Credit risk premium → only on substantial change in credit assessment",
         "Other components → once in 3 years, but may be reduced earlier (from 1 October 2025)"],
  why="Banks cannot change the spread at will, nor is it linked to repo changes; it is not frozen for life either.",
  facts=[fact("Credit risk premium may undergo change only when borrower's credit assessment undergoes a substantial "
              "change; other components of spread including operating cost could be altered once in three years",
              EBLR),
         fact6("RBI amendment directions of 29 September 2025: banks may reduce the other spread components for the "
               "benefit of the borrower earlier than three years", EBLR_2025)])
Q(T, "Transmission", "Intermediate",
  "Which of the following is NOT one of the components of the Marginal Cost of Funds based Lending Rate (MCLR)?",
  ["Negative carry on account of SLR", "Marginal cost of funds", "Negative carry on account of CRR", "Tenor premium"],
  concept="MCLR methodology",
  explanation="MCLR comprises the marginal cost of funds, negative carry on account of CRR, operating costs and a tenor "
              "premium. Negative carry on SLR was part of the older Base Rate methodology, not MCLR.",
  steps=["MCLR = MCF + negative carry on CRR + operating costs + tenor premium"],
  why="The other three are listed components of MCLR.",
  facts=[fact("MCLR comprises marginal cost of funds; negative carry on account of CRR; operating costs; tenor premium",
              MCLR_MD)])
Q(T, "MPC structure", "Intermediate",
  "One of the three RBI members of the MPC is an officer of RBI nominated by the Central Board. Who held this place at "
  "the MPC meeting of June 2026?",
  ["Shri Indranil Bhattacharyya", "Shri Saugata Bhattacharya", "Shri Rohit Jain", "Dr. Nagesh Kumar"],
  concept="Composition of the MPC",
  explanation="The June 2026 MPC comprised the Governor, Deputy Governor Dr. Poonam Gupta, Shri Indranil Bhattacharyya "
              "(the RBI officer) and three external members: Dr. Nagesh Kumar, Shri Saugata Bhattacharya and Prof. Ram "
              "Singh.",
  steps=["External: Nagesh Kumar, Saugata Bhattacharya, Ram Singh", "RBI: Governor, Poonam Gupta, Indranil "
         "Bhattacharyya"],
  why="Saugata Bhattacharya and Nagesh Kumar are external members; Rohit Jain is a Deputy Governor who was not on the "
      "MPC.",
  current=ca(JUN26),
  facts=[fact("MPC meeting June 3-5, 2026 attended by Dr. Nagesh Kumar, Shri Saugata Bhattacharya, Prof. Ram Singh, "
              "Dr. Poonam Gupta and Shri Indranil Bhattacharyya", MPC_JUN26),
         fact("Deputy Governors: S. Swaminathan J, Dr. Poonam Gupta, Shirish Chandra Murmu, Rohit Jain", ORG)])
Q(T, "Policy stance", "Intermediate",
  "In his statement of 7 October 2026, the Governor cited strong growth in money and credit aggregates as a "
  "demand-side risk. What year-on-year growth in bank credit did he report (as of 15 September 2026)?",
  ["18.1%", "11.2%", "7.8%", "24.5%"],
  concept="Credit growth as an input to policy",
  explanation="The Governor reported bank credit growth of 18.1% year-on-year as of 15 September 2026 and treated "
              "strong money and credit growth as a demand-side risk, one reason for the shift to calibrated "
              "tightening.",
  steps=["Bank credit growth (y-o-y, 15 Sept 2026): 18.1%"],
  why="7.8% is Q1 2026-27 GDP growth; the others do not match the statement.",
  current=ca(OCT26),
  facts=[fact("Bank credit grew 18.1 per cent year-on-year as of September 15, 2026; strong growth in money and credit "
              "aggregates is a demand-side risk", GOV_OCT26)])
Q(T, "Transmission", "Intermediate",
  "According to the Governor's statement of 7 October 2026, what was the average daily surplus liquidity in the "
  "banking system since the August 2026 MPC meeting?",
  ["About ₹5.9 lakh crore", "About ₹1.2 lakh crore", "A deficit of about ₹2 lakh crore", "About ₹12 lakh crore"],
  concept="Liquidity conditions and transmission",
  explanation="The Governor said liquidity had remained in surplus, averaging about ₹5.9 lakh crore a day since the "
              "August meeting. Ample liquidity keeps overnight rates near the lower end of the policy corridor.",
  steps=["Average daily surplus since August meeting: ₹5.9 lakh crore"],
  why="Liquidity was in surplus, not deficit, and the reported average was ₹5.9 lakh crore.",
  current=ca(OCT26),
  facts=[fact("Average daily surplus liquidity of ₹5.9 lakh crore since the August meeting", GOV_OCT26)])
Q(T, "Transmission", "Intermediate",
  "Under the MCLR system, the actual lending rate is MCLR plus a spread. What does that spread consist of?",
  ["Only business strategy and credit risk premium", "Operating costs and tenor premium",
   "Negative carry on CRR and SLR", "Return on net worth and operating costs"],
  concept="MCLR and spread",
  explanation="RBI's MCLR directions state that the actual lending rate is MCLR plus spread, and the spread comprises "
              "only two components: business strategy and credit risk premium. Operating costs and tenor premium are "
              "already part of the MCLR.",
  steps=["Lending rate = MCLR + spread", "Spread = business strategy + credit risk premium"],
  why="Operating costs and tenor premium are inside the MCLR; SLR negative carry belongs to the old Base Rate; return "
      "on net worth is part of the marginal cost of funds.",
  facts=[fact("The MCLR plus spread is the actual lending rate; the spread comprises only two components, viz., "
              "business strategy and credit risk premium", MCLR_MD)])

borrow_cost, ronw = 6.0, 15.0
mcf = 0.92 * borrow_cost + 0.08 * ronw
assert round(mcf, 2) == 6.72
Q(T, "Transmission", "Advanced",
  "Under RBI's MCLR methodology, the marginal cost of funds gives 92% weight to the marginal cost of borrowings and 8% "
  "to return on net worth. If a bank's marginal cost of borrowings is 6.00% and its required return on net worth is "
  "15%, what is its marginal cost of funds?",
  ["6.72%", "6.48%", "10.50%", "7.20%"],
  concept="Marginal cost of funds",
  explanation="MCF = 0.92 × 6.00 + 0.08 × 15 = 5.52 + 1.20 = 6.72%.",
  steps=["0.92 × 6.00 = 5.52", "0.08 × 15 = 1.20", "MCF = 6.72%"],
  why="6.48% and 7.20% use wrong weights; 10.50% is a simple average.",
  computed=True,
  facts=[fact("The marginal cost of borrowings shall have a weightage of 92% of Marginal Cost of Funds while return on "
              "networth will have the balance weightage of 8%", MCLR_MD)])

crr, mc = 0.03, 6.0
neg = crr * mc / (1 - crr)
assert round(neg, 3) == 0.186
Q(T, "Transmission", "Advanced",
  "In MCLR, the negative carry on CRR is computed as: required CRR × marginal cost ÷ (1 − CRR). With CRR at 3% and a "
  "marginal cost of funds of 6%, what is the negative carry (approx.)?",
  ["0.19 percentage point", "0.18 percentage point exactly", "0.30 percentage point", "0.06 percentage point"],
  concept="Negative carry on CRR",
  explanation="CRR balances earn no return, so the cost is grossed up: 0.03 × 6 ÷ 0.97 = 0.1856 ≈ 0.19 percentage "
              "point.",
  steps=["0.03 × 6 = 0.18", "0.18 ÷ 0.97 = 0.1856 ≈ 0.19"],
  why="0.18 ignores the division by (1 − CRR); 0.30 and 0.06 use wrong inputs.",
  computed=True,
  facts=[fact("Negative carry on CRR: Required CRR x (marginal cost) / (1 - CRR)", MCLR_MD)])
Q(T, "Transmission", "Advanced",
  "Consider the following statements about RBI's external benchmark framework (circular of 4 September 2019):\n"
  "I. It applied to all new floating-rate personal or retail loans and floating-rate loans to Micro and Small "
  "Enterprises from 1 October 2019.\n"
  "II. Banks were free to offer external-benchmark-linked loans to other types of borrowers as well.\n"
  "III. The interest rate had to be reset at most once a year.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Scope of external benchmarking",
  explanation="From 1 October 2019 all new floating-rate personal/retail loans and floating-rate loans to MSEs had to "
              "be linked to an external benchmark (I), and banks could offer such loans to others too (II). The rate "
              "had to be reset at least once in three months, not at most once a year (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (reset at least once in three months)"],
  why="III reverses the reset rule; 'I only' omits II.",
  facts=[fact("All new floating rate personal or retail loans and floating rate loans to Micro and Small Enterprises "
              "extended by banks from October 01, 2019 shall be benchmarked to an external benchmark; banks free to "
              "offer such loans to other types of borrowers; interest rate reset at least once in three months",
              EBLR)])

# ================================================================= 6. Repo Rate (2 / 2 / 2)
T = "Repo Rate"
SUB = "Repo and policy corridor"
Q(T, SUB, "Basic",
  "At an off-cycle meeting on 2 and 4 May 2022, the MPC raised the policy repo rate to 4.40%. By how much was it "
  "raised?",
  ["40 basis points", "25 basis points", "50 basis points", "35 basis points"],
  concept="Off-cycle repo rate action",
  explanation="The MPC held an off-cycle meeting on 2 and 4 May 2022 and voted unanimously to raise the repo rate by "
              "40 bps to 4.40% with immediate effect, which RBI described as a reversal of the rate action of 22 May "
              "2020.",
  steps=["May 2022: +40 bps → 4.40%"],
  why="25 and 50 bps were sizes of other moves; 35 bps was not this decision.",
  current=ca("2022-05-04"),
  facts=[fact("The MPC held an off-cycle meeting on 2nd and 4th May, 2022 and voted unanimously to increase the policy "
              "repo rate by 40 basis points to 4.40 per cent with immediate effect", GOV_MAY22)])
Q(T, SUB, "Basic",
  "On 6 June 2025, the MPC cut the policy repo rate by 50 basis points. What was the new repo rate, and what did the "
  "MPC do with its stance?",
  ["5.50%; changed the stance from accommodative to neutral", "5.75%; kept the stance accommodative",
   "5.25%; changed the stance from neutral to accommodative", "5.50%; changed the stance to calibrated tightening"],
  concept="June 2025 policy",
  explanation="In June 2025 the MPC reduced the repo rate by 50 bps to 5.50% with immediate effect (SDF 5.25%, MSF and "
              "Bank Rate 5.75%) and changed its stance from accommodative to neutral. A 100 bps CRR cut was announced "
              "at the same time.",
  steps=["Repo: −50 bps → 5.50%", "Stance: accommodative → neutral"],
  why="5.75% was the MSF rate after the cut; 5.25% came only in December 2025; calibrated tightening was adopted in "
      "October 2026.",
  current=ca("2025-06-06"),
  facts=[fact("The MPC decided to reduce the policy repo rate by 50 basis points to 5.50% with immediate effect and to "
              "change the stance from accommodative to neutral", MCIR_JUN25)])

repo_pre, onr, sdf_pre = 5.25, 5.06, 5.00
gap_bps = round((repo_pre - onr) * 100)
assert gap_bps == 19 and sdf_pre < onr < repo_pre
Q(T, SUB, "Intermediate",
  "On 6 October 2026, a day before the MPC raised the repo rate, the weighted average rate in the overnight money "
  "market segment was 5.06%. With the repo rate then at 5.25% and the SDF at 5.00%, where did the overnight rate "
  "stand?",
  ["19 bps below the repo rate, between the SDF rate and the repo rate", "19 bps above the repo rate",
   "Below the SDF rate, outside the corridor", "Exactly at the repo rate"],
  concept="Overnight rates within the LAF corridor",
  explanation="5.25 − 5.06 = 0.19, so the overnight rate was 19 bps below the repo rate but above the 5.00% SDF floor. "
              "With large surplus liquidity, overnight rates trade in the lower half of the corridor.",
  steps=["Repo 5.25 − 5.06 = 19 bps", "5.00 (SDF) < 5.06 < 5.25 (repo)"],
  why="The rate was below the repo rate and above the SDF floor.",
  computed=True, current=ca("2026-10-06"),
  facts=[fact("Money market operations as on October 6, 2026: overnight segment ₹7,24,312.63 crore at a weighted "
              "average rate of 5.06%; Standing Deposit Facility at 5.00%", MMO_OCT6),
         fact("Policy repo rate raised from 5.25% to 5.50% on October 7, 2026", GOV_OCT26)])

repo22 = 4.40
assert (round(repo22 - 0.25, 2), round(repo22 + 0.25, 2)) == (4.15, 4.65)
Q(T, SUB, "Intermediate",
  "After the repo rate was raised to 4.40% on 4 May 2022, what were the SDF rate and the MSF rate/Bank Rate?",
  ["SDF 4.15%; MSF and Bank Rate 4.65%", "SDF 3.35%; MSF and Bank Rate 4.65%", "SDF 4.15%; MSF and Bank Rate 5.40%",
   "SDF 3.40%; MSF and Bank Rate 5.40%"],
  concept="Corridor around the repo rate",
  explanation="The SDF rate is 25 bps below the repo rate and the MSF rate and Bank Rate 25 bps above it: 4.40 − 0.25 "
              "= 4.15% and 4.40 + 0.25 = 4.65%.",
  steps=["SDF = 4.40 − 0.25 = 4.15%", "MSF = Bank Rate = 4.40 + 0.25 = 4.65%"],
  why="3.35% is the fixed rate reverse repo, not the SDF; ±100 bps belongs to the 2011 corridor.",
  computed=True, current=ca("2022-05-04"),
  facts=[fact("The standing deposit facility (SDF) rate stands adjusted to 4.15 per cent and the marginal standing "
              "facility (MSF) rate and the Bank Rate to 4.65 per cent", GOV_MAY22)])

repo11 = 7.25
rr11, msf11 = repo11 - 1.0, repo11 + 1.0
width11 = round((msf11 - rr11) * 100)
width26 = round((5.75 - 5.25) * 100)
assert (rr11, msf11, width11, width26) == (6.25, 8.25, 200, 50)
Q(T, SUB, "Advanced",
  "On 3 May 2011, when the repo rate became the single policy rate, it was raised to 7.25%, with the reverse repo "
  "pegged 100 bps below and the new MSF 100 bps above it. How does that corridor compare with the corridor after the "
  "MPC decision of 7 October 2026?",
  ["2011: 6.25%–8.25% (200 bps wide); 2026: SDF 5.25% to MSF 5.75% (50 bps wide)",
   "2011: 6.75%–7.75% (100 bps wide); 2026: 5.25%–5.75% (50 bps wide)",
   "2011: 6.25%–8.25% (200 bps wide); 2026: 5.00%–6.00% (100 bps wide)",
   "Both corridors were 50 bps wide"],
  concept="Width of the policy corridor",
  explanation="In May 2011 the reverse repo was 7.25 − 1 = 6.25% and the MSF 7.25 + 1 = 8.25%, a 200 bps corridor. "
              "After 7 October 2026 the floor is the SDF at 5.25% and the ceiling the MSF at 5.75%, a 50 bps corridor.",
  steps=["2011: 6.25 to 8.25 → 200 bps", "2026: 5.25 to 5.75 → 50 bps"],
  why="The 2011 spreads were 100 bps on each side, not 50; the 2026 corridor is ±25 bps around 5.50%.",
  computed=True, current=ca("2011-05-03"),
  facts=[fact("The repo rate has become the only independently varying policy rate, with the reverse repo rate pegged "
              "at 100 bps below the repo rate and the MSF at 100 bps above it; repo 7.25% and reverse repo 6.25% "
              "effective May 3, 2011", MOHANTY),
         fact("SDF rate 5.25%; MSF rate and Bank Rate 5.75% after October 7, 2026", GOV_OCT26)])

impound_cr, crr_hike = 87_000, 0.005
ndtl_lakh_cr = impound_cr / crr_hike / 1e5
assert round(ndtl_lakh_cr) == 174
Q(T, SUB, "Advanced",
  "Along with the 40 bps repo hike of May 2022, RBI raised the CRR by 50 bps to 4.5%, which it estimated would "
  "withdraw about ₹87,000 crore of liquidity. What level of banks' NDTL does this estimate imply (approx.)?",
  ["₹174 lakh crore", "₹43.5 lakh crore", "₹19.3 lakh crore", "₹1,740 lakh crore"],
  concept="Liquidity impact of a CRR change",
  explanation="Liquidity withdrawn = change in CRR × NDTL, so NDTL = 87,000 ÷ 0.005 = ₹1,74,00,000 crore = ₹174 lakh "
              "crore.",
  steps=["NDTL = 87,000 crore ÷ 0.005", "= 1,74,00,000 crore = ₹174 lakh crore"],
  why="₹19.3 lakh crore divides by 4.5%; ₹43.5 lakh crore and ₹1,740 lakh crore misplace the decimal.",
  computed=True, current=ca("2022-05-04"),
  facts=[fact("CRR increased by 50 basis points to 4.5 per cent of NDTL effective from the fortnight beginning May 21, "
              "2022, withdrawing about ₹87,000 crore of liquidity", GOV_MAY22)])

# ================================================================= 7. Reverse Repo Rate (1 / 1 / 1)
T = "Reverse Repo Rate"
SUB = "Reverse repo and SDF"
Q(T, SUB, "Basic",
  "When the repo rate became the single policy rate in May 2011, the reverse repo was pegged 100 bps below it. To what "
  "spread was this narrowed with effect from 5 April 2016?",
  ["50 basis points below the repo rate", "25 basis points below the repo rate", "75 basis points below the repo rate",
   "150 basis points below the repo rate"],
  concept="Narrowing of the policy corridor",
  explanation="RBI's rate tables record that the reverse repo peg was brought down to 50 bps below the repo rate with "
              "effect from 5 April 2016, to align the weighted average call rate more finely with the repo rate. It "
              "was narrowed again to 25 bps from 6 April 2017.",
  steps=["May 2011: 100 bps below", "5 April 2016: 50 bps below", "6 April 2017: 25 bps below"],
  why="25 bps came in 2017; 75 and 150 bps were never the peg.",
  facts=[fact("The reverse repo peg was brought down to 50 basis points w.e.f. April 5, 2016; since April 6, 2017 the "
              "rate is pegged at 25 basis points below the repo rate", CORRIDOR)])
Q(T, SUB, "Intermediate",
  "On 6 October 2026, RBI announced an overnight Variable Rate Reverse Repo (VRRR) auction for 7 October 2026. What "
  "were its notified amount and tenor?",
  ["₹3,00,000 crore for one day", "₹50,000 crore for 14 days", "₹1,00,000 crore for 7 days",
   "₹3,00,000 crore for 28 days"],
  concept="Variable rate reverse repo",
  explanation="RBI's press release of 6 October 2026 notified a one-day VRRR auction of ₹3,00,000 crore on 7 October "
              "2026 (window 12:00 noon to 12:30 pm, reversal on 8 October), under the operational guidelines of 13 "
              "February 2020. A VRRR absorbs surplus liquidity.",
  steps=["Notified amount: ₹3 lakh crore", "Tenor: 1 day (reversal 8 October)"],
  why="The other combinations do not match the notified amount or tenor.",
  current=ca("2026-10-06"),
  facts=[fact("Overnight VRRR auction on October 7, 2026: notified amount ₹3,00,000 crore, tenor one day, window 12:00 "
              "noon to 12:30 PM, reversal date October 8, 2026", VRRR_OCT7)])

vrrr, sdf_amt, msf_amt = 192_357, 167_822, 475
net = vrrr + sdf_amt - msf_amt
assert net == 359_704
Q(T, SUB, "Advanced",
  "RBI's money market operations for 6 October 2026 show ₹1,92,357 crore absorbed through a VRRR at a weighted rate "
  "of 5.24%, ₹1,67,822 crore placed under the SDF at 5.00%, and ₹475 crore borrowed under the MSF at 5.50%. What was "
  "the net liquidity effect of that day's operations?",
  ["Net absorption of ₹3,59,704 crore", "Net injection of ₹3,59,704 crore", "Net absorption of ₹3,60,654 crore",
   "Net absorption of ₹24,535 crore"],
  concept="Absorption and injection under the LAF",
  explanation="VRRR and SDF absorb liquidity while MSF injects it: 1,92,357 + 1,67,822 − 475 = ₹3,59,704 crore of net "
              "absorption, matching RBI's reported figure for the day's operations.",
  steps=["Absorbed: 1,92,357 + 1,67,822 = 3,60,179", "Injected (MSF): 475", "Net absorption = 3,59,704"],
  why="Reverse repo and SDF absorb, so the net effect is not an injection; ₹3,60,654 crore adds the MSF instead of "
      "subtracting it; ₹24,535 crore is the gap between VRRR and SDF.",
  computed=True, current=ca("2026-10-06"),
  facts=[fact("October 6, 2026: VRRR ₹1,92,357 crore at 5.24%; SDF ₹1,67,822 crore at 5.00%; MSF ₹475 crore at 5.50%; "
              "net liquidity from today's operations -₹3,59,704 crore (absorption)", MMO_OCT6)])

# ================================================================= 8. CRR (0 / 2 / 1)
T = "CRR"
Q(T, "CRR concept", "Intermediate",
  "In August 2023, to absorb surplus liquidity (including that from the return of ₹2000 notes), RBI required banks to "
  "maintain an incremental CRR (I-CRR). What was it?",
  ["10% on the increase in NDTL between 19 May 2023 and 28 July 2023", "4.5% on the entire NDTL as on 28 July 2023",
   "10% on the entire NDTL for one year", "1% on the increase in NDTL since March 2023"],
  concept="Incremental CRR",
  explanation="On 10 August 2023 RBI asked scheduled banks to keep an I-CRR of 10% on the increase in their NDTL "
              "between 19 May 2023 and 28 July 2023, from the fortnight beginning 12 August 2023, as a temporary "
              "measure. The base CRR stayed at 4.5%.",
  steps=["I-CRR: 10% of increase in NDTL (19 May – 28 July 2023)", "Base CRR unchanged at 4.5%"],
  why="The I-CRR applied only to the increase in NDTL in that window, not to total NDTL.",
  facts=[fact("Scheduled banks to maintain an incremental CRR of 10 per cent on the increase in their NDTL between May "
              "19, 2023 and July 28, 2023, effective from the fortnight beginning August 12, 2023", ICRR)])
Q(T, "CRR concept", "Intermediate",
  "According to RBI's chronology, which liabilities were exempted from CRR from the week commencing 11 August 2001?",
  ["Inter-bank term liabilities of more than 15 days' maturity", "All savings bank deposits",
   "All term deposits of more than one year", "Deposits of senior citizens"],
  concept="Exemptions from CRR",
  explanation="RBI's chronology records that inter-bank term liabilities with maturity greater than 15 days were "
              "exempted from CRR from the week commencing 11 August 2001.",
  steps=["Exempt (2001): inter-bank term liabilities > 15 days"],
  why="Savings deposits, long term deposits and senior citizens' deposits remain part of NDTL for CRR.",
  facts=[fact("Effective week commencing August 11 (2001), inter-bank term liabilities greater than 15 days maturity "
              "exempt from CRR", CHRON_00)])

ndtl_may, ndtl_jul = 240_000, 252_500
icrr = 0.10 * (ndtl_jul - ndtl_may)
base = 0.045 * ndtl_jul
assert icrr == 1_250 and round(base + icrr, 1) == 12_612.5
Q(T, "CRR value", "Advanced",
  "A bank's NDTL was ₹2,40,000 crore on 19 May 2023 and ₹2,52,500 crore on 28 July 2023. Under the August 2023 rules "
  "(base CRR 4.5% plus I-CRR), what total cash balance had it to keep with RBI on NDTL of ₹2,52,500 crore?",
  ["₹12,612.5 crore", "₹11,362.5 crore", "₹25,250 crore", "₹1,250 crore"],
  concept="Base CRR plus incremental CRR",
  explanation="Base CRR = 4.5% × 2,52,500 = ₹11,362.5 crore. I-CRR = 10% × (2,52,500 − 2,40,000) = ₹1,250 crore. "
              "Total = ₹12,612.5 crore.",
  steps=["Base: 0.045 × 2,52,500 = 11,362.5", "I-CRR: 0.10 × 12,500 = 1,250", "Total = 12,612.5"],
  why="₹11,362.5 crore ignores the I-CRR; ₹1,250 crore is only the I-CRR; ₹25,250 crore applies 10% to all NDTL.",
  computed=True,
  facts=[fact("Incremental CRR of 10 per cent on the increase in NDTL between May 19, 2023 and July 28, 2023; CRR kept "
              "unchanged at 4.5 per cent", ICRR)])

# ================================================================= 9. SLR (2 / 2 / 2)
T = "SLR"
Q(T, "SLR value", "Basic",
  "RBI's records of reserve requirements show the Statutory Liquidity Ratio at its highest level, effective 22 "
  "September 1990. What was it?",
  ["38.5%", "25%", "40%", "31.5%"],
  concept="History of SLR",
  explanation="RBI's table of Bank Rate, CRR and SLR changes lists an SLR of 38.5% effective 22 September 1990, the "
              "peak before the post-1991 reductions.",
  steps=["SLR peak: 38.5% (22 September 1990)"],
  why="25% is the 1962 minimum; 40% is the statutory ceiling RBI can prescribe; 31.5% is not the peak.",
  facts=[fact("Statutory Liquidity Ratio 38.5 effective 22-09-1990", RATES_HIST),
         fact("SLR 38.5 per cent effective 22-09-1990", SLR_PEAK)])
Q(T, "SLR value", "Basic",
  "Under the glide path announced in RBI's statement of 5 December 2018, by how much was the SLR to be reduced every "
  "calendar quarter from 19.50% of NDTL?",
  ["25 basis points", "50 basis points", "10 basis points", "100 basis points"],
  concept="SLR glide path",
  explanation="RBI's circular of 5 December 2018 reduced the SLR by 25 bps every calendar quarter from 19.50% of NDTL, "
              "starting with 19.25% from 5 January 2019, until it reached 18%.",
  steps=["19.50% → 19.25% (Jan 2019) → … → 18.00%", "Step = 25 bps per quarter"],
  why="Steps were 25 bps, not 10, 50 or 100 bps.",
  facts=[fact("SLR requirement of banks reduced by 25 basis points every calendar quarter from 19.50 per cent of NDTL; "
              "19.25 per cent from January 5, 2019", SLR_2018)])
Q(T, "SLR value", "Intermediate",
  "From which date did the SLR of 18.00% of NDTL take effect under the December 2018 glide path?",
  ["11 April 2020", "5 January 2019", "4 January 2020", "1 April 2021"],
  concept="SLR glide path",
  explanation="The schedule was 19.25% (5 Jan 2019), 19.00% (13 Apr 2019), 18.75% (6 Jul 2019), 18.50% (12 Oct 2019), "
              "18.25% (4 Jan 2020) and 18.00% from 11 April 2020.",
  steps=["Last step: 18.25% → 18.00% on 11 April 2020"],
  why="5 January 2019 was the first step (19.25%); 4 January 2020 was 18.25%.",
  facts=[fact("SLR 18.25 per cent from January 4, 2020 and 18.00 per cent from April 11, 2020", SLR_2018)])
Q(T, "SLR concept", "Intermediate",
  "Under the facilities that let banks count part of their mandatory SLR holdings as Level 1 HQLA for the Liquidity "
  "Coverage Ratio, RBI raised FALLCR to 16% of NDTL in April 2022. Together with the 2% MSF window, what total "
  "carve-out from SLR did this give?",
  ["18% of NDTL", "16% of NDTL", "15% of NDTL", "20% of NDTL"],
  concept="SLR and LCR (FALLCR)",
  explanation="FALLCR lets banks reckon government securities within the mandatory SLR as Level 1 HQLA. In April 2022 "
              "it was raised to 16% of NDTL; with the 2% MSF window, the total carve-out became 18% of NDTL.",
  steps=["FALLCR 16% + MSF 2% = 18% of NDTL"],
  why="16% is FALLCR alone; 15% was the earlier FALLCR level; 20% overstates it.",
  current=ca("2022-04-18"),
  facts=[fact("April 18, 2022: banks permitted to reckon government securities as Level 1 HQLA under FALLCR within the "
              "mandatory SLR up to 16 per cent of NDTL; total carve-out 18 per cent (2 per cent MSF plus 16 per cent "
              "FALLCR)", FALLCR)])

steps_n = round((19.50 - 18.00) / 0.25)
ndtl_bank = 120_000
freed = ndtl_bank * 0.015
assert steps_n == 6 and freed == 1_800
Q(T, "SLR value", "Advanced",
  "Under the glide path from 19.50% to 18.00% (25 bps a quarter, January 2019 to April 2020), how many quarterly "
  "reductions were made, and how much of its SLR requirement did a bank with NDTL of ₹1,20,000 crore have released "
  "in all?",
  ["6 reductions; ₹1,800 crore", "8 reductions; ₹1,800 crore", "6 reductions; ₹300 crore",
   "4 reductions; ₹1,200 crore"],
  concept="SLR glide path arithmetic",
  explanation="(19.50 − 18.00) ÷ 0.25 = 6 quarterly cuts (Jan 2019, Apr 2019, Jul 2019, Oct 2019, Jan 2020, Apr 2020). "
              "Total cut 1.5% × 1,20,000 = ₹1,800 crore.",
  steps=["Cuts = 1.50 ÷ 0.25 = 6", "Release = 0.015 × 1,20,000 = 1,800 crore"],
  why="There were six steps, not four or eight; ₹300 crore is only one 25 bps step.",
  computed=True,
  facts=[fact("SLR schedule: 19.25% (Jan 5, 2019), 19.00% (Apr 13, 2019), 18.75% (Jul 6, 2019), 18.50% (Oct 12, "
              "2019), 18.25% (Jan 4, 2020), 18.00% (Apr 11, 2020)", SLR_2018)])

ndtl2, gsec_total, encumbered = 60_000, 11_500, 1_200
req = 0.18 * ndtl2
eligible = gsec_total - encumbered
assert req == 10_800 and eligible - req == -500
Q(T, "SLR concept", "Advanced",
  "A bank with NDTL of ₹60,000 crore holds government securities of ₹11,500 crore (book value), of which ₹1,200 "
  "crore are pledged under market repo and remain encumbered at day-end. It holds no other SLR assets. With SLR at "
  "18%, what is its SLR position?",
  ["Short by ₹500 crore", "Surplus of ₹700 crore", "Exactly compliant", "Short by ₹1,700 crore"],
  concept="Only unencumbered securities count for SLR",
  explanation="Required SLR = 18% × 60,000 = ₹10,800 crore. Only unencumbered securities count: 11,500 − 1,200 = "
              "₹10,300 crore, which is ₹500 crore short.",
  steps=["Requirement = 0.18 × 60,000 = 10,800", "Eligible = 11,500 − 1,200 = 10,300", "Shortfall = 500"],
  why="A surplus of ₹700 crore counts the encumbered securities; ₹1,700 crore double-deducts the pledge.",
  computed=True,
  facts=[fact("SLR assets: cash, gold, or unencumbered investment in specified securities; investments reported at "
              "book value including encumbered securities, but only the unencumbered portion counts toward SLR",
              SLR_MD25)])

# ================================================================= 10. Bank Rate (1 / 1 / 0)
T = "Bank Rate"
SUB = "Bank rate and MSF"
Q(T, SUB, "Basic",
  "When RBI began operations, the first Bank Rate in its records, effective 5 July 1935, was:",
  ["3.5%", "5%", "2%", "6%"],
  concept="History of the Bank Rate",
  explanation="RBI's table of Bank Rate, CRR and SLR changes starts with a Bank Rate of 3.5% effective 5 July 1935, "
              "the same date from which scheduled banks had to keep a CRR of 5% of demand liabilities.",
  steps=["Bank Rate, 5 July 1935: 3.5%"],
  why="5% was the first CRR on demand liabilities, not the Bank Rate.",
  facts=[fact("Bank Rate 3.5 effective 5/7/1935; CRR 5 per cent of demand liabilities effective 5/7/1935",
              RATES_HIST)])
Q(T, SUB, "Intermediate",
  "During the 1991 balance of payments crisis, to what level was the Bank Rate raised with effect from 9 October "
  "1991?",
  ["12%", "10%", "8%", "15%"],
  concept="Bank Rate in 1991",
  explanation="RBI's table of Bank Rate changes lists a Bank Rate of 12% effective 9 October 1991. It was later "
              "reduced (11% from 16 April 1997, among other changes).",
  steps=["9 October 1991: Bank Rate 12%"],
  why="10%, 8% and 15% do not match the entry.",
  facts=[fact("Bank Rate 12% effective 9/10/1991; 11% effective 16-04-1997", RATES_HIST)])

# ================================================================= 11. Inflation (3 / 1 / 1)
T = "Inflation"
Q(T, "CPI and WPI", "Basic",
  "According to MoSPI's release of 12 October 2026, what was India's headline CPI (combined) inflation in September "
  "2026?",
  ["5.54%", "4.83%", "3.48%", "6.08%"],
  concept="Latest CPI inflation",
  explanation="Headline inflation on the new CPI series (2024=100) rose to 5.54% in September 2026 from 4.83% in "
              "August, driven by food prices.",
  steps=["August 2026: 4.83%", "September 2026: 5.54%"],
  why="4.83% is August's figure; 3.48% was April's; 6.08% is rural inflation for September.",
  current=ca("2026-10-12"),
  facts=[fact("Retail inflation rose to 5.54 per cent in September 2026 from 4.83 per cent in August; MoSPI release "
              "of October 12, 2026", CPI_SEP26)])
Q(T, "CPI and WPI", "Basic",
  "Which body compiles the Consumer Price Index for Industrial Workers (CPI-IW), whose current series has base "
  "2016=100?",
  ["Labour Bureau, Ministry of Labour and Employment", "National Statistics Office, MoSPI",
   "Office of the Economic Adviser, DPIIT", "Reserve Bank of India"],
  concept="Consumer price indices in India",
  explanation="CPI-IW is compiled by the Labour Bureau under the Ministry of Labour and Employment; the 2016=100 series "
              "has been effective from September 2020 and is used to regulate wages and dearness allowance.",
  steps=["CPI (combined) → MoSPI (NSO)", "WPI → Office of the Economic Adviser", "CPI-IW → Labour Bureau"],
  why="MoSPI compiles CPI (combined); the Economic Adviser's office compiles WPI; RBI does not compile CPI-IW.",
  facts=[fact("The new series of Consumer Price Index for Industrial Workers (CPI-IW) on base 2016=100 has been "
              "effective from September 2020 (Labour Bureau)", CPI_IW)])
Q(T, "CPI and WPI", "Basic",
  "In September 2026, food inflation measured by the Consumer Food Price Index (CFPI) rose to:",
  ["7.74%", "5.97%", "5.54%", "4.88%"],
  concept="Food inflation",
  explanation="MoSPI's September 2026 release showed CFPI inflation rising to 7.74% from 5.97% in August, the main "
              "driver of the rise in headline CPI inflation to 5.54%.",
  steps=["CFPI: 5.97% (Aug) → 7.74% (Sep)"],
  why="5.97% is August's food inflation; 5.54% is headline CPI; 4.88% is urban inflation.",
  current=ca("2026-10-12"),
  facts=[fact("Food inflation (CFPI) rose from 5.97 per cent in August to 7.74 per cent in September 2026",
              CPI_SEP26)])
Q(T, "CPI and WPI", "Intermediate",
  "How did rural and urban CPI inflation compare in September 2026, according to MoSPI's provisional data?",
  ["Rural 6.08%, higher than urban 4.88%", "Urban 6.08%, higher than rural 4.88%", "Both were 5.54%",
   "Rural 4.83%, lower than urban 5.54%"],
  concept="Rural and urban CPI",
  explanation="Provisional data for September 2026 showed CPI inflation of 6.08% in rural areas and 4.88% in urban "
              "areas; the combined figure was 5.54%.",
  steps=["Rural 6.08%", "Urban 4.88%", "Combined 5.54%"],
  why="The rural and urban figures are reversed in one option; 5.54% is only the combined rate; 4.83% is August's "
      "combined rate.",
  current=ca("2026-10-12"),
  facts=[fact("CPI inflation was 6.08 per cent in rural areas and 4.88 per cent in urban areas in September 2026 "
              "(provisional)", CPI_SEP26)])

jul, aug, sep = 4.5, 4.8, 5.54
q2 = (jul + aug + sep) / 3
assert round(q2, 2) == 4.95 and round((q2 - 4.9) * 100) == 5
Q(T, "Inflation targeting", "Advanced",
  "The October 2026 MPC resolution projected Q2 (July–September) 2026-27 CPI inflation at 4.9%. Inflation was 4.5% in "
  "July and 4.8% in August (as cited by the Governor), and 5.54% in September. How did the realised quarterly average "
  "compare with the projection?",
  ["About 4.95%, roughly 5 bps above the projection and within the 2–6% band",
   "About 5.54%, 64 bps above the projection", "About 4.65%, below the projection",
   "About 6.1%, breaching the upper tolerance"],
  concept="Comparing realised inflation with projections",
  explanation="(4.5 + 4.8 + 5.54) ÷ 3 = 4.95%, about 5 bps above the 4.9% projection, above the 4% target but within "
              "the 2–6% tolerance band.",
  steps=["Sum = 14.84", "Average = 4.95%", "4.95 − 4.90 ≈ 0.05 = 5 bps"],
  why="5.54% is only September's reading; 4.65% averages only July and August; 6.1% is not supported.",
  computed=True, current=ca("2026-10-12"),
  facts=[fact("CPI inflation rose to 4.8 per cent in August from 4.5 per cent in July; Q2 2026-27 CPI projected at "
              "4.9 per cent", GOV_OCT26),
         fact("Retail inflation 5.54 per cent in September 2026", CPI_SEP26)])

# ================================================================= 12. NPA (1 / 3 / 5)
T = "NPA"
Q(T, "Classification", "Basic",
  "Under RBI's prudential norms, when can a loan account classified as NPA be upgraded to 'standard'?",
  ["Only when the entire arrears of interest and principal are paid by the borrower",
   "As soon as the borrower pays the latest instalment", "When the borrower pays at least half of the arrears",
   "Automatically after one year in the NPA category"],
  concept="Upgradation of NPAs",
  explanation="RBI's directions allow an NPA to be upgraded to standard only if the entire arrears of interest and "
              "principal are paid by the borrower. Partial payment does not upgrade the account.",
  steps=["NPA → standard only on payment of all arrears (interest + principal)"],
  why="Paying only the latest instalment or part of the arrears does not suffice; there is no automatic upgrade.",
  facts=[fact("Loan accounts classified as NPAs may be upgraded as 'standard' asset only if entire arrears of interest "
              "and principal are paid by the borrower", IRAC_MD)])
Q(T, "Classification", "Intermediate",
  "A borrower has three credit facilities with a bank, all classified as NPA. He clears all arrears on two of them "
  "but not on the third. Under RBI's norms, what happens?",
  ["None of the facilities can be upgraded until arrears on all facilities are paid",
   "The two cleared facilities are upgraded to standard", "All three are upgraded because most arrears are paid",
   "The third facility is written off and the other two upgraded"],
  concept="Borrower-wise upgradation",
  explanation="For borrowers with more than one credit facility, upgradation from NPA to standard requires repayment "
              "of arrears of interest and principal on all the credit facilities.",
  steps=["Multiple facilities → all arrears on all facilities must be paid", "One facility still in arrears → no "
         "upgrade"],
  why="Upgradation is borrower-wise, not facility-wise, and there is no automatic write-off.",
  facts=[fact("In case of borrowers having more than one credit facility, loan accounts shall be upgraded from NPA to "
              "standard asset category only upon repayment of entire arrears of interest and principal pertaining to "
              "all the credit facilities", IRAC_MD)])
Q(T, "Resolution and IBC", "Intermediate",
  "After a corporate insolvency resolution process (CIRP) has been admitted, can it be withdrawn under the IBC?",
  ["Yes, by the Adjudicating Authority on an application through the resolution professional, with approval of 90% "
   "of the voting share of the committee of creditors",
   "No, an admitted CIRP can never be withdrawn", "Yes, with approval of 51% of the voting share of the committee of "
   "creditors", "Yes, at the sole discretion of the applicant creditor"],
  concept="Withdrawal of CIRP",
  explanation="IBBI's FAQs explain that a CIRP may be withdrawn before or even after admission. After admission, the "
              "Adjudicating Authority may allow withdrawal on an application made through the resolution "
              "professional with the approval of 90% of the voting share of the committee of creditors.",
  steps=["Withdrawal after admission → application through RP", "CoC approval: 90% voting share"],
  why="Withdrawal is possible; the threshold is 90%, not 51%; the applicant alone cannot withdraw it.",
  facts=[fact("The Adjudicating Authority may allow withdrawal of application admitted under section 7, 9 or 10, on an "
              "application made by the applicant through the resolution professional, with the approval of 90 percent "
              "of voting share of the committee of creditors", IBBI_FAQ)])
Q(T, "Resolution and IBC", "Intermediate",
  "A moratorium under Section 14 of the IBC is in force against a company undergoing CIRP. Its loan is also backed by "
  "a personal guarantee from the promoter. Can the bank proceed against the guarantor?",
  ["Yes; the moratorium does not apply to a surety in a contract of guarantee to the corporate debtor",
   "No; the moratorium protects guarantors as well", "Only after the CIRP is completed",
   "Only with the approval of the committee of creditors"],
  concept="Scope of the IBC moratorium",
  explanation="Under Section 14(3), the moratorium does not apply to a surety in a contract of guarantee to a corporate "
              "debtor, so actions against a guarantor are not affected.",
  steps=["Section 14(1): bars suits, transfers, enforcement of security (incl. SARFAESI), recovery by lessors",
         "Section 14(3): does not apply to a surety/guarantor"],
  why="Guarantors are expressly outside the moratorium; no waiting period or CoC approval is needed.",
  facts=[fact("As per section 14(3) of the Code, the order of moratorium shall not apply to a surety in a contract of "
              "guarantee to a corporate debtor", IBBI_FAQ)])

exp = {"farm": (400, 0.0025), "cre": (300, 0.01), "cre_rh": (200, 0.0075), "other": (1000, 0.004)}
prov = sum(a * r for a, r in exp.values())
assert round(prov, 2) == 9.5
Q(T, "Classification", "Advanced",
  "A bank's standard advances consist of farm credit of ₹400 crore, commercial real estate (CRE) of ₹300 crore, CRE "
  "– residential housing of ₹200 crore and other loans of ₹1,000 crore. Using RBI's standard-asset provisioning "
  "rates, what is the minimum provision required?",
  ["₹9.5 crore", "₹7.6 crore", "₹19.0 crore", "₹10.0 crore"],
  concept="Provisioning on standard assets",
  explanation="Rates: farm credit 0.25%, CRE 1.00%, CRE-RH 0.75%, other loans 0.40%. Provision = 400 × 0.0025 + 300 × "
              "0.01 + 200 × 0.0075 + 1,000 × 0.004 = 1 + 3 + 1.5 + 4 = ₹9.5 crore.",
  steps=["Farm: 1.0", "CRE: 3.0", "CRE-RH: 1.5", "Other: 4.0", "Total = 9.5"],
  why="₹7.6 crore applies 0.40% to everything; ₹19.0 crore applies 1% to everything; ₹10.0 crore treats CRE-RH like "
      "CRE at 1%.",
  computed=True,
  facts=[fact("Standard asset provisioning: farm credit to agricultural activities, individual housing and SME 0.25 "
              "per cent; CRE 1.00 per cent; CRE-RH 0.75 per cent; other loans and advances 0.40 per cent", IRAC_MD)])
Q(T, "Classification", "Advanced",
  "Consider the following statements about income recognition on NPAs under RBI's prudential norms:\n"
  "I. Interest accrued and credited to income in the past on an account that becomes NPA must be reversed if it has "
  "not been realised.\n"
  "II. Interest realised on an NPA may be taken to income, provided the credit is not out of fresh facilities "
  "sanctioned to the borrower.\n"
  "III. Interest on an NPA continues to be booked as income every quarter on an accrual basis.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Income recognition on NPAs",
  explanation="Unrealised interest already credited on an account that turns NPA is reversed, and further interest is "
              "not applied but tracked in a memorandum account (III wrong). Interest actually realised may be taken "
              "to income if it does not come from fresh facilities sanctioned to the borrower (II).",
  steps=["I: correct", "II: correct", "III: wrong (no accrual on NPAs)"],
  why="III contradicts the realisation basis; 'I only' omits II.",
  facts=[fact("Interest accrued and credited to income in past periods shall be reversed if not realised; further "
              "application of interest stops and is tracked in a memorandum account; interest realised on NPAs may be "
              "taken to income provided it is not out of fresh credit facilities sanctioned to the borrower",
              IRAC_MD)])

icd = dt.date(2026, 3, 2)
pa = icd + dt.timedelta(days=3)
im_cap = icd + dt.timedelta(days=53)
assert pa == dt.date(2026, 3, 5) and im_cap == dt.date(2026, 4, 24)
Q(T, "Resolution and IBC", "Advanced",
  "A CIRP commences on 2 March 2026 (day 1), and the interim resolution professional is appointed the same day. Under "
  "the IBBI regulations described in its FAQs, by when must the public announcement in Form A be made, and what is "
  "the latest date by which the information memorandum must reach CoC members?",
  ["5 March 2026; 24 April 2026", "2 April 2026; 24 April 2026", "5 March 2026; 2 June 2026",
   "9 March 2026; 30 April 2026"],
  concept="CIRP timelines",
  explanation="The IRP makes the public announcement within three days of appointment: 2 March + 3 days = 5 March. "
              "The information memorandum is due within two weeks of the RP's appointment but not later than the 54th "
              "day from the insolvency commencement date; counting 2 March as day 1, day 54 is 24 April 2026.",
  steps=["Public announcement: 2 Mar + 3 days = 5 Mar", "Day 54: 2 Mar + 53 days = 24 Apr"],
  why="The announcement is due in three days, not a month or a week; 2 June and 30 April do not match day 54.",
  computed=True,
  facts=[fact("Interim resolution professional makes a public announcement in Form A within three days from his "
              "appointment; RP to submit information memorandum within 2 weeks of his appointment, but not later than "
              "54th day from the insolvency commencement date", IBBI_FAQ)])
Q(T, "Resolution and IBC", "Advanced",
  "Consider the following statements about the committee of creditors (CoC) under the IBC, as explained by IBBI:\n"
  "I. A CoC meeting needs members holding at least 33% of the voting rights, present in person or by video "
  "conferencing, for quorum.\n"
  "II. Operational creditors whose aggregate dues are at least 10% of the debt receive notice of CoC meetings but have "
  "no voting rights.\n"
  "III. The resolution professional appoints two registered valuers to determine fair value and liquidation value.\n"
  "Which of the above is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I and III only"],
  concept="Working of the committee of creditors",
  explanation="Quorum is 33% of voting rights (I). Notice goes to operational creditors (or their representatives) if "
              "their aggregate dues are not less than 10% of the debt, but only CoC members vote (II). The RP appoints "
              "two registered valuers within 7 days of appointment, not later than the 47th day (III). All three are "
              "correct.",
  steps=["I: correct", "II: correct", "III: correct"],
  why="Each of the other options leaves out a correct statement.",
  facts=[fact("Quorum: members holding at least thirty three percent of voting rights; notice to operational creditors "
              "if aggregate dues not less than 10% of the debt, but only CoC members have voting rights; RP appoints "
              "two registered valuers to determine fair value and liquidation value", IBBI_FAQ)])

default = dt.date(2026, 1, 10)
review_end = default + dt.timedelta(days=30)
deadline = review_end + dt.timedelta(days=180)
exposure = 500
addl = 0.20 * exposure
assert review_end == dt.date(2026, 2, 9) and deadline == dt.date(2026, 8, 8) and addl == 100
Q(T, "Resolution and IBC", "Advanced",
  "A large borrower defaults with a lender on 10 January 2026. Apply the timelines and disincentives of RBI's "
  "Prudential Framework for Resolution of Stressed Assets as laid down in its circular of 7 June 2019: a review "
  "period of 30 days from default, and a resolution plan to be implemented within 180 days from the end of the "
  "review period. If no plan is implemented by then, what additional provision does a lender with ₹500 crore "
  "exposure make?",
  ["₹100 crore (20%), with the deadline falling on 8 August 2026",
   "₹175 crore (35%), with the deadline falling on 8 July 2026",
   "₹75 crore (15%), with the deadline falling on 9 February 2026",
   "Nothing, as long as the account is under review"],
  concept="Disincentives for delayed resolution",
  explanation="Review period ends 30 days after default: 9 February 2026. Implementation deadline: 180 days later, 8 "
              "August 2026. If the plan is not implemented by then, lenders make an additional 20% provision (₹100 "
              "crore on ₹500 crore); a further 15% (total 35%) applies if it is still not implemented within 365 days "
              "from the start of the review period.",
  steps=["Review end: 10 Jan + 30 = 9 Feb 2026", "Deadline: 9 Feb + 180 = 8 Aug 2026",
         "Additional provision: 20% × 500 = ₹100 crore"],
  why="35% applies only after 365 days from the start of review; 15% is the second tranche alone; provisions are due "
      "once the 180-day window lapses.",
  computed=True,
  facts=[fact6("Circular of 7 June 2019: review period of thirty days from default; resolution plan implemented within "
               "180 days from the end of the review period; additional provision of 20% if not implemented within "
               "180 days, and further 15% (total 35%) if not implemented within 365 days from commencement of review "
               "period", STRESS)])

# ================================================================= 13. Basel Norms (1 / 6 / 1)
T = "Basel Norms"
Q(T, "Capital adequacy", "Basic",
  "Basel II (June 2004) rests on three pillars. Pillar 2 refers to:",
  ["Supervisory review of capital adequacy", "Minimum capital requirements",
   "Market discipline through disclosure", "Liquidity coverage"],
  concept="Three pillars of Basel II",
  explanation="The Basel Committee describes Basel II's three pillars as minimum capital requirements (Pillar 1), "
              "supervisory review of an institution's capital adequacy and internal assessment process (Pillar 2), "
              "and effective use of disclosure to strengthen market discipline (Pillar 3).",
  steps=["Pillar 1: minimum capital", "Pillar 2: supervisory review", "Pillar 3: market discipline"],
  why="Minimum capital is Pillar 1; disclosure/market discipline is Pillar 3; liquidity coverage is a Basel III "
      "liquidity standard.",
  facts=[fact("Basel II comprised three pillars: minimum capital requirements, supervisory review of an institution's "
              "capital adequacy and internal assessment process, and effective use of disclosure to strengthen market "
              "discipline", BCBS_HIST)])
Q(T, "Capital adequacy", "Intermediate",
  "In RBI's 2025 list of Domestic Systemically Important Banks (released 2 December 2025), which bank is in bucket 1, "
  "and what additional CET1 requirement applies to it?",
  ["ICICI Bank; 0.20% of RWAs", "HDFC Bank; 0.40% of RWAs", "ICICI Bank; 0.40% of RWAs", "State Bank of India; 0.20% "
   "of RWAs"],
  concept="D-SIB surcharges",
  explanation="The 2025 list places SBI in bucket 4 (0.80%), HDFC Bank in bucket 2 (0.40%) and ICICI Bank in bucket 1 "
              "(0.20%), based on data as on 31 March 2025. The surcharge is in addition to the capital conservation "
              "buffer.",
  steps=["Bucket 4: SBI 0.80%", "Bucket 2: HDFC 0.40%", "Bucket 1: ICICI 0.20%"],
  why="HDFC Bank is in bucket 2; SBI is in bucket 4.",
  current=ca("2025-12-02"),
  facts=[fact("2025 list of D-SIBs: bucket 4 State Bank of India 0.80%; bucket 2 HDFC Bank 0.40%; bucket 1 ICICI Bank "
              "0.20%; based on data as on March 31, 2025", DSIB_25)])
Q(T, "Capital adequacy", "Intermediate",
  "RBI's D-SIB framework has five buckets. What additional CET1 surcharge applies to bucket 5, and which bank was in "
  "it in the 2025 list?",
  ["1% of RWAs; no bank was in bucket 5", "1% of RWAs; State Bank of India", "0.60% of RWAs; HDFC Bank",
   "0.80% of RWAs; no bank was in bucket 5"],
  concept="D-SIB buckets",
  explanation="The surcharges are 1% (bucket 5), 0.80% (4), 0.60% (3), 0.40% (2) and 0.20% (1). In 2025, buckets 5 and "
              "3 were empty; SBI was in bucket 4.",
  steps=["Bucket 5: 1%, empty", "Bucket 4: 0.80%, SBI", "Bucket 3: 0.60%, empty"],
  why="SBI is in bucket 4 (0.80%); 0.60% is bucket 3, which was empty.",
  current=ca("2025-12-02"),
  facts=[fact("Additional CET1 requirement: bucket 5 1% (none), bucket 4 0.80% (SBI), bucket 3 0.60% (none), bucket 2 "
              "0.40% (HDFC Bank), bucket 1 0.20% (ICICI Bank)", DSIB_25)])
Q(T, "Capital adequacy", "Intermediate",
  "In November 2023, RBI raised the risk weight on consumer credit exposures of commercial banks (excluding housing, "
  "education, vehicle and gold-backed loans) from 100% to:",
  ["125%", "150%", "75%", "200%"],
  concept="Risk weights on consumer credit",
  explanation="RBI's regulatory measures of 16 November 2023 increased the risk weight on consumer credit exposures of "
              "commercial banks, including personal loans but excluding housing, education, vehicle and gold-backed "
              "loans, by 25 percentage points to 125%. Credit card receivables of banks went from 125% to 150%.",
  steps=["Consumer credit: 100% → 125%", "Credit card receivables (banks): 125% → 150%"],
  why="150% is the new credit card risk weight; 75% is the regulatory retail weight; 200% was not prescribed.",
  current=ca("2023-11-16"),
  facts=[fact("Risk weights on consumer credit exposure of commercial banks increased by 25 percentage points to 125 "
              "per cent, excluding housing, education, vehicle and gold-backed loans; credit card receivables to 150 "
              "per cent", CONSUMER_RW),
         fact("Risk weights on consumer credit were increased to 125 per cent, excluding housing, education, vehicle "
              "and gold loans", MFI_RW)])
Q(T, "Capital adequacy", "Intermediate",
  "Under RBI's February 2025 review of risk weights on microfinance loans, what risk weight applies to microfinance "
  "loans that are in the nature of consumer credit?",
  ["100%, excluded from the higher 125% risk weight", "125%, the same as other consumer credit", "150%", "50%"],
  concept="Risk weights on microfinance loans",
  explanation="RBI decided that microfinance loans in the nature of consumer credit would carry a 100% risk weight and "
              "be excluded from the higher risk weights on consumer credit. Other microfinance loans may be treated as "
              "regulatory retail (75%) if they meet the criteria; for RRBs and LABs all microfinance loans carry "
              "100%.",
  steps=["Consumer-type microfinance → 100%", "Others meeting criteria → regulatory retail 75%"],
  why="The point of the review was to exclude them from 125%; 150% and 50% are not the prescribed weights.",
  current=ca("2025-02-25"),
  facts=[fact("Microfinance loans in the nature of consumer credit shall be subject to a risk weight of 100 per cent "
              "and excluded from the applicability of higher risk weights", MFI_RW)])
Q(T, "Capital adequacy", "Intermediate",
  "The Basel Committee's market risk amendment of January 1996 was significant because it:",
  ["Added capital requirements for market risk and allowed banks to use internal value-at-risk models",
   "Introduced the Liquidity Coverage Ratio", "Replaced Basel I with the three-pillar framework",
   "Introduced the leverage ratio"],
  concept="Evolution of Basel standards",
  explanation="The 1996 amendment to the 1988 Accord brought market risk into capital requirements (to take effect by "
              "the end of 1997) and allowed banks to use internal value-at-risk models to measure it.",
  steps=["1988: Basel I (credit risk)", "1996: market risk amendment, internal VaR models", "2004: Basel II"],
  why="LCR and the leverage ratio are Basel III; the three pillars came with Basel II in 2004.",
  facts=[fact("January 1996: amendment to the Capital Accord to incorporate market risks, effective at the end of 1997; "
              "banks allowed to use internal value-at-risk models", BCBS_HIST)])
Q(T, "Capital adequacy", "Intermediate",
  "According to the Basel Committee's own history, its membership has grown from the G10 to how many institutions?",
  ["45 institutions from 28 jurisdictions", "20 institutions from 20 jurisdictions",
   "27 institutions from 27 countries", "190 central banks"],
  concept="Basel Committee",
  explanation="The Basel Committee, set up by the G10 central bank Governors at the end of 1974, has expanded its "
              "membership to 45 institutions from 28 jurisdictions.",
  steps=["Origin: G10 (1974)", "Now: 45 institutions, 28 jurisdictions"],
  why="The other figures do not match the Committee's stated membership.",
  facts=[fact("The Committee expanded its membership from the G10 to 45 institutions from 28 jurisdictions",
              BCBS_HIST)])

rw = {"personal": (400, 1.25), "cards": (100, 1.50), "mfi_consumer": (200, 1.00), "home": (300, 0.0)}
rwa = sum(a * w for a, w in list(rw.values())[:3])
assert rwa == 850
Q(T, "Capital adequacy", "Advanced",
  "Using RBI's current risk weights for a scheduled commercial bank, what are the risk-weighted assets for: personal "
  "loans of ₹400 crore (consumer credit), credit card receivables of ₹100 crore, and microfinance loans in the nature "
  "of consumer credit of ₹200 crore?",
  ["₹850 crore", "₹875 crore", "₹700 crore", "₹900 crore"],
  concept="Computing RWAs",
  explanation="Personal loans 400 × 125% = 500; credit cards 100 × 150% = 150; consumer-type microfinance 200 × 100% "
              "= 200. Total RWAs = ₹850 crore.",
  steps=["400 × 1.25 = 500", "100 × 1.50 = 150", "200 × 1.00 = 200", "Total = 850"],
  why="₹875 crore puts card receivables at 175%; ₹700 crore uses 100% for everything; ₹900 crore applies 125% to "
      "microfinance too.",
  computed=True,
  facts=[fact("Consumer credit 125 per cent; credit card receivables of SCBs 150 per cent", CONSUMER_RW),
         fact("Microfinance loans in the nature of consumer credit: 100 per cent risk weight", MFI_RW)])

# ================================================================= 14. Financial Inclusion (1 / 3 / 1)
T = "Financial Inclusion"
Q(T, "PMJDY and allied schemes", "Basic",
  "RBI's Financial Literacy Week 2026, observed from 9 to 13 February 2026, had which theme?",
  ["KYC – Your First Step to Safe Banking", "Power of Compounding", "Go Digital, Go Secure",
   "Women and Financial Inclusion"],
  concept="Financial literacy campaigns",
  explanation="RBI's financial education site states that Financial Literacy Week 2026 was observed from 9 to 13 "
              "February 2026 on the theme 'KYC – Your First Step to Safe Banking', covering KYC basics, the Central "
              "KYC Registry and account hygiene.",
  steps=["FLW 2026: 9–13 February", "Theme: KYC – Your First Step to Safe Banking"],
  why="The other themes are not the 2026 theme.",
  current=ca("2026-02-09"),
  facts=[fact("Financial Literacy Week 2026 will be observed from February 09-13, 2026 on the theme of 'KYC - Your "
              "First Step to Safe Banking'", FLW_26)])
Q(T, "Business correspondents", "Intermediate",
  "Under Pradhan Mantri Jan Dhan Yojana, the business correspondent agents who provide basic banking access in rural "
  "areas are popularly called:",
  ["Bank Mitras", "Jan Sevaks", "Banking Sahayaks", "Krishi Mitras"],
  concept="BCs under PMJDY",
  explanation="The Department of Financial Services lists access to banking in rural areas through Bank Mitras "
              "(business correspondent agents) among PMJDY's features, along with BSBD accounts, RuPay cards and "
              "overdrafts.",
  steps=["PMJDY delivery in rural areas → Bank Mitras (BC agents)"],
  why="The other names are not the PMJDY term for BC agents.",
  facts=[fact("PMJDY features include rural banking access through Bank Mitras", PMJDY_DFS)])
Q(T, "Business correspondents", "Intermediate",
  "By its circular of 28 September 2010, RBI permitted banks to engage which additional category of entities as "
  "Business Correspondents?",
  ["Companies registered under the Companies Act, 1956 with large and widespread retail outlets, excluding NBFCs",
   "All NBFCs, including microfinance companies", "Only post offices and Section 25 companies",
   "Foreign companies without retail outlets in India"],
  concept="Expanding the BC model",
  explanation="In September 2010 RBI allowed scheduled commercial banks (including RRBs and LABs) to engage companies "
              "registered under the Indian Companies Act, 1956, with large and widespread retail outlets, as BCs, in "
              "addition to entities already permitted, but excluding NBFCs.",
  steps=["2006: NGOs, post offices, Section 25 companies etc.", "Sept 2010: 'for-profit' companies, excluding NBFCs"],
  why="NBFCs were expressly excluded; post offices and Section 25 companies were already permitted; foreign companies "
      "were not the category added.",
  facts=[fact("Banks may engage companies registered under the Indian Companies Act, 1956, excluding Non Banking "
              "Financial Companies (NBFCs), with large and widespread retail outlets, as BCs", BC_2010)])
Q(T, "Business correspondents", "Intermediate",
  "Under RBI's BC guidelines (September 2010 circular), how are Business Correspondents to be compensated?",
  ["Banks may pay BCs a reasonable commission or fee; BCs must not charge customers any fee directly",
   "BCs may collect a fee from each customer at their discretion", "BCs earn interest on the deposits they collect",
   "BCs are paid by RBI from the Financial Inclusion Fund"],
  concept="Remuneration of BCs",
  explanation="Banks may pay a reasonable commission/fee to the BC, and the agreement must prohibit the BC from "
              "charging any fee to customers directly for services rendered on the bank's behalf. Banks themselves "
              "may collect reasonable service charges in a transparent manner.",
  steps=["Bank → pays BC", "BC → cannot charge customers directly"],
  why="Customers cannot be charged by BCs directly, BCs do not earn interest on deposits, and RBI does not pay them.",
  facts=[fact("Banks may pay reasonable commission/fee to the BC; the agreement should contain a clause that the BC "
              "shall not charge any fee to the customers directly", BC_2010)])
Q(T, "Business correspondents", "Advanced",
  "Under RBI's circular of 28 September 2010, which of the following could a bank engage as a Business "
  "Correspondent (each retail outlet attached to a designated base branch)?\n"
  "P. A company with a large retail network, whose outlet in a rural area is 25 km from the base branch\n"
  "Q. A non-banking financial company with many branches\n"
  "R. A company with a large retail network, whose outlet in a metropolitan centre is 12 km from the base branch\n"
  "S. A company with a large retail network, whose outlet in a semi-urban area is 28 km from the base branch",
  ["P and S only", "P, R and S", "Q and R only", "P only"],
  concept="Eligibility and distance norms for BCs",
  explanation="NBFCs are excluded (Q out). The distance between a BC outlet and its base branch should ordinarily not "
              "exceed 30 km in rural, semi-urban and urban areas and 5 km in metropolitan centres. P (25 km rural) "
              "and S (28 km semi-urban) are within limits; R (12 km in a metro) exceeds 5 km.",
  steps=["Q: NBFC → excluded", "P: 25 ≤ 30 ✓", "R: 12 > 5 (metro) ✗", "S: 28 ≤ 30 ✓"],
  why="Options with Q or R are wrong; 'P only' leaves out S.",
  computed=True,
  facts=[fact("Distance between the place of business of a BC and the base branch should ordinarily not exceed 30 kms "
              "in rural, semi-urban and urban areas and 5 kms in metropolitan centres; companies excluding NBFCs",
              BC_2010)])

# ================================================================= 15. Priority Sector Lending (4 / 1 / 1)
T = "Priority Sector Lending"
SUB = "Targets and sub-targets"
Q(T, SUB, "Basic",
  "Which of the following is NOT one of the eight categories of priority sector under RBI's PSL directions?",
  ["Consumer durables", "Social infrastructure", "Renewable energy", "Export credit"],
  concept="Categories of priority sector",
  explanation="The eight categories are Agriculture; Micro, Small and Medium Enterprises; Export Credit; Education; "
              "Housing; Social Infrastructure; Renewable Energy; and Others. Loans for consumer durables are not a "
              "priority sector category.",
  steps=["8 categories: Agri, MSME, Export credit, Education, Housing, Social infra, Renewable energy, Others"],
  why="Social infrastructure, renewable energy and export credit are all listed categories.",
  facts=[fact("The categories under priority sector are Agriculture; Micro, Small and Medium Enterprises; Export "
              "Credit; Education; Housing; Social Infrastructure; Renewable Energy; and Others", PSL_MD)])
Q(T, SUB, "Basic",
  "Up to what amount per borrowing entity do bank loans to Farmer Producer Organisations/Companies (FPOs/FPCs), "
  "undertaking farming with assured marketing at a pre-determined price, qualify as priority sector (agriculture)?",
  ["₹10 crore", "₹2 crore", "₹50 crore", "₹100 crore"],
  concept="Agriculture – FPO loans",
  explanation="Loans up to ₹10 crore per borrowing entity to FPOs/FPCs undertaking farming with assured marketing of "
              "their produce at a pre-determined price qualify under agriculture.",
  steps=["FPO/FPC loans → up to ₹10 crore per entity"],
  why="₹50 crore is the start-up limit; ₹100 crore is the food and agro-processing limit; ₹2 crore is not the FPO "
      "limit.",
  facts=[fact("Loans up to ₹10 crore per borrowing entity to FPOs/FPCs undertaking farming with assured marketing of "
              "their produce at a pre-determined price", PSL_MD)])
Q(T, SUB, "Basic",
  "Bank loans to individual households for renewable energy (for example rooftop solar) qualify as priority sector "
  "up to what limit per borrower?",
  ["₹10 lakh", "₹35 lakh", "₹1 lakh", "₹25 lakh"],
  concept="Renewable energy under PSL",
  explanation="Under the renewable energy category, the loan limit for individual households is ₹10 lakh per "
              "borrower. (Larger limits apply to renewable energy generators and public utilities.)",
  steps=["Individual households → ₹10 lakh per borrower"],
  why="₹35 crore (not lakh) is the limit for generators and public utilities; ₹1 lakh and ₹25 lakh do not apply.",
  facts=[fact("For individual households, the loan limit will be ₹10 lakh per borrower", PSL_MD)])
Q(T, SUB, "Basic",
  "Under the weaker sections category of PSL, loans to individual women beneficiaries count up to what amount per "
  "borrower?",
  ["₹2 lakh", "₹50,000", "₹10 lakh", "₹5 lakh"],
  concept="Weaker sections",
  explanation="Weaker sections include small and marginal farmers, SC/ST, SHGs/JLGs, persons with disabilities, "
              "transgenders and individual women beneficiaries up to ₹2 lakh per borrower, among others.",
  steps=["Individual women beneficiaries → up to ₹2 lakh"],
  why="The other amounts are not the prescribed limit.",
  facts=[fact("Weaker sections include individual women beneficiaries up to ₹2 lakh per borrower", PSL_MD)])
Q(T, SUB, "Intermediate",
  "For loans to individuals for repairs to their dwelling units to qualify as priority sector, what are the loan "
  "limits by population of the centre?",
  ["₹15 lakh (50 lakh and above), ₹12 lakh (10 lakh to under 50 lakh), ₹10 lakh (below 10 lakh)",
   "₹10 lakh in all centres", "₹25 lakh (metros) and ₹15 lakh elsewhere",
   "₹15 lakh (10 lakh and above) and ₹6 lakh (below 10 lakh)"],
  concept="Housing repair loans under PSL",
  explanation="Loans for repairs to damaged dwelling units qualify up to ₹15 lakh in centres with population of 50 "
              "lakh and above, ₹12 lakh in centres with 10 lakh to below 50 lakh, and ₹10 lakh in centres below 10 "
              "lakh.",
  steps=["≥ 50 lakh population: ₹15 lakh", "10–50 lakh: ₹12 lakh", "< 10 lakh: ₹10 lakh"],
  why="The other options do not match the three-tier limits.",
  facts=[fact("Housing repair loans: ₹15 lakh in centres with population of 50 lakh and above; ₹12 lakh for 10 lakh "
              "to below 50 lakh; ₹10 lakh for below 10 lakh", PSL_MD)])

prev_psl, via_nbfc = 60_000, 3_600
cap = 0.05 * prev_psl
counted = min(via_nbfc, cap)
assert cap == 3_000 and counted == 3_000
Q(T, SUB, "Advanced",
  "A bank's total priority sector lending in the previous financial year was ₹60,000 crore. This year it gives "
  "₹3,600 crore to NBFCs for on-lending to eligible priority sector borrowers. Under RBI's PSL directions, how much "
  "of this can be classified as priority sector?",
  ["₹3,000 crore", "₹3,600 crore", "₹6,000 crore", "₹1,800 crore"],
  concept="Cap on bank lending through NBFCs",
  explanation="Bank loans to NBFCs for on-lending are classified as priority sector up to an overall limit of 5% of "
              "the bank's total PSL of the previous financial year: 5% × 60,000 = ₹3,000 crore, so only ₹3,000 crore "
              "of the ₹3,600 crore counts.",
  steps=["Cap = 5% × 60,000 = 3,000", "Counted = min(3,600, 3,000) = 3,000"],
  why="₹3,600 crore ignores the cap; ₹6,000 crore uses 10% (the MFI on-lending cap); ₹1,800 crore uses 3%.",
  computed=True,
  facts=[fact("Bank loans to NBFCs for on-lending allowed up to an overall limit of 5% of individual bank's total "
              "priority sector lending of the previous financial year", PSL_MD)])

# ================================================================= 16. RBI Integrated Ombudsman Scheme (2 / 1 / 2)
T = "RBI Integrated Ombudsman Scheme"
Q(T, "Process and limits", "Basic",
  "Complaints under the Reserve Bank – Integrated Ombudsman Scheme, 2026 can be filed online on RBI's Complaint "
  "Management System at:",
  ["https://cms.rbi.org.in", "https://sachet.rbi.org.in", "https://www.pgportal.gov.in",
   "https://www.npci.org.in/complaint"],
  concept="Filing a complaint",
  explanation="RBI's FAQs on RB-IOS, 2026 direct customers to file complaints online on the CMS portal at "
              "https://cms.rbi.org.in.",
  steps=["Online filing → CMS portal cms.rbi.org.in"],
  why="Sachet is RBI's portal on unauthorised deposit-taking; CPGRAMS (pgportal) is the Government's grievance portal; "
      "NPCI does not run the RBI Ombudsman.",
  facts=[fact("Complaints can be lodged online on the CMS portal at https://cms.rbi.org.in", RBIOS_FAQ)])
Q(T, "Scope and grounds", "Basic",
  "Which of the following types of entities is covered by the Reserve Bank – Integrated Ombudsman Scheme, 2026?",
  ["Credit Information Companies", "Housing Finance Companies", "Core Investment Companies",
   "Stock brokers registered with SEBI"],
  concept="Regulated entities covered",
  explanation="RB-IOS, 2026 covers banks, eligible NBFCs, non-bank PPI issuers and Credit Information Companies, among "
              "others. Housing Finance Companies and Core Investment Companies are among the excluded NBFC "
              "categories; stock brokers fall under SEBI.",
  steps=["Covered: banks, eligible NBFCs, non-bank PPI issuers, CICs", "Excluded: HFCs, CICs (core investment), "
         "non-RBI entities"],
  why="HFCs and Core Investment Companies are excluded; SEBI-registered brokers are outside RBI's scheme.",
  facts=[fact("Regulated entities covered include Credit Information Companies; NBFCs excluding categories such as "
              "Housing Finance Companies and Core Investment Companies", RBIOS_FAQ)])
Q(T, "Scope and grounds", "Intermediate",
  "A customer has a grievance against a non-bank issuer of a prepaid payment instrument (wallet) that is regulated by "
  "RBI. Can she use RB-IOS, 2026?",
  ["Yes; non-bank Prepaid Payment Instrument issuers are covered by the scheme",
   "No; only banks are covered", "No; wallet complaints go only to NPCI",
   "Only if the wallet is linked to a bank account of the same issuer"],
  concept="Coverage of payment system participants",
  explanation="RB-IOS, 2026 covers non-bank PPI issuers along with banks, eligible NBFCs and CICs, so a deficiency in "
              "service by a wallet issuer can be taken to the RBI Ombudsman after the issuer's own grievance process.",
  steps=["Non-bank PPI issuers → covered"],
  why="The scheme is not limited to banks, and NPCI is not the forum for RBI-regulated PPI issuers.",
  facts=[fact("RB-IOS, 2026 covers non-bank Prepaid Payment Instrument Issuers", RBIOS_FAQ)])
Q(T, "Process and limits", "Advanced",
  "Consider the following statements about filing complaints under RB-IOS, 2026:\n"
  "I. Complaints on the CMS portal can be filed in Hindi and English.\n"
  "II. Complaints submitted by e-mail or in physical form may be filed in any language.\n"
  "III. A complaint can be filed only in the language of the State in which the bank branch is located.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II only", "I and III only", "I, II and III"],
  concept="Language of complaints",
  explanation="RBI's FAQs state that the CMS portal accepts complaints in Hindi and English, while complaints sent by "
              "e-mail or in physical mode may be in any language. There is no rule tying the complaint to the "
              "branch's State language.",
  steps=["I: correct", "II: correct", "III: wrong"],
  why="III is not a rule of the scheme; 'II only' omits I.",
  facts=[fact("The CMS portal accepts complaints in Hindi and English; complaints submitted through e-mail or physical "
              "mode may be filed in any language", RBIOS_FAQ)])
Q(T, "Scope and grounds", "Advanced",
  "A borrower has a dispute with a Credit Information Company (CIC) about his credit information. Under RB-IOS, 2026, "
  "which of the following is correct?",
  ["CICs are covered, but a grievance for which a remedy exists under Section 18 of the Credit Information Companies "
   "(Regulation) Act, 2005 is excluded from the scheme",
   "CICs are not covered by the scheme at all", "All grievances against CICs must go to the RBI Ombudsman, which "
   "overrides the CIC Act", "Only credit institutions, not CICs, can be complained against"],
  concept="CICs under RB-IOS",
  explanation="RB-IOS, 2026 covers CICs as regulated entities, but it excludes grievances where a remedy is available "
              "under Section 18 of the CIC (Regulation) Act, 2005, which provides its own mechanism.",
  steps=["CICs covered", "Exclusion: grievances with a remedy under Section 18 of CICRA, 2005"],
  why="CICs are covered; the scheme does not override the CIC Act's own remedy; complaints can be made against CICs.",
  facts=[fact("Credit Information Companies are covered; grievances where a remedy is available under Section 18 of "
              "the Credit Information Companies (Regulation) Act, 2005 are excluded", RBIOS_FAQ)])

# ================================================================= 17. Digital Banking (3 / 4 / 4)
T = "Digital Banking"
Q(T, "CBDC (e-rupee)", "Basic",
  "Since when has the retail digital rupee (e₹-R) been live in RBI's pilot, for users and merchants of participating "
  "banks and non-banks?",
  ["December 2022", "November 2022", "April 2024", "December 2020"],
  concept="Retail CBDC pilot",
  explanation="RBI's e₹ FAQs state that retail issuance and use of e₹ has been live since December 2022 for users and "
              "merchants of participating banks and non-banks. (The wholesale pilot began a month earlier, in November "
              "2022.)",
  steps=["Wholesale e₹: November 2022", "Retail e₹: December 2022"],
  why="November 2022 is the wholesale pilot; the other dates do not match.",
  facts=[fact("The retail e₹ is live with effect from December 2022 for users and merchants of participating banks and "
              "non-banks", ERUPEE_FAQ)])
Q(T, "Mobile and internet banking", "Basic",
  "According to RBI's chronology, RBI issued guidelines for internet banking, 'heralding in a new era in banking', in:",
  ["June 2001", "June 1995", "November 1999", "April 2003"],
  concept="Evolution of internet banking",
  explanation="RBI's chronology records the issue of internet banking guidelines in June 2001.",
  steps=["June 2001: internet banking guidelines"],
  why="June 1995 is the Banking Ombudsman office; November 1999 is the debit/smart card guidelines; April 2003 is "
      "risk-based supervision.",
  facts=[fact("June 2001: RBI issues guidelines for internet banking heralding in a new era in banking", CHRON_00)])
Q(T, "CBDC (e-rupee)", "Basic",
  "What happens to the e₹ in a user's wallet if the mobile phone on which the wallet is installed is lost?",
  ["The e₹ remains safe, and the wallet can be recovered on a new device using the same phone number/SIM",
   "The e₹ is lost permanently, like cash", "RBI refunds it only after a police report and six months",
   "It is automatically converted into a fixed deposit"],
  concept="Safety of e₹ wallets",
  explanation="RBI's FAQs state that e₹ in the wallet is safe even if the device is lost, and the wallet can be "
              "recovered on a new device using the same phone number/SIM.",
  steps=["Lost phone → e₹ safe", "Recover wallet with the same number/SIM on a new device"],
  why="The balance is not lost, there is no six-month refund process, and it is not converted into a deposit.",
  facts=[fact("The e₹ stored in the e₹ wallet is safe even if the mobile device is lost; the wallet can be recovered "
              "using the same phone number/SIM on a new mobile device", ERUPEE_FAQ)])
Q(T, "CBDC (e-rupee)", "Intermediate",
  "What does the offline feature of the retail e₹ enable, as described in RBI's FAQs?",
  ["Transactions in locations with limited or no internet connectivity", "Earning interest on wallet balances",
   "Cross-border payments without KYC", "Converting e₹ into foreign currency"],
  concept="Offline CBDC",
  explanation="RBI's FAQs say the offline feature enables users to transact in places with limited or no internet "
              "connectivity; different offline solutions are being explored.",
  steps=["Offline e₹ → transactions with little or no connectivity"],
  why="e₹ pays no interest; offline does not mean no-KYC cross-border use or currency conversion.",
  facts=[fact("The offline feature of e₹ enables the user to transact in locations with limited or no internet "
              "connectivity", ERUPEE_FAQ)])
Q(T, "Mobile and internet banking", "Intermediate",
  "Under RBI's circular of 6 July 2017 on limiting customer liability in unauthorised electronic banking "
  "transactions, a customer had zero liability for a fraud arising from a third-party breach (with no fault of the "
  "bank or the customer) if he notified the bank within:",
  ["Three working days of receiving the communication of the transaction", "Seven working days",
   "Ten working days", "Thirty days"],
  concept="Customer liability in electronic transactions",
  explanation="Under the 2017 circular, zero liability applied where the deficiency lay neither with the bank nor the "
              "customer but elsewhere in the system, and the customer notified the bank within three working days of "
              "receiving the communication from the bank.",
  steps=["Third-party breach + report within 3 working days → zero liability", "4–7 working days → limited liability"],
  why="Reporting in 4–7 working days attracts limited liability; 10 working days is the bank's deadline for shadow "
      "reversal; 30 days is not the threshold.",
  facts=[fact6("Circular of 6 July 2017: zero liability where the deficiency lies elsewhere in the system and the "
               "customer notifies the bank within three working days of receiving the communication", LIAB)])
Q(T, "Mobile and internet banking", "Intermediate",
  "Under RBI's circular of 6 July 2017 on limiting customer liability, within how many working days of a customer "
  "reporting an unauthorised electronic transaction did the bank have to credit (shadow reverse) the amount to the "
  "customer's account?",
  ["10 working days", "3 working days", "30 days", "90 days"],
  concept="Shadow reversal",
  explanation="On notification, the bank must credit the amount involved to the customer's account within 10 working "
              "days, value-dated to the date of the unauthorised transaction, without waiting for any insurance "
              "claim.",
  steps=["Credit within 10 working days of notification", "Value-dated to the transaction date"],
  why="3 working days is the customer's reporting window for zero liability; 90 days is the outer limit for "
      "resolving the complaint.",
  facts=[fact6("Circular of 6 July 2017: on being notified by the customer, the bank shall credit (shadow reversal) the "
               "amount involved within 10 working days, without waiting for settlement of insurance claim, "
               "value-dated to the date of the unauthorised transaction", LIAB)])
Q(T, "Mobile and internet banking", "Intermediate",
  "Under RBI's circular of 6 July 2017 on limiting customer liability, within what period did a bank have to "
  "resolve a customer's complaint about an unauthorised electronic transaction and establish his liability, if any?",
  ["Within the Board-approved timeline, not exceeding 90 days from receipt of the complaint", "Within 7 days",
   "Within 30 days, after which RBI decides", "There is no time limit"],
  concept="Resolution timeline",
  explanation="The complaint must be resolved and liability established within the time specified in the bank's "
              "Board-approved policy, not exceeding 90 days from the date of receipt. If it is not resolved in time, "
              "compensation is paid as prescribed.",
  steps=["Outer limit: 90 days from receipt of complaint"],
  why="7 and 30 days are not the prescribed limits, and a limit does exist.",
  facts=[fact6("Circular of 6 July 2017: complaint to be resolved and liability of the customer established within the "
               "time in the bank's Board approved policy, not exceeding 90 days from receipt of the complaint", LIAB)])

txn, cap_sb = 18_000, 10_000
assert min(txn, cap_sb) == 10_000
Q(T, "Mobile and internet banking", "Advanced",
  "An unauthorised UPI debit of ₹18,000 from Ravi's ordinary savings account resulted from a third-party breach, with "
  "no negligence by Ravi or the bank. He reports it on the fifth working day after receiving the bank's alert. Under "
  "RBI's circular of 6 July 2017 on limiting customer liability, what was his maximum liability?",
  ["₹10,000", "₹18,000", "Nil", "₹5,000"],
  concept="Limited liability",
  explanation="Reporting within four to seven working days gives limited liability: the lower of the transaction "
              "value and the cap in RBI's table. For savings accounts (other than BSBD) the cap is ₹10,000, so his "
              "liability is min(18,000, 10,000) = ₹10,000.",
  steps=["Reported on day 5 → limited liability band", "Savings account cap = ₹10,000",
         "Liability = min(18,000, 10,000) = 10,000"],
  why="Nil applies only if reported within three working days; ₹5,000 is the BSBD cap; ₹18,000 ignores the cap.",
  computed=True,
  facts=[fact6("Circular of 6 July 2017: reported within four to seven working days, liability is the transaction value "
               "or the amount in Table 1, whichever is lower; Table 1: BSBD accounts ₹5,000; all other savings "
               "accounts ₹10,000; other current/cash credit/overdraft accounts and credit cards with limits above ₹5 "
               "lakh ₹25,000", LIAB)])

cases = {"P": min(7_000, 5_000), "Q": min(40_000, 25_000), "R": 0}
assert sum(cases.values()) == 30_000
Q(T, "Mobile and internet banking", "Advanced",
  "Three customers suffer unauthorised electronic transactions through third-party breaches (no fault of bank or "
  "customer):\n"
  "P. ₹7,000 from a BSBD account, reported on the 6th working day\n"
  "Q. ₹40,000 on a credit card with a ₹6 lakh limit, reported on the 4th working day\n"
  "R. ₹8,000 from a savings account, reported on the 2nd working day\n"
  "Under RBI's circular of 6 July 2017 on limiting customer liability, what was the total maximum liability of the "
  "three customers?",
  ["₹30,000", "₹55,000", "₹25,000", "₹38,000"],
  concept="Liability matrix",
  explanation="P (BSBD, day 6) → min(7,000, 5,000) = 5,000. Q (credit card limit above ₹5 lakh, day 4) → min(40,000, "
              "25,000) = 25,000. R (day 2) → zero liability. Total = ₹30,000.",
  steps=["P: 5,000", "Q: 25,000", "R: 0", "Total = 30,000"],
  why="₹55,000 ignores the caps for P and Q; ₹25,000 drops P; ₹38,000 charges R in full and P at its cap.",
  computed=True,
  facts=[fact6("Circular of 6 July 2017: zero liability if notified within three working days; for four to seven working "
               "days, liability is the lower of the transaction value and Table 1: BSBD ₹5,000; credit cards with "
               "limit above ₹5 lakh ₹25,000", LIAB)])
Q(T, "Mobile and internet banking", "Advanced",
  "Consider the following statements about RBI's Digital Banking Units (DBUs) framework of 7 April 2022:\n"
  "I. DBUs may be opened by domestic scheduled commercial banks other than RRBs, payments banks and local area banks.\n"
  "II. DBUs are treated as banking outlets.\n"
  "III. Cash deposits and withdrawals at a DBU are handled at teller counters by bank staff.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Digital Banking Units",
  explanation="The DBU circular applies to domestic scheduled commercial banks excluding RRBs, payments banks and "
              "LABs, and DBUs are treated as banking outlets. Cash services at DBUs are only through ATMs and cash "
              "deposit machines, with no counter cash handling, so III is wrong.",
  steps=["I: correct", "II: correct", "III: wrong (only ATMs/CDMs)"],
  why="III contradicts the circular; 'I only' omits II.",
  facts=[fact("DBUs: domestic scheduled commercial banks excluding RRBs, Payments Banks and Local Area Banks; DBUs "
              "treated as Banking Outlets; cash withdrawal and deposit only through ATMs and cash deposit machines",
              DBU)])
Q(T, "Mobile and internet banking", "Advanced",
  "Consider the following statements about customer liability as laid down in RBI's circular of 6 July 2017 on "
  "unauthorised electronic banking transactions:\n"
  "I. If the loss was due to contributory fraud, negligence or deficiency on the part of the bank, the customer had "
  "zero liability even if he had not reported the transaction.\n"
  "II. A credit card customer was not to bear any additional interest burden while the complaint was being "
  "resolved.\n"
  "III. Banks could not waive any customer liability, even where the customer was negligent.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Liability rules",
  explanation="Contributory fraud, negligence or deficiency by the bank gives zero liability irrespective of whether "
              "the customer reported it (I). Debit card/account customers must not lose interest and credit card "
              "customers must not bear additional interest (II). Banks may, at their discretion, waive customer "
              "liability even in cases of customer negligence, so III is wrong.",
  steps=["I: correct", "II: correct", "III: wrong (banks may waive)"],
  why="III contradicts the circular; 'I only' omits II.",
  facts=[fact6("Circular of 6 July 2017: zero liability for contributory fraud/negligence/deficiency on the part of the "
               "bank irrespective of whether the transaction is reported; credit card customers shall not bear any "
               "additional burden of interest; banks may waive customer liability even in case of customer "
               "negligence", LIAB)])

# ================================================================= 18. UPI (1 / 3 / 3)
T = "UPI"
Q(T, "Features", "Basic",
  "In December 2021, the UPI transaction limit for payments under the RBI Retail Direct Scheme and for IPO "
  "subscriptions was raised to:",
  ["₹5 lakh", "₹2 lakh", "₹1 lakh", "₹10 lakh"],
  concept="Higher UPI limits for specific uses",
  explanation="RBI's December 2023 statement recalls that in December 2021 the UPI limit for Retail Direct Scheme and "
              "IPO subscriptions was increased to ₹5 lakh, while the general UPI cap is ₹1 lakh.",
  steps=["General UPI cap: ₹1 lakh", "Retail Direct and IPOs (Dec 2021): ₹5 lakh"],
  why="₹1 lakh is the general cap; ₹2 lakh applied to some other categories; ₹10 lakh was not the limit.",
  facts=[fact("In December 2021, the limit for Retail Direct Scheme and for IPO subscriptions was increased to ₹5 "
              "lakh; the transaction limit for UPI is capped at ₹1 lakh", SDRP_DEC23)])
Q(T, "Features", "Intermediate",
  "In December 2023, RBI proposed raising the UPI transaction limit for payments to hospitals and educational "
  "institutions:",
  ["From ₹1 lakh to ₹5 lakh per transaction", "From ₹2 lakh to ₹10 lakh per transaction",
   "From ₹1 lakh to ₹2 lakh per transaction", "From ₹50,000 to ₹1 lakh per transaction"],
  concept="UPI limits for health and education",
  explanation="RBI's Statement on Developmental and Regulatory Policies of 20 December 2023 proposed enhancing the UPI "
              "limit for payments to hospitals and educational institutions from ₹1 lakh to ₹5 lakh per transaction "
              "to encourage UPI use for such payments.",
  steps=["Hospitals and educational institutions: ₹1 lakh → ₹5 lakh"],
  why="The other ranges do not match the proposal.",
  facts=[fact("It is proposed to enhance the limit for payments to hospitals and educational institutions from ₹1 lakh "
              "to ₹5 lakh per transaction (December 20, 2023)", SDRP_DEC23)])
Q(T, "Features", "Intermediate",
  "As noted in RBI's December 2023 statement, up to what amount can recurring e-mandate payments (for example via "
  "UPI AutoPay) generally be processed without an Additional Factor of Authentication (AFA)?",
  ["₹15,000", "₹5,000", "₹1 lakh", "₹2 lakh"],
  concept="E-mandates for recurring payments",
  explanation="Under the e-mandate framework, recurring transactions up to ₹15,000 do not need AFA. In December 2023 "
              "RBI proposed exempting AFA up to ₹1 lakh only for mutual fund subscriptions, insurance premiums and "
              "credit card bill payments.",
  steps=["General AFA-free limit: ₹15,000", "Special categories (proposed Dec 2023): up to ₹1 lakh"],
  why="₹1 lakh applies only to the three special categories; ₹5,000 and ₹2 lakh are not the limit.",
  facts=[fact("The current limit for e-mandates without Additional Factor of Authentication is ₹15,000; proposed to "
              "exempt AFA for transactions up to ₹1 lakh for subscription to mutual funds, payment of insurance "
              "premium and payment of credit card bills", SDRP_DEC23)])
Q(T, "Features", "Intermediate",
  "According to RBI's booklet on payment systems, UPI 2.0 was launched in which year?",
  ["2018", "2016", "2020", "2022"],
  concept="Evolution of UPI",
  explanation="RBI's payments booklet records that UPI went live in 2016 and UPI 2.0 followed in 2018.",
  steps=["UPI: 2016", "UPI 2.0: 2018"],
  why="2016 is UPI's original launch; 2020 and 2022 are not the UPI 2.0 year.",
  facts=[fact("UPI 2.0 was launched in 2018", PAY_BOOKLET)])

mandates = {"P": (40_000, "mf"), "Q": (14_000, "utility"), "R": (25_000, "ott"), "S": (90_000, "card")}
special = {"mf", "insurance", "card"}
need_afa = sorted(k for k, (amt, cat) in mandates.items() if amt > (100_000 if cat in special else 15_000))
assert need_afa == ["R"]
Q(T, "Features", "Advanced",
  "Assume the December 2023 proposal on e-mandates was implemented. Which of these recurring UPI AutoPay debits would "
  "still need an Additional Factor of Authentication?\n"
  "P. ₹40,000 monthly mutual fund SIP\n"
  "Q. ₹14,000 monthly electricity bill\n"
  "R. ₹25,000 monthly subscription to a streaming and gaming service\n"
  "S. ₹90,000 credit card bill payment",
  ["R only", "P, R and S", "P and R only", "None of them"],
  concept="AFA thresholds for e-mandates",
  explanation="The general AFA-free limit is ₹15,000. For mutual fund subscriptions, insurance premiums and credit card "
              "bills the AFA-free limit becomes ₹1 lakh. P (₹40,000 MF) and S (₹90,000 card bill) are below ₹1 lakh; "
              "Q (₹14,000) is below ₹15,000; R (₹25,000, ordinary category) exceeds ₹15,000 and needs AFA.",
  steps=["P: MF, 40,000 ≤ 1 lakh → no AFA", "Q: 14,000 ≤ 15,000 → no AFA", "R: 25,000 > 15,000 → AFA",
         "S: card bill, 90,000 ≤ 1 lakh → no AFA"],
  why="P and S fall within the ₹1 lakh special limit; R does not fall in a special category.",
  computed=True,
  facts=[fact("Limit for e-mandates without AFA is ₹15,000; proposal to exempt AFA for transactions up to ₹1 lakh for "
              "mutual fund subscriptions, insurance premium and credit card bill payments", SDRP_DEC23)])
Q(T, "Features", "Advanced",
  "Consider the following statements about RBI's Statement on Developmental and Regulatory Policies of 20 December "
  "2023:\n"
  "I. It proposed a ₹5 lakh UPI limit per transaction for payments to hospitals and educational institutions.\n"
  "II. It proposed a Fintech Repository, to be operationalised by the Reserve Bank Innovation Hub.\n"
  "III. It proposed exempting AFA for e-mandates up to ₹1 lakh for all merchant categories.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="December 2023 payments measures",
  explanation="The statement proposed raising the UPI limit for hospitals and educational institutions to ₹5 lakh "
              "(I) and a Fintech Repository to be operationalised by RBIH (II). The ₹1 lakh AFA exemption was only for "
              "mutual funds, insurance premiums and credit card bills, not all categories (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (only three categories)"],
  why="III overstates the AFA exemption; 'I only' omits II.",
  facts=[fact("Proposals of December 20, 2023: UPI limit for hospitals and educational institutions to ₹5 lakh; AFA "
              "exemption up to ₹1 lakh for mutual funds, insurance premium and credit card bills; Fintech Repository "
              "to be operationalised by the Reserve Bank Innovation Hub", SDRP_DEC23)])

dig_vol, dig_val = 99.8, 97.8
assert round(100 - dig_vol, 1) == 0.2 and round(100 - dig_val, 1) == 2.2
Q(T, "Features", "Advanced",
  "RBI's Payment System Report (released 18 May 2026) says digital modes, led by UPI, made up 99.8% of the volume and "
  "97.8% of the value of payment transactions in CY 2025. What does this imply for the remaining (paper-based) "
  "transactions?",
  ["About 0.2% of volume but about 2.2% of value, so their average size is far larger than digital payments",
   "About 2.2% of volume and 0.2% of value", "About 0.2% of both volume and value",
   "About 22% of value, mostly cheques"],
  concept="Digital and paper payments",
  explanation="Non-digital share = 100 − 99.8 = 0.2% of volume and 100 − 97.8 = 2.2% of value. Because their value "
              "share is about 11 times their volume share, paper instruments such as cheques are, on average, much "
              "larger transactions.",
  steps=["Volume: 100 − 99.8 = 0.2%", "Value: 100 − 97.8 = 2.2%", "2.2 ÷ 0.2 = 11 → larger average size"],
  why="The volume and value shares are swapped in one option; the value share is 2.2%, not 0.2% or 22%.",
  computed=True, current=ca(PSR_DATE),
  facts=[fact("Digital payments accounted for 99.8 per cent of volume and 97.8 per cent of value of payment "
              "transactions in CY 2025", PSR),
         fact("RBI released the half-yearly Payment System Report on May 18, 2026", PSR_PR)])

# ================================================================= 19. NEFT (2 / 2 / 1)
T = "NEFT"
SUB = "Settlement and timings"
Q(T, SUB, "Basic",
  "Can the beneficiary's bank levy a charge for crediting an inward NEFT transaction to the beneficiary's account?",
  ["No; no charges are to be levied for inward NEFT transactions at destination bank branches",
   "Yes, up to ₹2.50 per transaction", "Yes, only for amounts above ₹2 lakh", "Yes, if the credit is on a holiday"],
  concept="NEFT charges",
  explanation="RBI's NEFT FAQs state that no charges are to be levied for inward transactions at destination bank "
              "branches for credit to beneficiary accounts.",
  steps=["Inward NEFT → free for the beneficiary"],
  why="There is no inward charge of any amount, on any day.",
  facts=[fact("No charges to be levied for inward transactions at destination bank branches for credit to "
              "beneficiary accounts", NEFT_FAQ)])
Q(T, SUB, "Basic",
  "After an NEFT credit to the beneficiary's account, how does the remitter come to know of it, according to RBI?",
  ["Positive confirmation to the remitter by SMS/e-mail on credit to the beneficiary account",
   "Only from the beneficiary's monthly statement", "By a letter from RBI", "There is no confirmation in NEFT"],
  concept="Features of NEFT",
  explanation="Among the benefits of NEFT, RBI lists positive confirmation to the remitter by SMS/e-mail when the "
              "beneficiary's account is credited.",
  steps=["NEFT credit → positive confirmation by SMS/e-mail to remitter"],
  why="NEFT does provide confirmation, through the banks, not by RBI letters or statements.",
  facts=[fact("Positive confirmation to the remitter by SMS / e-mail on credit to beneficiary account", NEFT_FAQ)])
Q(T, SUB, "Intermediate",
  "According to RBI's Payment System Report (released 18 May 2026), roughly how many NEFT transactions were processed "
  "in CY 2025, and of what value?",
  ["About 1,000 crore transactions worth ₹482 lakh crore", "About 518 crore transactions worth ₹75 lakh crore",
   "About 33 crore transactions worth ₹2,206 lakh crore", "About 742 crore transactions worth ₹51 lakh crore"],
  concept="Scale of NEFT",
  explanation="RBI's report puts NEFT at about 1,000 crore transactions worth ₹482 lakh crore in CY 2025. 518 crore/₹75 "
              "lakh crore is IMPS, 33 crore/₹2,206 lakh crore is RTGS and 742 crore/₹51 lakh crore is NACH.",
  steps=["NEFT CY 2025: ~1,000 crore txns, ₹482 lakh crore"],
  why="The other pairs belong to IMPS, RTGS and NACH.",
  current=ca(PSR_DATE),
  facts=[fact("NEFT: about 1,000 crore transactions worth ₹482 lakh crore in CY 2025; IMPS 518 crore worth ₹75 lakh "
              "crore; RTGS about 33 crore worth ₹2,206 lakh crore; NACH 742 crore worth ₹51 lakh crore", PSR),
         fact("Payment System Report released on May 18, 2026", PSR_PR)])
Q(T, SUB, "Intermediate",
  "What compound annual growth rates did NEFT record between CY 2021 and CY 2025, according to RBI's Payment System "
  "Report?",
  ["27.4% in volume and 14.9% in value", "55.8% in volume and 43% in value", "14.9% in volume and 27.4% in value",
   "10% in both volume and value"],
  concept="Growth of NEFT",
  explanation="RBI reports NEFT's CAGR for 2021–2025 at 27.4% in volume and 14.9% in value. (55.8% and 43% are UPI's "
              "growth rates.)",
  steps=["NEFT CAGR 2021–25: volume 27.4%, value 14.9%"],
  why="55.8%/43% is UPI; the third option swaps volume and value.",
  current=ca(PSR_DATE),
  facts=[fact("NEFT CAGR 2021-2025: 27.4% in volume and 14.9% in value", PSR)])
Q(T, SUB, "Advanced",
  "Consider the following statements based on RBI's NEFT FAQs:\n"
  "I. NEFT can be used for inward foreign exchange remittances into India.\n"
  "II. NEFT can be used to pay credit card dues to the card-issuing bank.\n"
  "III. Customers can track an NEFT transaction only by writing to RBI's NEFT Processing Centre.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II only", "I and III only", "I, II and III"],
  concept="Uses and tracking of NEFT",
  explanation="RBI lists inward foreign exchange remittances and payment of credit card dues among NEFT's uses (I, II). "
              "Tracking is done through the NEFT Customer Facilitation Centre of one's own bank, quoting the UTR "
              "number, not by writing to RBI (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (bank's CFC, with UTR)"],
  why="III misstates the tracking channel; 'II only' omits I.",
  facts=[fact("NEFT can be used for payment of credit card dues to the card issuing banks and inward foreign exchange "
              "remittances; status can be tracked by contacting the NEFT Customer Facilitation Centre (CFC) of the "
              "bank with the UTR number", NEFT_FAQ)])

# ================================================================= 20. RTGS (1 / 1 / 1)
T = "RTGS"
SUB = "Limits and timings"
Q(T, SUB, "Basic",
  "Is there a maximum amount that can be sent through RTGS, according to RBI?",
  ["No; RBI has prescribed no upper ceiling", "Yes, ₹10 crore per transaction", "Yes, ₹2 lakh per transaction",
   "Yes, ₹5 lakh per transaction"],
  concept="RTGS limits",
  explanation="RTGS is meant for large-value transactions: the minimum is ₹2 lakh, and RBI prescribes no maximum.",
  steps=["Minimum ₹2 lakh", "Maximum: none"],
  why="₹2 lakh is the minimum, not a maximum; ₹5 lakh is the IMPS limit; ₹10 crore is not a ceiling.",
  facts=[fact("RTGS: minimum amount ₹2,00,000; there is no upper or maximum ceiling", RTGS_FAQ)])
Q(T, SUB, "Intermediate",
  "From which date did RBI waive the processing charges it levied on banks for RTGS transactions, so that banks could "
  "pass on the benefit to customers?",
  ["1 July 2019", "14 December 2020", "16 December 2019", "1 April 2016"],
  concept="RTGS charges",
  explanation="RBI waived its processing charges on RTGS from 1 July 2019. Inward RTGS is free; banks may charge at "
              "most ₹25 (₹2–5 lakh) or ₹50 (above ₹5 lakh) plus tax on outward transactions.",
  steps=["RBI processing charges on RTGS waived: 1 July 2019"],
  why="14 December 2020 is when RTGS became 24x7; 16 December 2019 is when NEFT became 24x7.",
  facts=[fact("RBI has waived the processing charges levied on banks for RTGS transactions with effect from July 1, "
              "2019", RTGS_FAQ)])

rtgs_val, neft_val, rtgs_vol, neft_vol = 2206, 482, 33, 1000
assert round(rtgs_val / neft_val, 1) == 4.6 and round(neft_vol / rtgs_vol) == 30
Q(T, SUB, "Advanced",
  "In CY 2025, RTGS handled about 33 crore transactions worth ₹2,206 lakh crore, while NEFT handled about 1,000 crore "
  "transactions worth ₹482 lakh crore. Which statement is correct?",
  ["RTGS carried about 4.6 times NEFT's value with about one-thirtieth of its volume",
   "NEFT carried about 4.6 times RTGS's value", "RTGS carried about 30 times NEFT's value with similar volume",
   "Both systems carried roughly equal value"],
  concept="Large-value versus retail payment systems",
  explanation="Value ratio = 2,206 ÷ 482 ≈ 4.6. Volume ratio = 1,000 ÷ 33 ≈ 30, so RTGS handles roughly one-thirtieth "
              "of NEFT's volume — consistent with RTGS being a large-value gross settlement system.",
  steps=["2,206 ÷ 482 ≈ 4.6", "1,000 ÷ 33 ≈ 30"],
  why="The other options invert or misstate the ratios.",
  computed=True, current=ca(PSR_DATE),
  facts=[fact("RTGS about 33 crore transactions worth ₹2,206 lakh crore and NEFT about 1,000 crore transactions worth "
              "₹482 lakh crore in CY 2025", PSR)])

# ================================================================= 21. IMPS (1 / 1 / 1)
T = "IMPS"
SUB = "Limits and features"
Q(T, SUB, "Basic",
  "For person-to-person IMPS transfers using the beneficiary's mobile number, the beneficiary's bank issues a Mobile "
  "Money Identifier (MMID). How many digits does an MMID have?",
  ["7", "4", "11", "16"],
  concept="MMID in IMPS",
  explanation="NPCI describes the MMID as a 7-digit number issued by the bank on registering a mobile number for IMPS; "
              "a sender needs the beneficiary's mobile number and MMID.",
  steps=["MMID = 7 digits, linked to the mobile number"],
  why="11 characters is the IFSC; 16 digits is a typical card number; 4 is not the MMID length.",
  facts=[fact("MMID is a 7-digit number issued by banks for IMPS; each MMID is linked with a unique mobile number",
              UPI_2016)])
Q(T, SUB, "Intermediate",
  "Under NPCI's 'simplified IMPS' from 1 February 2024, what does a sender need in order to transfer funds without "
  "first adding the beneficiary with account number and IFSC?",
  ["The beneficiary's mobile number and bank name, with real-time name validation",
   "Only the beneficiary's Aadhaar number", "The beneficiary's UPI PIN", "The beneficiary's card number and CVV"],
  concept="Mobile number and bank name based IMPS",
  explanation="NPCI enabled IMPS transfers using the recipient's mobile number and bank name, carried on the existing "
              "P2P route with the default MMID and accompanied by real-time beneficiary name validation; banks were "
              "to comply by 31 January 2024.",
  steps=["Inputs: mobile number + bank name", "Uses default MMID on the P2P route", "Name validated in real time"],
  why="Aadhaar is used by AePS/APBS; a UPI PIN or card details are never shared with a sender.",
  facts=[fact("From February 1, 2024 IMPS transfers can be made using only the recipient's mobile number and bank "
              "name, without account number or IFSC, with real-time beneficiary name validation; carried on the P2P "
              "route using mobile number + default MMID", IMPS_SIMPLE)])
Q(T, SUB, "Advanced",
  "Consider the following statements about IMPS:\n"
  "I. According to RBI's payments booklet, IMPS can be accessed through Business Correspondents in addition to "
  "mobile, ATMs, internet banking and branches.\n"
  "II. Mobile-number-and-bank-name based IMPS transfers use the beneficiary's default MMID on the existing P2P route.\n"
  "III. IMPS transactions are settled between banks one by one in real time in RBI's books.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II only", "I and III only", "I, II and III"],
  concept="IMPS channels and settlement",
  explanation="RBI's booklet lists mobile, ATM, internet banking, branches and BCs as IMPS channels (I). Simplified "
              "IMPS uses the mobile number with the default MMID on the P2P route (II). IMPS gives real-time credit to "
              "customers, but inter-bank settlement is deferred net, not gross in real time (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (deferred net settlement)"],
  why="III describes RTGS, not IMPS; 'II only' omits I.",
  facts=[fact("IMPS is available through mobile, ATM, internet banking, bank branches and Business Correspondents, with "
              "deferred net settlement between banks", PAY_BOOKLET),
         fact("Mobile Number + Bank Name based transactions carried out on existing P2P railroad using Mobile Number + "
              "default MMID combination", IMPS_SIMPLE)])

# ================================================================= 22. NPCI (1 / 5 / 2)
T = "NPCI"
SUB = "Products: NACH, AePS, RuPay, FASTag"
Q(T, SUB, "Basic",
  "Bharat QR, a common interoperable QR code standard for card and other payments, was developed jointly by:",
  ["NPCI, Mastercard and Visa", "RBI and SEBI", "NPCI and IDRBT only", "SBI and IBA"],
  concept="Interoperable QR",
  explanation="RBI's payments booklet notes that Bharat QR was formulated collectively by Mastercard, NPCI and Visa as "
              "a common interoperable standard.",
  steps=["Bharat QR = NPCI + Mastercard + Visa"],
  why="RBI, SEBI, IDRBT, SBI and IBA did not jointly develop the standard.",
  facts=[fact("Bharat QR was formulated collectively by Mastercard, NPCI and Visa as a common interoperable standard",
              PAY_BOOKLET)])
Q(T, SUB, "Intermediate",
  "Which of the following is NOT a service offered through the Aadhaar Enabled Payment System (AePS)?",
  ["Issue of a demand draft", "Cash withdrawal", "Balance enquiry", "Aadhaar to Aadhaar fund transfer"],
  concept="AePS services",
  explanation="AePS offers cash withdrawal, cash deposit, balance enquiry and Aadhaar-to-Aadhaar fund transfer as "
              "financial services, plus non-financial services such as demographic authentication, Best Finger "
              "Detection and e-KYC.",
  steps=["Financial: withdrawal, deposit, balance enquiry, Aadhaar-to-Aadhaar transfer", "Demand drafts → not AePS"],
  why="The other three are listed AePS services.",
  facts=[fact("AePS services: cash withdrawal, cash deposit, balance enquiry, Aadhaar to Aadhaar fund transfer; "
              "non-financial: demographic authentication, Best Finger Detection, e-KYC", PAY_BOOKLET)])
Q(T, SUB, "Intermediate",
  "In an AePS transaction, which institution performs the biometric authentication of the customer?",
  ["UIDAI, while NPCI provides switching, clearing and settlement", "NPCI", "The customer's bank",
   "The Business Correspondent"],
  concept="Roles in AePS",
  explanation="In AePS, UIDAI performs the biometric authentication; NPCI handles the switching, clearing and "
              "settlement. AePS has been operational since January 2011.",
  steps=["Authentication → UIDAI", "Switching, clearing, settlement → NPCI"],
  why="NPCI switches and settles but does not authenticate; banks and BCs capture but do not authenticate biometrics.",
  facts=[fact("AePS operational since January 2011; biometric authentication by UIDAI, switching, clearing and "
              "settlement by NPCI", PAY_BOOKLET)])
Q(T, SUB, "Intermediate",
  "According to RBI's Payment System Report (released 18 May 2026), how many transactions did NACH process in "
  "CY 2025, and of what value?",
  ["742 crore transactions worth ₹51 lakh crore", "305 crore transactions worth ₹14.8 lakh crore",
   "518 crore transactions worth ₹75 lakh crore", "57.2 crore transactions worth ₹70.82 lakh crore"],
  concept="Scale of NACH",
  explanation="NACH, NPCI's bulk payment system, processed 742 crore transactions worth ₹51 lakh crore in CY 2025. "
              "305 crore/₹14.8 lakh crore is BBPS, 518 crore/₹75 lakh crore is IMPS and 57.2 crore/₹70.82 lakh crore "
              "is CTS.",
  steps=["NACH CY 2025: 742 crore txns, ₹51 lakh crore"],
  why="The other pairs are BBPS, IMPS and CTS.",
  current=ca(PSR_DATE),
  facts=[fact("NACH: 742 crore transactions worth ₹51 lakh crore in CY 2025; BBPS 305 crore worth ₹14.8 lakh crore; "
              "CTS 57.2 crore worth ₹70.82 lakh crore", PSR)])
Q(T, SUB, "Intermediate",
  "According to RBI's Payment System Report, how many FASTags had been issued by December 2025?",
  ["11.87 crore", "1.18 crore", "103.43 crore", "60.36 crore"],
  concept="FASTag adoption",
  explanation="RBI's report records FASTag issuance of 11.87 crore by December 2025. (103.43 crore is the number of "
              "debit cards; 60.36 crore is RuPay cards issued by November 2020.)",
  steps=["FASTags issued by December 2025: 11.87 crore"],
  why="103.43 crore is debit cards; 60.36 crore is RuPay cards (2020); 1.18 crore misplaces the decimal.",
  current=ca(PSR_DATE),
  facts=[fact("FASTag issuance reached 11.87 crore by December 2025; 103.43 crore debit cards", PSR)])
Q(T, SUB, "Intermediate",
  "A common USSD platform for mobile banking on basic phones (later the *99# service) was set up through NPCI in:",
  ["2013", "2008", "2016", "2010"],
  concept="USSD-based banking",
  explanation="RBI's booklet notes that a common USSD platform was set up through NPCI in 2013; USSD 2.0 was launched "
              "with BHIM in December 2016 and USSD has since been merged into UPI.",
  steps=["2013: common USSD platform via NPCI", "Dec 2016: USSD 2.0 with BHIM"],
  why="2008 is NPCI's incorporation; 2016 is USSD 2.0; 2010 is IMPS.",
  facts=[fact("A common USSD platform was set up through NPCI in 2013; USSD 2.0 went live with BHIM on December 30, "
              "2016", PAY_BOOKLET)])

atm09, atm20, mem09, mem20 = 50_000, 230_000, 37, 112
assert round(atm20 / atm09, 1) == 4.6 and round(mem20 / mem09, 1) == 3.0
Q(T, SUB, "Advanced",
  "When NPCI took over the National Financial Switch (NFS) from IDRBT in December 2009, it had 37 members and 50,000 "
  "ATMs. By end-December 2020 it connected 112 member banks and over 2.3 lakh ATMs. Which statement is correct?",
  ["ATMs on the switch grew about 4.6 times and members about 3 times",
   "ATMs grew about 3 times and members about 4.6 times", "Both roughly doubled",
   "ATMs grew about 46 times"],
  concept="Growth of the NFS ATM network",
  explanation="2,30,000 ÷ 50,000 = 4.6 and 112 ÷ 37 ≈ 3.0. ATMs grew faster than membership.",
  steps=["ATMs: 2.3 lakh ÷ 50,000 = 4.6", "Members: 112 ÷ 37 ≈ 3.0"],
  why="The ratios are swapped in one option; neither merely doubled; 46 misplaces the decimal.",
  computed=True,
  facts=[fact("NPCI took over NFS from IDRBT in December 2009, when it had 37 members and 50,000 ATMs; as of "
              "end-December 2020 it connected 112 member banks and over 2.3 lakh ATMs", PAY_BOOKLET)])
Q(T, SUB, "Advanced",
  "Consider the following statements about QR codes in Indian payments, as described in RBI's payments booklet:\n"
  "I. As of 30 November 2020, 30.46 lakh Bharat QR codes had been deployed.\n"
  "II. Under RBI's October 2020 instructions, only Bharat QR and UPI QR would continue, and proprietary QR codes had "
  "to shift to interoperable ones by 31 March 2022.\n"
  "III. Bharat QR was developed by NPCI alone.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Interoperable QR codes",
  explanation="The booklet records 30.46 lakh Bharat QR codes by 30 November 2020 (I) and RBI's October 2020 decision "
              "that only Bharat QR and UPI QR would continue, with proprietary QRs moving to interoperable codes by 31 "
              "March 2022 (II). Bharat QR was developed jointly by Mastercard, NPCI and Visa (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (jointly with Mastercard and Visa)"],
  why="III is false; 'I only' omits II.",
  facts=[fact("As of November 30, 2020, 30.46 lakh Bharat QR codes deployed; October 2020 RBI instructions: only "
              "Bharat QR and UPI QR to continue, proprietary QR codes to shift by March 31, 2022; Bharat QR formulated "
              "by Mastercard, NPCI and Visa", PAY_BOOKLET)])

# ================================================================= 23. Payment Banks (1 / 1 / 1)
T = "Payment Banks"
Q(T, "Permitted activities", "Basic",
  "On 19 August 2015, RBI granted 'in-principle' approval to how many applicants to set up payments banks?",
  ["11", "10", "41", "6"],
  concept="Licensing of payments banks",
  explanation="RBI received 41 applications under the payments bank guidelines of 27 November 2014 and gave "
              "in-principle approval to 11 applicants on 19 August 2015. (Ten small finance bank approvals followed in "
              "September 2015.)",
  steps=["Applications: 41", "In-principle approvals: 11"],
  why="41 is the number of applications; 10 is the SFB approvals; 6 is not the figure.",
  facts=[fact("RBI grants in-principle approval to 11 applicants for payments banks; 41 applications received",
              PB_2015)])
Q(T, "Permitted activities", "Intermediate",
  "Which of the following was among the 11 applicants that received in-principle approval for payments banks in "
  "August 2015?",
  ["Department of Posts", "Life Insurance Corporation of India", "Bajaj Finance Limited", "Muthoot Finance Limited"],
  concept="Payments bank applicants",
  explanation="The 11 were Aditya Birla Nuvo, Airtel M Commerce Services, Cholamandalam Distribution Services, the "
              "Department of Posts, Fino PayTech, NSDL, Reliance Industries, Dilip Shanghvi, Vijay Shekhar Sharma, "
              "Tech Mahindra and Vodafone m-pesa.",
  steps=["Department of Posts → approved (later India Post Payments Bank)"],
  why="LIC, Bajaj Finance and Muthoot Finance were not on the list.",
  facts=[fact("Approved applicants included Aditya Birla Nuvo, Airtel M Commerce Services, Cholamandalam Distribution "
              "Services, Department of Posts, Fino PayTech, NSDL, Reliance Industries, Dilip Shanghvi, Vijay Shekhar "
              "Sharma, Tech Mahindra and Vodafone m-pesa", PB_2015)])
Q(T, "Permitted activities", "Advanced",
  "Consider the following statements about RBI's in-principle approvals for payments banks of 19 August 2015:\n"
  "I. Applications were screened by an External Advisory Committee chaired by Dr. Nachiket Mor.\n"
  "II. The in-principle approval was valid for 18 months, during which the applicants had to comply with the "
  "requirements.\n"
  "III. The applicants could begin banking business immediately on receiving in-principle approval.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="In-principle approval",
  explanation="The External Advisory Committee chaired by Dr. Nachiket Mor screened the applications (I). The "
              "in-principle approval was valid for 18 months (II), and applicants could not undertake any banking "
              "business until they received a regular licence (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong"],
  why="III contradicts the press release; 'I only' omits II.",
  facts=[fact("External Advisory Committee chaired by Dr. Nachiket Mor; in-principle approval valid for 18 months; "
              "applicants cannot undertake any banking business until a regular licence is granted", PB_2015)])

# ================================================================= 24. Small Finance Banks (1 / 2 / 1)
T = "Small Finance Banks"
Q(T, "Licensing norms", "Basic",
  "In September 2015, RBI granted in-principle approval to how many applicants to set up small finance banks?",
  ["10", "11", "25", "6"],
  concept="Licensing of SFBs",
  explanation="RBI's SFB compendium records in-principle approvals to ten applicants by press release dated 16 "
              "September 2015 (a month after 11 payments bank approvals).",
  steps=["SFB approvals (Sept 2015): 10"],
  why="11 is the payments bank approvals; 25 and 6 do not match.",
  facts=[fact("In-principle approvals were given to ten applicants to set up SFBs vide press release dated September "
              "16, 2015", SFB_COMP)])
Q(T, "Licensing norms", "Intermediate",
  "Under the criteria in RBI's circular of 26 April 2024 on voluntary transition of a small finance bank into a "
  "universal bank, which of the following was required?",
  ["Net worth of at least ₹1,000 crore, listed shares, and GNPA ≤ 3% and NNPA ≤ 1% in the last two financial years",
   "Net worth of at least ₹300 crore and three years of operations",
   "Net worth of at least ₹500 crore, with no listing requirement", "Net worth of at least ₹1,000 crore and a "
   "mandatory identified promoter holding 40%"],
  concept="SFB to universal bank",
  explanation="An eligible SFB must have scheduled status and a satisfactory five-year track record, listed shares, "
              "minimum net worth of ₹1,000 crore (previous quarter, audited), compliance with SFB CRAR norms, net "
              "profit in the last two years, and GNPA/NNPA of at most 3%/1% in the last two years.",
  steps=["5-year track record, scheduled", "Listed", "Net worth ≥ ₹1,000 crore", "Profit in last 2 years",
         "GNPA ≤ 3%, NNPA ≤ 1%"],
  why="₹300 crore is the SFB entry capital; listing is required; there is no mandatory promoter requirement.",
  facts=[fact6("Circular of 26 April 2024: scheduled status with five-year track record; listed shares; minimum net "
               "worth of ₹1,000 crore; meeting CRAR for SFBs; net profit in last two financial years; GNPA and NNPA ≤ "
               "3 percent and 1 percent in the last two financial years", SFB_UB)])
Q(T, "Licensing norms", "Intermediate",
  "Under RBI's circular of 26 April 2024 on SFBs moving to universal banks, which statement about promoters was "
  "correct?",
  ["There is no mandatory requirement for an eligible SFB to have an identified promoter",
   "A new promoter must be inducted before transition", "Existing promoters must exit on transition",
   "Promoters must accept a fresh five-year lock-in"],
  concept="Promoters in SFB transition",
  explanation="The circular says there is no mandatory requirement to have an identified promoter; existing promoters "
              "continue; no new promoters or change in promoters is allowed during transition; and there is no new "
              "lock-in for existing promoters.",
  steps=["No mandatory promoter", "No new/changed promoters", "No new lock-in"],
  why="New promoters are not permitted, existing ones need not exit, and no new lock-in applies.",
  facts=[fact6("Circular of 26 April 2024: no mandatory requirement for an eligible SFB to have an identified promoter; "
               "addition of new promoters or change in promoters not permitted; no new mandatory lock-in for existing "
               "promoters", SFB_UB)])

gnpa, nnpa, nw, listed, profit_years = 2.6, 1.3, 1_450, True, 2
eligible = nw >= 1_000 and listed and profit_years >= 2 and gnpa <= 3 and nnpa <= 1
assert not eligible and gnpa <= 3 and nnpa > 1
Q(T, "Licensing norms", "Advanced",
  "A listed, scheduled SFB with a seven-year track record has net worth of ₹1,450 crore, meets SFB CRAR norms and was "
  "profitable in each of the last two years. Its GNPA and NNPA in both of those years were 2.6% and 1.3%. Does it "
  "meet the criteria in RBI's circular of 26 April 2024 for transition to a universal bank?",
  ["No; its NNPA exceeds the 1% ceiling, though its GNPA is within 3%", "Yes; it meets every criterion",
   "No; its net worth is below the required ₹2,000 crore", "No; its GNPA exceeds the 2% ceiling"],
  concept="Applying the transition criteria",
  explanation="Net worth (₹1,450 crore ≥ 1,000), listing, track record, CRAR and profitability are met, and GNPA 2.6% "
              "≤ 3%. But NNPA 1.3% exceeds the 1% limit, so it is not eligible.",
  steps=["Net worth ✓, listed ✓, profit ✓", "GNPA 2.6 ≤ 3 ✓", "NNPA 1.3 > 1 ✗ → not eligible"],
  why="The net worth threshold is ₹1,000 crore and the GNPA ceiling is 3%, so those are not the reasons; it fails on "
      "NNPA.",
  computed=True,
  facts=[fact6("Circular of 26 April 2024: minimum net worth ₹1,000 crore; GNPA and NNPA of less than or equal to 3 "
               "percent and 1 percent respectively in the last two financial years", SFB_UB)])

# ================================================================= 25. Financial Markets (3 / 1 / 1)
T = "Financial Markets"
SUB = "Structure and regulators"
Q(T, SUB, "Basic",
  "Chit fund companies in India are regulated under the Chit Funds Act, 1982, which is implemented by:",
  ["State Governments", "RBI", "SEBI", "The Ministry of Corporate Affairs"],
  concept="Regulators of non-bank entities",
  explanation="RBI's NBFC FAQs explain that chit funds are regulated under the Chit Funds Act, 1982, a Central Act "
              "implemented by the State Governments; they are exempt from registration with RBI.",
  steps=["Chit funds → Chit Funds Act, 1982 → State Governments"],
  why="RBI does not register chit funds; SEBI regulates securities markets; MCA is not the implementing authority.",
  facts=[fact("Chit Fund companies are regulated under the Chit Funds Act, 1982, a Central Act implemented by the "
              "State Governments; exempt from RBI registration", NBFC_FAQ)])
Q(T, SUB, "Basic",
  "Under RBI's scale-based regulation of NBFCs, which of the following is NOT one of the four layers?",
  ["Bottom Layer", "Base Layer", "Middle Layer", "Upper Layer"],
  concept="Scale-based regulation",
  explanation="NBFCs are placed in four layers: Base Layer, Middle Layer, Upper Layer and Top Layer. There is no "
              "'Bottom Layer'.",
  steps=["Layers: Base, Middle, Upper, Top"],
  why="Base, Middle and Upper are all layers.",
  facts=[fact("Scale-based regulation layers: Base Layer, Middle Layer, Upper Layer and Top Layer", NBFC_FAQ)])
Q(T, SUB, "Basic",
  "Public deposits accepted by deposit-taking NBFCs must be for what period, according to RBI?",
  ["Not less than 12 months and not more than 60 months", "Repayable on demand", "7 days to one year",
   "Up to 10 years"],
  concept="NBFC deposits",
  explanation="RBI's FAQs say NBFC deposits must be repayable after 12 months to 60 months; deposits repayable on "
              "demand are not allowed.",
  steps=["Tenor: 12 to 60 months", "No demand deposits"],
  why="NBFCs cannot take demand deposits; 7 days–1 year is the bank term-deposit/CD range; 10 years exceeds the limit.",
  facts=[fact("NBFC deposits can be accepted for a period of 12 months to 60 months; deposits repayable on demand are "
              "not permitted", NBFC_FAQ)])
Q(T, SUB, "Intermediate",
  "What is the maximum rate of interest that an NBFC may currently offer on public deposits, according to RBI's NBFC "
  "FAQs?",
  ["12.5% per annum, compounded at not shorter than monthly rests", "9% per annum", "18% per annum",
   "There is no ceiling"],
  concept="Ceiling on NBFC deposit rates",
  explanation="RBI's FAQs state that the present ceiling on the rate of interest NBFCs can offer is 12.5%, with "
              "interest paid or compounded at rests not shorter than monthly.",
  steps=["Ceiling: 12.5%"],
  why="There is a ceiling, and it is 12.5%.",
  facts=[fact("The maximum rate of interest an NBFC can offer is 12.5%, compounded at rests not shorter than monthly",
              NBFC_FAQ)])

nof = 80
max_dep = 1.5 * nof
assert max_dep == 120
Q(T, SUB, "Advanced",
  "A deposit-taking NBFC holds a valid deposit-accepting certificate and a 'BBB–' rating, and has a Net Owned Fund of "
  "₹80 crore. Under RBI's norms, what is the maximum public deposit it can hold, and for what tenor?",
  ["₹120 crore, for 12 to 60 months", "₹80 crore, repayable on demand", "₹240 crore, for 12 to 60 months",
   "₹120 crore, for 7 days to one year"],
  concept="Deposit ceiling for NBFCs",
  explanation="Rated deposit-taking NBFCs (at least BBB–) can hold deposits up to 1.5 times their NOF: 1.5 × 80 = ₹120 "
              "crore, repayable after 12 to 60 months.",
  steps=["Ceiling = 1.5 × NOF = 1.5 × 80 = 120", "Tenor: 12–60 months"],
  why="Demand deposits are not allowed; ₹240 crore uses 3 times NOF; 7 days–1 year is not the NBFC tenor.",
  computed=True,
  facts=[fact("Deposit-taking NBFCs with minimum investment grade rating of BBB-: deposits capped at 1.5 times NOF; "
              "repayable after 12 to 60 months", NBFC_FAQ)])

# ================================================================= 26. Money Market (1 / 2 / 3)
T = "Money Market"
SUB = "Instruments: T-bills, CP, CD, call money"
Q(T, SUB, "Basic",
  "Since 1 July 2025, during what hours is trading in the inter-bank call money market permitted on each business "
  "day?",
  ["9:00 AM to 7:00 PM", "10:00 AM to 3:30 PM", "24 hours on all days", "9:15 AM to 3:30 PM"],
  concept="Call money market timings",
  explanation="The Call, Notice and Term Money Markets Directions, 2021 set market timings of 9:00 AM to 5:00 PM on "
              "each business day, or as specified by RBI. RBI extended call money market timings to 7:00 PM with "
              "effect from 1 July 2025 (and moved the SDF/MSF window to 7:00 PM – 11:59 PM), so the call money "
              "market now runs from 9:00 AM to 7:00 PM.",
  steps=["Directions, 2021: 9 AM – 5 PM unless RBI specifies otherwise", "From 1 July 2025: call money till 7 PM"],
  why="9:15–3:30 is the equity market's normal session; the call money market is not open round the clock.",
  facts=[fact("The market timings shall be from 9:00 AM to 5:00 PM on each business day, or as specified by the "
              "Reserve Bank", CALL_MD),
         fact6("SDF/MSF window moved to 7:00 PM – 11:59 PM from July 01, 2025 in light of the extension of market "
               "timings for call money to 7:00 PM", CALL_TIME)])
Q(T, SUB, "Intermediate",
  "Under RBI's Call, Notice and Term Money Markets Directions, what is the borrowing limit for co-operative banks in "
  "these markets?",
  ["2.0% of their aggregate deposits as at the end of the previous financial year",
   "100% of capital funds on a fortnightly average basis", "225% of net owned fund",
   "No limit, subject to Board approval"],
  concept="Prudential limits in the call money market",
  explanation="Co-operative banks may borrow in call, notice and term money up to 2.0% of their aggregate deposits as "
              "at the end of the previous financial year. Payments banks and RRBs are limited to 100% of capital "
              "funds (fortnightly average) and 125% on any day; standalone primary dealers to 225% of NOF.",
  steps=["Co-operative banks → 2% of aggregate deposits (previous year-end)"],
  why="100% of capital funds applies to payments banks/RRBs/SFBs; 225% of NOF applies to primary dealers; "
      "Board-approved limits apply to scheduled commercial banks.",
  facts=[fact("Co-operative banks: borrowing in call, notice and term money limited to 2.0% of aggregate deposits as "
              "at end of the previous financial year", CALL_MD)])
Q(T, SUB, "Intermediate",
  "According to RBI's chronology, how did the auction format for 91-day Treasury Bills change in December 2002?",
  ["From uniform price auction to multiple price auction", "From multiple price auction to uniform price auction",
   "From auctions to tap issues at a fixed rate", "From weekly to monthly auctions"],
  concept="T-bill auction methods",
  explanation="RBI's chronology records that in December 2002 the auction format of 91-day T-bills was changed from "
              "the uniform price auction to the multiple price auction method.",
  steps=["Dec 2002: 91-day T-bills → multiple price auction"],
  why="The change was in the opposite direction to the second option; T-bills were not moved to tap issue or monthly "
      "auctions.",
  facts=[fact("December 2002: Auction format of 91 day Treasury Bills changed from uniform price auction to the "
              "multiple price auction method", CHRON_00)])

cap_funds = 800
borrow = [900] * 4 + [1_050] + [700] * 9
avg = sum(borrow) / len(borrow)
assert len(borrow) == 14 and round(avg, 1) == 782.1 and avg <= cap_funds and max(borrow) > 1.25 * cap_funds
Q(T, SUB, "Advanced",
  "A small finance bank has capital funds of ₹800 crore. In a 14-day reporting fortnight its outstanding call/notice "
  "borrowing was ₹900 crore on 4 days, ₹1,050 crore on 1 day and ₹700 crore on the other 9 days. Under RBI's limits "
  "for SFBs (100% of capital funds on a daily average basis in a fortnight and 125% on any day), what is its position?",
  ["The fortnightly average (about ₹782 crore) is within limit, but the ₹1,050 crore day breaches the ₹1,000 crore "
   "daily cap", "Both limits are breached", "Both limits are met",
   "The average is breached, but no single day exceeds the cap"],
  concept="Call money borrowing limits for SFBs",
  explanation="Average = (4 × 900 + 1,050 + 9 × 700) ÷ 14 = 10,950 ÷ 14 ≈ ₹782 crore ≤ ₹800 crore. Daily cap = 125% × "
              "800 = ₹1,000 crore; ₹1,050 crore on one day exceeds it.",
  steps=["Total = 3,600 + 1,050 + 6,300 = 10,950", "Average = 782.1 ≤ 800 ✓", "Daily cap 1,000; 1,050 > 1,000 ✗"],
  why="The average is within the limit, and one day does exceed the cap.",
  computed=True,
  facts=[fact("Small finance banks: call and notice money borrowing limited to 100 per cent of capital funds on a "
              "daily average basis in a reporting fortnight and 125 per cent of capital funds on any day", CALL_MD)])

def segment(days_):
    return "call" if days_ == 1 else "notice" if days_ <= 14 else "term" if days_ <= 365 else "outside"
deals = {"P": 14, "Q": 15, "R": 1, "S": 400}
assert {k: segment(v) for k, v in deals.items()} == {"P": "notice", "Q": "term", "R": "call", "S": "outside"}
Q(T, SUB, "Advanced",
  "Classify the following unsecured inter-bank deals under RBI's definitions: P – 14 days; Q – 15 days; R – overnight; "
  "S – 400 days.",
  ["P notice money, Q term money, R call money, S outside the term money market",
   "P term money, Q term money, R call money, S term money", "P notice money, Q notice money, R call money, S term money",
   "P call money, Q notice money, R call money, S outside the term money market"],
  concept="Call, notice and term money",
  explanation="Call money is overnight; notice money is for more than overnight up to and including 14 days; term "
              "money is beyond 14 days up to one year. So P (14 days) is notice, Q (15 days) is term, R is call, and "
              "S (400 days) exceeds one year.",
  steps=["Overnight → call", "2–14 days → notice", "15 days–1 year → term", "> 1 year → none"],
  why="Notice money ends at 14 days, term money at one year; 14 days is not call money.",
  computed=True,
  facts=[fact("Call money: overnight; notice money: tenor up to and including 14 days excluding overnight; term money: "
              "beyond 14 days and up to one year", CALL_MD)])
Q(T, SUB, "Advanced",
  "Consider the following statements about RBI's Call, Notice and Term Money Markets Directions, 2021:\n"
  "I. Payments banks and small finance banks are eligible participants.\n"
  "II. Deals not executed on NDS-CALL must be reported on it within 15 minutes of the deal.\n"
  "III. Local Area Banks are eligible, as they are scheduled commercial banks.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Participants and reporting",
  explanation="Eligible participants are scheduled commercial banks (excluding Local Area Banks), payments banks, SFBs, "
              "RRBs, co-operative banks and primary dealers (I correct, III wrong). Deals outside NDS-CALL must be "
              "reported on it within 15 minutes (II).",
  steps=["I: correct", "II: correct", "III: wrong (LABs excluded)"],
  why="LABs are expressly excluded; 'I only' omits the reporting rule.",
  facts=[fact("Eligible: scheduled commercial banks (excluding Local Area Banks), payments banks, small finance banks, "
              "RRBs, co-operative banks and primary dealers; transactions not executed on NDS-CALL to be reported "
              "within 15 minutes", CALL_MD)])

# ================================================================= 27. Capital Market (2 / 4 / 2)
T = "Capital Market"
Q(T, "Primary and secondary market", "Basic",
  "Which two depositories operate in India's securities market?",
  ["NSDL (established 1996) and CDSL (established 1999)", "NSE and BSE", "CCIL and NPCI", "SEBI and AMFI"],
  concept="Depositories",
  explanation="SEBI's investor site lists National Securities Depository Ltd (1996) and Central Depository Services "
              "(India) Ltd (1999) as India's depositories, which hold securities in electronic form.",
  steps=["NSDL: 1996", "CDSL: 1999"],
  why="NSE and BSE are stock exchanges; CCIL is a clearing corporation and NPCI a payments body; SEBI and AMFI are a "
      "regulator and an industry body.",
  facts=[fact("NSDL was established in 1996 and CDSL in 1999", SEBI_DEP)])
Q(T, "Primary and secondary market", "Basic",
  "In the securities market, 'dematerialisation' means:",
  ["Converting physical securities into electronic form", "Cancelling shares bought back by a company",
   "Converting debt into equity", "Delisting a company from an exchange"],
  concept="Demat",
  explanation="SEBI defines dematerialisation as converting physical securities into electronic form, held in a demat "
              "account with a depository through a depository participant.",
  steps=["Physical certificates → electronic holdings"],
  why="Buy-back, conversion of debt and delisting are different corporate actions.",
  facts=[fact("Dematerialization is the process of converting physical securities into electronic form", SEBI_DEP)])
Q(T, "Primary and secondary market", "Intermediate",
  "NSDL, India's first depository, which began operations in November 1996, was promoted by:",
  ["IDBI, UTI and the National Stock Exchange", "BSE alone", "SEBI and RBI", "LIC and SBI only"],
  concept="Promoters of depositories",
  explanation="NSDL was promoted by IDBI, UTI and NSE; CDSL was initially promoted by BSE, which later divested its "
              "stake to leading banks.",
  steps=["NSDL → IDBI, UTI, NSE", "CDSL → initially BSE"],
  why="BSE promoted CDSL; regulators do not promote depositories; LIC and SBI were not NSDL's promoters.",
  facts=[fact("NSDL began operations in November 1996, promoted by IDBI, UTI and the National Stock Exchange; CDSL "
              "initially promoted by BSE", NSDL_ABOUT)])
Q(T, "SEBI", "Intermediate",
  "India's index-based market-wide circuit breakers are triggered at which levels of movement, and by which indices?",
  ["10%, 15% and 20%, by movement of either the BSE Sensex or the Nifty 50, whichever is breached earlier",
   "5%, 10% and 15%, by the Nifty 50 only", "10% and 20%, by the Sensex only",
   "2%, 5% and 10%, by each individual stock"],
  concept="Market-wide circuit breakers",
  explanation="Market-wide circuit breakers apply at 10%, 15% and 20% movements in either direction, triggered by the "
              "Sensex or the Nifty 50, whichever is breached earlier, and halt trading in all equity and equity "
              "derivative markets nationwide.",
  steps=["Levels: 10%, 15%, 20%", "Trigger: Sensex or Nifty 50, whichever earlier"],
  why="Individual-stock price bands (2%, 5%, 10% etc.) are different from market-wide breakers; both indices count.",
  facts=[fact("Index based market-wide circuit breakers at 10%, 15% and 20% levels, triggered by movement of either "
              "the BSE Sensex or the Nifty 50 whichever is breached earlier, bring about a coordinated trading halt in "
              "all equity and equity derivative markets", NSE_MWCB)])
Q(T, "Primary and secondary market", "Intermediate",
  "To deepen the corporate bond market, what did the Union Budget 2026-27 propose?",
  ["A market-making framework with access to funds and derivatives on corporate bond indices, and total return swaps "
   "on corporate bonds", "Abolishing the corporate bond market in favour of G-secs",
   "Making all corporate bonds tax-free", "Merging NSE and BSE debt platforms"],
  concept="Corporate bond market reforms",
  explanation="The Budget proposed a market-making framework with suitable access to funds and derivatives on "
              "corporate bond indices, along with total return swaps on corporate bonds.",
  steps=["Market making + derivatives on bond indices", "Total return swaps on corporate bonds"],
  why="The Budget did not propose abolition, blanket tax exemption or an exchange merger.",
  current=ca(BUDGET_DAY),
  facts=[fact("The Union Budget 2026-27 proposes a market making framework with suitable access to funds and "
              "derivatives on corporate bond indices along with total return swaps on corporate bonds", BUDGET)])
Q(T, "Primary and secondary market", "Intermediate",
  "Among the external-sector measures announced by the RBI Governor on 5 June 2026, what was done about investment by "
  "NRIs and OCIs in equity instruments traded on stock exchanges without SEBI registration?",
  ["The limits were increased, and the same facility was extended to all individual Persons Resident Outside India",
   "The facility was withdrawn", "The limits were frozen at existing levels for one year",
   "It was restricted to mutual fund units only"],
  concept="Portfolio investment by non-residents",
  explanation="The Governor announced that limits for investment by NRIs and OCIs in equity instruments traded on the "
              "stock market without SEBI registration would be increased, and the facility extended to all individual "
              "PROIs at par with NRIs and OCIs.",
  steps=["NRI/OCI limits increased", "Extended to all individual PROIs"],
  why="The facility was widened, not withdrawn, frozen or restricted.",
  current=ca(JUN26),
  facts=[fact("The limits for investment by NRIs and OCIs in equity instruments traded on the stock market without SEBI "
              "registration are being increased; the same facility is being extended to all individual Persons "
              "Resident Outside India at par with NRIs and OCIs", GOV_JUN26)])

prev, low = 25_000, 21_150
fall = (prev - low) / prev * 100
assert round(fall, 1) == 15.4 and 15 <= fall < 20
Q(T, "Indices", "Advanced",
  "The Nifty 50 closed at 25,000 the previous day. At 12:40 pm today it falls to 21,150 before the Sensex has hit any "
  "trigger. Under the market-wide circuit breaker table published by NSE, what happens?",
  ["The 15% level is breached before 1 pm, so trading halts for 1 hour 45 minutes, followed by a 15-minute pre-open "
   "session", "The 10% level is breached, so trading halts for 45 minutes",
   "The 20% level is breached, so trading halts for the rest of the day", "No halt, since the fall is after noon"],
  concept="Applying circuit breaker levels",
  explanation="Fall = (25,000 − 21,150) ÷ 25,000 = 15.4%, which crosses the 15% level (but not 20%). For a 15% move "
              "before 1 pm, trading halts for 1 hour 45 minutes, and resumes with a 15-minute pre-open call auction.",
  steps=["Fall = 3,850 ÷ 25,000 = 15.4%", "15% level, before 1 pm → 1 h 45 min halt + 15 min pre-open"],
  why="The move exceeds 15% (so the 10% rule is superseded) but not 20%; halts apply after noon too.",
  computed=True,
  facts=[fact("Market-wide circuit breaker: 15% movement before 1 pm → 1 hour 45 minutes halt; 10% before 1 pm → 45 "
              "minutes; 20% → trading halted for the remainder of the day; 15 minutes pre-open session after each "
              "halt", NSE_MWCB)])
Q(T, "SEBI", "Advanced",
  "Consider the following statements based on SEBI's investor education pages on Market Infrastructure Institutions "
  "(MIIs):\n"
  "I. Stock exchanges and depositories are MIIs.\n"
  "II. NSDL, established in August 1996, introduced dematerialisation in India.\n"
  "III. CDSL was established in February 1999.\n"
  "Which of the above is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I only"],
  concept="Market Infrastructure Institutions",
  explanation="SEBI's page describes stock exchanges and depositories as MIIs (I), states that NSDL was established in "
              "August 1996 and introduced dematerialisation (II), and that CDSL was established in February 1999 "
              "(III). All three are correct.",
  steps=["I: correct", "II: correct", "III: correct"],
  why="Each other option leaves out a correct statement.",
  facts=[fact("MIIs include stock exchanges and depositories; NSDL established in August 1996 introduced "
              "dematerialization in India; CDSL established in February 1999", SEBI_MII)])

# ================================================================= 28. Insurance (1 / 2 / 0)
T = "Insurance"
Q(T, "Life and general insurance", "Basic",
  "Under IRDAI's 2024 master circular on life insurance products, the free-look period (to return a policy) is:",
  ["30 days from receipt of the policy document", "15 days from issue of the policy", "7 days from payment of premium",
   "60 days from the policy date"],
  concept="Free-look period",
  explanation="IRDAI's master circular of June 2024 extended the free-look period for life insurance policies to 30 "
              "days from the receipt of the policy document, from 15 days earlier.",
  steps=["Earlier: 15 days", "From 2024: 30 days from receipt of the policy document"],
  why="15 days was the old period; 7 and 60 days are not the rule.",
  current=ca("2024-06-12"),
  facts=[fact("Free look period extended to 30 days from 15 days in IRDAI's master circular on life insurance "
              "products of June 12, 2024", FREELOOK)])
Q(T, "Life and general insurance", "Intermediate",
  "IRDAI's master circular on life insurance products (June 2024) made which facility mandatory in all savings-type "
  "life insurance products?",
  ["Policy loan", "Guaranteed return of 8%", "Free health cover", "Monthly dividend"],
  concept="Policyholder-friendly product rules",
  explanation="IRDAI made the policy loan facility mandatory in all savings life insurance products, to meet "
              "policyholders' liquidity needs.",
  steps=["Savings life products → policy loan facility mandatory"],
  why="IRDAI did not mandate guaranteed returns, free health cover or dividends.",
  current=ca("2024-06-12"),
  facts=[fact("IRDAI says facility of policy loan is mandatory for life insurance savings products (master circular, "
              "June 2024)", FREELOOK)])
Q(T, "Life and general insurance", "Intermediate",
  "According to LIC's account of insurance history, which was the first Indian life insurance company, and when did "
  "it start business?",
  ["Bombay Mutual Life Assurance Society, 1870", "Oriental Life Insurance Company, 1818",
   "Triton Insurance Company, 1850", "New India Assurance, 1919"],
  concept="History of insurance",
  explanation="Oriental Life (1818, Calcutta) was the first life insurer on Indian soil, but it was a British "
              "company. Bombay Mutual Life Assurance Society (1870) was the first Indian life insurance company. "
              "Triton (1850) was the first general insurer.",
  steps=["1818: Oriental Life — first life insurer on Indian soil", "1870: Bombay Mutual — first Indian life insurer"],
  why="Oriental Life was not Indian-owned; Triton was a general insurer; New India Assurance is a general insurer.",
  facts=[fact("1818: Oriental Life Insurance Company, the first life insurance company on Indian soil; 1870: Bombay "
              "Mutual Life Assurance Society, the first Indian life insurance company; 1850: Triton Insurance Company, "
              "first general insurer", LIC_HIST)])

# ================================================================= 29. Mutual Funds (2 / 2 / 2)
T = "Mutual Funds"
Q(T, "Types", "Basic",
  "Under SEBI's categorisation of mutual fund schemes, a 'Focused Fund' may invest in at most how many stocks?",
  ["30", "50", "20", "100"],
  concept="Equity scheme categories",
  explanation="A focused fund is an equity scheme focused on the number of stocks, with a maximum of 30 stocks and at "
              "least 65% of assets in equity.",
  steps=["Focused fund: maximum 30 stocks; ≥ 65% equity"],
  why="The other numbers are not the SEBI cap.",
  facts=[fact("Focused Fund: a scheme focused on the number of stocks (maximum 30); minimum investment in equity 65% "
              "of total assets", MF_CAT)])
Q(T, "Types", "Basic",
  "SEBI's October 2017 circular grouped mutual fund schemes broadly into five groups. Which of the following is NOT "
  "one of them?",
  ["Commodity schemes", "Hybrid schemes", "Solution oriented schemes", "Other schemes"],
  concept="Broad groups of schemes",
  explanation="The five groups are Equity, Debt, Hybrid, Solution Oriented and Other schemes.",
  steps=["Equity, Debt, Hybrid, Solution Oriented, Other"],
  why="Hybrid, solution oriented and other schemes are all among the five groups.",
  facts=[fact("Schemes broadly classified as Equity Schemes, Debt Schemes, Hybrid Schemes, Solution Oriented Schemes "
              "and Other Schemes", MF_CAT)])
Q(T, "Types", "Intermediate",
  "SEBI's October 2017 scheme categorisation (in force until the February 2026 revision) allowed a mutual fund "
  "only one scheme per category. Which of the following was an exception that allowed more than one scheme in a "
  "category?",
  ["Index funds/ETFs tracking different indices", "Large cap funds with different fund managers",
   "Liquid funds with different minimum investments", "ELSS schemes with different lock-ins"],
  concept="One scheme per category",
  explanation="Under the 2017 framework only one scheme per category was permitted, except index funds/ETFs tracking "
              "different indices, fund of funds with different underlying schemes, and sectoral/thematic funds "
              "investing in different sectors or themes. SEBI's circular of 26 February 2026 revised the "
              "categorisation framework.",
  steps=["Exceptions: index funds/ETFs, FoFs, sectoral/thematic funds"],
  why="Different managers, minimum investments or lock-ins do not create exceptions (ELSS has a fixed 3-year lock-in).",
  facts=[fact("Only one scheme per category permitted, except Index Funds/ETFs replicating/tracking different indices; "
              "Fund of Funds having different underlying schemes; Sectoral/thematic funds investing in different "
              "sectors/themes", MF_CAT),
         fact6("SEBI circular 'Categorization and Rationalization of Mutual Fund Schemes' dated 26 February 2026",
               SEBI_CAT26)])
Q(T, "AMFI", "Intermediate",
  "How often does AMFI update the list of large cap, mid cap and small cap stocks that mutual funds must follow, and "
  "how quickly must funds rebalance?",
  ["Every six months, based on end-June and end-December data; rebalance within one month",
   "Every quarter; rebalance within one week", "Once a year in April; rebalance within three months",
   "Every month; no rebalancing required"],
  concept="AMFI's market-cap list",
  explanation="AMFI prepares the list using full market capitalisation (average across exchanges where listed), "
              "updates it every six months based on data as on the end of June and December, and mutual funds must "
              "rebalance their portfolios within one month of an update.",
  steps=["Update: half-yearly (June, December data)", "Rebalancing: within one month"],
  why="The list is half-yearly, and rebalancing within one month is required.",
  facts=[fact("The list would be updated every six months based on the data as on the end of June and December; Mutual "
              "Funds to rebalance their portfolios within a period of one month", MF_CAT)])
Q(T, "Types", "Advanced",
  "Consider the following statements about SEBI's equity scheme categories as laid down in its October 2017 "
  "circular (before the February 2026 revision):\n"
  "I. An ELSS had to invest at least 80% of total assets in equity and equity-related instruments.\n"
  "II. A sectoral/thematic fund had to invest at least 80% of total assets in its chosen sector or theme.\n"
  "III. A fund house could offer both a value fund and a contra fund.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Equity scheme characteristics",
  explanation="ELSS: minimum 80% in equity (I). Sectoral/thematic: minimum 80% in the sector/theme (II). Under the "
              "2017 circular a mutual fund could offer either a value fund or a contra fund, not both (III wrong). "
              "SEBI's February 2026 circular now allows both, subject to portfolio overlap of at most 50%.",
  steps=["I: correct", "II: correct", "III: wrong (either value or contra)"],
  why="III contradicts the circular; 'I only' omits II.",
  facts=[fact("ELSS minimum investment in equity 80% of total assets; Sectoral/Thematic minimum 80% in the sector/theme; "
              "Mutual Funds will be permitted to offer either Value fund or Contra fund", MF_CAT),
         fact6("SEBI circular 'Categorization and Rationalization of Mutual Fund Schemes' dated 26 February 2026",
               SEBI_CAT26),
         fact6("Law-firm summary of the February 2026 circular: earlier either a value or a contra fund; now both "
               "permitted subject to portfolio overlap not exceeding 50%", ELP_CAT26)])

def debt_cat(md_years):
    if 0.25 <= md_years <= 0.5:
        return "Ultra Short Duration"
    if 0.5 < md_years <= 1:
        return "Low Duration"
    if 1 < md_years <= 3:
        return "Short Duration"
    if 3 < md_years <= 4:
        return "Medium Duration"
    if 4 < md_years <= 7:
        return "Medium to Long Duration"
    return "Long Duration"
port = {"P": 4 / 12, "Q": 2, "R": 5, "S": 9}
assert {k: debt_cat(v) for k, v in port.items()} == {"P": "Ultra Short Duration", "Q": "Short Duration",
                                                     "R": "Medium to Long Duration", "S": "Long Duration"}
Q(T, "Types", "Advanced",
  "Four open-ended debt schemes have portfolio Macaulay durations of: P – 4 months; Q – 2 years; R – 5 years; S – 9 "
  "years. Under SEBI's categorisation, which matching is correct?",
  ["P Ultra Short Duration; Q Short Duration; R Medium to Long Duration; S Long Duration",
   "P Low Duration; Q Short Duration; R Medium Duration; S Long Duration",
   "P Ultra Short Duration; Q Medium Duration; R Long Duration; S Long Duration",
   "P Liquid; Q Short Duration; R Medium to Long Duration; S Dynamic Bond"],
  concept="Debt categories by Macaulay duration",
  explanation="Ultra short: 3–6 months; low: 6–12 months; short: 1–3 years; medium: 3–4 years; medium to long: 4–7 "
              "years; long: more than 7 years. So P (4 months) ultra short, Q (2 years) short, R (5 years) medium to "
              "long, S (9 years) long.",
  steps=["4 months → 3–6 m → Ultra Short", "2 y → 1–3 y → Short", "5 y → 4–7 y → Medium to Long", "9 y → > 7 y → Long"],
  why="4 months is not low duration (6–12 months); 5 years is not medium (3–4 years); liquid funds are defined by "
      "maturity up to 91 days, and dynamic bond funds invest across durations.",
  computed=True,
  facts=[fact("Ultra Short Duration: Macaulay duration 3-6 months; Low Duration 6-12 months; Short Duration 1-3 years; "
              "Medium Duration 3-4 years; Medium to Long Duration 4-7 years; Long Duration greater than 7 years",
              MF_CAT)])

# ================================================================= 30. Budget and Economic Survey (4 / 1 / 1)
T = "Budget and Economic Survey"
Q(T, "Union Budget highlights", "Basic",
  "To strengthen private developers' confidence about risks during infrastructure construction, the Union Budget "
  "2026-27 proposed to set up:",
  ["An Infrastructure Risk Guarantee Fund providing partial credit guarantees to lenders",
   "A new infrastructure bank to replace NaBFID", "A sovereign wealth fund for highways",
   "A tax-free infrastructure bond scheme for retail investors"],
  concept="Infrastructure financing",
  explanation="The Budget proposed an Infrastructure Risk Guarantee Fund to provide prudently calibrated partial credit "
              "guarantees to lenders, addressing risks during development and construction.",
  steps=["Infrastructure Risk Guarantee Fund → partial credit guarantees to lenders"],
  why="The Budget did not propose replacing NaBFID, a highway sovereign fund or tax-free retail bonds.",
  current=ca(BUDGET_DAY),
  facts=[fact("The Finance Minister proposed to set up an Infrastructure Risk Guarantee Fund to provide prudently "
              "calibrated partial credit guarantees to lenders", BUDGET)])
Q(T, "Union Budget highlights", "Basic",
  "Which two public sector NBFCs did the Union Budget 2026-27 propose to restructure to achieve scale and improve "
  "efficiency?",
  ["Power Finance Corporation and Rural Electrification Corporation", "NABARD and SIDBI", "LIC and GIC Re",
   "IRFC and IREDA"],
  concept="Public sector NBFCs",
  explanation="The Budget proposed to restructure the Power Finance Corporation and the Rural Electrification "
              "Corporation to achieve scale and improve efficiency in public sector NBFCs.",
  steps=["PFC + REC → restructuring proposed"],
  why="NABARD and SIDBI are development finance institutions; LIC and GIC Re are insurers; IRFC and IREDA were not "
      "named.",
  current=ca(BUDGET_DAY),
  facts=[fact("The Union Budget proposes to restructure the Power Finance Corporation and Rural Electrification "
              "Corporation to achieve scale and improve efficiency in the Public Sector NBFCs", BUDGET)])
Q(T, "Fiscal terms", "Basic",
  "What revenue deficit did the Union Budget documents estimate for BE 2026-27, as a percentage of GDP?",
  ["1.5%", "4.3%", "0.3%", "4.4%"],
  concept="Revenue deficit",
  explanation="The Budget estimated the fiscal deficit at 4.3% of GDP (BE 2026-27), the revenue deficit at 1.5% and "
              "the effective revenue deficit at 0.3%. 4.4% is the RE 2025-26 fiscal deficit.",
  steps=["FD 4.3%", "RD 1.5%", "ERD 0.3%"],
  why="4.3% is the fiscal deficit, 0.3% the effective revenue deficit, 4.4% the RE 2025-26 fiscal deficit.",
  current=ca(BUDGET_DAY),
  facts=[fact("Revenue deficit for BE 2026-27 is estimated at 1.5%; effective revenue deficit at 0.3%; fiscal deficit "
              "4.3% (RE 2025-26: 4.4%)", BUDGET)])
Q(T, "Fiscal terms", "Basic",
  "What did the Union Budget documents estimate the Centre's gross tax revenue to be in BE 2026-27, as a share of "
  "GDP?",
  ["11.2%", "7.8%", "17.0%", "61.5%"],
  concept="Tax-to-GDP",
  explanation="The macroeconomic framework laid with the Budget estimated gross tax revenue at 11.2% of GDP for BE "
              "2026-27.",
  steps=["Gross tax revenue (BE 2026-27): 11.2% of GDP"],
  why="7.8% is GFCF growth in FY26; 61.5% is the PFCE share of GDP; 17.0% is not the figure.",
  current=ca(BUDGET_DAY),
  facts=[fact("Gross tax revenue is estimated at 11.2% of GDP for BE 2026-27", BUDGET)])
Q(T, "Union Budget highlights", "Intermediate",
  "Which of the following was among the Union Budget 2026-27 measures to make TReDS more useful for MSMEs?",
  ["A credit guarantee support mechanism through CGTMSE for invoice discounting on TReDS platforms",
   "Abolishing TReDS in favour of bank overdrafts", "Allowing only private companies to buy from MSMEs via TReDS",
   "Capping TReDS financing at ₹1 lakh per invoice"],
  concept="Liquidity support for MSMEs",
  explanation="Noting that TReDS had made more than ₹7 lakh crore available to MSMEs, the Budget proposed: mandating "
              "TReDS for all CPSE purchases from MSMEs; credit guarantee support through CGTMSE for invoice "
              "discounting on TReDS; linking GeM with TReDS; and TReDS receivables as asset-backed securities.",
  steps=["TReDS mandatory for CPSE purchases", "CGTMSE guarantee for TReDS discounting", "GeM–TReDS link",
         "TReDS receivables as ABS"],
  why="The Budget expanded TReDS rather than abolishing or capping it, and the CPSE mandate is the opposite of the "
      "third option.",
  current=ca(BUDGET_DAY),
  facts=[fact("Proposed measures: mandate TReDS as the transaction settlement platform for all purchases from MSMEs by "
              "CPSEs; credit guarantee support mechanism through CGTMSE for invoice discounting on TReDS; link GeM with "
              "TReDS; TReDS receivables as asset-backed securities; more than ₹7 lakh crore made available through "
              "TReDS", BUDGET)])

rd, erd = 1.5, 0.3
assert round(rd - erd, 1) == 1.2
Q(T, "Fiscal terms", "Advanced",
  "Effective revenue deficit is the revenue deficit minus grants-in-aid for creation of capital assets. With the "
  "revenue deficit at 1.5% of GDP and the effective revenue deficit at 0.3% of GDP in BE 2026-27, what do grants for "
  "creation of capital assets amount to?",
  ["About 1.2% of GDP", "About 1.8% of GDP", "About 0.3% of GDP", "About 4.0% of GDP"],
  concept="Effective revenue deficit",
  explanation="ERD = RD − grants for capital assets, so grants = RD − ERD = 1.5 − 0.3 = 1.2% of GDP.",
  steps=["Grants = RD − ERD", "= 1.5 − 0.3 = 1.2% of GDP"],
  why="1.8% adds the two; 0.3% is the ERD itself; 4.0% is the fiscal deficit less ERD.",
  computed=True, current=ca(BUDGET_DAY),
  facts=[fact("Revenue deficit for BE 2026-27 estimated at 1.5%; effective revenue deficit for BE 2026-27 estimated at "
              "0.3%", BUDGET)])

# ================================================================= 31. Government Financial Schemes (3 / 4 / 4)
T = "Government Financial Schemes"
CG = "Credit guarantee schemes"
Q(T, CG, "Basic",
  "The Credit Guarantee Scheme for Exporters (CGSE), approved by the Union Cabinet on 12 November 2025, provides:",
  ["100% credit guarantee cover by NCGTC to lenders for up to ₹20,000 crore of additional collateral-free credit to "
   "eligible exporters", "50% guarantee by CGTMSE only for micro exporters", "Interest-free loans from RBI to exporters",
   "Export insurance by ECGC at zero premium"],
  concept="Credit guarantees for exporters",
  explanation="CGSE lets NCGTC give 100% credit guarantee coverage to member lending institutions for up to ₹20,000 "
              "crore of additional collateral-free credit to eligible exporters, including MSMEs.",
  steps=["Guarantor: NCGTC", "Cover: 100%", "Size: up to ₹20,000 crore additional credit"],
  why="It is run through NCGTC, not CGTMSE or RBI, and is a guarantee, not ECGC insurance.",
  current=ca("2025-11-12"),
  facts=[fact("Cabinet approves Credit Guarantee Scheme for Exporters: 100% credit guarantee coverage by NCGTC to "
              "Member Lending Institutions for extending additional credit facilities up to ₹20,000 crore to eligible "
              "exporters including MSMEs", CGSE)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Basic",
  "Under the PM Vishwakarma scheme for artisans and craftspeople, collateral-free enterprise development loans carry "
  "what concessional rate of interest for the beneficiary?",
  ["5%", "7%", "4%", "9%"],
  concept="PM Vishwakarma credit support",
  explanation="Beneficiaries pay a concessional 5% rate on standard accounts; the Government's interest subvention "
              "(capped at 8%) covers the rest of the bank's rate.",
  steps=["Beneficiary rate: 5%", "Subvention: up to 8%"],
  why="7% and 4% relate to KCC crop loans; 9% is not the scheme rate.",
  facts=[fact("PM Vishwakarma: concessional rate of interest 5% for standard accounts, with interest subvention of up "
              "to 8% provided upfront to banks", VISHWA)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Basic",
  "Under the Modified Interest Subvention Scheme for short-term agricultural loans through KCC, as continued by the "
  "Union Cabinet for FY 2025-26, what was the effective interest rate for a farmer who repaid promptly?",
  ["4%", "7%", "1.5%", "9%"],
  concept="Interest subvention on KCC loans",
  explanation="Lenders give eligible short-term crop loans at 7% with 1.5% interest subvention from the Government; "
              "prompt repayment earns a further 3% incentive, bringing the effective rate to 4%.",
  steps=["Lending rate 7%", "Prompt repayment incentive 3%", "Effective rate 4%"],
  why="7% is the rate before the prompt repayment incentive; 1.5% is the subvention to lenders.",
  facts=[fact("Farmers get short-term loans at 7 per cent with eligible lending institutions receiving 1.5 per cent "
              "interest subvention; additional 3 per cent prompt repayment incentive effectively reduces the rate to "
              "4 per cent", KCC_MISS),
         fact6("Cabinet (28 May 2025) approved continuation of MISS for FY 2025-26 with the existing 1.5% interest "
               "subvention; loans up to ₹3 lakh at 7%; prompt repayment incentive up to 3%", MISS_2526)])
Q(T, CG, "Intermediate",
  "Which of the following is true of the Credit Guarantee Scheme for Exporters (CGSE) approved in November 2025?",
  ["It is implemented by the Department of Financial Services through NCGTC and is open to non-MSME exporters too",
   "It is limited to micro enterprises", "It is administered by RBI", "It applies only to exports to the USA"],
  concept="Design of CGSE",
  explanation="CGSE is run by DFS through NCGTC, with a management committee chaired by the DFS Secretary, and covers "
              "eligible exporters including MSMEs as well as larger exporters.",
  steps=["Administered: DFS via NCGTC", "Eligibility: MSME and non-MSME exporters"],
  why="It is not limited to micro enterprises or a single destination, and RBI does not administer it.",
  current=ca("2025-11-12"),
  facts=[fact("CGSE implemented by the Department of Financial Services through NCGTC for eligible exporters including "
              "MSMEs (and non-MSMEs), overseen by a Management Committee chaired by Secretary, DFS", CGSE)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Intermediate",
  "Under PM Vishwakarma, how is the collateral-free credit provided?",
  ["Up to ₹1 lakh in the first tranche (18 months) and up to ₹2 lakh in the second tranche (30 months)",
   "A single loan of ₹3 lakh repayable over 5 years", "Up to ₹50,000 in each of three tranches",
   "Up to ₹10 lakh in one tranche"],
  concept="PM Vishwakarma loan tranches",
  explanation="The first tranche is up to ₹1 lakh repayable in 18 months; the second, up to ₹2 lakh repayable in 30 "
              "months, is available after the first is fully repaid (standard account) and the borrower has adopted "
              "digital transactions or undergone advanced skill training.",
  steps=["Tranche 1: ₹1 lakh / 18 months", "Tranche 2: ₹2 lakh / 30 months"],
  why="The loan comes in two tranches totalling ₹3 lakh, not one loan or three ₹50,000 tranches.",
  facts=[fact("First tranche up to Rs 1 lakh for 18 months; second tranche up to Rs 2 lakh for 30 months after full "
              "repayment of the first tranche and adoption of digital transactions or advanced skill training", VISHWA)])
Q(T, CG, "Intermediate",
  "Under PM Vishwakarma, loans are covered by CGTMSE on a portfolio basis. What are the maximum guarantee covers for "
  "the first and second tranches?",
  ["50% and 15%", "75% and 50%", "85% and 85%", "100% and 100%"],
  concept="Credit guarantee for PM Vishwakarma loans",
  explanation="CGTMSE covers PM Vishwakarma loans on a portfolio basis with maximum guarantee cover of 50% for the "
              "first tranche and 15% for the second (effective cover 35.5% and 13%).",
  steps=["Tranche 1: up to 50%", "Tranche 2: up to 15%"],
  why="The other percentages do not match the scheme.",
  facts=[fact("Guarantee cover under CGTMSE on portfolio basis: maximum 50% for first tranche and 15% for second "
              "tranche", VISHWA)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Intermediate",
  "Under the Modified Interest Subvention Scheme for KCC loans, as continued by the Union Cabinet for FY 2025-26, "
  "what interest subvention did the Government give to lending institutions?",
  ["1.5%", "3%", "4%", "7%"],
  concept="Interest subvention",
  explanation="Eligible lending institutions receive 1.5% interest subvention for lending at 7%; farmers who repay "
              "promptly get a separate 3% incentive.",
  steps=["To lenders: 1.5%", "To prompt-paying farmers: 3%"],
  why="3% is the prompt repayment incentive to farmers; 4% and 7% are interest rates.",
  facts=[fact("Eligible lending institutions receive 1.5 per cent interest subvention; farmers pay 7 per cent, "
              "reduced to 4 per cent with prompt repayment", KCC_MISS),
         fact6("Cabinet (28 May 2025) approved continuation of MISS for FY 2025-26 with the existing 1.5% interest "
               "subvention", MISS_2526)])

loan = 160_000
saving = loan * (0.07 - 0.04)
assert round(loan * 0.04) == 6_400 and round(saving) == 4_800
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Advanced",
  "In FY 2025-26, a farmer took a short-term KCC crop loan of ₹1.6 lakh under MISS for one year and repaid it on the "
  "due date. What interest did she effectively bear, and how much did prompt repayment save her compared with the "
  "7% rate?",
  ["₹6,400; saves ₹4,800", "₹11,200; saves ₹2,400", "₹6,400; saves ₹2,400", "₹4,800; saves ₹6,400"],
  concept="Prompt repayment incentive",
  explanation="Effective rate 4%: 1,60,000 × 4% = ₹6,400. At 7% the interest would be ₹11,200, so the 3% prompt "
              "repayment incentive saves ₹4,800.",
  steps=["4% × 1,60,000 = 6,400", "7% × 1,60,000 = 11,200", "Saving = 4,800"],
  why="₹11,200 is the interest without the incentive; ₹2,400 uses 1.5%; the last option swaps the figures.",
  computed=True,
  facts=[fact("Short-term loans at 7 per cent; additional 3 per cent prompt repayment incentive effectively reducing "
              "the interest rate to 4 per cent", KCC_MISS),
         fact6("MISS continued for FY 2025-26: loans up to ₹3 lakh at 7%; prompt repayment incentive up to 3%, "
               "effective 4%", MISS_2526)])

bank_rate, ben_rate, avg_out = 13.0, 5.0, 60_000
subv = min(bank_rate - ben_rate, 8.0)
assert subv == 8.0 and round(avg_out * subv / 100) == 4_800
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Advanced",
  "A bank sanctions a PM Vishwakarma first-tranche loan at its fixed rate of 13%. The average outstanding over the "
  "year is ₹60,000 and the account stays standard. How much interest subvention does the Government bear for the "
  "year, and what rate does the artisan effectively pay?",
  ["₹4,800; 5%", "₹7,800; nil", "₹3,000; 8%", "₹4,800; 13%"],
  concept="Interest subvention under PM Vishwakarma",
  explanation="The beneficiary pays 5%; the Government covers the difference up to an 8% cap. 13 − 5 = 8%, within the "
              "cap, so subvention = 8% × 60,000 = ₹4,800.",
  steps=["Subvention rate = min(13 − 5, 8) = 8%", "8% × 60,000 = ₹4,800", "Artisan pays 5%"],
  why="₹7,800 assumes the Government pays the full 13%; ₹3,000 uses 5%; the artisan does not pay 13% or 8%.",
  computed=True,
  facts=[fact("Rate of interest 13.00% (fixed); concessional rate of interest 5% for standard accounts, balance "
              "received as interest subvention of up to 8% from the Government", VISHWA)])
Q(T, CG, "Advanced",
  "In March 2026 the Government modified the Mutual Credit Guarantee Scheme for MSMEs (MCGS-MSME), adding a track for "
  "exporters. Which of the following describes it?",
  ["Guarantee coverage of 75% of the default amount for exporters who exported at least 25% of turnover in each of "
   "the previous three years", "100% coverage for any exporter, without conditions",
   "60% coverage only for exporters with turnover above ₹500 crore", "Coverage replaced by an interest subsidy"],
  concept="MCGS-MSME modifications",
  explanation="Under the March 2026 revision, exporters that are profitable and have exported at least 25% of turnover "
              "in each of the previous three financial years get guarantee coverage of 75% of the default amount (the "
              "general scheme gives 60%).",
  steps=["General MCGS cover: 60%", "Exporters (≥ 25% export share for 3 years): 75%"],
  why="Cover is 75%, not 100%, and it is conditional; no turnover floor or subsidy replacement was announced.",
  current=ca("2026-03-21"),
  facts=[fact("Exporters should have exported at least 25 per cent of their turnover in each of the previous three "
              "financial years; guarantee coverage for exporters set at 75 per cent of the default amount", MCGS_26)])

loan_cr = 20
upfront = 0.05 * loan_cr
yearly = 0.01 * loan_cr
years = list(range(4, 4 + round(upfront / yearly)))
assert upfront == 1.0 and round(yearly, 2) == 0.2 and years == [4, 5, 6, 7, 8]
Q(T, CG, "Advanced",
  "Under the March 2026 revision of MCGS-MSME, the 5% upfront contribution on the loan amount is refundable at 1% a "
  "year from the fourth year, subject to satisfactory loan performance. For a guaranteed loan of ₹20 crore, how much "
  "is deposited upfront and when is it fully refunded?",
  ["₹1 crore; ₹20 lakh a year in years 4 to 8", "₹1 crore; all of it in year 4", "₹20 lakh; in year 5",
   "₹2 crore; ₹40 lakh a year in years 4 to 8"],
  concept="Refundable upfront contribution",
  explanation="Upfront = 5% × 20 = ₹1 crore. Refund = 1% × 20 = ₹20 lakh a year from year 4, so five refunds (years 4, "
              "5, 6, 7, 8) return the full ₹1 crore.",
  steps=["Upfront = 0.05 × 20 = 1 crore", "Refund = 0.01 × 20 = 0.2 crore a year", "1 ÷ 0.2 = 5 years: years 4–8"],
  why="The refund is spread at 1% a year, not paid at once; ₹20 lakh is one year's refund; ₹2 crore uses 10%.",
  computed=True, current=ca("2026-03-21"),
  facts=[fact("The five per cent upfront contribution has been made refundable, with one per cent returned each year "
              "from the fourth year onwards, subject to satisfactory loan performance", MCGS_26)])

# ================================================================= 32. RBI Circulars and Regulatory Updates (2 / 3 / 2)
T = "RBI Circulars and Regulatory Updates"
SUB = "Recent RBI directions"
Q(T, SUB, "Basic",
  "Among the external-sector measures announced by the RBI Governor on 5 June 2026, what was proposed for the time "
  "allowed for realisation of export proceeds?",
  ["To restore it to nine months", "To cut it to three months", "To abolish any time limit",
   "To extend it to two years"],
  concept="Export realisation period",
  explanation="The Governor's statement of 5 June 2026 proposed to restore the time for realisation of export proceeds "
              "to nine months, alongside measures on G-secs under FAR, NRI/OCI equity limits and FCNR(B) deposits.",
  steps=["Export proceeds realisation → restored to nine months"],
  why="The proposal was a nine-month period, not three months, two years or no limit.",
  current=ca(JUN26),
  facts=[fact("It is proposed to restore the time for realisation of export proceeds to nine months (Governor's "
              "Statement, June 5, 2026)", GOV_JUN26)])
Q(T, SUB, "Basic",
  "By a circular of 23 October 2026, RBI delegated the power to compound certain FEMA contraventions (overseas "
  "investment, borrowing and lending, and guarantees) from its Central Office to:",
  ["Its Regional Offices", "Authorised Dealer banks", "The Enforcement Directorate", "SEBI"],
  concept="Compounding under FEMA",
  explanation="As a customer-service measure, RBI delegated compounding of these contraventions to selected Regional "
              "Offices (by the UIN prefix for overseas investment, or by the applicant's jurisdiction for borrowing, "
              "lending and guarantees). Applications without a UIN or covering several categories go to CEFA, Mumbai.",
  steps=["Central Office → Regional Offices (compounding)"],
  why="Compounding stays with RBI; ADs, ED and SEBI were not given this power.",
  current=ca("2026-10-23"),
  facts=[fact("Powers to compound contraventions relating to overseas investment, borrowing and lending, and "
              "guarantee transactions delegated from Central Office to Regional Offices as a measure for promoting "
              "customer service (circular of October 23, 2026)", COMPOUND)])
Q(T, SUB, "Intermediate",
  "The Foreign Exchange Management (Export and Import of Goods and Services) (Second Amendment) Regulations, 2026, "
  "notified on 2 November 2026 with effect from 1 October 2026, provide that a service exporter who is a resident "
  "individual:",
  ["Is deemed to have submitted the EDF once he gives his AD bank the payment-receipt details needed to credit his "
   "account", "Must file a separate EDF for every invoice regardless of value", "Is exempt from realising export "
   "proceeds", "Must route all receipts through RBI"],
  concept="Simplified EDF for service exporters",
  explanation="The amendment adds a definition of 'resident individual' and provides that such a service exporter is "
              "deemed to have submitted the Export Declaration Form once he furnishes the information required by the "
              "AD to credit the payment to his account.",
  steps=["Resident individual service exporter → deemed EDF on furnishing receipt details to AD"],
  why="The amendment removes a separate filing step; it does not exempt realisation or route receipts through RBI.",
  current=ca("2026-11-02"),
  facts=[fact("An exporter of services who is a resident individual shall be deemed to have submitted the EDF once "
              "information required by the AD to credit the payment receipt to the account is furnished; regulations "
              "dated November 02, 2026 come into force from October 01, 2026", FEMA_EXP)])
Q(T, SUB, "Intermediate",
  "In June 2026 RBI expanded the universe of government securities under the Fully Accessible Route (FAR) for "
  "non-residents. What was added?",
  ["All new issuances of 15-, 30- and 40-year G-secs", "All State Development Loans", "All Treasury Bills",
   "All corporate bonds rated AAA"],
  concept="FAR for foreign investment in G-secs",
  explanation="The Governor announced that all new issuances of 15-, 30- and 40-year tenor G-secs would be included "
              "under FAR, and that short-term, concentration and individual-security limits on FPI investment under "
              "the General Route would be removed.",
  steps=["FAR expanded: new 15-, 30-, 40-year G-secs"],
  why="SDLs, T-bills and corporate bonds were not the additions announced.",
  current=ca(JUN26),
  facts=[fact("For government securities under the Fully Accessible Route, the universe is expanded by including all "
              "new issuances of 15-, 30- and 40-year tenor G-secs", GOV_JUN26)])
Q(T, SUB, "Intermediate",
  "To encourage foreign currency inflows, which facilities did the RBI Governor announce on 5 June 2026, available "
  "till 30 September 2026?",
  ["A concessional forex swap for ECBs raised by PSUs, and full hedging-cost support to AD banks for fresh 3–5-year "
   "FCNR(B) deposits", "A tax holiday on all NRE deposits", "Interest-free loans to exporters",
   "Removal of CRR on all foreign currency deposits permanently"],
  concept="Measures to attract foreign currency",
  explanation="The Governor announced a concessional forex swap facility till 30 September 2026 to incentivise ECBs by "
              "PSUs, and a facility to bear the full hedging cost for AD banks raising fresh 3–5-year FCNR(B) deposits "
              "till the same date.",
  steps=["PSU ECBs → concessional forex swap", "Fresh 3–5-year FCNR(B) → full hedging cost borne"],
  why="Tax holidays, interest-free loans and a permanent CRR removal were not announced.",
  current=ca(JUN26),
  facts=[fact("A facility of concessional forex swap will be provided till 30th September 2026 to incentivize ECBs by "
              "PSUs; a similar facility for bearing the full hedging cost to AD banks for raising fresh 3-5-year "
              "FCNR(B) deposits", GOV_JUN26)])
Q(T, SUB, "Advanced",
  "Consider the following statements about RBI's amendment directions of 19 October 2026 for commercial banks and "
  "small finance banks:\n"
  "I. They deleted the section on 'Limits for Non-Option Derivative Contracts' from the respective Miscellaneous "
  "Directions, 2025.\n"
  "II. They were issued under Section 35A of the Banking Regulation Act, 1949.\n"
  "III. They take effect from 1 April 2027.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Recent amendment directions",
  explanation="The Commercial Banks – Miscellaneous Second Amendment Directions and the SFB – Miscellaneous Amendment "
              "Directions of 19 October 2026 deleted paragraph 37 ('Limits for Non-Option Derivative Contracts') (I), "
              "were issued under Section 35A of the BR Act (II), and came into effect immediately on issue (III "
              "wrong).",
  steps=["I: correct", "II: correct", "III: wrong (effective immediately)"],
  why="III misstates the effective date; 'I only' omits II.",
  current=ca("2026-10-19"),
  facts=[fact("Section C 'Limits for Non-Option Derivative Contracts' (paragraph 37) stands deleted; issued under "
              "section 35A of the Banking Regulation Act, 1949; effective immediately upon issuance (October 19, "
              "2026)", CB_MISC),
         fact("SFB Miscellaneous Directions: paragraph 37, limits for non-option derivative contracts, stands deleted, "
              "effective immediately", SFB_MISC)])

receipts = {"P": ("resident individual", 25.0), "Q": ("company", 8.0), "R": ("company", 12.0)}
deemed = sorted(k for k, (who, lakh) in receipts.items() if who == "resident individual" or lakh <= 10)
assert deemed == ["P", "Q"]
Q(T, SUB, "Advanced",
  "Under the FEMA (Export and Import of Goods and Services) Second Amendment Regulations, 2026 (effective 1 October "
  "2026), for which of these service exporters is the EDF deemed submitted once the AD has the details needed to "
  "credit the receipt?\n"
  "P. A resident individual freelancer receiving ₹25 lakh for one assignment\n"
  "Q. A company receiving an inward remittance of ₹8 lakh for a service\n"
  "R. A company receiving an inward remittance of ₹12 lakh for a service",
  ["P and Q only", "P only", "Q and R only", "P, Q and R"],
  concept="Deemed EDF thresholds",
  explanation="Resident individuals get deemed submission regardless of amount (P). Other exporters get it only if the "
              "inward remittance for the service is not more than ₹10 lakh: Q (₹8 lakh) qualifies, R (₹12 lakh) does "
              "not.",
  steps=["P: resident individual → deemed", "Q: 8 ≤ 10 lakh → deemed", "R: 12 > 10 lakh → not deemed"],
  why="R exceeds ₹10 lakh; P is covered without any threshold.",
  computed=True, current=ca("2026-11-02"),
  facts=[fact("Exporter of services other than a resident individual deemed to have submitted the EDF only where the "
              "inward remittance for the service is not more than ₹10 Lakh; resident individuals deemed on furnishing "
              "the payment-receipt information", FEMA_EXP)])


# ================================================================= checks and output
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_004_plan.json").read_text(encoding="utf-8"))
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
assert all(0 <= i < len(questions) for i in INDEPENDENT)

# ---------------------------------------------------------------- superseded-rules audit (2026-11-06)
# These questions were rewritten to the current rule, or reframed as historical (dated, past tense), after checking
# current RBI/SEBI/Government texts on 2026-11-06. IDs, topics, subtopics, difficulty and keys are unchanged. Any
# earlier ai:independent-check is dropped because the revised wording has not been re-solved blind.
AUDIT_REVISED = {"BANK_BFA_000614", "BANK_BFA_000615", "BANK_BFA_000641", "BANK_BFA_000683", "BANK_BFA_000712", "BANK_BFA_000713", "BANK_BFA_000714", "BANK_BFA_000715", "BANK_BFA_000716", "BANK_BFA_000718", "BANK_BFA_000749", "BANK_BFA_000750", "BANK_BFA_000751", "BANK_BFA_000757", "BANK_BFA_000776", "BANK_BFA_000778", "BANK_BFA_000788", "BANK_BFA_000792", "BANK_BFA_000793"}
assert AUDIT_REVISED <= {q["question_id"] for q in questions}
for q in questions:
    if q["question_id"] in AUDIT_REVISED:
        v = q["verification"]
        v["verified_by"] = [x for x in v["verified_by"] if x != "ai:independent-check"]
        v["verified_at"] = AUDIT_DAY

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_004",
    "created_at": TODAY,
    "notes": "BATCH_004 Banking and Financial Awareness part: 200 original questions (60 Basic, 80 Intermediate, "
             "60 Advanced) across 32 topics, IDs BANK_BFA_000604 to BANK_BFA_000803. Built mostly from primary texts "
             "opened on 2026-11-05: RBI history chronologies, list of Governors, Organisation page, table of Bank "
             "Rate/CRR/SLR changes; Master Directions on KYC, IRAC and PSL; circulars on customer liability (2017), "
             "stressed assets (2019), external benchmarks (2019), DBUs (2022), BCs (2010), SFB transition (2024), "
             "SLR glide path (2018), microfinance risk weights (2025), call/notice/term money (2021); October 2026 "
             "amendment directions and FEMA notices; RBI FAQs (NBFCs, NEFT, RTGS, e-rupee, RB-IOS 2026); MPC and "
             "Governor's statements of May 2022, June 2025, June 2026 and October 2026; money market operations of 6 "
             "October 2026; WMA and ₹2000-note releases; D-SIB list 2025; Payment System Report (released 18 May "
             "2026) and payments booklet; IBBI CIRP FAQs; BIS history; SEBI circular on MF categorisation; SEBI "
             "investor pages; LIC history; DFS PMJDY page; Indian Bank's PM Vishwakarma page; PIB Budget 2026-27 "
             "compilation. Facts available only through search results (NPCI, PIB/pmindia, rbidocs PDFs and some "
             "news-only facts; no workaround attempted) are marked web:search-confirmed. Only changeable values and "
             "dated events carry current_affairs, with the event or release date from the source. Computed answers "
             "are re-derived in tools/batch_004/banking.py. Facts tested in BATCH_000–BATCH_003 are not repeated. "
             "ai:independent-check marks only the questions a separate solver answered blind and got right.",
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_004_BFA.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions; keys {dict(sorted(_keys.items()))}; "
      f"current_affairs {sum('current_affairs' in q for q in questions)}; independent {len(INDEPENDENT)})")
