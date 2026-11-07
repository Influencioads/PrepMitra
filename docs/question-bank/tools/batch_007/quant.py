"""Writes batches/parts/BATCH_007_QUANT.json: the 199 Quantitative Aptitude questions of BATCH_007.

Every answer is recomputed here before the file is written: arithmetic with exact fractions, series regenerated
from their rule (wrong-number series: exactly one term differs from the regenerated series), quadratic roots
substituted back into the equations, probabilities, arrangements and selections counted by brute force,
data-sufficiency statements checked by enumerating candidate cases, approximation answers checked to be the option
nearest the exact value by a clear margin. If any assertion fails, nothing is written.

Structure and helpers follow tools/batch_006/quant.py (relation-option guards, no-equal-quantity rule and 2% gap for
quantity comparison, balanced key shuffler with a new seed, approximation margin check, set-size asserts). Contexts,
data sets and number templates are new: all earlier Quant stems (BATCH_000 to BATCH_006) and the 68 earlier DI titles
were read first, and none of their DI themes or arithmetic templates is reused. DI data avoid tied values wherever a
question asks for a maximum or minimum.

    python tools/batch_007/quant.py          (run from docs/question-bank)
    python tools/batch_007/quant.py --dump <file> [--ids a,b,...]   (blind copy for solvers: no key, no solution)
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

# Balanced answer keys: 50 A, 50 B, 50 C and 49 D, order fixed by the seed (new seed for batch 7).
_rng = random.Random(20261105 + 7)
KEYS = list("ABCD" * 50)[:TOTAL]
_rng.shuffle(KEYS)

QUESTIONS, STIMULI = [], []
_set_pos = {}
_FIRST_ID = 1205
_FIRST_STIM = 7001
RECOMPUTE = ["script:recompute", "ai:self-recheck"]
BRUTE = ["script:recompute", "script:brute-force-unique", "ai:self-recheck"]

# Questions that a separate, fresh solver re-answered from the stem, options and data set alone (no key, no
# solution) and whose answer matched the key. Only these carry ai:independent-check. Every third question
# (BANK_QUANT_001205, _001208, ..., _001403: 67 questions) was given to two separate fresh solver agents (34 and 33
# questions, blind dumps made with --dump --ids); all 67 answers matched the key. One solver flagged the wording of
# BANK_QUANT_001385 ("total payout"); its stem was tightened to "net amount ... minus the reverse-shipping charges" and
# the new stem was re-solved blind by a third fresh solver, who matched the key. No other question was changed after
# its blind check.
INDEPENDENT = {f"BANK_QUANT_{n:06d}" for n in range(1205, 1404, 3)}

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


# ================================================================ Simplification (B3 I10 A4)
T = "Simplification"
v = F(3, 4) * 168 + F(25, 100) * 360 / 6 - 8 ** 2
assert v == 77 and F(3, 4) * 168 + 90 - 64 == 152 and (126 + 90) / 6 - 64 == -28 and 126 + 15 - 16 == 125
Q(T, "BODMAS", B, "Simplify: ¾ of 168 + 25% of 360 ÷ 6 − 8²",
  "77", ["152", "−28", "125"],
  "'Of' (and a percentage of) is worked first, then ÷ and ×, then + and −",
  "¾ of 168 = 126 and 25% of 360 = 90. Next the division: 90 ÷ 6 = 15. Then 126 + 15 − 64 = 77.",
  ["¾ of 168 = 126", "25% of 360 = 90, and 90 ÷ 6 = 15", "8² = 64", "126 + 15 − 64 = 77"],
  why="152 skips the ÷ 6 (126 + 90 − 64); −28 works left to right, dividing 126 + 90 by 6; 125 reads 8² as 2 × 8 = "
      "16.", secs=40)

v = F("6.25") * F("0.48") + F("0.9") / F("0.025") - F("2.5") ** 2
assert v == F(131, 4) and 3 + F("3.6") - F("6.25") == F("0.35") and 3 + 36 - 5 == 34 and 3 + 36 + F("6.25") == F("45.25")
Q(T, "Fractions and decimals", B, QMARK + "6.25 × 0.48 + 0.9 ÷ 0.025 − 2.5² = ?",
  "32.75", ["0.35", "34", "45.25"],
  "Clear the decimals: 6.25 = 25/4, and dividing by 0.025 is multiplying by 40",
  "6.25 × 0.48 = 3; 0.9 ÷ 0.025 = 900 ÷ 25 = 36; 2.5² = 6.25. So 3 + 36 − 6.25 = 32.75.",
  ["6.25 × 0.48 = 25/4 × 0.48 = 3", "0.9 ÷ 0.025 = 36", "2.5² = 6.25", "3 + 36 − 6.25 = 32.75"],
  why="0.35 divides 0.9 by 0.25 instead of 0.025 (3.6); 34 squares 2.5 as 5; 45.25 adds 6.25 instead of subtracting "
      "it.", secs=45)

assert 2450 == 2 * 35 ** 2 and all(math.isqrt(2450 // d) ** 2 != 2450 // d for d in (5, 7, 10))
assert math.isqrt(2450 // 2) == 35
Q(T, "Square and cube roots", B,
  "What is the smallest number by which 2,450 must be divided so that the quotient is a perfect square?",
  "2", ["5", "7", "10"],
  "Write the number as a product of primes; divide out every prime that appears an odd number of times",
  "2,450 = 2 × 5² × 7². Only the prime 2 has an odd power, so dividing by 2 leaves 5² × 7² = 1,225 = 35².",
  ["2,450 = 2 × 1,225", "1,225 = 5² × 7² = 35²", "Divide by 2"],
  why="Dividing by 5 gives 490, by 7 gives 350 and by 10 gives 245, none of which is a perfect square (5 and 7 already "
      "appear squared).", secs=40)

v = (F(45, 100) * 1240 - (F(7, 9) * 315 + 11 ** 2)) / 12
assert v == 16 and F(558 + 366, 12) == 77 and F(558 - 245 - 22, 12) == F(97, 4) and F(540 - 366, 12) == F(29, 2)
Q(T, "BODMAS", I, QMARK + "45% of 1,240 − ? × 12 = 7/9 of 315 + 11²",
  "16", ["77", "24.25", "14.5"],
  "Evaluate both sides fully, then isolate the term with ?",
  "45% of 1,240 = 558. Right side: 7/9 of 315 = 245 and 11² = 121, so it is 366. Then 558 − 12 × ? = 366, so "
  "12 × ? = 192 and ? = 16.",
  ["45% of 1,240 = 558", "7/9 × 315 + 121 = 245 + 121 = 366", "12 × ? = 558 − 366 = 192", "? = 16"],
  why="77 adds 366 to 558 instead of subtracting; 24.25 takes 11² as 22; 14.5 takes 45% of 1,240 as 540.", secs=60)

e = F(8) * F(16, 100) + F(4) * F(18, 100)
assert e == 2 and 2 ** e == 4
Q(T, "Surds and indices", I, "Find the value of (256)^0.16 × (16)^0.18.",
  "4", ["2", "8", "16"],
  "Write both bases as powers of 2 and add the exponents",
  "256 = 2⁸ and 16 = 2⁴. So 256^0.16 = 2^1.28 and 16^0.18 = 2^0.72. The product is 2^(1.28 + 0.72) = 2² = 4.",
  ["256^0.16 = 2^(8 × 0.16) = 2^1.28", "16^0.18 = 2^(4 × 0.18) = 2^0.72", "2^(1.28 + 0.72) = 2² = 4"],
  why="2 stops at 2¹ (adding 0.28 + 0.72); 8 is 2³; 16 is 4², mixing the base 4 with the exponent 2.", secs=60)

r5 = math.sqrt(5)
x_ = r5 + 2
assert near(x_ - 1 / x_, 4) and near(1 / x_, r5 - 2) and near(x_ * x_, 9 + 4 * r5)
Q(T, "Surds and indices", I, "If x = √5 + 2, what is the value of x − 1/x?",
  "4", ["2√5", "√5 − 2", "9 + 4√5"],
  "Rationalise 1/x: multiply the numerator and denominator by √5 − 2",
  "1/x = 1/(√5 + 2) = (√5 − 2)/(5 − 4) = √5 − 2. So x − 1/x = (√5 + 2) − (√5 − 2) = 4.",
  ["1/x = (√5 − 2)/(5 − 4) = √5 − 2", "x − 1/x = √5 + 2 − √5 + 2", "= 4"],
  why="2√5 is x + 1/x; √5 − 2 is 1/x itself; 9 + 4√5 is x².", secs=60)

xs_ = [x for x in (F(3), F(0), F(-9), F(11, 3)) if (2 * x - 1) - (x - 4) == 6]
assert xs_ == [3] and 0 + 3 == 3 and -9 + 3 == -6 and 3 * F(11, 3) - 5 == 6
Q(T, "Surds and indices", I, "If (5/3)^(2x − 1) × (3/5)^(x − 4) = (9/25)^(−3), what is the value of x?",
  "3", ["0", "−9", "11/3"],
  "Write everything as a power of 5/3: (3/5)ⁿ = (5/3)⁻ⁿ and (9/25)⁻³ = (25/9)³ = (5/3)⁶",
  "Left side: (5/3)^(2x − 1) × (5/3)^(−x + 4) = (5/3)^(x + 3). Right side: (9/25)^(−3) = (25/9)³ = (5/3)⁶. "
  "So x + 3 = 6 and x = 3.",
  ["(3/5)^(x − 4) = (5/3)^(4 − x)", "Left = (5/3)^(x + 3)", "(9/25)^(−3) = (5/3)⁶", "x + 3 = 6 ⇒ x = 3"],
  why="0 takes the right side as (5/3)³; −9 takes it as (5/3)⁻⁶ (forgetting that the negative power flips 9/25); "
      "11/3 treats (3/5)^(x − 4) as (5/3)^(x − 4), giving 3x − 5 = 6.", secs=75)

v = (F(6, 10) ** 0 - F(1, 10) ** -1) / (F(3, 8) ** -1 * F(3, 2) ** 3 + F(-1, 3) ** -1)
assert v == F(-3, 2) and F(-9, 9 + 3) == F(-3, 4) and F(-10, 6) == F(-5, 3)
Q(T, "Surds and indices", I,
  "Simplify: [(0.6)⁰ − (0.1)⁻¹] ÷ [(3/8)⁻¹ × (3/2)³ + (−1/3)⁻¹]",
  "−3/2", ["3/2", "−3/4", "−5/3"],
  "a⁰ = 1 and a⁻¹ = 1/a; keep the sign of (−1/3)⁻¹ = −3",
  "Numerator: 1 − 10 = −9. Denominator: (8/3) × (27/8) + (−3) = 9 − 3 = 6. Value = −9 ÷ 6 = −3/2.",
  ["(0.6)⁰ = 1, (0.1)⁻¹ = 10 ⇒ numerator −9", "(3/8)⁻¹ = 8/3, (3/2)³ = 27/8 ⇒ product 9",
   "(−1/3)⁻¹ = −3 ⇒ denominator 6", "−9 ÷ 6 = −3/2"],
  why="3/2 drops the minus sign of the numerator; −3/4 takes (−1/3)⁻¹ as +3 (denominator 12); −5/3 takes (0.6)⁰ as 0 "
      "(numerator −10).", secs=80)

xv = (F(13, 12) ** 2 - 1) * 144
assert xv == 25 and (F(13, 12) - 1) * 144 == 12
Q(T, "Square and cube roots", I, "If √(1 + x/144) = 13/12, what is the value of x?",
  "25", ["12", "169", "5"],
  "Square both sides before isolating x",
  "Squaring: 1 + x/144 = 169/144, so x/144 = 25/144 and x = 25.",
  ["1 + x/144 = (13/12)² = 169/144", "x/144 = 169/144 − 144/144 = 25/144", "x = 25"],
  why="12 forgets to square 13/12 (x/144 = 1/12); 169 is 13², the numerator before subtracting 144; 5 is √25, the "
      "square root of the answer.", secs=50)

assert 11111 ** 2 == 123454321 and all(k ** 2 != 123454321 for k in (11011, 11101, 10111))
Q(T, "Square and cube roots", I, "What is the square root of 12,34,54,321?",
  "11,111", ["11,011", "11,101", "10,111"],
  "Numbers made of 1s have palindromic squares: 11² = 121, 111² = 12,321, 1,111² = 12,34,321, …",
  "12,34,54,321 rises 1-2-3-4-5 and falls back 4-3-2-1, the pattern of 11,111² (five 1s). Check: 11,111² = "
  "12,34,54,321.",
  ["9 digits ⇒ the root has 5 digits", "Digits rise to 5 and fall back ⇒ five 1s", "11,111² = 12,34,54,321 ✓"],
  short="1…1 (n ones) squared reads 1, 2, …, n, …, 2, 1 for n ≤ 9.",
  why="11,011² = 12,12,42,121; 11,101² = 12,32,32,201; 10,111² = 10,22,32,321; none matches.", secs=45)

a_, b_ = F("2.36"), F("1.64")
v = (a_ ** 3 + b_ ** 3) / (a_ ** 2 - a_ * b_ + b_ ** 2)
assert v == 4 and a_ - b_ == F("0.72") and a_ * b_ == F("3.8704")
Q(T, "Fractions and decimals", I,
  "If a = 2.36 and b = 1.64, what is the value of (a³ + b³) ÷ (a² − ab + b²)?",
  "4", ["0.72", "3.8704", "16"],
  "a³ + b³ = (a + b)(a² − ab + b²), so the quotient is simply a + b",
  "Since a³ + b³ = (a + b)(a² − ab + b²), the expression equals a + b = 2.36 + 1.64 = 4.",
  ["a³ + b³ = (a + b)(a² − ab + b²)", "Quotient = a + b", "= 2.36 + 1.64 = 4"],
  why="0.72 is a − b (the result for a³ − b³ over a² + ab + b²); 3.8704 is ab; 16 is (a + b)².", secs=50)

v = (F(7, 9) - F(2, 3)) * F(21, 4) / F(7, 3) + F(1, 4)
assert v == F(1, 2) and F(7, 12) + F(1, 4) == F(5, 6) and F(7, 12) * F(7, 3) + F(1, 4) == F(29, 18)
Q(T, "Fractions and decimals", I, QMARK + "(7/9 − 2/3) of 5¼ ÷ 2⅓ + ¼ = ?",
  "1/2", ["5/6", "29/18", "1/4"],
  "Bracket first, then 'of', then ÷, then +",
  "7/9 − 2/3 = 1/9. 1/9 of 21/4 = 7/12. 7/12 ÷ 7/3 = 7/12 × 3/7 = 1/4. Then 1/4 + 1/4 = 1/2.",
  ["7/9 − 6/9 = 1/9", "1/9 × 21/4 = 7/12", "7/12 ÷ 7/3 = 1/4", "1/4 + 1/4 = 1/2"],
  why="5/6 skips the ÷ 2⅓ (7/12 + 1/4); 29/18 multiplies by 2⅓ instead of dividing; 1/4 forgets the final + ¼.",
  secs=60)

e = F("3.2") * 3 + F("1.8") * 2 - 5
assert e == F("8.2") and F("13.2") + 5 == F("18.2") and F("6.2") + F("3.6") - 5 == F("4.8") and F("9.6") + F("1.8") - 5 == F("6.4")
Q(T, "Surds and indices", I, QMARK + "8^3.2 × 4^1.8 ÷ 2^? = 32",
  "8.2", ["18.2", "4.8", "6.4"],
  "Convert to base 2: 8 = 2³, 4 = 2², 32 = 2⁵; then compare exponents",
  "8^3.2 = 2^9.6 and 4^1.8 = 2^3.6, so the left side is 2^(13.2 − ?). Setting 13.2 − ? = 5 gives ? = 8.2.",
  ["8^3.2 = 2^(3 × 3.2) = 2^9.6", "4^1.8 = 2^(2 × 1.8) = 2^3.6", "13.2 − ? = 5", "? = 8.2"],
  why="18.2 adds 5 to 13.2 instead of subtracting; 4.8 writes 8^3.2 as 2^(3 + 3.2); 6.4 writes 4^1.8 as 2^1.8.",
  secs=60)

s2 = 3 ** 2 + 2
assert s2 == 11 and s2 ** 2 - 2 == 119 and 3 ** 4 == 81 and 9 ** 2 - 2 == 79
xr = (3 + math.sqrt(13)) / 2
assert near(xr - 1 / xr, 3) and near(xr ** 4 + xr ** -4, 119, 1e-6)
Q(T, "Surds and indices", A, "If x − 1/x = 3, what is the value of x⁴ + 1/x⁴?",
  "119", ["121", "81", "79"],
  "Square twice: (x − 1/x)² = x² + 1/x² − 2, then (x² + 1/x²)² = x⁴ + 1/x⁴ + 2",
  "x² + 1/x² = 3² + 2 = 11. Then x⁴ + 1/x⁴ = 11² − 2 = 119.",
  ["(x − 1/x)² = 9 ⇒ x² + 1/x² = 9 + 2 = 11", "(x² + 1/x²)² = 121", "x⁴ + 1/x⁴ = 121 − 2 = 119"],
  why="121 forgets to subtract 2 at the second squaring; 81 is simply 3⁴; 79 forgets to add 2 at the first squaring "
      "(9² − 2).", secs=75)

v = sum(k * k for k in range(11, 21))
assert v == 2485 and sum(k * k for k in range(1, 21)) == 2870 and 2870 - 506 == 2364 and 10 * (121 + 400) // 2 == 2605
Q(T, "BODMAS", A, "What is the value of 11² + 12² + 13² + … + 20²?",
  "2,485", ["2,870", "2,364", "2,605"],
  "1² + 2² + … + n² = n(n + 1)(2n + 1)/6; take the sum up to 20 and subtract the sum up to 10",
  "Sum up to 20 = 20 × 21 × 41 ÷ 6 = 2,870. Sum up to 10 = 10 × 11 × 21 ÷ 6 = 385. Required sum = 2,870 − 385 = "
  "2,485.",
  ["Σ(1 to 20) k² = 20 × 21 × 41 / 6 = 2,870", "Σ(1 to 10) k² = 385", "2,870 − 385 = 2,485"],
  why="2,870 forgets to remove 1² to 10²; 2,364 removes 1² to 11² (506), dropping 11² as well; 2,605 averages only "
      "the first and last squares (10 × (121 + 400)/2), but squares do not rise evenly.", secs=75)

cand = {"√5 − √3": math.sqrt(5) - math.sqrt(3), "√7 − √5": math.sqrt(7) - math.sqrt(5),
        "√9 − √7": 3 - math.sqrt(7), "√11 − √9": math.sqrt(11) - 3}
assert max(cand, key=cand.get) == "√5 − √3" and sorted(cand.values(), reverse=True)[1] < cand["√5 − √3"] - 0.05
Q(T, "Surds and indices", A, "Which of the following is the largest?",
  "√5 − √3", ["√7 − √5", "√9 − √7", "√11 − √9"],
  "√a − √b = (a − b)/(√a + √b); with the same a − b, the smallest denominator gives the largest value",
  "Each difference has a − b = 2, so each equals 2 ÷ (√a + √b). The denominator is smallest for √5 + √3 (about "
  "3.97), so √5 − √3 (about 0.504) is the largest; the others are about 0.410, 0.354 and 0.317.",
  ["√a − √b = 2/(√a + √b) for each option", "√5 + √3 is the smallest sum", "So √5 − √3 is the largest"],
  why="√7 − √5, √9 − √7 and √11 − √9 have larger denominators √7 + √5, √9 + √7 and √11 + √9, so they are smaller.",
  secs=70)

a_, b_, c_ = F("2.7"), F("-1.2"), F("-1.5")
v = (a_ ** 3 + b_ ** 3 + c_ ** 3) / (a_ * b_ * c_)
assert a_ + b_ + c_ == 0 and v == 3
Q(T, "Fractions and decimals", A,
  "If a = 2.7, b = −1.2 and c = −1.5, what is the value of (a³ + b³ + c³) ÷ abc?",
  "3", ["−3", "0", "1"],
  "If a + b + c = 0, then a³ + b³ + c³ = 3abc",
  "a + b + c = 2.7 − 1.2 − 1.5 = 0, so a³ + b³ + c³ = 3abc and the quotient is 3. (Check: a³ + b³ + c³ = 19.683 − "
  "1.728 − 3.375 = 14.58 and abc = 4.86; 14.58 ÷ 4.86 = 3.)",
  ["a + b + c = 0", "⇒ a³ + b³ + c³ = 3abc", "Quotient = 3"],
  why="−3 slips a sign in abc (which is positive here: 2.7 × −1.2 × −1.5 = 4.86); 0 assumes the cubes also add to "
      "zero; 1 assumes a³ + b³ + c³ = abc.", secs=70)

# ================================================================ Approximation (B6 I2 A2)
T = "Approximation"
ex = (2 / 9 * 1350.4 + 14.98 ** 2) / 1499.7 * 100
nearest(ex, [35, 20, 15, 42], 35)
Q(T, "Percentage approximation", B, APPROX + "?% of 1,499.7 ≈ 2/9 of 1,350.4 + 14.98²",
  "35", ["20", "15", "42"],
  "Round each figure to a convenient value: 1,500, 1,350 and 15",
  "2/9 of 1,350 = 300 and 15² = 225, so the right side ≈ 525. ?% of 1,500 = 525 gives ? = 525 ÷ 15 = 35.",
  ["2/9 × 1,350 = 300", "15² = 225", "? = 525 ÷ 1,500 × 100 = 35"],
  why="20 leaves out the 15² term (300 ÷ 15); 15 uses only the 15² term (225 ÷ 15); 42 is not supported by any "
      "reading of the figures.", secs=40)

ex = math.sqrt(4224.8) * 2.98 - 1330.6 ** (1 / 3)
nearest(ex, [184, 206, 154, 130], 184)
Q(T, "Root approximation", B, APPROX + "√4,224.8 × 2.98 − ∛1,330.6 ≈ ?",
  "184", ["206", "154", "130"],
  "4,225 = 65² and 1,331 = 11³",
  "√4,225 = 65 and ∛1,331 = 11. So 65 × 3 − 11 = 195 − 11 = 184.",
  ["√4,224.8 ≈ 65", "∛1,330.6 ≈ 11", "65 × 3 − 11 = 184"],
  why="206 adds the cube root instead of subtracting it; 154 takes √4,225 as 55; 130 multiplies 65 by 2 and drops the "
      "cube root.", secs=40)

ex = 520.4 / (1399.7 / 34.98)
nearest(ex, [13, 15, 11, 17], 13)
Q(T, "Mixed approximation", B, APPROX + "(1,399.7 ÷ 34.98) × ? ≈ 520.4",
  "13", ["15", "11", "17"],
  "1,400 ÷ 35 = 40",
  "1,399.7 ÷ 34.98 ≈ 1,400 ÷ 35 = 40. Then 40 × ? ≈ 520, so ? ≈ 13.",
  ["1,400 ÷ 35 = 40", "? = 520 ÷ 40 = 13"],
  why="15, 11 and 17 give 600, 440 and 680, far from 520.", secs=35)

ex = 1.2498 * 319.7 - 0.3333 * 482.9
nearest(ex, [239, 561, 279, 199], 239)
Q(T, "Percentage approximation", B, APPROX + "124.98% of 319.7 − 33.33% of 482.9 ≈ ?",
  "239", ["561", "279", "199"],
  "125% = 5/4 and 33.33% = 1/3",
  "125% of 320 = 400 and one-third of 483 = 161. So 400 − 161 = 239.",
  ["5/4 × 320 = 400", "483 ÷ 3 = 161", "400 − 161 = 239"],
  why="561 adds the two terms; 279 and 199 are 40 away, from mis-rounding one of the percentages.", secs=40)

ex = (17.97 ** 2 - 12.02 ** 2) / 5.01
nearest(ex, [36, 30, 42, 48], 36)
Q(T, "Mixed approximation", B, APPROX + "17.97² − 12.02² ≈ ? × 5.01",
  "36", ["30", "42", "48"],
  "a² − b² = (a + b)(a − b): 18² − 12² = 30 × 6",
  "18² − 12² = (18 + 12)(18 − 12) = 180. Then ? × 5 = 180, so ? = 36.",
  ["18² − 12² = 30 × 6 = 180", "? = 180 ÷ 5 = 36"],
  why="30 is a + b, not the quotient; 42 and 48 give 210 and 240, too large.", secs=35)

ex = 729.4 ** (1 / 3) * math.sqrt(323.9) / 2.98
nearest(ex, [54, 48, 61, 72], 54)
Q(T, "Root approximation", B, APPROX + "∛729.4 × √323.9 ÷ 2.98 ≈ ?",
  "54", ["48", "61", "72"],
  "729 = 9³ and 324 = 18²",
  "∛729 = 9 and √324 = 18. So 9 × 18 ÷ 3 = 54.",
  ["∛729.4 ≈ 9", "√323.9 ≈ 18", "9 × 18 ÷ 3 = 54"],
  why="48 takes √324 as 16; 72 takes ∛729 as 12; 61 divides by about 2.65 instead of 3.", secs=40)

ex = (3.98 ** 2 + 12.02) * 5.98 / 799.6 * 100
nearest(ex, [21, 18, 24, 27], 21)
Q(T, "Percentage approximation", I, APPROX + "(?% of 799.6) ÷ 5.98 ≈ 3.98² + 12.02",
  "21", ["18", "24", "27"],
  "Round to 800, 6, 4 and 12, then undo the division",
  "Right side ≈ 16 + 12 = 28. So ?% of 800 ≈ 28 × 6 = 168, and ? = 168 ÷ 8 = 21.",
  ["4² + 12 = 28", "?% of 800 = 28 × 6 = 168", "? = 168 ÷ 800 × 100 = 21"],
  why="18 forgets 12 and uses 4² + 8; 24 multiplies by 6.85; 27 multiplies 28 by about 7.7. None of them matches 168 ÷ 8.",
  secs=55)

ex = ((0.1599 * 450.2 - 4.01 * 2.98) / 4.02) ** 3
nearest(ex, [3375, 2744, 4096, 4913], 3375)
Q(T, "Root approximation", I, APPROX + "∛? × 4.02 ≈ 15.99% of 450.2 − 4.01 × 2.98",
  "3,375", ["2,744", "4,096", "4,913"],
  "Simplify the right side, divide by 4, then cube",
  "16% of 450 = 72 and 4 × 3 = 12, so the right side ≈ 60. Then ∛? ≈ 60 ÷ 4 = 15 and ? ≈ 15³ = 3,375.",
  ["16% of 450 = 72", "72 − 12 = 60", "∛? = 15", "? = 15³ = 3,375"],
  why="2,744 = 14³, 4,096 = 16³ and 4,913 = 17³ correspond to cube roots of 14, 16 and 17, not 15.", secs=60)

ex = (0.3598 * 449.7 + 6.02 * 9.01) ** (2 / 3)
nearest(ex, [36, 49, 25, 64], 36)
Q(T, "Mixed approximation", A, APPROX + "?^(3/2) ≈ 35.98% of 449.7 + 6.02 × 9.01",
  "36", ["49", "25", "64"],
  "x^(3/2) = (√x)³; find the right side, take its cube root, then square",
  "36% of 450 = 162 and 6 × 9 = 54, so the right side ≈ 216 = 6³. Then √? = 6 and ? = 36.",
  ["36% of 450 = 162", "162 + 54 = 216", "(√?)³ = 216 ⇒ √? = 6", "? = 36"],
  why="49 gives 7³ = 343; 25 gives 5³ = 125; 64 gives 8³ = 512; only 36 gives 216.", secs=75)

ex = (4 / 7 * 1679.6 - 0.6248 * 639.8) / (6.98 * 4.02)
nearest(ex, [20, 24, 16, 28], 20)
Q(T, "Mixed approximation", A, APPROX + "(4/7 of 1,679.6 − 62.48% of 639.8) ÷ ? ≈ 6.98 × 4.02",
  "20", ["24", "16", "28"],
  "4/7 of 1,680 = 960 and 62.5% = 5/8",
  "4/7 of 1,680 = 960; 5/8 of 640 = 400; 960 − 400 = 560. The right side ≈ 7 × 4 = 28, so ? ≈ 560 ÷ 28 = 20.",
  ["4/7 × 1,680 = 960", "5/8 × 640 = 400", "560 ÷ ? = 28", "? = 20"],
  why="28 is the right side itself, not ?; 24 and 16 give 560 ÷ 24 ≈ 23.3 and 560 ÷ 16 = 35, not 28.", secs=75)

# ================================================================ Number Series (B3 I5 A2)
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


s = series_from(200, lambda t, k: t - 9 * (6 - k), 6)
assert s == [200, 155, 119, 92, 74, 65] and diffs(s) == [-45, -36, -27, -18, -9] and 74 - 18 == 56 and 74 - 9 * 0 == 74
Q(T, "Pattern: differences", B, SERIES_Q + "200, 155, 119, 92, 74, ?",
  "65", ["56", "74", "47"],
  "The differences are falling multiples of 9: 45, 36, 27, 18, …",
  "200 − 45 = 155, 155 − 36 = 119, 119 − 27 = 92, 92 − 18 = 74. The next difference is 9, so the term is 74 − 9 = 65.",
  ["Differences: −45, −36, −27, −18", "Next: −9", "74 − 9 = 65"],
  why="56 subtracts 18 again; 74 repeats the last term as if the next difference were 0; 47 reverses the digits of 74.",
  secs=35)

s = series_from(1, lambda t, k: 3 * t + k, 6)
assert s == [1, 4, 14, 45, 139, 422] and 139 * 3 + 4 == 421 and 139 * 3 == 417 and 139 + 94 * 3 == 421
Q(T, "Pattern: multiply-add", B, SERIES_Q + "1, 4, 14, 45, 139, ?",
  "422", ["421", "417", "426"],
  "Each term is 3 times the previous term plus 1, 2, 3, 4, …",
  "1 × 3 + 1 = 4, 4 × 3 + 2 = 14, 14 × 3 + 3 = 45, 45 × 3 + 4 = 139. Next: 139 × 3 + 5 = 422.",
  ["× 3 + 1, × 3 + 2, × 3 + 3, × 3 + 4", "Next: × 3 + 5", "139 × 3 + 5 = 422"],
  why="421 adds 4 again instead of 5; 417 multiplies by 3 and adds nothing; 426 adds 9 (taking the added numbers as "
      "squares).", secs=45)

PR = [2, 3, 5, 7, 11, 13]
s = [p * p - 1 for p in PR]
assert s == [3, 8, 24, 48, 120, 168] and 12 ** 2 - 1 == 143 and 13 ** 2 + 1 == 170 and 120 + 72 == 192
Q(T, "Pattern: squares and cubes", B, SERIES_Q + "3, 8, 24, 48, 120, ?",
  "168", ["143", "170", "192"],
  "The terms are one less than the squares of the prime numbers 2, 3, 5, 7, 11, …",
  "3 = 2² − 1, 8 = 3² − 1, 24 = 5² − 1, 48 = 7² − 1, 120 = 11² − 1. The next prime is 13, so the term is 13² − 1 = "
  "168.",
  ["2² − 1, 3² − 1, 5² − 1, 7² − 1, 11² − 1", "Next prime: 13", "13² − 1 = 168"],
  why="143 = 12² − 1 uses 12, which is not prime; 170 = 13² + 1 adds instead of subtracting; 192 adds the last "
      "difference (72) again.", secs=45)

s = series_from(20, lambda t, k: t + (k * k if k % 2 else -k * k), 7)
assert s == [20, 21, 17, 26, 10, 35, -1] and 35 + 36 == 71 and 35 - 49 == -14 and 35 - 25 == 10
Q(T, "Pattern: differences", I, SERIES_Q + "20, 21, 17, 26, 10, 35, ?",
  "−1", ["71", "−14", "10"],
  "The differences are squares with alternating signs: +1², −2², +3², −4², +5², …",
  "20 + 1 = 21, 21 − 4 = 17, 17 + 9 = 26, 26 − 16 = 10, 10 + 25 = 35. Next: 35 − 36 = −1.",
  ["+1, −4, +9, −16, +25", "Next: −6² = −36", "35 − 36 = −1"],
  why="71 adds 36 instead of subtracting it; −14 subtracts 7² and skips 6²; 10 subtracts 5² and repeats an earlier "
      "term.", secs=55)

s = [n * n + 2 ** n for n in range(1, 7)]
assert s == [3, 8, 17, 32, 57, 100] and diffs(s) == [5, 9, 15, 25, 43] and 57 + 35 == 92 and 57 + 32 == 89 and 57 + 39 == 96
assert 17 + 32 + 57 != 100 and 8 + 17 + 32 == 57  # the last three terms do not sum to the next (no rival rule)
Q(T, "Pattern: squares and cubes", I, SERIES_Q + "3, 8, 17, 32, 57, ?",
  "100", ["92", "89", "96"],
  "Each term is n² + 2ⁿ for n = 1, 2, 3, …",
  "1 + 2 = 3, 4 + 4 = 8, 9 + 8 = 17, 16 + 16 = 32, 25 + 32 = 57. Next: 6² + 2⁶ = 36 + 64 = 100.",
  ["n = 1 to 5: 3, 8, 17, 32, 57", "n = 6: 36 + 64", "= 100"],
  short="Differences 5, 9, 15, 25 have second differences 4, 6, 10 = 2 + 2, 2 + 4, 2 + 8; next 2 + 16 = 18, so the "
        "next difference is 43.",
  why="92 assumes the differences grow by 10 each time (+35); 89 adds only 2⁵ = 32; 96 assumes the second differences "
      "go 4, 6, 10, 14 (+39).", secs=60)

s = [n * n * (n - 1) for n in range(2, 8)]
assert s == [4, 18, 48, 100, 180, 294] and 4 ** 3 == 64 and 18 + (18 - 4) * 2 == 46 and 4 * 4 * 4 - 4 * 4 + 2 == 50
Q(T, "Pattern: squares and cubes", I, MISSING_Q + "4, 18, ?, 100, 180, 294",
  "48", ["64", "46", "50"],
  "Each term is n³ − n² = n²(n − 1) for n = 2, 3, 4, …",
  "2²(1) = 4, 3²(2) = 18, 4²(3) = 48, 5²(4) = 100, 6²(5) = 180, 7²(6) = 294. The missing term is 48.",
  ["n = 2: 8 − 4 = 4", "n = 3: 27 − 9 = 18", "n = 4: 64 − 16 = 48", "n = 5: 125 − 25 = 100 ✓"],
  why="64 is 4³ without subtracting 4²; 46 doubles the first difference (18 + 28); 50 is 48 + 2 and does not give "
      "100 by the same rule.", secs=60)

s = [F(n * n, 2) for n in range(3, 9)]
assert s == [F(9, 2), 8, F(25, 2), 18, F(49, 2), 32] and F(49, 2) + F(13, 2) == 31 and F(49, 2) + 7 == F(63, 2)
Q(T, "Pattern: squares and cubes", I, SERIES_Q + "4.5, 8, 12.5, 18, 24.5, ?",
  "32", ["31", "31.5", "36"],
  "Each term is half of a perfect square: 9/2, 16/2, 25/2, 36/2, 49/2, …",
  "4.5 = 3²/2, 8 = 4²/2, 12.5 = 5²/2, 18 = 6²/2, 24.5 = 7²/2. Next: 8²/2 = 32. (The differences 3.5, 4.5, 5.5, 6.5 "
  "also lead to + 7.5.)",
  ["Terms = n²/2 for n = 3 to 7", "Next n = 8", "64/2 = 32"],
  why="31 adds 6.5 again; 31.5 adds 7; 36 is 6² rather than 8²/2.", secs=55)

s = [1, 2]
while len(s) < 7:
    s.append(2 * (s[-1] + s[-2]))
assert s == [1, 2, 6, 16, 44, 120, 328] and 16 * 3 == 48 and 16 + 26 == 42 and 2 * (16 + 6) + 6 == 50
Q(T, "Missing number series", I, MISSING_Q + "1, 2, 6, 16, ?, 120, 328",
  "44", ["48", "42", "50"],
  "From the third term on, each term is twice the sum of the two terms before it",
  "6 = 2(1 + 2), 16 = 2(2 + 6), ? = 2(6 + 16) = 44. Check: 2(16 + 44) = 120 and 2(44 + 120) = 328.",
  ["6 = 2 × (1 + 2)", "16 = 2 × (2 + 6)", "? = 2 × (6 + 16) = 44", "Check: 2 × (16 + 44) = 120 ✓"],
  why="48 triples 16 and fails the check 2(16 + 48) = 128 ≠ 120; 42 and 50 also fail the check (116 and 132).",
  secs=65)

def digit_sum(n):
    return sum(int(c) for c in str(n))


s = series_from(47, lambda t, k: t + digit_sum(t), 7)
assert s == [47, 58, 71, 79, 95, 109, 119] and 109 + 14 == 123 and 109 + 10 + 2 == 121 and 109 + 1 == 110
Q(T, "Pattern: differences", A, SERIES_Q + "47, 58, 71, 79, 95, 109, ?",
  "119", ["123", "121", "110"],
  "Each term is the previous term plus the sum of its own digits",
  "47 + (4 + 7) = 58, 58 + 13 = 71, 71 + 8 = 79, 79 + 16 = 95, 95 + 14 = 109, 109 + (1 + 0 + 9) = 119.",
  ["47 + 11 = 58", "58 + 13 = 71", "71 + 8 = 79", "79 + 16 = 95", "95 + 14 = 109", "109 + 10 = 119"],
  why="123 adds 14 again (repeating the last difference); 121 adds 12 (taking the digit sum of 109 as 12); 110 adds 1, "
      "the digit sum of 10 only.", secs=90)

s = series_from(1, lambda t, k: (t + 1) * (k + 1), 6)
assert s == [1, 4, 15, 64, 325, 1956] and 325 * 6 == 1950 and 326 * 5 == 1630 and 325 * 6 + 1 == 1951
Q(T, "Pattern: multiply-add", A, SERIES_Q + "1, 4, 15, 64, 325, ?",
  "1,956", ["1,950", "1,630", "1,951"],
  "Add 1 to each term, then multiply by 2, 3, 4, 5, …",
  "(1 + 1) × 2 = 4, (4 + 1) × 3 = 15, (15 + 1) × 4 = 64, (64 + 1) × 5 = 325. Next: (325 + 1) × 6 = 1,956.",
  ["(1 + 1) × 2 = 4", "(4 + 1) × 3 = 15", "(15 + 1) × 4 = 64", "(64 + 1) × 5 = 325", "(325 + 1) × 6 = 1,956"],
  why="1,950 multiplies 325 by 6 without adding 1 first; 1,630 multiplies by 5 again; 1,951 multiplies first and adds "
      "1 afterwards.", secs=90)

# ================================================================ Wrong Number Series (B2 I3 A2)
T = "Wrong Number Series"


def wrong_series(correct, shown):
    diff = [i for i, (a, b) in enumerate(zip(correct, shown)) if a != b]
    assert len(diff) == 1, (correct, shown)
    return shown[diff[0]], correct[diff[0]]


WRONG_Q = "Find the wrong number in the series:\n"
good = series_from(150, lambda t, k: t - (21 - 2 * k), 7)
shown = [150, 131, 114, 99, 86, 74, 66]
assert good == [150, 131, 114, 99, 86, 75, 66] and wrong_series(good, shown) == (74, 75)
Q(T, "Find the wrong term", B, WRONG_Q + series_text(shown),
  "74", ["114", "86", "66"],
  "The differences fall by 2 each time: 19, 17, 15, 13, 11, 9",
  "150 − 19 = 131, 131 − 17 = 114, 114 − 15 = 99, 99 − 13 = 86, 86 − 11 = 75, 75 − 9 = 66. The sixth term should be "
  "75, not 74.",
  ["Differences shown: 19, 17, 15, 13, 12, 8", "Expected: 19, 17, 15, 13, 11, 9", "86 − 11 = 75 ≠ 74"],
  why="114, 86 and 66 fit the rule; 66 confirms 75, since 75 − 9 = 66.", secs=40)

shown = [29, 31, 37, 41, 43, 49, 53]
primes = [p for p in range(29, 54) if all(p % d for d in range(2, p))]
assert primes == [29, 31, 37, 41, 43, 47, 53] and wrong_series(primes, shown) == (49, 47) and 49 == 7 * 7
Q(T, "Find the wrong term", B, WRONG_Q + series_text(shown),
  "49", ["41", "43", "53"],
  "The terms are consecutive prime numbers",
  "The primes after 29 are 31, 37, 41, 43, 47, 53. The sixth term should be 47; 49 = 7 × 7 is not prime.",
  ["29, 31, 37, 41, 43 are consecutive primes", "Next prime is 47", "49 = 7² is not prime"],
  why="41, 43 and 53 are all primes in the right places.", secs=35)

good = series_from(5, lambda t, k: t + k * (k + 1), 7)
shown = [5, 7, 13, 25, 44, 75, 117]
assert good == [5, 7, 13, 25, 45, 75, 117] and wrong_series(good, shown) == (44, 45)
Q(T, "Find the wrong term", I, WRONG_Q + series_text(shown),
  "44", ["25", "75", "117"],
  "The differences are 1 × 2, 2 × 3, 3 × 4, … = 2, 6, 12, 20, 30, 42",
  "5 + 2 = 7, 7 + 6 = 13, 13 + 12 = 25, 25 + 20 = 45, 45 + 30 = 75, 75 + 42 = 117. The fifth term should be 45, "
  "not 44.",
  ["Expected differences: 2, 6, 12, 20, 30, 42", "25 + 20 = 45 ≠ 44", "45 + 30 = 75 ✓"],
  why="25, 75 and 117 fit; 75 confirms 45, since 44 + 30 = 74.", secs=55)

good = [n ** 3 + n for n in range(1, 8)]
shown = [2, 10, 32, 68, 130, 222, 350]
assert good == [2, 10, 30, 68, 130, 222, 350] and wrong_series(good, shown) == (32, 30)
Q(T, "Find the wrong term", I, WRONG_Q + series_text(shown),
  "32", ["10", "130", "222"],
  "Each term is n³ + n for n = 1, 2, 3, …",
  "1 + 1 = 2, 8 + 2 = 10, 27 + 3 = 30, 64 + 4 = 68, 125 + 5 = 130, 216 + 6 = 222, 343 + 7 = 350. The third term "
  "should be 30, not 32.",
  ["n = 1, 2: 2, 10", "n = 3: 27 + 3 = 30 ≠ 32", "n = 4 to 7: 68, 130, 222, 350 ✓"],
  why="10, 130 and 222 equal 2³ + 2, 5³ + 5 and 6³ + 6.", secs=60)

good = series_from(4, lambda t, k: 2 * t - k, 7)
shown = [4, 7, 12, 21, 39, 71, 136]
assert good == [4, 7, 12, 21, 38, 71, 136] and wrong_series(good, shown) == (39, 38)
Q(T, "Find the wrong term", I, WRONG_Q + series_text(shown),
  "39", ["21", "71", "136"],
  "Each term is twice the previous term minus 1, 2, 3, 4, …",
  "4 × 2 − 1 = 7, 7 × 2 − 2 = 12, 12 × 2 − 3 = 21, 21 × 2 − 4 = 38, 38 × 2 − 5 = 71, 71 × 2 − 6 = 136. The fifth "
  "term should be 38, not 39.",
  ["× 2 − 1, × 2 − 2, × 2 − 3", "21 × 2 − 4 = 38 ≠ 39", "38 × 2 − 5 = 71 ✓"],
  why="21, 71 and 136 fit; 71 confirms 38, since 39 × 2 − 5 = 73.", secs=60)

good = series_from(3, lambda t, k: 3 * t - k * k, 7)
shown = [3, 8, 20, 51, 137, 384, 1122]
assert good == [3, 8, 20, 51, 137, 386, 1122] and wrong_series(good, shown) == (384, 386)
Q(T, "Find the wrong term", A, WRONG_Q + series_text(shown),
  "384", ["51", "137", "1,122"],
  "Each term is three times the previous term minus 1², 2², 3², …",
  "3 × 3 − 1 = 8, 8 × 3 − 4 = 20, 20 × 3 − 9 = 51, 51 × 3 − 16 = 137, 137 × 3 − 25 = 386, 386 × 3 − 36 = 1,122. "
  "The sixth term should be 386, not 384.",
  ["× 3 − 1, × 3 − 4, × 3 − 9, × 3 − 16", "137 × 3 − 25 = 386 ≠ 384", "386 × 3 − 36 = 1,122 ✓"],
  why="51, 137 and 1,122 fit; 1,122 confirms 386, since 384 × 3 − 36 = 1,116.", secs=90)

good = [3]
for k in range(1, 8):
    good.append(good[-1] * 2 if k % 2 else good[-1] + (k // 2) ** 2)
shown = [3, 6, 7, 14, 17, 36, 45, 90]
assert good == [3, 6, 7, 14, 18, 36, 45, 90] and wrong_series(good, shown) == (17, 18)
Q(T, "Find the wrong term", A, WRONG_Q + series_text(shown),
  "17", ["7", "36", "45"],
  "The operations alternate: × 2, then + 1², × 2, then + 2², × 2, then + 3², …",
  "3 × 2 = 6, 6 + 1 = 7, 7 × 2 = 14, 14 + 4 = 18, 18 × 2 = 36, 36 + 9 = 45, 45 × 2 = 90. The fifth term should be "
  "18, not 17.",
  ["× 2: 3 → 6, 7 → 14, 18 → 36, 45 → 90", "+ squares: 6 + 1 = 7, 14 + 4 = 18, 36 + 9 = 45", "Shown 17 ≠ 18"],
  why="7, 36 and 45 fit; 36 confirms 18, since 17 × 2 = 34.", secs=90)

# ================================================================ Quadratic Equations (B3 I5 A1)
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


xs, ys = [F(9), F(-6)], [F(-6), F(-7)]
roots_check(1, -3, -54, xs), roots_check(1, 13, 42, ys)
qe("Relation between roots", B, "Find the roots of I and II and choose the relation between x and y that holds for "
   "every pair.", "x² − 3x − 54 = 0", "y² + 13y + 42 = 0", xs, ys, ">=", [">", "<"],
   "Factorise; a root shared by both equations makes the relation non-strict",
   "I: (x − 9)(x + 6) = 0, so x = 9 or −6. II: (y + 6)(y + 7) = 0, so y = −6 or −7. The smallest x (−6) equals the "
   "largest y (−6), and every other pair has x > y. So x ≥ y.",
   ["I: x = 9, −6", "II: y = −6, −7", "min x = −6 = max y", "So x ≥ y"],
   why="x > y fails for the pair x = y = −6; x < y holds for no pair.", secs=45)

xs, ys = [F(8), F(9)], [F(10), F(11)]
roots_check(1, -17, 72, xs), roots_check(1, -21, 110, ys)
qe("Relation between roots", B, "Solve both quadratics and state how x compares with y.",
   "x² − 17x + 72 = 0", "y² − 21y + 110 = 0", xs, ys, "<", [">", ">="],
   "Factorise each equation; compare the largest x with the smallest y",
   "I: (x − 8)(x − 9) = 0, so x = 8 or 9. II: (y − 10)(y − 11) = 0, so y = 10 or 11. The largest x (9) is below the "
   "smallest y (10), so x < y.",
   ["I: 8 × 9 = 72, 8 + 9 = 17", "II: 10 × 11 = 110, 10 + 11 = 21", "max x = 9 < min y = 10"],
   why="x > y and x ≥ y reverse the comparison; every x is smaller than every y.", secs=40)

xs, ys = [F(7), F(-9)], [F(9), F(-5)]
roots_check(1, 2, -63, xs), roots_check(1, -4, -45, ys)
qe("Relation between roots", B, "Each equation has one positive and one negative root. Find them and decide which "
   "relation between x and y, if any, always holds.", "x² + 2x − 63 = 0", "y² − 4y − 45 = 0", xs, ys, "cbe",
   [">", "<="],
   "When the roots interleave, no single relation holds for every pair",
   "I: (x + 9)(x − 7) = 0, so x = 7 or −9. II: (y − 9)(y + 5) = 0, so y = 9 or −5. x = 7 is less than y = 9 but "
   "greater than y = −5, so no relation holds for every pair.",
   ["I: x = 7, −9", "II: y = 9, −5", "7 < 9 but 7 > −5", "Relationship cannot be established"],
   why="x > y fails for 7 and 9; x ≤ y fails for 7 and −5; x < y and x ≥ y fail similarly.", secs=45)

xs, ys = [F(-8, 3), F(-4)], [F(-2), F(-5, 2)]
roots_check(3, 20, 32, xs), roots_check(2, 9, 10, ys)
qe("Relation between roots", I, "Solve the two equations, whose roots are negative, and choose the relation between "
   "x and y.", "3x² + 20x + 32 = 0", "2y² + 9y + 10 = 0", xs, ys, "<", [">", ">="],
   "Split the middle term: 20x = 12x + 8x and 9y = 4y + 5y",
   "I: 3x² + 12x + 8x + 32 = (3x + 8)(x + 4) = 0, so x = −8/3 ≈ −2.67 or −4. II: 2y² + 4y + 5y + 10 = (y + 2)(2y + 5) "
   "= 0, so y = −2 or −2.5. The largest x (−2.67) is below the smallest y (−2.5), so x < y.",
   ["I: (3x + 8)(x + 4) = 0 ⇒ x = −2.67, −4", "II: (y + 2)(2y + 5) = 0 ⇒ y = −2, −2.5", "max x = −2.67 < min y = −2.5"],
   why="x > y and x ≥ y compare 8/3 and 4 with 2 and 2.5 without the minus signs.", secs=70)

xs, ys = [F(3), F(3, 5)], [F(3, 5), F(1, 4)]
roots_check(5, -18, 9, xs), roots_check(20, -17, 3, ys)
qe("Relation between roots", I, "The roots of both equations below are positive. Solve them and mark the relation "
   "between x and y.", "5x² − 18x + 9 = 0", "20y² − 17y + 3 = 0", xs, ys, ">=", [">", "<"],
   "Factorise by splitting the middle term; watch for a common root",
   "I: 5x² − 15x − 3x + 9 = (5x − 3)(x − 3) = 0, so x = 3 or 0.6. II: 20y² − 12y − 5y + 3 = (5y − 3)(4y − 1) = 0, "
   "so y = 0.6 or 0.25. The smallest x (0.6) equals the largest y (0.6), and all other pairs have x > y. So x ≥ y.",
   ["I: (5x − 3)(x − 3) = 0 ⇒ x = 3, 0.6", "II: (5y − 3)(4y − 1) = 0 ⇒ y = 0.6, 0.25", "Common value 0.6 ⇒ x ≥ y"],
   why="x > y fails for the common root 0.6; x < y holds for no pair.", secs=75)

xs, ys = [F(-3, 2), F(-4)], [F(-9, 2), F(-5)]
roots_check(2, 11, 12, xs), roots_check(2, 19, 45, ys)
qe("Relation between roots", I, "Find all the roots of I and II and choose the relation between x and y.",
   "2x² + 11x + 12 = 0", "2y² + 19y + 45 = 0", xs, ys, ">", ["<", "<="],
   "Factorise both; with negative roots, the larger number is the one nearer zero",
   "I: (2x + 3)(x + 4) = 0, so x = −1.5 or −4. II: (2y + 9)(y + 5) = 0, so y = −4.5 or −5. The smallest x (−4) is "
   "greater than the largest y (−4.5), so x > y.",
   ["I: x = −1.5, −4", "II: y = −4.5, −5", "min x = −4 > max y = −4.5"],
   why="x < y and x ≤ y treat −4 as smaller than −4.5.", secs=70)

k_ = 4 * 9 - 16
xs, ys = [F(4), F(5)], [F(3), F(7)]
assert k_ == 20 and 4 + 5 == 9 and 4 * 5 == k_
roots_check(1, -9, k_, xs), roots_check(1, -10, 21, ys)
qe("Relation between roots", I, "In equation I, k is a constant, and x = 4 is known to be one root of I. Find the "
   "other root of I and the roots of II, then choose the relation between x and y.",
   "x² − 9x + k = 0", "y² − 10y + 21 = 0", xs, ys, "cbe", ["<", ">="],
   "The two roots of x² − 9x + k = 0 add up to 9",
   "Sum of the roots of I = 9, so the other root is 9 − 4 = 5 (and k = 20). II: (y − 3)(y − 7) = 0, so y = 3 or 7. "
   "x = 4 is greater than 3 but less than 7, so no relation holds for every pair.",
   ["Other root = 9 − 4 = 5 ⇒ x = 4, 5", "II: y = 3, 7", "4 > 3 but 4 < 7", "Relationship cannot be established"],
   why="x < y fails for x = 4, y = 3; x ≥ y fails for x = 5, y = 7; x > y and x ≤ y fail for the same pairs.",
   secs=65)

xs, ys = [F(2), F(4)], [F(4), F(5)]
for r in xs:
    assert r * r / 2 - 3 * r + 4 == 0
for r in ys:
    assert r * r / 2 - F(9, 2) * r + 10 == 0
qe("Relation between roots", I, "Both equations have fractional coefficients. Clear the fractions, solve, and choose "
   "the relation between x and y.", "x²/2 − 3x + 4 = 0", "y²/2 − 9y/2 + 10 = 0", xs, ys, "<=", ["<", ">="],
   "Multiply each equation by 2 first",
   "I × 2: x² − 6x + 8 = 0, so x = 2 or 4. II × 2: y² − 9y + 20 = 0, so y = 4 or 5. x = y = 4 is possible and every "
   "other pair has x < y. So x ≤ y.",
   ["I: x² − 6x + 8 = 0 ⇒ x = 2, 4", "II: y² − 9y + 20 = 0 ⇒ y = 4, 5", "Common value 4 ⇒ x ≤ y"],
   why="x < y fails for x = y = 4; x ≥ y holds only for that one pair.", secs=60)

xs = [F(x) for x in range(-10, 11) if x * x - 4 * abs(x) + 3 == 0]
ys = [F(-3), F(-5)]
assert xs == [-3, -1, 1, 3]
roots_check(1, 8, 15, ys)
qe("Linear vs quadratic", A, "Equation I contains |x|, the absolute value of x. Find every real x and y and choose "
   "the relation between them.", "x² − 4|x| + 3 = 0", "y² + 8y + 15 = 0", xs, ys, ">=", [">", "<="],
   "Since x² = |x|², equation I is a quadratic in |x|; each positive |x| gives two values of x",
   "I: |x|² − 4|x| + 3 = 0, so |x| = 1 or 3, giving x = −3, −1, 1, 3. II: (y + 3)(y + 5) = 0, so y = −3 or −5. The "
   "smallest x (−3) equals the largest y (−3), and every other pair has x > y. So x ≥ y.",
   ["I: (|x| − 1)(|x| − 3) = 0 ⇒ x = ±1, ±3", "II: y = −3, −5", "min x = −3 = max y", "So x ≥ y"],
   why="x > y misses the negative roots of I (x = −3 = y); x ≤ y holds only for that pair.", secs=90)

# ================================================================ Number System (B2 I3 A2)
T = "Number System"
h = math.gcd(math.gcd(84, 126), 210)
assert h == 42 and (84 + 126 + 210) // h == 10 and (84 + 126 + 210) // 21 == 20 and (84 + 126 + 210) // 14 == 30
Q(T, "HCF and LCM", B,
  "Three ropes 84 m, 126 m and 210 m long are to be cut into pieces of equal length, with no rope left over. The "
  "pieces are to be as long as possible. How many pieces will there be in all?",
  "10", ["20", "30", "42"],
  "The longest equal piece that divides every rope is the HCF of the lengths",
  "HCF(84, 126, 210) = 42 m. Pieces: 84 ÷ 42 + 126 ÷ 42 + 210 ÷ 42 = 2 + 3 + 5 = 10.",
  ["84 = 2² × 3 × 7, 126 = 2 × 3² × 7, 210 = 2 × 3 × 5 × 7", "HCF = 2 × 3 × 7 = 42", "2 + 3 + 5 = 10 pieces"],
  why="20 and 30 use 21 m or 14 m pieces, which are common divisors but not the greatest; 42 is the piece length, "
      "not the number of pieces.", secs=45)

L = math.lcm(12, 18, 21)
cands = [n for n in range(100, 1000) if all(n % d == 5 for d in (12, 18, 21))]
assert L == 252 and cands[-1] == 761 and 252 * 3 == 756 and 252 * 4 + 5 == 1013 and 999 - 999 % 252 == 756
Q(T, "Remainders", B,
  "What is the largest three-digit number that leaves a remainder of 5 when divided by each of 12, 18 and 21?",
  "761", ["756", "1,013", "751"],
  "Such numbers are 5 more than a multiple of LCM(12, 18, 21)",
  "LCM(12, 18, 21) = 252. Multiples of 252 below 1,000: 252, 504, 756. The largest required number is 756 + 5 = 761.",
  ["LCM = 2² × 3² × 7 = 252", "Largest multiple ≤ 994 = 756", "756 + 5 = 761"],
  why="756 forgets to add the remainder; 1,013 (1,008 + 5) has four digits; 751 subtracts 5 instead of adding it.",
  secs=50)

vals = {(n * n + 3 * n) % 6 for n in range(4, 400, 6)}
assert vals == {4} and (4 * 4) % 6 == 4 and (16 + 3) % 6 == 1 and (16 + 7) % 6 == 5
Q(T, "Remainders", I,
  "When a number n is divided by 6, the remainder is 4. What is the remainder when n² + 3n is divided by 6?",
  "4", ["1", "0", "5"],
  "Replace n by its remainder: n² + 3n leaves the same remainder as 4² + 3 × 4",
  "n = 6k + 4, so n² + 3n leaves the same remainder as 16 + 12 = 28 when divided by 6. 28 = 4 × 6 + 4, so the "
  "remainder is 4.",
  ["n ≡ 4 (mod 6)", "n² + 3n ≡ 16 + 12 = 28", "28 ÷ 6 leaves 4"],
  why="1 uses 16 + 3 (forgetting to multiply 3 by n); 0 assumes n² + 3n = n(n + 3) must be a multiple of 6, but "
      "4 × 7 = 28 is not; 5 treats 3n as 3 + n (16 + 7 = 23 leaves 5).", secs=55)


def sigma(n):
    return sum(d for d in range(1, n + 1) if n % d == 0)


assert sigma(360) == 1170 == 15 * 13 * 6 and sum(1 for d in range(1, 361) if 360 % d == 0) == 24 and sigma(360) - 360 == 810
Q(T, "Divisibility", I, "What is the sum of all the factors (divisors) of 360, including 1 and 360?",
  "1,170", ["810", "24", "1,080"],
  "For n = 2ᵃ × 3ᵇ × 5ᶜ, the sum of divisors is (1 + 2 + … + 2ᵃ)(1 + 3 + … + 3ᵇ)(1 + 5 + … + 5ᶜ)",
  "360 = 2³ × 3² × 5. Sum of divisors = (1 + 2 + 4 + 8)(1 + 3 + 9)(1 + 5) = 15 × 13 × 6 = 1,170.",
  ["360 = 2³ × 3² × 5", "(1 + 2 + 4 + 8) = 15", "(1 + 3 + 9) = 13, (1 + 5) = 6", "15 × 13 × 6 = 1,170"],
  why="810 leaves out 360 itself; 24 is the number of divisors, not their sum; 1,080 is three times 360, not a divisor "
      "sum.", secs=60)

h, Lc = 21, 1008
assert 49 * h == 1029 and Lc == 48 * h and h * Lc // 63 == 336 and math.gcd(63, 336) == 21 and math.lcm(63, 336) == 1008
Q(T, "HCF and LCM", I,
  "The LCM of two numbers is 48 times their HCF, and the sum of their HCF and LCM is 1,029. If one of the numbers is "
  "63, what is the other?",
  "336", ["1,008", "16", "48"],
  "HCF × LCM = product of the two numbers",
  "HCF + 48 × HCF = 49 × HCF = 1,029, so HCF = 21 and LCM = 1,008. The other number = 21 × 1,008 ÷ 63 = 336. Check: "
  "HCF(63, 336) = 21 and LCM(63, 336) = 1,008.",
  ["49 × HCF = 1,029 ⇒ HCF = 21", "LCM = 48 × 21 = 1,008", "Other = 21 × 1,008 ÷ 63 = 336"],
  why="1,008 is the LCM, not the second number; 16 is 1,008 ÷ 63, which forgets to multiply by the HCF; 48 is the "
      "ratio LCM ÷ HCF.", secs=70)


def legendre(n, p):
    e, q = 0, p
    while q <= n:
        e += n // q
        q *= p
    return e


e2, e3 = legendre(40, 2), legendre(40, 3)
assert (e2, e3) == (38, 18) and min(e2 // 2, e3) == 18 and 40 // 12 == 3 and e2 // 2 == 19
Q(T, "Divisibility", A, "What is the highest power of 12 that divides 40! (the product 1 × 2 × 3 × … × 40) exactly?",
  "18", ["19", "3", "38"],
  "12 = 2² × 3: count the 2s and the 3s in 40! and see which runs out first",
  "Number of 2s in 40! = 20 + 10 + 5 + 2 + 1 = 38, enough for 19 copies of 2². Number of 3s = 13 + 4 + 1 = 18. Each 12 "
  "needs one 3, so only 18 copies of 12 divide 40!.",
  ["2s: 40/2 + 40/4 + 40/8 + 40/16 + 40/32 = 38 ⇒ 19 pairs", "3s: 40/3 + 40/9 + 40/27 = 13 + 4 + 1 = 18",
   "Limit = min(19, 18) = 18"],
  why="19 counts only the pairs of 2s; 3 counts only the multiples of 12 up to 40; 38 counts the single 2s.", secs=85)

assert pow(7, 100, 100) == 1 and pow(7, 4) == 2401 and pow(7, 2, 100) == 49 and pow(7, 3, 100) == 43
Q(T, "Unit digit", A, "What are the last two digits of 7¹⁰⁰?",
  "01", ["49", "43", "07"],
  "7⁴ = 2,401 ends in 01, and any power of a number ending in 01 also ends in 01",
  "7⁴ = 2,401, which ends in 01. 7¹⁰⁰ = (7⁴)²⁵, and numbers ending in 01 multiply to numbers ending in 01, so 7¹⁰⁰ "
  "ends in 01.",
  ["7² = 49, 7³ = 343, 7⁴ = 2,401", "7¹⁰⁰ = (7⁴)²⁵", "Last two digits: 01"],
  short="The last two digits of powers of 7 repeat in the cycle 07, 49, 43, 01; 100 is a multiple of 4.",
  why="49, 43 and 07 are the last two digits of 7², 7³ and 7¹; 100 is a multiple of 4, so the cycle ends at 01.",
  secs=75)

# ================================================================ Percentage (B1 I2 A2)
T = "Percentage"
run = 110 - (3 * 6 + 8 * 4)
v = F(run, 110) * 100
assert run == 60 and v == F(600, 11) and F(50, 110) * 100 == F(500, 11) and F(60, 100) * 100 == 60
Q(T, "Basic percentage", B,
  "A batter scored 110 runs, including 3 sixes and 8 fours. What percentage of his runs did he make by running "
  "between the wickets?",
  "54 6/11%", ["45 5/11%", "60%", "40%"],
  "Runs from boundaries = 6 × sixes + 4 × fours; the rest came from running",
  "Boundaries: 3 × 6 + 8 × 4 = 18 + 32 = 50 runs. Running: 110 − 50 = 60 runs = 60/110 × 100 = 54 6/11%.",
  ["Boundary runs = 18 + 32 = 50", "Running = 110 − 50 = 60", "60 ÷ 110 × 100 = 54 6/11%"],
  why="45 5/11% is the boundary share; 60% divides the running runs by 100 instead of 110; 40% subtracts the 50 "
      "boundary runs from 100 and divides by 100.", secs=45)

dry = F(45) * F(20, 100) / F(90, 100)
assert dry == 10 and F(45) * F(20, 100) == 9 and F(45) * F(10, 100) == F(9, 2) and F(45) * F(20, 100) / F(80, 100) == F(45, 4)
Q(T, "Basic percentage", I,
  "Fresh grapes contain 80% water by weight, while raisins made from them contain 10% water. How many kilograms of "
  "raisins can be made from 45 kg of fresh grapes?",
  "10 kg", ["9 kg", "4.5 kg", "11.25 kg"],
  "Drying removes only water: the solid part stays the same",
  "Solid in the grapes = 20% of 45 = 9 kg. In the raisins this 9 kg is 90% of the weight, so the raisins weigh "
  "9 ÷ 0.9 = 10 kg.",
  ["Solid = 20% × 45 = 9 kg", "Raisins: solid = 90%", "Weight = 9 ÷ 0.9 = 10 kg"],
  why="9 kg is the solid alone, ignoring the 10% water left in the raisins; 4.5 kg is 10% of 45; 11.25 kg divides 9 "
      "by 0.8, mixing up the two water percentages.", secs=60)

I_, E_ = F(100), F(80)
S_ = I_ - E_
newE = I_ * F(115, 100) - S_
assert (newE - E_) / E_ * 100 == F(75, 4) and F(15, 100) * 100 / 80 * 100 == F(75, 4) and F(15) == 15
assert (I_ * F(115, 100) * F(80, 100) - E_) / E_ * 100 == 15
Q(T, "Income and expenditure", I,
  "Meena spends 80% of her income and saves the rest. Her income rises by 15%, but she keeps her savings the same in "
  "rupees. By what percentage does her expenditure rise?",
  "18.75%", ["15%", "75%", "12%"],
  "All the extra income goes into expenditure; compare that extra with the old expenditure",
  "Take income = 100: expenditure 80, savings 20. New income = 115 and savings stay 20, so expenditure = 95. Rise = "
  "15 on 80 = 18.75%.",
  ["Income 100 ⇒ spend 80, save 20", "New income 115, savings 20 ⇒ spend 95", "Rise = 15/80 = 18.75%"],
  why="15% assumes expenditure grows at the same rate as income; 75% divides the extra 15 by the savings (20) instead of the "
      "expenditure (80); 12% takes 80% of the 15% rise in income.", secs=60)

v = (1 - F(112, 118)) * 100
assert r2(v) == F(508, 100) and F(6, 100) * 100 == 6 and r2(F(6, 112) * 100) == F(536, 100)
Q(T, "Successive change", A,
  "A refrigerator's price includes 18% GST on its pre-tax price. The GST rate is cut to 12% while the pre-tax price "
  "does not change. By what percentage does the price paid by the buyer fall (correct to two decimal places)?",
  "5.08%", ["6.00%", "5.36%", "33.33%"],
  "Final price ∝ (1 + GST rate); compare 1.12 with 1.18",
  "With a pre-tax price of 100, the buyer paid 118 and now pays 112. The fall is 6 on 118 = 5.08%.",
  ["Old price = 118", "New price = 112", "Fall = 6 ÷ 118 × 100 = 5.08%"],
  why="6.00% is the cut in percentage points of tax, not the change in price; 5.36% divides 6 by the new price 112; "
      "33.33% is the fall in the tax rate itself (6 on 18).", secs=70)

r_ = (F(12) - F(96, 10)) / (F(96, 10) - 8)
assert r_ == F(3, 2) and (3 * F(8, 100) + 2 * F(12, 100)) / 5 == F(96, 1000)
Q(T, "Population and depreciation", A,
  "In a village, the number of men rose by 8% and the number of women by 12% over a year, and the total population "
  "rose by 9.6%. What was the ratio of men to women at the start of the year?",
  "3 : 2", ["2 : 3", "1 : 1", "4 : 3"],
  "The overall rate is a weighted average of the two rates; use alligation",
  "Men : women = (12 − 9.6) : (9.6 − 8) = 2.4 : 1.6 = 3 : 2. Check: (3 × 8% + 2 × 12%) ÷ 5 = 9.6%.",
  ["Alligation: 12 − 9.6 = 2.4", "9.6 − 8 = 1.6", "2.4 : 1.6 = 3 : 2"],
  why="2 : 3 reverses the alligation; 1 : 1 would give 10%; 4 : 3 would give about 9.71%.", secs=70)

# ================================================================ Ratio and Proportion (B2 I3 A3)
T = "Ratio and Proportion"
ang = [F(180 * k, 12) for k in (2, 3, 7)]
assert ang == [30, 45, 105] and sum(ang) == 180
Q(T, "Basic ratio", B, "The angles of a triangle are in the ratio 2 : 3 : 7. What is the largest angle?",
  "105°", ["30°", "45°", "70°"],
  "The three angles add up to 180°",
  "2 + 3 + 7 = 12 parts = 180°, so one part = 15°. Largest angle = 7 × 15° = 105°.",
  ["12 parts = 180°", "1 part = 15°", "7 × 15° = 105°"],
  why="30° and 45° are the other two angles; 70° takes one part as 10°.", secs=35)

k_ = F(8000, 4)
assert (5 * k_ + 4000) / (7 * k_ + 4000) == F(7, 9) and 5 * k_ == 10000 and 7 * k_ == 14000 and 5 * k_ + 4000 == 14000
Q(T, "Coins and salary share", B,
  "The monthly salaries of A and B are in the ratio 5 : 7. If each gets an increment of ₹4,000, the ratio becomes "
  "7 : 9. What is A's present salary?",
  "₹10,000", ["₹14,000", "₹8,000", "₹18,000"],
  "Let the salaries be 5k and 7k; the increment is added to both",
  "(5k + 4,000) ÷ (7k + 4,000) = 7/9 ⇒ 45k + 36,000 = 49k + 28,000 ⇒ 4k = 8,000 ⇒ k = 2,000. A's salary = 5k = "
  "₹10,000.",
  ["9(5k + 4,000) = 7(7k + 4,000)", "45k + 36,000 = 49k + 28,000", "k = 2,000", "A = 5 × 2,000 = ₹10,000"],
  why="₹14,000 is B's present salary (or A's new salary); ₹8,000 is 4k; ₹18,000 is B's new salary.", secs=50)

xv, yv = F(3), F(4)
assert (4 * xv * xv - yv * yv) / (xv * xv + yv * yv) == F(4, 5) and (4 * 3 - 4) / F(3 + 4) == F(8, 7)
assert (36 - 16) / F(9 - 16) == F(-20, 7)
Q(T, "Proportion", I, "If x : y = 3 : 4, what is (4x² − y²) : (x² + y²)?",
  "4 : 5", ["8 : 7", "4 : 25", "5 : 4"],
  "Put x = 3k and y = 4k; k² cancels",
  "4x² − y² = 4 × 9k² − 16k² = 20k² and x² + y² = 9k² + 16k² = 25k². Ratio = 20 : 25 = 4 : 5.",
  ["x = 3k, y = 4k", "4x² − y² = 36k² − 16k² = 20k²", "x² + y² = 25k²", "20 : 25 = 4 : 5"],
  why="8 : 7 uses x and y without squaring (4 × 3 − 4 : 3 + 4); 4 : 25 takes 4x² − y² as (2x − y)² = 4k²; "
      "5 : 4 inverts the answer.", secs=55)

k_ = F(28, 7)
m_, d_ = 9 * k_, 2 * k_
n_ = (m_ - 3 * d_) / 2
assert (m_, d_) == (36, 8) and n_ == 6 and (m_ + n_) == 3 * (d_ + n_)
Q(T, "Ages via ratio", I,
  "The present ages of a mother and her daughter are in the ratio 9 : 2, and the mother is 28 years older than the "
  "daughter. After how many years will the mother be exactly three times as old as the daughter?",
  "6 years", ["4 years", "8 years", "12 years"],
  "The age gap (7 parts) is fixed at 28 years",
  "7 parts = 28 years, so 1 part = 4: mother 36, daughter 8. In n years: 36 + n = 3(8 + n) ⇒ 36 + n = 24 + 3n ⇒ "
  "n = 6. Check: 42 = 3 × 14.",
  ["9k − 2k = 28 ⇒ k = 4", "Mother 36, daughter 8", "36 + n = 3(8 + n) ⇒ n = 6"],
  why="4 years is one part (k); 8 years is the daughter's present age; 12 years gives 48 and 20, a ratio of 2.4.",
  secs=60)

c_ = F(4200, 3 * 3 + 4 * F(3, 2) + 6)
assert c_ == 200 and 3 * (3 * c_) + 4 * (F(3, 2) * c_) + 6 * c_ == 4200 and F(4200, 13) != 200
Q(T, "Coins and salary share", I,
  "₹4,200 is shared among 3 men, 4 women and 6 children so that each man gets twice as much as each woman, and each "
  "woman gets 1½ times as much as each child. How much does each child get?",
  "₹200", ["₹300", "₹600", "₹323.08"],
  "Express every share in terms of one child's share c: woman = 1.5c, man = 3c",
  "Total = 3 × 3c + 4 × 1.5c + 6 × c = 9c + 6c + 6c = 21c = 4,200, so c = ₹200 (woman ₹300, man ₹600).",
  ["Woman = 1.5c, man = 2 × 1.5c = 3c", "9c + 6c + 6c = 21c", "21c = 4,200 ⇒ c = 200"],
  why="₹300 and ₹600 are a woman's and a man's shares; ₹323.08 divides 4,200 by the 13 people as if all shares were "
      "equal.", secs=60)

r_ = F(54, 2) ** F(1, 3)
assert 3 ** 3 == 27 and 2 * 3 ** 3 == 54 and 2 * 3 + 2 * 9 == 24 and 6 * 18 == 2 * 54
Q(T, "Proportion", A, "If 2, x, y and 54 are in continued proportion, what is the value of x + y?",
  "24", ["56", "18", "36"],
  "In continued proportion each term is the previous one times the same ratio r: 2, 2r, 2r², 2r³",
  "2r³ = 54 ⇒ r³ = 27 ⇒ r = 3. So x = 6 and y = 18, and x + y = 24. Check: 2 : 6 = 6 : 18 = 18 : 54.",
  ["2r³ = 54 ⇒ r = 3", "x = 6, y = 18", "x + y = 24"],
  why="56 adds the end terms 2 and 54; 18 is y alone; 36 takes x and y as 9 and 27 (the ratio 3 applied from 3 "
      "instead of from 2).", secs=60)

k_ = F(16, 2)
A_, B_ = 5 * k_ + 4, 4 * k_ + 4
assert k_ == 8 and (A_, B_) == (44, 36) and (A_ + 4) / (B_ - 4) == F(3, 2) and (A_ - 4) / (B_ - 4) == F(5, 4)
Q(T, "Ages via ratio", A,
  "Four years ago, the ages of A and B were in the ratio 5 : 4. The ratio of A's age four years from now to B's age "
  "four years ago is 3 : 2. What is the sum of their present ages?",
  "80 years", ["72 years", "88 years", "44 years"],
  "Let A − 4 = 5k and B − 4 = 4k; then A + 4 = 5k + 8",
  "(5k + 8) ÷ 4k = 3/2 ⇒ 10k + 16 = 12k ⇒ k = 8. So A = 44 and B = 36, and the sum is 80 years.",
  ["A − 4 = 5k, B − 4 = 4k", "(5k + 8)/(4k) = 3/2 ⇒ k = 8", "A = 44, B = 36", "Sum = 80"],
  why="72 years is the sum four years ago; 88 years is the sum four years from now; 44 years uses A's present age "
      "instead of his age four years from now in the second ratio ((5k + 4)/4k = 3/2 gives k = 4).", secs=80)

var = F(7700 - 5600, 300)
fix = 5600 - 600 * var
assert var == 7 and fix == 1400 and fix + 1200 * var == 9800 and F(5600, 600) * 1200 == 11200 and 7700 + 2100 == 9800
Q(T, "Proportion", A,
  "The monthly cost of running a delivery van is partly fixed and partly proportional to the distance driven. It "
  "costs ₹5,600 in a month in which the van covers 600 km and ₹7,700 in a month in which it covers 900 km. What will "
  "it cost in a month in which it covers 1,200 km?",
  "₹9,800", ["₹11,200", "₹10,500", "₹8,400"],
  "The extra cost of the extra distance gives the cost per km; the rest is the fixed part",
  "300 extra km cost 7,700 − 5,600 = ₹2,100, so ₹7 per km. Fixed part = 5,600 − 600 × 7 = ₹1,400. For 1,200 km: "
  "1,400 + 1,200 × 7 = ₹9,800.",
  ["Per km = 2,100 ÷ 300 = ₹7", "Fixed = 5,600 − 4,200 = ₹1,400", "1,200 km: 1,400 + 8,400 = ₹9,800"],
  why="₹11,200 treats the whole cost as proportional to distance (5,600 × 2); ₹10,500 is 7,700 × 1,200/900, the same "
      "mistake from the other month; ₹8,400 forgets the fixed part.", secs=85)

# ================================================================ Problems on Ages (B1 I1 A2)
T = "Problems on Ages"
c_ = F(61 - 13, 3)
assert c_ == 16 and c_ + 8 == 24 and c_ + (c_ + 5) + (c_ + 8) == 61
Q(T, "Present and future ages", B,
  "A is 3 years older than B, and B is 5 years older than C. The sum of the present ages of A, B and C is 61 years. "
  "How old is A?",
  "24 years", ["21 years", "16 years", "26 years"],
  "Write every age in terms of C's age",
  "C = c, B = c + 5, A = c + 8. Then 3c + 13 = 61, so c = 16 and A = 24 years.",
  ["A + B + C = (c + 8) + (c + 5) + c = 3c + 13", "3c = 48 ⇒ c = 16", "A = 16 + 8 = 24"],
  why="21 years is B's age; 16 years is C's age; 26 years adds 3 and 5 to B instead of to C.", secs=40)

x_ = F(10 * 5, 1)
assert x_ / 4 == F(25, 2) and x_ == F(5, 4) * (x_ - 10) and x_ == F(5, 6) * (x_ + 10)
Q(T, "Present and future ages", I,
  "A man's present age is 125% of what it was 10 years ago, and 83⅓% of what it will be 10 years from now. What is "
  "his present age?",
  "50 years", ["40 years", "60 years", "45 years"],
  "125% = 5/4 and 83⅓% = 5/6; either condition gives the age, and the other checks it",
  "x = (5/4)(x − 10) ⇒ 4x = 5x − 50 ⇒ x = 50. Check: (5/6) × 60 = 50 ✓.",
  ["x = 1.25(x − 10)", "x = 50", "Check: 5/6 of 60 = 50"],
  why="40 years is his age 10 years ago; 60 years is his age 10 years from now; 45 years satisfies neither condition.",
  secs=55)

sols = [(m - d, m, m + d) for m in range(1, 40) for d in range(1, 20) if 3 * m == 39 and (m - d) * (m + d) == 153]
assert sols == [(9, 13, 17)]
Q(T, "Present and future ages", A,
  "The present ages of three sisters are in arithmetic progression (equal gaps). The sum of their ages is 39 years "
  "and the product of the youngest and the eldest sisters' ages is 153. What is the eldest sister's age?",
  "17 years", ["13 years", "21 years", "9 years"],
  "Let the ages be m − d, m, m + d; the sum fixes m",
  "3m = 39 ⇒ m = 13. Then (13 − d)(13 + d) = 169 − d² = 153 ⇒ d = 4. The ages are 9, 13 and 17, so the eldest is "
  "17.",
  ["3m = 39 ⇒ m = 13", "169 − d² = 153 ⇒ d = 4", "Ages 9, 13, 17"],
  why="13 years is the middle sister; 9 years is the youngest; 21 years takes d = 8 (from 169 − 153 = 16 without the "
      "square root).", secs=75)

r_ = F(80, 4)
assert r_ == 20 and 40 + (40 - r_) == 3 * r_ and 40 + (40 - 10) != 3 * 10
Q(T, "Ratio-based ages", A,
  "When Ravi reaches his father's present age, his father will be three times as old as Ravi is now. Ravi's father "
  "is 40 years old now. How old is Ravi now?",
  "20 years", ["10 years", "13⅓ years", "60 years"],
  "Ravi reaches 40 after (40 − r) years; the father ages by the same amount",
  "If Ravi is r now, he reaches 40 after 40 − r years, when his father will be 40 + (40 − r) = 80 − r. So 80 − r = "
  "3r ⇒ r = 20.",
  ["Gap = 40 − r years", "Father then = 80 − r", "80 − r = 3r ⇒ r = 20"],
  why="10 years subtracts the gap from the father's age instead of adding it (40 − r = 3r); 13⅓ years uses the father's present age "
      "(40 = 3r); 60 years is the father's age at that future time.", secs=70)

# ================================================================ Average (B1 I2 A1)
T = "Average"
v = F(sum(k * k for k in range(1, 11)), 10)
assert v == F(77, 2) and F(55, 10) ** 2 == F(121, 4) and F(385, 11) == 35
Q(T, "Simple average", B, "What is the average of the squares of the first ten natural numbers (1², 2², …, 10²)?",
  "38.5", ["30.25", "35", "55"],
  "1² + 2² + … + n² = n(n + 1)(2n + 1)/6",
  "Sum = 10 × 11 × 21 ÷ 6 = 385. Average = 385 ÷ 10 = 38.5.",
  ["Sum = 10 × 11 × 21 / 6 = 385", "Average = 385 ÷ 10 = 38.5"],
  why="30.25 squares the average of 1 to 10 (5.5²); 35 divides 385 by 11; 55 is the sum of 1 to 10, not of squares.",
  secs=40)

rest = F(8 * 25 - 3 * 18 - 3 * 33, 2)
assert rest == F(47, 2) and (25 * 8 - 18 - 33) / F(2) == F(149, 2)
Q(T, "Simple average", I,
  "The average of 8 numbers is 25. The average of the smallest three of them is 18 and the average of the largest "
  "three is 33. What is the average of the remaining two numbers?",
  "23.5", ["25", "74.5", "47"],
  "Total of all = 8 × average; subtract the totals of the two groups of three",
  "Total = 8 × 25 = 200. Smallest three = 54 and largest three = 99. Remaining two = 200 − 54 − 99 = 47, so their "
  "average is 23.5.",
  ["Total = 200", "3 × 18 = 54, 3 × 33 = 99", "200 − 153 = 47", "47 ÷ 2 = 23.5"],
  why="25 assumes the middle numbers share the overall average; 74.5 subtracts the two averages (18 and 33) instead of "
      "the two totals; 47 is the total of the two numbers, not their average.", secs=55)

p_ = (70 - F(7, 10) * 64) / F(3, 10)
assert p_ == 84 and (64 + 84) / 2 == 74 and 2 * 70 - 64 == 76
Q(T, "Weighted average", I,
  "In a course, the final score is a weighted average of the theory mark (weight 70%) and the practical mark "
  "(weight 30%). A student scored 64 in theory and got a final score of 70. What did she score in the practical?",
  "84", ["76", "74", "90"],
  "Final = 0.7 × theory + 0.3 × practical",
  "0.7 × 64 = 44.8. So 0.3 × practical = 70 − 44.8 = 25.2 and the practical mark = 25.2 ÷ 0.3 = 84.",
  ["0.7 × 64 = 44.8", "0.3 × P = 25.2", "P = 84"],
  why="76 treats the two parts as equally weighted (2 × 70 − 64); 74 is the simple average of 64 and 84; 90 gives a "
      "final score of 71.8.", secs=60)

w_ = F(5 * 12 - 26, F(4, 10))
assert w_ == 85 and (F(124, 10) * w_ + 26) / (w_ + 5) == 12 and F(26, 5) == F(52, 10) and F(60, F(4, 10)) == 150
Q(T, "Replacement", A,
  "A bowler had conceded an average of 12.4 runs per wicket. In his next match he took 5 wickets for 26 runs, and his "
  "average fell by 0.4. How many wickets had he taken before this match?",
  "85", ["90", "80", "150"],
  "Runs = average × wickets; write the new average as total runs ÷ total wickets",
  "If he had w wickets: (12.4w + 26) ÷ (w + 5) = 12 ⇒ 12.4w + 26 = 12w + 60 ⇒ 0.4w = 34 ⇒ w = 85.",
  ["Old runs = 12.4w", "(12.4w + 26)/(w + 5) = 12", "0.4w = 34 ⇒ w = 85"],
  why="90 counts the wickets after the match (85 + 5); 80 subtracts the 5 new wickets; 150 forgets the 26 runs of the new "
      "match (12.4w = 12w + 60).", secs=90)

# ================================================================ Profit and Loss (B2 I2 A1)
T = "Profit and Loss"
cp = F(90, F(15, 100))
assert cp == 600 and cp * F(90, 100) + 90 == cp * F(105, 100) and F(90, F(5, 100)) == 1800
Q(T, "Cost and selling price", B,
  "A trader sells a table at a loss of 10%. Had he sold it for ₹90 more, he would have gained 5%. What is the cost "
  "price of the table?",
  "₹600", ["₹900", "₹1,800", "₹540"],
  "The ₹90 bridges a 10% loss and a 5% gain, i.e. 15% of the cost",
  "From 90% of the cost to 105% of the cost is 15%. So 15% of CP = ₹90 and CP = 90 ÷ 0.15 = ₹600.",
  ["Loss 10% → gain 5%: a 15% swing", "0.15 × CP = 90", "CP = ₹600"],
  why="₹900 takes ₹90 as 10% of the cost; ₹1,800 takes it as 5%; ₹540 is the selling price at a 10% loss.", secs=40)

cp = F(22500, F(125, 100))
assert cp == 18000 and F(22500) * F(75, 100) == 16875 and F(22500, F(120, 100)) == 18750
Q(T, "Marked price", B,
  "A shopkeeper marks a television at ₹22,500, which is 25% above its cost price. What is the cost price?",
  "₹18,000", ["₹16,875", "₹18,750", "₹17,500"],
  "Marked price = 125% of cost, so cost = marked price ÷ 1.25",
  "CP × 1.25 = 22,500 ⇒ CP = 22,500 ÷ 1.25 = ₹18,000.",
  ["MP = 1.25 × CP", "CP = 22,500 ÷ 1.25 = 18,000"],
  why="₹16,875 takes 25% off the marked price; ₹18,750 divides by 1.2; ₹17,500 subtracts a flat ₹5,000.", secs=35)

n_ = F(60000 + 30000, 700 - 400)
assert n_ == 300 and F(60000, 300) == 200 and F(90000, 700) != 300
Q(T, "Cost and selling price", I,
  "A workshop has fixed costs of ₹60,000 a month. Each chair costs ₹400 in materials and labour and sells for ₹700. "
  "How many chairs must it make and sell in a month to earn a profit of ₹30,000?",
  "300", ["200", "100", "129"],
  "Each chair contributes SP − variable cost towards the fixed cost and the profit",
  "Each chair contributes 700 − 400 = ₹300. Needed: 60,000 + 30,000 = ₹90,000, so 90,000 ÷ 300 = 300 chairs.",
  ["Contribution per chair = ₹300", "Fixed cost + profit = ₹90,000", "90,000 ÷ 300 = 300 chairs"],
  why="200 only covers the fixed cost (break-even); 100 covers only the profit; 129 divides 90,000 by the full price "
      "of ₹700.", secs=55)

k_ = F(420, F(4, 10) + F(3, 10))
assert k_ == 600 and 5 * k_ == 3000 and 2 * k_ * F(12, 10) + 3 * k_ * F(11, 10) == 3420
Q(T, "Cost and selling price", I,
  "The cost prices of two articles are in the ratio 2 : 3. The first is sold at a profit of 20% and the second at a "
  "profit of 10%, and the total profit is ₹420. What is the total cost price of the two articles?",
  "₹3,000", ["₹2,800", "₹2,100", "₹4,200"],
  "Write the costs as 2k and 3k; profit = 0.2 × 2k + 0.1 × 3k",
  "Profit = 0.4k + 0.3k = 0.7k = 420, so k = 600. Total cost = 5k = ₹3,000.",
  ["Costs 2k and 3k", "0.4k + 0.3k = 0.7k = 420", "k = 600 ⇒ total = 5k = ₹3,000"],
  why="₹2,800 divides 420 by a simple average profit of 15%; ₹2,100 assumes 20% on the whole; ₹4,200 assumes "
      "10% on the whole.", secs=60)

pv = F(125, 100) / (1 + F(10, 100) * F(1, 2))
assert r2((pv - 1) * 100) == F(1905, 100) and r2((F(125, 110) - 1) * 100) == F(1364, 100) and F(125 - 5, 100) - 1 == F(20, 100)
Q(T, "Cost and selling price", A,
  "A dealer sells a machine at 25% above his cost, with payment due 6 months later. Money is worth 10% per annum "
  "simple interest. What is his true profit percentage, measured in today's money (correct to two decimal places)?",
  "19.05%", ["25.00%", "20.00%", "13.64%"],
  "Bring the future payment to today: present worth = amount ÷ (1 + rate × time)",
  "Take cost = 100. He receives 125 after 6 months; its present worth = 125 ÷ (1 + 0.10 × ½) = 125 ÷ 1.05 = 119.05. "
  "True profit = 19.05%.",
  ["Amount due = 125", "Present worth = 125 ÷ 1.05 = 119.05", "Profit = 19.05%"],
  why="25.00% ignores the delay in payment; 20.00% subtracts the 5% interest from 25% instead of dividing; 13.64% "
      "discounts for a full year instead of six months (125 ÷ 1.1).", secs=90)

# ================================================================ Discount (B1 I1 A1)
T = "Discount"
c_ = F(168, F(140 - 112, 100))
assert c_ == 600 and c_ * F(140, 100) - 168 == c_ * F(112, 100) and F(168, F(12, 100)) == 1400
Q(T, "Discount with profit", B,
  "A shopkeeper marks a lamp 40% above its cost price. He allows a discount of ₹168 and still makes a profit of 12%. "
  "What is the cost price of the lamp?",
  "₹600", ["₹1,400", "₹840", "₹672"],
  "The discount equals the gap between the marked price (140% of cost) and the selling price (112% of cost)",
  "Discount = 140% − 112% = 28% of cost = ₹168, so cost = 168 ÷ 0.28 = ₹600.",
  ["MP = 1.4C, SP = 1.12C", "0.28C = 168", "C = ₹600"],
  why="₹1,400 takes ₹168 as 12% of the cost; ₹840 is the marked price; ₹672 is the selling price.", secs=45)

v = 1 - F(1 + F(1, 2), 2)
assert v == F(1, 4)
Q(T, "Single discount", I,
  "A shop sells socks at a fixed price per pair but runs an offer: 'Buy one pair at full price and get the second "
  "pair at half price.' What single discount on two pairs is this offer equal to?",
  "25%", ["50%", "33⅓%", "20%"],
  "Compare what is paid for two pairs with their full price",
  "For two pairs worth 2 units, the buyer pays 1 + 0.5 = 1.5 units. Discount = 0.5 on 2 = 25%.",
  ["Full price for 2 pairs = 2", "Paid = 1.5", "Discount = 0.5 ÷ 2 = 25%"],
  why="50% is the discount on the second pair alone; 33⅓% divides the saving by the amount paid (0.5 ÷ 1.5); 20% "
      "is the 'buy 4, get 1 free' equivalent.", secs=45)

dsol = [F(d, 100) for d in range(1, 100) if 3 * (1 - F(d, 100)) == 2 * (1 + F(d, 100))]
assert dsol == [F(1, 5)] and F(1, 3) * 100 != 20 and F(3 - 2, 3) == F(1, 3)
Q(T, "Discount with profit", A,
  "The cost price and the marked price of an article are in the ratio 2 : 3. The shopkeeper sells it at a discount, "
  "and his discount percentage equals his profit percentage. What is the discount percentage?",
  "20%", ["33⅓%", "50%", "25%"],
  "Let CP = 2 and MP = 3; then SP = 3(1 − d) = 2(1 + d)",
  "3(1 − d) = 2(1 + d) ⇒ 3 − 3d = 2 + 2d ⇒ d = 1/5 = 20%. Check: SP = 2.4, a 20% discount on 3 and a 20% profit on 2.",
  ["CP = 2, MP = 3", "3 − 3d = 2 + 2d", "d = 20%", "SP = 2.4"],
  why="33⅓% is the discount that brings MP down to CP (no profit); 50% is the mark-up over cost; 25% gives SP = 2.25, "
      "a 12.5% profit.", secs=75)

# ================================================================ Simple Interest (B1 I1 A1)
T = "Simple Interest"
g = 8000 * F(12 - 9, 100) * 2
assert g == 480 and 8000 * F(12, 100) * 2 == 1920 and 8000 * F(3, 100) == 240
Q(T, "Basic SI", B,
  "Ravi borrows ₹8,000 at 9% per annum simple interest and at once lends the same sum at 12% per annum simple "
  "interest. What is his gain over 2 years?",
  "₹480", ["₹240", "₹1,920", "₹1,440"],
  "Gain per year = sum × (difference in rates)",
  "He earns 12% and pays 9%, so he gains 3% of 8,000 = ₹240 a year, or ₹480 in 2 years.",
  ["Rate gap = 3%", "3% of 8,000 = ₹240 per year", "2 years ⇒ ₹480"],
  why="₹240 is the gain for one year only; ₹1,920 is the interest he receives; ₹1,440 is the interest he pays.",
  secs=40)

t_ = F(5000 - 4000, 4000 * F(12, 100) - 5000 * F(8, 100))
assert t_ == F(25, 2) and 5000 + 400 * t_ == 4000 + 480 * t_ == 10000
Q(T, "Basic SI", I,
  "₹5,000 is lent at 8% per annum simple interest and ₹4,000 at 12% per annum simple interest, both on the same day. "
  "After how many years will the two amounts be equal?",
  "12½ years", ["10 years", "25 years", "12 years"],
  "The smaller sum grows ₹80 a year faster; it must close a gap of ₹1,000",
  "Yearly interest: 8% of 5,000 = ₹400; 12% of 4,000 = ₹480. The gap of ₹1,000 closes at ₹80 a year, so it takes "
  "1,000 ÷ 80 = 12½ years (both amounts are then ₹10,000).",
  ["Interest per year: 400 and 480", "Gap 1,000 closes by 80 a year", "t = 12.5 years", "Check: 5,000 + 5,000 = "
   "4,000 + 6,000"],
  why="10 years leaves amounts of ₹9,000 and ₹8,800; 25 years doubles the answer; 12 years leaves ₹9,800 and ₹9,760.",
  secs=55)

pw = F(40710, 1 + F(10, 100) * F(3, 2))
assert pw == 35400 and pw - 35000 == 400 and 40710 - 35000 * F(115, 100) == 460
Q(T, "Basic SI", A,
  "A shopkeeper can sell a machine for ₹35,000 in cash today, or for ₹40,710 payable 18 months from now. Money earns "
  "10% per annum simple interest. Which offer is better for him, and by how much in today's money?",
  "The credit offer, by ₹400", ["The cash offer, by ₹400", "The credit offer, by ₹460",
                                "The credit offer, by ₹5,710"],
  "Compare present worths: present worth = amount ÷ (1 + rate × time)",
  "Present worth of ₹40,710 due in 1.5 years = 40,710 ÷ (1 + 0.10 × 1.5) = 40,710 ÷ 1.15 = ₹35,400. That is ₹400 "
  "more than the ₹35,000 cash price, so the credit offer is better by ₹400.",
  ["Interest factor = 1 + 0.15 = 1.15", "Present worth = 40,710 ÷ 1.15 = 35,400", "35,400 − 35,000 = ₹400"],
  why="'The cash offer' gets the direction wrong; ₹460 compares the amounts 18 months from now (40,710 − 40,250), not "
      "today; ₹5,710 ignores interest altogether.", secs=85)

# ================================================================ Compound Interest (B1 I1 A1)
T = "Compound Interest"
ci = 50000 * (F(11, 10) ** 2 - 1)
si = 50000 * F(11, 100) * 2
assert ci == 10500 and si == 11000 and si - ci == 500
Q(T, "Annual compounding", B,
  "Asha invests ₹50,000 for 2 years at 10% per annum compound interest, compounded annually. Bina invests ₹50,000 "
  "for 2 years at 11% per annum simple interest. Who earns more interest, and by how much?",
  "Bina, by ₹500", ["Asha, by ₹500", "Bina, by ₹1,000", "Asha, by ₹10,500"],
  "CI for 2 years = P[(1 + r)² − 1]; SI = P × r × t",
  "Asha: 50,000 × (1.1² − 1) = 50,000 × 0.21 = ₹10,500. Bina: 50,000 × 0.11 × 2 = ₹11,000. Bina earns ₹500 more.",
  ["CI = 50,000 × 0.21 = 10,500", "SI = 50,000 × 0.22 = 11,000", "Difference = ₹500 (Bina)"],
  why="'Asha, by ₹500' gets the direction wrong; ₹1,000 compares 11% SI with 10% SI; 'Asha, by ₹10,500' quotes her "
      "interest, not the difference.", secs=50)

hy = 20000 * (F(105, 100) ** 2 - 1)
assert hy == 2050 and hy - 20000 * F(10, 100) == 50 and 20000 * (F(11, 10) - 1) == 2000
Q(T, "Half-yearly and quarterly", I,
  "On ₹20,000 for 1 year at 10% per annum, by how much does the compound interest compounded half-yearly exceed the "
  "simple interest?",
  "₹50", ["₹0", "₹100", "₹2,050"],
  "Half-yearly: rate 5% per half-year for 2 half-years",
  "CI = 20,000 × (1.05² − 1) = 20,000 × 0.1025 = ₹2,050. SI = 10% of 20,000 = ₹2,000. Excess = ₹50.",
  ["1.05² = 1.1025", "CI = ₹2,050", "SI = ₹2,000", "Excess = ₹50"],
  why="₹0 treats yearly compounding as half-yearly (for 1 year annual CI equals SI); ₹100 doubles the excess; ₹2,050 "
      "is the CI itself.", secs=55)

r_ = F(11, 10) - 1
P_ = F(1000) / r_
assert 1000 * (1 + r_) ** 2 == 1210 and P_ == 10000 and 3 * P_ * r_ == 3000 and P_ * r_ * (1 + r_) ** 2 == 1210
Q(T, "CI vs SI difference", A,
  "On a certain sum, the simple interest for 3 years is ₹3,000, and the compound interest (compounded annually, at "
  "the same rate) for the third year alone is ₹1,210. What is the sum?",
  "₹10,000", ["₹12,100", "₹1,000", "₹11,000"],
  "SI for one year = P × r; the CI for the third year = P × r × (1 + r)²",
  "SI per year = 3,000 ÷ 3 = ₹1,000 = P × r. Third-year CI = 1,000 × (1 + r)² = 1,210 ⇒ (1 + r)² = 1.21 ⇒ r = 10%. "
  "Then P = 1,000 ÷ 0.10 = ₹10,000.",
  ["P × r = 1,000", "1,000(1 + r)² = 1,210 ⇒ r = 10%", "P = ₹10,000"],
  why="₹12,100 divides the third-year interest by the rate; ₹1,000 is one year's simple interest; ₹11,000 is the "
      "amount after one year.", secs=85)

# ================================================================ Partnership (B3 I2 A1)
T = "Partnership"
q_ = F(2100, F(10, 100))
tot = q_ * F(12, 7)
assert q_ == 21000 and tot == 36000 and F(2100 * 12, 5) == 5040 and F(21000 * 12, 5) == 50400
Q(T, "Simple partnership", B,
  "P and Q invest in a business in the ratio 5 : 7 for the same period. Q gives 10% of his share of the year's "
  "profit to charity, and this amounts to ₹2,100. What was the total profit?",
  "₹36,000", ["₹21,000", "₹50,400", "₹25,200"],
  "Q's share = 7/12 of the profit; 10% of Q's share = ₹2,100",
  "Q's share = 2,100 ÷ 0.10 = ₹21,000, which is 7/12 of the profit. Total = 21,000 × 12/7 = ₹36,000.",
  ["Q's share = 2,100 × 10 = 21,000", "7/12 of profit = 21,000", "Profit = ₹36,000"],
  why="₹21,000 is Q's share only; ₹50,400 takes Q's share as 5/12 of the profit; ₹25,200 is 21,000 × 6/5, mixing "
      "the ratio terms.", secs=45)

a_, b_ = 20000 * 9, 15000 * 12
assert a_ == b_ == 180000 and F(13200, 2) == 6600 and F(13200 * 4, 7) != 6600
Q(T, "Compound partnership", B,
  "A invests ₹20,000 for 9 months and B invests ₹15,000 for 12 months in a business. Out of a profit of ₹13,200, "
  "what is A's share?",
  "₹6,600", ["₹7,543", "₹5,657", "₹4,400"],
  "Profit is shared in the ratio of capital × time",
  "A: 20,000 × 9 = 1,80,000; B: 15,000 × 12 = 1,80,000. The ratio is 1 : 1, so A gets half of ₹13,200 = ₹6,600.",
  ["A: 20,000 × 9 = 1,80,000", "B: 15,000 × 12 = 1,80,000", "Ratio 1 : 1 ⇒ ₹6,600 each"],
  why="₹7,543 shares by capital only (4 : 3); ₹5,657 is B's share on that wrong ratio; ₹4,400 shares by time only "
      "₹4,400 gives A only one-third of the profit, as if B's "
      "capital-months were twice A's.", secs=40)

b_ = F(5000, 3 - 2) * 2
assert b_ == 10000 and b_ + 5000 == 15000 and F(15000, b_) == F(3, 2)
Q(T, "Simple partnership", B,
  "A and B invest in a business for the same period. A's capital is ₹5,000 more than B's, and they share the profit "
  "in the ratio 3 : 2. What is B's capital?",
  "₹10,000", ["₹15,000", "₹5,000", "₹7,500"],
  "With equal periods, capitals are in the ratio of the profits",
  "A : B = 3 : 2, so the difference of 1 part = ₹5,000. B's capital = 2 parts = ₹10,000 (A has ₹15,000).",
  ["Capitals 3k and 2k", "3k − 2k = 5,000 ⇒ k = 5,000", "B = 2k = ₹10,000"],
  why="₹15,000 is A's capital; ₹5,000 is one part; ₹7,500 takes the difference as 2/3 of B's capital.", secs=40)

A_ = 40000 * 3 + 30000 * 6 + 50000 * 3
B_ = 50000 * 12
assert (A_, B_) == (450000, 600000) and F(56000 * A_, A_ + B_) == 24000 and F(56000 * 4, 9) != 24000
Q(T, "Compound partnership", I,
  "A starts a business with ₹40,000 and B with ₹50,000. After 3 months A withdraws 25% of his capital, and 6 months "
  "after that he adds ₹20,000. B keeps his capital unchanged. Out of a profit of ₹56,000 at the end of the year, what "
  "is A's share?",
  "₹24,000", ["₹24,889", "₹32,000", "₹28,000"],
  "Add capital × months over the three periods for A",
  "A: 40,000 × 3 + 30,000 × 6 + 50,000 × 3 = 1,20,000 + 1,80,000 + 1,50,000 = 4,50,000. B: 50,000 × 12 = 6,00,000. "
  "Ratio 3 : 4, so A gets 3/7 × 56,000 = ₹24,000.",
  ["A: 1,20,000 + 1,80,000 + 1,50,000 = 4,50,000", "B: 6,00,000", "Ratio 3 : 4", "A = 3/7 × 56,000 = ₹24,000"],
  why="₹24,889 uses the starting capitals only (4 : 5); ₹32,000 is B's share; ₹28,000 splits the profit equally."
  , secs=75)

P_ = F(9600, F(48, 100) - F(32, 100))
assert P_ == 60000 and P_ * F(20, 100) == 12000 and F(9600, F(20, 100)) == 48000
Q(T, "Working partner", I,
  "A and B invest ₹60,000 and ₹40,000 in a shop. C joins as a working partner without capital and receives 20% of "
  "the profit for running the shop; the rest is shared between A and B in the ratio of their capitals. If B "
  "receives ₹9,600 less than A, what is the total profit?",
  "₹60,000", ["₹48,000", "₹12,000", "₹75,000"],
  "A gets 60% of the remaining 80%, B gets 40% of it",
  "A's share = 0.6 × 0.8P = 0.48P; B's share = 0.4 × 0.8P = 0.32P. Difference = 0.16P = 9,600, so P = ₹60,000 (C "
  "gets ₹12,000).",
  ["Remaining = 0.8P", "A = 0.48P, B = 0.32P", "0.16P = 9,600 ⇒ P = ₹60,000"],
  why="₹48,000 is the profit after C's 20%; ₹12,000 is C's share; ₹75,000 forgets C's share and takes 0.128P as the "
      "difference.", secs=65)

A_ = 45000 * 6 + 30000 * 6
B_ = 30000 * 8
C_ = 60000 * 6
assert (A_, B_, C_) == (450000, 240000, 360000) and F(140000 * C_, A_ + B_ + C_) == 48000
assert F(140000 * 360000, 540000 + 240000 + 360000) != 48000
Q(T, "Compound partnership", A,
  "A starts a business with ₹45,000. After 4 months B joins with ₹30,000. Two months after B joins, A withdraws "
  "one-third of his capital and C joins with ₹60,000. Out of a profit of ₹1,40,000 at the end of the year, what is "
  "C's share?",
  "₹48,000", ["₹44,211", "₹32,000", "₹60,000"],
  "Track each partner's capital month by month: A changes after 6 months",
  "A: 45,000 × 6 + 30,000 × 6 = 4,50,000. B: 30,000 × 8 = 2,40,000. C: 60,000 × 6 = 3,60,000. Ratio 45 : 24 : 36 = "
  "15 : 8 : 12. C = 12/35 × 1,40,000 = ₹48,000.",
  ["A: 2,70,000 + 1,80,000 = 4,50,000", "B: 2,40,000", "C: 3,60,000", "15 : 8 : 12 ⇒ C = 12/35 × 1,40,000"],
  why="₹44,211 ignores A's withdrawal (A = 5,40,000); ₹32,000 is B's share; ₹60,000 is A's share "
      "(15/35 of ₹1,40,000).", secs=100)

# ================================================================ Mixture and Alligation (B1 I4 A3)
T = "Mixture and Alligation"
r_ = F(50 - 30, 30 - 20)
assert r_ == 2 and 60 * F(2, 3) == 40 and (40 * F(20, 100) + 20 * F(50, 100)) / 60 == F(3, 10)
Q(T, "Mixing solutions", B,
  "How many litres of a 20% salt solution must be mixed with a 50% salt solution to make 60 litres of a 30% "
  "solution?",
  "40 litres", ["20 litres", "30 litres", "36 litres"],
  "Alligation: (50 − 30) : (30 − 20) gives the ratio of the 20% and 50% solutions",
  "20% : 50% = (50 − 30) : (30 − 20) = 20 : 10 = 2 : 1. So the 20% solution is 2/3 of 60 = 40 litres. Check: 8 + 10 = "
  "18 litres of salt = 30% of 60.",
  ["Ratio = 20 : 10 = 2 : 1", "20% solution = 2/3 × 60 = 40 L", "Salt: 8 + 10 = 18 L = 30% ✓"],
  why="20 litres is the 50% solution; 30 litres splits equally; 36 litres is 60% of the total.", secs=45)

left = [F(3, 4) ** n for n in range(1, 5)]
assert left[1] > F(1, 2) > left[2] and left[2] == F(27, 64)
Q(T, "Replacement of mixture", I,
  "A 20-litre can is full of pure milk. 5 litres are taken out and replaced with water, and this is repeated. After "
  "how many such operations will the milk first fall below half of the can?",
  "3", ["2", "4", "5"],
  "After each operation the milk is multiplied by (1 − 5/20) = 3/4",
  "Milk fraction after n operations = (3/4)ⁿ: 0.75, 0.5625, 0.4219, … It first falls below 0.5 after the third "
  "operation (milk = 20 × 27/64 ≈ 8.44 litres).",
  ["Factor per operation = 3/4", "(3/4)² = 0.5625 > 0.5", "(3/4)³ = 0.4219 < 0.5", "Answer: 3"],
  why="2 leaves 11.25 litres of milk, still above 10; 4 and 5 are later than the first time it drops below half.",
  secs=60)

T_ = F(9) + F(63 * 9, 21)
mk, wt = F(7, 9) * (T_ - 9), F(2, 9) * (T_ - 9) + 9
assert T_ == 36 and mk / wt == F(7, 5)
Q(T, "Replacement of mixture", I,
  "A vessel contains milk and water in the ratio 7 : 2. When 9 litres of the mixture are taken out and replaced "
  "with water, the ratio becomes 7 : 5. How many litres of mixture did the vessel hold?",
  "36 litres", ["27 litres", "45 litres", "54 litres"],
  "Removing mixture keeps the 7 : 2 ratio; only the added 9 litres of water change it",
  "If the vessel holds T litres, after removing 9 litres it has 7(T − 9)/9 milk and 2(T − 9)/9 water; adding 9 "
  "litres of water: 7(T − 9)/9 : 2(T − 9)/9 + 9 = 7 : 5. So 5 × 7(T − 9)/9 = 7 × 2(T − 9)/9 + 63, i.e. "
  "21(T − 9)/9 = 63, T − 9 = 27, T = 36.",
  ["Milk = 7(T − 9)/9, water = 2(T − 9)/9 + 9", "35(T − 9)/9 = 14(T − 9)/9 + 63", "T − 9 = 27 ⇒ T = 36",
   "Check: 21 milk, 6 + 9 = 15 water ⇒ 7 : 5"],
  why="27 litres is what remains after removal; 45 and 54 litres give 7 : 4.6 and 7 : 4.25, not 7 : 5.", secs=80)

r_ = F(15 - 9, 19 - 15)
assert r_ == F(3, 2) and (3 * 19 + 2 * 9) / F(5) == 15
Q(T, "Alligation rule", I,
  "Gold is 19 times as heavy as water and copper is 9 times as heavy as water. In what ratio must gold and copper be "
  "mixed to get an alloy 15 times as heavy as water?",
  "3 : 2", ["2 : 3", "4 : 6", "5 : 3"],
  "Alligation on the relative weights (19 and 9) with mean 15",
  "Gold : copper = (15 − 9) : (19 − 15) = 6 : 4 = 3 : 2. Check: (3 × 19 + 2 × 9) ÷ 5 = 75 ÷ 5 = 15.",
  ["Gold: 15 − 9 = 6", "Copper: 19 − 15 = 4", "6 : 4 = 3 : 2"],
  why="2 : 3 reverses the alligation; 4 : 6 is the same reversed ratio unreduced; 5 : 3 gives (95 + 27) ÷ 8 = 15.25.",
  secs=50)

cp = F(26 * 20 + 30 * 36)
sp = 56 * 30
assert cp == 1600 and sp == 1680 and (sp - cp) / cp * 100 == 5 and F(30 * 2 - 56, 56) * 100 != 5
Q(T, "Alligation rule", I,
  "A grocer mixes 26 kg of rice costing ₹20 per kg with 30 kg costing ₹36 per kg, and sells the mixture at ₹30 per "
  "kg. What is his profit percentage?",
  "5%", ["7.14%", "4.76%", "6.67%"],
  "Find the cost of the whole mixture, then compare with its selling price",
  "Cost = 26 × 20 + 30 × 36 = 520 + 1,080 = ₹1,600 for 56 kg. Selling price = 56 × 30 = ₹1,680. Profit = 80 on 1,600 "
  "= 5%.",
  ["Cost = 520 + 1,080 = 1,600", "SP = 56 × 30 = 1,680", "Profit = 80/1,600 = 5%"],
  why="7.14% takes the cost per kg as the simple average ₹28; 4.76% divides the profit by the selling price; 6.67% "
      "uses the simple average cost ₹28 and divides the ₹2 profit by the selling price ₹30.", secs=60)
assert r2((F(30, 28) - 1) * 100) == F(714, 100) and r2(F(80, 1680) * 100) == F(476, 100)

A_m, A_w = F(30) * F(3, 4), F(30) * F(1, 4)
B_m, B_w = F(15) + F(10) * F(3, 4), F(15) + F(10) * F(1, 4)
tm, tw = B_m * F(10, 40), B_w * F(10, 40)
fm, fw = A_m + tm, A_w + tw
assert (fm, fw) == (F(225, 8), F(95, 8)) and fm / fw == F(45, 19)
Q(T, "Mixing solutions", A,
  "Vessel A holds 40 litres of milk and water in the ratio 3 : 1, and vessel B holds 30 litres of milk and water in "
  "the ratio 1 : 1. 10 litres are poured from A into B and mixed well, and then 10 litres are poured from B back into "
  "A. What is the ratio of milk to water in A now?",
  "45 : 19", ["3 : 1", "9 : 7", "11 : 5"],
  "Track milk and water separately; a poured quantity carries its vessel's current ratio",
  "A keeps 30 L (22.5 milk, 7.5 water). B becomes 40 L: 15 + 7.5 = 22.5 milk and 15 + 2.5 = 17.5 water. 10 L of B "
  "carries 5.625 milk and 4.375 water back to A. A: 28.125 milk, 11.875 water = 225 : 95 = 45 : 19.",
  ["A after pouring: 22.5 milk, 7.5 water", "B: 22.5 milk, 17.5 water (40 L)", "Back 10 L: 5.625 milk, 4.375 water",
   "A: 28.125 : 11.875 = 45 : 19"],
  why="3 : 1 is A's original ratio; 9 : 7 is B's ratio after the first pour; 11 : 5 returns 10 L of B's original "
      "1 : 1 mixture (27.5 : 12.5), ignoring what A poured into B.", secs=110)

sol = [(a, b) for a in range(0, 61) for b in range(0, 61) if 2 * a + b == 60 and 10 * a + 20 * a + 40 * b == 25 * 60]
assert sol == [(18, 24)]
Q(T, "Mixing solutions", A,
  "Solutions with 10%, 20% and 40% acid are mixed to make 60 litres of a 25% acid solution. Equal volumes of the 10% "
  "and the 20% solutions are used. How many litres of the 40% solution are used?",
  "24 litres", ["18 litres", "20 litres", "30 litres"],
  "Let a litres each of the 10% and 20% solutions and b litres of the 40%; write the volume and the acid equations",
  "Volume: 2a + b = 60. Acid: 0.1a + 0.2a + 0.4b = 0.25 × 60 = 15. Substituting b = 60 − 2a: 0.3a + 24 − 0.8a = 15 ⇒ "
  "a = 18, b = 24.",
  ["2a + b = 60", "0.3a + 0.4b = 15", "a = 18, b = 24"],
  why="18 litres is the amount of each weaker solution; 20 litres splits the 60 litres equally; 30 litres treats the "
      "10% and 20% as one 15% solution mixed with the 40% solution 1 : 1.", secs=95, by=BRUTE)

w_ = F(1, 6)
m_ = 1 - w_
assert (m_ * F(4, 5)) / (w_ * F(4, 5) + F(1, 5)) == 2 and m_ / w_ == 5
Q(T, "Replacement of mixture", A,
  "A vessel is full of a mixture of milk and water. One-fifth of the mixture is taken out and replaced with water, "
  "after which milk and water are in the ratio 2 : 1. What was the ratio of milk to water at first?",
  "5 : 1", ["5 : 2", "3 : 1", "2 : 1"],
  "Removing a fifth of the mixture leaves four-fifths of each liquid; then water is added",
  "Take the vessel as 1 unit with m milk and w water (m + w = 1). After the replacement: milk 0.8m, water 0.8w + 0.2. "
  "0.8m = 2(0.8w + 0.2) and m = 1 − w give 0.8 − 0.8w = 1.6w + 0.4 ⇒ w = 1/6, m = 5/6. Ratio 5 : 1.",
  ["Milk 0.8m, water 0.8w + 0.2", "0.8m = 1.6w + 0.4", "m + w = 1 ⇒ w = 1/6", "m : w = 5 : 1"],
  why="5 : 2 and 3 : 1 give final ratios 4 : 3.6 and 2.4 : 1.6, not 2 : 1; 2 : 1 is the final ratio, not the "
      "starting one.", secs=95)

# ================================================================ Time and Work (B2 I2 A1)
T = "Time and Work"
need = 12 * 2
assert F(2, 3) / F(1, 3) * 12 == 24 and need - 12 == 12
Q(T, "Work efficiency", B,
  "12 men complete one-third of a job in 8 days. How many more men must join them so that the rest of the job is "
  "finished in the next 8 days?",
  "12", ["24", "6", "8"],
  "In equal time, the number of men needed is proportional to the work left",
  "The rest is 2/3 of the job, twice the work done. To do twice the work in the same 8 days needs 24 men, so 12 more "
  "men must join.",
  ["Done: 1/3 by 12 men in 8 days", "Left: 2/3 = twice as much", "Men needed = 24", "Extra = 24 − 12 = 12"],
  why="24 is the total number of men needed, not the extra men; 6 halves instead of doubling; 8 takes 2/3 of 12 "
      "men.", secs=45)

w_ = F(600 * 3, 5)
assert w_ == 360 and 3 * 600 * 12 == 5 * w_ * 12
Q(T, "Men-women-children", B,
  "3 men or 5 women can finish a job in 12 days. A man is paid ₹600 a day, and wages are in proportion to the work "
  "done. What is a woman's daily wage?",
  "₹360", ["₹1,000", "₹200", "₹120"],
  "3 men do as much as 5 women, so 1 woman does 3/5 of a man's daily work",
  "3 men = 5 women in work, so a woman's daily work (and wage) is 3/5 of a man's: 3/5 × 600 = ₹360.",
  ["3 men ≡ 5 women", "Woman = 3/5 man", "Wage = 0.6 × 600 = ₹360"],
  why="₹1,000 uses 5/3 instead of 3/5; ₹200 divides 600 by 3; ₹120 divides 600 by 5.", secs=40)

sol = [b for b in range(2, 100) if 4 * (F(1, 12) - F(1, b)) + 18 * F(1, b) == 1]
assert sol == [21] and 1 / (F(1, 12) - F(1, 21)) == 28
Q(T, "Work efficiency", I,
  "A and B together can finish a job in 12 days. A works alone for 4 days, and then B works alone for 18 days and "
  "completes the job. In how many days can B alone finish it?",
  "21 days", ["28 days", "18 days", "24 days"],
  "Pair 4 days of A with 4 days of B as 4 days of joint work",
  "Think of it as A and B together for 4 days (4/12 = 1/3 of the job) plus B alone for 14 more days. So 14 days of B = "
  "2/3 of the job, and B alone needs 14 × 3/2 = 21 days.",
  ["4 days of A + 4 days of B = 1/3 of the job", "B's other 14 days = 2/3", "B alone = 21 days"],
  why="28 days is A's time alone; 18 days is B's working time here, not B's time for the whole job; 24 days doubles "
      "the joint time.", secs=65)

rate = F(1, 8) + F(1, 12)
left = 1 - 2 * rate
hrs = left * 12
assert left == F(7, 12) and hrs == 7 and 11 + hrs == 18
Q(T, "Work efficiency", I,
  "A can finish a job in 8 hours and B in 12 hours. They start together at 9:00 AM, but A leaves at 11:00 AM. At what "
  "time does B finish the job?",
  "6:00 PM", ["1:48 PM", "2:00 PM", "8:00 PM"],
  "Find the work done together in the first 2 hours; B does the rest alone",
  "Together they do 1/8 + 1/12 = 5/24 per hour; in 2 hours, 5/12. B does the remaining 7/12 at 1/12 per hour, taking "
  "7 hours: 11:00 AM + 7 h = 6:00 PM.",
  ["Joint rate = 5/24 per hour", "By 11 AM: 5/12 done", "B: 7/12 ÷ 1/12 = 7 h", "Finish at 6:00 PM"],
  why="1:48 PM assumes both work throughout (24/5 h from 9 AM); 2:00 PM is 5 hours after 9 AM; 8:00 PM "
      "has B working 9 hours.", secs=60)


def build_demolish(a, b):
    w, day = F(0), 0
    while True:
        day += 1
        w += a if day % 2 else -b
        if w >= 1:
            return day


d_ = build_demolish(F(1, 10), F(1, 15))
assert d_ == 55 and 27 * (F(1, 10) - F(1, 15)) + F(1, 10) == 1 and F(1, F(1, 30)) * 2 == 60
Q(T, "Alternate days", A,
  "A mason can build a wall in 10 days, and a wrecker can knock the same wall down in 15 days. They work on alternate "
  "days, the mason starting on day 1. On which day is the wall first completed?",
  "Day 55", ["Day 60", "Day 30", "Day 59"],
  "Each 2-day cycle adds 1/10 − 1/15 = 1/30 of the wall, but the last mason's day finishes it before the wrecker "
  "returns",
  "After 2k days, k/30 of the wall stands. On day 2k + 1 the mason adds 1/10, so the wall is complete when k/30 + 1/10 "
  "≥ 1, i.e. k ≥ 27. So it is completed on day 2 × 27 + 1 = 55.",
  ["Net per 2 days = 1/30", "After 54 days: 27/30 = 0.9", "Day 55: 0.9 + 0.1 = 1 ✓"],
  why="Day 60 divides the whole wall by the 2-day net (30 cycles) and ignores the final mason day; day 30 counts "
      "cycles, not days; day 59 adds two extra cycles.", secs=100, by=BRUTE)

# ================================================================ Pipes and Cisterns (B1 I1 A2)
T = "Pipes and Cisterns"
assert F(450, 15) == 30 and F(450, 30 + 20) == 9
Q(T, "Inlet and outlet", B,
  "Tap A fills a 450-litre tank in 15 minutes. Tap B delivers 20 litres per minute. If both taps are opened on the "
  "empty tank, how long will it take to fill?",
  "9 minutes", ["22.5 minutes", "15 minutes", "37.5 minutes"],
  "Convert both taps to litres per minute and add",
  "A delivers 450 ÷ 15 = 30 L/min; with B the total is 50 L/min. Time = 450 ÷ 50 = 9 minutes.",
  ["A = 30 L/min", "A + B = 50 L/min", "450 ÷ 50 = 9 min"],
  why="22.5 minutes is B alone; 15 minutes is A alone; 37.5 minutes adds the two times.", secs=40)

done10 = 2 * F(1, 4) + F(1, 6)
rest = 1 - done10
rate = F(1, 4) + F(1, 6) + F(1, 12)
assert done10 == F(2, 3) and rest / rate * 60 == 40
Q(T, "Inlet and outlet", I,
  "Pipes A, B and C can fill a tank in 4, 6 and 12 hours respectively. A is opened on the empty tank at 8:00 AM, B "
  "at 9:00 AM and C at 10:00 AM. At what time will the tank be full?",
  "10:40 AM", ["10:00 AM", "11:00 AM", "10:20 AM"],
  "Add up what has been filled by 10:00 AM, then use the combined rate of all three",
  "By 10 AM: A has run 2 hours (1/2) and B 1 hour (1/6), so 2/3 is full. All three together fill 1/4 + 1/6 + 1/12 = "
  "1/2 per hour, so the last 1/3 takes 2/3 hour = 40 minutes. Full at 10:40 AM.",
  ["By 10 AM: 1/2 + 1/6 = 2/3", "Combined rate = 1/2 per hour", "1/3 ÷ 1/2 = 40 min", "10:40 AM"],
  why="10:00 AM assumes the tank is full when C opens; 11:00 AM adds an hour for the last third; 10:20 AM uses the "
      "rate of A and B only for 1/6 of the tank.", secs=70)

out_frac = F(1, 30) + F(1, 45) - F(1, 36)
cap = 6 / out_frac
assert out_frac == F(1, 36) and cap == 216 and 6 * 36 == 216
Q(T, "Leak problems", A,
  "Two inlet pipes can fill a tank in 30 minutes and 45 minutes. A leak at the bottom drains 6 litres per minute. "
  "With both pipes open and the leak working, the empty tank fills in 36 minutes. What is the capacity of the tank?",
  "216 litres", ["108 litres", "270 litres", "180 litres"],
  "Inlet rate − leak rate = 1/36 of the tank per minute; find the leak's share",
  "The inlets fill 1/30 + 1/45 = 1/18 of the tank per minute. Net rate = 1/36, so the leak removes 1/18 − 1/36 = "
  "1/36 of the tank per minute = 6 litres. Capacity = 6 × 36 = 216 litres.",
  ["Inlets: 1/30 + 1/45 = 1/18 per min", "Leak = 1/18 − 1/36 = 1/36 per min", "1/36 of tank = 6 L ⇒ 216 L"],
  why="108 litres takes the leak as 1/18 of the tank; 270 litres uses 45 minutes in place of 36; 180 litres uses 30 "
      "minutes.", secs=90)

sol = [x for x in range(1, 60) if F(1, x) + F(1, x + 5) == F(1, 6)]
assert sol == [10]
Q(T, "Inlet and outlet", A,
  "Pipe B takes 5 hours longer than pipe A to fill a tank. Together they fill it in 6 hours. How long does pipe A "
  "alone take?",
  "10 hours", ["15 hours", "12 hours", "5 hours"],
  "1/x + 1/(x + 5) = 1/6 leads to a quadratic in x",
  "6(x + 5) + 6x = x(x + 5) ⇒ x² − 7x − 30 = 0 ⇒ (x − 10)(x + 3) = 0 ⇒ x = 10 hours (B takes 15 hours). Check: "
  "1/10 + 1/15 = 1/6 ✓.",
  ["1/x + 1/(x + 5) = 1/6", "x² − 7x − 30 = 0", "x = 10 (reject −3)"],
  why="15 hours is pipe B; 12 hours is twice the joint time, true only for two equal pipes; 5 hours is the difference between the "
      "two pipes' times.", secs=85)

# ================================================================ Speed, Time and Distance (B1 I3 A2)
T = "Speed, Time and Distance"
car = F(300, 5)
train = car * F(125, 100)
assert train == 75 and 450 / train == 6 and 450 / car == F(15, 2) and 450 / (car * F(75, 100)) == 10
Q(T, "Average speed", B,
  "A car covers 300 km in 5 hours. A train runs 25% faster than the car. How long will the train take to cover "
  "450 km?",
  "6 hours", ["7.5 hours", "10 hours", "4.8 hours"],
  "Car speed = distance ÷ time; train speed = 1.25 × car speed",
  "Car speed = 300 ÷ 5 = 60 km/h. Train speed = 1.25 × 60 = 75 km/h. Time for 450 km = 450 ÷ 75 = 6 hours.",
  ["Car = 60 km/h", "Train = 75 km/h", "450 ÷ 75 = 6 h"],
  why="7.5 hours uses the car's speed; 10 hours makes the train 25% slower; 4.8 hours is 6 × 0.8.", secs=40)

t_ = F(12, 10) / (15 - 9) * 60
assert t_ == 12 and F(12, 10) / 24 * 60 == 3
Q(T, "Relative speed", I,
  "Two runners start together from the same point on a 1.2 km circular track and run in the same direction at "
  "9 km/h and 15 km/h. After how many minutes will the faster runner first catch up with the slower one?",
  "12 minutes", ["3 minutes", "8 minutes", "4.8 minutes"],
  "To meet again, the faster runner must gain one full lap at the relative speed",
  "Relative speed = 15 − 9 = 6 km/h. Gaining 1.2 km takes 1.2 ÷ 6 = 0.2 hour = 12 minutes.",
  ["Relative speed = 6 km/h", "Gain needed = 1.2 km", "Time = 0.2 h = 12 min"],
  why="3 minutes uses the sum of the speeds (opposite directions); 8 minutes is one lap at 9 km/h; 4.8 minutes is one "
      "lap at 15 km/h.", secs=50)

t_ = 1 / (F(1, 4) + F(1, 6))
assert t_ == F(12, 5) and t_ * 60 == 144 and F(4 + 6, 2) == 5
Q(T, "Meeting and overtaking", I,
  "A walks from town P to town Q in 4 hours and B walks from Q to P in 6 hours. If they start at the same time, after "
  "how long will they meet?",
  "2 hours 24 minutes", ["5 hours", "2 hours", "3 hours"],
  "Take the distance as 1: A covers 1/4 and B covers 1/6 of it per hour",
  "Together they close 1/4 + 1/6 = 5/12 of the distance per hour, so they meet after 12/5 hours = 2 hours 24 minutes.",
  ["Combined = 5/12 of the distance per hour", "Time = 12/5 h", "= 2 h 24 min"],
  why="5 hours averages the two times; 2 hours halves A's time; 3 hours halves B's time.", secs=55)

t_ = F(100, 5)
assert t_ == 20 and 6 * t_ == 120 and 2 * t_ == 40
Q(T, "Relative speed", I,
  "A is twice as fast as B, and B is three times as fast as C. On the same route, C takes 1 hour 40 minutes longer "
  "than A. How long does C take?",
  "2 hours", ["1 hour 40 minutes", "20 minutes", "40 minutes"],
  "Time is inversely proportional to speed: if A takes t, B takes 2t and C takes 6t",
  "Speeds A : B : C = 6 : 3 : 1, so times are t : 2t : 6t. C − A = 5t = 100 minutes ⇒ t = 20 minutes. C takes "
  "6 × 20 = 120 minutes = 2 hours.",
  ["Times t, 2t, 6t", "5t = 100 min ⇒ t = 20 min", "C = 120 min = 2 h"],
  why="1 hour 40 minutes is the difference itself; 20 minutes is A's time; 40 minutes is B's time.", secs=60)

c_run = 900 * F(900, 1000)
assert c_run == 810 and 1000 - c_run == 190
Q(T, "Meeting and overtaking", A,
  "In a 1 km race, A beats B by 100 m, and in another 1 km race B beats C by 100 m. Running at the same speeds, by how "
  "many metres would A beat C in a 1 km race?",
  "190 m", ["200 m", "100 m", "180 m"],
  "Speeds are in the ratio of distances covered in the same time",
  "When A runs 1,000 m, B runs 900 m. When B runs 1,000 m, C runs 900 m, so when B runs 900 m, C runs 810 m. Hence "
  "when A finishes, C has run 810 m and A wins by 190 m.",
  ["A : B = 1,000 : 900", "B : C = 1,000 : 900", "A : C = 1,000 : 810", "Lead = 190 m"],
  why="200 m simply adds the two margins; 100 m assumes the margins do not combine; 180 m takes 90% of 200 m.",
  secs=70)

T3 = [F(1200, v) for v in (3, 5, 7)]
lcm_t = F(math.lcm(*[int(t * 7) for t in T3]), 7)
assert 1200 % 600 == 0 and F(1200, 7 - 5) == 600
assert T3 == [400, 240, F(1200, 7)] and lcm_t == 1200 and 1200 // 400 == 3 and 1200 // 240 == 5
assert all((lcm_t / t).denominator == 1 for t in T3) and 1200 * 3 == 3600
Q(T, "Meeting and overtaking", A,
  "Three cyclists start together from the same point on a 1,200 m circular track and ride in the same direction at "
  "3 m/s, 5 m/s and 7 m/s. After how many seconds will all three be together at the starting point for the first "
  "time?",
  "1,200 seconds", ["2,400 seconds", "8,400 seconds", "600 seconds"],
  "Each returns to the start after 1,200 ÷ speed seconds; find the LCM of these times",
  "Lap times: 400 s, 240 s and 1,200/7 s. As multiples of 1/7 s these are 2,800, 1,680 and 1,200, whose LCM is 8,400; "
  "so all three are first together at the start after 8,400/7 = 1,200 seconds, having done 3, 5 and 7 laps.",
  ["Lap times 400, 240, 1,200/7 s", "LCM = 1,200 s", "Laps: 3, 5, 7 (all whole)"],
  short="In 1,200 s a rider at v m/s covers 1,200v m = v laps, a whole number for every integer speed.",
  why="2,400 seconds is the second meeting at the start; 8,400 seconds is a later common time; 600 seconds is "
      "when the two faster riders first meet anywhere on the track, not at the start.", secs=90)

# ================================================================ Boats and Streams (B1 I2 A1)
T = "Boats and Streams"
up = F(12) / F(48, 60)
assert up == 15 and up + 3 == 18 and up - 3 == 12 and up + 6 == 21
Q(T, "Upstream and downstream", B,
  "A boat covers 12 km upstream in 48 minutes. The stream flows at 3 km/h. What is the speed of the boat in still "
  "water?",
  "18 km/h", ["15 km/h", "12 km/h", "21 km/h"],
  "Upstream speed = boat speed − stream speed",
  "Upstream speed = 12 ÷ 0.8 h = 15 km/h. Boat speed = 15 + 3 = 18 km/h.",
  ["48 min = 0.8 h", "Upstream = 15 km/h", "Boat = 15 + 3 = 18 km/h"],
  why="15 km/h is the upstream speed; 12 km/h subtracts the stream again; 21 km/h is the downstream speed.", secs=40)

sol = [(5 * s, s) for s in range(1, 20) if F(72, 4 * s) - F(72, 6 * s) == 3]
assert sol == [(10, 2)]
Q(T, "Speed of stream", I,
  "The speed of a boat in still water is five times the speed of the stream. The boat takes 3 hours longer to cover "
  "72 km upstream than to cover 72 km downstream. What is the speed of the boat in still water?",
  "10 km/h", ["2 km/h", "12 km/h", "8 km/h"],
  "With stream speed s, the boat moves at 4s upstream and 6s downstream",
  "72/(4s) − 72/(6s) = 18/s − 12/s = 6/s = 3, so s = 2 km/h and the boat's speed is 5 × 2 = 10 km/h. Check: 72 ÷ 8 = "
  "9 h upstream, 72 ÷ 12 = 6 h downstream.",
  ["Upstream 4s, downstream 6s", "18/s − 12/s = 3 ⇒ s = 2", "Boat = 10 km/h"],
  why="2 km/h is the stream; 12 km/h is the downstream speed; 8 km/h is the upstream speed.", secs=65, by=BRUTE)

b_ = F(24, 2)
assert b_ == 12
Q(T, "Speed of stream", I,
  "A boat leaves point A and goes downstream. At the same moment a log is dropped into the river at A and floats "
  "with the current. When the boat reaches point B 2 hours later, the log is 24 km behind it. What is the speed of "
  "the boat in still water?",
  "12 km/h", ["24 km/h", "6 km/h", "Cannot be found without the stream's speed"],
  "The log moves with the water, so the gap between boat and log grows at the boat's still-water speed",
  "Boat speed = b + s and log speed = s, so the gap grows at b km/h. In 2 hours the gap is 2b = 24 km, so b = 12 km/h. "
  "The stream's speed cancels out.",
  ["Boat: b + s; log: s", "Gap grows at b", "2b = 24 ⇒ b = 12 km/h"],
  why="24 km/h ignores the 2 hours; 6 km/h divides by 4; the stream's speed is not needed because it cancels in the "
      "gap.", secs=60)

s_ = F(36, 2) - 15
assert 60 / F(30) == 2 and s_ == 3 and (15 - s_) * 2 == 60 - 36
Q(T, "Upstream and downstream", A,
  "Two boats start at the same time from points A and B, 60 km apart on a river, and move towards each other. A is "
  "upstream of B. Each boat has a speed of 15 km/h in still water. They meet 36 km from A. What is the speed of the "
  "stream?",
  "3 km/h", ["6 km/h", "12 km/h", "18 km/h"],
  "Their closing speed is (15 + s) + (15 − s) = 30 km/h whatever the stream",
  "They meet after 60 ÷ 30 = 2 hours. The boat from A goes downstream: 2(15 + s) = 36 ⇒ s = 3 km/h. Check: the boat "
  "from B covers 2 × 12 = 24 km.",
  ["Closing speed = 30 km/h ⇒ meet after 2 h", "2(15 + s) = 36", "s = 3 km/h"],
  why="6 km/h is the difference between the two boats' ground speeds; 12 km/h and 18 km/h are the ground speeds "
      "of the boats from B and A.", secs=80)

# ================================================================ Problems on Trains (B1 I1 A1)
T = "Problems on Trains"
L_ = F(160 * 10, 18 - 10)
assert L_ == 200 and L_ / 10 * F(18, 5) == 72 and F(160, 8) * F(18, 5) == 72 and F(160, 18) * F(18, 5) == 32
Q(T, "Crossing a pole or platform", B,
  "A train passes a signal pole in 10 seconds and a 160 m long platform in 18 seconds. What is its speed?",
  "72 km/h", ["32 km/h", "20 km/h", "57.6 km/h"],
  "The extra 8 seconds are spent covering the 160 m platform",
  "The platform's 160 m takes 18 − 10 = 8 extra seconds, so the speed is 20 m/s = 20 × 18/5 = 72 km/h (the train is "
  "200 m long).",
  ["160 m in 8 s ⇒ 20 m/s", "20 × 18/5 = 72 km/h"],
  why="32 km/h divides 160 m by the full 18 seconds; 20 km/h forgets to convert from m/s; 57.6 km/h converts 16 m/s.",
  secs=40)

t_ = F(60 * 2, 80 - 60)
assert t_ == 6 and 80 * t_ == 480 and 60 * (t_ + 2) == 480
Q(T, "Trains crossing each other", I,
  "A goods train leaves a station at 6:00 AM at 60 km/h. An express train leaves the same station at 8:00 AM on a "
  "parallel track in the same direction at 80 km/h. How far from the station will the express train draw level with "
  "the goods train?",
  "480 km", ["120 km", "360 km", "240 km"],
  "The goods train's 2-hour head start is closed at the relative speed of 20 km/h",
  "Head start = 60 × 2 = 120 km. Closing speed = 80 − 60 = 20 km/h, so it takes 6 hours. The express covers 80 × 6 = "
  "480 km.",
  ["Head start = 120 km", "Time = 120 ÷ 20 = 6 h", "Distance = 80 × 6 = 480 km"],
  why="120 km is the head start; 360 km is how far the goods train runs in the 6 hours after 8 AM; 240 km uses the sum "
      "of the speeds.", secs=55)

t_ = F(100 + 150 + 250, (72 - 54) * F(5, 18))
assert t_ == 100 and F(400, 5) == 80 and F(500, 35) != 100
Q(T, "Trains crossing each other", A,
  "On parallel tracks, a 150 m train runs at 72 km/h behind a 250 m train running at 54 km/h in the same direction. "
  "At a certain moment the front of the faster train is 100 m behind the rear of the slower one. How long after that "
  "moment will the faster train have completely passed the slower one?",
  "100 seconds", ["80 seconds", "20 seconds", "14.3 seconds"],
  "To pass completely, the faster train must gain the gap plus both lengths",
  "Gain needed = 100 + 150 + 250 = 500 m. Relative speed = 72 − 54 = 18 km/h = 5 m/s. Time = 500 ÷ 5 = 100 seconds.",
  ["Distance to gain = 500 m", "Relative speed = 5 m/s", "Time = 100 s"],
  why="80 seconds ignores the 100 m gap; 20 seconds covers only the gap; 14.3 seconds uses the sum of the speeds "
      "(35 m/s), as if the trains were moving towards each other.", secs=80)

# ================================================================ Mensuration (B2 I2 A1)
T = "Mensuration"
side = 36 // 3
assert side == 12 and side ** 2 / 4 == 36 and side ** 2 / 2 == 72
Q(T, "2D areas and perimeters", B,
  "The perimeter of an equilateral triangle is 36 cm. What is its area?",
  "36√3 cm²", ["72√3 cm²", "144 cm²", "18√3 cm²"],
  "Area of an equilateral triangle = (√3/4) × side²",
  "Side = 36 ÷ 3 = 12 cm. Area = (√3/4) × 144 = 36√3 cm² (about 62.35 cm²).",
  ["Side = 12 cm", "Area = √3/4 × 12²", "= 36√3 cm²"],
  why="72√3 cm² uses √3/2 instead of √3/4; 144 cm² is the area of a square of side 12; 18√3 cm² takes half the "
      "correct value.", secs=40)

vol = F(25, 10) * F(16, 10) * F(12, 10)
assert vol == F(24, 5) and vol * 1000 == 4800
Q(T, "3D volume and surface area", B,
  "A rectangular water tank measures 2.5 m × 1.6 m × 1.2 m on the inside. How many litres of water can it hold? "
  "(1 m³ = 1,000 litres)",
  "4,800 litres", ["480 litres", "48,000 litres", "5.3 litres"],
  "Volume = length × breadth × height; then convert m³ to litres",
  "Volume = 2.5 × 1.6 × 1.2 = 4.8 m³ = 4.8 × 1,000 = 4,800 litres.",
  ["2.5 × 1.6 = 4", "4 × 1.2 = 4.8 m³", "4.8 × 1,000 = 4,800 L"],
  why="480 and 48,000 litres slip a zero in the conversion; 5.3 adds the three dimensions.", secs=35)

h_ = F(18, 3)
assert h_ == 6
Q(T, "Cylinder, cone and sphere", I,
  "A cone and a cylinder have the same base radius and the same volume. The cone is 18 cm high. How high is the "
  "cylinder?",
  "6 cm", ["54 cm", "9 cm", "18 cm"],
  "Cone volume = ⅓πr²h; cylinder volume = πr²H",
  "⅓πr² × 18 = πr²H ⇒ H = 18 ÷ 3 = 6 cm.",
  ["⅓πr²(18) = πr²H", "H = 6 cm"],
  why="54 cm multiplies by 3 instead of dividing; 9 cm halves the height; 18 cm forgets the ⅓ in the cone formula.",
  secs=40)

side = math.isqrt(484)
r_ = F(4 * side * 7, 2 * 22)
area = F(22, 7) * r_ * r_
assert side == 22 and r_ == 14 and area == 616 and area - 484 == 132
Q(T, "2D areas and perimeters", I,
  "A wire bent into a square encloses an area of 484 cm². The same wire is bent into a circle. What area does the "
  "circle enclose? (Use π = 22/7.)",
  "616 cm²", ["484 cm²", "1,232 cm²", "154 cm²"],
  "The length of the wire (the perimeter) stays the same",
  "Side = √484 = 22 cm, so the wire is 88 cm long. 2πr = 88 ⇒ r = 14 cm. Area = 22/7 × 14² = 616 cm².",
  ["Side = 22 cm ⇒ wire = 88 cm", "2 × 22/7 × r = 88 ⇒ r = 14", "Area = 616 cm²"],
  why="484 cm² assumes the area is unchanged; 1,232 cm² doubles the correct area; 154 cm² takes the radius as 7 cm "
      "(half of 14).", secs=60)

l_ = math.isqrt(21 * 21 + 20 * 20)
csa = F(22, 7) * 21 * l_
assert F(22, 7) * 21 * 21 / F(22, 10) == 630 and l_ == 29 and csa == 1914 and csa / F(22, 10) == 870 and F(22, 7) * 21 * 20 / F(22, 10) == 600
Q(T, "Cylinder, cone and sphere", A,
  "A conical tent has a base radius of 21 m and a height of 20 m. It is made of canvas 2.2 m wide. What length of "
  "canvas is needed, ignoring wastage? (Use π = 22/7.)",
  "870 m", ["600 m", "1,914 m", "630 m"],
  "Canvas area = curved surface area = πrl, where l = √(r² + h²)",
  "Slant height l = √(21² + 20²) = √841 = 29 m. Curved surface = 22/7 × 21 × 29 = 1,914 m². Length = 1,914 ÷ 2.2 = "
  "870 m.",
  ["l = √(441 + 400) = 29 m", "πrl = 66 × 29 = 1,914 m²", "Length = 1,914 ÷ 2.2 = 870 m"],
  why="600 m uses the height (20 m) in place of the slant height; 1,914 m is the area, not the length; 630 m divides "
      "the base area (1,386 m²) by 2.2 instead of the curved surface.", secs=90)

# ================================================================ Probability (B1 I2 A2)
T = "Probability"
D2 = list(itertools.product(range(1, 7), repeat=2))
p_ = F(sum(1 for a, b in D2 if (a + b) % 4 == 0), 36)
assert p_ == F(1, 4) and F(sum(1 for a, b in D2 if (a + b) % 3 == 0), 36) == F(1, 3)
Q(T, "Coins and dice", B,
  "Two fair dice are rolled. What is the probability that the sum of the numbers is a multiple of 4?",
  "1/4", ["1/3", "1/6", "5/36"],
  "List the sums 4, 8 and 12 and count the outcomes",
  "Sum 4: 3 outcomes; sum 8: 5 outcomes; sum 12: 1 outcome. Total 9 of 36, so the probability is 9/36 = 1/4.",
  ["Sum 4: (1,3), (2,2), (3,1)", "Sum 8: 5 outcomes; sum 12: 1", "9/36 = 1/4"],
  why="1/3 is the probability of a multiple of 3; 1/6 counts sums 4 and 8 but forgets one outcome each; 5/36 counts "
      "only the sum 8.", secs=45, by=BRUTE)

cards = range(1, 51)
fav = [n for n in cards if math.isqrt(n) ** 2 == n or n % 7 == 0]
assert len(fav) == 13 and F(len(fav), 50) == F(13, 50) and F(14, 50) == F(7, 25)
Q(T, "Cards", I,
  "Fifty cards are numbered 1 to 50. One card is drawn at random. What is the probability that its number is a "
  "perfect square or a multiple of 7?",
  "13/50", ["7/25", "7/50", "6/25"],
  "P(A or B) = P(A) + P(B) − P(A and B); 49 is both a square and a multiple of 7",
  "Squares: 1, 4, 9, 16, 25, 36, 49 (7 numbers). Multiples of 7: 7, 14, …, 49 (7 numbers). 49 is counted twice, so "
  "there are 7 + 7 − 1 = 13 favourable cards: 13/50.",
  ["Squares up to 50: 7", "Multiples of 7 up to 50: 7", "Both: 49", "13/50"],
  why="7/25 (14/50) counts 49 twice; 7/50 counts only one of the two kinds; 6/25 (12/50) subtracts the "
      "common number 49 twice.", secs=55, by=BRUTE)

bag = ["R"] * 4 + ["B"] * 3 + ["G"] * 2
draws = list(itertools.combinations(range(9), 3))
p_ = F(sum(1 for c in draws if len({bag[i] for i in c}) == 3), len(draws))
assert len(draws) == 84 and p_ == F(2, 7) and F(24, 504) == F(1, 21)
Q(T, "Balls from bags", I,
  "A bag contains 4 red, 3 blue and 2 green balls. Three balls are drawn at random together. What is the probability "
  "that they are all of different colours?",
  "2/7", ["1/21", "24/729", "1/3"],
  "Favourable = 4 × 3 × 2 choices (one of each colour); total = C(9, 3)",
  "Ways to pick one of each colour = 4 × 3 × 2 = 24. Ways to pick any 3 balls = C(9, 3) = 84. Probability = 24/84 = "
  "2/7.",
  ["Favourable = 4 × 3 × 2 = 24", "Total = C(9, 3) = 84", "24/84 = 2/7"],
  why="1/21 divides 24 by the ordered count 9 × 8 × 7 = 504; 24/729 treats the draws as with replacement and "
      "unordered; 1/3 assumes each colour is equally likely.", secs=60, by=BRUTE)

suits = [s for s in range(4) for _ in range(13)]
p_ = F(4 * math.comb(13, 4), math.comb(52, 4))
assert p_ == F(44, 4165) and F(math.comb(13, 4), math.comb(52, 4)) == F(11, 4165)
assert p_ == F(1, 1) * 1 * F(12, 51) * F(11, 50) * F(10, 49)
Q(T, "Cards", A,
  "Four cards are drawn together at random from a well-shuffled pack of 52 cards. What is the probability that all "
  "four belong to the same suit?",
  "44/4165", ["11/4165", "1/256", "1/64"],
  "Choose the suit (4 ways), then 4 of its 13 cards; divide by C(52, 4)",
  "Favourable = 4 × C(13, 4) = 4 × 715 = 2,860. Total = C(52, 4) = 2,70,725. Probability = 2,860/2,70,725 = 44/4165. "
  "(Or: 12/51 × 11/50 × 10/49 = 1,320/1,24,950 = 44/4165.)",
  ["C(13, 4) = 715", "× 4 suits = 2,860", "C(52, 4) = 2,70,725", "2,860/2,70,725 = 44/4165"],
  short="The first card fixes the suit: 12/51 × 11/50 × 10/49.",
  why="11/4165 is for one named suit (forgets the 4 choices); 1/256 is (1/4)⁴, treating the draws as independent "
      "for one named suit; 1/64 is (1/4)³, ignoring that the deck shrinks.", secs=95)

D3 = list(itertools.product(range(1, 7), repeat=3))
p_ = F(sum(1 for a, b, c in D3 if a < b < c), 216)
assert p_ == F(5, 54) and F(sum(1 for a, b, c in D3 if a <= b <= c), 216) == F(7, 27) and F(1, 6) != p_
Q(T, "Coins and dice", A,
  "A fair die is rolled three times. What is the probability that the three numbers come up in strictly increasing "
  "order (for example 2, 3, 6)?",
  "5/54", ["7/27", "1/6", "5/9"],
  "Any 3 different numbers can appear in exactly one increasing order",
  "Choose 3 different numbers from 6: C(6, 3) = 20 ways; each gives exactly one increasing sequence. Total outcomes = "
  "6³ = 216. Probability = 20/216 = 5/54.",
  ["Favourable = C(6, 3) = 20", "Total = 216", "20/216 = 5/54"],
  why="7/27 (56/216) also counts non-decreasing sequences with repeats; 1/6 is 1/3! as if all numbers were always "
      "different; 5/9 (120/216) counts all sequences of three different numbers.", secs=85, by=BRUTE)

# ================================================================ Permutation and Combination (B2 I2 A1)
T = "Permutation and Combination"
assert math.comb(12, 2) == 66 and 12 * 11 == 132 and 12 * 12 == 144
Q(T, "Selections", B,
  "At a meeting, each of 12 people shakes hands once with every other person. How many handshakes take place?",
  "66", ["132", "144", "78"],
  "Each handshake is a selection of 2 people from 12",
  "Number of handshakes = C(12, 2) = 12 × 11 ÷ 2 = 66.",
  ["C(12, 2)", "= 12 × 11 / 2 = 66"],
  why="132 counts each handshake twice (ordered pairs); 144 is 12²; 78 is C(13, 2).", secs=30, by=BRUTE)

cnt = sum(1 for p in itertools.permutations(range(6)) if p[0] == 0 or p[-1] == 0)
assert cnt == 240 == 2 * math.factorial(5) and math.factorial(5) == 120 and math.factorial(6) == 720
Q(T, "Arrangements", B,
  "In how many ways can 6 different books be arranged on a shelf so that one particular book is always at one of "
  "the two ends?",
  "240", ["120", "720", "480"],
  "Place the particular book first (2 choices), then arrange the other 5",
  "The particular book can go at the left end or the right end: 2 ways. The other 5 books fill the remaining places "
  "in 5! = 120 ways. Total = 2 × 120 = 240.",
  ["Ends: 2 choices", "Others: 5! = 120", "2 × 120 = 240"],
  why="120 fixes the book at one end only; 720 ignores the condition; 480 counts 4 × 5!.", secs=40, by=BRUTE)

cnt = sum(1 for a in range(0, 7) for b in range(0, 5) if a + b == 5 and a >= 2 and b >= 2
          for _ in range(math.comb(6, a) * math.comb(4, b)))
assert cnt == 180 and math.comb(10, 5) == 252 and math.comb(6, 2) * math.comb(4, 2) * 6 == 540
Q(T, "Selections", I,
  "An examination paper has 6 questions in Part A and 4 in Part B. A candidate must answer 5 questions, with at least "
  "2 from each part. In how many ways can the candidate choose the questions?",
  "180", ["252", "120", "60"],
  "The split must be 2 + 3 or 3 + 2; add the two cases",
  "A2 + B3: C(6, 2) × C(4, 3) = 15 × 4 = 60. A3 + B2: C(6, 3) × C(4, 2) = 20 × 6 = 120. Total = 180.",
  ["2 from A, 3 from B: 15 × 4 = 60", "3 from A, 2 from B: 20 × 6 = 120", "Total = 180"],
  why="252 = C(10, 5) ignores the condition; 120 and 60 are the two cases taken separately.", secs=60, by=BRUTE)

cnt = sum(1 for p in itertools.permutations(range(1, 10), 3) if p[2] == 5)
assert cnt == 56 and 9 * 8 * 7 // 9 == 56 and 8 * 8 == 64 and 2 * 56 == 112
Q(T, "Arrangements", I,
  "How many three-digit numbers with all digits different can be formed from the digits 1 to 9 so that the number is "
  "divisible by 5?",
  "56", ["64", "112", "72"],
  "Without 0, a multiple of 5 must end in 5",
  "The units digit must be 5 (no 0 is available). The hundreds and tens digits are chosen in order from the other 8 "
  "digits: 8 × 7 = 56.",
  ["Units digit = 5", "Hundreds: 8 choices, tens: 7 choices", "8 × 7 = 56"],
  why="64 allows the two leading digits to repeat (8 × 8); 112 also counts 0 as a units digit; 72 is 9 × 8, letting 5 "
      "appear twice.", secs=50, by=BRUTE)

cnt = sum(1 for a in range(1, 9) for b in range(1, 9) for c in range(1, 9) if a + b + c == 8)
assert cnt == 21 == math.comb(7, 2) and math.comb(10, 2) == 45 and 3 ** 8 != 21
Q(T, "Selections", A,
  "In how many ways can 8 identical sweets be shared among 3 children so that every child gets at least one sweet?",
  "21", ["45", "56", "28"],
  "Give each child one sweet first, then share the remaining 5 freely; or place 2 dividers in the 7 gaps between 8 "
  "sweets",
  "Line up the 8 sweets: there are 7 gaps between them. Choosing 2 gaps for dividers splits the sweets into 3 "
  "non-empty groups, so the number of ways = C(7, 2) = 21.",
  ["7 gaps between 8 sweets", "Choose 2 gaps: C(7, 2) = 21"],
  why="45 = C(10, 2) allows a child to get nothing; 56 = C(8, 3) chooses 3 dividers; 28 = C(8, 2) uses 8 gaps.",
  secs=80, by=BRUTE)

# ================================================================ Tabular DI (B4 I3 A1): two sets of 4
T = "Tabular DI"
KCC = {"Rampur": (480, 75, 120), "Sitapur": (600, 65, 110), "Nandgaon": (350, 84, 140), "Bhimpur": (520, 70, 125),
       "Karanpur": (450, 76, 105)}
sid = stimulus("data_table", "Kisan Credit Card applications at five rural branches, 2025-26",
               "The table shows, for five rural branches of a bank in 2025-26, the number of Kisan Credit Card (KCC) "
               "applications received, the percentage of them that were sanctioned, and the average loan per "
               "sanctioned application (₹ thousand).\n\n" +
               md_table(["Branch", "Applications received", "Sanctioned (% of applications)",
                         "Average loan per sanction (₹ thousand)"], [[k, a, p, l] for k, (a, p, l) in KCC.items()]),
               {"columns": ["branch", "applications", "sanctioned_pct", "avg_loan_rs_thousand"],
                "rows": [[k, *v] for k, v in KCC.items()]})
san = {k: a * F(p, 100) for k, (a, p, l) in KCC.items()}
amt = {k: san[k] * KCC[k][2] for k in KCC}
assert san == {"Rampur": 360, "Sitapur": 390, "Nandgaon": 294, "Bhimpur": 364, "Karanpur": 342}
assert len(set(san.values())) == 5 and len(set(amt.values())) == 5
assert san["Nandgaon"] == 294 and 350 - 294 == 56 and 350 * F(76, 100) == 266
Q(T, "Table with percentages", B, "How many KCC applications did the Nandgaon branch sanction?",
  "294", ["56", "266", "140"],
  "Sanctioned = applications × sanction percentage",
  "Nandgaon: 84% of 350 = 294.",
  ["84% of 350 = 0.84 × 350 = 294"],
  why="56 is the number not sanctioned; 266 uses Karanpur's 76%; 140 is Nandgaon's average loan in ₹ thousand.",
  secs=30, stim=sid)

tot_app = sum(a for a, p, l in KCC.values())
assert tot_app == 2400 and sum(san.values()) == 1750 and tot_app - 350 == 2050
Q(T, "Single table", B, "How many KCC applications did the five branches receive in all?",
  "2,400", ["1,750", "2,050", "2,500"],
  "Add the 'applications received' column",
  "480 + 600 + 350 + 520 + 450 = 2,400.",
  ["480 + 600 = 1,080", "+ 350 + 520 + 450 = 2,400"],
  why="1,750 is the number sanctioned; 2,050 leaves out Nandgaon; 2,500 is an addition slip of 100.", secs=30,
  stim=sid)

srt = sorted(amt, key=amt.get, reverse=True)
assert srt[0] == "Bhimpur" and amt["Bhimpur"] == 45500 and amt["Rampur"] == 43200 and amt["Sitapur"] == 42900
assert max(san, key=san.get) == "Sitapur" and max(KCC, key=lambda k: KCC[k][2]) == "Nandgaon"
Q(T, "Table with percentages", I,
  "Which branch sanctioned the largest total amount of KCC loans in 2025-26?",
  "Bhimpur", ["Sitapur", "Nandgaon", "Rampur"],
  "Total amount = number sanctioned × average loan",
  "Totals (₹ thousand): Rampur 360 × 120 = 43,200; Sitapur 390 × 110 = 42,900; Nandgaon 294 × 140 = 41,160; Bhimpur "
  "364 × 125 = 45,500; Karanpur 342 × 105 = 35,910. Bhimpur is the largest (₹4.55 crore).",
  ["Rampur 43,200", "Sitapur 42,900", "Nandgaon 41,160", "Bhimpur 45,500", "Karanpur 35,910"],
  why="Sitapur sanctioned the most applications but has a smaller average loan; Nandgaon has the largest average loan "
      "but the fewest sanctions; Rampur is second at ₹43,200 thousand.", secs=75, stim=sid)

ov = F(sum(san.values()), tot_app)
assert pct2(ov) == "72.92%" and F(75 + 65 + 84 + 70 + 76, 5) == 74 and pct2(F(1750, 2500)) == "70.00%"
Q(T, "Table with percentages", A,
  "Taking the five branches together, what percentage of the KCC applications received were sanctioned (correct to "
  "two decimal places)?",
  "72.92%", ["74.00%", "70.00%", "27.08%"],
  "Overall rate = total sanctioned ÷ total received; do not average the five percentages",
  "Sanctioned: 360 + 390 + 294 + 364 + 342 = 1,750 out of 2,400 received. 1,750 ÷ 2,400 = 72.92%.",
  ["Total sanctioned = 1,750", "Total received = 2,400", "1,750 ÷ 2,400 = 72.92%"],
  why="74.00% is the simple average of the five percentages, which ignores the different numbers of applications; "
      "70.00% divides by 2,500; 27.08% is the share not sanctioned.", secs=80, stim=sid)

VAN = {"Van P": (1260, 18), "Van Q": (1125, 15), "Van R": (1600, 20), "Van S": (1020, 12), "Van T": (1155, 21)}
sid = stimulus("data_table", "Distance and mileage of five delivery vans in one week",
               "The table shows the distance driven by each of five delivery vans of a courier company in one week "
               "of October 2026 and the van's mileage (kilometres per litre of diesel). Diesel cost ₹102 per litre "
               "that week.\n\n" +
               md_table(["Van", "Distance driven (km)", "Mileage (km per litre)"],
                        [[k, ind(d), m] for k, (d, m) in VAN.items()]),
               {"columns": ["van", "distance_km", "km_per_litre"], "rows": [[k, *v] for k, v in VAN.items()]})
lit = {k: F(d, m) for k, (d, m) in VAN.items()}
assert lit == {"Van P": 70, "Van Q": 75, "Van R": 80, "Van S": 85, "Van T": 55} and len(set(lit.values())) == 5
assert F(1600, 18) != 80 and 1600 * 20 == 32000
Q(T, "Single table", B, "How many litres of diesel did Van R use in the week?",
  "80 litres", ["85 litres", "32,000 litres", "75 litres"],
  "Litres used = distance ÷ mileage",
  "Van R: 1,600 km ÷ 20 km per litre = 80 litres.",
  ["1,600 ÷ 20 = 80"],
  why="85 litres is Van S; 32,000 multiplies distance by mileage; 75 litres is Van Q.", secs=30, stim=sid)

tkm = sum(d for d, m in VAN.values())
assert tkm == 6160 and tkm - 1600 == 4560 and tkm - 1020 == 5140
Q(T, "Single table", B, "What total distance did the five vans drive in the week?",
  "6,160 km", ["5,140 km", "6,060 km", "4,560 km"],
  "Add the distance column",
  "1,260 + 1,125 + 1,600 + 1,020 + 1,155 = 6,160 km.",
  ["1,260 + 1,125 = 2,385", "+ 1,600 = 3,985", "+ 1,020 + 1,155 = 6,160"],
  why="5,140 km leaves out Van S; 6,060 km is an addition slip of 100; 4,560 km leaves out Van R.", secs=35, stim=sid)

tl = sum(lit.values())
fm = F(tkm, tl)
assert tl == 365 and r2(fm) == F(1688, 100) and F(18 + 15 + 20 + 12 + 21, 5) == F(86, 5) and r2(F(6160, 385)) == 16
Q(T, "Single table", I,
  "What was the fleet's overall mileage for the week, i.e. total distance ÷ total diesel used (correct to two decimal "
  "places)?",
  "16.88 km per litre", ["17.20 km per litre", "16.00 km per litre", "16.50 km per litre"],
  "Overall mileage is not the simple average of the five mileages",
  "Diesel used: 70 + 75 + 80 + 85 + 55 = 365 litres. Overall mileage = 6,160 ÷ 365 = 16.88 km per litre.",
  ["Litres: P 70, Q 75, R 80, S 85, T 55", "Total = 365 L", "6,160 ÷ 365 = 16.88"],
  why="17.20 is the simple average of the five mileages; 16.00 divides by 385 litres (an addition slip); 16.50 averages "
      "only the lowest and highest mileages (12 and 21).", secs=70, stim=sid)

saved = lit["Van S"] - F(1020, 17)
assert saved == 25 and F(1020, 17) == 60 and saved * 102 == 2550
Q(T, "Single table", I,
  "If Van S had been replaced by a van giving 17 km per litre, covering the same distance, how many litres of diesel "
  "would have been saved in the week?",
  "25 litres", ["60 litres", "5 litres", "2,550 litres"],
  "Litres = distance ÷ mileage, before and after",
  "Van S used 1,020 ÷ 12 = 85 litres. At 17 km per litre it would use 1,020 ÷ 17 = 60 litres. Saving = 25 litres.",
  ["Now: 1,020 ÷ 12 = 85 L", "New: 1,020 ÷ 17 = 60 L", "Saving = 25 L"],
  why="60 litres is the new consumption, not the saving; 5 litres is the gain in mileage (17 − 12); 2,550 is the "
      "saving in rupees (25 × 102), not litres.", secs=55, stim=sid)

# ================================================================ Bar Graph DI (B3 I2 A4): sets of 5 and 4
T = "Bar Graph DI"
CB = {"Oct 2025": 42, "Nov 2025": 68, "Dec 2025": 85, "Jan 2026": 72, "Feb 2026": 54, "Mar 2026": 39}
sid = stimulus("chart", "Cotton bales arriving at a ginning mill, October 2025 to March 2026",
               "The bar chart shows the number of cotton bales (in thousands) that arrived at a ginning mill in each "
               "month from October 2025 to March 2026 (values read from the bars).\n\n" +
               md_table(["Month", "Bales arrived (thousand)"], [[k, v] for k, v in CB.items()]),
               {"chart_type": "bar", "x": list(CB), "series": [{"name": "Bales arrived (thousand)",
                                                                "values": list(CB.values())}]})
assert len(set(CB.values())) == 6
v = CB["Dec 2025"] + CB["Jan 2026"] + CB["Feb 2026"]
assert v == 211 and CB["Nov 2025"] + CB["Dec 2025"] + CB["Jan 2026"] == 225 and v - 54 + 39 == 196
Q(T, "Simple bar", B, "How many bales arrived in December 2025, January 2026 and February 2026 together?",
  "2,11,000", ["2,25,000", "1,96,000", "1,65,000"],
  "Add the three bars (each in thousands)",
  "85 + 72 + 54 = 211 thousand = 2,11,000 bales.",
  ["85 + 72 + 54 = 211 thousand"],
  why="2,25,000 adds November to January; 1,96,000 uses March in place of February; 1,65,000 is the total for "
      "January to March.", secs=30, stim=sid)

g = F(68 - 42, 42) * 100
assert pct2(F(26, 42)) == "61.90%" and pct2(F(26, 68)) == "38.24%" and pct2(F(68, 42)) == "161.90%"
Q(T, "Simple bar", B,
  "By what percentage were the arrivals in November 2025 more than those in October 2025 (correct to two decimal "
  "places)?",
  "61.90%", ["38.24%", "161.90%", "26.00%"],
  "Percentage increase = increase ÷ earlier value × 100",
  "Increase = 68 − 42 = 26 thousand. 26 ÷ 42 × 100 = 61.90%.",
  ["68 − 42 = 26", "26 ÷ 42 = 0.6190", "61.90%"],
  why="38.24% divides by November's 68; 161.90% is November as a percentage of October; 26.00% is the increase in "
      "thousands, not a percentage.", secs=40, stim=sid)

tot = sum(CB.values())
assert tot == 360 and F(tot, 6) == 60 and F(tot, 5) == 72
Q(T, "Simple bar", B, "What was the average number of bales arriving per month over the six months?",
  "60,000", ["72,000", "54,000", "63,500"],
  "Average = total of the six bars ÷ 6",
  "Total = 42 + 68 + 85 + 72 + 54 + 39 = 360 thousand. Average = 360 ÷ 6 = 60 thousand.",
  ["Total = 360 thousand", "360 ÷ 6 = 60 thousand"],
  why="72,000 divides by 5; 54,000 is February's figure; 63,500 is the average of the highest and lowest bars "
      "((85 + 42) ÷ 2).", secs=40, stim=sid)

q1, q2 = CB["Oct 2025"] + CB["Nov 2025"] + CB["Dec 2025"], CB["Jan 2026"] + CB["Feb 2026"] + CB["Mar 2026"]
ch = (F(q2) * F(112, 100) / q1 - 1) * 100
assert (q1, q2) == (195, 165) and r2(-ch) == F(523, 100) and pct2(F(30, 195)) == "15.38%"
assert r2((F(195) * F(112, 100) / 165 - 1) * 100) == F(3236, 100)
Q(T, "Simple bar", A,
  "The mill paid the same price per bale from October to December 2025, and a price 12% higher from January to March "
  "2026. By what percentage did its spending on bales in January–March differ from that in October–December (correct "
  "to two decimal places)?",
  "5.23% less", ["15.38% less", "3.38% less", "32.36% more"],
  "Spending ∝ bales × price; compare 165 × 1.12 with 195 × 1",
  "Oct–Dec: 42 + 68 + 85 = 195 thousand bales. Jan–Mar: 72 + 54 + 39 = 165 thousand. Spending ratio = 165 × 1.12 ÷ "
  "195 = 184.8 ÷ 195 = 0.9477, i.e. 5.23% less.",
  ["Oct–Dec = 195, Jan–Mar = 165", "165 × 1.12 = 184.8", "184.8 ÷ 195 = 0.9477 ⇒ 5.23% less"],
  why="15.38% less ignores the price rise; 3.38% less subtracts 12 from 15.38 instead of multiplying; 32.36% more "
      "compares 195 × 1.12 with 165, reversing the periods.", secs=95, stim=sid)

ys_ = list(CB)
fall = {ys_[i]: F(CB[ys_[i - 1]] - CB[ys_[i]], CB[ys_[i - 1]]) for i in range(1, 6) if CB[ys_[i]] < CB[ys_[i - 1]]}
assert fall == {"Jan 2026": F(13, 85), "Feb 2026": F(1, 4), "Mar 2026": F(15, 54)}
assert max(fall, key=fall.get) == "Mar 2026" and max(CB[ys_[i - 1]] - CB[ys_[i]] for i in range(1, 6)) == 18
Q(T, "Simple bar", A,
  "In which month was the percentage fall in arrivals, compared with the previous month, the largest?",
  "March 2026", ["February 2026", "January 2026", "October 2025"],
  "Compare each fall as a percentage of the previous month, not in thousands",
  "January: 13 on 85 = 15.29%. February: 18 on 72 = 25%. March: 15 on 54 = 27.78%. March has the largest percentage "
  "fall, although February has the largest fall in thousands.",
  ["Jan: −13/85 = −15.29%", "Feb: −18/72 = −25%", "Mar: −15/54 = −27.78%"],
  why="February has the largest fall in thousands (18) but a smaller percentage; January's fall is only 15.29%; "
      "October has no previous month in the chart.", secs=80, stim=sid)

FL = {"Indore": (240, 360), "Bhopal": (310, 305), "Ujjain": (180, 270), "Gwalior": (275, 225)}
sid = stimulus("chart", "Rice and atta packets dispatched by a flour mill to four cities, September 2026",
               "The grouped bar chart shows the number of rice packets and atta (wheat flour) packets, in thousands, "
               "that a mill dispatched to four cities in September 2026 (values read from the bars).\n\n" +
               md_table(["City", "Rice packets (thousand)", "Atta packets (thousand)"],
                        [[k, r, a] for k, (r, a) in FL.items()]),
               {"chart_type": "grouped_bar", "x": list(FL),
                "series": [{"name": "Rice packets (thousand)", "values": [r for r, a in FL.values()]},
                           {"name": "Atta packets (thousand)", "values": [a for r, a in FL.values()]}]})
assert len({r + a for r, a in FL.values()}) == 4
num, den = FL["Indore"][0] + FL["Ujjain"][0], FL["Bhopal"][1] + FL["Gwalior"][1]
assert (num, den) == (420, 530) and F(num, den) == F(42, 53) and F(240 + 270, 310 + 225) == F(102, 107)
Q(T, "Stacked or grouped bar", I,
  "What is the ratio of the rice packets sent to Indore and Ujjain together to the atta packets sent to Bhopal and "
  "Gwalior together?",
  "42 : 53", ["53 : 42", "102 : 107", "28 : 39"],
  "Pick the right bar for each city before adding",
  "Rice to Indore and Ujjain = 240 + 180 = 420 thousand. Atta to Bhopal and Gwalior = 305 + 225 = 530 thousand. "
  "Ratio = 420 : 530 = 42 : 53.",
  ["420 : 530", "÷ 10 ⇒ 42 : 53"],
  why="53 : 42 reverses the ratio; 102 : 107 uses Ujjain's atta bar instead of its rice bar; 28 : 39 uses the rice bars "
      "of Bhopal and Gwalior (420 : 585) instead of their atta bars.", secs=50, stim=sid)

share = {k: F(r, r + a) for k, (r, a) in FL.items()}
assert max(share, key=share.get) == "Gwalior" and share["Gwalior"] == F(11, 20) and share["Bhopal"] == F(62, 123)
assert max(FL, key=lambda k: FL[k][0]) == "Bhopal"
Q(T, "Stacked or grouped bar", I,
  "For which city did rice packets make up the largest share of all the packets sent to it?",
  "Gwalior", ["Bhopal", "Indore", "Ujjain"],
  "Share = rice ÷ (rice + atta) for each city",
  "Indore 240/600 = 40%; Bhopal 310/615 = 50.4%; Ujjain 180/450 = 40%; Gwalior 275/500 = 55%. Gwalior has the "
  "largest share.",
  ["Indore 40%", "Bhopal 50.4%", "Ujjain 40%", "Gwalior 55%"],
  why="Bhopal received the most rice packets (310 thousand) but also many atta packets; Indore and Ujjain are at 40% "
      "each.", secs=60, stim=sid)

wt = FL["Bhopal"][0] * 5 + FL["Bhopal"][1] * 10
assert wt == 4600 and (310 + 305) * 5 == 3075 and 310 * 10 + 305 * 5 == 4625
Q(T, "Stacked or grouped bar", A,
  "Each rice packet weighs 5 kg and each atta packet 10 kg. What total weight of packets did the mill send to Bhopal "
  "in September 2026?",
  "4,600 tonnes", ["3,075 tonnes", "4,625 tonnes", "6,150 tonnes"],
  "Weight = packets × weight per packet; 1,000 kg = 1 tonne, so thousand packets × kg = tonnes",
  "Rice: 310 thousand × 5 kg = 1,550 tonnes. Atta: 305 thousand × 10 kg = 3,050 tonnes. Total = 4,600 tonnes.",
  ["Rice 310 × 5 = 1,550 t", "Atta 305 × 10 = 3,050 t", "Total 4,600 t"],
  why="3,075 tonnes weighs every packet at 5 kg; 4,625 tonnes swaps the two packet weights; 6,150 tonnes weighs every "
      "packet at 10 kg.", secs=70, stim=sid)

rice, atta = sum(r for r, a in FL.values()), sum(a for r, a in FL.values())
new = rice * F(120, 100) + atta * F(90, 100)
assert (rice, atta) == (1005, 1160) and new == 2250 and r2((new / (rice + atta) - 1) * 100) == F(393, 100)
assert (F(120 + 90, 2) - 100) == 5 and F(420, 585) == F(28, 39)
Q(T, "Stacked or grouped bar", A,
  "Next month the mill raises rice dispatches to every city by 20% and cuts atta dispatches to every city by 10%. By "
  "what percentage does the total number of packets change (correct to two decimal places)?",
  "3.93% increase", ["5.00% increase", "10.00% increase", "3.93% decrease"],
  "Apply each change to its own total; the overall change is a weighted average",
  "Rice total = 240 + 310 + 180 + 275 = 1,005 thousand; atta total = 360 + 305 + 270 + 225 = 1,160 thousand; together "
  "2,165. New total = 1,206 + 1,044 = 2,250. Change = 85 ÷ 2,165 = 3.93% increase.",
  ["Rice 1,005 → 1,206", "Atta 1,160 → 1,044", "Total 2,165 → 2,250", "+85 ÷ 2,165 = +3.93%"],
  why="5.00% averages +20% and −10% as if the two totals were equal; 10.00% simply adds the two rates; '3.93% "
      "decrease' gets the direction wrong.", secs=95, stim=sid)

# ================================================================ Pie Chart DI (B1 I2 A3): two sets of 3
T = "Pie Chart DI"
BM = {"Customer meetings": 96, "Loan appraisal": 84, "Recovery visits": 60, "Staff review": 48, "Reports": 42,
      "Training": 30}
assert sum(BM.values()) == 360 and len(set(BM.values())) == 6
sid = stimulus("chart", "A branch manager's 60-hour working week by activity (central angles)",
               "The pie chart shows how a bank branch manager's 60 working hours in one week of October 2026 were "
               "divided among six activities. Each sector's central angle (in degrees) is given.\n\n" +
               md_table(["Activity", "Central angle (degrees)"], [[k, v] for k, v in BM.items()]),
               {"chart_type": "pie", "unit": "degrees", "total_hours": 60, "labels": list(BM),
                "values": list(BM.values())})
hrs = {k: F(v * 60, 360) for k, v in BM.items()}
assert hrs == {"Customer meetings": 16, "Loan appraisal": 14, "Recovery visits": 10, "Staff review": 8, "Reports": 7,
               "Training": 5}
Q(T, "Degree-based", B, "How many hours did the manager spend on loan appraisal that week?",
  "14 hours", ["16 hours", "8.4 hours", "23.3 hours"],
  "Hours = central angle ÷ 360 × 60, i.e. angle ÷ 6",
  "Loan appraisal: 84° ÷ 360° × 60 = 84 ÷ 6 = 14 hours.",
  ["60/360 = 1/6 hour per degree", "84 ÷ 6 = 14 hours"],
  why="16 hours is customer meetings; 8.4 hours divides 84 by 10; 23.3 hours is 84 as a percentage of 360.", secs=30,
  stim=sid)

v = (hrs["Customer meetings"] - hrs["Reports"] - hrs["Training"]) / (hrs["Reports"] + hrs["Training"]) * 100
assert v == F(100, 3) and F(4, 16) * 100 == 25 and F(16, 12) * 100 == F(400, 3)
Q(T, "Degree-based", I,
  "The time spent on customer meetings was what percentage more than the time spent on reports and training "
  "together?",
  "33⅓%", ["25%", "133⅓%", "4%"],
  "Percentage more = difference ÷ the smaller quantity × 100",
  "Customer meetings: 16 hours; reports + training: 7 + 5 = 12 hours. 16 is 4 more than 12, and 4 ÷ 12 = 33⅓%.",
  ["16 hours vs 12 hours", "Difference = 4", "4 ÷ 12 = 33⅓%"],
  why="25% divides the difference by 16; 133⅓% is 16 as a percentage of 12; 4% is the difference in hours.", secs=50,
  stim=sid)

new_rv = hrs["Recovery visits"] + hrs["Staff review"] * F(25, 100) + 2
assert new_rv == 14 and new_rv * 6 == 84 and (hrs["Recovery visits"] + 4) == 14 and (10 + 2 + 8 * F(1, 4)) * 6 == 84
Q(T, "Degree-based", A,
  "The next week the manager again works 60 hours. He cuts his staff-review time by 25% and his report-writing time "
  "by 2 hours, and spends all the time saved on recovery visits; everything else is unchanged. What is the new "
  "central angle for recovery visits?",
  "84°", ["72°", "64°", "96°"],
  "Work in hours, then convert back: angle = hours × 6",
  "Saved: 25% of 8 = 2 hours from staff review and 2 hours from reports, 4 hours in all. Recovery visits rise from 10 "
  "to 14 hours, so the angle = 14 × 6 = 84°.",
  ["Staff review: 25% of 8 = 2 h", "Reports: 2 h", "Recovery: 10 + 4 = 14 h", "14 × 6 = 84°"],
  why="72° adds only the 2 hours from reports; 64° adds the 4 hours to the angle as if they were degrees; 96° counts "
      "the reports saving twice (10 + 2 + 2 + 2 = 16 hours).", secs=80, stim=sid)

RV24 = {"North": 30, "South": 25, "East": 15, "West": 20, "Exports": 10}
RV25 = {"North": 28, "South": 30, "East": 12, "West": 22, "Exports": 8}
assert sum(RV24.values()) == sum(RV25.values()) == 100 and len(set(RV25.values())) == 5
sid = stimulus("chart", "Sales revenue of a pump maker by market, 2024-25 and 2025-26 (two pie charts)",
               "Two pie charts show how a pump manufacturer's sales revenue was divided among five markets: ₹480 crore "
               "in all in 2024-25 and ₹600 crore in all in 2025-26 (percentages of each year's total).\n\n" +
               md_table(["Market", "2024-25 (% of ₹480 crore)", "2025-26 (% of ₹600 crore)"],
                        [[k, RV24[k], RV25[k]] for k in RV24]),
               {"chart_type": "two_pies", "unit": "percent",
                "pies": [{"name": "2024-25", "total_rs_crore": 480, "labels": list(RV24),
                          "values": list(RV24.values())},
                         {"name": "2025-26", "total_rs_crore": 600, "labels": list(RV25),
                          "values": list(RV25.values())}]})
r24 = {k: F(480 * v, 100) for k, v in RV24.items()}
r25 = {k: F(600 * v, 100) for k, v in RV25.items()}
gr = {k: r25[k] / r24[k] - 1 for k in RV24}
assert r24 == {"North": 144, "South": 120, "East": 72, "West": 96, "Exports": 48}
assert r25 == {"North": 168, "South": 180, "East": 72, "West": 132, "Exports": 48}
assert max(gr, key=gr.get) == "South" and gr["South"] == F(1, 2) and gr["West"] == F(3, 8)
assert max(RV25, key=lambda k: RV25[k] - RV24[k]) == "South"
Q(T, "Two pie charts", I, "Which market's revenue grew the most, in percentage terms, from 2024-25 to 2025-26?",
  "South", ["West", "North", "East"],
  "Convert each share into rupees for its own year before comparing",
  "Revenue (₹ crore), 2024-25 → 2025-26: North 144 → 168 (+16.7%); South 120 → 180 (+50%); East 72 → 72 (0%); West "
  "96 → 132 (+37.5%); Exports 48 → 48 (0%). South grew the most.",
  ["North +16.7%", "South +50%", "East 0%", "West +37.5%", "Exports 0%"],
  why="West grew 37.5%, second to South; North's share fell, though its revenue grew 16.7%; East's revenue did not "
      "change.", secs=70, stim=sid)

o24 = sum(v for k, v in r24.items() if k != "South")
o25 = sum(v for k, v in r25.items() if k != "South")
assert (o24, o25) == (360, 420) and (o25 - o24) / o24 == F(1, 6) and F(600 - 480, 480) == F(1, 4)
Q(T, "Two pie charts", A,
  "By what percentage did the combined revenue from all markets other than South increase from 2024-25 to 2025-26?",
  "16⅔%", ["25%", "14.29%", "50%"],
  "Other markets = total − South in each year",
  "2024-25: 480 − 120 = ₹360 crore. 2025-26: 600 − 180 = ₹420 crore. Increase = 60 on 360 = 16⅔%.",
  ["2024-25: 75% of 480 = 360", "2025-26: 70% of 600 = 420", "60 ÷ 360 = 16⅔%"],
  why="25% is the growth of the whole company; 14.29% divides 60 by 420; 50% is South's own growth.", secs=70,
  stim=sid)

dom = 600 - r25["Exports"]
prof = dom * F(12, 100) + r25["Exports"] * F(20, 100)
assert dom == 552 and prof == F(7584, 100) and 600 * F(12, 100) == 72 and 600 * F(16, 100) == 96
Q(T, "Two pie charts", A,
  "In 2025-26 the company earned a profit of 12% on its domestic revenue (all markets except Exports) and 20% on its "
  "export revenue. What was its total profit in 2025-26?",
  "₹75.84 crore", ["₹72.00 crore", "₹96.00 crore", "₹66.24 crore"],
  "Split 2025-26 revenue into domestic (92%) and exports (8%)",
  "Exports = 8% of 600 = ₹48 crore; domestic = ₹552 crore. Profit = 12% of 552 + 20% of 48 = 66.24 + 9.60 = ₹75.84 "
  "crore.",
  ["Exports = 48, domestic = 552", "0.12 × 552 = 66.24", "0.20 × 48 = 9.60", "Total = 75.84"],
  why="₹72.00 crore applies 12% to all ₹600 crore; ₹96.00 crore averages the two rates (16%); ₹66.24 crore leaves out "
      "the export profit.", secs=85, stim=sid)

# ================================================================ Line Graph DI (B3 I3 A1): sets of 4 and 3
T = "Line Graph DI"
DM = {"Jan": 840, "Feb": 760, "Mar": 1140, "Apr": 950, "May": 1330, "Jun": 1064}
sid = stimulus("chart", "New demat accounts opened at a brokerage branch, January to June 2026",
               "The line graph shows the number of new demat accounts opened at one branch of a stock-broking firm in "
               "each month from January to June 2026 (values read from the graph).\n\n" +
               md_table(["Month", "New demat accounts"], [[k, ind(v)] for k, v in DM.items()]),
               {"chart_type": "line", "x": list(DM), "series": [{"name": "New demat accounts",
                                                                 "values": list(DM.values())}]})
assert len(set(DM.values())) == 6
q1 = DM["Jan"] + DM["Feb"] + DM["Mar"]
assert q1 == 2740 and DM["Apr"] + DM["May"] + DM["Jun"] == 3344 and DM["Feb"] + DM["Mar"] + DM["Apr"] == 2850
Q(T, "Single line", B, "How many new demat accounts were opened in January, February and March together?",
  "2,740", ["3,344", "2,850", "1,980"],
  "Add the three monthly points",
  "840 + 760 + 1,140 = 2,740.",
  ["840 + 760 = 1,600", "1,600 + 1,140 = 2,740"],
  why="3,344 is the April–June total; 2,850 adds February to April; 1,980 leaves out February (840 + 1,140).",
  secs=30, stim=sid)

assert F(1140 - 760, 760) == F(1, 2) and F(380, 1140) == F(1, 3)
Q(T, "Single line", B, "By what percentage did the number of new accounts rise from February to March?",
  "50%", ["33⅓%", "150%", "38%"],
  "Percentage rise = rise ÷ February's value × 100",
  "Rise = 1,140 − 760 = 380. 380 ÷ 760 = 50%.",
  ["1,140 − 760 = 380", "380 ÷ 760 = 0.5 = 50%"],
  why="33⅓% divides the rise by March's 1,140; 150% is March as a percentage of February; 38% treats the rise of 380 "
      "as a percentage of 1,000.", secs=35, stim=sid)

ms = list(DM)
chg = {ms[i]: F(DM[ms[i]] - DM[ms[i - 1]], DM[ms[i - 1]]) for i in range(1, 6)}
falls = {k: -c for k, c in chg.items() if c < 0}
assert falls == {"Feb": F(2, 21), "Apr": F(1, 6), "Jun": F(1, 5)} and max(falls, key=falls.get) == "Jun"
assert max(DM[ms[i - 1]] - DM[ms[i]] for i in range(1, 6)) == 266
Q(T, "Single line", I,
  "Compared with the month before, which month saw the steepest percentage drop in new demat accounts?",
  "June", ["April", "February", "May"],
  "Only months with a fall count; compare falls as a percentage of the previous month",
  "February: 80 on 840 = 9.52%. April: 190 on 1,140 = 16.67%. June: 266 on 1,330 = 20%. The largest percentage fall "
  "was in June. (May was a rise.)",
  ["Feb: −80/840 = −9.52%", "Apr: −190/1,140 = −16.67%", "Jun: −266/1,330 = −20%"],
  why="April's fall is 16.67%; February's is 9.52%; May shows a rise of 40%, not a fall.", secs=60, stim=sid)

avg = F(sum(DM.values()), 6)
assert avg == 1014 and sum(DM.values()) == 6084 and F(6084, 5) != 1014 and F(840 + 1330, 2) == 1085
Q(T, "Single line", I, "What was the average number of new accounts opened per month over the six months?",
  "1,014", ["1,085", "1,216.8", "950"],
  "Average = total of the six points ÷ 6",
  "Total = 840 + 760 + 1,140 + 950 + 1,330 + 1,064 = 6,084. Average = 6,084 ÷ 6 = 1,014.",
  ["Total = 6,084", "6,084 ÷ 6 = 1,014"],
  why="1,085 averages only January and May; 1,216.8 divides by 5; 950 is April's value.", secs=50, stim=sid)

MF = {"2021": (120, 96), "2022": (150, 129), "2023": (180, 153), "2024": (210, 189), "2025": (252, 210)}
sid = stimulus("chart", "Loans disbursed and recovered by a microfinance company, 2021 to 2025",
               "The line graph has two lines: the amount of loans a microfinance company disbursed in each year from "
               "2021 to 2025, and the amount of loan repayments it recovered in the same year (both in ₹ crore, "
               "values read from the graph).\n\n" +
               md_table(["Year", "Disbursed (₹ crore)", "Recovered (₹ crore)"], [[k, d, r] for k, (d, r) in MF.items()]),
               {"chart_type": "line", "x": list(MF), "unit": "rs_crore",
                "series": [{"name": "Disbursed", "values": [d for d, r in MF.values()]},
                           {"name": "Recovered", "values": [r for d, r in MF.values()]}]})
rr = {k: F(r, d) for k, (d, r) in MF.items()}
assert len(set(rr.values())) == 5 and max(rr, key=rr.get) == "2024" and rr["2024"] == F(9, 10)
assert max(MF, key=lambda k: MF[k][1]) == "2025" and max(MF, key=lambda k: MF[k][1] - MF[k][0]) == "2022"
Q(T, "Multiple lines", B,
  "In which year was the amount recovered the highest percentage of the amount disbursed in that year?",
  "2024", ["2025", "2022", "2023"],
  "Recovery ratio = recovered ÷ disbursed for each year",
  "2021: 96/120 = 80%; 2022: 129/150 = 86%; 2023: 153/180 = 85%; 2024: 189/210 = 90%; 2025: 210/252 = 83.3%. 2024 "
  "is the highest.",
  ["2021 80%", "2022 86%", "2023 85%", "2024 90%", "2025 83.3%"],
  why="2025 has the largest amount recovered but only 83.3% of disbursement; 2022 (86%) and 2023 (85%) are lower than "
      "2024.", secs=55, stim=sid)

td, tr = sum(d for d, r in MF.values()), sum(r for d, r in MF.values())
assert (td, tr) == (912, 777) and pct2(F(tr, td)) == "85.20%" and F(80 + 86 + 85 + 90, 1) + F(250, 3) == F(1273, 3)
assert r2(F(1273, 15)) == F(8487, 100) and pct2(F(td - tr, td)) == "14.80%"
Q(T, "Multiple lines", I,
  "Over the five years taken together, the total amount recovered was what percentage of the total amount disbursed "
  "(correct to two decimal places)?",
  "85.20%", ["84.87%", "14.80%", "117.37%"],
  "Divide the two five-year totals; do not average the yearly percentages",
  "Disbursed: 120 + 150 + 180 + 210 + 252 = ₹912 crore. Recovered: 96 + 129 + 153 + 189 + 210 = ₹777 crore. "
  "777 ÷ 912 = 85.20%.",
  ["Total disbursed = 912", "Total recovered = 777", "777 ÷ 912 = 85.20%"],
  why="84.87% is the simple average of the five yearly percentages; 14.80% is the unrecovered share; 117.37% divides "
      "disbursed by recovered.", secs=65, stim=sid)

gap21, gap25 = MF["2021"][0] - MF["2021"][1], MF["2025"][0] - MF["2025"][1]
assert (gap21, gap25) == (24, 42) and F(gap25 - gap21, gap21) == F(3, 4) and F(18, 42) == F(3, 7)
assert F(252 - 120, 120) == F(11, 10)
Q(T, "Multiple lines", A,
  "The gap between the amount disbursed and the amount recovered in a year is that year's net new lending. By what "
  "percentage did the net new lending grow from 2021 to 2025?",
  "75%", ["110%", "42.86%", "175%"],
  "Net new lending = disbursed − recovered; compare 2025 with 2021",
  "2021: 120 − 96 = ₹24 crore. 2025: 252 − 210 = ₹42 crore. Growth = 18 on 24 = 75%.",
  ["2021 gap = 24", "2025 gap = 42", "18 ÷ 24 = 75%"],
  why="110% is the growth in disbursement alone (120 → 252); 42.86% divides the rise by 2025's 42; 175% is 42 as a "
      "percentage of 24.", secs=70, stim=sid)

# ================================================================ Caselet DI (B1 I4 A6): sets of 6 and 5
T = "Caselet DI"
sid = stimulus("caselet", "Orders, returns and payouts of an online clothing seller",
               "In October 2026 an online seller received 2,400 orders in three categories: apparel, footwear and "
               "accessories, in the ratio 5 : 3 : 4. The return rates were 18% for apparel, 12% for footwear and 5% "
               "for accessories. The average order value was ₹800 for apparel, ₹1,500 for footwear and ₹450 for "
               "accessories. The marketplace keeps a commission of 15% of the value of the orders that are not "
               "returned and pays the rest to the seller; in addition, the seller pays ₹60 of reverse-shipping charge "
               "for every returned order. (Assume every order in a category has that category's average value.)")
cnt = {"A": F(2400 * 5, 12), "F": F(2400 * 3, 12), "X": F(2400 * 4, 12)}
rate = {"A": F(18, 100), "F": F(12, 100), "X": F(5, 100)}
aov = {"A": 800, "F": 1500, "X": 450}
ret = {k: cnt[k] * rate[k] for k in cnt}
kept = {k: cnt[k] - ret[k] for k in cnt}
assert cnt == {"A": 1000, "F": 600, "X": 800} and ret == {"A": 180, "F": 72, "X": 40}
Q(T, "Paragraph data", B, "How many footwear orders were returned in October 2026?",
  "72", ["528", "108", "40"],
  "Footwear orders = 3/12 of 2,400; then apply the 12% return rate",
  "Footwear orders = 3/12 × 2,400 = 600. Returned = 12% of 600 = 72.",
  ["600 footwear orders", "12% of 600 = 72"],
  why="528 is the footwear orders kept; 108 applies apparel's 18% to footwear; 40 is the accessories returned.",
  secs=40, stim=sid)

tr = sum(ret.values())
assert tr == 292 and pct2(F(tr, 2400)) == "12.17%" and r2(F(18 + 12 + 5, 3)) == F(1167, 100) and pct2(F(2108, 2400)) == "87.83%"
Q(T, "Paragraph data", I,
  "What percentage of all the orders received in October were returned (correct to two decimal places)?",
  "12.17%", ["11.67%", "87.83%", "13.11%"],
  "Count the returns in each category, add, and divide by 2,400",
  "Returns: apparel 18% of 1,000 = 180; footwear 72; accessories 5% of 800 = 40. Total = 292 of 2,400 = 12.17%.",
  ["Returns: 180 + 72 + 40 = 292", "292 ÷ 2,400 = 12.17%"],
  why="11.67% is the simple average of the three return rates; 87.83% is the share kept; 13.11% is the share of order "
      "value returned, not of orders.", secs=60, stim=sid)

kv = kept["A"] * aov["A"]
assert kv == 656000 and kv * F(85, 100) == 557600 and cnt["A"] * 800 == 800000
Q(T, "Paragraph data", I, "What was the total value of the apparel orders that were not returned?",
  "₹6,56,000", ["₹8,00,000", "₹5,57,600", "₹1,44,000"],
  "Apparel kept = 82% of 1,000 orders, each worth ₹800",
  "Apparel orders = 1,000; 180 were returned, so 820 were kept. Value = 820 × 800 = ₹6,56,000.",
  ["1,000 − 180 = 820 kept", "820 × 800 = ₹6,56,000"],
  why="₹8,00,000 includes the returned orders; ₹5,57,600 also deducts the 15% commission; ₹1,44,000 is the value "
      "returned.", secs=50, stim=sid)

def net(k, r=None):
    r_ = rate[k] if r is None else r
    rt = cnt[k] * r_
    return (cnt[k] - rt) * aov[k] * F(85, 100) - rt * 60


assert net("F") == 668880 and kept["F"] * 1500 * F(85, 100) == 673200 and 792000 - 4320 == 787680
assert cnt["F"] * 1500 * F(85, 100) == 765000
Q(T, "Paragraph data", A,
  "How much did the seller finally receive for the footwear orders, after the marketplace's commission and the "
  "reverse-shipping charges?",
  "₹6,68,880", ["₹6,73,200", "₹7,87,680", "₹7,65,000"],
  "Payout = 85% of the value of orders kept − ₹60 × orders returned",
  "Footwear kept = 600 − 72 = 528, worth 528 × 1,500 = ₹7,92,000. After 15% commission: ₹6,73,200. Less reverse "
  "shipping 72 × 60 = ₹4,320: ₹6,68,880.",
  ["Kept value = 528 × 1,500 = 7,92,000", "85% = 6,73,200", "− 72 × 60 = 4,320", "= ₹6,68,880"],
  why="₹6,73,200 forgets the reverse-shipping charges; ₹7,87,680 forgets the commission; ₹7,65,000 charges the "
      "commission on all 600 orders and ignores returns.", secs=85, stim=sid)

gain = net("A", F(10, 100)) - net("A")
assert gain == 59200 and 80 * 800 * F(85, 100) == 54400 and 80 * 800 == 64000 and 54400 - 4800 == 49600
Q(T, "Paragraph data", A,
  "If the return rate for apparel had been 10% instead of 18%, with everything else the same, by how much would the "
  "seller's net amount for October (the marketplace's payout minus the reverse-shipping charges) have been "
  "higher?",
  "₹59,200", ["₹54,400", "₹64,000", "₹49,600"],
  "80 fewer returns: each one adds 85% of ₹800 to the payout and saves ₹60 of reverse shipping",
  "Returns fall from 180 to 100, so 80 more apparel orders are kept. Extra payout = 80 × 800 × 0.85 = ₹54,400, and "
  "80 × ₹60 = ₹4,800 less reverse shipping. Total gain = ₹59,200.",
  ["80 more orders kept", "80 × 800 × 0.85 = 54,400", "+ 80 × 60 = 4,800", "= ₹59,200"],
  why="₹54,400 forgets the saved reverse shipping; ₹64,000 forgets the commission; ₹49,600 subtracts the shipping "
      "saving instead of adding it.", secs=95, stim=sid)

placed = sum(cnt[k] * aov[k] for k in cnt)
rv = sum(ret[k] * aov[k] for k in cnt)
assert (placed, rv) == (2060000, 270000) and pct2(F(rv, placed)) == "13.11%" and pct2(F(270000, 2400 * 800)) == "14.06%"
Q(T, "Paragraph data", A,
  "What percentage of the total value of all orders received was returned (correct to two decimal places)?",
  "13.11%", ["12.17%", "11.67%", "14.06%"],
  "Weight each category's returns by its order value",
  "Order value: 1,000 × 800 + 600 × 1,500 + 800 × 450 = 8,00,000 + 9,00,000 + 3,60,000 = ₹20,60,000. Returned value: "
  "180 × 800 + 72 × 1,500 + 40 × 450 = 1,44,000 + 1,08,000 + 18,000 = ₹2,70,000. Share = 2,70,000 ÷ 20,60,000 = "
  "13.11%.",
  ["Total value = ₹20,60,000", "Returned value = ₹2,70,000", "2,70,000 ÷ 20,60,000 = 13.11%"],
  why="12.17% is the share of orders (by number) returned; 11.67% averages the three rates; 14.06% divides by 2,400 "
      "orders at ₹800 each, as if every order were apparel.", secs=100, stim=sid)

HL = {"Affordable (up to ₹30 lakh)": (90, 80, 22, F(5, 10)), "Mid (₹30–75 lakh)": (60, 70, 48, F(4, 10)),
      "Premium (above ₹75 lakh)": (30, 60, 110, F(25, 100))}
sid = stimulus("caselet", "Home-loan applications at a bank branch by property segment, October 2026",
               "In October 2026 a bank branch received 180 home-loan applications, divided into three property "
               "segments as shown below. For each segment the table gives the number of applications, the "
               "percentage approved, the average loan per approved application and the processing fee charged on "
               "each approved loan (as a percentage of the loan amount).\n\n" +
               md_table(["Segment", "Applications", "Approved (%)", "Average loan (₹ lakh)", "Processing fee (%)"],
                        [[k, a, p, l, N(f)] for k, (a, p, l, f) in HL.items()]),
               {"columns": ["segment", "applications", "approved_pct", "avg_loan_lakh", "fee_pct"],
                "rows": [[k, a, p, l, float(f)] for k, (a, p, l, f) in HL.items()]})
apr = {k: a * F(p, 100) for k, (a, p, l, f) in HL.items()}
lam = {k: apr[k] * HL[k][2] for k in HL}
fee = {k: lam[k] * HL[k][3] / 100 for k in HL}
assert list(apr.values()) == [72, 42, 18] and list(lam.values()) == [1584, 2016, 1980]
assert sum(HL[k][0] for k in HL) == 180
ta = sum(apr.values())
assert ta == 132 and pct2(F(ta, 180)) == "73.33%" and F(80 + 70 + 60, 3) == 70 and pct2(F(48, 180)) == "26.67%"
Q(T, "Caselet with table", I,
  "What percentage of all the home-loan applications received in October were approved (correct to two decimal "
  "places)?",
  "73.33%", ["70.00%", "26.67%", "75.00%"],
  "Count the approvals in each segment; do not average the three percentages",
  "Approved: 80% of 90 = 72, 70% of 60 = 42, 60% of 30 = 18; total 132 of 180 = 73.33%.",
  ["72 + 42 + 18 = 132", "132 ÷ 180 = 73.33%"],
  why="70.00% is the simple average of 80%, 70% and 60%; 26.67% is the share not approved; 75.00% averages only the "
      "first two segments.", secs=55, stim=sid)

assert max(fee, key=fee.get) == "Mid (₹30–75 lakh)" and len(set(fee.values())) == 3
assert fee == {"Affordable (up to ₹30 lakh)": F(792, 100), "Mid (₹30–75 lakh)": F(8064, 1000),
               "Premium (above ₹75 lakh)": F(495, 100)}
assert max(lam, key=lam.get) == "Mid (₹30–75 lakh)" and max(HL, key=lambda k: HL[k][3]) == "Affordable (up to ₹30 lakh)"
Q(T, "Caselet with table", I, "Which segment earned the branch the most processing-fee income in October?",
  "Mid", ["Affordable", "Premium", "Affordable and Mid earned the same"],
  "Fee income = approvals × average loan × fee rate",
  "Affordable: 72 × 22 = 1,584 lakh × 0.5% = ₹7.92 lakh. Mid: 42 × 48 = 2,016 lakh × 0.4% = ₹8.064 lakh. Premium: "
  "18 × 110 = 1,980 lakh × 0.25% = ₹4.95 lakh. Mid is the highest.",
  ["Affordable 7.92 lakh", "Mid 8.064 lakh", "Premium 4.95 lakh"],
  why="Affordable has the highest fee rate and most approvals but earns ₹7.92 lakh, slightly less; Premium has the "
      "largest loans but the lowest rate and fewest approvals; the two top segments differ by ₹14,400.", secs=75,
  stim=sid)

avg_l = F(sum(lam.values()), ta)
assert sum(lam.values()) == 5580 and r2(avg_l) == F(4227, 100) and F(22 + 48 + 110, 3) == 60 and F(5580, 180) == 31
Q(T, "Caselet with table", A,
  "What was the average loan amount per approved application, taking all three segments together (correct to two "
  "decimal places)?",
  "₹42.27 lakh", ["₹60.00 lakh", "₹31.00 lakh", "₹48.00 lakh"],
  "Average = total amount approved ÷ number of approvals",
  "Total approved = 1,584 + 2,016 + 1,980 = 5,580 lakh over 132 approvals. Average = 5,580 ÷ 132 = ₹42.27 lakh.",
  ["Total = ₹5,580 lakh", "Approvals = 132", "5,580 ÷ 132 = 42.27"],
  why="₹60.00 lakh is the simple average of the three segment averages; ₹31.00 lakh divides by all 180 applications; "
      "₹48.00 lakh is the Mid segment's average.", secs=75, stim=sid)

tf = sum(fee.values())
assert F(792, 100) + F(8064, 1000) == F(15984, 1000) and F(792, 100) + F(8064, 1000) + F(99, 10) == F(25884, 1000) and tf == F(20934, 1000) and tf * 100000 == 2093400 and F(5580 * 4, 1000) == F(2232, 100)
Q(T, "Caselet with table", A, "What total processing fee did the branch earn on the loans approved in October?",
  "₹20,93,400", ["₹22,32,000", "₹15,98,400", "₹25,88,400"],
  "Fee = loan amount × fee rate, segment by segment",
  "Affordable 1,584 lakh × 0.5% = 7.92 lakh; Mid 2,016 lakh × 0.4% = 8.064 lakh; Premium 1,980 lakh × 0.25% = 4.95 "
  "lakh. Total = 20.934 lakh = ₹20,93,400.",
  ["7.92 + 8.064 + 4.95 = 20.934 lakh", "= ₹20,93,400"],
  why="₹22,32,000 applies 0.4% to the whole ₹5,580 lakh; ₹15,98,400 leaves out the Premium segment's fee; "
      "₹25,88,400 charges 0.5% on Premium loans too.",
  secs=85, stim=sid)

d_ = (30 * F(70, 100) - 18) * 110 + (90 * F(70, 100) - 72) * 22
assert d_ == 132 and 3 * 110 == 330 and 9 * 22 == 198
Q(T, "Caselet with table", A,
  "Suppose the approval rate rises to 70% in the Premium segment and falls to 70% in the Affordable segment, with "
  "the same applications and average loans, and the Mid segment unchanged. How would the total loan amount "
  "approved change?",
  "It would rise by ₹1.32 crore", ["It would rise by ₹3.30 crore", "It would fall by ₹1.98 crore",
                                   "It would not change"],
  "Work out the change in approvals in each segment and multiply by that segment's average loan",
  "Premium: 70% of 30 = 21, which is 3 more approvals × ₹110 lakh = +₹330 lakh. Affordable: 70% of 90 = 63, which is "
  "9 fewer × ₹22 lakh = −₹198 lakh. Net change = +₹132 lakh = +₹1.32 crore.",
  ["Premium: +3 × 110 = +330 lakh", "Affordable: −9 × 22 = −198 lakh", "Net = +132 lakh = ₹1.32 crore"],
  why="'Rise by ₹3.30 crore' counts only the Premium gain; 'fall by ₹1.98 crore' counts only the Affordable loss; "
      "'no change' assumes the two rate changes cancel because both move to 70%.", secs=95, stim=sid)

# ================================================================ Missing DI (B2 I1 A1): one set of 4
T = "Missing DI"
dash = "—"
WH = {"W1": (800, None, 65, None), "W2": (None, 450, 75, None), "W3": (1000, 840, None, None),
      "W4": (None, None, 76, 288), "W5": (750, None, None, 195)}
sid = stimulus("data_table", "Capacity, stock and utilisation of five grain warehouses (some values missing)",
               "The table shows, for five grain warehouses on 1 October 2026, the storage capacity (tonnes), the "
               "stock held (tonnes), the utilisation (stock as a percentage of capacity) and the free space "
               "(capacity − stock, in tonnes). Some values are missing (—); work them out from the others.\n\n" +
               md_table(["Warehouse", "Capacity (tonnes)", "Stock (tonnes)", "Utilisation (%)", "Free space (tonnes)"],
                        [[k, *[dash if c is None else ind(c) for c in v]] for k, v in WH.items()]),
               {"columns": ["warehouse", "capacity_t", "stock_t", "utilisation_pct", "free_t"],
                "rows": [[k, *v] for k, v in WH.items()]})
cap = {"W1": F(800), "W2": F(450) / F(75, 100), "W3": F(1000), "W4": F(288) / F(24, 100), "W5": F(750)}
stk = {"W1": F(800) * F(65, 100), "W2": F(450), "W3": F(840), "W4": cap["W4"] - 288, "W5": F(750 - 195)}
assert cap == {"W1": 800, "W2": 600, "W3": 1000, "W4": 1200, "W5": 750}
assert stk == {"W1": 520, "W2": 450, "W3": 840, "W4": 912, "W5": 555}
util = {k: stk[k] / cap[k] * 100 for k in cap}
assert util == {"W1": 65, "W2": 75, "W3": 84, "W4": 76, "W5": 74} and len(set(util.values())) == 5
Q(T, "Table with missing values", B, "What is the utilisation of warehouse W3?",
  "84%", ["16%", "119.05%", "8.4%"],
  "Utilisation = stock ÷ capacity × 100",
  "W3: 840 ÷ 1,000 × 100 = 84%.",
  ["840 ÷ 1,000 = 0.84 = 84%"],
  why="16% is the free space as a percentage; 119.05% divides capacity by stock; 8.4% slips a decimal place.", secs=30,
  stim=sid)

assert cap["W2"] == 600 and F(450 * 75, 100) == F(675, 2) and 450 + 450 * F(25, 100) == F(1125, 2)
Q(T, "Table with missing values", B, "What is the storage capacity of warehouse W2?",
  "600 tonnes", ["337.5 tonnes", "562.5 tonnes", "525 tonnes"],
  "Capacity = stock ÷ utilisation",
  "Stock 450 tonnes is 75% of capacity, so capacity = 450 ÷ 0.75 = 600 tonnes (free space 150 tonnes).",
  ["450 = 0.75 × capacity", "Capacity = 600 tonnes"],
  why="337.5 tonnes takes 75% of the stock; 562.5 tonnes adds 25% of the stock to it; 525 tonnes adds 75 to 450.",
  secs=40, stim=sid)

assert stk["W4"] == 912 and cap["W4"] == 1200 and F(288, F(76, 100)) == F(7200, 19) and 288 * 76 // 24 == 912
assert F(288 * 100, 76) != 912
Q(T, "Table with missing values", I, "How many tonnes of stock does warehouse W4 hold?",
  "912 tonnes", ["1,200 tonnes", "378.95 tonnes", "218.88 tonnes"],
  "Free space is the unused (100 − 76)% = 24% of capacity",
  "Free space 288 tonnes = 24% of capacity, so capacity = 288 ÷ 0.24 = 1,200 tonnes. Stock = 1,200 − 288 = 912 tonnes "
  "(76% of 1,200).",
  ["288 = 24% of capacity", "Capacity = 1,200", "Stock = 1,200 − 288 = 912"],
  why="1,200 tonnes is the capacity, not the stock; 378.95 tonnes treats 288 as 76% of the capacity; 218.88 tonnes "
      "takes 76% of the free space.", secs=60, stim=sid)
assert r2(F(288, F(76, 100))) == F(37895, 100) and r2(288 * F(76, 100)) == F(21888, 100)

tc, ts = sum(cap.values()), sum(stk.values())
assert (tc, ts) == (4350, 3277) and pct2(F(ts, tc)) == "75.33%" and F(65 + 75 + 84 + 76 + 74, 5) == F(748, 10)
assert pct2(F(tc - ts, tc)) == "24.67%"
Q(T, "Table with missing values", A,
  "Taking the five warehouses together, what is the overall utilisation (correct to two decimal places)?",
  "75.33%", ["74.80%", "24.67%", "76.00%"],
  "Fill in every missing capacity and stock first; then divide the totals",
  "Capacities: 800, 600, 1,000, 1,200, 750 = 4,350 tonnes. Stocks: 520, 450, 840, 912, 555 = 3,277 tonnes. Overall "
  "utilisation = 3,277 ÷ 4,350 = 75.33%.",
  ["W1 stock 520; W2 capacity 600; W4: 1,200 and 912; W5 stock 555", "Totals: 4,350 and 3,277",
   "3,277 ÷ 4,350 = 75.33%"],
  why="74.80% is the simple average of the five utilisation percentages; 24.67% is the free share; 76.00% is W4's "
      "utilisation only.", secs=100, stim=sid)

# ================================================================ Quantity Comparison (B1 I2 A2)
T = "Quantity Comparison"
QREL = {">": "Quantity I > Quantity II", ">=": "Quantity I ≥ Quantity II", "<": "Quantity I < Quantity II",
        "<=": "Quantity I ≤ Quantity II", "cbe": "Quantity I = Quantity II or the relationship cannot be established"}


def qc(sub, diff, q1, q2, vals1, vals2, expect, wrong_syms, concept, expl, steps, short=None, why=None, secs=None,
       by=None):
    got = relation(vals1, vals2)
    assert got == expect, (q1, got)
    assert expect not in wrong_syms and "cbe" not in wrong_syms and len(set(wrong_syms)) == 2
    assert all(a != b for a in vals1 for b in vals2), "avoid exactly equal quantities"
    # every pair at least 2% apart, so rounding in mental arithmetic cannot flip the relation
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


pr = [p for p in range(51, 80) if all(p % d for d in range(2, p))]
nd = sum(1 for d in range(1, 37) if 36 % d == 0)
assert pr == [53, 59, 61, 67, 71, 73, 79] and nd == 9
qc("Quantity I vs II", B, "The number of prime numbers between 50 and 80",
   "The number of positive factors of 36", [F(len(pr))], [F(nd)], "<", [">", ">="],
   "List the primes; count factors from the prime factorisation 36 = 2² × 3²",
   "Primes between 50 and 80: 53, 59, 61, 67, 71, 73, 79, so Quantity I = 7. Factors of 36: (2 + 1)(2 + 1) = 9, so "
   "Quantity II = 9. Quantity I < Quantity II.",
   ["I: 53, 59, 61, 67, 71, 73, 79 ⇒ 7", "II: 36 = 2² × 3² ⇒ 3 × 3 = 9", "7 < 9"],
   why="'I > II' and 'I ≥ II' come from counting 51, 57 or 77 as primes (they are 3 × 17, 3 × 19 and 7 × 11) or "
       "from missing factors of 36.", secs=50, by=BRUTE)

q1v = F(1, 5) * 100
q2v = (F(7, 6) - 1) * 100
assert q1v == 20 and q2v == F(50, 3)
qc("Arithmetic-based comparison", I, "The discount percentage equivalent to the offer 'buy 4, get 1 free'",
   "The profit percentage when the cost price of 7 articles equals the selling price of 6 articles",
   [q1v], [q2v], ">", ["<", "<="],
   "Buy 4 get 1 free: pay for 4, receive 5. CP of 7 = SP of 6: profit = 1 article on 6",
   "Quantity I: the buyer pays for 4 of 5 items, a discount of 1/5 = 20%. Quantity II: SP of 6 = CP of 7, so profit = "
   "1/6 = 16⅔%. Quantity I > Quantity II.",
   ["I: 1/5 = 20%", "II: (7 − 6)/6 = 16⅔%", "20 > 16⅔"],
   why="'I < II' and 'I ≤ II' take the free item as 25% of 4 bought (1/4) for Quantity I, or the profit as 1/6 of 7.",
   secs=60)

nums = [F(10 * a + b) for a in range(1, 10) for b in range(10) if a + b == 9 and abs(a - b) == 3]
assert nums == [36, 63]
qc("Arithmetic-based comparison", I, "A two-digit number whose digits add up to 9 and differ by 3",
   "50", nums, [F(50)], "cbe", [">", "<="],
   "Find every number that fits the description before comparing",
   "Digits a + b = 9 and a − b = ±3 give the digit pairs (6, 3) and (3, 6), so Quantity I is 63 or 36. 63 > 50 but "
   "36 < 50, so no single relation holds.",
   ["a + b = 9, |a − b| = 3", "Numbers: 63 or 36", "63 > 50, 36 < 50", "Relationship cannot be established"],
   why="'I > II' and 'I ≥ II' consider only 63; 'I < II' and 'I ≤ II' consider only 36.", secs=55, by=BRUTE)

p1 = F(26 + 2, 52)
p2 = 1 - F(25, 36)
assert p1 == F(7, 13) and p2 == F(11, 36)
qc("Arithmetic-based comparison", A,
   "The probability that a card drawn at random from a pack of 52 is a red card or a king",
   "The probability of getting at least one six when a fair die is rolled twice", [p1], [p2], ">", ["<", "<="],
   "P(A or B) = P(A) + P(B) − P(both); P(at least one) = 1 − P(none)",
   "Quantity I: 26 red cards + 4 kings − 2 red kings = 28 cards, so 28/52 = 7/13 ≈ 0.538. Quantity II: 1 − (5/6)² = "
   "11/36 ≈ 0.306. Quantity I > Quantity II.",
   ["I: (26 + 4 − 2)/52 = 7/13 ≈ 0.538", "II: 1 − 25/36 = 11/36 ≈ 0.306", "0.538 > 0.306"],
   why="'I < II' and 'I ≤ II' would need Quantity II to exceed 0.538, e.g. by taking 'at least one six' as "
       "1/6 + 1/6 + … rather than 11/36.", secs=80)

q1v = F(22, 7) * 7 * 7
q2v = F(2 * 9 * 9)
assert q1v == 154 and q2v == 162
qc("Arithmetic-based comparison", A,
   "Area (cm²) of the largest circle that can be drawn inside a square of side 14 cm (take π = 22/7)",
   "Area (cm²) of the largest square that can be drawn inside a circle of radius 9 cm", [q1v], [q2v], "<",
   [">", ">="],
   "The circle in a square has diameter = side; the square in a circle has diagonal = diameter, so area = d²/2",
   "Quantity I: radius 7 cm, area = 22/7 × 49 = 154 cm². Quantity II: the square's diagonal is 18 cm, so its area = "
   "18²/2 = 162 cm². Quantity I < Quantity II.",
   ["I: r = 7 ⇒ 154 cm²", "II: diagonal 18 ⇒ area 18²/2 = 162 cm²", "154 < 162"],
   why="'I > II' and 'I ≥ II' come from taking the square's side as 9 cm (area 81) or as 18 cm (area 324 compared the "
       "other way), instead of using the diagonal.", secs=85)

# ================================================================ Data Sufficiency (Quant) (B1 I1 A1)
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


cands = [(F(a, 10), F(b, 10)) for a in range(1, 301) for b in range(1, 301)]
verdict = ds2_verdict(cands, lambda c: (c[0], c[1]) == (16, 12),
                      lambda c: (c[0] / 2) ** 2 + (c[1] / 2) ** 2 == 100, lambda c: c[0] * c[1] / 2)
assert verdict == "I" and {c[0] * c[1] / 2 for c in cands if (c[0] / 2) ** 2 + (c[1] / 2) ** 2 == 100} >= {96, F(5376, 100)}
Q(T, "Two-statement", B,
  f"{DS_PRE}\nQuestion: What is the area of the rhombus?\n"
  "I. Its diagonals are 16 cm and 12 cm long.\n"
  "II. Each of its sides is 10 cm long.",
  DS2["I"], [DS2["II"], DS2["either"], DS2["both"]],
  "Area of a rhombus = ½ × product of the diagonals; a side alone does not fix the shape",
  "I alone: area = ½ × 16 × 12 = 96 cm². II alone: a rhombus of side 10 cm can be squashed into many shapes (for "
  "example diagonals 16 and 12 give 96 cm², diagonals 19.2 and 5.6 give 53.76 cm²), so II is not sufficient.",
  ["I: ½ × 16 × 12 = 96 cm²", "II: side 10 fits many pairs of diagonals", "Answer: I alone"],
  why="'II alone' assumes a fixed shape for a given side; 'either' wrongly accepts II; 'both needed' overlooks that I "
      "alone already gives the area.", secs=45, by=BRUTE)

cands = [(F(L), F(k, 4)) for L in range(25, 1501, 25) for k in range(1, 401)]
conds = [lambda c: c[0] == 15 * c[1], lambda c: c[0] + 300 == 27 * c[1], lambda c: c[0] > 300]
mp_ = suff_map(cands, conds, lambda c: c[1])
assert mp_ == {(0,): False, (1,): False, (2,): False, (0, 1): True, (0, 2): False, (1, 2): False, (0, 1, 2): True}
assert {c[1] for c in cands if all(f(c) for f in conds[:2])} == {25}
Q(T, "Three-statement", I,
  f"{DS3_PRE}\nQuestion: What is the speed of the train?\n"
  "I. The train passes a signal pole in 15 seconds.\n"
  "II. The train passes a 300 m long platform in 27 seconds.\n"
  "III. The train is more than 300 m long.",
  "Only I and II together are sufficient",
  ["Any two of the three statements together are sufficient", "Only I and III together are sufficient",
   "All three statements together are necessary"],
  "Two crossing times with a known platform length fix the speed; an inequality on the length does not",
  "I + II: L = 15v and L + 300 = 27v ⇒ 12v = 300 ⇒ v = 25 m/s (90 km/h), L = 375 m. I + III: L = 15v with L > 300 "
  "allows many speeds. II + III: L + 300 = 27v with L > 300 also allows many (e.g. L = 375, v = 25 or L = 1,050, v = 50).",
  ["I + II: 12v = 300 ⇒ v = 25 m/s", "I + III: only v > 20 m/s", "II + III: several (L, v) pairs",
   "Answer: only I and II"],
  why="'Any two' wrongly accepts I + III and II + III; 'only I and III' gives only a range; 'all three' is more than "
      "needed, since III adds nothing to I + II.", secs=75, by=BRUTE)

cands = [(F(p), F(r)) for p in range(100, 20001, 100) for r in range(1, 31)]
verdict = ds2_verdict(cands, lambda c: c[0] * (c[1] / 100) ** 2 == 50 and c[1] == 10,
                      lambda c: c[0] * c[1] / 100 * 3 == 1500 and c[1] == 10, lambda c: c[0])
assert verdict == "either"
Q(T, "Two-statement", A,
  f"{DS_PRE}\nQuestion: What is the sum of money?\n"
  "I. At 10% per annum, the compound interest (compounded annually) on it for 2 years exceeds the simple interest on "
  "it for 2 years by ₹50.\n"
  "II. The simple interest on it for 3 years at 10% per annum is ₹1,500.",
  DS2["either"], [DS2["I"], DS2["II"], DS2["both"]],
  "For 2 years, CI − SI = P × r²; SI = P × r × t",
  "I alone: P × (0.1)² = 50 ⇒ P = ₹5,000. II alone: P × 0.1 × 3 = 1,500 ⇒ P = ₹5,000. Each statement alone gives the "
  "sum.",
  ["I: P × 0.01 = 50 ⇒ P = 5,000", "II: 0.3P = 1,500 ⇒ P = 5,000", "Either alone is sufficient"],
  why="'I alone' and 'II alone' each overlook that the other statement also fixes P; 'both needed' assumes the rate "
      "must be found first, but both statements state it.", secs=70, by=BRUTE)

# ================================================================ checks and output
assert len(QUESTIONS) == TOTAL, len(QUESTIONS)
assert len(STIMULI) == 11

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_007_plan.json").read_text(encoding="utf-8"))
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
    "batch_id": "BATCH_007",
    "created_at": TODAY,
    "notes": "BATCH_007, Quantitative Aptitude part: 199 original questions (60 Basic, 80 Intermediate, 59 Advanced) "
             "with 11 shared DI stimuli on new data sets. Every answer was recomputed by tools/batch_007/quant.py "
             "before writing; quantity-comparison values are at least 2% apart. Questions tagged "
             "ai:independent-check were also re-solved from the stem, options and data set alone by a separate "
             "solver. Pending human review.",
    "stimuli": STIMULI,
    "questions": QUESTIONS,
}
out = ROOT / "batches" / "parts" / "BATCH_007_QUANT.json"
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
