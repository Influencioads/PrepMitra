"""Writes batches/parts/BATCH_007_BFA.json: the 200 Banking and Financial Awareness questions of BATCH_007.

Every fact is backed by at least one fact_check whose source was opened on 2026-11-06, or, where only search results
stated it (no block was worked around), by search results, in which case the question carries web:search-confirmed.
Time-sensitive questions carry a current_affairs block whose event_date is the date of the event or release as stated
by the source (Repo Rate and Budget questions always). Computable answers are re-derived below with assertions, the
quota per (topic, difficulty) is checked against the batch plan, and the answer keys are balanced.
ai:independent-check is added only to the questions listed in INDEPENDENT, which a separate fresh solver answered
blind (stem and options only) and got right with confidence. If any check fails, nothing is written. All ~1,200
earlier Banking stems and answers (BATCH_000 to BATCH_006) were read first; their facts, and neighbouring steps of
the schedules they tested, are not repeated.

    python tools/batch_007/banking.py      (run from anywhere)
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
FIRST_ID = 1204
SECONDS = {"Basic": 20, "Intermediate": 30, "Advanced": 60}

_rng = random.Random(2026110607)
_keys = Counter()
questions = []

# Question numbers (offset from BANK_BFA_001204, i.e. 0 = 001204) that a separate fresh solver answered blind (stem
# and options only, no key or solution) and matched the key with high confidence. Two fresh solvers were used: one
# answered the even offsets 0-198 (97 matched the key, 57 with high confidence; 3 low/medium mismatches at 64, 66,
# 106 were checked against their sources and kept), the other the odd offsets 1-199 (99 matched, 87 with high
# confidence; it missed 73, whose key was re-confirmed on the current Resolution of Stressed Assets Directions).
# Neither had web search; the second fetched rbi.org.in pages. Only high-confidence matches are tagged.
# After review, 12 questions were changed (28 and 133/131 replaced: WMA for Delhi, NACH on all days, e-mandates for
# FASTag/NCMC; 52 and 61 re-sourced to RBI pages; 29, 127, 129 framed by circular date; 82, 90, 167, 171 stems
# tightened), so their earlier tags are dropped. A third fresh solver answered all 12 blind and matched every
# key; the 10 high-confidence ones are re-tagged (82 and 90 were medium and stay untagged).
INDEPENDENT = {0, 128, 2, 130, 4, 6, 8, 10, 12, 140, 14, 16, 144, 18, 146, 20, 148, 24, 152, 26, 28, 156, 30, 32, 160, 162, 164, 38, 46, 48, 178, 52, 54, 182, 184, 60, 188, 192, 194, 68, 196, 70, 198, 72, 74, 76, 78, 80, 84, 86, 96, 108, 110, 112, 114, 116, 120} | {1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 67, 69, 71, 75, 79, 81, 83, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147, 149, 151, 153, 155, 157, 159, 161, 163, 165, 171, 173, 175, 181, 185, 187, 189, 193, 195, 197}
INDEPENDENT = (INDEPENDENT - {28, 29, 52, 61, 82, 90, 127, 129, 131, 133, 167, 171}) | {28, 29, 52, 61, 127, 129, 131, 133, 167, 171}

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


NOTES = ("BATCH_007 Banking and Financial Awareness part: 200 original questions (60 Basic, 80 Intermediate, 60 "
         "Advanced) across 32 topics, IDs BANK_BFA_001204 to BANK_BFA_001403. Built from sources opened on "
         "2026-11-06 (current RBI Directions of 2025-26 and their amendments, FAQs, notifications and press releases "
         "incl. the October 2026 MPC minutes and Monetary Policy Report, MoSPI, BIS, IBBI, SEBI, NSE, AMFI, IRDAI, "
         "DFS, static.pib PDFs, and named news or legal pages where no official HTML page could be opened); facts "
         "seen only in search results are marked web:search-confirmed; no block was worked around. Only changeable "
         "values and dated events carry current_affairs. Computed answers are re-derived with asserts in "
         "tools/batch_007/banking.py. Facts tested in BATCH_000-BATCH_006 are not repeated. ai:independent-check "
         "marks only the questions a separate fresh solver answered blind and got right with confidence.")


# ######## section A
# ---- sources (group A), opened 2026-11-06
A_DEPINT = "https://rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13157"   # CB - Interest Rate on Deposits Directions, 2025 (updated 1 Oct 2026)
A_UNIV = "https://rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13168"     # Universal Banks - Licensing Guidelines, 2025
A_GOVN = "https://rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13161"     # CB - Governance Directions, 2025 (updated 1 Oct 2026)
A_NI138 = "https://devgan.in/nia/section/138/"                                # NI Act, Section 138 (bare-act reproduction)
A_RBIACT = "https://bnblegal.com/bareact/reserve-bank-of-india-act-1934/"     # RBI Act, 1934 (bare-act reproduction)
A_GOVS = "https://www.rbi.org.in/Scripts/Governors.aspx"                      # RBI list of Governors
A_SURP = "https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=62789"  # RBI press release, 22 May 2026, surplus transfer
A_DAMO = "https://www.rbi.org.in/scripts/PublicationReportDetails.aspx?ID=645"    # Report of Committee on Customer Service in Banks
A_VERMA = "https://www.rbi.org.in/Scripts/PublicationReportDetails.aspx?ID=46"    # Report of WG on Restructuring Weak PSBs (1999)
A_GTB = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=10428"   # RBI press release, 26 July 2004, GTB draft scheme
A_GTBN = ("https://website.rbi.org.in/web/rbi/-/notifications/scheme-for-amalgamation-of-global-trust-bank-ltd.-with-"
          "oriental-bank-of-commerce-1800")                                       # RBI notification title (search result only)
A_PNB = "https://www.pnb.bank.in/heritage.html"                                   # PNB heritage page
A_HDFC = "https://www.hdfc.bank.in/press-release/2023/q2/hdfc-ltd-to-merge-into-hdfc-bank-effective-july-1-2023"
A_NBI = "https://www.gktoday.in/new-bank-of-india-merger"                         # search snippet only
A_1980 = "https://eparlib.nic.in/bitstream/123456789/831085/1/07_III_13-06-1980_p162_p165_PII.pdf"  # Lok Sabha debate 1980, search snippet only
A_WMA26 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=62011"   # RBI press release, 9 Jan 2026, WMA for States/UTs (GNCTD)
A_SDF = "https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=58187"       # RBI press release, 28 June 2024, WMA/SDF for States
A_BLA = "https://www.scconline.com/blog/post/2025/08/01/provisions-of-banking-laws-amendment-act-2025-notified/"
A_BLA_AIR = "https://www.newsonair.gov.in/new-banking-laws-to-come-into-effect-from-august-1"
SEARCH_ONLY.update({A_GTBN, A_NBI, A_1980})

# ================= Banking Fundamentals (Basic 4 / Intermediate 3 / Advanced 2)
T = "Banking Fundamentals"
Q(T, "Types of accounts", "Basic",
  "Under RBI's Commercial Banks – Interest Rate on Deposits Directions, 2025, what is the minimum tenor of a domestic "
  "term deposit that a bank may offer?",
  ["Seven days", "Fifteen days", "Thirty days", "Ninety-one days"],
  concept="Minimum tenor of term deposits",
  explanation="The Directions fix the minimum tenor of a domestic term deposit at seven days. (For NRE term deposits "
              "the minimum is one year, while NRO term deposits follow the seven-day minimum.)",
  steps=["Domestic term deposit → minimum tenor 7 days"],
  why="Fifteen, thirty and ninety-one days are not the prescribed minimum; 15 days was an older minimum and 91 days is "
      "a Treasury Bill tenor.",
  facts=[fact("Para 10(1): the minimum tenor of the deposit offered shall be seven days.", A_DEPINT)])
Q(T, "Types of accounts", "Basic",
  "According to RBI's Commercial Banks – Interest Rate on Deposits Directions, 2025, how often must a bank credit "
  "interest on savings deposits?",
  ["At quarterly or shorter intervals", "Only at half-yearly intervals", "Once a year, on 31 March",
   "Monthly, on the last working day"],
  concept="Savings deposit interest",
  explanation="Interest on savings deposits is calculated on a daily product basis, i.e. on the end-of-day balance, "
              "and the Directions require it to be credited at quarterly or shorter intervals.",
  steps=["Calculation: daily product basis", "Credit: quarterly or shorter intervals"],
  why="Half-yearly and annual credit are longer than the permitted interval; monthly credit is allowed (it is shorter "
      "than quarterly) but is not the rule laid down.",
  facts=[fact("Para 18: Interest on savings deposit shall be credited by a bank at quarterly or shorter intervals.",
              A_DEPINT),
         fact("Para 9(1): Interest shall be calculated on a daily product basis.", A_DEPINT)])
Q(T, "Types of accounts", "Basic",
  "Under RBI's Commercial Banks – Interest Rate on Deposits Directions, 2025, up to what end-of-day balance must a "
  "bank pay a single uniform rate of interest on a savings account, irrespective of the amount within that limit?",
  ["₹1 lakh", "₹50,000", "₹5 lakh", "₹10 lakh"],
  concept="Savings deposit rate slabs",
  explanation="The Directions require a uniform interest rate on savings balances up to ₹1 lakh; banks may offer "
              "differential rates only on any end-of-day balance exceeding ₹1 lakh.",
  steps=["Up to ₹1 lakh: one uniform rate", "Above ₹1 lakh: differential rates allowed"],
  why="₹50,000, ₹5 lakh and ₹10 lakh are not the threshold in the Directions (₹5 lakh is the DICGC insurance cover).",
  facts=[fact("Para 9(1)(a): A uniform interest rate shall be set on balance up to ₹1 lakh, irrespective of the amount "
              "in the account within this limit. (b) Differential rates of interest may be provided for any end-of-day "
              "savings bank account balance exceeding ₹1 lakh.", A_DEPINT)])
Q(T, "Types of banks", "Basic",
  "Under RBI's Universal Banks – Licensing Guidelines, 2025, what minimum share of its branches must a new universal "
  "bank open in unbanked rural centres?",
  ["25 per cent", "10 per cent", "33 per cent", "50 per cent"],
  concept="Licensing of universal banks",
  explanation="The guidelines require a new universal bank to open at least 25 per cent of its branches in unbanked "
              "rural centres, i.e. centres with a population of up to 9,999 as per the latest census.",
  steps=["Branch condition for new banks", "≥ 25% in unbanked rural centres (population up to 9,999)"],
  why="10, 33 and 50 per cent are not the prescribed share.",
  facts=[fact("Para 29: The bank shall open at least 25 per cent of its branches in unbanked rural centres "
              "(population up to 9,999 as per the latest census).", A_UNIV)])
Q(T, "Types of accounts", "Intermediate",
  "For a commercial bank, which deposit is a 'bulk deposit' under RBI's Commercial Banks – Interest Rate on Deposits "
  "Directions, 2025?",
  ["A single rupee term deposit of ₹3 crore and above", "A single rupee term deposit of ₹1 crore and above",
   "Any savings or term deposit of ₹2 crore and above", "Aggregate deposits of one customer of ₹5 crore and above"],
  concept="Bulk deposits",
  explanation="The Directions define a bulk deposit as a single rupee term deposit of ₹3 crore and above. Interest "
              "rates on deposits, including bulk deposits, must be uniform across all branches and are not "
              "negotiable between the depositor and the bank.",
  steps=["Single rupee term deposit", "Amount ₹3 crore or more → bulk deposit"],
  why="₹1 crore is the limit up to which individuals' term deposits must carry a premature withdrawal facility; "
      "savings deposits and aggregate holdings are not part of the definition.",
  facts=[fact("Para 6(2): 'Bulk Deposit' means Single Rupee term deposits of ₹3 crore and above.", A_DEPINT),
         fact("Para 7(2): The interest rates offered on deposits, including bulk deposits, shall be uniform across all "
              "branches.", A_DEPINT)])
Q(T, "Types of accounts", "Intermediate",
  "Ramesh ran a sole proprietorship whose current account had a balance of ₹4 lakh when he died. His legal heirs "
  "were paid four months later. Under RBI's Commercial Banks – Interest Rate on Deposits Directions, 2025, what "
  "interest is due on this current account balance?",
  ["Interest at the savings deposit rate, from the date of death until repayment to the claimants",
   "No interest, because no interest is payable on current accounts",
   "Interest at the bank's one-year term deposit rate, from the date of the claim",
   "Interest at the savings deposit rate, only for the period beyond 15 days after the claim"],
  concept="Current accounts of deceased depositors",
  explanation="Normally no interest is paid on current accounts. But the Directions provide that balances in a current "
              "account of a deceased individual depositor or a sole proprietorship concern earn interest at the "
              "savings deposit rate applicable on the date of payment, from the date of death until repayment to the "
              "claimants.",
  steps=["General rule: no interest on current accounts", "Exception: deceased individual / sole proprietorship",
         "Savings rate from date of death till payment"],
  why="The general no-interest rule has this exception; the term deposit rate and a 15-day start are not in the "
      "provision.",
  facts=[fact("Para 8: No interest shall be paid on deposits held in current accounts. Provided that balances lying in "
              "current account standing in the name of a deceased individual depositor or sole proprietorship concern "
              "shall attract interest at the savings deposit rate from the date of death till the date of repayment "
              "to the claimants.", A_DEPINT)])
Q(T, "Types of banks", "Intermediate",
  "Under RBI's Universal Banks – Licensing Guidelines, 2025, promoters of a new bank must initially hold at least "
  "40 per cent of its paid-up voting equity, locked in for five years. To what level must this holding be brought "
  "down, and within what period?",
  ["26 per cent, within 15 years", "15 per cent, within 12 years", "26 per cent, within 10 years",
   "10 per cent, within 15 years"],
  concept="Promoter shareholding in new banks",
  explanation="The guidelines require promoters to hold at least 40% of the paid-up voting equity, locked in for five "
              "years from the commencement of business, and to bring it down to 26% within 15 years. The bank must "
              "also list its shares within six years and have minimum paid-up voting equity of ₹1,000 crore.",
  steps=["Initial: ≥ 40%, locked in 5 years", "Dilute to 26% within 15 years"],
  why="15% in 12 years, 26% in 10 years and 10% in 15 years do not match the guidelines.",
  facts=[fact("Para 15(1): a minimum of 40 per cent of the paid-up voting equity share capital of the bank ... locked "
              "in for five years. Para 15(4): shall be brought down to 26 per cent of the paid-up voting equity share "
              "capital of the bank within a period of 15 years.", A_UNIV)])

dep1, rate_card, penalty, yrs = 200000, 7.00, 1.00, 2
int1 = dep1 * (rate_card - penalty) / 100 * yrs
assert int1 == 24000
contracted = dep1 * 7.25 / 100 * yrs
assert contracted == 29000 and dep1 * rate_card / 100 * yrs == 28000
Q(T, "Types of accounts", "Advanced",
  "Meena, an individual, placed two term deposits with a bank. (a) ₹2,00,000 for 3 years at 7.25%, which she "
  "withdrew after exactly 2 years; when it was made, the bank's rate for a 2-year deposit was 7.00% and its "
  "premature-withdrawal penalty is 1 percentage point. (b) ₹50,000, which she withdrew after 5 days. Assuming simple "
  "interest, what total interest will she receive under RBI's Interest Rate on Deposits Directions, 2025?",
  ["₹24,000", "₹29,000", "₹28,000", "₹24,034"],
  concept="Premature withdrawal of term deposits",
  explanation="On premature withdrawal, interest is paid at the rate applicable to the amount and period for which "
              "the deposit actually remained with the bank, not the contracted rate, less the disclosed penalty: "
              "2,00,000 × (7.00% − 1%) × 2 = ₹24,000. The second deposit was withdrawn before the 7-day minimum "
              "tenor, so no interest is paid on it.",
  steps=["Deposit (a): rate for 2 years 7.00% − penalty 1% = 6%", "2,00,000 × 6% × 2 = ₹24,000",
         "Deposit (b): withdrawn before 7 days → no interest", "Total ₹24,000"],
  why="₹29,000 uses the contracted 7.25%; ₹28,000 ignores the penalty; ₹24,034 wrongly pays interest on the 5-day "
      "deposit.",
  facts=[fact("Para 11(1): Interest shall be paid at the rate applicable to the amount and period for which the deposit "
              "remained with the bank and not at the contracted rate. Para 11(2): No interest shall be paid, where "
              "premature withdrawal of deposit takes place before completion of the minimum period specified in "
              "paragraph 10(1).", A_DEPINT),
         fact("Para 10(1): the minimum tenor of the deposit offered shall be seven days.", A_DEPINT)],
  computed=True)

chq = 75000
info_day, notice_window = 25, 30
notice_last = info_day + notice_window - 31     # March has 31 days -> day in April
assert notice_last == 24
notice_recd, pay_window = 2, 15
assert notice_recd + pay_window == 17
assert 2 * chq == 150000
Q(T, "Cheques and instruments", "Advanced",
  "A cheque for ₹75,000 is returned unpaid for insufficient funds, and the payee receives this information from the "
  "bank on 25 March 2026. The payee's written demand notice reaches the drawer on 2 April 2026. Under Section 138 of "
  "the Negotiable Instruments Act, 1881, which statement is correct?",
  ["The notice had to be given by 24 April 2026; an offence arises if the drawer does not pay by 17 April 2026, and the "
   "fine can extend to ₹1,50,000",
   "The notice had to be given by 9 April 2026; an offence arises if the drawer does not pay by 2 May 2026, and the "
   "fine can extend to ₹75,000",
   "The notice had to be given by 24 April 2026; an offence arises if the drawer does not pay by 2 May 2026, and the "
   "fine can extend to ₹2,25,000",
   "The notice had to be given by 9 April 2026; an offence arises if the drawer does not pay by 17 April 2026, and the "
   "fine can extend to ₹1,50,000"],
  concept="Dishonour of cheques (Section 138)",
  explanation="Section 138 applies only if the payee makes a written demand within 30 days of receiving the bank's "
              "information about the dishonour (25 March + 30 days = 24 April) and the drawer fails to pay within "
              "15 days of receiving the notice (2 April + 15 days = 17 April). The punishment is imprisonment up to "
              "two years, or a fine up to twice the cheque amount (2 × ₹75,000 = ₹1,50,000), or both.",
  steps=["Notice: within 30 days of 25 March → by 24 April", "Payment: within 15 days of 2 April → by 17 April",
         "Fine: up to 2 × ₹75,000 = ₹1,50,000"],
  why="A 15-day notice window gives 9 April and a 30-day payment window gives 2 May, both wrong; the fine ceiling is "
      "twice, not once or thrice, the cheque amount.",
  facts=[fact("Section 138: punishable with imprisonment for a term which may extend to two years, or with fine which "
              "may extend to twice the amount of the cheque, or with both ... the payee ... makes a demand ... by "
              "giving a notice in writing to the drawer of the cheque, within thirty days of the receipt of "
              "information by him from the bank ... and the drawer of such cheque fails to make the payment ... "
              "within fifteen days of the receipt of the said notice.", A_NI138)],
  computed=True)

# ================= History of Banking in India (Basic 1 / Intermediate 3 / Advanced 4)
T = "History of Banking in India"
Q(T, "Committees", "Basic",
  "The Committee on Customer Service in Banks, set up by RBI in 2010 to examine services to retail and small "
  "customers including pensioners, was chaired by:",
  ["M. Damodaran", "M. S. Verma", "P. J. Nayak", "S. S. Tarapore"],
  concept="Customer service committees",
  explanation="RBI constituted the Committee on Customer Service in Banks in 2010 under Shri M. Damodaran, former "
              "Chairman of SEBI, to look into services to retail and small customers, grievance redressal and the "
              "Banking Ombudsman Scheme.",
  steps=["2010 customer service committee → M. Damodaran (former SEBI Chairman)"],
  why="M. S. Verma chaired the 1999 working group on weak public sector banks; P. J. Nayak reviewed bank board "
      "governance (2014); the Tarapore Committee's 2004 recommendations concerned board-level customer service "
      "committees.",
  facts=[fact("Committee on Customer Service in Banks ... Chairman: Shri M. Damodaran, former Chairman, SEBI ... "
              "constituted by Board Memorandum dated May 26, 2010.", A_DAMO)])
Q(T, "Committees", "Intermediate",
  "The Working Group on Restructuring Weak Public Sector Banks (1999), chaired by M. S. Verma, identified which three "
  "banks as weak?",
  ["Indian Bank, UCO Bank and United Bank of India", "Indian Bank, Dena Bank and Vijaya Bank",
   "UCO Bank, Central Bank of India and Bank of Maharashtra", "United Bank of India, Syndicate Bank and Andhra Bank"],
  concept="Verma Working Group",
  explanation="RBI, in consultation with the Government, set up the working group under M. S. Verma, former SBI "
              "Chairman. Its report (October 1999) identified Indian Bank, UCO Bank and United Bank of India as weak "
              "banks and proposed a comprehensive restructuring of them.",
  steps=["Verma group (1999) → weak PSBs", "Indian Bank, UCO Bank, United Bank of India"],
  why="Each wrong option includes banks that the working group did not classify as weak.",
  facts=[fact("Report of the Working Group on Restructuring Weak Public Sector Banks, chaired by Shri M.S. Verma, "
              "former Chairman, State Bank of India ... the three banks identified as weak: Indian Bank, UCO Bank and "
              "United Bank of India.", A_VERMA)])
Q(T, "Mergers and consolidation", "Intermediate",
  "Global Trust Bank, a new-generation private bank, was placed under a moratorium on 24 July 2004. With which bank "
  "did RBI draft a scheme to amalgamate it?",
  ["Oriental Bank of Commerce", "Punjab National Bank", "ICICI Bank", "Bank of Baroda"],
  concept="Compulsory amalgamations",
  explanation="After Global Trust Bank (GTB) was put under a moratorium on 24 July 2004, RBI prepared a draft scheme "
              "of amalgamation of GTB with Oriental Bank of Commerce, keeping in view the interests of GTB's "
              "depositors; the scheme took effect in August 2004.",
  steps=["GTB moratorium: 24 July 2004", "Draft scheme: GTB with OBC"],
  why="PNB, ICICI Bank and Bank of Baroda were not parties to the GTB scheme.",
  facts=[fact("Global Trust Bank Ltd. was placed under an Order of Moratorium on July 24, 2004 ... the Reserve Bank has "
              "prepared a draft scheme of amalgamation of GTB with OBC.", A_GTB),
         fact("Scheme for Amalgamation of Global Trust Bank Ltd. with Oriental Bank of Commerce", A_GTBN)])
Q(T, "Mergers and consolidation", "Intermediate",
  "In 2003, which Kerala-based private sector bank was amalgamated with Punjab National Bank?",
  ["Nedungadi Bank", "Lord Krishna Bank", "Catholic Syrian Bank", "Bank of Cochin"],
  concept="Amalgamations of private banks",
  explanation="PNB's heritage record notes that the erstwhile Nedungadi Bank Ltd, a Kerala-based private bank, was "
              "amalgamated with Punjab National Bank in 2003.",
  steps=["2003 → Nedungadi Bank Ltd amalgamated with PNB"],
  why="Lord Krishna Bank, Catholic Syrian Bank and Bank of Cochin were not the bank amalgamated with PNB in 2003.",
  facts=[fact("In 2003, the erstwhile Nedungadi Bank Ltd (e-NBL), a Kerala based private bank was amalgamated with "
              "Punjab National Bank.", A_PNB)])
Q(T, "Committees", "Advanced",
  "Arrange the following customer-service milestones in chronological order: I. RBI appoints the Goiporia Committee on "
  "customer service in banks II. RBI constitutes the Committee on Customer Service in Banks under M. Damodaran "
  "III. The Government appoints the Talwar Committee on customer service in banks IV. Tarapore Committee "
  "recommendations lead to Board-level committees for monitoring customer service",
  ["III, I, IV, II", "I, III, IV, II", "III, IV, I, II", "III, I, II, IV"],
  concept="Customer service committees",
  explanation="The Damodaran Committee report recounts the history: Talwar Committee (1975, appointed by the "
              "Government of India), Goiporia Committee (1990, appointed by RBI), Tarapore Committee recommendations "
              "(2004) leading to Board-level customer service committees, and the Damodaran Committee itself (2010).",
  steps=["Talwar: 1975", "Goiporia: 1990", "Tarapore: 2004", "Damodaran: 2010"],
  why="The other orders misplace Talwar (the earliest), Tarapore (2004) or Damodaran (2010, the latest).",
  facts=[fact("In 1975, the Government of India had appointed the Talwar Committee on customer service in banks. In "
              "1990, RBI appointed the Goiporia Committee on customer service in banks. In 2004, the Tarapore "
              "Committee recommendations led to formation of Board level committees.", A_DAMO),
         fact("Committee on Customer Service in Banks ... constituted by Board Memorandum dated May 26, 2010.", A_DAMO)])

held = 1000
new_shares = held * 42 / 25
assert new_shares == 1680
Q(T, "Mergers and consolidation", "Advanced",
  "HDFC Ltd merged into HDFC Bank effective 1 July 2023 at a swap ratio of 42 HDFC Bank shares for every 25 HDFC Ltd "
  "shares. An investor held 1,000 HDFC Ltd shares on the record date. How many HDFC Bank shares did she get, and what "
  "was HDFC Bank's promoter position after the merger?",
  ["1,680 shares; HDFC Bank has no identified promoter",
   "1,680 shares; HDFC Ltd's successor remains the promoter",
   "595 shares; HDFC Bank has no identified promoter",
   "1,050 shares; the Government becomes the promoter"],
  concept="HDFC–HDFC Bank merger",
  explanation="Shareholders of HDFC Ltd received 42 HDFC Bank shares of ₹1 each for every 25 HDFC Ltd shares held on "
              "the record date (13 July 2023): 1,000 × 42/25 = 1,680. HDFC Bank says that after the merger it has no "
              "identified promoter.",
  steps=["1,000 × 42 / 25 = 1,680", "Post-merger: no identified promoter"],
  why="595 inverts the ratio (1,000 × 25/42); 1,050 has no basis; HDFC Ltd ceased to exist, and the Government was "
      "never the promoter.",
  facts=[fact("the merger would be effective from July 1, 2023 ... 42 new equity shares of the face value of Re. 1/- "
              "each ... for every 25 equity shares of HDFC Ltd. held ... as on the Record Date i.e., July 13, 2023 ... "
              "Post the merger, HDFC Bank has no identified promoter.", A_HDFC)],
  computed=True)
Q(T, "Nationalisation", "Advanced",
  "One of the six private banks nationalised in April 1980 (each with demand and time liabilities above ₹200 crore) "
  "later became, in 1993, the first nationalised bank ever merged into Punjab National Bank. Which bank was it?",
  ["New Bank of India", "Vijaya Bank", "Punjab and Sind Bank", "Andhra Bank"],
  concept="Second nationalisation and its sequel",
  explanation="The six banks nationalised in April 1980 were Andhra Bank, Corporation Bank, New Bank of India, "
              "Oriental Bank of Commerce, Punjab and Sind Bank and Vijaya Bank. New Bank of India was merged into "
              "PNB with effect from 4 September 1993, which PNB records as its first merger of a nationalised bank.",
  steps=["1980 list: Andhra, Corporation, New Bank of India, OBC, Punjab and Sind, Vijaya",
         "1993 merger into PNB → New Bank of India"],
  why="Vijaya Bank went to Bank of Baroda (2019), Andhra Bank to Union Bank of India (2020), and Punjab and Sind Bank "
      "is still a separate bank.",
  facts=[fact("nationalisation of six Indian private sector banks having demand and time liabilities exceeding Rs. 200 "
              "crores each as on March 14, 1980: Andhra Bank, Corporation Bank, New Bank of India, Oriental Bank of "
              "Commerce, Punjab and Sind Bank and Vijaya Bank.", A_1980),
         fact("The merger of New Bank of India with Punjab National Bank came into effect on 4 September 1993.", A_NBI),
         fact("The first ever and the only merger of a nationalized bank with PNB was in 1993.", A_PNB)])
Q(T, "Committees", "Advanced",
  "The Verma Working Group (1999) used seven parameters, along with two criteria of the Narasimham Committee on Banking "
  "Sector Reforms, to judge the health of public sector banks. Which of the following was NOT one of the seven?",
  ["Credit–deposit ratio", "Return on assets", "Cost to income ratio", "Staff cost to income ratio"],
  concept="Identifying weak banks",
  explanation="The seven parameters were capital adequacy, coverage ratio, return on assets, net interest margin, "
              "operating profit to average working funds, cost to income and staff cost to income. The group also "
              "proposed a government-owned Asset Reconstruction Fund managed by an independent AMC.",
  steps=["Seven parameters: CAR, coverage, RoA, NIM, operating profit/AWF, cost/income, staff cost/income",
         "Credit–deposit ratio is not among them"],
  why="Return on assets, cost to income and staff cost to income are all among the seven parameters.",
  facts=[fact("Seven parameters: capital adequacy ratio, coverage ratio, return on assets, net interest margin, "
              "operating profit to average working funds, cost to income and staff cost to income ... along with the "
              "two criteria recommended by the Committee on Banking Sector Reforms.", A_VERMA)])

# ================= Reserve Bank of India (Basic 2 / Intermediate 4 / Advanced 1)
T = "Reserve Bank of India"
Q(T, "Governors and leadership", "Basic",
  "Who became the 23rd Governor of the Reserve Bank of India on 4 September 2013?",
  ["Dr. Raghuram Rajan", "Dr. D. Subbarao", "Dr. Urjit R. Patel", "Dr. Y. V. Reddy"],
  concept="RBI Governors",
  explanation="RBI's list of Governors shows Dr. Raghuram Rajan as the 23rd Governor, from 4 September 2013 to "
              "4 September 2016. He succeeded Dr. D. Subbarao and was followed by Dr. Urjit R. Patel.",
  steps=["22nd: D. Subbarao (2008–2013)", "23rd: Raghuram Rajan (2013–2016)", "24th: Urjit R. Patel (2016–2018)"],
  why="Subbarao (22nd) and Reddy (21st) served earlier; Patel (24th) took over in September 2016.",
  facts=[fact("23 Dr. Raghuram Rajan 04-09-2013 04-09-2016", A_GOVS)])
Q(T, "Establishment and structure", "Basic",
  "Under Section 4 of the Reserve Bank of India Act, 1934, the capital of the Reserve Bank is:",
  ["₹5 crore", "₹100 crore", "₹50 crore", "₹500 crore"],
  concept="RBI's capital",
  explanation="Section 4 of the RBI Act states that the capital of the Bank shall be five crores of rupees. Since "
              "nationalisation in 1949 this capital is wholly owned by the Central Government.",
  steps=["Section 4 → capital ₹5 crore"],
  why="₹50 crore, ₹100 crore and ₹500 crore are not the statutory capital.",
  facts=[fact("Section 4: The capital of the Bank shall be five crores of rupees.", A_RBIACT)])
Q(T, "Establishment and structure", "Intermediate",
  "Under Section 13 of the RBI Act, 1934, meetings of RBI's Central Board must be convened by the Governor at least:",
  ["Six times in each year, and at least once in each quarter", "Four times in each year, once in each quarter",
   "Twelve times in each year, once a month", "Twice in each year, once in each half-year"],
  concept="Central Board meetings",
  explanation="Section 13 requires the Governor to convene Central Board meetings at least six times in each year and "
              "at least once in each quarter.",
  steps=["Section 13 → at least 6 meetings a year", "At least one in each quarter"],
  why="Four, twelve and two meetings a year are not the statutory minimum.",
  facts=[fact("Section 13: Meetings of the Central Board shall be convened by the Governor at least six times in each "
              "year and at least once in each quarter.", A_RBIACT)])
Q(T, "Governors and leadership", "Intermediate",
  "Under Section 8(4) of the RBI Act, 1934, for what term do the Governor and a Deputy Governor hold office?",
  ["For a term not exceeding five years fixed by the Central Government, with eligibility for re-appointment",
   "For a fixed term of three years, with one extension of two years",
   "For a term not exceeding four years, like other directors, without re-appointment",
   "Until the age of 65 years, as decided by the Central Board"],
  concept="Tenure of Governor",
  explanation="Section 8(4) provides that the Governor and a Deputy Governor hold office for such term not exceeding "
              "five years as the Central Government may fix when appointing them, and are eligible for "
              "re-appointment. (The four-year term applies to nominated directors.)",
  steps=["Term fixed by the Central Government", "Ceiling: 5 years", "Re-appointment allowed"],
  why="The Act does not fix a three-year term or an age limit; the four-year term is for nominated directors.",
  facts=[fact("Section 8(4): The Governor and a Deputy Governor shall hold office for such term not exceeding five "
              "years as the Central Government may fix when appointing them, and shall be eligible for "
              "re-appointment.", A_RBIACT)])
Q(T, "Governors and leadership", "Intermediate",
  "Which of the following pairs of RBI Governors is correctly shown as predecessor → immediate successor?",
  ["Dr. Y. V. Reddy → Dr. D. Subbarao", "Dr. Bimal Jalan → Dr. C. Rangarajan", "Dr. Raghuram Rajan → Dr. D. Subbarao",
   "Dr. Urjit R. Patel → Dr. Raghuram Rajan"],
  concept="Succession of RBI Governors",
  explanation="RBI's list shows Rangarajan (1992–1997), Jalan (1997–2003), Reddy (6 September 2003 – 5 September 2008), "
              "Subbarao (5 September 2008 – 4 September 2013), Rajan (2013–2016) and Patel (2016–2018). So Reddy was "
              "succeeded by Subbarao.",
  steps=["Order: Rangarajan → Jalan → Reddy → Subbarao → Rajan → Patel → Das"],
  why="The other three pairs are reversed: Rangarajan preceded Jalan, Subbarao preceded Rajan, and Rajan preceded "
      "Patel.",
  facts=[fact("19 Dr. C Rangarajan 22-12-1992 22-11-1997; 20 Dr. Bimal Jalan 22-11-1997 06-09-2003; 21 Dr. Y V Reddy "
              "06-09-2003 05-09-2008; 22 Dr. D. Subbarao 05-09-2008 04-09-2013; 23 Dr. Raghuram Rajan 04-09-2013 "
              "04-09-2016; 24 Dr. Urjit R. Patel 04-09-2016 11-12-2018", A_GOVS)])
Q(T, "Establishment and structure", "Intermediate",
  "At its 623rd meeting on 22 May 2026, RBI's Central Board approved what amount as surplus transfer to the Central "
  "Government for the accounting year 2025-26?",
  ["₹2,86,588.46 crore", "₹2,48,700 crore", "₹1,09,379.64 crore", "₹3,95,972.10 crore"],
  concept="RBI's surplus transfer",
  explanation="The Board, chaired by Governor Sanjay Malhotra in Mumbai, approved a record surplus transfer of "
              "₹2,86,588.46 crore for 2025-26, after transferring ₹1,09,379.64 crore to the Contingent Risk Buffer.",
  steps=["623rd Central Board meeting, 22 May 2026", "Surplus to Government: ₹2,86,588.46 crore"],
  why="₹1,09,379.64 crore is the amount transferred to the Contingent Risk Buffer, not to the Government; "
      "₹2,48,700 crore and ₹3,95,972.10 crore are not the surplus the Board approved.",
  facts=[fact("The Board approved the transfer of surplus of ₹2,86,588.46 crore to the Central Government for the "
              "accounting year 2025-26.", A_SURP)],
  current=ca("2026-05-22"))
Q(T, "Establishment and structure", "Advanced",
  "Consider the following statements about the decisions of RBI's Central Board on 22 May 2026: I. Under the revised "
  "Economic Capital Framework, the Contingent Risk Buffer (CRB) can be held between 4.5% and 7.5% of the size of "
  "RBI's balance sheet. II. The Board decided to keep the CRB at the top of this range, 7.5% of the balance sheet. "
  "III. The Board transferred ₹1,09,379.64 crore towards the CRB for 2025-26. Which of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="Economic Capital Framework",
  explanation="RBI's release says the revised ECF allows the CRB to be maintained between 4.5% and 7.5% of the balance "
              "sheet; the Board decided to transfer ₹1,09,379.64 crore to the CRB and to maintain it at 6.5%, not "
              "7.5%. The surplus transferred to the Government was ₹2,86,588.46 crore.",
  steps=["I: range 4.5%–7.5% → correct", "II: CRB kept at 6.5% → incorrect", "III: ₹1,09,379.64 crore → correct"],
  why="Any option that includes II is wrong because the CRB was kept at 6.5%.",
  facts=[fact("the Board decided to transfer ₹1,09,379.64 crore towards the CRB for FY 2025-26 ... maintain the CRB at "
              "6.5 per cent of the Balance Sheet size ... between the range of 4.5 per cent and 7.5 per cent of the "
              "size of the Balance Sheet.", A_SURP)],
  current=ca("2026-05-22"))

# ================= RBI Functions (Basic 2 / Intermediate 3 / Advanced 2)
T = "RBI Functions"
Q(T, "Issuer of currency", "Basic",
  "Under Section 23 of the RBI Act, 1934, the issue of bank notes is conducted by RBI in:",
  ["An Issue Department, kept wholly separate from the Banking Department",
   "The Department of Currency Management of the Ministry of Finance",
   "The Banking Department, together with Government business",
   "Its wholly owned subsidiary, Bharatiya Reserve Bank Note Mudran"],
  concept="Issue and Banking Departments",
  explanation="Section 23 provides that the issue of bank notes shall be conducted by the Bank in an Issue Department, "
              "which shall be separated and kept wholly distinct from the Banking Department.",
  steps=["Section 23 → Issue Department", "Separate from the Banking Department"],
  why="The Finance Ministry does not issue notes; the Banking Department handles banking business; BRBNMPL only prints "
      "notes.",
  facts=[fact("Section 23: The issue of bank notes shall be conducted by the Bank in an Issue Department which shall be "
              "separated and kept wholly distinct from the Banking Department.", A_RBIACT)])
Q(T, "Issuer of currency", "Basic",
  "Under Section 26(2) of the RBI Act, 1934, how can a series of bank notes of any denomination be made to cease to be "
  "legal tender?",
  ["By a Central Government notification in the Gazette, on the recommendation of RBI's Central Board",
   "By a resolution of RBI's Central Board alone, without Government involvement",
   "By an Act of Parliament amending the Coinage Act, 2011",
   "By an order of the RBI Governor with the approval of the President"],
  concept="Demonetisation power",
  explanation="Section 26(2) empowers the Central Government, on the recommendation of the Central Board, to declare "
              "by notification in the Gazette of India that any series of bank notes of any denomination shall cease "
              "to be legal tender.",
  steps=["Central Board recommends", "Central Government notifies in the Gazette"],
  why="The Central Board cannot act alone; the Coinage Act deals with coins; there is no Governor-President route.",
  facts=[fact("Section 26(2): On recommendation of the Central Board the Central Government may, by notification in the "
              "Gazette of India, declare that ... any series of bank notes of any denomination shall cease to be legal "
              "tender.", A_RBIACT)])
Q(T, "Regulator and supervisor", "Intermediate",
  "The Banking Laws (Amendment) Act, 2025 raised the maximum tenure of directors of co-operative banks (other than the "
  "chairperson and whole-time director) from 8 years to:",
  ["10 years", "12 years", "9 years", "15 years"],
  concept="Banking Laws (Amendment) Act, 2025",
  explanation="The Act, whose key provisions came into force on 1 August 2025, raised the maximum tenure of directors "
              "of co-operative banks, excluding the chairperson and whole-time director, from 8 to 10 years, in "
              "Section 10A of the Banking Regulation Act.",
  steps=["Earlier cap: 8 years", "New cap for co-operative banks: 10 years"],
  why="12, 9 and 15 years are not the new limit.",
  facts=[fact("increasing the maximum tenure from 8 years to 10 years (excluding the chairperson and whole-time "
              "director)", A_BLA_AIR),
         fact("Ministry of Finance appointed 1-8-2025 as the date on which certain provisions of the Banking Laws "
              "(Amendment) Act, 2025 come into force ... Section 10-A ... Board of directors to include persons with "
              "professional or other experience.", A_BLA)])
Q(T, "Regulator and supervisor", "Intermediate",
  "Under RBI's Commercial Banks – Governance Directions, 2025, an MD & CEO of a private sector bank who is also its "
  "promoter can hold the post for at most how long (except when RBI allows more in extraordinary circumstances)?",
  ["12 years", "15 years", "10 years", "8 years"],
  concept="Tenure of MD & CEO in private banks",
  explanation="The posts of MD & CEO or WTD cannot be held by the same person for more than 15 years (re-appointment "
              "possible after three years), with an upper age limit of 70. An MD & CEO or WTD who is a promoter or "
              "major shareholder cannot hold the post for more than 12 years, which RBI may extend to 15 in "
              "extraordinary circumstances.",
  steps=["General cap: 15 years; age limit 70", "Promoter/major shareholder: 12 years"],
  why="15 years is the general cap; 8 years is the cap on non-executive directors; 10 years is not prescribed.",
  facts=[fact("Para 50: shall not hold these posts for more than 12 years ... Para 48: shall not be held by the same "
              "incumbent for more than 15 years ... Para 44(viii): The total tenure of an NED ... shall not exceed "
              "eight years.", A_GOVN)])
Q(T, "Banker to government", "Intermediate",
  "RBI took over the general banking business of the Government of NCT of Delhi with effect from 9 January 2026. What "
  "Ways and Means Advances (WMA) limit did it fix for Delhi, and what did the aggregate WMA limit of States/UTs become?",
  ["₹890 crore; ₹61,008 crore", "₹890 crore; ₹60,118 crore", "₹1,780 crore; ₹61,898 crore",
   "₹600 crore; ₹60,718 crore"],
  concept="RBI as banker to State Governments",
  explanation="After an agreement with GNCTD on 5 January 2026, RBI took over its general banking business from 9 "
              "January 2026 and fixed its WMA limit at ₹890 crore. The aggregate WMA limit of States/UTs therefore "
              "rose from ₹60,118 crore (set in the review of 28 June 2024) to ₹61,008 crore.",
  steps=["Delhi WMA limit: ₹890 crore", "Aggregate: 60,118 + 890 = ₹61,008 crore"],
  why="₹60,118 crore was the aggregate before Delhi was added; ₹1,780 crore and ₹600 crore are not Delhi's limit, and "
      "the matching aggregates follow from those wrong figures.",
  current=ca("2026-01-09"),
  facts=[fact("The WMA limit for GNCTD have been fixed at ₹890 crore, effective from January 09, 2026. Accordingly, the "
              "revised aggregate WMA limit for State Governments / UTs will be ₹61,008 crore as against the existing "
              "limit of ₹60,118 crore.", A_WMA26)])

csf_old, csf_now, atb_old, atb_now = 8000, 9200, 1200, 900
sdf = 0.5 * min(csf_old, csf_now) + 0.5 * min(atb_old, atb_now)
assert sdf == 4450
assert 0.5 * (csf_now + atb_now) == 5050 and 0.5 * (csf_old + atb_old) == 4600
Q(T, "Banker to government", "Advanced",
  "A State Government's balance in its Consolidated Sinking Fund and Guarantee Redemption Fund was ₹8,000 crore on the "
  "last date of the second preceding quarter and is ₹9,200 crore now. Its Auction Treasury Bill holdings were "
  "₹1,200 crore on that date and are ₹900 crore now. Under the Special Drawing Facility (SDF) rule in RBI's release of "
  "28 June 2024 (effective 1 July 2024), what is its maximum SDF?",
  ["₹4,450 crore", "₹5,050 crore", "₹4,600 crore", "₹4,000 crore"],
  concept="Special Drawing Facility for States",
  explanation="For each type of investment, the maximum SDF is 50% of the lower of the balance on the last date of the "
              "second preceding quarter and the current balance. CSF/GRF: 50% × min(8,000, 9,200) = 4,000. ATBs: "
              "50% × min(1,200, 900) = 450. Total = ₹4,450 crore.",
  steps=["CSF/GRF: 50% × 8,000 = 4,000", "ATB: 50% × 900 = 450", "Total = ₹4,450 crore"],
  why="₹5,050 crore uses the current balances; ₹4,600 crore uses the old balances; ₹4,000 crore ignores the ATBs.",
  facts=[fact("the maximum limit of SDF ... against investments in CSF/GRF shall be 50 per cent of the lower of the "
              "outstanding balance of the funds as on the last date of the second preceding quarter and the current "
              "outstanding balance ... the same for investments in Auction Treasury Bills.", A_SDF)],
  computed=True)
Q(T, "Regulator and supervisor", "Advanced",
  "Consider the following statements about the Banking Laws (Amendment) Act, 2025: I. It amended five laws, including "
  "the RBI Act, 1934, the Banking Regulation Act, 1949 and the State Bank of India Act, 1955. II. It permits public "
  "sector banks to transfer unclaimed shares, interest and bond redemption amounts to the Investor Education and "
  "Protection Fund. III. It raised the maximum continuous tenure of the chairperson of a co-operative bank to 10 years. "
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Banking Laws (Amendment) Act, 2025",
  explanation="The Act amended five laws: the RBI Act, the BR Act, the SBI Act and the two Banking Companies "
              "(Acquisition and Transfer of Undertakings) Acts of 1970 and 1980. It lets PSBs transfer unclaimed "
              "shares, interest and bond redemption amounts to the IEPF and pay statutory auditors. The tenure increase "
              "from 8 to 10 years for co-operative bank directors excludes the chairperson and whole-time director.",
  steps=["I: five Acts → correct", "II: IEPF transfers → correct", "III: chairperson excluded → incorrect"],
  why="Any option that includes III is wrong because the 10-year limit excludes the chairperson.",
  facts=[fact("This Act brought amendments in 5 legislations: Reserve Bank of India Act, 1934; Banking Regulation Act, "
              "1949; State Bank of India Act, 1955; Banking Companies (Acquisition and Transfer of Undertakings) Acts "
              "1970 and 1980 ... Public Sector Banks will now be permitted to transfer unclaimed shares, interest, and "
              "bond redemption amounts to the Investor Education and Protection Fund.", A_BLA),
         fact("increasing the maximum tenure from 8 years to 10 years (excluding the chairperson and whole-time "
              "director)", A_BLA_AIR)])


# ######## section B
# ---- sources (group B), opened 2026-11-06
B_P = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid="
B_MIN = B_P + "63839"        # Minutes of the MPC meeting, October 5 to 7, 2026 (published 21 Oct 2026)
B_MMO = B_P + "63912"        # Money Market Operations as on November 03, 2026 (press release 2026-2027/1434)
B_VRRR = B_P + "63913"       # Result of the Overnight VRRR auction held on November 04, 2026 (first auction)
B_MPR = "https://www.rbi.org.in/Scripts/PublicationsView.aspx?id=24085"   # Monetary Policy Report - October 2026
B_MPF = "https://www.rbi.org.in/Scripts/FS_Overview.aspx?fn=2752"          # RBI monetary policy framework page
B_AMD = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13224&Mode=0"  # CRR & SLR Amendment Directions, 11 Dec 2025
B_CPI = ("https://www.mospi.gov.in/uploads/latestreleasesfiles/1791801549227-Press%20Release%20for%20the%20month%20of"
         "%20September,%202026.pdf")   # MoSPI CPI (2024=100) press release for September 2026, dated 12 Oct 2026
B_WPI = ("https://www.devdiscourse.com/article/business/3992075-wpi-inflation-climbs-to-1139-in-september-from-992-"
         "in-august")      # news report of the WPI release for September 2026 (eaindustry.nic.in did not open: TLS error)
B_L = "https://lawx.in/acts/section/48/"   # bare-act text of the RBI Act, 1934
B_45ZC = B_L + "489/4741"    # Section 45ZC: eligibility and selection of Government-appointed members
B_45ZD = B_L + "489/4742"    # Section 45ZD: terms and conditions of appointment
B_45ZE = B_L + "489/4743"    # Section 45ZE: removal of members
B_45ZG = B_L + "489/4745"    # Section 45ZG: Secretary to the MPC
B_45ZI = B_L + "489/4747"    # Section 45ZI: meetings of the MPC
B_45ZJ = B_L + "489/4748"    # Section 45ZJ: steps to implement MPC decisions
B_MPOV = "https://www.rbi.org.in/Scripts/FS_Overview.aspx?fn=2752"   # RBI Monetary Policy overview: instruments of monetary policy
B_PEN26 = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=13728&Mode=0"   # Penal interest on shortfall in CRR and SLR - Change in Bank Rate, 7 Oct 2026
B_S42 = B_L + "483/4691"     # Section 42: cash reserves of scheduled banks
B_S49 = B_L + "490/4760"     # Section 49: publication of Bank rate
B_HOME = "https://www.rbi.org.in/"   # current rates panel (Repo 5.50, SDF 5.25, MSF 5.75, Bank Rate 5.75, CRR 3.00, SLR 18.00)

# ================= Monetary Policy (Basic 4 / Intermediate 4 / Advanced 3)
T = "Monetary Policy"
Q(T, "MPC structure", "Basic",
  "The three Government-appointed members of the Monetary Policy Committee are chosen on the recommendation of a "
  "Search-cum-Selection Committee under Section 45ZC of the RBI Act, 1934. Who chairs that committee?",
  ["The Cabinet Secretary", "The Governor of RBI", "The Secretary, Department of Economic Affairs",
   "The Union Finance Minister"],
  concept="Selection of external MPC members",
  explanation="Section 45ZC(2) sets up a Search-cum-Selection Committee chaired by the Cabinet Secretary. Its members "
              "are the RBI Governor (or his representative not below the rank of Deputy Governor), the Secretary of "
              "the Department of Economic Affairs and three experts nominated by the Central Government.",
  steps=["External members are appointed by the Central Government", "On the recommendation of a committee chaired "
         "by the Cabinet Secretary"],
  why="The Governor and the DEA Secretary are members of the selection committee, not its chair; the Finance Minister "
      "is not on it.",
  facts=[fact("Cabinet Secretary--Chairperson; Governor of the Reserve Bank of India or his representative (not below "
              "the rank of Deputy Governor)--member; Secretary, Department of Economic Affairs--member", B_45ZC)])
Q(T, "MPC structure", "Basic",
  "Under Section 45ZD of the RBI Act, 1934, what is the term of a Government-appointed member of the Monetary Policy "
  "Committee?",
  ["Four years, without eligibility for re-appointment", "Three years, with one re-appointment allowed",
   "Five years, with eligibility for re-appointment", "Until the age of 65 years, whichever is earlier"],
  concept="Tenure of external MPC members",
  explanation="Section 45ZD(1) gives the Government-appointed members a four-year term and bars re-appointment, which "
              "protects their independence. Their remuneration is set by regulations of RBI's Central Board.",
  steps=["Term: four years", "Re-appointment: not allowed"],
  why="The Act fixes four years, not three or five, and expressly rules out re-appointment; it does not fix tenure by "
      "age.",
  facts=[fact("Members ... shall hold office for a period of four years and shall not be eligible for "
              "re-appointment.", B_45ZD)])
Q(T, "MPC structure", "Basic",
  "Under Section 45ZI of the RBI Act, 1934, who presides over a meeting of the Monetary Policy Committee if the "
  "Governor is absent?",
  ["The Deputy Governor who is a member of the MPC", "The senior-most Government-appointed member",
   "A member elected by those present", "The RBI officer nominated by the Central Board"],
  concept="Conduct of MPC meetings",
  explanation="The Governor presides over MPC meetings; in his absence the Deputy Governor who is a member of the MPC "
              "(the Deputy Governor in charge of monetary policy) presides. The quorum is four members.",
  steps=["Chair: Governor", "In his absence: the Deputy Governor-member"],
  why="The Act does not give the chair to an external member, to an elected member or to the Board-nominated RBI "
      "officer.",
  facts=[fact("The meetings of the Monetary Policy Committee shall be presided over by the Governor and, in his "
              "absence, by the Deputy Governor who is the Member of the Monetary Policy Committee (Section 45ZI(6), "
              "as summarised on the page).", B_45ZI)])
Q(T, "Policy stance", "Basic",
  "At the October 2026 MPC meeting, Dr. Nagesh Kumar voted for the 25 bps repo rate increase but wanted to retain "
  "the neutral stance. What reason did he give in the minutes?",
  ["Continued geopolitical and trade policy uncertainties",
   "Inflation had already fallen below the 4% target",
   "Bank credit growth had slowed sharply",
   "The rupee had appreciated too fast against the dollar"],
  concept="Policy stance and dissent",
  explanation="The minutes of 5–7 October 2026 show two members, Dr. Nagesh Kumar and Prof. Ram Singh, preferring a "
              "neutral stance. Dr. Kumar said a neutral stance remained appropriate in view of continued geopolitical "
              "and trade policy uncertainties, which call for flexibility.",
  steps=["Rate decision unanimous (+25 bps)", "Stance: Dr. Kumar preferred neutral, citing uncertainties"],
  why="Inflation was above 4% (4.8% in August), credit growth was strong, and he did not cite the rupee.",
  current=ca("2026-10-21"),
  facts=[fact("in view of the continued geopolitical and trade policy uncertainties, I feel that a neutral stance "
              "remains appropriate", B_MIN)])

Q(T, "MPC structure", "Intermediate",
  "Under Section 45ZE of the RBI Act, 1934, which of the following is a ground on which the Central Government may "
  "remove a member of the Monetary Policy Committee?",
  ["Not attending three consecutive MPC meetings without prior leave",
   "Voting against the Governor at two consecutive meetings",
   "Dissenting on the policy stance in the published minutes",
   "Failing to meet the inflation target for three consecutive quarters"],
  concept="Removal of MPC members",
  explanation="Section 45ZE lists grounds such as insolvency, incapacity, conviction for moral turpitude, undisclosed "
              "conflict of interest, abuse of position, and absence from three consecutive MPC meetings without prior "
              "leave. Voting or dissent is a member's right; missing the inflation target triggers a report by RBI "
              "under Section 45ZN, not removal of a member.",
  steps=["Recall the Section 45ZE list", "Only absence without leave appears there"],
  why="Votes and dissents are recorded and published as part of the process; target failure leads to a report to the "
      "Government, not removal.",
  facts=[fact("does not attend three consecutive meetings of the Monetary Policy Committee without obtaining prior "
              "leave", B_45ZE)])
Q(T, "Policy stance", "Intermediate",
  "Prof. Ram Singh supported the 25 bps repo rate increase of October 2026 but opposed changing the stance to "
  "'calibrated tightening'. According to the minutes, why?",
  ["It might signal an extended cycle of rate hikes",
   "He believed the repo rate should have been cut instead",
   "He wanted the stance changed to accommodative",
   "He felt a stance should be announced only in the Monetary Policy Report"],
  concept="Signalling role of the stance",
  explanation="The stance signals the likely direction of future rate moves. Prof. Ram Singh favoured a mild hike "
              "because real rates would turn negative, but said that shifting from neutral to tightening may signal "
              "an extended cycle of rate hikes.",
  steps=["Rate: voted for +25 bps", "Stance: wanted neutral, fearing a signal of prolonged hikes"],
  why="He voted for the hike, not a cut; he did not seek an accommodative stance; the stance is part of the MPC "
      "resolution, not an MPR-only item.",
  current=ca("2026-10-21"),
  facts=[fact("I do not favour shifting the stance from neutral to tightening mode, as it may signal an extended "
              "cycle of rate hikes.", B_MIN)])
Q(T, "Transmission", "Intermediate",
  "The Monetary Policy Report of October 2026 lists the baseline assumptions behind RBI's projections. Which set "
  "matches it?",
  ["Crude oil US$95 a barrel in H2:2026-27 and US$85 in 2027-28; exchange rate ₹95 per US$",
   "Crude oil US$85 a barrel in H2:2026-27 and US$95 in 2027-28; exchange rate ₹88 per US$",
   "Crude oil US$116 a barrel in H2:2026-27 and US$95 in 2027-28; exchange rate ₹95 per US$",
   "Crude oil US$70 a barrel throughout; exchange rate ₹85 per US$"],
  concept="Assumptions behind the projections",
  explanation="Table V.2 of the October 2026 MPR assumes the Indian crude basket at US$95 a barrel in H2:2026-27 and "
              "US$85 in 2027-28, the rupee at ₹95 per US$ during 2026-27, a below-normal monsoon in 2026-27 and "
              "global growth of 3.0% in 2026. Oil and the exchange rate pass through to domestic prices.",
  steps=["Oil: 95 then 85 (US$ per barrel)", "Rupee: ₹95/US$"],
  why="The other sets reverse the oil path, use the realised September 2026 basket price (about US$116) as if it "
      "were the assumption, or give levels the MPR does not use.",
  current=ca("2026-10-07"),
  facts=[fact("US$95 per barrel during H2: 2026-27 and $85 per barrel during 2027-28 ... ₹ 95/US$ during 2026-27 "
              "(Table V.2, baseline assumptions)", B_MPR)])
Q(T, "MPC structure", "Intermediate",
  "What role does the Central Government have in the deliberations of the Monetary Policy Committee under Section "
  "45ZI of the RBI Act, 1934?",
  ["It may communicate its views to the MPC in writing from time to time",
   "Its nominee attends every meeting and has one vote",
   "It must approve the MPC's resolution before it is published",
   "It can veto a repo rate change within 14 days"],
  concept="Independence of the MPC",
  explanation="The Government sets the inflation target and appoints three members, but it does not sit in or vote "
              "at MPC meetings. Section 45ZI only allows it to send its views to the MPC in writing from time to "
              "time; the decision rests with the MPC.",
  steps=["Government: target-setting and appointments", "During deliberations: written views only"],
  why="No Government official is an MPC member, the resolution is published by RBI without Government approval, and "
      "the Act gives no veto.",
  facts=[fact("The Central Government may, from time to time, communicate in writing its views to the Monetary Policy "
              "Committee (Section 45ZI(9), as summarised on the page).", B_45ZI)])

Q(T, "MPC structure", "Advanced",
  "Consider the following statements about the monetary policy provisions of the RBI Act, 1934:\n"
  "I. RBI must publish the schedule of MPC meetings for a year at least one week before the first meeting of that "
  "year.\nII. The Secretary to the Monetary Policy Committee is appointed by the Central Government.\n"
  "III. RBI must publish a document explaining the steps it will take to implement the MPC's decisions.\n"
  "Which of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="Chapter IIIF of the RBI Act",
  explanation="Section 45ZI requires the annual schedule to be published at least a week before the first meeting. "
              "Section 45ZG says the Bank (RBI), not the Government, appoints the Secretary to the MPC. Section 45ZJ "
              "requires RBI to publish a document explaining the steps to implement MPC decisions.",
  steps=["I: Section 45ZI – true", "II: Section 45ZG – Secretary appointed by RBI – false",
         "III: Section 45ZJ – true"],
  why="Any option containing II is wrong because the Secretary is appointed by the Bank.",
  facts=[fact("The annual schedule must be published at least one week before the year's first meeting (Section "
              "45ZI(2), as summarised on the page).", B_45ZI),
         fact("The Bank shall appoint a Secretary to the Monetary Policy Committee.", B_45ZG),
         fact("The Bank shall publish a document explaining the steps to be taken by it to implement the decisions of "
              "the Monetary Policy Committee, including any changes thereto.", B_45ZJ)])
Q(T, "Policy stance", "Advanced",
  "Consider the following statements about Dr. Nagesh Kumar's statement in the minutes of the October 2026 MPC "
  "meeting:\nI. He noted that gross fixed capital formation was 34.3% in Q1:FY27, about 2.9 percentage points higher "
  "than in Q1:FY26.\nII. He argued that inflation was being driven mainly by demand-side overheating of the economy.\n"
  "III. He voted against the increase in the policy repo rate.\nWhich of the above is/are correct?",
  ["I only", "I and II only", "II and III only", "I and III only"],
  concept="Reading MPC minutes",
  explanation="Dr. Kumar cited GFCF of 34.3% in Q1:FY27 against 31.4% a year earlier (a 2.9 percentage point rise). "
              "He said inflation is driven largely by supply-side factors with no sign of overheating, and he voted "
              "for the 25 bps hike while preferring a neutral stance.",
  steps=["I: 34.3 − 31.4 = 2.9 pp – true", "II: he said supply-side, no overheating – false",
         "III: the hike was unanimous – false"],
  why="II reverses his diagnosis; III is wrong because all six members voted for the increase.",
  current=ca("2026-10-21"), computed=True,
  facts=[fact("a healthy rate of gross fixed capital formation (GFCF), which was 34.3% in Q1:FY27 compared to 31.4% in "
              "Q1:FY26.", B_MIN),
         fact("inflation is driven largely by supply-side factors and does not show any signs of overheating of the "
              "economy", B_MIN)])
assert round(34.3 - 31.4, 1) == 2.9
Q(T, "Policy stance", "Advanced",
  "Match each member of the MPC with an argument from his or her statement in the minutes of the October 2026 "
  "meeting:\n1. Shri Saugata Bhattacharya   2. Shri Indranil Bhattacharyya   3. Prof. Ram Singh   4. Dr. Poonam Gupta\n"
  "P. RBI's September household survey showed 3-month-ahead median inflation expectations jumping to 9.9%\n"
  "Q. A gap between Indian and G7 interest rates matters for attracting debt capital flows\n"
  "R. With headline inflation likely to hit the 6% upper tolerance limit, one may not want to wait for definitive "
  "evidence of generalisation\nS. The weighted median and trimmed mean measures show high momentum of underlying "
  "inflation",
  ["1-Q, 2-S, 3-P, 4-R", "1-S, 2-Q, 3-P, 4-R", "1-Q, 2-S, 3-R, 4-P", "1-P, 2-S, 3-Q, 4-R"],
  concept="Members' reasoning in MPC minutes",
  explanation="Saugata Bhattacharya stressed the India–G7 rate gap and capital flows; Indranil Bhattacharyya pointed "
              "to weighted median and trimmed mean measures; Prof. Ram Singh cited the household survey (9.9%); Dr. "
              "Poonam Gupta argued against waiting given projections of inflation reaching the upper tolerance limit.",
  steps=["1 → external flows (Q)", "2 → underlying inflation measures (S)", "3 → household survey (P)",
         "4 → 'not wait' argument (R)"],
  why="The other options swap the household-survey, underlying-inflation and 'not wait' arguments between members.",
  current=ca("2026-10-21"),
  facts=[fact("maintaining a certain gap between India and G7 interest rates is important for attracting debt capital "
              "flows.", B_MIN),
         fact("The momentum of underlying inflation is also high as evident from the weighted median and trimmed mean "
              "measures in recent months.", B_MIN),
         fact("the RBI's September household survey showed the 3-month median inflation expectation jumped to 9.9%",
              B_MIN),
         fact("with projections indicating the likelihood of headline inflation hitting the upper tolerance limit of 6 "
              "per cent, one may not want to wait for more definitive evidence of generalisation", B_MIN)])

# ================= Repo Rate (Basic 2 / Intermediate 2 / Advanced 2)
T = "Repo Rate"
Q(T, "Repo and policy corridor", "Basic",
  "In the minutes of the October 2026 MPC meeting, Prof. Ram Singh backed a mild increase in the repo rate. What did "
  "he say the projected inflation trajectory would otherwise do to the real policy rate?",
  ["Make it negative", "Push it above 3%", "Keep it exactly at zero", "Make it equal to the SDF rate"],
  concept="Real policy rate",
  explanation="The real policy rate is roughly the repo rate minus expected inflation. With headline inflation "
              "projected to average about 5.8% over the next three quarters against a repo rate of 5.25%, Prof. Ram "
              "Singh noted that the real rate would turn negative, which argued for a calibrated hike.",
  steps=["Real rate ≈ repo − expected inflation", "5.25% − ~5.8% < 0"],
  why="A real rate above 3% or of exactly zero is not what he described; the SDF rate is a nominal corridor rate, not "
      "a real rate.",
  current=ca("2026-10-21"),
  facts=[fact("the projected inflation trajectory will render the real rate negative", B_MIN)])
Q(T, "Repo and policy corridor", "Basic",
  "Explaining her vote for the repo rate increase of October 2026, Dr. Poonam Gupta pointed to projections that "
  "headline CPI inflation could hit which level?",
  ["6 per cent, the upper tolerance limit", "4 per cent, the target", "2 per cent, the lower tolerance limit",
   "8 per cent, the ceiling set in the RBI Act"],
  concept="Inflation targeting and pre-emptive action",
  explanation="Under flexible inflation targeting the target is 4% with a 2–6% band. Dr. Gupta said that with "
              "projections showing headline inflation likely to hit the 6% upper tolerance limit (6.0% projected for "
              "Q3), one may not want to wait, since monetary policy acts with a lag.",
  steps=["Band: 2%–6%", "Projected Q3:2026-27 inflation: 6.0% → upper limit"],
  why="4% is the target and 2% the lower limit; the Act sets no 8% ceiling.",
  current=ca("2026-10-21"),
  facts=[fact("with projections indicating the likelihood of headline inflation hitting the upper tolerance limit of 6 "
              "per cent, one may not want to wait", B_MIN)])
Q(T, "Repo and policy corridor", "Intermediate",
  "In the October 2026 MPC minutes, Shri Saugata Bhattacharya argued that the pace of tightening must also consider "
  "the external sector. Why did he say a gap between Indian and G7 interest rates matters?",
  ["It is important for attracting debt capital flows", "It decides the level of the CRR",
   "It sets the ceiling of the LAF corridor", "It determines the Government's borrowing calendar"],
  concept="Policy rate and capital flows",
  explanation="A higher domestic policy rate relative to rates in advanced economies keeps rupee debt attractive to "
              "foreign investors. Mr Bhattacharya said maintaining a certain gap between Indian and G7 rates is "
              "important for attracting debt capital flows.",
  steps=["Interest differential → debt inflows", "Relevant with the rupee under pressure"],
  why="The CRR, the corridor and the borrowing calendar are set domestically and were not linked to the G7 gap.",
  current=ca("2026-10-21"),
  facts=[fact("maintaining a certain gap between India and G7 interest rates is important for attracting debt capital "
              "flows.", B_MIN)])
Q(T, "Repo and policy corridor", "Intermediate",
  "Shri Indranil Bhattacharyya urged the MPC in October 2026 to set aside the 'cautiousness bias' and act "
  "pre-emptively. What risk does the term refer to, as explained in the minutes?",
  ["Acting too little lets inflation expectations de-anchor, forcing sharper tightening later",
   "Raising rates too fast causes a sudden fall in bank deposits",
   "Waiting for the Union Budget delays transmission to lending rates",
   "Changing the stance too often confuses the bond market"],
  concept="Pre-emptive monetary policy",
  explanation="A footnote to his statement explains that the 'cautiousness bias' is the risk that a central bank, by "
              "doing too little, allows inflation expectations to de-anchor and then has to tighten more sharply. He "
              "therefore favoured a pre-emptive 25 bps increase.",
  steps=["Too little action → expectations rise", "Later, larger hikes needed"],
  why="The footnote does not relate the term to deposits, the Budget or stance changes.",
  current=ca("2026-10-21"),
  facts=[fact("I feel it is better to set aside the “cautiousness bias” (footnote 4: the risk that acting too little "
              "lets inflation expectations de-anchor, forcing sharper tightening later, as summarised).", B_MIN)])

r_lo, r_hi, target = 1.4, 1.9, 4.0
repo, exp_inf = 5.50, 5.8
real = round(repo - exp_inf, 1)
gap_lo, gap_hi = round(r_lo - real, 1), round(r_hi - real, 1)
assert (real, gap_lo, gap_hi) == (-0.3, 1.7, 2.2)
assert (round(r_lo + target, 1), round(r_hi + target, 1)) == (5.4, 5.9)
Q(T, "Repo and policy corridor", "Advanced",
  "In the October 2026 MPC minutes, Shri Saugata Bhattacharya cited an estimate of the real natural rate of interest "
  "of 1.4–1.9%. The repo rate after the meeting is 5.50%, and headline inflation was expected to average about 5.8% "
  "over the next three quarters. Taking the real rate as the repo rate minus expected inflation, how does it compare "
  "with the natural-rate estimate?",
  ["About −0.3%, i.e. 1.7 to 2.2 percentage points below the estimate, so policy is still accommodative",
   "About +0.3%, i.e. 1.1 to 1.6 percentage points below the estimate, so policy is neutral",
   "About −0.3%, within the estimate, so policy is neutral",
   "About +1.5%, within the estimate, so policy is restrictive"],
  concept="Real policy rate vs natural rate",
  explanation=f"Real rate ≈ 5.50 − 5.8 = {real}%. The natural-rate range is 1.4–1.9%, so the real rate is "
              f"{gap_lo}–{gap_hi} percentage points below it, which means policy remains accommodative even after the "
              "hike. That is why Mr Bhattacharya asked whether policy was 'too accommodative'.",
  steps=["Real = 5.50 − 5.8 = −0.3%", "Gap = 1.4 − (−0.3) = 1.7; 1.9 − (−0.3) = 2.2",
         "Real rate below natural rate → accommodative"],
  why="+0.3% uses the annual 2026-27 projection (5.2%) instead of the next-three-quarter average; −0.3% is not "
      "within 1.4–1.9%; +1.5% has no basis in the stated numbers, and a real rate below the natural rate is "
      "accommodative, not restrictive.",
  current=ca("2026-10-21"), computed=True,
  facts=[fact("The real natural rate of interest (pertaining to Q4 of FY23-24) estimated this to be 1.4-1.9%.", B_MIN),
         fact("In this context, might the broad monetary policy environment in India now be too accommodative?",
              B_MIN),
         fact("Headline inflation averaging about 5.8% over the next three quarters (cited by Prof. Ram Singh and "
              "Shri Indranil Bhattacharyya).", B_MIN)])

sdf, mpr_repo, msf = 5.25, 5.50, 5.75
seg = {"call": 5.45, "triparty": 5.43, "market": 5.48, "corp": 5.70}
assert all(sdf < seg[k] < mpr_repo for k in ("call", "triparty", "market")) and mpr_repo < seg["corp"] < msf
assert round((seg["corp"] - mpr_repo) * 100) == 20 and round((mpr_repo - seg["triparty"]) * 100) == 7
Q(T, "Repo and policy corridor", "Advanced",
  "RBI's money market data for 3 November 2026 show weighted average overnight rates of 5.45% (call money), 5.43% "
  "(triparty repo), 5.48% (market repo) and 5.70% (repo in corporate bonds). With the repo rate at 5.50%, SDF at "
  "5.25% and MSF at 5.75%, which statement is correct?",
  ["Call, triparty and market repo rates were in the lower half of the corridor; the corporate bond repo rate was "
   "20 bps above the repo rate but below the MSF",
   "All four segments traded below the repo rate, between the SDF and the repo rate",
   "The corporate bond repo rate was above the MSF rate, the ceiling of the corridor",
   "Triparty repo traded 7 bps above the repo rate, the highest of the government-collateral segments"],
  concept="Overnight rates within the LAF corridor",
  explanation="The corridor runs from 5.25% (SDF) to 5.75% (MSF) around the 5.50% repo rate. Call (5.45%), triparty "
              "(5.43%) and market repo (5.48%) were just below the repo rate. Repo in corporate bonds, backed by "
              "riskier collateral, traded at 5.70%: 20 bps above the repo rate but 5 bps under the MSF.",
  steps=["Lower half: 5.25–5.50", "5.45, 5.43, 5.48 → lower half", "5.70 → upper half (5.50–5.75)"],
  why="The corporate bond repo was above the repo rate; 5.70% is below the 5.75% MSF; triparty was 7 bps below, not "
      "above, the repo rate and was the lowest of the three.",
  current=ca("2026-11-03"), computed=True,
  facts=[fact("I. Call Money 11,860.77 5.45; II. Triparty Repo 5,50,320.25 5.43; III. Market Repo 1,86,513.67 5.48; "
              "IV. Repo in Corporate Bond 6,311.45 5.70 (Money Market Operations as on November 03, 2026)", B_MMO),
         fact("MSF 5.75; SDF 5.25 (RBI operations, November 03, 2026)", B_MMO)])

# ================= Reverse Repo Rate (Basic 1 / Intermediate 2 / Advanced 1)
T = "Reverse Repo Rate"
Q(T, "Reverse repo and SDF", "Basic",
  "RBI's money market statement for 3 November 2026 shows an outstanding variable rate reverse repo of ₹25,555 crore "
  "at 5.49%, auctioned on 8 October 2026 and maturing on 6 November 2026. What was its tenor?",
  ["29 days", "14 days", "7 days", "1 day"],
  concept="Term VRRR operations",
  explanation="A variable rate reverse repo (VRRR) absorbs surplus funds from banks for a fixed period. The operation "
              "auctioned on Thursday 8 October 2026 had a 29-day tenor, maturing on Friday 6 November 2026.",
  steps=["8 October → 6 November", "Tenor shown in the statement: 29 days"],
  why="14 and 7 days are standard tenors but not this one's; 1 day is the overnight VRRR.",
  current=ca("2026-11-03"),
  facts=[fact("2(b). Variable Rate: Reverse Repo – Auction date Thu, 08/10/2026 – Tenor 29 – Maturity Fri, 06/11/2026 "
              "– 25,555.00 – 5.49 (Outstanding Operations)", B_MMO)])
Q(T, "Reverse repo and SDF", "Intermediate",
  "In RBI's overnight VRRR auction of 4 November 2026 (notified ₹50,000 crore), offers of ₹73,907 crore were "
  "received and ₹50,015 crore was accepted at a cut-off rate of 5.49%, with 'partial acceptance of offers received at "
  "cut-off rate' of 67.64%. What does the 67.64% mean?",
  ["Only that share of the amount offered exactly at the cut-off rate was accepted, as offers exceeded the notified "
   "amount",
   "67.64% of all offers received in the auction were accepted",
   "Banks were paid 67.64% of the cut-off rate as interest",
   "67.64% of the notified amount was left unsubscribed"],
  concept="Allotment in variable rate auctions",
  explanation="In a VRRR, offers at rates up to the cut-off are accepted. When the offers at the marginal (cut-off) "
              "rate are more than what is needed to fill the notified amount, they are accepted only in part; here "
              "67.64% of the offers at 5.49% were accepted. Overall, about 68% of total offers (50,015 of 73,907) "
              "were taken, but the figure in the result refers only to offers at the cut-off.",
  steps=["Oversubscribed: 73,907 > 50,000", "Bids at the cut-off pro-rated at 67.64%"],
  why="The percentage applies to offers at the cut-off rate, not all offers; interest is paid at the bid rate; the "
      "auction was oversubscribed, so nothing was left unsubscribed.",
  current=ca("2026-11-04"),
  facts=[fact("Notified Amount 50,000; Total amount of offers received 73,907; Amount accepted 50,015; Cut off Rate "
              "5.49; Partial Acceptance Percentage of offers received at cut off rate 67.64", B_VRRR)])
Q(T, "Reverse repo and SDF", "Intermediate",
  "According to RBI's Monetary Policy Report of October 2026, how many variable rate repo (VRR) and variable rate "
  "reverse repo (VRRR) auctions did RBI conduct in H1 (April–September) 2026-27?",
  ["36 VRR and 51 VRRR", "51 VRR and 36 VRRR", "55 VRR and 2 VRRR", "12 VRR and 87 VRRR"],
  concept="Fine-tuning operations",
  explanation="The MPR says RBI conducted 36 VRR (injection) and 51 VRRR (absorption) auctions in H1:2026-27, as "
              "liquidity swung into large surplus. Average daily net absorption under the LAF rose to ₹3.21 lakh "
              "crore from ₹1.43 lakh crore in H2:2025-26.",
  steps=["Recall MPR Chapter II", "VRR 36; VRRR 51"],
  why="51/36 reverses the two; '55 and 2' mixes up the Governor's count of VRRR auctions (incl. 2 term) since August; "
      "12/87 has no basis.",
  current=ca("2026-10-07"),
  facts=[fact("Overall, the RBI conducted a total of 36 VRR and 51 VRRR auctions in H1.", B_MPR),
         fact("average daily absorption under the LAF increased to ₹3.21 lakh crore in H1:2026–27 from ₹1.43 lakh "
              "crore in H2:2025–26", B_MPR)])

vrrr_amt, sdf_amt, msf_amt = 23905, 174812, 5765
absorbed = vrrr_amt + sdf_amt
net = msf_amt - absorbed
sdf_share = round(sdf_amt / absorbed * 100)
assert absorbed == 198717 and net == -192952 and sdf_share == 88
Q(T, "Reverse repo and SDF", "Advanced",
  "On 3 November 2026 RBI absorbed ₹23,905 crore through an overnight VRRR at 5.49% and ₹1,74,812 crore under the "
  "SDF at 5.25%, and lent ₹5,765 crore under the MSF. Approximately what share of the day's absorption came through "
  "the SDF, and what was the net liquidity effect of the day's operations?",
  ["About 88%; net absorption of ₹1,92,952 crore", "About 12%; net absorption of ₹1,92,952 crore",
   "About 88%; net absorption of ₹1,98,717 crore", "About 88%; net injection of ₹5,765 crore"],
  concept="SDF as the floor absorption window",
  explanation=f"Total absorption = 23,905 + 1,74,812 = ₹{absorbed:,} crore, of which the SDF was "
              f"1,74,812/1,98,717 ≈ {sdf_share}%. Net = MSF 5,765 − 1,98,717 = ₹{-net:,} crore absorbed. Even though "
              "the VRRR paid 24 bps more, most surplus went to the standing SDF because the VRRR amount is capped by "
              "the auction while the SDF has no ceiling.",
  steps=["Absorption = 23,905 + 1,74,812 = 1,98,717", "SDF share ≈ 88%", "Net = 5,765 − 1,98,717 = −1,92,952"],
  why="12% is the VRRR share; ₹1,98,717 crore ignores the MSF injection; the day's operations absorbed, not injected, "
      "liquidity.",
  current=ca("2026-11-03"), computed=True,
  facts=[fact("2(b). Variable Rate: Reverse Repo 1 day 23,905.00 5.49; 3. MSF 5,765.00 5.75; 4. SDF 1,74,812.00 5.25; "
              "5. Net liquidity injected from today's operations [injection (+)/absorption (-)]: -1,92,952.00",
              B_MMO)])

# ================= CRR (Basic 2 / Intermediate 1 / Advanced 1)
T = "CRR"
Q(T, "CRR value", "Basic",
  "According to RBI's description of its monetary policy instruments, how is the percentage of net demand and time "
  "liabilities that a bank must keep as the Cash Reserve Ratio (CRR) prescribed?",
  ["By notification in the Gazette of India, from time to time", "Through the Union Budget each year",
   "By a resolution of the Monetary Policy Committee", "Through an amendment to the RBI Act each time"],
  concept="Legal basis of the CRR",
  explanation="RBI defines the CRR as the average daily balance a bank must keep with it as a per cent of its NDTL "
              "that the Reserve Bank may notify from time to time in the Official Gazette (the power comes from "
              "Section 42 of the RBI Act). The MPC decides only the policy repo rate.",
  steps=["CRR is set by RBI, not by Parliament or the MPC", "Mode: Gazette notification"],
  why="The Budget and Act amendments are not used to set the CRR; the MPC's remit is the repo rate.",
  facts=[fact("Cash Reserve Ratio (CRR): The average daily balance that a bank is required to maintain with the Reserve "
              "Bank as a per cent of its net demand and time liabilities (NDTL) ... that the Reserve Bank may notify "
              "from time to time in the Official Gazette.", B_MPOV)])
Q(T, "CRR concept", "Basic",
  "Which provision of the RBI Act, 1934 allows RBI to require scheduled banks to keep an additional cash balance on "
  "the increase in their liabilities over a specified date (an 'incremental CRR')?",
  ["Section 42(1A)", "Section 17(2)", "Section 45ZA", "Section 49"],
  concept="Incremental CRR",
  explanation="Section 42(1A) lets RBI direct scheduled banks to keep, in addition to the normal CRR balance, an "
              "additional average daily balance calculated on the excess of their liabilities over those on a date "
              "RBI specifies; the additional balance can never exceed that excess.",
  steps=["Normal CRR: Section 42(1)", "Additional (incremental) balance: Section 42(1A)"],
  why="Section 17 lists RBI's business; Section 45ZA deals with the inflation target; Section 49 with the Bank Rate.",
  facts=[fact("Under Section 42(1A) the Bank may require an additional average daily balance ... provided that the "
              "additional balance shall, in no case, be more than such excess.", B_S42)])
Q(T, "CRR concept", "Intermediate",
  "The Monetary Policy Report of October 2026 says reserve money grew 8.5% (y-o-y) as on 15 September 2026, but "
  "11.9% after adjusting for the first-round impact of the CRR change. Why is the adjusted figure higher?",
  ["The CRR cut reduced banks' required balances with RBI, which are part of reserve money",
   "The CRR cut increased currency held by the public, which is excluded from reserve money",
   "CRR balances earn interest, which is deducted from reserve money",
   "The adjustment adds the SLR holdings released by the CRR cut"],
  concept="CRR and reserve money",
  explanation="Reserve money includes banks' deposits with RBI, most of which are CRR balances. A CRR cut (to 3% of "
              "NDTL by November 2025) mechanically shrinks these balances, depressing measured reserve money growth. "
              "Stripping out this first-round effect gives a higher underlying growth of 11.9%.",
  steps=["Reserve money = currency + bankers' deposits with RBI + other deposits", "CRR cut → lower bankers' "
         "deposits", "Adjusted growth > raw growth"],
  why="Currency with the public is part of reserve money; RBI pays no interest on CRR balances; SLR securities are "
      "not part of reserve money.",
  current=ca("2026-10-07"),
  facts=[fact("Adjusted for the first-round impact of CRR change, growth in reserve money stood at 11.9 per cent (9.4 "
              "per cent a year ago).", B_MPR),
         fact("As on September 15, 2026, reserve money expanded by 8.5 per cent (y-o-y) as against 5.6 per cent a year "
              "ago.", B_MPR)])

req = 816655
ndtl = req / 0.03
assert round(ndtl / 1e5, 1) == 272.2
Q(T, "CRR value", "Advanced",
  "RBI's money market statement for 3 November 2026 puts the average daily cash reserve requirement of banks for the "
  "fortnight ending 15 November 2026 at ₹8,16,655 crore. Assuming a uniform CRR of 3% of NDTL and the current rule "
  "that CRR is maintained on NDTL as on the last day of the second preceding fortnight, on which date's NDTL is this "
  "based, and what NDTL does it imply?",
  ["15 October 2026; about ₹272 lakh crore", "31 October 2026; about ₹272 lakh crore",
   "15 October 2026; about ₹24.5 lakh crore", "30 September 2026; about ₹245 lakh crore"],
  concept="CRR arithmetic with the new fortnight",
  explanation=f"Fortnights now run 1–15 and 16–end of month. For 1–15 November, the preceding fortnight is 16–31 "
              f"October and the second preceding is 1–15 October, so NDTL as on 15 October 2026 applies. Implied NDTL "
              f"= 8,16,655 ÷ 0.03 ≈ ₹{ndtl:,.0f} crore ≈ ₹272 lakh crore.",
  steps=["Second preceding fortnight of 1–15 Nov = 1–15 Oct → 15 Oct", "NDTL = 8,16,655 / 0.03 ≈ 2,72,21,833 crore",
         "≈ ₹272 lakh crore"],
  why="31 October is the end of the immediately preceding fortnight; ₹24.5 lakh crore and ₹245 lakh crore come from "
      "misplacing the decimal or dividing by 3.33%; 30 September is not a fortnight-end used for this period.",
  current=ca("2026-11-03"), computed=True,
  facts=[fact("G(ii). Average daily cash reserve requirement for the fortnight ending November 15, 2026: 8,16,655.00",
              B_MMO),
         fact("the period from the first day to the fifteenth day of each calendar month and sixteenth day to the last "
              "day of each calendar month ... based on the NDTL as on the last day of the second preceding fortnight",
              B_AMD)])

# ================= SLR (Basic 1 / Intermediate 1 / Advanced 1)
T = "SLR"
Q(T, "SLR concept", "Basic",
  "After RBI's amendment of the CRR and SLR Directions effective 15 December 2025, in which return do scheduled "
  "commercial banks report their SLR maintenance, and how often?",
  ["Form VIII, monthly, on RBI's CIMS portal", "Form A, fortnightly, in hard copy",
   "Form VIII, weekly, by e-mail to the regional office", "Form X, quarterly, with the audited balance sheet"],
  concept="SLR reporting",
  explanation="The December 2025 amendment says CRR and SLR maintenance are reported in Form A and Form VIII "
              "respectively. Banks file a fortnightly Form A and a monthly Form VIII electronically on the "
              "Centralised Information Management System (CIMS); paper returns are not accepted.",
  steps=["CRR → Form A (fortnightly)", "SLR → Form VIII (monthly), on CIMS"],
  why="Form A is the CRR return and is no longer filed on paper; Form VIII is monthly, not weekly; Form X is not the "
      "SLR return.",
  current=ca("2025-12-11"),
  facts=[fact("the CRR and SLR maintenance and reporting in their returns i.e., Form A and Form VIII respectively ... "
              "The banks are required to submit fortnightly Form A return from December 15, 2025 and monthly Form VIII "
              "return", B_AMD),
         fact("Form A and Form VIII are not to be submitted in hard copy / paper returns by Scheduled Commercial banks.",
              B_AMD)])

crr_req = 1200
slr_req = crr_req / 3 * 18
assert slr_req == 7200
Q(T, "SLR value", "Intermediate",
  "A scheduled commercial bank's required CRR balance for a fortnight is ₹1,200 crore. Both CRR and SLR are "
  "computed on the same NDTL. At the current CRR and SLR, what is its SLR requirement?",
  ["₹7,200 crore", "₹6,000 crore", "₹21,600 crore", "₹40,000 crore"],
  concept="SLR as a multiple of CRR",
  explanation="CRR is 3% and SLR 18% of NDTL, so the SLR requirement is 18/3 = 6 times the CRR requirement: "
              "6 × 1,200 = ₹7,200 crore (NDTL = 1,200 ÷ 0.03 = ₹40,000 crore).",
  steps=["NDTL = 1,200 / 0.03 = 40,000", "SLR = 18% × 40,000 = 7,200"],
  why="₹6,000 crore uses a 15% SLR; ₹21,600 crore multiplies by 18 instead of 6; ₹40,000 crore is the NDTL itself.",
  shortcut="SLR/CRR = 18/3 = 6, so SLR = 6 × 1,200.",
  current=ca("2026-11-05"), computed=True,
  facts=[fact("CRR: 3.00%; SLR: 18.00% (current rates panel)", B_HOME),
         fact("the CRR and SLR maintenance and reporting ... based on the NDTL as on the last day of the second "
              "preceding fortnight", B_AMD)])

days_old = (15 - 13 + 1) + (31 - 16 + 1)
assert days_old == 19
Q(T, "SLR concept", "Advanced",
  "Under the transition arrangements in RBI's CRR and SLR Amendment Directions of 11 December 2025, banks maintained "
  "CRR and SLR during 13–15 December 2025 and 16–31 December 2025 on NDTL as on 28 November 2025, and during 1–15 "
  "January 2026 on NDTL as on 15 December 2025. For how many consecutive days was the 28 November NDTL used, and what "
  "applied from 16 January 2026?",
  ["19 days; NDTL as on the last day of the second preceding fortnight",
   "16 days; NDTL as on the last day of the preceding fortnight",
   "19 days; NDTL as on the last Friday of the second preceding fortnight",
   "34 days; NDTL as on the first day of the current fortnight"],
  concept="Transition to calendar fortnights",
  explanation=f"13–15 December is 3 days and 16–31 December is 16 days, so the 28 November NDTL was used for "
              f"{days_old} consecutive days. From 16 January 2026 maintenance is based on NDTL as on the last day of "
              "the second preceding fortnight; Friday-based references were replaced by calendar fortnights.",
  steps=["3 + 16 = 19 days", "From 16 Jan 2026: last day of second preceding fortnight"],
  why="16 days omits the three transition days; the 'last Friday' rule was replaced in December 2025; 34 days wrongly "
      "adds 1–15 January, which used the 15 December NDTL.",
  current=ca("2025-12-11"), computed=True,
  facts=[fact("During the transition period of three days i.e., December 13-15, 2025, the maintenance of CRR and SLR is "
              "to be done by the banks, based on the Net Demand and Time Liabilities (NDTL) as on November 28, 2025.",
              B_AMD),
         fact("for December 16-31, 2025 and January 1-15, 2026, maintenance is based on the NDTL as on November 28, "
              "2025 and December 15, 2025, respectively; from January 16, 2026, based on the NDTL as on the last day "
              "of the second preceding fortnight", B_AMD)])

# ================= Bank Rate (Basic 1 / Intermediate 1 / Advanced 1)
T = "Bank Rate"
Q(T, "Bank rate and MSF", "Basic",
  "Section 49 of the RBI Act, 1934 requires RBI to make public the rate at which it is prepared to buy or rediscount "
  "bills of exchange. What does the section call this rate?",
  ["The standard rate", "The policy rate", "The marginal rate", "The reference rate"],
  concept="Statutory basis of the Bank Rate",
  explanation="Section 49, headed 'Publication of Bank rate', requires RBI to publish from time to time the standard "
              "rate at which it will buy or rediscount eligible bills of exchange or commercial paper. Today the Bank "
              "Rate is aligned with the MSF rate.",
  steps=["Section 49 heading: Publication of Bank rate", "Body: 'the standard rate'"],
  why="'Policy rate' refers to the repo rate set by the MPC; 'marginal' and 'reference' rate are not the Act's terms.",
  facts=[fact("The Bank shall make public from time to time the standard rate at which it is prepared to buy or "
              "re-discount bills of exchange or other commercial paper eligible for purchase under this Act.", B_S49)])

msf_avg_h1 = 0.01e5   # ₹0.01 lakh crore = ₹1,000 crore
ratio = round(5765 / msf_avg_h1, 1)
assert ratio == 5.8
Q(T, "Bank rate and MSF", "Intermediate",
  "On 3 November 2026 banks borrowed ₹5,765 crore overnight under the Marginal Standing Facility. The October 2026 "
  "MPR says MSF recourse averaged ₹0.01 lakh crore a day in H1:2026-27. Which statement is correct?",
  ["The day's MSF borrowing was about 5.8 times the H1 average and cost 5.75%, the same as the Bank Rate",
   "The day's MSF borrowing was about 58 times the H1 average and cost 5.50%, the repo rate",
   "The day's MSF borrowing was about 5.8 times the H1 average and cost 5.25%, the SDF rate",
   "The day's MSF borrowing was below the H1 average and cost 6.00%"],
  concept="MSF and the Bank Rate",
  explanation=f"₹0.01 lakh crore = ₹1,000 crore, so 5,765 ÷ 1,000 ≈ {ratio} times. MSF funds are priced at 25 bps "
              "above the repo rate, i.e. 5.75%, and the Bank Rate is aligned with the MSF rate.",
  steps=["0.01 lakh crore = 1,000 crore", "5,765 / 1,000 ≈ 5.8", "MSF = repo + 25 bps = 5.75% = Bank Rate"],
  why="58 times misreads ₹0.01 lakh crore as ₹100 crore; 5.50% and 5.25% are the repo and SDF rates; borrowing was "
      "well above, not below, the average, and 6.00% is no current rate.",
  current=ca("2026-11-03"), computed=True,
  facts=[fact("3. MSF 1 day Wed, 04/11/2026 5,765.00 5.75", B_MMO),
         fact("banks' recourse to the marginal standing facility (MSF) averaged ₹0.01 lakh crore during H1:2026-27",
              B_MPR)])

bank_rate = 5.75
p1, p2 = bank_rate + 3, bank_rate + 5
assert (p1, p2) == (8.75, 10.75)
Q(T, "Bank rate and MSF", "Advanced",
  "After the Bank Rate was raised to 5.75% on 7 October 2026, RBI revised the penal interest rates on shortfalls in "
  "CRR and SLR requirements, which are linked to the Bank Rate and depend on how long the shortfall lasts. What are "
  "the two revised rates?",
  ["8.75% at first, rising to 10.75% if the default continues", "7.75% at first, rising to 9.75%",
   "8.75% throughout, with no increase", "6.75% at first, rising to 8.75%"],
  concept="Bank Rate as the penal reference rate",
  explanation=f"RBI's circular of 7 October 2026 revised the penal rates to Bank Rate plus 3.0 percentage points "
              f"({bank_rate} + 3 = {p1}%) or Bank Rate plus 5.0 percentage points ({p2}%), the higher rate applying "
              "when the shortfall continues. This is why the Bank Rate still matters even though it is no longer a "
              "policy signal.",
  steps=["First: Bank Rate + 3 = 8.75%", "Continuing: Bank Rate + 5 = 10.75%"],
  why="7.75%/9.75% use +2/+4; a flat 8.75% ignores the escalation; 6.75%/8.75% use +1/+3.",
  current=ca("2026-10-07"), computed=True,
  facts=[fact("the Bank Rate is revised upwards by 25 basis points from 5.50 per cent to 5.75 per cent with immediate "
              "effect. Accordingly, all penal interest rates on shortfall in CRR and SLR requirements, which are "
              "specifically linked to the Bank Rate, also stand revised as under: Bank Rate plus 3.0 percentage points "
              "(8.75 per cent) or Bank Rate plus 5.0 percentage points (10.75 per cent)", B_PEN26)])

# ================= Inflation (Basic 2 / Intermediate 3 / Advanced 3)
T = "Inflation"
Q(T, "CPI and WPI", "Basic",
  "According to MoSPI's CPI (base 2024=100) release for September 2026, which division recorded the highest "
  "year-on-year inflation at the all-India combined level?",
  ["Personal care, social protection and miscellaneous goods and services",
   "Restaurants and accommodation services", "Food and beverages", "Transport"],
  concept="Division-wise CPI inflation",
  explanation="In September 2026, the 'personal care, social protection and miscellaneous goods and services' "
              "division (which includes gold and silver jewellery) had inflation of 13.75%, ahead of restaurants and "
              "accommodation services (9.36%), food and beverages (7.36%) and transport (5.01%).",
  steps=["Compare division rates", "13.75% > 9.36% > 7.36% > 5.01%"],
  why="The other three divisions were high but lower: 9.36%, 7.36% and 5.01%.",
  current=ca("2026-10-12"),
  facts=[fact("Annexure-I (combined inflation, September 2026): Food and beverages 7.36; Transport 5.01; Restaurants "
              "and accommodation services 9.36; Personal care, social protection and miscellaneous goods and services "
              "13.75", B_CPI)])
Q(T, "CPI and WPI", "Basic",
  "In the WPI data for September 2026 (headline WPI inflation 11.39%), which major group recorded the highest annual "
  "inflation rate?",
  ["Fuel and power", "Primary articles", "Manufactured products", "Food index"],
  concept="Components of WPI",
  explanation="Fuel and power inflation rose to 25.85% in September 2026 from 22.93% in August, driven by mineral "
              "oils and crude petroleum and natural gas. Primary articles were at 8.67%, manufactured products at "
              "9.76% and the food index at 8.66%.",
  steps=["Fuel and power 25.85%", "Others between 8.7% and 9.8%"],
  why="Primary articles (8.67%), manufactured products (9.76%) and the food index (8.66%) were all far below 25.85%.",
  current=ca("2026-10-14"),
  facts=[fact("Fuel and Power recorded the highest annual inflation rate at 25.85 per cent in September, compared to "
              "22.93 per cent in August.", B_WPI)])

Q(T, "CPI and WPI", "Intermediate",
  "Among the key items in MoSPI's CPI release for September 2026, which item recorded the highest year-on-year "
  "inflation at the all-India combined level?",
  ["Onion", "Silver jewellery", "Ginger", "Garlic"],
  concept="Item-level CPI inflation",
  explanation="Onion inflation more than doubled from 48.78% in August to 108.09% in September 2026, overtaking "
              "silver jewellery (87.80%, down from 106.81%), ginger (62.85%) and garlic (54.62%).",
  steps=["Top-5 high-inflation items, September 2026", "Onion 108.09% is first"],
  why="Silver jewellery led in August but eased to 87.80% in September; ginger and garlic were third and fourth.",
  current=ca("2026-10-12"),
  facts=[fact("Top 5 key items with high inflation ... September, 2026: 1 Onion 0.7006 48.78 108.09; 2 Silver "
              "Jewellery 0.3127 106.81 87.80; 3 Ginger 0.2556 73.82 62.85; 4 Garlic 0.3738 43.60 54.62", B_CPI)])
Q(T, "CPI and WPI", "Intermediate",
  "According to MoSPI's CPI release for September 2026, which of the major States (population above 50 lakh) "
  "recorded the highest headline inflation?",
  ["Tamil Nadu", "Odisha", "Madhya Pradesh", "Telangana"],
  concept="State-level CPI inflation",
  explanation="Among States with population above 50 lakh, Tamil Nadu had the highest headline inflation at 6.81% in "
              "September 2026, followed by Odisha (6.70%), Madhya Pradesh (6.68%), Telangana (6.64%) and Andhra "
              "Pradesh (6.29%). All-India inflation was 5.54%.",
  steps=["Read the top-five States chart", "Tamil Nadu 6.81% leads"],
  why="Odisha, Madhya Pradesh and Telangana were second, third and fourth.",
  current=ca("2026-10-12"),
  facts=[fact("Top five States (having more than 50 lakh population as per Census 2011) with high headline ... "
              "Inflation in September, 2026: Tamil Nadu 6.81, Odisha 6.70, Madhya Pradesh 6.68, Telangana 6.64, Andhra "
              "Pradesh 6.29", B_CPI)])
Q(T, "Inflation targeting", "Intermediate",
  "According to the Monetary Policy Report of October 2026, what was urban households' one-year-ahead inflation "
  "expectation in RBI's September 2026 survey?",
  ["10.0 per cent", "9.9 per cent", "7.9 per cent", "6.8 per cent"],
  concept="Inflation expectations",
  explanation="Urban households' three-month-ahead and one-year-ahead expectations rose by 70 bps and 60 bps to 9.9% "
              "and 10.0% respectively. Anchoring such expectations is central to inflation targeting and was one "
              "reason for the October 2026 hike.",
  steps=["3-month ahead: 9.9%", "1-year ahead: 10.0%"],
  why="9.9% is the three-month-ahead figure; 7.9% is rural households' one-year-ahead expectation; 6.8% is rural "
      "households' current perception.",
  current=ca("2026-10-07"),
  facts=[fact("Urban households' inflation expectations for the next three months as well as one year ahead rose by "
              "70 bps and 60 bps to 9.9 and 10.0 per cent, respectively", B_MPR),
         fact("rural ... increased by 70 bps to 6.8 per cent in September 2026 ... one-year-ahead expectations also "
              "rose by 50 bps to 7.9 per cent", B_MPR)])

ci50, ci70 = (3.1, 6.1), (2.3, 6.9)
w50, w70 = round(ci50[1] - ci50[0], 1), round(ci70[1] - ci70[0], 1)
assert (w50, w70, round(w70 - w50, 1)) == (3.0, 4.6, 1.6) and ci50[1] > 6 and ci70[0] > 2
Q(T, "Inflation targeting", "Advanced",
  "The October 2026 MPR gives 50% and 70% confidence intervals for headline CPI inflation in Q4:2027-28 of 3.1–6.1% "
  "and 2.3–6.9% respectively. Consider:\nI. The upper end of the 50% interval lies above the upper tolerance limit "
  "of the inflation target.\nII. The lower end of the 70% interval lies below the lower tolerance limit.\nIII. The "
  "70% interval is 1.6 percentage points wider than the 50% interval.\nWhich of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="Fan charts and the tolerance band",
  explanation=f"The tolerance band is 2–6%. I: 6.1 > 6 – true. II: 2.3 > 2 – false. III: widths are {w50} and {w70} "
              f"points, a difference of {round(w70 - w50, 1)} – true. Wider intervals reflect greater uncertainty at "
              "higher confidence.",
  steps=["Band 2–6%", "I: 6.1 > 6 ✓", "II: 2.3 not < 2 ✗", "III: 4.6 − 3.0 = 1.6 ✓"],
  why="Any option with II is wrong because 2.3% is above the 2% lower limit.",
  current=ca("2026-10-07"), computed=True,
  facts=[fact("The 50 per cent and the 70 per cent confidence intervals for headline inflation in Q4:2027-28 are "
              "3.1-6.1 per cent and 2.3-6.9 per cent, respectively.", B_MPR)])

tm_mar, tm_aug = (2.2, 2.7), (3.7, 4.2)
wm_mar, wm_aug = 2.0, 3.5
rise = {round(tm_aug[0] - tm_mar[0], 1), round(tm_aug[1] - tm_mar[1], 1), round(wm_aug - wm_mar, 1)}
assert rise == {1.5}
Q(T, "Inflation targeting", "Advanced",
  "In the October 2026 MPC minutes, Shri Indranil Bhattacharyya noted that trimmed mean measures (5%, 10% and 25%) "
  "of CPI inflation rose from a range of 2.2–2.7% in March 2026 to 3.7–4.2% in August, and the weighted median from "
  "2% to 3.5%. Which inference is correct?",
  ["Each measure rose by about 1.5 percentage points, pointing to broad-based momentum in underlying inflation",
   "The trimmed means rose by 1.5 points but the weighted median by only 1.0 point, so pressure was narrow",
   "All measures rose about 0.5 point, so underlying inflation was stable",
   "The measures fell, showing the rise in headline inflation came from a few volatile items"],
  concept="Exclusion-based measures of underlying inflation",
  explanation="Trimmed means drop the most extreme price changes and the weighted median takes the middle one, so "
              "they capture underlying inflation. Both ends of the trimmed-mean range rose from 2.2–2.7% to 3.7–4.2% "
              "(+1.5 points) and the weighted median from 2% to 3.5% (+1.5 points), a broad-based rise that "
              "supported a pre-emptive hike.",
  steps=["3.7 − 2.2 = 1.5; 4.2 − 2.7 = 1.5", "3.5 − 2.0 = 1.5", "Uniform rise → broad-based pressure"],
  why="The weighted median also rose 1.5 points, not 1.0; a 0.5-point rise or a fall contradicts the data.",
  current=ca("2026-10-21"), computed=True,
  facts=[fact("Various measures of trimmed mean (5%, 10% and 25%) suggest that it has increased from the range "
              "2.2-2.7 per cent ... the weighted median has increased from 2 per cent to 3.5 per cent over the same "
              "period.", B_MIN),
         fact("Table IV.2 (August 2026, y-o-y): 5% trimmed mean 4.2; 10% trimmed mean 4.0; 25% trimmed mean 3.7; "
              "weighted median 3.5", B_MPR)])

wpi_fuel, cpi_head, wpi_food, cfpi, prim, manuf = 25.85, 5.54, 8.66, 7.74, 8.67, 9.76
assert wpi_fuel > 4 * cpi_head and round(wpi_food - cfpi, 2) == 0.92 and prim < manuf
Q(T, "CPI and WPI", "Advanced",
  "For September 2026: CPI headline inflation 5.54% and CFPI (food) 7.74%; WPI fuel and power 25.85%, WPI food index "
  "8.66%, WPI primary articles 8.67% and WPI manufactured products 9.76%. Consider:\nI. WPI fuel and power inflation "
  "was more than four times CPI headline inflation.\nII. WPI food index inflation exceeded CFPI inflation by about 0.9 "
  "percentage point.\nIII. WPI primary articles inflation exceeded manufactured products inflation.\nWhich of the "
  "above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Comparing CPI and WPI",
  explanation="I: 4 × 5.54 = 22.16 < 25.85 – true. II: 8.66 − 7.74 = 0.92 – true. III: 8.67 < 9.76 – false. WPI is "
              "far above CPI because it gives more weight to fuel and intermediate goods, where the oil shock hit "
              "hardest; CPI has a large services share.",
  steps=["I: 25.85 / 5.54 ≈ 4.7 ✓", "II: 0.92 pp ✓", "III: 8.67 < 9.76 ✗"],
  why="Options containing III are wrong because manufactured products inflation was higher than primary articles.",
  current=ca("2026-10-14"), computed=True,
  facts=[fact("Primary Articles inflation also accelerated to 8.67 per cent in September ... Inflation in Manufactured "
              "Products increased to 9.76 per cent ... [the Food Index] recorded an annual inflation rate of 8.66 per "
              "cent in September", B_WPI),
         fact("Fuel and Power recorded the highest annual inflation rate at 25.85 per cent in September", B_WPI),
         fact("Retail inflation based on Consumer Price Index in September, 2026 is 5.54% ... food inflation, based on "
              "Consumer Food Price Index, in September, 2026 is 7.74%", B_CPI)])


# ######## section C
# ---- sources (group C), all opened (fetched and read) on 2026-11-06
C_N = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id="
C_RSA = "https://rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=13145"     # CB - Resolution of Stressed Assets Directions, 2025 (updated 1 Oct 2026)
C_PPIRP = "https://ibbi.gov.in/uploads/press/2c3259202fdd122cabc6ef77d88c994c.pdf"  # IBBI press release IBBI/PR/2021/08, 9 Apr 2021
C_SARF = ("https://www.sansalegal.com/post/how-to-challenge-a-sarfaesi-enforcement-measure-before-the-"
          "debts-recovery-tribunal")                                          # law-firm explainer quoting SARFAESI ss. 13(3A), 17, 18
C_CCYB = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=62756"   # CCyB review, 18 May 2026
C_LCR = "https://www.bis.org/fsi/fsisummaries/lcr.htm"                       # BIS FSI executive summary: LCR
C_NSFR = "https://www.bis.org/fsi/fsisummaries/nsfr.htm"                     # BIS FSI executive summary: NSFR
C_QCCP = C_N + "13732&Mode=0"     # CB - Capital Adequacy Twelfth Amendment Directions, 7 Oct 2026
C_QCCPS = C_N + "13733&Mode=0"    # SFB - Capital Adequacy Sixth Amendment Directions, 7 Oct 2026
C_LEV = C_N + "13743&Mode=0"      # CB - Capital Adequacy Eleventh Amendment Directions (leverage ratio), 23 Oct 2026
C_MR = C_N + "13705&Mode=0"       # CB - Minimum Capital Requirements for Market Risk Directions, 21 Sep 2026
C_PSL = "https://rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12799"      # PSL - Targets and Classification Directions, 2025 (updated 11 Sep 2026)
C_PSLFAQ = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id=87"            # PSL FAQs (updated 11 Sep 2026)
C_IOS = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id=153"              # RB-IOS, 2026 FAQs (updated 1 Jul 2026)
C_NOV = C_N + "13706&Mode=0"      # Novation of OTC Derivative Contracts, 22 Sep 2026
C_CAS = C_N + "13717&Mode=0"      # Cassette-Swaps in ATMs, 1 Oct 2026
C_CUR = C_N + "13718&Mode=0"      # Currency management: withdrawal of circulars, 1 Oct 2026
C_KYCS = C_N + "13700&Mode=0"     # SFB - KYC Amendment Directions, 18 Sep 2026
C_KYCR = C_N + "13702&Mode=0"     # RRB - KYC Amendment Directions, 18 Sep 2026
C_FXD = C_N + "13737&Mode=0"      # Risk Management and Inter-Bank Dealings, 10 Oct 2026
C_SCST = C_N + "13716&Mode=0"     # Master Circular - Credit Facilities to SCs & STs, 1 Oct 2026

# ================= NPA (Basic 1 / Intermediate 3 / Advanced 3)
T = "NPA"
Q(T, "Resolution and IBC", "Basic",
  "The pre-packaged insolvency resolution process (PPIRP), introduced into the Insolvency and Bankruptcy Code by the "
  "Amendment Ordinance of April 2021, is available for which borrowers?",
  ["Corporate debtors classified as micro, small and medium enterprises",
   "Individuals and partnership firms with debts below ₹1 crore",
   "Large corporate borrowers with bank exposure above ₹1,500 crore",
   "Financial service providers such as NBFCs and housing finance companies"],
  concept="Pre-packaged insolvency (PPIRP)",
  explanation="The IBC (Amendment) Ordinance, 2021, promulgated on 4 April 2021, provided a pre-packaged insolvency "
              "resolution process for corporate debtors classified as MSMEs. IBBI notified the PPIRP Regulations on "
              "9 April 2021 to operationalise it, covering matters such as the base resolution plan and its "
              "competition with the best resolution plan.",
  steps=["PPIRP = insolvency route under the IBC", "Eligible debtors: corporate debtors that are MSMEs"],
  why="Individuals and partnership firms are not corporate debtors; PPIRP is not meant for large corporates; financial "
      "service providers are outside the corporate insolvency process of the IBC.",
  facts=[fact("The Insolvency and Bankruptcy Code (Amendment) Ordinance, 2021 promulgated on 4th April, 2021 provides "
              "for pre-packaged insolvency resolution process (PPIRP) for corporate debtors classified as micro, small "
              "and medium enterprises.", C_PPIRP)])
Q(T, "SARFAESI", "Intermediate",
  "After receiving a demand notice under Section 13(2) of the SARFAESI Act, a borrower sends a representation "
  "objecting to it. If the secured creditor does not accept the objection, within what time must it communicate the "
  "reasons for non-acceptance under Section 13(3A)?",
  ["Within 15 days of receipt of the representation", "Within 7 days of receipt of the representation",
   "Within 30 days of receipt of the representation", "Within 60 days of receipt of the representation"],
  concept="Section 13(3A) of SARFAESI",
  explanation="Section 13(3A) requires the secured creditor to consider the borrower's representation or objection "
              "and, if it is not acceptable, communicate the reasons for non-acceptance within fifteen days of "
              "receipt. Non-compliance can later be raised when the borrower challenges the creditor's measures "
              "before the DRT under Section 17.",
  steps=["Borrower objects to the 13(2) notice", "Creditor must reply with reasons within 15 days"],
  why="Seven and 30 days are not the statutory period; 60 days is the notice period "
      "given to the borrower under Section 13(2), not the creditor's reply period.",
  facts=[fact("Where a borrower objects, the creditor must consider the objection and 'communicate the reasons for "
              "non-acceptance within fifteen days of receipt'.", C_SARF)])
Q(T, "Resolution and IBC", "Intermediate",
  "Under RBI's Commercial Banks – Resolution of Stressed Assets Directions, 2025, a resolution plan involving "
  "restructuring is proposed for a borrower to whom the lenders' aggregate exposure is ₹650 crore. What independent "
  "credit evaluation (ICE) of the residual debt is required?",
  ["Two ICEs, by credit rating agencies specifically authorised by RBI",
   "One ICE, by any SEBI-registered credit rating agency",
   "One ICE, by the lead bank's statutory auditor",
   "No ICE, because only accounts above ₹1,000 crore need one"],
  concept="Independent credit evaluation under the prudential framework",
  explanation="Restructuring or change-in-ownership plans for accounts where the lenders' aggregate exposure is ₹100 "
              "crore or more need an independent credit evaluation of the residual debt by credit rating agencies "
              "specifically authorised by RBI. Accounts of ₹500 crore and above need two such evaluations; others "
              "need one. ₹650 crore is above ₹500 crore, so two ICEs are needed.",
  steps=["ICE needed: aggregate exposure ≥ ₹100 crore", "Two ICEs: aggregate exposure ≥ ₹500 crore",
         "₹650 crore ≥ ₹500 crore → two ICEs by RBI-authorised CRAs"],
  why="One ICE applies only between ₹100 crore and ₹500 crore, and must come from RBI-authorised CRAs, not any agency "
      "or an auditor; the threshold for needing an ICE is ₹100 crore, not ₹1,000 crore.",
  facts=[fact("Plans involving restructuring or change in ownership where the aggregate exposure is ₹100 crore or more "
              "'shall require independent credit evaluation of the residual debt by credit rating agencies' "
              "specifically authorised by the Reserve Bank (para 32).", C_RSA),
         fact("'accounts with aggregate exposure of ₹500 crore and above shall require two such independent credit "
              "evaluations' (para 34).", C_RSA)])
Q(T, "Resolution and IBC", "Intermediate",
  "Under RBI's Resolution of Stressed Assets Directions, 2025, the 'specified period' after a resolution plan is "
  "implemented (relevant for upgrading a restructured account) runs from the date of implementation until at least "
  "what share of the outstanding principal under the plan (plus any capitalised interest) is repaid?",
  ["20 per cent", "10 per cent", "25 per cent", "50 per cent"],
  concept="Specified period and monitoring period",
  explanation="The Directions define two periods from the date of implementation of the resolution plan: the "
              "'monitoring period' runs until at least 10% of the outstanding principal (plus sanctioned interest "
              "capitalisation) is repaid, and the 'specified period' runs until at least 20% is repaid. An account can "
              "be upgraded only if it performs satisfactorily during the specified period.",
  steps=["Monitoring period → 10% repaid", "Specified period → 20% repaid"],
  why="10% defines the monitoring period, not the specified period; 25% and 50% are not used in either definition.",
  facts=[fact("'specified period' shall mean the period from the date of implementation of resolution plan up to the "
              "date by which at least 20 per cent of the outstanding principal debt as per the resolution plan and "
              "interest capitalisation sanctioned as part of the restructuring, if any, is repaid (para 6(16)); the "
              "'monitoring period' uses a 10 per cent threshold (para 6(8)).", C_RSA)])
Q(T, "Resolution and IBC", "Advanced",
  "Lenders' aggregate exposure to Company X is ₹900 crore. Its restructuring plan gets credit opinions on the residual "
  "debt of RP3 from one RBI-authorised credit rating agency and RP5 from another. Under RBI's Resolution of Stressed "
  "Assets Directions, 2025, what is the position?",
  ["The plan cannot be implemented, since both required opinions must be RP4 or better",
   "The plan can be implemented, since the better opinion (RP3) is above RP4",
   "The plan can be implemented, since the average of RP3 and RP5 is RP4",
   "The plan can be implemented if 75% of lenders by value approve it despite the RP5 opinion"],
  concept="RP symbols and plan eligibility",
  explanation="An exposure of ₹900 crore (≥ ₹500 crore) needs two independent credit evaluations. Only plans that "
              "receive a credit opinion of RP4 (moderate degree of safety) or better for the residual debt from the "
              "required number of agencies can be implemented. RP5 signals a moderate risk of default, so one of the two "
              "required opinions fails the test.",
  steps=["₹900 crore ≥ ₹500 crore → two ICEs required", "Each required opinion must be RP4 or better",
         "RP5 is worse than RP4 → plan not eligible"],
  why="The rule is not satisfied by the better opinion or by an 'average' rating; lender approval cannot override "
      "the ICE condition.",
  facts=[fact("'Only such resolution plans which receive a credit opinion of RP4 or better for the residual debt' from "
              "the required number of credit rating agencies shall be considered for implementation (para 35); RP4 "
              "denotes a moderate degree of safety and RP5 a moderate risk of default (para 33).", C_RSA),
         fact("'accounts with aggregate exposure of ₹500 crore and above shall require two such independent credit "
              "evaluations' (para 34).", C_RSA)])
Q(T, "Resolution and IBC", "Advanced",
  "Under RBI's Resolution of Stressed Assets Directions, 2025, the Chapter IV timelines for implementing a resolution "
  "plan apply from a reference date that depends on the lenders' aggregate exposure. Consider three borrowers: "
  "P (aggregate exposure ₹2,400 crore), Q (₹1,600 crore) and R (₹1,200 crore). Which is correct?",
  ["P from 7 June 2019 and Q from 1 January 2020; R is not subject to Chapter IV",
   "P, Q and R all from 7 June 2019",
   "P from 1 January 2020 and Q from 7 June 2019; R from 1 April 2020",
   "Only P, from 7 June 2019; Q and R are not subject to Chapter IV"],
  concept="Reference dates under the prudential framework",
  explanation="The table of reference dates sets 7 June 2019 for accounts with aggregate exposure of ₹2,000 crore and "
              "above, and 1 January 2020 for ₹1,500 crore and above but below ₹2,000 crore; for accounts below ₹1,500 "
              "crore the date is to be announced, and such accounts are not subject to the Chapter IV requirements.",
  steps=["P: ₹2,400 crore ≥ ₹2,000 crore → 7 June 2019", "Q: ₹1,500–2,000 crore → 1 January 2020",
         "R: below ₹1,500 crore → not subject to Chapter IV"],
  why="The dates are tiered, not uniform; they are not reversed; and Q (above ₹1,500 crore) is covered.",
  facts=[fact("Reference dates (para 42): aggregate exposure of ₹2,000 crore and above – June 07, 2019; ₹1,500 crore "
              "and above but less than ₹2,000 crore – January 1, 2020; less than ₹1,500 crore – to be announced. "
              "Accounts with aggregate exposure below ₹1,500 crore are not subject to the Chapter IV requirements "
              "(para 43).", C_RSA)])
Q(T, "SARFAESI", "Advanced",
  "Consider the following statements about remedies against measures taken under the SARFAESI Act:\n"
  "I. Any person aggrieved, including the borrower, may apply to the Debts Recovery Tribunal within 45 days of the "
  "date on which the measure was taken.\n"
  "II. An appeal against the DRT's order lies to the Appellate Tribunal within 30 days of receipt of the order.\n"
  "III. A borrower's appeal is entertained only on deposit of 75% of the debt due, which the Appellate Tribunal may "
  "reduce to not less than 50%.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Sections 17 and 18 of SARFAESI",
  explanation="Under Section 17, any person aggrieved by a measure under Section 13(4), including the borrower, can "
              "apply to the DRT within 45 days of the date the measure was taken. Under Section 18, an appeal lies to "
              "the Appellate Tribunal within 30 days of receipt of the DRT's order; a borrower must deposit 50% of the "
              "debt due, which the Appellate Tribunal may reduce, for reasons recorded, to not less than 25%.",
  steps=["S.17: DRT within 45 days of the measure → I correct", "S.18: appeal within 30 days → II correct",
         "Pre-deposit is 50%, reducible to 25% (not 75%/50%) → III wrong"],
  why="Statement III misstates the pre-deposit (75% was the DRT pre-deposit struck down in Mardia Chemicals), so any "
      "option containing III is wrong.",
  facts=[fact("Section 17(1): 'any person aggrieved, including the borrower' may apply 'to apply to the Tribunal within "
              "forty five days of the date on which the measure was taken'.", C_SARF),
         fact("An appeal may be filed 'within thirty days of receipt of the order', and 'no appeal by a borrower is "
              "entertained unless it deposits fifty per cent of the amount of debt due', reducible to 'not less than "
              "twenty five per cent'.", C_SARF)])

# ================= Basel Norms (Basic 3 / Intermediate 4 / Advanced 1)
T = "Basel Norms"
Q(T, "Capital adequacy", "Basic",
  "After reviewing the Counter-Cyclical Capital Buffer (CCyB) framework in May 2026, what did RBI decide?",
  ["Not to activate the CCyB at that time, with the credit-to-GDP gap as the main indicator",
   "To activate the CCyB at 0.5% of risk-weighted assets, based on the credit-to-GDP gap",
   "To activate the CCyB at 1% of risk-weighted assets, based on the gross NPA ratio",
   "To replace the CCyB with a higher capital conservation buffer of 3.5%"],
  concept="Counter-cyclical capital buffer",
  explanation="The CCyB is a Basel III buffer built up in good times for use in a downturn. In its review of 18 May "
              "2026, RBI said, based on empirical analysis of CCyB indicators, that it was not necessary to activate "
              "the CCyB at that point. The framework uses the credit-to-GDP gap as the main indicator, with "
              "supplementary indicators.",
  steps=["CCyB indicators reviewed (May 2026)", "Main indicator: credit-to-GDP gap", "Decision: not activated"],
  why="RBI did not activate the buffer at any rate, the GNPA ratio is not the main indicator, and the capital "
      "conservation buffer was not changed.",
  facts=[fact("Review of Requirement of Counter-Cyclical Capital Buffer: 'it has been decided that it is not necessary "
              "to activate CCyB at this point in time'; the framework uses the 'credit-to-GDP gap as the main "
              "indicator'.", C_CCYB)],
  current=ca("2026-05-18"))
Q(T, "LCR and NSFR", "Basic",
  "Under the Basel III Liquidity Coverage Ratio standard, Level 2 assets can make up at most what share of a bank's "
  "stock of high-quality liquid assets (HQLA)?",
  ["40%", "15%", "25%", "60%"],
  concept="Composition of HQLA",
  explanation="HQLA consists of Level 1 assets, which can be included without limit, and Level 2 assets, which cannot "
              "exceed 40% of the liquidity reserve. Within Level 2, the riskier Level 2B assets cannot exceed 15% of "
              "the HQLA stock.",
  steps=["Level 1: no limit", "Level 2 (2A + 2B): at most 40%", "Level 2B alone: at most 15%"],
  why="15% is the cap on Level 2B alone; 25% and 60% are not Basel caps (60% was the initial LCR phase-in level).",
  facts=[fact("'Level 1 assets, which can be included without limit' and 'Level 2 assets, which cannot exceed 40% of "
              "the liquidity reserve'.", C_LCR)])
Q(T, "LCR and NSFR", "Basic",
  "From which date did the Net Stable Funding Ratio (NSFR) become a Basel minimum standard for internationally active "
  "banks?",
  ["1 January 2018", "1 January 2015", "1 January 2019", "1 January 2023"],
  concept="NSFR implementation",
  explanation="The NSFR, which requires available stable funding to at least equal required stable funding (a ratio "
              "of at least 100%), became a minimum standard for all internationally active banks on a consolidated "
              "basis on 1 January 2018.",
  steps=["NSFR = ASF ÷ RSF ≥ 100%", "Basel minimum standard from 1 January 2018"],
  why="2015 was when the LCR began its phase-in at 60%; 2019 was when the LCR reached 100%; 2023 is not the NSFR date.",
  facts=[fact("'The NSFR became a minimum standard applicable to all internationally active banks on a consolidated "
              "basis on 1 January 2018'.", C_NSFR),
         fact("LCR phase-in: 'the requirement set at 60% and rising by 10 percentage points annually to reach 100% on 1 "
              "January 2019'.", C_LCR)])
Q(T, "Capital adequacy", "Intermediate",
  "Under RBI's capital adequacy amendment directions of 7 October 2026, what risk weight applies to a commercial "
  "bank's trade exposure to a qualifying central counterparty (QCCP) when it acts as a clearing member for its own "
  "purposes, in OTC derivatives, exchange-traded derivatives and securities financing transactions?",
  ["2 per cent", "0 per cent", "20 per cent", "100 per cent"],
  concept="Exposures to central counterparties",
  explanation="The Twelfth Amendment Directions revised the treatment of clearing member banks to align with "
              "international standards: a 2% risk weight applies to the bank's trade exposure to a QCCP for OTC "
              "derivatives, exchange-traded derivatives and SFTs. The same 2% applies where the bank, offering client "
              "clearing, must reimburse clients for losses if the QCCP defaults. Parallel amendments were issued for "
              "SFBs, payments banks and AIFIs the same day.",
  steps=["Bank = clearing member of a QCCP (own purposes)", "Trade exposure (OTC, ETD, SFT) → 2% risk weight"],
  why="QCCP trade exposures are not risk-free (0%), and 20% and 100% are far above the prescribed weight.",
  facts=[fact("'Where a bank acts as a clearing member of a QCCP for its own purposes, a risk weight of 2 per cent shall "
              "be applied' to the bank's trade exposure to the QCCP in respect of OTC derivatives transactions, "
              "exchange traded derivatives transactions, and SFTs.", C_QCCP),
         fact("SFB amendment of the same date: trade exposure to a QCCP from OTC derivatives, exchange-traded "
              "derivatives and SFTs carries a 2% risk weight.", C_QCCPS)],
  current=ca("2026-10-07"))
Q(T, "LCR and NSFR", "Intermediate",
  "Under the Basel III Liquidity Coverage Ratio standard, which statement about Level 2A and Level 2B assets is "
  "correct?",
  ["Level 2A assets take a 15% haircut; Level 2B assets take higher haircuts and cannot exceed 15% of HQLA",
   "Level 2A assets take no haircut; Level 2B assets take a 15% haircut and cannot exceed 40% of HQLA",
   "Level 2A assets take a 50% haircut; Level 2B assets cannot be included in HQLA at all",
   "Both take a 15% haircut, and together they cannot exceed 15% of HQLA"],
  concept="HQLA haircuts and caps",
  explanation="Level 2A assets are subject to a 15% haircut. Level 2B assets carry higher haircuts and cannot exceed "
              "15% of the stock of HQLA. All Level 2 assets together cannot exceed 40%.",
  steps=["Level 2A: 15% haircut", "Level 2B: higher haircuts, cap 15% of HQLA", "Level 2 total: cap 40%"],
  why="Level 2A does take a haircut; Level 2B can be included (within its cap); the 15% cap is on Level 2B only, "
      "while all Level 2 assets are capped at 40%.",
  facts=[fact("'Level 2A assets, whose value is subject to a 15% haircut' and 'Level 2B assets, which are subject to "
              "higher haircuts but cannot exceed 15% of the stock of HQLA'.", C_LCR)])
_rc, _pfe, _coll = 20, 30, 15
_lev = 1.4 * (_rc + _pfe)
assert abs(_lev - 70) < 1e-9 and abs(1.4 * (_rc + _pfe - _coll) - 49) < 1e-9 and _rc + _pfe == 50
assert abs(_rc + 1.4 * _pfe - 62) < 1e-9
Q(T, "Leverage ratio", "Intermediate",
  "Under RBI's amended leverage ratio framework (directions of 23 October 2026, effective 1 April 2027), a bank's "
  "derivative netting set has a replacement cost of ₹20 crore and an aggregate add-on of ₹30 crore, and the bank has "
  "received collateral of ₹15 crore from the counterparty. Applying the framework's formula for derivative exposures "
  "(with the alpha it prescribes and the PFE multiplier fixed at one), what is the leverage ratio exposure for this "
  "netting set?",
  ["₹70 crore", "₹49 crore", "₹50 crore", "₹62 crore"],
  concept="Derivative exposures in the leverage ratio (SA-CCR)",
  explanation="For the leverage ratio, derivative exposure = alpha × (RC + PFE), with alpha = 1.4 and the PFE "
              "multiplier fixed at one, so PFE equals the aggregate add-on. Collateral received from the counterparty "
              "does not reduce the exposure measure. Exposure = 1.4 × (20 + 30) = ₹70 crore.",
  steps=["PFE = 1 × ₹30 crore = ₹30 crore", "RC + PFE = ₹50 crore", "× alpha 1.4 = ₹70 crore; collateral ignored"],
  why="₹49 crore wrongly deducts the collateral; ₹50 crore omits the alpha of 1.4; ₹62 crore applies alpha only to "
      "the add-on.",
  facts=[fact("'Exposure measure = alpha * (RC + PFE)', where 'alpha is 1.4'; 'For the purposes of the leverage ratio "
              "framework, the multiplier is fixed at one.'", C_LEV),
         fact("'a bank shall not reduce the leverage ratio exposure measure amount by any collateral received from the "
              "counterparty.'", C_LEV)],
  current=ca("2026-10-23"), computed=True)
_mrc = 240
_mrwa = _mrc * 12.5
assert _mrwa == 3000 and _mrc * 10 == 2400 and round(_mrc / 0.09) == 2667 and _mrc * 8 == 1920
Q(T, "Capital adequacy", "Intermediate",
  "Under RBI's Commercial Banks – Minimum Capital Requirements for Market Risk Directions, 2026 (effective 1 April "
  "2027), a bank's capital requirement for market risk computed under the simplified standardised approach is ₹240 "
  "crore. What are its risk-weighted assets for market risk?",
  ["₹3,000 crore", "₹2,400 crore", "₹2,667 crore", "₹1,920 crore"],
  concept="Converting a capital charge into RWAs",
  explanation="Banks must use the simplified standardised approach (SSA) for market risk, and the risk-weighted assets "
              "are obtained by multiplying the capital requirement by 12.5 (the reciprocal of 8%). So RWA = 240 × "
              "12.5 = ₹3,000 crore.",
  steps=["RWA = capital requirement × 12.5", "240 × 12.5 = ₹3,000 crore"],
  why="Multiplying by 10, dividing by 9% (the minimum CRAR) or multiplying by 8 are not the prescribed conversion.",
  facts=[fact("'A bank shall use the simplified standardised approach (SSA) for computing risk-weighted assets for "
              "market risk', by 'multiplying the capital requirements calculated as set out in paragraph 40 by a factor "
              "of 12.5.' These Directions shall come into effect from April 1, 2027.", C_MR)],
  current=ca("2026-09-21"), computed=True)
_l1, _l2a_mv, _out = 450, 480, 700
_l2a = _l2a_mv * 0.85
_cap = _l1 * 40 / 60
_hqla = _l1 + min(_l2a, _cap)
_lcr = 100 * _hqla / _out
assert abs(_l2a - 408) < 1e-9 and abs(_cap - 300) < 1e-9 and abs(_hqla - 750) < 1e-9 and round(_lcr, 1) == 107.1
assert round(100 * (_l1 + _l2a) / _out, 1) == 122.6
assert round(100 * (_l1 + 0.4 * (_l1 + _l2a)) / _out, 1) == 113.3
assert round(100 * (_l1 + _l1 * 15 / 85) / _out, 1) == 75.6
Q(T, "LCR and NSFR", "Advanced",
  "Under the Basel III LCR standard, a bank holds Level 1 assets of ₹450 crore and Level 2A assets with a market value "
  "of ₹480 crore; it has no Level 2B assets. Its total net cash outflows over the next 30 days are ₹700 crore. "
  "Applying the Level 2A haircut and the cap on Level 2 assets, what is its LCR?",
  ["About 107.1%; it meets the 100% minimum",
   "About 122.6%; it meets the 100% minimum",
   "About 113.3%; it meets the 100% minimum",
   "About 75.6%; it falls short of the 100% minimum"],
  concept="Applying HQLA haircuts and caps",
  explanation="Level 2A after the 15% haircut = 480 × 0.85 = ₹408 crore. Level 2 can be at most 40% of HQLA, i.e. at "
              "most 40/60 of Level 1 = 300. So eligible Level 2A = ₹300 crore and HQLA = 450 + 300 = ₹750 crore. LCR = "
              "750 ÷ 700 ≈ 107.1%.",
  steps=["Level 2A after haircut = ₹408 crore", "Cap: L2 ≤ 40% of HQLA ⇒ L2 ≤ (40/60) × 450 = ₹300 crore",
         "HQLA = 450 + 300 = ₹750 crore", "LCR = 750/700 ≈ 107.1% ≥ 100%"],
  shortcut="A 40% cap on Level 2 means Level 2 can be at most two-thirds of Level 1.",
  why="122.6% ignores the 40% cap; 113.3% wrongly takes 40% of the uncapped total; 75.6% applies the 15% Level 2B cap "
      "to Level 2A assets.",
  facts=[fact("'Level 2 assets, which cannot exceed 40% of the liquidity reserve'; 'Level 2A assets, whose value is "
              "subject to a 15% haircut'.", C_LCR)],
  computed=True)

# ================= Priority Sector Lending (Basic 1 / Intermediate 2 / Advanced 5)
T = "Priority Sector Lending"
Q(T, "Targets and sub-targets", "Basic",
  "Under RBI's PSL Directions, 2025, what is the total priority sector lending target for Primary (Urban) Co-operative "
  "Banks?",
  ["60% of ANBC or CEOBSE, whichever is higher", "40% of ANBC or CEOBSE, whichever is higher",
   "75% of ANBC or CEOBSE, whichever is higher", "50% of ANBC or CEOBSE, whichever is higher"],
  concept="PSL targets for UCBs",
  explanation="Paragraph 7.2 of the PSL Directions sets UCB targets as a percentage of ANBC or CEOBSE, whichever is "
              "higher: total priority sector 60%, micro enterprises 7.5% and advances to weaker sections 12%.",
  steps=["UCB total PSL target = 60%", "Sub-targets: micro enterprises 7.5%, weaker sections 12%"],
  why="40% is the target for domestic commercial banks, 75% for RRBs, and 50% is not a prescribed PSL target.",
  facts=[fact("'The priority sector lending targets for UCBs shall be as follows': Total Priority Sector 60%; Micro "
              "Enterprises 7.5%; Advances to Weaker Sections 12% (targets as a percentage of ANBC or CEOBSE, whichever "
              "is higher).", C_PSL)])
Q(T, "Targets and sub-targets", "Intermediate",
  "Under the PSL Directions, 2025, what is the sub-target for advances to weaker sections for Regional Rural Banks?",
  ["15 per cent of ANBC or CEOBSE, whichever is higher", "12 per cent of ANBC or CEOBSE, whichever is higher",
   "10 per cent of ANBC or CEOBSE, whichever is higher", "18 per cent of ANBC or CEOBSE, whichever is higher"],
  concept="Weaker sections sub-target by bank type",
  explanation="The weaker sections sub-target is 12% for domestic commercial banks (and foreign banks with 20 or more "
              "branches) and for SFBs, but RRBs, with their rural focus, have a higher sub-target of 15%. It does not "
              "apply to foreign banks with fewer than 20 branches.",
  steps=["Domestic SCBs and SFBs: 12%", "RRBs: 15%", "Foreign banks < 20 branches: not applicable"],
  why="12% is for commercial banks and SFBs; 10% is the small and marginal farmers sub-target; 18% is the agriculture "
      "target.",
  facts=[fact("Advances to Weaker Sections: Domestic Commercial Banks & Foreign Banks with 20 branches and above – '12 "
              "percent of ANBC or CEOBSE, whichever is higher'; Regional Rural Banks – '15 per cent of ANBC or CEOBSE, "
              "whichever is higher'; Small Finance Banks – 12 percent.", C_PSL)])
Q(T, "PSLCs", "Intermediate",
  "Can a bank use its export credit portfolio as the underlying for issuing 'PSLC – General', according to RBI's PSL "
  "FAQs?",
  ["Yes, provided the export credit is eligible for PSL classification under the criteria for domestic banks",
   "No, export credit can back only PSLCs issued by foreign banks with fewer than 20 branches",
   "No, PSLC – General can be backed only by agriculture and micro enterprise loans",
   "Yes, without any condition, since all export credit is priority sector"],
  concept="Underlying assets for PSLCs",
  explanation="RBI's FAQs say export credit can be used as the underlying for PSLC – General, but the issuing bank must "
              "ensure that the export credit portfolio is eligible for priority sector classification under the "
              "criteria applicable to domestic banks.",
  steps=["PSLC – General counts towards the overall PSL target", "Export credit may back it if PSL-eligible"],
  why="Export credit is not restricted to foreign banks' PSLCs; PSLC – General is not limited to agriculture or "
      "micro-enterprise loans; and export credit qualifies only if it meets the PSL criteria.",
  facts=[fact("Export credit can be the underlying for PSLC – General, provided the bank ensures that the export credit "
              "portfolio 'is eligible for priority sector classification' as per the criteria for domestic banks.",
              C_PSLFAQ)])
_fills = [(1.5, 25), (1.8, 50), (2.0, 25)]
_prem = sum(r / 100 * a for r, a in _fills)
assert sum(a for _, a in _fills) == 100 and abs(_prem - 1.775) < 1e-9
assert abs((2.0 * 50 + 1.5 * 25 + 1.8 * 25) / 100 - 1.825) < 1e-9 and abs(2.0 / 100 * 100 - 2.0) < 1e-9
Q(T, "PSLCs", "Advanced",
  "On RBI's e-Kuber portal, a bank places a buy order for PSLCs of ₹100 lakh at a premium of up to 2%. Sale offers "
  "were placed in this order of time: ₹50 lakh at 2.0%, ₹25 lakh at 1.5% and ₹50 lakh at 1.8%. Following RBI's "
  "matching rule, what total premium will the buyer pay?",
  ["₹1.775 lakh", "₹2.000 lakh", "₹1.825 lakh", "₹1.767 lakh"],
  concept="Order matching for PSLCs",
  explanation="Orders are matched at the lowest sale offer first, and only then by time (FIFO). So ₹25 lakh is bought "
              "at 1.5% (₹0.375 lakh), ₹50 lakh at 1.8% (₹0.90 lakh) and the remaining ₹25 lakh at 2.0% (₹0.50 lakh): "
              "total ₹1.775 lakh.",
  steps=["Sort sale offers by premium: 1.5%, 1.8%, 2.0%", "25 × 1.5% = 0.375; 50 × 1.8% = 0.90; 25 × 2.0% = 0.50",
         "Total = ₹1.775 lakh"],
  why="₹2.000 lakh assumes the buyer's own 2% bid applies throughout; ₹1.825 lakh matches in order of time instead of "
      "price; ₹1.767 lakh uses a simple average of the three rates.",
  facts=[fact("Matching follows the lowest sale offer first, then first-in-first-out; in the FAQ's example of a buyer "
              "at 2% with sellers at 1.5%, 1.8% and 2%, 'the portal will first match with the sale deal at 1.5%', then "
              "moves to 1.8% and 2% for remaining units.", C_PSLFAQ)],
  computed=True)
Q(T, "Targets and sub-targets", "Advanced",
  "RBI gives higher or lower weights to incremental priority sector credit depending on the district's per capita PSL. "
  "Consider the following statements, according to RBI's PSL FAQs:\n"
  "I. If a bank's credit in a district declines, the weighted incremental credit for that district is taken as zero.\n"
  "II. Loans bought through Inter Bank Participation Certificates (IBPCs) from another bank in a low-credit district "
  "earn the higher weight.\n"
  "III. Credit is mapped to a district on the basis of its place of utilisation.\n"
  "Which of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="District-wise weights in PSL achievement",
  explanation="Incremental credit in lower-credit districts gets a 125% weight and in higher-credit districts 90%. "
              "Only organic credit (disbursed directly, with borrower details on the bank's books) counts; routes such "
              "as securitised assets, direct assignment, IBPCs, PSLCs and on-lending through NBFCs, MFIs or HFCs are "
              "excluded. A decline gives a weighted incremental credit of zero, and credit is mapped by place of "
              "utilisation.",
  steps=["I: decline → zero → correct", "II: IBPCs excluded from weights → wrong", "III: place of utilisation → correct"],
  why="Statement II is wrong because IBPCs are one of the seven indirect routes excluded from the weighting, so any "
      "option containing II is wrong.",
  facts=[fact("'If there is a decline in credit, the weighted incremental credit will be zero (0).' Credit is mapped "
              "to a district based on its place of utilization.", C_PSLFAQ),
         fact("Only organic credit counts for incremental weights; excluded routes include 'Inter Bank Participation "
              "Certificates (IBPCs)' and 'Priority Sector Lending Certificates (PSLCs)'.", C_PSLFAQ)])
_a_out, _b_out = 26.4, 21.0
_pslamt = _a_out + _b_out
assert abs(_pslamt - 47.4) < 1e-9 and abs(25 + _b_out - 46.0) < 1e-9
Q(T, "Targets and sub-targets", "Advanced",
  "A bank has two education loans to individuals. Loan A was sanctioned for ₹25 lakh, but accrued interest during the "
  "repayment moratorium has taken the outstanding to ₹26.4 lakh. Loan B was sanctioned for ₹22 lakh and has ₹21 lakh "
  "outstanding. Applying RBI's PSL FAQ on education loans whose outstanding exceeds the limit because of interest "
  "accrued during the moratorium, how much of the two outstandings together counts as priority sector?",
  ["₹47.4 lakh", "₹46.0 lakh", "₹21.0 lakh", "₹47.0 lakh"],
  concept="Education loans under PSL",
  explanation="Education loans to individuals qualify up to ₹25 lakh. When the sanctioned limit is within ₹25 lakh, the "
              "entire outstanding counts as PSL even if accrued moratorium interest pushes it above ₹25 lakh. Both "
              "loans are within the limit, so 26.4 + 21 = ₹47.4 lakh counts.",
  steps=["Loan A: limit ₹25 lakh (within cap) → full ₹26.4 lakh counts", "Loan B: ₹21 lakh counts",
         "Total = ₹47.4 lakh"],
  why="₹46.0 lakh wrongly caps Loan A at ₹25 lakh; ₹21.0 lakh wrongly excludes Loan A; ₹47.0 lakh uses Loan B's "
      "sanctioned amount instead of its outstanding.",
  facts=[fact("Outstanding may exceed ₹25 lakh due to 'accrued interest due to moratorium on repayment during the study "
              "period'; if the sanctioned limit is within ₹25 lakh, the full outstanding counts toward PSL.", C_PSLFAQ)],
  computed=True)
Q(T, "Targets and sub-targets", "Advanced",
  "Two borrowers take bank loans for PSL-eligible activities: a partnership firm in which three of its five partners "
  "belong to a specified minority community, and a company in which three of its five directors belong to that "
  "community. According to RBI's PSL FAQs, which can be counted as advances to specified minority communities (a "
  "weaker sections category)?",
  ["Only the partnership firm's loan",
   "Only the company's loan",
   "Both loans, since the majority test is met in each",
   "Neither loan, since only individuals can be counted"],
  concept="Minority community advances",
  explanation="A partnership firm whose majority partners belong to a specified minority community can be treated as "
              "an advance to minority communities. A company is a separate legal entity, so advances to it cannot be "
              "classified as advances to specified minority communities, whoever its directors are.",
  steps=["Partnership firm: majority partners from minority → eligible", "Company: separate legal entity → not eligible"],
  why="The company does not qualify, so options including it are wrong; firms are not excluded, as RBI expressly allows "
      "partnership firms with majority minority partners.",
  facts=[fact("A partnership firm whose majority partners belong to a specified minority community can be treated as a "
              "minority-community advance; however, 'A company has a separate legal entity', so its advances 'cannot "
              "be classified as advances to the specified minority communities.'", C_PSLFAQ)])
Q(T, "PSLCs", "Advanced",
  "Consider the following statements about trading of Priority Sector Lending Certificates on RBI's e-Kuber portal, "
  "according to RBI's PSL FAQs:\n"
  "I. The premium is settled in real time by debiting/crediting the banks' current accounts with RBI, with no "
  "separate RTGS transaction.\n"
  "II. The portal levies a transaction charge on each lot traded.\n"
  "III. The tax treatment of PSLC trading is left to banks to determine under the applicable tax laws.\n"
  "Which of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I only"],
  concept="Settlement of PSLC trades",
  explanation="Premiums on matched PSLC deals are settled in real time through the banks' current accounts with RBI, "
              "so no separate RTGS is needed. There are no transaction charges on the e-Kuber PSLC module, and RBI "
              "leaves the tax treatment to banks under the applicable tax laws.",
  steps=["I: real-time settlement via RBI current accounts → correct", "II: no transaction charges → wrong",
         "III: tax treatment left to banks → correct"],
  why="Statement II is false, so options with II are wrong; 'I only' omits the correct statement III.",
  facts=[fact("Premiums are settled in real time; the participating banks' RBI current accounts are debited or credited "
              "by the matched premium, so no separate RTGS transaction is needed.", C_PSLFAQ),
         fact("There are no transaction charges for the e-Kuber PSLC module; tax treatment is for banks to determine "
              "'in accordance with the applicable tax laws'.", C_PSLFAQ)])

# ================= RBI Integrated Ombudsman Scheme (Basic 1 / Intermediate 4 / Advanced 1)
T = "RBI Integrated Ombudsman Scheme"
Q(T, "Process and limits", "Basic",
  "Under RB-IOS, 2026, callers to RBI's Contact Centre (toll-free 14448) can speak to its personnel in English, Hindi "
  "and how many regional languages?",
  ["Ten", "Eight", "Twelve", "Twenty-two"],
  concept="RBI Contact Centre",
  explanation="The Contact Centre guides complainants on the grievance redress mechanism and complaint status. Its "
              "personnel are available in English, Hindi and ten regional languages (Assamese, Bengali, Gujarati, "
              "Kannada, Marathi, Malayalam, Odia, Punjabi, Telugu and Tamil).",
  steps=["Languages: English + Hindi + 10 regional languages"],
  why="Eight and twelve are wrong counts; 22 is the number of languages in the Eighth Schedule, not the Contact "
      "Centre's languages.",
  facts=[fact("The facility to connect to Contact Center personnel is available ... 'in English, Hindi and ten "
              "regional languages' (Assamese, Bengali, Gujarati, Kannada, Marathi, Malayalam, Odia, Punjabi, Telugu, "
              "Tamil).", C_IOS)])
Q(T, "Process and limits", "Intermediate",
  "Under RB-IOS, 2026, the RBI Ombudsman or Deputy Ombudsman may help the complainant and the regulated entity reach "
  "a mutually acceptable settlement. By which means can this be done, according to RBI's FAQs?",
  ["Facilitation, advisory or conciliation", "Arbitration, mediation or adjudication",
   "Conciliation only, in a meeting held in person", "Negotiation through a Lok Adalat or a civil court"],
  concept="Modes of resolving complaints",
  explanation="A maintainable complaint can end in settlement, an Award or rejection. Settlement may be reached through "
              "facilitation, advisory or conciliation; if the grievance is resolved or the complainant accepts the "
              "resolution, the complaint is closed as settled. Conciliation meetings may be attended in person or online.",
  steps=["Outcomes: settlement, Award, rejection", "Settlement via facilitation, advisory or conciliation"],
  why="The scheme does not use arbitration or court adjudication, and conciliation is neither the only mode nor "
      "restricted to in-person meetings.",
  facts=[fact("Settlement: The RBI Ombudsman or RBI Deputy Ombudsman may help the complainant and the Regulated Entity "
              "arrive at a mutually acceptable resolution. 'This may be done through facilitation, advisory or "
              "conciliation.'", C_IOS)])
Q(T, "Scope and grounds", "Intermediate",
  "Which of the following NBFCs is NOT covered by RB-IOS, 2026, even though it is registered with RBI?",
  ["An NBFC-Infrastructure Finance Company with assets of ₹5,000 crore",
   "A deposit-taking NBFC-Investment and Credit Company",
   "An NBFC-Microfinance Institution with customer interface and assets of ₹250 crore",
   "A gold-loan NBFC with customer interface and assets of ₹1,000 crore"],
  concept="NBFC coverage under RB-IOS",
  explanation="RB-IOS covers NBFCs that accept deposits or have customer interface with assets of ₹100 crore and above, "
              "but excludes Housing Finance Companies, Core Investment Companies, IDF-NBFCs, NBFC-IFCs, NOFHCs, Primary "
              "Dealers and Mortgage Guarantee Companies. An NBFC-IFC is therefore outside the scheme whatever its size.",
  steps=["Check excluded types: HFC, CIC, IDF-NBFC, NBFC-IFC, NOFHC, PD, MGC", "NBFC-IFC → excluded"],
  why="A deposit-taking NBFC and customer-facing NBFCs with assets of ₹100 crore or more are covered.",
  facts=[fact("NBFCs: all NBFCs registered with RBI, excluding Housing Finance Companies, Core Investment Companies, "
              "IDF-NBFCs, NBFC-IFCs, NOFHCs, Primary Dealers and Mortgage Guarantee Companies, which either are "
              "authorized to accept deposits or have customer interface with asset size of Rs 100 crore and above.",
              C_IOS)])
Q(T, "Scope and grounds", "Intermediate",
  "In 2026 Kiran first complains to her bank about a disputed debit from 2019, after the period of limitation under the "
  "Limitation Act, 1963 has expired. The bank rejects it and she approaches the RBI Ombudsman within 90 days. Under "
  "RB-IOS, 2026, her complaint is:",
  ["Not maintainable, because her complaint to the bank was made after the limitation period expired",
   "Maintainable, because she approached the Ombudsman within 90 days of the bank's reply",
   "Maintainable, because there is no limit on the amount or age of a dispute under the scheme",
   "Not maintainable, because complaints about debits must go to the card network first"],
  concept="Limitation and maintainability",
  explanation="Besides the 30-day and 90-day timelines, the complaint to the regulated entity must itself have been "
              "made before the expiry of the limitation period under the Limitation Act, 1963. Complaints where the "
              "complaint to the RE was made after that period are not maintainable.",
  steps=["Check 90-day window → met", "Check limitation for the original complaint to the RE → expired",
         "→ non-maintainable"],
  why="Meeting the 90-day window does not cure the limitation defect; 'no limit' applies only to the amount in "
      "dispute; there is no rule routing debit complaints to the card network.",
  facts=[fact("Non-maintainable: 'Complaints where the complaint to the Regulated Entity was made after expiry of the "
              "limitation period under the Limitation Act, 1963.'", C_IOS)])
Q(T, "Process and limits", "Intermediate",
  "Two customers with apparently similar grievances receive different outcomes from the RBI Ombudsman. According to "
  "RBI's FAQs on RB-IOS, 2026, which statement best explains this?",
  ["Similar-looking cases may differ in facts, documents, relief sought and applicable instructions, and the Ombudsman "
   "considers principles of banking law and practice and RBI directions",
   "The Ombudsman is bound by the earlier decision in a similar case, so the second outcome must be an error",
   "Each RBI Ombudsman office follows its own local rules, so outcomes vary by State",
   "Outcomes depend only on whether the regulated entity agrees to settle"],
  concept="Basis of the Ombudsman's decisions",
  explanation="The FAQs say cases that appear similar may differ in facts, documents, relief sought, applicable "
              "regulatory instructions and conduct of the parties. The Scheme lets the Ombudsman consider the "
              "principles of banking law and practice, RBI directions/instructions and other relevant factors.",
  steps=["Look at facts, documents, relief and conduct", "Apply banking law and practice and RBI instructions"],
  why="There is no binding precedent rule; handling is jurisdiction-neutral ('One Nation One Ombudsman'), not State-"
      "wise; and Awards can be passed without the entity's agreement.",
  facts=[fact("'Cases that appear similar may differ in facts, documents, relief sought,' applicable regulatory "
              "instructions and conduct of the parties. The Scheme enables the RBI Ombudsman to consider the principles "
              "of banking law and practice, RBI directions/instructions/guidelines/regulations and other relevant "
              "factors while deciding a complaint.", C_IOS)])
Q(T, "Scope and grounds", "Advanced",
  "Under RB-IOS, 2026, on which of the following grounds may an RBI Deputy Ombudsman (as distinct from the RBI "
  "Ombudsman) reject a complaint?\n"
  "I. The complaint is non-maintainable under Clause 10 of the Scheme.\n"
  "II. The complaint requires elaborate documentary and oral evidence, making the proceedings inappropriate.\n"
  "III. A case on the same cause of action is filed before a court or tribunal while the complaint is being examined.\n"
  "Select the correct answer:",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="Powers of the Deputy Ombudsman",
  explanation="The Deputy Ombudsman can reject a complaint only on the grounds in Clause 16(1): non-maintainability "
              "under Clause 10, no deficiency in service (suggestions, queries and the like), or a case on the same "
              "cause of action being filed before a court or other forum during examination. Rejection because "
              "elaborate evidence is needed is among the RBI Ombudsman's wider Clause 16 grounds.",
  steps=["Deputy Ombudsman: Clause 16(1) grounds only", "I and III are Clause 16(1) grounds",
         "II is an Ombudsman-only ground"],
  why="Options containing II are wrong because that ground is exercised by the RBI Ombudsman, not the Deputy "
      "Ombudsman.",
  facts=[fact("The RBI Deputy Ombudsman may reject a complaint at any stage on any of the grounds specified in Clause "
              "16(1): the complaint is non-maintainable under Clause 10; it does not disclose any deficiency in service; "
              "or a case on the same cause of action is filed before a Court, Tribunal, Arbitrator or other forum.",
              C_IOS),
         fact("The RBI Ombudsman may reject a complaint at any stage if, among other grounds, it requires consideration "
              "of elaborate documentary and oral evidence (Clause 16).", C_IOS)])

# ================= RBI Circulars and Regulatory Updates (Basic 2 / Intermediate 4 / Advanced 2)
T = "RBI Circulars and Regulatory Updates"
Q(T, "Recent RBI directions", "Basic",
  "On 22 September 2026, RBI finalised instructions, based on feedback on draft directions of July 2025, on the "
  "novation of which contracts?",
  ["OTC derivative contracts", "Housing loan agreements", "Bank guarantees in trade finance",
   "Gold loan contracts of NBFCs"],
  concept="Novation of OTC derivatives",
  explanation="Novation transfers a party's rights and obligations under a contract to a new party. RBI's circular of "
              "22 September 2026 finalised the instructions on novation of OTC derivative contracts, issued in draft on "
              "9 July 2025, and inserted them into four existing directions (OTC forex, rupee interest rate "
              "derivatives, G-sec forwards and credit derivatives). They apply to novations on or after the circular's "
              "date.",
  steps=["Draft: July 2025", "Final: 22 September 2026, for OTC derivative contracts"],
  why="The circular is about OTC derivatives, not loans, guarantees or gold loans.",
  facts=[fact("Refers to the 'draft Reserve Bank of India (Novation of OTC Derivative Contracts) Directions, 2025' "
              "issued on July 09, 2025; 'Based on the feedback received, the instructions related to the OTC derivative "
              "contracts have been finalised.'", C_NOV)],
  current=ca("2026-09-22"))
Q(T, "Recent RBI directions", "Basic",
  "By a circular effective 1 October 2026, RBI allowed a bank's Board to delegate the monitoring of progress in "
  "implementing cassette swaps in ATMs to:",
  ["A Committee of Executives", "The RBI Regional Office", "The bank's statutory central auditor",
   "The National Payments Corporation of India"],
  concept="Cassette swaps in ATMs",
  explanation="Under RBI's 2022 circular, banks were to replace ATM cash cassettes with pre-loaded ones (cassette "
              "swaps). The 1 October 2026 amendment, issued alongside the 2026 governance amendment directions, lets "
              "the Board delegate monitoring of implementation to a Committee of Executives.",
  steps=["2022 circular: cassette swaps", "2026 change: monitoring may be delegated to a Committee of Executives"],
  why="Monitoring is an internal governance task; it is not handed to RBI, auditors or NPCI.",
  facts=[fact("'monitoring the progress of implementation of cassette swap may be delegated by the Board to a Committee "
              "of Executives' (substituted w.e.f. October 1, 2026).", C_CAS)],
  current=ca("2026-10-01"))
Q(T, "Recent RBI directions", "Intermediate",
  "On 1 October 2026, after reviewing its instructions on currency management, RBI withdrew the instructions that had "
  "been consolidated into function-wise Master Directions or had become obsolete. How many were listed for withdrawal?",
  ["268", "186", "312", "120"],
  concept="Consolidation of currency management instructions",
  explanation="RBI reviewed its currency management instructions, consolidated the extant ones into function-wise "
              "Master Directions (for example on exchange of notes and coins, and counterfeit notes) and withdrew the "
              "268 instructions listed in the Annex, including obsolete or redundant ones dating from 1976 onward.",
  steps=["Review of currency management instructions", "Annex lists 268 instructions → withdrawn"],
  why="The other figures do not match the number of instructions listed in the Annex.",
  facts=[fact("'Accordingly, the instructions listed in the Annex, comprising those which have been consolidated into "
              "Master Directions as well as those which have become obsolete or redundant, stands withdrawn.' The "
              "Annex runs to serial number 268.", C_CUR)],
  current=ca("2026-10-01"))
Q(T, "Recent RBI directions", "Intermediate",
  "RBI's KYC amendment directions of 18 September 2026 (for small finance banks and regional rural banks, among "
  "others) extended the option of submitting an 'original certified copy' of documents, earlier available to NRIs and "
  "PIOs, to which customers?",
  ["Foreign Portfolio Investors (FPIs)", "Resident senior citizens", "Self-help groups", "Foreign diplomats in India"],
  concept="KYC for non-resident customers",
  explanation="The amendments let the bank obtain an original certified copy of KYC documents from FPIs too, as already "
              "allowed for NRIs and PIOs. The copy may be certified by, among others, overseas branches of Indian "
              "scheduled commercial banks, partner overseas banks, a Notary Public abroad, a Court Magistrate, a Judge "
              "or the Indian Embassy/Consulate.",
  steps=["Existing option: NRIs and PIOs", "Extended to: FPIs"],
  why="The change concerns non-resident customers who cannot easily present documents in person; the other groups "
      "were not mentioned.",
  facts=[fact("Amended para 5(1)(v): for NRIs, PIOs 'and Foreign Portfolio Investors (FPIs), the bank may alternatively "
              "obtain the original certified copy, certified by any one of the following'.", C_KYCS),
         fact("RRB KYC Amendment Directions (18 September 2026) extend to FPIs the option to accept original certified "
              "copies, earlier available only to NRIs and PIOs.", C_KYCR)],
  current=ca("2026-09-18"))
Q(T, "Recent RBI directions", "Intermediate",
  "Under RBI's directions of 10 October 2026 on foreign exchange derivative contracts involving the INR, what is the "
  "new threshold for the facilities that let users undertake such transactions without establishing underlying "
  "exposure?",
  ["USD 5 million equivalent of notional value outstanding at any time",
   "USD 100 million equivalent of notional value outstanding at any time",
   "USD 2 million equivalent per transaction",
   "USD 25 million equivalent per financial year"],
  concept="Hedging without underlying exposure",
  explanation="The 10 October 2026 directions cut the threshold for these facilities from USD 100 million to USD 5 "
              "million equivalent of notional value outstanding at any time. Users must give an undertaking that the "
              "same exposure is not hedged elsewhere, and ADs must keep documents for at least two years.",
  steps=["Old threshold: USD 100 million", "New threshold: USD 5 million (outstanding at any time)"],
  why="USD 100 million was the earlier limit; USD 2 million is the threshold used for the Foreign Exchange Risk "
      "Reserve; USD 25 million per year is not prescribed.",
  facts=[fact("'The threshold for each of the above facilities shall, henceforth, be USD 5 million equivalent of "
              "notional value (outstanding at any point of time)'; the earlier limit for positions without proving "
              "underlying exposure was USD 100 million.", C_FXD)],
  current=ca("2026-10-10"))
Q(T, "Recent RBI directions", "Intermediate",
  "RBI's Commercial Banks – Minimum Capital Requirements for Market Risk Directions, 2026, issued on 21 September "
  "2026, require banks to compute market-risk RWAs using which approach, and from when?",
  ["The simplified standardised approach, from 1 April 2027",
   "The internal models approach, from 1 October 2026",
   "The basic indicator approach, from 1 April 2027",
   "The advanced measurement approach, from 1 January 2027"],
  concept="New market risk framework",
  explanation="The Directions require banks to use the simplified standardised approach (SSA) for market risk, with "
              "capital charges for interest rate, equity, foreign exchange and options risk, and replace the market "
              "risk section of the 2025 capital adequacy directions from 1 April 2027.",
  steps=["Approach: SSA", "Effective: 1 April 2027"],
  why="No internal models approach is provided; the basic indicator and advanced measurement approaches belong to "
      "operational risk, not market risk.",
  facts=[fact("'A bank shall use the simplified standardised approach (SSA) for computing risk-weighted assets for "
              "market risk.' 'These Directions shall come into effect from April 1, 2027.'", C_MR)],
  current=ca("2026-09-21"))
Q(T, "Recent RBI directions", "Advanced",
  "Consider the following statements about RBI's Market Risk Directions, 2026 (21 September 2026):\n"
  "I. They apply to all banking companies, including small finance banks, payments banks and local area banks.\n"
  "II. The trading book includes all instruments classified as 'Held for Trading' under RBI's investment portfolio "
  "directions.\n"
  "III. On their implementation, the section on 'Capital charge for market risk' in the 2025 capital adequacy "
  "directions (except one sub-section) stands repealed.\n"
  "Which of the above is/are correct?",
  ["II and III only", "I and II only", "I and III only", "I, II and III"],
  concept="Scope of the market risk directions",
  explanation="'Commercial Banks' here means banking companies other than SFBs, payments banks and local area banks, "
              "plus nationalised banks and SBI, so statement I is wrong. The trading book is all HFT instruments, with "
              "everything else in the banking book, and Section D (except D.8) on market risk in the 2025 capital "
              "adequacy directions is repealed.",
  steps=["I: SFBs, PBs and LABs are excluded → wrong", "II: trading book = HFT → correct",
         "III: Section D (except D.8) repealed → correct"],
  why="Statement I is wrong, so every option containing I is wrong.",
  facts=[fact("'Commercial Banks' means banking companies (other than Small Finance Banks, Payments Banks, and Local "
              "Area Banks), corresponding new banks, and the State Bank of India.", C_MR),
         fact("The trading book 'shall include all instruments classified as 'Held for Trading''; and 'Section D "
              "(except sub-section D.8) on 'Capital charge for market risk'' of the 2025 Capital Adequacy Directions "
              "'shall stand repealed.'", C_MR)],
  current=ca("2026-09-21"))
Q(T, "Recent RBI directions", "Advanced",
  "Consider the following statements about RBI's Master Circular on credit facilities to Scheduled Castes and "
  "Scheduled Tribes (1 October 2026):\n"
  "I. Under DAY-NRLM, 50% of the beneficiaries are to be SCs/STs.\n"
  "II. Guarantee cover under the Credit Enhancement Guarantee Scheme for Scheduled Castes ranges from ₹0.15 crore to "
  "₹5 crore, with IFCI Ltd as nodal agency.\n"
  "III. Banks should review measures to improve credit flow to SC/ST borrowers on a half-yearly basis.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Credit to SCs and STs",
  explanation="The master circular consolidates 21 earlier circulars. It records that DAY-NRLM aims for 50% SC/ST "
              "beneficiaries, that at least 40% of DRI advances go to SC/ST borrowers, and that CEGSSC cover ranges "
              "from ₹0.15 crore to ₹5 crore with IFCI as nodal agency. Banks must review the measures quarterly, not "
              "half-yearly.",
  steps=["I: 50% under DAY-NRLM → correct", "II: ₹0.15–5 crore, IFCI → correct", "III: review is quarterly → wrong"],
  why="Statement III is wrong, so options containing III are wrong.",
  facts=[fact("DAY-NRLM would ensure coverage 'such that 50% of these beneficiaries are SCs/STs'; 'The amount of "
              "guarantee cover under CEGSSC ranges from a minimum of ₹0.15 cr to a maximum of ₹5.00 cr.' 'IFCI Ltd. has "
              "been designated as the Nodal Agency under the scheme.'", C_SCST),
         fact("'Banks should review the measures taken to enhance the flow of credit to SC/ST borrowers on a quarterly "
              "basis.'", C_SCST)],
  current=ca("2026-10-01"))


# ######## section D
# ---- sources (group D), opened 2026-11-06
D_ERUPEE = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id=169"                 # RBI Digital Rupee (e₹) FAQs (1 Oct 2026)
D_DBC = "https://www.rbi.org.in/SCRIPTs/BS_ViewMasDirections.aspx?id=13163"       # CB - Digital Banking Channels Authorisation Directions, 2025 (28 Nov 2025, updated 6 Nov 2026)
D_DL25 = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12848"          # RBI (Digital Lending) Directions, 2025 (8 May 2025)
D_NEFT = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id=60"                   # RBI NEFT FAQs (2 Sep 2024)
D_NEFT24 = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11750&Mode=0" # RBI circular on 24x7 NEFT, 6 Dec 2019 (shown as withdrawn)
D_RTGS = "https://www.rbi.org.in/Scripts/FAQView.aspx?Id=65"                      # RBI RTGS FAQs (14 Oct 2026)
D_TAT = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11693"           # RBI TAT and compensation for failed transactions, 20 Sep 2019
D_LOOKUP = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12759&Mode=0" # RBI name look-up for RTGS/NEFT, 30 Dec 2024
D_RUPAYCC = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=53833"  # Governor's Statement, 8 June 2022
D_AEPSPR = "https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=60734"   # RBI press release on AePS ATO Directions, 27 June 2025
D_AEPSMN = "https://www.medianama.com/2025/07/223-rbi-guidelines-aeps-touchpoint-operators-banks/"  # news on the AePS ATO Directions
D_NACH7 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=51684"  # Statement on Developmental and Regulatory Policies, 4 June 2021
D_EMAND = "https://www.rbi.org.in/scripts/FS_Notification.aspx?Id=12722"  # Processing of e-mandates for recurring transactions, 22 Aug 2024
D_LITE = ("https://www.outlookmoney.com/banking/upi-lite-is-here-with-enhanced-featurescan-you-use-it-online-know-"
          "the-details")                                                           # Outlook Money on NPCI's Feb 2025 UPI Lite circulars
D_NEPAL = ("https://www.devdiscourse.com/article/law-order/3933679-india-nepal-launch-instant-cross-border-upi-"
           "remittance-service")                                                   # Devdiscourse, 11 June 2026
D_MDR = "https://www.scconline.com/blog/post/2026/08/10/no-charges-upi-users-government-clarifies-mdr/"  # SCC Online, 10 Aug 2026

# ================= Digital Banking (Basic 1 / Intermediate 5 / Advanced 1)
T = "Digital Banking"
Q(T, "CBDC (e-rupee)", "Basic",
  "According to RBI's Digital Rupee (e₹) FAQs, what fees or charges does a user pay for holding and using a retail e₹ "
  "wallet?",
  ["None; no fees or charges apply to e₹ or e₹ wallets",
   "A flat annual wallet maintenance fee fixed by RBI",
   "A small charge on every person-to-merchant payment",
   "A charge only when e₹ is redeemed back to the bank account"],
  concept="Charges on the retail digital rupee",
  explanation="RBI's e₹ FAQs state that no fees or charges apply to e₹ or to e₹ wallets. Like cash, the digital rupee "
              "can be loaded, spent and redeemed without a charge to the user.",
  steps=["Recall RBI's FAQ on fees for e₹", "No fees or charges apply"],
  why="RBI prescribes no wallet maintenance fee, no per-payment charge and no redemption charge for e₹; all three "
      "distractors invent charges the FAQ rules out.",
  facts=[fact("Are there fees? No fees or charges apply to e₹ or e₹ wallets.", D_ERUPEE)])
Q(T, "CBDC (e-rupee)", "Intermediate",
  "According to RBI's Digital Rupee FAQs, under which provision is every e₹ note legal tender anywhere in India, "
  "guaranteed by the Central Government?",
  ["Section 26 of the RBI Act, 1934",
   "Section 22 of the RBI Act, 1934",
   "Section 10 of the Payment and Settlement Systems Act, 2007",
   "Section 6 of the Coinage Act, 2011"],
  concept="Legal tender status of e₹",
  explanation="RBI's FAQs say that under Section 26 of the RBI Act, 1934, every e₹ note is legal tender anywhere in "
              "India and is guaranteed by the Central Government. Being a digital form of the rupee note, e₹ is a "
              "liability of the RBI, just like a physical banknote.",
  steps=["e₹ is a digital form of the banknote", "Banknotes are legal tender under Section 26 of the RBI Act"],
  why="Section 22 gives RBI the sole right to issue banknotes but is not the legal-tender clause; the PSS Act governs "
      "payment systems, not legal tender; and the Coinage Act covers coins, not e₹ notes.",
  facts=[fact("Under Section 26 of the RBI Act, 1934, every e₹ note is legal tender anywhere in India and is guaranteed "
              "by the Central Government. As a digital form of the ₹ note, it is a liability of the RBI.", D_ERUPEE)])
Q(T, "Mobile and internet banking", "Intermediate",
  "A bank lets customers check balances and transfer funds by dialling a USSD code on a basic phone. Under RBI's "
  "Commercial Banks – Digital Banking Channels Authorisation Directions, 2025, this service falls under which channel?",
  ["Mobile banking, which covers mobile applications, USSD and SMS",
   "Internet banking, which covers all channels that use a telecom network",
   "A separate 'assisted banking' channel outside digital banking",
   "Phone banking, which is not regulated by these Directions"],
  concept="Internet banking vs mobile banking under the 2025 Directions",
  explanation="The Directions define mobile banking as a channel using mobile applications, USSD and SMS. Internet "
              "banking means operating accounts over the internet, including browser-based applications but "
              "excluding mobile applications. So a USSD service is mobile banking.",
  steps=["Mobile banking = mobile apps, USSD and SMS", "Internet banking = web/browser-based, excludes apps",
         "USSD service -> mobile banking"],
  why="Internet banking is browser-based and excludes mobile apps, so it does not cover USSD; the Directions create no "
      "separate assisted or phone-banking category for USSD.",
  facts=[fact("Internet banking: a channel for operating accounts over the internet, including browser-based "
              "applications but excluding mobile applications. Mobile banking: a channel using mobile applications, "
              "USSD, and SMS.", D_DBC)])
Q(T, "Mobile and internet banking", "Intermediate",
  "A bank wants to show an insurance company's products on its mobile banking app after the customer logs in. Under "
  "RBI's Commercial Banks – Digital Banking Channels Authorisation Directions, 2025, what is the position?",
  ["Third-party products shall not be displayed after login unless RBI permits it under the applicable Directions",
   "The bank may display them freely if the customer has given SMS consent",
   "They may be displayed only before login, on the app's landing page, without restriction",
   "They may be displayed after login if the bank charges no fee for the display"],
  concept="Third-party products on digital banking channels",
  explanation="The Directions say that after login, third-party products and services shall not be displayed on the "
              "bank's digital channels unless RBI permits it, as provided in the Undertaking of Financial Services "
              "Directions, 2025. Consent or a zero fee does not override this.",
  steps=["Identify the rule on third-party products after login", "Not displayed unless permitted by RBI"],
  why="Customer consent, a no-fee display or pre-login placement are not conditions the Directions recognise; the test "
      "is RBI permission under the Undertaking of Financial Services Directions.",
  facts=[fact("After login, third-party products and services \"shall not be displayed\" on bank channels unless the "
              "RBI permits, per paras 58 to 62 of the Undertaking of Financial Services Directions, 2025.", D_DBC)])
Q(T, "Digital lending", "Intermediate",
  "A borrower complains to a bank about a loan taken through its digital lending app. Under the RBI (Digital Lending) "
  "Directions, 2025, when can the borrower take the complaint to RBI's Integrated Ombudsman Scheme?",
  ["If the complaint is rejected or he is dissatisfied, or he gets no reply within 30 days of its receipt by the "
   "lender",
   "Only after 60 days, and only if the lending service provider has also rejected it",
   "Immediately, since digital lending complaints go straight to RBI",
   "Only after the lending service provider's nodal officer closes the complaint"],
  concept="Grievance redressal in digital lending",
  explanation="Lenders and their LSPs must designate nodal grievance redressal officers, but the responsibility for "
              "redressal remains with the regulated entity (lender). If the complaint is rejected wholly or partly, "
              "the borrower is dissatisfied, or there is no reply within 30 days of receipt by the lender, the "
              "borrower can complain under the RB-IOS through the CMS portal.",
  steps=["Complaint first to the lender (RE)", "Escalate if rejected/dissatisfied/no reply in 30 days",
         "File under RB-IOS on the CMS portal"],
  why="The period is 30 days, not 60; the complaint must first go to the lender, not straight to RBI; and the LSP's "
      "officer cannot hold up escalation because responsibility stays with the lender.",
  facts=[fact("Borrowers may escalate if a complaint is rejected in whole or part, they are dissatisfied, or they receive "
              "no reply \"within 30 days of receipt of complaint by the RE\".", D_DL25),
         fact("\"responsibility of grievance redressal shall continue to remain with the RE\"", D_DL25)])
Q(T, "Digital lending", "Intermediate",
  "Under the RBI (Digital Lending) Directions, 2025, how must repayments of a digital loan flow, and what applies when "
  "a delinquent borrower repays in cash?",
  ["Repayments go directly to the lender's account with no third-party pool account; a cash recovery must be "
   "reflected in the borrower's account the same day",
   "Repayments may pass through the LSP's pool account; cash recoveries are credited within 7 days",
   "Repayments go to an escrow account of the LSP; cash recoveries are not allowed at all",
   "Repayments may go to any account the borrower chooses; cash recoveries are credited at month-end"],
  concept="Fund flows in digital lending",
  explanation="The Directions require repayments to go directly to the regulated entity's account, without any "
              "pass-through or pool account of a third party, and bar third parties such as LSPs from controlling "
              "the fund flow. Cash recoveries from delinquent loans are allowed, but must be fully reflected in the "
              "borrower's account on the same day.",
  steps=["Repayment: borrower -> lender directly", "No pass-through/pool account of LSP",
         "Cash recovery: allowed, reflected the same day"],
  why="Pass-through, pool or escrow accounts of the LSP are prohibited; cash recovery is permitted, not barred; and "
      "the same-day rule rules out 7-day or month-end credit.",
  facts=[fact("Repayments go directly to the RE's account, with no \"pass-through account/ pool account of any third "
              "party\".", D_DL25),
         fact("Cash recoveries on delinquent loans are permitted but must be fully reflected in the borrower's account "
              "the same day.", D_DL25)])
Q(T, "Mobile and internet banking", "Advanced",
  "Consider the following statements about RBI's Commercial Banks – Digital Banking Channels Authorisation "
  "Directions, 2025:\nI. They came into effect from 1 January 2026.\nII. To get approval for a transactional facility, "
  "a bank must have had no major adverse observations in its IS Audit reports for the last three financial years.\n"
  "III. Where transaction limits under RBI instructions and payment network rules differ, the stricter of the two "
  "applies.\nWhich of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="Eligibility and risk controls for digital banking channels",
  explanation="The Directions came into effect on 1 January 2026. A satisfactory compliance record for a transactional "
              "facility is judged through a GAICA report by a CERT-In empanelled auditor, no major adverse "
              "observations in IS Audit reports for the last two (not three) financial years, and supervisory inputs. "
              "Banks must set per-transaction, daily, weekly and monthly limits, and the stricter of RBI's and the "
              "payment network's requirements applies.",
  steps=["I: effective 1 January 2026 - correct", "II: the look-back is two financial years - wrong",
         "III: stricter of the two applies - correct"],
  why="Any option containing II is wrong because the IS Audit look-back is two years; 'I and II only' also drops the "
      "correct statement III.",
  facts=[fact("\"These Directions shall come into effect from January 01, 2026.\"", D_DBC),
         fact("A satisfactory compliance record, assessed through a CERT-In empanelled auditor's GAICA report, no major "
              "adverse observations in IS Audit reports for the last two financial years, and supervisory inputs.",
              D_DBC),
         fact("Where RBI or payment network rules differ, \"the requirements that are stricter of the two shall be "
              "applicable.\"", D_DBC)])

# ================= UPI (Basic 3 / Intermediate 1 / Advanced 1)
T = "UPI"
Q(T, "UPI Lite and international", "Basic",
  "Under NPCI's directions to issuer banks, what happens to the balance in a UPI Lite account that has had no "
  "transaction for six months?",
  ["It is refunded to the user's source bank account",
   "It is forfeited and credited to the DEA Fund",
   "It is frozen until the user completes fresh KYC",
   "It is converted into retail e₹ in the user's wallet"],
  concept="Inactive UPI Lite balances",
  explanation="NPCI directed issuer banks to identify 'zero transaction' UPI Lite accounts, those with no transaction "
              "in six months, and refund the amount lying in them to the source bank accounts. The money thus goes "
              "back to the user's own account.",
  steps=["Inactive = no transaction in six months", "Balance refunded to the source bank account"],
  why="The balance is not forfeited to the DEA Fund, not frozen pending KYC and not converted into e₹; NPCI requires a "
      "refund to the linked bank account.",
  facts=[fact("NPCI directed issuer banks to \"identify zero transaction UPI Lite accounts and refund the amount lying in "
              "these accounts to the source bank accounts.\" Such accounts are those with \"no transaction in six "
              "months.\"", D_LITE)])
Q(T, "UPI Lite and international", "Basic",
  "According to NPCI's February 2025 circular on UPI Lite (to be implemented by 31 March 2025), what new facility did "
  "users get?",
  ["'Transfer out', to move the UPI Lite balance back to the bank account without closing the wallet",
   "Payments of up to ₹5,000 at a time without a UPI PIN",
   "Use of UPI Lite for international merchant payments",
   "Interest on the UPI Lite balance at the savings rate"],
  concept="UPI Lite transfer-out",
  explanation="NPCI's circular of 21 February 2025 asked members to provide a 'transfer out' facility so that users can "
              "withdraw funds from the UPI Lite balance to their bank account. Earlier, transfer out was possible only "
              "when the UPI Lite wallet was closed or disabled.",
  steps=["Earlier: transfer out only on closing/disabling the wallet", "Now: transfer out at any time to the bank account"],
  why="₹5,000 is the overall UPI Lite limit, not the per-payment limit (₹1,000); the circular is not about international "
      "use; and UPI Lite balances earn no interest.",
  facts=[fact("\"Under this facility, users will be able to withdraw funds from their UPI Lite wallet balance to their "
              "bank account\" ... \"Earlier transfer out was possible only when closing or disabling the UPI Lite "
              "wallet.\" Members to make changes \"by March 31, 2025.\"", D_LITE)])
Q(T, "UPI Lite and international", "Basic",
  "Under NPCI's circular of 27 February 2025 that raised the UPI Lite limits, how can a user replenish (top up) the used "
  "UPI Lite limit?",
  ["Only in online mode, with an additional factor of authentication (AFA)",
   "Only offline, by tapping the phone at an NFC terminal",
   "Only at a bank branch, by filling a top-up form",
   "Automatically from any wallet, without any authentication"],
  concept="Replenishing UPI Lite",
  explanation="While UPI Lite payments themselves are small and need no PIN, NPCI's circular says replenishment of the "
              "used limit is allowed only in online mode with an additional factor of authentication. This keeps the "
              "movement of money from the bank account into UPI Lite secure.",
  steps=["Small payments from UPI Lite: no PIN", "Top-up from the bank account: online with AFA"],
  why="Top-up is not done offline at NFC terminals or through branch forms, and it is never without authentication.",
  facts=[fact("\"Replenishment of the used limit shall be allowed only in online mode with AFA\" ... \"the enhanced limit "
              "shall be Rs 1000 per transaction with Rs 5,000 being the total limit.\"", D_LITE)])
Q(T, "UPI Lite and international", "Intermediate",
  "A cross-border link that went live on 6 June 2026 lets people in India and Nepal send money to each other in real "
  "time. It connects UPI with which Nepali system, and who built it?",
  ["Nepal's National Payments Interface (NPI); built by NIPL and Nepal Clearing House Ltd",
   "Nepal's Fonepay network; built by NPCI and Nepal Rastra Bank",
   "Nepal's National Payments Interface (NPI); built by SBI and Nepal SBI Bank Ltd",
   "Nepal's NEFT-linked remittance scheme; built by RBI and Nepal Clearing House Ltd"],
  concept="UPI's international linkages",
  explanation="The UPI–NPI linkage connects India's UPI with Nepal's National Payments Interface. It was developed by "
              "NPCI International Payments Ltd (NIPL), NPCI's international arm, and Nepal Clearing House Ltd (NCHL), "
              "and became operational on 6 June 2026 for real-time peer-to-peer transfers both ways.",
  steps=["Nepali system: National Payments Interface (NPI)", "Builders: NIPL and NCHL"],
  why="Fonepay is a different Nepali network and the builders were not NPCI with Nepal Rastra Bank; SBI and Nepal SBI "
      "Bank run the older Indo-Nepal Remittance Facility, which uses NEFT, not this UPI link.",
  facts=[fact("The service became operational on \"June 6, 2026\" ... It connects India's UPI with Nepal's National "
              "Payments Interface (NPI) ... built by NPCI International Payments Limited (NIPL) ... and Nepal Clearing "
              "House Limited (NCHL).", D_NEPAL)],
  current=ca("2026-06-06"))
Q(T, "Features", "Advanced",
  "Consider the following statements about the debate on charges on UPI in August 2026:\nI. UPI has remained free for "
  "users and merchants since January 2020.\nII. The Taxation and Other Laws (Amendment) Bill, 2026 amends Section 10A of "
  "the Payment and Settlement Systems Act, 2007, which the Ministry of Finance called only an enabling provision.\n"
  "III. Once the Bill is enacted, RBI's Board for Regulation and Supervision of Payment and Settlement Systems will fix "
  "the MDR on UPI.\nWhich of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Zero MDR on UPI and the 2026 amendment",
  explanation="UPI has been free for users and merchants since January 2020. The Taxation and Other Laws (Amendment) "
              "Bill, 2026 amends Section 10A of the PSS Act so that the Centre can notify payment modes; the Ministry "
              "of Finance clarified on 8 August 2026 that this is only an enabling provision. Whether any MDR is "
              "needed is to be decided by the NPCI-led UPI and Services Steering Committee, not by an RBI board.",
  steps=["I: free since January 2020 - correct", "II: Section 10A, enabling provision - correct",
         "III: decision rests with the NPCI-led UPI and Services Steering Committee - wrong"],
  why="Any option with III is wrong because the MDR decision is left to the NPCI-led steering committee; 'II and III' "
      "and 'I and III' also omit a correct statement.",
  facts=[fact("UPI \"has remained free for users and merchants since January 2020.\"", D_MDR),
         fact("The Taxation and Other Laws (Amendment) Bill, 2026 would amend Section 10A of the Payment and Settlement "
              "Systems Act, 2007 ... \"only an enabling provision and does not automatically impose MDR on UPI "
              "transactions.\" Ministry of Finance clarification: 8 August 2026.", D_MDR),
         fact("After the bill is enacted, the NPCI-led \"UPI and Services Steering Committee\" will decide whether MDR "
              "is required and, if so, its structure.", D_MDR)],
  current=ca("2026-08-08"))

# ================= NEFT (Basic 1 / Intermediate 1 / Advanced 1)
T = "NEFT"
neft_batch, neft_window = 15 * 60 + 30, 120
assert divmod(neft_batch + neft_window, 60) == (17, 30)
Q(T, "Settlement and timings", "Basic",
  "NEFT is available round the clock on all days and settles in half-hourly batches. According to RBI's NEFT FAQs, "
  "what happens if the NEFT system is not available at some time?",
  ["RBI broadcasts a message to all NEFT participants",
   "Pending transactions are automatically moved to RTGS",
   "Banks must convert pending transfers into demand drafts",
   "NPCI routes the pending transactions through IMPS"],
  concept="NEFT availability",
  explanation="RBI's FAQs say NEFT is available on a 24x7x365 basis with batches every half hour. If the system is "
              "unavailable for any reason, RBI broadcasts a message to all participants of NEFT.",
  steps=["NEFT runs 24x7x365 in half-hourly batches", "Unavailability is announced by an RBI broadcast message"],
  why="There is no automatic shift of NEFT transactions to RTGS or IMPS, and no conversion into demand drafts; NEFT is "
      "operated by RBI, not NPCI.",
  facts=[fact("\"The NEFT system is available round the clock throughout the year on all days, i.e., on 24x7x365 "
              "basis.\" NEFT runs in batches every half hour. If it is unavailable, RBI broadcasts a message to all "
              "participants.", D_NEFT)])
Q(T, "Settlement and timings", "Intermediate",
  "An NEFT transfer is settled in the 15:30 batch, but the beneficiary's account turns out to be closed. According to "
  "RBI's NEFT FAQs, what must happen?",
  ["The beneficiary bank returns it by 17:30, and the originating bank shows the entry as 'NEFT-Return' in the "
   "remitter's statement",
   "The beneficiary bank returns it by the end of the next working day, marked 'Unpaid NEFT'",
   "The beneficiary bank holds the funds until the remitter files a claim with RBI",
   "The beneficiary bank returns it within 30 minutes, marked 'NEFT-Reject'"],
  concept="Return of failed NEFT credits",
  explanation="If the beneficiary's account cannot be credited, the destination bank must return the transaction to "
              "the originating branch within two hours of completion of the batch in which it was processed, here by "
              "17:30. The originating bank should then mark the returned entry as 'NEFT-Return' in the remitter's "
              "pass book or statement.",
  steps=["Batch 15:30 + 2 hours = 17:30", "Returned entry labelled 'NEFT-Return'"],
  why="The return window is two hours from the batch, not the next working day and not 30 minutes (that is RTGS "
      "crediting); the bank cannot hold funds pending a claim; and the labels 'Unpaid NEFT' and 'NEFT-Reject' are not "
      "the prescribed one.",
  facts=[fact("The destination bank must \"return the transaction (to the originating branch) within two hours of "
              "completion of the batch in which the transaction was processed.\"", D_NEFT),
         fact("If a payment fails, the originating bank should label the originator's entry \"NEFT-Return\" in the "
              "passbook or statement.", D_NEFT)],
  computed=True)
Q(T, "Settlement and timings", "Advanced",
  "Consider the following statements about RBI's circular of 6 December 2019 that made NEFT available 24x7 from "
  "16 December 2019:\nI. NEFT transactions after usual banking hours were expected to be automated transactions "
  "initiated through straight-through processing (STP) modes.\nII. Member banks were expected to keep adequate "
  "liquidity in their current accounts with RBI at all times.\nIII. Banks were to send the positive confirmation "
  "message (N06) for all NEFT credits.\nWhich of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Operating NEFT round the clock",
  explanation="The 2019 circular said NEFT transactions after usual banking hours were expected to be automated, "
              "initiated through STP modes, and that member banks must keep adequate liquidity in their current "
              "accounts with RBI at all times so that every batch settles. It required positive confirmation for all "
              "NEFT credits through the N10 message, not N06.",
  steps=["I: STP after banking hours - correct", "II: adequate liquidity in RBI current account - correct",
         "III: the positive confirmation message is N10 - wrong"],
  why="Options containing III are wrong because the message type is N10; 'I and III' and 'II and III' also leave out a "
      "correct statement.",
  facts=[fact("\"NEFT transactions after usual banking hours of banks are expected to be automated transactions\" "
              "initiated through Straight Through Processing.", D_NEFT24),
         fact("\"Member banks are expected to keep adequate liquidity in their current account with Reserve Bank of "
              "India at all times\"", D_NEFT24),
         fact("\"Member banks will ensure sending of positive confirmation message (N10) for all NEFT credits.\"",
              D_NEFT24)])

# ================= RTGS (Basic 1 / Intermediate 2 / Advanced 2)
T = "RTGS"
Q(T, "Limits and timings", "Basic",
  "According to RBI's RTGS FAQs (updated October 2026), roughly how many bank branches are RTGS-enabled?",
  ["More than 1,82,000", "About 50,000", "About 95,000", "More than 5,00,000"],
  concept="Reach of RTGS",
  explanation="Both the sending and the receiving branch must be RTGS-enabled. RBI's FAQs say more than 1,82,000 bank "
              "branches are RTGS-enabled, and the list is on RBI's website, updated every fortnight.",
  steps=["Recall RBI's FAQ on RTGS-enabled branches", "More than 1,82,000"],
  why="50,000 and 95,000 understate the network, and 5,00,000 exceeds the total number of bank branches in India.",
  facts=[fact("Both the sending and receiving branches must be RTGS-enabled. More than 1,82,000 branches are enabled. "
              "RBI's website lists them, updated every fortnight.", D_RTGS)],
  current=ca("2026-10-14"))
Q(T, "Limits and timings", "Intermediate",
  "In RTGS the beneficiary bank credits the account solely on the basis of the account number in the payment "
  "message. What reason do RBI's RTGS FAQs give for this?",
  ["Names cannot be matched before credit in a real-time system, and spellings of names vary in India",
   "The beneficiary's name is not allowed to be part of an RTGS message",
   "RBI's books record only account numbers, not names",
   "The name check is done afterwards by NPCI for all RTGS credits"],
  concept="Credit on account number in RTGS",
  explanation="RBI explains that in a real-time transfer, matching names before crediting is not possible, and the "
              "spelling of names varies across India. Credit is therefore given on the account number alone, which "
              "is why the remitter must be extremely careful with it.",
  steps=["Real-time credit leaves no time for name matching", "Name spellings vary",
         "Hence credit on account number only"],
  why="The beneficiary's name is a required field in an RTGS message; RBI's books hold banks' settlement accounts, not "
      "customer names; and NPCI does no after-the-fact name check of RTGS credits.",
  facts=[fact("Real-time transfers can't match names before crediting, and name spellings vary in India. Chapter 11 of "
              "the RTGS System Regulations has more detail.", D_RTGS),
         fact("Be extremely careful with the account number, since credit depends only on it.", D_RTGS)])
Q(T, "Limits and timings", "Intermediate",
  "A new entity has applied for membership of the RTGS system. According to RBI's RTGS FAQs, where is the membership "
  "procedure laid down, and how can the applicant check the status of its application?",
  ["In the RTGS System Regulations; the status can be checked on RBI's PRAVAAH portal",
   "In the NPCI Procedural Guidelines; the status can be checked on the NPCI website",
   "In the Banking Regulation Act, 1949; the status is sent by post",
   "In the RBI Act, 1934; the status can be checked on the CIMS portal"],
  concept="RTGS membership",
  explanation="RBI's FAQs say the procedure for RTGS membership is set out in the RTGS System Regulations, and applicants "
              "can check the status of their application through the PRAVAAH portal. Timelines for applications under "
              "the PSS Act, 2007 are set in RBI's Citizens' Charter.",
  steps=["Procedure: RTGS System Regulations", "Status: PRAVAAH portal"],
  why="RTGS is owned and run by RBI, not NPCI; the BR Act and RBI Act do not lay down RTGS membership procedure; and "
      "CIMS is RBI's supervisory returns portal, not the application-tracking portal.",
  facts=[fact("How do entities apply for membership? The procedure is set out in the RTGS System Regulations. How can "
              "applicants check their status? Through the PRAVAAH portal.", D_RTGS)])
Q(T, "Limits and timings", "Advanced",
  "Consider the following statements based on RBI's RTGS FAQs:\nI. Unlike NEFT, which settles transactions in batches, "
  "RTGS processes each transaction continuously throughout the day.\nII. Customers can track the status of an RTGS "
  "transaction directly in the RTGS system.\nIII. The lists of IFSCs and RTGS-enabled branches on RBI's website are "
  "updated every fortnight.\nWhich of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="RTGS operation and information",
  explanation="RTGS processes instructions continuously, while NEFT batches transactions received up to set times. "
              "Customers cannot track an RTGS transaction themselves; under positive confirmation the remitting bank "
              "gets the credit confirmation and informs them. RBI's IFSC and branch lists are updated every fortnight.",
  steps=["I: continuous vs batch - correct", "II: customers cannot track directly - wrong",
         "III: fortnightly updates - correct"],
  why="Options containing II are wrong because RBI says customers cannot track RTGS directly; 'I and II only' also "
      "omits the correct statement III.",
  facts=[fact("NEFT batches transactions received up to set times. RTGS processes each transaction continuously "
              "throughout the day.", D_RTGS),
         fact("Customers cannot track it directly. Under positive confirmation, the remitting bank receives RBI's "
              "confirmation, via the beneficiary bank, that the money was credited, and then informs the customer.",
              D_RTGS),
         fact("RBI's website publishes IFSC lists, updated every fortnight.", D_RTGS)])
rtgs_recv, rtgs_tat = 21 * 60 + 5, 30
assert divmod(rtgs_recv + rtgs_tat, 60) == (21, 35)
Q(T, "Limits and timings", "Advanced",
  "At 21:00 on a Sunday, Alpha Traders sends ₹30 lakh by RTGS to Beta Ltd. Beta's bank receives the payment message at "
  "21:05 and credits the account. Based on RBI's RTGS FAQs, which of the following are correct?\nI. Beta's bank "
  "had to credit the account by 21:35.\nII. Beta's account statement must show Alpha Traders' name, and Alpha's "
  "statement must show Beta Ltd's name.\nIII. Alpha learns of the credit only by asking Beta, since banks do not "
  "confirm RTGS credits.",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Applying RTGS crediting and statement rules",
  explanation="RTGS runs 24x7, and the beneficiary bank must credit within 30 minutes of receiving the message, so by "
              "21:35. RBI requires members to show the ordering customer's name on the beneficiary's statement and the "
              "beneficiary's name on the originator's statement. Through positive confirmation, Beta's bank sends an "
              "acknowledgement of credit through RTGS/SFMS to Alpha's bank, which informs Alpha, so III is wrong.",
  steps=["21:05 + 30 minutes = 21:35 -> I correct", "Statements carry the counterparty's name -> II correct",
         "Positive confirmation exists -> III wrong"],
  why="Options with III are wrong because positive confirmation informs the remitter through its bank; 'II and III' "
      "and 'I and III' also omit a correct statement.",
  facts=[fact("The beneficiary bank must credit the account within 30 minutes of receiving the message.", D_RTGS),
         fact("Members must show the debtor (ordering customer) name and creditor (beneficiary customer) name. The "
              "beneficiary's statement shows the originator's name, and the originator's statement shows the "
              "beneficiary's name.", D_RTGS),
         fact("The beneficiary bank sends a credit acknowledgement through RTGS/SFMS messaging to the remitting bank, "
              "which can then update its customer.", D_RTGS)],
  computed=True)

# ================= IMPS (Basic 1 / Intermediate 1 / Advanced 1)
T = "IMPS"
Q(T, "Limits and features", "Basic",
  "An IMPS transfer debits the sender's account but the beneficiary's account is not credited. Under RBI's circular of "
  "20 September 2019 on harmonisation of turn-around time (TAT) for failed transactions, by when must the beneficiary "
  "bank reverse it?",
  ["Latest on T + 1 day, where T is the day of the transaction",
   "Within T + 5 days",
   "Within 2 hours of the next settlement batch",
   "Within 30 days, after the customer files a complaint"],
  concept="TAT for failed IMPS transfers",
  explanation="RBI's 2019 framework on harmonisation of TAT says that when an IMPS transfer debits the account but the "
              "beneficiary is not credited, the beneficiary bank must auto-reverse it latest on T + 1 day. Beyond "
              "that, the bank pays ₹100 per day of delay to the customer.",
  steps=["Failed IMPS credit -> auto-reversal by beneficiary bank", "Deadline: T + 1 day; then ₹100 per day"],
  why="T + 5 applies to failures such as ATM cash not dispensed; the 2-hour rule belongs to NEFT; and the reversal is "
      "automatic, not dependent on a complaint.",
  facts=[fact("IMPS (row 3a, beneficiary not credited): Reversal by the beneficiary bank \"latest on T + 1 day.\" "
              "Compensation is ₹100 per day beyond T + 1.", D_TAT)])
Q(T, "Limits and features", "Intermediate",
  "In December 2024 RBI asked banks to offer a beneficiary account name look-up facility for RTGS and NEFT by 1 April "
  "2025, noting that a similar check already existed in which systems, and asking which body to build it?",
  ["UPI and IMPS; NPCI was advised to develop it and onboard all banks",
   "UPI and IMPS; IDRBT was advised to develop it on the SFMS platform",
   "AePS and NACH; NPCI was advised to develop it and onboard all banks",
   "Cheque truncation and NACH; CCIL was advised to develop it"],
  concept="Name verification before payment",
  explanation="RBI's circular of 30 December 2024 notes that UPI and IMPS already let a remitter verify the beneficiary's "
              "name before paying, and extends a similar facility to RTGS and NEFT. NPCI was advised to develop the "
              "facility and onboard all banks; NPCI does not store any data relating to it.",
  steps=["Existing name check: UPI and IMPS", "Developer: NPCI"],
  why="IDRBT and CCIL were not given this task; AePS, NACH and cheque truncation are not the systems RBI cited as already "
      "offering pre-payment name verification.",
  facts=[fact("UPI and IMPS already let a remitter check the beneficiary's name before paying ... \"National Payments "
              "Corporation of India (NPCI) has been advised to develop the facility and onboard all banks.\"",
              D_LOOKUP),
         fact("Direct and sub-members must offer the facility \"no later than April 1, 2025.\" \"NPCI shall not store "
              "any data relating to this facility.\"", D_LOOKUP)])
# Customer compensation: IMPS failed credit reversed on T+4; ATM cash not dispensed, reversed on T+7.
imps_tat, atm_tat, rate = 1, 5, 100
imps_r, atm_r = 4, 7
comp = (imps_r - imps_tat) * rate + (atm_r - atm_tat) * rate
assert comp == 500
assert (imps_r - 1) * rate + (atm_r - 1) * rate == 900      # both counted from T+1 (wrong)
assert imps_r * rate + atm_r * rate == 1100                  # counted from T (wrong)
assert (imps_r - imps_tat) * rate == 300                     # IMPS part only (wrong)
Q(T, "Limits and features", "Advanced",
  "On day T, Ravi's IMPS transfer debits his account but is never credited to the beneficiary; the reversal reaches "
  "his account on T + 4. On the same day T, an ATM of another bank debits his account without dispensing cash; that "
  "reversal is concluded on T + 7. Under RBI's circular of 20 September 2019 on harmonisation of TAT and customer "
  "compensation for failed transactions, what total compensation is due to Ravi?",
  [f"₹{comp}", "₹900", "₹1,100", "₹300"],
  concept="Compensation for delayed reversal of failed transactions",
  explanation="For an IMPS transfer not credited to the beneficiary, reversal is due latest on T + 1, and ₹100 per day "
              "is payable beyond that. For an ATM transaction where cash is not dispensed, reversal is due within "
              "T + 5, with ₹100 per day beyond. IMPS: 4 − 1 = 3 days × ₹100 = ₹300; ATM: 7 − 5 = 2 days × ₹100 = "
              "₹200; total ₹500.",
  steps=["IMPS TAT T + 1; delay 3 days -> ₹300", "ATM TAT T + 5; delay 2 days -> ₹200", "Total = ₹500"],
  why="₹900 wrongly applies the T + 1 deadline to the ATM failure too; ₹1,100 counts delay from day T; ₹300 ignores the "
      "ATM compensation.",
  facts=[fact("IMPS (row 3a, beneficiary not credited): Reversal by the beneficiary bank \"latest on T + 1 day.\" "
              "Compensation is ₹100 per day beyond T + 1.", D_TAT),
         fact("ATM (cash not dispensed, row 1a): \"Pro-active reversal (R) of failed transaction within a maximum of "
              "T + 5 days.\" Compensation is ₹100 per day of delay beyond T + 5.", D_TAT)],
  computed=True)

# ================= NPCI (Basic 2 / Intermediate 1 / Advanced 1)
T = "NPCI"
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Basic",
  "In June 2022, RBI allowed credit cards to be linked to the UPI platform for the first time. Which credit cards were "
  "to be linked to begin with?",
  ["RuPay credit cards", "Visa credit cards", "Mastercard credit cards", "Corporate credit cards of all networks"],
  concept="Credit cards on UPI",
  explanation="In the Governor's Statement of 8 June 2022, RBI noted that UPI then linked only savings and current "
              "accounts through debit cards, and proposed to allow credit cards on UPI, beginning with RuPay credit "
              "cards issued on NPCI's own card network.",
  steps=["UPI earlier linked only savings/current accounts", "First credit cards on UPI: RuPay"],
  why="Visa, Mastercard and corporate cards were not the starting point; RBI specified RuPay credit cards to begin with.",
  facts=[fact("\"It is now proposed to allow linking of credit cards on the UPI platform.\" \"To begin with, the Rupay "
              "credit cards will be linked to the UPI platform.\"", D_RUPAYCC)])
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Basic",
  "NPCI's National Automated Clearing House (NACH), used for bulk payments such as salaries, dividends and EMIs, was "
  "earlier available only on days when banks were functional. From which date did RBI decide, in June 2021, to make "
  "NACH available on all days of the week?",
  ["1 August 2021", "1 July 2021", "16 December 2019", "14 December 2020"],
  concept="NACH on all days of the week",
  explanation="In its Statement on Developmental and Regulatory Policies of 4 June 2021, RBI noted that NACH was "
              "available only on bank working days and, to take advantage of RTGS being available on all days, "
              "decided to make NACH available on all days of the week throughout the year from 1 August 2021.",
  steps=["Before: bank working days only", "Leveraging 24x7 RTGS -> NACH on all days from 1 August 2021"],
  why="16 December 2019 is when NEFT went 24x7 and 14 December 2020 when RTGS went 24x7; 1 July 2021 is not the date "
      "RBI announced.",
  facts=[fact("NACH is currently available only on the days when banks are functional. In the interest of customer "
              "convenience, and to take advantage of the availability of RTGS on all days of the year, it is proposed "
              "to make available NACH on all days of the week throughout the year, effective August 1, 2021.",
              D_NACH7)])
Q(T, "Products: NACH, AePS, RuPay, FASTag", "Intermediate",
  "RBI's AePS Directions on due diligence of AePS Touchpoint Operators (ATOs), effective 1 January 2026, apply to the "
  "agents through whom customers withdraw cash using Aadhaar biometrics. Which requirement do they impose on acquiring "
  "banks?",
  ["KYC-based due diligence before onboarding an ATO, repeated for an ATO inactive for a continuous period of three "
   "months",
   "Each ATO must be a permanent employee of the acquiring bank",
   "Each ATO must be licensed directly by NPCI before onboarding",
   "Each ATO must deposit a security of ₹1 lakh with UIDAI"],
  concept="Due diligence of AePS Touchpoint Operators",
  explanation="RBI issued the final Directions on 27 June 2025, effective 1 January 2026, to curb AePS frauds. Acquiring "
              "banks must carry out KYC-based due diligence of ATOs before onboarding them, and the KYC verification "
              "applies again to ATOs that have remained inactive for a continuous period of three months. Banks must "
              "also monitor ATOs through their transaction monitoring systems.",
  steps=["Who: acquiring banks onboarding ATOs", "KYC before onboarding", "Again after three months' inactivity"],
  why="ATOs need not be bank employees (they can be BCs or sub-agents); NPCI does not license ATOs; and no UIDAI "
      "security deposit is prescribed.",
  facts=[fact("The directions cover due diligence requirements for ATOs and risk management instructions for their "
              "activities. \"These directions shall come into effect from January 01, 2026.\"", D_AEPSPR),
         fact("Acquiring banks must \"conduct due diligence as per the Know Your Customer (KYC) Directions, 2016\" ... "
              "KYC verification applies to operators who \"have remained inactive for a continuous period of three "
              "months\".", D_AEPSMN)],
  current=ca("2026-01-01"))

Q(T, "Products: NACH, AePS, RuPay, FASTag", "Advanced",
  "Consider the following statements about RBI's circular of 22 August 2024 on processing of e-mandates for recurring "
  "transactions:\nI. Auto-replenishment of FASTag and NCMC balances, as and when the balance falls below a threshold "
  "set by the customer, was brought under the e-mandate framework.\nII. Such auto-replenishment debits are exempt "
  "from the requirement of a pre-debit notification at least 24 hours before the debit, because they are recurring but "
  "have no fixed periodicity.\nIII. For these payments, all other instructions of the e-mandate framework ceased to "
  "apply.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="E-mandates for FASTag and NCMC top-ups",
  explanation="The circular included auto-replenishment of FASTag (NPCI's NETC tag) and the National Common Mobility "
              "Card in the e-mandate framework whenever the balance falls below a customer-set threshold (I). Since "
              "these payments recur without fixed periodicity, they are exempt from the 24-hour pre-debit notification "
              "(II). All other e-mandate instructions continue to apply, so III is wrong.",
  steps=["I: FASTag/NCMC top-ups under e-mandates -> true", "II: no pre-debit notification -> true",
         "III: other instructions continue -> false"],
  why="Any option with III is wrong because the circular keeps the rest of the framework; 'I only' leaves out the "
      "pre-debit exemption in II.",
  facts=[fact("It has been decided to include auto-replenishment of FASTag and NCMC, as and when the balance falls below "
              "a threshold ... Payments for auto-replenishment, since they are recurring in nature but without any "
              "fixed periodicity, will be exempt from the requirement of pre-debit notification", D_EMAND),
         fact("the issuer shall send a pre-debit notification to the customer at least 24 hours prior to the actual "
              "charge / debit ... All other instructions provided under the e-mandate framework shall continue to "
              "remain applicable.", D_EMAND)])


# ######## section E
# ---- sources (group E), opened 2026-11-06
E_PBMISC = "https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=13087"   # RBI (Payments Banks - Miscellaneous) Directions, 2025 (updated 1 Oct 2026)
E_SFB25 = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=13135"       # RBI (Small Finance Banks - Licensing) Guidelines, 2025
E_PSL = "https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12799"     # PSL - Targets and Classification Directions, 2025 (updated 11 Sep 2026)
E_BRANCH = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13164"  # CB - Branch Authorisation Directions, 2025 (updated 1 Oct 2026)
E_LBS = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13521&Mode=0"  # Lead Bank Scheme circular, 19 June 2026
E_LBSPR = "https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=62980"  # press release 2026-2027/502, 19 June 2026
E_PMJDY12 = "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/aug/doc_9716_20260827_14055201.pdf"  # PIB note, 12 years of PMJDY
E_PIB18 = "https://pib.gov.in/PressReleasePage.aspx?PRID=1545090"               # PIB release on PMJDY extension (2018), search snippet only
E_PMI = "https://pmindia.gov.in/?p=4117701"                                     # PM India page on PMJDY, search snippet only (403 on open)
SEARCH_ONLY.update({E_PIB18, E_PMI})

# ================= Payment Banks (Basic 2 / Intermediate 2 / Advanced 2)
T = "Payment Banks"
Q(T, "Permitted activities", "Basic",
  "Payments banks may issue prepaid payment instruments (PPIs) in addition to opening normal accounts. Under RBI's "
  "Payments Banks – Miscellaneous Directions, 2025, which restriction applies to the group to which a payments bank "
  "belongs?",
  ["A separate PPI-issuing entity cannot coexist with the payments bank in the same group",
   "No entity in the group may hold a banking licence of any kind for 10 years",
   "The group must route all its UPI transactions through the payments bank",
   "The group may hold a PPI entity only if it is listed on a stock exchange"],
  concept="Payments banks and PPIs",
  explanation="The Directions say payments banks may undertake only restricted activities such as accepting demand "
              "deposits, and they can issue PPIs in addition to opening normal accounts. Because the payments bank "
              "itself can issue PPIs, a separate PPI entity cannot coexist with it in the same group.",
  steps=["PBs may issue PPIs themselves", "Hence no separate PPI entity in the same group"],
  why="The Directions impose no 10-year bar on other licences, no UPI-routing rule and no listing-based exception; "
      "they simply prohibit a PPI entity in the same group.",
  facts=[fact("PBs may undertake only certain restricted activities such as acceptance of demand deposits ... PBs can "
              "issue PPIs in addition to opening normal accounts ... a PPI entity cannot coexist with the PB in the "
              "same group.", E_PBMISC)])
Q(T, "Deposit limit", "Basic",
  "A payments bank both maintains savings accounts and issues prepaid wallets (PPIs) to its customers. Under RBI's "
  "Payments Banks – Miscellaneous Directions, 2025, how does the ₹2 lakh end-of-day limit per individual customer "
  "treat the customer's PPI balance with that payments bank?",
  ["The PPI balance also counts towards the ₹2 lakh limit",
   "The PPI balance is excluded and has a separate ₹2 lakh limit",
   "The PPI balance counts only if it exceeds ₹50,000",
   "The PPI balance counts only for customers with minimum KYC"],
  concept="Scope of the payments bank balance limit",
  explanation="Payments banks may hold a maximum balance of ₹2,00,000 per individual customer at the end of the day, "
              "and the Directions state that this individual customer limit applies to PPI balances also. So deposits "
              "and wallet balances with the payments bank are taken together.",
  steps=["Limit: ₹2 lakh per individual customer at day-end", "Applies to PPI balances also"],
  why="There is no separate wallet limit within a payments bank, no ₹50,000 threshold and no KYC-based carve-out "
      "for counting PPI balances in this limit.",
  facts=[fact("PBs are restricted to holding a maximum balance of ₹2,00,000 per individual customer at the end of the "
              "day. The individual customer limit applies to PPI balances also.", E_PBMISC)])
Q(T, "Permitted activities", "Intermediate",
  "Payments banks are barred from lending. Under RBI's Payments Banks – Miscellaneous Directions, 2025, which "
  "exception to this bar exists?",
  ["Loans to its own employees out of the bank's own funds, under a Board-approved policy capping such loans",
   "Loans to its directors, if approved by the full Board without the interested director",
   "Overdrafts up to ₹10,000 to customers whose accounts have run satisfactorily for six months",
   "Loans against the pledge of the customer's own fixed deposit with the payments bank"],
  concept="Lending restriction on payments banks",
  explanation="The Directions say a payments bank shall not lend to any person, including its directors. The only "
              "carve-out is lending to its own employees out of the bank's own funds, as per a Board-approved policy "
              "that sets caps on such loans.",
  steps=["General rule: no lending to any person, including directors", "Exception: own employees, own funds, Board "
         "policy with caps"],
  why="Directors are expressly covered by the bar; the ₹10,000 overdraft is a PMJDY feature of full-service banks, "
      "not of payments banks; and payments banks cannot accept fixed deposits, so there is no deposit to lend against.",
  facts=[fact("A bank shall not lend to any person including its directors ... the bank may lend to its own employees "
              "out of the bank's own funds ... a Board approved policy outlining the caps on such loans.", E_PBMISC)])
Q(T, "Deposit limit", "Intermediate",
  "A payments bank collects a security deposit of ₹5 lakh from a technology vendor that provides it services. Under "
  "RBI's Payments Banks – Miscellaneous Directions, 2025, how is this treated against the ₹2 lakh end-of-day limit?",
  ["It is outside the limit, which applies to customer deposits and not to security or earnest money deposits",
   "It breaches the limit, so ₹3 lakh must be swept to a partner bank at the end of the day",
   "It is allowed only if the vendor is a scheduled commercial bank",
   "It must be held in Treasury Bills, as payments banks cannot hold any balance above ₹2 lakh"],
  concept="What the payments bank limit covers",
  explanation="The ₹2 lakh end-of-day cap is a limit per individual customer. The Directions clarify that it applies "
              "to customer deposits and not to any security or earnest money deposit, such as one collected from a "
              "service provider.",
  steps=["Limit is on customer deposits", "Security/earnest money deposits are excluded", "No sweep needed"],
  why="A sweep applies only to customer balances above the limit; there is no condition that the vendor be a bank; "
      "and nothing requires such a deposit to be held in Treasury Bills.",
  facts=[fact("The above limit shall apply to customer deposits and not to any security/earnest money deposit", E_PBMISC)])
Q(T, "Permitted activities", "Advanced",
  "A payments bank (PB) has a sweep arrangement under which its customers' balances above ₹2 lakh move to their "
  "accounts with a partner bank, for which it is also a business correspondent. Under RBI's Payments Banks – "
  "Miscellaneous Directions, 2025, consider: I. With a general consent from the customer, the PB may itself initiate "
  "debits in the customer's account held with the partner bank. II. As the partner bank's BC, the PB may facilitate "
  "withdrawals and transfers by the customer from that account. III. The PB may arrange intraday funding for the "
  "customer against the balance lying with the partner bank. Which of the above is/are correct?",
  ["II only", "I and II only", "II and III only", "I, II and III"],
  concept="Limits of the payments bank sweep arrangement",
  explanation="The PB shall not have rights to operate or real-time access to funds held with the other bank and "
              "shall not initiate any debit in the customer's account with another bank, even under a power of "
              "attorney or general consent (I wrong). As a BC of that bank it may facilitate withdrawals and "
              "transfers by the customer (II right). It shall neither arrange nor avail of intraday funding for "
              "customers based on balances with other banks (III wrong).",
  steps=["I: PB cannot debit the other-bank account → false", "II: allowed as BC → true",
         "III: no intraday funding → false"],
  why="Any option including I or III is wrong, because the Directions bar both self-initiated debits and intraday "
      "funding against the swept balances.",
  facts=[fact("PBs shall not initiate any debit transactions in the customer's account, held with another bank ... "
              "However, as a BC of a bank, PBs may facilitate withdrawals and transfers by the customer", E_PBMISC),
         fact("A PB shall neither arrange nor avail of intraday funding facilities for its customers", E_PBMISC)])
e_sb, e_ppi, e_emd = 140000, 45000, 50000
e_counted = e_sb + e_ppi
assert e_counted == 185000 and e_counted <= 200000 and e_counted + e_emd == 235000
Q(T, "Deposit limit", "Advanced",
  "At the end of a day, Kiran, a small trader, has ₹1,40,000 in his savings account with a payments bank and "
  "₹45,000 in a PPI wallet issued by the same payments bank. He has also placed an earnest money deposit of ₹50,000 "
  "with the payments bank as a service provider to it. Under RBI's Payments Banks – Miscellaneous Directions, 2025, "
  "what is the position?",
  ["Balance counted is ₹1,85,000, within the ₹2 lakh limit; no sweep is needed",
   "Balance counted is ₹2,35,000; ₹35,000 must be swept to a partner bank",
   "Balance counted is ₹1,40,000; the wallet and earnest money are both outside the limit",
   "Balance counted is ₹1,90,000; ₹10,000 of the earnest money counts towards the limit"],
  concept="Applying the payments bank end-of-day limit",
  explanation="The ₹2 lakh limit per individual customer covers customer deposits and PPI balances, but not security "
              "or earnest money deposits. So ₹1,40,000 + ₹45,000 = ₹1,85,000 is counted, which is within the limit.",
  steps=["Savings ₹1,40,000 counts", "PPI ₹45,000 counts (limit applies to PPI balances)",
         "Earnest money ₹50,000 excluded", "₹1,85,000 ≤ ₹2,00,000 → no sweep"],
  why="Adding the earnest money (₹2,35,000) wrongly includes an excluded deposit; leaving out the wallet ignores that "
      "PPI balances count; there is no partial counting of earnest money.",
  facts=[fact("PBs are restricted to holding a maximum balance of ₹2,00,000 per individual customer at the end of the "
              "day. The individual customer limit applies to PPI balances also.", E_PBMISC),
         fact("The above limit shall apply to customer deposits and not to any security/earnest money deposit", E_PBMISC)],
  computed=True)

# ================= Small Finance Banks (Basic 1 / Intermediate 1 / Advanced 1)
T = "Small Finance Banks"
Q(T, "Licensing norms", "Basic",
  "Under the RBI (Small Finance Banks – Licensing) Guidelines, 2025, may a small finance bank set up subsidiaries?",
  ["No, small finance banks are not allowed to set up any subsidiaries",
   "Yes, but only for insurance and mutual fund distribution",
   "Yes, after five years of operations with RBI's approval",
   "Yes, but only an NBFC subsidiary for microfinance"],
  concept="SFB structure",
  explanation="The guidelines allow an SFB's promoter to use a Non-Operative Financial Holding Company as an "
              "intermediate holding company, but they state plainly that small finance banks will not be allowed to "
              "set up any subsidiaries.",
  steps=["Check the corporate-structure clause", "SFBs: no subsidiaries"],
  why="The guidelines carve out no exception for insurance or mutual fund business, for seasoning, or for an NBFC; "
      "the prohibition is absolute.",
  facts=[fact("However, small finance banks will not be allowed to set up any subsidiaries.", E_SFB25)])
Q(T, "Licensing norms", "Intermediate",
  "A promoter group that already holds a universal banking licence proposes to set up a small finance bank, with both "
  "banks held under a Non-Operative Financial Holding Company (NOFHC). Under the RBI (Small Finance Banks – Licensing) "
  "Guidelines, 2025, what is the position?",
  ["It will not be granted licences for both, even under the NOFHC structure",
   "It may, because both banks would be held under an NOFHC",
   "It may, if the SFB operates only in north-eastern States",
   "It may, if the universal bank holds less than 26% of the SFB"],
  concept="One promoter, one type of bank",
  explanation="The guidelines say a promoter will not be granted licences for both a universal bank and a small "
              "finance bank, even if the proposal is to set them up under the NOFHC structure. The NOFHC route is "
              "required, for example, when a payments bank promoter also sets up an SFB, but it does not permit a "
              "universal bank and an SFB together.",
  steps=["Universal bank + SFB under one promoter: not permitted", "NOFHC does not cure this"],
  why="The NOFHC structure is expressly ruled out as a way around the bar; there is no regional or shareholding-based "
      "exception.",
  facts=[fact("A promoter will not be granted licenses for both universal bank and small finance bank even if the "
              "proposal is to set them up under the NOFHC structure.", E_SFB25)])
e_prev_psl = 6000
e_cap = e_prev_psl * 10 // 100
e_q = [520, 560, 640, 680]           # eligible MFI on-lending portfolio, quarter-ends (₹ crore)
e_avg = sum(e_q) / 4
assert e_cap == 600 and e_avg == 600 and e_avg <= e_cap and max(e_q) > e_cap
Q(T, "PSL targets", "Advanced",
  "A small finance bank's total priority sector lending in the previous financial year was ₹6,000 crore. This year "
  "it lends to RBI-registered NBFC-MFIs (members of an RBI-recognised SRO, each with a gross loan portfolio below "
  "₹500 crore as on 31 March of the previous year) for on-lending to individuals. Its eligible outstanding to them at "
  "the four quarter-ends was ₹520 crore, ₹560 crore, ₹640 crore and ₹680 crore. Under RBI's PSL Directions, 2025, "
  "how much of this lending can it classify as priority sector?",
  ["All of it, as the four-quarter average of ₹600 crore is within the cap of 10% of last year's PSL",
   "Only ₹520 crore, the lowest quarter-end figure, because the cap is tested at every quarter-end",
   "None, because on-lending through NBFC-MFIs is not allowed for SFBs",
   "Only up to ₹300 crore, because the cap is 5% of last year's PSL"],
  concept="SFB lending to MFIs for on-lending",
  explanation="SFBs may classify loans to registered NBFC-MFIs and other MFIs that are SRO members and have a gross "
              "loan portfolio of up to ₹500 crore (as on 31 March of the previous year) for on-lending to "
              "individuals. Such credit is capped at 10% of the bank's total PSL in the previous year (₹600 crore "
              "here), and adherence is measured by averaging across the four quarters: (520 + 560 + 640 + 680)/4 = "
              "₹600 crore, which is within the cap.",
  steps=["Cap = 10% × ₹6,000 crore = ₹600 crore", "Average = (520 + 560 + 640 + 680)/4 = ₹600 crore",
         "₹600 crore ≤ ₹600 crore → within cap"],
  why="The cap is checked on the four-quarter average, not at each quarter-end; the general bar on NBFC on-lending "
      "does not cover this specific MFI route for SFBs; and the cap is 10%, not 5%.",
  facts=[fact("[SFBs: loans to registered NBFC-MFIs and other MFIs] which have a 'gross loan portfolio' (GLP) of up to "
              "₹500 crore as on March 31 of the previous year ... Bank credit as above, up to an overall limit of 10% "
              "of an individual bank's total priority sector lending of the previous financial year, is eligible for "
              "PSL classification.", E_PSL),
         fact("Banks shall determine adherence to the prescribed cap by averaging the eligible portfolio under "
              "on-lending mechanism across four quarters of the current financial year.", E_PSL)],
  computed=True)

# ================= Financial Inclusion (Basic 4 / Intermediate 2 / Advanced 2)
T = "Financial Inclusion"
Q(T, "Business correspondents", "Basic",
  "Under RBI's Commercial Banks – Branch Authorisation Directions, 2025, a 'Banking Outlet', which may be manned by "
  "bank staff or a Business Correspondent, must provide service for at least:",
  ["Four hours a day on at least five days a week",
   "Six hours a day on at least six days a week",
   "Three hours a day on at least four days a week",
   "Eight hours a day on all working days"],
  concept="Banking Outlet definition",
  explanation="A Banking Outlet is a fixed-point service delivery unit, manned by the bank's staff or its BC, that "
              "provides services for a minimum of four hours per day for at least five days a week. An outlet that "
              "falls short of this is a Part-time Banking Outlet.",
  steps=["Fixed point, staffed by bank or BC", "Minimum 4 hours/day, at least 5 days/week"],
  why="The other hour/day combinations are not the definition in the Directions.",
  facts=[fact("'Banking Outlet' is a fixed point service delivery unit, manned by either bank's staff or its Business "
              "Correspondent ... for a minimum of four hours per day for at least five days a week", E_BRANCH)])
Q(T, "Business correspondents", "Basic",
  "Under RBI's Commercial Banks – Branch Authorisation Directions, 2025, an 'Unbanked Rural Centre' (URC) is a:",
  ["Tier 5 or Tier 6 centre that does not have a CBS-enabled Banking Outlet",
   "Village with a population below 2,000 that has no bank branch",
   "Tier 3 or Tier 4 centre without an ATM",
   "Rural centre with no Business Correspondent within 5 km"],
  concept="Unbanked Rural Centre",
  explanation="The Directions define a URC as a rural (Tier 5 and 6) centre that does not have a CBS-enabled Banking "
              "Outlet. Tier 5 covers centres with population 5,000 to 9,999 and Tier 6 below 5,000 (Census 2011).",
  steps=["Rural = Tier 5 and 6", "Unbanked = no CBS-enabled Banking Outlet"],
  why="The definition is not tied to a 2,000 population, to ATMs, to Tier 3-4 centres or to BC distance.",
  facts=[fact("'Unbanked Rural Centre' (URC) is a rural (Tier 5 and 6) centre that does not have a CBS-enabled "
              "'Banking Outlet'", E_BRANCH)])
Q(T, "PMJDY and allied schemes", "Basic",
  "What rate of interest is paid on savings in an account opened under Pradhan Mantri Jan Dhan Yojana (PMJDY)?",
  ["The rate applicable to savings bank accounts",
   "A concessional rate fixed at 1% above the savings rate",
   "No interest, as PMJDY accounts are zero-balance accounts",
   "The rate on 1-year fixed deposits of the bank"],
  concept="PMJDY account interest",
  explanation="The Government's August 2026 note on 12 years of PMJDY says the interest rate applicable to savings "
              "bank accounts applies to accounts opened under PMJDY. Being a zero-balance account does not take "
              "away interest.",
  steps=["PMJDY account is a savings (BSBD) account", "Earns the normal savings bank rate"],
  why="There is no special premium, no zero-interest rule and no link to fixed-deposit rates.",
  facts=[fact("The interest rate applicable to savings bank accounts is applicable to accounts opened under PMJDY "
              "scheme.", E_PMJDY12)])
Q(T, "PMJDY and allied schemes", "Basic",
  "When PMJDY was extended in 2018 with added features, what was decided about the conditions attached to the "
  "overdraft (OD) facility?",
  ["No conditions would be attached for OD up to ₹2,000",
   "No conditions would be attached for OD up to ₹10,000",
   "OD would be allowed only after 12 months of satisfactory operation",
   "OD would be allowed only to holders of a Kisan Credit Card"],
  concept="PMJDY 2018 extension",
  explanation="The 2018 extension raised the OD limit and made the small OD easier to get: no conditions are "
              "attached for an overdraft of up to ₹2,000.",
  steps=["2018 extension of PMJDY", "No conditions for OD up to ₹2,000"],
  why="₹10,000 is the overall OD limit, not the condition-free amount; the six-month operation rule was not extended "
      "to 12 months; and OD is not tied to a Kisan Credit Card.",
  facts=[fact("No conditions for Overdraft upto Rs 2,000", E_PIB18),
         fact("There will not be any conditions attached for OD upto Rs 2,000.", E_PMI)])
Q(T, "PMJDY and allied schemes", "Intermediate",
  "With the extension of PMJDY in 2018, the age limit for availing the overdraft facility in a PMJDY account was "
  "revised to:",
  ["18-65 years, from 18-60 years", "18-60 years, from 21-58 years", "21-65 years, from 18-60 years",
   "18-70 years, from 18-65 years"],
  concept="PMJDY overdraft eligibility",
  explanation="As part of the 2018 changes to PMJDY, the age limit for the overdraft facility was raised at the upper "
              "end, from 18-60 years to 18-65 years.",
  steps=["Earlier: 18-60 years", "From 2018: 18-65 years"],
  why="The lower age stayed at 18, the earlier band was 18-60 (not 21-58 or 18-65), and the new upper limit is 65, "
      "not 70.",
  facts=[fact("Age limit for availing Over Draft facility revised from 18-60 years to 18-65 years.", E_PIB18),
         fact("Age limit for availing OD facility to be revised from 18-60 years to 18-65 years.", E_PMI)])
Q(T, "Business correspondents", "Intermediate",
  "A Business Correspondent (BC) company has been appointed by two banks. Under RBI's Commercial Banks – Branch "
  "Authorisation Directions, 2025, which statement is correct?",
  ["This is allowed, but at the point of customer interface each retail outlet or sub-agent represents the bank that "
   "appointed it",
   "This is not allowed; a BC may work for only one bank",
   "This is allowed only if both banks are public sector banks",
   "This is allowed, and each outlet may offer both banks' products side by side as a common agent"],
  concept="BCs serving more than one bank",
  explanation="The Directions say that while a BC may be a BC for more than one bank, at the point of customer "
              "interface a retail outlet or a sub-agent of the BC shall represent the bank which has appointed the "
              "BC. Each outlet or sub-agent is also attached to a base Banking Outlet of that bank.",
  steps=["Multi-bank BC: permitted", "At customer interface: outlet/sub-agent represents its appointing bank"],
  why="A BC is not restricted to one bank, there is no public-sector-only condition, and an outlet cannot act as a "
      "common agent for both banks at the customer interface.",
  facts=[fact("While a BC may be a BC for more than one bank, at the point of customer interface, a retail outlet or a "
              "sub-agent of a BC shall represent the bank which has appointed the BC.", E_BRANCH)])
Q(T, "Business correspondents", "Advanced",
  "Consider the following statements about a bank's arrangements with its Business Correspondents under RBI's "
  "Commercial Banks – Branch Authorisation Directions, 2025: I. All off-line transactions done through BCs must be "
  "accounted for and reflected in the bank's books by the end of the day. II. The BC issues a receipt on behalf of the "
  "bank as acknowledgment for cash collected from a customer. III. The bank must carry out a detailed review of the "
  "performance of its BCs at least once a quarter. Which of the above is/are correct?",
  ["I and II only", "I, II and III", "II and III only", "I and III only"],
  concept="Operational safeguards for BCs",
  explanation="The Directions require the bank's arrangements to provide that off-line transactions reflect in the "
              "bank's books by the end of the day (I right) and that a receipt is issued on behalf of the bank for "
              "cash collected (II right). The detailed review of BC performance is required at least once in a year, "
              "not every quarter (III wrong).",
  steps=["I: day-end accounting → true", "II: receipt on bank's behalf → true", "III: review is annual → false"],
  why="Any option including III is wrong, because the minimum frequency for the detailed review is once a year.",
  facts=[fact("Issuing a receipt on behalf of the bank as acknowledgment for cash collected from the customer; All "
              "off-line transactions are accounted for and reflect in the books of the bank by the end of the day",
              E_BRANCH),
         fact("A bank shall carry out a detailed review of the performance of various BCs engaged by it at least once "
              "in a year", E_BRANCH)])
Q(T, "PMJDY and allied schemes", "Advanced",
  "Under RBI's revised circular on the Lead Bank Scheme issued on 19 June 2026, in which districts must Special "
  "Sub-Committees (SSCs) of the District Consultative Committee be set up, and with whom as Convenor?",
  ["Districts with a CD ratio below 40% and Annual Credit Plan achievement below 100% in the preceding year; the Lead "
   "District Manager",
   "Districts with a CD ratio below 60% in the preceding year; the District Collector",
   "Districts with a CD ratio below 40% or no banking outlet in some villages; the RBI Lead District Officer",
   "Districts with Annual Credit Plan achievement below 75%; the SLBC Convenor Bank"],
  concept="Lead Bank Scheme, 2026 circular",
  explanation="The revised Lead Bank Scheme circular (19 June 2026) provides that in districts with a CD ratio of less "
              "than 40% as well as ACP achievement of less than 100% for the preceding financial year, Special "
              "Sub-Committees of the DCC, with the LDM as Convenor, shall be set up to monitor the CD ratio. Both "
              "conditions must hold.",
  steps=["Trigger: CD ratio < 40% AND ACP achievement < 100% (preceding FY)", "SSC of the DCC, LDM as Convenor"],
  why="The threshold is 40% (not 60%) and needs both conditions, not either; the Convenor is the LDM, not the "
      "Collector, the RBI LDO or the SLBC Convenor Bank.",
  facts=[fact("In districts having CD Ratio less than 40 percent as well as ACP achievement less than 100% for the "
              "preceding financial year, Special Sub-Committees (SSCs) of the DCC, with LDM as Convenor shall be set "
              "up to monitor the CD Ratio.", E_LBS),
         fact("The revised Circular on the Lead Bank Scheme (LBS) has been issued today.", E_LBSPR)],
  current=ca("2026-06-19"))


# ######## section F
# ---- sources (group F), opened 2026-11-06
F_MD = "https://rbi.org.in/scripts/BS_ViewMasDirections.aspx?id="
F_CP = F_MD + "12592"      # MD - RBI (Commercial Paper and NCDs of original or initial maturity upto one year) Directions, 2024
F_CD = F_MD + "12108"      # MD - RBI (Certificate of Deposit) Directions, 2021
F_UID = F_MD + "13343"     # MD - RBI (Unique Identifiers in Financial Markets) Directions, 2026 (27 Mar 2026)
F_CDS = F_MD + "13552"     # MD - RBI (Credit Derivatives) Directions, 2026 (25 Jun 2026, updated 22 Sep 2026)
F_FBA = F_MD + "12581"     # RBI (Financial Benchmark Administrators) Directions, 2023
F_ETP = F_MD + "12870"     # MD - RBI (Electronic Trading Platforms) Directions, 2025
F_GSL = F_MD + "12580"     # RBI (Government Securities Lending) Directions, 2023
F_FBIL = "https://www.rbi.org.in/scripts/BS_ViewMasCirculardetails.aspx?id=9923"   # RBI circular 2 Jul 2015 on FBIL
F_SEBI_MAR26 = "https://www.sebi.gov.in/sebi_data/attachdocs/mar-2026/1774268916433.pdf"   # PR 18/2026, 213th Board meeting
F_SEBI_SEP26 = "https://www.sebi.gov.in/sebi_data/attachdocs/sep-2026/1790259036651.pdf"   # PR, Board meeting 24 Sep 2026
F_NIFTY = "https://archives.nseindia.com/content/indices/ind_nifty50.pdf"   # Nifty 50 factsheet dated 30 Oct 2026
F_MFCAT = "https://www.sebi.gov.in/sebi_data/attachdocs/feb-2026/1772079826878.pdf"   # SEBI circular 26 Feb 2026, categorisation of MF schemes
F_AMFI_NAV = "https://www.amfiindia.com/investor/knowledge-center-info?zoneName=NetAssetValueNAV"   # AMFI NAV page

# ================= Financial Markets (Basic 2 / Intermediate 4 / Advanced 3)
T = "Financial Markets"
Q(T, "Structure and regulators", "Basic",
  "Financial Benchmarks India Pvt. Ltd (FBIL), the independent administrator of rupee interest rate and foreign "
  "exchange benchmarks recognised by RBI, was jointly floated by:",
  ["FIMMDA, FEDAI and the Indian Banks' Association", "RBI, SEBI and NSE", "CCIL, NSDL and the State Bank of India",
   "NABARD, SIDBI and EXIM Bank"],
  concept="Benchmark administration in Indian financial markets",
  explanation="On RBI's acceptance of a committee's recommendations, FBIL was set up as an independent company jointly "
              "floated by the Fixed Income Money Market and Derivatives Association (FIMMDA), the Foreign Exchange "
              "Dealers' Association of India (FEDAI) and the IBA. Its first benchmark, from 22 July 2015, was the "
              "'FBIL-Overnight MIBOR', which replaced the FIMMDA-NSE overnight rate.",
  steps=["Industry bodies of the money/debt market (FIMMDA), forex market (FEDAI) and banks (IBA) -> FBIL"],
  why="RBI and SEBI are regulators, not FBIL's promoters; CCIL is a clearing house (FBIL's calculation agent for some "
      "benchmarks), not an owner; NABARD, SIDBI and EXIM Bank are development finance institutions.",
  facts=[fact("FBIL, an independent company jointly floated by the FIMMDA, the FEDAI and the IBA ... The FBIL will act as "
              "an independent benchmark administrator.", F_FBIL)])

Q(T, "Structure and regulators", "Basic",
  "Under RBI's Unique Identifiers in Financial Markets Directions, 2026, the Legal Entity Identifier (LEI) that parties "
  "to a financial transaction must hold is a unique identity code of how many characters?",
  ["20", "12", "16", "52"],
  concept="Legal Entity Identifier (LEI)",
  explanation="The LEI is a 20-character code that identifies the parties to a financial transaction worldwide. Under "
              "RBI's directions, non-individual entities need an LEI to undertake OTC transactions in government "
              "securities, money market, foreign exchange and derivatives markets.",
  steps=["LEI = 20-character global code"],
  why="12 characters is the length of an ISIN; 16 is the length of a typical card number; 52 is the maximum length of "
      "the Unique Transaction Identifier (UTI) for OTC derivatives under the same directions.",
  facts=[fact("LEI code, a 20-character unique identity code assigned to entities who are parties to a financial "
              "transaction", F_UID)])

Q(T, "Structure and regulators", "Intermediate",
  "RBI's Unique Identifiers in Financial Markets Directions of March 2026 introduce a Unique Transaction Identifier "
  "(UTI) from 1 January 2027. Which description of the UTI is correct?",
  ["It identifies each OTC derivative transaction, has a maximum of 52 characters and begins with the LEI of the "
   "generating entity",
   "It identifies each UPI payment, has 12 digits and begins with the payer's bank IFSC",
   "It identifies each investor in mutual funds, has 10 characters and is the same as the PAN",
   "It identifies each government security, has 20 characters and is issued by CCIL"],
  concept="Identifiers in OTC markets: LEI and UTI",
  explanation="Section B of the 2026 directions, effective 1 January 2027, requires a Unique Transaction Identifier for "
              "OTC derivative transactions. It can be up to 52 characters long and is formed from the LEI of the "
              "entity generating it followed by a unique identifier, so that each trade can be traced in trade "
              "repositories.",
  steps=["UTI = transaction-level identifier for OTC derivatives", "Structure: LEI of generating entity + unique code",
         "Max 52 characters; effective 1 January 2027"],
  why="UPI transaction references, PAN-based investor identity and ISINs of securities are other identifiers; none is "
      "the UTI defined by these directions.",
  current=ca("2026-03-27"),
  facts=[fact("It shall have a maximum of 52 characters comprising the LEI of the generating entity followed by a unique "
              "identifier", F_UID),
         fact("Section B (UTI) shall come into effect from January 01, 2027.", F_UID)])

Q(T, "Structure and regulators", "Intermediate",
  "RBI issued new Credit Derivatives Directions in June 2026, replacing the 2022 directions. What did they mainly "
  "introduce?",
  ["Derivatives on credit indices and total return swaps on corporate bonds",
   "Credit default swaps on government securities and State Development Loans",
   "Permission for market-makers to sell credit default swaps to individuals",
   "Credit derivatives on asset-backed and mortgage-backed securities"],
  concept="Credit derivatives market in India",
  explanation="The Credit Derivatives Directions, 2026 (in force from 25 June 2026) allow market-makers and users to "
              "deal in CDS and total return swaps (TRS); their stated purpose is the introduction of derivatives on "
              "credit indices and TRS on corporate bonds. Reference obligations are money market debt instruments and "
              "rated (and certain unrated infrastructure SPV) INR corporate bonds.",
  steps=["2026 Directions -> CDS + TRS", "New: credit-index derivatives and TRS on corporate bonds"],
  why="G-secs and SDLs are not eligible reference obligations; market-makers may not offer CDS to individuals; ABS/MBS "
      "are expressly excluded.",
  current=ca("2026-06-25"),
  facts=[fact("Please refer to Paragraph 13 of the Statement on Developmental and Regulatory Policies regarding the "
              "introduction of derivatives on credit indices and total return swaps on corporate bonds.", F_CDS),
         fact("These Directions shall come into force on June 25, 2026. Market-makers and users may undertake "
              "transactions in CDS and TRS contracts.", F_CDS)])

Q(T, "Structure and regulators", "Intermediate",
  "Under RBI's Government Securities Lending (GSL) Directions, 2023, which statement about Treasury Bills is correct?",
  ["T-bills cannot be lent under GSL, but may be placed as collateral in a GSL transaction",
   "T-bills are the only securities that can be lent under GSL",
   "T-bills can be lent under GSL, but cannot be placed as collateral",
   "T-bills can neither be lent nor placed as collateral under GSL"],
  concept="Securities lending in the G-sec market",
  explanation="In a GSL transaction the owner lends eligible government securities to a borrower for a fee against "
              "other government securities as collateral. Central Government securities excluding T-bills are "
              "eligible for lending, whereas the collateral may be Central Government securities including T-bills, "
              "or State Government securities. The minimum tenor is one day.",
  steps=["Lendable: Central G-secs excluding T-bills", "Collateral: Central G-secs including T-bills, and SGSs"],
  why="Each wrong option reverses or misstates the two rules: T-bills are excluded from lending but allowed as "
      "collateral.",
  facts=[fact("Government securities issued by the Central Government excluding Treasury Bills shall be eligible for "
              "lending under a GSL transaction.", F_GSL),
         fact("Central Government securities (including Treasury Bills) and State Government securities can be placed "
              "as collateral. The minimum tenor of a GSL transaction shall be one day.", F_GSL)])

Q(T, "Structure and regulators", "Intermediate",
  "Under RBI's Electronic Trading Platforms (ETP) Directions, 2025, which of the following is an eligibility "
  "requirement for an entity seeking authorisation to operate an ETP?",
  ["A company incorporated in India with a minimum net worth of ₹5 crore, maintained at all times",
   "A recognised stock exchange with a minimum net worth of ₹100 crore",
   "A scheduled commercial bank with a minimum net worth of ₹500 crore",
   "Any foreign entity registered with IOSCO, with no net worth requirement"],
  concept="Regulation of electronic trading platforms by RBI",
  explanation="An ETP is any electronic system, other than a recognised stock exchange, on which securities, money "
              "market instruments, forex instruments or derivatives are traded. To operate one, an entity must be a "
              "company incorporated in India, keep a minimum net worth of ₹5 crore at all times, and it (or at least two "
              "key managerial persons) must have at least three years' experience of operating trading infrastructure "
              "in financial markets.",
  steps=["Form: company incorporated in India", "Net worth: ₹5 crore, at all times", "Experience: 3 years"],
  why="Recognised stock exchanges are outside the ETP definition; banks' own systems are a separate exemption and no "
      "₹500 crore rule exists; foreign entities without incorporation in India are not eligible.",
  facts=[fact("ETP means any electronic system, other than a recognised stock exchange, on which transactions in "
              "eligible instruments are contracted.", F_ETP),
         fact("The entity shall be a company incorporated in India ... minimum net-worth of ₹5 crore (Rupees five crore "
              "only) ... maintained at all times.", F_ETP)])

Q(T, "Structure and regulators", "Advanced",
  "Under RBI's Credit Derivatives Directions, 2026, which of the following entities is NOT eligible to act as a "
  "market-maker in credit derivatives?",
  ["A small finance bank", "An NBFC in the Middle Layer", "A standalone primary dealer",
   "NaBFID (National Bank for Financing Infrastructure and Development)"],
  concept="Market-makers in credit derivatives",
  explanation="Eligible market-makers are scheduled commercial banks other than small finance banks, payments banks, "
              "local area banks and RRBs; standalone primary dealers; NBFCs in the Upper and Middle Layers (including "
              "HFCs); and EXIM Bank, NABARD, NHB, SIDBI and NaBFID. A small finance bank is expressly excluded.",
  steps=["SCBs eligible except SFBs, PBs, LABs, RRBs", "SPDs, NBFC-UL/ML and the AIFIs including NaBFID eligible",
         "Hence the SFB is not eligible"],
  why="Middle Layer NBFCs, standalone PDs and NaBFID are all listed as eligible market-makers.",
  current=ca("2026-06-25"),
  facts=[fact("The following entities shall be eligible to act as market-makers in credit derivatives: (a) Scheduled "
              "Commercial Banks, except Small Finance Banks, Payment Banks, Local Area Banks and Regional Rural Banks; "
              "... (c) NBFCs – Upper Layer and NBFCs – Middle Layer (including Housing Financial Companies)", F_CDS),
         fact("Market-makers include standalone primary dealers ... and EXIM, NABARD, NHB, SIDBI and NaBFID.", F_CDS)])

hold_face, wanted = 40, 50
net_worth, turnover = 400, 900
is_retail = not (net_worth >= 500 or turnover >= 1000)
max_cover = min(wanted, hold_face)
assert is_retail and max_cover == 40
Q(T, "Structure and regulators", "Advanced",
  f"A resident company with a net worth of ₹{net_worth} crore and turnover of ₹{turnover} crore (latest audited) holds "
  f"₹{hold_face} crore face value of a rated corporate bond. It approaches a bank to buy CDS protection of "
  f"₹{wanted} crore on that bond. Under RBI's Credit Derivatives Directions, 2026, what is the position?",
  [f"It is a retail user; it may buy protection only to hedge, for a notional of at most ₹{max_cover} crore",
   f"It is a non-retail user; it may buy the full ₹{wanted} crore of protection for any purpose",
   f"It is a retail user; it may buy the full ₹{wanted} crore as long as it holds the bond",
   "It is a retail user and is not allowed to buy CDS protection at all"],
  concept="Retail and non-retail users of credit derivatives",
  explanation="A resident company is non-retail only if its net worth is at least ₹500 crore or its turnover at least "
              "₹1,000 crore; this company meets neither, so it is a retail user. A non-individual retail user may buy "
              "protection only for hedging; it must have exposure to the reference asset, and the notional cannot "
              f"exceed the face value of the reference obligation held, i.e. ₹{max_cover} crore.",
  steps=[f"₹{net_worth} cr < ₹500 cr and ₹{turnover} cr < ₹1,000 cr -> retail",
         "Retail (non-individual): hedging only", f"Notional cap = face value held = ₹{max_cover} crore"],
  why="It fails both non-retail thresholds; even a hedger cannot buy notional above the face value it holds; retail "
      "users other than individuals are allowed to buy protection for hedging.",
  computed=True, current=ca("2026-06-25"),
  facts=[fact("Resident companies with (a) minimum net worth of ₹500 crore; or (b) minimum turnover of ₹1,000 crore, as "
              "per the latest audited financial statements ... Any user who is not eligible to be classified as a "
              "non-retail user shall be classified as a retail user.", F_CDS),
         fact("A resident retail user, other than an individual, shall be allowed to buy protection only for the purpose "
              "of hedging ... shall not buy a credit derivative contract(s) with notional amount higher than the face "
              "value of the reference obligation", F_CDS)])

Q(T, "Structure and regulators", "Advanced",
  "Consider the following statements based on RBI's market directions: "
  "I. Under the Financial Benchmark Administrators Directions, 2023, an administrator of a 'significant benchmark' must "
  "maintain a minimum net worth of ₹5 crore, against ₹1 crore for other benchmarks. "
  "II. Under the Unique Identifiers Directions, 2026, the LEI requirement for non-derivative foreign exchange "
  "transactions applies only to transactions of USD one million or more. "
  "III. Under the Financial Benchmark Administrators Directions, 2023, the methodology of a non-significant benchmark "
  "need be reviewed only once every three years. "
  "Which of the above is/are correct?",
  ["I and II only", "I, II and III", "II and III only", "I only"],
  concept="Benchmark administrators and LEI thresholds",
  explanation="FBAs must be companies incorporated in India with net worth of ₹5 crore (significant benchmark) or ₹1 "
              "crore (non-significant), maintained at all times. For non-derivative forex, the LEI applies to "
              "transactions of USD 1 million or more. Statement III is wrong: a non-significant benchmark's "
              "methodology must be reviewed at least once a year.",
  steps=["I: ₹5 cr / ₹1 cr -> correct", "II: USD 1 million threshold -> correct",
         "III: review at least once a year, not three years -> wrong"],
  why="Any option including III is wrong; 'I only' omits the correct statement II.",
  facts=[fact("Minimum net-worth of ₹5 crore for an FBA administering a significant benchmark and ₹1 crore for a "
              "non-significant benchmark ... at all times. The methodology [of a non-significant benchmark] shall be "
              "reviewed at least once in a year.", F_FBA),
         fact("the LEI code shall be applicable only for transactions involving an amount equivalent to or exceeding USD "
              "one million", F_UID)])

# ================= Money Market (Basic 1 / Intermediate 2 / Advanced 2)
T = "Money Market"
Q(T, "Instruments: T-bills, CP, CD, call money", "Basic",
  "Under RBI's Certificate of Deposit Directions, 2021, can a bank grant a loan against the security of a Certificate "
  "of Deposit (CD)?",
  ["No, unless specifically permitted by the Reserve Bank",
   "Yes, up to 75% of the face value of the CD",
   "Yes, but only against CDs issued by itself",
   "Yes, freely, as CDs are negotiable instruments"],
  concept="Certificates of Deposit",
  explanation="A CD is a negotiable money market instrument issued in demat form against funds deposited with a bank. "
              "Unlike ordinary term deposits, banks are not allowed to grant loans against CDs unless RBI specifically "
              "permits it; an issuer may, however, buy back its CDs before maturity, but only after seven days from "
              "issue.",
  steps=["Loans against CDs: not allowed, save with RBI's specific permission"],
  why="There is no 75% margin rule for CDs; loans against own CDs are equally barred; negotiability allows transfer, "
      "not loans against CDs.",
  facts=[fact("Banks are not allowed to grant loans against CDs, unless specifically permitted by the Reserve Bank",
              F_CD)])

Q(T, "Instruments: T-bills, CP, CD, call money", "Intermediate",
  "RBI's 2024 directions on Commercial Paper also cover Non-Convertible Debentures (NCDs) of original maturity up to "
  "one year. How are such NCDs described, and what tenor is permitted?",
  ["A secured instrument, with a tenor of 90 days to one year",
   "An unsecured instrument, with a tenor of 7 days to one year",
   "A secured instrument, with a tenor of 7 days to 90 days",
   "An unsecured instrument, with a tenor of one year to three years"],
  concept="Short-term NCDs vs Commercial Paper",
  explanation="Under the 2024 directions an NCD is a secured money market instrument with original or initial maturity "
              "up to one year, issued for 90 days to one year. CP, in contrast, is an unsecured promissory note issued "
              "for 7 days to one year. Both are issued in demat form in minimum denominations of ₹5 lakh.",
  steps=["NCD (up to 1 year) = secured", "Tenor: 90 days to 1 year (CP: 7 days to 1 year)"],
  why="7 days to one year is the CP tenor and CP is unsecured; 7-90 days and 1-3 years are not the NCD range.",
  facts=[fact("NCD means a secured money market instrument with an original or initial maturity upto one year.", F_CP),
         fact("CPs run from 7 days to 1 year; NCDs run from 90 days to 1 year.", F_CP)])

Q(T, "Instruments: T-bills, CP, CD, call money", "Intermediate",
  "Which of the following is permitted under RBI's Commercial Paper and short-term NCD Directions, 2024?",
  ["Issuing CP with a credit rating of A3 or above",
   "Issuing CP with a call option exercisable after 30 days",
   "Underwriting of a CP issue by a bank",
   "Issuing CP in physical form to retail investors"],
  concept="Features of Commercial Paper",
  explanation="CP must carry a minimum credit rating of A3 (SEBI's symbol and definition) and must be issued in "
              "dematerialised form. Issuing CP or NCDs with call/put options is not permitted, nor are underwriting "
              "and co-acceptance.",
  steps=["Minimum rating: A3 -> permitted", "Options, underwriting, physical form -> not permitted"],
  why="Call/put options are prohibited; underwriting and co-acceptance are prohibited; CPs must be issued in demat "
      "form only.",
  facts=[fact("The minimum credit rating of the CP shall be A3 as per rating symbol and definition prescribed by SEBI. "
              "Issuance of a CP/NCD with options (call/put) is not permitted.", F_CP),
         fact("CPs and NCDs shall be issued in dematerialised form and held with a depository registered with SEBI. "
              "Underwriting and co-acceptance are not permitted.", F_CP)])

Q(T, "Instruments: T-bills, CP, CD, call money", "Advanced",
  "A company issued a 91-day Commercial Paper on 1 September 2026. Its cash position improves and it wants to buy back "
  "the CP from investors on 5 September 2026. Under RBI's CP Directions, 2024, which statement is correct?",
  ["It cannot buy back on 5 September, as a CP may be bought back only after 7 days from issue; any later buyback "
   "must be offered to all investors on identical terms at the prevailing market price, and the CP extinguished",
   "It can buy back on 5 September from any investors it chooses, at par value",
   "It cannot buy back the CP at all before maturity",
   "It can buy back on 5 September only with SEBI's prior approval, and may resell the CP later"],
  concept="Buyback of Commercial Paper",
  explanation="An issuer may buy back CP before maturity only after seven days from issue (NCDs only after 90 days). The "
              "offer must be made to all investors in that issue on identical terms, at the prevailing market price, "
              "and the bought-back CP is extinguished on the buyback date. 5 September is only four days after issue, "
              "so the buyback is not allowed then.",
  steps=["Issue 1 Sep -> 5 Sep is 4 days later (< 7 days)", "Not permitted yet",
         "Later buyback: all investors, identical terms, market price, extinguished"],
  why="Selective buyback at par is not allowed; buyback is permitted after 7 days, not barred entirely; SEBI approval "
      "and resale of bought-back CP have no basis, as the CP must be extinguished.",
  facts=[fact("CPs can be bought back only after 7 days from issue, and NCDs only after 90 days. The offer must go to all "
              "investors on identical terms, at the prevailing market price. Bought-back instruments are extinguished "
              "on the buyback date.", F_CP)])

fv_cr, days, y = 25, 182, 0.073
price = 100 / (1 + y * days / 365)
units = fv_cr * 10**7 // (5 * 10**5)
alt_disc = 100 * (1 - y * days / 365)
alt_year = 100 / (1 + y)
assert round(price, 2) == 96.49 and units == 500
assert round(alt_disc, 2) == 96.36 and round(alt_year, 2) == 93.2
Q(T, "Instruments: T-bills, CP, CD, call money", "Advanced",
  f"A bank issues a {days}-day Certificate of Deposit of face value ₹{fv_cr} crore at a discount, priced to give a "
  f"yield of {y*100:.2f}% (Actual/365). What is the issue price per ₹100 of face value, and into how many units of the "
  "minimum denomination allowed by RBI's CD Directions can the issue be divided?",
  [f"₹{price:.2f}; {units} units", f"₹{alt_disc:.2f}; {units} units", f"₹{price:.2f}; 2,500 units",
   f"₹{alt_year:.2f}; {units} units"],
  concept="Pricing of discounted money market instruments",
  explanation=f"Price = 100 / (1 + yield × days/365) = 100 / (1 + 0.073 × {days}/365) ≈ ₹{price:.2f}. CDs are issued in "
              f"a minimum denomination of ₹5 lakh and multiples thereof, so ₹{fv_cr} crore = {units} units of ₹5 lakh.",
  steps=[f"0.073 × {days}/365 = {y*days/365:.5f}", f"100 / {1 + y*days/365:.5f} = {price:.2f}",
         f"₹{fv_cr} crore / ₹5 lakh = {units}"],
  why=f"₹{alt_disc:.2f} treats 7.30% as a discount rate on face value, not a yield; 2,500 units assumes a ₹1 lakh "
      f"denomination; ₹{alt_year:.2f} discounts for a full year instead of {days} days.",
  computed=True,
  facts=[fact("CDs shall be issued in minimum denomination of ₹5 lakh and in multiples of ₹5 lakh thereafter.", F_CD),
         fact("CDs may be issued at a discount to face value or on a fixed or floating rate basis; banks may issue CDs "
              "for a minimum of seven days and up to one year.", F_CD)])

# ================= Capital Market (Basic 2 / Intermediate 4 / Advanced 1)
T = "Capital Market"
Q(T, "Indices", "Basic",
  "According to NSE Indices' factsheet of 30 October 2026, which sector has the highest weight in the Nifty 50?",
  ["Financial Services", "Information Technology", "Oil, Gas & Consumable Fuels", "Fast Moving Consumer Goods"],
  concept="Sectoral composition of the Nifty 50",
  explanation="Financial Services made up 37.13% of the Nifty 50, far ahead of Oil, Gas & Consumable Fuels (9.00%) and "
              "Information Technology (8.80%). The two largest constituents were HDFC Bank (9.95%) and ICICI Bank "
              "(9.39%).",
  steps=["Financial Services 37.13% > Oil & Gas 9.00% > IT 8.80% > ... FMCG 5.36%"],
  why="Oil & Gas, IT and FMCG each have under 10% weight.",
  current=ca("2026-10-30"),
  facts=[fact("Sector Weight(%): Financial Services 37.13; Oil, Gas & Consumable Fuels 9.00; Information Technology 8.80; "
              "Fast Moving Consumer Goods 5.36", F_NIFTY)])

Q(T, "SEBI", "Basic",
  "On 24 September 2026, SEBI's Board approved an enabling provision for issuing Depository Receipts (DRs) on units of "
  "REITs and InvITs. Where does the framework envisage such DRs being issued and listed to begin with?",
  ["In the International Financial Services Centre (IFSC) in India",
   "On the SME platforms of NSE and BSE",
   "Only on stock exchanges in the United States",
   "On the Social Stock Exchange"],
  concept="Foreign capital for REITs and InvITs",
  explanation="To attract foreign capital to REITs and InvITs, SEBI approved amendments enabling DRs on their units. The "
              "framework envisages issue and listing of these DRs in the IFSC in India (GIFT City) to begin with, and "
              "all foreign investors, including NRIs, can invest in them.",
  steps=["DRs on REIT/InvIT units -> IFSC in India first"],
  why="DRs are aimed at foreign investors, so domestic SME platforms and the Social Stock Exchange do not fit; the "
      "framework starts in India's IFSC, not on US exchanges.",
  current=ca("2026-09-24"),
  facts=[fact("The framework envisages issuance and listing of DRs on units of REITs and InvITs in the International "
              "Financial Services Centre (IFSC) in India to begin with. Further, all foreign investors (including NRIs) "
              "can invest in such DRs.", F_SEBI_SEP26)])

Q(T, "Indices", "Intermediate",
  "Under the eligibility criteria in NSE Indices' Nifty 50 factsheet (October 2026), which require F&O eligibility, a "
  "minimum listing history and an impact-cost test, which of these companies can be considered for inclusion?",
  ["P: in the F&O segment, listed 2 months, average impact cost 0.40% for 92% of observations (basket ₹10 crore)",
   "Q: in the F&O segment, listed 3 weeks, average impact cost 0.30% for 95% of observations (basket ₹10 crore)",
   "R: not in the F&O segment, listed 5 years, average impact cost 0.20% for 99% of observations (basket ₹10 crore)",
   "S: in the F&O segment, listed 4 years, average impact cost 0.70% for 90% of observations (basket ₹10 crore)"],
  concept="Liquidity and eligibility screens for the Nifty 50",
  explanation="To qualify, a stock must have traded at an average impact cost of 0.50% or less for 90% of observations "
              "over six months for a basket of ₹100 million (₹10 crore), be allowed in the F&O segment, and have a "
              "listing history of at least one month at the cut-off date. Only P meets all three.",
  steps=["Q: listing 3 weeks < 1 month -> out", "R: not in F&O -> out", "S: impact cost 0.70% > 0.50% -> out",
         "P meets all -> eligible"],
  why="Q fails the one-month listing rule, R fails the F&O rule, and S fails the impact-cost rule.",
  facts=[fact("For a stock to qualify for possible inclusion into the Nifty50, have traded at an average impact cost of "
              "0.50% or less during the last six months for 90% of the observations, for the basket size of Rs. 100 "
              "Million.", F_NIFTY),
         fact("Companies that are allowed to trade in F&O segment are only eligible to be constituent of the index. The "
              "Company should have a minimum listing history of 1 month as on the cutoff date.", F_NIFTY)])

Q(T, "SEBI", "Intermediate",
  "On 23 March 2026, SEBI's Board approved recommendations of the High-Level Committee on conflict of interest of its "
  "own Members and officials. Which of the following was among them?",
  ["The Chairman and Whole-Time Members are to be brought within the definition of 'insider', and new investments by "
   "officials in products of a single intermediary may not exceed 25% of their financial portfolio",
   "Part-time Members of the Board must publicly disclose all their assets and liabilities every year",
   "SEBI officials are barred from investing in mutual funds and all other pooled vehicles",
   "The Chairman and Whole-Time Members must liquidate only their unlisted investments before joining"],
  concept="Conflict-of-interest framework within SEBI",
  explanation="The Board approved bringing the Chairman and WTMs within the definition of 'insider', applying "
              "employees' trading restrictions to them, and a 25% cap on new investments by employees/WTMs/Chairman in "
              "products managed by a single SEBI-registered intermediary (with recusal if breached). Investments in "
              "regulated pooled vehicles remain allowed, and no public disclosure is required for Part-Time Members.",
  steps=["Chairman/WTMs -> 'insider'", "Single-intermediary cap: 25% of financial portfolio"],
  why="No public disclosure is required of Part-Time Members; investments in mutual funds and professionally managed "
      "pooled vehicles are permitted; listed and unlisted equity holdings at joining must be liquidated, frozen or sold "
      "under the chosen option, not only unlisted ones.",
  current=ca("2026-03-23"),
  facts=[fact("Chairman and WTMs to be brought within the definition of \"insider\".", F_SEBI_MAR26),
         fact("New investments by employees / WTMs / Chairman in products managed by a single SEBI-registered "
              "intermediary may not exceed 25% of their financial portfolio.", F_SEBI_MAR26)])

Q(T, "Primary and secondary market", "Intermediate",
  "In September 2026 SEBI's Board amended Regulation 62A of the LODR Regulations for issuers listing non-convertible "
  "debentures (NCDs) for the first time. What changed?",
  ["Such an issuer need no longer list all its outstanding unlisted NCDs; only prospective NCD issuances must be listed",
   "Such an issuer must now list all its outstanding unlisted NCDs within one month instead of three",
   "All unlisted NCDs issued since 2015 must now be listed within three months",
   "NCDs may no longer be issued on a private placement basis by listed entities"],
  concept="Listing of debt securities",
  explanation="Earlier, an entity proposing to list an NCD had to list all its outstanding unlisted NCDs issued on or "
              "after 1 January 2024 within three months of the new listing. SEBI removed this to ease costs (ISIN "
              "limits, covenant monitoring): the entity now has to list only prospective issuances, which should "
              "encourage new issuers to list debt.",
  steps=["Old: list all outstanding unlisted NCDs (issued on/after 1 Jan 2024) within 3 months",
         "New: only prospective issuances need listing"],
  why="The other options tighten rather than relax the rule, or describe changes that were not made.",
  current=ca("2026-09-24"),
  facts=[fact("to do away with the requirement for mandatory listing of all outstanding unlisted non-convertible debt "
              "securities (\"NCD\") by an issuer who proposes to list its NCD for the first time.", F_SEBI_SEP26),
         fact("The amendment provides that an entity shall be required to list only prospective issuances of "
              "non-convertible debt securities.", F_SEBI_SEP26)])

Q(T, "Primary and secondary market", "Intermediate",
  "SEBI's Board on 24 September 2026 allowed FPIs to participate in non-cash settled, non-agricultural commodity "
  "derivatives contracts. What safeguard applies?",
  ["FPIs must exit their positions before the Tender Period (three days before expiry) and cannot increase positions "
   "from T-3",
   "FPIs must take delivery of the commodity on expiry of every contract",
   "FPIs can trade only through the IFSC exchanges and must settle in US dollars",
   "FPIs must hold at least 50% of their positions until expiry"],
  concept="FPIs in exchange-traded commodity derivatives",
  explanation="FPIs may now trade non-agricultural index derivatives and non-cash-settled non-agricultural commodity "
              "derivatives, but must exit before a delivery obligation can arise, i.e. before the Tender Period that "
              "starts three days before expiry; they cannot increase positions from T-3. Residual open positions are "
              "devolved on the trading member/clearing member under a prior agreement.",
  steps=["Allowed: non-cash settled non-agri contracts", "Safeguard: exit before Tender Period (T-3)",
         "No increase in positions from T-3"],
  why="The whole point is to avoid delivery by FPIs; trading is on Indian commodity exchanges, not only IFSC; there is "
      "no minimum holding rule.",
  current=ca("2026-09-24"),
  facts=[fact("a safeguard mechanism is proposed to ensure that FPIs exit their positions before entering the Tender "
              "Period, i.e. three (3) days before the expiry of the contract ... FPIs shall not be permitted to increase "
              "their positions from T-3 day.", F_SEBI_SEP26)])

sa = lambda n: 144000 if n <= 5 else (288000 if n <= 50 else 720000 + 14400 * n)
p_, q_, r_ = 4, 50, 75
total = sa(p_) + sa(q_) + sa(r_)
assert sa(51) == 1454400 and sa(r_) == 1800000 and total == 2232000
assert 144000 + 288000 + 720000 + 25 * 14400 == 1512000 and 144000 + (720000 + 50 * 14400) + 1800000 == 3384000
assert 288000 + 288000 + 1800000 == 2376000
Q(T, "SEBI", "Advanced",
  "Under SEBI's Settlement Scheme, 2026 for non-genuine trades in illiquid stock options on BSE, the settlement amount "
  "is ₹1,44,000 for 1-5 contracts, ₹2,88,000 for 6-50 contracts, and, for 51 contracts and above, ₹7,20,000 plus "
  "₹14,400 multiplied by the total number of contracts traded (not just those above 50). Entities P, Q and R traded "
  f"{p_}, {q_} and {r_} contracts respectively. What is the total settlement amount payable by the three?",
  ["₹22,32,000", "₹15,12,000", "₹33,84,000", "₹23,76,000"],
  concept="Settlement schemes under the SEBI Act",
  explanation=f"P ({p_} contracts) pays ₹1,44,000; Q ({q_} contracts, still within 6-50) pays ₹2,88,000; R ({r_} "
              f"contracts) pays ₹7,20,000 + {r_} × ₹14,400 = ₹18,00,000. Total = ₹22,32,000. This fourth scheme, "
              "under Section 15JB of the SEBI Act, follows schemes of 2020, 2022 and 2024 for trades on BSE between "
              "1 April 2014 and 30 September 2015.",
  steps=["P: ₹1,44,000", "Q: 50 contracts -> ₹2,88,000", f"R: 7,20,000 + {r_}×14,400 = ₹18,00,000",
         "Total = ₹22,32,000"],
  why="₹15,12,000 charges R only for the 25 contracts above 50; ₹33,84,000 wrongly puts Q (50 contracts) in the top "
      "slab (₹14,40,000); ₹23,76,000 wrongly puts P (4 contracts) in the 6-50 slab.",
  computed=True, current=ca("2026-09-24"),
  facts=[fact("Settlement Amount: 01-05 contracts ₹1,44,000; 06-50 ₹2,88,000; 51 and above ₹7,20,000 + ₹14,400 per "
              "contract. E.g. for 51 contracts, the SA would be ₹14,54,400", F_SEBI_SEP26),
         fact("SEBI has decided to introduce a fourth (4th) Settlement Scheme ... under Section 15JB of the SEBI Act, "
              "1992 ... for dealing with the matter of trading activities of certain entities in ISOs on Bombay Stock "
              "Exchange (BSE).", F_SEBI_SEP26)])

# ================= Mutual Funds (Basic 1 / Intermediate 2 / Advanced 2)
T = "Mutual Funds"
Q(T, "Types", "Basic",
  "Under SEBI's circular of 26 February 2026 on categorisation of mutual fund schemes, which scheme category was "
  "discontinued, with existing schemes stopping all subscriptions immediately?",
  ["Solution Oriented Schemes", "Arbitrage Funds", "Fund of Funds", "Equity Savings Funds"],
  concept="Categorisation and rationalisation of mutual fund schemes",
  explanation="The 2026 circular re-grouped schemes into Equity, Debt, Hybrid, Life Cycle Funds and Other schemes "
              "(FoFs and passive schemes). The Solution Oriented category (retirement and children's funds) was "
              "discontinued; existing schemes had to stop subscriptions at once and be merged with similar schemes "
              "with SEBI's approval.",
  steps=["Feb 2026 circular -> Solution Oriented category discontinued", "New group added: Life Cycle Funds"],
  why="Arbitrage and Equity Savings remain hybrid categories, and FoFs remain under 'Other Schemes'.",
  current=ca("2026-02-26"),
  facts=[fact("Solutions oriented scheme category is being discontinued w.e.f the date of the circular. Existing schemes "
              "in this category shall stop all subscriptions with immediate effect.", F_MFCAT)])

Q(T, "Types", "Intermediate",
  "Under SEBI's revised scheme categories of February 2026, what are the investment requirements of a Multi Cap Fund?",
  ["At least 75% in equity, with at least 25% each in large cap, mid cap and small cap companies",
   "At least 65% in equity across market caps, with no minimum for any one segment",
   "At least 80% in equity, of which at least 35% each in large cap and mid cap companies",
   "At least 65% in equity, with at least 25% each in large cap and mid cap companies only"],
  concept="Equity scheme categories",
  explanation="A Multi Cap Fund must invest at least 75% of total assets in equity, with minimums of 25% each in large, "
              "mid and small cap companies. The 65% equity floor with no segment minimum describes a Flexi Cap Fund, "
              "and 35% each in large and mid caps is the Large & Mid Cap Fund.",
  steps=["Multi Cap: 75% equity = 25% + 25% + 25%", "Flexi Cap: 65% dynamic", "Large & Mid Cap: 35% + 35%"],
  why="Option 2 is Flexi Cap; option 3 mixes in the Large & Mid Cap rule; option 4 drops the small cap minimum.",
  current=ca("2026-02-26"),
  facts=[fact("Multi Cap Fund: Minimum investment in equity & equity related instruments - 75% of total assets ... large "
              "cap companies - 25% ... mid cap companies - 25% ... small cap companies - 25% of total assets", F_MFCAT),
         fact("Flexi Cap Fund: Minimum Investment in equity & equity related instruments – 65% of total assets", F_MFCAT)])

Q(T, "AMFI", "Intermediate",
  "Under SEBI's February 2026 circular on categorisation of mutual fund schemes, what role does AMFI play in the "
  "launch of sectoral and thematic funds?",
  ["Mutual funds may launch sectoral/thematic funds only as per the list of sectors/themes published by AMFI, in "
   "consultation with SEBI, and updated half-yearly",
   "AMFI must individually approve each sectoral/thematic scheme before its NFO",
   "AMFI sets the maximum expense ratio of each sectoral/thematic scheme every quarter",
   "AMFI computes the portfolio overlap of each scheme and publishes it monthly"],
  concept="AMFI's role in scheme categorisation",
  explanation="To keep sectoral and thematic funds true to label, the circular requires mutual funds to launch them "
              "only from the list of sectors/themes that AMFI publishes and updates half-yearly in consultation with "
              "SEBI. Portfolio overlap is disclosed monthly by each AMC on its own website, not by AMFI.",
  steps=["Sector/theme list: AMFI, with SEBI, half-yearly", "Launch only within that list"],
  why="SEBI, not AMFI, approves schemes; expense limits are set by SEBI regulations; AMCs, not AMFI, disclose overlap.",
  current=ca("2026-02-26"),
  facts=[fact("Mutual Funds shall launch sectoral/thematic funds as per the list of sectors/themes as published and "
              "updated by AMFI in consultation with SEBI on half yearly basis.", F_MFCAT)])

wa = {"P": 20, "Q": 15, "R": 25, "S": 10, "T": 30}
wb = {"P": 10, "Q": 25, "R": 20, "U": 30, "V": 15}
assert sum(wa.values()) == 100 and sum(wb.values()) == 100
overlap = sum(min(wa[k], wb[k]) for k in wa if k in wb)
sum_a = sum(wa[k] for k in wa if k in wb)
sum_b = sum(wb[k] for k in wb if k in wa)
assert overlap == 45 and sum_a == 60 and sum_b == 55 and (sum_a + sum_b) / 2 == 57.5
Q(T, "Types", "Advanced",
  "A banking sectoral fund (Scheme A) holds stocks P 20%, Q 15%, R 25%, S 10% and T 30%. The same AMC's flexi cap fund "
  "(Scheme B) holds P 10%, Q 25%, R 20%, U 30% and V 15%. Using SEBI's portfolio overlap methodology of February 2026, "
  "what is the overlap, and does it meet the limit for sectoral/thematic schemes?",
  [f"{overlap}%, within the 50% limit", f"{sum_a}%, breaching the 50% limit", "57.5%, breaching the 50% limit",
   f"{sum_b}%, breaching the 50% limit"],
  concept="Portfolio overlap between schemes",
  explanation="Overlap is the sum, over common stocks only, of the lower of the two weights: P min(20,10) = 10, Q "
              "min(15,25) = 15, R min(25,20) = 20; S, T, U and V count zero. Total = 45%. A sectoral/thematic scheme "
              "may overlap no more than 50% with other equity schemes (except large cap schemes), so 45% is within the "
              "limit.",
  steps=["Common stocks: P, Q, R", "Minimums: 10 + 15 + 20 = 45%", "45% ≤ 50% -> compliant"],
  why=f"{sum_a}% adds Scheme A's weights of the common stocks, {sum_b}% adds Scheme B's, and 57.5% averages the two; "
      "the method takes the minimum weight of each common stock.",
  computed=True, current=ca("2026-02-26"),
  facts=[fact("For each common scrip, the minimum weightage between the two schemes shall be considered. The overall "
              "portfolio overlap between the two schemes shall be the sum of such minimum weightages of all common "
              "scrips", F_MFCAT),
         fact("no more than 50% of the schemes portfolios would overlap with other equity schemes in sectoral/thematic "
              "category and other equity schemes categories except for large cap scheme.", F_MFCAT)])

units_h, nav = 2000, 15
gross = units_h * nav
net = gross * (1 - 0.02)
assert gross == 30000 and net == 29400 and gross * 0.97 == 29100 and gross * 0.99 == 29700
Q(T, "NAV and SIP", "Advanced",
  f"Ravi invested in a Life Cycle Fund launched under SEBI's February 2026 framework and redeems all his "
  f"{units_h:,} units 18 months later, when the applicable NAV is ₹{nav}. Using Redemption Price = Applicable NAV × "
  "(1 − exit load), how much does he receive?",
  ["₹29,400", "₹29,100", "₹29,700", "₹30,000"],
  concept="Exit load and redemption price",
  explanation="Life Cycle Funds carry a mandatory exit load to instil discipline: 3% on exit within one year, 2% within "
              "the first two years and 1% within the first three years. At 18 months the 2% load applies: redemption "
              f"price = 15 × 0.98 = ₹14.70, and {units_h:,} × 14.70 = ₹29,400.",
  steps=["18 months -> second year -> 2% load", f"Gross = {units_h:,} × 15 = ₹{gross:,}",
         f"Net = ₹{gross:,} × 0.98 = ₹{int(net):,}"],
  why="₹29,100 applies the first-year 3% load; ₹29,700 applies the third-year 1% load; ₹30,000 ignores the exit load.",
  computed=True, current=ca("2026-02-26"),
  facts=[fact("an exit load of 3% would be chargeable on any exit by an investor within one year of investment; an exit "
              "load of 2% within first two years of investment and 1% in the first three years of investment.", F_MFCAT),
         fact("Redemption Price = Applicable NAV*(1- Exit Load, if any)", F_AMFI_NAV)])


# ######## section G
# ---- sources (group G), opened 2026-11-06
G_BUD = "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc202621776101.pdf"  # PIB summary of Union Budget 2026-27 (1 Feb 2026), incl. Macro-economic Framework / MTFP statements
G_ESD = "https://www.drishtiias.com/daily-updates/daily-news-analysis/economic-survey-2025-26"  # Economic Survey 2025-26 explainer (30 Jan 2026)
G_ESP = "https://theprint.in/economy/economic-survey-2025-26-the-top-10-takeaways-for-india/2839818"  # ThePrint: top 10 takeaways of Economic Survey 2025-26
G_ESBS = "https://www.business-standard.com/budget/news/eco-survey-maps-swadeshi-path-to-strategic-resilience-indispensability-126012901867_1.html"  # Business Standard (search result only)
G_IRAR = "https://deccanchronicle.com/business/life-insurance-penetration-further-falls-to-27-in-fy25-irdai-annual-report-1927344"  # IRDAI annual report 2024-25 (30 Dec 2025)
G_IRCM = "https://cafemutual.com/news/insurance/36646-insurance-penetration-stalls-at-37-again-density-rises-to-usd-97"  # Cafemutual on IRDAI annual report 2024-25
G_PRS = "https://prsindia.org/files/bills_acts/bills_parliament/2025/Summary_Insurance_Laws_A_2025.pdf"  # PRS Bill summary, Sabka Bima Sabki Raksha Bill, 2025
G_PMFBY = "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/aug/doc_9735_20260829_18493301.pdf"  # PIB backgrounder on PMFBY (29 Aug 2026)
G_APY = "https://financialservices.gov.in/atal-pension-yojana-apy"  # DFS scheme page: APY
G_PMMY = "https://financialservices.gov.in/pradhan-mantri-mudra-yojana-pmmy"  # DFS scheme page: PMMY
G_MUDRA = "https://ies.gov.in/arthapedia/concept/micro-units-development-refinance-agency-mudra-bank"  # IES Arthapedia: MUDRA Bank
G_VL = "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/jul/doc2026729936401.pdf"  # PIB backgrounder on PM Vidyalaxmi (29 Jul 2026)
G_NCGTC = "https://www.ncgtc.in/en/Background"  # NCGTC background page
SEARCH_ONLY.update({G_ESBS})

G_BD = ca("2026-02-01")    # Union Budget 2026-27 presented (PIB summary dated 1 February 2026)
G_ES = ca("2026-01-29")    # Economic Survey 2025-26 tabled on Thursday, 29 January 2026

# ================= Insurance (Basic 3 / Intermediate 1 / Advanced 1)
T = "Insurance"
Q(T, "Life and general insurance", "Basic",
  "According to IRDAI's Annual Report 2024-25, released in December 2025, what was India's overall insurance "
  "penetration (life and non-life together) in 2024-25?",
  ["3.7%, unchanged from 2023-24", "4.2%, a new peak", "2.7%, down from 2.8%", "7.3%, in line with the world average"],
  concept="Insurance penetration (premium as a share of GDP)",
  explanation="IRDAI's Annual Report 2024-25 put overall insurance penetration at 3.7% in 2024-25, the same as in "
              "2023-24. Life penetration alone slipped to 2.7% from 2.8%. Overall penetration had peaked at 4.2% in "
              "2021-22 and has since declined.",
  steps=["Overall penetration 2024-25 = 3.7%", "Same as 2023-24"],
  why="4.2% was the 2021-22 peak, not the 2024-25 level; 2.7% (down from 2.8%) is life penetration alone; 7.3% is "
      "far above India's level.",
  current=ca("2025-12-30"),
  facts=[fact("The overall insurance penetration (life and non-life) remained flat at 3.7 per cent as in 2023-24. "
              "Insurance penetration in India had peaked at 4.2 per cent during the pandemic in 2021-22 but has since "
              "declined. ... life insurance penetration which has declined to 2.7 per cent during 2024-25 from 2.8 per "
              "cent in the previous year", G_IRAR),
         fact("Overall, insurance penetration stood unchanged at 3.7% in 2024–25, the same level as in 2023–24", G_IRCM)])
Q(T, "Government insurance schemes", "Basic",
  "Under the Pradhan Mantri Fasal Bima Yojana (PMFBY), what is the maximum premium payable by farmers for Kharif and "
  "Rabi foodgrain and oilseed crops respectively?",
  ["2% and 1.5%", "1.5% and 2%", "5% and 2%", "2% and 5%"],
  concept="PMFBY premium structure",
  explanation="Farmers pay at most 2% for Kharif and 1.5% for Rabi foodgrain and oilseed crops, and at most 5% for "
              "commercial and horticultural crops. The rest of the premium is subsidised by the Centre and the "
              "States.",
  steps=["Kharif foodgrain/oilseeds: 2%", "Rabi foodgrain/oilseeds: 1.5%", "Commercial/horticultural: 5%"],
  why="1.5% and 2% reverses the seasons; 5% applies only to commercial and horticultural crops.",
  facts=[fact("Farmers pay a maximum premium of 2% for Kharif and 1.5% for Rabi foodgrain and oilseed crops. For "
              "commercial and horticultural crops, the maximum premium is 5%.", G_PMFBY)])
Q(T, "IRDAI", "Basic",
  "Under the Sabka Bima Sabki Raksha (Amendment of Insurance Laws) Bill, 2025, the category of 'insurance "
  "intermediaries' (which already included brokers, insurance consultants and third-party administrators) is "
  "broadened to also include:",
  ["Managing general agents and insurance repositories", "Banks and NBFCs acting as corporate agents",
   "Insurance surveyors and actuaries", "Reinsurers and foreign reinsurance branches"],
  concept="Insurance intermediaries and IRDAI's oversight",
  explanation="The Bill, introduced in Lok Sabha on 16 December 2025, broadens insurance intermediaries to include "
              "managing general agents and insurance repositories, and extends IRDAI's powers of inspection and "
              "investigation to intermediaries.",
  steps=["Existing: brokers, consultants, TPAs", "Added: managing general agents, insurance repositories"],
  why="The other groups are not the additions named in the Bill; reinsurers are insurers, not intermediaries.",
  current=ca("2025-12-16"),
  facts=[fact("Under the Act, intermediaries include brokers, insurance consultants, and third-party administrators. "
              "The Bill broadens this to also include managing general agents and insurance repositories.", G_PRS)])
Q(T, "Life and general insurance", "Intermediate",
  "What change does the Sabka Bima Sabki Raksha (Amendment of Insurance Laws) Bill, 2025 make for insurance "
  "co-operative societies?",
  ["It removes the requirement of a minimum paid-up share capital of ₹100 crore for life, general and health "
   "insurance business",
   "It raises their minimum paid-up share capital from ₹100 crore to ₹500 crore",
   "It allows them 100% foreign direct investment through the automatic route",
   "It bars them from health insurance business"],
  concept="Entry norms for insurers",
  explanation="The Bill amends the definition of an insurance co-operative society to remove the requirement of a "
              "minimum paid-up share capital of ₹100 crore for life, general and health insurance businesses, easing "
              "entry for co-operatives.",
  steps=["Earlier: ₹100 crore minimum paid-up capital", "Bill: requirement removed"],
  why="The Bill lowers, not raises, the entry bar; 100% FDI relates to Indian insurance companies; nothing bars health "
      "insurance.",
  current=ca("2025-12-16"),
  facts=[fact("The Bill amends the definition of an insurance co-operative society to remove the requirement of "
              "minimum paid-up share capital of Rs 100 crore for life, general, and health insurance businesses.",
              G_PRS)])

si, act_rate = 80000, 9
total_prem = si * act_rate / 100
farmer = si * 2 / 100
subsidy = total_prem - farmer
centre, state = subsidy * 0.9, subsidy * 0.1
assert (total_prem, farmer, centre, state) == (7200, 1600, 5040, 560)
assert subsidy / 2 == 2800
Q(T, "Government insurance schemes", "Advanced",
  "A farmer in Assam insures her Kharif paddy under PMFBY for a sum insured of ₹80,000. The actuarial premium rate "
  "for the crop is 9%. How is the premium shared among the farmer, the Centre and the State?",
  ["Farmer ₹1,600; Centre ₹5,040; State ₹560", "Farmer ₹1,600; Centre ₹2,800; State ₹2,800",
   "Farmer ₹1,200; Centre ₹5,400; State ₹600", "Farmer ₹4,000; Centre ₹2,880; State ₹320"],
  concept="PMFBY premium subsidy sharing",
  explanation="Total premium = 9% × 80,000 = ₹7,200. The farmer pays the Kharif cap of 2% = ₹1,600. The balance "
              "₹5,600 is subsidised; for North-Eastern and Himalayan States the Centre and State share it 90:10, so "
              "the Centre pays ₹5,040 and Assam ₹560.",
  steps=["Total premium = ₹7,200", "Farmer: 2% × 80,000 = ₹1,600", "Subsidy = ₹5,600",
         "Centre 90% = ₹5,040; State 10% = ₹560"],
  why="50:50 sharing (₹2,800 each) applies to other States; 1.5% is the Rabi cap; 5% is for commercial and "
      "horticultural crops.",
  computed=True,
  facts=[fact("Farmers pay a maximum premium of 2% for Kharif and 1.5% for Rabi foodgrain and oilseed crops. The "
              "Central & State Governments subsidizes the remaining premium in 50:50 proportion. For the farmers in "
              "North-Eastern & Himalayan States/UTs, the contribution of Central & State Govt. subsidy is in a 90:10 "
              "proportion.", G_PMFBY)])

# ================= Budget and Economic Survey (Basic 4 / Intermediate 3 / Advanced 4)
T = "Budget and Economic Survey"
Q(T, "Union Budget highlights", "Basic",
  "To produce equipment and materials, design full-stack Indian IP and fortify supply chains, the Union Budget "
  "2026-27 proposed to launch:",
  ["India Semiconductor Mission (ISM) 2.0", "National Quantum Mission 2.0", "Digital India Mission 2.0",
   "National Manufacturing Mission 2.0"],
  concept="Manufacturing in strategic and frontier sectors",
  explanation="Building on ISM 1.0, the Budget proposed ISM 2.0 to produce semiconductor equipment and materials, "
              "design full-stack Indian IP and fortify supply chains, with industry-led research and training "
              "centres.",
  steps=["Semiconductor equipment, materials, Indian IP → ISM 2.0"],
  why="The other missions were not announced as '2.0' versions for this purpose in the Budget.",
  current=G_BD,
  facts=[fact("India Semiconductor Mission (ISM) 2.0 to be launched to produce equipment and materials, design "
              "full-stack Indian IP, and fortify supply chains", G_BUD)])
Q(T, "Union Budget highlights", "Basic",
  "To create a more contemporary, user-friendly framework for foreign investments, the Union Budget 2026-27 proposed "
  "a comprehensive review of the:",
  ["Foreign Exchange Management (Non-debt Instruments) Rules", "Foreign Exchange Management (Debt Instruments) "
   "Regulations", "Foreign Exchange Management (Overseas Investment) Rules",
   "Foreign Exchange Management (Current Account Transactions) Rules"],
  concept="Foreign investment framework under FEMA",
  explanation="Equity-type foreign investment into India (FDI and portfolio investment) is governed by the FEM "
              "(Non-debt Instruments) Rules. The Budget proposed a comprehensive review of these Rules to create a "
              "more contemporary, user-friendly framework for foreign investments consistent with India's evolving "
              "economic priorities.",
  steps=["Inbound equity investment → FEM (Non-debt Instruments) Rules", "Budget 2026-27: comprehensive review"],
  why="The Debt Instruments Regulations cover debt flows, the Overseas Investment Rules cover outward investment and "
      "the Current Account Transactions Rules cover current account payments; none was named for review.",
  current=G_BD,
  facts=[fact("Smt. Nirmala Sitharaman proposes a comprehensive review of the Foreign Exchange Management (Non-debt "
              "Instruments) Rules in the Union Budget to create a more contemporary, user-friendly framework for "
              "foreign investments consistent with India's evolving economic priorities.", G_BUD)])
Q(T, "Fiscal terms", "Basic",
  "According to the Medium-term Fiscal Policy cum Fiscal Policy Strategy Statement presented with the Union Budget "
  "2026-27, the medium-term aim is a Central Government debt-to-GDP ratio of 50±1% by 2030-31. Which indicator acts "
  "as the operational target?",
  ["Fiscal deficit", "Revenue deficit", "Primary deficit", "Effective revenue deficit"],
  concept="Debt anchor and operational target",
  explanation="The fiscal anchor is the debt glide path; to reach it, the fiscal deficit is used as the operational "
              "target, set at 4.3% of GDP for BE 2026-27.",
  steps=["Anchor: debt-to-GDP 50±1% by FY31", "Operational target: fiscal deficit"],
  why="Revenue, primary and effective revenue deficits are reported but are not the operational target.",
  current=G_BD,
  facts=[fact("The medium-term aim to reach a debt to GDP ratio of 50±1 per cent by FY 2030-31, with the fiscal deficit "
              "acting as the operational target.", G_BUD)])
Q(T, "Economic Survey highlights", "Basic",
  "According to the Economic Survey 2025-26, what were the gross and net NPA ratios of banks in September 2025?",
  ["Gross NPAs 2.2% and net NPAs 0.5%", "Gross NPAs 3.9% and net NPAs 1.0%", "Gross NPAs 0.5% and net NPAs 2.2%",
   "Gross NPAs 7.1% and net NPAs 1.3%"],
  concept="Asset quality of banks",
  explanation="The Survey reported gross NPAs down to 2.2% and net NPAs to 0.5% by September 2025, with bank credit "
              "growing 14.5%.",
  steps=["GNPA 2.2%, NNPA 0.5% (September 2025)"],
  why="3.9%/1.0% are not the September 2025 levels; the third option swaps the two (net NPAs cannot exceed gross); "
      "7.1% and 1.3% are the FY18 and FY26 slippage ratios.",
  current=G_ES,
  facts=[fact("Gross Non-Performing Assets fell to 2.2 percent, while net NPAs declined to 0.5 percent by September "
              "2025. ... Bank credit growth accelerated to 14.5 percent year-on-year.", G_ESP),
         fact("Banking sector asset quality improved significantly, with Gross Non-performing Assets (NPA) at 2.2% and "
              "net NPA at 0.5% in September 2025", G_ESD)])
Q(T, "Fiscal terms", "Intermediate",
  "The Centre's capital expenditure of ₹12.22 lakh crore in BE 2026-27 includes capital support to States through "
  "SASCI. What is SASCI, and what is its outlay?",
  ["Special Assistance as Loan to States for Capital Expenditure; ₹2.0 lakh crore",
   "State Allocation for Social and Capital Investment; ₹1.4 lakh crore",
   "Special Assistance as Loan to States for Capital Expenditure; ₹4.93 lakh crore",
   "Scheme for Aid to States for Capital Infrastructure; ₹2.0 lakh crore as revenue grants"],
  concept="Capital support to States",
  explanation="SASCI (Special Assistance as Loan to States for Capital Expenditure) has an outlay of ₹2.0 lakh crore "
              "in BE 2026-27 and is counted in the Centre's capital expenditure, since it is a loan, not a grant.",
  steps=["SASCI = Special Assistance as Loan to States for Capital Expenditure", "Outlay ₹2.0 lakh crore"],
  why="₹1.4 lakh crore is FC grants; ₹4.93 lakh crore is grants-in-aid for capital assets; SASCI is a loan, not a "
      "revenue grant.",
  current=G_BD,
  facts=[fact("This includes capital support to States through SASCI (Special Assistance as Loan to States for Capital "
              "Expenditure) with an outlay of ₹2.0 lakh crore.", G_BUD)])
Q(T, "Economic Survey highlights", "Intermediate",
  "The Economic Survey 2025-26 urged India to move from import substitution and 'strategic resilience' towards "
  "which goal?",
  ["Strategic indispensability", "Strategic autonomy", "Strategic decoupling", "Strategic self-sufficiency"],
  concept="Theme of the Economic Survey 2025-26",
  explanation="The Survey's framing is a shift from 'Strategic Resilience' (the ability to withstand shocks) to "
              "'Strategic Indispensability', making India hard to replace in key global supply chains.",
  steps=["Import substitution → strategic resilience → strategic indispensability"],
  why="Autonomy, decoupling and self-sufficiency are not the Survey's named goal.",
  current=G_ES,
  facts=[fact("The Survey calls for a shift from Strategic Resilience to Strategic Indispensability", G_ESD),
         fact("Eco Survey maps swadeshi path to strategic resilience, indispensability", G_ESBS)])
Q(T, "Economic Survey highlights", "Intermediate",
  "According to the Economic Survey 2025-26, India's services exports in FY25 reached a record of:",
  ["USD 387.6 billion, up 13.6%", "USD 825.3 billion, up 6.1%", "USD 135.4 billion, up 13.6%",
   "USD 701.4 billion, up 4.9%"],
  concept="External sector",
  explanation="Services exports reached a record USD 387.6 billion in FY25 (+13.6%), helping total exports hit a "
              "record USD 825.3 billion (+6.1%). Remittances were a record USD 135.4 billion.",
  steps=["Services exports FY25 = USD 387.6 bn (+13.6%)"],
  why="USD 825.3 bn is total exports; USD 135.4 bn is remittances; USD 701.4 bn is forex reserves.",
  current=G_ES,
  facts=[fact("Total exports touched a record USD 825.3 bn in FY25 (6.1% YoY growth) ... services exports at an "
              "all-time high of USD 387.6 bn (13.6% YoY growth) ... record remittances of USD 135.4 bn", G_ESD)])

cap18, cap26, yrs = 2.63, 11.21, 8          # FY18 -> FY26 BE = 8 years
mult = cap26 / cap18
cagr = 100 * (mult ** (1 / yrs) - 1)
assert round(mult, 1) == 4.3 and 19.5 < cagr < 20.5          # source rounds the multiple down to "4.2 times"
assert abs(100 * (mult ** (1 / 9) - 1) - 17.5) < 0.5          # wrong count of years (9) gives ~17.5%
assert abs(100 * (mult - 1) / yrs - 40.8) < 0.5               # simple average growth ~41%
assert abs(100 * (mult ** (1 / 7) - 1) - 23.0) < 0.5          # wrong count of years (7) gives ~23%
Q(T, "Fiscal terms", "Advanced",
  "The Economic Survey 2025-26 noted that the Centre's capital expenditure rose from ₹2.63 lakh crore in FY18 to "
  "₹11.21 lakh crore in FY26 (BE). Over these eight years, at roughly what compound annual growth rate (CAGR) did "
  "central capex grow?",
  ["About 20% a year", "About 17.5% a year", "About 41% a year", "About 23% a year"],
  concept="Growth of public capex; compound annual growth rate",
  explanation="The multiple is 11.21 ÷ 2.63 ≈ 4.26 (the Survey calls it a rise of 4.2 times). FY18 to FY26 is 8 "
              "years, so CAGR = 4.26^(1/8) − 1 ≈ 0.199, i.e. about 20% a year (check: 1.2^8 ≈ 4.3).",
  steps=["Multiple = 11.21 ÷ 2.63 ≈ 4.26", "Years = FY26 − FY18 = 8", "CAGR = 4.26^(1/8) − 1 ≈ 20%"],
  why="17.5% spreads the growth over 9 years and 23% over 7; 41% is a simple average (326% ÷ 8) that ignores "
      "compounding.",
  shortcut="Test round rates: 1.2^2 = 1.44, 1.2^4 ≈ 2.07, 1.2^8 ≈ 4.3, which matches the 4.26 multiple.",
  computed=True, current=G_ES,
  facts=[fact("central capex rising 4.2 times from Rs 2.63 lakh crore (FY18) to Rs 11.21 lakh crore (FY26 BE)",
              G_ESD)])
Q(T, "Union Budget highlights", "Advanced",
  "Consider the following statements based on the Macro-economic Framework Statement presented with the Union Budget "
  "2026-27:\nI. Gross fixed capital formation rose by 7.8% in FY26, and its share has stayed at around 30% of GDP for "
  "the past three years.\nII. Gross FDI inflows were USD 81.0 billion in FY25.\nIII. Growth of government final "
  "consumption expenditure slowed from 5.2% in FY25 to 2.3% in FY26.\nWhich of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Macro-economic Framework Statement",
  explanation="GFCF rose 7.8% in FY26 with its share stable at about 30% of GDP (I true). Gross FDI inflows were USD "
              "81.0 billion in FY25 (II true). Government final consumption expenditure is estimated to rebound to "
              "5.2% growth in FY26 from 2.3% in FY25, so III reverses the years and is false.",
  steps=["I: true", "II: true", "III: reversed → false"],
  why="Every option containing III is wrong; 'I and II only' is the only one with both true statements alone.",
  current=G_BD,
  facts=[fact("gross fixed capital formation (GFCF) rising by 7.8 per cent in FY26, higher than the previous year. "
              "Further, the share of GFCF has remained stable at around 30 per cent of GDP for the past three years.",
              G_BUD),
         fact("Government final consumption expenditure is also estimated to strongly rebound with a YoY growth of 5.2 "
              "per cent in FY26 as against 2.3 per cent in FY25. Gross Foreign Direct Investment (FDI) inflows were "
              "recorded at USD 81.0 billion in FY25", G_BUD)])
Q(T, "Union Budget highlights", "Advanced",
  "Match the following FY 2025-26 growth estimates (first advance estimates, as cited in the Budget's Macro-economic "
  "Framework Statement):\nP. Nominal GDP   Q. Services sector   R. Manufacturing and construction   S. Agriculture\n"
  "1. 3.1%   2. 7.0%   3. 8.0%   4. 9.1%",
  ["P-3, Q-4, R-2, S-1", "P-4, Q-3, R-2, S-1", "P-3, Q-2, R-4, S-1", "P-2, Q-4, R-3, S-1"],
  concept="Sectoral growth in FY26",
  explanation="Nominal GDP is estimated to grow 8%, services (the main growth driver) 9.1%, manufacturing and "
              "construction 7% and agriculture 3.1% in FY 2025-26.",
  steps=["Nominal GDP 8.0%", "Services 9.1%", "Manufacturing and construction 7.0%", "Agriculture 3.1%"],
  why="The other options swap nominal GDP with services or manufacturing; services, not nominal GDP, grew fastest.",
  current=G_BD,
  facts=[fact("India's real GDP is estimated to grow by 7.4 per cent in FY 2025–26, with nominal GDP growth at 8 per "
              "cent. The services sector remains the primary growth driver, expanding by 9.1 per cent. Manufacturing "
              "and construction have grown by 7 per cent. Agriculture is estimated to grow at 3.1 per cent.", G_BUD)])

amt_lakh_crore, accts_crore = 36.18, 55.45
avg = amt_lakh_crore * 1e12 / (accts_crore * 1e7)
assert 65000 < avg < 65500 and 50000 < avg <= 500000
Q(T, "Economic Survey highlights", "Advanced",
  "The Economic Survey 2025-26 reported that ₹36.18 lakh crore had been disbursed under Pradhan Mantri MUDRA Yojana "
  "across 55.45 crore loan accounts. What is the average loan per account, and in which PMMY category would a loan "
  "of that size fall?",
  ["About ₹65,000; Kishor", "About ₹65,000; Shishu", "About ₹6.5 lakh; Tarun", "About ₹6,500; Shishu"],
  concept="Scale of MUDRA lending",
  explanation="₹36.18 lakh crore = ₹36.18 × 10¹² and 55.45 crore = 55.45 × 10⁷, so the average is about ₹65,250. "
              "Shishu covers loans up to ₹50,000 and Kishor above ₹50,000 up to ₹5 lakh, so the average lies in Kishor.",
  steps=["36.18 × 10¹² ÷ 55.45 × 10⁷ ≈ ₹65,250", "Above ₹50,000 and up to ₹5 lakh → Kishor"],
  why="₹65,000 exceeds the ₹50,000 Shishu limit; ₹6.5 lakh and ₹6,500 misplace the decimal by a factor of ten.",
  computed=True, current=G_ES,
  facts=[fact("Pradhan Mantri Mudra Yojana ... has disbursed Rs 36.18 lakh crore across 55.45 crore loan accounts.",
              G_ESD),
         fact("Shishu – upto Rs.50,000; Kishore– Above Rs.50,000 and upto Rs.5 lakh; Tarun- Above Rs.5 lakh and upto "
              "Rs.10 lakh", G_PMMY)])

# ================= Government Financial Schemes (Basic 1 / Intermediate 4 / Advanced 2)
T = "Government Financial Schemes"
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Basic",
  "MUDRA, the refinancing agency behind Pradhan Mantri MUDRA Yojana, was converted on 6 January 2016 into a wholly "
  "owned subsidiary of which institution?",
  ["Small Industries Development Bank of India (SIDBI)", "National Bank for Agriculture and Rural Development (NABARD)",
   "Reserve Bank of India", "State Bank of India"],
  concept="Institutional set-up of MUDRA",
  explanation="MUDRA was launched on 8 April 2015 as a subsidiary of SIDBI; on 6 January 2016 it became a wholly owned "
              "subsidiary of SIDBI and was renamed MUDRA (SIDBI) Bank. It refinances member lending institutions "
              "rather than lending to micro units directly.",
  steps=["Launched 8 April 2015", "6 January 2016: wholly owned subsidiary of SIDBI → MUDRA (SIDBI) Bank"],
  why="NABARD, RBI and SBI do not own MUDRA.",
  facts=[fact("On 6 January 2016 it became a wholly owned SIDBI subsidiary and was renamed MUDRA (SIDBI) Bank.",
              G_MUDRA)])
Q(T, "PMMY, PMSBY, PMJJBY, APY", "Intermediate",
  "According to the Department of Financial Services, which of the following is correct about Atal Pension Yojana "
  "(APY)?",
  ["The minimum period of contribution is 20 years or more, and a subscriber may exit voluntarily before 60 on "
   "deduction of the Government co-contribution and the return on it",
   "The minimum period of contribution is 10 years, and a subscriber who exits voluntarily before 60 gets the full "
   "corpus including the Government co-contribution",
   "The minimum period of contribution is 20 years or more, and voluntary exit before 60 is not permitted in any "
   "case",
   "The minimum period of contribution is 15 years, and a subscriber may exit voluntarily before 60 on forfeiting "
   "all contributions"],
  concept="APY contribution period and voluntary exit",
  explanation="Pension under APY begins at 60 and the latest joining age is 40, so every subscriber contributes for at "
              "least 20 years. Subscribers can also exit voluntarily before 60, subject to conditions, but the "
              "Government co-contribution and the return on it are deducted from what they get back.",
  steps=["Pension starts at 60; latest entry at 40 → at least 20 years of contribution",
         "Voluntary exit allowed; Government co-contribution and its return deducted"],
  why="10 and 15 years understate the minimum period; voluntary exit is allowed; on exit the subscriber does not get "
      "the Government co-contribution, nor forfeit his own contributions.",
  facts=[fact("Therefore, minimum period of contribution by any subscriber under APY would be 20 years or more. "
              "Subscribers can also voluntarily exit from APY subject to certain conditions, on deduction of "
              "Government co-contribution and return/interest thereon.", G_APY)])
Q(T, "Credit guarantee schemes", "Intermediate",
  "Under the PM Vidyalaxmi scheme for students admitted on merit to Quality Higher Educational Institutions, what "
  "credit guarantee does the Government of India give to lenders?",
  ["75% for loans up to ₹7.5 lakh", "100% for loans up to ₹10 lakh", "75% for loans up to ₹10 lakh",
   "50% for loans up to ₹7.5 lakh"],
  concept="Credit guarantee for education loans",
  explanation="To encourage lending, the Government provides a 75% credit guarantee on PM Vidyalaxmi education loans "
              "of up to ₹7.5 lakh. ₹10 lakh is the loan limit for the 3% interest subvention, not for the guarantee.",
  steps=["Guarantee: 75%", "Loan size: up to ₹7.5 lakh"],
  why="₹10 lakh is the subvention ceiling; 100% and 50% are not the guarantee rates.",
  facts=[fact("Loans up to ₹ 7.5 lakhs are provided 75% credit guarantee by Government of India, to support banks to "
              "expand coverage.", G_VL)])
Q(T, "Credit guarantee schemes", "Intermediate",
  "The National Credit Guarantee Trustee Company (NCGTC), which acts as a common trustee for several credit "
  "guarantee funds, was set up by:",
  ["The Department of Financial Services, incorporated under the Companies Act, 1956 on 28 March 2014",
   "SIDBI and the Ministry of MSME, as a trust registered in July 2000",
   "RBI, under Section 17 of the RBI Act, 1934, in 1962",
   "NABARD, under the NABARD Act, 1981, in 2010"],
  concept="Institutions for credit guarantees",
  explanation="Following credit guarantee announcements in the 2013-14 Budget, the Department of Financial Services "
              "set up NCGTC, incorporated under the Companies Act, 1956 on 28 March 2014 with paid-up capital of ₹10 "
              "crore, as a common trustee company to manage various credit guarantee trust funds.",
  steps=["Set up by DFS, Ministry of Finance", "Incorporated 28 March 2014 under the Companies Act, 1956"],
  why="The SIDBI/MSME trust of July 2000 is CGTMSE; RBI and NABARD did not set up NCGTC.",
  facts=[fact("incorporated under the Companies Act, 1956 on March 28, 2014 with a paid up capital of ₹10 crore; set "
              "up by the Department of Financial Services, Ministry of Finance, Government of India to act as a "
              "common trustee company to manage and operate various credit guarantee trust funds", G_NCGTC)])
Q(T, "Credit guarantee schemes", "Intermediate",
  "Which of the following credit guarantee funds is NOT listed among the funds under NCGTC's trusteeship?",
  ["Credit Guarantee Fund Trust for Micro and Small Enterprises (CGTMSE)",
   "Credit Guarantee Fund for Stand Up India (CGFSI)", "Credit Guarantee Fund for Education Loans (CGFEL)",
   "Credit Guarantee Fund for Factoring (CGFF)"],
  concept="Credit guarantee institutions",
  explanation="NCGTC acts as trustee for funds such as CGFSD (skill development), CGFEL (education loans), CGFF "
              "(factoring), CGFMU (micro units), CGFSI (Stand-Up India), ECLGS and CGSS (startups). CGTMSE is a "
              "separate trust set up by SIDBI and the Ministry of MSME.",
  steps=["NCGTC funds: CGFSD, CGFEL, CGFF, CGFMU, CGFSI, ECLGS, CGSS …", "CGTMSE: separate trust"],
  why="CGFSI, CGFEL and CGFF are all on NCGTC's list of funds.",
  facts=[fact("Funds under its trusteeship: Credit Guarantee Fund for Skill Development (CGFSD), Credit Guarantee Fund "
              "for Education Loans (CGFEL), Credit Guarantee Fund for Factoring (CGFF), Credit Guarantee Fund for "
              "Micro Units (CGFMU), Credit Guarantee Fund for Stand Up India (CGFSI)", G_NCGTC)])

loan_a, inc_a, loan_b, inc_b, sub_cap, g_cap, inc_cap = 7, 9, 12, 6, 10, 7.5, 8   # ₹ lakh
sub_b = min(loan_b, sub_cap) * 100000 * 3 // 100
assert loan_a <= g_cap and inc_a > inc_cap               # A: guarantee yes, subvention no
assert loan_b > g_cap and inc_b <= inc_cap               # B: guarantee no, subvention yes
assert sub_b == 30000 and loan_b * 100000 * 3 // 100 == 36000
Q(T, "Credit guarantee schemes", "Advanced",
  "Two students secure merit admission to Quality Higher Educational Institutions and take PM Vidyalaxmi education "
  "loans; neither gets any other scholarship or subvention. A borrows ₹7 lakh and her annual family income is ₹9 "
  "lakh. B borrows ₹12 lakh and his family income is ₹6 lakh. Which statement is correct?",
  ["A's loan gets the 75% guarantee but no subvention; B's loan gets no guarantee but subvention of ₹30,000 a year "
   "during the moratorium",
   "A's loan gets the guarantee and 3% subvention; B gets subvention of ₹36,000 a year during the moratorium",
   "A's loan gets neither benefit; B's loan gets the 75% guarantee and subvention of ₹30,000 a year",
   "A's loan gets the 75% guarantee but no subvention; B gets the guarantee on ₹7.5 lakh and subvention of ₹36,000 "
   "a year"],
  concept="PM Vidyalaxmi: guarantee and interest subvention",
  explanation="The 75% guarantee is for loans up to ₹7.5 lakh, so A (₹7 lakh) is covered and B (₹12 lakh) is not. "
              "The 3% subvention is for family income up to ₹8 lakh and on loans up to ₹10 lakh (only the first ₹10 "
              "lakh of a bigger loan), during the moratorium: A (₹9 lakh income) gets none; B gets 3% × ₹10 lakh = "
              "₹30,000 a year.",
  steps=["Guarantee: A yes (≤ ₹7.5 lakh), B no", "Subvention: A no (income > ₹8 lakh)",
         "B: 3% × ₹10 lakh = ₹30,000 a year"],
  why="₹36,000 applies 3% to the whole ₹12 lakh; B's loan exceeds the ₹7.5 lakh guarantee limit; A qualifies for the "
      "guarantee.",
  computed=True,
  facts=[fact("Loans up to ₹ 7.5 lakhs are provided 75% credit guarantee by Government of India. For students with up "
              "to ₹ 8 lakhs annual family income, the scheme provides for 3% interest subvention on loans up to ₹ 10 "
              "lakh.", G_VL),
         fact("If the education loan amount is more than ₹ 10 lakhs, interest subvention is provided for the disbursed "
              "total principal amount of the loan up to ₹ 10 lakhs only.", G_VL)])
Q(T, "Credit guarantee schemes", "Advanced",
  "Consider the following statements about PM Vidyalaxmi education loans:\nI. The interest rate is capped at the "
  "lending bank's External Benchmark Lending Rate (EBLR) plus 0.5%.\nII. The loan is repayable over up to 15 years, "
  "excluding a moratorium of the course period plus one year.\nIII. There is no cap on the number of students who can "
  "receive the 3% interest subvention in a year.\nWhich of the above is/are correct?",
  ["I and II only", "II and III only", "I only", "I, II and III"],
  concept="PM Vidyalaxmi loan terms",
  explanation="Interest is capped at the bank's EBLR + 0.5% (I) and repayment runs up to 15 years after a moratorium "
              "of course period plus one year (II). A maximum of one lakh students a year are eligible for the 3% "
              "subvention, so III is false (the no-limit rule is for PM-USP CSIS beneficiaries).",
  steps=["I: true", "II: true", "III: capped at 1 lakh students a year → false"],
  why="Options containing III are wrong; 'I only' leaves out II.",
  facts=[fact("The interest rates charged on the educational loan under the scheme will be capped at the individual "
              "bank's Externally Benchmarked Lending Rate (EBLR) + 0.5%. The repayment period of the education loan is "
              "up to 15 years, excluding a moratorium period of the course period plus one year.", G_VL),
         fact("In a year, a maximum of one lakh students shall be eligible for 3% interest subvention during the "
              "moratorium period. No such limit is for CSIS beneficiaries.", G_VL)])


# ================================================================= checks and output
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_007_plan.json").read_text(encoding="utf-8"))
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
    "batch_id": "BATCH_007",
    "created_at": TODAY,
    "notes": NOTES,
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_007_BFA.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions; keys {dict(sorted(_keys.items()))}; "
      f"current_affairs {sum('current_affairs' in q for q in questions)}; independent {len(INDEPENDENT)})")
