"""Writes batches/parts/BATCH_005_BFA.json: the 200 Banking and Financial Awareness questions of BATCH_005.

Every fact is backed by at least one fact_check whose source was opened on 2026-11-05 (fetched with a plain client and
read; PDFs were downloaded and their text extracted), or, where only search results stated it (NPCI circulars, some
news-only facts, RBI pages that could not be read; no block was worked around), by search results, in which case the
question carries web:search-confirmed. Only questions whose answer can change or that report a dated event carry a
current_affairs block, and its event_date is the date of that event or release as stated by the source (Repo Rate and
Budget questions always carry one, as the validator requires). Every computable answer is re-derived below with
assertions, the quota per (topic, difficulty) is checked against the batch plan, and the answer keys are balanced.
ai:independent-check is added only to the questions listed in INDEPENDENT, which a separate fresh solver answered
blind (stem and options only, no key) and got right with confidence. If any check fails, nothing is written. All ~800
earlier Banking stems and answers (BATCH_000 to BATCH_004) were read first; their facts, and neighbouring steps of the
schedules they tested, are not repeated.

    python tools/batch_005/banking.py      (run from anywhere)
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
TODAY = "2026-11-05"
REVIEW_BY = "2027-05-05"
LETTERS = "ABCD"
BF = "Banking and Financial Awareness"
FIRST_ID = 804
SECONDS = {"Basic": 20, "Intermediate": 30, "Advanced": 60}

_rng = random.Random(2026110505)
_keys = Counter()
questions = []

# Question numbers (offset from BANK_BFA_000804, i.e. 0 = 000804) that a separate fresh solver answered blind (stem
# and options only, no key or solution) and matched the key with high confidence. 100 questions (the even offsets 0-198)
# were given; 73 matched with high confidence and are tagged. 24 matches with medium/low confidence are not tagged.
# Three answers differed: 28 (solver used the pre-2018 65% note-refund threshold; key follows the 2018 rule on RBI's
# FAQ), 58 (statement II was reworded after the solver noted later extensions; not tagged) and 164 (solver used the
# old ₹30 lakh Insurance Ombudsman limit; key follows the ₹50 lakh limit on cioins.co.in). Question 172 was replaced
# after the solver noted that SEBI's 2024 nomination rule had changed; it is not tagged.
INDEPENDENT = {4, 6, 8, 12, 14, 18, 20, 22, 24, 26, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 60,
               62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 96, 98, 104, 106, 108, 110, 112, 114, 116, 118,
               120, 124, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, 154, 156, 158, 162, 166, 168, 170, 174,
               176, 178, 186, 190, 196}

# ---------------------------------------------------------------- sources
# Opened (fetched and read) on 2026-11-05
_F = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id="
_P = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid="
CHRON_35 = "https://rbi.org.in/history/Brief_Chro1935to1949.html"
CHRON_50 = "https://rbi.org.in/history/Brief_Chro1950to1960.html"
CHRON_60 = "https://rbi.org.in/history/Brief_Chro1960to1971.html"
CHRON_68 = "https://rbi.org.in/history/Brief_Chro1968to1985.html"
CHRON_85 = "https://rbi.org.in/history/Brief_Chro1985to1991.html"
CHRON_91 = "https://rbi.org.in/history/Brief_Chro1991to2000.html"
CHRON_00 = "https://rbi.org.in/history/Brief_Chro2000_Onwards.html"
RATES_HIST = "https://www.rbi.org.in/commonman/english/history/Scripts/BankrateCRRandSLRChanges.aspx"
ORG = "https://www.rbi.org.in/commonman/english/Scripts/Organisation.aspx"
CUR_FAQ = _F + "136"
CHQ_FAQ = _F + "175"
GOVBANK_FAQ = _F + "61"
SGB_FAQ = _F + "109"
NCB_FAQ = _F + "49"
GSEC_FAQ = _F + "79"
RTGS_FAQ = _F + "65"
ARC_FAQ = _F + "179"
PSL_FAQ = _F + "87"
PPI_FAQ = _F + "126"
ATM_FAQ = _F + "75"
PSS_FAQ = _F + "73"
UDGAM_FAQ = _F + "166"
PAYTM_FAQ = _F + "164"
RBIOS_FAQ = _F + "153"
ERUPEE_FAQ = _F + "169"
NEFT_FAQ = _F + "60"
IRAC_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13146"
STRESS = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11580&Mode=0"
PAY_BOOKLET = "https://www.rbi.org.in/scripts/PublicationsView.aspx?Id=20315"
AR_2021 = "https://www.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1326"
MPC_MAY20 = "https://rbi.org.in/commonman/English/Scripts/PressReleases.aspx?Id=3220"
BR_2012 = _P + "25954"
RTGS_2020 = _P + "50775"
PB_GUIDE = _P + "32615"
SFB_GUIDE = _P + "32614"
MPC_DEC25 = _P + "61749"
GOV_DEC25 = _P + "61750"
MPC_FEB26 = _P + "62169"
GOV_FEB26 = _P + "62170"
SDRP_FEB26 = _P + "62171"
ASSAM = _P + "62180"
MPC_AUG26 = _P + "63287"
GOV_AUG26 = _P + "63288"
NBFC_UL = _P + "63301"
MPC_OCT26 = _P + "63742"
GOV_OCT26 = _P + "63744"
CVA = _P + "63749"
LEND_RATES = _P + "63894"
VRRR_NOV4A = _P + "63913"
TCCFM = _P + "63914"
VRRR_NOV4B = _P + "63916"
TBILL_NOV4 = _P + "63917"
CAP_LR = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13743&Mode=0"
OPRISK = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13744&Mode=0"
NDDC = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13739&Mode=0"
BUDGET = "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc202621776101.pdf"
PMJDY12 = "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/aug/doc_9716_20260827_14055201.pdf"
PMJJBY = "https://financialservices.gov.in/pmjjby"
SIDBI_ECO = "https://sidbi.in/ecosystem"
CIO_FAQ = "https://cioins.co.in/Faqs"
SEBI_SEP26 = "https://www.sebi.gov.in/sebi_data/attachdocs/sep-2026/1790259036651.pdf"
SEBI_DABBA = "https://investor.sebi.gov.in/dabba_trading.html"
SEBI_ASBA = "https://investor.sebi.gov.in/ipo_through_asba.html"
SEBI_WIW = "https://investor.sebi.gov.in/wiw-2026/wiw-2026.html"
SEBI_SME = "https://investor.sebi.gov.in/advisory-investment-in-sme-segment.html"
SEBI_CAS = "https://investor.sebi.gov.in/consolidated_account_statement.html"

# Confirmed only through search results (official page not fetchable/readable, or only news coverage found)
SDF_2022 = "https://www.informistmedia.com/rbi-policy-introduces-sdf-at-3-75-restores-laf-corridor-to-50-bps/"
REPO_FEB23 = "https://taxmann.com/post/blog/rbi-increases-repo-rate-by-25-basis-points-to-6-50-revises-sdf-msf-rate"
WPI_SEP26 = "https://www.psuconnect.in/news/wpi-inflation-rises-to-11-39-in-september-2026"
UPI_COLLECT = ("https://www.businesstoday.in/personal-finance/banking/story/npci-to-tighten-upi-rules-peer-to-peer-"
               "collect-feature-to-end-in-october-489244-2025-08-13")
UPI_LIMITS = ("https://www.lokmattimes.com/national/upi-transaction-limit-increased-to-rs10-lakh-for-select-payments-"
              "from-september-15-a525")
TPAP_CAP = ("https://www.businesstoday.in/tech-today/news/story/npci-extends-30-upi-market-share-cap-deadline-on-3rd-"
            "party-apps-to-december-2026-459171-2024-12-31")
ERUPI = ("https://www.mondaq.com/india/fin-tech/1106822/e-rupi-and-its-benefits-for-the-digital-payments-ecosystem-"
         "in-india")
IRDAI_HEALTH = ("https://www.businesstoday.in/personal-finance/insurance/story/health-insurance-irdai-sets-3-hour-time-"
                "limit-for-insurers-to-clear-cashless-claims-details-here-431354-2024-05-29")
SEBI_JUN26 = ("https://www.businesstoday.in/personal-finance/investment/story/sebis-big-ease-of-doing-business-push-9-"
              "key-decisions-that-could-impact-investors-538169-2026-06-20")
ECLGS = ("https://www.businesstoday.in/news-reel/video/eclgs-credit-line-enhanced-to-rs-5-lakh-crore-fm-321125-"
         "2022-02-01")
SEARCH_ONLY = {SDF_2022, REPO_FEB23, WPI_SEP26, UPI_COLLECT, UPI_LIMITS, TPAP_CAP, ERUPI, IRDAI_HEALTH, SEBI_JUN26,
               ECLGS}

# Release / event dates taken from the sources
OCT26 = "2026-10-07"
AUG26 = "2026-08-05"
FEB26 = "2026-02-06"
DEC25 = "2025-12-05"
BUDGET_DAY = "2026-02-01"


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


def pct(a, b):
    return 100 * a / b


# ================================================================= 1. Banking Fundamentals (4 / 5 / 3)
T = "Banking Fundamentals"
Q(T, "Cheques and instruments", "Basic",
  "Separate clearing sessions for non-CTS cheques were discontinued with effect from 31 December 2018. According to "
  "RBI, what is the status of a non-CTS cheque today?",
  ["It cannot be presented in CTS clearing but remains valid as a negotiable instrument",
   "It is void and cannot be used for any purpose", "It can be cleared only through a separate weekly session",
   "It can be presented in CTS if the drawer counter-signs it"],
  concept="CTS-2010 standard cheques",
  explanation="Banks were advised to issue only CTS-2010 compliant cheques from 30 September 2012, and separate "
              "clearing sessions for non-CTS cheques ended on 31 December 2018. Non-CTS cheques cannot be presented "
              "in CTS, but such a cheque continues to be valid as a negotiable instrument.",
  steps=["Non-CTS sessions ended 31 December 2018", "Cannot be presented in CTS", "Still a valid negotiable instrument"],
  why="RBI does not call them void; no weekly session or counter-signature route exists.",
  facts=[fact("Separate clearing sessions for non-CTS cheques were discontinued with effect from December 31, 2018; "
              "non-CTS cheques cannot be presented in CTS; however, a non-CTS cheque continues to be valid as a "
              "negotiable instrument", CHQ_FAQ)])
Q(T, "Cheques and instruments", "Basic",
  "With effect from 13 October 2023, the three CTS grids (New Delhi, Chennai and Mumbai) were merged into a National "
  "Grid. Where is the National Grid Clearing House (NGCH) that manages it?",
  ["Chennai", "Mumbai", "New Delhi", "Nagpur"],
  concept="National Grid for cheque clearing",
  explanation="RBI's cheque-clearing FAQs state that the three CTS grids were merged with effect from 13 October 2023 "
              "to form a National Grid managed by the National Grid Clearing House (NGCH), Chennai.",
  steps=["Three grids merged on 13 October 2023", "Managed by NGCH, Chennai"],
  why="Mumbai and New Delhi were earlier grid locations, not the NGCH; Nagpur houses RBI's Central Accounts Section.",
  facts=[fact("With effect from October 13, 2023, the three grids were merged to form a National Grid managed by "
              "National Grid Clearing House (NGCH), Chennai", CHQ_FAQ)])
Q(T, "Cheques and instruments", "Basic",
  "Under the Cheque Truncation System the physical cheque stays with the presenting bank. For how long must the "
  "presenting bank preserve the physical instruments to meet legal requirements?",
  ["10 years", "3 years", "5 years", "8 years"],
  concept="Preservation of truncated cheques",
  explanation="Physical cheques do not move to the paying bank under CTS. To meet legal requirements, the presenting "
              "banks that truncate the cheques must preserve the physical instruments for 10 years.",
  steps=["Truncated cheque stays with presenting bank", "Preservation period: 10 years"],
  why="3, 5 and 8 years are not the period stated by RBI.",
  facts=[fact("To meet legal requirements, the presenting banks, which truncate the cheques, need to preserve the "
              "physical instruments for a period of 10 years", CHQ_FAQ)])
Q(T, "Types of accounts", "Basic",
  "Which law, which came into force on 12 January 1984, provided nomination facilities to bank account holders for "
  "the first time and also widened the activities banks could undertake, such as leasing?",
  ["Banking Laws (Amendment) Act, 1983", "Banking Regulation Act, 1949", "Banking Companies (Acquisition and "
   "Transfer of Undertakings) Act, 1970", "Deposit Insurance Corporation Act, 1961"],
  concept="Origin of nomination in bank accounts",
  explanation="RBI's chronology records that the Banking Laws (Amendment) Act, 1983, which came into force on 12 "
              "January 1984, widened banks' activities (such as leasing), provided nomination facilities to account "
              "holders and strengthened RBI's powers.",
  steps=["12 January 1984 → Banking Laws (Amendment) Act, 1983", "Introduced nomination; widened activities"],
  why="The 1949 Act is the base law; the 1970 Act nationalised banks; the 1961 Act set up deposit insurance.",
  facts=[fact("12 Jan 1984: Banking Laws (Amendment) Act, 1983 widened the activities that banks could undertake "
              "(such as leasing), provided nomination facilities to account holders, strengthened the powers of the "
              "Reserve Bank", CHRON_68)])
Q(T, "Types of accounts", "Intermediate",
  "A savings account holder of Bank A uses ATMs of other banks in Hyderabad. Under RBI's ATM rules, how many free "
  "transactions in a month must Bank A at least allow him at these other-bank ATMs?",
  ["Three, including financial and non-financial transactions",
   "Five financial transactions, with non-financial ones free",
   "Five, including financial and non-financial transactions", "Unlimited, since ATMs are interoperable"],
  concept="Free ATM transactions",
  explanation="At other banks' ATMs in the six metro locations (Bengaluru, Chennai, Hyderabad, Kolkata, Mumbai, New "
              "Delhi), banks must offer at least three free transactions a month, financial and non-financial "
              "together. At non-metro locations the minimum is five; at the bank's own ATMs it is five free "
              "financial transactions.",
  steps=["Hyderabad is one of the six metro locations", "Off-us at metro → minimum 3 free (financial + "
         "non-financial)"],
  why="Five applies to non-metro off-us ATMs or own-bank ATMs; free use is not unlimited.",
  facts=[fact("In case of ATMs located in six metro locations, viz. Bengaluru, Chennai, Hyderabad, Kolkata, Mumbai, "
              "and New Delhi, banks shall offer their savings bank account holders a minimum of three free "
              "transactions (including financial and non-financial transactions) in a month", ATM_FAQ)])
Q(T, "Types of accounts", "Intermediate",
  "A customer's account is debited for an ATM cash withdrawal, but no cash is dispensed. Within what maximum time "
  "must the card-issuing bank re-credit the account, as per RBI?",
  ["T+5 calendar days, where T is the day of the transaction", "T+1 working day", "Within 30 days of a complaint",
   "Within 90 days of the transaction"],
  concept="Failed ATM transactions",
  explanation="Banks must reverse failed ATM/WLA transactions on their own; RBI has mandated that the customer's "
              "account be re-credited within a maximum of T+5 calendar days.",
  steps=["Failed ATM debit → auto-reversal", "Maximum: T+5 calendar days"],
  why="T+1, 30 days and 90 days are not the prescribed limit.",
  facts=[fact("In the case of a failed ATM transaction, the banks have been mandated to re-credit the customer's "
              "account within a maximum of T+5 calendar days (where 'T' is the day of transaction)", ATM_FAQ)])
Q(T, "Cheques and instruments", "Intermediate",
  "A customer has written the wrong amount in words on a cheque. Under the Cheque Truncation System, what should "
  "she do?",
  ["Use a fresh cheque leaf, because cheques with alterations are not accepted in CTS",
   "Strike out the words and countersign the change", "Write the correction on the back and sign it",
   "Ask the bank to correct it after scanning"],
  concept="No alterations under CTS",
  explanation="RBI's cheque-clearing FAQs say cheques with alterations are not accepted under CTS. Apart from date "
              "validation, no change can be made; for a change in payee name, amount in figures or amount in words, a "
              "fresh cheque leaf must be used.",
  steps=["CTS rejects altered cheques", "Only date validation is allowed", "Use a fresh leaf"],
  why="Countersigned or back-side corrections and post-scan correction are not permitted.",
  facts=[fact("Cheques with alteration / modification are not accepted under CTS; no changes / corrections can be "
              "carried out on the cheques (other than for date validation purposes); for any change in the payee's "
              "name, courtesy amount or legal amount, fresh cheque leaves should be used", CHQ_FAQ)])
Q(T, "Cheques and instruments", "Intermediate",
  "According to RBI's chronology, an Ordinance of July 1981 barred companies, co-operative societies and firms from "
  "repaying any deposit of ₹10,000 or more otherwise than by:",
  ["An account payee cheque or bank draft", "Cash against a signed receipt", "A bearer cheque",
   "Postal money order"],
  concept="Repayment of deposits through banking channels",
  explanation="The July 1981 Ordinance prohibited companies (including banking companies), co-operative societies and "
              "firms from repaying any deposit otherwise than by an account payee cheque or bank draft when the "
              "repayment amounted to ₹10,000 or more.",
  steps=["July 1981 Ordinance", "Repayment ≥ ₹10,000 → account payee cheque / bank draft only"],
  why="Cash, bearer cheques and money orders were exactly what the rule sought to avoid.",
  facts=[fact("11 July 1981: Ordinance prohibiting companies (including Banking Companies), cooperative societies, "
              "firms, to repay any person any deposit otherwise than by an account payee cheque / bank draft when "
              "such repayment amounted to Rs. 10,000 or more", CHRON_68)])
Q(T, "Types of banks", "Intermediate",
  "Which specialised bank was established on 1 January 1982 to provide a comprehensive package of financial and "
  "allied services to exporters and importers?",
  ["Export-Import Bank of India", "Industrial Development Bank of India", "Small Industries Development Bank of "
   "India", "National Housing Bank"],
  concept="Development financial institutions",
  explanation="RBI's chronology records the establishment of the Export Import Bank of India on 1 January 1982 to "
              "provide comprehensive financial and allied services to exporters and importers.",
  steps=["1 January 1982 → EXIM Bank"],
  why="IDBI dates from 1964, SIDBI from 1990 and NHB from 1988.",
  facts=[fact("01 Jan 1982: Export Import Bank of India established with the objective of providing comprehensive "
              "package of financial and allied services to exporters and importers", CHRON_68)])

own, own_free, metro_off, metro_free, fee = 6, 5, 5, 3, 23
charge = ((own - own_free) + (metro_off - metro_free)) * fee
assert charge == 69
Q(T, "Types of accounts", "Advanced",
  "In one month, a savings account holder of Bank X in Chennai makes 6 cash withdrawals at Bank X's own ATMs and 5 "
  "transactions (cash withdrawals and balance enquiries) at other banks' ATMs in Chennai. Assuming Bank X allows only "
  "the minimum free transactions and charges the maximum permitted fee, what is the most it can charge (excluding "
  "taxes)?",
  ["₹69", "₹46", "₹23", "₹115"],
  concept="Free ATM transactions and charges",
  explanation="At its own ATMs a bank must allow at least five free financial transactions a month, so the sixth "
              "withdrawal is chargeable. At other banks' ATMs in a metro (Chennai), the minimum is three free "
              "transactions including non-financial ones, so two of the five are chargeable. The charge cannot exceed "
              "₹23 per transaction: 3 × ₹23 = ₹69.",
  steps=["Own ATM: 6 − 5 free = 1 chargeable", "Other-bank ATM in metro: 5 − 3 free = 2 chargeable",
         "3 × ₹23 = ₹69"],
  why="₹46 ignores the sixth own-ATM withdrawal; ₹23 counts only one chargeable transaction; ₹115 charges all five "
      "other-bank ATM transactions.",
  computed=True,
  facts=[fact("Banks should offer their savings bank account holders a minimum of five free financial transactions "
              "in a month at own ATMs; minimum of three free transactions at other banks' ATMs in six metro "
              "locations; charges cannot exceed a maximum of Rs. 23 per transaction (plus applicable taxes)",
              ATM_FAQ)])
Q(T, "Cheques and instruments", "Advanced",
  "Consider the following statements about the Cheque Truncation System, as described in RBI's FAQs of January "
  "2026:\n"
  "I. Three images of each cheque are captured: front grey scale, front black-and-white and back black-and-white.\n"
  "II. RBI has prescribed specific ink colours that customers must use to write cheques.\n"
  "III. Under continuous clearing, presenting banks release the payment to customers within one hour of successful "
  "settlement, subject to usual safeguards.\n"
  "Which of the above is/are correct?",
  ["I and III only", "I only", "II and III only", "I, II and III"],
  concept="CTS operations",
  explanation="CTS captures three images of each cheque (I correct). Customers should use image-friendly, permanent "
              "ink, but RBI has not prescribed specific ink colours (II wrong). Under continuous clearing, after "
              "settlement the presenting bank releases payment within one hour, subject to usual safeguards (III "
              "correct).",
  steps=["I: correct", "II: wrong (no prescribed colour)", "III: correct"],
  why="Any option including II is wrong; 'I only' omits III.",
  facts=[fact("There are three images of each cheque that are taken in CTS – front Gray Scale, front Black and White "
              "and back Black and White; RBI has not prescribed specific ink colours to be used to write cheques",
              CHQ_FAQ),
         fact("Presenting banks will release the payment to the customers within one hour of the successful "
              "settlement, subject to usual safeguard", CHQ_FAQ)])
Q(T, "Types of banks", "Advanced",
  "The State Bank of India (Subsidiary Banks) Act, 1959 made banks of erstwhile princely states subsidiaries of SBI. "
  "Which statement about these banks is correct?",
  ["The Bank of Bikaner and the Bank of Jaipur were amalgamated in 1963 to form the State Bank of Bikaner and Jaipur",
   "The Bank of Mysore and the Bank of Travancore were amalgamated in 1963 to form the State Bank of Mysore",
   "The Bank of Patiala and the Bank of Indore were amalgamated in 1963 to form the State Bank of Patiala",
   "Only three banks became subsidiaries under the 1959 Act"],
  concept="SBI's subsidiary banks",
  explanation="Under the 1959 Act, the Bank of Bikaner, Bank of Jaipur, Bank of Indore, Bank of Mysore, Bank of "
              "Patiala, Bank of Hyderabad, Bank of Saurashtra and Bank of Travancore became SBI subsidiaries. The Bank "
              "of Bikaner and the Bank of Jaipur were amalgamated in 1963 to form the State Bank of Bikaner and "
              "Jaipur.",
  steps=["1959 Act → eight subsidiaries", "1963 → Bikaner + Jaipur = State Bank of Bikaner and Jaipur"],
  why="No 1963 merger of Mysore with Travancore or Patiala with Indore took place; eight, not three, banks were made "
      "subsidiaries.",
  facts=[fact("State Bank of India (Subsidiary Banks) Act, 1959 made the banks of the erstwhile Princely States "
              "subsidiaries of SBI (Bikaner, Jaipur, Indore, Mysore, Patiala, Hyderabad, Saurashtra, Travancore); "
              "the Bank of Bikaner and the Bank of Jaipur were amalgamated in 1963 to form the State Bank of Bikaner "
              "and Jaipur", CHRON_50)])

# ================================================================= 2. History of Banking in India (1 / 3 / 1)
T = "History of Banking in India"
Q(T, "Nationalisation", "Basic",
  "The 14 banks nationalised on 19 July 1969 were Indian scheduled commercial banks with deposits of over:",
  ["₹50 crore", "₹200 crore", "₹25 crore", "₹100 crore"],
  concept="1969 nationalisation threshold",
  explanation="RBI's chronology records that the 14 major Indian scheduled commercial banks with deposits of over "
              "₹50 crore were nationalised on 19 July 1969.",
  steps=["1969 → deposits above ₹50 crore → 14 banks"],
  why="₹200 crore relates to the 1980 round; ₹25 crore and ₹100 crore are not the 1969 threshold.",
  facts=[fact("19 Jul 1969: 14 major Indian Scheduled Commercial Banks with deposits of over Rs 50 crores "
              "nationalised", CHRON_68)])
Q(T, "Nationalisation", "Intermediate",
  "On 10 February 1970 the Supreme Court held the 1969 bank nationalisation law void. How was nationalisation "
  "then given effect?",
  ["A fresh Ordinance on 14 February 1970, later replaced by the Banking Companies (Acquisition and Transfer of "
   "Undertakings) Act, 1970", "By an amendment to the RBI Act, 1934 transferring the banks to RBI",
   "By a constitutional amendment passed in 1972", "The banks were returned to private owners until 1980"],
  concept="Legal history of nationalisation",
  explanation="The Supreme Court found the Act discriminatory against the 14 banks and the compensation unfair. A "
              "fresh Ordinance was issued on 14 February 1970 and later replaced by the Banking Companies "
              "(Acquisition and Transfer of Undertakings) Act, 1970 (5 of 1970).",
  steps=["10 Feb 1970: Act held void", "14 Feb 1970: fresh Ordinance", "Replaced by the 1970 Act"],
  why="Nationalisation was not routed through the RBI Act, a 1972 constitutional amendment or a reversal.",
  facts=[fact("On February 10, 1970 the Supreme Court held the Act void; a fresh Ordinance was issued on February 14 "
              "which was later replaced by the Banking Companies (Acquisition and Transfer of Undertakings) Act, "
              "1970", CHRON_68)])
Q(T, "Nationalisation", "Intermediate",
  "Before the 1969 nationalisation, the Government introduced 'social controls' over banks in December 1967. "
  "Which body was set up on 22 December 1967 as a forum to assess credit priorities on an all-India basis?",
  ["National Credit Council", "Agricultural Credit Board", "Banks Board Bureau", "State Level Bankers' Committee"],
  concept="Social controls over banks",
  explanation="Social controls were introduced in December 1967 to align banking with economic policy. The National "
              "Credit Council, set up on 22 December 1967, was a forum to discuss and assess credit priorities and to "
              "assist RBI and the Government in allocating credit.",
  steps=["Dec 1967 → social controls", "22 Dec 1967 → National Credit Council"],
  why="The Agricultural Credit Board came in 1970, SLBCs in 1971 and the Banks Board Bureau in 2016.",
  facts=[fact("Dec 1967: Introduction of Social Controls over banks; 22 Dec 1967: National Credit Council set up to "
              "provide a forum to discuss and assess credit priorities on an all India basis", CHRON_68)])
Q(T, "Mergers and consolidation", "Intermediate",
  "From 1960, RBI acquired powers for reconstruction and compulsory amalgamation of weak banks. According to RBI's "
  "chronology, roughly how many banks were merged or liquidated between 1960 and 1982?",
  ["Over 200", "About 50", "About 14", "Over 1,000"],
  concept="Early consolidation of Indian banking",
  explanation="RBI's chronology says the policy of reconstruction/compulsory amalgamation introduced in 1960 (with "
              "powers acquired through an RBI Act amendment) led to over 200 banks being merged or liquidated between "
              "1960 and 1982.",
  steps=["1960 → compulsory amalgamation policy", "1960–1982 → over 200 banks merged or liquidated"],
  why="14 is the number nationalised in 1969; 50 and 1,000 do not match the record.",
  facts=[fact("1960: Policy of reconstruction / compulsory amalgamation of banks introduced to consolidate the "
              "Banking sector; between 1960 to 1982 over 200 banks were merged or liquidated", CHRON_60)])
Q(T, "Committees", "Advanced",
  "Consider the following statements:\n"
  "I. The Banking Commission set up on 29 January 1969 was asked to report on banking costs, legislation affecting "
  "banking, indigenous banking, bank procedures and non-banking financial intermediaries.\n"
  "II. Recommendations made in April 1998 on harmonising the roles of development financial institutions and banks "
  "paved the way for universal banking in India.\n"
  "III. The Banking Commission of 1969 was constituted by RBI under the Banking Regulation Act.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Committees and commissions",
  explanation="The Banking Commission of 29 January 1969 had the terms of reference in I, but it was set up by the "
              "Government of India, not RBI (III wrong). RBI's chronology records that the April 1998 "
              "recommendations on harmonising the roles of DFIs and banks paved the way for universal banking (II).",
  steps=["I: correct", "II: correct", "III: wrong (set up by GoI)"],
  why="III is wrong, so any option including it fails; 'I only' omits II.",
  facts=[fact("29 Jan 1969: Setting up of the Banking Commission by GOI to report on banking costs, legislations "
              "affecting banking, indigenous banking, bank procedures, non banking financial intermediaries",
              CHRON_68),
         fact("Apr 1998: Recommendations on the harmonisation of the Role and Operations of Development Financial "
              "Institutions and Banks paved the way for universal banking in India", CHRON_91)])


# ================================================================= 3. Reserve Bank of India (3 / 3 / 2)
T = "Reserve Bank of India"
Q(T, "Governors and leadership", "Basic",
  "RBI was nationalised on 1 January 1949. Who was the Governor of RBI at that time?",
  ["Sir C. D. Deshmukh", "Sir Benegal Rama Rau", "Sir James Taylor", "H. V. R. Iengar"],
  concept="RBI Governors in the 1940s",
  explanation="Sir C. D. Deshmukh assumed office on 11 August 1943. RBI was nationalised on 1 January 1949, and Sir "
              "Benegal Rama Rau took over only on 1 July 1949, so Deshmukh was Governor at nationalisation.",
  steps=["Deshmukh: from 11 Aug 1943", "Nationalisation: 1 Jan 1949", "Rama Rau: from 1 Jul 1949"],
  why="Rama Rau came after July 1949, Taylor before 1943 and Iengar in 1957.",
  facts=[fact("11 Aug 1943: Sir C. D. Deshmukh assumes office of Governor; 1 Jan 1949: Reserve Bank of India "
              "nationalised; 1 Jul 1949: Sir Benegal Rama Rau assumes office as Governor", CHRON_35)])
Q(T, "Governors and leadership", "Basic",
  "Who was appointed Governor of RBI on 22 November 1997, shortly before RBI responded to the Asian currency crisis?",
  ["Bimal Jalan", "C. Rangarajan", "Y. V. Reddy", "S. Venkitaramanan"],
  concept="RBI Governors in the 1990s",
  explanation="RBI's chronology records that Bimal Jalan was appointed Governor on 22 November 1997; a series of "
              "measures in response to the Asian currency crisis followed on 28 November 1997.",
  steps=["22 Nov 1997 → Bimal Jalan"],
  why="Rangarajan took over in 1992, Venkitaramanan in 1990, and Reddy succeeded Jalan in 2003.",
  facts=[fact("22 Nov 1997: Bimal Jalan appointed Governor; 28 Nov 1997: a series of measures introduced in "
              "response to the Asian Currency Crisis", CHRON_91)])
Q(T, "Establishment and structure", "Basic",
  "On 11 March 1940, RBI changed its accounting year from:",
  ["January–December to July–June", "April–March to July–June", "July–June to April–March",
   "January–December to April–March"],
  concept="RBI's accounting year",
  explanation="RBI's chronology records that on 11 March 1940 its accounting year was changed from January–December "
              "to July–June. (It moved to April–March much later.)",
  steps=["Before 1940: January–December", "From 1940: July–June"],
  why="The other combinations do not describe the 1940 change.",
  facts=[fact("11 Mar 1940: RBI Accounting Year changed from Jan-Dec to July-June", CHRON_35)])
Q(T, "Establishment and structure", "Intermediate",
  "From 1937, RBI performed central banking roles for a neighbouring territory. Which?",
  ["It acted as banker to the Government of Burma and was responsible for note issue in Burma",
   "It issued currency for Ceylon", "It acted as banker to the Government of Nepal",
   "It managed the public debt of Afghanistan"],
  concept="RBI's early external roles",
  explanation="RBI's chronology records that in 1937 RBI acted as banker to the Government of Burma and was "
              "responsible for note issue in Burma. In 1945 it was also entrusted with the currency and coinage of "
              "the British Military Administration of Burma.",
  steps=["1937 → banker to Burma Government + note issue in Burma"],
  why="RBI had no such role for Ceylon, Nepal or Afghanistan.",
  facts=[fact("1937: RBI acts as banker to the Government of Burma and also responsible for note issue in Burma",
              CHRON_35)])
Q(T, "Governors and leadership", "Intermediate",
  "N. C. Sengupta was Governor of RBI only from 19 May 1975 to 19 August 1975. Who was appointed Governor on 20 "
  "August 1975?",
  ["K. R. Puri", "M. Narasimham", "I. G. Patel", "S. Jagannathan"],
  concept="RBI Governors in the 1970s",
  explanation="RBI's chronology records N. C. Sengupta as Governor up to 19 August 1975 and K. R. Puri's appointment "
              "on 20 August 1975. M. Narasimham followed in May 1977 and I. G. Patel in December 1977.",
  steps=["Sengupta: 19 May – 19 Aug 1975", "Puri: from 20 Aug 1975"],
  why="Jagannathan preceded Sengupta; Narasimham and Patel came in 1977.",
  facts=[fact("19 May 1975: N. C. Sengupta appointed governor up to August 19; 20 Aug 1975: K.R. Puri appointed "
              "governor", CHRON_68)])
Q(T, "Governors and leadership", "Intermediate",
  "Which person served as RBI Governor for only about six weeks in 1970, between L. K. Jha and S. Jagannathan?",
  ["B. N. Adarkar", "P. C. Bhattacharyya", "K. G. Ambegaonkar", "N. C. Sengupta"],
  concept="Short-tenure Governors",
  explanation="RBI's chronology records that B. N. Adarkar was appointed Governor on 4 May 1970 till 15 June, and S. "
              "Jagannathan was appointed on 16 June 1970.",
  steps=["4 May 1970: B. N. Adarkar", "16 Jun 1970: S. Jagannathan"],
  why="Bhattacharyya served from 1962, Ambegaonkar briefly in 1957 and Sengupta in 1975.",
  facts=[fact("04 May 1970: B.N. Adarkar appointed Governor till June 15; 16 Jun 1970: S. Jagannathan appointed "
              "Governor", CHRON_68)])
Q(T, "Establishment and structure", "Advanced",
  "Consider the following developments in RBI's organisation:\n"
  "I. A Department of Banking Development was created in October 1950 together with the new post of Executive "
  "Director.\n"
  "II. The RBI (Amendment) Act, 1951 enabled RBI to become banker to Part B States after executing agreements with "
  "them.\n"
  "III. An Urban Banks Department was formed on 1 February 1984 to supervise urban co-operative banks.\n"
  "Which of the above is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I and III only"],
  concept="Evolution of RBI's structure",
  explanation="All three are recorded in RBI's chronology: the Department of Banking Development and the post of "
              "Executive Director (October 1950), banker to Part B States under the 1951 amendment, and the Urban "
              "Banks Department (1 February 1984).",
  steps=["I: Oct 1950 ✓", "II: 1951 ✓", "III: 1 Feb 1984 ✓"],
  why="Each of the other options leaves out a correct statement.",
  facts=[fact("Oct 1950: Department of Banking Development created together with the new post of Executive "
              "Director; 1951: RBI (Amendment) Act, 1951 enabled the Bank to become Banker to Part B states after "
              "executing agreements with them", CHRON_50),
         fact("01 Feb 1984: Urban Banks Department formed to supervise the affairs of Urban Cooperative Banks",
              CHRON_68)])

board, ccb, halt_days = 3, 4, 5
fees = board * 60_000 + ccb * 30_000 + halt_days * 3_750
assert fees == 318_750
Q(T, "Establishment and structure", "Advanced",
  "RBI pays its Central Board directors a sitting fee of ₹60,000 per Central Board meeting and ₹30,000 per meeting of "
  "the Committee of the Central Board (CCB), plus a halting allowance of ₹3,750 per day. A director attends 3 Board "
  "meetings and 4 CCB meetings and is eligible for 5 days of halting allowance in a year. What does RBI pay as "
  "sitting fees and halting allowance (travel and stay are borne separately)?",
  ["₹3,18,750", "₹3,00,000", "₹2,58,750", "₹4,38,750"],
  concept="Remuneration of RBI's Central Board directors",
  explanation="Sitting fees: 3 × ₹60,000 = ₹1,80,000 and 4 × ₹30,000 = ₹1,20,000. Halting allowance: 5 × ₹3,750 = "
              "₹18,750. Total = ₹3,18,750. Travel and stay expenses are borne by RBI in addition.",
  steps=["3 × 60,000 = 1,80,000", "4 × 30,000 = 1,20,000", "5 × 3,750 = 18,750", "Total = 3,18,750"],
  why="₹3,00,000 omits the halting allowance; ₹2,58,750 pays CCB meetings at half the actual count; ₹4,38,750 pays "
      "CCB meetings at the Board rate.",
  computed=True,
  facts=[fact("Sitting fees per meeting: Central Board ₹60,000; Committee of the Central Board ₹30,000; halting "
              "allowance per diem ₹3,750; travel and stay expenses are also borne by the Reserve Bank", ORG)])


# ================================================================= 4. RBI Functions (3 / 3 / 3)
T = "RBI Functions"
Q(T, "Issuer of currency", "Basic",
  "Apart from Hindi in the centre and English on the reverse, how many languages appear in the language panel of "
  "Indian banknotes?",
  ["15", "22", "12", "18"],
  concept="Banknote design",
  explanation="RBI's currency FAQs state that fifteen languages appear in the language panel of banknotes, in "
              "addition to Hindi in the centre and English on the reverse.",
  steps=["Language panel → 15 languages"],
  why="22 is the number of Eighth Schedule languages, not those on the panel; 12 and 18 are wrong.",
  facts=[fact("Fifteen languages are appearing in the language panel of banknotes in addition to Hindi prominently "
              "displayed in the centre of the note and English on the reverse", CUR_FAQ)])
Q(T, "Issuer of currency", "Basic",
  "With effect from 30 June 2011, coins of which denomination were withdrawn from circulation and ceased to be "
  "legal tender?",
  ["25 paise", "50 paise", "₹1", "10 paise only, while 25 paise continued"],
  concept="Legal tender of coins",
  explanation="RBI's FAQs state that 25 paise coins were withdrawn from circulation with effect from 30 June 2011; "
              "coins below 25 paise had been withdrawn much earlier. 50 paise and higher coins remain legal tender.",
  steps=["30 June 2011 → 25 paise coins withdrawn"],
  why="50 paise and ₹1 coins remain legal tender; 10 paise was withdrawn earlier, not alongside a continuing 25 "
      "paise coin.",
  facts=[fact("Twenty-five (25) paise coins have been withdrawn from circulation with effect from June 30, 2011 and "
              "are no more legal tender; coins of denominations below 25 paise were withdrawn much earlier",
              CUR_FAQ)])
Q(T, "Banker to government", "Basic",
  "Under which section of the RBI Act, 1934 is RBI obliged to undertake the receipts and payments of the Central "
  "Government and to manage the public debt of the Union?",
  ["Section 20", "Section 17", "Section 45", "Section 42"],
  concept="Statutory basis of banker to Government",
  explanation="Section 20 places on RBI the obligation to undertake the receipts and payments of the Central "
              "Government and to carry out its exchange, remittance and banking operations, including management of "
              "the public debt. Section 21 gives RBI the right to transact the Union's business.",
  steps=["Obligation → Section 20", "Right → Section 21"],
  why="Section 17 lists RBI's business, Section 45 deals with agency banks and Section 42 with CRR.",
  facts=[fact("In terms of Section 20 of the RBI Act 1934, RBI has the obligation to undertake the receipts and "
              "payments of the Central Government and to carry out the exchange, remittance and other banking "
              "operations, including the management of the public debt of the Union", GOVBANK_FAQ)])
Q(T, "Issuer of currency", "Intermediate",
  "Under the RBI (Note Refund) Rules as amended in 2018, a mutilated ₹500 note is paid full value only if the area "
  "of its single largest undivided piece is:",
  ["More than 80% of the note", "More than 65% of the note", "More than 50% of the note",
   "At least 40% of the note"],
  concept="Exchange of mutilated notes",
  explanation="For notes of ₹50 and above, the 2018 amendment pays full value if the largest undivided piece is more "
              "than 80%, half value if it is 40% to 80%, and nothing below 40%. The earlier (2009) full-value "
              "threshold was 65%.",
  steps=["₹50 and above: > 80% → full", "40%–80% → half", "< 40% → reject"],
  why="65% was the pre-2018 threshold; 50% applies to notes up to ₹20; 40% is the half-value floor.",
  facts=[fact("Notes of ₹50 and above (amended NRR 2018): area less than 40% – reject; 40% to 80% – half value; "
              "single largest undivided piece more than 80% – full value", CUR_FAQ)])
Q(T, "Banker to government", "Intermediate",
  "RBI pays agency banks a commission for conducting Government business. At the rates applicable from 1 July 2019, "
  "what does an agency bank earn for a Government receipt collected in e-mode?",
  ["₹9 per transaction", "₹40 per transaction", "₹75 per transaction", "6.5 paise per ₹100 of turnover"],
  concept="Agency commission",
  explanation="The agency commission rates are ₹40 per physical receipt, ₹9 per e-mode receipt, ₹75 per pension "
              "payment and 6.5 paise per ₹100 of turnover for payments other than pension.",
  steps=["e-mode receipt → ₹9"],
  why="₹40 is for physical receipts, ₹75 for pension payments, and 6.5 paise per ₹100 for other payments.",
  facts=[fact("Agency commission from July 1, 2019: Receipts – physical mode ₹40 per transaction; Receipts – e-mode "
              "₹9 per transaction; Payments – pension ₹75 per transaction; Payments other than pension 6.5 paise per "
              "₹100 turnover", GOVBANK_FAQ)])
Q(T, "Regulator and supervisor", "Intermediate",
  "The Payment and Settlement Systems Act, 2007, which designates RBI as the authority to regulate and supervise "
  "payment systems, came into force on:",
  ["12 August 2008", "20 December 2007", "1 April 2008", "14 December 2020"],
  concept="Legal basis of payment system oversight",
  explanation="The PSS Act received the President's assent on 20 December 2007 and came into force on 12 August "
              "2008, the same date as the Payment and Settlement Systems Regulations, 2008.",
  steps=["Assent: 20 Dec 2007", "In force: 12 Aug 2008"],
  why="20 December 2007 is the assent date; 1 April 2008 is wrong; 14 December 2020 is when RTGS became 24x7.",
  facts=[fact("The PSS Act, 2007 received the assent of the President on 20th December 2007 and it came into force "
              "with effect from 12th August 2008", PSS_FAQ)])

pieces = [85, 60, 35]
value = sum(500 if p > 80 else 250 if p >= 40 else 0 for p in pieces)
assert value == 750
Q(T, "Issuer of currency", "Advanced",
  "A shopkeeper brings three mutilated ₹500 notes to a bank branch. The single largest undivided piece of each is "
  "85%, 60% and 35% of the note respectively. Under the Note Refund Rules as amended in 2018, how much will he "
  "receive?",
  ["₹750", "₹1,000", "₹1,250", "₹500"],
  concept="Note refund computation",
  explanation="For ₹50 and above: more than 80% → full value; 40%–80% → half value; below 40% → rejected. So ₹500 + "
              "₹250 + 0 = ₹750.",
  steps=["85% > 80% → ₹500", "60% in 40–80% → ₹250", "35% < 40% → ₹0", "Total ₹750"],
  why="₹1,000 pays the 60% note in full; ₹1,250 also pays the 35% note at half value; ₹500 pays nothing for the 60% "
      "note.",
  computed=True,
  facts=[fact("Notes of ₹50 and above: less than 40% – reject; 40% to 80% – half value; more than 80% – full value "
              "(Note Refund Rules as amended in 2018)", CUR_FAQ)])

phys, emode, pension, other_turnover = 1_000, 5_000, 200, 50 * 10**7
commission = phys * 40 + emode * 9 + pension * 75 + other_turnover / 100 * 0.065
assert round(commission) == 425_000
Q(T, "Banker to government", "Advanced",
  "In a month an agency bank handles 1,000 Government receipts in physical mode, 5,000 receipts in e-mode, 200 "
  "pension payments and other Government payments with a turnover of ₹50 crore. At the agency commission rates in "
  "force since 1 July 2019, what commission does RBI pay it?",
  ["₹4,25,000", "₹1,00,000", "₹3,65,000", "₹3,40,000"],
  concept="Agency commission computation",
  explanation="Physical receipts 1,000 × ₹40 = ₹40,000; e-mode receipts 5,000 × ₹9 = ₹45,000; pension 200 × ₹75 = "
              "₹15,000; other payments ₹50 crore ÷ 100 × 6.5 paise = ₹3,25,000. Total = ₹4,25,000.",
  steps=["40,000 + 45,000 + 15,000 = 1,00,000", "₹50,00,00,000 / 100 × ₹0.065 = 3,25,000", "Total 4,25,000"],
  why="₹1,00,000 omits the turnover commission; ₹3,65,000 omits the e-mode and pension commission; ₹3,40,000 counts "
      "only pension and turnover commission.",
  computed=True,
  facts=[fact("Agency commission from July 1, 2019: physical receipts ₹40; e-mode receipts ₹9; pension payments ₹75 "
              "per transaction; payments other than pension 6.5 paise per ₹100 turnover", GOVBANK_FAQ)])
Q(T, "Regulator and supervisor", "Advanced",
  "Consider the following statements about authorisation under the Payment and Settlement Systems Act, 2007, as "
  "explained by RBI:\n"
  "I. An application for authorisation must be accompanied by a fee of ₹10,000 (excluding GST).\n"
  "II. RBI endeavours to dispose of applications within six months of receipt.\n"
  "III. An applicant whose application is refused can appeal to the Supreme Court within 90 days.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="PSS Act authorisation",
  explanation="The application fee is ₹10,000 excluding GST (I) and RBI endeavours to dispose of applications within "
              "six months (II). An aggrieved applicant or system provider appeals to the Central Government within "
              "30 days, not the Supreme Court within 90 days (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (Central Government, 30 days)"],
  why="III is wrong; 'I only' omits II.",
  facts=[fact("A sum of ₹10,000 (excluding applicable GST) is required to be submitted as application fee; the "
              "Reserve Bank will endeavour to dispose of all applications within six months; the aggrieved applicant "
              "can appeal to the Central Government within 30 days (Section 9)", PSS_FAQ)])

# ================================================================= 5. Monetary Policy (3 / 3 / 4)
T = "Monetary Policy"
Q(T, "Transmission", "Basic",
  "In his statement of 5 December 2025, the RBI Governor clarified the primary purpose of open market operations "
  "(OMOs). What is it?",
  ["To provide sufficient (durable) liquidity, not to directly influence G-sec yields",
   "To set the policy repo rate", "To directly target the 10-year G-sec yield",
   "To manage the exchange rate of the rupee"],
  concept="OMOs versus the policy rate",
  explanation="The Governor reiterated that the policy repo rate is the primary instrument of monetary policy and "
              "that the primary purpose of OMOs is to provide sufficient liquidity, not to directly influence G-sec "
              "yields.",
  steps=["Primary instrument → repo rate", "OMOs → liquidity provision, not yield targeting"],
  why="OMOs do not set the repo rate, target yields or manage the exchange rate.",
  current=ca(DEC25),
  facts=[fact("The primary instrument of monetary policy is the policy repo rate; the primary purpose of open market "
              "operations is to provide sufficient liquidity and not to directly influence G-sec yields", GOV_DEC25)])
Q(T, "Transmission", "Basic",
  "To provide durable liquidity, what did the RBI Governor announce on 5 December 2025 for that month?",
  ["OMO purchases of ₹1,00,000 crore and 3-year USD/INR buy/sell swaps of USD 5 billion",
   "A 100 bps cut in the CRR", "OMO sales of ₹50,000 crore", "A special repo window for mutual funds"],
  concept="Durable liquidity tools",
  explanation="After reviewing liquidity, RBI decided to conduct OMO purchases of government securities of ₹1,00,000 "
              "crore and 3-year USD/INR buy/sell swaps of USD 5 billion in December 2025 to ensure adequate durable "
              "liquidity and aid transmission.",
  steps=["OMO purchases ₹1 lakh crore", "3-year buy/sell swap USD 5 billion"],
  why="No CRR cut, OMO sale or special mutual fund window was announced.",
  current=ca(DEC25),
  facts=[fact("We have decided to conduct open market operation (OMO) purchases of government securities amounting "
              "to ₹1,00,000 crore and 3-year USD/INR Buy Sell swaps of USD 5 billion this month", GOV_DEC25)])
Q(T, "Policy stance", "Basic",
  "At its 62nd meeting (3–5 August 2026), the MPC kept the repo rate at 5.25%. What did it decide about the stance?",
  ["It retained the neutral stance", "It moved to an accommodative stance", "It moved to calibrated tightening",
   "It adopted 'withdrawal of accommodation'"],
  concept="Policy stance",
  explanation="The August 2026 resolution says the MPC decided to continue with the neutral stance to respond "
              "appropriately to macroeconomic developments. The change to calibrated tightening came in October "
              "2026.",
  steps=["August 2026 → neutral stance retained"],
  why="Calibrated tightening was adopted in October; accommodative and withdrawal of accommodation were not chosen.",
  current=ca(AUG26),
  facts=[fact("The MPC voted unanimously to keep the policy repo rate unchanged at 5.25 per cent; the MPC also "
              "decided to continue with the neutral stance", MPC_AUG26)])
Q(T, "Transmission", "Intermediate",
  "According to the Governor's statement of 6 February 2026, by how much did the weighted average lending rate "
  "(WALR) on fresh rupee loans fall during February–December 2025 in response to the cumulative 125 bps repo cut?",
  ["105 bps", "125 bps", "69 bps", "41 bps"],
  concept="Transmission to lending rates",
  explanation="The Governor said the WALR on fresh rupee loans declined by 105 bps during February–December 2025 "
              "(interest rate effect 94 bps), while the WADTDR on fresh deposits fell 95 bps and on outstanding "
              "deposits 41 bps.",
  steps=["Repo cut: 125 bps", "WALR fresh loans: −105 bps"],
  why="125 bps is the repo cut itself; 69 bps was the figure for February–October 2025; 41 bps is the fall in "
      "outstanding deposit rates.",
  current=ca(FEB26),
  facts=[fact("In response to the cumulative 125 bps cut in the policy repo rate, the WALR of SCBs declined by 105 "
              "bps for fresh rupee loans during February-December 2025; WADTDR on fresh deposits declined by 95 bps, "
              "while that on outstanding deposits softened by 41 bps", GOV_FEB26)])
Q(T, "Transmission", "Intermediate",
  "According to the Governor's statement of 7 October 2026, during July–August 2026 the WALR on fresh loans hardened "
  "by 8 bps while the weighted average domestic term deposit rate (WADTDR) on fresh deposits fell by 28 bps. What "
  "explained the fall in deposit rates?",
  ["A decline in bulk deposit rates as liquidity surged from mobilisation of FCNR(B) deposits",
   "A cut in the policy repo rate in August 2026", "A reduction in the CRR in July 2026",
   "A ceiling on deposit rates imposed by RBI"],
  concept="Divergent transmission",
  explanation="The Governor attributed the moderation in deposit rates to a decline in bulk deposit rates because of "
              "a surge in liquidity from mobilisation of FCNR(B) deposits, while lending rates firmed with robust "
              "credit demand and a change in lending composition.",
  steps=["Fresh WALR +8 bps; fresh WADTDR −28 bps", "Cause: FCNR(B) inflows lowered bulk deposit rates"],
  why="The repo rate was unchanged in August 2026; there was no CRR cut or deposit-rate ceiling.",
  current=ca(OCT26),
  facts=[fact("During July-August 2026, WALR on fresh rupee loans hardened by 8 bps, while WADTDR moderated by 28 bps "
              "for fresh deposits due to a decline in bulk deposit rates on account of a surge in liquidity from "
              "mobilisation of FCNR(B) deposits", GOV_OCT26)])
Q(T, "Transmission", "Intermediate",
  "In December 2025 RBI bought government securities through OMOs and, at the same time, absorbed funds through "
  "VRRR auctions. How did the Governor explain this?",
  ["OMOs manage durable liquidity while repo/VRRR operations manage transient liquidity to keep the WACR near the "
   "repo rate", "OMOs are meant to raise G-sec yields while VRRRs lower them",
   "The two operations cancel out and have no purpose", "VRRRs are used only for exchange rate management"],
  concept="Durable versus transient liquidity",
  explanation="The Governor said OMO purchases (sales) provide (absorb) durable liquidity, while short-term LAF "
              "operations (VRR/VRRR) manage transient liquidity to align the WACR with the repo rate. So RBI can "
              "inject durable liquidity through OMOs and withdraw transient liquidity through VRRR simultaneously.",
  steps=["OMO → durable liquidity", "VRR/VRRR → transient liquidity, WACR alignment"],
  why="OMOs are not meant to move yields; the operations serve different purposes; VRRRs are not FX tools.",
  current=ca(DEC25),
  facts=[fact("While the objective of purchase (sale) under OMO is to provide (absorb) durable liquidity, the purpose "
              "of repo operations is to manage transient liquidity so as to align the WACR to the policy repo rate; "
              "it is quite possible that we inject durable liquidity through OMO while withdrawing transient "
              "liquidity through VRRR", GOV_DEC25)])

walr = {"Aug": 8.61, "Sep": 8.51}
wad = {"Aug": 5.67, "Sep": 5.61}
spread = {m: round(walr[m] - wad[m], 2) for m in walr}
assert spread == {"Aug": 2.94, "Sep": 2.90} and round((spread["Aug"] - spread["Sep"]) * 100) == 4
Q(T, "Transmission", "Advanced",
  "RBI's data released on 30 October 2026 show the WALR on fresh rupee loans at 8.61% (August 2026) and 8.51% "
  "(September 2026), and the WADTDR on fresh term deposits at 5.67% and 5.61% respectively. What happened to the "
  "spread between fresh lending and fresh deposit rates?",
  ["It narrowed by 4 bps, from 2.94 to 2.90 percentage points",
   "It widened by 4 bps, from 2.90 to 2.94 percentage points", "It narrowed by 16 bps",
   "It was unchanged at 2.90 percentage points"],
  concept="Lending–deposit spread",
  explanation="August spread = 8.61 − 5.67 = 2.94; September spread = 8.51 − 5.61 = 2.90. Lending rates fell 10 bps "
              "and deposit rates 6 bps, so the spread narrowed by 4 bps.",
  steps=["Aug: 8.61 − 5.67 = 2.94", "Sep: 8.51 − 5.61 = 2.90", "Change: −4 bps"],
  why="The spread fell, not rose; 16 bps adds the two declines; it was not unchanged.",
  computed=True, current=ca("2026-10-30"),
  facts=[fact("WALR on fresh rupee loans of SCBs declined to 8.51 per cent in September 2026 from 8.61 per cent in "
              "August 2026; WADTDR on fresh rupee term deposits declined to 5.61 per cent in September 2026 from 5.67 "
              "per cent in August 2026", LEND_RATES)])

cut, walr_fresh, wad_fresh, wad_out = 125, 105, 95, 41
assert round(pct(walr_fresh, cut)) == 84 and round(pct(wad_fresh, cut)) == 76 and wad_out < cut / 3
Q(T, "Transmission", "Advanced",
  "The Governor's statement of February 2026 reported that, after a cumulative 125 bps repo cut, the WALR on fresh "
  "loans fell 105 bps, the WADTDR on fresh deposits fell 95 bps and the WADTDR on outstanding deposits fell 41 bps "
  "(February–December 2025). Consider:\n"
  "I. Pass-through to fresh lending rates was about 84% of the repo cut.\n"
  "II. Pass-through to fresh deposit rates was about 76% of the repo cut.\n"
  "III. Outstanding deposit rates fell by more than half of the repo cut.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Measuring transmission",
  explanation="105/125 = 84% and 95/125 = 76%, so I and II hold. 41 bps is about 33% of 125 bps, well under half, "
              "so III is wrong — outstanding deposits reprice slowly because most are fixed-rate term deposits.",
  steps=["105 ÷ 125 = 84%", "95 ÷ 125 = 76%", "41 ÷ 125 ≈ 33% < 50%"],
  why="III is wrong; 'I only' leaves out II.",
  computed=True, current=ca(FEB26),
  facts=[fact("In response to the cumulative 125 bps cut, WALR on fresh rupee loans declined by 105 bps; WADTDR on "
              "fresh deposits declined by 95 bps, while that on outstanding deposits softened by 41 bps", GOV_FEB26)])
Q(T, "Policy stance", "Advanced",
  "Consider the following statements about liquidity conditions reported by the RBI Governor on 7 October 2026 for "
  "the period since the August 2026 policy:\n"
  "I. RBI conducted 55 VRRR auctions, including 2 term VRRR auctions, and OMO sales of ₹1.0 lakh crore.\n"
  "II. Average daily net absorption under the LAF rose from ₹5.8 lakh crore in August to ₹7.8 lakh crore in "
  "September.\n"
  "III. The weighted average call rate traded on average 14 bps above the policy repo rate.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Liquidity management under a tightening stance",
  explanation="RBI conducted 55 VRRR auctions (including 2 term VRRRs) and OMO sales of ₹1.0 lakh crore (I), and net "
              "absorption rose from ₹1.2 lakh crore in July to ₹5.8 lakh crore in August and ₹7.8 lakh crore in "
              "September (II). With surplus liquidity, the WACR traded 14 bps below, not above, the repo rate (III "
              "wrong).",
  steps=["I: correct", "II: correct", "III: wrong (14 bps below)"],
  why="III is wrong; 'I only' omits II.",
  current=ca(OCT26),
  facts=[fact("The average daily net absorption under the LAF increased from ₹1.2 lakh crore in July 2026 to ₹5.8 "
              "lakh crore in August and further to ₹7.8 lakh crore in September; RBI conducted 55 VRRR auctions, "
              "including 2 term VRRR auctions and OMO sales amounting to ₹1.0 lakh crore since August 2026 policy; "
              "the WACR on average traded 14 basis points below the policy repo rate since August policy",
              GOV_OCT26)])

repo, wacr_aug = 5.25, 5.31
wacr_oct = round(repo - 0.14, 2)
assert round((wacr_aug - repo) * 100) == 6 and wacr_oct == 5.11 and round((wacr_aug - wacr_oct) * 100) == 20
Q(T, "Policy stance", "Advanced",
  "With the repo rate at 5.25% throughout, the Governor said in August 2026 that the WACR had averaged 5.31% since "
  "the June meeting, and in October 2026 that it had traded on average 14 bps below the repo rate since the August "
  "meeting. How did the average WACR move between the two periods?",
  ["From 6 bps above the repo rate to 14 bps below it, a fall of about 20 bps (to about 5.11%)",
   "From 6 bps below the repo rate to 14 bps above it, a rise of about 20 bps",
   "It fell by about 8 bps, to about 5.23%", "It stayed at the repo rate in both periods"],
  concept="Operating target and liquidity",
  explanation="5.31 − 5.25 = 6 bps above repo. Since August it averaged 14 bps below repo, i.e. about 5.11%. The fall "
              "of about 20 bps reflects the large liquidity surplus from capital-inflow measures, which pushed the "
              "WACR into the lower half of the corridor.",
  steps=["June–Aug: 5.31 − 5.25 = +6 bps", "Aug–Oct: 5.25 − 0.14 = 5.11", "Change ≈ −20 bps"],
  why="The direction in the second option is reversed; 8 bps subtracts 6 from 14; the WACR was not at the repo rate.",
  computed=True, current=ca(OCT26),
  facts=[fact("Since the June meeting, the weighted average call rate traded within the policy corridor averaging "
              "5.31 per cent", GOV_AUG26),
         fact("The WACR on average traded 14 basis points below the policy repo rate since August policy",
              GOV_OCT26)])


# ================================================================= 6. Repo Rate (1 / 2 / 1)
T = "Repo Rate"
SUB = "Repo and policy corridor"
Q(T, SUB, "Basic",
  "At its meeting of 20–22 May 2020, advanced from June because of COVID-19, the MPC cut the policy repo rate by 40 "
  "bps. What was the new repo rate?",
  ["4.00%", "4.40%", "3.35%", "4.25%"],
  concept="Repo rate during the pandemic",
  explanation="The MPC reduced the repo rate from 4.40% to 4.00% with immediate effect. The MSF rate and Bank Rate "
              "fell to 4.25% and the reverse repo rate to 3.35%.",
  steps=["4.40% − 0.40% = 4.00%"],
  why="4.40% was the earlier rate; 3.35% was the reverse repo; 4.25% was the MSF/Bank Rate.",
  current=ca("2020-05-22"),
  facts=[fact("Reduce the policy repo rate under the LAF by 40 bps to 4.0 per cent from 4.40 per cent; MSF rate and "
              "Bank Rate reduced to 4.25 per cent from 4.65 per cent; reverse repo rate reduced to 3.35 per cent; "
              "meeting held from May 20 to 22, 2020, advanced from June 3 to 5", MPC_MAY20)])
Q(T, SUB, "Intermediate",
  "In February 2023, the MPC raised the policy repo rate by 25 bps by a majority vote. To what level?",
  ["6.50%", "6.25%", "6.75%", "5.90%"],
  concept="End of the 2022–23 tightening cycle",
  explanation="On 8 February 2023 the MPC raised the repo rate by 25 bps to 6.50% (SDF 6.25%, MSF and Bank Rate "
              "6.75%), with two members voting against.",
  steps=["6.25% + 0.25% = 6.50%"],
  why="6.25% was the SDF after the hike, 6.75% the MSF; 5.90% was the level in September 2022.",
  current=ca("2023-02-08"),
  facts=[fact("The MPC decided by a majority to increase the policy repo rate by 25 basis points to 6.50 per cent; "
              "SDF 6.25 per cent; MSF rate and Bank Rate 6.75 per cent", REPO_FEB23)])
Q(T, SUB, "Intermediate",
  "How did the six MPC members vote at the May 2020 meeting that cut the repo rate to 4.0%?",
  ["Five voted for a 40 bps cut and one (Dr. Chetan Ghate) for a 25 bps cut",
   "All six voted for a 40 bps cut", "Four voted for 40 bps and two for keeping the rate unchanged",
   "Three voted for 40 bps and three for 25 bps, with the Governor's casting vote deciding"],
  concept="MPC voting on the size of a cut",
  explanation="The minutes show that all members voted for a reduction, but Dr. Pami Dua, Dr. Ravindra H. Dholakia, "
              "Dr. Janak Raj, Dr. Michael Debabrata Patra and Shri Shaktikanta Das voted for 40 bps, while Dr. Chetan "
              "Ghate voted for 25 bps.",
  steps=["All six favoured a cut", "Magnitude: 5 for 40 bps, 1 for 25 bps"],
  why="The vote was not unanimous on the size; nobody voted for no change; there was no tie.",
  current=ca("2020-05-22"),
  facts=[fact("Dr. Pami Dua, Dr. Ravindra H. Dholakia, Dr. Janak Raj, Dr. Michael Debabrata Patra and Shri "
              "Shaktikanta Das voted for a reduction in the policy repo rate by 40 bps, while Dr. Chetan Ghate voted "
              "for a reduction by 25 bps", MPC_MAY20)])

may20 = {"repo": 4.00, "floor": 3.35, "msf": 4.25}
oct26 = {"repo": 5.50, "floor": 5.25, "msf": 5.75}
d = {k: round((oct26[k] - may20[k]) * 100) for k in may20}
assert d == {"repo": 150, "floor": 190, "msf": 150}
Q(T, SUB, "Advanced",
  "Compare the policy rates after the MPC decision of 22 May 2020 (repo 4.00%, reverse repo 3.35%, MSF/Bank Rate "
  "4.25%) with those after 7 October 2026 (repo 5.50%, SDF 5.25%, MSF/Bank Rate 5.75%):\n"
  "I. The repo rate is now 150 bps higher.\n"
  "II. The floor of the corridor is now 190 bps higher.\n"
  "III. The MSF rate is now 175 bps higher.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Policy corridor over time",
  explanation="Repo: 5.50 − 4.00 = 150 bps. Floor: SDF 5.25 − reverse repo 3.35 = 190 bps (the floor rose more "
              "because the corridor narrowed from 90 bps to 50 bps). MSF: 5.75 − 4.25 = 150 bps, not 175 (III "
              "wrong).",
  steps=["Repo +150", "Floor 5.25 − 3.35 = +190", "MSF 5.75 − 4.25 = +150 (not 175)"],
  why="III is wrong; 'I only' omits II.",
  computed=True, current=ca(OCT26),
  facts=[fact("May 2020: repo reduced to 4.0 per cent; MSF rate and Bank Rate to 4.25 per cent; reverse repo rate to "
              "3.35 per cent", MPC_MAY20),
         fact("October 2026: repo 5.50 per cent; SDF 5.25 per cent; MSF rate and Bank Rate 5.75 per cent",
              MPC_OCT26)])


# ================================================================= 7. Reverse Repo Rate (1 / 1 / 1)
T = "Reverse Repo Rate"
SUB = "Reverse repo and SDF"
Q(T, SUB, "Basic",
  "When RBI introduced the Standing Deposit Facility on 8 April 2022 as the floor of the LAF corridor, at what rate "
  "was it set?",
  ["3.75%, 25 bps below the repo rate of 4%", "3.35%, equal to the reverse repo rate",
   "4.25%, equal to the MSF rate", "3.50%, 50 bps below the repo rate"],
  concept="Introduction of the SDF",
  explanation="The SDF began on 8 April 2022 at 3.75%, 25 bps below the then repo rate of 4.00%, replacing the "
              "fixed rate reverse repo (retained at 3.35%) as the corridor floor and restoring the corridor to 50 "
              "bps.",
  steps=["Repo 4.00% − 0.25% = SDF 3.75%"],
  why="3.35% was the retained reverse repo; 4.25% was the MSF; 3.50% is not the rate set.",
  facts=[fact("RBI introduced the SDF at 3.75 per cent, 25 bps below the policy repo rate, on April 8, 2022, "
              "restoring the LAF corridor to 50 bps; fixed rate reverse repo retained at 3.35 per cent", SDF_2022)])
Q(T, SUB, "Intermediate",
  "On 4 November 2026 RBI held a second overnight VRRR auction with a notified amount of ₹25,000 crore. What was "
  "the outcome?",
  ["Offers of only ₹1,180 crore were received, and all were accepted at 5.49%",
   "Offers of ₹73,907 crore were received and ₹25,000 crore was accepted",
   "The auction was cancelled for want of bids", "₹25,000 crore was accepted at 5.25%"],
  concept="Variable rate reverse repo auctions",
  explanation="The first overnight VRRR that day (notified ₹50,000 crore) drew ₹73,907 crore of offers, of which "
              "₹50,015 crore was accepted at 5.49%. The second (notified ₹25,000 crore) drew only ₹1,180 crore, all "
              "accepted at 5.49%, showing that most surplus had already been absorbed.",
  steps=["2nd VRRR: offers ₹1,180 crore", "Accepted in full at 5.49%"],
  why="₹73,907 crore was offered in the first auction; the second was held, not cancelled; the rate was 5.49%.",
  current=ca("2026-11-04"),
  facts=[fact("Second Overnight VRRR auction held on November 04, 2026: notified amount ₹25,000 crore; total offers "
              "₹1,180 crore; amount accepted ₹1,180 crore; cut off rate 5.49 per cent", VRRR_NOV4B),
         fact("Overnight VRRR auction held on November 04, 2026: notified ₹50,000 crore; offers ₹73,907 crore; "
              "accepted ₹50,015 crore; cut off rate 5.49 per cent", VRRR_NOV4A)])

before = round((4.25 - 3.35) * 100)
after = round((4.25 - 3.75) * 100)
assert (before, after, before - after) == (90, 50, 40)
Q(T, SUB, "Advanced",
  "Just before April 2022 the repo rate was 4.00%, the fixed rate reverse repo 3.35% and the MSF rate 4.25%. When "
  "the SDF was introduced at 3.75% as the new floor (rates otherwise unchanged), what happened to the LAF corridor?",
  ["It narrowed from 90 bps to 50 bps, and the floor rose by 40 bps",
   "It widened from 50 bps to 90 bps", "It stayed at 90 bps because the reverse repo was retained",
   "It narrowed from 65 bps to 25 bps"],
  concept="SDF as the corridor floor",
  explanation="Before: MSF 4.25 − reverse repo 3.35 = 90 bps. After: MSF 4.25 − SDF 3.75 = 50 bps. The effective "
              "floor rose by 40 bps (3.35 → 3.75), a first step of policy normalisation. The 3.35% reverse repo was "
              "retained but de-emphasised, with operations at RBI's discretion.",
  steps=["4.25 − 3.35 = 90 bps", "4.25 − 3.75 = 50 bps", "Floor +40 bps"],
  why="The corridor narrowed, not widened; the reverse repo ceased to be the floor; 65/25 bps are not the widths.",
  computed=True,
  facts=[fact("Reverse repo rate under the LAF 3.35 per cent; MSF rate 4.25 per cent (May 2020 decision)", MPC_MAY20),
         fact("SDF introduced at 3.75 per cent with repo at 4 per cent and MSF at 4.25 per cent, restoring the LAF "
              "corridor to 50 bps; fixed rate reverse repo retained at 3.35 per cent", SDF_2022)])


# ================================================================= 8. CRR (2 / 1 / 2)
T = "CRR"
Q(T, "CRR concept", "Basic",
  "According to RBI's chronology, penalties for non-compliance with CRR and SLR were introduced in March 1979 in "
  "order to:",
  ["Give RBI teeth to implement monetary policy measures more effectively",
   "Raise revenue for the Government", "Encourage banks to lend to priority sectors",
   "Replace the Bank Rate as the policy rate"],
  concept="Enforcement of reserve requirements",
  explanation="On 30 March 1979 penalties for non-compliance with CRR and SLR were introduced to give RBI teeth to "
              "implement monetary policy measures more effectively.",
  steps=["30 March 1979 → penalties for CRR/SLR shortfalls"],
  why="The penalties were a monetary-policy enforcement tool, not a revenue, PSL or policy-rate measure.",
  facts=[fact("30 Mar 1979: Penalty for non-compliance of CRR & SLR introduced to give the Reserve Bank teeth to "
              "implement Monetary Policy measures more effectively", CHRON_68)])
Q(T, "CRR value", "Basic",
  "As a COVID-19 response, RBI cut the CRR by 100 basis points with effect from the fortnight beginning 28 March "
  "2020. To what level, and for how long?",
  ["3% of NDTL, for one year (up to 26 March 2021)", "4% of NDTL, permanently", "2% of NDTL, for six months",
   "3.5% of NDTL, for two years"],
  concept="CRR as a liquidity tool",
  explanation="The CRR of all banks was reduced by 100 bps to 3% of NDTL from the fortnight beginning 28 March 2020 "
              "for one year ending 26 March 2021; it was later restored in two phases.",
  steps=["4% − 1% = 3%", "Period: one year"],
  why="The level was 3%, the cut was temporary, and the period was one year.",
  facts=[fact("The CRR of all banks was reduced by 100 basis points to 3 per cent of their NDTL, effective the "
              "reporting fortnight beginning March 28, 2020 for a period of one year ending March 26, 2021", AR_2021)])
Q(T, "CRR value", "Intermediate",
  "The CRR, fixed uniformly at 3% in 1962, was raised for the first time in June 1973 as inflation rose. To what "
  "level was it raised on 29 June 1973?",
  ["5%", "7%", "4%", "6%"],
  concept="CRR history",
  explanation="RBI's table of CRR changes shows the CRR at 3% from 16 September 1962, raised to 5% on 29 June 1973, "
              "6% on 8 September 1973 and 7% on 22 September 1973.",
  steps=["1962: 3%", "29 June 1973: 5%", "Sept 1973: 6% then 7%"],
  why="6% and 7% came later in September 1973; 4% came in December 1974 after reductions.",
  facts=[fact("CRR: 3 per cent from 16-09-1962; 5 per cent from 29-06-1973; 6 per cent from 8-9-1973; 7 per cent "
              "from 22-09-1973", RATES_HIST)])
Q(T, "CRR value", "Advanced",
  "Consider the following statements about the CRR relief of 2020 and its reversal:\n"
  "I. CRR was restored to 3.5% of NDTL from the fortnight beginning 27 March 2021.\n"
  "II. It returned to 4.0% from the fortnight beginning 22 May 2021.\n"
  "III. As a one-time dispensation in 2020, the minimum daily CRR balance was relaxed from 90% to 70% of the "
  "requirement.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Phased restoration of CRR",
  explanation="RBI restored the CRR in two phases: 3.5% from the fortnight beginning 27 March 2021 and 4.0% from 22 "
              "May 2021. The 2020 one-time dispensation relaxed the daily minimum from 90% to 80% (not 70%) up to 26 "
              "June 2020.",
  steps=["I: correct", "II: correct", "III: wrong (80%, not 70%)"],
  why="III misstates the relaxation; 'I only' omits II.",
  facts=[fact("Banks were required to maintain the CRR at 3.50 per cent of NDTL effective from the reporting fortnight "
              "beginning March 27, 2021 and 4.0 per cent effective from fortnight beginning May 22, 2021", AR_2021),
         fact("Minimum daily CRR balance maintenance reduced from 90 per cent to 80 per cent, effective March 28, "
              "2020, as a one-time dispensation available up to June 26, 2020", AR_2021)])
Q(T, "CRR concept", "Advanced",
  "In 1981, following a build-up of inflation and an adverse trade movement after the oil price hike, RBI tightened "
  "policy. Which combination does RBI's chronology record for that year?",
  ["Bank Rate 10%, CRR 7.5%, SLR 35%", "Bank Rate 12%, CRR 15%, SLR 38.5%", "Bank Rate 9%, CRR 5%, SLR 34%",
   "Bank Rate 10%, CRR 3%, SLR 25%"],
  concept="Reserve requirements as anti-inflation tools",
  explanation="RBI's chronology says that in 1981 the Bank Rate was raised to 10%, the CRR to 7.5% and the SLR to "
              "35%.",
  steps=["1981 → Bank Rate 10%, CRR 7.5%, SLR 35%"],
  why="12%/15%/38.5% belong to the 1989–91 period; the others do not match 1981.",
  facts=[fact("1981: Build up of inflationary pressures and adverse movement in foreign trade following the hike in "
              "oil prices. Bank rate raised to 10%, CRR raised to 7.5%, SLR to 35%", CHRON_68)])


# ================================================================= 9. SLR (0 / 2 / 1)
T = "SLR"
Q(T, "SLR concept", "Intermediate",
  "State Development Loans (SDLs) are dated securities issued by State Governments. How are they treated for "
  "banks' statutory liquidity ratio?",
  ["Like Central Government dated securities, they qualify for SLR",
   "They do not qualify for SLR because they are State liabilities",
   "They qualify only up to 25% of a bank's SLR requirement", "They qualify only if guaranteed by RBI"],
  concept="SLR-eligible securities",
  explanation="RBI's G-sec primer states that SDLs, like dated securities of the Central Government, qualify for SLR "
              "and are also eligible as collateral for borrowing through market repo and LAF.",
  steps=["SDLs = State G-secs", "Qualify for SLR like Central G-secs"],
  why="There is no exclusion, 25% cap or RBI-guarantee condition.",
  facts=[fact("Like dated securities issued by the Central Government, SDLs issued by the State Governments also "
              "qualify for SLR", GSEC_FAQ)])
Q(T, "SLR value", "Intermediate",
  "Between February and August 1970, faced with inflationary trends, RBI raised the SLR in steps. From and to what "
  "level?",
  ["From 25% to 28%", "From 20% to 25%", "From 28% to 35%", "From 30% to 38.5%"],
  concept="SLR history",
  explanation="RBI's chronology records that inflation between February and August 1970 led to measures including "
              "raising the SLR from 25% to 28% (26% on 5 February, 27% on 24 April and 28% on 28 August 1970).",
  steps=["25% (1964)", "→ 26%, 27%, 28% in 1970"],
  why="20%→25% is the 1949–1964 rise; 35% came in 1981 and 38.5% in 1990.",
  facts=[fact("Between Feb & Aug 1970: inflationary trends led to measures including increasing bank rate and "
              "raising SLR from 25 to 28%", CHRON_60),
         fact("SLR: 26 per cent from 5-2-1970, 27 per cent from 24-04-1970, 28 per cent from 28-08-1970", RATES_HIST)])
Q(T, "SLR concept", "Advanced",
  "Consider the following statements about the COVID-era relaxation of the MSF window that lets banks dip into their "
  "SLR holdings:\n"
  "I. From 28 March 2020 banks could borrow under the MSF by dipping into SLR up to 3% of NDTL, instead of 2%.\n"
  "II. In February 2021, after earlier extensions, the relaxation was extended by a further six months, up to 30 "
  "September 2021.\n"
  "III. Borrowing under the relaxed limit was priced at the repo rate rather than the MSF rate.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="MSF and SLR",
  explanation="RBI allowed banks to dip into SLR by an additional 1% of NDTL, i.e. up to 3%, from 28 March 2020. "
              "After extensions in 2020, it was extended on 5 February 2021 by six months up to 30 September 2021, "
              "also helping banks meet LCR requirements. The borrowing "
              "remained MSF borrowing at the MSF rate (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (MSF rate applies)"],
  why="III is wrong; 'I only' omits II.",
  facts=[fact("Increase in MSF borrowing from 2 per cent of SLR to 3 per cent effective March 28, 2020; banks allowed "
              "to avail funds under the MSF by dipping into the SLR cumulatively up to 3 per cent of NDTL; extended "
              "for a further period of six months, i.e., up to September 30, 2021", AR_2021)])


# ================================================================= 10. Bank Rate (1 / 1 / 1)
T = "Bank Rate"
SUB = "Bank rate and MSF"
Q(T, SUB, "Basic",
  "Before RBI realigned it with the MSF rate in February 2012, at what level had the Bank Rate been kept unchanged "
  "since April 2003?",
  ["6%", "9.5%", "8%", "5.75%"],
  concept="Dormant Bank Rate",
  explanation="RBI's press release says the Bank Rate had been kept unchanged at 6% since April 2003 because "
              "signalling was done through the LAF repo and reverse repo rates.",
  steps=["April 2003 – February 2012 → 6%"],
  why="9.5% was the level after the 2012 realignment; 8% and 5.75% are other values.",
  facts=[fact("The Bank Rate has, however, been kept unchanged at 6 per cent since April 2003", BR_2012)])
Q(T, SUB, "Intermediate",
  "On 13 February 2012 RBI raised the Bank Rate by 350 bps to 9.5%. How did RBI describe this change?",
  ["As a one-time technical adjustment to align the Bank Rate with the MSF rate, not a change in policy stance",
   "As a tightening of monetary policy to fight inflation", "As a penalty on banks for excess borrowing",
   "As the new policy rate replacing the repo rate"],
  concept="Bank Rate realignment",
  explanation="RBI realigned the Bank Rate with the MSF rate (itself linked to the repo rate) and said the change "
              "should be viewed as a one-time technical adjustment rather than a change in the monetary policy "
              "stance; the Bank Rate would normally stay aligned to the MSF rate.",
  steps=["6% → 9.5% (+350 bps)", "Aligned with MSF; technical, not a stance change"],
  why="RBI explicitly said it was not a policy tightening, a penalty or a replacement of the repo rate.",
  facts=[fact("This should be viewed and understood as one-time technical adjustment to align the Bank Rate with the "
              "MSF rate rather than a change in the monetary policy stance; the Bank Rate will stand increased by 350 "
              "basis points from 6.00 per cent to 9.50 per cent", BR_2012)])
Q(T, SUB, "Advanced",
  "Consider the following statements about the Bank Rate:\n"
  "I. Being a discount rate, RBI noted in 2012 that it should technically be higher than the policy repo rate.\n"
  "II. At the off-cycle MPC decision of May 2020, the Bank Rate was reduced to 4.25% from 4.65%.\n"
  "III. Since February 2012 the Bank Rate has been aligned to the policy repo rate.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Bank Rate in the operating framework",
  explanation="RBI's 2012 release says the Bank Rate, being the discount rate, should technically be higher than the "
              "repo rate (I). In May 2020 the MSF rate and Bank Rate were cut to 4.25% from 4.65% (II). Since 2012 "
              "the Bank Rate is aligned to the MSF rate, not the repo rate (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (aligned to MSF)"],
  why="III is wrong; 'I only' omits II.",
  facts=[fact("Being the discount rate, the Bank Rate should technically be higher than the policy repo rate; the Bank "
              "Rate should normally stay aligned to the MSF rate", BR_2012),
         fact("The MSF rate and the Bank Rate stand reduced to 4.25 per cent from 4.65 per cent", MPC_MAY20)])

# ================================================================= 11. Inflation (2 / 4 / 1)
T = "Inflation"
Q(T, "CPI and WPI", "Basic",
  "As defined in the RBI Governor's statement of October 2026, 'core' CPI inflation is CPI inflation excluding:",
  ["The food and beverages division and fuel", "Only food items", "Only fuel and light",
   "Housing and services"],
  concept="Core inflation",
  explanation="RBI defines CPI core as CPI excluding the food and beverages division and fuel (both the group "
              "'Electricity, gas and other fuels' and the class 'Fuels and lubricants for personal transport "
              "equipment').",
  steps=["Core = headline − food & beverages − fuel"],
  why="Excluding only food or only fuel is incomplete; housing and services stay in core.",
  facts=[fact("CPI core is defined as CPI excluding food and beverages division, and fuel (both the group "
              "'Electricity, gas and other fuels' and the class 'Fuels and lubricants for personal transport "
              "equipment')", GOV_OCT26)])
Q(T, "CPI and WPI", "Basic",
  "According to data released in October 2026, India's WPI-based inflation in September 2026 rose to about:",
  ["11.39%", "5.54%", "9.92%", "4.8%"],
  concept="Wholesale price inflation",
  explanation="WPI inflation rose to 11.39% in September 2026 from 9.92% in August, led by mineral oils, food "
              "articles, crude petroleum and natural gas, and basic metals.",
  steps=["September 2026 WPI inflation: 11.39% (August: 9.92%)"],
  why="9.92% was August's figure; 5.54% was September's CPI inflation; 4.8% was August CPI inflation.",
  current=ca("2026-10-14"),
  facts=[fact("WPI inflation rose to 11.39 per cent in September 2026 from 9.92 per cent in August 2026", WPI_SEP26)])
Q(T, "CPI and WPI", "Intermediate",
  "According to the MPC resolution of 6 February 2026, what was headline CPI inflation in November and December "
  "2025?",
  ["0.7% and 1.3%", "2.0% and 2.9%", "3.9% and 4.0%", "1.3% and 0.7%"],
  concept="Low inflation phase of 2025",
  explanation="The MPC noted headline CPI inflation remained low at 0.7% in November and 1.3% in December 2025, below "
              "the lower tolerance band, with the food group in deflation.",
  steps=["Nov 2025: 0.7%", "Dec 2025: 1.3%"],
  why="2.0% was the FY26 projection made in December; the reversed order is wrong; 3.9–4.0% were projections.",
  current=ca(FEB26),
  facts=[fact("Headline CPI inflation remained low at 0.7 per cent in November and 1.3 per cent in December, 2025",
              MPC_FEB26)])
Q(T, "Inflation targeting", "Intermediate",
  "In February 2026 the MPC slightly raised its inflation outlook. What did it say was mainly responsible, and by how "
  "much?",
  ["Higher prices of precious metals, contributing about 60–70 basis points", "A spike in vegetable prices, about "
   "150 basis points", "A rise in fuel taxes, about 25 basis points", "Higher rents in the new CPI series, about 100 "
   "basis points"],
  concept="Precious metals and core inflation",
  explanation="The resolution said the slight upward revision in the inflation outlook was primarily due to higher "
              "prices of precious metals, which contribute about 60–70 basis points; underlying inflation remained "
              "low.",
  steps=["Upward revision ← precious metals", "Contribution ≈ 60–70 bps"],
  why="The MPC did not attribute it to vegetables, fuel taxes or rents.",
  current=ca(FEB26),
  facts=[fact("The slight upward revision in the inflation outlook is primarily due to increase in prices of precious "
              "metals, which contribute about 60-70 basis points", MPC_FEB26)])
Q(T, "CPI and WPI", "Intermediate",
  "According to the Governor's statement of 7 October 2026, what was core CPI inflation excluding precious metals in "
  "August 2026?",
  ["2.9%", "4.2%", "3.9%", "4.8%"],
  concept="Core excluding precious metals",
  explanation="Core inflation rose to 4.2% in August 2026 after staying at 3.9% for three months, but core excluding "
              "precious metals was only 2.9%, indicating that much of the core rise came from gold and silver.",
  steps=["Core: 4.2%", "Core ex precious metals: 2.9%"],
  why="4.2% is overall core, 3.9% the earlier core level and 4.8% headline inflation.",
  current=ca(OCT26),
  facts=[fact("Core inflation also increased to 4.2 per cent in August after remaining unchanged at 3.9 per cent for "
              "three consecutive months; core inflation, excluding precious metals, increased to 2.9 per cent in "
              "August", GOV_OCT26)])
Q(T, "Inflation targeting", "Intermediate",
  "In October 2026 the MPC cited diffusion indices as evidence of broadening price pressures. What share (weighted) "
  "of CPI items recorded inflation above 4% in August 2026?",
  ["About 37%", "About 60%", "About 20%", "About 80%"],
  concept="Diffusion indices",
  explanation="Diffusion indices show how widespread price increases are. The weighted share of CPI items with "
              "inflation above 4% rose steadily to about 37% in August 2026.",
  steps=["Weighted share of items with inflation > 4% → ~37%"],
  why="The other shares are not the figure reported.",
  current=ca(OCT26),
  facts=[fact("The weighted share of items in headline CPI recording inflation above 4 per cent increased steadily to "
              "about 37 per cent in August", MPC_OCT26)])

fb = {"Jun": 5.1, "Jul": 5.2, "Aug": 5.7}
fuel = {"Jun": 4.5, "Jul": 4.6, "Aug": 5.2}
assert round((fb["Aug"] - fb["Jun"]) * 100) == 60 and round((fuel["Aug"] - fuel["Jun"]) * 100) == 70
assert round((fuel["Aug"] - fuel["Jul"]) * 100) > round((fb["Aug"] - fb["Jul"]) * 100)
Q(T, "CPI and WPI", "Advanced",
  "The Governor's statement of October 2026 reported inflation in the CPI food and beverages division at 5.1% (June), "
  "5.2% (July) and 5.7% (August 2026), and fuel inflation at 4.5%, 4.6% and 5.2%. Consider:\n"
  "I. Between June and August, fuel inflation rose by 10 bps more than food and beverages inflation.\n"
  "II. From July to August, fuel inflation rose by more than food and beverages inflation.\n"
  "III. In August 2026, both were above headline CPI inflation of 4.8%.\n"
  "Which is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I and III only"],
  concept="Components of inflation",
  explanation="June→August: food & beverages +60 bps, fuel +70 bps → fuel rose 10 bps more (I). July→August: fuel +60 "
              "bps vs food & beverages +50 bps (II). In August both 5.7% and 5.2% exceed headline 4.8% (III).",
  steps=["F&B: 5.7 − 5.1 = 0.6; fuel: 5.2 − 4.5 = 0.7", "Jul→Aug: fuel +0.6 > F&B +0.5", "5.7, 5.2 > 4.8"],
  why="All three statements hold, so options omitting any are wrong.",
  computed=True, current=ca(OCT26),
  facts=[fact("Inflation in CPI food and beverages division increased to 5.2 per cent and 5.7 per cent in July and "
              "August from 5.1 per cent in June 2026; fuel inflation increased to 4.6 per cent in July and 5.2 per cent "
              "in August from 4.5 per cent in June", GOV_OCT26),
         fact("CPI inflation increased to 4.8 per cent in August 2026", MPC_OCT26)])


# ================================================================= 12. NPA (4 / 2 / 2)
T = "NPA"
Q(T, "Classification", "Basic",
  "Under the early-recognition-of-stress categories in RBI's Prudential Framework for Resolution of Stressed Assets "
  "(circular of 7 June 2019), a loan whose principal or interest was overdue for 45 days was classified as:",
  ["SMA-1", "SMA-0", "SMA-2", "Substandard asset"],
  concept="Special Mention Accounts",
  explanation="Lenders classify stressed loans as SMA-0 (overdue 1–30 days), SMA-1 (31–60 days) and SMA-2 (61–90 "
              "days). 45 days falls in SMA-1; an account becomes NPA only after 90 days.",
  steps=["31–60 days overdue → SMA-1"],
  why="SMA-0 is up to 30 days, SMA-2 is 61–90 days; substandard requires NPA status.",
  facts=[fact6("Circular of 7 June 2019: SMA-0: 1-30 days; SMA-1: 31-60 days; SMA-2: 61-90 days (principal or "
               "interest payment or any other amount wholly or partly overdue)", STRESS)])
Q(T, "Classification", "Basic",
  "Under RBI's prudential norms, what must a bank do with loss assets?",
  ["Write them off; if retained in the books, provide 100% of the outstanding",
   "Provide 25% and keep them as doubtful", "Upgrade them after one year", "Transfer them to RBI"],
  concept="Provisioning for loss assets",
  explanation="RBI's IRAC Directions say loss assets should be written off; if they are permitted to remain in the "
              "books for any reason, 100% of the outstanding must be provided for.",
  steps=["Loss asset → write off", "If retained → 100% provision"],
  why="25% applies to doubtful assets up to one year; loss assets are not upgraded or transferred to RBI.",
  facts=[fact("Loss assets should be written off. If loss assets are permitted to remain in the books for any reason, "
              "100 per cent of the outstanding should be provided for", IRAC_MD)])
Q(T, "SARFAESI", "Basic",
  "The Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Ordinance, which "
  "paved the way for asset reconstruction companies, came into force on:",
  ["21 June 2002", "1 April 1993", "28 May 2016", "15 July 1978"],
  concept="Origin of SARFAESI",
  explanation="RBI's chronology records that the SARFAESI Ordinance came into force on 21 June 2002, paving the way "
              "for ARCs and faster recovery by banks and FIs.",
  steps=["21 June 2002 → SARFAESI Ordinance"],
  why="1993 relates to the DRT law era; 2016 is the IBC year; 1978 is DICGC's formation.",
  facts=[fact("21 Jun 2002: The Securitisation and Reconstruction of Financial Assets and Enforcement of Security "
              "Interest Ordinance came into force, paving the way for setting up asset reconstruction companies",
              CHRON_00)])
Q(T, "Resolution and IBC", "Basic",
  "Under RBI's Prudential Framework for Resolution of Stressed Assets (circular of 7 June 2019), lenders had to "
  "report credit information, including SMA status, to the Central Repository of Information on Large Credits "
  "(CRILC) for borrowers with aggregate exposure of at least:",
  ["₹5 crore (₹50 million)", "₹1 crore", "₹25 crore", "₹100 crore"],
  concept="CRILC reporting",
  explanation="Under the 2019 stressed-assets framework, lenders reported to CRILC on all borrowers with aggregate "
              "exposure of ₹50 million (₹5 crore) and above, monthly, plus a weekly report of defaults every Friday.",
  steps=["CRILC threshold: ₹50 million = ₹5 crore"],
  why="The other amounts are not the CRILC threshold.",
  facts=[fact6("Circular of 7 June 2019: lenders to report credit information, including SMA classification, to CRILC on "
               "all borrowers with aggregate exposure of ₹50 million and above; weekly report of defaults every "
               "Friday", STRESS)])
Q(T, "Resolution and IBC", "Intermediate",
  "Under RBI's Prudential Framework for Resolution of Stressed Assets as laid down in its circular of 7 June 2019, an "
  "inter-creditor agreement had to provide that a decision was binding on all lenders when agreed by lenders "
  "representing:",
  ["75% by value of total outstanding facilities and 60% of lenders by number",
   "66% by value and 50% by number", "51% by value only", "90% by value and 75% by number"],
  concept="Inter-creditor agreement",
  explanation="The ICA must provide that any decision agreed by lenders representing 75% by value of total "
              "outstanding credit facilities (fund and non-fund based) and 60% by number binds all lenders, with "
              "dissenting lenders getting at least liquidation value.",
  steps=["Value: 75%", "Number: 60%"],
  why="66% is the IBC committee-of-creditors threshold for some decisions; the others are not the ICA rule.",
  facts=[fact6("Circular of 7 June 2019: the ICA shall provide that any decision agreed by lenders representing 75 per "
               "cent by value of total outstanding credit facilities and 60 per cent of lenders by number shall be "
               "binding upon all the lenders", STRESS)])
Q(T, "SARFAESI", "Intermediate",
  "According to RBI's FAQs on asset reconstruction companies (September 2026), which of the following is NOT "
  "permitted to an ARC?",
  ["Investing in security receipts issued by another ARC",
   "Acquiring financial assets from banks for asset reconstruction",
   "Following KYC directions for acquired financial assets",
   "Transferring a financial asset to another ARC after eight years, subject to conditions"],
  concept="Permissible ARC activities",
  explanation="ARCs registered under Section 3 of the SARFAESI Act may undertake only permitted functions. RBI "
              "clarifies that they are not permitted to invest in SRs issued by another ARC. Acquisition of assets, "
              "KYC compliance and transfer to another ARC after eight years (subject to conditions) are allowed.",
  steps=["ARC activity limited to securitisation/reconstruction", "Investment in another ARC's SRs → not allowed"],
  why="The other three are explicitly allowed or required.",
  current=ca("2026-09-11"),
  facts=[fact("ARCs are not permitted to invest in the SRs issued by another ARC; ARCs are not prohibited from "
              "transferring financial assets to another ARC even after the completion of eight years, subject to "
              "conditions", ARC_FAQ)])

def ero(o, r, pct_of_earlier):
    """Outstanding, realisable value, realisable value as % of the earlier assessed value."""
    if r < 0.10 * o:
        return "loss"
    if pct_of_earlier < 50:
        return "doubtful"
    return "normal"


assert (ero(150, 12, 30), ero(150, 40, 45), ero(100, 70, 90)) == ("loss", "doubtful", "normal")
Q(T, "Classification", "Advanced",
  "A bank reviews three NPAs for erosion in security:\n"
  "P. Outstanding ₹150 lakh; the realisable value of security is now ₹12 lakh.\n"
  "Q. Outstanding ₹150 lakh; the realisable value has fallen to 45% of the value assessed at the last inspection, "
  "but is still ₹40 lakh.\n"
  "R. Outstanding ₹100 lakh; the realisable value is 90% of the earlier assessed value.\n"
  "Under RBI's IRAC norms, how should P and Q be treated?",
  ["P straightaway as loss asset; Q straightaway as doubtful asset",
   "P as doubtful asset; Q as loss asset", "Both as loss assets", "Both continue in their normal ageing category"],
  concept="Accelerated classification for erosion of security",
  explanation="If the realisable value of security is less than 10% of the outstanding, the security is ignored and "
              "the asset is straightaway a loss asset: P (12 < 15). If erosion is significant—realisable value below "
              "50% of the value assessed earlier—the NPA may straightaway be classified doubtful: Q (45%). R has no "
              "significant erosion.",
  steps=["P: 12 < 10% × 150 = 15 → loss", "Q: 45% < 50% of earlier value → doubtful", "R: normal ageing"],
  why="The P/Q treatments are swapped in the second option; Q is not below the 10% test; erosion rules do apply.",
  computed=True,
  facts=[fact("Erosion in the value of security shall be reckoned as significant when the realisable value of the "
              "security is less than fifty per cent of the value assessed; such NPAs may be straightaway classified "
              "under doubtful category; if the realisable value of the security is less than ten per cent of the "
              "outstanding, the asset shall be straightaway classified as loss asset", IRAC_MD)])

out_bal, sec = 20.0, 4.0
unsec = out_bal - sec
cover = 0.75 * unsec
prov = 0.40 * sec + 1.00 * (unsec - cover)
assert (unsec, cover, round(prov, 2)) == (16.0, 12.0, 5.6)
Q(T, "Classification", "Advanced",
  "A ₹20 lakh MSE loan covered by a CGTMSE guarantee (75% of the unsecured amount) has been doubtful for two years. "
  "The realisable value of security is ₹4 lakh. Following RBI's IRAC illustration (40% on the secured portion for "
  "1–3 years doubtful, 100% on the unsecured and uncovered portion, nothing on the guaranteed portion), what "
  "provision is required?",
  ["₹5.6 lakh", "₹17.6 lakh", "₹12.0 lakh", "₹1.6 lakh"],
  concept="Provisioning for guaranteed NPAs",
  explanation="Unsecured = 20 − 4 = ₹16 lakh. CGTMSE cover = 75% × 16 = ₹12 lakh, needing no provision. Unsecured "
              "and uncovered = ₹4 lakh at 100% = ₹4 lakh. Secured ₹4 lakh at 40% = ₹1.6 lakh. Total ₹5.6 lakh.",
  steps=["Unsecured 16; cover 12; uncovered 4", "Provision = 4 × 100% + 4 × 40% = 5.6"],
  why="₹17.6 lakh ignores the guarantee; ₹12.0 lakh provides on the guaranteed part; ₹1.6 lakh covers only the "
      "secured portion.",
  computed=True,
  facts=[fact("In case the advance covered by schemes/guarantees of CGTMSE, CRGFTLIH and NCGTC becomes non-performing, "
              "no provision need be made towards the guaranteed portion; illustration: secured portion @ 40 per cent, "
              "unsecured and uncovered portion @ 100 per cent", IRAC_MD),
         fact("Doubtful assets – secured portion: up to one year 25 per cent; one to three years 40 per cent; more than "
              "three years 100 per cent", IRAC_MD)])

# ================================================================= 13. Basel Norms (1 / 3 / 5)
T = "Basel Norms"
OCT23 = "2026-10-23"
Q(T, "Leverage ratio", "Basic",
  "How is the Basel III leverage ratio defined in RBI's capital adequacy directions?",
  ["Capital measure (Tier 1 capital) divided by the exposure measure, expressed as a percentage",
   "Total capital divided by risk-weighted assets", "High-quality liquid assets divided by 30-day net outflows",
   "Available stable funding divided by required stable funding"],
  concept="Leverage ratio",
  explanation="The leverage ratio is the capital measure (Tier 1 capital) as the numerator divided by the exposure "
              "measure as the denominator, expressed as a percentage. It is a non-risk-based backstop to the "
              "risk-weighted capital ratio.",
  steps=["Numerator: Tier 1 capital", "Denominator: exposure measure"],
  why="The others define CRAR, LCR and NSFR respectively.",
  facts=[fact("The Basel III leverage ratio is defined as the capital measure (the numerator) divided by the exposure "
              "measure (the denominator), with this ratio expressed as a percentage; Tier 1 leverage ratio "
              "requirement", CAP_LR)])
Q(T, "Leverage ratio", "Intermediate",
  "Under RBI's amended leverage ratio framework (October 2026), how is the exposure measure generally computed?",
  ["On gross accounting values, without using collateral, guarantees or other credit risk mitigation to reduce it "
   "and without netting assets and liabilities", "On risk-weighted values after credit risk mitigation",
   "On net values after netting deposits against loans", "Only on off-balance-sheet items"],
  concept="Leverage exposure measure",
  explanation="The exposure measure generally follows gross accounting values; unless specified otherwise, a bank "
              "shall not take account of physical or financial collateral, guarantees or other CRM to reduce it, and "
              "shall not net assets and liabilities.",
  steps=["Gross accounting values", "No CRM reduction", "No netting"],
  why="Risk weighting, netting and an off-balance-sheet-only measure are all inconsistent with the rule.",
  current=ca(OCT23),
  facts=[fact("The leverage ratio exposure measure generally follows gross accounting values; a bank shall not take "
              "account of physical or financial collateral, guarantees or other credit risk mitigation techniques to "
              "reduce the leverage ratio exposure measure and shall not net assets and liabilities", CAP_LR)])
Q(T, "Leverage ratio", "Intermediate",
  "Under RBI's October 2026 amendment, what scope of consolidation does the Basel III leverage ratio framework "
  "follow?",
  ["The same scope of regulatory consolidation as the risk-based capital framework",
   "Solo (standalone) bank only, always", "Only the bank's overseas branches", "Accounting consolidation including "
   "insurance subsidiaries in all cases"],
  concept="Scope of application",
  explanation="The amendment substitutes paragraph 263(1): the leverage ratio framework follows the same scope of "
              "regulatory consolidation, including consolidation criteria, as the risk-based capital framework.",
  steps=["Leverage scope = risk-based capital scope"],
  why="The rule is not solo-only, branch-only or full accounting consolidation.",
  current=ca(OCT23),
  facts=[fact("The Basel III leverage ratio framework shall follow the same scope of regulatory consolidation, "
              "including consolidation criteria, as is used for the risk-based capital framework", CAP_LR)])
Q(T, "LCR and NSFR", "Intermediate",
  "According to the RBI Governor's statement of October 2026, what was the Liquidity Coverage Ratio of scheduled "
  "commercial banks as of end-June 2026?",
  ["126.74%", "100%", "17.87%", "81%"],
  concept="System-level liquidity buffers",
  explanation="The Governor reported robust liquidity buffers, with an LCR of 126.74% as of end-June 2026, well above "
              "the 100% minimum.",
  steps=["System LCR end-June 2026 = 126.74%"],
  why="100% is the minimum; 17.87% was the system CRAR; 81 bps was the credit–deposit growth gap.",
  current=ca(OCT26),
  facts=[fact("Liquidity buffers were robust, with an LCR of 126.74 per cent as of end June 2026", GOV_OCT26)])

cet1_req = 5.5 + 2.5 + 1.0 + 0.0
assert cet1_req == 9.0
Q(T, "Capital adequacy", "Advanced",
  "RBI's October 2026 amendment defines the CET1 risk-based requirement of a G-SIB branch in India as the 5.5% "
  "minimum plus the capital conservation buffer, the G-SIB higher loss-absorbency requirement and any countercyclical "
  "buffer. For a branch in the first G-SIB bucket (1% buffer), with no countercyclical buffer in force, what CET1 "
  "ratio must it meet?",
  ["9.0% of RWAs", "8.0% of RWAs", "6.5% of RWAs", "11.5% of RWAs"],
  concept="CET1 requirement for G-SIB branches",
  explanation="CET1 requirement = 5.5% minimum + 2.5% CCB + 1% G-SIB buffer (bucket 1) + 0% CCyB = 9.0%.",
  steps=["5.5 + 2.5 + 1.0 + 0 = 9.0%"],
  why="8.0% omits the G-SIB buffer; 6.5% omits the CCB; 11.5% is the total capital requirement with CCB for banks.",
  computed=True, current=ca(OCT23),
  facts=[fact("CET1 risk-based capital requirements (defined as a 5.5 per cent minimum requirement, a 2.5 per cent "
              "capital conservation buffer, the G-SIB higher loss-absorbency requirement, and countercyclical capital "
              "buffer, if applicable); first bucket where a 1 per cent risk-based G-SIB capital buffer applies",
              CAP_LR)])

tier1, deducted, gross = 3_900, 200, 100_200
exposure = gross - deducted
lr = pct(tier1, exposure)
assert exposure == 100_000 and round(lr, 1) == 3.9 and 3.5 <= lr < 4.0
Q(T, "Leverage ratio", "Advanced",
  "A bank's on-balance-sheet assets at gross accounting value are ₹1,00,200 crore. These include a ₹200 crore "
  "investment in an unconsolidated financial entity that has been deducted from CET1, leaving Tier 1 capital of "
  "₹3,900 crore. Under RBI's leverage ratio rules (items deducted from Tier 1 are also deducted from the exposure "
  "measure), what is its leverage ratio, and how does it fare?",
  ["3.9%; it meets the 3.5% minimum for other banks but would fall short of the 4% D-SIB minimum",
   "About 3.89%; it fails the 3.5% minimum", "3.9%; it meets the minimum even as a D-SIB",
   "4.1%; it meets both minimums"],
  concept="Leverage ratio computation",
  explanation="Exposure measure = 1,00,200 − 200 (deducted from Tier 1) = ₹1,00,000 crore. Leverage ratio = 3,900 / "
              "1,00,000 = 3.9%. That clears the 3.5% minimum for non-D-SIB banks but not the 4% D-SIB minimum.",
  steps=["Exposure = 1,00,200 − 200 = 1,00,000", "LR = 3,900 / 1,00,000 = 3.9%", "3.5% ≤ 3.9% < 4%"],
  why="3.89% fails to deduct the ₹200 crore; 3.9% is below the D-SIB 4%; 4.1% is a miscalculation.",
  computed=True, current=ca(OCT23),
  facts=[fact("Any item deducted from Tier 1 capital and regulatory adjustments other than those related to "
              "liabilities shall be deducted from the leverage ratio exposure measure; the minimum leverage ratio for "
              "a D-SIB shall be 4 per cent and 3.5 per cent for other banks", CAP_LR)])
Q(T, "Capital adequacy", "Advanced",
  "RBI's amendment of 23 October 2026 to its forthcoming operational-risk capital directions (effective 1 April "
  "2027) clarified the treatment of interest rate derivative assets in the 'interest earning assets' used for the "
  "Business Indicator. Which statement is correct?",
  ["They are included at fair value (not notional), using only positive fair values, without subtracting negative "
   "fair values", "They are included at notional value", "They are excluded from interest earning assets",
   "They are included at net fair value after offsetting negative values"],
  concept="Business Indicator under the standardised approach for operational risk",
  explanation="Interest rate derivative assets that affect interest income are included in interest earning assets "
              "at fair value, not notional value; the fair value used is positive and a negative fair value is not "
              "subtracted.",
  steps=["Include IR derivative assets", "Measure: positive fair value", "No subtraction of negative values"],
  why="Notional value, exclusion and netting all contradict the amendment.",
  current=ca(OCT23),
  facts=[fact("The interest rate derivative assets that affect a bank's interest income shall be included in interest "
              "earning assets; these derivative assets shall be captured at their fair value (not their notional "
              "value); the fair value used shall be positive, and a negative fair value should not be subtracted; "
              "Chapter IV shall come into effect from April 1, 2027", OPRISK)])
Q(T, "Capital adequacy", "Advanced",
  "Consider the following statements on the health of scheduled commercial banks, as reported by the RBI Governor in "
  "October 2026:\n"
  "I. System-level CRAR was 17.87% in June 2026, higher than a year earlier.\n"
  "II. The GNPA ratio improved to 1.67% in June 2026 from 2.22% in June 2025.\n"
  "III. The net interest margin rose to 3.26% in June 2026 from 3.22% a year earlier.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Capital and asset quality indicators",
  explanation="CRAR was 17.87% in June 2026 and higher than the previous year (I); GNPA improved to 1.67% from 2.22% "
              "(II). NIM actually eased to 3.22% in June 2026 from 3.26% in June 2025, so III reverses the figures.",
  steps=["I: correct", "II: correct", "III: wrong (3.26% → 3.22%, a decline)"],
  why="III is wrong; 'I only' omits II.",
  current=ca(OCT26),
  facts=[fact("The system-level CRAR of 17.87 per cent in June 2026 was well above the regulatory minimum and higher "
              "than the previous year; GNPA ratio at 1.67 per cent in June 2026 vis-à-vis 2.22 per cent in June 2025; "
              "Net Interest Margin was 3.22 per cent for June 2026 (3.26 per cent in June 2025)", GOV_OCT26)])
Q(T, "Capital adequacy", "Advanced",
  "Consider the following statements about RBI's Credit Valuation Adjustment (CVA) Framework Directions:\n"
  "I. Draft directions were issued on 7 August 2026 and the final directions on 7 October 2026.\n"
  "II. Among the key revisions, eligible banks may choose a simpler approach, and the full basic approach separates "
  "systematic and idiosyncratic CVA risk components.\n"
  "III. The directions came into effect immediately on issue.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Capital for CVA risk",
  explanation="RBI issued the draft on 7 August 2026 and the final Commercial Banks – CVA Framework Directions on 7 "
              "October 2026 (I). Revisions include a simpler approach for eligible banks and separate systematic and "
              "idiosyncratic components in the full BA-CVA (II). They take effect from 1 April 2027, not immediately "
              "(III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (from 1 April 2027)"],
  why="III is wrong; 'I only' omits II.",
  current=ca(OCT26),
  facts=[fact("Draft Directions on the CVA Framework issued on August 7, 2026; key revisions included allowing "
              "eligible banks to choose a simpler approach and separate systematic and idiosyncratic CVA risk "
              "components in the full BA-CVA; final Directions released today (October 7, 2026); effective from April "
              "1, 2027", CVA)])


# ================================================================= 14. Financial Inclusion (1 / 6 / 1)
T = "Financial Inclusion"
PM = "PMJDY and allied schemes"
Q(T, PM, "Basic",
  "In January 2015, Guinness World Records recognised the scale of the PMJDY drive. For what?",
  ["Opening 1,80,96,130 bank accounts in a single week", "Issuing the most debit cards in one day",
   "Opening 10 crore accounts in one month", "Enrolling the most people in a pension scheme in a week"],
  concept="PMJDY milestones",
  explanation="PIB's note on 12 years of PMJDY says Guinness World Records recognised that 18,096,130 bank accounts "
              "were opened in a single week as part of the campaign led by the Department of Financial Services.",
  steps=["Jan 2015 → Guinness record: 1,80,96,130 accounts in one week"],
  why="The record was for accounts opened in a week, not cards, a month's total or pensions.",
  facts=[fact("In January 2015, Guinness World Records recognized the scale of the financial inclusion drive under "
              "PMJDY: 18,096,130 bank accounts were opened in a single week", PMJDY12)])
Q(T, PM, "Intermediate",
  "Under PMJDY, who pays the premium for the accident insurance cover attached to the RuPay debit card?",
  ["The National Payments Corporation of India", "The account holder, through auto-debit",
   "The Department of Financial Services", "The account-holding bank"],
  concept="RuPay accident cover",
  explanation="PMJDY account holders get a RuPay debit card with accident insurance cover. No premium is charged to "
              "the beneficiary; the premium is paid by NPCI.",
  steps=["Cover with RuPay card", "Premium paid by NPCI"],
  why="The beneficiary pays nothing; the premium is not borne by DFS or the bank.",
  facts=[fact("No premium is charged from the beneficiary and the premium is paid by the National Payments "
              "Corporation of India", PMJDY12)])
Q(T, PM, "Intermediate",
  "Which of the following is correct about eligibility for a PMJDY account, as described in the Government's 2026 "
  "note on the scheme?",
  ["All Indian citizens are eligible, with no upper age limit and no minimum balance requirement",
   "Only women in rural areas are eligible", "Only persons aged 18 to 60 are eligible",
   "A minimum balance of ₹500 is required"],
  concept="PMJDY eligibility",
  explanation="All citizens of Indian nationality are eligible with no upper age limit; one basic savings account is "
              "opened for an unbanked person; no minimum balance is required.",
  steps=["All citizens", "No upper age limit", "No minimum balance"],
  why="The scheme is not restricted by gender, area or an 18–60 age band, and has no minimum balance.",
  facts=[fact("All citizens of Indian nationality are eligible to open PM-JDY accounts, with no upper age limit; "
              "there is no requirement to maintain any minimum balance", PMJDY12)])
Q(T, PM, "Intermediate",
  "The Differential Interest Rate (DRI) Scheme, introduced on 25 March 1972, provided:",
  ["Concessional interest rates on advances by public sector banks to selected low-income groups",
   "Higher deposit rates for senior citizens", "Interest-free loans to large industries",
   "Differential CRR for rural branches"],
  concept="Early financial inclusion schemes",
  explanation="RBI's chronology records that the DRI Scheme of 25 March 1972 envisaged concessional interest rates on "
              "advances made by public sector banks to selected low-income groups.",
  steps=["1972 → DRI scheme → concessional loans to low-income groups"],
  why="It was a lending concession for the poor, not a deposit, industry or CRR measure.",
  facts=[fact("25 Mar 1972: Differential Interest Rate Scheme introduced which envisaged concessional interest rates "
              "on advances made by Public Sector Banks to selected low income groups", CHRON_68)])
Q(T, "Business correspondents", "Intermediate",
  "In February 2026 RBI said it would revise its guidelines on banks' use of Business Correspondents based on the "
  "recommendations of a committee. Who were the members of that committee?",
  ["Officials from RBI, the Department of Financial Services, IBA and NABARD",
   "Officials from RBI, SEBI and IRDAI only", "Representatives of BC companies alone",
   "Officials from NPCI and UIDAI only"],
  concept="Reviewing the BC model",
  explanation="RBI set up a committee of officials from RBI, DFS, IBA and NABARD to examine BC operations and suggest "
              "ways to improve their efficiency; draft amendment directions were to follow.",
  steps=["Committee: RBI + DFS + IBA + NABARD"],
  why="SEBI/IRDAI, BC companies alone, or NPCI/UIDAI were not the committee.",
  current=ca(FEB26),
  facts=[fact("Reserve Bank had set up a committee, consisting of officials from Reserve Bank, DFS, IBA and NABARD, to "
              "comprehensively examine their operations and make suitable recommendations", SDRP_FEB26)])
Q(T, PM, "Intermediate",
  "State Level Bankers' Committees (SLBCs), a key forum in India's financial inclusion architecture, were set up in "
  "October 1971 to:",
  ["Consider problems requiring inter-bank coordination", "License new bank branches in each State",
   "Supervise urban co-operative banks", "Fix interest rates on agricultural loans"],
  concept="SLBCs",
  explanation="RBI's chronology records that SLBCs were set up in October 1971 to consider problems requiring "
              "inter-bank coordination at the State level.",
  steps=["Oct 1971 → SLBCs → inter-bank coordination"],
  why="SLBCs do not license branches, supervise UCBs or fix rates.",
  facts=[fact("Oct 1971: State Level Bankers' Committees set up to consider problems requiring inter-bank "
              "coordination", CHRON_68)])
Q(T, PM, "Intermediate",
  "Which measure regarding the Lead Bank Scheme did RBI announce in February 2026?",
  ["A comprehensive revised set of instructions and a unified portal for bank-wise LBS data reporting",
   "Abolition of the Lead Bank Scheme", "Transfer of lead bank responsibility to NABARD",
   "Assigning lead banks only in metropolitan districts"],
  concept="Lead Bank Scheme reforms",
  explanation="RBI reviewed the Lead Bank Scheme and proposed comprehensive instructions to streamline it, with "
              "clearly delineated objectives, and a unified portal for reporting bank-wise LBS data that was "
              "fragmented across portals.",
  steps=["Revised LBS instructions (draft)", "Unified LBS reporting portal"],
  why="The scheme was not abolished, transferred to NABARD or limited to metros.",
  current=ca(FEB26),
  facts=[fact("It is now proposed to issue a comprehensive set of instructions on the Lead Bank Scheme; the Reserve "
              "Bank will be launching a unified portal for reporting of Bank-wise LBS data which is currently "
              "fragmented across various portals", SDRP_FEB26)])

tot, rural, urban, women = 59.09, 45.95, 13.14, 32.92
assert round(rural + urban, 2) == tot and round(pct(rural, tot), 1) == 77.8 and round(pct(women, tot), 1) == 55.7
Q(T, PM, "Advanced",
  "As on 19 August 2026, PMJDY had 59.09 crore accounts: 45.95 crore in rural and semi-urban areas, 13.14 crore in "
  "urban and metropolitan areas, and 32.92 crore held by women. Consider:\n"
  "I. About 78% of the accounts are in rural and semi-urban areas.\n"
  "II. Women hold more than 55% of the accounts.\n"
  "III. Urban and metropolitan accounts exceed 15 crore.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="PMJDY composition",
  explanation="45.95 / 59.09 ≈ 77.8% (I). 32.92 / 59.09 ≈ 55.7% (II). Urban and metro accounts are 13.14 crore, "
              "below 15 crore (III wrong); 45.95 + 13.14 = 59.09 confirms the split.",
  steps=["45.95 ÷ 59.09 ≈ 77.8%", "32.92 ÷ 59.09 ≈ 55.7%", "Urban 13.14 < 15"],
  why="III is wrong; 'I only' omits II.",
  computed=True, current=ca("2026-08-27"),
  facts=[fact("Accounts rose from 14.72 crore in 2015 to 59.09 crore as of 19th August 2026; of these, 45.95 crore "
              "accounts are in rural and semi-urban areas, while 13.14 crore are in urban and metropolitan areas; "
              "32.92 crore female beneficiaries", PMJDY12)])


# ================================================================= 15. Priority Sector Lending (1 / 3 / 1)
T = "Priority Sector Lending"
Q(T, "PSLCs", "Basic",
  "During which hours are Priority Sector Lending Certificates normally traded on RBI's e-Kuber portal?",
  ["10 AM to 4:30 PM, except on Saturdays, Sundays and holidays", "9 AM to 5 PM on all days",
   "24x7 on all days", "Only on the last working day of each quarter"],
  concept="PSLC trading",
  explanation="RBI's PSL FAQs state that normal PSLC trading hours are 10 AM to 4:30 PM, and the market operates on "
              "all days except Saturdays, Sundays and holidays under the NI Act declared by the Government of "
              "Maharashtra.",
  steps=["Hours: 10:00–16:30", "Closed on Saturdays, Sundays, holidays"],
  why="PSLC trading is not round-the-clock, not 9–5 on all days and not quarter-end only.",
  facts=[fact("The normal trading hours shall be from 10 AM to 4:30 PM. The PSLC market operates on all days except "
              "Saturdays, Sundays and holidays declared under The Negotiable Instruments Act, 1881 by the Government "
              "of Maharashtra", PSL_FAQ)])
Q(T, "PSLCs", "Intermediate",
  "A foreign bank with fewer than 20 branches in India must meet a target of 8% for lending to sectors other than "
  "exports. Which PSLC can it NOT buy for this purpose?",
  ["PSLC – General", "PSLC – Agriculture", "PSLC – Micro Enterprises", "PSLC – Small and Marginal Farmers"],
  concept="PSLCs for foreign banks",
  explanation="RBI clarifies that foreign banks with fewer than 20 branches cannot buy PSLC-General to achieve their "
              "8% non-export target, but may buy PSLC-Agriculture, PSLC-Micro Enterprises and PSLC-SMF.",
  steps=["8% non-export target", "PSLC-General not allowed; others allowed"],
  why="The other three are expressly allowed.",
  facts=[fact("Foreign banks with less than 20 branches are not allowed to buy PSLC General for achieving their 8% "
              "target of lending to sectors other than exports; such banks are allowed to buy PSLC Agriculture, PSLC "
              "Micro Enterprises and PSLC Small and Marginal Farmer", PSL_FAQ)])
Q(T, "Targets and sub-targets", "Intermediate",
  "A bank lends to a school and to a health care facility, both of which also qualify as MSMEs. How can it classify "
  "these loans for PSL, according to RBI's FAQs?",
  ["Either under MSME (no credit cap) or under Social Infrastructure (subject to its cap), but not both",
   "Under both MSME and Social Infrastructure", "Only under Social Infrastructure", "Not as priority sector at all"],
  concept="Avoiding double counting in PSL",
  explanation="Loans for schools (Social Infrastructure cap ₹8 crore) and health care facilities (cap ₹12 crore) "
              "that also qualify as MSME can be classified under MSME, where no cap applies, or under Social "
              "Infrastructure with its cap—but not under both.",
  steps=["Eligible under two categories", "Choose one: MSME (no cap) or Social Infrastructure (capped)"],
  why="Double classification is barred; MSME classification is permitted; they do qualify as PSL.",
  facts=[fact("Bank loans for schools (prescribed limit of ₹8 crore) and health care facilities (prescribed limit of "
              "₹12 crore) can be classified under MSME, wherein no cap on credit has been prescribed; banks can "
              "classify such activities either under MSME or Social Infrastructure, and not both", PSL_FAQ)])
Q(T, "Targets and sub-targets", "Intermediate",
  "A bank gives housing loans to its own employees on the same commercial terms as other customers. Can these "
  "loans be classified as priority sector?",
  ["No, housing loans to a bank's own employees are not PSL-eligible, whatever the terms",
   "Yes, if the terms are commercial", "Yes, but only up to ₹25 lakh", "Yes, if the employee is a first-time buyer"],
  concept="PSL exclusions",
  explanation="RBI's PSL FAQs clarify that housing loans to banks' own employees are not eligible for priority "
              "sector classification, irrespective of whether they are on commercial or subsidised terms.",
  steps=["Own-employee housing loans → not PSL"],
  why="Terms, amount or first-time status do not change the exclusion.",
  facts=[fact("Housing loans to banks' own employees are not eligible for classification under priority sector "
              "lending, irrespective of whether they are extended on commercial terms or at subsidised rates",
              PSL_FAQ)])

target, quarters = 40, [38, 41, 37, 40]
avg_gap = sum(q - target for q in quarters) / 4
assert avg_gap == -1.0
Q(T, "Targets and sub-targets", "Advanced",
  "A domestic bank's overall PSL achievement (as % of the applicable base) in the four quarters of a year was 38%, "
  "41%, 37% and 40%, against the 40% target. Under RBI's method, what is its shortfall for the year?",
  ["1 percentage point, the simple average of the quarterly shortfall/excess", "5 percentage points, the sum of "
   "quarterly shortfalls", "Nil, because the March quarter met the target", "3 percentage points, the worst quarter"],
  concept="Computing annual PSL shortfall",
  explanation="RBI computes shortfall/excess for each quarter and takes the simple average of the four. Gaps: −2, +1, "
              "−3, 0 → average −1, i.e. a shortfall of 1 percentage point, which must be contributed to the specified "
              "funds.",
  steps=["Quarterly gaps: −2, +1, −3, 0", "Average = −4 ÷ 4 = −1"],
  why="Summing shortfalls ignores the excess and averaging; the March position alone and the worst quarter are not "
      "the rule.",
  computed=True,
  facts=[fact("The shortfall/excess in achievement is calculated for each quarter of the financial year. The "
              "shortfall/excess for the year is arrived at by taking a simple average of the shortfall/excess for all "
              "the four quarters", PSL_FAQ)])

# ================================================================= 16. RBI Integrated Ombudsman Scheme (3 / 1 / 1)
T = "RBI Integrated Ombudsman Scheme"
Q(T, "Process and limits", "Basic",
  "Under RB-IOS, 2026, the IVRS on toll-free number 14448 works 24x7. During what hours can a caller speak to "
  "Contact Centre personnel?",
  ["8:00 AM to 10:00 PM", "9:30 AM to 5:15 PM", "10:00 AM to 4:30 PM", "24x7"],
  concept="RBI Contact Centre",
  explanation="RBI's RB-IOS 2026 FAQs say the IVRS facility on 14448 is available 24x7, and the facility to connect "
              "to Contact Centre personnel is available from 8:00 AM to 10:00 PM.",
  steps=["IVRS: 24x7", "Personnel: 8 AM–10 PM"],
  why="9:30–5:15 was an older timing; 10–4:30 is PSLC trading; 24x7 applies only to the IVRS.",
  current=ca("2026-07-01"),
  facts=[fact("The IVRS facility on Toll Free No. 14448 is available 24x7. The facility to connect to Contact Center "
              "personnel is available from 8:00 AM to 10:00 PM", RBIOS_FAQ)])
Q(T, "Process and limits", "Basic",
  "Is there a ceiling on the amount involved in a dispute that a complainant can bring before the RBI Ombudsman "
  "under RB-IOS, 2026?",
  ["No; there is no limit on the disputed amount, though compensation for consequential loss is capped",
   "Yes, ₹20 lakh", "Yes, ₹50 lakh", "Yes, ₹1 crore"],
  concept="Pecuniary jurisdiction",
  explanation="The FAQs state there is no limit on the amount involved in a dispute that can be brought before the "
              "RBI Ombudsman; caps apply only to compensation for consequential loss and for time, expenses and "
              "harassment.",
  steps=["Disputed amount: no limit", "Compensation heads: capped"],
  why="₹20 lakh, ₹50 lakh and ₹1 crore are not ceilings on the disputed amount (₹50 lakh is the insurance "
      "ombudsman's limit).",
  facts=[fact("There is no limit on the amount involved in a dispute that can be brought before the RBI Ombudsman for "
              "settlement or passing of an Award; for consequential loss the RBI Ombudsman can provide compensation "
              "up to Rs 30 lakh", RBIOS_FAQ)])
Q(T, "Scope and grounds", "Basic",
  "A customer e-mails her grievance to her bank and marks a copy to RBI. Under RB-IOS, 2026, is this a complaint to "
  "the RBI Ombudsman?",
  ["No; complaints not addressed directly to the RBI Ombudsman, including those where RBI is only marked in copy, "
   "are not maintainable", "Yes, marking RBI in copy is enough", "Yes, if the amount exceeds ₹1 lakh",
   "Yes, but only after 90 days"],
  concept="Maintainability",
  explanation="Among non-maintainable complaints are those not addressed directly to the RBI Ombudsman, including "
              "communications where RBI is merely marked in copy. She must file through CMS, e-mail to the CRPC or "
              "post.",
  steps=["RBI in copy ≠ complaint to Ombudsman"],
  why="A copy to RBI does not create a complaint, regardless of amount or time elapsed.",
  facts=[fact("Complaints not addressed directly to the RBI Ombudsman, including communications where RBI is merely "
              "marked in copy, are not maintainable under RB-IOS, 2026", RBIOS_FAQ)])
Q(T, "Process and limits", "Intermediate",
  "Noting a rise in pendency with the RBI Ombudsman, what did the RBI Governor announce on 5 December 2025?",
  ["A two-month campaign from 1 January 2026 to resolve all grievances pending with the RBI Ombudsman for more than "
   "a month", "A fee for filing complaints above ₹1 lakh", "Closure of the Centralised Receipt and Processing "
   "Centre", "Raising the compensation limit to ₹50 lakh"],
  concept="Grievance redress campaign",
  explanation="The Governor exhorted regulated entities to reduce grievances and proposed a two-month campaign from 1 "
              "January 2026 to resolve all grievances pending for more than a month with the RBI Ombudsman.",
  steps=["Pendency rising", "Campaign: 2 months from 1 Jan 2026"],
  why="No fee, CRPC closure or limit increase was announced.",
  current=ca(DEC25),
  facts=[fact("Pendency with the RBI Ombudsman has increased; we propose to hold a two-month campaign from 1st January "
              "next year with an aim to resolve all grievances pending for more than a month with the RBI Ombudsman",
              GOV_DEC25)])
Q(T, "Scope and grounds", "Advanced",
  "Under Clause 16 of RB-IOS, 2026, on which of the following grounds may the RBI Ombudsman reject a complaint at "
  "any stage?\n"
  "I. The complaint is only a suggestion or query and discloses no deficiency in service.\n"
  "II. The complaint requires elaborate documentary and oral evidence, making Ombudsman proceedings inappropriate.\n"
  "III. The complainant seeks compensation for consequential loss beyond the Ombudsman's power to award.\n"
  "Which are valid grounds?",
  ["I, II and III", "I and II only", "II and III only", "I only"],
  concept="Rejection of complaints",
  explanation="Clause 16 allows rejection at any stage where the complaint is not valid (suggestions, queries), where "
              "consequential-loss compensation sought is beyond the Ombudsman's power, where elaborate evidence is "
              "needed, or where the same cause is filed before a court or other forum during examination.",
  steps=["I ✓", "II ✓", "III ✓"],
  why="All three are listed grounds, so partial options are wrong.",
  facts=[fact("The RBI Ombudsman may reject a complaint at any stage, if the complaint is in the nature of suggestions, "
              "queries; the compensation sought for consequential loss is beyond the power of the RBI Ombudsman; the "
              "complaint requires consideration of elaborate documentary and oral evidence", RBIOS_FAQ)])


# ================================================================= 17. Digital Banking (3 / 1 / 2)
T = "Digital Banking"
Q(T, "Mobile and internet banking", "Basic",
  "What does RBI's UDGAM portal enable users to do?",
  ["Search unclaimed deposits across multiple banks at one place; claims are settled by the respective banks",
   "Claim unclaimed deposits directly from RBI", "Open new deposit accounts online", "File complaints against banks"],
  concept="UDGAM",
  explanation="UDGAM (Unclaimed Deposits – Gateway to Access inforMation) lets registered users search unclaimed "
              "deposits transferred to the DEA Fund across banks in one place and shows each bank's claim process; "
              "claims can be made only with the respective bank.",
  steps=["Search across banks", "Claim with the bank, not RBI"],
  why="RBI does not settle claims; UDGAM is not for opening accounts or complaints (that is CMS).",
  facts=[fact("UDGAM is an online portal developed by RBI that facilitates registered users to search unclaimed "
              "deposits/accounts across multiple banks at one place; the unclaimed deposits can be claimed only from "
              "the respective banks", UDGAM_FAQ)])
Q(T, "CBDC (e-rupee)", "Basic",
  "Can a retail e₹ (digital rupee) payment be made for an amount such as ₹157.35?",
  ["Yes; e₹ supports payments up to two decimal places", "No; only whole-rupee amounts are allowed",
   "Only amounts in multiples of ₹10", "Only if the merchant accepts coins"],
  concept="Features of the e-rupee",
  explanation="RBI's e₹ FAQs say the e₹ supports payments involving decimal or fractional values up to two decimal "
              "places, and wallets automatically provide change from available denominations.",
  steps=["Fractional amounts up to two decimals supported"],
  why="e₹ is not limited to whole rupees or multiples of ₹10.",
  facts=[fact("The e₹ supports payments involving decimal or fractional values. Transactions can be made for any "
              "amount up to two decimal places", ERUPEE_FAQ)])
Q(T, "Mobile and internet banking", "Basic",
  "RBI's NEFT FAQs refer customers to the 'RBI Kehta Hai' web page and to a magazine for users of digital "
  "transactions, on ways to keep digital payments safe. What is that magazine called?",
  ["BE(A)WARE", "Arthashastra", "Mint Street Memo", "Financial Stability Report"],
  concept="Digital payment safety awareness",
  explanation="RBI launched the magazine BE(A)WARE for users of digital transactions, alongside the 'RBI Kehta Hai' "
              "awareness page.",
  steps=["Safe digital payments → 'RBI Kehta Hai' + BE(A)WARE"],
  why="Mint Street Memos are research notes; the FSR is a financial stability publication; Arthashastra is not an "
      "RBI magazine.",
  facts=[fact("RBI has also launched a magazine named BE(A)WARE for users of digital transactions", NEFT_FAQ)])
Q(T, "Mobile and internet banking", "Intermediate",
  "In February 2026, while reviewing the 2017 framework on limiting customer liability in unauthorised electronic "
  "banking transactions, the Governor proposed a new compensation framework. What was it?",
  ["Compensation of up to ₹25,000 for losses in small-value fraudulent transactions",
   "Full compensation for all frauds regardless of customer negligence", "Insurance of all digital payments by DICGC",
   "Compensation only for frauds above ₹1 lakh"],
  concept="Customer protection in digital transactions",
  explanation="The Governor said draft revised instructions would be issued, including a framework to compensate "
              "customers up to ₹25,000 for losses in small-value fraudulent transactions, along with a discussion "
              "paper on safeguards such as lagged credits.",
  steps=["Proposal: compensation up to ₹25,000 for small-value frauds"],
  why="The proposal is limited to small-value frauds and is not DICGC insurance or a high-value-only scheme.",
  current=ca(FEB26),
  facts=[fact("It is also proposed to introduce a framework to compensate customers up to an amount of ₹25000/- for "
              "loss incurred in small-value fraudulent transactions", GOV_FEB26)])

bal_cap, xfer_unreg, cash_txn, cash_month = 200_000, 10_000, 2_000, 10_000
withdrawals = [2_000, 2_000, 2_000, 2_000, 2_000]
assert all(w <= cash_txn for w in withdrawals) and sum(withdrawals) == cash_month and 2_500 > cash_txn
Q(T, "Mobile and internet banking", "Advanced",
  "Neha holds a full-KYC wallet (PPI) issued by a non-bank. Under RBI's PPI rules, which of the following is "
  "permitted?\n"
  "P. Holding a balance of ₹1.8 lakh in the wallet.\n"
  "Q. Withdrawing cash of ₹2,500 in one transaction at an agent.\n"
  "R. Five cash withdrawals of ₹2,000 each in a month.\n"
  "S. Sending ₹15,000 in a month to a friend whom she has not pre-registered as a beneficiary.",
  ["P and R only", "P, Q and R only", "R and S only", "P and S only"],
  concept="Limits on full-KYC PPIs",
  explanation="A full-KYC PPI may hold up to ₹2 lakh (P allowed). Non-bank PPI cash withdrawal is capped at ₹2,000 "
              "per transaction within ₹10,000 a month (Q not allowed; R exactly ₹10,000, allowed). Funds transfer is "
              "limited to ₹10,000 a month per holder unless the beneficiary is pre-registered (S not allowed).",
  steps=["P: 1.8 ≤ 2 lakh ✓", "Q: 2,500 > 2,000 ✗", "R: 5 × 2,000 = 10,000 ✓", "S: 15,000 > 10,000, "
         "unregistered ✗"],
  why="Q breaches the per-transaction cash limit; S breaches the unregistered transfer limit.",
  computed=True,
  facts=[fact("Full-KYC PPI: the amount outstanding shall not exceed ₹2,00,000 at any point of time; funds transfer "
              "is allowed within a limit of ₹10,000 per month per holder; enhanced limit of up to ₹2,00,000 per month "
              "per beneficiary if the beneficiary is pre-registered", PPI_FAQ),
         fact("In case of non-bank issued PPIs, cash withdrawal is permitted upto a limit of ₹2,000 per transaction "
              "within an overall monthly limit of ₹10,000 per PPI across all channels", PPI_FAQ)])
Q(T, "CBDC (e-rupee)", "Advanced",
  "Consider the following statements based on RBI's e₹ FAQs updated in October 2026:\n"
  "I. 19 banks were offering CBDC wallets.\n"
  "II. e₹ wallets are currently linked to the user's savings bank account, which removes the need for a separate "
  "KYC.\n"
  "III. When a user scans a UPI QR code from an e₹ app, the payment settles instantly between two e₹ wallets, "
  "outside UPI timelines.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Retail CBDC pilot",
  explanation="The FAQs list 19 banks offering CBDC wallets (I) and say wallet opening is linked to savings accounts, "
              "avoiding separate KYC (II). Payments at a CBDC QR settle instantly wallet-to-wallet, but when a UPI QR "
              "is scanned from the e₹ app, settlement follows UPI timelines (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (UPI QR → UPI settlement timelines)"],
  why="III confuses CBDC-QR and UPI-QR settlement; 'I only' omits II.",
  current=ca("2026-10-01"),
  facts=[fact("Currently, 19 banks are offering CBDC wallets; opening of e₹ wallets is linked to user's savings bank "
              "accounts, which obviates the need for separate KYC; for payments scanning a UPI QR from an e₹ app, the "
              "settlement will be based on the UPI settlement timelines", ERUPEE_FAQ)])


# ================================================================= 18. UPI (3 / 3 / 4)
T = "UPI"
Q(T, "Features", "Basic",
  "When UPI went live in September 2016, what was its per-transaction limit?",
  ["₹1 lakh", "₹2 lakh", "₹5 lakh", "₹10,000"],
  concept="UPI at launch",
  explanation="RBI's payments booklet says UPI went live in September 2016 with a transaction limit of ₹1 lakh and "
              "was upgraded to UPI 2.0 in 2018 with a ₹2 lakh per-transaction limit.",
  steps=["Launch (Sept 2016): ₹1 lakh"],
  why="₹2 lakh came with UPI 2.0; ₹5 lakh applies to specific categories later; ₹10,000 is not the launch limit.",
  facts=[fact("The system that went live in September 2016 with a transaction limit of ₹1 lakh was upgraded to UPI "
              "2.0 in 2018 with a per transaction limit of ₹2 lakh", PAY_BOOKLET)])
Q(T, "Features", "Basic",
  "To curb fraud, NPCI stopped processing which type of UPI transaction from 1 October 2025?",
  ["Person-to-person (P2P) collect requests", "Person-to-merchant collect requests",
   "UPI Lite payments", "UPI AutoPay mandates"],
  concept="UPI collect requests",
  explanation="By a circular of July 2025, NPCI directed that P2P collect requests would not be processed in UPI from "
              "1 October 2025; merchants can still initiate collect requests.",
  steps=["From 1 Oct 2025 → P2P collect discontinued", "Merchant collect continues"],
  why="Merchant collect, UPI Lite and AutoPay continue.",
  facts=[fact("By October 1, 2025, UPI P2P Collect shall not be allowed to be processed in UPI; merchants can continue "
              "to use collect requests", UPI_COLLECT)])
Q(T, "Features", "Basic",
  "How does UPI achieve two-factor authentication for transactions?",
  ["Through device binding and the UPI PIN", "Through a signature and a cheque", "Through the card's CVV and OTP",
   "Through Aadhaar biometrics only"],
  concept="UPI security",
  explanation="UPI transactions use two-factor authentication through device binding and a UPI PIN; the PIN is "
              "encrypted using Public Key Infrastructure.",
  steps=["Factor 1: device binding", "Factor 2: UPI PIN (PKI-encrypted)"],
  why="Signatures and CVVs are not UPI factors; biometrics are not the standard UPI method.",
  facts=[fact("Transactions are carried out through mobile devices with two factor authentication using device "
              "binding and a UPI PIN as security; the UPI PIN is encrypted using PKI technology", PAY_BOOKLET)])
Q(T, "Features", "Intermediate",
  "In the UPI framework described by RBI, what role does NPCI play?",
  ["Network and settlement service provider, with banks as PSPs and issuer/beneficiary banks and apps like Google "
   "Pay as TPAPs", "Issuer of all UPI accounts", "Regulator of UPI under the PSS Act", "Payment service provider "
   "to individual customers"],
  concept="UPI architecture",
  explanation="The UPI framework comprises NPCI as the network and settlement service provider, banks as Payment "
              "System Providers and as issuer and beneficiary banks, and TPAPs such as Google Pay, Truecaller and "
              "WhatsApp; non-bank PPI issuers may also offer UPI interoperably.",
  steps=["NPCI → network + settlement", "Banks → PSPs, issuers", "TPAPs → apps"],
  why="NPCI does not hold accounts or regulate payment systems (RBI does), nor serve customers as a PSP.",
  facts=[fact("The framework of UPI comprises of NPCI as network and settlement service provider, banks as Payment "
              "System Providers (PSPs), and as issuer banks and beneficiary banks; apart from TPAPs such as Google "
              "Pay, Truecaller, WhatsApp", PAY_BOOKLET)])
Q(T, "Features", "Intermediate",
  "From 15 September 2025, NPCI raised UPI limits for certain merchant categories such as capital market "
  "investments and insurance premiums. What were the new limits?",
  ["₹5 lakh per transaction and ₹10 lakh in 24 hours", "₹10 lakh per transaction with no daily cap",
   "₹2 lakh per transaction and ₹5 lakh a day", "₹1 lakh per transaction and ₹10 lakh a month"],
  concept="Category-specific UPI limits",
  explanation="For categories such as capital markets and insurance, the per-transaction limit was raised to ₹5 lakh "
              "(from ₹2 lakh) with a daily limit of ₹10 lakh, effective 15 September 2025.",
  steps=["Per transaction: ₹5 lakh", "Per day: ₹10 lakh"],
  why="The other combinations misstate the limits.",
  facts=[fact("From September 15, 2025, UPI transactions for capital markets and insurance can go up to ₹5 lakh per "
              "transaction with a daily limit of ₹10 lakh; earlier per-transaction cap ₹2 lakh", UPI_LIMITS)])
Q(T, "Features", "Intermediate",
  "According to the RBI Governor's statement of October 2026, how did the volume of UPI transactions grow in Q2 "
  "(July–September) of 2026-27?",
  ["By 22.2%, slower than 24.2% in Q1", "By 24.2%, faster than 22.2% in Q1", "By 55.8%", "It declined by 5.4%"],
  concept="UPI growth as a demand indicator",
  explanation="Among indicators of private consumption, the Governor cited UPI transaction volume growth of 22.2% in "
              "Q2:2026-27 compared with 24.2% in Q1.",
  steps=["Q2: 22.2%", "Q1: 24.2%"],
  why="The figures are reversed in the second option; 55.8% is the CY2021–25 CAGR; −5.4% was air traffic.",
  current=ca(OCT26),
  facts=[fact("UPI transactions (volume) grew by 22.2 per cent in Q2:2026-27 (24.2 per cent in Q1)", GOV_OCT26)])
Q(T, "Features", "Advanced",
  "Consider the following statements about NPCI's volume cap on third-party UPI apps (TPAPs):\n"
  "I. A TPAP's share is capped at 30% of the total UPI volume, computed on the preceding three months on a rolling "
  "basis.\n"
  "II. The deadline for existing TPAPs above the cap was extended to 31 December 2026.\n"
  "III. The cap applies equally to UPI apps offered by banks.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="UPI market concentration",
  explanation="The cap limits TPAPs to 30% of UPI volume, calculated on the total volume of the preceding three months "
              "on a rolling basis, and NPCI extended the compliance deadline to 31 December 2026. Bank-offered UPI "
              "apps are exempt (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (bank apps exempt)"],
  why="III is wrong; 'I only' omits II.",
  current=ca("2024-12-31"),
  facts=[fact("NPCI extended the deadline for existing TPAPs exceeding the 30% volume cap by two years, until "
              "December 31, 2026; the cap is calculated on the total volume of UPI transactions in the preceding three "
              "months on a rolling basis; it does not apply to UPI apps offered by banks", TPAP_CAP)])

premium, per_txn, per_day = 12, 5, 10  # ₹ lakh
day1 = min(premium, per_day)
txns_day1 = -(-day1 // per_txn)
assert (day1, txns_day1, premium - day1) == (10, 2, 2)
Q(T, "Features", "Advanced",
  "Under the UPI limits effective 15 September 2025 for insurance payments (₹5 lakh per transaction, ₹10 lakh in 24 "
  "hours), a policyholder must pay a premium of ₹12 lakh entirely through UPI. What is the minimum she needs?",
  ["Two transactions totalling ₹10 lakh on day 1 and one of ₹2 lakh after 24 hours",
   "A single ₹12 lakh transaction", "Three transactions of ₹4 lakh on the same day",
   "Twelve transactions of ₹1 lakh on the same day"],
  concept="Applying UPI limits",
  explanation="Within 24 hours she can pay at most ₹10 lakh, and each transaction is capped at ₹5 lakh, so day 1 "
              "needs two ₹5 lakh payments. The remaining ₹2 lakh can go only after the 24-hour window.",
  steps=["Daily cap 10 → day 1 pays 10", "Per-txn cap 5 → 2 transactions", "Balance 2 → next window"],
  why="₹12 lakh exceeds both caps; any same-day plan totalling ₹12 lakh breaches the ₹10 lakh daily limit.",
  computed=True,
  facts=[fact("From September 15, 2025, UPI payments for insurance and capital markets: up to ₹5 lakh per "
              "transaction with a daily limit of ₹10 lakh", UPI_LIMITS)])
Q(T, "UPI Lite and international", "Advanced",
  "Consider the following statements about UPI as described in RBI's payments booklet:\n"
  "I. UPI supports both pull and push payments.\n"
  "II. Non-bank PPI issuers have been allowed to offer UPI to their wallet holders in an interoperable manner.\n"
  "III. UPI can be used only on smartphones.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Reach of UPI",
  explanation="UPI facilitates immediate transfers through pull and push payments (I), and non-bank PPI issuers may "
              "provide UPI to wallet holders interoperably (II). UPI also works on feature phones through USSD "
              "(*99#), so III is wrong.",
  steps=["I: correct", "II: correct", "III: wrong (USSD on feature phones)"],
  why="III is wrong; 'I only' omits II.",
  facts=[fact("UPI facilitates immediate money transfer through pull and push payments; it can be used over smart "
              "phone (app based), feature phone (USSD based); non-bank PPI issuers have also been allowed to provide "
              "this facility in an interoperable manner to their PPI wallet holders", PAY_BOOKLET)])
Q(T, "UPI Lite and international", "Advanced",
  "On UPI's international outreach, RBI's payments booklet notes two developments. Which pair is correct?",
  ["NPCI set up NPCI International Payments Ltd (NIPL) in April 2020, and BIS expressed interest in working with RBI "
   "on a UPI prototype replicable in other countries", "NPCI set up NIPL in 2016, and the IMF took over UPI's "
   "international licensing", "RBI set up NIPL as its own subsidiary in 2020, and the World Bank funded UPI abroad",
   "NIPL was set up in 2008 with NPCI, and SWIFT adopted UPI as its messaging standard"],
  concept="Internationalising UPI",
  explanation="NIPL, a subsidiary of NPCI, was established in April 2020 to export NPCI's offerings (initially RuPay "
              "and UPI) in consultation with RBI. The booklet also notes that BIS expressed interest in working with "
              "RBI to build a prototype of UPI that could be replicated in other countries.",
  steps=["NIPL: NPCI subsidiary, April 2020", "BIS: interest in a replicable UPI prototype"],
  why="NIPL is NPCI's (not RBI's) subsidiary, set up in 2020; the IMF, World Bank and SWIFT roles are invented.",
  facts=[fact("A subsidiary, viz., NPCI International Payments Limited (NIPL), was established in April 2020; BIS has "
              "expressed interest in working with RBI towards building a prototype of the system that could be "
              "replicated and scaled up in other countries", PAY_BOOKLET)])

# ================================================================= 19. NEFT (1 / 1 / 1)
T = "NEFT"
SUB = "Settlement and timings"
Q(T, SUB, "Basic",
  "In NEFT, on what basis does the beneficiary bank give credit to the beneficiary's account?",
  ["Solely on the account number given by the remitter", "On matching both name and account number",
   "Solely on the beneficiary's name", "On the beneficiary's mobile number"],
  concept="Account-number-based credit",
  explanation="RBI's NEFT FAQs state that credit is released solely on the account number in the remitter's "
              "instruction, so the remitter must take care to give the correct number.",
  steps=["Credit based only on account number"],
  why="Name matching, name alone or mobile number are not the basis.",
  facts=[fact("Credit to beneficiary account is released solely based on account number. It is the responsibility of "
              "remitting customer to write correct account number", NEFT_FAQ)])
Q(T, SUB, "Intermediate",
  "When NEFT was implemented in November 2005, how many member banks did it start with, and how had it grown by end-"
  "December 2020?",
  ["Eight banks; 222 member banks with about 1.71 lakh branches", "Four banks; 237 banks",
   "Fourteen banks; 112 banks", "Ten banks; 67 banks"],
  concept="Growth of NEFT",
  explanation="RBI's payments booklet records that NEFT started in November 2005 with only eight member banks and by "
              "end-December 2020 covered 222 member banks and 1,70,996 branches.",
  steps=["Nov 2005: 8 banks", "Dec 2020: 222 banks, 1,70,996 branches"],
  why="Four banks and 237 relate to RTGS; 112 to the NFS network; 10/67 to NPCI's shareholders.",
  facts=[fact("At the time of its implementation in November 2005, NEFT was started with only eight member banks. As "
              "at the end of December 2020, NEFT system covers a network of 222 member banks and their 1,70,996 "
              "branches", PAY_BOOKLET)])
Q(T, SUB, "Advanced",
  "Consider the following statements about NEFT:\n"
  "I. Positive confirmation, relaying the date and time of credit to the originating bank, was introduced from 1 "
  "March 2010.\n"
  "II. Despite being available 24x7, NEFT is not tagged as a 'fast payment' system.\n"
  "III. If credit is not possible, the destination bank must return the transaction within 30 minutes of the "
  "batch.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="NEFT features",
  explanation="Positive confirmation in NEFT began on 1 March 2010 (I). NEFT runs in half-hourly batches, so although "
              "available 24x7 it is not tagged a 'fast payment' system, which needs real-time availability of final "
              "funds (II). Returns must be made within two hours of completion of the batch, not 30 minutes (III "
              "wrong).",
  steps=["I: correct", "II: correct", "III: wrong (two hours)"],
  why="III is wrong; 'I only' omits II.",
  facts=[fact("An element of positive confirmation was introduced with effect from March 1, 2010; notwithstanding its "
              "many features, NEFT is not tagged as a 'fast payment' system", PAY_BOOKLET),
         fact("Destination banks are required to return the transaction within two hours of completion of the batch "
              "in which the transaction was processed", NEFT_FAQ)])


# ================================================================= 20. RTGS (2 / 2 / 1)
T = "RTGS"
SUB = "Limits and timings"
Q(T, SUB, "Basic",
  "RTGS in India began operations on 26 March 2004. How did it start?",
  ["With a soft launch involving four banks", "With all scheduled banks on day one",
   "As a 24x7 system", "As a system operated by NPCI"],
  concept="Origins of RTGS",
  explanation="RBI's December 2020 press release recalls that RTGS began operations on 26 March 2004 with a soft "
              "launch involving four banks; it became 24x7 only in December 2020 and is operated by RBI.",
  steps=["26 March 2004 → soft launch, 4 banks"],
  why="It did not start with all banks or 24x7, and it is RBI-operated.",
  facts=[fact("RTGS, which began its operations on March 26, 2004 with a soft launch involving four banks",
              RTGS_2020)])
Q(T, SUB, "Basic",
  "Which messaging standard does India's RTGS use?",
  ["ISO 20022", "ISO 8583", "SWIFT MT103 only", "ISO 9001"],
  concept="RTGS messaging",
  explanation="RBI says RTGS uses the ISO 20022 format, the best-in-class messaging standard for financial "
              "transactions.",
  steps=["RTGS → ISO 20022"],
  why="ISO 8583 is used for card messages; ISO 9001 is a quality standard; MT103 is not RTGS's format.",
  facts=[fact("RTGS uses ISO 20022 format which is the best-in-class messaging standard for financial transactions",
              RTGS_2020)])
Q(T, SUB, "Intermediate",
  "When announcing RTGS 24x7 in December 2020, what average ticket size did RBI report for RTGS in November 2020?",
  ["₹57.96 lakh", "₹2 lakh", "₹4.17 lakh crore", "₹14,500"],
  concept="RTGS as a large-value system",
  explanation="RBI said RTGS handled 6.35 lakh transactions daily worth ₹4.17 lakh crore across 237 participant banks "
              "and that its average ticket size in November 2020 was ₹57.96 lakh, making it a truly large-value "
              "system.",
  steps=["Average ticket size (Nov 2020) = ₹57.96 lakh"],
  why="₹2 lakh is the minimum amount; ₹4.17 lakh crore is daily value; ₹14,500 is an IMPS-scale figure.",
  facts=[fact("The average ticket size for RTGS in November 2020 was ₹57.96 lakh; RTGS presently handles 6.35 lakh "
              "transactions daily for a value of ₹4.17 lakh crore across 237 participant banks", RTGS_2020)])
Q(T, SUB, "Intermediate",
  "According to RBI's RTGS FAQs updated in October 2026, what must RTGS members do for transactions relating to the "
  "Foreign Contribution (Regulation) Act, 2010?",
  ["Use the prescribed transaction type codes for such transactions", "Route them only through NEFT",
   "Obtain RBI's prior approval for each transaction", "Settle them in a separate end-of-day batch"],
  concept="Special RTGS requirements",
  explanation="The FAQs state that RTGS members must use the prescribed transaction type codes for FCRA-related "
              "transactions wherever applicable, and customers should give accurate purpose information.",
  steps=["FCRA transactions → prescribed transaction type codes"],
  why="No NEFT-only routing, per-transaction approval or separate batch is prescribed.",
  current=ca("2026-10-14"),
  facts=[fact("RTGS members must use the prescribed transaction type codes for transactions relating to the Foreign "
              "Contribution (Regulation) Act, 2010, wherever applicable", RTGS_FAQ)])

vol, val = 6.35e5, 4.17e5  # transactions per day; ₹ crore per day
avg_lakh = val / vol * 100
assert round(avg_lakh, 1) == 65.7 and avg_lakh > 57.96
Q(T, SUB, "Advanced",
  "In December 2020 RBI said RTGS handled 6.35 lakh transactions a day worth ₹4.17 lakh crore, and that the average "
  "ticket size in November 2020 was ₹57.96 lakh. What average ticket size do the daily figures imply, and how does "
  "it compare?",
  ["About ₹65.7 lakh, higher than the November average", "About ₹6.57 lakh, far lower than the November average",
   "About ₹57.96 lakh, identical", "About ₹6.57 crore, about ten times the November average"],
  concept="Average ticket size",
  explanation="₹4.17 lakh crore ÷ 6.35 lakh transactions = ₹4,17,000 crore ÷ 6,35,000 ≈ ₹0.657 crore ≈ ₹65.7 lakh, "
              "higher than November's ₹57.96 lakh (the daily figures need not match a single month's average).",
  steps=["4,17,000 crore ÷ 6,35,000 = 0.657 crore", "= ₹65.7 lakh > ₹57.96 lakh"],
  why="₹6.57 lakh and ₹6.57 crore are off by a factor of ten; the figures are not identical.",
  computed=True,
  facts=[fact("RTGS presently handles 6.35 lakh transactions daily for a value of ₹4.17 lakh crore; the average ticket "
              "size for RTGS in November 2020 was ₹57.96 lakh", RTGS_2020)])


# ================================================================= 21. IMPS (1 / 1 / 1)
T = "IMPS"
SUB = "Limits and features"
Q(T, SUB, "Basic",
  "RBI's payments booklet classifies IMPS and UPI as 'fast payment' systems. Which two key features define fast "
  "payments?",
  ["Speed and continuous service availability", "Low cost and paper-based processing",
   "Batch settlement and high value", "Cheque-based clearing and netting"],
  concept="Fast payments",
  explanation="Fast payments are defined by speed and continuous service availability, with transmission of the "
              "payment message and availability of final funds to the payee in real time, round the clock.",
  steps=["Fast payment = speed + continuous availability"],
  why="Batch, paper or cheque-based features are the opposite of fast payments.",
  facts=[fact("Fast payments are defined by two key features, speed and continuous service availability", PAY_BOOKLET)])
Q(T, SUB, "Intermediate",
  "What early feature of IMPS inhibited its growth, leading to upgrades that allowed transfers using other "
  "parameters?",
  ["Both the remitter and the beneficiary had to be registered for mobile banking",
   "It worked only during banking hours", "It allowed only government payments", "It needed a physical cheque"],
  concept="Evolution of IMPS",
  explanation="RBI's booklet notes that IMPS initially required both remitter and beneficiary to be registered for "
              "mobile banking, which inhibited growth; it was then upgraded to allow remittances using other "
              "parameters such as account number and IFSC.",
  steps=["Initial constraint: both parties on mobile banking", "Upgrade: other identifiers allowed"],
  why="IMPS was always 24x7, general-purpose and paperless.",
  facts=[fact("Initially, the system required both the remitter and the beneficiary to be registered for mobile "
              "banking which was inhibiting the growth. Hence, the system was upgraded to enable remittance of funds "
              "by using other parameters", PAY_BOOKLET)])
Q(T, SUB, "Advanced",
  "Consider the following statements from RBI's payments booklet:\n"
  "I. NEFT, though available round the clock, is not tagged as a fast payment system.\n"
  "II. IMPS facilitates push transactions.\n"
  "III. IMPS cannot be accessed through bank branches or Business Correspondents.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="IMPS compared with NEFT",
  explanation="NEFT works in half-hourly batches and is not tagged a fast payment system (I). IMPS is a 24x7 fast "
              "payment system that facilitates push transactions (II). IMPS is multi-channel—mobile, ATM, internet "
              "banking, branches and BCs—so III is wrong.",
  steps=["I: correct", "II: correct", "III: wrong (multi-channel)"],
  why="III is wrong; 'I only' omits II.",
  facts=[fact("NEFT is not tagged as a 'fast payment' system; IMPS is a 24*7 'fast payments' system that facilitates "
              "push transactions; IMPS is a multi-channel system that can be accessed using mobile, ATM, internet "
              "banking, bank branches, BCs", PAY_BOOKLET)])


# ================================================================= 22. NPCI (1 / 2 / 2)
T = "NPCI"
SUB = "Products: NACH, AePS, RuPay, FASTag"
Q(T, SUB, "Basic",
  "NPCI started with 10 core promoter banks as shareholders. Which of the following was NOT one of them?",
  ["Axis Bank", "HSBC", "Citibank N.A.", "Canara Bank"],
  concept="NPCI's ownership",
  explanation="NPCI's 10 core promoters were SBI, PNB, Canara Bank, Bank of Baroda, Union Bank of India, Bank of "
              "India, ICICI Bank, HDFC Bank, Citibank N.A. and HSBC. Its shareholding was broad-based in 2016.",
  steps=["Promoters: SBI, PNB, Canara, BoB, Union, BoI, ICICI, HDFC, Citibank, HSBC"],
  why="HSBC, Citibank and Canara Bank were promoters.",
  facts=[fact("NPCI started with 10 core promoter banks (State Bank of India, Punjab National Bank, Canara Bank, Bank "
              "of Baroda, Union Bank of India, Bank of India, ICICI Bank, HDFC Bank, Citibank N. A. and HSBC); in "
              "2016 the shareholding was broad-based", PAY_BOOKLET)])
Q(T, SUB, "Intermediate",
  "Which RBI document first envisioned an umbrella organisation for all retail payment systems, leading to NPCI?",
  ["RBI's Vision for Payment Systems 2005-08", "Narasimham Committee Report, 1991",
   "Payment System Vision 2019-21", "Nachiket Mor Committee Report, 2014"],
  concept="Genesis of NPCI",
  explanation="RBI's Vision for Payment Systems 2005-08 envisioned an umbrella organisation for retail payments; NPCI "
              "was then incorporated in December 2008 with RBI and IBA's support.",
  steps=["Vision 2005-08 → umbrella organisation → NPCI (Dec 2008)"],
  why="The 1991 report was on banking reform; Vision 2019-21 came long after; Nachiket Mor dealt with inclusion.",
  facts=[fact("RBI, in its Vision for Payment Systems 2005-08, envisioned the need for an umbrella organisation for "
              "all the retail payment systems in the country; NPCI was incorporated in December 2008", PAY_BOOKLET)])
Q(T, SUB, "Intermediate",
  "e-RUPI, launched on 2 August 2021 by the Prime Minister and developed by NPCI, is best described as:",
  ["A voucher-based, cashless and contactless payment instrument delivered as an SMS string or QR code",
   "RBI's retail central bank digital currency", "A credit card for government employees",
   "A new denomination of the rupee coin"],
  concept="e-RUPI",
  explanation="e-RUPI is a person- and purpose-specific prepaid digital voucher on NPCI's UPI platform, issued by "
              "onboarded banks and delivered as an SMS string or QR code. It is distinct from RBI's e₹ (CBDC).",
  steps=["e-RUPI = prepaid digital voucher (NPCI)", "e₹ = CBDC (RBI)"],
  why="It is not the CBDC, a credit card or a coin.",
  facts=[fact("e-RUPI, launched on August 2, 2021, is a voucher-based payments system launched by NPCI to promote "
              "cashless and contactless transactions; recipients receive it as an SMS string or QR code", ERUPI)])
Q(T, SUB, "Advanced",
  "Consider the following statements about RBI's oversight of payment systems, from its payments booklet:\n"
  "I. RBI conducts on-site inspection of entities such as CCIL, NPCI, PPI issuers, WLA operators and TReDS "
  "operators.\n"
  "II. CCIL and NPCI are assessed against the 24 Principles for Financial Market Infrastructures (PFMIs) of "
  "CPMI-IOSCO.\n"
  "III. NPCI, being a not-for-profit company, is outside RBI's supervision.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Oversight of FMIs",
  explanation="RBI inspects CCIL, NPCI, PPI issuers, WLA operators, ATM network operators and TReDS operators; CCIL "
              "and NPCI are assessed against the 24 PFMIs. NPCI's not-for-profit status does not take it outside RBI "
              "oversight (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong"],
  why="III is wrong; 'I only' omits II.",
  facts=[fact("RBI conducts onsite inspection of CCIL, NPCI, authorised PPI issuers, White Label ATM Operators, ATM "
              "Network Operators, Instant Money Transfer Operator and TReDS Operators. Of these, CCIL and NPCI are "
              "assessed against the 24 PFMIs", PAY_BOOKLET)])
Q(T, SUB, "Advanced",
  "Consider the following statements about micro-ATMs used by Business Correspondents, as described by RBI:\n"
  "I. A micro-ATM has no cash storage or dispensing facility; the BC handles the physical cash.\n"
  "II. IBA, IDRBT, NPCI and UIDAI are the custodians of micro-ATM standards.\n"
  "III. Supported authentication modes include Aadhaar + biometric, Aadhaar + OTP and Card + PIN.\n"
  "Which is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I and III only"],
  concept="Micro-ATMs and AePS",
  explanation="A micro-ATM is a BC's device without cash storage; cash is handled by the BC (I). IBA, IDRBT, NPCI and "
              "UIDAI are custodians of the standards, with RBI regulating the platform (II). Authentication modes "
              "include Aadhaar + biometric, Aadhaar + OTP, Card + biometric, Card + OTP and Card + PIN (III).",
  steps=["I ✓", "II ✓", "III ✓"],
  why="All three are correct, so partial options are wrong.",
  facts=[fact("Micro-ATM does not have cash storage or dispensation facilities; means of authentication: Aadhaar + "
              "Biometric, Aadhaar + OTP, Card + Biometric, Card + OTP and Card + PIN; IBA, IDRBT, NPCI and UIDAI are "
              "the custodians of the micro-ATM standards", PAY_BOOKLET)])


# ================================================================= 23. Payment Banks (1 / 3 / 2)
T = "Payment Banks"
Q(T, "Permitted activities", "Basic",
  "Under RBI's 2014 guidelines, which of the following can a payments bank NOT do?",
  ["Undertake lending activities", "Accept demand deposits", "Act as a business correspondent of another bank",
   "Offer payments and remittance services"],
  concept="Scope of payments banks",
  explanation="Payments banks may accept demand deposits, issue ATM/debit cards, offer payments and remittances, act "
              "as BCs of other banks and distribute simple products, but they cannot undertake lending.",
  steps=["Deployment of funds: no lending"],
  why="The other three are permitted activities.",
  facts=[fact("The payments bank cannot undertake lending activities; scope: acceptance of demand deposits, payments "
              "and remittance services, BC of another bank", PB_GUIDE)])
Q(T, "Permitted activities", "Intermediate",
  "After the business restrictions on Paytm Payments Bank took effect on 15 March 2024, which credits could still "
  "be received in its customers' accounts?",
  ["Only interest, cashbacks, sweep-in from partner banks and refunds", "Salary credits and DBT subsidies",
   "Any credit up to ₹2 lakh", "No credits of any kind"],
  concept="Supervisory restrictions on a payments bank",
  explanation="RBI's FAQs state that after 15 March 2024 no credits or deposits are allowed other than interest, "
              "cashbacks, sweep-in from partner banks and refunds; salary and DBT credits stopped.",
  steps=["Allowed: interest, cashback, sweep-in, refunds"],
  why="Salary/DBT credits were barred; there was no general ₹2 lakh window; some credits remained allowed.",
  facts=[fact("After March 15, 2024, no credits or deposits other than interest, cashbacks, sweep-in from partner "
              "banks or refunds are allowed to be credited", PAYTM_FAQ)])
Q(T, "Permitted activities", "Intermediate",
  "Which entities were eligible to promote payments banks under RBI's licensing guidelines of November 2014?",
  ["Existing non-bank PPI issuers and others such as NBFCs, corporate BCs, mobile telephone companies and super-market "
   "chains owned and controlled by residents, with a five-year track record",
   "Only scheduled commercial banks", "Only foreign banks with Indian branches",
   "Only public sector undertakings"],
  concept="Promoters of payments banks",
  explanation="Eligible promoters included existing non-bank PPI issuers, individuals/professionals, NBFCs, corporate "
              "BCs, mobile telephone companies, super-market chains, companies and real-sector co-operatives owned "
              "and controlled by residents, and public sector entities, with at least five years of track record.",
  steps=["Wide range of resident-controlled promoters", "Fit and proper; 5-year track record"],
  why="Eligibility was not limited to banks, foreign banks or PSUs.",
  facts=[fact("Eligible promoters: existing non-bank PPI issuers; and other entities such as individuals / "
              "professionals; NBFCs, corporate BCs, mobile telephone companies, super-market chains, companies, real "
              "sector cooperatives; that are owned and controlled by residents; and public sector entities; track "
              "record of at least five years", PB_GUIDE)])
Q(T, "Permitted activities", "Intermediate",
  "The payments bank licensing framework of November 2014 followed which announcement?",
  ["The Union Budget 2014-15 (10 July 2014), which said RBI would create a framework for small and differentiated "
   "banks", "The Narasimham Committee report of 1998", "The PMJDY launch on 28 August 2014",
   "The Banking Laws (Amendment) Act, 2012"],
  concept="Differentiated banks",
  explanation="The Finance Minister's Budget 2014-15 speech (10 July 2014) said RBI would create a framework for "
              "licensing small banks and other differentiated banks such as payment banks. RBI issued draft "
              "guidelines on 17 July 2014 and final ones on 27 November 2014.",
  steps=["10 Jul 2014: Budget announcement", "17 Jul 2014: draft", "27 Nov 2014: final guidelines"],
  why="The guidelines cite the Budget announcement, not the other events.",
  facts=[fact("In the Union Budget 2014-2015 presented on July 10, 2014, the Finance Minister announced that RBI will "
              "create a framework for licensing small banks and other differentiated banks; draft guidelines were "
              "released on July 17, 2014", PB_GUIDE)])
Q(T, "Deposit limit", "Advanced",
  "After 15 March 2024, a customer of Paytm Payments Bank with money in his account finds four transactions pending:\n"
  "P. His employer's salary credit\n"
  "Q. An NACH debit for his loan EMI, within the available balance\n"
  "R. A recharge of his FASTag issued by Paytm Payments Bank\n"
  "S. A refund from a cancelled online order\n"
  "Which can go through?",
  ["Q and S only", "P and Q only", "Q, R and S only", "S only"],
  concept="Applying the restrictions",
  explanation="Debits, including NACH mandates, continue up to the available balance (Q). Credits are barred except "
              "interest, cashbacks, sweep-in and refunds, so the refund goes through (S) but salary does not (P). "
              "FASTags issued by the bank cannot be topped up (R).",
  steps=["P ✗ (salary credit)", "Q ✓ (debit within balance)", "R ✗ (FASTag top-up)", "S ✓ (refund)"],
  why="Options with P or R are wrong; 'S only' wrongly blocks the EMI debit.",
  facts=[fact("Withdrawal/debit mandates (such as NACH mandates) will continue to get executed till there is balance "
              "available; after March 15, 2024 you will not be able to receive salary credits; refunds are permitted; "
              "you will not be able to top-up or recharge your FASTag issued by Paytm Payments Bank", PAYTM_FAQ)])
Q(T, "Permitted activities", "Advanced",
  "Consider the following statements about RBI's 2014 payments bank guidelines:\n"
  "I. Applications were to be evaluated by an External Advisory Committee, with RBI taking the final decision.\n"
  "II. Applications were to be made under Rule 11 of the Banking Regulation (Companies) Rules, 1949 in Form III.\n"
  "III. A scheduled commercial bank was barred from taking any equity stake in a payments bank.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Licensing process",
  explanation="An EAC of eminent professionals evaluated applications, with RBI's decision final (I); applications "
              "were in Form III under Rule 11 (II). A promoter could form a JV with an existing SCB, and an SCB could "
              "take equity to the extent permitted under Section 19(2) of the BR Act (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (allowed within Section 19(2))"],
  why="III is wrong; 'I only' omits II.",
  facts=[fact("An External Advisory Committee will evaluate the applications; the decision will be taken by the "
              "Reserve Bank; applications under Rule 11 of the Banking Regulation (Companies) Rules, 1949 in Form III; "
              "scheduled commercial bank can take equity stake in a payments bank to the extent permitted under "
              "Section 19 (2) of the Banking Regulation Act, 1949", PB_GUIDE)])


# ================================================================= 24. Small Finance Banks (1 / 1 / 1)
T = "Small Finance Banks"
Q(T, "Licensing norms", "Basic",
  "Under RBI's 2014 guidelines for small finance banks, which existing entities owned and controlled by residents "
  "could opt to convert into SFBs?",
  ["NBFCs, micro finance institutions and local area banks", "Only regional rural banks",
   "Only urban co-operative banks", "Foreign bank branches"],
  concept="Conversion into SFBs",
  explanation="The 2014 guidelines allowed existing NBFCs, MFIs and Local Area Banks owned and controlled by residents "
              "to opt for conversion into small finance banks.",
  steps=["NBFC / MFI / LAB → may convert to SFB"],
  why="RRBs, UCBs (under the 2014 framework) and foreign bank branches were not the categories named.",
  facts=[fact("Existing NBFCs, MFIs and Local Area Banks (LABs) that are owned and controlled by residents can also "
              "opt for conversion into small finance banks", SFB_GUIDE)])
Q(T, "Licensing norms", "Intermediate",
  "Under the 2014 SFB guidelines, which individuals were eligible to promote a small finance bank?",
  ["Resident individuals/professionals with 10 years of experience in banking and finance",
   "Any individual with a net worth of ₹100 crore", "Only retired bankers above 60",
   "Non-resident Indians with 5 years of experience"],
  concept="SFB promoters",
  explanation="Resident individuals and professionals with 10 years of experience in banking and finance, and "
              "companies and societies owned and controlled by residents, were eligible.",
  steps=["Individuals: resident + 10 years in banking/finance"],
  why="Net worth, age or NRI status was not the criterion.",
  facts=[fact("Resident individuals/professionals with 10 years of experience in banking and finance; and companies "
              "and societies owned and controlled by residents will be eligible to set up small finance banks",
              SFB_GUIDE)])
Q(T, "PSL targets", "Advanced",
  "Consider the following statements about RBI's 2014 small finance bank guidelines:\n"
  "I. There was no restriction on the area of operations of SFBs.\n"
  "II. An SFB would automatically become a universal bank after five years.\n"
  "III. SFBs were subject to all prudential norms applicable to commercial banks, including CRR and SLR, with no "
  "forbearance, and had to extend 75% of ANBC to priority sector.\n"
  "Which is/are correct?",
  ["I and III only", "I only", "II and III only", "I, II and III"],
  concept="SFB framework of 2014",
  explanation="SFBs had no restriction on area of operations (I) and were subject to all prudential norms including "
              "CRR and SLR with no forbearance, with 75% of ANBC to PSL under the 2014 guidelines (III). Transition to "
              "a universal bank was not automatic; it depended on capital, track record and RBI's due diligence (II "
              "wrong).",
  steps=["I: correct", "II: wrong (not automatic)", "III: correct"],
  why="II is wrong; 'I only' omits III.",
  facts=[fact("There will not be any restriction in the area of operations of small finance banks; subject to all "
              "prudential norms including CRR and SLR, no forbearance; 75 per cent of ANBC to priority sector; "
              "transition into a universal bank will not be automatic", SFB_GUIDE)])

# ================================================================= 25. Financial Markets (1 / 4 / 1)
T = "Financial Markets"
SUB = "Structure and regulators"
Q(T, SUB, "Basic",
  "NDS-OM, the anonymous screen-based order-matching system for government securities, was introduced by RBI in "
  "August 2005. Who operates it on RBI's behalf?",
  ["The Clearing Corporation of India Ltd (CCIL)", "NPCI", "NSDL", "FIMMDA"],
  concept="G-sec trading platform",
  explanation="RBI's G-sec primer states that NDS-OM, introduced in August 2005, is an order-driven anonymous trading "
              "system operated by CCIL on behalf of RBI.",
  steps=["NDS-OM (Aug 2005) → operated by CCIL for RBI"],
  why="NPCI runs retail payments, NSDL is a depository and FIMMDA is a market association.",
  facts=[fact("In August 2005, RBI introduced an anonymous screen-based order matching module called NDS-OM; NDS-OM is "
              "operated by the CCIL on behalf of the RBI", GSEC_FAQ)])
Q(T, SUB, "Intermediate",
  "From 31 March 2018, which entity took over from FIMMDA the responsibility for administering valuation of "
  "government securities?",
  ["Financial Benchmarks India Pvt. Ltd (FBIL)", "CCIL", "SEBI", "The Public Debt Office of RBI"],
  concept="Benchmark administration",
  explanation="RBI advised FBIL to assume responsibility for valuation of government securities with effect from 31 "
              "March 2018; FIMMDA ceased publishing G-sec prices/yields.",
  steps=["31 March 2018 → FBIL administers G-sec valuation"],
  why="CCIL, SEBI and the PDO do not publish these valuation benchmarks.",
  facts=[fact("FBIL has been advised to assume the responsibility for administering valuation of Government "
              "securities with effect from March 31, 2018; FIMMDA has ceased to publish prices/yield of Government "
              "securities", GSEC_FAQ)])
Q(T, SUB, "Intermediate",
  "Under the Sovereign Gold Bond Scheme, what is the maximum subscription per fiscal year for an individual and for "
  "a trust?",
  ["4 kg for an individual and 20 kg for a trust", "1 kg and 10 kg", "500 g and 4 kg", "No limit for either"],
  concept="SGB limits",
  explanation="SGBs are issued in multiples of one gram, with a maximum of 4 kg for individuals, 4 kg for HUFs and 20 "
              "kg for trusts and similar entities per fiscal year; they bear 2.5% fixed interest.",
  steps=["Individual / HUF: 4 kg", "Trusts: 20 kg"],
  why="The other limits do not match the scheme.",
  facts=[fact("Maximum limit of subscription of 4 kg for individuals, 4 kg for HUF and 20 kg for trusts and similar "
              "entities per fiscal year; the Bonds bear interest at the rate of 2.50 per cent per annum", SGB_FAQ)])
Q(T, SUB, "Intermediate",
  "RBI constituted the Technical Consultative Committee for Financial Markets (TCCFM) on 4 November 2026. Who chairs "
  "it, and how often must it meet?",
  ["The Deputy Governor in charge of the Financial Markets Regulation Department; at least once a quarter",
   "The Governor; once a year", "The Chairman of FIMMDA; every month", "The Finance Secretary; twice a year"],
  concept="Market consultation forum",
  explanation="The TCCFM is chaired by the Deputy Governor in charge of FMRD, has external members from markets and "
              "institutions, and meets at least once a quarter.",
  steps=["Chair: DG in charge of FMRD", "Meetings: at least quarterly"],
  why="The Governor, FIMMDA's chairman (an external member) and the Finance Secretary do not chair it.",
  current=ca("2026-11-04"),
  facts=[fact("The Committee will be Chaired by the Deputy Governor (DG) in charge of the Financial Markets Regulation "
              "Department (FMRD); the meetings of the Committee will be convened at least once a quarter", TCCFM)])
Q(T, SUB, "Intermediate",
  "What did RBI announce in February 2026 about the Voluntary Retention Route (VRR) for FPI investment in debt?",
  ["The ₹2.5 lakh crore VRR limit would be removed, with VRR investment counted under the General Route ceilings",
   "The VRR would be closed to new investment", "The VRR limit would be doubled to ₹5 lakh crore",
   "VRR investments would be exempt from all limits"],
  concept="Foreign portfolio investment in debt",
  explanation="With over 80% of the ₹2.5 lakh crore VRR limit used, RBI decided that VRR investment would be reckoned "
              "under the General Route limits, effectively removing the separate ₹2.5 lakh crore cap, with more "
              "operational flexibility.",
  steps=["Old: separate ₹2.5 lakh crore limit", "New: counted within General Route ceilings"],
  why="The route was not closed, doubled or freed of all limits.",
  current=ca(FEB26),
  facts=[fact("We also propose to remove the limit of ₹2.5 lakh crore for investments under the VRR. Investment "
              "through the VRR in each category of securities will be subject to the investment ceiling for the "
              "respective category under the General Route", GOV_FEB26)])
Q(T, SUB, "Advanced",
  "Consider the following statements about 'when issued' trading and short sales in government securities, as "
  "described in RBI's G-sec primer:\n"
  "I. 'When issued' transactions are undertaken only on NDS-OM and cease at the close of trading on the auction "
  "date.\n"
  "II. All 'when issued' transactions are contracted for settlement on the date of issue.\n"
  "III. For liquid securities, up to 10% of the outstanding stock of a security can be short sold.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="WI market and short selling",
  explanation="WI trading takes place on NDS-OM from notification until close of trading on the auction date (I), "
              "with all trades settled on the issue date (II). The short-sale limit for liquid securities is 2% of "
              "the outstanding stock, not 10% (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (2%)"],
  why="III is wrong; 'I only' omits II.",
  facts=[fact("When Issued transactions would commence after the issue of a security is notified and cease at the "
              "close of trading on the date of auction; all When Issued transactions shall be contracted for "
              "settlement on the date of issue; undertaken only on NDS-OM; maximum short sale for liquid securities 2% "
              "of the total outstanding stock of each security", GSEC_FAQ)])


# ================================================================= 26. Money Market (3 / 1 / 1)
T = "Money Market"
SUB = "Instruments: T-bills, CP, CD, call money"
Q(T, SUB, "Basic",
  "Certificates of Deposit and Commercial Paper were introduced in India in:",
  ["March 1989", "April 1988", "November 1986", "June 1997"],
  concept="Development of money market instruments",
  explanation="RBI's chronology records that CDs and CPs were introduced in March 1989 to widen the range of "
              "money market instruments.",
  steps=["March 1989 → CDs and CPs"],
  why="April 1988 is DFHI; November 1986 the 182-day T-bill; June 1997 the 14-day T-bill.",
  facts=[fact("Mar 1989: Certificates of Deposit (CDs) and Commercial Paper (CPs) introduced in India to widen the "
              "monetary instruments", CHRON_85)])
Q(T, SUB, "Basic",
  "In RBI's Treasury Bill auction of 4 November 2026, notified at ₹8,000 crore each for 91-day and 182-day bills and "
  "₹7,000 crore for 364-day bills, what happened in the 182-day auction?",
  ["No bids were accepted", "The full ₹8,000 crore was accepted at a yield of 5.90%",
   "It was oversubscribed and accepted at 6.65%", "It was converted into a cash management bill"],
  concept="T-bill auctions",
  explanation="RBI accepted the full amounts in the 91-day (cut-off yield about 5.90%) and 364-day (about 6.65%) "
              "auctions, but the face value accepted in the 182-day auction was nil.",
  steps=["91-day: ₹8,000 crore accepted", "182-day: NIL", "364-day: ₹7,000 crore accepted"],
  why="5.90% and 6.65% were the 91-day and 364-day yields; no conversion took place.",
  current=ca("2026-11-04"),
  facts=[fact("T-Bill auction result November 04, 2026: 91-day ₹8,000 crore accepted (YTM 5.8970%); 182-day total face "
              "value accepted NIL; 364-day ₹7,000 crore accepted (YTM 6.6485%)", TBILL_NOV4)])
Q(T, SUB, "Basic",
  "During the 1973 oil shock, the call money rate rose to an all-time high. What was it, and what did the Indian "
  "Banks' Association do?",
  ["30%; IBA intervened and fixed a ceiling of 15%", "15%; IBA fixed a floor of 10%", "50%; RBI closed the call "
   "market", "20%; IBA abolished call money"],
  concept="Call money history",
  explanation="RBI's chronology says the call money rate rose to an all-time high of 30% in 1973, prompting the IBA "
              "to intervene and fix a ceiling of 15%.",
  steps=["1973: call rate 30%", "IBA ceiling: 15%"],
  why="The other figures and actions are not recorded.",
  facts=[fact("1973: Call money rate rose to an all time high of 30% prompting the Indian Banks' Association to "
              "intervene and fix a ceiling of 15%", CHRON_68)])
Q(T, SUB, "Intermediate",
  "Under RBI's non-competitive bidding facility for retail investors in G-sec and T-bill auctions, what share of the "
  "notified amount is set aside, and how do investors participate?",
  ["Up to 5% of the notified amount, through an aggregator such as a scheduled bank, primary dealer or specified "
   "stock exchange", "Up to 25%, directly with RBI", "Exactly 10%, only through post offices",
   "Up to 2%, only through mutual funds"],
  concept="Non-competitive bidding",
  explanation="Non-competitive bids up to 5% of the notified amount are allowed within it. Retail investors cannot bid "
              "directly; they come through an aggregator/facilitator, with a minimum bid of ₹10,000, and are allotted "
              "at the weighted average price of competitive bids.",
  steps=["Reserve: up to 5%", "Via aggregator", "Minimum ₹10,000"],
  why="25%, 10% (that is for SDLs) and 2% are not the facility for central auctions; the routes are wrong.",
  facts=[fact("Non-competitive bids up to 5 per cent of the notified amount will be allowed; eligible investors have to "
              "come through an aggregator or facilitator (Scheduled Bank, Primary Dealer or Specified Stock "
              "Exchange); minimum amount Rs.10,000", NCB_FAQ)])

notified = 8_000
reserved = 0.05 * notified
bids = 500
ratio = reserved / bids
alloc = 10 * ratio  # ₹ lakh
fee = alloc * 1e5 / 100 * 0.06
assert (reserved, ratio, alloc, round(fee)) == (400, 0.8, 8.0, 480)
Q(T, SUB, "Advanced",
  "In a T-bill auction notified at ₹8,000 crore, the non-competitive segment (5% of the notified amount) receives "
  "bids of ₹500 crore. An investor bids ₹10 lakh through her bank, which charges the maximum permitted commission. "
  "What does she get, and what is the commission?",
  ["₹8 lakh of T-bills; commission up to ₹480", "₹10 lakh; commission ₹600", "₹8 lakh; commission ₹800",
   "₹4 lakh; commission ₹240"],
  concept="Pro-rata allotment and aggregator commission",
  explanation="Reserved amount = 5% × 8,000 = ₹400 crore. Bids of ₹500 crore exceed it, so allotment is pro rata: "
              "400/500 = 80%, giving ₹8 lakh. The aggregator may recover up to 6 paise per ₹100: 8,00,000 / 100 × "
              "0.06 = ₹480.",
  steps=["Reserve = ₹400 crore", "Ratio = 400/500 = 80%", "Allotment = ₹8 lakh", "Commission = ₹480"],
  why="₹10 lakh ignores pro-rata allotment; ₹800 uses 10 paise; ₹4 lakh halves the ratio.",
  computed=True,
  facts=[fact("Non-competitive bids up to 5 per cent of the notified amount; if the aggregate amount bid is more than "
              "the reserved amount, allotment would be made on a pro rata basis; the aggregator can recover up to six "
              "paise per Rs.100 as commission", NCB_FAQ)])


# ================================================================= 27. Capital Market (1 / 3 / 4)
T = "Capital Market"
SEP24 = "2026-09-24"
Q(T, "SEBI", "Basic",
  "According to SEBI, what is 'dabba trading'?",
  ["Illegal trading in which deals are settled internally by an operator without being executed on a recognised "
   "stock exchange", "Trading in small-cap shares on the SME platform", "Algorithmic trading by brokers",
   "Trading in government securities on NDS-OM"],
  concept="Investor protection",
  explanation="SEBI describes dabba trading as an illegal, unregulated form of trading where deals are not executed "
              "on any SEBI-recognised exchange but settled internally by the dabba operator, leaving investors "
              "without exchange grievance redress or guaranteed settlement.",
  steps=["Off-exchange, internally settled → illegal"],
  why="SME trading, algo trading and NDS-OM trades are legitimate regulated activities.",
  facts=[fact("Dabba trading is an illegal and unregulated form of trading in securities; traders place deals without "
              "the trades actually being executed on any official SEBI recognized stock exchange; settled internally "
              "by the dabba operator", SEBI_DABBA)])
Q(T, "Primary and secondary market", "Intermediate",
  "When an investor applies in an IPO through ASBA (Application Supported by Blocked Amount), what happens to the "
  "application money?",
  ["It stays in her account, blocked and earning interest, and is debited only on allotment",
   "It is transferred to the issuer at once and refunded if shares are not allotted",
   "It is moved to an escrow account and earns no interest", "It is held by the stock exchange until listing"],
  concept="ASBA",
  explanation="Under ASBA the amount is blocked but remains in the investor's account until allotment, continues to "
              "earn interest, and is debited only on allotment; no refund is needed if shares are not allotted. UPI "
              "can be used as the payment mechanism.",
  steps=["Amount blocked in own account", "Earns interest", "Debited on allotment"],
  why="ASBA avoids transfer-and-refund, escrow without interest and exchange custody of funds.",
  facts=[fact("In ASBA, money to the extent of price of the shares applied for is blocked, but it remains in their "
              "account till allotment; blocked amount continues to earn interest and there is no requirement of "
              "refund in case of non-allotment", SEBI_ASBA)])
Q(T, "SEBI", "Intermediate",
  "World Investor Week 2026, celebrated in India from 5 to 11 October 2026, is a global investor-awareness "
  "initiative of:",
  ["IOSCO (International Organization of Securities Commissions)", "The IMF", "The Bank for International "
   "Settlements", "The World Bank"],
  concept="Investor education",
  explanation="SEBI's investor site describes World Investor Week as an IOSCO initiative for global investor "
              "awareness, celebrated every year by securities regulators; in India in 2026 it ran from 5 to 11 "
              "October.",
  steps=["WIW → IOSCO", "India: 5–11 Oct 2026"],
  why="The IMF, BIS and World Bank do not run World Investor Week.",
  current=ca("2026-10-05"),
  facts=[fact("World Investor Week 2026 initiative by IOSCO for global investor awareness campaign; it is being "
              "celebrated in India from October 5 to 11, 2026", SEBI_WIW)])
Q(T, "Primary and secondary market", "Intermediate",
  "According to RBI's chronology, which depository institution commenced operations in August 1988?",
  ["Stock Holding Corporation of India Ltd (SHCIL)", "NSDL", "CDSL", "Clearing Corporation of India Ltd"],
  concept="Market infrastructure history",
  explanation="RBI's chronology records that SHCIL, a depository institution, commenced operations in August 1988. "
              "NSDL came in 1996, CDSL in 1999 and CCIL in 2001.",
  steps=["Aug 1988 → SHCIL"],
  why="The other institutions came later.",
  facts=[fact("Aug 1988: Stock Holding Corporation of India Ltd. (SHCIL) a depository institution commenced "
              "operations", CHRON_85)])
Q(T, "SEBI", "Advanced",
  "At its 215th meeting on 24 September 2026, SEBI's Board approved new Portfolio Managers Regulations, 2026. "
  "Consider:\n"
  "I. Discretionary PMS may invest up to 10% of client AUM in investment-grade, non-convertible, unlisted debt "
  "securities with client consent.\n"
  "II. Investment in exchange-traded derivatives is permitted up to 1.25 times the client's AUM.\n"
  "III. The new regulations retain the 2020 regulations alongside them.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Portfolio management regulation",
  explanation="The Board approved PMS Regulations, 2026 in supersession of (not alongside) the 2020 regulations (III "
              "wrong). Measures include up to 10% of AUM in investment-grade unlisted NCDs under discretionary PMS "
              "with consent (I) and derivatives up to 1.25 times AUM (II).",
  steps=["I: correct", "II: correct", "III: wrong (supersession)"],
  why="III is wrong; 'I only' omits II.",
  current=ca(SEP24),
  facts=[fact("The Board approved the proposal to introduce SEBI (Portfolio Managers) Regulations, 2026 in "
              "supersession of SEBI (Portfolio Managers) Regulations, 2020; enabling investment upto 10% of client AUM "
              "in investment-grade, non-convertible, unlisted debt securities under DPMS with client consent; "
              "investment in Exchange traded Derivatives up to 1.25 times of client's AUM", SEBI_SEP26)])
Q(T, "SEBI", "Advanced",
  "Which set of items was among the approvals of SEBI's Board on 24 September 2026?",
  ["Settlement Regulations, 2026 replacing the 2018 settlement regulations, a Common Advertisement Code for specified "
   "regulated entities, and FPI participation in exchange-traded commodity derivatives",
   "Abolition of the T+1 settlement cycle and a return to T+2", "A ban on all IPOs on the SME platform",
   "Merger of NSE and BSE"],
  concept="SEBI's 2026 reforms",
  explanation="PR No. 59/2026 lists approvals including the SEBI Settlement Regulations, 2026 (replacing the 2018 "
              "regulations, in force from the day after the 30th day from notification), a Common Advertisement Code, "
              "FPI participation in ETCDs, Vault Manager amendments, DRs on REIT/InvIT units and a Settlement Scheme "
              "for illiquid stock options.",
  steps=["Settlement Regs 2026", "Common Advertisement Code", "FPIs in ETCDs"],
  why="None of the other measures was approved.",
  current=ca(SEP24),
  facts=[fact("215th meeting of the SEBI Board: review of SEBI (Settlement Proceedings) Regulations, 2018; Common "
              "Advertisement Code for Specified SEBI Regulated Entities; FPI Participation in Exchange Traded "
              "Commodity Derivatives; Settlement Regulations, 2026 shall come into force the day succeeding the 30th "
              "day from the date of notification", SEBI_SEP26)])
Q(T, "SEBI", "Advanced",
  "At its meeting of 19 June 2026, the SEBI Board revisited share buybacks. Consider:\n"
  "I. Open-market buybacks through stock exchanges were reinstated, with effect from 1 August 2026.\n"
  "II. Promoters remain barred from participating in such buybacks.\n"
  "III. All forms of buyback, including tender offers, were abolished.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Buyback regulation",
  explanation="The Board amended the Buy-back Regulations, 2018 to reinstate open-market buybacks via exchanges from "
              "1 August 2026, with promoters still not allowed to participate. Buybacks were not abolished (III "
              "wrong).",
  steps=["I: correct", "II: correct", "III: wrong"],
  why="III is wrong; 'I only' omits II.",
  current=ca("2026-06-19"),
  facts=[fact("SEBI board reinstated open-market buybacks through stock exchanges, effective August 1, 2026, with "
              "promoters barred from participating", SEBI_JUN26)])
Q(T, "SEBI", "Advanced",
  "SEBI's investor advisory (August 2024) on companies listed on the SME segment described a pattern used by some "
  "promoters. Which sequence matches it?",
  ["Exaggerated public claims about operations, followed by bonus issues, stock splits or preferential allotments, "
   "while promoters offload shares at inflated prices", "Delisting the company to avoid disclosures",
   "Listing only through the book-building route on the main board", "Issuing only debt instruments to retail "
   "investors"],
  concept="Market manipulation in SME stocks",
  explanation="SEBI observed that some SME companies and promoters make exaggerated claims, follow them with "
              "corporate actions like bonus issues, stock splits or preferential allotments that create optimism, "
              "and then offload holdings at inflated prices. It advised investors to verify information and avoid "
              "tips.",
  steps=["Hype → corporate actions → promoter selling at high prices"],
  why="Delisting, main-board book building and debt issues are not the described modus operandi.",
  facts=[fact("Some companies and their promoters make exaggerated claims about their operations, followed by corporate "
              "actions like bonus issues, stock splits, or preferential allotments; promoters may exploit this to "
              "offload their holdings at higher prices", SEBI_SME)])

# ================================================================= 28. Insurance (2 / 3 / 2)
T = "Insurance"
Q(T, "IRDAI", "Basic",
  "Under the Insurance Ombudsman Rules, 2017, what is the maximum compensation (including expenses) for which an "
  "Insurance Ombudsman can entertain a complaint?",
  ["₹50 lakh", "₹30 lakh", "₹20 lakh", "₹1 crore"],
  concept="Insurance Ombudsman",
  explanation="The Council for Insurance Ombudsmen states that the Ombudsman can entertain complaints where the "
              "compensation does not exceed ₹50 lakh, including relevant expenses.",
  steps=["Ceiling: ₹50 lakh"],
  why="₹30 lakh is the RBI Ombudsman's consequential-loss cap; ₹20 lakh and ₹1 crore are wrong.",
  facts=[fact("The Insurance Ombudsman can entertain complaints where the compensation awarded does not exceed rupees "
              "50 Lakhs (including relevant expenses, if any)", CIO_FAQ)])
Q(T, "Life and general insurance", "Basic",
  "The 'Committee on Reform of the Insurance Sector' constituted in 1994 was chaired by:",
  ["R. N. Malhotra", "M. Narasimham", "S. S. Tarapore", "C. Rangarajan"],
  concept="Insurance sector reforms",
  explanation="RBI's chronology records the 1994 Committee on Reform of the Insurance Sector under R. N. Malhotra, "
              "whose recommendations led to opening of the sector and to IRDA.",
  steps=["1994 → Malhotra Committee"],
  why="Narasimham chaired banking reform committees; Tarapore capital account convertibility; Rangarajan other "
      "panels.",
  facts=[fact("1994: 'Committee on Reform of the Insurance Sector', RN Malhotra", CHRON_91)])
Q(T, "IRDAI", "Intermediate",
  "Within what time must a policyholder approach the Insurance Ombudsman under the 2017 Rules?",
  ["Within one year of the insurer's rejection or reply, or of the expiry of one month without a reply",
   "Within 30 days of the claim event", "Within 90 days of the insurer's reply", "Within three years of buying "
   "the policy"],
  concept="Filing with the Insurance Ombudsman",
  explanation="A complaint must first be made to the insurer. A representation can be made to the Ombudsman within "
              "one year from the insurer's rejection/reply, or after one month with no reply.",
  steps=["Approach insurer first", "Ombudsman: within one year"],
  why="30 days, 90 days (RBI Ombudsman's window) and three years are not the rule.",
  facts=[fact("A representation should stand made to the Insurance Ombudsman within one year from the date of the "
              "insurer's rejection/reply, or after the expiry of one month if no reply", CIO_FAQ)])
Q(T, "Life and general insurance", "Intermediate",
  "Under IRDAI's master circular on health insurance (May 2024), within what time must insurers decide on a cashless "
  "authorisation request and on final authorisation after a discharge request?",
  ["Within one hour, and within three hours of the discharge request", "Within 24 hours, and within 48 hours",
   "Within three hours, and within seven days", "Within 30 minutes, and within one hour"],
  concept="Health insurance claim timelines",
  explanation="The May 2024 master circular requires insurers to decide on cashless authorisation within one hour of "
              "request and to give final authorisation within three hours of the discharge request.",
  steps=["Cashless authorisation: 1 hour", "Discharge authorisation: 3 hours"],
  why="The other timelines are not those prescribed.",
  facts=[fact("Insurers to decide on cashless authorisation within one hour of request and final authorisation within "
              "three hours of receipt of discharge request from the hospital (IRDAI master circular, May 29, 2024)",
              IRDAI_HEALTH)])
Q(T, "IRDAI", "Intermediate",
  "Besides personal lines and group policies, the Insurance Ombudsman Rules, 2017 also cover policies issued to which "
  "kind of businesses?",
  ["Sole proprietorships and micro enterprises", "Large listed companies", "Public sector undertakings only",
   "Reinsurance companies"],
  concept="Scope of the Insurance Ombudsman",
  explanation="The Rules cover complaints on personal lines of insurance, group policies, and policies issued to sole "
              "proprietorships and micro enterprises.",
  steps=["Coverage includes sole proprietorship and micro-enterprise policies"],
  why="Large companies, PSUs and reinsurers are outside this consumer forum.",
  facts=[fact("These Rules aim at resolving complaints relating to disputes with insurance companies on personal lines "
              "of insurance, group insurance policies, policies issued to sole proprietorship and micro enterprises",
              CIO_FAQ)])
Q(T, "IRDAI", "Advanced",
  "Consider the following statements about the Insurance Ombudsman:\n"
  "I. The institution of Insurance Ombudsman has been functioning since 1999.\n"
  "II. Where a complaint is settled through mediation, the Ombudsman makes a recommendation within one month of "
  "receiving the parties' written consent.\n"
  "III. A complainant may engage a lawyer to argue the case before the Ombudsman.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Insurance Ombudsman procedure",
  explanation="The Insurance Ombudsman has functioned since 1999 (I), and in mediation the Ombudsman makes a "
              "recommendation within one month of the written consent (II). The 2017 Rules have no provision for "
              "engaging a lawyer (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong"],
  why="III is wrong; 'I only' omits II.",
  facts=[fact("The Institution of Insurance Ombudsman has been established and is functioning since 1999; the "
              "Ombudsman shall make a recommendation within one month of the date of receipt of mutual written consent "
              "for mediation; as per the Insurance Ombudsman Rules 2017, there is no provision to engage a lawyer",
              CIO_FAQ)])
Q(T, "Life and general insurance", "Advanced",
  "Consider the following statements about IRDAI's master circular on health insurance of May 2024:\n"
  "I. The moratorium period, after which a claim cannot be contested for non-disclosure, was cut from eight years to "
  "five years.\n"
  "II. After the moratorium, a policy and claim can be contested only for established fraud.\n"
  "III. Insurers may take up to 24 hours to decide a cashless authorisation request.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Policyholder protection in health insurance",
  explanation="The moratorium was reduced from eight to five years (I), and afterwards claims are contestable only on "
              "established fraud (II). Cashless authorisation must be decided within one hour, not 24 hours (III "
              "wrong).",
  steps=["I: correct", "II: correct", "III: wrong (one hour)"],
  why="III is wrong; 'I only' omits II.",
  facts=[fact("The moratorium period is reduced from eight years to five; no policy and claim shall be contestable on "
              "grounds of non-disclosure except for established fraud after the moratorium; cashless authorisation "
              "within one hour", IRDAI_HEALTH)])


# ================================================================= 29. Mutual Funds (1 / 2 / 0)
T = "Mutual Funds"
Q(T, "NAV and SIP", "Basic",
  "What is a Consolidated Account Statement (CAS) in the securities market?",
  ["A single monthly statement of an investor's transactions across all mutual funds and holdings in demat accounts",
   "A bank statement covering all savings accounts", "A tax statement issued by the Income Tax Department",
   "A statement of a company's consolidated accounts"],
  concept="CAS",
  explanation="SEBI describes the CAS as a combined statement showing an investor's transactions in a month across all "
              "mutual funds and other securities held in demat accounts; investors must update their PAN with the "
              "DP/broker.",
  steps=["CAS = MF transactions + demat holdings in one statement"],
  why="It is not a bank, tax or company-accounts statement.",
  facts=[fact("Consolidated Account Statement (CAS) is a single/combined account statement which shows the details of "
              "transactions made by an investor during a month across all Mutual Funds and also other securities held "
              "in their demat account(s)", SEBI_CAS)])
Q(T, "Types", "Intermediate",
  "According to RBI's G-sec primer, which of the following may re-repo government securities acquired under reverse "
  "repo, subject to RBI's conditions and approval of their regulators?",
  ["Mutual funds and insurance companies maintaining SGL accounts with RBI, along with SCBs and primary dealers",
   "Only scheduled commercial banks", "Only RBI", "Retail investors through Retail Direct accounts"],
  concept="Mutual funds in the G-sec repo market",
  explanation="Scheduled commercial banks and primary dealers, along with mutual funds and insurance companies "
              "(subject to the approval of their regulators) that maintain SGL accounts with RBI, are permitted to "
              "re-repo government securities, including SDLs and T-bills, acquired under reverse repo.",
  steps=["Eligible: SCBs, PDs, MFs, insurers (with SGL accounts)"],
  why="Re-repo is not limited to banks or RBI, and retail investors are not eligible.",
  facts=[fact("Scheduled commercial banks, Primary Dealers along with Mutual Funds and Insurance Companies (subject to "
              "the approval of the regulators concerned) maintaining Subsidiary General Ledger account with RBI are "
              "permitted to re-repo the government securities, including SDLs and Treasury Bills, acquired under "
              "reverse repo", GSEC_FAQ)])
Q(T, "Types", "Intermediate",
  "To help mutual funds manage short-term liquidity gaps during a trading day, what did SEBI's Board allow on 19 June "
  "2026?",
  ["Intraday borrowing by mutual funds", "Investment of 100% of scheme assets in unlisted equity",
   "Guaranteed returns on debt schemes", "Suspension of redemptions for a week"],
  concept="Liquidity management by mutual funds",
  explanation="The Board permitted mutual funds to use intraday borrowings to bridge temporary liquidity gaps during "
              "the trading day.",
  steps=["June 2026 → MF intraday borrowing allowed"],
  why="The other measures were not approved and would be inconsistent with investor protection.",
  current=ca("2026-06-19"),
  facts=[fact("SEBI board allowed mutual funds to use intraday borrowing to cover short-term liquidity gaps",
              SEBI_JUN26)])


# ================================================================= 31. Government Financial Schemes (3 / 1 / 1)
T = "Government Financial Schemes"
Q(T, "Credit guarantee schemes", "Basic",
  "The Credit Guarantee Fund Trust for Micro and Small Enterprises (CGTMSE) was set up in July 2000 by:",
  ["SIDBI and the Ministry of MSME, Government of India", "RBI and NABARD", "NCGTC and IBA",
   "SBI and the Ministry of Finance"],
  concept="CGTMSE",
  explanation="SIDBI's ecosystem page says CGTMSE was set up by SIDBI and the Ministry of MSME in July 2000 and "
              "operates the credit guarantee scheme for micro and small enterprises.",
  steps=["July 2000 → CGTMSE (SIDBI + MoMSME)"],
  why="RBI/NABARD, NCGTC/IBA and SBI/MoF were not the founders.",
  facts=[fact("Credit Guarantee Fund Trust for Micro and Small Enterprises (CGTMSE) set up by SIDBI and Ministry of "
              "MSME, Government of India in July 2000", SIDBI_ECO)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Basic",
  "A person enrolls in PMJJBY for the first time. During the first 30 days (the lien period), which death is "
  "covered?",
  ["Only death due to accident", "Death due to any cause", "No death of any kind", "Only death due to illness"],
  concept="PMJJBY lien period",
  explanation="For first-time subscribers, risk starts from auto-debit of premium, but death other than due to "
              "accident in the first 30 days is not covered.",
  steps=["First 30 days → only accidental death covered"],
  why="Any-cause cover starts after the lien; illness deaths are excluded in this period.",
  facts=[fact("Insurance cover shall not be available for death (other than due to accident) occurring during the "
              "first 30 days from the date of enrolment into the scheme (lien period)", PMJJBY)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Basic",
  "Under PMJJBY, who are the master policy holders for the scheme?",
  ["Participating banks and Post Office", "Each individual subscriber", "LIC alone", "The Department of Financial "
   "Services"],
  concept="PMJJBY administration",
  explanation="PMJJBY is offered through LIC and other life insurers in collaboration with participating banks and Post "
              "Office, which are the master policy holders.",
  steps=["Master policy holders = banks / Post Office"],
  why="Individuals are subscribers; LIC is an insurer; DFS administers policy.",
  facts=[fact("Participating Banks/ Post office are the Master policy holders for the scheme", PMJJBY)])
Q(T, "Credit guarantee schemes", "Intermediate",
  "The Emergency Credit Line Guarantee Scheme (ECLGS), launched in May 2020 under the Aatmanirbhar package, provided:",
  ["100% guarantee cover by NCGTC on emergency credit to eligible businesses, later enhanced to ₹5 lakh crore and "
   "valid till 31 March 2023", "Interest-free loans directly from RBI", "50% guarantee by CGTMSE for housing loans",
   "Subsidy on credit card dues of MSMEs"],
  concept="ECLGS",
  explanation="ECLGS gave 100% guarantee coverage through NCGTC to lenders on guaranteed emergency credit lines; its "
              "size, initially ₹3 lakh crore, was enhanced to ₹5 lakh crore and the scheme ran till 31 March 2023.",
  steps=["May 2020 launch", "100% NCGTC guarantee", "Up to ₹5 lakh crore; till 31 Mar 2023"],
  why="It was a guarantee scheme, not RBI lending, housing cover or card subsidy.",
  facts=[fact("Emergency Credit Line Guarantee Scheme enhanced to Rs 5 lakh crore, extended up to March 2023; 100% "
              "guarantee coverage by NCGTC", ECLGS)])

prem = {"Jun": 436, "Sep": 342, "Dec": 228, "Mar": 114}
first, renew = prem["Sep"], prem["Jun"]
assert first + renew == 778 and prem["Jun"] - prem["Sep"] == 94
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Advanced",
  "Ravi, 35, joins PMJJBY for the first time in October 2026 and renews in June 2027. Using the pro-rata premiums "
  "on the Department of Financial Services' PMJJBY page, what does he pay in total for the two debits?",
  ["₹778 (₹342 on joining + ₹436 on renewal)", "₹872 (₹436 + ₹436)", "₹664 (₹228 + ₹436)",
   "₹550 (₹114 + ₹436)"],
  concept="PMJJBY pro-rata premium",
  explanation="For first enrolment mid-year: June–August ₹436; September–November ₹342; December–February ₹228; "
              "March–May ₹114. Joining in October → ₹342. Renewal is always at the full ₹436. Total ₹778.",
  steps=["October → Sep–Nov slab → ₹342", "Renewal June → ₹436", "Total ₹778"],
  why="₹872 ignores pro-rating; ₹664 and ₹550 use the wrong slab for October.",
  computed=True,
  facts=[fact("Pro-rata premium for first enrolment: June, July, August – ₹436; September, October, November – ₹342; "
              "December, January, February – ₹228; March, April, May – ₹114; full year's premium of ₹436 is payable "
              "at the time of renewal", PMJJBY)])

# ================================================================= 30. Budget and Economic Survey (2 / 5 / 3)
T = "Budget and Economic Survey"
BD = ca(BUDGET_DAY)
Q(T, "Fiscal terms", "Basic",
  "As noted in the Union Budget 2026-27, the Sixteenth Finance Commission recommended what share of the divisible "
  "pool of central taxes for the States?",
  ["41% (retained)", "42%", "32%", "50%"],
  concept="Tax devolution",
  explanation="2026-27 is the first year of the Sixteenth Finance Commission's award period; it recommended retaining "
              "the States' share at 41% of the divisible pool, which the Government accepted.",
  steps=["16th FC → 41% retained"],
  why="42% was the 14th FC's share; 32% the 13th FC's; 50% was not recommended.",
  current=BD,
  facts=[fact("SFC has recommended for retaining the share of devolution to the States at 41 per cent of divisible "
              "pool; this recommendation is accepted by the Government", BUDGET)])
Q(T, "Union Budget highlights", "Basic",
  "Besides a new ₹10,000 crore SME Growth Fund, the Union Budget 2026-27 proposed to top up which existing fund with "
  "₹2,000 crore to support micro enterprises' access to risk capital?",
  ["Self-Reliant India Fund (set up in 2021)", "National Investment Fund", "Infrastructure Risk Guarantee Fund",
   "Rural Infrastructure Development Fund"],
  concept="Equity support for MSMEs",
  explanation="Under equity support for MSMEs, the Finance Minister proposed topping up the Self-Reliant India Fund, "
              "set up in 2021, with ₹2,000 crore.",
  steps=["Self-Reliant India Fund (2021) + ₹2,000 crore"],
  why="The other funds were not the ones topped up for micro enterprises' risk capital.",
  current=BD,
  facts=[fact("She also proposed to top up the Self-Reliant India Fund set up in 2021, with ₹2,000 crore to continue "
              "support to micro enterprises and maintain their access to risk capital", BUDGET)])
Q(T, "Fiscal terms", "Intermediate",
  "What tax devolution to the States did the Union Budget estimate for BE 2026-27?",
  ["₹15.26 lakh crore, about 3.9% of GDP", "₹13.93 lakh crore, about 3.5% of GDP", "₹1.4 lakh crore, 0.4% of GDP",
   "₹28.67 lakh crore, 7.3% of GDP"],
  concept="Transfers to States",
  explanation="Tax devolution in BE 2026-27 is ₹15.26 lakh crore (3.9% of GDP), against ₹13.93 lakh crore in RE "
              "2025-26. Finance Commission grants are ₹1.4 lakh crore; ₹28.67 lakh crore is the Centre's net tax "
              "revenue.",
  steps=["BE 2026-27 devolution = ₹15.26 lakh crore (3.9% of GDP)"],
  why="₹13.93 lakh crore is RE 2025-26; ₹1.4 lakh crore is FC grants; ₹28.67 lakh crore is net tax to the Centre.",
  current=BD,
  facts=[fact("In BE 2026-27, tax devolution to the States is estimated at ₹15.26 lakh crore compared to ₹13.93 lakh "
              "crore in RE 2025-26; tax devolution in BE 2026-27 is 3.9 per cent of GDP", BUDGET)])
Q(T, "Union Budget highlights", "Intermediate",
  "The Union Budget 2026-27 said TReDS had made more than ₹7 lakh crore available to MSMEs. Which of the following "
  "was among the measures it proposed to leverage TReDS further?",
  ["Mandating TReDS as the settlement platform for all purchases from MSMEs by CPSEs",
   "Closing TReDS platforms run by private entities", "Allowing only banks to buy MSME invoices",
   "Capping TReDS financing at ₹10 lakh per invoice"],
  concept="Liquidity support for MSMEs",
  explanation="The four TReDS measures were: mandate TReDS for all CPSE purchases from MSMEs; CGTMSE-backed credit "
              "guarantee for invoice discounting; link GeM with TReDS; and introduce TReDS receivables as asset-backed "
              "securities.",
  steps=["CPSE purchases from MSMEs → settled on TReDS"],
  why="No closure, bank-only rule or per-invoice cap was proposed.",
  current=BD,
  facts=[fact("With TReDS, more than ₹7 lakh crore has been made available to MSMEs; proposed to mandate TReDS as the "
              "transaction settlement platform for all purchases from MSMEs by CPSEs", BUDGET)])
Q(T, "Economic Survey highlights", "Intermediate",
  "According to the Macro-economic Framework Statement presented with the Union Budget 2026-27, private final "
  "consumption expenditure in FY26 was projected to account for what share of GDP?",
  ["61.5%, the highest since FY12", "55.6%, the lowest since FY12", "30%, stable for three years",
   "13.6%, up from FY25"],
  concept="Composition of demand",
  explanation="PFCE was projected to grow 7% and account for 61.5% of GDP, the highest since FY12. GFCF has been "
              "about 30% of GDP for three years; 55.6% is the debt-to-GDP ratio and 13.6% total expenditure/GDP.",
  steps=["PFCE share = 61.5% (highest since FY12)"],
  why="55.6%, 30% and 13.6% are other indicators.",
  current=BD,
  facts=[fact("Private final consumption expenditure (PFCE) is projected to grow by 7 per cent, accounting for 61.5 per "
              "cent of GDP - the highest level since FY12", BUDGET)])
Q(T, "Economic Survey highlights", "Intermediate",
  "According to the Budget's Macro-economic Framework Statement, India's current account deficit in H1 FY26 "
  "(April–September 2025) was:",
  ["0.8% of GDP, down from 1.3% in H1 FY25", "1.3% of GDP, up from 0.8%", "0.5% of GDP", "2.0% of GDP"],
  concept="External sector",
  explanation="The CAD declined to 0.8% of GDP in H1 FY26 from 1.3% in H1 FY25, despite US tariffs.",
  steps=["H1 FY26 CAD = 0.8% of GDP (H1 FY25: 1.3%)"],
  why="The second option reverses the figures; 0.5% was Q1 2026-27; 2.0% is wrong.",
  current=BD,
  facts=[fact("The current account deficit declined to 0.8 per cent of GDP in H1 FY26 from 1.3 per cent in H1 FY25",
              BUDGET)])
Q(T, "Fiscal terms", "Intermediate",
  "By how much did the Union Budget 2026-27 project nominal GDP to grow over the first advance estimates of FY "
  "2025-26?",
  ["10.0%", "7.4%", "8.0%", "11.2%"],
  concept="Nominal GDP assumption",
  explanation="The Budget projected nominal GDP growth of 10.0% over the first advance estimates for FY26, in which "
              "real growth was 7.4% and nominal growth 8%.",
  steps=["Budget assumption: nominal GDP +10.0%"],
  why="7.4% is FY26 real growth; 8% FY26 nominal growth; 11.2% gross tax/GDP.",
  current=BD,
  facts=[fact("In the Budget for FY 2026-27, nominal GDP is projected to grow by 10.0 per cent over the First Advance "
              "Estimates of FY 2025-26; real GDP estimated to grow by 7.4 per cent in FY 2025-26, with nominal GDP "
              "growth at 8 per cent", BUDGET)])

net_tax, ntr, rev = 28.67, 6.66, 35.33
assert round(net_tax + ntr, 2) == rev and round(pct(ntr, rev), 1) == 18.9
Q(T, "Fiscal terms", "Advanced",
  "In BE 2026-27, the Centre's tax revenue (net to Centre) is ₹28.67 lakh crore and non-tax revenue ₹6.66 lakh crore. "
  "What are revenue receipts, and roughly what share of them is non-tax revenue?",
  ["₹35.33 lakh crore; about 18.9%", "₹35.33 lakh crore; about 23.2%", "₹22.01 lakh crore; about 30%",
   "₹44.04 lakh crore; about 15%"],
  concept="Composition of revenue receipts",
  explanation="Revenue receipts = net tax revenue + non-tax revenue = 28.67 + 6.66 = ₹35.33 lakh crore. NTR share = "
              "6.66 ÷ 35.33 ≈ 18.9%. (6.66 ÷ 28.67 ≈ 23.2% is NTR relative to net tax, not to receipts.)",
  steps=["28.67 + 6.66 = 35.33", "6.66 ÷ 35.33 ≈ 18.9%"],
  why="23.2% divides by net tax; ₹22.01 lakh crore subtracts; ₹44.04 lakh crore is gross tax revenue.",
  computed=True, current=BD,
  facts=[fact("The Tax Revenues (Net to Centre) are projected to be ₹28.67 lakh crore; NTR of the Central Government is "
              "projected at ₹6.66 lakh crore; Revenue Receipts estimated at ₹35.33 lakh crore", BUDGET)])

gtr, direct, indirect, growth = 44.04, 26.97, 17.07, 8.0
assert round(direct + indirect, 2) == gtr and round(pct(direct, gtr), 1) == 61.2
assert round(gtr / (1 + growth / 100), 1) == 40.8
Q(T, "Fiscal terms", "Advanced",
  "In BE 2026-27, gross tax revenue (GTR) is ₹44.04 lakh crore, a growth of 8.0% over RE 2025-26, with direct taxes "
  "at ₹26.97 lakh crore and indirect taxes at ₹17.07 lakh crore. Which statement is correct?",
  ["Direct taxes are about 61.2% of GTR, and RE 2025-26 GTR works out to about ₹40.8 lakh crore",
   "Indirect taxes are about 61.2% of GTR, and RE 2025-26 GTR was about ₹47.6 lakh crore",
   "Direct taxes are about 38.8% of GTR, and RE 2025-26 GTR was about ₹40.8 lakh crore",
   "Direct taxes are about 61.2% of GTR, and RE 2025-26 GTR was about ₹47.6 lakh crore"],
  concept="Tax structure",
  explanation="26.97 + 17.07 = 44.04; direct share = 26.97 ÷ 44.04 ≈ 61.2%. RE 2025-26 GTR = 44.04 ÷ 1.08 ≈ ₹40.8 "
              "lakh crore (₹47.6 lakh crore would wrongly add 8%).",
  steps=["26.97 ÷ 44.04 ≈ 61.2%", "44.04 ÷ 1.08 ≈ 40.8"],
  why="Indirect taxes are 38.8%; 47.6 multiplies instead of dividing by 1.08.",
  computed=True, current=BD,
  facts=[fact("In BE 2026-27, Gross Tax Revenue (GTR) is estimated at ₹44.04 lakh crore. It represents a growth of 8.0 "
              "per cent over RE 2025-26. Direct Taxes at ₹26.97 lakh crore are the major contributor to GTR (61.2 per "
              "cent of the GTR). Indirect taxes are estimated at ₹17.07 lakh crore", BUDGET)])

fmv = 80  # ₹ lakh
due = fmv * 0.30 + fmv * 0.30
assert due == 48 and fmv <= 100
Q(T, "Union Budget highlights", "Advanced",
  "Under the one-time six-month foreign asset disclosure scheme proposed in the Union Budget 2026-27, a young "
  "professional (category A) declares an undisclosed overseas asset with a fair market value of ₹80 lakh. Another "
  "taxpayer (category B) had paid tax on overseas income but failed to declare a ₹3 crore asset. What do they pay?",
  ["A: ₹48 lakh (30% tax + 30% additional tax); B: a fee of ₹1 lakh", "A: ₹24 lakh; B: ₹90 lakh",
   "A: ₹48 lakh; B: ₹1.8 crore", "A: ₹80 lakh; B: nil"],
  concept="Foreign asset disclosure scheme",
  explanation="Category A (undisclosed income/asset up to ₹1 crore) pays 30% of FMV as tax and 30% as additional "
              "income tax in lieu of penalty: 0.6 × 80 = ₹48 lakh, with immunity from prosecution. Category B (asset "
              "up to ₹5 crore, income already taxed) pays a fee of ₹1 lakh for immunity from penalty and prosecution.",
  steps=["A: 30% + 30% of 80 = 48", "B: ≤ ₹5 crore → fee ₹1 lakh"],
  why="₹24 lakh omits the additional 30%; B does not pay a percentage of the asset; A is not the full FMV.",
  computed=True, current=BD,
  facts=[fact("For category (A), the limit of undisclosed income/asset is up to 1 crore rupees; they need to pay 30 "
              "percent of Fair Market Value as tax and 30 percent as additional income tax in lieu of penalty; for "
              "category (B), asset value up to 5 crore rupees; immunity with payment of fee of 1 lakh rupees",
              BUDGET)])


# ================================================================= 32. RBI Circulars and Regulatory Updates (3 / 4 / 4)
T = "RBI Circulars and Regulatory Updates"
SUB = "Recent RBI directions"
Q(T, SUB, "Basic",
  "Which bank was included in the Second Schedule to the RBI Act, 1934 by a notification dated 12 January 2026?",
  ["The Assam Co-operative Apex Bank Ltd", "The Kerala State Co-operative Bank", "India Post Payments Bank",
   "NABARD"],
  concept="Scheduled status",
  explanation="RBI announced on 6 February 2026 that the Assam Co-operative Apex Bank Ltd had been included in the "
              "Second Schedule by notification dated 12 January 2026, published in the Gazette on 29 January 2026.",
  steps=["Notification 12 Jan 2026 → Assam Co-operative Apex Bank scheduled"],
  why="The others were not the subject of this notification (NABARD is not a bank under the Schedule).",
  current=ca("2026-01-12"),
  facts=[fact("The Assam Co-operative Apex Bank Ltd has been included in the Second Schedule to the RBI Act, 1934 vide "
              "Notification dated January 12, 2026 and published in the Gazette of India dated January 29, 2026",
              ASSAM)])
Q(T, SUB, "Basic",
  "Which of the following NBFCs is in RBI's list of Upper Layer NBFCs (NBFC-UL) for 2026-27, released on 6 August "
  "2026?",
  ["HDB Financial Services Limited", "Manappuram Finance Limited", "IIFL Finance Limited",
   "Poonawalla Fincorp Limited"],
  concept="Scale-based regulation",
  explanation="The 2026-27 list of 17 NBFC-ULs includes REC, PFC, IRFC, Bajaj Finance, Shriram Finance, LIC Housing "
              "Finance, Cholamandalam, Tata Capital, Tata Sons, Muthoot Finance, Aditya Birla Capital, HUDCO, M&M "
              "Financial Services, L&T Finance, Bajaj Housing Finance, HDB Financial Services and Piramal Finance.",
  steps=["HDB Financial Services is No. 16 on the list"],
  why="The other three are not in the 2026-27 list.",
  current=ca("2026-08-06"),
  facts=[fact("2026-27 list of NBFC-UL: REC, PFC, IRFC, Bajaj Finance, Shriram Finance, LIC Housing Finance, "
              "Cholamandalam, Tata Capital, Tata Sons, Muthoot Finance, Aditya Birla Capital, HUDCO, Mahindra & "
              "Mahindra Financial Services, L&T Finance, Bajaj Housing Finance, HDB Financial Services, Piramal "
              "Finance", NBFC_UL)])
Q(T, SUB, "Basic",
  "In February 2026, RBI proposed to allow commercial banks, subject to prudential safeguards, to lend to which "
  "entities that they had not been permitted to finance?",
  ["Real Estate Investment Trusts (REITs)", "Infrastructure Investment Trusts (InvITs)", "Chit funds",
   "Nidhi companies"],
  concept="Bank lending to REITs",
  explanation="Banks were not permitted to lend to REITs and InvITs at the outset; lending to InvITs was later "
              "allowed. In February 2026 RBI proposed to permit lending to listed REITs with safeguards and to "
              "harmonise InvIT norms.",
  steps=["InvITs already allowed", "REITs → proposed to be permitted"],
  why="InvIT lending was already permitted; chit funds and Nidhis were not the subject.",
  current=ca(FEB26),
  facts=[fact("While bank lending to InvITs was allowed subsequently, lending to REITs was not permitted hitherto; it "
              "is proposed to permit commercial banks to extend finance to REITs, subject to appropriate prudential "
              "safeguards", SDRP_FEB26)])
Q(T, SUB, "Intermediate",
  "RBI proposed in February 2026 to exempt certain 'Type I' NBFCs from the requirement of registration. Which?",
  ["Those not availing public funds and without customer interface, with asset size up to ₹1,000 crore",
   "All deposit-taking NBFCs", "NBFCs with more than 1,000 branches", "Upper Layer NBFCs"],
  concept="Ease of doing business for NBFCs",
  explanation="Considering their low systemic risk, Type-I NBFCs—with no public funds and no customer interface—and "
              "asset size not exceeding ₹1,000 crore were proposed to be exempted from registration with RBI, "
              "subject to conditions.",
  steps=["No public funds + no customer interface + assets ≤ ₹1,000 crore"],
  why="Deposit-takers, large-branch NBFCs and UL NBFCs are higher-risk categories.",
  current=ca(FEB26),
  facts=[fact("Type-I NBFCs with asset size not exceeding ₹1,000 crore, may be exempted from registration requirement "
              "with the Reserve Bank subject to certain specified conditions", SDRP_FEB26)])
Q(T, SUB, "Intermediate",
  "By a circular of 12 October 2026, RBI changed the rules for non-deliverable derivative contracts (NDDCs) involving "
  "INR offered by Authorised Dealers to non-residents. What is the new rule?",
  ["They may be offered to a non-resident user only for the purpose of hedging",
   "They are banned entirely", "They may be offered without any restriction on purpose",
   "They may be offered only to residents"],
  concept="INR NDF market",
  explanation="Earlier, AD Category-I banks with an IFSC Banking Unit and SPDs could offer INR NDDCs to non-residents "
              "without restriction on purpose. Henceforth, they may offer them only for hedging.",
  steps=["Before: no purpose restriction", "After: only for hedging"],
  why="NDDCs were not banned or opened to residents; the purpose restriction was introduced, not removed.",
  current=ca("2026-10-12"),
  facts=[fact("Henceforth, Authorised Dealers shall offer NDDCs involving INR to a non-resident user only for the "
              "purpose of hedging", NDDC)])
Q(T, SUB, "Intermediate",
  "In February 2026, what did RBI propose for NBFC-Investment and Credit Companies lending against gold that have "
  "more than 1,000 branches?",
  ["To dispense with the requirement of prior RBI approval for opening new branches",
   "To require them to convert into banks", "To cap their branches at 1,000", "To bar them from gold loans"],
  concept="NBFC branch authorisation",
  explanation="NBFC-ICCs lending against gold with over 1,000 branches needed prior RBI approval to open branches. "
              "Given their prudential framework, RBI proposed to dispense with this requirement.",
  steps=["Earlier: prior approval beyond 1,000 branches", "Proposal: dispense with it"],
  why="No conversion, branch cap or ban was proposed.",
  current=ca(FEB26),
  facts=[fact("NBFC - ICCs engaged in the business of lending against gold collateral with over 1,000 branches are "
              "required to obtain prior RBI approval for opening new branches; it is proposed to dispense with the "
              "requirement of prior approval", SDRP_FEB26)])
Q(T, SUB, "Intermediate",
  "PNB Housing Finance and Sammaan Capital did not meet the NBFC-UL criteria in 2026-27 but stay in the Upper Layer. "
  "Why?",
  ["Once classified as NBFC-UL, an NBFC remains subject to enhanced regulation for at least five years",
   "They voluntarily opted in", "They are government-owned", "They hold deposits above ₹10,000 crore"],
  concept="Stickiness of NBFC-UL classification",
  explanation="Under the scale-based framework, an NBFC classified as UL stays under enhanced regulation for at least "
              "five years even if it does not meet the criteria later; both were in the 2024-25 list.",
  steps=["Five-year minimum in UL", "Last identified 2024-25 → continue"],
  why="It is not voluntary, ownership-based or deposit-based.",
  current=ca("2026-08-06"),
  facts=[fact("Once an NBFC is classified as NBFC-UL, it shall be subject to enhanced regulatory requirement, at least "
              "for a period of five years; PNB Housing Finance Limited and Sammaan Capital Limited would continue in "
              "NBFC-UL", NBFC_UL)])

ul = {"IFC": ["REC", "PFC", "IRFC", "HUDCO"],
      "D-ICC": ["Bajaj Finance", "Shriram", "M&M Financial"], "D-HFC": ["LIC HF"],
      "ND-ICC": ["Chola", "Tata Capital", "Muthoot", "ABCL", "L&T Finance", "HDB", "Piramal"],
      "ND-HFC": ["Bajaj Housing"], "CIC": ["Tata Sons"]}
assert sum(map(len, ul.values())) == 17 and len(ul["IFC"]) == 4
assert len(ul["D-ICC"]) + len(ul["D-HFC"]) == 4 and 17 + 2 == 19
Q(T, SUB, "Advanced",
  "RBI's NBFC-UL list for 2026-27 has 17 NBFCs, and two more continue from earlier lists. Using the list, which "
  "statement is correct?",
  ["4 are Infrastructure Finance Companies, 4 are deposit-taking (3 NBFC-ICCs and 1 HFC), and 19 NBFCs in all face "
   "Upper Layer regulation", "6 are IFCs and 17 in all face Upper Layer regulation",
   "There are no deposit-taking NBFCs in the list", "Only 2 are Infrastructure Finance Companies"],
  concept="Composition of the Upper Layer",
  explanation="IFCs: REC, PFC, IRFC, HUDCO (4). Deposit-taking: Bajaj Finance, Shriram Finance, M&M Financial "
              "Services (ICCs) and LIC Housing Finance (HFC) = 4. With PNB Housing Finance and Sammaan Capital "
              "continuing, 19 NBFCs are under UL requirements.",
  steps=["IFCs = 4", "Deposit-taking = 3 + 1 = 4", "17 + 2 = 19"],
  why="The other options miscount the IFCs, deposit-takers or total.",
  computed=True, current=ca("2026-08-06"),
  facts=[fact("2026-27 NBFC-UL list with categories: REC, PFC, IRFC, HUDCO – Infrastructure Finance Company; Bajaj "
              "Finance, Shriram Finance, Mahindra & Mahindra Financial Services – Deposit taking NBFC-ICC; LIC Housing "
              "Finance – Deposit taking HFC; PNB Housing Finance and Sammaan Capital continue in NBFC-UL", NBFC_UL)])
Q(T, SUB, "Advanced",
  "Consider the following measures for urban co-operative banks announced by RBI in February 2026:\n"
  "I. Raising the financial limits on unsecured loans and on loans to nominal members.\n"
  "II. Removing tenor and moratorium requirements on housing loans given by Tier III and Tier IV UCBs.\n"
  "III. Launching Mission SAKSHAM to train over 1.4 lakh participants from UCBs.\n"
  "Which is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I and III only"],
  concept="Strengthening UCBs",
  explanation="The Governor announced four UCB measures: higher limits on unsecured loans and on loans to nominal "
              "members (I), removal of tenor and moratorium requirements on housing loans by Tier III and IV UCBs "
              "(II), and Mission SAKSHAM to train over 1.4 lakh participants (III).",
  steps=["I ✓", "II ✓", "III ✓"],
  why="All three are correct; the partial options omit one.",
  current=ca(FEB26),
  facts=[fact("The first two pertain to raising the financial limits on unsecured loans and loans to nominal members by "
              "UCBs; we also propose to remove the tenor and moratorium related requirements on housing loans given by "
              "Tier III and Tier IV UCBs; Mission-SAKSHAM intends to train over 1.4 lakh participants from UCBs",
              GOV_FEB26)])
Q(T, SUB, "Advanced",
  "Consider the following statements about RBI's proposed revision of Kisan Credit Card guidelines (February 2026):\n"
  "I. KCC tenure is to be extended to six years.\n"
  "II. Drawing limits are to be aligned with the Scale of Finance for each crop season, with crop seasons "
  "standardised.\n"
  "III. Expenses on technological interventions are to be excluded from the KCC limit.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="KCC reforms",
  explanation="The proposed guidelines include standardising crop seasons, extending KCC tenure to six years, aligning "
              "the drawing limit with the Scale of Finance for each crop season, and including (not excluding) "
              "expenses on technological interventions (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (included)"],
  why="III is wrong; 'I only' omits II.",
  current=ca(FEB26),
  facts=[fact("The proposed guidelines include standardisation of crop season, extension of KCC tenure to six years, "
              "alignment of drawing limit with Scale of Finance (SoF) for each crop season and inclusion of expenses "
              "on technological interventions", SDRP_FEB26)])
Q(T, SUB, "Advanced",
  "RBI's circular of 12 October 2026 also required Authorised Dealers to keep a Foreign Exchange Risk Reserve (FERR) "
  "on certain derivative contracts for their own hedging. Consider:\n"
  "I. It applies to INR derivative contracts where the AD buys foreign currency against INR to hedge its own assets "
  "and liabilities.\n"
  "II. The FERR equals 20% of the INR equivalent of the notional amount, kept in cash with RBI daily until the "
  "contract ends.\n"
  "III. It applies also to contracts undertaken before the circular was issued.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="FERR on banks' own hedges",
  explanation="ADs must maintain FERR on INR derivative contracts undertaken to hedge currency risk of their own "
              "assets and liabilities where they purchase foreign currency against INR (I), at 20% of the INR notional, "
              "in cash with RBI daily till termination (II). It applies only to contracts undertaken after the "
              "directions were issued (III wrong).",
  steps=["I: correct", "II: correct", "III: wrong (prospective only)"],
  why="III is wrong; 'I only' omits II.",
  current=ca("2026-10-12"),
  facts=[fact("An Authorised Dealer shall maintain a FERR for foreign exchange derivative contracts involving INR "
              "undertaken by it for hedging the currency risk of its own assets and liabilities, where it is "
              "purchasing foreign currency against INR; FERR equal to 20 per cent of the INR equivalent of the "
              "notional amount, maintained by way of cash with the Reserve Bank on a daily basis until termination; "
              "applicable to contracts undertaken after the issuance of these Directions", NDDC)])



# ================================================================= checks and output
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_005_plan.json").read_text(encoding="utf-8"))
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
AUDIT_REVISED = {"BANK_BFA_000873", "BANK_BFA_000876", "BANK_BFA_000877"}
assert AUDIT_REVISED <= {q["question_id"] for q in questions}
for q in questions:
    if q["question_id"] in AUDIT_REVISED:
        v = q["verification"]
        v["verified_by"] = [x for x in v["verified_by"] if x != "ai:independent-check"]
        v["verified_at"] = AUDIT_DAY

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_005",
    "created_at": TODAY,
    "notes": "BATCH_005 Banking and Financial Awareness part: 200 original questions (60 Basic, 80 Intermediate, "
             "60 Advanced) across 32 topics, IDs BANK_BFA_000804 to BANK_BFA_001003. Built mostly from primary texts "
             "opened on 2026-11-05: RBI history chronologies (1935-2003) and table of Bank Rate/CRR/SLR changes; RBI "
             "Organisation page; RBI FAQs on Indian currency, cheque clearing, RBI as banker to Government, SGBs, "
             "non-competitive bidding, the G-sec primer, RTGS, NEFT, ARCs, PSL, PPIs, ATMs, the PSS Act, UDGAM, Paytm "
             "Payments Bank restrictions, RB-IOS 2026 and the e-rupee; IRAC Directions and the stressed-assets "
             "framework; RBI's payments booklet; MPC resolutions and Governor's statements of May 2020, December "
             "2025, February, August and October 2026 and the February 2026 developmental statement; RBI press "
             "releases (Bank Rate 2012, RTGS 24x7, payments bank and SFB guidelines 2014, NBFC-UL list 2026-27, CVA "
             "directions, lending rates, VRRR and T-bill results of November 2026, TCCFM); October 2026 notifications "
             "on leverage ratio, operational risk and NDDCs; PIB Budget 2026-27 summary and PMJDY 12-year note; DFS "
             "PMJJBY page; SIDBI ecosystem page; Insurance Ombudsman FAQs; SEBI board meeting of 24 September 2026 "
             "and SEBI investor pages. Facts available only through search results (NPCI circulars, some news-only "
             "facts; no block was worked around) are marked web:search-confirmed. Only changeable values and dated "
             "events carry current_affairs, with the event or release date from the source. Computed answers are "
             "re-derived in tools/batch_005/banking.py. Facts tested in BATCH_000-BATCH_004 are not repeated. "
             "ai:independent-check marks only the questions a separate fresh solver answered blind and got right.",
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_005_BFA.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions; keys {dict(sorted(_keys.items()))}; "
      f"current_affairs {sum('current_affairs' in q for q in questions)}; independent {len(INDEPENDENT)})")
