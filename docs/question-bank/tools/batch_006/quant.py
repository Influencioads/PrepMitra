"""Writes batches/parts/BATCH_006_QUANT.json: the 199 Quantitative Aptitude questions of BATCH_006.

Every answer is recomputed here before the file is written: arithmetic with exact fractions, series regenerated
from their rule (wrong-number series: exactly one term differs from the regenerated series), quadratic roots
substituted back into the equations, probabilities, arrangements, rotations and alternate-day schedules counted by
brute force, data-sufficiency statements checked by enumerating candidate cases, approximation answers checked to
be the option nearest the exact value by a clear margin. If any assertion fails, nothing is written.

Structure and helpers follow tools/batch_005/quant.py (relation-option guards, no-equal-quantity rule for quantity
comparison, balanced key shuffler with a new seed, approximation margin check, set-size asserts). New in this batch:
quantity-comparison values must be at least 2% apart, so rounding in mental arithmetic cannot flip the relation.
Contexts, data sets and number templates are new: all earlier Quant stems (BATCH_000 to BATCH_005) and the 58 earlier
DI titles were read first, and none of their DI themes or arithmetic templates is reused.

    python tools/batch_006/quant.py          (run from docs/question-bank)
    python tools/batch_006/quant.py --dump <file>   (blind copy for solvers: no key, no solution)
"""

import itertools
import json
import math
import random
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import default_mappings, normalize  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-05"
LETTERS = "ABCD"
SUBJECT = "Quantitative Aptitude"
B, I, A = "Basic", "Intermediate", "Advanced"
TOTAL = 199

# Balanced answer keys: 50 A, 50 B, 50 C and 49 D, order fixed by the seed (new seed for batch 6).
_rng = random.Random(20261105 + 6)
KEYS = list("ABCD" * 50)[:TOTAL]
_rng.shuffle(KEYS)

QUESTIONS, STIMULI = [], []
_set_pos = {}
_FIRST_ID = 1006
_FIRST_STIM = 6001
RECOMPUTE = ["script:recompute", "ai:self-recheck"]
BRUTE = ["script:recompute", "script:brute-force-unique", "ai:self-recheck"]

# Questions that a separate, fresh solver re-answered from the stem, options and data set alone (no key, no
# solution) and whose answer matched the key. Only these carry ai:independent-check. Every third question
# (BANK_QUANT_001006, _001009, ..., _001204: 67 questions) was given to two separate fresh solver agents (34 and 33
# questions, blind dumps made with --dump --ids); all 67 answers matched the key, no question was flagged, and none
# was changed afterwards.
INDEPENDENT = {f"BANK_QUANT_{n:06d}" for n in range(1006, 1205, 3)}

# ---------------------------------------------------------------- formatting helpers
VULGAR = {F(1, 2): "½", F(1, 3): "⅓", F(2, 3): "⅔", F(1, 4): "¼", F(3, 4): "¾", F(1, 6): "⅙", F(5, 6): "⅚",
          F(1, 8): "⅛", F(3, 8): "⅜", F(5, 8): "⅝", F(7, 8): "⅞"}


def ind(n: int) -> str:
    """Indian digit grouping: 1234567 -> 12,34,567."""
    s = str(abs(n))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        groups = []
        while len(head) > 2:
            groups.insert(0, head[-2:])
            head = head[:-2]
        if head:
            groups.insert(0, head)
        s = ",".join(groups + [tail])
    return ("−" if n < 0 else "") + s


def N(x, dp=2) -> str:
    if isinstance(x, float):
        x = F(x).limit_denominator(10 ** 6)
    x = F(x)
    sign = "−" if x < 0 else ""
    x = abs(x)
    if x.denominator == 1:
        return sign + ind(int(x))
    whole = x.numerator // x.denominator
    for k in range(1, 5):
        if (x * 10 ** k).denominator == 1:
            digits = str(int((x - whole) * 10 ** k)).rjust(k, "0").rstrip("0")
            return f"{sign}{ind(whole)}.{digits}"
    rem = x - whole
    if rem in VULGAR:
        return f"{sign}{ind(whole) if whole else ''}{VULGAR[rem]}"
    return f"{sign}{float(x):,.{dp}f}"


def R(x) -> str:
    return "₹" + N(x)


def near(a, b, tol=1e-9):
    return abs(float(a) - float(b)) < tol


def r2(x) -> F:
    """Round half up to two decimals (for stems that fix two-decimal precision)."""
    return F(math.floor(F(x) * 100 + F(1, 2)), 100)


def pct2(x) -> str:
    """A fraction shown as a percentage correct to two decimal places, e.g. 0.24475 -> '24.47%'."""
    return f"{float(r2(F(x) * 100)):.2f}%"


# ---------------------------------------------------------------- record builder
def Q(topic, sub, diff, text, ans, wrong, concept, expl, steps, short=None, why=None, secs=None, stim=None,
      by=None):
    """Places the correct option at the next balanced key, checks the options and appends the record."""
    assert len(wrong) == 3, wrong
    assert diff in (B, I, A)
    assert why, f"why_others_wrong missing: {text[:60]}"
    n = len(QUESTIONS)
    key = KEYS[n]
    opts = list(wrong)
    opts.insert(LETTERS.index(key), ans)
    assert len({normalize(o) for o in opts}) == 4, f"options not distinct: {opts}"
    qid = f"BANK_QUANT_{_FIRST_ID + n:06d}"
    rec = {
        "question_id": qid,
        "exam_mappings": default_mappings(SUBJECT, diff),
        "subject": SUBJECT, "topic": topic, "subtopic": sub, "difficulty": diff,
        "question_type": "MCQ", "language": "en",
    }
    if stim:
        _set_pos[stim] = _set_pos.get(stim, 0) + 1
        rec |= {"stimulus_id": stim, "set_position": _set_pos[stim]}
    if secs is None:
        secs = {B: 40, I: 60, A: 100}[diff]
    verified_by = list(by or RECOMPUTE)
    if qid in INDEPENDENT:
        verified_by.append("ai:independent-check")
    rec |= {
        "question_text": text,
        "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(opts)],
        "correct_answer": key,
        "solution": {"concept": concept, "explanation": expl, "steps": steps, "shortcut": short,
                     "why_others_wrong": why, "final_answer": f"Option {key}: {ans}"},
        "suggested_time_seconds": secs,
        "source": {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                   "original_exam_year": None, "license_note": None},
        "verification": {"answer_verified": True, "solution_verified": True,
                         "review_status": "Pending Human Review",
                         "verified_by": verified_by, "verified_at": TODAY},
    }
    QUESTIONS.append(rec)


def stimulus(kind, title, content, chart_data=None):
    sid = f"STIM_QUANT_{_FIRST_STIM + len(STIMULI):06d}"
    s = {"stimulus_id": sid, "type": kind, "title": title, "content": content}
    if chart_data:
        s["chart_data"] = chart_data
    STIMULI.append(s)
    return sid


def md_table(header, rows, align=None):
    align = align or ["---"] + ["---:"] * (len(header) - 1)
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join(align) + "|"]
    lines += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(lines)


def nearest(exact, options, answer):
    """Approximation check: the answer is the option nearest the exact value, by a clear margin."""
    dist = sorted((abs(exact - o), o) for o in options)
    assert dist[0][1] == answer, (exact, dist)
    assert dist[1][0] >= 3 * dist[0][0] and dist[1][0] >= 1, (exact, dist)


APPROX = "What approximate value should come in place of the question mark (?)?\n"
QMARK = "What will come in place of the question mark (?)?\n"

# ================================================================ Simplification (B6 I2 A2)
T = "Simplification"
rhs = F(1008, 24) + 5 * 7
v = (rhs + 14 * 3) * 9
assert rhs == 77 and v == 1071 and (77 - 42) * 9 == 315 and 77 * 9 == 693 and (F(1008, 18) + 35 + 42) * 9 == 1197
Q(T, "BODMAS", B, QMARK + "? ÷ 9 − 14 × 3 = 1,008 ÷ 24 + 5 × 7",
  "1,071", ["315", "693", "1,197"],
  "Finish × and ÷ on both sides first, then undo the operations on ? in reverse order",
  "Right side: 1,008 ÷ 24 = 42 and 5 × 7 = 35, so it is 77. Left side: ? ÷ 9 − 42 = 77, so ? ÷ 9 = 119 and "
  "? = 119 × 9 = 1,071.",
  ["1,008 ÷ 24 + 5 × 7 = 42 + 35 = 77", "? ÷ 9 = 77 + 14 × 3 = 119", "? = 119 × 9 = 1,071"],
  why="315 subtracts 42 from 77 instead of adding it (35 × 9); 693 forgets the − 14 × 3 term (77 × 9); 1,197 divides "
      "1,008 by 18 instead of 24 (56 + 35 + 42 = 133, × 9).", secs=40)

v = F(7 * 68 - 18 ** 2, 640) * 100
assert v == F(95, 4) and F(476 + 324, 640) * 100 == 125 and F(476, 640) * 100 == F(595, 8)
Q(T, "BODMAS", B, QMARK + "?% of 640 + 18² = 7 × 68",
  "23.75", ["125", "74.375", "2.375"],
  "Evaluate the known terms, isolate the percentage term, then convert: ?% of 640 = ? × 6.4",
  "7 × 68 = 476 and 18² = 324, so ?% of 640 = 476 − 324 = 152. Then ? = 152 ÷ 6.4 = 23.75.",
  ["7 × 68 = 476", "18² = 324", "?% of 640 = 152", "? = 152 × 100 ÷ 640 = 23.75"],
  why="125 adds 324 instead of subtracting it (800 ÷ 6.4); 74.375 ignores the 18² term (476 ÷ 6.4); 2.375 divides by "
      "64 instead of 6.4.", secs=45)

v = F(11, 4) + F(23, 6) - F(13, 8)
assert v == F(119, 24) and F(11, 4) + F(23, 6) + F(13, 8) == F(197, 24)
assert F(11, 4) + F(23, 6) - 1 + F(5, 8) == F(149, 24) and v - 1 == F(95, 24)
Q(T, "Fractions and decimals", B, QMARK + "2¾ + 3⅚ − 1⅝ = ?",
  "4 23/24", ["8 5/24", "6 5/24", "3 23/24"],
  "Add and subtract the whole parts and the fractional parts separately, using the LCM 24 for the fractions",
  "Whole parts: 2 + 3 − 1 = 4. Fractions: 3/4 + 5/6 − 5/8 = 18/24 + 20/24 − 15/24 = 23/24. So the value is 4 23/24.",
  ["Wholes: 2 + 3 − 1 = 4", "3/4 = 18/24, 5/6 = 20/24, 5/8 = 15/24", "18 + 20 − 15 = 23 ⇒ 23/24", "Answer 4 23/24"],
  why="8 5/24 adds 1⅝ instead of subtracting it; 6 5/24 subtracts only the whole 1 and adds the ⅝; 3 23/24 subtracts 2 "
      "in the whole parts instead of 1.", secs=45)

v = F(36, 100) * F(5, 2) + F(48, 10) / F(12, 100) - F(19, 10)
assert v == 39 and F(9, 10) + 4 - F(19, 10) == 3 and F(9, 10) + 400 - F(19, 10) == 399 and F(9, 10) + 40 + F(19, 10) == F(428, 10)
Q(T, "Fractions and decimals", B, QMARK + "0.36 × 2.5 + 4.8 ÷ 0.12 − 1.9 = ?",
  "39", ["3", "399", "42.8"],
  "Do × and ÷ before + and −; to divide by a decimal, multiply both numbers by a power of 10",
  "0.36 × 2.5 = 0.9 and 4.8 ÷ 0.12 = 480 ÷ 12 = 40. So the value is 0.9 + 40 − 1.9 = 39.",
  ["0.36 × 2.5 = 0.9", "4.8 ÷ 0.12 = 480 ÷ 12 = 40", "0.9 + 40 − 1.9 = 39"],
  why="3 takes 4.8 ÷ 0.12 as 4 (dividing by 1.2); 399 takes it as 400 (dividing by 0.012); 42.8 adds the 1.9 instead "
      "of subtracting it.", secs=40)

roots = [F(13, 100), F(13, 10), F(13)]
assert all(r * r == x for r, x in zip(roots, [F(169, 10000), F(169, 100), F(169)]))
assert sum(roots) == F(1443, 100) and F(13, 10) * 2 + 13 == F(156, 10) and F(13, 100) * 2 + 13 == F(1326, 100)
Q(T, "Square and cube roots", B, QMARK + "√0.0169 + √1.69 + √169 = ?",
  "14.43", ["15.6", "13.26", "1.443"],
  "The square root of a decimal has half as many decimal places: √0.0169 = 0.13, √1.69 = 1.3",
  "√0.0169 = 0.13 (four decimal places become two), √1.69 = 1.3 and √169 = 13. Sum = 0.13 + 1.3 + 13 = 14.43.",
  ["√0.0169 = 0.13", "√1.69 = 1.3", "√169 = 13", "0.13 + 1.3 + 13 = 14.43"],
  why="15.6 takes √0.0169 as 1.3; 13.26 takes √1.69 as 0.13; 1.443 misplaces the decimal point in the sum.", secs=40)

# (√12 + √27 − √48)² with √12 = 2√3, √27 = 3√3, √48 = 4√3
assert (2 + 3 - 4) ** 2 * 3 == 3 and (2 + 3 - 3) ** 2 * 3 == 12 and (2 + 3 - 2) ** 2 * 3 == 27 and (2 + 3 + 4) ** 2 * 3 == 243
assert 12 == 4 * 3 and 27 == 9 * 3 and 48 == 16 * 3
Q(T, "Surds and indices", B, QMARK + "(√12 + √27 − √48)² = ?",
  "3", ["12", "27", "243"],
  "Write each surd as a multiple of the same surd (here √3) before adding or subtracting",
  "√12 = 2√3, √27 = 3√3 and √48 = 4√3. So the bracket is (2 + 3 − 4)√3 = √3, and (√3)² = 3.",
  ["√12 = 2√3", "√27 = 3√3", "√48 = 4√3", "2√3 + 3√3 − 4√3 = √3", "(√3)² = 3"],
  why="12 takes √48 as 3√3, leaving 2√3; 27 takes √48 as 2√3, leaving 3√3; 243 adds √48 instead of subtracting it "
      "(9√3, squared).", secs=45)

a_, b_ = F(275, 100), F(125, 100)
v = a_ * a_ + 2 * a_ * b_ + b_ * b_
assert v == 16 == (a_ + b_) ** 2 and a_ * a_ + b_ * b_ == F(9125, 1000) and (a_ - b_) ** 2 == F(9, 4)
Q(T, "Fractions and decimals", I, "Find the value of 2.75 × 2.75 + 2 × 2.75 × 1.25 + 1.25 × 1.25.",
  "16", ["9.125", "4", "2.25"],
  "Recognise the identity a² + 2ab + b² = (a + b)²",
  "With a = 2.75 and b = 1.25 the expression is (a + b)² = (2.75 + 1.25)² = 4² = 16.",
  ["a = 2.75, b = 1.25", "a² + 2ab + b² = (a + b)²", "(2.75 + 1.25)² = 4² = 16"],
  short="Spot the pattern a² + 2ab + b² instead of multiplying the decimals out.",
  why="9.125 adds only the two squares and drops the 2ab term; 4 forgets to square a + b; 2.25 uses (a − b)² = 1.5².",
  secs=50)

v = F(2 ** 10 - 2 ** 8, 2 ** 7 + 2 ** 6)
assert v == 4 and F(2 ** 10 - 2 ** 8, 2 ** 7) == 6 and F(2 ** 10 - 2 ** 8, 2 ** 6) == 12 and F(2 ** 2, 2 ** 1) == 2
Q(T, "Surds and indices", I, "What is the value of (2¹⁰ − 2⁸) ÷ (2⁷ + 2⁶)?",
  "4", ["6", "12", "2"],
  "Take the smallest power out as a common factor in the numerator and in the denominator",
  "Numerator: 2⁸(2² − 1) = 2⁸ × 3. Denominator: 2⁶(2 + 1) = 2⁶ × 3. So the value is 2⁸ ÷ 2⁶ = 2² = 4.",
  ["2¹⁰ − 2⁸ = 2⁸ × 3 = 768", "2⁷ + 2⁶ = 2⁶ × 3 = 192", "768 ÷ 192 = 4"],
  why="6 divides 768 by 2⁷ alone; 12 divides it by 2⁶ alone; 2 subtracts the exponents inside each bracket "
      "(2¹⁰⁻⁸ ÷ 2⁷⁻⁶), which is not allowed for a sum or difference.", secs=55)

x_ = F(5, 2)
assert near(4 ** float(x_) - 4 ** float(x_ - 1), 24) and near((2 * float(x_)) ** float(x_), 25 * math.sqrt(5))
assert near(4 ** 2 - 4 ** 1, 12) and 2 * x_ - 2 == 3 and (2 * 3) ** 3 == 216 and near(3 ** 1.5, 3 * math.sqrt(3))
Q(T, "Surds and indices", A, "If 4ˣ − 4ˣ⁻¹ = 24, what is the value of (2x)ˣ?",
  "25√5", ["216", "25", "3√3"],
  "Take the smaller power out as a factor: 4ˣ − 4ˣ⁻¹ = 4ˣ⁻¹(4 − 1); then write both sides as powers of 2",
  "4ˣ⁻¹ × 3 = 24, so 4ˣ⁻¹ = 8, i.e. 2^(2x − 2) = 2³. Hence 2x − 2 = 3 and x = 2.5. Then (2x)ˣ = 5^2.5 = 5² × √5 = "
  "25√5.",
  ["4ˣ⁻¹(4 − 1) = 24 ⇒ 4ˣ⁻¹ = 8", "2^(2x − 2) = 2³ ⇒ x = 5/2", "(2x)ˣ = 5^(5/2) = 25√5"],
  why="216 rounds the solution to x = 3 (6³); 25 drops the half power and takes 5²; 3√3 solves 2x = 3 (forgetting "
      "the − 2), so x = 1.5 and 3^1.5 = 3√3.", secs=95)

vals_ = [F(4, 9), F(25, 9), F(1, 9)]
assert [F(4, 10) + F(4, 90), F(2) + F(7, 9), F(1, 9)] == vals_
v = F(2, 3) + F(5, 3) + F(1, 3)
assert v == F(8, 3) and sum(vals_) == F(10, 3) and F(2, 3) + F(4, 3) + F(1, 3) == F(7, 3) and F(2 + 5 + 1, 9) == F(8, 9)
Q(T, "Square and cube roots", A,
  "Find the value of √0.444… + √2.777… + √0.111…, where each decimal has its last digit recurring.",
  "2⅔", ["3⅓", "2⅓", "8/9"],
  "Convert each recurring decimal to a fraction with denominator 9 (0.ddd… = d/9), then take square roots",
  "0.444… = 4/9, 2.777… = 2 + 7/9 = 25/9 and 0.111… = 1/9. Their square roots are 2/3, 5/3 and 1/3, whose sum is "
  "8/3 = 2⅔.",
  ["0.444… = 4/9 ⇒ √ = 2/3", "2.777… = 25/9 ⇒ √ = 5/3", "0.111… = 1/9 ⇒ √ = 1/3", "2/3 + 5/3 + 1/3 = 8/3 = 2⅔"],
  why="3⅓ adds the fractions 4/9 + 25/9 + 1/9 and forgets the square roots; 2⅓ converts 2.777… as 1 + 7/9 = 16/9 "
      "(root 4/3); 8/9 takes the roots of the numerators but forgets that √9 = 3 in the denominator.", secs=85)

# ================================================================ Approximation (B2 I4 A2)
T = "Approximation"
exact = 0.3748 * 1600.3 + 0.8752 * 799.8
nearest(exact, [1300, 1200, 1100, 1700], 1300)
assert F(3, 8) * 1600 == 600 and F(7, 8) * 800 == 700 and F(3, 4) * 800 == 600 and F(5, 8) * 1600 == 1000
Q(T, "Percentage approximation", B, APPROX + "37.48% of 1600.3 + 87.52% of 799.8 ≈ ?",
  "1300", ["1200", "1100", "1700"],
  "Use fraction equivalents: 37.5% = 3/8 and 87.5% = 7/8",
  "37.5% of 1600 = 3/8 × 1600 = 600 and 87.5% of 800 = 7/8 × 800 = 700, so the value ≈ 1300.",
  ["37.5% = 3/8 ⇒ 600", "87.5% = 7/8 ⇒ 700", "600 + 700 = 1300"],
  why="1200 takes 87.5% as 75% (600 + 600); 1100 takes 37.5% as 25% (400 + 700); 1700 takes 37.5% as 5/8 "
      "(1000 + 700).", secs=35)

exact = 4912.7 ** (1 / 3) * 5.97 + math.sqrt(728.6)
nearest(exact, [129, 102, 75, 139], 129)
assert 17 ** 3 == 4913 and 27 ** 2 == 729
Q(T, "Root approximation", B, APPROX + "∛4912.7 × 5.97 + √728.6 ≈ ?",
  "129", ["102", "75", "139"],
  "Round to the nearest perfect cube and square: 4913 = 17³ and 729 = 27²",
  "∛4912.7 ≈ 17 and √728.6 ≈ 27, so the value ≈ 17 × 6 + 27 = 102 + 27 = 129.",
  ["∛4913 = 17", "17 × 6 = 102", "√729 = 27", "102 + 27 = 129"],
  why="102 stops before adding √728.6; 75 subtracts the 27 instead of adding it; 139 is 10 away from the exact value "
      "(about 128.5).", secs=40)

exact = (16.98 ** 2 - 0.3496 * 140.2) / 1599.7 * 100
nearest(exact, [15, 21, 18, 9], 15)
assert 17 ** 2 - F(35, 100) * 140 == 240 and F(240, 1600) * 100 == 15
Q(T, "Percentage approximation", I, APPROX + "?% of 1599.7 ≈ 16.98² − 34.96% of 140.2",
  "15", ["21", "18", "9"],
  "Round, finish the right side, then ?% of 1600 = 16 × ?",
  "17² = 289 and 35% of 140 = 49, so the right side ≈ 240. Then ?% of 1600 = 240 gives ? = 240 ÷ 16 = 15.",
  ["17² = 289", "35% of 140 = 49", "289 − 49 = 240", "? = 240 ÷ 16 = 15"],
  why="21 adds 49 instead of subtracting it (338 ÷ 16 ≈ 21); 18 ignores the 35% term (289 ÷ 16 ≈ 18); 9 is 6 away "
      "from the exact value (about 15.0).", secs=50)

exact = math.sqrt(5183.9) * 0.3429 ** (1 / 3)
nearest(exact, [50.4, 5.04, 504, 64.8], 50.4)
assert 72 ** 2 == 5184 and F(7, 10) ** 3 == F(343, 1000) and 72 * F(9, 10) == F(648, 10)
Q(T, "Root approximation", I, APPROX + "√5183.9 × ∛0.3429 ≈ ?",
  "50.4", ["5.04", "504", "64.8"],
  "5184 = 72²; the cube root of a decimal with three decimal places has one: ∛0.343 = 0.7",
  "√5183.9 ≈ 72 and ∛0.3429 ≈ ∛0.343 = 0.7, so the value ≈ 72 × 0.7 = 50.4.",
  ["√5184 = 72", "∛0.343 = 0.7", "72 × 0.7 = 50.4"],
  why="5.04 takes ∛0.343 as 0.07; 504 takes it as 7; 64.8 takes it as 0.9.", secs=50)

exact = (8.97 * 13.02 + 2.99 * 13.01) / 5.98
nearest(exact, [26, 156, 13, 20], 26)
assert F(13 * (9 + 3), 6) == 26 and 13 * 12 == 156 and F(9 * 13 + 3, 6) == 20
Q(T, "Mixed approximation", I, APPROX + "(8.97 × 13.02 + 2.99 × 13.01) ÷ 5.98 ≈ ?",
  "26", ["156", "13", "20"],
  "Round, then take the common factor 13 out of the bracket",
  "The bracket ≈ 9 × 13 + 3 × 13 = 13 × 12 = 156, and 156 ÷ 6 = 26.",
  ["9 × 13 + 3 × 13 = 13 × 12 = 156", "156 ÷ 6 = 26"],
  why="156 forgets to divide by 5.98; 13 divides by 12 instead of 6; 20 multiplies only the first 9 by 13 "
      "((117 + 3) ÷ 6).", secs=45)

exact = (61.97 - 1 / 0.0499) / 0.4998
nearest(exact, [84, 21, 164, 120], 84)
assert (62 - 20) / F(1, 2) == 84 and (62 + 20) * 2 == 164 and (62 - 2) * 2 == 120 and (62 - 20) * F(1, 2) == 21
Q(T, "Mixed approximation", I, APPROX + "0.4998 × ? + 1/0.0499 ≈ 61.97",
  "84", ["21", "164", "120"],
  "1/0.05 = 20; then undo the + and the × in reverse order",
  "1/0.0499 ≈ 1/0.05 = 20. So 0.5 × ? ≈ 62 − 20 = 42 and ? ≈ 42 ÷ 0.5 = 84.",
  ["1/0.05 = 20", "0.5 × ? = 62 − 20 = 42", "? = 42 ÷ 0.5 = 84"],
  why="21 multiplies 42 by 0.5 instead of dividing; 164 adds 20 instead of subtracting it; 120 takes 1/0.05 as 2.",
  secs=50)

exact = (27.03 * 3.99 - math.sqrt(1023.6)) * 6.02 - 0.1498 * 239.9
nearest(exact, [420, 492, 456, 612], 420)
assert (108 - 32) * 6 - 36 == 420 and (108 - 32) * 6 + 36 == 492 and (108 - 32) * 6 == 456 and 108 * 6 - 36 == 612
Q(T, "Mixed approximation", A, APPROX + "(? + 14.98% of 239.9) ÷ 6.02 ≈ 27.03 × 3.99 − √1023.6",
  "420", ["492", "456", "612"],
  "Finish the right side, multiply back by 6, then remove the known part of the bracket",
  "Right side ≈ 27 × 4 − √1024 = 108 − 32 = 76. So the bracket ≈ 76 × 6 = 456. 15% of 240 = 36, so ? ≈ 456 − 36 = "
  "420.",
  ["27 × 4 = 108", "√1024 = 32", "108 − 32 = 76", "76 × 6 = 456", "15% of 240 = 36", "? = 456 − 36 = 420"],
  why="492 adds 36 instead of subtracting it; 456 is the value of the whole bracket, not of ?; 612 forgets the √1024 "
      "term (108 × 6 − 36).", secs=90)

exact = math.sqrt(24.02 ** 2 + 3.98 ** 2 - math.sqrt(4095.7) * 2.99)
nearest(exact, [20, 24, 28, 400], 20)
assert 24 ** 2 + 4 ** 2 - 64 * 3 == 400 == 20 ** 2 and 24 ** 2 + 4 ** 2 + 64 * 3 == 28 ** 2
Q(T, "Root approximation", A, APPROX + "?² + √4095.7 × 2.99 ≈ 24.02² + 3.98² (? is positive)",
  "20", ["24", "28", "400"],
  "Round each term, isolate ?², then take the positive square root",
  "24² + 4² = 576 + 16 = 592 and √4096 × 3 = 64 × 3 = 192. So ?² ≈ 592 − 192 = 400 and ? ≈ 20.",
  ["24² + 4² = 592", "√4096 = 64 ⇒ 64 × 3 = 192", "?² = 592 − 192 = 400", "? = 20"],
  why="24 keeps only the 24.02² term; 28 adds 192 instead of subtracting it (√784); 400 is ?², not ?.", secs=85)

# ================================================================ Number Series (B4 I7 A4)
T = "Number Series"
SERIES_Q = "What will come in place of the question mark (?) in the following series?\n"
MISSING_Q = "Find the missing number (?) in the series:\n"


def series_from(start, step, n):
    out = [start]
    for k in range(1, n):
        out.append(step(out[-1], k))
    return out


def diffs(seq):
    return [b - a for a, b in zip(seq, seq[1:])]


def series_text(seq):
    return ", ".join(N(x) for x in seq)


s = series_from(50, lambda t, k: t + (11 if k % 2 else -3), 6)
assert s == [50, 61, 58, 69, 66, 77] and 66 - 3 == 63 and 66 + 8 == 74 and 66 + 22 == 88
Q(T, "Pattern: differences", B, SERIES_Q + "50, 61, 58, 69, 66, ?",
  "77", ["63", "74", "88"],
  "The steps alternate: + 11, − 3, + 11, − 3, …",
  "50 + 11 = 61, 61 − 3 = 58, 58 + 11 = 69, 69 − 3 = 66. The next step is + 11, so the term is 77.",
  ["+11, −3, +11, −3", "Next step: +11", "66 + 11 = 77"],
  why="63 applies − 3 again instead of + 11; 74 adds the net change of a pair of steps (+ 8); 88 adds 11 twice.",
  secs=30)

s = [4, 7]
while len(s) < 7:
    s.append(s[-1] + s[-2])
assert s == [4, 7, 11, 18, 29, 47, 76] and 18 + 7 != 29 and all(x + 18 != 47 for x in (25, 36, 22))
Q(T, "Missing number series", B, MISSING_Q + "4, 7, 11, 18, ?, 47, 76",
  "29", ["25", "36", "22"],
  "Each term is the sum of the two terms before it",
  "4 + 7 = 11, 7 + 11 = 18, 11 + 18 = 29, 18 + 29 = 47 and 29 + 47 = 76.",
  ["4 + 7 = 11", "7 + 11 = 18", "11 + 18 = 29", "18 + 29 = 47 ✓", "29 + 47 = 76 ✓"],
  why="25 repeats the difference 7; 36 doubles 18; 22 adds the first difference 4 again. None of them gives 47 at the "
      "next step (18 + 25 = 43, 18 + 36 = 54, 18 + 22 = 40).", secs=35)

s = series_from(F(81), lambda t, k: t / 3 if k % 2 else t * 2, 7)
assert s == [81, 27, 54, 18, 36, 12, 24]
Q(T, "Pattern: multiply-add", B, SERIES_Q + "81, 27, 54, 18, 36, 12, ?",
  "24", ["4", "36", "6"],
  "The operations alternate: ÷ 3, × 2, ÷ 3, × 2, …",
  "81 ÷ 3 = 27, 27 × 2 = 54, 54 ÷ 3 = 18, 18 × 2 = 36, 36 ÷ 3 = 12. The next operation is × 2, so the term is 24.",
  ["÷3, ×2 alternately", "12 × 2 = 24"],
  why="4 divides by 3 again; 36 repeats the previous high term; 6 halves 12 instead of doubling it.", secs=30)

s = list(itertools.accumulate([100, 32, 16, 8, 4, 2]))
assert s == [100, 132, 148, 156, 160, 162]
Q(T, "Pattern: differences", B, SERIES_Q + "100, 132, 148, 156, 160, ?",
  "162", ["164", "161", "158"],
  "The differences halve each time: 32, 16, 8, 4, …",
  "The differences are 32, 16, 8, 4, so the next difference is 2 and the term is 160 + 2 = 162.",
  ["Differences: 32, 16, 8, 4", "Next difference: 2", "160 + 2 = 162"],
  why="164 adds 4 again; 161 halves twice and adds 1; 158 subtracts 2 instead of adding it.", secs=35)

s = list(itertools.accumulate([3] + [(2 * k - 1) ** 2 for k in range(1, 6)]))
assert s == [3, 4, 13, 38, 87, 168] and 87 + 64 == 151 and 87 + 49 == 136 and 87 + 100 == 187
Q(T, "Pattern: squares and cubes", I, SERIES_Q + "3, 4, 13, 38, 87, ?",
  "168", ["151", "136", "187"],
  "The differences are the squares of odd numbers: 1², 3², 5², 7², …",
  "The differences are 1, 9, 25, 49 = 1², 3², 5², 7². The next is 9² = 81, so the term is 87 + 81 = 168.",
  ["Differences: 1, 9, 25, 49", "= 1², 3², 5², 7²", "Next: 9² = 81", "87 + 81 = 168"],
  why="151 adds 8², an even square; 136 adds 7² again; 187 adds 10², skipping 9².", secs=50)

s = [(2 * n - 1) * (2 * n + 1) for n in range(1, 7)]
assert s == [3, 15, 35, 63, 99, 143] and 35 + 20 == 55 and 8 ** 2 == 64 and 7 ** 2 - 1 == 48
Q(T, "Missing number series", I, MISSING_Q + "3, 15, 35, ?, 99, 143",
  "63", ["55", "64", "48"],
  "Each term is the product of two consecutive odd numbers: 1 × 3, 3 × 5, 5 × 7, …",
  "3 = 1 × 3, 15 = 3 × 5, 35 = 5 × 7, so the missing term is 7 × 9 = 63; then 9 × 11 = 99 and 11 × 13 = 143. "
  "(Equivalently each term is one less than an even square: 4 − 1, 16 − 1, 36 − 1, 64 − 1, …)",
  ["1 × 3, 3 × 5, 5 × 7", "7 × 9 = 63", "9 × 11 = 99 ✓, 11 × 13 = 143 ✓"],
  short="Differences 12, 20, 28, 36, 44 rise by 8: 35 + 28 = 63.",
  why="55 adds 20 again; 64 is 8² and forgets the − 1; 48 is 7² − 1, the pattern applied to an odd base.", secs=50)

s = [n * n + (1 if n % 2 else -1) for n in range(1, 8)]
assert s == [2, 3, 10, 15, 26, 35, 50] and diffs(s) == [1, 7, 5, 11, 9, 15]
Q(T, "Pattern: squares and cubes", I, SERIES_Q + "2, 3, 10, 15, 26, 35, ?",
  "50", ["48", "49", "44"],
  "Odd positions are n² + 1 and even positions are n² − 1",
  "2 = 1² + 1, 3 = 2² − 1, 10 = 3² + 1, 15 = 4² − 1, 26 = 5² + 1, 35 = 6² − 1. The 7th term is 7² + 1 = 50.",
  ["1² + 1, 2² − 1, 3² + 1, 4² − 1, 5² + 1, 6² − 1", "7th term: 7² + 1 = 50"],
  short="Differences 1, 7, 5, 11, 9 alternate between two series rising by 4: the next difference is 15.",
  why="48 uses 7² − 1, the even-position rule; 49 forgets the ± 1 altogether; 44 adds 9 again.", secs=55)

s = series_from(F(256), lambda t, k: t * F(5, 4), 6)
assert s == [256, 320, 400, 500, 625, F(3125, 4)] and 625 + 125 == 750 and 625 * F(13, 10) == F(1625, 2)
Q(T, "Pattern: multiply-add", I, SERIES_Q + "256, 320, 400, 500, 625, ?",
  "781.25", ["750", "812.5", "1,250"],
  "Each term = previous term × 1.25 (= 5/4)",
  "256 × 1.25 = 320, 320 × 1.25 = 400, 400 × 1.25 = 500, 500 × 1.25 = 625, so the next term is 625 × 1.25 = 781.25.",
  ["320/256 = 400/320 = … = 1.25", "625 × 1.25 = 781.25"],
  why="750 adds the last difference 125 again; 812.5 multiplies by 1.3; 1,250 doubles 625.", secs=45)

s = [1, 2]
while len(s) < 7:
    s.append(s[-1] * s[-2])
assert s == [1, 2, 2, 4, 8, 32, 256]
Q(T, "Pattern: multiply-add", I, SERIES_Q + "1, 2, 2, 4, 8, 32, ?",
  "256", ["64", "128", "1,024"],
  "Each term is the product of the two terms before it",
  "1 × 2 = 2, 2 × 2 = 4, 2 × 4 = 8, 4 × 8 = 32, so the next term is 8 × 32 = 256.",
  ["1 × 2 = 2", "2 × 2 = 4", "2 × 4 = 8", "4 × 8 = 32", "8 × 32 = 256"],
  why="64 only doubles 32; 128 multiplies 32 by 4 instead of 8; 1,024 squares 32.", secs=45)

s = list(itertools.accumulate([5] + [(-2) ** k for k in range(6)]))
assert s == [5, 6, 4, 8, 0, 16, -16] and 16 + 32 == 48 and 16 - 64 == -48
Q(T, "Pattern: differences", I, SERIES_Q + "5, 6, 4, 8, 0, 16, ?",
  "−16", ["48", "0", "−48"],
  "The differences are +1, −2, +4, −8, +16: they double in size and alternate in sign",
  "Differences: +1, −2, +4, −8, +16. The next difference is −32, so the term is 16 − 32 = −16.",
  ["Differences: +1, −2, +4, −8, +16", "Next difference: −32", "16 − 32 = −16"],
  why="48 adds 32 and ignores the alternating sign; 0 subtracts 16, repeating the size of the last step; −48 doubles "
      "the step twice (− 64).", secs=55)

pr = [2, 3, 5, 7, 11, 13]
s = [p * p + 1 for p in pr]
assert s == [5, 10, 26, 50, 122, 170] and 12 ** 2 + 1 == 145 and 17 ** 2 + 1 == 290 and 15 ** 2 + 1 == 226
Q(T, "Pattern: squares and cubes", I, SERIES_Q + "5, 10, 26, 50, 122, ?",
  "170", ["145", "290", "226"],
  "Each term is (a prime number)² + 1, taking the primes in order: 2, 3, 5, 7, 11, …",
  "5 = 2² + 1, 10 = 3² + 1, 26 = 5² + 1, 50 = 7² + 1, 122 = 11² + 1. The next prime is 13, so the term is "
  "13² + 1 = 170.",
  ["2² + 1, 3² + 1, 5² + 1, 7² + 1, 11² + 1", "Next prime: 13", "13² + 1 = 170"],
  why="145 uses 12, which is not prime; 290 uses 17 and skips 13; 226 uses 15, which is not prime.", secs=55)

fib = [2, 3]
while len(fib) < 7:
    fib.append(fib[-1] + fib[-2])
s = [f * f for f in fib]
assert fib == [2, 3, 5, 8, 13, 21, 34] and s[:6] == [4, 9, 25, 64, 169, 441]
Q(T, "Pattern: squares and cubes", A, SERIES_Q + "4, 9, 25, 64, 169, ?",
  "441", ["289", "324", "338"],
  "Take square roots: 2, 3, 5, 8, 13 — each is the sum of the two before it",
  "√ of the terms: 2, 3, 5, 8, 13. Each is the sum of the previous two (2 + 3 = 5, 3 + 5 = 8, 5 + 8 = 13), so the next "
  "root is 8 + 13 = 21 and the term is 21² = 441.",
  ["Roots: 2, 3, 5, 8, 13", "Rule: add the two previous roots", "8 + 13 = 21", "21² = 441"],
  why="289 = 17² takes the roots as primes (2, 3, 5, … but 8 is not prime); 324 = 18² adds 5 to 13, repeating an "
      "earlier gap; 338 doubles 169.", secs=75)

s = [1]
for n in range(2, 7):
    s.append(2 * s[-1] + (n - 1) ** 2)
assert s == [1, 3, 10, 29, 74, 173] and 2 * 74 + 16 == 164 and 2 * 74 == 148 and 3 * 74 + 1 == 223
Q(T, "Pattern: multiply-add", A, SERIES_Q + "1, 3, 10, 29, 74, ?",
  "173", ["164", "148", "223"],
  "Each term = previous term × 2 + a perfect square, the squares rising 1², 2², 3², …",
  "1 × 2 + 1 = 3, 3 × 2 + 4 = 10, 10 × 2 + 9 = 29, 29 × 2 + 16 = 74, so the next term is 74 × 2 + 25 = 173.",
  ["×2 + 1", "×2 + 4", "×2 + 9", "×2 + 16", "74 × 2 + 25 = 173"],
  why="164 adds 16 again; 148 only doubles; 223 uses × 3 + 1, which fits only the step 3 → 10.", secs=80)

s = [p * p - 2 for p in [2, 3, 5, 7, 11, 13, 17]]
assert s == [2, 7, 23, 47, 119, 167, 287] and 15 ** 2 - 2 == 223 and 16 ** 2 - 2 == 254 and 19 ** 2 - 2 == 359
Q(T, "Pattern: squares and cubes", A, SERIES_Q + "2, 7, 23, 47, 119, 167, ?",
  "287", ["223", "254", "359"],
  "Add 2 to each term: 4, 9, 25, 49, 121, 169 are the squares of consecutive primes",
  "Each term is p² − 2 for the primes p = 2, 3, 5, 7, 11, 13. The next prime is 17, so the term is 17² − 2 = 287.",
  ["Terms + 2: 4, 9, 25, 49, 121, 169", "= 2², 3², 5², 7², 11², 13²", "Next prime 17: 289 − 2 = 287"],
  why="223 uses 15 and 254 uses 16, neither of which is prime; 359 uses 19 and skips 17.", secs=80)

s = series_from(2, lambda t, k: t * t - 1, 5)
assert s == [2, 3, 8, 63, 3968] and 48 ** 2 - 1 != 3968 and 65 ** 2 - 1 != 3968 and 24 ** 2 - 1 != 3968
Q(T, "Missing number series", A, MISSING_Q + "2, 3, 8, ?, 3968",
  "63", ["48", "65", "24"],
  "Each term = (previous term)² − 1",
  "2² − 1 = 3, 3² − 1 = 8, 8² − 1 = 63 and 63² − 1 = 3969 − 1 = 3968, which confirms 63.",
  ["2² − 1 = 3", "3² − 1 = 8", "8² − 1 = 63", "63² − 1 = 3968 ✓"],
  why="48 multiplies 8 by 6; 65 uses 8² + 1; 24 multiplies 8 by 3. None of them gives 3968 at the next step "
      "(48² − 1 = 2303, 65² − 1 = 4224, 24² − 1 = 575).", secs=75)

# ================================================================ Wrong Number Series (B2 I2 A1)
T = "Wrong Number Series"


def wrong_series(correct, shown):
    diff = [i for i, (a, b) in enumerate(zip(correct, shown)) if a != b]
    assert len(diff) == 1, (correct, shown)
    return shown[diff[0]], correct[diff[0]]


WRONG_Q = "Find the wrong number in the series:\n"
good = [(2 * n - 1) ** 2 for n in range(1, 8)]
shown = [1, 9, 25, 48, 81, 121, 169]
assert good == [1, 9, 25, 49, 81, 121, 169] and wrong_series(good, shown) == (48, 49)
Q(T, "Find the wrong term", B, WRONG_Q + series_text(shown),
  "48", ["81", "121", "25"],
  "The terms are the squares of the odd numbers 1, 3, 5, 7, …",
  "1², 3², 5², 7², 9², 11², 13² = 1, 9, 25, 49, 81, 121, 169. The fourth term should be 49, not 48.",
  ["1, 9, 25 = 1², 3², 5²", "7² = 49 ≠ 48", "81, 121, 169 = 9², 11², 13²"],
  why="81, 121 and 25 are 9², 11² and 5² and fit the pattern.", secs=30)

good = series_from(5, lambda t, k: t * 2 if k % 2 else t - 3, 7)
shown = [5, 10, 7, 14, 12, 22, 19]
assert good == [5, 10, 7, 14, 11, 22, 19] and wrong_series(good, shown) == (12, 11) and 12 * 2 != 22
Q(T, "Find the wrong term", B, WRONG_Q + series_text(shown),
  "12", ["7", "22", "19"],
  "The operations alternate: × 2, − 3, × 2, − 3, …",
  "5 × 2 = 10, 10 − 3 = 7, 7 × 2 = 14, 14 − 3 = 11, 11 × 2 = 22, 22 − 3 = 19. The fifth term should be 11, not 12.",
  ["5 × 2 = 10", "10 − 3 = 7", "7 × 2 = 14", "14 − 3 = 11 ≠ 12", "11 × 2 = 22", "22 − 3 = 19"],
  why="7, 22 and 19 all fit; 22 looks wrong only if 12 is taken as correct (12 × 2 = 24).", secs=40)

good = series_from(F(2), lambda t, k: t * 3 if k % 2 else t / 2, 7)
shown = [F(2), F(6), F(3), F(9), F(9, 2), F(25, 2), F(27, 4)]
assert good == [2, 6, 3, 9, F(9, 2), F(27, 2), F(27, 4)] and wrong_series(good, shown) == (F(25, 2), F(27, 2))
Q(T, "Find the wrong term", I, WRONG_Q + series_text(shown),
  "12.5", ["4.5", "9", "6.75"],
  "The operations alternate: × 3, ÷ 2, × 3, ÷ 2, …",
  "2 × 3 = 6, 6 ÷ 2 = 3, 3 × 3 = 9, 9 ÷ 2 = 4.5, 4.5 × 3 = 13.5, 13.5 ÷ 2 = 6.75. The sixth term should be 13.5, not "
  "12.5.",
  ["×3: 2 → 6, 3 → 9, 4.5 → 13.5", "÷2: 6 → 3, 9 → 4.5, 13.5 → 6.75", "Shown 12.5 ≠ 13.5"],
  why="4.5, 9 and 6.75 fit the rule; 6.75 confirms 13.5, since 12.5 ÷ 2 would be 6.25.", secs=50)

good = list(itertools.accumulate([3] + [math.factorial(k) for k in range(1, 7)]))
shown = [3, 4, 6, 12, 36, 154, 876]
assert good == [3, 4, 6, 12, 36, 156, 876] and wrong_series(good, shown) == (154, 156)
Q(T, "Find the wrong term", I, WRONG_Q + series_text(shown),
  "154", ["36", "12", "876"],
  "The differences are factorials: 1!, 2!, 3!, 4!, 5!, 6! = 1, 2, 6, 24, 120, 720",
  "3 + 1 = 4, 4 + 2 = 6, 6 + 6 = 12, 12 + 24 = 36, 36 + 120 = 156, 156 + 720 = 876. The sixth term should be 156, "
  "not 154.",
  ["+1, +2, +6, +24 fit", "36 + 120 = 156 ≠ 154", "156 + 720 = 876 ✓"],
  why="36, 12 and 876 fit; 876 confirms 156, since 154 + 720 = 874.", secs=60)

good = list(itertools.accumulate([1] + [p * p for p in [2, 3, 5, 7, 11, 13]]))
shown = [1, 5, 14, 39, 89, 209, 378]
assert good == [1, 5, 14, 39, 88, 209, 378] and wrong_series(good, shown) == (89, 88)
Q(T, "Find the wrong term", A, WRONG_Q + series_text(shown),
  "89", ["39", "209", "378"],
  "The differences are the squares of consecutive primes: 2², 3², 5², 7², 11², 13²",
  "1 + 4 = 5, 5 + 9 = 14, 14 + 25 = 39, 39 + 49 = 88, 88 + 121 = 209, 209 + 169 = 378. The fifth term should be 88, "
  "not 89.",
  ["Differences shown: 4, 9, 25, 50, 120, 169", "Expected: 4, 9, 25, 49, 121, 169", "39 + 49 = 88 ≠ 89",
   "88 + 121 = 209 ✓"],
  why="39, 209 and 378 fit; the shown differences 50 and 120 both point to the single term 89, which should be 88.",
  secs=80)

# ================================================================ Quadratic Equations (B4 I3 A3)
T = "Quadratic Equations"
REL = {">": "x > y", ">=": "x ≥ y", "<": "x < y", "<=": "x ≤ y",
       "cbe": "x = y or the relationship cannot be established"}
_TESTS = {">": lambda x, y: x > y, "<": lambda x, y: x < y, ">=": lambda x, y: x >= y, "<=": lambda x, y: x <= y}


def relation(xs, ys):
    pairs = [(x, y) for x in xs for y in ys]
    if all(x == y for x, y in pairs):
        return "cbe"
    for sym in (">", "<", ">=", "<="):
        if all(_TESTS[sym](x, y) for x, y in pairs):
            return sym
    return "cbe"


def no_true_distractor(xs, ys, syms):
    """No wrong relation may hold for every pair (e.g. x ≥ y when the answer is x > y, or when x = y)."""
    for s_ in syms:
        assert not all(_TESTS[s_](x, y) for x in xs for y in ys), f"distractor {s_} is also true"


def roots_check(a, b, c, roots):
    for r in roots:
        assert a * r * r + b * r + c == 0, (a, b, c, r)


def qe(sub, diff, pre, eq1, eq2, xs, ys, expect, wrong_syms, concept, expl, steps, short=None, why=None, secs=None):
    got = relation(xs, ys)
    assert got == expect, (eq1, eq2, got)
    assert "cbe" not in wrong_syms and expect not in wrong_syms and len(set(wrong_syms)) == 2
    if expect == "cbe":
        third = next(s_ for s_ in ("<", ">", "<=", ">=") if s_ not in wrong_syms)
        wrong = [REL[wrong_syms[0]], REL[wrong_syms[1]], REL[third]]
        no_true_distractor(xs, ys, [*wrong_syms, third])
    else:
        wrong = [REL[wrong_syms[0]], REL["cbe"], REL[wrong_syms[1]]]
        no_true_distractor(xs, ys, wrong_syms)
    Q(T, sub, diff, f"{pre}\nI. {eq1}\nII. {eq2}", REL[expect], wrong, concept, expl, steps, short, why, secs)


xs, ys = [F(9), F(10)], [F(5), F(8)]
roots_check(1, -19, 90, xs), roots_check(1, -13, 40, ys)
qe("Relation between roots", B, "Solve equations I and II and choose the relation between x and y that is true for every pair of their roots.",
   "x² − 19x + 90 = 0", "y² − 13y + 40 = 0", xs, ys, ">", ["<", "<="],
   "Factorise each quadratic; compare the smallest x with the largest y",
   "I: (x − 9)(x − 10) = 0, so x = 9 or 10. II: (y − 5)(y − 8) = 0, so y = 5 or 8. The smallest x (9) is greater than "
   "the largest y (8), so x > y.",
   ["I: 9 × 10 = 90, 9 + 10 = 19 ⇒ x = 9, 10", "II: 5 × 8 = 40, 5 + 8 = 13 ⇒ y = 5, 8", "min x = 9 > max y = 8",
    "So x > y"],
   why="x < y and x ≤ y come from a sign slip that gives negative roots for I (−9 and −10).", secs=40)

xs, ys = [F(7), F(-12)], [F(7), F(9)]
roots_check(1, 5, -84, xs), roots_check(1, -16, 63, ys)
qe("Relation between roots", B, "Work out the roots of both equations, then mark the relation between x and y.",
   "x² + 5x − 84 = 0", "y² − 16y + 63 = 0", xs, ys, "<=", ["<", ">="],
   "When the two equations share a root, the relation can only be non-strict",
   "I: (x + 12)(x − 7) = 0, so x = 7 or −12. II: (y − 7)(y − 9) = 0, so y = 7 or 9. x = 7 = y is possible, and every "
   "other pair has x < y. So x ≤ y.",
   ["I: 12 × 7 = 84, 12 − 7 = 5 ⇒ x = −12, 7", "II: y = 7, 9", "x = y = 7 possible", "Other pairs: x < y ⇒ x ≤ y"],
   why="x < y misses the common root 7; x ≥ y holds only for the pair x = y = 7.", secs=45)

xs, ys = [F(-8), F(-10)], [F(-5), F(-6)]
roots_check(1, 18, 80, xs), roots_check(1, 11, 30, ys)
qe("Relation between roots", B, "Both equations have only negative roots. Solve them and choose how x is related to y.",
   "x² + 18x + 80 = 0", "y² + 11y + 30 = 0", xs, ys, "<", [">", ">="],
   "With all coefficients positive, both roots are negative; compare the largest x with the smallest y",
   "I: (x + 8)(x + 10) = 0, so x = −8 or −10. II: (y + 5)(y + 6) = 0, so y = −5 or −6. The largest x (−8) is below the "
   "smallest y (−6), so x < y.",
   ["I: x = −8, −10", "II: y = −5, −6", "max x = −8 < min y = −6", "So x < y"],
   why="x > y and x ≥ y come from comparing 8 and 10 with 5 and 6 without the minus signs.", secs=40)

xs, ys = [F(3, 2), F(4)], [F(2), F(5)]
roots_check(2, -11, 12, xs), roots_check(1, -7, 10, ys)
qe("Relation between roots", B, "Find all the roots of I and II and decide which relation between x and y, if any, always holds.",
   "2x² − 11x + 12 = 0", "y² − 7y + 10 = 0", xs, ys, "cbe", [">", "<="],
   "If the roots of one equation lie on both sides of a root of the other, no relation holds for every pair",
   "I: (2x − 3)(x − 4) = 0, so x = 1.5 or 4. II: (y − 2)(y − 5) = 0, so y = 2 or 5. x = 4 is above y = 2 but below "
   "y = 5, so the relationship cannot be established.",
   ["I: 2x² − 8x − 3x + 12 = (x − 4)(2x − 3) ⇒ x = 4, 1.5", "II: y = 2, 5", "4 > 2 but 4 < 5", "Cannot be established"],
   why="x > y uses only the pair x = 4, y = 2; x ≤ y and x < y use x = 1.5 or the pair x = 4, y = 5.", secs=45)

xs = [F(6)]
assert F(4, 10) * 6 + F(12, 10) == F(25, 100) * 6 + F(21, 10)
ys = [F(6), F(7)]
roots_check(1, -13, 42, ys)
qe("Linear vs quadratic", I, "Equation I is linear with decimal coefficients and equation II is quadratic. Solve both and choose the relation between x and y.",
   "0.4x + 1.2 = 0.25x + 2.1", "y² − 13y + 42 = 0", xs, ys, "<=", ["<", ">"],
   "Collect the x-terms in the linear equation; a value shared with the quadratic makes the relation non-strict",
   "I: 0.4x − 0.25x = 2.1 − 1.2, so 0.15x = 0.9 and x = 6. II: (y − 6)(y − 7) = 0, so y = 6 or 7. x = y when y = 6 "
   "and x < y when y = 7, so x ≤ y.",
   ["I: 0.15x = 0.9 ⇒ x = 6", "II: y = 6, 7", "6 = 6 and 6 < 7", "So x ≤ y"],
   why="x < y misses y = 6; x > y comes from moving 1.2 to the right side with the wrong sign (0.15x = 3.3 ⇒ x = 22).",
   secs=55)

xs, ys = [F(3, 2), F(5, 3)], [F(3, 2), F(7, 5)]
roots_check(6, -19, 15, xs), roots_check(10, -29, 21, ys)
qe("Relation between roots", I, "Solve both equations, whose roots are fractions, and choose the relation between x and y.",
   "6x² − 19x + 15 = 0", "10y² − 29y + 21 = 0", xs, ys, ">=", [">", "<"],
   "Split the middle term using factors of a × c; check for a common root",
   "I: 6x² − 9x − 10x + 15 = (2x − 3)(3x − 5) = 0, so x = 1.5 or 5/3. II: 10y² − 15y − 14y + 21 = (2y − 3)(5y − 7) = 0, "
   "so y = 1.5 or 1.4. x = y = 1.5 is possible and every other pair has x > y, so x ≥ y.",
   ["I: (2x − 3)(3x − 5) ⇒ x = 1.5, 1.67", "II: (2y − 3)(5y − 7) ⇒ y = 1.5, 1.4", "x = y = 1.5 possible",
    "Other pairs: x > y ⇒ x ≥ y"],
   why="x > y misses the common root 1.5; x < y comes from taking 5y − 7 = 0 as y = 7/2 = 3.5.", secs=70)

xs, ys = [F(-3, 2)], [F(-1), F(-2)]
roots_check(4, 12, 9, xs), roots_check(1, 3, 2, ys)
qe("Relation between roots", I, "Equation I is a perfect square. Solve both equations and choose the relation between x and y.",
   "4x² + 12x + 9 = 0", "y² + 3y + 2 = 0", xs, ys, "cbe", [">", "<="],
   "A perfect-square quadratic has one repeated root; see where it falls among the other equation's roots",
   "I: (2x + 3)² = 0, so x = −1.5 only. II: (y + 1)(y + 2) = 0, so y = −1 or −2. −1.5 lies between −2 and −1: it is "
   "greater than −2 but less than −1. So the relationship cannot be established.",
   ["I: (2x + 3)² = 0 ⇒ x = −1.5", "II: y = −1, −2", "−1.5 > −2 but −1.5 < −1", "Cannot be established"],
   why="x > y compares −1.5 with −2 only; x ≤ y and x < y compare it with −1 only.", secs=60)

xs = [F(0), F(4)]
for r in xs:
    assert 2 ** int(r * r) == 16 ** int(r)
ys = [F(4), F(5)]
roots_check(1, -9, 20, ys)
qe("Relation between roots", A, "Equation I is an exponential equation. Find every real value of x and y and choose the relation between them.",
   "2^(x²) = 16ˣ", "y² − 9y + 20 = 0", xs, ys, "<=", ["<", ">="],
   "Write both sides with base 2 and equate the exponents; do not divide by x, which could be zero",
   "I: 16ˣ = 2^(4x), so x² = 4x, i.e. x(x − 4) = 0 and x = 0 or 4. II: (y − 4)(y − 5) = 0, so y = 4 or 5. x = 4 = y "
   "is possible and every other pair has x < y. So x ≤ y.",
   ["I: 2^(x²) = 2^(4x) ⇒ x² = 4x", "x(x − 4) = 0 ⇒ x = 0, 4", "II: y = 4, 5", "x = y = 4 possible; else x < y",
    "So x ≤ y"],
   why="x < y misses the common value 4; x ≥ y holds only for x = y = 4, and dividing by x (losing x = 0) still "
       "leaves x = 4 < 5.", secs=90)

xs = [F(3), F(-1, 2)]
for r in xs:
    assert F(3) / r + F(4) / (r + 1) == 2
ys = [F(1, 2), F(3, 2)]
roots_check(4, -8, 3, ys)
qe("Relation between roots", A, "Equation I contains fractions in x (x ≠ 0, −1). Clear them, solve both equations and choose the relation between x and y.",
   "3/x + 4/(x + 1) = 2", "4y² − 8y + 3 = 0", xs, ys, "cbe", [">", "<="],
   "Multiply through by x(x + 1) to get a quadratic; check that the roots do not make a denominator zero",
   "I: 3(x + 1) + 4x = 2x(x + 1), so 2x² − 5x − 3 = 0 = (2x + 1)(x − 3), giving x = 3 or −0.5. II: (2y − 1)(2y − 3) = 0, "
   "so y = 0.5 or 1.5. x = 3 is above both y values, but x = −0.5 is below both. So the relationship cannot be "
   "established.",
   ["I: 7x + 3 = 2x² + 2x ⇒ 2x² − 5x − 3 = 0", "x = 3 or −1/2", "II: y = 1/2, 3/2", "3 > 3/2 but −1/2 < 1/2",
    "Cannot be established"],
   why="x > y uses only x = 3; x ≤ y and x < y use only x = −0.5.", secs=95)

xs, ys = [F(22), F(24)], [F(23), F(24)]
roots_check(1, -46, 528, xs), roots_check(1, -47, 552, ys)
qe("Relation between roots", A, "The coefficients below are large. Solve both equations and choose the relation between x and y.",
   "x² − 46x + 528 = 0", "y² − 47y + 552 = 0", xs, ys, "cbe", [">=", "<"],
   "Find two numbers with the given sum and product; near-equal roots must be compared pair by pair",
   "I: 22 + 24 = 46 and 22 × 24 = 528, so x = 22 or 24. II: 23 + 24 = 47 and 23 × 24 = 552, so y = 23 or 24. x = 22 is "
   "below both y values, but x = 24 is above y = 23. So the relationship cannot be established.",
   ["I: x = 22, 24", "II: y = 23, 24", "22 < 23 but 24 > 23", "Cannot be established"],
   short="Half the sum gives the middle: 46/2 = 23 ⇒ roots 23 ± 1; 47/2 = 23.5 ⇒ roots 23.5 ± 0.5.",
   why="x ≥ y and x > y use only x = 24; x < y uses only x = 22 and misses the pair x = 24, y = 23.", secs=90)

# ================================================================ Number System (B1 I2 A1)
T = "Number System"
v = (pow(1234, 567, 10) + pow(5678, 123, 10)) % 10
assert v == 6 and pow(1234, 567, 10) == 4 and pow(5678, 123, 10) == 2 and (4 * 2) % 10 == 8 and (6 + 4) % 10 == 0
Q(T, "Unit digit", B, "What is the unit digit of 1234⁵⁶⁷ + 5678¹²³?",
  "6", ["8", "0", "2"],
  "Only the unit digits matter: powers of 4 end in 4, 6, 4, 6, … and powers of 8 cycle 8, 4, 2, 6",
  "1234⁵⁶⁷ ends like 4⁵⁶⁷; an odd power of 4 ends in 4. 5678¹²³ ends like 8¹²³; 123 = 4 × 30 + 3, so it ends like 8³ = "
  "512, i.e. in 2. The sum ends in 4 + 2 = 6.",
  ["4^odd ends in 4", "123 ÷ 4 leaves 3 ⇒ 8³ ends in 2", "4 + 2 = 6"],
  why="8 multiplies the unit digits (4 × 2) instead of adding them; 0 takes 4⁵⁶⁷ as ending in 6 (an even power); 2 "
      "is the unit digit of the second term alone.", secs=45)

h, l = 27, 2079
pairs = [(a, b) for a in range(h, l + 1, h) for b in range(a, l + 1, h)
         if math.gcd(a, b) == h and a * b // math.gcd(a, b) == l]
assert pairs == [(27, 2079), (189, 297)] and 2079 // 27 == 77 and 2079 // 9 == 231
Q(T, "HCF and LCM", I,
  "The HCF of two numbers is 27 and their LCM is 2,079. If one of the numbers lies between 250 and 300, what is the "
  "other number?",
  "189", ["297", "77", "231"],
  "Write the numbers as 27a and 27b with a, b co-prime; then 27ab = LCM",
  "2,079 ÷ 27 = 77 = 7 × 11, so (a, b) = (1, 77) or (7, 11). The pairs are 27 and 2,079, or 189 and 297. Only the "
  "second pair has a number between 250 and 300 (297), so the other number is 189.",
  ["LCM ÷ HCF = 77 = 7 × 11", "Pairs: (27, 2,079) or (189, 297)", "297 lies in 250–300", "Other number = 189"],
  short="HCF × LCM = product: 27 × 2,079 ÷ 297 = 189.",
  why="297 is the number in the given range, not the other one; 77 is LCM ÷ HCF; 231 divides 2,079 by 9 instead of "
      "using the HCF 27.", secs=60, by=BRUTE)

n = 720
facs = [d for d in range(1, n + 1) if n % d == 0]
even = [d for d in facs if d % 2 == 0]
assert len(facs) == 30 and len(even) == 24 and len(facs) - len(even) == 6 and (4 + 1) * (2 + 1) * (1 + 1) == 30
Q(T, "Divisibility", I, "How many even factors does 720 have?",
  "24", ["30", "6", "20"],
  "720 = 2⁴ × 3² × 5; an even factor must contain at least one 2",
  "720 = 2⁴ × 3² × 5. All factors: (4 + 1)(2 + 1)(1 + 1) = 30. Odd factors use 2⁰ only: (2 + 1)(1 + 1) = 6. Even "
  "factors = 30 − 6 = 24 (equivalently, choose 2¹ to 2⁴: 4 × 3 × 2 = 24).",
  ["720 = 2⁴ × 3² × 5", "Total factors = 5 × 3 × 2 = 30", "Odd factors = 3 × 2 = 6", "Even = 30 − 6 = 24"],
  why="30 counts all the factors; 6 counts only the odd factors; 20 uses 2⁴ × 3 × 5 and misses the 3².", secs=55,
  by=BRUTE)

sol = [x for x in range(1, 1000) if x % 5 == 2 and x % 7 == 3 and x % 9 == 4]
assert sol[:2] == [157, 472] and 31 % 7 == 3 and 31 % 9 == 4 and 94 % 7 == 3 and 94 % 9 == 4 and 31 % 5 != 2
Q(T, "Remainders", A,
  "What is the smallest positive number that leaves a remainder of 2 when divided by 5, a remainder of 3 when "
  "divided by 7 and a remainder of 4 when divided by 9?",
  "157", ["31", "94", "472"],
  "Satisfy the conditions one at a time: list numbers fitting two of them (they repeat every LCM), then test the third",
  "Numbers leaving 4 on division by 9: 4, 13, 22, 31, … The first that also leaves 3 on division by 7 is 31; such "
  "numbers repeat every 63: 31, 94, 157, … Testing division by 5: 31 → 1, 94 → 4, 157 → 2 ✓. So the number is 157.",
  ["÷9 rem 4 and ÷7 rem 3: 31, 94, 157, … (step 63)", "31 ÷ 5 rem 1 ✗", "94 ÷ 5 rem 4 ✗", "157 ÷ 5 rem 2 ✓"],
  why="31 and 94 satisfy the conditions for 7 and 9 but not for 5; 472 also works but is the next such number "
      "(157 + 315), not the smallest.", secs=100, by=BRUTE)

# ================================================================ Percentage (B2 I3 A3)
T = "Percentage"
r_ = F(125, 100) * F(80, 100)
assert r_ == 1 and F(120, 100) * F(80, 100) * 100 == 96 and F(125, 100) * F(120, 100) * 100 == 150
Q(T, "Basic percentage", B,
  "A's salary is 25% more than B's, and B's salary is 20% less than C's. A's salary is what percentage of C's?",
  "100%", ["105%", "95%", "125%"],
  "Chain the multipliers: A = 1.25 B and B = 0.80 C",
  "B = 0.8 C, so A = 1.25 × 0.8 C = C. A's salary is 100% of C's.",
  ["B = 0.8 C", "A = 1.25 × 0.8 C = 1.0 C", "A is 100% of C"],
  short="+25% undoes −20% exactly, because 1.25 = 1 ÷ 0.8.",
  why="105% adds the two percentages (+25 − 20 = +5); 95% subtracts them the other way; 125% compares A with B "
      "instead of with C.", secs=35)

x_ = F(819) / (F(130, 100) * F(70, 100))
assert x_ == 900 and F(819) / F(70, 100) == 1170 and F(819) * F(130, 100) * F(70, 100) == F(74529, 100)
Q(T, "Successive change", B,
  "A number is increased by 30% and the result is then decreased by 30%. The final value is 819. What was the "
  "original number?",
  "900", ["819", "1,170", "745.29"],
  "Successive changes multiply: × 1.3 then × 0.7 = × 0.91",
  "The net multiplier is 1.3 × 0.7 = 0.91, so the original number = 819 ÷ 0.91 = 900.",
  ["Net factor = 1.3 × 0.7 = 0.91", "Original = 819 ÷ 0.91 = 900"],
  why="819 assumes +30% and −30% cancel; 1,170 undoes only the 30% fall (819 ÷ 0.7); 745.29 applies the two changes "
      "to 819 again instead of reversing them.", secs=40)

v = F(60, 100) * 25 + F(40, 100) * 35
assert v == 29 and F(25 + 35, 2) == 30 and F(40, 100) * 25 + F(60, 100) * 35 == 31 and 25 + 35 == 60
Q(T, "Basic percentage", I,
  "In a class, 40% of the students are girls. 25% of the boys and 35% of the girls scored a distinction. What "
  "percentage of the whole class scored a distinction?",
  "29%", ["30%", "31%", "60%"],
  "The overall rate is a weighted average of the two rates, weighted by the share of boys and girls",
  "Take 100 students: 60 boys and 40 girls. Distinctions: 25% of 60 = 15 and 35% of 40 = 14, so 29 out of 100 = 29%.",
  ["Boys 60, girls 40", "25% of 60 = 15", "35% of 40 = 14", "15 + 14 = 29 ⇒ 29%"],
  why="30% is the simple average of 25% and 35%; 31% swaps the weights (40% boys, 60% girls); 60% adds the two rates.",
  secs=50)

v = F(120, 100) ** 2 * F(80, 100)
assert v == F(1152, 1000) and (v - 1) * 100 == F(152, 10) and F(120, 100) * F(80, 100) == F(96, 100)
Q(T, "Successive change", I,
  "The radius of a cylinder is increased by 20% and its height is decreased by 20%. What is the percentage change "
  "in its volume?",
  "15.2% increase", ["No change", "4% decrease", "44% increase"],
  "Volume ∝ r²h, so the radius change enters twice: multiply 1.2 × 1.2 × 0.8",
  "New volume ÷ old volume = 1.2² × 0.8 = 1.44 × 0.8 = 1.152. The volume rises by 15.2%.",
  ["V ∝ r²h", "Factor = 1.2 × 1.2 × 0.8 = 1.152", "Increase = 15.2%"],
  why="'No change' assumes +20% and −20% cancel; '4% decrease' treats volume as r × h (1.2 × 0.8 = 0.96); '44% "
      "increase' squares the radius change but forgets the height.", secs=55)

M = [m for m in range(100, 2001) if F(30, 100) * m + 15 == F(40, 100) * m - 35]
assert M == [500] and F(30, 100) * 500 + 15 == 165 and F(165, 500) * 100 == 33 and F(200 - 15, 500) * 100 == 37
Q(T, "Basic percentage", I,
  "In a test, a candidate who scored 30% of the maximum marks failed by 15 marks, while another who scored 40% got "
  "35 marks more than the pass mark. What percentage of the maximum marks is needed to pass?",
  "33%", ["35%", "37%", "30%"],
  "Both statements describe the same pass mark: set 30% of M + 15 equal to 40% of M − 35",
  "0.3M + 15 = 0.4M − 35, so 0.1M = 50 and M = 500. Pass mark = 0.3 × 500 + 15 = 165, which is 165 ÷ 500 = 33%.",
  ["0.3M + 15 = 0.4M − 35", "0.1M = 50 ⇒ M = 500", "Pass mark = 150 + 15 = 165", "165 ÷ 500 = 33%"],
  why="35% takes the mid-point of 30% and 40%; 37% subtracts 15 from the 40% score (200 − 15 = 185) instead of 35; "
      "30% is the failing candidate's own score.", secs=60, by=BRUTE)

yrs = next(n for n in range(1, 20) if F(85, 100) ** n < F(1, 2))
assert yrs == 5 and F(85, 100) ** 4 > F(1, 2) and r2(F(85, 100) ** 4) == F(52, 100) and r2(F(85, 100) ** 5) == F(44, 100)
Q(T, "Population and depreciation", A,
  "A car loses 15% of its value every year (on its value at the start of that year). After how many complete years "
  "will its value first fall below half of the purchase price?",
  "5 years", ["4 years", "3 years", "6 years"],
  "Depreciation compounds: value after n years = P × 0.85ⁿ; find the first n with 0.85ⁿ < 0.5",
  "0.85² = 0.7225, 0.85³ ≈ 0.614, 0.85⁴ ≈ 0.522 (still above half) and 0.85⁵ ≈ 0.444 (below half). So it first falls "
  "below half after 5 years.",
  ["0.85² = 0.7225", "0.85³ ≈ 0.6141", "0.85⁴ ≈ 0.5220 > 0.5", "0.85⁵ ≈ 0.4437 < 0.5"],
  why="4 years stops too early (52.2% of the price is left); 3 years uses straight-line loss (50 ÷ 15 ≈ 3.3, rounded "
      "down); 6 years is one year after it has already fallen below half.", secs=75)

inc = 100
food, rent, other = 40, 15, 25
sav0 = inc - food - rent - other
new_exp = food * F(125, 100) + rent * F(120, 100) + other
sav1 = F(110) - new_exp
assert sav0 == 20 and new_exp == 93 and sav1 == 17 and (sav1 - sav0) / sav0 * 100 == -15
assert F(110) - (food + rent + other) * F(110, 100) == 22 and F(110) - (80 + 10 + 3) == 17
Q(T, "Income and expenditure", A,
  "A family spends 40% of its income on food, 15% on rent and 25% on other items, and saves the rest. Its income "
  "rises by 10%, food costs rise by 25%, rent rises by 20% and other spending does not change. By what percentage "
  "do its savings change?",
  "15% decrease", ["10% increase", "3% decrease", "15% increase"],
  "Take income = 100; update each spending head separately and recompute savings",
  "Old: spending 40 + 15 + 25 = 80, savings 20. New: income 110; food 50, rent 18, others 25, total 93; savings 17. "
  "Savings fall from 20 to 17, i.e. by 15%.",
  ["Old savings = 100 − 80 = 20", "New spending = 50 + 18 + 25 = 93", "New savings = 110 − 93 = 17",
   "Change = −3 on 20 = −15%"],
  why="'10% increase' assumes savings move with income; '3% decrease' gives the fall in rupees per 100 of old income, "
      "not as a percentage of the old savings; '15% increase' gets the sign of the change wrong.", secs=95)

A_ = 75000 * F(104, 100) ** 2
B_ = 90000 * F(95, 100) ** 2
assert A_ == 81120 and B_ == 81225 and B_ - A_ == 105
assert 75000 * F(108, 100) == 81000 == 90000 * F(90, 100) and B_ - 81000 == 225
Q(T, "Population and depreciation", A,
  "Town P has 75,000 people and its population grows by 4% a year. Town Q has 90,000 people and its population falls "
  "by 5% a year. Both rates are applied on the population at the start of each year. After 2 years, which town has "
  "more people, and by how many?",
  "Town Q, by 105", ["Both have the same population", "Town P, by 105", "Town Q, by 225"],
  "Apply each rate twice (compounding) and compare",
  "P: 75,000 × 1.04² = 75,000 × 1.0816 = 81,120. Q: 90,000 × 0.95² = 90,000 × 0.9025 = 81,225. Q still has 105 more "
  "people.",
  ["P: 75,000 × 1.0816 = 81,120", "Q: 90,000 × 0.9025 = 81,225", "Q − P = 105"],
  why="'Same population' applies the rates as simple (non-compounding) changes: 75,000 × 1.08 = 90,000 × 0.90 = "
      "81,000; 'Town P, by 105' reverses the difference; 'Town Q, by 225' compounds Q's fall but treats P's growth "
      "as simple (81,000).", secs=90)

# ================================================================ Ratio and Proportion (B1 I1 A2)
T = "Ratio and Proportion"
v = F(18 * 30, 12)
assert v == 45 and F(12 * 30, 18) == 20 and 18 + (30 - 12) == 36 and 18 * 30 == 540
Q(T, "Proportion", B, "What is the fourth proportional to 12, 18 and 30?",
  "45", ["20", "36", "540"],
  "x is the fourth proportional to a, b, c when a : b = c : x, so x = bc ÷ a",
  "12 : 18 = 30 : x, so x = 18 × 30 ÷ 12 = 540 ÷ 12 = 45.",
  ["12 : 18 = 30 : x", "x = 18 × 30 ÷ 12", "x = 45"],
  why="20 sets up 18 : 12 = 30 : x (the ratio reversed); 36 adds the difference 18 − 12 to 30 instead of keeping the "
      "ratio; 540 forgets to divide by 12.", secs=35)

sol = [n for n in range(1, 200) if F(n, 2) + 2 * n + 2 * (2 * n - 5) == 185]
assert sol == [30] and 2 * 30 - 5 == 55
Q(T, "Coins and salary share", I,
  "A purse contains 50-paise, ₹1 and ₹2 coins worth ₹185 in all. There are twice as many ₹1 coins as 50-paise "
  "coins, and 5 fewer ₹2 coins than ₹1 coins. How many ₹2 coins are there?",
  "55", ["30", "60", "50"],
  "Let the number of 50-paise coins be n and write the total value in rupees",
  "50-paise coins: n; ₹1 coins: 2n; ₹2 coins: 2n − 5. Value: 0.5n + 2n + 2(2n − 5) = 6.5n − 10 = 185, so n = 30. "
  "₹2 coins = 2 × 30 − 5 = 55.",
  ["0.5n + 2n + 2(2n − 5) = 185", "6.5n = 195 ⇒ n = 30", "₹2 coins = 60 − 5 = 55"],
  why="30 is the number of 50-paise coins; 60 is the number of ₹1 coins; 50 subtracts 10 instead of 5 from 60.",
  secs=60, by=BRUTE)

kk = F(14 * 2, 6 + 7 + 8)
ab, bc, ca = 6 * kk, 7 * kk, 8 * kk
a_, b_, c_ = 14 - bc, 14 - ca, 14 - ab
assert (a_, b_, c_) == (F(14, 3), F(10, 3), 6) and a_ + b_ == ab and b_ + c_ == bc and c_ + a_ == ca
Q(T, "Basic ratio", A, "If (a + b) : (b + c) : (c + a) = 6 : 7 : 8 and a + b + c = 14, what is the value of c?",
  "6", ["14/3", "10/3", "8"],
  "Adding the three sums gives 2(a + b + c); this fixes the scale k of the ratio",
  "(a + b) + (b + c) + (c + a) = 21k = 2 × 14 = 28, so k = 4/3. Then a + b = 6k = 8, and c = 14 − 8 = 6.",
  ["Sum of the three = 2(a + b + c) = 28", "21k = 28 ⇒ k = 4/3", "a + b = 6 × 4/3 = 8", "c = 14 − 8 = 6"],
  why="14/3 is the value of a and 10/3 the value of b; 8 is a + b, not c.", secs=80)

T_ = F(2600 + 300 - 500) / (1 - F(2, 5) - F(1, 3))
assert F(2600) * F(15, 4) == 9750 and F(2800) * F(15, 4) == 10500
assert T_ == 9000 and F(2, 5) * 9000 + 300 == 3900 and F(9000, 3) - 500 == 2500 and 3900 + 2500 + 2600 == 9000
Q(T, "Coins and salary share", A,
  "A sum of money is divided among P, Q and R. P gets ₹300 more than two-fifths of the sum, Q gets ₹500 less than "
  "one-third of the sum, and R gets ₹2,600. What is the total sum?",
  "₹9,000", ["₹3,900", "₹9,750", "₹10,500"],
  "Write each share in terms of the total S and use P + Q + R = S",
  "(2S/5 + 300) + (S/3 − 500) + 2,600 = S, so 11S/15 + 2,400 = S, i.e. 4S/15 = 2,400 and S = ₹9,000. "
  "(Check: P = 3,900, Q = 2,500, R = 2,600.)",
  ["P = 2S/5 + 300, Q = S/3 − 500, R = 2,600", "11S/15 + 2,400 = S", "4S/15 = 2,400 ⇒ S = 9,000"],
  why="₹3,900 is P's share; ₹9,750 forgets the ₹300 and ₹500 adjustments (4S/15 = 2,600); ₹10,500 moves the "
      "adjustments across with the wrong signs (4S/15 = 2,800).", secs=85)

# ================================================================ Problems on Ages (B1 I2 A1)
T = "Problems on Ages"
H = 3 * 27 - (2 * 20 + 3 * 2)
assert H == 35 and 81 - 40 == 41 and 81 - 43 == 38 and 81 - 34 == 47
Q(T, "Present and future ages", B,
  "The average present age of a husband, his wife and their child is 27 years. Three years ago, the average age of "
  "the wife and the child was 20 years. What is the husband's present age?",
  "35 years", ["41 years", "38 years", "47 years"],
  "Convert averages to totals, and move the past total to the present by adding 3 years for each person",
  "Present total of all three = 3 × 27 = 81. Three years ago, wife + child = 2 × 20 = 40, so now they total "
  "40 + 6 = 46. Husband = 81 − 46 = 35 years.",
  ["Total now = 81", "Wife + child 3 years ago = 40", "Wife + child now = 46", "Husband = 81 − 46 = 35"],
  why="41 forgets to add 3 years to each of the wife and child; 38 adds 3 years only once; 47 subtracts 6 years "
      "instead of adding them.", secs=45)

sol = [(f, s) for s in range(1, 60) for f in [12 * s] if f + s == 65]
assert sol == [(60, 5)]
Q(T, "Present and future ages", I,
  "A father is as many years old as his son is months old. The sum of their ages is 65 years. How old is the "
  "father?",
  "60 years", ["5 years", "55 years", "52 years"],
  "The son's age in months is 12 times his age in years, so the father is 12 times as old as the son",
  "If the son is s years old, he is 12s months old, so the father is 12s years old. 12s + s = 65 gives s = 5, and the "
  "father is 60.",
  ["Son = s years = 12s months", "Father = 12s years", "13s = 65 ⇒ s = 5", "Father = 60"],
  why="5 years is the son's age; 55 takes the son as 10; 52 splits 65 in the ratio 4 : 1.", secs=50, by=BRUTE)

sol = [(f, s) for s in range(1, 80) for f in [s + 28] if 5 * f == 9 * s]
f_, s_ = sol[0]
nn = [n for n in range(0, 100) if 2 * (f_ + n) == 3 * (s_ + n)]
assert sol == [(63, 35)] and nn == [21] and (f_ - F(3, 2) * s_) == F(21, 2)
Q(T, "Ratio-based ages", I,
  "When Ravi was born, his father was 28 years old. Now the father is 1.8 times as old as Ravi. After how many years "
  "will the father be 1.5 times as old as Ravi?",
  "21 years", ["10.5 years", "28 years", "35 years"],
  "The age gap (28 years) never changes; use it to find the present ages, then set up the future ratio",
  "Father − Ravi = 28 and Father = 1.8 × Ravi, so 0.8 × Ravi = 28: Ravi is 35 and the father 63. Then "
  "63 + n = 1.5(35 + n) gives 0.5n = 10.5 and n = 21.",
  ["F − R = 28, F = 1.8R ⇒ R = 35, F = 63", "63 + n = 1.5(35 + n)", "0.5n = 10.5 ⇒ n = 21"],
  short="When F = 1.5R, the gap 28 = 0.5R, so R = 56: that is 56 − 35 = 21 years from now.",
  why="10.5 forgets to divide by 0.5; 28 is the age gap; 35 is Ravi's present age.", secs=65, by=BRUTE)

sol = [(f, m, e, y) for y in range(1, 40) for e in [y + 3] for m in range(15, 80) for f in [m + 5]
       if f + m + e + y == 104 and (f - y) + (m - y) + (e - y) == 64]
assert sol == [(43, 38, 13, 10)]
Q(T, "Present and future ages", A,
  "A family has a father, a mother and two children. The four ages now add up to 104 years. The father is 5 years "
  "older than the mother, and the elder child is 3 years older than the younger. When the younger child was born, "
  "the ages of the other three members added up to 64 years. What is the mother's present age?",
  "38 years", ["43 years", "40.5 years", "28 years"],
  "Going back y years (the younger child's age) takes y years off each of the other three members",
  "Let the younger child be y. Then the other three now total 104 − y, and y years ago they totalled "
  "104 − y − 3y = 104 − 4y = 64, so y = 10. The elder child is 13, so the parents total 104 − 23 = 81. With the "
  "father 5 years older, the mother is (81 − 5) ÷ 2 = 38.",
  ["Others then = (104 − y) − 3y = 64 ⇒ y = 10", "Elder child = 13", "Parents = 104 − 23 = 81",
   "Mother = (81 − 5) ÷ 2 = 38"],
  why="43 is the father's age; 40.5 splits 81 equally and ignores the 5-year gap; 28 is the mother's age when the "
      "younger child was born.", secs=110, by=BRUTE)

# ================================================================ Average (B2 I2 A1)
T = "Average"
tot, ab_, bc_ = 3 * 60, 2 * 56, 2 * 61
b_ = ab_ + bc_ - tot
assert b_ == 54 and ab_ - b_ == 58 and bc_ - b_ == 68
Q(T, "Simple average", B,
  "The average weight of A, B and C is 60 kg. The average weight of A and B is 56 kg, and that of B and C is 61 kg. "
  "What is B's weight?",
  "54 kg", ["58 kg", "68 kg", "56 kg"],
  "Convert each average to a total; B is counted in both pair totals",
  "A + B + C = 180, A + B = 112 and B + C = 122. Adding the pair totals counts B twice: 112 + 122 = 234 = 180 + B, so "
  "B = 54 kg.",
  ["A + B + C = 180", "A + B = 112, B + C = 122", "B = 112 + 122 − 180 = 54"],
  why="58 kg is A's weight; 68 kg is C's weight; 56 kg is the average of A and B, not B's own weight.", secs=40)

v = F(120 * 45 + 80 * 60, 200)
assert v == 51 and F(45 + 60, 2) == F(105, 2) and F(120 * 60 + 80 * 45, 200) == 54 and 120 * 45 + 80 * 60 == 10200
Q(T, "Weighted average", B,
  "A shop sold 120 items at an average price of ₹45 on Monday and 80 items at an average price of ₹60 on Tuesday. "
  "What was the average price of all the items sold on the two days?",
  "₹51", ["₹52.50", "₹54", "₹10,200"],
  "Average of all items = total takings ÷ total items",
  "Takings: 120 × 45 = ₹5,400 and 80 × 60 = ₹4,800, total ₹10,200 for 200 items. Average = 10,200 ÷ 200 = ₹51.",
  ["120 × 45 = 5,400", "80 × 60 = 4,800", "10,200 ÷ 200 = 51"],
  why="₹52.50 is the simple average of 45 and 60, which ignores the numbers sold; ₹54 swaps the weights; ₹10,200 is "
      "the total takings, not the average.", secs=40)

x_ = (17 * 17500 - (15 * 18000 - 24000)) / F(2)
assert x_ == 25750 and (17 * 17500 - 15 * 18000) / F(2) == 13750 and (16 * 17500 - (15 * 18000 - 24000)) / F(2) == 17000
Q(T, "Replacement", I,
  "The average monthly salary of 15 workers is ₹18,000. A worker earning ₹24,000 leaves, and two new workers with "
  "equal salaries join. The average salary of the group is now ₹17,500. What is the salary of each new worker?",
  "₹25,750", ["₹51,500", "₹17,000", "₹13,750"],
  "Track the total: remove the leaving worker's salary, then compare with the new total for the new group size",
  "Old total = 15 × 18,000 = ₹2,70,000. After the worker leaves: ₹2,46,000 for 14 workers. With two more there are "
  "17 workers and the total is 17 × 17,500 = ₹2,97,500. The two new salaries add up to 2,97,500 − 2,46,000 = ₹51,500, "
  "so each is ₹25,750.",
  ["Old total = 2,70,000", "After leaving: 2,46,000", "New total = 17 × 17,500 = 2,97,500",
   "Two new = 51,500 ⇒ each 25,750"],
  why="₹51,500 is the two new salaries together; ₹17,000 counts the new group as 16 workers; ₹13,750 forgets to remove "
      "the leaving worker's ₹24,000.", secs=65)

terms = [45 + 3 * k for k in range(-3, 4)]
assert sum(terms) == 7 * 45 and terms[0] * terms[-1] == 1944 and 45 * 45 == 2025 and 39 * 51 == 1989 and 42 * 48 == 2016
Q(T, "Simple average", I,
  "The average of seven consecutive multiples of 3 is 45. What is the product of the smallest and the largest of "
  "them?",
  "1,944", ["2,025", "1,989", "2,016"],
  "Consecutive multiples of 3 are equally spaced, so their average is the middle (4th) term",
  "The middle term is 45, so the numbers are 36, 39, 42, 45, 48, 51 and 54. The product of the smallest and largest is "
  "36 × 54 = 1,944.",
  ["Middle term = 45", "Numbers: 36, 39, …, 54", "36 × 54 = 1,944"],
  why="2,025 = 45², the middle term squared; 1,989 = 39 × 51, the second and sixth terms; 2,016 = 42 × 48, the third "
      "and fifth terms.", secs=50)

g = next(g for g in range(1, 100) if 30 * 150 + 140 * g == 146 * (30 + g))
new_avg = F(30 * 150 - 5 * 152 + g * 140 + 5 * 138, 30 + g)
assert g == 20 and new_avg == F(723, 5) and F(30 * 150 - 750 + 2800 + 700, 50) == 145
assert F(30 * 150 - 690 + 2800 + 760, 50) == F(737, 5)
Q(T, "Weighted average", A,
  "In a class, the 30 boys have an average height of 150 cm and the girls an average height of 140 cm; the average "
  "height of the whole class is 146 cm. Five boys with an average height of 152 cm leave the class, and five new "
  "girls with an average height of 138 cm join it. What is the new average height of the class?",
  "144.6 cm", ["145 cm", "146 cm", "147.4 cm"],
  "First find the number of girls from the weighted average, then update the total height",
  "30 × 150 + 140g = 146(30 + g) gives 4,500 + 140g = 4,380 + 146g, so g = 20 and the class has 50 students. "
  "Total height = 7,300 cm. Remove 5 × 152 = 760 and add 5 × 138 = 690: new total 7,230 cm for 50 students, so the "
  "new average is 144.6 cm.",
  ["Girls: 6g = 120 ⇒ g = 20", "Total = 50 × 146 = 7,300", "7,300 − 760 + 690 = 7,230", "7,230 ÷ 50 = 144.6"],
  why="145 cm assumes the leaving boys and joining girls are at their groups' averages (150 and 140); 146 cm assumes "
      "the average does not change because the class size is the same; 147.4 cm swaps the 760 and the 690.", secs=100)

# ================================================================ Profit and Loss (B2 I2 A1)
T = "Profit and Loss"
cp, sp = F(6000), F(270 * 25)
assert (sp - cp) / cp * 100 == F(25, 2) and r2((sp - cp) / sp * 100) == F(1111, 100) and sp / cp * 100 == F(225, 2)
Q(T, "Cost and selling price", B,
  "A trader buys 25 kg of tea for ₹6,000 and sells all of it at ₹270 per kg. What is his profit percentage?",
  "12.5%", ["11.11%", "30%", "112.5%"],
  "Profit % = (SP − CP) ÷ CP × 100, with both prices for the same quantity",
  "Cost per kg = 6,000 ÷ 25 = ₹240. Profit per kg = 270 − 240 = ₹30, so profit % = 30 ÷ 240 × 100 = 12.5%.",
  ["CP per kg = 240", "Profit per kg = 30", "30 ÷ 240 = 12.5%"],
  why="11.11% divides the profit by the selling price (30 ÷ 270); 30% takes the ₹30 profit per kg as a percentage; "
      "112.5% is SP as a percentage of CP.", secs=35)

g_ = F(1000 - 960, 960) * 100
assert g_ == F(25, 6) and F(40, 1000) * 100 == 4 and r2(F(40, 1040) * 100) == F(385, 100)
Q(T, "Dishonest dealer", B,
  "A shopkeeper sells rice at its cost price but uses a false weight of 960 g in place of 1 kg. What is his gain "
  "percentage?",
  "4⅙%", ["4%", "40%", "3.85%"],
  "Gain % = error ÷ (true value given) × 100",
  "For every 960 g he gives, he charges the cost of 1,000 g. Gain = 40 g on 960 g = 40 ÷ 960 × 100 = 4⅙%.",
  ["Gives 960 g, charges for 1,000 g", "Gain = 40 g", "40 ÷ 960 × 100 = 4⅙%"],
  why="4% divides the 40 g by 1,000 g instead of by the 960 g actually given; 40% misplaces the decimal; 3.85% divides "
      "by 1,040 g.", secs=40)

cp_ = F(22770) / (F(110, 100) * F(115, 100) * F(90, 100))
assert cp_ == 20000 and F(22770) / F(115, 100) == 19800 and F(22770) / F(1265, 1000) == 18000 and F(22770) / F(11, 10) == 20700
Q(T, "Successive transactions", I,
  "A sells an article to B at a profit of 10%, B sells it to C at a profit of 15%, and C sells it to D at a loss of "
  "10%. If D pays ₹22,770, at what price did A buy it?",
  "₹20,000", ["₹19,800", "₹18,000", "₹20,700"],
  "Successive selling prices multiply the cost by 1.10, 1.15 and 0.90",
  "D's price = A's cost × 1.1 × 1.15 × 0.9 = A's cost × 1.1385. So A's cost = 22,770 ÷ 1.1385 = ₹20,000.",
  ["Factor = 1.1 × 1.15 × 0.9 = 1.1385", "A's cost = 22,770 ÷ 1.1385 = 20,000"],
  why="₹19,800 adds the rates (+10 + 15 − 10 = +15%); ₹18,000 ignores C's loss (22,770 ÷ 1.265); ₹20,700 undoes only "
      "A's 10% profit.", secs=55)

cp_ = F(4800) * F(75, 100) / F(120, 100)
assert cp_ == 3000 and F(3600) * F(80, 100) == 2880 and F(4800) * F(80, 100) == 3840
Q(T, "Marked price", I,
  "An article is marked at ₹4,800. After a discount of 25%, the shopkeeper still makes a profit of 20%. What is its "
  "cost price?",
  "₹3,000", ["₹2,880", "₹3,840", "₹3,600"],
  "SP = MP × (1 − discount) and SP = CP × (1 + profit)",
  "SP = 4,800 × 0.75 = ₹3,600. Then CP = 3,600 ÷ 1.2 = ₹3,000.",
  ["SP = 4,800 × 0.75 = 3,600", "CP = 3,600 ÷ 1.2 = 3,000"],
  why="₹2,880 takes 20% off the SP instead of dividing by 1.2; ₹3,840 takes 20% off the marked price; ₹3,600 is the "
      "selling price.", secs=50)

f_ = F(120, 100) * F(125, 100) * F(88, 100)
x_ = F(480) / (f_ - 1)
assert f_ == F(132, 100) and x_ == 1500 and F(480) / F(20, 100) == 2400 and F(480) / F(25, 100) == 1920 and x_ * f_ == 1980
Q(T, "Successive transactions", A,
  "A sells a mixer to B at a profit of 20%. B marks it 25% above his cost and sells it to C at a discount of 12%. C "
  "pays ₹480 more than A's cost. What was A's cost?",
  "₹1,500", ["₹2,400", "₹1,920", "₹1,980"],
  "Chain the factors: C pays A's cost × 1.20 × 1.25 × 0.88",
  "C's price = x × 1.2 × 1.25 × 0.88 = 1.32x. So 1.32x − x = 0.32x = 480 and x = ₹1,500.",
  ["Factor = 1.2 × 1.25 × 0.88 = 1.32", "0.32x = 480", "x = 1,500"],
  why="₹2,400 uses only A's 20% profit (480 ÷ 0.2); ₹1,920 uses only B's 25% mark-up; ₹1,980 is what C pays, not A's "
      "cost.", secs=80)

# ================================================================ Discount (B1 I1 A1)
T = "Discount"
mp = F(3230) / F(85, 100)
assert mp == 3800 and mp - 3230 == 570 and F(3230) * F(15, 100) == F(9690, 20) and F(3230) * F(115, 100) == F(74290, 20)
Q(T, "Single discount", B,
  "After a discount of 15%, a cooler is sold for ₹3,230. How much is the discount in rupees?",
  "₹570", ["₹484.50", "₹3,800", "₹3,714.50"],
  "SP = MP × 0.85, so MP = SP ÷ 0.85; discount = MP − SP",
  "MP = 3,230 ÷ 0.85 = ₹3,800. Discount = 3,800 − 3,230 = ₹570.",
  ["MP = 3,230 ÷ 0.85 = 3,800", "Discount = 3,800 − 3,230 = 570"],
  why="₹484.50 takes 15% of the selling price instead of the marked price; ₹3,800 is the marked price; ₹3,714.50 adds "
      "15% to the selling price to get a marked price.", secs=40)

ds = [(d1, d2) for d2 in range(1, 50) for d1 in [2 * d2] if 6000 * (100 - d1) * (100 - d2) == 4320 * 10000]
assert ds == [(20, 10)] and F(28, 3) * 2 == F(56, 3)
Q(T, "Successive discounts", I,
  "An article marked at ₹6,000 is sold for ₹4,320 after two successive discounts. The first discount is twice the "
  "second. What is the first discount?",
  "20%", ["18⅔%", "28%", "10%"],
  "Successive discounts multiply: (1 − 2d)(1 − d) = 4,320 ÷ 6,000 = 0.72",
  "(1 − 2d)(1 − d) = 0.72 ⇒ 2d² − 3d + 0.28 = 0 ⇒ d = 0.1 (the other root, 1.4, is impossible). So the discounts "
  "are 20% and 10%: 6,000 × 0.8 × 0.9 = 4,320 ✓.",
  ["4,320 ÷ 6,000 = 0.72", "(1 − 2d)(1 − d) = 0.72", "d = 0.1 ⇒ discounts 20% and 10%", "Check: 0.8 × 0.9 = 0.72"],
  short="Try the options: 20% then 10% gives 0.8 × 0.9 = 0.72 at once.",
  why="18⅔% splits the overall 28% in the ratio 2 : 1, as if successive discounts added; 28% is the single "
      "equivalent discount; 10% is the second discount.", secs=60, by=BRUTE)

C = F(100)
mp = C * F(150, 100)
w_cost = mp * F(80, 100)
w_sp = mp * F(90, 100) * F(95, 100)
p_ = (w_sp - w_cost) / w_cost * 100
assert w_cost == 120 and w_sp == F(25650, 200) and p_ == F(55, 8) and (w_sp - w_cost) == F(825, 100)
assert (mp * F(85, 100) - w_cost) / w_cost * 100 == F(25, 4) and w_sp - C == F(2825, 100)
Q(T, "Discount with profit", A,
  "A manufacturer marks his goods 50% above cost and sells them to a wholesaler at a discount of 20% on the marked "
  "price. The wholesaler sells them at the same marked price after two successive discounts of 10% and 5%. What is "
  "the wholesaler's profit percentage?",
  "6.875%", ["8.25%", "6.25%", "28.25%"],
  "Work with the manufacturer's cost = 100; the wholesaler's cost is the manufacturer's selling price",
  "Marked price = 150. The wholesaler pays 150 × 0.8 = 120 and sells at 150 × 0.9 × 0.95 = 128.25. Profit = 8.25 on "
  "120 = 6.875%.",
  ["MP = 150", "Wholesaler's cost = 120", "Wholesaler's SP = 150 × 0.855 = 128.25", "8.25 ÷ 120 = 6.875%"],
  why="8.25% divides the profit by the manufacturer's cost (100) instead of the wholesaler's (120); 6.25% adds the "
      "discounts to a single 15%; 28.25% measures the final price against the manufacturer's cost.", secs=95)

# ================================================================ Simple Interest (B1 I1 A1)
T = "Simple Interest"
P_ = F(2268) / (F(7, 100) * 3)
assert P_ == 10800 and F(2268) / F(7, 100) == 32400 and 2268 * 7 == 15876 and P_ + 2268 == 13068
Q(T, "Basic SI", B,
  "What sum of money earns a simple interest of ₹2,268 in 3 years at 7% per annum?",
  "₹10,800", ["₹32,400", "₹15,876", "₹13,068"],
  "P = SI × 100 ÷ (R × T)",
  "P = 2,268 × 100 ÷ (7 × 3) = 2,26,800 ÷ 21 = ₹10,800.",
  ["P = SI × 100 ÷ (R × T)", "2,268 × 100 ÷ 21 = 10,800"],
  why="₹32,400 forgets the 3 years; ₹15,876 multiplies 2,268 by 7 instead of dividing; ₹13,068 is the amount "
      "(principal + interest), not the sum lent.", secs=35)

P_ = F(540) / F(15, 1000)
assert P_ == 36000 and F(540) / F(75, 1000) == 7200 and F(540) / F(9, 100) == 6000
Q(T, "SI with changing rates", I,
  "A bank cut the simple interest rate on a deposit from 9% to 7.5% per annum. As a result, the depositor's yearly "
  "interest fell by ₹540. How much is the deposit?",
  "₹36,000", ["₹7,200", "₹6,000", "₹3,600"],
  "The fall in yearly interest is the deposit × the fall in the rate",
  "The rate fell by 9 − 7.5 = 1.5 percentage points, so 1.5% of the deposit = ₹540 and the deposit = 540 ÷ 0.015 = "
  "₹36,000.",
  ["Fall in rate = 1.5%", "1.5% of P = 540", "P = 36,000"],
  why="₹7,200 divides 540 by the new rate 7.5%; ₹6,000 divides by the old rate 9%; ₹3,600 misplaces a zero.", secs=50)

P_ = F(16320) / (F(120, 100) * F(136, 100))
assert P_ == 10000 and r2(F(16320) / F(156, 100)) == F(1046154, 100) and F(16320) / F(136, 100) == 12000 and F(16320) / F(12, 10) == 13600
Q(T, "SI with changing rates", A,
  "Arjun invested a sum at 10% per annum simple interest. After 2 years he withdrew the whole amount and invested it "
  "at 12% per annum simple interest for 3 more years, receiving ₹16,320 at the end. What sum did he invest at the "
  "start?",
  "₹10,000", ["₹10,461.54", "₹12,000", "₹13,600"],
  "The amount after the first 2 years becomes the principal for the next 3 years",
  "After 2 years: P × (1 + 0.2) = 1.2P. After 3 more years at 12%: 1.2P × (1 + 0.36) = 1.632P = 16,320, so "
  "P = ₹10,000.",
  ["Stage 1: 1.2P", "Stage 2: 1.2P × 1.36 = 1.632P", "P = 16,320 ÷ 1.632 = 10,000"],
  why="₹10,461.54 earns the 12% only on the original sum (1.56P); ₹12,000 is the amount after the first stage; ₹13,600 "
      "undoes only the first stage.", secs=85)

# ================================================================ Compound Interest (B3 I3 A2)
T = "Compound Interest"
ci = 40000 * (F(1075, 1000) ** 2 - 1)
assert ci == 6225 and 40000 * F(15, 100) == 6000 and 40000 + ci == 46225
Q(T, "Annual compounding", B,
  "What is the compound interest on ₹40,000 for 2 years at 7.5% per annum, compounded annually?",
  "₹6,225", ["₹6,000", "₹46,225", "₹3,000"],
  "CI = P[(1 + r)ⁿ − 1]; for 2 years, CI = SI + interest on the first year's interest",
  "Year 1 interest: 7.5% of 40,000 = ₹3,000. Year 2 interest: 7.5% of 43,000 = ₹3,225. CI = 3,000 + 3,225 = ₹6,225.",
  ["Year 1: 3,000", "Year 2: 7.5% of 43,000 = 3,225", "CI = 6,225"],
  short="CI = 2 × 3,000 + 7.5% of 3,000 = 6,000 + 225 = 6,225.",
  why="₹6,000 is the simple interest; ₹46,225 is the amount, not the interest; ₹3,000 is one year's interest.",
  secs=40)

amt = 50000 * F(104, 100) ** 2
assert amt == 54080 and 50000 * F(108, 100) == 54000 and 50000 * F(108, 100) ** 2 == 58320
Q(T, "Half-yearly and quarterly", B,
  "What amount will ₹50,000 grow to in 1 year at 8% per annum compound interest, compounded half-yearly?",
  "₹54,080", ["₹54,000", "₹58,320", "₹4,080"],
  "Half-yearly: halve the rate (4%) and double the number of periods (2)",
  "Amount = 50,000 × 1.04² = 50,000 × 1.0816 = ₹54,080.",
  ["Rate per half-year = 4%", "2 half-years", "50,000 × 1.0816 = 54,080"],
  why="₹54,000 compounds annually (one period at 8%); ₹58,320 uses 8% per half-year; ₹4,080 is the interest, not the "
      "amount.", secs=40)

d_ = 12000 * F(15, 100) ** 2
assert d_ == 270 and 12000 * F(15, 100) == 1800 and 12000 * (F(115, 100) ** 2 - 1) == 3870
Q(T, "CI vs SI difference", B,
  "What is the difference between the compound interest (compounded annually) and the simple interest on ₹12,000 "
  "for 2 years at 15% per annum?",
  "₹270", ["₹1,800", "₹135", "₹3,870"],
  "For 2 years, CI − SI = P × (r/100)²",
  "Difference = 12,000 × 0.15² = 12,000 × 0.0225 = ₹270. (SI = ₹3,600, CI = ₹3,870.)",
  ["CI − SI = P(r/100)²", "12,000 × 0.0225 = 270"],
  why="₹1,800 is one year's interest; ₹135 halves the correct difference; ₹3,870 is the compound interest itself.",
  secs=35)

amt = 10000 * F(11, 10) ** 2 + 10000 * F(11, 10)
assert amt == 23100 and 10000 * F(12, 10) + 10000 * F(11, 10) == 23000 and 2 * 10000 * F(11, 10) ** 2 == 24200
Q(T, "Instalments", I,
  "Meena deposits ₹10,000 at the start of each of two consecutive years in a scheme paying 10% per annum compound "
  "interest, compounded annually. What is the total in her account at the end of the second year?",
  "₹23,100", ["₹23,000", "₹24,200", "₹22,000"],
  "Each deposit grows for the number of years it stays in the account",
  "The first ₹10,000 stays 2 years: 10,000 × 1.1² = ₹12,100. The second stays 1 year: 10,000 × 1.1 = ₹11,000. "
  "Total = ₹23,100.",
  ["First deposit: 10,000 × 1.21 = 12,100", "Second deposit: 10,000 × 1.1 = 11,000", "Total = 23,100"],
  why="₹23,000 uses simple interest on the first deposit (12,000); ₹24,200 grows both deposits for 2 years; ₹22,000 "
      "grows both deposits for only 1 year.", secs=55)

bal = (21000 * F(11, 10) - 11000) * F(11, 10)
assert bal == 13310 and 21000 * F(11, 10) - 11000 == 12100 and 21000 * F(121, 100) - 11000 == 14410 and 21000 * F(12, 10) - 11000 == 14200
Q(T, "Instalments", I,
  "Ravi borrows ₹21,000 at 10% per annum compound interest, compounded annually. He repays ₹11,000 at the end of "
  "the first year. How much must he pay at the end of the second year to clear the loan?",
  "₹13,310", ["₹12,100", "₹14,410", "₹14,200"],
  "Interest is charged each year on the balance outstanding at the start of that year",
  "End of year 1: 21,000 × 1.1 = ₹23,100; after paying ₹11,000 the balance is ₹12,100. End of year 2: "
  "12,100 × 1.1 = ₹13,310.",
  ["Year 1: 21,000 × 1.1 = 23,100", "Balance = 23,100 − 11,000 = 12,100", "Year 2: 12,100 × 1.1 = 13,310"],
  why="₹12,100 forgets the second year's interest; ₹14,410 grows the whole loan for 2 years but gives no interest "
      "credit for the ₹11,000 paid early; ₹14,200 uses simple interest on ₹21,000 for 2 years.", secs=60)

rates = [r for r in range(1, 100) if F(100 + r, 100) ** 2 == F(36, 25)]
assert rates == [20]
Q(T, "Annual compounding", I,
  "A sum is invested at compound interest, compounded annually. The amounts after 3 years and after 5 years are in "
  "the ratio 25 : 36. What is the rate of interest per annum?",
  "20%", ["44%", "22%", "11%"],
  "Between year 3 and year 5 the amount is multiplied by (1 + r)², whatever the principal",
  "A₅ ÷ A₃ = (1 + r)² = 36/25, so 1 + r = 6/5 and r = 20%.",
  ["A₅ / A₃ = (1 + r)²", "(1 + r)² = 36/25", "1 + r = 6/5 ⇒ r = 20%"],
  why="44% is the growth over the two years, not per year; 22% halves the 44% as if it were simple interest; 11% "
      "takes the difference 36 − 25 as the rate.", secs=55, by=BRUTE)

q_ = F(103, 100) ** 4
diff_ = 100000 * (q_ - F(1125, 1000))
assert r2(diff_) == F(5088, 100) and 100000 * (F(125, 1000) - F(12, 100)) == 500
Q(T, "Half-yearly and quarterly", A,
  "Deposit X pays 12% per annum compounded quarterly; deposit Y pays 12.5% per annum compounded annually. On "
  "₹1,00,000 for one year, which deposit earns more interest, and by how much (to the nearest paisa)?",
  "X earns ₹50.88 more", ["Y earns ₹500 more", "Y earns ₹50.88 more", "Both earn the same interest"],
  "Compare effective annual rates: quarterly 12% means 3% per quarter for 4 quarters",
  "X: 1,00,000 × 1.03⁴ = 1,00,000 × 1.12550881 = ₹1,12,550.88, interest ₹12,550.88. Y: interest = ₹12,500. X earns "
  "₹50.88 more.",
  ["1.03² = 1.0609", "1.03⁴ = 1.0609² = 1.12550881", "X: 12,550.88", "Y: 12,500", "X − Y = 50.88"],
  why="'Y earns ₹500 more' compares 12% and 12.5% and ignores quarterly compounding; 'Y earns ₹50.88 more' gets the "
      "direction wrong; 'the same' assumes 12% quarterly equals 12.5% annually.", secs=95)

r_ = F(2 * (3150 - 3000), 3000)
P_ = F(3000) / (2 * r_)
ci3 = P_ * ((1 + r_) ** 3 - 1)
assert r_ == F(1, 10) and P_ == 15000 and ci3 == 4965 and P_ * 3 * r_ == 4500 and F(3150) * F(3, 2) == 4725 and 3150 + 1500 == 4650
Q(T, "CI vs SI difference", A,
  "On a certain sum, the simple interest for 2 years is ₹3,000 and the compound interest (compounded annually) for "
  "2 years at the same rate is ₹3,150. What is the compound interest on the same sum for 3 years at that rate?",
  "₹4,965", ["₹4,500", "₹4,725", "₹4,650"],
  "CI − SI for 2 years is the interest on one year's interest: it gives the rate, and then the sum",
  "One year's SI = ₹1,500. CI − SI = 150 = interest on 1,500 for a year, so r = 10%. Sum = 1,500 ÷ 0.1 = ₹15,000. "
  "CI for 3 years = 15,000 × (1.1³ − 1) = 15,000 × 0.331 = ₹4,965.",
  ["r = 150 ÷ 1,500 = 10%", "P = 1,500 ÷ 0.1 = 15,000", "CI₃ = 15,000 × 0.331 = 4,965"],
  short="Third-year interest = 10% of the amount after 2 years (18,150) = 1,815; 3,150 + 1,815 = 4,965.",
  why="₹4,500 is the simple interest for 3 years; ₹4,725 scales the 2-year CI by 3/2; ₹4,650 adds a third year's "
      "interest on the principal only (₹1,500).", secs=95)

# ================================================================ Partnership (B1 I3 A2)
T = "Partnership"
caps = [25000, 35000, 40000]
tot = F(6000) * sum(caps) / caps[0]
assert tot == 24000 and F(6000) * sum(caps) / caps[2] == 15000 and 24000 * F(35, 100) == 8400
Q(T, "Simple partnership", B,
  "A, B and C invest ₹25,000, ₹35,000 and ₹40,000 in a business for the same period. A's share of the profit is "
  "₹6,000. What is the total profit?",
  "₹24,000", ["₹18,000", "₹15,000", "₹8,400"],
  "Shares are in the ratio of capitals, 25 : 35 : 40 = 5 : 7 : 8",
  "A's share is 25/100 of the profit, so the total profit = 6,000 × 100 ÷ 25 = ₹24,000.",
  ["Capitals 25 : 35 : 40", "A's fraction = 25/100", "Total = 6,000 ÷ 0.25 = 24,000"],
  why="₹18,000 assumes equal shares (3 × 6,000); ₹15,000 uses C's capital in place of A's; ₹8,400 is B's share.",
  secs=40)

a_ = 30000 * 12
b_ = 20000 * 6 + 35000 * 6
share = F(46000) * a_ / (a_ + b_)
assert (a_, b_) == (360000, 330000) and share == 24000 and F(46000) * F(3, 5) == 27600
Q(T, "Compound partnership", I,
  "A invests ₹30,000 in a business for a whole year. B invests ₹20,000 for the first 6 months and raises it to "
  "₹35,000 for the next 6 months. Out of a year's profit of ₹46,000, what is A's share?",
  "₹24,000", ["₹22,000", "₹27,600", "₹23,000"],
  "Profit shares are in the ratio of capital × time, adding B's two periods",
  "A: 30,000 × 12 = 3,60,000. B: 20,000 × 6 + 35,000 × 6 = 3,30,000. Ratio 12 : 11, so A gets 46,000 × 12/23 = "
  "₹24,000.",
  ["A = 3,60,000", "B = 1,20,000 + 2,10,000 = 3,30,000", "Ratio 12 : 11", "A = 46,000 × 12/23 = 24,000"],
  why="₹22,000 is B's share; ₹27,600 uses only the starting capitals 30 : 20; ₹23,000 splits the profit equally.",
  secs=60)

sol = [p for p in range(24000, 400001, 1000) if 24000 + F(3, 7) * (p - 24000) == F(4, 7) * (p - 24000)]
assert sol == [192000]
Q(T, "Working partner", I,
  "A and B are partners, and A's capital is three-fourths of B's. A manages the business and draws a salary of "
  "₹2,000 a month out of the profit; the rest of the profit is shared in the ratio of capitals. At the end of the "
  "year A and B receive equal amounts in all. What was the year's profit?",
  "₹1,92,000", ["₹1,68,000", "₹16,000", "₹1,44,000"],
  "A's salary must make up exactly the gap between B's and A's capital shares",
  "Salary for the year = ₹24,000. The remainder R is shared 3 : 4, so B gets R/7 more than A. Equal totals mean "
  "R/7 = 24,000, so R = 1,68,000 and the profit = 1,68,000 + 24,000 = ₹1,92,000.",
  ["Salary = 12 × 2,000 = 24,000", "Rest R shared 3 : 4", "R/7 = 24,000 ⇒ R = 1,68,000", "Profit = 1,92,000"],
  why="₹1,68,000 is only the part shared in the capital ratio; ₹16,000 takes the salary as ₹2,000 for the whole year; "
      "₹1,44,000 takes the gap between the shares as R/6 instead of R/7.", secs=70, by=BRUTE)

cap, prof = [2, 3, 4], [4, 3, 2]
tm = [F(p, c) for p, c in zip(prof, cap)]
months_A = 3 * tm[0] / tm[2]
assert tm == [2, 1, F(1, 2)] and months_A == 12 and 3 * tm[1] / tm[2] == 6 and 3 * F(2, 4) / F(4, 2) == F(3, 4)
Q(T, "Compound partnership", I,
  "The capitals of A, B and C are in the ratio 2 : 3 : 4 and their profits at the end of the business are in the "
  "ratio 4 : 3 : 2. If C's capital was invested for 3 months, for how many months was A's capital invested?",
  "12 months", ["6 months", "¾ month", "3 months"],
  "Profit ∝ capital × time, so time ∝ profit ÷ capital",
  "Times are in the ratio 4/2 : 3/3 : 2/4 = 2 : 1 : ½ = 4 : 2 : 1. C's 3 months is 1 part, so A's time is 4 × 3 = "
  "12 months.",
  ["Time ∝ profit ÷ capital", "A : B : C = 2 : 1 : ½ = 4 : 2 : 1", "C = 3 months ⇒ A = 12 months"],
  why="6 months is B's period; ¾ month divides capital by profit instead of profit by capital; 3 months assumes "
      "everyone invested for the same time.", secs=60)

A_units = sum(c * 4 for c in (40000, 50000, 60000))
B_units = sum(c * 4 for c in (50000, 40000, 30000))
share = F(108000) * A_units / (A_units + B_units)
assert (A_units, B_units) == (600000, 480000) and share == 60000 and F(108000) * F(4, 9) == 48000 and F(108000) * F(2, 3) == 72000
Q(T, "Compound partnership", A,
  "A and B start a business with ₹40,000 and ₹50,000. At the end of every 4 months, A adds ₹10,000 to his capital "
  "while B withdraws ₹10,000 from his. Out of a profit of ₹1,08,000 at the end of the year, what is A's share?",
  "₹60,000", ["₹48,000", "₹54,000", "₹72,000"],
  "Split the year into three 4-month periods and add capital × time for each partner",
  "A: (40,000 + 50,000 + 60,000) × 4 = 6,00,000. B: (50,000 + 40,000 + 30,000) × 4 = 4,80,000. Ratio 5 : 4, so A "
  "gets 1,08,000 × 5/9 = ₹60,000.",
  ["A: 40k, 50k, 60k for 4 months each = 6,00,000", "B: 50k, 40k, 30k for 4 months each = 4,80,000", "Ratio 5 : 4",
   "A = 60,000"],
  why="₹48,000 uses the starting capitals 4 : 5 (it is also B's correct share); ₹54,000 splits equally; ₹72,000 uses "
      "the final capitals 60,000 : 30,000.", secs=95)

units_A = 40000 * 12
total_units = units_A * 3
c_cap = total_units * F(5, 12) / 6
assert total_units == 1440000 and total_units * F(1, 4) / 9 == 40000 and c_cap == 100000 and total_units * F(5, 12) / 12 == 50000 and units_A / 6 == 80000
Q(T, "Compound partnership", A,
  "In a business, A gets one-third of the profit, B gets one-fourth and C gets the rest. A invested ₹40,000 for 12 "
  "months, B invested for 9 months and C invested for 6 months. How much did C invest?",
  "₹1,00,000", ["₹50,000", "₹40,000", "₹80,000"],
  "Profit shares are proportional to capital × months; A's share fixes the value of one share",
  "A's capital × time = 40,000 × 12 = 4,80,000, which is 1/3 of the total, so the total is 14,40,000. C's share is "
  "1 − 1/3 − 1/4 = 5/12, i.e. 6,00,000. Over 6 months, C's capital = 6,00,000 ÷ 6 = ₹1,00,000.",
  ["A: 4,80,000 = 1/3 of total ⇒ total 14,40,000", "C's fraction = 5/12 ⇒ 6,00,000", "C = 6,00,000 ÷ 6 = 1,00,000"],
  short="B's capital works out to 3,60,000 ÷ 9 = ₹40,000 by the same method.",
  why="₹50,000 divides C's 6,00,000 by 12 months instead of 6; ₹40,000 is B's capital (and A's); ₹80,000 gives C "
      "one-third of the profit, like A.", secs=100)

# ================================================================ Mixture and Alligation (B2 I2 A1)
T = "Mixture and Alligation"
rat = (F(41, 2) - 18) / (22 - F(41, 2))
assert rat == F(5, 3) and F(5 * 22 + 3 * 18, 8) == F(41, 2)
Q(T, "Alligation rule", B,
  "In what ratio must 22-carat gold be mixed with 18-carat gold to get 20.5-carat gold?",
  "5 : 3", ["3 : 5", "1 : 1", "11 : 9"],
  "Alligation: (mean − cheaper) : (dearer − mean) gives dearer : cheaper",
  "22-carat : 18-carat = (20.5 − 18) : (22 − 20.5) = 2.5 : 1.5 = 5 : 3.",
  ["Dearer 22, cheaper 18, mean 20.5", "2.5 : 1.5", "= 5 : 3"],
  why="3 : 5 reverses the alligation ratio; 1 : 1 would give 20 carat, not 20.5; 11 : 9 is just the ratio 22 : 18 of "
      "the purities.", secs=35)

total_new = F(6) / F(12, 100)
assert total_new == 50 and total_new - 30 == 20 and F(8, 100) * 30 == F(12, 5) and F(88, 100) * total_new == 44
Q(T, "Mixing solutions", B,
  "A 30-litre mixture of milk and water contains 20% water. How much pure milk must be added so that water makes "
  "up only 12% of the mixture?",
  "20 litres", ["2.4 litres", "50 litres", "44 litres"],
  "The quantity of water stays fixed; find the new total in which it is 12%",
  "Water = 20% of 30 = 6 litres. For 6 litres to be 12% of the mixture, the mixture must be 6 ÷ 0.12 = 50 litres. "
  "Milk to add = 50 − 30 = 20 litres.",
  ["Water = 6 L (unchanged)", "New total = 6 ÷ 0.12 = 50 L", "Add 50 − 30 = 20 L of milk"],
  why="2.4 litres takes 8% (20 − 12) of 30; 50 litres is the new total, not the milk added; 44 litres is all the milk "
      "in the final mixture.", secs=40)

t1 = (F(25, 2) - 5) / (20 - 5) * 4
assert t1 == 2 and 20 * t1 + 5 * (4 - t1) == 50 and 5 * (4 - t1) == 10
Q(T, "Alligation rule", I,
  "A man covers 50 km in 4 hours, partly by cycle at 20 km/h and the rest on foot at 5 km/h. How many kilometres "
  "does he cover by cycle?",
  "40 km", ["10 km", "25 km", "20 km"],
  "Alligation on speeds gives the ratio of the TIMES spent at each speed (average speed 12.5 km/h)",
  "Average speed = 50 ÷ 4 = 12.5 km/h. Time on cycle : time on foot = (12.5 − 5) : (20 − 12.5) = 1 : 1, i.e. 2 hours "
  "each. Distance by cycle = 20 × 2 = 40 km.",
  ["Mean speed = 12.5 km/h", "Times = 7.5 : 7.5 = 1 : 1 ⇒ 2 h each", "Cycle: 20 × 2 = 40 km"],
  why="10 km is the distance on foot; 25 km applies the 1 : 1 ratio to distances instead of times; 20 km assumes he "
      "cycled for only 1 hour.", secs=55)

xs_ = [x for x in range(0, 200) if F(6 + x, 40 + x) == F(32, 100)]
assert xs_ == [10] and F(17, 100) * 40 == F(68, 10) and F(32, 100) * 40 == F(128, 10) and 40 * F(68, 17) == 160
Q(T, "Mixing solutions", I,
  "How many litres of pure alcohol must be added to 40 litres of a 15% alcohol solution to make it a 32% solution?",
  "10 litres", ["6.8 litres", "12.8 litres", "160 litres"],
  "Alligation of 15% and 100%: (100 − 32) : (32 − 15) = solution : pure alcohol",
  "Solution : pure = 68 : 17 = 4 : 1, so pure alcohol = 40 ÷ 4 = 10 litres. Check: (6 + 10) ÷ 50 = 32% ✓.",
  ["Alcohol now = 6 L", "(6 + x) ÷ (40 + x) = 0.32", "0.68x = 6.8 ⇒ x = 10"],
  why="6.8 litres adds 17% of 40 and forgets that the volume grows; 12.8 litres is 32% of 40, the alcohol needed if "
      "the volume stayed 40; 160 litres reverses the alligation ratio.", secs=55, by=BRUTE)

c1 = (80 * F(30, 100) + 20 * F(50, 100)) / 100
c2 = (80 * c1 + 20 * F(50, 100)) / 100
assert c1 == F(34, 100) and c2 == F(372, 1000)
Q(T, "Replacement of mixture", A,
  "A tank holds 100 litres of a 30% sugar syrup. Twenty litres are drawn off and replaced with a 50% sugar syrup, and "
  "then this is done once more. What is the sugar concentration of the final syrup?",
  "37.2%", ["34%", "38%", "40%"],
  "Each operation keeps 80% of the existing syrup and adds 20 litres at 50%",
  "After the first operation: 80 litres at 30% (24 L sugar) + 20 litres at 50% (10 L) = 34 L sugar, i.e. 34%. After the "
  "second: 80 litres at 34% (27.2 L) + 10 L = 37.2 L sugar in 100 litres = 37.2%.",
  ["Op 1: 24 + 10 = 34 L ⇒ 34%", "Op 2: 0.8 × 34 + 10 = 37.2 L ⇒ 37.2%"],
  short="The gap to 50% shrinks by 20% each time: 20 → 16 → 12.8, so 50 − 12.8 = 37.2%.",
  why="34% stops after one operation; 38% assumes each operation adds the same 4 points; 40% simply averages 30% and "
      "50%.", secs=80)

# ================================================================ Time and Work (B1 I2 A3)
T = "Time and Work"
per_house = F(6 * 8, 3)
d_ = per_house * 2 / 4
assert per_house == 16 and d_ == 8 and F(6 * 8, 4) == 12 and 8 * F(2, 3) == F(16, 3) and F(6, 4) * F(3, 2) * 8 == 18
Q(T, "Work efficiency", B,
  "6 painters can paint 3 identical houses in 8 days. In how many days can 4 painters paint 2 such houses?",
  "8 days", ["12 days", "5⅓ days", "18 days"],
  "Work = painters × days; one house needs a fixed number of painter-days",
  "3 houses need 6 × 8 = 48 painter-days, so one house needs 16. Two houses need 32 painter-days; with 4 painters "
  "that is 32 ÷ 4 = 8 days.",
  ["3 houses = 48 painter-days", "1 house = 16 painter-days", "2 houses = 32 ⇒ 32 ÷ 4 = 8 days"],
  short="M₁D₁/W₁ = M₂D₂/W₂: 6 × 8/3 = 4 × D/2 ⇒ D = 8.",
  why="12 days ignores the drop from 3 houses to 2; 5⅓ days ignores the drop from 6 painters to 4; 18 days applies "
      "the house ratio upside down (8 × 6/4 × 3/2).", secs=40)

rem = 1 - F(3, 12)
t_both = rem / (F(1, 12) + F(1, 18))
b_share = t_both / 18 * 3600
assert t_both == F(27, 5) and b_share == 1080 and F(3600 * 2, 5) == 1440 and 3600 - b_share == 2520
Q(T, "Work and wages", I,
  "A can finish a job in 12 days and B in 18 days. A works alone for the first 3 days, and then A and B together "
  "finish the job. The payment of ₹3,600 is shared in proportion to the work each did. What is B's share?",
  "₹1,080", ["₹1,440", "₹1,800", "₹2,520"],
  "Find how long B worked, then B's share of the work = days worked ÷ B's time for the whole job",
  "A does 3/12 = 1/4 alone. The remaining 3/4 at the joint rate 1/12 + 1/18 = 5/36 per day takes 27/5 = 5.4 days. B "
  "worked 5.4 days, i.e. 5.4/18 = 0.3 of the job, so B gets 0.3 × 3,600 = ₹1,080.",
  ["A alone: 1/4 done", "Rest 3/4 ÷ 5/36 = 5.4 days", "B's work = 5.4/18 = 0.3", "B = 0.3 × 3,600 = 1,080"],
  why="₹1,440 splits the money in the ratio of efficiencies 3 : 2, ignoring A's 3 days alone; ₹1,800 splits it "
      "equally; ₹2,520 is A's share.", secs=75)

work, day, rates = F(0), 0, [F(1, 8), F(1, 12), F(1, 16)]
while work < 1:
    work += rates[day % 3]
    day += 1
assert day == 11 and sum(rates) == F(13, 48)
Q(T, "Alternate days", I,
  "A, B and C can finish a job alone in 8, 12 and 16 days respectively. They work one at a time in turn: A on the "
  "1st day, B on the 2nd, C on the 3rd, A on the 4th, and so on. On which day is the job completed?",
  "11th day", ["10th day", "12th day", "9th day"],
  "Take the work as 48 units: A does 6, B 4 and C 3 units a day, i.e. 13 units per 3-day cycle",
  "Three cycles (9 days) complete 39 units, leaving 9. Day 10 (A) does 6 → 45 units. Day 11 (B) needs only 3 of its "
  "4 units, so the job is completed on the 11th day.",
  ["Total = 48 units; A 6, B 4, C 3", "9 days: 3 × 13 = 39", "Day 10 (A): 45", "Day 11 (B): 48 ✓"],
  why="10th day leaves 3 units undone after A's turn; 12th day overshoots by a full day; 9th day leaves 9 units after "
      "three complete cycles.", secs=65, by=BRUTE)

man, woman = F(1, 12 * 18), F(1, 18 * 20)
done = 6 * man * 12
more = (1 - done) / (6 * man + 10 * woman)
assert man == F(5, 1080) and woman == F(3, 1080) and done == F(1, 3) and more == 12
assert (1 - done) / (16 * man) == 9 and 1 / (6 * man) == 36
Q(T, "Men-women-children", A,
  "12 men can finish a job in 18 days, and 18 women can finish it in 20 days. 6 men start the job and work alone "
  "for 12 days; then 10 women join them. In how many days in all is the job finished?",
  "24 days", ["12 days", "21 days", "36 days"],
  "Convert men and women to work units per day using a common total",
  "Take the job as 1,080 units: a man does 1,080 ÷ 216 = 5 units a day and a woman 1,080 ÷ 360 = 3. Six men in "
  "12 days do 6 × 5 × 12 = 360 units, leaving 720. With 10 women, the daily output is 30 + 30 = 60 units, so 720 "
  "units take 12 more days. Total = 12 + 12 = 24 days.",
  ["Man = 5 units/day, woman = 3 units/day (job = 1,080)", "First 12 days: 360 units", "Then 60 units/day: 720 ÷ 60 "
   "= 12 days", "Total = 24 days"],
  why="12 days counts only the time after the women join; 21 days treats a woman as working as fast as a man "
      "(720 ÷ 80 = 9 more days); 36 days is the time for the 6 men working alone throughout.", secs=100)

T_ = next(t for t in range(1, 60) if F(t - 5, 20) + F(t, 30) == 1)
a_share = F(T_ - 5, 20) * 15000
assert T_ == 15 and a_share == 7500 and F(15000 * 3, 5) == 9000 and F(15000 * 10, 15) == 10000
Q(T, "Work and wages", A,
  "A and B can finish a job alone in 20 and 30 days. They start together, but A leaves 5 days before the job is "
  "finished. The payment of ₹15,000 is shared in proportion to the work done. What is A's share?",
  "₹7,500", ["₹9,000", "₹6,000", "₹10,000"],
  "If the job takes T days, B works T days and A works T − 5 days",
  "(T − 5)/20 + T/30 = 1 ⇒ 3(T − 5) + 2T = 60 ⇒ T = 15. A worked 10 days and did 10/20 = 1/2 of the job, so A's "
  "share = ₹7,500.",
  ["(T − 5)/20 + T/30 = 1", "5T = 75 ⇒ T = 15", "A's work = 10/20 = 1/2", "A = ½ × 15,000 = 7,500"],
  why="₹9,000 splits by the efficiencies 3 : 2 as if both worked throughout; ₹6,000 splits by days worked 10 : 15; "
      "₹10,000 gives A 10/15 of the money (his days as a share of the total time).", secs=95, by=BRUTE)


def alt_days(a, b, first):
    work, day = F(0), F(0)
    rates = [a, b] if first == "A" else [b, a]
    k = 0
    while True:
        r = rates[k % 2]
        if work + r >= 1:
            return day + (1 - work) / r
        work += r
        day += 1
        k += 1


sols = [d for d in range(2, 80) if alt_days(F(1, d), F(1, 2 * d), "A") == 17 and alt_days(F(1, d), F(1, 2 * d), "B") == F(35, 2)]
assert sols == [13] and 1 / (F(1, 13) + F(1, 26)) == F(26, 3)
assert alt_days(F(1, 17), F(1, 17), "A") == 17
Q(T, "Alternate days", A,
  "A and B work on a job on alternate days. If A works on the first day, the job is finished in exactly 17 days. If "
  "B works on the first day, it is finished in 17½ days. In how many days can A alone finish the job?",
  "13 days", ["26 days", "17 days", "8⅔ days"],
  "Count the working days of each person in both orders and compare",
  "A first: A works 9 days and B 8 days, so 9a + 8b = 1. B first: B works 9 days, A 8 days and A works half of the "
  "18th day, so 9b + 8.5a = 1. Equating, 9a + 8b = 8.5a + 9b ⇒ 0.5a = b. Then 9a + 4a = 13a = 1, so A takes 13 days.",
  ["A first: 9a + 8b = 1", "B first: 8.5a + 9b = 1", "⇒ b = a/2", "13a = 1 ⇒ A = 13 days"],
  why="26 days is B's time; 17 days assumes A and B are equally fast; 8⅔ days is the time for A and B working "
      "together.", secs=110, by=BRUTE)

# ================================================================ Pipes and Cisterns (B1 I2 A1)
T = "Pipes and Cisterns"
done = 6 * (F(1, 20) + F(1, 30))
rest = (1 - done) * 30
assert done == F(1, 2) and rest == 15 and 1 / (F(1, 20) + F(1, 30)) == 12 and (1 - done) * 20 == 10
Q(T, "Inlet and outlet", B,
  "Pipes A and B can fill a tank in 20 minutes and 30 minutes. Both are opened on the empty tank, and after 6 "
  "minutes pipe A is closed. How long does it take in all to fill the tank?",
  "21 minutes", ["15 minutes", "12 minutes", "16 minutes"],
  "Work out the part filled while both run, then the time B alone needs for the rest",
  "Together they fill 1/20 + 1/30 = 1/12 per minute, so in 6 minutes they fill 1/2. B fills the other half in "
  "½ × 30 = 15 minutes. Total = 6 + 15 = 21 minutes.",
  ["Joint rate = 1/12 per min", "6 min ⇒ 1/2 full", "B: ½ × 30 = 15 min", "Total = 21 min"],
  why="15 minutes is only B's time after A closes; 12 minutes is the time if both stay open; 16 minutes uses A's "
      "rate for the second half (6 + 10).", secs=40)

cap = 3 / (F(1, 12) - F(1, 16))
assert cap == 144 and 3 * 16 == 48 and 3 * 12 == 36 and 3 * 12 * 16 == 576
Q(T, "Inlet and outlet", I,
  "Pipes A and B can each fill a tank on their own, in 12 minutes and 16 minutes respectively. Pipe A delivers 3 "
  "litres per minute more than pipe B. What is the capacity of the tank?",
  "144 litres", ["48 litres", "36 litres", "576 litres"],
  "Rate = capacity ÷ time; the difference of the two rates is 3 litres per minute",
  "C/12 − C/16 = C/48 = 3, so C = 144 litres. (A: 12 L/min, B: 9 L/min.)",
  ["A's rate = C/12, B's rate = C/16", "C/12 − C/16 = C/48 = 3", "C = 144 L"],
  why="48 litres is 3 × 16; 36 litres is 3 × 12; 576 litres is 3 × 12 × 16 without dividing by the 4-minute gap "
      "between the two times.", secs=55, by=BRUTE)

t_ = F(3, 2) + F(1, 2) / (4 * F(1, 3))
assert t_ == F(15, 8) and F(3, 2) + F(1, 2) / (3 * F(1, 3)) == 2 and 1 / (4 * F(1, 3)) == F(3, 4)
Q(T, "Inlet and outlet", I,
  "A pipe can fill a tank in 3 hours. When the tank is half full, three more pipes of the same size are opened. How "
  "long does it take in all to fill the tank, starting from empty?",
  "1 hour 52½ minutes", ["2 hours", "45 minutes", "3 hours"],
  "The first half takes half the single pipe's time; then four pipes work together",
  "One pipe fills half the tank in 1.5 hours. Then 4 pipes fill at 4/3 of the tank per hour, so the other half takes "
  "½ ÷ 4/3 = 3/8 hour = 22½ minutes. Total = 1 h 30 min + 22½ min = 1 hour 52½ minutes.",
  ["First half: 1.5 h", "Then 4 pipes: rate 4/3 per hour", "Second half: 3/8 h = 22.5 min", "Total = 1 h 52.5 min"],
  why="2 hours counts only 3 pipes in all after the half-way point; 45 minutes assumes all four pipes run from the "
      "start; 3 hours ignores the extra pipes.", secs=55)

level, minute, rates_ = F(0), 0, [F(1, 20), F(1, 30), F(-1, 15)]
while level < 1:
    level = max(F(0), level + rates_[minute % 3])
    minute += 1
assert minute == 167 and sum(rates_) == F(1, 60) and 57 * 3 + 1 == 172
Q(T, "Inlet and outlet", A,
  "Pipes A and B can fill a tank in 20 minutes and 30 minutes, and pipe C can empty the full tank in 15 minutes. "
  "Starting with the tank empty, the pipes are opened one at a time for one minute each in the order A, B, C, A, B, "
  "C, … . After how many minutes is the tank first full?",
  "167 minutes", ["180 minutes", "172 minutes", "168 minutes"],
  "Net gain per 3-minute cycle is small, but the tank can fill during a B-minute before C empties it",
  "Take the tank as 60 units: A adds 3, B adds 2 and C removes 4 units, a net 1 unit per cycle. Within a cycle the "
  "level peaks after B at (start + 5). So the tank is full once start + 5 ≥ 60, i.e. after 55 complete cycles "
  "(165 minutes, level 55): A brings it to 58 and B to 60 at the 167th minute.",
  ["Tank = 60 units: A +3, B +2, C −4", "Net +1 per 3-minute cycle", "After 55 cycles (165 min): 55 units",
   "Minute 166 (A): 58; minute 167 (B): 60 ✓"],
  why="180 minutes divides 60 units by the net 1 unit per cycle and ignores the peak within a cycle; 172 minutes waits "
      "for an A-minute to finish the job; 168 minutes counts the whole 56th cycle.", secs=110, by=BRUTE)

# ================================================================ Speed, Time and Distance (B2 I3 A1)
T = "Speed, Time and Distance"
speeds = [35 + 2 * k for k in range(12)]
assert sum(speeds) == 552 and F(sum(speeds), 12) == 46 and speeds[-1] == 57 and F(35 + 59, 2) == 47
Q(T, "Average speed", B,
  "A car covers 35 km in the first hour of a journey, and its speed rises by 2 km/h every hour after that. What is "
  "its average speed over the first 12 hours?",
  "46 km/h", ["57 km/h", "35 km/h", "47 km/h"],
  "The hourly distances form an arithmetic progression; the average equals (first + last) ÷ 2",
  "The 12 hourly distances are 35, 37, …, 57 km. Total = 12 × (35 + 57) ÷ 2 = 552 km, so the average speed is "
  "552 ÷ 12 = 46 km/h.",
  ["Last hour: 35 + 11 × 2 = 57", "Total = 6 × (35 + 57) = 552 km", "Average = 552 ÷ 12 = 46 km/h"],
  why="57 km/h is the speed in the last hour; 35 km/h is the speed in the first hour; 47 km/h counts 12 increases "
      "instead of 11 (last speed 59).", secs=45)

t_ = F(75, 12 + 18)
assert t_ == F(5, 2) and F(75, 6) == F(25, 2) and F(75, 12) == F(25, 4) and F(75, 18) == F(25, 6)
Q(T, "Relative speed", B,
  "Two cyclists start from the same point at the same time and ride in opposite directions at 12 km/h and 18 km/h. "
  "After how long will they be 75 km apart?",
  "2 hours 30 minutes", ["12 hours 30 minutes", "6 hours 15 minutes", "4 hours 10 minutes"],
  "Moving apart in opposite directions, the gap grows at the sum of the speeds",
  "The gap grows at 12 + 18 = 30 km/h, so 75 km takes 75 ÷ 30 = 2.5 hours = 2 hours 30 minutes.",
  ["Relative speed = 30 km/h", "75 ÷ 30 = 2.5 h"],
  why="12 h 30 min uses the difference of speeds (6 km/h); 6 h 15 min uses only the slower speed; 4 h 10 min uses "
      "only the faster speed.", secs=35)

first, second = F(100 - 20, 40), F(100 + 20, 40)
assert (first, second) == (2, 3) and F(100, 40) == F(5, 2) and F(100, 25) == 4
Q(T, "Meeting and overtaking", I,
  "At 6:00 AM, P and Q start walking towards each other from two places 100 km apart, at 15 km/h and 25 km/h. They "
  "keep walking after they meet. At what time will they be 20 km apart for the second time?",
  "9:00 AM", ["8:00 AM", "8:30 AM", "10:00 AM"],
  "They are 20 km apart once before meeting and once after crossing; the closing speed is 40 km/h throughout",
  "Before meeting, the gap is 20 km after covering 80 km together: 80 ÷ 40 = 2 h (8:00 AM). After crossing, they "
  "are 20 km apart when together they have covered 120 km: 120 ÷ 40 = 3 h, i.e. at 9:00 AM.",
  ["Combined speed = 40 km/h", "1st time: 80 ÷ 40 = 2 h ⇒ 8:00 AM", "2nd time: 120 ÷ 40 = 3 h ⇒ 9:00 AM"],
  why="8:00 AM is the first time they are 20 km apart; 8:30 AM is when they meet; 10:00 AM uses only Q's speed "
      "(100 ÷ 25 = 4 h).", secs=60)

w = 1 / (F(1, 24) - F(1, 40))
assert w == 60 and 1 / (F(1, 24) + F(1, 40)) == 15 and F(24 + 40, 2) == 32
Q(T, "Relative speed", I,
  "A man walking up a moving escalator reaches the top in 24 seconds. Standing still on the moving escalator, he "
  "reaches the top in 40 seconds. How long would he take to walk up the escalator if it were not moving?",
  "60 seconds", ["15 seconds", "32 seconds", "16 seconds"],
  "Speeds add: walking speed + escalator speed = his speed on the moving escalator",
  "Per second he covers 1/24 of the escalator walking on it while it moves, and the escalator alone covers 1/40. "
  "His own walking covers 1/24 − 1/40 = 1/60 per second, so he would take 60 seconds.",
  ["Walk + escalator = 1/24 per s", "Escalator = 1/40 per s", "Walk = 1/24 − 1/40 = 1/60 ⇒ 60 s"],
  why="15 seconds adds the two rates instead of subtracting; 32 seconds averages the two times; 16 seconds subtracts "
      "the times (40 − 24).", secs=55)

used = 2 + F(150, 75)
need = F(100) / (F(350, 50) - used)
assert used == 4 and need == F(100, 3) and 3 * 50 - 50 - 75 == 25 and F(350 - 150, 3) == F(200, 3)
Q(T, "Average speed", I,
  "A car travels for the first 2 hours at 50 km/h and then covers the next 150 km at 75 km/h. At what speed must it "
  "cover the remaining 100 km so that its average speed for the whole 350 km is 50 km/h?",
  "33⅓ km/h", ["25 km/h", "50 km/h", "66⅔ km/h"],
  "Average speed = total distance ÷ total time; find the time left for the last part",
  "The whole 350 km at 50 km/h must take 7 hours. The first part (100 km) took 2 hours and the second 150 ÷ 75 = 2 "
  "hours. So 100 km must be covered in 3 hours, at 100 ÷ 3 = 33⅓ km/h.",
  ["Total time allowed = 350 ÷ 50 = 7 h", "Used: 2 + 2 = 4 h", "Last 100 km in 3 h ⇒ 33⅓ km/h"],
  why="25 km/h averages the three speeds; 50 km/h assumes the last part must match the target average; 66⅔ km/h "
      "forgets that the first 2 hours covered 100 km (200 km left in 3 h).", secs=65)

gap = F(40 * 20, 60)
interval = gap / (40 + 20) * 60
assert interval == F(40, 3) and gap / (40 - 20) * 60 == 40 and F(20 * 20, 40) == 10
Q(T, "Meeting and overtaking", A,
  "Buses leave town X for town Y every 20 minutes and run at 40 km/h. A man rides a scooter from Y towards X at "
  "20 km/h along the same road. How often does he meet a bus coming towards him?",
  "Every 13⅓ minutes", ["Every 20 minutes", "Every 40 minutes", "Every 10 minutes"],
  "Successive buses are a fixed distance apart; he closes that gap at the sum of the speeds",
  "Buses 20 minutes apart at 40 km/h are 40 × ⅓ = 13⅓ km apart. Moving towards them, the man closes the gap at "
  "40 + 20 = 60 km/h, so he meets a bus every 13⅓ ÷ 60 hour = 13⅓ minutes.",
  ["Gap between buses = 40 × 20/60 = 13⅓ km", "Closing speed = 60 km/h", "13⅓ ÷ 60 h = 13⅓ min"],
  why="'Every 20 minutes' ignores his own motion; 'every 40 minutes' uses the difference of speeds, as if he rode in "
      "the same direction as the buses; 'every 10 minutes' scales 20 minutes by the speed ratio 20 : 40.", secs=95)

# ================================================================ Boats and Streams (B1 I1 A1)
T = "Boats and Streams"
up, down = F(2) / F(40, 60), F(2) / F(24, 60)
assert (up, down) == (3, 5) and (up + down) / 2 == 4 and (down - up) / 2 == 1 and F(4) / F(64, 60) == F(15, 4)
Q(T, "Upstream and downstream", B,
  "A swimmer swims 2 km against the current in 40 minutes and swims back the same 2 km with the current in 24 "
  "minutes. What is her speed in still water?",
  "4 km/h", ["1 km/h", "8 km/h", "3.75 km/h"],
  "Still-water speed = (downstream speed + upstream speed) ÷ 2",
  "Upstream: 2 km in 40 min = 3 km/h. Downstream: 2 km in 24 min = 5 km/h. Still-water speed = (5 + 3) ÷ 2 = "
  "4 km/h.",
  ["Upstream = 2 ÷ (2/3) = 3 km/h", "Downstream = 2 ÷ (2/5) = 5 km/h", "(5 + 3) ÷ 2 = 4 km/h"],
  why="1 km/h is the speed of the current; 8 km/h adds the two speeds without halving; 3.75 km/h is her average "
      "speed for the round trip (4 km in 64 minutes).", secs=40)

s_ = F(24, 3) / 4
b_ = 3 * s_
total = F(24, b_ + s_) + F(24, b_ - s_)
assert (s_, b_, total) == (2, 6, 9) and F(24, 4) == 6 and 3 + F(24, 6) == 7
Q(T, "Speed of stream", I,
  "A boat's speed in still water is three times the speed of the stream. It goes 24 km downstream in 3 hours. How "
  "long does the round trip (24 km downstream and back) take?",
  "9 hours", ["6 hours", "7 hours", "12 hours"],
  "If the stream is s, the boat is 3s: downstream = 4s, upstream = 2s",
  "Downstream speed = 24 ÷ 3 = 8 km/h = 4s, so s = 2 km/h and the boat is 6 km/h. Upstream speed = 4 km/h, so the "
  "return takes 24 ÷ 4 = 6 hours. Round trip = 3 + 6 = 9 hours.",
  ["Downstream = 8 = 4s ⇒ s = 2", "Boat = 6, upstream = 4 km/h", "Return = 6 h", "Total = 9 h"],
  why="6 hours is only the return journey; 7 hours takes the upstream speed as the still-water speed 6 km/h; 12 hours "
      "doubles the upstream time.", secs=55)

t2 = F(35, 14) + F(35, 10)
t3 = F(35, 15) + F(35, 9)
assert t2 == 6 and (t3 - t2) * 60 == F(40, 3) and (F(35, 9) - F(35, 10)) * 60 == F(70, 3) and (F(35, 14) - F(35, 15)) * 60 == 10
Q(T, "Speed of stream", A,
  "A boat with a speed of 12 km/h in still water makes a 35 km trip downstream and back. If the speed of the stream "
  "rises from 2 km/h to 3 km/h, how much longer does the round trip take?",
  "13⅓ minutes", ["No longer: the effects cancel", "23⅓ minutes", "10 minutes"],
  "Compute both round-trip times; the slower upstream leg loses more time than the faster downstream leg saves",
  "Stream 2 km/h: 35/14 + 35/10 = 2.5 + 3.5 = 6 hours. Stream 3 km/h: 35/15 + 35/9 = 2⅓ + 3 8/9 = 6 2/9 hours. The "
  "difference is 2/9 hour = 13⅓ minutes.",
  ["At 2 km/h: 2.5 h + 3.5 h = 6 h", "At 3 km/h: 2⅓ h + 3⁸⁄₉ h = 6²⁄₉ h", "Extra = ²⁄₉ h = 13⅓ min"],
  why="'No longer' assumes the gain downstream cancels the loss upstream; 23⅓ minutes counts only the extra time "
      "upstream; 10 minutes counts only the time saved downstream.", secs=95)

# ================================================================ Problems on Trains (B1 I1 A1)
T = "Problems on Trains"
v = F(200 + 400, 30) * F(18, 5)
assert v == 72 and F(400, 30) * F(18, 5) == 48 and F(200, 30) * F(18, 5) == 24
Q(T, "Crossing a pole or platform", B,
  "A train 200 m long crosses a bridge 400 m long in 30 seconds. What is the speed of the train in km/h?",
  "72 km/h", ["48 km/h", "24 km/h", "20 km/h"],
  "To cross a bridge, the train covers its own length plus the bridge; 1 m/s = 3.6 km/h",
  "Distance = 200 + 400 = 600 m in 30 s = 20 m/s = 20 × 18/5 = 72 km/h.",
  ["600 m in 30 s", "20 m/s", "20 × 3.6 = 72 km/h"],
  why="48 km/h uses only the bridge's length; 24 km/h uses only the train's length; 20 is the speed in m/s, not km/h.",
  secs=35)

rel = F(300, 36) * F(18, 5)
assert rel == 30 and 60 - rel == 30 and 60 + rel == 90 and 60 - F(180, 36) * F(18, 5) == 42
Q(T, "Trains crossing each other", I,
  "A train 120 m long running at 60 km/h overtakes a train 180 m long running in the same direction on a parallel "
  "track, and passes it completely in 36 seconds. What is the speed of the slower train?",
  "30 km/h", ["90 km/h", "42 km/h", "8⅓ km/h"],
  "Overtaking covers the sum of the lengths at the difference of the speeds",
  "Relative speed = (120 + 180) ÷ 36 = 25/3 m/s = 25/3 × 18/5 = 30 km/h. Slower train = 60 − 30 = 30 km/h.",
  ["Distance = 300 m", "Relative = 300 ÷ 36 = 25/3 m/s = 30 km/h", "Slower = 60 − 30 = 30 km/h"],
  why="90 km/h adds the relative speed, as if the trains ran towards each other; 42 km/h uses only the 180 m train's "
      "length; 8⅓ is the relative speed in m/s.", secs=60)

sol = [(L, v) for v in range(1, 60) for L in range(1, 1000) if L + 300 == 30 * v and 3 * L == 27 * v + 45]
v_ = (300 + 15) / F(21)
assert v_ == 15 and sol == [(150, 15)] and F(900, 7) == 9 * F(300, 21) and r2(9 * (F(285, 21) - F(5, 3))) == F(10714, 100)
Q(T, "Crossing a pole or platform", A,
  "A train passes completely through a 300 m long platform in 30 seconds. It passes a man walking on the platform "
  "at 6 km/h towards the train (in the opposite direction) in 9 seconds. What is the length of the train?",
  "150 m", ["128.57 m", "107.14 m", "450 m"],
  "Use L + 300 = 30v for the platform and L = 9 × (v + man's speed) for the man; 6 km/h = 5/3 m/s",
  "L + 300 = 30v and L = 9(v + 5/3) = 9v + 15. Subtracting, 300 − 15 = 21v, so v = 15 m/s (54 km/h) and "
  "L = 30 × 15 − 300 = 150 m.",
  ["6 km/h = 5/3 m/s", "L + 300 = 30v", "L = 9v + 15", "21v = 285 ⇒ v = 15 m/s", "L = 150 m"],
  why="128.57 m ignores the man's speed (L = 9v); 107.14 m takes him as walking in the same direction as the train; "
      "450 m is the length of the train plus the platform.", secs=100, by=BRUTE)

# ================================================================ Mensuration (B1 I2 A2)
T = "Mensuration"
r_ = next(r for r in range(1, 100) if F(22, 7) * r * r == 616)
assert r_ == 14 and 2 * F(22, 7) * 14 == 88 and 2 * F(22, 7) * 7 == 44 and 2 * F(22, 7) * 28 == 176
Q(T, "2D areas and perimeters", B,
  "The area of a circular plot is 616 m². What is its circumference? (Use π = 22/7.)",
  "88 m", ["44 m", "176 m", "196 m"],
  "Find r from πr² = area, then circumference = 2πr",
  "22/7 × r² = 616 ⇒ r² = 196 ⇒ r = 14 m. Circumference = 2 × 22/7 × 14 = 88 m.",
  ["r² = 616 × 7/22 = 196", "r = 14 m", "2πr = 88 m"],
  why="44 m uses r = 7 (half the radius); 176 m uses r = 28 (the diameter as the radius); 196 is r², not the "
      "circumference.", secs=40)

assert F(2 ** 2 * 5, 3 ** 2 * 3) == F(20, 27) and F(2 * 5, 3 * 3) == F(10, 9)
Q(T, "Cylinder, cone and sphere", I,
  "The radii of two cylinders are in the ratio 2 : 3 and their heights are in the ratio 5 : 3. What is the ratio of "
  "their volumes?",
  "20 : 27", ["10 : 9", "4 : 9", "27 : 20"],
  "Volume = πr²h, so the radius ratio is squared and the height ratio is not",
  "V₁ : V₂ = (2² × 5) : (3² × 3) = 20 : 27.",
  ["V ∝ r²h", "(4 × 5) : (9 × 3)", "= 20 : 27"],
  why="10 : 9 forgets to square the radii; 4 : 9 ignores the heights; 27 : 20 inverts the ratio.", secs=45)

path = 50 * 30 - (50 - 4) * (30 - 4)
assert path == 304 and 2 * (50 + 30) * 2 == 320 and (54 * 34) - 1500 == 336 and 46 * 26 == 1196
Q(T, "2D areas and perimeters", I,
  "A rectangular lawn measures 50 m × 30 m. A path 2 m wide runs along all four sides inside the lawn. What is the "
  "area of the path?",
  "304 m²", ["320 m²", "336 m²", "1,196 m²"],
  "Area of an inside path = outer area − inner area, where each inner side is shorter by 2 × width",
  "Inner rectangle = (50 − 4) × (30 − 4) = 46 × 26 = 1,196 m². Path = 1,500 − 1,196 = 304 m².",
  ["Outer = 1,500 m²", "Inner = 46 × 26 = 1,196 m²", "Path = 304 m²"],
  why="320 m² multiplies the perimeter by the width and counts the four corner squares twice; 336 m² is a 2 m path "
      "outside the lawn; 1,196 m² is the area inside the path.", secs=55)

w_ = [w for w in range(1, 30) if (40 + 2 * w) * (30 + 2 * w) - 1200 == 456]
assert w_ == [3] and (40 + 6) * (30 + 6) - 1200 == 456 and r2(F(456, 140)) == F(326, 100)
wi = (35 - math.sqrt(35 ** 2 - 4 * 114)) / 2
assert abs(wi - 3.63) < 0.005
Q(T, "2D areas and perimeters", A,
  "A path of uniform width runs around the outside of a rectangular garden 40 m long and 30 m wide. The area of the "
  "path is 456 m². What is the width of the path?",
  "3 m", ["3.26 m", "6 m", "3.63 m"],
  "Outer rectangle = (40 + 2w)(30 + 2w); the path's area gives a quadratic in w",
  "(40 + 2w)(30 + 2w) − 1,200 = 456 ⇒ 4w² + 140w − 456 = 0 ⇒ w² + 35w − 114 = 0 ⇒ (w + 38)(w − 3) = 0, so w = 3 m.",
  ["(40 + 2w)(30 + 2w) − 1,200 = 456", "w² + 35w − 114 = 0", "(w − 3)(w + 38) = 0 ⇒ w = 3 m"],
  why="3.26 m divides 456 by the perimeter 140 and ignores the four corner squares; 6 m adds the width only once to "
      "each dimension, (40 + w)(30 + w); 3.63 m treats the path as lying inside the garden.", secs=90, by=BRUTE)

cube = 14 ** 3
sph = F(4, 3) * F(22, 7) * 7 ** 3
assert cube == 2744 and sph == F(4312, 3) and cube - sph == F(3920, 3) and cube - F(4, 3) * 3 * 343 == 1372
Q(T, "Cylinder, cone and sphere", A,
  "The largest possible sphere is carved out of a solid cube of edge 14 cm. What volume of the cube is cut away? "
  "(Use π = 22/7.)",
  "1,306⅔ cm³", ["1,437⅓ cm³", "2,744 cm³", "1,372 cm³"],
  "The largest sphere in a cube has diameter equal to the edge, so r = 7 cm",
  "Cube = 14³ = 2,744 cm³. Sphere = 4/3 × 22/7 × 7³ = 4,312/3 = 1,437⅓ cm³. Cut away = 2,744 − 1,437⅓ = 1,306⅔ cm³.",
  ["r = 14 ÷ 2 = 7 cm", "Cube = 2,744 cm³", "Sphere = 1,437⅓ cm³", "Waste = 1,306⅔ cm³"],
  why="1,437⅓ cm³ is the volume of the sphere; 2,744 cm³ is the whole cube; 1,372 cm³ uses π = 3 instead of the "
      "stated 22/7.", secs=80)

# ================================================================ Probability (B2 I2 A1)
T = "Probability"
dice = list(itertools.product(range(1, 7), repeat=2))
fav = [d for d in dice if d[0] == d[1] or sum(d) == 4]
assert F(len(fav), 36) == F(2, 9) and F(6 + 3, 36) == F(1, 4)
Q(T, "Coins and dice", B,
  "Two fair dice are rolled. What is the probability of getting a doublet (both dice showing the same number) or a "
  "total of 4?",
  "2/9", ["1/4", "1/6", "1/12"],
  "Count the outcomes in the union once each: (2, 2) is both a doublet and a total of 4",
  "Doublets: 6 outcomes. Total 4: (1, 3), (2, 2), (3, 1). (2, 2) is in both, so the union has 6 + 3 − 1 = 8 outcomes, "
  "and the probability is 8/36 = 2/9.",
  ["Doublets = 6", "Total 4 = 3", "Overlap (2, 2) = 1", "8/36 = 2/9"],
  why="1/4 counts (2, 2) twice (9/36); 1/6 counts only the doublets; 1/12 counts only the totals of 4.", secs=40,
  by=BRUTE)

primes = [n for n in range(1, 26) if n > 1 and all(n % d for d in range(2, n))]
assert len(primes) == 9
Q(T, "Balls from bags", B,
  "A bag contains 25 balls numbered 1 to 25. One ball is drawn at random. What is the probability that its number "
  "is a prime?",
  "9/25", ["2/5", "8/25", "16/25"],
  "List the primes up to 25; 1 is not prime and 2 is",
  "Primes from 1 to 25: 2, 3, 5, 7, 11, 13, 17, 19, 23 — nine numbers. Probability = 9/25.",
  ["Primes: 2, 3, 5, 7, 11, 13, 17, 19, 23", "Count = 9", "P = 9/25"],
  why="2/5 counts 1 as a prime (10/25); 8/25 leaves out 2, the only even prime; 16/25 is the probability of NOT "
      "getting a prime.", secs=35, by=BRUTE)

deck = [(r, s) for r in range(13) for s in range(4)]
face = lambda c: c[0] in (10, 11, 12)  # noqa: E731
combos = list(itertools.combinations(deck, 3))
fav = sum(1 for c in combos if all(face(x) for x in c))
assert len(combos) == 22100 and fav == 220 and F(fav, 22100) == F(11, 1105) and F(1320, 22100) == F(66, 1105)
Q(T, "Cards", I,
  "Three cards are drawn together at random from a well-shuffled pack of 52 cards. What is the probability that all "
  "three are face cards (jack, queen or king)?",
  "11/1105", ["27/2197", "3/13", "66/1105"],
  "Use combinations for both counts: ¹²C₃ favourable out of ⁵²C₃",
  "There are 12 face cards. ¹²C₃ = 220 and ⁵²C₃ = 22,100, so the probability = 220/22,100 = 11/1105.",
  ["¹²C₃ = 220", "⁵²C₃ = 22,100", "220/22,100 = 11/1105"],
  why="27/2197 = (12/52)³ assumes each card is replaced before the next draw; 3/13 is the probability for a single "
      "card; 66/1105 counts the favourable cards in order (12 × 11 × 10) but the total without order.", secs=60,
  by=BRUTE)

bag = ["W"] * 5 + ["B"] * 3
pairs = list(itertools.product(bag, repeat=2))
assert F(sum(1 for a, b in pairs if a != b), 64) == F(15, 32)
assert F(sum(1 for a, b in itertools.permutations(range(8), 2) if (a < 5) != (b < 5)), 56) == F(15, 28)
Q(T, "Balls from bags", I,
  "A bag contains 5 white and 3 black balls. Two balls are drawn one after the other, the first being replaced before "
  "the second is drawn. What is the probability that the two balls are of different colours?",
  "15/32", ["15/64", "15/28", "17/32"],
  "With replacement the draws are independent; 'different colours' can happen as WB or BW",
  "P(W then B) = 5/8 × 3/8 = 15/64 and P(B then W) = 15/64, so P(different) = 30/64 = 15/32.",
  ["P(WB) = 15/64", "P(BW) = 15/64", "Total = 30/64 = 15/32"],
  why="15/64 counts only one order; 15/28 draws without replacement; 17/32 is the probability that the colours are "
      "the same.", secs=50, by=BRUTE)

six = [d for d in dice if 6 in d]
hi = [d for d in six if sum(d) >= 10]
assert len(six) == 11 and len(hi) == 5 and F(len(hi), len(six)) == F(5, 11)
assert len([d for d in dice if sum(d) >= 10]) == 6
Q(T, "Coins and dice", A,
  "Two fair dice are rolled, and you are told that at least one of them shows a 6. What is the probability that the "
  "total is 10 or more?",
  "5/11", ["5/36", "1/6", "6/11"],
  "Conditional probability: count only within the outcomes that have at least one 6",
  "Outcomes with at least one 6: 11. Of these, totals of 10 or more are (4, 6), (6, 4), (5, 6), (6, 5) and (6, 6) — "
  "5 outcomes. Probability = 5/11.",
  ["Reduced sample space: 11 outcomes with a 6", "Favourable: (4,6), (6,4), (5,6), (6,5), (6,6)", "P = 5/11"],
  why="5/36 forgets the condition and divides by all 36 outcomes; 1/6 is the unconditional chance of a total of 10 or "
      "more (6/36); 6/11 also counts (5, 5), which has no 6.", secs=80, by=BRUTE)

# ================================================================ Permutation and Combination (B1 I2 A1)
T = "Permutation and Combination"
cnt = sum(1 for p in itertools.permutations("ABCDE") if abs(p.index("A") - p.index("B")) == 1)
assert cnt == 48 and math.factorial(4) == 24 and 120 - 48 == 72
Q(T, "Arrangements", B,
  "In how many ways can 5 people sit in a row of 5 chairs if two particular people must sit next to each other?",
  "48", ["24", "120", "72"],
  "Tie the two people together as one unit, arrange the units, then arrange the two inside the unit",
  "Treat the pair as one unit: 4 units can be arranged in 4! = 24 ways, and the pair can sit in 2 orders. Total = "
  "24 × 2 = 48.",
  ["4 units ⇒ 4! = 24", "Pair can swap ⇒ × 2", "48"],
  why="24 forgets that the two can swap places; 120 ignores the condition; 72 counts the arrangements in which the "
      "two are NOT together.", secs=40, by=BRUTE)

cnt = len({p for p in itertools.permutations("CREDIT") if abs(p.index("E") - p.index("I")) != 1})
assert cnt == 480 and 720 - 240 == 480 and 720 - 120 == 600
Q(T, "Word arrangements", I,
  "In how many ways can the letters of the word CREDIT be arranged so that the two vowels are never next to each "
  "other?",
  "480", ["240", "600", "720"],
  "Never together = all arrangements − arrangements with the vowels together",
  "All arrangements: 6! = 720. With E and I together: treat them as one unit, 5! × 2 = 240. Never together = 720 − 240 "
  "= 480.",
  ["Total = 720", "Vowels together = 5! × 2 = 240", "Never together = 480"],
  short="Gap method: arrange C, R, D, T in 4! = 24 ways and place E, I in 2 of the 5 gaps: ⁵P₂ = 20; 24 × 20 = 480.",
  why="240 counts the arrangements with the vowels together; 600 forgets that E and I can swap within their unit "
      "(720 − 120); 720 ignores the condition.", secs=55, by=BRUTE)

cnt = sum(1 for c in itertools.combinations(range(8), 3) if not (0 in c and 1 in c))
assert cnt == 50 and math.comb(8, 3) == 56 and math.comb(6, 3) == 20
Q(T, "Selections", I,
  "In how many ways can 3 books be chosen from 8 different books if two particular books must never both be chosen?",
  "50", ["56", "20", "44"],
  "Subtract the selections that contain both of the two books",
  "All selections: ⁸C₃ = 56. Selections containing both particular books: the third book can be any of the other 6, "
  "so 6. Allowed = 56 − 6 = 50.",
  ["⁸C₃ = 56", "Both chosen: 6 ways", "56 − 6 = 50"],
  why="56 ignores the condition; 20 leaves out both books altogether (⁶C₃); 44 subtracts the 6 bad selections twice.",
  secs=50, by=BRUTE)

players = ["bat"] * 6 + ["bowl"] * 4
cnt = sum(4 for c in itertools.combinations(range(10), 4) if any(players[i] == "bowl" for i in c))
assert cnt == 780 and math.comb(10, 4) - math.comb(6, 4) == 195 and 210 * 4 == 840 and 4 * math.comb(9, 3) * 4 == 1344
Q(T, "Selections", A,
  "A team of 4 is to be chosen from 6 batsmen and 4 bowlers so that it has at least one bowler, and then one of the "
  "4 chosen players is to be made captain. In how many ways can this be done?",
  "780", ["195", "840", "1,344"],
  "Count the teams with at least one bowler (complement), then multiply by the 4 choices of captain",
  "Teams of 4 from 10: ¹⁰C₄ = 210. Teams with no bowler: ⁶C₄ = 15. So 195 teams have at least one bowler. Each can "
  "choose its captain in 4 ways: 195 × 4 = 780.",
  ["¹⁰C₄ = 210", "No bowler: ⁶C₄ = 15", "195 teams", "× 4 captains = 780"],
  why="195 forgets to choose the captain; 840 drops the 'at least one bowler' condition; 1,344 counts 'pick one bowler, "
      "then any 3 others' (4 × ⁹C₃), which counts teams with two or more bowlers several times.", secs=90, by=BRUTE)

# ================================================================ Tabular DI (B3 I2 A6): sets of 6 and 5
T = "Tabular DI"
TEA = {"Amguri": (400, 2250, 20), "Borjan": (320, 2500, 35), "Chandra": (500, 1800, 10),
       "Dhelakhat": (250, 2800, 36), "Erabari": (450, 2400, 25)}
sid = stimulus("data_table", "Area, yield and orthodox share at five tea estates, 2025",
               "The table shows, for five tea estates in 2025, the area under tea (hectares), the yield of made tea "
               "(kg per hectare) and the share of the production that was orthodox tea; the rest of each estate's "
               "production was CTC tea. 1 tonne = 1,000 kg.\n\n" +
               md_table(["Estate", "Area (hectares)", "Yield (kg per hectare)", "Orthodox share (% of production)"],
                        [[k, a, ind(y), o] for k, (a, y, o) in TEA.items()]),
               {"columns": ["estate", "area_ha", "yield_kg_per_ha", "orthodox_pct"],
                "rows": [[k, *v] for k, v in TEA.items()]})
prod = {k: F(a * y, 1000) for k, (a, y, o) in TEA.items()}  # tonnes
orth = {k: prod[k] * F(o, 100) for k, (a, y, o) in TEA.items()}
assert prod == {"Amguri": 900, "Borjan": 800, "Chandra": 900, "Dhelakhat": 700, "Erabari": 1080}
assert orth == {"Amguri": 180, "Borjan": 280, "Chandra": 90, "Dhelakhat": 252, "Erabari": 270}
Q(T, "Single table", B, "How many tonnes of made tea did Borjan produce in 2025?",
  "800 tonnes", ["80 tonnes", "280 tonnes", "8,000 tonnes"],
  "Production = area × yield; convert kg to tonnes by dividing by 1,000",
  "Borjan: 320 ha × 2,500 kg/ha = 8,00,000 kg = 800 tonnes.",
  ["320 × 2,500 = 8,00,000 kg", "÷ 1,000 = 800 tonnes"],
  why="80 tonnes and 8,000 tonnes slip a zero in the conversion; 280 tonnes is Borjan's orthodox tea only.", secs=35,
  stim=sid)

assert prod["Chandra"] - orth["Chandra"] == 810 and prod["Chandra"] * F(80, 100) == 720
Q(T, "Table with percentages", B, "How many tonnes of CTC tea did Chandra produce in 2025?",
  "810 tonnes", ["90 tonnes", "900 tonnes", "720 tonnes"],
  "CTC share = 100% − orthodox share",
  "Chandra produced 500 × 1,800 = 9,00,000 kg = 900 tonnes, of which 10% (90 tonnes) was orthodox. CTC = 90% of 900 = "
  "810 tonnes.",
  ["Production = 900 tonnes", "CTC share = 90%", "0.9 × 900 = 810 tonnes"],
  why="90 tonnes is the orthodox tea; 900 tonnes is the whole production; 720 tonnes uses Amguri's 20% orthodox share.",
  secs=40, stim=sid)

srt = sorted(orth, key=orth.get, reverse=True)
assert srt[:2] == ["Borjan", "Erabari"] and max(TEA, key=lambda k: TEA[k][2]) == "Dhelakhat"
Q(T, "Table with percentages", I, "Which estate produced the largest quantity of orthodox tea in 2025?",
  "Borjan", ["Erabari", "Dhelakhat", "Amguri"],
  "Orthodox tea = area × yield × orthodox share; compare the products, not the percentages",
  "Orthodox tea (tonnes): Amguri 180, Borjan 280, Chandra 90, Dhelakhat 252, Erabari 270. Borjan is the largest.",
  ["Amguri 900 × 20% = 180", "Borjan 800 × 35% = 280", "Chandra 900 × 10% = 90", "Dhelakhat 700 × 36% = 252",
   "Erabari 1,080 × 25% = 270"],
  why="Erabari has the largest total production but only 270 tonnes of orthodox tea; Dhelakhat has the highest "
      "orthodox percentage but a small area (252 tonnes); Amguri produces only 180 tonnes.", secs=60, stim=sid)

tp, to = sum(prod.values()), sum(orth.values())
assert (tp, to) == (4380, 1072) and pct2(F(to, tp)) == "24.47%" and F(126, 5) == F(252, 10)
area_w = F(sum(a * o for a, y, o in TEA.values()), sum(a for a, y, o in TEA.values()))
assert pct2(area_w / 100) == "23.15%" and pct2(1 - F(to, tp)) == "75.53%"
Q(T, "Table with percentages", A,
  "What percentage of the total production of the five estates was orthodox tea (correct to two decimal places)?",
  "24.47%", ["25.20%", "23.15%", "75.53%"],
  "Overall share = total orthodox ÷ total production; the estates' percentages must be weighted by production",
  "Total production = 900 + 800 + 900 + 700 + 1,080 = 4,380 tonnes. Total orthodox = 180 + 280 + 90 + 252 + 270 = "
  "1,072 tonnes. Share = 1,072 ÷ 4,380 = 24.47%.",
  ["Total production = 4,380 t", "Total orthodox = 1,072 t", "1,072 ÷ 4,380 = 24.47%"],
  why="25.20% is the simple average of the five percentages; 23.15% weights the percentages by area instead of by "
      "production; 75.53% is the CTC share.", secs=100, stim=sid)

rev = orth["Erabari"] * 1000 * 420 + (prod["Erabari"] - orth["Erabari"]) * 1000 * 240
assert rev == 307800000 and 1080000 * 240 == 259200000 and 1080000 * 420 == 453600000 and 1080000 * 330 == 356400000
Q(T, "Table with percentages", A,
  "Orthodox tea sells at ₹420 per kg and CTC tea at ₹240 per kg. What was Erabari's revenue from its 2025 "
  "production?",
  "₹30.78 crore", ["₹25.92 crore", "₹45.36 crore", "₹35.64 crore"],
  "Split the production into orthodox and CTC, price each, then add",
  "Erabari: 1,080 tonnes, 25% orthodox. Orthodox 270 t = 2,70,000 kg × ₹420 = ₹11.34 crore. CTC 810 t = 8,10,000 kg × "
  "₹240 = ₹19.44 crore. Total = ₹30.78 crore.",
  ["Orthodox: 2,70,000 × 420 = 11.34 crore", "CTC: 8,10,000 × 240 = 19.44 crore", "Total = 30.78 crore"],
  why="₹25.92 crore prices all the tea as CTC; ₹45.36 crore prices it all as orthodox; ₹35.64 crore uses the simple "
      "average price ₹330.", secs=90, stim=sid)

new_prod = prod["Chandra"] * F(125, 100)
new_orth = new_prod * F(20, 100)
assert new_prod == 1125 and new_orth == 225 and (new_orth - 90) / 90 * 100 == 150
Q(T, "Table with percentages", A,
  "Next year Chandra keeps the same area, its yield rises by 25% and its orthodox share doubles. By what percentage "
  "does its orthodox production increase?",
  "150%", ["100%", "125%", "25%"],
  "Orthodox output = area × yield × share; multiply the change factors: 1.25 × 2",
  "New production = 900 × 1.25 = 1,125 tonnes; new orthodox share = 20%, so orthodox = 225 tonnes against 90 now. "
  "Increase = 135 ÷ 90 = 150%.",
  ["Factor = 1.25 × 2 = 2.5", "90 → 225 tonnes", "Increase = 150%"],
  why="100% counts only the doubled share; 125% adds the two changes (25% + 100%) instead of multiplying the factors; "
      "25% counts only the yield rise.", secs=80, stim=sid)

FD = {"1 year": (300, F(25, 10), F(65, 10)), "2 years": (200, F(45, 10), F(68, 10)),
      "3 years": (150, F(6), F(7)), "5 years": (50, F(19), F(725, 100))}
sid = stimulus("data_table", "Fixed deposits booked at a bank branch in a quarter, by tenure",
               "The table shows the fixed deposits booked at a bank branch in one quarter, by tenure: the number of "
               "deposits, the average size of a deposit (₹ lakh) and the interest rate offered (% per annum). "
               "1 crore = 100 lakh.\n\n" +
               md_table(["Tenure", "Number of deposits", "Average deposit (₹ lakh)", "Interest rate (% p.a.)"],
                        [[k, n, N(a), N(r)] for k, (n, a, r) in FD.items()]),
               {"columns": ["tenure", "deposits", "average_deposit_lakh", "rate_pct"],
                "rows": [[k, n, float(a), float(r)] for k, (n, a, r) in FD.items()]})
amt = {k: n * a for k, (n, a, r) in FD.items()}
assert amt == {"1 year": 750, "2 years": 900, "3 years": 900, "5 years": 950} and sum(amt.values()) == 3500
Q(T, "Single table", B, "What was the total amount of the 1-year deposits booked in the quarter?",
  "₹7.5 crore", ["₹75 crore", "₹9 crore", "₹2.5 crore"],
  "Total amount = number of deposits × average deposit",
  "300 deposits × ₹2.5 lakh = ₹750 lakh = ₹7.5 crore.",
  ["300 × 2.5 = 750 lakh", "= 7.5 crore"],
  why="₹75 crore slips a decimal place in converting lakh to crore; ₹9 crore is the 2-year (or 3-year) total; ₹2.5 "
      "crore confuses the average deposit in lakh with the total.", secs=35, stim=sid)

avg_ = F(3500, 700)
assert avg_ == 5 and sum(a for n, a, r in FD.values()) / 4 == 8
Q(T, "Single table", I, "What was the average size of a deposit across all four tenures taken together?",
  "₹5 lakh", ["₹8 lakh", "₹4.375 lakh", "₹50 lakh"],
  "Overall average = total amount ÷ total number of deposits (a weighted average)",
  "Total amount = 750 + 900 + 900 + 950 = ₹3,500 lakh; total deposits = 300 + 200 + 150 + 50 = 700. Average = "
  "3,500 ÷ 700 = ₹5 lakh.",
  ["Total = 3,500 lakh", "Number = 700", "3,500 ÷ 700 = 5 lakh"],
  why="₹8 lakh is the simple average of the four averages; ₹4.375 lakh divides the total by 800 deposits (a miscount); "
      "₹50 lakh slips a decimal place.", secs=55, stim=sid)

ci3 = amt["3 years"] * (F(107, 100) ** 3 - 1)
assert r2(ci3) == F(20254, 100) and amt["3 years"] * F(21, 100) == 189 and r2(amt["3 years"] + ci3) == F(110254, 100)
Q(T, "Single table", A,
  "Interest on the 3-year deposits is compounded annually at the rate shown. What total interest will be payable on "
  "all the 3-year deposits at maturity (in ₹ lakh, correct to two decimal places)?",
  "₹202.54 lakh", ["₹189 lakh", "₹1,102.54 lakh", "₹63 lakh"],
  "Total 3-year amount = 150 × 6 = ₹900 lakh; CI = P(1.07³ − 1)",
  "1.07³ = 1.225043, so the interest = 900 × 0.225043 = ₹202.54 lakh.",
  ["P = 900 lakh", "1.07² = 1.1449; 1.07³ = 1.225043", "CI = 900 × 0.225043 = 202.54 lakh"],
  why="₹189 lakh is simple interest for 3 years; ₹1,102.54 lakh is the maturity amount, not the interest; ₹63 lakh is "
      "one year's interest.", secs=90, stim=sid)

wr = sum(amt[k] * FD[k][2] for k in FD) / 3500
nr = sum(FD[k][0] * FD[k][2] for k in FD) / F(700)
assert f"{float(r2(wr)):.2f}" == "6.91" and f"{float(r2(nr)):.2f}" == "6.75" and r2(sum(r for n, a, r in FD.values()) / 4) == F(689, 100)
Q(T, "Single table", A,
  "What is the average interest rate on all the deposits booked, weighted by the amount deposited (correct to two "
  "decimal places)?",
  "6.91%", ["6.89%", "6.75%", "7.25%"],
  "Weight each rate by the rupee amount of that tenure: Σ(amount × rate) ÷ Σ amount",
  "Amounts (₹ lakh): 750, 900, 900, 950. Σ(amount × rate) = 750 × 6.5 + 900 × 6.8 + 900 × 7 + 950 × 7.25 = 4,875 + "
  "6,120 + 6,300 + 6,887.5 = 24,182.5. Divided by 3,500, this is 6.91%.",
  ["Amounts: 750, 900, 900, 950", "Σ amount × rate = 24,182.5", "24,182.5 ÷ 3,500 = 6.91%"],
  why="6.89% is the simple average of the four rates; 6.75% weights the rates by the number of deposits, not the "
      "amount; 7.25% is just the highest rate.", secs=100, stim=sid)

base = amt["3 years"] * F(7, 100)
extra = amt["3 years"] * F(40, 100) * F(5, 1000)
assert base == 63 and extra == F(18, 10) and base + extra == F(648, 10) and amt["3 years"] * F(75, 1000) == F(675, 10)
assert base + amt["3 years"] * F(60, 100) * F(5, 1000) == F(657, 10)
Q(T, "Single table", A,
  "Senior citizens hold 40% (by amount) of the 3-year deposits and receive 0.5% per annum more than the rate shown. "
  "What is the total simple interest for one year on all the 3-year deposits?",
  "₹64.8 lakh", ["₹67.5 lakh", "₹63 lakh", "₹65.7 lakh"],
  "Interest at 7% on the whole amount, plus an extra 0.5% on the senior citizens' 40%",
  "Total 3-year amount = ₹900 lakh. At 7%: ₹63 lakh. Senior citizens' share = ₹360 lakh, extra 0.5% = ₹1.8 lakh. "
  "Total = ₹64.8 lakh.",
  ["Amount = 900 lakh", "7% of 900 = 63", "0.5% of 360 = 1.8", "63 + 1.8 = 64.8 lakh"],
  why="₹67.5 lakh pays 7.5% on everyone's deposits; ₹63 lakh ignores the senior-citizen extra; ₹65.7 lakh applies the "
      "extra to 60% of the deposits instead of 40%.", secs=80, stim=sid)

# ================================================================ Bar Graph DI (B1 I2 A3): two sets of 3
T = "Bar Graph DI"
GL = {"2020-21": 500, "2021-22": 600, "2022-23": 540, "2023-24": 675, "2024-25": 945, "2025-26": 1260}
sid = stimulus("chart", "Gold loans disbursed by a bank, 2020-21 to 2025-26",
               "The bar chart shows the amount of gold loans (₹ crore) disbursed by a bank in each financial year "
               "from 2020-21 to 2025-26 (values read from the bars).\n\n" +
               md_table(["Year", "Gold loans disbursed (₹ crore)"], [[k, ind(v)] for k, v in GL.items()]),
               {"chart_type": "bar", "x": list(GL), "series": [{"name": "Gold loans (₹ crore)",
                                                                "values": list(GL.values())}]})
ys_ = list(GL)
chg = {ys_[i]: F(GL[ys_[i]] - GL[ys_[i - 1]], GL[ys_[i - 1]]) for i in range(1, 6)}
assert chg == {"2021-22": F(1, 5), "2022-23": F(-1, 10), "2023-24": F(1, 4), "2024-25": F(2, 5), "2025-26": F(1, 3)}
assert [y for y, c in chg.items() if c == F(1, 4)] == ["2023-24"]
Q(T, "Simple bar", B, "In which year was the disbursement exactly 25% more than in the previous year?",
  "2023-24", ["2021-22", "2024-25", "2025-26"],
  "Percentage change = (this year − previous year) ÷ previous year × 100",
  "2021-22: +100 on 500 = 20%; 2022-23: −10%; 2023-24: +135 on 540 = 25%; 2024-25: +270 on 675 = 40%; 2025-26: +315 "
  "on 945 = 33⅓%. Only 2023-24 shows a 25% rise.",
  ["2021-22: +20%", "2022-23: −10%", "2023-24: +25% ✓", "2024-25: +40%", "2025-26: +33⅓%"],
  why="2021-22 rose 20%; 2024-25 rose 40%; 2025-26 rose 33⅓% (315 ÷ 945), which is 25% only if the rise is divided by "
      "the later year's 1,260.", secs=45, stim=sid)

assert F(1260, 500) == F(252, 100) and sum(chg.values()) * 100 == F(325, 3) and r2(F(760, 1260) * 100) == F(6032, 100)
Q(T, "Simple bar", I, "By what percentage did the yearly disbursement grow from 2020-21 to 2025-26?",
  "152%", ["108⅓%", "252%", "60.32%"],
  "Overall growth compares the two end years directly; yearly growth rates cannot simply be added",
  "2025-26: ₹1,260 crore against ₹500 crore in 2020-21. Growth = 760 ÷ 500 = 152%.",
  ["Increase = 1,260 − 500 = 760", "760 ÷ 500 = 1.52 = 152%"],
  why="108⅓% adds the five yearly rates (20 − 10 + 25 + 40 + 33⅓); 252% is 1,260 as a percentage of 500, not the "
      "increase; 60.32% divides the increase by the later year's 1,260.", secs=55, stim=sid)

avg24 = F(945 * 10 ** 7, 63000)
avg25 = avg24 * F(120, 100)
n25 = F(1260 * 10 ** 7) / avg25
assert avg24 == 150000 and avg25 == 180000 and n25 == 70000 and F(1260 * 10 ** 7, 150000) == 84000 and 63000 * F(12, 10) == 75600
Q(T, "Simple bar", A,
  "In 2024-25 the bank disbursed 63,000 gold loans. In 2025-26 the average size of a gold loan was 20% higher than "
  "in 2024-25. How many gold loans did the bank disburse in 2025-26?",
  "70,000", ["84,000", "63,000", "75,600"],
  "Number of loans = amount disbursed ÷ average loan size",
  "2024-25 average = ₹945 crore ÷ 63,000 = ₹1.5 lakh. 2025-26 average = ₹1.8 lakh. Number in 2025-26 = ₹1,260 crore ÷ "
  "₹1.8 lakh = 70,000.",
  ["2024-25 average = 1.5 lakh", "2025-26 average = 1.8 lakh", "1,260 crore ÷ 1.8 lakh = 70,000"],
  why="84,000 keeps the 2024-25 average of ₹1.5 lakh; 63,000 assumes the number of loans did not change; 75,600 raises "
      "the number of loans by 20% instead of the loan size.", secs=95, stim=sid)

RE = {"State A": (1200, 800), "State B": (900, 1500), "State C": (1650, 450), "State D": (600, 1200),
      "State E": (1350, 1150)}
sid = stimulus("chart", "Solar and wind power capacity added in five states, 2025-26",
               "The stacked bar chart shows the new solar and wind power capacity (in megawatts, MW) added in five "
               "states in 2025-26; each bar is split into its solar and wind parts (values read from the bars).\n\n" +
               md_table(["State", "Solar (MW)", "Wind (MW)", "Total (MW)"],
                        [[k, ind(s), ind(w), ind(s + w)] for k, (s, w) in RE.items()]),
               {"chart_type": "stacked_bar", "x": list(RE),
                "series": [{"name": "Solar (MW)", "values": [v[0] for v in RE.values()]},
                           {"name": "Wind (MW)", "values": [v[1] for v in RE.values()]}]})
share_w = {k: F(w, s + w) for k, (s, w) in RE.items()}
assert sum(1 for v in share_w.values() if v > F(2, 5)) == 3 and share_w["State A"] == F(2, 5)
Q(T, "Stacked or grouped bar", I,
  "In how many of the five states did wind make up more than 40% of the new capacity added?",
  "3", ["4", "2", "5"],
  "Wind share = wind ÷ (solar + wind) for each state; 'more than 40%' excludes exactly 40%",
  "Wind shares: A 800/2,000 = 40% (not more); B 1,500/2,400 = 62.5%; C 450/2,100 ≈ 21.4%; D 1,200/1,800 ≈ 66.7%; "
  "E 1,150/2,500 = 46%. Three states (B, D, E) exceed 40%.",
  ["A: 40% ✗", "B: 62.5% ✓", "C: 21.4% ✗", "D: 66.7% ✓", "E: 46% ✓"],
  why="4 counts State A, whose share is exactly 40%; 2 misses State E (46%); 5 counts every state.", secs=60,
  stim=sid)

gen = {k: s * F(16, 10) + w * F(24, 10) for k, (s, w) in RE.items()}
assert max(gen, key=gen.get) == "State B" and gen["State B"] == 5040 and gen["State E"] == 4920
Q(T, "Stacked or grouped bar", A,
  "Each MW of solar capacity generates 1.6 million units (MU) of electricity a year and each MW of wind capacity "
  "2.4 MU a year. Which state's new capacity will generate the most electricity in a year?",
  "State B", ["State E", "State C", "State D"],
  "Generation = solar MW × 1.6 + wind MW × 2.4; the state with the most MW need not generate the most",
  "Generation (MU): A 1,920 + 1,920 = 3,840; B 1,440 + 3,600 = 5,040; C 2,640 + 1,080 = 3,720; D 960 + 2,880 = 3,840; "
  "E 2,160 + 2,760 = 4,920. State B generates the most.",
  ["A 3,840", "B 5,040", "C 3,720", "D 3,840", "E 4,920"],
  why="State E adds the most capacity (2,500 MW) but much of it is solar (4,920 MU); State C adds the most solar but "
      "generates only 3,720 MU; State D has the highest wind share but a small total (3,840 MU).", secs=90, stim=sid)

cost = {k: s * F(42, 10) + w * F(65, 10) for k, (s, w) in RE.items()}
assert cost["State A"] == 10240 and cost["State E"] == 13145
assert pct2((cost["State E"] - cost["State A"]) / cost["State A"]) == "28.37%" and pct2(F(2905, 13145)) == "22.10%"
Q(T, "Stacked or grouped bar", A,
  "Solar capacity costs ₹4.2 crore per MW to set up and wind capacity ₹6.5 crore per MW. The investment in State E's "
  "new capacity is what percentage more than that in State A's (correct to two decimal places)?",
  "28.37%", ["25.00%", "22.10%", "43.75%"],
  "Price the solar and wind parts separately for each state, then compare the totals",
  "State E: 1,350 × 4.2 + 1,150 × 6.5 = 5,670 + 7,475 = ₹13,145 crore. State A: 1,200 × 4.2 + 800 × 6.5 = 5,040 + "
  "5,200 = ₹10,240 crore. E is 2,905 ÷ 10,240 = 28.37% more.",
  ["E: 5,670 + 7,475 = 13,145", "A: 5,040 + 5,200 = 10,240", "2,905 ÷ 10,240 = 28.37%"],
  why="25.00% compares the capacities (2,500 vs 2,000 MW) and ignores the different costs; 22.10% divides the "
      "difference by E's investment instead of A's; 43.75% compares only the wind parts (1,150 vs 800 MW).", secs=100,
  stim=sid)

# ================================================================ Pie Chart DI (B3 I3 A1): sets of 4 and 3
T = "Pie Chart DI"
OPD = {"General Medicine": 108, "Paediatrics": 54, "Orthopaedics": 45, "Gynaecology": 63, "ENT": 27,
       "Dermatology": 36, "Ophthalmology": 27}
assert sum(OPD.values()) == 360
sid = stimulus("chart", "Out-patients at a district hospital by department, October 2026 (central angles)",
               "The pie chart shows how the 7,200 out-patients who visited a district hospital in October 2026 were "
               "distributed among seven departments. Each sector's central angle (in degrees) is given.\n\n" +
               md_table(["Department", "Central angle (degrees)"], [[k, v] for k, v in OPD.items()]),
               {"chart_type": "pie", "unit": "degrees", "total": 7200, "labels": list(OPD),
                "values": list(OPD.values())})
pat = {k: F(v, 360) * 7200 for k, v in OPD.items()}
assert pat["Orthopaedics"] == 900 and pat["Paediatrics"] == 1080 and 45 * 10 == 450
Q(T, "Degree-based", B, "How many out-patients visited the Orthopaedics department?",
  "900", ["1,080", "450", "4,500"],
  "Number = (central angle ÷ 360) × total",
  "Orthopaedics: 45/360 × 7,200 = 900 patients.",
  ["45 ÷ 360 = 1/8", "7,200 ÷ 8 = 900"],
  why="1,080 is the Paediatrics figure; 450 and 4,500 multiply the angle by 10 or 100 instead of scaling by 7,200/360 "
      "= 20.", secs=30, stim=sid)

assert F(63, 360) * 100 == F(35, 2) and F(63, 300) * 100 == 21
Q(T, "Degree-based", B, "What percentage of the out-patients visited the Gynaecology department?",
  "17.5%", ["63%", "21%", "12.6%"],
  "Percentage = angle ÷ 360 × 100",
  "63 ÷ 360 × 100 = 17.5%.",
  ["63 ÷ 360 = 0.175", "= 17.5%"],
  why="63% reads the angle as a percentage; 21% divides by 300 instead of 360; 12.6% divides by 500.", secs=30,
  stim=sid)

assert (pat["Paediatrics"] - pat["Dermatology"]) / pat["Paediatrics"] * 100 == F(100, 3)
assert (pat["Paediatrics"] - pat["Dermatology"]) / pat["Dermatology"] * 100 == 50
Q(T, "Degree-based", I,
  "The number of Dermatology patients is what percentage less than the number of Paediatrics patients?",
  "33⅓%", ["50%", "18%", "66⅔%"],
  "Percentage less = difference ÷ the larger (base) value × 100; angles can be compared directly",
  "Dermatology 36° (720 patients), Paediatrics 54° (1,080). Difference = 18° on 54° = 1/3 = 33⅓% less.",
  ["Angles 36° and 54°", "Difference 18°", "18 ÷ 54 = 33⅓%"],
  why="50% divides the difference by Dermatology's angle; 18% takes the 18° gap as a percentage; 66⅔% is Dermatology "
      "as a percentage of Paediatrics.", secs=45, stim=sid)

gm = pat["General Medicine"]
fee = gm * F(3, 4) * 300 + gm * F(1, 4) * 150 + (7200 - gm) * 500
assert gm == 2160 and fee == 3087000 and gm * 300 + (7200 - gm) * 500 == 3168000 and 7200 * 500 == 3600000
Q(T, "Degree-based", A,
  "The consultation fee is ₹300 in General Medicine and ₹500 in every other department. A quarter of the General "
  "Medicine patients were senior citizens, who paid half the fee. What was the total fee collected in October?",
  "₹30,87,000", ["₹31,68,000", "₹36,00,000", "₹25,20,000"],
  "Find the General Medicine patients, split them into full-fee and half-fee, and price the other departments at "
  "₹500",
  "General Medicine: 108/360 × 7,200 = 2,160 patients. Fee: 1,620 × 300 + 540 × 150 = 4,86,000 + 81,000 = ₹5,67,000. "
  "Other departments: 5,040 × 500 = ₹25,20,000. Total = ₹30,87,000.",
  ["GM = 2,160", "GM fees = 4,86,000 + 81,000 = 5,67,000", "Others = 5,040 × 500 = 25,20,000", "Total = 30,87,000"],
  why="₹31,68,000 ignores the senior citizens' half fee; ₹36,00,000 charges every patient ₹500; ₹25,20,000 leaves out "
      "General Medicine altogether.", secs=95, stim=sid)

LB25 = {"Agriculture": 18, "MSME": 22, "Housing": 25, "Personal": 15, "Corporate": 20}
LB26 = {"Agriculture": 16, "MSME": 24, "Housing": 28, "Personal": 14, "Corporate": 18}
assert sum(LB25.values()) == sum(LB26.values()) == 100
sid = stimulus("chart", "Loan book of a small finance bank by sector, March 2025 and March 2026 (two pie charts)",
               "Two pie charts show how a small finance bank's outstanding loans were divided among five sectors: "
               "₹2,400 crore in all on 31 March 2025 and ₹3,000 crore in all on 31 March 2026 (percentages of each "
               "year's total).\n\n" +
               md_table(["Sector", "March 2025 (% of ₹2,400 crore)", "March 2026 (% of ₹3,000 crore)"],
                        [[k, LB25[k], LB26[k]] for k in LB25]),
               {"chart_type": "two_pies", "unit": "percent",
                "pies": [{"name": "March 2025", "total_rs_crore": 2400, "labels": list(LB25),
                          "values": list(LB25.values())},
                         {"name": "March 2026", "total_rs_crore": 3000, "labels": list(LB26),
                          "values": list(LB26.values())}]})
a25 = {k: F(2400 * v, 100) for k, v in LB25.items()}
a26 = {k: F(3000 * v, 100) for k, v in LB26.items()}
assert a26["Housing"] == 840 and F(2400 * 28, 100) == 672 and F(3000 * 25, 100) == 750 and a25["Housing"] == 600
Q(T, "Two pie charts", B, "What was the amount of housing loans outstanding in March 2026?",
  "₹840 crore", ["₹672 crore", "₹750 crore", "₹600 crore"],
  "Use each year's own total with that year's percentage",
  "March 2026: 28% of ₹3,000 crore = ₹840 crore.",
  ["28% of 3,000 = 840"],
  why="₹672 crore applies 2026's 28% to 2025's total; ₹750 crore applies 2025's 25% to 2026's total; ₹600 crore is "
      "the March 2025 figure.", secs=30, stim=sid)

gr = {k: (a26[k] - a25[k]) / a25[k] for k in LB25}
assert max(gr, key=gr.get) == "Housing" and gr["Housing"] == F(2, 5) and r2(gr["MSME"] * 100) == F(3636, 100)
assert r2(gr["Agriculture"] * 100) == F(1111, 100) and r2(gr["Personal"] * 100) == F(1667, 100)
Q(T, "Two pie charts", I, "Which sector's loans grew the most, in percentage terms, from March 2025 to March 2026?",
  "Housing", ["MSME", "Personal", "Agriculture"],
  "Convert both years' percentages to rupees before comparing growth; shares of different totals cannot be compared "
  "directly",
  "Amounts (₹ crore) 2025 → 2026: Agriculture 432 → 480 (+11.1%), MSME 528 → 720 (+36.4%), Housing 600 → 840 (+40%), "
  "Personal 360 → 420 (+16.7%), Corporate 480 → 540 (+12.5%). Housing grew the most.",
  ["Agriculture +11.1%", "MSME +36.4%", "Housing +40%", "Personal +16.7%", "Corporate +12.5%"],
  why="MSME grew 36.4%, second to housing; Personal grew only 16.7% even though its amount rose; Agriculture's share "
      "fell and its amount rose just 11.1%.", secs=65, stim=sid)

nh25, nh26 = 2400 - a25["Housing"], 3000 - a26["Housing"]
assert 3000 * F(75, 100) - 1800 == 450
assert (nh25, nh26) == (1800, 2160) and nh26 - nh25 == 360 and a26["Housing"] - a25["Housing"] == 240
Q(T, "Two pie charts", I,
  "By how much did the loans outstanding in all sectors other than housing increase from March 2025 to March 2026?",
  "₹360 crore", ["₹600 crore", "₹240 crore", "₹450 crore"],
  "Non-housing loans = total − housing, for each year",
  "March 2025: 2,400 − 600 = ₹1,800 crore. March 2026: 3,000 − 840 = ₹2,160 crore. Increase = ₹360 crore.",
  ["2025: 2,400 − 600 = 1,800", "2026: 3,000 − 840 = 2,160", "Increase = 360"],
  why="₹600 crore is the increase in the whole loan book; ₹240 crore is the increase in housing loans alone; ₹180 "
      "crore applies the 2025 non-housing share (75%) to the 2026 total (2,250 − 1,800).", secs=55,
  stim=sid)

# ================================================================ Line Graph DI (B1 I4 A4): sets of 5 and 4
T = "Line Graph DI"
CG = {"Jan": 900, "Feb": 765, "Mar": 918, "Apr": 1071, "May": 918, "Jun": 1224}
sid = stimulus("chart", "Cargo handled at a minor port, January to June 2026",
               "The line graph shows the cargo handled (in thousand tonnes) at a minor port in each month from "
               "January to June 2026 (values read from the graph).\n\n" +
               md_table(["Month", "Cargo (thousand tonnes)"], [[k, ind(v)] for k, v in CG.items()]),
               {"chart_type": "line", "x": list(CG), "series": [{"name": "Cargo (thousand tonnes)",
                                                                 "values": list(CG.values())}]})
q1, q2 = CG["Jan"] + CG["Feb"] + CG["Mar"], CG["Apr"] + CG["May"] + CG["Jun"]
assert (q1, q2) == (2583, 3213) and CG["Mar"] + CG["Apr"] + CG["May"] == 2907
Q(T, "Single line", B, "How much cargo did the port handle in the second quarter (April to June)?",
  "3,213 thousand tonnes", ["2,583 thousand tonnes", "2,907 thousand tonnes", "1,224 thousand tonnes"],
  "Add the three monthly points of the quarter",
  "April 1,071 + May 918 + June 1,224 = 3,213 thousand tonnes.",
  ["1,071 + 918 + 1,224 = 3,213"],
  why="2,583 is the first quarter's total; 2,907 adds March to May; 1,224 is June alone.", secs=35, stim=sid)

ms = list(CG)
pc = {ms[i]: F(CG[ms[i]] - CG[ms[i - 1]], CG[ms[i - 1]]) for i in range(1, 6)}
falls = {m: c for m, c in pc.items() if c < 0}
assert min(falls, key=falls.get) == "Feb" and pc["Feb"] == F(-3, 20) and CG["Apr"] - CG["May"] == 153 > CG["Jan"] - CG["Feb"]
Q(T, "Single line", I, "In which month was the percentage fall in cargo, compared with the previous month, the largest?",
  "February", ["May", "June", "April"],
  "Percentage fall = fall ÷ previous month's value; the biggest drop in tonnes need not be the biggest in percent",
  "Falls: February 900 → 765, a fall of 135 on 900 = 15%; May 1,071 → 918, a fall of 153 on 1,071 ≈ 14.3%. The other "
  "months rose. The largest percentage fall is in February.",
  ["Feb: −135 on 900 = −15%", "May: −153 on 1,071 ≈ −14.3%", "Mar, Apr, Jun: rises"],
  why="May has the larger fall in tonnes (153) but the smaller fall in percent; June and April were months of rising "
      "cargo.", secs=55, stim=sid)

avg_ = F(sum(CG.values()), 6)
assert avg_ == 966 and F(q1, 3) == 861 and F(q2, 3) == 1071 and F(900 + 1224, 2) == 1062
Q(T, "Single line", I, "What was the average monthly cargo handled over the six months?",
  "966 thousand tonnes", ["861 thousand tonnes", "1,071 thousand tonnes", "1,062 thousand tonnes"],
  "Average = sum of the six values ÷ 6",
  "Sum = 900 + 765 + 918 + 1,071 + 918 + 1,224 = 5,796, so the average = 5,796 ÷ 6 = 966 thousand tonnes.",
  ["Sum = 5,796", "÷ 6 = 966"],
  why="861 is the first quarter's average; 1,071 is the second quarter's average; 1,062 averages only January and "
      "June.", secs=50, stim=sid)

assert pct2(F(q2, q1 + q2)) == "55.43%" and pct2(F(q1, q1 + q2)) == "44.57%" and pct2(F(q2, q1)) == "124.39%"
Q(T, "Single line", I,
  "What percentage of the six months' cargo was handled in the second quarter (correct to two decimal places)?",
  "55.43%", ["44.57%", "124.39%", "50.00%"],
  "Share = quarter total ÷ six-month total × 100",
  "Second quarter = 3,213; six-month total = 5,796. Share = 3,213 ÷ 5,796 = 55.43%.",
  ["Q2 = 3,213", "Total = 5,796", "3,213 ÷ 5,796 = 55.43%"],
  why="44.57% is the first quarter's share; 124.39% compares the second quarter with the first; 50.00% assumes the "
      "two quarters were equal.", secs=55, stim=sid)

c1, c2 = q1 * F(40, 100), q2 * F(45, 100)
assert pct2((c2 - c1) / c1) == "39.94%" and pct2(F(q2 - q1, q1)) == "24.39%"
Q(T, "Single line", A,
  "Containers made up 40% of the cargo in the first quarter and 45% in the second quarter. By what percentage did the "
  "container cargo increase from the first quarter to the second (correct to two decimal places)?",
  "39.94%", ["12.50%", "24.39%", "5.00%"],
  "Container cargo = share × quarter total; then compare the two quarters",
  "Q1: 40% of 2,583 = 1,033.2 thousand tonnes. Q2: 45% of 3,213 = 1,445.85. Increase = 412.65 ÷ 1,033.2 = 39.94%.",
  ["Q1: 0.40 × 2,583 = 1,033.2", "Q2: 0.45 × 3,213 = 1,445.85", "412.65 ÷ 1,033.2 = 39.94%"],
  short="Growth factor = (3,213 ÷ 2,583) × (45 ÷ 40) = 1.2439 × 1.125 = 1.3994.",
  why="12.50% compares only the shares (45 ÷ 40); 24.39% is the growth of all cargo; 5.00% is the rise in the share "
      "in percentage points.", secs=95, stim=sid)

GRW = {"2022": (10, 25), "2023": (20, 20), "2024": (10, -4), "2025": (25, F(25, 2))}
sid = stimulus("chart", "Yearly growth in savings accounts at two banks, 2022 to 2025",
               "The line graph shows the percentage growth (over the previous year) in the number of savings "
               "accounts of Bank P and Bank Q for each year from 2022 to 2025. A negative value means the number "
               "fell. At the end of 2021, Bank P had 50 lakh savings accounts and Bank Q had 40 lakh.\n\n" +
               md_table(["Year", "Bank P growth (%)", "Bank Q growth (%)"],
                        [[k, N(p), N(q)] for k, (p, q) in GRW.items()]),
               {"chart_type": "line", "x": list(GRW), "unit": "percent growth over previous year",
                "base_2021_lakh": {"Bank P": 50, "Bank Q": 40},
                "series": [{"name": "Bank P", "values": [float(v[0]) for v in GRW.values()]},
                           {"name": "Bank Q", "values": [float(v[1]) for v in GRW.values()]}]})
P_, Q_ = {"2021": F(50)}, {"2021": F(40)}
for y, (p, q) in GRW.items():
    prev = str(int(y) - 1)
    P_[y], Q_[y] = P_[prev] * (1 + F(p) / 100), Q_[prev] * (1 + F(q) / 100)
assert P_ == {"2021": 50, "2022": 55, "2023": 66, "2024": F(363, 5), "2025": F(363, 4)}
assert Q_ == {"2021": 40, "2022": 50, "2023": 60, "2024": F(288, 5), "2025": F(324, 5)}
assert 40 * F(145, 100) == 58 and 40 * F(12, 10) == 48
Q(T, "Multiple lines", I, "How many savings accounts did Bank Q have at the end of 2023?",
  "60 lakh", ["58 lakh", "48 lakh", "66 lakh"],
  "Apply each year's growth rate in turn to the previous year's number",
  "Bank Q: 2021: 40 lakh; 2022: 40 × 1.25 = 50 lakh; 2023: 50 × 1.20 = 60 lakh.",
  ["2022: 40 × 1.25 = 50", "2023: 50 × 1.20 = 60"],
  why="58 lakh adds the two rates (45%) instead of compounding them; 48 lakh applies only the 2023 rate to the 2021 "
      "figure; 66 lakh is Bank P's figure for 2023.", secs=55, stim=sid)

assert (P_["2025"] - 50) / 50 * 100 == F(163, 2) and (P_["2024"] - 50) / 50 * 100 == F(226, 5)
Q(T, "Multiple lines", A, "By what percentage did Bank P's number of savings accounts grow from 2021 to 2025?",
  "81.5%", ["65%", "90.75%", "45.2%"],
  "Growth rates over successive years multiply; they do not add",
  "Bank P: 50 → 55 → 66 → 72.6 → 90.75 lakh. Growth = 40.75 ÷ 50 = 81.5%. (Factor 1.1 × 1.2 × 1.1 × 1.25 = 1.815.)",
  ["50 × 1.1 = 55", "55 × 1.2 = 66", "66 × 1.1 = 72.6", "72.6 × 1.25 = 90.75", "90.75 ÷ 50 = 1.815 ⇒ 81.5%"],
  why="65% adds the four yearly rates; 90.75% confuses the 2025 number of accounts (in lakh) with the growth; 45.2% "
      "stops at 2024.", secs=85, stim=sid)

assert min(["2022", "2023", "2024", "2025"], key=lambda y: Q_[y]) == "2022"
Q(T, "Multiple lines", A, "In which year from 2022 to 2025 did Bank Q have the fewest savings accounts?",
  "2022", ["2024", "2025", "2023"],
  "The graph shows growth rates, not numbers: a positive rate means the number still rose",
  "Bank Q's accounts: 2022: 50 lakh; 2023: 60; 2024: 57.6; 2025: 64.8. The fewest were in 2022, even though its "
  "growth rate (25%) was the highest.",
  ["2022: 50", "2023: 60", "2024: 57.6", "2025: 64.8"],
  why="2024 is the only year of decline, but 57.6 lakh is still above 2022's 50 lakh; 2025 has a low growth rate but "
      "the most accounts; 2023 has 60 lakh.", secs=80, stim=sid)

zb = P_["2025"] * F(30, 100) + Q_["2025"] * F(25, 100)
assert pct2(zb / (P_["2025"] + Q_["2025"])) == "27.92%" and pct2(F(25, 90)) == "27.78%"
Q(T, "Multiple lines", A,
  "At the end of 2025, 30% of Bank P's savings accounts and 25% of Bank Q's were zero-balance accounts. What "
  "percentage of the two banks' combined savings accounts were zero-balance (correct to two decimal places)?",
  "27.92%", ["27.50%", "27.78%", "55.00%"],
  "Find both banks' 2025 numbers, then take a weighted average of the two percentages",
  "2025: Bank P 90.75 lakh, Bank Q 64.8 lakh. Zero-balance: 27.225 + 16.2 = 43.425 lakh out of 155.55 lakh = 27.92%.",
  ["P 2025 = 90.75, Q 2025 = 64.8", "Zero-balance = 27.225 + 16.2 = 43.425", "43.425 ÷ 155.55 = 27.92%"],
  why="27.50% is the simple average of 30% and 25%; 27.78% weights them by the 2021 numbers (50 and 40 lakh); 55.00% "
      "adds the two percentages.", secs=100, stim=sid)

# ================================================================ Caselet DI (B2 I2 A1): one set of 5
T = "Caselet DI"
sid = stimulus("caselet", "Flats, tenants and maintenance charges in a housing society",
               "A housing society has 240 flats: 1BHK, 2BHK and 3BHK flats in the ratio 3 : 5 : 4. Of these, 40% of "
               "the 1BHK flats, 30% of the 2BHK flats and 25% of the 3BHK flats are let out to tenants; the rest "
               "are occupied by their owners. The monthly maintenance charge is ₹2,000 for a 1BHK, ₹3,000 for a "
               "2BHK and ₹4,500 for a 3BHK flat. For every flat let out to a tenant, the society also collects a "
               "non-occupancy charge of 10% of that flat's maintenance charge each month.")
cnt = {"1": 60, "2": 100, "3": 80}
assert [240 * F(r, 12) for r in (3, 5, 4)] == [60, 100, 80]
ten = {"1": 24, "2": 30, "3": 20}
assert ten == {k: cnt[k] * F(p, 100) for k, p in (("1", 40), ("2", 30), ("3", 25))}
Q(T, "Paragraph data", B, "How many 2BHK flats are occupied by their owners?",
  "70", ["30", "100", "60"],
  "2BHK flats = 5/12 of 240; owners occupy the 70% that are not let out",
  "2BHK flats = 5/12 × 240 = 100; 30% (30) are let out, so 70 are owner-occupied.",
  ["2BHK = 100", "Let out = 30", "Owner-occupied = 70"],
  why="30 is the number let out; 100 is all the 2BHK flats; 60 is the number of 1BHK flats.", secs=35, stim=sid)

assert sum(ten.values()) == 74 and 240 * F(30, 100) == 72 and 240 - 74 == 166 and F(40 + 30 + 25, 300) * 240 == 76
Q(T, "Paragraph data", B, "How many flats in all are let out to tenants?",
  "74", ["72", "166", "76"],
  "Apply each type's own percentage to that type's number of flats",
  "1BHK: 40% of 60 = 24; 2BHK: 30% of 100 = 30; 3BHK: 25% of 80 = 20. Total let out = 74.",
  ["24 + 30 + 20 = 74"],
  why="72 applies the 2BHK rate (30%) to all 240 flats; 166 is the number of owner-occupied flats; 76 applies the "
      "simple average of the three rates (31⅔%) to all 240 flats.", secs=45, stim=sid)

rate = {"1": 2000, "2": 3000, "3": 4500}
base = sum(cnt[k] * rate[k] for k in cnt)
extra = sum(ten[k] * rate[k] // 10 for k in cnt)
assert (base, extra) == (780000, 22800) and base + extra == 802800 and base * F(11, 10) == 858000
Q(T, "Paragraph data", I, "What is the total amount the society collects each month (maintenance plus non-occupancy charges)?",
  "₹8,02,800", ["₹7,80,000", "₹8,58,000", "₹7,57,200"],
  "Maintenance on all 240 flats, plus 10% extra on the let-out flats only",
  "Maintenance: 60 × 2,000 + 100 × 3,000 + 80 × 4,500 = 1,20,000 + 3,00,000 + 3,60,000 = ₹7,80,000. Non-occupancy: "
  "24 × 200 + 30 × 300 + 20 × 450 = 4,800 + 9,000 + 9,000 = ₹22,800. Total = ₹8,02,800.",
  ["Maintenance = 7,80,000", "Non-occupancy = 22,800", "Total = 8,02,800"],
  why="₹7,80,000 forgets the non-occupancy charge; ₹8,58,000 adds 10% on every flat; ₹7,57,200 subtracts the "
      "non-occupancy charge instead of adding it.", secs=70, stim=sid)

t3 = ten["3"] * 4500 * F(11, 10)
o1 = (cnt["1"] - ten["1"]) * 2000
assert (t3, o1) == (99000, 72000) and F(t3, o1) == F(11, 8) and F(20 * 4500, 72000) == F(5, 4)
Q(T, "Paragraph data", I,
  "What is the ratio of the total monthly amount paid for the let-out 3BHK flats to that paid for the owner-occupied "
  "1BHK flats?",
  "11 : 8", ["5 : 4", "5 : 9", "99 : 40"],
  "Each let-out flat pays its maintenance × 1.1; owner-occupied flats pay maintenance only",
  "Let-out 3BHK: 20 × 4,500 × 1.1 = ₹99,000. Owner-occupied 1BHK: 36 × 2,000 = ₹72,000. Ratio = 99,000 : 72,000 = "
  "11 : 8.",
  ["Let-out 3BHK = 20 × 4,950 = 99,000", "Owner 1BHK = 36 × 2,000 = 72,000", "99 : 72 = 11 : 8"],
  why="5 : 4 forgets the 10% non-occupancy charge (90,000 : 72,000); 5 : 9 compares the numbers of flats (20 : 36); "
      "99 : 40 compares the charge for a single flat (4,950 : 2,000).", secs=65, stim=sid)

new_rate = {"1": 2160, "2": 3360, "3": 5040}
ten2 = {"1": 24, "2": 30, "3": 26}
total2 = sum(cnt[k] * new_rate[k] + ten2[k] * new_rate[k] // 10 for k in cnt)
assert total2 == 897168 and total2 - 6 * 504 == 894144 and sum(cnt[k] * new_rate[k] for k in cnt) == 868800
assert 60 * 2240 + 24 * 224 + 346080 + 416304 == 902160
Q(T, "Paragraph data", A,
  "Next year the maintenance charge rises by 8% for 1BHK flats and by 12% for 2BHK and 3BHK flats, and 6 more 3BHK "
  "flats that are now owner-occupied are let out to tenants. Nothing else changes. What will the society's total "
  "monthly collection then be?",
  "₹8,97,168", ["₹8,94,144", "₹8,68,800", "₹9,02,160"],
  "Recompute each type's charge, then add 10% for each let-out flat at the new charge",
  "New charges: 1BHK ₹2,160, 2BHK ₹3,360, 3BHK ₹5,040. Maintenance: 60 × 2,160 + 100 × 3,360 + 80 × 5,040 = 1,29,600 + "
  "3,36,000 + 4,03,200 = ₹8,68,800. Non-occupancy: 24 × 216 + 30 × 336 + 26 × 504 = 5,184 + 10,080 + 13,104 = "
  "₹28,368. Total = ₹8,97,168.",
  ["New charges: 2,160 / 3,360 / 5,040", "Maintenance = 8,68,800", "Let out: 24, 30, 26", "Extra = 28,368",
   "Total = 8,97,168"],
  why="₹8,94,144 forgets the 6 newly let-out 3BHK flats; ₹8,68,800 leaves out the non-occupancy charge; ₹9,02,160 "
      "raises the 1BHK charge by 12% instead of 8%.", secs=110, stim=sid)

# ================================================================ Missing DI (B1 I2 A2): one set of 5
T = "Missing DI"
dash = "—"
NPA = {"Branch K": (400, 18, None, F(108, 10), None), "Branch L": (None, 15, 5, None, 60),
       "Branch M": (500, None, F(32, 10), 12, None), "Branch N": (250, 20, None, None, 80),
       "Branch O": (None, None, 6, F(27, 2), 75)}
sid = stimulus("data_table", "Advances, NPAs and provisions at five bank branches (some values missing)",
               "The table shows, for five branches of a bank on 31 March 2026, the gross advances (₹ crore), the gross "
               "non-performing assets or NPAs (₹ crore), the gross NPA ratio (NPAs as a percentage of advances), the "
               "provisions held against NPAs (₹ crore) and the provision coverage (provisions as a percentage of "
               "NPAs). Some values are missing (—); work them out from the others.\n\n" +
               md_table(["Branch", "Gross advances (₹ crore)", "Gross NPAs (₹ crore)", "Gross NPA ratio (%)",
                         "Provisions (₹ crore)", "Provision coverage (%)"],
                        [[k, *[dash if c is None else N(c) for c in v]] for k, v in NPA.items()]),
               {"columns": ["branch", "advances_cr", "gross_npa_cr", "gross_npa_pct", "provisions_cr", "coverage_pct"],
                "rows": [[k, *[None if c is None else float(c) for c in v]] for k, v in NPA.items()]})
adv = {"Branch K": F(400), "Branch L": F(15) / F(5, 100), "Branch M": F(500), "Branch N": F(250),
       "Branch O": F(27, 2) / F(75, 100) / F(6, 100)}
npa = {"Branch K": F(18), "Branch L": F(15), "Branch M": F(500) * F(32, 1000), "Branch N": F(20),
       "Branch O": F(27, 2) / F(75, 100)}
prov = {"Branch K": F(108, 10), "Branch L": F(15) * F(60, 100), "Branch M": F(12), "Branch N": F(20) * F(80, 100),
        "Branch O": F(27, 2)}
assert adv == {"Branch K": 400, "Branch L": 300, "Branch M": 500, "Branch N": 250, "Branch O": 300}
assert npa == {"Branch K": 18, "Branch L": 15, "Branch M": 16, "Branch N": 20, "Branch O": 18}
assert prov["Branch L"] == 9 and prov["Branch N"] == 16 and F(18, 400) * 100 == F(9, 2) and F(108, 10) / 400 * 100 == F(27, 10)
Q(T, "Table with missing values", B, "What was the gross NPA ratio of Branch K?",
  "4.5%", ["45%", "60%", "2.7%"],
  "Gross NPA ratio = gross NPAs ÷ gross advances × 100",
  "Branch K: 18 ÷ 400 × 100 = 4.5%.",
  ["18 ÷ 400 = 0.045 = 4.5%"],
  why="45% misplaces the decimal point; 60% is Branch K's provision coverage (10.8 ÷ 18); 2.7% divides the "
      "provisions, not the NPAs, by the advances.", secs=35, stim=sid)

assert 15 * 5 == 75 and F(15, 60, ) * 100 == 25
Q(T, "Table with missing values", I, "What were the gross advances of Branch L?",
  "₹300 crore", ["₹75 crore", "₹3,000 crore", "₹25 crore"],
  "Advances = NPAs ÷ (NPA ratio ÷ 100)",
  "NPAs of ₹15 crore are 5% of advances, so advances = 15 ÷ 0.05 = ₹300 crore.",
  ["15 = 5% of advances", "Advances = 15 × 100 ÷ 5 = 300"],
  why="₹75 crore multiplies 15 by 5 instead of dividing by 5%; ₹3,000 crore slips a zero; ₹25 crore uses the 60% "
      "coverage (15 ÷ 0.6), which relates provisions to NPAs, not NPAs to advances.", secs=45, stim=sid)

assert npa["Branch N"] - prov["Branch N"] == 4 and 250 * F(80, 100) == 200
Q(T, "Table with missing values", I, "What were the provisions held by Branch N?",
  "₹16 crore", ["₹20 crore", "₹4 crore", "₹200 crore"],
  "Provisions = NPAs × coverage ÷ 100",
  "Branch N's NPAs are ₹20 crore and its coverage is 80%, so provisions = 0.8 × 20 = ₹16 crore.",
  ["Provisions = 80% of 20 = 16"],
  why="₹20 crore is the NPA amount itself; ₹4 crore is the uncovered part (20 − 16); ₹200 crore applies 80% to the "
      "advances instead of the NPAs.", secs=40, stim=sid)

ta, tn, tp_ = sum(adv.values()), sum(npa.values()), sum(prov.values())
assert (ta, tn, tp_) == (1750, 87, F(613, 10))
assert pct2(tn / ta) == "4.97%" and F(45 + 50 + 32 + 80 + 60, 50) == F(267, 50) and pct2(F(69, 1450)) == "4.76%"
assert pct2(tp_ / ta) == "3.50%"
Q(T, "Table with missing values", A,
  "Taking the five branches together, what was the overall gross NPA ratio (correct to two decimal places)?",
  "4.97%", ["5.34%", "4.76%", "3.50%"],
  "Fill in the missing advances and NPAs first; the overall ratio is total NPAs ÷ total advances",
  "Missing values: L's advances 300; M's NPAs 3.2% of 500 = 16; O's NPAs 13.5 ÷ 0.75 = 18 and advances 18 ÷ 0.06 = "
  "300. Totals: advances 400 + 300 + 500 + 250 + 300 = 1,750; NPAs 18 + 15 + 16 + 20 + 18 = 87. Ratio = 87 ÷ 1,750 = "
  "4.97%.",
  ["L advances = 300", "M NPAs = 16", "O NPAs = 18, advances = 300", "Totals: 87 ÷ 1,750 = 4.97%"],
  why="5.34% is the simple average of the five ratios (4.5, 5, 3.2, 8, 6); 4.76% leaves out Branch O, whose values "
      "are missing; 3.50% divides total provisions, not NPAs, by advances.", secs=110, stim=sid)

net = {k: npa[k] - prov[k] for k in NPA}
netp = {k: net[k] / adv[k] for k in NPA}
assert max(netp, key=netp.get) == "Branch L" and max(net, key=net.get) == "Branch K" and netp["Branch L"] == F(2, 100)
assert max(npa[k] / adv[k] for k in NPA) == npa["Branch N"] / adv["Branch N"]
Q(T, "Table with missing values", A,
  "Net NPAs = gross NPAs − provisions. Which branch had the highest net NPAs as a percentage of its gross advances?",
  "Branch L", ["Branch K", "Branch N", "Branch O"],
  "Complete the table, compute net NPAs for each branch, then divide by that branch's advances",
  "Net NPAs (₹ crore) and % of advances: K 18 − 10.8 = 7.2 (1.8%); L 15 − 9 = 6 (2.0%); M 16 − 12 = 4 (0.8%); "
  "N 20 − 16 = 4 (1.6%); O 18 − 13.5 = 4.5 (1.5%). Branch L is the highest.",
  ["K: 7.2 ÷ 400 = 1.8%", "L: 6 ÷ 300 = 2.0%", "M: 4 ÷ 500 = 0.8%", "N: 4 ÷ 250 = 1.6%", "O: 4.5 ÷ 300 = 1.5%"],
  why="Branch K has the largest net NPAs in rupees (₹7.2 crore) but on larger advances; Branch N has the highest "
      "gross NPA ratio (8%) but strong 80% coverage; Branch O's net ratio is 1.5%.", secs=110, stim=sid)

# ================================================================ Quantity Comparison (B2 I7 A1)
T = "Quantity Comparison"
QREL = {">": "Quantity I > Quantity II", ">=": "Quantity I ≥ Quantity II", "<": "Quantity I < Quantity II",
        "<=": "Quantity I ≤ Quantity II", "cbe": "Quantity I = Quantity II or the relationship cannot be established"}


def qc(sub, diff, q1, q2, vals1, vals2, expect, wrong_syms, concept, expl, steps, short=None, why=None, secs=None,
       by=None):
    got = relation(vals1, vals2)
    assert got == expect, (q1, got)
    assert expect not in wrong_syms and "cbe" not in wrong_syms and len(set(wrong_syms)) == 2
    assert all(a != b for a in vals1 for b in vals2), "avoid exactly equal quantities"
    # new in batch 6: every pair at least 2% apart, so rounding in mental arithmetic cannot flip the relation
    assert all(abs(a - b) >= F(2, 100) * max(abs(a), abs(b)) for a in vals1 for b in vals2), (q1, q2)
    if expect == "cbe":
        third = next(s_ for s_ in (">", "<", ">=", "<=") if s_ not in wrong_syms)
        wrong = [QREL[wrong_syms[0]], QREL[wrong_syms[1]], QREL[third]]
        no_true_distractor(vals1, vals2, [*wrong_syms, third])
    else:
        wrong = [QREL[wrong_syms[0]], QREL["cbe"], QREL[wrong_syms[1]]]
        no_true_distractor(vals1, vals2, wrong_syms)
    Q(T, sub, diff, f"Compare the two quantities and choose the correct option.\nQuantity I: {q1}\nQuantity II: {q2}",
      QREL[expect], wrong, concept, expl, steps, short, why, secs, by=by)


q1v, q2v = F(8 * 5, 2), F(12 + 6)
assert (q1v, q2v) == (20, 18)
qc("Quantity I vs II", B, "The number of diagonals of an octagon",
   "The number of edges of a cube plus the number of faces of a cube", [q1v], [q2v], ">", ["<", "<="],
   "Diagonals of an n-sided polygon = n(n − 3)/2",
   "Quantity I = 8 × 5 ÷ 2 = 20. Quantity II = 12 edges + 6 faces = 18. So Quantity I > Quantity II.",
   ["I: 8(8 − 3)/2 = 20", "II: 12 + 6 = 18", "20 > 18"],
   why="'Quantity I < Quantity II' and '≤' come from halving the diagonal count twice (8 × 5 ÷ 4 = 10) or "
       "from counting the octagon's diagonals as n(n − 3) ÷ 2 with n = 6 (9).", secs=40)

q1v, q2v = F(15, 100) * F(15, 100) * 2000, F(math.isqrt(2209))
assert (q1v, q2v) == (45, 47)
qc("Quantity I vs II", B, "15% of 15% of 2,000", "The square root of 2,209", [q1v], [q2v], "<", [">", ">="],
   "Successive percentages multiply; 47² = 2,209",
   "Quantity I = 0.15 × 0.15 × 2,000 = 45. Quantity II = √2,209 = 47. So Quantity I < Quantity II.",
   ["I: 15% of 2,000 = 300; 15% of 300 = 45", "II: 47² = 2,209", "45 < 47"],
   why="'Quantity I > Quantity II' and '≥' come from taking 15% of 15% as 30% (600), or √2,209 as 43.", secs=40)

q1v = F(240) / (F(120, 40) + F(120, 60))
q2v = F(300, 20) * F(18, 5)
assert (q1v, q2v) == (48, 54)
qc("Arithmetic-based comparison", I,
   "Average speed (km/h) of a car that covers 120 km at 40 km/h and the next 120 km at 60 km/h",
   "Speed (km/h) of a 300 m long train that passes a signal pole in 20 seconds", [q1v], [q2v], "<", [">", ">="],
   "For equal distances the average speed is the harmonic mean 2ab/(a + b); 1 m/s = 3.6 km/h",
   "Quantity I = 240 km ÷ (3 h + 2 h) = 48 km/h. Quantity II = 300 ÷ 20 = 15 m/s = 54 km/h. So Quantity I < "
   "Quantity II.",
   ["I: 2 × 40 × 60/(40 + 60) = 48", "II: 15 m/s × 3.6 = 54", "48 < 54"],
   why="'Quantity I > Quantity II' and '≥' come from leaving the train's speed in m/s (15), which is then compared "
       "with 48 km/h.", secs=60)

xs_, ys_ = [F(8), F(12)], [F(11), F(15)]
roots_check(1, -20, 96, xs_), roots_check(1, -26, 165, ys_)
qc("Quantity I vs II", I, "The value of x, where x² − 20x + 96 = 0", "The value of y, where y² − 26y + 165 = 0",
   xs_, ys_, "cbe", [">", "<="],
   "Find all roots; if one root of I lies between the roots of II, no single relation holds",
   "I: (x − 8)(x − 12) = 0, so x = 8 or 12. II: (y − 11)(y − 15) = 0, so y = 11 or 15. x = 12 is above y = 11 but "
   "below y = 15, and x = 8 is below both. So the relationship cannot be established.",
   ["I: x = 8, 12", "II: y = 11, 15", "12 > 11 but 12 < 15", "Cannot be established"],
   why="'Quantity I > Quantity II' uses only x = 12 against y = 11; '≤' and '<' ignore the pair x = 12, y = 11.",
   secs=60)

q1v = F(2000) * F(117, 100) / F(90, 100)
q2v = F(2000) * F(11, 10) ** 3
assert (q1v, q2v) == (2600, 2662)
qc("Arithmetic-based comparison", I,
   "Marked price (₹) of an article that costs ₹2,000 and is sold at a 17% profit after a 10% discount",
   "Amount (₹) of ₹2,000 after 3 years at 10% per annum compound interest, compounded annually", [q1v], [q2v],
   "<", [">", ">="],
   "MP = SP ÷ (1 − discount); compound amount = P(1 + r)ⁿ",
   "Quantity I: SP = 2,000 × 1.17 = 2,340, so MP = 2,340 ÷ 0.9 = ₹2,600. Quantity II: 2,000 × 1.331 = ₹2,662. So "
   "Quantity I < Quantity II.",
   ["I: SP = 2,340; MP = 2,340 ÷ 0.9 = 2,600", "II: 2,000 × 1.1³ = 2,662", "2,600 < 2,662"],
   why="'Quantity I > Quantity II' and '≥' come from comparing the marked price with only the interest in II "
       "(₹662) instead of the amount (₹2,662).", secs=70)

a_, b_ = 40000 * 12, 60000 * 9
q1v = F(34000) * b_ / (a_ + b_)
q2v = F(45000) * F(8, 100) * F(9, 2)
assert (q1v, q2v) == (18000, 16200)
qc("Arithmetic-based comparison", I,
   "B's share (₹) of a profit of ₹34,000, if A invests ₹40,000 for 12 months and B invests ₹60,000 for 9 months",
   "Simple interest (₹) on ₹45,000 at 8% per annum for 4½ years", [q1v], [q2v], ">", ["<", "<="],
   "Profit shares ∝ capital × time; SI = PRT/100",
   "Quantity I: A 4,80,000, B 5,40,000, ratio 8 : 9, so B gets 34,000 × 9/17 = ₹18,000. Quantity II: 45,000 × 0.08 × "
   "4.5 = ₹16,200. So Quantity I > Quantity II.",
   ["I: 480 : 540 = 8 : 9 ⇒ B = 18,000", "II: 45,000 × 0.36 = 16,200", "18,000 > 16,200"],
   why="'Quantity I < Quantity II' and '≤' come from sharing the profit by time alone (12 : 9, so B gets "
       "34,000 × 9/21 ≈ 14,571).", secs=70)

q1v = F(2, 3) * F(22, 7) * 6 ** 3
q2v = F(1, 3) * F(22, 7) * 36 * 14
assert (q1v, q2v) == (F(3168, 7), 528)
qc("Quantity I vs II", I, "Volume (cm³) of a hemisphere of radius 6 cm (take π = 22/7)",
   "Volume (cm³) of a cone of base radius 6 cm and height 14 cm (take π = 22/7)", [q1v], [q2v], "<", [">", ">="],
   "Hemisphere: ⅔πr³; cone: ⅓πr²h",
   "Quantity I = ⅔ × 22/7 × 216 = 3,168/7 ≈ 452.57 cm³. Quantity II = ⅓ × 22/7 × 36 × 14 = 528 cm³. So Quantity I < "
   "Quantity II.",
   ["I: ⅔ × 22/7 × 216 ≈ 452.57", "II: ⅓ × 22/7 × 504 = 528", "452.57 < 528"],
   why="'Quantity I > Quantity II' and '≥' come from using the sphere's 4/3πr³ (905.14) for the hemisphere.",
   secs=60)

q1v = 1 / (F(1, 18) + F(1, 24))
q2v = 1 / (F(1, 15) + F(1, 20) - F(1, 60))
assert (q1v, q2v) == (F(72, 7), 10)
qc("Arithmetic-based comparison", I,
   "Days taken by A and B together to finish a job that A alone finishes in 18 days and B alone in 24 days",
   "Hours taken to fill a tank by two pipes that fill it in 15 and 20 hours, while a leak that empties the full tank "
   "in 60 hours is also open", [q1v], [q2v], ">", ["<", "<="],
   "Add the rates (subtract the leak's rate) and invert",
   "Quantity I = 1 ÷ (1/18 + 1/24) = 1 ÷ 7/72 = 72/7 ≈ 10.29 days. Quantity II = 1 ÷ (1/15 + 1/20 − 1/60) = 1 ÷ 6/60 "
   "= 10 hours. So Quantity I > Quantity II.",
   ["I: 1/18 + 1/24 = 7/72 ⇒ 10.29", "II: 4/60 + 3/60 − 1/60 = 6/60 ⇒ 10", "10.29 > 10"],
   why="'Quantity I < Quantity II' and '≤' come from rounding A and B's joint rate 7/72 up to 1/9, which gives 9 "
       "days for Quantity I.", secs=65)

ages = [(f, s) for s in range(1, 60) for f in [s * F(7, 3)] if f.denominator == 1 and f - 8 == 3 * (s - 8)]
q2v = F(ages[0][0])
q1v = F(5 * (1 + 20), 2)
assert ages == [(56, 24)] and q1v == F(105, 2)
qc("Arithmetic-based comparison", I, "The average of the first 20 multiples of 5",
   "A father's present age (years), if the ratio of the ages of the father and his son is 7 : 3 now and was 3 : 1 "
   "eight years ago", [q1v], [q2v], "<", [">", ">="],
   "Average of an arithmetic progression = (first + last) ÷ 2; set up the age ratio with a common multiplier",
   "Quantity I = (5 + 100) ÷ 2 = 52.5. Quantity II: father 7k, son 3k; 7k − 8 = 3(3k − 8) ⇒ 2k = 16 ⇒ k = 8, so the "
   "father is 56. So Quantity I < Quantity II.",
   ["I: (5 + 100)/2 = 52.5", "II: 7k − 8 = 9k − 24 ⇒ k = 8 ⇒ 56", "52.5 < 56"],
   why="'Quantity I > Quantity II' and '≥' come from using the father's age eight years ago (48) in II.", secs=70,
   by=BRUTE)

xs_ = [F(5, 2)]
assert 3 ** 5 * 9 ** 2 == 27 ** 3  # 3^(2.5) × 9 = 27^(1.5), squared: 3^5 × 81 = 27^3
ys_ = [F(2), F(3)]
roots_check(1, -5, 6, ys_)
qc("Quantity I vs II", A, "The value of x, where 3ˣ × 9 = 27^(x − 1)", "The value of y, where y² − 5y + 6 = 0",
   xs_, ys_, "cbe", [">", "<="],
   "Write every term as a power of 3 and equate exponents",
   "Quantity I: 3^(x + 2) = 3^(3x − 3), so x + 2 = 3x − 3 and x = 2.5. Quantity II: (y − 2)(y − 3) = 0, so y = 2 or "
   "3. 2.5 is above 2 but below 3, so the relationship cannot be established.",
   ["I: x + 2 = 3x − 3 ⇒ x = 2.5", "II: y = 2, 3", "2.5 > 2 but 2.5 < 3", "Cannot be established"],
   why="'Quantity I > Quantity II' compares 2.5 with y = 2 only; '≤' and '<' compare it with y = 3 only.", secs=85)

# ================================================================ Data Sufficiency (Quant) (B2 I3 A2)
T = "Data Sufficiency (Quant)"
DS2 = {"I": "Statement I alone is sufficient, but statement II alone is not",
       "II": "Statement II alone is sufficient, but statement I alone is not",
       "either": "Either statement I alone or statement II alone is sufficient",
       "both": "Both statements I and II together are needed",
       "neither": "Statements I and II together are not sufficient"}
DS_PRE = ("The question below is followed by two statements. Decide whether the data in the statements are "
          "sufficient to answer the question.")
DS3_PRE = "The question below is followed by three statements. Decide which statements are sufficient to answer it."


def ds2_verdict(cands, s1, s2, target):
    """Classify sufficiency by enumeration: a set of conditions is sufficient if the target value is unique."""
    def unique(conds):
        vals = {target(c) for c in cands if all(f(c) for f in conds)}
        assert vals, "no case satisfies the statements"
        return len(vals) == 1
    a, b, both = unique([s1]), unique([s2]), unique([s1, s2])
    if a and b:
        return "either"
    if a:
        return "I"
    if b:
        return "II"
    return "both" if both else "neither"


def suff_map(cands, conds, target):
    out = {}
    for r in (1, 2, 3):
        for sub in itertools.combinations(range(3), r):
            vals = {target(c) for c in cands if all(conds[i](c) for i in sub)}
            assert vals, sub
            out[sub] = len(vals) == 1
    return out


cands = [(F(b, 2), F(s, 2)) for b in range(1, 81) for s in range(1, 81) if b > s]
verdict = ds2_verdict(cands, lambda c: 2 * (c[0] + c[1]) == 30, lambda c: c[0] - c[1] == 10, lambda c: c[0])
assert verdict == "both"
Q(T, "Two-statement", B,
  f"{DS_PRE}\nQuestion: What is the speed of the boat in still water?\n"
  "I. The boat covers 30 km downstream in 2 hours.\n"
  "II. The boat's upstream speed is 10 km/h.",
  DS2["both"], [DS2["I"], DS2["II"], DS2["neither"]],
  "Still-water speed = (downstream speed + upstream speed) ÷ 2; both speeds are needed",
  "I gives the downstream speed, 15 km/h, but not the stream's speed. II gives only the upstream speed. Together: "
  "(15 + 10) ÷ 2 = 12.5 km/h.",
  ["I alone: b + s = 15 (one equation, two unknowns)", "II alone: b − s = 10", "Together: b = 12.5 km/h"],
  why="'I alone' and 'II alone' each give one equation in two unknowns (boat and stream); 'not sufficient even "
      "together' misses that the two equations solve directly.", secs=40, by=BRUTE)

cands = [F(k, 2) for k in range(1, 61)]
verdict = ds2_verdict(cands, lambda r: 2 * F(22, 7) * r == 44, lambda r: 2 * r == 14, lambda r: F(22, 7) * r * r)
assert verdict == "either"
Q(T, "Two-statement", B,
  f"{DS_PRE}\nQuestion: What is the area of the circle? (Use π = 22/7.)\n"
  "I. The circumference of the circle is 44 cm.\n"
  "II. The diameter of the circle is 14 cm.",
  DS2["either"], [DS2["I"], DS2["II"], DS2["both"]],
  "Any one measurement of a circle fixes its radius, and hence its area",
  "I: 2πr = 44 ⇒ r = 7 cm ⇒ area = 154 cm² — sufficient. II: r = 14 ÷ 2 = 7 cm ⇒ area 154 cm² — sufficient. Either "
  "statement alone answers the question.",
  ["I: 2 × 22/7 × r = 44 ⇒ r = 7", "II: r = 7", "Area = 154 cm² either way"],
  why="'I alone' or 'II alone' overlooks that the other statement also fixes the radius; 'both together' assumes the "
      "two must be combined.", secs=35, by=BRUTE)

cands = [(cp, sp) for cp in range(50, 1201, 50) for sp in range(50, 1201, 25)]
verdict = ds2_verdict(cands, lambda c: 12 * c[0] == 10 * c[1], lambda c: c[1] == 600,
                      lambda c: F(c[1] - c[0], c[0]) * 100)
assert verdict == "I"
Q(T, "Two-statement", I,
  f"{DS_PRE}\nQuestion: What is the profit percentage on the article?\n"
  "I. The cost price of 12 such articles equals the selling price of 10 of them.\n"
  "II. The selling price of the article is ₹600.",
  DS2["I"], [DS2["both"], DS2["II"], DS2["either"]],
  "A profit percentage needs only the ratio of SP to CP, not the actual prices",
  "I: 12 CP = 10 SP ⇒ SP/CP = 6/5 ⇒ profit = 20% — sufficient on its own. II gives the selling price but nothing "
  "about the cost, so it is not sufficient.",
  ["I: SP : CP = 12 : 10 ⇒ 20% profit", "II: SP = 600, CP unknown"],
  why="'Both together' assumes rupee values are needed, but a percentage needs only the ratio; 'II alone' and "
      "'either' forget that II says nothing about the cost.", secs=50, by=BRUTE)

cands = [(F(l, 2), F(b, 2)) for l in range(1, 81) for b in range(1, 81) if l > b]
conds = [lambda c: c[0] * c[1] == 180, lambda c: c[0] - c[1] == 8, lambda c: 2 * (c[0] + c[1]) == 56]
mp_ = suff_map(cands, conds, lambda c: c[0])
assert mp_ == {(0,): False, (1,): False, (2,): False, (0, 1): True, (0, 2): True, (1, 2): True, (0, 1, 2): True}
Q(T, "Three-statement", I,
  f"{DS3_PRE}\nQuestion: What is the length of the rectangle? (Its length is greater than its breadth.)\n"
  "I. The area of the rectangle is 180 m².\n"
  "II. The length exceeds the breadth by 8 m.\n"
  "III. The perimeter of the rectangle is 56 m.",
  "Any two of the three statements together are sufficient",
  ["Only I and II together are sufficient", "Only II and III together are sufficient",
   "All three statements together are necessary"],
  "Check every pair: each gives two independent equations in length and breadth",
  "I + II: l(l − 8) = 180 ⇒ l = 18. I + III: l + b = 28 and lb = 180 ⇒ l, b = 18, 10, and since the length is the "
  "longer side, l = 18. II + III: l − b = 8, l + b = 28 ⇒ l = 18. No single statement is enough.",
  ["I + II: l² − 8l − 180 = 0 ⇒ l = 18", "I + III: t² − 28t + 180 = 0 ⇒ 18, 10 ⇒ l = 18", "II + III: l = 18",
   "Singles: one equation, two unknowns"],
  why="'Only I and II' and 'only II and III' each miss that the other pairs also work; 'all three' is more than "
      "needed.", secs=85, by=BRUTE)

cands = list(range(10, 100))
verdict = ds2_verdict(cands, lambda n: abs(n // 10 - n % 10) == 3, lambda n: n == 4 * (n // 10 + n % 10), lambda n: n)
assert verdict == "both" and [n for n in cands if n == 4 * (n // 10 + n % 10)] == [12, 24, 36, 48]
Q(T, "Two-statement", I,
  f"{DS_PRE}\nQuestion: What is the two-digit number?\n"
  "I. Its two digits differ by 3.\n"
  "II. The number is 4 times the sum of its digits.",
  DS2["both"], [DS2["II"], DS2["I"], DS2["neither"]],
  "List the numbers each statement allows and look for a single common value",
  "I allows many numbers (14, 41, 25, 52, 36, 63, …). II: 10a + b = 4(a + b) ⇒ b = 2a, giving 12, 24, 36, 48. "
  "Together only 36 (digits 3 and 6 differ by 3) remains.",
  ["I: many numbers", "II: b = 2a ⇒ 12, 24, 36, 48", "Common: 36"],
  why="'II alone' leaves four numbers; 'I alone' leaves many; 'not sufficient together' misses that only 36 satisfies "
      "both.", secs=60, by=BRUTE)

cands = [(x, y) for x in range(-10, 11) for y in range(-10, 11)]
verdict = ds2_verdict(cands, lambda c: c[0] ** 2 + c[1] ** 2 == 25, lambda c: c[0] * c[1] == 12,
                      lambda c: c[0] + c[1])
assert verdict == "neither" and {c[0] + c[1] for c in cands if c[0] ** 2 + c[1] ** 2 == 25 and c[0] * c[1] == 12} == {7, -7}
Q(T, "Two-statement", A,
  f"{DS_PRE}\nQuestion: What is the value of x + y, where x and y are real numbers?\n"
  "I. x² + y² = 25\n"
  "II. xy = 12",
  DS2["neither"], [DS2["both"], DS2["I"], DS2["either"]],
  "(x + y)² = x² + y² + 2xy, but a square root has two signs",
  "Together: (x + y)² = 25 + 24 = 49, so x + y = 7 or −7 (for example x = 3, y = 4 or x = −3, y = −4). Two values "
  "remain, so even both statements together are not sufficient.",
  ["(x + y)² = 25 + 2 × 12 = 49", "x + y = ±7", "(3, 4) and (−3, −4) both fit", "Not sufficient"],
  why="'Both together' takes only the positive root, 7; 'I alone' and 'either' ignore that I alone allows many pairs "
      "(e.g. 0 and 5, 3 and 4).", secs=80, by=BRUTE)

cands = []
for m in range(0, 101):
    for d in range(0, 51):
        g = (100 + m) * (100 - d) - 10000  # profit = cp × g / 10000
        extra = [F(338 * 10000, g)] if g > 0 else []
        cands += [(F(cp), m, d) for cp in [F(500), F(1000), F(1300), F(2000), *extra]]
conds = [lambda c: c[1] == 40, lambda c: c[2] == 10,
         lambda c: c[0] * ((100 + c[1]) * (100 - c[2]) - 10000) == 338 * 10000]
mp_ = suff_map(cands, conds, lambda c: c[0])
assert mp_ == {(0,): False, (1,): False, (2,): False, (0, 1): False, (0, 2): False, (1, 2): False, (0, 1, 2): True}
Q(T, "Three-statement", A,
  f"{DS3_PRE}\nQuestion: What is the cost price of the article?\n"
  "I. The article is marked 40% above its cost price.\n"
  "II. It is sold at a discount of 10% on the marked price.\n"
  "III. The profit on the sale is ₹338.",
  "All three statements together are necessary",
  ["Only I and III together are sufficient", "Only II and III together are sufficient",
   "Any two of the three statements together are sufficient"],
  "The profit in rupees fixes the cost only when the profit percentage is known, which needs both I and II",
  "I + II: SP = 1.4 × 0.9 × CP = 1.26 CP, a 26% profit, but no rupee value. I + III or II + III: the profit "
  "percentage is unknown. All three: 0.26 CP = 338 ⇒ CP = ₹1,300.",
  ["I + II: profit = 26% of CP", "I + III: discount unknown", "II + III: mark-up unknown",
   "All three: 0.26 CP = 338 ⇒ CP = 1,300"],
  why="'Only I and III' forgets the discount; 'only II and III' forgets the mark-up; 'any two' assumes the pair I + II "
      "is enough, but it gives a percentage, not a rupee value.", secs=95, by=BRUTE)

# ================================================================ checks and output
assert len(QUESTIONS) == TOTAL, len(QUESTIONS)
assert len(STIMULI) == 10

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_006_plan.json").read_text(encoding="utf-8"))
qa = next(s for s in plan["subjects"] if s["subject"] == SUBJECT)
have = Counter((q["topic"], q["difficulty"]) for q in QUESTIONS)
want = Counter({(t["topic"], d): n for t in qa["topics"] for d, n in t["quota"].items() if n})
assert have == want, set(have.items()) ^ set(want.items())
subs = {t["topic"]: set(t["subtopics"]) for t in qa["topics"]}
assert all(q["subtopic"] in subs[q["topic"]] for q in QUESTIONS), [
    (q["topic"], q["subtopic"]) for q in QUESTIONS if q["subtopic"] not in subs[q["topic"]]]
assert QUESTIONS[0]["question_id"] == qa["question_ids"][0] and QUESTIONS[-1]["question_id"] == qa["question_ids"][1]
assert STIMULI[0]["stimulus_id"] == qa["stimulus_id_start"]
for s in STIMULI:  # every DI set has 3 to 6 questions
    assert 3 <= _set_pos[s["stimulus_id"]] <= 6, s["stimulus_id"]
keys = Counter(q["correct_answer"] for q in QUESTIONS)
assert keys == Counter({"A": 50, "B": 50, "C": 50, "D": 49}), keys
assert INDEPENDENT <= {q["question_id"] for q in QUESTIONS}

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_006",
    "created_at": TODAY,
    "notes": "BATCH_006, Quantitative Aptitude part: 199 original questions (60 Basic, 80 Intermediate, 59 Advanced) "
             "with 10 shared DI stimuli on new data sets. Every answer was recomputed by tools/batch_006/quant.py "
             "before writing; quantity-comparison values are at least 2% apart. Questions tagged "
             "ai:independent-check were also re-solved from the stem, options and data set alone by a separate "
             "solver. Pending human review.",
    "stimuli": STIMULI,
    "questions": QUESTIONS,
}
out = ROOT / "batches" / "parts" / "BATCH_006_QUANT.json"
if "--dump" in sys.argv:  # blind copies for solvers: no key, no solution
    ids = None
    if "--ids" in sys.argv:
        ids = set(sys.argv[sys.argv.index("--ids") + 1].split(","))
    blind = [{"question_id": q["question_id"], "stimulus_id": q.get("stimulus_id"), "question_text": q["question_text"],
              "options": q["options"]} for q in QUESTIONS if ids is None or q["question_id"] in ids]
    used = {q["stimulus_id"] for q in blind if q["stimulus_id"]}
    Path(sys.argv[sys.argv.index("--dump") + 1]).write_text(
        json.dumps({"stimuli": [s for s in STIMULI if s["stimulus_id"] in used], "questions": blind}, indent=1,
                   ensure_ascii=False), encoding="utf-8")
    print(f"blind dump written ({len(blind)} questions)")
    sys.exit(0)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(QUESTIONS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(keys.items()))}, "
      f"independent-check {len(INDEPENDENT)})")
