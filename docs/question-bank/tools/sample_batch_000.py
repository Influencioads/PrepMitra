"""Writes batches/BATCH_000_sample.json: the 20 fully solved sample questions for approval.

Every computable answer is re-derived here before the file is written (series, roots, instalments, DI, the floor
puzzle by brute force, the syllogism over all Venn models, the inequality over integer assignments, COUNTA). If any
assertion fails, nothing is written.

    python docs/question-bank/tools/sample_batch_000.py
"""

import itertools
import json
from fractions import Fraction as F
from pathlib import Path

from qbank import default_mappings

ROOT = Path(__file__).resolve().parent.parent
TODAY = "2026-11-05"
LETTERS = "ABCD"


def q(qid, subject, topic, subtopic, difficulty, text, options, answer, concept, explanation, steps, shortcut=None,
      why_others_wrong=None, seconds=60, stimulus=None, position=None, mappings=None, current_affairs=None,
      fact_checks=None, verified_by=("ai:author-solve", "ai:independent-check")):
    assert answer in LETTERS[: len(options)]
    out = {
        "question_id": qid,
        "exam_mappings": mappings or default_mappings(subject, difficulty),
        "subject": subject, "topic": topic, "subtopic": subtopic, "difficulty": difficulty,
        "question_type": "MCQ", "language": "en",
    }
    if stimulus:
        out |= {"stimulus_id": stimulus, "set_position": position}
    out |= {
        "question_text": text,
        "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(options)],
        "correct_answer": answer,
        "solution": {"concept": concept, "explanation": explanation, "steps": steps, "shortcut": shortcut,
                     "why_others_wrong": why_others_wrong,
                     "final_answer": f"Option {answer}: {options[LETTERS.index(answer)]}"},
        "suggested_time_seconds": seconds,
    }
    if current_affairs:
        out["current_affairs"] = current_affairs
    out["source"] = {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                     "original_exam_year": None, "license_note": None}
    out["verification"] = {"answer_verified": True, "solution_verified": True,
                           "review_status": "Pending Human Review", "verified_by": list(verified_by),
                           "verified_at": TODAY, **({"fact_checks": fact_checks} if fact_checks else {})}
    return out


def fact(claim, url):
    return {"claim": claim, "source_url": url, "checked_on": TODAY}


QA, RA, EN = "Quantitative Aptitude", "Reasoning Ability", "English Language"
GA, BF, CK = "General Awareness and Current Affairs", "Banking and Financial Awareness", "Computer Knowledge"
RECOMPUTED = ("script:recompute", "ai:author-solve")

# ---------------------------------------------------------------- verification of computable answers
series = [12]
for k in range(1, 6):
    series.append(series[-1] * k + k)
assert series == [12, 13, 28, 87, 352, 1765]

roots = lambda a, b, c: {F(-b + s, 2 * a) for s in (int((b * b - 4 * a * c) ** 0.5), -int((b * b - 4 * a * c) ** 0.5))}
xs, ys = roots(2, -13, 21), roots(3, -17, 24)
assert xs == {F(3), F(7, 2)} and ys == {F(3), F(8, 3)}
assert all(x >= y for x in xs for y in ys) and any(x == y for x in xs for y in ys)  # x >= y, equality possible

principal = F(14400) / F(6, 5) + F(14400) / F(6, 5) ** 2
assert principal == 22000 and 2 * 14400 - principal * F(13, 10) == 200

DI = {"P": (1200, 60), "Q": (1500, 52), "R": (900, 70), "S": (1600, 45), "T": (1000, 64)}
sav = {b: F(n * p, 100) for b, (n, p) in DI.items()}
cur = {b: DI[b][0] - sav[b] for b in DI}
assert cur["Q"] / cur["S"] == F(9, 11)
pct_more = (sav["P"] + sav["R"] + sav["T"] - cur["Q"] - cur["S"]) / (cur["Q"] + cur["S"]) * 100
assert (sav["P"] + sav["R"] + sav["T"], cur["Q"] + cur["S"]) == (1990, 1600) and pct_more == F(24375, 1000)

people = "JKLMNOP"
solutions = []
for perm in itertools.permutations(range(1, 8)):
    f = dict(zip(people, perm))
    if (f["K"] % 2 == 1 and f["K"] > 4 and abs(f["K"] - f["N"]) == 3 and f["M"] == f["N"] + 1
            and 1 < f["P"] < f["M"] and abs(f["O"] - f["P"]) == 2 and f["L"] > f["J"]):
        solutions.append(f)
assert solutions == [dict(O=1, J=2, P=3, N=4, M=5, L=6, K=7)], solutions
FLOORS = solutions[0]
assert FLOORS["M"] - FLOORS["J"] - 1 == 2 and FLOORS["L"] == FLOORS["M"] + 1

# Syllogism: sets bank, branch, office, vault -> 16 Venn regions, each present or absent (2^16 models)
regions = list(itertools.product((0, 1), repeat=4))  # (bank, branch, office, vault)
some = lambda m, pred: any(m[r] and pred(r) for r in regions)
valid_models = []
for bits in itertools.product((0, 1), repeat=16):
    m = dict(zip(regions, bits))
    if (some(m, lambda r: r[0] and r[1]) and some(m, lambda r: r[0] and not r[1])  # only a few banks are branches
            and not some(m, lambda r: r[1] and not r[2])                             # all branches are offices
            and not some(m, lambda r: r[2] and r[3])):                               # no office is a vault
        valid_models.append(m)
assert all(some(m, lambda r: r[0] and not r[3]) for m in valid_models)             # I: some banks are not vaults
assert any(not some(m, lambda r: r[0] and not r[2]) for m in valid_models)         # II: all banks offices possible

ineq_I, ineq_II = True, True
for P, Q, R, S, T, U in itertools.product(range(5), repeat=6):
    if P >= Q > R == S <= T < U:
        ineq_I &= P > S
        ineq_II &= T > R
assert ineq_I and not ineq_II

cells = [25, None, "Loan", 0, "#N/A", None]
assert sum(c is not None for c in cells) == 4

# ---------------------------------------------------------------- stimuli
stimuli = [
    {"stimulus_id": "STIM_QUANT_000001", "type": "data_table", "title": "Accounts opened by five branches in 2025",
     "content": "The table shows the total number of new accounts opened by five branches P, Q, R, S and T of a bank "
                "in 2025 and the percentage of those that were savings accounts. All remaining accounts were current "
                "accounts.\n\n| Branch | Total accounts opened | Savings accounts (%) |\n|---|---:|---:|\n"
                "| P | 1,200 | 60 |\n| Q | 1,500 | 52 |\n| R | 900 | 70 |\n| S | 1,600 | 45 |\n| T | 1,000 | 64 |",
     "chart_data": {"columns": ["branch", "total", "savings_pct"],
                    "rows": [[b, n, p] for b, (n, p) in DI.items()]}},
    {"stimulus_id": "STIM_REAS_000001", "type": "puzzle", "title": "Seven persons on seven floors",
     "content": "Seven persons J, K, L, M, N, O and P live on different floors of a seven-storey building. The "
                "lowermost floor is numbered 1 and the topmost floor is numbered 7.\n\n"
                "- K lives on an odd-numbered floor above floor 4.\n"
                "- Exactly two persons live between K and N.\n"
                "- M lives immediately above N.\n"
                "- P lives on a floor below M, but not on floor 1.\n"
                "- Only one person lives between O and P.\n"
                "- L lives on a floor above J.",
     "solution": "Case K = 5: N is two floors away with two persons between, so N = 2 (8 does not exist) and M = 3. "
                 "P must be below M and not on floor 1, so P = 2, but N is on 2: contradiction. Case K = 7: N = 4, "
                 "M = 5. P is on 2 or 3. If P = 2, O must be on 4 (taken by N): contradiction. So P = 3 and O = 1 "
                 "(5 is taken by M). Floors 2 and 6 remain for J and L; L is above J, so L = 6 and J = 2.\n\n"
                 "| Floor | Person |\n|---|---|\n| 7 | K |\n| 6 | L |\n| 5 | M |\n| 4 | N |\n| 3 | P |\n"
                 "| 2 | J |\n| 1 | O |"},
    {"stimulus_id": "STIM_ENG_000001", "type": "passage", "title": "Data-driven credit",
     "content": "When a small shopkeeper in a district town applies for a working-capital loan today, the decision may "
                "rest less on the collateral she can pledge than on the trail of digital payments her shop has "
                "generated. Lenders that once relied almost entirely on audited balance sheets now read the steady "
                "rhythm of UPI receipts, GST filings and utility payments as evidence of a business's health. For "
                "borrowers who were previously invisible to the formal system, this shift has been transformative: "
                "credit that once required a guarantor and weeks of paperwork can be sanctioned in hours.\n\n"
                "Yet the same data that opens doors can also close them. A shop whose customers prefer cash leaves a "
                "thin digital footprint, and an algorithm trained on urban, card-heavy merchants may read that "
                "thinness as risk rather than as habit. Regulators have therefore begun to insist that lenders "
                "explain the basis of automated decisions and give borrowers a way to contest them. The promise of "
                "data-driven credit, in other words, depends not only on how much data is collected but on how "
                "fairly it is interpreted."},
]

RBI_HOME = "https://www.rbi.org.in/"
RBI_POLICY = "https://www.rbi.org.in/Scripts/Annualpolicy.aspx"
RTGS_FAQ = "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=275"
PSL_MD = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12799"
BCBS_LCR = "https://www.bis.org/publ/bcbs238.htm"

questions = [
    # ------------------------------------------------------------ Quantitative Aptitude
    q("BANK_QUANT_000001", QA, "Number Series", "Pattern: multiply-add", "Basic",
      "What will come in place of the question mark (?) in the following number series?\n12, 13, 28, 87, 352, ?",
      ["1760", "1765", "1770", "1755"], "B",
      "Mixed multiply-and-add series",
      "Each term is the previous term multiplied by n and then increased by n, with n going 1, 2, 3, 4, 5.",
      ["12 × 1 + 1 = 13", "13 × 2 + 2 = 28", "28 × 3 + 3 = 87", "87 × 4 + 4 = 352",
       "352 × 5 + 5 = 1760 + 5 = 1765"],
      shortcut="The terms grow roughly ×1, ×2, ×3, ×4, so test ×n + n first: the next term must be just above "
               "352 × 5 = 1760, which leaves only 1765 among the options.",
      seconds=35, verified_by=RECOMPUTED),
    q("BANK_QUANT_000002", QA, "Quadratic Equations", "Relation between roots", "Intermediate",
      "In the following question, two equations numbered I and II are given. Solve both equations and choose the "
      "correct relation between x and y.\nI. 2x² − 13x + 21 = 0\nII. 3y² − 17y + 24 = 0",
      ["x > y", "x ≥ y", "x < y", "x = y or the relationship cannot be established"], "B",
      "Factorising quadratics and comparing every pair of roots",
      "x takes the values 3 and 3.5, y takes the values 3 and 8/3. Every x is greater than or equal to every y, and "
      "x = y is possible (both can be 3), so the relation is x ≥ y.",
      ["I: 2x² − 13x + 21 = 2x² − 6x − 7x + 21 = 2x(x − 3) − 7(x − 3) = (x − 3)(2x − 7), so x = 3 or 3.5",
       "II: 3y² − 17y + 24 = 3y² − 9y − 8y + 24 = 3y(y − 3) − 8(y − 3) = (y − 3)(3y − 8), so y = 3 or 2.67",
       "Compare all pairs: (3, 3) equal; (3, 2.67) x > y; (3.5, 3) x > y; (3.5, 2.67) x > y",
       "No pair has x < y and one pair is equal, so x ≥ y"],
      shortcut="Sign rule: both equations have form (+, −, +), so all roots are positive; then compare the smallest "
               "x (3) with the largest y (3). Equal values mean the answer is x ≥ y.",
      why_others_wrong="x > y fails because x = y = 3 is possible; x < y fails because x is never smaller; option D "
                       "would apply only if the comparison flipped between pairs.",
      seconds=45, verified_by=RECOMPUTED),
    q("BANK_QUANT_000003", QA, "Compound Interest", "Instalments", "Advanced",
      "Ravi borrowed a sum at 20% per annum compound interest, compounded annually, and repaid it in two equal "
      "annual instalments of ₹14,400 each. Had he borrowed the same sum at 15% per annum simple interest and "
      "repaid the whole amount at the end of 2 years, how much less would he have paid in total?",
      ["₹200", "₹400", "₹600", "₹800"], "A",
      "Present value of equal instalments under compound interest; simple-interest amount",
      "Each instalment is discounted back to today at 20%: the sum borrowed is ₹22,000. Under the instalment plan he "
      "pays ₹28,800 in total; under simple interest he pays 22,000 × 1.30 = ₹28,600, which is ₹200 less.",
      ["Present value of instalment 1 = 14,400 ÷ 1.2 = ₹12,000",
       "Present value of instalment 2 = 14,400 ÷ (1.2)² = 14,400 ÷ 1.44 = ₹10,000",
       "Sum borrowed = 12,000 + 10,000 = ₹22,000",
       "Total paid by instalments = 2 × 14,400 = ₹28,800",
       "Simple interest for 2 years at 15% = 22,000 × 30% = ₹6,600, so amount = ₹28,600",
       "Difference = 28,800 − 28,600 = ₹200"],
      shortcut="At 20% (= 1/5), the factor is 6/5. Instalment × (5/6 + 25/36) = 14,400 × 55/36 = 22,000.",
      seconds=90, verified_by=RECOMPUTED),
    q("BANK_QUANT_000004", QA, "Tabular DI", "Table with percentages", "Intermediate",
      "What is the ratio of the number of current accounts opened by branch Q to the number of current accounts "
      "opened by branch S?",
      ["9 : 11", "11 : 9", "8 : 11", "9 : 10"], "A",
      "Complement of a percentage and ratio reduction",
      "Current accounts are the accounts that are not savings accounts. Q opened 48% of 1,500 = 720 current "
      "accounts and S opened 55% of 1,600 = 880, giving 720 : 880 = 9 : 11.",
      ["Current accounts at Q = 1,500 × (100 − 52)% = 1,500 × 0.48 = 720",
       "Current accounts at S = 1,600 × (100 − 45)% = 1,600 × 0.55 = 880",
       "Ratio = 720 : 880; divide both by 80 to get 9 : 11"],
      shortcut="Ratio = (1,500 × 48) : (1,600 × 55) = (15 × 48) : (16 × 55) = 720 : 880 = 9 : 11.",
      seconds=45, stimulus="STIM_QUANT_000001", position=1, verified_by=RECOMPUTED),
    q("BANK_QUANT_000005", QA, "Tabular DI", "Table with percentages", "Advanced",
      "The total number of savings accounts opened by branches P, R and T together is what percent more than the "
      "total number of current accounts opened by branches Q and S together?",
      ["22.5%", "24.375%", "25.625%", "19.6%"], "B",
      "Percentage more than: (difference ÷ base) × 100",
      "Savings accounts at P, R and T total 1,990; current accounts at Q and S total 1,600. The excess of 390 is "
      "24.375% of 1,600.",
      ["Savings: P = 1,200 × 60% = 720; R = 900 × 70% = 630; T = 1,000 × 64% = 640; total = 1,990",
       "Current: Q = 1,500 × 48% = 720; S = 1,600 × 55% = 880; total = 1,600",
       "Difference = 1,990 − 1,600 = 390",
       "Percentage more = 390 ÷ 1,600 × 100 = 24.375%"],
      shortcut="390/1,600 = 39/160; 39/160 = 0.24375, so 24.375%.",
      why_others_wrong="19.6% is 390 ÷ 1,990 (wrong base); the other values come from using a wrong total.",
      seconds=75, stimulus="STIM_QUANT_000001", position=2, verified_by=RECOMPUTED),

    # ------------------------------------------------------------ Reasoning Ability
    q("BANK_REAS_000001", RA, "Floor-Based Puzzles", "Floor and flat", "Intermediate",
      "How many persons live between J and M?", ["None", "One", "Two", "Three"], "C",
      "Floor puzzle: fix the most restricted person first",
      "The arrangement (bottom to top) is O, J, P, N, M, L, K. J is on floor 2 and M on floor 5, so P (3) and N (4) "
      "live between them: two persons.",
      ["K is on an odd floor above 4, so K = 5 or 7",
       "K = 5 forces N = 2, M = 3, and leaves no valid floor for P (must be below M, not 1, and 2 is taken): rejected",
       "K = 7 gives N = 4 and M = 5",
       "P is below M, not on 1 or 4: P = 2 or 3. P = 2 needs O on 4 (taken), so P = 3 and O = 1",
       "Floors 2 and 6 remain; L is above J, so J = 2 and L = 6",
       "Between J (2) and M (5): floors 3 and 4, i.e. P and N, two persons"],
      shortcut="Start from K's two possible floors; the K = 5 branch dies within two lines.",
      seconds=75, stimulus="STIM_REAS_000001", position=1, verified_by=("script:brute-force-unique", "ai:author-solve")),
    q("BANK_REAS_000002", RA, "Floor-Based Puzzles", "Floor and flat", "Intermediate",
      "Which of the following statements is true according to the final arrangement?",
      ["P lives immediately above N", "L lives immediately above M", "O lives on an even-numbered floor",
       "K lives on floor 5"], "B",
      "Checking statements against the solved arrangement",
      "In the final arrangement L is on floor 6 and M on floor 5, so L lives immediately above M.",
      ["Final arrangement (floor: person): 1 O, 2 J, 3 P, 4 N, 5 M, 6 L, 7 K",
       "A: P (3) is below N (4), false", "B: L (6) is immediately above M (5), true",
       "C: O is on floor 1, odd, false", "D: K is on floor 7, false"],
      seconds=40, stimulus="STIM_REAS_000001", position=2, verified_by=("script:brute-force-unique", "ai:author-solve")),
    q("BANK_REAS_000003", RA, "Syllogism", "Possibility cases", "Advanced",
      "Statements:\nOnly a few banks are branches.\nAll branches are offices.\nNo office is a vault.\n\n"
      "Conclusions:\nI. Some banks are not vaults.\nII. All banks being offices is a possibility.",
      ["Only conclusion I follows", "Only conclusion II follows", "Neither conclusion I nor II follows",
       "Both conclusions I and II follow"], "D",
      "'Only a few' = some are and some are not; possibility conclusions",
      "Some banks are branches, those are offices, and no office is a vault, so those banks are definitely not vaults "
      "(I follows). Nothing stops the banks that are not branches from also being offices, so all banks being "
      "offices is possible (II follows).",
      ["'Only a few banks are branches' means: some banks are branches AND some banks are not branches",
       "Some banks are branches + all branches are offices ⇒ some banks are offices",
       "Some banks are offices + no office is a vault ⇒ some banks are not vaults: I follows",
       "Banks outside 'branch' are unrestricted, so they can lie inside 'office': II is possible, so II follows",
       "Both follow"],
      shortcut="For a possibility conclusion, check only whether any statement forbids it. No statement restricts "
               "banks that are not branches, so II follows.",
      why_others_wrong="Students often reject II thinking 'only a few' limits offices; it limits only banks that are "
                       "branches.",
      seconds=50, verified_by=("script:all-venn-models", "ai:author-solve")),
    q("BANK_REAS_000004", RA, "Inequality", "Direct inequality", "Basic",
      "Statement: P ≥ Q > R = S ≤ T < U\n\nConclusions:\nI. P > S\nII. T > R",
      ["Only conclusion I follows", "Only conclusion II follows", "Neither conclusion I nor II follows",
       "Both conclusions I and II follow"], "A",
      "Reading a chain of inequalities",
      "P ≥ Q > R = S gives P > S, so I follows. R = S ≤ T gives only T ≥ R; T could equal R, so T > R is not certain "
      "and II does not follow.",
      ["I: P ≥ Q > R = S. A chain with at least one strict '>' gives a strict result: P > S. Follows",
       "II: R = S ≤ T, so T ≥ R. T = R is possible, so 'T > R' is not definitely true. Does not follow"],
      shortcut="If the path between two letters contains any '≥' or '≤' and no '>' or '<', the strict conclusion "
               "fails.",
      seconds=30, verified_by=("script:exhaustive-integers", "ai:author-solve")),

    # ------------------------------------------------------------ English Language
    q("BANK_ENG_000001", EN, "Reading Comprehension", "Inference", "Intermediate",
      "According to the passage, why might a shop that is otherwise creditworthy still be refused a loan?",
      ["It has not filed GST returns for the past year.",
       "An algorithm trained on different kinds of merchants may read its thin digital footprint as risk.",
       "Regulators have barred lenders from lending to businesses that accept cash.",
       "It cannot provide a guarantor for the loan."], "B",
      "Locating the cause stated in the passage",
      "The second paragraph says a cash-preferring shop leaves a thin digital footprint, and an algorithm trained on "
      "urban, card-heavy merchants may read that thinness as risk rather than habit.",
      ["Find the paragraph that discusses data closing doors: paragraph 2",
       "Identify the stated cause: thin digital footprint misread by a model trained on different merchants",
       "Match it with option B"],
      why_others_wrong="A: GST filings are mentioned only as evidence lenders use, not as a reason for refusal. C: "
                       "regulators ask lenders to explain and allow appeals; there is no ban. D: guarantors belong to "
                       "the old process.",
      seconds=70, stimulus="STIM_ENG_000001", position=1),
    q("BANK_ENG_000002", EN, "Error Detection", "Part-wise error", "Basic",
      "Read the sentence to find out whether there is any grammatical error in it. The part with the error is the "
      "answer. If there is no error, choose 'No error'.\n"
      "Neither the manager nor the clerks (A) / was informed about the change (B) / in the branch's working "
      "hours. (C) / No error (D)",
      ["Neither the manager nor the clerks", "was informed about the change", "in the branch's working hours.",
       "No error"], "B",
      "Subject-verb agreement with 'neither ... nor' (rule of proximity)",
      "With 'neither ... nor', the verb agrees with the subject nearer to it. The nearer subject is 'the clerks' "
      "(plural), so the verb must be 'were', not 'was'.",
      ["Identify the subjects joined by 'neither ... nor': 'the manager' and 'the clerks'",
       "Apply the rule of proximity: the verb follows 'the clerks', which is plural",
       "'was informed' must become 'were informed': the error is in part B"],
      why_others_wrong="Parts A and C are correct as written; 'branch's' correctly shows possession.",
      seconds=30),
    q("BANK_ENG_000003", EN, "Fill in the Blanks", "Double blank", "Intermediate",
      "Choose the pair of words that best fills the blanks.\n"
      "Despite the bank's ______ efforts to recover the loan, the borrower's assets proved too ______ to cover even "
      "half of the outstanding amount.",
      ["sustained, meagre", "half-hearted, abundant", "reluctant, valuable", "persistent, plentiful"], "A",
      "Contrast signalled by 'despite' and the meaning of 'too ... to'",
      "'Despite' needs a positive word for the bank's effort, and 'too ______ to cover' needs a word meaning "
      "insufficient. 'Sustained' and 'meagre' (very small) fit both blanks.",
      ["Blank 1: 'despite' contrasts strong effort with a poor result, so it needs a positive word: sustained or "
       "persistent", "Blank 2: 'too ___ to cover' needs a word meaning insufficient: meagre",
       "Only option A has both: sustained, meagre"],
      why_others_wrong="'Persistent' fits blank 1, but 'too plentiful to cover' is illogical. 'Half-hearted', "
                       "and 'reluctant' remove the contrast that 'despite' requires.",
      seconds=40),

    # ------------------------------------------------------------ General Awareness and Current Affairs
    q("BANK_GA_000001", GA, "Economic Affairs", "Monetary policy decisions", "Intermediate",
      "What policy repo rate did the Reserve Bank of India's Monetary Policy Committee set at its meeting held from "
      "5 to 7 October 2026?",
      ["5.25%", "5.50%", "5.75%", "6.00%"], "B",
      "RBI policy rates after the October 2026 MPC meeting",
      "After the MPC meeting of 5 to 7 October 2026, the policy repo rate stands at 5.50%. The rest of the corridor "
      "is the Standing Deposit Facility rate at 5.25% and the Marginal Standing Facility rate and Bank Rate at "
      "5.75%, i.e. 25 basis points either side of the repo rate.",
      ["The MPC resolution was released on 7 October 2026 (RBI monetary policy page)",
       "RBI's published current rates: Policy Repo 5.50%, SDF 5.25%, MSF 5.75%, Bank Rate 5.75% (checked on "
       "rbi.org.in on 5 November 2026)", "So the repo rate is 5.50%"],
      shortcut="Remember the corridor: SDF = repo − 0.25, MSF = Bank Rate = repo + 0.25.",
      why_others_wrong="5.25% is the SDF rate and 5.75% is the MSF/Bank Rate, which are common traps.",
      seconds=20, current_affairs={"event_date": "2026-10-07", "review_by": "2026-12-04"},
      fact_checks=[fact("MPC meeting held 5-7 October 2026; resolution dated 7 October 2026", RBI_POLICY),
                   fact("Policy Repo 5.50%, SDF 5.25%, MSF 5.75%, Bank Rate 5.75% as displayed on 5 Nov 2026",
                        RBI_HOME)]),
    q("BANK_GA_000002", GA, "Important Reports and Indexes", "Publishing body", "Basic",
      "The Global Financial Stability Report (GFSR) is published by which of the following organisations?",
      ["World Bank", "International Monetary Fund", "Bank for International Settlements", "World Economic Forum"],
      "B",
      "Reports and their publishing bodies",
      "The GFSR is an International Monetary Fund publication, released twice a year (April and October). It "
      "assesses risks to the global financial system.",
      ["Recall the IMF's flagship reports: World Economic Outlook, Global Financial Stability Report and Fiscal "
       "Monitor", "The GFSR is therefore published by the IMF"],
      shortcut="IMF's flagship trio: WEO, GFSR, Fiscal Monitor.",
      why_others_wrong="The World Bank publishes the Global Economic Prospects; the WEF publishes the Global "
                       "Competitiveness and Global Gender Gap reports.",
      seconds=15, fact_checks=[fact("GFSR is an IMF publication released semiannually",
                                    "https://www.imf.org/en/Publications/GFSR")]),
    q("BANK_GA_000003", GA, "National and International Organizations", "Membership", "Basic",
      "The New Development Bank (NDB), established in 2015, was set up by which group of countries?",
      ["SAARC", "BRICS", "G20", "ASEAN"], "B",
      "Multilateral development banks and their founders",
      "The NDB was established in 2015 by Brazil, Russia, India, China and South Africa, i.e. the BRICS countries, "
      "to finance infrastructure and sustainable development projects.",
      ["Recall the founders: Brazil, Russia, India, China, South Africa", "These five form BRICS"],
      shortcut="NDB is often called the 'BRICS Bank'.",
      seconds=15, fact_checks=[fact("NDB was established in 2015 by Brazil, Russia, India, China and South Africa "
                                    "(BRICS)", "https://www.ndb.int/about-ndb/")]),

    # ------------------------------------------------------------ Banking and Financial Awareness
    q("BANK_BFA_000001", BF, "RTGS", "Limits and timings", "Basic",
      "What is the minimum amount that can be remitted through the RTGS system?",
      ["₹50,000", "₹1 lakh", "₹2 lakh", "There is no minimum amount"], "C",
      "Real Time Gross Settlement (RTGS)",
      "RTGS is meant for large-value transfers. RBI's FAQ sets the minimum amount at ₹2,00,000 with no upper "
      "ceiling. RTGS has been available 24x7x365 since 14 December 2020.",
      ["RTGS settles each transaction individually (gross) and in real time in RBI's books",
       "RBI FAQ: minimum ₹2,00,000; no maximum", "So the answer is ₹2 lakh"],
      why_others_wrong="₹1 lakh was an older minimum that is now outdated; NEFT, not RTGS, has no minimum amount.",
      seconds=15, fact_checks=[fact("RTGS minimum ₹2,00,000, no upper ceiling; 24x7x365 from 14 Dec 2020",
                                    RTGS_FAQ)]),
    q("BANK_BFA_000002", BF, "Priority Sector Lending", "Targets and sub-targets", "Intermediate",
      "Under the RBI (Priority Sector Lending – Targets and Classification) Directions, 2025, what is the total "
      "priority sector lending target for domestic scheduled commercial banks (excluding RRBs and SFBs)?",
      ["18% of ANBC or CEOBE, whichever is higher", "32% of ANBC or CEOBE, whichever is higher",
       "40% of ANBC or CEOBE, whichever is higher", "40% of ANBC or CEOBE, whichever is lower"], "C",
      "Priority sector lending targets",
      "Domestic commercial banks (other than RRBs and SFBs) must lend 40% of Adjusted Net Bank Credit (ANBC) or the "
      "Credit Equivalent of Off-Balance Sheet Exposures (CEOBE), whichever is higher, to the priority sector. "
      "Within this, agriculture has a sub-target of 18%.",
      ["Recall the overall PSL target for domestic SCBs: 40%", "The base is ANBC or CEOBE, whichever is HIGHER",
       "18% is the agriculture sub-target, not the total"],
      why_others_wrong="18% is the agriculture sub-target. Option D uses 'lower' instead of 'higher'.",
      seconds=20, fact_checks=[fact("Total PSL target 40% of ANBC or CEOBE, whichever is higher (2025 Directions)",
                                    PSL_MD)]),
    q("BANK_BFA_000003", BF, "Basel Norms", "LCR and NSFR", "Advanced",
      "A bank holds high-quality liquid assets (HQLA) of ₹540 crore. Under a 30-day stress scenario, its expected "
      "cash outflows are ₹900 crore and expected cash inflows are ₹400 crore. What is its Liquidity Coverage Ratio "
      "(LCR), and does it meet the 100% minimum?",
      ["60%; does not meet the minimum", "108%; meets the minimum", "135%; meets the minimum",
       "108%; does not meet the minimum"], "B",
      "Basel III Liquidity Coverage Ratio = Stock of HQLA ÷ Total net cash outflows over the next 30 calendar days",
      "Net cash outflows are outflows minus inflows: 900 − 400 = ₹500 crore. LCR = 540 ÷ 500 = 108%, which is "
      "above the 100% minimum. (The framework caps how much inflow can be counted; that cap does not bind here.)",
      ["Total net cash outflows = 900 − 400 = ₹500 crore", "LCR = 540 ÷ 500 × 100 = 108%",
       "108% ≥ 100%, so the bank meets the requirement"],
      why_others_wrong="60% divides HQLA by gross outflows (540 ÷ 900); 135% divides by inflows (540 ÷ 400).",
      seconds=60, fact_checks=[fact("LCR covers a 30-calendar-day stress scenario with a 100% minimum", BCBS_LCR)]),

    # ------------------------------------------------------------ Computer Knowledge
    q("BANK_COMP_000001", CK, "Internet", "Email", "Basic",
      "Which protocol is used to send email from an email client to a mail server?",
      ["FTP", "SMTP", "POP3", "HTTP"], "B",
      "Email protocols",
      "SMTP (Simple Mail Transfer Protocol) sends or relays outgoing mail. POP3 and IMAP are used to retrieve mail "
      "from a server.",
      ["Sending mail: SMTP", "Receiving mail: POP3 or IMAP", "So the answer is SMTP"],
      why_others_wrong="FTP transfers files and HTTP transfers web pages; POP3 retrieves mail rather than sending it.",
      seconds=15, fact_checks=None),
    q("BANK_COMP_000002", CK, "MS Office", "MS Excel", "Intermediate",
      "In MS Excel, cells A1 to A6 contain: 25, (empty), Loan, 0, #N/A, (empty). What value does the formula "
      "=COUNTA(A1:A6) return?",
      ["2", "3", "4", "5"], "C",
      "COUNT vs COUNTA in Excel",
      "COUNTA counts every cell that is not empty, including text, zero and error values. A1 (25), A3 (Loan), A4 (0) "
      "and A5 (#N/A) are non-empty, so COUNTA returns 4.",
      ["Non-empty cells: A1, A3, A4, A5", "Empty cells A2 and A6 are not counted", "COUNTA = 4"],
      why_others_wrong="2 is what =COUNT(A1:A6) returns, because COUNT counts only numbers (25 and 0).",
      seconds=30, verified_by=("script:recompute", "ai:author-solve")),
]

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_000",
    "created_at": TODAY,
    "notes": "Approval sample: 20 original questions across all six subjects. Not part of the 10,000 count until "
             "approved by a human reviewer.",
    "stimuli": stimuli,
    "questions": questions,
}
assert len(questions) == 20
out = ROOT / "batches" / "BATCH_000_sample.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions, all computable answers re-derived)")
