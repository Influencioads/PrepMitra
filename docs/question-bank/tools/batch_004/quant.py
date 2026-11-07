"""Writes batches/parts/BATCH_004_QUANT.json: the 200 Quantitative Aptitude questions of BATCH_004.

Every answer is recomputed here before the file is written: arithmetic with exact fractions, series regenerated
from their rule (wrong-number series: exactly one term differs from the regenerated series), quadratic roots
substituted back into the equations, probabilities and arrangements counted by brute force, data-sufficiency
statements checked by enumerating candidate cases, approximation answers checked to be the option nearest the
exact value by a clear margin. If any assertion fails, nothing is written.

Structure and helpers follow tools/batch_003/quant.py (relation-option guards, balanced key shuffler with a new
seed, approximation margin check, set-size asserts). Contexts, data sets and number templates are new: none of
the DI themes of batches 0-3 is reused, and the arithmetic templates were chosen after reading all earlier stems.

    python tools/batch_004/quant.py          (run from docs/question-bank)
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

# Balanced answer keys: exactly 50 of each letter, order fixed by the seed (new seed for batch 4).
_rng = random.Random(20261105 + 4)
KEYS = list("ABCD" * (TOTAL // 4))
_rng.shuffle(KEYS)

QUESTIONS, STIMULI = [], []
_set_pos = {}
_FIRST_ID = 606
_FIRST_STIM = 4001
RECOMPUTE = ["script:recompute", "ai:author-solve"]
BRUTE = ["script:recompute", "script:brute-force-unique", "ai:author-solve"]

# Questions that a separate solver re-answered from the stem, options and data set alone (no key, no solution)
# and whose answer matched the key. Only these carry ai:independent-check. Every third question
# (BANK_QUANT_000606, _000609, ..., _000804: 67 questions) was given to two separate solver agents; all 67 answers
# matched the key. BANK_QUANT_000783 is left untagged because one of its distractors was replaced afterwards.
INDEPENDENT = {f"BANK_QUANT_{n:06d}" for n in range(606, 806, 3)} - {"BANK_QUANT_000783"}

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

# ================================================================ Simplification (B3 I6 A4)
T = "Simplification"
v = (F(468, 13) + 17 * 4) / 8
assert v == 13 and F(468, 13) == 36 and (32 + 68) / F(8) == F(25, 2)
Q(T, "BODMAS", B, "What will come in place of the question mark (?)?\n(468 ÷ 13 + 17 × 4) ÷ ? = 8",
  "13", ["104", "832", "12.5"],
  "Simplify the bracket first (÷ and × before +), then undo the outer division",
  "Inside the bracket: 468 ÷ 13 = 36 and 17 × 4 = 68, so the bracket is 104. Then 104 ÷ ? = 8 gives ? = 104 ÷ 8 = 13.",
  ["468 ÷ 13 = 36", "17 × 4 = 68", "36 + 68 = 104", "104 ÷ ? = 8 ⇒ ? = 13"],
  why="104 is the value of the bracket, not of ?; 832 multiplies 104 by 8 instead of dividing; 12.5 takes 468 ÷ 13 "
      "as 32.", secs=35)

v = 1 + 1 / (2 + 1 / (3 + F(1, 4)))
assert v == F(43, 30) and 1 + 1 / (2 + (3 + F(1, 4))) == F(25, 21) and 1 + F(1, 2) + F(1, 3) + F(1, 4) == F(25, 12)
Q(T, "Fractions and decimals", B, "Simplify: 1 + 1/(2 + 1/(3 + 1/4))",
  "43/30", ["30/43", "25/21", "25/12"],
  "Continued fraction: work from the innermost level outwards, inverting at each step",
  "3 + 1/4 = 13/4, so 1/(13/4) = 4/13. Then 2 + 4/13 = 30/13, so 1/(30/13) = 13/30. Finally 1 + 13/30 = 43/30.",
  ["3 + 1/4 = 13/4 ⇒ its reciprocal is 4/13", "2 + 4/13 = 30/13 ⇒ its reciprocal is 13/30", "1 + 13/30 = 43/30"],
  why="30/43 inverts the final answer; 25/21 forgets to invert 13/4 (uses 2 + 13/4); 25/12 adds 1 + 1/2 + 1/3 + 1/4 "
      "as separate fractions.", secs=45)

assert 17 ** 3 == 4913 and 23 ** 2 == 529 and (17 + 23 - 14) ** 2 == 676
assert (17 + 23 + 14) ** 2 == 2916 and (13 + 23 - 14) ** 2 == 484
Q(T, "Square and cube roots", B, "What will come in place of the question mark (?)?\n√? + 14 = ∛4913 + √529",
  "676", ["26", "2,916", "484"],
  "Evaluate the known roots, isolate √?, then square",
  "∛4913 = 17 (17³ = 4,913) and √529 = 23, so the right side is 40. Then √? = 40 − 14 = 26 and ? = 26² = 676.",
  ["∛4913 = 17", "√529 = 23", "√? = 40 − 14 = 26", "? = 26² = 676"],
  short="4913 ends in 3, so its cube root ends in 7; 4913 lies between 10³ and 20³, so the root is 17.",
  why="26 is √?, not ?; 2,916 = 54² adds the 14 instead of subtracting it; 484 = 22² takes ∛4913 as 13.", secs=40)

vals = {"√6 + √8": math.sqrt(6) + math.sqrt(8), "√2 + √12": math.sqrt(2) + math.sqrt(12),
        "√5 + √9": math.sqrt(5) + 3, "√3 + √11": math.sqrt(3) + math.sqrt(11)}
assert max(vals, key=vals.get) == "√6 + √8"
for k_, (a_, b_) in {"√6 + √8": (6, 8), "√2 + √12": (2, 12), "√5 + √9": (5, 9), "√3 + √11": (3, 11)}.items():
    assert near(vals[k_] ** 2, 14 + 2 * math.sqrt(a_ * b_))
Q(T, "Surds and indices", I, "Which of the following is the largest?",
  "√6 + √8", ["√2 + √12", "√5 + √9", "√3 + √11"],
  "Compare positive sums by comparing their squares: (√a + √b)² = a + b + 2√(ab)",
  "In every option the numbers under the roots add up to 14, so each square is 14 + 2√(ab). The products ab are 48, "
  "24, 45 and 33, and 48 is the largest. So √6 + √8 is the largest.",
  ["(√6 + √8)² = 14 + 2√48", "(√2 + √12)² = 14 + 2√24", "(√5 + √9)² = 14 + 2√45", "(√3 + √11)² = 14 + 2√33",
   "Largest product 48 ⇒ √6 + √8"],
  short="With a fixed sum a + b, √a + √b is largest when a and b are closest to each other (6 and 8).",
  why="√2 + √12 has the largest single term but the smallest square (14 + 2√24); √5 + √9 is tempting because √9 = 3 is "
      "exact, but 45 < 48; √3 + √11 gives only 14 + 2√33.", secs=60)

v = 96 / F(4 * 3) - 2 * (15 - (6 + (8 - 5)))
assert v == -4 and 96 / 4 * 3 - 12 == 60 and 8 - 2 * (15 - 6 + 3) == -16
Q(T, "BODMAS", I, "Simplify: 96 ÷ 4 of 3 − 2 × [15 − {6 + (8 − 5)}]",
  "−4", ["60", "−16", "4"],
  "BODMAS with 'of': brackets innermost first, then 'of' before ÷, then ×, then −",
  "Brackets: 8 − 5 = 3, 6 + 3 = 9, 15 − 9 = 6, so the second term is 2 × 6 = 12. 'Of' comes before division: 4 of 3 "
  "= 12 and 96 ÷ 12 = 8. So the value is 8 − 12 = −4.",
  ["(8 − 5) = 3", "{6 + 3} = 9", "[15 − 9] = 6 ⇒ 2 × 6 = 12", "4 of 3 = 12 ⇒ 96 ÷ 12 = 8", "8 − 12 = −4"],
  why="60 divides 96 by 4 first and then multiplies by 3, ignoring that 'of' comes before ÷; −16 drops the curly "
      "bracket and computes 15 − 6 + 3 = 12; 4 subtracts the wrong way (12 − 8).", secs=55)

fr = [F(5, 8), F(7, 12), F(9, 16), F(11, 18)]
assert max(fr) == F(5, 8) and min(fr) == F(9, 16) and max(fr) - min(fr) == F(1, 16)
assert F(5, 8) - F(7, 12) == F(1, 24) and F(11, 18) - F(9, 16) == F(7, 144) and F(5, 8) - F(11, 18) == F(1, 72)
Q(T, "Fractions and decimals", I,
  "What is the difference between the largest and the smallest of the fractions 5/8, 7/12, 9/16 and 11/18?",
  "1/16", ["1/24", "7/144", "1/72"],
  "Compare fractions on a common denominator (here 144) or by their decimal values",
  "Over 144: 5/8 = 90/144, 7/12 = 84/144, 9/16 = 81/144 and 11/18 = 88/144. The largest is 5/8 and the smallest is "
  "9/16, so the difference is 9/144 = 1/16.",
  ["5/8 = 90/144", "7/12 = 84/144", "9/16 = 81/144", "11/18 = 88/144", "90/144 − 81/144 = 9/144 = 1/16"],
  why="1/24 takes 7/12 as the smallest; 7/144 takes 11/18 as the largest; 1/72 takes 11/18 as the smallest.",
  secs=60)

assert 1944 == 2 ** 3 * 3 ** 5 and 18 ** 3 == 1944 * 3
assert round((1944 * 9) ** (1 / 3)) ** 3 != 1944 * 9 and round((1944 * 6) ** (1 / 3)) ** 3 != 1944 * 6
assert round((1944 * 2) ** (1 / 3)) ** 3 != 1944 * 2
Q(T, "Square and cube roots", I,
  "What is the least number by which 1,944 must be multiplied so that the product is a perfect cube?",
  "3", ["9", "6", "2"],
  "In a perfect cube every prime appears with a power that is a multiple of 3",
  "1,944 = 2³ × 3⁵. The power of 2 is already 3; the power of 3 is 5, which needs one more 3 to reach 6. So the "
  "least multiplier is 3, and 1,944 × 3 = 5,832 = 18³.",
  ["1,944 = 8 × 243 = 2³ × 3⁵", "2³ is complete", "3⁵ needs one more 3 ⇒ 3⁶", "Multiplier = 3; check 5,832 = 18³"],
  why="9 would give 3⁷, which is not a multiple of 3; 6 also multiplies by 2 and spoils the complete 2³; 2 assumes "
      "the power of 2 is the incomplete one.", secs=55)

ka = 30.0
a_, b_, c_ = math.log(ka, 2), math.log(ka, 3), math.log(ka, 6)
assert near(c_, a_ * b_ / (a_ + b_)) and not near(c_, (a_ + b_) / (a_ * b_)) and not near(c_, math.sqrt(a_ * b_))
Q(T, "Surds and indices", I, "If 2ᵃ = 3ᵇ = 6ᶜ, where a, b and c are non-zero, then c equals:",
  "ab/(a + b)", ["(a + b)/ab", "a + b", "√(ab)"],
  "Set each power equal to k and use the laws of indices: 2 = k^(1/a), 3 = k^(1/b), 6 = k^(1/c)",
  "Let 2ᵃ = 3ᵇ = 6ᶜ = k. Then 2 = k^(1/a), 3 = k^(1/b) and 6 = k^(1/c). Since 6 = 2 × 3, k^(1/c) = k^(1/a + 1/b), "
  "so 1/c = 1/a + 1/b = (a + b)/ab and c = ab/(a + b).",
  ["2 = k^(1/a), 3 = k^(1/b), 6 = k^(1/c)", "6 = 2 × 3 ⇒ 1/c = 1/a + 1/b", "1/c = (a + b)/ab", "c = ab/(a + b)"],
  why="(a + b)/ab is 1/c, not c; a + b adds the exponents instead of their reciprocals; √(ab) is a guess with no "
      "basis in the laws of indices.", secs=70)

rhs = F(25, 100) * 1536 - 288
v = rhs / (F(3, 5) * F(4, 7))
assert rhs == 96 and v == 280 and rhs * F(5, 3) == 160 and rhs * F(7, 4) == 168
assert F(25, 100) * (1536 - 288) * F(35, 12) == 910
Q(T, "Fractions and decimals", I,
  "What will come in place of the question mark (?)?\n3/5 of 4/7 of ? = 25% of 1,536 − 288",
  "280", ["160", "168", "910"],
  "'Of' means multiply; divide the right side by the product of the fractions",
  "Right side: 25% of 1,536 = 384, and 384 − 288 = 96. Left side: 3/5 × 4/7 = 12/35 of ?. So ? = 96 × 35/12 = 280.",
  ["25% of 1,536 = 384", "384 − 288 = 96", "3/5 × 4/7 = 12/35", "? = 96 × 35/12 = 280"],
  why="160 uses only the 3/5; 168 uses only the 4/7; 910 takes 25% of (1,536 − 288) instead of subtracting 288 after "
      "taking 25%.", secs=55)

r2_, r3_, r6_ = math.sqrt(2), math.sqrt(3), math.sqrt(6)
v = 1 / (1 + r2_ + r3_)
assert near(v, (2 + r2_ - r6_) / 4)
assert not near(v, (2 + r2_ + r6_) / 4) and not near(v, (1 + r2_ - r3_) / 2) and not near(v, (r6_ - r2_ - 2) / 4)
Q(T, "Surds and indices", A, "Rationalise the denominator: 1/(1 + √2 + √3)",
  "(2 + √2 − √6)/4", ["(2 + √2 + √6)/4", "(1 + √2 − √3)/2", "(√6 − √2 − 2)/4"],
  "Group (1 + √2) and multiply by (1 + √2) − √3; then rationalise the remaining √2",
  "Multiply by (1 + √2 − √3): the denominator becomes (1 + √2)² − 3 = 3 + 2√2 − 3 = 2√2. So the value is "
  "(1 + √2 − √3)/(2√2). Multiply top and bottom by √2: (√2 + 2 − √6)/4.",
  ["Denominator × (1 + √2 − √3) = (1 + √2)² − (√3)² = 2√2", "Value = (1 + √2 − √3)/(2√2)",
   "× √2/√2 ⇒ (√2 + 2 − √6)/4", "Check: ≈ 0.2412 = 1/4.146"],
  why="(2 + √2 + √6)/4 has the sign of √6 wrong; (1 + √2 − √3)/2 takes the denominator 2√2 as 2; (√6 − √2 − 2)/4 is "
      "the negative of the answer.", secs=100)

t_ = 3
a_val = ((3 + math.sqrt(5)) / 2) ** 3
assert near(a_val ** (1 / 3) + a_val ** (-1 / 3), 3) and near(a_val + 1 / a_val, t_ ** 3 - 3 * t_)
assert t_ ** 3 - 3 * t_ == 18
Q(T, "Surds and indices", A, "If a > 0 and a^(1/3) + a^(−1/3) = 3, what is the value of a + 1/a?",
  "18", ["27", "24", "7"],
  "Let t = a^(1/3) + a^(−1/3); then t³ = a + 1/a + 3t, because a^(1/3) × a^(−1/3) = 1",
  "Cube both sides: (a^(1/3) + a^(−1/3))³ = a + 1/a + 3 × a^(1/3) × a^(−1/3) × (a^(1/3) + a^(−1/3)) = a + 1/a + 3 × 3. "
  "So 27 = a + 1/a + 9 and a + 1/a = 18.",
  ["(x + y)³ = x³ + y³ + 3xy(x + y)", "x = a^(1/3), y = a^(−1/3), xy = 1", "27 = (a + 1/a) + 3 × 1 × 3",
   "a + 1/a = 27 − 9 = 18"],
  why="27 forgets the 3xy(x + y) term; 24 subtracts 3 instead of 3 × 3; 7 squares instead of cubing (3² − 2 = 7 gives "
      "a^(2/3) + a^(−2/3)).", secs=90)

x_ = 0.0
for _ in range(60):
    x_ = math.sqrt(6 + x_)
assert near(x_, 3, 1e-9) and 3 * 3 - 3 - 6 == 0 and (-2) ** 2 - (-2) - 6 == 0
Q(T, "Square and cube roots", A, "Find the value of √(6 + √(6 + √(6 + …))), where the pattern continues without end.",
  "3", ["2", "√6", "6"],
  "An endless nested root repeats itself: call it x, so x = √(6 + x), and keep the positive root",
  "Let x = √(6 + √(6 + …)). The part under the first root after 6 is x itself, so x = √(6 + x), x² = 6 + x and "
  "x² − x − 6 = (x − 3)(x + 2) = 0. A square root is positive, so x = 3.",
  ["x = √(6 + x)", "x² − x − 6 = 0", "(x − 3)(x + 2) = 0", "x > 0 ⇒ x = 3"],
  why="2 takes the size of the rejected root −2; √6 (≈ 2.45) stops after the first square root; 6 forgets the outer "
      "square root.", secs=80)

v = 1
for k in range(2, 11):
    v *= 1 - F(1, k * k)
assert v == F(11, 20)
p_ = q_ = 1
for k in range(2, 11):
    p_ *= F(k - 1, k)
    q_ *= F(k + 1, k)
assert p_ == F(1, 10) and q_ == F(11, 2) and F(1, 2) * F(10, 9) == F(5, 9)
Q(T, "Fractions and decimals", A, "Find the value of (1 − 1/4)(1 − 1/9)(1 − 1/16) … (1 − 1/100).",
  "11/20", ["1/10", "11/2", "5/9"],
  "Factor each term: 1 − 1/k² = (k − 1)(k + 1)/k², then let the factors telescope",
  "Each factor is (k − 1)/k × (k + 1)/k for k = 2 to 10. The product of (k − 1)/k is 1/10, and the product of "
  "(k + 1)/k is 11/2. So the value is 1/10 × 11/2 = 11/20.",
  ["1 − 1/k² = (k − 1)/k × (k + 1)/k, k = 2, …, 10", "1/2 × 2/3 × … × 9/10 = 1/10",
   "3/2 × 4/3 × … × 11/10 = 11/2", "1/10 × 11/2 = 11/20"],
  why="1/10 keeps only the (k − 1)/k factors; 11/2 keeps only the (k + 1)/k factors; 5/9 stops the product at "
      "1 − 1/81.", secs=90)

# ================================================================ Approximation (B6 I2 A2)
T = "Approximation"
exact = 0.4003 * 0.5502 * 1999.8
nearest(exact, [440, 400, 480, 360], 440)
Q(T, "Percentage approximation", B, APPROX + "40.03% of 55.02% of 1999.8 ≈ ?",
  "440", ["400", "480", "360"],
  "A percentage of a percentage: multiply the two decimal fractions",
  "40.03% ≈ 40%, 55.02% ≈ 55% and 1999.8 ≈ 2000. 55% of 2000 = 1,100 and 40% of 1,100 = 440.",
  ["55% of 2000 = 1,100", "40% of 1,100 = 440"],
  why="400 rounds 55.02% down to 50%; 360 uses 45% instead of 55%; 480 uses 60%. Each is 40 or more away from the "
      "exact value (about 440.4).", secs=35)

exact = 26.98 ** (1 / 3) * 124.9 ** (1 / 3) * math.sqrt(15.97)
nearest(exact, [60, 45, 75, 80], 60)
Q(T, "Root approximation", B, APPROX + "∛26.98 × ∛124.9 × √15.97 ≈ ?",
  "60", ["45", "75", "80"],
  "Round each number to the nearest perfect cube or square: 27 = 3³, 125 = 5³, 16 = 4²",
  "∛26.98 ≈ 3, ∛124.9 ≈ 5 and √15.97 ≈ 4, so the product ≈ 3 × 5 × 4 = 60.",
  ["∛27 = 3", "∛125 = 5", "√16 = 4", "3 × 5 × 4 = 60"],
  why="45 takes √15.97 as 3; 75 takes ∛124.9 as 5 but √15.97 as 5; 80 takes ∛26.98 as 4. All are 15 or more away from "
      "the exact value (about 59.9).", secs=35)

exact = 4.97 * 3.2 + 6.02 * 8 / 3
nearest(exact, [32, 28, 36, 40], 32)
Q(T, "Mixed approximation", B, APPROX + "4.97 × 3⅕ + 6.02 × 2⅔ ≈ ?",
  "32", ["28", "36", "40"],
  "Round the decimals to whole numbers; turn mixed numbers into fractions that cancel neatly",
  "4.97 ≈ 5 and 3⅕ = 16/5, so the first product ≈ 16. 6.02 ≈ 6 and 2⅔ = 8/3, so the second ≈ 16. Total ≈ 32.",
  ["5 × 16/5 = 16", "6 × 8/3 = 16", "16 + 16 = 32"],
  why="28 and 36 are 4 away and 40 is 8 away from the exact value (about 31.96); 36 would need 2⅔ read as 3⅓.",
  secs=40)

exact = 19.98 ** 2 - 7.03 ** 2 * 4.97
nearest(exact, [155, 145, 165, 1755], 155)
Q(T, "Mixed approximation", B, APPROX + "19.98² − 7.03² × 4.97 ≈ ?",
  "155", ["145", "165", "1,755"],
  "Squares first, then multiplication, then subtraction",
  "19.98² ≈ 20² = 400. 7.03² ≈ 49, and 49 × 5 = 245. So the value ≈ 400 − 245 = 155.",
  ["20² = 400", "7² × 5 = 245", "400 − 245 = 155"],
  why="1,755 subtracts first, (400 − 49) × 5; 145 and 165 are 10 away from the rounded value (the exact value is "
      "about 153.6).", secs=40)

exact = 0.1796 * 2449.7 / 9.02
nearest(exact, [49, 44, 54, 59], 49)
Q(T, "Percentage approximation", B, APPROX + "17.96% of 2449.7 ÷ 9.02 ≈ ?",
  "49", ["44", "54", "59"],
  "Round the percentage and the numbers, then divide",
  "17.96% ≈ 18% and 2449.7 ≈ 2450, so 18% of 2450 = 441. Then 441 ÷ 9 = 49.",
  ["18% of 2450 = 441", "441 ÷ 9 = 49"],
  why="44 and 54 are 5 away and 59 is 10 away from the exact value (about 48.8); 44 would come from 16% of 2450 ÷ 9.",
  secs=40)

exact = 3599.8 / 24.02 / 5.98
nearest(exact, [25, 20, 30, 900], 25)
Q(T, "Mixed approximation", B, APPROX + "3599.8 ÷ 24.02 ÷ 5.98 ≈ ?",
  "25", ["20", "30", "900"],
  "Successive divisions are done left to right (equivalently, divide by the product 24 × 6)",
  "3599.8 ÷ 24.02 ≈ 3600 ÷ 24 = 150, and 150 ÷ 6 = 25.",
  ["3600 ÷ 24 = 150", "150 ÷ 6 = 25"],
  short="3600 ÷ (24 × 6) = 3600 ÷ 144 = 25.",
  why="900 multiplies by 6 at the second step (3600 ÷ 24 × 6); 20 and 30 are 5 away from the exact value (about "
      "25.06).", secs=35)

exact = 0.2501 * 3359.8 / math.sqrt(1763.9)
nearest(exact, [20, 24, 16, 28], 20)
Q(T, "Root approximation", I, APPROX + "√1763.9 × ? ≈ 25.01% of 3359.8",
  "20", ["24", "16", "28"],
  "1764 = 42²; 25% is one-quarter",
  "√1763.9 ≈ √1764 = 42. 25.01% of 3359.8 ≈ 3360 ÷ 4 = 840. So 42 × ? ≈ 840 and ? ≈ 20.",
  ["√1764 = 42", "¼ × 3360 = 840", "? = 840 ÷ 42 = 20"],
  why="24 and 16 take √1763.9 as 35 or 52.5; 28 takes it as 30. All are 4 or more away from the exact value (about "
      "20.0).", secs=50)

exact = math.sqrt(14.98 ** 2 + 19.97 ** 2)
nearest(exact, [25, 35, 30, 20], 25)
Q(T, "Mixed approximation", I, APPROX + "?² ≈ 14.98² + 19.97² (? is positive)",
  "25", ["35", "30", "20"],
  "Square, add, then take the positive square root; 15, 20, 25 is a Pythagorean triple",
  "14.98² ≈ 225 and 19.97² ≈ 400, so ?² ≈ 625 and ? ≈ 25.",
  ["15² = 225", "20² = 400", "225 + 400 = 625", "√625 = 25"],
  why="35 adds 15 and 20 (the roots do not add like that); 30 and 20 are 5 away from the exact value (about 24.96).",
  secs=50)

exact = 1295.9 ** 0.25 * 255.8 ** 0.75
nearest(exact, [384, 96, 1536, 64], 384)
Q(T, "Root approximation", A, APPROX + "1295.9^(1/4) × 255.8^(3/4) ≈ ?",
  "384", ["96", "1,536", "64"],
  "Round to perfect powers: 1296 = 6⁴ and 256 = 4⁴, so x^(3/4) = (x^(1/4))³",
  "1295.9^(1/4) ≈ 1296^(1/4) = 6. 255.8^(3/4) ≈ (256^(1/4))³ = 4³ = 64. Product ≈ 6 × 64 = 384.",
  ["1296 = 6⁴ ⇒ fourth root 6", "256 = 4⁴ ⇒ 256^(3/4) = 4³ = 64", "6 × 64 = 384"],
  why="96 uses 256^(1/2) = 16 for the second factor; 1,536 ignores the exponent 3/4 and uses 256; 64 leaves out the "
      "first factor.", secs=70)

exact = ((39.97 ** 2 / 7.99 - 0.2202 * 799.9) * 6.98 / 13.97) ** 2
nearest(exact, [144, 576, 36, 169], 144)
Q(T, "Mixed approximation", A, APPROX + "√? ÷ 6.98 × 13.97 + 22.02% of 799.9 ≈ 39.97² ÷ 7.99",
  "144", ["576", "36", "169"],
  "Round, simplify the right side, isolate √?, then square",
  "Right side ≈ 40² ÷ 8 = 1600 ÷ 8 = 200. 22% of 800 = 176. So √? × 14 ÷ 7 = √? × 2 ≈ 200 − 176 = 24, √? ≈ 12 and "
  "? ≈ 144.",
  ["40² ÷ 8 = 200", "22% of 800 = 176", "√? × 2 ≈ 24 ⇒ √? ≈ 12", "? ≈ 144"],
  why="576 = 24² forgets the factor 2 (÷ 7 × 14); 36 = 6² divides 24 by 4; 169 = 13² is more than 25 away from the "
      "exact value (about 141.5).", secs=90)

# ================================================================ Number Series (B2 I6 A7)
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


s = series_from(6, lambda t, k: t + k * (k + 1) // 2, 7)
assert s == [6, 7, 10, 16, 26, 41, 62] and diffs(s) == [1, 3, 6, 10, 15, 21]
Q(T, "Pattern: differences", B, SERIES_Q + "6, 7, 10, 16, 26, 41, ?",
  "62", ["57", "61", "66"],
  "The differences are the triangular numbers 1, 3, 6, 10, 15, …",
  "The differences are 1, 3, 6, 10, 15; each grows by one more than the last (+2, +3, +4, +5). The next difference is "
  "15 + 6 = 21, so the next term is 41 + 21 = 62.",
  ["Differences: 1, 3, 6, 10, 15", "They rise by 2, 3, 4, 5 ⇒ next rise 6", "Next difference = 21", "41 + 21 = 62"],
  why="57 adds 16 (15 + 1); 61 adds 20 (rise of 5 repeated); 66 adds 25 (treats the differences as squares).",
  secs=35)

s = [F(120, k) for k in range(1, 7)]
assert s == [120, 60, 40, 30, 24, 20]
Q(T, "Missing number series", B, MISSING_Q + "120, 60, ?, 30, 24, 20",
  "40", ["45", "48", "36"],
  "Each term is 120 divided by 1, 2, 3, 4, 5, 6 in turn",
  "120 ÷ 1 = 120, 120 ÷ 2 = 60, 120 ÷ 4 = 30, 120 ÷ 5 = 24 and 120 ÷ 6 = 20, so the missing term is 120 ÷ 3 = 40.",
  ["120 ÷ 1 = 120", "120 ÷ 2 = 60", "120 ÷ 3 = 40", "120 ÷ 4 = 30, 120 ÷ 5 = 24, 120 ÷ 6 = 20"],
  short="Equivalently, multiply by 1/2, 2/3, 3/4, 4/5, 5/6: 60 × 2/3 = 40.",
  why="45 assumes equal steps from 60 down to 30; 48 is 120 × 2/5; 36 extends the last fall of 6 (30 − 24) "
      "backwards to 30 + 6.",
  secs=40)

s = [n ** n for n in range(1, 7)]
assert s == [1, 4, 27, 256, 3125, 46656]
Q(T, "Pattern: squares and cubes", I, MISSING_Q + "1, 4, 27, 256, ?, 46,656",
  "3,125", ["625", "1,024", "3,025"],
  "Each term is n raised to the power n",
  "1 = 1¹, 4 = 2², 27 = 3³, 256 = 4⁴ and 46,656 = 6⁶, so the missing term is 5⁵ = 3,125.",
  ["1¹ = 1, 2² = 4, 3³ = 27, 4⁴ = 256", "5⁵ = 3,125", "6⁶ = 46,656 confirms the rule"],
  why="625 = 5⁴ and 1,024 = 4⁵ mix up base and power; 3,025 = 55² has no link to the pattern.", secs=50)

odd_, even_ = series_from(3, lambda t, k: 2 * t, 4), series_from(50, lambda t, k: t - 5, 4)
s = [x for pair in zip(odd_, even_) for x in pair]
assert s == [3, 50, 6, 45, 12, 40, 24, 35]
Q(T, "Pattern: differences", I, SERIES_Q + "3, 50, 6, 45, 12, 40, 24, ?",
  "35", ["48", "30", "29"],
  "Two series are interleaved: odd positions double, even positions fall by 5",
  "Odd positions: 3, 6, 12, 24 (× 2). Even positions: 50, 45, 40 (− 5). The ? is in an even position, so it is "
  "40 − 5 = 35.",
  ["Odd positions: 3 → 6 → 12 → 24", "Even positions: 50 → 45 → 40", "? is the 8th term (even) ⇒ 40 − 5 = 35"],
  why="48 continues the doubling series, which belongs to the odd positions; 30 subtracts 10 from 40; 29 applies "
      "the even-position rule (± 5) to the last odd-position term 24.", secs=50)

s = series_from(F(4), lambda t, k: t * (1 + F(k, 2)), 6)
assert s == [4, 6, 12, 30, 90, 315]
Q(T, "Pattern: multiply-add", I, SERIES_Q + "4, 6, 12, 30, 90, ?",
  "315", ["270", "360", "225"],
  "The multiplier rises by 0.5 each time: × 1.5, × 2, × 2.5, × 3, …",
  "4 × 1.5 = 6, 6 × 2 = 12, 12 × 2.5 = 30, 30 × 3 = 90, so the next term is 90 × 3.5 = 315.",
  ["4 × 1.5 = 6", "6 × 2 = 12", "12 × 2.5 = 30", "30 × 3 = 90", "90 × 3.5 = 315"],
  why="270 multiplies by 3 again; 360 jumps to × 4; 225 multiplies by 2.5.", secs=55)

s = list(itertools.accumulate(k * k for k in range(1, 7)))
assert s == [1, 5, 14, 30, 55, 91]
Q(T, "Pattern: squares and cubes", I, SERIES_Q + "1, 5, 14, 30, 55, ?",
  "91", ["80", "104", "89"],
  "Each term is the sum of the first n perfect squares (the differences are 2², 3², 4², …)",
  "The differences are 4, 9, 16, 25 = 2², 3², 4², 5². The next difference is 6² = 36, so the next term is "
  "55 + 36 = 91 (= 1² + 2² + … + 6²).",
  ["5 − 1 = 4", "14 − 5 = 9", "30 − 14 = 16", "55 − 30 = 25", "55 + 36 = 91"],
  short="Sum of squares formula: 6 × 7 × 13 ÷ 6 = 91.",
  why="80 adds 25 again; 104 adds 49 and skips 36; 89 adds 34.", secs=50)

s = series_from(9, lambda t, k: t + 2 ** k - 1, 7)
assert s == [9, 10, 13, 20, 35, 66, 129]
Q(T, "Pattern: differences", I, SERIES_Q + "9, 10, 13, 20, 35, 66, ?",
  "129", ["128", "97", "132"],
  "The differences are one less than powers of 2: 1, 3, 7, 15, 31, …",
  "The differences are 1, 3, 7, 15, 31 = 2¹ − 1, 2² − 1, …, 2⁵ − 1. The next is 2⁶ − 1 = 63, so the term is "
  "66 + 63 = 129.",
  ["Differences: 1, 3, 7, 15, 31", "Each = 2ⁿ − 1 (or previous × 2 + 1)", "Next = 63", "66 + 63 = 129"],
  why="128 adds 62 (doubles 31 but forgets the + 1); 97 adds 31 again; 132 doubles 66.", secs=55)

s = series_from(3, lambda t, k: 2 * t + k * k, 6)
assert s == [3, 7, 18, 45, 106, 237] and 18 * 2 == 36 and 18 * 2 + 7 == 43
Q(T, "Missing number series", I, MISSING_Q + "3, 7, 18, ?, 106, 237",
  "45", ["43", "36", "52"],
  "Each term = previous × 2 + n², with n = 1, 2, 3, …",
  "3 × 2 + 1 = 7, 7 × 2 + 4 = 18, 18 × 2 + 9 = 45, 45 × 2 + 16 = 106 and 106 × 2 + 25 = 237, which confirms it.",
  ["3 × 2 + 1² = 7", "7 × 2 + 2² = 18", "18 × 2 + 3² = 45", "45 × 2 + 4² = 106", "106 × 2 + 5² = 237"],
  why="43 adds 7, reading the additions 1, 4 as rising by 3; 36 only doubles; 52 does not give 106 at the next step "
      "(52 × 2 + 16 = 120).", secs=60)

s = series_from(3, lambda t, k: t * [2, 3, 5, 7, 11][k - 1], 6)
assert s == [3, 6, 18, 90, 630, 6930]
Q(T, "Pattern: multiply-add", A, SERIES_Q + "3, 6, 18, 90, 630, ?",
  "6,930", ["5,670", "7,560", "6,300"],
  "The multipliers are the prime numbers 2, 3, 5, 7, 11, …",
  "3 × 2 = 6, 6 × 3 = 18, 18 × 5 = 90, 90 × 7 = 630. The next prime is 11, so the next term is 630 × 11 = 6,930.",
  ["× 2, × 3, × 5, × 7", "Next prime = 11", "630 × 11 = 6,930"],
  why="5,670 multiplies by 9 (odd numbers); 7,560 multiplies by 12; 6,300 multiplies by 10.", secs=60)

s = series_from(4, lambda t, k: t + (k + 1) ** 3 - 1, 6)
assert s == [4, 11, 37, 100, 224, 439]
Q(T, "Pattern: squares and cubes", A, SERIES_Q + "4, 11, 37, 100, 224, ?",
  "439", ["440", "349", "441"],
  "The differences are one less than cubes: 2³ − 1, 3³ − 1, …",
  "The differences are 7, 26, 63, 124 = 2³ − 1, 3³ − 1, 4³ − 1, 5³ − 1. The next is 6³ − 1 = 215, so the term is "
  "224 + 215 = 439.",
  ["11 − 4 = 7 = 8 − 1", "37 − 11 = 26 = 27 − 1", "100 − 37 = 63 = 64 − 1", "224 − 100 = 124 = 125 − 1",
   "224 + (216 − 1) = 439"],
  why="440 adds 216 and forgets the − 1; 349 adds 125 (5³) again; 441 reads the differences as cubes plus 1 and "
      "adds 217.", secs=75)

s = [2, 3, 6]
while len(s) < 7:
    s.append(s[-1] + s[-2] + s[-3])
assert s == [2, 3, 6, 11, 20, 37, 68]
Q(T, "Missing number series", A, SERIES_Q + "2, 3, 6, 11, 20, 37, ?",
  "68", ["57", "74", "71"],
  "Each term is the sum of the three terms before it",
  "2 + 3 + 6 = 11, 3 + 6 + 11 = 20, 6 + 11 + 20 = 37, so the next term is 11 + 20 + 37 = 68.",
  ["2 + 3 + 6 = 11", "3 + 6 + 11 = 20", "6 + 11 + 20 = 37", "11 + 20 + 37 = 68"],
  why="57 adds only the last two terms; 74 doubles 37; 71 adds 34, doubling the last difference (17) instead of "
      "adding the three previous terms.", secs=75)

dd = [1, 8, 9, 64, 25, 216]
s = list(itertools.accumulate([10] + dd))
assert s == [10, 11, 19, 28, 92, 117, 333]
Q(T, "Pattern: squares and cubes", A, SERIES_Q + "10, 11, 19, 28, 92, 117, ?",
  "333", ["153", "242", "460"],
  "The differences alternate between squares of odd numbers and cubes of even numbers: 1², 2³, 3², 4³, 5², 6³",
  "Differences: 1 = 1², 8 = 2³, 9 = 3², 64 = 4³, 25 = 5². The next is 6³ = 216, so the term is 117 + 216 = 333.",
  ["11 − 10 = 1²", "19 − 11 = 2³", "28 − 19 = 3²", "92 − 28 = 4³", "117 − 92 = 5²", "117 + 6³ = 333"],
  why="153 adds 6² instead of 6³; 242 adds 5³; 460 adds 7³.", secs=90)

s = [p * q for p, q in zip([2, 3, 5, 7, 11, 13], [3, 5, 7, 11, 13, 17])]
assert s == [6, 15, 35, 77, 143, 221]
Q(T, "Missing number series", A, SERIES_Q + "6, 15, 35, 77, 143, ?",
  "221", ["209", "195", "187"],
  "Each term is the product of two consecutive prime numbers",
  "6 = 2 × 3, 15 = 3 × 5, 35 = 5 × 7, 77 = 7 × 11, 143 = 11 × 13, so the next term is 13 × 17 = 221.",
  ["2 × 3, 3 × 5, 5 × 7, 7 × 11, 11 × 13", "Next pair of consecutive primes: 13, 17", "13 × 17 = 221"],
  why="209 = 11 × 19 and 187 = 11 × 17 skip a prime; 195 = 13 × 15 uses 15, which is not prime.", secs=80)

s = [math.factorial(n) + n for n in range(1, 7)]
assert s == [2, 4, 9, 28, 125, 726]
Q(T, "Pattern: multiply-add", A, SERIES_Q + "2, 4, 9, 28, 125, ?",
  "726", ["720", "721", "625"],
  "Each term is n! + n",
  "2 = 1! + 1, 4 = 2! + 2, 9 = 3! + 3, 28 = 4! + 4, 125 = 5! + 5, so the next term is 6! + 6 = 726.",
  ["1! + 1 = 2", "2! + 2 = 4", "3! + 3 = 9", "4! + 4 = 28", "5! + 5 = 125", "6! + 6 = 720 + 6 = 726"],
  short="Equivalently, each term = (previous − n) × (n + 1) + (n + 1): (125 − 5) × 6 + 6 = 726.",
  why="720 forgets the + 6; 721 adds 1 instead of 6; 625 = 5⁴ reads 125 as 5³ and continues with powers of 5.",
  secs=90)

s = [2, 3]
while len(s) < 6:
    s.append(s[-1] * s[-2])
assert s == [2, 3, 6, 18, 108, 1944]
Q(T, "Missing number series", A, MISSING_Q + "2, 3, 6, 18, ?, 1,944",
  "108", ["72", "54", "96"],
  "Each term is the product of the two terms before it",
  "2 × 3 = 6, 3 × 6 = 18, 6 × 18 = 108, and 18 × 108 = 1,944 confirms it.",
  ["2 × 3 = 6", "3 × 6 = 18", "6 × 18 = 108", "Check: 18 × 108 = 1,944"],
  why="72 multiplies 18 by 4; 54 multiplies 18 by 3; 96 does not lead to 1,944 (18 × 96 = 1,728).", secs=80)

# ================================================================ Wrong Number Series (B2 I3 A2)
T = "Wrong Number Series"


def wrong_series(correct, shown):
    diff = [i for i, (a, b) in enumerate(zip(correct, shown)) if a != b]
    assert len(diff) == 1, (correct, shown)
    return shown[diff[0]], correct[diff[0]]


def series_text(seq):
    return ", ".join(N(x) for x in seq)


WRONG_Q = "Find the wrong number in the series:\n"
good = series_from(11, lambda t, k: t + k + 4, 7)
shown = [11, 16, 22, 29, 37, 47, 56]
assert good == [11, 16, 22, 29, 37, 46, 56] and wrong_series(good, shown) == (47, 46)
Q(T, "Find the wrong term", B, WRONG_Q + series_text(shown),
  "47", ["29", "37", "56"],
  "The differences rise by 1: 5, 6, 7, 8, 9, 10",
  "11 + 5 = 16, 16 + 6 = 22, 22 + 7 = 29, 29 + 8 = 37, 37 + 9 = 46, 46 + 10 = 56. The sixth term should be 46, not 47.",
  ["+5, +6, +7, +8 fit", "37 + 9 = 46 ≠ 47", "46 + 10 = 56 fits"],
  why="29, 37 and 56 all fit the rule; 56 looks wrong only if 47 is taken as correct (47 + 9 = 56 repeats the 9).",
  secs=35)

good = [n ** 3 for n in range(1, 8)]
shown = [1, 8, 27, 64, 124, 216, 343]
assert wrong_series(good, shown) == (124, 125)
Q(T, "Find the wrong term", B, WRONG_Q + series_text(shown),
  "124", ["216", "64", "343"],
  "The terms are the cubes 1³, 2³, 3³, …",
  "1, 8, 27, 64, 216 and 343 are 1³, 2³, 3³, 4³, 6³ and 7³. The fifth term should be 5³ = 125, not 124.",
  ["1³ = 1, 2³ = 8, 3³ = 27, 4³ = 64", "5³ = 125 ≠ 124", "6³ = 216, 7³ = 343"],
  why="216, 64 and 343 are exact cubes and fit the pattern.", secs=30)

good = series_from(F(32), lambda t, k: t * F(3, 2), 6)
shown = [32, 48, 72, 106, 162, 243]
assert good == [32, 48, 72, 108, 162, 243] and wrong_series(good, shown) == (106, 108)
Q(T, "Find the wrong term", I, WRONG_Q + series_text(shown),
  "106", ["72", "162", "243"],
  "Each term = previous × 1.5",
  "32 × 1.5 = 48, 48 × 1.5 = 72, 72 × 1.5 = 108, 108 × 1.5 = 162, 162 × 1.5 = 243. The fourth term should be 108.",
  ["32 × 1.5 = 48", "48 × 1.5 = 72", "72 × 1.5 = 108 ≠ 106", "108 × 1.5 = 162", "162 × 1.5 = 243"],
  why="72, 162 and 243 fit once 106 is corrected; 162 only looks wrong if 106 is taken as correct.", secs=45)

good = series_from(1, lambda t, k: 2 * t + 2 * k + 1, 6)
shown = [1, 5, 15, 37, 81, 177]
assert good == [1, 5, 15, 37, 83, 177] and wrong_series(good, shown) == (81, 83)
Q(T, "Find the wrong term", I, WRONG_Q + series_text(shown),
  "81", ["37", "15", "177"],
  "Each term = previous × 2 + an odd number that rises by 2 (3, 5, 7, 9, 11)",
  "1 × 2 + 3 = 5, 5 × 2 + 5 = 15, 15 × 2 + 7 = 37, 37 × 2 + 9 = 83, 83 × 2 + 11 = 177. The fifth term should be 83, "
  "not 81.",
  ["1 × 2 + 3 = 5", "5 × 2 + 5 = 15", "15 × 2 + 7 = 37", "37 × 2 + 9 = 83 ≠ 81", "83 × 2 + 11 = 177"],
  why="37, 15 and 177 all fit; 177 cannot follow 81 (81 × 2 + 11 = 173), which confirms 81 is the error.", secs=55)

good = series_from(5040, lambda t, k: t // (8 - k), 7)
shown = [5040, 840, 120, 24, 6, 2, 1]
assert good == [5040, 720, 120, 24, 6, 2, 1] and wrong_series(good, shown) == (840, 720)
Q(T, "Find the wrong term", I, WRONG_Q + series_text(shown),
  "840", ["120", "24", "2"],
  "The terms are factorials in decreasing order: 7!, 6!, 5!, …, 1! (each = previous ÷ 7, ÷ 6, ÷ 5, …)",
  "5,040 = 7!, then 6! = 720, 5! = 120, 4! = 24, 3! = 6, 2! = 2, 1! = 1. The second term should be 720, not 840.",
  ["5,040 ÷ 7 = 720 ≠ 840", "720 ÷ 6 = 120", "120 ÷ 5 = 24, 24 ÷ 4 = 6, 6 ÷ 3 = 2, 2 ÷ 2 = 1"],
  why="840 = 5,040 ÷ 6 skips the ÷ 7 step; 120, 24 and 2 are 5!, 4! and 2! and fit.", secs=50)

good = [1, 2]
while len(good) < 8:
    good.append(good[-1] + good[-2] + 1)
shown = [1, 2, 4, 7, 12, 21, 33, 54]
assert good == [1, 2, 4, 7, 12, 20, 33, 54] and wrong_series(good, shown) == (21, 20)
Q(T, "Find the wrong term", A, WRONG_Q + series_text(shown),
  "21", ["12", "33", "54"],
  "Each term = sum of the two previous terms + 1",
  "1 + 2 + 1 = 4, 2 + 4 + 1 = 7, 4 + 7 + 1 = 12, 7 + 12 + 1 = 20, 12 + 20 + 1 = 33, 20 + 33 + 1 = 54. The sixth term "
  "should be 20, not 21.",
  ["1 + 2 + 1 = 4", "2 + 4 + 1 = 7", "4 + 7 + 1 = 12", "7 + 12 + 1 = 20 ≠ 21", "12 + 20 + 1 = 33",
   "20 + 33 + 1 = 54"],
  short="The differences 1, 2, 3, 5, 8, 13, 21 are Fibonacci numbers; 21 breaks them (gives 9 and 12).",
  why="33 and 54 fit only with 20 in place of 21 (12 + 21 + 1 = 34, not 33); 12 fits the rule.", secs=80)

good = [n * n * (n - 1) for n in range(2, 9)]
shown = [4, 18, 48, 102, 180, 294, 448]
assert good == [4, 18, 48, 100, 180, 294, 448] and wrong_series(good, shown) == (102, 100)
Q(T, "Find the wrong term", A, WRONG_Q + series_text(shown),
  "102", ["48", "180", "294"],
  "Each term is n²(n − 1) = n³ − n², for n = 2, 3, 4, …",
  "2² × 1 = 4, 3² × 2 = 18, 4² × 3 = 48, 5² × 4 = 100, 6² × 5 = 180, 7² × 6 = 294, 8² × 7 = 448. The fourth term "
  "should be 100, not 102.",
  ["4 = 2² × 1", "18 = 3² × 2", "48 = 4² × 3", "5² × 4 = 100 ≠ 102", "180 = 6² × 5, 294 = 7² × 6, 448 = 8² × 7"],
  short="Second differences of n³ − n² rise by 6: differences 14, 30, 52, 80, 114, 154 ⇒ second differences 16, 22, "
        "28, 34, 40 only with 100.",
  why="48, 180 and 294 are 4² × 3, 6² × 5 and 7² × 6 and fit; 180 only looks off if 102 is taken as correct.",
  secs=90)

# ================================================================ Quadratic Equations (B2 I4 A2)
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


xs, ys = [F(2), F(7)], [F(8), F(11)]
roots_check(1, -9, 14, xs), roots_check(1, -19, 88, ys)
qe("Relation between roots", B, "Solve both equations and choose the relation between x and y that holds for all their roots.",
   "x² − 9x + 14 = 0", "y² − 19y + 88 = 0", xs, ys, "<", [">", ">="],
   "Factorise each quadratic; compare the largest x with the smallest y",
   "x = 2 or 7 and y = 8 or 11. The largest x (7) is less than the smallest y (8), so x < y.",
   ["I: (x − 2)(x − 7) = 0 ⇒ x = 2, 7", "II: (y − 8)(y − 11) = 0 ⇒ y = 8, 11", "max x = 7 < min y = 8", "So x < y"],
   why="x > y and x ≥ y come from reading the roots of II as negative (−8 and −11).",
   secs=40)

xs, ys = [F(5), F(-7)], [F(5), F(7)]
roots_check(1, 2, -35, xs), roots_check(1, -12, 35, ys)
qe("Relation between roots", B, "Find the roots of equations I and II and mark the relation between x and y that is always true.",
   "x² + 2x − 35 = 0", "y² − 12y + 35 = 0", xs, ys, "<=", ["<", ">="],
   "A root common to both equations makes the relation non-strict",
   "x = 5 or −7 and y = 5 or 7. x = 5, y = 5 gives x = y; every other pair has x < y. So x ≤ y.",
   ["I: (x + 7)(x − 5) = 0 ⇒ x = 5, −7", "II: (y − 5)(y − 7) = 0 ⇒ y = 5, 7", "x = y = 5 is possible",
    "All other pairs: x < y ⇒ x ≤ y"],
   why="x < y misses the common root 5; x ≥ y holds only for the pair x = 5, y = 5.", secs=45)

xs, ys = [F(2, 3), F(-3)], [F(5, 2), F(3)]
roots_check(3, 7, -6, xs), roots_check(2, -11, 15, ys)
qe("Relation between roots", I, "Solve the two equations and choose the correct relation between x and y.",
   "3x² + 7x − 6 = 0", "2y² − 11y + 15 = 0", xs, ys, "<", [">", ">="],
   "Split the middle term when the leading coefficient is not 1",
   "x = 2/3 or −3 and y = 2.5 or 3. The largest x (0.67) is below the smallest y (2.5), so x < y.",
   ["I: 3x² + 9x − 2x − 6 = (3x − 2)(x + 3) = 0 ⇒ x = 2/3, −3",
    "II: 2y² − 6y − 5y + 15 = (y − 3)(2y − 5) = 0 ⇒ y = 3, 5/2", "max x = 2/3 < min y = 5/2", "So x < y"],
   why="x > y comes from taking the roots of I as 3 and −2/3 (wrong signs); x ≥ y has no pair to support it.",
   secs=60)

xs = [F(10)]
assert 5 * xs[0] - 3 * (xs[0] - 2) == 3 * xs[0] - 4
ys = [F(10), F(13)]
roots_check(1, -23, 130, ys)
qe("Linear vs quadratic", I, "One equation is linear and the other quadratic. Solve both and choose the correct relation between x and y.",
   "5x − 3(x − 2) = 3x − 4", "y² − 23y + 130 = 0", xs, ys, "<=", ["<", ">"],
   "Solve the linear equation exactly, then compare its single value with both quadratic roots",
   "I: 5x − 3x + 6 = 3x − 4, so 2x + 6 = 3x − 4 and x = 10. II: y = 10 or 13. x = y when y = 10 and x < y when "
   "y = 13, so x ≤ y.",
   ["I: 2x + 6 = 3x − 4 ⇒ x = 10", "II: (y − 10)(y − 13) = 0 ⇒ y = 10, 13", "10 = 10 and 10 < 13", "So x ≤ y"],
   why="x < y misses y = 10; x > y comes from expanding −3(x − 2) as −3x − 6, which gives x = −2.", secs=60)

xs, ys = [F(3, 10), F(8, 10)], [F(4, 10), F(5, 10)]
roots_check(1, F(-11, 10), F(24, 100), xs), roots_check(1, F(-9, 10), F(2, 10), ys)
qe("Relation between roots", I, "The equations below have decimal coefficients. Solve them and choose the relation between x and y, if any.",
   "x² − 1.1x + 0.24 = 0", "y² − 0.9y + 0.2 = 0", xs, ys, "cbe", [">", "<="],
   "Find two numbers with the given sum and product; when the roots interleave, no relation holds",
   "I: two numbers with sum 1.1 and product 0.24 are 0.3 and 0.8. II: sum 0.9 and product 0.2 give 0.4 and 0.5. "
   "x = 0.3 is below both y values but x = 0.8 is above both, so the relationship cannot be established.",
   ["I: (x − 0.3)(x − 0.8) = 0 ⇒ x = 0.3, 0.8", "II: (y − 0.4)(y − 0.5) = 0 ⇒ y = 0.4, 0.5", "0.3 < 0.4 but 0.8 > 0.5",
    "Cannot be established"],
   short="Multiply by 100: 100x² − 110x + 24 = 0 and 10y² − 9y + 2 = 0 factorise as (10x − 3)(10x − 8) and "
         "(2y − 1)(5y − 2).",
   why="x > y uses only x = 0.8; x ≤ y uses only x = 0.3; x < y also ignores x = 0.8.", secs=70)

xs, ys = [F(2, 3), F(-1, 2)], [F(-3, 2), F(-2)]
roots_check(6, -1, -2, xs), roots_check(2, 7, 6, ys)
qe("Relation between roots", I, "Solve both equations and choose the relation between x and y that is always true.",
   "6x² − x − 2 = 0", "2y² + 7y + 6 = 0", xs, ys, ">", ["<", "<="],
   "With all coefficients positive (equation II), both roots are negative; compare the smallest x with the largest y",
   "x = 2/3 or −1/2 and y = −3/2 or −2. The smallest x (−0.5) is greater than the largest y (−1.5), so x > y.",
   ["I: 6x² − 4x + 3x − 2 = (3x − 2)(2x + 1) = 0 ⇒ x = 2/3, −1/2",
    "II: 2y² + 4y + 3y + 6 = (y + 2)(2y + 3) = 0 ⇒ y = −2, −3/2", "min x = −0.5 > max y = −1.5", "So x > y"],
   why="x < y and x ≤ y come from dropping the minus signs on y's roots (1.5 and 2 are larger than 2/3).", secs=65)

xs, ys = [F(2), F(-2), F(3), F(-3)], [F(-3), F(-4)]
for r in xs:
    assert r ** 4 - 13 * r ** 2 + 36 == 0
roots_check(1, 7, 12, ys)
qe("Relation between roots", A, "Equation I is of degree four. Find all real roots of both equations and choose the relation between x and y.",
   "x⁴ − 13x² + 36 = 0", "y² + 7y + 12 = 0", xs, ys, ">=", [">", "<"],
   "Substitute t = x² to turn a biquadratic into a quadratic; each positive t gives two values of x",
   "I: t² − 13t + 36 = 0 gives t = 4 or 9, so x = ±2 or ±3. II: y = −3 or −4. The smallest x (−3) equals the "
   "largest y (−3); every other pair has x > y. So x ≥ y.",
   ["Let t = x²: (t − 4)(t − 9) = 0 ⇒ x² = 4 or 9 ⇒ x = ±2, ±3", "II: (y + 3)(y + 4) = 0 ⇒ y = −3, −4",
    "x = −3, y = −3 gives x = y", "All other pairs x > y ⇒ x ≥ y"],
   why="x > y misses the pair x = −3, y = −3; x < y fails because every x (even −3) is at least as large as every "
       "y.", secs=90)

cand = [F(9), F(2)]
for r in cand:
    assert r * r - 11 * r + 18 == 0
xs = [r for r in cand if r - 5 >= 0 and (r + 7) == (r - 5) ** 2]
assert xs == [9]
ys = [F(9, 2), F(3)]
roots_check(2, -15, 27, ys)
assert relation(cand, ys) == "cbe"
qe("Linear vs quadratic", A, "Solve the equations below (√ denotes the non-negative square root) and choose the correct relation between x and y.",
   "√(x + 7) = x − 5", "2y² − 15y + 27 = 0", xs, ys, ">", ["<", "<="],
   "Squaring can create an extra root: check every root in the original equation",
   "I: squaring gives x + 7 = x² − 10x + 25, so x² − 11x + 18 = 0 and x = 9 or 2. Check: x = 9 gives √16 = 4 = 9 − 5 "
   "(valid); x = 2 gives √9 = 3 but 2 − 5 = −3 (invalid). So x = 9. II: y = 4.5 or 3. Since 9 > 4.5 and 9 > 3, x > y.",
   ["Square: x² − 11x + 18 = 0 ⇒ x = 9 or 2", "x = 2: √9 = 3 ≠ −3 ⇒ rejected", "x = 9 only",
    "II: (2y − 9)(y − 3) = 0 ⇒ y = 4.5, 3", "9 > 4.5 ⇒ x > y"],
   why="'Cannot be established' keeps the extra root x = 2, which lies below y = 3 and 4.5; x < y and x ≤ y are true "
       "only for that rejected root.", secs=100)

# ================================================================ Number System (B1 I1 A2)
T = "Number System"
big = max(n for n in range(1000, 10000) if n % 88 == 0)
assert big == 9944 and 9999 % 88 == 55 and 9999 - 55 == 9944
Q(T, "Divisibility", B, "What is the largest four-digit number that is exactly divisible by 88?",
  "9,944", ["9,999", "9,955", "9,856"],
  "Divide the largest four-digit number by the divisor and subtract the remainder",
  "9,999 ÷ 88 = 113 with remainder 55 (88 × 113 = 9,944). So the largest four-digit multiple of 88 is "
  "9,999 − 55 = 9,944.",
  ["88 × 113 = 9,944", "9,999 − 9,944 = 55 (remainder)", "Answer = 9,999 − 55 = 9,944"],
  why="9,999 is not divisible by 88; 9,955 subtracts 44 instead of the remainder 55; 9,856 = 88 × 112 is a multiple "
      "but not the largest.", secs=40)
assert 9856 == 88 * 112 and 9955 % 88 != 0

nums, dens = [2, 8, 16, 10], [3, 9, 81, 27]
h = F(math.gcd(*nums), math.lcm(*dens))
assert h == F(2, 81)
for f_ in [F(2, 3), F(8, 9), F(16, 81), F(10, 27)]:
    assert (f_ / h).denominator == 1
assert F(math.gcd(*nums), math.gcd(*dens)) == F(2, 3) and F(math.lcm(*nums), math.gcd(*dens)) == F(80, 3)
Q(T, "HCF and LCM", I, "What is the HCF of 2/3, 8/9, 16/81 and 10/27?",
  "2/81", ["2/3", "80/3", "1/81"],
  "HCF of fractions = HCF of the numerators ÷ LCM of the denominators",
  "HCF of 2, 8, 16 and 10 is 2. LCM of 3, 9, 81 and 27 is 81. So the HCF of the fractions is 2/81. (Check: each "
  "fraction divided by 2/81 is a whole number: 27, 36, 8 and 15.)",
  ["HCF(2, 8, 16, 10) = 2", "LCM(3, 9, 81, 27) = 81", "HCF = 2/81"],
  why="2/3 divides by the HCF of the denominators; 80/3 is the LCM-of-fractions formula (LCM of numerators ÷ HCF of "
      "denominators); 1/81 takes the HCF of the numerators as 1.", secs=50)

n_ = 5 * (6 * (7 * 0 + 4) + 3) + 2
assert n_ == 137 and n_ % 5 == 2 and (n_ // 5) % 6 == 3 and (n_ // 5 // 6) % 7 == 4
first = next(m for m in range(1, 1000) if m % 5 == 2 and (m // 5) % 6 == 3 and (m // 5 // 6) % 7 == 4)
assert first == 137
assert 7 * (6 * 2 + 3) + 4 != 0 and 7 * (6 * (5 * 0 + 2) + 3) + 4 == 109
assert 5 * (6 * 2 + 3) + 4 == 79 and 210 - 1 == 209
Q(T, "Remainders", A,
  "A number is divided by 5, the quotient is divided by 6, and that quotient is divided by 7. The remainders are 2, 3 "
  "and 4 respectively. What is the smallest such number?",
  "137", ["109", "79", "209"],
  "Successive division: rebuild the number from the last division backwards, taking the last quotient as 0 for the "
  "smallest number",
  "Let the last quotient be 0. The number divided by 7 was 7 × 0 + 4 = 4. The number divided by 6 was 6 × 4 + 3 = 27. "
  "The original number is 5 × 27 + 2 = 137.",
  ["Third division: 7 × 0 + 4 = 4", "Second: 6 × 4 + 3 = 27", "First: 5 × 27 + 2 = 137",
   "Check: 137 = 5 × 27 + 2, 27 = 6 × 4 + 3, 4 = 7 × 0 + 4"],
  why="109 rebuilds with the divisors in reverse order (7, 6, 5); 79 attaches the remainders to the wrong divisors "
      "(5 × 15 + 4); 209 = 5 × 6 × 7 − 1 treats it as an 'each remainder one less' problem.", secs=90, by=BRUTE)

m6 = [n for n in range(101, 400) if n % 6 == 0]
m15 = [n for n in range(101, 400) if n % 15 == 0]
both = [n for n in range(101, 400) if n % 6 == 0 or n % 15 == 0]
assert (len(m6), len(m15), len(both)) == (50, 20, 60) and len([n for n in m6 if n % 15 == 0]) == 10
Q(T, "Divisibility", A,
  "How many whole numbers between 100 and 400 (excluding both) are divisible by 6 or by 15?",
  "60", ["70", "50", "40"],
  "Inclusion–exclusion: count multiples of 6 and of 15, then subtract the multiples of their LCM, 30, counted twice",
  "Multiples of 6 from 102 to 396: 66 − 16 = 50. Multiples of 15 from 105 to 390: 26 − 6 = 20. Multiples of 30 from "
  "120 to 390: 13 − 3 = 10. So 50 + 20 − 10 = 60.",
  ["Multiples of 6: ⌊399/6⌋ − ⌊100/6⌋ = 66 − 16 = 50", "Multiples of 15: 26 − 6 = 20",
   "Multiples of 30 (both): 13 − 3 = 10", "50 + 20 − 10 = 60"],
  why="70 does not subtract the 10 numbers counted twice; 50 counts only multiples of 6; 40 subtracts the overlap "
      "twice.", secs=90, by=BRUTE)

# ================================================================ Percentage (B2 I2 A2)
T = "Percentage"
pc = F(100, 80) * 100 - 100
assert pc == 25 and F(20, 120) * 100 == F(50, 3)
Q(T, "Basic percentage", B, "Ritu's salary is 20% less than Mohan's. By what percentage is Mohan's salary more than "
  "Ritu's?",
  "25%", ["20%", "16⅔%", "80%"],
  "The base changes: 'more than Ritu's' is measured on Ritu's salary",
  "Take Mohan's salary as 100; Ritu's is 80. Mohan's is 20 more, and 20 is 20 ÷ 80 = 25% of Ritu's salary.",
  ["Mohan = 100, Ritu = 80", "Difference = 20", "20 ÷ 80 × 100 = 25%"],
  short="If A is r% less than B, B is r/(100 − r) × 100% more than A: 20/80 = 25%.",
  why="20% reuses the original base (Mohan's salary); 16⅔% divides by 120 as if Ritu earned 20% more; 80% is Ritu's "
      "salary as a percentage of Mohan's.", secs=35)

n_ = F(168) / (F(40, 100) - F(25, 100))
assert n_ == 1120 and n_ * F(60, 100) == 672 and F(168) / F(40, 100) * F(60, 100) == 252
Q(T, "Basic percentage", B, "40% of a number is 168 more than 25% of the same number. What is 60% of the number?",
  "672", ["1,120", "252", "403.2"],
  "The gap between two percentages of the same number is itself a percentage of it",
  "40% − 25% = 15% of the number = 168, so the number is 168 ÷ 0.15 = 1,120 and 60% of it is 672.",
  ["40% − 25% = 15%", "15% of N = 168 ⇒ N = 1,120", "60% of 1,120 = 672"],
  why="1,120 is the number itself, not 60% of it; 252 treats 168 as 40% of the number; 403.2 takes 60% of 672 again "
      "(60% of 60% of N).", secs=40)
assert F(672) * F(60, 100) == F(4032, 10)

ch = F(125, 100) * F(84, 100) - 1
assert ch == F(5, 100)
Q(T, "Successive change", I,
  "The price of cooking gas rises by 25%, and a family cuts its gas consumption by 16%. By what percentage does its "
  "spending on gas change?",
  "Increases by 5%", ["Increases by 9%", "Decreases by 5%", "Increases by 4%"],
  "Spending = price × quantity, so the two changes multiply: (1 + a)(1 − b) − 1",
  "New spending = 1.25 × 0.84 = 1.05 times the old spending, an increase of 5%.",
  ["Price factor = 1.25", "Quantity factor = 0.84", "1.25 × 0.84 = 1.05 ⇒ +5%"],
  short="a + b + ab/100 = 25 − 16 − (25 × 16)/100 = 9 − 4 = 5%.",
  why="'Increases by 9%' simply subtracts 16 from 25; 'decreases by 5%' gets the sign wrong; 'increases by 4%' uses "
      "the cross term 25 × 16/100 as the answer.", secs=50)

err = (F(5, 3) - F(3, 5)) / F(5, 3) * 100
assert err == 64 and (F(5, 3) - F(3, 5)) / F(3, 5) * 100 == F(1600, 9)
Q(T, "Basic percentage", I,
  "A student was asked to multiply a number by 5/3 but multiplied it by 3/5 instead. What was the percentage error "
  "in the result?",
  "64%", ["177.78%", "40%", "36%"],
  "Percentage error = (correct − wrong) ÷ correct × 100",
  "Take the number as 15. Correct result = 25, wrong result = 9. Error = 16, which is 16 ÷ 25 = 64% of the correct "
  "result.",
  ["Correct = 15 × 5/3 = 25", "Wrong = 15 × 3/5 = 9", "Error = 16", "16 ÷ 25 × 100 = 64%"],
  short="Error = 1 − (3/5)/(5/3) = 1 − 9/25 = 16/25 = 64%.",
  why="177.78% divides the error by the wrong result; 40% is 1 − 3/5; 36% is the wrong result as a percentage of the "
      "correct one (9/25).", secs=50)

p_ = F(12800) / (F(8, 10) ** 2 - F(8, 10) ** 3)
assert p_ == 100000 and F(12800) / F(20, 100) == 64000 and F(12800) / (F(8, 10) * F(2, 10)) == 80000
assert F(12800) / (F(8, 10) ** 3 * F(2, 10)) == 125000
Q(T, "Population and depreciation", A,
  "A machine depreciates by 20% every year on its value at the start of that year. The fall in its value during "
  "the third year is ₹12,800. What was the original value of the machine?",
  "₹1,00,000", ["₹64,000", "₹80,000", "₹1,25,000"],
  "Reducing-balance depreciation: value after n years = P × 0.8ⁿ; the fall in year n is 20% of the value after n − 1 "
  "years",
  "At the start of year 3 the value is P × 0.8² = 0.64P. The year-3 fall is 20% of that = 0.128P = 12,800, so "
  "P = 1,00,000.",
  ["Value after 2 years = 0.64P", "Fall in year 3 = 0.2 × 0.64P = 0.128P", "0.128P = 12,800 ⇒ P = 1,00,000"],
  why="₹64,000 treats ₹12,800 as 20% of the original value (straight-line); ₹80,000 uses the year-2 fall "
      "(0.2 × 0.8P); ₹1,25,000 uses the year-4 fall (0.2 × 0.8³P).", secs=80)

def tax(inc):
    return max(0, min(inc, 700000) - 300000) * F(5, 100) + max(0, inc - 700000) * F(10, 100)


inc = next(x for x in range(300000, 3000000, 10000) if tax(x) == 55000)
assert inc == 1050000 and tax(550000) != 55000 and F(55000) / F(10, 100) + 700000 == 1250000
assert 400000 + F(35000) / F(10, 100) == 750000
Q(T, "Income and expenditure", A,
  "In a town's income-tax scheme, the first ₹3,00,000 of yearly income is tax-free, the next ₹4,00,000 is taxed at "
  "5%, and income above ₹7,00,000 is taxed at 10%. Mr. Rao paid ₹55,000 in tax. What was his yearly income?",
  "₹10,50,000", ["₹5,50,000", "₹12,50,000", "₹7,50,000"],
  "Slab taxation: tax each slab separately, then find how far into the top slab the income goes",
  "The 5% slab gives at most 5% of 4,00,000 = ₹20,000. The remaining ₹35,000 comes from the 10% slab, so income "
  "above ₹7,00,000 is 35,000 ÷ 0.10 = ₹3,50,000. Income = 7,00,000 + 3,50,000 = ₹10,50,000.",
  ["Tax on ₹3–7 lakh = 5% of 4,00,000 = 20,000", "Rest = 55,000 − 20,000 = 35,000 at 10%",
   "Income above 7 lakh = 3,50,000", "Income = 10,50,000"],
  why="₹5,50,000 applies 10% to the whole income; ₹12,50,000 forgets the ₹20,000 from the 5% slab; ₹7,50,000 "
      "leaves out the tax-free ₹3,00,000.", secs=90, by=BRUTE)

# ================================================================ Ratio and Proportion (B1 I3 A2)
T = "Ratio and Proportion"
b_ = F(1)
a_, c_ = F(4, 3) * b_, F(5, 6) * b_
assert 3 * a_ == 4 * b_ and 5 * b_ == 6 * c_ and ratio(a_, c_) == "8 : 5"
Q(T, "Basic ratio", B, "If 3A = 4B and 5B = 6C, what is A : C?",
  "8 : 5", ["5 : 8", "10 : 9", "9 : 10"],
  "Write A and C in terms of B, then compare",
  "From 3A = 4B, A = 4B/3. From 5B = 6C, C = 5B/6. So A : C = 4/3 : 5/6 = 8/6 : 5/6 = 8 : 5.",
  ["A = 4B/3", "C = 5B/6", "A : C = 4/3 : 5/6", "× 6 ⇒ 8 : 5"],
  why="5 : 8 is reversed (or inverts both relations); 10 : 9 inverts 5B = 6C (C = 6B/5); 9 : 10 inverts 3A = 4B "
      "(A = 3B/4).", secs=40)

cr = (F(2, 3) ** 2) * F(6, 7) * (F(3, 2) ** 3)
assert cr == F(9, 7) and (F(2, 3) ** 2) * F(36, 49) * (F(3, 2) ** 3) == F(54, 49)
assert F(2, 3) * F(6, 7) * F(3, 2) == F(6, 7)
Q(T, "Proportion", I,
  "Find the compound ratio of the duplicate ratio of 2 : 3, the sub-duplicate ratio of 36 : 49 and the triplicate "
  "ratio of 3 : 2.",
  "9 : 7", ["7 : 9", "54 : 49", "6 : 7"],
  "Duplicate = squares, sub-duplicate = square roots, triplicate = cubes; a compound ratio multiplies the ratios",
  "Duplicate of 2 : 3 is 4 : 9. Sub-duplicate of 36 : 49 is 6 : 7. Triplicate of 3 : 2 is 27 : 8. Compound ratio = "
  "(4 × 6 × 27) : (9 × 7 × 8) = 648 : 504 = 9 : 7.",
  ["2² : 3² = 4 : 9", "√36 : √49 = 6 : 7", "3³ : 2³ = 27 : 8", "648 : 504 = 9 : 7"],
  why="7 : 9 is reversed; 54 : 49 uses 36 : 49 itself instead of its sub-duplicate; 6 : 7 multiplies the original "
      "ratios without squaring, rooting or cubing.", secs=60)

w = [5 * 4, 6 * 3, 8 * 2]
share = [F(108000 * x, sum(w)) for x in w]
assert w == [20, 18, 16] and share == [40000, 36000, 32000]
Q(T, "Coins and salary share", I,
  "A bonus of ₹1,08,000 is shared among three clerks P, Q and R in proportion to the product of their monthly "
  "salaries and their years of service. Their salaries are in the ratio 5 : 6 : 8 and their years of service in the "
  "ratio 4 : 3 : 2. What is Q's share?",
  "₹36,000", ["₹40,000", "₹32,000", "₹34,105"],
  "Combine the two ratios term by term (multiply), then divide in that ratio",
  "Weights: P = 5 × 4 = 20, Q = 6 × 3 = 18, R = 8 × 2 = 16, total 54. Q's share = 18/54 × 1,08,000 = ₹36,000.",
  ["P : Q : R = 20 : 18 : 16", "Sum = 54", "Q = 1,08,000 × 18/54 = 36,000"],
  why="₹40,000 is P's share; ₹32,000 is R's share; ₹34,105 (about) divides by the salary ratio alone (6/19).",
  secs=55)
assert round(108000 * 6 / 19) == 34105

k_ = F(72 + 24, 12)
assert k_ == 8 and 5 * k_ + 4 == 44 and 5 * k_ == 40
Q(T, "Ages via ratio", I,
  "The present ages of A, B and C are in the ratio 3 : 4 : 5. Eight years ago, the sum of their ages was 72 years. "
  "What will C's age be 4 years from now?",
  "44 years", ["40 years", "34 years", "36 years"],
  "Eight years ago each age was 8 less, so the sum was 24 less",
  "Present sum = 72 + 3 × 8 = 96. With ages 3k, 4k, 5k: 12k = 96, so k = 8 and C is 40 now. In 4 years C will be 44.",
  ["Present sum = 72 + 24 = 96", "12k = 96 ⇒ k = 8", "C now = 5 × 8 = 40", "C in 4 years = 44"],
  why="40 years is C's present age; 34 years uses 72 as the present sum (k = 6, C = 30) and adds 4; 36 years is C's "
      "age 4 years ago.", secs=55)

k_ = next(k for k in range(1, 2000) if F(7 * k - 600, 5 * k + 600) == F(4, 5))
assert k_ == 360 and 12 * k_ == 4320
Q(T, "Basic ratio", A,
  "A sum of money is divided between Asha and Bela in the ratio 7 : 5. If Asha gives ₹600 to Bela, the ratio of their "
  "amounts becomes 4 : 5. What was the total sum?",
  "₹4,320", ["₹7,200", "₹2,400", "₹1,920"],
  "A transfer changes both shares but keeps the total the same",
  "Let the shares be 7k and 5k. After the transfer: (7k − 600) : (5k + 600) = 4 : 5, so 35k − 3,000 = 20k + 2,400, "
  "15k = 5,400 and k = 360. Total = 12k = ₹4,320.",
  ["(7k − 600)/(5k + 600) = 4/5", "35k − 3,000 = 20k + 2,400", "k = 360", "Total = 12 × 360 = 4,320"],
  short="The total 12k stays fixed; after the transfer Asha has 4/9 of it, down from 7/12: (7/12 − 4/9) × 12k = 600 "
        "⇒ 5k/3 = 600 ⇒ k = 360.",
  why="₹7,200 solves for equal shares after the transfer (7k − 600 = 5k + 600); ₹2,400 forgets to add 600 to "
      "Bela's share (k = 200); ₹1,920 forgets to take 600 from Asha's share (k = 160).", secs=90)
assert 12 * 600 == 7200

k_ = F(12 * 6, 4 ** 2)
x_ = k_ * 6 ** 2 / 9
assert k_ == F(9, 2) and x_ == 18 and F(12 * 6, 4) * 6 / 9 == 12 and F(12, 16 * 6) * 36 * 9 == F(81, 2)
Q(T, "Proportion", A,
  "x varies directly as the square of y and inversely as z. When y = 4 and z = 6, x = 12. What is x when y = 6 and "
  "z = 9?",
  "18", ["12", "40.5", "27"],
  "Joint variation: x = k × y²/z; find k from the given values",
  "12 = k × 16/6, so k = 4.5. Then x = 4.5 × 36/9 = 18.",
  ["x = ky²/z", "12 = k × 16/6 ⇒ k = 9/2", "x = 9/2 × 36/9 = 18"],
  short="x changes by (6/4)² ÷ (9/6) = 2.25 ÷ 1.5 = 1.5 times: 12 × 1.5 = 18.",
  why="12 uses y instead of y² (x = ky/z); 40.5 multiplies by z instead of dividing (x = ky²z); 27 ignores z "
      "altogether (12 × 2.25).", secs=70)
assert 12 * F(9, 4) == 27

# ================================================================ Problems on Ages (B1 I1 A1)
T = "Problems on Ages"
pairs_ = [(a, a + 6) for a in range(1, 60) if a * (a + 6) == 280]
assert pairs_ == [(14, 20)]
Q(T, "Present and future ages", B,
  "The difference between the ages of two sisters is 6 years and the product of their ages is 280. What is the "
  "elder sister's age?",
  "20 years", ["14 years", "28 years", "17 years"],
  "Form a quadratic in the younger age, or test factor pairs of 280 that differ by 6",
  "If the younger is a years old, a(a + 6) = 280, so a² + 6a − 280 = 0 = (a − 14)(a + 20). Ages are positive, so "
  "a = 14 and the elder is 20.",
  ["a(a + 6) = 280", "(a − 14)(a + 20) = 0", "a = 14 (age is positive)", "Elder = 20"],
  short="Factor pairs of 280: 14 × 20 differ by 6.",
  why="14 years is the younger sister; 28 years pairs with 10 (difference 18); 17 years is the average of 14 and 20.",
  secs=40)

for b_age in range(1, 60):
    c_age = 50 - b_age
    a_age = F(b_age + c_age, 2)
    assert b_age - a_age == a_age - c_age
Q(T, "Present and future ages", I,
  "A is as much younger than B as he is older than C. If the sum of the ages of B and C is 50 years, how old is A?",
  "25 years", ["50 years", "20 years", "30 years"],
  "'As much younger than B as older than C' means A is midway between B and C",
  "B − A = A − C, so 2A = B + C = 50 and A = 25 years.",
  ["B − A = A − C", "2A = B + C", "A = 50 ÷ 2 = 25"],
  why="50 years is B + C, not A; 20 and 30 years assume particular ages for B and C instead of using the condition.",
  secs=40)

sols = [(s, s + 4, s + 32) for s in range(1, 80) if (s + 32 + 4) == F(3, 2) * ((s + 4) + (s + 4 + 4))]
assert sols == [(9, 13, 41)]
s_, d_, f_ = sols[0]
assert f_ - s_ == 8 * 4
Q(T, "Present and future ages", A,
  "A daughter is 4 years older than her brother. When the brother was born, their father was 8 times as old as the "
  "daughter was then. Four years from now, the father's age will be 1.5 times the sum of his two children's ages "
  "then. What is the father's present age?",
  "41 years", ["45 years", "32 years", "36 years"],
  "Express everything through the son's present age s; at the son's birth the daughter was 4",
  "At the son's birth the daughter was 4, so the father was 32 then. If the son is s now, the father is s + 32 and "
  "the daughter s + 4. In 4 years: s + 36 = 1.5 × (s + 4 + s + 8) = 3s + 18, so s = 9 and the father is 41.",
  ["Daughter at son's birth = 4 ⇒ father then = 32", "Now: son s, daughter s + 4, father s + 32",
   "In 4 years: s + 36 = 1.5(2s + 12)", "s + 36 = 3s + 18 ⇒ s = 9", "Father = 41"],
  why="45 years is the father's age 4 years from now; 32 years is his age when the son was born; 36 years adds only "
      "4 to that.", secs=100)

# ================================================================ Average (B2 I1 A1)
T = "Average"
x_ = F(42 * 3, 1 + 2 + 3)
assert x_ == 21 and 3 * x_ == 63
Q(T, "Simple average", B,
  "The average of three numbers is 42. The first number is twice the second, and the third is three times the "
  "second. What is the largest of the three numbers?",
  "63", ["42", "21", "84"],
  "Write all three numbers in terms of one of them; sum = average × count",
  "Let the second number be x. The numbers are 2x, x and 3x, and their sum is 6x = 3 × 42 = 126. So x = 21 and the "
  "largest is 3x = 63.",
  ["Sum = 3 × 42 = 126", "2x + x + 3x = 6x = 126", "x = 21", "Largest = 3x = 63"],
  why="42 is the first number (2x) and also the average; 21 is the second number; 84 takes the sum as 168.",
  secs=40)

avg = F(25 * 2 + 6 * 2 + 4, 3)
assert avg == 22 and F(50 + 4, 3) == 18
Q(T, "Simple average", B,
  "At the time of their marriage, the average age of a husband and wife was 25 years. Six years later they have a "
  "4-year-old child. What is the average age of the family of three now?",
  "22 years", ["31 years", "18 years", "20 years"],
  "Each of the couple has aged 6 years; add the child's age and divide by 3",
  "At marriage their ages added up to 50. Six years later they add up to 62. With the child, the total is 66, and "
  "66 ÷ 3 = 22 years.",
  ["Couple at marriage: 2 × 25 = 50", "Six years later: 50 + 12 = 62", "With child: 62 + 4 = 66", "66 ÷ 3 = 22"],
  why="31 years is the couple's average now (without the child); 18 years forgets the 6 years that have passed; "
      "20 years adds only 6 (not 12) for the couple.", secs=45)
assert F(62, 2) == 31 and F(56 + 4, 3) == 20

a_ = next(a for a in range(100, 2000) if 15 * a - 3 * 480 + 5 * 540 == 17 * (a + 10))
assert a_ == 545
Q(T, "Replacement", I,
  "A team of 15 workers had a certain average daily wage. Three workers whose average wage was ₹480 left, and five "
  "new workers whose average wage was ₹540 joined. The average wage of the team rose by ₹10. What was the original "
  "average daily wage?",
  "₹545", ["₹555", "₹510", "₹212"],
  "New total = old total − wages of those who left + wages of those who joined; the team size also changes",
  "Let the original average be a. New total = 15a − 1,440 + 2,700 = 15a + 1,260, shared by 17 workers at a + 10: "
  "15a + 1,260 = 17a + 170, so 2a = 1,090 and a = ₹545.",
  ["Leaving: 3 × 480 = 1,440", "Joining: 5 × 540 = 2,700", "15a + 1,260 = 17(a + 10)", "2a = 1,090 ⇒ a = 545"],
  why="₹555 is the new average; ₹510 averages 480 and 540; ₹212 divides by 20 workers, forgetting that 3 left "
      "(15a + 1,260 = 20(a + 10)).", secs=70)

sol = [(b, g) for g in range(1, 200) for b in [g + 12] if 58 * b + 67 * g == 62 * (b + g)]
assert sol == [(60, 48)] and sum(sol[0]) == 108
Q(T, "Weighted average", A,
  "In a class, the average mark of the boys is 58 and that of the girls is 67, and the average of the whole class is "
  "62. There are 12 more boys than girls. How many students are there in the class?",
  "108", ["60", "48", "54"],
  "Weighted average (alligation): the numbers of boys and girls are in the inverse ratio of their distances from "
  "the class average",
  "Boys are 4 below the class average and girls 5 above, so boys : girls = 5 : 4. The difference of 1 part = 12, so "
  "there are 60 boys and 48 girls: 108 students.",
  ["Boys: 62 − 58 = 4; girls: 67 − 62 = 5", "Boys : girls = 5 : 4", "1 part = 12 ⇒ 60 boys, 48 girls",
   "Total = 108"],
  why="60 is the number of boys only; 48 is the number of girls only; 54 treats the difference of 12 as two parts "
      "(9 parts × 6).", secs=80)

# ================================================================ Profit and Loss (B1 I2 A2)
T = "Profit and Loss"
cost, rev = 160 * 5, (160 - 10) * F(64, 10)
pc = (rev - cost) / cost * 100
assert (cost, rev, pc) == (800, 960, 20) and (F(64, 10) - 5) / 5 * 100 == 28 and F(160, 960) * 100 == F(50, 3)
Q(T, "Cost and selling price", B,
  "A shopkeeper bought 160 eggs at ₹5 each. 10 of them broke, and he sold the rest at ₹6.40 each. What was his profit "
  "percentage?",
  "20%", ["28%", "16⅔%", "6.25%"],
  "Profit % is on the total cost, including the cost of the broken eggs",
  "Cost = 160 × 5 = ₹800. Revenue = 150 × 6.40 = ₹960. Profit = ₹160, which is 160 ÷ 800 = 20% of the cost.",
  ["Cost = 160 × 5 = 800", "Sold = 160 − 10 = 150", "Revenue = 150 × 6.40 = 960", "Profit % = 160/800 × 100 = 20%"],
  why="28% ignores the broken eggs (profit of ₹1.40 on each ₹5); 16⅔% divides the profit by the selling price; "
      "6.25% divides the ₹50 lost on broken eggs by ₹800.", secs=45)
assert F(50, 800) * 100 == F(25, 4)

pc = (F(110, 100) / F(80, 100) - 1) * 100
assert pc == F(75, 2)
Q(T, "Dishonest dealer", I,
  "A grocer mixes 20% worthless husk (by weight) into his lentils and sells the mixture at 10% above the cost price "
  "of pure lentils. What is his actual profit percentage?",
  "37.5%", ["30%", "32%", "12.5%"],
  "In 1 kg of mixture only 0.8 kg is lentils, so the cost of 1 kg sold is the cost of 0.8 kg",
  "Let pure lentils cost ₹100 per kg. One kg of mixture contains 0.8 kg of lentils costing ₹80, and sells for ₹110. "
  "Profit = 30 on 80 = 37.5%.",
  ["Cost of 1 kg mixture = 0.8 × 100 = 80", "Selling price = 110", "Profit = 30", "30 ÷ 80 × 100 = 37.5%"],
  short="(1 + 10%) ÷ (1 − 20%) = 1.1/0.8 = 1.375.",
  why="30% adds 10 and 20; 32% multiplies 1.1 × 1.2 (treats husk as 20% extra on cost); 12.5% divides the 10% gain "
      "by 0.8 without adding the saved cost.", secs=60)
assert (F(11, 10) * F(12, 10) - 1) * 100 == 32

a_sell, a_buy = F(40) * F(110, 100), F(40) * F(110, 100) * F(90, 100)
assert (a_sell, a_buy, a_sell - a_buy, a_sell - 40) == (44, F(396, 10), F(44, 10), 4)
Q(T, "Successive transactions", I,
  "Arun buys a flat for ₹40 lakh and sells it to Bina at a profit of 10%. Later Bina sells it back to Arun at a loss "
  "of 10% on her cost. Counting the money Arun received and paid in both deals (he owns the flat again at the end), "
  "what is his net gain?",
  "₹4.4 lakh", ["₹4 lakh", "Nil", "₹0.4 lakh"],
  "Track Arun's cash: he receives Bina's price and later pays her resale price; he ends with the flat again",
  "Arun sells for 44 lakh (10% profit). Bina sells back at 10% below 44 lakh = 39.6 lakh. Arun received 44 and paid "
  "39.6, and has the flat again, so he is ₹4.4 lakh better off.",
  ["Sale to Bina: 40 × 1.1 = 44 lakh", "Buy-back: 44 × 0.9 = 39.6 lakh", "Net cash gain = 44 − 39.6 = 4.4 lakh"],
  why="₹4 lakh counts only the first sale; 'Nil' assumes a 10% gain and a 10% loss cancel; ₹0.4 lakh is Bina's net "
      "loss compared with her gain.", secs=60)

x_ = (8 - F(2, 5) * 15 + F(1, 3) * 10) / (1 - F(2, 5) - F(1, 3))
assert x_ == 20 and 1 - F(2, 5) - F(1, 3) == F(4, 15)
Q(T, "Cost and selling price", A,
  "A trader sells 2/5 of his stock at a profit of 15% and 1/3 of it at a loss of 10%. At what profit percentage must "
  "he sell the rest to make an overall profit of 8%?",
  "20%", ["19%", "26⅔%", "7.5%"],
  "Overall profit % is the weighted average of the parts' profit %, weighted by their share of the cost",
  "The rest is 1 − 2/5 − 1/3 = 4/15 of the stock. Weighted: (2/5)(15) + (1/3)(−10) + (4/15)x = 8, so "
  "6 − 10/3 + 4x/15 = 8, 4x/15 = 16/3 and x = 20%.",
  ["Remaining share = 4/15", "2/5 × 15 = 6", "1/3 × (−10) = −10/3", "6 − 10/3 + (4/15)x = 8 ⇒ x = 20"],
  why="19% gives the three parts equal weight ((15 − 10 + x)/3 = 8); 26⅔% takes the remaining share as 1/5; 7.5% "
      "leaves out the part sold at a loss.", secs=90)
assert (15 - 10 + 19) == 24 and 6 - F(10, 3) + F(80, 3) / 5 == 8 and 6 + F(4, 15) * F(15, 2) == 8

c_ = F(28) / (F(115, 100) - F(9, 10) * F(125, 100))
assert c_ == 1120 and F(28) / (F(125, 100) - F(115, 100)) == 280
Q(T, "Cost and selling price", A,
  "A shopkeeper sells an article at a profit of 15%. Had he bought it 10% cheaper and sold it for ₹28 less, he would "
  "have made a profit of 25%. What is the cost price of the article?",
  "₹1,120", ["₹280", "₹1,400", "₹1,288"],
  "Write both selling prices in terms of the cost price C and set up one equation",
  "Actual selling price = 1.15C. New cost = 0.9C and the new selling price = 1.25 × 0.9C = 1.125C. The new selling "
  "price is ₹28 less: 1.15C − 1.125C = 28, so 0.025C = 28 and C = ₹1,120.",
  ["SP = 1.15C", "New SP = 1.25 × 0.9C = 1.125C", "1.15C − 1.125C = 28", "C = 28 ÷ 0.025 = 1,120"],
  why="₹280 forgets that the cost also falls 10% (uses 1.25C − 1.15C = 28); ₹1,400 rounds 1.25 × 0.9 to 1.13 "
      "(28 ÷ 0.02); ₹1,288 is the actual selling price (1.15 × 1,120), not the cost.", secs=90)
assert F(28) / F(2, 100) == 1400 and F(115, 100) * 1120 == 1288

# ================================================================ Discount (B2 I2 A1)
T = "Discount"
mp = F(270) / F(15, 100)
assert mp == 1800 and mp - 270 == 1530
Q(T, "Single discount", B,
  "A discount of 15% on a watch saves the buyer ₹270. What does the buyer pay for the watch?",
  "₹1,530", ["₹1,800", "₹2,070", "₹1,755"],
  "The saving is 15% of the marked price",
  "15% of the marked price = 270, so the marked price = 270 ÷ 0.15 = ₹1,800. The buyer pays 1,800 − 270 = ₹1,530.",
  ["Marked price = 270 ÷ 0.15 = 1,800", "Price paid = 1,800 − 270 = 1,530"],
  why="₹1,800 is the marked price; ₹2,070 adds the saving; ₹1,755 = 1,800 − 45 subtracts 15% of 270 instead.",
  secs=35)

saved = 4000 * (1 - F(90, 100) * F(95, 100))
assert saved == 580 and 4000 * F(15, 100) == 600
Q(T, "Successive discounts", B,
  "On a microwave marked ₹4,000, a shop gives a 10% festive discount and then a further 5% discount on the reduced "
  "price for cash payment. How much does a cash buyer save in all?",
  "₹580", ["₹600", "₹3,420", "₹400"],
  "Successive discounts multiply: price paid = MP × 0.90 × 0.95",
  "After 10%: 4,000 × 0.9 = 3,600. After a further 5%: 3,600 × 0.95 = 3,420. Saving = 4,000 − 3,420 = ₹580.",
  ["4,000 × 0.90 = 3,600", "3,600 × 0.95 = 3,420", "Saving = 580"],
  short="Equivalent discount = 10 + 5 − (10 × 5)/100 = 14.5%; 14.5% of 4,000 = 580.",
  why="₹600 adds the two discounts as 15%; ₹3,420 is the price paid, not the saving; ₹400 counts only the first "
      "discount.", secs=40)

d_ = 1 - F(120, 100) / F(160, 100)
assert d_ == F(1, 4) and 1 - F(100, 160) == F(3, 8)
Q(T, "Discount with profit", I,
  "A shopkeeper marks his goods 60% above cost price. What is the largest discount he can allow and still make a "
  "profit of 20%?",
  "25%", ["40%", "37.5%", "33⅓%"],
  "Discount % is measured on the marked price, profit % on the cost price",
  "Let the cost be 100. Marked price = 160; the selling price must be 120. Discount = 40 on 160 = 25%.",
  ["CP = 100, MP = 160", "Required SP = 120", "Discount = 40", "40 ÷ 160 × 100 = 25%"],
  why="40% subtracts 20 from 60; 37.5% is the discount that gives no profit (selling at cost); 33⅓% divides 40 by 120.",
  secs=50)

mp = F(63) / (F(35, 100) - (1 - F(80, 100) * F(85, 100)))
assert mp == 2100 and 1 - F(80, 100) * F(85, 100) == F(32, 100)
Q(T, "Successive discounts", I,
  "On a marked price, the difference between a single discount of 35% and two successive discounts of 20% and 15% is "
  "₹63. What is the marked price?",
  "₹2,100", ["₹1,260", "₹6,300", "₹180"],
  "Convert the successive discounts to a single equivalent discount, then compare",
  "Successive 20% and 15% = 1 − 0.8 × 0.85 = 32%. The gap with 35% is 3% of the marked price = ₹63, so the marked "
  "price = 63 ÷ 0.03 = ₹2,100.",
  ["0.80 × 0.85 = 0.68 ⇒ 32%", "35% − 32% = 3%", "3% of MP = 63 ⇒ MP = 2,100"],
  why="₹1,260 takes the successive discounts as 20 + 15 − 5 = 30% (a 5% gap); ₹6,300 takes the gap as 1%; ₹180 is "
      "63 ÷ 0.35.",
  secs=60)
assert F(63) / F(5, 100) == 1260 and F(63) / F(1, 100) == 6300 and F(63) / F(35, 100) == 180

cost, sp = F(80, 100), F(120, 100) * F(90, 100)
pc = (sp - cost) / cost * 100
assert sp == F(108, 100) and pc == 35 and (F(108, 100) - 1) * 100 == 8
Q(T, "Discount with profit", A,
  "A retailer buys goods at 20% below their list price. He marks them 20% above the list price and then sells them "
  "at a 10% discount on his marked price. What is his profit percentage?",
  "35%", ["8%", "30%", "28%"],
  "Express cost and selling price as fractions of the list price; profit % is on cost",
  "Let the list price be 100. Cost = 80. Marked price = 120, and after a 10% discount the selling price is 108. "
  "Profit = 28 on 80 = 35%.",
  ["List = 100 ⇒ cost = 80", "Marked = 120", "SP = 120 × 0.9 = 108", "Profit % = 28/80 × 100 = 35%"],
  why="8% measures the profit against the list price instead of the retailer's cost (108 − 100); 30% adds 20 + 20 − "
      "10; 28% is the profit in rupees per ₹100 of list price.", secs=75)

# ================================================================ Simple Interest (B1 I2 A1)
T = "Simple Interest"
r_ = F(9300 - 7500, 7500 * 3) * 100
new = 7500 + 7500 * (r_ + 2) * 3 / 100
assert r_ == 8 and new == 9750 and 9300 + 7500 * F(2, 100) == 9450
Q(T, "Basic SI", B,
  "A sum of ₹7,500 lent at simple interest amounts to ₹9,300 in 3 years. What would it amount to in 3 years if the "
  "rate were 2% higher?",
  "₹9,750", ["₹9,450", "₹9,486", "₹2,250"],
  "Find the rate from the first deal; a 2% higher rate adds 2% × 3 years of interest",
  "Interest = 9,300 − 7,500 = 1,800, so the rate = 1,800 ÷ (7,500 × 3) = 8%. At 10% the interest is 7,500 × 10% × 3 "
  "= 2,250, and the amount is ₹9,750.",
  ["SI = 1,800 ⇒ R = 8%", "New rate = 10%", "SI = 7,500 × 0.10 × 3 = 2,250", "Amount = 9,750"],
  short="Extra interest = 7,500 × 2% × 3 = 450; 9,300 + 450 = 9,750.",
  why="₹9,450 adds the extra 2% for one year only; ₹9,486 raises ₹9,300 by 2%; ₹2,250 is the interest, not the "
      "amount.", secs=45)
assert 9300 * F(102, 100) == 9486

p_ = F(960) / (F(3, 100) * 4)
assert p_ == 8000
Q(T, "SI with changing rates", I,
  "If the rate of simple interest on a sum were 3% higher, the sum would earn ₹960 more in 4 years. What is the sum?",
  "₹8,000", ["₹32,000", "₹4,000", "₹24,000"],
  "The extra interest comes only from the extra rate: P × 3% × 4",
  "Extra interest = P × 3 × 4 ÷ 100 = 0.12P = 960, so P = ₹8,000.",
  ["Extra = P × 3% × 4 = 0.12P", "0.12P = 960", "P = 8,000"],
  why="₹32,000 divides 960 by 3% only (forgets the 4 years); ₹4,000 doubles the rate change to 6%; ₹24,000 divides "
      "by the 4 years only (forgets the 3%).", secs=50)
assert F(960) / F(3, 100) == 32000 and F(960) / F(24, 100) == 4000 and F(96000, 4) == 24000

days = (F(28 - 4) + 31 + 18)
si = 14600 * F(75, 1000) * days / 365
assert days == 73 and si == 219 and 14600 * F(75, 1000) * 74 / 365 == 222 and 14600 * F(75, 1000) * 72 / 365 == 216
assert 14600 * F(75, 1000) / 4 == F(27375, 100)
Q(T, "Basic SI", I,
  "₹14,600 is deposited at 7.5% per annum simple interest on 4 February 2026 and withdrawn on 18 April 2026. Interest "
  "is counted for each day from the day after the deposit up to and including the day of withdrawal, on a 365-day "
  "year. How much interest is earned?",
  "₹219", ["₹222", "₹216", "₹273.75"],
  "Count the days carefully, then SI = P × R × (days/365)",
  "Days: 24 in February (5th to 28th; 2026 is not a leap year), 31 in March and 18 in April = 73 days = 73/365 = 1/5 "
  "year. SI = 14,600 × 7.5% × 1/5 = ₹219.",
  ["February: 28 − 4 = 24 days", "March: 31 days", "April: 18 days", "Total = 73 days = 1/5 year",
   "SI = 14,600 × 0.075 ÷ 5 = 219"],
  why="₹222 counts 74 days (both the deposit day and the withdrawal day); ₹216 counts 72 days; ₹273.75 treats the "
      "period as a quarter of a year.", secs=75)

r_ = next(r for r in range(1, 50) if F(r * r, 100) == F(81, 100))
assert r_ == 9 and 12000 * F(11, 100) * 9 == 11880 and 12000 * F(11, 100) * 11 == 14520
Q(T, "Basic SI", A,
  "The simple interest on a sum is 81% of the sum, and the number of years equals the rate per cent per annum. What "
  "would be the simple interest on ₹12,000 for the same number of years at a rate 2% higher?",
  "₹11,880", ["₹9,720", "₹14,520", "₹10,560"],
  "SI/P = R × T/100; with T = R this gives R² = 81",
  "R × R/100 = 0.81, so R² = 81 and R = 9% for 9 years. At 11% for 9 years: 12,000 × 11% × 9 = ₹11,880.",
  ["R × T = 81 with T = R ⇒ R = 9, T = 9", "New rate = 11%", "SI = 12,000 × 0.11 × 9 = 11,880"],
  why="₹9,720 keeps the old rate (12,000 × 81%); ₹14,520 also changes the time to 11 years; ₹10,560 uses 11% for 8 "
      "years.", secs=80)
assert 12000 * F(81, 100) == 9720 and 12000 * F(11, 100) * 8 == 10560

# ================================================================ Compound Interest (B2 I2 A1)
T = "Compound Interest"
y2 = 10000 * F(110, 100) ** 2 - 10000 * F(110, 100)
assert y2 == 1100 and 10000 * (F(11, 10) ** 2 - 1) == 2100
Q(T, "Annual compounding", B,
  "₹10,000 is invested at 10% per annum compound interest, compounded annually. How much interest is earned in the "
  "second year alone?",
  "₹1,100", ["₹1,000", "₹2,100", "₹1,210"],
  "Interest for a year is charged on the amount at the start of that year",
  "After year 1 the amount is ₹11,000. The interest for year 2 is 10% of 11,000 = ₹1,100.",
  ["Amount after year 1 = 11,000", "Year-2 interest = 10% of 11,000 = 1,100"],
  why="₹1,000 is the simple-interest figure (10% of the original sum); ₹2,100 is the total interest for two years; "
      "₹1,210 is the third year's interest.", secs=35)

p_ = F(4840) / F(121, 100)
assert p_ == 4000 and p_ * F(20, 100) == 800 and F(4840) * F(20, 100) == 968
Q(T, "Annual compounding", B,
  "A sum amounts to ₹4,840 in 2 years at 10% per annum compound interest, compounded annually. What would be the "
  "simple interest on the same sum for 2 years at the same rate?",
  "₹800", ["₹840", "₹968", "₹4,000"],
  "First recover the sum: P = amount ÷ (1.1)²",
  "P = 4,840 ÷ 1.21 = ₹4,000. Simple interest for 2 years at 10% = 4,000 × 20% = ₹800.",
  ["1.1² = 1.21", "P = 4,840 ÷ 1.21 = 4,000", "SI = 4,000 × 0.10 × 2 = 800"],
  why="₹840 is the compound interest; ₹968 takes 20% of the amount instead of the sum; ₹4,000 is the sum itself.",
  secs=45)

r_ = ((1 + F(10, 100)) ** 2 - 1) * 100 / 2
assert r_ == F(21, 2)
Q(T, "CI vs SI difference", I,
  "At what rate of simple interest per annum will a sum earn the same interest in 2 years as it earns at 10% per "
  "annum compound interest, compounded annually, in 2 years?",
  "10.5%", ["10%", "21%", "11%"],
  "Equal interest over the same 2 years: 2 × R% = total CI% for 2 years",
  "At 10% compound interest, 2 years' interest is 1.1² − 1 = 0.21 = 21% of the sum. Simple interest of 21% in 2 years "
  "needs 21 ÷ 2 = 10.5% per annum.",
  ["CI for 2 years = 21% of P", "SI for 2 years = 2R% of P", "2R = 21 ⇒ R = 10.5%"],
  why="10% ignores the interest on interest; 21% is the total for 2 years, not per annum; 11% uses the second year's "
      "interest rate on the original sum.", secs=50)

x_ = F(26000 - 5000) / (1 / F(11, 10) + 1 / F(11, 10) ** 2)
assert x_ == 12100 and F(21000, 2) == 10500 and F(26000, 2) * F(11, 10) != x_
Q(T, "Instalments", I,
  "A scooter costs ₹26,000 in cash. It can also be bought for ₹5,000 down and two equal instalments paid at the ends "
  "of the first and second years, with interest at 10% per annum compounded annually. What is each instalment?",
  "₹12,100", ["₹10,500", "₹11,550", "₹12,705"],
  "The present values of the instalments must equal the amount financed",
  "Amount financed = 26,000 − 5,000 = 21,000. If each instalment is x, then x/1.1 + x/1.21 = 21,000, so "
  "x × 2.1/1.21 = 21,000 and x = 21,000 × 1.21 ÷ 2.1 = ₹12,100.",
  ["Financed = 21,000", "x/1.1 + x/1.21 = 21,000", "x(1.1 + 1)/1.21 = 21,000", "x = 12,100"],
  why="₹10,500 ignores interest (21,000 ÷ 2); ₹11,550 discounts both instalments by one year only "
      "(x/1.1 + x/1.1 = 21,000); ₹12,705 compounds 21,000 for two years and halves it.", secs=80)
assert 21000 * F(11, 10) / 2 == 11550 and 21000 * F(121, 100) / 2 == 12705

b_ = F(8840) / (1 + F(121, 100))
a_ = 8840 - b_
assert b_ == 4000 and a_ == 4840 and a_ * F(11, 10) ** 3 == b_ * F(11, 10) ** 5
Q(T, "Annual compounding", A,
  "₹8,840 is divided between A and B so that A's share, invested for 3 years, amounts to the same as B's share "
  "invested for 5 years, both at 10% per annum compound interest, compounded annually. What is A's share?",
  "₹4,840", ["₹4,000", "₹4,420", "₹840"],
  "Equal amounts: A × 1.1³ = B × 1.1⁵, so A = 1.21B",
  "A × 1.1³ = B × 1.1⁵ gives A = B × 1.1² = 1.21B. Then 2.21B = 8,840, so B = ₹4,000 and A = ₹4,840.",
  ["A(1.1)³ = B(1.1)⁵", "A : B = 1.21 : 1 = 121 : 100", "B = 8,840 × 100/221 = 4,000", "A = 4,840"],
  why="₹4,000 is B's share (also what A gets if the ratio is inverted); ₹4,420 splits the sum equally; ₹840 is the "
      "difference between the two shares.", secs=90)
assert a_ - b_ == 840

# ================================================================ Partnership (B1 I2 A3)
T = "Partnership"
a_ = F(32000) * F(3, 8)
assert a_ == 12000
Q(T, "Simple partnership", B,
  "In a business, A's capital is 3/5 of B's capital, and both invest for the same period. Out of a profit of ₹32,000, "
  "what is A's share?",
  "₹12,000", ["₹19,200", "₹20,000", "₹16,000"],
  "Same period: profit is shared in the ratio of capitals; A : B = 3 : 5",
  "A : B = 3/5 : 1 = 3 : 5. A's share = 3/8 × 32,000 = ₹12,000.",
  ["A : B = 3 : 5", "A's share = 32,000 × 3/8 = 12,000"],
  why="₹19,200 takes 3/5 of the whole profit; ₹20,000 is B's share; ₹16,000 splits equally.", secs=35)
assert 32000 * F(3, 5) == 19200

w = [10 * 7, 12 * 5, 15 * 3]
c_share = F(1750 * w[2], sum(w))
assert w == [70, 60, 45] and c_share == 450
Q(T, "Compound partnership", I,
  "A, B and C rent a pasture for ₹1,750. A grazes 10 oxen for 7 months, B 12 oxen for 5 months and C 15 oxen for 3 "
  "months. How much rent should C pay?",
  "₹450", ["₹700", "₹600", "₹350"],
  "Share in the ratio of 'ox-months' (number × time)",
  "Ox-months: A 70, B 60, C 45, total 175. C pays 45/175 × 1,750 = ₹450.",
  ["A: 10 × 7 = 70", "B: 12 × 5 = 60", "C: 15 × 3 = 45", "C = 1,750 × 45/175 = 450"],
  why="₹700 is A's share; ₹600 is B's share; ₹350 shares by months only (3/15 × 1,750).",
  secs=50)

p_ = F(22800) / (F(20, 100) + F(80, 100) * F(3, 12))
a_ = p_ * F(80, 100) * F(5, 12)
assert p_ == 57000 and a_ == 19000
Q(T, "Working partner", I,
  "A, B and C start a business with capitals in the ratio 5 : 4 : 3. C manages the business and receives 20% of the "
  "profit for this; the rest is shared in the ratio of capitals. If C receives ₹22,800 in all, what is A's share?",
  "₹19,000", ["₹23,750", "₹15,200", "₹9,500"],
  "C's total = 20% of profit + 3/12 of the remaining 80%",
  "C gets 0.2P + 0.8P × 3/12 = 0.2P + 0.2P = 0.4P = 22,800, so P = ₹57,000. A gets 0.8 × 57,000 × 5/12 = ₹19,000.",
  ["C = 0.2P + 0.8P × 1/4 = 0.4P", "P = 22,800 ÷ 0.4 = 57,000", "Distributable = 45,600", "A = 45,600 × 5/12 = 19,000"],
  why="₹23,750 gives A 5/12 of the whole profit; ₹15,200 is B's share; ₹9,500 treats 22,800 as C's capital share "
      "alone and scales it by 5/12.", secs=70)
assert F(57000) * F(5, 12) == 23750 and F(45600) * F(4, 12) == 15200 and F(22800) * F(5, 12) == 9500

b_cap = F(60000 * 12, 8)
units = [60000 * 12, b_cap * 8, 90000 * (12 - 4 - 6)]
c_ = F(198000 * units[2], sum(units))
assert b_cap == 90000 and units == [720000, 720000, 180000] and c_ == 22000
assert F(198000 * 540000, 720000 * 2 + 540000) == 54000 and F(198000 * 720000, sum(units)) == 88000
Q(T, "Compound partnership", A,
  "A starts a business with ₹60,000. B joins 4 months later, and C joins 6 months after B with ₹90,000. At the end of "
  "the year, B's share of the profit equals A's. If the year's profit is ₹1,98,000, what is C's share?",
  "₹22,000", ["₹54,000", "₹66,000", "₹88,000"],
  "Capital × months gives each partner's weight; use A = B to find B's capital first",
  "A: 60,000 × 12 = 7,20,000. B invests for 8 months, so B's capital × 8 = 7,20,000 ⇒ ₹90,000. C joins at the end "
  "of month 10 and invests for 2 months: 90,000 × 2 = 1,80,000. Ratio 72 : 72 : 18 = 4 : 4 : 1, so C gets "
  "1/9 × 1,98,000 = ₹22,000.",
  ["A = 7,20,000", "B: 8 months ⇒ capital 90,000 ⇒ 7,20,000", "C joins at month 4 + 6 = 10 ⇒ 2 months ⇒ 1,80,000",
   "4 : 4 : 1 ⇒ C = 22,000"],
  why="₹54,000 counts C's 6 months from the start of the year instead of from B's joining; ₹66,000 splits equally "
      "among three; ₹88,000 is A's (or B's) share.", secs=100)

ua = 20000 * 6 + 40000 * 6
ub = 30000 * 8 + 15000 * 4
uc = 40000 * 12
a_ = F(114000 * ua, ua + ub + uc)
assert (ua, ub, uc) == (360000, 300000, 480000) and a_ == 36000
Q(T, "Compound partnership", A,
  "A, B and C start a business with ₹20,000, ₹30,000 and ₹40,000. After 6 months A doubles his capital, and after 8 "
  "months B withdraws half of his. Out of a profit of ₹1,14,000 at the end of the year, what is A's share?",
  "₹36,000", ["₹38,000", "₹30,000", "₹48,000"],
  "Split each partner's year into periods of constant capital and add capital × months",
  "A: 20,000 × 6 + 40,000 × 6 = 3,60,000. B: 30,000 × 8 + 15,000 × 4 = 3,00,000. C: 40,000 × 12 = 4,80,000. Ratio "
  "36 : 30 : 48 = 6 : 5 : 8, so A gets 6/19 × 1,14,000 = ₹36,000.",
  ["A = 3,60,000", "B = 3,00,000", "C = 4,80,000", "6 : 5 : 8 ⇒ A = 1,14,000 × 6/19 = 36,000"],
  why="₹38,000 splits the profit equally among three; ₹30,000 is B's share; ₹48,000 is C's share.", secs=100)
assert F(114000, 3) == 38000 and F(114000 * 5, 19) == 30000 and F(114000 * 8, 19) == 48000

s_ = next(s for s in range(0, 80001, 500) if F(3, 5) * (80000 - s) + s == 54000)
b_ = F(2, 5) * (100000 - s_)
assert s_ == 15000 and b_ == 34000
Q(T, "Working partner", A,
  "A and B invest in the ratio 3 : 2. A runs the business and draws a fixed yearly salary from the profit before the "
  "rest is shared in the ratio of capitals. In a year when the profit was ₹80,000, A received ₹54,000 in all. How much "
  "will B receive in a year when the profit is ₹1,00,000 (same salary)?",
  "₹34,000", ["₹40,000", "₹26,000", "₹32,000"],
  "Find the salary from the first year: A's total = salary + 3/5 of (profit − salary)",
  "Year 1: S + 0.6(80,000 − S) = 54,000, so 48,000 + 0.4S = 54,000 and S = ₹15,000. Year 2: B gets 2/5 of "
  "(1,00,000 − 15,000) = ₹34,000.",
  ["S + 0.6(80,000 − S) = 54,000", "0.4S = 6,000 ⇒ S = 15,000", "Shared = 85,000", "B = 0.4 × 85,000 = 34,000"],
  why="₹40,000 ignores the salary; ₹26,000 is B's share in the first year; ₹32,000 deducts the salary twice "
      "(0.4 × 80,000).", secs=100)
assert F(2, 5) * 65000 == 26000 and F(2, 5) * 80000 == 32000

# ================================================================ Mixture and Alligation (B2 I3 A1)
T = "Mixture and Alligation"
q_ = F(30) * F(44 - 41, 41 - 36)
assert q_ == 18 and (36 * q_ + 44 * 30) / (q_ + 30) == 41
Q(T, "Alligation rule", B,
  "How many kg of sugar costing ₹36 per kg must be mixed with 30 kg of sugar costing ₹44 per kg so that the mixture "
  "costs ₹41 per kg?",
  "18 kg", ["50 kg", "24 kg", "30 kg"],
  "Alligation: cheaper : dearer = (dearer − mean) : (mean − cheaper)",
  "Cheaper : dearer = (44 − 41) : (41 − 36) = 3 : 5. With 30 kg of the dearer sugar, the cheaper is 30 × 3/5 = 18 kg.",
  ["(44 − 41) : (41 − 36) = 3 : 5", "5 parts = 30 kg ⇒ 1 part = 6 kg", "Cheaper = 3 × 6 = 18 kg",
   "Check: (18 × 36 + 30 × 44) ÷ 48 = 41"],
  why="50 kg reverses the ratio (5 : 3); 24 kg uses 4 : 5; 30 kg mixes equal quantities, which gives ₹40 per kg.",
  secs=45)

c_ = F(3 * 30 + 2 * 50, 5)
assert c_ == 38 and F(30 + 50, 2) == 40 and F(2 * 30 + 3 * 50, 5) == 42
Q(T, "Mixing solutions", B,
  "A 30% acid solution and a 50% acid solution are mixed in the ratio 3 : 2 by volume. What is the acid concentration "
  "of the mixture?",
  "38%", ["40%", "42%", "80%"],
  "The concentration of a mixture is the weighted average of the concentrations",
  "Take 3 litres of the 30% solution (0.9 litre acid) and 2 litres of the 50% solution (1 litre acid): 1.9 litres of "
  "acid in 5 litres = 38%.",
  ["3 × 30% = 0.9", "2 × 50% = 1.0", "1.9 ÷ 5 = 38%"],
  why="40% ignores the ratio; 42% swaps the weights (2 : 3); 80% adds the two concentrations.", secs=40)

fr = F(30 - 25, 30 - 15)
assert fr == F(1, 3) and (1 - fr) * 30 + fr * 15 == 25
Q(T, "Replacement of mixture", I,
  "Part of a 30% acid solution is drawn off and replaced with the same amount of a 15% acid solution. The result is "
  "a 25% acid solution. What fraction of the original solution was replaced?",
  "1/3", ["2/3", "1/2", "1/5"],
  "Alligation between the original (30%) and the replacement (15%) solutions about the result (25%)",
  "Kept : replaced = (25 − 15) : (30 − 25) = 10 : 5 = 2 : 1. So 1/3 of the solution was replaced.",
  ["Kept : replaced = (25 − 15) : (30 − 25)", "= 2 : 1", "Replaced fraction = 1/3",
   "Check: 2/3 × 30 + 1/3 × 15 = 25"],
  why="2/3 is the fraction kept; 1/2 assumes equal parts (which gives 22.5%); 1/5 divides the 5-point drop by 25.",
  secs=55)

r_ = (F(52) - 46) / (56 - 52)
assert r_ == F(3, 2)
Q(T, "Alligation rule", I,
  "The average weight of the students of a class is 52 kg. The average weight of the boys is 56 kg and that of the "
  "girls is 46 kg. What is the ratio of the number of boys to the number of girls?",
  "3 : 2", ["2 : 3", "28 : 23", "1 : 1"],
  "Alligation applies to any weighted average: each group's share is proportional to the other's distance from the "
  "mean",
  "Boys : girls = (52 − 46) : (56 − 52) = 6 : 4 = 3 : 2.",
  ["Distance of girls' average from 52 = 6", "Distance of boys' average from 52 = 4", "Boys : girls = 6 : 4 = 3 : 2",
   "Check: (3 × 56 + 2 × 46) ÷ 5 = 52"],
  why="2 : 3 crosses the distances the wrong way; 28 : 23 is just 56 : 46; 1 : 1 would give an average of 51 kg.",
  secs=50)

hi = F(50) * F(14 - 8, 18 - 8)
assert hi == 30 and (20 * F(8, 100) + 30 * F(18, 100)) / 50 * 100 == 14
Q(T, "Alligation rule", I,
  "A wholesaler has 50 kg of sugar. He sells part of it at 8% profit and the rest at 18% profit, and gains 14% on the "
  "whole. How many kg did he sell at 18% profit?",
  "30 kg", ["20 kg", "25 kg", "35 kg"],
  "Profit percentages combine like prices: alligate 8% and 18% about 14% (equal cost per kg)",
  "Quantity at 8% : quantity at 18% = (18 − 14) : (14 − 8) = 4 : 6 = 2 : 3. So 3/5 × 50 = 30 kg was sold at 18%.",
  ["(18 − 14) : (14 − 8) = 2 : 3", "18% part = 50 × 3/5 = 30 kg", "Check: (20 × 8 + 30 × 18) ÷ 50 = 14"],
  why="20 kg is the part sold at 8%; 25 kg splits equally (gives 13%); 35 kg uses 3 : 7.", secs=55)

a_milk, a_water = F(20 - 5), F(0)
b_milk, b_water = F(5), F(20)
mv = F(5) * b_milk / (b_milk + b_water)
wv = 5 - mv
a_milk, a_water = a_milk + mv, a_water + wv
assert (a_milk, a_water) == (16, 4) and a_water / (a_milk + a_water) == F(1, 5)
Q(T, "Replacement of mixture", A,
  "Jug A holds 20 litres of pure milk and jug B holds 20 litres of pure water. 5 litres are poured from A into B and "
  "mixed well, and then 5 litres of the mixture in B are poured back into A. What percentage of the liquid in A is "
  "now water?",
  "20%", ["25%", "16%", "50%"],
  "After the first pour, B's mixture is 1 : 4 milk to water; the 5 litres returned carry that ratio",
  "After the first pour, A has 15 L of milk and B has 5 L of milk + 20 L of water. 5 L from B contains 1 L of milk and "
  "4 L of water. A then has 16 L of milk and 4 L of water, so water is 4/20 = 20%.",
  ["A: 15 L milk; B: 5 L milk + 20 L water", "5 L from B = 1 L milk + 4 L water", "A: 16 L milk + 4 L water",
   "Water = 4/20 = 20%"],
  why="25% assumes the returned 5 L is all water; 16% treats the 4 L water as a share of 25 L; 50% assumes the two "
      "jugs end up identical.", secs=80)

# ================================================================ Time and Work (B1 I3 A2)
T = "Time and Work"
a_, b_ = F(5) / F(1, 4), F(12) / F(2, 5)
t_ = 1 / (1 / a_ + 1 / b_)
assert (a_, b_, t_) == (20, 30, 12)
Q(T, "Work efficiency", B,
  "A can do one-fourth of a job in 5 days, and B can do two-fifths of it in 12 days. In how many days can they finish "
  "the job working together?",
  "12 days", ["8.5 days", "25 days", "10 days"],
  "Convert each part-job time to a whole-job time first",
  "A alone takes 5 × 4 = 20 days; B alone takes 12 × 5/2 = 30 days. Together: 1/20 + 1/30 = 5/60 = 1/12, so 12 days.",
  ["A: 5 ÷ 1/4 = 20 days", "B: 12 ÷ 2/5 = 30 days", "1/20 + 1/30 = 1/12", "Together: 12 days"],
  why="8.5 days averages 5 and 12; 25 days averages 20 and 30; 10 days halves 20.", secs=45)
assert F(5 + 12, 2) == F(17, 2)

done_a = F(5, 15)
share_a = 4800 * done_a
assert share_a == 1600 and 4800 * F(5, 5 + 15) == 1200
Q(T, "Work and wages", I,
  "A and B can finish a job in 15 and 20 days respectively. They work together for 5 days; then A leaves and B "
  "finishes the job. The total payment for the job is ₹4,800. What is A's share?",
  "₹1,600", ["₹2,057", "₹1,200", "₹2,400"],
  "Wages are shared in proportion to the work each person actually did",
  "In 5 days A does 5/15 = 1/3 of the job. B does the remaining 2/3. So A gets 1/3 × 4,800 = ₹1,600.",
  ["A's work = 5 × 1/15 = 1/3", "B's work = 2/3", "A = 4,800 × 1/3 = 1,600"],
  why="₹2,057 shares in the ratio of efficiencies 4 : 3 (as if both worked throughout); ₹1,200 shares by days worked "
      "(5 : 15); ₹2,400 splits equally.", secs=60)
assert round(4800 * 3 / 7) == 2057 and round(4800 * 4 / 7) == 2743

rates = {"A": F(1, 12), "B": F(1, 15), "C": F(1, 20)}
work, day = F(0), 0
while work < 1:
    day += 1
    work += rates["A"] + (rates["B"] if day % 2 else rates["C"])
assert day == 7 and work == 1
Q(T, "Alternate days", I,
  "A, B and C can do a job alone in 12, 15 and 20 days respectively. A works every day; B helps him on the 1st, 3rd, "
  "5th, … days and C helps him on the 2nd, 4th, 6th, … days. On which day is the job completed?",
  "7th day", ["6th day", "8th day", "5th day"],
  "Take the job as 60 units (LCM); work in two-day cycles",
  "Daily units: A 5, B 4, C 3. A two-day cycle gives (5 + 4) + (5 + 3) = 17 units. Three cycles (6 days) give 51 units; "
  "on day 7 A and B add 9 more, making exactly 60. So the job ends on the 7th day.",
  ["Job = 60 units: A 5, B 4, C 3 per day", "Day 1 + day 2 = 9 + 8 = 17", "After 6 days: 51", "Day 7: 51 + 9 = 60"],
  why="6th day leaves 9 units undone; 8th day adds one cycle too many; 5th day assumes all three work every day "
      "(12 units a day ⇒ 5 days).", secs=70)

m_ = next(F(m) for m in range(1, 50) if 8 * (4 * m + 6) == 10 * (3 * m + 7))
work_ = 8 * (4 * m_ + 6)
assert m_ == 11 and work_ == 400 and work_ / 10 == 40
Q(T, "Men-women-children", I,
  "4 men and 6 women can finish a job in 8 days, while 3 men and 7 women can finish it in 10 days. In how many days "
  "can 10 women finish it?",
  "40 days", ["8 days", "10 days", "36.36 days"],
  "Equate the total work of the two groups to compare one man with one woman",
  "8(4m + 6w) = 10(3m + 7w) gives 32m + 48w = 30m + 70w, so m = 11w. The job = 8(44w + 6w) = 400 woman-days, so 10 "
  "women take 40 days.",
  ["8(4m + 6w) = 10(3m + 7w)", "2m = 22w ⇒ m = 11w", "Job = 8 × 50w = 400w", "10 women: 400 ÷ 10 = 40 days"],
  why="8 days and 10 days treat a man as equal to a woman (using the first or the second group); 36.36 days divides "
      "400 by 11, one man's worth of women, instead of by 10.", secs=70)
assert 8 * 10 / F(10) == 8 and 10 * 10 / F(10) == 10

hours = 1 / (F(1, 9 * 10) + F(1, 6 * 30))
assert hours == 60 and hours / F(15, 2) == 8
Q(T, "Work efficiency", A,
  "Working 9 hours a day, A can finish a job in 10 days. Working 6 hours a day, B can finish it in 30 days. If they "
  "work together for 7½ hours a day, in how many days will they finish it?",
  "8 days", ["7.5 days", "36 days", "4 days"],
  "Convert to total hours: A needs 90 hours, B 180 hours; combine hourly rates",
  "A's rate = 1/90 of the job per hour and B's = 1/180. Together 3/180 = 1/60 per hour, so they need 60 hours. At "
  "7½ hours a day that is 8 days.",
  ["A: 9 × 10 = 90 hours", "B: 6 × 30 = 180 hours", "1/90 + 1/180 = 1/60 ⇒ 60 hours", "60 ÷ 7.5 = 8 days"],
  why="7.5 days combines the day counts (1/10 + 1/30 = 2/15) and ignores the hours; 36 days adds the two times "
      "(90 + 180 hours ÷ 7.5); 4 days divides 60 hours by 15 (adds both daily hours).", secs=90)

abc, ab, bc = F(1, 6), F(1, 8), F(1, 12)
c_, a_ = abc - ab, abc - bc
b_ = abc - a_ - c_
assert (a_, b_, c_) == (F(1, 12), F(1, 24), F(1, 24)) and F(14400) * b_ / abc == 3600
Q(T, "Work and wages", A,
  "A and B together can do a job in 8 days, B and C together in 12 days, and A, B and C together in 6 days. All three "
  "do the job together and are paid ₹14,400. What is B's share?",
  "₹3,600", ["₹4,800", "₹7,200", "₹5,760"],
  "Find each person's daily rate by subtraction; wages follow the rates when all work for the same time",
  "C = 1/6 − 1/8 = 1/24; A = 1/6 − 1/12 = 1/12; B = 1/6 − 1/12 − 1/24 = 1/24. Rates A : B : C = 2 : 1 : 1, so B gets "
  "1/4 × 14,400 = ₹3,600.",
  ["C = ABC − AB = 1/24", "A = ABC − BC = 1/12", "B = 1/6 − 1/12 − 1/24 = 1/24", "2 : 1 : 1 ⇒ B = 3,600"],
  why="₹4,800 splits equally among three; ₹7,200 is A's share; ₹5,760 takes B and C's combined rate (1/12) as B's "
      "own rate, giving shares 2 : 2 : 1.",
  secs=90)
assert F(14400 * 2, 5) == 5760

# ================================================================ Pipes and Cisterns (B1 I1 A1)
T = "Pipes and Cisterns"
b_ = F(9) / F(3, 2)
t_ = 1 / (F(1, 9) + 1 / b_)
assert b_ == 6 and t_ == F(18, 5)
Q(T, "Inlet and outlet", B,
  "Pipe A can fill a tank in 9 hours. Pipe B is 50% more efficient than A. How long will both pipes take to fill the "
  "tank together?",
  "3.6 hours", ["4.5 hours", "6 hours", "3 hours"],
  "50% more efficient means 1.5 times the rate, so B takes 9 ÷ 1.5 hours",
  "B fills the tank in 9 ÷ 1.5 = 6 hours. Together: 1/9 + 1/6 = 5/18 per hour, so 18/5 = 3.6 hours (3 h 36 min).",
  ["B = 9 ÷ 1.5 = 6 hours", "1/9 + 1/6 = 2/18 + 3/18 = 5/18", "Time = 18/5 = 3.6 hours"],
  why="4.5 hours takes B as 50% faster but halves 9 only; 6 hours is B alone; 3 hours treats B as twice as fast.",
  secs=45)
assert 1 / (F(1, 9) + F(2, 9)) == 3

net = 2 * F(1, 12) - F(1, 8)
t_ = F(1, 3) / net
assert net == F(1, 24) and t_ == 8
Q(T, "Inlet and outlet", I,
  "A tank has two inlet pipes, each of which can fill it in 12 hours, and an outlet pipe that can empty it in 8 hours. "
  "The tank is two-thirds full when all three pipes are opened. How long will it take to fill the tank?",
  "8 hours", ["24 hours", "16 hours", "4 hours"],
  "Net rate = sum of inlet rates − outlet rate; only the empty third needs filling",
  "Net rate = 1/12 + 1/12 − 1/8 = 4/24 − 3/24 = 1/24 of the tank per hour. One-third remains, so the time is "
  "(1/3) ÷ (1/24) = 8 hours.",
  ["Inlets: 2 × 1/12 = 1/6", "Net = 1/6 − 1/8 = 1/24", "Remaining = 1/3", "Time = 24/3 = 8 hours"],
  why="24 hours fills a whole tank; 16 hours fills the two-thirds that are already full; 4 hours uses only one inlet "
      "and ignores the outlet (1/3 ÷ 1/12).", secs=60)

t_ = 5 + F(1, 2) / (F(1, 10) - F(1, 15))
assert t_ == 20
Q(T, "Leak problems", A,
  "A pipe fills a tank in 10 hours. There is a leak exactly halfway up the side of the tank. Whenever the water is "
  "above the leak, the leak drains water at a rate that would empty a full tank in 15 hours. How long does the pipe "
  "take to fill the empty tank?",
  "20 hours", ["30 hours", "15 hours", "12.5 hours"],
  "Below the leak the pipe works alone; above it the net rate is fill rate − leak rate",
  "The lower half fills at 1/10 per hour: 5 hours. Above the leak the net rate is 1/10 − 1/15 = 1/30 per hour, so the "
  "upper half takes (1/2) ÷ (1/30) = 15 hours. Total = 20 hours.",
  ["Lower half: 0.5 ÷ 0.1 = 5 h", "Net above leak = 1/10 − 1/15 = 1/30", "Upper half: 0.5 × 30 = 15 h",
   "Total = 20 h"],
  why="30 hours applies the leak to the whole tank; 15 hours counts only the upper half; 12.5 hours uses the net rate "
      "for the lower half and the full rate for the upper half (backwards).", secs=90)
assert 1 / (F(1, 10) - F(1, 15)) == 30

# ================================================================ Speed, Time and Distance (B1 I1 A1)
T = "Speed, Time and Distance"
avg = F(4 + 116, 1 + 2)
assert avg == 40 and F(4 + 58, 2) == 31 and F(4, 120) * 4 + F(116, 120) * 58 == F(562, 10)
Q(T, "Average speed", B,
  "Ravi walks 4 km to a bus stop at 4 km/h and then travels 116 km by bus at 58 km/h. What is his average speed for "
  "the whole journey?",
  "40 km/h", ["31 km/h", "56.2 km/h", "58 km/h"],
  "Average speed = total distance ÷ total time (not the average of the speeds)",
  "Walking takes 4 ÷ 4 = 1 hour and the bus 116 ÷ 58 = 2 hours. Total 120 km in 3 hours = 40 km/h.",
  ["Walk: 1 h", "Bus: 2 h", "120 km ÷ 3 h = 40 km/h"],
  why="31 km/h averages the two speeds; 56.2 km/h weights the speeds by distance instead of time; 58 km/h ignores "
      "the walk.", secs=40)

b_speed = F(50, 10)
b_time = F(1000) / b_speed
a_time = b_time - 10
assert (b_time, a_time) == (200, 190)
Q(T, "Meeting and overtaking", I,
  "In a 1 km race, A beats B by 50 m or by 10 seconds. How long does A take to run the race?",
  "190 seconds", ["200 seconds", "180 seconds", "210 seconds"],
  "'By 50 m or 10 seconds' means B covers the last 50 m in 10 seconds",
  "B runs 50 m in 10 s, so B's speed is 5 m/s and B takes 1,000 ÷ 5 = 200 s. A finishes 10 s earlier: 190 s.",
  ["B: 50 m in 10 s ⇒ 5 m/s", "B's time = 200 s", "A's time = 200 − 10 = 190 s"],
  why="200 s is B's time; 180 s subtracts 20 s; 210 s adds the 10 s instead of subtracting.", secs=50)

t_ = F(2 * 90, 12 + 18)
assert t_ == 6 and 90 - 12 * t_ == 18 and 12 * t_ == 72
Q(T, "Meeting and overtaking", A,
  "A and B start at the same time from town X towards town Y, 90 km away, at 12 km/h and 18 km/h. B reaches Y, turns "
  "back at once and meets A on the way. How far from Y do they meet?",
  "18 km", ["108 km", "72 km", "15 km"],
  "Up to the meeting, the two together cover twice the distance XY",
  "Together they cover 2 × 90 = 180 km at a combined 30 km/h, which takes 6 hours. A has then gone 12 × 6 = 72 km "
  "from X, so they meet 90 − 72 = 18 km from Y.",
  ["Combined distance = 180 km", "Time = 180 ÷ 30 = 6 h", "A: 72 km from X", "Distance from Y = 18 km"],
  why="108 km is the total distance B has run; 72 km is the meeting point's distance from X; 15 km divides 90 by "
      "the 6 hours.", secs=80)

# ================================================================ Boats and Streams (B1 I1 A1)
T = "Boats and Streams"
down = F(40, 2)
still, up = down - 4, down - 8
t_ = F(40) / up
assert (still, up, t_) == (16, 12, F(10, 3))
Q(T, "Upstream and downstream", B,
  "A boat goes 40 km downstream in 2 hours. The stream flows at 4 km/h. How long will the boat take to come back "
  "upstream over the same 40 km?",
  "3 hours 20 minutes", ["2 hours 30 minutes", "2 hours 51 minutes", "5 hours"],
  "Downstream speed = boat + stream; upstream speed = boat − stream",
  "Downstream speed = 40 ÷ 2 = 20 km/h, so the boat's own speed is 20 − 4 = 16 km/h and its upstream speed is 12 km/h. "
  "Time upstream = 40 ÷ 12 = 3⅓ hours = 3 hours 20 minutes.",
  ["Downstream = 20 km/h", "Boat = 16 km/h", "Upstream = 12 km/h", "40 ÷ 12 = 3⅓ h = 3 h 20 min"],
  why="2 h 30 min uses the boat's still-water speed 16 km/h; 2 h 51 min uses 14 km/h (subtracts the stream only "
      "half); 5 hours uses 8 km/h (subtracts the stream twice from 16).", secs=45)
assert F(40, 16) == F(5, 2) and F(40, 14) * 60 > 171 and F(40, 8) == 5

avg = F(2 * 12 * 8, 12 + 8)
assert avg == F(48, 5)
Q(T, "Upstream and downstream", I,
  "A boat whose speed in still water is 10 km/h goes some distance downstream and comes back the same distance "
  "upstream. The stream flows at 2 km/h. What is the boat's average speed for the round trip?",
  "9.6 km/h", ["10 km/h", "8 km/h", "11 km/h"],
  "Equal distances at two speeds: average speed = 2uv/(u + v), not (u + v)/2",
  "Downstream 12 km/h, upstream 8 km/h. For equal distances the average speed is 2 × 12 × 8 ÷ (12 + 8) = 192 ÷ 20 = "
  "9.6 km/h.",
  ["Downstream = 12, upstream = 8", "Average = 2 × 12 × 8/(12 + 8)", "= 9.6 km/h"],
  short="Average = (b² − s²)/b = (100 − 4)/10 = 9.6.",
  why="10 km/h averages 12 and 8 (as if the times were equal); 8 km/h is the upstream speed; 11 km/h has no basis in "
      "the round trip.", secs=55)

t_up, d_log = F(1), F(6)
s_ = d_log / (2 * t_up)
b_ = F(10)
assert s_ == 3
t_back = (d_log + (b_ - s_) * t_up) / (b_ + s_)
assert t_up + t_back == 2
assert (b_ - s_) * t_up + d_log == (b_ + s_) * t_back
Q(T, "Speed of stream", A,
  "A boat moving upstream passes a floating log at point P. One hour later the boat turns round (taking no time to "
  "turn) and goes downstream. It catches up with the log 6 km downstream of P. What is the speed of the stream?",
  "3 km/h", ["6 km/h", "2 km/h", "1.5 km/h"],
  "In the water's frame the log is still, so the boat takes as long to come back to the log as it took to leave it",
  "Relative to the water, the boat moves away from the log for 1 hour and back towards it at the same relative "
  "speed, so it returns after another hour. The log therefore drifted 6 km in 2 hours: the stream flows at 3 km/h.",
  ["Time away from the log (relative to the water) = 1 h", "Time back = 1 h", "Log drifts 6 km in 2 h",
   "Stream = 3 km/h"],
  short="Check with a boat speed of 10 km/h: upstream 7 km in 1 h, then 13 km at 13 km/h takes 1 h; the log moved "
        "3 × 2 = 6 km.",
  why="6 km/h assumes the log drifted for only 1 hour; 2 km/h divides by 3 hours; 1.5 km/h divides by 4 hours.",
  secs=90)

# ================================================================ Problems on Trains (B2 I2 A1)
T = "Problems on Trains"
v_ = F(280, 14)
t_ = F(280 + 420) / v_
assert v_ == 20 and t_ == 35 and F(420) / v_ == 21
Q(T, "Crossing a pole or platform", B,
  "A train 280 m long passes a signal pole in 14 seconds. How long will it take to pass completely through a tunnel "
  "420 m long?",
  "35 seconds", ["21 seconds", "14 seconds", "49 seconds"],
  "Passing a pole covers the train's length; passing through a tunnel covers train + tunnel",
  "Speed = 280 ÷ 14 = 20 m/s. Distance for the tunnel = 280 + 420 = 700 m, so the time = 700 ÷ 20 = 35 s.",
  ["Speed = 20 m/s", "Distance = 700 m", "Time = 35 s"],
  why="21 seconds covers only the tunnel's length; 14 seconds repeats the pole time; 49 seconds adds 14 to 35.",
  secs=40)

L_ = F(72 * 5, 18) * 40 / 4
assert L_ == 200
Q(T, "Crossing a pole or platform", B,
  "A train running at 72 km/h passes completely through a station whose platform is three times as long as the "
  "train, in 40 seconds. What is the length of the train?",
  "200 m", ["800 m", "266.67 m", "600 m"],
  "Platform crossing distance = train + platform = L + 3L = 4L",
  "72 km/h = 20 m/s. In 40 s the train covers 800 m = 4L, so L = 200 m.",
  ["72 × 5/18 = 20 m/s", "Distance = 20 × 40 = 800 m", "4L = 800 ⇒ L = 200 m"],
  why="800 m is the total distance; 266.67 m divides 800 by 3 (forgets the train's own length); 600 m is the "
      "platform.", secs=45)

slow = F(400, 10) / F(5, 2)
fast = slow * F(3, 2)
assert slow == 16 and fast == 24 and fast * F(18, 5) == F(864, 10)
Q(T, "Trains crossing each other", I,
  "Two trains 150 m and 250 m long, running in opposite directions on parallel tracks, cross each other completely in "
  "10 seconds. The faster train runs at 1.5 times the speed of the slower one. What is the speed of the faster train?",
  "86.4 km/h", ["57.6 km/h", "144 km/h", "54 km/h"],
  "Opposite directions: relative speed = sum of speeds; distance = sum of lengths",
  "Relative speed = (150 + 250) ÷ 10 = 40 m/s = s + 1.5s, so s = 16 m/s and the faster train runs at 24 m/s = "
  "24 × 3.6 = 86.4 km/h.",
  ["Relative speed = 400 ÷ 10 = 40 m/s", "2.5s = 40 ⇒ s = 16 m/s", "Faster = 24 m/s", "24 × 18/5 = 86.4 km/h"],
  why="57.6 km/h is the slower train; 144 km/h is the relative speed; 54 km/h uses only the 150 m train's length "
      "(15 m/s relative).", secs=60)
assert 16 * F(18, 5) == F(576, 10) and 40 * F(18, 5) == 144 and F(15) * F(18, 5) == 54

rel = F(54 - 36) * F(5, 18)
t_ = F(300) / rel
dist = F(54) * F(5, 18) * t_
assert rel == 5 and t_ == 60 and dist == 900
Q(T, "Trains crossing each other", I,
  "A 200 m long train running at 54 km/h overtakes a 100 m long train running at 36 km/h in the same direction on a "
  "parallel track. How far does the faster train travel while overtaking the slower one completely?",
  "900 m", ["300 m", "600 m", "540 m"],
  "Same direction: relative speed = difference; the faster train's ground distance = its own speed × overtaking time",
  "Relative speed = 18 km/h = 5 m/s. Overtaking needs 200 + 100 = 300 m of relative distance: 60 s. In 60 s the faster "
  "train runs 15 × 60 = 900 m.",
  ["Relative speed = 5 m/s", "Time = 300 ÷ 5 = 60 s", "Faster train speed = 15 m/s", "Distance = 900 m"],
  why="300 m is the relative distance, not the ground distance; 600 m is what the slower train covers in that time; "
      "540 m mixes km/h and seconds (54 × 10).", secs=60)

rel1 = F(150, 10)
train = rel1 + F(9) * F(5, 18)
rel2 = train + F(27) * F(5, 18)
t_ = F(150) / rel2
assert train == F(35, 2) and train * F(18, 5) == 63 and t_ == 6
Q(T, "Trains crossing each other", A,
  "A 150 m long train passes a man running at 9 km/h in the same direction in 10 seconds. How long will it take to "
  "pass a car (of negligible length) coming from the opposite direction at 27 km/h?",
  "6 seconds", ["10 seconds", "6⅔ seconds", "7.5 seconds"],
  "First find the train's speed from the same-direction pass, then use the sum of speeds for the car",
  "Relative speed with the man = 150 ÷ 10 = 15 m/s, so the train runs at 15 + 2.5 = 17.5 m/s (63 km/h). With the car: "
  "63 + 27 = 90 km/h = 25 m/s, and 150 ÷ 25 = 6 s.",
  ["Man: 9 km/h = 2.5 m/s", "Train = 15 + 2.5 = 17.5 m/s = 63 km/h", "Relative with car = 90 km/h = 25 m/s",
   "Time = 150 ÷ 25 = 6 s"],
  why="10 seconds repeats the first crossing; 6⅔ seconds forgets the man's speed and takes the train at 15 m/s "
      "(150 ÷ 22.5); 7.5 seconds subtracts the man's speed instead of adding it (12.5 + 7.5 = 20 m/s).",
  secs=100)

# ================================================================ Mensuration (B3 I3 A1)
T = "Mensuration"
s_ = F(13 + 14 + 15, 2)
area = math.isqrt(int(s_ * (s_ - 13) * (s_ - 14) * (s_ - 15)))
assert s_ == 21 and area == 84 and area ** 2 == s_ * 8 * 7 * 6
Q(T, "2D areas and perimeters", B, "What is the area of a triangle whose sides are 13 cm, 14 cm and 15 cm?",
  "84 cm²", ["105 cm²", "91 cm²", "42 cm²"],
  "Heron's formula: area = √(s(s − a)(s − b)(s − c)), where s is half the perimeter",
  "s = (13 + 14 + 15) ÷ 2 = 21. Area = √(21 × 8 × 7 × 6) = √7,056 = 84 cm².",
  ["s = 21", "s − a = 8, s − b = 7, s − c = 6", "21 × 8 × 7 × 6 = 7,056", "√7,056 = 84"],
  short="Split along the height to 14: it is 12 (5-12-13 and 9-12-15 triangles), so area = ½ × 14 × 12 = 84.",
  why="105 cm² is ½ × 14 × 15 (treats two sides as base and height); 91 cm² is ½ × 13 × 14; 42 cm² halves the "
      "correct area again.", secs=45)

n_ = (16 // 4) * (12 // 4) * (8 // 4)
assert n_ == 24 and 16 * 12 * 8 // 4 == 384
Q(T, "3D volume and surface area", B,
  "How many cubes of edge 4 cm can be cut from a cuboid measuring 16 cm × 12 cm × 8 cm?",
  "24", ["384", "96", "12"],
  "Number of cubes = (length ÷ edge) × (breadth ÷ edge) × (height ÷ edge)",
  "Along each side: 16 ÷ 4 = 4, 12 ÷ 4 = 3, 8 ÷ 4 = 2. Number of cubes = 4 × 3 × 2 = 24 (equivalently 1,536 ÷ 64).",
  ["16 ÷ 4 = 4", "12 ÷ 4 = 3", "8 ÷ 4 = 2", "4 × 3 × 2 = 24"],
  why="384 divides the volume by 4 instead of 4³; 96 divides by 16 (4²); 12 multiplies only two of the three counts.",
  secs=35)
assert 1536 // 16 == 96 and 4 * 3 == 12

circ = F(2 * 22 * 35, 7)
rev = F(110000) / circ
assert circ == 220 and rev == 500 and F(110000) / F(22 * 35, 7) == 1000
Q(T, "2D areas and perimeters", B,
  "A wheel has a radius of 35 cm. How many complete revolutions does it make in covering 1.1 km? (Use π = 22/7.)",
  "500", ["1,000", "250", "5,000"],
  "One revolution covers the circumference 2πr",
  "Circumference = 2 × 22/7 × 35 = 220 cm. 1.1 km = 1,10,000 cm. Revolutions = 1,10,000 ÷ 220 = 500.",
  ["2πr = 2 × 22/7 × 35 = 220 cm", "1.1 km = 1,10,000 cm", "1,10,000 ÷ 220 = 500"],
  why="1,000 uses πr (half the circumference); 250 uses the diameter as the radius; 5,000 converts 1.1 km to "
      "11,00,000 cm.", secs=40)

area = 3 * F(22, 7) * 7 * 7
assert area == 462 and 2 * F(22, 7) * 49 == 308 and 4 * F(22, 7) * 49 == 616
Q(T, "Cylinder, cone and sphere", I,
  "What is the total surface area of a solid hemisphere of radius 7 cm? (Use π = 22/7.)",
  "462 cm²", ["308 cm²", "616 cm²", "718.67 cm²"],
  "A solid hemisphere has a curved surface (2πr²) and a flat circular base (πr²): total 3πr²",
  "Total surface area = 3 × 22/7 × 7² = 3 × 154 = 462 cm².",
  ["Curved surface = 2πr² = 308", "Base = πr² = 154", "Total = 462 cm²"],
  why="308 cm² is the curved surface only; 616 cm² is the surface of a whole sphere; 718.67 cm² is the volume "
      "(2/3 πr³).", secs=50)
assert near(F(2, 3) * F(22, 7) * 343, 718.67, 0.01)

roads = 60 * 5 + 40 * 5 - 5 * 5
assert roads == 475
Q(T, "2D areas and perimeters", I,
  "A rectangular lawn measures 60 m × 40 m. Two roads, each 5 m wide, run through the middle of the lawn, one parallel "
  "to the length and the other parallel to the breadth. What is the total area of the roads?",
  "475 m²", ["500 m²", "450 m²", "2,400 m²"],
  "Add the two road areas and subtract the square where they cross (counted twice)",
  "Road along the length: 60 × 5 = 300 m². Road along the breadth: 40 × 5 = 200 m². They overlap in a 5 × 5 = 25 m² "
  "square. Total = 300 + 200 − 25 = 475 m².",
  ["60 × 5 = 300", "40 × 5 = 200", "Overlap = 25", "300 + 200 − 25 = 475 m²"],
  why="500 m² counts the crossing twice; 450 m² subtracts it twice; 2,400 m² is the whole lawn.", secs=50)

d_ = math.isqrt(12 ** 2 + 9 ** 2 + 8 ** 2)
assert d_ == 17 and d_ ** 2 == 289 and math.isqrt(144 + 81) == 15
Q(T, "3D volume and surface area", I,
  "What is the length of the longest rod that can be placed in a room 12 m long, 9 m wide and 8 m high?",
  "17 m", ["15 m", "29 m", "13 m"],
  "The longest rod lies along the space diagonal: √(l² + b² + h²)",
  "Diagonal = √(12² + 9² + 8²) = √(144 + 81 + 64) = √289 = 17 m.",
  ["12² + 9² + 8² = 289", "√289 = 17 m"],
  why="15 m is the floor diagonal √(12² + 9²); 29 m adds the three sides; 13 m is not the diagonal of any face here.",
  secs=50)

n_ = (F(22, 7) * 36 * 4) / (F(4, 3) * F(22, 7) * F(27, 8))
assert n_ == 32
Q(T, "Cylinder, cone and sphere", A,
  "A cylindrical jar of radius 6 cm contains water. How many solid spherical marbles, each of radius 1.5 cm, must be "
  "dropped in (fully submerged) to raise the water level by 4 cm? (π cancels out, so no value of π is needed.)",
  "32", ["4", "48", "24"],
  "The volume of the marbles equals the volume of water displaced: π × R² × rise",
  "Rise in volume = π × 6² × 4 = 144π cm³. One marble = 4/3 × π × 1.5³ = 4.5π cm³. Number = 144π ÷ 4.5π = 32.",
  ["Displaced volume = π × 36 × 4 = 144π", "Marble = 4/3 π × 3.375 = 4.5π", "144 ÷ 4.5 = 32"],
  why="4 uses the marble's diameter (3 cm) as its radius; 48 uses r² instead of r³ (4/3 × 2.25 = 3); 24 uses a "
      "rise of 3 cm.", secs=80)
assert F(144, F(4, 3) * 27) == 4 and 144 / (F(4, 3) * F(9, 4)) == 48 and 108 / F(9, 2) == 24

# ================================================================ Probability (B1 I1 A2)
T = "Probability"
nums = range(1, 31)
p_ = F(sum(1 for n in nums if n % 3 == 0 or n % 5 == 0), 30)
assert p_ == F(7, 15) and F(16, 30) == F(8, 15)
Q(T, "Balls from bags", B,
  "A bag contains 30 balls numbered 1 to 30. One ball is drawn at random. What is the probability that its number is "
  "a multiple of 3 or of 5?",
  "7/15", ["8/15", "1/2", "1/15"],
  "P(A or B) = P(A) + P(B) − P(A and B)",
  "Multiples of 3: 10. Multiples of 5: 6. Multiples of both (15, 30): 2. Favourable = 10 + 6 − 2 = 14, so "
  "P = 14/30 = 7/15.",
  ["Multiples of 3: 10", "Multiples of 5: 6", "Both: 2", "14/30 = 7/15"],
  why="8/15 does not subtract the 2 numbers counted twice; 1/2 counts 15 favourable; 1/15 is the probability of "
      "'both'.", secs=40, by=BRUTE)

dice = list(itertools.product(range(1, 7), repeat=2))
p_ = F(sum(1 for a, b in dice if a > b), 36)
assert p_ == F(5, 12)
Q(T, "Coins and dice", I,
  "Two fair dice, one red and one blue, are rolled. What is the probability that the number on the red die is greater "
  "than the number on the blue die?",
  "5/12", ["1/2", "7/12", "1/6"],
  "By symmetry, P(red > blue) = P(blue > red); remove the ties first",
  "There are 6 ties out of 36. The other 30 outcomes split equally, so 15 have red > blue: P = 15/36 = 5/12.",
  ["Ties: 6 of 36", "Remaining 30 split evenly", "Red > blue: 15", "P = 15/36 = 5/12"],
  why="1/2 forgets the ties; 7/12 counts 'greater than or equal'; 1/6 is the probability of a tie.", secs=50,
  by=BRUTE)

deck = [(r, s) for r in range(1, 14) for s in "HDCS"]
seq = list(itertools.permutations(range(52), 2))
p_ = F(sum(1 for i, j in seq if deck[i][0] == 1 and deck[j][0] == 13), len(seq))
assert p_ == F(4, 663) and F(4, 52) * F(4, 52) == F(1, 169) and F(4, 52) * F(3, 51) == F(1, 221)
Q(T, "Cards", A,
  "Two cards are drawn one after the other, without replacement, from a well-shuffled pack of 52 cards. What is the "
  "probability that the first is an ace and the second is a king?",
  "4/663", ["1/169", "1/221", "8/663"],
  "Multiply the probability of the first event by the conditional probability of the second",
  "P(first is an ace) = 4/52. With 51 cards left, all 4 kings remain: P(second is a king) = 4/51. Product = 16/2,652 "
  "= 4/663.",
  ["P(ace first) = 4/52 = 1/13", "P(king second | ace first) = 4/51", "1/13 × 4/51 = 4/663"],
  why="1/169 assumes the first card is replaced; 1/221 uses 3/51 as if a king had been removed; 8/663 also counts "
      "king-then-ace (the order is fixed in the question).", secs=60, by=BRUTE)

bagA = ["R"] * 5 + ["B"] * 3
bagB = ["R"] * 4 + ["B"] * 6
outs = list(itertools.product(bagA, bagB))
p_ = F(sum(1 for a, b in outs if (a == "R") != (b == "R")), len(outs))
assert p_ == F(21, 40) and F(5, 8) * F(4, 10) == F(1, 4) and F(5, 8) * F(6, 10) == F(3, 8)
Q(T, "Balls from bags", A,
  "Bag A contains 5 red and 3 blue balls; bag B contains 4 red and 6 blue balls. One ball is drawn at random from "
  "each bag. What is the probability that exactly one of the two balls is red?",
  "21/40", ["1/4", "3/8", "19/40"],
  "Exactly one red = (red from A, blue from B) or (blue from A, red from B); add the two cases",
  "P(R from A, B from B) = 5/8 × 6/10 = 30/80. P(B from A, R from B) = 3/8 × 4/10 = 12/80. Total = 42/80 = 21/40.",
  ["5/8 × 6/10 = 30/80", "3/8 × 4/10 = 12/80", "Sum = 42/80 = 21/40"],
  why="1/4 is P(both red); 3/8 counts only the first case; 19/40 is 1 − 21/40, the chance of 'both red or both "
      "blue'.", secs=70, by=BRUTE)

# ================================================================ Permutation and Combination (B1 I2 A2)
T = "Permutation and Combination"
diag = math.comb(10, 2) - 10
assert diag == 35
Q(T, "Selections", B, "How many diagonals does a polygon with 10 sides have?",
  "35", ["45", "70", "90"],
  "Every pair of vertices gives a side or a diagonal: diagonals = C(n, 2) − n",
  "Pairs of vertices = C(10, 2) = 45. Ten of them are sides, so there are 45 − 10 = 35 diagonals.",
  ["C(10, 2) = 45", "Sides = 10", "Diagonals = 35"],
  short="n(n − 3)/2 = 10 × 7 ÷ 2 = 35.",
  why="45 includes the 10 sides; 70 counts each diagonal from both ends (10 × 7); 90 counts ordered pairs of "
      "vertices (10 × 9).", secs=35)

arr = sum(1 for p in itertools.permutations(range(6)) if p[0] == 0
          and (abs(p.index(1) - p.index(2)) in (1, 5)))
assert arr == 48 and math.factorial(5) == 120
Q(T, "Arrangements", I,
  "In how many ways can 6 people sit around a round table if two particular people must sit next to each other? "
  "(Arrangements that differ only by a rotation are the same.)",
  "48", ["240", "24", "120"],
  "Tie the pair into one unit, arrange the units round the table in (n − 1)! ways, and multiply by the pair's 2 orders",
  "With the pair as one unit there are 5 units, which can be seated round a table in 4! = 24 ways. The pair can sit in "
  "2 orders, giving 24 × 2 = 48.",
  ["5 units in a circle: (5 − 1)! = 24", "Pair can swap: × 2", "24 × 2 = 48"],
  why="240 arranges the 5 units in a row (5! × 2); 24 forgets that the pair can swap; 120 is the number of circular "
      "arrangements with no condition.", secs=55, by=BRUTE)

word = "MORTGAGE"
perms = set(itertools.permutations(word))
tog = sum(1 for p in perms if "GG" in "".join(p))
assert len(perms) == 20160 and tog == 5040
Q(T, "Word arrangements", I,
  "In how many different ways can the letters of the word MORTGAGE be arranged so that the two G's are together?",
  "5,040", ["10,080", "20,160", "2,520"],
  "Glue the identical letters into one block; identical letters inside the block do not swap",
  "MORTGAGE has 8 letters with G twice. Treat GG as one block: 7 units, all different, giving 7! = 5,040 arrangements. "
  "Swapping the two G's gives nothing new.",
  ["Letters: M, O, R, T, G, A, G, E", "GG as one block ⇒ 7 distinct units", "7! = 5,040"],
  why="10,080 multiplies by 2! for swapping identical G's; 20,160 is the total number of arrangements with no "
      "condition (8!/2!); 2,520 divides 7! by 2! as if the G's were still separate.", secs=55, by=BRUTE)

pts = 12
tri = math.comb(pts, 3) - math.comb(5, 3)
assert tri == 210 and math.comb(12, 3) == 220
Q(T, "Selections", A,
  "There are 12 points in a plane, of which exactly 5 lie on one straight line; no other three of the points are "
  "collinear. How many triangles can be formed with vertices at these points?",
  "210", ["220", "205", "200"],
  "Count all triples, then remove the triples that lie on the line (they form no triangle)",
  "All triples: C(12, 3) = 220. Triples from the 5 collinear points: C(5, 3) = 10. Triangles = 220 − 10 = 210.",
  ["C(12, 3) = 220", "C(5, 3) = 10 (degenerate)", "220 − 10 = 210"],
  why="220 ignores the collinear points; 205 subtracts 5 (the points) instead of C(5, 3) = 10; 200 subtracts the "
      "10 collinear triples twice.", secs=70)

letters = sorted("LOANS")
rank = 1 + sum(1 for p in itertools.permutations(letters) if "".join(p) < "LOANS")
assert rank == 37
Q(T, "Word arrangements", A,
  "All the arrangements of the letters of the word LOANS are listed in dictionary (alphabetical) order. What is the "
  "rank (position) of the word LOANS in this list?",
  "37", ["36", "31", "25"],
  "Count the words that come before LOANS letter by letter: smaller first letters, then smaller second letters, …",
  "Letters in order: A, L, N, O, S. Words starting with A: 4! = 24. Words starting with L then A or N: 2 × 3! = 12. "
  "Next comes LOA…, and LOANS is the first such word (A, N, S in order). Rank = 24 + 12 + 1 = 37.",
  ["Start with A: 24", "Start with LA or LN: 2 × 6 = 12", "LOA + N, S in order: first", "Rank = 24 + 12 + 1 = 37"],
  why="36 forgets to add 1 for the word itself; 31 counts only the LA… words and misses LN… (24 + 6 + 1); 25 counts "
      "only the words starting with A, plus 1.", secs=90, by=BRUTE)

# ================================================================ Tabular DI (B4 I3 A1): two sets of 4
T = "Tabular DI"
EV = {"Indore": (4200, 1350, 650), "Nagpur": (3600, 1150, 850), "Coimbatore": (5100, 900, 1000),
      "Lucknow": (4800, 2100, 700), "Vadodara": (3300, 1000, 1200)}
sid = stimulus("data_table", "Electric vehicles registered in five cities, 2025",
               "The table shows the number of electric two-wheelers, three-wheelers and cars registered in five "
               "cities in the calendar year 2025.\n\n" +
               md_table(["City", "Two-wheelers", "Three-wheelers", "Cars"],
                        [[k, *[ind(x) for x in v]] for k, v in EV.items()]),
               {"columns": ["city", "two_wheelers", "three_wheelers", "cars"],
                "rows": [[k, *v] for k, v in EV.items()]})
tot = {k: sum(v) for k, v in EV.items()}
assert tot == {"Indore": 6200, "Nagpur": 5600, "Coimbatore": 7000, "Lucknow": 7600, "Vadodara": 5500}
Q(T, "Single table", B, "How many electric vehicles in all were registered in Coimbatore in 2025?",
  "7,000", ["6,000", "6,200", "7,600"],
  "Row total: add the three categories",
  "Coimbatore: 5,100 + 900 + 1,000 = 7,000.",
  ["5,100 + 900 = 6,000", "6,000 + 1,000 = 7,000"],
  why="6,000 leaves out the cars; 6,200 is Indore's total; 7,600 is Lucknow's total.", secs=30, stim=sid)

pc = F(2100, 4800) * 100
assert pc == F(175, 4) and near(F(4800, 2100) * 100, 228.57, 0.01) and near(F(2100, 7600) * 100, 27.63, 0.01)
Q(T, "Single table", B,
  "In Lucknow, the number of three-wheelers registered is what percentage of the number of two-wheelers registered?",
  "43.75%", ["228.57%", "56.25%", "27.63%"],
  "A as a percentage of B = A ÷ B × 100",
  "Lucknow: 2,100 three-wheelers and 4,800 two-wheelers. 2,100 ÷ 4,800 = 0.4375 = 43.75%.",
  ["2,100 ÷ 4,800 = 0.4375", "= 43.75%"],
  why="228.57% divides the other way (4,800 ÷ 2,100); 56.25% is 100% − 43.75%; 27.63% divides by Lucknow's total "
      "(7,600).", secs=40, stim=sid)

avg2 = F(sum(v[0] for v in EV.values()), 5)
pc = (avg2 - 3600) / 3600 * 100
assert avg2 == 4200 and pc == F(50, 3) and near(F(600, 4200) * 100, 14.29, 0.01)
Q(T, "Single table", I,
  "By what percentage is the average number of two-wheelers registered per city more than the number registered in "
  "Nagpur?",
  "16⅔%", ["14.29%", "116⅔%", "18.18%"],
  "Find the average first; 'more than Nagpur' uses Nagpur's figure as the base",
  "Two-wheelers: 4,200 + 3,600 + 5,100 + 4,800 + 3,300 = 21,000, average 4,200. The excess over Nagpur is 600, which "
  "is 600 ÷ 3,600 = 16⅔% of Nagpur's 3,600.",
  ["Total = 21,000", "Average = 4,200", "4,200 − 3,600 = 600", "600 ÷ 3,600 = 16⅔%"],
  why="14.29% divides by the average (4,200); 116⅔% is the average as a percentage of Nagpur's figure; 18.18% "
      "divides by Vadodara's 3,300 instead of Nagpur's 3,600.", secs=60, stim=sid)

over = [k for k, v in EV.items() if F(v[2], tot[k]) > F(12, 100)]
assert over == ["Nagpur", "Coimbatore", "Vadodara"]
Q(T, "Single table", I,
  "In how many of the five cities did cars make up more than 12% of all the electric vehicles registered in that "
  "city?",
  "3", ["2", "4", "1"],
  "Compare each city's cars with 12% of its own row total",
  "12% of each total: Indore 744 (cars 650, no); Nagpur 672 (850, yes); Coimbatore 840 (1,000, yes); Lucknow 912 "
  "(700, no); Vadodara 660 (1,200, yes). So 3 cities.",
  ["Indore: 650 < 744", "Nagpur: 850 > 672", "Coimbatore: 1,000 > 840", "Lucknow: 700 < 912", "Vadodara: 1,200 > 660",
   "Count = 3"],
  why="2 misses Coimbatore (14.3%); 4 includes Indore (10.5%); 1 counts only Vadodara, the clear leader.", secs=70,
  stim=sid)

SK = {"Kolar": (2400, 65, 40), "Hassan": (1800, 75, 48), "Mandya": (3000, 58, 50), "Tumakuru": (2500, 72, 45),
      "Udupi": (1600, 85, 55)}
sid = stimulus("data_table", "Candidates in a skill-certification test from five districts",
               "The table shows, for five districts, the number of candidates who appeared in a state skill-"
               "certification test, the percentage of them who passed, and the percentage of the passed candidates "
               "who were girls. Every candidate is either a girl or a boy.\n\n" +
               md_table(["District", "Appeared", "Passed (% of appeared)", "Girls (% of passed)"],
                        [[k, ind(a), p, g] for k, (a, p, g) in SK.items()]),
               {"columns": ["district", "appeared", "passed_pct", "girls_pct_of_passed"],
                "rows": [[k, *v] for k, v in SK.items()]})
passed = {k: a * F(p, 100) for k, (a, p, g) in SK.items()}
girls = {k: passed[k] * F(SK[k][2], 100) for k in SK}
boys = {k: passed[k] - girls[k] for k in SK}
assert passed == {"Kolar": 1560, "Hassan": 1350, "Mandya": 1740, "Tumakuru": 1800, "Udupi": 1360}
assert girls == {"Kolar": 624, "Hassan": 648, "Mandya": 870, "Tumakuru": 810, "Udupi": 748}
assert boys == {"Kolar": 936, "Hassan": 702, "Mandya": 870, "Tumakuru": 990, "Udupi": 612}
Q(T, "Table with percentages", B, "How many candidates from Mandya passed the test?",
  "1,740", ["1,260", "870", "1,800"],
  "Passed = appeared × pass percentage",
  "Mandya: 58% of 3,000 = 1,740.",
  ["3,000 × 0.58 = 1,740"],
  why="1,260 is the number who failed; 870 is the girls who passed; 1,800 is Tumakuru's figure.", secs=30, stim=sid)

Q(T, "Table with percentages", B, "How many girls from Udupi passed the test?",
  "748", ["612", "880", "1,360"],
  "Girls who passed = appeared × pass % × girls' %",
  "Udupi: passed = 85% of 1,600 = 1,360. Girls = 55% of 1,360 = 748.",
  ["Passed = 1,360", "Girls = 1,360 × 0.55 = 748"],
  why="612 is the boys who passed; 880 takes 55% of all 1,600 who appeared; 1,360 is everyone who passed.", secs=40,
  stim=sid)
assert 1600 * F(55, 100) == 880

assert max(boys, key=boys.get) == "Tumakuru" and max(SK, key=lambda k: SK[k][0]) == "Mandya"
Q(T, "Table with percentages", I, "Which district had the largest number of boys passing the test?",
  "Tumakuru", ["Kolar", "Mandya", "Udupi"],
  "Boys who passed = passed × (100 − girls' %)",
  "Boys passed: Kolar 936, Hassan 702, Mandya 870, Tumakuru 990, Udupi 612. Tumakuru is the largest.",
  ["Kolar: 1,560 × 0.60 = 936", "Hassan: 1,350 × 0.52 = 702", "Mandya: 1,740 × 0.50 = 870",
   "Tumakuru: 1,800 × 0.55 = 990", "Udupi: 1,360 × 0.45 = 612"],
  why="Kolar is second (936); Mandya had the most candidates but only half its passes were boys; Udupi has the "
      "highest pass rate but the fewest boys passing.", secs=65, stim=sid)

overall = F(sum(passed.values()), sum(v[0] for v in SK.values())) * 100
assert sum(passed.values()) == 7810 and sum(v[0] for v in SK.values()) == 11300
assert r2(overall) == F(6912, 100) and F(65 + 75 + 58 + 72 + 85, 5) == 71
assert r2(100 - overall) == F(3088, 100) and r2(F(sum(girls.values()), 7810) * 100) == F(4738, 100)
Q(T, "Table with percentages", A,
  "What was the overall pass percentage of the five districts taken together (correct to two decimal places)?",
  "69.12%", ["71%", "30.88%", "47.38%"],
  "Overall rate = total passed ÷ total appeared — not the average of the five rates",
  "Passed: 1,560 + 1,350 + 1,740 + 1,800 + 1,360 = 7,810. Appeared: 11,300. 7,810 ÷ 11,300 = 69.115…% ≈ 69.12%.",
  ["Total passed = 7,810", "Total appeared = 11,300", "7,810 ÷ 11,300 × 100 = 69.12%"],
  why="71% is the simple average of the five pass rates, which ignores the different numbers appearing; 30.88% is "
      "the overall fail rate; 47.38% is the girls' share of all who passed.", secs=90, stim=sid)

# ================================================================ Bar Graph DI (B1 I4 A4): sets of 5 and 4
T = "Bar Graph DI"
WAT = {"Ward 1": 84, "Ward 2": 96, "Ward 3": 72, "Ward 4": 120, "Ward 5": 108, "Ward 6": 60}
sid = stimulus("chart", "Water supplied to six wards of a town, June 2026",
               "The bar chart shows the water supplied by a town's municipal board to six wards in June 2026, in "
               "million litres (ML) (values read from the bars).\n\n" +
               md_table(["Ward", "Water supplied (ML)"], [[k, v] for k, v in WAT.items()]),
               {"chart_type": "bar", "x": list(WAT), "series": [{"name": "Water supplied (ML)",
                                                                 "values": list(WAT.values())}]})
assert sum(WAT.values()) == 540
Q(T, "Simple bar", B, "How much more water did Ward 4 receive than Ward 3?",
  "48 ML", ["24 ML", "36 ML", "12 ML"],
  "Read the two bars and subtract",
  "Ward 4 received 120 ML and Ward 3 72 ML. Difference = 48 ML.",
  ["120 − 72 = 48"],
  why="24 ML compares Ward 4 with Ward 2 (96); 36 ML compares Ward 5 (108) with Ward 3; 12 ML compares Ward 4 with "
      "Ward 5.", secs=25, stim=sid)

above = [k for k, v in WAT.items() if v > F(540, 6)]
assert above == ["Ward 2", "Ward 4", "Ward 5"]
Q(T, "Simple bar", I, "How many wards received more water than the average supply per ward?",
  "3", ["2", "4", "1"],
  "Average = total ÷ number of wards; then compare each bar",
  "Total = 84 + 96 + 72 + 120 + 108 + 60 = 540 ML, so the average is 90 ML. Wards 2 (96), 4 (120) and 5 (108) are "
  "above it: 3 wards.",
  ["Total = 540", "Average = 90", "Above 90: Wards 2, 4, 5"],
  why="2 misses Ward 2, which is only 6 ML above the average; 4 includes Ward 1 (84); 1 counts only the tallest bar.",
  secs=50, stim=sid)

pp = F(60 * 10 ** 6, 40000 * 30)
assert pp == 50 and F(60 * 10 ** 6, 40000) == 1500 and near(F(60 * 10 ** 6, 40000 * 31), 48.39, 0.01)
Q(T, "Simple bar", I,
  "Ward 6 has a population of 40,000. What was the average water supply per person per day in Ward 6 in June? "
  "(June has 30 days; 1 ML = 10 lakh litres.)",
  "50 litres", ["1,500 litres", "48.39 litres", "5 litres"],
  "Per person per day = monthly supply ÷ population ÷ days",
  "Ward 6 received 60 ML = 6,00,00,000 litres. Per person: 6,00,00,000 ÷ 40,000 = 1,500 litres in the month, or "
  "1,500 ÷ 30 = 50 litres a day.",
  ["60 ML = 6 crore litres", "÷ 40,000 = 1,500 litres per person per month", "÷ 30 = 50 litres per day"],
  why="1,500 litres is the monthly figure; 48.39 litres divides by 31 days; 5 litres treats 1 ML as 1 lakh litres.",
  secs=60, stim=sid)

lost = (84 + 108) * F(15, 100) + (540 - 84 - 108) * F(10, 100)
deliv = 540 - lost
assert deliv == F(4764, 10) and 540 * F(9, 10) == 486 and 540 * F(85, 100) == 459
assert 540 - ((84 + 108) * F(10, 100) + 348 * F(15, 100)) == F(4686, 10)
Q(T, "Simple bar", A,
  "Wards 1 and 5 lose 15% of their supply to leakage, and every other ward loses 10%. How much water actually reached "
  "consumers in the six wards in June?",
  "476.4 ML", ["486 ML", "459 ML", "468.6 ML"],
  "Apply each loss rate to its own wards' supply",
  "Wards 1 and 5 received 84 + 108 = 192 ML and lost 15% = 28.8 ML. The other wards received 348 ML and lost 10% = "
  "34.8 ML. Delivered = 540 − 63.6 = 476.4 ML.",
  ["Wards 1 + 5 = 192 ML; loss 28.8", "Others = 348 ML; loss 34.8", "Total loss = 63.6", "Delivered = 476.4 ML"],
  why="486 ML applies 10% to every ward; 459 ML applies 15% to every ward; 468.6 ML swaps the two rates.", secs=80,
  stim=sid)

july = sum(v * (F(70, 100) if k == "Ward 4" else F(115, 100)) for k, v in WAT.items())
pc = (july - 540) / 540 * 100
assert july == 567 and pc == 5 and F(5 * 15 - 30, 6) == F(15, 2)
Q(T, "Simple bar", A,
  "In July, supply to every ward rises by 15% over June, except Ward 4, whose supply falls by 30%. By what percentage "
  "does the total supply to the six wards change from June to July?",
  "Increases by 5%", ["Increases by 15%", "Increases by 7.5%", "Decreases by 15%"],
  "Compute July's total from each ward's own change; percentage changes cannot simply be averaged",
  "Five wards other than Ward 4 had 420 ML; +15% gives 483 ML. Ward 4: 120 × 0.7 = 84 ML. July total = 567 ML against "
  "540 ML in June: an increase of 27 ML = 5%.",
  ["Others: 420 × 1.15 = 483", "Ward 4: 120 × 0.70 = 84", "July = 567", "(567 − 540) ÷ 540 = 5%"],
  why="'Increases by 15%' ignores Ward 4's fall; 'increases by 7.5%' averages the six percentage changes; "
      "'decreases by 15%' subtracts 30 from 15.", secs=90, stim=sid)

MILK = {"Village P": (14, 8), "Village Q": (9, 12), "Village R": (16, 6), "Village S": (11, 14)}
sid = stimulus("chart", "Cow and buffalo milk collected by a dairy cooperative from four villages in a week",
               "The grouped bar chart shows the cow milk and the buffalo milk (in thousand litres) collected by a "
               "dairy cooperative from four villages in one week (values read from the bars).\n\n" +
               md_table(["Village", "Cow milk (thousand L)", "Buffalo milk (thousand L)"],
                        [[k, *v] for k, v in MILK.items()]),
               {"chart_type": "grouped_bar", "x": list(MILK),
                "series": [{"name": "Cow milk", "values": [v[0] for v in MILK.values()]},
                           {"name": "Buffalo milk", "values": [v[1] for v in MILK.values()]}]})
cow, buf = sum(v[0] for v in MILK.values()), sum(v[1] for v in MILK.values())
assert (cow, buf) == (50, 40) and F(buf, cow) * 100 == 80 and near(F(buf, cow + buf) * 100, 44.44, 0.01)
Q(T, "Stacked or grouped bar", I,
  "The total buffalo milk collected from the four villages is what percentage of the total cow milk collected?",
  "80%", ["125%", "44.44%", "20%"],
  "Add each series across the villages, then divide",
  "Cow milk = 14 + 9 + 16 + 11 = 50 thousand litres. Buffalo milk = 8 + 12 + 6 + 14 = 40 thousand litres. 40 ÷ 50 = "
  "80%.",
  ["Cow total = 50", "Buffalo total = 40", "40 ÷ 50 × 100 = 80%"],
  why="125% divides the other way; 44.44% is buffalo milk's share of all milk; 20% is how much less buffalo milk "
      "there is.", secs=50, stim=sid)

share = {k: F(b, c + b) for k, (c, b) in MILK.items()}
assert max(share, key=share.get) == "Village Q" and max(MILK, key=lambda k: MILK[k][1]) == "Village S"
Q(T, "Stacked or grouped bar", I,
  "In which village did buffalo milk form the largest share of that village's total milk collection?",
  "Village Q", ["Village S", "Village P", "Village R"],
  "Compare buffalo ÷ (cow + buffalo) for each village",
  "Buffalo shares: P 8/22 ≈ 36.4%, Q 12/21 ≈ 57.1%, R 6/22 ≈ 27.3%, S 14/25 = 56%. Village Q is highest.",
  ["P ≈ 36.4%", "Q ≈ 57.1%", "R ≈ 27.3%", "S = 56%"],
  why="Village S has the most buffalo milk but also more cow milk, so its share (56%) is just below Q's; P and R "
      "have much lower shares.", secs=60, stim=sid)

pay = 11000 * 42 + 14000 * 58
assert pay == 1274000 and 11000 * 58 + 14000 * 42 == 1226000 and 25000 * 50 == 1250000 and 25000 * 58 == 1450000
Q(T, "Stacked or grouped bar", A,
  "The cooperative pays ₹42 per litre for cow milk and ₹58 per litre for buffalo milk. How much did it pay Village S "
  "for the week's milk?",
  "₹12,74,000", ["₹12,26,000", "₹12,50,000", "₹14,50,000"],
  "Price each kind of milk separately; the bars are in thousand litres",
  "Village S: cow 11,000 L × ₹42 = ₹4,62,000; buffalo 14,000 L × ₹58 = ₹8,12,000. Total = ₹12,74,000.",
  ["11,000 × 42 = 4,62,000", "14,000 × 58 = 8,12,000", "Total = 12,74,000"],
  why="₹12,26,000 swaps the two prices; ₹12,50,000 uses the average price ₹50 for all 25,000 litres; ₹14,50,000 pays "
      "the buffalo-milk price for all of it.", secs=70, stim=sid)

fat = (cow * F(4, 100) + buf * F(7, 100)) / (cow + buf) * 100
assert fat == F(16, 3) and (cow * F(7, 100) + buf * F(4, 100)) / 90 * 100 == F(17, 3)
Q(T, "Stacked or grouped bar", A,
  "Cow milk contains 4% fat and buffalo milk 7% fat. If all the milk collected from the four villages is mixed "
  "together, what is the fat percentage of the mixture?",
  "5⅓%", ["5.5%", "5⅔%", "4.8%"],
  "Fat % of a mixture is the quantity-weighted average of the fat percentages",
  "Fat = 50 × 4% + 40 × 7% = 2 + 2.8 = 4.8 thousand litres in 90 thousand litres of milk, so 4.8 ÷ 90 = 5⅓%.",
  ["Cow fat = 50 × 0.04 = 2.0", "Buffalo fat = 40 × 0.07 = 2.8", "Total fat = 4.8 in 90", "4.8 ÷ 90 = 5⅓%"],
  why="5.5% is the simple average of 4% and 7%; 5⅔% swaps the quantities (50 of buffalo milk, 40 of cow milk); 4.8% "
      "is the fat in thousand litres, not a percentage.", secs=80, stim=sid)

# ================================================================ Pie Chart DI (B2 I5 A1): two sets of 4
T = "Pie Chart DI"
EXP = {"Salaries": 35, "Marketing": 20, "Technology": 15, "Content": 12, "Rent": 8, "Others": 10}
assert sum(EXP.values()) == 100
sid = stimulus("chart", "Expenditure of an ed-tech start-up by head, 2025-26",
               "The pie chart shows how an ed-tech start-up's total expenditure of ₹48 crore in 2025-26 was divided "
               "among six heads (percentage of the total).\n\n" +
               md_table(["Head", "Share of expenditure (%)"], [[k, v] for k, v in EXP.items()]),
               {"chart_type": "pie", "unit": "percent", "total_rs_crore": 48,
                "labels": list(EXP), "values": list(EXP.values())})
amt = {k: F(48 * v, 100) for k, v in EXP.items()}
assert amt["Technology"] == F(72, 10)
Q(T, "Percentage-based", B, "How much did the start-up spend on technology in 2025-26?",
  "₹7.2 crore", ["₹15 crore", "₹5.76 crore", "₹9.6 crore"],
  "Amount = percentage × total",
  "Technology is 15% of ₹48 crore = ₹7.2 crore.",
  ["48 × 15/100 = 7.2"],
  why="₹15 crore reads the percentage as crore; ₹5.76 crore is content (12%); ₹9.6 crore is marketing (20%).",
  secs=30, stim=sid)

d_ = F(48 * (35 - 20 - 8), 100)
assert d_ == F(336, 100)
Q(T, "Percentage-based", I,
  "By how much did spending on salaries exceed the combined spending on marketing and rent?",
  "₹3.36 crore", ["₹7 crore", "₹7.2 crore", "₹11.04 crore"],
  "Subtract the percentages first, then convert to rupees",
  "Salaries 35% against marketing + rent = 20% + 8% = 28%. The gap is 7% of ₹48 crore = ₹3.36 crore.",
  ["20 + 8 = 28%", "35 − 28 = 7%", "7% of 48 = 3.36 crore"],
  why="₹7 crore leaves the gap as a percentage; ₹7.2 crore subtracts content + rent (20%) instead of marketing + rent; "
      "₹11.04 crore subtracts only rent (27%).", secs=45, stim=sid)
assert F(48 * 15, 100) == F(72, 10) and F(48 * 23, 100) == F(1104, 100)

assert EXP["Marketing"] * F(360, 100) == 72
Q(T, "Percentage-based", I, "What is the central angle of the sector for marketing?",
  "72°", ["20°", "54°", "36°"],
  "Central angle = percentage × 360 ÷ 100 = percentage × 3.6",
  "Marketing is 20% of the total, so its angle is 20 × 3.6 = 72°.",
  ["20% × 360° = 72°"],
  why="20° reads the percentage as degrees; 54° is technology's angle (15%); 36° is the angle for 'Others' (10%).",
  secs=30, stim=sid)

new_sal, new_tot = amt["Salaries"] * F(120, 100), 48 * F(125, 100)
pc = new_sal / new_tot * 100
assert pc == F(336, 10) and 35 * F(12, 10) == 42 and F(35, F(125, 100)) == 28
Q(T, "Percentage-based", I,
  "In 2026-27 the start-up's total expenditure rises by 25% and its spending on salaries rises by 20%. What "
  "percentage of the new total will salaries be?",
  "33.6%", ["35%", "42%", "28%"],
  "New share = old share × (1 + salary growth) ÷ (1 + total growth)",
  "Salaries were ₹16.8 crore; 20% more is ₹20.16 crore. The new total is ₹60 crore. 20.16 ÷ 60 = 33.6%.",
  ["Salaries = 16.8 × 1.2 = 20.16 crore", "Total = 48 × 1.25 = 60 crore", "20.16 ÷ 60 = 33.6%"],
  short="35 × 1.2 ÷ 1.25 = 33.6.",
  why="35% assumes the share is unchanged; 42% applies only the salary growth; 28% applies only the total's growth.",
  secs=60, stim=sid)

CROP = {"Wheat": 108, "Rice": 72, "Pulses": 54, "Oilseeds": 45, "Sugarcane": 36, "Vegetables": 27, "Others": 18}
assert sum(CROP.values()) == 360
sid = stimulus("chart", "Area under different crops in a district (central angles)",
               "The pie chart shows how the 7,200 hectares of cultivated land in a district were divided among "
               "crops in the 2025-26 rabi and kharif seasons together. The central angle of each sector is "
               "given.\n\n" + md_table(["Crop", "Central angle (degrees)"], [[k, v] for k, v in CROP.items()]),
               {"chart_type": "pie", "unit": "degrees", "total_hectares": 7200,
                "labels": list(CROP), "values": list(CROP.values())})
per = F(7200, 360)
area = {k: v * per for k, v in CROP.items()}
assert per == 20 and area["Pulses"] == 1080 and 7200 * F(54, 100) == 3888
Q(T, "Degree-based", B, "How many hectares are under pulses?",
  "1,080", ["900", "1,440", "3,888"],
  "Area = angle ÷ 360 × total",
  "Each degree stands for 7,200 ÷ 360 = 20 hectares. Pulses have 54°, so 54 × 20 = 1,080 hectares.",
  ["1° = 20 ha", "54 × 20 = 1,080 ha"],
  why="900 uses oilseeds' 45°; 1,440 uses rice's 72°; 3,888 reads 54 as a percentage of 7,200.", secs=30, stim=sid)

pc = F(108 - 72, 72) * 100
assert pc == 50 and near(F(36, 108) * 100, 33.33, 0.01)
Q(T, "Degree-based", I, "The area under wheat is what percentage more than the area under rice?",
  "50%", ["33.33%", "36%", "150%"],
  "Percentage more can be worked out directly from the angles",
  "Wheat 108°, rice 72°. The difference 36° is 36 ÷ 72 = 50% of rice's angle, so wheat's area is 50% more.",
  ["108 − 72 = 36", "36 ÷ 72 × 100 = 50%"],
  why="33.33% divides by wheat's 108°; 36% reads the difference in degrees as a percentage; 150% is wheat as a "
      "percentage of rice.", secs=40, stim=sid)

prod = area["Sugarcane"] * 70 + area["Vegetables"] * 18
assert prod == 60120 and area["Sugarcane"] * 18 + area["Vegetables"] * 70 == 50760 and area["Sugarcane"] * 70 == 50400
assert (area["Sugarcane"] + area["Vegetables"]) * 44 == 55440
Q(T, "Degree-based", I,
  "Sugarcane yields 70 tonnes per hectare and vegetables 18 tonnes per hectare. What is the total production of "
  "sugarcane and vegetables together?",
  "60,120 tonnes", ["50,760 tonnes", "55,440 tonnes", "50,400 tonnes"],
  "Convert each angle to hectares, then multiply by that crop's own yield",
  "Sugarcane: 36 × 20 = 720 ha × 70 = 50,400 t. Vegetables: 27 × 20 = 540 ha × 18 = 9,720 t. Total = 60,120 tonnes.",
  ["Sugarcane area = 720 ha ⇒ 50,400 t", "Vegetable area = 540 ha ⇒ 9,720 t", "Total = 60,120 t"],
  why="50,760 tonnes swaps the yields; 55,440 tonnes applies the average yield (44 t/ha) to both; 50,400 tonnes is "
      "sugarcane alone.", secs=60, stim=sid)

pul, ric = CROP["Pulses"] + CROP["Rice"] * F(1, 4), CROP["Rice"] * F(3, 4)
assert ratio(pul, ric) == "4 : 3" and ratio(CROP["Pulses"] * F(5, 4), ric) == "5 : 4" and ratio(54 + 25, 72 - 25) == "79 : 47"
Q(T, "Degree-based", A,
  "Next year, one-fourth of the area now under rice is shifted to pulses, and nothing else changes. What will be the "
  "ratio of the area under pulses to the area under rice?",
  "4 : 3", ["3 : 4", "5 : 4", "79 : 47"],
  "Move the shifted area out of one sector and into the other; the total is unchanged",
  "One-fourth of rice's 72° is 18°. Rice falls to 54° and pulses rise to 54 + 18 = 72°. Ratio = 72 : 54 = 4 : 3.",
  ["¼ × 72° = 18°", "Rice: 72 − 18 = 54°", "Pulses: 54 + 18 = 72°", "72 : 54 = 4 : 3"],
  why="3 : 4 is reversed; 5 : 4 raises pulses by a quarter of their own area instead of rice's; 79 : 47 shifts 25 "
      "degrees instead of 25%.", secs=70, stim=sid)

# ================================================================ Line Graph DI (B1 I3 A2): two sets of 3
T = "Line Graph DI"
MET = {"Jan": 240, "Feb": 225, "Mar": 270, "Apr": 300, "May": 285, "Jun": 330}
sid = stimulus("chart", "Passengers using a metro station each month, January to June 2026",
               "The line graph shows the number of passengers (in thousand) who used a metro station in each month "
               "from January to June 2026.\n\n" +
               md_table(["Month", "Passengers (thousand)"], [[k, v] for k, v in MET.items()]),
               {"chart_type": "line", "x": list(MET), "series": [{"name": "Passengers (thousand)",
                                                                  "values": list(MET.values())}]})
assert sum(MET.values()) == 1650 and F(1650, 6) == 275
Q(T, "Single line", B, "What was the average number of passengers per month over the six months?",
  "2,75,000", ["2,85,000", "3,30,000", "2,70,000"],
  "Average = total of the six values ÷ 6; the values are in thousands",
  "Total = 240 + 225 + 270 + 300 + 285 + 330 = 1,650 thousand. Average = 1,650 ÷ 6 = 275 thousand = 2,75,000.",
  ["Total = 1,650 thousand", "÷ 6 = 275 thousand"],
  why="2,85,000 averages only January and June; 3,30,000 divides by 5 instead of 6; 2,70,000 is March's figure.",
  secs=40, stim=sid)
assert F(240 + 330, 2) == 285 and F(1650, 5) == 330

m = list(MET)
chg = {m[i]: F(MET[m[i]] - MET[m[i - 1]], MET[m[i - 1]]) for i in range(1, 6)}
assert max(chg, key=chg.get) == "Mar" and chg["Mar"] == F(1, 5) and near(chg["Jun"] * 100, 15.79, 0.01)
Q(T, "Single line", I, "In which month was the percentage increase in passengers over the previous month the "
  "highest?",
  "March", ["June", "April", "May"],
  "Percentage change = change ÷ previous month's value; a large absolute rise on a large base can be a smaller "
  "percentage",
  "Changes: Feb −6.25%, Mar +45 on 225 = +20%, Apr +30 on 270 ≈ +11.1%, May −5%, Jun +45 on 285 ≈ +15.8%. March is "
  "highest.",
  ["Mar: 45/225 = 20%", "Apr: 30/270 ≈ 11.1%", "Jun: 45/285 ≈ 15.8%", "Feb and May fell"],
  why="June has the same absolute rise as March (45 thousand) but on a larger base; April's rise is smaller; May "
      "fell.", secs=60, stim=sid)

q1, q2 = sum(list(MET.values())[:3]), sum(list(MET.values())[3:])
d_ = q2 * 1000 * 42 - q1 * 1000 * 38
assert (q1, q2) == (735, 915) and d_ == 10500000
assert (q2 - q1) * 1000 * 38 == 6840000 and (q2 - q1) * 1000 * 42 == 7560000 and q1 * 1000 * 4 == 2940000
Q(T, "Single line", A,
  "The average fare was ₹38 per passenger in January–March and ₹42 per passenger in April–June. By how much did the "
  "fare revenue of April–June exceed that of January–March?",
  "₹1.05 crore", ["₹68.4 lakh", "₹75.6 lakh", "₹29.4 lakh"],
  "Revenue = passengers × fare for each quarter; both the count and the fare changed",
  "January–March: 735 thousand × ₹38 = ₹2.793 crore. April–June: 915 thousand × ₹42 = ₹3.843 crore. Difference = "
  "₹1.05 crore.",
  ["Q1 passengers = 7,35,000 ⇒ × 38 = 2,79,30,000", "Q2 passengers = 9,15,000 ⇒ × 42 = 3,84,30,000",
   "Difference = 1,05,00,000 = ₹1.05 crore"],
  why="₹68.4 lakh prices the 1,80,000 extra passengers at ₹38 and ignores the fare rise; ₹75.6 lakh prices them at "
      "₹42 only; ₹29.4 lakh is only the effect of the ₹4 fare rise on the first quarter's passengers.", secs=90,
  stim=sid)

RX = {"Jun": 180, "Jul": 320, "Aug": 290, "Sep": 210, "Oct": 100}
RY = {"Jun": 150, "Jul": 260, "Aug": 300, "Sep": 220, "Oct": 70}
sid = stimulus("chart", "Monsoon rainfall in two cities, June to October 2025",
               "The line graph shows the rainfall (in mm) recorded in City X and City Y in each month from June to "
               "October 2025.\n\n" +
               md_table(["Month", "City X (mm)", "City Y (mm)"], [[k, RX[k], RY[k]] for k in RX]),
               {"chart_type": "line", "x": list(RX), "series": [{"name": "City X", "values": list(RX.values())},
                                                                {"name": "City Y", "values": list(RY.values())}]})
tx, ty = sum(RX.values()), sum(RY.values())
assert (tx, ty) == (1100, 1000) and F(tx - ty, ty) * 100 == 10 and near(F(100, 1100) * 100, 9.09, 0.01)
Q(T, "Multiple lines", I,
  "City X's total rainfall for the five months was what percentage more than City Y's?",
  "10%", ["9.09%", "110%", "100%"],
  "Add each line's five values; 'more than Y' uses Y's total as the base",
  "City X: 180 + 320 + 290 + 210 + 100 = 1,100 mm. City Y: 150 + 260 + 300 + 220 + 70 = 1,000 mm. X is 100 mm, or "
  "10%, more.",
  ["X = 1,100 mm", "Y = 1,000 mm", "100 ÷ 1,000 = 10%"],
  why="9.09% divides by X's total; 110% is X as a percentage of Y; 100% reads the 100 mm difference as a percentage.",
  secs=55, stim=sid)

gap = {k: abs(RX[k] - RY[k]) for k in RX}
assert max(gap, key=gap.get) == "Jul" and gap["Jul"] == 60
Q(T, "Multiple lines", I, "In which month was the difference between the rainfall of the two cities the largest?",
  "July", ["August", "October", "June"],
  "Read the vertical gap between the two lines for each month",
  "Gaps: June 30 mm, July 60 mm, August 10 mm, September 10 mm, October 30 mm. The largest is July.",
  ["Jun 30", "Jul 60", "Aug 10", "Sep 10", "Oct 30"],
  why="August is Y's wettest month but the cities differ by only 10 mm; October and June differ by 30 mm.", secs=45,
  stim=sid)

nx, ny = tx * F(9, 10), ty * F(11, 10)
assert ny - nx == 110
Q(T, "Multiple lines", A,
  "In 2026, City X's rainfall in each of these months is 10% less than in 2025, and City Y's is 10% more. By how many "
  "millimetres will City Y's five-month total exceed City X's?",
  "110 mm", ["10 mm", "210 mm", "0 mm"],
  "A uniform percentage change in every month changes the total by the same percentage",
  "X's total becomes 1,100 × 0.9 = 990 mm and Y's becomes 1,000 × 1.1 = 1,100 mm. Y exceeds X by 110 mm.",
  ["X: 1,100 × 0.9 = 990", "Y: 1,000 × 1.1 = 1,100", "1,100 − 990 = 110 mm"],
  why="10 mm applies the 10% changes to the 100 mm gap only; 210 mm adds the old 100 mm gap to the new one; 0 mm "
      "assumes a 10% fall and a 10% rise cancel.", secs=70, stim=sid)

# ================================================================ Caselet DI (B5 I3 A3): sets of 6 and 5
T = "Caselet DI"
sid = stimulus("caselet", "Members and fees of a fitness centre, October 2026",
               "In October 2026 a fitness centre had 840 members, each on exactly one plan: monthly, quarterly or "
               "annual. Three-sevenths of the members were on the monthly plan, and the number on the quarterly plan "
               "was 60 less than the number on the monthly plan; the rest were on the annual plan. Women made up 40% "
               "of the monthly-plan members, 45% of the quarterly-plan members and two-thirds of the annual-plan "
               "members. The monthly plan costs ₹1,500 a month, the quarterly plan ₹4,000 a quarter and the annual "
               "plan ₹14,400 a year.")
mon = 840 * F(3, 7)
qtr = mon - 60
ann = 840 - mon - qtr
w = {"m": mon * F(40, 100), "q": qtr * F(45, 100), "a": ann * F(2, 3)}
assert (mon, qtr, ann) == (360, 300, 180) and w == {"m": 144, "q": 135, "a": 120}
assert sum(w.values()) == 399 and 840 - 399 == 441
Q(T, "Paragraph data", B, "How many members were on the annual plan?",
  "180", ["300", "240", "120"],
  "Members on annual plan = total − monthly − quarterly",
  "Monthly = 3/7 × 840 = 360. Quarterly = 360 − 60 = 300. Annual = 840 − 360 − 300 = 180.",
  ["Monthly = 360", "Quarterly = 300", "Annual = 180"],
  why="300 is the quarterly plan; 240 splits the non-monthly 480 equally; 120 is the number of women on the annual "
      "plan.", secs=40, stim=sid)

Q(T, "Paragraph data", B, "How many women members did the centre have in all?",
  "399", ["441", "420", "336"],
  "Apply each plan's own percentage of women and add",
  "Women: monthly 40% of 360 = 144, quarterly 45% of 300 = 135, annual 2/3 of 180 = 120. Total = 399.",
  ["144 + 135 + 120 = 399"],
  why="441 is the number of men; 420 assumes half the members are women; 336 applies the monthly plan's 40% to all "
      "840.", secs=45, stim=sid)

assert qtr - w["q"] == 165 and mon - w["m"] == 216 and ann - w["a"] == 60
Q(T, "Paragraph data", B, "How many men were on the quarterly plan?",
  "165", ["135", "216", "60"],
  "Men = members on the plan − women on the plan",
  "Quarterly members = 300, of whom 45% = 135 are women, so 165 are men.",
  ["Women = 135", "Men = 300 − 135 = 165"],
  why="135 is the women on the quarterly plan; 216 is the men on the monthly plan; 60 is the men on the annual plan.",
  secs=35, stim=sid)

pc = F(12 * 1500 - 14400, 14400) * 100
assert pc == 25 and F(3600, 18000) * 100 == 20 and near(F(16000 - 14400, 14400) * 100, 11.11, 0.01)
Q(T, "Paragraph data", I,
  "Over a full year, by what percentage does staying on the monthly plan cost more than buying the annual plan?",
  "25%", ["20%", "11.11%", "125%"],
  "Convert both plans to a yearly cost; 'more than the annual plan' uses the annual cost as the base",
  "Monthly plan for a year = 12 × 1,500 = ₹18,000. Annual plan = ₹14,400. The extra ₹3,600 is 3,600 ÷ 14,400 = 25%.",
  ["12 × 1,500 = 18,000", "18,000 − 14,400 = 3,600", "3,600 ÷ 14,400 = 25%"],
  why="20% divides by the monthly plan's 18,000; 11.11% compares the quarterly plan (16,000) with the annual plan; "
      "125% is the monthly plan's yearly cost as a percentage of the annual plan's.", secs=50, stim=sid)

year = mon * 18000 + qtr * 16000 + ann * 14400
assert year == 13872000 and mon * 18000 + qtr * 4000 + ann * 14400 == 10272000 and 840 * 14400 == 12096000
assert mon * 1500 + qtr * 16000 + ann * 14400 == 7932000
Q(T, "Paragraph data", I,
  "If every member stays on the same plan for a full year, what total fee will the centre collect in that year?",
  "₹1,38,72,000", ["₹1,02,72,000", "₹1,20,96,000", "₹79,32,000"],
  "Convert each plan's fee to a yearly amount before multiplying by the number of members",
  "Monthly: 360 × 18,000 = ₹64,80,000. Quarterly: 300 × 16,000 = ₹48,00,000. Annual: 180 × 14,400 = ₹25,92,000. "
  "Total = ₹1,38,72,000.",
  ["Monthly plan: 12 × 1,500 = 18,000 a year ⇒ 64,80,000", "Quarterly: 4 × 4,000 = 16,000 ⇒ 48,00,000",
   "Annual: 14,400 ⇒ 25,92,000", "Total = 1,38,72,000"],
  why="₹1,02,72,000 counts only one quarter's fee for quarterly members; ₹1,20,96,000 charges everyone the annual "
      "fee; ₹79,32,000 counts only one month's fee for monthly members.", secs=70, stim=sid)

mon2, ann2, qtr2 = mon * F(3, 4), ann + mon * F(1, 4), qtr + 60
pc = F(ann2, mon2 + ann2 + qtr2) * 100
assert (mon2, ann2, qtr2) == (270, 270, 360) and pc == 30
assert near(F(270, 840) * 100, 32.14, 0.01) and near(F(180, 840) * 100, 21.43, 0.01) and F(180, 900) * 100 == 20
Q(T, "Paragraph data", A,
  "In November, one-fourth of the monthly-plan members switch to the annual plan, and 60 new members join on the "
  "quarterly plan; no one leaves. What percentage of all members are then on the annual plan?",
  "30%", ["32.14%", "21.43%", "20%"],
  "Update each plan's count, then divide by the new total membership",
  "A quarter of the 360 monthly members (90) move to the annual plan, which now has 270. With 60 new quarterly "
  "members, the total is 900. Annual share = 270 ÷ 900 = 30%.",
  ["Switchers = 90", "Annual = 180 + 90 = 270", "Total = 840 + 60 = 900", "270 ÷ 900 = 30%"],
  why="32.14% divides by the old total of 840; 21.43% is the October share (180 ÷ 840); 20% forgets the 90 "
      "switchers (180 ÷ 900).", secs=80, stim=sid)

sid = stimulus("caselet", "A bakery's baking, sales and costs on one Saturday",
               "On a Saturday a bakery baked 1,500 items: loaves of bread, cakes and packets of cookies in the ratio "
               "6 : 2 : 7. It sold 90% of the loaves, 85% of the cakes and four-fifths of the cookie packets that day. "
               "Unsold loaves and cookie packets were given away free to a shelter; all the unsold cakes were sold "
               "the next morning at half price. Selling prices: loaf ₹40, cake ₹300, cookie packet ₹52.50. Cost of "
               "making: loaf ₹25, cake ₹175, cookie packet ₹30.")
br, ck, co = [1500 * F(r, 15) for r in (6, 2, 7)]
sold = {"br": br * F(9, 10), "ck": ck * F(85, 100), "co": co * F(4, 5)}
assert (br, ck, co) == (600, 200, 700) and sold == {"br": 540, "ck": 170, "co": 560}
Q(T, "Paragraph data", B, "How many packets of cookies did the bakery make that Saturday?",
  "700", ["600", "560", "1,050"],
  "Split 1,500 in the ratio 6 : 2 : 7 (15 parts)",
  "One part = 1,500 ÷ 15 = 100, so cookie packets = 7 × 100 = 700.",
  ["6 + 2 + 7 = 15 parts", "1 part = 100", "Cookies = 700"],
  why="600 is the number of loaves; 560 is the cookie packets sold; 1,050 takes 7/10 of 1,500.", secs=35, stim=sid)

uns = (br - sold["br"]) + (ck - sold["ck"]) + (co - sold["co"])
assert uns == 230 and 1500 - 230 == 1270
Q(T, "Paragraph data", B, "How many items in all were left unsold at the end of Saturday?",
  "230", ["90", "1,270", "200"],
  "Unsold = made − sold, for each item",
  "Unsold loaves = 60, cakes = 30 and cookie packets = 140. Total = 230.",
  ["Loaves: 600 − 540 = 60", "Cakes: 200 − 170 = 30", "Cookies: 700 − 560 = 140", "Total = 230"],
  why="90 counts only loaves and cakes; 1,270 is the number sold; 200 counts loaves and cookies but not cakes.",
  secs=40, stim=sid)

rv = sold["ck"] * 300
assert rv == 51000 and 200 * 300 == 60000 and sold["ck"] * 175 == 29750 and rv + 30 * 150 == 55500
Q(T, "Paragraph data", I, "What was the bakery's revenue from cakes on the Saturday itself?",
  "₹51,000", ["₹60,000", "₹29,750", "₹55,500"],
  "Revenue = number sold × selling price, counting only that day's sales",
  "Cakes sold on Saturday = 85% of 200 = 170. Revenue = 170 × 300 = ₹51,000.",
  ["170 cakes sold", "170 × 300 = 51,000"],
  why="₹60,000 counts all 200 cakes; ₹29,750 uses the cost of making; ₹55,500 adds the next morning's half-price "
      "sales.", secs=45, stim=sid)

prof = 55500 - ck * 175
assert prof == 20500 and 51000 - 35000 == 16000 and 55500 - 29750 == 25750 and 60000 - 35000 == 25000
Q(T, "Paragraph data", A,
  "What was the bakery's total profit on the Saturday's cakes, including the next morning's half-price sales?",
  "₹20,500", ["₹16,000", "₹25,750", "₹25,000"],
  "Profit = all revenue from the cakes − cost of making all 200 cakes",
  "Revenue: 170 × 300 = ₹51,000 on Saturday plus 30 × 150 = ₹4,500 next morning = ₹55,500. Cost = 200 × 175 = "
  "₹35,000. Profit = ₹20,500.",
  ["Saturday: 51,000", "Next morning: 30 × 150 = 4,500", "Cost: 200 × 175 = 35,000", "Profit = 20,500"],
  why="₹16,000 leaves out the half-price sales; ₹25,750 charges the cost of the 170 cakes sold on Saturday only; "
      "₹25,000 sells all 200 at full price.", secs=75, stim=sid)

rev = sold["br"] * 40 + 55500 + sold["co"] * F(105, 2)
cost = br * 25 + ck * 175 + co * 30
pc = (rev - cost) / cost * 100
assert (rev, cost, pc) == (106500, 71000, 50)
assert r2(F(102000 - 71000, 71000) * 100) == F(4366, 100) and r2(F(35500, 106500) * 100) == F(3333, 100)
sold_cost = sold["br"] * 25 + sold["ck"] * 175 + sold["co"] * 30
assert sold_cost == 60050 and r2((rev - sold_cost) / sold_cost * 100) == F(7735, 100)
Q(T, "Paragraph data", A,
  "Taking all the items baked that Saturday (including those given away, and counting the next morning's cake "
  "sales), what was the bakery's overall profit percentage (correct to two decimal places)?",
  "50%", ["43.66%", "33.33%", "77.35%"],
  "Profit % = (total revenue − total cost of everything made) ÷ total cost × 100",
  "Revenue: loaves 540 × 40 = ₹21,600; cakes ₹55,500; cookies 560 × 52.50 = ₹29,400; total ₹1,06,500. Cost: "
  "600 × 25 + 200 × 175 + 700 × 30 = 15,000 + 35,000 + 21,000 = ₹71,000. Profit = ₹35,500 = 50% of cost.",
  ["Revenue = 21,600 + 55,500 + 29,400 = 1,06,500", "Cost = 15,000 + 35,000 + 21,000 = 71,000",
   "Profit = 35,500", "35,500 ÷ 71,000 = 50%"],
  why="43.66% leaves out the next morning's cake sales; 33.33% divides the profit by revenue instead of cost; 77.35% "
      "counts the cost of only the items sold on Saturday.", secs=100, stim=sid)

# ================================================================ Missing DI (B2 I3 A2): sets of 4 and 3
T = "Missing DI"
dash = "—"
SALES = {"Asha": (40, 46, None, None), "Bilal": (None, 36, 90, None), "Chitra": (50, None, 112, None),
         "Deepak": (45, None, None, 45000), "Eshan": (None, 63, 105, None)}
sid = stimulus("data_table", "Sales targets, achievements and incentives of five executives (some values missing)",
               "The table shows, for five sales executives of a bank's home-loan desk, the quarterly target and the "
               "amount achieved (both in ₹ lakh), the achievement as a percentage of the target, and the incentive "
               "earned. The incentive is 5% of the amount achieved above the target (nil if the target is not met). "
               "Some values are missing (—); work them out from the others.\n\n" +
               md_table(["Executive", "Target (₹ lakh)", "Achieved (₹ lakh)", "Achievement (%)", "Incentive (₹)"],
                        [[k, *[dash if c is None else ind(c) for c in v]] for k, v in SALES.items()]),
               {"columns": ["executive", "target_lakh", "achieved_lakh", "achievement_pct", "incentive_rs"],
                "rows": [[k, *v] for k, v in SALES.items()]})
tgt = {"Asha": F(40), "Bilal": F(36) / F(90, 100), "Chitra": F(50), "Deepak": F(45), "Eshan": F(63) / F(105, 100)}
ach = {"Asha": F(46), "Bilal": F(36), "Chitra": F(50) * F(112, 100), "Deepak": F(45) + F(45000, 5 * 1000),
       "Eshan": F(63)}
inc = {k: max(F(0), (ach[k] - tgt[k]) * 100000 * F(5, 100)) for k in SALES}
assert tgt["Bilal"] == 40 and tgt["Eshan"] == 60 and ach["Chitra"] == 56 and ach["Deepak"] == 54
assert inc == {"Asha": 30000, "Bilal": 0, "Chitra": 30000, "Deepak": 45000, "Eshan": 15000}
assert F(46, 40) * 100 == 115 and near(F(40, 46) * 100, 86.96, 0.01)
Q(T, "Table with missing values", B, "What was Asha's achievement percentage?",
  "115%", ["86.96%", "15%", "6%"],
  "Achievement % = achieved ÷ target × 100",
  "Asha achieved ₹46 lakh against a target of ₹40 lakh: 46 ÷ 40 = 115%.",
  ["46 ÷ 40 = 1.15", "= 115%"],
  why="86.96% divides target by achievement; 15% is only the excess over 100%; 6% reads the ₹6 lakh excess as a "
      "percentage.", secs=30, stim=sid)

Q(T, "Table with missing values", I, "What was Bilal's target?",
  "₹40 lakh", ["₹32.4 lakh", "₹39.6 lakh", "₹45 lakh"],
  "Target = achieved ÷ achievement %",
  "Bilal achieved ₹36 lakh, which was 90% of his target, so the target = 36 ÷ 0.9 = ₹40 lakh. (He earns no incentive.)",
  ["36 = 0.9 × target", "Target = 36 ÷ 0.9 = 40"],
  why="₹32.4 lakh takes 90% of 36; ₹39.6 lakh adds 10% to 36; ₹45 lakh is Deepak's target.", secs=45, stim=sid)
assert 36 * F(9, 10) == F(324, 10) and 36 * F(11, 10) == F(396, 10)

assert F(45) * F(105, 100) == F(4725, 100)
Q(T, "Table with missing values", I, "What amount did Deepak achieve?",
  "₹54 lakh", ["₹9 lakh", "₹47.25 lakh", "₹90 lakh"],
  "Work back from the incentive: excess = incentive ÷ 5%",
  "An incentive of ₹45,000 is 5% of the excess, so the excess = 45,000 ÷ 0.05 = ₹9,00,000 = ₹9 lakh. Achieved = "
  "45 + 9 = ₹54 lakh (120% of target).",
  ["Excess = 45,000 ÷ 0.05 = 9,00,000 = 9 lakh", "Achieved = 45 + 9 = 54 lakh"],
  why="₹9 lakh is only the excess; ₹47.25 lakh adds 5% to the target; ₹90 lakh reads ₹45,000 as ₹45 lakh of excess.",
  secs=55, stim=sid)

total_inc = sum(inc.values())
assert total_inc == 120000 and total_inc - inc["Eshan"] == 105000 and total_inc - inc["Chitra"] == 90000
assert total_inc - F(4, 1) * 100000 * F(5, 100) == 100000
Q(T, "Table with missing values", A, "What was the total incentive earned by the five executives?",
  "₹1,20,000", ["₹1,05,000", "₹90,000", "₹1,00,000"],
  "Fill every missing cell first; an executive below target earns nil, not a negative incentive",
  "Asha: 5% of 6 lakh = ₹30,000. Bilal: below target, nil. Chitra: achieved 112% of 50 = 56 lakh, excess 6 lakh ⇒ "
  "₹30,000. Deepak: ₹45,000. Eshan: target = 63 ÷ 1.05 = 60 lakh, excess 3 lakh ⇒ ₹15,000. Total = ₹1,20,000.",
  ["Asha 30,000", "Bilal 0", "Chitra: 56 − 50 = 6 lakh ⇒ 30,000", "Deepak 45,000",
   "Eshan: target 60, excess 3 lakh ⇒ 15,000", "Total = 1,20,000"],
  why="₹1,05,000 leaves out Eshan; ₹90,000 leaves out Chitra; ₹1,00,000 deducts 5% of Bilal's ₹4 lakh shortfall as "
      "a negative incentive.", secs=100, stim=sid)

BAT = {"Morning": (120, None, 100, None, 64), "Afternoon": (None, 15, None, 54, 72),
       "Evening": (150, 30, None, None, 55), "Weekend": (80, None, None, 45, 75)}
sid = stimulus("data_table", "Four batches of a bank-exam coaching course (some values missing)",
               "The table shows, for four batches of a bank-exam coaching course, the number of students who "
               "enrolled, the number who dropped out, the number who completed the course (enrolled − dropped out), "
               "the number who passed the final test and the pass percentage (passed as a percentage of those who "
               "completed). Some values are missing (—).\n\n" +
               md_table(["Batch", "Enrolled", "Dropped out", "Completed", "Passed", "Pass %"],
                        [[k, *[dash if c is None else c for c in v]] for k, v in BAT.items()]),
               {"columns": ["batch", "enrolled", "dropped", "completed", "passed", "pass_pct"],
                "rows": [[k, *v] for k, v in BAT.items()]})
comp = {"Morning": F(100), "Afternoon": F(54) / F(72, 100), "Evening": F(150 - 30), "Weekend": F(45) / F(75, 100)}
enr = {"Morning": 120, "Afternoon": comp["Afternoon"] + 15, "Evening": 150, "Weekend": 80}
drop = {k: enr[k] - comp[k] for k in BAT}
pas = {"Morning": 100 * F(64, 100), "Afternoon": F(54), "Evening": comp["Evening"] * F(55, 100), "Weekend": F(45)}
assert comp == {"Morning": 100, "Afternoon": 75, "Evening": 120, "Weekend": 60}
assert enr["Afternoon"] == 90 and drop == {"Morning": 20, "Afternoon": 15, "Evening": 30, "Weekend": 20}
assert pas == {"Morning": 64, "Afternoon": 54, "Evening": 66, "Weekend": 45}
Q(T, "Table with missing values", B, "How many students dropped out of the Morning batch?",
  "20", ["56", "36", "30"],
  "Dropped out = enrolled − completed",
  "Morning: 120 enrolled and 100 completed, so 20 dropped out.",
  ["120 − 100 = 20"],
  why="56 subtracts the passed students (64) from the enrolled; 36 is the number who completed but failed; 30 is "
      "the Evening batch's dropouts.", secs=30, stim=sid)

Q(T, "Table with missing values", I, "How many students enrolled in the Afternoon batch?",
  "90", ["75", "69", "60"],
  "Completed = passed ÷ pass %; enrolled = completed + dropped out",
  "54 passed, which is 72% of those who completed, so 54 ÷ 0.72 = 75 completed. Enrolled = 75 + 15 = 90.",
  ["Completed = 54 ÷ 0.72 = 75", "Enrolled = 75 + 15 = 90"],
  why="75 is the number who completed; 69 adds the dropouts to the passed students; 60 subtracts the dropouts "
      "instead of adding them.", secs=50, stim=sid)

tot_e, tot_c, tot_p = sum(enr.values()), sum(comp.values()), sum(pas.values())
assert (tot_e, tot_c, tot_p) == (440, 355, 229)
assert r2(F(tot_p, tot_e) * 100) == F(5205, 100) and r2(F(tot_p, tot_c) * 100) == F(6451, 100)
assert F(64 + 72 + 55 + 75, 4) == F(665, 10) and r2(F(tot_c, tot_e) * 100) == F(8068, 100)
Q(T, "Table with missing values", A,
  "Taking the four batches together, what percentage of all the students who enrolled passed the final test "
  "(correct to two decimal places)?",
  "52.05%", ["64.51%", "66.5%", "80.68%"],
  "Fill all the missing cells, then total passed ÷ total enrolled",
  "Enrolled: 120 + 90 + 150 + 80 = 440. Passed: Morning 64% of 100 = 64, Afternoon 54, Evening 55% of 120 = 66, "
  "Weekend 45 — total 229. 229 ÷ 440 = 52.045…% ≈ 52.05%.",
  ["Enrolled total = 440", "Passed: 64 + 54 + 66 + 45 = 229", "229 ÷ 440 × 100 = 52.05%"],
  why="64.51% divides by those who completed (355) instead of those who enrolled; 66.5% averages the four pass "
      "percentages; 80.68% is the completion rate (355 ÷ 440).", secs=100, stim=sid)

# ================================================================ Quantity Comparison (B1 I2 A1)
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


q1v, q2v = F(3, 8) * 256, F(45, 100) * 200
assert (q1v, q2v) == (96, 90)
qc("Quantity I vs II", B, "3/8 of 256", "0.45 × 200", [q1v], [q2v], ">", ["<", "<="],
   "Evaluate each quantity exactly",
   "Quantity I = 256 ÷ 8 × 3 = 96. Quantity II = 0.45 × 200 = 90. So Quantity I > Quantity II.",
   ["I: 256 × 3/8 = 96", "II: 0.45 × 200 = 90", "96 > 90"],
   why="'Quantity I < Quantity II' compares 3/8 = 0.375 with 0.45 and ignores the different numbers they multiply.",
   secs=30)

q1v, q2v = F(4 * 14), 2 * F(22, 7) * 9
assert q1v == 56 and q2v == F(396, 7) and q1v < q2v
qc("Arithmetic-based comparison", I, "Perimeter (cm) of a square of area 196 cm²",
   "Circumference (cm) of a circle of radius 9 cm (take π = 22/7)", [q1v], [q2v], "<", [">", ">="],
   "Square: side = √area, perimeter = 4 × side; circle: circumference = 2πr",
   "Quantity I: side = √196 = 14 cm, perimeter = 56 cm. Quantity II: 2 × 22/7 × 9 = 396/7 ≈ 56.57 cm. So Quantity I < "
   "Quantity II.",
   ["I: √196 = 14 ⇒ 4 × 14 = 56", "II: 2 × 22/7 × 9 = 56.57", "56 < 56.57"],
   why="'Quantity I > Quantity II' comes from using π = 3 (2 × 3 × 9 = 54); '≥' would need the two to be equal.",
   secs=55)

q1v = (F(30, 2) - F(18, 2)) / 2
assert q1v == 3
qc("Arithmetic-based comparison", I,
   "Speed of the stream (km/h) if a boat goes 30 km downstream in 2 hours and 18 km upstream in 2 hours",
   "2.5", [q1v], [F(5, 2)], ">", ["<", "<="],
   "Stream speed = (downstream speed − upstream speed) ÷ 2",
   "Downstream = 15 km/h, upstream = 9 km/h, so the stream = (15 − 9) ÷ 2 = 3 km/h. 3 > 2.5, so Quantity I > "
   "Quantity II.",
   ["Downstream = 30 ÷ 2 = 15", "Upstream = 18 ÷ 2 = 9", "Stream = 3 km/h", "3 > 2.5"],
   why="'Quantity I < Quantity II' halves the difference twice (6 ÷ 4 = 1.5); 'Quantity I ≤ Quantity II' would "
       "need the stream to be no faster than 2.5 km/h.", secs=55)

coins = list(itertools.product("HT", repeat=3))
q1v = F(sum(1 for c in coins if "H" in c), 8)
q2v = F(sum(1 for n in range(1, 51) if n % 8), 50)
assert q1v == F(7, 8) and q2v == F(44, 50) and q1v < q2v
qc("Quantity I vs II", A,
   "Probability of getting at least one head when three fair coins are tossed",
   "Probability that a number chosen at random from 1 to 50 is not a multiple of 8", [q1v], [q2v], "<", [">", ">="],
   "Use complements: P(at least one head) = 1 − P(no head); count multiples of 8 up to 50",
   "Quantity I = 1 − 1/8 = 7/8 = 0.875. Quantity II: multiples of 8 up to 50 are 8, 16, 24, 32, 40, 48 (6 numbers), "
   "so P = 44/50 = 0.88. So Quantity I < Quantity II.",
   ["I: 1 − (1/2)³ = 7/8 = 0.875", "II: 6 multiples of 8 ⇒ 44/50 = 0.88", "0.875 < 0.88"],
   why="'Quantity I > Quantity II' counts 7 multiples of 8 (43/50 = 0.86); 'Quantity I ≥ Quantity II' fails for the "
       "same reason, since 0.875 < 0.88.", secs=80, by=BRUTE)

# ================================================================ Data Sufficiency (Quant) (B2 I1 A1)
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


cands = [F(k, 2) for k in range(1, 401)]
verdict = ds2_verdict(cands, lambda s: s * F(7, 2) == 210, lambda s: s == F(6, 5) * F(150, 3), lambda s: s)
assert verdict == "either"
Q(T, "Two-statement", B,
  f"{DS_PRE}\nQuestion: What is the speed of the car?\n"
  "I. The car covers 210 km in 3 hours 30 minutes.\n"
  "II. The car's speed is 20% more than that of a bus that covers 150 km in 3 hours.",
  DS2["either"], [DS2["I"], DS2["II"], DS2["both"]],
  "A statement is sufficient on its own if it fixes the answer without the other",
  "I: 210 ÷ 3.5 = 60 km/h — sufficient. II: the bus runs at 150 ÷ 3 = 50 km/h, so the car runs at 1.2 × 50 = "
  "60 km/h — sufficient. Either statement alone answers the question.",
  ["I: 210 ÷ 3.5 = 60 km/h", "II: bus = 50 km/h ⇒ car = 60 km/h", "Each alone is sufficient"],
  why="'I alone' or 'II alone' overlooks that the other statement also gives the speed; 'both together' assumes "
      "the two must be combined.", secs=40, by=BRUTE)

cands = [(F(cp), F(pc)) for cp in range(100, 3001, 50) for pc in range(1, 61)]
verdict = ds2_verdict(cands, lambda c: c[1] == 20, lambda c: c[0] * c[1] / 100 == 150, lambda c: c[0])
assert verdict == "both"
Q(T, "Two-statement", B,
  f"{DS_PRE}\nQuestion: What is the cost price of the bag?\n"
  "I. The bag was sold at a profit of 20%.\n"
  "II. The profit on the bag was ₹150.",
  DS2["both"], [DS2["I"], DS2["II"], DS2["neither"]],
  "Profit % alone or profit alone does not fix the cost; together profit = CP × profit %",
  "I gives only a percentage, and II only a rupee amount; neither fixes the cost price alone. Together: 20% of the "
  "cost price = ₹150, so the cost price = ₹750.",
  ["I alone: any CP with 20% profit", "II alone: ₹150 profit on any CP", "Together: 0.2 × CP = 150 ⇒ CP = 750"],
  why="'I alone' and 'II alone' each leave the cost price open; 'not sufficient even together' misses that the "
      "two combine into one equation.", secs=40, by=BRUTE)

cands = [(F(L), F(v)) for L in range(50, 601, 10) for v in range(5, 41)]
conds = [lambda c: c[0] / c[1] == 12, lambda c: (c[0] + 300) / c[1] == 27, lambda c: c[1] == 20]
m = suff_map(cands, conds, lambda c: c[0])
assert m == {(0,): False, (1,): False, (2,): False, (0, 1): True, (0, 2): True, (1, 2): True, (0, 1, 2): True}
Q(T, "Three-statement", I,
  f"{DS3_PRE}\nQuestion: What is the length of the train?\n"
  "I. The train crosses a signal pole in 12 seconds.\n"
  "II. The train crosses a 300 m long platform in 27 seconds.\n"
  "III. The speed of the train is 72 km/h.",
  "Any two of the three statements together are sufficient",
  ["Only I and II together are sufficient", "Statement III alone is sufficient",
   "All three statements together are necessary"],
  "Check each pair; each statement alone links length and speed but cannot fix both",
  "I + II: L/12 = (L + 300)/27 ⇒ 27L = 12L + 3,600 ⇒ L = 240 m. I + III: 72 km/h = 20 m/s, L = 20 × 12 = 240 m. "
  "II + III: L + 300 = 20 × 27 = 540 ⇒ L = 240 m. No single statement fixes L.",
  ["I + II: 15L = 3,600 ⇒ L = 240", "I + III: 20 × 12 = 240", "II + III: 540 − 300 = 240",
   "Any one alone: two unknowns"],
  why="'Only I and II' misses the other two working pairs; 'III alone' gives the speed but not the length; 'all "
      "three' is more than needed.", secs=75, by=BRUTE)

TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)]
cands = []
for p, q, r in TRIPLES:
    for n in range(1, 81):
        k = F(n, 10)
        cands += [(p * k, q * k, r * k), (q * k, p * k, r * k)]
verdict = ds2_verdict(cands, lambda c: c[2] == 13, lambda c: sum(c) == 30, lambda c: c[0] * c[1] / 2)
assert verdict == "both"
for c, P in [(13, 30)]:  # algebra: a + b = P − c and a² + b² = c² fix ab, hence the area
    assert F((P - c) ** 2 - c ** 2, 4) == 30
Q(T, "Two-statement", A,
  f"{DS_PRE}\nQuestion: What is the area of the right-angled triangle?\n"
  "I. Its hypotenuse is 13 cm.\n"
  "II. Its perimeter is 30 cm.",
  DS2["both"], [DS2["I"], DS2["either"], DS2["neither"]],
  "With the hypotenuse c and perimeter P known, a + b = P − c and a² + b² = c², so ab (and the area) is fixed",
  "I alone: many right triangles have hypotenuse 13 (5-12-13 has area 30; 7.8-10.4-13 has area 40.56). II alone: "
  "5-12-13 and 7.5-10-12.5 both have perimeter 30, with areas 30 and 37.5. Together: a + b = 17 and a² + b² = 169, so "
  "2ab = 289 − 169 = 120 and the area = ab/2 = 30 cm².",
  ["I alone: 5-12-13 vs 7.8-10.4-13 ⇒ different areas", "II alone: 5-12-13 vs 7.5-10-12.5 ⇒ different areas",
   "Together: (a + b)² − (a² + b²) = 2ab ⇒ 289 − 169 = 120", "Area = ab/2 = 30 cm²"],
  why="'I alone' assumes the triangle must be 5-12-13; 'either' assumes the same for the perimeter; 'not sufficient' "
      "misses that a + b and a² + b² together fix ab.", secs=100, by=BRUTE)

# ================================================================ checks and output
assert len(QUESTIONS) == TOTAL, len(QUESTIONS)
assert len(STIMULI) == 12

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_004_plan.json").read_text(encoding="utf-8"))
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
    "batch_id": "BATCH_004",
    "created_at": TODAY,
    "notes": "BATCH_004, Quantitative Aptitude part: 200 original questions (60 Basic, 80 Intermediate, 60 Advanced) "
             "with 12 shared DI stimuli on new data sets. Every answer was recomputed by tools/batch_004/quant.py "
             "before writing; questions tagged ai:independent-check were also re-solved from the stem, options and "
             "data set alone by a separate solver. Pending human review.",
    "stimuli": STIMULI,
    "questions": QUESTIONS,
}
out = ROOT / "batches" / "parts" / "BATCH_004_QUANT.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(QUESTIONS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(keys.items()))}, "
      f"independent-check {len(INDEPENDENT)})")
