"""Writes batches/parts/BATCH_006_BFA.json: the 200 Banking and Financial Awareness questions of BATCH_006.

Every fact is backed by at least one fact_check whose source was opened on 2026-11-06 (fetched with a plain client and
read; PDFs were downloaded and their text extracted), or, where only search results stated it (no block was worked
around), by search results, in which case the question carries web:search-confirmed. Only questions whose answer can
change or that report a dated event carry a current_affairs block, and its event_date is the date of that event or
release as stated by the source (Repo Rate and Budget questions always carry one, as the validator requires). Every
computable answer is re-derived below with assertions, the quota per (topic, difficulty) is checked against the batch
plan, and the answer keys are balanced. ai:independent-check is added only to the questions listed in INDEPENDENT,
which a separate fresh solver answered blind (stem and options only, no key) and got right with confidence. If any
check fails, nothing is written. All ~1,000 earlier Banking stems and answers (BATCH_000 to BATCH_005) were read
first; their facts, and neighbouring steps of the schedules they tested, are not repeated.

    python tools/batch_006/banking.py      (run from anywhere)
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
FIRST_ID = 1004
SECONDS = {"Basic": 20, "Intermediate": 30, "Advanced": 60}

_rng = random.Random(2026110606)
_keys = Counter()
questions = []

# Question numbers (offset from BANK_BFA_001004, i.e. 0 = 001004) that a separate fresh solver answered blind (stem
# and options only, no key or solution) and matched the key with high confidence. 100 questions (the even offsets
# 0-198) were given; all 100 answers matched the key, 74 with high confidence (tagged below); the 26 medium/low ones are
# not tagged. Four questions were later replaced for overlap with earlier batches (offsets 19, 71, 97, 141: none of
# them tagged); every replacement sits at the same position, so no other question's text, options or key changed.
# After the accuracy review, 22 questions were reworded or replaced (KYC and EEFC items re-sourced to the current
# Master Directions, the two draft-BC items replaced from the final Branch Authorisation Directions, payments-booklet
# items framed as of January 2021, the INRF limits item rewritten from the current FAQ, the VRRR option reworded):
# 4, 9, 12, 13, 46, 51, 73, 136, 138, 139, 142, 143, 145, 147, 148, 149, 150, 151, 153, 155, 157, 159. A second fresh
# solver answered all 22 blind and matched every key; the 17 high-confidence matches are tagged (6 of them were tagged
# before and keep the tag only because of this re-check); 51, 143, 145, 149 and 155 (medium confidence) are not.
INDEPENDENT = {0, 2, 4, 8, 10, 12, 16, 18, 20, 22, 24, 26, 28, 30, 32, 36, 40, 48, 50, 52, 54, 56, 58, 62, 64, 66, 70,
               72, 74, 78, 80, 82, 84, 86, 88, 90, 94, 96, 102, 104, 106, 110, 112, 114, 116, 118, 122, 126, 128, 130,
               132, 134, 136, 138, 142, 144, 146, 150, 154, 156, 158, 160, 162, 166, 172, 178, 180, 182, 184, 190, 192,
               194, 196, 198} | {9, 13, 46, 73, 139, 147, 148, 151, 153, 157, 159}

# URLs confirmed only through search results (each section adds its own with SEARCH_ONLY.update(...)).
SEARCH_ONLY = set()


def fact(claim, url):
    return {"claim": claim, "source_url": url, "checked_on": CHECKED}


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


NOTES = ("BATCH_006 Banking and Financial Awareness part: 200 original questions (60 Basic, 80 Intermediate, 60 "
         "Advanced) across 32 topics, IDs BANK_BFA_001004 to BANK_BFA_001203. Built from sources opened on "
         "2026-11-06 (RBI FAQs, Master Directions, notifications, press releases incl. MPC resolutions and "
         "Governor's statements of 2025-26, RBI history chronologies and rate tables, the RBI payments booklet, BIS, "
         "IBBI, SEBI, IRDAI, Insurance Ombudsman, AMFI, DFS/PMJDY pages, PIB/static.pib PDFs, and named news pages); "
         "facts seen only in search results are marked web:search-confirmed; no block was worked around. Only "
         "changeable values and dated events carry current_affairs, with the event or release date from the source. "
         "Computed answers are re-derived with asserts in tools/batch_006/banking.py. Facts tested in "
         "BATCH_000-BATCH_005 are not repeated. ai:independent-check marks only the questions a separate fresh "
         "solver answered blind and got right with confidence.")

# ---- sources (group M: replacements written by the lane author)
M_CH91 = "https://rbi.org.in/history/Brief_Chro1991to2000.html"                                   # opened 2026-11-06
# ---- sources (group A), all opened (fetched and read) on 2026-11-06
A_F = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id="
A_P = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid="
A_KYC = A_F + "173"        # FAQs on Master Direction on KYC (June 9, 2025)
A_KYCD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13141"  # Commercial Banks - KYC Directions, 2025 (updated 1 Oct 2026)
A_NR = A_F + "52"          # Accounts in India by Non-residents (Jan 16, 2025)
A_RFC = A_F + "69"         # Foreign Currency Accounts by Resident Individuals
A_EEFC = A_F + "21"        # EEFC Account
A_FXDEP = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=10198"  # MD - Deposits and Accounts (updated 2 Sep 2026)
A_CHQ = A_F + "175"        # FAQs on Cheque Clearing (Jan 07, 2026)
A_CUR = A_F + "136"        # Indian currency (Apr 15, 2025)
A_2000 = A_F + "157"       # Withdrawal of ₹2000 banknotes
A_GOVB = A_F + "61"        # RBI as Banker to Government
A_PSS = A_F + "177"        # FAQs on Authorisation Process (Apr 23, 2026)
A_DEA = A_F + "165"        # DEA Fund Scheme, 2014
A_CH60 = "https://rbi.org.in/history/Brief_Chro1960to1971.html"
A_CH68 = "https://rbi.org.in/history/Brief_Chro1968to1985.html"
A_CH91 = "https://rbi.org.in/history/Brief_Chro1991to2000.html"
A_ORG = "https://www.rbi.org.in/commonman/english/Scripts/Organisation.aspx"
A_GOVS = "https://www.rbi.org.in/Scripts/governors.aspx"
A_DGS = "https://www.rbi.org.in/Scripts/DeputyGovernors.aspx"
A_PB2L = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12074"
A_SFB25 = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=13135"
A_FINO = A_P + "61762"
A_BC = A_P + "62505"
A_BRANCH = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13164"  # CB - Branch Authorisation Directions, 2025 (updated 1 Oct 2026)
A_NSFI = A_P + "61712"
A_LVB = A_P + "50674"
A_PNB = A_P + "49590"
A_LVB2 = "https://www.outlookbusiness.com/banking/lakshmi-vilas-bank-dbil-merger-effective-from-nov-27-rbi-5582"
A_PMJDY12 = "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/aug/doc_9716_20260827_14055201.pdf"
A_PMJDYS = "https://pmjdy.gov.in/scheme"
A_INOP = "https://www.outlookmoney.com/news/mos-finance-says-15-crore-pm-jan-dhan-accounts-are-inoperative"

# ================= Banking Fundamentals (Basic 4 / Intermediate 6 / Advanced 6)
T = "Banking Fundamentals"
Q(T, "Types of accounts", "Basic",
  "According to RBI's FAQs on accounts of non-residents, interest earned in which of the following rupee accounts is "
  "exempt from income tax?",
  ["Non-Resident (External) Rupee (NRE) account", "Non-Resident Ordinary (NRO) account",
   "Special Non-Resident Rupee (SNRR) account", "Resident savings account of a returning NRI"],
  concept="Tax treatment of non-resident accounts",
  explanation="RBI's comparison table states that income earned in NRE accounts is exempt from income tax (and the "
              "balances from wealth tax), whereas income in NRO accounts is taxable.",
  steps=["NRE: repatriable and tax-exempt", "NRO: taxable"],
  why="NRO income is taxable; SNRR is a non-interest bearing business account; a resident account earns taxable "
      "interest.",
  facts=[fact("NRE: Income earned in the accounts is exempt from income tax and balances exempt from wealth tax; "
              "NRO: Taxable", A_NR)])
Q(T, "Cheques and instruments", "Basic",
  "According to RBI's FAQs on cheque clearing, up to what value can a savings account customer get cheques collected "
  "without any service charge?",
  ["Up to and including ₹1,00,000", "Up to ₹50,000", "Up to ₹25,000", "Up to ₹2,00,000"],
  concept="Cheque collection charges",
  explanation="For collection of cheques up to and including ₹1,00,000 there is no service charge for savings account "
              "customers. For higher values and other account types, charges are decided by each bank in its Cheque "
              "Collection Policy.",
  steps=["Savings account + cheque ≤ ₹1 lakh → free", "Above that → bank's own policy"],
  why="₹25,000, ₹50,000 and ₹2 lakh are not the threshold RBI states.",
  facts=[fact("For collection of cheques up to and including ₹1,00,000/-, there is no service charge for savings "
              "account customers", A_CHQ)])
Q(T, "Cheques and instruments", "Basic",
  "Under RBI's KYC rules, a demand draft, pay order or traveller's cheque can be purchased against cash only if its "
  "amount is:",
  ["Less than ₹50,000", "Less than ₹10,000", "Less than ₹20,000", "Up to ₹2,00,000"],
  concept="Cash purchase of instruments",
  explanation="Under RBI's Commercial Banks – KYC Directions, 2025, remittances by demand draft and similar modes and "
              "issue of traveller's cheques for ₹50,000 and above must be made by debit to the customer's account or "
              "against cheques, not against cash; below ₹50,000 cash is allowed.",
  steps=["Below ₹50,000 → cash allowed", "₹50,000 and above → account debit or cheque only"],
  why="₹10,000 and ₹20,000 are not the RBI limit; ₹2 lakh is the cash-receipt limit under income-tax law, not this "
      "rule.",
  facts=[fact("Any remittance of funds by way of demand draft, mail / telegraphic transfer / NEFT / IMPS or any other "
              "mode and issue of travellers' cheques for value of ₹50,000 and above shall be effected by debit to the "
              "customer's account or against cheques and not against cash payment", A_KYCD)])
Q(T, "Types of banks", "Basic",
  "DBS Bank India Ltd., into which The Lakshmi Vilas Bank was amalgamated in 2020, operates in India as:",
  ["A wholly owned subsidiary of DBS Bank Ltd, Singapore, incorporated in India as a banking company",
   "A branch of DBS Bank Ltd, Singapore, without a separate Indian company",
   "A small finance bank promoted by DBS Group",
   "A public sector bank in which DBS holds a minority stake"],
  concept="Wholly owned subsidiary mode of foreign banks",
  explanation="RBI's November 2020 press release describes DBS Bank India Ltd. as a banking company incorporated in "
              "India under the Companies Act, 2013, a wholly owned subsidiary of DBS Bank Ltd, Singapore, licensed "
              "under Section 22(1) of the BR Act on 4 October 2018.",
  steps=["Incorporated in India", "Wholly owned by DBS Bank, Singapore", "Licensed 4 October 2018"],
  why="It is not a branch, not an SFB and not a public sector bank.",
  facts=[fact("DBS Bank India Ltd. (DBIL), a banking company incorporated in India under Companies Act, 2013 ... DBIL "
              "is a wholly owned subsidiary of DBS Bank Ltd, Singapore ... issued a banking license ... under Section "
              "22 (1) of the B R Act, on October 4, 2018", A_LVB)])

Q(T, "Types of accounts", "Intermediate",
  "Under RBI's Master Direction – Deposits and Accounts (FEMA), which of the following is NOT permitted in respect "
  "of balances held in an Exchange Earners' Foreign Currency (EEFC) account?",
  ["Obtaining fund-based or non-fund-based credit facilities against the balances",
   "Crediting the balances to NRE/FCNR(B) accounts when the holder becomes a non-resident",
   "Repaying packing credit advances to the extent exports have actually taken place",
   "Making payments outside India for permitted current or capital account transactions"],
  concept="EEFC account",
  explanation="The Master Direction lists the features of the EEFC scheme: it is a non-interest bearing account; "
              "balances may be used for permitted payments abroad, to repay packing credit to the extent exports have "
              "taken place, and may be credited to NRE/FCNR(B) accounts on a change of residential status. Fund-based "
              "or non-fund-based credit facilities should not be granted against EEFC balances.",
  steps=["Permitted: payments abroad, packing credit repayment, transfer to NRE/FCNR(B) on becoming NR",
         "Not permitted: credit facilities against EEFC balances"],
  why="The other three uses are expressly allowed by the Master Direction.",
  facts=[fact("Fund-based/ non-fund based credit facilities should not be granted against the balances held in EEFC "
              "Accounts; Exporters can repay packing credit advances ... from balances in their EEFC account to the "
              "extent exports have actually taken place; Balances held in the account may be credited to NRE/ FCNR (B) "
              "Accounts ... consequent upon change of their residential status; Debits: Payment outside India towards "
              "capital or current account transactions", A_FXDEP)])
Q(T, "Types of accounts", "Intermediate",
  "Under the definition used in RBI's FAQs on accounts of non-residents, a 'Person of Indian Origin' (PIO) is a person "
  "resident outside India who is a citizen of any country other than:",
  ["Bangladesh or Pakistan, or any other country specified by the Central Government",
   "Nepal or Bhutan, or any other country specified by RBI",
   "China or Afghanistan only", "Sri Lanka or Myanmar only"],
  concept="PIO definition",
  explanation="A PIO is a person resident outside India who is a citizen of any country other than Bangladesh or "
              "Pakistan (or another country specified by the Central Government) and meets conditions such as having "
              "been an Indian citizen, or being the child, grandchild or great-grandchild or foreign-origin spouse of "
              "such a person. OCI cardholders resident outside India are included.",
  steps=["PIO excludes citizens of Bangladesh and Pakistan", "Includes OCI cardholders resident abroad"],
  why="Nepal/Bhutan, China/Afghanistan and Sri Lanka/Myanmar are not the excluded countries named.",
  facts=[fact("A 'Person of Indian Origin (PIO)' is a person resident outside India who is a citizen of any country "
              "other than Bangladesh or Pakistan or such other country as may be specified by the Central Government",
              A_NR)])
Q(T, "Types of accounts", "Intermediate",
  "For what period are fixed deposits normally accepted in an NRE account, according to RBI's FAQs?",
  ["One to three years, though banks may accept longer deposits from their asset-liability point of view",
   "Not less than 1 year and not more than 5 years, with no exceptions",
   "Seven days to ten years, as for resident term deposits", "Only for exactly one year, renewable annually"],
  concept="NRE term deposits",
  explanation="RBI's table on non-resident accounts gives the period for NRE fixed deposits as one to three years, "
              "adding that banks may accept NRE deposits above three years from their asset-liability point of view. "
              "The 1–5 year band applies to FCNR(B), and NRO deposits follow resident rules.",
  steps=["NRE FD: 1–3 years", "Longer allowed for ALM reasons"],
  why="1–5 years is the FCNR(B) band; resident-style periods apply to NRO; there is no one-year-only rule.",
  facts=[fact("Period for fixed deposits: From one to three years, However, banks are allowed to accept NRE deposits "
              "above three years from their Asset-Liability point of view", A_NR)])
Q(T, "Cheques and instruments", "Intermediate",
  "CTS-2010 standards prescribe minimum security features for cheque forms. Which of the following is NOT one of the "
  "features RBI mentions?",
  ["A photograph of the account holder printed on each leaf", "Watermark on the cheque paper",
   "The bank's logo in invisible ink", "Void pantograph"],
  concept="CTS-2010 standard cheques",
  explanation="RBI says CTS-2010 standards include mandatory minimum security features such as quality of paper, "
              "watermark, bank's logo in invisible ink and void pantograph, together with standardised field "
              "placement. A photograph of the account holder is not among them.",
  steps=["CTS-2010: paper quality, watermark, invisible-ink logo, void pantograph", "No customer photograph"],
  why="Watermark, invisible-ink logo and void pantograph are all named by RBI.",
  facts=[fact("These include provision of mandatory minimum-security features on cheque forms like quality of paper, "
              "watermark, bank's logo in invisible ink, void pantograph, etc.", A_CHQ)])
Q(T, "Types of banks", "Intermediate",
  "According to RBI's chronology, in which year were the operations of the co-operative banking system brought under "
  "the regulatory ambit of the Reserve Bank?",
  ["1966", "1949", "1975", "1984"],
  concept="RBI regulation of co-operative banks",
  explanation="RBI's chronology records that on 1 March 1966 the operations of the co-operative banking system were "
              "brought under RBI's regulatory ambit, and on 2 July 1966 twelve State Co-operative Banks were included "
              "in the Second Schedule of the RBI Act.",
  steps=["1 March 1966 → co-operative banks under RBI regulation"],
  why="1949 is the Banking Companies Act; 1975 the start of RRBs; 1984 the Urban Banks Department.",
  facts=[fact("1 Mar 1966: Operations of co-operative banking system brought under the regulatory ambit of the RBI",
              A_CH60)])
Q(T, "Types of accounts", "Intermediate",
  "If any of the documents a customer submitted at account opening, such as the OVD, is updated (for example, after a "
  "change of address), within what time must the customer submit the updated document to the bank, under "
  "RBI's KYC Directions, 2025 for commercial banks?",
  ["Within 30 days of the update", "Within 7 days of the update", "Within 6 months of the update",
   "Only at the next periodic updation of KYC"],
  concept="Updating KYC documents",
  explanation="RBI's Commercial Banks – KYC Directions, 2025 say customers shall submit to the bank the update of "
              "documents submitted at account opening within 30 days of the update, so that the bank can update its "
              "records.",
  steps=["Document updated → submit within 30 days", "Bank updates its records"],
  why="7 days and 6 months are not the period stated; it need not wait for periodic updation.",
  facts=[fact("customers shall submit to the bank the update of such documents. This shall be done within 30 days of "
              "the update to the documents for the purpose of updating the records at the bank's end", A_KYCD)])

Q(T, "Types of accounts", "Advanced",
  "Match the account with its feature as described in RBI's FAQs: 1. RFC (Domestic) account 2. Resident Foreign "
  "Currency (RFC) account 3. FCNR(B) account 4. SNRR account  P. Current account only, non-interest earning  "
  "Q. Current, savings or term deposit, interest deregulated  R. Term deposit only, for 1 to 5 years  "
  "S. Non-interest bearing rupee account whose tenure is concurrent with the holder's contract or business",
  ["1-P, 2-Q, 3-R, 4-S", "1-Q, 2-P, 3-R, 4-S", "1-P, 2-Q, 3-S, 4-R", "1-Q, 2-R, 3-P, 4-S"],
  concept="Foreign currency and special accounts",
  explanation="RFC(D) accounts are current accounts only and earn no interest; RFC accounts may be current, savings "
              "or term deposits with interest decided by the bank; FCNR(B) accounts are term deposits of 1 to 5 years; "
              "SNRR accounts are non-interest bearing and run concurrently with the holder's contract or business.",
  steps=["RFC(D) → P", "RFC → Q", "FCNR(B) → R", "SNRR → S"],
  why="The other options swap the RFC(D)/RFC types or the FCNR(B)/SNRR features.",
  facts=[fact("RFC(D): Type of Account: Current only; Interest: Non-interest earning. RFC: Current/ savings/ term "
              "deposits; Interest: De-regulated (As decided by the AD bank)", A_RFC),
         fact("FCNR(B): Term Deposit only; For terms not less than 1 year and not more than 5 years. SNRR: "
              "Non-interest bearing; Tenure: Concurrent to the tenure of the contract / period of operation / the "
              "business of the account holder", A_NR)])
Q(T, "Types of accounts", "Advanced",
  "Three foreign nationals of non-Indian origin visiting India opened NRO savings accounts with money remitted from "
  "abroad. A held his account for 5 months and it received only remittances from abroad and interest. B held hers for "
  "8 months with only remittances and interest. C held his for 4 months, but it was also credited with ₹20,000 of "
  "local fees. Who can have the balance paid out to them at the time of departure under RBI's rules?",
  ["A only", "A and B only", "A and C only", "A, B and C"],
  concept="NRO accounts of tourists",
  explanation="A tourist's NRO balance may be paid at departure provided the account was maintained for not more than "
              "six months and was not credited with any local funds other than interest. A meets both conditions; B "
              "exceeds six months; C received local funds.",
  steps=["Condition 1: ≤ 6 months → A, C", "Condition 2: no local credits except interest → A, B",
         "Both → A only"],
  why="B fails the six-month condition; C fails the no-local-funds condition.",
  facts=[fact("The balance in the NRO account may be paid to the account holder at the time of his departure from "
              "India provided the account has been maintained for a period not exceeding six months and the account "
              "has not been credited with any local funds, other than interest accrued thereon", A_NR)])
_eefc_acc, _eefc_used = 50000, 20000
assert _eefc_acc - _eefc_used == 30000
Q(T, "Types of accounts", "Advanced",
  "An exporter receives USD 50,000 of export proceeds in its EEFC account in March 2026 and, in April, uses USD 20,000 "
  "of these March accruals for an approved import payment; it has no forward commitments. Under RBI's Master "
  "Direction – Deposits and Accounts, how much of the March accruals must be converted into rupees, and by when?",
  ["USD 30,000, on or before 30 April 2026", "USD 50,000, on or before 31 March 2026",
   "USD 30,000, on or before 31 March 2027", "Nothing, because EEFC balances never need conversion"],
  concept="Conversion of EEFC accruals",
  explanation="100% of foreign exchange earnings can be credited to EEFC, but the total accruals of a calendar month "
              "must be converted into rupees on or before the last day of the succeeding calendar month, after "
              "adjusting for use for approved purposes or forward commitments. March accruals of 50,000 less 20,000 "
              "used leaves USD 30,000 to convert by 30 April 2026.",
  steps=["March accruals = USD 50,000", "Less approved use = USD 20,000 → USD 30,000",
         "Deadline: last day of the next month = 30 April 2026"],
  why="Conversion is net of approved use and due by the end of the following month, not the same month or a year "
      "later; balances are not exempt from conversion.",
  facts=[fact("Credits permitted: 100 percent of the foreign exchange earnings by way of inward remittance ...; the sum "
              "total of the accruals in the account during a calendar month should be converted into Rupees on or "
              "before the last day of the succeeding calendar month after adjusting for utilization of the balances "
              "for approved purposes or forward commitments", A_FXDEP)],
  computed=True)
Q(T, "Types of accounts", "Advanced",
  "Priya lives in Chennai, but the OVD she has shows her old New Delhi address. To open an account in Chennai she can "
  "offer: (P) an electricity bill dated six weeks ago, (Q) a post-paid mobile bill dated three months ago, (R) a "
  "municipal property tax receipt. Under RBI's KYC Directions, 2025 for commercial banks, which can serve as deemed OVDs for proof of address, "
  "and what must she do afterwards?",
  ["P and R; submit an OVD with her current address within three months",
   "P, Q and R; no further document is needed",
   "R only; submit an OVD with her current address within one year",
   "P and Q; submit an OVD with her current address within 30 days"],
  concept="Deemed OVDs for address",
  explanation="If the OVD does not show the current address, a customer may give a deemed OVD such as a utility bill "
              "not more than two months old or a property/municipal tax receipt, but must submit an OVD with the "
              "current address within three months. The three-month-old mobile bill is too old.",
  steps=["Utility bill ≤ 2 months → P valid, Q not", "Property tax receipt → R valid",
         "OVD with current address within 3 months"],
  why="Q is older than two months; the follow-up OVD is due within three months, not one year or 30 days, and it is "
      "required.",
  facts=[fact("when the customer furnishes an OVD that does not have an updated address, the bank shall deem ... "
              "utility bill which is not more than two months old of any service provider (electricity, telephone, "
              "post-paid mobile phone ...); property or Municipal tax receipt ... the customer shall submit OVD with "
              "current address within a period of three months of submitting the documents specified at (b) above",
              A_KYCD)])
Q(T, "Types of accounts", "Advanced",
  "Consider the following statements about the Depositor Education and Awareness (DEA) Fund Scheme, 2014: I. The "
  "Scheme came into effect on 24 May 2014. II. A depositor loses the right to claim the money if it is not claimed "
  "within ten years after its transfer to the DEA Fund. III. Undrawn balances in prepaid cards issued by banks are "
  "transferred to the Fund, but amounts outstanding against travellers' cheques are not. Which of the above is/are "
  "correct?",
  ["I and III only", "I and II only", "II and III only", "III only"],
  concept="DEA Fund Scheme",
  explanation="The Scheme came into effect on 24 May 2014, the date of its Gazette notification. No time limit is "
              "prescribed for claiming refunds. The amounts transferred include undrawn balances in bank-issued "
              "prepaid cards but not amounts outstanding against travellers' cheques or similar instruments.",
  steps=["I: true (24 May 2014)", "II: false (no time limit)", "III: true"],
  why="Statement II is wrong, so any option containing it is wrong; III alone omits the true statement I.",
  facts=[fact("The Scheme has come into effect from May 24, 2014", A_DEA),
         fact("There is no specific time limit prescribed in the Scheme for claiming a refund from the DEA Fund", A_DEA),
         fact("undrawn balance amounts remaining in any prepaid card issued by banks but not amounts outstanding "
              "against travellers cheques or other similar instruments", A_DEA)])
Q(T, "Types of accounts", "Advanced",
  "Rahul, an NRI, holds an NRE savings account and a three-year FCNR(B) deposit. He returns to India to take up "
  "employment. According to RBI's FAQs, which of the following is correct?",
  ["The NRE account must at once be redesignated as a resident account or moved to an RFC account, while the FCNR(B) "
   "deposit may continue till maturity at the contracted rate",
   "Both accounts must be closed on his return and the money credited to a resident savings account",
   "The NRE account may continue as an NRE account until he has stayed in India for 182 days",
   "The FCNR(B) deposit must be broken immediately, while the NRE account can continue till he chooses to close it"],
  concept="Change of residential status",
  explanation="On return for employment, NRE accounts should be designated as resident accounts, or the funds "
              "transferred to RFC accounts at the holder's option, immediately. FCNR(B) deposits may continue till "
              "maturity at the contracted rate; on maturity they are converted into resident rupee or RFC accounts.",
  steps=["NRE → redesignate as resident / transfer to RFC immediately", "FCNR(B) → may run to maturity"],
  why="Closure is not required, the NRE status does not wait 182 days, and FCNR(B) need not be broken.",
  facts=[fact("NRE accounts should be designated as resident accounts or the funds held in these accounts may be "
              "transferred to the RFC accounts, at the option of the account holder, immediately upon the return of "
              "the account holder to India for taking up employment ... FCNR (B) deposits may be allowed to continue "
              "till maturity at the contracted rate of interest", A_NR)])

# ================= History of Banking in India (Basic 1 / Intermediate 3 / Advanced 1)
T = "History of Banking in India"
Q(T, "Nationalisation", "Basic",
  "Who was the Governor of the Reserve Bank of India when 14 major commercial banks were nationalised in July 1969?",
  ["L. K. Jha", "P. C. Bhattacharya", "S. Jagannathan", "B. N. Adarkar"],
  concept="RBI leadership at nationalisation",
  explanation="L. K. Jha was Governor from 1 July 1967 to 3 May 1970. RBI's note on him records that social controls "
              "were introduced during his tenure and that 14 major commercial banks were nationalised in 1969, a step "
              "that did not have the endorsement of the Reserve Bank.",
  steps=["July 1969 falls in L. K. Jha's tenure (1967–1970)"],
  why="Bhattacharya served 1962–67; Adarkar briefly in 1970; Jagannathan from June 1970.",
  facts=[fact("L K Jha 01-07-1967 to 03-05-1970 ... 14 major commercial banks were nationalised in 1969, a step which "
              "did not have the endorsement of the Reserve Bank", A_GOVS)])
Q(T, "Nationalisation", "Intermediate",
  "The second round of bank nationalisation, in which six private sector banks were nationalised, took place on:",
  ["15 April 1980", "19 July 1980", "1 January 1980", "14 February 1980"],
  concept="1980 nationalisation",
  explanation="RBI's chronology records that on 15 April 1980 six private sector banks were nationalised to further "
              "control the heights of the economy and serve better the needs of development.",
  steps=["Six banks nationalised on 15 April 1980"],
  why="19 July is the 1969 date; the other dates are not linked to the event.",
  facts=[fact("15 Apr 1980: Six private sector banks nationalised", A_CH68)])
Q(T, "Committees", "Intermediate",
  "M. Narasimham, who chaired the Committee on the Financial System (1991), later chaired which committee in 1998?",
  ["Committee on Banking Sector Reforms", "Committee on Reform of the Insurance Sector",
   "Committee on Capital Account Convertibility", "Committee on Financial Sector Reforms"],
  concept="Narasimham Committees",
  explanation="RBI's profile of M. Narasimham (Governor in 1977) notes that he chaired the Committee on the Financial "
              "System, 1991 and the Committee on Banking Sector Reforms, 1998.",
  steps=["1991 → Committee on the Financial System", "1998 → Committee on Banking Sector Reforms"],
  why="The insurance reform committee (1994) was chaired by R. N. Malhotra; the others were chaired by other people.",
  facts=[fact("He was chairperson of the Committee on the Financial System, 1991 and the Committee of Banking Sector "
              "Reforms, 1998", A_GOVS),
         fact("1994: 'Committee on Reform of the Insurance Sector', RN Malhotra", A_CH91)])
# ================= History of Banking in India (1 Intermediate)
Q("History of Banking in India", "Nationalisation", "Intermediate",
  "According to RBI's chronology, what were nationalised banks allowed to do from 15 July 1994?",
  ["Tap the capital market to strengthen their capital base",
   "Open branches abroad without the Government's approval",
   "Reduce the Government's shareholding below 51 per cent",
   "Merge with one another without a Government scheme"],
  concept="Recapitalisation of nationalised banks after 1991",
  explanation="RBI's chronology for 1991–2000 records that on 15 July 1994 nationalised banks were allowed to tap the "
              "capital market to strengthen their capital base, part of the reforms that followed the 1991 "
              "Narasimham Committee report.",
  steps=["15 July 1994 → nationalised banks may raise capital from the market", "Purpose: strengthen capital base"],
  why="The chronology records no such permission for overseas branches, cutting the Government's stake below 51% or "
      "mergers without a Government scheme; amalgamations of nationalised banks are made by Government schemes.",
  facts=[fact("15 Jul 1994: Nationalised Banks allowed to tap the capital market to strengthen their capital base",
              M_CH91)])
Q(T, "Mergers and consolidation", "Advanced",
  "Consider the following statements: I. The amalgamation of Oriental Bank of Commerce and United Bank of India into "
  "Punjab National Bank was a scheme framed by RBI under Section 45 of the Banking Regulation Act. II. The amalgamation "
  "of The Lakshmi Vilas Bank with DBS Bank India Ltd. came into force on 27 November 2020, from when LVB's branches "
  "functioned as DBS Bank India branches. III. Both these amalgamations were sanctioned under section 9 of the "
  "Banking Companies (Acquisition and Transfer of Undertakings) Acts. Which of the above is/are correct?",
  ["II only", "I and II only", "II and III only", "I, II and III"],
  concept="Legal routes for bank amalgamations",
  explanation="The OBC/UBI scheme was issued by the Government of India under section 9 of the Banking Companies "
              "(Acquisition and Transfer of Undertakings) Acts of 1970 and 1980, not by RBI. LVB, a private sector "
              "lender under moratorium, was amalgamated with DBS Bank India through a scheme that RBI itself drafted "
              "and placed in the public domain for objections; it took effect on 27 November 2020. Being a private "
              "bank, LVB was outside the bank nationalisation Acts.",
  steps=["I: false (Government scheme under section 9 of the 1970/1980 Acts)", "II: true",
         "III: false (LVB was not a nationalised bank)"],
  why="Statements I and III are wrong, so every option containing them is wrong.",
  facts=[fact("Amalgamation of Oriental Bank of Commerce and United Bank of India into Punjab National Bank Scheme, "
              "2020 dated March 4, 2020, issued by the Government of India ... in terms of section 9 of the Banking "
              "Companies (Acquisition and Transfer of Undertakings) Act, 1970 ... and section 9 of the Banking "
              "Companies (Acquisition and Transfer of Undertakings) Act, 1980", A_PNB),
         fact("The Reserve Bank of India has today placed in public domain a draft scheme of amalgamation of The "
              "Lakshmi Vilas Bank Ltd. (LVB) with DBS Bank India Ltd.", A_LVB),
         fact("The amalgamation will come into force on the Appointed date i.e. November 27, 2020. All the branches "
              "of the Lakshmi Vilas Bank Ltd. will function as branches of DBS Bank India Ltd. with effect from this "
              "date", A_LVB2),
         fact("The RBI had superseded the board of LVB on November 17 following the imposition of a moratorium on "
              "the private sector lender", A_LVB2)])

# ================= Reserve Bank of India (Basic 2 / Intermediate 3 / Advanced 2)
T = "Reserve Bank of India"
Q(T, "Establishment and structure", "Basic",
  "According to RBI's Organisation and Functions page, at how many locations does the Reserve Bank of India have "
  "offices?",
  ["34", "19", "27", "41"],
  concept="RBI's office network",
  explanation="RBI states that it has offices at 34 locations. (Separately, it runs currency operations through 19 "
              "Issue Offices.)",
  steps=["RBI offices: 34 locations"],
  why="19 is the number of Issue Offices; 27 and 41 are not RBI figures.",
  facts=[fact("The Reserve Bank of India has offices at 34 locations", A_ORG)])
Q(T, "Governors and leadership", "Basic",
  "Which Governor of RBI had served as Chairman and Managing Director of the Life Insurance Corporation of India "
  "before his appointment?",
  ["K. R. Puri", "N. C. Sen Gupta", "S. Jagannathan", "I. G. Patel"],
  concept="Backgrounds of RBI Governors",
  explanation="RBI's profile says K. R. Puri (Governor 1975–77) was Chairman and Managing Director of LIC before "
              "becoming Governor.",
  steps=["K. R. Puri: LIC CMD → RBI Governor (20 August 1975)"],
  why="Sen Gupta was Banking Secretary; Jagannathan was Executive Director at the World Bank; I. G. Patel came from "
      "the Finance Ministry and UNDP.",
  facts=[fact("K R Puri served as the Chairman and Managing Director of the Life Insurance Corporation of India before "
              "his appointment as Governor", A_GOVS)])
Q(T, "Governors and leadership", "Intermediate",
  "According to RBI's history of its Governors, which two Governors did not sign any bank notes?",
  ["Sir Osborne Smith and K. G. Ambegaonkar", "Sir James Taylor and B. N. Adarkar",
   "Sir C. D. Deshmukh and N. C. Sen Gupta", "K. G. Ambegaonkar and A. Ghosh"],
  concept="RBI Governors and bank notes",
  explanation="RBI notes that Sir Osborne Smith, the first Governor, did not sign any bank notes (RBI's first notes "
              "came in 1938, after he left), and that K. G. Ambegaonkar, interim Governor in January–February 1957, "
              "also did not sign any.",
  steps=["Osborne Smith: no notes", "Ambegaonkar: no notes"],
  why="RBI's profiles name only Osborne Smith and Ambegaonkar as Governors who did not sign notes.",
  facts=[fact("Sir Osborne, however, did not sign any bank notes during his tenure", A_GOVS),
         fact("K G Ambegaonkar did not sign any bank notes", A_GOVS)])
Q(T, "Governors and leadership", "Intermediate",
  "Who took office as a Deputy Governor of the Reserve Bank of India on 4 May 2026?",
  ["Rohit Jain", "T. Rabi Sankar", "M. Rajeshwar Rao", "Shirish Chandra Murmu"],
  concept="RBI Deputy Governors",
  explanation="RBI's list of Deputy Governors shows Rohit Jain in office from 04.05.2026. T. Rabi Sankar's term ended "
              "on 02.05.2026; M. Rajeshwar Rao served till October 2025; Shirish Chandra Murmu took office on "
              "9 October 2025.",
  steps=["Rohit Jain: 04.05.2026 onwards"],
  why="Rabi Sankar's term ended on 2 May 2026; Rajeshwar Rao left in 2025; Murmu joined in October 2025.",
  facts=[fact("68. Shri Rohit Jain 04.05.2026 onwards; 67. Shri Shirish Chandra Murmu 09.10.2025 onwards; 64. Shri T. "
              "Rabi Sankar ... 03.05.2025 to 02.05.2026", A_DGS)],
  current=ca("2026-05-04"))
Q(T, "Governors and leadership", "Intermediate",
  "Sir C. D. Deshmukh, the first Indian Governor of RBI, represented India at the Bretton Woods negotiations in 1944. "
  "Which office did he later hold between 1950 and 1956?",
  ["Union Finance Minister", "Chairman of the Planning Commission", "Chairman of the State Bank of India",
   "India's Executive Director at the IMF"],
  concept="C. D. Deshmukh",
  explanation="RBI's profile of Deshmukh (Governor 1943–49) says he represented India at Bretton Woods in 1944, saw "
              "RBI's nationalisation on 1 January 1949, and later held the office of Union Finance Minister in "
              "1950–56.",
  steps=["After RBI → Union Finance Minister (1950–56)"],
  why="He did not chair the Planning Commission or SBI, nor serve as Executive Director at the IMF.",
  facts=[fact("During his tenure as Governor, he represented India at the Bretton Woods negotiations in 1944 ... He "
              "later held the office of Union Finance Minister between 1950-56", A_GOVS)])
Q(T, "Governors and leadership", "Advanced",
  "Consider the following statements about RBI Governors, based on RBI's profiles: I. M. Narasimham is the first and "
  "so far the only Governor appointed from the Reserve Bank cadre. II. L. K. Jha left before completing his term "
  "because he was appointed Union Finance Minister. III. Both H. V. R. Iengar and P. C. Bhattacharya had served as "
  "Chairman of the State Bank of India before becoming Governor. Which of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="Backgrounds of RBI Governors",
  explanation="Narasimham joined RBI as a Research Officer and is the only Governor from the RBI cadre. L. K. Jha left "
              "in May 1970 on appointment as India's Ambassador to the United States, not as Finance Minister. Iengar "
              "(briefly) and Bhattacharya both chaired SBI before becoming Governor.",
  steps=["I: true", "II: false (Ambassador to the US)", "III: true"],
  why="Statement II is wrong, so options containing it are wrong.",
  facts=[fact("M Narasimham was the first and so far the only Governor to be appointed from the Reserve Bank cadre",
              A_GOVS),
         fact("L K Jha was appointed India's Ambassador to the United States in May 1970 prior to the completion of "
              "his term as Governor", A_GOVS),
         fact("H V R Iengar ... served for a brief while as the Chairman of State Bank of India, before being "
              "appointed as the Governor; P C Bhattacharya ... later as Chairman of the State Bank of India prior to "
              "his appointment as Governor", A_GOVS)])
Q(T, "Governors and leadership", "Advanced",
  "Match the RBI Governor with a development RBI records during his tenure: 1. H. V. R. Iengar 2. S. Jagannathan "
  "3. K. R. Puri 4. R. N. Malhotra  P. Regional Rural Banks set up  Q. India's shift to decimal coinage  "
  "R. Service Area Approach adopted for rural finance  S. State Level Bankers' Committees set up",
  ["1-Q, 2-S, 3-P, 4-R", "1-Q, 2-P, 3-S, 4-R", "1-S, 2-Q, 3-P, 4-R", "1-Q, 2-S, 3-R, 4-P"],
  concept="Developments under RBI Governors",
  explanation="RBI's profiles record decimal coinage under Iengar (1957–62); SLBCs and the Credit Guarantee "
              "Corporation under Jagannathan (1970–75); Regional Rural Banks under K. R. Puri (1975–77); and the "
              "Service Area Approach, DFHI and NHB under R. N. Malhotra (1985–90).",
  steps=["Iengar → decimal coinage", "Jagannathan → SLBCs", "Puri → RRBs", "Malhotra → Service Area Approach"],
  why="The other options swap the RRB, SLBC or Service Area Approach links.",
  facts=[fact("H V R Iengar ... His tenure witnessed India's shift to decimal coinage from the earlier system", A_GOVS),
         fact("S Jagannathan ... the setting up of State Level Bankers' Committees", A_GOVS),
         fact("K R Puri ... During his tenure, Regional Rural Banks were set up", A_GOVS),
         fact("R.N. Malhotra ... In the field of rural finance, the Service Area Approach was adopted", A_GOVS)])

# ================= RBI Functions (Basic 3 / Intermediate 3 / Advanced 2)
T = "RBI Functions"
Q(T, "Issuer of currency", "Basic",
  "Up to what denomination can coins be issued under the Coinage Act, 2011, according to RBI?",
  ["₹1,000", "₹100", "₹500", "₹10,000"],
  concept="Coin denominations",
  explanation="Coins are currently issued in denominations of 50 paise, ₹1, ₹2, ₹5, ₹10 and ₹20, but the Coinage "
              "Act, 2011 allows coins to be issued up to a denomination of ₹1,000. (The ₹10,000 ceiling applies to "
              "bank notes under the RBI Act.)",
  steps=["Coinage Act, 2011 → coins up to ₹1,000"],
  why="₹10,000 is the ceiling for bank notes; ₹100 and ₹500 are not the statutory limit.",
  facts=[fact("Coins can be issued up to the denomination of ₹1000 under The Coinage Act, 2011", A_CUR)])
Q(T, "Issuer of currency", "Basic",
  "The first banknote of the Mahatma Gandhi (New) Series, introduced on 8 November 2016, was of which denomination and "
  "theme?",
  ["₹2000, with the theme of Mangalyaan", "₹500, with the Red Fort", "₹200, with the Sanchi Stupa",
   "₹100, with Rani ki Vav"],
  concept="Mahatma Gandhi (New) Series",
  explanation="RBI says the first note of the MG (New) Series was introduced on 8 November 2016 in a new "
              "denomination, ₹2000, with the theme of Mangalyaan; ₹500, ₹200, ₹100, ₹50, ₹20 and ₹10 followed.",
  steps=["First MGNS note: ₹2000", "Theme: Mangalyaan"],
  why="₹500, ₹200 and ₹100 notes came later in the series.",
  facts=[fact("The first banknote from the new series was introduced on November 8, 2016 in a new denomination i.e. "
              "₹2000 with the theme of Mangalyaan", A_CUR)])
Q(T, "Issuer of currency", "Basic",
  "Who decides the quantity of coins to be minted in India each year?",
  ["The Government of India, on the basis of RBI's yearly indent", "RBI alone, under Section 22 of the RBI Act",
   "SPMCIL, based on its production capacity", "The Central Board of RBI, with Parliament's approval"],
  concept="Coin management",
  explanation="RBI says the Government of India decides the quantity of coins to be minted on the basis of the "
              "indent received from RBI every year. The Government designs and mints coins; RBI only distributes "
              "them.",
  steps=["RBI sends a yearly indent", "Government decides the quantity"],
  why="Section 22 gives RBI the sole right to issue bank notes, not coins; SPMCIL only mints; Parliament does not "
      "approve quantities.",
  facts=[fact("The Government of India decides on the quantity of coins to be minted on the basis of indent received "
              "from the Reserve Bank on yearly basis", A_CUR)])
Q(T, "Issuer of currency", "Intermediate",
  "Which is the highest denomination banknote ever printed by the Reserve Bank of India, and when was it first "
  "printed?",
  ["₹10,000, in 1938", "₹5,000, in 1954", "₹10,000, in 1954", "₹2,000, in 2016"],
  concept="High denomination notes",
  explanation="RBI says the highest denomination note it ever printed was the ₹10,000 note of 1938, demonetised in "
              "January 1946, reintroduced in 1954 and demonetised again in 1978.",
  steps=["₹10,000 first printed in 1938", "Demonetised 1946; reintroduced 1954; demonetised 1978"],
  why="1954 was a reintroduction; ₹5,000 and ₹2,000 are lower denominations.",
  facts=[fact("The highest denomination note ever printed by the Reserve Bank of India was the ₹10000 note in 1938 "
              "which was demonetized in January 1946. The ₹10000 was again introduced in 1954. These notes were "
              "demonetized in 1978", A_CUR)])
Q(T, "Issuer of currency", "Intermediate",
  "According to RBI, the ₹2000 banknote was introduced in November 2016 to meet the currency requirement quickly "
  "after the withdrawal of old ₹500 and ₹1000 notes. In which year was its printing stopped?",
  ["2018-19", "2016-17", "2019-20", "2022-23"],
  concept="₹2000 banknote",
  explanation="RBI's FAQs say the ₹2000 note was introduced under Section 24(1) of the RBI Act; once its objective "
              "was met and other denominations were adequately available, its printing was stopped in 2018-19. "
              "Its withdrawal from circulation was announced in May 2023 under the Clean Note Policy.",
  steps=["Introduced Nov 2016 under Section 24(1)", "Printing stopped in 2018-19"],
  why="2016-17 was its first year; 2019-20 and 2022-23 are not the year RBI gives.",
  facts=[fact("printing of ₹2000 banknote was stopped in 2018-19", A_2000)])
Q(T, "Regulator and supervisor", "Intermediate",
  "If RBI refuses an entity's application for authorisation to operate a payment system under the PSS Act, 2007, what "
  "restriction applies to the entity?",
  ["A cooling period of one year, during which it cannot apply to operate any payment system",
   "A cooling period of three years, only for the same payment system",
   "A cooling period of six months, only for the same payment system",
   "No restriction; it can reapply at once after rectifying the issues"],
  concept="Payment system authorisation",
  explanation="RBI's FAQs distinguish return from refusal. A returned application can be resubmitted after "
              "rectification, but after a refusal a cooling period of one year applies, during which the entity "
              "cannot apply for that or any other payment system.",
  steps=["Refusal → one-year cooling period", "Bar covers any payment system"],
  why="The period is one year and covers all payment systems; immediate reapplication applies only to returned "
      "applications.",
  facts=[fact("Cooling period of one year shall be applicable on entities whose application is refused. During this "
              "period applicant entity is prohibited from submitting a fresh application for not only the payment "
              "system but also for any other payment system", A_PSS)])
Q(T, "Banker to government", "Advanced",
  "Consider the following statements about RBI as banker to the Government: I. Under Section 21 of the RBI Act, RBI "
  "has the right to transact the Government business of the Union in India. II. RBI is the aggregator for accounting "
  "of all GST collections in the respective government accounts. III. If a receipted challan for a payment into "
  "Government account is lost, a duplicate challan is issued on payment of the prescribed fee. Which of the above "
  "is/are correct?",
  ["I and II only", "I and III only", "II and III only", "I, II and III"],
  concept="RBI's government banking role",
  explanation="Section 20 obliges RBI to handle the Central Government's banking and Section 21 gives it the right "
              "to transact the Union's Government business. RBI aggregates GST collections reported by agency banks. "
              "No duplicate challan is issued under any circumstances; instead a 'Certificate of Credit' is issued "
              "on request and payment of a fee.",
  steps=["I: true", "II: true", "III: false (Certificate of Credit, not a duplicate challan)"],
  why="Statement III is wrong, so options containing it are wrong.",
  facts=[fact("as per Section 21 of the said Act, RBI has the right to transact Government business of the Union in "
              "India", A_GOVB),
         fact("The Reserve Bank of India is the aggregator for accounting of all GST collections in the respective "
              "government accounts", A_GOVB),
         fact("No duplicate challan is issued under any circumstances. Instead, a 'Certificate of Credit' is issued "
              "on specific request with the requisite particulars and payment of prescribed fee", A_GOVB)])
Q(T, "Issuer of currency", "Advanced",
  "Which of the following statements is correct according to RBI's FAQs on Indian currency?",
  ["Mere possession of a forged note does not attract punishment; possessing one knowingly with intent to use it as "
   "genuine is an offence",
   "The MANI mobile app authenticates whether a banknote is genuine or counterfeit",
   "RBI has limited the coins a customer can deposit in a bank account to ₹1,000 a day",
   "Banknotes with writing or colour stains on them cease to be legal tender"],
  concept="Currency rules for the public",
  explanation="RBI says mere possession of a forged note is not punishable; possession knowing it to be forged and "
              "intending to use it as genuine is an offence under Section 180 of the BNS, 2023. MANI only identifies "
              "denominations for the visually impaired and does not authenticate notes. RBI prescribes no limit on "
              "coin deposits. Notes with writing or stains remain legal tender if decipherable.",
  steps=["Forged note: mere possession not punishable", "MANI: denomination only", "No coin deposit limit",
         "Stained notes: still legal tender"],
  why="The MANI app does not check genuineness; RBI sets no coin-deposit limit; stained or scribbled notes remain "
      "legal tender.",
  facts=[fact("Mere possession of a forged note does not attract punishment. Possession of any forged or counterfeit "
              "banknotes, knowing or having reason to believe the same to be forged or counterfeit and intending to "
              "use the same as genuine ... are offences under Section 180 of the Bhartiya Nyaya Sanhita (BNS), 2023",
              A_CUR),
         fact("This mobile application does not authenticate a note as being either genuine or counterfeit", A_CUR),
         fact("RBI has not prescribed any limit for coin deposits by customers with banks", A_CUR)])

# ================= Payment Banks (Basic 1 / Intermediate 1 / Advanced 1)
T = "Payment Banks"
Q(T, "Deposit limit", "Basic",
  "Before RBI raised it in April 2021, what was the maximum end-of-day balance a payments bank could hold per "
  "individual customer under the 2014 licensing guidelines?",
  ["₹1 lakh", "₹50,000", "₹1.5 lakh", "₹5 lakh"],
  concept="Payments bank balance limit",
  explanation="The November 2014 guidelines restricted payments banks to a maximum balance of ₹1 lakh per individual "
              "customer. Citing progress in financial inclusion, RBI raised the limit to ₹2 lakh with immediate "
              "effect in April 2021.",
  steps=["2014: ₹1 lakh", "April 2021: raised to ₹2 lakh"],
  why="₹50,000, ₹1.5 lakh and ₹5 lakh were never the limit.",
  facts=[fact("PBs were restricted to hold a maximum balance of ₹1 lakh per individual customer at the end of the day "
              "... it has been decided to enhance the limit of maximum balance at the end of the day from ₹1 lakh to "
              "₹2 lakh per individual customer of PBs with immediate effect", A_PB2L)])
Q(T, "Permitted activities", "Intermediate",
  "All bank branches must exchange soiled notes and adjudicate mutilated notes under the Note Refund Rules. Which "
  "banks may exchange mutilated and imperfect notes at their option, according to RBI?",
  ["Payments banks, and small finance banks up to two years from the start of their banking business",
   "Regional Rural Banks and co-operative banks",
   "Foreign banks operating through branches",
   "Small finance banks permanently, but never payments banks"],
  concept="Note exchange by differentiated banks",
  explanation="RBI's currency FAQs say all banks must exchange soiled notes and all commercial bank branches must "
              "adjudicate mutilated notes, but small finance banks (for two years after starting business) and "
              "payments banks may exchange mutilated and imperfect notes at their option.",
  steps=["General rule: all branches exchange", "Option: payments banks; SFBs for first two years"],
  why="RRBs, co-operative banks and foreign banks get no such option; for SFBs the option lasts only two years.",
  facts=[fact("Small Finance Banks (up to two years from the commencement of their banking business) and Payment "
              "Banks may exchange mutilated and imperfect/defective notes at their option", A_CUR)])
Q(T, "Permitted activities", "Advanced",
  "Consider the following statements: I. If the promoter of a payments bank wants to set up a small finance bank, both "
  "banks must be held under a Non-Operative Financial Holding Company (NOFHC). II. When a payments bank converts into "
  "a small finance bank, the payments bank ceases to exist and its business folds into the SFB. III. RBI's April 2021 "
  "increase in the payments bank balance limit to ₹2 lakh took effect immediately. Which of the above is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I and III only"],
  concept="Payments banks and SFB conversion",
  explanation="The SFB Licensing Guidelines, 2025 require a payments bank promoter who wants an SFB to hold both under "
              "an NOFHC, and say that on conversion the NBFC/MFI/PB ceases to exist with its permitted business folded "
              "into the bank. RBI's April 2021 circular raised the limit from ₹1 lakh to ₹2 lakh with immediate "
              "effect.",
  steps=["I: true", "II: true", "III: true"],
  why="All three statements are correct, so options omitting any of them are wrong.",
  facts=[fact("If a promoter of a payments bank desires to set up a small finance bank, both the banks should be under "
              "NOFHC structure", A_SFB25),
         fact("on conversion into a small finance bank, the NBFC / MFI / PB will cease to exist and all its business "
              "which a bank can undertake should fold into the bank", A_SFB25),
         fact("enhance the limit of maximum balance at the end of the day from ₹1 lakh to ₹2 lakh per individual "
              "customer of PBs with immediate effect", A_PB2L)])

# ================= Small Finance Banks (Basic 1 / Intermediate 3 / Advanced 2)
T = "Small Finance Banks"
Q(T, "Licensing norms", "Basic",
  "Under the RBI (Small Finance Banks – Licensing) Guidelines, 2025, how is a small finance bank constituted and "
  "licensed?",
  ["As a public limited company, licensed under Section 22 of the Banking Regulation Act, 1949",
   "As a co-operative society, registered under the Multi-State Co-operative Societies Act",
   "As a statutory corporation under a special Act of Parliament",
   "As an NBFC registered under Section 45-IA of the RBI Act"],
  concept="Legal form of SFBs",
  explanation="The guidelines say an SFB shall be registered as a public limited company under the Companies Act, "
              "2013 and licensed under Section 22 of the BR Act, 1949; it gets scheduled bank status once it "
              "commences operations.",
  steps=["Public limited company", "Licence under Section 22, BR Act"],
  why="SFBs are not co-operatives, statutory corporations or NBFCs.",
  facts=[fact("The small finance bank shall be registered as a public limited company under the Companies Act, 2013. "
              "It will be licensed under Section 22 of the Banking Regulation Act, 1949", A_SFB25)])
Q(T, "PSL targets", "Intermediate",
  "Small finance banks must lend 60% of ANBC or CEOBE (whichever is higher) to the priority sector. How is this "
  "requirement split under the SFB Licensing Guidelines, 2025?",
  ["40% across PSL sub-sectors as per the extant prescriptions, and the remaining 20% to any PSL sub-sectors where "
   "the SFB has competitive advantage",
   "50% to agriculture and 10% to micro enterprises",
   "40% to micro finance and 20% to housing",
   "30% to weaker sections and 30% to any PSL sub-sector"],
  concept="SFB priority sector requirement",
  explanation="The 60% PSL requirement has two parts: 40% of ANBC or CEOBE must be allocated to the different PSL "
              "sub-sectors as per the extant PSL prescriptions, and the balance 20% can go to any one or more PSL "
              "sub-sectors where the bank has competitive advantage.",
  steps=["60% total", "40% as per extant sub-sector prescriptions", "20% flexible"],
  why="The other splits are invented; RBI does not earmark 50% for agriculture or 30% for weaker sections here.",
  facts=[fact("the bank will be required to extend 60 per cent of its Adjusted Net Bank Credit (ANBC) or Credit "
              "Equivalent of Off-Balance Sheet Exposures (CEOBE), whichever is higher, to the sectors eligible for "
              "classification as priority sector lending (PSL) by RBI. While 40 per cent of its ANBC or CEOBE, "
              "whichever is higher, should be allocated to different sub-sectors under PSL as per the extant PSL "
              "prescriptions, the bank can allocate the balance 20 per cent to any one or more sub-sectors under the "
              "PSL where it has competitive advantage", A_SFB25)])
Q(T, "Licensing norms", "Intermediate",
  "On 5 December 2025, RBI granted 'in-principle' approval to which payments bank for conversion into a small finance "
  "bank?",
  ["Fino Payments Bank Limited", "Airtel Payments Bank Limited", "India Post Payments Bank Limited",
   "Jio Payments Bank Limited"],
  concept="Payments bank to SFB conversion",
  explanation="RBI's press release of 5 December 2025 announced in-principle approval to Fino Payments Bank Limited "
              "to convert into an SFB, assessed under the 'on tap' SFB guidelines, which allow resident-controlled "
              "payments banks with five years of operations to convert.",
  steps=["5 December 2025 → Fino Payments Bank", "Route: on-tap SFB guidelines"],
  why="RBI's release names only Fino Payments Bank.",
  facts=[fact("The Reserve Bank has today granted 'in-principle' approval to Fino Payments Bank Limited (FPBL) for "
              "conversion into a Small Finance Bank (SFB)", A_FINO)],
  current=ca("2025-12-05"))
Q(T, "Licensing norms", "Intermediate",
  "A small finance bank wants to distribute mutual fund units and insurance products. Under the SFB Licensing "
  "Guidelines, 2025, when does it need RBI's prior approval for this?",
  ["Only during the first three years from commencement of operations; after that the extant norms apply",
   "Always, for every new product it distributes",
   "Never, because distribution needs only the sectoral regulator's approval",
   "Only after it is listed on a stock exchange"],
  concept="Para-banking by SFBs",
  explanation="SFBs may distribute non-risk-sharing products such as mutual fund units, insurance and pension "
              "products with RBI's prior approval and the sectoral regulator's requirements. After three years from "
              "commencement of operations, RBI's prior approval is no longer required.",
  steps=["First 3 years → RBI prior approval", "Thereafter → extant norms"],
  why="Approval is not permanent, not absent, and not linked to listing.",
  facts=[fact("A small finance bank can also undertake other non-risk sharing simple financial services activities ... "
              "such as distribution of mutual fund units, insurance products, pension products, etc. with the prior "
              "approval of the RBI ... After three years from the date of commencement of operations of the bank, "
              "requirement for prior approval from the Reserve Bank will no longer apply", A_SFB25)])
_anbc, _ceobe = 4000, 4200
_base = max(_anbc, _ceobe)
assert (round(_base * 0.60), round(_base * 0.40)) == (2520, 1680)
Q(T, "PSL targets", "Advanced",
  "A small finance bank has ANBC of ₹4,000 crore and CEOBE of ₹4,200 crore. Under the SFB Licensing Guidelines, 2025, "
  "what is its overall priority sector target, and how much of it must be allocated across PSL sub-sectors as per the "
  "extant prescriptions?",
  ["₹2,520 crore overall; ₹1,680 crore as per extant sub-sector prescriptions",
   "₹2,400 crore overall; ₹1,600 crore as per extant sub-sector prescriptions",
   "₹3,150 crore overall; ₹1,680 crore as per extant sub-sector prescriptions",
   "₹2,520 crore overall; ₹840 crore as per extant sub-sector prescriptions"],
  concept="SFB PSL computation",
  explanation="The base is the higher of ANBC and CEOBE, i.e. ₹4,200 crore. The overall target is 60% = ₹2,520 crore; "
              "40% = ₹1,680 crore must follow the extant sub-sector prescriptions; the remaining 20% = ₹840 crore can "
              "go to sub-sectors where the bank has competitive advantage.",
  steps=["Base = max(4,000, 4,200) = ₹4,200 crore", "60% × 4,200 = ₹2,520 crore", "40% × 4,200 = ₹1,680 crore"],
  why="₹2,400/₹1,600 crore uses ANBC instead of the higher CEOBE; ₹3,150 crore applies the old 75% target; ₹840 crore "
      "is the flexible 20% part.",
  facts=[fact("extend 60 per cent of its Adjusted Net Bank Credit (ANBC) or Credit Equivalent of Off-Balance Sheet "
              "Exposures (CEOBE), whichever is higher ... While 40 per cent of its ANBC or CEOBE, whichever is higher, "
              "should be allocated to different sub-sectors under PSL as per the extant PSL prescriptions", A_SFB25)],
  computed=True)
Q(T, "Licensing norms", "Advanced",
  "Consider the following statements under the SFB Licensing Guidelines, 2025: I. An NBFC converting into an SFB must "
  "reach a net worth of ₹300 crore within eighteen months of in-principle approval or by the date it starts "
  "operations, whichever is earlier. II. An SFB may have exposure to its promoters up to 10% of its capital funds. "
  "III. A group with total assets of ₹6,000 crore whose non-financial business makes up 45% of its assets is treated "
  "as a large industrial house, and its SFB proposal will not be entertained. Which of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="SFB licensing conditions",
  explanation="Converting NBFCs/MFIs/LABs/PBs must have ₹300 crore net worth, or infuse capital to reach it within 18 "
              "months of in-principle approval or by commencement, whichever is earlier. SFBs are precluded from any "
              "exposure to their promoters, to 10%-plus shareholders and their relatives. A group with assets of "
              "₹5,000 crore or more and non-financial business of 40% or more is a large industrial house, whose "
              "proposals are not entertained.",
  steps=["I: true", "II: false (no exposure to promoters at all)", "III: true (₹6,000 cr ≥ ₹5,000 cr; 45% ≥ 40%)"],
  why="Statement II is wrong, so options containing it are wrong.",
  facts=[fact("Converted from NBFC/MFI/LAB/PB: The entity shall have a minimum net worth of ₹300 crore or it shall "
              "infuse additional paid-up voting equity share capital to achieve net worth of ₹300 crore within "
              "eighteen months from the date of in-principle approval or as on the date of commencement of "
              "operations, whichever is earlier", A_SFB25),
         fact("the small finance bank is precluded from having any exposure to its promoters, shareholders who have "
              "shareholding of 10 per cent or more of paid-up share capital or voting rights in the bank", A_SFB25),
         fact("a group with assets of ₹5,000 crore or more with the non-financial business of the group accounting "
              "for 40 per cent or more in terms of total assets / gross income, will be treated as a large industrial "
              "house / business groups", A_SFB25)])

# ================= Financial Inclusion (Basic 1 / Intermediate 3 / Advanced 5)
T = "Financial Inclusion"
Q(T, "PMJDY and allied schemes", "Basic",
  "Under Pradhan Mantri Jan-Dhan Yojana, which type of account is opened, and for whom?",
  ["A basic savings bank deposit (BSBD) account, for persons not having any other account",
   "A current account, for small traders without GST registration",
   "A recurring deposit account, for every household",
   "A fixed deposit account with a ₹1,000 minimum, for every adult"],
  concept="PMJDY account",
  explanation="The PMJDY scheme page says a basic savings bank deposit (BSBD) account can be opened in any bank branch "
              "or Business Correspondent (Bank Mitra) outlet by persons not having any other account, with no minimum "
              "balance.",
  steps=["PMJDY → BSBD account", "For persons without any other account"],
  why="PMJDY does not open current, recurring or fixed deposit accounts.",
  facts=[fact("Under the scheme, a basic savings bank deposit (BSBD) account can be opened in any bank branch or "
              "Business Correspondent (Bank Mitra) outlet, by persons not having any other account", A_PMJDYS)])
Q(T, "Business correspondents", "Intermediate",
  "Under RBI's Commercial Banks – Branch Authorisation Directions, 2025, which non-banking financial companies may a "
  "bank engage as Business Correspondents?",
  ["Non-deposit taking NBFCs, provided bank funds are not commingled with the NBFC's funds and other safeguards are met",
   "No NBFC of any kind may be engaged as a Business Correspondent",
   "Only deposit-taking NBFCs with an investment-grade rating",
   "Any NBFC registered with RBI, without any further conditions"],
  concept="Eligible Business Correspondents",
  explanation="The 2025 Directions allow banks to engage, among others, individuals, NGOs/MFIs, co-operative societies, "
              "post offices, payments banks, companies (other than NBFCs) with widespread retail outlets, and "
              "non-deposit taking NBFCs (NBFCs-ND). For an NBFC-ND, there must be no commingling of bank and NBFC "
              "funds, a specific contract addressing conflicts of interest, and no restrictive practices such as "
              "offering services only to the NBFC's own customers.",
  steps=["Eligible: NBFC-ND only", "Conditions: no commingling of funds, contract on conflicts, no restrictive practices"],
  why="NBFCs are not barred altogether; deposit-taking NBFCs are not the eligible category; and NBFCs-ND come with "
      "conditions.",
  facts=[fact("A bank may engage the following individuals / entities as BCs: ... (7) Non-deposit taking NBFCs "
              "(NBFCs-ND), subject to the following conditions: It shall be ensured that there is no comingling of bank "
              "funds and those of the NBFC-ND appointed as BC; There shall be a specific contractual arrangement ...",
              A_BRANCH)],
  current=ca("2025-11-28"))
Q(T, "PMJDY and allied schemes", "Intermediate",
  "The National Strategy for Financial Inclusion (NSFI) 2025-30 lays down five strategic objectives, the "
  "'Panch-Jyoti'. Which of the following is NOT one of them?",
  ["Opening a bank branch in every village with a population above 2,000",
   "A gender-sensitive approach for women-led financial inclusion",
   "Leveraging financial education as a tool for promoting financial discipline",
   "Strengthening customer protection and grievance redressal measures"],
  concept="NSFI 2025-30",
  explanation="RBI's 1 December 2025 release lists the Panch-Jyoti: an affordable bouquet of financial services for "
              "financial safety and security of households and micro enterprises; a gender-sensitive approach for "
              "women-led inclusion; synergising livelihood and skill ecosystems with inclusion; financial education for "
              "financial discipline; and stronger customer protection and grievance redressal. A branch in every "
              "large village is not one of them.",
  steps=["Check each option against the five listed objectives"],
  why="The other three options are among the listed Panch-Jyoti.",
  facts=[fact("The Panch Jyoti are: ... adopting gender-sensitive approach for women-led financial inclusion ... "
              "leveraging financial education as a tool for promoting financial discipline, and strengthening the "
              "quality and reliability of customer protection and grievance redressal measures", A_NSFI)],
  current=ca("2025-12-01"))
Q(T, "PMJDY and allied schemes", "Intermediate",
  "PMJDY accounts are eligible for several Government schemes. Which of the following is NOT among those listed on "
  "the PMJDY scheme page?",
  ["Pradhan Mantri Fasal Bima Yojana (PMFBY)", "Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)",
   "Pradhan Mantri Suraksha Bima Yojana (PMSBY)", "Atal Pension Yojana (APY)"],
  concept="Schemes linked to PMJDY accounts",
  explanation="The PMJDY scheme page says PMJDY accounts are eligible for Direct Benefit Transfer, PMJJBY, PMSBY, "
              "APY and the MUDRA scheme. PMFBY, a crop insurance scheme, is not listed.",
  steps=["Listed: DBT, PMJJBY, PMSBY, APY, MUDRA", "PMFBY not listed"],
  why="PMJJBY, PMSBY and APY are all named on the page.",
  facts=[fact("PMJDY accounts are eligible for Direct Benefit Transfer (DBT), Pradhan Mantri Jeevan Jyoti Bima Yojana "
              "(PMJJBY), Pradhan Mantri Suraksha Bima Yojana (PMSBY), Atal Pension Yojana (APY), Micro Units "
              "Development & Refinance Agency Bank (MUDRA) scheme", A_PMJDYS)])
_acc15, _acc26, _dep15, _dep26 = 14.72, 59.09, 15670, 316514
assert round(_acc26 / _acc15) == 4 and round(_dep26 / _dep15) == 20
assert round((_dep26 / _acc26) / (_dep15 / _acc15)) == 5
Q(T, "PMJDY and allied schemes", "Advanced",
  "According to the Government's note on 12 years of PMJDY (August 2026), accounts grew from 14.72 crore in 2015 to "
  "59.09 crore as of 19 August 2026, and deposits from ₹15,670 crore in March 2015 to ₹3,16,514 crore. Which statement "
  "is correct?",
  ["Deposits grew about 20 times while accounts grew about 4 times, so deposits per account rose about fivefold",
   "Accounts grew about 20 times while deposits grew about 4 times",
   "Deposits grew about 10 times while accounts grew about 4 times, so deposits per account rose about 2.5 times",
   "Accounts and deposits both grew about 4 times, so deposits per account were unchanged"],
  concept="Growth of PMJDY",
  explanation="Accounts: 59.09 ÷ 14.72 ≈ 4.0 times. Deposits: 3,16,514 ÷ 15,670 ≈ 20.2 times. Deposits per account "
              "therefore rose about 20.2 ÷ 4.0 ≈ 5 times (from about ₹1,065 to about ₹5,357).",
  steps=["Accounts ratio = 59.09/14.72 ≈ 4.0", "Deposits ratio = 3,16,514/15,670 ≈ 20.2",
         "Per-account ratio ≈ 20.2/4.0 ≈ 5"],
  why="The second option reverses the ratios; the third understates deposit growth; the fourth ignores it.",
  facts=[fact("PM-JDY accounts have grown 4x over the last 12 years. Accounts rose from 14.72 crore in 2015 to 59.09 "
              "crore as of 19th August 2026", A_PMJDY12),
         fact("PM-JDY deposits have surged ~20x, rising from ₹15,670 crore in March 2015 to ₹3,16,514 crore as of "
              "19th August 2026", A_PMJDY12)],
  computed=True, current=ca("2026-08-27"))
_cards = 41.29
assert round(100 * _cards / _acc26) == 70 and round(_acc26 - _cards, 1) == 17.8
Q(T, "PMJDY and allied schemes", "Advanced",
  "As of 19 August 2026 there were 59.09 crore PMJDY accounts, and 41.29 crore RuPay debit cards had been issued to "
  "PMJDY account holders. Which statement is correct?",
  ["Cards issued equal about 70% of the accounts, about 17.8 crore fewer than the number of accounts",
   "Cards issued equal about 59% of the accounts, about 24.3 crore fewer than the number of accounts",
   "Cards issued equal about 70% of the accounts, about 41.3 crore fewer than the number of accounts",
   "Cards issued exceed the accounts by about 17.8 crore"],
  concept="RuPay card coverage under PMJDY",
  explanation="41.29 ÷ 59.09 ≈ 0.699, i.e. about 70%. The gap is 59.09 − 41.29 = 17.80 crore.",
  steps=["Share = 41.29/59.09 ≈ 69.9% ≈ 70%", "Gap = 59.09 − 41.29 = 17.8 crore"],
  why="59% and 24.3 crore come from wrong divisions; 41.3 crore is the number of cards, not the gap; cards are fewer, "
      "not more, than accounts.",
  facts=[fact("As of 19th August 2026, 41.29 crore RuPay debit cards have been issued to PM-JDY account holders",
              A_PMJDY12),
         fact("Accounts rose from 14.72 crore in 2015 to 59.09 crore as of 19th August 2026", A_PMJDY12)],
  computed=True, current=ca("2026-08-27"))
Q(T, "Business correspondents", "Advanced",
  "Consider the following statements about Business Correspondents of domestic scheduled commercial banks under RBI's "
  "Commercial Banks – Branch Authorisation Directions, 2025: I. Every BC retail outlet must be within 30 km of its base "
  "Banking Outlet (5 km in metropolitan centres), and only the DCC/SLBC can relax this. II. Interoperability is "
  "permitted at BC retail outlets if transactions are online on the bank's CBS and IBA's standard operating "
  "procedures are followed. III. As the cash handled by BCs is the bank's cash, the bank is responsible for insuring "
  "it. Which of the above is/are correct?",
  ["II and III only", "I and II only", "I, II and III", "I and III only"],
  concept="BC operating rules, 2025 Directions",
  explanation="The 30 km / 5 km distance criterion survives in the text, but RBI has removed the stipulation for "
              "domestic scheduled commercial banks, which decide it in their Board-approved BC policy (I wrong). "
              "Interoperability at BC outlets is allowed if transactions are online, on CBS and per IBA's SOPs (II "
              "right). Cash handled by BCs is the bank's cash, so insuring it is the bank's responsibility (III right).",
  steps=["I: distance criterion removed for domestic SCBs → false", "II: true", "III: true"],
  why="Any option with statement I is wrong, because the distance stipulation no longer binds domestic SCBs.",
  facts=[fact("it has been decided to remove the stipulation regarding distance criteria for domestic scheduled "
              "commercial banks. The bank shall, however, while formulating the Board approved policy for engaging "
              "BCs, keep in mind the objectives of adequate oversight", A_BRANCH),
         fact("interoperability is permitted at the retail outlets or sub-agents of BCs ... provided ... the "
              "transactions and authentications ... are carried out on-line; the transactions are carried out on Core "
              "Banking Solution (CBS) platform; and the bank follows the standard operating procedures advised by the "
              "Indian Banks' Association (IBA)", A_BRANCH),
         fact("As the cash handled by BCs is the bank's cash, the responsibility for insuring this cash shall rest with "
              "the bank", A_BRANCH)],
  current=ca("2025-11-28"))
Q(T, "PMJDY and allied schemes", "Advanced",
  "Consider the following statements about the National Strategy for Financial Inclusion (NSFI) 2025-30: I. It was "
  "approved by the Union Cabinet and released by the Union Finance Minister. II. It was framed under the aegis of "
  "RBI's Technical Group on Financial Inclusion and Financial Literacy (TGFIFL). III. It was approved by the "
  "Sub-Committee of the Financial Stability and Development Council (FSDC-SC) in its 32nd meeting. Which of the above "
  "is/are correct?",
  ["II and III only", "I and II only", "I and III only", "III only"],
  concept="NSFI 2025-30",
  explanation="RBI's release says NSFI 2025-30 was approved by the FSDC Sub-Committee at its 32nd meeting and released "
              "by RBI Governor Sanjay Malhotra on 1 December 2025. It was framed under the aegis of the TGFIFL after "
              "consultations with DEA, DFS, SEBI, IRDAI, PFRDA, NABARD, NSDC and NCFE.",
  steps=["I: false (FSDC-SC approval; released by the RBI Governor)", "II: true", "III: true"],
  why="Statement I is wrong, so options containing it are wrong; 'III only' omits the true statement II.",
  facts=[fact("approved by the Sub-Committee of the Financial Stability and Development Council (FSDC-SC) in its 32nd "
              "meeting, was formally released by Shri Sanjay Malhotra, Governor, RBI on December 01, 2025", A_NSFI),
         fact("The Strategy has been framed under the aegis of Technical Group on Financial Inclusion and Financial "
              "Literacy (TGFIFL)", A_NSFI)],
  current=ca("2025-12-01"))
_inop, _tot = 15.09, 57.07
assert round(100 * _inop / _tot) == 26 and round(_tot - _inop) == 42
Q(T, "PMJDY and allied schemes", "Advanced",
  "In a written Lok Sabha reply in December 2025, the Minister of State for Finance said about 15.09 crore of the 57.07 "
  "crore PMJDY accounts were inoperative. Which statement is correct?",
  ["About 26% of the accounts were inoperative, leaving about 42 crore operative accounts",
   "About 15% of the accounts were inoperative, leaving about 42 crore operative accounts",
   "About 36% of the accounts were inoperative, leaving about 36.5 crore operative accounts",
   "About 26% of the accounts were inoperative, leaving about 15 crore operative accounts"],
  concept="Inoperative PMJDY accounts",
  explanation="15.09 ÷ 57.07 ≈ 0.264, i.e. about 26%. Operative accounts ≈ 57.07 − 15.09 = 41.98 ≈ 42 crore. (An "
              "account is inoperative when there has been no customer-induced transaction for over two years.)",
  steps=["Share = 15.09/57.07 ≈ 26.4%", "Operative = 57.07 − 15.09 ≈ 42 crore"],
  why="15% confuses the crore figure with a percentage; 36% is a miscalculation; 15 crore is the inoperative count, "
      "not the operative one.",
  facts=[fact("there are about 15.09 crore inoperative PMJDY accounts out of the total 57.07 crore PMJDY accounts in "
              "the country, he said in a written reply in the Lok Sabha", A_INOP)],
  computed=True, current=ca("2025-12-08"))
M_SACCR = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13730&Mode=0"                   # opened 2026-11-06
# ---- sources (group B): all opened (fetched and read) on 2026-11-06 unless listed in SEARCH_ONLY
B_P = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid="
B_N = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id="
B_MPF = "https://www.rbi.org.in/Scripts/FS_Overview.aspx?fn=2752"            # monetary policy framework page
B_RATES = "https://www.rbi.org.in/commonman/english/history/Scripts/BankrateCRRandSLRChanges.aspx"
B_GSEC = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id=79"              # G-sec primer FAQ
B_CPI = "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc2026212787501.pdf"
B_OCT18 = B_P + "45152"           # MPC resolution 5 Oct 2018
B_MPC_DEC25 = B_P + "61749"
B_GOV_DEC25 = B_P + "61750"
B_MPC_FEB26 = B_P + "62169"
B_GOV_FEB26 = B_P + "62170"
B_MPC_APR26 = B_P + "62514"
B_GOV_APR26 = B_P + "62515"
B_MPC_JUN26 = B_P + "62863"
B_GOV_JUN26 = B_P + "62864"
B_VRR_JUN8 = B_P + "62882"
B_MPC_AUG26 = B_P + "63287"
B_GOV_AUG26 = B_P + "63288"
B_VRRR_AUG28 = B_P + "63467"
B_VRRR_AUG31 = B_P + "63470"
B_VRR90_A = B_P + "62129"
B_VRR90_B = B_P + "62131"
B_WMA_ST = B_P + "63689"
B_MPC_OCT26 = B_P + "63742"
B_GOV_OCT26 = B_P + "63744"
B_FORTNIGHT = B_N + "13224&Mode=0"   # CRR/SLR amendment directions, Dec 2025 (fortnight redefined)
B_INVIT = B_N + "13707&Mode=0"
B_MALDIVES = B_N + "13712&Mode=0"
B_SHARES = B_N + "13719&Mode=0"
B_FORMA2 = B_N + "13724&Mode=0"
B_SLF_PD = B_N + "13726&Mode=0"
B_LAF_OCT = B_N + "13727&Mode=0"
B_DELHI = B_N + "13746&Mode=0"
B_HOME = "https://www.rbi.org.in/"                                  # current rates panel
B_C91 = "https://rbi.org.in/history/Brief_Chro1991to2000.html"
B_HIKE23 = "https://www.angelone.in/news/economy/rbi-increases-repo-rate-to-5-50-first-hike-since-february-2023"
SEARCH_ONLY.update({B_HIKE23})

# ================= Monetary Policy (Basic 4 / Intermediate 4 / Advanced 3)
T = "Monetary Policy"
Q(T, "MPC structure", "Basic",
  "Who is the Chairperson of the Monetary Policy Committee constituted under Section 45ZB of the RBI Act, 1934?",
  ["The Governor of RBI, ex officio", "The Deputy Governor in charge of monetary policy",
   "The Union Finance Secretary", "A Government-appointed external member chosen by rotation"],
  concept="Composition of the MPC",
  explanation="The six-member MPC is chaired ex officio by the RBI Governor. The Deputy Governor in charge of "
              "monetary policy and one RBI officer nominated by the Central Board are the other ex officio "
              "members; three members are appointed by the Central Government.",
  steps=["MPC = 3 RBI members + 3 Government-appointed members", "Chairperson = Governor (ex officio)"],
  why="The Deputy Governor is a member, not the chair; the Finance Secretary is not a member; the chair does not "
      "rotate among external members.",
  facts=[fact("Governor of the Reserve Bank of India—Chairperson, ex officio; Deputy Governor of the Reserve Bank "
              "of India, in charge of Monetary Policy—Member, ex officio", B_MPF)])
Q(T, "MPC structure", "Basic",
  "Which department of the Reserve Bank assists the Monetary Policy Committee in formulating monetary policy?",
  ["Monetary Policy Department (MPD)", "Financial Markets Operations Department (FMOD)",
   "Department of Regulation (DoR)", "Department of Economic and Policy Research (DEPR)"],
  concept="Monetary policy process",
  explanation="RBI's framework page states that the Reserve Bank's Monetary Policy Department assists the MPC in "
              "formulating monetary policy, drawing on surveys, staff projections and stakeholder views.",
  steps=["MPC decides the repo rate", "MPD provides analytical support and projections"],
  why="FMOD conducts market operations such as LAF auctions; DoR frames banking regulation; DEPR does research "
      "but is not named as assisting the MPC.",
  facts=[fact("The Reserve Bank's Monetary Policy Department (MPD) assists the MPC in formulating the monetary "
              "policy", B_MPF)])
Q(T, "Transmission", "Basic",
  "In his statement of 5 December 2025, the RBI Governor noted in passing that RBI had moved away from targeting "
  "money supply. In which year did this happen?",
  ["1998", "1985", "2014", "2016"],
  concept="Evolution of the monetary policy framework",
  explanation="RBI followed monetary targeting (money supply as the intermediate target) from the mid-1980s and "
              "moved away from it in 1998 to a multiple-indicator approach, before adopting flexible inflation "
              "targeting in 2016. The Governor's December 2025 statement recalls this while stressing that the "
              "policy repo rate is the primary instrument.",
  steps=["Monetary targeting: from the mid-1980s", "Dropped in 1998", "FIT formalised in 2016"],
  why="1985 is around when monetary targeting began; 2014 is the Urjit Patel Committee report; 2016 is when the "
      "MPC and FIT got statutory backing.",
  current=ca("2025-12-05"),
  facts=[fact("We moved away from targeting money supply in 1998 (footnote to the statement that the primary "
              "instrument of monetary policy is the policy repo rate)", B_GOV_DEC25)])
Q(T, "MPC structure", "Basic",
  "From which date did the Reserve Bank of India Monetary Policy Committee and Monetary Policy Process "
  "Regulations, 2016 come into effect?",
  ["1 August 2016", "29 September 2016", "20 February 2015", "1 April 2017"],
  concept="Legal framework of the MPC",
  explanation="RBI notified the MPC and Monetary Policy Process Regulations, 2016, effective 1 August 2016. They "
              "lay down the meeting schedule, notice periods, the resolution and the publication of minutes. The "
              "MPC itself was constituted later, on 29 September 2016.",
  steps=["Regulations in force: 1 August 2016", "First MPC constituted: 29 September 2016"],
  why="29 September 2016 is when the first MPC was constituted; 20 February 2015 is the Monetary Policy "
      "Framework Agreement; 1 April 2017 has no such link.",
  facts=[fact("The Reserve Bank has notified Reserve Bank of India Monetary Policy Committee and Monetary Policy "
              "Process Regulations, 2016 which came into effect from August 01, 2016", B_MPF)])

Q(T, "MPC structure", "Intermediate",
  "RBI publishes a Monetary Policy Report (MPR) once every six months. Which of the following is NOT among the "
  "elements the MPR must contain?",
  ["The Government's fiscal deficit target for the next financial year",
   "Projections of inflation and growth and the balance of risks",
   "An assessment of projection performance",
   "An updated review of the operating procedure of monetary policy"],
  concept="Monetary Policy Report",
  explanation="The MPR explains inflation dynamics over the last six months and the near-term outlook, gives "
              "inflation and growth projections with the balance of risks, assesses the state of the economy "
              "(including the fiscal situation), reviews the operating procedure and assesses projection "
              "performance. Setting the fiscal deficit target is the Government's job, not part of the MPR.",
  steps=["List the five MPR elements", "Fiscal targets are set in the Union Budget, not the MPR"],
  why="Projections with risks, projection-performance assessment and the operating-procedure review are all listed "
      "MPR elements.",
  facts=[fact("Once in every six months, the Reserve Bank publishes the Monetary Policy Report containing ... "
              "projections of inflation and growth and the balance of risks; ... an updated review of the operating "
              "procedure of monetary policy; and an assessment of projection performance", B_MPF)])
Q(T, "Policy stance", "Intermediate",
  "At its meeting of February 2026, the MPC did not give growth and inflation projections for the full year "
  "2026-27, only for Q1 and Q2. Why?",
  ["Full-year projections were to be set out in April 2026 after incorporating the new GDP and CPI series due "
   "for release that month",
   "The Union Budget had not yet been presented, so fiscal numbers were unknown",
   "The MPC had changed its stance and stopped publishing annual projections",
   "The West Asia conflict had made all projections beyond one quarter impossible"],
  concept="Projections and data revisions",
  explanation="The Governor's February 2026 statement said full-year 2026-27 projections would be set out in the "
              "April 2026 policy after incorporating the new GDP and CPI series, released on 27 February and 12 "
              "February 2026. The resolution added that the MPC would be guided by data from the new series.",
  steps=["New CPI released 12 February 2026; new GDP 27 February 2026", "Full-year numbers deferred to April"],
  why="The Budget was presented on 1 February, before the meeting; the stance stayed neutral; the West Asia "
      "conflict escalated only later (March 2026).",
  current=ca("2026-02-06"),
  facts=[fact("Projections for full year 2026-27 will be set out in the Monetary Policy Statement to be announced "
              "in April 2026 after incorporating the new GDP and CPI series ... to be released on February 27 and "
              "February 12, 2026, respectively", B_GOV_FEB26),
         fact("Going forward, the MPC will be guided by the evolving macroeconomic conditions and the outlook based "
              "on data from the new series", B_MPC_FEB26)])
Q(T, "Policy stance", "Intermediate",
  "At its 60th meeting (6–8 April 2026), held soon after the conflict in West Asia began, how did the MPC "
  "characterise the shock to the economy and what did it decide?",
  ["A supply shock; it kept the repo rate unchanged and continued with the neutral stance, preferring to wait "
   "and watch",
   "A demand shock; it raised the repo rate by 25 bps and changed the stance to calibrated tightening",
   "A supply shock; it cut the repo rate by 25 bps to cushion growth",
   "A financial shock; it kept the rate unchanged but changed the stance to accommodative"],
  concept="Policy response to supply shocks",
  explanation="The April 2026 resolution said the economy was confronted with a supply shock and that it was "
              "prudent to wait and watch the evolving growth-inflation outlook; the MPC unanimously kept the repo "
              "rate at 5.25% and continued with the neutral stance, retaining flexibility.",
  steps=["Nature of shock: supply (energy, supply chains)", "Decision: hold at 5.25%, neutral stance"],
  why="The rate hike and calibrated tightening came only in October 2026; there was no cut or move to "
      "accommodative in April 2026.",
  current=ca("2026-04-08"),
  facts=[fact("The economy is confronted with a supply shock. It is prudent to wait and watch the changing "
              "circumstances ... the MPC voted to keep the policy rate unchanged ... The MPC also decided to "
              "continue with the neutral stance", B_MPC_APR26)])
Q(T, "Transmission", "Intermediate",
  "In its data on transmission to lending rates, RBI reports an 'interest rate effect' on the weighted average "
  "lending rate (WALR) separately from the total change. How is the interest rate effect calculated?",
  ["By keeping the weights (loan composition) constant, as of January 2025",
   "By excluding all loans linked to external benchmarks",
   "By counting only loans to the government and public sector undertakings",
   "By deducting the change in the repo rate from the change in WALR"],
  concept="Measuring monetary transmission",
  explanation="WALR can change because rates on each loan category change (interest rate effect) or because the "
              "mix of loans shifts (composition effect). RBI isolates the interest rate effect by holding the "
              "weights constant as of January 2025; e.g. in December 2025 the fresh-loan WALR fell 69 bps, but the "
              "interest rate effect was 78 bps.",
  steps=["Total WALR change = interest rate effect + composition effect", "Interest rate effect: fixed weights "
         "(January 2025)"],
  why="The other options describe no RBI method; subtracting the repo change gives the gap in transmission, not "
      "the interest rate effect.",
  current=ca("2025-12-05"),
  facts=[fact("Interest rate effect on transmission to weighted average lending rate (WALR) is calculated by "
              "keeping the weight constant (as of January 2025)", B_GOV_DEC25)])

Q(T, "Policy stance", "Advanced",
  "The MPC adopted the stance of 'calibrated tightening' in October 2026. It had used this stance once before, "
  "in October 2018. Consider:\n"
  "I. In October 2018 the repo rate was kept unchanged at 6.50%, whereas in October 2026 it was raised.\n"
  "II. In October 2018 one member voted for a 25 bps increase in the repo rate.\n"
  "III. On both occasions the change of stance was decided unanimously.\n"
  "Which is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Policy stance across cycles",
  explanation="On 5 October 2018 the MPC kept the repo rate at 6.5%; Dr. Chetan Ghate voted for a 25 bps "
              "increase, and Dr. Ravindra H. Dholakia voted to keep the neutral stance. In October 2026 the repo "
              "rate was raised unanimously to 5.50%, but two members (Dr. Nagesh Kumar and Prof. Ram Singh) "
              "preferred a neutral stance. So the stance change was not unanimous either time (III wrong).",
  steps=["2018: hold at 6.50%; Ghate for a hike; Dholakia against the stance change",
         "2026: unanimous hike; two members against the stance change", "I and II true, III false"],
  why="'I only' omits II; III is false on both occasions.",
  current=ca("2026-10-07"),
  facts=[fact("keep the policy repo rate ... unchanged at 6.5 per cent ... Dr. Chetan Ghate voted for an increase "
              "in the policy rate by 25 bps ... Dr. Ravindra H. Dholakia voted to keep the neutral stance unchanged",
              B_OCT18),
         fact("the MPC voted unanimously to increase the policy repo rate ... by 25 bps to 5.50 per cent ... Two "
              "members - Dr. Nagesh Kumar and Prof. Ram Singh - were of the view that the stance be retained at "
              "neutral", B_MPC_OCT26)])

apr = {"wf": -83, "wo": -89, "df": -85, "do": -50}   # Feb 2025-Apr 2026 (bps)
jun = {"wf": -80, "wo": -91, "df": -63, "do": -51}   # Feb 2025-Jun 2026 (bps)
chg = {k: jun[k] - apr[k] for k in apr}
assert chg == {"wf": 3, "wo": -2, "df": 22, "do": -1}
Q(T, "Transmission", "Advanced",
  "RBI reported the cumulative change since February 2025 in banks' rates as follows. Up to April 2026: WALR on "
  "fresh loans −83 bps, on outstanding loans −89 bps; WADTDR on fresh deposits −85 bps, on outstanding deposits "
  "−50 bps. Up to June 2026: WALR fresh −80, outstanding −91; WADTDR fresh −63, outstanding −51. What happened "
  "during May–June 2026?",
  ["Fresh deposit rates rose by about 22 bps and fresh lending rates by about 3 bps, while rates on outstanding "
   "loans eased by about 2 bps",
   "Fresh lending rates fell by a further 3 bps and fresh deposit rates fell by 22 bps",
   "All four rates rose, led by outstanding deposit rates",
   "Fresh deposit rates rose by about 22 bps, but fresh lending rates fell by about 3 bps"],
  concept="Reading transmission data",
  explanation="Change in May–June = (cumulative to June) − (cumulative to April). WALR fresh: −80 − (−83) = +3; "
              "WALR outstanding: −91 − (−89) = −2; WADTDR fresh: −63 − (−85) = +22; WADTDR outstanding: "
              "−51 − (−50) = −1. This matches the Governor's remark that transmission moderated with hardening of "
              "deposit and lending rates as credit demand stayed strong.",
  steps=["Fresh WALR +3", "Outstanding WALR −2", "Fresh WADTDR +22", "Outstanding WADTDR −1"],
  why="Fresh lending rates rose, not fell; outstanding rates eased slightly, so not all four rose.",
  computed=True, current=ca("2026-08-05"),
  facts=[fact("WALR ... declined by 83 bps for fresh rupee loans and 89 bps for outstanding loans during February "
              "2025 - April 2026 ... WADTDR on fresh deposits declined by 85 bps, while that on outstanding "
              "deposits softened by 50 bps", B_GOV_JUN26),
         fact("WALR ... declined by 80 bps for fresh rupee loans, and 91 bps for outstanding rupee loans during "
              "February 2025 to June 2026 ... WADTDR on fresh deposits has declined by 63 bps while that on "
              "outstanding deposits has softened by 51 bps", B_GOV_AUG26)])

q2 = {"Dec 2025": 6.8, "Feb 2026": 7.0, "Apr 2026": 6.7, "Jun 2026": 6.3, "Aug 2026": 6.4, "Oct 2026": 7.2}
assert max(q2, key=q2.get) == "Oct 2026" and min(q2, key=q2.get) == "Jun 2026"
assert round(q2["Oct 2026"] - q2["Jun 2026"], 1) == 0.9
Q(T, "Policy stance", "Advanced",
  "The MPC's projection of real GDP growth for Q2 (July–September) 2026-27 was 6.8% in December 2025, 7.0% in "
  "February 2026, 6.7% in April, 6.3% in June, 6.4% in August and 7.2% in October 2026. Which statement is "
  "correct?",
  ["The projection was lowest in June and highest in October, a range of 0.9 percentage point",
   "The projection was cut at every meeting from February to October 2026",
   "The October projection was 0.2 percentage point below the February projection",
   "The projection was lowest in April and highest in February, a range of 0.3 percentage point"],
  concept="Evolution of MPC projections",
  explanation="Lowest: 6.3% (June 2026, as the West Asia conflict hit); highest: 7.2% (October 2026, after strong "
              "Q1 data). Range = 7.2 − 6.3 = 0.9 pp. The projection rose in August and October, and October was "
              "0.2 pp above February.",
  steps=["Min 6.3 (June), max 7.2 (October)", "7.2 − 6.3 = 0.9"],
  why="It was raised in August and October; October (7.2) is above February (7.0); April (6.7) was not the low.",
  computed=True, current=ca("2026-10-07"),
  facts=[fact("Real GDP growth for Q1:2026-27 is projected at 6.7 per cent and Q2 at 6.8 per cent", B_MPC_DEC25),
         fact("real GDP growth projections for Q1:2026-27 and Q2 are revised upwards to 6.9 per cent and 7.0 per "
              "cent, respectively", B_MPC_FEB26),
         fact("Q1 at 6.8 per cent; Q2 at 6.7 per cent; Q3 at 7.0 per cent", B_MPC_APR26),
         fact("Q1 at 6.6 per cent; Q2 at 6.3 per cent; Q3 at 6.5 per cent", B_MPC_JUN26),
         fact("Q1 at 7.0 per cent; Q2 at 6.4 per cent; Q3 at 6.5 per cent", B_MPC_AUG26),
         fact("real GDP growth for 2026-27 is projected at 7.1 per cent, with Q2 at 7.2 per cent", B_MPC_OCT26)])

# ================= Repo Rate (Basic 2 / Intermediate 3 / Advanced 2) — all current
T = "Repo Rate"
SUB = "Repo and policy corridor"
Q(T, SUB, "Basic",
  "After the MPC decision of 7 October 2026, at what rate is RBI's Standing Liquidity Facility (collateralised "
  "liquidity support) available to Primary Dealers?",
  ["5.50%, the revised repo rate", "5.25%, the SDF rate", "5.75%, the MSF rate", "6.00%, repo plus 50 bps"],
  concept="Facilities linked to the repo rate",
  explanation="RBI's circular to Primary Dealers of 7 October 2026 said that, after the repo rate was raised from "
              "5.25% to 5.50%, the Standing Liquidity Facility to PDs would be available at the revised repo rate "
              "of 5.50% with immediate effect.",
  steps=["SLF to PDs is priced at the repo rate", "Repo after 7 October 2026 = 5.50%"],
  why="5.25% is the SDF (floor), 5.75% the MSF/Bank Rate; 6.00% has no basis.",
  current=ca("2026-10-07"),
  facts=[fact("the Standing Liquidity Facility provided to Primary Dealers (PDs) (collateralised liquidity support) "
              "from the Reserve Bank would be available at the revised repo rate of 5.50 per cent with immediate "
              "effect", B_SLF_PD)])
Q(T, SUB, "Basic",
  "The MPC raised the policy repo rate to 5.50% on 7 October 2026. This was RBI's first repo rate increase since:",
  ["February 2023", "May 2022", "June 2025", "December 2025"],
  concept="Rate cycles",
  explanation="The last tightening cycle ended with a 25 bps hike to 6.50% in February 2023. The rate was then "
              "held, cut from February 2025 to December 2025 (to 5.25%), held again, and raised in October 2026.",
  steps=["Last hike: February 2023 (to 6.50%)", "Easing: February–December 2025", "Next hike: October 2026"],
  why="May 2022 began the earlier hiking cycle; June 2025 and December 2025 were cuts.",
  current=ca("2026-10-07"),
  facts=[fact("RBI increases repo rate to 5.50%, first hike since February 2023", B_HIKE23)])

Q(T, SUB, "Intermediate",
  "To add durable liquidity in January–February 2026, RBI used OMO purchases and forex swaps and also conducted "
  "repo operations of an unusually long tenor (₹25,000 crore and a second operation of ₹1,11,500 crore). What was "
  "their tenor?",
  ["90 days", "14 days", "7 days", "One year"],
  concept="Variable rate repo operations",
  explanation="Normally RBI manages transient liquidity through VRR/VRRR operations of overnight to 14 days. In "
              "January–February 2026 it also ran two 90-day VRR operations, alongside ₹1,00,000 crore of OMO "
              "purchases and USD 10 billion of long-term buy/sell swaps.",
  steps=["Usual VRR tenor: overnight to 14 days", "Jan–Feb 2026: two 90-day VRRs"],
  why="7 and 14 days are the usual main-operation tenors; one-year repos were not used.",
  current=ca("2026-02-06"),
  facts=[fact("additional OMO purchase auctions amounting to ₹1,00,000 crore, long term forex buy/sell swaps of USD "
              "10 billion, 90-day VRR operation of ₹25,000 crore and a second 90-day VRR operation of ₹1,11,500 "
              "crore for January and February 2026", B_GOV_FEB26)])
Q(T, SUB, "Intermediate",
  "According to the MPC's resolution of 7 October 2026, which major central bank had raised its policy rate by 25 "
  "bps in September 2026, shortly before RBI raised the repo rate?",
  ["The US Federal Reserve", "The European Central Bank", "The Bank of Japan", "The People's Bank of China"],
  concept="Global context of the repo rate hike",
  explanation="The resolution noted that rising inflation in key economies had prompted a hawkish shift: the US Fed "
              "hiked by 25 bps in September 2026, and further tightening by major central banks reinforced "
              "expectations of higher global policy rates.",
  steps=["Global shift towards tightening", "Named example: US Fed, +25 bps in September 2026"],
  why="The resolution names only the US Fed's September hike.",
  current=ca("2026-10-07"),
  facts=[fact("Acceleration of inflation in key economies has prompted a shift towards hawkish monetary policy. The "
              "US Fed hiked by 25 bps in September", B_MPC_OCT26)])
Q(T, SUB, "Intermediate",
  "In August 2026 the MPC kept the repo rate at 5.25% with a neutral stance. What did its resolution say any "
  "future policy action would also have to consider?",
  ["The need to recalibrate policy rates as underlying inflation normalises from its benign levels",
   "The need to cut rates to offset the weak monsoon",
   "The Government's request to lower borrowing costs",
   "A shift of the inflation target to the WPI"],
  concept="Forward signals before a rate change",
  explanation="The August 2026 resolution said greater clarity on inflation was needed before acting, and that "
              "any action would have to consider the need for recalibration of policy rates in line with the "
              "growth-inflation dynamics, especially the normalisation of underlying inflation. The repo rate was "
              "raised at the next meeting, in October 2026.",
  steps=["August: hold, neutral", "Signal: recalibration as underlying inflation normalises", "October: hike"],
  why="No cut was signalled; the MPC does not act on Government requests; the target remains CPI-based.",
  current=ca("2026-08-05"),
  facts=[fact("Any such action would also have to consider the need for recalibration of policy rates in line with "
              "the evolving growth-inflation dynamics, especially the normalisation of the underlying inflation from "
              "its benign levels seen hitherto", B_MPC_AUG26)])

notified, bids, rate, days = 75000, 23680, 5.26, 4
share = 100 * bids / notified
interest = bids * rate / 100 * days / 365
assert round(share, 1) == 31.6 and round(interest, 2) == 13.65
Q(T, SUB, "Advanced",
  "On 8 June 2026 (repo rate 5.25%), RBI held a 4-day Variable Rate Repo (VRR) auction with a notified amount of "
  "₹75,000 crore. Bids of ₹23,680 crore were received and all were allotted at a cut-off (and weighted average) "
  "rate of 5.26%. Which statement is correct? (Use a 365-day year.)",
  ["Only about 31.6% of the notified amount was taken up, at 1 bp above the repo rate; interest payable to RBI "
   "was about ₹13.65 crore",
   "The auction was oversubscribed about 3.2 times and allotment was pro rata",
   "About 31.6% was taken up, at 1 bp below the repo rate; interest payable to RBI was about ₹13.65 crore",
   "About 68.4% of the notified amount was taken up; interest payable to RBI was about ₹47.4 crore"],
  concept="Variable rate repo auctions",
  explanation="Take-up = 23,680 ÷ 75,000 = 31.6%. In a VRR, banks borrow from RBI and bid rates at or above the "
              "repo rate; the cut-off of 5.26% is 1 bp above 5.25%. Interest = 23,680 × 5.26% × 4/365 ≈ ₹13.65 "
              "crore. Low take-up showed banks' borrowing need was well below what RBI offered.",
  steps=["23,680/75,000 = 31.6%", "5.26 − 5.25 = +1 bp", "23,680 × 0.0526 × 4/365 ≈ 13.65"],
  why="Bids were below the notified amount (not oversubscribed); 5.26% is above, not below, the repo rate; 68.4% "
      "is the untaken share.",
  computed=True, current=ca("2026-06-08"),
  facts=[fact("4-day Variable Rate Repo (VRR) auction ... Notified Amount (in ₹ crore) 75,000; Total amount of bids "
              "received (in ₹ crore) 23,680; Amount allotted (in ₹ crore) 23,680; Cut off Rate (%) 5.26; Weighted "
              "Average Rate (%) 5.26", B_VRR_JUN8),
         fact("the MPC voted unanimously to keep the policy repo rate ... unchanged at 5.25 per cent",
              B_MPC_JUN26)])

cover = 95062 / 25000
assert round(cover, 1) == 3.8 and round(5.40 - 5.34, 2) == 0.06 and round(5.40 - 5.25, 2) == 0.15
Q(T, SUB, "Advanced",
  "On 30 January 2026 (repo rate 5.25%), RBI held a long-tenor Variable Rate Repo auction with a notified amount of "
  "₹25,000 crore. Bids of ₹95,062 crore were received; ₹25,004 crore was allotted at a cut-off rate of 5.34% and a "
  "weighted average rate of 5.40%, with 38.37% partial allotment of bids at the cut-off rate. Which statement is "
  "correct?",
  ["Bids were about 3.8 times the notified amount; successful bidders paid their own (higher) bid rates, averaging "
   "6 bps above the cut-off and 15 bps above the repo rate, and bids at the cut-off got only part of what they sought",
   "Bids were about 3.8 times the notified amount, and every successful bidder paid the uniform cut-off rate of "
   "5.34%",
   "The auction was undersubscribed, so all bids were accepted in full at the repo rate",
   "Bids were about 3.8 times the notified amount; successful bidders paid on average 6 bps below the cut-off rate"],
  concept="Reading a variable rate repo auction result",
  explanation="Cover = 95,062 ÷ 25,000 ≈ 3.8 times. In a VRR, banks borrow and bid rates; RBI accepts the highest "
              "bids down to the cut-off (5.34%), the lowest accepted rate. Because the weighted average rate (5.40%) "
              "exceeds the cut-off, allotments were priced at the bidders' own rates (multiple price), not one "
              "uniform rate: 5.40 − 5.34 = 6 bps above cut-off; 5.40 − 5.25 = 15 bps above repo. Bids exactly at "
              "the cut-off were scaled down (38.37% allotment) to keep the total near the notified amount. The "
              "heavy demand led RBI to hold a second 90-day VRR (notified ₹2,00,000 crore) the same day.",
  steps=["95,062/25,000 ≈ 3.8x", "Weighted average 5.40 > cut-off 5.34 → bid-rate (multiple) pricing",
         "5.40 − 5.25 = 15 bps over repo", "Bids at cut-off: 38.37% partial allotment"],
  why="A uniform price would make the weighted average equal the cut-off; the auction was oversubscribed; in a repo "
      "auction accepted bids are at or above the cut-off, so the average cannot be below it.",
  computed=True, current=ca("2026-01-30"),
  facts=[fact("Result of the 90-day Variable Rate Repo (VRR) auction held on January 30, 2026 ... Notified Amount "
              "25,000; Total amount of bids received 95,062; Amount allotted 25,004; Cut off Rate (%) 5.34; Weighted "
              "Average Rate (%) 5.40; Partial Allotment Percentage of bids received at cut off rate (%) 38.37",
              B_VRR90_A),
         fact("RBI to conduct Second 90-day Variable Rate Repo (VRR) auction ... Notified Amount 2,00,000 ... January "
              "30, 2026", B_VRR90_B),
         fact("the MPC voted unanimously to keep the policy repo rate under the liquidity adjustment facility (LAF) "
              "unchanged at 5.25 per cent", B_MPC_FEB26)])

# ================= Reverse Repo Rate (Basic 1 / Intermediate 1 / Advanced 1)
T = "Reverse Repo Rate"
SUB = "Reverse repo and SDF"
Q(T, SUB, "Basic",
  "On 31 August 2026, with system liquidity in large surplus, RBI conducted a 15-day Variable Rate Reverse Repo "
  "(VRRR) auction with a notified amount of ₹6,00,000 crore. What does such an operation do?",
  ["It absorbs surplus funds from banks for 15 days, with the funds returning on reversal (15 September 2026)",
   "It injects liquidity into banks for 15 days against government securities",
   "It permanently withdraws liquidity by selling government securities outright",
   "It lends to banks at the MSF rate for 15 days"],
  concept="VRRR as an absorption tool",
  explanation="In a reverse repo RBI borrows from banks (absorbing liquidity). A 15-day VRRR is a term operation: "
              "funds placed on 31 August 2026 were to come back to banks on the reversal date, 15 September 2026.",
  steps=["Reverse repo = RBI absorbs funds", "Tenor 15 days; reversal 15 September 2026"],
  why="Injection is done through repo (VRR); outright sales are OMOs; the MSF is a borrowing window for banks.",
  current=ca("2026-08-31"),
  facts=[fact("Variable Rate Reverse Repo (VRRR) auction on Monday, August 31, 2026 ... Notified Amount 6,00,000 ... "
              "Tenor 15 ... Date of Reversal September 15, 2026", B_VRRR_AUG28)])
Q(T, SUB, "Intermediate",
  "In August 2026 the repo rate was 5.25% and the SDF rate 5.00%. A bank with surplus funds could place them in "
  "RBI's VRRR auctions (cut-off rates such as 5.24%) or in the SDF. Why did VRRR auctions attract offers at all?",
  ["The VRRR cut-off rate (such as 5.24%) was above the SDF rate of 5.00%, so it paid banks more than the SDF",
   "VRRR deposits count towards the CRR, while SDF balances do not",
   "The SDF window was closed on the days VRRR auctions were held",
   "VRRR deposits earn the MSF rate if held for more than a week"],
  concept="Where VRRR rates sit in the corridor",
  explanation="In a VRRR, banks offer funds at rates they quote and RBI accepts offers up to a cut-off rate. Any "
              "rate above the SDF floor (5.00%) beats parking money in the SDF, so a 5.24% cut-off (15-day VRRR of "
              "31 August 2026) was attractive. The SDF remains the floor of the corridor.",
  steps=["Corridor: SDF 5.00% – repo 5.25% – MSF 5.50%", "VRRR cut-off 5.24% > SDF 5.00%"],
  why="Neither VRRR nor SDF balances count for CRR; the SDF is available daily; VRRR never pays the MSF rate.",
  current=ca("2026-08-31"),
  facts=[fact("Result of the 15-day Variable Rate Reverse Repo (VRRR) auction held on August 31, 2026 ... Cut off "
              "Rate (%) 5.24", B_VRRR_AUG31),
         fact("the standing deposit facility (SDF) rate remains at 5.00 per cent and the marginal standing facility "
              "(MSF) rate and the Bank Rate remain at 5.50 per cent", B_MPC_AUG26),
         fact("The SDF rate is placed at 25 basis points below the policy repo rate. With introduction of SDF in "
              "April 2022, the SDF rate replaced the fixed reverse repo rate as the floor of the LAF corridor",
              B_MPF)])
take = 100 * 134625 / 600000
assert round(take, 1) == 22.4 and 5.00 < 5.24 < 5.25
Q(T, SUB, "Advanced",
  "Consider the following about RBI's 15-day VRRR auction of 31 August 2026 (notified ₹6,00,000 crore; offers "
  "₹1,34,625 crore, all accepted at 5.24%; repo rate 5.25%, SDF 5.00%):\n"
  "I. Offers covered only about 22% of the notified amount.\n"
  "II. The rate RBI paid lay inside the LAF corridor, just below the repo rate.\n"
  "III. Unlike the SDF, a reverse repo is a collateralised operation in which RBI provides eligible government "
  "securities.\n"
  "Which is/are correct?",
  ["I, II and III", "I and II only", "II and III only", "I and III only"],
  concept="Reverse repo vs SDF",
  explanation="I: 1,34,625 ÷ 6,00,000 = 22.4%. II: 5.24% is between the SDF floor (5.00%) and the repo rate "
              "(5.25%). III: RBI defines the reverse repo as absorbing liquidity against the collateral of eligible "
              "G-secs, while the SDF accepts uncollateralised deposits. All three are correct.",
  steps=["134,625/600,000 = 22.4%", "5.00 < 5.24 < 5.25", "Reverse repo collateralised; SDF not"],
  why="Each of the other options leaves out a correct statement.",
  computed=True, current=ca("2026-08-31"),
  facts=[fact("Notified Amount (in ₹ crore) 6,00,000; Total amount of offers received (in ₹ crore) 1,34,625; Amount "
              "accepted (in ₹ crore) 1,34,625; Cut off Rate (%) 5.24", B_VRRR_AUG31),
         fact("Reverse Repo Rate: The interest rate at which the Reserve Bank absorbs liquidity from banks against "
              "the collateral of eligible government securities under the LAF; SDF Rate: The rate at which the "
              "Reserve Bank accepts uncollateralised deposits", B_MPF)])

# ================= CRR (Basic 1 / Intermediate 1 / Advanced 1)
T = "CRR"
Q(T, "CRR concept", "Basic",
  "Following the Banking Laws (Amendment) Act, 2025, how is a 'fortnight' now defined for banks' maintenance of "
  "CRR and SLR (effective 15 December 2025)?",
  ["1st to 15th, and 16th to the last day, of each calendar month",
   "Saturday to the second following Friday, both days inclusive",
   "Monday to the second following Sunday",
   "Any 14 consecutive days chosen by the bank"],
  concept="Reserve maintenance period",
  explanation="The old definition (Saturday to the second following Friday) was replaced. A fortnight is now the "
              "1st–15th or the 16th–last day of each calendar month, both days inclusive; Friday-based reporting "
              "references were changed to the last day of the fortnight.",
  steps=["Old: Saturday to second Friday", "New: 1–15 and 16–month end"],
  why="The Saturday–Friday cycle is the old definition; the other two never applied.",
  current=ca("2025-12-15"),
  facts=[fact("the definition of 'Fortnight' has been amended from \"the period from Saturday to the second "
              "following Friday, both days inclusive\" to \"the period from the first day to the fifteenth day of "
              "each calendar month or sixteenth day to the last day of each calendar month, both days inclusive\" "
              "... the enactment date of the stated definition of fortnight is December 15, 2025", B_FORTNIGHT)])
Q(T, "CRR concept", "Intermediate",
  "Under RBI's amended directions issued after the Banking Laws (Amendment) Act, 2025, how do scheduled "
  "commercial banks now report their CRR position?",
  ["A single fortnightly Form A return, filed electronically on RBI's CIMS portal; there is no provisional or "
   "final Form A",
   "A provisional Form A within 7 days and a final Form A within 20 days of the fortnight",
   "A monthly Form VIII filed in hard copy",
   "A weekly Form A submitted through the bank's sponsor bank"],
  concept="CRR reporting",
  explanation="RBI said that under the new reporting structure there would be no provisional, final or special "
              "Form A. Banks submit a single fortnightly Form A (from 15 December 2025) and a monthly Form VIII "
              "(SLR) on the CIMS portal, digitally signed by two authorised officials, not on paper.",
  steps=["Form A = CRR, fortnightly, single return", "Form VIII = SLR, monthly", "Both on CIMS, no hard copy"],
  why="Provisional/final returns were abolished; Form VIII is the SLR return and is not filed on paper; there is "
      "no weekly return via sponsor banks.",
  current=ca("2025-12-15"),
  facts=[fact("there shall be no Provisional or Final or Special Form A return. The banks are required to submit "
              "single Form A return ... fortnightly Form A return from December 15, 2025 and monthly Form VIII return "
              "from December 2025 on the CIMS portal ... not to be submitted in hard copy", B_FORTNIGHT)])
ndtl = 2_40_000
req = ndtl * 3 / 100
assert req == 7200
Q(T, "CRR value", "Advanced",
  "Under the amended rules, CRR for a fortnight is maintained on the NDTL as on the last day of the second "
  "preceding fortnight. For the fortnight 16–31 March 2026, a bank's NDTL on the relevant date was ₹2,40,000 crore. "
  "With CRR at 3%, on which date's NDTL is the requirement based, and what average balance must it keep?",
  ["28 February 2026; ₹7,200 crore", "15 March 2026; ₹7,200 crore", "15 February 2026; ₹7,200 crore",
   "28 February 2026; ₹9,600 crore"],
  concept="Applying the new fortnight definition",
  explanation="Fortnight 16–31 March. Preceding fortnight: 1–15 March. Second preceding: 16–28 February 2026, whose "
              "last day is 28 February 2026. Requirement = 3% × 2,40,000 = ₹7,200 crore (average daily balance, "
              "subject to the daily minimum).",
  steps=["Preceding: 1–15 Mar", "Second preceding: 16–28 Feb → 28 Feb 2026", "0.03 × 2,40,000 = 7,200"],
  why="15 March ends the immediately preceding fortnight; 15 February is three fortnights back; ₹9,600 crore uses "
      "the old 4% CRR.",
  computed=True, current=ca("2025-12-15"),
  facts=[fact("From the subsequent fortnights starting from January 16, 2026, the maintenance shall be done, as "
              "presently applicable, i.e., based on the NDTL as on the last day of the second preceding fortnight",
              B_FORTNIGHT),
         fact("Cash Reserve Ratio (CRR): The average daily balance that a bank is required to maintain with the "
              "Reserve Bank as a per cent of its net demand and time liabilities (NDTL)", B_MPF)])

# ================= SLR (Basic 2 / Intermediate 1 / Advanced 2)
T = "SLR"
Q(T, "SLR value", "Basic",
  "According to RBI's table of reserve requirement changes, the SLR, which had been 38.5% in the early 1990s, was "
  "brought down in phases to what level with effect from 25 October 1997?",
  ["25%", "31.5%", "20%", "18%"],
  concept="SLR reduction after the 1991 reforms",
  explanation="Following the Narasimham Committee's call for a phased reduction of pre-emptions, the SLR was "
              "lowered from its 38.5% peak in steps (to 31.5% by October 1994) and reached 25% from 25 October 1997.",
  steps=["Peak 38.5% (1990)", "31.5% (October 1994)", "25% (25 October 1997)"],
  why="31.5% was the October 1994 level; 20% was the 1949 level; 18% is today's SLR.",
  facts=[fact("Statutory Liquidity Ratio: 31.5 (29-10-1994); 25 (25-10-1997)", B_RATES),
         fact("Nov 1991: The Narsimahmam Committee Report suggested ... a phased reduction in the SLR and CRR", B_C91)])
Q(T, "SLR concept", "Basic",
  "How are District Central Co-operative Banks (DCCBs) allowed to meet their SLR requirement, according to RBI's "
  "G-sec FAQ?",
  ["By maintaining cash balances with their respective State Co-operative Bank",
   "By holding term deposits with any public sector bank",
   "By holding shares of the State Co-operative Bank",
   "Only by holding Treasury Bills with RBI"],
  concept="SLR for rural co-operative banks",
  explanation="State Co-operative Banks and DCCBs maintain SLR in cash, gold or unencumbered approved securities "
              "under Section 24 of the BR Act; DCCBs are specifically allowed to meet their SLR by keeping cash "
              "balances with their State Co-operative Bank.",
  steps=["Section 24 BR Act applies to StCBs and DCCBs", "DCCBs: cash balances with the StCB count"],
  why="PSB term deposits are not SLR assets (they were excluded even for UCBs from 2015); shares are not SLR "
      "assets; T-bills are allowed but not the only route.",
  facts=[fact("DCCBs are allowed to meet their SLR requirement by maintaining cash balances with their respective "
              "State Co-operative Bank", B_GSEC)])
Q(T, "SLR concept", "Intermediate",
  "For primary (urban) co-operative banks, which of the following stopped being reckoned for SLR with effect from "
  "1 April 2015?",
  ["Balances with State/District Central Co-operative Banks and term deposits with public sector banks",
   "Unencumbered investments in Central Government securities",
   "Cash in hand and gold",
   "State Development Loans"],
  concept="Eligible SLR assets for UCBs",
  explanation="Under Section 24(2A) of the BR Act (as applicable to co-operative societies), UCBs keep SLR in "
              "cash, gold or unencumbered approved securities, up to 40% of DTL as RBI specifies. Balances with "
              "StCBs/DCCBs and term deposits with PSBs ceased to count from 1 April 2015, pushing UCBs to hold "
              "G-secs.",
  steps=["Eligible: cash, gold, unencumbered approved securities", "Excluded from 1 April 2015: co-op bank "
         "balances and PSB term deposits"],
  why="G-secs, cash, gold and SDLs remain eligible SLR assets.",
  facts=[fact("balances kept with State Co-operative Banks / District Central Co-operative Banks as also term "
              "deposits with public sector banks are now not eligible for being reckoned for SLR purpose w.e.f "
              "April 1, 2015", B_GSEC)])
Q(T, "SLR concept", "Advanced",
  "Consider the following statements from RBI's G-sec FAQ on the SLR of co-operative and regional rural banks:\n"
  "I. A primary (urban) co-operative bank's SLR can be specified at not more than 40% of its DTL.\n"
  "II. Regional Rural Banks may keep part of their SLR as deposits with their sponsor bank.\n"
  "III. Since April 2002, RRBs must hold their entire SLR in Government and other approved securities.\n"
  "Which is/are correct?",
  ["I and III only", "I and II only", "II and III only", "III only"],
  concept="SLR across bank types",
  explanation="I is correct: Section 24(2A) caps the UCB SLR at 40% of DTL. III is correct: since April 2002 RRBs "
              "hold their entire SLR in Government and other approved securities, so II (deposits with the sponsor "
              "bank) is wrong.",
  steps=["I: 40% ceiling – true", "III: RRBs entirely in securities since April 2002 – true", "II contradicts III"],
  why="Any option with II is wrong; 'III only' omits I.",
  facts=[fact("every primary (urban) cooperative bank shall maintain liquid assets ... not exceeding 40% of its DTL",
              B_GSEC),
         fact("Since April 2002, all the RRBs are required to maintain their entire Statutory Liquidity Ratio (SLR) "
              "holdings in Government and other approved securities", B_GSEC)])
peak, y97, now = 38.5, 25.0, 18.0
cut97 = 100 * (peak - y97) / peak
assert round(cut97, 1) == 35.1 and round(100 * (peak - now) / peak, 1) == 53.2
Q(T, "SLR value", "Advanced",
  "The SLR was 38.5% of NDTL from September 1990, 25% from October 1997 and is 18% today. Which statement is "
  "correct?",
  ["The 1990–97 reduction cut the requirement by about 35%; the current level is about 53% below the 1990 peak",
   "The 1990–97 reduction cut the requirement by about 13.5%; the current level is about 20.5% below the peak",
   "The 1990–97 reduction cut the requirement by about 54%; the current level is about 35% below the peak",
   "The 1990–97 reduction cut the requirement by about 25%; the current level is about 46.8% below the peak"],
  concept="Relative change in a reserve ratio",
  explanation="1990→1997: (38.5 − 25) ÷ 38.5 = 35.1% lower (13.5 percentage points). Peak→now: (38.5 − 18) ÷ 38.5 "
              "= 53.2% lower (20.5 percentage points). Percentage-point and percentage changes must not be "
              "confused.",
  steps=["13.5/38.5 = 35.1%", "20.5/38.5 = 53.2%"],
  why="13.5% and 20.5% are percentage-point changes, not percentages; the other options swap or misstate the "
      "figures.",
  computed=True,
  facts=[fact("Statutory Liquidity Ratio: 38.5 (22-09-1990); 25 (25-10-1997)", B_RATES),
         fact("Current rates: CRR 3.00%; SLR 18.00%", B_HOME)])

# ================= Bank Rate (Intermediate 2 / Advanced 1)
T = "Bank Rate"
SUB = "Bank rate and MSF"
Q(T, SUB, "Intermediate",
  "RBI's table of Bank Rate changes shows the rate rising in steps from 3.5% (1951) to 12% (1991). Between November "
  "1951 and October 1991, when was the Bank Rate reduced, the only cut in that period?",
  ["2 March 1968, from 6% to 5%", "9 January 1971, from 6% to 5%", "23 July 1974, from 9% to 7%",
   "26 September 1964, from 5% to 4.5%"],
  concept="History of the Bank Rate",
  explanation="The table lists 3.5% (1951), 4% (1957), 4.5% (1963), 5% (1964), 6% (1965), 5% (2 March 1968), "
              "6% (1971), 7% (1973), 9% (1974), 10% (1981), 11% and 12% (1991). The 1968 move is the only "
              "reduction.",
  steps=["Read the sequence 1951–1991", "Only fall: 6% (1965) → 5% (2 March 1968)"],
  why="In January 1971 the rate was raised from 5% to 6%; in July 1974 raised from 7% to 9%; in September 1964 "
      "raised from 4.5% to 5%.",
  facts=[fact("Bank Rate: 6 (17-02-1965); 5 (2/3/1968); 6 (9/1/1971); 7 (31-05-1973); 9 (23-07-1974)", B_RATES)])
Q(T, SUB, "Intermediate",
  "According to RBI's table of rate changes, what did RBI do to the Bank Rate in July 2000?",
  ["Raised it from 7% to 8% (22 July 2000), and raised CRR soon after",
   "Cut it from 8% to 7%, and cut CRR to 8%",
   "Raised it from 8% to 9%, leaving CRR unchanged",
   "Kept it at 7% but raised SLR to 25%"],
  concept="Bank Rate as a signalling rate",
  explanation="After cutting the Bank Rate to 7% on 2 April 2000, RBI raised it to 8% on 22 July 2000 and raised "
              "the CRR from 8% to 8.25% (29 July 2000) and 8.5% (12 August 2000), before resuming cuts in 2001.",
  steps=["2 April 2000: 7%", "22 July 2000: 8%", "CRR 8.25% (29 July), 8.5% (12 August)"],
  why="The 7%-to-8% move was a hike, not a cut; the rate did not go to 9% in 2000; SLR was not raised.",
  facts=[fact("Bank Rate: 7 (2/4/2000); 8 (22-07-2000); CRR: 8 (22-04-2000); 8.25 (29-07-2000); 8.5 (12/8/2000)",
              B_RATES)])
Q(T, SUB, "Advanced",
  "Consider the following about RBI's response to pressure on the rupee during the Asian crisis, as recorded in "
  "RBI's table of rate changes:\n"
  "I. On 17 January 1998 the Bank Rate was raised by 200 bps to 11% and the CRR to 10.5%.\n"
  "II. The Bank Rate increase was fully reversed by 29 April 1998, in three cuts.\n"
  "III. The CRR was brought back to 10% on 11 April 1998.\n"
  "Which is/are correct?",
  ["I, II and III", "I and II only", "I and III only", "II only"],
  concept="Bank Rate in a currency defence",
  explanation="Table: Bank Rate 9% (22 Oct 1997) → 11% (17 Jan 1998) → 10.5% (19 Mar) → 10% (3 Apr) → 9% (29 Apr "
              "1998): +200 bps then three cuts back to 9%. CRR 10% → 10.5% (17 Jan 1998) → 10.25% (28 Mar) → 10% "
              "(11 Apr 1998). All three statements are correct.",
  steps=["11 − 9 = +200 bps", "Cuts: 10.5, 10, 9 → reversed by 29 April", "CRR back to 10% on 11 April 1998"],
  why="Each other option leaves out a correct statement.",
  facts=[fact("Bank Rate: 9 (22-10-1997); 11 (17-01-1998); 10.5 (19-03-1998); 10 (3/4/1998); 9 (29-04-1998); CRR: "
              "10 (6/12/1997); 10.5 (17-01-1998); 10.25 (28-03-1998); 10 (11/4/1998)", B_RATES),
         fact("28 Nov 1997: A series of measures introduced in response to the Asian Currency Crisis", B_C91)])

# ================= Inflation (Basic 1 / Intermediate 2 / Advanced 2)
T = "Inflation"
Q(T, "CPI and WPI", "Basic",
  "How many weighted items does the all-India basket of the new Consumer Price Index (base 2024=100) contain?",
  ["358", "299", "448", "260"],
  concept="New CPI series",
  explanation="MoSPI's first release of CPI (2024=100), on 12 February 2026, says the weighted items rose from 299 "
              "to 358: goods from 259 to 308 and services from 40 to 50.",
  steps=["Old CPI (2012): 299 items", "New CPI (2024): 358 items (308 goods + 50 services)"],
  why="299 was the old basket; 448 and 260 are not CPI basket sizes.",
  current=ca("2026-02-12"),
  facts=[fact("At the all-India level, the number of weighted items has increased from 299 to 358 in CPI 2024 ... "
              "Goods items are increased from 259 to 308; Services items are increased from 40 to 50", B_CPI)])
Q(T, "CPI and WPI", "Intermediate",
  "Which of the following is a first-time addition in the new CPI series (base 2024=100)?",
  ["Rural house rent, to cover rural housing", "Urban house rent", "Prices of cereals sold through the PDS",
   "Prices collected from rural markets"],
  concept="Coverage of the new CPI",
  explanation="The new series includes rural house rent for the first time; the 2012 series covered housing only "
              "for urban areas. It also adds e-commerce prices in 12 large towns and online sources for airfares "
              "and OTT subscriptions.",
  steps=["2012 series: housing index urban only", "2024 series: rural house rent added"],
  why="Urban rent and rural market prices were already part of the CPI; PDS prices are not a new addition.",
  current=ca("2026-02-12"),
  facts=[fact("First-time inclusion of rural house rent for improving coverage of rural housing consumption",
              B_CPI)])
Q(T, "Inflation targeting", "Intermediate",
  "According to the RBI Governor's statement of 5 December 2025, what happened for the first time since the "
  "adoption of flexible inflation targeting?",
  ["Average headline inflation for a quarter (1.7% in Q2:2025-26) fell below the lower tolerance threshold of 2%",
   "Average headline inflation for a quarter rose above the upper tolerance threshold of 6%",
   "CPI inflation turned negative for a full quarter",
   "Core inflation fell below 1% for a full year"],
  concept="Tolerance band of the inflation target",
  explanation="The Governor said Q2:2025-26 average headline inflation of 1.7% breached the 2% lower threshold of "
              "the 4% target, the first time this had happened; inflation then dipped to 0.3% in October 2025. "
              "(Breaches of the upper 6% band had occurred before, e.g. in 2022.)",
  steps=["Target 4%, band 2–6%", "Q2:2025-26 average 1.7% < 2%: first lower-band breach"],
  why="Upper-band breaches had happened earlier; inflation stayed positive; core inflation was over 4% then.",
  current=ca("2025-12-05"),
  facts=[fact("For the first time since the adoption of flexible inflation targeting (FIT), average headline "
              "inflation for a quarter at 1.7 per cent in Q2:2025-26, breached the lower tolerance threshold (2 per "
              "cent) of the inflation target (4 per cent). It dipped further to a mere 0.3 per cent in October 2025",
              B_GOV_DEC25)])
Q(T, "CPI and WPI", "Advanced",
  "Consider the following statements about the CPI with base 2024=100 released by MoSPI:\n"
  "I. Its weights come from HCES 2023-24, while base-period prices were collected from January to December 2024.\n"
  "II. Food and beverages still have the largest weight, although it fell to 36.75% from 45.86%.\n"
  "III. E-commerce prices are collected from online markets in every district of the country.\n"
  "Which is/are correct?",
  ["I and II only", "II only", "I and III only", "I, II and III"],
  concept="Design of the new CPI",
  explanation="I and II are stated in MoSPI's release. III is wrong: e-commerce prices were added as an extra market "
              "only in 12 large towns with population above 25 lakh; physical market collection remains the "
              "backbone.",
  steps=["I true (weight vs price reference periods)", "II true (36.75%, still the largest)",
         "III false (12 large towns only)"],
  why="'II only' omits I; options with III are wrong.",
  current=ca("2026-02-12"),
  facts=[fact("In CPI 2024, expenditure weights are derived from HCES 2023–24, while base-period prices were "
              "collected during January 2024 to December 2024", B_CPI),
         fact("Share of Food & Beverages is declined in the new series, however, it continues to remain the largest "
              "component of the CPI basket (weights: CPI 2012 45.86%; CPI 2024 36.75)", B_CPI),
         fact("E-commerce prices introduced as an additional market in 12 large towns (population exceeding 25 "
              "lakhs)", B_CPI)])
q3 = round((0.3 + 0.7 + 1.3) / 3, 2)
q4 = round((2.7 + 3.2 + 3.4) / 3, 2)
assert q3 == 0.77 and q4 == 3.1
Q(T, "Inflation targeting", "Advanced",
  "Failure to meet the inflation target means average CPI inflation below 2% (or above 6%) for any three "
  "consecutive quarters. RBI reported: Q2:2025-26 average 1.7% (the first quarter ever below 2%); monthly "
  "inflation of 0.3% (October), 0.7% (November) and 1.3% (December 2025); and 2.7% (January), 3.2% (February) and "
  "3.4% (March 2026). Was there a failure?",
  ["No; Q2 and Q3 averaged below 2% (Q3 about 0.8%), but Q4 averaged about 3.1%, so there were only two "
   "consecutive quarters",
   "Yes; Q1, Q2 and Q3 of 2025-26 all averaged below 2%",
   "Yes; Q2, Q3 and Q4 of 2025-26 all averaged below 2%",
   "No; because the lower band applies only if inflation turns negative"],
  concept="Failure criteria under the RBI Act",
  explanation="Q3 average = (0.3 + 0.7 + 1.3) ÷ 3 ≈ 0.77%; Q4 = (2.7 + 3.2 + 3.4) ÷ 3 = 3.1%. Q1:2025-26 was "
              "above 2% (Q2 was the first breach ever). So only Q2 and Q3 were below 2% – two quarters, not "
              "three. The CPI series changed base from January 2026, but every reading of Q4 is above 2%.",
  steps=["Q2 = 1.7 (<2)", "Q3 ≈ 0.77 (<2)", "Q4 = 3.1 (>2)", "Q1 > 2 (Q2 was the first breach)"],
  why="Q1 was not below 2%; Q4 was above 2%; the lower threshold is 2%, not zero.",
  computed=True, current=ca("2026-06-05"),
  facts=[fact("Failure ... (b) the average inflation is less than the lower tolerance level for any three "
              "consecutive quarters", B_MPF),
         fact("For the first time since the adoption of flexible inflation targeting (FIT), average headline "
              "inflation for a quarter at 1.7 per cent in Q2:2025-26 ... breached the lower tolerance threshold ... "
              "It dipped further to a mere 0.3 per cent in October 2025", B_GOV_DEC25),
         fact("Headline CPI inflation remained low at 0.7 per cent in November and 1.3 per cent in December, 2025",
              B_MPC_FEB26),
         fact("headline inflation increased to 3.2 per cent in February 2026 from 2.7 per cent in January",
              B_MPC_APR26),
         fact("Headline CPI inflation inched up to 3.4 per cent in March and 3.5 per cent in April 2026",
              B_MPC_JUN26)])

# ================= Money Market (Basic 1 / Intermediate 4 / Advanced 1)
T = "Money Market"
SUB = "Instruments: T-bills, CP, CD, call money"
Q(T, SUB, "Basic",
  "Which day count convention is followed in India's money market, including for Treasury Bills?",
  ["Actual/365", "30/360", "Actual/360", "Actual/actual"],
  concept="Day count conventions",
  explanation="RBI's G-sec FAQ states that the money market uses actual/365 (actual days in the numerator, 365 in "
              "the year), and T-bills follow it; the bond market uses 30/360.",
  steps=["Money market (T-bills, CP, CD): actual/365", "Dated G-secs: 30/360"],
  why="30/360 is the Indian bond-market convention; actual/360 and actual/actual are used elsewhere.",
  facts=[fact("Money market: The day count convention followed is actual/365 ... Hence, in the case of T-Bills, "
              "which are essentially money market instruments, money market convention is followed", B_GSEC)])
Q(T, SUB, "Intermediate",
  "In February 2026 the RBI Governor explained why rates on commercial papers (CPs) and certificates of deposit "
  "(CDs) tightened in January 2026. Which reasons did he give?",
  ["Moderation in surplus liquidity, excess supply from bunched CP/CD redemptions, and year-end seasonal effects",
   "A repo rate hike in January 2026 and higher CRR",
   "A ban on mutual funds investing in CPs and CDs",
   "Large OMO sales by RBI and a cut in the WMA limit"],
  concept="Drivers of money market rates",
  explanation="The Governor cited (i) moderation in surplus liquidity, (ii) excess supply from bunching of CP and CD "
              "redemptions in January and (iii) year-end seasonal effects. RBI was in fact injecting durable "
              "liquidity then through OMO purchases and swaps.",
  steps=["Liquidity surplus shrank", "Bunched redemptions → heavy fresh issuance", "Year-end effects"],
  why="There was no repo hike or CRR increase then; no such MF ban; RBI was buying, not selling, G-secs.",
  current=ca("2026-02-06"),
  facts=[fact("Money market rates, especially for commercial papers (CPs) and certificates of deposit (CDs), "
              "tightened in January 2026 reflecting (i) moderation in surplus liquidity; (ii) excess supply from "
              "bunching of redemptions in CPs and CDs in January; and (iii) year-end seasonal effects",
              B_GOV_FEB26)])
cp, cd, tb = 6.99 - 7.45, 6.75 - 7.16, 5.34 - 5.32
assert round(cp * 100) == -46 and round(cd * 100) == -41 and round(tb * 100) == 2
Q(T, SUB, "Intermediate",
  "The June 2026 Governor's statement gave average rates since the April policy (3-month T-bill 5.34%, 3-month CD "
  "6.75%, 3-month CP 6.99%) and between the February and April policies (5.32%, 7.16% and 7.45%). Which statement "
  "is correct?",
  ["CP rates eased the most (about 46 bps), CD rates about 41 bps, while the T-bill rate rose 2 bps",
   "CD rates eased the most (about 46 bps), while CP rates eased 41 bps",
   "All three rates eased, the T-bill rate by 2 bps",
   "CP rates rose about 46 bps as liquidity tightened"],
  concept="Comparing money market rates",
  explanation="CP: 6.99 − 7.45 = −46 bps; CD: 6.75 − 7.16 = −41 bps; T-bill: 5.34 − 5.32 = +2 bps. Private "
              "paper (CP, CD) eased markedly while the sovereign T-bill rate was almost flat.",
  steps=["CP −46", "CD −41", "T-bill +2"],
  why="CD fell 41 (not 46); the T-bill rate rose; CP rates fell, not rose.",
  computed=True, current=ca("2026-06-05"),
  facts=[fact("The rates on 3-month treasury bill, 3-month certificates of deposit and 3-month commercial paper "
              "averaged 5.34 per cent, 6.75 per cent and 6.99 per cent, respectively, since April policy as "
              "compared to 5.32 per cent, 7.16 per cent and 7.45 per cent, respectively, between February and April "
              "policy", B_GOV_JUN26)])
Q(T, SUB, "Intermediate",
  "Under RBI's rules described in its G-sec FAQ, which entities may re-repo government securities (including SDLs "
  "and T-bills) that they acquired under reverse repo?",
  ["Scheduled commercial banks, primary dealers, and mutual funds and insurance companies (with their regulators' "
   "approval) holding SGL accounts with RBI",
   "Only RBI, as part of the LAF",
   "Only scheduled commercial banks, and only overnight",
   "Any individual investor holding a gilt account"],
  concept="Repo and re-repo in the money market",
  explanation="A repo is borrowing by selling securities with an agreement to repurchase; a reverse repo is the "
              "lending side. Re-repo lets the lender use securities received in a reverse repo for its own repo. "
              "SCBs, PDs, and MFs and insurers (subject to their regulators' approval) maintaining SGL accounts "
              "with RBI may re-repo G-secs, including SDLs and T-bills.",
  steps=["Reverse repo: lend cash, receive securities", "Re-repo: repo those securities onward",
         "Eligible: SCBs, PDs, MFs, insurers with SGL accounts"],
  why="Re-repo is a market facility, not an RBI-only one; it is not restricted to SCBs; individuals are not "
      "eligible.",
  facts=[fact("Scheduled commercial banks, Primary Dealers along with Mutual Funds and Insurance Companies (subject "
              "to the approval of the regulators concerned) maintaining Subsidiary General Ledger account with RBI "
              "are permitted to re-repo the government securities, including SDLs and Treasury Bills, acquired "
              "under reverse repo", B_GSEC)])
dec = {"WACR": 110, "T-bill": 113, "NBFC CP": 124, "CD": 140}
assert all(v > 100 for v in dec.values()) and max(dec, key=dec.get) == "CD"
Q(T, SUB, "Intermediate",
  "In December 2025 the Governor reported how money market rates had responded to the cumulative 100 bps repo cut "
  "of the easing cycle (up to 3 December 2025): WACR −110 bps, 3-month T-bill −113 bps, 3-month NBFC CP −124 bps "
  "and 3-month CD −140 bps. What does this show?",
  ["Transmission to the money market was more than full: every rate fell by more than the repo cut, CDs the most",
   "Transmission was weak: no money market rate fell as much as the repo rate",
   "Only the call rate fell by more than the repo cut",
   "CP rates fell the most, while CD rates fell less than the repo cut"],
  concept="Transmission to the money market",
  explanation="All four rates fell by more than 100 bps (comfortable liquidity added to the rate cuts); the 3-month "
              "CD rate fell the most (140 bps).",
  steps=["Compare each fall with 100 bps", "All > 100; maximum = CD (140)"],
  why="All rates fell more than 100 bps, so the 'weak' and 'only the call rate' options are wrong; CD (not CP) "
      "fell the most.",
  computed=True, current=ca("2025-12-05"),
  facts=[fact("In response to the cumulative policy repo rate cut of 100 bps in the current easing cycle (up to "
              "December 03), the WACR, the 3-month T-bill rate, the rate on 3-month CPs issued by NBFCs, and the "
              "3-month CD rate declined by 110 bps, 113 bps, 124 bps, and 140 bps, respectively", B_GOV_DEC25)])
cum = {"T-bill": -119 + 6, "NBFC CP": -143 + 73, "CD": -127 + 84}
assert cum == {"T-bill": -113, "NBFC CP": -70, "CD": -43}
Q(T, SUB, "Advanced",
  "The February 2026 Governor's statement said that, after the cumulative 125 bps repo cut, the 3-month T-bill, "
  "3-month NBFC CP and 3-month CD rates had fallen by 119, 143 and 127 bps up to end-December 2025, but then "
  "hardened by 6, 73 and 84 bps respectively between 1 January and 4 February 2026. What was the net decline in "
  "each by 4 February 2026?",
  ["T-bill 113 bps, CP 70 bps, CD 43 bps – all now below the 125 bps repo cut",
   "T-bill 125 bps, CP 216 bps, CD 211 bps",
   "T-bill 113 bps, CP 70 bps, CD 43 bps – only the CD rate below the repo cut",
   "T-bill 106 bps, CP 57 bps, CD 41 bps – all below the repo cut"],
  concept="Net transmission after a reversal",
  explanation="Net decline = earlier fall − later rise: T-bill 119 − 6 = 113; CP 143 − 73 = 70; CD 127 − 84 = 43. "
              "All three are now below 125 bps, though before January the CP and CD rates had fallen by more than "
              "the repo cut.",
  steps=["119 − 6 = 113", "143 − 73 = 70", "127 − 84 = 43", "All < 125"],
  why="Adding the rises double-counts; the T-bill and CP declines are also below 125; the last option miscalculates.",
  computed=True, current=ca("2026-02-06"),
  facts=[fact("the WACR, the 3-month T-bill rate, the 3-month CP issued by NBFCs, and the 3-month CD rate declined "
              "by 89 bps, 119 bps, 143 bps, and 127 bps, respectively up to end-December, 2025. However, since the "
              "beginning of January and up to February 4, 2026, the 3-month T-bill rate, the 3-month CP issued by "
              "NBFCs, and the 3-month CD rate have hardened by 6 bps, 73 bps and 84 bps, respectively",
              B_GOV_FEB26)])

# ================= RBI Circulars and Regulatory Updates (Basic 3 / Intermediate 1 / Advanced 1)
T = "RBI Circulars and Regulatory Updates"
SUB = "Recent RBI directions"
# ================= RBI Circulars and Regulatory Updates (1 Basic)
Q("RBI Circulars and Regulatory Updates", "Recent RBI directions", "Basic",
  "RBI's amendment directions of 7 October 2026 revise the methodology for minimum capital requirements for "
  "counterparty credit risk from 1 April 2027. To which commercial banks do they apply mandatorily?",
  ["Banks with an international presence or with derivatives outstanding (book value) of ₹25,000 crore and above",
   "Only the Domestic Systemically Important Banks (D-SIBs)",
   "All commercial banks, including small finance banks and payments banks",
   "Only foreign banks operating in India through branches"],
  concept="Scope of the revised counterparty credit risk framework",
  explanation="The Commercial Banks – Forthcoming Instructions Amendment Directions, 2026 (7 October 2026), effective 1 "
              "April 2027, apply to commercial banks with an international presence or with book value of derivatives "
              "outstanding of ₹25,000 crore and above on a consolidated group-wide basis. The remaining commercial banks "
              "may choose either the Current Exposure Method (CEM) or the Standardised Approach for Counterparty Credit "
              "Risk (SA-CCR).",
  steps=["Mandatory: international presence, or derivatives book ≥ ₹25,000 crore",
         "Others: choose CEM or SA-CCR"],
  why="The scope is not defined by D-SIB status or by foreign ownership, and other banks are given a choice rather "
      "than being covered mandatorily.",
  current=ca("2026-10-07"),
  facts=[fact("These Amendment Directions shall come into effect from April 1, 2027; shall be applicable to commercial "
              "banks with an international presence or with book value of derivative outstanding of ₹ 25,000 crore and "
              "above as on the reporting date, on a consolidated group wide basis. However, remaining commercial banks "
              "may choose to adopt either the Current Exposure Method (CEM) or the Standardised Approach for "
              "Counterparty Credit Risk (SA-CCR)", M_SACCR)])
Q(T, SUB, "Basic",
  "RBI's circular of 23 September 2026 notified a Government of India-supported Line of Credit extended by Exim "
  "Bank to which country, for ₹4,850 crore?",
  ["Maldives", "Sri Lanka", "Mauritius", "Bangladesh"],
  concept="Exim Bank Lines of Credit",
  explanation="Exim Bank's ₹4,850 crore GOI-supported LoC to the Government of the Republic of Maldives finances "
              "development projects; at least 75% of the contract value must be supplied from India. The agreement "
              "is effective from 27 August 2026.",
  steps=["LoC: ₹4,850 crore to the Maldives", "Indian content ≥ 75%"],
  why="The circular concerns only the Maldives.",
  current=ca("2026-09-23"),
  facts=[fact("Exim Bank's GOI-supported Line of Credit (LOC) for ₹ 4,850 crores the Government of Maldives, for "
              "financing various developmental projects in Maldives ... goods, works and services of the value of at "
              "least 75% of the contract price ... shall be supplied by the Seller from India", B_MALDIVES)])
Q(T, SUB, "Basic",
  "By a circular of 1 October 2026 on online submission of Form A2 for outward remittances, what did RBI change "
  "for Authorised Dealers' internal guidelines?",
  ["They may be approved by the Board or by a Board Committee/Management Committee to which the Board has "
   "delegated powers",
   "They must now be approved by RBI before use",
   "They can be framed only for remittances up to USD 25,000 a year",
   "They now need approval of the Foreign Exchange Dealers' Association of India"],
  concept="Forex remittance procedure",
  explanation="Earlier (July 2024 circular) ADs had to frame internal guidelines for Form A2-based remittances with "
              "Board approval. The October 2026 circular allows approval by the Board or any Board Committee or "
              "Management Committee with delegated powers; other instructions remain unchanged.",
  steps=["Before: Board approval only", "Now: Board or delegated committee"],
  why="No RBI pre-approval or FEDAI approval is required; the circular adds no amount ceiling.",
  current=ca("2026-10-01"),
  facts=[fact("Authorised Dealers shall frame appropriate internal guidelines with the approval of their Board or "
              "any Board Committee / Management Committee to which powers have been delegated by the Board",
              B_FORMA2)])
Q(T, SUB, "Intermediate",
  "Under RBI's amendment of 22 September 2026 to the commercial banks' investment portfolio directions, how must a "
  "bank value units of an unlisted InvIT or REIT that fails to compute and disclose its NAV as required by SEBI?",
  ["At ₹1 per unit", "At face value", "At the last traded price on any exchange", "At cost less 50%"],
  concept="Valuation of investments",
  explanation="Unquoted InvIT and REIT units are valued at the NAV the trust discloses. If the trust fails to compute "
              "and disclose NAV in the manner and frequency SEBI specifies, or the units are infrequently traded, "
              "they are valued at ₹1 – a conservative rule.",
  steps=["Normally: disclosed NAV", "NAV not disclosed: ₹1 per unit"],
  why="Face value, last traded price and cost-based haircuts are not the prescribed treatment.",
  current=ca("2026-09-22"),
  facts=[fact("Units: The valuation shall be done at the NAV as disclosed by the InvIT. Where an InvIT fails to "
              "compute and disclose the NAV in the manner and frequency specified under SEBI (Infrastructure "
              "Investment Trusts) Regulations, 2014, the value of its units shall be treated as ₹1", B_INVIT)])
Q(T, SUB, "Advanced",
  "RBI's amendment directions of 1 October 2026 on acquisition of shares in banks introduced a one-time approval "
  "for 'qualifying persons'. Consider:\n"
  "I. Qualifying persons are SEBI-registered mutual funds, PFRDA-registered pension funds and IRDAI-registered "
  "insurers that do not belong to the bank's promoter group or group.\n"
  "II. The one-time approval covers subsequent acquisitions of major shareholding up to 10% of the bank's paid-up "
  "capital or voting rights, on an aggregate basis.\n"
  "III. With the one-time approval, prior approval is no longer needed even for the initial acquisition of major "
  "shareholding.\n"
  "Which is/are correct?",
  ["I and II only", "II only", "II and III only", "I, II and III"],
  concept="Ownership regulation of banks",
  explanation="I and II follow the amendment's definitions and proviso. III is wrong: RBI said prior approval stays "
              "mandatory for the initial acquisition of major shareholding; the relief is only for subsequent "
              "acquisitions after a holding has fallen below 5%. Applications go through PRAVAAH.",
  steps=["I: definition of qualifying person", "II: up to 10%, aggregate basis", "III: initial acquisition still "
         "needs prior approval"],
  why="'II only' omits I; options with III are wrong.",
  current=ca("2026-10-01"),
  facts=[fact("While obtaining prior approval shall continue to be mandatory for initial acquisition of major "
              "shareholding in a banking company ... decided to grant one-time approval for subsequent acquisitions "
              "of major shareholding in the same banking company by mutual funds, insurance companies and pension "
              "funds", B_SHARES),
         fact("'qualifying person' ... is a mutual fund registered with the Securities and Exchange Board of India, "
              "or a pension fund registered with the Pension Fund Regulatory and Development Authority, or an "
              "insurance company registered with the Insurance Regulatory and Development Authority of India; and "
              "... does not belong to the promoter group or group of the investee banking company ... one-time "
              "approval ... for subsequent acquisitions of major shareholding up to 10 per cent of the paid-up "
              "share capital or voting rights", B_SHARES)])
M_UPIOCT = ("https://www.outlookmoney.com/banking/upi-average-daily-transaction-value-crosses-rs-1-lakh-crore-for-"
            "first-time-ever-in-october")                                                           # opened 2026-11-06
# ---- sources (group C)
C_F = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id="
C_IRAC = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13146"   # opened 2026-11-06 (updated 1 Oct 2026)
C_ARC = C_F + "179"                                                            # opened 2026-11-06 (ARC FAQs, Sep 2026)
C_IBBI = "https://ibbi.gov.in/about"                                           # opened 2026-11-06
C_BCBS = "https://www.bis.org/bcbs/history.htm"                                # opened 2026-11-06
C_LCR25 = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12836"     # opened 2026-11-06
C_PSL = C_F + "87"                                                             # opened 2026-11-06
C_RBIOS = C_F + "153"                                                          # opened 2026-11-06
C_ERUPEE = C_F + "169"                                                         # opened 2026-11-06
C_DL25 = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12848"      # opened 2026-11-06
C_TOKEN = C_F + "129"                                                          # opened 2026-11-06
C_PAYNOW = C_F + "156"                                                         # opened 2026-11-06
C_NEFT = C_F + "60"                                                            # opened 2026-11-06
C_INRF = C_F + "67"                                                            # opened 2026-11-06 (INRF FAQs, Sep 2023)
C_CHQ = C_F + "175"                                                            # opened 2026-11-06 (cheque clearing FAQs, Jan 2026)
C_BOOKLET = "https://www.rbi.org.in/scripts/PublicationsView.aspx?Id=20315"   # opened 2026-11-06
C_UPILITE = ("https://www.businesstoday.in/personal-finance/banking/story/upi-rule-changes-increased-limits-for-upi-"
             "lite-transactions-wallets-check-key-changes-456364-2024-12-05")   # opened 2026-11-06

# ================= NPA (Basic 3 / Intermediate 4 / Advanced 1)
T = "NPA"
Q(T, "Classification", "Basic",
  "Under RBI's income recognition and asset classification norms, advances against certain instruments need not be "
  "treated as NPAs if adequate margin is available. Advances against which of the following are NOT covered by this "
  "exemption?",
  ["Gold ornaments", "Term deposits", "Kisan Vikas Patras", "Life insurance policies"],
  concept="Advances against specific securities",
  explanation="RBI's IRAC Directions, 2025 exempt advances against term deposits, NSCs eligible for surrender, KVPs and "
              "life insurance policies from NPA treatment as long as adequate margin is available. Advances against "
              "gold ornaments, government securities and all other securities are expressly not covered.",
  steps=["Exempt (with adequate margin): term deposits, NSCs, KVPs, life insurance policies",
         "Not exempt: gold ornaments, government securities, other securities"],
  why="Term deposits, KVPs and life insurance policies are all in the exempted list.",
  facts=[fact("Advances against term deposits, NSCs eligible for surrender, KVPs and life insurance policies need not "
              "be treated as NPAs, provided adequate margin is available; advances against gold ornaments, government "
              "securities and all other securities are not covered by this exemption", C_IRAC)])
Q(T, "Resolution and IBC", "Basic",
  "The Insolvency and Bankruptcy Board of India (IBBI), the regulator that implements the Insolvency and Bankruptcy "
  "Code, was established on:",
  ["1 October 2016", "28 May 2016", "1 December 2016", "1 April 2017"],
  concept="IBBI",
  explanation="IBBI was established on 1 October 2016 under the Insolvency and Bankruptcy Code, 2016. It is a key pillar "
              "of the ecosystem that implements the Code (it marks 1 October as its Annual Day).",
  steps=["IBC enacted 2016", "IBBI established under the Code on 1 October 2016"],
  why="The other dates are not IBBI's establishment date.",
  facts=[fact("The Insolvency and Bankruptcy Board of India was established on 1st October, 2016 under the Insolvency "
              "and Bankruptcy Code, 2016", C_IBBI)])
Q(T, "SARFAESI", "Basic",
  "Asset reconstruction companies (ARCs) registered under the SARFAESI Act acquire stressed loans and issue security "
  "receipts (SRs). According to RBI's FAQs on ARCs, what is the maximum realisation period for financial assets "
  "acquired by an ARC?",
  ["Eight years from the date of acquisition", "Three years from the date of acquisition",
   "Five years from the date of acquisition", "Ten years from the date of acquisition"],
  concept="ARCs and security receipts",
  explanation="RBI's ARC FAQs (September 2026) refer to the maximum realisation period of 8 years from the date of "
              "acquisition. A transferee ARC cannot issue SRs to other qualified buyers for such assets after the "
              "eight-year period from the first acquisition has expired.",
  steps=["ARC acquires asset and issues SRs", "Realisation window: 8 years from acquisition"],
  why="Three, five and ten years are not the prescribed window.",
  facts=[fact("ARCs are not prohibited from transferring financial assets to another ARC even after completion of the "
              "maximum realisation period of 8 years from the date of acquisition, but the transferee ARC shall not "
              "issue SRs to other QBs after the expiry of the stipulated eight-year period", C_ARC)])
Q(T, "Classification", "Intermediate",
  "A bank's loan is backed by a guarantee of the Central Government. Interest has been overdue for more than 90 days. "
  "Under RBI's IRAC Directions, 2025, when will this account be treated as an NPA?",
  ["Only when the Government repudiates its guarantee when invoked",
   "Immediately, since interest is overdue for more than 90 days",
   "Only after it remains overdue for 12 months",
   "Never, since sovereign-guaranteed loans are always standard"],
  concept="Government guaranteed advances",
  explanation="Credit facilities backed by a Central Government guarantee, though overdue, are treated as NPA only when "
              "the Government repudiates its guarantee when invoked. This exemption is not for income recognition. "
              "State Government guaranteed advances, by contrast, follow the normal 90-day norm.",
  steps=["Central Government guarantee → NPA only on repudiation when invoked",
         "State Government guarantee → normal 90-day overdue norm"],
  why="The 90-day norm applies to State (not Central) Government guaranteed advances; there is no 12-month rule; the "
      "account is not standard for ever, as repudiation makes it an NPA.",
  facts=[fact("The credit facilities backed by guarantee of the Central Government though overdue shall be treated as "
              "NPA only when the Government repudiates its guarantee when invoked; State Government guaranteed advances "
              "attract the norms if dues remain overdue for more than 90 days", C_IRAC)])
Q(T, "Classification", "Intermediate",
  "When a fraud is detected in a borrower account, a bank must normally provide for the entire amount due immediately. "
  "To smooth the impact on quarterly profits, over what maximum period may it spread this provision?",
  ["Four quarters, starting with the quarter in which the fraud is detected", "Two quarters after the fraud is reported",
   "Eight quarters from the date of the fraud", "Until the end of the next financial year"],
  concept="Provisioning for frauds",
  explanation="Under the IRAC Directions, a bank has the option to make the fraud provision over a period not exceeding "
              "four quarters, commencing with the quarter of detection. If this spills into the next financial year, the "
              "unprovided amount at year-end is debited to 'other reserves'.",
  steps=["Default: full provision immediately", "Option: spread over up to four quarters from the quarter of detection"],
  why="Two quarters is too short; eight quarters and 'end of next year' exceed the four-quarter limit.",
  facts=[fact("A bank shall normally provide for the entire amount due immediately upon a fraud being detected; it has "
              "the option to make the provisions over a period not exceeding four quarters, commencing from the quarter "
              "in which the fraud has been detected", C_IRAC)])
Q(T, "Classification", "Intermediate",
  "What provision must a bank hold on its standard-account exposure to a company that has a director (other than a "
  "nominee director of a government or financial institution brought in at the time of distress) whose name appears "
  "more than once in the list of wilful defaulters?",
  ["5 per cent", "0.40 per cent", "1 per cent", "15 per cent"],
  concept="Standard asset provisioning: wilful defaulters",
  explanation="The IRAC Directions prescribe a provision of 5% on existing loans or exposures to companies with such "
              "director(s), even when the accounts are standard, well above the normal standard-asset rate.",
  steps=["Director appears more than once in wilful defaulter list", "Standard account → 5% provision"],
  why="0.40% is the general standard-asset rate; 1% applies to commercial real estate; 15% is the substandard rate.",
  facts=[fact("The provisioning in respect of existing loans / exposures to companies having director(s) (other than "
              "nominee directors of government / financial institutions brought on board at the time of distress), whose "
              "name(s) appear more than once in the list of wilful defaulters, shall be five per cent in cases of "
              "standard accounts", C_IRAC)])
Q(T, "SARFAESI", "Intermediate",
  "According to RBI's FAQs on asset reconstruction companies (September 2026), can an ARC restructure a borrower "
  "account that the lender has classified as fraud or wilful defaulter?",
  ["No, unless the existing promoters are replaced and the company is totally delinked from them",
   "Yes, if the restructuring is approved by the ARC's Board",
   "Yes, but only by converting debt into equity",
   "No, and the ARC must sell such accounts within one year"],
  concept="ARC restructuring",
  explanation="ARCs are not permitted to restructure accounts classified as fraud or wilful defaulter. Restructuring "
              "includes rescheduling, conversion of debt into equity and additional funding. The exception: where the "
              "existing promoters are replaced by new promoters and the borrower company is totally delinked from the "
              "erstwhile promoters/management, the ARC may consider restructuring based on viability.",
  steps=["Fraud / wilful defaulter accounts → no restructuring by ARC",
         "Exception: promoters replaced and company delinked from them"],
  why="Board approval does not override the bar; debt-equity conversion is itself a form of restructuring; there is no "
      "one-year sale rule.",
  facts=[fact("ARCs are not permitted to restructure borrower accounts classified as fraud/ wilful defaulter; however, "
              "where the existing promoters are replaced by new promoters and the borrower company is totally delinked "
              "from such erstwhile promoters/management, ARCs may take a view on restructuring based on viability",
              C_ARC)])
Q(T, "Classification", "Advanced",
  "Under RBI's IRAC Directions, 2025, certain agricultural loans follow the crop-season norms for NPA classification "
  "instead of the 90-day norm. Which of the following loans qualify for the crop-season norms?\n"
  "P. ₹50 lakh to an individual farmer against pledge of his produce for 10 months\n"
  "Q. ₹75 lakh to an individual farmer against pledge of his produce for 6 months\n"
  "R. ₹2 crore to a farmer producer organisation (aggregate borrowing ₹3 crore) against pledge of produce for 9 months\n"
  "S. ₹2 crore to a corporate farmer against pledge of produce for 15 months",
  ["P and R only", "P, Q and R only", "P only", "R and S only"],
  concept="Agricultural loans and crop-season NPA norms",
  explanation="Crop-season norms apply to pledge loans to individual farmers up to ₹60 lakh for not more than 12 months, "
              "and to corporate farmers, FPOs, partnership firms and co-operatives of farmers (aggregate limit ₹4 crore "
              "per borrower) for pledge loans up to ₹2.5 crore for not more than 12 months. Other agricultural loans "
              "follow the 90-day norm.",
  steps=["P: ₹50 lakh ≤ ₹60 lakh, 10 ≤ 12 months → qualifies",
         "Q: ₹75 lakh > ₹60 lakh → 90-day norm",
         "R: aggregate ₹3 crore ≤ ₹4 crore; ₹2 crore ≤ ₹2.5 crore; 9 months → qualifies",
         "S: 15 months > 12 months → 90-day norm"],
  why="Q exceeds the ₹60 lakh cap for individuals; S exceeds the 12-month period.",
  facts=[fact("Crop-season norms apply to loans to individual farmers up to ₹60 lakh against pledge / hypothecation of "
              "agricultural produce for a period not exceeding twelve months, and to loans to corporate farmers, FPOs, "
              "partnership firms and co-operatives of farmers up to an aggregate limit of ₹4 crore per borrower, "
              "including loans up to ₹2.5 crore against pledge of produce for not more than twelve months; other "
              "agricultural loans follow the 90 days delinquency norm", C_IRAC)])

# ================= Basel Norms (Basic 4 / Intermediate 2 / Advanced 2)
T = "Basel Norms"
Q(T, "Capital adequacy", "Basic",
  "The first paper issued by the Basel Committee, in 1975, came to be known as the 'Concordat'. What did it deal with?",
  ["Sharing supervisory responsibility for banks' foreign establishments between host and home supervisors",
   "A minimum capital ratio of 8% of risk-weighted assets",
   "Capital requirements for market risk using internal models",
   "Liquidity standards to survive a 30-day stress period"],
  concept="Basel Concordat",
  explanation="The 1975 Concordat set out principles for sharing supervisory responsibility for banks' foreign "
              "branches, subsidiaries and joint ventures between host and parent (home) supervisors, to close gaps in "
              "international supervisory coverage. It was revised in May 1983.",
  steps=["1975 Concordat → home/host supervision of foreign establishments", "8% ratio → 1988 Accord",
         "Market risk → 1996 amendment", "30-day liquidity → Basel III LCR"],
  why="The other options describe later Basel standards.",
  facts=[fact("The 1975 paper known as the Concordat set out principles for sharing supervisory responsibility for "
              "banks' foreign branches, subsidiaries and joint ventures between host and parent (or home) supervisory "
              "authorities", C_BCBS)])
Q(T, "Capital adequacy", "Basic",
  "The Basel Committee's 'Core Principles for Effective Banking Supervision', first published in September 1997 with "
  "25 principles, now contain how many principles after the latest revision in April 2024?",
  ["29", "25", "30", "24"],
  concept="Basel Core Principles",
  explanation="The Core Principles began with 25 basic principles in 1997. After several revisions, most recently in "
              "April 2024, the document now includes 29 principles.",
  steps=["1997: 25 principles", "After revisions (latest April 2024): 29 principles"],
  why="25 was the original number; 24 (the CPMI-IOSCO PFMIs) and 30 are distractors.",
  facts=[fact("When first published in September 1997, the paper set out 25 basic principles; after several revisions, "
              "most recently in April 2024, the document now includes 29 principles", C_BCBS)])
Q(T, "LCR and NSFR", "Basic",
  "Basel III introduced two liquidity standards. The Liquidity Coverage Ratio covers funding needs over a 30-day "
  "stress period. What is the Net Stable Funding Ratio (NSFR) intended to address?",
  ["Maturity mismatches over the entire balance sheet", "Intraday liquidity needs in payment systems",
   "Concentration of large exposures to one counterparty", "Losses from operational failures"],
  concept="LCR versus NSFR",
  explanation="In the Basel Committee's description, the LCR is meant to provide enough cash for a 30-day stress period, "
              "while the NSFR is a longer-term ratio intended to address maturity mismatches over the entire balance "
              "sheet.",
  steps=["LCR: short term, 30-day stress", "NSFR: longer term, maturity mismatch across the balance sheet"],
  why="Intraday liquidity, large exposures and operational risk are covered by other standards.",
  facts=[fact("Basel III liquidity requirements: the Liquidity Coverage Ratio (LCR), intended to provide enough cash to "
              "cover funding needs over a 30-day period of stress; and a longer-term ratio, the Net Stable Funding "
              "Ratio (NSFR), intended to address maturity mismatches over the entire balance sheet", C_BCBS)])
Q(T, "Leverage ratio", "Basic",
  "Which Basel III requirement sets a minimum amount of loss-absorbing capital relative to all of a bank's assets and "
  "off-balance sheet exposures, regardless of risk weighting?",
  ["Leverage ratio", "Capital conservation buffer", "Countercyclical capital buffer", "Liquidity Coverage Ratio"],
  concept="Leverage ratio as a non-risk-based measure",
  explanation="The Basel III leverage ratio is a simple, non-risk-based backstop: capital relative to total exposures, "
              "irrespective of risk weights. The buffers are add-ons to risk-based capital, and the LCR is a liquidity "
              "measure.",
  steps=["'Regardless of risk weighting' → leverage ratio"],
  why="The two buffers are percentages of risk-weighted assets; the LCR concerns liquid assets, not capital.",
  facts=[fact("Basel III includes a leverage ratio - a minimum amount of loss-absorbing capital relative to all of a "
              "bank's assets and off-balance sheet exposures regardless of risk weighting", C_BCBS)])
Q(T, "Capital adequacy", "Intermediate",
  "The Basel Committee completed its Basel III post-crisis reforms in 2017. Which element of these reforms limits the "
  "extent to which banks can use internal models to reduce their risk-based capital requirements?",
  ["The output floor, based on the revised standardised approaches", "The capital conservation buffer",
   "The Pillar 3 disclosure framework", "The Net Stable Funding Ratio"],
  concept="Basel III finalisation (2017)",
  explanation="The 2017 reforms revised the standardised approaches for credit, CVA and operational risk and added a "
              "revised leverage ratio, a leverage ratio buffer for G-SIBs and an output floor. The output floor is "
              "based on the revised standardised approaches and limits how far internal models can reduce RWAs, to cut "
              "excessive variability in risk-weighted assets.",
  steps=["2017 finalisation → output floor", "Purpose: curb RWA variability from internal models"],
  why="The conservation buffer restricts payouts; Pillar 3 is disclosure; the NSFR is a funding ratio.",
  facts=[fact("The final reforms also include a revised leverage ratio, a leverage ratio buffer for global systemically "
              "important banks and an output floor, based on the revised standardised approaches, which limits the "
              "extent to which banks can use internal models to reduce risk-based capital requirements", C_BCBS)])
Q(T, "LCR and NSFR", "Intermediate",
  "A customer's non-callable fixed deposit, normally excluded from a bank's LCR computation, is pledged as collateral "
  "for a loan to the customer. Under RBI's LCR amendments effective 1 April 2026, how is this deposit treated?",
  ["As a callable deposit for LCR purposes", "It stays excluded, as it is contractually non-callable",
   "As Level 1 high-quality liquid assets of the bank", "As a deduction from the bank's CET1 capital"],
  concept="LCR treatment of pledged deposits",
  explanation="RBI's April 2025 circular (effective 1 April 2026) says that a deposit hitherto excluded from LCR "
              "computation, such as a non-callable FD, that is contractually pledged as collateral for a credit facility "
              "shall be treated as callable for LCR purposes, so it attracts the relevant run-off.",
  steps=["Non-callable FD → normally excluded", "Pledged against a loan → treated as callable for LCR"],
  why="It does not stay excluded; a customer deposit is a liability, not the bank's HQLA; it has nothing to do with "
      "CET1 deductions.",
  facts=[fact("In case a deposit, hitherto excluded from LCR computation (for instance, a non-callable fixed deposit), "
              "is contractually pledged as collateral to secure a credit facility or loan, such deposit shall be treated "
              "as callable for LCR purposes; these amendments come into force from April 01, 2026", C_LCR25)])
hqla, outflow_old, trust = 1350, 1500, 400
lcr_old = pct(hqla, outflow_old)
outflow_new = outflow_old - trust + trust * 0.40
lcr_new = pct(hqla, outflow_new)
assert round(lcr_old, 1) == 90.0 and outflow_new == 1260 and round(lcr_new, 1) == 107.1
Q(T, "LCR and NSFR", "Advanced",
  "A bank has HQLA of ₹1,350 crore and total net cash outflows of ₹1,500 crore over the next 30 days, computed under "
  "the earlier rules. These outflows include ₹400 crore of deposits from educational trusts and partnership firms "
  "(not small business customers), which ran off at 100%. Under RBI's LCR amendments effective 1 April 2026, such "
  "funding is treated as from non-financial corporates. Assuming nothing else changes, how does the bank's LCR move?",
  ["From 90% to about 107.1%, crossing the 100% minimum", "From 90% to 100%, just meeting the minimum",
   "From 90% to about 95.1%, still below the minimum", "It stays at 90%, as only retail deposits were affected"],
  concept="LCR = HQLA ÷ total net cash outflows over 30 days",
  explanation="Funding from trusts, AoPs, partnerships, LLPs etc. (not treated as SBCs) now attracts a 40% run-off "
              "instead of 100%. Outflow on ₹400 crore falls from ₹400 crore to ₹160 crore, so net outflows fall to "
              "₹1,260 crore.",
  steps=["Old LCR = 1,350 ÷ 1,500 = 90%", "New outflow on trust deposits = 40% × 400 = ₹160 crore",
         "New net outflows = 1,500 − 400 + 160 = ₹1,260 crore", "New LCR = 1,350 ÷ 1,260 ≈ 107.1%"],
  why="100% ignores the reduced outflow's full effect; 95.1% would apply a smaller cut; the change applies to trusts "
      "and partnerships, not only retail deposits.",
  computed=True,
  facts=[fact("Funding from non-financial entities such as trusts (educational/religious/charitable), AoPs, "
              "partnerships, proprietorships, LLPs and other incorporated entities shall be categorised as funding from "
              "'non-financial corporates' and attract a run-off rate of 40 per cent (as against 100 per cent currently "
              "prescribed), unless treated as SBCs; effective April 01, 2026", C_LCR25)])
Q(T, "Capital adequacy", "Advanced",
  "Consider the following statements about the evolution of the Basel framework, as described by the Basel "
  "Committee:\n"
  "I. The 1988 Accord's minimum capital ratio was to be implemented by the end of 1992.\n"
  "II. The Market Risk Amendment of 1996 introduced the leverage ratio for the first time.\n"
  "III. Basel III added a capital conservation buffer that, when breached, restricts payouts, with most reforms phased "
  "in between 2013 and 2019.\n"
  "Which of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="History of the Basel accords",
  explanation="The 1988 Accord called for an 8% minimum to be implemented by end-1992 (I correct). The 1996 amendment "
              "added capital for market risk and allowed internal VaR models; the leverage ratio came only with Basel "
              "III (II wrong). Basel III added the capital conservation buffer, which restricts payouts when breached, "
              "with most reforms phased in between 2013 and 2019 (III correct).",
  steps=["I ✓ (end-1992)", "II ✗ (leverage ratio is a Basel III element)", "III ✓"],
  why="Any option including II is wrong.",
  facts=[fact("The 1988 Accord called for a minimum ratio of capital to risk-weighted assets of 8% to be implemented by "
              "the end of 1992", C_BCBS),
         fact("The Market Risk Amendment (January 1996) incorporated a capital requirement for market risks; Basel III "
              "adds a capital conservation buffer that, when breached, restricts payouts, and a leverage ratio; most of "
              "the reforms are being phased in between 2013 and 2019", C_BCBS)])

# ================= Priority Sector Lending (Basic 1 / Intermediate 5 / Advanced 1)
T = "Priority Sector Lending"
Q(T, "PSLCs", "Basic",
  "When a bank trades Priority Sector Lending Certificates (PSLCs) on RBI's e-Kuber portal, how is the counterparty "
  "decided?",
  ["Orders are matched anonymously by the portal; the bank cannot select the counterparty",
   "The buying bank selects the seller from a list of offers",
   "NABARD allots a seller to each buyer",
   "Buyer and seller negotiate bilaterally and report the deal to RBI"],
  concept="PSLC trading mechanism",
  explanation="RBI's PSL FAQs state that order matching on the e-Kuber PSLC module is anonymous; neither buyer nor "
              "seller can select the counterparty. Partial matching can happen depending on premium and lots available. "
              "No transaction fee is charged for using the module.",
  steps=["PSLC trade on e-Kuber", "Anonymous order matching; no counterparty selection"],
  why="Buyers cannot pick sellers; NABARD has no allotment role; PSLCs are not bilateral OTC deals.",
  facts=[fact("The order matching will be done on anonymous basis through the portal and the buyer/seller cannot select "
              "the counterparty; partial matching will happen depending on the matching of premium and availability of "
              "category-wise PSLC lots", C_PSL)])
Q(T, "PSLCs", "Intermediate",
  "Bank X sold a PSLC to Bank Y. Later, an RBI inspection finds that the loans underlying the PSLC were not eligible "
  "for priority sector classification. According to RBI's FAQs, whose achievement is reduced?",
  ["Only the seller's (Bank X); the buyer bears no risk",
   "Only the buyer's (Bank Y), as it used the certificate",
   "Both banks' equally",
   "Neither bank's, since the PSLC has expired on 31 March"],
  concept="Risk in PSLC trades",
  explanation="RBI's FAQs say misclassifications, if any, are reduced from the achievement of the PSLC seller bank only. "
              "There is no risk for the PSLC buyer even if the underlying asset is later found ineligible.",
  steps=["PSLC sold by X, bought by Y", "Underlying declassified → X's achievement reduced; Y unaffected"],
  why="The buyer is protected; the loss is not shared; expiry does not erase the seller's misclassification.",
  facts=[fact("The misclassifications, if any, will have to be reduced from the achievement of PSLC seller bank only. "
              "There will be no risk for the PSLC buyer, even if the underlying asset of the traded PSLC gets "
              "misclassified", C_PSL)])
Q(T, "Targets and sub-targets", "Intermediate",
  "A bank that missed its priority sector targets has outstanding shortfall deposits with NABARD, SIDBI and NHB. "
  "According to RBI's PSL FAQs, how are these deposits treated?",
  ["NABARD deposits count under agriculture, SIDBI under MSME and NHB under housing; all count towards the overall "
   "target and are added to net bank credit for ANBC",
   "They count only towards the overall PSL target, not any sub-target, and are excluded from ANBC",
   "They are deducted from net bank credit while computing ANBC",
   "Only NABARD deposits count, and only towards the agriculture sub-target"],
  concept="Shortfall deposits with DFIs",
  explanation="Outstanding deposits with NABARD on account of PSL shortfall count towards the agriculture sub-target; "
              "those with SIDBI and MUDRA under MSME lending; those with NHB under housing. All count for the overall "
              "PSL target and are added to net bank credit (NBC) in computing ANBC.",
  steps=["NABARD → agriculture", "SIDBI / MUDRA → MSME", "NHB → housing", "All → overall target; added to NBC"],
  why="They do count towards sub-targets, are added to (not deducted from) NBC, and are not limited to NABARD.",
  facts=[fact("Outstanding deposits with NABARD on account of PSL shortfall are eligible to be reckoned towards "
              "Agriculture sub-target and overall PSL target; deposits with SIDBI and MUDRA under MSME lending; deposits "
              "with NHB under Housing; all outstanding deposits shall be added to Net Bank Credit for the computation of "
              "ANBC", C_PSL)])
Q(T, "Targets and sub-targets", "Intermediate",
  "Bank loans for 'Agriculture Infrastructure' and for 'Food and Agro-processing' qualify as priority sector subject "
  "to an aggregate sanctioned limit per borrower from the banking system. What is that limit, and what happens if a "
  "borrower's aggregate exposure across banks exceeds it?",
  ["₹100 crore; the entire exposure ceases to be priority sector",
   "₹100 crore; only the excess over ₹100 crore loses PSL status",
   "₹50 crore; the entire exposure ceases to be priority sector",
   "₹50 crore; only the excess over ₹50 crore loses PSL status"],
  concept="Credit caps in agriculture PSL categories",
  explanation="Each of these categories is subject to an aggregate sanctioned limit of ₹100 crore per borrower from the "
              "banking system. If the aggregate exposure across the banking industry exceeds ₹100 crore, the total "
              "exposure ceases to be classified as PSL, not merely the excess.",
  steps=["Limit: ₹100 crore per borrower across banks", "Breach → whole exposure loses PSL status"],
  why="The limit is ₹100 crore, not ₹50 crore, and the whole exposure (not just the excess) is affected.",
  facts=[fact("Loans for Agriculture Infrastructure or for Food & Agro-processing activity are each subject to an "
              "aggregate sanctioned limit of ₹100 crore per borrower from the banking system; if aggregate exposure "
              "across the banking industry exceeds ₹100 crore, total exposure will cease to be classified under PSL",
              C_PSL)])
Q(T, "Targets and sub-targets", "Intermediate",
  "A farmer takes a crop loan from a bank against the pledge of gold jewellery. The loan is sanctioned on the basis of "
  "the scale of finance for the crop. Can it be classified under priority sector (agriculture)?",
  ["Yes; PSL is activity- and beneficiary-specific, so gold collateral alone does not make it ineligible",
   "No; loans against gold are never eligible for priority sector",
   "Yes, but only if the loan is below ₹2 lakh",
   "No, unless the farmer also mortgages agricultural land"],
  concept="PSL is based on activity, not collateral",
  explanation="RBI's FAQs say PSL guidelines are activity- and beneficiary-specific and not based on the type of "
              "collateral, so an agricultural loan does not become ineligible only because the security is gold "
              "jewellery. The bank should have assessed the credit requirement (scale of finance) for the activity.",
  steps=["Test the purpose and borrower, not the collateral", "Agricultural purpose + proper assessment → PSL"],
  why="There is no blanket bar on gold-backed loans; ₹2 lakh is the limit for waiving collateral, not an eligibility "
      "cap; a land mortgage is not required.",
  facts=[fact("The PSL guidelines are activity and beneficiary specific and are not based on type of collateral; "
              "therefore, bank loans given for undertaking agriculture activities do not automatically become ineligible "
              "for priority sector classification only on account of the fact that underlying asset is gold "
              "jewellery/ornament", C_PSL)])
Q(T, "Targets and sub-targets", "Intermediate",
  "A bank lends for farming to a partnership firm, one of whose partners holds 1.5 hectares of agricultural land. Can "
  "the loan be tagged under the Small and Marginal Farmers (SMF) category of PSL?",
  ["No; loans to partnership firms are not eligible for the SMF category on the basis of a partner's land holding",
   "Yes, since the partner holds less than 2 hectares",
   "Yes, but only for the partner's share of the loan",
   "Yes, if the firm also qualifies as a micro enterprise"],
  concept="SMF category eligibility",
  explanation="SMF covers individuals, SHGs, JLGs, Farmer Producer Companies and co-operatives of farmers meeting the "
              "membership and land-holding criteria. RBI's FAQs say loans to partnership firms, co-borrowers or a "
              "company whose director holds up to 2 hectares are not eligible for the SMF category.",
  steps=["SMF: individuals, SHGs, JLGs, FPCs, co-operatives of farmers", "Partnership firm → not SMF"],
  why="A partner's holding does not make the firm an SMF; there is no pro-rata tagging; MSME status is irrelevant to "
      "the SMF tag.",
  facts=[fact("Loans to partnership firms/co-borrowers or any director of a company holding agriculture land upto 2 "
              "hectares are not eligible to be classified under the SMF category of PSL", C_PSL)])
nbc, buy, sell, dep = 50000, 3000, 1000, 1500
anbc = nbc + (buy - sell) + dep
assert anbc == 53500 and anbc * 0.40 == 21400
Q(T, "Targets and sub-targets", "Advanced",
  "A domestic commercial bank has net bank credit (NBC) of ₹50,000 crore. During the year it bought PSLCs of ₹3,000 "
  "crore and sold PSLCs of ₹1,000 crore (all outstanding), and it has ₹1,500 crore of outstanding PSL-shortfall "
  "deposits with NABARD. Assume no other ANBC adjustments and that CEOBSE is lower. What is its overall PSL target "
  "(40% of ANBC)?",
  ["₹21,400 crore", "₹20,000 crore", "₹20,800 crore", "₹21,800 crore"],
  concept="ANBC adjustments for PSLCs and shortfall deposits",
  explanation="RBI's FAQs say the net PSLC position (buy minus sell) is added to NBC, and outstanding shortfall deposits "
              "with NABARD/SIDBI/MUDRA/NHB are also added to NBC, in computing ANBC.",
  steps=["Net PSLC = 3,000 − 1,000 = ₹2,000 crore", "ANBC = 50,000 + 2,000 + 1,500 = ₹53,500 crore",
         "Target = 40% × 53,500 = ₹21,400 crore"],
  why="₹20,000 crore ignores both adjustments; ₹20,800 crore ignores the deposits; ₹21,800 crore adds gross PSLC "
      "purchases instead of the net position.",
  computed=True,
  facts=[fact("The net PSLC outstanding (PSLC Buy minus PSLC Sell) is added to the Net Bank Credit; the effect of PSLC "
              "buy is increase in ANBC and of PSLC sell is decrease in ANBC", C_PSL),
         fact("All outstanding deposits with NABARD, SIDBI, MUDRA and NHB on account of PSL shortfall shall be added to "
              "Net Bank Credit (NBC) for the computation of ANBC", C_PSL)])

# ================= RBI Integrated Ombudsman Scheme (Basic 1 / Intermediate 3 / Advanced 1)
T = "RBI Integrated Ombudsman Scheme"
Q(T, "Process and limits", "Basic",
  "Under the Reserve Bank – Integrated Ombudsman Scheme, 2026, to which e-mail address should a complaint be sent if "
  "it is not filed on the CMS portal?",
  ["crpc@rbi.org.in", "ombudsman@rbi.org.in", "helpdoc@rbi.org.in", "cepd@rbi.org.in"],
  concept="Modes of filing under RB-IOS, 2026",
  explanation="Complaints can be filed online on the CMS portal (cms.rbi.org.in), by e-mail to crpc@rbi.org.in, or "
              "physically with the Centralised Receipt and Processing Centre (CRPC) in Chandigarh.",
  steps=["Online → cms.rbi.org.in", "E-mail → crpc@rbi.org.in", "Physical → CRPC, Chandigarh"],
  why="The other addresses are not the designated complaint e-mail under the Scheme.",
  facts=[fact("Procedure for filing a complaint: online through the CMS portal at https://cms.rbi.org.in; e-mail by "
              "sending the complaint to crpc@rbi.org.in; physical mode to the Centralised Receipt and Processing Centre, "
              "Chandigarh", C_RBIOS)])
Q(T, "Scope and grounds", "Intermediate",
  "Assuming all procedural conditions are met, which of the following grievances can be maintained before the RBI "
  "Ombudsman under RB-IOS, 2026?",
  ["A customer's complaint that her bank did not credit interest on her deposit as per its terms",
   "A software vendor's dispute with a bank over payment of its invoices",
   "An employee's grievance about salary arrears from the bank that employs him",
   "A customer's grievance against the bank's managing director personally"],
  concept="Maintainability under RB-IOS, 2026",
  explanation="The Scheme covers deficiency in service by a covered Regulated Entity to its customer. Disputes between a "
              "vendor and an RE, employer-employee disputes, and grievances against the management or executives of "
              "an RE are listed as non-maintainable.",
  steps=["Deposit interest not credited → deficiency in service → maintainable",
         "Vendor dispute, employment dispute, grievance against executives → non-maintainable"],
  why="The other three are expressly excluded categories.",
  facts=[fact("Not maintainable: disputes between a vendor and a Regulated Entity; grievances against Management or "
              "Executives of a Regulated Entity; disputes involving employee-employer relationship of a Regulated "
              "Entity", C_RBIOS)])
Q(T, "Process and limits", "Intermediate",
  "An appeal is filed before the Appellate Authority against an Award of the RBI Ombudsman under RB-IOS, 2026. Which "
  "of the following can the Appellate Authority do?",
  ["Remand the matter to the RBI Ombudsman for fresh disposal with directions",
   "Refer the complaint to a civil court for trial",
   "Transfer the case to the Banking Ombudsman of another State",
   "Impose a penalty on the complainant for filing the complaint"],
  concept="Appellate Authority under RB-IOS, 2026",
  explanation="The Appellate Authority may allow the appeal and set aside the Award, remand the matter to the RBI "
              "Ombudsman for fresh disposal with directions, modify the Award and pass directions to give effect to it, "
              "or pass any other order it deems fit.",
  steps=["Options: set aside / remand / modify / other order"],
  why="Referral to a civil court and penalising the complainant are not provided; under 'One Nation One Ombudsman' "
      "there is no State-wise transfer.",
  facts=[fact("The Appellate Authority may allow the appeal and set aside the Award; remand the matter to the RBI "
              "Ombudsman for fresh disposal with appropriate directions; modify the Award and pass directions; or pass "
              "any other order as it may deem fit", C_RBIOS)])
Q(T, "Scope and grounds", "Intermediate",
  "Ravi's bank froze his savings account in compliance with a written order of a law enforcement agency. He complains "
  "to the RBI Ombudsman about the freeze. Under RB-IOS, 2026, his complaint is:",
  ["Not maintainable, as the bank acted in compliance with an order of a law enforcement authority",
   "Maintainable, since freezing an account is a deficiency in service",
   "Maintainable only if the freeze lasted more than 30 days",
   "To be transferred by the Ombudsman to the police for decision"],
  concept="Excluded grounds under RB-IOS, 2026",
  explanation="Grievances arising from action taken by a Regulated Entity in compliance with orders of a judicial, "
              "quasi-judicial, statutory or law enforcing authority are not maintainable under the Scheme.",
  steps=["Action taken on a law enforcement order → excluded ground"],
  why="Such compliance is not a deficiency in service; there is no 30-day condition; the Ombudsman does not transfer "
      "complaints to the police.",
  facts=[fact("Not maintainable: grievances arising from action taken by a Regulated Entity in compliance with orders "
              "of a judicial/quasi-judicial, statutory or law enforcing authority", C_RBIOS)])
Q(T, "Process and limits", "Advanced",
  "Consider the following statements about RB-IOS, 2026:\n"
  "I. The Appellate Authority can only confirm or set aside an Award; it cannot modify it.\n"
  "II. A Regulated Entity may appeal (with the required prior approval) within 30 days of receiving the complainant's "
  "letter accepting the Award, and the Appellate Authority may allow up to 30 more days for sufficient reason.\n"
  "III. A complainant may voluntarily withdraw a complaint at any stage, through the 'Track a complaint' tab on the CMS "
  "portal.\n"
  "Which of the above is/are correct?",
  ["II and III only", "I and II only", "III only", "I, II and III"],
  concept="Appeals and withdrawal under RB-IOS, 2026",
  explanation="The Appellate Authority can also remand or modify an Award (I wrong). An RE's appeal lies within 30 days "
              "of receipt of the complainant's acceptance letter, extendable by up to 30 days (II correct). A complaint "
              "may be withdrawn at any stage via 'Track a complaint' on CMS (III correct).",
  steps=["I ✗ (can modify or remand)", "II ✓", "III ✓"],
  why="Options with I are wrong; 'III only' misses II.",
  facts=[fact("A Regulated Entity may also file an appeal within 30 days from the date of receipt of the complainant's "
              "letter accepting the Award, subject to the required prior approval; the Appellate Authority may allow a "
              "further period of up to 30 days; the Appellate Authority may modify the Award", C_RBIOS),
         fact("A complainant may voluntarily withdraw a complaint at any stage by logging on to the CMS portal and going "
              "to the tab 'Track a complaint'", C_RBIOS)])

# ================= Digital Banking (Basic 3 / Intermediate 2 / Advanced 1)
T = "Digital Banking"
Q(T, "CBDC (e-rupee)", "Basic",
  "Asha wants to buy a ₹15 item but has only a ₹20 denomination in her retail e₹ wallet. According to RBI's e₹ FAQs, "
  "what happens?",
  ["She enters ₹15; the merchant gets ₹15 and ₹5 stays in her wallet",
   "She must first load a ₹10 and a ₹5 denomination from her bank account",
   "The merchant must return ₹5 in cash",
   "She must pay ₹20 and the merchant credits ₹5 as a voucher"],
  concept="Change feature of the e₹ wallet",
  explanation="e₹ is held in denominations like cash, but every e₹ wallet has a change feature: the user enters the "
              "amount; ₹15 is credited to the merchant automatically and the balance ₹5 remains in the wallet.",
  steps=["Enter ₹15", "Merchant credited ₹15", "₹5 stays in the wallet"],
  why="No extra loading, cash change or voucher is needed.",
  facts=[fact("If one desires to purchase a ₹15 item but has only ₹20 denomination in the e₹ wallet, she can enter ₹15 "
              "in the amount field; ₹15 will automatically be credited to the merchant while the balance ₹5 will remain "
              "in the e₹ wallet", C_ERUPEE)])
Q(T, "Digital lending", "Basic",
  "Under the RBI (Digital Lending) Directions, 2025, when a recovery agent is assigned to a defaulted digital loan (or "
  "the agent is changed), what must the lender do?",
  ["Send the agent's particulars to the borrower by e-mail/SMS before the agent contacts the borrower",
   "Publish the agent's name in a national newspaper",
   "Obtain the borrower's written consent to the appointment",
   "Inform the borrower only after the dues are recovered"],
  concept="Recovery conduct in digital lending",
  explanation="The Directions require that the particulars of the recovery agent authorised to approach the borrower be "
              "communicated to the borrower through e-mail/SMS before the agent contacts the borrower.",
  steps=["Agent assigned or changed", "Particulars to borrower by e-mail/SMS first", "Then contact"],
  why="No newspaper notice or borrower consent is prescribed; telling the borrower afterwards defeats the purpose.",
  facts=[fact("In case of a loan default, when a recovery agent is assigned for recovery or there is a change in the "
              "recovery agent, the particulars of such recovery agent shall be communicated to the borrower through "
              "email/ SMS before the recovery agent contacts the borrower for recovery", C_DL25)])
Q(T, "Mobile and internet banking", "Basic",
  "Card tokenisation replaces actual card details with a unique 'token' for payments through phones, wearables and "
  "other devices. According to RBI, who can perform tokenisation and de-tokenisation?",
  ["The authorised card network or the card issuer", "The merchant accepting the payment",
   "The token requestor app on the customer's device", "The National Informatics Centre"],
  concept="Device-based card tokenisation",
  explanation="RBI's FAQs say tokenisation and de-tokenisation can be performed by the authorised card network or by "
              "the card issuer (the token service provider). Token requestors cannot store the card number; the "
              "merchant never receives actual card details. The service is free and optional for customers.",
  steps=["Token service provider = card network or card issuer"],
  why="Merchants and token requestors cannot hold card details; NIC has no role.",
  facts=[fact("Tokenisation and de-tokenisation can be performed by the authorised card network or by the card issuer; "
              "token requestor cannot store Primary Account Number (PAN) or any other card detail", C_TOKEN)])
Q(T, "Digital lending", "Intermediate",
  "Under the RBI (Digital Lending) Directions, 2025, in which of the following forms can a regulated entity NOT accept "
  "a default loss guarantee (DLG) from a lending service provider?",
  ["A corporate guarantee issued by the LSP's parent company", "Cash deposited with the regulated entity",
   "A fixed deposit with a scheduled commercial bank, with lien marked in favour of the regulated entity",
   "A bank guarantee in favour of the regulated entity"],
  concept="Forms of DLG",
  explanation="A regulated entity may accept DLG only as cash deposited with it, a fixed deposit with a scheduled "
              "commercial bank with lien marked in its favour, or a bank guarantee in its favour.",
  steps=["Permitted: cash, lien-marked FD with an SCB, bank guarantee", "Corporate guarantee → not permitted"],
  why="The other three are exactly the permitted forms.",
  facts=[fact("RE shall accept DLG only in one or more of the following forms: cash deposited with the RE; fixed deposit "
              "maintained with a Scheduled Commercial Bank with a lien marked in favour of the RE; bank guarantee in "
              "favour of the RE", C_DL25)])
Q(T, "CBDC (e-rupee)", "Intermediate",
  "Retail e₹ wallets are normally linked to the user's savings bank account. According to RBI's e₹ FAQs, how can "
  "beneficiaries of a Direct Benefit Transfer scheme receiving benefits through programmable CBDC be on-boarded?",
  ["Through mobile and/or Aadhaar number authentication, without a savings account being mandatory",
   "Only through a savings account opened under PMJDY",
   "Only by visiting an RBI regional office with KYC documents",
   "Through a credit card issued by a public sector bank"],
  concept="Programmable CBDC on-boarding",
  explanation="RBI notes that for programmable CBDC use cases such as DBT, the on-boarding criteria were modified: such "
              "users can on-board on the CBDC app through mobile and/or Aadhaar number authentication, and a savings "
              "account is not mandatory for them.",
  steps=["General e₹ wallets → linked to savings account", "DBT via programmable CBDC → mobile/Aadhaar authentication"],
  why="A PMJDY account, an RBI office visit or a credit card are not the prescribed route.",
  facts=[fact("For eligible beneficiaries of a Direct Benefit Transfer scheme receiving government benefits through "
              "Programmable CBDC, the on-boarding criteria has been modified; such users can get themselves on-boarded "
              "on CBDC App through Mobile and / or Aadhaar Number authentication; for such users it is not mandatory to "
              "have a savings account", C_ERUPEE)])
Q(T, "Digital lending", "Advanced",
  "Consider the following statements about default loss guarantee (DLG) arrangements under the RBI (Digital Lending) "
  "Directions, 2025:\n"
  "I. The regulated entity must invoke the DLG within a maximum overdue period of 120 days, unless the borrower makes "
  "good the dues earlier.\n"
  "II. Once the DLG is invoked, the amount is set off against the borrower's loan, reducing what the borrower owes.\n"
  "III. Where the DLG provider is itself a regulated entity, it must deduct the full outstanding DLG amount from its "
  "capital.\n"
  "Which of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I only"],
  concept="DLG invocation and treatment",
  explanation="DLG must be invoked within a maximum overdue period of 120 days (I correct). The invoked amount is not set "
              "off against individual loans: the borrower's liability is unaffected (II wrong). An RE acting as DLG "
              "provider deducts the full outstanding DLG from its capital (III correct). Once invoked, DLG cannot be "
              "reinstated.",
  steps=["I ✓", "II ✗ (borrower liability unaffected)", "III ✓"],
  why="Options containing II are wrong; 'I only' omits III.",
  facts=[fact("RE shall invoke DLG within a maximum overdue period of 120 days, unless the loan dues are made good by "
              "the borrower before that", C_DL25),
         fact("The amount of DLG invoked shall not be set off against the underlying individual loans, i.e. the "
              "liability of the borrowers shall remain unaffected; in case DLG provider is an RE, it shall deduct full "
              "amount of the DLG which is outstanding from its capital", C_DL25)])

# ================= UPI (Basic 3 / Intermediate 1 / Advanced 2)
T = "UPI"
Q(T, "Features", "Basic",
  "According to RBI's payments booklet (January 2021), UPI transactions use two-factor authentication through device binding and "
  "a UPI PIN. Which technology is used to encrypt the UPI PIN?",
  ["Public Key Infrastructure (PKI)", "Radio Frequency Identification (RFID)",
   "Near Field Communication (NFC)", "Magnetic Ink Character Recognition (MICR)"],
  concept="UPI security",
  explanation="RBI's payments booklet notes that the UPI PIN is encrypted using Public Key Infrastructure (PKI), while "
              "transaction data is stored in encrypted form in the app provider's system.",
  steps=["2FA = device binding + UPI PIN", "PIN encrypted with PKI"],
  why="RFID is used in FASTag, NFC in contactless cards and MICR in cheques.",
  facts=[fact("Transactions are carried out through mobile devices with two factor authentication using device binding "
              "and a UPI PIN; the UPI PIN is encrypted using Public Key Infrastructure (PKI) technology", C_BOOKLET)])
Q(T, "UPI Lite and international", "Basic",
  "Under the UPI–PayNow linkage between India and Singapore, what is the daily limit for cross-border remittances?",
  ["₹60,000 a day (about SGD 1,000)", "₹1 lakh a day (about SGD 1,600)", "₹25,000 a day (about SGD 400)",
   "₹2 lakh a day (about SGD 3,200)"],
  concept="UPI–PayNow linkage",
  explanation="RBI's FAQs on the UPI–PayNow linkage state a daily transaction limit of ₹60,000 (around SGD 1,000) for "
              "cross-border remittances.",
  steps=["UPI (India) ↔ PayNow (Singapore)", "Daily limit ₹60,000 ≈ SGD 1,000"],
  why="The other amounts are not the prescribed limit.",
  facts=[fact("There is a daily transaction limit of ₹60,000 in a day (equivalent to around SGD 1,000) for undertaking "
              "cross-border remittance transactions through the UPI-PayNow linkage", C_PAYNOW)])
Q(T, "Features", "Basic",
  "What makes payments using a UPI Virtual Payment Address (VPA) more secure, according to RBI's payments booklet (January 2021)?",
  ["The payer does not need the beneficiary's account or bank details",
   "Each VPA is valid for only one transaction",
   "VPA payments are settled in RBI's books in real time",
   "A VPA can be created only at a bank branch"],
  concept="Virtual Payment Address",
  explanation="RBI notes that the unique feature of VPA-based transactions is their security: they obviate the need for "
              "sharing account or bank details with the remitter. Users set their own VPA. Transfers can also be made "
              "using account number and IFSC.",
  steps=["VPA set by the user", "No sharing of account details → secure"],
  why="VPAs are reusable; UPI settles on a deferred net basis; VPAs are created in apps, not at branches.",
  facts=[fact("UPI users send and receive money using a Virtual Payment Address (VPA) set by the user; the unique feature "
              "of VPA based transaction is the secure aspect of UPI architecture as it obviates the need for sharing "
              "account or bank details", C_BOOKLET)])
Q(T, "Features", "Intermediate",
  "Third-party application providers (TPAPs) such as Google Pay and WhatsApp offer UPI payments. As described in "
  "RBI's payments booklet (January 2021), which statement about them is correct?",
  ["Only banks can connect directly to the UPI switch; TPAPs partner with a bank, which bears the operational and "
   "financial liability",
   "TPAPs connect directly to the UPI switch and bear full liability for their transactions",
   "TPAPs are licensed by RBI as payment banks before joining UPI",
   "TPAPs settle UPI transactions through their own accounts with RBI"],
  concept="Role of TPAPs in UPI",
  explanation="The UPI ecosystem is designed for banks: only a banking entity can directly interact with the UPI switch. "
              "Non-banks participate by partnering with a bank already on UPI. The entire operational and financial "
              "liability for transactions through the third-party app lies on the bank.",
  steps=["UPI switch ← banks only", "TPAP = facilitator via partner bank", "Liability on the bank"],
  why="TPAPs do not connect directly, are not licensed as payments banks for this, and do not settle with RBI.",
  facts=[fact("Only a banking entity can directly interact with the UPI switch; non-banking entities can participate by "
              "partnering with a banking entity already on the UPI platform; the entire operational and financial "
              "liability of transactions originated through third party app lies on the bank", C_BOOKLET)])
Q(T, "UPI Lite and international", "Advanced",
  "Consider the following statements about the UPI–PayNow linkage, based on RBI's FAQs:\n"
  "I. Only person-to-person remittances for 'Maintenance of Relatives Abroad' and 'Gift' are allowed, within the "
  "Liberalised Remittance Scheme limits.\n"
  "II. Apps of participating Indian banks offer an opt-in/opt-out feature for receiving remittances from Singapore.\n"
  "III. A remittance from Singapore can be received in an Indian bank account using a UPI ID registered with a "
  "different bank.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="UPI–PayNow rules",
  explanation="Only P2P remittances for maintenance of relatives abroad and gift are permitted, subject to LRS limits (I "
              "correct). There is an opt-in/opt-out feature for inward remittances (II correct). Presently, only a UPI "
              "ID registered with the same bank where the account is held can be used (III wrong).",
  steps=["I ✓", "II ✓", "III ✗ (UPI ID must be with the same bank)"],
  why="Options with III are wrong; 'I only' misses II.",
  facts=[fact("Only person to person (P2P) remittances towards 'Maintenance of Relatives Abroad' & 'Gift' under the LRS "
              "are allowed, and the LRS limits apply; there is an opt in / opt out feature in the apps of participating "
              "banks in India for receiving remittances from Singapore", C_PAYNOW),
         fact("Presently, the UPI ID registered with the same bank where account is held can only be used", C_PAYNOW)])
# ================= UPI (1 Advanced)
_val_oct, _val_sep = 31.53, 29.37            # ₹ lakh crore
_daily_oct, _daily_sep = 101707, 97913       # ₹ crore
assert round(pct(_val_oct - _val_sep, _val_sep), 1) == 7.4
assert round(pct(_daily_oct - _daily_sep, _daily_sep), 1) == 3.9
assert abs(_val_oct * 1e5 / 31 - _daily_oct) < 20 and abs(_val_sep * 1e5 / 30 - _daily_sep) < 20
assert abs((_daily_oct / _daily_sep) * (31 / 30) - _val_oct / _val_sep) < 0.001
assert 25.47 > 24.07                          # volume also rose (billion transactions)
Q("UPI", "Features", "Advanced",
  "UPI handled 25.47 billion transactions worth ₹31.53 lakh crore in October 2026, against 24.07 billion worth ₹29.37 "
  "lakh crore in September 2026. The average daily value rose from ₹97,913 crore to ₹1,01,707 crore. Why did the "
  "average daily value rise by only about 3.9% when the monthly value rose by about 7.4%?",
  ["October has 31 days against September's 30, so part of the monthly rise comes from the extra day",
   "The number of transactions fell in October, which held down the daily average",
   "Daily averages count only working days, and October had more holidays",
   "The monthly value includes UPI Lite payments, which the daily average excludes"],
  concept="Monthly totals versus daily averages",
  explanation="Monthly value rose 7.4% (29.37 → 31.53). Daily averages are monthly value ÷ days: 31.53 lakh crore ÷ 31 "
              "≈ ₹1,01,700 crore and 29.37 lakh crore ÷ 30 ≈ ₹97,900 crore, a rise of about 3.9%. The gap is the "
              "day-count effect: 1.039 × 31/30 ≈ 1.074.",
  steps=["Monthly growth = (31.53 − 29.37) ÷ 29.37 ≈ 7.4%", "Daily growth = (1,01,707 − 97,913) ÷ 97,913 ≈ 3.9%",
         "1.039 × (31 ÷ 30) ≈ 1.074 → the difference is the extra day"],
  shortcut="Growth in totals ≈ growth in daily average + growth in number of days (3.9% + 3.3% ≈ 7.4%).",
  why="Volume rose (24.07 → 25.47 billion); the daily figures match value ÷ calendar days, so no working-day or "
      "UPI Lite adjustment is involved.",
  computed=True, current=ca("2026-11-02"),
  facts=[fact("UPI recorded 25.47 billion transactions worth Rs 31.53 lakh crore in October; average daily transaction "
              "value increased to Rs 1,01,707 crore from Rs 97,913 crore in the previous month; in September 2026, UPI "
              "recorded 24.07 billion transactions worth Rs 29.37 lakh crore (published 2 November 2026)", M_UPIOCT)])

# ================= NEFT (Basic 1 / Intermediate 2 / Advanced 2)
T = "NEFT"
SUB = "Settlement and timings"
Q(T, SUB, "Basic",
  "NEFT settles in 48 half-hourly batches over 24 hours. According to RBI's payments booklet (January 2021), when do the first "
  "and the last batches of the day take place?",
  ["00:30 hours and midnight", "08:00 hours and 19:00 hours", "00:00 hours and 23:30 hours",
   "07:00 hours and 18:00 hours"],
  concept="NEFT batch timings",
  explanation="NEFT is a net-settlement system with 48 batches in 24 hours; the first batch is at 0030 hours and the "
              "last at midnight.",
  steps=["48 batches × 30 minutes = 24 hours", "First 00:30, last 24:00"],
  why="The other pairs either do not span 48 half-hour batches or start at the wrong time.",
  facts=[fact("NEFT settlement works on net-settlement in batches, with 48 batches of settlement over a span of 24 "
              "hours, the first and last batches taking place at 0030 hours and midnight, respectively", C_BOOKLET)])
Q(T, SUB, "Intermediate",
  "In RBI's payments booklet (January 2021), why does RBI describe NEFT as a 'hybrid' payment system?",
  ["It has features of both retail and large-value systems, with no floor or ceiling on amounts",
   "It settles some transactions gross and some net",
   "It is operated jointly by RBI and NPCI",
   "It accepts both paper and electronic instructions for settlement"],
  concept="NEFT as a hybrid system",
  explanation="RBI's booklet says NEFT is a unique hybrid payment system because it carries characteristics of both a "
              "retail and a large-value payment system, offering round-the-clock transfers with no floor or ceiling on "
              "amounts. Its average transaction value is about ₹10 lakh.",
  steps=["No minimum or maximum amount", "Retail + large-value features → hybrid"],
  why="NEFT settles only on a net batch basis, is owned and operated by RBI alone, and is an electronic system.",
  facts=[fact("NEFT is a unique hybrid payment system as it carries with it the characteristics of both a retail and a "
              "large value payment system, offering round the clock transfers with no floor or ceiling on the amounts; "
              "average transaction value of approximately ten lakh rupees", C_BOOKLET)])
Q(T, SUB, "Intermediate",
  "Under the Indo-Nepal Remittance Facility Scheme, which uses NEFT, how does money sent from India reach the "
  "beneficiary in Nepal?",
  ["It flows to a designated SBI branch, which transfers it to Nepal SBI Bank Ltd for disbursal in Nepalese currency",
   "It is routed through NPCI's IMPS to any bank in Nepal",
   "It is credited by RBI directly to the Nepal Rastra Bank",
   "It is paid out in Indian rupees by Indian post offices in Nepal"],
  concept="Indo-Nepal Remittance Facility",
  explanation="Launched in May 2008 under the NEFT ecosystem, the scheme is one-way (India to Nepal). The money flows to a designated SBI branch, which consolidates and transfers it to Nepal SBI Bank Ltd "
              "(NSBL); NSBL disburses it in local currency, through banks or banks plus money transfer agents.",
  steps=["NEFT → designated SBI branch → Nepal SBI Bank Ltd → beneficiary (Nepalese rupees)"],
  why="IMPS, Nepal Rastra Bank and post offices are not part of the channel.",
  facts=[fact("The money flows to a designated branch of SBI, which consolidates and transfers the amount to Nepal SBI "
              "Bank Ltd. (NSBL); NSBL disburses the remittance to beneficiaries in Nepal in the local currency", C_BOOKLET),
         fact("In Nepal, the INRF Scheme is handled by Nepal SBI Ltd. (NSBL) ... the remittance information is conveyed "
              "electronically by SBI in a secure mode to NSBL. NSBL then makes arrangements for credit to the bank "
              "account of the beneficiary ... Else, NSBL disburses funds in cash", C_INRF)])
import math
acc_per_txn, walkin_per_txn, walkin_max = 200000, 50000, 12
ram, shyam = 900000, 750000
assert math.ceil(ram / acc_per_txn) == 5
assert walkin_per_txn * walkin_max == 600000 and shyam - 600000 == 150000
Q(T, SUB, "Advanced",
  "Under RBI's current FAQs on the Indo-Nepal Remittance Facility (INRF) Scheme, Ram, who has an account with an "
  "NEFT-enabled branch, wants to send ₹9 lakh to his family in Nepal during a year, and Shyam, a walk-in customer "
  "with no account, wants to send ₹7.5 lakh in the year. What is the position?",
  ["Ram can send the full ₹9 lakh, in at least 5 remittances; Shyam can send at most ₹6 lakh",
   "Both are capped at 12 remittances of ₹50,000, so each can send at most ₹6 lakh",
   "Ram needs at least 18 remittances; Shyam can send the full ₹7.5 lakh in 15 remittances",
   "Ram can send at most ₹2 lakh in the year; Shyam can send at most ₹6 lakh"],
  concept="INRF limits for account holders and walk-in customers",
  explanation="A sender with an account at an NEFT-enabled branch can remit up to ₹2 lakh per transaction with no "
              "limit on the number of remittances, so Ram needs at least 9 ÷ 2 rounded up = 5 remittances. A walk-in "
              "customer can remit up to ₹50,000 per remittance and at most 12 remittances a year, a ceiling of ₹6 "
              "lakh, so ₹1.5 lakh of Shyam's amount cannot go through the scheme that year.",
  steps=["Account holder: ₹2 lakh per transaction, no cap on number → 9 ÷ 2 → 5 remittances",
         "Walk-in: 12 × ₹50,000 = ₹6 lakh a year → ₹1.5 lakh left over"],
  why="The ₹50,000 × 12 cap applies only to walk-in customers; ₹2 lakh is a per-transaction limit, not an annual one; "
      "18 remittances assumes the walk-in limit for Ram, and 15 remittances exceed Shyam's cap of 12.",
  computed=True,
  facts=[fact("One can remit upto ₹2 lakhs per transaction to the beneficiary residing in Nepal; provided the sender "
              "maintains account with any NEFT enabled bank branch in India. Walk-in / Non-customer can remit upto "
              "₹50,000 per transaction ... There is no limit on remittances if the sender is maintaining account with "
              "any NEFT enabled bank-branch in India. Walk-in / Non-customers are allowed to remit 12 remittances in a "
              "year with ceiling of ₹50,000 per remittance", C_INRF)])
Q(T, SUB, "Advanced",
  "Consider the following statements based on RBI's NEFT FAQs and payments booklet:\n"
  "I. An optional field (tag 7495) in the NEFT message carries additional sender-to-receiver information, which "
  "destination banks should store and give the customer on request.\n"
  "II. If a NEFT transaction is returned, the originating bank must show 'NEFT-Return' in the remitter's passbook or "
  "statement.\n"
  "III. NEFT transactions are settled one by one on a gross basis in RBI's books.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II only", "II and III only", "I, II and III"],
  concept="NEFT messaging and settlement",
  explanation="Tag 7495 is an optional field for sender-to-receiver information that destination banks should capture and "
              "provide on request (I correct). Returned transactions are shown as 'NEFT-Return' to the originator (II "
              "correct). NEFT settles on a net basis in half-hourly batches; gross settlement is RTGS (III wrong).",
  steps=["I ✓", "II ✓", "III ✗ (net batch settlement)"],
  why="Options with III are wrong; 'II only' misses I.",
  facts=[fact("There is an optional field with tag 7495 in NEFT payment message that enables inclusion of additional "
              "sender-to-receiver information; destination banks should capture and store this information to be "
              "provided to the customer on request; the originating bank shall provide the description 'NEFT-Return' in "
              "the pass book / account statement of the originator whose NEFT transaction is returned", C_NEFT),
         fact("NEFT settlement works on net-settlement in batches, with 48 batches of settlement over 24 hours",
              C_BOOKLET)])

# ================= RTGS (Basic 1 / Intermediate 1 / Advanced 1)
T = "RTGS"
SUB = "Limits and timings"
Q(T, SUB, "Basic",
  "According to RBI's payments booklet (January 2021), besides individual customer and inter-bank payments, RTGS also settles "
  "Multilateral Net Settlement Batch (MNSB) files. From which kind of systems do these files come?",
  ["Ancillary payment systems such as CCIL and NPCI", "Foreign central banks", "State treasuries",
   "Stock exchanges' trading terminals"],
  concept="RTGS as the settlement backbone",
  explanation="RBI's booklet says RTGS settles transactions in real time on a gross basis in RBI's books and also "
              "settles MNSB files emanating from ancillary payment systems such as CCIL and NPCI.",
  steps=["Ancillary systems (CCIL, NPCI) net their members' positions", "Net positions settled through RTGS"],
  why="Foreign central banks, State treasuries and exchange terminals do not send MNSB files to RTGS.",
  facts=[fact("RTGS also settles Multilateral Net Settlement Batch (MNSB) files emanating from ancillary payment "
              "systems such as CCIL and NPCI", C_BOOKLET)])
Q(T, SUB, "Intermediate",
  "As described in RBI's payments booklet (January 2021), RTGS had four types of participants. In which category were Primary "
  "Dealers placed?",
  ["Restricted participant", "Regular participant", "Clearing house", "Central bank participant"],
  concept="Types of RTGS participants",
  explanation="RBI lists four types: central bank (RBI only), regular participant (all facilities, e.g. banks), "
              "restricted participant (only particular facilities, e.g. Primary Dealers) and clearing house (for MNSB "
              "settlement).",
  steps=["RBI → central bank", "Banks → regular", "Primary Dealers → restricted", "MNSB settlement → clearing house"],
  why="Regular participation is for banks; the clearing house and central bank categories are for other entities.",
  facts=[fact("There are primarily four types of participants in RTGS viz. (i) central bank - exclusively for RBI (ii) "
              "regular participant - e.g. banks (iii) restricted participant - e.g. Primary Dealers and (iv) clearing "
              "house for settlement of MNSB file", C_BOOKLET)])
Q(T, SUB, "Advanced",
  "Consider the following statements about the intraday liquidity (IDL) facility that RBI gave RTGS members, as "
  "described in RBI's payments booklet (January 2021):\n"
  "I. IDL carries interest at the Bank Rate for the hours it is used.\n"
  "II. IDL is extended against fully collateralised Indian government securities held in the member's IDL-SGL "
  "account.\n"
  "III. IDL availed is reversed automatically by the RTGS system when the member's settlement account has sufficient "
  "funds above a threshold.\n"
  "Which of the above is/are correct?",
  ["II and III only", "I and II only", "III only", "I, II and III"],
  concept="Intraday liquidity in RTGS",
  explanation="IDL is extended free of interest (I wrong) against fully collateralised government securities in the "
              "IDL-SGL account (II correct). It is invoked automatically when funds are short and reversed automatically "
              "once sufficient funds are available (III correct). IDL not reversed by end of day attracts penal "
              "interest.",
  steps=["I ✗ (interest-free)", "II ✓", "III ✓"],
  why="Options with I are wrong; 'III only' misses II.",
  facts=[fact("Liquidity risks in RTGS are managed through IDL extended to members by RBI against fully collateralised "
              "Indian government securities held by the members in their IDL-SGL account; IDL is extended free of "
              "interest and has to be reversed by the end of the day", C_BOOKLET),
         fact("IDL facility availed by a participant is automatically reversed by the RTGS system on availability of "
              "sufficient funds in the settlement account of the participant (above a threshold level)", C_BOOKLET)])

# ================= IMPS (Basic 1 / Intermediate 1)
T = "IMPS"
SUB = "Limits and features"
Q(T, SUB, "Basic",
  "According to RBI's payments booklet (January 2021), at what point does NPCI route an IMPS transaction to the beneficiary "
  "bank?",
  ["Only after the remitting bank has debited the remitter's account",
   "Before the remitter's account is debited, to save time",
   "Only after RBI has settled the transaction gross",
   "Only after the beneficiary accepts the payment request"],
  concept="IMPS transaction flow",
  explanation="A transaction reaches NPCI for routing only after the remitting bank has debited the customer's account, "
              "which addresses the risk of a remittance without adequate funds. The beneficiary is credited on receipt "
              "of the message; inter-bank settlement happens later on a net basis.",
  steps=["Debit remitter", "NPCI routes to beneficiary bank", "Credit beneficiary; net settlement later"],
  why="Debit comes first; settlement is deferred net, not gross before credit; IMPS is a push payment.",
  facts=[fact("In IMPS, a transaction is received at NPCI for routing to beneficiary bank / PPI only after the remitting "
              "bank has debited the remitting customer's account; therefore the risk of a remittance being made without "
              "adequate funds is addressed", C_BOOKLET)])
Q(T, SUB, "Intermediate",
  "IMPS originally needed both remitter and beneficiary to register for mobile banking. According to RBI's payments booklet (January 2021), "
  "after it was upgraded, besides account number and IFSC, which other parameter could be used to send funds?",
  ["The beneficiary's bank account-linked Aadhaar number", "The beneficiary's PAN",
   "The beneficiary's passport number", "The beneficiary's GSTIN"],
  concept="IMPS addressing options",
  explanation="RBI's booklet notes that IMPS was upgraded to allow remittances using account number and IFSC (like NEFT) "
              "or using the bank account-linked Aadhaar number.",
  steps=["Original: mobile banking registration for both", "Upgrade: account + IFSC, or account-linked Aadhaar number"],
  why="PAN, passport and GSTIN are not IMPS payment addresses.",
  facts=[fact("The system was upgraded to enable remittance of funds by using other parameters such as account number "
              "and IFSC (like NEFT) or by using bank account linked Aadhaar number", C_BOOKLET)])

# ================= NPCI (Basic 3 / Intermediate 3 / Advanced 3)
T = "NPCI"
SUB = "Products: NACH, AePS, RuPay, FASTag"
Q(T, SUB, "Basic",
  "Since when has the Aadhaar Enabled Payment System (AePS) been operational?",
  ["January 2011", "December 2008", "August 2016", "March 2004"],
  concept="AePS",
  explanation="AePS has been operational since January 2011. It allows interoperable transactions at micro-ATMs through "
              "BCs of any bank using Aadhaar authentication.",
  steps=["AePS → January 2011"],
  why="December 2008 is NPCI's incorporation, August 2016 UPI's launch and March 2004 RTGS's start.",
  facts=[fact("AePS is operational since January 2011. It allows online interoperable transactions at Micro-ATM through "
              "the BCs of any bank using Aadhaar authentication", C_BOOKLET)])
Q(T, SUB, "Basic",
  "According to RBI's payments booklet (January 2021), FASTags used for toll payments under NPCI's NETC system were issued by "
  "banks and by which other entity?",
  ["Indian Highways Management Company Limited (IHMCL)", "National Highways Authority of India's toll contractors",
   "Regional Transport Offices", "NPCI International Payments Ltd"],
  concept="FASTag issuance",
  explanation="A FASTag is issued by a bank or by IHMCL and affixed on the vehicle. It is linked to a payment instrument "
              "such as a bank account, non-bank PPI, card or UPI.",
  steps=["Issuer: bank or IHMCL", "Linked to account / PPI / card / UPI"],
  why="Toll contractors, RTOs and NIPL do not issue FASTags.",
  facts=[fact("The FASTag, issued by a bank or the Indian Highways Management Company Limited (IHMCL) and affixed on the "
              "vehicle, is linked to an underlying payment instrument - bank account, non-bank PPIs, cards, UPI, etc.",
              C_BOOKLET)])
Q(T, SUB, "Basic",
  "When the Bharat Bill Payment System began, five mandatory biller categories were allowed. Which of the following "
  "was NOT one of them?",
  ["Insurance premium", "Electricity", "Direct-to-Home (DTH)", "Water"],
  concept="BBPS biller categories",
  explanation="The initial five mandatory categories were electricity, water, gas, telecom (landline, mobile post-paid, "
              "broadband) and DTH. Other recurring billers were added later.",
  steps=["Initial five: electricity, water, gas, telecom, DTH"],
  why="Electricity, DTH and water were among the initial five.",
  facts=[fact("Initially, five mandatory biller categories were allowed under BBPS, viz., electricity, water, gas, "
              "telecom (landline, mobile post-paid, broadband) and Direct-to-Home (DTH)", C_BOOKLET)])
Q(T, SUB, "Intermediate",
  "According to RBI's payments booklet (January 2021), which two activities had been NPCI's main sources of revenue, enabling "
  "it to invest in new systems?",
  ["Operating the Cheque Truncation System and managing the National Financial Switch",
   "Issuing RuPay credit cards and operating FASTag toll plazas",
   "Running UPI apps and charging merchants MDR on UPI",
   "Managing RTGS and NEFT on behalf of RBI"],
  concept="NPCI's revenue base",
  explanation="NPCI was entrusted with operating CTS on behalf of RBI in December 2013 and took over NFS from IDRBT in "
              "December 2009. RBI notes these two activities are NPCI's main revenue source.",
  steps=["CTS (since 2013) + NFS (since 2009) → main revenue"],
  why="NPCI does not issue cards, run toll plazas or UPI apps; RTGS and NEFT are owned and operated by RBI.",
  facts=[fact("In December 2013, NPCI was entrusted with the task of operating CTS on behalf of RBI; it also took over "
              "NFS from IDRBT in December 2009; these two activities are the main revenue source for NPCI", C_BOOKLET)])
Q(T, SUB, "Intermediate",
  "In September 2019, RBI widened the scope of the Bharat Bill Payment System. Which billers became eligible to "
  "participate?",
  ["All categories of billers raising recurring bills, except prepaid recharges, on a voluntary basis",
   "Only government utilities, on a mandatory basis",
   "All billers including prepaid mobile recharges, on a mandatory basis",
   "Only billers with annual collections above ₹100 crore"],
  concept="Expansion of BBPS",
  explanation="On 16 September 2019 the scope of BBPS was enhanced to include, as eligible participants, all categories "
              "of billers who raise recurring bills (except prepaid recharges), on a voluntary basis.",
  steps=["2017: five mandatory categories", "Sept 2019: all recurring billers (not prepaid recharges), voluntary"],
  why="It was not restricted to government utilities or large billers, and prepaid recharges were excluded.",
  facts=[fact("BBPS was extended in September 2019 to include as eligible participants all categories of billers, on a "
              "voluntary basis, who raise recurring bills (except prepaid recharges)", C_BOOKLET)])
Q(T, SUB, "Intermediate",
  "As described in RBI's payments booklet (January 2021), the Aadhaar Payments Bridge System (APBS), used to credit government "
  "subsidies to Aadhaar-linked accounts, is a component of which NPCI system?",
  ["National Automated Clearing House (NACH)", "National Financial Switch (NFS)",
   "Immediate Payment Service (IMPS)", "National Electronic Toll Collection (NETC)"],
  concept="APBS within NACH",
  explanation="APBS, implemented in 2012, is a component of NACH. NACH identifies destination accounts by account "
              "number, IFSC or MICR, and also by Aadhaar number through its APBS leg; NACH is the most prominent mode of "
              "DBT credits.",
  steps=["APBS = Aadhaar-based leg of NACH", "Used for DBT credits"],
  why="NFS is the ATM switch, IMPS is for instant transfers and NETC for tolls.",
  facts=[fact("APBS, a component of NACH, which uses Aadhaar number for electronic crediting of government subsidies and "
              "benefits in Aadhaar-linked bank account, was implemented in 2012", C_BOOKLET)])
rupay_total, rupay_credit = 60.36e7, 9.7e5
share = pct(rupay_credit, rupay_total)
assert round(share, 2) == 0.16
Q(T, SUB, "Advanced",
  "As on 30 November 2020, about 60.36 crore RuPay cards had been issued, of which only 9.7 lakh were credit cards. "
  "Roughly what share of RuPay cards were credit cards?",
  ["About 0.16%", "About 1.6%", "About 9.7%", "About 16%"],
  concept="Share computation: lakh and crore",
  explanation="1 crore = 100 lakh, so 60.36 crore = 6,036 lakh. Share = 9.7 ÷ 6,036 × 100 ≈ 0.16%. Most RuPay cards "
              "were debit cards (including those issued for BSBD/PMJDY accounts).",
  steps=["60.36 crore = 6,036 lakh", "9.7 ÷ 6,036 = 0.0016", "≈ 0.16%"],
  why="1.6% and 16% misplace the decimal by factors of 10 and 100; 9.7% mistakes the count for a percentage.",
  computed=True, shortcut="9.7 lakh ÷ 60 crore ≈ 10 ÷ 6,000 ≈ 0.17%",
  facts=[fact("As on November 30, 2020, with about 60.36 crore RuPay cards issued by nearly 1,158 banks, the market share "
              "of RuPay has increased to more than 60%; a significant proportion is debit cards, with only 9.7 lakh "
              "credit cards issued", C_BOOKLET)])
Q(T, SUB, "Advanced",
  "Consider the following statements about NACH, as described in RBI's payments booklet (January 2021):\n"
  "I. Besides paper mandates, paperless mandates can be created electronically for NACH debits.\n"
  "II. NACH Credit is used to collect insurance premiums from many policyholders into one account.\n"
  "III. Schemes such as PM-KISAN were rolled out using the NACH platform.\n"
  "Which of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I only"],
  concept="NACH Credit and NACH Debit",
  explanation="NACH works on customer mandates, which can be paper or paperless (I correct). NACH Credit is one-to-many "
              "(dividends, salaries, subsidies); collecting premiums from many accounts is NACH Debit (II wrong). Social "
              "schemes such as PM-KISAN, PM-SYM and PM-KMY were rolled out using NACH (III correct).",
  steps=["I ✓", "II ✗ (that is NACH Debit)", "III ✓"],
  why="Options with II are wrong; 'I only' misses III.",
  facts=[fact("NACH works on the strength of mandates given by customers; apart from paper mandates, paperless mandates "
              "can also be created electronically; NACH Debit collects from many accounts to one destination account, "
              "e.g. insurance premium", C_BOOKLET),
         fact("Many social schemes such as PM-KISAN, PMSYMY, PMLVMY and PMKMY were rolled out using NACH platform",
              C_BOOKLET)])
Q(T, SUB, "Advanced",
  "Consider the following statements about the Centralised Positive Pay System (CPPS) for cheques:\n"
  "I. If the cheque presented does not match the data, the clearing house automatically returns it unpaid.\n"
  "II. Member banks upload the details of issued cheques given by their customers to NPCI's CPPS.\n"
  "III. The facility was implemented from 1 January 2021.\n"
  "Which of the above is/are correct?",
  ["II and III only", "I and II only", "I and III only", "I, II and III"],
  concept="Positive Pay through NPCI's CPPS",
  explanation="Customers give details of issued cheques to their bank, which uploads them to NPCI's CPPS (II correct). On "
              "presentment the clearing house validates against CPPS and, on mismatch, puts a specified flag on the "
              "cheque data; it does not itself return the cheque (I wrong). The facility was implemented from 1 January "
              "2021 (III correct).",
  steps=["I ✗ (a flag is put; the drawee bank decides)", "II ✓", "III ✓"],
  why="Options with I are wrong.",
  facts=[fact("In the Centralised Positive Pay System, customers provide details of issued instruments to their banks; "
              "the data will be uploaded in NPCI's CPPS system by the member bank; if any difference is observed, the "
              "clearing house will put a specified flag with the cheque data; the facility was implemented from January "
              "01, 2021", C_BOOKLET),
         fact("Under Positive Pay, the issuer of the cheque submits electronically ... certain minimum details of that "
              "cheque ... to his bank, details of which are cross checked with the presented cheque by CTS. Any "
              "discrepancy is flagged by CTS to the drawee bank and presenting bank, who would take redressal measures",
              C_CHQ)])
# ---- sources (group D); every URL below was fetched and read on 2026-11-06 (scratch copies in D\pages)
D_RDG = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id=145"                 # RBI Retail Direct FAQs
D_SGB = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id=109"                 # Sovereign Gold Bond FAQs
D_DEMAT2 = "https://www.sebi.gov.in/sebi_data/attachdocs/sep-2026/1789039783353.pdf"   # SEBI PR 56/2026
D_SEBI_MAR26 = "https://www.sebi.gov.in/sebi_data/attachdocs/mar-2026/1774268916433.pdf"  # SEBI PR 18/2026
D_SEBI_FNO = "https://www.sebi.gov.in/sebi_data/attachdocs/aug-2026/1787236407005.pdf"    # SEBI PR 50/2026
D_SCORES = "https://investor.sebi.gov.in/sebi_scores.html"
D_NIFTY = ("https://businesstoday.in/markets/stocks/story/bse-to-replace-wipro-in-nifty-50-index-from-september-30-"
           "all-you-need-to-know-558467-2026-09-29")
D_NIFTY2 = ("https://upstox.com/news/market-news/stocks/bse-to-replace-wipro-in-nifty-50-how-index-reshuffles-impact-"
            "stock-prices/article-200747/")
D_DSII = ("https://taxguru.in/corporate-law/irdai-releases-fy-2025-26-list-domestic-systemically-important-insurers-"
          "d-slls.html")
D_INDAS = "https://www.taxmann.com/post/blog/irdai-amendment-ind-as-reporting-for-insurers/"
D_CIO = "https://cioins.co.in/Faqs"
D_PMSBY = "https://financialservices.gov.in/pmsby"
D_PMJJBY = "https://financialservices.gov.in/pmjjby"
D_AMFI = "https://www.amfiindia.com/aboutamfi"
D_CHHOTI = "https://assets.zerodhafundhouse.com/addendums/addendums/Addendum%20No.%2004%20-%202025-26.pdf"
D_MFREG = ("https://www.businesstoday.in/mutual-funds/story/sebi-overhauls-mutual-fund-rules-changes-made-to-ter-"
           "framework-check-details-507113-2025-12-17")
D_BUDGET = "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc202621776101.pdf"
D_ES_BANK = "https://www.deccanchronicle.com/business/scbs-improve-recovery-rate-in-npas-to-262-1933672"
D_ES_UP = ("https://upstox.com/news/market-news/latest-updates/economic-survey-2025-26-pegs-6-8-7-2-gdp-growth-multi-"
           "decade-low-np-as-strong-primary-markets-key-highlights/article-188528")
D_PMMY = "https://financialservices.gov.in/pradhan-mantri-mudra-yojana-pmmy"
D_APY = "https://financialservices.gov.in/atal-pension-yojana-apy"
D_CG_WOMEN = ("https://www.cgtmse.in/Default/ViewFile/?id=1734171815262_Circular%20241-%20enhancement%20in%20extent%20"
              "of%20coverage%20for%20women%20entrepreneurs%5B90%5D.pdf&path=Circular")
D_CG_AGF = ("https://www.cgtmse.in/Default/ViewFile/?id=1680282382939_Circular%20No.%20221_Reduction%20in%20AGF.pdf"
            "&path=Circular")
D_ECLGS5 = "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/sep/doc_9802_20260905_10264701.pdf"

D_BD = ca("2026-02-01")      # Union Budget 2026-27 presented
D_ES = ca("2026-01-29")      # Economic Survey 2025-26 tabled (Thursday, 29 January, per the Upstox report)

# ================= Financial Markets (Basic 1 / Intermediate 2 / Advanced 2)
T = "Financial Markets"
S = "Structure and regulators"
Q(T, S, "Basic",
  "Under the RBI Retail Direct Scheme, how can an individual with a Retail Direct Gilt (RDG) account buy dated "
  "government securities in a primary auction?",
  ["Only by bidding in the non-competitive segment, without quoting a price",
   "Only by quoting a competitive price bid through the portal",
   "Only through a primary dealer acting as her broker",
   "Only after the auction, at the cut-off yield set by RBI"],
  concept="RBI Retail Direct",
  explanation="The Retail Direct portal lets individuals buy G-secs in primary auctions in the non-competitive segment "
              "only: the investor enters only the amount, not a price. A competitive bid can be placed only through a "
              "bank, primary dealer or other authorised institution.",
  steps=["RDG account → primary auction → non-competitive segment only"],
  why="Competitive bids are not allowed on the portal; no primary dealer is needed, since the account is held directly "
      "with RBI; there is no post-auction purchase at a cut-off yield.",
  facts=[fact("The Scheme is designed to facilitate only Non-competitive participation (i.e., bids without choosing your "
              "own price) by individuals; to place a competitive bid one may contact a Bank/Primary Dealer", D_RDG)])
Q(T, S, "Intermediate",
  "According to RBI's Retail Direct FAQs, on which days of the week are primary auctions of Government of India dated "
  "securities and of State Development Loans (SDLs) usually held?",
  ["Dated G-secs on Fridays; SDLs on Tuesdays", "Dated G-secs on Wednesdays; SDLs on Fridays",
   "Dated G-secs on Tuesdays; SDLs on Thursdays", "Both on Mondays, after the weekly calendar is issued"],
  concept="Primary auction calendar",
  explanation="RBI's table lists the usual auction days: T-bills on Wednesdays, dated G-secs on Fridays and SDLs on "
              "Tuesdays (SGBs in windows announced by press release). Days may change for holidays.",
  steps=["T-bills: Wednesday", "Dated G-sec: Friday", "SDL: Tuesday"],
  why="Wednesday is the T-bill day; the other day combinations do not match RBI's table.",
  facts=[fact("Primary auction usually held on: T-Bills - Wednesdays; dated G-Sec - Fridays; State Development Loans - "
              "Tuesdays", D_RDG)])
Q(T, S, "Intermediate",
  "How is the nominal (issue) value of a Sovereign Gold Bond fixed, according to RBI's SGB FAQs?",
  ["On the simple average closing price of 999-purity gold published by IBJA for the last 3 business days of the "
   "week before the subscription period",
   "On the London Bullion Market Association's afternoon fix on the day before issue",
   "On the closing price of gold futures on MCX on the opening day of subscription",
   "On RBI's own reference rate for gold, announced on the issue date"],
  concept="Pricing of Sovereign Gold Bonds",
  explanation="The nominal value is in rupees, fixed on the simple average of the closing price of 999-purity gold "
              "published by the India Bullion and Jewellers Association for the last three business days of the week "
              "preceding the subscription period. Redemption uses the same IBJA average for the 3 business days before "
              "repayment.",
  steps=["Source = IBJA, 999 purity", "Average of last 3 business days of the preceding week"],
  why="LBMA, MCX futures and an 'RBI reference rate for gold' are not the basis RBI states.",
  facts=[fact("The nominal value of Gold Bonds shall be in Indian Rupees fixed on the basis of simple average of closing "
              "price of gold of 999 purity, published by the India Bullion and Jewelers Association Limited, for the "
              "last 3 business days of the week preceding the subscription period", D_SGB)])

units, charged, allotted = 2000, 99.40, 99.15
refund = round((charged - allotted) * units, 2)
assert refund == 500.0
Q(T, S, "Advanced",
  "Through RBI Retail Direct, Neha bids for ₹2,00,000 face value (2,000 units of ₹100) of a dated G-sec in the "
  "primary auction. She funds the bid at ₹99.40 per unit (indicative price plus mark-up), besides accrued interest. "
  "The securities are allotted at ₹99.15 per unit. What happens to the excess, under RBI's FAQs?",
  ["₹500 is refunded to her linked bank account within two business days of the auction",
   "₹800 is refunded, being the whole mark-up, within two business days",
   "₹500 is retained by RBI as the fee for using the portal",
   "₹300 is refunded at maturity, along with the last coupon"],
  concept="Non-competitive allotment and mark-up",
  explanation="Non-competitive bids are allotted at the weighted average price of the successful competitive bids, "
              "which is unknown while bidding, so a mark-up is collected. The excess (price charged minus allotment "
              "price) is refunded to the linked bank account within two business days of the auction. Excess = "
              "(99.40 − 99.15) × 2,000 = ₹500.",
  steps=["Excess per unit = 99.40 − 99.15 = ₹0.25", "× 2,000 units = ₹500", "Refund within 2 business days"],
  why="Not the whole mark-up is refunded, only the excess over the allotment price; the mark-up is not an RBI fee; "
      "the refund is not deferred to maturity.",
  computed=True,
  facts=[fact("At the weighted average price of the successful bids in the auction; markup is not a fee charged by RBI",
              D_RDG),
         fact("The excess markup, i.e., the price charged at the time of placing the bid, minus the actual allotment "
              "price, will be refunded to your linked bank account within two business days from the date of auction",
              D_RDG)])
Q(T, S, "Advanced",
  "Consider the following statements about 'Demat 2.0', SEBI's pilot for tokenised corporate bonds announced in "
  "September 2026:\nI. The bonds are tokens on a distributed ledger owned by the depositories, and the funds leg "
  "settles atomically in RBI's wholesale CBDC through its Unified Market Interface.\nII. SEBI described India as the "
  "first country to issue corporate bonds natively on a distributed ledger with ownership recorded by its statutory "
  "depositories and funds settled in CBDC.\nIII. Investors must open a separate token account and complete fresh KYC "
  "to hold these bonds.\nWhich of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="Tokenisation of corporate bonds",
  explanation="Under Demat 2.0 the bond is a digital token on a DLT ledger owned by the depositories, linked to RBI's "
              "wholesale e₹ through the Unified Market Interface for atomic settlement (I). SEBI called India the first "
              "country to issue corporate bonds natively on DLT with ownership held by statutory depositories and the "
              "funds leg in CBDC (II). Tokenised bonds sit in the investor's existing demat account, with no separate "
              "account and no fresh KYC, so III is wrong. REC was the first issuer, on 7 September 2026.",
  steps=["I: DLT + wholesale e₹ via UMI → true", "II: SEBI's 'first country' claim → true",
         "III: existing demat account, no fresh KYC → false"],
  why="Any option including III is wrong; 'I only' leaves out II, which is stated in the release.",
  current=ca("2026-09-10"),
  facts=[fact("Demat 2.0 is connected to RBI's wholesale CBDC (e₹) through Unified Market Interface (UMI) of RBI. This "
              "enables atomic settlement; the ledger is owned by the depositories", D_DEMAT2),
         fact("India is the first country in which corporate bonds have been issued natively on a distributed ledger, "
              "with the record of ownership held by a country's statutory depositories and the funds leg settled in "
              "central bank digital currency", D_DEMAT2),
         fact("Tokenised bonds are held in the investor's existing demat account, with no separate account to open and "
              "no fresh KYC", D_DEMAT2)])

# ================= Capital Market (Basic 4 / Intermediate 1 / Advanced 2)
T = "Capital Market"
Q(T, "SEBI", "Basic",
  "Under SCORES 2.0, the upgraded version of SEBI's complaints redress system introduced in April 2024, within what "
  "time must a regulated entity redress an investor complaint?",
  ["21 calendar days", "30 calendar days", "45 days", "15 working days"],
  concept="SEBI Complaints Redress System (SCORES)",
  explanation="SCORES 2.0 cut the timeline for redressal of investor complaints to 21 calendar days from 30 calendar "
              "days, with auto-routing to the entity, auto-escalation and two levels of review (designated body, then "
              "SEBI).",
  steps=["Old timeline 30 days → SCORES 2.0: 21 calendar days"],
  why="30 days was the earlier limit; 45 days and 15 working days are not the SCORES timeline (15 days is the window "
      "for seeking a review after the ATR).",
  facts=[fact("The timeline for redressal of investor complaints has been reduced to 21 calendar days from 30 calendar "
              "days", D_SCORES)])
Q(T, "SEBI", "Basic",
  "To widen retail participation on the Social Stock Exchange, SEBI's Board on 23 March 2026 reduced the minimum "
  "investment by an individual in a Social Impact Fund of an AIF to:",
  ["₹1,000, from ₹2 lakh", "₹10,000, from ₹1 lakh", "₹25,000, from ₹2 lakh", "₹1 lakh, from ₹10 lakh"],
  concept="Social Impact Funds and the Social Stock Exchange",
  explanation="At its 213th meeting the Board cut the minimum for individual investors in a Social Impact Fund to "
              "₹1,000 from ₹2 lakh, aligning it with the minimum application size for Zero Coupon Zero Principal "
              "instruments.",
  steps=["213th meeting, 23 March 2026", "₹2 lakh → ₹1,000"],
  why="The other pairs are not the amounts approved.",
  current=ca("2026-03-23"),
  facts=[fact("The Board approved amendments to SEBI (AIF) Regulations, 2012 to reduce the minimum value of investment "
              "by individual investors in Social Impact Fund of AIF to rupees one thousand from existing rupees two "
              "lakhs", D_SEBI_MAR26)])
Q(T, "Indices", "Basic",
  "In the semi-annual rebalancing of the Nifty 50 effective 30 September 2026, which company entered the index in "
  "place of Wipro?",
  ["BSE Ltd", "TVS Motor Company", "Hitachi Energy India", "Vodafone Idea"],
  concept="Index reconstitution",
  explanation="BSE Ltd, India's oldest stock exchange, replaced Wipro in the Nifty 50 from 30 September 2026; Wipro "
              "moved out after nearly three decades. Its six-month average free-float market capitalisation was "
              "₹1,40,879 crore.",
  steps=["Nifty 50, September 2026: BSE in, Wipro out"],
  why="TVS Motor was discussed as a candidate but did not qualify; neither it nor the other two companies replaced "
      "Wipro in the Nifty 50.",
  current=ca("2026-09-30"),
  facts=[fact("India's oldest stock exchange, BSE Ltd, will enter the NSE's benchmark Nifty 50 index, replacing IT major "
              "Wipro Ltd; the changes will come into effect from September 30, 2026", D_NIFTY),
         fact("In the current rejig, BSE is included in the benchmark NIFTY50 index, replacing Wipro", D_NIFTY2)])
Q(T, "SEBI", "Basic",
  "According to SEBI's study released in August 2026, what share of individual traders in the equity derivatives "
  "segment incurred losses in FY26?",
  ["87.7%", "50.3%", "70.0%", "97.0%"],
  concept="Retail participation in F&O",
  explanation="SEBI's study found that 87.7% of individual traders lost money in FY26, although aggregate net losses "
              "fell to about ₹91,685 crore from about ₹1.12 lakh crore in FY25; about 92% of losses came from options.",
  steps=["FY26: 87.7% of individual F&O traders were loss-making"],
  why="The other figures are not the study's loss share (97% is roughly the share of traders who mainly bought "
      "options).",
  current=ca("2026-08-20"),
  facts=[fact("Despite lower aggregate losses, 87.7% of individual traders continued to incur losses during FY26",
              D_SEBI_FNO)])
Q(T, "Primary and secondary market", "Intermediate",
  "SEBI's Board decided on 23 March 2026 to permit net settlement of funds for Foreign Portfolio Investors (FPIs) in "
  "the cash market. Which transactions does the netting cover?",
  ["Outright transactions only, i.e., securities in which the FPI either buys or sells, but not both, in a settlement "
   "cycle",
   "All FPI transactions, with securities also settled on a net basis",
   "Only intraday transactions in which the FPI buys and sells the same security",
   "Only transactions in government securities and corporate bonds"],
  concept="FPI settlement",
  explanation="FPIs settle with custodians on a gross basis, raising funding costs. SEBI permitted net settlement of "
              "funds for outright transactions only (purchase or sale, not both, in a security in a cycle); securities "
              "settle gross and STT/stamp duty stay on delivery basis. Implementation is due by 31 December 2026.",
  steps=["Funds leg netted", "Only for outright trades", "Securities leg stays gross"],
  why="Securities are not netted; non-outright (buy-and-sell) trades stay gross; the measure is for the equity cash "
      "market, not debt.",
  current=ca("2026-03-23"),
  facts=[fact("Decided to permit net settlement of funds for outright transactions done by FPIs in cash market, i.e., "
              "transactions in which there is either purchase or sale transactions, but not both, in a security in a "
              "settlement cycle; settlement of securities shall continue on a gross basis", D_SEBI_MAR26)])

buy_a, sell_b, c_each = 150, 100, 40
gross_now = buy_a + c_each
net_new = (buy_a - sell_b) + c_each
assert gross_now == 190 and net_new == 90
Q(T, "Primary and secondary market", "Advanced",
  "In one settlement cycle an FPI buys shares of A worth ₹150 crore and sells shares of B worth ₹100 crore (both "
  "outright), and also buys and sells shares of C worth ₹40 crore each. Once SEBI's March 2026 net settlement of "
  "funds is implemented, what is the FPI's funds pay-in obligation, compared with the present gross system?",
  ["₹90 crore, against ₹190 crore now", "₹50 crore, against ₹190 crore now", "₹90 crore, against ₹150 crore now",
   "₹10 crore, against ₹290 crore now"],
  concept="Net settlement of funds for outright FPI trades",
  explanation="Only outright trades are netted: A's purchase (₹150 crore) is set off against B's sale proceeds "
              "(₹100 crore), leaving ₹50 crore. C, bought and sold in the same cycle, is not outright and settles gross: "
              "₹40 crore pay-in (and ₹40 crore pay-out). Pay-in = 50 + 40 = ₹90 crore. Under gross settlement today the "
              "FPI pays in for every purchase: 150 + 40 = ₹190 crore.",
  steps=["Outright net: 150 − 100 = 50", "C gross pay-in: 40", "New pay-in = 90; current = 150 + 40 = 190"],
  why="₹50 crore wrongly nets C too; ₹150 crore ignores C's purchase in the gross case; ₹10 crore/₹290 crore have no "
      "basis.",
  computed=True, current=ca("2026-03-23"),
  facts=[fact("After implementation of netting, the FPI would only need to deliver stock B but the pay-in for purchase of "
              "stock A would be adjusted against the proceeds from sale of stock B; non-outright transactions will "
              "continue to be confirmed and settled on a gross basis", D_SEBI_MAR26)])

wipro, bse = 55930, 140879
threshold = 1.5 * wipro
assert threshold == 83895 and round(bse / wipro, 1) == 2.5
Q(T, "Indices", "Advanced",
  "For the September 2026 Nifty 50 rebalancing, a non-constituent could replace an index stock only if its six-month "
  "average free-float market capitalisation was at least 1.5 times that of the smallest constituent. Wipro, the "
  "smallest, had ₹55,930 crore and BSE Ltd had ₹1,40,879 crore. What was the qualifying threshold, and how many "
  "times Wipro's figure was BSE's?",
  ["₹83,895 crore; about 2.5 times", "₹55,930 crore; about 2.5 times", "₹83,895 crore; about 1.5 times",
   "₹93,919 crore; about 1.7 times"],
  concept="Replacement rule in index rebalancing",
  explanation="Threshold = 1.5 × 55,930 = ₹83,895 crore. BSE's ₹1,40,879 crore ÷ 55,930 ≈ 2.5 times, comfortably "
              "above 1.5 times, so BSE entered and Wipro left. TVS Motor and Divi's did not qualify against the next "
              "smallest constituents.",
  steps=["1.5 × 55,930 = 83,895", "1,40,879 ÷ 55,930 ≈ 2.52"],
  why="₹55,930 crore omits the 1.5 factor; 1.5 times is the rule, not BSE's ratio; ₹93,919 crore divides BSE's figure "
      "by 1.5.",
  computed=True, current=ca("2026-09-30"),
  facts=[fact("BSE's six-month average free-float market capitalisation stood at Rs 1,40,879 crore. This is at least 1.5 "
              "times the six-month average free-float market capitalisation of the smallest constituent in the "
              "eligible universe, Wipro, whose average free-float market capitalisation stood at Rs 55,930 crore",
              D_NIFTY)])

# ================= Insurance (Basic 1 / Intermediate 2 / Advanced 3)
T = "Insurance"
Q(T, "IRDAI", "Basic",
  "Which insurers did IRDAI identify as Domestic Systemically Important Insurers (D-SIIs) for FY 2025-26, in April "
  "2026?",
  ["LIC, The New India Assurance Company and General Insurance Corporation of India",
   "LIC, SBI Life Insurance and HDFC Life Insurance",
   "The New India Assurance, ICICI Lombard and Agriculture Insurance Company",
   "LIC and GIC Re only"],
  concept="Domestic Systemically Important Insurers",
  explanation="IRDAI's press release of 2 April 2026 said LIC, The New India Assurance Co. and GIC Re continue as "
              "D-SIIs, unchanged from FY 2024-25, because of their size, market importance and interconnectedness.",
  steps=["D-SIIs FY 2025-26 = LIC + New India Assurance + GIC Re (no change)"],
  why="Private insurers are not on the list; leaving out New India Assurance is wrong.",
  current=ca("2026-04-02"),
  facts=[fact("Press release dated April 2, 2026: the identified insurers remain unchanged from the previous financial "
              "year and include Life Insurance Corporation of India, The New India Assurance Company Ltd., and General "
              "Insurance Corporation of India", D_DSII)])
Q(T, "Life and general insurance", "Intermediate",
  "Under the IRDAI (Actuarial, Finance and Investment Functions of Insurers) (Amendment) Regulations, 2026, from when "
  "must insurers prepare Ind AS-based financial statements, and what relief is available to insurers that are not "
  "ready?",
  ["From 1 April 2026; a one-time forbearance of one year on a Board-approved transition plan, applied for by 30 April "
   "2026",
   "From 1 April 2027; a three-year deferral for all general insurers",
   "From 1 April 2026; life insurers are exempt, and only general insurers must comply",
   "From 1 October 2026; no relaxation is allowed for any insurer"],
  concept="Ind AS for insurers",
  explanation="The amended regulations apply to all life, general and health insurers and reinsurers from 1 April "
              "2026. Insurers that are not adequately prepared may seek a one-time one-year forbearance with a "
              "Board-approved action plan, applying by 30 April 2026 and submitting quarterly Ind AS information.",
  steps=["Applies to all insurers from 1 April 2026", "Forbearance: one year, apply by 30 April 2026"],
  why="The date is 1 April 2026, not 2027 or October 2026; life insurers are not exempt; relief is available.",
  current=ca("2026-04-01"),
  facts=[fact("The regulations are applicable to all insurers, including life, general, health insurers and reinsurers. "
              "They shall come into force from 1st April 2026", D_INDAS),
         fact("Insurers that are not adequately prepared may seek a one-time relaxation for a period of one year, subject "
              "to a Board-approved action plan; the application must be made by 30th April 2026", D_INDAS)])
Q(T, "Life and general insurance", "Intermediate",
  "Who bears the total expenses of running the institution of Insurance Ombudsman, according to the Council for "
  "Insurance Ombudsmen?",
  ["The Life Insurance Council and the General Insurance Council",
   "IRDAI, out of the fees it collects from insurers",
   "The Central Government, through the Department of Financial Services",
   "Complainants, through a nominal filing fee"],
  concept="Insurance Ombudsman",
  explanation="IRDAI provides secretarial staff, but the expenses of the institution are borne by the Life Insurance "
              "Council and the General Insurance Council in the proportion the Council for Insurance Ombudsmen "
              "specifies. Complainants pay no fee.",
  steps=["Cost of the Ombudsman offices → Life Insurance Council + General Insurance Council"],
  why="IRDAI only provides staff; the Government does not fund it; no fee is charged to complainants.",
  facts=[fact("The total expenses for running the Institution are borne by the Life Insurance Council and the General "
              "Insurance Council in such proportion as the Council for Insurance Ombudsmen may specify", D_CIO),
         fact("No charges are required to be paid for lodging a complaint with the Insurance Ombudsman", D_CIO)])
Q(T, "Life and general insurance", "Advanced",
  "Which of the following complaints can an Insurance Ombudsman entertain under the Insurance Ombudsman Rules, 2017, "
  "assuming the time limits are met?\nP. A sole proprietor's claim of ₹12 lakh under his shop policy was partly "
  "repudiated.\nQ. A partnership firm's fire claim of ₹30 lakh was rejected.\nR. An insurance agent has not received "
  "his commission from the insurer.\nS. A member of an employer's group health policy, whose claim is payable to her "
  "as beneficiary, faces delay in settlement.",
  ["P and S only", "P, Q and S only", "Q and R only", "P, R and S only"],
  concept="Scope of the Insurance Ombudsman",
  explanation="The Ombudsman handles personal-lines, group and sole-proprietorship/micro-enterprise policies, for "
              "claims up to ₹50 lakh. P (sole proprietor, partial repudiation) qualifies. Partnership firms cannot "
              "approach (Q). Agents' administrative issues such as commission are non-entertainable (R). A group-policy "
              "member can complain when the claim is payable to her as beneficiary (S).",
  steps=["P: sole proprietor → yes", "Q: partnership firm → no", "R: agent's commission → no",
         "S: group member, payable to her → yes"],
  why="Q and R fall outside the Rules, so every option containing them is wrong.",
  facts=[fact("Only individual policyholders, sole proprietorship or micro enterprises who have taken insurance on "
              "personal lines are eligible. However, a member covered under a Master Policy or a Group Insurance can "
              "approach the Ombudsman, provided the payment of the claim is to be made to the individual", D_CIO),
         fact("Routine administrative issues concerning agents (like non-issue of licence, non-receipt of commission "
              "etc.) are non-entertainable", D_CIO)])
Q(T, "Government insurance schemes", "Advanced",
  "Consider the following statements based on the Department of Financial Services' FAQs:\nI. Death of a PMJJBY "
  "subscriber by suicide is covered.\nII. Death of a PMSBY subscriber by suicide is covered.\nIII. Death of a PMSBY "
  "subscriber in a flood or earthquake is covered.\nWhich of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="Coverage of PMJJBY and PMSBY",
  explanation="PMJJBY is a term life cover for death due to any cause, so suicide, murder and natural calamities are "
              "covered (I true). PMSBY is an accident cover: death from suicide is not covered, though murder is (II "
              "false); natural calamities are treated as accidents and covered (III true).",
  steps=["PMJJBY: any cause → suicide covered", "PMSBY: suicide not covered", "PMSBY: natural calamity = accident → "
         "covered"],
  why="Every option with II is wrong, since PMSBY excludes suicide.",
  facts=[fact("Does the PMJJBY cover death resulting from natural calamities ... suicide / murder? All these events are "
              "covered as PMJJBY covers death due to any reason", D_PMJJBY),
         fact("Natural calamities being in the nature of accidents, any death / disability resulting from such natural "
              "calamities is also covered under PMSBY. While death due to suicide is not covered, that from murder is "
              "covered", D_PMSBY)])

pmjjby, pmsby = 2, 2
assert pmjjby + pmsby == 4
Q(T, "Government insurance schemes", "Advanced",
  "Ravi, 45, renewed PMJJBY through his savings account in June 2026. By mistake, PMSBY premium was debited from two of "
  "his bank accounts for the same year. He dies in a road accident in October 2026. What do his nominees receive under "
  "the two schemes?",
  ["₹4 lakh: ₹2 lakh under PMJJBY and ₹2 lakh under PMSBY, cover restricted to one account",
   "₹6 lakh: ₹2 lakh under PMJJBY and ₹2 lakh under each PMSBY enrolment",
   "₹2 lakh only, as a person cannot get both PMJJBY and PMSBY on one death",
   "₹2 lakh under PMSBY only, as PMJJBY does not cover accidental death"],
  concept="Combining PMJJBY and PMSBY benefits",
  explanation="PMJJBY pays ₹2 lakh on death due to any cause, and PMSBY cover is in addition to any other insurance, "
              "paying ₹2 lakh on accidental death. If a member is covered through more than one account, PMSBY cover is "
              "restricted to one account and the extra premium is forfeited. Total = 2 + 2 = ₹4 lakh.",
  steps=["PMJJBY (any cause) = ₹2 lakh", "PMSBY (accident) = ₹2 lakh, one account only", "Total ₹4 lakh"],
  why="PMSBY does not pay twice; the schemes are not mutually exclusive; PMJJBY covers accidental death too.",
  computed=True,
  facts=[fact("Rs.2 lakh is payable on a subscriber's death due to any cause", D_PMJJBY),
         fact("In case a member is covered through more than one account and premium is received by the insurance "
              "company inadvertently, insurance cover will be restricted to one account and the premium shall be liable "
              "to be forfeited; cover is in addition to cover under any other insurance scheme", D_PMSBY)])

# ================= Mutual Funds (Basic 2 / Intermediate 2 / Advanced 2)
T = "Mutual Funds"
Q(T, "AMFI", "Basic",
  "The nationwide investor-awareness campaign 'Mutual Funds Sahi Hai' was initiated in 2017, under SEBI's guidance, "
  "by:",
  ["AMFI", "SEBI's Investor Protection and Education Fund", "NISM", "The Ministry of Finance"],
  concept="Investor awareness in mutual funds",
  explanation="AMFI, the industry body of SEBI-registered AMCs, launched the 'Mutual Funds Sahi Hai' media campaign in "
              "2017 under SEBI's guidance, in several languages.",
  steps=["Mutual Funds Sahi Hai → AMFI, 2017"],
  why="SEBI guided it but AMFI runs it; NISM and the Finance Ministry did not initiate it.",
  facts=[fact("The 'Mutual Funds Sahi Hai' campaign, a nationwide investor awareness media outreach in various languages "
              "initiated by AMFI in 2017 under SEBI's guidance", D_AMFI)])
Q(T, "NAV and SIP", "Basic",
  "What is the instalment size of a 'Chhoti SIP', the small-ticket SIP introduced for first-time mutual fund "
  "investors following SEBI's letter of February 2025?",
  ["Exactly ₹250 a month", "₹100 a week", "₹500 a month", "₹1,000 a quarter"],
  concept="Chhoti SIP",
  explanation="A Chhoti SIP instalment must be exactly ₹250, monthly only, with a minimum commitment of 60 instalments "
              "(premature stopping is allowed), paid by UPI or NACH auto-pay.",
  steps=["Ticket = ₹250", "Monthly only"],
  why="No weekly, ₹500 or quarterly variant is allowed under the facility.",
  facts=[fact("The ticket size for each SIP installment under this facility must be exactly ₹250/-; the facility will be "
              "available with a monthly investment frequency only", D_CHHOTI)])
Q(T, "AMFI", "Intermediate",
  "Under which legal form was the Association of Mutual Funds in India (AMFI) incorporated?",
  ["As a non-profit company under Section 25 of the Companies Act, 1956 (now Section 8 of the 2013 Act)",
   "As a statutory body under the SEBI Act, 1992",
   "As a trust under the Indian Trusts Act, 1882, sponsored by UTI",
   "As a co-operative society registered with the Registrar of Societies"],
  concept="AMFI's constitution",
  explanation="AMFI was incorporated on 22 August 1995 under Section 25 of the Companies Act, 1956 (corresponding to "
              "Section 8 of the Companies Act, 2013) as a non-profit organisation of SEBI-registered AMCs.",
  steps=["AMFI = Section 25 (now Section 8) non-profit company"],
  why="AMFI is not a statutory body, a trust or a society; individual mutual funds, not AMFI, are set up as trusts.",
  facts=[fact("AMFI was incorporated on August 22, 1995 under section 25 of the Companies Act, 1956 (corresponding Section "
              "8 of the new Companies Act, 2013), as a non-profit organisation", D_AMFI)])
Q(T, "NAV and SIP", "Intermediate",
  "Under the SEBI (Mutual Funds) Regulations, 2026, approved by SEBI's Board on 17 December 2025 to replace the 1996 "
  "regulations, how are scheme expenses now capped?",
  ["Limits apply to a Base Expense Ratio; statutory levies such as STT, GST and stamp duty are charged on actuals "
   "outside it",
   "One all-inclusive TER cap now covers statutory levies, brokerage and distribution costs",
   "Expense limits are removed and left to each AMC's board",
   "Only direct plans may charge expenses; regular plans charge none"],
  concept="Total Expense Ratio and NAV",
  explanation="The expense limits are renamed the Base Expense Ratio (BER), which excludes statutory and regulatory "
              "levies (STT, CTT, GST, stamp duty, SEBI fees, exchange charges), now charged on actuals. TER = BER + "
              "brokerage + levies. The BER cap for index funds and ETFs fell to 0.9% from 1.0%.",
  steps=["TER = BER + brokerage + statutory/regulatory levies", "Caps apply to BER"],
  why="The levies were taken out of the cap, not folded in; limits were not removed; regular plans still bear "
      "expenses.",
  current=ca("2025-12-17"),
  facts=[fact("Statutory levies, including STT, CTT, GST, stamp duty, SEBI fees, and exchange charges, will now be billed "
              "on actuals, separate from the base expense ratio (BER); the TER will now consist of the BER, brokerage "
              "and statutory or regulatory levies", D_MFREG)])
Q(T, "NAV and SIP", "Advanced",
  "Which of the following investors can start a Chhoti SIP under the facility's terms?\nP. Asha, 24, who has never "
  "invested in a mutual fund, ₹250 a month by UPI.\nQ. Arjun, 16, a first-time investor, through his guardian.\nR. "
  "Meena, who already runs a ₹1,000 monthly SIP in another fund.\nS. Kiran, a first-time investor holding Chhoti SIPs "
  "with two AMCs, who now starts one with a third AMC at ₹250 a month by NACH.",
  ["P and S only", "P, Q and S only", "P only", "P, R and S only"],
  concept="Eligibility for Chhoti SIP",
  explanation="Only first-time individual MF investors, excluding minors, are eligible; each may have up to three Chhoti "
              "SIPs, one per AMC, at exactly ₹250 monthly via UPI or NACH. P qualifies; Q is a minor; R already has a "
              "regular SIP, so is not first-time; S's third Chhoti SIP with a new AMC is within the limit.",
  steps=["P: eligible", "Q: minor → no", "R: existing SIP → no", "S: third Chhoti SIP, new AMC → eligible"],
  why="Options with Q or R are wrong; 'P only' wrongly excludes S.",
  facts=[fact("The facility is available exclusively to first-time individual investors in the mutual fund industry, "
              "excluding minors. Each eligible investor can have a maximum of three Chhoti SIPs (one per Asset "
              "Management Company)", D_CHHOTI),
         fact("Investments can only be made via UPI or NACH Autopay; an investor who initiates any other type of SIP or "
              "makes a lumpsum investment will not be eligible for Chhoti SIP", D_CHHOTI)])

aum, ber_pct, brokerage, levies = 2000, 0.9, 0.6, 1.4
ber = aum * ber_pct / 100
ter = round(pct(ber + brokerage + levies, aum), 2)
assert ber == 18 and ter == 1.0
Q(T, "Types", "Advanced",
  "An index fund with average net assets of ₹2,000 crore charges its Base Expense Ratio at the 0.9% cap of the SEBI "
  "(Mutual Funds) Regulations, 2026. It also incurs brokerage of ₹0.6 crore and statutory and regulatory levies of "
  "₹1.4 crore in the year. What is its Total Expense Ratio?",
  ["1.0%, of which only 0.9% (₹18 crore) is the capped BER", "0.9%, as all costs must fit within the cap",
   "1.1%, as levies are charged twice", "0.8%, as levies are deducted from the BER"],
  concept="BER and TER",
  explanation="BER = 0.9% × 2,000 = ₹18 crore. TER = BER + brokerage + levies = 18 + 0.6 + 1.4 = ₹20 crore = 1.0% of "
              "net assets. Under the 2026 regulations the cap applies only to the BER; brokerage and levies are "
              "charged separately.",
  steps=["BER = ₹18 crore", "TER = 18 + 0.6 + 1.4 = ₹20 crore", "20 ÷ 2,000 = 1.0%"],
  why="Levies are outside the cap, so 0.9% understates the TER; nothing is charged twice or deducted from BER.",
  computed=True, current=ca("2025-12-17"),
  facts=[fact("SEBI has reduced the base expense ratio cap for index funds and ETFs to 0.9% from 1.0%; the TER will now "
              "consist of the BER, brokerage and statutory or regulatory levies", D_MFREG)])

# ================= Budget and Economic Survey (Basic 1 / Intermediate 4 / Advanced 2)
T = "Budget and Economic Survey"
Q(T, "Union Budget highlights", "Basic",
  "According to the Union Budget 2026-27, from when does the new Income-tax Act, 2025 come into effect?",
  ["April 2026", "1 February 2026", "April 2027", "1 October 2026"],
  concept="Direct tax reform",
  explanation="The Finance Minister said the new Income-tax Act, 2025 will come into effect from April 2026, with "
              "simplified Income Tax Rules and redesigned forms to be notified.",
  steps=["Income-tax Act, 2025 → effective April 2026"],
  why="1 February 2026 is the Budget date; the other dates are not stated.",
  current=D_BD,
  facts=[fact("The New Income tax Act, 2025 will come into effect from April 2026. Also the simplified Income Tax Rules "
              "and Forms will be notified shortly", D_BUDGET)])
Q(T, "Union Budget highlights", "Intermediate",
  "The Union Budget 2026-27 proposed to cut the TCS rate on remittances under the Liberalised Remittance Scheme (LRS) "
  "for education and medical purposes:",
  ["From 5% to 2%", "From 20% to 5%", "From 2% to nil", "From 10% to 5%"],
  concept="Tax collected at source on LRS",
  explanation="TCS on LRS remittances for education and medical treatment was proposed to fall from 5% to 2%; TCS on "
              "overseas tour packages was cut to 2% from 5% and 20%.",
  steps=["LRS education/medical TCS: 5% → 2%"],
  why="20% was a tour-package rate; nil and 10% → 5% were not proposed.",
  current=D_BD,
  facts=[fact("TCS for pursuing education and for medical purposes under the Liberalized Remittance Scheme (LRS) reduced "
              "from 5 percent to 2 percent", D_BUDGET)])
Q(T, "Union Budget highlights", "Intermediate",
  "What did the Union Budget 2026-27 propose for the taxation of share buybacks?",
  ["Buyback to be taxed as capital gains for all shareholders, with promoters paying an additional tax for an effective "
   "22% (corporate) or 30% (non-corporate)",
   "Buyback proceeds to be taxed as dividend income of all shareholders at slab rates",
   "A 20% buyback tax on the company, with shareholders fully exempt",
   "Buybacks to be exempt for minority shareholders and banned for promoters"],
  concept="Buyback taxation",
  explanation="In the interest of minority shareholders, buyback for all types of shareholders is to be taxed as "
              "capital gains; promoters pay an additional buyback tax, making the effective tax 22% for corporate and "
              "30% for non-corporate promoters.",
  steps=["All shareholders: capital gains", "Promoters: extra tax → 22% / 30%"],
  why="The proposal moves away from dividend treatment; it does not tax the company or ban promoter participation.",
  current=D_BD,
  facts=[fact("Buyback for all types of shareholders will be taxed as Capital Gains. It requires promoters to pay an "
              "additional buyback tax, making effective tax 22 percent for corporate promoters and 30 percent for "
              "non-corporate promoters", D_BUDGET)])
Q(T, "Economic Survey highlights", "Intermediate",
  "According to the Economic Survey 2025-26, how did the NPA recovery rate of scheduled commercial banks change "
  "between FY18 and FY25?",
  ["It nearly doubled, from 13.2% to 26.2%", "It fell from 26.2% to 13.2%", "It rose from 7.1% to 14.5%",
   "It stayed at about 17% throughout"],
  concept="Asset quality and recovery",
  explanation="The Survey said the NPA recovery rate of SCBs nearly doubled to 26.2% in FY25 from 13.2% in FY18, while "
              "the slippage ratio fell from 7.1% (FY18) to 1.3% (FY26, September 2025).",
  steps=["Recovery rate: FY18 13.2% → FY25 26.2%"],
  why="The second option reverses the trend; 7.1% is the FY18 slippage ratio; 17% is near the CRAR, not recovery.",
  current=D_ES,
  facts=[fact("The non-performing asset (NPA) recovery rate of scheduled commercial banks (SCBs) nearly doubling to 26.2 "
              "per cent in FY25 from 13.2 per cent in FY18, according to the Economic Survey 2025-26", D_ES_BANK)])

fx_new, fx_old = 701.4, 668.3
assert round(fx_new - fx_old, 1) == 33.1 and round(pct(fx_new - fx_old, fx_old), 1) == 5.0
Q(T, "Economic Survey highlights", "Intermediate",
  "The Economic Survey 2025-26 reported India's foreign exchange reserves at $701.4 billion on 16 January 2026, against "
  "$668.3 billion at the end of March 2025. By how much had reserves risen?",
  ["About $33.1 billion, roughly 5%", "About $33.1 billion, roughly 4.7%", "About $66.8 billion, roughly 10%",
   "About $3.3 billion, roughly 0.5%"],
  concept="External sector",
  explanation="Increase = 701.4 − 668.3 = $33.1 billion; as a share of the March 2025 level, 33.1 ÷ 668.3 ≈ 4.95%, "
              "about 5%. (Dividing by the January figure gives 4.7%, which uses the wrong base.)",
  steps=["701.4 − 668.3 = 33.1", "33.1 ÷ 668.3 ≈ 5.0%"],
  why="4.7% uses the later level as base; $66.8 billion and $3.3 billion misplace the decimal.",
  computed=True, current=D_ES,
  facts=[fact("India's foreign exchange reserves increased to $701.4 billion as of 16 January 2026, up from $668.3 billion "
              "as of the end of March 2025", D_ES_UP)])

capex, eff_capex, tot_exp = 12.22, 17.15, 53.47
assert round(pct(capex, tot_exp), 1) == 22.9 and round(pct(eff_capex, tot_exp), 1) == 32.1
Q(T, "Fiscal terms", "Advanced",
  "In BE 2026-27 the Centre's total expenditure is ₹53.47 lakh crore, its capital expenditure ₹12.22 lakh crore and its "
  "effective capital expenditure ₹17.15 lakh crore. What share of total expenditure is capital expenditure, and what "
  "share is effective capital expenditure?",
  ["About 22.9% and about 32.1%", "About 22.9% and about 9.2%", "About 3.1% and about 4.4%",
   "About 32.1% and about 22.9%"],
  concept="Capital expenditure and effective capital expenditure",
  explanation="Capex share = 12.22 ÷ 53.47 ≈ 22.9%. Effective capex (capex + grants-in-aid of ₹4.93 lakh crore for "
              "creation of capital assets) = 17.15 ÷ 53.47 ≈ 32.1%. 3.1% and 4.4% are the same items as shares of GDP, "
              "not of expenditure.",
  steps=["12.22 ÷ 53.47 ≈ 22.9%", "17.15 ÷ 53.47 ≈ 32.1%"],
  why="9.2% is the grants alone (4.93 ÷ 53.47); 3.1%/4.4% are GDP ratios; the last option swaps the two.",
  computed=True, current=D_BD,
  facts=[fact("Total expenditure in BE 2026-27 is projected to be ₹53.47 lakh crore; ₹12.22 lakh crore (3.1 per cent of "
              "GDP) towards capital expenditure; the effective capital expenditure in FY 2026-27 is estimated at ₹17.15 "
              "lakh crore (or 4.4 per cent of GDP)", D_BUDGET)])
Q(T, "Economic Survey highlights", "Advanced",
  "Consider the following statements based on reports of the Economic Survey 2025-26:\nI. The capital to "
  "risk-weighted assets ratio (CRAR) of scheduled commercial banks fell below 12% in September 2025.\nII. The slippage "
  "ratio of scheduled commercial banks improved from 7.1% in FY18 to 1.3% in FY26 (as of September 2025).\nIII. Since "
  "2016, creditors have realised ₹3.99 lakh crore from about 1,300 cases resolved under the IBC.\nWhich of the above "
  "is/are correct?",
  ["II and III only", "I and II only", "III only", "I, II and III"],
  concept="Banking sector in the Economic Survey",
  explanation="The Survey put SCBs' CRAR at a robust 17.2% in September 2025, so I is wrong. The slippage ratio fell "
              "from 7.1% in FY18 to 1.4% in FY25 and 1.3% in FY26 as of September 2025 (II). Creditors realised ₹3.99 "
              "lakh crore from around 1,300 resolved IBC cases (III).",
  steps=["I: CRAR 17.2% → false", "II: true", "III: true"],
  why="Options with I are wrong; 'III only' leaves out II.",
  current=D_ES,
  facts=[fact("The slippage ratio of SCBs improved from 7.1 per cent in FY18 to 1.4 per cent in FY25 and further to 1.3 "
              "per cent in FY26, as of September 2025; CRAR of SCBs standing at 17.2 per cent as of September 2025",
              D_ES_BANK),
         fact("Since its inception in 2016, the IBC has delivered superior outcomes, with creditors realising ₹3.99 lakh "
              "crore from around 1,300 resolved cases", D_ES_BANK)])

# ================= Government Financial Schemes (Basic 2 / Intermediate 4 / Advanced 2)
T = "Government Financial Schemes"
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Basic",
  "Which of the following activities can be financed under Pradhan Mantri MUDRA Yojana (PMMY)?",
  ["A dairy unit, as an activity allied to agriculture", "Crop cultivation by a farmer", "A personal home loan",
   "Purchase of shares by an individual"],
  concept="Purposes of MUDRA loans",
  explanation="PMMY gives collateral-free loans for non-agricultural income-generating activities, including activities "
              "allied to agriculture such as poultry, dairy and beekeeping, for term loans and working capital. Crop "
              "loans, housing and investment in shares are not covered.",
  steps=["PMMY = non-farm micro enterprises + allied activities (dairy, poultry, beekeeping)"],
  why="Crop cultivation is agriculture proper (KCC covers it); housing and share purchases are not enterprise loans.",
  facts=[fact("Purposes: Non-agricultural, including activities allied to agriculture such as poultry, dairy, beekeeping "
              "etc. Term loan and working capital requirements can both be met; collateral not required", D_PMMY)])
Q(T, "Credit guarantee schemes", "Basic",
  "Under CGTMSE's credit guarantee scheme, what is the maximum extent of guarantee cover for credit facilities to women "
  "entrepreneurs, for guarantees issued on or after 1 April 2024?",
  ["90%", "85%", "75%", "100%"],
  concept="CGTMSE coverage",
  explanation="CGTMSE's Circular 241 (December 2024) raised the cover for women entrepreneurs (and MSEs promoted by "
              "Agniveers) from 85% to 90%, applicable to guarantees issued on or after 1 April 2024.",
  steps=["Women entrepreneurs: 85% → 90%"],
  why="85% was the earlier level (still applicable to SC/ST, aspirational districts etc.); 75% is for other borrowers; "
      "100% is not offered.",
  facts=[fact("Enhancement in extent of guarantee coverage in respect of Women-led Enterprises from 85% to 90%; "
              "applicable to all guarantees issued on or after April 01, 2024", D_CG_WOMEN)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Intermediate",
  "Under Atal Pension Yojana, what happens if the accumulated corpus earns lower returns than estimated and cannot "
  "support the guaranteed minimum pension?",
  ["The Central Government funds the shortfall; if returns are higher, the subscriber gets enhanced pension",
   "The pension is cut in proportion to the shortfall",
   "The bank holding the account must make good the shortfall",
   "The subscriber must pay extra contributions to restore the corpus"],
  concept="Guaranteed pension under APY",
  explanation="APY pays a fixed minimum pension of ₹1,000 to ₹5,000 a month from 60. The minimum pension is guaranteed "
              "by the Government: any inadequacy from lower returns is funded by the Central Government, while higher "
              "returns give enhanced pension.",
  steps=["Lower returns → Government funds the gap", "Higher returns → enhanced benefits"],
  why="The pension is not cut, banks bear no liability, and no extra contribution is demanded.",
  facts=[fact("If the accumulated corpus earns a lower than estimated return on investment and is inadequate to provide "
              "the minimum guaranteed pension, the Central Government would fund such inadequacy. Alternatively, if the "
              "returns on investment are higher, the subscribers would get enhanced pensionary benefits", D_APY)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Intermediate",
  "Up to what age can a PMJJBY member keep the life cover by renewing it, and what does the scheme pay on surrender or "
  "maturity?",
  ["Up to 55 years; nothing, as it is pure term cover", "Up to 70 years; return of premiums at maturity",
   "Up to 50 years; a surrender value after five years", "Up to 60 years; a maturity bonus"],
  concept="PMJJBY design",
  explanation="Entry into PMJJBY is allowed only up to 50, but cover ends at 55 (age nearest birthday), subject to annual "
              "renewal. It is a pure term policy with no investment component, so there is no maturity benefit or "
              "surrender value; only the nominee gets ₹2 lakh on death.",
  steps=["Entry 18–50; cover till 55", "Pure term → no maturity/surrender value"],
  why="70 is PMSBY's exit age; 50 is the entry limit; PMJJBY has no maturity, bonus or surrender benefit.",
  facts=[fact("On attaining age 55 years (age near birth day), subject to annual renewal up to that date (entry, however, "
              "will not be possible beyond the age of 50 years)", D_PMJJBY),
         fact("PMJJBY is a pure term insurance policy, which covers only mortality with no investment component", D_PMJJBY)])
Q(T, "Credit guarantee schemes", "Intermediate",
  "Under the Emergency Credit Line Guarantee Scheme (ECLGS) 5.0, approved on 5 May 2026, what guarantee cover is "
  "provided on loans to eligible MSMEs and to eligible non-MSMEs?",
  ["100% for MSMEs and 90% for non-MSMEs, with no guarantee fee", "90% for MSMEs and 75% for non-MSMEs, at 1% fee",
   "100% for both, with a fee of 0.5% a year", "75% for MSMEs and 50% for non-MSMEs"],
  concept="ECLGS 5.0",
  explanation="ECLGS 5.0, run by NCGTC for businesses hit by external disruptions, gives 100% guarantee on additional "
              "working capital to eligible MSMEs and 90% to eligible non-MSMEs (and 90% for scheduled passenger "
              "airlines), with no guarantee fee payable by lenders. It runs till 31 March 2027 or ₹2.55 lakh crore of "
              "guarantees.",
  steps=["MSME 100%; non-MSME 90%; no fee"],
  why="The other percentages and fees do not match the scheme.",
  current=ca("2026-05-05"),
  facts=[fact("Credit guarantee coverage: 100% guarantee for loans extended to eligible MSMEs and 90% guarantee coverage "
              "for eligible non-MSMEs; no guarantee fee is payable by MLIs under the scheme", D_ECLGS5),
         fact("The Government approved the Emergency Credit Line Guarantee Scheme (ECLGS) 5.0 on 5th May 2026", D_ECLGS5)])
Q(T, "Credit guarantee schemes", "Intermediate",
  "Under CGTMSE's Credit Guarantee Scheme for banks, what is the standard annual guarantee fee (AGF) for guaranteed "
  "credit of up to ₹10 lakh?",
  ["0.37% per annum", "0.55% per annum", "1.00% per annum", "0.75% per annum"],
  concept="Annual Guarantee Fee",
  explanation="Following CGTMSE's fee cuts (Circular 221, effective 1 April 2023), the standard AGF is 0.37% a year for "
              "the 0–10 lakh slab, 0.55% for above ₹10 lakh to ₹50 lakh and 0.60% for above ₹50 lakh to ₹1 crore. AGF is "
              "charged on the guaranteed amount in the first year and on the outstanding amount thereafter.",
  steps=["0–₹10 lakh slab → 0.37% p.a."],
  why="0.55% is the next slab; 1.00% and 0.75% are not the rate for the smallest slab.",
  facts=[fact("Slab 0-10 lakh: Revised Standard Rate 0.37 (pa); Above 10-50 lakh: 0.55; applicable to all guarantees "
              "approved/renewed on or after April 01, 2023", D_CG_AGF)])

x_peak, y_peak = 45, 800
x_add = 0.20 * x_peak
y_add = min(0.20 * y_peak, 100)
assert x_add == 9 and y_add == 100
Q(T, "Credit guarantee schemes", "Advanced",
  "Under ECLGS 5.0, firm X (an MSME) had peak fund-based working capital outstanding of ₹45 crore in Q4 of FY 2025-26, "
  "and firm Y (an eligible non-MSME) had ₹800 crore. Both meet all other conditions. What maximum additional credit "
  "can each get, and with what guarantee cover?",
  ["X: ₹9 crore with 100% cover; Y: ₹100 crore with 90% cover", "X: ₹9 crore with 100% cover; Y: ₹160 crore with 90% "
   "cover", "X: ₹9 crore with 90% cover; Y: ₹100 crore with 100% cover", "X: ₹45 crore with 100% cover; Y: ₹100 crore "
   "with 90% cover"],
  concept="Additional credit under ECLGS 5.0",
  explanation="Additional credit is up to 20% of peak fund-based working capital outstanding in Q4 FY26, capped at "
              "₹100 crore per borrower. X: 20% × 45 = ₹9 crore, 100% guaranteed (MSME). Y: 20% × 800 = ₹160 crore, "
              "capped at ₹100 crore, 90% guaranteed (non-MSME).",
  steps=["X: 0.2 × 45 = 9 → 100% cover", "Y: 0.2 × 800 = 160 → cap 100 → 90% cover"],
  why="₹160 crore ignores the cap; the cover percentages are swapped in the third option; ₹45 crore ignores the 20% "
      "limit.",
  computed=True, current=ca("2026-05-05"),
  facts=[fact("The scheme provides additional credit of up to 20% of the peak fund-based working capital outstanding "
              "during the fourth quarter of FY 2025-26, subject to a ceiling of ₹100 crore per borrower", D_ECLGS5),
         fact("100% guarantee for loans extended to eligible MSMEs and 90% guarantee coverage for eligible non-MSMEs",
              D_ECLGS5)])

default = 20
p_cover, q_cover = 90 + 5, 75
assert default * p_cover / 100 == 19 and default * q_cover / 100 == 15
Q(T, "Credit guarantee schemes", "Advanced",
  "Two CGTMSE-guaranteed loans of ₹30 lakh each turn NPA with ₹20 lakh in default. P is a micro enterprise of a woman "
  "entrepreneur in a district identified by RBI as credit deficient (ICDD); Q is a small enterprise of a borrower in "
  "the 'all other' category, outside any ICDD. What is the maximum guarantee cover on each?",
  ["P: ₹19 lakh (95%); Q: ₹15 lakh (75%)", "P: ₹18 lakh (90%); Q: ₹15 lakh (75%)",
   "P: ₹19 lakh (95%); Q: ₹16 lakh (80%)", "P: ₹17 lakh (85%); Q: ₹17 lakh (85%)"],
  concept="Extent of CGTMSE guarantee cover",
  explanation="Women entrepreneurs get 90% cover, and MSEs in RBI's Identified Credit Deficient Districts get an extra 5 "
              "percentage points, so P gets 95%: 0.95 × 20 = ₹19 lakh. 'All other' borrowers get 75%: 0.75 × 20 = ₹15 "
              "lakh.",
  steps=["P: 90% + 5% (ICDD) = 95% → ₹19 lakh", "Q: 75% → ₹15 lakh"],
  why="₹18 lakh ignores the ICDD addition; 80% for Q would need an ICDD location; 85% applies to other categories.",
  computed=True,
  facts=[fact("Women entrepreneurs / MSE promoted by Agniveers 90%; All other category of borrowers 75%; the extent of "
              "guarantee coverage for MSEs situated in Identified Credit Deficient Districts (ICDD) by RBI is additional "
              "5% over and above the applicable guarantee coverage (for 90% it would be 95%)", D_CG_WOMEN)])


# ================================================================= checks and output
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_006_plan.json").read_text(encoding="utf-8"))
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
    assert ev is None or ev <= CHECKED, (q["question_id"], ev)
assert max(_keys.values()) - min(_keys.values()) <= 4, _keys
assert all(0 <= i < len(questions) for i in INDEPENDENT)

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_006",
    "created_at": TODAY,
    "notes": NOTES,
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_006_BFA.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions; keys {dict(sorted(_keys.items()))}; "
      f"current_affairs {sum('current_affairs' in q for q in questions)}; independent {len(INDEPENDENT)})")
