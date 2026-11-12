"""Writes batches/parts/BATCH_002_QUANT.json: the 200 Quantitative Aptitude questions of BATCH_002.

Every answer is recomputed here before the file is written: arithmetic with exact fractions, series regenerated
from their rule, quadratic roots substituted back into the equations, probabilities and arrangements counted by
brute force, data-sufficiency statements checked by enumerating candidate values, approximation answers checked to
be the option nearest the exact value. If any assertion fails, nothing is written.

The structure and helpers follow tools/batch_001/quant.py. Contexts, data sets and number templates are new: none
of batch 1's DI tables, charts or caselet themes is reused.

    python tools/batch_002/quant.py          (run from docs/question-bank)
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
TOTAL = 200

# Balanced answer keys: exactly 50 of each letter, order fixed by the seed.
_rng = random.Random(20261105 + 2)
KEYS = list("ABCD" * (TOTAL // 4))
_rng.shuffle(KEYS)

QUESTIONS, STIMULI = [], []
_set_pos = {}
_FIRST_ID = 206
_FIRST_STIM = 2001
RECOMPUTE = ["script:recompute", "ai:author-solve"]
BRUTE = ["script:recompute", "script:brute-force-unique", "ai:author-solve"]

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
    """Exact number text: integers grouped, terminating decimals in full, thirds/sixths etc. as mixed fractions."""
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


def P(x, dp=2) -> str:
    return N(x, dp) + "%"


def ratio(*vals) -> str:
    vals = [F(v) for v in vals]
    den = math.lcm(*[v.denominator for v in vals])
    ints = [int(v * den) for v in vals]
    g = math.gcd(*ints)
    return " : ".join(str(i // g) for i in ints)


def near(a, b, tol=1e-9):
    return abs(float(a) - float(b)) < tol


# ---------------------------------------------------------------- record builder
def Q(topic, sub, diff, text, ans, wrong, concept, expl, steps, short=None, why=None, secs=None, stim=None,
      by=None):
    """Places the correct option at the next balanced key, checks the options and appends the record."""
    assert len(wrong) == 3, wrong
    assert diff in (B, I, A)
    n = len(QUESTIONS)
    key = KEYS[n]
    opts = list(wrong)
    opts.insert(LETTERS.index(key), ans)
    assert len({normalize(o) for o in opts}) == 4, f"options not distinct: {opts}"
    rec = {
        "question_id": f"BANK_QUANT_{_FIRST_ID + n:06d}",
        "exam_mappings": default_mappings(SUBJECT, diff),
        "subject": SUBJECT, "topic": topic, "subtopic": sub, "difficulty": diff,
        "question_type": "MCQ", "language": "en",
    }
    if stim:
        _set_pos[stim] = _set_pos.get(stim, 0) + 1
        rec |= {"stimulus_id": stim, "set_position": _set_pos[stim]}
    if secs is None:
        secs = {B: 40, I: 60, A: 100}[diff]
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
                         "verified_by": list(by or RECOMPUTE), "verified_at": TODAY},
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


def pct_text(x):
    return P(x)


# ================================================================ Simplification (B2 I5 A6)
T = "Simplification"
v = F(156) / 12 + 7 * 8 - F(45) / 9
assert v == 64
assert 13 + 56 + 5 == 74 and (13 + 7) * 8 - 5 == 155 and 13 + 56 == 69
Q(T, "BODMAS", B, "Simplify: 156 ÷ 12 + 7 × 8 − 45 ÷ 9 = ?",
  "64", ["74", "155", "69"],
  "BODMAS: both divisions and the multiplication come before the addition and subtraction",
  "Do the divisions and the multiplication first: 156 ÷ 12 = 13, 7 × 8 = 56 and 45 ÷ 9 = 5. "
  "Then 13 + 56 − 5 = 64.",
  ["156 ÷ 12 = 13", "7 × 8 = 56", "45 ÷ 9 = 5", "13 + 56 − 5 = 64"],
  why="74 adds the 5 instead of subtracting it; 155 adds 13 + 7 before multiplying by 8; 69 drops the last term.",
  secs=30)

v = F(25, 100) * F(48, 10) + F(21, 8) / F(75, 100) - F(16, 10)
assert v == F(31, 10)
alt1 = F(25, 100) * F(48, 10) + F(21, 8) * F(75, 100) - F(16, 10)
assert alt1 == F(251, 160) and F(12, 10) + F(35, 10) + F(16, 10) == F(63, 10) and F(35, 10) - F(12, 10) == F(23, 10)
Q(T, "Fractions and decimals", B, "What is the value of 0.25 × 4.8 + 2⅝ ÷ 0.75 − 1.6?",
  "3.1", ["1.57", "6.3", "2.3"],
  "Convert mixed numbers and decimals to fractions; divide and multiply before adding and subtracting",
  "0.25 × 4.8 = 1.2. 2⅝ = 21/8 and 0.75 = 3/4, so 2⅝ ÷ 0.75 = 21/8 × 4/3 = 3.5. "
  "Then 1.2 + 3.5 − 1.6 = 3.1.",
  ["0.25 × 4.8 = 1.2 (a quarter of 4.8)", "2⅝ ÷ 0.75 = 21/8 × 4/3 = 84/24 = 3.5", "1.2 + 3.5 − 1.6 = 3.1"],
  short="Dividing by 0.75 is multiplying by 4/3: 2.625 × 4/3 = 3.5.",
  why="1.57 multiplies 2⅝ by 0.75 instead of dividing (1.2 + 1.97 − 1.6 ≈ 1.57); 6.3 adds the 1.6; "
      "2.3 is 3.5 − 1.2, which drops the last term and subtracts the first.", secs=40)

v = F(72, 12) * F(3, 2) + 3 ** 2
assert 72 ** 2 == 5184 and 12 ** 3 == 1728 and F(15, 10) ** 2 == F(225, 100) and v == 18
assert F(6) / F(3, 2) + 9 == 13 and 6 * 15 + 9 == 99 and 6 + 9 == 15
Q(T, "Square and cube roots", I, "Find the value of √5184 ÷ ∛1728 × √2.25 + 3².",
  "18", ["13", "99", "15"],
  "Square roots and cube roots of perfect powers, then left-to-right ÷ and ×",
  "√5184 = 72, ∛1728 = 12 and √2.25 = 1.5. So 72 ÷ 12 × 1.5 = 6 × 1.5 = 9, and 9 + 9 = 18.",
  ["√5184 = 72 (72² = 5184)", "∛1728 = 12 (12³ = 1728)", "√2.25 = 1.5 (1.5² = 2.25)",
   "72 ÷ 12 = 6; 6 × 1.5 = 9", "9 + 3² = 9 + 9 = 18"],
  short="5184 ends in 4 and lies between 70² = 4900 and 75² = 5625, so its root is 72.",
  why="13 divides 6 by 1.5 instead of multiplying; 99 takes √2.25 as 15; 15 leaves out the × 1.5.", secs=50)

v = F(5) ** 2 * F(2) ** 3 / F(2)
assert near(0.008 ** (-2 / 3), 25) and near(0.25 ** (-1.5), 8) and near(0.0625 ** (-0.25), 2) and v == 100
Q(T, "Surds and indices", I, "Simplify: (0.008)^(−2/3) × (0.25)^(−3/2) ÷ (0.0625)^(−1/4)",
  "100", ["50", "200", "400"],
  "Negative fractional exponents: a^(−m/n) = 1 ÷ (n-th root of a)^m; write each decimal as a power of a simple "
  "fraction",
  "0.008 = (1/5)³, so 0.008^(−2/3) = 5² = 25. 0.25 = (1/2)², so 0.25^(−3/2) = 2³ = 8. 0.0625 = (1/2)⁴, so "
  "0.0625^(−1/4) = 2. The value is 25 × 8 ÷ 2 = 100.",
  ["0.008 = (0.2)³ ⇒ (0.008)^(−2/3) = (0.2)^(−2) = 1/0.04 = 25", "0.25 = (0.5)² ⇒ (0.25)^(−3/2) = (0.5)^(−3) = 8",
   "0.0625 = (0.5)⁴ ⇒ (0.0625)^(−1/4) = (0.5)^(−1) = 2", "25 × 8 ÷ 2 = 100"],
  short="A negative exponent flips the base: 0.2 → 5 and 0.5 → 2, then take the powers 5², 2³ and 2¹.",
  why="50 divides by 4 instead of 2; 200 multiplies by 2 instead of dividing; 400 multiplies 25 × 8 × 2.", secs=60)

inner = 15 - 8 + 3 * 2
v = 45 - F(28 - (37 - inner), 4)
assert inner == 13 and v == 44
assert F(45 - 4, 4) == F(41, 4) and 45 - F(28 - (37 - (15 - 8 + 3) * 2), 4) == F(169, 4) and 45 - 4 == 41
Q(T, "BODMAS", I, "Simplify: 45 − [28 − {37 − (15 − 8 + 3 × 2)}] ÷ 4",
  "44", ["10.25", "42.25", "41"],
  "Open brackets from the innermost: ( ), then { }, then [ ]; division comes before subtraction",
  "Inside ( ): 15 − 8 + 6 = 13. Inside { }: 37 − 13 = 24. Inside [ ]: 28 − 24 = 4. Then 4 ÷ 4 = 1, and "
  "45 − 1 = 44.",
  ["( ): 15 − 8 + 3 × 2 = 15 − 8 + 6 = 13", "{ }: 37 − 13 = 24", "[ ]: 28 − 24 = 4", "4 ÷ 4 = 1",
   "45 − 1 = 44"],
  why="10.25 divides (45 − 4) by 4; 42.25 works out (15 − 8 + 3) × 2 = 20 inside the round bracket; 41 forgets the "
      "÷ 4.", secs=50)

v = (F(12, 5) + F(18, 5)) / (F(3, 5) * 15) + F(4, 3)
assert v == 2
left_to_right = (F(12, 5) + F(18, 5)) / F(3, 5) * 15 + F(4, 3)
assert left_to_right == F(454, 3) and (F(12, 5) + F(18, 5)) / F(3, 5) + F(4, 3) == F(34, 3)
Q(T, "Fractions and decimals", I, "(2⅖ + 3⅗) ÷ ⅗ of 15 + 1⅓ = ?",
  "2", ["151⅓", "11⅓", "⅔"],
  "'of' is worked out before division (the O in BODMAS)",
  "The bracket is 2⅖ + 3⅗ = 6. '⅗ of 15' = 9 is evaluated before the division, so 6 ÷ 9 = ⅔. "
  "Then ⅔ + 1⅓ = 2.",
  ["2⅖ + 3⅗ = 6", "⅗ of 15 = 9", "6 ÷ 9 = ⅔", "⅔ + 1⅓ = 2"],
  why="151⅓ divides by ⅗ first and then multiplies by 15, ignoring that 'of' comes first; 11⅓ drops the 'of 15'; "
      "⅔ forgets to add 1⅓.", secs=55)

v = F(21, 1000) + F(14, 100) * F(12, 10)
assert v == F(189, 1000)
assert F(21, 1000) ** 2 == F(441, 1000000) and F(14, 100) ** 2 == F(196, 10000) and F(12, 10) ** 2 == F(144, 100)
assert F(21, 100) + F(168, 1000) == F(378, 1000) and F(21, 1000) + F(168, 100) == F(1701, 1000)
assert (F(21, 1000) + F(14, 100)) * F(12, 10) == F(1932, 10000)
Q(T, "Square and cube roots", I, "√0.000441 + √0.0196 × √1.44 = ?",
  "0.189", ["0.378", "1.701", "0.1932"],
  "Square root of a decimal: the root has half as many decimal places",
  "√0.000441 = 0.021 (six decimal places become three), √0.0196 = 0.14 and √1.44 = 1.2. "
  "Multiplication first: 0.14 × 1.2 = 0.168. Then 0.021 + 0.168 = 0.189.",
  ["√0.000441 = √441 ÷ √1000000 = 21 ÷ 1000 = 0.021", "√0.0196 = 14 ÷ 100 = 0.14", "√1.44 = 1.2",
   "0.14 × 1.2 = 0.168", "0.021 + 0.168 = 0.189"],
  why="0.378 takes √0.000441 as 0.21; 1.701 takes √0.0196 as 1.4; 0.1932 adds before multiplying.", secs=50)

# Advanced simplification
x_ = 3 + 2 * math.sqrt(2)
assert near(x_ + 1 / x_, 6) and near(x_ ** 3 + 1 / x_ ** 3, 198, 1e-7)
assert 6 ** 3 - 3 * 6 == 198 and 6 ** 3 == 216 and 6 ** 3 + 3 * 6 == 234 and 6 ** 2 - 2 == 34
Q(T, "Surds and indices", A, "If x = 3 + 2√2, what is the value of x³ + 1/x³?",
  "198", ["216", "234", "34"],
  "Rationalising 1/x, then the identity a³ + b³ = (a + b)³ − 3ab(a + b) with ab = 1",
  "1/x = 1/(3 + 2√2) = (3 − 2√2)/(9 − 8) = 3 − 2√2, so x + 1/x = 6 and x × 1/x = 1. Then "
  "x³ + 1/x³ = (x + 1/x)³ − 3(x + 1/x) = 216 − 18 = 198.",
  ["1/x = (3 − 2√2)/((3 + 2√2)(3 − 2√2)) = 3 − 2√2", "x + 1/x = 6",
   "x³ + 1/x³ = (x + 1/x)³ − 3 · x · (1/x) · (x + 1/x)", "= 6³ − 3 × 6 = 216 − 18 = 198"],
  short="Whenever x × (1/x) = 1, x³ + 1/x³ = k³ − 3k with k = x + 1/x.",
  why="216 is (x + 1/x)³ without the correction term; 234 adds 3(x + 1/x) instead of subtracting it; 34 is "
      "x² + 1/x² = 6² − 2, not the cube expression.", secs=80)

sols = [x for x in range(-10, 21) if 2 ** (x + 3) + 2 ** (x + 1) == 320]
assert sols == [5]
assert 2 ** 4 * 10 != 320 and 2 ** 6 * 10 != 320 and 2 ** 5 * 10 == 320
Q(T, "Surds and indices", A, "If 2^(x + 3) + 2^(x + 1) = 320, what is the value of x?",
  "5", ["4", "6", "3"],
  "Take the lowest power out as a common factor",
  "2^(x + 3) = 8 × 2^x and 2^(x + 1) = 2 × 2^x, so the left side is 10 × 2^x. Then 10 × 2^x = 320 gives "
  "2^x = 32 = 2⁵, so x = 5.",
  ["2^(x + 3) + 2^(x + 1) = 2^x(2³ + 2¹) = 10 × 2^x", "10 × 2^x = 320 ⇒ 2^x = 32", "32 = 2⁵ ⇒ x = 5",
   "Check: 2⁸ + 2⁶ = 256 + 64 = 320"],
  why="6 is the value of x + 1 (factorising as 2^(x + 1)(2² + 1) = 320 gives 2^(x + 1) = 64), not of x; 4 and 3 "
      "fail the check: 2⁷ + 2⁵ = 160 and 2⁶ + 2⁴ = 80.", secs=70)

a_ = F(7, 30)
b_ = F(36, 99)
v = a_ + b_
assert v == F(197, 330)
assert F(23, 99) + F(36, 99) == F(59, 99) and F(23, 90) + F(36, 90) == F(59, 90) and a_ + F(36, 90) == F(19, 30)
assert near(float(v), 0.23333333 + 0.36363636, 1e-6)
Q(T, "Fractions and decimals", A,
  "Express 0.2333… (3 recurring) + 0.363636… (36 recurring) as a fraction in its lowest terms.",
  "197/330", ["59/99", "59/90", "19/30"],
  "Converting recurring decimals: pure recurring 0.abab… = ab/99; mixed recurring 0.abbb… = (ab − a)/90",
  "0.2333… is mixed recurring: (23 − 2)/90 = 21/90 = 7/30. 0.3636… is pure recurring: 36/99 = 4/11. "
  "7/30 + 4/11 = (77 + 120)/330 = 197/330.",
  ["0.2333… = (23 − 2)/90 = 21/90 = 7/30", "0.3636… = 36/99 = 4/11", "LCM of 30 and 11 = 330",
   "7/30 = 77/330 and 4/11 = 120/330", "Sum = 197/330"],
  why="59/99 treats both as pure recurring (23/99 + 36/99); 59/90 treats both as mixed with denominator 90; 19/30 "
      "writes 0.3636… as 36/90.", secs=90)

v_sq = 1030 - (F(15, 100) * 640 - 36 * F(5, 2))
assert v_sq == 1024 and math.isqrt(1024) == 32
assert [q for q in range(1, 100) if q * q + F(15, 100) * 640 - 36 * F(5, 2) == 1030] == [32]
Q(T, "BODMAS", A, "What will come in place of the question mark (?)?\n?² + 15% of 640 − √1296 × 2.5 = 1030 "
  "(? is a positive number)",
  "32", ["30", "34", "36"],
  "Evaluate every known term, then isolate ?²",
  "15% of 640 = 96 and √1296 × 2.5 = 36 × 2.5 = 90. So ?² + 96 − 90 = 1030, i.e. ?² + 6 = 1030 and ?² = 1024. "
  "Hence ? = 32.",
  ["15% of 640 = 96", "√1296 = 36; 36 × 2.5 = 90", "?² + 96 − 90 = 1030 ⇒ ?² = 1024", "? = 32"],
  why="30, 34 and 36 give ?² = 900, 1,156 and 1,296, none of which satisfies ?² + 6 = 1030.", secs=75)

v = math.sqrt(41 - math.sqrt(21 + math.sqrt(19 - math.sqrt(9))))
assert near(v, 6)
assert math.isqrt(9) == 3 and math.isqrt(16) == 4 and math.isqrt(25) == 5 and math.isqrt(36) == 6
assert near(math.sqrt(41 - math.sqrt(21 + math.sqrt(19 + 3))), math.sqrt(41 - math.sqrt(21 + math.sqrt(22))))
Q(T, "Square and cube roots", A, "Find the value of √(41 − √(21 + √(19 − √9))).",
  "6", ["5", "7", "4"],
  "Nested radicals are opened from the innermost root outwards",
  "√9 = 3, so 19 − 3 = 16 and √16 = 4. Then 21 + 4 = 25 and √25 = 5. Finally 41 − 5 = 36 and √36 = 6.",
  ["√9 = 3", "√(19 − 3) = √16 = 4", "√(21 + 4) = √25 = 5", "√(41 − 5) = √36 = 6"],
  why="5 is √25, the value one level inside, not the final root.", secs=60)

terms = [(9, 8), (8, 7), (7, 6), (6, 5), (5, 4)]
v = sum((1 if k % 2 == 0 else -1) / (math.sqrt(a) - math.sqrt(b)) for k, (a, b) in enumerate(terms))
assert near(v, 5, 1e-9)
Q(T, "Surds and indices", A,
  "Simplify: 1/(√9 − √8) − 1/(√8 − √7) + 1/(√7 − √6) − 1/(√6 − √5) + 1/(√5 − √4)",
  "5", ["0", "1", "3 + 2√2"],
  "Rationalising: 1/(√a − √b) = (√a + √b)/(a − b), and here every a − b = 1",
  "Each term rationalises to a sum: 1/(√9 − √8) = 3 + √8, 1/(√8 − √7) = √8 + √7, and so on. With the alternating "
  "signs, (3 + √8) − (√8 + √7) + (√7 + √6) − (√6 + √5) + (√5 + 2) = 3 + 2 = 5, since all the surds cancel.",
  ["1/(√9 − √8) = (√9 + √8)/(9 − 8) = 3 + √8", "1/(√8 − √7) = √8 + √7; 1/(√7 − √6) = √7 + √6",
   "1/(√6 − √5) = √6 + √5; 1/(√5 − √4) = √5 + 2",
   "Sum = 3 + √8 − √8 − √7 + √7 + √6 − √6 − √5 + √5 + 2 = 5"],
  why="0 assumes everything cancels, including 3 and 2; 1 subtracts 2 from 3; 3 + 2√2 keeps only the first term.",
  secs=90)

# ================================================================ Approximation (B3 I6 A3)
T = "Approximation"
exact = 0.3504 * 799.7 - 0.1202 * 249.9
nearest(exact, [250, 230, 270, 290], 250)
Q(T, "Percentage approximation", B,
  "What approximate value should come in place of the question mark (?)?\n35.04% of 799.7 − 12.02% of 249.9 ≈ ?",
  "250", ["230", "270", "290"],
  "Round each percentage and number to the nearest convenient value",
  f"35.04% of 799.7 ≈ 35% of 800 = 280 and 12.02% of 249.9 ≈ 12% of 250 = 30. So the value is about "
  f"280 − 30 = 250 (exact {exact:.2f}).",
  ["35% of 800 = 8 × 35 = 280", "12% of 250 = 30", "280 − 30 = 250"],
  short="1% of 800 is 8, so 35% is 8 × 35; 12% of 250 is a quarter of 120.", secs=35)

exact = math.sqrt(2499.6) * 3.98 + 1330.9 ** (1 / 3)
nearest(exact, [210, 190, 230, 250], 210)
Q(T, "Root approximation", B,
  "Find the approximate value of ?:\n√2499.6 × 3.98 + ∛1330.9 ≈ ?",
  "210", ["190", "230", "250"],
  "Nearest perfect square and perfect cube",
  f"√2499.6 ≈ √2500 = 50 and 3.98 ≈ 4, so the product is about 200. ∛1330.9 ≈ ∛1331 = 11. "
  f"200 + 11 ≈ 211, and the nearest option is 210 (exact {exact:.2f}).",
  ["√2499.6 ≈ 50", "50 × 4 = 200", "∛1330.9 ≈ 11 (11³ = 1331)", "200 + 11 = 211 ≈ 210"], secs=35)

exact = 1439.8 / 24.03 + 18.97 * 7.02
nearest(exact, [193, 173, 213, 233], 193)
Q(T, "Mixed approximation", B,
  "What approximate value will replace the question mark?\n1439.8 ÷ 24.03 + 18.97 × 7.02 ≈ ?",
  "193", ["173", "213", "233"],
  "Round each number to a value that divides or multiplies cleanly",
  f"1439.8 ÷ 24.03 ≈ 1440 ÷ 24 = 60 and 18.97 × 7.02 ≈ 19 × 7 = 133. The sum is about 193 (exact {exact:.2f}).",
  ["1440 ÷ 24 = 60", "19 × 7 = 133", "60 + 133 = 193"], secs=35)

exact = (432.1 - 0.2798 * 650.2) / 1249.7 * 100
nearest(exact, [20, 16, 24, 28], 20)
Q(T, "Percentage approximation", I,
  "What approximate value should come in place of the question mark (?)?\n?% of 1249.7 + 27.98% of 650.2 ≈ 432.1",
  "20", ["16", "24", "28"],
  "Rounding, then solving for the unknown percentage",
  f"27.98% of 650.2 ≈ 28% of 650 = 182. So ?% of 1250 ≈ 432 − 182 = 250, and ? ≈ 250 ÷ 12.5 = 20 "
  f"(exact {exact:.2f}).",
  ["28% of 650 = 182", "?% of 1250 = 432 − 182 = 250", "1% of 1250 = 12.5, so ? = 250 ÷ 12.5 = 20"], secs=50)

exact = math.sqrt(1155.8 + math.sqrt(4223.9))
nearest(exact, [35, 33, 37, 39], 35)
Q(T, "Root approximation", I,
  "Find the approximate value of ?:\n√(1155.8 + √4223.9) ≈ ?",
  "35", ["33", "37", "39"],
  "Approximate the inner root first, then the outer one",
  f"√4223.9 ≈ √4225 = 65. Then 1155.8 + 65 ≈ 1221 and √1221 is just under √1225 = 35 (exact {exact:.2f}).",
  ["√4223.9 ≈ 65 (65² = 4225)", "1155.8 + 65 ≈ 1220.8", "√1220.8 ≈ 35 (35² = 1225)"], secs=50)

exact = 5 / 8 * 1279.6 + 3 / 7 * 841.2 - 19.98 ** 2
nearest(exact, [760, 740, 780, 720], 760)
Q(T, "Mixed approximation", I,
  "What approximate value should replace ? in the expression\n5/8 of 1279.6 + 3/7 of 841.2 − 19.98² ≈ ?",
  "760", ["740", "780", "720"],
  "Round to multiples of the fraction's denominator",
  f"1279.6 ≈ 1280 (a multiple of 8) and 841.2 ≈ 840 (a multiple of 7). 5/8 of 1280 = 800, 3/7 of 840 = 360 and "
  f"19.98² ≈ 400. So 800 + 360 − 400 = 760 (exact {exact:.2f}).",
  ["5/8 of 1280 = 160 × 5 = 800", "3/7 of 840 = 120 × 3 = 360", "19.98² ≈ 400", "800 + 360 − 400 = 760"], secs=55)

exact = (12.98 * 15.03 - 44.99) / 6.02
nearest(exact, [25, 20, 30, 35], 25)
Q(T, "Mixed approximation", I,
  "What approximate value should come in place of the question mark (?)?\n(12.98 × 15.03 − 44.99) ÷ 6.02 ≈ ?",
  "25", ["20", "30", "35"],
  "Round to whole numbers and keep the bracket together",
  f"12.98 × 15.03 ≈ 13 × 15 = 195. 195 − 45 = 150 and 150 ÷ 6 = 25 (exact {exact:.2f}).",
  ["13 × 15 = 195", "195 − 45 = 150", "150 ÷ 6 = 25"],
  secs=45)

exact = 2196.8 ** (1 / 3) * 6.98 + 0.3996 * 1149.8
nearest(exact, [551, 531, 571, 591], 551)
Q(T, "Root approximation", I,
  "Find the approximate value of ?:\n∛2196.8 × 6.98 + 39.96% of 1149.8 ≈ ?",
  "551", ["531", "571", "591"],
  "Nearest perfect cube; 40% is two-fifths",
  f"∛2196.8 ≈ ∛2197 = 13 and 13 × 7 = 91. 39.96% of 1149.8 ≈ 40% of 1150 = 460. So ? ≈ 91 + 460 = 551 "
  f"(exact {exact:.2f}).",
  ["∛2196.8 ≈ 13 (13³ = 2197)", "13 × 7 = 91", "40% of 1150 = 460", "91 + 460 = 551"], secs=50)

exact = 2047.9 / (247.1 - 24.02 * 4.98)
nearest(exact, [16, 12, 20, 24], 16)
Q(T, "Mixed approximation", I,
  "What approximate value should come in place of the question mark (?)?\n2047.9 ÷ ? + 24.02 × 4.98 ≈ 247.1",
  "16", ["12", "20", "24"],
  "Unknown in the denominator: isolate the quotient first",
  f"24.02 × 4.98 ≈ 24 × 5 = 120. So 2048 ÷ ? ≈ 247 − 120 = 127 ≈ 128, and ? ≈ 2048 ÷ 128 = 16 "
  f"(exact {exact:.2f}).",
  ["24 × 5 = 120", "2048 ÷ ? ≈ 247 − 120 = 127", "2048 ÷ 128 = 16, so ? ≈ 16"], secs=55)

exact = (0.4498 * 1599.7 + math.sqrt(3135.9)) / 7.98 + 13.97 ** 2
nearest(exact, [293, 286, 313, 273], 293)
Q(T, "Mixed approximation", A,
  "What approximate value should come in place of the question mark (?)?\n"
  "(44.98% of 1599.7 + √3135.9) ÷ 7.98 ≈ ? − 13.97²",
  "293", ["286", "313", "273"],
  "Multi-term approximation with the unknown on the right side",
  f"44.98% of 1599.7 ≈ 45% of 1600 = 720 and √3135.9 ≈ √3136 = 56. (720 + 56) ÷ 8 = 97. 13.97² ≈ 14² = 196, "
  f"so ? ≈ 97 + 196 = 293 (exact {exact:.2f}).",
  ["45% of 1600 = 720", "√3136 = 56", "(720 + 56) ÷ 8 = 776 ÷ 8 = 97", "14² = 196", "? = 97 + 196 = 293"],
  why="286 leaves out √3135.9 (720 ÷ 8 + 196); 313 and 273 are 20 away from the computed value.", secs=85)

exact = math.sqrt(1285.2 + 0.3602 * 1249.8 - 3374.7 ** (1 / 3) * 8.97)
nearest(exact, [40, 35, 45, 50], 40)
Q(T, "Root approximation", A,
  "Find the approximate value of ?:\n?² − 36.02% of 1249.8 + ∛3374.7 × 8.97 ≈ 1285.2",
  "40", ["35", "45", "50"],
  "Cube root and percentage approximation, then solving for ?²",
  f"36.02% of 1249.8 ≈ 36% of 1250 = 450. ∛3374.7 ≈ 15 and 15 × 9 = 135. So ?² ≈ 1285 + 450 − 135 = 1600 and "
  f"? ≈ 40 (exact {exact:.2f}).",
  ["36% of 1250 = 450", "∛3375 = 15; 15 × 9 = 135", "?² = 1285 + 450 − 135 = 1600", "? = 40"],
  why="35, 45 and 50 square to 1,225, 2,025 and 2,500, far from 1,600.", secs=85)

exact = (17.02 ** 2 - 12.98 ** 2) * 4.99 / 9.97 + 0.6301 * 499.8
nearest(exact, [375, 355, 395, 415], 375)
Q(T, "Percentage approximation", A,
  "What approximate value should replace ? in\n(17.02² − 12.98²) × 4.99 ÷ 9.97 + 63.01% of 499.8 ≈ ?",
  "375", ["355", "395", "415"],
  "Difference of squares a² − b² = (a + b)(a − b) after rounding",
  f"17² − 13² = (17 + 13)(17 − 13) = 30 × 4 = 120. 120 × 5 ÷ 10 = 60. 63% of 500 = 315. So ? ≈ 60 + 315 = 375 "
  f"(exact {exact:.2f}).",
  ["17² − 13² = 30 × 4 = 120", "120 × 5 ÷ 10 = 60", "63% of 500 = 315", "60 + 315 = 375"],
  short="(a + b)(a − b) avoids squaring 17 and 13 separately.", secs=80)

# ================================================================ Number Series (B4 I3 A4)
T = "Number Series"


def series_from(start, step, n):
    out = [start]
    for k in range(1, n):
        out.append(step(out[-1], k))
    return out


def diffs(seq):
    return [b - a for a, b in zip(seq, seq[1:])]


PRIMES = [2, 3, 5, 7, 11, 13, 17]
s = [11]
for p_ in PRIMES[:6]:
    s.append(s[-1] + p_)
assert s == [11, 13, 16, 21, 28, 39, 52]
Q(T, "Pattern: differences", B, "What will come in place of the question mark (?) in the series?\n"
  "11, 13, 16, 21, 28, 39, ?",
  "52", ["50", "54", "51"],
  "Differences are consecutive prime numbers",
  "The differences are 2, 3, 5, 7, 11, the prime numbers in order. The next prime is 13, so the next term is "
  "39 + 13 = 52.",
  ["13 − 11 = 2, 16 − 13 = 3, 21 − 16 = 5", "28 − 21 = 7, 39 − 28 = 11", "Next prime = 13", "39 + 13 = 52"],
  why="50 repeats the difference 11; 51 uses 12, which is not prime.", secs=30)

s = [n * n - 1 for n in range(11, 5, -1)]
assert s == [120, 99, 80, 63, 48, 35]
Q(T, "Pattern: squares and cubes", B, "Find the next term of the series: 120, 99, 80, 63, 48, ?",
  "35", ["33", "36", "37"],
  "One less than perfect squares, in descending order",
  "120 = 11² − 1, 99 = 10² − 1, 80 = 9² − 1, 63 = 8² − 1, 48 = 7² − 1. The next term is 6² − 1 = 35.",
  ["120 = 121 − 1, 99 = 100 − 1, 80 = 81 − 1", "63 = 64 − 1, 48 = 49 − 1", "Next = 36 − 1 = 35"],
  short="The differences 21, 19, 17, 15 fall by 2, so the next difference is 13: 48 − 13 = 35.",
  why="36 is 6² without the −1; 33 repeats the difference 15.", secs=30)

s = series_from(4, lambda t, k: 3 * t - 2, 6)
assert s == [4, 10, 28, 82, 244, 730]
Q(T, "Pattern: multiply-add", B, "Which number should replace the question mark?\n4, 10, 28, 82, 244, ?",
  "730", ["732", "728", "734"],
  "Multiply by 3 and subtract 2",
  "Each term is three times the previous term minus 2: 4 × 3 − 2 = 10, 10 × 3 − 2 = 28, and so on. "
  "The next term is 244 × 3 − 2 = 730.",
  ["4 × 3 − 2 = 10", "10 × 3 − 2 = 28", "28 × 3 − 2 = 82", "82 × 3 − 2 = 244", "244 × 3 − 2 = 730"],
  short="The differences 6, 18, 54, 162 triple, so the next difference is 486: 244 + 486 = 730.",
  why="732 multiplies by 3 without subtracting 2; 734 adds 2 instead.", secs=30)

s = series_from(F(64), lambda t, k: t * F(3, 2), 6)
assert s == [64, 96, 144, 216, 324, 486]
assert 144 + 48 == 192 and 144 + 96 == 240
Q(T, "Missing number series", B, "Find the missing number (?) in the series: 64, 96, 144, ?, 324, 486",
  "216", ["192", "240", "228"],
  "Each term is 1.5 times the previous term",
  "96 ÷ 64 = 1.5 and 144 ÷ 96 = 1.5, so the missing term is 144 × 1.5 = 216. Check: 216 × 1.5 = 324 and "
  "324 × 1.5 = 486.",
  ["64 × 1.5 = 96", "96 × 1.5 = 144", "144 × 1.5 = 216", "Check: 216 × 1.5 = 324; 324 × 1.5 = 486"],
  why="192 repeats the difference 48; 240 adds 96. Neither continues to 324.", secs=40)

s = series_from(7, lambda t, k: t + 2 ** (k - 1), 7)
assert s == [7, 8, 10, 14, 22, 38, 70]
Q(T, "Missing number series", I, "Find the missing term: 7, 8, 10, 14, 22, ?, 70",
  "38", ["36", "30", "46"],
  "Differences double: 1, 2, 4, 8, 16, 32",
  "The differences are 1, 2, 4, 8, so the next ones are 16 and 32. The missing term is 22 + 16 = 38, and "
  "38 + 32 = 70 confirms it.",
  ["8 − 7 = 1, 10 − 8 = 2, 14 − 10 = 4, 22 − 14 = 8", "Next difference = 16 ⇒ 22 + 16 = 38",
   "Check: 38 + 32 = 70"],
  why="30 repeats the difference 8; 46 doubles 22 and adds 2, but 46 → 70 is a difference of 24, not 32.", secs=45)

s = [n ** 3 - n for n in range(2, 8)]
assert s == [6, 24, 60, 120, 210, 336] and 210 + 120 == 330 and 7 ** 3 == 343
Q(T, "Pattern: squares and cubes", I, "What will come in place of ? in the series 6, 24, 60, 120, 210, ?",
  "336", ["330", "343", "324"],
  "n³ − n, i.e. the product of three consecutive numbers (n − 1) n (n + 1)",
  "6 = 2³ − 2, 24 = 3³ − 3, 60 = 4³ − 4, 120 = 5³ − 5, 210 = 6³ − 6. The next term is 7³ − 7 = 336.",
  ["6 = 1 × 2 × 3, 24 = 2 × 3 × 4, 60 = 3 × 4 × 5", "120 = 4 × 5 × 6, 210 = 5 × 6 × 7", "Next = 6 × 7 × 8 = 336"],
  why="343 is 7³ without subtracting 7; 330 adds 120 (repeating a second difference of 30 instead of 36).",
  secs=50)

s = series_from(11, lambda t, k: 2 * t + (3 if k % 2 == 1 else -3), 6)
assert s == [11, 25, 47, 97, 191, 385]
Q(T, "Pattern: multiply-add", I, "What should come in place of the question mark?\n11, 25, 47, 97, 191, ?",
  "385", ["379", "382", "389"],
  "Alternating operations: ×2 + 3, then ×2 − 3",
  "11 × 2 + 3 = 25, 25 × 2 − 3 = 47, 47 × 2 + 3 = 97, 97 × 2 − 3 = 191. The next step is ×2 + 3: "
  "191 × 2 + 3 = 385.",
  ["11 × 2 + 3 = 25", "25 × 2 − 3 = 47", "47 × 2 + 3 = 97", "97 × 2 − 3 = 191", "191 × 2 + 3 = 385"],
  why="379 applies −3 twice in a row; 382 doubles without the +3.", secs=50)

s = [3, 7, 13, 23, 41, 75]
d1 = diffs(s)
d2 = diffs(d1)
assert d1 == [4, 6, 10, 18, 34] and d2 == [2, 4, 8, 16]
nxt = s[-1] + d1[-1] + d2[-1] * 2
assert nxt == 141 and s[-1] + d1[-1] == 109
Q(T, "Pattern: differences", A, "Find the next term of the series: 3, 7, 13, 23, 41, 75, ?",
  "141", ["109", "143", "147"],
  "Two levels of differences: the second differences double",
  "First differences: 4, 6, 10, 18, 34. Second differences: 2, 4, 8, 16, which double, so the next is 32. The next "
  "first difference is 34 + 32 = 66 and the next term is 75 + 66 = 141.",
  ["First differences: 4, 6, 10, 18, 34", "Second differences: 2, 4, 8, 16 → next 32",
   "Next first difference = 34 + 32 = 66", "75 + 66 = 141"],
  short="Each difference is twice the previous one minus 2 (6 = 2 × 4 − 2, 10 = 2 × 6 − 2, …): 2 × 34 − 2 = 66.",
  why="109 repeats the difference 34; 143 and 147 use second differences of 34 and 38.", secs=70)

s = [n * n * (n + 1) for n in range(1, 8)]
assert s == [2, 12, 36, 80, 150, 252, 392]
assert diffs(diffs(diffs(s))) == [6, 6, 6, 6]
Q(T, "Pattern: squares and cubes", A, "What will come in place of the question mark (?)?\n"
  "2, 12, 36, 80, 150, 252, ?",
  "392", ["384", "400", "343"],
  "n² × (n + 1), which is n³ + n²",
  "2 = 1² × 2, 12 = 2² × 3, 36 = 3² × 4, 80 = 4² × 5, 150 = 5² × 6, 252 = 6² × 7. The next term is 7² × 8 = 392.",
  ["1 × 2 = 2, 4 × 3 = 12, 9 × 4 = 36", "16 × 5 = 80, 25 × 6 = 150, 36 × 7 = 252", "Next = 49 × 8 = 392"],
  short="Check with differences: 10, 24, 44, 70, 102 → second differences 14, 20, 26, 32 → next 38 → "
        "252 + 140 = 392.",
  why="343 is 7³ without the 7²; 384 uses a second difference of 30 instead of 38; 400 is 20².", secs=75)

s = series_from(2, lambda t, k: 3 * t - k, 6)
assert s == [2, 5, 13, 36, 104, 307]
Q(T, "Pattern: multiply-add", A, "Which number will replace the question mark?\n2, 5, 13, 36, 104, ?",
  "307", ["312", "308", "302"],
  "Multiply by 3, then subtract 1, 2, 3, 4, 5",
  "2 × 3 − 1 = 5, 5 × 3 − 2 = 13, 13 × 3 − 3 = 36, 36 × 3 − 4 = 104. The next step is 104 × 3 − 5 = 307.",
  ["2 × 3 − 1 = 5", "5 × 3 − 2 = 13", "13 × 3 − 3 = 36", "36 × 3 − 4 = 104", "104 × 3 − 5 = 307"],
  why="312 multiplies by 3 without subtracting; 308 repeats −4.", secs=60)

odd = series_from(5, lambda t, k: 2 * t, 4)
even = series_from(12, lambda t, k: 3 * t, 4)
s = [x for pair in zip(odd, even) for x in pair]
assert s == [5, 12, 10, 36, 20, 108, 40, 324]
Q(T, "Missing number series", A, "Find the missing number: 5, 12, 10, 36, 20, 108, ?, 324",
  "40", ["216", "30", "60"],
  "Two interleaved series",
  "The terms in odd positions are 5, 10, 20, ? (each doubled) and those in even positions are 12, 36, 108, 324 "
  "(each tripled). So the missing term is 20 × 2 = 40.",
  ["Odd positions: 5, 10, 20, ? → ×2 each time", "Even positions: 12, 36, 108, 324 → ×3 each time",
   "Missing term = 20 × 2 = 40"],
  why="216 doubles 108 as if the series were one chain; 60 triples 20, mixing the two rules; 30 adds 10.",
  secs=65)

# ================================================================ Wrong Number Series (B1 I1 A2)
T = "Wrong Number Series"


def wrong_series(correct, shown):
    diff = [i for i, (a, b) in enumerate(zip(correct, shown)) if a != b]
    assert len(diff) == 1, (correct, shown)
    return shown[diff[0]], correct[diff[0]]


def series_text(seq):
    return ", ".join(N(x) for x in seq)


good = series_from(2, lambda t, k: 3 * t, 7)
shown = [2, 6, 18, 54, 160, 486, 1458]
w, c = wrong_series(good, shown)
assert (w, c) == (160, 162)
Q(T, "Find the wrong term", B, f"Find the wrong number in the series:\n{series_text(shown)}",
  "160", ["54", "486", "1,458"],
  "Each term is 3 times the previous term",
  "2 × 3 = 6, 6 × 3 = 18, 18 × 3 = 54, 54 × 3 = 162. The fifth term should be 162, not 160; 162 × 3 = 486 and "
  "486 × 3 = 1,458 fit.",
  ["2 × 3 = 6", "6 × 3 = 18", "18 × 3 = 54", "54 × 3 = 162 ≠ 160", "162 × 3 = 486; 486 × 3 = 1,458"],
  why="486 looks wrong if you divide by 160, but it equals 3 × 162.", secs=30)

good = series_from(7, lambda t, k: 2 * t + k + 1, 7)
shown = [7, 16, 35, 72, 153, 312, 631]
w, c = wrong_series(good, shown)
assert good == [7, 16, 35, 74, 153, 312, 631] and (w, c) == (72, 74)
Q(T, "Find the wrong term", I, f"Which number in the series below does not fit the pattern?\n{series_text(shown)}",
  "72", ["35", "153", "312"],
  "Multiply by 2 and add 2, 3, 4, 5, …",
  "The rule is ×2 + 2, ×2 + 3, ×2 + 4, ×2 + 5, … The fourth term should be 35 × 2 + 4 = 74, and 74 × 2 + 5 = 153 "
  "confirms that 72 is wrong.",
  ["7 × 2 + 2 = 16", "16 × 2 + 3 = 35", "35 × 2 + 4 = 74 (series shows 72)", "74 × 2 + 5 = 153",
   "153 × 2 + 6 = 312", "312 × 2 + 7 = 631"],
  why="153 looks wrong if you continue from 72 (72 × 2 + 5 = 149), but it fits the correct value 74.", secs=55)

good = series_from(1, lambda t, k: t * k + k, 7)
shown = [1, 2, 6, 21, 88, 446, 2676]
w, c = wrong_series(good, shown)
assert good == [1, 2, 6, 21, 88, 445, 2676] and (w, c) == (446, 445)
Q(T, "Find the wrong term", A, f"Find the wrong number in the series:\n{series_text(shown)}",
  "446", ["21", "88", "2,676"],
  "Multiply by n and add n: ×1 + 1, ×2 + 2, ×3 + 3, …",
  "1 × 1 + 1 = 2, 2 × 2 + 2 = 6, 6 × 3 + 3 = 21, 21 × 4 + 4 = 88. The sixth term should be 88 × 5 + 5 = 445, not "
  "446; then 445 × 6 + 6 = 2,676 fits.",
  ["1 × 1 + 1 = 2", "2 × 2 + 2 = 6", "6 × 3 + 3 = 21", "21 × 4 + 4 = 88", "88 × 5 + 5 = 445 (series shows 446)",
   "445 × 6 + 6 = 2,676"],
  why="2,676 looks wrong if you continue from 446 (446 × 6 + 6 = 2,682), but it fits 445.", secs=70)

good = series_from(4, lambda t, k: t * k - 1, 7)
shown = [4, 3, 5, 15, 55, 274, 1643]
w, c = wrong_series(good, shown)
assert good == [4, 3, 5, 14, 55, 274, 1643] and (w, c) == (15, 14)
Q(T, "Find the wrong term", A, f"Exactly one term of this series is incorrect. Which one?\n{series_text(shown)}",
  "15", ["5", "55", "274"],
  "Multiply by 1, 2, 3, … and subtract 1 each time",
  "4 × 1 − 1 = 3, 3 × 2 − 1 = 5, 5 × 3 − 1 = 14. The fourth term should be 14, not 15; then 14 × 4 − 1 = 55, "
  "55 × 5 − 1 = 274 and 274 × 6 − 1 = 1,643 all fit.",
  ["4 × 1 − 1 = 3", "3 × 2 − 1 = 5", "5 × 3 − 1 = 14 (series shows 15)", "14 × 4 − 1 = 55", "55 × 5 − 1 = 274",
   "274 × 6 − 1 = 1,643"],
  why="55 looks wrong if you continue from 15 (15 × 4 − 1 = 59), but it fits the correct value 14.", secs=75)

# ================================================================ Quadratic Equations (B2 I3 A4)
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


xs, ys = [F(7), F(8)], [F(5), F(-2)]
roots_check(1, -15, 56, xs), roots_check(1, -3, -10, ys)
qe("Relation between roots", B,
   "In the following question, two equations I and II are given. Solve both and choose the correct relation between "
   "x and y.", "x² − 15x + 56 = 0", "y² − 3y − 10 = 0", xs, ys, ">", ["<=", "<"],
   "Factorising by splitting the middle term; a negative constant term gives roots of opposite signs",
   "x = 7 or 8. y = 5 or −2. The smallest x (7) is greater than the largest y (5), so x > y.",
   ["I: x² − 7x − 8x + 56 = (x − 7)(x − 8) = 0 ⇒ x = 7, 8",
    "II: y² − 5y + 2y − 10 = (y − 5)(y + 2) = 0 ⇒ y = 5, −2", "min x = 7 > max y = 5", "So x > y"],
   secs=35)

xs, ys = [F(5), F(-8)], [F(5), F(-3)]
roots_check(1, 3, -40, xs), roots_check(1, -2, -15, ys)
qe("Relation between roots", B,
   "Find the roots of both equations below and state how x and y are related.",
   "x² + 3x − 40 = 0", "y² − 2y − 15 = 0", xs, ys, "cbe", [">=", "<="],
   "Compare every pair of roots; a shared root plus opposite-side roots means no relation holds",
   "x = 5 or −8 and y = 5 or −3. x = −8 is smaller than both values of y, but x = 5 is greater than y = −3. So no "
   "single relation holds.",
   ["I: (x + 8)(x − 5) = 0 ⇒ x = 5, −8", "II: (y − 5)(y + 3) = 0 ⇒ y = 5, −3",
    "x = −8, y = 5 gives x < y", "x = 5, y = −3 gives x > y", "Relationship cannot be established"],
   why="x ≥ y and x ≤ y come from noticing the common root 5 and checking only one other pair.", secs=40)

xs, ys = [F(3), F(10, 3)], [F(4), F(9, 4)]
roots_check(3, -19, 30, xs), roots_check(4, -25, 36, ys)
qe("Relation between roots", I,
   "Compare the roots of the following pair of equations and choose the relation between x and y that is always "
   "true.", "3x² − 19x + 30 = 0", "4y² − 25y + 36 = 0", xs, ys, "cbe", ["<", "<="],
   "When the root ranges overlap, no single relation holds",
   "x = 3 or 3.33 and y = 4 or 2.25. x is less than y = 4 but greater than y = 2.25, so no relation holds.",
   ["I: 3x² − 9x − 10x + 30 = (x − 3)(3x − 10) = 0 ⇒ x = 3, 3.33",
    "II: 4y² − 16y − 9y + 36 = (y − 4)(4y − 9) = 0 ⇒ y = 4, 2.25",
    "x = 3, y = 4 gives x < y", "x = 3, y = 2.25 gives x > y", "Relationship cannot be established"],
   why="x < y comes from comparing only the larger roots (3.33 and 4).", secs=55)

xs, ys = [F(17), F(-17)], [F(17)]
assert all(r * r == 289 for r in xs) and math.isqrt(289) == 17
qe("Linear vs quadratic", I,
   "Work out every possible value of x and of y, then pick the relation that always holds.",
   "x² = 289", "y = √289", xs, ys, "<=", ["<", ">="],
   "x² = k gives x = ±√k, but the symbol √k means only the positive root",
   "x² = 289 gives x = 17 or −17. y = √289 is the principal (positive) square root, so y = 17 only. "
   "x is either equal to y or smaller, so x ≤ y.",
   ["I: x = +17 or −17", "II: y = +17 (the radical sign denotes the non-negative root)",
    "x = 17: x = y; x = −17: x < y", "So x ≤ y"],
   why="x < y misses the case x = y = 17; x ≥ y treats y = √289 as ±17 as well.", secs=45)

x8 = F(16, 2)
ys = [F(8), F(9)]
assert 4 * x8 - 7 == 2 * x8 + 9
roots_check(1, -17, 72, ys)
qe("Linear vs quadratic", I,
   "One equation is linear and the other quadratic. Solve both and choose the correct relationship.",
   "4x − 7 = 2x + 9", "y² − 17y + 72 = 0", [x8], ys, "<=", ["<", ">"],
   "Solve the linear equation directly; factorise the quadratic",
   "I: 2x = 16, so x = 8. II: (y − 8)(y − 9) = 0, so y = 8 or 9. x is equal to or smaller than y, so x ≤ y.",
   ["I: 4x − 2x = 9 + 7 ⇒ 2x = 16 ⇒ x = 8", "II: y² − 8y − 9y + 72 = (y − 8)(y − 9) = 0 ⇒ y = 8, 9",
    "x = 8 = y (when y = 8) and x < y (when y = 9)", "So x ≤ y"],
   why="x < y ignores y = 8.", secs=45)

r3, r2 = math.sqrt(3), math.sqrt(2)
xs, ys = [r3, r2], [r3, 2 * r3]
for r in xs:
    assert near(r * r - (r3 + r2) * r + math.sqrt(6), 0)
for r in ys:
    assert near(r * r - 3 * r3 * r + 6, 0)
xs_e, ys_e = [F(3), F(2)], [F(3), F(12)]  # squares compare exactly: all roots are positive
assert relation(xs_e, ys_e) == "<=" and relation(xs, ys) == "<="
qe("Relation between roots", A,
   "In the question below, solve equations I and II and identify the correct relation between x and y.",
   "x² − (√3 + √2)x + √6 = 0", "y² − 3√3y + 6 = 0", xs, ys, "<=", ["<", ">="],
   "Quadratics with surd coefficients: find two roots from their sum and product",
   "For I, the roots have sum √3 + √2 and product √6, so x = √3 or √2. For II, the roots have sum 3√3 and "
   "product 6, so y = √3 or 2√3. The largest x (√3) equals the smallest y (√3), so x ≤ y.",
   ["I: (x − √3)(x − √2) = 0 ⇒ x = √3 ≈ 1.73 or √2 ≈ 1.41",
    "II: √3 + 2√3 = 3√3 and √3 × 2√3 = 6 ⇒ y = √3 ≈ 1.73 or 2√3 ≈ 3.46",
    "max x = √3 = min y", "So x ≤ y"],
   short="All roots are positive, so compare squares: x² ∈ {3, 2}, y² ∈ {3, 12}.",
   why="x < y misses the shared root √3.", secs=90)

xs, ys = [F(-3, 2), F(-2, 3)], [F(-3, 2), F(2, 3)]
roots_check(6, 13, 6, xs), roots_check(6, 5, -6, ys)
qe("Relation between roots", A,
   "Solve both equations and choose the option that correctly relates x and y.",
   "6x² + 13x + 6 = 0", "6y² + 5y − 6 = 0", xs, ys, "cbe", ["<=", "<"],
   "Factorising with a ≠ 1; check all four pairs",
   "x = −1.5 or −0.67 and y = −1.5 or 0.67. x = −0.67 is greater than y = −1.5 but less than y = 0.67, so no "
   "relation holds.",
   ["I: 6x² + 9x + 4x + 6 = (2x + 3)(3x + 2) = 0 ⇒ x = −3/2, −2/3",
    "II: 6y² + 9y − 4y − 6 = (2y + 3)(3y − 2) = 0 ⇒ y = −3/2, 2/3",
    "x = −2/3, y = −3/2 gives x > y", "x = −2/3, y = 2/3 gives x < y", "Relationship cannot be established"],
   why="x ≤ y comes from checking only x = −1.5 against both values of y.", secs=85)

xs, ys = [F(8)], [F(7), F(8)]
assert 8 ** 3 == 512 and [r for r in range(-20, 21) if r ** 3 == 512] == [8]
roots_check(1, -15, 56, ys)
qe("Linear vs quadratic", A,
   "Find all real values of x and y and choose the correct relation.",
   "x³ − 512 = 0", "y² − 15y + 56 = 0", xs, ys, ">=", [">", "<="],
   "A cube equation x³ = k has exactly one real root",
   "x³ = 512 has the single real root x = 8. y = 7 or 8. So x is greater than or equal to y: x ≥ y.",
   ["I: x³ = 512 = 8³ ⇒ x = 8 (the only real root)", "II: (y − 7)(y − 8) = 0 ⇒ y = 7, 8",
    "x = 8 > y = 7; x = 8 = y = 8", "So x ≥ y"],
   why="x > y misses y = 8; x ≤ y comes from treating x³ = 512 like a square and adding x = −8.", secs=75)

xs, ys = [F(-7, 2), F(-4)], [F(-3, 5), F(-2)]
roots_check(2, 15, 28, xs), roots_check(5, 13, 6, ys)
qe("Relation between roots", A,
   "Solve both equations and choose the correct relation between x and y.",
   "2x² + 15x + 28 = 0", "5y² + 13y + 6 = 0", xs, ys, "<", [">=", ">"],
   "All coefficients positive ⇒ both roots negative; compare carefully on the negative side",
   "x = −3.5 or −4 and y = −0.6 or −2. The largest x (−3.5) is less than the smallest y (−2), so x < y.",
   ["I: 2x² + 8x + 7x + 28 = (x + 4)(2x + 7) = 0 ⇒ x = −4, −3.5",
    "II: 5y² + 10y + 3y + 6 = (y + 2)(5y + 3) = 0 ⇒ y = −2, −0.6", "max x = −3.5 < min y = −2", "So x < y"],
   why="x > y comes from comparing the sizes 3.5, 4 with 0.6, 2 and forgetting the negative signs.", secs=75)

# ================================================================ Number System (B1 I2 A1)
T = "Number System"
digits_ok = [d for d in range(10) if int(f"473{d}28") % 11 == 0]
assert digits_ok == [5]
Q(T, "Divisibility", B, "If the six-digit number 473x28 is divisible by 11, what is the digit x?",
  "5", ["6", "4", "7"],
  "Divisibility by 11: (sum of digits in odd places) − (sum of digits in even places) must be 0 or a multiple of 11",
  "From the left, the odd places hold 4, 3, 2 (sum 9) and the even places hold 7, x, 8 (sum 15 + x). The difference "
  "9 − (15 + x) = −(6 + x) must be a multiple of 11, so 6 + x = 11 and x = 5.",
  ["Odd places: 4 + 3 + 2 = 9", "Even places: 7 + x + 8 = 15 + x", "9 − (15 + x) = −(6 + x)",
   "6 + x = 11 ⇒ x = 5", "Check: 473528 = 11 × 43048"],
  why="6, 4 and 7 make the difference −12, −10 and −13, none of which is a multiple of 11.", secs=40)
assert 473528 == 11 * 43048

pairs = [(a, b) for a in range(1, 1093) for b in range(a, 1093) if 7 * a == 4 * b and math.lcm(a, b) == 1092]
assert pairs == [(156, 273)] and sum(pairs[0]) == 429
Q(T, "HCF and LCM", I,
  "Two numbers are in the ratio 4 : 7 and their LCM is 1,092. What is the sum of the two numbers?",
  "429", ["273", "546", "390"],
  "Numbers in ratio a : b (co-prime) are ak and bk with HCF k and LCM abk",
  "Let the numbers be 4k and 7k. Since 4 and 7 are co-prime, the LCM is 28k = 1,092, so k = 39. The numbers are "
  "156 and 273, and their sum is 429.",
  ["Numbers = 4k and 7k", "LCM = 4 × 7 × k = 28k = 1,092 ⇒ k = 39", "Numbers = 156 and 273", "Sum = 11k = 429"],
  why="273 is only the larger number; 546 is half the LCM, not the sum of the numbers; 390 would need k = 35, but "
      "1,092 ÷ 28 = 39.", secs=50)

rem = pow(2, 100, 7)
assert rem == 2 and pow(2, 3, 7) == 1 and 100 % 3 == 1
Q(T, "Remainders", I, "What is the remainder when 2¹⁰⁰ is divided by 7?",
  "2", ["1", "4", "3"],
  "Find a power of the base that leaves remainder 1, then reduce the exponent",
  "2³ = 8 leaves remainder 1 on division by 7. 2¹⁰⁰ = (2³)³³ × 2¹, so the remainder is 1³³ × 2 = 2.",
  ["2³ = 8 = 7 + 1 ⇒ 2³ ≡ 1 (mod 7)", "100 = 3 × 33 + 1", "2¹⁰⁰ = (2³)³³ × 2 ≡ 1 × 2 = 2 (mod 7)"],
  short="Remainders of 2ⁿ ÷ 7 cycle 2, 4, 1; 100 leaves remainder 1 on division by 3, so take the first value, 2.",
  why="1 assumes 100 is a multiple of 3; 4 picks the second value of the cycle (as for an exponent ≡ 2 mod 3).",
  secs=45)

z = 0
n_ = math.factorial(250)
while n_ % 10 == 0:
    n_ //= 10
    z += 1
assert z == 62 == 250 // 5 + 250 // 25 + 250 // 125 and 250 // 5 + 250 // 25 == 60 and 50 + 2 == 52
Q(T, "Divisibility", A, "How many zeros are there at the end of 250! (the product 1 × 2 × 3 × … × 250)?",
  "62", ["50", "60", "52"],
  "Trailing zeros = number of factors 5 in n! (factors of 2 are always more): ⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + …",
  "Each trailing zero needs one factor 10 = 2 × 5, and 5s are scarcer than 2s. Multiples of 5 up to 250 give 50 "
  "fives, multiples of 25 give 10 extra, and multiples of 125 give 2 more. Total = 62.",
  ["⌊250/5⌋ = 50", "⌊250/25⌋ = 10", "⌊250/125⌋ = 2", "⌊250/625⌋ = 0", "50 + 10 + 2 = 62"],
  why="50 counts each multiple of 5 once; 60 stops at 25 and misses 125 and 250 (5³ factors); 52 skips the "
      "multiples of 25.", secs=60)

# ================================================================ Percentage (B3 I2 A1)
T = "Percentage"
mx = F(288 + 12) / F(40, 100)
assert mx == 750 and F(288) / F(40, 100) == 720 and F(276) / F(40, 100) == 690
Q(T, "Basic percentage", B,
  "In an examination a candidate needs 40% of the maximum marks to pass. She scores 288 marks and fails by 12 "
  "marks. What are the maximum marks?",
  "750", ["720", "690", "780"],
  "Pass marks = marks scored + shortfall = 40% of maximum",
  "The pass mark is 288 + 12 = 300. 300 is 40% of the maximum, so the maximum = 300 ÷ 0.4 = 750.",
  ["Pass mark = 288 + 12 = 300", "40% of maximum = 300", "Maximum = 300 × 100 ÷ 40 = 750"],
  why="720 treats 288 as the pass mark; 690 subtracts 12 instead of adding it.", secs=35)

cut = F(25, 125) * 100
assert cut == 20 and F(20, 120) * 100 == F(50, 3)
Q(T, "Successive change", B,
  "The price of cooking oil rises by 25%. By what percentage must a household cut its consumption so that its "
  "spending on oil does not change?",
  "20%", ["25%", "16⅔%", "18%"],
  "Spending = price × consumption; reduction needed = r ÷ (100 + r) × 100",
  "If the price becomes 125/100 of the old price, consumption must become 100/125 = 4/5 of the old amount, a cut "
  "of 1/5 = 20%.",
  ["New price = 1.25 × old price", "Consumption factor = 1 ÷ 1.25 = 0.8", "Cut = 1 − 0.8 = 0.2 = 20%"],
  short="Reduction = 25 ÷ 125 × 100 = 20%.",
  why="25% simply copies the price rise; 16⅔% is the cut needed for a 20% price rise.", secs=35)

inc = F(7840) / F(28, 100)
assert inc == 28000 and inc * F(72, 100) == 20160
Q(T, "Income and expenditure", B,
  "Rohit spends 72% of his monthly income and saves the rest. If he saves ₹7,840 a month, what is his monthly "
  "income?",
  "₹28,000", ["₹20,160", "₹10,889", "₹30,800"],
  "Savings % = 100 − expenditure %",
  "He saves 100 − 72 = 28% of his income. 28% of income = ₹7,840, so income = 7,840 ÷ 0.28 = ₹28,000.",
  ["Savings = 28% of income", "Income = 7,840 × 100 ÷ 28 = ₹28,000"],
  why="₹20,160 is his expenditure (72% of ₹28,000); ₹10,889 divides 7,840 by 0.72.", secs=35)
assert round(7840 / 0.72) == 10889

pop = 50000 * F(102, 100) ** 2
assert pop == 52020 and 50000 * (1 + F(2, 100) * 2) == 52000 and 50000 * F(98, 100) ** 2 == 48020
Q(T, "Population and depreciation", I,
  "A town has 50,000 people. Every year its population grows by a birth rate of 3.2% and falls by a death rate of "
  "1.2% of the population at the start of that year (ignore migration). What will the population be after 2 years?",
  "52,020", ["52,000", "48,020", "52,200"],
  "Net growth rate = birth rate − death rate, compounded yearly",
  "The net growth is 3.2% − 1.2% = 2% a year, compounded. After 2 years the population is "
  "50,000 × 1.02 × 1.02 = 52,020.",
  ["Net rate = 3.2 − 1.2 = 2% per year", "After year 1: 50,000 × 1.02 = 51,000", "After year 2: 51,000 × 1.02 = 52,020"],
  why="52,000 adds 2% twice on the original population (no compounding); 48,020 treats the net rate as a 2% fall.",
  secs=50)

pc = F(120, 150) * 100
assert pc == 80 and F(150, 120) * 100 == 125
Q(T, "Basic percentage", I,
  "Two numbers are 20% and 50% more than a third number respectively. What percentage of the second number is the "
  "first number?",
  "80%", ["70%", "75%", "125%"],
  "Take the third number as 100 to compare the other two",
  "If the third number is 100, the first is 120 and the second is 150. 120 ÷ 150 × 100 = 80%.",
  ["Third = 100", "First = 120, second = 150", "120 ÷ 150 × 100 = 80%"],
  why="70% subtracts the percentages (100 − 30); 125% is the second number as a percentage of the first.", secs=45)

sols = [F(e) for e in range(1, 100) if (120 - F(112, 100) * e) == F(132, 100) * (100 - e)]
assert sols == [60]
Q(T, "Income and expenditure", A,
  "Sunita's income rises by 20% and her expenditure rises by 12%. As a result her savings rise by 32%. What "
  "percentage of her original income did she originally spend?",
  "60%", ["40%", "66⅔%", "50%"],
  "Income = expenditure + savings, before and after the change",
  "Take income = 100 and expenditure = E, so savings = 100 − E. After the change, income = 120, expenditure = "
  "1.12E and savings = 1.32(100 − E). So 120 − 1.12E = 132 − 1.32E, giving 0.2E = 12 and E = 60. She spent 60% of "
  "her income.",
  ["Income 100, expenditure E, savings 100 − E", "New income 120, new expenditure 1.12E",
   "New savings: 120 − 1.12E = 1.32(100 − E)", "120 − 1.12E = 132 − 1.32E ⇒ 0.20E = 12 ⇒ E = 60",
   "Check: savings 40 → 120 − 67.2 = 52.8 = 1.32 × 40"],
  why="40% is the savings share, not the spending share; 66⅔% and 50% fail the check (savings would change by "
      "36% and 28%).", secs=100)
for e_, g_ in ((F(200, 3), 36), (50, 28)):
    assert (120 - F(112, 100) * e_) / (100 - e_) * 100 - 100 == g_

# ================================================================ Ratio and Proportion (B1 I2 A2)
T = "Ratio and Proportion"
assert ratio(3 * 6, 4 * 6, 4 * 7) == "9 : 12 : 14"
Q(T, "Basic ratio", B, "If A : B = 3 : 4 and B : C = 6 : 7, what is A : B : C?",
  "9 : 12 : 14", ["3 : 4 : 7", "9 : 12 : 7", "6 : 8 : 7"],
  "Make the common term (B) equal in both ratios",
  "B is 4 in the first ratio and 6 in the second. Make both 12: A : B = 9 : 12 and B : C = 12 : 14. So "
  "A : B : C = 9 : 12 : 14.",
  ["LCM of 4 and 6 = 12", "A : B = 3 : 4 = 9 : 12", "B : C = 6 : 7 = 12 : 14", "A : B : C = 9 : 12 : 14"],
  why="3 : 4 : 7 joins the ratios without matching B; 9 : 12 : 7 scales only the first ratio; 6 : 8 : 7 scales "
      "the first ratio by 2 but not the second.", secs=35)

xs_ = [x for x in range(0, 23) if (23 - x) * (78 - x) == (30 - x) * (57 - x)]
assert xs_ == [6] and F(17, 24) == F(51, 72)
Q(T, "Proportion", I,
  "What number must be subtracted from each of 23, 30, 57 and 78 so that the four results are in proportion?",
  "6", ["4", "5", "7"],
  "a : b = c : d means a × d = b × c (product of extremes = product of means)",
  "Let x be subtracted. Then (23 − x)(78 − x) = (30 − x)(57 − x). Expanding, 1794 − 101x + x² = 1710 − 87x + x², "
  "so 84 = 14x and x = 6. The numbers become 17, 24, 51, 72, and 17 : 24 = 51 : 72.",
  ["(23 − x)(78 − x) = (30 − x)(57 − x)", "1794 − 101x = 1710 − 87x", "14x = 84 ⇒ x = 6",
   "Check: 17 × 72 = 1224 = 24 × 51"],
  why="4, 5 and 7 fail the check: for example 19 × 74 = 1406 but 26 × 53 = 1378.", secs=60)
assert 19 * 74 == 1406 and 26 * 53 == 1378

c_share = F(3800) * F(4, 19)
assert ratio(F(1, 4), F(1, 6), F(1, 9)) == "9 : 6 : 4" and c_share == 800 and F(3800) * F(9, 19) == 1800
assert F(3800) * F(6, 19) == 1200
Q(T, "Coins and salary share", I,
  "₹3,800 is divided among A, B and C so that 4 times A's share, 6 times B's share and 9 times C's share are all "
  "equal. What is C's share?",
  "₹800", ["₹1,800", "₹1,200", "₹950"],
  "If 4A = 6B = 9C, then A : B : C = 1/4 : 1/6 : 1/9",
  "Let 4A = 6B = 9C = k. Then A : B : C = k/4 : k/6 : k/9 = 9 : 6 : 4 (multiplying by 36). C gets 4/19 of "
  "₹3,800 = ₹800.",
  ["A : B : C = 1/4 : 1/6 : 1/9", "Multiply by LCM 36: 9 : 6 : 4", "Total parts = 19", "C = 3,800 × 4/19 = ₹800"],
  why="₹1,800 uses the ratio 4 : 6 : 9 directly instead of the reciprocals; ₹1,200 is B's share.", secs=55)

ages = [(f, s) for s in range(1, 60) for f in range(s, 120) if 2 * f == 7 * s and f * s == 896]
assert ages == [(56, 16)] and ratio(62, 22) == "31 : 11" and ratio(64, 24) == "8 : 3" and ratio(60, 20) == "3 : 1"
Q(T, "Ages via ratio", A,
  "The present ages of a father and his son are in the ratio 7 : 2, and the product of their ages is 896. What "
  "will be the ratio of their ages 6 years from now?",
  "31 : 11", ["7 : 2", "8 : 3", "3 : 1"],
  "Write the ages as 7k and 2k and use the product to find k",
  "7k × 2k = 14k² = 896, so k² = 64 and k = 8. The father is 56 and the son 16. In 6 years they will be 62 and "
  "22, a ratio of 31 : 11.",
  ["Ages 7k and 2k", "14k² = 896 ⇒ k² = 64 ⇒ k = 8", "Father 56, son 16", "After 6 years: 62 and 22",
   "62 : 22 = 31 : 11"],
  why="7 : 2 is the present ratio (a ratio of ages changes with time); 8 : 3 is the ratio after 8 years and 3 : 1 "
      "after 4 years.", secs=75)

ks = [k for k in range(1, 100) if (3 * k - 9) * 23 == (5 * k - 9) * 12]
assert ks == [11]
Q(T, "Basic ratio", A,
  "Two numbers are in the ratio 3 : 5. If 9 is subtracted from each, the ratio becomes 12 : 23. What is the "
  "smaller number?",
  "33", ["55", "27", "36"],
  "Set up one equation in the common multiplier k",
  "Let the numbers be 3k and 5k. (3k − 9)/(5k − 9) = 12/23 gives 69k − 207 = 60k − 108, so 9k = 99 and k = 11. "
  "The smaller number is 33.",
  ["(3k − 9) × 23 = (5k − 9) × 12", "69k − 207 = 60k − 108", "9k = 99 ⇒ k = 11", "Smaller = 3 × 11 = 33",
   "Check: 24 : 46 = 12 : 23"],
  why="55 is the larger number; 27 and 36 fail the check (18 : 36 and 27 : 51 are not 12 : 23).", secs=70)

# ================================================================ Problems on Ages (B1 I1 A1)
T = "Problems on Ages"
ys_ = [y for y in range(0, 50) if sum(y + 3 * i for i in range(5)) == 50]
assert ys_ == [4]
Q(T, "Present and future ages", B,
  "The sum of the ages of five children born at intervals of 3 years each is 50 years. What is the age of the "
  "youngest child?",
  "4 years", ["10 years", "16 years", "7 years"],
  "Ages in arithmetic progression: y, y + 3, y + 6, y + 9, y + 12",
  "The ages are y, y + 3, y + 6, y + 9 and y + 12, with sum 5y + 30 = 50. So 5y = 20 and y = 4.",
  ["Sum = 5y + (0 + 3 + 6 + 9 + 12) = 5y + 30", "5y + 30 = 50 ⇒ y = 4"],
  why="10 years is the average (the middle child); 16 years is the eldest.", secs=35)

bs = [b for b in range(1, 40) if 40 == 2 * (b - (40 - b))]
assert bs == [30]
Q(T, "Present and future ages", I,
  "A is now twice as old as B was when A was as old as B is now. If A is 40 years old now, how old is B now?",
  "30 years", ["20 years", "25 years", "35 years"],
  "Translate each clause; the age gap between two people never changes",
  "Let B be b years old now. A was b years old 40 − b years ago, and B was then b − (40 − b) = 2b − 40. A's "
  "present age is twice that: 40 = 2(2b − 40), so 4b = 120 and b = 30.",
  ["A was b years old (40 − b) years ago", "B's age then = b − (40 − b) = 2b − 40", "40 = 2(2b − 40) ⇒ b = 30",
   "Check: 10 years ago A was 30 (B's age now) and B was 20; 40 = 2 × 20"],
  why="20 years is B's age at that earlier time, not now.", secs=60)

sols = [(a * a + 5, a + 5) for a in range(1, 30) if a * a + 9 == 3 * (a + 9)]
assert sols == [(41, 11)]
Q(T, "Present and future ages", A,
  "Five years ago, Neha's age was the square of her son's age at that time. Four years from now, Neha will be "
  "three times as old as her son. What is Neha's present age?",
  "41 years", ["36 years", "45 years", "11 years"],
  "Let the son's age five years ago be a; Neha's was a². Form a quadratic and keep the positive root",
  "Now Neha is a² + 5 and her son a + 5. In four years: a² + 9 = 3(a + 9), so a² − 3a − 18 = 0, i.e. "
  "(a − 6)(a + 3) = 0 and a = 6. Neha's present age = 36 + 5 = 41.",
  ["Five years ago: son a, Neha a²", "In 4 years: son a + 9, Neha a² + 9", "a² + 9 = 3a + 27 ⇒ a² − 3a − 18 = 0",
   "(a − 6)(a + 3) = 0 ⇒ a = 6", "Neha now = 6² + 5 = 41; check: in 4 years 45 = 3 × 15"],
  why="36 years is her age five years ago; 45 years is her age four years from now; 11 years is the son's "
      "present age.", secs=100)

# ================================================================ Average (B3 I3 A1)
T = "Average"
ex = 5 * 48 - 4 * 45
assert ex == 60
Q(T, "Simple average", B,
  "The average of five numbers is 48. When one number is removed, the average of the remaining four is 45. Which "
  "number was removed?",
  "60", ["3", "51", "57"],
  "Total = average × count",
  "Total of five = 5 × 48 = 240. Total of four = 4 × 45 = 180. The removed number is 240 − 180 = 60.",
  ["5 × 48 = 240", "4 × 45 = 180", "240 − 180 = 60"],
  short="The removed number is 48 + 4 × 3 = 60: it is above the old average by 3 for each of the 4 that remain.",
  why="3 is only the drop in the average; 51 adds 3 to 48 once instead of four times.", secs=30)

need = 17 * 45 - 16 * 42
assert need == 93 and 42 + 3 * 16 == 90 and 3 * 17 == 51
Q(T, "Simple average", B,
  "A batsman has an average of 42 runs over 16 innings. How many runs must he score in the 17th innings to raise "
  "his average to 45?",
  "93", ["90", "45", "51"],
  "New total − old total = runs needed in the new innings",
  "Old total = 16 × 42 = 672. New total needed = 17 × 45 = 765. Runs needed = 765 − 672 = 93.",
  ["16 × 42 = 672", "17 × 45 = 765", "765 − 672 = 93"],
  short="He must score the new average plus 3 for each of the 16 old innings: 45 + 48 = 93.",
  why="90 adds 3 × 16 to the old average 42 instead of the new average 45; 45 is the new average itself.", secs=35)

n_oth = [n for n in range(1, 500) if (10 * 40000 + n * 10000) == 15000 * (10 + n)]
assert n_oth == [50]
Q(T, "Weighted average", B,
  "In an office, the 10 officers earn an average of ₹40,000 a month and the other staff earn an average of "
  "₹10,000. The average salary of all employees is ₹15,000. How many other staff are there?",
  "50", ["30", "40", "60"],
  "Weighted average: deviations above and below the overall average balance out",
  "Officers are ₹25,000 above the overall average: 10 × 25,000 = 2,50,000. Each other employee is ₹5,000 below, "
  "so their number is 2,50,000 ÷ 5,000 = 50.",
  ["10 × 40,000 + n × 10,000 = 15,000 × (10 + n)", "4,00,000 + 10,000n = 1,50,000 + 15,000n",
   "2,50,000 = 5,000n ⇒ n = 50"],
  short="Alligation: officers : others = (15 − 10) : (40 − 15) = 5 : 25 = 1 : 5, so others = 50.",
  why="30, 40 and 60 give overall averages of ₹17,500, ₹16,000 and about ₹14,286.", secs=45)
assert F(400000 + 300000, 40) == 17500 and F(400000 + 400000, 50) == 16000

women = F(21 + 23 + 8 * 2, 2)
assert women == 30 and F(21 + 23 + 2, 2) == 23 and 22 + 2 == 24 and 22 + 16 == 38
Q(T, "Replacement", I,
  "The average age of 8 men rises by 2 years when two of them, aged 21 and 23, are replaced by two women. What is "
  "the average age of the two women?",
  "30 years", ["23 years", "24 years", "38 years"],
  "Replacement: increase in total = number of people × increase in average",
  "The total age rises by 8 × 2 = 16 years. So the women together are 21 + 23 + 16 = 60 years old, an average of "
  "30 years.",
  ["Increase in total = 8 × 2 = 16", "Sum of women's ages = 44 + 16 = 60", "Average = 60 ÷ 2 = 30"],
  why="23 adds only 2 years to the total; 24 adds 2 to the men's average 22; 38 gives all 16 years to each woman.",
  secs=50)

sixth = 6 * 49 + 6 * 52 - 11 * 50
assert sixth == 56
Q(T, "Simple average", I,
  "The average of 11 results is 50. The average of the first six is 49 and the average of the last six is 52. What "
  "is the sixth result?",
  "56", ["50.5", "46", "62"],
  "The sixth result is counted in both groups of six",
  "First six total = 294 and last six total = 312. Together they count all 11 results plus the sixth one again, so "
  "the sixth = 294 + 312 − 550 = 56.",
  ["First six: 6 × 49 = 294", "Last six: 6 × 52 = 312", "All eleven: 11 × 50 = 550", "Sixth = 294 + 312 − 550 = 56"],
  why="50.5 averages 49 and 52; 46 subtracts the wrong way (550 − 504).", secs=50)

na, nb, nc = 3, 2, 3
assert F(70 * na + 60 * nb, na + nb) == 66 and F(60 * nb + 55 * nc, nb + nc) == 57
overall = F(70 * na + 60 * nb + 55 * nc, na + nb + nc)
assert overall == F(495, 8) and near(F(70 + 60 + 55, 3), 61.6667, 1e-3)
Q(T, "Weighted average", I,
  "Sections A, B and C have average marks of 70, 60 and 55. The combined average of A and B is 66, and the combined "
  "average of B and C is 57. What is the average mark of all three sections together?",
  "61.875", ["61.67", "62.5", "60.75"],
  "Use each combined average to find the ratio of section sizes, then take the weighted average",
  "A and B: 70a + 60b = 66(a + b) gives 4a = 6b, so a : b = 3 : 2. B and C: 60b + 55c = 57(b + c) gives 3b = 2c, so "
  "b : c = 2 : 3. Hence a : b : c = 3 : 2 : 3 and the overall average is (210 + 120 + 165) ÷ 8 = 61.875.",
  ["a : b from 4a = 6b ⇒ 3 : 2", "b : c from 3b = 2c ⇒ 2 : 3", "a : b : c = 3 : 2 : 3",
   "Weighted total = 70 × 3 + 60 × 2 + 55 × 3 = 495", "Average = 495 ÷ 8 = 61.875"],
  why="61.67 is the simple average of 70, 60 and 55, which ignores the different section sizes.", secs=75)

corr = F(25 * 36 - 84 + 48 - 52 + 25, 25)
assert corr == F(3348, 100) and F(900 - 36, 25) == F(3456, 100) and F(900 - 36 + 27, 25) == F(3564, 100)
Q(T, "Replacement", A,
  "The average of 25 observations was found to be 36. Later it was noticed that the observation 48 had been "
  "recorded as 84 and the observation 25 had been recorded as 52. What is the correct average?",
  "33.48", ["34.56", "35.64", "36"],
  "Correct total = wrong total − wrong values + right values",
  "Wrong total = 25 × 36 = 900. Remove the wrong entries 84 and 52 and add the right ones 48 and 25: "
  "900 − 84 − 52 + 48 + 25 = 837. Correct average = 837 ÷ 25 = 33.48.",
  ["Wrong total = 900", "Excess from the first error = 84 − 48 = 36", "Excess from the second error = 52 − 25 = 27",
   "Correct total = 900 − 36 − 27 = 837", "Average = 837 ÷ 25 = 33.48"],
  why="34.56 corrects only the first error; 35.64 corrects the first error but adds the second excess instead of "
      "removing it.", secs=80)

# ================================================================ Profit and Loss (B2 I4 A3)
T = "Profit and Loss"
sp = F(1)  # selling price of 1 metre
cp33 = 33 * sp - 11 * sp
g = (33 * sp - cp33) / cp33 * 100
assert g == 50 and F(11, 33) * 100 == F(100, 3)
Q(T, "Cost and selling price", B,
  "By selling 33 metres of cloth, a shopkeeper gains the selling price of 11 metres. What is his gain percentage?",
  "50%", ["33⅓%", "25%", "66⅔%"],
  "Gain = SP − CP; express both in terms of the selling price of one metre",
  "SP of 33 m − CP of 33 m = SP of 11 m, so CP of 33 m = SP of 22 m. The gain is the SP of 11 m on a cost equal to "
  "the SP of 22 m: 11/22 = 50%.",
  ["SP(33) − CP(33) = SP(11)", "CP(33) = SP(22)", "Gain % = SP(11) ÷ SP(22) × 100 = 50%"],
  why="33⅓% takes the gain as a percentage of the selling price (11/33) instead of the cost.", secs=40)

mp = 800 * F(135, 100)
d = (mp - 972) / mp * 100
assert mp == 1080 and d == 10 and (972 - 800) / F(800) * 100 == F(215, 10)
Q(T, "Marked price", B,
  "An article costing ₹800 is marked 35% above its cost price and sold for ₹972. What discount percentage was "
  "allowed?",
  "10%", ["11.11%", "21.5%", "8%"],
  "Discount % is always calculated on the marked price",
  "Marked price = 800 × 1.35 = ₹1,080. Discount = 1,080 − 972 = ₹108, which is 108 ÷ 1,080 = 10% of the marked "
  "price.",
  ["MP = 800 × 135/100 = 1,080", "Discount = 1,080 − 972 = 108", "Discount % = 108 ÷ 1,080 × 100 = 10%"],
  why="11.11% divides the discount by the selling price; 21.5% is the profit percentage (172 on 800).", secs=40)

gain = F(1100, 900) - 1
assert gain == F(2, 9) and (F(11, 10) * F(11, 10) - 1) * 100 == 21
Q(T, "Dishonest dealer", I,
  "A shopkeeper uses a weight that reads 1 kg but actually holds 1.1 kg when he buys goods, and a weight that "
  "reads 1 kg but holds only 900 g when he sells. He buys and sells at the same price per 'kg'. What is his gain "
  "percentage?",
  "22 2/9%", ["20%", "21%", "11 1/9%"],
  "Compare the quantity he actually receives with the quantity he actually gives for the same money",
  "For the price of 1 kg he receives 1,100 g when buying and hands over only 900 g when selling. So the money he "
  "gets for 900 g would buy him 1,100 g: gain = 1,100/900 − 1 = 2/9 = 22 2/9%.",
  ["Buying: price P gets 1,100 g", "Selling: 900 g fetches P", "Gain factor = 1,100 ÷ 900 = 11/9",
   "Gain % = (11/9 − 1) × 100 = 22 2/9%"],
  short="Gain % = (100 + a)/(100 − b) − 1 with a = 10 and b = 10: 110/90 − 1 = 22 2/9%.",
  why="20% adds the two 10% cheats; 21% treats them as successive 10% gains (1.1 × 1.1); 11 1/9% counts only the "
      "selling cheat.", secs=60)

cost = F(2250) / (F(125, 100) * F(120, 100) - 1)
assert cost == 4500 and cost * F(150, 100) == 6750 and F(2250) / F(45, 100) == 5000
Q(T, "Successive transactions", I,
  "A sells a bicycle to B at a profit of 25%, and B sells it to C at a profit of 20%. C pays ₹2,250 more than A's "
  "cost price. What was A's cost price?",
  "₹4,500", ["₹5,000", "₹6,750", "₹3,750"],
  "Successive percentage changes multiply",
  "C pays 1.25 × 1.20 = 1.5 times A's cost, i.e. 50% more. So 50% of A's cost = ₹2,250 and A's cost = ₹4,500.",
  ["C's price = A's cost × 1.25 × 1.20 = 1.5 × A's cost", "Excess = 0.5 × A's cost = 2,250", "A's cost = ₹4,500"],
  why="₹5,000 adds the profit percentages (25 + 20 = 45%); ₹6,750 is what C paid.", secs=50)

cp1, cp2 = F(2400) / F(120, 100), F(2400) / F(80, 100)
res = (4800 - (cp1 + cp2)) / (cp1 + cp2) * 100
assert (cp1, cp2) == (2000, 3000) and res == -4
Q(T, "Cost and selling price", I,
  "A dealer sold two mobile phones for ₹2,400 each. On one he gained 20% and on the other he lost 20%. What is his "
  "overall gain or loss percentage?",
  "4% loss", ["No gain, no loss", "4% gain", "2% loss"],
  "Equal selling prices with equal gain and loss % always give a net loss of (x/10)² %",
  "Cost of the first = 2,400 ÷ 1.2 = ₹2,000; cost of the second = 2,400 ÷ 0.8 = ₹3,000. Total cost ₹5,000, total "
  "sale ₹4,800, so the loss is ₹200, i.e. 4%.",
  ["CP₁ = 2,400 ÷ 1.20 = 2,000", "CP₂ = 2,400 ÷ 0.80 = 3,000", "Total CP = 5,000; total SP = 4,800",
   "Loss = 200 ⇒ 200 ÷ 5,000 × 100 = 4%"],
  short="Loss % = (20/10)² = 4%.",
  why="'No gain, no loss' assumes the +20% and −20% cancel, but they apply to different cost prices.", secs=50)

cp = F(156) / (F(125, 100) * F(92, 100) - 1)
assert cp == 1040 and cp * F(125, 100) == 1300 and cp * F(115, 100) == 1196 and F(156) / F(125, 1000) == 1248
Q(T, "Marked price", I,
  "A shopkeeper marks a lamp 25% above its cost price and allows a discount of 8%. If his profit is ₹156, what is "
  "the cost price of the lamp?",
  "₹1,040", ["₹1,248", "₹1,196", "₹1,300"],
  "Selling price = CP × (1 + markup) × (1 − discount)",
  "SP = CP × 1.25 × 0.92 = 1.15 × CP, so the profit is 15% of CP. 0.15 × CP = 156 gives CP = ₹1,040.",
  ["SP = 1.25 × 0.92 × CP = 1.15 CP", "Profit = 0.15 CP = 156", "CP = 156 ÷ 0.15 = ₹1,040"],
  why="₹1,248 takes the profit as 12.5%; ₹1,196 is the selling price and ₹1,300 the marked price.", secs=55)

g = (F(96, 100) * 1000 / 840 - 1) * 100
assert g == F(100, 7) and near((F(1000, 840) - 1) * 100, 19.0476, 1e-3)
Q(T, "Dishonest dealer", A,
  "A dealer claims to sell rice at a loss of 4% on the cost price, but he gives only 840 g when the customer pays "
  "for 1 kg. What is his actual gain or loss percentage?",
  "14 2/7% gain", ["12% gain", "19.05% gain", "16% gain"],
  "Actual gain = money received ÷ cost of the quantity actually given",
  "Let 1 kg cost ₹1,000, so 840 g costs ₹840. He charges 96% of ₹1,000 = ₹960 for those 840 g. Gain = 120 on 840, "
  "i.e. 1/7 = 14 2/7%.",
  ["Cost of 1 kg = 1,000 ⇒ cost of 840 g = 840", "Price charged = 1,000 × 0.96 = 960", "Gain = 960 − 840 = 120",
   "Gain % = 120 ÷ 840 × 100 = 14 2/7%"],
  why="12% subtracts 4 from 16 (the weight cut as a percentage of 1 kg); 19.05% ignores the 4% price cut; 16% is the "
      "weight cut alone.", secs=80)

per = F(11, 4) - F(12, 5)
n_or = F(175) / per
assert per == F(35, 100) and n_or == 500
Q(T, "Cost and selling price", A,
  "A vendor buys oranges at 5 for ₹12 and sells them at 4 for ₹11. How many oranges must he sell to earn a profit "
  "of ₹175?",
  "500", ["400", "625", "700"],
  "Profit per article = SP per article − CP per article",
  "Cost per orange = 12 ÷ 5 = ₹2.40 and selling price per orange = 11 ÷ 4 = ₹2.75, so he gains ₹0.35 per orange. "
  "175 ÷ 0.35 = 500 oranges.",
  ["CP per orange = 2.40", "SP per orange = 2.75", "Profit per orange = 0.35", "Oranges = 175 ÷ 0.35 = 500"],
  short="Take 20 oranges (LCM of 5 and 4): cost ₹48, sale ₹55, profit ₹7. ₹175 needs 25 × 20 = 500 oranges.",
  why="400, 625 and 700 oranges give profits of ₹140, ₹218.75 and ₹245; only 500 oranges give ₹175.", secs=70)
assert 400 * per == 140 and 625 * per == F(21875, 100) and 700 * per == 245

xs_ = [x for x in range(0, 101) if (1 + F(x, 100)) * F(90, 100) * F(95, 100) == F(1026, 1000)]
assert xs_ == [20]
Q(T, "Marked price", A,
  "A trader marks his goods a certain percentage above cost. During a festival he allows two successive discounts "
  "of 10% and 5% and still makes a profit of 2.6%. By what percentage above cost had he marked the goods?",
  "20%", ["17.6%", "15%", "25%"],
  "Cost × (1 + m) × 0.90 × 0.95 = cost × 1.026",
  "Let the cost be 100 and the markup m%. The selling price is 100(1 + m/100) × 0.9 × 0.95 = 0.855 × (100 + m). "
  "This equals 102.6, so 100 + m = 120 and m = 20%.",
  ["0.90 × 0.95 = 0.855", "0.855 × (100 + m) = 102.6", "100 + m = 120 ⇒ m = 20%"],
  why="17.6% simply adds 2.6 + 10 + 5; 15% and 25% give profits of −1.675% and +6.875%.", secs=80)
assert (F(115, 100) * F(855, 1000) - 1) * 100 == F(-1675, 1000) and (F(125, 100) * F(855, 1000) - 1) * 100 == F(6875, 1000)

# ================================================================ Discount (B1 I1 A1)
T = "Discount"
d = F(2400 - 2040, 2400) * 100
assert d == 15 and near(F(360, 2040) * 100, 17.647, 1e-3)
Q(T, "Single discount", B,
  "A jacket marked at ₹2,400 is sold for ₹2,040. What is the rate of discount?",
  "15%", ["17.65%", "18%", "12%"],
  "Discount % = discount ÷ marked price × 100",
  "Discount = 2,400 − 2,040 = ₹360, and 360 ÷ 2,400 × 100 = 15%.",
  ["Discount = 2,400 − 2,040 = 360", "360 ÷ 2,400 × 100 = 15%"],
  why="17.65% divides the discount by the selling price instead of the marked price.", secs=30)

eq = (1 - F(80, 100) * F(90, 100) * F(95, 100)) * 100
assert eq == F(316, 10) and (1 - F(80, 100) * F(90, 100)) * 100 == 28
Q(T, "Successive discounts", I,
  "What single discount is equivalent to three successive discounts of 20%, 10% and 5%?",
  "31.6%", ["35%", "28%", "33%"],
  "Successive discounts multiply the remaining fractions: 0.8 × 0.9 × 0.95",
  "After the three discounts the customer pays 0.80 × 0.90 × 0.95 = 0.684 of the marked price, so the single "
  "equivalent discount is 1 − 0.684 = 31.6%.",
  ["0.80 × 0.90 = 0.72", "0.72 × 0.95 = 0.684", "Equivalent discount = 100 − 68.4 = 31.6%"],
  why="35% adds the three rates; 28% stops after the first two discounts.", secs=45)

eff = F(3, 4) * F(9, 10)
mk = F(117, 100) / eff
assert eff == F(27, 40) and mk == F(26, 15) and (mk - 1) * 100 == F(220, 3)
assert (F(117, 100) / F(3, 4) - 1) * 100 == 56 and (F(117, 100) / F(65, 100) - 1) * 100 == 80
assert (F(117, 100) / F(9, 10) - 1) * 100 == 30
Q(T, "Discount with profit", A,
  "A store offers 'buy 3, get 1 free' and then a further 10% discount on the bill. Even so, it makes a profit of "
  "17% on its cost. By what percentage above cost are the goods marked?",
  "73⅓%", ["56%", "80%", "30%"],
  "Convert the offer into an effective selling price per article, then compare with the cost",
  "For 4 articles the customer pays for 3, less 10%: 3 × 0.9 = 2.7 marked prices. So each article sells for "
  "2.7/4 = 0.675 of its marked price. 0.675 × MP = 1.17 × CP gives MP = 1.7333 × CP, i.e. 73⅓% above cost.",
  ["Pay for 3 of 4 articles: 3 × MP", "Further 10% off: 2.7 × MP for 4 articles", "Per article: 0.675 × MP",
   "0.675 MP = 1.17 CP ⇒ MP = 1.17 ÷ 0.675 CP = 1.7333 CP", "Markup = 73⅓%"],
  why="56% ignores the extra 10% discount; 80% adds the two discounts (25% + 10% = 35%) instead of multiplying; 30% "
      "ignores the free article.", secs=100)

# ================================================================ Simple Interest (B1 I1 A2)
T = "Simple Interest"
r = F(8320 - 6400) * 100 / (6400 * 4)
assert r == F(75, 10) and F(1920, 6400) * 100 == 30
Q(T, "Basic SI", B,
  "At what rate of simple interest per annum will ₹6,400 amount to ₹8,320 in 4 years?",
  "7.5%", ["7%", "8%", "30%"],
  "SI = P × R × T ÷ 100, with SI = amount − principal",
  "Interest = 8,320 − 6,400 = ₹1,920. R = 1,920 × 100 ÷ (6,400 × 4) = 7.5%.",
  ["SI = 8,320 − 6,400 = 1,920", "R = 1,920 × 100 ÷ 25,600", "R = 7.5%"],
  why="30% is the total interest over 4 years as a percentage of the principal, not the yearly rate.", secs=35)

yearly = F(12005 - 9800, 3)
p_ = 9800 - 5 * yearly
r = yearly / p_ * 100
assert yearly == 735 and p_ == 6125 and r == 12 and F(735, 9800) * 100 == F(75, 10)
Q(T, "Basic SI", I,
  "A sum of money lent at simple interest amounts to ₹9,800 in 5 years and to ₹12,005 in 8 years. What is the rate "
  "of interest per annum?",
  "12%", ["7.5%", "15%", "10.5%"],
  "The difference of two amounts is the interest for the difference in years",
  "Interest for 3 years = 12,005 − 9,800 = ₹2,205, so one year's interest is ₹735. The principal is "
  "9,800 − 5 × 735 = ₹6,125, and the rate is 735 ÷ 6,125 × 100 = 12%.",
  ["3 years' interest = 2,205 ⇒ 1 year = 735", "Principal = 9,800 − 3,675 = 6,125", "R = 735 ÷ 6,125 × 100 = 12%"],
  why="7.5% divides the yearly interest by the 5-year amount (₹9,800) instead of the principal.", secs=60)

rs = [F(k, 10) for k in range(1, 300) if 3 * F(k, 10) + 4 * (F(k, 10) + 2) + 3 * (F(k, 10) + 4) == 92]
assert rs == [F(72, 10)]
Q(T, "SI with changing rates", A,
  "A bank charges simple interest at r% per annum for the first 3 years, (r + 2)% for the next 4 years and "
  "(r + 4)% for the 3 years after that. If the total interest for the 10 years is 92% of the principal, what is r?",
  "7.2", ["9.2", "6.5", "7.5"],
  "Total SI % = Σ (rate × years) for each period",
  "Total interest as a percentage of the principal = 3r + 4(r + 2) + 3(r + 4) = 10r + 20. Setting 10r + 20 = 92 "
  "gives r = 7.2.",
  ["First 3 years: 3r%", "Next 4 years: 4(r + 2)% = 4r + 8%", "Last 3 years: 3(r + 4)% = 3r + 12%",
   "10r + 20 = 92 ⇒ r = 7.2"],
  why="9.2 forgets the extra 2% and 4% (10r = 92); 7.5 gives 95%, and 6.5 gives 85%.", secs=75)
assert 10 * F(75, 10) + 20 == 95 and 10 * F(65, 10) + 20 == 85

xs_ = [F(k, 10) for k in range(1, 70000) if 4 * F(k, 10) + F(k, 10) * F(5, 100) * (3 + 2 + 1) == 6450]
assert xs_ == [1500]
Q(T, "Basic SI", A,
  "What equal annual instalment, paid at the end of each year, will discharge a debt of ₹6,450 due in 4 years at "
  "5% per annum simple interest?",
  "₹1,500", ["₹1,612.50", "₹1,290", "₹1,400"],
  "Each instalment earns simple interest from its payment date to the due date; their total equals the debt",
  "Let each instalment be x. The first earns interest for 3 years, the second for 2, the third for 1 and the "
  "fourth for none. Total value at the due date = 4x + x × 5% × (3 + 2 + 1) = 4x + 0.3x = 4.3x = 6,450, so "
  "x = ₹1,500.",
  ["Value at due date = x(1 + 0.15) + x(1 + 0.10) + x(1 + 0.05) + x", "= 4x + 0.30x = 4.3x", "4.3x = 6,450",
   "x = ₹1,500"],
  why="₹1,612.50 divides the debt by 4 and ignores interest on the instalments; ₹1,290 divides by 5.", secs=90)

# ================================================================ Compound Interest (B1 I2 A1)
T = "Compound Interest"
rs = [r for r in range(1, 50) if 6400 * F(100 + r, 100) ** 2 == 7744]
assert rs == [10] and F(7744 - 6400, 6400 * 2) * 100 == F(105, 10)
Q(T, "Annual compounding", B,
  "At what rate of compound interest per annum, compounded annually, will ₹6,400 become ₹7,744 in 2 years?",
  "10%", ["10.5%", "11%", "21%"],
  "A = P(1 + R/100)ⁿ; take the square root of A/P",
  "7,744 ÷ 6,400 = 1.21 = (1.1)², so 1 + R/100 = 1.1 and R = 10%.",
  ["A/P = 7,744 ÷ 6,400 = 1.21", "√1.21 = 1.1", "R = 10%"],
  short="7744 = 88² and 6400 = 80², so 1 + R/100 = 88/80 = 1.1.",
  why="10.5% is the simple-interest rate for the same amounts; 21% is the total growth over two years.", secs=40)

ci = 16000 * (F(105, 100) ** 3 - 1)
assert ci == 2522 and 16000 * F(20, 100) * F(3, 4) == 2400 and 16000 * (F(105, 100) ** 2 - 1) == 1640
Q(T, "Half-yearly and quarterly", I,
  "Find the compound interest on ₹16,000 for 9 months at 20% per annum, compounded quarterly.",
  "₹2,522", ["₹2,400", "₹1,640", "₹3,840"],
  "Quarterly compounding: rate ÷ 4 per quarter, number of quarters as the exponent",
  "The quarterly rate is 20 ÷ 4 = 5% and 9 months = 3 quarters. Amount = 16,000 × 1.05³ = 16,000 × 1.157625 = "
  "₹18,522, so CI = ₹2,522.",
  ["Rate per quarter = 5%; quarters = 3", "1.05³ = 1.157625", "Amount = 16,000 × 1.157625 = 18,522",
   "CI = 18,522 − 16,000 = ₹2,522"],
  why="₹2,400 is simple interest; ₹1,640 counts only 2 quarters.", secs=55)

p_ = [(p, r) for p in range(100, 50001, 100) for r in range(1, 41)
      if p * r * 2 == 1600 * 100 and p * (F(100 + r, 100) ** 2 - 1) == 1680]
assert p_ == [(8000, 10)]
Q(T, "CI vs SI difference", I,
  "The simple interest on a sum for 2 years is ₹1,600 and the compound interest on it for 2 years at the same rate "
  "(compounded annually) is ₹1,680. What is the sum?",
  "₹8,000", ["₹16,000", "₹4,000", "₹8,400"],
  "CI − SI for 2 years = interest earned in year 2 on the first year's interest",
  "SI for one year = 1,600 ÷ 2 = ₹800. The extra ₹80 in CI is interest on that ₹800 for one year, so the rate is "
  "80 ÷ 800 = 10%. Then the sum = 800 ÷ 10% = ₹8,000.",
  ["One year's SI = 800", "CI − SI = 80 = 800 × R/100 ⇒ R = 10%", "P = 800 × 100 ÷ 10 = ₹8,000",
   "Check: 8,000 × 1.21 − 8,000 = 1,680"],
  why="₹16,000 uses the 2-year SI (₹1,600) as one year's interest; ₹4,000 uses a 20% rate.", secs=60)

half = 25000 * F(11, 10) ** 4
ann = 25000 * F(12, 10) ** 2
assert half - ann == F(6025, 10) and 25000 * (F(121, 100) - F(120, 100)) == 250 and half - 25000 * F(14, 10) == F(16025, 10)
Q(T, "Half-yearly and quarterly", A,
  "On ₹25,000 at 20% per annum for 2 years, by how much does the compound interest compounded half-yearly exceed "
  "the compound interest compounded annually?",
  "₹602.50", ["₹250", "₹500", "₹1,602.50"],
  "Half-yearly: rate/2 per half-year, 2n half-years",
  "Half-yearly: 25,000 × 1.1⁴ = 25,000 × 1.4641 = ₹36,602.50. Annually: 25,000 × 1.2² = 25,000 × 1.44 = ₹36,000. "
  "The difference is ₹602.50.",
  ["Half-yearly: 10% for 4 periods ⇒ 1.1⁴ = 1.4641", "Amount = 36,602.50",
   "Annually: 20% for 2 years ⇒ 1.2² = 1.44", "Amount = 36,000", "Difference = ₹602.50"],
  why="₹250 is the difference for 1 year only; ₹1,602.50 compares the half-yearly CI with simple interest.",
  secs=90)

# ================================================================ Partnership (B1 I3 A2)
T = "Partnership"
parts = [18, 27, 36]
unit = F(4800, 4 - 2)
assert ratio(*parts) == "2 : 3 : 4" and unit == 2400 and unit * 9 == 21600 and 4800 * 9 == 43200 and unit * 6 == 14400
Q(T, "Simple partnership", B,
  "P, Q and R invest ₹18,000, ₹27,000 and ₹36,000 in a business for a year. At the end of the year R gets ₹4,800 "
  "more than P. What is the total profit?",
  "₹21,600", ["₹43,200", "₹14,400", "₹10,800"],
  "Profit is shared in the ratio of capitals when the time is the same",
  "Capitals are in the ratio 18 : 27 : 36 = 2 : 3 : 4. R gets 2 parts more than P, so 2 parts = ₹4,800 and one "
  "part = ₹2,400. Total = 9 parts = ₹21,600.",
  ["Ratio = 2 : 3 : 4 (9 parts)", "R − P = 4 − 2 = 2 parts = 4,800", "1 part = 2,400", "Total = 9 × 2,400 = ₹21,600"],
  why="₹43,200 treats ₹4,800 as one part instead of two; ₹14,400 is P's and R's combined share (6 parts), not the "
      "total.", secs=40)

cap = {"A": 40 * 12, "B": 60 * 9, "C": 80 * 6}
assert ratio(*cap.values()) == "8 : 9 : 8" and F(50000 * 9, 25) == 18000
Q(T, "Compound partnership", I,
  "Asha starts a business with ₹40,000. Bharat joins after 3 months with ₹60,000 and Chetan joins after 6 months "
  "with ₹80,000. Out of a profit of ₹50,000 at the end of the year, what is Bharat's share?",
  "₹18,000", ["₹16,000", "₹15,000", "₹16,667"],
  "Profit share ∝ capital × months invested",
  "Capital-months: Asha 40,000 × 12, Bharat 60,000 × 9, Chetan 80,000 × 6, i.e. 480 : 540 : 480 = 8 : 9 : 8. "
  "Bharat gets 9/25 of ₹50,000 = ₹18,000.",
  ["Asha: 40 × 12 = 480", "Bharat: 60 × 9 = 540", "Chetan: 80 × 6 = 480", "Ratio 8 : 9 : 8 (25 parts)",
   "Bharat = 50,000 × 9/25 = ₹18,000"],
  why="₹16,000 is Asha's (or Chetan's) share; ₹16,667 ignores time and uses the capital ratio 2 : 3 : 4.", secs=55)
assert F(50000 * 8, 25) == 16000 and round(50000 * 3 / 9) == 16667

ts = [t for t in range(1, 13) if F(5 * 8, 6 * t) == F(2, 3)]
assert ts == [10]
Q(T, "Compound partnership", I,
  "The capitals of A and B are in the ratio 5 : 6 and their profits are in the ratio 2 : 3. If A's capital was "
  "invested for 8 months, for how many months was B's capital invested?",
  "10 months", ["12 months", "9 months", "8 months"],
  "Profit ratio = (capital × time) ratio",
  "(5 × 8) : (6 × t) = 2 : 3, so 40 × 3 = 12t and t = 10 months.",
  ["5 × 8 : 6 × t = 2 : 3", "120 = 12t", "t = 10 months"],
  why="12 months assumes B stayed the full year; 8 months assumes equal time, which would give a 5 : 6 profit ratio.",
  secs=50)

sal = 1500 * 12
rest = 108000 - sal
a_total = sal + F(rest * 2, 5)
assert ratio(60000, 90000) == "2 : 3" and a_total == 54000 and F(108000 * 2, 5) == 43200 and sal + 43200 == 61200
Q(T, "Working partner", I,
  "Anil and Bimal invest ₹60,000 and ₹90,000 in a shop. Anil runs the shop and draws ₹1,500 a month as salary; "
  "the remaining profit is shared in the ratio of capitals. If the profit for the year is ₹1,08,000, how much does "
  "Anil receive in all?",
  "₹54,000", ["₹43,200", "₹36,000", "₹61,200"],
  "Pay the working partner's salary first, then divide the rest by capital",
  "Salary for the year = 1,500 × 12 = ₹18,000. Remaining profit = ₹90,000, shared 2 : 3, so Anil gets ₹36,000 "
  "more. Total = 18,000 + 36,000 = ₹54,000.",
  ["Salary = 18,000", "Remaining profit = 1,08,000 − 18,000 = 90,000", "Capital ratio 60 : 90 = 2 : 3",
   "Anil's share = 90,000 × 2/5 = 36,000", "Total = ₹54,000"],
  why="₹43,200 ignores the salary; ₹36,000 leaves out the salary from the total; ₹61,200 adds the salary but "
      "shares the whole profit before deducting it.", secs=60)

xs_ = [x for x in range(0, 12) if F(45 * 12, 60 * (12 - x)) == F(3, 2)]
assert xs_ == [6]
c_months = 12 - xs_[0] - 2
c_share = F(126000 * 90 * c_months, 45 * 12 + 60 * (12 - xs_[0]) + 90 * c_months)
assert c_months == 4 and c_share == 36000
Q(T, "Compound partnership", A,
  "Ajay starts a business with ₹45,000. Some months later Bina joins with ₹60,000, and 2 months after Bina, Charu "
  "joins with ₹90,000. At the end of the year the profits of Ajay and Bina are in the ratio 3 : 2. Out of a total "
  "profit of ₹1,26,000, what is Charu's share?",
  "₹36,000", ["₹54,000", "₹42,000", "₹45,000"],
  "Find the unknown joining month from the given profit ratio, then share by capital × months",
  "Ajay: 45 × 12 = 540. If Bina stays t months, 540 : 60t = 3 : 2, so 60t = 360 and t = 6 (she joins after 6 "
  "months). Charu joins 2 months later and stays 4 months: 90 × 4 = 360. Ratio 540 : 360 : 360 = 3 : 2 : 2, so "
  "Charu gets 2/7 of ₹1,26,000 = ₹36,000.",
  ["Ajay: 45 × 12 = 540", "540 : 60t = 3 : 2 ⇒ t = 6 months", "Charu: 90 × 4 = 360",
   "Ratio 540 : 360 : 360 = 3 : 2 : 2", "Charu = 1,26,000 × 2/7 = ₹36,000"],
  why="₹54,000 is Ajay's share; ₹42,000 gives Charu 6 months, like Bina, instead of 4 (ratio 540 : 360 : 540).",
  secs=100)
assert F(126000 * 3, 7) == 54000 and F(126000 * 540, 540 + 360 + 540) == 47250

c_sh = F(84000 * 2, 7)
assert ratio(F(3, 2), 1, F(2, 5) * F(5, 2)) == "3 : 2 : 2" and c_sh == 24000 and 84000 * F(4, 10) == 33600
Q(T, "Simple partnership", A,
  "In a firm, A's capital is 1.5 times B's capital, and C's capital is 40% of A's and B's capitals together. All "
  "three invest for the same period. Out of a profit of ₹84,000, what is C's share?",
  "₹24,000", ["₹33,600", "₹36,000", "₹21,000"],
  "Express every capital in terms of one of them",
  "Let B = 2x, so A = 3x. A + B = 5x and C = 40% of 5x = 2x. Ratio A : B : C = 3 : 2 : 2, so C gets 2/7 of "
  "₹84,000 = ₹24,000.",
  ["B = 2x ⇒ A = 3x", "C = 0.4 × 5x = 2x", "A : B : C = 3 : 2 : 2", "C = 84,000 × 2/7 = ₹24,000"],
  why="₹33,600 is 40% of the profit; ₹36,000 is A's share.", secs=70)

# ================================================================ Mixture and Alligation (B1 I1 A1)
T = "Mixture and Alligation"
w = [(a, b) for a in range(1, 20) for b in range(1, 20) if math.gcd(a, b) == 1 and F(60 * b, a + b) == 48]
assert w == [(1, 4)]
Q(T, "Alligation rule", B,
  "In what ratio must water be mixed with milk costing ₹60 per litre so that the mixture is worth ₹48 per litre?",
  "1 : 4", ["4 : 1", "1 : 5", "1 : 3"],
  "Alligation: water costs ₹0 per litre",
  "By alligation, water : milk = (60 − 48) : (48 − 0) = 12 : 48 = 1 : 4.",
  ["Water ₹0, milk ₹60, mean ₹48", "Water : milk = (60 − 48) : (48 − 0)", "= 12 : 48 = 1 : 4",
   "Check: 4 litres of milk cost ₹240; 5 litres of mixture at ₹48 = ₹240"],
  why="4 : 1 is the ratio reversed (milk : water).", secs=35)

xs_ = [F(k, 2) for k in range(1, 200) if F(70, 100) * F(k, 2) + F(40, 100) * 30 == F(50, 100) * (30 + F(k, 2))]
assert xs_ == [15]
Q(T, "Mixing solutions", I,
  "How many litres of a 70% alcohol solution must be added to 30 litres of a 40% alcohol solution to get a 50% "
  "alcohol solution?",
  "15 litres", ["10 litres", "20 litres", "12 litres"],
  "Alligation on concentrations, or a balance of pure alcohol",
  "By alligation, 40% : 70% solution = (70 − 50) : (50 − 40) = 2 : 1. With 30 litres of the 40% solution, "
  "the 70% solution needed is 15 litres.",
  ["Ratio 40% : 70% = (70 − 50) : (50 − 40) = 2 : 1", "30 litres ↔ 2 parts ⇒ 1 part = 15 litres",
   "Check: alcohol = 12 + 10.5 = 22.5 litres in 45 litres = 50%"],
  why="10 litres gives 47.5%; 20 litres gives 52%.", secs=50)
assert F(12 + 7, 40) * 100 == F(475, 10) and F(12 + 14, 50) * 100 == 52

xs_ = [x for x in range(1, 50) if (1 - F(x, 50)) ** 2 == F(16, 25)]
assert xs_ == [10] and (1 - F(20, 50)) ** 2 == F(9, 25)
Q(T, "Replacement of mixture", A,
  "A cask holds 50 litres of pure juice. Some juice is drawn off and replaced with water; then the same quantity of "
  "the mixture is drawn off and replaced with water again. Juice and water are now in the ratio 16 : 9. How many "
  "litres were drawn off each time?",
  "10 litres", ["8 litres", "12.5 litres", "20 litres"],
  "After n replacements, juice left = initial × (1 − x/V)ⁿ",
  "Juice left is 16/25 of the cask, so (1 − x/50)² = 16/25. Then 1 − x/50 = 4/5, x/50 = 1/5 and x = 10 litres.",
  ["Juice fraction after 2 draws = (1 − x/50)²", "(1 − x/50)² = 16/(16 + 9) = 16/25", "1 − x/50 = 4/5",
   "x = 10 litres"],
  why="20 litres gives juice : water = 9 : 16 (the ratio reversed); 8 and 12.5 litres give 441 : 184 and 9 : 7.",
  secs=85)
assert (1 - F(8, 50)) ** 2 == F(441, 625) and (1 - F(25, 2) / 50) ** 2 == F(9, 16)

# ================================================================ Time and Work (B3 I2 A1)
T = "Time and Work"
total = (3 + 1) * 12
assert total == 48 and F(total, 3) == 16 and F(total, 1) == 48
Q(T, "Work efficiency", B,
  "A is three times as efficient as B. Working together they finish a job in 12 days. In how many days can A alone "
  "finish it?",
  "16 days", ["48 days", "36 days", "18 days"],
  "Work = efficiency × time",
  "Let B do 1 unit a day, so A does 3. Together they do 4 units a day for 12 days, i.e. 48 units. A alone takes "
  "48 ÷ 3 = 16 days.",
  ["A : B efficiency = 3 : 1", "Total work = (3 + 1) × 12 = 48 units", "A alone = 48 ÷ 3 = 16 days"],
  why="48 days is B's time alone; 36 days multiplies 12 by 3.", secs=35)

days = F(16 * 15 * 9, 20 * 8)
assert days == F(27, 2) and F(16 * 15 * 8, 20 * 9) == F(32, 3)
Q(T, "Work efficiency", B,
  "16 workers can build a wall in 15 days working 9 hours a day. In how many days can 20 workers build the same "
  "wall working 8 hours a day?",
  "13.5 days", ["12 days", "15 days", "10⅔ days"],
  "M₁ × D₁ × H₁ = M₂ × D₂ × H₂ for the same work",
  "Total work = 16 × 15 × 9 = 2,160 worker-hours. 20 workers working 8 hours a day put in 160 worker-hours a day, "
  "so they need 2,160 ÷ 160 = 13.5 days.",
  ["Work = 16 × 15 × 9 = 2,160 worker-hours", "Per day now = 20 × 8 = 160", "Days = 2,160 ÷ 160 = 13.5"],
  why="12 days ignores the change in hours; 10⅔ days swaps the hours (multiplies by 8/9 instead of 9/8).", secs=40)
assert F(16 * 15, 20) == 12

units = (6 * 2 + 8 * 1) * 10
d = F(units, 4 * 2 + 4 * 1)
assert units == 200 and d == F(50, 3)
Q(T, "Men-women-children", B,
  "One man does as much work as two boys. 6 men and 8 boys can finish a job in 10 days. How long will 4 men and 4 "
  "boys take to finish it?",
  "16⅔ days", ["20 days", "12½ days", "15 days"],
  "Convert everyone into one unit (boy-units)",
  "6 men + 8 boys = 12 + 8 = 20 boy-units, so the job is 20 × 10 = 200 boy-days. 4 men + 4 boys = 12 boy-units, "
  "so they need 200 ÷ 12 = 16⅔ days.",
  ["1 man = 2 boys", "6 men + 8 boys = 20 boys; work = 200 boy-days", "4 men + 4 boys = 12 boys",
   "Days = 200 ÷ 12 = 16⅔"],
  why="20 days counts 4 men + 4 boys as 10 boy-units; 12½ days counts them as 16.", secs=45)

a_days = F(8, F(40, 100))
b_days = F(18, F(60, 100))
tog = 1 / (1 / a_days + 1 / b_days)
assert (a_days, b_days, tog) == (20, 30, 12)
Q(T, "Work efficiency", I,
  "A completes 40% of a job in 8 days and then leaves. B completes the remaining job in 18 days. In how many days "
  "would A and B together have finished the whole job?",
  "12 days", ["25 days", "13 days", "10 days"],
  "Find each person's full-job time from the part done",
  "A does 40% in 8 days, so A alone needs 20 days. B does 60% in 18 days, so B alone needs 30 days. Together: "
  "1/20 + 1/30 = 1/12, i.e. 12 days.",
  ["A: 40% in 8 days ⇒ 100% in 20 days", "B: 60% in 18 days ⇒ 100% in 30 days",
   "Together: 1/20 + 1/30 = 5/60 = 1/12", "12 days"],
  why="25 days averages 20 and 30; 13 days averages the given 8 and 18 days.", secs=55)

sol = [(m, w) for m in range(1, 500) for w in range(1, 500) if 7 * (3 * m + 4 * w) == 3780 and
       8 * (11 * m + 13 * w) == 15040]
assert sol == [(100, 60)] and F(8800, 5 * 100 + 10 * 60) == 8
Q(T, "Work and wages", I,
  "3 men and 4 women together earn ₹3,780 in 7 days, while 11 men and 13 women together earn ₹15,040 in 8 days. "
  "In how many days will 5 men and 10 women together earn ₹8,800?",
  "8 days", ["6 days", "10 days", "11 days"],
  "Form two equations in the daily wages of a man (m) and a woman (w)",
  "Daily: 3m + 4w = 540 and 11m + 13w = 1,880. Multiplying the first by 13 and the second by 4 and subtracting "
  "gives 5m = 500, so m = ₹100 and w = ₹60. 5 men and 10 women earn 500 + 600 = ₹1,100 a day, so ₹8,800 takes "
  "8 days.",
  ["3m + 4w = 3,780 ÷ 7 = 540", "11m + 13w = 15,040 ÷ 8 = 1,880", "39m + 52w = 7,020 and 44m + 52w = 7,520",
   "5m = 500 ⇒ m = 100, w = 60", "5m + 10w = 1,100 per day ⇒ 8,800 ÷ 1,100 = 8 days"],
  why="6, 10 and 11 days would need daily earnings of about ₹1,467, ₹880 and ₹800; the wages found give ₹1,100 a "
      "day.", secs=90)

b_ = F(1)
a_eff, c_eff = F(3, 2) * b_, F(1, 2) * b_
work = (a_eff + b_ + c_eff) * 16
assert work == 48 and work / (a_eff + c_eff) == 24 and work / a_eff == 32
Q(T, "Work efficiency", A,
  "A is 50% more efficient than B, and C is half as efficient as B. Working together, A, B and C finish a project "
  "in 16 days. How many days would A and C together take?",
  "24 days", ["32 days", "20 days", "18 days"],
  "Efficiency ratios give a common unit of work",
  "Let B do 2 units a day. Then A does 3 and C does 1. Together they do 6 units a day, so the project is "
  "6 × 16 = 96 units. A and C do 4 units a day, so they need 96 ÷ 4 = 24 days.",
  ["A : B : C = 3 : 2 : 1", "Work = (3 + 2 + 1) × 16 = 96 units", "A + C = 4 units/day", "96 ÷ 4 = 24 days"],
  why="32 days is A's time alone; 20 days drops C's contribution from the total but not from the pair.", secs=80)

# ================================================================ Pipes and Cisterns (B1 I1 A1)
T = "Pipes and Cisterns"
t = 1 / (F(1, 15) + F(1, 20))
assert t == F(60, 7)
Q(T, "Inlet and outlet", B,
  "Pipe A can fill a tank in 15 minutes and pipe B in 20 minutes. If both are opened together on the empty tank, "
  "how long will they take to fill it?",
  "8 4/7 minutes", ["17½ minutes", "35 minutes", "5 minutes"],
  "Add the filling rates (fractions of the tank per minute)",
  "Together they fill 1/15 + 1/20 = (4 + 3)/60 = 7/60 of the tank per minute, so they take 60/7 = 8 4/7 minutes.",
  ["A: 1/15 per minute; B: 1/20 per minute", "Together: 7/60 per minute", "Time = 60/7 = 8 4/7 minutes"],
  short="Time = (15 × 20) ÷ (15 + 20) = 300 ÷ 35 = 8 4/7 minutes.",
  why="17½ minutes averages the two times; 35 minutes adds them.", secs=35)

leak = 1 / (F(1, 12) + F(1, 15) - F(1, 8))
assert leak == 40
Q(T, "Leak problems", I,
  "Two pipes can fill a tank in 12 hours and 15 hours. Because of a leak, the two pipes together take 8 hours to "
  "fill it. In how many hours can the leak alone empty the full tank?",
  "40 hours", ["24 hours", "60 hours", "20 hours"],
  "Leak rate = (rate without leak) − (rate with leak)",
  "Without the leak the pipes fill 1/12 + 1/15 = 9/60 = 3/20 of the tank per hour. With the leak they fill 1/8. "
  "So the leak empties 3/20 − 1/8 = 1/40 per hour, i.e. the full tank in 40 hours.",
  ["Pipes: 1/12 + 1/15 = 3/20 per hour", "With leak: 1/8 per hour", "Leak = 3/20 − 1/8 = 6/40 − 5/40 = 1/40",
   "Leak empties the tank in 40 hours"],
  why="24 hours compares the 8-hour rate with the first pipe alone (1/8 − 1/12 = 1/24); the leak works against both "
      "pipes together, so its rate is 3/20 − 1/8.", secs=60)
assert F(1, 8) - F(1, 12) == F(1, 24)

ts = [t for t in range(0, 19) if F(18, 24) + F(t, 32) == 1]
assert ts == [8]
Q(T, "Inlet and outlet", A,
  "Pipes A and B can fill a tank in 24 minutes and 32 minutes. Both are opened together on the empty tank. After "
  "how many minutes should B be closed so that the tank is full exactly 18 minutes after the start?",
  "8 minutes", ["6 minutes", "10 minutes", "12 minutes"],
  "Each pipe's contribution = its rate × the time it stays open",
  "A runs for all 18 minutes and fills 18/24 = 3/4 of the tank. B must fill the remaining 1/4, which takes "
  "32 × 1/4 = 8 minutes. So B is closed after 8 minutes.",
  ["A's share = 18 × 1/24 = 3/4", "B's share = 1 − 3/4 = 1/4", "B's time = 1/4 ÷ 1/32 = 8 minutes"],
  why="6 and 10 minutes leave the tank at 15/16 full or overflowing by 1/16 at 18 minutes.", secs=70)

# ================================================================ Speed, Time and Distance (B2 I2 A2)
T = "Speed, Time and Distance"
avg = F(150 + 200, F(150, 50) + F(200, 40))
assert avg == F(175, 4) and near(F(2 * 50 * 40, 90), 44.444, 1e-3)
Q(T, "Average speed", B,
  "A car covers 150 km at 50 km/h and then 200 km at 40 km/h. What is its average speed for the whole journey?",
  "43.75 km/h", ["45 km/h", "44.44 km/h", "42.5 km/h"],
  "Average speed = total distance ÷ total time (not the average of the speeds)",
  "Time for the first part = 150 ÷ 50 = 3 hours; for the second part = 200 ÷ 40 = 5 hours. Average speed = "
  "350 ÷ 8 = 43.75 km/h.",
  ["t₁ = 150 ÷ 50 = 3 h", "t₂ = 200 ÷ 40 = 5 h", "Average = (150 + 200) ÷ (3 + 5) = 43.75 km/h"],
  why="45 km/h averages the two speeds; 44.44 km/h uses the equal-distance formula 2ab/(a + b), but the distances "
      "are not equal.", secs=40)

gap = (F(15, 2) - 5) * F(16, 5)
assert gap == 8 and (F(15, 2) + 5) * F(16, 5) == 40
Q(T, "Relative speed", B,
  "Two friends start walking from the same point in the same direction at 5 km/h and 7.5 km/h. How far apart will "
  "they be after 3 hours 12 minutes?",
  "8 km", ["40 km", "7.5 km", "10 km"],
  "Same direction: relative speed = difference of speeds",
  "The gap grows at 7.5 − 5 = 2.5 km/h. 3 hours 12 minutes = 3.2 hours, so the gap is 2.5 × 3.2 = 8 km.",
  ["Relative speed = 2.5 km/h", "3 h 12 min = 3 + 12/60 = 3.2 h", "Distance apart = 2.5 × 3.2 = 8 km"],
  why="40 km adds the speeds (that is for opposite directions); 7.5 km uses only 3 hours.", secs=35)

xs_ = [x for x in range(1, 200) if F(2 * 48 * x, 48 + x) == F(576, 10)]
assert xs_ == [72] and 2 * F(576, 10) - 48 == F(672, 10)
Q(T, "Average speed", I,
  "A bus goes from town P to town Q at 48 km/h and returns along the same route. Its average speed for the round "
  "trip is 57.6 km/h. What was its speed on the return journey?",
  "72 km/h", ["67.2 km/h", "64 km/h", "80 km/h"],
  "For equal distances, average speed = 2ab ÷ (a + b)",
  "2 × 48 × x ÷ (48 + x) = 57.6 gives 96x = 57.6 × 48 + 57.6x, so 38.4x = 2,764.8 and x = 72 km/h.",
  ["2 × 48x ÷ (48 + x) = 57.6", "96x = 2,764.8 + 57.6x", "38.4x = 2,764.8 ⇒ x = 72"],
  why="67.2 km/h assumes the average is the mean of the two speeds (2 × 57.6 − 48).", secs=55)

t_meet = F(72, 5 + 7)
assert t_meet == 6 and 15 * t_meet == 90
Q(T, "Relative speed", I,
  "Two people start at the same time from towns 72 km apart and walk towards each other at 5 km/h and 7 km/h. A dog "
  "starts with the first person, runs to the second at 15 km/h, turns back at once, and keeps running between them "
  "until they meet. What total distance does the dog run?",
  "90 km", ["72 km", "60 km", "108 km"],
  "The dog runs for exactly as long as the two people take to meet",
  "The people close the gap at 5 + 7 = 12 km/h, so they meet after 72 ÷ 12 = 6 hours. The dog runs at 15 km/h for "
  "those 6 hours: 15 × 6 = 90 km.",
  ["Relative speed of the people = 12 km/h", "Time to meet = 72 ÷ 12 = 6 h", "Dog's distance = 15 × 6 = 90 km"],
  short="Do not trace each leg of the dog's run; only the total time matters.",
  why="72 km is the distance between the towns; 60 km uses the dog's speed relative to one walker (15 − 5) × 6.",
  secs=55)

t_ = next(t for t in range(1, 100000) if (5 * t) % 600 == 0 and (7 * t) % 600 == 0)
first_any = next(t for t in range(1, 100000) if (7 * t - 5 * t) % 600 == 0)
assert t_ == 600 and first_any == 300
Q(T, "Meeting and overtaking", A,
  "Two runners start together from the same point on a 600 m circular track and run in the same direction at "
  "5 m/s and 7 m/s. After how long will they first be together again at the starting point?",
  "10 minutes", ["5 minutes", "2 minutes", "20 minutes"],
  "Meeting at the start: LCM of the lap times; meeting anywhere: track length ÷ relative speed",
  "Lap times are 600 ÷ 5 = 120 s and 600 ÷ 7 = 600/7 s. They are both at the start when each has completed a "
  "whole number of laps: after 600 s the first has done 5 laps and the second 7 laps, and no earlier time works. "
  "600 s = 10 minutes.",
  ["Lap times: 120 s and 600/7 s", "LCM(120, 600/7) = LCM(840, 600)/7 = 4200/7 = 600 s",
   "Check: in 600 s, 5 laps and 7 laps", "600 s = 10 minutes"],
  why="5 minutes is when they first meet anywhere on the track (600 ÷ (7 − 5) = 300 s), which is not the start "
      "point; 2 minutes is only the first runner's lap time.", secs=90)

sp = [(a, b) for a in range(1, 200) for b in range(1, a) if (a + b) * F(5, 2) == 300 and (a - b) * 15 == 300]
assert sp == [(70, 50)]
Q(T, "Relative speed", A,
  "Two cars start at the same time from points A and B, 300 km apart. If they drive towards each other they meet "
  "in 2.5 hours; if they drive in the same direction, the faster one catches the slower one in 15 hours. What is the "
  "speed of the faster car?",
  "70 km/h", ["50 km/h", "60 km/h", "80 km/h"],
  "Towards each other: sum of speeds; same direction: difference of speeds",
  "Sum of speeds = 300 ÷ 2.5 = 120 km/h and difference = 300 ÷ 15 = 20 km/h. The faster car's speed is "
  "(120 + 20) ÷ 2 = 70 km/h.",
  ["a + b = 300 ÷ 2.5 = 120", "a − b = 300 ÷ 15 = 20", "a = (120 + 20) ÷ 2 = 70 km/h", "b = 50 km/h"],
  why="50 km/h is the slower car; 60 km/h is half the sum of the speeds.", secs=70)

# ================================================================ Boats and Streams (B1 I2 A1)
T = "Boats and Streams"
dd = (18 + 4) * F(5, 2)
assert dd == 55 and (18 - 4) * F(5, 2) == 35 and 18 * F(5, 2) == 45
Q(T, "Upstream and downstream", B,
  "A boat's speed in still water is 18 km/h and the stream flows at 4 km/h. How far will the boat travel downstream "
  "in 2 hours 30 minutes?",
  "55 km", ["35 km", "45 km", "50 km"],
  "Downstream speed = boat speed + stream speed",
  "Downstream speed = 18 + 4 = 22 km/h. In 2.5 hours the boat covers 22 × 2.5 = 55 km.",
  ["Downstream speed = 22 km/h", "2 h 30 min = 2.5 h", "Distance = 22 × 2.5 = 55 km"],
  why="35 km uses the upstream speed (14 km/h); 45 km ignores the stream.", secs=30)

ks = [F(k, 4) for k in range(1, 100) if F(48, 4 * F(k, 4)) + F(48, 3 * F(k, 4)) == 14]
assert ks == [2]
dn, up = 4 * ks[0], 3 * ks[0]
stream = (dn - up) / 2
assert (dn, up, stream) == (8, 6, 1)
Q(T, "Speed of stream", I,
  "A man rows to a place 48 km away and back in 14 hours. He finds that he can row 4 km downstream in the same time "
  "as 3 km upstream. What is the speed of the stream?",
  "1 km/h", ["2 km/h", "7 km/h", "1.5 km/h"],
  "Equal times for 4 km and 3 km mean downstream : upstream speed = 4 : 3",
  "Let the speeds be 4k and 3k. Then 48/(4k) + 48/(3k) = 12/k + 16/k = 28/k = 14, so k = 2. Downstream = 8 km/h, "
  "upstream = 6 km/h, and the stream's speed = (8 − 6) ÷ 2 = 1 km/h.",
  ["Downstream : upstream = 4 : 3 ⇒ 4k and 3k", "48/(4k) + 48/(3k) = 28/k = 14 ⇒ k = 2",
   "Downstream 8 km/h, upstream 6 km/h", "Stream = (8 − 6) ÷ 2 = 1 km/h"],
  why="2 km/h forgets to halve the difference; 7 km/h is the man's rowing speed in still water.", secs=70)

ss = [s for s in range(1, 9) if (9 + s) == 2 * (9 - s)]
assert ss == [3]
Q(T, "Speed of stream", I,
  "A boat takes twice as long to go a certain distance upstream as to go the same distance downstream. If its speed "
  "in still water is 9 km/h, what is the speed of the stream?",
  "3 km/h", ["4.5 km/h", "6 km/h", "2 km/h"],
  "Same distance: time is inversely proportional to speed",
  "Twice the time upstream means the downstream speed is twice the upstream speed: 9 + s = 2(9 − s), so 3s = 9 and "
  "s = 3 km/h.",
  ["Downstream speed = 2 × upstream speed", "9 + s = 18 − 2s", "3s = 9 ⇒ s = 3 km/h",
   "Check: downstream 12, upstream 6"],
  why="4.5 km/h halves the boat's speed; 6 km/h is the upstream speed.", secs=50)

sol = [(u, d) for u in range(1, 30) for d in range(u + 1, 40) if F(30, u) + F(44, d) == 10 and F(40, u) + F(55, d) == 13]
assert sol == [(5, 11)] and F(5 + 11, 2) == 8
Q(T, "Upstream and downstream", A,
  "A boat goes 30 km upstream and 44 km downstream in 10 hours. It also goes 40 km upstream and 55 km downstream in "
  "13 hours. What is the speed of the boat in still water?",
  "8 km/h", ["11 km/h", "5 km/h", "3 km/h"],
  "Treat 1/upstream speed and 1/downstream speed as the unknowns",
  "Let a = 1/u and b = 1/d. Then 30a + 44b = 10 and 40a + 55b = 13. Multiplying the first by 4 and the second by 3: "
  "120a + 176b = 40 and 120a + 165b = 39, so 11b = 1, b = 1/11 and d = 11 km/h. Then 30a = 10 − 4 = 6, a = 1/5 and "
  "u = 5 km/h. Boat speed = (11 + 5) ÷ 2 = 8 km/h.",
  ["30/u + 44/d = 10; 40/u + 55/d = 13", "Eliminate 1/u: 11/d = 1 ⇒ d = 11", "30/u = 10 − 4 = 6 ⇒ u = 5",
   "Boat = (11 + 5) ÷ 2 = 8 km/h", "Stream = (11 − 5) ÷ 2 = 3 km/h"],
  why="11 km/h and 5 km/h are the downstream and upstream speeds; 3 km/h is the stream.", secs=100)

# ================================================================ Problems on Trains (B1 I1 A1)
T = "Problems on Trains"
v = F(72 * 5, 18)
train = v * 18
plat = v * 30 - train
assert v == 20 and train == 360 and plat == 240
Q(T, "Crossing a pole or platform", B,
  "A train running at 72 km/h crosses a platform in 30 seconds and a man standing on the platform in 18 seconds. "
  "What is the length of the platform?",
  "240 m", ["360 m", "600 m", "216 m"],
  "Crossing a man covers the train's length; crossing a platform covers train + platform",
  "72 km/h = 20 m/s. The train's length = 20 × 18 = 360 m, and train + platform = 20 × 30 = 600 m. So the platform "
  "is 600 − 360 = 240 m.",
  ["72 × 5/18 = 20 m/s", "Train = 20 × 18 = 360 m", "Train + platform = 20 × 30 = 600 m", "Platform = 240 m"],
  short="The extra 12 seconds are spent on the platform alone: 20 × 12 = 240 m.",
  why="360 m is the train's length; 600 m is train + platform.", secs=40)

L = (46 - 36) * F(5, 18) * 36 / 2
assert L == 50
Q(T, "Trains crossing each other", I,
  "Two trains of equal length run on parallel tracks in the same direction at 46 km/h and 36 km/h. The faster train "
  "passes the slower one completely in 36 seconds. What is the length of each train?",
  "50 m", ["100 m", "25 m", "82 m"],
  "Overtaking: relative speed = difference; distance = sum of the two lengths",
  "Relative speed = 10 km/h = 25/9 m/s. In 36 seconds the faster train gains 25/9 × 36 = 100 m, which equals the "
  "two lengths together. Each train is 50 m long.",
  ["Relative speed = 46 − 36 = 10 km/h = 10 × 5/18 = 25/9 m/s", "Distance = 25/9 × 36 = 100 m = 2L", "L = 50 m"],
  why="100 m is the combined length; 82 m uses the sum of speeds (82 km/h) as a distance.", secs=55)

vs = [vv for vv in range(6, 200) if (vv - 3) * 10 == (vv + 5) * 9]
assert vs == [75]
L = (75 - 3) * F(5, 18) * 10
assert L == 200
Q(T, "Crossing a pole or platform", A,
  "A train passes a man walking at 3 km/h in the same direction in 10 seconds, and passes another man walking at "
  "5 km/h in the opposite direction in 9 seconds. What is the length of the train?",
  "200 m", ["180 m", "225 m", "250 m"],
  "Same direction: subtract the man's speed; opposite direction: add it. The train's length is the same both times",
  "Let the train's speed be v km/h. (v − 3) × 10 = (v + 5) × 9 (both in km/h × seconds), so v = 75 km/h. The length "
  "is (75 − 3) × 5/18 × 10 = 20 × 10 = 200 m.",
  ["(v − 3) × 10 = (v + 5) × 9", "10v − 30 = 9v + 45 ⇒ v = 75 km/h", "Relative speed with first man = 72 km/h = "
   "20 m/s", "Length = 20 × 10 = 200 m", "Check: (75 + 5) × 5/18 × 9 = 200 m"],
  why="180 m, 225 m and 250 m fail the check: with 10 s for the first man they give train speeds of 67.8, 84 and "
      "93 km/h, which do not give 9 s for the second man.", secs=100)
for L_, v_ in ((180, F(678, 10)), (225, 84), (250, 93)):
    assert F(L_, 10) * F(18, 5) + 3 == v_ and F(L_) / ((v_ + 5) * F(5, 18)) != 9

# ================================================================ Mensuration (B2 I2 A2)
T = "Mensuration"
side = math.isqrt(12 ** 2 + 9 ** 2)
assert side == 15 and 4 * side == 60 and F(24 * 18, 2) == 216
Q(T, "2D areas and perimeters", B,
  "The diagonals of a rhombus are 24 cm and 18 cm. What is its perimeter?",
  "60 cm", ["84 cm", "216 cm", "42 cm"],
  "The diagonals of a rhombus bisect each other at right angles",
  "Half-diagonals are 12 cm and 9 cm, so each side = √(12² + 9²) = √225 = 15 cm. Perimeter = 4 × 15 = 60 cm.",
  ["Half-diagonals: 12 cm and 9 cm", "Side = √(144 + 81) = 15 cm", "Perimeter = 4 × 15 = 60 cm"],
  why="84 cm doubles the sum of the diagonals; 216 is the area in cm²; 42 cm adds the diagonals.", secs=40)

a_ = math.isqrt(486 // 6)
assert 6 * a_ * a_ == 486 and a_ ** 3 == 729
Q(T, "3D volume and surface area", B,
  "The total surface area of a cube is 486 cm². What is its volume?",
  "729 cm³", ["81 cm³", "1,331 cm³", "512 cm³"],
  "Total surface area of a cube = 6a²; volume = a³",
  "6a² = 486 gives a² = 81 and a = 9 cm. Volume = 9³ = 729 cm³.",
  ["a² = 486 ÷ 6 = 81", "a = 9 cm", "Volume = 9³ = 729 cm³"],
  why="81 is the area of one face; 1,331 and 512 are the cubes of 11 and 8.", secs=35)

l_ = math.isqrt(7 ** 2 + 24 ** 2)
csa = F(22, 7) * 7 * l_
assert l_ == 25 and csa == 550 and F(22, 7) * 7 * 24 == 528 and csa + F(22, 7) * 49 == 704
Q(T, "Cylinder, cone and sphere", I,
  "A cone has a base radius of 7 cm and a height of 24 cm. What is its curved surface area? (Use π = 22/7.)",
  "550 cm²", ["528 cm²", "704 cm²", "1,232 cm²"],
  "Curved surface area of a cone = πrl, where l = √(r² + h²) is the slant height",
  "Slant height = √(7² + 24²) = √625 = 25 cm. CSA = 22/7 × 7 × 25 = 550 cm².",
  ["l = √(49 + 576) = 25 cm", "CSA = πrl = 22/7 × 7 × 25 = 550 cm²"],
  why="528 cm² uses the height instead of the slant height; 704 cm² is the total surface area (adds the base); "
      "1,232 cm³ is the volume.", secs=50)
assert F(1, 3) * F(22, 7) * 49 * 24 == 1232

chg = (F(120, 100) * F(80, 100) - 1) * 100
assert chg == -4
Q(T, "2D areas and perimeters", I,
  "The length of a rectangle is increased by 20% and its breadth is decreased by 20%. What is the effect on its "
  "area?",
  "4% decrease", ["No change", "4% increase", "2% decrease"],
  "New area = (1 + a)(1 − b) × old area",
  "New area = 1.2 × 0.8 = 0.96 times the old area, i.e. a 4% decrease.",
  ["Area factor = 1.20 × 0.80 = 0.96", "Change = 0.96 − 1 = −0.04 = 4% decrease"],
  short="Net change = a − b − ab/100 = 20 − 20 − 400/100 = −4%.",
  why="'No change' assumes +20% and −20% cancel; they do not, because the 20% decrease applies to a larger base.",
  secs=40)

vol = F(44 * 21 * 5, 100)
h = vol / (F(22, 7) * F(7, 2) ** 2)
assert vol == F(462, 10) and h == F(12, 10) and F(44 * 21 * 50, 100) / (F(22, 7) * F(7, 2) ** 2) == 12
assert vol / (F(22, 7) * 49) == F(3, 10)
Q(T, "Cylinder, cone and sphere", A,
  "Rain falls on a flat rectangular roof 44 m long and 21 m wide to a depth of 5 cm. All the water flows into an "
  "empty cylindrical tank with a base radius of 3.5 m. How high will the water rise in the tank? (Use π = 22/7.)",
  "1.2 m", ["12 m", "0.3 m", "2.4 m"],
  "Volume of rain on the roof = volume of water in the tank",
  "Rain volume = 44 × 21 × 0.05 = 46.2 m³. Tank base area = 22/7 × 3.5² = 38.5 m². Height = 46.2 ÷ 38.5 = 1.2 m.",
  ["5 cm = 0.05 m", "Volume = 44 × 21 × 0.05 = 46.2 m³", "Base area = 22/7 × 3.5 × 3.5 = 38.5 m²",
   "h = 46.2 ÷ 38.5 = 1.2 m"],
  why="12 m converts 5 cm to 0.5 m; 0.3 m uses 7 m (the diameter) as the radius; 2.4 m doubles the answer.",
  secs=90)

small = F(1, 2) ** 3
assert small == F(1, 8) and ratio(small, 1 - small) == "1 : 7"
Q(T, "Cylinder, cone and sphere", A,
  "A right circular cone is cut by a plane parallel to its base through the midpoint of its height. What is the "
  "ratio of the volume of the small cone cut off to the volume of the remaining frustum?",
  "1 : 7", ["1 : 8", "1 : 3", "1 : 1"],
  "Similar solids: volumes scale as the cube of the linear ratio",
  "The small cone is similar to the original with half its height and half its radius, so its volume is "
  "(1/2)³ = 1/8 of the original. The frustum is the remaining 7/8, giving 1 : 7.",
  ["Linear ratio small : original = 1 : 2", "Volume ratio = 1³ : 2³ = 1 : 8", "Frustum = 8 − 1 = 7 parts",
   "Small cone : frustum = 1 : 7"],
  why="1 : 8 compares the small cone with the whole cone, not with the frustum; 1 : 3 uses the area ratio 1 : 4.",
  secs=70)

# ================================================================ Probability (B1 I4 A3)
T = "Probability"
outs = list(itertools.product("HT", repeat=3))
p = F(sum(1 for o in outs if o.count("H") >= 2), len(outs))
assert p == F(1, 2) and F(sum(1 for o in outs if o.count("H") == 2), 8) == F(3, 8)
Q(T, "Coins and dice", B,
  "Three fair coins are tossed together. What is the probability of getting at least two heads?",
  "1/2", ["3/8", "7/8", "1/4"],
  "List the 8 equally likely outcomes and count the favourable ones",
  "Of the 8 outcomes, three have exactly two heads (HHT, HTH, THH) and one has three heads (HHH). So 4 of the 8 are "
  "favourable: 4/8 = 1/2.",
  ["Total outcomes = 2³ = 8", "Exactly 2 heads: 3 outcomes", "3 heads: 1 outcome", "P = 4/8 = 1/2"],
  why="3/8 counts exactly two heads only; 7/8 is the probability of at least one head.", secs=35, by=BRUTE)

deck = [(r, s) for r in range(1, 14) for s in "SHDC"]
fav = [c for c in deck if c[0] >= 11 or c[1] == "S"]
assert F(len(fav), 52) == F(11, 26) and F(25, 52) != F(11, 26)
Q(T, "Cards", I,
  "One card is drawn at random from a well-shuffled pack of 52 cards. What is the probability that it is a face "
  "card or a spade?",
  "11/26", ["25/52", "3/13", "1/4"],
  "P(A or B) = P(A) + P(B) − P(A and B)",
  "There are 12 face cards and 13 spades, but 3 cards (the jack, queen and king of spades) are in both groups. "
  "Favourable cards = 12 + 13 − 3 = 22, so P = 22/52 = 11/26.",
  ["Face cards = 12; spades = 13", "Both = 3 (J, Q, K of spades)", "Favourable = 12 + 13 − 3 = 22",
   "P = 22/52 = 11/26"],
  why="25/52 counts the three spade face cards twice; 3/13 counts face cards only; 1/4 counts spades only.", secs=50,
  by=BRUTE)

bag = ["R"] * 4 + ["G"] * 5 + ["Y"] * 6
pairs = list(itertools.combinations(range(15), 2))
p = F(sum(1 for i, j in pairs if bag[i] == bag[j]), len(pairs))
assert p == F(31, 105) and F(16 + 25 + 36, 225) == F(77, 225)
Q(T, "Balls from bags", I,
  "A bag contains 4 red, 5 green and 6 yellow balls. Two balls are drawn at random together. What is the "
  "probability that both are of the same colour?",
  "31/105", ["77/225", "1/3", "74/105"],
  "Count selections: ⁿC₂ for each colour over ¹⁵C₂ in all",
  "Total ways = ¹⁵C₂ = 105. Same colour: ⁴C₂ + ⁵C₂ + ⁶C₂ = 6 + 10 + 15 = 31. P = 31/105.",
  ["¹⁵C₂ = 105", "Both red: ⁴C₂ = 6; both green: ⁵C₂ = 10; both yellow: ⁶C₂ = 15", "Favourable = 31",
   "P = 31/105"],
  why="77/225 draws with replacement; 74/105 is the probability that the colours differ.", secs=60, by=BRUTE)

dice = list(itertools.product(range(1, 7), repeat=2))
p = F(sum(1 for a, b in dice if abs(a - b) <= 1), 36)
assert p == F(4, 9) and F(sum(1 for a, b in dice if abs(a - b) == 1), 36) == F(5, 18)
Q(T, "Coins and dice", I,
  "Two fair dice are rolled. What is the probability that the two numbers differ by at most 1?",
  "4/9", ["5/18", "1/6", "11/36"],
  "'At most 1' means a difference of 0 or 1",
  "Difference 0: 6 outcomes (1-1, …, 6-6). Difference 1: 5 pairs in each order, 10 outcomes. Favourable = 16 of "
  "36, so P = 4/9.",
  ["Difference 0: 6 outcomes", "Difference 1: (1,2), (2,3), …, (5,6) and reverses = 10 outcomes",
   "Favourable = 16; P = 16/36 = 4/9"],
  why="5/18 counts only a difference of exactly 1; 1/6 counts only equal numbers; 11/36 counts each "
      "difference-1 pair in one order only.", secs=55, by=BRUTE)

seqs = list(itertools.product("HT", repeat=4))
p = F(sum(1 for s_ in seqs if "HH" not in "".join(s_)), 16)
assert p == F(1, 2)
Q(T, "Coins and dice", I,
  "A fair coin is tossed four times. What is the probability that no two consecutive tosses are both heads?",
  "1/2", ["5/16", "3/8", "7/16"],
  "Count sequences directly (or build them toss by toss)",
  "Count the sequences with no 'HH': 0 heads: 1 (TTTT); 1 head: 4; 2 non-adjacent heads: HTHT, HTTH, THTH = 3. "
  "3 or 4 heads always have two adjacent heads. Total = 8 of 16, so P = 1/2.",
  ["Total sequences = 2⁴ = 16", "No heads: 1", "One head: 4", "Two heads, not adjacent: HTHT, HTTH, THTH = 3",
   "Favourable = 8 ⇒ P = 8/16 = 1/2"],
  why="5/16 counts only sequences with at most one head; 3/8 counts only those with exactly two heads (6/16).",
  secs=70, by=BRUTE)

hands = list(itertools.combinations(range(52), 3))
p = F(sum(1 for h_ in hands if len({deck[i][1] for i in h_}) == 3), len(hands))
assert len(hands) == 22100 and p == F(169, 425) and F(2197, 22100) != p
Q(T, "Cards", A,
  "Three cards are drawn together at random from a well-shuffled pack of 52 cards. What is the probability that "
  "they are all from different suits?",
  "169/425", ["3/8", "2197/22100", "4/17"],
  "Choose the 3 suits, then one card from each; divide by ⁵²C₃",
  "Ways = ⁴C₃ × 13 × 13 × 13 = 4 × 2,197 = 8,788. Total = ⁵²C₃ = 22,100. P = 8,788/22,100 = 169/425.",
  ["⁵²C₃ = 22,100", "Choose 3 suits: ⁴C₃ = 4", "One card from each: 13³ = 2,197", "Favourable = 8,788",
   "P = 8,788 ÷ 22,100 = 169/425"],
  short="Draw one by one: 1 × 39/51 × 26/50 = 169/425.",
  why="3/8 assumes the cards are drawn with replacement (1 × 3/4 × 2/4); 2197/22100 forgets to choose which 3 of "
      "the 4 suits appear.", secs=100, by=BRUTE)

world = [("A", c) for c in "WWWBB"] + [("B", c) for c in "WWBBBB"]
num = F(1, 2) * F(3, 5)
den = num + F(1, 2) * F(2, 6)
assert num / den == F(9, 14) and den == F(7, 15)
cnt_wA = sum(F(1, 2) * F(1, 5) for b_, c_ in world if b_ == "A" and c_ == "W")
cnt_w = cnt_wA + sum(F(1, 2) * F(1, 6) for b_, c_ in world if b_ == "B" and c_ == "W")
assert cnt_wA / cnt_w == F(9, 14)
Q(T, "Balls from bags", A,
  "Bag A has 3 white and 2 black balls; bag B has 2 white and 4 black balls. One bag is chosen at random and a ball "
  "drawn from it is white. What is the probability that it came from bag A?",
  "9/14", ["3/5", "7/15", "1/2"],
  "Conditional probability (Bayes): P(A | white) = P(A and white) ÷ P(white)",
  "P(A and white) = ½ × 3/5 = 3/10. P(B and white) = ½ × 2/6 = 1/6. P(white) = 3/10 + 1/6 = 7/15. So "
  "P(A | white) = (3/10) ÷ (7/15) = 9/14.",
  ["P(A and W) = 1/2 × 3/5 = 3/10", "P(B and W) = 1/2 × 1/3 = 1/6", "P(W) = 3/10 + 1/6 = 14/30 = 7/15",
   "P(A | W) = (3/10) ÷ (7/15) = 45/70 = 9/14"],
  why="3/5 is P(white | A), the reverse condition; 7/15 is the overall probability of drawing white; 1/2 ignores the "
      "evidence that the ball is white.", secs=100, by=BRUTE)

rolls = list(itertools.product(range(1, 7), repeat=3))
p = F(sum(1 for r_ in rolls if sum(r_) == 10), 216)
assert p == F(1, 8) and F(sum(1 for r_ in rolls if sum(r_) == 9), 216) == F(25, 216)
Q(T, "Coins and dice", A,
  "Three fair dice are rolled together. What is the probability that the total is 10?",
  "1/8", ["25/216", "1/6", "5/36"],
  "Count ordered triples (a, b, c) with a + b + c = 10, each from 1 to 6",
  "Group by the first die a: the other two must add to 10 − a. a = 1: 4 ways; a = 2: 5; a = 3: 6; a = 4: 5; a = 5: "
  "4; a = 6: 3. Total = 27 of the 216 outcomes, so P = 27/216 = 1/8.",
  ["Total outcomes = 6³ = 216", "a = 1 needs b + c = 9: (3,6), (4,5), (5,4), (6,3) → 4 ways",
   "a = 2 needs b + c = 8: 5 ways; a = 3 needs 7: 6 ways; a = 4 needs 6: 5 ways",
   "a = 5 needs 5: 4 ways; a = 6 needs 4: 3 ways", "Total = 4 + 5 + 6 + 5 + 4 + 3 = 27; P = 27/216 = 1/8"],
  why="25/216 is the probability of a total of 9, which looks similar but has fewer combinations.", secs=90,
  by=BRUTE)
assert [sum(1 for b_ in range(1, 7) for c_ in range(1, 7) if a_ + b_ + c_ == 10) for a_ in range(1, 7)] == \
    [4, 5, 6, 5, 4, 3]

# ================================================================ Permutation and Combination (B1 I2 A1)
T = "Permutation and Combination"
cnt = len(list(itertools.permutations(range(1, 7), 4)))
assert cnt == 360 and 6 ** 4 == 1296 and math.comb(6, 4) == 15
Q(T, "Arrangements", B,
  "How many 4-digit numbers can be formed using the digits 1, 2, 3, 4, 5 and 6 if no digit is repeated?",
  "360", ["1,296", "15", "720"],
  "Permutations: ⁿPᵣ = n × (n − 1) × … (r factors)",
  "The thousands digit has 6 choices, the hundreds 5, the tens 4 and the units 3: 6 × 5 × 4 × 3 = 360.",
  ["Choices: 6, 5, 4, 3", "⁶P₄ = 6 × 5 × 4 × 3 = 360"],
  why="1,296 allows repetition (6⁴); 15 counts selections (⁶C₄), not arrangements; 720 is 6!.", secs=35, by=BRUTE)

word = "DEPOSIT"
perms = set(itertools.permutations(word))
ok = [p_ for p_ in perms if all(p_[i] not in "EOI" for i in (1, 3, 5))]
assert len(perms) == 5040 and len(ok) == 576
tog = [p_ for p_ in perms if max(i for i, ch in enumerate(p_) if ch in "EOI") -
       min(i for i, ch in enumerate(p_) if ch in "EOI") == 2]
assert len(tog) == 720
Q(T, "Word arrangements", I,
  "In how many ways can the letters of the word DEPOSIT be arranged so that the vowels occupy only the odd "
  "positions (1st, 3rd, 5th and 7th)?",
  "576", ["720", "144", "5,040"],
  "Place the restricted letters first, then arrange the rest",
  "DEPOSIT has 7 different letters, with vowels E, O, I. The 3 vowels go into 3 of the 4 odd places in ⁴P₃ = 24 "
  "ways. The 4 consonants fill the remaining 4 places in 4! = 24 ways. Total = 24 × 24 = 576.",
  ["Odd positions: 1, 3, 5, 7 (four places)", "Vowels E, O, I into odd places: ⁴P₃ = 24",
   "Consonants D, P, S, T into the other 4 places: 4! = 24", "Total = 576"],
  why="720 is the count with the vowels together; 144 = 3! × 4! forgets that the vowels can choose 3 of 4 odd "
      "places; 5,040 has no restriction.", secs=70, by=BRUTE)

men, women_ = range(7), range(7, 11)
com = [c_ for c_ in itertools.combinations(range(11), 5) if sum(1 for x in c_ if x >= 7) >= 3]
assert len(com) == 91 and math.comb(4, 3) * math.comb(7, 2) == 84 and math.comb(11, 5) == 462
Q(T, "Selections", I,
  "A committee of 5 is to be chosen from 7 men and 4 women so that it includes at least 3 women. In how many ways "
  "can this be done?",
  "91", ["84", "462", "140"],
  "'At least' means adding the separate cases",
  "Case 3 women + 2 men: ⁴C₃ × ⁷C₂ = 4 × 21 = 84. Case 4 women + 1 man: ⁴C₄ × ⁷C₁ = 7. Total = 91.",
  ["3 women, 2 men: 4 × 21 = 84", "4 women, 1 man: 1 × 7 = 7", "Total = 84 + 7 = 91"],
  why="84 counts only exactly 3 women; 462 = ¹¹C₅ has no restriction; 140 = ⁴C₃ × ⁷C₃ is a 6-member committee.",
  secs=60, by=BRUTE)
assert math.comb(4, 3) * math.comb(7, 3) == 140

people = ["B"] * 5 + ["G"] * 5
seats = 10
count = 0
labels = list(range(10))  # 0-4 boys, 5-9 girls
for rest in itertools.permutations(labels[1:]):
    order = (0,) + rest  # fix boy 0 at seat 0 to remove rotations
    if all(not (order[i] >= 5 and order[(i + 1) % seats] >= 5) for i in range(seats)):
        count += 1
assert count == 2880 == math.factorial(4) * math.factorial(5)
Q(T, "Arrangements", A,
  "In how many ways can 5 boys and 5 girls sit around a circular table so that no two girls sit next to each "
  "other? (Arrangements that differ only by a rotation are the same.)",
  "2,880", ["14,400", "28,800", "576"],
  "Seat one group around the circle first ((n − 1)! ways), then place the other group in the gaps",
  "Seat the 5 boys around the table in (5 − 1)! = 24 ways. This leaves 5 gaps between boys, and the 5 girls fill "
  "them in 5! = 120 ways. Total = 24 × 120 = 2,880.",
  ["Boys in a circle: 4! = 24", "5 gaps between boys", "Girls in the gaps: 5! = 120", "Total = 2,880"],
  why="14,400 = 5! × 5! treats the table as a row of fixed seats with the boys first; 28,800 doubles that; "
      "576 = 4! × 4! fixes a girl as well.", secs=100, by=BRUTE)

# ================================================================ Tabular DI (B2 I7 A1): two sets of 5
T = "Tabular DI"
VIL = {"Amarpur": (420, 320, 85, 125), "Bhatpur": (380, 450, 60, 110), "Chandpur": (510, 280, 95, 155),
       "Dharampur": (290, 360, 70, 80), "Eklapur": (450, 400, 90, 140)}
crops = ["Wheat", "Rice", "Mustard", "Pulses"]
sid = stimulus("data_table", "Crop production in five villages of a block, 2025-26",
               "The table shows the production (in tonnes) of four crops in five villages of a development block in "
               "the crop year 2025-26.\n\n" + md_table(["Village", *crops], [[k, *v] for k, v in VIL.items()]),
               {"columns": ["village", *[c.lower() for c in crops]], "rows": [[k, *v] for k, v in VIL.items()]})
tot = {k: sum(v) for k, v in VIL.items()}
col = [sum(v[i] for v in VIL.values()) for i in range(4)]
assert tot == {"Amarpur": 950, "Bhatpur": 1000, "Chandpur": 1040, "Dharampur": 800, "Eklapur": 1080}
assert col == [2050, 1810, 400, 610]
Q(T, "Single table", B, "What is the total production of mustard in the five villages together?",
  "400 tonnes", ["380 tonnes", "420 tonnes", "410 tonnes"],
  "Column total",
  "Add the Mustard column: 85 + 60 + 95 + 70 + 90 = 400 tonnes.",
  ["85 + 60 = 145", "145 + 95 = 240", "240 + 70 = 310", "310 + 90 = 400"], secs=30, stim=sid)

best = max(tot, key=tot.get)
assert best == "Eklapur" and sorted(tot.values())[-2] == 1040
Q(T, "Single table", B, "Which village had the highest total production of the four crops?",
  "Eklapur", ["Chandpur", "Bhatpur", "Amarpur"],
  "Row totals",
  "Row totals: Amarpur 950, Bhatpur 1,000, Chandpur 1,040, Dharampur 800 and Eklapur 1,080 tonnes. Eklapur is "
  "highest.",
  ["Amarpur = 420 + 320 + 85 + 125 = 950", "Bhatpur = 1,000", "Chandpur = 1,040", "Dharampur = 800",
   "Eklapur = 450 + 400 + 90 + 140 = 1,080 (highest)"],
  why="Chandpur has the highest wheat and pulses output, but not the highest total.", secs=45, stim=sid)

pm = F(400 - 320, 320) * 100
assert pm == 25 and F(80, 400) * 100 == 20
Q(T, "Single table", I,
  "Rice production in Eklapur is what percentage more than rice production in Amarpur?",
  "25%", ["20%", "125%", "30%"],
  "Percentage more = difference ÷ base × 100 (base = the village after 'than')",
  "Eklapur 400 and Amarpur 320 tonnes. The difference, 80, is 80 ÷ 320 = 25% of Amarpur's output.",
  ["Difference = 400 − 320 = 80", "80 ÷ 320 × 100 = 25%"],
  why="20% uses Eklapur (400) as the base; 125% is Eklapur's output as a percentage of Amarpur's.", secs=40, stim=sid)

num = VIL["Chandpur"][0] + VIL["Dharampur"][0]
assert num == 800 and ratio(num, col[3]) == "80 : 61" and ratio(800, 620) == "40 : 31"
Q(T, "Single table", I,
  "What is the ratio of the wheat production of Chandpur and Dharampur together to the pulses production of all "
  "five villages together?",
  "80 : 61", ["61 : 80", "40 : 31", "16 : 11"],
  "Ratio of a partial column sum to a full column sum",
  "Wheat of Chandpur and Dharampur = 510 + 290 = 800. Pulses of all five = 125 + 110 + 155 + 80 + 140 = 610. "
  "800 : 610 = 80 : 61.",
  ["Wheat (Chandpur + Dharampur) = 800", "Pulses total = 610", "800 : 610 = 80 : 61"],
  why="61 : 80 is reversed; 40 : 31 uses a pulses total of 620.", secs=50, stim=sid)

pc = F(col[3], col[2]) * 100
assert pc == F(1525, 10) and near(F(col[2], col[3]) * 100, 65.57, 1e-2)
Q(T, "Single table", I,
  "The average pulses production per village is what percentage of the average mustard production per village?",
  "152.5%", ["65.57%", "52.5%", "122%"],
  "Averages over the same number of villages compare like totals",
  "Both averages divide by 5, so the comparison is 610 ÷ 400 × 100 = 152.5%.",
  ["Pulses total = 610 ⇒ average 122", "Mustard total = 400 ⇒ average 80", "122 ÷ 80 × 100 = 152.5%"],
  why="65.57% is mustard as a percentage of pulses; 52.5% is how much more pulses there are; 122 is the pulses "
      "average itself.", secs=50, stim=sid)

HOT = {"Sagar": (120, 75, 3200), "Pine View": (80, 90, 4500), "Lotus": (150, 60, 2800),
       "Heritage": (60, 85, 6000), "Orchid": (90, 70, 3600)}
sid = stimulus("data_table", "Rooms, occupancy and tariffs of five hotels, June 2026",
               "The table gives the number of rooms in five hotels of a hill town, the average occupancy (percentage of "
               "rooms occupied per night) in June 2026, and the average tariff per occupied room per night. June has "
               "30 days.\n\n" +
               md_table(["Hotel", "Rooms", "Average occupancy (%)", "Average tariff (₹ per room-night)"],
                        [[k, r, o, ind(t_)] for k, (r, o, t_) in HOT.items()]),
               {"columns": ["hotel", "rooms", "occupancy_pct", "tariff_rs"], "rows": [[k, *v] for k, v in HOT.items()]})
nights = {k: r * F(o, 100) * 30 for k, (r, o, _) in HOT.items()}
rev = {k: nights[k] * HOT[k][2] for k in HOT}
assert nights == {"Sagar": 2700, "Pine View": 2160, "Lotus": 2700, "Heritage": 1530, "Orchid": 1890}
assert rev == {"Sagar": 8640000, "Pine View": 9720000, "Lotus": 7560000, "Heritage": 9180000, "Orchid": 6804000}
assert 80 * 30 * 4500 == 10800000 and 80 * F(90, 100) * 31 * 4500 == 10044000 and 72 * 4500 == 324000
Q(T, "Table with percentages", I, "What was the room revenue of Pine View in June 2026?",
  "₹97.2 lakh", ["₹108 lakh", "₹100.44 lakh", "₹3.24 lakh"],
  "Revenue = rooms × occupancy × days × tariff",
  "Pine View sells 80 × 90% = 72 rooms a night, i.e. 72 × 30 = 2,160 room-nights in June. At ₹4,500 each, revenue = "
  "₹97,20,000 = ₹97.2 lakh.",
  ["Rooms occupied per night = 80 × 0.90 = 72", "Room-nights = 72 × 30 = 2,160", "Revenue = 2,160 × 4,500 = "
   "₹97,20,000"],
  why="₹108 lakh assumes 100% occupancy; ₹100.44 lakh uses 31 days; ₹3.24 lakh is one night's revenue.", secs=50,
  stim=sid)

pm = (rev["Heritage"] - rev["Sagar"]) / rev["Sagar"] * 100
assert pm == F(625, 100) and near((rev["Heritage"] - rev["Sagar"]) / rev["Heritage"] * 100, 5.882, 1e-3)
assert F(6000 - 3200, 3200) * 100 == F(875, 10)
Q(T, "Table with percentages", I,
  "Heritage's room revenue in June was what percentage more than Sagar's?",
  "6.25%", ["5.88%", "87.5%", "10%"],
  "Compute both revenues, then 'percent more than' on Sagar's base",
  "Heritage: 60 × 85% × 30 = 1,530 room-nights × ₹6,000 = ₹91.8 lakh. Sagar: 120 × 75% × 30 = 2,700 × ₹3,200 = "
  "₹86.4 lakh. Difference ₹5.4 lakh, which is 5.4 ÷ 86.4 = 6.25% of Sagar's revenue.",
  ["Heritage = 1,530 × 6,000 = 91,80,000", "Sagar = 2,700 × 3,200 = 86,40,000", "Difference = 5,40,000",
   "5.4 ÷ 86.4 × 100 = 6.25%"],
  why="5.88% uses Heritage as the base; 87.5% compares the tariffs only (6,000 vs 3,200).", secs=60, stim=sid)

occ = sum(r * F(o, 100) for r, o, _ in HOT.values())
rooms = sum(r for r, _, _ in HOT.values())
assert occ == 366 and rooms == 500 and occ / rooms * 100 == F(732, 10) and F(75 + 90 + 60 + 85 + 70, 5) == 76
Q(T, "Table with percentages", I,
  "On an average night in June, what percentage of all the rooms of the five hotels together were occupied?",
  "73.2%", ["76%", "70%", "74.4%"],
  "A combined percentage is a weighted average, weighted by the number of rooms",
  "Occupied rooms per night: Sagar 90, Pine View 72, Lotus 90, Heritage 51 and Orchid 63, total 366 of 500 rooms. "
  "366 ÷ 500 = 73.2%.",
  ["Sagar 120 × 0.75 = 90; Pine View 80 × 0.90 = 72", "Lotus 150 × 0.60 = 90; Heritage 60 × 0.85 = 51",
   "Orchid 90 × 0.70 = 63", "Total = 366 of 500 rooms", "366 ÷ 500 × 100 = 73.2%"],
  why="76% is the simple average of the five occupancy percentages, which ignores the different hotel sizes.",
  secs=60, stim=sid)

extra = 150 * F(12, 100) * 30 * 2800
assert extra == 1512000 and rev["Lotus"] * F(12, 100) == 907200 and 150 * F(72, 100) * 30 * 2800 == 9072000
Q(T, "Table with percentages", I,
  "If Lotus had achieved an average occupancy of 72% in June at the same tariff, by how much would its room revenue "
  "have increased?",
  "₹15.12 lakh", ["₹9.072 lakh", "₹90.72 lakh", "₹18 lakh"],
  "Extra revenue = rooms × extra occupancy × days × tariff",
  "Occupancy rises by 12 percentage points: 150 × 12% = 18 more rooms a night, i.e. 540 more room-nights in June. "
  "At ₹2,800 each, that is ₹15,12,000 = ₹15.12 lakh.",
  ["Extra rooms per night = 150 × 0.12 = 18", "Extra room-nights = 18 × 30 = 540",
   "Extra revenue = 540 × 2,800 = ₹15,12,000"],
  why="₹9.072 lakh raises revenue by 12% instead of by 12 percentage points of occupancy; ₹90.72 lakh is the new "
      "total revenue, not the increase.", secs=55, stim=sid)

sep = 80 * F(95, 100) * 30 * (4500 * F(90, 100))
chg = (sep - rev["Pine View"]) / rev["Pine View"] * 100
assert sep == 9234000 and chg == -5 and near((F(95, 90) - 1) * 100, 5.556, 1e-3)
Q(T, "Table with percentages", A,
  "In September 2026 (30 days), Pine View cut its tariff by 10% and its occupancy rose to 95%. By what percentage "
  "did its room revenue change compared with June?",
  "5% decrease", ["5.56% increase", "4.5% decrease", "10% decrease"],
  "Revenue ∝ occupancy × tariff when rooms and days are unchanged",
  "Revenue changes by the factor (95/90) × 0.90 = 0.95, a 5% decrease. Directly: 80 × 95% × 30 = 2,280 room-nights "
  "× ₹4,050 = ₹92.34 lakh, against ₹97.2 lakh in June.",
  ["Occupancy factor = 95 ÷ 90", "Tariff factor = 0.90", "Revenue factor = 95/90 × 0.90 = 0.95",
   "Check: 2,280 × 4,050 = 92,34,000 vs 97,20,000 ⇒ −5%"],
  why="5.56% increase counts only the higher occupancy; 10% decrease counts only the tariff cut.", secs=90, stim=sid)

# ================================================================ Bar Graph DI (B4 I3 A2): sets of 5 and 4
T = "Bar Graph DI"
YRS = [2020, 2021, 2022, 2023, 2024, 2025]
VIS = [72, 54, 90, 108, 135, 120]
sid = stimulus("chart", "Visitors to a science museum, 2020 to 2025",
               "The bar graph shows the number of visitors (in thousands) to a city science museum in each year from "
               "2020 to 2025. The bar values are given below.\n\n" +
               md_table(["Year", "Visitors (thousand)"], list(zip(YRS, VIS))),
               {"chart": "bar", "x": YRS, "series": [{"name": "Visitors (thousand)", "values": VIS}]})
V = dict(zip(YRS, VIS))
assert V[2022] + V[2023] == 198
Q(T, "Simple bar", B, "What was the total number of visitors in 2022 and 2023 together?",
  "1,98,000", ["1,88,000", "2,08,000", "18,000"],
  "Read two bars and add; values are in thousands",
  "2022: 90 thousand and 2023: 108 thousand. Together 198 thousand = 1,98,000 visitors.",
  ["90 + 108 = 198 thousand", "= 1,98,000"],
  why="18,000 is the difference between the two years, not the total.", secs=30, stim=sid)

dec = F(V[2020] - V[2021], V[2020]) * 100
assert dec == 25 and F(18, 54) * 100 == F(100, 3)
Q(T, "Simple bar", B, "By what percentage did the number of visitors fall from 2020 to 2021?",
  "25%", ["33⅓%", "18%", "75%"],
  "Percentage decrease = fall ÷ earlier value × 100",
  "Visitors fell from 72 thousand to 54 thousand, a fall of 18 thousand, which is 18 ÷ 72 = 25% of the 2020 figure.",
  ["Fall = 72 − 54 = 18 thousand", "18 ÷ 72 × 100 = 25%"],
  why="33⅓% uses 2021 as the base; 18% is the fall in thousands, not a percentage; 75% is 2021 as a percentage of "
      "2020.", secs=35, stim=sid)

avg = F(sum(VIS), 6)
assert avg == F(965, 10) and F(sum(VIS), 5) == F(1158, 10) and F(sum(VIS[1:]), 5) == F(1014, 10)
Q(T, "Simple bar", I, "What was the average number of visitors per year over the six years?",
  "96,500", ["1,15,800", "1,01,400", "97,000"],
  "Average = total ÷ number of years",
  "Total = 72 + 54 + 90 + 108 + 135 + 120 = 579 thousand. Average = 579 ÷ 6 = 96.5 thousand = 96,500.",
  ["Total = 579 thousand", "Average = 579 ÷ 6 = 96.5 thousand = 96,500"],
  why="1,15,800 divides by 5 instead of 6; 1,01,400 averages only 2021 to 2025.", secs=45, stim=sid)

assert ratio(V[2021] + V[2022], V[2024] + V[2025]) == "48 : 85" and ratio(144, 270) == "8 : 15"
Q(T, "Simple bar", I,
  "What is the ratio of the total visitors in 2021 and 2022 together to the total visitors in 2024 and 2025 "
  "together?",
  "48 : 85", ["85 : 48", "8 : 15", "16 : 27"],
  "Ratio of two sums, reduced to lowest terms",
  "2021 + 2022 = 54 + 90 = 144 thousand; 2024 + 2025 = 135 + 120 = 255 thousand. 144 : 255 = 48 : 85 (dividing by 3).",
  ["54 + 90 = 144", "135 + 120 = 255", "144 : 255 = 48 : 85"],
  why="85 : 48 is reversed; 8 : 15 uses 270 (2 × 135) for the second sum.", secs=45, stim=sid)

r24, r25 = 135000 * 80, 120000 * (80 * F(135, 100))
chg = (r25 - r24) / r24 * 100
assert r24 == 10800000 and r25 == 12960000 and chg == 20 and near(35 - F(15, 135) * 100, 23.89, 1e-2)
Q(T, "Simple bar", A,
  "The ticket price was ₹80 in 2024 and was raised by 35% for 2025. By what percentage did the museum's ticket "
  "revenue change from 2024 to 2025? (Assume every visitor bought one ticket.)",
  "20% increase", ["35% increase", "23.89% increase", "12.5% increase"],
  "Revenue = visitors × price; combine the two changes multiplicatively",
  "2024 revenue = 1,35,000 × ₹80 = ₹1.08 crore. 2025 price = ₹108 and revenue = 1,20,000 × ₹108 = ₹1.296 crore. "
  "Change = 0.216 ÷ 1.08 = 20% increase.",
  ["2024: 1,35,000 × 80 = 1,08,00,000", "2025 price = 80 × 1.35 = 108", "2025: 1,20,000 × 108 = 1,29,60,000",
   "Change = 21,60,000 ÷ 1,08,00,000 = 20%"],
  short="Factor = (120/135) × 1.35 = 1.2.",
  why="35% ignores the fall in visitors; 23.89% adds the percentage changes (+35% and −11.11%) instead of "
      "multiplying the factors.", secs=80, stim=sid)

BOOK = {"Kitab Ghar": (480, 320), "Page Turner": (360, 540), "Readwell": (600, 400), "Bookmark": (420, 280)}
sid = stimulus("chart", "Fiction and non-fiction books sold by four bookstores in a month",
               "The stacked bar graph shows the number of fiction and non-fiction books sold by four bookstores in "
               "October 2026. Each bar is split into the two categories; the values are given below.\n\n" +
               md_table(["Bookstore", "Fiction", "Non-fiction", "Total"],
                        [[k, f_, n_, f_ + n_] for k, (f_, n_) in BOOK.items()]),
               {"chart": "stacked_bar", "x": list(BOOK),
                "series": [{"name": "Fiction", "values": [v[0] for v in BOOK.values()]},
                           {"name": "Non-fiction", "values": [v[1] for v in BOOK.values()]}]})
fic = sum(v[0] for v in BOOK.values())
non = sum(v[1] for v in BOOK.values())
assert (fic, non) == (1860, 1540)
Q(T, "Stacked or grouped bar", B, "How many non-fiction books did the four bookstores sell in all?",
  "1,540", ["1,860", "3,400", "1,440"],
  "Add one segment across all bars",
  "Non-fiction: 320 + 540 + 400 + 280 = 1,540.",
  ["320 + 540 = 860", "860 + 400 = 1,260", "1,260 + 280 = 1,540"],
  why="1,860 is the fiction total; 3,400 is all books.", secs=30, stim=sid)

assert F(600, 1000) * 100 == 60
Q(T, "Stacked or grouped bar", B, "What percentage of the books sold by Readwell were fiction?",
  "60%", ["40%", "150%", "66⅔%"],
  "Segment ÷ bar total × 100",
  "Readwell sold 600 fiction out of 1,000 books, i.e. 60%.",
  ["Readwell total = 600 + 400 = 1,000", "600 ÷ 1,000 × 100 = 60%"],
  why="40% is the non-fiction share; 150% is fiction as a percentage of non-fiction.", secs=30, stim=sid)

a_ = BOOK["Kitab Ghar"][0] + BOOK["Bookmark"][0]
b_ = BOOK["Page Turner"][1] + BOOK["Readwell"][1]
assert (a_, b_) == (900, 940) and ratio(a_, b_) == "45 : 47" and ratio(900, 1000) == "9 : 10"
Q(T, "Stacked or grouped bar", I,
  "What is the ratio of the fiction books sold by Kitab Ghar and Bookmark together to the non-fiction books sold by "
  "Page Turner and Readwell together?",
  "45 : 47", ["47 : 45", "15 : 16", "9 : 10"],
  "Pick the right segment from each bar",
  "Fiction of Kitab Ghar + Bookmark = 480 + 420 = 900. Non-fiction of Page Turner + Readwell = 540 + 400 = 940. "
  "900 : 940 = 45 : 47.",
  ["480 + 420 = 900", "540 + 400 = 940", "900 : 940 = 45 : 47"],
  why="47 : 45 is reversed; 9 : 10 uses 1,000 (Readwell's total) in place of the non-fiction sum.", secs=45,
  stim=sid)

revn = fic * 250 + non * 400
assert revn == 1081000 and 3400 * 325 == 1105000 and fic * 400 + non * 250 == 1129000
Q(T, "Stacked or grouped bar", A,
  "Fiction books sell at an average of ₹250 and non-fiction books at an average of ₹400. What was the total revenue "
  "of the four bookstores from these sales?",
  "₹10.81 lakh", ["₹11.05 lakh", "₹11.29 lakh", "₹6.16 lakh"],
  "Revenue by category = units × average price; the categories have different volumes, so do not average the prices",
  "Fiction: 1,860 × 250 = ₹4,65,000. Non-fiction: 1,540 × 400 = ₹6,16,000. Total = ₹10,81,000 = ₹10.81 lakh.",
  ["Fiction units = 1,860; revenue = 4,65,000", "Non-fiction units = 1,540; revenue = 6,16,000",
   "Total = ₹10,81,000"],
  why="₹11.05 lakh multiplies all 3,400 books by the simple average price ₹325; ₹11.29 lakh swaps the two prices; "
      "₹6.16 lakh is the non-fiction revenue alone.", secs=80, stim=sid)

# ================================================================ Pie Chart DI (B2 I2 A2): two sets of 3
T = "Pie Chart DI"
DEPT = {"Production": 28, "Sales": 18, "Marketing": 14, "HR": 6, "Finance": 12, "IT": 22}
assert sum(DEPT.values()) == 100
EMP = 3500
sid = stimulus("chart", "Employees of a company by department",
               "The pie chart shows how the 3,500 employees of a manufacturing company are distributed across six "
               "departments, as percentages of all employees.\n\n" +
               md_table(["Department", "Share of employees (%)"], list(DEPT.items())),
               {"chart": "pie", "total": EMP, "unit": "percent",
                "slices": [{"label": k, "value": v} for k, v in DEPT.items()]})
cnt = {k: EMP * F(v, 100) for k, v in DEPT.items()}
assert cnt == {"Production": 980, "Sales": 630, "Marketing": 490, "HR": 210, "Finance": 420, "IT": 770}
assert 3600 * F(22, 100) == 792
Q(T, "Percentage-based", B, "How many employees work in the IT department?",
  "770", ["792", "700", "840"],
  "Slice value = total × percentage",
  "22% of 3,500 = 770.",
  ["1% of 3,500 = 35", "22 × 35 = 770"],
  why="792 takes the total as 3,600; 700 uses 20%.", secs=30, stim=sid)

assert ratio(cnt["Marketing"], cnt["HR"] + cnt["Finance"]) == "7 : 9" and ratio(14, 12) == "7 : 6"
assert ratio(14, 6) == "7 : 3"
Q(T, "Percentage-based", I,
  "What is the ratio of the number of employees in Marketing to the number in HR and Finance together?",
  "7 : 9", ["9 : 7", "7 : 6", "7 : 3"],
  "With a common total, ratios of counts equal ratios of percentages",
  "Marketing 14% against HR + Finance = 6% + 12% = 18%. 14 : 18 = 7 : 9 (490 : 630 employees).",
  ["Marketing = 14%", "HR + Finance = 18%", "14 : 18 = 7 : 9"],
  why="9 : 7 is reversed; 7 : 6 compares Marketing with Finance only; 7 : 3 with HR only.", secs=40, stim=sid)

w_ = cnt["Production"] * F(25, 100) + cnt["IT"] * F(40, 100)
share = w_ / (cnt["Production"] + cnt["IT"]) * 100
assert w_ == 553 and share == F(316, 10) and F(25 + 40, 2) == F(65, 2) and w_ / EMP * 100 == F(158, 10)
Q(T, "Percentage-based", A,
  "25% of the Production employees and 40% of the IT employees are women. What percentage of the employees of these "
  "two departments together are women?",
  "31.6%", ["32.5%", "15.8%", "65%"],
  "Weighted average of the two percentages, weighted by department size",
  "Women: 25% of 980 = 245 in Production and 40% of 770 = 308 in IT, total 553. The two departments have "
  "980 + 770 = 1,750 employees, so 553 ÷ 1,750 = 31.6%.",
  ["Production = 980; women = 245", "IT = 770; women = 308", "Women = 553 of 1,750", "553 ÷ 1,750 × 100 = 31.6%"],
  why="32.5% is the simple average of 25% and 40%; 15.8% divides by all 3,500 employees; 65% adds the two "
      "percentages.", secs=80, stim=sid)

S24 = {"P": 30, "Q": 25, "R": 20, "S": 15, "T": 10}
S25 = {"P": 26, "Q": 28, "R": 18, "S": 16, "T": 12}
assert sum(S24.values()) == 100 == sum(S25.values())
sid = stimulus("chart", "Market shares of five smartphone brands, 2024 and 2025",
               "Two pie charts show the market shares (by units sold) of five smartphone brands P, Q, R, S and T in a "
               "state. Total units sold were 40 lakh in 2024 and 50 lakh in 2025.\n\n" +
               md_table(["Brand", "Share in 2024 (%)", "Share in 2025 (%)"], [[k, S24[k], S25[k]] for k in S24]),
               {"chart": "pie_pair", "totals_lakh": {"2024": 40, "2025": 50},
                "series": [{"name": "2024", "slices": [{"label": k, "value": v} for k, v in S24.items()]},
                           {"name": "2025", "slices": [{"label": k, "value": v} for k, v in S25.items()]}]})
u24 = {k: 40 * F(v, 100) for k, v in S24.items()}
u25 = {k: 50 * F(v, 100) for k, v in S25.items()}
assert u25["Q"] == 14 and 50 * F(25, 100) == F(25, 2) and 40 * F(28, 100) == F(112, 10)
Q(T, "Two pie charts", B, "How many units did brand Q sell in 2025?",
  "14 lakh", ["12.5 lakh", "11.2 lakh", "10 lakh"],
  "Use the share and the total of the same year",
  "Q's 2025 share is 28% of 50 lakh = 14 lakh units.",
  ["28% of 50 lakh = 14 lakh"],
  why="12.5 lakh uses Q's 2024 share (25%); 11.2 lakh uses the 2024 total (40 lakh); 10 lakh is Q's 2024 sales.",
  secs=30, stim=sid)

g_ = (u25["T"] - u24["T"]) / u24["T"] * 100
assert (u24["T"], u25["T"]) == (4, 6) and g_ == 50 and F(12 - 10, 10) * 100 == 20
Q(T, "Two pie charts", I, "By what percentage did brand T's unit sales grow from 2024 to 2025?",
  "50%", ["20%", "2%", "40%"],
  "Convert each year's share into units before comparing — the totals differ",
  "2024: 10% of 40 lakh = 4 lakh. 2025: 12% of 50 lakh = 6 lakh. Growth = 2 ÷ 4 = 50%.",
  ["2024 units = 4 lakh", "2025 units = 6 lakh", "Growth = (6 − 4) ÷ 4 × 100 = 50%"],
  why="20% compares the shares (10% → 12%) and ignores the larger market; 2% is the change in percentage points.",
  secs=45, stim=sid)

g_ = (u25["P"] - u24["P"]) / u24["P"] * 100
assert (u24["P"], u25["P"]) == (12, 13) and g_ == F(25, 3) and F(30 - 26, 30) * 100 == F(40, 3)
Q(T, "Two pie charts", A,
  "Brand P's market share fell from 30% in 2024 to 26% in 2025. What happened to its unit sales?",
  "They rose by 8⅓%", ["They fell by 13⅓%", "They fell by 4%", "They fell by 8⅓%"],
  "A falling share of a growing market can still mean higher sales",
  "2024: 30% of 40 lakh = 12 lakh. 2025: 26% of 50 lakh = 13 lakh. Sales rose by 1 lakh, which is 1 ÷ 12 = 8⅓%.",
  ["2024 units = 12 lakh", "2025 units = 13 lakh", "Change = +1 lakh = +8⅓%"],
  why="13⅓% fall is the relative fall in share (4 ÷ 30); 4% is the fall in percentage points; neither accounts for "
      "the market growing from 40 to 50 lakh.", secs=70, stim=sid)

# ================================================================ Line Graph DI (B2 I3 A2): sets of 4 and 3
T = "Line Graph DI"
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
PAT = [400, 360, 440, 484, 550, 466]
sid = stimulus("chart", "Patients treated at a clinic, January to June 2026",
               "The line graph shows the number of patients treated at a neighbourhood clinic in each month from "
               "January to June 2026. The plotted values are given below.\n\n" +
               md_table(["Month", "Patients"], list(zip(MON, PAT))),
               {"chart": "line", "x": MON, "series": [{"name": "Patients", "values": PAT}]})
M = dict(zip(MON, PAT))
inc = F(M["Apr"] - M["Mar"], M["Mar"]) * 100
assert inc == 10 and near(F(44, 484) * 100, 9.09, 1e-2)
Q(T, "Single line", B, "By what percentage did the number of patients increase from March to April?",
  "10%", ["9.09%", "44%", "11%"],
  "Percentage increase = rise ÷ earlier value × 100",
  "Patients rose from 440 to 484, an increase of 44, which is 44 ÷ 440 = 10%.",
  ["Rise = 484 − 440 = 44", "44 ÷ 440 × 100 = 10%"],
  why="9.09% uses April as the base; 44 is the rise in patients, not a percentage.", secs=35, stim=sid)

q1, q2 = sum(PAT[:3]), sum(PAT[3:])
assert (q1, q2) == (1200, 1500) and ratio(q1, q2) == "4 : 5"
Q(T, "Single line", I,
  "What is the ratio of the patients treated in January–March to those treated in April–June?",
  "4 : 5", ["5 : 4", "6 : 7", "3 : 4"],
  "Sum each quarter, then reduce",
  "January–March: 400 + 360 + 440 = 1,200. April–June: 484 + 550 + 466 = 1,500. 1,200 : 1,500 = 4 : 5.",
  ["Q1 = 1,200", "Q2 = 1,500", "1,200 : 1,500 = 4 : 5"],
  why="5 : 4 is reversed.", secs=45, stim=sid)

avg = F(sum(PAT), 6)
assert avg == 450 and F(sum(PAT), 5) == 540
Q(T, "Single line", I, "What was the average number of patients treated per month over the six months?",
  "450", ["540", "455", "445"],
  "Average = total ÷ 6",
  "Total = 400 + 360 + 440 + 484 + 550 + 466 = 2,700. Average = 2,700 ÷ 6 = 450.",
  ["Total = 2,700", "Average = 2,700 ÷ 6 = 450"],
  why="540 divides the total by 5.", secs=40, stim=sid)

r1, r2 = q1 * 300, q2 * 360
assert (r1, r2) == (360000, 540000) and F(r2 - r1, r1) * 100 == 50
Q(T, "Single line", A,
  "The clinic charged a consultation fee of ₹300 per patient from January to March and ₹360 from April to June. Its "
  "fee income in April–June was what percentage more than in January–March?",
  "50%", ["25%", "45%", "20%"],
  "Income = patients × fee; both factors change",
  "January–March: 1,200 × ₹300 = ₹3,60,000. April–June: 1,500 × ₹360 = ₹5,40,000. The increase, ₹1,80,000, is "
  "50% of ₹3,60,000.",
  ["Q1 income = 3,60,000", "Q2 income = 5,40,000", "Increase = 1,80,000 ⇒ 50%"],
  short="Factor = (1,500/1,200) × (360/300) = 1.25 × 1.2 = 1.5.",
  why="25% counts only the rise in patients; 20% only the rise in fee; 45% adds the two percentages instead of "
      "multiplying the factors.", secs=70, stim=sid)

TY = [2021, 2022, 2023, 2024, 2025]
EXP = [120, 150, 135, 180, 210]
IMP = [100, 120, 150, 150, 186]
sid = stimulus("chart", "Exports and imports of a textile firm, 2021 to 2025",
               "The line graph shows the value of exports and imports (in ₹ crore) of a textile firm from 2021 to "
               "2025. The plotted values are given below.\n\n" +
               md_table(["Year", "Exports (₹ crore)", "Imports (₹ crore)"], [list(r) for r in zip(TY, EXP, IMP)]),
               {"chart": "line", "x": TY, "series": [{"name": "Exports", "values": EXP},
                                                     {"name": "Imports", "values": IMP}]})
deficit = [y for y, e, i_ in zip(TY, EXP, IMP) if i_ > e]
assert deficit == [2023]
Q(T, "Multiple lines", B, "In which year were the firm's imports greater than its exports?",
  "2023", ["2024", "2022", "2021"],
  "Compare the two lines year by year",
  "Only in 2023 is the imports line above the exports line: imports ₹150 crore against exports ₹135 crore.",
  ["2021: 120 > 100", "2022: 150 > 120", "2023: 135 < 150 (imports higher)", "2024: 180 > 150", "2025: 210 > 186"],
  why="In 2024 imports stayed at their 2023 level (₹150 crore), but exports rose to ₹180 crore.", secs=35, stim=sid)

surplus = sum(EXP) - sum(IMP)
pos = sum(e - i_ for e, i_ in zip(EXP, IMP) if e > i_)
assert surplus == 89 and pos == 104 and pos + 15 == 119
Q(T, "Multiple lines", I,
  "What was the firm's total trade surplus (exports minus imports) over the five years taken together?",
  "₹89 crore", ["₹104 crore", "₹119 crore", "₹74 crore"],
  "Net surplus = total exports − total imports (a deficit year counts as negative)",
  "Total exports = ₹795 crore and total imports = ₹706 crore, so the net surplus is ₹89 crore.",
  ["Exports total = 120 + 150 + 135 + 180 + 210 = 795", "Imports total = 100 + 120 + 150 + 150 + 186 = 706",
   "Surplus = 795 − 706 = ₹89 crore"],
  why="₹104 crore adds only the surplus years and ignores the ₹15 crore deficit in 2023; ₹119 crore adds that "
      "deficit instead of subtracting it.", secs=55, stim=sid)

t21, t25 = EXP[0] + IMP[0], EXP[-1] + IMP[-1]
g_ = F(t25 - t21, t21) * 100
assert (t21, t25) == (220, 396) and g_ == 80 and F(210 - 120, 120) * 100 == 75 and F(186 - 100, 100) * 100 == 86
Q(T, "Multiple lines", A,
  "By what percentage did the firm's total trade (exports + imports) grow from 2021 to 2025?",
  "80%", ["75%", "86%", "80.5%"],
  "Growth of a sum is a weighted average of the growth rates, not a simple average",
  "Total trade was 120 + 100 = ₹220 crore in 2021 and 210 + 186 = ₹396 crore in 2025. Growth = 176 ÷ 220 = 80%.",
  ["2021 total = 220", "2025 total = 396", "Growth = (396 − 220) ÷ 220 × 100 = 80%"],
  why="75% is the growth of exports alone and 86% of imports alone; 80.5% is their simple average, which ignores "
      "that exports were the larger part in 2021.", secs=75, stim=sid)

# ================================================================ Caselet DI (B4 I3 A1): two sets of 4
T = "Caselet DI"
FR = {"Mango": (500, 80, 8, 100), "Apple": (400, 120, 5, 150), "Banana": (300, 40, 10, 50)}
assert sum(v[0] for v in FR.values()) == 1200 and ratio(500, 400, 300) == "5 : 4 : 3"
sid = stimulus("caselet", "A fruit wholesaler's purchases, spoilage and sales",
               "A fruit wholesaler bought 1,200 kg of fruit: mangoes, apples and bananas in the ratio 5 : 4 : 3 by "
               "weight. He paid ₹80 per kg for mangoes, ₹120 per kg for apples and ₹40 per kg for bananas. Before they "
               "could be sold, 8% of the mangoes, 5% of the apples and 10% of the bananas (by weight) spoiled and "
               "were thrown away. He sold all the remaining fruit at ₹100 per kg for mangoes, ₹150 per kg for apples "
               "and ₹50 per kg for bananas.")
kg = {k: v[0] for k, v in FR.items()}
spoil = {k: v[0] * F(v[2], 100) for k, v in FR.items()}
sold = {k: kg[k] - spoil[k] for k in FR}
cost = sum(v[0] * v[1] for v in FR.values())
revn = sum(sold[k] * FR[k][3] for k in FR)
assert spoil == {"Mango": 40, "Apple": 20, "Banana": 30} and cost == 100000 and revn == 116500
Q(T, "Paragraph data", B, "How many kilograms of apples spoiled?",
  "20 kg", ["40 kg", "30 kg", "25 kg"],
  "First split 1,200 kg in the ratio 5 : 4 : 3",
  "Apples = 4/12 of 1,200 = 400 kg, and 5% of 400 kg = 20 kg spoiled.",
  ["Apples = 1,200 × 4/12 = 400 kg", "Spoiled = 5% of 400 = 20 kg"],
  why="40 kg is the spoiled mangoes and 30 kg the spoiled bananas.", secs=35, stim=sid)

assert 1200 * 80 == 96000
Q(T, "Paragraph data", B, "What was the total amount the wholesaler paid for the fruit?",
  "₹1,00,000", ["₹96,000", "₹1,16,500", "₹90,000"],
  "Cost = Σ (weight × price per kg) for each fruit",
  "Mangoes 500 kg × ₹80 = ₹40,000; apples 400 kg × ₹120 = ₹48,000; bananas 300 kg × ₹40 = ₹12,000. Total "
  "₹1,00,000.",
  ["Mango: 500 × 80 = 40,000", "Apple: 400 × 120 = 48,000", "Banana: 300 × 40 = 12,000", "Total = ₹1,00,000"],
  why="₹96,000 prices all 1,200 kg at the mango rate; ₹1,16,500 is the sales revenue.", secs=40, stim=sid)

m_rev = sold["Mango"] * 100
assert m_rev == 46000 and 500 * 100 == 50000 and sold["Mango"] * 80 == 36800
Q(T, "Paragraph data", I, "How much did the wholesaler receive from selling mangoes?",
  "₹46,000", ["₹50,000", "₹36,800", "₹6,000"],
  "Only the unspoiled weight is sold",
  "8% of 500 kg = 40 kg spoiled, so 460 kg were sold at ₹100 per kg: ₹46,000.",
  ["Spoiled mangoes = 40 kg", "Sold = 460 kg", "Revenue = 460 × 100 = ₹46,000"],
  why="₹50,000 ignores spoilage; ₹36,800 uses the cost price per kg; ₹6,000 is the profit on mangoes.", secs=45,
  stim=sid)

pp = F(revn - cost, cost) * 100
assert pp == F(165, 10) and near(F(16500, 116500) * 100, 14.16, 1e-2)
assert F(500 * 100 + 400 * 150 + 300 * 50 - cost, cost) * 100 == 25
Q(T, "Paragraph data", I, "What was the wholesaler's overall profit percentage on the whole deal?",
  "16.5%", ["25%", "14.16%", "20%"],
  "Profit % = (total revenue − total cost) ÷ total cost × 100",
  "Revenue: mangoes 460 × 100 = ₹46,000, apples 380 × 150 = ₹57,000, bananas 270 × 50 = ₹13,500, total ₹1,16,500. "
  "Profit = ₹16,500 on a cost of ₹1,00,000 = 16.5%.",
  ["Revenue = 46,000 + 57,000 + 13,500 = 1,16,500", "Cost = 1,00,000", "Profit = 16,500 ⇒ 16.5%"],
  why="25% ignores the spoiled fruit; 14.16% divides the profit by the revenue instead of the cost.", secs=70,
  stim=sid)

SCR = {"Screen 1": (240, 5, 80, 200), "Screen 2": (180, 4, 75, 250), "Screen 3": (150, 6, 64, 180),
       "Screen 4": (120, 4, 90, 400)}
sid = stimulus("caselet", "Seats, shows and ticket prices at a multiplex",
               "A multiplex has four screens. The table gives each screen's seating capacity, the number of shows it "
               "runs on a Saturday, the average percentage of seats filled per show that day, and the ticket price. "
               "Screen 4 has recliner seats and charges more. Every show of a screen has the same capacity and the "
               "same average occupancy.\n\n" +
               md_table(["Screen", "Seats", "Shows", "Seats filled (%)", "Ticket price (₹)"],
                        [[k, *v] for k, v in SCR.items()]),
               {"columns": ["screen", "seats", "shows", "occupancy_pct", "price_rs"],
                "rows": [[k, *v] for k, v in SCR.items()]})
offered = {k: s_ * n_ for k, (s_, n_, _, _) in SCR.items()}
tickets = {k: offered[k] * F(o, 100) for k, (_, _, o, _) in SCR.items()}
assert offered == {"Screen 1": 1200, "Screen 2": 720, "Screen 3": 900, "Screen 4": 480}
assert tickets == {"Screen 1": 960, "Screen 2": 540, "Screen 3": 576, "Screen 4": 432}
Q(T, "Caselet with table", B, "How many tickets did Screen 1 sell on Saturday?",
  "960", ["192", "1,200", "1,000"],
  "Tickets = seats × shows × occupancy",
  "Screen 1 offers 240 × 5 = 1,200 seats over the day, and 80% of them are filled: 960 tickets.",
  ["Seats offered = 240 × 5 = 1,200", "80% of 1,200 = 960"],
  why="192 is the tickets for one show; 1,200 is the seats offered.", secs=35, stim=sid)

assert sum(offered.values()) == 3300 and sum(s_ for s_, _, _, _ in SCR.values()) == 690
Q(T, "Caselet with table", B, "How many seats did the multiplex offer in all on Saturday, counting every show?",
  "3,300", ["690", "2,508", "3,000"],
  "Seats offered = seats per show × number of shows, summed over screens",
  "Screen 1: 240 × 5 = 1,200; Screen 2: 180 × 4 = 720; Screen 3: 150 × 6 = 900; Screen 4: 120 × 4 = 480. "
  "Total = 3,300.",
  ["1,200 + 720 = 1,920", "1,920 + 900 = 2,820", "2,820 + 480 = 3,300"],
  why="690 is the seating capacity of the four screens for a single show each; 2,508 is the number of tickets "
      "actually sold.", secs=40, stim=sid)

r4 = tickets["Screen 4"] * 400
assert r4 == 172800 and 480 * 400 == 192000 and 108 * 400 == 43200
Q(T, "Caselet with table", I, "What was Screen 4's ticket revenue on Saturday?",
  "₹1,72,800", ["₹1,92,000", "₹48,000", "₹43,200"],
  "Revenue = tickets sold × price",
  "Screen 4 offers 120 × 4 = 480 seats, 90% filled = 432 tickets. At ₹400 each, revenue = ₹1,72,800.",
  ["Seats offered = 480", "Tickets = 90% of 480 = 432", "Revenue = 432 × 400 = ₹1,72,800"],
  why="₹1,92,000 assumes every seat was sold; ₹43,200 is the revenue from one show (108 tickets).", secs=45,
  stim=sid)

ov = F(sum(tickets.values()), sum(offered.values())) * 100
assert ov == 76 and F(80 + 75 + 64 + 90, 4) == F(30900, 400)
Q(T, "Caselet with table", A,
  "Taking all shows of all four screens together, what percentage of the seats offered on Saturday were filled?",
  "76%", ["77.25%", "75%", "78%"],
  "An overall percentage is weighted by the seats offered, not a simple average of the four percentages",
  "Tickets sold: 960 + 540 + 576 + 432 = 2,508. Seats offered: 3,300. 2,508 ÷ 3,300 = 76%.",
  ["Tickets: 960 + 540 + 576 + 432 = 2,508", "Seats offered = 3,300", "2,508 ÷ 3,300 × 100 = 76%"],
  why="77.25% is the simple average of 80, 75, 64 and 90, which ignores that the screens offer different numbers "
      "of seats.", secs=75, stim=sid)

# ================================================================ Missing DI (B3 I2 A1): two sets of 3
T = "Missing DI"
MARKS = {"Anu": (78, 88, 64), "Babu": (85, 72, 81), "Charu": (92, 85, 78), "Dev": (66, 74, 70), "Esha": (88, 90, 76)}
shown = {"Anu": ("78", "—", "64", "230"), "Babu": ("—", "72", "81", "238"), "Charu": ("92", "85", "—", "255"),
         "Dev": ("66", "—", "70", "210"), "Esha": ("88", "90", "76", "—")}
for k, (m_, s_, e_) in MARKS.items():
    row = shown[k]
    for val, cell in zip((m_, s_, e_, m_ + s_ + e_), row):
        assert cell == "—" or int(cell) == val, (k, val, cell)
    assert sum(1 for c_ in row if c_ == "—") == 1
sid = stimulus("data_table", "Marks of five students in three subjects (some missing)",
               "The table shows the marks (out of 100 in each subject) of five students in a class test, with each "
               "student's total. One value in each row is missing (—); find it from the others.\n\n" +
               md_table(["Student", "Maths", "Science", "English", "Total"], [[k, *v] for k, v in shown.items()]))
assert 230 - 78 - 64 == 88 and 230 - 64 == 166
Q(T, "Table with missing values", B, "What were Anu's marks in Science?",
  "88", ["166", "86", "92"],
  "Missing value = total − the known values",
  "Anu's total is 230, and Maths + English = 78 + 64 = 142. So Science = 230 − 142 = 88.",
  ["78 + 64 = 142", "230 − 142 = 88"],
  why="166 subtracts only the English marks (230 − 64).", secs=30, stim=sid)

sci = [v[1] for v in MARKS.values()]
assert sum(sci) == 409 and F(409, 5) == F(818, 10) and F(409, 4) == F(10225, 100)
assert near(F(72 + 85 + 90, 3), 82.33, 1e-2)
Q(T, "Table with missing values", B, "What were the average Science marks of the five students?",
  "81.8", ["82.33", "102.25", "79.6"],
  "Fill in the missing Science marks first, then average all five",
  "Missing Science marks: Anu 230 − 78 − 64 = 88 and Dev 210 − 66 − 70 = 74. Science total = 88 + 72 + 85 + 74 + 90 "
  "= 409, average 409 ÷ 5 = 81.8.",
  ["Anu: 88; Dev: 74", "Total = 88 + 72 + 85 + 74 + 90 = 409", "Average = 409 ÷ 5 = 81.8"],
  why="82.33 averages only the three Science marks shown; 102.25 divides 409 by 4.", secs=50, stim=sid)

gap = F(238 - 210, 3)
assert gap == F(28, 3)
Q(T, "Table with missing values", I,
  "By how many marks is the average of Babu's three subject marks higher than the average of Dev's three subject "
  "marks?",
  "9⅓", ["28", "9", "7"],
  "Average of a row = row total ÷ 3; the missing cells do not change the given totals",
  "Babu's total is 238 and Dev's is 210, so the averages differ by (238 − 210) ÷ 3 = 28 ÷ 3 = 9⅓ marks.",
  ["Babu's average = 238 ÷ 3", "Dev's average = 210 ÷ 3", "Difference = 28 ÷ 3 = 9⅓"],
  why="28 is the difference in totals, not in averages.", secs=45, stim=sid)

ART = {"Kettle": (800, 25, 10), "Iron": (1000, 40, 15), "Fan": (1500, 40, 20), "Mixer": (2400, 50, 20),
       "Toaster": (950, 60, 30)}
calc = {}
for k, (c_, m_, d_) in ART.items():
    mp_ = c_ * F(100 + m_, 100)
    sp_ = mp_ * F(100 - d_, 100)
    calc[k] = (c_, m_, d_, sp_, (sp_ - c_) / c_ * 100)
assert calc["Kettle"][3:] == (900, F(25, 2)) and calc["Iron"][3:] == (1190, 19) and calc["Fan"][3:] == (1680, 12)
assert calc["Mixer"][3:] == (2880, 20) and calc["Toaster"][3:] == (1064, 12)
shown = {"Kettle": ("800", "25", "—", "900", "—"), "Iron": ("—", "40", "15", "1,190", "—"),
         "Fan": ("1,500", "—", "20", "—", "12"), "Mixer": ("2,400", "50", "—", "—", "20"),
         "Toaster": ("950", "60", "30", "—", "—")}
for k, row in shown.items():
    full = (ind(calc[k][0]), N(calc[k][1]), N(calc[k][2]), ind(int(calc[k][3])), N(calc[k][4]))
    assert all(a == "—" or a == b for a, b in zip(row, full)), (k, row, full)
sid = stimulus("data_table", "Cost, markup, discount and selling price of five kitchen appliances",
               "A shop sells five kitchen appliances. The table shows each one's cost price (₹), markup on cost (%), "
               "discount on the marked price (%), selling price (₹) and profit on cost (%). Some values are missing "
               "(—); find them from the others.\n\n" +
               md_table(["Appliance", "Cost price (₹)", "Markup (%)", "Discount (%)", "Selling price (₹)",
                         "Profit (%)"], [[k, *v] for k, v in shown.items()]))
assert (1 - F(900, 1000)) * 100 == 10 and near(F(100, 900) * 100, 11.11, 1e-2)
Q(T, "Table with missing values", B, "What discount was allowed on the kettle?",
  "10%", ["11.11%", "12.5%", "25%"],
  "Marked price = cost × (1 + markup); discount % is on the marked price",
  "Marked price = 800 × 1.25 = ₹1,000. It sold for ₹900, so the discount = 100 ÷ 1,000 = 10%.",
  ["MP = 800 × 1.25 = 1,000", "Discount = 1,000 − 900 = 100", "100 ÷ 1,000 × 100 = 10%"],
  why="11.11% divides the discount by the selling price; 12.5% is the kettle's profit percentage.", secs=40,
  stim=sid)

ms = [m for m in range(0, 101) if 1500 * F(100 + m, 100) * F(80, 100) == 1500 * F(112, 100)]
assert ms == [40] and F(112, 100) * F(120, 100) == F(1344, 1000)
Q(T, "Table with missing values", I, "What was the markup percentage on the fan?",
  "40%", ["32%", "34.4%", "25%"],
  "Work back: SP from profit %, then MP from discount %, then markup",
  "SP = 1,500 × 1.12 = ₹1,680. After a 20% discount, MP = 1,680 ÷ 0.8 = ₹2,100. Markup = 600 ÷ 1,500 = 40%.",
  ["SP = 1,500 × 1.12 = 1,680", "MP = 1,680 ÷ 0.80 = 2,100", "Markup = (2,100 − 1,500) ÷ 1,500 = 40%"],
  why="32% adds 12% and 20%; 34.4% multiplies 1.12 by 1.2 instead of dividing by 0.8.", secs=55, stim=sid)

tp = sum(v[3] - v[0] for v in calc.values())
tc = sum(v[0] for v in calc.values())
ts = sum(v[3] for v in calc.values())
assert (tp, tc, ts) == (1064, 6650, 7714) and F(tp, tc) * 100 == 16
assert F(sum(v[4] for v in calc.values()), 5) == F(151, 10) and near(F(tp, ts) * 100, 13.79, 1e-2)
Q(T, "Table with missing values", A,
  "If the shop sells one unit of each of the five appliances, what is its overall profit as a percentage of the "
  "total cost?",
  "16%", ["15.1%", "13.79%", "17.5%"],
  "Fill every missing value first; overall profit % = total profit ÷ total cost",
  "Selling prices: kettle ₹900, iron ₹1,190, fan ₹1,680, mixer 2,400 × 1.2 = ₹2,880, toaster 950 × 1.6 × 0.7 = "
  "₹1,064. Iron's cost = 1,190 ÷ (1.4 × 0.85) = ₹1,000. Total cost = ₹6,650, total sales = ₹7,714, profit = "
  "₹1,064, i.e. 16% of cost.",
  ["Iron: MP = 1,190 ÷ 0.85 = 1,400; CP = 1,400 ÷ 1.4 = 1,000", "Mixer: SP = 2,400 × 1.2 = 2,880",
   "Toaster: SP = 950 × 1.6 × 0.7 = 1,064", "Total CP = 800 + 1,000 + 1,500 + 2,400 + 950 = 6,650",
   "Total SP = 900 + 1,190 + 1,680 + 2,880 + 1,064 = 7,714", "Profit = 1,064 ⇒ 1,064 ÷ 6,650 = 16%"],
  why="15.1% is the simple average of the five profit percentages; 13.79% divides the profit by total sales.",
  secs=110, stim=sid)

# ================================================================ Quantity Comparison (B1 I2 A3)
T = "Quantity Comparison"
QREL = {">": "Quantity I > Quantity II", ">=": "Quantity I ≥ Quantity II", "<": "Quantity I < Quantity II",
        "<=": "Quantity I ≤ Quantity II", "cbe": "Quantity I = Quantity II or the relationship cannot be established"}


def qc(sub, diff, q1, q2, vals1, vals2, expect, wrong_syms, concept, expl, steps, short=None, why=None, secs=None,
       by=None):
    got = relation(vals1, vals2)
    assert got == expect, (q1, got)
    assert expect not in wrong_syms and "cbe" not in wrong_syms and len(set(wrong_syms)) == 2
    if expect == "cbe":
        third = next(s_ for s_ in (">", "<", ">=", "<=") if s_ not in wrong_syms)
        wrong = [QREL[wrong_syms[0]], QREL[wrong_syms[1]], QREL[third]]
        no_true_distractor(vals1, vals2, [*wrong_syms, third])
    else:
        wrong = [QREL[wrong_syms[0]], QREL["cbe"], QREL[wrong_syms[1]]]
        no_true_distractor(vals1, vals2, wrong_syms)
    Q(T, sub, diff, f"Compare the two quantities and choose the correct option.\nQuantity I: {q1}\nQuantity II: {q2}",
      QREL[expect], wrong, concept, expl, steps, short, why, secs, by=by)


q1v = F(100 - 80, 80) * 100
q2v = F(500 - 380, 500) * 100
assert (q1v, q2v) == (25, 24)
qc("Arithmetic-based comparison", B,
   "Profit percentage on an article bought for ₹80 and sold for ₹100",
   "Discount percentage on an article marked at ₹500 and sold for ₹380",
   [q1v], [q2v], ">", ["<", "<="],
   "Profit % is on cost price; discount % is on marked price",
   "Quantity I = 20 ÷ 80 × 100 = 25%. Quantity II = 120 ÷ 500 × 100 = 24%. So Quantity I > Quantity II.",
   ["I: profit = 20 on cost 80 ⇒ 25%", "II: discount = 120 on marked price 500 ⇒ 24%", "25 > 24"],
   why="'Quantity I < Quantity II' comes from taking the profit on the selling price (20 ÷ 100 = 20%).", secs=40)

q1v = F(10 * 10, 2)
q2v = F(314, 100) * 16
assert q1v == 50 and q2v == F(5024, 100)
qc("Quantity I vs II", I,
   "Area (cm²) of a square whose diagonal is 10 cm", "Area (cm²) of a circle of radius 4 cm (take π = 3.14)",
   [q1v], [q2v], "<", [">", ">="],
   "Area of a square from its diagonal = d²/2",
   "Quantity I = 10² ÷ 2 = 50 cm². Quantity II = 3.14 × 16 = 50.24 cm². So Quantity I < Quantity II.",
   ["I: side = 10/√2, area = 100/2 = 50", "II: 3.14 × 4² = 50.24", "50 < 50.24"],
   why="'Quantity I > Quantity II' comes from taking the square's area as d² = 100.", secs=50)

q1v = F(sum(4 * k for k in range(1, 16)), 15)
q2v = F(2 * 30 * 34, 30 + 34)
assert q1v == 32 and q2v == F(255, 8)
qc("Arithmetic-based comparison", I,
   "The average of the first 15 multiples of 4",
   "The average speed (km/h) of a car that goes from A to B at 30 km/h and returns from B to A at 34 km/h",
   [q1v], [q2v], ">", ["<", "<="],
   "Average of an arithmetic sequence; average speed for equal distances = 2ab ÷ (a + b)",
   "Quantity I = (4 + 60) ÷ 2 = 32. Quantity II = 2 × 30 × 34 ÷ 64 = 31.875 km/h. So Quantity I > Quantity II.",
   ["I: multiples 4, 8, …, 60; average = (4 + 60) ÷ 2 = 32", "II: 2 × 30 × 34 ÷ (30 + 34) = 2,040 ÷ 64 = 31.875",
    "32 > 31.875"],
   why="'Quantity I = Quantity II or cannot be established' comes from averaging the speeds ((30 + 34) ÷ 2 = 32), "
       "which is wrong for equal distances.", secs=60)

q1v = 10000 * (F(11, 10) ** 2 - 1)
q2v = F(7200 * F(95, 10) * 3, 100)
assert q1v == 2100 and q2v == 2052
qc("Arithmetic-based comparison", A,
   "Compound interest on ₹10,000 for 1 year at 20% per annum, compounded half-yearly",
   "Simple interest on ₹7,200 for 3 years at 9.5% per annum",
   [q1v], [q2v], ">", ["<=", "<"],
   "Half-yearly compounding: half the rate, twice the periods",
   "Quantity I = 10,000 × (1.1² − 1) = 10,000 × 0.21 = ₹2,100. Quantity II = 7,200 × 9.5 × 3 ÷ 100 = ₹2,052. So "
   "Quantity I > Quantity II.",
   ["I: 10% per half-year for 2 half-years ⇒ 1.21 ⇒ CI = 2,100", "II: 7,200 × 0.095 × 3 = 2,052", "2,100 > 2,052"],
   why="'Quantity I < Quantity II' comes from computing I as simple interest (₹2,000).", secs=80)

dice = list(itertools.product(range(1, 7), repeat=2))
q1v = F(sum(1 for a, b in dice if a + b == 9), 36)
q2v = F(sum(1 for r_, s_ in deck if r_ in (12, 13)), 52)
assert q1v == F(1, 9) and q2v == F(2, 13)
qc("Quantity I vs II", A,
   "Probability of getting a total of 9 when two fair dice are rolled",
   "Probability that a card drawn at random from a pack of 52 is a king or a queen",
   [q1v], [q2v], "<", [">=", ">"],
   "Classical probability; compare fractions by cross-multiplying",
   "Quantity I: totals of 9 are (3,6), (4,5), (5,4), (6,3), so 4/36 = 1/9 ≈ 0.111. Quantity II: 8/52 = 2/13 ≈ 0.154. "
   "So Quantity I < Quantity II.",
   ["I: 4 favourable of 36 ⇒ 1/9", "II: 4 kings + 4 queens = 8 of 52 ⇒ 2/13", "1/9 vs 2/13: 13 < 18, so 1/9 < 2/13"],
   why="'Quantity I > Quantity II' comes from counting only kings for Quantity II (4/52 = 1/13, which is less than "
       "1/9).", secs=80, by=BRUTE)

a_vals = [a for a in range(-20, 21) if a * a == 49]
b_vals = [b for b in range(-20, 21) if b ** 3 == -343]
assert a_vals == [-7, 7] and b_vals == [-7]
qc("Quantity I vs II", A,
   "The value of a, where a² = 49", "The value of b, where b³ = −343",
   [F(x) for x in a_vals], [F(x) for x in b_vals], ">=", [">", "<="],
   "A square has two real roots (±); a cube has exactly one real root, with the same sign as the number",
   "a = 7 or −7. b³ = −343 has the single real root b = −7. If a = 7, a > b; if a = −7, a = b. So Quantity I ≥ "
   "Quantity II.",
   ["I: a = +7 or −7", "II: b = −7 (only real cube root of −343)", "a = 7 > −7; a = −7 = −7", "So I ≥ II"],
   why="'Quantity I > Quantity II' forgets the root a = −7; 'Quantity I ≤ Quantity II' wrongly gives b two values.",
   secs=70)

# ================================================================ Data Sufficiency (Quant) (B2 I2 A1)
T = "Data Sufficiency (Quant)"
DS2 = {"I": "Statement I alone is sufficient, but statement II alone is not",
       "II": "Statement II alone is sufficient, but statement I alone is not",
       "either": "Either statement I alone or statement II alone is sufficient",
       "both": "Both statements I and II together are needed",
       "neither": "Statements I and II together are not sufficient"}
DS_PRE = ("Each question below is followed by two statements. Decide whether the data in the statements are "
          "sufficient to answer the question.")


def ds2_verdict(cands, s1, s2, target):
    """Classify sufficiency by enumeration: a set of conditions is sufficient if the target value is unique."""
    def unique(conds):
        vals = {target(c) for c in cands if all(f(c) for f in conds)}
        return len(vals) == 1
    a, b, both = unique([s1]), unique([s2]), unique([s1, s2])
    if a and b:
        return "either"
    if a:
        return "I"
    if b:
        return "II"
    return "both" if both else "neither"


def rev(n):
    return int(str(n)[::-1])


cands = list(range(10, 100))
verdict = ds2_verdict(cands, lambda n: n // 10 + n % 10 == 9, lambda n: n - rev(n) == 27, lambda n: n)
assert verdict == "both" and [n for n in cands if n // 10 + n % 10 == 9 and n - rev(n) == 27] == [63]
Q(T, "Two-statement", B,
  f"{DS_PRE}\nQuestion: What is the two-digit number?\n"
  "I. The sum of its digits is 9.\nII. The number is 27 more than the number formed by reversing its digits.",
  DS2["both"], [DS2["I"], DS2["either"], DS2["neither"]],
  "Two unknown digits need two independent conditions",
  "Let the number be 10a + b. I gives a + b = 9 (18, 27, …, 90 all fit). II gives 9(a − b) = 27, so a − b = 3 "
  "(30, 41, 52, …, 96 all fit). Together, a = 6 and b = 3, so the number is 63. Both statements are needed.",
  ["I alone: a + b = 9 — many numbers (18, 27, 36, …)", "II alone: (10a + b) − (10b + a) = 9(a − b) = 27 ⇒ "
   "a − b = 3 — many numbers", "Together: a + b = 9, a − b = 3 ⇒ a = 6, b = 3", "Number = 63; both needed"],
  why="'Statement I alone' ignores that every multiple of 9 from 18 to 90 has digit sum 9.", secs=40, by=BRUTE)

grid = [F(k, 4) for k in range(1, 68)]
cands = [(17 - w, w) for w in grid if 17 - w > 0]
cands += [(math.sqrt(169 - float(w) ** 2), w) for w in grid if w < 13]
s1 = lambda c: near(float(c[0]) + float(c[1]), 17, 1e-9)
s2 = lambda c: near(float(c[0]) ** 2 + float(c[1]) ** 2, 169, 1e-9)
area = lambda c: round(float(c[0]) * float(c[1]), 6)
verdict = ds2_verdict(cands, s1, s2, area)
assert verdict == "both" and {area(c) for c in cands if s1(c) and s2(c)} == {60.0}
assert F(17 ** 2 - 169, 2) == 60
Q(T, "Two-statement", B,
  f"{DS_PRE}\nQuestion: What is the area of the rectangular plot?\n"
  "I. The perimeter of the plot is 34 m.\nII. The diagonal of the plot is 13 m.",
  DS2["both"], [DS2["I"], DS2["II"], DS2["neither"]],
  "Area = lw; (l + w)² = l² + w² + 2lw",
  "I gives l + w = 17, which allows many rectangles (for example 10 × 7 or 12 × 5, with different areas). II gives "
  "l² + w² = 169, which also allows many shapes. Together, 2lw = (l + w)² − (l² + w²) = 289 − 169 = 120, so the "
  "area lw = 60 m². Both are needed.",
  ["I alone: l + w = 17 — area can be 70 (10 × 7), 60 (12 × 5), …", "II alone: l² + w² = 169 — area not fixed",
   "Together: 2lw = 17² − 169 = 120 ⇒ lw = 60 m²", "Both needed"],
  why="'Statement II alone' is tempting because 5-12-13 is a familiar triple, but other non-integer sides also "
      "have a 13 m diagonal (for example 2 m and √165 m).", secs=50, by=BRUTE)

cands = [(cp, sp) for cp in range(1, 3001) for sp in (F(6, 5) * cp, 1440)]
s1 = lambda c: c[1] == F(6, 5) * c[0] and F(5, 4) * c[0] - c[1] == 60
s2 = lambda c: c[1] == F(1800) * F(80, 100)
verdict = ds2_verdict(cands, s1, s2, lambda c: c[0])
assert verdict == "I" and {c[0] for c in cands if s1(c)} == {1200} and 1200 * F(6, 5) == 1440
Q(T, "Two-statement", I,
  f"{DS_PRE}\nQuestion: What is the cost price of the cooler?\n"
  "I. The cooler was sold at a profit of 20%; had it been sold for ₹60 more, the profit would have been 25%.\n"
  "II. The cooler's marked price is ₹1,800 and it was sold at a discount of 20%.",
  DS2["I"], [DS2["both"], DS2["either"], DS2["II"]],
  "Statement I links two profit levels to a known rupee difference; II gives only the selling price",
  "I: the extra ₹60 moves the profit from 20% to 25%, so 5% of the cost = ₹60 and the cost = ₹1,200 — sufficient. "
  "II: the selling price is 1,800 × 0.8 = ₹1,440, but with no profit information the cost is unknown — not "
  "sufficient. (Together they agree: 1,200 × 1.2 = 1,440.)",
  ["I: 25% − 20% = 5% of CP = 60 ⇒ CP = 1,200 — sufficient", "II: SP = 1,440 only — CP unknown",
   "Statement I alone is sufficient"],
  why="'Both together' is chosen when II's selling price seems necessary, but I already fixes the cost.", secs=60,
  by=BRUTE)

DS3W = {"any2": "Any two of the three statements together are sufficient",
        "all": "All three statements together are necessary",
        "13": "Only statements I and III together are sufficient",
        "none": "Even all three statements together are not sufficient"}
cands = [(a, b) for a in range(1, 401) for b in range(1, 401)]
c1 = lambda c: F(1, c[0]) + F(1, c[1]) == F(1, 12)
c2 = lambda c: F(1, c[1]) == F(3, 2) * F(1, c[0])
c3 = lambda c: c[1] == 20


def uniq(conds):
    return len({c[0] for c in cands if all(f(c) for f in conds)}) == 1


assert not any(uniq([f]) for f in (c1, c2, c3))
assert uniq([c1, c2]) and uniq([c1, c3]) and uniq([c2, c3])
assert {c[0] for c in cands if c1(c) and c2(c)} == {c[0] for c in cands if c2(c) and c3(c)} == {30}
Q(T, "Three-statement", I,
  "The question below is followed by three statements. Decide which statements are sufficient to answer it.\n"
  "Question: In how many days can A alone finish a piece of work?\n"
  "I. A and B together can finish it in 12 days.\nII. B is 50% more efficient than A.\n"
  "III. B alone can finish it in 20 days.",
  DS3W["any2"], [DS3W["all"], DS3W["13"], DS3W["none"]],
  "Two unknowns (A's and B's rates); each statement is one equation",
  "I + II: A's rate a and B's rate 1.5a give 2.5a = 1/12, so A takes 30 days. I + III: a = 1/12 − 1/20 = 1/30, so "
  "30 days. II + III: B's rate 1/20 = 1.5a gives a = 1/30, so 30 days. No single statement fixes A's time, but any "
  "two do.",
  ["I alone: 1/A + 1/B = 1/12 — two unknowns", "II alone: only a ratio of rates", "III alone: says nothing about A",
   "I + II: 2.5/A = 1/12 ⇒ A = 30", "I + III: 1/A = 1/12 − 1/20 ⇒ A = 30", "II + III: 1/A = (1/20) ÷ 1.5 ⇒ A = 30"],
  why="'Only I and III together' misses that II with either of the other two also works; 'all three' is more data "
      "than needed.", secs=80, by=BRUTE)

sal_grid = range(100, 60001, 100)
s1_set = {s for s in sal_grid if F(70, 100) * F(60, 100) * s == 8400}
mohan = set(range(100, 60001, 100))
s2_set = {s for s in sal_grid if F(4, 5) * s in mohan}  # some Mohan salary m with s = 1.25m exists
s3_set = {s for s in sal_grid if (s - F(4, 5) * s) == 4000}
assert s1_set == {20000} and s3_set == {20000} and len(s2_set) > 1
assert s1_set & s3_set == {20000} and len(s2_set & s3_set) == 1
Q(T, "Three-statement", A,
  "The question below is followed by three statements. Decide which statements are sufficient to answer it.\n"
  "Question: What is Ravi's monthly salary?\n"
  "I. Ravi spends 30% of his salary on rent and 40% of the remainder on household expenses, and saves the rest, "
  "which is ₹8,400.\n"
  "II. Ravi's salary is 25% more than Mohan's salary.\n"
  "III. The salaries of Ravi and Sunil are in the ratio 5 : 4, and Sunil earns ₹4,000 less than Ravi.",
  "Either statement I alone or statement III alone is sufficient",
  ["Statement I alone is sufficient, but III alone is not", "Statement III alone is sufficient, but I alone is not",
   "Statements II and III together are needed"],
  "Check each statement alone before combining; a statement with a new unknown (Mohan) adds nothing by itself",
  "I: savings = S × 0.7 × 0.6 = 0.42S = 8,400, so S = ₹20,000 — sufficient. II: S = 1.25 × Mohan's salary, which is "
  "unknown — not sufficient. III: S − 0.8S = 0.2S = 4,000, so S = ₹20,000 — sufficient. So either I alone or III "
  "alone answers the question.",
  ["I: 0.70 × 0.60 × S = 0.42S = 8,400 ⇒ S = 20,000", "II: S = 1.25M with M unknown — not sufficient",
   "III: Sunil = 0.8S and S − 0.8S = 4,000 ⇒ S = 20,000", "Answer: either I alone or III alone"],
  why="'I alone' and 'III alone' each name only one of the two sufficient statements; II and III are not both "
      "needed because III alone works.", secs=110, by=BRUTE)

# ================================================================ checks and output
assert len(QUESTIONS) == TOTAL, len(QUESTIONS)
assert len(STIMULI) == 12

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_002_plan.json").read_text(encoding="utf-8"))
qa = next(s for s in plan["subjects"] if s["subject"] == SUBJECT)
have = Counter((q["topic"], q["difficulty"]) for q in QUESTIONS)
want = Counter({(t["topic"], d): n for t in qa["topics"] for d, n in t["quota"].items() if n})
assert have == want, set(have.items()) ^ set(want.items())
subs = {t["topic"]: set(t["subtopics"]) for t in qa["topics"]}
assert all(q["subtopic"] in subs[q["topic"]] for q in QUESTIONS)
assert QUESTIONS[0]["question_id"] == qa["question_ids"][0] and QUESTIONS[-1]["question_id"] == qa["question_ids"][1]
assert STIMULI[0]["stimulus_id"] == qa["stimulus_id_start"]
for s in STIMULI:  # every DI set has 3 to 5 questions
    assert 3 <= _set_pos[s["stimulus_id"]] <= 5, s["stimulus_id"]
keys = Counter(q["correct_answer"] for q in QUESTIONS)
assert keys == Counter({k: 50 for k in "ABCD"})

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_002",
    "created_at": TODAY,
    "notes": "BATCH_002, Quantitative Aptitude part: 200 original questions (60 Basic, 80 Intermediate, 60 Advanced) "
             "with 12 shared DI stimuli on new data sets. Every answer was recomputed by tools/batch_002/quant.py "
             "before writing. Pending human review.",
    "stimuli": STIMULI,
    "questions": QUESTIONS,
}
out = ROOT / "batches" / "parts" / "BATCH_002_QUANT.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(QUESTIONS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(keys.items()))})")
