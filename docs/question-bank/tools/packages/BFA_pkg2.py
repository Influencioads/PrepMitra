"""Writes the three fragment files of Banking and Financial Awareness topic package 2 (BFA_pkg2):
batches/parts/frag/BATCH_008_BFA_pkg2.json, BATCH_009_BFA_pkg2.json and BATCH_010_BFA_pkg2.json.

Topics: NPA, Basel Norms, Financial Inclusion, Priority Sector Lending, RBI Integrated Ombudsman Scheme, Digital
Banking, UPI, NEFT, RTGS, IMPS, NPCI (209 questions across batches 8-10, per batches/plans/packages/BFA_pkg2.json).

Every fact is backed by at least one fact_check whose source was opened on 2026-11-06 with a plain client (curl, no
user-agent spoofing, no bot-check workaround; rbidocs PDFs and npci.org.in were not used because they block automated
access). Facts seen only in search results are listed in SEARCH_ONLY and carry web:search-confirmed. Only current rules
are tested (RBI's consolidated Directions of November 2025 as updated, current FAQs, the RB-IOS 2026); older booklets
and circulars appear only as explicitly historical facts. Dated or changeable values carry current_affairs with the
event date taken from the source. Every computable answer is re-derived below with assertions; the per-batch quota per
(topic, difficulty), the question-ID ranges and the stimulus starts are checked against the package plan, and keys are
balanced per batch. ai:independent-check is added only to questions whose tag is in INDEPENDENT (answered blind by a
separate fresh solver, matched with confidence, unchanged since). All earlier questions of these topics (BATCH_000 to
BATCH_006, and BATCH_007 if present) were read first and their facts are not repeated. If any check fails, nothing is
written.

    python tools/packages/BFA_pkg2.py      (run from anywhere)
"""

import json
import random
import sys
from collections import Counter, defaultdict
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
PKG = json.loads((ROOT / "batches" / "plans" / "packages" / "BFA_pkg2.json").read_text(encoding="utf-8"))
BATCHES = sorted(PKG["batches"])          # ["008", "009", "010"]

_rng = random.Random(2026110602)
_keys = {b: Counter() for b in BATCHES}
records = defaultdict(list)               # batch -> list of (tag, record)
_tags = set()

# Tags of questions that a separate fresh solver answered blind (stem and options only) and matched with confidence.
# Tags of questions that a separate fresh solver answered blind (stem and options only, no key or solution) and
# matched with high confidence. All 209 questions were given to two fresh solvers (105 + 104); 203 matched the key
# (138 high, 52 medium, 13 low confidence) and 6 did not (5 low, 1 high: the foreign-bank export-credit item, whose
# key was re-checked against the PSL Directions table and stands). Only the 138 high-confidence matches are tagged.
INDEPENDENT = {
    "A-FI08-01", "A-FI08-02", "A-FI08-03", "A-FI08-04", "A-FI08-06", "A-FI08-07", "A-FI09-01", "A-FI09-03",
    "A-FI09-04", "A-FI09-06", "A-FI10-01", "A-FI10-02", "A-FI10-03", "A-FI10-04", "A-FI10-05", "A-FI10-06",
    "A-FI10-07", "A-FI10-08", "A-FI10-09", "A-FI10-10", "A-NPA08-01", "A-NPA08-02", "A-NPA08-03", "A-NPA08-05",
    "A-NPA08-06", "A-NPA08-07", "A-NPA08-09", "A-NPA09-01", "A-NPA09-02", "A-NPA09-03", "A-NPA09-04", "A-NPA09-07",
    "A-NPA10-01", "A-NPA10-02", "A-NPA10-04", "A-NPA10-05", "A-NPA10-06", "A-PSL08-05", "A-PSL08-06", "A-PSL09-01",
    "A-PSL09-02", "A-PSL09-04", "A-PSL09-06", "A-PSL10-02", "A-PSL10-04", "B-BAS08-01", "B-BAS08-03", "B-BAS08-04",
    "B-BAS08-05", "B-BAS08-06", "B-BAS09-01", "B-BAS09-02", "B-BAS09-05", "B-BAS09-06", "B-BAS09-07", "B-BAS09-08",
    "B-BAS09-09", "B-BAS09-10", "B-BAS09-11", "B-BAS10-01", "B-BAS10-02", "B-BAS10-03", "B-BAS10-04", "B-BAS10-05",
    "B-BAS10-06", "B-BAS10-07", "B-DIG08-01", "B-DIG08-02", "B-DIG08-03", "B-DIG08-06", "B-DIG08-08", "B-DIG09-01",
    "B-DIG09-02", "B-DIG09-03", "B-DIG09-04", "B-DIG09-05", "B-DIG10-01", "B-DIG10-02", "B-IOS08-01", "B-IOS08-03",
    "B-IOS08-05", "B-IOS08-07", "B-IOS09-03", "B-IOS10-01", "B-IOS10-06", "C-IMPS08-01", "C-IMPS08-02",
    "C-IMPS08-03", "C-IMPS09-01", "C-IMPS09-02", "C-IMPS09-03", "C-IMPS10-01", "C-IMPS10-02", "C-IMPS10-03",
    "C-NEFT08-01", "C-NEFT08-02", "C-NEFT09-01", "C-NEFT09-02", "C-NEFT09-03", "C-NEFT10-01", "C-NEFT10-02",
    "C-NEFT10-03", "C-NPCI08-03", "C-NPCI08-06", "C-NPCI09-02", "C-NPCI09-03", "C-NPCI09-04", "C-NPCI09-05",
    "C-NPCI10-01", "C-NPCI10-02", "C-NPCI10-03", "C-NPCI10-04", "C-RTGS08-01", "C-RTGS08-02", "C-RTGS08-03",
    "C-RTGS09-01", "C-RTGS10-01", "C-RTGS10-02", "C-RTGS10-03", "C-RTGS10-04", "C-UPI08-01", "C-UPI08-02",
    "C-UPI08-03", "C-UPI08-04", "C-UPI08-06", "C-UPI08-07", "C-UPI09-02", "C-UPI09-03", "C-UPI09-04", "C-UPI09-05",
    "C-UPI09-06", "C-UPI09-07", "C-UPI10-01", "C-UPI10-02", "C-UPI10-03", "C-UPI10-04", "C-UPI10-06", "C-UPI10-08"
}

# URLs confirmed only through search results (each section adds its own with SEARCH_ONLY.update(...)).
SEARCH_ONLY = set()


def fact(claim, url):
    return {"claim": claim, "source_url": url, "checked_on": CHECKED}


def ca(event_date, review_by=REVIEW_BY):
    return {"event_date": event_date, "review_by": review_by}


def Q(batch, tag, topic, subtopic, difficulty, text, options, answer=None, *, concept, explanation, steps, facts, why,
      seconds=None, computed=False, current=None, shortcut=None):
    """Adds one question to `batch` ("008"/"009"/"010"). `tag` is a unique label (used for INDEPENDENT). With
    answer=None, options[0] is the correct text and it is placed at the batch's least-used key so far (random
    tie-break, fixed seed)."""
    assert batch in BATCHES, batch
    assert tag not in _tags, tag
    _tags.add(tag)
    assert len(options) == 4 and len(set(options)) == 4, text
    assert facts and why and steps, text
    if answer is None:
        k = _keys[batch]
        low = min(k[x] for x in LETTERS)
        pos = LETTERS.index(_rng.choice([x for x in LETTERS if k[x] == low]))
        correct, wrongs = options[0], list(options[1:])
        options = wrongs[:pos] + [correct] + wrongs[pos:]
        answer = LETTERS[pos]
    assert answer in LETTERS
    _keys[batch][answer] += 1
    urls = {f["source_url"] for f in facts}
    web = (["web:fact-check"] if urls - SEARCH_ONLY else []) + (["web:search-confirmed"] if urls & SEARCH_ONLY else [])
    out = {
        "question_id": None,                  # assigned per batch at the end, in order
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
    records[batch].append((tag, out))


# ####################################################################################################
# ===== NPA, Priority Sector Lending, Financial Inclusion
# ####################################################################################################
# ================================================================ PART A: NPA, Priority Sector Lending, Financial Inclusion
# Sources opened on 2026-11-06 with a plain client (curl) unless listed in SEARCH_ONLY.
A_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id="
A_IRAC = A_MD + "13146"     # CB - Income Recognition, Asset Classification and Provisioning Directions, 2025 (upd. 1 Oct 2026)
A_RSA = A_MD + "13145"      # CB - Resolution of Stressed Assets Directions, 2025 (updated 1 Oct 2026)
A_PSL = A_MD + "12799"      # Master Directions - PSL Targets and Classification Directions, 2025 (as updated)
A_BRANCH = A_MD + "13164"   # CB - Branch Authorisation Directions, 2025 (updated 1 Oct 2026)
A_PSLFAQ = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id=87"    # FAQs on PSL (Sep 11, 2026)
A_ARC = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id=179"      # All you wanted to know about ARCs (Sep 11, 2026)
A_IBBI = "https://ibbi.gov.in/en/about"
A_BCDP = "https://www.rbi.org.in/scripts/bs_viewcontent.aspx?Id=2234"  # RBI discussion paper on 'for-profit' companies as BCs
A_PMJDY12 = "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/aug/doc_9716_20260827_14055201.pdf"
A_SBIJDY = "https://sbi.bank.in/web/faq-s/faq-pradhan-mantri-jan-dhan-yojana-pmjdy"   # SBI FAQ on PMJDY (upd. 30-03-2026)
A_SARF1 = ("https://www.casemine.com/in/column/section-31-of-the-sarfaesi-act:-scope,-exemptions,-and-judicial-"
           "interpretation/view")
A_SARF2 = "https://www.taxmann.com/post/blog/enforcement-of-security-interest-by-banks-under-sarfaesi-act"
SEARCH_ONLY.update({A_SARF1, A_SARF2})

# ---------------------------------------------------------------- NPA
T = "NPA"
# ---- batch 008: Basic 3, Intermediate 5, Advanced 4
Q("008", "A-NPA08-01", T, "Classification", "Basic",
  "Under RBI's Income Recognition, Asset Classification and Provisioning (IRACP) Directions, 2025 for commercial "
  "banks, an account is classified as NPA if its regular or ad hoc credit limits have not been reviewed or renewed "
  "within how many days from the due date or date of ad hoc sanction?",
  ["180 days", "90 days", "60 days", "365 days"],
  concept="NPA trigger for unreviewed credit limits",
  explanation="Among the conditions for NPA classification, the IRACP Directions list an account where the regular or "
              "ad hoc credit limits have not been reviewed or renewed within 180 days from the due date or the date of "
              "ad hoc sanction.",
  steps=["Limits not reviewed/renewed", "Count from due date / date of ad hoc sanction", "More than 180 days → NPA"],
  why="90 days is the overdue norm for term loans; 60 days ends SMA-1; 365 days is not a period in this rule.",
  facts=[fact("an account where the regular / ad hoc credit limits have not been reviewed / renewed within 180 days "
              "from the due date / date of ad hoc sanction", A_IRAC)])
Q("008", "A-NPA08-02", T, "Classification", "Basic",
  "Under RBI's IRACP Directions, 2025, stock audit at annual intervals by external agencies is mandatory for NPAs "
  "with a balance of at least:",
  ["₹5 crore", "₹1 crore", "₹25 crore", "₹50 lakh"],
  concept="Stock audit of large NPAs",
  explanation="To make stock valuation more reliable and reduce divergence, the Directions make annual stock audit by "
              "external agencies (appointed under Board-approved guidelines) mandatory for NPAs with a balance of ₹5 "
              "crore and above.",
  steps=["NPA balance ≥ ₹5 crore", "Annual stock audit by external agency is mandatory"],
  why="₹1 crore, ₹25 crore and ₹50 lakh are not the threshold in the Directions.",
  facts=[fact("Stock audit at annual intervals by external agencies ... shall be mandatory in cases of NPAs with "
              "balance of ₹5 crore and above", A_IRAC)])
Q("008", "A-NPA08-03", T, "Resolution and IBC", "Basic",
  "Over which of the following does the Insolvency and Bankruptcy Board of India (IBBI) NOT have regulatory "
  "oversight?",
  ["Asset reconstruction companies", "Insolvency professional agencies", "Information utilities",
   "Insolvency professionals"],
  concept="Role of IBBI",
  explanation="IBBI describes itself as a unique regulator of both a profession and processes: it has regulatory "
              "oversight over insolvency professionals, insolvency professional agencies, insolvency professional "
              "entities and information utilities. Asset reconstruction companies are registered and regulated by "
              "RBI under the SARFAESI Act.",
  steps=["IBBI oversees IPs, IPAs, IPEs and IUs", "ARCs → RBI (SARFAESI Act)"],
  why="IPAs, information utilities and insolvency professionals are all under IBBI's oversight.",
  facts=[fact("It has regulatory oversight over the Insolvency Professionals, Insolvency Professional Agencies, "
              "Insolvency Professional Entities and Information Utilities", A_IBBI),
         fact("ARCs are registered under Section 3 of the ... SARFAESI Act and regulated using the powers vested with "
              "the Reserve Bank thereunder", A_ARC)])
Q("008", "A-NPA08-04", T, "Resolution and IBC", "Intermediate",
  "Under RBI's Resolution of Stressed Assets Directions, 2025, special mention account (SMA) categories differ for "
  "revolving facilities such as cash credit or overdraft. Which SMA sub-category is NOT defined for such revolving "
  "facilities?",
  ["SMA-0", "SMA-1", "SMA-2", "None; all three apply equally to revolving facilities"],
  concept="SMA classification of revolving facilities",
  explanation="For loans other than revolving facilities, SMA-0 (up to 30 days overdue), SMA-1 (31-60 days) and SMA-2 "
              "(61-90 days) are defined. For cash credit/overdraft, the table has only SMA-1 and SMA-2, based on the "
              "outstanding remaining continuously above the sanctioned limit or drawing power (whichever is lower) for "
              "more than 30 up to 60 days and more than 60 up to 90 days.",
  steps=["Term loans: SMA-0, SMA-1, SMA-2", "CC/OD: only SMA-1 (30-60 days) and SMA-2 (60-90 days)"],
  why="SMA-1 and SMA-2 do apply to revolving facilities, so they are not the answer, and the fourth option is wrong.",
  facts=[fact("Loans in the nature of revolving facilities like cash credit/overdraft ... SMA-1 More than 30 days and "
              "up to 60 days; SMA-2 More than 60 days and up to 90 days (SMA-0 Up to 30 days listed only for loans "
              "other than revolving facilities)", A_RSA)])
Q("008", "A-NPA08-05", T, "Classification", "Intermediate",
  "A bank financed an industrial project with a moratorium on payment of interest during the gestation period. The "
  "project is still within the moratorium. Under RBI's IRACP Directions, 2025, how is the unpaid interest treated?",
  ["It becomes 'due' only after the moratorium is over, so the account does not become NPA on this ground",
   "It is overdue from the first quarter, so the account becomes NPA after 90 days",
   "The account is classified as substandard but income may still be recognised",
   "The account is classified as SMA-2 until the moratorium ends"],
  concept="Loans with moratorium on interest",
  explanation="For finance to industrial projects or agricultural plantations with a moratorium on interest, interest "
              "becomes 'due' only after the moratorium or gestation period is over; such amounts do not become "
              "overdue, and hence the account does not become NPA, with reference to the date of debit of interest.",
  steps=["Moratorium running → interest not yet due", "Not overdue → no NPA on this ground"],
  why="Interest that is not due cannot be overdue, so neither NPA nor SMA classification arises; no substandard "
      "classification applies.",
  facts=[fact("where moratorium is available for payment of interest, payment of interest becomes 'due' only after "
              "the moratorium or gestation period is over. Such amounts of interest do not become overdue and hence do "
              "not become NPA", A_IRAC)])
Q("008", "A-NPA08-06", T, "Resolution and IBC", "Intermediate",
  "Under a resolution plan implemented under RBI's Resolution of Stressed Assets Directions, 2025, lenders sanction "
  "additional finance to the borrower. How may a bank classify this additional finance?",
  ["As a standard asset during the monitoring period, if the account performs satisfactorily; otherwise in the same "
   "category as the restructured debt",
   "Always as NPA until the entire restructured debt is repaid",
   "As a standard asset permanently, whatever the account's later performance",
   "As a loss asset, since it is lent to a stressed borrower"],
  concept="Additional finance under resolution plans",
  explanation="Additional finance approved under a resolution plan (including an IBC plan approved by the Adjudicating "
              "Authority) may be treated as standard during the monitoring period, provided the account shows "
              "satisfactory performance. If the restructured asset fails to perform or does not qualify for upgrade at "
              "the end of the monitoring period, the additional finance is placed in the same asset classification "
              "category as the restructured debt.",
  steps=["During monitoring period + satisfactory performance → standard",
         "Failure / no upgrade → same category as restructured debt"],
  why="It is neither automatically NPA nor permanently standard, and there is no rule making it a loss asset.",
  facts=[fact("Any additional finance approved under the resolution plan ... may be treated by a bank as standard asset "
              "during the monitoring period under the approved resolution plan, provided the account demonstrates "
              "satisfactory performance during the monitoring period", A_RSA),
         fact("If the restructured asset fails to perform satisfactorily during the monitoring period or does not "
              "qualify for upgradation at the end of the monitoring period, the additional finance shall be placed in "
              "the same asset classification category as the restructured debt", A_RSA)])
Q("008", "A-NPA08-07", T, "Classification", "Intermediate",
  "A borrower's cash credit account with a bank has been classified as NPA. The same bank had also discounted bills "
  "drawn under a letter of credit (LC) in the borrower's favour, which are not yet due. Under RBI's IRACP "
  "Directions, 2025, how may the LC-backed bills be treated?",
  ["They may not be classified as NPA, unless the LC is not honoured on the due date and the borrower does not make "
   "good the amount immediately",
   "They must be classified as NPA at once, since classification is borrower-wise",
   "They become NPA only if the LC-issuing bank is itself classified as weak",
   "They are written off along with the cash credit account"],
  concept="Exception for bills discounted under LC",
  explanation="Although classification is normally borrower-wise, the Directions say bills discounted under an LC "
              "favouring a borrower may not be classified as NPA when another facility of the borrower is NPA. If the "
              "documents are not accepted or the LC-issuing bank does not pay on the due date and the borrower does "
              "not immediately make good the amount, the bills become NPA at once.",
  steps=["Borrower-wise rule has an exception for LC-backed bills", "Default under LC + no immediate payment → NPA"],
  why="The borrower-wise rule is expressly relaxed here; the issuing bank's health is not the test; no write-off is "
      "required.",
  facts=[fact("The bills discounted under Letter of Credit (LC) favouring a borrower may not be classified as NPA, "
              "when any other facility granted to the borrower is classified as NPA", A_IRAC),
         fact("in case documents under LC are not accepted on presentation or the payment under the LC is not made on "
              "the due date ... and the borrower does not immediately make good the amount ... the outstanding bills "
              "discounted shall immediately be classified as NPA", A_IRAC)])
Q("008", "A-NPA08-08", T, "SARFAESI", "Intermediate",
  "An asset reconstruction company (ARC) registered under the SARFAESI Act does not have a net owned fund of ₹1,000 "
  "crore. According to RBI's FAQs on ARCs (September 2026), can it act as a resolution applicant under the IBC to "
  "acquire a financial asset (debt)?",
  ["Yes; acquisition of debt is a permitted activity for ARCs, so the ₹1,000 crore NOF condition need not be met",
   "No; only ARCs with NOF of at least ₹1,000 crore can be resolution applicants for any purpose",
   "No; ARCs can never be resolution applicants under the IBC",
   "Yes, but only with prior approval of IBBI"],
  concept="ARCs as resolution applicants",
  explanation="RBI's FAQs say that since acquisition of debt falls within 'securitisation' and 'asset reconstruction' "
              "under the SARFAESI Act, ARCs need not meet the conditions of paragraph 18 of the ARC Directions, 2025, "
              "including the ₹1,000 crore net owned fund, to act as resolution applicant for acquiring a financial "
              "asset.",
  steps=["Acquisition of debt = permitted ARC activity", "₹1,000 crore NOF condition does not apply to it"],
  why="The ₹1,000 crore NOF condition applies to other resolution-applicant roles, not to acquiring debt; IBBI approval "
      "is not the condition.",
  facts=[fact("acquisition of debt is a permitted activity for ARCs. Therefore, ARCs need not meet the conditions "
              "specified in paragraph 18 of the ... (Asset Reconstruction Companies) Directions, 2025 ..., inter alia, a "
              "net owned fund of ₹1000 crore", A_ARC)])


# unhedged foreign currency exposure: incremental provision in bps of total exposure by likely loss / EBID
def _ufce_bps(ratio):
    return 0 if ratio <= 15 else 20 if ratio <= 30 else 40 if ratio <= 50 else 60 if ratio <= 75 else 80


_u = [(500, 40), (200, 80), (300, 12)]          # (exposure ₹ crore, likely loss / EBID %)
assert abs(sum(e * _ufce_bps(r) / 10000 for e, r in _u) - 3.6) < 1e-9
assert abs(500 * 0.004 + 200 * 0.006 - 3.2) < 1e-9          # distractor logic check (Y at 60 bps) differs
Q("008", "A-NPA08-09", T, "Classification", "Advanced",
  "A bank has three borrowers with unhedged foreign currency exposure. Using the ratio of likely loss to EBID: X has a "
  "total exposure of ₹500 crore and a ratio of 40%; Y has ₹200 crore and 80%; Z has ₹300 crore and 12%. Under RBI's "
  "IRACP Directions, 2025, what incremental provision (over the standard asset provision) must the bank hold on "
  "these three exposures together?",
  ["₹3.6 crore", "₹3.2 crore", "₹4.2 crore", "₹2.0 crore"],
  concept="Incremental provisioning for unhedged foreign currency exposure",
  explanation="The table prescribes nil up to 15%, 20 bps for more than 15% up to 30%, 40 bps for more than 30% up to "
              "50%, 60 bps for more than 50% up to 75% and 80 bps above 75%, on the total credit exposure. X: 40 bps × "
              "500 = ₹2.0 crore; Y: 80 bps × 200 = ₹1.6 crore; Z: nil. Total ₹3.6 crore.",
  steps=["X: 40% → 40 bps × ₹500 crore = ₹2.0 crore", "Y: 80% → 80 bps × ₹200 crore = ₹1.6 crore",
         "Z: 12% ≤ 15% → nil", "Total = ₹3.6 crore"],
  why="₹3.2 crore applies 60 bps to Y (that slab ends at 75%); ₹4.2 crore wrongly adds 20 bps on Z; ₹2.0 crore "
      "counts X only.",
  computed=True,
  facts=[fact("Up to 15 per cent 0; More than 15 per cent and up to 30 per cent 20 bps; More than 30 per cent and up "
              "to 50 per cent 40 bps; More than 50 per cent and up to 75 per cent 60 bps; More than 75 per cent 80 bps "
              "(incremental provisioning on the total credit exposures over and above extant standard asset "
              "provisioning)", A_IRAC)])

# country risk: net funded exposure >= 1% of total assets; short-term (<180 days) may carry 25% of the requirement
_assets = 10000
_cr = [("C1", 25, 200, False), ("B1", 5, 100, True), ("A2", 0.25, 50, False)]   # (cat, rate %, exposure, short-term)
assert abs(sum(e * r / 100 * (0.25 if st else 1) for c, r, e, st in _cr if e >= 0.01 * _assets) - 51.25) < 1e-9
Q("008", "A-NPA08-10", T, "Classification", "Advanced",
  "A bank with total assets of ₹10,000 crore has these net funded country exposures: ₹200 crore to a country in ECGC "
  "category C1 (moderately high risk); ₹100 crore, all short-term (contractual maturity under 180 days), to a "
  "category B1 country (moderately low risk); and ₹50 crore to a category A2 country (low risk). It uses the lower "
  "provisioning allowed for short-term exposures. Under RBI's IRACP Directions, 2025, what is its minimum country "
  "risk provision?",
  ["₹51.25 crore", "₹55.00 crore", "₹51.375 crore", "₹50.00 crore"],
  concept="Provisioning for country risk",
  explanation="Country risk provisions apply only where the net funded exposure is 1% or more of total assets (here "
              "₹100 crore), at 0.25% (A1/A2), 5% (B1), 20% (B2), 25% (C1) and 100% (C2/D); short-term exposures may "
              "carry 25% of the requirement. C1: 25% of 200 = ₹50 crore. B1: 5% of 100 = ₹5 crore, × 25% = ₹1.25 "
              "crore. A2: ₹50 crore is below 1% of assets, so nil. Total ₹51.25 crore.",
  steps=["Threshold: 1% of ₹10,000 crore = ₹100 crore", "C1: 25% × 200 = ₹50 crore",
         "B1 (exactly 1%, short-term): 5% × 100 × 25% = ₹1.25 crore", "A2: below threshold → nil",
         "Total = ₹51.25 crore"],
  why="₹55 crore ignores the short-term relief; ₹51.375 crore wrongly provides 0.25% on the A2 exposure below the 1% "
      "threshold; ₹50 crore drops the B1 exposure, which meets the 'one per cent or more' test.",
  computed=True,
  facts=[fact("Moderately Low Risk B1 5; Moderate Risk B2 20; Moderately High Risk C1 25; ... A bank shall make "
              "provision for country risk in respect of a country where its net funded exposure is one per cent or "
              "more of its total assets", A_IRAC),
         fact("A bank may make a lower level of provisioning (say 25 per cent of the requirement) in respect of "
              "short-term exposures (i.e. exposures with contractual maturity of less than 180 days)", A_IRAC)])

_out = 40
assert abs(2 * 0.05 * _out - 4) < 1e-9 and abs(0.20 * _out - 8) < 1e-9
Q("008", "A-NPA08-11", T, "Resolution and IBC", "Advanced",
  "A borrower hit by a natural calamity has outstanding debt of ₹40 crore with a bank, all in term loans. A resolution "
  "plan is implemented under Chapter VI-A of RBI's Resolution of Stressed Assets Directions, 2025 and, later, a second "
  "restructuring under the same Chapter becomes necessary (assume the outstanding stays ₹40 crore). Under the IRACP "
  "Directions, 2025, what additional specific provision applies, and when can it be written back?",
  ["₹4 crore (5% for each instance); after the borrower pays at least ₹8 crore (20%) without slipping into NPA and "
   "without another restructuring",
   "₹2 crore (5% once); after the borrower pays at least ₹4 crore (10%)",
   "₹4 crore (5% for each instance); after one year from implementation, whatever the repayment",
   "₹8 crore (20%); only when the entire debt is repaid"],
  concept="Additional provisioning on resolution under Chapter VI-A",
  explanation="A bank must make an additional specific provision of 5% of the outstanding debt when a plan is "
              "implemented under Chapter VI-A, and another 5% for each instance of repeated restructuring (over and "
              "above prudential provisions, capped at 100%). It may be written back once the borrower pays at least "
              "20% of the outstanding debt without slipping into NPA and without another restructuring. The one-year "
              "write-back applies only when the debt is entirely non-fund-based or cash credit/overdraft type.",
  steps=["Two instances × 5% × ₹40 crore = ₹4 crore",
         "Write-back: borrower pays ≥ 20% = ₹8 crore, no NPA, no fresh restructuring"],
  why="Repeated restructuring attracts 5% per instance, not once; 10% repayment is not the write-back test; the "
      "one-year route is only for non-fund-based or CC/OD debt; 20% is the repayment test, not the provision.",
  computed=True,
  facts=[fact("A bank shall make an additional specific provision of five percent of the outstanding debt ... For "
              "accounts where repeated restructuring is necessitated ... additional specific provisioning of five per "
              "cent of the outstanding debt for each instance of restructuring", A_IRAC),
         fact("may be written back upon the borrower paying at least 20% of the outstanding debt with the bank, without "
              "slipping into NPA post implementation of the restructuring, and without being subjected to another "
              "restructuring", A_IRAC)])
Q("008", "A-NPA08-12", T, "SARFAESI", "Advanced",
  "Consider the following statements about asset reconstruction companies (ARCs), based on RBI's FAQs on ARCs "
  "(September 2026):\nI. Yield on security receipts (SRs) is recognised only after full redemption of the entire "
  "principal amount of the SRs.\nII. An ARC may distribute upside income on a priority basis to one class of SR "
  "holders over others.\nIII. Clauses such as 'NAV Protection Clauses' that delink the management fee from the ARC's "
  "performance are inconsistent with RBI's ARC Directions.\nWhich of the above are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="Distribution of SR income and management fee",
  explanation="RBI's FAQs say yield on SRs is recognised only after full redemption of the entire principal of SRs and "
              "upside income only after full redemption of SRs; ARCs may not distribute yield or upside income on a "
              "priority basis to one class of SR holders. The management fee must be linked to performance and "
              "actual recoveries; NAV protection clauses that delink it are inconsistent with the Directions.",
  steps=["I: correct (yield after full principal redemption)", "II: wrong (no priority distribution)",
         "III: correct (fee must be performance-linked)"],
  why="Any option containing II is wrong, because priority distribution to one class is not permitted.",
  facts=[fact("yield on SRs shall be recognised only after the full redemption of the entire principal amount of SRs, "
              "and upside income shall be recognised only after the full redemption of SRs ... ARCs are not permitted "
              "to distribute yield or upside income on a priority basis to one class of SR holders", A_ARC),
         fact("The management fee charged by ARCs must be linked to the performance of the ARC ... Any practice aimed at "
              "delinking the management fee from the performance of ARCs by clauses like 'NAV Protection Clauses' is "
              "inconsistent with the principles of the ... Directions, 2025", A_ARC)])


# ---- batch 009: Basic 3, Intermediate 1, Advanced 3
Q("009", "A-NPA09-01", T, "Classification", "Basic",
  "Housing loans given at 'teaser rates' (comparatively low rates in the first few years, reset higher later) attract "
  "what standard asset provision under RBI's IRACP Directions, 2025?",
  ["2.00 per cent", "0.25 per cent", "0.40 per cent", "1.00 per cent"],
  concept="Standard asset provision on teaser-rate housing loans",
  explanation="Because of their higher risk, housing loans at teaser rates carry a 2.00% standard asset provision. It "
              "reverts to 0.40% one year after the rates are reset higher, if the account stays standard.",
  steps=["Teaser-rate housing loan → 2.00%", "One year after reset (if standard) → 0.40%"],
  why="0.25% is for individual housing, farm and SME loans; 0.40% is the general rate (and the rate after reversion); "
      "1.00% is for commercial real estate.",
  facts=[fact("The standard asset provisioning on the outstanding amount of housing loans at teaser rates ... shall be "
              "2.00 per cent ... The provisioning on these assets shall revert to 0.40 per cent after one year from "
              "the date on which the rates are reset at higher rates if the accounts remain 'standard'", A_IRAC)])
Q("009", "A-NPA09-02", T, "Classification", "Basic",
  "Under RBI's IRACP Directions, 2025, how often must collateral such as immovable property charged to the bank be "
  "valued in the case of NPAs with a balance of ₹5 crore and above?",
  ["Once in three years", "Every year", "Once in five years", "Every six months"],
  concept="Valuation of collateral of large NPAs",
  explanation="For NPAs with a balance of ₹5 crore and above, collateral such as immovable properties charged to the "
              "bank must be valued once in three years by valuers appointed under Board-approved guidelines.",
  steps=["NPA ≥ ₹5 crore", "Collateral valuation → once in three years"],
  why="Annual intervals apply to the stock audit of such NPAs, not to collateral valuation; five years and six months "
      "are not the prescribed periods.",
  facts=[fact("In cases of NPAs with balance of ₹5 crore and above, collateral such as immovable properties charged in "
              "favour of the bank shall be valued once in three years by valuers appointed as per the guidelines "
              "approved by the Board of Directors", A_IRAC)])
Q("009", "A-NPA09-03", T, "Resolution and IBC", "Basic",
  "Under RBI's Resolution of Stressed Assets Directions, 2025, banks must submit a weekly report of instances of "
  "default by all borrowers with aggregate exposure of ₹5 crore and above. By when is this report due?",
  ["By close of business every Friday (or the preceding working day if Friday is a holiday)",
   "By close of business every Monday", "Within seven days of each default",
   "On the last working day of each month"],
  concept="Weekly reporting of defaults to CRILC",
  explanation="Besides monthly CRILC reporting of credit information (including SMA status) on borrowers with "
              "aggregate exposure of ₹5 crore and above, banks submit a weekly report of defaults by all such "
              "borrowers by close of business every Friday, or the preceding working day if Friday is a holiday.",
  steps=["Large borrowers (≥ ₹5 crore)", "Weekly default report → close of business every Friday"],
  why="Monday, a seven-day rolling window and month-end are not the stated timing; the monthly cycle is for CRILC "
      "credit information, not the weekly default report.",
  facts=[fact("A bank shall submit a weekly report of instances of default by all borrowers (with aggregate exposure "
              "of ₹5 crore and above) by close of business on every Friday, or the preceding working day if Friday "
              "happens to be a holiday", A_RSA)])
Q("009", "A-NPA09-04", T, "Classification", "Intermediate",
  "For loans sanctioned on or after 31 December 2021, RBI's IRACP Directions, 2025 require certain details to be "
  "clearly specified in the loan agreement. Which of the following is among them?",
  ["Examples of the dates on which the account would be classified as SMA or NPA",
   "The realisable value of the security at each future balance sheet date",
   "The provision the bank will make if the account becomes doubtful",
   "The name of the asset reconstruction company to which the loan may be sold"],
  concept="Borrower awareness of SMA/NPA dates",
  explanation="The loan agreement must clearly specify the exact due dates for repayment, the frequency of repayment, "
              "the break-up between principal and interest, examples of dates of SMA/NPA classification, and (for "
              "loans with a moratorium) the exact date of commencement of repayment. The borrower must be told of "
              "these at sanction and at later changes.",
  steps=["Due dates, frequency, principal/interest break-up", "Examples of SMA/NPA dates",
         "Repayment start date where there is a moratorium"],
  why="Future security values, provisioning plans and potential ARC buyers are not required contents of the "
      "agreement.",
  facts=[fact("The exact due dates for repayment of a loan, frequency of repayment, breakup between principal and "
              "interest, examples of dates of classification as special mention account (SMA) / non-performing asset "
              "(NPA), etc. shall be clearly specified in the loan agreement", A_IRAC)])

_pf = {"CRE": (400, 1.25), "CRE-RH": (200, 1.00), "Infra (all others, operational)": (500, 0.40)}
assert abs(sum(a * r / 100 for a, r in _pf.values()) - 9.0) < 1e-9
assert abs(400 * 1.00 / 100 + 200 * 0.75 / 100 + 500 * 0.40 / 100 - 7.5) < 1e-9     # all at operational rates
assert abs(400 * 1.25 / 100 + 200 * 1.00 / 100 + 500 * 1.00 / 100 - 12.0) < 1e-9    # all at construction rates
Q("009", "A-NPA09-05", T, "Classification", "Advanced",
  "A bank's standard project finance book (all projects reached financial closure after 1 October 2025) has: a "
  "commercial real estate (CRE) project under construction, ₹400 crore; a CRE–residential housing (CRE-RH) project "
  "under construction, ₹200 crore; and an infrastructure project in its operational phase (repaying interest and "
  "principal), ₹500 crore. Under RBI's IRACP Directions, 2025, what general provision must it hold on these?",
  ["₹9.0 crore", "₹7.5 crore", "₹12.0 crore", "₹8.0 crore"],
  concept="General provisions on project finance",
  explanation="Project finance attracts portfolio-level general provisions by phase: construction phase – CRE 1.25%, "
              "CRE-RH 1.00%, all others 1.00%; operational phase – CRE 1.00%, CRE-RH 0.75%, all others 0.40%. So: 400 "
              "× 1.25% = 5.0; 200 × 1.00% = 2.0; 500 × 0.40% = 2.0; total ₹9.0 crore.",
  steps=["CRE (construction): 1.25% × 400 = ₹5.0 crore", "CRE-RH (construction): 1.00% × 200 = ₹2.0 crore",
         "Infrastructure (operational): 0.40% × 500 = ₹2.0 crore", "Total = ₹9.0 crore"],
  why="₹7.5 crore applies operational-phase rates throughout; ₹12.0 crore applies construction-phase rates "
      "throughout; ₹8.0 crore uses 0.50% for CRE-RH, which is not a prescribed rate.",
  computed=True,
  facts=[fact("For project finance exposures, a bank shall maintain a general provision at the following rates ... "
              "Construction Phase / Operational Phase: CRE 1.25 1.00; CRE-RH 1.00 0.75; All others 1.00 0.40", A_IRAC),
         fact("The provisions stipulated ... shall not be applicable for projects where financial closure has been "
              "achieved as on October 1, 2025", A_IRAC)])
Q("009", "A-NPA09-06", T, "Classification", "Advanced",
  "Consider the following statements under RBI's IRACP Directions, 2025:\nI. When a loan is taken over by another "
  "bank, the taking-over bank must classify it as NPA from the actual date on which it became NPA, even though it was "
  "not in its books on that date.\nII. If a bank's on-lending facility to a Primary Agricultural Credit Society is in "
  "default, all direct loans by the bank to that society's member-borrowers also become NPA.\nIII. If overdues from "
  "a client's forward contract with the bank become NPA, all other funded facilities of that client are also "
  "classified as NPA.\nWhich of the above are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="Special cases of asset classification",
  explanation="Under takeout finance, the taking-over bank classifies the asset as NPA from the actual date of it "
              "becoming NPA. For PACS/FSS on-lending, only the particular facility to the PACS that is in default is "
              "NPA; direct loans to a member outside the on-lending arrangement become NPA only if one of that "
              "member's own facilities becomes NPA. Overdues from forward contracts, swaps and options that become NPA "
              "drag all other funded facilities of the client into NPA (borrower-wise classification).",
  steps=["I: correct (takeout finance)", "II: wrong (PACS default does not by itself make members' direct loans NPA)",
         "III: correct (borrower-wise principle for derivatives)"],
  why="Options including II are wrong; II overstates the PACS rule.",
  facts=[fact("Subsequent to take over by a bank, the taking over bank shall classify the asset as NPA from the actual "
              "date of it becoming NPA even though the account was not in its books as on that date", A_IRAC),
         fact("only that particular credit facility granted to PACS / FSS which is in default ... The other direct "
              "loans and advances, if any, granted by the bank to the member borrower of a PACS / FSS outside the "
              "on-lending arrangement shall become NPA even if one of the credit facilities granted to the same "
              "borrower becomes NPA", A_IRAC),
         fact("In case the overdues arising from forward contracts and plain vanilla swaps and options become NPAs, "
              "all other funded facilities granted to the client shall also be classified as NPA", A_IRAC)])

Q("009", "A-NPA09-07", T, "Resolution and IBC", "Advanced",
  "A borrower's account (lenders' aggregate exposure ₹700 crore at implementation) was restructured and has performed "
  "satisfactorily through the monitoring period. To support an upgrade, the borrower obtains normal bank-loan ratings "
  "from three RBI-accredited rating agencies: BBB, BBB- and BB+. Under RBI's Resolution of Stressed Assets "
  "Directions, 2025, can the account be upgraded?",
  ["No; when more ratings than required are obtained, all must be investment grade (BBB- or better), and BB+ is not",
   "Yes; two investment-grade ratings are required and the borrower has two",
   "Yes; only one investment-grade rating is needed for exposures above ₹500 crore",
   "No; upgrade needs an independent credit evaluation of RP1, not ratings"],
  concept="Upgrade of restructured large accounts",
  explanation="For accounts with aggregate exposure of ₹100 crore and above, an upgrade needs, besides satisfactory "
              "performance, investment-grade ratings (BBB- or better) of the credit facilities: two ratings for ₹500 "
              "crore and above, one below that. If more ratings than required are obtained, all of them must be "
              "investment grade. These are normal ratings, not the ICE used for implementing plans. Here BB+ is below "
              "investment grade, so the account cannot be upgraded.",
  steps=["₹700 crore → two ratings required", "Three obtained → all must be ≥ BBB-", "BB+ fails → no upgrade"],
  why="Having two good ratings is not enough once a third is obtained; above ₹500 crore two ratings are needed; ICE "
      "symbols apply to implementing plans, not upgrade.",
  facts=[fact("for accounts where the aggregate exposure of specified lenders is ₹100 crore and above ... the credit "
              "facilities of the borrower shall also be rated as investment grade (BBB- or better) ... accounts with "
              "aggregate exposure of ₹500 crore and above shall require two ratings, those below ₹500 crore shall "
              "require one rating", A_RSA),
         fact("if the ratings are obtained from more than the required number of credit rating agencies, all such "
              "ratings shall be investment grade for the account to qualify for an upgrade ... These ratings ... shall "
              "be the normal ratings provided by the credit rating agencies and not Independent Credit Evaluation",
              A_RSA)])

# ---- batch 010: Basic 4, Intermediate 2, Advanced 1
Q("010", "A-NPA10-01", T, "Classification", "Basic",
  "Where do commercial banks show the provisions held against standard assets in their balance sheet, according to "
  "RBI's IRACP Directions, 2025?",
  ["Separately, as 'Contingent Provisions against Standard Assets' under 'Other Liabilities and Provisions – Others'",
   "Netted from gross advances, like provisions on NPAs",
   "As part of the Interest Suspense Account", "Deducted from gross NPAs to arrive at net NPAs"],
  concept="Presentation of standard asset provisions",
  explanation="Standard asset provisions are not netted from gross advances and are not reckoned for arriving at net "
              "NPAs; they are shown separately as 'Contingent Provisions against Standard Assets' under 'Other "
              "Liabilities and Provisions – Others' in Schedule 5 of the balance sheet.",
  steps=["Not netted from advances", "Not used for net NPA", "Shown in Schedule 5 as contingent provisions"],
  why="The Directions expressly bar netting them from gross advances or using them for net NPAs; interest suspense is "
      "a different account.",
  facts=[fact("The provisions towards standard assets need not be netted from gross advances but shown separately as "
              "'Contingent Provisions against Standard Assets' under 'Other Liabilities and Provisions Others' in "
              "Schedule 5 of the balance sheet", A_IRAC),
         fact("The provisions on standard assets shall not be reckoned for arriving at net NPAs", A_IRAC)])
Q("010", "A-NPA10-02", T, "Classification", "Basic",
  "Under RBI's IRACP Directions, 2025, overdue receivables representing the positive mark-to-market value of a "
  "derivative contract are classified as NPA if they remain unpaid for how long from the specified due date?",
  ["90 days", "30 days", "60 days", "180 days"],
  concept="NPA norm for derivative receivables",
  explanation="In respect of derivative transactions, overdue receivables representing positive mark-to-market value "
              "become NPA if they remain unpaid for 90 days from the specified due date for payment.",
  steps=["Positive MTM receivable overdue", "Unpaid 90 days from due date → NPA"],
  why="30 and 60 days mark SMA stages; 180 days is the limit for reviewing credit limits.",
  facts=[fact("in respect of derivative transactions, the overdue receivables representing positive mark-to-market "
              "value of a derivative contract, remain unpaid for a period of 90 days from the specified due date for "
              "payment", A_IRAC)])
Q("010", "A-NPA10-03", T, "Resolution and IBC", "Basic",
  "A bank acquires a borrower's immovable property in satisfaction of its claims (a 'specified non-financial asset', "
  "SNFA). Under RBI's Resolution of Stressed Assets Directions, 2025, the bank's policy must set a maximum period for "
  "its disposal not exceeding:",
  ["Seven years", "One year", "Three years", "Ten years"],
  concept="Disposal of specified non-financial assets",
  explanation="An SNFA is an immovable asset acquired by a bank in full or part satisfaction of its claims, including "
              "non-banking assets. The bank's policy must cover the limit on SNFAs as a share of total assets, "
              "eligibility, delegation, recovery efforts before acquisition and a maximum disposal period not "
              "exceeding seven years.",
  steps=["SNFA = immovable asset taken over in satisfaction of claims", "Policy: disposal within ≤ 7 years"],
  why="One, three and ten years are not the ceiling in the Directions.",
  facts=[fact("'specified non-financial asset' (SNFA) means an immovable asset acquired by a bank in satisfaction or "
              "part satisfaction of its claims on the borrower", A_RSA),
         fact("Such provisions shall specify inter-alia the limit on SNFAs as a share of total assets, eligibility "
              "criteria, delegation matrix, recovery efforts to be explored before acquisition and maximum period for "
              "disposal not exceeding seven years", A_RSA)])
Q("010", "A-NPA10-04", T, "SARFAESI", "Basic",
  "Under Section 31 of the SARFAESI Act, 2002, a secured creditor cannot use the Act's enforcement provisions where the "
  "amount due is less than what share of the principal amount and interest?",
  ["20 per cent", "10 per cent", "25 per cent", "50 per cent"],
  concept="Exclusions under Section 31 of the SARFAESI Act",
  explanation="Section 31(j) excludes cases where the amount due is less than 20% of the principal amount and interest "
              "thereon; such dues must be recovered through other routes such as the DRT. Section 31(i) separately "
              "excludes security interest created in agricultural land.",
  steps=["Section 31 lists cases where SARFAESI does not apply", "Clause (j): amount due < 20% of principal and "
         "interest"],
  why="10%, 25% and 50% are not the threshold in Section 31(j).",
  facts=[fact("Section 31(j): the Act does not apply where the amount due is less than twenty per cent of the principal "
              "amount and interest thereon", A_SARF1),
         fact("SARFAESI proceedings can be initiated only if the outstanding due payable by the borrower is more than "
              "20% of principal and interest", A_SARF2)])
Q("010", "A-NPA10-05", T, "Classification", "Intermediate",
  "Under RBI's IRACP Directions, 2025, a bank must normally classify assets through an automated system. If, "
  "exceptionally, a manual intervention overrides the system classification, what is required?",
  ["At least two-level authorisation, with logs of the override stored for at least three years",
   "Approval of the statutory auditor, with logs kept for one year",
   "Prior approval of RBI for each override",
   "A single authorisation by the branch manager, with no logs required"],
  concept="Exceptions to automated asset classification",
  explanation="Manual intervention is to be avoided; where it is unavoidable it needs at least two-level "
              "authorisation under the Board-approved delegation, and logs (date and time stamp, reason, user IDs, "
              "names, designations and account details) must be stored for at least three years without tampering.",
  steps=["Override only in exceptional cases", "≥ two-level authorisation", "Logs retained ≥ three years"],
  why="Auditor approval, RBI approval per case and single authorisation without logs are not the rule.",
  facts=[fact("In any exceptional circumstance where manual intervention is required to override the System "
              "classification, it shall have at least two level authorisation", A_IRAC),
         fact("These logs shall also be stored for a minimum period of three years and not be tampered with", A_IRAC)])
Q("010", "A-NPA10-06", T, "SARFAESI", "Intermediate",
  "An official of an asset reconstruction company (ARC) was part of the committee that approved the acquisition of a "
  "financial asset. According to RBI's FAQs on ARCs (September 2026), what role can that official play when a "
  "settlement proposal for the same asset comes up?",
  ["None; the official cannot be part of processing or approving the settlement in any capacity",
   "The official may approve it if the settlement is above the acquisition price",
   "The official may process it but not approve it",
   "The official may approve it with the Board's prior consent"],
  concept="Segregation of duties in ARCs",
  explanation="To segregate acquisition and settlement, any official who was part of the acquisition of a financial "
              "asset (individually or in a committee) shall not be part of either processing or approving the "
              "settlement proposal for that asset, in any capacity.",
  steps=["Acquisition and settlement must be segregated", "Acquiring official → no role in settlement"],
  why="No exception exists for price, a processing-only role or Board consent.",
  facts=[fact("any official who was part of the acquisition (as an individual or part of a committee) of the "
              "concerned financial asset shall not be part of either processing or approving the proposal for "
              "settlement of the same financial asset, in any capacity", A_ARC)])
Q("010", "A-NPA10-07", T, "Classification", "Advanced",
  "Consider the following statements under RBI's IRACP Directions, 2025:\nI. Specific provisions that a bank "
  "voluntarily makes on NPAs at rates higher than the regulatory minimum are treated as floating provisions.\nII. Such "
  "additional provisions on NPAs may be netted off from gross NPAs to arrive at net NPAs.\nIII. Floating provisions "
  "cannot be reversed by credit to the profit and loss account.\nIV. Amounts held in the Interest Suspense Account "
  "are reckoned as part of provisions.\nWhich of the above are correct?",
  ["II and III only", "I and II only", "II, III and IV only", "I, III and IV only"],
  concept="Additional provisions, floating provisions and interest suspense",
  explanation="Voluntary higher provisions on NPAs (Board-approved and consistently applied) are not floating "
              "provisions, and like the regulatory minimum they may be netted from gross NPAs. Floating provisions "
              "can only be used for specific provisions in extraordinary circumstances and are never reversed to "
              "P&L. Interest suspense balances are not provisions; they are deducted from the advance before "
              "provisioning.",
  steps=["I: wrong (not floating provisions)", "II: correct", "III: correct", "IV: wrong (not part of provisions)"],
  why="Options containing I or IV are wrong.",
  facts=[fact("Such additional provisions shall not be considered as floating provisions. The additional provisions "
              "for NPAs, like the minimum regulatory provision on NPAs, may be netted off from gross NPAs to arrive at "
              "the net NPAs", A_IRAC),
         fact("Floating provisions shall not be reversed by credit to the profit and loss account", A_IRAC),
         fact("Amounts held in Interest Suspense Account shall not be reckoned as part of provisions", A_IRAC)])


# ---------------------------------------------------------------- Priority Sector Lending
T = "Priority Sector Lending"
# ---- batch 008: Basic 4, Intermediate 1, Advanced 1
Q("008", "A-PSL08-01", T, "Targets and sub-targets", "Basic",
  "Under RBI's PSL Directions, 2025, overdrafts given to Pradhan Mantri Jan-Dhan Yojana (PMJDY) account holders, "
  "within the limits and conditions set by the Department of Financial Services, are classified as lending to:",
  ["Micro Enterprises", "Agriculture", "Social Infrastructure", "Housing"],
  concept="PMJDY overdraft under PSL",
  explanation="The Directions list overdrafts to PMJDY account holders (as per DFS limits and conditions) among other "
              "loans eligible under the MSME category, to be categorised as lending to Micro Enterprises.",
  steps=["PMJDY OD → MSME category → Micro Enterprises"],
  why="The Directions place it under Micro Enterprises, not agriculture, social infrastructure or housing.",
  facts=[fact("Overdraft to Pradhan Mantri Jan-Dhan Yojana (PMJDY) account holders as per limits and conditions "
              "prescribed by Department of Financial Services, Ministry of Finance from time to time, which shall be "
              "categorised as lending to Micro Enterprises", A_PSL)])
Q("008", "A-PSL08-02", T, "Targets and sub-targets", "Basic",
  "Bank credit to NHB-approved Housing Finance Companies for on-lending for individual dwelling units qualifies as "
  "priority sector (Housing) under RBI's PSL Directions, 2025 subject to an aggregate loan limit per borrower of:",
  ["₹20 lakh", "₹10 lakh", "₹35 lakh", "₹50 lakh"],
  concept="On-lending through HFCs",
  explanation="Bank credit to HFCs approved by NHB for refinance, for on-lending for purchase/construction/"
              "reconstruction of individual dwelling units or slum clearance and rehabilitation, is PSL under "
              "'Housing' subject to an aggregate loan limit of ₹20 lakh per borrower.",
  steps=["HFC on-lending for housing → ₹20 lakh per borrower"],
  why="₹10 lakh is the agriculture term-lending limit for NBFC on-lending; ₹35 lakh and ₹50 lakh are not this limit.",
  facts=[fact("Bank credit to Housing Finance Companies (HFCs), approved by NHB for their refinance, for on-lending "
              "for the purpose of purchase/construction/reconstruction of individual dwelling units ... subject to an "
              "aggregate loan limit of ₹20 lakh per borrower, under 'Housing' category", A_PSL)])
Q("008", "A-PSL08-03", T, "Targets and sub-targets", "Basic",
  "Under the 'Others' category of RBI's PSL Directions, 2025, bank loans to Self Help Groups or Joint Liability "
  "Groups for purposes other than agriculture or MSME (such as social needs or house repair) qualify up to:",
  ["₹2 lakh", "₹1 lakh", "₹10 lakh", "₹50,000"],
  concept="PSL 'Others' category",
  explanation="Loans not exceeding ₹2.00 lakh by banks to SHGs/JLGs for activities other than agriculture or MSME — "
              "for social needs, construction or repair of houses, construction of toilets or any viable common "
              "activity — qualify under 'Others'.",
  steps=["SHG/JLG loan, non-agri non-MSME purpose", "Limit ₹2 lakh"],
  why="₹1 lakh is the limit for loans to distressed persons; ₹10 lakh and ₹50,000 are not limits for this item.",
  facts=[fact("Loans not exceeding ₹2.00 lakh provided by banks to SHG/JLG for activities other than agriculture or "
              "MSME, viz., loans for meeting social needs, construction or repair of house, construction of toilets or "
              "any viable common activity started by SHGs", A_PSL)])
Q("008", "A-PSL08-04", T, "PSLCs", "Basic",
  "According to RBI's PSL FAQs (September 2026), to which RBI department does a bank apply to get registered for "
  "trading Priority Sector Lending Certificates?",
  ["Financial Inclusion and Development Department, Central Office", "Department of Payment and Settlement Systems",
   "Department of Supervision", "Foreign Exchange Department"],
  concept="Registration for PSLC trading",
  explanation="Banks request registration from RBI's Financial Inclusion and Development Department, Central Office, "
              "submitting their DEA Fund code, customer identification number and RBI current account number.",
  steps=["Apply to FIDD, CO, RBI", "Give DEA Fund code, CIN, RBI current account number"],
  why="PSL, and hence PSLC registration, is handled by FIDD, not the payments, supervision or forex departments.",
  facts=[fact("The banks are required to submit a request to Financial Inclusion and Development Department, Central "
              "Office, RBI ... to obtain registration for PSLC trading by submitting a) DEA Fund Code b) Customer "
              "identification number and c) RBI Current Account number", A_PSLFAQ)])
Q("008", "A-PSL08-05", T, "Targets and sub-targets", "Intermediate",
  "Bank loans of up to ₹12 crore per borrower for building health care facilities qualify as priority sector under "
  "'Social Infrastructure'. For commercial banks, in which centres must such facilities be located?",
  ["Tier II to Tier VI centres", "Only Tier I centres", "Tier IV to Tier VI centres only",
   "Any centre, without restriction"],
  concept="Social infrastructure under PSL",
  explanation="Social infrastructure covers loans up to ₹8 crore per borrower for schools, drinking water and "
              "sanitation facilities, and loans up to ₹12 crore per borrower for building health care facilities in "
              "Tier II to Tier VI centres.",
  steps=["Health care facility loan ≤ ₹12 crore", "Location: Tier II–VI centres"],
  why="Tier I centres are excluded, so 'only Tier I' and 'any centre' are wrong; Tier IV–VI is too narrow.",
  facts=[fact("Loans up to a limit of ₹12 crore per borrower for building health care facilities in Tier II to Tier "
              "VI centres", A_PSL),
         fact("Loans up to a limit of ₹8 crore per borrower for setting up schools, drinking water facilities and "
              "sanitation facilities", A_PSL)])

_anbc = 20000
assert (0.60 * _anbc, 0.075 * _anbc, 0.12 * _anbc) == (12000, 1500, 2400)
Q("008", "A-PSL08-06", T, "Targets and sub-targets", "Advanced",
  "A Small Finance Bank's ANBC on the relevant date is ₹20,000 crore, higher than its CEOBSE. Under RBI's PSL "
  "Directions, 2025, what are its overall PSL target, micro enterprises sub-target and weaker sections sub-target?",
  ["₹12,000 crore; ₹1,500 crore; ₹2,400 crore", "₹8,000 crore; ₹1,500 crore; ₹2,400 crore",
   "₹15,000 crore; ₹1,500 crore; ₹3,000 crore", "₹12,000 crore; ₹1,600 crore; ₹2,400 crore"],
  concept="Computing SFB PSL targets",
  explanation="SFBs: total PSL 60%, micro enterprises 7.5%, weaker sections 12% of ANBC or CEOBSE, whichever is "
              "higher. 60% × 20,000 = 12,000; 7.5% × 20,000 = 1,500; 12% × 20,000 = 2,400 (₹ crore).",
  steps=["Base = ANBC ₹20,000 crore (higher)", "Total 60% → ₹12,000 crore", "Micro 7.5% → ₹1,500 crore",
         "Weaker sections 12% → ₹2,400 crore"],
  why="₹8,000 crore uses the 40% target of commercial banks; ₹15,000/₹3,000 crore use RRB rates (75%, 15%); ₹1,600 "
      "crore uses 8% for micro enterprises.",
  computed=True,
  facts=[fact("Small Finance Banks: Total Priority Sector [60] per cent of ANBC ... or CEOBSE, whichever is higher; "
              "Micro Enterprises 7.5 per cent; Advances to Weaker Sections 12 percent", A_PSL)])

# ---- batch 009: Basic 2, Intermediate 4, Advanced 1
Q("009", "A-PSL09-01", T, "Targets and sub-targets", "Basic",
  "Loans to distressed persons (other than distressed farmers) to prepay their debt to non-institutional lenders "
  "qualify as priority sector under RBI's PSL Directions, 2025 up to what amount per borrower?",
  ["₹1 lakh", "₹2 lakh", "₹50,000", "₹5 lakh"],
  concept="Loans to distressed persons",
  explanation="Loans to distressed persons, other than distressed farmers indebted to non-institutional lenders, of "
              "up to ₹1.00 lakh per borrower to prepay their debt to non-institutional lenders qualify under 'Others' "
              "and also count under weaker sections.",
  steps=["Distressed non-farmer borrower", "Prepay non-institutional debt", "Limit ₹1 lakh"],
  why="₹2 lakh is the limit for SHG/JLG social-needs loans and individual women beneficiaries; ₹50,000 and ₹5 lakh "
      "are not limits for this item.",
  facts=[fact("Loans to distressed persons [other than distressed farmers indebted to non-institutional lenders] not "
              "exceeding ₹1.00 lakh per borrower to prepay their debt to non-institutional lenders", A_PSL)])
Q("009", "A-PSL09-02", T, "Targets and sub-targets", "Basic",
  "Under RBI's PSL Directions, 2025, loans to start-ups that conform to the definition of MSME qualify under the MSME "
  "category up to:",
  ["₹50 crore", "₹25 crore", "₹10 crore", "₹100 crore"],
  concept="Start-up loans under PSL",
  explanation="Loans up to ₹50 crore to start-ups that conform to the MSME definition qualify under MSME. The same ₹50 "
              "crore limit applies to start-ups in agriculture and allied services and to start-ups under 'Others'.",
  steps=["Start-up conforming to MSME definition", "Limit ₹50 crore"],
  why="₹10 crore is the FPO limit; ₹100 crore the cap for agriculture infrastructure and food processing; ₹25 crore "
      "is not a start-up limit.",
  facts=[fact("Loans up to ₹50 crore to Start-ups, that conform to the definition of MSME, shall also be eligible to "
              "be classified under this category", A_PSL)])
Q("009", "A-PSL09-03", T, "Targets and sub-targets", "Intermediate",
  "A farmers' producer company directly engaged in agriculture takes loans against pledge of its produce for nine "
  "months. Under RBI's PSL Directions, 2025, up to what amounts do such loans qualify as farm credit?",
  ["₹4 crore against NWRs/eNWRs and ₹2.5 crore against other warehouse receipts",
   "₹90 lakh against NWRs/eNWRs and ₹75 lakh against other warehouse receipts",
   "₹2.5 crore against NWRs/eNWRs and ₹4 crore against other warehouse receipts",
   "₹10 crore against any kind of warehouse receipt"],
  concept="Pledge loans to corporate farmers and FPOs",
  explanation="For corporate farmers, FPOs/FPCs, partnership firms and co-operatives of farmers, loans against pledge "
              "or hypothecation of agricultural produce for up to 12 months qualify up to ₹4 crore against negotiable "
              "warehouse receipts (NWR/eNWR) and up to ₹2.5 crore against other warehouse receipts.",
  steps=["Entity borrower (FPC), pledge ≤ 12 months", "NWR/eNWR → ₹4 crore", "Other receipts → ₹2.5 crore"],
  why="₹90 lakh is the eNWR limit for individual farmers; the third option reverses the limits; ₹10 crore is the "
      "limit for FPO loans with assured marketing, not pledge loans.",
  facts=[fact("Loans up to ₹4 crore against pledge/hypothecation of agricultural produce (including warehouse "
              "receipts) for a period not exceeding 12 months against NWRs/eNWRs and up to ₹2.5 crore against "
              "warehouse receipts other than NWRs/eNWRs", A_PSL)])
Q("009", "A-PSL09-04", T, "Targets and sub-targets", "Intermediate",
  "Loans to Farmer Producer Organisations/Companies of individual farmers count towards the Small and Marginal Farmers "
  "(SMF) sub-target under RBI's PSL Directions, 2025 when the land-holding share of SMFs in the FPO is at least:",
  ["75 per cent", "51 per cent", "60 per cent", "90 per cent"],
  concept="FPO loans under the SMF sub-target",
  explanation="SMFs include loans to FPOs/FPCs of individual farmers and co-operatives of farmers directly engaged in "
              "agriculture and allied activities where the land-holding share of SMFs is not less than 75%, subject to "
              "the farm-credit loan limits.",
  steps=["FPO/co-operative of farmers", "SMF land-holding share ≥ 75% → SMF category"],
  why="51%, 60% and 90% are not the threshold in the Directions.",
  facts=[fact("Loans to FPOs/FPCs of individual farmers and co-operatives of farmers directly engaged in agriculture "
              "and allied activities where the land-holding share of SMFs is not less than 75 per cent", A_PSL)])
Q("009", "A-PSL09-05", T, "Targets and sub-targets", "Intermediate",
  "RBI's PSL Directions (as updated) allow bank credit to the National Co-operative Development Corporation (NCDC) for "
  "on-lending to co-operative societies to be classified as priority sector. Which condition applies?",
  ["NCDC must give the lending banks quarterly certificates from a CAG-empanelled chartered accountant firm confirming "
   "the use of the credit",
   "The loans must be guaranteed by the Government of India",
   "Only RRBs may lend to NCDC for this purpose",
   "The credit counts only if NCDC lends to individual farmers directly"],
  concept="On-lending through NCDC",
  explanation="Bank credit to NCDC for on-lending to co-operative societies for eligible purposes counts under the "
              "respective PSL categories, subject to NCDC furnishing quarterly certificates by a CAG-empanelled "
              "chartered accountant firm confirming how the credit was used. The provision applies to loans sanctioned "
              "after 19 January 2026.",
  steps=["Bank → NCDC → co-operative societies", "Quarterly certificate from CAG-empanelled CA firm",
         "Applies to loans sanctioned after 19 January 2026"],
  why="No Government guarantee or RRB-only rule is prescribed, and the on-lending is to co-operative societies.",
  current=ca("2026-01-19"),
  facts=[fact("Bank credit to National Co-operative Development Corporation (NCDC) for on-lending to co-operative "
              "societies ... will be eligible for classification as priority sector lending ... subject to NCDC "
              "furnishing quarterly certificates by a CAG empanelled chartered accountant firm, to the lending banks, "
              "confirming that the bank credit has been utilize[d]", A_PSL),
         fact("The provisions of para 24A are applicable to loans sanctioned by banks to NCDC after January 19, 2026",
              A_PSL)])
Q("009", "A-PSL09-06", T, "Targets and sub-targets", "Intermediate",
  "According to RBI's PSL FAQs (September 2026), what is the correct position on classifying loans under 'Weaker "
  "Sections'?",
  ["The loan must first qualify under one of the eight PSL categories; a customer's declaration suffices for the "
   "Minority/SC/ST status",
   "Any loan to a borrower from the listed groups qualifies, whatever its purpose",
   "The bank must obtain a caste or community certificate for every SC/ST/Minority borrower",
   "Weaker sections loans need not satisfy any PSL category since they form a separate target"],
  concept="Weaker sections classification",
  explanation="For classification under weaker sections, loans should first be eligible under any of the eight PSL "
              "categories as per the underlying activity. A declaration by the customer in the application form is "
              "enough to classify credit to Minorities/SCs/STs under weaker sections.",
  steps=["Step 1: eligible PSL activity", "Step 2: borrower in a weaker-section group (declaration enough for "
         "Minority/SC/ST)"],
  why="Group membership alone is not enough; certificates are not required; weaker sections is a sub-target within "
      "PSL, not outside it.",
  facts=[fact("For classification under 'Weaker Sections', the loans should first be eligible for classification "
              "under any of the eight PSL categories as per underlying activity", A_PSLFAQ),
         fact("Declaration by the customer in the application form would suffice for classifying credit facilities "
              "to Minorities/SCs/STs under Weaker Sections", A_PSLFAQ)])
Q("009", "A-PSL09-07", T, "Targets and sub-targets", "Advanced",
  "Consider the following statements about the co-lending model (CLM) between banks and NBFCs for priority sector "
  "loans, based on RBI's PSL FAQs (September 2026):\nI. If the bank can exercise its discretion on taking the "
  "NBFC-originated loans into its books, the arrangement is akin to a direct assignment transaction.\nII. If the "
  "agreement entails a prior, irrevocable commitment by the bank to take its share of each loan, the arrangement is "
  "also akin to a direct assignment transaction.\nIII. The bilateral Master Agreement may cap the number and amount of "
  "loans the NBFC can originate under the CLM.\nWhich of the above are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="Co-lending: discretion versus commitment",
  explanation="RBI's FAQs say only an arrangement in which the bank can exercise discretion over taking the loans is "
              "akin to direct assignment; a prior, irrevocable commitment is not. The Master Agreement governs the "
              "arrangement and may specify a cap on the number and amount of loans.",
  steps=["I: correct", "II: wrong (irrevocable commitment ≠ direct assignment)", "III: correct"],
  why="Options containing II are wrong.",
  facts=[fact("Only if the bank can exercise its discretion regarding taking into its books the loans originated by "
              "NBFC as per the agreement, the arrangement will be akin to a direct assignment transaction. If the "
              "Agreement entails a prior, irrevocable commitment ... it shall not be akin to direct assignment "
              "transaction", A_PSLFAQ),
         fact("The agreement may specify any cap on the number and amount of loans that can be originated by the NBFC "
              "under the Co-lending model", A_PSLFAQ)])

# ---- batch 010: Basic 1, Intermediate 3, Advanced 2
Q("010", "A-PSL10-01", T, "Targets and sub-targets", "Basic",
  "Under RBI's PSL Directions, 2025, loans to individuals solely engaged in allied activities (with no land holding) "
  "count towards the Small and Marginal Farmers sub-target up to:",
  ["₹2.5 lakh", "₹1.6 lakh", "₹5 lakh", "₹10 lakh"],
  concept="SMF category without land-holding criteria",
  explanation="SMFs include loans up to ₹2.5 lakh to individuals solely engaged in allied activities, without any "
              "accompanying land-holding criterion.",
  steps=["Allied activity, no land", "Up to ₹2.5 lakh → SMF"],
  why="₹1.6 lakh, ₹5 lakh and ₹10 lakh are not the limit in this clause.",
  facts=[fact("Loans up to ₹2.5 lakh to individuals solely engaged in allied activities without any accompanying land "
              "holding criteria", A_PSL)])
Q("010", "A-PSL10-02", T, "PSLCs", "Intermediate",
  "A domestic bank has met its overall PSL target but is short of its Micro Enterprises sub-target. Under RBI's PSLC "
  "guidelines in the PSL Directions, 2025, which certificate must it buy to cover this shortfall?",
  ["PSLC – Micro Enterprises", "PSLC – General", "PSLC – Agriculture", "PSLC – SF/MF"],
  concept="Matching PSLC type to the shortfall",
  explanation="PSLC – Micro Enterprises counts towards the micro enterprises sub-target and the overall target. A bank "
              "short of a specific sub-target must buy the specific PSLC; PSLC – General counts only towards the "
              "overall target, and the agriculture and SF/MF certificates count towards farm targets.",
  steps=["Shortfall in micro sub-target", "Buy the specific PSLC → PSLC – Micro Enterprises"],
  why="PSLC – General counts only for the overall target; agriculture and SF/MF certificates do not count for micro "
      "enterprises.",
  facts=[fact("PSLC - Micro Enterprises All PSL Loans to Micro Enterprises Achievement of micro-enterprise sub-target "
              "and overall PSL target; PSLC - General ... Achievement of overall PSL target", A_PSL),
         fact("a bank having shortfall in achievement of any sub-target (e.g. SF/MF, Micro), will have to buy the "
              "specific PSLC to achieve the target", A_PSL)])
Q("010", "A-PSL10-03", T, "Targets and sub-targets", "Intermediate",
  "A bank has purchased bills drawn under a letter of credit (payment to the beneficiary not under reserve). For "
  "computing 'bank credit in India' and ANBC for PSL, what do RBI's PSL FAQs say?",
  ["They must not be excluded from bank credit in India; if the advance is PSL-eligible it can be classified as PSL",
   "They are excluded as inter-bank exposure, since the LC-issuing bank bears the risk",
   "They are excluded from bank credit but may still be counted as PSL achievement",
   "They count only if the LC-issuing bank is a scheduled commercial bank"],
  concept="LC-backed bills in ANBC",
  explanation="Such bills may be treated as inter-bank exposure only for computing exposure and capital requirements. "
              "They amount to bank credit to the borrower and must not be excluded from 'bank credit in India'; if "
              "the advance is eligible, the bank can classify it as PSL.",
  steps=["Inter-bank treatment only for exposure/capital", "Remains in bank credit in India / ANBC",
         "PSL if eligible"],
  why="Exclusion from bank credit is not allowed; there is no condition about the type of LC-issuing bank.",
  facts=[fact("The bills purchased/ discounted/ negotiated (payment to beneficiary not under reserve) under LC is "
              "allowed to be treated as interbank exposure only for the limited purpose of computing exposure and "
              "capital requirements. It should not be excluded from the computation of 'bank credit in India' ... If "
              "this advance is eligible for priority sector classification, the bank can classify it as PSL", A_PSLFAQ)])
Q("010", "A-PSL10-04", T, "Targets and sub-targets", "Intermediate",
  "Under a co-lending arrangement between a bank and an NBFC for priority sector loans, RBI's PSL FAQs explain what "
  "'back-to-back basis' means. Which statement is correct?",
  ["The NBFC first opens the loan accounts, and the bank opens its share of the loan accounts subsequently",
   "The bank first opens the loan accounts, and the NBFC follows",
   "Both open and fund their loan accounts simultaneously on a single date",
   "The NBFC retains 100% of the risk on the bank's share"],
  concept="Co-lending model (CLM) mechanics",
  explanation="RBI clarified that back-to-back basis implies the loans are first opened by the NBFC and then the bank "
              "opens its loan accounts. It also said that PSL assets on the bank's books must at all times be without "
              "recourse to the NBFC.",
  steps=["NBFC opens first", "Bank opens its share after", "Bank's PSL assets: no recourse to NBFC"],
  why="The order is NBFC first; simultaneous opening is not what back-to-back means; the NBFC cannot carry the bank's "
      "risk, as the bank's PSL assets must be without recourse.",
  facts=[fact("Back-to-back basis implies that the loans will be first opened by NBFC and then bank will open loan "
              "accounts subsequently", A_PSLFAQ),
         fact("the priority sector assets on the bank's books should at all times be without recourse to the NBFC",
              A_PSLFAQ)])

# export credit: domestic bank: incremental, ≤ 2% of ANBC, sanction ≤ ₹50 crore per borrower;
# foreign bank with 20+ branches: incremental, ≤ 2% of ANBC, no per-borrower cap
_dom = min(3200 - 600, 0.02 * 150000)
_for = min(900, 0.02 * 50000)
assert (_dom, _for) == (2600, 900)
assert min(3200, 0.02 * 150000) == 3000 and min(900 - 300, 0.02 * 50000) == 600
Q("010", "A-PSL10-05", T, "Targets and sub-targets", "Advanced",
  "Bank D (domestic, ANBC ₹1,50,000 crore) has incremental export credit of ₹3,200 crore over the corresponding date "
  "of the previous year, of which ₹600 crore is to borrowers with sanctioned limits above ₹50 crore. Bank F (a foreign "
  "bank with 25 branches, ANBC ₹50,000 crore) has incremental export credit of ₹900 crore, of which ₹300 crore is to "
  "borrowers with sanctioned limits above ₹50 crore. ANBC is higher than CEOBSE for both, and none of this credit is "
  "to agriculture or MSMEs. How much export credit can each classify as priority sector?",
  ["D: ₹2,600 crore; F: ₹900 crore", "D: ₹3,000 crore; F: ₹900 crore", "D: ₹2,600 crore; F: ₹600 crore",
   "D: ₹3,000 crore; F: ₹600 crore"],
  concept="Export credit under PSL",
  explanation="Domestic banks may count incremental export credit up to 2% of ANBC, with a sanctioned limit of up to "
              "₹50 crore per borrower: (3,200 − 600) = 2,600, below 2% × 1,50,000 = 3,000, so ₹2,600 crore. Foreign "
              "banks with 20 or more branches may count incremental export credit up to 2% of ANBC without the "
              "per-borrower cap: 900, below 2% × 50,000 = 1,000, so ₹900 crore.",
  steps=["D: exclude large-sanction borrowers → 2,600; cap 3,000 → ₹2,600 crore",
         "F: no per-borrower cap → 900; cap 1,000 → ₹900 crore"],
  why="₹3,000 crore for D ignores the ₹50 crore sanction limit; ₹600 crore for F wrongly applies that limit to a "
      "foreign bank with 20+ branches.",
  computed=True,
  facts=[fact("Domestic banks/WoS of Foreign banks/SFBs/UCBs: Incremental export credit over corresponding date of the "
              "preceding year, up to 2 per cent of ANBC or CEOBSE whichever is higher, subject to a sanctioned limit "
              "of up to ₹50 crore per borrower. Foreign banks with 20 branches and above: Incremental export credit "
              "over corresponding date of the preceding year, up to 2 percent of ANBC or CEOBSE whichever is higher",
              A_PSL)])

# PSLC bought on 15 July counts on reporting dates 30 Sep, 31 Dec, 31 Mar; annual shortfall = average of quarters
_ach = [37, 38, 38, 39]
_with = [a + (1 if i > 0 else 0) for i, a in enumerate(_ach)]       # ₹100 crore on ANBC ₹10,000 crore = 1 pp
_sf = sum(max(40 - a, 0) for a in _with) / 4
assert _sf == 1.25 and sum(40 - a for a in _ach) / 4 == 2.0 and sum(max(40 - a - 1, 0) for a in _ach) / 4 == 1.0
Q("010", "A-PSL10-06", T, "PSLCs", "Advanced",
  "A domestic bank's ANBC (higher than CEOBSE) is ₹10,000 crore for all four quarters of a year, and its PSL target is "
  "40%. Its own priority sector lending equals 37%, 38%, 38% and 39% of ANBC on the four quarterly reporting dates (30 "
  "June, 30 September, 31 December, 31 March). On 15 July it buys a PSLC – General of ₹100 crore. Following RBI's "
  "illustration on when a purchased PSLC is reckoned, and RBI's method for the annual shortfall, what is the bank's "
  "shortfall for the year?",
  ["1.25 percentage points", "2.00 percentage points", "1.00 percentage point", "0.25 percentage point"],
  concept="Timing of PSLC reckoning and the annual shortfall",
  explanation="A PSLC bought on 15 July is reckoned on the reporting dates of 30 September, 31 December and 31 March "
              "(not 30 June). ₹100 crore is 1% of ANBC, so achievements become 37, 39, 39 and 40%; quarterly "
              "shortfalls are 3, 1, 1 and 0. The year's shortfall is their simple average: 5 ÷ 4 = 1.25 percentage "
              "points.",
  steps=["PSLC (1 pp) counts in Q2, Q3, Q4 only", "Achievement: 37, 39, 39, 40",
         "Shortfalls: 3, 1, 1, 0 → average 1.25 pp"],
  why="2.00 ignores the PSLC; 1.00 counts it in the June quarter too; 0.25 takes only the last quarter's position.",
  computed=True,
  facts=[fact("Bank A may sell PSLCs with a nominal value of ₹100 crores to Bank B on July 15, 2025. Bank B will reckon "
              "₹100 crore towards its priority sector achievement as on the reporting dates of September 30, 2025, "
              "December 31, 2025 & March 31, 2026", A_PSL),
         fact("The shortfall/ excess for the year is arrived at by taking a simple average of the shortfall/excess for "
              "all the four quarters", A_PSLFAQ)])


# ---------------------------------------------------------------- Financial Inclusion
T = "Financial Inclusion"
# ---- batch 008: Basic 3, Intermediate 4, Advanced 2
Q("008", "A-FI08-01", T, "Business correspondents", "Basic",
  "Under RBI's Branch Authorisation Directions, 2025, in what language must each retail outlet or sub-agent of a "
  "Business Correspondent post the sign indicating its status as a service provider for the bank?",
  ["The local (vernacular) language", "English only", "Hindi and English only", "Any language chosen by the BC"],
  concept="BC outlet signage",
  explanation="Each retail outlet/sub-agent must post a sign in the local (vernacular) language indicating its status "
              "as a service provider for the bank, and disclose the BC's name, the telephone number and e-mail of the "
              "base Banking Outlet/controlling office, the Banking Ombudsman and the fees for all services.",
  steps=["Signage in local language", "Shows BC name, bank contacts, Ombudsman, fees"],
  why="The Directions require the local language, not English or Hindi only or a language of the BC's choice.",
  facts=[fact("Each retail outlet / sub-agent shall post a sign in local language (vernacular) indicating their status "
              "as service providers for the bank as also disclose the name of the BC, the telephone number, email id "
              "of the base Banking Outlet / controlling office of the bank and the Banking Ombudsman and the fees for "
              "all services available at the outlet", A_BRANCH)])
Q("008", "A-FI08-02", T, "PMJDY and allied schemes", "Basic",
  "According to the Government's note on 12 years of Pradhan Mantri Jan Dhan Yojana (August 2026), which of the "
  "following is true of PM-JDY accounts?",
  ["A joint account can also be opened", "Only individuals aged 18 to 60 can open one",
   "A minimum balance of ₹500 must be maintained", "They can be opened only at bank branches, not at BC outlets"],
  concept="Features of PM-JDY accounts",
  explanation="The note says all Indian citizens are eligible with no upper age limit, no minimum balance is needed, "
              "accounts can be opened at a bank branch or a Business Correspondent (Bank Mitra) outlet, and a joint "
              "account can also be opened.",
  steps=["No upper age limit", "No minimum balance", "Branch or Bank Mitra outlet", "Joint account allowed"],
  why="There is no 18–60 age band, no minimum balance and no branch-only rule.",
  facts=[fact("Under PM-JDY, individuals can open an account by visiting a bank branch or Business Correspondent/ "
              "Bank Mitra outlet ... A joint account can also be opened", A_PMJDY12),
         fact("All citizens of Indian nationality are eligible to open PM-JDY accounts, with no upper age limit ... "
              "There is no requirement to maintain any minimum balance", A_PMJDY12)])
Q("008", "A-FI08-03", T, "Business correspondents", "Basic",
  "Under RBI's Branch Authorisation Directions, 2025, which of the following is NOT treated as a 'Banking Outlet'?",
  ["A mobile branch", "An extension counter that meets the four-hours, five-days definition",
   "A fixed-point unit manned by a Business Correspondent that meets the definition",
   "An ultra small branch that meets the definition"],
  concept="What counts as a Banking Outlet",
  explanation="Extension counters, satellite offices, part-shifted branches, ultra small branches and specialised "
              "branches count as Banking Outlets (or part-time outlets) if they meet the definition. ATMs, e-lobbies, "
              "bunch note acceptor machines, cash deposit machines, e-kiosks and mobile branches are not Banking "
              "Outlets.",
  steps=["Mobile branches, ATMs, CDMs, e-kiosks → not outlets", "Extension counters, USBs, BC fixed points meeting "
         "the definition → outlets"],
  why="The other three are expressly counted when they satisfy the definition.",
  facts=[fact("ATMs, E- lobbies, Bunch Note Acceptor Machines (BNAM), Cash Deposit Machines (CDM), E- Kiosks and "
              "Mobile Branches will not be treated as 'Banking Outlets'", A_BRANCH),
         fact("Extension Counters, Satellite Offices, Part-shifted Branches, Ultra Small Branches and Specialised "
              "Branches, subject to their satisfying the definition given above, shall be treated as independent "
              "'Banking Outlets' or 'Part-time Banking Outlets'", A_BRANCH)])
Q("008", "A-FI08-04", T, "Business correspondents", "Intermediate",
  "A bank sets up a Central Processing Centre that processes loans, verifies documents and issues cheque books and "
  "demand drafts on requests from its outlets. Under RBI's Branch Authorisation Directions, 2025, it is a:",
  ["Back Office, which is not permitted direct interface with customers",
   "Banking Outlet, since it carries out banking functions",
   "Part-time Banking Outlet", "Digital Banking Unit"],
  concept="Back offices versus banking outlets",
  explanation="A 'Back Office' is a CPC or office that exclusively handles functions such as data processing, loan "
              "processing, verification of documents and issue of cheque books and demand drafts on requests from "
              "other Banking Outlets. Direct interface with customers is not permitted.",
  steps=["Processes requests from other outlets", "No customer interface → Back Office"],
  why="It does not serve customers at a fixed point for deposits, withdrawals or lending, so it is not an outlet of "
      "either kind; a DBU is a customer-facing digital hub.",
  facts=[fact("'Back Office(s)' means a Central Processing Centre (CPC) or an Office ... that exclusively attends to "
              "functions such as data processing, processing of loans, verification and processing of documents, "
              "issuance of cheque books, demand drafts etc. on requests received from other Banking Outlets ... Direct "
              "interface with customers is not permitted", A_BRANCH)])
Q("008", "A-FI08-05", T, "Business correspondents", "Intermediate",
  "Which of the following can a scheduled commercial bank engage as a Business Correspondent under RBI's Branch "
  "Authorisation Directions, 2025?",
  ["A payments bank", "A deposit-taking NBFC", "An asset reconstruction company", "A chit fund company"],
  concept="Eligible Business Correspondents",
  explanation="Eligible BCs include specified individuals, NGOs/MFIs under Societies/Trust Acts and Section 8 "
              "companies, co-operative societies, post offices, payments banks, companies (other than NBFCs) with "
              "large and widespread retail outlets, and non-deposit-taking NBFCs subject to safeguards.",
  steps=["Listed: payments banks, post offices, co-operatives, NGOs/MFIs, retail companies, NBFC-ND",
         "Not listed: deposit-taking NBFCs, ARCs, chit funds"],
  why="Only non-deposit-taking NBFCs are allowed; ARCs and chit fund companies are not in the list.",
  facts=[fact("A bank may engage the following individuals / entities as BCs: ... (4) Post Offices (5) Payments Bank; "
              "and (6) Companies [other than Non-Banking Financial Companies (NBFCs)] ... (7) Non-deposit taking NBFCs "
              "(NBFCs-ND)", A_BRANCH)])
Q("008", "A-FI08-06", T, "PMJDY and allied schemes", "Intermediate",
  "A person holds two savings accounts, each with a RuPay debit card, and both are PMJDY-type accounts. According to "
  "SBI's FAQs on PMJDY, how does the free accidental insurance cover attached to RuPay cards apply?",
  ["It is available in only one account", "It is available separately on each card",
   "It doubles to ₹4 lakh because of the two cards", "It is lost on both cards because of the duplication"],
  concept="RuPay card accident insurance under PMJDY",
  explanation="SBI's FAQs say that where a person has two or more accounts and RuPay debit cards, the accidental "
              "insurance cover is available only in one account.",
  steps=["Multiple RuPay cards → cover in one account only"],
  why="The cover is neither multiplied nor forfeited; it is limited to one account.",
  facts=[fact("If someone has two or more accounts and two or more RuPay Debit Cards, whether accidental insurance cove "
              "is available in each account / each card? ANS : Accidental insurance cover is available only in one "
              "account", A_SBIJDY)])
Q("008", "A-FI08-07", T, "Business correspondents", "Intermediate",
  "Before engaging a Business Correspondent, a bank must carry out due diligence. Which of the following is NOT one "
  "of the aspects RBI's Branch Authorisation Directions, 2025 say this may cover?",
  ["The BC's holding of a licence from the State Government as a moneylender",
   "Reputation and market standing", "Cash handling ability",
   "Ability to implement technology solutions in rendering financial services"],
  concept="Due diligence on BCs",
  explanation="The due diligence may cover reputation/market standing, financial soundness, management and corporate "
              "governance, cash handling ability and ability to implement technology solutions. A moneylender licence "
              "is not among them.",
  steps=["Listed: reputation, financial soundness, governance, cash handling, technology"],
  why="The other three are named in the Directions.",
  facts=[fact("The due diligence exercise may, inter alia, cover aspects such as (i) reputation / market standing, "
              "(ii) financial soundness, (iii) management and corporate governance, (iv) cash handling ability and (v) "
              "ability to implement technology solutions in rendering financial services", A_BRANCH)])

# Unbanked Rural Centre norm: >= 25% of outlets opened in a year in URCs; part-time outlets pro rata
# (hours counted per day capped at 4, over a 20-hour week)
def _pt(hours, days):
    return min(hours, 4) * days / 20


_den = 120 + 3 * _pt(5, 4)
_num = 26 + 3 * _pt(5, 4)
assert abs(_pt(5, 4) - 0.8) < 1e-9 and abs(_den - 122.4) < 1e-9 and abs(_num - 28.4) < 1e-9
assert round(100 * _num / _den, 1) == 23.2 and abs(0.25 * _den - 30.6) < 1e-9
Q("008", "A-FI08-08", T, "Business correspondents", "Advanced",
  "During a year a bank opens 120 full-time Banking Outlets, 26 of them in Unbanked Rural Centres (URCs). It also opens "
  "three part-time outlets in URCs, each working 5 hours a day on 4 days a week. Applying the pro-rata method in RBI's "
  "Branch Authorisation Directions, 2025, does the bank meet the norm for URCs?",
  ["No; URC outlets are 28.4 of 122.4 (about 23.2%), against the required 25% (30.6)",
   "Yes; URC outlets are 29 of 123 (about 23.6%), which rounds up to the norm",
   "No; URC outlets are 26 of 120 (about 21.7%), as part-time outlets are ignored",
   "Yes; URC outlets are 29 of 120 (about 24.2%), and the norm is 20%"],
  concept="25% Unbanked Rural Centre norm with part-time outlets",
  explanation="At least 25% of the Banking Outlets opened in a year must be in URCs. Part-time outlets count pro rata "
              "against a 20-hour week (4 hours × 5 days), with at most 4 hours a day counted, in both the numerator "
              "(if in a URC) and the denominator. Each part-time outlet = 4 × 4 ÷ 20 = 0.8. Denominator = 120 + 2.4 = "
              "122.4; numerator = 26 + 2.4 = 28.4, about 23.2%, below 25% (which would need 30.6).",
  steps=["Part-time outlet = min(5,4) × 4 ÷ 20 = 0.8; three → 2.4", "Total = 122.4; URC = 28.4",
         "28.4 ÷ 122.4 ≈ 23.2% < 25% → not met"],
  why="Part-time outlets count pro rata, not as whole outlets; they are not ignored; the norm is 25%, not 20%.",
  computed=True,
  facts=[fact("At least 25 percent of the total number of 'Banking Outlets' opened during a financial year shall be "
              "opened in Unbanked Rural Centres (URCs) ... A 'Part-time Banking Outlet', opened in any Centre, will be "
              "counted and added to the denominator as well as numerator on pro rata basis", A_BRANCH),
         fact("The prescribed period for Banking Outlet is 4 hours per day for 5 days (minimum of 20 hours spread over "
              "5 days) this will remain constant denominator ... a maximum of 4 hours per day will be counted",
              A_BRANCH)])
Q("008", "A-FI08-09", T, "PMJDY and allied schemes", "Advanced",
  "Consider the following statements based on SBI's FAQs on Pradhan Mantri Jan Dhan Yojana, which describe the basic "
  "savings bank deposit (BSBD) account under RBI guidelines:\nI. The holder of a BSBD account is not eligible to open "
  "another BSBD account in the same or any other bank.\nII. There is no upper limit on the balance in the account, "
  "and no initial deposit is required.\nIII. A cheque book cannot be issued in a PMJDY account.\nWhich of the above "
  "are correct?",
  ["I and II only", "I and III only", "II and III only", "I, II and III"],
  concept="Features of BSBD/PMJDY accounts",
  explanation="A BSBD holder cannot open another BSBD account in any bank and must declare this. There is no minimum "
              "or maximum balance and no initial deposit. Cheque books are available: 25 leaves a year free for "
              "branch-channel accounts, and on request for accounts opened at CSP outlets.",
  steps=["I: correct", "II: correct", "III: wrong (cheque books are issued)"],
  why="Any option containing III is wrong.",
  facts=[fact("The holder of a BSBD account shall not be eligible to open another BSBD account in the same bank or any "
              "other bank", A_SBIJDY),
         fact("Maximum balance amount ANS : No upper limit ... Whether initial deposit is required? ANS : No",
              A_SBIJDY),
         fact("Cheque book with 25 cheque leaves can be issued free of cost per year for accounts opened at branches. "
              "Accounts opened at CSP outlets would also be issued cheque book on request", A_SBIJDY)])


# ---- batch 009: Basic 1, Intermediate 3, Advanced 2
Q("009", "A-FI09-01", T, "Business correspondents", "Basic",
  "Does a scheduled commercial bank need RBI's permission in each case to open a Banking Outlet in a Tier 1 centre, "
  "under RBI's Branch Authorisation Directions, 2025?",
  ["No; banks have general permission to open Banking Outlets in Tier 1 to Tier 6 centres unless specifically "
   "restricted",
   "Yes; permission is needed for every outlet in Tier 1 and Tier 2 centres",
   "Yes; permission is needed for every outlet in any centre",
   "No, but only if the outlet is manned by a Business Correspondent"],
  concept="General permission for Banking Outlets",
  explanation="With financial inclusion as the overarching objective, a scheduled commercial bank may open Banking "
              "Outlets in Tier 1 to Tier 6 centres without RBI permission in each case, unless specifically "
              "restricted; a bank from which general permission has been withdrawn needs prior approval.",
  steps=["General permission: Tier 1–6", "Exception: bank whose general permission is withdrawn"],
  why="Case-by-case permission is not required in any tier, and the permission is not limited to BC-manned outlets.",
  facts=[fact("a scheduled commercial bank is permitted to open Banking Outlets in Tier 1 to Tier 6 centres without "
              "having the need to obtain permission from RBI in each case, unless otherwise specifically restricted",
              A_BRANCH)])
Q("009", "A-FI09-02", T, "Business correspondents", "Intermediate",
  "When RBI introduced the Business Correspondent model, banks could not collect any charges from customers for "
  "services delivered through BCs. According to RBI's discussion paper on engaging 'for-profit' companies as BCs, when "
  "were banks first allowed to collect reasonable service charges for such services?",
  ["November 2009", "January 2006", "April 2008", "September 2010"],
  concept="History of BC service charges",
  explanation="RBI's discussion paper records that, initially, banks were not allowed to collect charges for BC "
              "services; in November 2009 they were allowed to collect reasonable service charges from customers in a "
              "transparent manner under a Board-approved policy. (Today the bank, not the BC, may levy such charges.)",
  steps=["2006: BC model, no charges", "November 2009: reasonable, transparent charges allowed (bank)"],
  why="January 2006 is when the BC model began; April 2008 brought the base-branch rules; September 2010 widened the "
      "list of eligible BCs.",
  facts=[fact("Initially, banks were not allowed to collect any charges from the customers for providing services "
              "through BC ... Subsequently, banks were allowed in November 2009 to collect reasonable service charges "
              "from customers in a transparent manner under a Board-approved policy", A_BCDP)])
Q("009", "A-FI09-03", T, "PMJDY and allied schemes", "Intermediate",
  "According to SBI's FAQs on PMJDY, how did Pradhan Mantri Jan Dhan Yojana differ from the earlier Financial "
  "Inclusion Plan ('Swabhimaan')?",
  ["Swabhimaan focused on covering villages, whereas PMJDY covers rural and urban areas, aiming at every household/"
   "adult",
   "Swabhimaan covered only urban areas, whereas PMJDY covers only rural areas",
   "Swabhimaan offered overdrafts, whereas PMJDY offers none",
   "Swabhimaan was run by RBI, whereas PMJDY is run by NABARD"],
  concept="PMJDY versus Swabhimaan",
  explanation="SBI's FAQs explain that the earlier plan focused on coverage of villages, while PMJDY covers both rural "
              "and urban areas and extends banking to households and, after its extension, to every unbanked adult.",
  steps=["Swabhimaan → villages", "PMJDY → rural + urban, households/adults"],
  why="Swabhimaan was not urban-only; PMJDY does offer an overdraft; PMJDY is run by the Department of Financial "
      "Services, not NABARD.",
  facts=[fact("PMJDY focuses on coverage of 'every adults' as against the earlier plan which focused on coverage of "
              "villages. It focuses on coverage of rural as well as urban areas", A_SBIJDY)])
Q("009", "A-FI09-04", T, "Business correspondents", "Intermediate",
  "A bank uses its Business Correspondents for preliminary work in opening customer accounts. Under RBI's Branch "
  "Authorisation Directions, 2025, who is responsible for ensuring compliance with KYC and AML norms in the BC model?",
  ["The bank", "The Business Correspondent", "The base Banking Outlet's local Lead District Manager",
   "UIDAI, when Aadhaar is used"],
  concept="KYC responsibility in the BC model",
  explanation="KYC and AML procedures under RBI's KYC Directions must be followed in all cases. The bank may use the BC "
              "for preliminary account-opening work, but ensuring KYC/AML compliance under the BC model remains the "
              "bank's responsibility.",
  steps=["BC may do preliminary work", "KYC/AML compliance → bank's responsibility"],
  why="Responsibility is not shifted to the BC, the LDM or UIDAI.",
  facts=[fact("The bank may, if necessary, use the services of the BC for preliminary work relating to account opening "
              "formalities. However, ensuring compliance with KYC and AML norms under the BC model shall be the "
              "responsibility of the bank", A_BRANCH)])
Q("009", "A-FI09-05", T, "Business correspondents", "Advanced",
  "Consider the following statements about the history of the Business Correspondent model, as recorded in RBI's "
  "discussion paper on engaging 'for-profit' companies as BCs:\nI. Guidelines of April 2008 required every BC to be "
  "attached to a base branch, ordinarily within 15 km in rural, semi-urban and urban areas and 5 km in metropolitan "
  "centres.\nII. The Committee on Financial Inclusion (Chairman: Dr C. Rangarajan) observed that NBFCs engaged in "
  "micro finance could be recognised as BCs only for savings and remittance services.\nIII. From the start of the BC "
  "model in 2006, banks could levy service charges on customers for services rendered through BCs.\nWhich of the above "
  "are correct?",
  ["I and II only", "I and III only", "II and III only", "I, II and III"],
  concept="Evolution of the BC model",
  explanation="The April 2008 guideline attached each BC to a base branch, ordinarily within 15 km (rural, semi-urban, "
              "urban) or 5 km (metropolitan). The Rangarajan Committee observed that micro-finance NBFCs could be BCs "
              "only for savings and remittance services, where there is no conflict of interest. Charges were not "
              "allowed at first; reasonable charges were permitted only from November 2009.",
  steps=["I: correct", "II: correct", "III: wrong (charges allowed only from November 2009)"],
  why="Any option containing III is wrong.",
  facts=[fact("every BC is required to be attached to and be under the oversight of a specific bank branch designated "
              "as the base branch. This guideline was issued in April 2008 along with the stipulation that the "
              "distance ... should not exceed 15 kms in rural, semi-urban and urban areas and 5 kms in metropolitan "
              "centers", A_BCDP),
         fact("The Committee on Financial Inclusion (Chairman: Dr C. Rangarajan) had observed that NBFCs engaged in "
              "micro finance could be recognized as BCs of banks for providing only savings and remittance services",
              A_BCDP),
         fact("Initially, banks were not allowed to collect any charges ... Subsequently, banks were allowed in "
              "November 2009 to collect reasonable service charges", A_BCDP)])
Q("009", "A-FI09-06", T, "Business correspondents", "Advanced",
  "Consider the following statements about grievance redressal and social audit in the Business Correspondent model "
  "under RBI's Branch Authorisation Directions, 2025:\nI. As a measure of social audit, there could be periodic "
  "block-level meetings of the public with BCs and linked branch managers, which the Lead District Manager could "
  "attend.\nII. The bank must widely publicise the name and contact number of its designated Grievance Redressal "
  "Officer for complaints about BC services.\nIII. Complaints about services rendered by BCs are to be redressed by "
  "the BC company's own grievance machinery, not the bank's.\nWhich of the above are correct?",
  ["I and II only", "I and III only", "II and III only", "I, II and III"],
  concept="Grievance redressal for BC services",
  explanation="The Directions suggest periodic block-level meetings as social audit, which the LDM could attend to get "
              "feedback. Grievance redressal machinery for BC services must be constituted within the bank and "
              "publicised, with the designated officer's name and number made known. Statement III is wrong.",
  steps=["I: correct", "II: correct", "III: wrong (machinery is within the bank)"],
  why="Options containing III are wrong.",
  facts=[fact("As a measure of social audit, there could be periodic block level meetings where members of public are "
              "invited along with the BCs operating in the area as also the linked branch managers ... Lead District "
              "Manager (LDM) of the lead bank could attend such meetings", A_BRANCH),
         fact("Grievance Redressal Machinery shall be constituted within the bank for redressing complaints for "
              "services rendered by the BCs ... The name and contact number of designated Grievance Redressal Officer "
              "of the bank shall also be made known and widely publicised", A_BRANCH)])

# ---- batch 010: Basic 3, Intermediate 5, Advanced 4
Q("010", "A-FI10-01", T, "Business correspondents", "Basic",
  "For opening Banking Outlets, RBI classifies centres into tiers by 2011 Census population. A centre with a "
  "population of 75,000 falls in which tier?",
  ["Tier 2", "Tier 1", "Tier 3", "Tier 4"],
  concept="Tier-wise classification of centres",
  explanation="Tier 1: 1,00,000 and above; Tier 2: 50,000–99,999; Tier 3: 20,000–49,999; Tier 4: 10,000–19,999; "
              "Tier 5: 5,000–9,999; Tier 6: below 5,000. 75,000 is in Tier 2 (a semi-urban centre).",
  steps=["75,000 lies in 50,000–99,999 → Tier 2"],
  why="Tier 1 starts at 1 lakh; Tier 3 ends at 49,999; Tier 4 ends at 19,999.",
  facts=[fact("Tier 1 1,00,000 and above; Tier 2 50,000 to 99,999; Tier 3 20,000 to 49,999; Tier 4 10,000 to 19,999",
              A_BRANCH)])
Q("010", "A-FI10-02", T, "PMJDY and allied schemes", "Basic",
  "According to SBI's FAQs on Pradhan Mantri Jan-Dhan Yojana, what fee must a person pay to open a PMJDY account?",
  ["No fee", "₹100", "₹50 plus GST", "₹500 as an initial deposit"],
  concept="Opening a PMJDY account",
  explanation="SBI's FAQs say no fee is payable to open a PMJDY account, and no initial deposit is required.",
  steps=["Account opening fee → nil", "Initial deposit → not required"],
  why="No fee or initial deposit is charged.",
  facts=[fact("Do you have to pay some fee to open a Bank account under PMJDY? ANS : NO ... Whether initial deposit is "
              "required? ANS : No", A_SBIJDY)])
Q("010", "A-FI10-03", T, "PMJDY and allied schemes", "Basic",
  "According to SBI's FAQs on PMJDY, how is a PMJDY account opened at a Customer Service Point (Business "
  "Correspondent) outlet?",
  ["Through Aadhaar-based e-KYC", "Only with a passport and PAN card",
   "On a self-declaration without any identity verification", "Only after a visit to the base branch"],
  concept="Opening PMJDY accounts at BC outlets",
  explanation="At CSP outlets, PMJDY accounts are opened through Aadhaar-based e-KYC. At branches, Aadhaar alone is "
              "enough, or any one officially valid document if Aadhaar is not available.",
  steps=["CSP outlet → Aadhaar e-KYC"],
  why="No passport/PAN requirement exists; identity is verified; a branch visit is not required.",
  facts=[fact("At Customer Service Point outlets: Account under PMJDY is opened through e-KYC based on Aadhaar",
              A_SBIJDY)])
Q("010", "A-FI10-04", T, "Business correspondents", "Intermediate",
  "As a consumer protection measure under RBI's Branch Authorisation Directions, 2025, how should a Business "
  "Correspondent's retail outlet or sub-agent be introduced to the public?",
  ["Personally, by bank officials in a public meeting in the presence of village elders and government functionaries",
   "Through an advertisement issued by the BC company",
   "By an RBI notification listing all BC outlets",
   "By the Gram Panchayat alone, without bank officials"],
  concept="Introducing BC outlets to the public",
  explanation="To prevent misrepresentation or impersonation, the retail outlet/sub-agent must be personally introduced "
              "to the public by bank officials in the presence of village elders and government functionaries in a "
              "public meeting.",
  steps=["Bank officials introduce the BC", "Public meeting with village elders and officials"],
  why="An advertisement, an RBI list or a Panchayat-only introduction is not what the Directions require.",
  facts=[fact("The retail outlet / sub-agent of the BC shall be personally introduced to the members of public by the "
              "bank officials in the presence of village elders and government functionaries in a public meeting so "
              "that there is no misrepresentation / impersonation", A_BRANCH)])
Q("010", "A-FI10-05", T, "Business correspondents", "Intermediate",
  "Which of the following must a bank's arrangement with a Business Correspondent specify, under RBI's Branch "
  "Authorisation Directions, 2025?",
  ["Suitable limits on cash holding by the BC and on individual customer payments and receipts",
   "That the BC may introduce its own products once it informs the bank",
   "That financial services at the outlet may be tied to the sale of the BC company's products",
   "That the BC may charge customers a fee directly for services rendered for the bank"],
  concept="Terms of BC arrangements",
  explanation="Arrangements must specify limits on cash holding and on individual customer payments and receipts, issue "
              "of receipts on the bank's behalf, end-of-day accounting of off-line transactions and the bank's "
              "responsibility for the BC's acts. BCs cannot introduce products without the bank's approval, cannot "
              "tie services to their own products and cannot charge customers directly.",
  steps=["Required: cash-holding and transaction limits", "Prohibited: own products, tie-ins, direct fees"],
  why="The other three are expressly prohibited.",
  facts=[fact("Suitable limits on cash holding by intermediaries as also limits on individual customer payments and "
              "receipts", A_BRANCH),
         fact("the BC shall not introduce any product / process without the approval of the bank ... Financial "
              "services offered by the retail outlets / sub-agents of the BC shall not be tied to the sale of any "
              "product of such company", A_BRANCH)])
Q("010", "A-FI10-06", T, "PMJDY and allied schemes", "Intermediate",
  "According to SBI's FAQs on PMJDY (describing RBI's BSBD guidelines), how many free withdrawals, including ATM "
  "transactions, must a BSBD account get every month at a minimum, and how are UPI, NEFT or IMPS payments treated?",
  ["At least four; digital payments such as UPI, NEFT and IMPS are not counted as withdrawals",
   "At least four; every UPI, NEFT or IMPS payment counts as one withdrawal",
   "At least five; digital payments count as half a withdrawal",
   "Unlimited withdrawals at own-bank ATMs only"],
  concept="Free withdrawals in BSBD accounts",
  explanation="A BSBD account gets a minimum of four free withdrawals and ATM transactions (own or other banks' ATMs) a "
              "month. Digital payments other than ATM transactions — PoS, NEFT, RTGS, UPI, IMPS and so on — are not "
              "counted as withdrawals for this purpose.",
  steps=["Minimum four free withdrawals/ATM transactions a month", "Digital payments excluded from the count"],
  why="Digital payments are not counted; five, half-counting and own-ATM-only are not the rule.",
  facts=[fact("Minimum of four free withdrawals and ATM transactions (done either at the bank's own ATM or another "
              "bank's ATM), in a month. Digital payment transactions excluding ATM transactions, i.e., Point of Sale "
              "transfers, NEFT, RTGS, UPI, IMPS, etc., shall not be counted as withdrawals for this purpose",
              A_SBIJDY)])
Q("010", "A-FI10-07", T, "Business correspondents", "Intermediate",
  "In formulating their Business Correspondent schemes, banks are to be guided, among other things, by the "
  "recommendations in Chapter III of which report, according to RBI's Branch Authorisation Directions, 2025?",
  ["The Khan Group Report", "The Nachiket Mor Committee Report", "The Narasimham Committee Report",
   "The Damodaran Committee Report"],
  concept="Origins of the BC framework",
  explanation="The Directions say banks shall be guided by the recommendations in Chapter III of the Khan Group Report, "
              "along with RBI's Directions on managing risks in outsourcing, when formulating BC schemes.",
  steps=["BC schemes → Khan Group Report (Chapter III) + outsourcing Directions"],
  why="The Directions name only the Khan Group Report for this purpose; the other committees are not cited there.",
  facts=[fact("In formulating the schemes on BC, the bank shall, inter alia, be guided by the recommendations made in "
              "Chapter III of the Khan Group Report", A_BRANCH)])
Q("010", "A-FI10-08", T, "Business correspondents", "Intermediate",
  "How should transactions put through Business Correspondents normally be processed, under RBI's Branch "
  "Authorisation Directions, 2025?",
  ["Through ICT devices integrated with the bank's CBS, accounted for in real time, with immediate verification to "
   "the customer",
   "In a paper register at the BC outlet, posted to CBS weekly",
   "Through the BC company's own ledger, settled with the bank monthly",
   "Only at the base Banking Outlet, with the BC collecting forms"],
  concept="Technology in the BC model",
  explanation="Transactions should normally go through ICT devices (handheld devices or mobile phones) seamlessly "
              "integrated with the bank's Core Banking Solution, be accounted for in real time, and give customers "
              "immediate verification through the screen or a debit/credit slip.",
  steps=["ICT device linked to CBS", "Real-time accounting", "Immediate verification to customer"],
  why="Weekly posting, BC ledgers and branch-only processing are contrary to the real-time CBS requirement.",
  facts=[fact("The transactions shall normally be put through ICT devices (handheld device/mobile phone) that are "
              "seamlessly integrated to the Core Banking Solution (CBS) of the bank. The transactions shall be "
              "accounted for on a real time basis and the customers shall receive immediate verification of their "
              "transactions through visuals (screen based) or other means (debit or credit slip)", A_BRANCH)])


# RuPay accident cover: ₹1 lakh (accounts up to 28.8.2018), ₹2 lakh (opened later); needs a successful transaction
# within 90 days before the accident (SBI FAQ)
def _cover(opened_after_aug2018, days_since_txn):
    return 0 if days_since_txn > 90 else (2 if opened_after_aug2018 else 1)


assert (_cover(False, 40), _cover(True, 120), _cover(True, 10)) == (1, 0, 2)
Q("010", "A-FI10-09", T, "PMJDY and allied schemes", "Advanced",
  "Three PMJDY account holders with RuPay debit cards die in accidents. P opened her account in March 2017 and last "
  "used her card 40 days before the accident. Q opened his account in January 2020; his last transaction on any "
  "channel was 120 days before the accident. R opened his account in 2022 and made a balance enquiry at a CSP 10 days "
  "before the accident. Based on the Government's PM-JDY note and SBI's PMJDY FAQs, what accident insurance is "
  "payable?",
  ["P ₹1 lakh; Q nil; R ₹2 lakh", "P ₹2 lakh; Q ₹2 lakh; R ₹2 lakh", "P ₹1 lakh; Q ₹2 lakh; R ₹2 lakh",
   "P ₹1 lakh; Q nil; R nil"],
  concept="Conditions for the RuPay card accident cover",
  explanation="The cover is ₹1 lakh, enhanced to ₹2 lakh for new PMJDY accounts opened after August 2018. It is payable "
              "only if the cardholder made at least one successful financial or non-financial transaction on any "
              "channel within 90 days before the accident (including the accident date). P: old account, active → ₹1 "
              "lakh. Q: no transaction in 90 days → nil. R: new account; a balance enquiry is a non-financial "
              "transaction → ₹2 lakh.",
  steps=["P: opened before Aug 2018, active → ₹1 lakh", "Q: inactive for 120 days → nil",
         "R: opened after Aug 2018, non-financial transaction counts → ₹2 lakh"],
  why="Q fails the 90-day activity test; P's account predates the enhancement; R's balance enquiry counts.",
  computed=True,
  facts=[fact("Accident insurance cover of ₹1 lakh (enhanced to ₹2 lakhs to new PMJDY accounts opened after "
              "August2018) is available", A_PMJDY12),
         fact("Benefits of Insurance will be available to the Cardholders who have performed minimum one successful "
              "financial or non-financial transaction at any Channel ... within 90 days prior to date of accident "
              "including accident date for Rupay Cardholders", A_SBIJDY)])
Q("010", "A-FI10-10", T, "Business correspondents", "Advanced",
  "Consider the following statements about consumer protection in the Business Correspondent model under RBI's Branch "
  "Authorisation Directions, 2025:\nI. A BC may introduce a new product at its outlets without the bank's approval if "
  "it informs the base Banking Outlet.\nII. The charges for various services must be indicated in a brochure available "
  "at the retail outlets or with the sub-agents.\nIII. The bank must have a business continuity plan to ensure "
  "uninterrupted service if the agency arrangement with the BC is terminated.\nWhich of the above are correct?",
  ["II and III only", "I and II only", "I and III only", "I, II and III"],
  concept="Consumer protection safeguards for BCs",
  explanation="Products and processes must be approved by the bank and the BC cannot introduce any product or process "
              "without that approval. Charges must be shown in a brochure at the outlets, and the bank must have a "
              "business continuity plan for uninterrupted service if the BC arrangement ends.",
  steps=["I: wrong (bank approval needed)", "II: correct", "III: correct"],
  why="Options containing I are wrong.",
  facts=[fact("The products and processes shall be approved by the bank and the BC shall not introduce any product / "
              "process without the approval of the bank", A_BRANCH),
         fact("The charges for offering various services shall be indicated in a brochure and made available at the "
              "retail outlets / with the sub-agents ... The bank shall have necessary Business Continuity Plan (BCP) in "
              "place to ensure uninterrupted service in case the agency arrangement with the BCs / subagents is "
              "terminated", A_BRANCH)])
Q("010", "A-FI10-11", T, "Business correspondents", "Advanced",
  "Under RBI's Branch Authorisation Directions, 2025, banks may use Business Facilitators (BFs) and Business "
  "Correspondents (BCs). Consider the following statements:\nI. Post offices appear in both the list of BF "
  "intermediaries and the list of entities eligible as BCs.\nII. Krishi Vigyan Kendras are listed among the entities "
  "eligible to be engaged as BCs.\nIII. KVIC/KVIB units are listed among the intermediaries a bank may use under the BF "
  "model.\nWhich of the above are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="Business Facilitators versus Business Correspondents",
  explanation="The BF list includes NGOs/SHGs, farmers' clubs, co-operatives, community-based organisations, IT-enabled "
              "rural outlets of corporates, post offices, insurance agents, panchayats, village knowledge centres, "
              "agri-clinics, agri-business centres, Krishi Vigyan Kendras and KVIC/KVIB units. The BC list includes "
              "specified individuals, NGOs/MFIs, co-operative societies, post offices, payments banks, non-NBFC "
              "companies and NBFCs-ND — but not Krishi Vigyan Kendras.",
  steps=["I: post offices are in both lists → correct", "II: KVKs are in the BF list only → wrong",
         "III: KVIC/KVIB units are BF intermediaries → correct"],
  why="Options containing II are wrong.",
  facts=[fact("Under the 'Business Facilitator' model, a bank may use the services of intermediaries such as: ... (vi) "
              "Post Offices ... (xii) Krishi Vigyan Kendras (xiii) KVIC/KVIB units", A_BRANCH),
         fact("A bank may engage the following individuals / entities as BCs: (1) Individuals ... (2) NGOs / MFIs ... "
              "(3) Cooperative Societies ... (4) Post Offices (5) Payments Bank; and (6) Companies ... (7) Non-deposit "
              "taking NBFCs", A_BRANCH)])
Q("010", "A-FI10-12", T, "Business correspondents", "Advanced",
  "Consider the following statements about remuneration and oversight of Business Correspondents under RBI's Branch "
  "Authorisation Directions, 2025:\nI. The commission structure must be designed so that a mere increase in the number "
  "of clients or transaction volume does not drive the commission.\nII. The Board (or its delegated committee) must "
  "review the operations of BCs at least once every six months, with a view to tapering down pre-funding by BCs.\nIII. "
  "Pre-funding should ideally come down, within two years of a BC starting operations, to around 30% of the limits for "
  "deposits and 15% for bank guarantees.\nWhich of the above are correct?",
  ["I and II only", "I and III only", "II and III only", "I, II and III"],
  concept="BC commission and pre-funding",
  explanation="Commission must not be driven merely by the number of clients or transactions; remuneration combines "
              "fixed and variable parts linked to customer satisfaction. The Board or its committee reviews BC "
              "operations at least every six months so that pre-funding tapers down, ideally to around 15% of the "
              "limits for deposits and 30% for bank guarantees within two years. Statement III swaps these figures.",
  steps=["I: correct", "II: correct", "III: wrong (15% deposits, 30% guarantees)"],
  why="Options containing III are wrong because the percentages are reversed.",
  facts=[fact("Commission structure or incentive mechanism shall be devised in a manner that mere increase in the "
              "number of clients served or the transaction volume does not drive the commission", A_BRANCH),
         fact("The Board or any committee ... shall review the operations of BCs at least once every six months with a "
              "view to ensuring that requirement of prefunding ... should progressively taper down ... so as to reach "
              "around 15 percent of the limits fixed for each BC / CSP in case of deposits and 30 percent in case of "
              "Bank Guarantees, etc. in two years", A_BRANCH)])


# ####################################################################################################
# ===== Basel Norms, RBI Integrated Ombudsman Scheme, Digital Banking
# ####################################################################################################
# ===================================================================== part B: Basel Norms, RB-IOS, Digital Banking
# All sources below were opened (fetched with plain curl and read) on 2026-11-06.
B_ALM = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13147"   # CB - Asset Liability Management Directions, 2025
B_BIS3 = "https://www.bis.org/bcbs/basel3.htm"                                 # BIS: Basel III overview page
B_CCYB = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=62756"   # Review of CCyB, 18 May 2026
B_DSIB = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=61729"   # 2025 D-SIB list, 2 Dec 2025
B_IOS = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id=153"                # FAQs on RB-IOS, 2026 (Jul 1, 2026)
B_OSAR = "https://rbi.org.in/Scripts/PublicationsView.aspx?id=23441"           # Annual Report of Ombudsman Scheme 2024-25 (Dec 1, 2025)
B_DBC = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13163"   # CB - Digital Banking Channels Authorisation Directions, 2025
B_AUTH = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12898"  # Authentication mechanisms Directions, 2025
B_ERS = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id=169"                # Digital Rupee (e₹) FAQs (Oct 1, 2026)
B_DPSC = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13642"  # CB - Digital Payment Security Controls Directions, 2026

# ================= Basel Norms
T = "Basel Norms"
LCR, CAP = "LCR and NSFR", "Capital adequacy"

# ---- batch 008 (Basic 1, Intermediate 3, Advanced 2)
Q("008", "B-BAS08-01", T, LCR, "Basic",
  "Under RBI's Liquidity Coverage Ratio (LCR) framework, how are Level 1 assets counted in the stock of high-quality "
  "liquid assets (HQLA)?",
  ["Without any limit and without any haircut, at no more than their current market value",
   "Up to 60% of the stock of HQLA, after a 15% haircut",
   "Up to 40% of the stock of HQLA, without a haircut",
   "Without any limit, but after a uniform 50% haircut"],
  concept="Level 1 HQLA",
  explanation="RBI's Asset Liability Management Directions say Level 1 assets can be included in the stock of HQLA "
              "without any limit and without applying any haircut, valued at no more than current market value. (From "
              "1 April 2026, Level 1 government securities attract the LAF/MSF haircuts.) Caps of 40% and 15% and "
              "haircuts of 15% and 50% apply to Level 2A and Level 2B assets.",
  steps=["Level 1 → no cap, no haircut", "Level 2 → 40% cap; Level 2A 15% haircut; Level 2B 50% haircut and 15% cap"],
  why="The 15% and 50% haircuts and the 40% cap belong to Level 2 assets, not Level 1.",
  facts=[fact("Level 1 assets can be included in the stock of HQLA without any limit as also without applying any "
              "haircut and shall be valued at an amount not greater than their current market value", B_ALM)])

Q("008", "B-BAS08-02", T, LCR, "Intermediate",
  "Within its mandatory SLR holding, up to what share of its NDTL may a bank count government securities as Level 1 "
  "HQLA for the LCR, taking the MSF window and the Facility to Avail Liquidity for LCR (FALLCR) together?",
  ["18% of NDTL (2% under MSF and 16% under FALLCR)", "16% of NDTL (all under FALLCR)",
   "2% of NDTL (only under MSF)", "15% of NDTL (3% under MSF and 12% under FALLCR)"],
  concept="SLR carve-out for LCR",
  explanation="Level 1 assets include government securities within the mandatory SLR to the extent allowed by RBI "
              "under MSF, currently 2% of NDTL, and under FALLCR, currently 16% of NDTL, i.e. 18% of NDTL in all, "
              "besides securities held in excess of the SLR.",
  steps=["MSF: 2% of NDTL", "FALLCR: 16% of NDTL", "Total within SLR: 18% of NDTL"],
  shortcut="2 + 16 = 18.",
  why="16% and 2% are only one of the two windows; 3%/12% are not RBI's figures.",
  computed=True,
  facts=[fact("Within the mandatory SLR requirement, Government securities to the extent allowed by RBI under (a) MSF "
              "currently 2 per cent of a bank's Net Demand and Time Liabilities (NDTL), and (b) Facility to Avail "
              "Liquidity for Liquidity Coverage Ratio (FALLCR) currently 16 per cent of a bank's NDTL", B_ALM)])
assert 2 + 16 == 18

Q("008", "B-BAS08-03", T, LCR, "Intermediate",
  "A plain-vanilla bond of a non-financial company, rated 'A' by an eligible credit rating agency, trades in a deep "
  "and active market and meets RBI's price-stability test. How is it treated in a bank's stock of HQLA for the LCR?",
  ["As a Level 2B asset, with a minimum haircut of 50%", "As a Level 2A asset, with a minimum haircut of 15%",
   "As a Level 1 asset, with no haircut", "It cannot be included in HQLA at all"],
  concept="Rating bands for corporate bonds in HQLA",
  explanation="Corporate bonds rated AA- or above (not issued by a bank, FI or NBFC) are Level 2A assets with a 15% "
              "haircut. Corporate debt rated between A+ and BBB- that meets the market conditions is a Level 2B "
              "asset with a 50% haircut. An 'A' rated bond therefore falls in Level 2B.",
  steps=["AA- or above → Level 2A (15% haircut)", "A+ to BBB- → Level 2B (50% haircut)", "'A' → Level 2B"],
  why="Level 2A needs AA- or better; corporate bonds are never Level 1; an A-rated non-financial bond meeting the "
      "conditions is eligible.",
  facts=[fact("Level 2A: Corporate bonds rated AA- or above by an Eligible Credit Rating Agency (ECRA), and not issued "
              "by a bank / financial institution / NBFC; minimum 15 per cent haircut", B_ALM),
         fact("Level 2B: Corporate debt securities, including commercial paper, subject to a 50 per cent haircut ... "
              "have a long-term credit rating from an ECRA between A+ and BBB-", B_ALM)])

Q("008", "B-BAS08-04", T, LCR, "Intermediate",
  "In computing the LCR denominator (total net cash outflows over the next 30 days), up to what limit can a bank count "
  "its expected cash inflows?",
  ["Up to 75% of its total expected cash outflows", "Up to 50% of its total expected cash outflows",
   "Up to 100% of its total expected cash outflows", "Up to 25% of its stock of HQLA"],
  concept="Inflow cap in the LCR",
  explanation="Total net cash outflows = total expected cash outflows − Min(total expected cash inflows; 75% of total "
              "expected cash outflows). The cap ensures that a bank always holds HQLA of at least 25% of its "
              "outflows and does not rely only on expected inflows.",
  steps=["Net outflows = outflows − min(inflows, 0.75 × outflows)"],
  why="The cap is 75% of outflows, not 50% or 100%, and it is not linked to HQLA.",
  facts=[fact("Total Net Cash Outflows in the next 30 calendar days = total expected cash outflows - Min (total "
              "expected cash inflows; 75 per cent of total expected cash outflows)", B_ALM)])

l1, l2a, l2b = 400, 200 * 0.85, 300 * 0.50
adj15 = max(l2b - 15 / 85 * (l1 + l2a), l2b - 15 / 60 * l1, 0)
adj40 = max(l2a + l2b - adj15 - 2 / 3 * l1, 0)
hqla = l1 + l2a + l2b - adj15 - adj40
assert (l2a, l2b) == (170, 150) and abs(adj15 - 50) < 1e-9 and abs(hqla - 2000 / 3) < 1e-9
assert abs((l2a + l2b - adj15 - adj40) / hqla - 0.40) < 1e-9 and abs((l2b - adj15) / hqla - 0.15) < 1e-9
Q("008", "B-BAS08-05", T, LCR, "Advanced",
  "A bank holds Level 1 assets of ₹400 crore (already at their HQLA value), Level 2A assets with a market value of "
  "₹200 crore and Level 2B assets with a market value of ₹300 crore, with no short-term repo or reverse repo to unwind. "
  "Applying RBI's minimum haircuts and the 15% (Level 2B) and 40% (Level 2) caps, what is its stock of HQLA "
  "(approximately)?",
  ["₹666.7 crore", "₹720.0 crore", "₹670.0 crore", "₹900.0 crore"],
  concept="Stock of HQLA with haircuts and caps",
  explanation="Adjusted Level 2A = 85% × 200 = 170; adjusted Level 2B = 50% × 300 = 150. Adjustment for the 15% cap = "
              "max[150 − 15/85 × (400 + 170), 150 − 15/60 × 400, 0] = max[49.4, 50, 0] = 50. Adjustment for the 40% "
              "cap = max[(170 + 150 − 50) − 2/3 × 400, 0] = 270 − 266.7 = 3.3. Stock of HQLA = 400 + 170 + 150 − 50 − "
              "3.3 ≈ ₹666.7 crore. Check: Level 2 is then exactly 40% and Level 2B exactly 15% of the stock.",
  steps=["Haircuts: 2A → 170, 2B → 150", "15% cap adjustment = 50", "40% cap adjustment ≈ 3.3",
         "HQLA = 720 − 50 − 3.3 ≈ 666.7"],
  why="₹720 crore ignores both caps; ₹670 crore applies only the 15% cap; ₹900 crore ignores haircuts and caps.",
  computed=True,
  facts=[fact("Stock of HQLA = Level 1 + Level 2A + Level 2B - Adjustment for 15 per cent cap - Adjustment for 40 per "
              "cent cap; Adjustment for 15 per cent cap = Max [{Adjusted Level 2B - 15/85 * (Adjusted Level 1 + "
              "Adjusted Level 2A)}, {Adjusted Level 2B - 15/60 * Adjusted Level 1}, 0]; Adjustment for 40 per cent cap "
              "= Max {(Adjusted Level 2A + Adjusted Level 2B - Adjustment for 15 per cent cap) - 2/3 * (Adjusted Level "
              "1 assets), 0}", B_ALM),
         fact("A minimum 15 per cent haircut shall be applied to the current market value of each Level 2A asset; A "
              "minimum haircut of 50 per cent shall be applied to the current market value of each Level 2B asset",
              B_ALM)])

Q("008", "B-BAS08-06", T, LCR, "Advanced",
  "Consider the following assets of a bank, each meeting RBI's market-liquidity tests:\n"
  "I. Commercial paper issued by an NBFC, rated equivalent to AA+.\n"
  "II. Equity shares of a non-financial company included in the Nifty 50 index.\n"
  "III. A bond of a non-financial company rated BBB-.\n"
  "Which of them can be counted as Level 2B HQLA under RBI's LCR framework?",
  ["II and III only", "I and II only", "III only", "I, II and III"],
  concept="Eligibility of Level 2 assets",
  explanation="Level 2B includes common equity shares in the Nifty or Sensex not issued by a bank, FI or NBFC, and "
              "corporate debt rated between A+ and BBB- not issued by a bank, FI, PD or NBFC. Paper issued by an NBFC "
              "is excluded from both Level 2A and Level 2B, however highly rated, because of its wrong-way risk.",
  steps=["I: NBFC issuer → not HQLA", "II: Nifty share of non-financial firm → Level 2B", "III: BBB- corporate bond → "
         "Level 2B"],
  why="Statement I fails because instruments issued by NBFCs and other financial entities are excluded; II and III "
      "both qualify.",
  facts=[fact("Common Equity Shares which satisfy all of the following conditions: (a) not issued by a bank / "
              "financial institution / NBFC or any of its affiliated entities; (b) included in NSE CNX Nifty index and "
              "/ or S&P BSE Sensex index", B_ALM),
         fact("Commercial Papers, with a short-term rating equivalent to the long-term rating of AA- or above by an "
              "ECRA, and not issued by a bank / PD / financial institution or any of its affiliated entities; "
              "Corporate debt securities ... not issued by a bank / financial institution / primary dealer / NBFC ... "
              "long-term credit rating from an ECRA between A+ and BBB-", B_ALM)])

# ---- batch 009 (Basic 3, Intermediate 5, Advanced 4)
Q("009", "B-BAS09-01", T, LCR, "Basic",
  "Under RBI's Net Stable Funding Ratio (NSFR) rules, what Required Stable Funding (RSF) factor applies to a bank's "
  "coins and banknotes and its CRR balances with RBI?",
  ["0 per cent", "5 per cent", "50 per cent", "100 per cent"],
  concept="RSF factors",
  explanation="Coins and banknotes immediately available to meet obligations, CRR balances (required and excess) and "
              "claims on RBI with residual maturity under six months get a zero RSF factor: they need no stable "
              "funding.",
  steps=["Cash and CRR balances → 0% RSF"],
  why="5% applies to unencumbered Level 1 assets and SLR securities; 50% and 100% apply to less liquid assets.",
  facts=[fact("The following shall be assigned a zero per cent RSF factor: (1) Coins and banknotes immediately "
              "available to meet obligations; (2) CRR balances including required and excess reserves; and all claims "
              "on the RBI with residual maturities of less than six months", B_ALM)])

Q("009", "B-BAS09-02", T, LCR, "Basic",
  "Available Stable Funding (ASF) in the NSFR is the portion of a bank's capital and liabilities expected to be "
  "reliable over what time horizon?",
  ["One year", "30 calendar days", "Three months", "Five years"],
  concept="NSFR time horizon",
  explanation="RBI defines ASF as the portion of capital and liabilities expected to be reliable over the time horizon "
              "considered by the NSFR, which extends to one year. The LCR, by contrast, looks at a 30-day stress "
              "period.",
  steps=["NSFR → one-year horizon", "LCR → 30 days"],
  why="30 days is the LCR horizon; three months and five years are not used.",
  facts=[fact("ASF refers to the portion of capital and liabilities expected to be reliable over the time horizon "
              "considered by the NSFR, which extends to one year", B_ALM)])

Q("009", "B-BAS09-03", T, CAP, "Basic",
  "In RBI's 2025 list of Domestic Systemically Important Banks (D-SIBs), HDFC Bank is placed in which bucket, and what "
  "additional CET1 requirement applies to it?",
  ["Bucket 2; 0.40% of risk-weighted assets", "Bucket 3; 0.60% of risk-weighted assets",
   "Bucket 1; 0.20% of risk-weighted assets", "Bucket 4; 0.80% of risk-weighted assets"],
  concept="D-SIB buckets",
  explanation="RBI's list released on 2 December 2025 keeps the 2024 bucketing: SBI in bucket 4 (0.80%), HDFC Bank in "
              "bucket 2 (0.40%) and ICICI Bank in bucket 1 (0.20%). Buckets 3 and 5 are empty.",
  steps=["SBI → 4", "HDFC Bank → 2 (0.40%)", "ICICI Bank → 1"],
  why="Bucket 1 is ICICI Bank, bucket 4 is SBI, and bucket 3 has no bank.",
  current=ca("2025-12-02"),
  facts=[fact("Bucket 4 State Bank of India 0.80%; 3 - 0.60%; 2 HDFC Bank 0.40%; 1 ICICI Bank 0.20%", B_DSIB)])

Q("009", "B-BAS09-04", T, LCR, "Intermediate",
  "A bank under liquidity stress, having used all its other HQLA, draws funds under the Facility to Avail Liquidity "
  "for LCR (FALLCR). On what terms is this facility available?",
  ["At 200 bps above the LAF repo rate, availed or rolled over for up to 90 days",
   "At the repo rate itself, for up to 14 days", "At the Bank Rate, for up to one year",
   "At 100 bps above the SDF rate, for up to 30 days"],
  concept="FALLCR",
  explanation="FALLCR is available only under stress and after all other HQLA (including MSF-eligible securities) are "
              "used, with a declaration to that effect. It can be availed or rolled over for a maximum of 90 days, the "
              "securities attract MSF haircuts, and the rate is 200 bps above the prevailing LAF repo rate.",
  steps=["Only in stress, after exhausting other HQLA", "Tenor up to 90 days", "Rate: repo + 200 bps"],
  why="The other options give tenors and rates that RBI has not prescribed for FALLCR.",
  facts=[fact("Tenor: This facility can be availed / rolled over for a maximum period of 90 days ... Facility rate: "
              "The interest rate on the funds availed under this facility shall be 200 bps above the prevailing LAF "
              "repo rate, up to a period of 90 days", B_ALM)])

Q("009", "B-BAS09-05", T, LCR, "Intermediate",
  "A bond in a bank's stock of HQLA is downgraded and ceases to be an eligible liquid asset. Under RBI's LCR rules, "
  "what may the bank do?",
  ["Keep it in the stock of HQLA for an additional 30 calendar days to adjust or replace it",
   "Keep it in the stock until it matures", "Remove it from the stock on the same day",
   "Keep it for 90 days with RBI's prior approval"],
  concept="Grace period after loss of eligibility",
  explanation="RBI allows a bank to keep an asset that becomes ineligible (for example, after a downgrade) in its stock "
              "of liquid assets for an additional 30 calendar days, so that it has time to adjust its stock or "
              "replace the asset.",
  steps=["Asset becomes ineligible → 30 more calendar days in the stock"],
  why="There is neither an immediate removal rule nor a 90-day or till-maturity allowance.",
  facts=[fact("If an eligible liquid asset becomes ineligible (e.g. due to downgrade), a bank will be allowed to keep "
              "the asset in its stock of liquid assets for an additional 30 calendar days", B_ALM)])

Q("009", "B-BAS09-06", T, LCR, "Intermediate",
  "For the NSFR, what Available Stable Funding (ASF) factor applies to 'less stable' demand deposits and term "
  "deposits of under one year placed by retail and small business customers?",
  ["90 per cent", "95 per cent", "50 per cent", "100 per cent"],
  concept="ASF factors for retail deposits",
  explanation="Stable retail and SBC deposits (non-maturity or under one year) get a 95% ASF factor and less stable "
              "ones 90%. Short-term funding from non-financial corporates gets 50%, and capital and liabilities of one "
              "year or more get 100%.",
  steps=["Stable → 95%", "Less stable → 90%"],
  why="95% is for stable deposits; 50% for non-financial corporate funding under one year; 100% for capital and "
      "long-term liabilities.",
  facts=[fact("Liabilities receiving a 90 per cent ASF factor shall comprise of 'less stable' (as defined in chapter "
              "on LCR) non-maturity (demand) deposits and /or term deposits with residual maturities of less than one "
              "year, provided by retail and SBCs", B_ALM)])

Q("009", "B-BAS09-07", T, LCR, "Intermediate",
  "For the LCR, 'stable' retail deposits are insured deposits held in transactional or relationship accounts. When is "
  "an account treated as 'transactional'?",
  ["When the depositor's salary or pension is credited automatically, or bills are regularly paid from it under a "
   "registered mandate", "When the depositor has made at least one transaction in the last 30 days",
   "When the account is a current account of any business entity", "When the depositor uses a debit card on it"],
  concept="Stable deposits in the LCR",
  explanation="RBI treats an account as transactional if the depositor's salary or pension is automatically deposited "
              "into it, or bill payments are regularly withdrawn from it through a registered mandate (ECS/NACH, "
              "utilities, loan repayments). A 'relationship' exists when, for instance, the depositor also holds "
              "another deposit, a locker, demat or loan account.",
  steps=["Salary/pension credit → transactional", "Regular mandate debits → transactional"],
  why="A single recent transaction, debit card use or being a business current account does not meet RBI's test.",
  facts=[fact("An account is 'transactional' if (i) the depositor's salary or pension is automatically deposited into "
              "the account, or (ii) bill payments are regularly withdrawn from the account by way of a registered "
              "mandate for ECS / NACH / utilities payments / loan repayments, etc.", B_ALM)])

Q("009", "B-BAS09-08", T, LCR, "Intermediate",
  "RBI requires banks to monitor the LCR in each 'significant' currency. When is a currency considered significant for "
  "this purpose?",
  ["When the bank's aggregate liabilities in that currency are 5% or more of its total liabilities",
   "When the currency is one of the SDR basket currencies", "When it forms 25% or more of the bank's HQLA",
   "When the bank has a branch in a country using that currency"],
  concept="LCR by significant currency",
  explanation="To capture currency mismatches, banks monitor the LCR in each significant currency, and a currency is "
              "significant if the aggregate liabilities denominated in it amount to 5% or more of the bank's total "
              "liabilities. Foreign bank branches, which hold no foreign-currency HQLA, need not submit this statement.",
  steps=["Liabilities in a currency ≥ 5% of total liabilities → significant currency → monitor its LCR"],
  why="The SDR basket, a share of HQLA or branch presence is not the test RBI uses.",
  facts=[fact("A currency is considered 'significant' if the aggregate liabilities denominated in that currency amount "
              "to 5 per cent or more of the bank's total liabilities", B_ALM),
         fact("In order to better capture potential currency mismatches, a bank shall monitor the LCR in each "
              "significant currency", B_ALM)])

asf = 100 * 1.00 + 500 * 0.95 + 300 * 0.90 + 200 * 0.50
rsf = 50 * 0 + 200 * 0.05 + 300 * 0.50 + 500 * 0.85 + 20 * 1.00 + 30 * 1.00
assert (asf, rsf) == (945, 635) and round(100 * asf / rsf, 1) == 148.8
assert round(100 * 1000 / rsf, 1) == 157.5 and round(100 * asf / (10 + 150 + 250 + 50), 1) == 205.4
Q("009", "B-BAS09-09", T, LCR, "Advanced",
  "A bank's balance sheet (₹ crore): regulatory capital 100; stable retail deposits under one year 500; less stable "
  "retail deposits under one year 300; deposits from non-financial corporates under one year 200. Assets: cash 50; "
  "unencumbered Level 1 securities 200; retail loans maturing within one year 300; performing loans of over one year "
  "not qualifying for a 35% or lower risk weight 500; non-performing loans 20; fixed assets 30. Using RBI's ASF and "
  "RSF factors, what is its NSFR (approximately)?",
  ["148.8%, meeting the 100% minimum", "157.5%, meeting the 100% minimum", "205.4%, meeting the 100% minimum",
   "100.0%, just meeting the minimum"],
  concept="Computing the NSFR",
  explanation="ASF = 100 × 100% + 500 × 95% + 300 × 90% + 200 × 50% = 100 + 475 + 270 + 100 = 945. RSF = 50 × 0% + 200 × "
              "5% + 300 × 50% + 500 × 85% + 20 × 100% + 30 × 100% = 0 + 10 + 150 + 425 + 20 + 30 = 635. NSFR = 945 ÷ "
              "635 ≈ 148.8%.",
  steps=["ASF = 945", "RSF = 635", "NSFR = 945/635 ≈ 148.8% (≥ 100%)"],
  why="157.5% treats all retail deposits as 100% ASF; 205.4% applies 50% instead of 85% to long-term loans; 100% "
      "ignores the factors altogether.",
  computed=True,
  facts=[fact("ASF factors: regulatory capital 100 per cent; 'stable' retail and SBC deposits of less than one year 95 "
              "per cent; 'less stable' 90 per cent; funding with residual maturity of less than one year provided by "
              "non-financial corporate customers 50 per cent", B_ALM),
         fact("RSF factors: coins and banknotes 0 per cent; unencumbered Level 1 assets 5 per cent; loans to retail "
              "customers with residual maturity of less than one year 50 per cent; other unencumbered performing loans "
              "that do not qualify for the 35 per cent or lower risk weight with residual maturities of one year or "
              "more 85 per cent; non-performing loans and fixed assets 100 per cent", B_ALM)])

out_, in_, h = 1000, 900, 300
net = out_ - min(in_, 0.75 * out_)
assert net == 250 and 100 * h / net == 120 and 100 * h / (out_ - in_) == 300
Q("009", "B-BAS09-10", T, LCR, "Advanced",
  "Over the next 30 days a bank expects cash outflows of ₹1,000 crore and contractual inflows of ₹900 crore. Its stock "
  "of HQLA is ₹300 crore. What is its LCR under RBI's rules?",
  ["120%", "300%", "30%", "92%"],
  concept="Inflow cap in the LCR",
  explanation="Inflows can be recognised only up to 75% of outflows: min(900, 750) = 750. Net cash outflows = 1,000 − 750 "
              "= 250. LCR = 300 ÷ 250 = 120%, above the 100% minimum. Without the cap the ratio would wrongly appear "
              "as 300 ÷ 100 = 300%.",
  steps=["Cap inflows: min(900, 0.75 × 1,000) = 750", "Net outflows = 250", "LCR = 300/250 = 120%"],
  why="300% ignores the 75% cap; 30% divides by gross outflows; 92% subtracts 75% of inflows instead of capping them.",
  computed=True,
  facts=[fact("Total expected cash inflows shall be calculated ... up to an aggregate cap of 75 per cent of total "
              "expected cash outflows", B_ALM),
         fact("LCR shall be computed as the ratio of the stock of HQLA to the Net Cash Outflows over the next 30 "
              "calendar days", B_ALM)])
assert round(100 * h / (out_ - 0.75 * in_)) == 92

Q("009", "B-BAS09-11", T, LCR, "Advanced",
  "Under RBI's NSFR rules, which of the following liability–ASF factor pairs is INCORRECTLY matched?",
  ["Operational deposits – 95%",
   "Funding of under one year from NABARD – 50%",
   "Funding from RBI with residual maturity of less than six months – 0%",
   "Term deposits of one year or more that cannot be withdrawn early without a significant penalty – 100%"],
  concept="ASF factors",
  explanation="Operational deposits (from clearing, custody and cash management relationships) get a 50% ASF factor, "
              "not 95%. Funding under one year from national development banks such as NABARD, EXIM Bank, NaBFID, NHB "
              "and SIDBI also gets 50%; funding from RBI or other central banks maturing within six months gets 0%; "
              "liabilities including term deposits with effective residual maturity of one year or more get 100%.",
  steps=["Operational deposits → 50%", "NDB funding < 1 year → 50%", "RBI funding < 6 months → 0%",
         "Liabilities ≥ 1 year → 100%"],
  why="The other three pairs are exactly as RBI prescribes.",
  facts=[fact("Liabilities receiving a 50 per cent ASF factor comprise: ... (2) Operational deposits as defined in "
              "chapter on LCR. (3) Funding with residual maturity of less than one year from sovereigns, PSEs MDBs, and "
              "national development banks (NDBs), viz., EXIM Bank, NABARD, NaBFID, NHB, and SIDBI", B_ALM),
         fact("zero per cent ASF factor ... including funding with residual maturity of less than six months from the "
              "RBI and / or other central banks and financial institutions; 100 per cent ASF: secured and unsecured "
              "borrowings and liabilities (including term deposits) with effective residual maturities of one year or "
              "more", B_ALM)])

Q("009", "B-BAS09-12", T, CAP, "Advanced",
  "Consider the following statements about RBI's 2025 list of Domestic Systemically Important Banks (D-SIBs), "
  "released on 2 December 2025:\n"
  "I. The additional CET1 requirement of a D-SIB applies in addition to the Capital Conservation Buffer.\n"
  "II. The D-SIB framework was first issued on 22 July 2014 and updated on 28 December 2023.\n"
  "III. Axis Bank was added to the list in bucket 3, with an additional CET1 requirement of 0.60%.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="D-SIB framework",
  explanation="RBI said the additional CET1 requirement for D-SIBs is in addition to the Capital Conservation Buffer, "
              "and that the framework issued on 22 July 2014 was updated on 28 December 2023. The 2025 list has only "
              "three banks: SBI (bucket 4), HDFC Bank (bucket 2) and ICICI Bank (bucket 1); bucket 3 is empty.",
  steps=["I: correct", "II: correct", "III: wrong – no bank in bucket 3, Axis Bank not a D-SIB"],
  why="Statement III is false, which rules out the options containing it; II is also true, so 'I only' is incomplete.",
  current=ca("2025-12-02"),
  facts=[fact("The additional Common Equity Tier 1 (CET1) requirement for these D-SIBs will be in addition to the "
              "Capital Conservation Buffer ... 3 - 0.60%", B_DSIB),
         fact("The Reserve Bank had issued the 'Framework for dealing with Domestic Systemically Important Banks "
              "(D-SIBs)' on July 22, 2014, which was subsequently updated on December 28, 2023", B_DSIB)])

# ---- batch 010 (Basic 3, Intermediate 1, Advanced 3)
Q("010", "B-BAS10-01", T, LCR, "Basic",
  "During a period of financial stress, a bank uses part of its stock of HQLA and its LCR falls below 100 per cent. "
  "What does RBI's LCR framework require it to do?",
  ["Immediately report the shortfall to RBI's Department of Supervision, with reasons and corrective steps",
   "Nothing, as the LCR is only a monitoring tool", "Stop all lending until the LCR is restored",
   "Pay a penal rate of interest on the shortfall to RBI for every day of the shortfall"],
  concept="Use of HQLA in stress",
  explanation="The LCR must normally be at least 100%, but in stress a bank may use its HQLA and let the ratio fall below "
              "100%. It must then immediately report the shortfall to the Department of Supervision, RBI, with the "
              "reasons and the corrective steps initiated.",
  steps=["Stress → HQLA may be used", "LCR < 100% → immediate report to DoS with reasons and remedial steps"],
  why="The LCR is a binding minimum; RBI does not require a lending freeze or a daily penal charge for this.",
  facts=[fact("during a period of financial stress, a bank shall have the option to use its stock of HQLA and thereby "
              "allowing LCR to fall below 100 per cent. In such a case, the bank shall immediately report the shortfall "
              "to DoS, RBI. The report shall include reasons for such usage and corrective steps initiated", B_ALM)])

Q("010", "B-BAS10-02", T, LCR, "Basic",
  "At what level does RBI's LCR framework apply to a foreign bank operating in India through branches?",
  ["On a standalone basis, for its Indian operations only", "On a consolidated basis for the global group",
   "Only to its largest branch in India", "It does not apply to foreign bank branches"],
  concept="Scope of the LCR",
  explanation="The LCR applies to an Indian bank on a solo and a consolidated basis. For a foreign bank operating as "
              "branches in India it applies on a standalone basis, i.e. to its Indian operations only.",
  steps=["Indian bank → solo + consolidated", "Foreign bank branches → standalone (Indian operations)"],
  why="RBI does not apply its LCR to the foreign bank's global group, to one branch only, or exempt the branches.",
  facts=[fact("The LCR framework shall be applicable to an Indian bank on a standalone ('solo') as well as consolidated "
              "level. For a foreign bank operating as branch in India, the framework shall be applicable on standalone "
              "basis i.e., for Indian operations only", B_ALM)])

Q("010", "B-BAS10-03", T, CAP, "Basic",
  "The Basel Committee's post-crisis Basel III reforms were endorsed in December 2017 by its oversight body. What is "
  "that body?",
  ["The Group of Central Bank Governors and Heads of Supervision (GHOS)", "The G20 Finance Ministers",
   "The Financial Action Task Force (FATF)", "The International Monetary and Financial Committee of the IMF"],
  concept="Governance of the Basel Committee",
  explanation="The BIS notes that the post-crisis regulatory reforms were endorsed on 7 December 2017 by the Group of "
              "Central Bank Governors and Heads of Supervision (GHOS), the Basel Committee's oversight body.",
  steps=["Oversight body of BCBS → GHOS"],
  why="The G20, FATF and IMFC are not the Basel Committee's oversight body.",
  facts=[fact("The post-crisis regulatory reforms were endorsed by the Group of Central Bank Governors and Heads of "
              "Supervision (GHOS), the Basel Committee's oversight body, on 7 December 2017", B_BIS3)])

Q("010", "B-BAS10-04", T, LCR, "Intermediate",
  "RBI's liquidity risk management directions draw on a Basel Committee document published after the global financial "
  "crisis. Which document, published in September 2008, is it?",
  ["Principles for Sound Liquidity Risk Management and Supervision", "Core Principles for Effective Banking Supervision",
   "International Convergence of Capital Measurement and Capital Standards", "Revised Framework on Market Risk"],
  concept="Basel principles on liquidity",
  explanation="RBI notes that, after the crisis, the BCBS published 'Principles for Sound Liquidity Risk Management and "
              "Supervision' in September 2008, later reviewed in January 2019; its broad principles are reproduced "
              "in the Asset Liability Management Directions.",
  steps=["September 2008 → Principles for Sound Liquidity Risk Management and Supervision"],
  why="The Core Principles (1997), the 1988 Capital Accord and market-risk standards are different documents.",
  facts=[fact("the Basel Committee on Banking Supervision (BCBS) published 'Principles for Sound Liquidity Risk "
              "Management and Supervision' in September 2008 and subsequently reviewed in January 2019", B_ALM)])

Q("010", "B-BAS10-05", T, LCR, "Advanced",
  "Consider the following statements on Required Stable Funding (RSF) factors under RBI's NSFR rules:\n"
  "I. Unencumbered SLR securities attract an RSF factor of 5%.\n"
  "II. Physically traded commodities, including gold, attract an RSF factor of 85%.\n"
  "III. Loans to financial institutions with a residual maturity of one year or more attract an RSF factor of 65%.\n"
  "Which of the above is/are correct?",
  ["I and II only", "I and III only", "II only", "I, II and III"],
  concept="RSF factors",
  explanation="Unencumbered Level 1 assets and SLR securities get 5%; physical traded commodities including gold get "
              "85%; loans to financial institutions with residual maturity of one year or more fall in the 100% "
              "category (the 65% factor is for other unencumbered loans of a year or more, excluding loans to "
              "financial institutions, such as loans to sovereigns and NDBs).",
  steps=["I: 5% – correct", "II: 85% – correct", "III: FI loans ≥ 1 year → 100%, not 65% – wrong"],
  why="Statement III is false, so options including it are wrong; 'II only' misses the true statement I.",
  facts=[fact("Assets assigned a 5 per cent RSF factor comprise (1) Unencumbered Level 1 assets ... (2) Unencumbered SLR "
              "securities; 85 per cent RSF factor: (7) Physical traded commodities, including gold", B_ALM),
         fact("100 per cent RSF factor: All other assets not included in the above categories, including non-performing "
              "loans, loans to financial institutions with a residual maturity of one year or more, non-exchange traded "
              "equities, fixed assets", B_ALM)])

inflow = 200 * 0.0 + 100 * 1.0 + 80 * 0.5
assert inflow == 140 and 200 + 100 + 80 == 380 and 100 + 80 == 180
Q("010", "B-BAS10-06", T, LCR, "Advanced",
  "Over the next 30 days a bank has these maturing secured loans: a reverse repo of ₹200 crore secured by Level 1 "
  "assets, a reverse repo of ₹100 crore secured by non-HQLA assets, and margin loans of ₹80 crore to customers against "
  "non-HQLA collateral. Under RBI's LCR rules, what total cash inflow can it recognise from these?",
  ["₹140 crore", "₹380 crore", "₹180 crore", "₹100 crore"],
  concept="Inflows from secured lending in the LCR",
  explanation="Maturing reverse repos secured by Level 1 assets are assumed to roll over, so 0% inflow. Those secured by "
              "non-HQLA are assumed not to roll over, so 100% (₹100 crore). For margin loans against non-HQLA "
              "collateral, no more than 50% of contractual inflows can be recognised (₹40 crore). Total = ₹140 crore.",
  steps=["Level 1 reverse repo: 0% × 200 = 0", "Non-HQLA reverse repo: 100% × 100 = 100",
         "Margin loans: 50% × 80 = 40", "Total = 140"],
  why="₹380 crore counts everything at 100%; ₹180 crore takes the margin loans at 100%; ₹100 crore ignores the margin "
      "loans.",
  computed=True,
  facts=[fact("A bank shall assume that maturing reverse repurchase or securities borrowing agreements secured by Level 1 "
              "assets will be rolled over, and therefore will not give rise to any cash inflows, i.e., zero per cent "
              "cash inflow ... A bank is assumed not to roll-over maturing reverse repurchase or securities borrowing "
              "agreements secured by non-HQLA assets and can assume to receive back 100 per cent of the cash", B_ALM),
         fact("a bank shall recognise no more than 50 per cent of contractual inflows from maturing margin loans made "
              "against non-HQLA collateral", B_ALM)])

Q("010", "B-BAS10-07", T, CAP, "Advanced",
  "Consider the following statements on Basel III, based on the Bank for International Settlements' account:\n"
  "I. The Basel Committee issued the full text of the revised Liquidity Coverage Ratio after its endorsement by the "
  "GHOS on 6 January 2013.\n"
  "II. The first Basel III text was published in December 2012 and has not been updated since.\n"
  "III. The Regulatory Consistency Assessment Programme (RCAP), which monitors implementation of Basel standards, was "
  "established in 2012.\n"
  "Which of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I only"],
  concept="Evolution of Basel III",
  explanation="The revised LCR text followed GHOS endorsement on 6 January 2013. The initial Basel III document was "
              "published in December 2010 and updated in June 2011, so statement II is wrong. The RCAP was set up in "
              "2012 to monitor timely and consistent adoption of Basel III.",
  steps=["I: correct", "II: wrong – December 2010, updated June 2011", "III: correct"],
  why="Options with II are wrong; 'I only' leaves out the correct statement III.",
  facts=[fact("The Basel Committee issued the full text of the revised Liquidity Coverage Ratio (LCR) following "
              "endorsement on 6 January 2013 by its governing body - the Group of Central Bank Governors and Heads of "
              "Supervision (GHOS); This document, originally published in December 2010 and updated in June 2011 "
              "represents the initial phase of Basel III reforms", B_BIS3),
         fact("The Basel Committee established a comprehensive Regulatory Consistency Assessment Programme (RCAP) in "
              "2012 to monitor and assess the adoption and implementation of its standards", B_BIS3)])

# ================= RBI Integrated Ombudsman Scheme
from datetime import date as _date, timedelta as _td  # noqa: E402

T = "RBI Integrated Ombudsman Scheme"
SG, PL = "Scope and grounds", "Process and limits"

# ---- batch 008 (Basic 1, Intermediate 2, Advanced 4)
Q("008", "B-IOS08-01", T, SG, "Basic",
  "How does RBI describe the Reserve Bank – Integrated Ombudsman Scheme, 2026 (RB-IOS, 2026)?",
  ["A cost-free, expeditious and non-adversarial alternate grievance redress mechanism",
   "A statutory consumer court set up under the Consumer Protection Act, 2019",
   "An arbitration mechanism under the Arbitration and Conciliation Act, 1996",
   "A fee-based fast-track tribunal under the Banking Regulation Act, 1949"],
  concept="Nature of RB-IOS, 2026",
  explanation="RBI's FAQs describe RB-IOS, 2026 as a cost-free, expeditious and non-adversarial alternate grievance "
              "redress mechanism for customer complaints involving deficiency in service by the regulated entities it "
              "covers. It is not a court, tribunal or arbitration.",
  steps=["RB-IOS → free, quick, non-adversarial alternate grievance redress"],
  why="It is not a consumer court, an arbitration under the 1996 Act, or a fee-based tribunal.",
  facts=[fact("The Reserve Bank - Integrated Ombudsman Scheme, 2026 (RB-IOS, 2026 / the Scheme) is a cost-free, "
              "expeditious and non-adversarial alternate grievance redress mechanism for customer complaints involving "
              "deficiency in service by Regulated Entities covered under the Scheme", B_IOS)])

bank_reply = _date(2026, 9, 12)
deadline = bank_reply + _td(days=90)
assert deadline == _date(2026, 12, 11)
Q("008", "B-IOS08-02", T, PL, "Intermediate",
  "Ritu complained to her bank on 1 September 2026. The bank rejected her complaint by a reply dated 12 September "
  "2026, and she is not satisfied. Under RB-IOS, 2026, when can she approach the RBI Ombudsman?",
  ["Immediately, and no later than 90 days from the bank's reply, i.e. by 11 December 2026",
   "Only after 30 days from her complaint, i.e. from 1 October 2026, and by 30 December 2026",
   "Only after 30 days from her complaint, and by 11 December 2026",
   "Immediately, and by 12 March 2027 (six months from the reply)"],
  concept="When a complaint can be filed",
  explanation="The 30-day wait applies only when the regulated entity has not replied. A complainant who has received a "
              "reply and is dissatisfied may approach the Ombudsman at once. The complaint must be made within 90 days "
              "from the expiry of the reply period or from the RE's last communication, whichever is later; here the "
              "last communication is 12 September, so the limit is 12 September + 90 days = 11 December 2026.",
  steps=["Reply received and not satisfied → no need to wait 30 days", "Limit: 90 days from last communication",
         "12 Sep 2026 + 90 days = 11 Dec 2026"],
  why="Waiting 30 days is needed only when there is no reply; six months is not the limit.",
  computed=True,
  facts=[fact("A complaint can be filed before the RBI Ombudsman if the complainant has not received any reply within 30 "
              "days ... or if the complainant is not satisfied with the reply/resolution provided by the Regulated "
              "Entity. The complaint must be made to the RBI Ombudsman within 90 days from the date on which the above "
              "timeline expires or the date of the last communication from the concerned Regulated Entity, whichever "
              "is later", B_IOS)])

Q("008", "B-IOS08-03", T, PL, "Intermediate",
  "Under RB-IOS, 2026, what must happen before the RBI Ombudsman passes an Award against a regulated entity?",
  ["Both the complainant and the regulated entity must be given a reasonable opportunity of being heard, orally or "
   "in writing", "The complainant must deposit 10% of the disputed amount",
   "The Appellate Authority must approve the draft Award", "The regulated entity's Board must consent to the Award"],
  concept="Award by the RBI Ombudsman",
  explanation="If a complaint is not settled and not liable to rejection, the Ombudsman examines the record and may pass "
              "an Award directing remedial action or compensation. Before passing it, both parties are given a "
              "reasonable opportunity of being heard, either orally or in writing.",
  steps=["Not settled → examination on record", "Hear both parties → Award"],
  why="There is no deposit, no prior approval by the Appellate Authority and no Board consent requirement.",
  facts=[fact("Before passing an Award, both the complainant and the Regulated Entity are given a reasonable "
              "opportunity of being heard, either orally or in writing", B_IOS)])

Q("008", "B-IOS08-04", T, PL, "Advanced",
  "Consider the following statements based on RBI's Annual Report of the Ombudsman Scheme 2024-25 (released 1 "
  "December 2025):\n"
  "I. Complaints received at the Offices of RBI Ombudsman per lakh accounts fell from 8.9 in 2023-24 to 7.7 in "
  "2024-25.\n"
  "II. 91.22 per cent of complaints received at the Offices of RBI Ombudsman were lodged digitally, through the CMS "
  "portal or e-mail.\n"
  "III. Complaints from individuals made up less than half of the complaints received at the Offices of RBI "
  "Ombudsman.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II only", "I and III only", "I, II and III"],
  concept="Ombudsman Scheme statistics 2024-25",
  explanation="The report records that complaints per lakh accounts (deposit and credit) fell from 8.9 to 7.7 and that "
              "91.22% of complaints at the ORBIOs were lodged digitally. Individuals accounted for 87.19% of "
              "complaints, so statement III is false.",
  steps=["I: correct (8.9 → 7.7)", "II: correct (91.22% digital)", "III: wrong – individuals 87.19%"],
  why="Options containing III are wrong; 'II only' omits the correct statement I.",
  current=ca("2025-12-01"),
  facts=[fact("Complaints received at ORBIOs per lakh accounts decreased from 8.9 complaints in F.Y.2023-24 to 7.7 "
              "complaints in F.Y.2024-25", B_OSAR),
         fact("Out of the total complaints received at the ORBIOs, 91.22 per cent of the complaints were lodged through "
              "digital mode using CMS portal or email. The share of complaints from individuals in the total complaints "
              "was the highest at 2,58,365 (87.19 per cent)", B_OSAR)])

maint = 180621
settled = round(maint * 51.91 / 100)
assert abs(settled - 93752) < 20 and round(290567 * 0.5191) == 150833 and round(maint * 0.4336) == 78317
Q("008", "B-IOS08-05", T, PL, "Advanced",
  "In 2024-25 the Offices of RBI Ombudsman disposed of 2,90,567 complaints, of which 62.16 per cent (1,80,621) were "
  "maintainable. Of the maintainable complaints, 51.91 per cent were resolved in the complainant's favour through "
  "mutual settlement, conciliation or mediation, and 43.36 per cent were rejected. About how many complaints were "
  "resolved through settlement, conciliation or mediation?",
  ["About 93,750", "About 1,50,830", "About 78,320", "About 1,12,330"],
  concept="Reading Ombudsman disposal data",
  explanation="The 51.91% share applies to maintainable complaints only: 1,80,621 × 0.5191 ≈ 93,760 (the report gives "
              "93,752). Applying 51.91% to all 2,90,567 disposals gives about 1,50,830, which is wrong; about 78,320 is "
              "the rejected share (43.36%).",
  steps=["Base = maintainable complaints = 1,80,621", "× 51.91% ≈ 93,750"],
  why="1,50,830 uses the wrong base; 78,320 is the number rejected; 1,12,330 has no basis in the data.",
  computed=True,
  current=ca("2025-12-01"),
  facts=[fact("Of these maintainable complaints 93,752 complaints (51.91 per cent) were resolved in favour of the "
              "complainant through mutual settlement, conciliation or mediation; 78,323 (43.36 per cent) complaints "
              "were rejected by RBI Ombudsmen", B_OSAR),
         fact("Out of the 2,90,567 complaints disposed by the ORBIOs during F.Y.2024-25, 62.16 per cent (1,80,621 "
              "complaints) were disposed as maintainable complaints", B_OSAR)])

Q("008", "B-IOS08-06", T, SG, "Advanced",
  "Customers file complaints against four NBFCs registered with RBI, none of them an excluded type (figures as per the "
  "audited balance sheet of the previous year):\n"
  "P. A deposit-taking NBFC with assets of ₹60 crore.\n"
  "Q. A non-deposit-taking NBFC with customer interface and assets of ₹150 crore.\n"
  "R. A deposit-taking NBFC with assets of ₹20 crore.\n"
  "S. A non-deposit-taking NBFC with customer interface and assets of ₹90 crore.\n"
  "Against which of them can a complaint be filed under RB-IOS, 2026?",
  ["P, Q and R only", "P and Q only", "Q only", "P, Q, R and S"],
  concept="Coverage of NBFCs under RB-IOS, 2026",
  explanation="RB-IOS, 2026 covers NBFCs (other than the excluded types) that either are authorised to accept deposits "
              "or have customer interface with assets of ₹100 crore and above. The ₹100 crore threshold applies only to "
              "the customer-interface limb, so every deposit-taking NBFC (P and R) is covered whatever its size; Q "
              "(₹150 crore) is covered; S (₹90 crore, non-deposit) is not.",
  steps=["Deposit-taking → covered regardless of size (P, R)", "Customer interface → needs ≥ ₹100 crore (Q yes, S no)"],
  why="'P and Q only' wrongly applies the ₹100 crore test to deposit-taking R; 'Q only' does the same to P and R; S is "
      "below the threshold.",
  facts=[fact("NBFCs: all NBFCs registered with RBI, excluding Housing Finance Companies, Core Investment Companies, "
              "IDF-NBFCs, NBFC-IFCs, NOFHCs, Primary Dealers and Mortgage Guarantee Companies, which either are "
              "authorized to accept deposits or have customer interface with asset size of Rs 100 crore and above as "
              "on the date of the audited balance sheet of the previous financial year", B_IOS)])

Q("008", "B-IOS08-07", T, SG, "Advanced",
  "Assuming every procedural condition is met, which of the following grievances is maintainable before the RBI "
  "Ombudsman under RB-IOS, 2026?",
  ["A borrower's complaint that the bank has not returned his title deeds after he closed his home loan",
   "An IT vendor's dispute with a bank over unpaid software licence fees",
   "A bank officer's grievance that he was denied promotion",
   "A customer's grievance against the personal conduct of a bank's executive director"],
  concept="Non-maintainable grounds",
  explanation="RB-IOS, 2026 deals with deficiency in service to customers. Disputes between a vendor and a regulated "
              "entity, disputes involving the employee-employer relationship, and grievances against the management or "
              "executives of the RE are expressly non-maintainable. Failure to return property documents after loan "
              "closure is a deficiency in service to a customer.",
  steps=["Vendor dispute → non-maintainable", "Employee-employer dispute → non-maintainable",
         "Grievance against management/executives → non-maintainable", "Title deeds not returned → maintainable"],
  why="The vendor, employee and management grievances fall under the excluded categories.",
  facts=[fact("Disputes between a vendor and a Regulated Entity. Grievances against Management or Executives of a "
              "Regulated Entity ... Disputes involving employee-employer relationship of a Regulated Entity", B_IOS),
         fact("Any customer aggrieved by an act or omission of a Regulated Entity resulting in deficiency in service may "
              "file a complaint under the Scheme", B_IOS)])

# ---- batch 009 (Basic 3, Intermediate 1, Advanced 1)
Q("009", "B-IOS09-01", T, PL, "Basic",
  "According to RBI's Annual Report of the Ombudsman Scheme 2024-25, complaints under the Integrated Ombudsman Scheme "
  "were handled by the Centralised Receipt and Processing Centre and how many Offices of RBI Ombudsman?",
  ["24", "22", "31", "15"],
  concept="Ombudsman offices",
  explanation="The report states that complaints are handled by 24 Offices of RBI Ombudsman (ORBIOs) together with the "
              "Centralised Receipt and Processing Centre (CRPC) at Chandigarh.",
  steps=["ORBIOs in 2024-25 → 24"],
  why="22, 31 and 15 are not the number given in the report.",
  current=ca("2025-12-01"),
  facts=[fact("Under RB-IOS, 2021, the complaints are presently handled by 24 Offices of RBI Ombudsman (ORBIOs) and the "
              "Centralised Receipt and Processing Centre (CRPC)", B_OSAR)])

Q("009", "B-IOS09-02", T, SG, "Basic",
  "According to RBI's Annual Report of the Ombudsman Scheme 2024-25, which category accounted for the largest share of "
  "complaints received at the Offices of RBI Ombudsman in 2024-25?",
  ["Loans and advances", "ATM and debit cards", "Deposit accounts", "Pension payments"],
  concept="Complaint categories",
  explanation="Loans and advances formed the largest category (29.25%). The top five – loans and advances, credit cards, "
              "mobile/electronic banking, deposit accounts and ATM/debit cards – made up 86.20% of complaints.",
  steps=["Top category 2024-25 → loans and advances (29.25%)"],
  why="ATM/debit cards and deposit accounts were among the top five but lower; pension complaints were not the largest.",
  current=ca("2025-12-01"),
  facts=[fact("the top five categories of complaints, consisting of complaints related to (i) loans and advances, (ii) "
              "credit cards, (iii) mobile / electronic banking, (iv) deposit accounts, and (v) ATM / Debit cards, "
              "accounted for 86.20 per cent of all complaints received by the ORBIOs. Complaints related to Loan and "
              "Advances was the highest at 29.25 per cent", B_OSAR)])

Q("009", "B-IOS09-03", T, SG, "Basic",
  "A customer files a complaint under RB-IOS, 2026 that is directed against the management and executives of his bank "
  "rather than any deficiency in a service to him. Such a complaint is:",
  ["Not maintainable under the Scheme", "Maintainable only if the bank is a public sector bank",
   "Maintainable if the amount involved is below ₹30 lakh", "Maintainable only through the Contact Centre"],
  concept="Non-maintainable complaints",
  explanation="Grievances against the management or executives of a regulated entity are listed among complaints that "
              "are not maintainable under RB-IOS, 2026. The Scheme addresses deficiency in service.",
  steps=["Grievance against management/executives → non-maintainable"],
  why="Bank ownership and amounts are irrelevant, and complaints cannot be filed through the Contact Centre.",
  facts=[fact("The following types of complaints are not maintainable under the Reserve Bank – Integrated Ombudsman "
              "Scheme, 2026 ... Grievances against Management or Executives of a Regulated Entity", B_IOS)])

Q("009", "B-IOS09-04", T, PL, "Intermediate",
  "According to RBI's Annual Report of the Ombudsman Scheme 2024-25, RBI's Contact Centre (toll-free 14448) operates "
  "from which centres?",
  ["Chandigarh, Kochi and Bhubaneswar", "Mumbai, Chennai and Kolkata", "New Delhi only", "Chandigarh only"],
  concept="RBI Contact Centre",
  explanation="The report says the Contact Centre, which gives information on the grievance redress mechanism, guides "
              "complainants and provides complaint status, operates from Chandigarh, Kochi and Bhubaneswar. The CRPC "
              "itself is at Chandigarh.",
  steps=["Contact Centre locations → Chandigarh, Kochi, Bhubaneswar"],
  why="Chandigarh alone is incomplete; the metros and New Delhi are not named.",
  current=ca("2025-12-01"),
  facts=[fact("The Contact Centre, which is operating from Chandigarh, Kochi and Bhubaneswar, received 9,27,598 calls "
              "during F.Y.2024-25", B_OSAR)])

Q("009", "B-IOS09-05", T, PL, "Advanced",
  "Consider the following statements about RBI's Contact Centre in 2024-25, from RBI's Annual Report of the Ombudsman "
  "Scheme 2024-25:\n"
  "I. It received 9,27,598 calls, up from 7,19,694 in 2023-24.\n"
  "II. Most calls were attended directly by Contact Centre personnel rather than through the IVRS.\n"
  "III. Abandoned calls were less than 1 per cent of the total.\n"
  "Which of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I only"],
  concept="Contact Centre statistics",
  explanation="Calls rose to 9,27,598 from 7,19,694. Of these, 60.64% were attended through the IVRS and 38.59% directly "
              "by personnel, so statement II is wrong. Only 0.78% (7,219) were abandoned.",
  steps=["I: correct", "II: wrong – IVRS 60.64% vs personnel 38.59%", "III: correct – 0.78%"],
  why="Options containing II are wrong; 'I only' omits the correct statement III.",
  current=ca("2025-12-01"),
  facts=[fact("The Contact Centre received 9,27,598 calls during F.Y.2024-25, as compared to 7,19,694 in F.Y.2023-24. Of "
              "these, 60.64 per cent (5,62,452) of the calls were attended through the IVRS facility, 38.59 per cent "
              "(3,57,927) of the calls were attended directly by the CC personnel and only 0.78 per cent (7,219) of "
              "calls were abandoned", B_OSAR)])

# ---- batch 010 (Basic 2, Intermediate 4, Advanced 1)
Q("010", "B-IOS10-01", T, PL, "Basic",
  "After registering a complaint with the RBI Ombudsman, how can a complainant track its status on RBI's CMS portal?",
  ["Using the complaint number and mobile number", "Using the bank account number and IFSC",
   "Using the Aadhaar number and PAN", "Only by visiting the Office of the RBI Ombudsman"],
  concept="Tracking a complaint",
  explanation="On successful registration the complainant gets a complaint number; the status can be tracked on the CMS "
              "portal with the complaint number and mobile number, or through the Contact Centre (14448).",
  steps=["Complaint number + mobile number → status on CMS"],
  why="Account/IFSC and Aadhaar/PAN are not used; no office visit is needed.",
  facts=[fact("The status of the complaint can be tracked through the CMS portal using the complaint number and mobile "
              "number", B_IOS)])

Q("010", "B-IOS10-02", T, PL, "Basic",
  "According to RBI's Annual Report of the Ombudsman Scheme 2024-25, about how many complaints were received under the "
  "Integrated Ombudsman Scheme in 2024-25?",
  ["13.34 lakh", "11.75 lakh", "9.11 lakh", "2.96 lakh"],
  concept="Volume of complaints",
  explanation="13,34,244 complaints were received in 2024-25 against 11,75,075 in 2023-24, a rise of 13.55%. Of the "
              "total, 9.11 lakh came to the CRPC and 2.96 lakh to the Offices of RBI Ombudsman.",
  steps=["2024-25 → 13.34 lakh (up 13.55%)"],
  why="11.75 lakh is the 2023-24 figure; 9.11 lakh and 2.96 lakh are the CRPC and ORBIO parts.",
  current=ca("2025-12-01"),
  facts=[fact("Under the RB-IOS, 13,34,244 complaints were received in F.Y.2024-25 as compared to 11,75,075 in "
              "F.Y.2023-24, an increase of 13.55 per cent over the previous year", B_OSAR)])

Q("010", "B-IOS10-03", T, PL, "Intermediate",
  "According to RBI's Annual Report of the Ombudsman Scheme 2024-25, from which population group did the largest share "
  "of complaints received at the Offices of RBI Ombudsman come?",
  ["Metropolitan centres", "Urban centres", "Semi-urban centres", "Rural areas"],
  concept="Complaints by population group",
  explanation="In 2024-25, 45.86% of complaints came from metropolitan centres, followed by urban (25.64%), "
              "semi-urban (18.46%) and rural areas (10.04%).",
  steps=["Metro 45.86% > urban 25.64% > semi-urban 18.46% > rural 10.04%"],
  why="Urban, semi-urban and rural areas each had smaller shares.",
  current=ca("2025-12-01"),
  facts=[fact("majority of complaints at the ORBIOs were received from Metropolitan Centres (45.86 per cent), followed "
              "by Urban (25.64 per cent), Semi Urban (18.46 per cent) and Rural areas (10.04 per cent)", B_OSAR)])

Q("010", "B-IOS10-04", T, SG, "Intermediate",
  "According to RBI's Annual Report of the Ombudsman Scheme 2024-25, which statement about complaints against banks "
  "received at the Offices of RBI Ombudsman is correct?",
  ["Private sector banks had the highest share among banks (37.53%), overtaking public sector banks (34.80%)",
   "Public sector banks continued to have the highest share among banks, at over 38%",
   "Small finance banks had the highest share among banks",
   "Complaints against NBFCs outnumbered those against banks"],
  concept="Complaints by type of entity",
  explanation="Banks accounted for 81.53% of complaints (NBFCs 14.80%). Among banks, the share of private sector banks "
              "rose from 34.39% to 37.53%, while that of public sector banks, the highest in 2023-24, fell from 38.32% "
              "to 34.80%.",
  steps=["Banks 81.53%, NBFCs 14.80%", "Private banks 37.53% > PSBs 34.80% in 2024-25"],
  why="PSBs were highest only in 2023-24; SFBs were not the highest; NBFCs were far fewer than banks.",
  current=ca("2025-12-01"),
  facts=[fact("Among the banks, the share of complaints received against private sector banks was the highest and "
              "increased from 34.39 per cent in F.Y.2023-24 to 37.53 per cent in F.Y.2024-25. However, the share of "
              "complaints received against the public sector banks, which was the highest in F.Y.2023-24, declined "
              "from 38.32 per cent in F.Y. 2023-24 to 34.80 per cent in F.Y.2024-25", B_OSAR)])

Q("010", "B-IOS10-05", T, SG, "Intermediate",
  "Which of the following banks is covered by RB-IOS, 2026?",
  ["A District Central Co-operative Bank",
   "A non-scheduled primary (urban) co-operative bank with deposits of ₹30 crore",
   "A housing finance company", "A core investment company"],
  concept="Coverage of RB-IOS, 2026",
  explanation="RB-IOS, 2026 covers all commercial banks, RRBs, State Co-operative Banks, Central Co-operative Banks, "
              "scheduled UCBs and non-scheduled UCBs with deposits of ₹50 crore and above. HFCs and CICs are among the "
              "excluded NBFC types.",
  steps=["Central Co-operative Banks → covered", "Non-scheduled UCB < ₹50 crore → not covered",
         "HFC, CIC → excluded"],
  why="The UCB is below the ₹50 crore threshold; HFCs and CICs are expressly excluded.",
  facts=[fact("Banks: all Commercial Banks, Regional Rural Banks, State Co-operative Banks, Central Co-operative Banks, "
              "Scheduled Primary (Urban) Co-operative Banks, and Non-Scheduled Primary (Urban) Co-operative Banks with "
              "deposit size of Rs 50 crore and above", B_IOS),
         fact("NBFCs: all NBFCs registered with RBI, excluding Housing Finance Companies, Core Investment Companies",
              B_IOS)])

Q("010", "B-IOS10-06", T, SG, "Intermediate",
  "In RBI's Annual Report of the Ombudsman Scheme 2024-25, the largest group of non-maintainable complaints closed by "
  "the Offices of RBI Ombudsman were 'First Resort Complaints'. What are these?",
  ["Complaints filed with the RBI Ombudsman without the complainant first approaching the regulated entity",
   "Complaints filed for the first time by a customer under any ombudsman scheme",
   "Complaints filed within the first 30 days of opening an account",
   "Complaints first filed in a civil court"],
  concept="First Resort Complaints",
  explanation="FRCs are complaints received at the ORBIOs without the complainant having approached the concerned RE "
              "first. They are sent to the RE for redress, and the complainant is told he may complain again if the RE "
              "does not reply within 30 days or the reply is unsatisfactory. They formed 33.01% of the non-maintainable "
              "complaints closed by ORBIOs in 2024-25.",
  steps=["No prior complaint to the RE → First Resort Complaint → sent to the RE"],
  why="The term has nothing to do with first-time complainants, new accounts or court cases.",
  current=ca("2025-12-01"),
  facts=[fact("Of these, 33.01 per cent (36,289 complaints) were closed as First Resort Complaints (FRCs) ... FRCs are "
              "those complaints which are received at the ORBIOs without the complainant having approached the "
              "concerned RE first", B_OSAR)])

Q("010", "B-IOS10-07", T, PL, "Advanced",
  "Consider the following statements about the Centralised Receipt and Processing Centre (CRPC) in 2024-25, as "
  "reported in RBI's Annual Report of the Ombudsman Scheme 2024-25:\n"
  "I. Complaints received at the CRPC grew much faster (18.83%) than those received at the Offices of RBI Ombudsman "
  "(0.82%).\n"
  "II. Most complaints disposed of at the CRPC were assigned to the Offices of RBI Ombudsman for examination.\n"
  "III. E-mail was the channel for 93.18% of the complaints received at the CRPC.\n"
  "Which of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "III only"],
  concept="CRPC operations",
  explanation="CRPC complaints rose 18.83% (7,66,957 to 9,11,384) while ORBIO complaints rose 0.82%. Of 9.04 lakh "
              "complaints disposed at the CRPC, only 1.20 lakh were assigned to ORBIOs/CEPCs; 7.84 lakh were closed at "
              "the CRPC as non-complaints or non-maintainable, mostly First Resort Complaints. 93.18% of CRPC complaints "
              "came by e-mail.",
  steps=["I: correct", "II: wrong – 1.20 lakh of 9.04 lakh assigned", "III: correct"],
  why="Statement II is false, which rules out the options containing it; 'III only' omits the correct statement I.",
  current=ca("2025-12-01"),
  facts=[fact("The complaints received at the CRPC increased by 18.83 per cent from 7,66,957 complaints in F.Y.2023-24 "
              "to 9,11,384 complaints in F.Y.2024-25, while those received at the ORBIOs ... increased by 0.82 per "
              "cent", B_OSAR),
         fact("the CRPC has received 9.11 lakh complaints and disposed 9.04 lakh complaints ... Out of these, 1.20 lakh "
              "complaints were assigned to ORBIOs/CEPCs, while the remaining 7.84 lakh complaints were closed at the "
              "CRPC as non-complaint / non-maintainable complaints", B_OSAR),
         fact("During F.Y.2024-25, 93.18 per cent of the complaints received at the CRPC were through email", B_OSAR)])

# ================= Digital Banking
T = "Digital Banking"
MIB, CBDC = "Mobile and internet banking", "CBDC (e-rupee)"

# ---- batch 008 (Basic 1, Intermediate 5, Advanced 3)
Q("008", "B-DIG08-01", T, MIB, "Basic",
  "Under RBI's Digital Banking Channels Authorisation Directions, 2025, besides the Information Technology Act, 2000, "
  "which data-protection law must banks continuously adhere to in their digital banking operations?",
  ["The Digital Personal Data Protection Act, 2023", "The Right to Information Act, 2005",
   "The Credit Information Companies (Regulation) Act, 2005", "The Payment and Settlement Systems Act, 2007 only"],
  concept="Legal framework for digital banking",
  explanation="The general guidelines require banks offering digital banking to adhere continuously to the Information "
              "Technology Act, 2000, the Digital Personal Data Protection Act, 2023 and other legal requirements, with "
              "legal jurisdiction within India, along with FEMA, KYC/AML and DPSS instructions.",
  steps=["Digital banking → IT Act, 2000 + DPDP Act, 2023"],
  why="The RTI Act and CICRA are not the data-protection law named; the PSS Act is relevant but is not a data-protection "
      "law.",
  facts=[fact("The provisions (as amended from time to time) of the Information Technology Act, 2000, Digital Personal "
              "Data Protection Act, 2023, and other legal requirements. The jurisdiction of legal settlement would be "
              "within India", B_DBC)])

Q("008", "B-DIG08-02", T, MIB, "Intermediate",
  "A bank offers only a 'view only' digital banking facility. Under RBI's Digital Banking Channels Authorisation "
  "Directions, which of the following can it offer through this facility?",
  ["Downloadable application forms for a loan", "A personal loan sanctioned and disbursed online",
   "An IMPS transfer to another bank", "A bill payment from the savings account"],
  concept="View-only versus transactional facility",
  explanation="A view-only facility allows only services that do not alter the customer's assets or liabilities, such "
              "as balance enquiry, balance viewing and statement download. Loans, fund transfers and other facilities "
              "that create a liability or move funds cannot be provided, though downloadable forms for them can.",
  steps=["View only → no change in assets/liabilities", "Loans, transfers, payments → transactional facility needed",
         "Downloadable forms → allowed"],
  why="Loans, IMPS transfers and bill payments move funds or create liabilities, so they need a transactional facility.",
  facts=[fact("View Only Banking Facility – A feature of digital banking channels which only allows banking services "
              "that do not alter the asset or liability of the customer viz. balance enquiry, balance viewing, account "
              "statement download, etc. Note: Loans, funds transfers, and other such facilities ... cannot be provided "
              "by banks having view only facility over digital channels. However, banks providing view only facility "
              "can provide downloadable forms for such facilities", B_DBC)])

Q("008", "B-DIG08-03", T, MIB, "Intermediate",
  "Under RBI's Digital Banking Channels Authorisation Directions, what must a bank ensure when it offers mobile "
  "banking through USSD or SMS rather than a mobile app?",
  ["The service must be network independent, usable by customers of all mobile network operators",
   "The service must be limited to customers of a single partner telecom operator",
   "The service must be restricted to balance enquiry only",
   "The service must be offered only to customers with smartphones"],
  concept="Mobile banking channels",
  explanation="The Directions define mobile banking to include mobile applications, USSD and SMS. A bank offering "
              "mobile banking other than through apps must ensure that customers across mobile network operators can "
              "use it, i.e. the service must be network independent.",
  steps=["Mobile banking = apps + USSD + SMS", "Non-app service → network independent"],
  why="Tying the service to one operator, to balance enquiry or to smartphones contradicts the rule and the purpose of "
      "USSD/SMS banking.",
  facts=[fact("Banks offering mobile banking service (other than through mobile applications) must ensure that "
              "customers across mobile network operators can avail of the service, i.e., the service shall be network "
              "independent", B_DBC)])

Q("008", "B-DIG08-04", T, CBDC, "Intermediate",
  "According to RBI's Digital Rupee FAQs (updated October 2026), how many participants, banks and non-banks, were in "
  "the wholesale e₹ (e₹-W) pilot?",
  ["16", "19", "9", "4"],
  concept="Wholesale CBDC pilot",
  explanation="The FAQs say there are currently 16 participants in the e₹-W pilot, including banks and non-banks. "
              "Separately, 19 banks offer retail CBDC wallets, and e₹-W has four use cases.",
  steps=["e₹-W pilot participants → 16"],
  why="19 is the number of banks offering retail wallets; 4 is the number of e₹-W use cases; 9 has no basis.",
  current=ca("2026-10-01"),
  facts=[fact("Currently, there are 16 participants in the e₹-W pilot, which includes banks and non-banks", B_ERS)])

Q("008", "B-DIG08-05", T, MIB, "Intermediate",
  "When a bank releases a new version of its mobile banking app, RBI's Digital Payment Security Controls Directions, "
  "2026 require it to deactivate older versions within what time?",
  ["In a phased, time-bound manner not exceeding six months from the release of the newer version",
   "Within 30 days of the release of the newer version", "Within one year of the release of the newer version",
   "Only when customers voluntarily update the app"],
  concept="Mobile app version control",
  explanation="Banks must deactivate older application versions in a phased but time-bound manner, not exceeding six "
              "months from the date of release of a newer version, so that only one version (apart from the overlap "
              "period) is maintained on each platform.",
  steps=["New version released → old one deactivated within 6 months", "One version per platform"],
  why="30 days and one year are not the prescribed limit, and leaving it to customers defeats the control.",
  facts=[fact("deactivating older application versions in a phased but time-bound manner (not exceeding six months "
              "from the date of release of newer version) i.e., maintaining only one version (excluding the overlap "
              "period while phasing out older version) of the mobile application on a platform / operating system",
              B_DPSC)])

Q("008", "B-DIG08-06", T, MIB, "Intermediate",
  "Under RBI's Digital Payment Security Controls Directions, 2026, when must a bank's mobile application require the "
  "user to re-authenticate?",
  ["Each time the user launches the app, and whenever the device or app remains unused for a designated period",
   "Only once, at the time of first registration on the device", "Only for transactions above ₹10,000",
   "Only when the user changes the mobile handset"],
  concept="Re-authentication in mobile apps",
  explanation="The mobile application shall require re-authentication whenever the device or application remains "
              "unused for a designated period and each time the user launches it. It must also not store passwords or "
              "keys on the device and must wipe sensitive data from memory when the user exits.",
  steps=["Every launch → re-authenticate", "Idle for designated period → re-authenticate"],
  why="One-time authentication, amount thresholds or handset change alone do not meet the requirement.",
  facts=[fact("The mobile application shall require re-authentication whenever the device or application remains "
              "unused for a designated period and each time the user launches the application", B_DPSC)])

Q("008", "B-DIG08-07", T, MIB, "Advanced",
  "Consider the following statements about the eligibility criteria for a commercial bank to launch a transactional "
  "digital banking facility under RBI's Digital Banking Channels Authorisation Directions, 2025:\n"
  "I. The bank's 'Gap Assessment and Internal Controls Adequacy' (GAICA) report must be certified by CERT-In "
  "empanelled third-party auditor(s).\n"
  "II. The bank must meet the minimum paid-up capital or net worth under its licensing requirement as on 31 March of "
  "the immediately preceding financial year.\n"
  "III. A bank that has implemented Core Banking Solution is exempt from the minimum CRAR requirement for this "
  "purpose.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II only", "I and III only", "I, II and III"],
  concept="Eligibility for transactional digital banking",
  explanation="Besides CBS with IPv6-enabled public-facing IT, the bank must comply with the minimum regulatory CRAR, "
              "meet the minimum paid-up capital/net worth, show adequate financial and technical capability, and have "
              "a satisfactory compliance record, assessed through a GAICA report certified by CERT-In empanelled "
              "auditor(s) and the IS audit reports. The paid-up capital/net worth is tested as on 31 March of the "
              "immediately preceding financial year. CBS does not exempt a bank from the CRAR condition.",
  steps=["I: correct", "II: correct", "III: wrong – CRAR compliance is a separate condition"],
  why="Statement III is false; 'II only' omits the correct statement I.",
  facts=[fact("b) Compliance with minimum regulatory CRAR requirement. c) Minimum paid up capital/Net worth as per the "
              "applicable licensing requirement (as amended from time to time), as on March 31st of the immediately "
              "preceding financial year ... GAICA Report with respect to the technological controls prescribed in para "
              "8 of these Directions. The report shall be certified by (third party) CERT-In empaneled auditor(s)",
              B_DBC)])

Q("008", "B-DIG08-08", T, MIB, "Advanced",
  "RBI's Authentication Directions, 2025 require at least two factors of authentication for digital payments, with "
  "listed exemptions. Which of the following card transactions still requires two-factor authentication?",
  ["The first transaction under a new recurring e-mandate on a credit card",
   "The third monthly debit under an e-mandate already registered on a credit card",
   "A payment made from a gift PPI", "A small-value contactless card payment at a shop"],
  concept="Exemptions from two-factor authentication",
  explanation="Annex 1 of the Directions lists exemptions in force, including small-value contactless card "
              "transactions, recurring transactions other than the first under the e-mandate framework, NETC "
              "transactions, select PPIs (PPI-MTS, gift PPIs) and small-value offline payments. The first transaction "
              "of an e-mandate is not exempt.",
  steps=["Recurring e-mandate debits after the first → exempt", "First e-mandate transaction → needs two factors",
         "Gift PPIs and small-value contactless → exempt"],
  why="The other three are on RBI's list of exemptions.",
  facts=[fact("Existing exemptions from the requirement of at least two factors of authentication: 1. Small-value "
              "Contactless Card transactions 2. Recurring transactions (other than the first) under the e-mandate "
              "framework 3. Select Prepaid Instruments such as PPI-MTS and Gift PPIs", B_AUTH)])

Q("008", "B-DIG08-09", T, CBDC, "Advanced",
  "RBI's Digital Rupee FAQs list four present use cases of the wholesale e₹ (e₹-W). Which of the following is NOT one "
  "of them?",
  ["Inter-bank settlement of UPI transactions",
   "Settlement of inter-bank lending and borrowing in the call money market",
   "Tokenised issuance and settlement of Certificates of Deposit",
   "Tokenised issuance and settlement of corporate bonds"],
  concept="Wholesale CBDC use cases",
  explanation="The four e₹-W use cases are funds settlement of secondary-market government securities transactions, "
              "settlement of call money market lending and borrowing, tokenised issuance and settlement of CDs, and "
              "tokenised issuance and settlement of corporate bonds. UPI settlement is not among them.",
  steps=["e₹-W: G-sec settlement, call money, tokenised CDs, tokenised corporate bonds"],
  why="Call money, tokenised CDs and tokenised corporate bonds are all listed use cases.",
  current=ca("2026-10-01"),
  facts=[fact("Presently, there are four use cases of e₹-W – (i) funds settlement of secondary market transactions in "
              "Government Securities, (ii) settlement of inter-bank lending and borrowing in call money market, (iii) "
              "tokenised issuances and settlements of Certificates of Deposit, and (iv) tokenised issuance and "
              "settlement of Corporate Bonds", B_ERS)])

# ---- batch 009 (Basic 3, Intermediate 2, Advanced 5)
Q("009", "B-DIG09-01", T, CBDC, "Basic",
  "On which mobile operating systems is the retail e₹ wallet available, according to RBI's Digital Rupee FAQs?",
  ["Both Android and iOS", "Android only", "iOS only", "Only on feature phones through USSD"],
  concept="e₹ wallet platforms",
  explanation="RBI's FAQs state that the e₹ wallet is available and supported on both Android and iOS devices; users "
              "download the e₹ app of a participating bank or non-bank from the Play Store or App Store.",
  steps=["e₹ wallet → Android and iOS"],
  why="It is not limited to one platform, and RBI does not describe a USSD-only wallet.",
  facts=[fact("e₹ wallet is available and supported both on Android and iOS mobile devices", B_ERS)])

Q("009", "B-DIG09-02", T, CBDC, "Basic",
  "Can a user load e₹ from a bank account into an e₹ wallet, or redeem it back, outside banking hours?",
  ["Yes, 24 hours a day, 7 days a week", "No, only during the bank's working hours",
   "Only on working days, from 8 AM to 8 PM", "Only through a bank branch"],
  concept="Availability of the retail e₹",
  explanation="RBI's FAQs say e₹ can be loaded, redeemed or transferred between one's bank account and the e₹ wallet "
              "24x7.",
  steps=["Load/redeem/transfer → 24x7"],
  why="There is no banking-hours or branch restriction.",
  facts=[fact("Yes. e₹ can be loaded / redeemed / transferred from / to one's bank account to / from the e₹ wallet 24 "
              "hours x 7 days a week", B_ERS)])

Q("009", "B-DIG09-03", T, CBDC, "Basic",
  "A user has a dispute about an e₹ (digital rupee) transaction. According to RBI's Digital Rupee FAQs, how can she "
  "raise it?",
  ["Through her e₹ wallet app or by contacting the wallet provider's customer care",
   "Only by filing a complaint at an RBI regional office", "Only through the RBI Ombudsman directly",
   "Only by writing to the Department of Currency Management"],
  concept="Dispute resolution for e₹",
  explanation="RBI's FAQs say users can raise disputes via their e₹ wallet app or reach out to their customer care "
              "centre, i.e. with the bank or non-bank providing the wallet.",
  steps=["e₹ dispute → wallet app or provider's customer care"],
  why="RBI does not require users to go first to its offices, the Ombudsman or a central department.",
  facts=[fact("Users can raise disputes via their e₹ wallet app or reach out to their customer care centre", B_ERS)])

Q("009", "B-DIG09-04", T, MIB, "Intermediate",
  "Under RBI's Authentication Directions, 2025, if a customer suffers a loss from a digital payment effected without "
  "complying with these Directions, who bears it?",
  ["The issuer, which must compensate the customer in full without demur",
   "The customer, unless he reports it within three days", "The payment system operator such as NPCI",
   "The merchant who accepted the payment"],
  concept="Liability for non-compliant authentication",
  explanation="The Directions state that if any loss arises out of transactions effected without complying with them, "
              "the issuer shall compensate the customer for the loss in full without demur.",
  steps=["Non-compliant authentication + loss → issuer compensates fully"],
  why="The rule places the loss on the issuer, not on the customer, network operator or merchant.",
  facts=[fact("If any loss arises out of transactions effected without complying with these directions, the issuer "
              "shall compensate the customer for the loss in full without demur", B_AUTH)])

Q("009", "B-DIG09-05", T, MIB, "Intermediate",
  "RBI's Digital Payment Security Controls Directions, 2026 require banks to provide which facility on their mobile "
  "and internet banking applications?",
  ["A mechanism for customers, with authentication, to mark a transaction as fraudulent for immediate notification "
   "to the bank", "An option for customers to reverse any transaction themselves within 24 hours",
   "A facility to switch off all authentication for small payments", "A chat facility with RBI's Ombudsman"],
  concept="Customer fraud reporting in digital channels",
  explanation="Banks must let customers, with necessary authentication, identify or mark a transaction as fraudulent in "
              "the app or internet banking for seamless and immediate notification, and should build capability to "
              "report it instantly to the beneficiary's bank.",
  steps=["In-app 'mark as fraud' → immediate notice to bank → onward reporting to beneficiary entity"],
  why="Self-reversal, switching off authentication and an Ombudsman chat are not required.",
  facts=[fact("The bank shall provide a mechanism on its mobile and internet banking application for its customers, "
              "with necessary authentication, to identify / mark a transaction as fraudulent for seamless and immediate "
              "notification to the bank", B_DPSC)])

Q("009", "B-DIG09-06", T, MIB, "Advanced",
  "Bank P received RBI's approval for mobile banking in 2024, before the Digital Banking Channels Authorisation "
  "Directions, 2025 took effect. Bank Q received approval for a transactional facility under these Directions in March "
  "2026. Both now wish to launch internet banking. Which statement is correct?",
  ["Q may launch it under its existing approval; P must first ensure it meets the eligibility criteria (CBS/IPv6, CRAR, "
   "capital, financial and technical capability) and send a GAICA report for the new channel within 30 days of its "
   "decision", "Both must apply afresh to RBI for prior approval of internet banking",
   "Both may launch it without any further step, since each already has an approval",
   "P may launch it freely, but Q must seek fresh approval because its approval was channel-specific"],
  concept="Scope of approval for digital channels",
  explanation="Once approval is granted under the 2025 Directions, a bank can provide all types of digital banking "
              "channels, so Q needs nothing more. A bank approved for a particular channel before the Directions "
              "applied must ensure compliance with criteria 7.1(a) to (d) before launching any other channel and send "
              "the GAICA report (certified by CERT-In empanelled auditors) for the new channel to RBI's Department of "
              "Regulation through PRAVAAH within thirty days of the decision to launch.",
  steps=["Approval under the 2025 Directions → all channels (Q)",
         "Pre-2026 channel-specific approval → meet 7.1(a)–(d) + GAICA report within 30 days (P)"],
  why="Neither bank needs a fresh prior approval; P cannot launch without meeting the criteria; Q's approval is not "
      "channel-specific.",
  facts=[fact("Once an approval is granted under these Directions, the bank can provide all types of digital banking "
              "channels. If a bank had received approval for a particular digital banking channel (like mobile banking) "
              "before the date of applicability of these Directions, it shall ensure compliance to the eligibility "
              "criteria as detailed in para 7.1(a) to (d) above before launching any other digital banking channel. "
              "Further, the GAICA Report ... shall be sent to the Department of Regulation ... within thirty days from "
              "the decision to launch the facility", B_DBC)])

Q("009", "B-DIG09-07", T, MIB, "Advanced",
  "Consider the following statements about cross-border card transactions under RBI's Authentication Directions, "
  "2025:\n"
  "I. The two-factor and other principles of the Directions apply in full to all cross-border digital payments.\n"
  "II. By 1 October 2026, card issuers had to put in place a mechanism to validate non-recurring cross-border "
  "card-not-present transactions where authentication is requested by an overseas merchant or acquirer.\n"
  "III. For this purpose, card issuers must register their Bank Identification Numbers (BINs) with the card "
  "networks.\n"
  "Which of the above is/are correct?",
  ["II and III only", "I and II only", "III only", "I, II and III"],
  concept="Authentication of cross-border CNP transactions",
  explanation="The Directions apply to domestic digital payments and are not applicable to cross-border transactions. "
              "However, card issuers had to set up, by 1 October 2026, a mechanism to validate non-recurring "
              "cross-border card-not-present transactions where the overseas merchant or acquirer raises an "
              "authentication request, register their BINs with card networks, and adopt a risk-based mechanism for "
              "all cross-border CNP transactions.",
  steps=["I: wrong – the Directions cover domestic transactions", "II: correct", "III: correct"],
  why="Statement I is false, which rules out options containing it; 'III only' omits the correct statement II.",
  current=ca("2026-10-01"),
  facts=[fact("The directions outlined above are not applicable to cross-border digital payment transactions. However, "
              "card issuers shall, by October 01, 2026, put in place a mechanism to validate non-recurring, "
              "cross-border card not present (CNP) transactions, where request for authentication is raised by an "
              "overseas merchant or overseas acquirer. To ensure compliance, card issuers shall register their Bank "
              "Identification Numbers (BINs) with card networks", B_AUTH)])

Q("009", "B-DIG09-08", T, MIB, "Advanced",
  "A bank allows its customers to register the mobile banking app on more than one device. Under RBI's Digital Payment "
  "Security Controls Directions, 2026, which of the following must it do?\n"
  "I. Bind the app to the device using a combination of hardware, software and service information.\n"
  "II. Notify the user of every new device registration on multiple channels, such as the registered mobile number, "
  "e-mail or a phone call.\n"
  "III. Keep a record of all registered devices and give the user a facility to disable a registered device.\n"
  "IV. Limit the user to a maximum of two registered devices.",
  ["I, II and III only", "I and II only", "II, III and IV only", "I, II, III and IV"],
  concept="Device binding of mobile apps",
  explanation="Banks must ensure device binding through a combination of hardware, software and service information. "
              "Where multiple devices are allowed, the user must be notified of every new device registration on "
              "multiple channels, and the bank must keep a record of all registered devices with a facility for the "
              "user to disable any of them. No numerical cap on devices is prescribed.",
  steps=["I, II, III → required", "IV → no such cap in the Directions"],
  why="Options with IV add a cap RBI has not set; 'I and II only' leaves out the device-record requirement.",
  facts=[fact("The bank shall ensure device binding of the mobile application. Device binding shall be implemented "
              "through a combination of hardware, software, and service information. In case, the bank allows multiple "
              "devices to be registered, then, (i) the user shall be notified of every new device registration on "
              "multiple channels such as registered mobile number, email, or phone call, and (ii) in relation to the "
              "mobile application, the bank shall maintain a record of all registered devices, providing the user a "
              "facility to disable a registered device", B_DPSC)])

Q("009", "B-DIG09-09", T, MIB, "Advanced",
  "RBI's Digital Payment Security Controls Directions, 2026 make some mobile-app controls mandatory ('shall') and leave "
  "others to the bank's discretion ('may'). Which of the following are mandatory?\n"
  "I. Hosting the checksum of the current active version of the app on a public platform.\n"
  "II. Checking whether the phone is rooted or jailbroken before the app is installed.\n"
  "III. Not storing user IDs, passwords or keys on the device.\n"
  "IV. Implementing alternatives to SMS-based OTP.",
  ["I and III only", "I, II and III only", "II and IV only", "III only"],
  concept="Mandatory and optional mobile-app controls",
  explanation="Banks shall host the checksum of the current active app version publicly, and the app shall not store "
              "sensitive authentication information such as user IDs, passwords, keys or hashes on the device. By "
              "contrast, a bank 'may explore' a rooted/jailbroken-device check and 'may implement' alternatives to "
              "SMS-based OTP.",
  steps=["Checksum hosting → shall", "No storing credentials on device → shall", "Rooted check → may explore",
         "Alternatives to SMS OTP → may"],
  why="II and IV are optional; 'III only' misses the mandatory checksum.",
  facts=[fact("The bank shall host the checksum of current active version of its mobile application on public platform "
              "so that users can verify the same", B_DPSC),
         fact("The bank may explore the feasibility of implementing a code that checks if the device is rooted / "
              "jailbroken prior to the installation of the mobile application ... The bank may implement alternatives "
              "to SMS-based OTP authentication mechanisms ... The mobile application shall not store / retain "
              "sensitive personal / customer authentication information such as user IDs, passwords, keys, hashes",
              B_DPSC)])

Q("009", "B-DIG09-10", T, MIB, "Advanced",
  "Consider the following statements about the principles in RBI's Authentication Directions, 2025:\n"
  "I. For every digital payment, including card-present transactions, at least one authentication factor must be "
  "dynamically created or proven.\n"
  "II. Issuers may apply checks beyond the minimum two factors based on behavioural or contextual parameters such as "
  "location, device attributes and transaction history.\n"
  "III. Issuers may, at their discretion, offer customers a choice of authentication factors.\n"
  "Which of the above is/are correct?",
  ["II and III only", "I and II only", "I and III only", "I, II and III"],
  concept="Principles of authentication",
  explanation="The dynamic-factor rule applies to digital payments other than card-present transactions, so statement "
              "I is wrong. Issuers may use risk-based checks on behavioural and contextual parameters beyond the "
              "two-factor minimum (and may explore DigiLocker for high-risk transactions), and may offer customers a "
              "choice of factors.",
  steps=["I: wrong – card-present transactions are outside the dynamic-factor rule", "II: correct", "III: correct"],
  why="Every option containing statement I is wrong.",
  facts=[fact("It shall be ensured that for digital payment transactions, other than card present transactions, at "
              "least one of the factors of authentication is dynamically created or proven", B_AUTH),
         fact("Issuers may, in line with their internal risk management policies, identify transactions for evaluation "
              "against behavioural / contextual parameters ... additional checks beyond the minimum two-factor "
              "authentication may be resorted to; Issuers may, at their discretion, offer a choice of authentication "
              "factors to their customers", B_AUTH)])

# ---- batch 010 (Basic 3, Intermediate 1, Advanced 1)
Q("010", "B-DIG10-01", T, MIB, "Basic",
  "Under RBI's Digital Payment Security Controls Directions, 2026, what must a bank do about fake or malicious apps with "
  "names or features similar to its own mobile banking app?",
  ["Actively monitor popular app stores and the web for them and respond to get them taken down",
   "Nothing, as app stores alone are responsible", "Report them only in its annual report",
   "Ask customers to verify apps by visiting a branch"],
  concept="Rogue mobile apps",
  explanation="Banks must institute a mechanism to actively monitor popular app stores and the web for non-genuine, "
              "unauthorised or malicious applications with similar names or features, and respond appropriately to "
              "bring them down. They must also publish the checksum of their genuine app.",
  steps=["Monitor app stores and the web → act to take down rogue apps"],
  why="The duty lies with the bank and calls for active monitoring and takedown, not passive reporting.",
  facts=[fact("The bank shall institute a mechanism to actively monitor for non-genuine / unauthorised / malicious "
              "applications (with similar name / features) on popular app-stores and the web and respond appropriately "
              "to bring them down", B_DPSC)])

Q("010", "B-DIG10-02", T, MIB, "Basic",
  "By what date did RBI require all payment system providers and participants to comply with its Authentication "
  "mechanisms for digital payment transactions Directions, 2025 (unless a provision specified otherwise)?",
  ["1 April 2026", "1 January 2026", "25 September 2025", "1 October 2026"],
  concept="Authentication Directions, 2025",
  explanation="The Directions, dated 25 September 2025 and issued under the PSS Act, 2007, required all payment system "
              "providers and participants, banks and non-banks, to comply by 1 April 2026. A separate deadline of 1 "
              "October 2026 applied to cross-border card-not-present validation.",
  steps=["Issued 25 Sep 2025", "General compliance date: 1 Apr 2026"],
  why="25 September 2025 is the date of issue; 1 October 2026 is the cross-border CNP deadline; 1 January 2026 is not "
      "the date.",
  current=ca("2026-04-01"),
  facts=[fact("All Payment System Providers and Payment System Participants, including banks and non-bank entities, "
              "shall ensure compliance with these directions by April 01, 2026, unless indicated otherwise for any "
              "specific provision herein", B_AUTH)])

Q("010", "B-DIG10-03", T, CBDC, "Basic",
  "An entity wishes to test a CBDC-related use case in RBI's CBDC and Asset Tokenisation (CAT) Sandbox. To which "
  "department of RBI should it send its request?",
  ["FinTech Department", "Department of Currency Management", "Department of Payment and Settlement Systems",
   "Consumer Education and Protection Department"],
  concept="CAT Sandbox",
  explanation="RBI's FAQs say interested entities submit a detailed request to the FinTech Department, RBI, by e-mail; "
              "after assessment and due diligence, the FinTech Department decides on granting access to the "
              "non-live sandbox environment.",
  steps=["CAT Sandbox requests → FinTech Department, RBI"],
  why="The other departments do not handle CAT Sandbox access.",
  facts=[fact("Interested entities can submit their detailed request to the FinTech Department, RBI for accessing the "
              "CAT Sandbox by email at rbicbdcsandbox@rbi.org.in", B_ERS)])

Q("010", "B-DIG10-04", T, MIB, "Intermediate",
  "A customer pays an online merchant through a payment aggregator. Under RBI's Digital Payment Security Controls "
  "Directions, 2026, whose name should the bank's alert and OTP for this transaction show?",
  ["The merchant's name, wherever applicable", "The payment aggregator's name",
   "The card network's name", "Only the bank's own name"],
  concept="Alerts and OTPs",
  explanation="Alerts and OTPs received by the customer for online transactions shall identify the merchant name, "
              "wherever applicable, rather than the payment aggregator through which the transaction was effected, so "
              "that the customer can recognise the payment.",
  steps=["Alert/OTP → merchant name, not the aggregator"],
  why="Showing the aggregator, network or only the bank defeats the purpose of identifying the payee.",
  facts=[fact("The alerts and OTPs received by the customer for online transactions shall identify the merchant name, "
              "wherever applicable, rather than the payment aggregator through which the transaction was effected",
              B_DPSC)])

Q("010", "B-DIG10-05", T, MIB, "Advanced",
  "Consider the following statements about customer conduct rules in RBI's Digital Banking Channels Authorisation "
  "Directions, 2025:\n"
  "I. Banks must obtain the customer's explicit consent, duly recorded, for registering or de-registering for digital "
  "banking services.\n"
  "II. Terms and conditions for registration should be in clear and simple language, preferably in English, Hindi and "
  "the local language.\n"
  "III. Banks may obtain and record the mobile numbers of all customers to send transaction and other alerts.\n"
  "Which of the above is/are correct?",
  ["I, II and III", "I and II only", "I only", "II and III only"],
  concept="Customer conduct in digital banking",
  explanation="All three reproduce the Directions: explicit, recorded consent for registration (para 10.1); terms in "
              "clear, simple language, preferably English, Hindi and the local language (para 10.3); and, although no "
              "digital channel may be made compulsory for other facilities, banks can obtain and record mobile numbers "
              "of all customers to send alerts (para 10.5).",
  steps=["I: correct", "II: correct", "III: correct"],
  why="Each of the other options leaves out at least one correct statement.",
  facts=[fact("Banks shall obtain explicit consent from the customer for registering/de-registering (in case of existing "
              "customers) for digital banking services and the consent shall be duly recorded/documented; For "
              "registration, banks shall provide the terms and conditions in clear and simple language (preferably in "
              "English, Hindi, and the local language)", B_DBC),
         fact("The banks can, however, obtain and record mobile numbers of all customers to send transaction or other "
              "alerts", B_DBC)])


# ####################################################################################################
# ===== UPI, NEFT, RTGS, IMPS, NPCI
# ####################################################################################################
# ===================================================================== PART C: UPI, NEFT, RTGS, IMPS, NPCI
# Sources (all opened with a plain client on 2026-11-06 unless listed in SEARCH_ONLY)
C_NEFT = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id=60"          # NEFT FAQs (updated Sep 2, 2024)
C_INRF = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id=67"          # Indo-Nepal Remittance Facility FAQs (Sep 27, 2023)
C_LEI = "https://www.rbi.org.in/Scripts/FAQView.aspx?Id=140"             # LEI for large value transactions FAQs
C_RTGS = "https://www.rbi.org.in/Scripts/FAQDisplay.aspx?Id=65"          # RTGS FAQs (updated Oct 14, 2026)
C_PSR = "https://www.rbi.org.in/Scripts/PublicationsView.aspx?id=23813"  # Payment Systems Report, Dec 2025 (May 18, 2026)
C_TAT = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11693"  # TAT for failed transactions (Sep 20, 2019)
C_EMAND = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13374"  # E-mandate Framework, 2026 (Apr 21, 2026)
C_AUTH = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12898"   # Authentication Directions, 2025
C_PPI = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12156"    # MD on PPIs (updated Sep 30, 2026)
C_OFFL = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12215&Mode=0"  # Offline payments framework (Dec 4, 2024)
C_AEPS = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12877"   # AePS touchpoint operators directions
C_BBPS = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12616"   # BBPS Directions, 2024
C_UPIAUG = ("https://www.theweek.in/news/biz-tech/2025/08/01/major-upi-changes-from-august-1-here-is-the-full-list-"
            "of-balance-enquiry-limits-pending-payment-status-upi-security-and-more-from-npci.html")
C_123 = "https://www.outlookmoney.com/news/rbi-enhances-transaction-limits-for-upi-lite-and-upi123pay-know-details"

# ================= NEFT (008: B2 I1 A1; 009: B1 I2 A1; 010: B1 I2 A1)
T = "NEFT"
S = "Settlement and timings"
Q("008", "C-NEFT08-01", T, S, "Basic",
  "From which date have banks been advised not to levy any charges on their savings bank account holders for NEFT "
  "transfers initiated online?",
  ["1 January 2020", "1 July 2019", "16 December 2019", "1 April 2020"],
  concept="NEFT charges for savings account holders",
  explanation="RBI's NEFT FAQs say that, to give impetus to digital retail payments, banks were advised not to levy any "
              "charges from savings bank account holders for NEFT transfers initiated online with effect from 1 "
              "January 2020. Separately, RBI stopped levying its own processing charges on member banks from 1 July "
              "2019.",
  steps=["Online NEFT by savings account holders → free from 1 January 2020"],
  why="1 July 2019 is when RBI stopped charging member banks; 16 December 2019 is when NEFT became 24x7; 1 April 2020 "
      "is not a date RBI gives.",
  facts=[fact("banks have been advised to not levy any charges from their savings bank account holders for NEFT funds "
              "transfers initiated online with effect from January 01, 2020", C_NEFT)])
Q("008", "C-NEFT08-02", T, S, "Basic",
  "The Indo-Nepal Remittance Facility (INRF) Scheme, which uses the NEFT system to send money from India to Nepal, was "
  "launched by RBI in:",
  ["May 2008", "November 2005", "August 2021", "December 2019"],
  concept="Indo-Nepal Remittance Facility",
  explanation="RBI's INRF FAQs say the scheme was launched in May 2008 to give migrant Nepalese workers in India a safe "
              "and cost-efficient way to send money home. It was enhanced in August 2021.",
  steps=["INRF launched May 2008", "Enhanced August 2021"],
  why="November 2005 is when NEFT itself started; August 2021 is the enhancement; December 2019 is NEFT going 24x7.",
  facts=[fact("The scheme was launched by the Reserve Bank of India (RBI) in May 2008 to provide a safe and "
              "cost-efficient avenue to migrant Nepalese workers in India to remit money back to their families in "
              "Nepal", C_INRF)])
Q("008", "C-NEFT08-03", T, S, "Intermediate",
  "Under the Indo-Nepal Remittance Facility Scheme, a beneficiary in Nepal without a Nepal SBI Ltd account is to collect "
  "cash from the money transfer company's outlet. What happens if the beneficiary does not approach the company within "
  "a week from the date of the transaction?",
  ["The money transfer company arranges to return the remittance to the originator in India",
   "The amount is credited to a suspense account of Nepal SBI Ltd until claimed",
   "The amount is converted into a fixed deposit in the beneficiary's name",
   "The remittance is forfeited and transferred to a depositor education fund"],
  concept="Return of undelivered INRF remittances",
  explanation="RBI's FAQs say that if the beneficiary does not approach the money transfer company within a week, the "
              "company arranges for the return of the remittance to the originator. The money flows back through NEFT "
              "to the originating branch, which credits the remitter's account (or refunds a walk-in remitter against "
              "the counterfoil).",
  steps=["No collection within a week", "Remittance returned to the originator through NEFT"],
  why="There is no suspense parking, conversion into a deposit or forfeiture in the scheme.",
  facts=[fact("If the beneficiary does not approach the money transfer company within a week from the date of the "
              "transaction, the money transfer company would make arrangements for return of the remittance to the "
              "originator", C_INRF)])

w1, w2 = 4000, 20000
orig, sbi = 5, 20
extra = lambda amt: 50 if amt <= 5000 else 75  # noqa: E731
total = sum(orig + sbi + extra(a) for a in (w1, w2))
assert total == 175 and (orig + sbi) * 2 + 50 * 2 == 150
Q("008", "C-NEFT08-04", T, S, "Advanced",
  "A walk-in customer sends two remittances to Nepal under the Indo-Nepal Remittance Facility: ₹4,000 to his mother and "
  "₹20,000 to his brother. Neither beneficiary has an account with Nepal SBI Ltd. Using the charges in RBI's INRF FAQs "
  "for remittances up to ₹50,000 (taking the originating bank's maximum), what are the total charges for the two "
  "remittances?",
  ["₹175", "₹150", "₹50", "₹200"],
  concept="INRF charges",
  explanation="For each remittance up to ₹50,000 the originating bank may charge at most ₹5 and SBI charges ₹20 (shared "
              "₹10 each with Nepal SBI Ltd). If the beneficiary has no NSBL account, a further ₹50 applies for "
              "remittances up to ₹5,000 and ₹75 above ₹5,000. So ₹4,000 → 5 + 20 + 50 = ₹75 and ₹20,000 → 5 + 20 + 75 "
              "= ₹100; total ₹175.",
  steps=["₹4,000: 5 + 20 + 50 = ₹75", "₹20,000: 5 + 20 + 75 = ₹100", "Total = ₹175"],
  why="₹150 applies the ₹50 slab to both; ₹50 ignores the cash-delivery charge; ₹200 applies ₹75 to both.",
  computed=True,
  facts=[fact("Originating bank – Maximum ₹5/- per transaction. State Bank of India – ₹20/- per transaction ... In case "
              "the beneficiary does not maintain an account with NSBL then, an additional amount would be charged- "
              "₹50/- for remittances up to ₹5,000/- and ₹75/- for remittance above ₹5,000/-", C_INRF)])

Q("009", "C-NEFT09-01", T, S, "Basic",
  "Under the Indo-Nepal Remittance Facility Scheme, if the beneficiary does not have an account with Nepal SBI Ltd or "
  "lives in an area not served by its branches, cash in Nepalese rupees is delivered through:",
  ["Prabhu Money Transfer", "Nepal Rastra Bank", "India Post Payments Bank", "Western Union"],
  concept="Cash delivery under INRF",
  explanation="RBI's FAQs say Nepal SBI Ltd (NSBL) has an arrangement with a money transfer company in Nepal, Prabhu "
              "Money Transfer, which delivers cash in Nepalese rupees to beneficiaries without an NSBL account or in "
              "areas not served by NSBL branches.",
  steps=["Beneficiary has NSBL account → credit to account", "Otherwise → cash through Prabhu Money Transfer"],
  why="Nepal Rastra Bank is Nepal's central bank; IPPB and Western Union are not part of the INRF arrangement.",
  facts=[fact("an arrangement has been entered into by NSBL with a money transfer company in Nepal (called Prabhu Money "
              "Transfer) who would make arrangements for delivery of cash (in Nepalese Rupees) to the beneficiary",
              C_INRF)])
Q("009", "C-NEFT09-02", T, S, "Intermediate",
  "In August 2021, RBI enhanced the Indo-Nepal Remittance Facility Scheme. According to RBI's FAQs, the enhancement "
  "was meant to:",
  ["Boost trade payments between India and Nepal and facilitate retirement and pension payments to ex-servicemen "
   "settled in Nepal",
   "Allow remittances from Nepal to India through NEFT for the first time",
   "Let Nepalese banks become direct members of India's NEFT system",
   "Shift the scheme from NEFT to UPI for all remittances"],
  concept="INRF enhancement of 2021",
  explanation="The scheme, started in May 2008 for migrant Nepalese workers, was enhanced in August 2021 to boost trade "
              "payments between the two countries and to facilitate retirement, pension and similar payments to Indian "
              "ex-servicemen who have settled or relocated in Nepal. It remains one-way, from India to Nepal.",
  steps=["2008: migrant workers' remittances", "2021: trade payments + pensions of ex-servicemen in Nepal"],
  why="INRF is still one-way India-to-Nepal, Nepalese banks did not join NEFT, and it was not moved to UPI.",
  facts=[fact("In August 2021, the Scheme was enhanced to boost the trade payments between the two countries, and to "
              "facilitate payments relating to retirement, pension, etc., to our ex-servicemen who have settled / "
              "relocated in Nepal", C_INRF),
         fact("a cross-border remittance scheme to transfer funds from India to Nepal (one-way only), enabled under the "
              "NEFT ecosystem", C_INRF)])
Q("009", "C-NEFT09-03", T, S, "Intermediate",
  "A company sends ₹60 crore by NEFT to a supplier company, but the remitting bank's message does not carry the "
  "beneficiary's Legal Entity Identifier (LEI). According to RBI's FAQs on LEI, how should the beneficiary bank treat "
  "this inward transaction?",
  ["It should not reject the transaction; both banks must maintain valid, verified LEI information after credit",
   "It must reject the transaction and return it to the remitting bank within two hours",
   "It must hold the credit until the remitter furnishes the LEI",
   "It may credit the amount only if the beneficiary is an individual"],
  concept="LEI in large-value NEFT transactions",
  explanation="All single NEFT/RTGS payments of ₹50 crore and above by non-individuals must carry remitter and "
              "beneficiary LEI, and the remitting bank should ensure both are captured. But an inward transaction with "
              "inappropriate or no LEI should not be rejected by the beneficiary bank; after credit, both banks should "
              "maintain valid and verified LEI information.",
  steps=["₹60 crore, non-individuals → LEI required", "Missing LEI on inward → do not reject",
         "Post-credit → both banks maintain valid LEI"],
  why="RBI says such transactions should not be rejected or held; a company-to-company payment is not an individual "
      "transaction.",
  facts=[fact("Any inward transaction with inappropriate or no LEI should not be rejected by beneficiary bank. However, "
              "post-credit, both remitting and beneficiary banks should maintain valid and verified LEI information for "
              "all payment transactions of ₹50 crore and above", C_LEI),
         fact("All single payment transactions of ₹50 crore and above undertaken by entities (non-individuals) should "
              "include remitter and beneficiary LEI information. This is applicable to transactions undertaken through "
              "the NEFT and RTGS payment systems", C_LEI)])
Q("009", "C-NEFT09-04", T, S, "Advanced",
  "Consider the following statements based on RBI's FAQs on the Legal Entity Identifier (LEI) for large value "
  "transactions:\nI. The LEI is a 20-character alpha-numeric code, obtainable in India from Legal Entity Identifier "
  "India Ltd.\nII. In NEFT messages, the first two lines of the optional field 7495 are used to capture the sender's "
  "and the beneficiary's LEI, in that order.\nIII. In RTGS, the LEI requirement for payments of ₹50 crore and above "
  "applies to customer payments but not to inter-bank transactions.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="LEI in NEFT and RTGS",
  explanation="The LEI is a 20-character code issued by LOUs accredited by GLEIF; in India, by LEIL (I correct). In NEFT "
              "the first two lines of field 7495 carry sender and beneficiary LEI, with narration in the last four "
              "lines (II correct). In RTGS both customer payments and inter-bank transactions of ₹50 crore and above "
              "must carry LEI (III wrong).",
  steps=["I: 20 characters, LEIL → correct", "II: field 7495 lines 1-2 → correct",
         "III: RTGS inter-bank also covered → wrong"],
  why="Any option including III is wrong; 'I only' misses II.",
  facts=[fact("The Legal Entity Identifier (LEI) is a 20-character alpha-numeric code ... In India, LEI can be obtained "
              "from Legal Entity Identifier India Ltd.", C_LEI),
         fact("In NEFT payment messages, the field 7495 ... The first two lines of this field hall be used for capturing "
              "sender and beneficiary customer LEI information, in that order", C_LEI),
         fact("In case of RTGS, both customer payment and inter-bank transactions meeting the above criterion should "
              "include LEI information", C_LEI)])

Q("010", "C-NEFT10-01", T, S, "Basic",
  "A remitter wants to send money to Nepal through NEFT under the Indo-Nepal Remittance Facility. If the remitter holds "
  "an account with an NEFT-enabled bank branch in India, what additional identification documents must be submitted?",
  ["None; no additional information, documents or identification is needed",
   "Passport and visa of the remitter", "PAN card and a letter from the employer",
   "Proof of the beneficiary's account with a Nepalese bank"],
  concept="KYC under INRF",
  explanation="RBI's FAQs say a remitter who maintains an account with a bank branch in India need not give any "
              "additional information, documents or identification. A walk-in remitter must submit proof of identity "
              "such as passport, PAN, driving licence, telephone bill or employer's certificate.",
  steps=["Account holder → no extra documents", "Walk-in → proof of identity"],
  why="Identity documents are needed only from walk-in customers; the beneficiary need not hold a bank account.",
  facts=[fact("If the remitting customer maintains an account with a bank branch in India, there is no need for any "
              "additional information, documents or identification. Else, the remitter has to submit documents for "
              "proof of identification", C_INRF)])
Q("010", "C-NEFT10-02", T, S, "Intermediate",
  "A bank in India and a bank in Nepal enter into their own bilateral arrangement to handle remittances between the two "
  "countries. According to RBI's FAQs, is this arrangement covered by the Indo-Nepal Remittance Facility Scheme?",
  ["No; INRF exclusively uses the NEFT ecosystem, and bilateral arrangements are outside its guidelines",
   "Yes; all India–Nepal remittances by banks fall under INRF",
   "Yes, if the Indian bank is a public sector bank",
   "Only if the Nepalese bank is a subsidiary of an Indian bank"],
  concept="Scope of INRF",
  explanation="RBI's FAQs say bilateral arrangements between banks or non-banks to handle India–Nepal cross-border "
              "transactions are not covered by the INRF guidelines; the scheme exclusively uses the NEFT ecosystem, "
              "and all NEFT-enabled branches are already covered.",
  steps=["INRF = NEFT-based scheme only", "Bilateral arrangements → outside INRF"],
  why="RBI states plainly that bilateral arrangements are not covered, irrespective of the banks' ownership.",
  facts=[fact("No. The bilateral arrangements between banks / non-banks to handle cross-border transactions between "
              "India and Nepal are not covered under guidelines of the INRF Scheme. The INRF Scheme exclusively uses "
              "NEFT ecosystem for such remittance to Nepal", C_INRF)])
Q("010", "C-NEFT10-03", T, S, "Intermediate",
  "A walk-in customer paid cash at an Indian bank branch to send money to Nepal under INRF, but the money could not be "
  "delivered and has flowed back through NEFT. According to RBI's FAQs, how does the customer get the refund?",
  ["By producing evidence of the remittance, the counterfoil of the remittance application form",
   "It is automatically credited to any bank account the customer names later",
   "By applying to Nepal SBI Ltd, which refunds in Nepalese rupees",
   "By filing a claim with RBI's NEFT Help Desk"],
  concept="Return of INRF remittances",
  explanation="Undelivered amounts flow back through NEFT to the originating branch. If the remittance was made by debit "
              "to an account, the amount is credited back to that account; a walk-in remitter who paid cash must produce "
              "proof of remittance, the counterfoil of the application form, to get the refund.",
  steps=["Account remitter → credited back to account", "Walk-in cash remitter → refund against counterfoil"],
  why="There is no automatic credit to a new account, no refund in Nepal and no claim with RBI.",
  facts=[fact("If the remittance was made by a walk-in customer through a cash deposit, the remitter has to produce "
              "evidence of proof of remittance (counterfoil of the remittance application form) for getting refund",
              C_INRF)])
Q("010", "C-NEFT10-04", T, S, "Advanced",
  "Consider the following statements about the Indo-Nepal Remittance Facility (INRF) Scheme, based on RBI's FAQs:\n"
  "I. A sender who maintains an account with an NEFT-enabled branch faces no limit on the number of remittances in a "
  "year.\nII. Of the ₹20 charged by SBI per remittance (up to ₹50,000), ₹10 is shared with Nepal SBI Ltd.\nIII. Nepal SBI "
  "Ltd charges an additional amount for crediting a beneficiary who holds an account with it.\nWhich of the above "
  "is/are correct?",
  ["I and II only", "II only", "I and III only", "I, II and III"],
  concept="INRF features and charges",
  explanation="Account-holding senders face no limit on the number of remittances (walk-in customers are limited to 12 "
              "a year) — I is correct. SBI's ₹20 is shared with NSBL at ₹10 each — II is correct. NSBL does not charge "
              "anything extra for crediting a beneficiary who has an account with it; the extra ₹50/₹75 applies only "
              "when the beneficiary has no NSBL account — III is wrong.",
  steps=["I → correct", "II → correct", "III → wrong (extra only without NSBL account)"],
  why="Options with III are wrong; 'II only' wrongly rejects I.",
  facts=[fact("There is no limit on remittances if the sender is maintaining account with any NEFT enabled bank-branch "
              "in India", C_INRF),
         fact("State Bank of India – ₹20/- per transaction. SBI would share this ₹20/- with NSBL at ₹10 each. NSBL "
              "would not charge any additional amount for crediting the beneficiary. if he maintains an account with "
              "it", C_INRF)])

# ================= RTGS (008: B1 I1 A1; 009: B1 I1 A1; 010: B1 I2 A1)
T = "RTGS"
S = "Limits and timings"
Q("008", "C-RTGS08-01", T, S, "Basic",
  "A remitter wants to send money by RTGS but does not know the IFSC of the beneficiary's branch. Besides asking his "
  "own branch or checking RBI's website, where do RBI's RTGS FAQs say the IFSC is available?",
  ["On the cheque leaf of the beneficiary", "On the beneficiary's PAN card", "On the beneficiary's Aadhaar letter",
   "Only with NPCI's helpline"],
  concept="Finding the IFSC",
  explanation="RBI's RTGS FAQs say the IFSC can be obtained from the remitter's bank branch, is available on the "
              "beneficiary's cheque leaf (and can be communicated by the beneficiary), and is listed on RBI's website.",
  steps=["IFSC sources: own branch, beneficiary's cheque leaf, RBI website"],
  why="PAN and Aadhaar documents do not carry the IFSC; NPCI does not run RTGS.",
  facts=[fact("The IFSC number can be obtained by the remitter (customer) from his / her bank branch. Alternatively, it "
              "is available on the cheque leaf of the beneficiary", C_RTGS)])
Q("008", "C-RTGS08-02", T, S, "Intermediate",
  "Sunil has a dispute about an RTGS transaction. According to RBI's RTGS FAQs (updated October 2026), what is the "
  "correct route for his grievance?",
  ["First the bank's grievance redressal cell; if not resolved satisfactorily within the prescribed timeline, a "
   "complaint under the Reserve Bank – Integrated Ombudsman Scheme, 2026",
   "Directly to RBI's RTGS Help Desk, which decides the dispute",
   "Only a civil suit, since RTGS payments are final and irrevocable",
   "A complaint to NPCI's dispute resolution system"],
  concept="Grievance redressal for RTGS",
  explanation="The FAQs say a customer should approach the bank's grievance redressal cell with the details; if the "
              "grievance is not resolved satisfactorily within the timeline prescribed in RB-IOS 2026, a complaint may "
              "be lodged under that Scheme, which is a single reference point for complaints against RBI-regulated "
              "entities.",
  steps=["Bank's grievance cell first", "Unresolved within timeline → RB-IOS 2026"],
  why="The Help Desk is a contact point, not an adjudicator; finality of settlement does not bar complaints; NPCI "
      "does not operate RTGS.",
  facts=[fact("You may approach grievance redressal cell of your bank with details of the disputed transaction. In case "
              "your grievance is not resolved satisfactorily as per the timeline prescribed in 'The Reserve "
              "Bank-Integrated Ombudsman Scheme (RB-IOS 2026)', you may lodge a complaint under the said Scheme", C_RTGS)])

v21, v25, val21, val25 = 20, 33, 1246, 2206          # crore transactions; ₹ lakh crore
t21, t25 = val21 / v21, val25 / v25                  # ₹ lakh per transaction
assert round(t21, 1) == 62.3 and round(t25, 1) == 66.8 and t25 > t21
Q("008", "C-RTGS08-03", T, S, "Advanced",
  "According to RBI's Payment Systems Report (December 2025), RTGS handled 20 crore transactions worth ₹1,246 lakh crore "
  "in CY 2021 and 33 crore transactions worth ₹2,206 lakh crore in CY 2025. Which statement is correct?",
  ["Value grew faster than volume, so the average RTGS transaction rose from about ₹62 lakh to about ₹67 lakh",
   "Volume grew faster than value, so the average transaction fell from about ₹67 lakh to about ₹62 lakh",
   "The average transaction rose from about ₹6.2 lakh to about ₹6.7 lakh",
   "The average transaction stayed unchanged at about ₹65 lakh"],
  concept="Average ticket size in RTGS",
  explanation="Average size = value ÷ volume. CY 2021: ₹1,246 lakh crore ÷ 20 crore = ₹62.3 lakh; CY 2025: ₹2,206 lakh "
              "crore ÷ 33 crore ≈ ₹66.8 lakh. RBI reports CAGRs of 13.5% in volume and 15.3% in value, consistent with "
              "a rising average.",
  steps=["2021: 1,246 ÷ 20 = 62.3 (₹ lakh)", "2025: 2,206 ÷ 33 ≈ 66.8 (₹ lakh)", "Value CAGR 15.3% > volume 13.5%"],
  shortcut="lakh crore ÷ crore = lakh.",
  why="The average rose, not fell; ₹6.2–6.7 lakh is off by a factor of ten; it did not stay unchanged.",
  computed=True, current=ca("2026-05-18"),
  facts=[fact("RTGS transactions volume grew from 20 crore in CY 2021 to 33 crore in CY 2025, while transactions value "
              "increased from ₹1,246 lakh crore to ₹2,206 lakh crore during this period ... a CAGR of 13.5% in "
              "transaction volume and 15.3% in transaction value", C_PSR)])

Q("009", "C-RTGS09-01", T, S, "Basic",
  "Which of the following is NOT among the details a remitting customer must furnish to the bank for an RTGS "
  "remittance, according to RBI's RTGS FAQs?",
  ["The beneficiary's PAN", "The IFSC of the receiving branch", "The beneficiary's account number",
   "The account number to be debited"],
  concept="Information needed for RTGS",
  explanation="The FAQs list: the account to be debited, the beneficiary bank and branch, the IFSC of the receiving "
              "branch, the beneficiary's name and account number, any sender-to-receiver information, and the sender "
              "and beneficiary LEI for eligible transactions. The beneficiary's PAN is not required.",
  steps=["Required: debit account, beneficiary bank/branch, IFSC, beneficiary name and account, LEI if eligible",
         "Not listed: PAN"],
  why="IFSC, beneficiary account number and debit account are all on RBI's list.",
  facts=[fact("The account number to be debited; Name of the beneficiary bank and branch; The IFSC number of the "
              "receiving branch; Name of the beneficiary customer; Account number of the beneficiary customer; Sender "
              "to receiver information, if any; Sender and Beneficiary Legal Entity Identifier (for eligible "
              "transactions)", C_RTGS)])
Q("009", "C-RTGS09-02", T, S, "Intermediate",
  "According to RBI's RTGS FAQs, where are the timelines for processing applications for the services of RBI's "
  "Department of Payment and Settlement Systems under the PSS Act, 2007 published?",
  ["In RBI's Citizens' Charter", "In the RTGS System Regulations only", "In NPCI's operating circulars",
   "They are not published; each application is decided case by case"],
  concept="Service timelines under the PSS Act",
  explanation="RBI's FAQs say RBI has published a Citizens' Charter defining timelines for services offered by its "
              "departments, including those of the Department of Payment and Settlement Systems under the PSS Act, "
              "2007. The membership procedure itself is in the RTGS System Regulations.",
  steps=["Service timelines → RBI's Citizens' Charter"],
  why="The RTGS Regulations give the procedure, not the departmental service timelines; NPCI has no role here.",
  facts=[fact("RBI has published Citizens' Charter, wherein, timelines are defined for various services offered by the "
              "respective departments. The timelines for the services offered by the Department of Payment and "
              "Settlement Systems under the PSS Act, 2007 are available", C_RTGS)])
Q("009", "C-RTGS09-03", T, S, "Advanced",
  "Consider the following statements about the LEI requirement in RTGS, based on RBI's FAQs:\nI. It applies to all "
  "channels used to connect to RTGS, including thick-client, Web-API and the Payment Originator module.\nII. Ministries "
  "and Departments of the Central Government must quote their LEI for RTGS payments of ₹50 crore and above.\nIII. In "
  "RTGS messages, the sender's and beneficiary's LEIs are captured in the first two loops of the relevant optional "
  "field.\nWhich of the above is/are correct?",
  ["I and III only", "I only", "II and III only", "I, II and III"],
  concept="LEI in RTGS",
  explanation="The LEI instructions apply to all RTGS channels: thick-client, Web-API (through INFINET or another "
              "approved network) and the Payment Originator module (I correct). Governments and their Departments/"
              "Ministries need not obtain or quote LEI, though Government corporations must (II wrong). In RTGS "
              "messages the first two loops carry sender and beneficiary LEI, and narration goes in the last two (III "
              "correct).",
  steps=["I → correct", "II → wrong (Government departments exempt)", "III → correct"],
  why="Options containing II are wrong; 'I only' misses III.",
  facts=[fact("The LEI instructions are applicable to all the channels being used for connecting to RTGS viz. "
              "thick-client, Web-API (through INFINET or any other approved network) and Payment Originator (PO) "
              "module", C_LEI),
         fact("It is not necessary for Governments or their Departments / Ministries to obtain LEI or mention LEI number "
              "for payment transactions in NEFT and RTGS", C_LEI),
         fact("The first two loops of this field shall be used for capturing sender and beneficiary customer LEI "
              "information, in that order", C_LEI)])

Q("010", "C-RTGS10-01", T, S, "Basic",
  "Which of the following is listed in RBI's RTGS FAQs as a benefit of using RTGS?",
  ["The transaction has legal backing", "RBI guarantees a minimum interest on the amount in transit",
   "Transfers can be scheduled for any future date", "There is no need to give the beneficiary's account number"],
  concept="Benefits of RTGS",
  explanation="RBI lists RTGS benefits such as safety, no amount cap set by RBI, 24x7x365 availability, real-time "
              "transfer, no need for physical cheques or drafts, capped charges and legal backing for the "
              "transaction.",
  steps=["Benefits include: legal backing, capped charges, 24x7, real-time credit"],
  why="No interest is paid on transit funds; RTGS does not accept future value-dated transactions; the beneficiary "
      "account number is essential.",
  facts=[fact("The transaction charges have been capped by RBI. The transaction has legal backing", C_RTGS)])
Q("010", "C-RTGS10-02", T, S, "Intermediate",
  "According to RBI's Payment Systems Report (December 2025), India's large value payment systems (LVPS) consist of "
  "RBI's RTGS and the systems operated by:",
  ["The Clearing Corporation of India Ltd (CCIL)", "The National Payments Corporation of India (NPCI)",
   "NPCI Bharat BillPay Ltd", "The Indian Banks' Association"],
  concept="Large value payment systems",
  explanation="RBI describes LVPS (wholesale payment systems) as those for large-value, high-priority payments such as "
              "money market, securities and interbank settlements. In India they include RBI-operated RTGS and CCIL-"
              "operated systems: Government securities clearing, forex clearing and rupee derivatives.",
  steps=["LVPS = RTGS (RBI) + CCIL systems (G-sec, forex, rupee derivatives)"],
  why="NPCI and NBBL run retail systems; IBA does not operate payment systems.",
  facts=[fact("In India, LVPS include RBI-operated system viz. Real Time Gross Settlement (RTGS) and systems operated by "
              "Clearing Corporation of India Limited (CCIL)", C_PSR)])
Q("010", "C-RTGS10-03", T, S, "Intermediate",
  "A businessman wants his bank to pull ₹10 lakh through RTGS from a customer's account in another bank, which owes "
  "him money. According to RBI's FAQs, can such a transaction be originated?",
  ["No; RTGS is a credit-push system and only the payer can originate a transfer to the beneficiary",
   "Yes, if the amount is ₹2 lakh or more", "Yes, but only on working days during business hours",
   "Yes, if the debtor's bank gives positive confirmation"],
  concept="Credit-push nature of RTGS",
  explanation="RBI's FAQs say RTGS is a credit-push system: transactions can be originated only by the payer/remitter "
              "to pay funds to a beneficiary. A transaction cannot be originated to draw (receive) funds from another "
              "account.",
  steps=["RTGS → credit push only", "Pull of funds not possible"],
  why="The amount, timing or positive confirmation does not change the credit-push design.",
  facts=[fact("No. RTGS is a credit-push system i.e., transactions can be originated by the payer / remitter / sender "
              "only to pay / transfer / remit funds to a beneficiary", C_RTGS)])
Q("010", "C-RTGS10-04", T, S, "Advanced",
  "Consider the following statements based on RBI's RTGS FAQs (updated October 2026):\nI. No charge may be levied on "
  "inward RTGS transactions, and for outward ones banks may charge less than RBI's prescribed caps but not more.\nII. "
  "With effect from 1 July 2019, RBI waived the processing charges it levied on banks for RTGS, and banks may pass the "
  "benefit on to customers.\nIII. To initiate an RTGS transfer, the remitter must hand over a physical cheque or "
  "demand draft at the branch.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="RTGS charges and convenience",
  explanation="Inward RTGS transactions are free, and banks may charge less than RBI's caps on outward ones but not "
              "more (I correct). RBI waived its own processing charges from 1 July 2019 so that banks could pass on the "
              "benefit (II correct). RBI lists as a benefit that the remitter need not use a physical cheque or draft, "
              "and can initiate RTGS through internet or mobile banking (III wrong).",
  steps=["I → correct", "II → correct", "III → wrong (no physical instrument needed)"],
  why="Options with III are wrong; 'I only' misses II.",
  facts=[fact("a) Inward transactions – Free, no charge to be levied ... Banks may decide to charge a lower rate but "
              "cannot charge more than the rates prescribed by RBI", C_RTGS),
         fact("With effect from July 01, 2019, RBI has waived the processing charges levied by it for RTGS transactions. "
              "Banks may pass on the benefit to its customers", C_RTGS),
         fact("The remitter need not use a physical cheque or a demand draft", C_RTGS)])
# ================= IMPS (008: I2 A1; 009: B1 I1 A1; 010: B1 I1 A1)
T = "IMPS"
S = "Limits and features"
Q("008", "C-IMPS08-01", T, S, "Intermediate",
  "An IMPS credit could not be made to the beneficiary because the remitter gave incomplete beneficiary details. Is "
  "this a 'failed transaction' under RBI's harmonised turn-around time (TAT) framework?",
  ["Yes; failed transactions include credits not effected for lack of full or proper information, and delay in "
   "initiating a reversal",
   "No; only failures caused by technical faults such as link failures are covered",
   "No; any failure involving the customer's own input is excluded altogether",
   "Only if the amount exceeds ₹2 lakh"],
  concept="Definition of a failed transaction",
  explanation="The framework defines a failed transaction as one not fully completed for reasons not attributable to "
              "the customer, such as communication failures, ATM cash outages or session time-outs, and expressly "
              "includes credits that could not be effected to the beneficiary account for lack of full or proper "
              "information and delay in initiating a reversal transaction.",
  steps=["Definition covers technical failures", "Also covers non-credit for lack of full/proper information"],
  why="RBI's definition expressly covers non-credit for lack of information; there is no amount threshold.",
  facts=[fact("Failed transactions shall also include the credits which could not be effected to the beneficiary "
              "account on account of lack of full information or lack of proper information and delay in initiating a "
              "reversal transaction", C_TAT)])
Q("008", "C-IMPS08-02", T, S, "Intermediate",
  "A customer uses her bank-issued PPI wallet to send money to a bank account of another bank, and the transfer rides "
  "on IMPS (an 'off-us' PPI transaction). It fails after the wallet is debited. Under RBI's TAT framework for failed "
  "transactions, which turn-around time and compensation rules apply?",
  ["Those of IMPS, the system on which the transaction rides",
   "A special PPI rule of reversal within T + 5 days with no compensation",
   "No TAT applies, since PPIs are outside the framework",
   "The rules for ATM transactions, as wallets are treated like cards"],
  concept="Off-us PPI transactions",
  explanation="For PPI off-us transactions, the framework says the transaction rides on UPI, a card network, IMPS, etc., "
              "and the TAT and compensation rules of that system apply. So here the IMPS rule (reversal by T + 1, ₹100 "
              "per day thereafter) applies. Separate T + 1 rules cover on-us PPI transactions.",
  steps=["Off-us PPI → follows the underlying system", "Here IMPS → IMPS TAT and compensation"],
  why="PPIs are covered; there is no separate T + 5 no-compensation rule; ATM rules are unrelated.",
  facts=[fact("Prepaid Payment Instruments (PPIs) – Cards / Wallets ... Off-Us transaction: The transaction will ride on "
              "UPI, card network, IMPS, etc., as the case may be. The TAT and compensation rule of respective system "
              "shall apply", C_TAT)])

Q("008", "C-IMPS08-03", T, S, "Advanced",
  "Ravi's IMPS transfer fails after his account is debited, and the beneficiary bank sends the money back. Consider the "
  "following statements about how RBI's harmonised turn-around time (TAT) framework treats such IMPS failures:\nI. 'R', "
  "the reversal day, is the day on which the reversal is concluded and the funds are received by the originator, and "
  "Ravi's bank must credit him on the same day it receives the funds.\nII. The term 'bank' in the framework also covers "
  "non-banks wherever they are authorised to operate.\nIII. 'T', the day of the transaction, means the next working "
  "day after Ravi initiated the transfer.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Definitions in the TAT framework",
  explanation="The framework defines R as the day the reversal is concluded and the funds are received by the issuer/"
              "originator, and requires the reversal to be effected at the originator's end on the same day the funds "
              "are received (I correct). The term bank includes non-banks wherever they are authorised to operate (II "
              "correct). T is the day of the transaction and refers to the calendar date, not the next working day "
              "(III wrong).",
  steps=["I → correct", "II → correct", "III → wrong (T = calendar date of the transaction)"],
  why="Options with III are wrong; 'I only' misses II.",
  facts=[fact("R is the day on which the reversal is concluded and the funds are received by the issuer / originator. "
              "Reversal should be effected at the issuer / originator end on the same day when the funds are received "
              "from the beneficiary end", C_TAT),
         fact("The term bank includes non-banks also and applies to them wherever they are authorised to operate", C_TAT),
         fact("T is the day of transaction and refers to the calendar date", C_TAT)])

Q("009", "C-IMPS09-01", T, S, "Basic",
  "Under RBI's turn-around time (TAT) framework for failed transactions in authorised payment systems such as IMPS, "
  "how is the compensation for delay paid to the customer?",
  ["It is credited to the customer's account suo moto, without waiting for a complaint or claim",
   "Only after the customer files a complaint with the bank",
   "Only after the RBI Ombudsman passes an award",
   "By NPCI directly, in cash at the bank branch"],
  concept="Suo moto compensation",
  explanation="RBI's circular of 20 September 2019 says that wherever financial compensation is involved, it must be "
              "credited to the customer's account suo moto, without waiting for a complaint or claim. Customers who do "
              "not get redress within the TAT can complain under RBI's Integrated Ombudsman Scheme.",
  steps=["Compensation due → credited automatically"],
  why="No complaint, Ombudsman award or cash payment by NPCI is required.",
  facts=[fact("Wherever financial compensation is involved, the same shall be effected to the customer's account suo "
              "moto, without waiting for a complaint or claim from the customer", C_TAT)])
Q("009", "C-IMPS09-02", T, S, "Intermediate",
  "Which transactions are covered by RBI's harmonised turn-around time (TAT) and compensation framework for failed "
  "transactions in authorised payment systems such as IMPS and UPI?",
  ["Domestic transactions, where both the originator and the beneficiary are within India",
   "All transactions of Indian customers, including remittances abroad",
   "Only transactions above ₹10,000", "Only transactions through bank branches, not through mobile apps"],
  concept="Scope of the TAT framework",
  explanation="The framework's general instructions say it covers domestic transactions, i.e., those where both the "
              "originator and the beneficiary are within India. It applies across authorised payment systems and to "
              "non-banks wherever they are authorised to operate, with no amount threshold or channel restriction.",
  steps=["Both parties in India → covered"],
  why="Cross-border transactions are excluded; there is no amount threshold or channel restriction.",
  facts=[fact("Domestic transactions i.e., those where both the originator and beneficiary are within India are covered "
              "under this framework", C_TAT)])
Q("009", "C-IMPS09-03", T, S, "Advanced",
  "RBI's TAT framework for failed transactions states two principles. Apply them to these IMPS cases:\nCase 1: Asha's "
  "account is debited for a credit-push transfer, but Bina's account is not credited within the prescribed time.\nCase "
  "2: Chetan's bank delays initiating his transfer beyond the TAT.\nTo whom is the penalty payable in each case?",
  ["Case 1: to Bina (the beneficiary); Case 2: to Chetan (the originator)",
   "Case 1: to Asha (the originator); Case 2: to Chetan (the originator)",
   "Case 1: to Bina; Case 2: to Chetan's intended beneficiary",
   "In both cases the penalty is paid to NPCI's customer protection fund"],
  concept="Principles of the TAT framework",
  explanation="The framework says: if a credit-push transfer is debited to the originator but the beneficiary account is "
              "not credited, credit must be given within the prescribed time, failing which the penalty is paid to the "
              "beneficiary; if there is delay in initiating the transaction at the originator bank's end beyond the "
              "TAT, the penalty is paid to the originator.",
  steps=["Delay in credit to beneficiary → penalty to beneficiary (Bina)",
         "Delay in initiation at originator's bank → penalty to originator (Chetan)"],
  why="The other options misplace the recipient of the penalty; there is no NPCI fund in the framework.",
  facts=[fact("If the transaction is a 'credit-push' funds transfer and the beneficiary account is not credited while the "
              "debit to originator has been effected, then credit is to be effected within the prescribed time period "
              "failing which the penalty has to be paid to the beneficiary; If there is delay in initiation of a "
              "transaction at the originator bank's end beyond the TAT, then penalty has to be paid to the originator",
              C_TAT)])

Q("010", "C-IMPS10-01", T, S, "Basic",
  "As described in RBI's Payment Systems Report (December 2025), IMPS, introduced by NPCI, supports which kinds of "
  "transactions?",
  ["Both person-to-person and person-to-merchant transactions, with real-time credit, 24x7",
   "Only person-to-person transfers, settled in half-hourly batches", "Only bulk salary and pension credits",
   "Only large-value interbank transfers of ₹2 lakh and above"],
  concept="Features of IMPS",
  explanation="The report describes IMPS as a fast payment system introduced by NPCI, offering 24x7 instant fund "
              "transfers through mobile banking, internet banking and ATMs, giving real-time credit to beneficiaries' "
              "accounts and supporting both person-to-person and person-to-merchant transactions.",
  steps=["IMPS: 24x7, instant, P2P and P2M"],
  why="Half-hourly batches describe NEFT; bulk credits describe NACH; ₹2 lakh minimum describes RTGS.",
  facts=[fact("Immediate Payment Service (IMPS): IMPS is a fast payment system introduced by NPCI, offering 24x7 instant "
              "fund transfer through multiple channels including mobile banking, internet banking, and ATMs. It enables "
              "real-time credit to beneficiaries' accounts and supports both person-to-person and person-to-merchant "
              "transactions", C_PSR)])
Q("010", "C-IMPS10-02", T, S, "Intermediate",
  "How does RBI describe the turn-around times (TAT) it prescribed in 2019 for resolving failed transactions in systems "
  "such as IMPS?",
  ["As the outer limit for resolution, with banks and operators expected to resolve failures sooner",
   "As the minimum period a bank must wait before reversing a failed transaction",
   "As indicative targets that banks may extend with Board approval",
   "As applicable only to complaints routed through the RBI Ombudsman"],
  concept="Nature of the TAT",
  explanation="RBI's circular of 20 September 2019 notes that the prescribed TAT is the outer limit for resolution of "
              "failed transactions and that banks and other operators/participants shall endeavour towards quicker "
              "resolution. It came into effect from 15 October 2019.",
  steps=["TAT = outer limit", "Quicker resolution expected"],
  why="It is a maximum, not a waiting period; banks cannot extend it; it applies to all failed transactions, not only "
      "Ombudsman cases.",
  facts=[fact("the prescribed TAT is the outer limit for resolution of failed transactions; and the banks and other "
              "operators / system participants shall endeavour towards quicker resolution of such failed transactions",
              C_TAT)])

v0, v1, a0, a1 = 434, 518, 38, 75
cg_v, cg_a = (v1 / v0) ** 0.25 - 1, (a1 / a0) ** 0.25 - 1
assert round(cg_v * 100, 1) == 4.5 and round(cg_a * 100, 1) == 18.5
assert round((v1 - v0) / v0 / 4 * 100, 1) == 4.8 and round((a1 - a0) / a0 / 4 * 100, 1) == 24.3
assert round(cg_v * 100 / 4, 1) == 1.1 and round(cg_a * 100 / 4, 1) == 4.6
Q("010", "C-IMPS10-03", T, S, "Advanced",
  "According to RBI's Payment Systems Report (December 2025), IMPS volume rose from 434 crore transactions in CY 2021 "
  "to 518 crore in CY 2025, and value from ₹38 lakh crore to ₹75 lakh crore. Using these figures over the four years, "
  "which compound annual growth rates (CAGR) are closest?",
  ["Volume about 4.5% a year; value about 18.5% a year", "Volume about 19% a year; value about 4.5% a year",
   "Volume about 4.8% a year; value about 24.3% a year", "Volume about 1.1% a year; value about 4.6% a year"],
  concept="Compound annual growth rate",
  explanation="CAGR = (end ÷ start)^(1/years) − 1 over 4 years. Volume: (518 ÷ 434)^0.25 − 1 ≈ 4.5%. Value: (75 ÷ "
              "38)^0.25 − 1 ≈ 18.5%; RBI, using unrounded data, reports 4.5% and 18.1%. Slow volume growth with fast "
              "value growth means IMPS is used for larger transfers.",
  steps=["Volume: (518/434)^(1/4) − 1 ≈ 4.5%", "Value: (75/38)^(1/4) − 1 ≈ 18.5% (RBI: 18.1%)"],
  why="The second option swaps the two; 4.8% and 24.3% are simple averages (total growth ÷ 4); 1.1% and 4.6% divide "
      "the CAGR by four again.",
  computed=True, current=ca("2026-05-18"),
  facts=[fact("IMPS transactions volume rose from 434 crore in CY 2021 to 518 crore in CY 2025. More notably, transaction "
              "value doubled during the same period from ₹38 lakh crore to ₹75 lakh crore ( Chart 10 ). This translates "
              "into a CAGR of 4.5 per cent in in volume and 18.1 per cent in value", C_PSR)])
# ================= UPI (008: B1 I5 A1; 009: B1 I4 A2; 010: B2 I2 A4)
T = "UPI"
F, L = "Features", "UPI Lite and international"
Q("008", "C-UPI08-01", T, L, "Basic",
  "Under RBI's framework for small value digital payments in offline mode (as updated in December 2024), what is the "
  "total limit on a UPI Lite balance at any point in time?",
  ["₹5,000", "₹2,000", "₹1,000", "₹10,000"],
  concept="UPI Lite limits",
  explanation="RBI's offline payments framework sets a general limit of ₹500 per transaction and ₹2,000 in total, but "
              "for UPI Lite the enhanced limits are ₹1,000 per transaction with ₹5,000 as the total limit.",
  steps=["UPI Lite: ₹1,000 per transaction", "UPI Lite: ₹5,000 total at any time"],
  why="₹2,000 is the general offline total; ₹1,000 is the per-transaction UPI Lite cap; ₹10,000 is not an offline "
      "limit.",
  current=ca("2024-12-04"),
  facts=[fact("For UPI Lite, the enhanced limits shall be ₹1,000 per transaction with ₹5,000 being the total limit",
              C_OFFL)])
Q("008", "C-UPI08-02", T, F, "Intermediate",
  "Under RBI's Digital Payments – E-mandate Framework, 2026, which also covers UPI AutoPay mandates, how far in advance "
  "must the issuer send a pre-transaction notification before the actual debit?",
  ["At least 24 hours", "At least 48 hours", "At least 7 days", "At least 2 hours"],
  concept="Pre-transaction notification for e-mandates",
  explanation="The framework (21 April 2026) consolidates RBI's e-mandate circulars for recurring transactions using "
              "cards, PPIs and UPI. The issuer must send a pre-transaction notification at least 24 hours before the "
              "charge, giving the merchant's name, amount, date/time of debit, mandate reference and reason for debit, "
              "and must let the customer opt out (validated with AFA).",
  steps=["E-mandate debit → notify customer ≥ 24 hours before"],
  why="48 hours, 7 days and 2 hours are not the period prescribed.",
  current=ca("2026-04-21"),
  facts=[fact("An issuer shall send a pre-transaction notification to the customer, at least 24 hours prior to the "
              "actual charge / debit", C_EMAND),
         fact("applicable to all Payment System Providers and Payment System Participants in respect of processing of "
              "recurring transactions, domestic or cross-border, using cards / PPI / UPI", C_EMAND)])
Q("008", "C-UPI08-03", T, F, "Intermediate",
  "To reduce the load on the UPI system, NPCI limited balance enquiries from 1 August 2025. What is the limit?",
  ["50 balance enquiries per day on each UPI app", "50 balance enquiries per day across all UPI apps together",
   "10 balance enquiries per day on each UPI app", "One balance enquiry after every UPI transaction only"],
  concept="UPI usage limits of August 2025",
  explanation="Under NPCI's changes effective 1 August 2025, a user can make at most 50 balance enquiries a day on each "
              "UPI app, and only 25 requests a day for the list of bank accounts linked to the mobile number.",
  steps=["Balance enquiries: 50/day per app"],
  why="The cap applies per app, not across apps, and is 50, not 10.",
  current=ca("2025-08-01"),
  facts=[fact("For balance enquiries, the maximum limit is 50 per day on each UPI app", C_UPIAUG)])
Q("008", "C-UPI08-04", T, F, "Intermediate",
  "Under RBI's Master Direction on Prepaid Payment Instruments, which PPIs may a PPI issuer enable for UPI payments by "
  "linking them to its UPI handle?",
  ["Only its full-KYC PPIs; the issuer acts as a PSP in UPI with a handle issued by NPCI",
   "All its PPIs, including small PPIs without full KYC",
   "Only gift PPIs, through a sponsor bank's handle",
   "Only PPIs issued by banks; non-bank PPI issuers cannot participate in UPI"],
  concept="PPIs on UPI",
  explanation="A PPI issuer acts as a Payment System Provider (PSP) in UPI, and NPCI issues it a handle. It may enable "
              "only its full-KYC PPIs to make UPI payments by linking them to its handle; such transactions on the "
              "issuer's app are authenticated with the customer's PPI credentials.",
  steps=["PPI issuer = PSP in UPI; NPCI issues handle", "Only full-KYC PPIs can be linked"],
  why="Small PPIs are excluded; gift PPIs are not the category named; non-bank PPI issuers can participate.",
  facts=[fact("PPI issuer shall act as Payment System Providers (PSP) in UPI. NPCI shall issue handle to the PPI issuer "
              "... A PPI issuer shall enable holders of only its full-KYC PPIs to make UPI payments by linking its "
              "customer PPIs to its UPI handle", C_PPI)])
Q("008", "C-UPI08-05", T, L, "Intermediate",
  "Under RBI's Master Direction on PPIs, banks and non-banks may issue INR-denominated full-KYC PPIs to foreign "
  "nationals and NRIs visiting India in the form of wallets linked to UPI. For what can these wallets be used?",
  ["Merchant payments (P2M) only", "Person-to-person transfers only",
   "Both P2P and P2M payments, and cash withdrawal at ATMs", "Only for paying visa and airport fees"],
  concept="UPI for inbound travellers",
  explanation="The PPI Master Direction allows full-KYC INR PPIs for foreign nationals/NRIs visiting India (to start "
              "with, travellers from G-20 countries at select international airports). They may be issued as wallets "
              "linked to UPI and used for merchant payments (P2M) only.",
  steps=["Inbound traveller PPI → UPI-linked wallet", "Use: P2M only"],
  why="P2P transfers and cash withdrawal are not allowed; the use is not limited to fees.",
  facts=[fact("The PPIs can be issued in the form of wallets linked to UPI and can be used for merchant payments (P2M) "
              "only", C_PPI)])
Q("008", "C-UPI08-06", T, F, "Intermediate",
  "A non-bank PPI issuer participates in UPI as a Payment System Provider so that its full-KYC wallet holders can make "
  "UPI payments. Under RBI's Master Direction on PPIs, how does it settle its UPI transactions?",
  ["Through a sponsor bank, meeting NPCI's requirements for the sponsor bank arrangement",
   "Directly in its own current account with RBI", "Through CCIL as a central counterparty",
   "In cash with each beneficiary bank at the end of the day"],
  concept="Settlement of non-bank PPI issuers in UPI",
  explanation="The PPI Master Direction says that for settlement a non-bank PPI issuer shall participate in UPI through "
              "a sponsor bank and meet the sponsor bank arrangement requirements of UPI and all NPCI requirements. "
              "Payments to and from the sponsor bank towards settlement obligations are permitted in its escrow "
              "account.",
  steps=["Non-bank PPI issuer in UPI → settles through a sponsor bank"],
  why="Non-banks do not hold settlement accounts with RBI for UPI; CCIL does not settle UPI; settlement is not in cash.",
  facts=[fact("Settlement : For the purposes of settlement, a non-bank PPI issuer shall participate through a sponsor "
              "bank. Non-bank PPI issuer shall adhere to the requirements of sponsor bank arrangement in UPI as also "
              "meet all requirements of NPCI in this regard", C_PPI)])

_c_mandates = {"P": ("first", 499, "ott"), "Q": ("later", 12000, "school"), "R": ("later", 60000, "mf"),
            "S": ("later", 22000, "gym")}


def _c_needs_afa(kind, amt, cat):
    if kind == "first":
        return True
    cap = 100000 if cat in ("insurance", "mf", "card") else 15000
    return amt > cap


assert [k for k, v in _c_mandates.items() if _c_needs_afa(*v)] == ["P", "S"]
Q("008", "C-UPI08-07", T, F, "Advanced",
  "Under RBI's Digital Payments – E-mandate Framework, 2026, which of these UPI AutoPay debits need an Additional "
  "Factor of Authentication (AFA)?\nP. The first debit of ₹499 under a new monthly streaming mandate\nQ. The fourth "
  "monthly debit of ₹12,000 for school fees\nR. A monthly mutual fund SIP debit of ₹60,000 (not the first)\nS. A monthly "
  "gym membership debit of ₹22,000 (not the first)",
  ["P and S only", "S only", "P, R and S only", "R and S only"],
  concept="AFA in e-mandates",
  explanation="The first transaction under any e-mandate needs AFA (it may be combined with registration), so P needs "
              "AFA. Later recurring debits are AFA-free up to ₹15,000 (Q is fine) and up to ₹1,00,000 for insurance "
              "premiums, mutual fund subscriptions and credit card bills (R is fine). S, at ₹22,000 in an ordinary "
              "category, exceeds ₹15,000 and needs AFA.",
  steps=["P: first transaction → AFA", "Q: ₹12,000 ≤ ₹15,000 → no AFA", "R: MF ₹60,000 ≤ ₹1 lakh → no AFA",
         "S: ₹22,000 > ₹15,000 → AFA"],
  why="'S only' forgets the first-transaction rule; options with R ignore the ₹1 lakh limit for mutual funds.",
  computed=True, current=ca("2026-04-21"),
  facts=[fact("The first transaction under an e-mandate shall require AFA validation", C_EMAND),
         fact("All recurring transactions may be authorised without AFA up to ₹15,000/- per transaction ... Payment of "
              "insurance premiums, subscription to mutual funds, and credit card bill payments may be made without AFA "
              "up to ₹1,00,000/- per transaction", C_EMAND)])

Q("009", "C-UPI09-01", T, F, "Basic",
  "RBI's Authentication Directions, 2025 require at least two factors of authentication for digital payments, with "
  "listed exemptions. Which UPI use case was added to the list of exemptions through a letter to NPCI in September "
  "2026?",
  ["Tap and Pay UPI payments on NFC-enabled point-of-sale machines", "UPI person-to-person transfers to new payees",
   "UPI payments above ₹1 lakh to hospitals", "UPI collect requests from merchants"],
  concept="Exemptions from two-factor authentication",
  explanation="Annexure-1 of the Reserve Bank of India (Authentication mechanisms for digital payment transactions) "
              "Directions, 2025 lists the exemptions in force, such as small-value contactless card payments, "
              "recurring e-mandate debits (other than the first), NETC transactions and small-value offline payments. "
              "It now includes Tap and Pay UPI payments on NFC-enabled PoS machines, under a letter to NPCI dated 2 "
              "September 2026.",
  steps=["Exemptions list (Annexure-1)", "Tap and Pay UPI on NFC PoS → letter of 2 September 2026"],
  why="The other UPI uses are not in the exemption list.",
  current=ca("2026-09-02"),
  facts=[fact("Tap and Pay UPI Payment on Near Field Communication enabled Point of Sale machines Letter dated September "
              "2, 2026 (CO.DPSS.POLC.No. S-550/02-23-001/2026-27 dated September 2, 2026) issued to NPCI", C_AUTH)])

Q("009", "C-UPI09-02", T, F, "Intermediate",
  "Under RBI's Digital Payments – E-mandate Framework, 2026, which also governs UPI AutoPay, what must the issuer's "
  "post-transaction notification include at the minimum, besides the merchant's name, amount, date and time and "
  "reference numbers?",
  ["The reason for the debit (the e-mandate registered by the customer) and details on grievance redressal",
   "The customer's credit score and available balance", "The merchant's GSTIN and PAN",
   "A one-time password to confirm the debit"],
  concept="Post-transaction notification",
  explanation="After an e-mandate debit, the issuer must send a post-transaction notification giving at least the "
              "merchant's name, transaction amount, date and time, reference numbers of the transaction and e-mandate, "
              "the reason for the debit (the customer's registered e-mandate) and details on grievance redressal, the "
              "last added on the basis of feedback.",
  steps=["Post-debit notice: merchant, amount, date/time, references, reason, grievance redressal details"],
  why="Credit score, merchant tax IDs or an OTP are not required; recurring debits after the first need no AFA within "
      "limits.",
  current=ca("2026-04-21"),
  facts=[fact("An issuer shall send a post-transaction notification to the customer. This notification shall, at the "
              "minimum, inform the customer about the merchant's name, transaction amount, date and time of debit, "
              "reference number of transaction and e-mandate, reason for debit, i.e., e-mandate registered by the "
              "customer, and details on grievance redressal", C_EMAND)])
Q("009", "C-UPI09-03", T, F, "Intermediate",
  "Under RBI's Digital Payments – E-mandate Framework, 2026, a customer wants to change the validity period of her UPI "
  "AutoPay mandate. What does the framework require for any modification or withdrawal of an existing e-mandate?",
  ["AFA validation by the issuer", "A written request at the home branch", "Prior approval of the merchant",
   "Nothing; it can be changed by the merchant on the customer's request"],
  concept="Modifying e-mandates",
  explanation="The issuer must let the customer modify the validity period or withdraw the e-mandate at any time, and "
              "any modification in, or withdrawal of, an existing e-mandate requires AFA validation by the issuer.",
  steps=["Modify/withdraw anytime", "Validated with AFA by the issuer"],
  why="No branch visit or merchant approval is needed, and the merchant cannot alter it.",
  current=ca("2026-04-21"),
  facts=[fact("Any modification in, or withdrawal of, an existing e-mandate shall require AFA validation by the issuer",
              C_EMAND)])
Q("009", "C-UPI09-04", T, F, "Intermediate",
  "From 1 August 2025, NPCI moved the execution of UPI AutoPay mandate debits to non-peak hours. Which periods does "
  "NPCI define as peak hours?",
  ["10 am to 1 pm and 5 pm to 9:30 pm", "8 am to 11 am and 6 pm to 10 pm", "9 am to 12 noon and 4 pm to 8 pm",
   "12 noon to 3 pm and 7 pm to 11 pm"],
  concept="Peak hours for UPI AutoPay",
  explanation="NPCI's May 2025 circular defines peak hours as 10:00 to 13:00 and 17:00 to 21:30, when UPI transactions "
              "reach their highest transactions per second; any other time is non-peak. AutoPay mandates can still be "
              "created at any time, but their execution is moved to non-peak hours.",
  steps=["Peak: 10:00–13:00 and 17:00–21:30", "AutoPay debits → outside these windows"],
  why="The other windows are not those NPCI specified.",
  current=ca("2025-08-01"),
  facts=[fact("Peak hours are defined as the period during the day when UPI financial transactions reach the highest "
              "transactions per second, observed from 10:00 hrs (10 am) to 13:00 hrs (1 pm) and from 17:00 hrs (5 pm) "
              "to 21:30 hrs (9.30 pm)", C_UPIAUG)])
Q("009", "C-UPI09-05", T, F, "Intermediate",
  "Under RBI's Master Direction on Prepaid Payment Instruments, how is interoperability across PPIs issued in the form "
  "of wallets to be enabled?",
  ["Through UPI", "Through the RuPay card network only", "Through NEFT", "Through the Bharat Bill Payment System"],
  concept="Wallet interoperability",
  explanation="The PPI Master Direction says that where PPIs are issued as wallets, interoperability across PPIs shall be "
              "enabled through UPI; PPIs in the form of cards achieve interoperability through authorised card "
              "networks. Since *99# USSD is part of UPI, non-bank PPI issuers may also participate in it.",
  steps=["Wallets → interoperable through UPI", "Cards → through card networks"],
  why="Card networks serve card PPIs; NEFT and BBPS are not the interoperability route for wallets.",
  facts=[fact("Where PPIs are issued in the form of wallets, interoperability across PPIs shall be enabled through UPI",
              C_PPI),
         fact("Since *99# USSD is part of UPI, non-bank PPI issuer are also allowed to participate in the same", C_PPI)])
Q("009", "C-UPI09-06", T, F, "Advanced",
  "Consider the following statements about UPI payments from PPIs under RBI's Master Direction on PPIs:\nI. A UPI "
  "payment from a PPI made on the issuer's own application is authenticated using the customer's existing PPI "
  "credentials.\nII. If the PPI is linked to a third-party UPI application, the payment is authenticated using UPI "
  "credentials.\nIII. A PPI issuer acting as a PSP may onboard customers of any bank onto its UPI handle.\nWhich of the "
  "above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Authentication of PPI-based UPI payments",
  explanation="On the issuer's own app, UPI transactions from a PPI use the existing PPI credentials and are thus "
              "pre-approved before reaching UPI (I correct). A full-KYC PPI discovered on a third-party UPI app is "
              "authenticated with UPI credentials (II correct). A PPI issuer, as PSP, shall not onboard customers of "
              "any bank or other PPI issuer (III wrong).",
  steps=["I → correct", "II → correct", "III → wrong"],
  why="Options with III are wrong; 'I only' misses II.",
  facts=[fact("UPI transactions from PPI on the issuer's application shall be authenticated using the customer's "
              "existing PPI credentials ... A PPI issuer, in its capacity as a PSP, shall not on-board customers of "
              "any bank or any other PPI issuer", C_PPI),
         fact("Such UPI transactions, from PPIs using third party UPI applications, shall be authenticated using the "
              "UPI credentials", C_PPI)])

bal, total_cap, per_txn, bill = 1700, 5000, 1000, 4600
top_up = total_cap - bal
n_pay = -(-bill // per_txn)
assert (top_up, n_pay) == (3300, 5)
Q("009", "C-UPI09-07", T, L, "Advanced",
  "Neha's UPI Lite balance is ₹1,700. Under RBI's current limits for UPI Lite, (a) what is the most she can add right "
  "now, and (b) after topping up fully, what is the minimum number of UPI Lite payments needed to pay ₹4,600 to a "
  "merchant entirely from UPI Lite?",
  ["(a) ₹3,300; (b) 5", "(a) ₹3,300; (b) 4", "(a) ₹5,000; (b) 5", "(a) ₹300; (b) 10"],
  concept="Applying UPI Lite limits",
  explanation="The UPI Lite balance cannot exceed ₹5,000 at any time, so she can add at most ₹5,000 − ₹1,700 = ₹3,300 "
              "(online, with AFA). Each UPI Lite payment is capped at ₹1,000, so ₹4,600 needs at least ⌈4,600 ÷ "
              "1,000⌉ = 5 payments.",
  steps=["Top-up = 5,000 − 1,700 = ₹3,300", "Payments = ⌈4,600 ÷ 1,000⌉ = 5"],
  why="4 payments can carry at most ₹4,000; ₹5,000 ignores the existing balance; ₹300 and 10 use the general offline "
      "limits of ₹2,000 and ₹500.",
  computed=True, current=ca("2024-12-04"),
  facts=[fact("For UPI Lite, the enhanced limits shall be ₹1,000 per transaction with ₹5,000 being the total limit. "
              "Replenishment of used limit shall be allowed only in online mode with AFA", C_OFFL)])

Q("010", "C-UPI10-01", T, L, "Basic",
  "Under RBI's framework for small value digital payments in offline mode, which governs UPI Lite, on what basis are "
  "payment instruments enabled for offline transactions?",
  ["The explicit consent of the customer", "Automatically for every customer of the bank",
   "On the merchant's request", "On NPCI's instructions to all banks"],
  concept="Consent for offline payments",
  explanation="The framework says payment instruments shall be enabled for offline transactions based on the explicit "
              "consent of the customer; offline payments are made in proximity mode and may be offered without AFA.",
  steps=["Offline capability → only with the customer's explicit consent"],
  why="RBI requires the customer's explicit consent, not automatic, merchant-driven or NPCI-driven enabling.",
  facts=[fact("Payment instruments shall be enabled for offline transactions based on explicit consent of the customer",
              C_OFFL)])
Q("010", "C-UPI10-02", T, F, "Basic",
  "In October 2024, RBI raised the per-transaction limit of UPI123Pay, the UPI facility for feature-phone users, to:",
  ["₹10,000", "₹5,000", "₹1,000", "₹1 lakh"],
  concept="UPI123Pay limit",
  explanation="In the October 2024 policy, RBI decided to enhance the per-transaction limit in UPI123Pay from ₹5,000 to "
              "₹10,000, along with raising UPI Lite limits.",
  steps=["UPI123Pay: ₹5,000 → ₹10,000"],
  why="₹5,000 was the earlier limit; ₹1,000 is the UPI Lite per-transaction limit; ₹1 lakh is the general UPI limit.",
  current=ca("2024-10-09"),
  facts=[fact("it has been decided to (i) enhance the per-transaction limit in UPI123Pay from ₹5,000 to ₹10,000", C_123)])
Q("010", "C-UPI10-03", T, L, "Intermediate",
  "UPI Lite is covered by RBI's framework for small value digital payments in offline mode. In what sense is a UPI "
  "Lite transaction 'offline', according to RBI?",
  ["To the extent that AFA is not required and transaction alerts are not sent in real time",
   "It works without any connectivity at both the payer's and the payee's end",
   "It is settled in cash at the end of the day", "It is not recorded by the issuing bank at all"],
  concept="Nature of UPI Lite",
  explanation="RBI's framework notes that a UPI Lite transaction is offline to the extent that the Additional Factor of "
              "Authentication is not required and transaction alerts are not sent in real time. Issuers must still "
              "convey details of each transaction adequately.",
  steps=["No AFA for payments", "Alerts not real-time"],
  why="RBI does not describe UPI Lite as connectivity-free, cash-settled or unrecorded.",
  facts=[fact("UPI Lite transaction is offline to the extent that AFA is not required, and transaction alerts not sent "
              "in real time", C_OFFL)])
Q("010", "C-UPI10-04", T, F, "Intermediate",
  "A customer has set a daily UPI limit of ₹10,000 in her banking app, and her UPI AutoPay mandate debits ₹12,000. "
  "Under RBI's Digital Payments – E-mandate Framework, 2026, are payments under the e-mandate subject to her own limit?",
  ["No; payments under e-mandates are not subject to any other limits or controls set by the customer",
   "Yes; the debit must be split to stay within her limit", "Yes; the debit fails and the mandate is cancelled",
   "Only if the mandate was registered after 2024"],
  concept="E-mandates and customer-set limits",
  explanation="The framework says payments under e-mandates shall not be subject to any other limits or controls set by "
              "the customer. The customer is protected instead by AFA at registration, pre-transaction notification "
              "with an opt-out, and the overall AFA-free caps.",
  steps=["E-mandate debit → outside customer-set limits"],
  why="The framework explicitly excludes customer-set limits; no splitting or cancellation follows.",
  current=ca("2026-04-21"),
  facts=[fact("Payments under e-mandates shall not be subject to any other limits / controls set by the customer",
              C_EMAND)])
Q("010", "C-UPI10-05", T, L, "Advanced",
  "Consider the following statements about RBI's Framework for Facilitating Small Value Digital Payments in Offline "
  "Mode (updated December 2024), under which UPI Lite operates:\nI. Apart from UPI Lite, an offline payment is capped "
  "at ₹500 per transaction and ₹2,000 in total on a payment instrument at any time.\nII. Offline payments may be made "
  "only in proximity (face-to-face) mode.\nIII. Offline payments are outside RBI's circulars on limited customer "
  "liability.\nWhich of the above is/are correct?",
  ["I and II only", "II only", "I and III only", "I, II and III"],
  concept="Offline payments framework",
  explanation="The general offline limits are ₹500 per transaction and ₹2,000 in total (UPI Lite has higher limits) — I "
              "correct. Offline payments are allowed in proximity (face-to-face) mode only — II correct. They are "
              "covered by RBI's limited customer liability circulars, and customers can use the Integrated Ombudsman "
              "Scheme — III wrong.",
  steps=["I → correct", "II → correct", "III → wrong (covered by limited liability rules)"],
  why="Options with III are wrong; 'II only' misses I.",
  facts=[fact("The upper limit of an offline payment transaction shall be ₹500. The total limit for offline "
              "transactions on a payment instrument shall be ₹2,000 at any point in time", C_OFFL),
         fact("Offline payments shall be made in proximity (face to face) mode only", C_OFFL),
         fact("Offline payments shall be covered under the provisions of RBI's limited customer liability circulars",
              C_OFFL)])
Q("010", "C-UPI10-06", T, L, "Advanced",
  "Consider the following statements about the INR prepaid wallets linked to UPI that RBI allows for foreign nationals "
  "and NRIs visiting India:\nI. To start with, the facility is for travellers from G-20 countries arriving at select "
  "international airports.\nII. The PPI is issued after physical verification of the customer's passport and visa at "
  "the point of issue.\nIII. The wallet can be loaded only against Indian rupee cash.\nWhich of the above is/are "
  "correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="PPIs for inbound travellers",
  explanation="RBI's PPI Master Direction allows full-KYC INR PPIs to foreign nationals/NRIs visiting India, starting "
              "with G-20 travellers at select international airports (I correct), after physical verification of "
              "passport and visa (II correct). Loading is against receipt of foreign exchange by cash or any payment "
              "instrument, with rupee conversion only by authorised dealers (III wrong). Unused balances can be "
              "encashed in foreign currency or sent back to source.",
  steps=["I → correct", "II → correct", "III → wrong (loaded against foreign exchange)"],
  why="Options with III are wrong; 'I only' misses II.",
  facts=[fact("to start with, this facility will be extended to travellers from the G-20 countries, arriving at select "
              "international airports ... The PPIs shall be issued after physical verification of Passport and Visa of "
              "the customers at the point of issuance", C_PPI),
         fact("Loading / Reloading of such PPIs shall be against receipt of foreign exchange by cash or through any "
              "payment instrument", C_PPI)])
Q("010", "C-UPI10-07", T, F, "Advanced",
  "Consider the following statements about NPCI's UPI changes that took effect from 1 August 2025:\nI. Within a 30-day "
  "window, a user can raise only 10 payment reversal requests, and only five against the same sender.\nII. The name "
  "linked to the recipient's account is displayed before the payer enters the UPI PIN.\nIII. A user can request the "
  "list of bank accounts linked to her mobile number up to 50 times a day on each app.\nWhich of the above is/are "
  "correct?",
  ["I and II only", "II only", "I and III only", "I, II and III"],
  concept="UPI rule changes of August 2025",
  explanation="From 1 August 2025, only 10 payment reversal requests are allowed in 30 days, with a cap of five per "
              "sender (I correct); the official name of the recipient's account is shown before the PIN is entered (II "
              "correct). Requests for the list of linked bank accounts are capped at 25 a day; 50 is the balance-"
              "enquiry cap (III wrong).",
  steps=["I → correct", "II → correct", "III → wrong (25, not 50)"],
  why="Options with III confuse the account-list cap with the balance-enquiry cap; 'II only' misses I.",
  current=ca("2025-08-01"),
  facts=[fact("within a 30-day window, only 10 payment reversal requests are allowed. However, there is also a cap on "
              "requests with each sender at five in the same time period", C_UPIAUG),
         fact("the official name linked to the recipient's account will be displayed before you hit your UPI PIN", C_UPIAUG),
         fact("users can only have 25 daily requests for getting the bank details associated with their phone number",
              C_UPIAUG)])
Q("010", "C-UPI10-08", T, F, "Advanced",
  "Consider the following statements about the Digital Payments – E-mandate Framework, 2026, which governs UPI "
  "AutoPay:\nI. Every e-mandate must specify its validity period, and the customer can modify the period or withdraw "
  "the mandate at any time.\nII. For a variable-amount e-mandate, the customer can specify the maximum value of any "
  "recurring transaction.\nIII. The issuer may levy a nominal charge on the customer for the e-mandate facility.\nWhich "
  "of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="Features of e-mandates",
  explanation="Each e-mandate must specify its validity period, and the issuer must allow the customer to modify it or "
              "withdraw the mandate at any time (I correct). For variable e-mandates the customer can set the maximum "
              "value of any recurring transaction (II correct). No charges may be levied for availing the e-mandate "
              "facility (III wrong).",
  steps=["I → correct", "II → correct", "III → wrong (no charges)"],
  why="Options with III are wrong; 'I only' misses II.",
  current=ca("2026-04-21"),
  facts=[fact("Every e-mandate registered by the issuer shall specify the validity period of the e-mandate. The issuer "
              "shall provide the customer with a facility to modify the validity period or withdraw the e-mandate at "
              "any point of time", C_EMAND),
         fact("In the case of variable e-mandates, the issuer shall provide the customer with a facility to specify the "
              "maximum value of any recurring transaction", C_EMAND),
         fact("No charges shall be levied to the customer for availing the e-mandate facility for recurring "
              "transactions", C_EMAND)])

# ================= NPCI (008: B3 I1 A2; 009: B1 I3 A1; 010: B1 I3 A1)
T = "NPCI"
S = "Products: NACH, AePS, RuPay, FASTag"
Q("008", "C-NPCI08-01", T, S, "Basic",
  "A customer's RuPay debit card, on which she had registered e-mandates for recurring payments, is reissued. Under "
  "RBI's Digital Payments – E-mandate Framework, 2026, what happens to the existing e-mandates?",
  ["They can be mapped to the reissued card", "They lapse and must be cancelled by the merchant",
   "They are converted into NACH mandates", "They are transferred to the customer's UPI ID"],
  concept="E-mandates on reissued cards",
  explanation="The framework, which applies to recurring transactions using cards, PPIs and UPI, provides that in the "
              "case of cards, existing e-mandates can be mapped to reissued cards. This clause was added on the basis "
              "of feedback.",
  steps=["Card reissued → existing e-mandates can be mapped to the new card"],
  why="The framework does not make mandates lapse or convert them to NACH or UPI.",
  current=ca("2026-04-21"),
  facts=[fact("In case of cards, existing e-mandate(s) can be mapped to reissued cards", C_EMAND)])
Q("008", "C-NPCI08-02", T, S, "Basic",
  "Under RBI's Authentication Directions, 2025, which of the following NPCI-run payments is exempted from the "
  "requirement of at least two factors of authentication?",
  ["NETC (FASTag) toll transactions", "AePS cash withdrawals", "IMPS fund transfers", "RuPay card online purchases"],
  concept="2FA exemptions",
  explanation="Annexure-1 of the Authentication Directions lists exemptions in force, including National Electronic Toll "
              "Collection (NETC) transactions, small-value contactless card payments, recurring e-mandate debits other "
              "than the first, and small-value offline payments.",
  steps=["NETC transactions → exempt from 2FA"],
  why="AePS, IMPS and online card purchases are not in the exemption list.",
  facts=[fact("Existing exemptions from the requirement of at least two factors of authentication ... 4. NETC "
              "transactions", C_AUTH)])
Q("008", "C-NPCI08-03", T, S, "Basic",
  "According to RBI's Payment Systems Report (December 2025), 'Best Finger Detection (BFD)' is an additional service "
  "offered under which NPCI system?",
  ["Aadhaar Enabled Payment System (AePS)", "National Automated Clearing House (NACH)",
   "National Electronic Toll Collection (NETC)", "RuPay card network"],
  concept="AePS services",
  explanation="RBI lists AePS banking services as cash deposit, cash withdrawal, balance enquiry, mini statement, "
              "Aadhaar-to-Aadhaar fund transfer and BHIM Aadhaar Pay, with additional services such as e-KYC, Best "
              "Finger Detection and biometric authentication.",
  steps=["BFD relates to biometric (fingerprint) use → AePS"],
  why="NACH, NETC and RuPay do not use fingerprint-based services.",
  facts=[fact("The banking services offered under AePS include cash deposit, cash withdrawal, balance enquiry, mini "
              "statement, Aadhaar-to-Aadhaar fund transfer, and BHIM Aadhaar Pay. Additional services include e-KYC, "
              "Best Finger Detection (BFD), and biometric authentication etc.", C_PSR)])
Q("008", "C-NPCI08-04", T, S, "Intermediate",
  "According to RBI's Payment Systems Report (December 2025), how did NACH Debit and NACH Credit compare in growth "
  "between CY 2021 and CY 2025?",
  ["NACH Debit grew faster in both volume and value (CAGR about 19% and 27%) than NACH Credit (about 16% and 17%)",
   "NACH Credit grew faster in both volume and value than NACH Debit",
   "NACH Debit grew faster in volume but NACH Credit grew faster in value",
   "Both grew at the same rate of about 17% in volume and value"],
  concept="NACH growth",
  explanation="RBI reports NACH Credit CAGRs of 15.8% in volume and 17.02% in value, and NACH Debit CAGRs of 19.3% in "
              "volume and 27% in value, indicating rising use of auto-debits such as EMIs, insurance premiums and "
              "bills.",
  steps=["Debit: 19.3% (vol), 27% (val)", "Credit: 15.8% (vol), 17.02% (val)", "Debit faster on both"],
  why="The other options reverse or equalise RBI's figures.",
  current=ca("2026-05-18"),
  facts=[fact("NACH Credit transactions grew at a CAGR of 15.8% in volume and 17.02% in value ... NACH Debit "
              "transactions have shown even more vigorous expansion, with a CAGR of 19.3% in volume and 27% in value",
              C_PSR)])
Q("008", "C-NPCI08-05", T, S, "Advanced",
  "Consider the following statements about RBI's directions on due diligence of AePS touchpoint operators (ATOs):\nI. "
  "If an ATO's due diligence has already been done as a Business Correspondent or sub-agent, the acquiring bank may "
  "adopt it.\nII. The acquiring bank must ensure that technological integrations such as APIs are used only for "
  "enabling AePS operations.\nIII. The directions apply only to scheduled commercial banks, not to co-operative "
  "banks.\nWhich of the above is/are correct?",
  ["I and II only", "I only", "II and III only", "I, II and III"],
  concept="AePS touchpoint operators",
  explanation="Banks must do customer due diligence of ATOs before onboarding, but may adopt due diligence already done "
              "for them as BCs/sub-agents (I correct). They must put in place system-level controls so that APIs are "
              "used only for AePS operations (II correct). The circular is addressed to scheduled commercial banks "
              "including RRBs, urban co-operative banks, state and district central co-operative banks, and NPCI (III "
              "wrong).",
  steps=["I → correct", "II → correct", "III → wrong (co-operative banks also covered)"],
  why="Options with III are wrong; 'I only' misses II.",
  facts=[fact("if the due diligence of ATOs has already been done in their capacity as Business Correspondent / "
              "sub-agent, then the same may be adopted", C_AEPS),
         fact("The acquiring bank shall put in place adequate system level controls to ensure that any technological "
              "integrations like APIs are used only for enabling AePS operations", C_AEPS),
         fact("All Scheduled Commercial Banks including RRBs / Urban Cooperative Banks / State Cooperative Banks / "
              "District Central Cooperative Banks / National Payments Corporation of India (NPCI)", C_AEPS)])

pl21, pl25, ft21, ft25 = 964, 1896, 4.42e7, 11.87e7
r_pl, r_ft = pl25 / pl21, ft25 / ft21
per21, per25 = ft21 / pl21, ft25 / pl25
assert round(r_pl, 1) == 2.0 and round(r_ft, 1) == 2.7 and round(per21, -3) == 46000 and round(per25, -3) == 63000
Q("008", "C-NPCI08-06", T, S, "Advanced",
  "According to RBI's Payment Systems Report (December 2025), toll plazas onboarded on NETC rose from 964 in December "
  "2021 to 1,896 in December 2025, while FASTags issued grew from 4.42 crore to 11.87 crore. Which statement is "
  "correct?",
  ["FASTags grew about 2.7 times and toll plazas about 2 times, so FASTags per plaza rose from about 46,000 to about "
   "63,000",
   "Toll plazas grew faster than FASTags, so FASTags per plaza fell",
   "Both grew about 2.7 times, leaving FASTags per plaza unchanged",
   "FASTags per plaza rose from about 4,600 to about 6,300"],
  concept="NETC infrastructure growth",
  explanation="Toll plazas: 1,896 ÷ 964 ≈ 1.97 times. FASTags: 11.87 ÷ 4.42 ≈ 2.69 times. FASTags per plaza: 4.42 crore "
              "÷ 964 ≈ 45,900 in 2021 and 11.87 crore ÷ 1,896 ≈ 62,600 in 2025.",
  steps=["Plazas ×1.97", "FASTags ×2.69", "Per plaza: ≈45,900 → ≈62,600"],
  why="FASTags grew faster, so the per-plaza figure rose; the 4,600/6,300 option is off by a factor of ten.",
  computed=True, current=ca("2026-05-18"),
  facts=[fact("The number of toll plazas onboarded increased from 964 in December 2021 to 1,896 in December 2025. "
              "FASTag issuance grew from 4.42 crore to 11.87 crore during this period", C_PSR)])

Q("009", "C-NPCI09-01", T, S, "Basic",
  "Under RBI's Bharat Bill Payment System Directions, 2024, what must happen before a bill payment is initiated "
  "through BBPS (other than for prepaid services)?",
  ["The bill must be fetched", "The biller must send a paper bill to the customer",
   "The customer must visit an agent outlet", "NPCI must approve each payment"],
  concept="Bill fetch in BBPS",
  explanation="The Directions describe BBPS, operated by NPCI's subsidiary NBBL, as an integrated platform for paying "
              "bills through multiple channels and modes; transactions require the bill to be fetched before payment "
              "initiation, while for prepaid services the customer's relationship with the biller is validated through "
              "the platform.",
  steps=["Postpaid bills → fetched first", "Prepaid services → relationship validated"],
  why="Paper bills, agent visits or NPCI approval of each payment are not required.",
  facts=[fact("The transactions facilitated through this platform will require the bill to be fetched before payment "
              "initiation. In case of transactions involving payments for prepaid services, the customer relationship "
              "with the biller will be validated through the platform", C_BBPS)])
Q("009", "C-NPCI09-02", T, S, "Intermediate",
  "Under RBI's Digital Payments – E-mandate Framework, 2026, for which of the following e-mandates is the issuer NOT "
  "required to send a pre-transaction notification before the debit?",
  ["E-mandates registered to auto-replenish FASTag and National Common Mobility Card (NCMC) balances",
   "E-mandates for mutual fund SIPs", "E-mandates for insurance premiums",
   "E-mandates for credit card bill payments"],
  concept="FASTag auto-replenishment",
  explanation="Issuers must normally send a pre-transaction notification at least 24 hours before an e-mandate debit, "
              "but it is not required for e-mandates registered to auto-replenish FASTag and NCMC balances.",
  steps=["General rule: pre-debit notice ≥ 24 hours", "Exception: FASTag and NCMC auto-replenishment"],
  why="SIPs, insurance premiums and credit card bills have a higher AFA-free limit but still need pre-debit notices.",
  current=ca("2026-04-21"),
  facts=[fact("Pre-transaction notification is not required for e-mandates registered to auto-replenish balances of "
              "FASTag, and National Common Mobility Card (NCMC)", C_EMAND)])
Q("009", "C-NPCI09-03", T, S, "Intermediate",
  "How does RBI's Payment Systems Report (December 2025) describe the Aadhaar Enabled Payment System (AePS)?",
  ["A bank-led model for interoperable financial inclusion transactions at micro-ATM terminals through Business "
   "Correspondents, using Aadhaar authentication",
   "A card-based system in which customers use RuPay debit cards at ATMs",
   "A non-bank wallet system regulated as a prepaid payment instrument",
   "A system for bulk credit of salaries operated by UIDAI"],
  concept="AePS model",
  explanation="RBI describes AePS as a bank-led model that facilitates online interoperable financial inclusion "
              "transactions at PoS (micro-ATM) terminals through banks' Business Correspondents, using Aadhaar "
              "authentication; UIDAI verifies biometrics and NPCI handles switching, clearing and settlement.",
  steps=["AePS: bank-led, BC micro-ATMs, Aadhaar authentication"],
  why="AePS is not card-based or a wallet system, and UIDAI does not operate a bulk-credit system.",
  facts=[fact("Aadhaar-enabled Payment System (AePS) is a bank-led model that facilitates online interoperable financial "
              "inclusion transactions at Point of Sale (Micro ATM) terminals through Business Correspondents of banks, "
              "using Aadhaar authentication", C_PSR)])
Q("009", "C-NPCI09-04", T, S, "Intermediate",
  "Under RBI's framework on turn-around time for failed transactions, there is a delay in crediting a beneficiary's "
  "account through the Aadhaar Payments Bridge System (APBS), used for government benefits. What must be done?",
  ["The beneficiary bank must reverse the transaction within T + 1 day, with ₹100 per day of delay beyond that",
   "The remitting government department must re-send the payment within T + 5 days",
   "NPCI must credit the beneficiary from its own funds within T + 3 days",
   "No time limit applies, as APBS payments are government transfers"],
  concept="TAT for APBS",
  explanation="For APBS, where there is a delay in crediting the beneficiary's account, the beneficiary bank must reverse "
              "the transaction within T + 1 day; compensation of ₹100 per day applies if the delay goes beyond T + 1.",
  steps=["APBS credit delay → beneficiary bank reverses by T + 1", "₹100/day beyond T + 1"],
  why="The framework places the duty on the beneficiary bank, not the department or NPCI, and APBS is covered.",
  facts=[fact("Aadhaar Payment Bridge System (APBS) a Delay in crediting beneficiary's account. Beneficiary bank to "
              "reverse the transaction within T + 1 day. ₹100/- per day if delay is beyond T + 1 day", C_TAT)])
Q("009", "C-NPCI09-05", T, S, "Advanced",
  "Consider the following statements about the Bharat Bill Payment System (BBPS) under RBI's BBPS Directions, 2024, "
  "operated by NPCI's subsidiary NPCI Bharat BillPay Ltd (NBBL):\nI. A non-bank BBPOU must open an escrow account with "
  "a scheduled commercial bank exclusively for BBPS transactions.\nII. A sponsor bank, which is a scheduled commercial "
  "bank, facilitates settlement of non-bank BBPOUs with NBBL.\nIII. A Customer Operating Unit (COU) is the entity that "
  "onboards billers onto the BBPS platform.\nWhich of the above is/are correct?",
  ["I and II only", "II only", "I and III only", "I, II and III"],
  concept="BBPS structure",
  explanation="Non-bank BBPOUs must keep an escrow account with an SCB exclusively for BBPS (I correct). A sponsor bank "
              "(an SCB) facilitates their settlement with NBBL (II correct). Billers are onboarded by a Biller "
              "Operating Unit (BOU); a COU provides customers the interface to pay bills (III wrong).",
  steps=["I → correct", "II → correct", "III → wrong (BOU onboards billers)"],
  why="Options with III confuse COU and BOU; 'II only' misses I.",
  facts=[fact("A non-bank BBPOU shall open an escrow account with a Scheduled Commercial Bank exclusively for BBPS "
              "transactions", C_BBPS),
         fact("Sponsor bank: A Scheduled Commercial Bank which facilitates settlement of non-bank BBPOUs with NBBL",
              C_BBPS),
         fact("Biller Operating Unit (BOU) is an entity which onboards biller(s) ... Customer Operating Unit (COU) is an "
              "entity which provides its customers with an interface (physical / digital) to pay bills", C_BBPS)])

Q("010", "C-NPCI10-01", T, S, "Basic",
  "Under RBI's directions of June 2025 on the Aadhaar Enabled Payment System, an 'AePS Touchpoint Operator (ATO)' is:",
  ["The individual onboarded by the acquiring bank who operates the AePS touchpoint",
   "The company that manufactures micro-ATM terminals", "The UIDAI official who verifies biometrics",
   "The NPCI unit that settles AePS transactions"],
  concept="AePS touchpoint operators",
  explanation="The directions define the AePS touchpoint as the terminal (mobile or fixed) deployed by acquirer banks "
              "for AePS transactions, and the ATO as the individual onboarded by the acquiring bank who operates it.",
  steps=["Touchpoint = terminal deployed by acquirer bank", "ATO = individual operating it, onboarded by that bank"],
  why="Device makers, UIDAI and NPCI are not ATOs.",
  facts=[fact("AePS Touchpoint Operator (ATO): The individual onboarded by the acquiring bank who operates the AePS "
              "touchpoint", C_AEPS)])
Q("010", "C-NPCI10-02", T, S, "Intermediate",
  "Under RBI's AePS directions, which aspects must form part of an acquiring bank's fraud risk management framework "
  "when it monitors AePS touchpoint operators?",
  ["Location and type of the ATO and the volume and velocity of transactions",
   "Only the ATO's educational qualifications", "Only the number of customers the ATO personally knows",
   "Only the ATO's income tax returns"],
  concept="Monitoring AePS operators",
  explanation="The acquiring bank must monitor ATOs through its transaction monitoring systems on an ongoing basis and "
              "set operational parameters based on their business risk profile; aspects such as location and type of "
              "the ATO and the volume and velocity of transactions form part of its fraud risk management framework, "
              "and the parameters are reviewed periodically for emerging fraud trends.",
  steps=["Ongoing monitoring", "Parameters: location, type, volume, velocity", "Periodic review"],
  why="The other options are not what RBI prescribes.",
  facts=[fact("Aspects such as location and type of the ATO, volume and velocity of transactions, etc. shall form part "
              "of bank's fraud risk management framework", C_AEPS)])
Q("010", "C-NPCI10-03", T, S, "Intermediate",
  "According to RBI's Payment Systems Report (December 2025), what recent enhancement has been made to the Bharat Bill "
  "Payment System, operated by NPCI's subsidiary NBBL?",
  ["A cross-border bill payment facility that lets NRIs pay utility, education and other bills in India for their "
   "families",
   "Settlement of bill payments in foreign currency within India",
   "Payment of bills only through bank branches", "Removal of insurance premiums from BBPS"],
  concept="BBPS cross-border facility",
  explanation="RBI notes that a recent BBPS enhancement is a cross-border bill payment facility allowing Non-Resident "
              "Indians to pay utility, education and other bills in India on behalf of their families.",
  steps=["BBPS → cross-border inward bill payments by NRIs"],
  why="There is no foreign-currency settlement within India, branch-only restriction or removal of insurance.",
  current=ca("2026-05-18"),
  facts=[fact("A recent enhancement to BBPS includes a cross-border bill payment facility that allows Non-Resident "
              "Indians (NRIs) to pay utility, education, and other bills in India on behalf of their families", C_PSR)])
Q("010", "C-NPCI10-04", T, S, "Advanced",
  "Match each failed transaction with the turn-around time (TAT) rule in RBI's harmonised framework:\n1. Account "
  "debited but cash not dispensed at an ATM or micro-ATM\n2. AePS: account debited but confirmation not received at "
  "the merchant location\n3. NACH: account debited despite the customer having revoked the debit mandate with the "
  "bank\n4. PPI on-us: PPI debited but the beneficiary's PPI not credited\nP. Pro-active reversal within T + 5 days\nQ. "
  "Acquirer to initiate 'Credit Adjustment' within T + 5 days\nR. Customer's bank responsible; resolution within T + 1 "
  "day\nS. Reversal in the remitter's account within T + 1 day",
  ["1-P, 2-Q, 3-R, 4-S", "1-Q, 2-P, 3-R, 4-S", "1-P, 2-Q, 3-S, 4-R", "1-S, 2-Q, 3-R, 4-P"],
  concept="TAT across payment systems",
  explanation="ATM/micro-ATM cash not dispensed → pro-active reversal within T + 5. AePS merchant confirmation not "
              "received → acquirer's 'Credit Adjustment' within T + 5. NACH debit despite mandate revocation → the "
              "customer's bank is responsible and must resolve within T + 1. PPI on-us failure → reversal in the "
              "remitter's account within T + 1. Each carries ₹100 per day for delay beyond the TAT where compensation "
              "applies.",
  steps=["1 → P", "2 → Q", "3 → R", "4 → S"],
  why="The other options swap the ATM and AePS rules or the NACH and PPI rules.",
  facts=[fact("Customer's account debited but cash not dispensed. Pro-active reversal (R) of failed transaction within a "
              "maximum of T + 5 days", C_TAT),
         fact("Aadhaar Enabled Payment System (including Aadhaar Pay) a Account debited but transaction confirmation not "
              "received at merchant location. Acquirer to initiate 'Credit Adjustment' within T + 5 days", C_TAT),
         fact("Account debited despite revocation of debit mandate with the bank by the customer. Customer's bank will "
              "be responsible for such debit. Resolution to be completed within T + 1 day", C_TAT),
         fact("On-Us transaction Beneficiary's PPI not credited. PPI debited but transaction confirmation not received "
              "at merchant location. Reversal effected in Remitter's account within T + 1 day", C_TAT)])

Q("010", "C-NPCI10-05", T, S, "Intermediate",
  "According to RBI's Payment Systems Report (December 2025), how did AePS fund transfers and BHIM Aadhaar Pay "
  "transactions grow between CY 2021 and CY 2025?",
  ["Slowly: volume from 212 lakh to 231 lakh and value from ₹5,697 crore to ₹7,422 crore (CAGR about 2% and 7%)",
   "Rapidly: volume grew more than ten times, like UPI",
   "They declined in both volume and value, like debit card transactions",
   "Volume grew about 7% a year while value fell"],
  concept="AePS growth",
  explanation="RBI reports that AePS (fund transfers) and BHIM Aadhaar Pay volume rose from 212 lakh in CY 2021 to 231 "
              "lakh in CY 2025 and value from ₹5,697 crore to ₹7,422 crore, CAGRs of 2.1% in volume and 6.8% in value.",
  steps=["Volume 212 → 231 lakh (2.1% CAGR)", "Value ₹5,697 → ₹7,422 crore (6.8% CAGR)"],
  why="Growth was modest, not tenfold; neither measure declined.",
  current=ca("2026-05-18"),
  facts=[fact("The volume of transactions conducted through AePS (fund transfers) and BHIM Aadhaar Pay increased from "
              "212 lakh in CY 2021 to 231 lakh in CY 2025. The corresponding value of these transactions rose from "
              "₹5,697 crore to ₹7,422 crore over the same period ... a CAGR of 2.1 per cent in volume and 6.8 per cent "
              "in value", C_PSR)])


# ================================================================= checks and output
NOTES = ("Banking and Financial Awareness topic package 2 (NPA, Basel Norms, Financial Inclusion, Priority Sector "
         "Lending, RBI Integrated Ombudsman Scheme, Digital Banking, UPI, NEFT, RTGS, IMPS, NPCI), fragment for {bid}: "
         "{n} original questions ({diff}), IDs {lo} to {hi}. Built by tools/packages/BFA_pkg2.py from sources opened on "
         "2026-11-06 with a plain client (RBI's consolidated Commercial Banks Directions of November 2025 as updated - "
         "IRACP, Resolution of Stressed Assets, Asset Liability Management, Branch Authorisation, Digital Banking "
         "Channels - the PSL Directions and FAQs, RB-IOS 2026 FAQs, e-rupee, NEFT, RTGS, LEI, INRF and ARC FAQs, the "
         "E-mandate Framework 2026, Authentication Directions 2025, PPI and BBPS Directions, RBI press releases and "
         "Payment Systems Report, BIS, IBBI and Government pages). rbidocs PDFs, npci.org.in and pib.gov.in were not "
         "fetched (they block automated access); facts seen only in search results are marked web:search-confirmed. "
         "Only current rules are tested; older documents appear only as explicitly historical facts. Computed "
         "answers are re-derived with asserts. Facts tested in BATCH_000-BATCH_007 are not repeated. "
         "ai:independent-check marks only questions a separate fresh solver answered blind and matched with "
         "confidence.")

all_tags = {t for b in BATCHES for t, _ in records[b]}
assert INDEPENDENT <= all_tags, INDEPENDENT - all_tags
outputs = {}
for b in BATCHES:
    spec = PKG["batches"][b]
    recs = records[b]
    planned = {(t["topic"], d): n for t in spec["topics"] for d, n in t["quota"].items() if n}
    subtopics = {t["topic"]: set(t["subtopics"]) for t in spec["topics"]}
    have = Counter((r["topic"], r["difficulty"]) for _, r in recs)
    assert have == Counter(planned), (b, sorted(set(have.items()) ^ set(planned.items())))
    assert len(recs) == spec["count"], (b, len(recs))
    assert Counter(r["difficulty"] for _, r in recs) == Counter(spec["by_difficulty"]), b
    assert all(r["subtopic"] in subtopics[r["topic"]] for _, r in recs), b
    lo, hi = spec["question_ids"]
    first = int(lo.rsplit("_", 1)[1])
    assert int(hi.rsplit("_", 1)[1]) - first + 1 == len(recs), b
    questions = []
    for i, (tag, r) in enumerate(recs):
        r["question_id"] = f"BANK_BFA_{first + i:06d}"
        if tag in INDEPENDENT:
            r["verification"]["verified_by"].append("ai:independent-check")
        questions.append(r)
    assert questions[0]["question_id"] == lo and questions[-1]["question_id"] == hi, b
    assert spec["stimulus_id_start"] == f"STIM_BFA_{b}201"     # no stimulus sets are used in this package
    assert all(q["verification"]["fact_checks"] for q in questions)
    for q in questions:
        ev = q.get("current_affairs", {}).get("event_date")
        assert ev is None or ev <= CHECKED, (q["question_id"], ev)
    k = _keys[b]
    assert max(k.values()) - min(k.values()) <= 2, (b, k)
    outputs[b] = (spec, questions)

texts = [q["question_text"] for b in BATCHES for q in outputs[b][1]]
assert len(set(texts)) == len(texts) == PKG["total"]

for b in BATCHES:
    spec, questions = outputs[b]
    diff = ", ".join(f"{spec['by_difficulty'][d]} {d}" for d in ("Basic", "Intermediate", "Advanced"))
    frag = {
        "schema_version": "1.0",
        "batch_id": spec["batch_id"],
        "created_at": TODAY,
        "notes": NOTES.format(bid=spec["batch_id"], n=len(questions), diff=diff, lo=spec["question_ids"][0],
                              hi=spec["question_ids"][1]),
        "stimuli": [],
        "questions": questions,
    }
    out = ROOT / spec["output"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(questions)} questions; keys {dict(sorted(_keys[b].items()))}; current_affairs "
          f"{sum('current_affairs' in q for q in questions)}; independent "
          f"{sum('ai:independent-check' in q['verification']['verified_by'] for q in questions)})")
