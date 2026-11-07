"""Writes batches/parts/BATCH_003_QUANT.json: the 200 Quantitative Aptitude questions of BATCH_003.

Every answer is recomputed here before the file is written: arithmetic with exact fractions, series regenerated
from their rule (wrong-number series: exactly one term differs from the regenerated series), quadratic roots
substituted back into the equations, probabilities and arrangements counted by brute force, data-sufficiency
statements checked by enumerating candidate values, approximation answers checked to be the option nearest the
exact value by a clear margin. If any assertion fails, nothing is written.

The structure and helpers follow tools/batch_002/quant.py (relation-option guards, balanced key shuffler with a new
seed). Contexts, data sets and number templates are new: none of the DI themes of batches 0-2 is reused.

    python tools/batch_003/quant.py          (run from docs/question-bank)
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

# Balanced answer keys: exactly 50 of each letter, order fixed by the seed (new seed for batch 3).
_rng = random.Random(20261105 + 3)
KEYS = list("ABCD" * (TOTAL // 4))
_rng.shuffle(KEYS)

QUESTIONS, STIMULI = [], []
_set_pos = {}
_FIRST_ID = 406
_FIRST_STIM = 3001
RECOMPUTE = ["script:recompute", "ai:author-solve"]
BRUTE = ["script:recompute", "script:brute-force-unique", "ai:author-solve"]

# Questions that a separate solver re-answered from the stem and options alone (no key, no solution) and whose
# answer matched the key. Only these carry ai:independent-check. See the batch report for the method.
# 50 questions (every fourth question, BANK_QUANT_000407 to _000603) were given to a separate solver as stems,
# options and data sets only; all 50 of its answers matched the key.
INDEPENDENT = {f"BANK_QUANT_{n:06d}" for n in range(407, 606, 4)}

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

# ================================================================ Simplification (B6 I2 A2)
T = "Simplification"
v = 18 * 5 - F(216, 8) + 13 * 4
assert v == 115 and 90 - 27 - 52 == 11 and 90 + 27 + 52 == 169 and 90 - 27 == 63
Q(T, "BODMAS", B, "Simplify: 18 × 5 − 216 ÷ 8 + 13 × 4 = ?",
  "115", ["11", "169", "63"],
  "BODMAS: multiplication and division before addition and subtraction, then left to right",
  "Work out the products and the quotient first: 18 × 5 = 90, 216 ÷ 8 = 27 and 13 × 4 = 52. Then, left to right, "
  "90 − 27 + 52 = 115.",
  ["18 × 5 = 90", "216 ÷ 8 = 27", "13 × 4 = 52", "90 − 27 + 52 = 115"],
  why="11 subtracts the 52 as well (90 − 27 − 52); 169 adds the 27; 63 stops after 90 − 27.", secs=30)

q_ = 12 ** 2 + 3 * 26 - F(35, 100) * 480
assert q_ == 54 and 222 + 168 == 390 and 222 - F(40, 100) * 480 == 30
Q(T, "BODMAS", B, "What will come in place of the question mark (?)?\n35% of 480 + ? = 12² + 3 × 26",
  "54", ["390", "222", "30"],
  "Evaluate both sides fully, then move the known term across the equals sign",
  "Left side: 35% of 480 = 168. Right side: 12² + 3 × 26 = 144 + 78 = 222. So 168 + ? = 222 and ? = 54.",
  ["35% of 480 = 0.35 × 480 = 168", "12² + 3 × 26 = 144 + 78 = 222", "? = 222 − 168 = 54"],
  why="390 adds 168 to 222 instead of subtracting; 222 forgets the 168 on the left; 30 takes 40% of 480 (192).",
  secs=40)

v = F(125, 100) * F(64, 10) - F(10, 3) * F(18, 10) + F(45, 10) / F(15, 100)
assert v == 32 and 8 + 6 + 30 == 44 and 8 - 6 + F(45, 10) * F(15, 100) == F(2675, 1000) and 30 - 6 == 24
Q(T, "Fractions and decimals", B, "1.25 × 6.4 − 3⅓ of 1.8 + 4.5 ÷ 0.15 = ?",
  "32", ["44", "2.675", "24"],
  "'of' means multiply; dividing by a decimal is multiplying by its reciprocal",
  "1.25 × 6.4 = 8. 3⅓ of 1.8 = 10/3 × 1.8 = 6. 4.5 ÷ 0.15 = 450 ÷ 15 = 30. So 8 − 6 + 30 = 32.",
  ["1.25 × 6.4 = 8", "3⅓ × 1.8 = 10/3 × 9/5 = 6", "4.5 ÷ 0.15 = 450 ÷ 15 = 30", "8 − 6 + 30 = 32"],
  why="44 adds the 6; 2.675 multiplies 4.5 by 0.15 instead of dividing; 24 drops the first term (8).", secs=40)

v = F(21, 5) / F(14, 10) + F(21, 8) * F(8, 10) - F(8, 5)
assert v == F(7, 2)
assert F(21, 5) * F(14, 10) + F(21, 10) - F(8, 5) == F(638, 100) and 3 + F(21, 10) + F(8, 5) == F(67, 10)
assert 3 + F(21, 10) == F(51, 10)
Q(T, "Fractions and decimals", B, "4⅕ ÷ 1.4 + 2⅝ × 0.8 − 1⅗ = ?",
  "3.5", ["6.7", "6.38", "5.1"],
  "Convert mixed numbers to fractions or decimals; ÷ and × before + and −",
  "4⅕ ÷ 1.4 = 4.2 ÷ 1.4 = 3. 2⅝ × 0.8 = 2.625 × 0.8 = 2.1. 1⅗ = 1.6. So 3 + 2.1 − 1.6 = 3.5.",
  ["4⅕ = 4.2; 4.2 ÷ 1.4 = 3", "2⅝ = 2.625; 2.625 × 0.8 = 2.1", "1⅗ = 1.6", "3 + 2.1 − 1.6 = 3.5"],
  why="6.7 adds the 1.6; 6.38 multiplies 4.2 by 1.4 (5.88); 5.1 leaves out the − 1⅗.", secs=45)

assert 56 ** 2 == 3136 and 14 ** 3 == 2744 and F(16, 100) ** 2 == F(256, 10000)
v = 56 - 14 + F(16, 100) * 50
assert v == 50 and 56 - 14 + F(16, 10) * 50 == 122 and 56 - 14 - 8 == 34 and 56 + 14 + 8 == 78
Q(T, "Square and cube roots", B, "√3136 − ∛2744 + √0.0256 × 50 = ?",
  "50", ["122", "34", "78"],
  "Roots of perfect squares and cubes; the square root of a decimal has half as many decimal places",
  "√3136 = 56, ∛2744 = 14 and √0.0256 = 0.16. Then 0.16 × 50 = 8, and 56 − 14 + 8 = 50.",
  ["√3136 = 56 (56² = 3,136)", "∛2744 = 14 (14³ = 2,744)", "√0.0256 = 0.16 (four decimal places → two)",
   "0.16 × 50 = 8", "56 − 14 + 8 = 50"],
  short="3136 ends in 6 and lies between 55² = 3025 and 60² = 3600, so its root is 56 (54 is too small).",
  why="122 takes √0.0256 as 1.6; 34 subtracts the 8; 78 adds ∛2744 instead of subtracting it.", secs=45)

v = F(6 ** 4 * 36 ** 2, 216 ** 2)
assert v == 36 and 36 ** 2 == 6 ** 4 and 216 ** 2 == 6 ** 6
Q(T, "Surds and indices", B, "Find the value of (6⁴ × 36²) ÷ 216².",
  "36", ["6", "216", "1,296"],
  "Write every term as a power of the same base: aᵐ × aⁿ = aᵐ⁺ⁿ and aᵐ ÷ aⁿ = aᵐ⁻ⁿ",
  "36² = (6²)² = 6⁴ and 216² = (6³)² = 6⁶. So the expression is 6⁴ × 6⁴ ÷ 6⁶ = 6⁴⁺⁴⁻⁶ = 6² = 36.",
  ["36 = 6², so 36² = 6⁴", "216 = 6³, so 216² = 6⁶", "6⁴ × 6⁴ ÷ 6⁶ = 6²", "6² = 36"],
  why="6, 216 and 1,296 (6¹, 6³ and 6⁴) come from writing 36² as 6³, 6⁵ or 6⁶ by mistake, or from multiplying "
      "instead of adding the powers.", secs=40)

r11, r7 = math.sqrt(11), math.sqrt(7)
v = (r11 + r7) / (r11 - r7) + (r11 - r7) / (r11 + r7)
assert near(v, 9) and F(2 * (11 + 7), 11 - 7) == 9
Q(T, "Surds and indices", I, "Simplify: (√11 + √7)/(√11 − √7) + (√11 − √7)/(√11 + √7)",
  "9", ["18", "4.5", "36"],
  "Add the two fractions over the common denominator (√11 − √7)(√11 + √7) = 11 − 7",
  "The common denominator is (√11)² − (√7)² = 4. The numerator is (√11 + √7)² + (√11 − √7)² = 2(11 + 7) = 36. "
  "So the value is 36 ÷ 4 = 9.",
  ["Denominator: (√11 − √7)(√11 + √7) = 11 − 7 = 4", "(√11 + √7)² = 18 + 2√77; (√11 − √7)² = 18 − 2√77",
   "Numerator = 36 (the √77 terms cancel)", "36 ÷ 4 = 9"],
  short="(a + b)/(a − b) + (a − b)/(a + b) = 2(a² + b²)/(a² − b²) = 2 × 18 ÷ 4 = 9.",
  why="18 divides by 2 instead of 4; 4.5 divides by 8; 36 forgets the denominator.", secs=60)

assert F(9, 100) ** 3 == F(729, 1000000) and F(9, 100) ** 2 == F(81, 10000) and F(5, 4) ** 2 == F(25, 16)
v = F(9, 100) / F(9, 100) + F(5, 4)
assert v == F(9, 4) and F(9, 10) / F(9, 100) + F(5, 4) == F(45, 4) and 1 + F(7, 4) == F(11, 4)
Q(T, "Square and cube roots", I, "∛0.000729 ÷ √0.0081 + √(1 9/16) = ?",
  "2.25", ["11.25", "2.75", "1.25"],
  "The cube root of a decimal has one-third as many decimal places; write a mixed number as an improper fraction "
  "before taking its root",
  "∛0.000729 = 0.09 (six decimal places → two), √0.0081 = 0.09 and 1 9/16 = 25/16, whose root is 5/4 = 1.25. "
  "So 0.09 ÷ 0.09 + 1.25 = 1 + 1.25 = 2.25.",
  ["∛0.000729 = 0.09 (0.09³ = 0.000729)", "√0.0081 = 0.09", "1 9/16 = 25/16 ⇒ √ = 5/4 = 1.25",
   "0.09 ÷ 0.09 + 1.25 = 2.25"],
  why="11.25 takes ∛0.000729 as 0.9; 2.75 takes √(1 9/16) as 1 + ¾; 1.25 drops the quotient 1.", secs=55)

r3_, r7_ = math.sqrt(3), math.sqrt(7)
assert near((r7_ + r3_) ** 2, 10 + 2 * math.sqrt(21)) and near((r7_ - r3_) ** 2, 10 - 2 * math.sqrt(21))
v = math.sqrt(10 + 2 * math.sqrt(21)) - math.sqrt(10 - 2 * math.sqrt(21))
assert near(v, 2 * r3_)
Q(T, "Surds and indices", A, "Find the value of √(10 + 2√21) − √(10 − 2√21).",
  "2√3", ["2√7", "2√10", "0"],
  "√(a + b ± 2√ab) = √a ± √b (with √a > √b): find two numbers whose sum is 10 and product is 21",
  "7 + 3 = 10 and 7 × 3 = 21, so 10 + 2√21 = (√7 + √3)² and 10 − 2√21 = (√7 − √3)². Since √7 > √3, the roots "
  "are √7 + √3 and √7 − √3, and their difference is 2√3.",
  ["Need a + b = 10 and ab = 21 ⇒ a = 7, b = 3", "√(10 + 2√21) = √7 + √3", "√(10 − 2√21) = √7 − √3 (positive, "
   "since √7 > √3)", "(√7 + √3) − (√7 − √3) = 2√3"],
  why="2√7 is the sum of the two roots, not the difference; 2√10 treats √(10 ± 2√21) as √10 ± something that "
      "cancels the wrong way; 0 assumes the two roots are equal.", secs=80)

v = sum(F(1, (2 * k - 1) * (2 * k + 1)) for k in range(1, 11))
assert v == F(10, 21) and F(1, 2) * (1 - F(1, 21)) == v
Q(T, "Fractions and decimals", A, "Find the value of 1/(1 × 3) + 1/(3 × 5) + 1/(5 × 7) + … + 1/(19 × 21).",
  "10/21", ["20/21", "11/21", "10/19"],
  "Telescoping: 1/(n(n + 2)) = ½ × (1/n − 1/(n + 2))",
  "Each term splits as ½(1/n − 1/(n + 2)). Adding from n = 1 to n = 19 (odd n only), the middle terms cancel and "
  "the sum is ½(1 − 1/21) = ½ × 20/21 = 10/21.",
  ["1/(1 × 3) = ½(1 − 1/3), 1/(3 × 5) = ½(1/3 − 1/5), …, 1/(19 × 21) = ½(1/19 − 1/21)",
   "All middle terms cancel", "Sum = ½(1 − 1/21) = ½ × 20/21", "= 10/21"],
  why="20/21 forgets the factor ½; 11/21 adds 1/21 instead of subtracting it; 10/19 stops the series at 1/19.",
  secs=80)

# ================================================================ Approximation (B2 I5 A6)
T = "Approximation"
exact = 0.1998 * 1450.3 + 0.3202 * 624.9
nearest(exact, [490, 520, 460, 550], 490)
Q(T, "Percentage approximation", B, APPROX + "19.98% of 1450.3 + 32.02% of 624.9 ≈ ?",
  "490", ["520", "460", "550"],
  "Round each percentage and each number to the nearest convenient value",
  "19.98% ≈ 20% and 1450.3 ≈ 1450, so the first term ≈ 290. 32.02% ≈ 32% and 624.9 ≈ 625, so the second term ≈ "
  "200. Total ≈ 490.",
  ["20% of 1450 = 290", "32% of 625 = 200", "290 + 200 = 490"],
  short="32% of 625 = 625 × 8/25 = 200.", why="The other options are 30 or more away from the true value (≈ 489.9).",
  secs=40)

exact = 36.98 * 14.02 - math.sqrt(1368.7)
nearest(exact, [481, 455, 505, 518], 481)
Q(T, "Mixed approximation", B, APPROX + "36.98 × 14.02 − √1368.7 ≈ ?",
  "481", ["455", "505", "518"],
  "Round factors to whole numbers and the radicand to the nearest perfect square",
  "36.98 × 14.02 ≈ 37 × 14 = 518. √1368.7 ≈ √1369 = 37. So the value ≈ 518 − 37 = 481.",
  ["37 × 14 = 518", "√1369 = 37", "518 − 37 = 481"],
  why="518 forgets to subtract the root; 455 and 505 are more than 20 away from the exact value (≈ 481.5).",
  secs=40)

exact = ((1000 - (34.98 ** 2 - 21.02 ** 2)) / 8.97) ** 2
nearest(exact, [576, 484, 676, 729], 576)
Q(T, "Root approximation", I, APPROX + "√? × 8.97 + 34.98² − 21.02² ≈ 1000",
  "576", ["484", "676", "729"],
  "Difference of squares: a² − b² = (a + b)(a − b)",
  "34.98² − 21.02² ≈ 35² − 21² = (35 + 21)(35 − 21) = 56 × 14 = 784. So √? × 9 ≈ 1000 − 784 = 216, √? ≈ 24 and "
  "? ≈ 576.",
  ["35² − 21² = 56 × 14 = 784", "√? × 9 ≈ 216", "√? ≈ 24", "? ≈ 24² = 576"],
  why="484 (22²) and 676 (26²) come from rounding 216 ÷ 9 the wrong way; 729 squares 27.", secs=60)

exact = 0.6497 * 360.2 + 1.3502 * 79.98
nearest(exact, [342, 322, 362, 382], 342)
Q(T, "Percentage approximation", I, APPROX + "64.97% of 360.2 + 135.02% of 79.98 ≈ ?",
  "342", ["322", "362", "382"],
  "A percentage above 100 multiplies by more than 1",
  "64.97% of 360.2 ≈ 65% of 360 = 234. 135.02% of 79.98 ≈ 1.35 × 80 = 108. Total ≈ 342.",
  ["65% of 360 = 234", "135% of 80 = 108", "234 + 108 = 342"],
  why="322 and 362 are 20 away and 382 is 40 away from the exact value (about 342.0).", secs=50)

exact = 2449.8 / 34.97 * 4.98 + 11.02 ** 3
nearest(exact, [1681, 1621, 1741, 1801], 1681)
Q(T, "Mixed approximation", I, APPROX + "(2449.8 ÷ 34.97) × 4.98 + 11.02³ ≈ ?",
  "1681", ["1621", "1741", "1801"],
  "Round each number, keep the order of operations, and remember 11³ = 1,331",
  "2449.8 ÷ 34.97 ≈ 2450 ÷ 35 = 70; 70 × 5 = 350. 11.02³ ≈ 11³ = 1,331. Total ≈ 350 + 1,331 = 1,681.",
  ["2450 ÷ 35 = 70", "70 × 5 = 350", "11³ = 1,331", "350 + 1,331 = 1,681"],
  why="1,621 and 1,741 are 60 away and 1,801 is 120 away from the value (about 1,687).", secs=55)

exact = math.sqrt(783.9) * 1727.6 ** (1 / 3) / 8.03 + 6.98 ** 2
nearest(exact, [91, 84, 98, 105], 91)
Q(T, "Root approximation", I, APPROX + "√783.9 × ∛1727.6 ÷ 8.03 + 6.98² ≈ ?",
  "91", ["84", "98", "105"],
  "Nearest perfect square and perfect cube: 784 = 28², 1728 = 12³",
  "√783.9 ≈ 28 and ∛1727.6 ≈ 12, so 28 × 12 ÷ 8 = 42. 6.98² ≈ 49. Total ≈ 42 + 49 = 91.",
  ["√784 = 28", "∛1728 = 12", "28 × 12 ÷ 8 = 42", "7² = 49", "42 + 49 = 91"],
  why="84 uses 7 × 6 for the last term; 98 doubles 49; 105 divides 28 × 12 by 6 instead of 8.",
  secs=55)

exact = 18.02 * 25.03 - (3 / 7 * 1679.8 - 5 / 9 * 539.9)
nearest(exact, [31, 51, 11, 71], 31)
Q(T, "Mixed approximation", I, APPROX + "3/7 of 1679.8 − 5/9 of 539.9 + ? ≈ 18.02 × 25.03",
  "31", ["51", "11", "71"],
  "Round the numbers so the fractions divide exactly: 1680 ÷ 7 and 540 ÷ 9",
  "3/7 of 1680 = 720. 5/9 of 540 = 300. 18 × 25 = 450. So 720 − 300 + ? = 450 and ? = 30, closest to 31 "
  "(the exact value is about 31.1).",
  ["3/7 × 1680 = 3 × 240 = 720", "5/9 × 540 = 5 × 60 = 300", "18 × 25 = 450", "? ≈ 450 − 420 = 30 ≈ 31"],
  why="51, 11 and 71 are each 20 or more away from the exact value.", secs=60)

exact = math.sqrt(1249.8 / 24.97 * 6.01 + math.sqrt(2024.7) * 3.02 - 291)
nearest(exact, [12, 9, 15, 18], 12)
Q(T, "Mixed approximation", A, APPROX + "1249.8 ÷ 24.97 × 6.01 + √2024.7 × 3.02 − ?² ≈ 291",
  "12", ["9", "15", "18"],
  "Round, solve for ?², then take the positive root (all options are positive)",
  "1249.8 ÷ 24.97 ≈ 1250 ÷ 25 = 50; 50 × 6 = 300. √2024.7 ≈ √2025 = 45; 45 × 3 = 135. So 300 + 135 − ?² ≈ 291, "
  "giving ?² ≈ 144 and ? ≈ 12.",
  ["1250 ÷ 25 × 6 = 300", "√2025 × 3 = 45 × 3 = 135", "435 − ?² = 291 ⇒ ?² = 144", "? = 12"],
  why="9 and 15 give ?² = 81 or 225, far from 144; 18 takes ?² = 324.", secs=90)

exact = (0.625 * 1919.8 + 4.02 ** 3) / 16.04
nearest(exact, [79, 74, 84, 89], 79)
Q(T, "Percentage approximation", A, APPROX + "(62.5% of 1919.8 + 4.02³) ÷ 16.04 ≈ ?",
  "79", ["74", "84", "89"],
  "62.5% = 5/8; 4³ = 64",
  "62.5% of 1920 = 5/8 × 1920 = 1,200. 4.02³ ≈ 64. (1,200 + 64) ÷ 16 = 1,264 ÷ 16 = 79.",
  ["5/8 × 1920 = 1,200", "4³ = 64", "1,264 ÷ 16 = 79"],
  why="74 and 84 are 5 away from the value and 89 is 10 away; leaving out 4³ gives 75, which is still not 74.",
  secs=75)

exact = (23.02 ** 2 - math.sqrt(6399.4) + 16.97 * 4.98) * 7.98 / 12.03
nearest(exact, [356, 324, 388, 420], 356)
Q(T, "Mixed approximation", A, APPROX + "? ÷ 7.98 × 12.03 ≈ 23.02² − √6399.4 + 16.97 × 4.98",
  "356", ["324", "388", "420"],
  "Simplify the right side first, then undo ÷ 8 × 12 (that is, × 1.5)",
  "Right side ≈ 23² − √6400 + 17 × 5 = 529 − 80 + 85 = 534. Then ? × 12 ÷ 8 = ? × 1.5 ≈ 534, so ? ≈ 356.",
  ["23² = 529", "√6400 = 80", "17 × 5 = 85", "529 − 80 + 85 = 534", "? = 534 ÷ 1.5 = 356"],
  why="324, 388 and 420 are each 30 or more away from the exact value (about 354.5).",
  secs=90)

exact = (22.03 - math.sqrt(48.97)) ** 2 - 12.98 ** 2
nearest(exact, [56, 46, 66, 76], 56)
Q(T, "Root approximation", A, APPROX + "√(? + 12.98²) ≈ 22.03 − √48.97",
  "56", ["46", "66", "76"],
  "Square both sides after rounding",
  "√48.97 ≈ 7, so the right side ≈ 22 − 7 = 15. Squaring, ? + 13² ≈ 225, so ? ≈ 225 − 169 = 56.",
  ["√49 = 7", "22 − 7 = 15", "? + 169 = 225", "? = 56"],
  why="46, 66 and 76 are each at least 8 away from the exact value (about 57.5).", secs=80)

num = 8.99 ** 3 - 7.02 ** 3
den = 8.98 ** 2 + 9.01 * 6.97 + 7.03 ** 2
exact = num / den + 0.5502 * 399.8
nearest(exact, [222, 238, 206, 191], 222)
Q(T, "Mixed approximation", A, APPROX + "(8.99³ − 7.02³) ÷ (8.98² + 9.01 × 6.97 + 7.03²) + 55.02% of 399.8 ≈ ?",
  "222", ["238", "206", "191"],
  "a³ − b³ = (a − b)(a² + ab + b²), so the first fraction is about a − b",
  "With a ≈ 9 and b ≈ 7, the fraction is (9³ − 7³) ÷ (9² + 9 × 7 + 7²) = 9 − 7 = 2. 55% of 400 = 220. "
  "Total ≈ 222.",
  ["(9³ − 7³) = 729 − 343 = 386", "9² + 63 + 7² = 193", "386 ÷ 193 = 2 (= 9 − 7)", "55% of 400 = 220",
   "2 + 220 = 222"],
  short="Recognise the identity instead of cubing: the fraction is just 9 − 7.",
  why="238 and 206 are 16 away and 191 is 31 away; working out the cubes in full wastes time but gives the same "
      "2.", secs=90)

exact = (41.98 ** 2 - 2.03 * 5.98 - 20.97 * 19.02) ** (1 / 3)
nearest(exact, [11, 9, 13, 15], 11)
Q(T, "Root approximation", A, APPROX + "?³ + 20.97 × 19.02 ≈ 41.98² − 2.03 × 5.98",
  "11", ["9", "13", "15"],
  "Solve for ?³, then find the nearest perfect cube",
  "41.98² − 2.03 × 5.98 ≈ 42² − 2 × 6 = 1,764 − 12 = 1,752. 20.97 × 19.02 ≈ 21 × 19 = 399. So ?³ ≈ 1,752 − 399 = "
  "1,353, and the nearest cube is 1,331 = 11³.",
  ["42² = 1,764", "1,764 − 12 = 1,752", "21 × 19 = 399", "?³ ≈ 1,353 ≈ 11³ = 1,331", "? ≈ 11"],
  why="9³ = 729, 13³ = 2,197 and 15³ = 3,375 are far from 1,353.", secs=80)

# ================================================================ Number Series (B3 I7 A4)
T = "Number Series"
SERIES_Q = "What will come in place of the question mark (?) in the following series?\n"


def series_from(start, step, n):
    out = [start]
    for k in range(1, n):
        out.append(step(out[-1], k))
    return out


def diffs(seq):
    return [b - a for a, b in zip(seq, seq[1:])]


s = series_from(17, lambda t, k: t + [2, 3, 5, 7, 11, 13][k - 1], 7)
assert s == [17, 19, 22, 27, 34, 45, 58]
Q(T, "Pattern: differences", B, SERIES_Q + "17, 19, 22, 27, 34, 45, ?",
  "58", ["56", "60", "62"],
  "The differences are consecutive prime numbers",
  "The differences are 2, 3, 5, 7, 11, the primes in order. The next prime is 13, so the next term is 45 + 13 = 58.",
  ["19 − 17 = 2, 22 − 19 = 3, 27 − 22 = 5", "34 − 27 = 7, 45 − 34 = 11", "Next prime = 13", "45 + 13 = 58"],
  why="56 adds 11 again; 60 adds 15 (odd numbers instead of primes); 62 adds 17, skipping 13.", secs=30)

s = series_from(5, lambda t, k: t + k * k, 7)
assert s == [5, 6, 10, 19, 35, 60, 96]
Q(T, "Pattern: squares and cubes", B, SERIES_Q + "5, 6, 10, 19, 35, 60, ?",
  "96", ["92", "85", "97"],
  "The differences are perfect squares 1², 2², 3², …",
  "The differences are 1, 4, 9, 16, 25 = 1², 2², 3², 4², 5². The next difference is 6² = 36, so the next term is "
  "60 + 36 = 96.",
  ["6 − 5 = 1, 10 − 6 = 4, 19 − 10 = 9", "35 − 19 = 16, 60 − 35 = 25", "Next: 6² = 36", "60 + 36 = 96"],
  why="92 adds 32; 85 adds 25 again; 97 adds 37.", secs=35)

s = series_from(3, lambda t, k: 2 * t + k, 6)
assert s == [3, 7, 16, 35, 74, 153]
Q(T, "Pattern: multiply-add", B, SERIES_Q + "3, 7, 16, 35, 74, ?",
  "153", ["149", "151", "148"],
  "Each term = previous × 2 + a number that rises by 1 (1, 2, 3, …)",
  "3 × 2 + 1 = 7, 7 × 2 + 2 = 16, 16 × 2 + 3 = 35, 35 × 2 + 4 = 74, so the next is 74 × 2 + 5 = 153.",
  ["3 × 2 + 1 = 7", "7 × 2 + 2 = 16", "16 × 2 + 3 = 35", "35 × 2 + 4 = 74", "74 × 2 + 5 = 153"],
  why="149 adds 1 after doubling (74 × 2 + 1); 151 adds 3; 148 only doubles.", secs=40)

s = series_from(4, lambda t, k: t * k + (k + 1), 6)
assert s == [4, 6, 15, 49, 201, 1011]
Q(T, "Missing number series", I, "Find the missing number (?) in the series:\n4, 6, 15, 49, ?, 1011",
  "201", ["196", "205", "199"],
  "Multiplier rises 1, 2, 3, … and the number added rises 2, 3, 4, …",
  "4 × 1 + 2 = 6, 6 × 2 + 3 = 15, 15 × 3 + 4 = 49, 49 × 4 + 5 = 201 and 201 × 5 + 6 = 1,011, which confirms it.",
  ["4 × 1 + 2 = 6", "6 × 2 + 3 = 15", "15 × 3 + 4 = 49", "49 × 4 + 5 = 201", "Check: 201 × 5 + 6 = 1,011"],
  why="196 is 49 × 4 with no addition; 205 and 199 do not give 1,011 at the next step.", secs=55)

s = [8]
for d_ in [4, 12, 24, 40, 60]:
    s.append(s[-1] + d_)
assert s == [8, 12, 24, 48, 88, 148] and diffs(diffs(s)) == [8, 12, 16, 20]
Q(T, "Pattern: differences", I, SERIES_Q + "8, 12, 24, 48, 88, ?",
  "148", ["136", "152", "144"],
  "Two-level differences: the second differences rise by 4",
  "First differences: 4, 12, 24, 40. Second differences: 8, 12, 16, so the next second difference is 20 and the "
  "next first difference is 40 + 20 = 60. The next term is 88 + 60 = 148.",
  ["Differences: 4, 12, 24, 40", "Second differences: 8, 12, 16 → next 20", "Next difference = 60",
   "88 + 60 = 148"],
  why="136 adds 48 (differences treated as doubling); 152 adds 64; 144 adds 56.", secs=60)

s = [k ** 2 if k % 2 else k ** 3 for k in range(1, 8)]
assert s == [1, 8, 9, 64, 25, 216, 49]
Q(T, "Pattern: squares and cubes", I, SERIES_Q + "1, 8, 9, 64, 25, 216, ?",
  "49", ["36", "343", "125"],
  "Alternate positions follow different rules: odd positions are squares, even positions are cubes",
  "Position n holds n² when n is odd and n³ when n is even: 1², 2³, 3², 4³, 5², 6³. The 7th term is 7² = 49.",
  ["1 = 1², 8 = 2³", "9 = 3², 64 = 4³", "25 = 5², 216 = 6³", "7th term = 7² = 49"],
  why="343 = 7³ ignores the alternation; 36 = 6² and 125 = 5³ use the wrong base.", secs=55)

s = series_from(5, lambda t, k: t + (2 * k) ** 2, 6)
assert s == [5, 9, 25, 61, 125, 225]
Q(T, "Pattern: squares and cubes", I, SERIES_Q + "5, 9, 25, 61, 125, ?",
  "225", ["221", "189", "215"],
  "The differences are squares of even numbers: 2², 4², 6², …",
  "The differences are 4, 16, 36, 64 = 2², 4², 6², 8². The next is 10² = 100, so the term is 125 + 100 = 225.",
  ["9 − 5 = 4 = 2²", "25 − 9 = 16 = 4²", "61 − 25 = 36 = 6²", "125 − 61 = 64 = 8²", "125 + 10² = 225"],
  why="221 adds 96; 189 adds 64 again; 215 adds 90.", secs=55)

s = series_from(3, lambda t, k: t + 3 ** (k - 1), 6)
assert s == [3, 4, 7, 16, 43, 124]
Q(T, "Pattern: differences", I, SERIES_Q + "3, 4, 7, 16, 43, ?",
  "124", ["129", "115", "132"],
  "The differences are powers of 3",
  "The differences are 1, 3, 9, 27 = 3⁰, 3¹, 3², 3³. The next difference is 81, so the term is 43 + 81 = 124.",
  ["4 − 3 = 1", "7 − 4 = 3", "16 − 7 = 9", "43 − 16 = 27", "43 + 81 = 124"],
  short="Equivalently, each term = previous × 3 − 5, 8, 14, …; the difference rule is quicker.",
  why="129 = 43 × 3; 115 adds 72; 132 adds 89.", secs=55)

s = series_from(4, lambda t, k: 2 * t + 3 if k % 2 else 3 * t + 2, 6)
assert s == [4, 11, 35, 73, 221, 445]
Q(T, "Pattern: multiply-add", I, SERIES_Q + "4, 11, 35, 73, 221, ?",
  "445", ["443", "665", "447"],
  "Two operations alternate: × 2 + 3, then × 3 + 2",
  "4 × 2 + 3 = 11, 11 × 3 + 2 = 35, 35 × 2 + 3 = 73, 73 × 3 + 2 = 221, so next is 221 × 2 + 3 = 445.",
  ["4 × 2 + 3 = 11", "11 × 3 + 2 = 35", "35 × 2 + 3 = 73", "73 × 3 + 2 = 221", "221 × 2 + 3 = 445"],
  why="665 applies × 3 + 2 twice in a row; 443 and 447 add 1 or 5 after doubling.", secs=60)

s = [k * k - 1 for k in range(11, 17)]
assert s == [120, 143, 168, 195, 224, 255]
Q(T, "Missing number series", I, "Find the missing number (?) in the series:\n120, ?, 168, 195, 224, 255",
  "143", ["144", "145", "142"],
  "Each term is one less than a perfect square",
  "120 = 11² − 1, 168 = 13² − 1, 195 = 14² − 1, 224 = 15² − 1 and 255 = 16² − 1, so the missing term is "
  "12² − 1 = 143. The differences 23, 25, 27, 29, 31 confirm it.",
  ["120 = 121 − 1", "? = 144 − 1 = 143", "168 = 169 − 1", "Differences 23, 25, 27, 29, 31 are consecutive odd "
   "numbers"],
  why="144 is 12² itself; 145 and 142 break the odd-number differences.", secs=45)

s = series_from(2, lambda t, k: t + k ** 3, 6)
assert s == [2, 3, 11, 38, 102, 227]
Q(T, "Pattern: squares and cubes", A, SERIES_Q + "2, 3, 11, 38, 102, ?",
  "227", ["218", "230", "226"],
  "The differences are perfect cubes 1³, 2³, 3³, …",
  "The differences are 1, 8, 27, 64 = 1³, 2³, 3³, 4³. The next is 5³ = 125, so the term is 102 + 125 = 227.",
  ["3 − 2 = 1", "11 − 3 = 8", "38 − 11 = 27", "102 − 38 = 64", "102 + 125 = 227"],
  why="218 adds 116; 230 adds 128 (2⁷); 226 adds 124.", secs=70)

s = series_from(F(7), lambda t, k: t * F(k, 2) + F(k, 2), 7)
assert s == [7, 4, 5, 9, 20, F(105, 2), F(321, 2)]
Q(T, "Pattern: multiply-add", A, SERIES_Q + "7, 4, 5, 9, 20, 52.5, ?",
  "160.5", ["157.5", "158", "162"],
  "Multiplier and addend rise together by 0.5: × 0.5 + 0.5, × 1 + 1, × 1.5 + 1.5, …",
  "7 × 0.5 + 0.5 = 4, 4 × 1 + 1 = 5, 5 × 1.5 + 1.5 = 9, 9 × 2 + 2 = 20, 20 × 2.5 + 2.5 = 52.5, so the next is "
  "52.5 × 3 + 3 = 160.5.",
  ["7 × 0.5 + 0.5 = 4", "4 × 1 + 1 = 5", "5 × 1.5 + 1.5 = 9", "9 × 2 + 2 = 20", "20 × 2.5 + 2.5 = 52.5",
   "52.5 × 3 + 3 = 160.5"],
  why="157.5 is 52.5 × 3 with nothing added; 158 and 162 do not follow either part of the rule.", secs=90)

s = series_from(3, lambda t, k: t * k + k * k, 6)
assert s == [3, 4, 12, 45, 196, 1005]
Q(T, "Missing number series", A, "Find the missing number (?) in the series:\n3, 4, 12, 45, ?, 1005",
  "196", ["184", "200", "192"],
  "Each term = previous × n + n², with n = 1, 2, 3, …",
  "3 × 1 + 1 = 4, 4 × 2 + 4 = 12, 12 × 3 + 9 = 45, 45 × 4 + 16 = 196, and 196 × 5 + 25 = 1,005 confirms it.",
  ["3 × 1 + 1² = 4", "4 × 2 + 2² = 12", "12 × 3 + 3² = 45", "45 × 4 + 4² = 196", "Check: 196 × 5 + 5² = 1,005"],
  why="184 adds 4 instead of 16; 200 and 192 do not lead to 1,005 (200 × 5 + 25 = 1,025).", secs=90)

s = [1, 3]
while len(s) < 6:
    s.append(3 * s[-1] - s[-2])
assert s == [1, 3, 8, 21, 55, 144]
Q(T, "Pattern: multiply-add", A, SERIES_Q + "1, 3, 8, 21, 55, ?",
  "144", ["89", "134", "155"],
  "Each term = 3 × (previous term) − (term before that)",
  "8 = 3 × 3 − 1, 21 = 3 × 8 − 3, 55 = 3 × 21 − 8, so the next term is 3 × 55 − 21 = 144. (These are alternate "
  "Fibonacci numbers.)",
  ["3 × 3 − 1 = 8", "3 × 8 − 3 = 21", "3 × 21 − 8 = 55", "3 × 55 − 21 = 144"],
  short="Differences 2, 5, 13, 34 are themselves alternate Fibonacci numbers; the next difference is 89.",
  why="89 is the next difference, not the next term; 134 and 155 use × 3 − 31 or × 3 − 10.", secs=90)

# ================================================================ Wrong Number Series (B1 I2 A2)
T = "Wrong Number Series"


def wrong_series(correct, shown):
    diff = [i for i, (a, b) in enumerate(zip(correct, shown)) if a != b]
    assert len(diff) == 1, (correct, shown)
    return shown[diff[0]], correct[diff[0]]


def series_text(seq):
    return ", ".join(N(x) for x in seq)


WRONG_Q = "Find the wrong number in the series:\n"
good = series_from(5, lambda t, k: 2 * t - 2, 7)
shown = [5, 8, 14, 27, 50, 98, 194]
assert wrong_series(good, shown) == (27, 26)
Q(T, "Find the wrong term", B, WRONG_Q + series_text(shown),
  "27", ["14", "50", "98"],
  "Each term = previous × 2 − 2",
  "5 × 2 − 2 = 8, 8 × 2 − 2 = 14, 14 × 2 − 2 = 26, 26 × 2 − 2 = 50, 50 × 2 − 2 = 98, 98 × 2 − 2 = 194. Only the "
  "fourth term breaks the rule: it should be 26, not 27.",
  ["5 × 2 − 2 = 8", "8 × 2 − 2 = 14", "14 × 2 − 2 = 26 ≠ 27", "26 × 2 − 2 = 50", "50 × 2 − 2 = 98; 98 × 2 − 2 = 194"],
  why="14, 50 and 98 all fit the rule once 27 is corrected to 26.", secs=40)

good = series_from(980, lambda t, k: t - 22 * k, 6)
shown = [980, 958, 914, 846, 760, 650]
assert good == [980, 958, 914, 848, 760, 650] and wrong_series(good, shown) == (846, 848)
Q(T, "Find the wrong term", I, WRONG_Q + series_text(shown),
  "846", ["914", "760", "958"],
  "The terms fall by multiples of 22: 22, 44, 66, …",
  "980 − 22 = 958, 958 − 44 = 914, 914 − 66 = 848, 848 − 88 = 760, 760 − 110 = 650. The fourth term should be "
  "848, not 846.",
  ["980 − 22 = 958", "958 − 44 = 914", "914 − 66 = 848 ≠ 846", "848 − 88 = 760", "760 − 110 = 650"],
  why="With 848 in place of 846, all the other terms fit; 760 only looks wrong because 846 − 760 = 86.", secs=50)

good = [p * p for p in (2, 3, 5, 7, 11, 13, 17)]
shown = [4, 9, 25, 49, 81, 169, 289]
assert wrong_series(good, shown) == (81, 121)
Q(T, "Find the wrong term", I, WRONG_Q + series_text(shown),
  "81", ["49", "169", "25"],
  "The terms are squares of consecutive prime numbers",
  "4, 9, 25, 49, 169 and 289 are 2², 3², 5², 7², 13² and 17². The fifth term should be 11² = 121; 81 = 9² is the "
  "square of a non-prime.",
  ["2² = 4, 3² = 9, 5² = 25, 7² = 49", "Next prime after 7 is 11 ⇒ 121, not 81", "13² = 169, 17² = 289"],
  why="49, 169 and 25 are squares of primes and fit the pattern.", secs=50)

good = series_from(3, lambda t, k: t * k + k, 7)
shown = [3, 4, 10, 33, 138, 685, 4116]
assert good == [3, 4, 10, 33, 136, 685, 4116] and wrong_series(good, shown) == (138, 136)
Q(T, "Find the wrong term", A, WRONG_Q + series_text(shown),
  "138", ["33", "685", "10"],
  "Each term = previous × n + n, with n = 1, 2, 3, …",
  "3 × 1 + 1 = 4, 4 × 2 + 2 = 10, 10 × 3 + 3 = 33, 33 × 4 + 4 = 136, 136 × 5 + 5 = 685, 685 × 6 + 6 = 4,116. The "
  "fifth term should be 136, not 138.",
  ["3 × 1 + 1 = 4", "4 × 2 + 2 = 10", "10 × 3 + 3 = 33", "33 × 4 + 4 = 136 ≠ 138", "136 × 5 + 5 = 685",
   "685 × 6 + 6 = 4,116"],
  why="685 looks wrong only if 138 is taken as correct (138 × 5 + 5 = 695); with 136 everything fits.", secs=80)

good = series_from(2, lambda t, k: 4 * t - 1, 7)
shown = [2, 7, 27, 109, 427, 1707, 6827]
assert good == [2, 7, 27, 107, 427, 1707, 6827] and wrong_series(good, shown) == (109, 107)
Q(T, "Find the wrong term", A, WRONG_Q + series_text(shown),
  "109", ["27", "427", "1,707"],
  "Each term = previous × 4 − 1",
  "2 × 4 − 1 = 7, 7 × 4 − 1 = 27, 27 × 4 − 1 = 107, 107 × 4 − 1 = 427, 427 × 4 − 1 = 1,707, "
  "1,707 × 4 − 1 = 6,827. The fourth term should be 107, not 109.",
  ["2 × 4 − 1 = 7", "7 × 4 − 1 = 27", "27 × 4 − 1 = 107 ≠ 109", "107 × 4 − 1 = 427", "427 × 4 − 1 = 1,707",
   "1,707 × 4 − 1 = 6,827"],
  why="427 would be wrong only if 109 were right (109 × 4 − 1 = 435).", secs=70)

# ================================================================ Quadratic Equations (B2 I1 A3)
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


xs, ys = [F(10), F(11)], [F(6), F(9)]
roots_check(1, -21, 110, xs), roots_check(1, -15, 54, ys)
qe("Relation between roots", B, "Solve the pair of equations given below. Which relation between x and y is true for every pair of roots?", "x² − 21x + 110 = 0", "y² − 15y + 54 = 0", xs, ys, ">", ["<", "<="],
   "Factorise by splitting the middle term; compare the smallest x with the largest y",
   "x = 10 or 11 and y = 6 or 9. The smallest x (10) is greater than the largest y (9), so x > y.",
   ["I: x² − 10x − 11x + 110 = (x − 10)(x − 11) = 0 ⇒ x = 10, 11",
    "II: y² − 6y − 9y + 54 = (y − 6)(y − 9) = 0 ⇒ y = 6, 9", "min x = 10 > max y = 9", "So x > y"],
   why="x < y and x ≤ y come from reading the root signs as negative.", secs=35)

xs, ys = [F(-5), F(-6)], [F(-3), F(-4)]
roots_check(1, 11, 30, xs), roots_check(1, 7, 12, ys)
qe("Relation between roots", B, "Find all the roots of equations I and II, then compare x with y.", "x² + 11x + 30 = 0", "y² + 7y + 12 = 0", xs, ys, "<", [">", ">="],
   "With all coefficients positive, both roots are negative",
   "x = −5 or −6 and y = −3 or −4. The largest x (−5) is smaller than the smallest y (−4), so x < y.",
   ["I: (x + 5)(x + 6) = 0 ⇒ x = −5, −6", "II: (y + 3)(y + 4) = 0 ⇒ y = −3, −4", "max x = −5 < min y = −4",
    "So x < y"],
   why="x > y comes from dropping the minus signs (5, 6 against 3, 4).", secs=40)

xs, ys = [F(2), F(5, 2)], [F(2), F(5, 3)]
roots_check(2, -9, 10, xs), roots_check(3, -11, 10, ys)
qe("Relation between roots", I, "Equations I and II below are quadratics in x and y. After solving them, mark the relation that always holds.", "2x² − 9x + 10 = 0", "3y² − 11y + 10 = 0", xs, ys, ">=", [">", "<"],
   "A shared root makes the relation non-strict",
   "x = 2 or 2.5 and y = 2 or 1.67. Every x is at least as large as every y, and x = y = 2 is possible, so x ≥ y.",
   ["I: 2x² − 4x − 5x + 10 = (x − 2)(2x − 5) = 0 ⇒ x = 2, 2.5",
    "II: 3y² − 6y − 5y + 10 = (y − 2)(3y − 5) = 0 ⇒ y = 2, 5/3", "x = 2, y = 2 gives x = y; all other pairs x > y",
    "So x ≥ y"],
   why="x > y misses the common root 2.", secs=55)

xs, ys = [F(3, 2), F(-4)], [F(-3, 2)]
roots_check(2, 5, -12, xs)
assert 5 * ys[0] - 2 == 2 * ys[0] - F(13, 2)
qe("Linear vs quadratic", A,
   "One equation below is quadratic and the other linear. Solve both and choose the correct relation between x "
   "and y.", "2x² + 5x − 12 = 0", "5y − 2 = 2y − 6.5", xs, ys, "cbe", [">", "<="],
   "Solve the linear equation directly; a quadratic root on each side of y means no relation holds",
   "I: x = 1.5 or −4. II: 3y = −4.5, so y = −1.5. x = 1.5 is greater than y but x = −4 is smaller, so the relation "
   "cannot be established.",
   ["I: 2x² + 8x − 3x − 12 = (x + 4)(2x − 3) = 0 ⇒ x = 1.5, −4", "II: 5y − 2y = −6.5 + 2 ⇒ 3y = −4.5 ⇒ y = −1.5",
    "x = 1.5 > −1.5; x = −4 < −1.5", "Relationship cannot be established"],
   why="x > y uses only the positive root 1.5; x ≤ y uses only −4.", secs=75)

xs = [3 * math.sqrt(2), 4 * math.sqrt(2)]
ys = [2 * math.sqrt(3), 4 * math.sqrt(3)]
for r in xs:
    assert near(r * r - 7 * math.sqrt(2) * r + 24, 0)
for r in ys:
    assert near(r * r - 6 * math.sqrt(3) * r + 24, 0)
assert relation([F(18), F(32)], [F(12), F(48)]) == "cbe" and relation(xs, ys) == "cbe"
qe("Relation between roots", A, "The equations below have irrational coefficients. Solve them and choose the relation between x and y, if any, that holds for all roots.", "x² − 7√2x + 24 = 0", "y² − 6√3y + 24 = 0", xs, ys, "cbe", ["<", ">="],
   "Quadratics with surd coefficients: find two roots from their sum and product",
   "For I, the roots have sum 7√2 and product 24: 3√2 and 4√2 (≈ 4.24 and 5.66). For II, the roots have sum 6√3 "
   "and product 24: 2√3 and 4√3 (≈ 3.46 and 6.93). x = 4.24 is above y = 3.46 but below y = 6.93, so no relation "
   "holds.",
   ["I: 3√2 + 4√2 = 7√2 and 3√2 × 4√2 = 24 ⇒ x = 3√2, 4√2", "II: 2√3 + 4√3 = 6√3 and 2√3 × 4√3 = 24 ⇒ y = 2√3, 4√3",
    "All roots are positive, so compare squares: x² ∈ {18, 32}, y² ∈ {12, 48}", "18 > 12 but 18 < 48",
    "Relationship cannot be established"],
   short="Compare the squares of the positive roots: 18, 32 against 12, 48.",
   why="x < y compares only 32 with 48; x ≥ y compares only 18 with 12.", secs=100)

xs, ys = [F(1, 2), F(2, 3)], [F(1, 3), F(1, 4)]
roots_check(6, -7, 2, xs), roots_check(12, -7, 1, ys)
qe("Relation between roots", A, "Both equations below have fractional roots. Determine the roots and select the correct relationship between x and y.", "6x² − 7x + 2 = 0", "12y² − 7y + 1 = 0", xs, ys, ">", ["<=", "<"],
   "Factorise with a ≠ 1 and compare fractional roots",
   "x = 1/2 or 2/3 and y = 1/3 or 1/4. The smallest x (0.5) is greater than the largest y (0.33), so x > y.",
   ["I: 6x² − 3x − 4x + 2 = (2x − 1)(3x − 2) = 0 ⇒ x = 1/2, 2/3",
    "II: 12y² − 4y − 3y + 1 = (3y − 1)(4y − 1) = 0 ⇒ y = 1/3, 1/4", "min x = 0.5 > max y ≈ 0.33", "So x > y"],
   why="x < y comes from taking the reciprocals (2, 1.5 against 3, 4) instead of the roots.", secs=80)

# ================================================================ Number System (B2 I2 A1)
T = "Number System"
other = 14 * 420 // 70
assert other == 84 and math.gcd(70, 84) == 14 and math.lcm(70, 84) == 420
assert all(not (math.gcd(70, w) == 14 and math.lcm(70, w) == 420) for w in (98, 56, 42))
Q(T, "HCF and LCM", B,
  "The HCF of two numbers is 14 and their LCM is 420. If one of the numbers is 70, what is the other number?",
  "84", ["98", "56", "42"],
  "For two numbers, product of the numbers = HCF × LCM",
  "70 × other = 14 × 420 = 5,880, so the other number is 5,880 ÷ 70 = 84. Check: HCF(70, 84) = 14 and "
  "LCM(70, 84) = 420.",
  ["HCF × LCM = 14 × 420 = 5,880", "Other number = 5,880 ÷ 70 = 84", "Check: 70 = 14 × 5, 84 = 14 × 6, "
   "LCM = 14 × 5 × 6 = 420"],
  why="98, 56 and 42 are multiples of 14, but with 70 their LCM is 490, 280 and 210, not 420.", secs=35)

u = sum(math.factorial(k) for k in range(1, 51)) % 10
assert u == 3 and sum(math.factorial(k) for k in range(1, 5)) == 33 and all(math.factorial(k) % 10 == 0
                                                                           for k in range(5, 51))
Q(T, "Unit digit", B, "What is the unit digit of 1! + 2! + 3! + … + 50!?",
  "3", ["0", "4", "9"],
  "From 5! onwards every factorial contains 2 × 5, so it ends in 0",
  "5!, 6!, …, 50! all end in 0. So only 1! + 2! + 3! + 4! = 1 + 2 + 6 + 24 = 33 decides the unit digit, which is 3.",
  ["5! = 120 and every later factorial is a multiple of 10", "1! + 2! + 3! + 4! = 33", "Unit digit = 3"],
  why="0 assumes every term ends in 0; 4 and 9 are the unit digits of 4! and of 1 + 2 + 6 only.", secs=35)

sols = [(a, b) for a in range(10) for b in range(10) if (20430 + 1000 * a + b) % 72 == 0]
assert sols == [(7, 2)] and 27432 == 72 * 381
Q(T, "Divisibility", I,
  "The five-digit number 2a43b, where a and b are digits, is divisible by 72. What is the value of a × b?",
  "14", ["16", "18", "12"],
  "72 = 8 × 9 with 8 and 9 co-prime: test divisibility by 8 (last three digits) and by 9 (digit sum)",
  "For 8, the last three digits 43b must be a multiple of 8; 432 is the only one, so b = 2. For 9, the digit sum "
  "2 + a + 4 + 3 + 2 = 11 + a must be a multiple of 9, so a = 7. The number is 27,432 = 72 × 381, and a × b = 14.",
  ["Divisible by 8: 43b ∈ {432} ⇒ b = 2", "Divisible by 9: 11 + a ∈ {18} ⇒ a = 7", "27,432 ÷ 72 = 381 ✓",
   "a × b = 7 × 2 = 14"],
  why="16, 18 and 12 come from pairs (a, b) that pass only one of the two tests, for example a = 9, b = 2 or "
      "b = 6.", secs=60, by=BRUTE)

n_ = next(n for n in range(1, 1000) if n % 8 == 5 and n % 12 == 9 and n % 15 == 12)
assert n_ == 117 == math.lcm(8, 12, 15) - 3
assert not (123 % 8 == 5 and 123 % 12 == 9) and not (113 % 12 == 9)
assert all(237 % d == r for d, r in ((8, 5), (12, 9), (15, 12)))
Q(T, "Remainders", I,
  "What is the smallest number which, when divided by 8, 12 and 15, leaves remainders 5, 9 and 12 respectively?",
  "117", ["123", "237", "113"],
  "If divisor − remainder is the same for every divisor (here 3), the number = k × LCM − that common difference",
  "8 − 5 = 12 − 9 = 15 − 12 = 3, so the number is 3 short of a common multiple of 8, 12 and 15. LCM(8, 12, 15) = "
  "120, so the smallest such number is 120 − 3 = 117.",
  ["Differences: 8 − 5 = 3, 12 − 9 = 3, 15 − 12 = 3", "LCM(8, 12, 15) = 120", "Number = 120 − 3 = 117",
   "Check: 117 = 8 × 14 + 5 = 12 × 9 + 9 = 15 × 7 + 12"],
  why="123 adds the 3 instead of subtracting; 237 is the next such number after 117, not the smallest; 113 "
      "subtracts 7.", secs=55, by=BRUTE)

pairs = [(x, 216 - x) for x in range(1, 109) if math.gcd(x, 216 - x) == 27]
assert pairs == [(27, 189), (81, 135)]
Q(T, "HCF and LCM", A,
  "The sum of two positive numbers is 216 and their HCF is 27. How many such pairs of numbers are possible?",
  "2", ["3", "4", "1"],
  "Write the numbers as 27a and 27b with a and b co-prime",
  "27a + 27b = 216 gives a + b = 8. Co-prime pairs with a < b are (1, 7) and (3, 5); (2, 6) and (4, 4) share a "
  "factor. So the pairs are (27, 189) and (81, 135): 2 pairs.",
  ["Numbers = 27a, 27b with HCF(a, b) = 1", "a + b = 216 ÷ 27 = 8", "Co-prime pairs: (1, 7), (3, 5)",
   "(2, 6) and (4, 4) are not co-prime", "2 pairs"],
  why="3 and 4 include (2, 6) or (4, 4), whose HCF would be 54 or 108; 1 misses (3, 5).", secs=75, by=BRUTE)

# ================================================================ Percentage (B1 I3 A2)
T = "Percentage"
cap = F(84) / (F(56, 100) - F(35, 100))
assert cap == 400 and F(84) / F(35, 100) == 240 and F(84) / F(56, 100) == 150
Q(T, "Basic percentage", B,
  "A water tank is 35% full. After 84 litres of water are poured in, it is 56% full. What is the capacity of the "
  "tank?",
  "400 litres", ["240 litres", "150 litres", "420 litres"],
  "The added water equals the change in the percentage filled",
  "The 84 litres raise the level from 35% to 56%, that is, by 21% of the capacity. So capacity = 84 ÷ 0.21 = "
  "400 litres.",
  ["56% − 35% = 21%", "21% of capacity = 84 litres", "Capacity = 84 × 100 ÷ 21 = 400 litres"],
  why="240 treats 84 litres as 35% of the tank; 150 treats it as 56%; 420 uses 20% instead of 21%.", secs=35)

f_ = F(125, 100) * F(80, 100) * F(110, 100)
assert f_ == F(11, 10)
Q(T, "Successive change", I,
  "The price of a television was raised by 25%, then cut by 20% in a sale, and later raised by 10%. What is the "
  "overall change in its price?",
  "10% increase", ["15% increase", "5% increase", "No change"],
  "Successive percentage changes multiply: final = original × (1 + r₁)(1 + r₂)(1 + r₃)",
  "Multiplying factors: 1.25 × 0.80 × 1.10 = 1.10. The price ends 10% above where it started.",
  ["Rise of 25%: × 1.25", "Cut of 20%: × 0.80 (1.25 × 0.8 = 1)", "Rise of 10%: × 1.10", "Net factor 1.10 ⇒ 10% "
   "increase"],
  short="A 25% rise followed by a 20% cut cancel exactly (5/4 × 4/5 = 1), leaving only the 10% rise.",
  why="15% adds the percentages (25 − 20 + 10); 5% ignores the last rise; 'No change' stops after the first two "
      "steps.", secs=45)

val = 625000 * F(80, 100) * F(88, 100) ** 2
assert val == 387200 and 625000 * F(56, 100) == 350000 and 625000 * F(80, 100) * F(88, 100) == 440000
assert 625000 * F(88, 100) ** 2 * F(80, 100) == 387200 and 500000 * F(88, 100) * F(80, 100) == 352000
Q(T, "Population and depreciation", I,
  "A car bought for ₹6,25,000 loses 20% of its value in the first year and 12% of its value at the start of each "
  "later year. What is its value after 3 years?",
  "₹3,87,200", ["₹3,50,000", "₹4,40,000", "₹3,52,000"],
  "Depreciation on the reducing value: multiply by (1 − rate) year by year",
  "After year 1: 6,25,000 × 0.80 = 5,00,000. After year 2: 5,00,000 × 0.88 = 4,40,000. After year 3: 4,40,000 × "
  "0.88 = 3,87,200.",
  ["Year 1: 6,25,000 × 0.8 = 5,00,000", "Year 2: 5,00,000 × 0.88 = 4,40,000", "Year 3: 4,40,000 × 0.88 = 3,87,200"],
  why="₹3,50,000 subtracts 20% + 12% + 12% = 44% of the original price; ₹4,40,000 is the value after 2 years; "
      "₹3,52,000 applies 20% again in year 3.", secs=55)

Bi = F(1500) / (F(30, 100) * F(125, 100) - F(25, 100))
assert Bi == 12000 and Bi * F(125, 100) == 15000
Q(T, "Income and expenditure", I,
  "Amit's income is 25% more than Bina's. Amit spends 70% of his income and Bina spends 75% of hers. If Amit saves "
  "₹1,500 more than Bina, what is Amit's income?",
  "₹15,000", ["₹12,000", "₹18,750", "₹20,000"],
  "Express both savings in terms of one income",
  "Let Bina's income be B. Amit's income is 1.25B and he saves 30% of it, 0.375B. Bina saves 0.25B. The "
  "difference 0.125B = 1,500, so B = 12,000 and Amit's income = 15,000.",
  ["Amit's saving = 30% × 1.25B = 0.375B", "Bina's saving = 25% × B = 0.25B", "0.125B = 1,500 ⇒ B = 12,000",
   "Amit's income = 1.25 × 12,000 = ₹15,000"],
  why="₹12,000 is Bina's income; ₹18,750 is 1.25 × 15,000; ₹20,000 takes the 1,500 as 7.5% of Amit's income.",
  secs=60)

both = 72 + 65 - (100 - 18)
assert both == 55 and F(495 * 100, both) == 900
assert F(495 * 100, 45) == 1100 and F(495 * 100, 60) == 825 and F(495 * 100, 50) == 990
Q(T, "Basic percentage", A,
  "In a test, 72% of the candidates passed in Mathematics, 65% passed in English and 18% failed in both. If 495 "
  "candidates passed in both subjects, how many candidates took the test?",
  "900", ["1,100", "825", "990"],
  "Sets: passed in at least one = 100% − failed in both; both = M + E − at least one",
  "82% passed in at least one subject. So both = 72% + 65% − 82% = 55%. 55% of the total is 495, so the total is "
  "495 ÷ 0.55 = 900.",
  ["At least one = 100% − 18% = 82%", "Both = 72 + 65 − 82 = 55%", "Total = 495 × 100 ÷ 55 = 900"],
  why="1,100 takes 495 as 45% of the candidates; 825 takes it as 60%; 990 takes it as 50%.", secs=80)

p_ = 50000
for _ in range(2):
    p_ = p_ * F(110, 100) - 1000
assert p_ == 58400 and 50000 * F(121, 100) == 60500 and 60500 - 2000 == 58500 and 60500 - 1000 == 59500
Q(T, "Population and depreciation", A,
  "A town's population of 50,000 grows by 10% every year. At the end of each year, after the growth, 1,000 people "
  "move out. What is the population at the end of 2 years?",
  "58,400", ["58,500", "60,500", "59,500"],
  "Apply growth and the fixed outflow year by year; the outflow of year 1 also misses the growth of year 2",
  "Year 1: 50,000 × 1.1 = 55,000, minus 1,000 = 54,000. Year 2: 54,000 × 1.1 = 59,400, minus 1,000 = 58,400.",
  ["Year 1: 55,000 − 1,000 = 54,000", "Year 2: 54,000 × 1.1 = 59,400", "59,400 − 1,000 = 58,400"],
  why="58,500 grows 50,000 for both years and subtracts 2,000 at the end, ignoring that the first 1,000 would "
      "not have grown; 60,500 ignores migration; 59,500 subtracts only once.", secs=80)

# ================================================================ Ratio and Proportion (B2 I1 A1)
T = "Ratio and Proportion"
x_ = next(x for x in range(2001, 100000) if F(4 * x - 6000, 3 * x - 6000) == F(3, 2))
assert x_ == 6000 and 4 * x_ == 24000
Q(T, "Basic ratio", B,
  "The incomes of A and B are in the ratio 4 : 3 and their expenditures are in the ratio 3 : 2. If each saves "
  "₹6,000 a month, what is A's monthly income?",
  "₹24,000", ["₹18,000", "₹30,000", "₹12,000"],
  "Income − expenditure = saving; set up the expenditure ratio",
  "Let the incomes be 4x and 3x. Expenditures are 4x − 6,000 and 3x − 6,000, in the ratio 3 : 2. So "
  "2(4x − 6,000) = 3(3x − 6,000), which gives x = 6,000. A's income = 4x = ₹24,000.",
  ["Incomes 4x, 3x; expenditures 4x − 6,000, 3x − 6,000", "2(4x − 6,000) = 3(3x − 6,000)",
   "8x − 12,000 = 9x − 18,000 ⇒ x = 6,000", "A's income = 24,000"],
  why="₹18,000 is B's income; ₹30,000 and ₹12,000 use x = 7,500 or 3,000.", secs=50)

sols = {F(a, b) for a in range(1, 60) for b in range(1, 60) if 3 * a != 5 * b and F(3 * a + 5 * b, 3 * a - 5 * b) == F(7, 3)}
assert sols == {F(25, 6)}
Q(T, "Proportion", B, "If (3a + 5b) : (3a − 5b) = 7 : 3, what is a : b?",
  "25 : 6", ["6 : 25", "5 : 3", "10 : 3"],
  "Cross-multiply a proportion: p : q = r : s means ps = qr",
  "3(3a + 5b) = 7(3a − 5b), so 9a + 15b = 21a − 35b. Then 50b = 12a and a : b = 50 : 12 = 25 : 6.",
  ["3(3a + 5b) = 7(3a − 5b)", "9a + 15b = 21a − 35b", "12a = 50b", "a : b = 50 : 12 = 25 : 6"],
  short="Componendo-dividendo: 3a : 5b = (7 + 3) : (7 − 3) = 5 : 2, so a : b = 25 : 6.",
  why="6 : 25 is inverted; 5 : 3 and 10 : 3 stop at 3a : 5b = 5 : 2 without dividing by 3 and 5 correctly.",
  secs=50)

shares = [(a, b, 10800 - a - b) for a in range(0, 10801, 60) for b in range(0, 10801 - a, 60)
          if F(a) == F(2, 3) * (b + 10800 - a - b) and F(b) == F(1, 4) * (a + 10800 - a - b)]
assert shares == [(4320, 2160, 4320)]
Q(T, "Coins and salary share", I,
  "₹10,800 is divided among A, B and C so that A gets two-thirds of what B and C together get, and B gets "
  "one-fourth of what A and C together get. What is B's share?",
  "₹2,160", ["₹4,320", "₹2,700", "₹1,800"],
  "If X gets p/q of what the others get, X's share = p/(p + q) of the total",
  "A = 2/3 of (B + C) means A is 2 parts out of 5, so A = 2/5 × 10,800 = 4,320. B = 1/4 of (A + C) means B is 1 part "
  "out of 5, so B = 10,800 ÷ 5 = 2,160. C = 10,800 − 4,320 − 2,160 = 4,320.",
  ["A : (B + C) = 2 : 3 ⇒ A = 2/5 × 10,800 = 4,320", "B : (A + C) = 1 : 4 ⇒ B = 1/5 × 10,800 = 2,160",
   "C = 4,320 (check)"],
  why="₹4,320 is A's (and C's) share; ₹2,700 takes B as one-fourth of the total; ₹1,800 takes it as one-sixth.",
  secs=60)

k2 = F(1368, 2 ** 2 + 3 ** 2 + 5 ** 2)
assert k2 == 36 and 5 * 6 == 30
Q(T, "Basic ratio", A,
  "Three numbers are in the ratio 2 : 3 : 5 and the sum of their squares is 1,368. What is the largest number?",
  "30", ["18", "36", "24"],
  "Write the numbers as 2k, 3k and 5k",
  "(2k)² + (3k)² + (5k)² = 38k² = 1,368, so k² = 36 and k = 6 (the numbers are positive). The numbers are 12, 18 "
  "and 30, and the largest is 30.",
  ["4k² + 9k² + 25k² = 38k²", "38k² = 1,368 ⇒ k² = 36 ⇒ k = 6", "Numbers: 12, 18, 30", "Largest = 30"],
  why="18 is the middle number; 36 is k², not 5k; 24 corresponds to k = 4.8, whose squares add up to only 875.52.",
  secs=60)

# ================================================================ Problems on Ages (B1 I1 A1)
T = "Problems on Ages"
S_ = next(s for s in range(6, 100) if (s + 6 - 5) == F(3, 2) * (s - 5))
assert S_ == 17 and S_ + 6 == 23
Q(T, "Present and future ages", B,
  "Ravi is 6 years older than Sunil. Five years ago, Ravi's age was 1.5 times Sunil's age. What is Ravi's present "
  "age?",
  "23 years", ["17 years", "29 years", "21 years"],
  "Write both ages five years ago in terms of one unknown",
  "Let Sunil be S, so Ravi is S + 6. Five years ago: S + 1 = 1.5(S − 5), so S + 1 = 1.5S − 7.5, 0.5S = 8.5 and "
  "S = 17. Ravi is 23.",
  ["Five years ago: Ravi S + 1, Sunil S − 5", "S + 1 = 1.5S − 7.5", "S = 17", "Ravi = 17 + 6 = 23"],
  why="17 is Sunil's age; 29 adds 6 twice; 21 uses S + 6 = 1.5S, ignoring the 5 years.", secs=45)

A_ = next(a for a in range(1, 54) if F(a + 8, 54 - a + 8) == F(4, 3))
assert (A_, 54 - A_) == (32, 22)
Q(T, "Ratio-based ages", I,
  "The sum of the present ages of A and B is 54 years. Eight years from now their ages will be in the ratio 4 : 3. "
  "What is B's present age?",
  "22 years", ["32 years", "30 years", "24 years"],
  "Both ages grow by 8, so the future sum is 54 + 16",
  "In 8 years the sum will be 54 + 16 = 70, split 4 : 3, so A will be 40 and B 30. B's present age = 30 − 8 = 22.",
  ["Sum in 8 years = 70", "B then = 3/7 × 70 = 30", "B now = 30 − 8 = 22"],
  why="32 is A's present age; 30 is B's age 8 years from now; 24 splits 54 in the ratio 4 : 3 and then subtracts "
      "nothing.", secs=50)

now_total = 5 * 28
before = F(now_total - 6 - 4 * 6, 4)
assert before == F(55, 2) and F(now_total - 6, 4) == F(67, 2)
Q(T, "Present and future ages", A,
  "The average age of a family of five is 28 years. The youngest member is 6 years old. What was the average age "
  "of the family just before the youngest member was born?",
  "27.5 years", ["33.5 years", "22 years", "28 years"],
  "Go back 6 years: remove the youngest and reduce every other member's age by 6",
  "Total now = 5 × 28 = 140. Without the youngest, the other four total 134 now. Six years ago each of them was "
  "6 years younger, so their total was 134 − 24 = 110, and the average of the family of four was 110 ÷ 4 = 27.5.",
  ["Total now = 140", "Others now = 140 − 6 = 134", "6 years ago: 134 − 4 × 6 = 110", "Average = 110 ÷ 4 = 27.5"],
  why="33.5 forgets that the other members were also 6 years younger; 22 subtracts 6 from the average of five; "
      "28 assumes the average does not change.", secs=75)

# ================================================================ Average (B1 I2 A2)
T = "Average"
v = 3 * 32 + 5
assert v == 101 and 3 * 32 == 96 and (32 + 5) * 3 == 111
Q(T, "Simple average", B,
  "The average of six numbers is 32. Each number is multiplied by 3 and then 5 is added to it. What is the new "
  "average?",
  "101", ["96", "111", "37"],
  "Multiplying or adding the same amount to every number does the same to the average",
  "Every number becomes 3x + 5, so the average becomes 3 × 32 + 5 = 101.",
  ["New average = 3 × old average + 5", "3 × 32 + 5 = 101"],
  why="96 forgets the + 5; 111 adds 5 before multiplying; 37 only adds 5.", secs=30)

t_ = 21 * 49 - 20 * 48
assert t_ == 69
Q(T, "Replacement", I,
  "The average weight of 20 students is 48 kg. When the teacher's weight is included, the average rises by 1 kg. "
  "What is the teacher's weight?",
  "69 kg", ["49 kg", "68 kg", "70 kg"],
  "New total − old total = the added weight",
  "Old total = 20 × 48 = 960 kg. New total = 21 × 49 = 1,029 kg. The teacher weighs 1,029 − 960 = 69 kg.",
  ["Old total = 960", "New total = 21 × 49 = 1,029", "Teacher = 69 kg"],
  short="Teacher = new average + (number of students × rise) = 49 + 20 × 1 = 69.",
  why="49 kg is the new average; 68 kg adds 20 to the old average; 70 kg adds 21 to the new average.", secs=45)

x_ = next(x for x in range(1, 200) if F(40 * 52 + 60 * 45 + 60 * x, 100 + x) == 50)
assert x_ == 22
Q(T, "Weighted average", I,
  "A grocer mixes 40 kg of rice at ₹52 per kg, 60 kg at ₹45 per kg and some rice at ₹60 per kg. The average cost of "
  "the mixture is ₹50 per kg. How many kg of the ₹60 rice did he use?",
  "22 kg", ["20 kg", "25 kg", "18 kg"],
  "Weighted average: total cost ÷ total quantity",
  "Cost of the first two lots = 40 × 52 + 60 × 45 = 2,080 + 2,700 = 4,780. With x kg at 60: (4,780 + 60x) ÷ "
  "(100 + x) = 50, so 4,780 + 60x = 5,000 + 50x and x = 22.",
  ["40 × 52 = 2,080; 60 × 45 = 2,700", "4,780 + 60x = 50(100 + x)", "10x = 220 ⇒ x = 22"],
  short="Balance around 50: lot 1 gives +2 × 40 = +80, lot 2 gives −5 × 60 = −300, so the ₹60 rice must give "
        "+220 = 10x.",
  why="20, 25 and 18 kg leave the mixture's average at about ₹49.8, ₹50.2 and ₹49.7.", secs=60)

for m in range(11, 101, 2):
    nums = [m - 4, m - 2, m, m + 2, m + 4, m + 6, m + 8, m + 10]
    assert F(sum(nums), 8) == m + 3
Q(T, "Simple average", A,
  "The average of five consecutive odd numbers is m. If the next three consecutive odd numbers are also included, "
  "what is the average of all eight numbers?",
  "m + 3", ["m + 4", "m + 6", "m + 5"],
  "Consecutive odd numbers are 2 apart; the average of an evenly spaced list is the middle value",
  "The five numbers are m − 4, m − 2, m, m + 2, m + 4. The next three are m + 6, m + 8, m + 10. The eight numbers "
  "sum to 8m + 24, so the average is m + 3.",
  ["Five numbers: m − 4 … m + 4 (sum 5m)", "Next three: m + 6, m + 8, m + 10 (sum 3m + 24)", "Total = 8m + 24",
   "Average = m + 3"],
  short="Eight evenly spaced numbers from m − 4 to m + 10: average = (first + last) ÷ 2 = m + 3.",
  why="m + 4 averages the first and the eighth wrongly as m and m + 8; m + 6 and m + 5 use the average of the "
      "three new numbers alone or forget the first five.", secs=60)

exp_ = 5 * 12000 + 4 * 14500 + 3 * 16000
inc = F(exp_ + 26000, 12)
assert exp_ == 166000 and inc == 16000
assert F(12000 + 14500 + 16000, 3) + F(26000, 12) == F(49000, 3) and F(166000, 12) == F(41500, 3)
Q(T, "Weighted average", A,
  "A family's average monthly expenditure was ₹12,000 for the first 5 months of a year, ₹14,500 for the next 4 "
  "months and ₹16,000 for the last 3 months. If the family saved ₹26,000 in the whole year, what was its average "
  "monthly income?",
  "₹16,000", ["₹16,333.33", "₹13,833.33", "₹15,500"],
  "Annual income = annual expenditure + annual saving; weight each monthly average by its number of months",
  "Annual expenditure = 5 × 12,000 + 4 × 14,500 + 3 × 16,000 = 60,000 + 58,000 + 48,000 = 1,66,000. Income = "
  "1,66,000 + 26,000 = 1,92,000, so the monthly average is 1,92,000 ÷ 12 = ₹16,000.",
  ["5 × 12,000 = 60,000", "4 × 14,500 = 58,000", "3 × 16,000 = 48,000", "Expenditure = 1,66,000",
   "Income = 1,92,000 ⇒ ₹16,000 a month"],
  why="₹16,333.33 takes the plain average of the three expenditure figures; ₹13,833.33 forgets the savings; "
      "₹15,500 is not supported by any combination of the data.", secs=70)

# ================================================================ Profit and Loss (B4 I4 A1)
T = "Profit and Loss"
pp = F(5400 - 4800, 4800) * 100
assert pp == F(25, 2) and F(600, 4500) * 100 == F(40, 3) and F(600, 5400) * 100 == F(100, 9)
Q(T, "Cost and selling price", B,
  "Kiran buys a used cycle for ₹4,500, spends ₹300 on repairs and sells it for ₹5,400. What is his profit "
  "percentage?",
  "12.5%", ["20%", "13.33%", "11.11%"],
  "Repair costs are part of the cost price",
  "Total cost = 4,500 + 300 = 4,800. Profit = 5,400 − 4,800 = 600, which is 600 ÷ 4,800 = 12.5% of the cost.",
  ["CP = 4,500 + 300 = 4,800", "Profit = 600", "600 ÷ 4,800 × 100 = 12.5%"],
  why="13.33% leaves out the repairs; 11.11% divides by the selling price; 20% takes the profit as ₹900.",
  secs=35)

assert F(15 - 12, 12) * 100 == 25 and F(3, 15) * 100 == 20
Q(T, "Cost and selling price", B,
  "The cost price of 15 pens equals the selling price of 12 pens. What is the profit percentage?",
  "25%", ["20%", "30%", "15%"],
  "Equal amounts of money: compare the number of items",
  "Let each pen cost ₹1. Then 12 pens sell for ₹15, so the profit on 12 pens is ₹3 on a cost of ₹12, i.e. 25%.",
  ["Let CP of 1 pen = 1 ⇒ CP of 15 = 15", "SP of 12 pens = 15", "Profit on 12 pens = 15 − 12 = 3",
   "Profit% = 3 ÷ 12 × 100 = 25%"],
  short="Profit% = (15 − 12) ÷ 12 × 100.", why="20% divides the 3 by 15 instead of 12.", secs=30)

cp = F(2760, F(115, 100))
assert cp == 2400 and F(2280 - cp, cp) * 100 == -5
Q(T, "Cost and selling price", B,
  "By selling a watch for ₹2,760, a shopkeeper gains 15%. What would be his gain or loss percentage if he sold it "
  "for ₹2,280?",
  "5% loss", ["5% gain", "4.35% loss", "20% loss"],
  "Find the cost price first, then compare the new selling price with it",
  "CP = 2,760 ÷ 1.15 = 2,400. Selling at 2,280 means a loss of 120, which is 120 ÷ 2,400 = 5% of the cost.",
  ["CP = 2,760 ÷ 1.15 = 2,400", "Loss = 2,400 − 2,280 = 120", "Loss% = 120 ÷ 2,400 × 100 = 5%"],
  why="5% gain gets the direction wrong; 4.35% divides 120 by 2,760; 20% divides the drop of 480 by 2,400.",
  secs=40)

gain = F(5 - 4, 4) * 100
assert gain == 25 and F(1, 5) * 100 == 20
Q(T, "Dishonest dealer", B,
  "A milkman adds 1 litre of water to every 4 litres of milk and sells the mixture at the cost price of milk. What "
  "is his gain percentage?",
  "25%", ["20%", "16.67%", "33.33%"],
  "Water costs nothing, so the gain comes from selling 5 litres for the cost of 4",
  "4 litres of milk cost him 4 units. He sells 5 litres of mixture at 1 unit each, getting 5 units. Gain = 1 on 4, "
  "which is 25%.",
  ["Cost of 4 L milk = 4 units", "Sells 5 L mixture for 5 units", "Gain% = 1 ÷ 4 × 100 = 25%"],
  why="20% divides the gain by the 5 litres sold instead of the cost of 4 litres.", secs=35)

cp = F(1860 + 1340, 2)
assert cp == 1600 and 1860 - cp == cp - 1340 and cp * F(6, 5) == 1920
Q(T, "Cost and selling price", I,
  "The profit made by selling an article for ₹1,860 equals the loss made by selling it for ₹1,340. At what price "
  "should it be sold to make a profit of 20%?",
  "₹1,920", ["₹2,016", "₹1,860", "₹2,232"],
  "If profit at S₁ equals loss at S₂, the cost price is midway: (S₁ + S₂) ÷ 2",
  "1,860 − CP = CP − 1,340, so CP = (1,860 + 1,340) ÷ 2 = 1,600. For a 20% profit, SP = 1.2 × 1,600 = 1,920.",
  ["1,860 − CP = CP − 1,340", "CP = 3,200 ÷ 2 = 1,600", "SP = 1,600 × 1.2 = ₹1,920"],
  why="₹2,016 starts from 1,680; ₹1,860 already includes a profit of only 16.25%; ₹2,232 adds 20% to 1,860.",
  secs=45)

C_ = next(c for c in range(100, 20000, 100) if F(85, 100) * (c + 1500) - c == 600)
assert C_ == 4500
Q(T, "Marked price", I,
  "The marked price of a sofa is ₹1,500 more than its cost price. When it is sold at a discount of 15%, the "
  "shopkeeper makes a profit of ₹600. What is the cost price?",
  "₹4,500", ["₹4,000", "₹6,000", "₹3,600"],
  "SP = 0.85 × MP and MP = CP + 1,500; profit = SP − CP",
  "0.85(C + 1,500) − C = 600 gives 0.85C + 1,275 − C = 600, so 0.15C = 675 and C = 4,500. Check: MP = 6,000, "
  "SP = 5,100, profit = 600.",
  ["SP = 0.85(C + 1,500)", "0.85C + 1,275 − C = 600", "0.15C = 675 ⇒ C = 4,500", "Check: 5,100 − 4,500 = 600"],
  why="₹6,000 is the marked price; ₹4,000 and ₹3,600 give profits of ₹675 and ₹735.", secs=60)

S_ = F(1)
C0 = F(3, 4) * S_
C1 = C0 * F(6, 5)
assert F(S_ - C1, C1) * 100 == F(100, 9)
Q(T, "Cost and selling price", I,
  "A trader's profit is 25% of his selling price. His cost then rises by 20% while his selling price stays the same. "
  "What is his new profit as a percentage of the new cost price?",
  "11.11%", ["5%", "10%", "8.33%"],
  "Profit on SP must be converted to a cost-based figure",
  "Take SP = 100. Profit = 25, so cost = 75. The new cost = 75 × 1.2 = 90 and the new profit = 10, which is 10 ÷ 90 "
  "= 11.11% of the new cost.",
  ["SP = 100 ⇒ CP = 75", "New CP = 90", "New profit = 10", "10 ÷ 90 × 100 = 11.11%"],
  why="5% subtracts 20% from 25%; 10% is profit as a percentage of SP; 8.33% divides 10 by 120.", secs=60)

m_total = F(56400, F(120, 100))
R_ = (m_total - 2000) / F(90, 100)
assert m_total == 47000 and R_ == 50000
assert near(F(47000, 1) / F(9, 10), 52222.22, 0.01) and near(F(49000) / F(9, 10), 54444.44, 0.01)
Q(T, "Successive transactions", I,
  "Rahul sold a scooter to Mohan at a loss of 10%. Mohan spent ₹2,000 on repairs and sold it to Sohan at a profit "
  "of 20% on his total cost. If Sohan paid ₹56,400, what did Rahul pay for the scooter?",
  "₹50,000", ["₹52,222.22", "₹54,444.44", "₹47,911.11"],
  "Work backwards; the repair cost is added to Mohan's cost before his profit",
  "Mohan's total cost = 56,400 ÷ 1.2 = 47,000. He paid Rahul 47,000 − 2,000 = 45,000, which was 90% of Rahul's cost. "
  "So Rahul paid 45,000 ÷ 0.9 = ₹50,000.",
  ["Mohan's total cost = 56,400 ÷ 1.2 = 47,000", "Paid to Rahul = 47,000 − 2,000 = 45,000",
   "Rahul's CP = 45,000 ÷ 0.9 = 50,000"],
  why="₹52,222.22 forgets the repairs; ₹54,444.44 adds them instead of subtracting; ₹47,911.11 takes 20% of the "
      "selling price as the profit.", secs=60)

a_ = next(a for a in range(0, 12001) if F(115, 100) * a + F(90, 100) * (12000 - a) == 12480)
b_ = 12000 - a_
new = F(90, 100) * a_ + F(115, 100) * b_
assert (a_, b_, new) == (6720, 5280, 12120)
Q(T, "Cost and selling price", A,
  "Two articles A and B together cost ₹12,000. A is sold at a profit of 15% and B at a loss of 10%, and together "
  "they fetch ₹12,480. If A had instead been sold at a loss of 10% and B at a profit of 15%, how much would they "
  "have fetched together?",
  "₹12,120", ["₹12,480", "₹11,880", "₹12,000"],
  "Two unknown costs from the total cost and the total selling price",
  "1.15a + 0.9(12,000 − a) = 12,480 gives 0.25a = 1,680, so a = 6,720 and b = 5,280. Swapping the rates: 0.9 × "
  "6,720 + 1.15 × 5,280 = 6,048 + 6,072 = ₹12,120.",
  ["1.15a + 0.9b = 12,480 and a + b = 12,000", "0.25a + 10,800 = 12,480 ⇒ a = 6,720, b = 5,280",
   "New SP = 0.9 × 6,720 + 1.15 × 5,280", "= 6,048 + 6,072 = 12,120"],
  short="The new total = 2 × 12,000 × 1.025 − 12,480 because each article gets both rates once: 24,600 − 12,480 = "
        "12,120.",
  why="₹12,480 ignores the swap; ₹11,880 mirrors the gain of 480 into a loss; ₹12,000 assumes the swap cancels.",
  secs=100)

# ================================================================ Discount (B1 I2 A1)
T = "Discount"
pay = 2500 * F(88, 100) - 50
assert pay == 2150 and (2500 - 50) * F(88, 100) == 2156
Q(T, "Single discount", B,
  "An item marked ₹2,500 is sold at a discount of 12%, and the customer gets a further cash discount of ₹50 on the "
  "discounted price. How much does the customer pay?",
  "₹2,150", ["₹2,156", "₹2,200", "₹2,100"],
  "Apply the percentage discount first, then the flat cash discount",
  "12% of 2,500 = 300, so the price after discount is 2,200. The cash discount brings it to 2,200 − 50 = ₹2,150.",
  ["12% of 2,500 = 300", "2,500 − 300 = 2,200", "2,200 − 50 = 2,150"],
  why="₹2,156 takes the ₹50 off before the 12%; ₹2,200 ignores the cash discount; ₹2,100 takes ₹100 off.", secs=35)

x_ = next(x for x in range(1, 100) if 4000 * F(80, 100) * F(100 - x, 100) == 2720)
assert x_ == 15 and F(4000 - 2720, 4000) * 100 == 32
Q(T, "Successive discounts", I,
  "After two successive discounts of 20% and x%, an article marked at ₹4,000 is sold for ₹2,720. What is x?",
  "15", ["12", "18", "32"],
  "Apply the discounts one after the other; the second is on the reduced price",
  "After 20%: 4,000 × 0.8 = 3,200. The second discount takes it from 3,200 to 2,720, a cut of 480, which is "
  "480 ÷ 3,200 = 15%.",
  ["4,000 × 0.8 = 3,200", "3,200 − 2,720 = 480", "480 ÷ 3,200 × 100 = 15%"],
  why="12% takes 480 as a percentage of 4,000; 32% is the single equivalent discount; 18% has no basis.", secs=45)

mp = F(200 + 100, F(10, 100))
cp = mp * F(80, 100) - 200
assert (mp, cp) == (3000, 2200) and mp * F(70, 100) - cp == -100
Q(T, "Discount with profit", I,
  "If a shopkeeper sells an article at a 20% discount, he gains ₹200. If he sells it at a 30% discount, he loses "
  "₹100. What is the cost price of the article?",
  "₹2,200", ["₹2,400", "₹3,000", "₹2,000"],
  "The extra 10% discount equals the swing from +200 to −100",
  "Going from 20% to 30% discount lowers the selling price by 10% of MP and changes the result by 200 + 100 = 300. So "
  "MP = 3,000. At 20% off, SP = 2,400, and CP = 2,400 − 200 = ₹2,200.",
  ["10% of MP = 300 ⇒ MP = 3,000", "SP at 20% off = 2,400", "CP = 2,400 − 200 = 2,200",
   "Check: at 30% off, SP = 2,100 ⇒ loss 100"],
  why="₹2,400 is the selling price at 20% off; ₹3,000 is the marked price; ₹2,000 uses a swing of 200 only.",
  secs=60)

pre_tax = F(16992, F(118, 100))
mp = pre_tax / (F(80, 100) * F(90, 100))
cp = pre_tax / F(120, 100)
assert (pre_tax, mp, cp) == (14400, 20000, 12000) and F(16992, F(12, 10)) == 14160
Q(T, "Discount with profit", A,
  "A shop allows successive discounts of 20% and 10% on the marked price of a refrigerator and then adds 18% GST on "
  "the discounted price. A customer pays ₹16,992. If the shop's profit is 20% of its cost on the pre-tax price, what "
  "is the cost price of the refrigerator?",
  "₹12,000", ["₹14,160", "₹14,400", "₹11,520"],
  "Strip the tax first, then the profit; the marked price is not needed for the cost",
  "Pre-tax price = 16,992 ÷ 1.18 = 14,400. This is 120% of the cost, so CP = 14,400 ÷ 1.2 = ₹12,000. (The marked "
  "price was 14,400 ÷ 0.72 = ₹20,000.)",
  ["Pre-tax price = 16,992 ÷ 1.18 = 14,400", "CP = 14,400 ÷ 1.2 = 12,000", "Check: MP = 14,400 ÷ (0.8 × 0.9) = "
   "20,000"],
  why="₹14,160 removes the 20% profit from the tax-inclusive price; ₹14,400 is the pre-tax selling price; ₹11,520 "
      "takes 20% off 14,400 instead of dividing by 1.2.", secs=90)

# ================================================================ Simple Interest (B1 I1 A1)
T = "Simple Interest"
t_ = F(1512 * 100, 4800 * F(63, 10))
assert t_ == 5
Q(T, "Basic SI", B,
  "In how many years will ₹4,800 earn a simple interest of ₹1,512 at 6.3% per annum?",
  "5 years", ["4.5 years", "6 years", "5.5 years"],
  "SI = P × R × T ÷ 100, so T = SI × 100 ÷ (P × R)",
  "Interest for one year = 4,800 × 6.3% = ₹302.40. ₹1,512 ÷ 302.40 = 5 years.",
  ["One year's interest = 4,800 × 0.063 = 302.4", "T = 1,512 ÷ 302.4 = 5"],
  why="4.5, 6 and 5.5 years give interest of ₹1,360.80, ₹1,814.40 and ₹1,663.20.", secs=35)

P_ = F(1200, 1 - F(12 * 5, 100))
assert P_ == 3000
Q(T, "Basic SI", I,
  "The simple interest on a sum for 5 years at 12% per annum is ₹1,200 less than the sum itself. What is the sum?",
  "₹3,000", ["₹2,000", "₹2,500", "₹3,600"],
  "Interest for 5 years at 12% is 60% of the principal",
  "SI = 60% of P, so P − 0.6P = 0.4P = 1,200, which gives P = ₹3,000.",
  ["SI = P × 12 × 5 ÷ 100 = 0.6P", "P − 0.6P = 1,200", "0.4P = 1,200 ⇒ P = 3,000"],
  why="₹2,000 divides 1,200 by 0.6 (taking ₹1,200 as the interest); ₹2,500 and ₹3,600 give differences of ₹1,000 "
      "and ₹1,440.", secs=45)

x_ = next(x for x in range(5000, 100001, 100) if F(16, 100) * x + F(30, 100) * (x - 5000) == 7700)
assert x_ == 20000
Q(T, "SI with changing rates", A,
  "Neha deposits a sum at 8% per annum simple interest. After 2 years she withdraws the interest earned plus "
  "₹5,000 of the principal, and leaves the rest for 3 more years at 10% per annum simple interest. Her total "
  "interest over the 5 years is ₹7,700. How much did she deposit?",
  "₹20,000", ["₹18,000", "₹22,000", "₹25,000"],
  "Split the time into two periods with different principals and rates",
  "First 2 years: interest = 0.16x. Then the principal is x − 5,000 for 3 years at 10%: interest = 0.3(x − 5,000). "
  "So 0.16x + 0.3x − 1,500 = 7,700, giving 0.46x = 9,200 and x = ₹20,000.",
  ["Period 1: x × 8% × 2 = 0.16x", "Period 2: (x − 5,000) × 10% × 3 = 0.3x − 1,500", "0.46x − 1,500 = 7,700",
   "x = 9,200 ÷ 0.46 = 20,000"],
  why="₹18,000, ₹22,000 and ₹25,000 give total interest of ₹6,780, ₹8,620 and ₹10,000.", secs=90)

# ================================================================ Compound Interest (B2 I3 A3)
T = "Compound Interest"
amt = 20000 * F(105, 100) ** 3
assert amt == F(46305, 2) and 20000 * F(105, 100) ** 2 == 22050 and near(20000 * 1.05 ** 4, 24310.125)
Q(T, "Annual compounding", B,
  "What amount will ₹20,000 grow to in 3 years at 5% per annum compound interest, compounded annually?",
  "₹23,152.50", ["₹23,000", "₹22,050", "₹24,310.13"],
  "Amount = P(1 + r/100)ⁿ",
  "20,000 × 1.05 = 21,000; × 1.05 = 22,050; × 1.05 = 23,152.50.",
  ["Year 1: 20,000 × 1.05 = 21,000", "Year 2: 21,000 × 1.05 = 22,050", "Year 3: 22,050 × 1.05 = 23,152.50"],
  why="₹23,000 is the simple-interest amount; ₹22,050 stops at 2 years; ₹24,310.13 runs to 4 years.", secs=40)

ci = 12500 * F(108, 100) * F(110, 100) - 12500
assert ci == 2350 and 12500 * F(18, 100) == 2250 and 12500 * F(109, 100) ** 2 - 12500 == F(9405, 4)
Q(T, "Annual compounding", B,
  "₹12,500 is invested at compound interest, compounded annually, at 8% for the first year and 10% for the second "
  "year. What is the compound interest for the two years?",
  "₹2,350", ["₹2,250", "₹2,351.25", "₹2,450"],
  "With different yearly rates, multiply the year factors: P × 1.08 × 1.10",
  "After year 1: 12,500 × 1.08 = 13,500. After year 2: 13,500 × 1.10 = 14,850. CI = 14,850 − 12,500 = ₹2,350.",
  ["Year 1 interest = 1,000 ⇒ 13,500", "Year 2 interest = 1,350 ⇒ 14,850", "CI = 2,350"],
  why="₹2,250 is simple interest (8% + 10% of 12,500); ₹2,351.25 averages the rates to 9% for both years.",
  secs=45)

P_ = F(8820, F(105, 100) ** 2)
assert P_ == 8000
Q(T, "Half-yearly and quarterly", I,
  "A sum amounts to ₹8,820 in 1 year at 10% per annum compound interest, compounded half-yearly. What is the sum?",
  "₹8,000", ["₹8,018.18", "₹7,938", "₹8,400"],
  "Half-yearly: rate halves (5%) and periods double (2)",
  "Amount = P × 1.05² = 1.1025P = 8,820, so P = 8,820 ÷ 1.1025 = ₹8,000.",
  ["Rate per half-year = 5%, periods = 2", "1.05² = 1.1025", "P = 8,820 ÷ 1.1025 = 8,000"],
  why="₹8,018.18 divides by 1.10 (annual compounding); ₹7,938 subtracts 10% of 8,820; ₹8,400 divides by 1.05 once.",
  secs=50)

assert 2 ** 3 == 8 and 4 * 3 == 12
Q(T, "Annual compounding", I,
  "A sum of money doubles itself in 4 years at compound interest, compounded annually. In how many years will it "
  "become 8 times itself at the same rate?",
  "12 years", ["16 years", "8 years", "14 years"],
  "At compound interest, equal time periods multiply the sum by the same factor",
  "Every 4 years the sum doubles. 8 = 2³, so it needs three doublings: 3 × 4 = 12 years.",
  ["×2 in 4 years", "8 = 2 × 2 × 2", "Time = 3 × 4 = 12 years"],
  why="16 years treats the growth as linear (8 ÷ 2 × 4); 8 years gives only 4 times.", secs=40)

x_ = F(31000) / (F(1, F(11, 10)) + F(2, F(121, 100)))
assert x_ == 12100 and F(12100, F(11, 10)) + F(24200, F(121, 100)) == 31000
Q(T, "Instalments", I,
  "A loan of ₹31,000 at 10% per annum compound interest, compounded annually, is repaid in two annual "
  "instalments, the first at the end of year 1 and the second at the end of year 2. The second instalment is "
  "twice the first. What is the first instalment?",
  "₹12,100", ["₹10,333.33", "₹11,000", "₹12,400"],
  "Loan = sum of the present values of the instalments",
  "If the first instalment is x, the present values are x ÷ 1.1 and 2x ÷ 1.21. So x(1.1 + 2) ÷ 1.21 = 31,000, which "
  "gives 3.1x = 37,510 and x = ₹12,100. The second instalment is ₹24,200.",
  ["31,000 = x/1.1 + 2x/1.21", "Multiply by 1.21: 37,510 = 1.1x + 2x = 3.1x", "x = 12,100",
   "Check: 11,000 + 20,000 = 31,000"],
  why="₹10,333.33 ignores interest (31,000 ÷ 3); ₹11,000 is the present value of the first instalment; ₹12,400 "
      "adds simple interest for 2 years and splits it 1 : 2.", secs=80)

bal = 100000
for _ in range(3):
    bal = bal * F(11, 10) - 20000
assert bal == 66900 and 100000 * F(1331, 1000) - 60000 == 73100
bal2 = 100000
for _ in range(3):
    bal2 = (bal2 - 20000) * F(11, 10)
assert bal2 == 60280
Q(T, "Annual compounding", A,
  "Meera invests ₹1,00,000 at 10% per annum compound interest, compounded annually. At the end of each year, just "
  "after the interest is added, she withdraws ₹20,000. How much remains in the account just after the third "
  "withdrawal?",
  "₹66,900", ["₹73,100", "₹70,000", "₹60,280"],
  "Add interest, then withdraw, year by year: each withdrawal stops earning interest",
  "Year 1: 1,10,000 − 20,000 = 90,000. Year 2: 99,000 − 20,000 = 79,000. Year 3: 86,900 − 20,000 = ₹66,900.",
  ["Year 1: 1,00,000 × 1.1 − 20,000 = 90,000", "Year 2: 90,000 × 1.1 − 20,000 = 79,000",
   "Year 3: 79,000 × 1.1 − 20,000 = 66,900"],
  why="₹73,100 subtracts all three withdrawals from the full compound amount, as if the withdrawn money kept earning; "
      "₹70,000 uses simple interest; ₹60,280 withdraws before adding interest.", secs=80)

P_ = F(290) / (F(36, 100) - (F(11, 10) ** 3 - 1))
assert P_ == 10000
Q(T, "CI vs SI difference", A,
  "The simple interest on a sum for 3 years at 12% per annum exceeds the compound interest on the same sum for 3 "
  "years at 10% per annum, compounded annually, by ₹290. What is the sum?",
  "₹10,000", ["₹12,000", "₹9,000", "₹14,500"],
  "Express both interests as fractions of P: SI = 36% of P, CI = (1.1³ − 1) = 33.1% of P",
  "SI = 0.36P. CI = (1.331 − 1)P = 0.331P. The difference 0.029P = 290, so P = ₹10,000.",
  ["SI = 12 × 3 = 36% of P", "CI = 1.1³ − 1 = 0.331 ⇒ 33.1% of P", "0.36P − 0.331P = 0.029P = 290", "P = 10,000"],
  why="₹14,500 uses 30% for the compound interest (simple interest at 10%); ₹12,000 and ₹9,000 give differences "
      "of ₹348 and ₹261.", secs=80)

r_ = next(r for r in range(1, 41) if 16000 * (1 + F(r, 200)) ** 4 == F(1944810, 100))
assert r_ == 10
Q(T, "Half-yearly and quarterly", A,
  "₹16,000 grows to ₹19,448.10 in 2 years at compound interest, compounded half-yearly. What is the rate of interest "
  "per annum?",
  "10%", ["5%", "12%", "20%"],
  "Half-yearly: amount = P(1 + r/200)⁴ over 2 years",
  "19,448.10 ÷ 16,000 = 1.21550625 = 1.05⁴. So the half-yearly rate is 5% and the annual rate is 10%.",
  ["Ratio = 19,448.10 ÷ 16,000 = 1.21550625", "1.05² = 1.1025 and 1.1025² = 1.21550625", "Half-yearly rate = 5%",
   "Annual rate = 10%"],
  why="5% is the half-yearly rate, not the annual one; 12% and 20% give amounts of ₹20,199.63 and ₹23,425.60.",
  secs=80)
assert near(16000 * 1.06 ** 4, 20199.63, 0.01) and near(16000 * 1.1 ** 4, 23425.6, 0.01)

# ================================================================ Partnership (B1 I2 A1)
T = "Partnership"
a_, b_ = 35000 * 8, 40000 * 6
share = F(26000 * a_, a_ + b_)
assert share == 14000 and near(F(26000 * 7, 15), 12133.33, 0.01)
Q(T, "Compound partnership", B,
  "A invests ₹35,000 for 8 months and B invests ₹40,000 for 6 months in a business. Out of a profit of ₹26,000, "
  "what is A's share?",
  "₹14,000", ["₹12,000", "₹12,133.33", "₹13,000"],
  "Profit is shared in the ratio of capital × time",
  "A: 35,000 × 8 = 2,80,000. B: 40,000 × 6 = 2,40,000. Ratio 7 : 6, so A gets 7/13 × 26,000 = ₹14,000.",
  ["A = 2,80,000; B = 2,40,000", "Ratio = 7 : 6", "A's share = 26,000 × 7 ÷ 13 = 14,000"],
  why="₹12,000 is B's share; ₹12,133.33 ignores time (ratio 7 : 8); ₹13,000 splits equally.", secs=40)

P_ = F(2400, F(52, 100) - F(48, 100))
assert P_ == 60000
Q(T, "Working partner", I,
  "A and B invest ₹60,000 and ₹90,000 in a firm. A manages the firm and first takes 20% of the profit as a "
  "management fee; the rest is shared in the ratio of their capitals. If A receives ₹2,400 more than B in all, what "
  "is the total profit?",
  "₹60,000", ["₹48,000", "₹12,000", "₹30,000"],
  "Write each partner's total receipt as a fraction of the profit",
  "Capitals are in the ratio 2 : 3. A gets 0.2P + 2/5 × 0.8P = 0.52P. B gets 3/5 × 0.8P = 0.48P. The difference "
  "0.04P = 2,400, so P = ₹60,000.",
  ["Fee = 0.2P; remainder 0.8P shared 2 : 3", "A = 0.2P + 0.32P = 0.52P", "B = 0.48P", "0.04P = 2,400 ⇒ P = 60,000"],
  why="₹12,000 treats ₹2,400 as the 20% fee; ₹48,000 is the shared remainder; ₹30,000 halves the answer.", secs=65)

parts = [3 * 4, 4 * 3, 5 * 2]
c_share = F(51000 * parts[2], sum(parts))
assert parts == [12, 12, 10] and c_share == 15000 and F(51000 * 5, 12) == 21250
Q(T, "Compound partnership", I,
  "The capitals of A, B and C are in the ratio 3 : 4 : 5, and the periods for which they invest are in the ratio "
  "4 : 3 : 2. Out of a profit of ₹51,000, what is C's share?",
  "₹15,000", ["₹21,250", "₹18,000", "₹12,750"],
  "Profit ratio = capital ratio × time ratio, term by term",
  "Capital × time: A 3 × 4 = 12, B 4 × 3 = 12, C 5 × 2 = 10. Ratio 6 : 6 : 5, so C gets 5/17 × 51,000 = ₹15,000.",
  ["A: 12, B: 12, C: 10", "Ratio 12 : 12 : 10 = 6 : 6 : 5", "C = 51,000 × 5 ÷ 17 = 15,000"],
  why="₹21,250 uses capitals only (5/12); ₹18,000 and ₹12,750 split by time only or by 1/4.", secs=55)

rest = 43000 - 8000 - 5000
a_total = 8000 + F(rest, 2)
assert a_total == 23000 and near(F(43000 * 8, 13), 26461.54, 0.01)
Q(T, "Simple partnership", A,
  "A and B invest ₹80,000 and ₹50,000 in a partnership. Under their agreement, each partner first receives interest "
  "on capital at 10% per annum, and the profit left after that is shared equally. If the profit for the year is "
  "₹43,000, how much does A receive in all?",
  "₹23,000", ["₹26,461.54", "₹21,500", "₹20,000"],
  "Apply the agreement in its order: interest on capital first, then the remainder",
  "Interest on capital: A gets 8,000 and B gets 5,000. Remaining profit = 43,000 − 13,000 = 30,000, shared equally, "
  "so 15,000 each. A receives 8,000 + 15,000 = ₹23,000.",
  ["Interest: A 8,000, B 5,000", "Remainder = 30,000", "Each gets 15,000", "A = 8,000 + 15,000 = 23,000"],
  why="₹26,461.54 shares the whole profit in the capital ratio 8 : 5; ₹21,500 shares it equally; ₹20,000 is B's "
      "total.", secs=75)

# ================================================================ Mixture and Alligation (B1 I3 A2)
T = "Mixture and Alligation"
milk = F(3, 4) + F(5, 8)
water = F(1, 4) + F(3, 8)
assert ratio(milk, water) == "11 : 5" and ratio(3 + 5, 1 + 3) == "2 : 1"
Q(T, "Mixing solutions", B,
  "Two vessels contain milk and water in the ratios 3 : 1 and 5 : 3. Equal quantities from the two vessels are "
  "mixed. What is the ratio of milk to water in the new mixture?",
  "11 : 5", ["2 : 1", "5 : 3", "4 : 1"],
  "Convert each ratio to a fraction of the vessel's contents, then add equal volumes",
  "Take 1 litre from each. Milk = 3/4 + 5/8 = 11/8 litres; water = 1/4 + 3/8 = 5/8 litres. Ratio = 11 : 5.",
  ["Vessel 1: milk 3/4, water 1/4", "Vessel 2: milk 5/8, water 3/8", "Milk = 11/8, water = 5/8", "Ratio 11 : 5"],
  why="2 : 1 adds the ratio terms (8 : 4), which is wrong because one vessel's ratio has 4 parts and the other 8; "
      "5 : 3 is the second vessel alone; 4 : 1 has no basis.", secs=45)

left = 60 * F(54, 60) * F(50, 60)
assert left == 45 and 60 * F(9, 10) ** 2 == F(486, 10)
Q(T, "Replacement of mixture", I,
  "A container holds 60 litres of pure milk. 6 litres are taken out and replaced with water. Then 10 litres of the "
  "mixture are taken out and replaced with water. How much milk is now in the container?",
  "45 litres", ["44 litres", "48.6 litres", "50 litres"],
  "Each replacement leaves the milk fraction multiplied by (1 − removed/total)",
  "After the first step the milk is 54 litres out of 60. Removing 10 litres of the mixture removes 10/60 of the milk, "
  "so 54 × 50/60 = 45 litres remain.",
  ["After step 1: 60 × 54/60 = 54 L milk", "Step 2 removes 1/6 of the mixture", "54 × 5/6 = 45 L"],
  why="44 L assumes the second 10 litres were pure milk; 48.6 L removes 6 litres both times; 50 L subtracts only "
      "the second removal.", secs=55)

avg = F(2 * 80 + 3 * 95, 5)
assert avg == 89 and avg * F(6, 5) == F(5340, 50) and F(80 + 95, 2) * F(6, 5) == 105
assert F(3 * 80 + 2 * 95, 5) * F(6, 5) == F(5160, 50)
Q(T, "Alligation rule", I,
  "A dealer mixes two varieties of pulses costing ₹80 and ₹95 per kg in the ratio 2 : 3. At what price per kg must "
  "he sell the mixture to gain 20%?",
  "₹106.80", ["₹105", "₹103.20", "₹89"],
  "Weighted average cost, then add the profit",
  "Cost of 5 kg = 2 × 80 + 3 × 95 = 445, so the cost is ₹89 per kg. For a 20% gain, SP = 89 × 1.2 = ₹106.80.",
  ["2 × 80 + 3 × 95 = 160 + 285 = 445", "Cost per kg = 445 ÷ 5 = 89", "SP = 89 × 1.2 = 106.80"],
  why="₹105 uses the simple average 87.5; ₹103.20 reverses the ratio (cost 86); ₹89 is the cost without profit.",
  secs=50)

salt = 40 * F(15, 100)
evap = 40 - salt / F(25, 100)
assert salt == 6 and evap == 16
Q(T, "Mixing solutions", I,
  "40 litres of a salt solution contain 15% salt. How many litres of water must be evaporated to make the solution "
  "25% salt?",
  "16 litres", ["24 litres", "10 litres", "15 litres"],
  "Evaporation removes only water: the amount of salt stays fixed",
  "Salt = 15% of 40 = 6 litres. For 6 litres to be 25% of the solution, the solution must be 24 litres. So 40 − 24 "
  "= 16 litres of water must be evaporated.",
  ["Salt = 6 L", "New volume = 6 ÷ 0.25 = 24 L", "Evaporate 40 − 24 = 16 L"],
  why="24 L is the volume left, not the water removed; 10 L uses (25 − 15)% of 40; 15 L has no basis.", secs=45)

m_ = 30 * F(2, 3) + 40 * F(3, 8) + 50 * F(7, 10)
w_ = 120 - m_
assert (m_, w_) == (70, 50) and ratio(2 + 3 + 7, 1 + 5 + 3) == "4 : 3"
Q(T, "Mixing solutions", A,
  "Three vessels hold 30 litres, 40 litres and 50 litres of milk–water mixtures in the ratios 2 : 1, 3 : 5 and "
  "7 : 3 respectively. All three are poured into one drum. What is the ratio of milk to water in the drum?",
  "7 : 5", ["4 : 3", "5 : 7", "3 : 2"],
  "Find the actual litres of milk in each vessel and add",
  "Milk: 30 × 2/3 = 20, 40 × 3/8 = 15, 50 × 7/10 = 35, total 70 litres. Water = 120 − 70 = 50 litres. Ratio 7 : 5.",
  ["Vessel 1: 20 L milk, 10 L water", "Vessel 2: 15 L milk, 25 L water", "Vessel 3: 35 L milk, 15 L water",
   "Milk 70 : water 50 = 7 : 5"],
  why="4 : 3 adds the ratio terms (12 : 9), ignoring the different volumes; 5 : 7 is inverted; 3 : 2 averages the "
      "fractions.", secs=75)

x_ = next(x for x in range(1, 60) if F(45, 60) * (60 - x) == F(1, 2) * 60)
assert x_ == 20
Q(T, "Replacement of mixture", A,
  "A 60-litre container is full of milk and water in the ratio 3 : 1. How much of the mixture must be drawn off and "
  "replaced with water so that the container holds equal amounts of milk and water?",
  "20 litres", ["15 litres", "30 litres", "22.5 litres"],
  "Only the milk fraction falls during replacement; the total stays 60 litres",
  "Milk is 45 litres. After drawing off x litres, milk = 45 × (60 − x)/60. For a 1 : 1 mixture, milk must be 30 "
  "litres: 45(60 − x)/60 = 30, so 60 − x = 40 and x = 20 litres.",
  ["Milk now = 45 L", "Target milk = 30 L (half of 60)", "45 × (60 − x)/60 = 30 ⇒ 60 − x = 40", "x = 20 L"],
  why="15 L is the water already present; 30 L is the water you would add without drawing anything off (and the "
      "container would overflow); 22.5 L assumes pure milk is drawn off and halves the milk.", secs=80)

# ================================================================ Time and Work (B1 I1 A1)
T = "Time and Work"
days = 1 / (F(1, 20) * F(5, 4) + F(1, 20))
assert days == F(80, 9)
Q(T, "Work efficiency", B,
  "A is 25% more efficient than B. B alone can finish a job in 20 days. In how many days can A and B together finish "
  "it?",
  "8 8/9 days", ["16 days", "10 days", "9 days"],
  "Efficiency is work per day; 25% more efficient means 1.25 times the daily work",
  "B does 1/20 of the job a day, so A does 1.25/20 = 1/16. Together: 1/20 + 1/16 = 9/80 per day, so the job takes "
  "80/9 = 8 8/9 days.",
  ["B = 1/20 per day", "A = 1.25 × 1/20 = 1/16 per day", "Together = 4/80 + 5/80 = 9/80", "Time = 80/9 = 8 8/9 days"],
  why="16 days is A alone; 10 days assumes A and B are equally fast; 9 days rounds 80/9.", secs=45)

day = 1 / (F(1, 4 * 26) + F(1, 6 * 26) + F(1, 8 * 26))
assert day == 48
Q(T, "Men-women-children", I,
  "A job can be finished by 4 men in 26 days, or by 6 women in 26 days, or by 8 children in 26 days. In how many "
  "days can 1 man, 1 woman and 1 child working together finish it?",
  "48 days", ["52 days", "39 days", "36 days"],
  "Find each person's daily share of the job",
  "One man does 1/104 of the job a day, one woman 1/156 and one child 1/208. Together: 6/624 + 4/624 + 3/624 = "
  "13/624 = 1/48. So they take 48 days.",
  ["Man = 1/(4 × 26) = 1/104", "Woman = 1/(6 × 26) = 1/156", "Child = 1/(8 × 26) = 1/208",
   "Sum = 13/624 = 1/48 ⇒ 48 days"],
  why="52 days counts the trio as only 2 men; 39 days treats them as 2⅔ men; 36 days has no basis.", secs=65)

t_ = next(t for t in range(1, 40) if F(t - 2, 10) + F(t - 3, 15) + F(t, 30) == 1)
assert t_ == 7
Q(T, "Work efficiency", A,
  "A, B and C can finish a job alone in 10, 15 and 30 days respectively. They start together, but A leaves 2 days "
  "before the job is finished and B leaves 3 days before it is finished. In how many days is the job finished?",
  "7 days", ["5 days", "8 days", "6 days"],
  "Let the total be t days: A works t − 2 days, B t − 3 days and C all t days",
  "(t − 2)/10 + (t − 3)/15 + t/30 = 1. Multiply by 30: 3(t − 2) + 2(t − 3) + t = 30, so 6t − 12 = 30 and t = 7.",
  ["A's work = (t − 2)/10", "B's work = (t − 3)/15", "C's work = t/30", "3t − 6 + 2t − 6 + t = 30 ⇒ 6t = 42",
   "t = 7 days"],
  why="5 days is the time if all three worked throughout; 8 and 6 days do not make the work add up to 1.", secs=90)

# ================================================================ Pipes and Cisterns (B1 I1 A1)
T = "Pipes and Cisterns"
t_ = 1 / (F(1, 10) + F(1, 15) - F(1, 20))
assert t_ == F(60, 7)
Q(T, "Inlet and outlet", B,
  "Pipes A and B can fill a tank in 10 hours and 15 hours, and pipe C can empty the full tank in 20 hours. If all "
  "three are opened together on the empty tank, in how many hours will it be full?",
  "8 4/7 hours", ["6 hours", "12 hours", "10 hours"],
  "Add filling rates and subtract emptying rates",
  "Net rate = 1/10 + 1/15 − 1/20 = 6/60 + 4/60 − 3/60 = 7/60 of the tank per hour. Time = 60/7 = 8 4/7 hours.",
  ["A + B = 1/10 + 1/15 = 1/6", "Net = 1/6 − 1/20 = 7/60", "Time = 60/7 = 8 4/7 hours"],
  why="6 hours ignores pipe C; 12 hours takes the net rate as 1/12; 10 hours ignores pipe B and C.", secs=45)

t_ = F(1, 2) / F(1, 6) + F(1, 2) / (F(1, 6) - F(1, 9))
assert t_ == 12
Q(T, "Inlet and outlet", I,
  "An inlet pipe can fill a tank in 6 hours. When the tank is half full, an outlet pipe that can empty the full tank "
  "in 9 hours is also opened. How long does it take to fill the tank completely, starting from empty?",
  "12 hours", ["9 hours", "18 hours", "10.5 hours"],
  "Split the filling into two stages with different net rates",
  "The first half takes 3 hours. Then the net rate is 1/6 − 1/9 = 1/18 per hour, so the second half takes "
  "(1/2) ÷ (1/18) = 9 hours. Total = 12 hours.",
  ["First half: ½ ÷ 1/6 = 3 hours", "Net rate = 1/6 − 1/9 = 1/18", "Second half: ½ × 18 = 9 hours",
   "Total = 3 + 9 = 12 hours"],
  why="9 hours is the second stage alone; 18 hours runs both pipes from the start; 10.5 hours adds 3 hours to "
      "half of the 15 hours the second stage would take from empty.", secs=60)

# brute-force simulation in exact fractions: A on odd hours, B on even hours
filled, hour = F(0), 0
while True:
    rate = F(1, 12) if hour % 2 == 0 else F(1, 15)
    if filled + rate >= 1:
        total = hour + (1 - filled) / rate
        break
    filled += rate
    hour += 1
assert total == F(53, 4)
Q(T, "Inlet and outlet", A,
  "Pipes A and B can fill a tank in 12 hours and 15 hours respectively. They are opened alternately for one hour "
  "each, starting with A, on an empty tank. How long will it take to fill the tank?",
  "13 hours 15 minutes", ["13 hours 20 minutes", "13 hours 30 minutes", "14 hours"],
  "Find the work done in each 2-hour cycle, then finish the last part carefully",
  "One cycle (A then B) fills 1/12 + 1/15 = 9/60 = 3/20. After 6 cycles (12 hours) 18/20 is full, leaving 1/10. "
  "In the 13th hour A fills 1/12, leaving 1/10 − 1/12 = 1/60. B fills 1/60 in (1/60) ÷ (1/15) = 1/4 hour. "
  "Total = 13 hours 15 minutes.",
  ["Cycle = 1/12 + 1/15 = 3/20 per 2 hours", "6 cycles = 12 hours ⇒ 9/10 full", "Hour 13 (A): 1/10 − 1/12 = 1/60 "
   "left", "B needs 1/60 × 15 = 1/4 hour", "Total = 13¼ hours = 13 h 15 min"],
  why="13 h 20 min gives B 1/3 hour for the last 1/60 (as if B filled the tank in 20 hours); 13 h 30 min and "
      "14 hours round the last part up.", secs=100, by=BRUTE)

# ================================================================ Speed, Time and Distance (B3 I2 A1)
T = "Speed, Time and Distance"
avg = F(2 * 45 + 3 * 60, 5)
assert avg == 54 and F(45 + 60, 2) == F(105, 2)
Q(T, "Average speed", B,
  "A car travels for 2 hours at 45 km/h and then for 3 hours at 60 km/h. What is its average speed for the whole "
  "journey?",
  "54 km/h", ["52.5 km/h", "55 km/h", "50 km/h"],
  "Average speed = total distance ÷ total time",
  "Distance = 2 × 45 + 3 × 60 = 90 + 180 = 270 km in 5 hours, so the average speed is 54 km/h.",
  ["Distance 1 = 90 km", "Distance 2 = 180 km", "270 ÷ 5 = 54 km/h"],
  why="52.5 km/h averages the two speeds without weighting by time; 55 and 50 km/h use 275 or 250 km.", secs=35)

rel = F(72 - 54) * F(5, 18)
t_ = 600 / rel
assert rel == 5 and t_ == 120 and near(600 / (F(126) * F(5, 18)), 17.14, 0.01)
Q(T, "Relative speed", B,
  "A police jeep chases a car that is 600 m ahead on the same road. The jeep runs at 72 km/h and the car at 54 km/h. "
  "How long will the jeep take to catch the car?",
  "2 minutes", ["33⅓ seconds", "17.14 seconds", "1 minute"],
  "Same direction: relative speed = difference of speeds; convert km/h to m/s with × 5/18",
  "Relative speed = 72 − 54 = 18 km/h = 18 × 5/18 = 5 m/s. Time = 600 ÷ 5 = 120 seconds = 2 minutes.",
  ["Relative speed = 18 km/h = 5 m/s", "Time = 600 ÷ 5 = 120 s", "= 2 minutes"],
  why="33⅓ seconds divides 600 by 18 without converting units; 17.14 seconds adds the speeds; 1 minute halves the "
      "time.", secs=40)

t_ = F(30, 4 + 6)
assert t_ == 3 and 4 * t_ == 12
Q(T, "Meeting and overtaking", B,
  "Two friends start at the same time from towns A and B, 30 km apart, and walk towards each other at 4 km/h and "
  "6 km/h respectively. How far from A do they meet?",
  "12 km", ["18 km", "15 km", "10 km"],
  "Towards each other: relative speed = sum of speeds; each walks for the same time",
  "They close the gap at 4 + 6 = 10 km/h, so they meet after 30 ÷ 10 = 3 hours. The friend from A has walked "
  "4 × 3 = 12 km.",
  ["Relative speed = 10 km/h", "Time = 3 hours", "Distance from A = 4 × 3 = 12 km"],
  short="The distance splits in the ratio of speeds 4 : 6, so A's part = 30 × 4/10 = 12 km.",
  why="18 km is the distance from B; 15 km assumes equal speeds; 10 km is the distance covered in one hour.",
  secs=35)

d_ = 6 / (F(1, 30) + F(1, 60))
assert d_ == 120
Q(T, "Average speed", I,
  "A car goes up a hill road at 30 km/h and comes back down the same road at 60 km/h. The round trip takes 6 hours. "
  "How long is the road one way?",
  "120 km", ["135 km", "90 km", "180 km"],
  "Time up + time down = total time",
  "d/30 + d/60 = 6, so (2d + d)/60 = 6, 3d = 360 and d = 120 km.",
  ["d/30 + d/60 = 6", "3d/60 = 6", "d = 120 km"],
  short="The average speed for the round trip is 2 × 30 × 60 ÷ 90 = 40 km/h, so the round trip is 240 km.",
  why="135 km uses the simple average 45 km/h; 90 km and 180 km use 30 km/h or 60 km/h for the whole trip.",
  secs=50)

t_ = F(400, 6 + 4) * 3
assert t_ == 120
Q(T, "Meeting and overtaking", I,
  "Two runners start together from the same point on a 400 m circular track and run in opposite directions at "
  "6 m/s and 4 m/s. After how many seconds will they meet for the third time?",
  "120 seconds", ["40 seconds", "200 seconds", "600 seconds"],
  "Opposite directions on a loop: they meet each time they jointly cover one full lap",
  "Together they cover 6 + 4 = 10 m every second, so they meet every 400 ÷ 10 = 40 seconds. The third meeting is at "
  "3 × 40 = 120 seconds.",
  ["Relative speed = 10 m/s", "One meeting every 40 s", "Third meeting at 120 s"],
  why="40 s is the first meeting; 200 s is when they are next together at the start; 600 s uses the same-direction "
      "speed 2 m/s.", secs=50)

v_ = next(v for v in range(1, 200) if F(480, v) - F(480, v + 8) == 2)
assert v_ == 40
Q(T, "Average speed", A,
  "A car would take 2 hours less to cover 480 km if its speed were 8 km/h more. What is its usual speed?",
  "40 km/h", ["48 km/h", "32 km/h", "36 km/h"],
  "Set up time at the usual speed minus time at the faster speed",
  "480/v − 480/(v + 8) = 2. This gives 480 × 8 = 2v(v + 8), i.e. v² + 8v − 1,920 = 0 = (v − 40)(v + 48). So "
  "v = 40 km/h (speed is positive).",
  ["480/v − 480/(v + 8) = 2", "3,840 = 2v(v + 8) ⇒ v² + 8v − 1,920 = 0", "(v − 40)(v + 48) = 0 ⇒ v = 40",
   "Check: 12 hours at 40 km/h, 10 hours at 48 km/h"],
  why="48 km/h is the faster speed; 32 and 36 km/h give time savings of 3 hours and about 2.4 hours.", secs=80)

# ================================================================ Boats and Streams (B2 I2 A1)
T = "Boats and Streams"
assert F(20 - 12, 2) == 4 and F(20 + 12, 2) == 16
Q(T, "Speed of stream", B,
  "A boat goes downstream at 20 km/h and upstream at 12 km/h. What is the speed of the stream?",
  "4 km/h", ["8 km/h", "16 km/h", "6 km/h"],
  "Stream speed = (downstream − upstream) ÷ 2",
  "Downstream = b + s = 20 and upstream = b − s = 12. Subtracting, 2s = 8, so s = 4 km/h (and b = 16 km/h).",
  ["b + s = 20", "b − s = 12", "2s = 8 ⇒ s = 4 km/h"],
  why="8 km/h forgets to halve; 16 km/h is the boat's speed in still water.", secs=30)

t_ = F(35, 12 - 2)
assert t_ == F(7, 2)
Q(T, "Upstream and downstream", B,
  "A boat's speed in still water is 12 km/h and the stream flows at 2 km/h. How long will the boat take to go 35 km "
  "upstream?",
  "3 hours 30 minutes", ["2 hours 30 minutes", "2 hours 55 minutes", "3 hours"],
  "Upstream speed = boat speed − stream speed",
  "Upstream speed = 12 − 2 = 10 km/h, so 35 km takes 3.5 hours = 3 hours 30 minutes.",
  ["Upstream speed = 10 km/h", "Time = 35 ÷ 10 = 3.5 h"],
  why="2 hours 30 minutes uses the downstream speed 14 km/h; 2 hours 55 minutes ignores the stream.", secs=35)

s_ = next(s for s in range(1, 20) if F(48, 20 + s) + F(48, 20 - s) == 5)
assert s_ == 4
Q(T, "Speed of stream", I,
  "A motorboat whose speed in still water is 20 km/h goes 48 km downstream and comes back in a total of 5 hours. "
  "What is the speed of the stream?",
  "4 km/h", ["5 km/h", "3 km/h", "2 km/h"],
  "Total time = d/(b + s) + d/(b − s)",
  "48/(20 + s) + 48/(20 − s) = 5 gives 48 × 40 = 5(400 − s²), so 400 − s² = 384, s² = 16 and s = 4 km/h.",
  ["48 × 40 ÷ (400 − s²) = 5", "400 − s² = 384", "s = 4 km/h", "Check: 48/24 + 48/16 = 2 + 3 = 5 h"],
  why="5, 3 and 2 km/h give round-trip times of about 5.12, 4.91 and 4.85 hours.", secs=60)

d_ = next(d for d in range(2, 200, 2) if F(d, 12) + F(d // 2, 8) == 7)
assert d_ == 48
Q(T, "Upstream and downstream", I,
  "A boat's speed in still water is 10 km/h and the stream flows at 2 km/h. It goes downstream from A to B and then "
  "comes back upstream to C, the midpoint of AB. The whole trip takes 7 hours. What is the distance AB?",
  "48 km", ["42 km", "56 km", "36 km"],
  "Downstream for the full distance, upstream for half of it",
  "Downstream speed = 12 km/h and upstream speed = 8 km/h. d/12 + (d/2)/8 = 7, so d/12 + d/16 = 7, 7d/48 = 7 and "
  "d = 48 km.",
  ["Down = 12 km/h, up = 8 km/h", "d/12 + d/16 = 7", "(4d + 3d)/48 = 7 ⇒ d = 48 km"],
  why="42 km and 56 km give 6.1 and 8.2 hours; 36 km gives 5.25 hours.", secs=60)

d_ = next(F(d, 2) for d in range(1, 60) if F(30, F(6, 10) * F(d, 2)) + F(30, F(d, 2)) == 8)
u_ = F(6, 10) * d_
assert (d_, u_) == (10, 6) and F(d_ + u_, 2) == 8
Q(T, "Upstream and downstream", A,
  "A boat's upstream speed is 60% of its downstream speed. It goes 30 km upstream and returns to its starting point "
  "in 8 hours. What is the speed of the boat in still water?",
  "8 km/h", ["10 km/h", "6 km/h", "9 km/h"],
  "Write both speeds with one unknown; still-water speed = (down + up) ÷ 2",
  "Let downstream speed be d; upstream is 0.6d. 30/(0.6d) + 30/d = 8 gives 50/d + 30/d = 80/d = 8, so d = 10 km/h "
  "and upstream = 6 km/h. Still-water speed = (10 + 6) ÷ 2 = 8 km/h.",
  ["30/(0.6d) = 50/d", "50/d + 30/d = 8 ⇒ d = 10", "Upstream = 6 km/h", "Boat = (10 + 6) ÷ 2 = 8 km/h"],
  why="10 km/h is the downstream speed and 6 km/h the upstream speed; 9 km/h has no basis.", secs=80)

# ================================================================ Problems on Trains (B1 I2 A1)
T = "Problems on Trains"
v_ = F(150, 9) * F(18, 5)
assert v_ == 60
Q(T, "Crossing a pole or platform", B,
  "A train 150 m long crosses a signal pole in 9 seconds. What is its speed in km/h?",
  "60 km/h", ["54 km/h", "72 km/h", "50 km/h"],
  "Crossing a pole: distance = length of the train; m/s × 18/5 = km/h",
  "Speed = 150 ÷ 9 = 50/3 m/s = 50/3 × 18/5 = 60 km/h.",
  ["Speed = 150 ÷ 9 = 16⅔ m/s", "16⅔ × 18/5 = 60 km/h"],
  why="54 and 72 km/h use 15 or 20 m/s; 50 km/h uses × 3 instead of × 3.6.", secs=30)

v_ = F(330 - 180, 21 - 15)
L_ = 15 * v_ - 180
assert (v_, L_) == (25, 195) and v_ * F(18, 5) == 90
Q(T, "Crossing a pole or platform", I,
  "A train crosses a 180 m long bridge in 15 seconds and a 330 m long tunnel in 21 seconds at the same speed. What is "
  "the length of the train?",
  "195 m", ["225 m", "150 m", "175 m"],
  "The extra length (330 − 180) takes the extra time (21 − 15)",
  "The extra 150 m takes 6 seconds, so the speed is 25 m/s. In 15 seconds the train covers 375 m = its length + "
  "180, so its length is 195 m.",
  ["Speed = 150 ÷ 6 = 25 m/s (90 km/h)", "15 × 25 = 375 m", "Length = 375 − 180 = 195 m"],
  why="150 m is the difference in the lengths of the tunnel and the bridge; 225 m and 175 m give different "
      "speeds for the bridge and the tunnel (225 m: 27 m/s and 26.4 m/s).", secs=55)

t_ = F(200 + 160, (72 - 54) * F(5, 18))
assert t_ == 72 and near(F(360, (72 + 54) * F(5, 18)), 10.29, 0.01)
Q(T, "Trains crossing each other", I,
  "Two trains 200 m and 160 m long run on parallel tracks in the same direction at 72 km/h and 54 km/h. How long "
  "will the faster train take to pass the slower one completely?",
  "72 seconds", ["10.29 seconds", "20 seconds", "36 seconds"],
  "Same direction: relative speed = difference; distance = sum of lengths",
  "Relative speed = 72 − 54 = 18 km/h = 5 m/s. The faster train must gain 200 + 160 = 360 m, which takes 360 ÷ 5 = "
  "72 seconds.",
  ["Relative speed = 18 km/h = 5 m/s", "Distance = 360 m", "Time = 72 s"],
  why="10.29 seconds adds the speeds (opposite directions); 20 seconds uses 360 ÷ 18 without converting; 36 seconds "
      "uses only half the combined length.", secs=50)

v1 = F(500, 10)
v2 = F(500, 50)
fast = (v1 + v2) / 2
assert (v1, v2, fast) == (50, 10, 30) and fast * F(18, 5) == 108
Q(T, "Trains crossing each other", A,
  "Two trains 260 m and 240 m long run on parallel tracks. They cross each other completely in 10 seconds when "
  "moving in opposite directions and in 50 seconds when moving in the same direction. What is the speed of the "
  "faster train in km/h?",
  "108 km/h", ["72 km/h", "90 km/h", "126 km/h"],
  "Opposite directions give the sum of speeds; same direction gives the difference",
  "Total length = 500 m. Sum of speeds = 500 ÷ 10 = 50 m/s; difference = 500 ÷ 50 = 10 m/s. The faster train's "
  "speed = (50 + 10) ÷ 2 = 30 m/s = 108 km/h.",
  ["u + v = 50 m/s", "u − v = 10 m/s", "u = 30 m/s", "30 × 18/5 = 108 km/h"],
  why="72 km/h is the slower train (20 m/s); 90 km/h uses the average 25 m/s; 126 km/h uses 35 m/s.", secs=80)

# ================================================================ Mensuration (B1 I1 A2)
T = "Mensuration"
side = math.isqrt(2025)
assert side * side == 2025 and 4 * side * 15 == 2700
Q(T, "2D areas and perimeters", B,
  "A square field has an area of 2,025 m². What is the cost of fencing it all round at ₹15 per metre?",
  "₹2,700", ["₹675", "₹1,350", "₹30,375"],
  "Side of a square = √area; fencing runs along the perimeter",
  "Side = √2,025 = 45 m. Perimeter = 4 × 45 = 180 m. Cost = 180 × 15 = ₹2,700.",
  ["√2,025 = 45 m", "Perimeter = 180 m", "Cost = 180 × 15 = 2,700"],
  why="₹675 fences one side only; ₹1,350 two sides; ₹30,375 multiplies the area by the rate.", secs=35)

vol = F(2, 3) * F(22, 7) * F(21, 2) ** 3
assert vol == F(48510, 20) and vol * 2 == 4851
Q(T, "Cylinder, cone and sphere", I,
  "How much liquid can a hemispherical bowl of internal radius 10.5 cm hold? (Use π = 22/7.)",
  "2,425.5 cm³", ["4,851 cm³", "1,212.75 cm³", "3,638.25 cm³"],
  "Volume of a hemisphere = (2/3)πr³",
  "r³ = 10.5³ = 1,157.625. Volume = 2/3 × 22/7 × 1,157.625 = 2,425.5 cm³.",
  ["r³ = 1,157.625", "22/7 × 1,157.625 = 3,638.25", "× 2/3 = 2,425.5 cm³"],
  why="4,851 cm³ is the full sphere; 1,212.75 cm³ is a quarter-sphere; 3,638.25 cm³ forgets the 2/3.", secs=55)

k_ = next(k for k in range(1, 50) if 2 * (4 * 3 + 3 * 2 + 2 * 4) * k * k == 1872)
assert k_ == 6 and (4 * k_) * (3 * k_) * (2 * k_) == 5184
Q(T, "3D volume and surface area", A,
  "The length, breadth and height of a cuboid are in the ratio 4 : 3 : 2, and its total surface area is 1,872 cm². "
  "What is its volume?",
  "5,184 cm³", ["2,592 cm³", "1,728 cm³", "6,912 cm³"],
  "TSA of a cuboid = 2(lb + bh + hl); write each side as a multiple of k",
  "With sides 4k, 3k, 2k: TSA = 2(12k² + 6k² + 8k²) = 52k² = 1,872, so k² = 36 and k = 6. The sides are 24, 18 and "
  "12 cm, and the volume is 24 × 18 × 12 = 5,184 cm³.",
  ["TSA = 2(12 + 6 + 8)k² = 52k²", "52k² = 1,872 ⇒ k = 6", "Sides: 24, 18, 12 cm", "Volume = 5,184 cm³"],
  why="2,592 cm³ is half the volume; 1,728 cm³ is 12³; 6,912 cm³ uses a height of 16 cm.", secs=75)

total = 2 * 6 * 15 + 6 * 6 + 6 * math.isqrt(36 + 64)
assert total == 276 and math.isqrt(100) ** 2 == 100
Q(T, "Cylinder, cone and sphere", A,
  "A solid cylinder has a base radius of 6 cm and a height of 15 cm. A cone of the same base radius and height 8 cm "
  "is hollowed out from one end. What is the total surface area of the remaining solid?",
  "276π cm²", ["312π cm²", "240π cm²", "216π cm²"],
  "Count every exposed surface: the cylinder's curved surface, the uncut base, and the inside of the cone (its "
  "curved surface); the cut base is gone",
  "Curved surface of the cylinder = 2π × 6 × 15 = 180π. The intact base = π × 6² = 36π. The cone's slant height = "
  "√(6² + 8²) = 10, so its curved surface = π × 6 × 10 = 60π. Total = 180π + 36π + 60π = 276π cm².",
  ["Cylinder curved surface = 180π", "Bottom base = 36π (the top base is removed)", "Cone slant = √(36 + 64) = 10",
   "Cone curved surface = 60π", "Total = 276π cm²"],
  why="312π also counts the removed top base; 240π leaves out the bottom base; 216π ignores the hollow cone.",
  secs=100)

# ================================================================ Probability (B2 I2 A2)
T = "Probability"
dice = list(itertools.product(range(1, 7), repeat=2))
p = F(sum(1 for a, b in dice if math.isqrt(a * b) ** 2 == a * b), 36)
assert p == F(2, 9)
Q(T, "Coins and dice", B,
  "Two fair dice are rolled. What is the probability that the product of the two numbers is a perfect square?",
  "2/9", ["1/6", "7/36", "1/4"],
  "List the favourable outcomes among the 36 equally likely pairs",
  "Products that are perfect squares: doubles (1,1), (2,2), …, (6,6) give 1, 4, 9, 16, 25, 36 (6 outcomes), and "
  "(1,4) and (4,1) give 4. That is 8 outcomes, so P = 8/36 = 2/9.",
  ["Doubles: 6 outcomes", "(1, 4) and (4, 1): product 4", "8 favourable of 36", "P = 2/9"],
  why="1/6 counts only the doubles; 7/36 counts (1, 4) but not (4, 1).", secs=45, by=BRUTE)

deck = [(r, s) for r in range(1, 14) for s in "HDCS"]
p = F(sum(1 for r, s in deck if s in "HD" and 2 <= r <= 10), 52)
assert p == F(9, 26) and F(sum(1 for r, s in deck if 2 <= r <= 10), 52) == F(9, 13)
assert F(sum(1 for r, s in deck if s in "HD" and r <= 10), 52) == F(5, 13)
Q(T, "Cards", B,
  "One card is drawn at random from a well-shuffled pack of 52 cards. What is the probability that it is a red card "
  "bearing a number from 2 to 10?",
  "9/26", ["9/13", "5/13", "1/2"],
  "Count the favourable cards: 9 numbered cards in each red suit",
  "Each red suit (hearts and diamonds) has the numbered cards 2 to 10, which is 9 cards. So 18 cards are favourable "
  "and P = 18/52 = 9/26.",
  ["Numbered cards per suit: 2 to 10 = 9", "Two red suits ⇒ 18 cards", "P = 18/52 = 9/26"],
  why="9/13 counts numbered cards of all four suits; 5/13 includes the red aces; 1/2 counts every red card.",
  secs=35, by=BRUTE)

balls = ["R"] * 5 + ["B"] * 7
draws = list(itertools.permutations(range(12), 2))
p = F(sum(1 for i, j in draws if balls[j] == "R"), len(draws))
assert p == F(5, 12)
Q(T, "Balls from bags", I,
  "A bag contains 5 red and 7 blue balls. Two balls are drawn one after the other without replacement. What is the "
  "probability that the second ball is red?",
  "5/12", ["5/11", "4/11", "35/132"],
  "Total probability over the colour of the first ball (or symmetry: every position is equally likely to hold any "
  "ball)",
  "P = P(R first) × 4/11 + P(B first) × 5/11 = 5/12 × 4/11 + 7/12 × 5/11 = (20 + 35)/132 = 55/132 = 5/12.",
  ["First red: 5/12 × 4/11 = 20/132", "First blue: 7/12 × 5/11 = 35/132", "Total = 55/132 = 5/12"],
  short="Without any information about the first ball, the second is like a fresh draw: 5/12.",
  why="5/11 assumes the first ball was blue; 4/11 assumes it was red; 35/132 is only the blue-then-red case.",
  secs=60, by=BRUTE)

outs = list(itertools.product("HT", "HT", "HT", range(1, 7)))
p = F(sum(1 for *c, d in outs if c.count("H") == 2 and d % 2 == 0), len(outs))
assert p == F(3, 16)
Q(T, "Coins and dice", I,
  "Three fair coins are tossed and a fair die is rolled. What is the probability of getting exactly two heads and an "
  "even number on the die?",
  "3/16", ["3/8", "1/4", "7/16"],
  "Independent events: multiply their probabilities",
  "P(exactly two heads) = 3/8 (HHT, HTH, THH out of 8). P(even) = 1/2. P(both) = 3/8 × 1/2 = 3/16.",
  ["Exactly 2 heads: 3 of 8 outcomes", "Even on die: 3 of 6", "3/8 × 1/2 = 3/16"],
  why="3/8 ignores the die; 1/4 uses P(two heads) = 1/2; 7/16 adds the probabilities instead of multiplying.",
  secs=50, by=BRUTE)

pairs = list(itertools.combinations(deck, 2))
fav = sum(1 for a, b in pairs if (a[0] == 13 and b[0] == 13) or (a[1] in "HD" and b[1] in "HD"))
p = F(fav, len(pairs))
assert len(pairs) == 1326 and fav == 330 and p == F(55, 221) and F(325, 1326) == F(25, 102)
Q(T, "Cards", A,
  "Two cards are drawn together at random from a well-shuffled pack of 52 cards. What is the probability that both "
  "are kings or both are red?",
  "55/221", ["331/1326", "25/102", "1/221"],
  "Addition rule: P(A or B) = P(A) + P(B) − P(A and B)",
  "Total pairs = C(52, 2) = 1,326. Both kings: C(4, 2) = 6. Both red: C(26, 2) = 325. Both red kings: 1 (the king of "
  "hearts and the king of diamonds). Favourable = 6 + 325 − 1 = 330, so P = 330/1,326 = 55/221.",
  ["C(52, 2) = 1,326", "Both kings = 6", "Both red = 325", "Overlap (two red kings) = 1",
   "330/1,326 = 55/221"],
  why="331/1,326 adds 6 + 325 without removing the pair of red kings counted twice; 25/102 is 'both red' alone; "
      "1/221 is 'both kings' alone.", secs=100, by=BRUTE)

bagA = ["R"] * 4 + ["G"] * 6
bagB = ["R"] * 7 + ["G"] * 3
pA = F(sum(1 for x, y in itertools.combinations(bagA, 2) if x == y == "R"), 45)
pB = F(sum(1 for x, y in itertools.combinations(bagB, 2) if x == y == "R"), 45)
p = F(1, 2) * pA + F(1, 2) * pB
assert (pA, pB, p) == (F(2, 15), F(7, 15), F(3, 10))
Q(T, "Balls from bags", A,
  "Bag A contains 4 red and 6 green balls; bag B contains 7 red and 3 green balls. A fair coin is tossed: on heads "
  "bag A is chosen, on tails bag B. Two balls are then drawn together from the chosen bag. What is the probability "
  "that both balls are red?",
  "3/10", ["3/5", "13/40", "2/15"],
  "Total probability: weight each bag's probability by the chance of choosing it",
  "From A: C(4, 2)/C(10, 2) = 6/45. From B: C(7, 2)/C(10, 2) = 21/45. P = ½ × 6/45 + ½ × 21/45 = 27/90 = 3/10.",
  ["P(both red | A) = 6/45 = 2/15", "P(both red | B) = 21/45 = 7/15", "P = ½(2/15 + 7/15) = 9/30 = 3/10"],
  why="3/5 forgets the ½ for choosing a bag; 13/40 draws with replacement; 2/15 uses bag A only.", secs=90,
  by=BRUTE)

# ================================================================ Permutation and Combination (B1 I2 A1)
T = "Permutation and Combination"
n_ = len(set(itertools.permutations("RUPEE")))
assert n_ == 60
Q(T, "Word arrangements", B, "In how many different ways can the letters of the word RUPEE be arranged?",
  "60", ["120", "30", "24"],
  "Arrangements with a repeated letter: n! ÷ (repeats)!",
  "RUPEE has 5 letters with E twice. Arrangements = 5! ÷ 2! = 120 ÷ 2 = 60.",
  ["5 letters, E repeated twice", "5! = 120", "120 ÷ 2! = 60"],
  why="120 treats the two Es as different; 30 divides by 4; 24 is 4!.", secs=30, by=BRUTE)

bag = ["R"] * 5 + ["W"] * 4
n_ = sum(1 for c in itertools.combinations(range(9), 3) if any(bag[i] == "W" for i in c))
assert n_ == 74 == math.comb(9, 3) - math.comb(5, 3)
Q(T, "Selections", I,
  "A bag contains 5 red and 4 white balls. In how many ways can 3 balls be selected so that at least one of them is "
  "white?",
  "74", ["84", "64", "80"],
  "'At least one' = all selections − selections with none",
  "All selections of 3 from 9 = C(9, 3) = 84. Selections with no white ball = C(5, 3) = 10. So 84 − 10 = 74.",
  ["C(9, 3) = 84", "All red: C(5, 3) = 10", "84 − 10 = 74"],
  why="84 is every selection; 64 subtracts 20; 80 subtracts only C(4, 3) = 4 (the all-white selections).", secs=50,
  by=BRUTE)

n_ = sum(1 for p_ in itertools.permutations(range(7), 4) if p_[0] != 0 and p_[3] % 2 == 0)
assert n_ == 420
Q(T, "Arrangements", I,
  "How many four-digit even numbers can be formed with the digits 0, 1, 2, 3, 4, 5 and 6 if no digit is repeated?",
  "420", ["360", "480", "400"],
  "Fill the restricted places first; treat the case of 0 in the units place separately",
  "Units digit 0: the other three places can be filled in 6 × 5 × 4 = 120 ways. Units digit 2, 4 or 6: the "
  "thousands digit cannot be 0 or the units digit, so 5 choices, then 5 and 4: 3 × 5 × 5 × 4 = 300. Total = 420.",
  ["Units = 0: 6 × 5 × 4 = 120", "Units = 2, 4 or 6: 3 × (5 × 5 × 4) = 300", "Total = 420"],
  why="360 counts all four even digits the same way (4 × 90); 480 allows 0 in the thousands place; 400 has no "
      "basis.", secs=70, by=BRUTE)

words = set(itertools.permutations("SAVINGS"))
n_ = sum(1 for w in words if "SS" not in "".join(w))
assert len(words) == 2520 and n_ == 1800
Q(T, "Word arrangements", A,
  "In how many ways can the letters of the word SAVINGS be arranged so that the two S's are not next to each other?",
  "1,800", ["2,520", "720", "2,160"],
  "Not together = total arrangements − arrangements with the S's together",
  "SAVINGS has 7 letters with S twice: total = 7! ÷ 2! = 2,520. Treating SS as one block gives 6 units, all different: "
  "6! = 720. So 2,520 − 720 = 1,800.",
  ["Total = 7!/2! = 2,520", "SS together: 6! = 720", "Not together = 1,800"],
  short="Gap method: arrange A, V, I, N, G in 5! = 120 ways, then put the two S's in 2 of the 6 gaps: C(6, 2) = 15. "
        "120 × 15 = 1,800.",
  why="2,520 ignores the condition; 720 counts the S's together; 2,160 subtracts only 360.", secs=80, by=BRUTE)

# ================================================================ Tabular DI (B1 I4 A5): two sets of 5
T = "Tabular DI"
SOL = {"Alwar": (420, 515, 480, 625), "Bikaner": (360, 440, 505, 575), "Churu": (280, 335, 390, 455),
       "Dausa": (510, 470, 560, 655), "Jhunjhunu": (330, 405, 445, 540)}
qs = ["Q1", "Q2", "Q3", "Q4"]
sid = stimulus("data_table", "Rooftop solar capacity installed in five districts, 2025-26",
               "The table shows the rooftop solar capacity (in kW) installed in five districts in each quarter of the "
               "financial year 2025-26.\n\n" + md_table(["District", *qs], [[k, *v] for k, v in SOL.items()]),
               {"columns": ["district", "q1_kw", "q2_kw", "q3_kw", "q4_kw"],
                "rows": [[k, *v] for k, v in SOL.items()]})
col = [sum(v[i] for v in SOL.values()) for i in range(4)]
tot = {k: sum(v) for k, v in SOL.items()}
assert col == [1900, 2165, 2380, 2850] and tot == {"Alwar": 2040, "Bikaner": 1880, "Churu": 1460, "Dausa": 2195,
                                                   "Jhunjhunu": 1720}
Q(T, "Single table", B, "What was the total rooftop solar capacity installed in Q3 by the five districts together?",
  "2,380 kW", ["2,165 kW", "2,420 kW", "2,350 kW"],
  "Column total",
  "Add the Q3 column: 480 + 505 + 390 + 560 + 445 = 2,380 kW.",
  ["480 + 505 = 985", "985 + 390 = 1,375", "1,375 + 560 = 1,935", "1,935 + 445 = 2,380"],
  why="2,165 kW is the Q2 total; the other two are addition slips.", secs=35, stim=sid)

pc = F(455 - 280, 280) * 100
assert pc == F(125, 2) and near(F(175, 455) * 100, 38.46, 0.01)
Q(T, "Single table", I, "Churu's installation in Q4 was what percentage more than its installation in Q1?",
  "62.5%", ["38.46%", "162.5%", "60%"],
  "Percentage more = increase ÷ earlier value × 100",
  "Churu installed 280 kW in Q1 and 455 kW in Q4. The increase of 175 kW is 175 ÷ 280 = 62.5% of the Q1 figure.",
  ["Increase = 455 − 280 = 175", "175 ÷ 280 × 100 = 62.5%"],
  why="38.46% divides by the Q4 figure; 162.5% is Q4 as a percentage of Q1; 60% is a rounding guess.", secs=40,
  stim=sid)

num, den = SOL["Alwar"][1] + SOL["Bikaner"][1], SOL["Churu"][2] + SOL["Jhunjhunu"][2]
assert (num, den) == (955, 835) and ratio(num, den) == "191 : 167"
Q(T, "Single table", I,
  "What is the ratio of the Q2 installations of Alwar and Bikaner together to the Q3 installations of Churu and "
  "Jhunjhunu together?",
  "191 : 167", ["167 : 191", "8 : 7", "19 : 17"],
  "Add the two cells on each side, then reduce",
  "Q2 of Alwar and Bikaner = 515 + 440 = 955. Q3 of Churu and Jhunjhunu = 390 + 445 = 835. 955 : 835 = 191 : 167 "
  "(dividing by 5).",
  ["515 + 440 = 955", "390 + 445 = 835", "955 : 835 = 191 : 167"],
  why="167 : 191 is reversed; 8 : 7 and 19 : 17 are close but not equal to 955 : 835.", secs=50, stim=sid)

over30 = [k for k, v in SOL.items() if F(v[3], sum(v)) > F(3, 10)]
assert over30 == ["Alwar", "Bikaner", "Churu", "Jhunjhunu"]
Q(T, "Single table", A,
  "In how many of the five districts was the Q4 installation more than 30% of that district's installation for the "
  "whole year?",
  "4", ["3", "5", "2"],
  "Compare each Q4 value with 30% of the row total",
  "Row totals and 30% of them: Alwar 2,040 → 612 (Q4 625, yes); Bikaner 1,880 → 564 (575, yes); Churu 1,460 → 438 "
  "(455, yes); Dausa 2,195 → 658.5 (655, no); Jhunjhunu 1,720 → 516 (540, yes). So 4 districts.",
  ["Alwar: 625 > 612 ✓", "Bikaner: 575 > 564 ✓", "Churu: 455 > 438 ✓", "Dausa: 655 < 658.5 ✗",
   "Jhunjhunu: 540 > 516 ✓", "Count = 4"],
  why="5 misses that Dausa falls just short (655 against 658.5); 3 and 2 drop districts that are only slightly above "
      "30%.", secs=100, stim=sid)

nxt = sum(F(6, 5) * v[3] for k, v in SOL.items() if k != "Dausa") + F(9, 10) * SOL["Dausa"][3]
assert nxt == F(6447, 2) and F(6, 5) * 2850 == 3420 and 3420 - F(655, 10) == F(6709, 2)
assert F(9, 10) * 2850 == 2565
Q(T, "Single table", A,
  "In Q1 of 2026-27, every district except Dausa installs 20% more than it did in Q4 of 2025-26, while Dausa "
  "installs 10% less than its Q4 figure. What is the total installation of the five districts in Q1 of 2026-27?",
  "3,223.5 kW", ["3,420 kW", "3,354.5 kW", "2,565 kW"],
  "Apply each district's own change to its Q4 value",
  "The four districts other than Dausa installed 2,850 − 655 = 2,195 kW in Q4; 20% more is 2,634 kW. Dausa's "
  "655 kW falls 10% to 589.5 kW. Total = 2,634 + 589.5 = 3,223.5 kW.",
  ["Q4 total = 2,850; Dausa Q4 = 655", "Others: 2,195 × 1.2 = 2,634", "Dausa: 655 × 0.9 = 589.5",
   "Total = 3,223.5 kW"],
  why="3,420 kW applies +20% to Dausa too; 3,354.5 kW subtracts only 10% of Dausa from 3,420; 2,565 kW applies −10% "
      "to every district.", secs=100, stim=sid)

HUB = {"Hub A": (12000, 65, 80), "Hub B": (9600, 75, 70), "Hub C": (15000, 58, 85), "Hub D": (8400, 80, 75),
       "Hub E": (10800, 70, 60)}
sid = stimulus("data_table", "Parcels handled by five courier hubs in a week",
               "The table shows the number of parcels received by five hubs of a courier company in one week, the "
               "percentage of those parcels delivered on the same day, and the percentage of the remaining parcels "
               "that were delivered on the next day. Parcels not delivered by the next day are 'delayed'.\n\n" +
               md_table(["Hub", "Parcels received", "Delivered same day (%)",
                         "Of the rest, delivered next day (%)"],
                        [[k, ind(r), s_, n_] for k, (r, s_, n_) in HUB.items()]),
               {"columns": ["hub", "received", "same_day_pct", "next_day_pct_of_rest"],
                "rows": [[k, *v] for k, v in HUB.items()]})
same = {k: r * F(s_, 100) for k, (r, s_, n_) in HUB.items()}
rest = {k: r - same[k] for k, (r, s_, n_) in HUB.items()}
nextd = {k: rest[k] * F(HUB[k][2], 100) for k in HUB}
late = {k: rest[k] - nextd[k] for k in HUB}
assert same == {"Hub A": 7800, "Hub B": 7200, "Hub C": 8700, "Hub D": 6720, "Hub E": 7560}
assert nextd == {"Hub A": 3360, "Hub B": 1680, "Hub C": 5355, "Hub D": 1260, "Hub E": 1944}
assert late == {"Hub A": 840, "Hub B": 720, "Hub C": 945, "Hub D": 420, "Hub E": 1296}
Q(T, "Table with percentages", I, "How many parcels did Hub C deliver on the next day?",
  "5,355", ["6,300", "7,395", "945"],
  "Next-day deliveries are a percentage of the parcels left after the same day, not of all parcels",
  "Hub C delivered 58% of 15,000 = 8,700 on the same day, leaving 6,300. 85% of 6,300 = 5,355 were delivered the "
  "next day.",
  ["Same day = 15,000 × 0.58 = 8,700", "Remaining = 6,300", "Next day = 6,300 × 0.85 = 5,355"],
  why="6,300 is the number left after the same day; 7,395 takes 85% of 8,700; 945 is the number delayed.", secs=50,
  stim=sid)

best = max(same, key=same.get)
assert best == "Hub C" and max(HUB, key=lambda k: HUB[k][1]) == "Hub D"
Q(T, "Table with percentages", I, "Which hub delivered the largest number of parcels on the same day?",
  "Hub C", ["Hub A", "Hub E", "Hub D"],
  "Compare numbers, not percentages: same-day count = parcels × same-day %",
  "Same-day deliveries: A 7,800, B 7,200, C 8,700, D 6,720 and E 7,560. Hub C is the largest even though its "
  "percentage (58%) is the lowest.",
  ["A: 12,000 × 65% = 7,800", "B: 9,600 × 75% = 7,200", "C: 15,000 × 58% = 8,700", "D: 8,400 × 80% = 6,720",
   "E: 10,800 × 70% = 7,560"],
  why="Hub D has the highest percentage but the fewest same-day parcels; Hub A and Hub E come second and third.",
  secs=55, stim=sid)

pct = F(same["Hub D"] + nextd["Hub D"], HUB["Hub D"][0]) * 100
assert pct == 95
Q(T, "Table with percentages", A,
  "What percentage of the parcels received at Hub D were delivered within two days (on the same day or the next "
  "day)?",
  "95%", ["77.5%", "60%", "85%"],
  "Delivered within two days = same day + next day; the next-day percentage applies to the remainder only",
  "Same day: 80% of 8,400 = 6,720. Remainder 1,680, of which 75% = 1,260 were delivered the next day. Within two "
  "days: 7,980 of 8,400 = 95%.",
  ["Same day = 6,720 (80%)", "Next day = 75% of 20% = 15% of all = 1,260", "Total = 95%"],
  short="80% + 75% × 20% = 80% + 15% = 95%.",
  why="77.5% averages 80 and 75; 60% multiplies them; 85% adds only 5 points for the next day.", secs=60, stim=sid)

pc = F(late["Hub E"], late["Hub B"]) * 100
assert pc == 180 and near(F(late["Hub B"], late["Hub E"]) * 100, 55.56, 0.01) and F(3240, 2400) * 100 == 135
Q(T, "Table with percentages", A,
  "The number of delayed parcels at Hub E is what percentage of the number of delayed parcels at Hub B?",
  "180%", ["80%", "55.56%", "135%"],
  "Delayed = received × (1 − same-day %) × (1 − next-day %)",
  "Hub E: 10,800 × 0.30 × 0.40 = 1,296 delayed. Hub B: 9,600 × 0.25 × 0.30 = 720 delayed. 1,296 ÷ 720 = 180%.",
  ["E: 10,800 × 30% = 3,240 left; 40% of 3,240 = 1,296 delayed", "B: 9,600 × 25% = 2,400 left; 30% of 2,400 = 720",
   "1,296 ÷ 720 × 100 = 180%"],
  why="80% is how much more E has, not the percentage; 55.56% is B as a percentage of E; 135% compares the parcels "
      "left after the same day (3,240 and 2,400).", secs=80, stim=sid)

alt_same = 15000 * F(70, 100)
alt_next = (15000 - alt_same) * F(85, 100)
gain = alt_same + alt_next - (same["Hub C"] + nextd["Hub C"])
assert (alt_same, alt_next, gain) == (10500, 3825, 270)
Q(T, "Table with percentages", A,
  "If Hub C had delivered 70% of its parcels on the same day, and the same next-day percentage had applied to the "
  "rest, how many more parcels would it have delivered within two days?",
  "270", ["1,800", "1,530", "945"],
  "A higher same-day share leaves fewer parcels for the next day; compute both stages again",
  "New same-day = 10,500 and new remainder 4,500, of which 85% = 3,825 go the next day. Within two days: 14,325 "
  "instead of 8,700 + 5,355 = 14,055. Increase = 270.",
  ["New same day = 15,000 × 0.7 = 10,500", "New next day = 4,500 × 0.85 = 3,825", "New total = 14,325",
   "Old total = 14,055", "Increase = 270"],
  short="Only the extra 12% (1,800 parcels) changes stage, and 85% of them would have gone the next day anyway: "
        "1,800 × 15% = 270.",
  why="1,800 ignores the fall in next-day deliveries; 1,530 is that fall itself; 945 is the old number delayed.",
  secs=90, stim=sid)

# ================================================================ Bar Graph DI (B2 I5 A1): two sets of 4
T = "Bar Graph DI"
SAP = {"Ashoka": 480, "Bharati": 360, "Chanakya": 540, "Disha": 300, "Eklavya": 600, "Gyanodaya": 420}
sid = stimulus("chart", "Saplings planted by six schools in a green drive",
               "The bar chart shows the number of saplings planted by six schools of a town during a one-week green "
               "drive (values read from the bars).\n\n" + md_table(["School", "Saplings planted"],
                                                                     [[k, v] for k, v in SAP.items()]),
               {"chart_type": "bar", "x": list(SAP), "series": [{"name": "Saplings", "values": list(SAP.values())}]})
assert sum(SAP.values()) == 2700
Q(T, "Simple bar", B, "How many saplings did Bharati and Disha plant together?",
  "660", ["720", "600", "780"],
  "Read the two bars and add",
  "Bharati planted 360 and Disha 300, so together 660.",
  ["Bharati = 360", "Disha = 300", "Total = 660"],
  why="720 doubles Bharati; 600 doubles Disha; 780 uses Gyanodaya (420) instead of Disha.", secs=25, stim=sid)

pc = F(600 - 480, 480) * 100
assert pc == 25 and F(120, 600) * 100 == 20
Q(T, "Simple bar", B, "Eklavya planted what percentage more saplings than Ashoka?",
  "25%", ["20%", "125%", "30%"],
  "Percentage more = difference ÷ the value after 'than' × 100",
  "Eklavya 600, Ashoka 480. The difference 120 is 120 ÷ 480 = 25% of Ashoka's figure.",
  ["Difference = 600 − 480 = 120", "120 ÷ 480 × 100 = 25%"],
  why="20% divides by Eklavya's 600; 125% is Eklavya as a percentage of Ashoka.", secs=35, stim=sid)

assert ratio(540 + 420, 360 + 300) == "16 : 11"
Q(T, "Simple bar", I,
  "What is the ratio of the saplings planted by Chanakya and Gyanodaya together to those planted by Bharati and "
  "Disha together?",
  "16 : 11", ["11 : 16", "8 : 5", "32 : 21"],
  "Sum each pair, then reduce",
  "Chanakya + Gyanodaya = 540 + 420 = 960. Bharati + Disha = 360 + 300 = 660. 960 : 660 = 16 : 11.",
  ["960", "660", "960 : 660 = 16 : 11 (÷ 60)"],
  why="11 : 16 is reversed; 8 : 5 and 32 : 21 come from misreading one bar by 60.", secs=45, stim=sid)

surv = 480 * F(90, 100) + 600 * F(85, 100) + 540 * F(80, 100)
assert surv == 1374 and (480 + 600 + 540) * F(85, 100) == 1377 and (480 + 600 + 540) * F(80, 100) == 1296
Q(T, "Simple bar", I,
  "90% of Ashoka's saplings, 85% of Eklavya's and 80% of Chanakya's survived. How many saplings of these three "
  "schools survived in all?",
  "1,374", ["1,377", "1,620", "1,296"],
  "Apply each school's own survival rate to its own bar",
  "Ashoka: 480 × 0.9 = 432. Eklavya: 600 × 0.85 = 510. Chanakya: 540 × 0.8 = 432. Total = 1,374.",
  ["432 + 510 + 432 = 1,374"],
  why="1,377 applies the average rate 85% to the combined 1,620; 1,620 counts every sapling; 1,296 uses 80% for "
      "all.", secs=55, stim=sid)

ORD = {"Spice Hub": (640, 410), "Tandoor Tales": (480, 520), "Curry Leaf": (720, 330), "Biryani Bay": (585, 315),
       "Dosa Point": (375, 625)}
sid = stimulus("chart", "Online and walk-in orders at five restaurant outlets in a week",
               "The grouped bar chart shows the number of online orders and walk-in orders received by five outlets "
               "of a restaurant chain in one week (values read from the bars).\n\n" +
               md_table(["Outlet", "Online orders", "Walk-in orders"], [[k, *v] for k, v in ORD.items()]),
               {"chart_type": "grouped_bar", "x": list(ORD),
                "series": [{"name": "Online", "values": [v[0] for v in ORD.values()]},
                           {"name": "Walk-in", "values": [v[1] for v in ORD.values()]}]})
on, walk = sum(v[0] for v in ORD.values()), sum(v[1] for v in ORD.values())
assert (on, walk) == (2800, 2200) and F(on, on + walk) * 100 == 56
Q(T, "Stacked or grouped bar", I, "What percentage of all the orders received by the five outlets were online?",
  "56%", ["44%", "50%", "58%"],
  "Share = online total ÷ (online + walk-in) total",
  "Online = 640 + 480 + 720 + 585 + 375 = 2,800. Walk-in = 2,200. Share = 2,800 ÷ 5,000 = 56%.",
  ["Online total = 2,800", "All orders = 5,000", "2,800 ÷ 5,000 = 56%"],
  why="44% is the walk-in share; 50% and 58% are slips in one of the totals.", secs=55, stim=sid)

share = {k: F(a, a + b) for k, (a, b) in ORD.items()}
assert max(share, key=share.get) == "Curry Leaf" and max(ORD, key=lambda k: ORD[k][0]) == "Curry Leaf"
assert sorted(share.values(), reverse=True)[1] == share["Biryani Bay"] == F(13, 20)
Q(T, "Stacked or grouped bar", I, "At which outlet did online orders form the largest share of the outlet's own "
  "orders?",
  "Curry Leaf", ["Biryani Bay", "Spice Hub", "Tandoor Tales"],
  "Compare online ÷ total for each outlet",
  "Online shares: Spice Hub 640/1,050 ≈ 61.0%, Tandoor Tales 48%, Curry Leaf 720/1,050 ≈ 68.6%, Biryani Bay "
  "585/900 = 65% and Dosa Point 37.5%. Curry Leaf is highest.",
  ["Spice Hub ≈ 61.0%", "Tandoor Tales = 48%", "Curry Leaf ≈ 68.6%", "Biryani Bay = 65%", "Dosa Point = 37.5%"],
  why="Biryani Bay is second (65%); Spice Hub has many online orders but also many walk-ins.", secs=60, stim=sid)

pc = F(720 - 375, 375) * 100
assert pc == 92 and near(F(345, 720) * 100, 47.92, 0.01)
Q(T, "Stacked or grouped bar", I,
  "Online orders at Curry Leaf were what percentage more than online orders at Dosa Point?",
  "92%", ["47.92%", "192%", "82%"],
  "Percentage more = difference ÷ smaller (base) value × 100",
  "Curry Leaf 720, Dosa Point 375. Difference 345, and 345 ÷ 375 = 92%.",
  ["720 − 375 = 345", "345 ÷ 375 × 100 = 92%"],
  why="47.92% divides by 720; 192% is Curry Leaf as a percentage of Dosa Point.", secs=45, stim=sid)

net = 480 * 350 * F(80, 100) + 520 * 420
assert net == 352800 and 480 * 350 + 520 * 420 == 386400 and (480 * 350 + 520 * 420) * F(80, 100) == 309120
Q(T, "Stacked or grouped bar", A,
  "Online orders average ₹350 each and walk-in orders ₹420 each. The delivery platform keeps a 20% commission on the "
  "value of online orders. What was Tandoor Tales' net revenue for the week?",
  "₹3,52,800", ["₹3,86,400", "₹3,09,120", "₹3,43,280"],
  "Commission applies to online value only",
  "Online value = 480 × 350 = 1,68,000; after 20% commission the outlet keeps 1,34,400. Walk-in value = 520 × 420 = "
  "2,18,400. Net revenue = 1,34,400 + 2,18,400 = ₹3,52,800.",
  ["Online: 480 × 350 = 1,68,000 → × 0.8 = 1,34,400", "Walk-in: 520 × 420 = 2,18,400", "Net = 3,52,800"],
  why="₹3,86,400 ignores the commission; ₹3,09,120 deducts it from walk-in sales too; ₹3,40,800 swaps the two "
      "average values.", secs=80, stim=sid)
assert 480 * 420 * F(80, 100) + 520 * 350 == 343280

# ================================================================ Pie Chart DI (B4 I3 A2): sets of 5 and 4
T = "Pie Chart DI"
BUD = {"Roads": 90, "Water supply": 72, "Sanitation": 54, "Health": 45, "Education": 36, "Street lighting": 27,
       "Others": 36}
assert sum(BUD.values()) == 360
sid = stimulus("chart", "A city's municipal budget by head (central angles)",
               "The pie chart shows how a city's municipal budget of ₹720 crore for 2026-27 is divided among seven "
               "heads. The central angle of each sector is given.\n\n" +
               md_table(["Head", "Central angle (degrees)"], [[k, v] for k, v in BUD.items()]),
               {"chart_type": "pie", "unit": "degrees", "total_rs_crore": 720,
                "labels": list(BUD), "values": list(BUD.values())})
per_deg = F(720, 360)
assert per_deg == 2 and BUD["Water supply"] * per_deg == 144
Q(T, "Degree-based", B, "How much of the budget is allocated to water supply?",
  "₹144 crore", ["₹72 crore", "₹180 crore", "₹120 crore"],
  "Amount = angle ÷ 360 × total",
  "Each degree stands for 720 ÷ 360 = ₹2 crore. Water supply has 72°, so it gets 72 × 2 = ₹144 crore.",
  ["1° = 720 ÷ 360 = ₹2 crore", "72 × 2 = ₹144 crore"],
  why="₹72 crore reads the angle as crore; ₹180 crore uses Roads (90°); ₹120 crore uses 60°.", secs=30, stim=sid)

assert F(45, 360) * 100 == F(25, 2)
Q(T, "Degree-based", B, "What percentage of the budget goes to health?",
  "12.5%", ["45%", "15%", "10%"],
  "Percentage = angle ÷ 360 × 100",
  "Health has 45°, which is 45 ÷ 360 = 1/8 = 12.5% of the budget.",
  ["45 ÷ 360 = 0.125", "= 12.5%"],
  why="45% reads the angle as a percentage; 15% and 10% use 54° or 36°.", secs=30, stim=sid)

d_ = (BUD["Roads"] - BUD["Sanitation"] - BUD["Street lighting"]) * per_deg
assert d_ == 18
Q(T, "Degree-based", I,
  "By how much does the allocation for roads exceed the combined allocation for sanitation and street lighting?",
  "₹18 crore", ["₹9 crore", "₹36 crore", "₹27 crore"],
  "Subtract angles first, then convert",
  "Roads 90° against Sanitation + Street lighting = 54° + 27° = 81°. The gap is 9°, worth 9 × 2 = ₹18 crore.",
  ["54 + 27 = 81°", "90 − 81 = 9°", "9 × ₹2 crore = ₹18 crore"],
  why="₹9 crore leaves the gap in degrees; ₹36 crore and ₹27 crore use 18° or 13.5°.", secs=40, stim=sid)

edu = BUD["Education"] * per_deg
others_new = BUD["Others"] * per_deg - edu * F(25, 100)
assert edu == 72 and others_new == 54 and others_new / per_deg == 27
Q(T, "Degree-based", I,
  "The education allocation is raised by 25%, and the extra money is taken entirely from 'Others', keeping the total "
  "budget the same. What will be the central angle of 'Others'?",
  "27°", ["45°", "18°", "36°"],
  "Work in rupees (or directly in degrees): 25% of Education's 36° is 9°",
  "Education gets 36° = ₹72 crore; 25% more is ₹18 crore = 9°. 'Others' falls from 36° to 36° − 9° = 27°.",
  ["Education = 36° = ₹72 crore", "Increase = 25% of 72 = ₹18 crore = 9°", "Others = 36° − 9° = 27°"],
  why="45° adds the 9° instead of subtracting; 18° takes off 18 degrees (reading crore as degrees); 36° leaves "
      "'Others' unchanged.", secs=55, stim=sid)

old_h = BUD["Health"] * per_deg
new_h = 720 * F(115, 100) * F(15, 100)
pc = F(new_h - old_h, old_h) * 100
assert (old_h, new_h, pc) == (90, F(621, 5), 38) and F(115, 100) * F(115, 100) == F(529, 400)
Q(T, "Degree-based", A,
  "Next year the total budget rises by 15% and health's share of the budget rises to 15%. By what percentage does "
  "the health allocation increase?",
  "38%", ["20%", "15%", "32.25%"],
  "New amount = new total × new share; compare with the old amount",
  "This year health gets ₹90 crore (12.5% of 720). Next year the budget is 720 × 1.15 = ₹828 crore and health gets "
  "15% of it = ₹124.2 crore. Increase = 34.2 ÷ 90 = 38%.",
  ["Old = 45 × 2 = ₹90 crore", "New total = ₹828 crore", "New health = 0.15 × 828 = ₹124.2 crore",
   "34.2 ÷ 90 × 100 = 38%"],
  short="Growth factor = 1.15 (budget) × 15/12.5 (share) = 1.15 × 1.2 = 1.38.",
  why="20% counts only the change in share; 15% only the budget growth; 32.25% treats the share as rising by 15% "
      "of itself.", secs=80, stim=sid)

ALLP = [15, 18, 22, 25, 20]
FEMP = [F(25, 2), 20, 25, F(45, 2), 20]
assert sum(ALLP) == 100 and sum(FEMP) == 100
days = [f"Day {i}" for i in range(1, 6)]
sid = stimulus("chart", "Visitors to a five-day trade fair: all visitors and women visitors",
               "Two pie charts describe the visitors to a five-day trade fair. Chart 1 shows how the 60,000 visitors "
               "were spread over the five days. Chart 2 shows how the 24,000 women visitors (included in the 60,000) "
               "were spread over the same days.\n\n" +
               md_table(["Day", "All visitors (% of 60,000)", "Women visitors (% of 24,000)"],
                        [[d, a, N(f)] for d, a, f in zip(days, ALLP, FEMP)]),
               {"chart_type": "two_pies", "labels": days,
                "all_visitors": {"total": 60000, "percent": ALLP},
                "women_visitors": {"total": 24000, "percent": [float(x) for x in FEMP]}})
allv = [60000 * F(p, 100) for p in ALLP]
women = [24000 * F(p, 100) for p in FEMP]
men = [a - w for a, w in zip(allv, women)]
assert allv == [9000, 10800, 13200, 15000, 12000] and women == [3000, 4800, 6000, 5400, 4800]
assert men == [6000, 6000, 7200, 9600, 7200]
Q(T, "Two pie charts", B, "How many women visited the fair on Day 3?",
  "6,000", ["13,200", "5,400", "7,200"],
  "Use the women's chart and the women's total",
  "Day 3 has 25% of the 24,000 women visitors: 24,000 × 0.25 = 6,000.",
  ["24,000 × 25% = 6,000"],
  why="13,200 is all visitors on Day 3; 5,400 is women on Day 4; 7,200 is men on Day 3.", secs=30, stim=sid)

Q(T, "Two pie charts", B, "How many men visited the fair on Day 4?",
  "9,600", ["5,400", "15,000", "9,000"],
  "Men on a day = all visitors that day − women that day",
  "All visitors on Day 4 = 25% of 60,000 = 15,000. Women on Day 4 = 22.5% of 24,000 = 5,400. Men = 15,000 − 5,400 "
  "= 9,600.",
  ["All on Day 4 = 15,000", "Women on Day 4 = 5,400", "Men = 9,600"],
  why="5,400 is the women; 15,000 is everyone; 9,000 takes 25% of the 36,000 men, which the charts do not give.",
  secs=40, stim=sid)

wshare = [F(w, a) for w, a in zip(women, allv)]
assert wshare.index(max(wshare)) == 2 and sorted(wshare)[-2] == wshare[1]
Q(T, "Two pie charts", I,
  "On which day did women form the largest share of that day's visitors?",
  "Day 3", ["Day 2", "Day 5", "Day 4"],
  "For each day, divide women by all visitors",
  "Women's shares: Day 1 3,000/9,000 = 33.3%, Day 2 4,800/10,800 = 44.4%, Day 3 6,000/13,200 = 45.5%, Day 4 "
  "5,400/15,000 = 36% and Day 5 4,800/12,000 = 40%. Day 3 is highest.",
  ["Day 1 ≈ 33.3%", "Day 2 ≈ 44.4%", "Day 3 ≈ 45.5%", "Day 4 = 36%", "Day 5 = 40%"],
  why="Day 2 is a close second; Day 4 has the most visitors but a low women's share.", secs=60, stim=sid)

rev = men[3] * 120 + women[3] * 90
assert rev == 1638000 and allv[3] * 120 == 1800000 and allv[3] * 90 == 1350000
assert men[3] * 90 + women[3] * 120 == 1512000
Q(T, "Two pie charts", A,
  "The entry ticket costs ₹120, and women get a 25% discount on it. What was the ticket revenue on Day 4?",
  "₹16,38,000", ["₹18,00,000", "₹13,50,000", "₹15,12,000"],
  "Split Day 4's visitors into men and women and price each group",
  "Day 4: 9,600 men pay ₹120 each = ₹11,52,000; 5,400 women pay ₹90 each = ₹4,86,000. Total = ₹16,38,000.",
  ["Men = 9,600 × 120 = 11,52,000", "Women = 5,400 × 90 = 4,86,000", "Total = 16,38,000"],
  why="₹18,00,000 ignores the discount; ₹13,50,000 gives everyone the discount; ₹15,12,000 gives the discount to the "
      "men instead.", secs=80, stim=sid)

# ================================================================ Line Graph DI (B2 I2 A2): two sets of 3
T = "Line Graph DI"
WIND = {"Jan": 40, "Feb": 46, "Mar": 52, "Apr": 65, "May": 78, "Jun": 79}
sid = stimulus("chart", "Electricity generated by a wind farm, January to June 2026",
               "The line graph shows the electricity generated by a wind farm in each month from January to June 2026, "
               "in million units (MU).\n\n" + md_table(["Month", "Generation (MU)"], [[k, v] for k, v in WIND.items()]),
               {"chart_type": "line", "x": list(WIND), "series": [{"name": "Generation (MU)",
                                                                    "values": list(WIND.values())}]})
pc = F(65 - 52, 52) * 100
assert pc == 25 and near(F(13, 65) * 100, 20)
Q(T, "Single line", B, "By what percentage did generation rise from March to April?",
  "25%", ["20%", "13%", "30%"],
  "Percentage change = change ÷ earlier value × 100",
  "March 52 MU, April 65 MU. The rise of 13 MU is 13 ÷ 52 = 25% of March's figure.",
  ["Rise = 65 − 52 = 13", "13 ÷ 52 × 100 = 25%"],
  why="20% divides by April's 65; 13% is the rise in MU, not a percentage.", secs=35, stim=sid)

q1_, q2_ = sum(list(WIND.values())[:3]), sum(list(WIND.values())[3:])
assert (q1_, q2_) == (138, 222) and ratio(q1_, q2_) == "23 : 37"
Q(T, "Single line", I,
  "What is the ratio of the total generation in January–March to the total generation in April–June?",
  "23 : 37", ["37 : 23", "2 : 3", "46 : 79"],
  "Add each quarter's three months, then reduce",
  "January–March = 40 + 46 + 52 = 138 MU. April–June = 65 + 78 + 79 = 222 MU. 138 : 222 = 23 : 37 (dividing by 6).",
  ["138", "222", "138 : 222 = 23 : 37"],
  why="37 : 23 is reversed; 2 : 3 is close but not exact; 46 : 79 compares February with June.", secs=45, stim=sid)

rev = 50 * F(32, 10) + (78 - 50) * F(28, 10)
assert rev == F(2384, 10) and 78 * F(32, 10) == F(2496, 10) and 78 * F(28, 10) == F(2184, 10)
Q(T, "Single line", A,
  "The farm sells the first 50 MU it generates in a month at ₹3.20 per unit and any further units that month at "
  "₹2.80 per unit. What was its revenue for May? (1 MU = 10 lakh units.)",
  "₹23.84 crore", ["₹24.96 crore", "₹21.84 crore", "₹23.40 crore"],
  "Slab pricing: price each slab separately",
  "May generation = 78 MU. First 50 MU × ₹3.20 = ₹160 million; the other 28 MU × ₹2.80 = ₹78.4 million. Total = "
  "₹238.4 million = ₹23.84 crore.",
  ["50 MU = 5 crore units × ₹3.20 = ₹16 crore", "28 MU = 2.8 crore units × ₹2.80 = ₹7.84 crore",
   "Total = ₹23.84 crore"],
  why="₹24.96 crore prices all 78 MU at ₹3.20; ₹21.84 crore prices all at ₹2.80; ₹23.40 crore uses a flat ₹3.00.",
  secs=80, stim=sid)

DOM = {2021: 32, 2022: 45, 2023: 54, 2024: 60, 2025: 63}
INT = {2021: 8, 2022: 12, 2023: 15, 2024: 18, 2025: 21}
sid = stimulus("chart", "Domestic and international flights handled by an airport, 2021-2025",
               "The line graph shows the number of domestic and international flights (in thousands) handled by an "
               "airport in each year from 2021 to 2025.\n\n" +
               md_table(["Year", "Domestic (thousand)", "International (thousand)"],
                        [[y, DOM[y], INT[y]] for y in DOM]),
               {"chart_type": "line", "x": list(DOM), "series": [{"name": "Domestic", "values": list(DOM.values())},
                                                                  {"name": "International",
                                                                   "values": list(INT.values())}]})
assert DOM[2023] + INT[2023] == 69
Q(T, "Multiple lines", B, "How many flights in all did the airport handle in 2023?",
  "69,000", ["54,000", "75,000", "66,000"],
  "Add the two lines' values for the year; the unit is thousands",
  "2023: domestic 54 thousand + international 15 thousand = 69 thousand = 69,000 flights.",
  ["54 + 15 = 69 thousand"],
  why="54,000 counts only domestic flights; 75,000 uses 2024's domestic figure (60 + 15); 66,000 "
      "is 2023's domestic plus 2022's international (54 + 12).", secs=30, stim=sid)

sh = F(INT[2025], DOM[2025] + INT[2025]) * 100
assert sh == 25 and near(F(21, 63) * 100, 33.33, 0.01)
Q(T, "Multiple lines", I, "What percentage of all flights handled in 2025 were international?",
  "25%", ["33.33%", "20%", "21%"],
  "Share = part ÷ (domestic + international) × 100",
  "2025: international 21 thousand out of 63 + 21 = 84 thousand, which is 25%.",
  ["Total 2025 = 84 thousand", "21 ÷ 84 × 100 = 25%"],
  why="33.33% divides by domestic flights only; 21% reads the value as a percentage.", secs=40, stim=sid)

d26, i26 = DOM[2025] * F(110, 100), INT[2025] * F(120, 100)
sh = F(i26, d26 + i26) * 100
assert (d26, i26) == (F(693, 10), F(252, 10)) and sh == F(80, 3)
Q(T, "Multiple lines", A,
  "In 2026 domestic flights grow by 10% and international flights by 20% over 2025. What percentage of all 2026 "
  "flights will be international?",
  "26⅔%", ["28%", "30%", "25.2%"],
  "Project both lines, then take the share",
  "2026: domestic 63 × 1.1 = 69.3 thousand, international 21 × 1.2 = 25.2 thousand. Share = 25.2 ÷ 94.5 = 26⅔%.",
  ["Domestic 2026 = 69.3", "International 2026 = 25.2", "Total = 94.5", "25.2 ÷ 94.5 = 4/15 = 26⅔%"],
  why="28% and 30% add percentage points to the 2025 share; 25.2% divides by 100 instead of 94.5.", secs=80,
  stim=sid)

# ================================================================ Caselet DI (B2 I5 A3): two sets of 5
T = "Caselet DI"
sid = stimulus("caselet", "Output and sales of a handloom cooperative, October 2026",
               "In October 2026 a handloom cooperative produced 1,200 items in all: sarees, dupattas and stoles. "
               "Sarees made up 40% of the items, and the number of dupattas was 50% more than the number of stoles. "
               "During the month the cooperative sold 85% of its sarees, three-fourths of its dupattas and "
               "seven-eighths of its stoles. A saree sells for ₹2,400, a dupatta for ₹600 and a stole for ₹450. It "
               "costs ₹1,800 to produce a saree, ₹380 to produce a dupatta and ₹300 to produce a stole.")
sar = 1200 * F(40, 100)
sto = (1200 - sar) / F(5, 2)
dup = sto * F(3, 2)
sold = {"saree": sar * F(85, 100), "dupatta": dup * F(3, 4), "stole": sto * F(7, 8)}
assert (sar, dup, sto) == (480, 432, 288) and sold == {"saree": 408, "dupatta": 324, "stole": 252}
Q(T, "Paragraph data", B, "How many dupattas did the cooperative produce?",
  "432", ["288", "360", "480"],
  "Split the non-saree items in the ratio dupattas : stoles = 1.5 : 1 = 3 : 2",
  "Sarees = 40% of 1,200 = 480, so dupattas + stoles = 720. Dupattas : stoles = 3 : 2, so dupattas = 3/5 × 720 = "
  "432.",
  ["Sarees = 480", "Dupattas + stoles = 720", "Dupattas = 720 × 3/5 = 432"],
  why="288 is the stoles; 360 splits 720 equally; 480 is the sarees.", secs=40, stim=sid)

rv = sold["saree"] * 2400
assert rv == 979200 and sar * 2400 == 1152000 and sold["saree"] * 1800 == 734400
Q(T, "Paragraph data", I, "What was the cooperative's revenue from the sarees sold in October?",
  "₹9,79,200", ["₹11,52,000", "₹7,34,400", "₹9,60,000"],
  "Revenue = units sold × selling price",
  "Sarees sold = 85% of 480 = 408. Revenue = 408 × 2,400 = ₹9,79,200.",
  ["408 sarees sold", "408 × 2,400 = 9,79,200"],
  why="₹11,52,000 counts all 480 sarees; ₹7,34,400 uses the production cost; ₹9,60,000 uses 400 sarees.", secs=50,
  stim=sid)

unsold = (sar - sold["saree"]) + (dup - sold["dupatta"]) + (sto - sold["stole"])
assert unsold == 216
Q(T, "Paragraph data", I, "How many items in all remained unsold at the end of October?",
  "216", ["180", "252", "144"],
  "Unsold = produced − sold, for each item",
  "Unsold sarees = 72, dupattas = 108, stoles = 36. Total = 216.",
  ["Sarees: 480 − 408 = 72", "Dupattas: 432 − 324 = 108", "Stoles: 288 − 252 = 36", "Total = 216"],
  why="180 leaves out the stoles; 252 is the number of stoles sold; 144 halves the dupattas.", secs=55, stim=sid)

pct = F(sum(sold.values()), 1200) * 100
assert pct == 82 and F(85 + 75 + F(175, 2), 3) == F(165, 2)
Q(T, "Paragraph data", I, "What percentage of all the items produced were sold?",
  "82%", ["82.5%", "18%", "80%"],
  "Use actual numbers sold; the three percentages apply to different bases",
  "Items sold = 408 + 324 + 252 = 984, out of 1,200, which is 82%.",
  ["Sold = 984", "984 ÷ 1,200 × 100 = 82%"],
  why="82.5% averages 85%, 75% and 87.5% without weighting; 18% is the unsold share.", secs=55, stim=sid)

pf = sold["dupatta"] * 600 - dup * 380
assert pf == 30240 and sold["dupatta"] * (600 - 380) == 71280 and dup * (600 - 380) == 95040
Q(T, "Paragraph data", A,
  "Taking profit as the revenue from items sold minus the production cost of all items produced, what was the "
  "cooperative's profit on dupattas in October?",
  "₹30,240", ["₹71,280", "₹95,040", "₹23,040"],
  "The cost of unsold items still counts against the revenue",
  "Revenue = 324 × 600 = ₹1,94,400. Cost of all 432 dupattas = 432 × 380 = ₹1,64,160. Profit = ₹30,240.",
  ["Revenue = 324 × 600 = 1,94,400", "Cost = 432 × 380 = 1,64,160", "Profit = 30,240"],
  why="₹71,280 counts the cost of only the dupattas sold; ₹95,040 assumes all were sold; ₹23,040 is a slip in the "
      "cost.", secs=80, stim=sid)

RACE = {"5 km": (2400, 600, 95, 40), "10 km": (1800, 900, 90, 35), "Half marathon": (1200, 1500, 85, 30),
        "Full marathon": (600, 2500, 70, 25)}
sid = stimulus("caselet", "Registrations, fees and finishers at a city marathon",
               "A city marathon had four race categories. The table gives the number of runners registered in each "
               "category, the entry fee and the percentage of registered runners who finished.\n\n" +
               md_table(["Category", "Registrations", "Entry fee (₹)", "Finished (%)"],
                        [[k, ind(r), ind(f_), p_] for k, (r, f_, p_, w_) in RACE.items()]) +
               "\n\nWomen made up 40% of the 5 km registrations, 35% of the 10 km, 30% of the half marathon and 25% of "
               "the full marathon. Every finisher received a medal that cost the organisers ₹250.",
               {"columns": ["category", "registrations", "fee_rs", "finished_pct", "women_pct"],
                "rows": [[k, *v] for k, v in RACE.items()]})
fin = {k: r * F(p_, 100) for k, (r, f_, p_, w_) in RACE.items()}
assert fin == {"5 km": 2280, "10 km": 1620, "Half marathon": 1020, "Full marathon": 420}
Q(T, "Caselet with table", B, "How many runners finished the 10 km race?",
  "1,620", ["1,800", "180", "1,710"],
  "Finishers = registrations × finishing percentage",
  "90% of 1,800 = 1,620.",
  ["1,800 × 0.9 = 1,620"],
  why="1,800 is all registrations; 180 is the non-finishers; 1,710 uses 95%.", secs=30, stim=sid)

fees = sum(r * f_ for r, f_, p_, w_ in RACE.values())
assert fees == 6360000 and 6000 * F(600 + 900 + 1500 + 2500, 4) == 8250000
assert sum(fin[k] * RACE[k][1] for k in RACE) == 5406000
Q(T, "Caselet with table", I, "What was the total entry-fee collection from all registered runners?",
  "₹63,60,000", ["₹82,50,000", "₹54,06,000", "₹60,60,000"],
  "Fee income = Σ registrations × fee",
  "5 km: 2,400 × 600 = 14,40,000. 10 km: 1,800 × 900 = 16,20,000. Half: 1,200 × 1,500 = 18,00,000. Full: 600 × 2,500 "
  "= 15,00,000. Total = ₹63,60,000.",
  ["14,40,000 + 16,20,000 = 30,60,000", "+ 18,00,000 = 48,60,000", "+ 15,00,000 = 63,60,000"],
  why="₹82,50,000 multiplies 6,000 runners by the plain average fee; ₹54,06,000 counts finishers only; ₹60,60,000 "
      "is an addition slip.", secs=55, stim=sid)

wpct = F(sum(r * F(w_, 100) for r, f_, p_, w_ in RACE.values()), 6000) * 100
assert wpct == 35
Q(T, "Caselet with table", I, "Women made up what percentage of all registered runners?",
  "35%", ["32.5%", "30%", "37.5%"],
  "Weight each category's percentage by its registrations",
  "Women: 40% of 2,400 = 960; 35% of 1,800 = 630; 30% of 1,200 = 360; 25% of 600 = 150. Total 2,100 of 6,000 = 35%.",
  ["960 + 630 + 360 + 150 = 2,100", "2,100 ÷ 6,000 = 35%"],
  why="32.5% is the simple average of the four percentages.", secs=55, stim=sid)

net_ = fees - sum(fin.values()) * 250
assert sum(fin.values()) == 5340 and net_ == 5025000 and fees - 6000 * 250 == 4860000
Q(T, "Caselet with table", A,
  "What was the organisers' fee collection minus the cost of the medals?",
  "₹50,25,000", ["₹48,60,000", "₹40,71,000", "₹13,35,000"],
  "Medals go to finishers only",
  "Finishers = 2,280 + 1,620 + 1,020 + 420 = 5,340. Medals cost 5,340 × 250 = ₹13,35,000. Fee collection ₹63,60,000 "
  "− ₹13,35,000 = ₹50,25,000.",
  ["Finishers = 5,340", "Medal cost = 13,35,000", "63,60,000 − 13,35,000 = 50,25,000"],
  why="₹48,60,000 buys medals for all 6,000 runners; ₹40,71,000 counts fees from finishers only; ₹13,35,000 is the "
      "medal cost itself.", secs=75, stim=sid)

non = {k: RACE[k][0] - fin[k] for k in RACE}
pc = F(non["Full marathon"], sum(non.values())) * 100
assert sum(non.values()) == 660 and pc == F(300, 11)
Q(T, "Caselet with table", A,
  "The runners who did not finish the full marathon form what percentage of all the runners who did not finish, "
  "across the four categories?",
  "27.27%", ["30%", "25%", "33.33%"],
  "Non-finishers = registrations × (100 − finished)%",
  "Non-finishers: 5 km 120, 10 km 180, half 180, full 180, total 660. The full marathon's share = 180 ÷ 660 = "
  "27.27%.",
  ["5 km: 5% of 2,400 = 120", "10 km: 10% of 1,800 = 180", "Half: 15% of 1,200 = 180", "Full: 30% of 600 = 180",
   "180 ÷ 660 × 100 = 27.27%"],
  why="30% is the full marathon's own non-finishing rate; 25% assumes the four categories share equally; 33.33% "
      "leaves out the 5 km race.", secs=80, stim=sid)

# ================================================================ Missing DI (B1 I2 A1): one set of 4
T = "Missing DI"
UNITS = {"U1": (2400, 96, None, None), "U2": (None, 150, F(5), None), "U3": (3200, None, F(7, 2), None),
         "U4": (None, None, F(6), 2820)}
dash = "—"
sid = stimulus("data_table", "Shirts stitched and rejected at four tailoring units (some values missing)",
               "The table shows, for four units of a garment company, the number of shirts stitched in a month, the "
               "number rejected at quality check, the rejection rate (rejected as a percentage of stitched) and the "
               "number accepted (stitched − rejected). Some values are missing (—); work them out from the "
               "others.\n\n" +
               md_table(["Unit", "Shirts stitched", "Rejected", "Rejection rate (%)", "Accepted"],
                        [[k, *[dash if c is None else (N(c) if isinstance(c, F) else ind(c)) for c in v]]
                         for k, v in UNITS.items()]),
               {"columns": ["unit", "stitched", "rejected", "rejection_pct", "accepted"],
                "rows": [[k, *[None if c is None else float(c) for c in v]] for k, v in UNITS.items()]})
stitched = {"U1": 2400, "U2": F(150) / F(5, 100), "U3": 3200, "U4": F(2820) / F(94, 100)}
rejected = {"U1": 96, "U2": 150, "U3": 3200 * F(35, 1000), "U4": stitched["U4"] * F(6, 100)}
accepted = {k: stitched[k] - rejected[k] for k in stitched}
assert stitched == {"U1": 2400, "U2": 3000, "U3": 3200, "U4": 3000}
assert rejected == {"U1": 96, "U2": 150, "U3": 112, "U4": 180}
assert accepted == {"U1": 2304, "U2": 2850, "U3": 3088, "U4": 2820}
assert F(96, 2400) * 100 == 4 and near(F(96, 2304) * 100, 4.17, 0.01)
Q(T, "Table with missing values", B, "What was the rejection rate of unit U1?",
  "4%", ["4.17%", "2.5%", "3.5%"],
  "Rejection rate = rejected ÷ stitched × 100",
  "U1 rejected 96 of the 2,400 shirts it stitched: 96 ÷ 2,400 = 4%.",
  ["96 ÷ 2,400 = 0.04", "= 4%"],
  why="4.17% divides by the accepted shirts (2,304); 2.5% inverts part of the calculation; 3.5% is U3's rate.",
  secs=35, stim=sid)

assert near(2820 * 1.06, 2989.2) and near(2820 * 0.94, 2650.8)
Q(T, "Table with missing values", I, "How many shirts did unit U4 stitch?",
  "3,000", ["2,989.2", "2,650.8", "3,120"],
  "Accepted shirts are (100 − rejection rate)% of the shirts stitched",
  "U4 rejected 6%, so the 2,820 accepted shirts are 94% of those stitched: 2,820 ÷ 0.94 = 3,000.",
  ["Accepted = 94% of stitched", "Stitched = 2,820 ÷ 0.94 = 3,000", "Check: 6% of 3,000 = 180 rejected"],
  why="2,989.2 adds 6% to 2,820 (a percentage of the wrong base); 2,650.8 takes 6% off 2,820; 94% of 3,120 is "
      "2,932.8, not 2,820.", secs=50, stim=sid)

d_ = accepted["U3"] - accepted["U2"]
assert d_ == 238 and 3200 - 3000 == 200
Q(T, "Table with missing values", I, "By how many shirts did U3's accepted shirts exceed U2's accepted shirts?",
  "238", ["200", "162", "312"],
  "Fill both rows first: U2 stitched = rejected ÷ rate; U3 rejected = stitched × rate",
  "U2: 150 is 5% of the shirts stitched, so U2 stitched 3,000 and accepted 2,850. U3: 3.5% of 3,200 = 112 rejected, "
  "so 3,088 accepted. Difference = 3,088 − 2,850 = 238.",
  ["U2 stitched = 150 ÷ 0.05 = 3,000; accepted = 2,850", "U3 rejected = 3,200 × 0.035 = 112; accepted = 3,088",
   "3,088 − 2,850 = 238"],
  why="200 compares stitched shirts; 162 subtracts the difference in rejections (38) instead of adding it; 312 has "
      "no basis.", secs=65, stim=sid)

overall = F(sum(rejected.values()), sum(stitched.values())) * 100
assert sum(rejected.values()) == 538 and sum(stitched.values()) == 11600
assert near(overall, 4.6379, 1e-3) and F(4 + 5 + F(7, 2) + 6, 4) == F(37, 8)
assert near(F(538, sum(accepted.values())) * 100, 4.86, 5e-3) and near(F(358, 8600) * 100, 4.16, 5e-3)
Q(T, "Table with missing values", A,
  "What was the overall rejection rate of the four units taken together (correct to two decimal places)?",
  "4.64%", ["4.63%", "4.86%", "4.16%"],
  "Overall rate = total rejected ÷ total stitched — not the average of the four rates",
  "Total rejected = 96 + 150 + 112 + 180 = 538. Total stitched = 2,400 + 3,000 + 3,200 + 3,000 = 11,600. Overall "
  "rate = 538 ÷ 11,600 = 4.6379…% ≈ 4.64%.",
  ["Rejected: 96 + 150 + 112 + 180 = 538", "Stitched: 11,600", "538 ÷ 11,600 × 100 = 4.6379… ≈ 4.64%"],
  why="4.63% is the simple average of the four rates (4.625%) rounded, which ignores the different volumes; "
      "4.86% divides by the accepted total (11,062); 4.16% leaves out U4 (358 ÷ 8,600).", secs=90, stim=sid)

# ================================================================ Quantity Comparison (B4 I3 A1)
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


q1v, q2v = F(35, 100) * 260, F(28, 100) * 320
assert (q1v, q2v) == (91, F(896, 10))
qc("Quantity I vs II", B, "35% of 260", "28% of 320", [q1v], [q2v], ">", ["<", "<="],
   "Compute each percentage exactly",
   "Quantity I = 0.35 × 260 = 91. Quantity II = 0.28 × 320 = 89.6. So Quantity I > Quantity II.",
   ["I: 35% of 260 = 91", "II: 28% of 320 = 89.6", "91 > 89.6"],
   why="'Quantity I < Quantity II' comes from assuming the larger base (320) gives the larger value.", secs=30)

q1v = F(13 + 17 + 21 + 25 + 29, 5)
q2v = sorted([12, 30, 19, 24, 22])[2]
assert (q1v, q2v) == (21, 22)
qc("Arithmetic-based comparison", B, "The average of 13, 17, 21, 25 and 29",
   "The median of 12, 30, 19, 24 and 22", [q1v], [F(q2v)], "<", [">", ">="],
   "The average of an evenly spaced list is its middle term; the median is the middle value after sorting",
   "Quantity I: the numbers rise by 4, so the average is the middle term, 21. Quantity II: sorted, the numbers are "
   "12, 19, 22, 24, 30, so the median is 22. Quantity I < Quantity II.",
   ["I: 13, 17, 21, 25, 29 ⇒ average 21", "II: 12, 19, 22, 24, 30 ⇒ median 22", "21 < 22"],
   why="'Quantity I > Quantity II' takes the middle value of II without sorting (19).", secs=35)

q1v, q2v = F(189, 54), F(200, 60)
assert (q1v, q2v) == (F(7, 2), F(10, 3))
qc("Arithmetic-based comparison", B, "Time (in hours) taken by a car at 54 km/h to cover 189 km",
   "Time (in hours) taken by a car at 60 km/h to cover 200 km", [q1v], [q2v], ">", ["<=", "<"],
   "Time = distance ÷ speed",
   "Quantity I = 189 ÷ 54 = 3.5 hours. Quantity II = 200 ÷ 60 = 3⅓ hours ≈ 3.33 hours. So Quantity I > Quantity II.",
   ["I: 189 ÷ 54 = 3.5", "II: 200 ÷ 60 = 3.33", "3.5 > 3.33"],
   why="'Quantity I < Quantity II' assumes the longer distance always takes longer.", secs=35)

sums = sorted({a + 36 // a for a in range(1, 37) if 36 % a == 0})
assert sums == [12, 13, 15, 20, 37]
qc("Quantity I vs II", B, "The sum of two positive whole numbers whose product is 36", "13",
   [F(x) for x in sums], [F(13)], "cbe", [">=", "<="],
   "List every possible pair before comparing",
   "Pairs with product 36: (1, 36), (2, 18), (3, 12), (4, 9), (6, 6), with sums 37, 20, 15, 13 and 12. Quantity I "
   "can be more than, equal to or less than 13, so the relationship cannot be established.",
   ["Pairs: 1 × 36, 2 × 18, 3 × 12, 4 × 9, 6 × 6", "Sums: 37, 20, 15, 13, 12", "12 < 13, 13 = 13, 15 > 13",
    "Cannot be established"],
   why="'Quantity I ≥ Quantity II' misses the pair (6, 6) with sum 12; 'Quantity I ≤ Quantity II' looks only at "
       "(6, 6) and (4, 9).", secs=45)

q1v = F(173, 100) * 144 / 4
q2v = F(22, 7) * F(81, 4)
assert q1v == F(6228, 100) and near(q2v, 63.6429, 1e-3)
qc("Quantity I vs II", I, "Area (cm²) of an equilateral triangle of side 12 cm (take √3 = 1.73)",
   "Area (cm²) of a circle of diameter 9 cm (take π = 22/7)", [q1v], [q2v], "<", [">", ">="],
   "Area of an equilateral triangle = (√3/4)a²; area of a circle = πr² with r = diameter ÷ 2",
   "Quantity I = 1.73 × 144 ÷ 4 = 1.73 × 36 = 62.28 cm². Quantity II = 22/7 × 4.5² = 22/7 × 20.25 ≈ 63.64 cm². So "
   "Quantity I < Quantity II.",
   ["I: (1.73/4) × 144 = 62.28", "II: r = 4.5, r² = 20.25, 22/7 × 20.25 ≈ 63.64", "62.28 < 63.64"],
   why="'Quantity I > Quantity II' comes from using π = 3 instead of the stated 22/7 (3 × 20.25 = 60.75).", secs=60)

q1v = F(200 + 250, 30) * F(18, 5)
assert q1v == 54
qc("Arithmetic-based comparison", I,
   "Speed (km/h) of a 200 m long train that crosses a 250 m long platform in 30 seconds", "52",
   [q1v], [F(52)], ">", ["<", "<="],
   "Crossing a platform: distance = train + platform",
   "Quantity I = (200 + 250) ÷ 30 = 15 m/s = 15 × 18/5 = 54 km/h. So Quantity I > Quantity II.",
   ["Distance = 450 m", "Speed = 15 m/s", "15 × 3.6 = 54 km/h", "54 > 52"],
   why="'Quantity I < Quantity II' uses only the train's length (200 ÷ 30 = 6⅔ m/s = 24 km/h).", secs=50)

ints = [x for x in range(-10, 11) if x * x < 20]
divs = [d for d in range(1, 49) if 48 % d == 0]
assert len(ints) == 9 and len(divs) == 10
qc("Quantity I vs II", I, "The number of integers x for which x² < 20",
   "The number of positive divisors of 48", [F(len(ints))], [F(len(divs))], "<", [">=", ">"],
   "Count negative integers and zero too; count divisors from the prime factorisation",
   "Quantity I: x² < 20 holds for x = −4, −3, …, 3, 4, which is 9 integers. Quantity II: 48 = 2⁴ × 3, so it has "
   "(4 + 1)(1 + 1) = 10 divisors. So Quantity I < Quantity II.",
   ["I: −4 to 4 ⇒ 9 integers", "II: 48 = 2⁴ × 3 ⇒ 5 × 2 = 10 divisors", "9 < 10"],
   why="'≥' and '>' come from miscounting the divisors of 48 (for example missing 16 and 24 and getting 8).",
   secs=55)

xs_ = [x for x in range(-10, 11) if 2 ** (x + 1) + F(2) ** (x - 1) == 80]
ys_ = [y for y in range(-20, 21) if y * y - 11 * y + 30 == 0]
assert xs_ == [5] and ys_ == [5, 6]
qc("Quantity I vs II", A, "The value of x, where 2^(x + 1) + 2^(x − 1) = 80",
   "The value of y, where y² − 11y + 30 = 0", [F(5)], [F(5), F(6)], "<=", ["<", ">="],
   "Factor out the smaller power: 2^(x − 1)(2² + 1); a quadratic has two roots to compare against",
   "Quantity I: 2^(x − 1) × (4 + 1) = 80, so 2^(x − 1) = 16 = 2⁴ and x = 5. Quantity II: (y − 5)(y − 6) = 0, so "
   "y = 5 or 6. x equals y in one case and is smaller in the other, so Quantity I ≤ Quantity II.",
   ["I: 2^(x − 1)(4 + 1) = 80 ⇒ 2^(x − 1) = 16 ⇒ x = 5", "II: y = 5 or 6", "5 = 5 and 5 < 6", "So I ≤ II"],
   why="'Quantity I < Quantity II' misses y = 5; 'Quantity I ≥ Quantity II' compares only with y = 5.", secs=80,
   by=BRUTE)

# ================================================================ Data Sufficiency (Quant) (B1 I2 A2)
T = "Data Sufficiency (Quant)"
DS2 = {"I": "Statement I alone is sufficient, but statement II alone is not",
       "II": "Statement II alone is sufficient, but statement I alone is not",
       "either": "Either statement I alone or statement II alone is sufficient",
       "both": "Both statements I and II together are needed",
       "neither": "Statements I and II together are not sufficient"}
DS_PRE = ("Each question below is followed by two statements. Decide whether the data in the statements are "
          "sufficient to answer the question.")
DS3_PRE = "The question below is followed by three statements. Decide which statements are sufficient to answer it."


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


def suff_map(cands, conds, target):
    """For three statements: which subsets fix the target uniquely (each subset must allow at least one case)."""
    out = {}
    for r in (1, 2, 3):
        for sub in itertools.combinations(range(3), r):
            vals = {target(c) for c in cands if all(conds[i](c) for i in sub)}
            assert vals, sub
            out[sub] = len(vals) == 1
    return out


cands = [F(k, 4) for k in range(1, 201)]
verdict = ds2_verdict(cands, lambda s: s * s * 2 == 128, lambda s: s * s == 16 * 4, lambda s: 4 * s)
assert verdict == "either"
Q(T, "Two-statement", B,
  f"{DS_PRE}\nQuestion: What is the perimeter of the square?\n"
  "I. The diagonal of the square is 8√2 cm.\nII. The area of the square equals the area of a rectangle measuring "
  "16 cm by 4 cm.",
  DS2["either"], [DS2["I"], DS2["II"], DS2["both"]],
  "One measurement fixes a square completely",
  "I: side = diagonal ÷ √2 = 8 cm, so the perimeter is 32 cm — sufficient. II: area = 64 cm², so the side is 8 cm "
  "(a length is positive) and the perimeter is 32 cm — sufficient. Either statement alone answers the question.",
  ["I: side = 8√2 ÷ √2 = 8 ⇒ perimeter 32 cm", "II: side² = 64 ⇒ side = 8 ⇒ perimeter 32 cm",
   "Each alone is sufficient"],
  why="'Both together' is chosen when a candidate does not notice that a square has only one free measurement.",
  secs=40, by=BRUTE)

cands = [(F(b, 2), F(g, 2)) for b in range(20, 41) for g in range(20, 41)]
target = lambda c: (c[0] + c[1]) / 2
s1 = lambda c: (30 * target(c) + 30) / 31 == target(c) + F(1, 2)
s2 = lambda c: c[0] == 15
verdict = ds2_verdict(cands, s1, s2, target)
assert verdict == "I" and {target(c) for c in cands if s1(c)} == {F(29, 2)}
Q(T, "Two-statement", I,
  f"{DS_PRE}\nQuestion: What is the average age of the 30 students of a class (15 boys and 15 girls)?\n"
  "I. When the class teacher, who is 30 years old, is included, the average age rises by 6 months.\n"
  "II. The average age of the 15 boys is 15 years.",
  DS2["I"], [DS2["either"], DS2["both"], DS2["II"]],
  "Inclusion changes the total by the new member's age; a group's average needs both sub-group averages",
  "I: if the class average is a, then 30a + 30 = 31(a + 0.5), so a = 14.5 years — sufficient. II gives the boys' "
  "average only; the girls' average is unknown — not sufficient.",
  ["I: 30a + 30 = 31a + 15.5 ⇒ a = 14.5", "II: girls' average unknown ⇒ not sufficient", "I alone is sufficient"],
  why="'Either' assumes the girls' average equals the boys'; 'Both' is not needed because I alone fixes the "
      "average.", secs=60, by=BRUTE)

DS3W = {"all": "All three statements together are necessary",
        "any2": "Any two of the three statements together are sufficient",
        "23": "Only statements II and III together are sufficient",
        "none": "Even all three statements together are not sufficient"}
cands = [(inc, s_, q_) for inc in range(1000, 200001, 1000) for s_ in (F(1, 10), F(1, 5), F(3, 10), F(9, 25))
         for q_ in (F(1, 5), F(3, 10), F(2, 5), F(1, 2))]
conds = [lambda c: c[1] == F(1, 5), lambda c: c[2] == F(3, 10),
         lambda c: c[2] * (1 - c[1]) * c[0] == 9600]
m = suff_map(cands, conds, lambda c: c[0])
assert m == {(0,): False, (1,): False, (2,): False, (0, 1): False, (0, 2): False, (1, 2): False, (0, 1, 2): True}
assert F(9600, F(3, 10) * F(4, 5)) == 40000
Q(T, "Three-statement", I,
  f"{DS3_PRE}\nQuestion: What is Neha's monthly income?\n"
  "I. She saves 20% of her income and spends the rest.\n"
  "II. Her rent is 30% of her total monthly expenditure.\n"
  "III. Her monthly rent is ₹9,600.",
  DS3W["all"], [DS3W["any2"], DS3W["23"], DS3W["none"]],
  "Chain of percentages: rent = 30% of expenditure = 30% of 80% of income",
  "With all three: rent = 0.3 × 0.8 × income = 0.24 × income = 9,600, so the income is ₹40,000. Without I, the "
  "share of income spent is unknown; without II, the rent's share of spending is unknown; without III, there is no "
  "rupee figure. So all three are needed.",
  ["I + II: only percentages, no amount", "I + III: rent's share of spending unknown",
   "II + III: expenditure = 32,000, but its share of income unknown", "All three: 0.24 × income = 9,600 ⇒ 40,000"],
  why="'Only II and III' gives the expenditure (₹32,000) but not the income; 'any two' fails for the same reason.",
  secs=70, by=BRUTE)

cands = [(F(r, 2), F(P_)) for r in range(1, 61) for P_ in range(1000, 50001, 250)]
cands += [(F(r, 2), F(265625, 100) / ((1 + F(r, 200)) ** 2 - 1)) for r in range(1, 61)]
s1 = lambda c: c[0] * 8 == 100
s2 = lambda c: c[1] * ((1 + c[0] / 100) ** 2 - 1) == F(265625, 100)
verdict = ds2_verdict(cands, s1, s2, lambda c: c[0])
assert verdict == "I" and len({c[0] for c in cands if s2(c)}) > 1
assert 10000 * ((1 + F(25, 200)) ** 2 - 1) == F(265625, 100)
Q(T, "Two-statement", A,
  f"{DS_PRE}\nQuestion: What is the rate of interest per annum?\n"
  "I. A sum lent at this rate of simple interest doubles itself in 8 years.\n"
  "II. The compound interest for 2 years, compounded annually, on a certain sum at this rate is ₹2,656.25.",
  DS2["I"], [DS2["either"], DS2["both"], DS2["II"]],
  "A rate can be found from a doubling time, but not from an interest amount on an unknown sum",
  "I: doubling means the interest equals the principal: R × 8 = 100, so R = 12.5% — sufficient. II: one equation "
  "with two unknowns (sum and rate): ₹10,000 at 12.5% fits, but so does a larger sum at a lower rate (about "
  "₹12,649 at 10%) — not sufficient.",
  ["I: SI = P in 8 years ⇒ 8R = 100 ⇒ R = 12.5%", "II: P[(1 + R/100)² − 1] = 2,656.25 has many (P, R) solutions",
   "I alone is sufficient"],
  why="'Either' assumes the sum in II is known; 'Both' is unnecessary because I alone fixes the rate.", secs=80,
  by=BRUTE)

cands = [(p24, g1, F(g2)) for p24 in range(40000, 60001, 500) for g1 in range(0, 21) for g2 in range(0, 21)]
target = lambda c: c[0] * (1 + F(c[1], 100)) * (1 + c[2] / 100)
conds = [lambda c: c[1] == 10 and c[2] == 12, lambda c: c[0] == 50000,
         lambda c: c[0] * (1 + F(c[1], 100)) * c[2] / 100 == 6600]
m = suff_map(cands, conds, target)
assert m == {(0,): False, (1,): False, (2,): False, (0, 1): True, (0, 2): True, (1, 2): False, (0, 1, 2): True}
assert target((50000, 10, F(12))) == 61600
Q(T, "Three-statement", A,
  f"{DS3_PRE}\nQuestion: What was the population of the town in 2026?\n"
  "I. The population grew by 10% from 2024 to 2025 and by 12% from 2025 to 2026.\n"
  "II. The population in 2024 was 50,000.\n"
  "III. The population increased by 6,600 from 2025 to 2026.",
  "Either I and II together or I and III together are sufficient",
  ["Only I and II together are sufficient", "Any two of the three statements together are sufficient",
   "All three statements together are necessary"],
  "Check every pair; a pair works only if it fixes one base value and the growth that follows it",
  "I + II: 50,000 × 1.1 × 1.12 = 61,600 — sufficient. I + III: 12% of the 2025 population = 6,600, so the 2025 "
  "population was 55,000 and 2026's was 61,600 — sufficient. II + III: the growth from 2024 to 2025 is unknown, so "
  "the 2025 base for the 6,600 is unknown (for example 10% then 12%, or 20% then 11%, give 61,600 or 66,600) — not "
  "sufficient. No statement alone is enough.",
  ["I + II: 50,000 × 1.1 × 1.12 = 61,600", "I + III: 0.12 × P₂₀₂₅ = 6,600 ⇒ P₂₀₂₅ = 55,000 ⇒ P₂₀₂₆ = 61,600",
   "II + III: two unknown growth rates ⇒ not sufficient", "Answer: I with II, or I with III"],
  why="'Only I and II' misses that III can replace II; 'any two' wrongly includes II + III.", secs=110, by=BRUTE)

# ================================================================ checks and output
assert len(QUESTIONS) == TOTAL, len(QUESTIONS)
assert len(STIMULI) == 11

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_003_plan.json").read_text(encoding="utf-8"))
qa = next(s for s in plan["subjects"] if s["subject"] == SUBJECT)
have = Counter((q["topic"], q["difficulty"]) for q in QUESTIONS)
want = Counter({(t["topic"], d): n for t in qa["topics"] for d, n in t["quota"].items() if n})
assert have == want, set(have.items()) ^ set(want.items())
subs = {t["topic"]: set(t["subtopics"]) for t in qa["topics"]}
assert all(q["subtopic"] in subs[q["topic"]] for q in QUESTIONS)
assert QUESTIONS[0]["question_id"] == qa["question_ids"][0] and QUESTIONS[-1]["question_id"] == qa["question_ids"][1]
assert STIMULI[0]["stimulus_id"] == qa["stimulus_id_start"]
for s in STIMULI:  # every DI set has 3 to 6 questions
    assert 3 <= _set_pos[s["stimulus_id"]] <= 6, s["stimulus_id"]
keys = Counter(q["correct_answer"] for q in QUESTIONS)
assert keys == Counter({k: 50 for k in "ABCD"})
assert INDEPENDENT <= {q["question_id"] for q in QUESTIONS}

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_003",
    "created_at": TODAY,
    "notes": "BATCH_003, Quantitative Aptitude part: 200 original questions (60 Basic, 80 Intermediate, 60 Advanced) "
             "with 11 shared DI stimuli on new data sets. Every answer was recomputed by tools/batch_003/quant.py "
             "before writing; questions tagged ai:independent-check were also re-solved from the stem and options "
             "alone by a separate solver. Pending human review.",
    "stimuli": STIMULI,
    "questions": QUESTIONS,
}
out = ROOT / "batches" / "parts" / "BATCH_003_QUANT.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(QUESTIONS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(keys.items()))}, "
      f"independent-check {len(INDEPENDENT)})")
