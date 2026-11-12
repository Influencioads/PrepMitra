"""Writes batches/parts/BATCH_001_QUANT.json: the 200 Quantitative Aptitude questions of BATCH_001.

Every answer is recomputed here before the file is written: arithmetic with exact fractions, series regenerated
from their rule, quadratic roots substituted back into the equations, probabilities and arrangements counted by
brute force, data-sufficiency statements checked by enumerating every candidate value, approximation answers
checked to be the option nearest the exact value. If any assertion fails, nothing is written.

    python tools/batch_001/quant.py          (run from docs/question-bank)
"""

import itertools
import json
import math
import random
import sys
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
_rng = random.Random(20261105)
KEYS = list("ABCD" * (TOTAL // 4))
_rng.shuffle(KEYS)

QUESTIONS, STIMULI = [], []
_set_pos = {}
_FIRST_ID = 6
_FIRST_STIM = 2

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
def Q(topic, sub, diff, text, ans, wrong, concept, expl, steps, short=None, why=None, secs=None, stim=None):
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
                         "verified_by": ["script:recompute", "ai:author-solve"], "verified_at": TODAY},
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


# ================================================================ Simplification (B3 I4 A3)
T = "Simplification"
v = F(72) / 8 * 4 - 3 * 5 + 11
assert v == 32 and ((F(72) / 8 * 4 - 3) * 5) + 11 == 176 and 36 - (15 + 11) == 10
assert F(72) / (8 * 4) - 15 + 11 == F(-7, 4)
Q(T, "BODMAS", B, "Simplify: 72 ÷ 8 × 4 − 3 × 5 + 11 = ?",
  "32", ["176", "10", "−1.75"],
  "BODMAS: division and multiplication from left to right, then addition and subtraction from left to right",
  "Division and multiplication come first and are done in the order they appear: 72 ÷ 8 × 4 = 36 and 3 × 5 = 15. "
  "Then 36 − 15 + 11 = 32.",
  ["72 ÷ 8 = 9, then 9 × 4 = 36", "3 × 5 = 15", "36 − 15 + 11 = 21 + 11 = 32"],
  why="176 comes from working strictly left to right and ignoring precedence; 10 from computing 36 − (15 + 11); "
      "−1.75 from doing 8 × 4 before the division.", secs=30)

v = F(10, 3) * F(12, 5) + F(7, 4) / F(35, 100)
assert v == 13 and F(10, 3) * F(12, 5) + F(7, 4) * F(35, 100) == F(86125, 10000)
assert F(33, 10) * F(12, 5) + 5 == F(1292, 100) and near((8 + F(7, 4)) / F(35, 100), 27.857142857, 1e-6)
Q(T, "Fractions and decimals", B, "What is the value of 3⅓ × 2.4 + 1¾ ÷ 0.35?",
  "13", ["8.6125", "12.92", "27.86"],
  "Converting mixed numbers and decimals to fractions, then BODMAS",
  "3⅓ = 10/3 and 2.4 = 12/5, so the product is 8. 1¾ ÷ 0.35 = (7/4) ÷ (7/20) = 5. The sum is 13.",
  ["3⅓ × 2.4 = 10/3 × 12/5 = 120/15 = 8", "1¾ ÷ 0.35 = 7/4 × 20/7 = 5", "8 + 5 = 13"],
  short="0.35 = 7/20 and 1¾ = 7/4, so the 7s cancel: 20/4 = 5.",
  why="8.6125 multiplies by 0.35 instead of dividing; 12.92 treats 3⅓ as 3.3; 27.86 adds before dividing.", secs=40)

v = 42 + 13 - F(9, 100) * 100
assert 42 ** 2 == 1764 and 13 ** 3 == 2197 and F(9, 100) ** 2 == F(81, 10000) and v == 46
assert 42 + 13 - F(9, 10) * 100 == -35 and 42 + 13 - F(9, 1000) * 100 == F(541, 10) and (42 + 13 - F(9, 100)) * 100 == 5491
Q(T, "Square and cube roots", B, "√1764 + ∛2197 − √0.0081 × 100 = ?",
  "46", ["−35", "54.1", "5491"],
  "Perfect squares and cubes; square root of a decimal (halve the number of decimal places)",
  "√1764 = 42, ∛2197 = 13 and √0.0081 = 0.09 (0.0081 has four decimal places, so its root has two). "
  "Then 42 + 13 − 0.09 × 100 = 55 − 9 = 46.",
  ["√1764 = 42 (42² = 1764)", "∛2197 = 13 (13³ = 2197)", "√0.0081 = √81 ÷ √10000 = 9 ÷ 100 = 0.09",
   "0.09 × 100 = 9", "42 + 13 − 9 = 46"],
  short="Unit digit 4 with 1764 between 40² and 45² gives 42; a cube ending in 7 has a root ending in 3, so 13.",
  why="−35 takes √0.0081 as 0.9; 54.1 takes it as 0.009; 5491 subtracts before multiplying by 100.", secs=40)

v = F(9) * 8 / 4
assert round(27 ** (2 / 3)) == 9 and round(16 ** 0.75) == 8 and round(32 ** 0.4) == 4 and v == 18
assert F(9) * 12 / 4 == 27 and 9 * 8 == 72 and F(18) * 8 / 4 == 36
Q(T, "Surds and indices", I, "Find the value of 27^(2/3) × 16^(3/4) ÷ 32^(2/5).",
  "18", ["27", "72", "36"],
  "Fractional exponents: a^(m/n) = (n-th root of a)^m",
  "Write each base as a power: 27 = 3³, 16 = 2⁴ and 32 = 2⁵. Then 27^(2/3) = 3² = 9, 16^(3/4) = 2³ = 8 and "
  "32^(2/5) = 2² = 4, so the value is 9 × 8 ÷ 4 = 18.",
  ["27^(2/3) = (3³)^(2/3) = 3² = 9", "16^(3/4) = (2⁴)^(3/4) = 2³ = 8", "32^(2/5) = (2⁵)^(2/5) = 2² = 4",
   "9 × 8 ÷ 4 = 72 ÷ 4 = 18"],
  short="Take the root first, then the power: cube root of 27 is 3, squared 9; fourth root of 16 is 2, cubed 8.",
  why="27 treats 16^(3/4) as 16 × 3/4 = 12; 72 forgets the division by 4; 36 treats 27^(2/3) as 18.", secs=50)

inner = F(36) / (4 + 2) * 5
v = F(1, 2) * (84 - inner) + 17
assert inner == 30 and v == 44
assert F(1, 2) * (84 - F(36) / 30) + 17 == F(584, 10) and (84 - inner + 17) / 2 == F(71, 2) and 84 - inner + 17 == 71
Q(T, "BODMAS", I, "Simplify: ½ of [84 − {36 ÷ (4 + 2) × 5}] + 17",
  "44", ["58.4", "35.5", "71"],
  "Order of brackets ( ), { }, [ ] and the 'of' operation",
  "Open the innermost bracket first: (4 + 2) = 6. Inside the curly bracket, 36 ÷ 6 × 5 = 30. The square bracket "
  "gives 84 − 30 = 54, half of it is 27, and 27 + 17 = 44.",
  ["(4 + 2) = 6", "{36 ÷ 6 × 5} = 6 × 5 = 30", "[84 − 30] = 54", "½ of 54 = 27", "27 + 17 = 44"],
  why="58.4 computes 36 ÷ (6 × 5); 35.5 adds 17 before halving; 71 ignores the ½ of.", secs=50)

part1 = (F(7, 12) + F(5, 18) - F(1, 4)) / F(11, 36)
part2 = F(12, 5) * F(5, 6)
v = part1 + part2
assert part1 == 2 and part2 == 2 and v == 4
assert F(1, 2) + 2 == F(5, 2) and 2 + (2 * F(5, 6) + F(2, 5)) == F(61, 15)
Q(T, "Fractions and decimals", I, "(7/12 + 5/18 − 1/4) ÷ 11/36 + 2⅖ × 5/6 = ?",
  "4", ["2½", "4 1/15", "5"],
  "LCM of denominators; dividing by a fraction is multiplying by its reciprocal; mixed numbers become improper "
  "fractions before multiplying",
  "With LCM 36 the bracket is (21 + 10 − 9)/36 = 22/36, and 22/36 ÷ 11/36 = 2. Next, 2⅖ = 12/5 and "
  "12/5 × 5/6 = 2. The total is 4.",
  ["LCM of 12, 18, 4 = 36: 7/12 = 21/36, 5/18 = 10/36, 1/4 = 9/36", "Bracket = (21 + 10 − 9)/36 = 22/36",
   "22/36 ÷ 11/36 = 22/36 × 36/11 = 2", "2⅖ = 12/5; 12/5 × 5/6 = 12/6 = 2", "2 + 2 = 4"],
  why="2½ divides the wrong way (11/36 ÷ 22/36 = ½); 4 1/15 multiplies only the whole part 2 by 5/6 and then adds ⅖; "
      "5 is a slip in the bracket.", secs=55)

v = F(28 + 16, 14 - 10)
assert 28 ** 2 == 784 and 16 ** 3 == 4096 and v == 11
assert F(28 + 64, 4) == 23 and 28 + 16 == 44 and F(44, 12 - 10) == 22
Q(T, "Square and cube roots", I, "Find the value of (√784 + ∛4096) ÷ (√196 − √100).",
  "11", ["23", "44", "22"],
  "Square roots and cube roots of perfect powers",
  "√784 = 28 and ∛4096 = 16, so the numerator is 44. √196 = 14 and √100 = 10, so the denominator is 4. "
  "44 ÷ 4 = 11.",
  ["√784 = 28 (28² = 784)", "∛4096 = 16 (16³ = 4096)", "Numerator = 28 + 16 = 44",
   "Denominator = 14 − 10 = 4", "44 ÷ 4 = 11"],
  short="4096 = 2¹², so its cube root is 2⁴ = 16 (not √4096 = 64).",
  why="23 uses √4096 = 64 instead of the cube root; 44 forgets the denominator; 22 takes √196 as 12.", secs=50)

# Advanced simplification
sols = [x for x in range(-20, 21) if (2 * x - 1) + 2 * (x + 2) == 3 * (x + 3)]
assert sols == [6]
assert [x for x in range(-20, 21) if (2 * x - 1) + 2 * (x + 2) == 3 * x + 3] == [0]
assert [x for x in range(-20, 21) if (2 * x - 1) + (2 * x + 2) == 3 * (x + 3)] == [8]
assert [x for x in range(-20, 21) if 2 * x + 2 * (x + 2) == 3 * (x + 3)] == [5]
Q(T, "Surds and indices", A, "If 3^(2x − 1) × 9^(x + 2) = 27^(x + 3), what is the value of x?",
  "6", ["0", "8", "5"],
  "Bring every term to the same base and equate exponents",
  "Write 9 = 3² and 27 = 3³. The left side becomes 3^(2x − 1) × 3^(2x + 4) = 3^(4x + 3) and the right side "
  "3^(3x + 9). Equating exponents, 4x + 3 = 3x + 9, so x = 6.",
  ["9^(x + 2) = (3²)^(x + 2) = 3^(2x + 4)", "Left side = 3^((2x − 1) + (2x + 4)) = 3^(4x + 3)",
   "27^(x + 3) = (3³)^(x + 3) = 3^(3x + 9)", "4x + 3 = 3x + 9 ⇒ x = 6",
   "Check: left exponent 4(6) + 3 = 27; right exponent 3(6) + 9 = 27"],
  why="0 comes from writing 27^(x + 3) as 3^(3x + 3); 8 from writing 9^(x + 2) as 3^(2x + 2); 5 from dropping the "
      "−1 in the first exponent.", secs=75)

rhs = 15 ** 2 - 99
known = F(375, 1000) * 168
v = (rhs - known) * F(5, 2) / F(5, 4)
assert rhs == 126 and known == 63 and v == 126 and (v / F(5, 2)) * F(5, 4) + known == rhs
assert (rhs - known) * F(5, 4) / F(5, 2) == F(63, 2) and rhs * 2 == 252 and (rhs - 56) * 2 == 140
Q(T, "Fractions and decimals", A, "What will come in place of the question mark (?)?\n(? ÷ 2.5) × 1¼ + 37.5% of 168 = 15² − 99",
  "126", ["31.5", "252", "140"],
  "Solving for an unknown in a simplification; 37.5% = 3/8",
  "The right side is 225 − 99 = 126 and 37.5% of 168 = 63, so (? ÷ 2.5) × 1.25 = 63. Since 1.25 ÷ 2.5 = ½, "
  "? × ½ = 63 and ? = 126.",
  ["15² − 99 = 225 − 99 = 126", "37.5% of 168 = 3/8 × 168 = 63", "(? ÷ 2.5) × 1.25 = 126 − 63 = 63",
   "1.25 ÷ 2.5 = 0.5, so ? × 0.5 = 63", "? = 126"],
  short="÷ 2.5 then × 1.25 is the same as halving, so ? = 2 × 63.",
  why="31.5 multiplies by 1.25/2.5 instead of dividing; 252 forgets to subtract 63; 140 uses 1/3 for 37.5%.",
  secs=80)

a2b2 = 2 * (5 + 3)
v = F(a2b2) * 7 / F(7, 100)
assert near((math.sqrt(5) + math.sqrt(3)) ** 2 + (math.sqrt(5) - math.sqrt(3)) ** 2, 16)
assert a2b2 == 16 and 7 ** 3 == 343 and F(7, 100) ** 2 == F(49, 10000) and v == 1600
assert F(16) * 7 / F(7, 10) == 160 and F(16) * 7 / F(7, 1000) == 16000 and F(32) * 7 / F(7, 100) == 3200
Q(T, "Surds and indices", A, "Simplify: [(√5 + √3)² + (√5 − √3)²] × ∛343 ÷ √0.0049",
  "1600", ["160", "16000", "3200"],
  "Identity (a + b)² + (a − b)² = 2(a² + b²); roots of decimals",
  "By the identity the bracket is 2(5 + 3) = 16, because the 2√15 terms cancel. ∛343 = 7 and √0.0049 = 0.07. "
  "So the value is 16 × 7 ÷ 0.07 = 112 ÷ 0.07 = 1600.",
  ["(√5 + √3)² = 8 + 2√15 and (√5 − √3)² = 8 − 2√15", "Sum = 16 (the surd terms cancel)",
   "∛343 = 7", "√0.0049 = √49 ÷ √10000 = 7 ÷ 100 = 0.07", "16 × 7 ÷ 0.07 = 112 ÷ 0.07 = 1600"],
  short="7 ÷ 0.07 = 100, so the answer is 16 × 100.",
  why="160 takes √0.0049 as 0.7; 16000 takes it as 0.007; 3200 doubles the identity twice (32 instead of 16).",
  secs=75)

# ================================================================ Approximation (B3 I4 A3)
T = "Approximation"
exact = 0.2497 * 639.8 + 0.1502 * 480.3
nearest(exact, [232, 212, 252, 272], 232)
Q(T, "Percentage approximation", B,
  "What approximate value should come in place of the question mark (?)?\n24.97% of 639.8 + 15.02% of 480.3 ≈ ?",
  "232", ["212", "252", "272"],
  "Round each percentage and number to the nearest convenient value",
  f"24.97% ≈ 25% and 639.8 ≈ 640, so the first term is about 160. 15.02% ≈ 15% and 480.3 ≈ 480, so the second "
  f"term is about 72. The sum is about 232 (exact value {exact:.2f}).",
  ["24.97% of 639.8 ≈ 25% of 640 = 160", "15.02% of 480.3 ≈ 15% of 480 = 72", "160 + 72 = 232",
   f"Exact value = {exact:.2f}, so the closest option is 232"],
  short="25% is a quarter: 640 ÷ 4 = 160; 15% = 10% + 5% = 48 + 24.", secs=35)

exact = math.sqrt(1023.8) + math.sqrt(399.6) * 3.98
nearest(exact, [112, 208, 132, 92], 112)
Q(T, "Root approximation", B,
  "Find the approximate value of ? in: √1023.8 + √399.6 × 3.98 ≈ ?",
  "112", ["208", "132", "92"],
  "Round to the nearest perfect square, then apply BODMAS",
  f"√1023.8 ≈ √1024 = 32 and √399.6 ≈ √400 = 20. Multiplication comes before addition: 20 × 4 = 80, so the value "
  f"is about 32 + 80 = 112 (exact {exact:.2f}).",
  ["√1023.8 ≈ √1024 = 32", "√399.6 ≈ √400 = 20; 3.98 ≈ 4", "20 × 4 = 80", "32 + 80 = 112"],
  why="208 adds the two roots first and then multiplies by 4 ((32 + 20) × 4), ignoring BODMAS.", secs=35)

exact = 839.89 / 12.03 + 14.98 * 6.02
nearest(exact, [160, 140, 180, 200], 160)
Q(T, "Mixed approximation", B,
  "What approximate value will replace the question mark?\n839.89 ÷ 12.03 + 14.98 × 6.02 = ?",
  "160", ["140", "180", "200"],
  "Round each number to a value that divides or multiplies cleanly",
  f"839.89 ≈ 840 and 12.03 ≈ 12, so the quotient is about 70. 14.98 × 6.02 ≈ 15 × 6 = 90. The sum is about 160 "
  f"(exact {exact:.2f}).",
  ["839.89 ÷ 12.03 ≈ 840 ÷ 12 = 70", "14.98 × 6.02 ≈ 15 × 6 = 90", "70 + 90 = 160"], secs=35)

exact = (0.4489 * 1199.7 - 251.9) / 800.2 * 100
nearest(exact, [36, 32, 40, 28], 36)
Q(T, "Percentage approximation", I,
  "What approximate value should come in place of the question mark (?)?\n44.89% of 1199.7 − ?% of 800.2 ≈ 251.9",
  "36", ["32", "40", "28"],
  "Rounding, then solving a simple linear equation for the unknown percentage",
  f"44.89% of 1199.7 ≈ 45% of 1200 = 540. Then ?% of 800 ≈ 540 − 252 = 288, so ? ≈ 288 ÷ 8 = 36 "
  f"(exact {exact:.2f}).",
  ["44.89% of 1199.7 ≈ 45% of 1200 = 540", "251.9 ≈ 252", "?% of 800 = 540 − 252 = 288",
   "? = 288 × 100 ÷ 800 = 36"],
  short="?% of 800 means 8 × ?, so ? = 288 ÷ 8.", secs=50)

exact = math.sqrt(154.1 - math.sqrt(1295.8) * (3374.6 ** (1 / 3)) / 5.98)
nearest(exact, [8, 6, 10, 12], 8)
Q(T, "Root approximation", I,
  "Find the approximate value of ?:\n√1295.8 × ∛3374.6 ÷ 5.98 + ?² ≈ 154.1",
  "8", ["6", "10", "12"],
  "Nearest perfect square and perfect cube",
  f"√1295.8 ≈ √1296 = 36 and ∛3374.6 ≈ ∛3375 = 15. 36 × 15 ÷ 6 = 90, so ?² ≈ 154 − 90 = 64 and ? ≈ 8 "
  f"(exact {exact:.2f}).",
  ["√1295.8 ≈ 36 (36² = 1296)", "∛3374.6 ≈ 15 (15³ = 3375)", "36 × 15 ÷ 6 = 540 ÷ 6 = 90",
   "?² ≈ 154 − 90 = 64", "? ≈ 8"], secs=55)

exact = 7 / 9 * 1350.4 - 2 / 5 * 849.7 + 20.02 ** 2
nearest(exact, [1110, 1050, 1170, 990], 1110)
Q(T, "Mixed approximation", I,
  "What approximate value should replace ? in the expression\n7/9 of 1350.4 − 2/5 of 849.7 + 20.02² = ?",
  "1110", ["1050", "1170", "990"],
  "Round to multiples of the fraction's denominator",
  f"1350.4 ≈ 1350 (a multiple of 9), 849.7 ≈ 850 (a multiple of 5) and 20.02² ≈ 400. 7/9 of 1350 = 1050 and "
  f"2/5 of 850 = 340. So 1050 − 340 + 400 = 1110 (exact {exact:.2f}).",
  ["7/9 of 1350 = 150 × 7 = 1050", "2/5 of 850 = 170 × 2 = 340", "20.02² ≈ 20² = 400",
   "1050 − 340 + 400 = 1110"], secs=55)

exact = (28.03 ** 2 - 0.1598 * 400.3) / 1599.8 * 100
nearest(exact, [45, 40, 50, 55], 45)
Q(T, "Percentage approximation", I,
  "Find the approximate value of ? in: ?% of 1599.8 + 15.98% of 400.3 ≈ 28.03²",
  "45", ["40", "50", "55"],
  "Rounding a square and two percentage terms",
  f"28.03² ≈ 28² = 784 and 15.98% of 400.3 ≈ 16% of 400 = 64. So ?% of 1600 ≈ 720, i.e. 16 × ? = 720 and ? = 45 "
  f"(exact {exact:.2f}).",
  ["28.03² ≈ 784", "15.98% of 400.3 ≈ 16% of 400 = 64", "?% of 1600 ≈ 784 − 64 = 720",
   "? = 720 ÷ 16 = 45"], secs=55)

lhs = (math.sqrt(624.7) * 11.98 + 3.97 * 75.04) / 7.96
exact = lhs + 0.4487 * 159.6
nearest(exact, [147, 3, 161, 175], 147)
Q(T, "Mixed approximation", A,
  "What approximate value should come in place of the question mark (?)?\n"
  "(√624.7 × 11.98 + 3.97 × 75.04) ÷ 7.96 ≈ ? − 44.87% of 159.6",
  "147", ["3", "161", "175"],
  "Multi-term approximation with the unknown on the right side",
  f"√624.7 ≈ 25, so the bracket ≈ 25 × 12 + 4 × 75 = 300 + 300 = 600 and 600 ÷ 8 = 75. 44.87% of 159.6 ≈ 45% of "
  f"160 = 72. So ? − 72 ≈ 75 and ? ≈ 147 (exact {exact:.2f}).",
  ["√624.7 ≈ 25; 25 × 12 = 300", "3.97 × 75.04 ≈ 4 × 75 = 300", "(300 + 300) ÷ 8 = 75",
   "44.87% of 159.6 ≈ 45% of 160 = 72", "? = 75 + 72 = 147"],
  why="3 comes from subtracting 72 instead of adding it when moving the term across.", secs=80)

exact = math.sqrt(1650.2 - 0.3997 * 3749.6 - (15624.8 ** (1 / 3)) * math.sqrt(675.9) / 12.97)
nearest(exact, [10, 8, 12, 14], 10)
Q(T, "Root approximation", A,
  "Find the approximate value of ?:\n∛15624.8 × √675.9 ÷ 12.97 + ?² ≈ 1650.2 − 39.97% of 3749.6",
  "10", ["8", "12", "14"],
  "Cube root and square root approximation combined with percentages",
  f"∛15624.8 ≈ 25 (25³ = 15625) and √675.9 ≈ 26 (26² = 676), so the first term ≈ 25 × 26 ÷ 13 = 50. "
  f"The right side ≈ 1650 − 40% of 3750 = 1650 − 1500 = 150. So ?² ≈ 100 and ? ≈ 10 (exact {exact:.2f}).",
  ["∛15624.8 ≈ 25; √675.9 ≈ 26", "25 × 26 ÷ 13 = 50", "39.97% of 3749.6 ≈ 40% of 3750 = 1500",
   "1650 − 1500 = 150", "?² ≈ 150 − 50 = 100, so ? ≈ 10"], secs=90)

exact = 0.6248 * 1279.6 + 0.1429 * 2099.7 - 0.1667 * 1440.3
nearest(exact, [860, 940, 780, 1020], 860)
Q(T, "Percentage approximation", A,
  "What approximate value should replace ? in\n62.48% of 1279.6 + 14.29% of 2099.7 − 16.67% of 1440.3 ≈ ?",
  "860", ["940", "780", "1020"],
  "Fraction equivalents of percentages: 62.5% = 5/8, 14.28% ≈ 1/7, 16.67% = 1/6",
  f"Use 62.5% = 5/8, 14.29% ≈ 1/7 and 16.67% ≈ 1/6: 5/8 × 1280 = 800, 1/7 × 2100 = 300 and 1/6 × 1440 = 240. "
  f"800 + 300 − 240 = 860 (exact {exact:.2f}).",
  ["62.48% ≈ 5/8; 5/8 of 1280 = 800", "14.29% ≈ 1/7; 1/7 of 2100 = 300", "16.67% ≈ 1/6; 1/6 of 1440 = 240",
   "800 + 300 − 240 = 860"],
  short="Spot the fraction percentages first; every base then becomes a multiple of its denominator.", secs=75)

# ================================================================ Number Series (B4 I5 A4)
T = "Number Series"


def series_from(start, step, n):
    out = [start]
    for k in range(1, n):
        out.append(step(out[-1], k))
    return out


s = series_from(18, lambda t, k: t + 7 * k, 6)
assert s == [18, 25, 39, 60, 88, 123]
Q(T, "Pattern: differences", B,
  "What will come in place of the question mark (?) in the following series?\n18, 25, 39, 60, 88, ?",
  "123", ["116", "121", "125"],
  "Differences in an arithmetic progression (multiples of 7)",
  "The differences are 7, 14, 21, 28, i.e. multiples of 7. The next difference is 35, so the next term is "
  "88 + 35 = 123.",
  ["25 − 18 = 7, 39 − 25 = 14, 60 − 39 = 21, 88 − 60 = 28", "Differences are 7 × 1, 7 × 2, 7 × 3, 7 × 4",
   "Next difference = 7 × 5 = 35", "88 + 35 = 123"],
  why="116 repeats the last difference 28.", secs=30)

s = [n ** 3 + 2 for n in range(1, 7)]
assert s == [3, 10, 29, 66, 127, 218]
Q(T, "Pattern: squares and cubes", B, "Find the next term of the series: 3, 10, 29, 66, 127, ?",
  "218", ["216", "220", "214"],
  "Cubes plus a constant",
  "Each term is n³ + 2: 1 + 2, 8 + 2, 27 + 2, 64 + 2, 125 + 2. The next term is 6³ + 2 = 216 + 2 = 218.",
  ["3 = 1³ + 2, 10 = 2³ + 2, 29 = 3³ + 2", "66 = 4³ + 2, 127 = 5³ + 2", "Next = 6³ + 2 = 218"],
  why="216 is 6³ without the +2.", secs=35)

s = series_from(7, lambda t, k: 2 * t + 1, 6)
assert s == [7, 15, 31, 63, 127, 255]
Q(T, "Pattern: multiply-add", B, "Which number should replace the question mark?\n7, 15, 31, 63, 127, ?",
  "255", ["254", "253", "257"],
  "Multiply by 2 and add 1",
  "Each term is twice the previous term plus 1: 7 × 2 + 1 = 15, 15 × 2 + 1 = 31 and so on. "
  "So the next term is 127 × 2 + 1 = 255.",
  ["7 × 2 + 1 = 15", "15 × 2 + 1 = 31", "31 × 2 + 1 = 63", "63 × 2 + 1 = 127", "127 × 2 + 1 = 255"],
  short="The differences 8, 16, 32, 64 double, so the next difference is 128: 127 + 128 = 255.",
  why="254 doubles without adding 1.", secs=30)

s = series_from(5, lambda t, k: 2 * t + k, 6)
assert s == [5, 11, 24, 51, 106, 217]
Q(T, "Missing number series", B, "Find the missing number (?) in the series: 5, 11, 24, ?, 106, 217",
  "51", ["50", "52", "49"],
  "Multiply by 2 and add 1, 2, 3, ...",
  "The pattern is ×2 + 1, ×2 + 2, ×2 + 3, ... So the missing term is 24 × 2 + 3 = 51, and it checks forward: "
  "51 × 2 + 4 = 106 and 106 × 2 + 5 = 217.",
  ["5 × 2 + 1 = 11", "11 × 2 + 2 = 24", "24 × 2 + 3 = 51", "Check: 51 × 2 + 4 = 106; 106 × 2 + 5 = 217"],
  why="52 uses +4 at this step, which then fails the check 52 × 2 + 4 ≠ 106.", secs=40)

s = series_from(11, lambda t, k: t + k * (k + 1), 6)
assert s == [11, 13, 19, 31, 51, 81]
Q(T, "Pattern: differences", I, "What will come in place of ? in the series 11, 13, 19, 31, 51, ?",
  "81", ["79", "83", "71"],
  "Differences of the form n(n + 1)",
  "The differences are 2, 6, 12, 20, which are 1×2, 2×3, 3×4, 4×5. The next difference is 5×6 = 30, so the "
  "next term is 51 + 30 = 81.",
  ["Differences: 2, 6, 12, 20", "These are 1×2, 2×3, 3×4, 4×5 (second differences 4, 6, 8)",
   "Next difference = 5×6 = 30", "51 + 30 = 81"],
  why="71 uses a difference of 20 again; 79 and 83 use second differences of 8 and 12 instead of 10.", secs=45)

s = series_from(2, lambda t, k: t + (k + 1) ** 2, 6)
assert s == [2, 6, 15, 31, 56, 92]
Q(T, "Pattern: squares and cubes", I, "Find the next number in the series: 2, 6, 15, 31, 56, ?",
  "92", ["87", "90", "96"],
  "Differences are consecutive perfect squares",
  "The differences are 4, 9, 16, 25, i.e. 2², 3², 4², 5². The next difference is 6² = 36, giving 56 + 36 = 92.",
  ["6 − 2 = 4 = 2²", "15 − 6 = 9 = 3²", "31 − 15 = 16 = 4²", "56 − 31 = 25 = 5²", "56 + 6² = 56 + 36 = 92"],
  why="87 adds 31 (treating the differences as an arithmetic progression with common difference 6).", secs=45)

s = series_from(5, lambda t, k: t * k - k, 6)
assert s == [5, 4, 6, 15, 56, 275]
Q(T, "Pattern: multiply-add", I, "What should come in place of the question mark?\n5, 4, 6, 15, 56, ?",
  "275", ["280", "270", "285"],
  "Multiply by n and subtract n",
  "The terms follow ×1 − 1, ×2 − 2, ×3 − 3, ×4 − 4. The next step is ×5 − 5: 56 × 5 − 5 = 275.",
  ["5 × 1 − 1 = 4", "4 × 2 − 2 = 6", "6 × 3 − 3 = 15", "15 × 4 − 4 = 56", "56 × 5 − 5 = 280 − 5 = 275"],
  why="280 forgets the −5; 285 adds 5 instead of subtracting it.", secs=50)

s = series_from(F(1250), lambda t, k: t * F(2 * k, 10), 6)
assert s == [1250, 250, 100, 60, 48, 48]
Q(T, "Missing number series", I, "Find the missing term: 1250, 250, ?, 60, 48, 48",
  "100", ["125", "80", "50"],
  "Multipliers increasing by 0.2: ×0.2, ×0.4, ×0.6, ×0.8, ×1",
  "1250 × 0.2 = 250, so the multipliers are 0.2, 0.4, 0.6, ... The missing term is 250 × 0.4 = 100, and then "
  "100 × 0.6 = 60, 60 × 0.8 = 48 and 48 × 1 = 48 confirm it.",
  ["1250 × 0.2 = 250", "250 × 0.4 = 100", "Check: 100 × 0.6 = 60, 60 × 0.8 = 48, 48 × 1.0 = 48"],
  why="125 halves 250 (assuming ÷2); 50 repeats ×0.2. Neither continues to 60 and 48.", secs=55)

s = [4]
for k in range(6):
    s.append(s[-1] * 3 if k % 2 == 0 else s[-1] - 4)
assert s == [4, 12, 8, 24, 20, 60, 56]
Q(T, "Pattern: multiply-add", I, "Which number will replace the question mark?\n4, 12, 8, 24, 20, 60, ?",
  "56", ["180", "64", "52"],
  "Alternating operations: ×3, then −4",
  "The operations alternate: ×3, −4, ×3, −4, ×3. The next operation is −4, so the answer is 60 − 4 = 56.",
  ["4 × 3 = 12; 12 − 4 = 8", "8 × 3 = 24; 24 − 4 = 20", "20 × 3 = 60", "Next: 60 − 4 = 56"],
  why="180 applies ×3 twice in a row; 64 adds 4 instead of subtracting.", secs=45)

s = series_from(9, lambda t, k: t + (k + 1) ** 3, 6)
assert s == [9, 17, 44, 108, 233, 449]
Q(T, "Pattern: squares and cubes", A, "What will come in place of the question mark (?)?\n9, 17, 44, 108, 233, ?",
  "449", ["441", "358", "457"],
  "Differences are consecutive cubes",
  "The differences 8, 27, 64, 125 are 2³, 3³, 4³, 5³. The next difference is 6³ = 216, so 233 + 216 = 449.",
  ["17 − 9 = 8 = 2³", "44 − 17 = 27 = 3³", "108 − 44 = 64 = 4³", "233 − 108 = 125 = 5³",
   "233 + 6³ = 233 + 216 = 449"],
  why="358 repeats 5³; 441 adds 6³ − 8 by misreading the start.", secs=60)

s = [7, 9, 16, 34, 70, 132]
d1 = [b - a for a, b in zip(s, s[1:])]
d2 = [b - a for a, b in zip(d1, d1[1:])]
d3 = [b - a for a, b in zip(d2, d2[1:])]
assert d1 == [2, 7, 18, 36, 62] and d2 == [5, 11, 18, 26] and d3 == [6, 7, 8]
nxt = s[-1] + d1[-1] + d2[-1] + d3[-1] + 1
assert nxt == 229
Q(T, "Pattern: differences", A, "Find the next term of the series: 7, 9, 16, 34, 70, 132, ?",
  "229", ["225", "194", "219"],
  "Three levels of differences",
  "First differences: 2, 7, 18, 36, 62. Second differences: 5, 11, 18, 26. Third differences: 6, 7, 8, so the next "
  "third difference is 9. Then the next second difference is 26 + 9 = 35, the next first difference is 62 + 35 = 97 "
  "and the next term is 132 + 97 = 229.",
  ["First differences: 2, 7, 18, 36, 62", "Second differences: 5, 11, 18, 26", "Third differences: 6, 7, 8 → next 9",
   "Next second difference = 26 + 9 = 35", "Next first difference = 62 + 35 = 97", "132 + 97 = 229"],
  why="194 repeats the difference 62; 225 stops at the second level and assumes 26 + 8 = 34.", secs=90)

s = series_from(F(16), lambda t, k: t * F(k, 2), 7)
assert s == [16, 8, 8, 12, 24, 60, 180]
Q(T, "Pattern: multiply-add", A, "What will come in place of ? in the series 16, 8, 8, 12, 24, 60, ?",
  "180", ["150", "120", "210"],
  "Multipliers increasing by 0.5",
  "16 × 0.5 = 8, 8 × 1 = 8, 8 × 1.5 = 12, 12 × 2 = 24, 24 × 2.5 = 60. The next multiplier is 3: 60 × 3 = 180.",
  ["Multipliers: 0.5, 1, 1.5, 2, 2.5", "Next multiplier = 3", "60 × 3 = 180"],
  why="150 repeats ×2.5; 120 uses ×2.", secs=60)

s = series_from(3, lambda t, k: t * (k + 1) + k, 6)
assert s == [3, 7, 23, 95, 479, 2879]
Q(T, "Missing number series", A, "Find the missing number: 3, 7, 23, ?, 479, 2879",
  "95", ["92", "96", "99"],
  "Multiply by 2, 3, 4, ... and add 1, 2, 3, ...",
  "The pattern is ×2 + 1, ×3 + 2, ×4 + 3, ×5 + 4, ×6 + 5. The missing term is 23 × 4 + 3 = 95; checking, "
  "95 × 5 + 4 = 479 and 479 × 6 + 5 = 2879.",
  ["3 × 2 + 1 = 7", "7 × 3 + 2 = 23", "23 × 4 + 3 = 95", "Check: 95 × 5 + 4 = 479", "Check: 479 × 6 + 5 = 2879"],
  why="92 uses ×4 with no addition; 96 uses +4 with ×4, which fails the check at 479.", secs=75)

# ================================================================ Wrong Number Series (B2 I2 A2)
T = "Wrong Number Series"


def wrong_series(correct, shown):
    diff = [i for i, (a, b) in enumerate(zip(correct, shown)) if a != b]
    assert len(diff) == 1, (correct, shown)
    return shown[diff[0]], correct[diff[0]]


def series_text(seq):
    return ", ".join(N(x) for x in seq)


good = series_from(5, lambda t, k: 2 * t - 1, 7)
shown = [5, 9, 17, 33, 65, 128, 257]
w, c = wrong_series(good, shown)
assert (w, c) == (128, 129)
Q(T, "Find the wrong term", B, f"Find the wrong number in the series:\n{series_text(shown)}",
  "128", ["33", "65", "257"],
  "Multiply by 2 and subtract 1",
  "Each term should be twice the previous term minus 1: 5, 9, 17, 33, 65, 129, 257. The sixth term should be "
  "65 × 2 − 1 = 129, not 128.",
  ["5 × 2 − 1 = 9", "9 × 2 − 1 = 17", "17 × 2 − 1 = 33", "33 × 2 − 1 = 65", "65 × 2 − 1 = 129 ≠ 128",
   "129 × 2 − 1 = 257, so the last term fits the correct value"],
  short="Differences should double: 4, 8, 16, 32, 64, 128. 65 → 128 is a difference of 63.", secs=35)

good = [n * n + 1 for n in range(1, 8)]
shown = [2, 5, 10, 17, 26, 38, 50]
w, c = wrong_series(good, shown)
assert (w, c) == (38, 37)
Q(T, "Find the wrong term", B, f"One number in the following series is wrong. Find it.\n{series_text(shown)}",
  "38", ["17", "26", "50"],
  "n² + 1",
  "The terms are 1² + 1, 2² + 1, 3² + 1, ... The sixth term should be 6² + 1 = 37, not 38.",
  ["2 = 1² + 1, 5 = 2² + 1, 10 = 3² + 1", "17 = 4² + 1, 26 = 5² + 1", "Sixth term should be 6² + 1 = 37",
   "50 = 7² + 1 fits"],
  short="Differences should be odd numbers 3, 5, 7, 9, 11, 13; 26 → 38 gives 12.", secs=35)

good = series_from(4, lambda t, k: t * k + k * k, 7)
shown = [4, 5, 14, 53, 220, 1125, 6786]
w, c = wrong_series(good, shown)
assert good == [4, 5, 14, 51, 220, 1125, 6786] and (w, c) == (53, 51)
Q(T, "Find the wrong term", I, f"Identify the wrong term in the series:\n{series_text(shown)}",
  "53", ["14", "220", "1,125"],
  "Multiply by n and add n²",
  "The rule is ×1 + 1, ×2 + 4, ×3 + 9, ×4 + 16, ×5 + 25, ×6 + 36. The fourth term should be 14 × 3 + 9 = 51, and "
  "51 × 4 + 16 = 220 confirms that 53 is wrong.",
  ["4 × 1 + 1 = 5", "5 × 2 + 4 = 14", "14 × 3 + 9 = 51 (series shows 53)", "51 × 4 + 16 = 220",
   "220 × 5 + 25 = 1125", "1125 × 6 + 36 = 6786"],
  why="220 looks off if you continue from 53 (53 × 4 + 16 = 228), but it is consistent with the correct value 51.",
  secs=60)

good = series_from(4320, lambda t, k: t // (k + 1), 6)
shown = [4320, 2160, 740, 180, 36, 6]
w, c = wrong_series(good, shown)
assert good == [4320, 2160, 720, 180, 36, 6] and (w, c) == (740, 720)
Q(T, "Find the wrong term", I, f"Which number in the series below does not fit the pattern?\n{series_text(shown)}",
  "740", ["2,160", "180", "36"],
  "Divide by 2, 3, 4, 5, 6",
  "4320 ÷ 2 = 2160, 2160 ÷ 3 = 720, 720 ÷ 4 = 180, 180 ÷ 5 = 36 and 36 ÷ 6 = 6. The third term should be 720, "
  "so 740 is wrong.",
  ["4320 ÷ 2 = 2160", "2160 ÷ 3 = 720 (series shows 740)", "720 ÷ 4 = 180", "180 ÷ 5 = 36", "36 ÷ 6 = 6"],
  why="180 seems wrong if you divide 740 by 4 (185), but it fits the correct value 720.", secs=50)

good = series_from(6, lambda t, k: t + (2 * k - 1) ** 2, 7)
shown = [6, 7, 16, 41, 90, 172, 292]
w, c = wrong_series(good, shown)
assert good == [6, 7, 16, 41, 90, 171, 292] and (w, c) == (172, 171)
Q(T, "Find the wrong term", A, f"Find the wrong number in the series:\n{series_text(shown)}",
  "172", ["41", "90", "292"],
  "Differences are squares of consecutive odd numbers",
  "The differences should be 1², 3², 5², 7², 9², 11², i.e. 1, 9, 25, 49, 81, 121. From 90 the next term should be "
  "90 + 81 = 171, and 171 + 121 = 292. So 172 is wrong.",
  ["7 − 6 = 1 = 1²", "16 − 7 = 9 = 3²", "41 − 16 = 25 = 5²", "90 − 41 = 49 = 7²",
   "90 + 9² = 171 (series shows 172)", "171 + 11² = 292"],
  why="292 looks wrong against 172 (difference 120), but it fits 171 + 121.", secs=75)

good = series_from(3, lambda t, k: t * k + (k + 1), 7)
shown = [3, 5, 13, 45, 177, 891, 5353]
w, c = wrong_series(good, shown)
assert good == [3, 5, 13, 43, 177, 891, 5353] and (w, c) == (45, 43)
Q(T, "Find the wrong term", A, f"Exactly one term of this series is incorrect. Which one?\n{series_text(shown)}",
  "45", ["13", "177", "891"],
  "Multiply by 1, 2, 3, ... and add 2, 3, 4, ...",
  "The rule is ×1 + 2, ×2 + 3, ×3 + 4, ×4 + 5, ×5 + 6, ×6 + 7. The fourth term should be 13 × 3 + 4 = 43; "
  "then 43 × 4 + 5 = 177 confirms that 45 is the wrong term.",
  ["3 × 1 + 2 = 5", "5 × 2 + 3 = 13", "13 × 3 + 4 = 43 (series shows 45)", "43 × 4 + 5 = 177",
   "177 × 5 + 6 = 891", "891 × 6 + 7 = 5353"],
  why="177 looks wrong if you continue from 45 (45 × 4 + 5 = 185), but it fits the correct value 43.", secs=80)

# ================================================================ Quadratic Equations (B3 I4 A3)
T = "Quadratic Equations"
REL = {">": "x > y", ">=": "x ≥ y", "<": "x < y", "<=": "x ≤ y",
       "cbe": "x = y or the relationship cannot be established"}


def relation(xs, ys):
    pairs = [(x, y) for x in xs for y in ys]
    if all(x == y for x, y in pairs):
        return "cbe"
    for sym, test in ((">", lambda x, y: x > y), ("<", lambda x, y: x < y), (">=", lambda x, y: x >= y),
                      ("<=", lambda x, y: x <= y)):
        if all(test(x, y) for x, y in pairs):
            return sym
    return "cbe"


_TESTS = {">": lambda x, y: x > y, "<": lambda x, y: x < y, ">=": lambda x, y: x >= y, "<=": lambda x, y: x <= y}


def no_true_distractor(xs, ys, syms):
    """No wrong relation may hold for every pair (e.g. x ≥ y when the answer is x > y, or when x = y)."""
    for s in syms:
        assert not all(_TESTS[s](x, y) for x in xs for y in ys), f"distractor {s} is also true"


def roots_check(a, b, c, roots):
    for r in roots:
        assert a * r * r + b * r + c == 0, (a, b, c, r)


def qe(sub, diff, pre, eq1, eq2, xs, ys, expect, wrong_syms, concept, expl, steps, short=None, why=None, secs=None):
    got = relation(xs, ys)
    assert got == expect, (eq1, eq2, got)
    assert "cbe" not in wrong_syms and expect not in wrong_syms and len(set(wrong_syms)) == 2
    if expect == "cbe":
        third = next(s for s in ("<", ">", "<=", ">=") if s not in wrong_syms)
        wrong = [REL[wrong_syms[0]], REL[wrong_syms[1]], REL[third]]
        no_true_distractor(xs, ys, [*wrong_syms, third])
    else:
        wrong = [REL[wrong_syms[0]], REL["cbe"], REL[wrong_syms[1]]]
        no_true_distractor(xs, ys, wrong_syms)
    Q(T, sub, diff, f"{pre}\nI. {eq1}\nII. {eq2}", REL[expect], wrong, concept, expl, steps, short, why, secs)


xs, ys = [F(5), F(6)], [F(3), F(4)]
roots_check(1, -11, 30, xs), roots_check(1, -7, 12, ys)
qe("Relation between roots", B,
   "In the following question, two equations I and II are given. Solve both and choose the correct relation between "
   "x and y.", "x² − 11x + 30 = 0", "y² − 7y + 12 = 0", xs, ys, ">", ["<=", "<"],
   "Factorising by splitting the middle term; comparing all root pairs",
   "x = 5 or 6 and y = 3 or 4. The smallest x (5) is greater than the largest y (4), so x > y.",
   ["I: x² − 5x − 6x + 30 = (x − 5)(x − 6) = 0 ⇒ x = 5, 6", "II: y² − 3y − 4y + 12 = (y − 3)(y − 4) = 0 ⇒ y = 3, 4",
    "min x = 5 > max y = 4", "So x > y"],
   short="Both equations have signs (+, −, +), so all roots are positive; compare min x with max y.", secs=35)

xs, ys = [F(-4), F(-5)], [F(-2), F(-3)]
roots_check(1, 9, 20, xs), roots_check(1, 5, 6, ys)
qe("Relation between roots", B,
   "Solve the given equations and mark the relation that holds between x and y.",
   "x² + 9x + 20 = 0", "y² + 5y + 6 = 0", xs, ys, "<", [">=", ">"],
   "Roots of quadratics with all positive coefficients are negative",
   "x = −4 or −5 and y = −2 or −3. The largest x (−4) is smaller than the smallest y (−3), so x < y.",
   ["I: (x + 4)(x + 5) = 0 ⇒ x = −4, −5", "II: (y + 2)(y + 3) = 0 ⇒ y = −2, −3",
    "max x = −4 < min y = −3", "So x < y"],
   why="x > y comes from comparing the sizes 4, 5 and 2, 3 and forgetting the negative signs.", secs=35)

xs, ys = [F(6), F(7)], [F(6)]
roots_check(1, -13, 42, xs), roots_check(1, -12, 36, ys)
qe("Relation between roots", B,
   "Two equations in x and y are given below. Find their roots and select the correct option.",
   "x² − 13x + 42 = 0", "y² − 12y + 36 = 0", xs, ys, ">=", [">", "<="],
   "Perfect-square quadratic gives a repeated root",
   "x = 6 or 7, and y = 6 (a repeated root). x is never less than y, and x = y = 6 is possible, so x ≥ y.",
   ["I: (x − 6)(x − 7) = 0 ⇒ x = 6, 7", "II: (y − 6)² = 0 ⇒ y = 6",
    "Pairs: (6, 6) equal; (7, 6) x > y", "So x ≥ y"],
   why="x > y ignores the case x = 6 = y.", secs=40)

xs, ys = [F(3), F(5, 2)], [F(2), F(8, 3)]
roots_check(2, -11, 15, xs), roots_check(3, -14, 16, ys)
qe("Relation between roots", I,
   "Compare the roots of the following pair of equations and choose the relation between x and y that is always "
   "true.", "2x² − 11x + 15 = 0", "3y² − 14y + 16 = 0", xs, ys, "cbe", [">", ">="],
   "When root ranges overlap, no single relation holds",
   "x = 3 or 2.5 and y = 2 or 2.67. x = 2.5 is less than y = 2.67 but greater than y = 2, so no single relation "
   "holds.",
   ["I: 2x² − 6x − 5x + 15 = (x − 3)(2x − 5) = 0 ⇒ x = 3, 2.5",
    "II: 3y² − 6y − 8y + 16 = (y − 2)(3y − 8) = 0 ⇒ y = 2, 2.67",
    "x = 2.5, y = 2.67 gives x < y", "x = 3, y = 2 gives x > y", "Relationship cannot be established"],
   why="x > y or x ≥ y looks right if you compare only the larger roots (3 and 2.67).", secs=55)

xs, ys = [F(-1, 2), F(-1, 3)], [F(-1, 3), F(-1, 5)]
roots_check(6, 5, 1, xs), roots_check(15, 8, 1, ys)
qe("Relation between roots", I,
   "Each question below has two equations. Solve them and decide how x is related to y.",
   "6x² + 5x + 1 = 0", "15y² + 8y + 1 = 0", xs, ys, "<=", ["<", ">="],
   "Negative fractional roots; −1/2 < −1/3 < −1/5",
   "x = −1/2 or −1/3 and y = −1/3 or −1/5. The largest x (−1/3) equals the smallest y (−1/3), so x ≤ y.",
   ["I: 6x² + 3x + 2x + 1 = (2x + 1)(3x + 1) = 0 ⇒ x = −0.5, −0.33",
    "II: 15y² + 5y + 3y + 1 = (3y + 1)(5y + 1) = 0 ⇒ y = −0.33, −0.2",
    "max x = −1/3 = min y", "So x ≤ y"],
   why="x < y misses the common root −1/3.", secs=55)

xs, ys = [F(4), F(-4)], [F(4), F(5)]
roots_check(1, 0, -16, xs), roots_check(1, -9, 20, ys)
qe("Linear vs quadratic", I,
   "Find the values of x and y from the equations below and choose the correct relationship.",
   "x² − 16 = 0", "y² − 9y + 20 = 0", xs, ys, "<=", ["<", ">"],
   "A pure quadratic x² = k has roots ±√k",
   "x = 4 or −4 and y = 4 or 5. Every x is at most 4 and every y is at least 4, with equality at 4, so x ≤ y.",
   ["I: x² = 16 ⇒ x = +4 or −4", "II: (y − 4)(y − 5) = 0 ⇒ y = 4, 5",
    "max x = 4 = min y", "So x ≤ y"],
   why="x < y misses the pair x = y = 4; x > y comes from forgetting the root x = −4 and misreading y.", secs=50)

x, y = F(6), F(8)
assert 3 * x + 2 * y == 34 and 5 * x - 3 * y == 6
qe("Linear vs quadratic", I,
   "Two linear equations in x and y are given. Solve them and choose the correct relationship.",
   "3x + 2y = 34", "5x − 3y = 6", [x], [y], "<", [">=", ">"],
   "Solving simultaneous linear equations by elimination",
   "Multiply I by 3 and II by 2 and add: 19x = 114, so x = 6. Then 2y = 34 − 18 = 16 and y = 8. So x < y.",
   ["I × 3: 9x + 6y = 102", "II × 2: 10x − 6y = 12", "Adding: 19x = 114 ⇒ x = 6",
    "From I: 2y = 34 − 18 = 16 ⇒ y = 8", "6 < 8, so x < y"], secs=60)

xs = [2 * math.sqrt(5), 3 * math.sqrt(5)]
ys = [math.sqrt(2), 2 * math.sqrt(2)]
for r in xs:
    assert near(r * r - 5 * math.sqrt(5) * r + 30, 0, 1e-9)
for r in ys:
    assert near(r * r - 3 * math.sqrt(2) * r + 4, 0, 1e-9)
qe("Relation between roots", A,
   "In the question below, solve equations I and II and identify the correct relation between x and y.",
   "x² − 5√5x + 30 = 0", "y² − 3√2y + 4 = 0", xs, ys, ">", ["<=", "<"],
   "Factorising quadratics with surd coefficients (product and sum of roots)",
   "For I, find two numbers with sum 5√5 and product 30: 2√5 and 3√5, so x ≈ 4.47 or 6.71. For II, the numbers "
   "with sum 3√2 and product 4 are √2 and 2√2, so y ≈ 1.41 or 2.83. Every x is greater than every y.",
   ["I: 2√5 + 3√5 = 5√5 and 2√5 × 3√5 = 30 ⇒ x = 2√5 ≈ 4.47 or 3√5 ≈ 6.71",
    "II: √2 + 2√2 = 3√2 and √2 × 2√2 = 4 ⇒ y = √2 ≈ 1.41 or 2√2 ≈ 2.83",
    "min x ≈ 4.47 > max y ≈ 2.83", "So x > y"],
   short="Compare squares instead of roots: min x² = 20, max y² = 8, both positive, so x > y.", secs=90)

xs, ys = [F(9, 4), F(2)], [F(3, 2), F(2)]
roots_check(4, -17, 18, xs), roots_check(2, -7, 6, ys)
qe("Relation between roots", A,
   "Solve both equations and choose the option that correctly relates x and y.",
   "4x² − 17x + 18 = 0", "2y² − 7y + 6 = 0", xs, ys, ">=", [">", "<="],
   "Factorising with a ≠ 1 and spotting a common root",
   "x = 2.25 or 2 and y = 1.5 or 2. The smallest x (2) equals the largest y (2), so x ≥ y.",
   ["I: 4x² − 8x − 9x + 18 = 4x(x − 2) − 9(x − 2) = (x − 2)(4x − 9) = 0 ⇒ x = 2, 2.25",
    "II: 2y² − 4y − 3y + 6 = 2y(y − 2) − 3(y − 2) = (y − 2)(2y − 3) = 0 ⇒ y = 2, 1.5",
    "Pairs: (2, 2) equal; (2, 1.5), (2.25, 2), (2.25, 1.5) all x > y", "So x ≥ y"],
   why="x > y misses the shared root 2.", secs=80)

xs, ys = [F(4), F(6)], [F(6), F(7)]
for r in xs:
    assert (r - 3) ** 2 == 4 * r - 15
for r in ys:
    assert r * (r - 13) == -42
qe("Linear vs quadratic", A,
   "Rearrange each equation into standard form, solve, and choose the correct relation between x and y.",
   "(x − 3)² = 4x − 15", "y(y − 13) = −42", xs, ys, "<=", ["<", ">="],
   "Rewriting non-standard forms as ax² + bx + c = 0 before factorising",
   "I becomes x² − 10x + 24 = 0, so x = 4 or 6. II becomes y² − 13y + 42 = 0, so y = 6 or 7. The largest x equals "
   "the smallest y (6), so x ≤ y.",
   ["I: x² − 6x + 9 = 4x − 15 ⇒ x² − 10x + 24 = 0 ⇒ (x − 4)(x − 6) = 0 ⇒ x = 4, 6",
    "II: y² − 13y + 42 = 0 ⇒ (y − 6)(y − 7) = 0 ⇒ y = 6, 7", "max x = 6 = min y", "So x ≤ y"],
   why="x < y misses the pair x = y = 6; x ≥ y comes from a sign error when expanding (x − 3)².", secs=90)

# ================================================================ Number System (B1 I2 A1)
T = "Number System"
u = (pow(7, 95, 10) * pow(3, 58, 10)) % 10
assert pow(7, 95, 10) == 3 and pow(3, 58, 10) == 9 and u == 7 == (7 ** 95 * 3 ** 58) % 10
Q(T, "Unit digit", B, "What is the unit digit of 7⁹⁵ × 3⁵⁸?",
  "7", ["1", "9", "3"],
  "Cyclicity of unit digits: powers of 7 and 3 repeat in cycles of 4",
  "Unit digits of powers of 7 cycle 7, 9, 3, 1 and those of 3 cycle 3, 9, 7, 1. 95 leaves remainder 3 on division by "
  "4, so 7⁹⁵ ends in 3. 58 leaves remainder 2, so 3⁵⁸ ends in 9. 3 × 9 = 27, so the unit digit is 7.",
  ["Cycle of 7: 7, 9, 3, 1; 95 ÷ 4 leaves 3 ⇒ unit digit of 7⁹⁵ = 3",
   "Cycle of 3: 3, 9, 7, 1; 58 ÷ 4 leaves 2 ⇒ unit digit of 3⁵⁸ = 9", "3 × 9 = 27 ⇒ unit digit 7"],
  why="1 uses remainder 0 for 95; 9 and 3 are the unit digits of only one of the two factors.", secs=35)

L = math.lcm(12, 18, 30)
times = [t for t in range(0, 12 * 60 + 1) if t % L == 0]
assert L == 180 and len(times) == 5
Q(T, "HCF and LCM", I,
  "Three alarm systems in a bank vault beep every 12, 18 and 30 minutes respectively. They beep together at 8:00 AM. "
  "How many times will they beep together from 8:00 AM to 8:00 PM, both times included?",
  "5", ["4", "9", "6"],
  "Events coincide at multiples of the LCM of their intervals",
  "LCM(12, 18, 30) = 180 minutes = 3 hours, so they beep together at 8 AM, 11 AM, 2 PM, 5 PM and 8 PM: 5 times.",
  ["12 = 2² × 3, 18 = 2 × 3², 30 = 2 × 3 × 5", "LCM = 2² × 3² × 5 = 180 minutes = 3 hours",
   "8 AM to 8 PM = 12 hours ⇒ 12 ÷ 3 = 4 intervals", "Including the start: 4 + 1 = 5 times"],
  why="4 forgets to count 8:00 AM; 9 uses 90 minutes as the LCM (dropping one factor of 2).", secs=50)

assert all((357 * k + 39) % 17 == 5 for k in range(1, 50)) and 357 % 17 == 0
Q(T, "Remainders", I,
  "A number leaves a remainder of 39 when divided by 357. What remainder will it leave when divided by 17?",
  "5", ["22", "39", "12"],
  "If the first divisor is a multiple of the second, reduce the first remainder by the second divisor",
  "357 = 17 × 21, so the number is 357k + 39 and 357k is divisible by 17. The remainder is 39 mod 17 = 5.",
  ["Number = 357k + 39", "357 = 17 × 21, so 357k leaves remainder 0 on division by 17",
   "39 = 17 × 2 + 5", "Remainder = 5"],
  why="22 subtracts 17 only once; 39 cannot be a remainder for divisor 17.", secs=45)

L = math.lcm(6, 9, 15, 18)
cands = [n for n in range(5, 2000) if all(n % d == 4 for d in (6, 9, 15, 18)) and n % 7 == 0]
assert L == 90 and cands[0] == 364
Q(T, "HCF and LCM", A,
  "Find the least number which leaves a remainder of 4 when divided by 6, 9, 15 or 18, but is exactly divisible by 7.",
  "364", ["94", "184", "454"],
  "Numbers leaving the same remainder r are LCM × k + r; then apply the extra divisibility condition",
  "LCM(6, 9, 15, 18) = 90, so the number is 90k + 4. 90k + 4 ≡ 6k + 4 (mod 7), and this is 0 when k = 4. "
  "So the number is 90 × 4 + 4 = 364 = 7 × 52.",
  ["LCM(6, 9, 15, 18) = 90 ⇒ number = 90k + 4", "Try k = 1: 94 (94 ÷ 7 leaves 3)", "k = 2: 184 (leaves 2)",
   "k = 3: 274 (leaves 1)", "k = 4: 364 = 7 × 52 ✓"],
  short="90 ≡ 6 ≡ −1 (mod 7), so 90k + 4 ≡ 4 − k; this is 0 at k = 4.",
  why="94 is just LCM + 4 and is not divisible by 7; 184 and 454 also leave non-zero remainders on division by 7.",
  secs=90)

# ================================================================ Percentage (B2 I3 A2)
T = "Percentage"
v = 2400 * F(65, 100) * F(60, 100)
assert v == 936 and 2400 * F(65, 100) * F(40, 100) == 624 and 2400 * F(25, 100) == 600
Q(T, "Basic percentage", B,
  "A bank branch has 2,400 savings accounts. 35% of them are zero-balance accounts. Of the remaining accounts, 40% "
  "belong to senior citizens. How many accounts are neither zero-balance nor held by senior citizens?",
  "936", ["624", "600", "1,440"],
  "Successive percentages are applied to the remaining amount, not to the original total",
  "Non-zero-balance accounts = 65% of 2,400 = 1,560. Of these, 60% are not senior citizens: 60% of 1,560 = 936.",
  ["Zero-balance = 35% of 2,400 = 840; remaining = 1,560", "Senior citizens = 40% of 1,560 = 624",
   "Required = 1,560 − 624 = 936"],
  short="2,400 × 0.65 × 0.60 = 936.",
  why="624 is the senior-citizen count; 600 subtracts 35% and 40% from 100% directly; 1,440 takes 40% of 2,400.",
  secs=40)

v = 450 * F(120, 100) * F(85, 100)
assert v == 459 and 450 * F(105, 100) == F(4725, 10) and 450 * F(98, 100) == 441
Q(T, "Successive change", B,
  "The price of a share rose by 20% on Monday and fell by 15% on Tuesday. If the price was ₹450 before Monday, "
  "what was it at the end of Tuesday?",
  "₹459", ["₹472.5", "₹441", "₹450"],
  "Successive percentage change: multiply the factors",
  "After the rise the price is 450 × 1.2 = ₹540. A 15% fall is taken on ₹540: 540 × 0.85 = ₹459.",
  ["After +20%: 450 × 1.20 = 540", "After −15%: 540 × 0.85 = 459"],
  short="Net change = 20 − 15 + (20 × −15)/100 = +2%; 450 × 1.02 = 459.",
  why="₹472.5 assumes a net change of +5% (20 − 15); ₹441 takes the net change as −2%.", secs=35)

inc, exp_ = F(100), F(80)
s0 = inc - exp_
s1 = inc * F(125, 100) - exp_ * F(115, 100)
pct = (s1 - s0) / s0 * 100
assert s0 == 20 and s1 == 33 and pct == 65
Q(T, "Income and expenditure", I,
  "Meera saves 20% of her income. Her income increases by 25% and her expenditure increases by 15%. By what percent "
  "do her savings increase?",
  "65%", ["10%", "33%", "40%"],
  "Income = Expenditure + Savings; assume income = 100",
  "Let income be 100: expenditure 80, savings 20. New income 125, new expenditure 92, new savings 33. "
  "Savings rise by 13 on 20, i.e. 65%.",
  ["Income 100 ⇒ expenditure 80, savings 20", "New income = 125; new expenditure = 80 × 1.15 = 92",
   "New savings = 125 − 92 = 33", "Increase = 13; 13 ÷ 20 × 100 = 65%"],
  why="10% subtracts the two percentages; 33% reads the new savings amount as the percentage increase.", secs=55)

v = F(510300) / F(9, 10) ** 3
assert v == 700000 and F(510300) / F(7, 10) == 729000 and F(510300) * F(13, 10) == 663390
assert F(510300) / F(3, 4) == 680400
Q(T, "Population and depreciation", I,
  "A machine loses 10% of its value every year (on its value at the beginning of that year). Its value now is "
  "₹5,10,300. What was its value 3 years ago?",
  "₹7,00,000", ["₹7,29,000", "₹6,63,390", "₹6,80,400"],
  "Depreciation is compound: value after n years = original × (1 − r/100)ⁿ",
  "Value now = original × 0.9³ = original × 0.729. So the original = 5,10,300 ÷ 0.729 = ₹7,00,000.",
  ["Value after 3 years = V × (0.9)³ = 0.729V", "0.729V = 5,10,300", "V = 5,10,300 ÷ 0.729 = 7,00,000"],
  short="0.729 = 729/1000; 5,10,300 ÷ 729 = 700, so V = 700 × 1000.",
  why="₹7,29,000 treats depreciation as simple (30% in total); ₹6,63,390 adds 30% to today's value.", secs=60)

N_ = F(5244) / (F(92, 100) * F(95, 100) * F(20, 100))
assert N_ == 30000
assert F(5244) / F(20, 100) == 26220 and F(5244) / (F(20, 100) * F(92, 100)) == 28500
assert F(5244) / (F(20, 100) * F(95, 100)) == 27600
Q(T, "Basic percentage", I,
  "In an election between two candidates, 8% of the registered voters did not vote and 5% of the votes cast were "
  "invalid. The winner got 60% of the valid votes and won by 5,244 votes. How many voters were registered?",
  "30,000", ["26,220", "28,500", "27,600"],
  "Chain of percentages from registered voters to valid votes; winning margin as a percentage of valid votes",
  "Valid votes = 92% × 95% = 87.4% of registered voters. The margin is 60% − 40% = 20% of valid votes, i.e. "
  "17.48% of registered voters. 5,244 ÷ 0.1748 = 30,000.",
  ["Votes cast = 92% of N", "Valid votes = 95% of 92% of N = 0.874N", "Margin = (60 − 40)% of valid = 0.2 × 0.874N = 0.1748N",
   "0.1748N = 5,244 ⇒ N = 30,000"],
  why="26,220 is the number of valid votes; 28,500 ignores the invalid votes; 27,600 ignores the voters who did not "
      "vote.", secs=75)

factor = F(120, 100) * F(75, 100) * F(130, 100)
v = F(3570) / (factor - 1)
assert factor == F(117, 100) and v == 21000 and F(3570) / F(25, 100) == 14280
Q(T, "Population and depreciation", A,
  "The population of a town increased by 20% in the first year, decreased by 25% in the second year and increased "
  "by 30% in the third year. At the end of three years the population was 3,570 more than at the start. What was "
  "the population at the start?",
  "21,000", ["14,280", "17,000", "25,500"],
  "Net effect of successive changes = product of the growth factors",
  "The net factor is 1.2 × 0.75 × 1.3 = 1.17, a net rise of 17%. So 17% of the population is 3,570 and the "
  "population was 3,570 ÷ 0.17 = 21,000.",
  ["Net factor = 1.20 × 0.75 × 1.30", "1.20 × 0.75 = 0.90; 0.90 × 1.30 = 1.17", "Net increase = 17%",
   "0.17P = 3,570 ⇒ P = 21,000"],
  why="14,280 adds the percentages (20 − 25 + 30 = 25%) instead of multiplying the factors.", secs=80)

S = F(12600) / (F(70, 100) * F(75, 100) * F(80, 100))
new = (S * F(110, 100) - S * F(30, 100)) * F(75, 100) * F(80, 100)
assert S == 30000 and new == 14400 and F(12600) * F(110, 100) == 13860
Q(T, "Income and expenditure", A,
  "Arjun spends 30% of his salary on rent, 25% of the remainder on food and 20% of what is then left on travel. He "
  "saves the rest, which is ₹12,600. His salary now rises by 10%, but his rent stays the same in rupees, and he keeps "
  "the same percentages for food and travel. What are his new savings?",
  "₹14,400", ["₹13,860", "₹15,600", "₹14,850"],
  "Working back through successive percentages; a fixed rupee cost does not grow with salary",
  "Savings = salary × 0.70 × 0.75 × 0.80 = 0.42 × salary, so the salary is ₹30,000 and rent is ₹9,000. The new salary "
  "is ₹33,000; after the same ₹9,000 rent, ₹24,000 is left. After food (25%) ₹18,000 remains and after travel (20%) "
  "₹14,400 is saved.",
  ["Savings = S × 0.70 × 0.75 × 0.80 = 0.42S = 12,600 ⇒ S = 30,000", "Rent = 30% of 30,000 = 9,000 (fixed)",
   "New salary = 33,000; after rent = 24,000", "After food: 24,000 × 0.75 = 18,000",
   "After travel: 18,000 × 0.80 = 14,400"],
  why="₹13,860 raises the savings by 10% as if rent were also 30% of the new salary; ₹15,600 adds the whole ₹3,000 "
      "raise to savings, forgetting that food and travel take their share of it.", secs=110)

# ================================================================ Ratio and Proportion (B2 I2 A2)
T = "Ratio and Proportion"
parts = [F(1, 2), F(1, 3), F(1, 4)]
shares = [7800 * p / sum(parts) for p in parts]
assert shares == [3600, 2400, 1800] and F(7800 * 3, 9) == 2600
Q(T, "Basic ratio", B,
  "₹7,800 is divided among A, B and C in the ratio ½ : ⅓ : ¼. What is B's share?",
  "₹2,400", ["₹2,600", "₹1,800", "₹3,600"],
  "Convert a ratio of fractions to whole numbers by multiplying by the LCM of the denominators",
  "Multiply ½ : ⅓ : ¼ by 12 to get 6 : 4 : 3, a total of 13 parts. One part is 7,800 ÷ 13 = 600, so B gets "
  "4 × 600 = ₹2,400.",
  ["LCM of 2, 3, 4 = 12", "½ : ⅓ : ¼ = 6 : 4 : 3", "13 parts = 7,800 ⇒ 1 part = 600", "B = 4 × 600 = 2,400"],
  why="₹2,600 uses the denominators 2 : 3 : 4 as the ratio; ₹1,800 and ₹3,600 are C's and A's shares.", secs=40)

x = F(math.isqrt(8 * 18))
y = F(12 * 12, 8)
assert x * x == 8 * 18 and y == 18 and x + y == 30
Q(T, "Proportion", B,
  "If x is the mean proportional between 8 and 18, and y is the third proportional to 8 and 12, find x + y.",
  "30", ["31", "24", "36"],
  "Mean proportional of a and b = √(ab); third proportional to a and b = b²/a",
  "x = √(8 × 18) = √144 = 12. For the third proportional, 8 : 12 = 12 : y, so y = 144 ÷ 8 = 18. x + y = 30.",
  ["x = √(8 × 18) = √144 = 12", "8 : 12 :: 12 : y ⇒ y = 12² ÷ 8 = 18", "x + y = 12 + 18 = 30"],
  why="31 takes the mean proportional as the average (8 + 18)/2 = 13.", secs=40)

k = F(240, 5 * 1 + 6 * F(1, 2) + 8 * F(1, 4))
counts = [5 * k, 6 * k, 8 * k]
assert k == 24 and counts == [120, 144, 192] and counts[0] * 1 + counts[1] / 2 + counts[2] / 4 == 240
Q(T, "Coins and salary share", I,
  "A cash box contains ₹1, 50-paise and 25-paise coins in the ratio 5 : 6 : 8 by number. The total value of the "
  "coins is ₹240. How many 50-paise coins are there?",
  "144", ["72", "120", "192"],
  "Convert a ratio of numbers of coins into a ratio of values",
  "Value ratio = 5 × 1 : 6 × 0.5 : 8 × 0.25 = 5 : 3 : 2, total 10 parts = ₹240, so 1 part = ₹24. The 50-paise coins "
  "are worth 3 × 24 = ₹72, which is 72 ÷ 0.5 = 144 coins.",
  ["Values: 5 × ₹1 : 6 × ₹0.50 : 8 × ₹0.25 = 5 : 3 : 2", "10 parts = ₹240 ⇒ 1 part = ₹24",
   "Value of 50-paise coins = 3 × 24 = ₹72", "Number = 72 ÷ 0.5 = 144"],
  short="Number of coins = 6k with value 10k = 240, so k = 24 and 6k = 144.",
  why="72 is the value in rupees, not the number of coins; 120 and 192 are the counts of the other coins.", secs=55)

sol = [k for k in range(1, 50) if F(4 * k - 6, 5 * k - 6) == F(7, 9)]
assert sol == [12]
a_, b_ = 48, 60
Q(T, "Ages via ratio", I,
  "The present ages of Kiran and Lata are in the ratio 4 : 5. Six years ago the ratio was 7 : 9. What will Lata's "
  "age be 8 years from now?",
  "68 years", ["60 years", "56 years", "72 years"],
  "Form an equation from the past ratio",
  "Let the ages be 4k and 5k. (4k − 6) : (5k − 6) = 7 : 9 gives 36k − 54 = 35k − 42, so k = 12. Lata is 60 now and "
  "will be 68 in 8 years.",
  ["Ages: 4k and 5k", "9(4k − 6) = 7(5k − 6) ⇒ 36k − 54 = 35k − 42", "k = 12 ⇒ Kiran 48, Lata 60",
   "Lata after 8 years = 60 + 8 = 68"],
  why="60 is Lata's present age; 56 is Kiran's age after 8 years.", secs=55)

new = [2 * F(115, 100), 3 * F(110, 100), 5 * F(120, 100)]
assert ratio(*new) == "23 : 33 : 60"
assert ratio(2 * F(110, 100), 3 * F(115, 100), 6) == "44 : 69 : 120"
assert ratio(F(23, 10), F(33, 10), 5) == "23 : 33 : 50"
assert ratio(F(215, 100), F(310, 100), F(520, 100)) == "43 : 62 : 104"
Q(T, "Coins and salary share", A,
  "The salaries of three bank officers P, Q and R are in the ratio 2 : 3 : 5. They receive increments of 15%, 10% "
  "and 20% respectively. What is the new ratio of their salaries?",
  "23 : 33 : 60", ["44 : 69 : 120", "23 : 33 : 50", "43 : 62 : 104"],
  "Multiply each term of the ratio by its own growth factor",
  "New salaries are 2 × 1.15 = 2.3, 3 × 1.10 = 3.3 and 5 × 1.20 = 6. Multiplying by 10 gives 23 : 33 : 60.",
  ["P: 2 × 1.15 = 2.3", "Q: 3 × 1.10 = 3.3", "R: 5 × 1.20 = 6.0", "2.3 : 3.3 : 6 = 23 : 33 : 60"],
  why="44 : 69 : 120 swaps P's and Q's increments; 23 : 33 : 50 forgets R's increment; 43 : 62 : 104 adds the "
      "percentages to the ratio terms as decimals (2 + 0.15 and so on).", secs=75)

sol = [k for k in range(1, 100) if 8 * (7 * k - 5) == 9 * (5 * k + 20)]
assert sol == [20] and 7 * 20 + 5 * 20 == 240 and (7 * 20 - 5) + (5 * 20 + 20) == 255
Q(T, "Basic ratio", A,
  "In a coaching centre the ratio of boys to girls is 7 : 5. If 5 boys leave and 20 girls join, the ratio becomes "
  "9 : 8. How many students were there originally?",
  "240", ["255", "228", "264"],
  "Set up the new ratio as an equation in the multiplier",
  "Let the numbers be 7k and 5k. (7k − 5) : (5k + 20) = 9 : 8 gives 56k − 40 = 45k + 180, so 11k = 220 and k = 20. "
  "The original total is 12k = 240.",
  ["Boys = 7k, girls = 5k", "8(7k − 5) = 9(5k + 20)", "56k − 40 = 45k + 180 ⇒ 11k = 220 ⇒ k = 20",
   "Original total = 7k + 5k = 12 × 20 = 240", "Check: 135 boys : 120 girls = 9 : 8"],
  why="255 is the total after the change (135 + 120).", secs=90)

# ================================================================ Problems on Ages (B1 I2 A1)
T = "Problems on Ages"
sol = [s for s in range(1, 60) if 3 * s + 12 == 2 * (s + 12)]
assert sol == [12]
Q(T, "Present and future ages", B,
  "A father is three times as old as his son. After 12 years he will be twice as old as his son. What is the "
  "father's present age?",
  "36 years", ["48 years", "12 years", "30 years"],
  "Translate the future condition into an equation",
  "Let the son be s years old; the father is 3s. In 12 years: 3s + 12 = 2(s + 12), so s = 12 and the father is 36.",
  ["Son = s, father = 3s", "3s + 12 = 2(s + 12) = 2s + 24", "s = 12", "Father = 3 × 12 = 36"],
  why="48 is the father's age after 12 years; 12 is the son's present age.", secs=35)

sol = [k for k in range(1, 40) if 6 * (3 * k + 12) == 5 * (4 * k + 12)]
assert sol == [6]
A_, B_ = 3 * 6 + 5, 4 * 6 + 5
assert (A_, B_) == (23, 29) and A_ + B_ == 52
Q(T, "Ratio-based ages", I,
  "Five years ago the ages of Arun and Bimal were in the ratio 3 : 4. Seven years from now the ratio will be "
  "5 : 6. What is the sum of their present ages?",
  "52 years", ["42 years", "66 years", "56 years"],
  "Ratios at two different times, linked by the same gap of years",
  "Five years ago the ages were 3k and 4k, so now they are 3k + 5 and 4k + 5, and in 7 years 3k + 12 and 4k + 12. "
  "6(3k + 12) = 5(4k + 12) gives k = 6. Present ages are 23 and 29, and the sum is 52.",
  ["5 years ago: 3k, 4k", "7 years from now: 3k + 12, 4k + 12", "6(3k + 12) = 5(4k + 12) ⇒ 18k + 72 = 20k + 60 ⇒ k = 6",
   "Present ages: 18 + 5 = 23 and 24 + 5 = 29", "Sum = 52"],
  why="42 is the sum five years ago; 66 is the sum seven years from now.", secs=60)

sol = [(m, d) for d in range(1, 50) for m in [50 - d] if m - 5 == 7 * (d - 5)]
assert sol == [(40, 10)]
Q(T, "Present and future ages", I,
  "The sum of the present ages of a mother and her daughter is 50 years. Five years ago the mother was seven times "
  "as old as the daughter. What will the mother's age be five years from now?",
  "45 years", ["40 years", "50 years", "15 years"],
  "Two equations from a sum and a past multiple",
  "Let the daughter be d; the mother is 50 − d. Then 45 − d = 7(d − 5), so 8d = 80 and d = 10. The mother is 40 "
  "now and will be 45 in five years.",
  ["Mother = 50 − d", "(50 − d) − 5 = 7(d − 5) ⇒ 45 − d = 7d − 35", "8d = 80 ⇒ d = 10",
   "Mother now = 40; after 5 years = 45"],
  why="40 is the mother's present age; 15 is the daughter's age five years from now.", secs=55)

sol = [x for x in range(1, 40) if (3 * x + 6) + (2 * x + 6) + (2 * x - 4 + 6) == 98]
assert sol == [12]
Aa, Bb, Cc = 36, 24, 20
t = [t for t in range(0, 60) if F(Aa + t) == F(5, 4) * (Bb + t)]
assert t == [24]
Q(T, "Ratio-based ages", A,
  "The present ages of P and Q are in the ratio 3 : 2, and R is 4 years younger than Q. Six years from now the sum "
  "of the ages of P, Q and R will be 98 years. After how many years will P's age be 1.25 times Q's age?",
  "24 years", ["12 years", "18 years", "30 years"],
  "Build the ages from the ratio, then solve a second linear condition",
  "Let P = 3x and Q = 2x; R = 2x − 4. In six years the sum is 7x − 4 + 18 = 98, so x = 12: P = 36, Q = 24, R = 20. "
  "Then 36 + t = 1.25(24 + t) gives 0.25t = 6, so t = 24 years.",
  ["P = 3x, Q = 2x, R = 2x − 4", "Sum after 6 years: 3x + 2x + 2x − 4 + 18 = 98 ⇒ 7x = 84 ⇒ x = 12",
   "P = 36, Q = 24, R = 20", "36 + t = 1.25(24 + t) = 30 + 1.25t ⇒ 0.25t = 6 ⇒ t = 24",
   "Check: in 24 years P = 60, Q = 48 and 60 ÷ 48 = 1.25"],
  why="12 is the multiplier x; 18 comes from forgetting to add 3 × 6 years to the sum.", secs=100)

# ================================================================ Average (B1 I2 A1)
T = "Average"
nums = [46 + d for d in (-6, -4, -2, 0, 2, 4, 6)]
assert sum(nums) / 7 == 46 and max(nums) == 52
Q(T, "Simple average", B,
  "The average of seven consecutive even numbers is 46. What is the largest of these numbers?",
  "52", ["49", "58", "50"],
  "The average of an odd count of equally spaced numbers is the middle number",
  "The middle (4th) number equals the average, 46. The largest is three even steps above it: 46 + 6 = 52.",
  ["Seven consecutive even numbers: middle number = average = 46", "Numbers: 40, 42, 44, 46, 48, 50, 52",
   "Largest = 52"],
  why="49 uses consecutive (not even) numbers; 58 adds 2 × 6 instead of 2 × 3.", secs=30)

new = 58 + 12 * F(3, 2)
assert new == 76
Q(T, "Replacement", I,
  "The average weight of 12 members of a rowing team increases by 1.5 kg when one member weighing 58 kg is replaced "
  "by a new member. What is the weight of the new member?",
  "76 kg", ["59.5 kg", "70 kg", "64 kg"],
  "Replacement: new value = old value + (number of members × change in average)",
  "The total weight rises by 12 × 1.5 = 18 kg, and that rise is due only to the replacement. The new member weighs "
  "58 + 18 = 76 kg.",
  ["Increase in total = 12 × 1.5 = 18 kg", "New member = 58 + 18 = 76 kg"],
  why="59.5 kg adds only 1.5 kg; 70 kg adds 12 kg (the number of members); 64 kg adds 12 × 0.5.", secs=45)

avg = F(30 * 64 + 45 * 72 + 25 * 80, 100)
assert avg == F(716, 10) and F(64 + 72 + 80, 3) == 72
Q(T, "Weighted average", I,
  "Three sections of a training batch have 30, 45 and 25 trainees with average scores 64, 72 and 80 respectively. "
  "What is the average score of all the trainees together?",
  "71.6", ["72", "70.8", "72.4"],
  "Weighted average = total of all scores ÷ total number",
  "Total score = 30 × 64 + 45 × 72 + 25 × 80 = 1,920 + 3,240 + 2,000 = 7,160 for 100 trainees, so the average is "
  "71.6.",
  ["30 × 64 = 1,920", "45 × 72 = 3,240", "25 × 80 = 2,000", "Total = 7,160 for 100 trainees", "Average = 71.6"],
  short="Deviation from 72: (30 × −8 + 0 + 25 × 8) ÷ 100 = −40/100 = −0.4, so 72 − 0.4 = 71.6.",
  why="72 is the simple average of the three averages, which ignores the different section sizes.", secs=55)

pair = 11 * 26 - 9 * 25
keeper = F(pair - 3, 2)
assert pair == 61 and keeper == 29
Q(T, "Replacement", A,
  "The average age of an 11-member cricket team is 26 years. When the captain and the wicket-keeper are excluded, "
  "the average age of the remaining players is 1 year less than the team average. If the captain is 3 years older "
  "than the wicket-keeper, how old is the wicket-keeper?",
  "29 years", ["32 years", "30.5 years", "28 years"],
  "Difference of totals gives the sum of the excluded values",
  "Team total = 11 × 26 = 286. The other 9 players average 25, total 225. So captain + keeper = 61, and with the "
  "captain 3 years older, the keeper is (61 − 3) ÷ 2 = 29.",
  ["Team total = 11 × 26 = 286", "Remaining 9 players: 9 × 25 = 225", "Captain + keeper = 286 − 225 = 61",
   "Keeper = (61 − 3) ÷ 2 = 29; captain = 32"],
  why="32 is the captain's age; 30.5 halves 61 without using the 3-year gap.", secs=75)

# ================================================================ Profit and Loss (B2 I3 A2)
T = "Profit and Loss"
cp = F(1232) / F(88, 100)
assert cp == 1400 and cp * F(115, 100) == 1610 and F(1232) * F(115, 100) == F(14168, 10)
Q(T, "Cost and selling price", B,
  "A trader sold a mixer-grinder at a loss of 12% for ₹1,232. At what price should he sell it to gain 15%?",
  "₹1,610", ["₹1,416.80", "₹1,564.64", "₹1,540"],
  "Find the cost price first; profit and loss percentages are on the cost price",
  "CP = 1,232 ÷ 0.88 = ₹1,400. For a 15% gain, SP = 1,400 × 1.15 = ₹1,610.",
  ["CP = SP ÷ (1 − 12/100) = 1,232 ÷ 0.88 = 1,400", "Required SP = 1,400 × 1.15 = 1,610"],
  short="SP₂ = 1,232 × 115/88 = 14 × 115 = 1,610.",
  why="₹1,416.80 adds 15% to the old selling price instead of the cost price; ₹1,564.64 adds 27% to the selling "
      "price.", secs=40)

pf = F(140, 100) * F(85, 100) - 1
assert pf == F(19, 100)
Q(T, "Marked price", B,
  "A shopkeeper marks his goods 40% above the cost price and allows a discount of 15% on the marked price. What is "
  "his profit percentage?",
  "19%", ["25%", "21%", "15%"],
  "Profit factor = (1 + markup) × (1 − discount)",
  "Take CP = 100. MP = 140 and SP = 85% of 140 = 119, so the profit is 19%.",
  ["CP = 100 ⇒ MP = 140", "SP = 140 × 0.85 = 119", "Profit = 19 on 100 = 19%"],
  short="40 − 15 − (40 × 15)/100 = 40 − 15 − 6 = 19%.",
  why="25% subtracts the discount from the markup directly (40 − 15).", secs=35)

gain = F(108, 100) / F(900, 1000) - 1
assert gain == F(20, 100) and F(18, 108) == F(1, 6)
Q(T, "Dishonest dealer", I,
  "A grocer claims to sell rice at 8% above cost price, but uses a weight of 900 g in place of 1 kg. What is his "
  "actual gain percentage?",
  "20%", ["18%", "19.11%", "16⅔%"],
  "Dishonest dealer: gain factor = (1 + stated markup) × (true weight ÷ weight given)",
  "Let 1 g cost ₹1. He gives 900 g, costing ₹900, but charges for 1,000 g at 8% above cost, i.e. ₹1,080. "
  "Gain = 180 on 900 = 20%.",
  ["Cost of 900 g = ₹900 (at ₹1 per g)", "He charges for 1 kg: 1,000 × 1.08 = ₹1,080",
   "Gain = 1,080 − 900 = ₹180", "Gain % = 180 ÷ 900 × 100 = 20%"],
  short="1.08 × 1000/900 = 1.08 × 10/9 = 1.2.",
  why="18% adds 8% and 10%; 19.11% adds 8% and 11.11%; 16⅔% divides the gain of 180 by the 1,080 he charges "
      "instead of by the cost.", secs=55)

cp = F(5940) / (F(120, 100) * F(90, 100))
assert cp == 5500 and F(5940) / F(110, 100) == 5400 and F(5940) * F(90, 100) == 5346
Q(T, "Successive transactions", I,
  "A sells a scooter to B at a profit of 20%. B sells it to C at a loss of 10%. If C pays ₹59,400, at what price "
  "did A buy it?",
  "₹55,000", ["₹54,000", "₹53,460", "₹60,000"],
  "Chain of transactions: multiply the factors and divide back",
  "C's price = A's CP × 1.2 × 0.9 = 1.08 × A's CP. So A's CP = 59,400 ÷ 1.08 = ₹55,000.",
  ["B's CP = A's CP × 1.20", "C's price = A's CP × 1.20 × 0.90 = 1.08 × A's CP",
   "A's CP = 59,400 ÷ 1.08 = 55,000"],
  why="₹54,000 treats the net change as +10% (20 − 10); ₹53,460 takes 90% of C's price.", secs=55)
assert F(59400) / F(108, 100) == 55000 and F(59400) / F(110, 100) == 54000 and F(59400) * F(90, 100) == 53460

cost = 60 * 480
rev = 40 * 480 * F(125, 100) + 20 * 480 * F(90, 100)
pf = (rev - cost) / cost * 100
assert cost == 28800 and rev == 32640 and pf == F(40, 3)
Q(T, "Cost and selling price", I,
  "A dealer bought 60 calculators at ₹480 each. He sold two-thirds of them at a profit of 25% and the rest at a loss "
  "of 10%. What is his overall profit percentage?",
  "13⅓%", ["7.5%", "15%", "11⅔%"],
  "Overall profit is a weighted average of the individual percentages (weights = cost of each lot)",
  "40 calculators are sold at 25% profit and 20 at 10% loss. Since each calculator costs the same, the overall "
  "profit is (2 × 25 − 1 × 10) ÷ 3 = 40/3 = 13⅓%.",
  ["Cost = 60 × 480 = ₹28,800", "40 sold at ₹600 = ₹24,000", "20 sold at ₹432 = ₹8,640",
   "Revenue = ₹32,640; profit = ₹3,840", "Profit % = 3,840 ÷ 28,800 × 100 = 13⅓%"],
  short="Weighted average: (2 × 25 + 1 × (−10)) ÷ 3 = 13⅓%.",
  why="7.5% is the simple average of +25% and −10%; 15% just subtracts 10 from 25.", secs=60)

eff = F(150, 100) * F(90, 100) * F(90, 100) * F(9, 10)
assert eff == F(10935, 10000) and F(150, 100) * F(81, 100) == F(1215, 1000) and F(150, 100) * F(80, 100) * F(9, 10) == F(108, 100)
Q(T, "Marked price", A,
  "A trader marks his goods 50% above cost. He allows two successive discounts of 10% each and, in addition, gives "
  "one article free with every nine articles bought. What is his overall profit percentage?",
  "9.35%", ["21.5%", "8%", "12.5%"],
  "Successive discounts multiply; 'one free with nine' means 10 articles are given for the price of 9",
  "Take the CP of one article as 100. MP = 150; after 10% and 10%, the price is 150 × 0.81 = 121.5. For 10 "
  "articles (cost 1,000) he receives 9 × 121.5 = 1,093.5, so the profit is 9.35%.",
  ["CP per article = 100, MP = 150", "After two 10% discounts: 150 × 0.9 × 0.9 = 121.5",
   "He gives 10 articles and is paid for 9: 9 × 121.5 = 1,093.5", "Cost of 10 articles = 1,000",
   "Profit = 93.5 on 1,000 = 9.35%"],
  why="21.5% ignores the free article; 8% adds the two discounts to 20% instead of applying them one after the other.",
  secs=100)

sols = [(a, 8400 - a) for a in range(1, 8400) if F(16, 100) * a == F(12, 100) * (8400 - a)]
assert sols == [(3600, 4800)]
Q(T, "Successive transactions", A,
  "A man bought two used laptops for ₹84,000 in total. He sold one at a profit of 16% and the other at a loss of "
  "12%, and on the whole neither gained nor lost. What was the cost price of the laptop sold at a loss?",
  "₹48,000", ["₹36,000", "₹42,000", "₹50,400"],
  "No overall gain or loss: the profit on one equals the loss on the other",
  "16% of x = 12% of (84,000 − x), so 4x = 3(84,000 − x), giving x = ₹36,000 for the one sold at a profit. The one "
  "sold at a loss cost 84,000 − 36,000 = ₹48,000.",
  ["Let the CP of the profitable laptop be x", "0.16x = 0.12(84,000 − x) ⇒ 16x = 12(84,000 − x)",
   "28x = 10,08,000 ⇒ x = 36,000", "CP of the other = 84,000 − 36,000 = 48,000",
   "Check: profit 5,760 = loss 5,760"],
  short="The costs are in the inverse ratio of the percentages: 12 : 16 = 3 : 4, so 4/7 × 84,000 = 48,000.",
  why="₹36,000 is the laptop sold at a profit; ₹42,000 assumes both cost the same.", secs=80)
assert F(16, 100) * 36000 == F(12, 100) * 48000 == 5760

# ================================================================ Discount (B1 I2 A1)
T = "Discount"
mp = F(1968) / F(82, 100)
assert mp == 2400 and F(1968) * F(118, 100) == F(232224, 100)
Q(T, "Single discount", B,
  "After allowing a discount of 18%, a store sells a pair of shoes for ₹1,968. What is the marked price?",
  "₹2,400", ["₹2,322.24", "₹2,360", "₹2,460"],
  "SP = MP × (1 − discount%)",
  "1,968 is 82% of the marked price, so MP = 1,968 ÷ 0.82 = ₹2,400.",
  ["SP = 82% of MP", "MP = 1,968 ÷ 0.82 = 2,400"],
  why="₹2,322.24 adds 18% to the selling price; the discount is on the marked price, not on the selling price.",
  secs=35)

flat = 5000 * F(70, 100)
succ = 5000 * F(80, 100) * F(90, 100)
assert flat == 3500 and succ == 3600 and succ - flat == 100
Q(T, "Successive discounts", I,
  "On a microwave oven marked at ₹5,000, one shop offers a flat 30% discount and another offers successive "
  "discounts of 20% and 10%. How much more does a customer pay at the second shop?",
  "₹100", ["No difference", "₹150", "₹50"],
  "Successive discounts a% and b% equal a single discount of a + b − ab/100",
  "Flat 30%: 5,000 × 0.70 = ₹3,500. Successive 20% and 10%: 5,000 × 0.8 × 0.9 = ₹3,600. The second shop costs "
  "₹100 more.",
  ["Shop 1: 5,000 × 0.70 = 3,500", "Shop 2: 5,000 × 0.80 = 4,000, then 4,000 × 0.90 = 3,600",
   "Difference = 3,600 − 3,500 = 100"],
  short="20% and 10% successive = 28% single; 2% of 5,000 = ₹100.",
  why="'No difference' assumes 20% + 10% = 30%.", secs=45)

mp = F(1500) * F(112, 100) / F(80, 100)
assert mp == 2100 and F(1500) * F(112, 100) * F(120, 100) == 2016 and F(1500) * F(132, 100) == 1980
Q(T, "Discount with profit", I,
  "A shopkeeper allows a discount of 20% on the marked price and still makes a profit of 12%. If the cost price of "
  "an article is ₹1,500, what is its marked price?",
  "₹2,100", ["₹2,016", "₹1,980", "₹2,240"],
  "MP × (1 − d) = CP × (1 + p)",
  "SP = 1,500 × 1.12 = ₹1,680. Since SP is 80% of MP, MP = 1,680 ÷ 0.8 = ₹2,100.",
  ["SP = 1,500 × 1.12 = 1,680", "SP = 0.80 × MP ⇒ MP = 1,680 ÷ 0.80 = 2,100"],
  why="₹2,016 adds 20% to the selling price instead of dividing by 0.8; ₹1,980 adds 32% to the cost price.",
  secs=50)

r = F(1225, 1000) / F(875, 1000)
pf = r * F(80, 100) - 1
assert r == F(7, 5) and pf == F(12, 100)
Q(T, "Discount with profit", A,
  "By allowing a discount of 12.5% on the marked price, a dealer earns a profit of 22.5%. What would his profit "
  "percentage be if he allowed a discount of 20% instead?",
  "12%", ["15%", "10%", "14%"],
  "The ratio MP : CP stays fixed; recompute SP with the new discount",
  "MP × 0.875 = CP × 1.225, so MP = 1.4 × CP. With a 20% discount, SP = 0.8 × 1.4 × CP = 1.12 × CP: a 12% profit.",
  ["MP × 0.875 = CP × 1.225", "MP/CP = 1.225 ÷ 0.875 = 1.4", "New SP = 0.80 × 1.4 CP = 1.12 CP",
   "Profit = 12%"],
  why="15% just reduces the profit by the extra 7.5% discount, ignoring that the discount is on a larger base (MP).",
  secs=75)

# ================================================================ Simple Interest (B1 I2 A1)
T = "Simple Interest"
si = F(12500) * 8 * F(7, 2) / 100
assert si == 3500 and F(12500) * 8 * 3 / 100 == 3000
Q(T, "Basic SI", B,
  "What is the simple interest on ₹12,500 at 8% per annum for 3 years and 6 months?",
  "₹3,500", ["₹3,000", "₹16,000", "₹3,750"],
  "SI = P × R × T ÷ 100, with T in years",
  "T = 3.5 years. SI = 12,500 × 8 × 3.5 ÷ 100 = ₹3,500.",
  ["T = 3 years 6 months = 3.5 years", "SI = 12,500 × 8 × 3.5 ÷ 100", "= 125 × 28 = 3,500"],
  why="₹3,000 ignores the 6 months; ₹16,000 is the amount, not the interest.", secs=30)

rate = F(100, 8)
t = F(250) / rate
assert rate == F(25, 2) and t == 20
Q(T, "Basic SI", I,
  "A sum of money doubles itself in 8 years at simple interest. In how many years will it become 3.5 times "
  "itself at the same rate?",
  "20 years", ["28 years", "24 years", "18 years"],
  "At simple interest, the interest grows linearly with time",
  "Doubling means interest = 100% of the principal in 8 years, so the rate is 12.5% per annum. To become 3.5 times, "
  "the interest must be 250%, which takes 250 ÷ 12.5 = 20 years.",
  ["Interest in 8 years = 100% of P ⇒ R = 100 ÷ 8 = 12.5%", "3.5 times ⇒ interest = 250% of P",
   "Time = 250 ÷ 12.5 = 20 years"],
  short="100% takes 8 years, so 250% takes 8 × 2.5 = 20 years.",
  why="28 multiplies 8 by 3.5, using the amount instead of the interest.", secs=45)

ry = 6 * 2 + 8 * 3 + 10 * 3
p = F(7920) * 100 / ry
assert ry == 66 and p == 12000 and F(7920) * 100 / 64 == F(12375) and F(7920) * 100 / 72 == 11000
Q(T, "SI with changing rates", I,
  "A sum is lent at simple interest at 6% per annum for the first 2 years, 8% per annum for the next 3 years and "
  "10% per annum after that. If the total interest at the end of 8 years is ₹7,920, find the sum.",
  "₹12,000", ["₹12,375", "₹11,000", "₹13,200"],
  "With changing rates, add up rate × years for each period",
  "Total rate-years = 6 × 2 + 8 × 3 + 10 × 3 = 12 + 24 + 30 = 66, so the interest is 66% of the sum. "
  "Sum = 7,920 ÷ 0.66 = ₹12,000.",
  ["First 2 years: 6 × 2 = 12%", "Next 3 years: 8 × 3 = 24%", "Last 3 years (years 6 to 8): 10 × 3 = 30%",
   "Total = 66% of P = 7,920 ⇒ P = 12,000"],
  why="₹12,375 uses the plain average rate 8% for all 8 years; ₹11,000 counts 4 years at 10%.", secs=60)
assert F(7920) * 100 / 60 == 13200

sols = [a for a in range(0, 40001, 100) if 3 * (F(8, 100) * a + F(12, 100) * (40000 - a)) == 11520]
assert sols == [24000]
Q(T, "SI with changing rates", A,
  "Ravi lent ₹40,000 in two parts: one part to Suresh at 8% per annum and the rest to Manoj at 12% per annum, both "
  "at simple interest. After 3 years he received ₹11,520 as total interest. How much did he lend to Suresh?",
  "₹24,000", ["₹16,000", "₹20,000", "₹28,000"],
  "Split-sum problems: set up one equation, or use alligation on the average rate",
  "The average rate is 11,520 ÷ (40,000 × 3) = 9.6%. By alligation, Suresh : Manoj = (12 − 9.6) : (9.6 − 8) = "
  "2.4 : 1.6 = 3 : 2. Suresh got 3/5 × 40,000 = ₹24,000.",
  ["Interest per year = 11,520 ÷ 3 = 3,840", "Average rate = 3,840 ÷ 40,000 = 9.6%",
   "Alligation: (12 − 9.6) : (9.6 − 8) = 2.4 : 1.6 = 3 : 2", "Suresh = 3/5 × 40,000 = 24,000",
   "Check: 24,000 × 8% + 16,000 × 12% = 1,920 + 1,920 = 3,840 per year"],
  why="₹16,000 is the part lent to Manoj (the ratio read the wrong way round).", secs=80)

# ================================================================ Compound Interest (B2 I2 A2)
T = "Compound Interest"
ci = 15000 * (F(11, 10) ** 2 - 1)
assert ci == 3150
Q(T, "Annual compounding", B,
  "Find the compound interest on ₹15,000 for 2 years at 10% per annum, compounded annually.",
  "₹3,150", ["₹3,000", "₹18,150", "₹3,300"],
  "CI = P[(1 + R/100)ⁿ − 1]",
  "Amount = 15,000 × 1.1² = 15,000 × 1.21 = ₹18,150, so the CI is ₹3,150.",
  ["Year 1 interest = 10% of 15,000 = 1,500", "Year 2 interest = 10% of 16,500 = 1,650",
   "CI = 1,500 + 1,650 = 3,150"],
  short="For 2 years at 10%, CI = 21% of P = 0.21 × 15,000.",
  why="₹3,000 is simple interest; ₹18,150 is the amount.", secs=35)

p = F(96) / F(8, 100) ** 2
assert p == 15000 and F(96) / F(8, 100) == 1200
Q(T, "CI vs SI difference", B,
  "The difference between the compound interest and the simple interest on a sum for 2 years at 8% per annum is "
  "₹96. Find the sum.",
  "₹15,000", ["₹1,200", "₹12,000", "₹7,500"],
  "For 2 years, CI − SI = P(R/100)²",
  "96 = P × (0.08)² = 0.0064P, so P = 96 ÷ 0.0064 = ₹15,000.",
  ["CI − SI for 2 years = P × (R/100)²", "96 = P × 0.0064", "P = 15,000"],
  why="₹1,200 divides by 0.08 instead of 0.08²; ₹7,500 divides by 2 × 0.0064.", secs=40)

ci = 32000 * (F(11, 10) ** 3 - 1)
assert ci == 10592 and 32000 * F(20, 100) * F(3, 2) == 9600 and 32000 * F(12, 10) * F(11, 10) - 32000 == 10240
Q(T, "Half-yearly and quarterly", I,
  "What is the compound interest on ₹32,000 for 1½ years at 20% per annum, compounded half-yearly?",
  "₹10,592", ["₹9,600", "₹10,240", "₹11,200"],
  "Half-yearly compounding: halve the rate and double the number of periods",
  "Rate per half-year = 10% and there are 3 half-years. Amount = 32,000 × 1.1³ = 32,000 × 1.331 = ₹42,592, so CI = "
  "₹10,592.",
  ["Rate per half-year = 20 ÷ 2 = 10%; periods = 1.5 × 2 = 3", "Amount = 32,000 × (1.1)³ = 32,000 × 1.331 = 42,592",
   "CI = 42,592 − 32,000 = 10,592"],
  short="3 periods at 10%: 33.1% of 32,000 = 10,592.",
  why="₹9,600 is simple interest; ₹10,240 compounds annually for 1 year and then adds simple interest for the "
      "half-year.", secs=55)

rate = F(14641, 13310) - 1
p = F(13310) / (1 + rate) ** 3
assert rate == F(1, 10) and p == 10000 and 13310 - 3 * 1331 == 9317
Q(T, "Annual compounding", I,
  "A sum invested at compound interest (compounded annually) amounts to ₹13,310 in 3 years and to ₹14,641 in 4 years. "
  "What is the sum?",
  "₹10,000", ["₹11,000", "₹9,317", "₹12,100"],
  "Consecutive annual amounts differ by one year's interest on the previous amount",
  "Interest in year 4 = 14,641 − 13,310 = 1,331, which is 10% of 13,310, so the rate is 10%. Then "
  "P = 13,310 ÷ 1.1³ = 13,310 ÷ 1.331 = ₹10,000.",
  ["Rate = (14,641 − 13,310) ÷ 13,310 = 1,331 ÷ 13,310 = 10%", "13,310 = P × (1.1)³ = 1.331P",
   "P = 10,000"],
  why="₹11,000 discounts only 2 years; ₹9,317 subtracts 1,331 three times as if the interest were simple.",
  secs=60)

loan = sum(F(13310) / F(11, 10) ** k for k in (1, 2, 3))
assert loan == 33100 and 3 * 13310 == 39930
Q(T, "Instalments", A,
  "A loan taken at 10% per annum compound interest (compounded annually) is repaid in three equal annual "
  "instalments of ₹13,310 each, the first paid one year after the loan. What was the amount of the loan?",
  "₹33,100", ["₹39,930", "₹36,300", "₹30,250"],
  "Loan = sum of the present values of the instalments",
  "Discount each instalment to today: 13,310 ÷ 1.1 = 12,100; 13,310 ÷ 1.21 = 11,000; 13,310 ÷ 1.331 = 10,000. "
  "Loan = 12,100 + 11,000 + 10,000 = ₹33,100.",
  ["PV of instalment 1 = 13,310 ÷ 1.1 = 12,100", "PV of instalment 2 = 13,310 ÷ 1.21 = 11,000",
   "PV of instalment 3 = 13,310 ÷ 1.331 = 10,000", "Loan = 33,100"],
  short="13,310 = 1.1³ × 10,000, so the present values are 10,000 × (1.21, 1.1, 1).",
  why="₹39,930 is the total repaid; ₹36,300 discounts all three instalments by one year only.", secs=90)
assert 3 * F(13310) / F(11, 10) == 36300

p = F(930) / (F(11, 10) ** 3 - 1 - F(3, 10))
ci2 = p * (F(11, 10) ** 2 - 1)
assert p == 30000 and ci2 == 6300 and p * F(331, 1000) == 9930
Q(T, "CI vs SI difference", A,
  "The difference between the compound interest (compounded annually) and the simple interest on a sum for 3 years "
  "at 10% per annum is ₹930. What is the compound interest on the same sum for 2 years at the same rate?",
  "₹6,300", ["₹6,000", "₹9,930", "₹6,600"],
  "For 3 years, CI − SI = P(r/100)²(3 + r/100)",
  "CI − SI for 3 years at 10% = P × 0.01 × 3.1 = 0.031P = 930, so P = ₹30,000. CI for 2 years = 21% of 30,000 = "
  "₹6,300.",
  ["3-year CI = 33.1% of P; 3-year SI = 30% of P", "Difference = 3.1% of P = 930 ⇒ P = 30,000",
   "2-year CI = 21% of 30,000 = 6,300"],
  why="₹6,000 is the 2-year simple interest; ₹9,930 is the 3-year compound interest; ₹6,600 takes 22% for two "
      "years.", secs=90)

# ================================================================ Partnership (B1 I2 A1)
T = "Partnership"
inv = [45000, 60000, 75000]
b_share = F(36000) * inv[1] / sum(inv)
assert b_share == 12000
Q(T, "Simple partnership", B,
  "A, B and C start a business with ₹45,000, ₹60,000 and ₹75,000 respectively for one year. Out of a profit of "
  "₹36,000, what is B's share?",
  "₹12,000", ["₹9,000", "₹15,000", "₹10,800"],
  "Equal time: profit is shared in the ratio of capitals",
  "45,000 : 60,000 : 75,000 = 3 : 4 : 5 (12 parts). One part = 36,000 ÷ 12 = 3,000, so B gets 4 × 3,000 = ₹12,000.",
  ["Ratio = 45 : 60 : 75 = 3 : 4 : 5", "12 parts = 36,000 ⇒ 1 part = 3,000", "B = 4 × 3,000 = 12,000"],
  why="₹9,000 and ₹15,000 are A's and C's shares.", secs=35)

a_cap = 30000 * 7 + 20000 * 5
b_cap = 40000 * 8
b_sh = F(63000) * b_cap / (a_cap + b_cap)
assert (a_cap, b_cap) == (310000, 320000) and b_sh == 32000 and F(63000) * 4 / 7 == 36000
Q(T, "Compound partnership", I,
  "Neha starts a business with ₹30,000. After 4 months Vikram joins with ₹40,000. Three months after Vikram joins, "
  "Neha withdraws ₹10,000. Out of a profit of ₹63,000 at the end of the year, what is Vikram's share?",
  "₹32,000", ["₹31,000", "₹36,000", "₹31,500"],
  "Profit share ∝ capital × time (month-weighted capital)",
  "Neha: 30,000 for 7 months and 20,000 for 5 months = 3,10,000. Vikram: 40,000 for 8 months = 3,20,000. Ratio "
  "31 : 32, so Vikram gets 32/63 × 63,000 = ₹32,000.",
  ["Neha: 30,000 × 7 + 20,000 × 5 = 2,10,000 + 1,00,000 = 3,10,000", "Vikram: 40,000 × 8 = 3,20,000",
   "Ratio = 31 : 32 (63 parts)", "Vikram = 32 × 1,000 = 32,000"],
  why="₹31,000 is Neha's share; ₹36,000 ignores time and uses the capital ratio 3 : 4.", secs=65)

prof = F(27600) / (F(10, 100) + F(90, 100) * F(2, 5))
assert prof == 60000 and F(27600) / F(2, 5) == 69000
Q(T, "Working partner", I,
  "Asha and Bina invest in a firm in the ratio 2 : 3. Asha manages the firm and takes 10% of the profit as salary; "
  "the remaining profit is shared in the ratio of investment. If Asha receives ₹27,600 in all, what is the total "
  "profit?",
  "₹60,000", ["₹69,000", "₹66,000", "₹55,200"],
  "Working partner: salary first, then the balance in the capital ratio",
  "Asha gets 10% + 2/5 of 90% = 10% + 36% = 46% of the profit. 0.46 × profit = 27,600, so the profit is ₹60,000.",
  ["Salary = 10% of profit", "Remaining 90% shared 2 : 3 ⇒ Asha gets 2/5 × 90% = 36%",
   "Asha's total = 46% of profit = 27,600", "Profit = 27,600 ÷ 0.46 = 60,000"],
  why="₹69,000 ignores the salary and treats ₹27,600 as 2/5 of the profit.", secs=60)

a = 24000 * 6 + 36000 * 6
b = 36000 * 6 + 30000 * 6
c = 45000 * 3
c_sh = F(79200) * c / (a + b + c)
assert (a, b, c) == (360000, 396000, 135000) and ratio(a, b, c) == "40 : 44 : 15" and c_sh == 12000
assert F(79200) * a / (a + b + c) == 32000 and F(79200) * b / (a + b + c) == 35200
Q(T, "Compound partnership", A,
  "P and Q start a business with ₹24,000 and ₹36,000. After 6 months P adds ₹12,000 and Q withdraws ₹6,000. "
  "Three months later R joins with ₹45,000. If the profit at the end of the year is ₹79,200, what is R's share?",
  "₹12,000", ["₹32,000", "₹35,200", "₹26,400"],
  "Month-weighted capital with changes during the year",
  "P: 24,000 × 6 + 36,000 × 6 = 3,60,000. Q: 36,000 × 6 + 30,000 × 6 = 3,96,000. R: 45,000 × 3 = 1,35,000. "
  "Ratio 40 : 44 : 15 (99 parts), so R gets 15/99 × 79,200 = ₹12,000.",
  ["P = 24,000 × 6 + 36,000 × 6 = 3,60,000", "Q = 36,000 × 6 + 30,000 × 6 = 3,96,000",
   "R joins after 9 months: 45,000 × 3 = 1,35,000", "Ratio = 360 : 396 : 135 = 40 : 44 : 15",
   "R = 79,200 × 15/99 = 12,000"],
  why="₹32,000 and ₹35,200 are P's and Q's shares; ₹26,400 splits the profit equally.", secs=100)

# ================================================================ Mixture and Alligation (B2 I2 A2)
T = "Mixture and Alligation"
r_ = ratio(54 - 46, 46 - 42)
assert r_ == "2 : 1" and F(2 * 42 + 1 * 54, 3) == 46
Q(T, "Alligation rule", B,
  "In what ratio must rice costing ₹42 per kg be mixed with rice costing ₹54 per kg so that the mixture costs ₹46 "
  "per kg?",
  "2 : 1", ["1 : 2", "3 : 1", "4 : 3"],
  "Alligation: cheaper : dearer = (dearer − mean) : (mean − cheaper)",
  "Cheaper : dearer = (54 − 46) : (46 − 42) = 8 : 4 = 2 : 1.",
  ["Dearer − mean = 54 − 46 = 8", "Mean − cheaper = 46 − 42 = 4", "Ratio = 8 : 4 = 2 : 1",
   "Check: (2 × 42 + 1 × 54) ÷ 3 = 138 ÷ 3 = 46"],
  why="1 : 2 writes the alligation differences the wrong way round.", secs=30)

milk, water = 30, 10
add = [w for w in range(0, 50) if F(milk, water + w) == F(3, 2)]
assert add == [10]
Q(T, "Mixing solutions", B,
  "A 40-litre mixture contains milk and water in the ratio 3 : 1. How much water must be added to make the ratio "
  "3 : 2?",
  "10 litres", ["5 litres", "15 litres", "20 litres"],
  "Milk stays constant when only water is added",
  "Milk = 30 L and water = 10 L. For 3 : 2 with 30 L of milk, water must be 20 L, so 10 L must be added.",
  ["Milk = 3/4 × 40 = 30 L; water = 10 L", "Required: 30 : W = 3 : 2 ⇒ W = 20 L", "Water to add = 20 − 10 = 10 L"],
  why="20 litres is the final quantity of water, not the amount to add.", secs=35)

left = 80 * F(9, 10) ** 3
assert left == F(5832, 100)
Q(T, "Replacement of mixture", I,
  "A container holds 80 litres of pure milk. 8 litres are taken out and replaced with water. This is done two more "
  "times. How much milk is left in the container?",
  "58.32 litres", ["56 litres", "57.6 litres", "60 litres"],
  "Repeated replacement: milk left = initial × (1 − x/V)ⁿ",
  "Each operation keeps 72/80 = 0.9 of the milk. After three operations, milk = 80 × 0.9³ = 80 × 0.729 = 58.32 L.",
  ["Fraction kept each time = 1 − 8/80 = 0.9", "After 3 operations: 80 × 0.9³", "= 80 × 0.729 = 58.32 L"],
  why="56 litres subtracts 8 litres of pure milk each time, ignoring that later withdrawals already contain water.",
  secs=50)

cp = F(2475, 10) / F(125, 100)
r_ = ratio(240 - cp, cp - 180)
assert cp == 198 and r_ == "7 : 3"
Q(T, "Alligation rule", I,
  "A merchant mixes tea costing ₹180 per kg with tea costing ₹240 per kg and sells the blend at ₹247.50 per kg, "
  "making a 25% profit. In what ratio did he mix the two teas?",
  "7 : 3", ["3 : 7", "1 : 1", "3 : 2"],
  "Find the cost price of the mixture from the selling price, then apply alligation",
  "Cost of the blend = 247.50 ÷ 1.25 = ₹198 per kg. Cheaper : dearer = (240 − 198) : (198 − 180) = 42 : 18 = 7 : 3.",
  ["CP of blend = 247.50 ÷ 1.25 = 198", "240 − 198 = 42 and 198 − 180 = 18", "Ratio = 42 : 18 = 7 : 3"],
  why="Using ₹247.50 directly as the mean gives no valid alligation (it lies above both prices); 3 : 7 reverses the "
      "ratio.", secs=55)

m, w = F(42), F(18)
m, w = m * F(2, 3), w * F(2, 3) + 20
m, w = m * F(2, 3) + 20, w * F(2, 3)
assert (m, w) == (F(116, 3), F(64, 3)) and ratio(m, w) == "29 : 16"
Q(T, "Replacement of mixture", A,
  "A 60-litre vessel holds milk and water in the ratio 7 : 3. 20 litres of the mixture are drawn off and replaced "
  "with water. Then 20 litres of the new mixture are drawn off and replaced with pure milk. What is the final ratio "
  "of milk to water?",
  "29 : 16", ["7 : 8", "16 : 29", "3 : 2"],
  "Each withdrawal removes the same fraction of both components",
  "Start: milk 42, water 18. Removing 20 L (one-third) leaves 28 and 12; adding water gives 28 : 32. Removing "
  "one-third again leaves 56/3 and 64/3; adding 20 L milk gives 116/3 : 64/3 = 29 : 16.",
  ["Start: milk 42 L, water 18 L", "Draw 20 L (1/3): milk 28, water 12; add 20 L water ⇒ 28 : 32",
   "Draw 20 L (1/3): milk 18⅔, water 21⅓", "Add 20 L milk ⇒ milk 38⅔, water 21⅓", "Ratio = 116 : 64 = 29 : 16"],
  why="7 : 8 is the ratio after the first step only; 16 : 29 is reversed.", secs=100)

ga, gb, target = F(5, 8), F(2, 5), F(3, 5)
qty = [x for x in [F(k, 2) for k in range(1, 40)] if (24 * ga + x * gb) / (24 + x) == target]
assert qty == [3]
Q(T, "Mixing solutions", A,
  "Alloy A contains gold and copper in the ratio 5 : 3 and alloy B contains them in the ratio 2 : 3. How many kg of "
  "alloy B must be melted with 24 kg of alloy A to obtain an alloy with gold and copper in the ratio 3 : 2?",
  "3 kg", ["4 kg", "6 kg", "8 kg"],
  "Alligation on the fraction of gold in each alloy",
  "Gold fractions: A = 5/8, B = 2/5, target = 3/5. A : B = (3/5 − 2/5) : (5/8 − 3/5) = 1/5 : 1/40 = 8 : 1. With "
  "24 kg of A, B = 24 ÷ 8 = 3 kg.",
  ["Gold in A = 5/8 = 0.625; in B = 2/5 = 0.4; target = 3/5 = 0.6", "A : B = (0.6 − 0.4) : (0.625 − 0.6) = 0.2 : 0.025 = 8 : 1",
   "B = 24 ÷ 8 = 3 kg", "Check: gold = 15 + 1.2 = 16.2 of 27 kg = 0.6"],
  why="8 kg uses the ratio the wrong way round (24 ÷ 3); 6 kg compares the copper ratios incorrectly.", secs=100)

# ================================================================ Time and Work (B2 I2 A2)
T = "Time and Work"
d = 1 / (F(1, 12) + F(1, 18))
assert d == F(36, 5)
Q(T, "Work efficiency", B,
  "A can complete a piece of work in 12 days and B in 18 days. In how many days can they finish it working together?",
  "7.2 days", ["15 days", "6 days", "30 days"],
  "Combined rate = sum of individual rates",
  "Take the work as 36 units (LCM of 12 and 18). A does 3 units a day and B 2, so together 5 units a day: "
  "36 ÷ 5 = 7.2 days.",
  ["Total work = LCM(12, 18) = 36 units", "A = 3 units/day, B = 2 units/day", "Together = 5 units/day",
   "Time = 36 ÷ 5 = 7.2 days"],
  short="ab/(a + b) = 12 × 18 ÷ 30 = 7.2.",
  why="15 days averages the two times; 30 days adds them.", secs=35)

a_sh = F(4500) * F(1, 10) / (F(1, 10) + F(1, 15))
assert a_sh == 2700
Q(T, "Work and wages", B,
  "Ramesh can paint a hall in 10 days and Suresh in 15 days. They paint it together and are paid ₹4,500. What is "
  "Ramesh's share?",
  "₹2,700", ["₹1,800", "₹2,250", "₹3,000"],
  "Wages are shared in the ratio of work done, i.e. of efficiencies when they work for the same time",
  "Efficiencies are 1/10 : 1/15 = 3 : 2. Ramesh gets 3/5 × 4,500 = ₹2,700.",
  ["Ratio of efficiencies = 1/10 : 1/15 = 3 : 2", "Ramesh = 3/5 × 4,500 = 2,700"],
  why="₹1,800 shares in the ratio of days (10 : 15), which is the inverse of efficiency.", secs=35)

done, day = F(0), 0
while done < 1:
    day += 1
    done += F(1, 20) if day % 2 == 1 else F(1, 30)
assert day == 24 and done == 1
Q(T, "Alternate days", I,
  "A can finish a job in 20 days and B in 30 days. They work on alternate days, A starting on the first day. "
  "On which day will the job be completed?",
  "24th day", ["12th day", "23rd day", "25th day"],
  "Work in 2-day cycles, then finish the remainder day by day",
  "Take the job as 60 units: A does 3 units a day and B 2. Each 2-day cycle does 5 units, so 11 cycles (22 days) "
  "do 55 units. On day 23, A does 3 more (58), and on day 24 B does the last 2 units.",
  ["Work = 60 units; A = 3/day, B = 2/day", "One 2-day cycle = 5 units", "11 cycles = 22 days ⇒ 55 units",
   "Day 23 (A): 58 units", "Day 24 (B): 60 units, so the job finishes on day 24"],
  why="12 days is the time if both worked together every day; 23rd day forgets that A's 3 units on day 23 do not "
      "finish the job.", secs=60)

w_total = 12 * 18
d = F(w_total, 4 * F(3, 2) + 12)
assert d == 12
Q(T, "Men-women-children", I,
  "8 men or 12 women can complete a project in 18 days. In how many days will 4 men and 12 women complete it "
  "together?",
  "12 days", ["9 days", "13.5 days", "15 days"],
  "Convert everyone into one kind of worker",
  "8 men = 12 women, so 1 man = 1.5 women. 4 men + 12 women = 6 + 12 = 18 women. The work is 12 × 18 = 216 "
  "woman-days, so 18 women take 216 ÷ 18 = 12 days.",
  ["1 man = 12/8 = 1.5 women", "4 men + 12 women = 6 + 12 = 18 women", "Work = 12 × 18 = 216 woman-days",
   "Time = 216 ÷ 18 = 12 days"],
  why="9 days treats 4 men + 12 women as twice the original team; 13.5 days converts women into men the wrong way.",
  secs=55)

abc = (F(1, 24) + F(1, 30) + F(1, 40)) / 2
rem = 1 - 10 * abc
d = 10 + rem / F(1, 30)
assert abc == F(1, 20) and rem == F(1, 2) and d == 25
Q(T, "Work efficiency", A,
  "A and B can complete a work in 24 days, B and C in 30 days, and C and A in 40 days. All three work together for "
  "10 days, after which A leaves. B and C finish the remaining work. How many days does the whole work take?",
  "25 days", ["15 days", "20 days", "30 days"],
  "Adding the three pair-rates gives twice the combined rate",
  "Take the work as 120 units: A + B = 5, B + C = 4, C + A = 3 units per day. So A + B + C = 12 ÷ 2 = 6 units a day. "
  "In 10 days they do 60 units; B and C finish the other 60 at 4 units a day in 15 days. Total = 25 days.",
  ["Work = LCM(24, 30, 40) = 120 units", "A + B = 5, B + C = 4, C + A = 3 ⇒ 2(A + B + C) = 12 ⇒ A + B + C = 6",
   "10 days × 6 = 60 units", "Remaining 60 units at B + C = 4 units/day ⇒ 15 days", "Total = 10 + 15 = 25 days"],
  why="15 days is only the time B and C take after A leaves; 20 days is the time all three would take together.",
  secs=100)

c_rate = F(1, 6) - F(1, 16) - F(1, 24)
c_sh = F(9600) * 6 * c_rate
assert c_rate == F(1, 16) and c_sh == 3600 and F(9600) * 6 * F(1, 24) == 2400
Q(T, "Work and wages", A,
  "A can finish a job in 16 days and B in 24 days. With the help of C, the three finish it in 6 days and are paid "
  "₹9,600 in total. What is C's share of the payment?",
  "₹3,600", ["₹3,200", "₹2,400", "₹4,800"],
  "Find C's rate from the combined rate; wages follow the work done",
  "In 6 days A does 6/16 = 3/8 of the work and B does 6/24 = 1/4. C does the rest: 1 − 3/8 − 1/4 = 3/8. "
  "C's share = 3/8 × 9,600 = ₹3,600.",
  ["A's work in 6 days = 6/16 = 3/8", "B's work in 6 days = 6/24 = 1/4", "C's work = 1 − 3/8 − 2/8 = 3/8",
   "C's share = 3/8 × 9,600 = 3,600"],
  why="₹3,200 splits equally; ₹2,400 is B's share; ₹4,800 gives C half the work.", secs=80)

# ================================================================ Pipes and Cisterns (B1 I2 A1)
T = "Pipes and Cisterns"
h = 1 / (F(1, 12) - F(1, 18))
assert h == 36
Q(T, "Inlet and outlet", B,
  "Pipe A can fill a tank in 12 hours and pipe B can empty the full tank in 18 hours. If both are opened together "
  "when the tank is empty, in how many hours will it be full?",
  "36 hours", ["7.2 hours", "6 hours", "30 hours"],
  "Net rate = filling rate − emptying rate",
  "Take the tank as 36 units: A fills 3 units an hour and B empties 2, a net of 1 unit an hour. The tank fills in "
  "36 hours.",
  ["Capacity = LCM(12, 18) = 36 units", "A = +3/hour, B = −2/hour", "Net = 1 unit/hour", "Time = 36 hours"],
  why="7.2 hours adds the two rates as if both pipes were filling.", secs=35)

filled = 10 * (F(1, 20) + F(1, 30) - F(1, 15))
more = (1 - filled) / (F(1, 20) + F(1, 30))
assert filled == F(1, 6) and more == 10
Q(T, "Inlet and outlet", I,
  "Pipes A and B can fill a tank in 20 minutes and 30 minutes, while pipe C can empty it in 15 minutes. All three are "
  "opened on an empty tank, and after 10 minutes pipe C is closed. How many more minutes will it take to fill the "
  "tank?",
  "10 minutes", ["12 minutes", "8 minutes", "15 minutes"],
  "Work in units; switch rates when a pipe is closed",
  "Take the tank as 60 units: A = 3, B = 2 and C = −4 units a minute. With all three open the tank gains 1 unit a "
  "minute, so 10 units in 10 minutes. The remaining 50 units at 5 units a minute take 10 more minutes.",
  ["Capacity = 60 units; A = 3, B = 2, C = −4 per minute", "All open: net 1 unit/min × 10 min = 10 units",
   "Remaining = 50 units", "A + B = 5 units/min ⇒ 50 ÷ 5 = 10 minutes"],
  why="12 minutes is the time A and B need for an empty tank; it ignores the 10 units already filled.", secs=60)

leak = 1 / (F(1, 6) - F(2, 15))
assert leak == 30
Q(T, "Leak problems", I,
  "A pipe can fill a tank in 6 hours. Because of a leak at the bottom, it takes 7½ hours to fill the tank. In how "
  "many hours can the leak empty the full tank?",
  "30 hours", ["1.5 hours", "13.5 hours", "45 hours"],
  "Leak rate = rate without leak − rate with leak",
  "Take the tank as 30 units. The pipe fills 5 units an hour; with the leak only 30 ÷ 7.5 = 4 units an hour. So the "
  "leak removes 1 unit an hour and empties the tank in 30 hours.",
  ["Capacity = 30 units (LCM of 6 and 7.5)", "Pipe: 30 ÷ 6 = 5 units/hour", "With leak: 30 ÷ 7.5 = 4 units/hour",
   "Leak = 1 unit/hour ⇒ 30 hours"],
  short="ab/(b − a) = 6 × 7.5 ÷ 1.5 = 30.",
  why="1.5 hours is just the delay (7.5 − 6); 13.5 hours adds the two times.", secs=50)

cap = [c for c in range(60, 20000, 60) if F(c, 6 * 60) - 4 == F(c, 8 * 60)]
assert cap == [5760]
Q(T, "Leak problems", A,
  "A leak can empty a full tank in 6 hours. An inlet pipe that fills water at 4 litres per minute is opened at the "
  "moment the tank is full, and the tank now empties in 8 hours. What is the capacity of the tank?",
  "5,760 litres", ["1,440 litres", "1,920 litres", "2,880 litres"],
  "Equate the net outflow rates and convert hours to minutes",
  "Let the capacity be C litres. The leak drains C/360 litres a minute. With the inlet, the net drain is C/480 a "
  "minute, so C/360 − 4 = C/480. This gives C/1440 = 4, so C = 5,760 litres.",
  ["Leak rate = C ÷ 360 L/min", "Net rate with inlet = C ÷ 480 L/min", "C/360 − C/480 = 4 ⇒ C (4 − 3)/1440 = 4",
   "C = 5,760 litres"],
  why="1,440 and 1,920 litres are 4 L/min × 6 h and × 8 h, which is only what the inlet supplies in that time.",
  secs=90)

# ================================================================ Speed, Time and Distance (B2 I2 A2)
T = "Speed, Time and Distance"
avg = F(2 * 60 * 40, 60 + 40)
assert avg == 48
Q(T, "Average speed", B,
  "A courier van goes from a bank's head office to a branch at 60 km/h and returns along the same road at 40 km/h. "
  "What is its average speed for the whole trip?",
  "48 km/h", ["50 km/h", "45 km/h", "52 km/h"],
  "Average speed for equal distances = 2xy ÷ (x + y)",
  "Average speed = total distance ÷ total time. For equal distances this is 2 × 60 × 40 ÷ (60 + 40) = 4,800 ÷ 100 = "
  "48 km/h.",
  ["Let each way be 120 km", "Time = 120/60 + 120/40 = 2 + 3 = 5 hours", "Average = 240 ÷ 5 = 48 km/h"],
  why="50 km/h is the simple average of the two speeds, which is wrong because more time is spent at the slower "
      "speed.", secs=35)

t = F(360, 50 + 70)
assert t == 3 and F(360, 20) == 18
Q(T, "Relative speed", B,
  "Two cars start at the same time from two towns 360 km apart and drive towards each other at 50 km/h and 70 km/h. "
  "After how long will they meet?",
  "3 hours", ["18 hours", "7.2 hours", "6 hours"],
  "Objects moving towards each other: relative speed = sum of speeds",
  "They close the gap at 50 + 70 = 120 km/h, so they meet after 360 ÷ 120 = 3 hours.",
  ["Relative speed = 50 + 70 = 120 km/h", "Time = 360 ÷ 120 = 3 hours"],
  why="18 hours uses the difference of the speeds (for the same direction); 7.2 hours uses only one car's speed.",
  secs=30)

lead = 9 * F(15, 60)
t = lead / (12 - 9)
dist = 12 * t
assert lead == F(9, 4) and t == F(3, 4) and dist == 9 and 9 * t == F(27, 4)
Q(T, "Meeting and overtaking", I,
  "A thief runs away at 9 km/h. A guard starts chasing him 15 minutes later at 12 km/h along the same road. "
  "How far will the guard have run when he catches the thief?",
  "9 km", ["6.75 km", "2.25 km", "12 km"],
  "Chasing: time to catch = lead ÷ relative speed",
  "In 15 minutes the thief gets 9 × ¼ = 2.25 km ahead. The guard gains 12 − 9 = 3 km/h, so he takes 2.25 ÷ 3 = "
  "¾ hour and runs 12 × ¾ = 9 km.",
  ["Lead = 9 × 15/60 = 2.25 km", "Relative speed = 12 − 9 = 3 km/h", "Time = 2.25 ÷ 3 = 0.75 hour",
   "Guard's distance = 12 × 0.75 = 9 km"],
  why="6.75 km is the distance the thief runs during the chase; 2.25 km is only his lead.", secs=55)

avg = 3 / (F(1, 30) + F(1, 40) + F(1, 60))
assert avg == 40
Q(T, "Average speed", I,
  "A cyclist covers the first third of a route at 30 km/h, the second third at 40 km/h and the last third at "
  "60 km/h. What is the average speed for the whole route?",
  "40 km/h", ["43⅓ km/h", "45 km/h", "42 km/h"],
  "For equal distances, average speed is the harmonic mean of the speeds",
  "Take each third as 120 km (LCM of 30, 40, 60). Times: 4 h, 3 h and 2 h, total 9 h for 360 km, so the average is "
  "40 km/h.",
  ["Each third = 120 km", "Times: 120/30 = 4 h, 120/40 = 3 h, 120/60 = 2 h", "Total = 360 km in 9 h",
   "Average = 360 ÷ 9 = 40 km/h"],
  why="43⅓ km/h is the simple average (30 + 40 + 60)/3, which applies only to equal times, not equal distances.",
  secs=55)

sb = 36 * F(3, 4)
assert math.isqrt(16) * 3 == 4 * math.isqrt(9) and sb == 27 and 36 * F(9, 16) == F(81, 4)
Q(T, "Meeting and overtaking", A,
  "Two trucks start at the same time from cities P and Q towards each other. After they meet, the first truck takes "
  "9 hours to reach Q and the second takes 16 hours to reach P. If the first truck's speed is 36 km/h, what is the "
  "speed of the second truck?",
  "27 km/h", ["20.25 km/h", "48 km/h", "24 km/h"],
  "After meeting: S₁ : S₂ = √t₂ : √t₁",
  "S₁/S₂ = √(16/9) = 4/3. So S₂ = 36 × 3/4 = 27 km/h.",
  ["Let them meet after t hours: S₁t = 16S₂ and S₂t = 9S₁", "Dividing: S₁/S₂ = 16S₂/(9S₁) ⇒ (S₁/S₂)² = 16/9",
   "S₁/S₂ = 4/3", "S₂ = 36 × 3/4 = 27 km/h", "Check: t = 12 h; 36 × 12 = 432 = 27 × 16 and 27 × 12 = 324 = 36 × 9"],
  why="20.25 km/h uses the ratio 16 : 9 without the square root; 48 km/h inverts the ratio.", secs=90)
assert 36 * 12 == 27 * 16 and 27 * 12 == 36 * 9

meet_h = F(340 - 40 * 1, 40 + 60)
clock = 9 + meet_h
assert meet_h == 3 and clock == 12 and 8 + F(340, 100) == F(114, 10)
Q(T, "Meeting and overtaking", A,
  "Town X and town Y are 340 km apart. Bus A leaves X at 8:00 AM towards Y at 40 km/h. Bus B leaves Y at 9:00 AM "
  "towards X at 60 km/h. At what time do the two buses meet?",
  "12:00 noon", ["11:24 AM", "11:00 AM", "12:24 PM"],
  "Head start, then relative speed of approach",
  "By 9:00 AM bus A has covered 40 km, leaving 300 km. The buses then close the gap at 40 + 60 = 100 km/h, taking "
  "3 hours. They meet at 12:00 noon, 160 km from X.",
  ["8 to 9 AM: A covers 40 km; gap = 340 − 40 = 300 km", "Relative speed = 40 + 60 = 100 km/h",
   "Time after 9 AM = 300 ÷ 100 = 3 hours", "Meeting time = 12:00 noon",
   "Check: A covers 40 × 4 = 160 km, B covers 60 × 3 = 180 km; total 340 km"],
  why="11:24 AM assumes both buses started at 8:00 AM (340 ÷ 100 = 3.4 h).", secs=80)

# ================================================================ Boats and Streams (B1 I1 A1)
T = "Boats and Streams"
t = F(36, 15 + 3) + F(36, 15 - 3)
assert t == 5 and F(72, 15) == F(24, 5)
Q(T, "Upstream and downstream", B,
  "A boat's speed in still water is 15 km/h and the stream flows at 3 km/h. How long will the boat take to go 36 km "
  "downstream and come back?",
  "5 hours", ["4.8 hours", "4 hours", "6 hours"],
  "Downstream speed = boat + stream; upstream speed = boat − stream",
  "Downstream speed = 18 km/h, so 36 km takes 2 hours. Upstream speed = 12 km/h, so 36 km takes 3 hours. Total = "
  "5 hours.",
  ["Downstream = 15 + 3 = 18 km/h ⇒ 36 ÷ 18 = 2 h", "Upstream = 15 − 3 = 12 km/h ⇒ 36 ÷ 12 = 3 h", "Total = 5 h"],
  why="4.8 hours ignores the stream (72 ÷ 15).", secs=35)

up, down = F(48, 6), F(72, 4)
assert (up, down) == (8, 18) and (down - up) / 2 == 5 and (down + up) / 2 == 13
Q(T, "Speed of stream", I,
  "A motor boat covers 48 km upstream in 6 hours and 72 km downstream in 4 hours. What is the speed of the stream?",
  "5 km/h", ["13 km/h", "10 km/h", "4 km/h"],
  "Stream speed = (downstream − upstream) ÷ 2",
  "Upstream speed = 48 ÷ 6 = 8 km/h and downstream speed = 72 ÷ 4 = 18 km/h. Stream = (18 − 8) ÷ 2 = 5 km/h.",
  ["Upstream = 8 km/h", "Downstream = 18 km/h", "Stream = (18 − 8)/2 = 5 km/h"],
  why="13 km/h is the boat's speed in still water; 10 km/h forgets to halve the difference.", secs=45)

s_ = [s for s in [F(k, 2) for k in range(1, 29)] if F(60, 15 - s) - F(60, 15 + s) == 3]
assert s_ == [5]
rt = F(60, 10) + F(60, 20)
assert rt == 9
Q(T, "Speed of stream", A,
  "A boat with a speed of 15 km/h in still water takes 3 hours longer to cover 60 km upstream than to cover 60 km "
  "downstream. How long will it take to go 60 km upstream and return?",
  "9 hours", ["8 hours", "6 hours", "10 hours"],
  "Form an equation in the stream speed, then compute both legs",
  "60/(15 − s) − 60/(15 + s) = 3 gives 120s = 3(225 − s²), i.e. s² + 40s − 225 = 0, so s = 5 km/h. Upstream speed "
  "10 km/h (6 h), downstream 20 km/h (3 h): 9 hours in all.",
  ["60/(15 − s) − 60/(15 + s) = 3", "60 × 2s = 3(225 − s²) ⇒ s² + 40s − 225 = 0", "(s − 5)(s + 45) = 0 ⇒ s = 5 km/h",
   "Upstream: 60 ÷ 10 = 6 h; downstream: 60 ÷ 20 = 3 h", "Round trip = 9 hours"],
  short="Try the options' implied speeds: s = 5 gives 6 h and 3 h, a gap of exactly 3 h.",
  why="8 hours ignores the stream (120 ÷ 15); 6 hours is only the upstream leg.", secs=100)

# ================================================================ Problems on Trains (B1 I1 A1)
T = "Problems on Trains"
v = F(54 * 5, 18)
t = (240 + 210) / v
assert v == 15 and t == 30
Q(T, "Crossing a pole or platform", B,
  "A train 240 m long runs at 54 km/h. How long will it take to cross a platform 210 m long?",
  "30 seconds", ["16 seconds", "14 seconds", "25 seconds"],
  "Crossing a platform: distance = train length + platform length",
  "54 km/h = 15 m/s. The train must cover 240 + 210 = 450 m, which takes 450 ÷ 15 = 30 seconds.",
  ["Speed = 54 × 5/18 = 15 m/s", "Distance = 240 + 210 = 450 m", "Time = 450 ÷ 15 = 30 s"],
  why="16 seconds counts only the train's length; 14 seconds counts only the platform.", secs=35)

rel = F((50 + 40) * 5, 18)
t = (180 + 220) / rel
assert rel == 25 and t == 16 and (180 + 220) / F(10 * 5, 18) == 144
Q(T, "Trains crossing each other", I,
  "Two trains 180 m and 220 m long run on parallel tracks in opposite directions at 50 km/h and 40 km/h. How long "
  "will they take to cross each other completely?",
  "16 seconds", ["144 seconds", "8 seconds", "20 seconds"],
  "Opposite directions: add the speeds; distance = sum of lengths",
  "Relative speed = 90 km/h = 25 m/s. The distance is 180 + 220 = 400 m, so the time is 400 ÷ 25 = 16 seconds.",
  ["Relative speed = 50 + 40 = 90 km/h = 25 m/s", "Distance = 180 + 220 = 400 m", "Time = 400 ÷ 25 = 16 s"],
  why="144 seconds subtracts the speeds (same direction); 8 seconds uses 200 m instead of the sum of the lengths; "
      "20 seconds uses only the 50 km/h train's speed.", secs=45)

sol = [(L, v) for v in range(1, 60) for L in [12 * v] if L + 300 == 27 * v]
assert sol == [(240, 20)]
t = F(240 + 360, 20 + 10)
assert t == 20 and F(600, 10) == 60 and F(600, 20) == 30
Q(T, "Trains crossing each other", A,
  "A train crosses a signal pole in 12 seconds and a 300 m platform in 27 seconds. How long will it take to cross "
  "another train 360 m long coming from the opposite direction at 36 km/h?",
  "20 seconds", ["60 seconds", "30 seconds", "24 seconds"],
  "Find the train's length and speed from two crossings, then use relative speed",
  "The extra 300 m takes 27 − 12 = 15 s, so the speed is 20 m/s and the length is 20 × 12 = 240 m. The other train "
  "moves at 36 km/h = 10 m/s towards it, so the relative speed is 30 m/s. Time = (240 + 360) ÷ 30 = 20 s.",
  ["Speed = 300 ÷ (27 − 12) = 20 m/s", "Length = 20 × 12 = 240 m", "Other train: 36 × 5/18 = 10 m/s",
   "Relative speed (opposite) = 20 + 10 = 30 m/s", "Time = (240 + 360) ÷ 30 = 600 ÷ 30 = 20 s"],
  why="60 seconds subtracts the speeds (same direction); 30 seconds ignores the other train's speed.", secs=90)

# ================================================================ Mensuration (B2 I2 A2)
T = "Mensuration"
b_ = 76 // 2 - 24
assert b_ == 14 and 24 * b_ == 336 and 24 * 19 == 456 and 24 * 26 == 624 and 24 * 28 == 672
Q(T, "2D areas and perimeters", B,
  "The perimeter of a rectangular plot is 76 m and its length is 24 m. What is its area?",
  "336 m²", ["456 m²", "624 m²", "672 m²"],
  "Perimeter = 2(l + b); area = l × b",
  "l + b = 76 ÷ 2 = 38, so b = 38 − 24 = 14 m. Area = 24 × 14 = 336 m².",
  ["2(l + b) = 76 ⇒ l + b = 38", "b = 38 − 24 = 14 m", "Area = 24 × 14 = 336 m²"],
  why="456 m² takes the breadth as 76 ÷ 4 (a square); 624 m² forgets to halve the perimeter correctly, taking "
      "b = (76 − 24) ÷ 2.", secs=35)

l_, w_, h_ = 12, 8, 5
tsa = 2 * (l_ * w_ + w_ * h_ + h_ * l_)
assert tsa == 392 and l_ * w_ * h_ == 480 and 2 * (l_ + w_) * h_ == 200
Q(T, "3D volume and surface area", B,
  "A closed wooden box measures 12 cm × 8 cm × 5 cm. What is its total surface area?",
  "392 cm²", ["480 cm²", "196 cm²", "200 cm²"],
  "Total surface area of a cuboid = 2(lb + bh + hl)",
  "TSA = 2(12 × 8 + 8 × 5 + 5 × 12) = 2(96 + 40 + 60) = 2 × 196 = 392 cm².",
  ["lb = 96, bh = 40, hl = 60", "Sum = 196", "TSA = 2 × 196 = 392 cm²"],
  why="480 is the volume (in cm³); 196 forgets the factor 2; 200 is the area of the four side faces only.", secs=35)

pi = F(22, 7)
r, h = 7, 20
tsa = 2 * pi * r * (r + h)
assert tsa == 1188 and 2 * pi * r * h == 880 and pi * r * r * h == 3080 and 880 + pi * 49 == 1034
Q(T, "Cylinder, cone and sphere", I,
  "A closed cylindrical water tank has a radius of 7 m and a height of 20 m. What is its total surface area? "
  "(Use π = 22/7.)",
  "1,188 m²", ["880 m²", "1,034 m²", "3,080 m²"],
  "TSA of a closed cylinder = 2πr(r + h)",
  "TSA = 2 × 22/7 × 7 × (7 + 20) = 44 × 27 = 1,188 m².",
  ["2πr = 2 × 22/7 × 7 = 44", "r + h = 27", "TSA = 44 × 27 = 1,188 m²"],
  why="880 m² is the curved surface only; 1,034 m² adds only one circular end; 3,080 is the volume.", secs=45)

area = pi * (F(35, 2) ** 2 - 14 ** 2)
assert area == F(3465, 10) and 2 * pi * 14 * F(7, 2) == 308 and 2 * pi * F(35, 2) * F(7, 2) == 385
Q(T, "2D areas and perimeters", I,
  "A circular garden has a radius of 14 m. A path 3.5 m wide runs around it on the outside. What is the area of the "
  "path? (Use π = 22/7.)",
  "346.5 m²", ["308 m²", "385 m²", "154 m²"],
  "Area of a ring = π(R² − r²)",
  "Outer radius = 14 + 3.5 = 17.5 m. Area = 22/7 × (17.5² − 14²) = 22/7 × (306.25 − 196) = 22/7 × 110.25 = "
  "346.5 m².",
  ["R = 14 + 3.5 = 17.5 m", "R² − r² = 306.25 − 196 = 110.25", "Area = 22/7 × 110.25 = 346.5 m²"],
  short="R² − r² = (R + r)(R − r) = 31.5 × 3.5 = 110.25.",
  why="308 m² multiplies the inner circumference by the width; 385 m² uses the outer circumference instead.",
  secs=55)

sphere = F(4, 3) * 6 ** 3
cone = F(1, 3) * 3 ** 2 * 4
assert sphere / cone == 24 and sphere / (3 ** 2 * 4) == 8
Q(T, "Cylinder, cone and sphere", A,
  "A solid metal sphere of radius 6 cm is melted and recast into small solid cones, each of base radius 3 cm and "
  "height 4 cm. How many cones are made?",
  "24", ["8", "18", "72"],
  "Volume is conserved when a solid is melted and recast",
  "Sphere volume = 4/3 π × 216 = 288π. Cone volume = 1/3 π × 9 × 4 = 12π. Number of cones = 288π ÷ 12π = 24.",
  ["Sphere = 4/3 × π × 6³ = 288π cm³", "Cone = 1/3 × π × 3² × 4 = 12π cm³", "Number = 288 ÷ 12 = 24"],
  why="8 forgets the 1/3 in the cone's volume; 18 forgets the 4/3 in the sphere's volume.", secs=80)

flow = pi * F(7, 100) ** 2 * 15000
need = F(50 * 44 * 21, 100)
assert flow == 231 and need == 462 and need / flow == 2 and need / (pi * F(14, 100) ** 2 * 15000) == F(1, 2)
Q(T, "Cylinder, cone and sphere", A,
  "Water flows through a cylindrical pipe of internal diameter 14 cm at 15 km/h into a rectangular tank 50 m long "
  "and 44 m wide. How long will it take for the water level in the tank to rise by 21 cm? (Use π = 22/7.)",
  "2 hours", ["30 minutes", "1 hour", "4 hours"],
  "Volume delivered per hour = cross-section area × length of water column per hour",
  "Pipe radius = 7 cm = 0.07 m. Each hour a 15,000 m column flows in: 22/7 × 0.07² × 15,000 = 231 m³. The tank needs "
  "50 × 44 × 0.21 = 462 m³, so the time is 462 ÷ 231 = 2 hours.",
  ["Radius = 0.07 m; area = 22/7 × 0.0049 = 0.0154 m²", "Flow per hour = 0.0154 × 15,000 = 231 m³",
   "Volume needed = 50 × 44 × 0.21 = 462 m³", "Time = 462 ÷ 231 = 2 hours"],
  why="30 minutes uses 14 cm as the radius instead of the diameter (four times the area).", secs=110)

# ================================================================ Probability (B2 I2 A2)
T = "Probability"
dice = list(itertools.product(range(1, 7), repeat=2))
p = F(sum(1 for a, b in dice if a + b == 8), 36)
assert p == F(5, 36)
Q(T, "Coins and dice", B, "Two fair dice are rolled together. What is the probability that the sum of the numbers is 8?",
  "5/36", ["1/6", "1/9", "7/36"],
  "Probability = favourable outcomes ÷ total outcomes (36 for two dice)",
  "The favourable outcomes are (2, 6), (3, 5), (4, 4), (5, 3) and (6, 2): 5 of 36.",
  ["Total outcomes = 6 × 6 = 36", "Sum 8: (2,6), (3,5), (4,4), (5,3), (6,2) = 5 outcomes", "P = 5/36"],
  why="1/6 (= 6/36) is the probability of a sum of 7; 1/9 counts only 4 outcomes, missing one ordered pair.",
  secs=35)

bag = ["R"] * 5 + ["B"] * 4 + ["G"] * 3
p = F(sum(1 for c in bag if c != "B"), len(bag))
assert p == F(2, 3)
Q(T, "Balls from bags", B,
  "A bag contains 5 red, 4 blue and 3 green balls. One ball is drawn at random. What is the probability that it is "
  "not blue?",
  "2/3", ["1/3", "5/12", "3/4"],
  "P(not A) = 1 − P(A)",
  "P(blue) = 4/12 = 1/3, so P(not blue) = 1 − 1/3 = 2/3.",
  ["Total balls = 12", "P(blue) = 4/12 = 1/3", "P(not blue) = 2/3"],
  why="1/3 is the probability of blue; 5/12 counts only red balls.", secs=30)

deck = [(s, r) for s in "HSDC" for r in range(13)]
pairs = list(itertools.combinations(deck, 2))
p = F(sum(1 for a, b in pairs if {a[0], b[0]} == {"H", "S"}), len(pairs))
assert p == F(13, 102) and len(pairs) == 1326
Q(T, "Cards", I,
  "Two cards are drawn together at random from a well-shuffled pack of 52 cards. What is the probability that one "
  "is a heart and the other is a spade?",
  "13/102", ["1/16", "13/204", "1/8"],
  "Selections without replacement: count with combinations",
  "Ways to pick one heart and one spade = 13 × 13 = 169. Ways to pick any 2 cards = ⁵²C₂ = 1,326. "
  "P = 169/1,326 = 13/102.",
  ["Favourable = ¹³C₁ × ¹³C₁ = 169", "Total = ⁵²C₂ = 52 × 51 ÷ 2 = 1,326", "P = 169/1,326 = 13/102"],
  why="1/16 and 1/8 treat the draws as with replacement; 13/204 counts only the order 'heart first, then spade' "
      "within an unordered total.", secs=55)

balls = ["R"] * 6 + ["W"] * 4
tri = list(itertools.combinations(range(10), 3))
p = F(sum(1 for t_ in tri if sum(balls[i] == "R" for i in t_) == 2), len(tri))
assert p == F(1, 2) and 3 * F(6, 10) ** 2 * F(4, 10) == F(54, 125)
assert F(6, 10) * F(5, 9) * F(4, 8) == F(1, 6) and F(math.comb(6, 2), math.comb(10, 3)) == F(1, 8)
Q(T, "Balls from bags", I,
  "A box has 6 red and 4 white tokens. Three tokens are drawn at random without replacement. What is the probability "
  "that exactly two of them are red?",
  "1/2", ["54/125", "1/6", "1/8"],
  "Hypergeometric selection: choose the reds and the whites separately",
  "Ways = ⁶C₂ × ⁴C₁ = 15 × 4 = 60. Total = ¹⁰C₃ = 120. P = 60/120 = 1/2.",
  ["⁶C₂ = 15 ways to choose 2 red", "⁴C₁ = 4 ways to choose 1 white", "Favourable = 60; total = ¹⁰C₃ = 120",
   "P = 60/120 = 1/2"],
  why="54/125 treats the draws as with replacement (3 × 0.6² × 0.4); 1/6 counts only one order, red-red-white "
      "(6/10 × 5/9 × 4/8); 1/8 forgets the factor ⁴C₁ = 4 for the white token (15/120).", secs=55)

sum_prime = {(a, b) for a, b in dice if a + b in (2, 3, 5, 7, 11)}
prod6 = {(a, b) for a, b in dice if (a * b) % 6 == 0}
p = F(len(sum_prime | prod6), 36)
assert (len(sum_prime), len(prod6), len(sum_prime & prod6)) == (15, 15, 8) and p == F(11, 18)
Q(T, "Coins and dice", A,
  "Two fair dice are thrown. What is the probability that the sum of the numbers is a prime number or the product "
  "of the numbers is a multiple of 6?",
  "11/18", ["5/6", "5/12", "2/9"],
  "P(A or B) = P(A) + P(B) − P(A and B)",
  "Sum prime: 15 outcomes. Product a multiple of 6: 15 outcomes. Both: 8 outcomes. So the union has 15 + 15 − 8 = "
  "22 outcomes and P = 22/36 = 11/18.",
  ["Sum prime (2, 3, 5, 7, 11): 1 + 2 + 4 + 6 + 2 = 15 outcomes",
   "Product multiple of 6: 20 outcomes contain a 3 or 6; remove the 5 with both numbers odd ⇒ 15",
   "Both: sum 5 → (2,3), (3,2); sum 7 → (1,6), (6,1), (3,4), (4,3); sum 11 → (5,6), (6,5) = 8",
   "Union = 15 + 15 − 8 = 22", "P = 22/36 = 11/18"],
  why="5/6 adds the two counts without subtracting the 8 common outcomes; 5/12 counts only one event; 2/9 counts "
      "only the overlap.", secs=120)

pa = F(3, 8) * F(5, 9) + F(5, 8) * F(4, 9)
assert pa == F(35, 72) and (F(3, 8) + F(1, 2)) / 2 == F(7, 16)
Q(T, "Balls from bags", A,
  "Bag X contains 3 red and 5 black balls; bag Y contains 4 red and 4 black balls. One ball is drawn at random from "
  "X and put into Y without looking at it. Then a ball is drawn from Y. What is the probability that this ball is "
  "red?",
  "35/72", ["1/2", "7/16", "37/72"],
  "Total probability: split on the colour of the transferred ball",
  "If a red ball is moved (probability 3/8), Y has 5 red of 9; if a black ball is moved (5/8), Y has 4 red of 9. "
  "P = 3/8 × 5/9 + 5/8 × 4/9 = 15/72 + 20/72 = 35/72.",
  ["Red transferred: P = 3/8; then P(red from Y) = 5/9", "Black transferred: P = 5/8; then P(red from Y) = 4/9",
   "P = 3/8 × 5/9 + 5/8 × 4/9", "= 15/72 + 20/72 = 35/72"],
  why="1/2 ignores the transfer; 7/16 averages the two bags' red proportions; 37/72 swaps 5/9 and 4/9 between the "
      "two cases.", secs=100)
assert F(3, 8) * F(4, 9) + F(5, 8) * F(5, 9) == F(37, 72)

# ================================================================ Permutation and Combination (B1 I1 A1)
T = "Permutation and Combination"
ways = math.comb(6, 2) * math.comb(5, 2)
assert ways == 150 and math.comb(11, 4) == 330
Q(T, "Selections", B,
  "A committee of 4 is to be formed from 6 men and 5 women so that it has exactly 2 men and 2 women. In how many "
  "ways can this be done?",
  "150", ["25", "330", "300"],
  "Independent selections multiply: ⁿCᵣ × ᵐCₛ",
  "Choose 2 men in ⁶C₂ = 15 ways and 2 women in ⁵C₂ = 10 ways. Total = 15 × 10 = 150.",
  ["⁶C₂ = 15", "⁵C₂ = 10", "Total = 15 × 10 = 150"],
  why="25 adds the two counts instead of multiplying; 330 = ¹¹C₄ ignores the 2-and-2 condition; 300 counts "
      "ordered pairs.", secs=35)

word = "BANKER"
arr = set(itertools.permutations(word))
good = sum(1 for p_ in arr if abs(p_.index("A") - p_.index("E")) == 1)
assert len(arr) == 720 and good == 240
Q(T, "Word arrangements", I,
  "In how many ways can the letters of the word BANKER be arranged so that the vowels always come together?",
  "240", ["120", "720", "480"],
  "Treat the vowels as one block, then arrange inside the block",
  "The vowels A and E form one block. With B, N, K, R this gives 5 units: 5! = 120 arrangements. The vowels can be "
  "ordered inside the block in 2! = 2 ways. Total = 240.",
  ["Letters: B, A, N, K, E, R (all different); vowels A, E", "Units = (AE), B, N, K, R ⇒ 5! = 120",
   "Arrangements inside the block = 2! = 2", "Total = 120 × 2 = 240"],
  why="120 forgets the 2 internal orders (AE and EA); 720 is the number of arrangements with no restriction.",
  secs=45)

kids = ["B1", "B2", "B3", "B4", "G1", "G2", "G3"]
ok = sum(1 for p_ in itertools.permutations(kids)
         if all(not (p_[i][0] == "G" and p_[i + 1][0] == "G") for i in range(6)))
assert ok == 1440 == math.factorial(4) * math.perm(5, 3) and math.factorial(4) * math.comb(5, 3) == 240
Q(T, "Arrangements", A,
  "In how many ways can 4 boys and 3 girls sit in a row of 7 chairs so that no two girls sit next to each other?",
  "1,440", ["240", "720", "2,880"],
  "Gap method: seat the unrestricted people first, then place the others in the gaps",
  "Seat the 4 boys in 4! = 24 ways. They create 5 gaps (including both ends). Place the 3 girls in 3 different gaps "
  "in ⁵P₃ = 60 ways. Total = 24 × 60 = 1,440.",
  ["Boys: 4! = 24 ways", "Gaps: _B_B_B_B_ = 5 gaps", "Girls in 3 of the 5 gaps, in order: ⁵P₃ = 5 × 4 × 3 = 60",
   "Total = 24 × 60 = 1,440"],
  why="240 uses ⁵C₃ and forgets that the girls are different people who can swap seats; 720 is 6!, from treating "
      "the girls as one block.", secs=90)

# ================================================================ Tabular DI (B3 I4 A3): two sets of 5
T = "Tabular DI"
LOANS = {"Nagpur": (120, 45, 30, 55), "Indore": (150, 60, 25, 65), "Patna": (90, 35, 40, 35),
         "Kochi": (180, 70, 45, 55), "Surat": (110, 40, 20, 30)}
cols = ["Home", "Car", "Education", "Personal"]
sid = stimulus("data_table", "Loans disbursed by five branches in 2025-26",
               "The table shows the loans disbursed (in ₹ crore) by five branches of a bank in the financial year "
               "2025-26, by type of loan.\n\n" +
               md_table(["Branch", *cols], [[b, *v] for b, v in LOANS.items()]),
               {"columns": ["branch", *[c.lower() for c in cols]], "rows": [[b, *v] for b, v in LOANS.items()]})
tot = {b: sum(v) for b, v in LOANS.items()}
car = sum(v[1] for v in LOANS.values())
assert car == 250 and tot == {"Nagpur": 250, "Indore": 300, "Patna": 200, "Kochi": 350, "Surat": 200}
Q(T, "Single table", B, "What is the total amount of car loans disbursed by all five branches together?",
  "₹250 crore", ["₹240 crore", "₹260 crore", "₹245 crore"],
  "Column total",
  "Add the Car column: 45 + 60 + 35 + 70 + 40 = 250, i.e. ₹250 crore.",
  ["45 + 60 = 105", "105 + 35 = 140", "140 + 70 = 210", "210 + 40 = 250"], secs=30, stim=sid)

p = F(40, tot["Patna"]) * 100
assert p == 20 and F(40, 160) * 100 == 25 and F(40, 250) * 100 == 16
Q(T, "Single table", B,
  "Education loans at the Patna branch form what percentage of all loans disbursed by the Patna branch?",
  "20%", ["25%", "16%", "22.5%"],
  "Part ÷ whole × 100, with the branch total as the whole",
  "Patna's total = 90 + 35 + 40 + 35 = 200. Education loans = 40, so the share is 40 ÷ 200 × 100 = 20%.",
  ["Patna total = 90 + 35 + 40 + 35 = 200", "Share = 40 ÷ 200 × 100 = 20%"],
  why="25% divides by the other three loan types only (160); 16% divides by the wrong row total (Nagpur's 250).",
  secs=35, stim=sid)

num = LOANS["Nagpur"][3] + LOANS["Indore"][3]
den = LOANS["Patna"][2] + LOANS["Kochi"][2]
assert (num, den) == (120, 85) and ratio(num, den) == "24 : 17"
Q(T, "Single table", I,
  "What is the ratio of the personal loans disbursed by Nagpur and Indore together to the education loans "
  "disbursed by Patna and Kochi together?",
  "24 : 17", ["17 : 24", "11 : 8", "24 : 19"],
  "Ratio of two sums",
  "Personal loans of Nagpur and Indore = 55 + 65 = 120. Education loans of Patna and Kochi = 40 + 45 = 85. "
  "120 : 85 = 24 : 17.",
  ["Personal (Nagpur + Indore) = 55 + 65 = 120", "Education (Patna + Kochi) = 40 + 45 = 85",
   "120 : 85 = 24 : 17 (divide by 5)"],
  why="17 : 24 is the ratio reversed.", secs=45, stim=sid)

home_avg = F(sum(v[0] for v in LOANS.values()), 5)
car_avg = F(car, 5)
pm = (home_avg - car_avg) / car_avg * 100
assert home_avg == 130 and car_avg == 50 and pm == 160 and near((home_avg - car_avg) / home_avg * 100, 61.538, 1e-3)
Q(T, "Single table", I,
  "By what percentage is the average home loan disbursed per branch more than the average car loan disbursed per "
  "branch?",
  "160%", ["61.54%", "260%", "80%"],
  "Percentage more = difference ÷ base × 100, with the car-loan average as the base",
  "Average home loan = 650 ÷ 5 = 130 and average car loan = 250 ÷ 5 = 50. The excess is 80, which is 160% of 50.",
  ["Home total = 120 + 150 + 90 + 180 + 110 = 650 ⇒ average 130", "Car total = 250 ⇒ average 50",
   "Difference = 80", "80 ÷ 50 × 100 = 160%"],
  short="Averages over the same 5 branches compare like totals: (650 − 250) ÷ 250 = 160%.",
  why="61.54% uses the home-loan average as the base; 260% is the ratio 130 ÷ 50 expressed as a percentage.",
  secs=55, stim=sid)

h, c, e, pl = LOANS["Kochi"]
new_k = h * F(120, 100) + c * F(90, 100) + e + pl
pct = new_k / (tot["Patna"] + tot["Surat"]) * 100
assert new_k == 379 and pct == F(9475, 100) and F(350, 400) * 100 == F(875, 10) and F(386, 400) * 100 == F(965, 10)
Q(T, "Single table", A,
  "In 2026-27, Kochi's home loans grow by 20% and its car loans fall by 10% over 2025-26, while its other loans stay "
  "the same. Kochi's total loans in 2026-27 will be what percentage of the combined 2025-26 loans of Patna and "
  "Surat?",
  "94.75%", ["87.5%", "96.5%", "92.75%"],
  "Apply each change to its own category, then compare totals",
  "New home = 180 × 1.2 = 216 and new car = 70 × 0.9 = 63, so Kochi's new total = 216 + 63 + 45 + 55 = 379. "
  "Patna + Surat = 200 + 200 = 400. 379 ÷ 400 × 100 = 94.75%.",
  ["Home: 180 × 1.20 = 216", "Car: 70 × 0.90 = 63", "New total = 216 + 63 + 45 + 55 = 379",
   "Patna + Surat (2025-26) = 400", "379 ÷ 400 × 100 = 94.75%"],
  why="87.5% uses Kochi's unchanged total (350); 96.5% applies the home-loan rise but forgets the fall in car "
      "loans.", secs=90, stim=sid)

COMP = {"P": (1600, 35, 25), "Q": (2000, 40, 30), "R": (1200, 45, 20), "S": (2500, 32, 50), "T": (1800, 25, 40)}
sid = stimulus("data_table", "Employees and women in tech roles at five companies",
               "The table gives the total number of employees of five companies, the percentage of employees who are "
               "women, and the percentage of those women who work in technology roles.\n\n" +
               md_table(["Company", "Total employees", "Women (% of employees)", "Women in tech roles (% of women)"],
                        [[k, ind(n), w, t_] for k, (n, w, t_) in COMP.items()]),
               {"columns": ["company", "employees", "women_pct", "women_tech_pct_of_women"],
                "rows": [[k, *v] for k, v in COMP.items()]})
women = {k: n * F(w, 100) for k, (n, w, _) in COMP.items()}
tech = {k: women[k] * F(t_, 100) for k, (_, _, t_) in COMP.items()}
assert women == {"P": 560, "Q": 800, "R": 540, "S": 800, "T": 450}
assert tech == {"P": 140, "Q": 240, "R": 108, "S": 400, "T": 180}
men_r = COMP["R"][0] - women["R"]
assert men_r == 660
Q(T, "Table with percentages", B, "How many men are employed in company R?",
  "660", ["540", "720", "600"],
  "Men = total × (100 − women%)",
  "Women are 45% of 1,200 = 540, so men = 1,200 − 540 = 660.",
  ["Women in R = 45% of 1,200 = 540", "Men = 1,200 − 540 = 660"],
  why="540 is the number of women; 720 uses 60% for men.", secs=30, stim=sid)

pm = (tech["S"] - tech["Q"]) / tech["Q"] * 100
assert near(pm, 66.6667, 1e-3) and (tech["S"] - tech["Q"]) / tech["S"] * 100 == 40
Q(T, "Table with percentages", I,
  "The number of women in tech roles in company S is what percent more than that in company Q?",
  "66⅔%", ["40%", "20%", "166⅔%"],
  "Two-level percentages, then 'percent more than' on the right base",
  "Women in tech: S = 50% of (32% of 2,500) = 400; Q = 30% of (40% of 2,000) = 240. S has 160 more, which is "
  "160/240 = 66⅔% more than Q.",
  ["S: women = 800; in tech = 50% of 800 = 400", "Q: women = 800; in tech = 30% of 800 = 240",
   "Difference = 160", "160 ÷ 240 × 100 = 66⅔%"],
  why="40% uses S (400) as the base; 20% subtracts the percentages 50 − 30; 166⅔% is 400 as a percentage of 240.",
  secs=55, stim=sid)

nt = {k: women[k] - tech[k] for k in COMP}
assert nt == {"P": 420, "Q": 560, "R": 432, "S": 400, "T": 270} and ratio(nt["P"], nt["Q"]) == "3 : 4"
Q(T, "Table with percentages", I,
  "What is the ratio of the number of women not in tech roles in company P to that in company Q?",
  "3 : 4", ["7 : 10", "7 : 8", "4 : 3"],
  "Complement percentages applied to the number of women",
  "P: women = 560, 75% not in tech = 420. Q: women = 800, 70% not in tech = 560. 420 : 560 = 3 : 4.",
  ["P: 35% of 1,600 = 560 women; 75% of 560 = 420", "Q: 40% of 2,000 = 800 women; 70% of 800 = 560",
   "420 : 560 = 3 : 4"],
  why="7 : 10 is the ratio of all women (560 : 800); 7 : 8 applies Q's women percentage (40%) instead of its "
      "non-tech share (70%), giving 420 : 480; 4 : 3 is reversed.", secs=55, stim=sid)
assert ratio(560, 800) == "7 : 10" and ratio(420, 800 * F(60, 100)) == "7 : 8"

avg = F(sum(nt.values()), 5)
assert avg == F(4164, 10) and F(sum(women.values()), 5) == 630 and F(sum(tech.values()), 5) == F(2136, 10)
Q(T, "Table with percentages", A,
  "What is the average number of women working in non-tech roles across the five companies?",
  "416.4", ["630", "213.6", "420"],
  "Average of derived values computed per company",
  "Women not in tech: P 420, Q 560, R 432, S 400, T 270. Total = 2,082, so the average is 2,082 ÷ 5 = 416.4.",
  ["P: 560 × 75% = 420", "Q: 800 × 70% = 560", "R: 540 × 80% = 432", "S: 800 × 50% = 400", "T: 450 × 60% = 270",
   "Total = 2,082; average = 416.4"],
  why="630 is the average number of all women; 213.6 is the average number of women in tech roles.", secs=90, stim=sid)

men_t = COMP["T"][0] - women["T"]
share = tech["T"] / (tech["T"] + men_t * F(20, 100)) * 100
assert men_t == 1350 and share == 40
Q(T, "Table with percentages", A,
  "If 20% of the men in company T also work in tech roles, what percentage of company T's tech-role employees are "
  "women?",
  "40%", ["25%", "13⅓%", "60%"],
  "Build the tech-role group from both genders before taking the share",
  "T has 450 women, 180 of them in tech. Men = 1,800 − 450 = 1,350, and 20% of them = 270 are in tech. Tech "
  "employees = 180 + 270 = 450, of whom women are 180/450 = 40%.",
  ["Women in T = 25% of 1,800 = 450; in tech = 40% of 450 = 180", "Men = 1,350; in tech = 20% of 1,350 = 270",
   "Tech employees = 180 + 270 = 450", "Women's share = 180 ÷ 450 × 100 = 40%"],
  why="25% is the share of women among all employees of T; 13⅓% divides 180 by all men; 60% is the men's share.",
  secs=90, stim=sid)

# ================================================================ Bar Graph DI (B2 I3 A2): sets of 4 and 3
T = "Bar Graph DI"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
SALES = [450, 520, 600, 380, 550, 500]
sid = stimulus("chart", "Two-wheelers sold by a dealer, January to June",
               "The bar graph shows the number of two-wheelers sold by a dealer in each month from January to June. "
               "The values are given below.\n\n" + md_table(["Month", "Units sold"], list(zip(MONTHS, SALES))),
               {"chart": "bar", "x": MONTHS, "series": [{"name": "Units sold", "values": SALES}]})
avg = F(sum(SALES), 6)
assert avg == 500
Q(T, "Simple bar", B, "What is the average number of two-wheelers sold per month over the six months?",
  "500", ["520", "480", "550"],
  "Average = total ÷ number of months",
  "Total = 450 + 520 + 600 + 380 + 550 + 500 = 3,000, so the monthly average is 3,000 ÷ 6 = 500.",
  ["Total = 3,000", "Average = 3,000 ÷ 6 = 500"], secs=35, stim=sid)

less = F(600 - 380, 600) * 100
assert near(less, 36.6667, 1e-3) and near(F(220, 380) * 100, 57.89, 1e-2)
Q(T, "Simple bar", B, "The sales in April were what percent less than the sales in March?",
  "36⅔%", ["57.89%", "63⅓%", "22%"],
  "Percent less than = difference ÷ the larger (reference) value × 100",
  "March = 600 and April = 380. The fall of 220 is 220/600 = 36⅔% of March's sales.",
  ["Difference = 600 − 380 = 220", "220 ÷ 600 × 100 = 36⅔%"],
  why="57.89% divides by April's sales; 63⅓% is April as a percentage of March.", secs=40, stim=sid)

odd = SALES[0] + SALES[2] + SALES[4]
even = SALES[1] + SALES[3] + SALES[5]
assert (odd, even) == (1600, 1400) and ratio(odd, even) == "8 : 7"
Q(T, "Simple bar", I,
  "What is the ratio of the combined sales of January, March and May to the combined sales of February, April and "
  "June?",
  "8 : 7", ["7 : 8", "4 : 3", "16 : 13"],
  "Ratio of two sums",
  "January + March + May = 450 + 600 + 550 = 1,600. February + April + June = 520 + 380 + 500 = 1,400. "
  "1,600 : 1,400 = 8 : 7.",
  ["450 + 600 + 550 = 1,600", "520 + 380 + 500 = 1,400", "1,600 : 1,400 = 8 : 7"],
  why="7 : 8 is reversed.", secs=45, stim=sid)

above = [m for m, s_ in zip(MONTHS, SALES) if s_ > avg]
assert above == ["Feb", "Mar", "May"]
Q(T, "Simple bar", I,
  "In how many of the six months were the sales strictly more than the six-month average?",
  "3", ["2", "4", "1"],
  "Compare each month with the average",
  "The average is 500. Sales above 500 were in February (520), March (600) and May (550): 3 months. June (500) "
  "equals the average and does not count.",
  ["Average = 3,000 ÷ 6 = 500", "Above 500: Feb 520, Mar 600, May 550", "Jun = 500 is not more than 500",
   "Answer = 3"],
  why="4 counts June, whose sales equal the average.", secs=50, stim=sid)

YEARS = ["2021", "2022", "2023", "2024", "2025"]
X = [240, 300, 280, 360, 420]
Y = [200, 260, 320, 300, 380]
sid = stimulus("chart", "Deposits mobilised by branches X and Y, 2021-2025",
               "The grouped bar graph shows the deposits (in ₹ lakh) mobilised by two branches, X and Y, of a bank in "
               "each year from 2021 to 2025. The values are given below.\n\n" +
               md_table(["Year", "Branch X", "Branch Y"], list(zip(YEARS, X, Y))),
               {"chart": "grouped_bar", "x": YEARS,
                "series": [{"name": "Branch X", "values": X}, {"name": "Branch Y", "values": Y}]})
growth = {YEARS[i]: F(X[i] - X[i - 1], X[i - 1]) for i in range(1, 5)}
best = max(growth, key=growth.get)
assert best == "2024" and growth["2024"] == F(2, 7) and growth["2022"] == F(1, 4)
assert max(range(1, 5), key=lambda i: X[i] - X[i - 1]) in (3,)  # 2024 also has the largest absolute rise here
Q(T, "Stacked or grouped bar", I,
  "In which year did branch X record the highest percentage increase in deposits over the previous year?",
  "2024", ["2022", "2025", "2023"],
  "Percentage change = change ÷ previous year's value",
  "X's year-on-year changes: 2022: 60/240 = 25%; 2023: −20/300 = −6.67%; 2024: 80/280 = 28.57%; 2025: 60/360 = "
  "16.67%. The highest is in 2024.",
  ["2022: (300 − 240)/240 = 25%", "2023: (280 − 300)/300 = −6.67%", "2024: (360 − 280)/280 = 28.57%",
   "2025: (420 − 360)/360 = 16.67%", "Highest: 2024"],
  why="2022 and 2025 have the same absolute rise of 60, but on larger or smaller bases; 2022's 25% is still below "
      "2024's 28.57%.", secs=60, stim=sid)

pct = F(sum(Y), sum(X)) * 100
assert sum(X) == 1600 and sum(Y) == 1460 and pct == F(9125, 100)
Q(T, "Stacked or grouped bar", A,
  "The total deposits mobilised by branch Y over the five years are what percentage of the total deposits mobilised "
  "by branch X over the same period?",
  "91.25%", ["109.59%", "8.75%", "92.5%"],
  "Ratio of totals as a percentage",
  "Y's total = 200 + 260 + 320 + 300 + 380 = 1,460. X's total = 240 + 300 + 280 + 360 + 420 = 1,600. "
  "1,460 ÷ 1,600 × 100 = 91.25%.",
  ["Y total = 1,460", "X total = 1,600", "1,460 ÷ 1,600 × 100 = 91.25%"],
  why="109.59% is X as a percentage of Y; 8.75% is the gap (140) as a percentage of X.", secs=75, stim=sid)
assert near(F(1600, 1460) * 100, 109.589, 1e-3)

late = X[3] + Y[3] + X[4] + Y[4]
early = X[0] + Y[0] + X[1] + Y[1]
pm = F(late - early, early) * 100
assert (late, early) == (1460, 1000) and pm == 46
Q(T, "Stacked or grouped bar", A,
  "The combined deposits of both branches in 2024 and 2025 together are what percent more than their combined "
  "deposits in 2021 and 2022 together?",
  "46%", ["31.51%", "146%", "41%"],
  "Sum four bars on each side, then compute the percentage increase on the earlier total",
  "2024 + 2025: 360 + 300 + 420 + 380 = 1,460. 2021 + 2022: 240 + 200 + 300 + 260 = 1,000. The increase of 460 is "
  "46% of 1,000.",
  ["2024: 360 + 300 = 660; 2025: 420 + 380 = 800 ⇒ 1,460", "2021: 240 + 200 = 440; 2022: 300 + 260 = 560 ⇒ 1,000",
   "Increase = 460", "460 ÷ 1,000 × 100 = 46%"],
  why="31.51% divides by the later total (1,460); 146% is the later total as a percentage of the earlier one.",
  secs=80, stim=sid)

# ================================================================ Pie Chart DI (B2 I3 A2): sets of 4 and 3
T = "Pie Chart DI"
EXP = {"Rent": 90, "Food": 72, "Education": 54, "Transport": 36, "Savings": 63, "Others": 45}
assert sum(EXP.values()) == 360
INCOME = 72000
sid = stimulus("chart", "A family's monthly budget (central angles)",
               "The pie chart shows how a family divides its monthly income of ₹72,000. The central angle of each "
               "sector is given below.\n\n" + md_table(["Head", "Central angle (degrees)"], list(EXP.items())),
               {"chart": "pie", "unit": "degrees", "total_amount": INCOME,
                "series": [{"name": k, "value": v} for k, v in EXP.items()]})
amt = {k: F(v, 360) * INCOME for k, v in EXP.items()}
assert amt["Food"] == 14400
Q(T, "Degree-based", B, "How much does the family spend on food each month?",
  "₹14,400", ["₹18,000", "₹7,200", "₹12,960"],
  "Amount = (angle ÷ 360) × total",
  "Food has 72°, which is 72/360 = 1/5 of the income. 1/5 × 72,000 = ₹14,400.",
  ["Share = 72/360 = 1/5", "Amount = 72,000 ÷ 5 = 14,400"],
  why="₹18,000 is the rent (90°); ₹7,200 is transport (36°).", secs=30, stim=sid)

sp = F(EXP["Savings"], 360) * 100
assert sp == F(35, 2)
Q(T, "Degree-based", B, "What percentage of the monthly income does the family save?",
  "17.5%", ["63%", "12.6%", "15%"],
  "Percentage = angle ÷ 360 × 100",
  "Savings = 63°, so the share is 63 ÷ 360 × 100 = 17.5%.",
  ["63 ÷ 360 = 0.175", "0.175 × 100 = 17.5%"],
  why="63% reads the angle as a percentage; 12.6% divides by 500 instead of 360.", secs=30, stim=sid)

pm = F(EXP["Rent"] - EXP["Education"], EXP["Education"]) * 100
assert near(pm, 66.6667, 1e-3)
Q(T, "Degree-based", I, "The family's spending on rent is what percent more than its spending on education?",
  "66⅔%", ["40%", "36%", "50%"],
  "Percentages can be compared directly from the angles",
  "Rent = 90° and education = 54°. The excess is 36°, which is 36/54 = 66⅔% of education.",
  ["Difference = 90 − 54 = 36°", "36 ÷ 54 × 100 = 66⅔%"],
  why="40% uses rent as the base (36/90); 36% reads the angle difference as a percentage.", secs=45, stim=sid)

diff = (amt["Rent"] + amt["Transport"]) - (amt["Education"] + amt["Others"])
assert diff == 5400
Q(T, "Degree-based", I,
  "By how many rupees does the family's spending on rent and transport together exceed its spending on education "
  "and others together?",
  "₹5,400", ["₹14,400", "₹16,200", "₹2,700"],
  "Work with angles first, convert to rupees once",
  "Rent + transport = 90° + 36° = 126°. Education + others = 54° + 45° = 99°. The gap of 27° is 27/360 × 72,000 = "
  "₹5,400.",
  ["126° − 99° = 27°", "1° = 72,000 ÷ 360 = ₹200", "27 × 200 = ₹5,400"],
  short="Each degree is ₹200, so the answer is just 27 × 200.",
  why="₹14,400 leaves out 'Others' (126° − 54° = 72°); ₹16,200 leaves out education (126° − 45° = 81°); ₹2,700 "
      "takes 1° as ₹100.", secs=50, stim=sid)
assert 72 * 200 == 14400 and 81 * 200 == 16200 and 27 * 100 == 2700

TOTAL_ST, TOTAL_G = 3600, 1500
ST = {"Commerce": 30, "Science": 25, "Arts": 20, "Management": 15, "Law": 10}
GI = {"Commerce": 28, "Science": 20, "Arts": 32, "Management": 12, "Law": 8}
assert sum(ST.values()) == 100 == sum(GI.values())
sid = stimulus("chart", "Students and girls by stream in a college",
               f"Pie chart 1 shows the distribution of all {ind(TOTAL_ST)} students of a college across five streams. "
               f"Pie chart 2 shows the distribution of the {ind(TOTAL_G)} girls among them across the same streams. "
               "All other students are boys.\n\n" +
               md_table(["Stream", "All students (%)", "Girls (%)"], [[s, ST[s], GI[s]] for s in ST]),
               {"chart": "two_pies",
                "pies": [{"title": "All students", "total": TOTAL_ST,
                          "series": [{"name": s, "value": v} for s, v in ST.items()]},
                         {"title": "Girls", "total": TOTAL_G,
                          "series": [{"name": s, "value": v} for s, v in GI.items()]}]})
stu = {s: TOTAL_ST * F(v, 100) for s, v in ST.items()}
girls = {s: TOTAL_G * F(v, 100) for s, v in GI.items()}
boys = {s: stu[s] - girls[s] for s in ST}
assert boys == {"Commerce": 660, "Science": 600, "Arts": 240, "Management": 360, "Law": 240}
assert ratio(boys["Science"], girls["Arts"]) == "5 : 4"
Q(T, "Two pie charts", I,
  "What is the ratio of the number of boys in Science to the number of girls in Arts?",
  "5 : 4", ["4 : 5", "25 : 32", "15 : 8"],
  "Boys in a stream = students in the stream − girls in the stream",
  "Science students = 25% of 3,600 = 900; Science girls = 20% of 1,500 = 300; so Science boys = 600. Arts girls = "
  "32% of 1,500 = 480. 600 : 480 = 5 : 4.",
  ["Science: 900 students − 300 girls = 600 boys", "Arts girls = 32% of 1,500 = 480", "600 : 480 = 5 : 4"],
  why="4 : 5 is reversed; 25 : 32 compares the two percentages, which are of different totals.", secs=60, stim=sid)

pct = (girls["Science"] + girls["Law"]) / (boys["Arts"] + boys["Law"]) * 100
assert pct == F(875, 10)
Q(T, "Two pie charts", A,
  "The number of girls in Science and Law together is what percentage of the number of boys in Arts and Law "
  "together?",
  "87.5%", ["114.29%", "46.67%", "80%"],
  "Derive boys stream-wise from the two charts, then take the percentage",
  "Girls: Science 300 + Law 120 = 420. Boys: Arts 720 − 480 = 240 and Law 360 − 120 = 240, total 480. "
  "420 ÷ 480 × 100 = 87.5%.",
  ["Girls in Science = 300; in Law = 8% of 1,500 = 120 ⇒ 420", "Arts: 720 students − 480 girls = 240 boys",
   "Law: 360 students − 120 girls = 240 boys", "Boys (Arts + Law) = 480", "420 ÷ 480 × 100 = 87.5%"],
  why="114.29% is the inverse (480 ÷ 420); 46.67% uses all Arts and Law students (900) as the base.", secs=90,
  stim=sid)
assert near(F(480, 420) * 100, 114.2857, 1e-3) and near(F(420, 900) * 100, 46.6667, 1e-3)

placed = girls["Management"] * F(25, 100) + boys["Management"] * F(40, 100)
pct = placed / stu["Management"] * 100
assert placed == 189 and pct == 35
Q(T, "Two pie charts", A,
  "If 25% of the girls and 40% of the boys in the Management stream got campus placements, what percentage of all "
  "Management students got placed?",
  "35%", ["32.5%", "38%", "30%"],
  "Weighted percentage over girls and boys of one stream",
  "Management has 540 students, of whom 180 are girls and 360 boys. Placed = 25% of 180 + 40% of 360 = 45 + 144 = "
  "189, which is 189/540 = 35%.",
  ["Management students = 15% of 3,600 = 540", "Girls = 12% of 1,500 = 180; boys = 360",
   "Placed = 45 + 144 = 189", "189 ÷ 540 × 100 = 35%"],
  why="32.5% is the simple average of 25% and 40%, ignoring that there are twice as many boys as girls.", secs=90,
  stim=sid)

# ================================================================ Line Graph DI (B2 I3 A2): sets of 4 and 3
T = "Line Graph DI"
YRS = ["2019", "2020", "2021", "2022", "2023", "2024", "2025"]
PROFIT = [40, 48, 42, 56, 70, 63, 80]
sid = stimulus("chart", "Annual profit of a company, 2019-2025",
               "The line graph shows the annual profit (in ₹ lakh) of a company from 2019 to 2025. The plotted values "
               "are given below.\n\n" + md_table(["Year", "Profit (₹ lakh)"], list(zip(YRS, PROFIT))),
               {"chart": "line", "x": YRS, "series": [{"name": "Profit (₹ lakh)", "values": PROFIT}]})
assert F(70 - 56, 56) * 100 == 25 and F(14, 70) * 100 == 20
Q(T, "Single line", B, "By what percentage did the profit increase from 2022 to 2023?",
  "25%", ["20%", "14%", "30%"],
  "Percentage increase = increase ÷ earlier value × 100",
  "Profit rose from 56 to 70, an increase of 14. 14 ÷ 56 × 100 = 25%.",
  ["Increase = 70 − 56 = 14", "14 ÷ 56 × 100 = 25%"],
  why="20% uses 2023 as the base (14 ÷ 70); 14% reads the increase in lakh as a percentage.", secs=30, stim=sid)

avg = F(sum(PROFIT), 7)
assert avg == 57
Q(T, "Single line", B, "What is the average annual profit of the company over the seven years?",
  "₹57 lakh", ["₹56 lakh", "₹60 lakh", "₹63 lakh"],
  "Average = total ÷ number of years",
  "Total = 40 + 48 + 42 + 56 + 70 + 63 + 80 = 399, so the average is 399 ÷ 7 = ₹57 lakh.",
  ["Total = 399", "Average = 399 ÷ 7 = 57"],
  why="₹60 lakh averages only the first and last years ((40 + 80) ÷ 2).", secs=40, stim=sid)

margin = F(70, 280 + 70) * 100
assert margin == 20 and F(70, 280) * 100 == 25
Q(T, "Single line", I,
  "In 2023 the company's expenses were ₹280 lakh, and profit = income − expenses. What was the profit as a "
  "percentage of income in 2023?",
  "20%", ["25%", "80%", "22.5%"],
  "Income = expenses + profit; margin on income",
  "Income = 280 + 70 = ₹350 lakh. Profit as a percentage of income = 70 ÷ 350 × 100 = 20%.",
  ["2023 profit = 70", "Income = 280 + 70 = 350", "70 ÷ 350 × 100 = 20%"],
  why="25% divides the profit by the expenses instead of the income; 80% is the expenses' share of income.",
  secs=50, stim=sid)

chg = {YRS[i]: F(PROFIT[i] - PROFIT[i - 1], PROFIT[i - 1]) for i in range(1, 7)}
best = max(chg, key=lambda y_: abs(chg[y_]))
assert best == "2022" and chg["2022"] == F(1, 3) and max(range(1, 7), key=lambda i: PROFIT[i] - PROFIT[i - 1]) == 6
Q(T, "Single line", I,
  "In which year was the percentage change in profit over the previous year the largest (ignoring whether it was a "
  "rise or a fall)?",
  "2022", ["2025", "2023", "2020"],
  "Compare percentage changes, not absolute changes",
  "Changes: 2020 +20%, 2021 −12.5%, 2022 +33⅓%, 2023 +25%, 2024 −10%, 2025 +26.98%. The largest is 2022.",
  ["2020: 8/40 = 20%", "2021: −6/48 = −12.5%", "2022: 14/42 = 33⅓%", "2023: 14/56 = 25%", "2024: −7/70 = −10%",
   "2025: 17/63 ≈ 26.98%", "Largest: 2022"],
  why="2025 has the largest absolute rise (17 lakh), but on a bigger base; 2022 and 2023 have the same rise of 14, "
      "and 2022's base is smaller.", secs=70, stim=sid)

YR5 = ["2021", "2022", "2023", "2024", "2025"]
MADE = [50, 60, 75, 80, 95]
SOLD = [45, 54, 60, 72, 84]
sid = stimulus("chart", "Units manufactured and sold, 2021-2025",
               "The line graph shows the number of units (in thousands) of a product manufactured and sold by a "
               "company each year from 2021 to 2025. The plotted values are given below.\n\n" +
               md_table(["Year", "Manufactured ('000)", "Sold ('000)"], list(zip(YR5, MADE, SOLD))),
               {"chart": "line", "x": YR5, "series": [{"name": "Manufactured ('000)", "values": MADE},
                                                      {"name": "Sold ('000)", "values": SOLD}]})
assert F(60, 75) * 100 == 80
Q(T, "Multiple lines", I, "What percentage of the units manufactured in 2023 were sold in 2023?",
  "80%", ["125%", "20%", "75%"],
  "Sold ÷ manufactured × 100",
  "In 2023, 75 thousand units were made and 60 thousand sold. 60 ÷ 75 × 100 = 80%.",
  ["Manufactured = 75, sold = 60 (thousand)", "60 ÷ 75 × 100 = 80%"],
  why="125% inverts the ratio; 20% is the unsold share.", secs=40, stim=sid)

unsold = sum(MADE) - sum(SOLD)
pct = F(unsold, sum(MADE)) * 100
assert (sum(MADE), sum(SOLD), unsold) == (360, 315, 45) and pct == F(25, 2)
Q(T, "Multiple lines", A,
  "Over the five years, the total number of unsold units is what percentage of the total number of units "
  "manufactured?",
  "12.5%", ["14.29%", "87.5%", "11.11%"],
  "Gap between two lines, summed over the period",
  "Total manufactured = 360 thousand and total sold = 315 thousand, so 45 thousand were unsold. "
  "45 ÷ 360 × 100 = 12.5%.",
  ["Manufactured: 50 + 60 + 75 + 80 + 95 = 360", "Sold: 45 + 54 + 60 + 72 + 84 = 315", "Unsold = 45",
   "45 ÷ 360 × 100 = 12.5%"],
  why="14.29% divides by the units sold (315); 87.5% is the sold share.", secs=75, stim=sid)

rev = SOLD[3] * 1000 * 2500 + (MADE[2] - SOLD[2]) * 1000 * 2000
assert rev == 210_000_000 and (SOLD[3] + 15) * 1000 * 2500 == 217_500_000
Q(T, "Multiple lines", A,
  "Each unit sells at ₹2,500. In 2024 the company also cleared all the units left unsold in 2023 at a 20% discount. "
  "What was its total revenue in 2024 from these two sources?",
  "₹21 crore", ["₹21.75 crore", "₹18 crore", "₹20.4 crore"],
  "Revenue = units × price; the unsold units of a year are the gap between the two lines",
  "Regular sales in 2024 = 72,000 × 2,500 = ₹18 crore. Unsold in 2023 = 75,000 − 60,000 = 15,000 units, cleared at "
  "₹2,000 each = ₹3 crore. Total = ₹21 crore.",
  ["2024 sales: 72,000 × ₹2,500 = ₹18,00,00,000", "2023 unsold = 75,000 − 60,000 = 15,000 units",
   "Clearance price = 80% of 2,500 = ₹2,000", "Clearance revenue = 15,000 × 2,000 = ₹3,00,00,000",
   "Total = ₹21 crore"],
  why="₹21.75 crore ignores the 20% discount; ₹18 crore leaves out the clearance sale.", secs=100, stim=sid)

# ================================================================ Caselet DI (B3 I4 A3): two sets of 5
T = "Caselet DI"
TOTAL_C = 1200
SHARE = {"S": 40, "F": 15, "C": 10, "SF": 12, "SC": 8, "FC": 5}
SHARE["SFC"] = 100 - sum(SHARE.values())
cnt = {k: TOTAL_C * F(v, 100) for k, v in SHARE.items()}
assert SHARE["SFC"] == 10 and cnt == {"S": 480, "F": 180, "C": 120, "SF": 144, "SC": 96, "FC": 60, "SFC": 120}
sid = stimulus("caselet", "Products held by customers of a branch",
               "A bank branch has 1,200 customers, and each of them holds at least one of three products: a savings "
               "account, a fixed deposit (FD) and a credit card. 40% of the customers hold only a savings account, 15% "
               "hold only an FD and 10% hold only a credit card. 12% hold a savings account and an FD but no credit "
               "card, 8% hold a savings account and a credit card but no FD, and 5% hold an FD and a credit card but "
               "no savings account. The remaining customers hold all three products.")
Q(T, "Paragraph data", B, "How many customers of the branch hold all three products?",
  "120", ["108", "144", "96"],
  "The 'remaining' group is 100% minus all the listed groups",
  "The listed groups add up to 40 + 15 + 10 + 12 + 8 + 5 = 90%, so 10% hold all three: 10% of 1,200 = 120.",
  ["Listed groups = 90%", "All three = 100 − 90 = 10%", "10% of 1,200 = 120"], secs=35, stim=sid)

fd = cnt["F"] + cnt["SF"] + cnt["FC"] + cnt["SFC"]
assert fd == 504
Q(T, "Paragraph data", B, "How many customers hold a fixed deposit?",
  "504", ["180", "384", "444"],
  "Every region of the Venn diagram that includes FD",
  "FD holders = only FD (180) + savings and FD (144) + FD and card (60) + all three (120) = 504.",
  ["Only FD = 15% = 180", "Savings + FD only = 12% = 144", "FD + card only = 5% = 60", "All three = 120",
   "Total = 504"],
  why="180 counts only those with FD alone; 384 leaves out those with all three products.", secs=40, stim=sid)

two = cnt["SF"] + cnt["SC"] + cnt["FC"]
assert two == 300
Q(T, "Paragraph data", I, "How many customers hold exactly two of the three products?",
  "300", ["420", "360", "240"],
  "'Exactly two' excludes those holding all three",
  "Exactly two = 12% + 8% + 5% = 25% of 1,200 = 300.",
  ["Savings + FD only = 144", "Savings + card only = 96", "FD + card only = 60", "Total = 300"],
  why="420 also counts the 120 customers with all three products.", secs=45, stim=sid)

sav = cnt["S"] + cnt["SF"] + cnt["SC"] + cnt["SFC"]
cc = cnt["C"] + cnt["SC"] + cnt["FC"] + cnt["SFC"]
assert (sav, cc) == (840, 396) and ratio(sav, cc) == "70 : 33"
Q(T, "Paragraph data", I,
  "What is the ratio of the number of customers holding a savings account to the number holding a credit card?",
  "70 : 33", ["33 : 70", "4 : 1", "35 : 18"],
  "Total holders of a product = sum of every region containing it",
  "Savings: 480 + 144 + 96 + 120 = 840. Credit card: 120 + 96 + 60 + 120 = 396. 840 : 396 = 70 : 33.",
  ["Savings holders = 840", "Card holders = 396", "Divide both by 12: 70 : 33"],
  why="4 : 1 compares only the single-product groups (480 : 120); 33 : 70 is reversed.", secs=55, stim=sid)

new_two = two + cnt["S"] * F(25, 100)
pct = new_two / TOTAL_C * 100
assert new_two == 420 and pct == 35
Q(T, "Paragraph data", A,
  "Next month, 25% of the customers who hold only a savings account also open an FD, and nothing else changes. "
  "What percentage of the branch's customers will then hold exactly two products?",
  "35%", ["25%", "45%", "32%"],
  "Track which Venn region the moving customers leave and join",
  "25% of the 480 savings-only customers = 120 customers move from 'only savings' to 'savings and FD'. Exactly two "
  "becomes 300 + 120 = 420, which is 35% of 1,200.",
  ["Movers = 25% of 480 = 120", "They now hold savings + FD only (exactly two)", "Exactly two = 300 + 120 = 420",
   "420 ÷ 1,200 × 100 = 35%"],
  why="25% ignores the movers; 45% also includes the customers who hold all three.", secs=80, stim=sid)

TOT_PK = 1500
DOM = TOT_PK * F(60, 100)
INTL = TOT_PK - DOM
PK = {"Goa": DOM * F(35, 100), "Kerala": DOM * F(25, 100), "Dubai": INTL * F(40, 100),
      "Thailand": INTL * F(36, 100)}
PK["Himachal"] = DOM - PK["Goa"] - PK["Kerala"]
PK["Singapore"] = INTL - PK["Dubai"] - PK["Thailand"]
PRICE = {"Goa": 24000, "Kerala": 30000, "Himachal": 20000, "Dubai": 60000, "Thailand": 45000, "Singapore": 75000}
assert PK == {"Goa": 315, "Kerala": 225, "Dubai": 240, "Thailand": 216, "Himachal": 360, "Singapore": 144}
sid = stimulus("caselet", "Holiday packages sold by an online travel agency",
               "An online travel agency sold 1,500 holiday packages in a quarter. 60% of them were domestic and the "
               "rest international. Of the domestic packages, 35% were for Goa, 25% for Kerala and the rest for "
               "Himachal. Of the international packages, 40% were for Dubai, 36% for Thailand and the rest for "
               "Singapore. The average price per package was as follows.\n\n" +
               md_table(["Destination", "Average price per package (₹)"], [[d, ind(p_)] for d, p_ in PRICE.items()]))
Q(T, "Caselet with table", B, "How many packages for Himachal did the agency sell?",
  "360", ["315", "540", "400"],
  "Remainder share within the domestic group",
  "Domestic packages = 60% of 1,500 = 900. Himachal gets 100 − 35 − 25 = 40% of them: 360.",
  ["Domestic = 900", "Himachal share = 40%", "40% of 900 = 360"],
  why="315 is the Goa figure; 540 takes 60% of 900.", secs=35, stim=sid)

rev = {d: PK[d] * PRICE[d] for d in PK}
assert ratio(rev["Singapore"], rev["Dubai"]) == "3 : 4"
Q(T, "Caselet with table", I,
  "What is the ratio of the revenue from Singapore packages to the revenue from Dubai packages?",
  "3 : 4", ["3 : 5", "4 : 3", "5 : 4"],
  "Revenue = number of packages × average price",
  "Singapore: 144 × 75,000 = ₹1.08 crore. Dubai: 240 × 60,000 = ₹1.44 crore. 1.08 : 1.44 = 3 : 4.",
  ["International = 600; Singapore = 24% of 600 = 144; Dubai = 40% of 600 = 240",
   "Singapore revenue = 144 × 75,000 = 1,08,00,000", "Dubai revenue = 240 × 60,000 = 1,44,00,000", "Ratio = 3 : 4"],
  why="3 : 5 compares the number of packages only; 5 : 4 compares the prices only.", secs=55, stim=sid)

less = F(PK["Kerala"] - PK["Thailand"], PK["Kerala"]) * 100
assert less == 4 and near(F(9, 216) * 100, 4.1667, 1e-3)
Q(T, "Caselet with table", I,
  "The number of Thailand packages sold was what percent less than the number of Kerala packages sold?",
  "4%", ["4⅙%", "9%", "11%"],
  "Percent less = difference ÷ the reference (Kerala) × 100",
  "Kerala = 25% of 900 = 225 and Thailand = 36% of 600 = 216. The gap of 9 is 9/225 = 4% of Kerala's figure.",
  ["Kerala = 225", "Thailand = 216", "9 ÷ 225 × 100 = 4%"],
  why="4⅙% divides by Thailand's figure; 11% subtracts the two percentages (36 − 25), which are of different bases.",
  secs=55, stim=sid)

dom_rev = rev["Goa"] + rev["Kerala"] + rev["Himachal"]
avg = dom_rev / DOM
assert dom_rev == 21_510_000 and avg == 23900 and near(F(24000 + 30000 + 20000, 3), 24666.67, 1e-2)
Q(T, "Caselet with table", A, "What was the average revenue per domestic package?",
  "₹23,900", ["₹24,666.67", "₹23,000", "₹25,000"],
  "Weighted average price = total revenue ÷ total packages",
  "Goa: 315 × 24,000 = ₹75.6 lakh; Kerala: 225 × 30,000 = ₹67.5 lakh; Himachal: 360 × 20,000 = ₹72 lakh. Total = "
  "₹2,15,10,000 for 900 packages, i.e. ₹23,900 per package.",
  ["Goa = 315 × 24,000 = 75,60,000", "Kerala = 225 × 30,000 = 67,50,000", "Himachal = 360 × 20,000 = 72,00,000",
   "Total = 2,15,10,000", "÷ 900 = 23,900"],
  why="₹24,666.67 is the simple average of the three prices and ignores how many packages were sold at each.",
  secs=90, stim=sid)

intl_rev = rev["Dubai"] + rev["Thailand"] + rev["Singapore"]
comm = dom_rev * F(8, 100) + intl_rev * F(5, 100)
swapped = dom_rev * F(5, 100) + intl_rev * F(8, 100)
assert intl_rev == 34_920_000 and comm == 3_466_800 and swapped == 3_869_100 and intl_rev * F(5, 100) == 1_746_000
Q(T, "Caselet with table", A,
  "The agency earns a commission of 8% on domestic revenue and 5% on international revenue. What is its total "
  "commission for the quarter?",
  "₹34,66,800", ["₹38,69,100", "₹17,46,000", "₹36,67,950"],
  "Apply each rate to its own revenue base",
  "Domestic revenue = ₹2,15,10,000, so 8% = ₹17,20,800. International revenue = 1,44,00,000 + 97,20,000 + "
  "1,08,00,000 = ₹3,49,20,000, so 5% = ₹17,46,000. Total = ₹34,66,800.",
  ["Domestic commission = 8% of 2,15,10,000 = 17,20,800", "Thailand revenue = 216 × 45,000 = 97,20,000",
   "International revenue = 3,49,20,000; 5% = 17,46,000", "Total = 17,20,800 + 17,46,000 = 34,66,800"],
  why="₹38,69,100 swaps the two rates; ₹17,46,000 is the international commission alone; ₹36,67,950 applies the "
      "average rate 6.5% to all revenue.", secs=110, stim=sid)
assert (dom_rev + intl_rev) * F(65, 1000) == 3_667_950

# ================================================================ Missing DI (B2 I2 A2): two sets of 3
T = "Missing DI"
SHOP = {"A": (800, 120), "B": (750, 90), "C": (1200, 180), "D": (800, 64), "E": (1000, 92)}
shown = {"A": ("800", "15", "—", "—"), "B": ("—", "12", "90", "—"), "C": ("1,200", "—", "—", "1,020"),
         "D": ("—", "—", "64", "736"), "E": ("1,000", "—", "92", "—")}
for k, (sold, ret) in SHOP.items():
    sh = shown[k]
    if sh[1] != "—":
        assert F(ret, sold) * 100 == F(sh[1])
    if sh[3] != "—":
        assert sold - ret == int(sh[3].replace(",", ""))
sid = stimulus("data_table", "Items sold and returned at five electronics stores",
               "The table shows the number of items sold by five electronics stores in a month, the percentage and "
               "number of those items that customers returned, and the number of items kept (not returned). Some "
               "values are missing (—); find them from the others.\n\n" +
               md_table(["Store", "Items sold", "Returned (%)", "Items returned", "Items kept"],
                        [[k, *v] for k, v in shown.items()]))
b_sold = F(90) / F(12, 100)
assert b_sold == 750 and 90 * 12 == 1080
Q(T, "Table with missing values", B, "How many items did store B sell?",
  "750", ["1,080", "660", "780"],
  "Total = part ÷ percentage",
  "90 items are 12% of the items sold, so items sold = 90 ÷ 0.12 = 750.",
  ["12% of sold = 90", "Sold = 90 × 100 ÷ 12 = 750"],
  why="1,080 multiplies 90 by 12; 660 is the number of items kept.", secs=35, stim=sid)

d_pct = F(64, 64 + 736) * 100
assert d_pct == 8 and near(F(64, 736) * 100, 8.6957, 1e-3)
Q(T, "Table with missing values", B, "What percentage of the items sold by store D were returned?",
  "8%", ["8.7%", "7.5%", "9%"],
  "Items sold = returned + kept",
  "Store D sold 64 + 736 = 800 items, so the return rate is 64 ÷ 800 × 100 = 8%.",
  ["Sold = 64 + 736 = 800", "64 ÷ 800 × 100 = 8%"],
  why="8.7% divides by the items kept (736) instead of the items sold.", secs=35, stim=sid)

tot_s = sum(s_ for s_, _ in SHOP.values())
tot_r = sum(r_ for _, r_ in SHOP.values())
pct = F(tot_r, tot_s) * 100
simple = sum(F(r_, s_) * 100 for s_, r_ in SHOP.values()) / 5
assert (tot_s, tot_r) == (4550, 546) and pct == 12 and simple == F(1184, 100)
Q(T, "Table with missing values", A,
  "Taking all five stores together, what percentage of the items sold were returned?",
  "12%", ["11.84%", "13.64%", "88%"],
  "Overall rate = total returned ÷ total sold, after filling every missing cell",
  "Fill the gaps: A returned 15% of 800 = 120; B sold 750; C returned 1,200 − 1,020 = 180; D sold 800; E returned "
  "92 of 1,000. Total sold = 4,550 and total returned = 546, so the overall rate is 546 ÷ 4,550 = 12%.",
  ["A: 120 returned of 800", "B: 90 of 750", "C: 180 of 1,200", "D: 64 of 800", "E: 92 of 1,000",
   "Totals: 546 returned of 4,550 sold", "546 ÷ 4,550 × 100 = 12%"],
  why="11.84% averages the five stores' percentages without weighting by items sold; 13.64% divides by the items "
      "kept (4,004); 88% is the share kept.", secs=110, stim=sid)
assert near(F(546, 4004) * 100, 13.636, 1e-3)

SCH = {"S1": (25000, 8, 3), "S2": (24000, 10, 4), "S3": (40000, 7, 5), "S4": (32000, 9, 4)}
si = {k: F(p_ * r_ * t_, 100) for k, (p_, r_, t_) in SCH.items()}
assert si == {"S1": 6000, "S2": 9600, "S3": 14000, "S4": 11520}
shown = {"S1": ("25,000", "8", "3", "—"), "S2": ("—", "10", "4", "9,600"), "S3": ("40,000", "—", "5", "14,000"),
         "S4": ("32,000", "9", "—", "11,520")}
sid = stimulus("data_table", "Four simple-interest deposits with missing values",
               "The table gives details of four deposit schemes that pay simple interest. Some values are missing (—); "
               "find them from the others.\n\n" +
               md_table(["Scheme", "Principal (₹)", "Rate (% p.a.)", "Time (years)", "Interest (₹)"],
                        [[k, *v] for k, v in shown.items()]))
p2 = F(9600 * 100, 10 * 4)
assert p2 == 24000 and F(9600 * 100, 10) == 96000
Q(T, "Table with missing values", I, "What is the principal invested in scheme S2?",
  "₹24,000", ["₹33,600", "₹96,000", "₹19,200"],
  "P = SI × 100 ÷ (R × T)",
  "P = 9,600 × 100 ÷ (10 × 4) = 9,60,000 ÷ 40 = ₹24,000.",
  ["SI = P × R × T ÷ 100", "P = 9,600 × 100 ÷ 40 = 24,000"],
  why="₹33,600 is the amount (principal plus interest); ₹96,000 ignores the time of 4 years.", secs=45, stim=sid)

pct = si["S1"] / si["S2"] * 100
assert pct == F(625, 10)
Q(T, "Table with missing values", I,
  "The interest earned in scheme S1 is what percentage of the interest earned in scheme S2?",
  "62.5%", ["160%", "37.5%", "60%"],
  "Fill the missing interest first, then compare",
  "S1 interest = 25,000 × 8 × 3 ÷ 100 = ₹6,000. S2 interest = ₹9,600. 6,000 ÷ 9,600 × 100 = 62.5%.",
  ["S1: 25,000 × 8% × 3 = 6,000", "6,000 ÷ 9,600 × 100 = 62.5%"],
  why="160% is S2 as a percentage of S1; 37.5% is the gap as a percentage of S2.", secs=50, stim=sid)

r3 = F(14000 * 100, 40000 * 5)
ci = 40000 * ((1 + r3 / 100) ** 2 - 1)
assert r3 == 7 and ci == 5796 and 40000 * r3 * 2 / 100 == 5600
Q(T, "Table with missing values", A,
  "If the principal of scheme S3 were instead invested for 2 years at compound interest (compounded annually) at "
  "the same rate as S3, what interest would it earn?",
  "₹5,796", ["₹5,600", "₹45,796", "₹5,992"],
  "Find the missing rate from the table, then apply compound interest",
  "S3's rate = 14,000 × 100 ÷ (40,000 × 5) = 7%. CI for 2 years = 40,000 × (1.07² − 1) = 40,000 × 0.1449 = ₹5,796.",
  ["R = 14,000 × 100 ÷ 2,00,000 = 7%", "1.07² = 1.1449", "CI = 40,000 × 0.1449 = 5,796"],
  short="2-year CI = 2 × 7% + 0.49% = 14.49% of the principal.",
  why="₹5,600 is the 2-year simple interest; ₹45,796 is the amount, not the interest.", secs=90, stim=sid)

# ================================================================ Quantity Comparison (B2 I3 A2)
T = "Quantity Comparison"
QREL = {">": "Quantity I > Quantity II", ">=": "Quantity I ≥ Quantity II", "<": "Quantity I < Quantity II",
        "<=": "Quantity I ≤ Quantity II", "cbe": "Quantity I = Quantity II or the relationship cannot be established"}


def qc(sub, diff, q1, q2, vals1, vals2, expect, wrong_syms, concept, expl, steps, short=None, why=None, secs=None):
    got = relation(vals1, vals2)
    assert got == expect, (q1, got)
    assert expect not in wrong_syms and "cbe" not in wrong_syms and len(set(wrong_syms)) == 2
    if expect == "cbe":
        third = next(s for s in (">", "<", ">=", "<=") if s not in wrong_syms)
        wrong = [QREL[wrong_syms[0]], QREL[wrong_syms[1]], QREL[third]]
        no_true_distractor(vals1, vals2, [*wrong_syms, third])
    else:
        wrong = [QREL[wrong_syms[0]], QREL["cbe"], QREL[wrong_syms[1]]]
        no_true_distractor(vals1, vals2, wrong_syms)
    Q(T, sub, diff, f"Compare the two quantities and choose the correct option.\nQuantity I: {q1}\nQuantity II: {q2}",
      QREL[expect], wrong, concept, expl, steps, short, why, secs)


q1v = F(8000 * 10 * 3, 100)
q2v = 8000 * (F(11, 10) ** 2 - 1)
assert (q1v, q2v) == (2400, 1680)
qc("Arithmetic-based comparison", B,
   "Simple interest on ₹8,000 at 10% per annum for 3 years",
   "Compound interest on ₹8,000 at 10% per annum for 2 years, compounded annually",
   [q1v], [q2v], ">", ["<=", "<"],
   "SI over 3 years vs CI over 2 years",
   "Quantity I = 8,000 × 10% × 3 = ₹2,400. Quantity II = 8,000 × 21% = ₹1,680. So Quantity I > Quantity II.",
   ["I: 8,000 × 10 × 3 ÷ 100 = 2,400", "II: 8,000 × (1.1² − 1) = 8,000 × 0.21 = 1,680", "2,400 > 1,680"],
   why="'Quantity I < Quantity II' comes from assuming compound interest is always larger, without noticing the "
       "different periods.", secs=40)

q1v = F(sum(range(2, 21, 2)), 10)
q2v = 11 - 1
assert q1v == 11 and q2v == 10 and F(sum(range(2, 19, 2)), 9) == 10 and F(sum(range(1, 11)), 10) == F(11, 2)
qc("Quantity I vs II", B,
   "The average of the first ten even natural numbers", "√121 − 1",
   [q1v], [q2v], ">", ["<=", "<"],
   "Average of an arithmetic sequence = average of first and last terms",
   "The first ten even numbers are 2 to 20, with average (2 + 20) ÷ 2 = 11. Quantity II = 11 − 1 = 10. So "
   "Quantity I > Quantity II.",
   ["I: (2 + 20) ÷ 2 = 11", "II: √121 − 1 = 11 − 1 = 10", "11 > 10"],
   why="'= or cannot be established' comes from averaging 2 to 18 (only nine even numbers, average 10); "
       "'Quantity I < Quantity II' comes from averaging the first ten natural numbers (5.5).", secs=35)

xs = [F(6), F(8)]
roots_check(1, -14, 48, xs)
qc("Quantity I vs II", I,
   "The value of x, where x² − 14x + 48 = 0", "7",
   xs, [F(7)], "cbe", [">", "<="],
   "A quantity with two possible values can lie on either side of a fixed number",
   "x² − 14x + 48 = (x − 6)(x − 8) = 0, so x = 6 or 8. 6 < 7 but 8 > 7, so no single relation holds.",
   ["(x − 6)(x − 8) = 0 ⇒ x = 6 or 8", "x = 6: Quantity I < Quantity II", "x = 8: Quantity I > Quantity II",
    "The relationship cannot be established"],
   why="'Quantity I > Quantity II' takes only the larger root.", secs=50)

q1v = F(22 + 14, 2)
q2v = F(50, F(5, 2))
assert (q1v, q2v) == (18, 20)
qc("Arithmetic-based comparison", I,
   "The speed (km/h) of a boat in still water if it goes downstream at 22 km/h and upstream at 14 km/h",
   "The speed (km/h) of a cyclist who covers 50 km in 2 hours 30 minutes",
   [q1v], [q2v], "<", [">=", ">"],
   "Boat speed = (downstream + upstream) ÷ 2; speed = distance ÷ time",
   "Quantity I = (22 + 14) ÷ 2 = 18 km/h. Quantity II = 50 ÷ 2.5 = 20 km/h. So Quantity I < Quantity II.",
   ["I: (22 + 14) ÷ 2 = 18 km/h", "II: 50 ÷ 2.5 = 20 km/h", "18 < 20"],
   why="'Quantity I > Quantity II' uses the downstream speed 22 km/h as the boat's speed.", secs=45)

q1v = (F(130, 100) * F(90, 100) - 1) * 100
q2v = F(20 - 17, 17) * 100
assert q1v == 17 and near(q2v, 17.647, 1e-3)
qc("Arithmetic-based comparison", I,
   "Profit percentage when an article is marked 30% above its cost price and sold at a 10% discount",
   "Profit percentage when the cost price of 20 articles equals the selling price of 17 articles",
   [q1v], [q2v], "<", [">", ">="],
   "Markup–discount profit vs 'cost of n = selling price of m' profit",
   "Quantity I: 1.3 × 0.9 = 1.17, so 17%. Quantity II: profit = (20 − 17) ÷ 17 = 3/17 ≈ 17.65%. "
   "So Quantity I < Quantity II.",
   ["I: SP = 1.30 × 0.90 × CP = 1.17 CP ⇒ 17%", "II: let CP of 1 article = 1; 17 articles sell for 20",
    "Profit on 17 articles = 3 ⇒ 3/17 × 100 ≈ 17.65%", "17 < 17.65"],
   why="'Quantity I > Quantity II' comes from computing II as 3/20 = 15% (using 20 as the base instead of 17).",
   secs=70)

q1v = F(math.factorial(5), math.factorial(2) * math.factorial(2))
q2v = math.comb(8, 2)
assert q1v == 30 == len(set(itertools.permutations("LEVEL"))) and q2v == 28
qc("Quantity I vs II", A,
   "The number of different arrangements of the letters of the word LEVEL",
   "The number of ways of choosing 2 members from a group of 8",
   [q1v], [q2v], ">", ["<", "<="],
   "Arrangements with repeated letters: n! ÷ (p! q!)",
   "LEVEL has 5 letters with L twice and E twice: 5! ÷ (2! × 2!) = 120 ÷ 4 = 30. ⁸C₂ = 28. So Quantity I > "
   "Quantity II.",
   ["I: 5! ÷ (2! 2!) = 120 ÷ 4 = 30", "II: ⁸C₂ = 8 × 7 ÷ 2 = 28", "30 > 28"],
   why="'Quantity I < Quantity II' comes from dividing 5! by 2! three times (120 ÷ 8 = 15) or from using ⁸P₂ = 56 "
       "for Quantity II; a selection of 2 members is unordered, so ⁸C₂ is correct.", secs=80)

a_days = F(30, F(3, 2))
together = 1 / (1 / a_days + F(1, 30))
c_days = 1 / (F(1, 9) - F(1, 18))
assert a_days == 20 and together == 12 and c_days == 18 and 18 - 9 == 9
qc("Arithmetic-based comparison", A,
   "Days taken by A and B together, if A is 50% more efficient than B and B alone takes 30 days",
   "Days taken by C alone, if C and D together take 9 days and D alone takes 18 days",
   [together], [c_days], "<", [">=", ">"],
   "Efficiency and time are inversely proportional",
   "A is 1.5 times as efficient as B, so A alone takes 30 ÷ 1.5 = 20 days and A + B take 1 ÷ (1/20 + 1/30) = 12 "
   "days. C's rate = 1/9 − 1/18 = 1/18, so C takes 18 days. So Quantity I < Quantity II.",
   ["A alone = 30 ÷ 1.5 = 20 days", "A + B: 1/20 + 1/30 = 5/60 = 1/12 ⇒ 12 days",
    "C: 1/9 − 1/18 = 1/18 ⇒ 18 days", "12 < 18"],
   why="'Quantity I > Quantity II' comes from subtracting days instead of rates for C (18 − 9 = 9 days).",
   secs=100)

# ================================================================ Data Sufficiency (Quant) (B1 I2 A1)
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


cands = [(L_, v_) for v_ in range(1, 61) for L_ in range(50, 1001)]
verdict = ds2_verdict(cands, lambda c: c[0] + 200 == 18 * c[1], lambda c: c[0] == 10 * c[1], lambda c: c[1])
assert verdict == "both"
Q(T, "Two-statement", B,
  f"{DS_PRE}\nQuestion: What is the speed of the train?\n"
  "I. The train crosses a 200 m long platform in 18 seconds.\nII. The train crosses a signal pole in 10 seconds.",
  DS2["both"], [DS2["I"], DS2["either"], DS2["neither"]],
  "Two unknowns (length and speed) need two independent equations",
  "Statement I gives L + 200 = 18v and statement II gives L = 10v; each has two unknowns. Together, 10v + 200 = 18v, "
  "so v = 25 m/s (90 km/h). Both statements are needed.",
  ["I alone: L + 200 = 18v — L unknown, not sufficient", "II alone: L = 10v — L unknown, not sufficient",
   "Together: 10v + 200 = 18v ⇒ 8v = 200 ⇒ v = 25 m/s = 90 km/h", "Both are needed"],
  why="'Statement I alone' is tempting because the platform length is known, but the train's own length is not.",
  secs=40)

cands = list(range(100, 100001, 100))
verdict = ds2_verdict(cands, lambda p_: F(p_ * 8 * 3, 100) == 4800, lambda p_: p_ * (F(11, 10) ** 2 - 1) == 4200,
                      lambda p_: p_)
assert verdict == "either" and F(4800 * 100, 24) == 20000 and F(4200) / F(21, 100) == 20000
Q(T, "Two-statement", I,
  f"{DS_PRE}\nQuestion: What is the principal deposited by Kavya?\n"
  "I. The simple interest on it for 3 years at 8% per annum is ₹4,800.\n"
  "II. The compound interest on it for 2 years at 10% per annum, compounded annually, is ₹4,200.",
  DS2["either"], [DS2["I"], DS2["both"], DS2["II"]],
  "Each statement fixes the rate and time, leaving only the principal unknown",
  "From I: P = 4,800 × 100 ÷ (8 × 3) = ₹20,000. From II: 0.21P = 4,200, so P = ₹20,000. Each statement alone "
  "answers the question.",
  ["I: P × 8 × 3 ÷ 100 = 4,800 ⇒ P = 20,000 — sufficient", "II: P × (1.1² − 1) = 0.21P = 4,200 ⇒ P = 20,000 — "
   "sufficient", "Either statement alone is sufficient"],
  why="'Both together' is a common choice when one statement looks complicated (compound interest), but II alone "
      "has only one unknown.", secs=55)

DS3 = {"all": "All three statements together are necessary", "any2": "Any two of the three statements are sufficient",
       "13": "Only statements I and III together are sufficient",
       "none": "Even all three statements together are not sufficient"}
cands = [(r, s, m) for r in range(1, 101) for s in range(1, 101) for m in range(1, 101)]
c1 = lambda c: c[0] == c[1] + 4
c2 = lambda c: 4 * c[1] == 3 * c[2]
c3 = lambda c: c[0] + c[1] + c[2] == 84


def uniq(conds):
    return len({c[0] for c in cands if all(f(c) for f in conds)}) == 1


assert not any(uniq([f]) for f in (c1, c2, c3))
assert not uniq([c1, c2]) and not uniq([c1, c3]) and not uniq([c2, c3]) and uniq([c1, c2, c3])
assert {c[0] for c in cands if c1(c) and c2(c) and c3(c)} == {28}
Q(T, "Three-statement", I,
  "The question below is followed by three statements. Decide which statements are sufficient to answer it.\n"
  "Question: What is Rahul's present age?\nI. Rahul is 4 years older than Sita.\n"
  "II. The ratio of the present ages of Sita and Mohan is 3 : 4.\n"
  "III. The average present age of Rahul, Sita and Mohan is 28 years.",
  DS3["all"], [DS3["any2"], DS3["13"], DS3["none"]],
  "Three unknowns need three independent equations",
  "There are three unknown ages. I gives R = S + 4, II gives M = 4S/3 and III gives R + S + M = 84. Any two leave "
  "one unknown free; all three give S + 4 + S + 4S/3 = 84, so S = 24 and R = 28.",
  ["Unknowns: R, S, M", "I: R = S + 4; II: M = 4S/3; III: R + S + M = 84",
   "Any two statements: 2 equations, 3 unknowns — not sufficient", "All three: 10S/3 + 4 = 84 ⇒ S = 24 ⇒ R = 28",
   "All three are necessary"],
  why="'Only I and III' looks enough because III ties all three ages, but without II Mohan's age is free "
      "(R + S + M = 84 with R = S + 4 has many solutions).", secs=75)

rates = [F(k, 2) for k in range(1, 101)]
s1 = {r for r in rates if 8 * r == 100}
s2 = {r for r in rates if 5000 * r * 4 / 100 == 2500}
s3 = {r for r in rates if 16000 * (r / 100) ** 2 == 250}
assert s1 == s2 == s3 == {F(25, 2)}
Q(T, "Three-statement", A,
  "The question below is followed by three statements. Decide which statements are sufficient to answer it.\n"
  "Question: At what rate of interest per annum is a bank lending money?\n"
  "I. A sum lent at this rate of simple interest doubles itself in 8 years.\n"
  "II. The simple interest on ₹5,000 for 4 years at this rate is ₹2,500.\n"
  "III. On ₹16,000 lent for 2 years at this rate, compound interest (compounded annually) exceeds simple interest "
  "by ₹250.",
  "Any one of the three statements alone is sufficient",
  ["Either I alone or II alone is sufficient, but III alone is not", "Only II and III together are sufficient",
   DS3["all"]],
  "Each statement is a single equation in the rate alone",
  "I: interest of 100% in 8 years gives R = 12.5%. II: 5,000 × R × 4 ÷ 100 = 2,500 gives R = 12.5%. III: for 2 "
  "years, CI − SI = P(R/100)², so 16,000 × (R/100)² = 250, (R/100)² = 1/64 and R = 12.5%. Each statement alone is "
  "sufficient.",
  ["I: 8R = 100 ⇒ R = 12.5%", "II: 5,000 × R × 4 ÷ 100 = 2,500 ⇒ 200R = 2,500 ⇒ R = 12.5%",
   "III: 16,000 × (R/100)² = 250 ⇒ (R/100)² = 1/64 ⇒ R/100 = 1/8 ⇒ R = 12.5%",
   "Each statement alone gives R"],
  why="Many reject III alone, not recalling the 2-year formula CI − SI = P(R/100)²; the negative root is "
      "impossible for a rate, so III gives a unique answer.", secs=110)

# ================================================================ checks and output
assert len(QUESTIONS) == TOTAL, len(QUESTIONS)
assert len(STIMULI) == 12

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_001_plan.json").read_text(encoding="utf-8"))
qa = next(s for s in plan["subjects"] if s["subject"] == SUBJECT)
from collections import Counter  # noqa: E402

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
    "batch_id": "BATCH_001",
    "created_at": TODAY,
    "notes": "BATCH_001, Quantitative Aptitude part: 200 original questions (60 Basic, 80 Intermediate, 60 Advanced) "
             "with 12 shared DI stimuli. Every answer was recomputed by tools/batch_001/quant.py before writing. "
             "Pending human review.",
    "stimuli": STIMULI,
    "questions": QUESTIONS,
}
out = ROOT / "batches" / "parts" / "BATCH_001_QUANT.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(QUESTIONS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(keys.items()))})")
