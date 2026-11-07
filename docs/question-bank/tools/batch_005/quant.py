"""Writes batches/parts/BATCH_005_QUANT.json: the 200 Quantitative Aptitude questions of BATCH_005.

Every answer is recomputed here before the file is written: arithmetic with exact fractions, series regenerated
from their rule (wrong-number series: exactly one term differs from the regenerated series), quadratic roots
substituted back into the equations, probabilities and arrangements counted by brute force, data-sufficiency
statements checked by enumerating candidate cases, approximation answers checked to be the option nearest the
exact value by a clear margin. If any assertion fails, nothing is written.

Structure and helpers follow tools/batch_004/quant.py (relation-option guards, no-equal-quantity rule for
quantity comparison, balanced key shuffler with a new seed, approximation margin check, set-size asserts).
Contexts, data sets and number templates are new: none of the DI themes of batches 0-4 is reused, and the
arithmetic templates were chosen after reading all earlier stems.

    python tools/batch_005/quant.py          (run from docs/question-bank)
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

# Balanced answer keys: exactly 50 of each letter, order fixed by the seed (new seed for batch 5).
_rng = random.Random(20261105 + 5)
KEYS = list("ABCD" * (TOTAL // 4))
_rng.shuffle(KEYS)

QUESTIONS, STIMULI = [], []
_set_pos = {}
_FIRST_ID = 806
_FIRST_STIM = 5001
RECOMPUTE = ["script:recompute", "ai:author-solve"]
BRUTE = ["script:recompute", "script:brute-force-unique", "ai:author-solve"]

# Questions that a separate solver re-answered from the stem, options and data set alone (no key, no solution)
# and whose answer matched the key. Only these carry ai:independent-check. Every third question
# (BANK_QUANT_000806, _000809, ..., _001004: 67 questions) was given to two separate solver agents (34 and 33
# questions); all 67 answers matched the key, no question was flagged, and none was changed afterwards.
INDEPENDENT = {f"BANK_QUANT_{n:06d}" for n in range(806, 1006, 3)}

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


def ratio(*vals) -> str:
    vals = [F(v) for v in vals]
    den = math.lcm(*[v.denominator for v in vals])
    ints = [int(v * den) for v in vals]
    g = math.gcd(*ints)
    return " : ".join(str(i // g) for i in ints)


def near(a, b, tol=1e-9):
    return abs(float(a) - float(b)) < tol


def r2(x) -> F:
    """Round half up to two decimals (for stems that fix two-decimal precision)."""
    return F(math.floor(F(x) * 100 + F(1, 2)), 100)


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

# ================================================================ Simplification (B2 I4 A2)
T = "Simplification"
rhs = 13 * 9 + 3
v = F(rhs + F(384, 16), 6)
assert rhs == 120 and F(384, 16) == 24 and v == 24
assert F(rhs - 24, 6) == 16 and F(rhs, 6) == 20 and rhs + 24 == 144
Q(T, "BODMAS", B, QMARK + "? × 6 − 384 ÷ 16 = 13 × 9 + 3",
  "24", ["16", "20", "144"],
  "Simplify each side with ÷ and × before + and −, then isolate the unknown",
  "Right side: 13 × 9 + 3 = 120. Left side: 384 ÷ 16 = 24, so 6 × ? − 24 = 120. Then 6 × ? = 144 and ? = 24.",
  ["13 × 9 + 3 = 120", "384 ÷ 16 = 24", "6 × ? = 120 + 24 = 144", "? = 144 ÷ 6 = 24"],
  why="16 subtracts the 24 from 120 instead of adding it; 20 ignores the 384 ÷ 16 term; 144 stops before dividing by "
      "6.", secs=35)

assert F(15) * F(6, 10) == 9 and 9 ** 3 == 729 and 15 ** 3 == 3375 and 6 ** 3 == 216
Q(T, "Square and cube roots", B, QMARK + "∛? ÷ √0.36 = 15",
  "729", ["9", "3,375", "216"],
  "Evaluate the known root, undo the division, then cube",
  "√0.36 = 0.6, so ∛? = 15 × 0.6 = 9 and ? = 9³ = 729.",
  ["√0.36 = 0.6", "∛? = 15 × 0.6 = 9", "? = 9³ = 729"],
  why="9 is ∛?, not ?; 3,375 = 15³ forgets the √0.36; 216 = 6³ takes √0.36 as 0.4.", secs=40)

lo, hi = F(3, 7), F(4, 9)
cands = {"7/16": F(7, 16), "5/11": F(5, 11), "2/5": F(2, 5), "9/20": F(9, 20)}
inside = [k for k, x in cands.items() if lo < x < hi]
assert inside == ["7/16"] and F(3 + 4, 7 + 9) == F(7, 16)
Q(T, "Fractions and decimals", I, "Which of the following fractions lies between 3/7 and 4/9?",
  "7/16", ["5/11", "2/5", "9/20"],
  "Compare by decimals or cross-multiplication; the mediant (a + c)/(b + d) always lies between a/b and c/d",
  "3/7 ≈ 0.4286 and 4/9 ≈ 0.4444. 7/16 = 0.4375 lies between them; 5/11 ≈ 0.4545 and 9/20 = 0.45 are above 4/9, and "
  "2/5 = 0.4 is below 3/7.",
  ["3/7 ≈ 0.4286, 4/9 ≈ 0.4444", "7/16 = 0.4375 ✓", "5/11 ≈ 0.4545, 9/20 = 0.45 (too large)", "2/5 = 0.4 (too small)"],
  short="Mediant: (3 + 4)/(7 + 9) = 7/16 lies between 3/7 and 4/9.",
  why="5/11 and 9/20 are slightly larger than 4/9; 2/5 is smaller than 3/7.", secs=55)

x5 = math.log(3, 5)
assert near(25 ** (x5 + 1), 225) and 25 * 3 == 75 and 25 + 9 == 34 and 5 * 9 == 45
Q(T, "Surds and indices", I, "If 5ˣ = 3, what is the value of 25^(x + 1)?",
  "225", ["75", "34", "45"],
  "Write 25 as 5²: 25^(x + 1) = 25 × (5ˣ)²",
  "25^(x + 1) = 25ˣ × 25 = (5²)ˣ × 25 = (5ˣ)² × 25 = 3² × 25 = 225.",
  ["25^(x + 1) = 25 × 25ˣ", "25ˣ = (5ˣ)² = 9", "25 × 9 = 225"],
  why="75 takes 25ˣ as 3 instead of 3²; 34 adds 25 and 9 instead of multiplying; 45 multiplies 9 by 5 instead of 25.",
  secs=50)

assert 80 ** 2 == 6400 and 6412 - 6400 == 12 and 81 ** 2 - 6412 == 149 and 6412 - 79 ** 2 == 171
assert math.isqrt(6412) == 80
Q(T, "Square and cube roots", I,
  "What is the least number that must be subtracted from 6,412 to make it a perfect square?",
  "12", ["149", "171", "80"],
  "Find the largest perfect square not exceeding the number",
  "80² = 6,400 and 81² = 6,561, so the largest perfect square below 6,412 is 6,400. Subtract 6,412 − 6,400 = 12.",
  ["80² = 6,400 ≤ 6,412 < 6,561 = 81²", "6,412 − 6,400 = 12"],
  why="149 must be added to reach 81² = 6,561; 171 goes one square too far down, to 79² = 6,241; 80 is the square "
      "root of 6,400, not the number to subtract.", secs=50)

v = F(125, 1000) * F(64, 100) / F(16, 1000) + F(12, 10) * F(75, 100)
assert v == F(59, 10) and F(8, 100) / F(16, 1000) == 5 and F(1, 2) + F(9, 10) == F(14, 10) and 5 + F(9, 100) == F(509, 100)
Q(T, "Fractions and decimals", I, QMARK + "0.125 × 0.64 ÷ 0.016 + 1.2 × 0.75 = ?",
  "5.9", ["1.4", "0.59", "5.09"],
  "Work left to right for × and ÷, then add; count decimal places carefully",
  "0.125 × 0.64 = 0.08 and 0.08 ÷ 0.016 = 5. Also 1.2 × 0.75 = 0.9. So the value is 5 + 0.9 = 5.9.",
  ["0.125 × 0.64 = 0.08", "0.08 ÷ 0.016 = 80 ÷ 16 = 5", "1.2 × 0.75 = 0.9", "5 + 0.9 = 5.9"],
  why="1.4 takes 0.08 ÷ 0.016 as 0.5; 0.59 misplaces the decimal point in the final sum; 5.09 takes 1.2 × 0.75 as "
      "0.09.", secs=55)

rts = {"∜6": 6 ** 0.25, "∛4": 4 ** (1 / 3), "√2": 2 ** 0.5, "⁶√10": 10 ** (1 / 6)}
order = sorted(rts, key=rts.get, reverse=True)
assert order == ["∛4", "∜6", "⁶√10", "√2"] and (6 ** 3, 4 ** 4, 2 ** 6, 10 ** 2) == (216, 256, 64, 100)
Q(T, "Surds and indices", A, "Which of the following arranges ∜6, ∛4, √2 and ⁶√10 in descending order?",
  "∛4 > ∜6 > ⁶√10 > √2", ["⁶√10 > ∜6 > ∛4 > √2", "√2 > ∛4 > ∜6 > ⁶√10", "∜6 > ∛4 > ⁶√10 > √2"],
  "Bring all the roots to a common index (the LCM of 4, 3, 2 and 6 is 12) and compare the 12th powers",
  "Raise each number to the 12th power: (∜6)¹² = 6³ = 216, (∛4)¹² = 4⁴ = 256, (√2)¹² = 2⁶ = 64 and (⁶√10)¹² = 10² = 100. "
  "So ∛4 > ∜6 > ⁶√10 > √2.",
  ["LCM of 4, 3, 2, 6 = 12", "∜6 → 6³ = 216", "∛4 → 4⁴ = 256", "√2 → 2⁶ = 64", "⁶√10 → 10² = 100",
   "256 > 216 > 100 > 64"],
  why="⁶√10 > ∜6 > ∛4 > √2 orders by the number under the root and ignores the index; √2 > ∛4 > ∜6 > ⁶√10 orders by the "
      "index alone; ∜6 > ∛4 > ⁶√10 > √2 swaps the top two, which would need 216 > 256.", secs=90)

v = sum(F(1, n * (n + 1) * (n + 2)) for n in range(2, 9))
assert v == F(7, 90) and F(1, 2) * (F(1, 6) - F(1, 90)) == v
assert F(1, 6) - F(1, 90) == F(7, 45) and F(1, 2) * F(1, 6) == F(1, 12) and F(1, 2) * (F(1, 6) - F(1, 72)) == F(11, 144)
Q(T, "Fractions and decimals", A,
  "Find the value of 1/(2 × 3 × 4) + 1/(3 × 4 × 5) + 1/(4 × 5 × 6) + … + 1/(8 × 9 × 10).",
  "7/90", ["7/45", "1/12", "11/144"],
  "Split each term: 1/(n(n + 1)(n + 2)) = ½ × [1/(n(n + 1)) − 1/((n + 1)(n + 2))], so the sum telescopes",
  "Each term is half the difference of two consecutive terms of 1/(n(n + 1)). Adding from n = 2 to n = 8, everything "
  "cancels except the first and the last: ½ × [1/(2 × 3) − 1/(9 × 10)] = ½ × (1/6 − 1/90) = ½ × 14/90 = 7/90.",
  ["1/(n(n + 1)(n + 2)) = ½[1/(n(n + 1)) − 1/((n + 1)(n + 2))]", "Sum = ½[1/(2·3) − 1/(9·10)]",
   "1/6 − 1/90 = 14/90", "½ × 14/90 = 7/90"],
  why="7/45 forgets the factor ½; 1/12 keeps only the first part, ½ × 1/6; 11/144 ends the telescoping at 1/(8 × 9) "
      "instead of 1/(9 × 10).", secs=100)

# ================================================================ Approximation (B3 I6 A4)
T = "Approximation"
exact = 1.1998 * 450.2 - 0.5997 * 249.8
nearest(exact, [390, 690, 375, 405], 390)
Q(T, "Percentage approximation", B, APPROX + "119.98% of 450.2 − 59.97% of 249.8 ≈ ?",
  "390", ["690", "375", "405"],
  "Round each percentage and number; 120% of a number is the number plus one-fifth of it",
  "120% of 450 = 540 and 60% of 250 = 150, so the value ≈ 540 − 150 = 390.",
  ["120% of 450 = 540", "60% of 250 = 150", "540 − 150 = 390"],
  why="690 adds the two parts instead of subtracting; 375 and 405 are 15 away from the exact value (about 390.3).",
  secs=35)

exact = math.sqrt(3249.2) + 2743.9 ** (1 / 3) - 6.98
nearest(exact, [64, 71, 54, 74], 64)
Q(T, "Root approximation", B, APPROX + "√3249.2 + ∛2743.9 − 6.98 ≈ ?",
  "64", ["71", "54", "74"],
  "Round to the nearest perfect square and cube: 3249 = 57², 2744 = 14³",
  "√3249.2 ≈ 57, ∛2743.9 ≈ 14 and 6.98 ≈ 7, so the value ≈ 57 + 14 − 7 = 64.",
  ["√3249 = 57", "∛2744 = 14", "57 + 14 − 7 = 64"],
  why="71 ignores the − 6.98; 54 and 74 are 10 away from the exact value (about 64.0).", secs=40)

exact = 18.03 * 24.98 / 14.97 + 9.02 ** 2
nearest(exact, [111, 48, 121, 101], 111)
Q(T, "Mixed approximation", B, APPROX + "(18.03 × 24.98) ÷ 14.97 + 9.02² ≈ ?",
  "111", ["48", "121", "101"],
  "Round to whole numbers; cancel before multiplying",
  "18 × 25 ÷ 15 = 450 ÷ 15 = 30, and 9² = 81, so the value ≈ 30 + 81 = 111.",
  ["18 × 25 = 450", "450 ÷ 15 = 30", "9² = 81", "30 + 81 = 111"],
  why="48 doubles 9 instead of squaring it (30 + 18); 121 and 101 are 10 away from the exact value (about 111.4).",
  secs=40)

exact = 4.99 ** 3 - 3.01 ** 3
nearest(exact, [98, 8, 152, 16], 98)
assert 5 ** 3 - 3 ** 3 == 98 and (5 - 3) ** 3 == 8 and 5 ** 3 + 3 ** 3 == 152 and 5 ** 2 - 3 ** 2 == 16
Q(T, "Mixed approximation", I, APPROX + "4.99³ − 3.01³ ≈ ?",
  "98", ["8", "152", "16"],
  "Round the bases first, then cube each one separately",
  "4.99 ≈ 5 and 3.01 ≈ 3, so the value ≈ 5³ − 3³ = 125 − 27 = 98.",
  ["5³ = 125", "3³ = 27", "125 − 27 = 98"],
  why="8 cubes the difference, (5 − 3)³; 152 adds the cubes; 16 squares instead of cubing (25 − 9).", secs=45)

exact = (math.sqrt(143.9) + math.sqrt(224.8)) ** 2
nearest(exact, [729, 369, 27, 784], 729)
Q(T, "Root approximation", I, APPROX + "(√143.9 + √224.8)² ≈ ?",
  "729", ["369", "27", "784"],
  "Find each square root first; the square of a sum is not the sum of the squares",
  "√143.9 ≈ 12 and √224.8 ≈ 15, so the bracket ≈ 27 and its square ≈ 729.",
  ["√144 = 12", "√225 = 15", "12 + 15 = 27", "27² = 729"],
  why="369 adds 144 and 225 and drops the cross term 2 × 12 × 15; 27 forgets to square; 784 = 28² takes √143.9 as 13.",
  secs=45)

exact = (0.6502 * 1199.8) / (0.1298 * 299.7)
nearest(exact, [20, 2, 200, 26], 20)
assert F(65, 100) * 1200 == 780 and F(13, 100) * 300 == 39 and F(780, 39) == 20 and F(780, 30) == 26
Q(T, "Percentage approximation", I, APPROX + "(65.02% of 1199.8) ÷ (12.98% of 299.7) ≈ ?",
  "20", ["2", "200", "26"],
  "Round each percentage and number, evaluate both brackets, then divide",
  "65% of 1200 = 780 and 13% of 300 = 39, so the value ≈ 780 ÷ 39 = 20.",
  ["65% of 1200 = 780", "13% of 300 = 39", "780 ÷ 39 = 20"],
  why="2 and 200 slip a decimal place; 26 takes 12.98% as 10% (780 ÷ 30).", secs=50)

exact = 3599.6 / (0.1498 * 1999.8)
nearest(exact, [12, 9, 18, 120], 12)
Q(T, "Mixed approximation", I, APPROX + "1/? of 3599.6 ≈ 14.98% of 1999.8",
  "12", ["9", "18", "120"],
  "'1/? of N' means N ÷ ?; find the right side first",
  "15% of 2000 = 300. So 3600 ÷ ? = 300 and ? = 12.",
  ["15% of 2000 = 300", "3600 ÷ ? = 300", "? = 12"],
  why="9 uses 20% (3600 ÷ 400); 18 uses 10% (3600 ÷ 200); 120 uses 1.5% (3600 ÷ 30).", secs=45)

exact = 189.04 / 0.3497 + 120.3
nearest(exact, [660, 420, 540, 750], 660)
assert F(189, 1) / F(35, 100) == 540 and F(189) / F(30, 100) + 120 == 750
Q(T, "Percentage approximation", I, APPROX + "34.97% of (? − 120.3) ≈ 189.04",
  "660", ["420", "540", "750"],
  "Divide by the percentage to find the bracket, then undo the subtraction",
  "35% of (? − 120) = 189, so ? − 120 = 189 ÷ 0.35 = 540 and ? = 540 + 120 = 660.",
  ["189 ÷ 0.35 = 540", "? − 120 = 540", "? = 660"],
  why="420 subtracts 120 instead of adding it; 540 is the value of the bracket, not of ?; 750 uses 30% instead of 35% "
      "(630 + 120).", secs=55)

exact = 624.9 ** 0.25 * 511.8 ** (1 / 3) + 1 / 0.2498
nearest(exact, [44, 40.25, 204, 36], 44)
Q(T, "Root approximation", I, APPROX + "∜624.9 × ∛511.8 + 1/0.2498 ≈ ?",
  "44", ["40.25", "204", "36"],
  "Use 625 = 5⁴ and 512 = 8³; the reciprocal of 0.25 is 4",
  "∜624.9 ≈ 5, ∛511.8 ≈ 8 and 1/0.2498 ≈ 1/0.25 = 4. So the value ≈ 5 × 8 + 4 = 44.",
  ["∜625 = 5", "∛512 = 8", "1/0.25 = 4", "40 + 4 = 44"],
  why="40.25 adds 0.25 instead of its reciprocal; 204 takes the fourth root of 625 as its square root (25 × 8 + 4); 36 "
      "subtracts the 4.", secs=50)

exact = (math.sqrt(2304.2) * 6.01 + 0.4002 * 819.6 - 16.98 ** 2) / 3.01
nearest(exact, [109, 205, 194, 119], 109)
assert (48 * 6 + 328 - 289) / 3 == 109 and math.floor((48 * 6 + 328) / 3) == 205 and (288 + 328 - 34) / 3 == 194
Q(T, "Mixed approximation", A, APPROX + "? × 3.01 ≈ √2304.2 × 6.01 + 40.02% of 819.6 − 16.98²",
  "109", ["205", "194", "119"],
  "Round every term to a convenient value; finish the right side before dividing by the multiplier of ?",
  "√2304 = 48, so 48 × 6 = 288. 40% of 820 = 328. 17² = 289. Right side ≈ 288 + 328 − 289 = 327, so ? ≈ 327 ÷ 3 = 109.",
  ["√2304 = 48 ⇒ 48 × 6 = 288", "40% of 820 = 328", "17² = 289", "288 + 328 − 289 = 327", "? = 327 ÷ 3 = 109"],
  why="205 forgets to subtract 17²; 194 takes 17² as 34; 119 is 10 away from the exact value (about 109.0).",
  secs=90)

exact = ((0.1499 * 180.2) * 2.998 - 12.01) ** 2
nearest(exact, [4761, 6561, 69, 4225], 4761)
assert (27 * 3 - 12) ** 2 == 4761 and (27 * 3) ** 2 == 6561
Q(T, "Root approximation", A, APPROX + "(√? + 12.01) ÷ 2.998 ≈ 14.99% of 180.2",
  "4761", ["6561", "69", "4225"],
  "Work backwards: undo the division, then the addition, then the square root",
  "15% of 180 = 27. So √? + 12 = 27 × 3 = 81, √? = 69 and ? = 69² = 4761.",
  ["15% of 180 = 27", "√? + 12 = 81", "√? = 69", "? = 69² = 4761"],
  why="6561 = 81² forgets to subtract 12; 69 is √?, not ?; 4225 = 65² is far from the exact value (about 4,757).",
  secs=90)

exact = math.sqrt(144.02 * 100)
nearest(exact, [120, 12, 1200, 72], 120)
Q(T, "Percentage approximation", A, APPROX + "?% of ? ≈ 144.02",
  "120", ["12", "1200", "72"],
  "?% of ? = ? × ?/100 = ?²/100",
  "?² ÷ 100 ≈ 144, so ?² ≈ 14,400 and ? ≈ 120.",
  ["?% of ? = ?²/100", "?² ≈ 14,400", "? ≈ 120"],
  why="12 solves ?² = 144 and forgets the ÷ 100; 1200 multiplies by 100 twice; 72 halves 144 as if ?% of ? were 2 × ?.",
  secs=60)

exact = (31.96 / 3.99 * 5.99) / (0.1202 * 0.2498)
nearest(exact, [1600, 160, 3200, 1920], 1600)
assert F(48) / (F(12, 100) * F(25, 100)) == 1600 and F(48) / F(15, 1000) == 3200 and F(48) / (F(10, 100) * F(25, 100)) == 1920
Q(T, "Percentage approximation", A, APPROX + "12.02% of 24.98% of ? ≈ 31.96 ÷ 3.99 × 5.99",
  "1600", ["160", "3200", "1920"],
  "A percentage of a percentage is the product of the two decimals: 12% of 25% = 3%",
  "Right side ≈ 32 ÷ 4 × 6 = 48. 12% of 25% = 0.12 × 0.25 = 0.03, so 0.03 × ? = 48 and ? = 1600.",
  ["32 ÷ 4 × 6 = 48", "12% × 25% = 3%", "? = 48 ÷ 0.03 = 1600"],
  why="160 slips a decimal place; 3200 takes 12% of 25% as 1.5%; 1920 takes 12.02% as 10% (48 ÷ 0.025).", secs=80)

# ================================================================ Number Series (B6 I3 A3)
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


s = series_from(200, lambda t, k: t - (7 - k) ** 2, 6)
assert s == [200, 164, 139, 123, 114, 110]
Q(T, "Pattern: squares and cubes", B, SERIES_Q + "200, 164, 139, 123, 114, ?",
  "110", ["113", "105", "98"],
  "The falls are the perfect squares 6², 5², 4², 3², … in decreasing order",
  "200 − 36 = 164, 164 − 25 = 139, 139 − 16 = 123, 123 − 9 = 114. The next fall is 2² = 4, so the term is 110.",
  ["Falls: 36, 25, 16, 9", "= 6², 5², 4², 3²", "Next fall = 2² = 4", "114 − 4 = 110"],
  why="113 subtracts 1², skipping 2²; 105 subtracts 9 again; 98 subtracts 16 (4²) again.", secs=35)

def digit_sum(n):
    return sum(int(c) for c in str(n))


s = series_from(13, lambda t, k: t + digit_sum(t), 7)
assert s == [13, 17, 25, 32, 37, 47, 58]
Q(T, "Pattern: differences", B, SERIES_Q + "13, 17, 25, 32, 37, 47, ?",
  "58", ["57", "59", "52"],
  "Each term = previous term + the sum of its digits",
  "13 + (1 + 3) = 17, 17 + 8 = 25, 25 + 7 = 32, 32 + 5 = 37, 37 + 10 = 47, so the next term is 47 + (4 + 7) = 58.",
  ["13 + 4 = 17", "17 + 8 = 25", "25 + 7 = 32", "32 + 5 = 37", "37 + 10 = 47", "47 + 11 = 58"],
  why="57 adds 10 again; 59 adds 12; 52 adds 5, repeating an earlier jump. Only the digit-sum rule fits every step.",
  secs=45)

s = [n * (n + 1) for n in range(1, 7)]
assert s == [2, 6, 12, 20, 30, 42]
Q(T, "Missing number series", B, MISSING_Q + "2, 6, 12, 20, ?, 42",
  "30", ["28", "32", "36"],
  "Each term is n(n + 1): 1 × 2, 2 × 3, 3 × 4, …",
  "2 = 1 × 2, 6 = 2 × 3, 12 = 3 × 4, 20 = 4 × 5 and 42 = 6 × 7, so the missing term is 5 × 6 = 30.",
  ["1 × 2 = 2, 2 × 3 = 6, 3 × 4 = 12, 4 × 5 = 20", "5 × 6 = 30", "6 × 7 = 42 confirms"],
  short="The differences 4, 6, 8, 10, 12 rise by 2: 20 + 10 = 30.",
  why="28 adds 8 again; 32 adds 12, skipping 10; 36 = 6² does not lead to 42 by the rule.", secs=35)

s = series_from(F(96), lambda t, k: t / 2 + 8, 6)
assert s == [96, 56, 36, 26, 21, F(37, 2)]
Q(T, "Missing number series", B, MISSING_Q + "96, 56, ?, 26, 21, 18.5",
  "36", ["28", "41", "31"],
  "Each term = previous ÷ 2 + 8",
  "96 ÷ 2 + 8 = 56, 56 ÷ 2 + 8 = 36, 36 ÷ 2 + 8 = 26, 26 ÷ 2 + 8 = 21 and 21 ÷ 2 + 8 = 18.5.",
  ["96 ÷ 2 + 8 = 56", "56 ÷ 2 + 8 = 36", "36 ÷ 2 + 8 = 26", "26 ÷ 2 + 8 = 21", "21 ÷ 2 + 8 = 18.5"],
  why="28 only halves 56 and forgets the + 8; 41 assumes equal steps from 56 to 26; 31 extends the last fall of 5 "
      "backwards to 26 + 5.", secs=45)

s = series_from(F(8), lambda t, k: t * F(5, 2), 5)
assert s == [8, 20, 50, 125, F(625, 2)]
Q(T, "Pattern: multiply-add", B, SERIES_Q + "8, 20, 50, 125, ?",
  "312.5", ["250", "375", "437.5"],
  "Each term = previous × 2.5",
  "8 × 2.5 = 20, 20 × 2.5 = 50, 50 × 2.5 = 125, so the next term is 125 × 2.5 = 312.5.",
  ["8 × 2.5 = 20", "20 × 2.5 = 50", "50 × 2.5 = 125", "125 × 2.5 = 312.5"],
  why="250 multiplies by 2; 375 multiplies by 3; 437.5 multiplies by 3.5.", secs=35)

s = series_from(6, lambda t, k: 2 * t + 3, 6)
assert s == [6, 15, 33, 69, 141, 285]
Q(T, "Pattern: multiply-add", B, SERIES_Q + "6, 15, 33, 69, 141, ?",
  "285", ["282", "288", "213"],
  "Each term = previous × 2 + 3",
  "6 × 2 + 3 = 15, 15 × 2 + 3 = 33, 33 × 2 + 3 = 69, 69 × 2 + 3 = 141, so the next is 141 × 2 + 3 = 285.",
  ["6 × 2 + 3 = 15", "15 × 2 + 3 = 33", "33 × 2 + 3 = 69", "69 × 2 + 3 = 141", "141 × 2 + 3 = 285"],
  short="The differences 9, 18, 36, 72 double: next difference 144, and 141 + 144 = 285.",
  why="282 doubles and forgets the + 3; 288 adds 6 instead of 3; 213 adds 72 again.", secs=40)

s = [n * (2 * n + 1) for n in range(1, 7)]
assert s == [3, 10, 21, 36, 55, 78]
Q(T, "Pattern: squares and cubes", I, SERIES_Q + "3, 10, 21, 36, 55, ?",
  "78", ["76", "74", "81"],
  "Each term is n(2n + 1) = 2n² + n; the differences 7, 11, 15, 19 rise by 4",
  "3 = 1 × 3, 10 = 2 × 5, 21 = 3 × 7, 36 = 4 × 9, 55 = 5 × 11, so the next is 6 × 13 = 78. (Differences 7, 11, 15, 19, "
  "next 23.)",
  ["1 × 3, 2 × 5, 3 × 7, 4 × 9, 5 × 11", "6 × 13 = 78", "Check: 55 + 23 = 78"],
  why="76 adds 21, raising the difference by 2 instead of 4; 74 adds 19 again; 81 = 9² does not fit n(2n + 1).",
  secs=50)

s = list(itertools.accumulate([5] + [k * k + 1 for k in range(1, 7)]))
assert s == [5, 7, 12, 22, 39, 65, 102]
Q(T, "Pattern: differences", I, SERIES_Q + "5, 7, 12, 22, 39, 65, ?",
  "102", ["101", "91", "100"],
  "The differences are n² + 1: 2, 5, 10, 17, 26, …",
  "The differences are 2, 5, 10, 17, 26 = 1² + 1, 2² + 1, 3² + 1, 4² + 1, 5² + 1. The next is 6² + 1 = 37, so the term "
  "is 65 + 37 = 102.",
  ["Differences: 2, 5, 10, 17, 26", "= n² + 1", "Next = 37", "65 + 37 = 102"],
  why="101 adds 36 and forgets the + 1; 91 adds 26 again; 100 adds 35, repeating the last rise of 9 in the "
      "differences instead of 11.", secs=55)

s = [1, 2]
for m in (4, 6, 8, 10):
    s.append(s[-1] * m)
assert s == [1, 2, 8, 48, 384, 3840]
Q(T, "Pattern: multiply-add", I, SERIES_Q + "1, 2, 8, 48, 384, ?",
  "3,840", ["3,456", "4,608", "3,072"],
  "The multipliers are the even numbers 2, 4, 6, 8, …",
  "1 × 2 = 2, 2 × 4 = 8, 8 × 6 = 48, 48 × 8 = 384, so the next term is 384 × 10 = 3,840.",
  ["× 2, × 4, × 6, × 8", "Next multiplier = 10", "384 × 10 = 3,840"],
  why="3,456 multiplies by 9; 4,608 multiplies by 12; 3,072 multiplies by 8 again.", secs=50)

d1 = [2]
for p in (2, 3, 5, 7, 11):
    d1.append(d1[-1] + p)
s = list(itertools.accumulate([4] + d1))
assert d1 == [2, 4, 7, 12, 19, 30] and s == [4, 6, 10, 17, 29, 48, 78]
Q(T, "Pattern: differences", A, SERIES_Q + "4, 6, 10, 17, 29, 48, ?",
  "78", ["76", "74", "80"],
  "Take differences twice: the second differences are the prime numbers 2, 3, 5, 7, …",
  "First differences: 2, 4, 7, 12, 19. Second differences: 2, 3, 5, 7 — consecutive primes. The next second "
  "difference is 11, so the next first difference is 19 + 11 = 30 and the term is 48 + 30 = 78.",
  ["First differences: 2, 4, 7, 12, 19", "Second differences: 2, 3, 5, 7 (primes)", "Next prime 11 ⇒ difference 30",
   "48 + 30 = 78"],
  why="76 takes the second differences as odd numbers (next 9); 74 repeats the second difference 7; 80 skips 11 and "
      "uses 13.", secs=80)

s = [(n * (n + 1) // 2) ** 2 for n in range(1, 7)]
assert s == [1, 9, 36, 100, 225, 441] and s == list(itertools.accumulate(k ** 3 for k in range(1, 7)))
Q(T, "Pattern: squares and cubes", A, SERIES_Q + "1, 9, 36, 100, 225, ?",
  "441", ["361", "450", "400"],
  "Each term is the sum of the first n cubes, which equals the square of the n-th triangular number",
  "The differences are 8, 27, 64, 125 = 2³, 3³, 4³, 5³, so the next term is 225 + 6³ = 441. Equivalently the terms are "
  "1², 3², 6², 10², 15², and the next triangular number is 21, giving 21² = 441.",
  ["Differences: 2³, 3³, 4³, 5³", "225 + 216 = 441", "Check: 1, 3, 6, 10, 15, 21 squared"],
  why="361 = 19² continues the square roots 10, 15 by + 4; 450 doubles 225; 400 = 20² continues the roots by + 5 "
      "again.", secs=75)

s = [1, 2]
while len(s) < 7:
    s.append(2 * s[-1] + s[-2])
assert s == [1, 2, 5, 12, 29, 70, 169] and 2 * 36 + 12 != 70 and 2 * 25 + 12 != 70
Q(T, "Missing number series", A, MISSING_Q + "1, 2, 5, 12, ?, 70, 169",
  "29", ["24", "36", "25"],
  "Each term = 2 × previous term + the term before that",
  "2 × 2 + 1 = 5, 2 × 5 + 2 = 12, 2 × 12 + 5 = 29, 2 × 29 + 12 = 70 and 2 × 70 + 29 = 169.",
  ["2 × 2 + 1 = 5", "2 × 5 + 2 = 12", "2 × 12 + 5 = 29", "2 × 29 + 12 = 70", "2 × 70 + 29 = 169"],
  why="24 only doubles 12; 36 triples 12; 25 adds 1 to 2 × 12. None of them gives 70 at the next step "
      "(2 × 24 + 12 = 60, 2 × 36 + 12 = 84, 2 × 25 + 12 = 62).", secs=80)

# ================================================================ Wrong Number Series (B2 I3 A2)
T = "Wrong Number Series"


def wrong_series(correct, shown):
    diff = [i for i, (a, b) in enumerate(zip(correct, shown)) if a != b]
    assert len(diff) == 1, (correct, shown)
    return shown[diff[0]], correct[diff[0]]


def series_text(seq):
    return ", ".join(N(x) for x in seq)


WRONG_Q = "Find the wrong number in the series:\n"
good = series_from(100, lambda t, k: t - 5 * k, 7)
shown = [100, 95, 85, 70, 50, 26, -5]
assert good == [100, 95, 85, 70, 50, 25, -5] and wrong_series(good, shown) == (26, 25)
Q(T, "Find the wrong term", B, WRONG_Q + series_text(shown),
  "26", ["85", "50", "−5"],
  "The falls are multiples of 5: 5, 10, 15, 20, 25, 30",
  "100 − 5 = 95, 95 − 10 = 85, 85 − 15 = 70, 70 − 20 = 50, 50 − 25 = 25, 25 − 30 = −5. The sixth term should be 25, "
  "not 26.",
  ["−5, −10, −15, −20 fit", "50 − 25 = 25 ≠ 26", "25 − 30 = −5 fits"],
  why="85, 50 and −5 all fit the rule; −5 looks wrong only if 26 is taken as correct (26 − 30 = −4).", secs=35)

good = [11 * n * (n + 1) // 2 for n in range(1, 7)]
shown = [11, 33, 66, 110, 166, 231]
assert good == [11, 33, 66, 110, 165, 231] and wrong_series(good, shown) == (166, 165)
Q(T, "Find the wrong term", B, WRONG_Q + series_text(shown),
  "166", ["66", "110", "231"],
  "The differences are 22, 33, 44, 55, 66: multiples of 11 (the terms are 11 × 1, 11 × 3, 11 × 6, …)",
  "11 + 22 = 33, 33 + 33 = 66, 66 + 44 = 110, 110 + 55 = 165, 165 + 66 = 231. The fifth term should be 165, not 166.",
  ["+22, +33, +44 fit", "110 + 55 = 165 ≠ 166", "165 + 66 = 231 fits"],
  short="Every correct term is a multiple of 11; 166 is not.",
  why="66, 110 and 231 are 11 × 6, 11 × 10 and 11 × 21 and fit the pattern.", secs=35)

odd_ = series_from(5, lambda t, k: 2 * t, 4)
even_ = series_from(40, lambda t, k: t - 6, 4)
good = [x for pair in zip(odd_, even_) for x in pair]
shown = [5, 40, 10, 34, 20, 28, 41, 22]
assert good == [5, 40, 10, 34, 20, 28, 40, 22] and wrong_series(good, shown) == (41, 40)
Q(T, "Find the wrong term", I, WRONG_Q + series_text(shown),
  "41", ["34", "20", "22"],
  "Two series alternate: odd positions double (5, 10, 20, …) and even positions fall by 6 (40, 34, 28, …)",
  "Odd positions: 5, 10, 20, then 40 — but the series shows 41. Even positions: 40, 34, 28, 22 fall by 6 and fit. "
  "So 41 is wrong.",
  ["Odd positions: 5 → 10 → 20 → 40", "Shown 41 ≠ 40", "Even positions: 40 → 34 → 28 → 22"],
  why="34, 20 and 22 belong to the two interleaved series and fit their rules.", secs=50)

good = list(itertools.accumulate([F(2)] + [1 + F(3, 2) * k for k in range(6)]))
shown = [F(2), F(3), F(11, 2), F(19, 2), F(31, 2), F(22), F(61, 2)]
assert good == [2, 3, F(11, 2), F(19, 2), 15, 22, F(61, 2)] and wrong_series(good, shown) == (F(31, 2), 15)
Q(T, "Find the wrong term", I, WRONG_Q + series_text(shown),
  "15.5", ["5.5", "22", "30.5"],
  "The differences rise by 1.5 each time: 1, 2.5, 4, 5.5, 7, 8.5",
  "2 + 1 = 3, 3 + 2.5 = 5.5, 5.5 + 4 = 9.5, 9.5 + 5.5 = 15, 15 + 7 = 22, 22 + 8.5 = 30.5. The fifth term should be "
  "15, not 15.5.",
  ["+1, +2.5, +4 fit", "9.5 + 5.5 = 15 ≠ 15.5", "15 + 7 = 22", "22 + 8.5 = 30.5"],
  why="5.5, 22 and 30.5 fit once 15.5 is corrected to 15; 22 looks off only if 15.5 is taken as correct.", secs=55)

good = [3]
for k in range(6):
    good.append(good[-1] * (2 if k % 2 == 0 else 3))
shown = [3, 6, 18, 36, 106, 216, 648]
assert good == [3, 6, 18, 36, 108, 216, 648] and wrong_series(good, shown) == (106, 108)
Q(T, "Find the wrong term", I, WRONG_Q + series_text(shown),
  "106", ["18", "216", "648"],
  "The multipliers alternate: × 2, × 3, × 2, × 3, …",
  "3 × 2 = 6, 6 × 3 = 18, 18 × 2 = 36, 36 × 3 = 108, 108 × 2 = 216, 216 × 3 = 648. The fifth term should be 108.",
  ["3 × 2 = 6", "6 × 3 = 18", "18 × 2 = 36", "36 × 3 = 108 ≠ 106", "108 × 2 = 216", "216 × 3 = 648"],
  why="18, 216 and 648 fit the alternating rule; 216 only looks wrong if 106 is taken as correct.", secs=45)

good = [1, 3]
while len(good) < 7:
    good.append(good[-1] + 2 * good[-2])
shown = [1, 3, 5, 11, 21, 42, 85]
assert good == [1, 3, 5, 11, 21, 43, 85] and wrong_series(good, shown) == (42, 43)
assert [2 * t + (1 if i % 2 == 0 else -1) for i, t in enumerate(good[:-1])] == good[1:]
Q(T, "Find the wrong term", A, WRONG_Q + series_text(shown),
  "42", ["11", "21", "85"],
  "Each term = previous term + 2 × the term before it (equivalently × 2 + 1 and × 2 − 1 alternately)",
  "3 + 2 × 1 = 5, 5 + 2 × 3 = 11, 11 + 2 × 5 = 21, 21 + 2 × 11 = 43, 43 + 2 × 21 = 85. The sixth term should be 43.",
  ["3 + 2 = 5", "5 + 6 = 11", "11 + 10 = 21", "21 + 22 = 43 ≠ 42", "43 + 42 = 85"],
  short="× 2 + 1, × 2 − 1 alternately: 1 → 3 → 5 → 11 → 21 → 43 → 85.",
  why="11, 21 and 85 fit; 85 confirms 43, since 42 × 2 + 1 = 85 would need the rule to change.", secs=80)

good = [x for k in range(1, 5) for x in (k ** 3, (k + 1) ** 2)]
shown = [1, 4, 8, 9, 26, 16, 64, 25]
assert good == [1, 4, 8, 9, 27, 16, 64, 25] and wrong_series(good, shown) == (26, 27)
Q(T, "Find the wrong term", A, WRONG_Q + series_text(shown),
  "26", ["9", "16", "64"],
  "Two series alternate: odd positions are cubes (1³, 2³, 3³, 4³) and even positions are squares (2², 3², 4², 5²)",
  "Odd positions: 1, 8, ?, 64 = 1³, 2³, …, 4³, so the fifth term should be 3³ = 27, not 26. Even positions: 4, 9, 16, "
  "25 = 2², 3², 4², 5² fit.",
  ["Odd positions: 1³, 2³, 3³ = 27 (shown 26), 4³", "Even positions: 2², 3², 4², 5²"],
  why="9, 16 and 64 are 3², 4² and 4³ and fit their series.", secs=70)

# ================================================================ Quadratic Equations (B2 I3 A6)
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


xs, ys = [F(-6), F(-7)], [F(-8), F(-9)]
roots_check(1, 13, 42, xs), roots_check(1, 17, 72, ys)
qe("Relation between roots", B, "Both quadratics below have only negative roots. Find them and state how x compares with y.",
   "x² + 13x + 42 = 0", "y² + 17y + 72 = 0", xs, ys, ">", ["<", "<="],
   "When all coefficients are positive, both roots are negative; compare the smallest x with the largest y",
   "x = −6 or −7 and y = −8 or −9. The smallest x (−7) is greater than the largest y (−8), so x > y.",
   ["I: (x + 6)(x + 7) = 0 ⇒ x = −6, −7", "II: (y + 8)(y + 9) = 0 ⇒ y = −8, −9", "min x = −7 > max y = −8",
    "So x > y"],
   why="x < y and x ≤ y come from dropping the minus signs (6 and 7 are smaller than 8 and 9).", secs=40)

xs, ys = [F(7), F(-3)], [F(3), F(5)]
roots_check(1, -4, -21, xs), roots_check(1, -8, 15, ys)
qe("Relation between roots", B, "Find the roots of the two equations and choose the relation between x and y, if any.",
   "x² − 4x − 21 = 0", "y² − 8y + 15 = 0", xs, ys, "cbe", [">", "<="],
   "If one x lies above both y values and the other below them, no relation holds for every pair",
   "x = 7 or −3 and y = 3 or 5. x = 7 is greater than both y values but x = −3 is less than both, so the relationship "
   "cannot be established.",
   ["I: (x − 7)(x + 3) = 0 ⇒ x = 7, −3", "II: (y − 3)(y − 5) = 0 ⇒ y = 3, 5", "7 > 5 but −3 < 3",
    "Cannot be established"],
   why="x > y uses only x = 7; x ≤ y and x < y use only x = −3 (or read the root −3 as 3).", secs=45)

xs, ys = [F(5, 2), F(-5, 2)], [F(-7, 2), F(-3)]
roots_check(4, 0, -25, xs), roots_check(2, 13, 21, ys)
qe("Relation between roots", I, "Equation I has no x-term. Find all roots of I and II and pick the relation between x and y that holds for every pair.",
   "4x² − 25 = 0", "2y² + 13y + 21 = 0", xs, ys, ">", ["<", "<="],
   "x² = k gives two roots ±√k; do not drop the negative one",
   "I: x² = 25/4, so x = ±2.5. II: (2y + 7)(y + 3) = 0, so y = −3.5 or −3. Even the smaller x (−2.5) is greater than the "
   "larger y (−3), so x > y.",
   ["I: x² = 25/4 ⇒ x = 2.5, −2.5", "II: 2y² + 6y + 7y + 21 = (y + 3)(2y + 7) = 0 ⇒ y = −3, −3.5",
    "min x = −2.5 > max y = −3", "So x > y"],
   why="x < y and x ≤ y come from reading the roots of II as +3 and +3.5.", secs=60)

xs, ys = [F(2), F(-4, 3)], [F(8, 3), F(3)]
roots_check(3, -2, -8, xs), roots_check(3, -17, 24, ys)
qe("Relation between roots", I, "Solve the two equations and mark the relation between x and y.",
   "3x² − 2x − 8 = 0", "3y² − 17y + 24 = 0", xs, ys, "<", [">", ">="],
   "Split the middle term; then compare the largest x with the smallest y",
   "I: (3x + 4)(x − 2) = 0, so x = 2 or −4/3. II: (3y − 8)(y − 3) = 0, so y = 8/3 or 3. The largest x (2) is below the "
   "smallest y (2.67), so x < y.",
   ["I: 3x² − 6x + 4x − 8 = (x − 2)(3x + 4) = 0 ⇒ x = 2, −4/3",
    "II: 3y² − 9y − 8y + 24 = (y − 3)(3y − 8) = 0 ⇒ y = 3, 8/3", "max x = 2 < min y = 8/3", "So x < y"],
   why="x > y and x ≥ y come from a sign slip in II that gives y = −8/3 and −3.", secs=65)

xs = [F(12)]
assert xs[0] / 4 + xs[0] / 6 == 5
ys = [F(9), F(12)]
roots_check(1, -21, 108, ys)
qe("Linear vs quadratic", I, "One equation is linear and the other quadratic. Solve both and choose the relation between x and y.",
   "x/4 + x/6 = 5", "y² − 21y + 108 = 0", xs, ys, ">=", [">", "<"],
   "Solve the linear equation exactly; a common value makes the relation non-strict",
   "I: x/4 + x/6 = 5x/12 = 5, so x = 12. II: (y − 9)(y − 12) = 0, so y = 9 or 12. x = y when y = 12 and x > y when "
   "y = 9, so x ≥ y.",
   ["I: 5x/12 = 5 ⇒ x = 12", "II: (y − 9)(y − 12) = 0 ⇒ y = 9, 12", "12 > 9 and 12 = 12", "So x ≥ y"],
   why="x > y misses y = 12; x < y comes from forgetting to multiply the 5 by 12 when clearing the fractions "
       "(3x + 2x = 5 ⇒ x = 1).", secs=55)

xs = [F(-3), F(4)]
for r in xs:
    assert r * (r + 3) == 4 * (r + 3)
ys = [F(1), F(-3)]
roots_check(1, 2, -3, ys)
assert relation([F(4)], ys) == ">"
qe("Relation between roots", A, "Solve both equations (do not cancel a common factor that could be zero) and choose the relation between x and y.",
   "x(x + 3) = 4(x + 3)", "y² + 2y − 3 = 0", xs, ys, "cbe", [">", ">="],
   "Move everything to one side and factorise; dividing by (x + 3) would lose the root x = −3",
   "I: x(x + 3) − 4(x + 3) = (x + 3)(x − 4) = 0, so x = −3 or 4. II: (y + 3)(y − 1) = 0, so y = −3 or 1. x = 4 is "
   "greater than both y values, but x = −3 is less than y = 1. So the relationship cannot be established.",
   ["I: (x + 3)(x − 4) = 0 ⇒ x = −3, 4", "II: (y + 3)(y − 1) = 0 ⇒ y = −3, 1", "x = 4 > 1 but x = −3 < 1",
    "Cannot be established"],
   why="x > y and x ≥ y come from cancelling (x + 3), which leaves only x = 4; x < y uses only x = −3.", secs=90)

xs, ys = [F(3, 4), F(-4, 3)], [F(3, 4), F(4, 5)]
roots_check(12, 7, -12, xs), roots_check(20, -31, 12, ys)
qe("Relation between roots", A, "Solve both equations and choose the relation between x and y that holds for all their roots.",
   "12x² + 7x − 12 = 0", "20y² − 31y + 12 = 0", xs, ys, "<=", ["<", ">="],
   "Use the quadratic formula when splitting the middle term is slow; watch for a root common to both equations",
   "I: discriminant = 49 + 576 = 625, so x = (−7 ± 25)/24 = 3/4 or −4/3. II: discriminant = 961 − 960 = 1, so "
   "y = (31 ± 1)/40 = 4/5 or 3/4. x = y = 3/4 is possible and every other pair has x < y, so x ≤ y.",
   ["I: x = (−7 ± 25)/24 ⇒ 3/4, −4/3", "II: y = (31 ± 1)/40 ⇒ 4/5, 3/4", "x = y = 3/4 possible",
    "All other pairs x < y ⇒ x ≤ y"],
   why="x < y misses the common root 3/4; x ≥ y holds only for the pair x = y = 3/4.", secs=100)

xk, yk = [4, -1], [-2, -3]  # roots are k√2
for k in xk:
    assert 2 * k * k - 6 * k - 8 == 0  # (k√2)² − 3√2(k√2) − 8
for k in yk:
    assert 2 * k * k + 10 * k + 12 == 0  # (k√2)² + 5√2(k√2) + 12
xs, ys = [F(k) for k in xk], [F(k) for k in yk]  # √2 > 0, so comparing k compares the roots
qe("Relation between roots", A, "The equations below have irrational coefficients (√2 ≈ 1.414). Solve them and choose the relation between x and y.",
   "x² − 3√2x − 8 = 0", "y² + 5√2y + 12 = 0", xs, ys, ">", ["<", "<="],
   "Quadratic formula with surds: write the discriminant as a multiple of 2 so that its root is a multiple of √2",
   "I: discriminant = 18 + 32 = 50, √50 = 5√2, so x = (3√2 ± 5√2)/2 = 4√2 or −√2. II: discriminant = 50 − 48 = 2, so "
   "y = (−5√2 ± √2)/2 = −2√2 or −3√2. The smallest x (−√2 ≈ −1.41) is greater than the largest y (−2√2 ≈ −2.83), so "
   "x > y.",
   ["I: x = (3√2 ± 5√2)/2 ⇒ 4√2, −√2", "II: y = (−5√2 ± √2)/2 ⇒ −2√2, −3√2", "−√2 > −2√2", "So x > y"],
   why="x < y and x ≤ y come from taking the roots of II with the wrong sign (2√2 and 3√2).", secs=100)

xs = [F(4), F(1)]
for r in xs:
    assert (r - 4) ** 2 + 3 * (r - 4) == 0
ys = [F(1), F(1, 2)]
for r in ys:
    assert 2 * r * (r - 1) == r - 1
qe("Relation between roots", A, "Solve both equations without cancelling any factor that could be zero, and choose the relation between x and y.",
   "(x − 4)² + 3(x − 4) = 0", "2y(y − 1) = y − 1", xs, ys, ">=", [">", "<"],
   "Take the common bracket out as a factor; each factor can be zero",
   "I: (x − 4)[(x − 4) + 3] = (x − 4)(x − 1) = 0, so x = 4 or 1. II: 2y(y − 1) − (y − 1) = (y − 1)(2y − 1) = 0, so y = 1 "
   "or 1/2. x = 1, y = 1 gives x = y; every other pair has x > y. So x ≥ y.",
   ["I: (x − 4)(x − 1) = 0 ⇒ x = 4, 1", "II: (y − 1)(2y − 1) = 0 ⇒ y = 1, 1/2", "x = y = 1 possible",
    "All other pairs x > y ⇒ x ≥ y"],
   why="x > y comes from cancelling (y − 1), which loses y = 1; x < y comes from writing the factors of I as "
       "(x + 4)(x + 1), which gives the negative roots −4 and −1.", secs=90)

xs = [F(1), F(9)]
for r in xs:
    assert r / 3 + 3 / r == F(10, 3)
ys = [F(12), F(13)]
roots_check(1, -25, 156, ys)
qe("Linear vs quadratic", A, "Solve both equations (x ≠ 0) and choose the relation between x and y.",
   "x/3 + 3/x = 10/3", "y² − 25y + 156 = 0", xs, ys, "<", [">", ">="],
   "Clear the fractions by multiplying by 3x to get a quadratic",
   "I: multiply by 3x: x² + 9 = 10x, so x² − 10x + 9 = 0 and x = 1 or 9. II: (y − 12)(y − 13) = 0, so y = 12 or 13. "
   "The largest x (9) is below the smallest y (12), so x < y.",
   ["I: x² − 10x + 9 = 0 ⇒ x = 1, 9", "II: y = 12, 13", "max x = 9 < min y = 12", "So x < y"],
   why="x > y and x ≥ y come from a sign slip in II that gives y = −12 and −13; with the correct roots every x is "
       "below every y.", secs=90)

xs = [F(5, 3)]
roots_check(9, -30, 25, xs)
ys = [F(5, 3), F(2)]
roots_check(3, -11, 10, ys)
qe("Relation between roots", A, "Solve both equations and choose the relation between x and y.",
   "9x² − 30x + 25 = 0", "3y² − 11y + 10 = 0", xs, ys, "<=", ["<", ">"],
   "A perfect-square quadratic has one repeated root",
   "I: 9x² − 30x + 25 = (3x − 5)² = 0, so x = 5/3 only. II: (3y − 5)(y − 2) = 0, so y = 5/3 or 2. x = y when "
   "y = 5/3 and x < y when y = 2, so x ≤ y.",
   ["I: (3x − 5)² = 0 ⇒ x = 5/3", "II: 3y² − 6y − 5y + 10 = (y − 2)(3y − 5) = 0 ⇒ y = 2, 5/3", "5/3 = 5/3 and 5/3 < 2",
    "So x ≤ y"],
   why="x < y misses the common value 5/3; x > y comes from taking the roots of II as 5/3 and 2/3.", secs=80)

# ================================================================ Number System (B1 I2 A2)
T = "Number System"
opts_ = {"7,632": 7632, "5,418": 5418, "8,724": 8724, "7,362": 7362}
ok_ = [k for k, n in opts_.items() if n % 4 == 0 and n % 9 == 0]
assert ok_ == ["7,632"] and 5418 % 9 == 0 and 8724 % 4 == 0 and 8724 % 9 and 7362 % 9 == 0 and 7362 % 4
Q(T, "Divisibility", B, "Which of the following numbers is divisible by both 4 and 9?",
  "7,632", ["5,418", "8,724", "7,362"],
  "Divisible by 4: the last two digits form a multiple of 4. Divisible by 9: the digit sum is a multiple of 9",
  "7,632: 32 is a multiple of 4 and 7 + 6 + 3 + 2 = 18 is a multiple of 9, so it is divisible by both (7,632 = 36 × "
  "212).",
  ["7,632: 32 ÷ 4 = 8 ✓; digit sum 18 ✓", "5,418: digit sum 18 ✓ but 18 is not a multiple of 4",
   "8,724: 24 ÷ 4 ✓ but digit sum 21 ✗", "7,362: digit sum 18 ✓ but 62 is not a multiple of 4"],
  why="5,418 and 7,362 pass the test for 9 but fail the test for 4 (7,362 has the same digits as 7,632 in another "
      "order); 8,724 passes the test for 4 but its digit sum, 21, is only a multiple of 3.", secs=40)

g = math.gcd(960, 720)
assert g == 240 and (960 // g) * (720 // g) == 12 and (960 // 120) * (720 // 120) == 48 and (960 // 80) * (720 // 80) == 108
Q(T, "HCF and LCM", I,
  "A hall floor measuring 9.6 m by 7.2 m is to be paved with identical square tiles, with no tile cut. What is the "
  "least number of tiles needed?",
  "12", ["48", "108", "240"],
  "The largest square tile that fits exactly has a side equal to the HCF of the two lengths",
  "In cm the floor is 960 × 720. HCF(960, 720) = 240, so the largest tile is 240 cm × 240 cm. Tiles needed = "
  "(960 ÷ 240) × (720 ÷ 240) = 4 × 3 = 12.",
  ["960 = 240 × 4, 720 = 240 × 3", "HCF = 240 cm", "Tiles = 4 × 3 = 12"],
  why="48 uses 120 cm tiles, a common factor but not the highest; 108 uses 80 cm tiles; 240 is the side of the tile in "
      "cm, not the number of tiles.", secs=60)

r_ = (pow(17, 23, 40) + pow(23, 23, 40)) % 40
assert r_ == 0 and pow(17, 23, 40) == 33 and pow(23, 23, 40) == 7 and (17 ** 23 + 23 ** 23) % 40 == 0
Q(T, "Remainders", I, "What is the remainder when 17²³ + 23²³ is divided by 40?",
  "0", ["33", "7", "2"],
  "For an odd power n, aⁿ + bⁿ is always divisible by a + b",
  "23 is odd, so 17²³ + 23²³ is divisible by 17 + 23 = 40. The remainder is 0.",
  ["aⁿ + bⁿ is divisible by a + b when n is odd", "17 + 23 = 40", "Remainder = 0"],
  short="Check: 17²³ leaves 33 and 23²³ leaves 7 on division by 40; 33 + 7 = 40.",
  why="33 is the remainder of 17²³ alone; 7 is the remainder of 23²³ alone; 2 treats both powers as leaving remainder "
      "1, a rule that holds only for suitable even powers.", secs=60)

nmb = 2 ** 4 * 3 ** 3 * 5 ** 2
divs = [d for d in range(1, nmb + 1) if nmb % d == 0]
sq = [d for d in divs if math.isqrt(d) ** 2 == d]
cu = [d for d in divs if round(d ** (1 / 3)) ** 3 == d]
assert len(divs) == 60 and len(sq) == 12 and len(cu) == 4
Q(T, "Divisibility", A, "How many factors of 2⁴ × 3³ × 5² are perfect squares?",
  "12", ["60", "4", "30"],
  "A factor is a perfect square when every prime in it has an even power",
  "A square factor is 2ᵃ × 3ᵇ × 5ᶜ with a, b and c even: a ∈ {0, 2, 4} (3 ways), b ∈ {0, 2} (2 ways), c ∈ {0, 2} "
  "(2 ways). So there are 3 × 2 × 2 = 12 such factors.",
  ["Powers of 2: 0, 2, 4 → 3 choices", "Powers of 3: 0, 2 → 2 choices", "Powers of 5: 0, 2 → 2 choices",
   "3 × 2 × 2 = 12"],
  why="60 counts all factors, (4 + 1)(3 + 1)(2 + 1); 4 counts the perfect-cube factors; 30 assumes half of all factors "
      "are squares.", secs=80, by=BRUTE)

nums = (1305, 4665, 6905)
best = max(d for d in range(1, 7000) if len({n % d for n in nums}) == 1)
assert best == 1120 and 1305 % 1120 == 185 and len({n % 560 for n in nums}) == 1 and len({n % 2240 for n in nums}) > 1
assert math.gcd(4665 - 1305, 6905 - 4665) == 1120
Q(T, "HCF and LCM", A,
  "What is the largest number that divides 1,305, 4,665 and 6,905 and leaves the same remainder in each case?",
  "1,120", ["560", "2,240", "185"],
  "If three numbers leave the same remainder on division by d, then d divides every difference; take the HCF of the "
  "differences",
  "Differences: 4,665 − 1,305 = 3,360, 6,905 − 4,665 = 2,240 and 6,905 − 1,305 = 5,600. HCF(3,360, 2,240, 5,600) = "
  "1,120. Check: each number leaves remainder 185 on division by 1,120.",
  ["3,360, 2,240, 5,600", "HCF(3,360, 2,240) = 1,120", "1,120 divides 5,600", "Remainder 185 each time"],
  why="560 also leaves equal remainders but is not the largest such number; 2,240 is one of the differences but does "
      "not divide 3,360; 185 is the common remainder, not the divisor.", secs=90, by=BRUTE)

# ================================================================ Percentage (B2 I2 A2)
T = "Percentage"
a_, b_ = F(45), F(30)  # 30% of A = 45% of B, e.g. A = 45k, B = 30k
assert a_ * F(30, 100) == b_ * F(45, 100) and b_ / a_ * 100 == F(200, 3)
Q(T, "Basic percentage", B, "If 30% of A equals 45% of B, then B is what percentage of A?",
  "66⅔%", ["150%", "33⅓%", "15%"],
  "Equal parts of A and B: 0.30A = 0.45B, so B/A = 30/45",
  "0.30A = 0.45B gives B/A = 0.30/0.45 = 2/3, so B is 66⅔% of A.",
  ["0.30A = 0.45B", "B/A = 30/45 = 2/3", "= 66⅔%"],
  why="150% is A as a percentage of B; 33⅓% is how much less B is than A; 15% is the difference between the two "
      "percentages.", secs=35)

v = 60000 * F(85, 100) * F(90, 100)
assert v == 45900 and 60000 * F(75, 100) == 45000 and 60000 * F(85, 100) == 51000 and 60000 * F(85, 100) ** 2 == 43350
Q(T, "Population and depreciation", B,
  "A laptop bought for ₹60,000 loses 15% of its value in the first year and, in the second year, 10% of its value "
  "at the start of that year. What is its value after 2 years?",
  "₹45,900", ["₹45,000", "₹51,000", "₹43,350"],
  "Successive depreciation multiplies the factors: (1 − 0.15)(1 − 0.10)",
  "After year 1: 60,000 × 0.85 = ₹51,000. After year 2: 51,000 × 0.90 = ₹45,900.",
  ["60,000 × 0.85 = 51,000", "51,000 × 0.90 = 45,900"],
  why="₹45,000 subtracts 25% of the original price at once; ₹51,000 stops after the first year; ₹43,350 applies 15% in "
      "both years.", secs=40)

x_, y_ = F(1), F(7500)  # x% of y = 75 ⇒ xy = 7,500
z_ = F(120 * 100) / y_
assert x_ * y_ / 100 == 75 and y_ * z_ / 100 == 120 and z_ / x_ * 100 == 160
Q(T, "Basic percentage", I,
  "For positive numbers x, y and z, x% of y is 75 and y% of z is 120. What percentage of x is z?",
  "160%", ["62.5%", "45%", "60%"],
  "Write both statements as products: xy/100 = 75 and yz/100 = 120; divide to cancel y",
  "x% of y = xy/100 = 75 and y% of z = yz/100 = 120. Dividing, z/x = 120/75 = 1.6, so z is 160% of x.",
  ["xy = 7,500", "yz = 12,000", "z/x = 12,000/7,500 = 1.6", "z = 160% of x"],
  why="62.5% is x as a percentage of z; 45% reads the difference 120 − 75 as a percentage; 60% is how much more z is "
      "than x, written as if it were the whole.", secs=60)

r_ = 1 - F(4, 5)
assert (1 - r_) ** 2 == F(160000, 250000) and r_ == F(1, 5)
assert F(90000, 250000) / 2 == F(18, 100) and F(90000, 250000) == F(36, 100)
Q(T, "Population and depreciation", I,
  "The value of a machine fell from ₹2,50,000 to ₹1,60,000 in 2 years. If it depreciated at the same rate each year "
  "(on its value at the start of that year), what was the annual rate of depreciation?",
  "20%", ["18%", "36%", "40%"],
  "Value after n years = original × (1 − r)ⁿ; take the n-th root of the ratio",
  "(1 − r)² = 1,60,000 ÷ 2,50,000 = 0.64, so 1 − r = 0.8 and r = 20%.",
  ["(1 − r)² = 160/250 = 0.64", "1 − r = 0.8", "r = 20%"],
  why="18% treats the fall as simple (36% ÷ 2); 36% is the total fall over 2 years; 40% takes the square root of 0.36 "
      "(the fall) instead of 0.64 (what remains).", secs=55)

inc0, sav0 = F(100), F(25)
inc1 = inc0 * F(120, 100)
sav1 = inc1 * F(20, 100)
e0, e1 = inc0 - sav0, inc1 - sav1
assert (e0, e1) == (75, 96) and (e1 - e0) / e0 * 100 == 28 and (sav0 - sav1) / sav0 * 100 == 4
Q(T, "Income and expenditure", A,
  "Ravi saves 25% of his income. His income rises by 20%, and he now saves 20% of the new income. By what percentage "
  "does his expenditure rise?",
  "28%", ["20%", "4%", "21%"],
  "Take the old income as 100 and work out both expenditures",
  "Old: income 100, savings 25, expenditure 75. New: income 120, savings 20% of 120 = 24, expenditure 96. Expenditure "
  "rises by 21 on 75, i.e. 28%.",
  ["Old expenditure = 75", "New income = 120, savings = 24", "New expenditure = 96", "21 ÷ 75 = 28%"],
  why="20% assumes expenditure rises with income; 4% is the fall in savings (25 → 24); 21% reads the rise of 21 on an "
      "income of 100 as a percentage of expenditure.", secs=80)

p_ = F(30)
assert 600 / (p_ * F(4, 5)) - 600 / p_ == 5 and F(600 * 20, 100) / 5 == 24 and 24 * F(12, 10) == F(288, 10)
pp = [p for p in range(21, 200) if F(600, p - 20) - F(600, p) == 5]
assert pp == [60]
Q(T, "Basic percentage", A,
  "A 20% fall in the price of sugar lets a household buy 5 kg more sugar for ₹600. What was the original price per "
  "kg?",
  "₹30", ["₹24", "₹28.80", "₹60"],
  "The money saved on the old quantity buys the extra quantity at the new price",
  "A 20% fall saves 20% of ₹600 = ₹120, and this buys the extra 5 kg, so the new price is 120 ÷ 5 = ₹24 per kg. The "
  "original price was 24 ÷ 0.8 = ₹30 per kg.",
  ["Saving = 20% of 600 = 120", "New price = 120 ÷ 5 = ₹24", "Original = 24 ÷ 0.8 = ₹30",
   "Check: 600 ÷ 30 = 20 kg, 600 ÷ 24 = 25 kg"],
  why="₹24 is the new price; ₹28.80 adds 20% to ₹24 instead of dividing by 0.8; ₹60 reads the 20% fall as a ₹20 fall "
      "per kg.", secs=80)

# ================================================================ Ratio and Proportion (B2 I2 A1)
T = "Ratio and Proportion"
k_ = F(45, 8 - 5)
assert k_ == 15 and 13 * k_ == 195 and 8 * k_ == 120 and 5 * k_ == 75 and 13 * 45 == 585
Q(T, "Basic ratio", B, "Two numbers are in the ratio 5 : 8 and their difference is 45. What is their sum?",
  "195", ["120", "75", "585"],
  "The difference corresponds to 8 − 5 = 3 parts",
  "3 parts = 45, so 1 part = 15. The numbers are 75 and 120, and their sum is 13 parts = 195.",
  ["8 − 5 = 3 parts = 45", "1 part = 15", "Sum = 13 × 15 = 195"],
  why="120 is the larger number; 75 is the smaller number; 585 multiplies 45 by 13 without first dividing by 3.",
  secs=35)

sol = [x for x in range(-50, 51) if x + 11 != 0 and x + 2 != 0 and F(x + 3, x + 11) == F(x - 2, x + 2)]
assert sol == [7] and F(-7, 3) * -12 == 28
Q(T, "Proportion", B, "If (x + 3) : (x + 11) = (x − 2) : (x + 2), what is the value of x?",
  "7", ["−7/3", "5.5", "28"],
  "In a proportion a : b = c : d, the product of the extremes equals the product of the means: ad = bc",
  "(x + 3)(x + 2) = (x + 11)(x − 2) gives x² + 5x + 6 = x² + 9x − 22, so 4x = 28 and x = 7. Check: 10 : 18 = 5 : 9.",
  ["(x + 3)(x + 2) = (x + 11)(x − 2)", "x² + 5x + 6 = x² + 9x − 22", "4x = 28 ⇒ x = 7"],
  why="−7/3 multiplies the wrong pairs, (x + 3)(x − 2) = (x + 11)(x + 2); 5.5 drops the constant 6 when expanding; 28 "
      "stops at 4x = 28.", secs=45)

kk = F(32)
inc = [7 * kk, 9 * kk, 12 * kk]
sav_a = inc[0] / 4
m_ = (inc[0] - sav_a) / 8
sav = [inc[0] - 8 * m_, inc[1] - 9 * m_, inc[2] - 15 * m_]
assert sav == [56, 99, 69] and ratio(*sav) == "56 : 99 : 69"
Q(T, "Coins and salary share", I,
  "The incomes of A, B and C are in the ratio 7 : 9 : 12 and their expenditures are in the ratio 8 : 9 : 15. If A "
  "saves one-fourth of his income, what is the ratio of the savings of A, B and C?",
  "56 : 99 : 69", ["7 : 9 : 12", "8 : 9 : 15", "69 : 99 : 56"],
  "Use one unit for incomes and another for expenditures; A's saving links the two units",
  "Let the incomes be 7k, 9k and 12k. A saves 7k/4, so A spends 21k/4 = 8 parts of expenditure, and one expenditure "
  "part = 21k/32. Then B spends 189k/32 and saves 288k/32 − 189k/32 = 99k/32; C spends 315k/32 and saves "
  "384k/32 − 315k/32 = 69k/32; A saves 56k/32. Ratio 56 : 99 : 69.",
  ["Take k = 32: incomes 224, 288, 384", "A saves 56, spends 168 = 8 × 21", "Expenditures 168, 189, 315",
   "Savings 56, 99, 69"],
  why="7 : 9 : 12 assumes everyone saves a quarter; 8 : 9 : 15 is the expenditure ratio; 69 : 99 : 56 lists the "
      "savings in reverse order.", secs=75)

val = F(144000)
pieces = [val * F(w * w, 36) for w in (1, 2, 3)]
assert pieces == [4000, 16000, 36000] and val - sum(pieces) == 88000
assert sum(pieces) == 56000 and val - pieces[2] == 108000 and val * (1 - F(6, 36)) == 120000
Q(T, "Proportion", I,
  "The price of a diamond varies directly as the square of its weight. A diamond worth ₹1,44,000 breaks into three "
  "pieces whose weights are in the ratio 1 : 2 : 3. What is the loss caused by the breakage?",
  "₹88,000", ["₹56,000", "₹1,08,000", "₹1,20,000"],
  "Price ∝ weight², so compare the sum of the squares of the parts with the square of the whole",
  "Whole weight = 6 parts, so its price corresponds to 6² = 36 units: 1 unit = ₹4,000. The pieces are worth 1², 2² and "
  "3² units = 14 units = ₹56,000. Loss = 1,44,000 − 56,000 = ₹88,000.",
  ["Whole: 6² = 36 units = ₹1,44,000 ⇒ 1 unit = ₹4,000", "Pieces: 1 + 4 + 9 = 14 units = ₹56,000",
   "Loss = ₹88,000"],
  why="₹56,000 is the value of the pieces, not the loss; ₹1,08,000 subtracts only the largest piece; ₹1,20,000 adds "
      "the weights (6) instead of their squares (14).", secs=70)

shares = [F(1100) * F(r, 11) for r in (5, 4, 2)]
coins = [shares[0] / 1, shares[1] / 2, shares[2] / 5]
assert shares == [500, 400, 200] and coins == [500, 200, 40] and sum(coins) == 740
assert shares[0] + shares[1] / 5 + shares[2] / 2 == 680 and coins[0] + coins[2] == 540
Q(T, "Coins and salary share", A,
  "A bag contains ₹1, ₹2 and ₹5 coins whose total VALUES are in the ratio 5 : 4 : 2. The total value of the coins is "
  "₹1,100. How many coins are there in the bag?",
  "740", ["1,100", "680", "540"],
  "Split the value first, then divide each share by its coin's denomination",
  "Values: ₹1 coins 5/11 × 1,100 = ₹500, ₹2 coins ₹400 and ₹5 coins ₹200. Number of coins: 500 + 400 ÷ 2 + 200 ÷ 5 = "
  "500 + 200 + 40 = 740.",
  ["Values = ₹500, ₹400, ₹200", "₹1 coins = 500", "₹2 coins = 200", "₹5 coins = 40", "Total = 740"],
  why="1,100 treats each rupee as one coin; 680 divides the ₹400 by 5 and the ₹200 by 2 (wrong coins); 540 leaves out "
      "the ₹2 coins.", secs=80)

# ================================================================ Problems on Ages (B1 I2 A1)
T = "Problems on Ages"
sol = [(3 * d + 3, d) for d in range(1, 40) if 3 * d + 3 + 3 == 2 * (d + 3) + 10]
assert sol == [(33, 10)]
Q(T, "Present and future ages", B,
  "A mother's present age is 3 years more than three times her daughter's present age. Three years from now, the "
  "mother's age will be 10 years more than twice the daughter's age then. What is the mother's present age?",
  "33 years", ["10 years", "36 years", "30 years"],
  "Write both statements as equations in the daughter's present age",
  "Let the daughter be d. Mother = 3d + 3. In 3 years: 3d + 6 = 2(d + 3) + 10 = 2d + 16, so d = 10 and the mother is "
  "3 × 10 + 3 = 33.",
  ["M = 3d + 3", "M + 3 = 2(d + 3) + 10", "3d + 6 = 2d + 16 ⇒ d = 10", "M = 33"],
  why="10 years is the daughter's age; 36 years is the mother's age three years from now; 30 years forgets the "
      "'3 more than' (3 × 10).", secs=45)

k_ = F(44, 11)
a_, b_ = 6 * k_, 5 * k_
n_ = [n for n in range(0, 60) if F(a_ + n, b_ + n) == F(8, 7)]
assert (a_, b_) == (24, 20) and n_ == [8] and F(24 + 12, 20 + 12) == F(9, 8)
Q(T, "Ratio-based ages", I,
  "The present ages of A and B are in the ratio 6 : 5 and add up to 44 years. After how many years will their ages "
  "be in the ratio 8 : 7?",
  "8 years", ["2 years", "4 years", "12 years"],
  "Find the present ages from the sum, then add the same n to both",
  "A = 6/11 × 44 = 24 and B = 20. (24 + n) : (20 + n) = 8 : 7 gives 168 + 7n = 160 + 8n, so n = 8. Check: 32 : 28 = "
  "8 : 7.",
  ["A = 24, B = 20", "7(24 + n) = 8(20 + n)", "168 + 7n = 160 + 8n ⇒ n = 8"],
  why="2 years subtracts the ratio terms (8 − 6); 4 years is the age gap; 12 years gives 36 : 32 = 9 : 8.", secs=55)

sol = [(3 * s, s) for s in range(1, 40) if 3 * s + 20 == s + 40]
assert sol == [(30, 10)] and [s for s in range(1, 40) if 3 * s == s + 40] == [20]
Q(T, "Present and future ages", I,
  "A father is now three times as old as the sum of the ages of his two sons. Twenty years from now, his age will "
  "equal the sum of their ages. What is the father's present age?",
  "30 years", ["50 years", "10 years", "60 years"],
  "In 20 years the father gains 20 years, but the two sons together gain 40",
  "Let the sons' total now be S, so the father is 3S. In 20 years: 3S + 20 = S + 40, so 2S = 20, S = 10 and the father "
  "is 30.",
  ["Father = 3S", "3S + 20 = S + 2 × 20", "2S = 20 ⇒ S = 10", "Father = 30"],
  why="50 years is the father's age 20 years from now; 10 years is the sons' present total; 60 years forgets to add 20 "
      "years to the father's own age (3S = S + 40).", secs=60)

sol = [(10 * a + b, 10 * b + a) for a in range(1, 10) for b in range(1, 10)
       if 10 * a + b > 10 * b + a and (10 * a + b) - 1 == 2 * ((10 * b + a) - 1)]
assert sol == [(73, 37)]
Q(T, "Present and future ages", A,
  "A father's age, a two-digit number, has the same digits as his son's age in reverse order. One year ago the father "
  "was exactly twice as old as the son. What is the father's present age?",
  "73 years", ["37 years", "72 years", "74 years"],
  "Write the ages as 10a + b and 10b + a and look for digit solutions",
  "Let the father be 10a + b and the son 10b + a. Then 10a + b − 1 = 2(10b + a − 1), so 8a = 19b − 1. The only digits "
  "that work are b = 3, a = 7. The father is 73 and the son 37 (a year ago: 72 = 2 × 36).",
  ["10a + b − 1 = 2(10b + a − 1)", "8a = 19b − 1", "b = 3 ⇒ a = 7", "Father 73, son 37"],
  why="37 years is the son's age; 72 years is the father's age one year ago; 74 years is his age a year from now.",
  secs=90, by=BRUTE)

# ================================================================ Average (B1 I1 A1)
T = "Average"
m7 = [n for n in range(51, 150) if n % 7 == 0]
assert m7[0] == 56 and m7[-1] == 147 and F(sum(m7), len(m7)) == F(203, 2) and F(63 + 147, 2) == 105
Q(T, "Simple average", B, "What is the average of all the multiples of 7 between 50 and 150?",
  "101.5", ["100", "98", "105"],
  "Equally spaced numbers: average = (first + last) ÷ 2",
  "The multiples of 7 between 50 and 150 run from 56 to 147. Their average is (56 + 147) ÷ 2 = 101.5.",
  ["First = 56 (7 × 8)", "Last = 147 (7 × 21)", "(56 + 147) ÷ 2 = 101.5"],
  why="100 averages 50 and 150, which are not multiples of 7; 98 = 7 × 14 is a middle multiple, not the average; 105 "
      "starts from 63 and skips 56.", secs=40)

g_ = (F(576, 10) - F(6, 10) * 54) / F(4, 10)
assert g_ == 63 and 2 * F(576, 10) - 54 == F(612, 10) and (F(576, 10) - F(4, 10) * 54) / F(6, 10) == 60
assert F(576, 10) + (F(576, 10) - 54) / F(4, 10) == F(666, 10)
Q(T, "Weighted average", I,
  "In an examination, 60% of the candidates were boys. The boys' average score was 54 and the average score of all the "
  "candidates was 57.6. What was the girls' average score?",
  "63", ["61.2", "60", "66.6"],
  "Overall average = weighted average: 0.6 × boys' average + 0.4 × girls' average",
  "0.6 × 54 + 0.4 × g = 57.6, so 32.4 + 0.4g = 57.6, 0.4g = 25.2 and g = 63.",
  ["0.6 × 54 = 32.4", "0.4g = 57.6 − 32.4 = 25.2", "g = 63"],
  why="61.2 treats boys and girls as equal in number; 60 swaps the shares (40% boys); 66.6 adds the gap 3.6 ÷ 0.4 = 9 "
      "to the overall average instead of to the boys' average.", secs=60)

nn = [n for n in range(1, 100) if 36 * n + 96 == 39 * (n + 1)]
assert nn == [19]
need = 40 * 21 - 39 * 20
assert need == 60 and 40 * 21 - 36 * 20 == 120 and 40 * 20 - 39 * 19 == 59
Q(T, "Simple average", A,
  "A batsman's average was 36 runs per innings after a certain number of innings. He then scored 96 in the next "
  "innings, which raised his average to 39. How many runs must he score in the following innings to raise his average "
  "to 40?",
  "60", ["120", "59", "99"],
  "First find the number of innings from the change in average; then the runs needed = new total − old total",
  "If he had played n innings: 36n + 96 = 39(n + 1), so 3n = 57 and n = 19. After 20 innings his total is 20 × 39 = "
  "780. For an average of 40 over 21 innings he needs 840, i.e. 840 − 780 = 60 runs.",
  ["36n + 96 = 39(n + 1) ⇒ n = 19", "Total after 20 innings = 780", "Needed after 21 innings = 840",
   "Runs needed = 60"],
  why="120 uses the old average 36 for 20 innings; 59 counts one innings too few (40 × 20 − 39 × 19); 99 simply adds "
      "3 to the last score.", secs=90)

# ================================================================ Profit and Loss (B2 I2 A3)
T = "Profit and Loss"
assert F(6 - 5, 5) * 100 == 20 and F(1, 6) * 100 == F(50, 3) and F(5, 6) * 100 == F(250, 3)
Q(T, "Cost and selling price", B, "The cost price and the selling price of an article are in the ratio 5 : 6. What "
  "is the profit percentage?",
  "20%", ["16⅔%", "120%", "83⅓%"],
  "Profit % = (SP − CP) ÷ CP × 100",
  "Take CP = 5 and SP = 6. Profit = 1, which is 1/5 = 20% of the cost price.",
  ["CP = 5, SP = 6", "Profit = 1", "1 ÷ 5 = 20%"],
  why="16⅔% divides the profit by the selling price; 120% is SP as a percentage of CP; 83⅓% is CP as a percentage of "
      "SP.", secs=30)

sol = [(c, s) for c in range(1, 101) for s in range(c + 1, 401) if 2 * s - c == 3 * (s - c)]
assert all(s == 2 * c for c, s in sol) and len(sol) > 10
Q(T, "Cost and selling price", B,
  "If the selling price of an article is doubled, the profit becomes three times as large. What is the profit "
  "percentage at the original selling price?",
  "100%", ["300%", "200%", "50%"],
  "Write both profits in terms of CP and SP: 2SP − CP = 3(SP − CP)",
  "2SP − CP = 3SP − 3CP gives SP = 2CP. So the profit equals the cost price: a profit of 100%.",
  ["2SP − CP = 3(SP − CP)", "SP = 2CP", "Profit = CP ⇒ 100%"],
  why="300% is the profit percentage at the doubled price (4CP − CP = 3CP); 200% is the rise in the profit itself "
      "(from P to 3P); 50% is the profit as a percentage of the selling price.", secs=50, by=BRUTE)

cp45 = F(40) / F(80, 100)
sp45 = cp45 * F(120, 100)
n_ = 45 * F(24) / sp45
assert cp45 == 50 and sp45 == 60 and n_ == 18 and 45 * F(24, 40) == 27 and 45 * F(24, 48) == F(45, 2)
assert 45 * F(24, 80) == F(27, 2)
Q(T, "Cost and selling price", I,
  "By selling 45 lemons for ₹40, a vendor loses 20%. How many lemons should he sell for ₹24 to gain 20%?",
  "18", ["27", "22.5", "13.5"],
  "Find the cost of the 45 lemons from the loss, then the selling price that gives the required gain",
  "₹40 is 80% of the cost, so 45 lemons cost ₹50. For a 20% gain they must sell for ₹60, i.e. 45 lemons for ₹60. For "
  "₹24 he should give 45 × 24 ÷ 60 = 18 lemons.",
  ["CP of 45 = 40 ÷ 0.8 = ₹50", "SP for 20% gain = ₹60", "Lemons for ₹24 = 45 × 24/60 = 18"],
  why="27 keeps the old rate of 45 lemons for ₹40; 22.5 applies the 20% gain to ₹40 instead of to the cost; 13.5 "
      "doubles ₹40 to ₹80 for the 45 lemons.", secs=60)

M_ = F(9, 10) / F(3, 4)
assert M_ == F(6, 5) and (M_ - 1) * 100 == 20
Q(T, "Marked price", I,
  "By selling an article at three-fourths of its marked price, a shopkeeper incurs a loss of 10%. What would his "
  "profit percentage be if he sold it at the marked price?",
  "20%", ["15%", "35%", "25%"],
  "Link the marked price to the cost price: 0.75 × MP = 0.90 × CP",
  "0.75 MP = 0.9 CP, so MP = 1.2 CP. Selling at the marked price gives a profit of 20%.",
  ["0.75 MP = 0.9 CP", "MP = 0.9/0.75 × CP = 1.2 CP", "Profit = 20%"],
  why="15% subtracts the 10% loss from the 25% cut; 35% adds the 25% cut and the 10% loss; 25% takes the cut of "
      "one-fourth as the markup.", secs=60)

tv = [t for t in range(1000, 82000, 1000) if F(125, 100) * t == F(80, 100) * (82000 - t)]
assert tv == [32000] and F(125, 100) * 32000 == 40000
Q(T, "Cost and selling price", A,
  "A dealer bought a television and a refrigerator for ₹82,000 in all. He sold the television at a profit of 25% and "
  "the refrigerator at a loss of 20%, and both fetched the same price. What did the television cost him?",
  "₹32,000", ["₹50,000", "₹41,000", "₹40,000"],
  "Equal selling prices: 1.25 × CP(TV) = 0.80 × CP(fridge); split ₹82,000 in that ratio",
  "1.25T = 0.8F gives T : F = 0.8 : 1.25 = 16 : 25. So T = 16/41 × 82,000 = ₹32,000 (and F = ₹50,000; each sold for "
  "₹40,000).",
  ["1.25T = 0.80F", "T : F = 16 : 25", "T = 82,000 × 16/41 = 32,000"],
  why="₹50,000 is the refrigerator's cost; ₹41,000 splits the total equally; ₹40,000 is the common selling price.",
  secs=80, by=BRUTE)

rev = F(1, 2) * F(14, 10) + F(1, 4) * F(14, 10) * F(8, 10) + F(1, 4) * F(14, 10) * F(6, 10)
assert rev == F(119, 100) and F(14, 10) * F(8, 10) == F(112, 100)
Q(T, "Marked price", A,
  "A shopkeeper marks his goods 40% above cost. He sells half his stock at the marked price, one-fourth at a "
  "discount of 20% and the rest at a discount of 40%. What is his overall profit percentage?",
  "19%", ["12%", "25%", "40%"],
  "Find the revenue from each part of the stock per unit of cost, then add",
  "Take the cost of the whole stock as 100, so it is marked at 140. Half at MP: 70. One-fourth at 20% off: 35 × 0.8 = "
  "28. One-fourth at 40% off: 35 × 0.6 = 21. Revenue = 119, a profit of 19%.",
  ["Marked value = 140", "½ × 140 = 70", "¼ × 140 × 0.8 = 28", "¼ × 140 × 0.6 = 21", "70 + 28 + 21 = 119 ⇒ 19%"],
  why="12% averages the three discounts as 20% without weighting by stock; 25% subtracts the weighted discount (15) "
      "from the markup (40); 40% ignores the discounts.", secs=90)

cost = 60 * 40 + 40 * 50
left = F(100) * F(96, 100)
price = cost * F(120, 100) / left
assert cost == 4400 and left == 96 and price == 55 and cost * F(120, 100) / 100 == F(528, 10)
assert near(F(4400, 96), 45.83, 0.01) and F(40 + 50, 2) * F(12, 10) == 54
Q(T, "Cost and selling price", A,
  "A grocer buys 60 kg of rice at ₹40 per kg and 40 kg at ₹50 per kg and mixes them. In handling, 4% of the mixture by "
  "weight is lost. At what price per kg must he sell the rest to gain 20% on his total outlay?",
  "₹55", ["₹52.80", "₹45.83", "₹54"],
  "Required revenue = total cost × 1.2; divide it by the quantity actually left to sell",
  "Cost = 60 × 40 + 40 × 50 = ₹4,400. For a 20% gain he needs ₹5,280. Only 96 kg remain, so the price must be "
  "5,280 ÷ 96 = ₹55 per kg.",
  ["Cost = 2,400 + 2,000 = 4,400", "Target revenue = 5,280", "Saleable = 96 kg", "5,280 ÷ 96 = ₹55"],
  why="₹52.80 ignores the 4% loss (divides by 100 kg); ₹45.83 recovers only the cost (4,400 ÷ 96); ₹54 averages ₹40 "
      "and ₹50 without weighting and ignores the loss.", secs=90)

# ================================================================ Discount (B1 I1 A1)
T = "Discount"
assert F(1, 3) * 100 == F(100, 3) and F(1, 2) * 100 == 50 and F(1, 4) * 100 == 25
Q(T, "Single discount", B, "A shop offers 'Buy 2, get 1 free' on soaps of the same price. What single discount "
  "percentage is this equivalent to?",
  "33⅓%", ["50%", "25%", "66⅔%"],
  "Discount % = value given free ÷ value of everything taken × 100",
  "The customer takes 3 soaps and pays for 2. The free soap is 1 of 3, so the discount is 1/3 = 33⅓%.",
  ["Takes 3, pays for 2", "Free = 1 of 3", "= 33⅓%"],
  why="50% compares the free soap with the 2 paid for; 25% treats it as 1 free out of 4; 66⅔% is the fraction actually "
      "paid.", secs=35)

mp_ = F(100)
c_ = mp_ * F(9, 10) - mp_ * F(1, 10)
assert c_ == 80 and (mp_ - c_) / c_ * 100 == 25 and (mp_ - c_) / mp_ * 100 == 20 and (90 - c_) / c_ * 100 == F(25, 2)
Q(T, "Discount with profit", I,
  "A shopkeeper allows a discount of 10% on the marked price, and the discount in rupees is exactly equal to his "
  "profit in rupees. By what percentage is the marked price above the cost price?",
  "25%", ["20%", "12.5%", "10%"],
  "Take MP = 100; then the discount is 10 and the profit is also 10",
  "MP = 100, discount = 10, so SP = 90. Profit = 10, so CP = 90 − 10 = 80. The marked price is 20 above the cost, which "
  "is 20/80 = 25% above it.",
  ["MP = 100, SP = 90", "Profit = 10 ⇒ CP = 80", "Markup = 20/80 = 25%"],
  why="20% measures the markup on the marked price; 12.5% is the profit percentage (10/80); 10% repeats the discount.",
  secs=55)

p1 = F(7500) * F(8, 10)
assert p1 == 6000 and p1 > 5000
p2 = p1 * F(9, 10)
paid = p2 * F(95, 100)
assert p2 == 5400 and paid == 5130 and F(7500) * F(65, 100) == 4875 and p2 - F(7500) * F(5, 100) == 5025
Q(T, "Successive discounts", A,
  "A store gives 20% off the marked price, then a further 10% off the discounted price on bills above ₹5,000, and "
  "finally a 5% cashback on the amount paid. What is the net cost to a customer who buys a single item marked "
  "₹7,500?",
  "₹5,130", ["₹4,875", "₹5,400", "₹5,025"],
  "Apply each reduction to the amount left after the previous one; check the ₹5,000 condition on the discounted bill",
  "After 20% off: ₹6,000, which is above ₹5,000, so a further 10% off gives ₹5,400. A 5% cashback on ₹5,400 is ₹270, so "
  "the net cost is ₹5,130.",
  ["7,500 × 0.8 = 6,000 (> 5,000)", "6,000 × 0.9 = 5,400", "Cashback = 5% of 5,400 = 270", "Net = 5,130"],
  why="₹4,875 adds the three rates and takes 35% off the marked price; ₹5,400 forgets the cashback; ₹5,025 takes the "
      "cashback on the marked price (₹375) instead of on the amount paid.", secs=80)

# ================================================================ Simple Interest (B2 I2 A1)
T = "Simple Interest"
P_ = F(7260) / (1 + F(5 * 4, 100))
assert P_ == 6050 and 7260 - P_ == 1210 and F(7260) * F(80, 100) == 5808 and F(7260) / F(11, 10) == 6600
Q(T, "Basic SI", B, "A sum of money amounts to ₹7,260 in 4 years at 5% per annum simple interest. What is the sum?",
  "₹6,050", ["₹5,808", "₹1,210", "₹6,600"],
  "Amount = P(1 + rt/100), so P = Amount ÷ (1 + rt/100)",
  "In 4 years at 5% the interest is 20% of P, so 1.2P = 7,260 and P = ₹6,050.",
  ["rt = 5 × 4 = 20%", "1.2P = 7,260", "P = 6,050"],
  why="₹5,808 takes 20% off the amount instead of dividing by 1.2; ₹1,210 is the interest; ₹6,600 uses only 10% "
      "(2 years).", secs=40)

si_ = F(4500 * 6 * 4, 100)
t_ = si_ / F(3600 * 5, 100)
assert si_ == 1080 and t_ == 6 and si_ / F(3600 * 6, 100) == 5 and F(4 * 6, 5) == F(24, 5)
assert 4 * F(3600, 4500) * F(6, 5) == F(384, 100)
Q(T, "Basic SI", B,
  "In how many years will ₹3,600 earn at 5% per annum simple interest the same interest that ₹4,500 earns in 4 years "
  "at 6% per annum?",
  "6 years", ["5 years", "4.8 years", "3.84 years"],
  "Find the target interest first, then solve SI = Prt/100 for t",
  "₹4,500 at 6% for 4 years earns 4,500 × 6 × 4 ÷ 100 = ₹1,080. ₹3,600 at 5% earns ₹180 a year, so it needs "
  "1,080 ÷ 180 = 6 years.",
  ["Target SI = 1,080", "3,600 × 5% = 180 per year", "1,080 ÷ 180 = 6 years"],
  why="5 years uses 6% for the second sum as well; 4.8 years ignores the different principals (4 × 6/5); 3.84 years "
      "inverts the ratio of the principals.", secs=50)

parts = [p for p in range(100, 6500, 100) if F(p * 5 * 6, 100) == F((6500 - p) * 4 * 5, 100)]
assert parts == [2600]
Q(T, "Basic SI", I,
  "₹6,500 is divided into two parts. The simple interest on the first part at 5% per annum for 6 years equals the "
  "simple interest on the second part at 4% per annum for 5 years. What is the first part?",
  "₹2,600", ["₹3,900", "₹3,250", "₹1,300"],
  "Equal interest: P₁ × 30% = P₂ × 20%, so P₁ : P₂ = 20 : 30 = 2 : 3",
  "The first part earns 30% of itself and the second 20% of itself. For equal interest, P₁ : P₂ = 2 : 3, so the first "
  "part is 2/5 × 6,500 = ₹2,600.",
  ["rt₁ = 30%, rt₂ = 20%", "0.3P₁ = 0.2P₂ ⇒ P₁ : P₂ = 2 : 3", "P₁ = 6,500 × 2/5 = 2,600"],
  why="₹3,900 is the second part (or takes the ratio as 3 : 2); ₹3,250 splits the sum equally; ₹1,300 is the "
      "difference between the two parts.", secs=60, by=BRUTE)

si_ = F(40000 * 7 * 2, 100) + F(60000 * 7 * 3, 100)
assert si_ == 18200 and F(60000 * 7 * 5, 100) == 21000 and F(40000 * 7 * 5, 100) == 14000
assert F(60000 * 7 * 2, 100) + F(40000 * 7 * 3, 100) == 16800
Q(T, "Basic SI", I,
  "Neha deposits ₹40,000 at 7% per annum simple interest. After 2 years she adds ₹20,000 to the same deposit at the "
  "same rate. What total interest will she have earned at the end of 5 years from the first deposit?",
  "₹18,200", ["₹21,000", "₹14,000", "₹16,800"],
  "Split the time: the principal is ₹40,000 for the first 2 years and ₹60,000 for the next 3",
  "First 2 years: 40,000 × 7% × 2 = ₹5,600. Next 3 years: 60,000 × 7% × 3 = ₹12,600. Total = ₹18,200.",
  ["40,000 × 0.07 × 2 = 5,600", "60,000 × 0.07 × 3 = 12,600", "Total = 18,200"],
  why="₹21,000 charges the full ₹60,000 for all 5 years; ₹14,000 ignores the second deposit; ₹16,800 swaps the periods "
      "(₹60,000 for 2 years, ₹40,000 for 3).", secs=60)

sol = [(p, r) for p in range(500, 30001, 100) for r in range(1, 31)
       if F(p * r * 4, 100) == 1440 and F(p * (r + 1) * 5, 100) == 2000]
assert sol == [(4000, 9)] and F(560 * 100, 5) == 11200 and F(560 * 100, 4) == 14000
Q(T, "SI with changing rates", A,
  "The simple interest on a sum for 4 years is ₹1,440. If the rate were 1% higher and the time 1 year longer, the "
  "simple interest would be ₹2,000. What is the sum?",
  "₹4,000", ["₹11,200", "₹14,000", "₹3,600"],
  "Write both interests as P × r × t/100 and eliminate the product Pr",
  "4Pr/100 = 1,440, so Pr/100 = 360. 5P(r + 1)/100 = 2,000, so P(r + 1)/100 = 400. Subtracting, P/100 = 40 and "
  "P = ₹4,000 (the rate is 9%).",
  ["Pr/100 = 1,440 ÷ 4 = 360", "P(r + 1)/100 = 2,000 ÷ 5 = 400", "P/100 = 40 ⇒ P = 4,000", "r = 9%"],
  why="₹11,200 credits the whole ₹560 increase to the extra 1% over 5 years; ₹14,000 keeps the time at 4 years in the "
      "second case; ₹3,600 assumes a 10% rate (1,440 ÷ 0.4).", secs=90, by=BRUTE)

# ================================================================ Compound Interest (B1 I3 A2)
T = "Compound Interest"
ci_ = 25000 * (F(112, 100) ** 2 - 1)
assert ci_ == 6360 and 25000 * F(24, 100) == 6000 and 25000 * F(12, 100) == 3000
Q(T, "Annual compounding", B, "What is the compound interest on ₹25,000 for 2 years at 12% per annum, compounded "
  "annually?",
  "₹6,360", ["₹6,000", "₹3,000", "₹31,360"],
  "CI = P[(1 + r/100)ⁿ − 1]",
  "Amount = 25,000 × 1.12² = 25,000 × 1.2544 = ₹31,360, so CI = ₹6,360.",
  ["1.12² = 1.2544", "Amount = 31,360", "CI = 31,360 − 25,000 = 6,360"],
  short="Two-year CI rate = 12 + 12 + 12 × 12/100 = 25.44%.",
  why="₹6,000 is the simple interest; ₹3,000 is one year's interest; ₹31,360 is the amount, not the interest.",
  secs=40)

eff = (F(102, 100) ** 4 - 1) * 100
assert r2(eff) == F(824, 100) and (F(104, 100) ** 2 - 1) * 100 == F(816, 100) and r2((F(108, 100) ** 4 - 1) * 100) == F(3605, 100)
Q(T, "Half-yearly and quarterly", I,
  "What is the effective annual rate of interest on a deposit that pays 8% per annum compounded quarterly (correct to "
  "two decimal places)?",
  "8.24%", ["8%", "8.16%", "36.05%"],
  "Effective rate = (1 + r/4)⁴ − 1 for quarterly compounding",
  "Each quarter pays 2%. Over a year, 1.02⁴ = 1.0824 (to four decimals), so the effective annual rate is 8.24%.",
  ["Quarterly rate = 8% ÷ 4 = 2%", "1.02² = 1.0404", "1.0404² = 1.08243…", "Effective rate ≈ 8.24%"],
  why="8% ignores compounding; 8.16% compounds only half-yearly (1.04² − 1); 36.05% applies the full 8% every quarter.",
  secs=60)

n_ = [n for n in range(1, 10) if F(8000) * F(105, 100) ** n == 9261]
assert n_ == [3] and F(8000) * F(105, 100) ** 2 == 8820 and F(8000) * F(11, 10) ** 2 == 9680
Q(T, "Half-yearly and quarterly", I,
  "In what time will ₹8,000 amount to ₹9,261 at 10% per annum compound interest, compounded half-yearly?",
  "1½ years", ["3 years", "1 year", "2 years"],
  "Half-yearly: rate 5% per half-year; solve 1.05ⁿ = 9,261/8,000 for the number of half-years",
  "9,261/8,000 = (21/20)³ = 1.05³. So the money is compounded for 3 half-years, i.e. 1½ years.",
  ["Rate per half-year = 5%", "9,261 ÷ 8,000 = 1.157625 = 1.05³", "3 half-years = 1½ years"],
  short="9,261 = 21³ and 8,000 = 20³.",
  why="3 years counts half-years as years; 1 year gives only ₹8,820; 2 years would give more than ₹9,261 (₹9,724.05).",
  secs=55)

r_ = F(1452 - 1320, 1320)
P_ = F(1320) / ((1 + r_) * r_)
assert r_ == F(1, 10) and P_ == 12000 and F(1320) / r_ == 13200 and F(1452) / r_ == 14520 and F(13200) / F(12, 10) == 11000
Q(T, "Annual compounding", I,
  "The compound interest (compounded annually) on a sum is ₹1,320 for the second year and ₹1,452 for the third year. "
  "What is the sum?",
  "₹12,000", ["₹13,200", "₹14,520", "₹11,000"],
  "Interest of a year = previous year's interest × (1 + r); the second year's interest is P × (1 + r) × r",
  "1,452 ÷ 1,320 = 1.1, so the rate is 10%. Second-year interest = P × 1.1 × 0.1 = 0.11P = 1,320, so P = ₹12,000.",
  ["r = (1,452 − 1,320) ÷ 1,320 = 10%", "0.11P = 1,320", "P = 12,000"],
  why="₹13,200 treats ₹1,320 as the first year's interest; ₹14,520 treats ₹1,452 as the first year's interest; "
      "₹11,000 divides 13,200 by 1.2 instead of 1.1.", secs=65)

sol = [x for x in range(1000, 37000, 1000) if F(x) * (F(11, 10) ** 2 - 1) == F(37000 - x) * F(16, 100)]
assert sol == [16000] and near(F(37000 * 4, 9), 16444.44, 0.01)
Q(T, "CI vs SI difference", A,
  "Ramesh invests ₹37,000 in two parts: one at 10% per annum compound interest (compounded annually) and the other "
  "at 8% per annum simple interest. After 2 years the two parts have earned equal interest. How much did he invest at "
  "compound interest?",
  "₹16,000", ["₹21,000", "₹18,500", "₹16,444.44"],
  "Two-year CI at 10% = 21% of the principal; two-year SI at 8% = 16%",
  "0.21x = 0.16(37,000 − x), so 0.37x = 5,920 and x = ₹16,000 (the other part, ₹21,000, earns ₹3,360 too).",
  ["CI factor = 1.1² − 1 = 0.21", "SI factor = 0.16", "0.21x = 0.16(37,000 − x)", "x = 16,000"],
  why="₹21,000 is the part at simple interest; ₹18,500 splits the money equally; ₹16,444.44 treats the 10% part as "
      "simple interest too (0.20x = 0.16y).", secs=80, by=BRUTE)

r_ = F(26, 25) - 1
assert F(15625) * F(26, 25) ** 3 == 17576 and r_ * 100 == 4
assert r2(F(17576 - 15625, 15625 * 3) * 100) == F(416, 100) and r2(F(1951, 15625) * 100) == F(1249, 100)
assert near((17576 / 15625) ** 0.5 * 100 - 100, 6.06, 0.01)
Q(T, "Annual compounding", A,
  "At what rate per annum, compounded annually, will ₹15,625 amount to ₹17,576 in 3 years?",
  "4%", ["4.16%", "12.49%", "6.06%"],
  "(1 + r)³ = A/P; recognise 15,625 = 25³ and 17,576 = 26³",
  "17,576 ÷ 15,625 = (26/25)³, so 1 + r = 26/25 = 1.04 and the rate is 4%.",
  ["15,625 = 25³", "17,576 = 26³", "1 + r = 26/25", "r = 4%"],
  why="4.16% treats the growth as simple interest (12.49% ÷ 3); 12.49% is the total growth over 3 years; 6.06% takes "
      "the square root instead of the cube root.", secs=70)

# ================================================================ Partnership (B2 I2 A1)
T = "Partnership"
la = F(9000) * F(40, 90)
assert la == 4000 and F(9000) * F(50, 90) == 5000 and F(9000) * F(40, 100) == 3600
Q(T, "Simple partnership", B,
  "A and B invest ₹40,000 and ₹50,000 in a business for the same period. The business makes a loss of ₹9,000, shared "
  "in the ratio of their investments. What is A's share of the loss?",
  "₹4,000", ["₹5,000", "₹4,500", "₹3,600"],
  "Losses, like profits, are shared in the ratio of capital × time",
  "Capitals 40,000 : 50,000 = 4 : 5. A's share = 4/9 × 9,000 = ₹4,000.",
  ["Ratio 4 : 5", "A = 9,000 × 4/9 = 4,000"],
  why="₹5,000 is B's share; ₹4,500 splits the loss equally; ₹3,600 takes A's share as 40% of the loss.", secs=35)

bcap = F(30000 * 12 * 3, 2 * 10)
assert bcap == 54000 and F(30000 * 3, 2) == 45000 and F(30000 * 10 * 3, 2 * 12) == 37500 and F(30000 * 12 * 2, 3 * 10) == 24000
Q(T, "Compound partnership", B,
  "A invests ₹30,000 for 12 months and B invests some money for 10 months. Their profits are in the ratio 2 : 3. How "
  "much did B invest?",
  "₹54,000", ["₹45,000", "₹37,500", "₹24,000"],
  "Profit ratio = ratio of capital × months",
  "30,000 × 12 : B × 10 = 2 : 3, so B × 10 = 30,000 × 12 × 3/2 = 5,40,000 and B = ₹54,000.",
  ["A's capital-months = 3,60,000", "B × 10 = 3,60,000 × 3/2 = 5,40,000", "B = 54,000"],
  why="₹45,000 ignores the different periods; ₹37,500 swaps the periods (multiplies by 10/12 instead of 12/10); "
      "₹24,000 uses the profit ratio upside down.", secs=45)

caps = [F(20), F(30), F(50)]
P_ = F(90000)
eq = P_ / 3 / 3
sh = [eq + (P_ * F(2, 3)) * c / sum(caps) for c in caps]
assert sh == [22000, 28000, 40000] and sh[2] - sh[0] == 18000 and P_ * F(50 - 20, 100) == 27000
Q(T, "Simple partnership", I,
  "A, B and C invest ₹20,000, ₹30,000 and ₹50,000 in a business. They agree that one-third of the profit is shared "
  "equally and the rest in the ratio of their investments. Out of a profit of ₹90,000, how much more does C get than "
  "A?",
  "₹18,000", ["₹27,000", "₹40,000", "₹22,000"],
  "The equal part adds the same amount to everyone, so only the capital-based part creates a difference",
  "Equal part: ₹30,000, i.e. ₹10,000 each. Capital part: ₹60,000 in the ratio 2 : 3 : 5, i.e. ₹12,000, ₹18,000, "
  "₹30,000. A gets ₹22,000 and C gets ₹40,000; the difference is ₹18,000.",
  ["Equal part = 30,000 ⇒ 10,000 each", "Capital part 60,000 ⇒ 12,000 : 18,000 : 30,000", "A = 22,000, C = 40,000",
   "C − A = 18,000"],
  why="₹27,000 shares the whole profit by capital; ₹40,000 is C's share; ₹22,000 is A's share.", secs=60)

cap = [F(1, 2), F(1, 3), F(1, 4)]
base = [c * 12 for c in cap]  # 6 : 4 : 3
cm = [base[0] * 4 + base[0] * F(3, 2) * 8, base[1] * 12, base[2] * 12]
P_ = F(195000)
shareB = P_ * cm[1] / sum(cm)
assert base == [6, 4, 3] and cm == [96, 48, 36] and shareB == 52000
assert P_ * 4 / 13 == 60000 and P_ * 3 / 9 == 65000 and P_ * cm[0] / sum(cm) == 104000
Q(T, "Compound partnership", I,
  "A, B and C start a business with capitals in the ratio ½ : ⅓ : ¼. After 4 months A increases his capital by 50%. "
  "Out of a profit of ₹1,95,000 at the end of the year, what is B's share?",
  "₹52,000", ["₹60,000", "₹65,000", "₹1,04,000"],
  "Convert the fractional ratio to whole numbers (× 12), then multiply each capital by its time",
  "½ : ⅓ : ¼ = 6 : 4 : 3. A: 6 × 4 + 9 × 8 = 96; B: 4 × 12 = 48; C: 3 × 12 = 36. Ratio 96 : 48 : 36 = 8 : 4 : 3. "
  "B's share = 4/15 × 1,95,000 = ₹52,000.",
  ["½ : ⅓ : ¼ = 6 : 4 : 3", "A = 6 × 4 + 9 × 8 = 96", "B = 48, C = 36", "8 : 4 : 3 ⇒ B = 1,95,000 × 4/15 = 52,000"],
  why="₹60,000 ignores A's increase (6 : 4 : 3); ₹65,000 reads the ratio from the denominators as 2 : 3 : 4; "
      "₹1,04,000 is A's share.", secs=75)

sol = [x for x in range(1000, 60000, 1000) if 60000 * 4 + (60000 - x) * 8 == 40000 * 4 + (40000 + x) * 8]
assert sol == [15000] and [x for x in range(1000, 60000, 1000) if 60000 * 4 + (60000 - x) * 8 == 40000 * 12] == [30000]
assert [x for x in range(1000, 60000, 1000) if 60000 * 6 + (60000 - x) * 6 == 40000 * 6 + (40000 + x) * 6] == [20000]
Q(T, "Compound partnership", A,
  "A and B start a business with ₹60,000 and ₹40,000. After 4 months, A withdraws an amount x and B adds the same "
  "amount x to his capital. At the end of the year the profit is shared equally. What is x?",
  "₹15,000", ["₹10,000", "₹20,000", "₹30,000"],
  "Equal profit shares need equal capital-months over the whole year",
  "A: 60,000 × 4 + (60,000 − x) × 8. B: 40,000 × 4 + (40,000 + x) × 8. Setting them equal: 7,20,000 − 8x = "
  "4,80,000 + 8x, so 16x = 2,40,000 and x = ₹15,000.",
  ["A = 2,40,000 + 8(60,000 − x)", "B = 1,60,000 + 8(40,000 + x)", "7,20,000 − 8x = 4,80,000 + 8x", "x = 15,000"],
  why="₹10,000 only equalises the two capitals for the last 8 months and ignores A's lead in the first 4; ₹20,000 "
      "treats the change as happening after 6 months; ₹30,000 forgets that B also adds x.", secs=90, by=BRUTE)

# ================================================================ Mixture and Alligation (B1 I2 A3)
T = "Mixture and Alligation"
sug = F(60) * F(20, 100)
assert sug == 12 and sug / 80 * 100 == 15 and F(20, 80) * 100 == 25
Q(T, "Mixing solutions", B,
  "A 60-litre sugar solution contains 20% sugar. If 20 litres of water are added, what is the percentage of sugar in "
  "the new solution?",
  "15%", ["20%", "12%", "25%"],
  "Adding water does not change the amount of sugar; only the total volume grows",
  "Sugar = 20% of 60 = 12 litres. New volume = 80 litres. Sugar % = 12 ÷ 80 = 15%.",
  ["Sugar = 12 L", "New volume = 80 L", "12 ÷ 80 = 15%"],
  why="20% ignores the added water; 12% divides 12 litres by 100 instead of 80; 25% takes the 20 litres added as "
      "sugar.", secs=35)

ma, mb, tgt = F(2, 3), F(1, 4), F(1, 2)
r_ = (tgt - mb) / (ma - tgt)
assert r_ == F(3, 2) and (1 - F(1, 3)) / (2 - 1) == F(2, 3) and (tgt - F(1, 3)) / (ma - tgt) == 1 and ma / mb == F(8, 3)
assert (ma * 3 + mb * 2) / 5 == tgt
Q(T, "Alligation rule", I,
  "Jug P contains milk and water in the ratio 2 : 1 and jug Q contains them in the ratio 1 : 3. In what ratio must "
  "the contents of P and Q be mixed to get a mixture with equal amounts of milk and water?",
  "3 : 2", ["2 : 3", "1 : 1", "8 : 3"],
  "Apply alligation to the fraction of milk in each jug: P has 2/3, Q has 1/4, target 1/2",
  "P : Q = (1/2 − 1/4) : (2/3 − 1/2) = 1/4 : 1/6 = 3 : 2. Check: 3 parts of P give 2 of milk, 2 parts of Q give 1/2 "
  "of milk; 2.5 out of 5 is half.",
  ["Milk in P = 2/3, in Q = 1/4", "(1/2 − 1/4) : (2/3 − 1/2) = 1/4 : 1/6", "= 3 : 2"],
  why="2 : 3 applies alligation to the ratios 2 and 1/3 themselves instead of the milk fractions; 1 : 1 uses P's "
      "water fraction (1/3) in place of its milk fraction; 8 : 3 is just the ratio of the two milk fractions.",
  secs=60)

x_ = F(300) * (F(20) - 10) / (70 - 20)
assert x_ == 60 and (300 * F(1, 10) + x_ * F(7, 10)) / (300 + x_) == F(1, 5)
assert near((300 * 0.2 - 30) / 0.7, 42.86, 0.01) and F(300) * 50 / 10 == 1500
Q(T, "Mixing solutions", I,
  "A fuel depot has 300 litres of E10 petrol (10% ethanol by volume). How many litres of a 70% ethanol blend must be "
  "added to make E20 petrol (20% ethanol)?",
  "60 litres", ["1,500 litres", "42.86 litres", "30 litres"],
  "Alligation: E10 : E70 = (70 − 20) : (20 − 10) = 50 : 10 = 5 : 1",
  "E10 and the 70% blend must be mixed in the ratio 5 : 1, so 300 litres of E10 need 300 ÷ 5 = 60 litres of the blend. "
  "Check: (30 + 42) ÷ 360 = 20%.",
  ["E10 : blend = 50 : 10 = 5 : 1", "Blend = 300 ÷ 5 = 60 L", "Ethanol = 30 + 42 = 72 in 360 L = 20%"],
  why="1,500 litres inverts the alligation ratio; 42.86 litres forgets that the added blend also increases the total "
      "volume (it solves 30 + 0.7x = 60); 30 litres simply takes 10% of 300.", secs=60)

c_ = F(50) * F(40, 100)
c_ = c_ - 10 * c_ / 50          # remove 10 L, replace with water
c_ = c_ - 10 * c_ / 50 + 10     # remove 10 L, replace with pure concentrate
assert c_ / 50 * 100 == F(456, 10) and (16 + 10) / F(50) * 100 == 52 and (16 - 4 + 10) / F(50) * 100 == 44
Q(T, "Replacement of mixture", A,
  "A 50-litre tank holds a juice mixture that is 40% concentrate. 10 litres are drawn off and replaced with water. "
  "Then 10 litres of the new mixture are drawn off and replaced with pure concentrate. What percentage of the final "
  "mixture is concentrate?",
  "45.6%", ["40%", "52%", "44%"],
  "Track the litres of concentrate step by step; each draw removes the current percentage",
  "Start: 20 L of concentrate. Draw 10 L (40%): 16 L left; add water: 16 L in 50 L = 32%. Draw 10 L (32%): "
  "16 − 3.2 = 12.8 L; add 10 L concentrate: 22.8 L in 50 L = 45.6%.",
  ["Start: 20 L", "After step 1: 20 − 4 = 16 L (32%)", "Step 2 draw removes 3.2 L ⇒ 12.8 L", "+ 10 L ⇒ 22.8 L",
   "22.8 ÷ 50 = 45.6%"],
  why="40% assumes the two steps cancel; 52% forgets that the second draw also removes concentrate; 44% removes "
      "concentrate at the original 40% strength in the second draw.", secs=90)

x_ = [x for x in range(1, 200) if (20 * 30 + 30 * 40 + x * 55) == 45 * (50 + x)]
assert x_ == [45] and F(30 * (45 - 40), 55 - 45) == 15 and F(20 * (45 - 30), 55 - 45) == 30
assert [x for x in range(1, 200) if 50 * F(30 + 40, 2) + 55 * x == 45 * (50 + x)] == [50]
Q(T, "Alligation rule", A,
  "A grocer has 20 kg of rice at ₹30 per kg and 30 kg of rice at ₹40 per kg. How many kg of rice at ₹55 per kg must "
  "he mix with them so that the whole mixture is worth ₹45 per kg?",
  "45 kg", ["50 kg", "15 kg", "30 kg"],
  "Total value = total quantity × mean price; the two cheaper lots can first be combined into one",
  "The 50 kg already held cost 600 + 1,200 = ₹1,800, i.e. ₹36 per kg. Alligation of ₹36 and ₹55 about ₹45: "
  "cheap : dear = 10 : 9, so the ₹55 rice = 50 × 9/10 = 45 kg. Check: 1,800 + 45 × 55 = 4,275 = 95 × 45.",
  ["Existing 50 kg cost ₹1,800 (₹36 per kg)", "36 → 45 ← 55: ratio 10 : 9", "x = 50 × 9/10 = 45 kg"],
  why="50 kg averages ₹30 and ₹40 as ₹35 without weighting; 15 kg balances only the ₹40 rice; 30 kg balances only the "
      "₹30 rice.", secs=90, by=BRUTE)

mix_cost = F(54) / F(135, 100)
mf = mix_cost / 48
assert mix_cost == 40 and mf == F(5, 6) and ratio(1 - mf, mf) == "1 : 5"
Q(T, "Alligation rule", A,
  "A milkman buys milk at ₹48 per litre, adds water and sells the mixture at ₹54 per litre, making a profit of 35%. "
  "In what ratio did he mix water with milk?",
  "1 : 5", ["5 : 1", "1 : 6", "1 : 8"],
  "Find the cost price of the mixture from the selling price and the profit; water costs nothing",
  "Cost of 1 litre of mixture = 54 ÷ 1.35 = ₹40. Milk costs ₹48, so each litre of mixture contains 40/48 = 5/6 litre "
  "of milk and 1/6 litre of water. Water : milk = 1 : 5.",
  ["CP of mixture = 54 ÷ 1.35 = ₹40", "Milk fraction = 40/48 = 5/6", "Water : milk = 1/6 : 5/6 = 1 : 5"],
  short="Alligation: water (₹0) and milk (₹48) about ₹40 → (48 − 40) : (40 − 0) = 8 : 40 = 1 : 5.",
  why="5 : 1 is milk to water; 1 : 6 is water to the whole mixture; 1 : 8 ignores the profit and compares the extra ₹6 "
      "with ₹48.", secs=80)

# ================================================================ Time and Work (B2 I3 A1)
T = "Time and Work"
b_ = 1 / (F(1, 10) - F(1, 15))
assert b_ == 30 and 1 / (F(1, 15) + F(1, 10)) == 6
Q(T, "Work efficiency", B,
  "A and B together can finish a piece of work in 10 days, and A alone can finish it in 15 days. In how many days can "
  "B alone finish it?",
  "30 days", ["5 days", "25 days", "6 days"],
  "B's one-day work = (A + B)'s one-day work − A's one-day work",
  "Together they do 1/10 of the work a day and A does 1/15, so B does 1/10 − 1/15 = 1/30 a day and needs 30 days.",
  ["1/10 − 1/15 = 3/30 − 2/30 = 1/30", "B alone = 30 days"],
  why="5 days subtracts the day counts (15 − 10); 25 days adds them; 6 days adds the two rates as if both were "
      "individual workers (10 × 15 ÷ 25).", secs=35)

left = 12 * 10 - 12 * 4
d_ = F(left, 9)
assert left == 72 and d_ == 8 and 4 + d_ == 12 and F(120, 9) == F(40, 3)
Q(T, "Work efficiency", B,
  "12 men can complete a job in 10 days. They start together, but after 4 days 3 of them leave. In how many days in "
  "all is the job completed?",
  "12 days", ["8 days", "13⅓ days", "10 days"],
  "Count the work in man-days: total = 12 × 10 = 120",
  "In the first 4 days 12 men do 48 man-days of work, leaving 72. The remaining 9 men need 72 ÷ 9 = 8 more days, so the "
  "job takes 4 + 8 = 12 days in all.",
  ["Total = 120 man-days", "Done in 4 days = 48", "Left = 72 ⇒ 72 ÷ 9 = 8 days", "Total = 4 + 8 = 12 days"],
  why="8 days is only the time after the 3 men leave; 13⅓ days assumes 9 men worked from the start (120 ÷ 9); "
      "10 days is the original plan.", secs=45)

costs = {"A alone": 12 * 600, "B alone": 18 * 450, "Both": 1 / (F(1, 12) + F(1, 18)) * (600 + 450)}
assert costs == {"A alone": 7200, "B alone": 8100, "Both": 7560} and min(costs.values()) == 7200
assert F(7200 + 8100, 2) == 7650
Q(T, "Work and wages", I,
  "A can finish a job in 12 days and is paid ₹600 a day; B can finish it in 18 days and is paid ₹450 a day. Payment "
  "is only for the days worked. What is the least total wage at which the job can be finished — by A alone, B alone "
  "or both together?",
  "₹7,200", ["₹7,560", "₹8,100", "₹7,650"],
  "Compare the total cost of each option: days needed × daily wage",
  "A alone: 12 × 600 = ₹7,200. B alone: 18 × 450 = ₹8,100. Together they need 1 ÷ (1/12 + 1/18) = 7.2 days at ₹1,050 a "
  "day = ₹7,560. The least is ₹7,200 (A alone).",
  ["A alone: 12 × 600 = 7,200", "B alone: 18 × 450 = 8,100", "Together: 7.2 days × 1,050 = 7,560", "Least = 7,200"],
  short="A's cost per whole job (₹7,200) is lower than B's (₹8,100), so any share of B's work only adds cost.",
  why="₹7,560 is the cost of both working together; ₹8,100 is B alone; ₹7,650 averages the two single costs.",
  secs=65)

man, woman, child = 4, 2, 1
total = (2 * man + 3 * woman + 4 * child) * 6
d_ = F(total, man + woman + child)
assert total == 108 and d_ == F(108, 7) and F(108, 9) == 12 and F((2 * 2 + 3 * 2 + 4) * 6, 5) == F(84, 5)
Q(T, "Men-women-children", I,
  "A man works twice as fast as a woman, and a woman works twice as fast as a child. 2 men, 3 women and 4 children "
  "together finish a job in 6 days. How long will 1 man, 1 woman and 1 child take to finish it together?",
  "15 3/7 days", ["18 days", "16.8 days", "12 days"],
  "Convert everyone to child-units: man = 4, woman = 2, child = 1",
  "The group does 2 × 4 + 3 × 2 + 4 × 1 = 18 units a day, so the job is 18 × 6 = 108 units. One man, one woman and one "
  "child do 4 + 2 + 1 = 7 units a day and need 108 ÷ 7 = 15 3/7 days.",
  ["Man = 4, woman = 2, child = 1 units/day", "Group = 18 units/day ⇒ job = 108 units", "Trio = 7 units/day",
   "108 ÷ 7 = 15 3/7 days"],
  why="18 days counts heads (9 people against 3) and ignores efficiency; 16.8 days takes a man as equal to a woman "
      "(both 2 units); 12 days divides 108 by the 9 people of the group.", secs=70)

sol = [a for a in range(1, 50) if F(1, a) + F(1, a + 6) == F(1, 4)]
assert sol == [6]
Q(T, "Work efficiency", I,
  "A takes 6 days less than B to finish a job alone. Working together, they finish it in 4 days. How many days does A "
  "alone take?",
  "6 days", ["12 days", "8 days", "10 days"],
  "Let A take a days and B take a + 6 days; their one-day works add to 1/4",
  "1/a + 1/(a + 6) = 1/4 gives 4(2a + 6) = a(a + 6), i.e. a² − 2a − 24 = 0, so (a − 6)(a + 4) = 0 and a = 6 (a "
  "number of days cannot be negative). B takes 12 days.",
  ["1/a + 1/(a + 6) = 1/4", "a² − 2a − 24 = 0", "(a − 6)(a + 4) = 0 ⇒ a = 6"],
  short="Try the options: 1/6 + 1/12 = 3/12 = 1/4 ✓.",
  why="12 days is B's time; 8 days assumes A and B are equally fast (2 × 4); 10 days adds the 6-day gap to the joint "
      "time.", secs=60, by=BRUTE)

done_mh = 30 * 20 * 8
total_mh = done_mh * F(8, 3)
need = (total_mh - done_mh) / (20 * 10)
assert done_mh == 4800 and total_mh == 12800 and need == 40 and need - 30 == 10
assert (total_mh - done_mh) / (20 * 8) - 30 == 20 and (30 * 40 * 8 * F(5, 8)) / 200 == 30
Q(T, "Work efficiency", A,
  "A contractor plans to finish a road in 40 days with 30 workers working 8 hours a day. After 20 days only 3/8 of the "
  "road is complete. From then on everyone works 10 hours a day. How many more workers must he employ to finish on "
  "time? (All workers work at the same rate.)",
  "10", ["20", "40", "0"],
  "Measure the work in man-hours from what was actually achieved, not from the plan",
  "In 20 days, 30 × 20 × 8 = 4,800 man-hours produced 3/8 of the road, so the whole road needs 12,800 man-hours and "
  "8,000 remain. The remaining 20 days at 10 hours give 200 hours, so 8,000 ÷ 200 = 40 workers are needed: 10 more.",
  ["Done: 4,800 man-hours = 3/8", "Whole = 12,800 man-hours", "Remaining = 8,000", "Hours left = 20 × 10 = 200",
   "Workers = 40 ⇒ 10 more"],
  why="20 keeps the 8-hour day (8,000 ÷ 160 = 50 workers); 40 is the total number of workers needed, not the extra; 0 "
      "trusts the original plan of 9,600 man-hours instead of the actual progress.", secs=100)

# ================================================================ Pipes and Cisterns (B1 I2 A1)
T = "Pipes and Cisterns"
o_ = 1 / (F(1, 6) - F(1, 10))
assert o_ == 15 and 1 / (F(1, 6) + F(1, 10)) == F(15, 4)
Q(T, "Inlet and outlet", B,
  "Two pipes together fill a tank in 6 hours. One of them alone fills it in 10 hours. How long does the other pipe "
  "alone take to fill it?",
  "15 hours", ["4 hours", "16 hours", "3.75 hours"],
  "Rate of the second pipe = joint rate − rate of the first",
  "Together the pipes fill 1/6 of the tank an hour and the first fills 1/10, so the second fills 1/6 − 1/10 = 1/15 an "
  "hour and needs 15 hours.",
  ["1/6 − 1/10 = 5/30 − 3/30 = 2/30 = 1/15", "15 hours"],
  why="4 hours subtracts the times; 16 hours adds them; 3.75 hours adds the two rates (the time if the 6-hour and "
      "10-hour figures were two separate pipes).", secs=35)

done = F(3, 12)
t_ = (1 - done) / (F(1, 12) + F(1, 18))
assert t_ == F(27, 5) and 3 + t_ == F(42, 5) and 1 / (F(1, 12) + F(1, 18)) == F(36, 5)
Q(T, "Inlet and outlet", I,
  "Pipe A can fill a tank in 12 hours and pipe B in 18 hours. A is opened on the empty tank, and 3 hours later B is "
  "also opened. How long does it take in all to fill the tank?",
  "8 hours 24 minutes", ["7 hours 12 minutes", "5 hours 24 minutes", "8 hours 40 minutes"],
  "Work out the part filled by A alone, then the time for both pipes to fill the rest",
  "In 3 hours A fills 3/12 = 1/4. Together A and B fill 1/12 + 1/18 = 5/36 an hour, so the remaining 3/4 takes "
  "3/4 ÷ 5/36 = 5.4 hours. Total = 3 + 5.4 = 8.4 hours = 8 hours 24 minutes.",
  ["A alone, 3 h: 1/4", "Joint rate = 5/36 per hour", "3/4 ÷ 5/36 = 5.4 h", "Total = 8.4 h = 8 h 24 min"],
  why="7 hours 12 minutes assumes both pipes ran from the start; 5 hours 24 minutes is only the time after B is "
      "opened; 8 hours 40 minutes reads 0.4 hour as 40 minutes.", secs=60)

t3 = F(36) * F(2, 3) ** 2
assert t3 == 16 and F(36) * F(2, 3) == 24 and F(36) * F(3, 2) == 54 and F(36) * F(2, 3) ** 3 == F(32, 3)
Q(T, "Inlet and outlet", I,
  "The rate at which water flows through a pipe is proportional to the area of its circular cross-section (assume the "
  "same water speed). A pipe of diameter 2 cm fills a tank in 36 minutes. How long will a pipe of diameter 3 cm take "
  "to fill the same tank?",
  "16 minutes", ["24 minutes", "54 minutes", "10⅔ minutes"],
  "Cross-section area ∝ diameter², and time ∝ 1 ÷ rate",
  "The area grows by (3/2)² = 9/4, so the flow rate is 9/4 times as fast and the time is 36 × 4/9 = 16 minutes.",
  ["Rate ∝ d²: (3/2)² = 9/4", "Time ∝ 1/rate", "36 × 4/9 = 16 minutes"],
  why="24 minutes takes the rate as proportional to the diameter; 54 minutes multiplies by 3/2 as if a wider pipe "
      "were slower; 10⅔ minutes uses the cube of the diameter ratio.", secs=55)

level, t_ = F(0), 0
while True:
    t_ += 1
    level += F(1, 6) if t_ % 2 == 1 else -F(1, 9)
    if level >= 1:
        break
assert t_ == 31 and level == 1 and 1 / (F(1, 6) - F(1, 9)) == 18 and 15 * (F(1, 6) - F(1, 9)) == F(5, 6)
Q(T, "Inlet and outlet", A,
  "Pipe A fills a tank in 6 hours and pipe B empties the full tank in 9 hours. Starting with the tank empty, A and B "
  "are opened alternately for one hour each, beginning with A. After how many hours will the tank first be full?",
  "31 hours", ["18 hours", "36 hours", "30 hours"],
  "Each 2-hour cycle adds 1/6 − 1/9 = 1/18; stop as soon as A's hour can top the tank up",
  "Each A–B cycle adds 1/18. The tank is full when A's hour starts with at least 1 − 1/6 = 5/6 in it. After 15 cycles "
  "(30 hours) the tank holds 15/18 = 5/6, and in the 31st hour A adds 1/6. So it is full after 31 hours.",
  ["Net per 2 hours = 1/18", "Need 5/6 before an A-hour", "15 cycles = 30 h ⇒ 5/6", "31st hour: + 1/6 ⇒ full"],
  why="18 hours keeps both pipes open together all the time; 36 hours forgets that the tank fills during A's hour, "
      "before B can empty it; 30 hours stops when the tank is only 5/6 full.", secs=100, by=BRUTE)

# ================================================================ Speed, Time and Distance (B1 I2 A2)
T = "Speed, Time and Distance"
v = F(12 + 18) / (F(40 + 50, 60))
assert v == 20 and F(12, F(40, 60)) == 18 and F(18, F(50, 60)) == F(108, 5) and (18 + F(108, 5)) / 2 == F(198, 10)
Q(T, "Average speed", B,
  "A cyclist covers 12 km in 40 minutes and the next 18 km in 50 minutes. What is the average speed for the whole "
  "ride?",
  "20 km/h", ["19.8 km/h", "18 km/h", "21.6 km/h"],
  "Average speed = total distance ÷ total time",
  "Total distance = 30 km and total time = 90 minutes = 1.5 hours, so the average speed = 30 ÷ 1.5 = 20 km/h.",
  ["Distance = 12 + 18 = 30 km", "Time = 40 + 50 = 90 min = 1.5 h", "30 ÷ 1.5 = 20 km/h"],
  why="19.8 km/h averages the two section speeds (18 and 21.6 km/h) instead of using total distance ÷ total time; "
      "18 km/h and 21.6 km/h are the speeds of the two sections alone.", secs=40)

stop = F(54 - 45, 54) * 60
assert stop == 10 and F(9, 45) * 60 == 12 and F(45, 54) * 60 == 50
Q(T, "Average speed", I,
  "Excluding stoppages, a bus runs at 54 km/h; including stoppages, its average speed is 45 km/h. For how many "
  "minutes does the bus stop per hour?",
  "10 minutes", ["9 minutes", "12 minutes", "50 minutes"],
  "In each hour the bus loses 54 − 45 = 9 km; find the time it would need to run those 9 km",
  "Because of stoppages the bus covers 9 km less per hour. At 54 km/h, 9 km takes 9/54 hour = 10 minutes, so it stops "
  "10 minutes per hour.",
  ["Lost distance = 54 − 45 = 9 km per hour", "Time for 9 km at 54 km/h = 9/54 h", "= 10 minutes"],
  why="9 minutes reads the 9 km as minutes; 12 minutes divides 9 by 45 instead of 54; 50 minutes is the running time "
      "per hour.", secs=50)

t_ = F(30, 50 - 40)
d_ = (50 + 40) * t_
assert t_ == 3 and d_ == 270 and 50 * t_ == 150 and 40 * t_ == 120
Q(T, "Meeting and overtaking", I,
  "Two cars start at the same time from towns X and Y and drive towards each other at 50 km/h and 40 km/h. When they "
  "meet, the faster car has travelled 30 km more than the slower one. How far apart are X and Y?",
  "270 km", ["150 km", "120 km", "90 km"],
  "The faster car gains 50 − 40 = 10 km every hour, which tells you the travel time",
  "The gap between their distances grows by 10 km each hour, so a 30 km gap means they met after 3 hours. In 3 hours "
  "they cover (50 + 40) × 3 = 270 km together, which is the distance XY.",
  ["Extra distance per hour = 10 km", "30 ÷ 10 = 3 hours", "XY = 90 × 3 = 270 km"],
  why="150 km is only the faster car's distance; 120 km is only the slower car's; 90 km is one hour of travel.",
  secs=55)

ok_ = []
for d in range(13, 80):
    for va, vb in [(F(12), F(d - 12)), (F(24), F(2 * (d - 12)))]:
        # times of second meeting: A's position after first meeting, both reverse at the ends
        ta = F(12) / va  # time to first meeting
        assert near(F(d - 12) / vb, ta)
        # second meeting happens when combined distance = 3d; A then has covered 3 × 12 = 36
        a_dist = va * (3 * d / (va + vb))
        if a_dist - d == 8 and 3 * d - a_dist - d == d - 8:
            ok_.append(d)
assert set(ok_) == {28} and 3 * 12 - 8 == 28 and 3 * 12 + 8 == 44
Q(T, "Meeting and overtaking", A,
  "A and B start at the same time from towns P and Q and walk towards each other at constant speeds. They first meet "
  "12 km from P. Each continues to the other town, turns back at once, and they meet again 8 km from Q. What is the "
  "distance between P and Q?",
  "28 km", ["20 km", "36 km", "44 km"],
  "By the second meeting the two together have covered three times the distance PQ, so each has walked three times "
  "his distance to the first meeting",
  "At the first meeting they have together covered PQ, and A has walked 12 km. By the second meeting they have "
  "together covered 3 × PQ, so A has walked 3 × 12 = 36 km. A has gone from P to Q and come back 8 km, i.e. PQ + 8 = "
  "36, so PQ = 28 km.",
  ["First meeting: total = PQ, A = 12 km", "Second meeting: total = 3PQ, A = 36 km", "A walked PQ + 8 = 36",
   "PQ = 28 km"],
  why="20 km adds 12 and 8; 36 km is the distance A walks before the second meeting; 44 km adds 8 instead of "
      "subtracting it (36 + 8).", secs=100, by=BRUTE)

d_ = 1 / (F(1, 5) - F(1, 6)) * F(10, 60)
t_on = d_ / 5 - F(6, 60)
sp = d_ / t_on
assert d_ == 5 and t_on == F(9, 10) and sp == F(50, 9) and F(2 * 5 * 6, 11) == F(60, 11)
assert d_ / (d_ / 5 + F(6, 60)) == F(50, 11)
Q(T, "Average speed", A,
  "Walking at 5 km/h, a man reaches his office 6 minutes late; walking at 6 km/h, he reaches 4 minutes early. At what "
  "speed should he walk to reach exactly on time?",
  "5 5/9 km/h", ["5.5 km/h", "5 5/11 km/h", "4 6/11 km/h"],
  "The two times differ by 10 minutes; find the distance, then the exact time available",
  "d/5 − d/6 = 10/60 gives d/30 = 1/6, so d = 5 km. At 5 km/h he takes 1 hour, which is 6 minutes late, so the time "
  "available is 54 minutes = 0.9 hour. Required speed = 5 ÷ 0.9 = 50/9 = 5 5/9 km/h.",
  ["d/5 − d/6 = 1/6 h ⇒ d = 5 km", "Time at 5 km/h = 60 min (6 min late)", "On-time = 54 min = 0.9 h",
   "Speed = 5 ÷ 0.9 = 5 5/9 km/h"],
  why="5.5 km/h averages the two speeds; 5 5/11 km/h is their harmonic mean (equal distances), which does not fit "
      "these times; 4 6/11 km/h adds the 6 minutes instead of subtracting them (5 ÷ 1.1).", secs=90)

# ================================================================ Boats and Streams (B1 I1 A1)
T = "Boats and Streams"
dn, up = F(32, 2), F(24, 3)
assert (dn, up) == (16, 8) and (dn + up) / 2 == 12 and (dn - up) / 2 == 4
Q(T, "Upstream and downstream", B,
  "A boat covers 32 km downstream in 2 hours and 24 km upstream in 3 hours. What is its speed in still water?",
  "12 km/h", ["4 km/h", "24 km/h", "8 km/h"],
  "Boat speed = (downstream speed + upstream speed) ÷ 2",
  "Downstream speed = 32 ÷ 2 = 16 km/h; upstream speed = 24 ÷ 3 = 8 km/h. Boat speed = (16 + 8) ÷ 2 = 12 km/h.",
  ["Downstream = 16 km/h", "Upstream = 8 km/h", "(16 + 8) ÷ 2 = 12 km/h"],
  why="4 km/h is the speed of the stream; 24 km/h adds the two speeds and forgets to halve; 8 km/h is the upstream "
      "speed.", secs=35)

d_ = 1 / (1 / F(72, 10) + 1 / F(48, 10))
assert d_ == F(288, 100) and F(72, 10) / 2 == F(36, 10) and F(48, 10) / 2 == F(24, 10)
Q(T, "Upstream and downstream", I,
  "A man can row at 6 km/h in still water. When the stream flows at 1.2 km/h, it takes him 1 hour to row to a place "
  "and come back. How far is the place?",
  "2.88 km", ["3 km", "3.6 km", "2.4 km"],
  "Time downstream + time upstream = 1 hour, with speeds 7.2 and 4.8 km/h",
  "d/7.2 + d/4.8 = 1. The LCM approach: d × (4.8 + 7.2)/(7.2 × 4.8) = 1, so d = 34.56 ÷ 12 = 2.88 km.",
  ["Downstream = 7.2 km/h, upstream = 4.8 km/h", "d/7.2 + d/4.8 = 1", "d = 7.2 × 4.8 ÷ 12 = 2.88 km"],
  short="Distance = (u × v) ÷ (u + v) × total time = 34.56 ÷ 12 = 2.88 km.",
  why="3 km ignores the stream (half an hour each way at 6 km/h); 3.6 km uses the downstream speed for half an hour; "
      "2.4 km uses the upstream speed for half an hour.", secs=60)

d_ = F(24)
s_ = (d_ / 4 - d_ / 6) / 2
assert d_ / s_ == 24 and d_ / (d_ / 4 - d_ / 6) == 12 and near(F(2 * 4 * 6, 10), 4.8)
Q(T, "Speed of stream", A,
  "A boat goes from A to B downstream in 4 hours and returns from B to A in 6 hours. How long would a log take to float "
  "from A to B with the stream?",
  "24 hours", ["12 hours", "10 hours", "4.8 hours"],
  "Stream speed = (downstream speed − upstream speed) ÷ 2; a log moves at the stream's speed",
  "Let AB = d. Downstream speed = d/4 and upstream speed = d/6, so the stream speed = (d/4 − d/6) ÷ 2 = d/24. The log "
  "takes d ÷ (d/24) = 24 hours.",
  ["Downstream = d/4, upstream = d/6", "Stream = (d/4 − d/6) ÷ 2 = d/24", "Log time = 24 hours"],
  short="Take AB = 24 km: downstream 6 km/h, upstream 4 km/h, stream 1 km/h, log 24 hours.",
  why="12 hours forgets to halve the difference of the speeds; 10 hours adds the two times; 4.8 hours is the harmonic "
      "mean of 4 and 6, which has nothing to do with the stream.", secs=80)

# ================================================================ Problems on Trains (B1 I1 A1)
T = "Problems on Trains"
v_ = F(72 * 5, 18)
assert v_ == 20 and F(360 + 140) / v_ == 25 and F(360) / v_ == 18 and F(140) / v_ == 7 and near(F(500, 72), 6.94, 0.01)
Q(T, "Crossing a pole or platform", B,
  "A 360 m long train running at 72 km/h passes a 140 m long goods train standing on a parallel track. How long does "
  "it take to pass the goods train completely?",
  "25 seconds", ["18 seconds", "7 seconds", "6.94 seconds"],
  "A standing train is like a platform: distance = sum of the two lengths",
  "72 km/h = 20 m/s. Distance = 360 + 140 = 500 m. Time = 500 ÷ 20 = 25 seconds.",
  ["72 × 5/18 = 20 m/s", "500 m ÷ 20 m/s = 25 s"],
  why="18 seconds counts only the moving train's length; 7 seconds counts only the goods train's length; 6.94 seconds "
      "divides 500 m by 72 without converting km/h to m/s.", secs=40)

L_ = F(60)
t_ = 2 * L_ / (L_ / 10 + L_ / 15)
assert t_ == 12 and 1 / (F(1, 10) + F(1, 15)) == 6
Q(T, "Trains crossing each other", I,
  "Two trains of equal length take 10 seconds and 15 seconds respectively to pass a telegraph post. If they run in "
  "opposite directions on parallel tracks, how long will they take to cross each other completely?",
  "12 seconds", ["12.5 seconds", "25 seconds", "6 seconds"],
  "Let each length be L: speeds are L/10 and L/15; crossing distance = 2L at the sum of the speeds",
  "Time = 2L ÷ (L/10 + L/15) = 2L ÷ (L/6) = 12 seconds.",
  ["Speeds: L/10 and L/15", "Relative speed (opposite) = L/6", "Distance = 2L", "Time = 2L ÷ L/6 = 12 s"],
  why="12.5 seconds averages the two times; 25 seconds adds them; 6 seconds forgets that the distance is both lengths "
      "(L ÷ L/6).", secs=55)

rel = F((72 - 36) * 5, 18)
L1 = rel * 18
L2 = rel * 30 - L1
assert rel == 10 and L1 == 180 and L2 == 120 and F((72 + 36) * 5, 18) * 30 - F((72 + 36) * 5, 18) * 18 == 360
Q(T, "Trains crossing each other", A,
  "A fast train running at 72 km/h overtakes a slow train running at 36 km/h on a parallel track in the same "
  "direction. It passes the slow train completely in 30 seconds, and a passenger sitting in the slow train sees the "
  "fast train go past him in 18 seconds. What is the length of the slow train?",
  "120 m", ["180 m", "300 m", "360 m"],
  "Relative speed (same direction) = 72 − 36 = 36 km/h = 10 m/s; the passenger is a point, so 18 s gives the fast "
  "train's length alone",
  "Relative speed = 10 m/s. Passing the passenger: fast train's length = 10 × 18 = 180 m. Passing the whole slow "
  "train: both lengths = 10 × 30 = 300 m. So the slow train is 300 − 180 = 120 m long.",
  ["Relative speed = 36 km/h = 10 m/s", "Fast train = 10 × 18 = 180 m", "Both = 10 × 30 = 300 m",
   "Slow train = 120 m"],
  why="180 m is the fast train's length; 300 m is the two lengths together; 360 m adds the speeds although the trains "
      "move the same way (30 m/s × 12 s).", secs=90)

# ================================================================ Mensuration (B2 I2 A1)
T = "Mensuration"
ar = F(18 + 12, 2) * 8
assert ar == 120 and 2 * ar == 240 and 18 * 8 == 144 and 12 * 8 == 96
Q(T, "2D areas and perimeters", B,
  "The parallel sides of a trapezium are 18 cm and 12 cm, and the distance between them is 8 cm. What is its area?",
  "120 cm²", ["240 cm²", "144 cm²", "96 cm²"],
  "Area of a trapezium = ½ × (sum of the parallel sides) × height",
  "Area = ½ × (18 + 12) × 8 = ½ × 30 × 8 = 120 cm².",
  ["Sum of parallel sides = 30 cm", "½ × 30 × 8 = 120 cm²"],
  why="240 cm² forgets the ½; 144 cm² uses only the longer side (18 × 8); 96 cm² uses only the shorter side (12 × 8).",
  secs=30)

pi = F(22, 7)
per = pi * 14 + 28
assert per == 72 and pi * 14 == 44 and 2 * pi * 14 == 88 and pi * 14 + 14 == 58
Q(T, "2D areas and perimeters", B,
  "What is the perimeter of a semicircular plate of radius 14 cm? (Use π = 22/7.)",
  "72 cm", ["44 cm", "88 cm", "58 cm"],
  "Perimeter of a semicircle = half the circumference + the diameter = πr + 2r",
  "πr = 22/7 × 14 = 44 cm, and the straight edge is the diameter, 28 cm. Perimeter = 44 + 28 = 72 cm.",
  ["Curved part = πr = 44 cm", "Diameter = 28 cm", "44 + 28 = 72 cm"],
  why="44 cm leaves out the straight edge; 88 cm is the full circle's circumference; 58 cm adds the radius instead of "
      "the diameter.", secs=35)

sec = F(120, 360) * pi * 21 * 21
assert sec == 462 and pi * 441 == 1386 and F(120, 360) * 2 * pi * 21 == 44 and F(60, 360) * pi * 441 == 231
Q(T, "2D areas and perimeters", I,
  "What is the area of a sector of a circle of radius 21 cm whose central angle is 120°? (Use π = 22/7.)",
  "462 cm²", ["1,386 cm²", "44 cm²", "231 cm²"],
  "Sector area = (θ/360°) × πr²",
  "πr² = 22/7 × 441 = 1,386 cm². A 120° sector is one-third of the circle: 1,386 ÷ 3 = 462 cm².",
  ["πr² = 1,386 cm²", "120/360 = 1/3", "Sector = 462 cm²"],
  why="1,386 cm² is the whole circle; 44 cm is the arc length, not an area; 231 cm² uses 60° instead of 120°.",
  secs=50)

r_ = F(1320) / (2 * pi * 15)
vol = pi * r_ * r_ * 15
assert r_ == 14 and vol == 9240 and vol / 3 == 3080 and pi * 28 * 28 * 15 == 36960 and 1320 * 15 == 19800
Q(T, "Cylinder, cone and sphere", I,
  "The curved surface area of a right circular cylinder is 1,320 cm² and its height is 15 cm. What is its volume? "
  "(Use π = 22/7.)",
  "9,240 cm³", ["3,080 cm³", "36,960 cm³", "19,800 cm³"],
  "Find the radius from CSA = 2πrh, then use V = πr²h",
  "2 × 22/7 × r × 15 = 1,320 gives r = 1,320 × 7 ÷ 660 = 14 cm. Volume = 22/7 × 14² × 15 = 22/7 × 196 × 15 = "
  "9,240 cm³.",
  ["2πrh = 1,320 ⇒ r = 14 cm", "V = 22/7 × 196 × 15", "= 9,240 cm³"],
  why="3,080 cm³ uses the cone formula (one-third); 36,960 cm³ uses the diameter 28 cm as the radius; 19,800 cm³ "
      "multiplies the curved surface area by the height.", secs=65)

h_ = F(4, 3) * (6 ** 3 - 4 ** 3) / 4 ** 2
assert h_ == F(38, 3) and F(4, 3) * 216 / 16 == 18 and F(4, 3) * 64 / 16 == F(16, 3) and F(152, 16) == F(19, 2)
Q(T, "Cylinder, cone and sphere", A,
  "A hollow metal sphere has an external radius of 6 cm and an internal radius of 4 cm. It is melted and recast into "
  "a solid cylinder of base radius 4 cm. What is the height of the cylinder?",
  "12⅔ cm", ["18 cm", "5⅓ cm", "9.5 cm"],
  "Volume of metal in a hollow sphere = 4/3 π (R³ − r³); equate it to πr²h (π cancels)",
  "Metal = 4/3 π (216 − 64) = 4/3 π × 152 = 608π/3 cm³. Cylinder: π × 16 × h. So h = 608/(3 × 16) = 38/3 = 12⅔ cm.",
  ["Metal = 4/3 π (6³ − 4³) = 608π/3", "Cylinder = 16πh", "h = 608/48 = 12⅔ cm"],
  why="18 cm uses the whole outer sphere (ignores the hollow); 5⅓ cm uses only the inner sphere; 9.5 cm forgets the "
      "4/3 in the sphere's volume (152/16).", secs=90)

# ================================================================ Probability (B3 I3 A1)
T = "Probability"
toss = list(itertools.product("HT", repeat=2))
p_ = F(sum(1 for t in toss if t.count("H") <= 1), 4)
assert p_ == F(3, 4)
Q(T, "Coins and dice", B, "Two fair coins are tossed together. What is the probability of getting at most one head?",
  "3/4", ["1/4", "1/2", "2/3"],
  "List the 4 equally likely outcomes: HH, HT, TH, TT",
  "At most one head means 0 or 1 head: HT, TH and TT — 3 of the 4 outcomes. Probability = 3/4.",
  ["Outcomes: HH, HT, TH, TT", "At most one head: HT, TH, TT", "P = 3/4"],
  why="1/4 is the probability of two heads; 1/2 counts only exactly one head; 2/3 treats 'no head, one head, two "
      "heads' as three equally likely outcomes.", secs=30, by=BRUTE)

die = range(1, 7)
p_ = F(sum(1 for d in die if d > 4 or d % 2 == 0), 6)
assert p_ == F(2, 3)
Q(T, "Coins and dice", B,
  "A fair die is rolled once. What is the probability that the number shown is greater than 4 or is even?",
  "2/3", ["5/6", "1/2", "1/3"],
  "P(A or B) = P(A) + P(B) − P(A and B); here count the favourable faces directly",
  "Greater than 4: 5, 6. Even: 2, 4, 6. Together: 2, 4, 5, 6 — 4 faces. Probability = 4/6 = 2/3.",
  ["> 4: {5, 6}", "Even: {2, 4, 6}", "Union: {2, 4, 5, 6}", "P = 4/6 = 2/3"],
  why="5/6 adds 2/6 and 3/6 without removing the 6 counted twice; 1/2 counts only the even numbers; 1/3 counts only "
      "the numbers greater than 4.", secs=35, by=BRUTE)

balls = ["W"] * 6 + ["K"] * 4
pairs = list(itertools.combinations(range(10), 2))
p_ = F(sum(1 for a, b in pairs if balls[a] == balls[b] == "W"), len(pairs))
assert p_ == F(1, 3) and F(6, 10) ** 2 == F(9, 25) and F(math.comb(4, 2), 45) == F(2, 15)
Q(T, "Balls from bags", B,
  "A bag contains 6 white and 4 black balls. Two balls are drawn at random together. What is the probability that "
  "both are white?",
  "1/3", ["9/25", "3/5", "2/15"],
  "P = (ways to choose 2 white) ÷ (ways to choose any 2) = ⁶C₂ ÷ ¹⁰C₂",
  "⁶C₂ = 15 and ¹⁰C₂ = 45, so the probability is 15/45 = 1/3.",
  ["⁶C₂ = 15", "¹⁰C₂ = 45", "P = 15/45 = 1/3"],
  why="9/25 draws with replacement (6/10 × 6/10); 3/5 is the chance for one white ball only; 2/15 is the probability "
      "that both are black.", secs=40, by=BRUTE)

deck = [(r, s) for r in range(13) for s in "SHDC"]
p_ = F(sum(1 for r, s in deck if s != "H" and r != 12), 52)
assert p_ == F(9, 13) and F(39, 52) == F(3, 4) and F(48, 52) == F(12, 13)
Q(T, "Cards", I,
  "One card is drawn at random from a well-shuffled pack of 52 cards. What is the probability that it is neither a "
  "heart nor a king?",
  "9/13", ["3/4", "35/52", "12/13"],
  "Count hearts or kings without double-counting the king of hearts, then take the complement",
  "Hearts = 13 and kings = 4, but the king of hearts is in both, so 16 cards are a heart or a king. The rest, 36 cards, "
  "are neither: 36/52 = 9/13.",
  ["Hearts or kings = 13 + 4 − 1 = 16", "Neither = 52 − 16 = 36", "P = 36/52 = 9/13"],
  why="3/4 removes only the hearts; 35/52 removes 13 + 4 = 17 cards, counting the king of hearts twice; 12/13 removes "
      "only the kings.", secs=50, by=BRUTE)

kids = list(itertools.product("BG", repeat=3))
p_ = F(sum(1 for k in kids if "B" in k and "G" in k), 8)
assert p_ == F(3, 4) and F(sum(1 for k in kids if "B" in k), 8) == F(7, 8) and F(sum(1 for k in kids if k.count("B") == 2), 8) == F(3, 8)
Q(T, "Coins and dice", I,
  "A family has three children. Assuming each child is equally likely to be a boy or a girl, independently of the "
  "others, what is the probability that the family has at least one boy and at least one girl?",
  "3/4", ["7/8", "3/8", "1/2"],
  "The complement of 'at least one of each' is 'all boys or all girls'",
  "There are 2³ = 8 equally likely outcomes. Only BBB and GGG fail, so the probability is 1 − 2/8 = 3/4.",
  ["Total outcomes = 8", "All boys or all girls = 2", "P = 1 − 2/8 = 3/4"],
  why="7/8 is the probability of at least one boy only; 3/8 is the probability of exactly two boys; 1/2 assumes the "
      "two kinds of mixed family are the only outcomes.", secs=55, by=BRUTE)

pairs = list(itertools.combinations(range(1, 21), 2))
p_ = F(sum(1 for a, b in pairs if (a + b) % 2 == 0), len(pairs))
assert p_ == F(9, 19) and F(math.comb(10, 2), 190) == F(9, 38)
Q(T, "Balls from bags", I,
  "A box contains 20 balls numbered 1 to 20. Two balls are drawn at random together. What is the probability that the "
  "sum of their numbers is even?",
  "9/19", ["1/2", "9/38", "10/19"],
  "An even sum needs two even numbers or two odd numbers",
  "There are 10 odd and 10 even numbers. Both even: ¹⁰C₂ = 45; both odd: 45. Favourable = 90 out of ²⁰C₂ = 190, so "
  "P = 90/190 = 9/19.",
  ["²⁰C₂ = 190", "Both even = 45, both odd = 45", "P = 90/190 = 9/19"],
  why="1/2 treats the two draws as independent (with replacement); 9/38 counts only the both-even case; 10/19 is the "
      "probability of an odd sum.", secs=60, by=BRUTE)

pa = F(0)
for k in range(0, 200):
    pa += F(5, 6) ** (2 * k) * F(1, 6)
assert near(pa, F(6, 11), 1e-12) and F(1, 6) / (1 - F(25, 36)) == F(6, 11)
Q(T, "Coins and dice", A,
  "A and B take turns to throw a fair die, A throwing first. The first person to throw a six wins. What is the "
  "probability that A wins?",
  "6/11", ["1/2", "1/6", "5/11"],
  "A wins on throw 1, 3, 5, …: add a geometric series with ratio (5/6)²",
  "P(A) = 1/6 + (5/6)²(1/6) + (5/6)⁴(1/6) + … = (1/6) ÷ (1 − 25/36) = (1/6) × 36/11 = 6/11.",
  ["A wins on his 1st throw: 1/6", "Each later chance needs two misses first: × 25/36", "Sum = (1/6)/(11/36)",
   "= 6/11"],
  why="1/2 ignores A's advantage of throwing first; 1/6 counts only A's first throw; 5/11 is B's probability of "
      "winning.", secs=90)

# ================================================================ Permutation and Combination (B1 I1 A1)
T = "Permutation and Combination"
assert math.perm(11, 2) == 110 and math.comb(11, 2) == 55
Q(T, "Arrangements", B,
  "In how many ways can a captain and a vice-captain be chosen from a team of 11 players?",
  "110", ["55", "121", "22"],
  "Order matters (the two posts are different): ¹¹P₂ = 11 × 10",
  "The captain can be any of 11 players and the vice-captain any of the remaining 10, so there are 11 × 10 = 110 ways.",
  ["Captain: 11 choices", "Vice-captain: 10 choices", "11 × 10 = 110"],
  why="55 = ¹¹C₂ ignores that the two posts are different; 121 lets the same player hold both posts; 22 adds 11 + 11 "
      "instead of multiplying.", secs=30, by=BRUTE)

words = {p for p in itertools.permutations("ACCOUNT") if p[0] == "A" and p[-1] == "T"}
assert len(words) == 60 and math.factorial(7) // 2 == 2520
Q(T, "Word arrangements", I,
  "How many different arrangements of the letters of the word ACCOUNT begin with A and end with T?",
  "60", ["120", "2,520", "30"],
  "Fix the end letters; arrange the middle letters, dividing by the factorial of any repeated letter",
  "With A first and T last, the middle five letters are C, C, O, U, N, with C repeated. Arrangements = 5!/2! = 120/2 "
  "= 60.",
  ["Fix A and T", "Middle: C, C, O, U, N", "5!/2! = 60"],
  why="120 forgets that the two C's are identical; 2,520 = 7!/2! counts all arrangements of ACCOUNT; 30 divides by 2 "
      "twice.", secs=50, by=BRUTE)

inc_ = [n for n in range(100, 1000) if str(n)[0] < str(n)[1] < str(n)[2]]
assert len(inc_) == 84 == math.comb(9, 3) and math.comb(10, 3) == 120 and math.comb(11, 3) == 165
Q(T, "Selections", A,
  "How many three-digit numbers have their digits in strictly increasing order from left to right (for example 147)?",
  "84", ["120", "504", "165"],
  "Any 3 different non-zero digits can be written in increasing order in exactly one way",
  "0 cannot appear: it cannot be the first digit and cannot follow a larger digit. So choose any 3 of the digits 1–9: "
  "⁹C₃ = 84, and each choice gives exactly one number.",
  ["0 is impossible", "Choose 3 digits from 1–9: ⁹C₃", "= 84"],
  why="120 = ¹⁰C₃ wrongly allows the digit 0; 504 = 9 × 8 × 7 counts every order of three different digits; 165 = "
      "¹¹C₃ counts digits that may repeat (non-decreasing).", secs=80, by=BRUTE)

# ================================================================ Tabular DI (B1 I3 A3): sets of 4 and 3
T = "Tabular DI"
PAY = {"Grocery": (2400, 350), "Pharmacy": (1500, 480), "Fuel": (1800, 900), "Restaurants": (1200, 700),
       "Electronics": (300, 6400)}
sid = stimulus("data_table", "Digital payments received by five merchant categories in a market in one week",
               "The table shows, for five categories of merchants in a market, the number of digital (UPI and card) "
               "payments received in one week and the average value of a payment in that category.\n\n" +
               md_table(["Category", "Number of payments", "Average value per payment (₹)"],
                        [[k, ind(n), ind(v)] for k, (n, v) in PAY.items()]),
               {"columns": ["category", "payments", "average_value_rs"],
                "rows": [[k, *v] for k, v in PAY.items()]})
val = {k: n * v for k, (n, v) in PAY.items()}
assert val == {"Grocery": 840000, "Pharmacy": 720000, "Fuel": 1620000, "Restaurants": 840000,
               "Electronics": 1920000}
tot_v, tot_n = sum(val.values()), sum(n for n, _ in PAY.values())
assert (tot_v, tot_n) == (5940000, 7200)
Q(T, "Single table", B, "What was the total value of the payments received by fuel merchants in the week?",
  "₹16,20,000", ["₹1,62,000", "₹19,20,000", "₹2,700"],
  "Total value = number of payments × average value",
  "Fuel: 1,800 payments × ₹900 = ₹16,20,000.",
  ["1,800 × 900 = 16,20,000"],
  why="₹1,62,000 drops a zero; ₹19,20,000 is the electronics total; ₹2,700 adds the two figures instead of "
      "multiplying.", secs=30, stim=sid)

assert max(val, key=val.get) == "Electronics" and max(PAY, key=lambda k: PAY[k][0]) == "Grocery"
Q(T, "Single table", I, "Which category received the largest total value of payments in the week?",
  "Electronics", ["Fuel", "Grocery", "Restaurants"],
  "Compare number × average value for every row, not either column alone",
  "Totals: Grocery ₹8.4 lakh, Pharmacy ₹7.2 lakh, Fuel ₹16.2 lakh, Restaurants ₹8.4 lakh, Electronics 300 × 6,400 = "
  "₹19.2 lakh. Electronics is the largest despite having the fewest payments.",
  ["Grocery 8,40,000", "Pharmacy 7,20,000", "Fuel 16,20,000", "Restaurants 8,40,000", "Electronics 19,20,000"],
  why="Fuel is second (₹16.2 lakh); Grocery has the most payments but a small average value; Restaurants total only "
      "₹8.4 lakh.", secs=55, stim=sid)

avg_ = F(tot_v, tot_n)
assert avg_ == 825 and F(sum(v for _, v in PAY.values()), 5) == 1766 and F(tot_v, 5) == 1188000
Q(T, "Single table", I, "What was the average value of a payment across all five categories taken together?",
  "₹825", ["₹1,766", "₹11,88,000", "₹82.50"],
  "Overall average = total value ÷ total number of payments (a weighted average)",
  "Total value = ₹59,40,000 and total payments = 7,200, so the average = 59,40,000 ÷ 7,200 = ₹825.",
  ["Total value = 59,40,000", "Total payments = 7,200", "59,40,000 ÷ 7,200 = 825"],
  why="₹1,766 is the simple average of the five averages, which ignores how many payments each has; ₹11,88,000 is the "
      "average value per category; ₹82.50 slips a decimal place.", secs=65, stim=sid)

new_r = F(1200 * 125, 100) * F(700 * 92, 100)
chg = (new_r - val["Restaurants"]) / tot_v * 100
assert new_r == 966000 and r2(chg) == F(212, 100) and F(125 * 92, 100) == 115
assert r2(F(17, 100) * F(840000, tot_v) * 100) == F(240, 100) and F(15, 1) * F(1200, 7200) == F(5, 2)
Q(T, "Single table", A,
  "In the next week, the number of restaurant payments rises by 25% and their average value falls by 8%; the other "
  "four categories do not change. By what percentage does the total value of all payments increase (correct to two "
  "decimal places)?",
  "2.12%", ["15%", "2.4%", "2.5%"],
  "A change in one row moves the total by (change in that row) ÷ (old total)",
  "Restaurants: 1,500 payments × ₹644 = ₹9,66,000, up ₹1,26,000 from ₹8,40,000. The total rises from ₹59,40,000 by "
  "₹1,26,000, i.e. 1,26,000 ÷ 59,40,000 = 2.12%.",
  ["New restaurant payments = 1,500", "New average = 700 × 0.92 = 644", "New value = 9,66,000 (+1,26,000)",
   "1,26,000 ÷ 59,40,000 = 2.12%"],
  why="15% is the change in the restaurants' own value (1.25 × 0.92 = 1.15); 2.4% adds the rates (+17%) instead of "
      "multiplying them before weighting; 2.5% weights the 15% by the restaurants' share of payments (1/6) instead of "
      "their share of value.", secs=100, stim=sid)

AG = {"Kavya": (240, 35), "Imran": (300, 20), "Sujata": (180, 60), "Rohan": (260, 45)}
IND, FAM = 12000, 30000
sid = stimulus("data_table", "Health-insurance policies sold by four agents in 2025-26",
               "The table shows the number of health-insurance policies sold by four agents of an insurance company "
               "in 2025-26 and the percentage of them that were family-floater policies; the rest were individual "
               "policies. The annual premium is ₹12,000 for every individual policy and ₹30,000 for every "
               "family-floater policy.\n\n" +
               md_table(["Agent", "Policies sold", "Family floater (% of policies sold)"],
                        [[k, n, p] for k, (n, p) in AG.items()]),
               {"columns": ["agent", "policies_sold", "family_floater_pct"],
                "rows": [[k, *v] for k, v in AG.items()], "premium_rs": {"individual": IND, "family_floater": FAM}})
fam = {k: n * F(p, 100) for k, (n, p) in AG.items()}
indv = {k: AG[k][0] - fam[k] for k in AG}
assert fam == {"Kavya": 84, "Imran": 60, "Sujata": 108, "Rohan": 117}
assert indv == {"Kavya": 156, "Imran": 240, "Sujata": 72, "Rohan": 143}
Q(T, "Table with percentages", I, "How many individual policies did Rohan sell?",
  "143", ["117", "260", "156"],
  "Individual policies = policies sold × (100 − family-floater %)",
  "Rohan sold 260 policies, 45% of them family floaters (117). The remaining 55% = 143 were individual policies.",
  ["Family floaters = 260 × 0.45 = 117", "Individual = 260 − 117 = 143"],
  why="117 is Rohan's family-floater count; 260 is all the policies he sold; 156 is Kavya's individual policies.",
  secs=45, stim=sid)

prem = {k: fam[k] * FAM + indv[k] * IND for k in AG}
assert prem["Imran"] == 4680000 and 300 * IND == 3600000 and 300 * F(IND + FAM, 2) == 6300000 and indv["Imran"] * IND == 2880000
Q(T, "Table with percentages", A, "What was the total annual premium on the policies sold by Imran?",
  "₹46,80,000", ["₹36,00,000", "₹63,00,000", "₹28,80,000"],
  "Price each kind of policy separately and add",
  "Imran: 20% of 300 = 60 family floaters × ₹30,000 = ₹18,00,000, and 240 individual policies × ₹12,000 = "
  "₹28,80,000. Total = ₹46,80,000.",
  ["Family floaters = 60 ⇒ 18,00,000", "Individual = 240 ⇒ 28,80,000", "Total = 46,80,000"],
  why="₹36,00,000 prices all 300 policies at ₹12,000; ₹63,00,000 uses the average of the two premiums for every "
      "policy; ₹28,80,000 counts only the individual policies.", secs=70, stim=sid)

comm = {k: fam[k] * FAM * F(15, 100) + indv[k] * IND * F(10, 100) for k in AG}
assert comm == {"Kavya": 565200, "Imran": 558000, "Sujata": 572400, "Rohan": 698100}
assert min(comm, key=comm.get) == "Imran" and max(AG, key=lambda k: AG[k][0]) == "Imran"
Q(T, "Table with percentages", A,
  "Each agent earns a commission of 15% of the premium on family-floater policies and 10% of the premium on "
  "individual policies. Which agent earned the lowest commission?",
  "Imran", ["Sujata", "Kavya", "Rohan"],
  "Commission per family floater = ₹4,500; per individual policy = ₹1,200",
  "Commissions: Kavya 84 × 4,500 + 156 × 1,200 = ₹5,65,200; Imran 60 × 4,500 + 240 × 1,200 = ₹5,58,000; Sujata "
  "108 × 4,500 + 72 × 1,200 = ₹5,72,400; Rohan 117 × 4,500 + 143 × 1,200 = ₹6,98,100. Imran earned the least, though "
  "he sold the most policies.",
  ["Per floater: 15% of 30,000 = 4,500", "Per individual: 10% of 12,000 = 1,200", "Kavya 5,65,200",
   "Imran 5,58,000", "Sujata 5,72,400", "Rohan 6,98,100"],
  why="Sujata sold the fewest policies, but 60% of them were high-commission floaters (₹5,72,400); Kavya is close but "
      "higher at ₹5,65,200; Rohan earned the most.", secs=100, stim=sid)

# ================================================================ Bar Graph DI (B3 I3 A1): sets of 4 and 3
T = "Bar Graph DI"
PP = {"2020": 48, "2021": 36, "2022": 72, "2023": 90, "2024": 81, "2025": 99}
sid = stimulus("chart", "Passports issued by a regional passport office, 2020 to 2025",
               "The bar chart shows the number of passports (in thousand) issued by a regional passport office in "
               "each year from 2020 to 2025 (values read from the bars).\n\n" +
               md_table(["Year", "Passports issued (thousand)"], [[k, v] for k, v in PP.items()]),
               {"chart_type": "bar", "x": list(PP), "series": [{"name": "Passports issued (thousand)",
                                                                "values": list(PP.values())}]})
assert [y for y, v in PP.items() if v == 2 * PP["2021"]] == ["2022"]
Q(T, "Simple bar", B, "In which year did the office issue exactly twice as many passports as in 2021?",
  "2022", ["2023", "2024", "2025"],
  "Double the 2021 bar and look for a matching bar",
  "In 2021 the office issued 36 thousand passports. Twice that is 72 thousand, which is the figure for 2022.",
  ["2021 = 36 thousand", "2 × 36 = 72 thousand", "2022 = 72 thousand"],
  why="2023 (90 thousand) is 2.5 times 2021; 2024 (81 thousand) is 2.25 times; 2025 (99 thousand) is 2.75 times.",
  secs=30, stim=sid)

srt = sorted(PP.values())
med = F(srt[2] + srt[3], 2)
assert srt == [36, 48, 72, 81, 90, 99] and med == F(153, 2) and F(sum(PP.values()), 6) == 71
assert F(PP["2023"] + PP["2024"], 2) == F(171, 2)
Q(T, "Simple bar", B, "What is the median of the yearly numbers of passports issued from 2020 to 2025?",
  "76,500", ["71,000", "81,000", "85,500"],
  "Median of an even number of values = average of the two middle values after sorting",
  "Sorted (thousand): 36, 48, 72, 81, 90, 99. The two middle values are 72 and 81, so the median = (72 + 81) ÷ 2 = "
  "76.5 thousand = 76,500.",
  ["Sort: 36, 48, 72, 81, 90, 99", "Middle two: 72 and 81", "Median = 76.5 thousand"],
  why="71,000 is the mean, not the median; 81,000 takes only the fourth sorted value; 85,500 averages the middle two "
      "years (2023 and 2024) without sorting.", secs=45, stim=sid)

ys_ = list(PP)
chg = {ys_[i]: F(PP[ys_[i]] - PP[ys_[i - 1]], PP[ys_[i - 1]]) for i in range(1, 6)}
big = [y for y, c in chg.items() if abs(c) > F(1, 5)]
assert big == ["2021", "2022", "2023", "2025"] and chg["2025"] == F(2, 9) and chg["2024"] == F(-1, 10)
later = [ys_[i] for i in range(1, 6) if F(abs(PP[ys_[i]] - PP[ys_[i - 1]]), PP[ys_[i]]) > F(1, 5)]
assert len(later) == 2 and len([y for y, c in chg.items() if c > F(1, 5)]) == 3
Q(T, "Simple bar", I,
  "In how many years from 2021 to 2025 did the number of passports issued change (rise or fall) by more than 20% "
  "compared with the previous year?",
  "4", ["3", "5", "2"],
  "Percentage change = change ÷ previous year's figure; count falls as well as rises",
  "2021: −12 on 48 = −25%; 2022: +36 on 36 = +100%; 2023: +18 on 72 = +25%; 2024: −9 on 90 = −10%; 2025: +18 on 81 ≈ "
  "+22.2%. Four years (2021, 2022, 2023, 2025) changed by more than 20%.",
  ["2021: −25% ✓", "2022: +100% ✓", "2023: +25% ✓", "2024: −10% ✗", "2025: +22.2% ✓"],
  why="3 counts only the rises and misses the 25% fall in 2021; 5 includes 2024 (only −10%); 2 divides each change by "
      "the later year's figure instead of the previous year's.", secs=70, stim=sid)

rev = 99000 * (F(88, 100) * 1500 + F(12, 100) * 3500)
assert rev == 172260000 and 99000 * 1500 == 148500000 and 99000 * 3500 == 346500000 and 99000 * 2500 == 247500000
Q(T, "Simple bar", A,
  "In 2025, 12% of the passports issued were Tatkaal passports with a fee of ₹3,500 each, and the rest were normal "
  "passports with a fee of ₹1,500 each. What was the total fee collected on the passports issued in 2025?",
  "₹17,22,60,000", ["₹14,85,00,000", "₹34,65,00,000", "₹24,75,00,000"],
  "Split the year's total by type, price each part, then add",
  "2025: 99,000 passports. Tatkaal = 12% = 11,880 × ₹3,500 = ₹4,15,80,000. Normal = 87,120 × ₹1,500 = ₹13,06,80,000. "
  "Total = ₹17,22,60,000.",
  ["Tatkaal: 11,880 × 3,500 = 4,15,80,000", "Normal: 87,120 × 1,500 = 13,06,80,000", "Total = 17,22,60,000"],
  short="Average fee = 0.88 × 1,500 + 0.12 × 3,500 = ₹1,740; 99,000 × 1,740 = ₹17,22,60,000.",
  why="₹14,85,00,000 charges every passport the normal fee; ₹34,65,00,000 charges every passport the Tatkaal fee; "
      "₹24,75,00,000 uses the simple average fee of ₹2,500.", secs=90, stim=sid)

PROC = {"Mandi P": (42, 30), "Mandi Q": (36, 45), "Mandi R": (28, 52), "Mandi S": (54, 33)}
sid = stimulus("chart", "Paddy and wheat procured at four mandis in 2025-26",
               "The grouped bar chart shows the quantities of paddy and wheat (in thousand tonnes) procured by "
               "government agencies at four mandis in 2025-26 (values read from the bars).\n\n" +
               md_table(["Mandi", "Paddy (thousand tonnes)", "Wheat (thousand tonnes)"],
                        [[k, *v] for k, v in PROC.items()]),
               {"chart_type": "grouped_bar", "x": list(PROC),
                "series": [{"name": "Paddy", "values": [v[0] for v in PROC.values()]},
                           {"name": "Wheat", "values": [v[1] for v in PROC.values()]}]})
gap = {k: abs(p - w) for k, (p, w) in PROC.items()}
assert min(gap, key=gap.get) == "Mandi Q" and gap == {"Mandi P": 12, "Mandi Q": 9, "Mandi R": 24, "Mandi S": 21}
Q(T, "Stacked or grouped bar", B,
  "At which mandi was the difference between the paddy procured and the wheat procured the smallest?",
  "Mandi Q", ["Mandi P", "Mandi R", "Mandi S"],
  "Read the two bars of each mandi and subtract the smaller from the larger",
  "Differences (thousand tonnes): P 42 − 30 = 12, Q 45 − 36 = 9, R 52 − 28 = 24, S 54 − 33 = 21. The smallest is at "
  "Mandi Q.",
  ["P: 12", "Q: 9", "R: 24", "S: 21"],
  why="Mandi P has the next smallest gap (12); Mandi R has the largest gap (24); Mandi S's gap is 21.", secs=35,
  stim=sid)

v_q = 36000 * 10 * 2300 + 45000 * 10 * 2400
assert v_q == 1908000000 and 36000 * 10 * 2400 + 45000 * 10 * 2300 == 1899000000 and 81000 * 10 * 2350 == 1903500000
Q(T, "Stacked or grouped bar", I,
  "Assume the agencies paid ₹2,300 per quintal for paddy and ₹2,400 per quintal for wheat (1 tonne = 10 quintals). "
  "What was the total value of the paddy and wheat procured at Mandi Q?",
  "₹190.8 crore", ["₹19.08 crore", "₹189.9 crore", "₹190.35 crore"],
  "Convert thousand tonnes to quintals, then price each crop separately",
  "Paddy: 36,000 t = 3,60,000 quintals × ₹2,300 = ₹82.8 crore. Wheat: 45,000 t = 4,50,000 quintals × ₹2,400 = "
  "₹108 crore. Total = ₹190.8 crore.",
  ["Paddy: 3,60,000 q × 2,300 = 82.8 crore", "Wheat: 4,50,000 q × 2,400 = 108 crore", "Total = 190.8 crore"],
  why="₹19.08 crore forgets that 1 tonne is 10 quintals; ₹189.9 crore swaps the two prices; ₹190.35 crore prices all "
      "81,000 tonnes at the average ₹2,350.", secs=70, stim=sid)

sel = [k for k, (p, w) in PROC.items() if w > 40]
assert sel == ["Mandi Q", "Mandi R"] and F(sum(PROC[k][0] for k in sel), 2) == 32
assert F(sum(p for p, _ in PROC.values()), 4) == 40 and F(45 + 52, 2) == F(97, 2) and F(42 + 54, 2) == 48
Q(T, "Stacked or grouped bar", I,
  "What was the average paddy procurement of the mandis at which wheat procurement exceeded 40 thousand tonnes?",
  "32 thousand tonnes", ["40 thousand tonnes", "48.5 thousand tonnes", "48 thousand tonnes"],
  "First pick the mandis using the wheat bars, then average their paddy bars",
  "Wheat exceeded 40 thousand tonnes only at Q (45) and R (52). Their paddy figures are 36 and 28, whose average is "
  "32 thousand tonnes.",
  ["Wheat > 40: Mandi Q, Mandi R", "Paddy: 36 and 28", "Average = 32"],
  why="40 is the average paddy of all four mandis; 48.5 averages the wheat figures of Q and R; 48 averages the paddy "
      "of the other two mandis (P and S).", secs=55, stim=sid)

# ================================================================ Pie Chart DI (B1 I4 A4): sets of 5 and 4
T = "Pie Chart DI"
SAV = {"Bank deposits": 35, "Small savings (PPF, NSC etc.)": 15, "Mutual funds": 18, "Insurance": 12, "Gold": 14,
       "Others": 6}
TOTS = 2400
assert sum(SAV.values()) == 100
sid = stimulus("chart", "Household financial savings of a district by instrument, 2025-26",
               "The pie chart shows how the households of a district divided their total financial savings of "
               "₹2,400 crore in 2025-26 among six instruments (percentage of the total).\n\n" +
               md_table(["Instrument", "Share of savings (%)"], [[k, v] for k, v in SAV.items()]),
               {"chart_type": "pie", "unit": "percent", "total_rs_crore": TOTS,
                "labels": list(SAV), "values": list(SAV.values())})
amt = {k: F(TOTS * v, 100) for k, v in SAV.items()}
assert amt["Mutual funds"] == 432 and amt["Small savings (PPF, NSC etc.)"] == 360 and amt["Gold"] == 336
Q(T, "Percentage-based", B, "How much did the households save in mutual funds in 2025-26?",
  "₹432 crore", ["₹360 crore", "₹43.2 crore", "₹336 crore"],
  "Amount = share % × total",
  "Mutual funds: 18% of ₹2,400 crore = ₹432 crore.",
  ["2,400 × 0.18 = 432"],
  why="₹360 crore is the small-savings figure (15%); ₹43.2 crore slips a decimal place; ₹336 crore is gold (14%).",
  secs=30, stim=sid)

over = [k for k, a in amt.items() if a > 300]
assert len(over) == 4 and amt["Insurance"] == 288 and len([k for k, v in SAV.items() if v > 15]) == 2
Q(T, "Percentage-based", I, "For how many of the six instruments did the households save more than ₹300 crore?",
  "4", ["3", "5", "2"],
  "₹300 crore is 12.5% of ₹2,400 crore, so count the shares above 12.5%",
  "₹300 crore ÷ ₹2,400 crore = 12.5%. Shares above 12.5%: bank deposits (35%), small savings (15%), mutual funds (18%) "
  "and gold (14%). Insurance (12% = ₹288 crore) and others (6%) fall short. So 4 instruments.",
  ["300/2,400 = 12.5%", "Above: 35%, 15%, 18%, 14%", "Below: 12%, 6%", "Count = 4"],
  why="3 misses gold (14% = ₹336 crore); 5 includes insurance (₹288 crore); 2 counts only the shares above 15%.",
  secs=50, stim=sid)

per_hh = amt["Bank deposits"] * 10 ** 7 / 600000
assert per_hh == 14000 and F(TOTS * 10 ** 7, 600000) == 40000
Q(T, "Percentage-based", I,
  "The district has 6 lakh households. What was the average saving per household in bank deposits in 2025-26?",
  "₹14,000", ["₹40,000", "₹1,400", "₹1,40,000"],
  "1 crore = 100 lakh; divide the bank-deposit amount by the number of households",
  "Bank deposits = 35% of ₹2,400 crore = ₹840 crore = ₹8,40,00,00,000. Dividing by 6,00,000 households gives "
  "₹14,000 per household.",
  ["Bank deposits = ₹840 crore = ₹8,40,00,00,000", "÷ 6,00,000 households", "= ₹14,000"],
  why="₹40,000 divides all savings (₹2,400 crore) by the households; ₹1,400 and ₹1,40,000 slip a place in the "
      "crore-to-lakh conversion.", secs=55, stim=sid)

RET = {"Bank deposits": F(65, 10), "Small savings (PPF, NSC etc.)": F(75, 10), "Mutual funds": F(12),
       "Insurance": F(5), "Gold": F(10), "Others": F(4)}
earn = sum(amt[k] * RET[k] / 100 for k in SAV)
assert earn == F(1872, 10) and sum(RET.values()) / 6 == F(75, 10) and TOTS * F(75, 1000) == 180 and TOTS * F(65, 1000) == 156
Q(T, "Percentage-based", A,
  "In 2025-26 the instruments earned these annual returns: bank deposits 6.5%, small savings 7.5%, mutual funds 12%, "
  "insurance 5%, gold 10% and others 4%. What total return did the district's savings earn in the year?",
  "₹187.2 crore", ["₹180 crore", "₹156 crore", "₹18.72 crore"],
  "Total return = Σ (amount in each instrument × its rate); the overall rate is a weighted average",
  "Weighted rate = 0.35 × 6.5 + 0.15 × 7.5 + 0.18 × 12 + 0.12 × 5 + 0.14 × 10 + 0.06 × 4 = 2.275 + 1.125 + 2.16 + 0.6 + "
  "1.4 + 0.24 = 7.8%. Return = 7.8% of ₹2,400 crore = ₹187.2 crore.",
  ["Weighted rate = 7.8%", "7.8% × 2,400 = 187.2 crore"],
  why="₹180 crore uses the simple average of the six rates (7.5%); ₹156 crore applies the bank-deposit rate to "
      "everything; ₹18.72 crore slips a decimal place.", secs=100, stim=sid)

phys = amt["Gold"] * F(5, 7)
health = amt["Insurance"] * F(1, 4)
assert (phys, health) == (240, 72) and ratio(phys, health) == "10 : 3" and ratio(336, 288) == "7 : 6"
assert ratio(phys, amt["Insurance"] - health) == "10 : 9"
Q(T, "Percentage-based", A,
  "The gold savings were split between physical gold and gold ETFs in the ratio 5 : 2, and the insurance savings "
  "between life and health insurance in the ratio 3 : 1. What is the ratio of the savings in physical gold to the "
  "savings in health insurance?",
  "10 : 3", ["7 : 6", "5 : 1", "10 : 9"],
  "Find each sector's amount first, then apply the inner ratio within that sector",
  "Gold = ₹336 crore, so physical gold = 5/7 × 336 = ₹240 crore. Insurance = ₹288 crore, so health = 1/4 × 288 = ₹72 "
  "crore. Ratio = 240 : 72 = 10 : 3.",
  ["Gold = 336 ⇒ physical = 240", "Insurance = 288 ⇒ health = 72", "240 : 72 = 10 : 3"],
  why="7 : 6 compares all gold with all insurance; 5 : 1 compares the ratio terms without the sector sizes; 10 : 9 "
      "uses life insurance (₹216 crore) instead of health insurance.", secs=90, stim=sid)

ACC = {"Raigad": 25, "Ratnagiri": 20, "Sindhudurg": 10, "Satara": 30, "Sangli": 15}
DEP = {"Raigad": 30, "Ratnagiri": 15, "Sindhudurg": 11, "Satara": 25, "Sangli": 19}
assert sum(ACC.values()) == 100 and sum(DEP.values()) == 100
sid = stimulus("chart", "Savings accounts and deposits of a regional rural bank by district (two pie charts)",
               "Two pie charts describe a regional rural bank that works in five districts. The first shows how its "
               "2,40,000 savings accounts are distributed among the districts; the second shows how the ₹1,200 crore "
               "held in these accounts is distributed (percentages of each total).\n\n" +
               md_table(["District", "Accounts (% of 2,40,000)", "Deposits (% of ₹1,200 crore)"],
                        [[k, ACC[k], DEP[k]] for k in ACC]),
               {"chart_type": "two_pies", "unit": "percent",
                "pies": [{"name": "Savings accounts", "total": 240000, "labels": list(ACC), "values": list(ACC.values())},
                         {"name": "Deposits", "total_rs_crore": 1200, "labels": list(DEP),
                          "values": list(DEP.values())}]})
acc = {k: 240000 * F(v, 100) for k, v in ACC.items()}
dep = {k: 1200 * F(v, 100) * 10 ** 7 for k, v in DEP.items()}
avgd = {k: dep[k] / acc[k] for k in ACC}
assert dep["Satara"] == 300 * 10 ** 7 and 1200 * F(30, 100) == 360
Q(T, "Two pie charts", I, "What were the total deposits held in the bank's savings accounts in Satara?",
  "₹300 crore", ["₹360 crore", "₹30 crore", "₹250 crore"],
  "Use the deposits pie for money and the accounts pie for numbers of accounts",
  "Satara's share of deposits is 25%, so its deposits are 25% of ₹1,200 crore = ₹300 crore.",
  ["Deposits pie: Satara 25%", "25% of 1,200 = 300 crore"],
  why="₹360 crore uses Satara's share of accounts (30%) instead of deposits; ₹30 crore slips a decimal place; ₹250 "
      "crore takes 25% of ₹1,000 crore.", secs=40, stim=sid)

assert avgd["Raigad"] == 60000 and F(1200 * 10 ** 7, 240000) == 50000 and near(avgd["Satara"], 41666.67, 0.01)
Q(T, "Two pie charts", I, "What was the average deposit per savings account in Raigad?",
  "₹60,000", ["₹50,000", "₹6,000", "₹41,666.67"],
  "Average deposit = district's deposits ÷ district's accounts; take each from its own pie",
  "Raigad: deposits = 30% of ₹1,200 crore = ₹360 crore; accounts = 25% of 2,40,000 = 60,000. Average = ₹360 crore ÷ "
  "60,000 = ₹60,000.",
  ["Deposits = ₹360 crore = ₹3,60,00,00,000", "Accounts = 60,000", "Average = ₹60,000"],
  short="Average = overall average (₹50,000) × deposit share ÷ account share = 50,000 × 30/25.",
  why="₹50,000 is the bank-wide average; ₹6,000 slips a place in converting crore; ₹41,666.67 is Satara's average.",
  secs=60, stim=sid)

above = [k for k in ACC if avgd[k] > 50000]
assert above == ["Raigad", "Sindhudurg", "Sangli"] and avgd["Sindhudurg"] == 55000
Q(T, "Two pie charts", A,
  "In how many of the five districts was the average deposit per account higher than the bank's overall average "
  "deposit per account?",
  "3", ["2", "4", "1"],
  "A district's average beats the overall average exactly when its share of deposits exceeds its share of accounts",
  "Overall average = ₹1,200 crore ÷ 2,40,000 = ₹50,000. Compare the shares: Raigad 30% > 25% ✓, Ratnagiri 15% < 20%, "
  "Sindhudurg 11% > 10% ✓, Satara 25% < 30%, Sangli 19% > 15% ✓. So 3 districts.",
  ["Raigad ₹60,000 ✓", "Ratnagiri ₹37,500", "Sindhudurg ₹55,000 ✓", "Satara ₹41,667", "Sangli ₹63,333 ✓"],
  why="2 misses Sindhudurg, whose shares (11% vs 10%) are close; 4 includes Satara, which has the most accounts but a "
      "smaller deposit share; 1 counts only Raigad, the largest deposit share.", secs=90, stim=sid)

new_avg = dep["Ratnagiri"] * F(140, 100) / (acc["Ratnagiri"] * F(125, 100))
assert new_avg == 42000 and avgd["Ratnagiri"] == 37500 and 37500 * F(14, 10) == 52500 and 37500 * F(115, 100) == 43125
assert near(37500 * F(125, 140), 33482.14, 0.01)
Q(T, "Two pie charts", A,
  "Next year Ratnagiri's number of accounts grows by 25% and its deposits grow by 40%. What will be its average "
  "deposit per account?",
  "₹42,000", ["₹52,500", "₹43,125", "₹33,482.14"],
  "New average = old average × (1 + deposit growth) ÷ (1 + account growth)",
  "Now: deposits ₹180 crore, accounts 48,000, average ₹37,500. Next year: deposits ₹252 crore, accounts 60,000, "
  "average = ₹252 crore ÷ 60,000 = ₹42,000 (= 37,500 × 1.4 ÷ 1.25).",
  ["Now: 180 crore ÷ 48,000 = 37,500", "Deposits → 252 crore", "Accounts → 60,000", "252 crore ÷ 60,000 = 42,000"],
  why="₹52,500 applies the 40% deposit growth but ignores the new accounts; ₹43,125 adds the net 15% (40 − 25) to the "
      "average; ₹33,482.14 inverts the two growth factors.", secs=90, stim=sid)

# ================================================================ Line Graph DI (B2 I1 A1): one set of 4
T = "Line Graph DI"
ON = {"Jan": 1800, "Feb": 1500, "Mar": 1350, "Apr": 1620, "May": 2025, "Jun": 2430}
sid = stimulus("chart", "Wholesale price of onions at a mandi, January to June 2026",
               "The line graph shows the average wholesale price of onions (in ₹ per quintal) at a mandi in each "
               "month from January to June 2026. 1 quintal = 100 kg.\n\n" +
               md_table(["Month", "Price (₹ per quintal)"], [[k, ind(v)] for k, v in ON.items()]),
               {"chart_type": "line", "x": list(ON), "series": [{"name": "Price (₹ per quintal)",
                                                                 "values": list(ON.values())}]})
assert ON["Jun"] - ON["Mar"] == 1080 and ON["Jun"] - ON["May"] == 405 and ON["Jun"] - ON["Jan"] == 630
Q(T, "Single line", B, "By how many rupees per quintal did the price rise from March to June?",
  "₹1,080", ["₹405", "₹630", "₹270"],
  "Read the two points and subtract",
  "March: ₹1,350; June: ₹2,430. Rise = ₹1,080 per quintal.",
  ["2,430 − 1,350 = 1,080"],
  why="₹405 is the rise from May to June only; ₹630 is the rise from January to June; ₹270 is the rise from March to "
      "April.", secs=30, stim=sid)

avg_ = F(sum(ON.values()), 6)
above = [m for m, v in ON.items() if v > avg_]
assert avg_ == F(35750, 20) and above == ["Jan", "May", "Jun"]
Q(T, "Single line", B, "In how many of the six months was the price higher than its six-month average?",
  "3", ["2", "4", "1"],
  "Average = sum of the six prices ÷ 6; then compare each month",
  "Sum = 1,800 + 1,500 + 1,350 + 1,620 + 2,025 + 2,430 = 10,725, so the average is ₹1,787.50. January (1,800), May "
  "(2,025) and June (2,430) are above it: 3 months.",
  ["Sum = 10,725", "Average = 1,787.50", "Above: Jan, May, Jun"],
  why="2 misses January, which is only ₹12.50 above the average; 4 adds April (₹1,620); 1 counts only June.", secs=50,
  stim=sid)

kg_m = F(24300, ON["Mar"]) * 100
kg_j = F(24300, ON["Jun"]) * 100
assert (kg_m, kg_j) == (1800, 1000) and kg_m - kg_j == 800 and kg_m - F(24300, ON["May"]) * 100 == 600
Q(T, "Single line", I,
  "A restaurant spends exactly ₹24,300 on onions every month at the month's wholesale price. How many more kilograms "
  "of onions did it get in March than in June?",
  "800 kg", ["1,800 kg", "8 kg", "600 kg"],
  "Quantity = money spent ÷ price; convert quintals to kg",
  "March: 24,300 ÷ 1,350 = 18 quintals = 1,800 kg. June: 24,300 ÷ 2,430 = 10 quintals = 1,000 kg. Difference = 800 kg.",
  ["March: 18 quintals = 1,800 kg", "June: 10 quintals = 1,000 kg", "1,800 − 1,000 = 800 kg"],
  why="1,800 kg is the March quantity alone; 8 kg forgets that 1 quintal is 100 kg; 600 kg compares March with May "
      "(1,200 kg) instead of June.", secs=60, stim=sid)

cost = 40 * ON["Feb"]
revn = 40 * F(95, 100) * ON["May"]
pc = (revn - cost) / cost * 100
assert cost == 60000 and revn == 76950 and pc == F(2825, 100)
assert F(ON["May"] - ON["Feb"], ON["Feb"]) * 100 == 35 and r2((revn - cost) / revn * 100) == F(2203, 100)
Q(T, "Single line", A,
  "A trader bought 40 quintals of onions in February at February's price and sold them in May at May's price. 5% of "
  "the onions (by weight) were lost in storage. What was his profit percentage (correct to two decimal places)?",
  "28.25%", ["35%", "30%", "22.03%"],
  "Revenue comes only from the quantity left after the loss; profit % is on the purchase cost",
  "Cost = 40 × 1,500 = ₹60,000. Saleable = 38 quintals × ₹2,025 = ₹76,950. Profit = ₹16,950, which is "
  "16,950 ÷ 60,000 = 28.25% of the cost.",
  ["Cost = 60,000", "Sold 38 q × 2,025 = 76,950", "Profit = 16,950", "16,950 ÷ 60,000 = 28.25%"],
  why="35% ignores the storage loss (price rise from ₹1,500 to ₹2,025); 30% subtracts 5 from 35 instead of applying "
      "the loss to the quantity; 22.03% divides the profit by the revenue instead of the cost.", secs=90, stim=sid)

# ================================================================ Caselet DI (B2 I7 A2): sets of 6 and 5
T = "Caselet DI"
sid = stimulus("caselet", "Buses of a city transport undertaking at three depots",
               "A city transport undertaking runs 300 buses from three depots — North, Central and South — in the "
               "ratio 5 : 3 : 2. On a working day, 90% of North's buses, 80% of Central's buses and 85% of South's "
               "buses are on the road; the rest are under maintenance. Each bus on the road runs 180 km a day at "
               "North, 200 km at Central and 240 km at South. North and South run diesel buses that cover 4 km per "
               "litre of diesel, which costs ₹90 per litre. Central runs electric buses that use 1.2 kWh of "
               "electricity per km, at ₹8 per kWh.")
fleet = {"N": 150, "C": 90, "S": 60}
assert [300 * F(r, 10) for r in (5, 3, 2)] == [150, 90, 60]
road = {"N": 150 * F(90, 100), "C": 90 * F(80, 100), "S": 60 * F(85, 100)}
km = {"N": road["N"] * 180, "C": road["C"] * 200, "S": road["S"] * 240}
assert road == {"N": 135, "C": 72, "S": 51} and km == {"N": 24300, "C": 14400, "S": 12240}
Q(T, "Paragraph data", B, "How many of the South depot's buses are on the road on a working day?",
  "51", ["60", "9", "54"],
  "South's fleet = 2/10 of 300; take 85% of it",
  "South has 2/10 × 300 = 60 buses, and 85% of 60 = 51 are on the road.",
  ["South fleet = 60", "85% of 60 = 51"],
  why="60 is South's whole fleet; 9 is the number under maintenance; 54 uses North's 90% instead of South's 85%.",
  secs=35, stim=sid)

tkm = sum(km.values())
assert tkm == 50940 and 150 * 180 + 90 * 200 + 60 * 240 == 59400 and 258 * 200 == 51600
assert near(258 * F(180 + 200 + 240, 3), 53320, 1e-6)
Q(T, "Paragraph data", I, "What is the total distance run by all the buses on the road on a working day?",
  "50,940 km", ["59,400 km", "51,600 km", "53,320 km"],
  "Distance = buses on the road × km per bus, depot by depot",
  "North 135 × 180 = 24,300 km; Central 72 × 200 = 14,400 km; South 51 × 240 = 12,240 km. Total = 50,940 km.",
  ["North 24,300", "Central 14,400", "South 12,240", "Total = 50,940 km"],
  why="59,400 km counts the buses under maintenance as well; 51,600 km gives all 258 buses on the road 200 km each; "
      "53,320 km uses the simple average of the three daily runs for every bus.", secs=60, stim=sid)

dN = km["N"] / 4 * 90
assert dN == 546750 and F(150 * 180, 4) * 90 == 607500 and km["N"] * 90 == 2187000 and km["S"] / 4 * 90 == 275400
Q(T, "Paragraph data", I, "What is the North depot's daily diesel bill?",
  "₹5,46,750", ["₹6,07,500", "₹21,87,000", "₹2,75,400"],
  "Diesel used = km ÷ 4; cost = litres × ₹90",
  "North's buses on the road run 24,300 km, using 24,300 ÷ 4 = 6,075 litres. Cost = 6,075 × 90 = ₹5,46,750.",
  ["km = 24,300", "Litres = 6,075", "Cost = 6,075 × 90 = 5,46,750"],
  why="₹6,07,500 includes the 15 buses under maintenance; ₹21,87,000 multiplies the km (not the litres) by ₹90; "
      "₹2,75,400 is the South depot's bill.", secs=60, stim=sid)

e_km, d_km = F(12, 10) * 8, F(90, 4)
pc = (d_km - e_km) / d_km * 100
assert (e_km, d_km) == (F(96, 10), F(45, 2)) and r2(pc) == F(5733, 100)
assert r2((d_km - e_km) / e_km * 100) == F(13438, 100) and r2(e_km / d_km * 100) == F(4267, 100)
Q(T, "Paragraph data", I,
  "By what percentage is the energy cost per km of an electric bus lower than the fuel cost per km of a diesel bus "
  "(correct to two decimal places)?",
  "57.33%", ["134.38%", "42.67%", "12.9%"],
  "Cost per km: diesel = ₹90 ÷ 4 km; electric = 1.2 kWh × ₹8. 'Lower than diesel' uses the diesel cost as the base",
  "Diesel: ₹22.50 per km. Electric: ₹9.60 per km. The electric bus is ₹12.90 cheaper, which is 12.90 ÷ 22.50 = 57.33% "
  "lower.",
  ["Diesel = 90 ÷ 4 = ₹22.50/km", "Electric = 1.2 × 8 = ₹9.60/km", "Saving = ₹12.90", "12.90 ÷ 22.50 = 57.33%"],
  why="134.38% divides the saving by the electric cost (how much more diesel costs); 42.67% is the electric cost as a "
      "percentage of the diesel cost; 12.9% reads the ₹12.90 saving as a percentage.", secs=65, stim=sid)

off = sum(fleet[k] - road[k] for k in fleet)
assert off == 42 and F(off, 300) * 100 == 14 and r2(F(off, 258) * 100) == F(1628, 100) and F(10 + 20 + 15, 3) == 15
Q(T, "Paragraph data", I,
  "What percentage of the undertaking's 300 buses are under maintenance on a working day?",
  "14%", ["15%", "86%", "16.28%"],
  "Count the buses off the road at each depot, then divide by the whole fleet",
  "Off the road: North 15, Central 18, South 9 — 42 buses. 42 ÷ 300 = 14%.",
  ["North 150 − 135 = 15", "Central 90 − 72 = 18", "South 60 − 51 = 9", "42 ÷ 300 = 14%"],
  why="15% is the simple average of 10%, 20% and 15%, which ignores the different fleet sizes; 86% is the share on "
      "the road; 16.28% divides by the 258 buses on the road instead of the whole fleet.", secs=60, stim=sid)

save = km["N"] * (d_km - e_km)
assert save == 313470 and km["N"] * e_km == 233280 and 150 * 180 * (d_km - e_km) == 348300
Q(T, "Paragraph data", A,
  "The undertaking replaces all of North's diesel buses with electric buses like Central's, keeping the same number "
  "on the road and the same daily km per bus. How much will it save on North's daily energy bill?",
  "₹3,13,470", ["₹5,46,750", "₹2,33,280", "₹3,48,300"],
  "Saving = North's daily km × (diesel cost per km − electric cost per km)",
  "North runs 24,300 km a day. Saving per km = 22.50 − 9.60 = ₹12.90. Daily saving = 24,300 × 12.90 = ₹3,13,470 "
  "(diesel bill ₹5,46,750 minus electricity bill ₹2,33,280).",
  ["North km = 24,300", "Saving per km = ₹12.90", "24,300 × 12.90 = 3,13,470"],
  why="₹5,46,750 is the whole diesel bill, as if electricity were free; ₹2,33,280 is the new electricity bill; "
      "₹3,48,300 counts all 150 North buses, including those under maintenance.", secs=90, stim=sid)

FAMS = {2: 150, 3: 240, 4: 300, 5: 150, 6: 60}
sid = stimulus("caselet", "Grain distributed by a fair-price shop in a month",
               "A fair-price shop serves 1,200 ration cards: 300 Antyodaya (AAY) cards and 900 priority-household "
               "(PHH) cards. Every AAY card gets 35 kg of grain a month whatever the family size; every PHH card gets "
               "5 kg per family member a month. For every card, the grain is rice and wheat in the ratio 3 : 2. The "
               "shopkeeper is paid a commission of ₹1.50 for every kg distributed. The PHH cards are distributed by "
               "family size as follows.\n\n" +
               md_table(["Members on the card", "Number of PHH cards"], [[k, v] for k, v in FAMS.items()]),
               {"columns": ["members", "phh_cards"], "rows": [[k, v] for k, v in FAMS.items()]})
mem = sum(k * v for k, v in FAMS.items())
phh = 5 * mem
aay = 300 * 35
assert sum(FAMS.values()) == 900 and mem == 3330 and phh == 16650 and aay == 10500
assert 900 * 5 == 4500 and 900 * 4 * 5 == 18000 and 900 * 35 == 31500
Q(T, "Caselet with table", B, "How much grain does the shop distribute to PHH cards in a month?",
  "16,650 kg", ["4,500 kg", "18,000 kg", "31,500 kg"],
  "PHH grain = 5 kg × total members on PHH cards",
  "Members = 2 × 150 + 3 × 240 + 4 × 300 + 5 × 150 + 6 × 60 = 300 + 720 + 1,200 + 750 + 360 = 3,330. Grain = "
  "3,330 × 5 = 16,650 kg.",
  ["Members = 3,330", "3,330 × 5 = 16,650 kg"],
  why="4,500 kg gives 5 kg per card instead of per member; 18,000 kg assumes 4 members on every card; 31,500 kg gives "
      "every PHH card the AAY quota of 35 kg.", secs=50, stim=sid)

rice = F(phh + aay) * F(3, 5)
assert rice == 16290 and F(phh + aay) * F(2, 5) == 10860 and F(phh) * F(3, 5) == 9990
Q(T, "Caselet with table", I, "How much rice in all does the shop distribute in a month?",
  "16,290 kg", ["10,860 kg", "9,990 kg", "16,650 kg"],
  "Total grain = AAY + PHH; rice is 3/5 of it",
  "Total grain = 10,500 (AAY: 300 × 35) + 16,650 (PHH) = 27,150 kg. Rice = 3/5 × 27,150 = 16,290 kg.",
  ["AAY = 10,500 kg", "PHH = 16,650 kg", "Total = 27,150 kg", "Rice = 16,290 kg"],
  why="10,860 kg is the wheat; 9,990 kg is the rice for PHH cards only; 16,650 kg is the PHH grain, not the rice.",
  secs=60, stim=sid)

big = sum(k * v for k, v in FAMS.items() if k >= 4)
pc = F(big, mem) * 100
assert big == 2310 and r2(pc) == F(6937, 100) and r2(F(510, 900) * 100) == F(5667, 100)
assert r2(100 - pc) == F(3063, 100) and r2(F(1200, mem) * 100) == F(3604, 100)
Q(T, "Caselet with table", I,
  "What percentage of the grain given to PHH cards goes to cards with 4 or more members (correct to two decimal "
  "places)?",
  "69.37%", ["56.67%", "30.63%", "36.04%"],
  "PHH grain is proportional to members, not to cards",
  "Members on cards with 4, 5 or 6 members: 1,200 + 750 + 360 = 2,310 out of 3,330. Share = 2,310 ÷ 3,330 = 69.37%.",
  ["Members (4+) = 2,310", "All PHH members = 3,330", "2,310 ÷ 3,330 = 69.37%"],
  why="56.67% uses the share of cards (510 of 900) instead of members; 30.63% is the share of the smaller families; "
      "36.04% counts only the 4-member cards.", secs=70, stim=sid)

com = F(phh + aay) * F(3, 2)
assert com == 40725 and phh * F(3, 2) == 24975 and aay * F(3, 2) == 15750
Q(T, "Caselet with table", I, "What commission does the shopkeeper earn in a month?",
  "₹40,725", ["₹24,975", "₹15,750", "₹4,07,250"],
  "Commission = ₹1.50 × all grain distributed (AAY + PHH)",
  "Total grain = 27,150 kg, so the commission = 27,150 × 1.50 = ₹40,725.",
  ["Total grain = 27,150 kg", "× ₹1.50 = ₹40,725"],
  why="₹24,975 counts only PHH grain; ₹15,750 counts only AAY grain; ₹4,07,250 slips a decimal place.", secs=45,
  stim=sid)

delta = -50 * 6 * 5 + 50 * 35 + 100 * 3 * 5
assert delta == 1750 and 50 * 35 + 100 * 15 == 3250 and -1500 + 1750 == 250
Q(T, "Caselet with table", A,
  "Next month, 50 of the 6-member PHH cards are converted into AAY cards, and 100 new 3-member PHH cards are issued. "
  "How does the shop's total monthly grain distribution change?",
  "Increases by 1,750 kg", ["Increases by 3,250 kg", "Increases by 250 kg", "Increases by 1,500 kg"],
  "Track each change: a converted card stops getting 5 kg × 6 and starts getting 35 kg",
  "Each converted card changes from 30 kg (PHH) to 35 kg (AAY): +5 kg × 50 = +250 kg. The new cards add 100 × 15 = "
  "1,500 kg. Net change = +1,750 kg.",
  ["Conversion: −1,500 + 1,750 = +250 kg", "New cards: +1,500 kg", "Net = +1,750 kg"],
  why="3,250 kg adds the AAY quota of the converted cards without removing their old PHH quota; 250 kg forgets the "
      "new cards; 1,500 kg forgets the conversion.", secs=90, stim=sid)

# ================================================================ Missing DI (B2 I2 A1): one set of 5
T = "Missing DI"
dash = "—"
ATM = {"ATM-1": (40, 30, None, 1500, None), "ATM-2": (None, 36, 80, None, 2400),
       "ATM-3": (50, None, 64, 1600, None), "ATM-4": (75, None, None, 2250, 2000),
       "ATM-5": (None, 28, 70, None, 1750)}
sid = stimulus("data_table", "Cash loaded and withdrawn at five ATMs of a bank in a week (some values missing)",
               "The table shows, for five ATMs of a bank in one week, the cash loaded and the cash withdrawn (both in "
               "₹ lakh), the utilisation (cash withdrawn as a percentage of cash loaded), the number of withdrawals "
               "and the average amount per withdrawal (₹). Some values are missing (—); work them out from the "
               "others.\n\n" +
               md_table(["ATM", "Cash loaded (₹ lakh)", "Cash withdrawn (₹ lakh)", "Utilisation (%)",
                         "Withdrawals", "Average withdrawal (₹)"],
                        [[k, *[dash if c is None else ind(c) for c in v]] for k, v in ATM.items()]),
               {"columns": ["atm", "loaded_lakh", "withdrawn_lakh", "utilisation_pct", "withdrawals",
                            "average_withdrawal_rs"], "rows": [[k, *v] for k, v in ATM.items()]})
ld = {"ATM-1": F(40), "ATM-2": F(36) / F(80, 100), "ATM-3": F(50), "ATM-4": F(75), "ATM-5": F(28) / F(70, 100)}
wd = {"ATM-1": F(30), "ATM-2": F(36), "ATM-3": F(50) * F(64, 100), "ATM-4": F(2250 * 2000, 100000), "ATM-5": F(28)}
nw = {"ATM-1": F(1500), "ATM-2": wd["ATM-2"] * 100000 / 2400, "ATM-3": F(1600), "ATM-4": F(2250),
      "ATM-5": wd["ATM-5"] * 100000 / 1750}
aw = {k: wd[k] * 100000 / nw[k] for k in ATM}
assert ld == {"ATM-1": 40, "ATM-2": 45, "ATM-3": 50, "ATM-4": 75, "ATM-5": 40}
assert wd == {"ATM-1": 30, "ATM-2": 36, "ATM-3": 32, "ATM-4": 45, "ATM-5": 28}
assert nw["ATM-2"] == 1500 and nw["ATM-5"] == 1600 and aw == {"ATM-1": 2000, "ATM-2": 2400, "ATM-3": 2000,
                                                              "ATM-4": 2000, "ATM-5": 1750}
assert F(30, 40) * 100 == 75 and r2(F(40, 30) * 100) == F(13333, 100)
Q(T, "Table with missing values", B, "What was the utilisation of ATM-1?",
  "75%", ["133.33%", "25%", "10%"],
  "Utilisation = cash withdrawn ÷ cash loaded × 100",
  "ATM-1: ₹30 lakh withdrawn out of ₹40 lakh loaded = 75%.",
  ["30 ÷ 40 = 0.75 = 75%"],
  why="133.33% divides the other way; 25% is the share left unused; 10% reads the ₹10 lakh left as a percentage.",
  secs=30, stim=sid)

assert 28 * F(70, 100) == F(196, 10) and 28 * F(13, 10) == F(364, 10) and ld["ATM-5"] - 28 == 12
Q(T, "Table with missing values", B, "How much cash was loaded into ATM-5?",
  "₹40 lakh", ["₹19.6 lakh", "₹36.4 lakh", "₹12 lakh"],
  "Cash loaded = cash withdrawn ÷ utilisation",
  "₹28 lakh was 70% of the cash loaded, so the cash loaded = 28 ÷ 0.7 = ₹40 lakh.",
  ["28 = 0.7 × loaded", "Loaded = 40"],
  why="₹19.6 lakh takes 70% of 28; ₹36.4 lakh adds 30% to 28; ₹12 lakh is the cash left unused.", secs=40, stim=sid)

assert F(36 * 100000, 2400) == 1500 and F(45 * 100000, 2400) == 1875
Q(T, "Table with missing values", I, "How many withdrawals were made at ATM-2?",
  "1,500", ["15,000", "1,875", "150"],
  "Number of withdrawals = cash withdrawn ÷ average withdrawal (convert lakh to rupees)",
  "ATM-2: ₹36 lakh = ₹36,00,000 withdrawn at an average of ₹2,400, so 36,00,000 ÷ 2,400 = 1,500 withdrawals.",
  ["₹36 lakh = 36,00,000", "36,00,000 ÷ 2,400 = 1,500"],
  why="15,000 and 150 slip a place in the lakh conversion; 1,875 divides the cash loaded (₹45 lakh) instead of the "
      "cash withdrawn.", secs=50, stim=sid)

assert max(aw, key=aw.get) == "ATM-2" and max(nw, key=nw.get) == "ATM-4"
Q(T, "Table with missing values", I, "Which ATM had the highest average amount per withdrawal?",
  "ATM-2", ["ATM-4", "ATM-3", "ATM-5"],
  "Fill the missing averages: average = cash withdrawn ÷ number of withdrawals",
  "ATM-1: 30 lakh ÷ 1,500 = ₹2,000. ATM-2: ₹2,400 (given). ATM-3: 32 lakh ÷ 1,600 = ₹2,000. ATM-4: ₹2,000 (given). "
  "ATM-5: ₹1,750. ATM-2 is the highest.",
  ["ATM-1 ₹2,000", "ATM-2 ₹2,400", "ATM-3: withdrawn 32 lakh ⇒ ₹2,000", "ATM-4 ₹2,000", "ATM-5 ₹1,750"],
  why="ATM-4 had the most withdrawals and the most cash withdrawn, but an average of only ₹2,000; ATM-3 also averages "
      "₹2,000; ATM-5 has the lowest average.", secs=60, stim=sid)

tl, tw = sum(ld.values()), sum(wd.values())
assert (tl, tw) == (250, 171) and F(tw, tl) * 100 == F(684, 10) and F(75 + 80 + 64 + 60 + 70, 5) == F(698, 10)
assert r2(F(tl, tw) * 100) == F(14620, 100)
Q(T, "Table with missing values", A,
  "Taking the five ATMs together, what was the overall utilisation (cash withdrawn as a percentage of cash loaded)?",
  "68.4%", ["69.8%", "31.6%", "146.2%"],
  "Fill every missing cell; overall utilisation = total withdrawn ÷ total loaded, not the average of the five rates",
  "Loaded: 40 + 45 + 50 + 75 + 40 = ₹250 lakh (ATM-2: 36 ÷ 0.8 = 45; ATM-5: 28 ÷ 0.7 = 40). Withdrawn: 30 + 36 + 32 + "
  "45 + 28 = ₹171 lakh (ATM-3: 64% of 50 = 32; ATM-4: 2,250 × 2,000 = ₹45 lakh). 171 ÷ 250 = 68.4%.",
  ["Total loaded = 250 lakh", "Total withdrawn = 171 lakh", "171 ÷ 250 = 68.4%"],
  why="69.8% averages the five utilisation rates (ATM-4's is 45 ÷ 75 = 60%) without weighting; 31.6% is the share "
      "left unused; 146.2% divides loaded by withdrawn.", secs=100, stim=sid)

# ================================================================ Quantity Comparison (B5 I3 A3)
T = "Quantity Comparison"
QREL = {">": "Quantity I > Quantity II", ">=": "Quantity I ≥ Quantity II", "<": "Quantity I < Quantity II",
        "<=": "Quantity I ≤ Quantity II", "cbe": "Quantity I = Quantity II or the relationship cannot be established"}


def qc(sub, diff, q1, q2, vals1, vals2, expect, wrong_syms, concept, expl, steps, short=None, why=None, secs=None,
       by=None):
    got = relation(vals1, vals2)
    assert got == expect, (q1, got)
    assert expect not in wrong_syms and "cbe" not in wrong_syms and len(set(wrong_syms)) == 2
    assert all(a != b for a in vals1 for b in vals2), "avoid exactly equal quantities"
    if expect == "cbe":
        third = next(s_ for s_ in (">", "<", ">=", "<=") if s_ not in wrong_syms)
        wrong = [QREL[wrong_syms[0]], QREL[wrong_syms[1]], QREL[third]]
        no_true_distractor(vals1, vals2, [*wrong_syms, third])
    else:
        wrong = [QREL[wrong_syms[0]], QREL["cbe"], QREL[wrong_syms[1]]]
        no_true_distractor(vals1, vals2, wrong_syms)
    Q(T, sub, diff, f"Compare the two quantities and choose the correct option.\nQuantity I: {q1}\nQuantity II: {q2}",
      QREL[expect], wrong, concept, expl, steps, short, why, secs, by=by)


q1v, q2v = F(math.lcm(12, 18, 30)), F(13 ** 2)
assert (q1v, q2v) == (180, 169)
qc("Quantity I vs II", B, "The least common multiple (LCM) of 12, 18 and 30", "The square of the prime number 13", [q1v], [q2v], ">", ["<", "<="],
   "LCM: take the highest power of each prime",
   "12 = 2² × 3, 18 = 2 × 3², 30 = 2 × 3 × 5, so the LCM = 2² × 3² × 5 = 180. 13² = 169. So Quantity I > Quantity II.",
   ["LCM = 4 × 9 × 5 = 180", "13² = 169", "180 > 169"],
   why="'Quantity I < Quantity II' and '≤' come from taking the HCF (6) or a smaller common multiple such as 90 "
       "instead of the LCM.", secs=35)

q1v, q2v = F(2.5 * 3600), F(6.5 * 24 * 60)
assert (q1v, q2v) == (9000, 9360)
qc("Quantity I vs II", B, "The number of seconds in 2.5 hours", "The number of minutes in 6.5 days", [q1v], [q2v],
   "<", [">", ">="],
   "Convert units step by step: 1 hour = 3,600 s; 1 day = 1,440 min",
   "Quantity I = 2.5 × 3,600 = 9,000. Quantity II = 6.5 × 1,440 = 9,360. So Quantity I < Quantity II.",
   ["I: 2.5 × 3,600 = 9,000", "II: 6.5 × 24 × 60 = 9,360", "9,000 < 9,360"],
   why="'Quantity I > Quantity II' and '≥' come from taking a day as 20 hours or 6.5 days as 6 days 5 hours "
       "(6 × 1,440 + 300 = 8,940).", secs=40)

q1v, q2v = 1040 * F(93, 100), 840 * F(115, 100)
assert (q1v, q2v) == (F(9672, 10), 966)
qc("Arithmetic-based comparison", B, "Selling price (₹) of an article marked ₹1,040 and sold at a 7% discount",
   "Selling price (₹) of an article that costs ₹840 and is sold at a 15% profit", [q1v], [q2v], ">", ["<", "<="],
   "Discount: SP = MP × (1 − d%); profit: SP = CP × (1 + p%)",
   "Quantity I = 1,040 × 0.93 = ₹967.20. Quantity II = 840 × 1.15 = ₹966. So Quantity I > Quantity II.",
   ["I: 1,040 − 72.80 = 967.20", "II: 840 + 126 = 966", "967.20 > 966"],
   why="'Quantity I < Quantity II' and '≤' come from judging by the percentages alone (a 15% profit looks larger "
       "than a 7% cut) without working out the two prices.", secs=45)

q1v, q2v = F(4 * 7 * 24), F((6 - 2) * 180)
assert (q1v, q2v) == (672, 720)
qc("Quantity I vs II", B, "The number of hours in 4 weeks", "The sum of the interior angles of a hexagon (in degrees)",
   [q1v], [q2v], "<", [">", ">="],
   "Sum of interior angles of an n-sided polygon = (n − 2) × 180°",
   "Quantity I = 4 × 7 × 24 = 672. Quantity II = (6 − 2) × 180 = 720. So Quantity I < Quantity II.",
   ["I: 28 days × 24 = 672", "II: 4 × 180 = 720", "672 < 720"],
   why="'Quantity I > Quantity II' and '≥' come from taking the hexagon's angle sum as 6 × 90° = 540° or as 360°.",
   secs=40)

q1v, q2v = F(4 * 50, 7), F(420, 15)
assert q1v == F(200, 7) and q2v == 28 and q1v > q2v
qc("Arithmetic-based comparison", B,
   "Days 7 workers take to finish a job that 4 workers finish in 50 days (all work at the same rate)",
   "Minutes a tap pouring 15 litres per minute takes to fill a 420-litre tank", [q1v], [q2v], ">", ["<", "<="],
   "Workers × days is constant for a fixed job; time = capacity ÷ rate",
   "Quantity I = 4 × 50 ÷ 7 = 200/7 ≈ 28.57 days. Quantity II = 420 ÷ 15 = 28 minutes. So Quantity I > Quantity II.",
   ["I: 200 worker-days ÷ 7 ≈ 28.57", "II: 420 ÷ 15 = 28", "28.57 > 28"],
   why="'Quantity I < Quantity II' and '≤' come from rounding 200/7 down to 28 or below, or from taking 420 ÷ 15 "
       "as 30.", secs=45)

xs_, ys_ = [F(7), F(-2)], [F(8), F(9)]
roots_check(1, -5, -14, xs_), roots_check(1, -17, 72, ys_)
qc("Quantity I vs II", I, "The value of x, where x² − 5x − 14 = 0", "The value of y, where y² − 17y + 72 = 0",
   xs_, ys_, "<", [">", ">="],
   "Find every root; compare the largest value of Quantity I with the smallest of Quantity II",
   "I: (x − 7)(x + 2) = 0, so x = 7 or −2. II: (y − 8)(y − 9) = 0, so y = 8 or 9. The largest x (7) is below the "
   "smallest y (8), so Quantity I < Quantity II.",
   ["I: x = 7, −2", "II: y = 8, 9", "7 < 8"],
   why="'Quantity I > Quantity II' and '≥' come from taking the roots of II with the wrong sign (−8 and −9).",
   secs=55)

q1v, q2v = F(22, 7) * F(7, 2) ** 2 * 9, F(7 ** 3)
assert q1v == F(693, 2) and q2v == 343
qc("Arithmetic-based comparison", I,
   "Volume (cm³) of a cylinder of radius 3.5 cm and height 9 cm (take π = 22/7)", "Volume (cm³) of a cube of edge 7 cm",
   [q1v], [q2v], ">", ["<", "<="],
   "Cylinder: V = πr²h; cube: V = a³",
   "Quantity I = 22/7 × 12.25 × 9 = 38.5 × 9 = 346.5 cm³. Quantity II = 7³ = 343 cm³. So Quantity I > Quantity II.",
   ["I: 22/7 × 3.5² = 38.5; × 9 = 346.5", "II: 7³ = 343", "346.5 > 343"],
   why="'Quantity I < Quantity II' and '≤' come from using π = 3, which gives 3 × 12.25 × 9 = 330.75 cm³.",
   secs=55)

q1v, q2v = F(math.factorial(4)), F(math.comb(7, 2))
assert (q1v, q2v) == (24, 21)
qc("Quantity I vs II", I, "The number of arrangements of the letters of the word BANK",
   "The number of ways of choosing 2 people from 7", [q1v], [q2v], ">", ["<", "<="],
   "Arrangements of n different letters = n!; selections = ⁿCᵣ",
   "Quantity I = 4! = 24 (all four letters are different). Quantity II = ⁷C₂ = 21. So Quantity I > Quantity II.",
   ["I: 4! = 24", "II: 7 × 6 ÷ 2 = 21", "24 > 21"],
   why="'Quantity I < Quantity II' and '≤' come from using ⁷P₂ = 42 for the selection, where order does not matter.",
   secs=50)

days = 366
lp = F(2, 7)
coins3 = F(sum(1 for t in itertools.product("HT", repeat=3) if t.count("H") == 2), 8)
assert days - 52 * 7 == 2 and coins3 == F(3, 8) and lp < coins3
qc("Quantity I vs II", A, "The probability that a leap year chosen at random has 53 Sundays",
   "The probability of getting exactly two heads when three fair coins are tossed", [lp], [coins3], "<", [">", ">="],
   "A leap year has 52 full weeks and 2 extra days; count the favourable outcomes for the coins",
   "Quantity I: the 2 extra days are one of 7 equally likely pairs (Sun–Mon, Mon–Tue, …, Sat–Sun); 2 of them contain a "
   "Sunday, so P = 2/7 ≈ 0.286. Quantity II: HHT, HTH, THH — 3 of 8 outcomes, P = 0.375. So Quantity I < Quantity II.",
   ["I: 366 = 52 × 7 + 2 ⇒ P = 2/7", "II: 3/8", "0.286 < 0.375"],
   why="'Quantity I > Quantity II' and '≥' come from counting only one two-head arrangement (HHT), which gives 1/8 "
       "for Quantity II.", secs=80, by=BRUTE)

ages = [(a, b) for b in range(1, 60) for a in [2 * b] if F(a + 10) == F(3, 2) * (b + 10)]
q2v = F(ages[0][0])
q1v = F(80) / F(15, 4)
assert ages == [(20, 10)] and q1v == F(64, 3) and q1v > q2v
qc("Arithmetic-based comparison", A, "Average speed (km/h) of a car that covers 80 km in 3 hours 45 minutes",
   "A's present age (years), if A is now twice as old as B and in 10 years A will be 1.5 times as old as B",
   [q1v], [q2v], ">", ["<", "<="],
   "Convert 3 h 45 min to 3.75 h; set up the age equations with B as the unknown",
   "Quantity I = 80 ÷ 3.75 = 21⅓ km/h. Quantity II: A = 2B and 2B + 10 = 1.5(B + 10), so 0.5B = 5, B = 10 and A = 20. "
   "So Quantity I > Quantity II.",
   ["I: 80 ÷ 3.75 = 21.33", "II: 2B + 10 = 1.5B + 15 ⇒ B = 10, A = 20", "21.33 > 20"],
   why="'Quantity I < Quantity II' and '≤' come from giving A's age 10 years from now (30) instead of his present "
       "age.", secs=90, by=BRUTE)

xs_, ys_ = [F(4), F(1, 2)], [F(1, 3), F(2)]
roots_check(2, -9, 4, xs_), roots_check(3, -7, 2, ys_)
qc("Quantity I vs II", A, "The value of x, where 2x² − 9x + 4 = 0", "The value of y, where 3y² − 7y + 2 = 0",
   xs_, ys_, "cbe", [">", "<="],
   "When the roots interleave, no single relation holds for every pair",
   "I: (2x − 1)(x − 4) = 0, so x = 4 or 1/2. II: (3y − 1)(y − 2) = 0, so y = 1/3 or 2. x = 4 is above both y values, "
   "but x = 1/2 lies between them (above 1/3, below 2). So the relationship cannot be established.",
   ["I: x = 4, 1/2", "II: y = 1/3, 2", "1/2 < 2 but 4 > 2", "Cannot be established"],
   why="'Quantity I > Quantity II' uses only x = 4; '≤' and '<' use only x = 1/2 against y = 2.", secs=80)

# ================================================================ Data Sufficiency (Quant) (B1 I2 A1)
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


cands = [(F(a), F(r)) for a in [s * s for s in range(10, 101, 5)] + [2500] for r in range(5, 51, 5)]
verdict = ds2_verdict(cands, lambda c: c[0] == 2500, lambda c: c[1] == 25, lambda c: 4 * math.isqrt(int(c[0])) * c[1])
assert verdict == "both" and 4 * 50 * 25 == 5000
Q(T, "Two-statement", B,
  f"{DS_PRE}\nQuestion: What is the cost of fencing a square field all round?\n"
  "I. The area of the field is 2,500 m².\n"
  "II. Fencing costs ₹25 per metre.",
  DS2["both"], [DS2["I"], DS2["II"], DS2["neither"]],
  "Cost of fencing = perimeter × rate; the perimeter needs the side, the cost needs the rate",
  "I gives the side (√2,500 = 50 m) and so the perimeter (200 m), but not the rate. II gives the rate but not the "
  "size. Together: 200 × 25 = ₹5,000.",
  ["I alone: perimeter 200 m, rate unknown", "II alone: rate known, size unknown", "Together: 200 × 25 = ₹5,000"],
  why="'I alone' forgets that the rate is needed; 'II alone' forgets that the size is needed; 'not sufficient even "
      "together' misses that the two combine directly.", secs=35, by=BRUTE)

cands = [F(k, 2) for k in range(1, 61)]
verdict = ds2_verdict(cands, lambda a: 6 * a * a == 294, lambda a: 2 * a * a == 98, lambda a: a ** 3)
assert verdict == "either"
Q(T, "Two-statement", I,
  f"{DS_PRE}\nQuestion: What is the volume of the cube?\n"
  "I. The total surface area of the cube is 294 cm².\n"
  "II. The diagonal of one face of the cube is 7√2 cm.",
  DS2["either"], [DS2["I"], DS2["II"], DS2["both"]],
  "Any one measurement of a cube fixes its edge, and hence its volume",
  "I: 6a² = 294 ⇒ a² = 49 ⇒ a = 7 cm, volume 343 cm³ — sufficient. II: face diagonal = a√2 = 7√2 ⇒ a = 7 cm — "
  "sufficient. Either statement alone answers the question.",
  ["I: 6a² = 294 ⇒ a = 7", "II: a√2 = 7√2 ⇒ a = 7", "Volume = 343 cm³ either way"],
  why="'I alone' or 'II alone' overlooks that the other statement also fixes the edge; 'both together' assumes the two "
      "must be combined.", secs=50, by=BRUTE)

cands = [(m, s, e) for m in range(0, 101, 5) for s in range(0, 101, 5) for e in range(0, 101, 5)]
conds = [lambda c: sum(c) == 225, lambda c: c[1] + c[2] == 140, lambda c: c[0] == c[1] + 15]
mp = suff_map(cands, conds, lambda c: c[0])
assert mp == {(0,): False, (1,): False, (2,): False, (0, 1): True, (0, 2): False, (1, 2): False, (0, 1, 2): True}
Q(T, "Three-statement", I,
  f"{DS3_PRE}\nQuestion: How many marks did Ravi score in Mathematics?\n"
  "I. His total in Mathematics, Science and English is 225.\n"
  "II. His average in Science and English is 70.\n"
  "III. His Mathematics marks are 15 more than his Science marks.",
  "Only I and II together are sufficient",
  ["Any two of the three statements together are sufficient", "Only I and III together are sufficient",
   "All three statements together are necessary"],
  "Check every pair: a pair is sufficient only if it fixes the Mathematics marks",
  "I + II: Science + English = 140, so Mathematics = 225 − 140 = 85 — sufficient. I + III: M + S + E = 225 and "
  "M = S + 15 leave E free — not sufficient. II + III: S + E = 140 and M = S + 15 leave S free — not sufficient. No "
  "statement works alone.",
  ["I + II: M = 225 − 2 × 70 = 85", "I + III: E unknown", "II + III: S unknown", "Single statements: not enough"],
  why="'Any two' assumes every pair works, but I + III and II + III each leave a subject's marks free; 'only I and "
      "III' misses that English is still unknown; 'all three' is more than needed.", secs=75, by=BRUTE)

cands = list(range(1, 101))
verdict = ds2_verdict(cands, lambda n: n * n - 13 * n + 36 == 0,
                      lambda n: 36 % n == 0 and n > 1 and math.isqrt(n) ** 2 == n, lambda n: n)
assert verdict == "neither" and [n for n in cands if n * n - 13 * n + 36 == 0 and 36 % n == 0] == [4, 9]
Q(T, "Two-statement", A,
  f"{DS_PRE}\nQuestion: What is the value of the positive integer n?\n"
  "I. n² − 13n + 36 = 0\n"
  "II. n is a factor of 36 and a perfect square greater than 1.",
  DS2["neither"], [DS2["both"], DS2["I"], DS2["either"]],
  "List every value each statement allows; a set of statements is sufficient only if exactly one value survives",
  "I: (n − 4)(n − 9) = 0 ⇒ n = 4 or 9. II: perfect-square factors of 36 greater than 1 are 4, 9 and 36. Together n "
  "can still be 4 or 9, so even both statements together are not sufficient.",
  ["I: n = 4 or 9", "II: n = 4, 9 or 36", "Together: n = 4 or 9", "Not sufficient"],
  why="'Both together' assumes the overlap is a single value, but both 4 and 9 satisfy I and II; 'I alone' and "
      "'either' forget that a quadratic gives two positive roots here.", secs=90, by=BRUTE)

# ================================================================ checks and output
assert len(QUESTIONS) == TOTAL, len(QUESTIONS)
assert len(STIMULI) == 10

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_005_plan.json").read_text(encoding="utf-8"))
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
assert keys == Counter({k: 50 for k in "ABCD"})
assert INDEPENDENT <= {q["question_id"] for q in QUESTIONS}

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_005",
    "created_at": TODAY,
    "notes": "BATCH_005, Quantitative Aptitude part: 200 original questions (60 Basic, 80 Intermediate, 60 Advanced) "
             "with 10 shared DI stimuli on new data sets. Every answer was recomputed by tools/batch_005/quant.py "
             "before writing; questions tagged ai:independent-check were also re-solved from the stem, options and "
             "data set alone by a separate solver. Pending human review.",
    "stimuli": STIMULI,
    "questions": QUESTIONS,
}
out = ROOT / "batches" / "parts" / "BATCH_005_QUANT.json"
if "--dump" in sys.argv:  # blind copies for solvers: no key, no solution
    blind = [{"question_id": q["question_id"], "stimulus_id": q.get("stimulus_id"), "question_text": q["question_text"],
              "options": q["options"]} for q in QUESTIONS]
    Path(sys.argv[-1]).write_text(json.dumps({"stimuli": STIMULI, "questions": blind}, indent=1, ensure_ascii=False),
                                  encoding="utf-8")
    print("blind dump written")
    sys.exit(0)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(QUESTIONS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(keys.items()))}, "
      f"independent-check {len(INDEPENDENT)})")
