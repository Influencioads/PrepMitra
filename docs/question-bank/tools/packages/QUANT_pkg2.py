"""QUANT package 2: Quantitative Aptitude topics Mixture and Alligation, Time and Work, Pipes and Cisterns, Speed,
Time and Distance, Boats and Streams, Problems on Trains, Mensuration, Probability, Permutation and Combination, all
DI types (Tabular, Bar Graph, Pie Chart, Line Graph, Caselet, Missing), Quantity Comparison and Data Sufficiency
(Quant) for BATCH_009 and BATCH_010.

Writes batches/parts/frag/BATCH_009_QUANT_pkg2.json (99 questions) and batches/parts/frag/BATCH_010_QUANT_pkg2.json
(101 questions), as laid down in batches/plans/packages/QUANT_pkg2.json.

Every answer is recomputed here before anything is written: arithmetic with exact fractions, probabilities and
arrangements counted by brute-force enumeration, data-sufficiency verdicts found by enumerating candidate cases,
DI answers recomputed from the data dictionaries that also produce the stimulus tables (no ties where a maximum or
minimum is asked). Quantity comparison uses the relation guards of tools/batch_008/quant.py (a strict answer never
beside its weaker form, no wrong relation that also holds, no exactly equal quantities, every pair at least 2% apart).
Per-batch quotas, ID ranges, subtopics, stimulus starts, set sizes (3 to 6) and balanced keys (seed 20261105 + 92)
are asserted. If any assertion fails, nothing is written.

All earlier stems of these topics (BATCH_000 to BATCH_008) and all 89 earlier Quant DI stimulus titles were read
first; DI themes, contexts and number templates here are new.

    python tools/packages/QUANT_pkg2.py          (run from docs/question-bank)
    python tools/packages/QUANT_pkg2.py --dump <file> [--ids a,b,...]   (blind copy: no key, no solution)
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
PKG = json.loads((ROOT / "batches" / "plans" / "packages" / "QUANT_pkg2.json").read_text(encoding="utf-8"))
RECOMPUTE = ["script:recompute", "ai:self-recheck"]
BRUTE = ["script:recompute", "script:brute-force-unique", "ai:self-recheck"]

# Balanced answer keys per fragment, order fixed by the seed: 99 -> 25/25/25/24, 101 -> 26/25/25/25.
_rng = random.Random(20261105 + 92)
KEYS = {}
for _bt in ("009", "010"):
    _n = PKG["batches"][_bt]["count"]
    _k = list("ABCD" * 26)[:_n]
    _rng.shuffle(_k)
    KEYS[_bt] = _k

# Questions re-answered blind by a separate fresh solver (stem, options and data set only, no key, no solution) whose
# answer matched the key. Only these carry ai:independent-check. Every fourth question of the package (50 questions:
# BANK_QUANT_001703, _001707, ..., _001799 and BANK_QUANT_001901, _001905, ..., _001997) was given to one separate,
# fresh solver agent as a blind dump (--dump --ids); all 50 answers matched the key. No question was changed after
# its blind check, except BANK_QUANT_001989, whose Quantity II was restated in hours afterwards (units now match), so
# its ai:independent-check tag was dropped.
INDEPENDENT = set(([f"BANK_QUANT_{n:06d}" for n in range(1703, 1802)] +
                   [f"BANK_QUANT_{n:06d}" for n in range(1900, 2001)])[::4]) - {"BANK_QUANT_001989"}

QS = {"009": [], "010": []}
STIMS = {"009": [], "010": []}
_set_pos = {}
BT = "009"  # batch currently being written


def first_num(s):
    return int(s.rsplit("_", 1)[1])


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


def r2(x) -> F:
    """Round half up to two decimals (for stems that fix two-decimal precision)."""
    return F(math.floor(F(x) * 100 + F(1, 2)), 100)


def pct2(x) -> str:
    """A fraction shown as a percentage correct to two decimal places, e.g. 0.24475 -> '24.48%'."""
    return f"{float(r2(F(x) * 100)):.2f}%"


def frac(x) -> str:
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


# ---------------------------------------------------------------- record builder
def Q(topic, sub, diff, text, ans, wrong, concept, expl, steps, short=None, why=None, secs=None, stim=None,
      by=None):
    """Places the correct option at the next balanced key of the current batch, checks the options, appends."""
    assert len(wrong) == 3, wrong
    assert diff in (B, I, A)
    assert why, f"why_others_wrong missing: {text[:60]}"
    lst = QS[BT]
    n = len(lst)
    key = KEYS[BT][n]
    opts = list(wrong)
    opts.insert(LETTERS.index(key), ans)
    assert len({normalize(o) for o in opts}) == 4, f"options not distinct: {opts}"
    qid = f"BANK_QUANT_{first_num(PKG['batches'][BT]['question_ids'][0]) + n:06d}"
    rec = {
        "question_id": qid,
        "exam_mappings": default_mappings(SUBJECT, diff),
        "subject": SUBJECT, "topic": topic, "subtopic": sub, "difficulty": diff,
        "question_type": "MCQ", "language": "en",
    }
    if stim:
        assert stim.startswith(f"STIM_QUANT_{BT}"), (stim, BT)
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
    lst.append(rec)


def stimulus(kind, title, content, chart_data=None):
    sid = f"STIM_QUANT_{first_num(PKG['batches'][BT]['stimulus_id_start']) + len(STIMS[BT]):06d}"
    s = {"stimulus_id": sid, "type": kind, "title": title, "content": content}
    if chart_data:
        s["chart_data"] = chart_data
    STIMS[BT].append(s)
    return sid


def md_table(header, rows, align=None):
    align = align or ["---"] + ["---:"] * (len(header) - 1)
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join(align) + "|"]
    lines += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(lines)


def unique_max(d):
    """The key of the largest value, asserting there is no tie for first place."""
    srt = sorted(d.values(), reverse=True)
    assert srt[0] != srt[1], ("tie for maximum", d)
    return max(d, key=d.get)


def unique_min(d):
    srt = sorted(d.values())
    assert srt[0] != srt[1], ("tie for minimum", d)
    return min(d, key=d.get)


def prob(space, event):
    """Exact probability by enumeration of an equally likely sample space."""
    space = list(space)
    return F(sum(1 for w in space if event(w)), len(space))


DICE2 = list(itertools.product(range(1, 7), repeat=2))
DECK = [(r, s) for s in "SHDC" for r in range(1, 14)]  # 1 = ace, 11 J, 12 Q, 13 K; S, C black; H, D red

# ---------------------------------------------------------------- relation guards (Quantity Comparison)
_TESTS = {">": lambda x, y: x > y, "<": lambda x, y: x < y, ">=": lambda x, y: x >= y, "<=": lambda x, y: x <= y}
QREL = {">": "Quantity I > Quantity II", ">=": "Quantity I ≥ Quantity II", "<": "Quantity I < Quantity II",
        "<=": "Quantity I ≤ Quantity II", "cbe": "Quantity I = Quantity II or the relationship cannot be established"}


def relation(xs, ys):
    pairs = [(x, y) for x in xs for y in ys]
    if all(x == y for x, y in pairs):
        return "cbe"
    for sym in (">", "<", ">=", "<="):
        if all(_TESTS[sym](x, y) for x, y in pairs):
            return sym
    return "cbe"


def no_true_distractor(xs, ys, syms):
    """No wrong relation may hold for every pair (e.g. x ≥ y when the answer is x > y)."""
    for s_ in syms:
        assert not all(_TESTS[s_](x, y) for x in xs for y in ys), f"distractor {s_} is also true"


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
        # a strict answer never sits beside its weaker form
        weaker = {">": ">=", "<": "<="}.get(expect)
        assert weaker not in wrong_syms, (expect, wrong_syms)
        wrong = [QREL[wrong_syms[0]], QREL["cbe"], QREL[wrong_syms[1]]]
        no_true_distractor(vals1, vals2, wrong_syms)
    Q("Quantity Comparison", sub, diff,
      f"Compare the two quantities and choose the correct option.\nQuantity I: {q1}\nQuantity II: {q2}",
      QREL[expect], wrong, concept, expl, steps, short, why, secs, by=by)


# ---------------------------------------------------------------- data sufficiency
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


# ######################################################################## BATCH_009
BT = "009"

# ================================================================ Mixture and Alligation (B1 I1 A2)
T = "Mixture and Alligation"
tot, avg = 50000, F(5200, 50000) * 100
x12 = tot * (avg - 8) / (12 - 8)
assert avg == F(52, 5) and x12 == 30000 and tot - x12 == 20000
Q(T, "Alligation rule", B, "Meena lends ₹50,000 in two parts, one at 8% and the other at 12% simple interest per "
  "annum. Her total interest for one year is ₹5,200. How much did she lend at 12%?",
  "₹30,000", ["₹20,000", "₹25,000", "₹26,000"],
  "The overall rate is a weighted average of the two rates, so alligation gives the ratio of the two parts",
  "Overall rate = 5,200 ÷ 50,000 × 100 = 10.4%. By alligation, (8% part) : (12% part) = (12 − 10.4) : (10.4 − 8) = "
  "1.6 : 2.4 = 2 : 3. The 12% part is 3/5 of ₹50,000 = ₹30,000.",
  ["Average rate = 10.4%", "8% : 12% = 1.6 : 2.4 = 2 : 3", "12% part = 3/5 × 50,000 = ₹30,000"],
  short="Check: 20,000 × 8% + 30,000 × 12% = 1,600 + 3,600 = 5,200.",
  why="₹20,000 is the 8% part (the ratio read the wrong way round); ₹25,000 assumes an equal split; ₹26,000 comes "
      "from taking the interest ₹5,200 as 20% of the 12% part.", secs=45)

milk0, water0 = F(40) * F(85, 100), F(40) * F(15, 100)
k = F(32, 40)
m1, w1 = milk0 * k, water0 * k
total_needed = m1 / F(68, 100)
add = total_needed - (m1 + w1)
assert (m1, w1) == (F(136, 5), F(24, 5)) and total_needed == 40 and add == 8
assert F(32) * F(32 - 15, 100) == F(272, 50) and (F(40) * F(68, 100) - 34) < 0
Q(T, "Mixing solutions", I, "A dairy booth has 40 litres of milk adulterated with water, water being 15% of the "
  "mixture. It sells 8 litres of this mixture and then adds water to what is left until water is 32% of the "
  "mixture. How many litres of water does it add?",
  "8 litres", ["5.44 litres", "6.8 litres", "10 litres"],
  "Selling part of a mixture leaves the proportion unchanged; the milk stays fixed when only water is added",
  "After selling 8 litres, 32 litres remain: milk 85% = 27.2 L, water 4.8 L. When water is 32%, milk is 68% of the "
  "new total, so the total = 27.2 ÷ 0.68 = 40 L. Water added = 40 − 32 = 8 litres.",
  ["Left: 32 L, milk 27.2 L", "Milk = 68% of new total ⇒ total = 40 L", "Water added = 40 − 32 = 8 L"],
  why="5.44 litres raises the water by 17% of the 32 litres (32% − 15%); 6.8 litres is 17% of 40 litres; 10 litres "
      "forgets the 8 litres sold and works from 40 litres of mixture (40 × 0.85 ÷ 0.68 − 40).", secs=70)

cp_mix = F(432) / F(6, 5)
r1, r2_ = 450 - cp_mix, cp_mix - 300  # cheap : dear
assert cp_mix == 360 and (r1, r2_) == (90, 60)  # 3 : 2
cp_rev = (2 * 300 + 3 * 450) / F(5)
gain = (432 - cp_rev) / cp_rev
assert cp_rev == 390 and pct2(gain) == "10.77%" and pct2(F(432 - 375, 375)) == "15.20%" and pct2(F(42, 432)) == "9.72%"
Q(T, "Alligation rule", A, "A merchant blends two teas costing ₹300 and ₹450 per kg and sells the blend at ₹432 per "
  "kg, making a profit of 20%. If he had blended the same two teas in the reverse ratio and sold the blend at the "
  "same price, what would his profit percentage have been (correct to two decimal places)?",
  "10.77%", ["15.20%", "9.72%", "20.00%"],
  "Find the cost of the blend from the selling price, the mixing ratio by alligation, then cost the reversed blend",
  "Cost of the blend = 432 ÷ 1.2 = ₹360 per kg. Alligation: cheap : dear = (450 − 360) : (360 − 300) = 90 : 60 = "
  "3 : 2. Reversed, the ratio is 2 : 3, costing (2 × 300 + 3 × 450) ÷ 5 = ₹390 per kg. Profit = (432 − 390) ÷ 390 = "
  "10.77%.",
  ["CP of blend = 432 ÷ 1.2 = 360", "Ratio cheap : dear = 3 : 2", "Reversed: CP = 1,950 ÷ 5 = 390",
   "Profit = 42 ÷ 390 = 10.77%"],
  why="15.20% costs the reversed blend at the simple average ₹375; 9.72% divides the profit ₹42 by the selling price; "
      "20.00% assumes the ratio does not affect the profit.", secs=110)

cost_mix = F(390) / F(13, 10)
h_, s_ = cost_mix - 40, 400 - cost_mix  # honey : syrup
syrup = s_ / (h_ + s_)
assert cost_mix == 300 and (h_, s_) == (260, 100) and pct2(syrup) == "27.78%"
assert pct2(F(100, 260)) == "38.46%" and pct2(F(100, 400)) == "25.00%"
assert pct2(F(400 - 390, 400 - 40)) == "2.78%"
Q(T, "Mixing solutions", A, "A trader buys pure honey at ₹400 per kg and mixes it with sugar syrup that costs him "
  "₹40 per kg. He sells the mixture at ₹390 per kg and makes a profit of 30%. What percentage of the mixture, by "
  "weight, is sugar syrup (correct to two decimal places)?",
  "27.78%", ["38.46%", "25.00%", "2.78%"],
  "Cost price of the mixture from the profit; then alligation between the two cost prices",
  "Cost of the mixture = 390 ÷ 1.3 = ₹300 per kg. Honey : syrup = (300 − 40) : (400 − 300) = 260 : 100 = 13 : 5. "
  "Syrup = 5 ÷ 18 = 27.78% of the mixture.",
  ["CP of mixture = 390 ÷ 1.3 = 300", "Honey : syrup = 260 : 100 = 13 : 5", "Syrup share = 5/18 = 27.78%"],
  why="38.46% is the ratio syrup : honey (100 ÷ 260), not the syrup's share of the whole; 25.00% divides the syrup's "
      "100 parts by 400 instead of by the 360 parts of the whole; 2.78% uses the selling price ₹390 in place of the "
      "cost price in the alligation (10 : 350).", secs=110)

# ================================================================ Time and Work (B3 I2 A1)
T = "Time and Work"
ab = F(40, 100) / 6
a_ = ab - F(1, 25)
assert ab == F(1, 15) and a_ == F(2, 75) and 1 / a_ == F(75, 2)
Q(T, "Work efficiency", B, "A and B together finish 40% of a job in 6 days. B alone can finish the whole job in 25 "
  "days. In how many days can A alone finish the whole job?",
  "37½ days", ["15 days", "10 days", "40 days"],
  "Rate = work ÷ time; A's rate = (A + B)'s rate − B's rate",
  "Together they do 0.4 of the job in 6 days, i.e. 1/15 of it per day. B does 1/25 per day. A does 1/15 − 1/25 = "
  "2/75 per day, so A alone needs 75/2 = 37½ days.",
  ["(A + B) = 0.4 ÷ 6 = 1/15 per day", "A = 1/15 − 1/25 = 2/75", "A alone = 37½ days"],
  why="15 days is the time for A and B together on the whole job; 10 days subtracts the times (25 − 15); 40 days "
      "treats 40% of the job as taking 6 days for A alone.", secs=45)

r = {"A": F(1, 10), "B": F(1, 12), "C": F(1, 15)}
c_sh = 18000 * r["C"] / sum(r.values())
assert c_sh == 4800 and 18000 * F(10, 37) != c_sh and 18000 * F(1, 3) == 6000
Q(T, "Work and wages", B, "A, B and C can finish a job alone in 10, 12 and 15 days respectively. They do it together "
  "and are paid ₹18,000, shared in proportion to the work each does. What is C's share?",
  "₹4,800", ["₹7,200", "₹6,000", "₹1,200"],
  "Working the same number of days, shares are in the ratio of daily rates (1/10 : 1/12 : 1/15)",
  "Daily rates 1/10 : 1/12 : 1/15 = 6 : 5 : 4 (multiply by 60). C's share = 4/15 × 18,000 = ₹4,800.",
  ["Rates × 60: 6 : 5 : 4", "Total parts = 15", "C = 4/15 × 18,000 = ₹4,800"],
  why="₹7,200 is A's share (6 parts), given to C because C's number of days is largest; ₹6,000 splits the money "
      "equally; ₹1,200 is 18,000 × 1/15, C's daily rate applied to the whole payment.",
  secs=45)

t_ = 1 / (F(1, 12) + F(1, 15))
assert t_ == F(20, 3) and (12 + 15) / F(2) == F(27, 2) and 1 / (F(1, 12) + F(1, 15)) / 2 != t_
Q(T, "Men-women-children", B, "5 men can finish a job in 12 days, and 6 women can finish the same job in 15 days. "
  "In how many days can 5 men and 6 women working together finish it?",
  "6⅔ days", ["13½ days", "27 days", "7½ days"],
  "Each group is a single 'worker' with its own rate; add the rates",
  "5 men do 1/12 of the job a day and 6 women do 1/15. Together: 1/12 + 1/15 = 9/60 = 3/20 per day, so they need "
  "20/3 = 6⅔ days.",
  ["5 men: 1/12 per day", "6 women: 1/15 per day", "Together 3/20 ⇒ 6⅔ days"],
  why="13½ days averages the two times; 27 days adds them; 7½ days divides the product by the wrong sum "
      "(12 × 15 ÷ 24).", secs=40)

# A works every day; B helps on even days only (days 2, 4, 6, ...)
work, day = F(0), 0
while True:
    day += 1
    rate = F(1, 20) + (F(1, 30) if day % 2 == 0 else 0)
    if work + rate >= 1:
        total = day - 1 + (1 - work) / rate
        break
    work += rate
assert total == F(76, 5) and day == 16
Q(T, "Alternate days", I, "A can finish a job in 20 days and B in 30 days. A works every day, while B joins him only "
  "on the 2nd, 4th, 6th, … days. How long does the job take in all?",
  "15⅕ days", ["16 days", "12 days", "15 days"],
  "Work out a two-day cycle, then finish the remainder at the rate of the day on which it falls",
  "A two-day cycle (A alone, then A + B) does 1/20 + (1/20 + 1/30) = 2/15. Seven cycles (14 days) do 14/15, leaving "
  "1/15. Day 15 (A alone) does 1/20, leaving 1/15 − 1/20 = 1/60. Day 16 (A + B, rate 1/12) needs (1/60) ÷ (1/12) = "
  "1/5 of a day. Total = 15⅕ days.",
  ["Cycle of 2 days = 2/15", "14 days ⇒ 14/15", "Day 15: 1/20 ⇒ 1/60 left", "Day 16: 1/60 ÷ 1/12 = 1/5 day",
   "Total 15⅕ days"],
  why="16 days counts the 16th day as a full day; 12 days assumes A and B work together every day; 15 days stops "
      "when the cycles reach 14/15 and adds a full day without checking that the job is not yet finished.", secs=80)

# A takes 10 days more than (A + B), B takes 22.5 more: T^2 = 10 * 22.5
T_ = F(15)
assert T_ * T_ == 10 * F(45, 2)
assert 1 / (1 / (T_ + 10) + 1 / (T_ + F(45, 2))) == T_
Q(T, "Work efficiency", I, "Working alone, A takes 10 days more than A and B take together, and B takes 22½ days "
  "more than A and B take together. How many days does A alone take?",
  "25 days", ["15 days", "37½ days", "32½ days"],
  "If together they take T days, then T² = (A's extra days) × (B's extra days)",
  "Let together = T. Then A = T + 10, B = T + 22.5 and 1/(T + 10) + 1/(T + 22.5) = 1/T, which simplifies to "
  "T² = 10 × 22.5 = 225, so T = 15. A alone = 15 + 10 = 25 days.",
  ["T² = 10 × 22.5 = 225", "T = 15 days", "A = T + 10 = 25 days"],
  short="T = √(10 × 22.5) = 15.",
  why="15 days is the time taken together; 37½ days is B's time; 32½ days adds 10 and 22½.", secs=70)

W = (2 * 2 + 3 * 1) * 8
assert W == (3 * 2 + 2 * 1) * 7 == 56
men = (F(W, 4) - 4 * 1) / 2
assert men == 5
Q(T, "Men-women-children", A, "2 men and 3 boys can finish a job in 8 days, while 3 men and 2 boys can finish it in "
  "7 days. How many men must work along with 4 boys to finish the job in 4 days?",
  "5", ["10", "3", "7"],
  "Two equations in the daily work of a man (m) and a boy (b); then the strength needed for the deadline",
  "8(2m + 3b) = 7(3m + 2b) ⇒ 16m + 24b = 21m + 14b ⇒ 5m = 10b ⇒ m = 2b. Take b = 1 unit a day: the job = "
  "8 × (4 + 3) = 56 units. To finish in 4 days, 14 units a day are needed; 4 boys give 4, so men must give 10, "
  "i.e. 10 ÷ 2 = 5 men.",
  ["8(2m + 3b) = 7(3m + 2b) ⇒ m = 2b", "Job = 56 boy-days", "Need 14 per day; 4 boys give 4", "Men = 10 ÷ 2 = 5"],
  why="10 treats a man as equal to a boy (14 − 4 = 10); 3 counts each boy as a man's work (14 − 8 = 6, ÷ 2); 7 "
      "ignores the 4 boys (14 ÷ 2).", secs=100)

# ================================================================ Pipes and Cisterns (B1 I2 A1)
T = "Pipes and Cisterns"
need = 1800 - F(1800, 3)
t_ = need / (25 - 15)
assert t_ == 120 and F(1800, 10) == 180 and need / 25 == 48
Q(T, "Inlet and outlet", B, "A 1,800-litre tank is one-third full. Its inlet pipe adds 25 litres a minute and its "
  "outlet pipe drains 15 litres a minute. If both are opened together, how long will it take to fill the tank?",
  "2 hours", ["3 hours", "48 minutes", "1 hour 12 minutes"],
  "Net inflow = inlet rate − outlet rate; time = water still needed ÷ net inflow",
  "Water still needed = 1,800 − 600 = 1,200 litres. Net inflow = 25 − 15 = 10 litres a minute. Time = 1,200 ÷ 10 = "
  "120 minutes = 2 hours.",
  ["Needed = 1,200 L", "Net = 10 L/min", "Time = 120 min = 2 h"],
  why="3 hours fills all 1,800 litres from empty; 48 minutes ignores the outlet (1,200 ÷ 25); 1 hour 12 minutes "
      "fills only 1,800 ÷ 25 minutes with the inlet alone.", secs=40)

leak = F(1, 6) - (F(1, 2) / 4)
assert leak == F(1, 24) and 1 / (F(1, 6) - F(1, 7)) == 42
Q(T, "Leak problems", I, "A pipe can fill a tank in 6 hours. When the tank is exactly half full, a leak develops at "
  "the bottom, and the tank takes 7 hours in all to fill, counted from empty. How long would the leak alone take "
  "to empty the full tank?",
  "24 hours", ["42 hours", "12 hours", "8 hours"],
  "The first half fills at the normal rate; the leak acts only during the second half",
  "The first half takes 3 hours, so the second half takes 7 − 3 = 4 hours: net rate = (1/2) ÷ 4 = 1/8 per hour. "
  "Leak = 1/6 − 1/8 = 1/24 per hour, so the leak empties the full tank in 24 hours.",
  ["First half: 3 h", "Second half: 4 h ⇒ net 1/8", "Leak = 1/6 − 1/8 = 1/24 ⇒ 24 h"],
  why="42 hours assumes the leak worked for the whole 7 hours (1/6 − 1/7); 12 hours is the time the leak needs to "
      "empty only half the tank; 8 hours is the time the pipe and leak together would need for a full "
      "tank.", secs=65)

part1 = 6 * (F(1, 18) + F(1, 24))
t2 = (1 - part1) / (F(1, 18) + F(1, 24) - F(1, 36))
assert part1 == F(7, 12) and t2 == 6 and 6 + t2 == 12
assert 1 / (F(1, 18) + F(1, 24) - F(1, 36)) == F(72, 5) and 1 / (F(1, 18) + F(1, 24)) == F(72, 7)
Q(T, "Inlet and outlet", I, "Pipes A and B can fill a tank in 18 minutes and 24 minutes respectively, and pipe C can "
  "empty the full tank in 36 minutes. A and B are opened together on the empty tank; after 6 minutes C is also "
  "opened. How long does it take in all to fill the tank?",
  "12 minutes", ["14 minutes 24 seconds", "10 minutes 17 seconds", "6 minutes"],
  "Fill part of the tank with A + B, then the rest with the net rate of all three",
  "In 6 minutes A and B fill 6 × (1/18 + 1/24) = 6 × 7/72 = 7/12. Net rate of all three = 1/18 + 1/24 − 1/36 = "
  "(4 + 3 − 2)/72 = 5/72 per minute. The remaining 5/12 needs (5/12) ÷ (5/72) = 6 minutes. Total = 12 minutes.",
  ["6 min of A + B: 7/12", "Net rate with C: 5/72", "Rest: 5/12 ÷ 5/72 = 6 min", "Total = 12 min"],
  why="14 min 24 s has all three pipes open from the start (72/5 min); 10 min 17 s never opens C (72/7 min); "
      "6 minutes is only the time after C is opened.", secs=70)

a_r = F(1, 9)
b_r = F(1, 6) - a_r
assert 2 * a_r + b_r / 2 == F(1, 4) and 1 / a_r == 9 and 1 / b_r == 18
Q(T, "Inlet and outlet", A, "Pipes A and B together fill a tank in 6 hours. If A worked at twice its normal rate and "
  "B at half its normal rate, together they would fill the tank in 4 hours. How long does A alone take to fill the "
  "tank?",
  "9 hours", ["18 hours", "12 hours", "8 hours"],
  "Two equations in the hourly rates a and b",
  "a + b = 1/6 and 2a + b/2 = 1/4. From the first, b = 1/6 − a; then 2a + 1/12 − a/2 = 1/4, so 1.5a = 1/6 and "
  "a = 1/9. A alone takes 9 hours (and B 18 hours).",
  ["a + b = 1/6", "2a + b/2 = 1/4", "1.5a = 1/6 ⇒ a = 1/9", "A alone = 9 h"],
  why="18 hours is B's time; 12 hours assumes A and B are equally fast (each twice 6 hours); 8 hours treats the "
      "4-hour figure as A's double-rate time (2 × 4).", secs=100)

# ================================================================ Speed, Time and Distance (B1 I3 A3)
T = "Speed, Time and Distance"
v = 1 / (F(2, 5) / 40 + F(3, 5) / 60)
assert v == 50 and F(2, 5) * 40 + F(3, 5) * 60 == 52 and F(2 * 40 * 60, 100) == 48
alt = 1 / (F(2, 5) / 60 + F(3, 5) / 40)
assert N(alt) == "46.15"
Q(T, "Average speed", B, "A van covers two-fifths of a journey at 40 km/h and the rest at 60 km/h. What is its "
  "average speed for the whole journey?",
  "50 km/h", ["52 km/h", "48 km/h", "46.15 km/h"],
  "Average speed = total distance ÷ total time; take the distance as 1 (or any convenient number)",
  "Take the journey as 5 units: 2 units at 40 km/h take 2/40 = 1/20, and 3 units at 60 km/h take 3/60 = 1/20. "
  "Total time = 1/10, so the average speed = 5 ÷ (1/10) = 50 km/h.",
  ["Time for 2/5 at 40 = 1/100 per unit journey", "Time for 3/5 at 60 = 1/100", "Average = 1 ÷ (2/100) = 50 km/h"],
  short="Take 200 km: 80 km take 2 h, 120 km take 2 h ⇒ 200 ÷ 4 = 50 km/h.",
  why="52 km/h weights the speeds by distance (0.4 × 40 + 0.6 × 60); 48 km/h is the equal-distance formula "
      "2 × 40 × 60 ÷ 100, which ignores the 2 : 3 split; 46.15 km/h swaps the two speeds.", secs=45)

head = 30 * 1
t_after8 = F(255 - head, 30 + 45)
assert t_after8 == 3 and F(255, 75) == F(17, 5) and F(255, 45) == F(17, 3)
Q(T, "Relative speed", I, "From a crossroads, Amit drives east at 30 km/h starting at 7:00 AM. Bina starts from the "
  "same crossroads at 8:00 AM and drives west at 45 km/h. At what time will they be 255 km apart?",
  "11:00 AM", ["10:24 AM", "11:24 AM", "1:40 PM"],
  "Moving apart in opposite directions, the gap grows at the sum of the speeds; count Amit's head start first",
  "By 8:00 AM Amit is 30 km away. After that the gap grows at 30 + 45 = 75 km/h, so the remaining 225 km take "
  "225 ÷ 75 = 3 hours: 8:00 AM + 3 h = 11:00 AM.",
  ["Head start by 8:00 = 30 km", "Gap grows at 75 km/h", "225 ÷ 75 = 3 h ⇒ 11:00 AM"],
  why="10:24 AM divides 255 by 75 and counts from 7:00 AM, as if both had started then; 11:24 AM does the same "
      "division but counts from 8:00 AM, ignoring the head start; 1:40 PM uses Bina's speed alone (255 ÷ 45).",
  secs=60)

# A covers x km in 2 h and the remaining (54 - x) km in 2.5 h at the same speed: x/2 = (54 - x)/2.5
x_ = F(54 * 2, F(9, 2))
va, vb = x_ / 2, (54 - x_) / 2
assert x_ == 24 and va == 12 and vb == 15
Q(T, "Meeting and overtaking", I, "Two cyclists start at 10:00 AM from towns A and B, 54 km apart, and ride towards "
  "each other. They meet at 12:00 noon. After the meeting, the cyclist from A takes another 2 hours 30 minutes to "
  "reach B. What is the speed of the cyclist from B?",
  "15 km/h", ["12 km/h", "13.5 km/h", "27 km/h"],
  "The part A covers before the meeting (2 h) and after it (2½ h) are in the ratio of the times at A's speed",
  "A's distances before and after the meeting are in the ratio 2 : 2.5 = 4 : 5, so A covered 4/9 × 54 = 24 km "
  "before the meeting. B covered the other 30 km in the same 2 hours, so B's speed = 30 ÷ 2 = 15 km/h.",
  ["A: 2 h + 2.5 h for 54 km ⇒ 12 km/h", "Before meeting A covered 24 km", "B covered 30 km in 2 h ⇒ 15 km/h"],
  why="12 km/h is A's speed; 13.5 km/h divides 54 km by 4 hours (counting the 2 hours to the meeting twice); 27 km/h is their combined "
      "speed (54 ÷ 2).", secs=70)

gap0 = 4 * F(1, 2)
t_ = (gap0 + 1) / (10 - 4)
assert gap0 == 2 and t_ == F(1, 2) and gap0 / 6 == F(1, 3) and F(3, 10) * 60 == 18 and F(1, 6) * 60 == 10
Q(T, "Relative speed", I, "Ravi starts walking along a road at 4 km/h. Half an hour later Shyam starts cycling from "
  "the same point along the same road at 10 km/h. How many minutes after Shyam starts will he be 1 km ahead of "
  "Ravi?",
  "30 minutes", ["20 minutes", "18 minutes", "10 minutes"],
  "Shyam must first make up Ravi's lead and then gain 1 km more, at the relative speed 10 − 4 = 6 km/h",
  "In half an hour Ravi walks 2 km. Shyam must gain 2 + 1 = 3 km at 6 km/h: 3 ÷ 6 = ½ hour = 30 minutes.",
  ["Ravi's lead = 2 km", "Gain needed = 3 km", "3 ÷ 6 h = 30 min"],
  why="20 minutes is when Shyam only catches up (2 ÷ 6 h); 18 minutes divides 3 km by Shyam's own speed; 10 minutes "
      "covers only the extra 1 km at 6 km/h.", secs=55)

b_ = None
for bd in range(1, 120):
    t1 = F(bd, 60) + F(120 - bd, 80)
    t2 = F(bd, 80) + F(120 - bd, 60)
    if t2 - t1 == F(1, 6):
        b_ = bd
assert b_ == 40
Q(T, "Average speed", A, "Kiran travels 120 km, partly by bus at 60 km/h and the rest by car at 80 km/h. Had he "
  "travelled the bus part by car and the car part by bus, the journey would have taken 10 minutes longer. How many "
  "kilometres did he travel by bus?",
  "40 km", ["80 km", "60 km", "20 km"],
  "Write both total times in terms of the bus distance b and subtract",
  "Actual time = b/60 + (120 − b)/80; swapped time = b/80 + (120 − b)/60. The difference = (120 − b)(1/60 − 1/80) − "
  "b(1/60 − 1/80) = (120 − 2b)/240 hours. Setting this equal to 1/6 hour: 120 − 2b = 40, so b = 40 km.",
  ["Swapped − actual = (120 − 2b)/240 h", "= 1/6 h", "120 − 2b = 40 ⇒ b = 40 km"],
  short="Check: actual 40/60 + 80/80 = 1 h 40 min; swapped 40/80 + 80/60 = 1 h 50 min.",
  why="80 km is the car distance; 60 km assumes an equal split, which would make the two journeys equally long; "
      "20 km comes from setting 120 − 2b = 80 (taking 10 minutes as 1/3 hour).", secs=110, by=BRUTE)

# dog: 3 leaps while hare 4; 2 dog leaps = 3 hare leaps; hare 60 hare-leaps ahead
gain_per_unit = 3 * F(3, 2) - 4
units = 60 / gain_per_unit
assert gain_per_unit == F(1, 2) and units == 120 and 3 * units == 360 and 4 * units == 480
Q(T, "Meeting and overtaking", A, "A hare is 60 of its own leaps ahead of a dog. The dog makes 3 leaps in the time "
  "the hare makes 4, but 2 of the dog's leaps cover the same distance as 3 of the hare's. How many leaps must the "
  "dog make to catch the hare?",
  "360", ["480", "120", "240"],
  "Measure everything in hare-leaps: the dog gains (its distance − hare's distance) in each time unit",
  "In one time unit the dog makes 3 leaps = 3 × 1.5 = 4.5 hare-leaps, while the hare makes 4. The dog gains 0.5 "
  "hare-leap per unit, so it needs 60 ÷ 0.5 = 120 units, in which it makes 3 × 120 = 360 leaps.",
  ["1 dog leap = 1.5 hare leaps", "Gain per unit = 4.5 − 4 = 0.5", "Units = 120", "Dog leaps = 360"],
  why="480 is the number of leaps the hare makes in that time; 120 is the number of time units; 240 counts only two "
      "dog leaps per unit.", secs=110)

walk = F(31, 4) / 2
ride = F(23, 4) - walk
assert walk == F(31, 8) and ride == F(15, 8) and 2 * ride == F(15, 4)
Q(T, "Average speed", A, "Walking to his office and riding back home takes Sunil 5 hours 45 minutes. Walking both "
  "ways takes him 7 hours 45 minutes. How long would he take to ride both ways?",
  "3 hours 45 minutes", ["1 hour 52½ minutes", "2 hours", "3 hours 52½ minutes"],
  "Walk-both-ways gives one walk; subtract it from walk + ride to get one ride",
  "One walk = 7 h 45 min ÷ 2 = 3 h 52½ min. One ride = 5 h 45 min − 3 h 52½ min = 1 h 52½ min. Riding both ways = "
  "2 × 1 h 52½ min = 3 h 45 min.",
  ["Walk one way = 3 h 52½ min", "Ride one way = 1 h 52½ min", "Ride both ways = 3 h 45 min"],
  short="Ride both = 2 × (walk + ride) − (walk both) = 11 h 30 min − 7 h 45 min = 3 h 45 min.",
  why="1 h 52½ min is a single ride; 2 hours is the difference between the two given times; 3 h 52½ min is a "
      "single walk.", secs=80)

# ================================================================ Boats and Streams (B1 I2 A2)
T = "Boats and Streams"
dn = F(48, 3)
assert dn - 14 == 2
Q(T, "Speed of stream", B, "A boat's speed in still water is 14 km/h. It covers 48 km downstream in 3 hours. What is "
  "the speed of the stream?",
  "2 km/h", ["16 km/h", "1 km/h", "4 km/h"],
  "Downstream speed = boat speed + stream speed",
  "Downstream speed = 48 ÷ 3 = 16 km/h. Stream = 16 − 14 = 2 km/h.",
  ["Downstream = 16 km/h", "Stream = 16 − 14 = 2 km/h"],
  why="16 km/h is the downstream speed; 1 km/h halves the difference as if 16 and 14 were the downstream and "
      "upstream speeds; 4 km/h doubles the difference.", secs=35)

down, up = 10 + 2, 14 - 2
t_ = F(72, down + up)
assert t_ == 3 and down * t_ == 36 and 10 * t_ == 30 and 14 * t_ == 42 and 8 * t_ == 24
Q(T, "Upstream and downstream", I, "Ports P and Q are 72 km apart on a river that flows from P towards Q at 2 km/h. "
  "At the same moment a boat with a still-water speed of 10 km/h leaves P for Q, and a boat with a still-water "
  "speed of 14 km/h leaves Q for P. How far from P do they meet?",
  "36 km", ["30 km", "42 km", "24 km"],
  "Moving towards each other, the stream adds to one boat and takes the same from the other, so the closing speed "
  "is the sum of the still-water speeds",
  "Closing speed = (10 + 2) + (14 − 2) = 24 km/h, so they meet after 72 ÷ 24 = 3 hours. The boat from P moves "
  "downstream at 12 km/h and covers 12 × 3 = 36 km.",
  ["Closing speed = 12 + 12 = 24 km/h", "Meet after 3 h", "From P: 12 × 3 = 36 km"],
  why="30 km uses the boat's still-water speed (10 × 3); 42 km is the other boat's still-water speed × 3; 24 km "
      "subtracts the stream from the downstream boat (8 × 3).", secs=60)

dn, b_s = F(42, 3), F(7, 3)
up = dn * F(3, 7)
assert dn == 14 and up == 6 and F(42) / up == 7 and F(42) / ((dn + up) / 2) == F(21, 5) and F(42, 7) == 6
Q(T, "Upstream and downstream", I, "A boat's downstream speed and upstream speed are in the ratio 7 : 3. It covers "
  "42 km downstream in 3 hours. How long will it take to cover the same 42 km upstream?",
  "7 hours", ["4 hours 12 minutes", "1 hour 17 minutes", "6 hours"],
  "Upstream speed = 3/7 of the downstream speed; time = distance ÷ speed",
  "Downstream speed = 42 ÷ 3 = 14 km/h, so upstream speed = 14 × 3/7 = 6 km/h. Time upstream = 42 ÷ 6 = 7 hours.",
  ["Downstream = 14 km/h", "Upstream = 6 km/h", "42 ÷ 6 = 7 h"],
  short="Time varies inversely as speed: 3 × 7/3 = 7 hours.",
  why="4 h 12 min uses the still-water speed 10 km/h; 1 h 17 min applies the ratio the wrong way (3 × 3/7 h); "
      "6 hours is the upstream speed, not the time.", secs=50)

s_ = None
for k in range(1, 100):
    s = F(k, 10)
    if 2 * (12 - s) - F(1, 2) * s + F(3, 2) * (12 - s) == 36:
        s_ = s
assert s_ == F(3, 2)
assert r2(12 - F(36, F(7, 2))) == F("1.71") and F(12 - 9) == 3 and F(12, F(9, 2)) == F(8, 3)
Q(T, "Speed of stream", A, "A motorboat with a still-water speed of 12 km/h goes upstream for 2 hours. Its engine "
  "then fails and it drifts with the current for 30 minutes. After the repair it goes upstream again for 1½ hours, "
  "and is now 36 km upstream of its starting point. What is the speed of the stream?",
  "1.5 km/h", ["1.71 km/h", "3 km/h", "2.67 km/h"],
  "Upstream legs move the boat forward at (12 − s); the drift carries it back at s",
  "Net distance = 3.5 × (12 − s) − 0.5 × s = 42 − 4s = 36, so s = 1.5 km/h.",
  ["Upstream: 3.5 h at (12 − s)", "Drift back: 0.5 h at s", "42 − 4s = 36 ⇒ s = 1.5"],
  why="1.71 km/h ignores the drift (3.5(12 − s) = 36); 3 km/h treats the drift as 30 more minutes upstream "
      "(4(12 − s) = 36); 2.67 km/h counts 4 hours upstream and also subtracts the drift.", secs=110, by=BRUTE)

sol = [(b, F(16, 3) * b / 2) for b in range(4, 40) if 2 * (F(16, 3) * b / 2) * b / F(b * b - 9) == 6]
assert sol == [(9, 24)]
Q(T, "Upstream and downstream", A, "On a river flowing at 3 km/h, a boat goes from ghat A to ghat B and comes back in "
  "6 hours. On still water the same round trip would take 5 hours 20 minutes. How far apart are the ghats?",
  "24 km", ["48 km", "27 km", "32 km"],
  "In still water 2d/b = 16/3; with the stream d/(b + 3) + d/(b − 3) = 6. Eliminate d",
  "From still water, d = (8/3)b. Then 2db/(b² − 9) = 6 gives (16/3)b² = 6b² − 54, so b² = 81 and b = 9 km/h. "
  "d = (8/3) × 9 = 24 km. Check: 24 ÷ 12 + 24 ÷ 6 = 2 + 4 = 6 hours.",
  ["d = 8b/3", "2db/(b² − 9) = 6 ⇒ b = 9", "d = 24 km", "Check: 2 h + 4 h = 6 h"],
  why="48 km is the round-trip distance; 27 km uses the average of the downstream and upstream speeds (9 km/h) "
      "for the 6 hours; 32 km takes the downstream speed 12 km/h as the still-water speed (12 × 5⅓ ÷ 2).",
  secs=120, by=BRUTE)

# ================================================================ Problems on Trains (B1 I2 A1)
T = "Problems on Trains"
gap = 14 * 50
t_ = F(gap, F(90 * 5, 18))
assert t_ == 28 and F(15 * 50, 25) == 30 and F(13 * 50, 25) == 26 and F(16 * 50, 25) == 32
Q(T, "Crossing a pole or platform", B, "Telegraph poles stand 50 m apart along a railway line. A train runs at "
  "90 km/h. How long does its engine take to go from the 1st pole to the 15th pole?",
  "28 seconds", ["30 seconds", "26 seconds", "32 seconds"],
  "From the 1st to the 15th pole there are 14 gaps; 90 km/h = 25 m/s",
  "Distance = 14 × 50 = 700 m. Speed = 90 × 5/18 = 25 m/s. Time = 700 ÷ 25 = 28 seconds.",
  ["14 gaps × 50 m = 700 m", "90 km/h = 25 m/s", "700 ÷ 25 = 28 s"],
  why="30 seconds counts 15 gaps; 26 seconds counts 13; 32 seconds counts 16 — the usual off-by-one slips.", secs=35)

t_meet = F(330, 110)
assert t_meet == 3 and (50 + 60) * 1 == 110 and 330 - 110 == 220 and 60 - 50 == 10
Q(T, "Trains crossing each other", I, "Two trains start at the same time from stations 330 km apart and run towards "
  "each other on parallel tracks at 50 km/h and 60 km/h. How far apart are they one hour before they meet?",
  "110 km", ["220 km", "10 km", "55 km"],
  "One hour before meeting, the gap equals the distance closed in one hour, i.e. the sum of the speeds",
  "They close the gap at 50 + 60 = 110 km/h, so one hour before they meet they are 110 km apart (they meet after "
  "3 hours; after 2 hours they have covered 220 km of the 330 km).",
  ["Closing speed = 110 km/h", "Gap 1 h before meeting = 110 km"],
  short="The starting distance is not needed.",
  why="220 km is the distance already covered after 2 hours; 10 km uses the difference of the speeds; 55 km halves "
      "the closing distance.", secs=45)

rel = F((54 + 36) * 5, 18)
lb = rel * 12
la = rel * 18 - lb
assert rel == 25 and lb == 300 and la == 150 and F(54 * 5, 18) * 12 == 180
Q(T, "Trains crossing each other", I, "Train P runs at 54 km/h and train Q at 36 km/h, towards each other on "
  "parallel tracks. They cross each other completely in 18 seconds. A passenger sitting in P sees Q go past him in "
  "12 seconds. What is the length of train P?",
  "150 m", ["300 m", "450 m", "180 m"],
  "Relative speed (opposite directions) = sum of speeds; the passenger is a point, so Q's length = relative speed "
  "× 12",
  "Relative speed = 90 km/h = 25 m/s. Q passes the passenger in 12 s, so Q = 25 × 12 = 300 m. Crossing completely "
  "covers both lengths: 25 × 18 = 450 m. So P = 450 − 300 = 150 m.",
  ["Relative speed = 25 m/s", "Q = 25 × 12 = 300 m", "P + Q = 25 × 18 = 450 m", "P = 150 m"],
  why="300 m is Q's length; 450 m is the two lengths together; 180 m multiplies P's own speed (15 m/s) by 12 s.",
  secs=70)

# tunnel of length 4 units, cat 1 unit from entrance A, train d units before A; speeds v (train), c (cat)
ok = []
for ratio in (F(2), F(4), F(3), F(3, 2)):
    c = F(1)
    v = ratio * c
    d = v * (1 / c)               # cat runs 1 unit towards A, train reaches A at the same instant
    ok.append((ratio, (d + 4) / v == 3 / c))   # cat runs 3 units to B, train covers d + 4
assert ok == [(F(2), True), (F(4), False), (F(3), False), (F(3, 2), False)]
Q(T, "Crossing a pole or platform", A, "A cat is inside a railway tunnel at a point one-quarter of the tunnel's "
  "length from entrance A. A train is approaching entrance A. If the cat runs towards the train, it just escapes "
  "at A as the train arrives there; if instead it runs away from the train, it just escapes at the other end B as "
  "the train arrives there. What is the ratio of the train's speed to the cat's speed?",
  "2 : 1", ["4 : 1", "3 : 1", "3 : 2"],
  "Compare the two escapes: the extra distance the cat runs (3/4 − 1/4 of the tunnel) takes the same time as the "
  "train needs to run through the whole tunnel",
  "Let the tunnel be 4 units, the cat 1 unit from A. Running to A takes the cat 1 unit of its distance; running to "
  "B takes 3. In the extra time the cat runs 3 − 1 = 2 units, the train goes from A to B, i.e. 4 units. So the "
  "train is 4 ÷ 2 = 2 times as fast as the cat.",
  ["Cat: 1 unit (to A) or 3 units (to B)", "Extra 2 units ↔ train's 4 units through the tunnel",
   "Speed ratio = 4 : 2 = 2 : 1"],
  why="4 : 1 divides the tunnel length by the cat's 1-unit run; 3 : 1 is the ratio of the cat's two runs; 3 : 2 "
      "divides the cat's longer run by its extra 2 units.", secs=110, by=BRUTE)

# ================================================================ Mensuration (B2 I2 A1)
T = "Mensuration"
d2 = 45 ** 2 + 28 ** 2
assert d2 == 53 ** 2 and r2(math.sqrt(45 ** 2 - 28 ** 2)) == F("35.23")
Q(T, "2D areas and perimeters", B, "A rectangular plot is 45 m long and 28 m wide. A straight path runs from one "
  "corner to the opposite corner. How long is the path?",
  "53 m", ["73 m", "35.23 m", "106 m"],
  "Diagonal of a rectangle = √(length² + breadth²)",
  "Diagonal = √(45² + 28²) = √(2,025 + 784) = √2,809 = 53 m.",
  ["45² = 2,025, 28² = 784", "Sum = 2,809", "√2,809 = 53 m"],
  why="73 m adds the two sides; 35.23 m subtracts the squares instead of adding them; 106 m is the two diagonals "
      "together.", secs=40)

wall = 1500 * 300 * 25
brick = F(25) * F(25, 2) * F(15, 2)
assert wall / brick == 4800
Q(T, "3D volume and surface area", B, "How many bricks, each 25 cm × 12.5 cm × 7.5 cm, are needed to build a wall "
  "15 m long, 3 m high and 25 cm thick? (Ignore the mortar.)",
  "4,800", ["48,000", "480", "2,400"],
  "Number of bricks = volume of the wall ÷ volume of one brick, both in the same unit",
  "Wall = 1,500 × 300 × 25 = 1,12,50,000 cm³. Brick = 25 × 12.5 × 7.5 = 2,343.75 cm³. Bricks = 1,12,50,000 ÷ "
  "2,343.75 = 4,800.",
  ["Wall = 1,12,50,000 cm³", "Brick = 2,343.75 cm³", "Bricks = 4,800"],
  why="48,000 and 480 come from slipping a factor of 10 in converting metres to centimetres; 2,400 takes the wall "
      "as 12.5 cm thick (half a brick's length).", secs=50)

csa = 2 * F(22, 7) * F(35, 100) * 4
assert csa == F(44, 5) and csa * 15 == 132 and (csa + 2 * F(22, 7) * F(35, 100) ** 2) * 15 == F(28710, 200)
Q(T, "Cylinder, cone and sphere", I, "A cylindrical pillar has a diameter of 70 cm and a height of 4 m. What will it "
  "cost to polish its curved surface at ₹15 per m²? (Use π = 22/7.)",
  "₹132", ["₹264", "₹66", "₹143.55"],
  "Curved surface area of a cylinder = 2πrh; radius = half the diameter",
  "r = 0.35 m, h = 4 m. CSA = 2 × 22/7 × 0.35 × 4 = 8.8 m². Cost = 8.8 × 15 = ₹132.",
  ["r = 0.35 m", "CSA = 2πrh = 8.8 m²", "Cost = 8.8 × 15 = ₹132"],
  why="₹264 uses the diameter as the radius; ₹66 drops the factor 2 (πrh); ₹143.55 also polishes the top and "
      "bottom faces (9.57 m²).", secs=55)

h_ = math.isqrt(10 ** 2 - ((32 - 20) // 2) ** 2)
assert h_ == 8 and F(32 + 20, 2) * h_ == 208 and 26 * 10 == 260 and 52 * 8 == 416 and 26 * 6 == 156
Q(T, "2D areas and perimeters", I, "A field is shaped like an isosceles trapezium. Its parallel sides are 32 m and "
  "20 m, and each of the other two sides is 10 m. What is its area?",
  "208 m²", ["260 m²", "416 m²", "156 m²"],
  "Drop perpendiculars from the shorter side: each end overhang is (32 − 20)/2 = 6 m, so height = √(10² − 6²)",
  "Overhang = 6 m, height = √(100 − 36) = 8 m. Area = ½ × (32 + 20) × 8 = 26 × 8 = 208 m².",
  ["Overhang = 6 m", "Height = 8 m", "Area = 26 × 8 = 208 m²"],
  why="260 m² uses the slanting side 10 m as the height; 416 m² forgets the ½; 156 m² uses the overhang 6 m as the "
      "height.", secs=60)

big = 6 * 12 ** 2
small = 27 * 6 * 4 ** 2
assert big == 864 and small == 2592 and (small - big) * 100 / big == 200 and small * 100 / big == 300
Q(T, "3D volume and surface area", A, "A solid cube of edge 12 cm is cut into 27 identical smaller cubes. By what "
  "percentage does the total surface area increase?",
  "200%", ["300%", "100%", "2,600%"],
  "Cutting into n³ cubes divides the edge by n; total surface area is multiplied by n",
  "Small edge = 12 ÷ 3 = 4 cm. Original area = 6 × 144 = 864 cm²; new total = 27 × 6 × 16 = 2,592 cm². Increase = "
  "1,728 ÷ 864 = 200%.",
  ["Small edge = 4 cm", "864 → 2,592 cm²", "Increase = 1,728 ÷ 864 = 200%"],
  short="Area becomes 3 times (n = 3), an increase of 200%.",
  why="300% is the new area as a percentage of the old, not the increase; 100% assumes the area only doubles; "
      "2,600% treats each small cube as having the original surface area.", secs=80)

# ================================================================ Probability (B1 I2 A2)
T = "Probability"
p = prob(DICE2, lambda w: w[0] > 4 and w[1] % 2 == 1)
assert p == F(1, 6) and prob(DICE2, lambda w: w[0] >= 4 and w[1] % 2) == F(1, 4)
Q(T, "Coins and dice", B, "A fair die is rolled twice. What is the probability that the first roll shows a number "
  "greater than 4 and the second roll shows an odd number?",
  "1/6", ["5/6", "1/3", "1/4"],
  "Independent rolls: multiply the probabilities",
  "P(first > 4) = 2/6 = 1/3 (5 or 6). P(second odd) = 3/6 = 1/2. Both: 1/3 × 1/2 = 1/6.",
  ["P(5 or 6) = 1/3", "P(odd) = 1/2", "Product = 1/6"],
  why="5/6 adds the two probabilities; 1/3 is the first event alone; 1/4 counts 4 as 'greater than 4'.", secs=35,
  by=BRUTE)

pairs = list(itertools.combinations(DECK, 2))
p = prob(pairs, lambda w: all(c[0] > 10 for c in w) and w[0][1] == w[1][1])
assert p == F(2, 221) and prob(pairs, lambda w: all(c[0] > 10 for c in w)) == F(11, 221)
Q(T, "Cards", I, "Two cards are drawn together at random from a well-shuffled pack of 52 cards. What is the "
  "probability that both are face cards (jack, queen or king) of the same suit?",
  "2/221", ["11/221", "1/442", "4/221"],
  "Favourable pairs: choose a suit (4 ways) and 2 of its 3 face cards (3 ways)",
  "Favourable = 4 × C(3, 2) = 12. Total = C(52, 2) = 1,326. P = 12/1,326 = 2/221.",
  ["Favourable = 4 × 3 = 12", "Total = 1,326", "P = 2/221"],
  why="11/221 allows the two face cards to be of any suits (C(12, 2) = 66); 1/442 fixes one particular suit; 4/221 "
      "counts ordered pairs (24) over unordered ones.", secs=60, by=BRUTE)

bag = ["R"] * 4 + ["B"] * 5 + ["W"] * 3
tri = list(itertools.combinations(range(12), 3))
p = prob(tri, lambda t: any(bag[i] == "W" for i in t))
assert p == F(34, 55) and prob(tri, lambda t: sum(bag[i] == "W" for i in t) == 1) == F(27, 55)
Q(T, "Balls from bags", I, "A bag contains 4 red, 5 blue and 3 white balls. Three balls are drawn at random "
  "together. What is the probability that at least one of them is white?",
  "34/55", ["21/55", "27/55", "1/4"],
  "P(at least one) = 1 − P(none)",
  "P(no white) = C(9, 3)/C(12, 3) = 84/220 = 21/55. P(at least one white) = 1 − 21/55 = 34/55.",
  ["Non-white balls = 9", "P(none white) = 84/220 = 21/55", "Answer = 34/55"],
  why="21/55 is the probability of no white ball; 27/55 is exactly one white ball; 1/4 is the chance that a single "
      "ball is white.", secs=60, by=BRUTE)

nums = list(itertools.combinations(range(1, 21), 2))
p = prob(nums, lambda t: t[0] * t[1] % 2 == 0)
assert p == F(29, 38) and prob(nums, lambda t: (t[0] + t[1]) % 2 == 1) == F(10, 19)
Q(T, "Balls from bags", A, "A box holds 20 tickets numbered 1 to 20. Two tickets are drawn at random together. What "
  "is the probability that the product of their numbers is even?",
  "29/38", ["9/38", "3/4", "10/19"],
  "The product is odd only if both numbers are odd; use the complement",
  "P(both odd) = C(10, 2)/C(20, 2) = 45/190 = 9/38. P(product even) = 1 − 9/38 = 29/38.",
  ["Odd tickets = 10", "P(both odd) = 45/190 = 9/38", "P(even product) = 29/38"],
  why="9/38 is the probability that the product is odd; 3/4 treats the draws as independent with replacement "
      "(1 − ½ × ½); 10/19 is the chance that exactly one number is even.", secs=80, by=BRUTE)

seqs = list(itertools.product("HT", repeat=5))
p = prob(seqs, lambda s: "HHH" in "".join(s))
p_exact3 = prob(seqs, lambda s: "HHH" in "".join(s) and "HHHH" not in "".join(s))
assert p == F(1, 4) and p_exact3 == F(5, 32) and prob(seqs, lambda s: s.count("H") >= 3) == F(1, 2)
Q(T, "Coins and dice", A, "A fair coin is tossed 5 times. What is the probability that at some point it shows heads "
  "at least 3 times in a row?",
  "1/4", ["1/2", "5/32", "3/8"],
  "Count the sequences directly by where the first run of three heads starts",
  "Run starting at toss 1 (HHH__): 4 sequences. First run starting at toss 2 (THHH_): 2. First run starting at "
  "toss 3 (_THHH): 2. Total 8 of 32 sequences, so P = 8/32 = 1/4.",
  ["Start at 1: HHH** ⇒ 4", "Start at 2: THHH* ⇒ 2", "Start at 3: *THHH ⇒ 2", "8/32 = 1/4"],
  why="1/2 is the probability of at least 3 heads in any positions; 5/32 counts only the sequences whose longest "
      "run is exactly 3; 3/8 adds 1/8 for each of the 3 possible starting positions, counting HHHH and HHHHH more "
      "than once.", secs=100, by=BRUTE)

# ================================================================ Permutation and Combination (B1 I1 A1)
T = "Permutation and Combination"
people = ["M"] * 8 + ["W"] * 5
cnt = sum(1 for t in itertools.combinations(range(13), 3) if any(people[i] == "W" for i in t))
assert cnt == 230 == math.comb(13, 3) - math.comb(8, 3) and 5 * math.comb(8, 2) == 140
Q(T, "Selections", B, "A team of 3 is to be chosen from 8 men and 5 women. In how many ways can it be chosen so that "
  "it includes at least one woman?",
  "230", ["286", "140", "56"],
  "At least one = all selections − selections with no woman",
  "All selections: C(13, 3) = 286. All-men selections: C(8, 3) = 56. With at least one woman: 286 − 56 = 230.",
  ["C(13, 3) = 286", "C(8, 3) = 56", "286 − 56 = 230"],
  why="286 ignores the condition; 140 counts exactly one woman (5 × 28); 56 is the number of all-men teams.",
  secs=45, by=BRUTE)

arr = set(p for p in itertools.permutations("BALANCE") if p[0] in "BLNC" and p[-1] in "BLNC")
assert len(arr) == 720 and len(set(itertools.permutations("BALANCE"))) == 2520
Q(T, "Word arrangements", I, "How many different arrangements of the letters of the word BALANCE begin and end with "
  "a consonant?",
  "720", ["1,440", "2,520", "360"],
  "Fill the two ends from the 4 distinct consonants, then arrange the middle five letters (A repeated)",
  "Consonants B, L, N, C: the first and last letters in 4 × 3 = 12 ways. The middle 5 letters (two consonants and "
  "A, A, E) can be arranged in 5!/2! = 60 ways. Total = 12 × 60 = 720.",
  ["Ends: 4 × 3 = 12", "Middle: 5!/2! = 60", "12 × 60 = 720"],
  why="1,440 forgets that the two A's are identical (12 × 5!); 2,520 is all arrangements of BALANCE; 360 divides by "
      "2! once more than needed.", secs=70, by=BRUTE)

seat = ["R", "M2", "M3", "M4", "S", "W2", "W3", "W4"]
alt_all = [p for p in itertools.permutations(seat)
           if all((p[i] in ("R", "M2", "M3", "M4")) != (p[i + 1] in ("R", "M2", "M3", "M4")) for i in range(7))]
adj = [p for p in alt_all if abs(p.index("R") - p.index("S")) == 1]
assert len(alt_all) == 1152 and len(adj) == 504 == 2 * 7 * 36
Q(T, "Arrangements", A, "Four men (including Rohan) and four women (including Sana) are to sit in a row of 8 chairs "
  "so that men and women sit alternately. In how many such arrangements do Rohan and Sana sit next to each other?",
  "504", ["1,152", "252", "1,008"],
  "Alternating patterns: MWMW… or WMWM…; any two neighbouring chairs hold one man and one woman",
  "There are 2 alternating patterns. In either pattern there are 7 pairs of neighbouring chairs, each pair having "
  "one man's chair and one woman's chair, so Rohan and Sana can be placed as neighbours in 7 ways. The other 3 men "
  "and 3 women fill their chairs in 3! × 3! = 36 ways. Total = 2 × 7 × 36 = 504.",
  ["Patterns = 2", "Neighbouring chair pairs = 7", "Others: 3! × 3! = 36", "2 × 7 × 36 = 504"],
  why="1,152 counts all alternating arrangements (2 × 4! × 4!); 252 uses only one of the two patterns; 1,008 also "
      "swaps Rohan and Sana within a pair, which the alternating pattern does not allow.", secs=110, by=BRUTE)

# ================================================================ Tabular DI (B2 I2 A3): sets of 4 and 3
T = "Tabular DI"
LOCK = {"Anandpur": (240, 204, 2400), "Bhimgarh": (180, 171, 3000), "Chandoli": (320, 256, 1800),
        "Devnagar": (150, 105, 4200), "Elampur": (200, 170, 2700)}
sid = stimulus("data_table", "Safe-deposit lockers at five bank branches, October 2026",
               "The table shows, for five branches of a bank in October 2026, the number of safe-deposit lockers "
               "available, the number allotted to customers and the annual rent charged per allotted locker. "
               "Lockers not allotted earn no rent.\n\n" +
               md_table(["Branch", "Lockers available", "Lockers allotted", "Annual rent per locker (₹)"],
                        [[k, a, b, ind(r)] for k, (a, b, r) in LOCK.items()]),
               {"columns": ["branch", "lockers_available", "lockers_allotted", "annual_rent_rs"],
                "rows": [[k, a, b, r] for k, (a, b, r) in LOCK.items()]})
vac = {k: a - b for k, (a, b, r) in LOCK.items()}
assert sum(vac.values()) == 184 and sum(b for a, b, r in LOCK.values()) == 906
assert sum(a for a, b, r in LOCK.values()) == 1090 and 184 - vac["Elampur"] == 154
Q(T, "Single table", B, "How many lockers in all were lying vacant (not allotted) at the five branches?",
  "184", ["906", "1,090", "154"],
  "Vacant = available − allotted, for each branch, then add",
  "Vacant: Anandpur 36, Bhimgarh 9, Chandoli 64, Devnagar 45, Elampur 30. Total = 184.",
  ["36 + 9 + 64 = 109", "45 + 30 = 75", "109 + 75 = 184"],
  why="906 is the number allotted and 1,090 the number available; 154 leaves out Elampur.", secs=40, stim=sid)

occ = {k: F(b, a) for k, (a, b, r) in LOCK.items()}
assert unique_max(occ) == "Bhimgarh" and occ["Bhimgarh"] == F(95, 100) and unique_max(
    {k: b for k, (a, b, r) in LOCK.items()}) == "Chandoli"
assert occ["Anandpur"] == occ["Elampur"] == F(85, 100) and occ["Chandoli"] == F(80, 100)
Q(T, "Table with percentages", B, "Which branch had allotted the highest percentage of its available lockers?",
  "Bhimgarh", ["Chandoli", "Anandpur", "Elampur"],
  "Allotment percentage = allotted ÷ available × 100",
  "Anandpur 85%, Bhimgarh 95%, Chandoli 80%, Devnagar 70%, Elampur 85%. Bhimgarh is the highest.",
  ["Anandpur 204/240 = 85%", "Bhimgarh 171/180 = 95%", "Chandoli 80%, Devnagar 70%, Elampur 85%"],
  why="Chandoli allotted the most lockers (256) but only 80% of its 320; Anandpur and Elampur are tied at 85%.",
  secs=45, stim=sid)

rent_d = 105 * 4200
assert rent_d == 441000 and 150 * 4200 == 630000 and 45 * 4200 == 189000 and F(rent_d, 12) == 36750
Q(T, "Single table", I, "What annual rent did the Devnagar branch earn from its lockers?",
  "₹4,41,000", ["₹6,30,000", "₹1,89,000", "₹36,750"],
  "Rent is earned only on allotted lockers",
  "Devnagar allotted 105 lockers at ₹4,200 a year each: 105 × 4,200 = ₹4,41,000.",
  ["Allotted = 105", "105 × 4,200 = ₹4,41,000"],
  why="₹6,30,000 charges rent on all 150 lockers; ₹1,89,000 charges it on the 45 vacant ones; ₹36,750 is one "
      "month's rent.", secs=45, stim=sid)

rc, ra = 256 * 1800, 204 * 2400
assert (rc, ra) == (460800, 489600) and pct2(F(ra - rc, ra)) == "5.88%" and pct2(F(ra - rc, rc)) == "6.25%"
assert pct2(F(600, 2400)) == "25.00%" and pct2(F(256 - 204, 204)) == "25.49%"
Q(T, "Single table", A, "By what percentage was the annual locker rent earned at Chandoli less than that earned at "
  "Anandpur (correct to two decimal places)?",
  "5.88%", ["6.25%", "25.00%", "25.49%"],
  "Compute each rent (allotted × rate), then (difference ÷ Anandpur's rent) × 100",
  "Chandoli: 256 × 1,800 = ₹4,60,800. Anandpur: 204 × 2,400 = ₹4,89,600. Difference = ₹28,800. 28,800 ÷ "
  "4,89,600 = 5.88%.",
  ["Chandoli = 4,60,800", "Anandpur = 4,89,600", "28,800 ÷ 4,89,600 = 5.88%"],
  why="6.25% divides the difference by Chandoli's rent; 25.00% compares only the rent per locker; 25.49% compares "
      "only the number of lockers allotted (and Chandoli has more, not fewer).", secs=90, stim=sid)

RD = {"Rampur": (480, 50, 1250), "Sitapur": (360, 65, 1500), "Kheda": (600, 40, 950), "Lonar": (420, 60, 1100)}
sid = stimulus("data_table", "Recurring deposit accounts opened at four post offices, 2025-26",
               "The table shows the number of recurring deposit (RD) accounts opened at four post offices in "
               "2025-26, the percentage of these accounts held by women and the average monthly instalment per "
               "account.\n\n" +
               md_table(["Post office", "RD accounts opened", "Held by women (%)", "Average monthly instalment (₹)"],
                        [[k, a, p, ind(m)] for k, (a, p, m) in RD.items()]),
               {"columns": ["post_office", "rd_accounts", "women_pct", "avg_monthly_instalment_rs"],
                "rows": [[k, a, p, m] for k, (a, p, m) in RD.items()]})
women = {k: a * p // 100 for k, (a, p, m) in RD.items()}
assert all(a * p % 100 == 0 for a, p, m in RD.values())
tot_w, tot = sum(women.values()), sum(a for a, p, m in RD.values())
avg_pct_guess = F(sum(p for a, p, m in RD.values()), 4) * tot / 100
assert tot_w == 966 and tot == 1860 and tot - tot_w == 894 and avg_pct_guess == F(3999, 4)
Q(T, "Table with percentages", I, "How many RD accounts opened at the four post offices together were held by "
  "women?",
  "966", ["894", "1,860", "1,000"],
  "Women's accounts at each office = accounts × women's percentage; add the four results",
  "Rampur 50% of 480 = 240; Sitapur 65% of 360 = 234; Kheda 40% of 600 = 240; Lonar 60% of 420 = 252. Total = 966.",
  ["240 + 234 = 474", "240 + 252 = 492", "474 + 492 = 966"],
  why="894 is the number held by men; 1,860 is all accounts; 1,000 applies the simple average of the four "
      "percentages (53.75%) to the total (999.75, about 1,000), ignoring that the offices differ in size.", secs=60, stim=sid)

ms, mk = 360 * 1500, 600 * 950
g = math.gcd(ms, mk)
assert (ms // g, mk // g) == (18, 19)
Q(T, "Single table", A, "What is the ratio of the total monthly instalments collected on RD accounts at Sitapur to "
  "those collected at Kheda?",
  "18 : 19", ["3 : 5", "30 : 19", "19 : 18"],
  "Total instalments = number of accounts × average instalment",
  "Sitapur: 360 × 1,500 = ₹5,40,000. Kheda: 600 × 950 = ₹5,70,000. Ratio = 540 : 570 = 18 : 19.",
  ["Sitapur = 5,40,000", "Kheda = 5,70,000", "Ratio = 18 : 19"],
  why="3 : 5 compares only the numbers of accounts; 30 : 19 compares only the average instalments; 19 : 18 is the "
      "ratio inverted.", secs=75, stim=sid)

men_avg = F(480 * 1250 - 240 * 1400, 240)
assert men_avg == 1100 and F(1250 + 1400, 2) == 1325 and 1250 - 2 * (1400 - 1250) == 950
Q(T, "Table with percentages", A, "At Rampur, the women's RD accounts had an average monthly instalment of ₹1,400. "
  "What was the average monthly instalment of the men's RD accounts at Rampur?",
  "₹1,100", ["₹1,325", "₹1,250", "₹950"],
  "Total of the group = number × average; men's total = office total − women's total",
  "Rampur: 480 accounts × ₹1,250 = ₹6,00,000 in all. Women: 240 × 1,400 = ₹3,36,000. Men: 240 accounts with "
  "₹2,64,000, an average of ₹1,100.",
  ["Total = 6,00,000", "Women = 3,36,000", "Men = 2,64,000 ÷ 240 = ₹1,100"],
  short="Equal numbers of men and women: men's average = 2 × 1,250 − 1,400 = 1,100.",
  why="₹1,325 averages ₹1,250 and ₹1,400; ₹1,250 is the overall average; ₹950 subtracts twice the women's excess "
      "over the overall average.", secs=80, stim=sid)

# ================================================================ Bar Graph DI (B2 I3 A2): sets of 4 and 3
T = "Bar Graph DI"
RAIN = {"Aster": 420, "Banyan": 365, "Cedar": 510, "Deodar": 295, "Elm": 480, "Fern": 330}
sid = stimulus("chart", "Rainwater harvested by six housing societies, 2026 monsoon",
               "The bar chart shows the rainwater harvested (in thousand litres) by six housing societies of a "
               "township during the 2026 monsoon (values read from the bars).\n\n" +
               md_table(["Society", "Rainwater harvested (thousand litres)"], [[k, v] for k, v in RAIN.items()]),
               {"chart_type": "bar", "x": list(RAIN), "unit": "thousand litres",
                "series": [{"name": "Rainwater harvested", "values": list(RAIN.values())}]})
tot = sum(RAIN.values())
assert tot == 2400 and F(tot, 6) == 400 and F(tot, 5) == 480 and N(F(tot, 7)) == "342.86" and F(510 + 295, 2) == F(805, 2)
Q(T, "Simple bar", B, "What was the average rainwater harvested per society (in thousand litres)?",
  "400", ["480", "342.86", "402.5"],
  "Average = total ÷ number of societies (6)",
  "Total = 420 + 365 + 510 + 295 + 480 + 330 = 2,400. Average = 2,400 ÷ 6 = 400 thousand litres.",
  ["Total = 2,400", "÷ 6 = 400"],
  why="480 divides by 5; 342.86 divides by 7; 402.5 is the mid-point of the highest and lowest bars.", secs=40,
  stim=sid)

above = [k for k, v in RAIN.items() if v > 400]
assert above == ["Aster", "Cedar", "Elm"]
Q(T, "Simple bar", B, "How many societies harvested more rainwater than the average of the six?",
  "3", ["2", "4", "1"],
  "Find the average first (400 thousand litres), then count the bars above it",
  "Average = 400. Aster (420), Cedar (510) and Elm (480) are above it: 3 societies.",
  ["Average = 400", "Above: Aster, Cedar, Elm", "Count = 3"],
  why="2 misses Aster, which is only a little above 400; 4 adds Banyan (365), which is below; 1 counts only the "
      "tallest bar.", secs=45, stim=sid)

assert pct2(F(510 - 295, 295)) == "72.88%" and pct2(F(215, 510)) == "42.16%" and pct2(F(295, 510)) == "57.84%"
assert pct2(F(510, 295)) == "172.88%"
Q(T, "Simple bar", I, "By what percentage was Cedar's harvest more than Deodar's (correct to two decimal places)?",
  "72.88%", ["42.16%", "57.84%", "172.88%"],
  "Percentage more = (difference ÷ the smaller, base value) × 100",
  "Difference = 510 − 295 = 215. 215 ÷ 295 = 72.88%.",
  ["510 − 295 = 215", "215 ÷ 295 = 72.88%"],
  why="42.16% divides the difference by Cedar's harvest; 57.84% is Deodar's harvest as a percentage of Cedar's; "
      "172.88% is Cedar's as a percentage of Deodar's, not the excess.", secs=50, stim=sid)

new = 295 * F(14, 10) + 330 * F(13, 10)
alt = 295 * F(13, 10) + 330 * F(14, 10)
assert new == 842 and pct2(F(new - 625, 625)) == "34.72%" and pct2(F(alt - 625, 625)) == "35.28%"
Q(T, "Simple bar", A, "Next monsoon, Deodar plans to raise its harvest by 40% and Fern by 30%. If both succeed, by "
  "what percentage will their combined harvest rise (correct to two decimal places)?",
  "34.72%", ["35.00%", "35.28%", "70.00%"],
  "The combined rise is a weighted average of 40% and 30%, weighted by this year's harvests",
  "This year: 295 + 330 = 625. Next year: 295 × 1.4 + 330 × 1.3 = 413 + 429 = 842. Rise = 217 ÷ 625 = 34.72%.",
  ["This year = 625", "Next year = 413 + 429 = 842", "217 ÷ 625 = 34.72%"],
  why="35.00% is the simple average of 40% and 30%, ignoring that Fern is larger; 35.28% applies 40% to Fern and "
      "30% to Deodar; 70.00% adds the two percentages.", secs=90, stim=sid)

INS = {"Q1": (240, 160), "Q2": (300, 180), "Q3": (270, 210), "Q4": (330, 190)}
sid = stimulus("chart", "Two-wheeler and car insurance policies renewed by an agency, 2025-26",
               "The grouped bar chart shows the number of two-wheeler and car insurance policies renewed by an "
               "insurance agency in each quarter of 2025-26 (values read from the bars). The average premium is "
               "₹1,800 per two-wheeler policy and ₹9,500 per car policy.\n\n" +
               md_table(["Quarter", "Two-wheeler policies", "Car policies"], [[k, a, b] for k, (a, b) in INS.items()]),
               {"chart_type": "bar", "x": list(INS),
                "series": [{"name": "Two-wheeler policies", "values": [a for a, b in INS.values()]},
                           {"name": "Car policies", "values": [b for a, b in INS.values()]}]})
tw, car = sum(a for a, b in INS.values()), sum(b for a, b in INS.values())
assert (tw, car) == (1140, 740) and pct2(F(car, tw)) == "64.91%" and pct2(F(car, tw + car)) == "39.36%"
assert pct2(F(tw, car)) == "154.05%" and pct2(F(tw, tw + car)) == "60.64%"
Q(T, "Stacked or grouped bar", I, "For the whole year, the number of car policies renewed was what percentage of the "
  "number of two-wheeler policies renewed (correct to two decimal places)?",
  "64.91%", ["39.36%", "154.05%", "60.64%"],
  "'A as a percentage of B' = A ÷ B × 100, with yearly totals",
  "Two-wheeler total = 240 + 300 + 270 + 330 = 1,140. Car total = 160 + 180 + 210 + 190 = 740. 740 ÷ 1,140 = "
  "64.91%.",
  ["Two-wheeler = 1,140", "Car = 740", "740 ÷ 1,140 = 64.91%"],
  why="39.36% divides by all 1,880 policies; 154.05% is the inverse ratio; 60.64% is the two-wheeler share of all "
      "policies.", secs=55, stim=sid)

ratio = {k: F(b, a) for k, (a, b) in INS.items()}
assert unique_max(ratio) == "Q3"
Q(T, "Stacked or grouped bar", I, "In which quarter was the number of car policies, as a fraction of the number of "
  "two-wheeler policies, the highest?",
  "Q3", ["Q1", "Q2", "Q4"],
  "Compare car ÷ two-wheeler for each quarter",
  "Q1: 160/240 = 0.667; Q2: 180/300 = 0.6; Q3: 210/270 = 0.778; Q4: 190/330 = 0.576. Q3 is the highest.",
  ["Q1 0.667, Q2 0.600", "Q3 0.778, Q4 0.576", "Highest: Q3"],
  why="Q1 has the second-highest ratio; Q2 and Q4 have more two-wheeler renewals, which pulls their ratios down "
      "(Q4 has the most two-wheelers and the lowest ratio).", secs=55, stim=sid)

prem = {k: a * 1800 + b * 9500 for k, (a, b) in INS.items()}
assert prem["Q2"] == 2250000 and prem["Q3"] == 2481000 and sum(INS["Q2"]) == sum(INS["Q3"]) == 480
assert pct2(F(prem["Q3"] - prem["Q2"], prem["Q2"])) == "10.27%" and pct2(F(231000, 2481000)) == "9.31%"
assert pct2(F(210 - 180, 180)) == "16.67%"
Q(T, "Stacked or grouped bar", A, "By what percentage was the agency's total premium from renewals in Q3 higher "
  "than in Q2 (correct to two decimal places)?",
  "10.27%", ["0.00%", "16.67%", "9.31%"],
  "Premium = policies × average premium for each type; the two types carry very different premiums",
  "Q2: 300 × 1,800 + 180 × 9,500 = 5,40,000 + 17,10,000 = ₹22,50,000. Q3: 270 × 1,800 + 210 × 9,500 = 4,86,000 + "
  "19,95,000 = ₹24,81,000. Rise = 2,31,000 ÷ 22,50,000 = 10.27%.",
  ["Q2 premium = 22,50,000", "Q3 premium = 24,81,000", "2,31,000 ÷ 22,50,000 = 10.27%"],
  why="0.00% compares the number of policies (480 in each quarter), ignoring the premiums; 16.67% compares only the "
      "car policies; 9.31% divides the rise by Q3's premium.", secs=100, stim=sid)

# ================================================================ Pie Chart DI (B2 I3 A1): one set of 6
T = "Pie Chart DI"
CALLS = {"Card blocking": 54, "Net banking": 72, "Loan queries": 45, "Account statements": 63, "UPI disputes": 81,
         "KYC updates": 27, "Others": 18}
assert sum(CALLS.values()) == 360
TOTC = 48000
sid = stimulus("chart", "Calls to a bank's customer-care centre by query type, October 2026 (central angles)",
               "The pie chart shows how the 48,000 calls received by a bank's customer-care centre in October 2026 "
               "were divided by type of query; the central angle of each sector is given.\n\n" +
               md_table(["Query type", "Central angle (degrees)"], [[k, v] for k, v in CALLS.items()]),
               {"chart_type": "pie", "unit": "degrees", "labels": list(CALLS), "values": list(CALLS.values()),
                "total_calls": TOTC})
nc = {k: TOTC * v // 360 for k, v in CALLS.items()}
assert all(TOTC * v % 360 == 0 for v in CALLS.values())
assert nc["UPI disputes"] == 10800 and nc["Net banking"] == 9600 and nc["Card blocking"] == 7200
Q(T, "Degree-based", B, "How many calls were about UPI disputes?",
  "10,800", ["9,600", "8,100", "7,200"],
  "Calls = central angle ÷ 360 × total calls",
  "UPI disputes: 81/360 × 48,000 = 10,800 calls.",
  ["81 ÷ 360 = 0.225", "0.225 × 48,000 = 10,800"],
  why="9,600 is the net-banking figure (72°); 8,100 reads the angle as hundreds of calls; 7,200 is the "
      "card-blocking figure (54°).", secs=35, stim=sid)

assert F(45, 360) * 100 == F(25, 2) and F(54, 360) * 100 == 15 and F(27, 360) * 100 == F(15, 2)
Q(T, "Degree-based", B, "What percentage of the calls were loan queries?",
  "12.5%", ["45%", "15%", "7.5%"],
  "Percentage = central angle ÷ 360 × 100",
  "Loan queries: 45 ÷ 360 × 100 = 12.5%.",
  ["45 ÷ 360 = 0.125", "= 12.5%"],
  why="45% reads the angle as a percentage; 15% is card blocking (54°); 7.5% is KYC updates (27°).", secs=30,
  stim=sid)

d_ = nc["Card blocking"] + nc["KYC updates"] - nc["Others"]
assert d_ == 8400 and nc["Card blocking"] + nc["KYC updates"] == 10800 and 63 * 100 == 6300
Q(T, "Degree-based", I, "By how many calls did the card-blocking and KYC-update calls together exceed the calls "
  "under 'Others'?",
  "8,400", ["10,800", "7,200", "6,300"],
  "Work with angles first: (54 + 27 − 18)° = 63°, then convert once",
  "(54 + 27 − 18) = 63°. 63/360 × 48,000 = 8,400 calls.",
  ["54 + 27 = 81°", "81 − 18 = 63°", "63/360 × 48,000 = 8,400"],
  why="10,800 forgets to subtract 'Others'; 7,200 is the card-blocking figure alone; 6,300 reads 63° as hundreds of "
      "calls.", secs=50, stim=sid)

g = math.gcd(72, 63)
assert (72 // g, 63 // g) == (8, 7)
Q(T, "Degree-based", I, "What is the ratio of net-banking calls to account-statement calls?",
  "8 : 7", ["7 : 8", "9 : 7", "6 : 7"],
  "Sectors of the same pie are in the ratio of their angles",
  "72° : 63° = 8 : 7.",
  ["72 : 63", "÷ 9 ⇒ 8 : 7"],
  why="7 : 8 is inverted; 9 : 7 uses the UPI angle (81°) in place of net banking; 6 : 7 uses the card-blocking "
      "angle (54°).", secs=35, stim=sid)

mins = nc["UPI disputes"] * 6 + nc["Card blocking"] * F(5, 2)
assert mins == 82800 and mins / 60 == 1380 and nc["UPI disputes"] * 6 / 60 == 1080
assert 18000 * F(17, 4) / 60 == 1275 and nc["Card blocking"] * F(5, 2) / 60 == 300
Q(T, "Degree-based", I, "An agent spends on average 6 minutes on a UPI-dispute call and 2½ minutes on a "
  "card-blocking call. How many hours in all were spent on these two types of call in October?",
  "1,380 hours", ["1,080 hours", "1,275 hours", "300 hours"],
  "Hours = (number of calls × minutes per call) ÷ 60 for each type",
  "UPI: 10,800 × 6 = 64,800 min. Card blocking: 7,200 × 2.5 = 18,000 min. Total = 82,800 min = 1,380 hours.",
  ["UPI: 64,800 min", "Card: 18,000 min", "82,800 ÷ 60 = 1,380 h"],
  why="1,080 hours counts only the UPI calls; 1,275 hours uses the average of 6 and 2½ minutes for all 18,000 calls; "
      "300 hours counts only card blocking.", secs=70, stim=sid)

nov_tot, nov_upi = TOTC * F(9, 8), nc["UPI disputes"] * F(5, 4)
ang = nov_upi / nov_tot * 360
assert ang == 90 and 81 * F(5, 4) == F(405, 4) and 81 / F(9, 8) == 72
Q(T, "Degree-based", A, "In November, the total number of calls rose by 12.5% and the number of UPI-dispute calls "
  "rose by 25%. What was the central angle of the UPI-dispute sector in November's pie chart?",
  "90°", ["101.25°", "72°", "81°"],
  "New angle = new UPI calls ÷ new total × 360",
  "November total = 48,000 × 1.125 = 54,000. UPI calls = 10,800 × 1.25 = 13,500. Angle = 13,500/54,000 × 360 = "
  "90°.",
  ["Total = 54,000", "UPI = 13,500", "13,500/54,000 × 360 = 90°"],
  short="81° × 1.25 ÷ 1.125 = 90°.",
  why="101.25° raises the angle by 25% but forgets that the total grew too; 72° divides the old angle by 1.125 "
      "without raising the UPI calls; 81° assumes the share is unchanged.", secs=90, stim=sid)

# ================================================================ Line Graph DI (B3 I2 A1): one set of 6
T = "Line Graph DI"
SIP = {"Jan": (420, 90), "Feb": (380, 110), "Mar": (510, 120), "Apr": (460, 85), "May": (540, 140),
       "Jun": (600, 130)}
sid = stimulus("chart", "New and cancelled SIP registrations at a mutual fund branch, January to June 2026",
               "The line graph shows the number of new systematic investment plan (SIP) registrations and the "
               "number of SIP cancellations at a mutual fund's city branch in each month from January to June 2026 "
               "(values read from the graph). Net addition = new registrations − cancellations.\n\n" +
               md_table(["Month", "New SIPs", "Cancellations"], [[k, a, b] for k, (a, b) in SIP.items()]),
               {"chart_type": "line", "x": list(SIP),
                "series": [{"name": "New SIPs", "values": [a for a, b in SIP.values()]},
                           {"name": "Cancellations", "values": [b for a, b in SIP.values()]}]})
new_t, can_t = sum(a for a, b in SIP.values()), sum(b for a, b in SIP.values())
assert (new_t, can_t) == (2910, 675) and new_t - can_t == 2235 and new_t - 420 == 2490
Q(T, "Multiple lines", B, "How many new SIPs were registered from January to June in all?",
  "2,910", ["675", "2,235", "2,490"],
  "Add the six points of the 'New SIPs' line",
  "420 + 380 + 510 + 460 + 540 + 600 = 2,910.",
  ["420 + 380 + 510 = 1,310", "460 + 540 + 600 = 1,600", "1,310 + 1,600 = 2,910"],
  why="675 is the total of cancellations; 2,235 is the net addition; 2,490 leaves out January.", secs=35, stim=sid)

net = {k: a - b for k, (a, b) in SIP.items()}
assert unique_min(net) == "Feb" and net == {"Jan": 330, "Feb": 270, "Mar": 390, "Apr": 375, "May": 400, "Jun": 470}
assert unique_min({k: b for k, (a, b) in SIP.items()}) == "Apr"
Q(T, "Multiple lines", B, "In which month was the net addition of SIPs the lowest?",
  "February", ["January", "April", "March"],
  "Net addition = new − cancellations for each month",
  "Net: Jan 330, Feb 270, Mar 390, Apr 375, May 400, Jun 470. February is the lowest.",
  ["Jan 330, Feb 270, Mar 390", "Apr 375, May 400, Jun 470", "Lowest: February"],
  why="January (330) is the second-lowest; April has the fewest cancellations, not the lowest net addition; March "
      "has the most cancellations in the first quarter but a high net addition.", secs=45, stim=sid)

assert pct2(F(140, 540)) == "25.93%" and pct2(F(140, 680)) == "20.59%" and pct2(F(540, 140)) == "385.71%"
assert pct2(F(400, 540)) == "74.07%"
Q(T, "Multiple lines", B, "In May, cancellations were what percentage of new registrations (correct to two decimal "
  "places)?",
  "25.93%", ["20.59%", "385.71%", "74.07%"],
  "'A as a percentage of B' = A ÷ B × 100",
  "May: 140 cancellations, 540 new SIPs. 140 ÷ 540 = 25.93%.",
  ["140 ÷ 540", "= 25.93%"],
  why="20.59% divides by new + cancelled (680); 385.71% is the inverse; 74.07% is the net addition as a share of "
      "new SIPs.", secs=40, stim=sid)

assert pct2(F(600 - 380, 380)) == "57.89%" and pct2(F(220, 600)) == "36.67%" and pct2(F(600, 380)) == "157.89%"
assert pct2(F(470 - 270, 270)) == "74.07%"
Q(T, "Single line", I, "By what percentage did new SIP registrations rise from February to June (correct to two "
  "decimal places)?",
  "57.89%", ["36.67%", "157.89%", "74.07%"],
  "Percentage rise = (later − earlier) ÷ earlier × 100",
  "February 380, June 600. Rise = 220 ÷ 380 = 57.89%.",
  ["600 − 380 = 220", "220 ÷ 380 = 57.89%"],
  why="36.67% divides by June's figure; 157.89% is June as a percentage of February; 74.07% is the rise in net "
      "additions (270 to 470), not in new registrations.", secs=45, stim=sid)

assert F(can_t, 6) == F(225, 2) and F(can_t, 5) == 135 and N(F(can_t, 7)) == "96.43" and F(90 + 130, 2) == 110
Q(T, "Single line", I, "What was the average number of SIP cancellations per month from January to June?",
  "112.5", ["135", "96.43", "110"],
  "Average = total cancellations ÷ 6 months",
  "Cancellations = 90 + 110 + 120 + 85 + 140 + 130 = 675. Average = 675 ÷ 6 = 112.5.",
  ["Total = 675", "÷ 6 = 112.5"],
  why="135 divides by 5; 96.43 divides by 7; 110 averages only the first and last months "
      "(90 and 130).", secs=45, stim=sid)

q1n = sum(net[m] for m in ("Jan", "Feb", "Mar"))
q2n = sum(net[m] for m in ("Apr", "May", "Jun"))
assert (q1n, q2n) == (990, 1245) and pct2(F(q2n - q1n, q1n)) == "25.76%" and pct2(F(255, 1245)) == "20.48%"
assert pct2(F(1600 - 1310, 1310)) == "22.14%" and pct2(F(355 - 320, 320)) == "10.94%"
Q(T, "Multiple lines", A, "By what percentage was the net addition of SIPs in April–June higher than in "
  "January–March (correct to two decimal places)?",
  "25.76%", ["20.48%", "22.14%", "10.94%"],
  "Net addition for each quarter = Σ new − Σ cancellations; then the percentage rise",
  "January–March: (420 + 380 + 510) − (90 + 110 + 120) = 1,310 − 320 = 990. April–June: 1,600 − 355 = 1,245. Rise = "
  "255 ÷ 990 = 25.76%.",
  ["Jan–Mar net = 990", "Apr–Jun net = 1,245", "255 ÷ 990 = 25.76%"],
  why="20.48% divides the rise by the April–June figure; 22.14% compares only new registrations (1,310 to 1,600); "
      "10.94% compares only cancellations (320 to 355).", secs=90, stim=sid)

# ================================================================ Caselet DI (B1 I4 A6): sets of 6 and 5
T = "Caselet DI"
STAFF = {"Officers": (108, 36, 72000), "Clerks": (96, 60, 42000), "Sub-staff": (36, 9, 28000)}
assert sum(v[0] for v in STAFF.values()) == 240 and 108 == 240 * 45 // 100 and 96 == 240 * 40 // 100
assert 36 == 108 // 3 and 60 == 96 * 5 // 8 and 9 == 36 // 4
sid = stimulus("passage", "Staff of a bank's regional office by cadre and gender, October 2026",
               "A bank's regional office has 240 employees in three cadres: officers, clerks and sub-staff. Officers "
               "make up 45% of the staff and clerks 40%; the rest are sub-staff. One-third of the officers, "
               "five-eighths of the clerks and one-fourth of the sub-staff are women. Thirty of the officers work in "
               "the credit department, and 12 of these 30 are women. The average monthly salary is ₹72,000 for an "
               "officer, ₹42,000 for a clerk and ₹28,000 for a member of the sub-staff.")
Q(T, "Paragraph data", B, "How many of the clerks are men?",
  "36", ["60", "96", "48"],
  "Clerks = 40% of 240; men = clerks − women clerks",
  "Clerks = 40% of 240 = 96. Women clerks = 5/8 × 96 = 60. Men clerks = 96 − 60 = 36.",
  ["Clerks = 96", "Women clerks = 60", "Men clerks = 36"],
  why="60 is the number of women clerks; 96 is all clerks; 48 assumes clerks are split equally.", secs=40, stim=sid)

women = sum(v[1] for v in STAFF.values())
assert women == 105 and pct2(F(women, 240)) == "43.75%" and pct2(F(135, 240)) == "56.25%"
assert pct2((F(1, 3) + F(5, 8) + F(1, 4)) / 3) == "40.28%"
Q(T, "Paragraph data", I, "What percentage of all the employees are women?",
  "43.75%", ["56.25%", "40.28%", "45.00%"],
  "Find the women in each cadre, add, then divide by 240",
  "Women: officers 36, clerks 60, sub-staff 9 = 105. 105 ÷ 240 = 43.75%.",
  ["36 + 60 + 9 = 105", "105 ÷ 240 = 43.75%"],
  why="56.25% is the share of men; 40.28% averages the three fractions (1/3, 5/8, 1/4) without weighting by cadre "
      "size; 45.00% is the officers' share of the staff.", secs=55, stim=sid)

assert F(36, 9) == 4 and F(108, 36) == 3
Q(T, "Paragraph data", I, "What is the ratio of women officers to women in the sub-staff?",
  "4 : 1", ["3 : 1", "1 : 4", "4 : 3"],
  "Women officers = 1/3 of 108; women sub-staff = 1/4 of 36",
  "Women officers = 36; sub-staff = 240 − 108 − 96 = 36, of whom one-fourth = 9 are women. Ratio = 36 : 9 = 4 : 1.",
  ["Women officers = 36", "Sub-staff = 36, women = 9", "36 : 9 = 4 : 1"],
  why="3 : 1 compares all officers with all sub-staff (108 : 36); 1 : 4 is inverted; 4 : 3 compares the fractions "
      "1/3 and 1/4 instead of the numbers of women.", secs=50, stim=sid)

men_off = 108 - 36
assert men_off - (30 - 12) == 54 and 108 - 30 == 78 and men_off - 12 == 60
Q(T, "Paragraph data", A, "How many men officers work outside the credit department?",
  "54", ["78", "60", "72"],
  "Men officers in all − men officers in credit (30 − 12)",
  "Men officers = 108 − 36 = 72. Men officers in credit = 30 − 12 = 18. Outside credit: 72 − 18 = 54.",
  ["Men officers = 72", "Men in credit = 18", "72 − 18 = 54"],
  why="78 is all officers (men and women) outside credit; 60 subtracts the 12 women in credit from the men; 72 is "
      "all men officers.", secs=70, stim=sid)

assert pct2(F(125, 260)) == "48.08%" and pct2(F(125, 240)) == "52.08%" and pct2(F(120, 260)) == "46.15%"
Q(T, "Paragraph data", A, "If 20 more women clerks join and nobody leaves, what percentage of the staff will be "
  "women (correct to two decimal places)?",
  "48.08%", ["52.08%", "46.15%", "43.75%"],
  "Both the number of women and the total staff rise by 20",
  "Women become 105 + 20 = 125 and the staff 240 + 20 = 260. 125 ÷ 260 = 48.08%.",
  ["Women = 125", "Staff = 260", "125 ÷ 260 = 48.08%"],
  why="52.08% keeps the total at 240; 46.15% adds only 15 women; 43.75% is the present share.", secs=70, stim=sid)

pay = sum(n * s for n, w, s in STAFF.values())
assert pay == 12816000 and F(pay, 240) == 53400 and r2(F(72000 + 42000 + 28000, 3)) == F("47333.33")
assert F(72000 + 42000, 2) == 57000
Q(T, "Paragraph data", A, "What is the average monthly salary of all 240 employees?",
  "₹53,400", ["₹47,333.33", "₹57,000", "₹51,900"],
  "Weighted average: Σ(number × salary) ÷ 240",
  "Officers 108 × 72,000 = 77,76,000; clerks 96 × 42,000 = 40,32,000; sub-staff 36 × 28,000 = 10,08,000. Total = "
  "1,28,16,000. Average = 1,28,16,000 ÷ 240 = ₹53,400.",
  ["Officers: 77,76,000", "Clerks: 40,32,000", "Sub-staff: 10,08,000", "1,28,16,000 ÷ 240 = 53,400"],
  why="₹47,333.33 is the simple average of the three salaries; ₹57,000 ignores the sub-staff; ₹51,900 swaps the "
      "officers' and clerks' shares (40% and 45%).", secs=90, stim=sid)
assert 72000 * F(40, 100) + 42000 * F(45, 100) + 28000 * F(15, 100) == 51900

CAB = {"Airport": (600, 650, F(20, 100)), "Intercity": (300, 2400, F(15, 100)), "Local": (1500, 180, F(20, 100))}
assert sum(v[0] for v in CAB.values()) == 2400 and 600 == 2400 // 4 and 300 == 2400 // 8
sid = stimulus("passage", "Rides booked through a cab aggregator in a city on one Sunday",
               "On one Sunday, 2,400 rides were booked through a cab aggregator in a city. One-fourth of the rides were "
               "airport rides and one-eighth were intercity rides; the rest were local rides. The average fare was "
               "₹650 for an airport ride, ₹2,400 for an intercity ride and ₹180 for a local ride. The aggregator "
               "keeps a commission of 20% of the fare on airport and local rides and 15% on intercity rides; the "
               "rest of the fare goes to the driver.")
fare = {k: n * f for k, (n, f, c) in CAB.items()}
tf = sum(fare.values())
assert fare == {"Airport": 390000, "Intercity": 720000, "Local": 270000} and tf == 1380000
assert F(650 + 2400 + 180, 3) * 2400 == 2584000 and tf - 270000 == 1110000 and tf - 390000 == 990000
Q(T, "Paragraph data", I, "What was the total fare paid for all the rides on that Sunday?",
  "₹13,80,000", ["₹25,84,000", "₹11,10,000", "₹9,90,000"],
  "Rides of each kind × average fare, then add",
  "Airport 600 × 650 = 3,90,000; intercity 300 × 2,400 = 7,20,000; local 1,500 × 180 = 2,70,000. Total = "
  "₹13,80,000.",
  ["Airport: 3,90,000", "Intercity: 7,20,000", "Local: 2,70,000", "Total = 13,80,000"],
  why="₹25,84,000 applies the simple average of the three fares to all 2,400 rides; ₹11,10,000 leaves out the "
      "local rides; ₹9,90,000 leaves out the airport rides.", secs=60, stim=sid)

assert pct2(F(720000, tf)) == "52.17%" and pct2(F(660000, tf)) == "47.83%" and pct2(F(720000, 660000)) == "109.09%"
Q(T, "Paragraph data", I, "Intercity rides made up what percentage of the total fare (correct to two decimal "
  "places)?",
  "52.17%", ["12.50%", "47.83%", "109.09%"],
  "Share of fare = intercity fare ÷ total fare × 100",
  "Intercity fare = ₹7,20,000 of ₹13,80,000: 7,20,000 ÷ 13,80,000 = 52.17%.",
  ["Intercity = 7,20,000", "Total = 13,80,000", "52.17%"],
  why="12.50% is the intercity share of the number of rides; 47.83% is the share of the other two kinds; 109.09% "
      "compares intercity fare with the other two kinds' fare.", secs=55, stim=sid)

comm = sum(fare[k] * c for k, (n, f, c) in CAB.items())
assert comm == 240000 and tf * F(20, 100) == 276000 and tf * F(15, 100) == 207000 and comm - 108000 == 132000
Q(T, "Paragraph data", A, "How much did the aggregator earn in commission on that Sunday?",
  "₹2,40,000", ["₹2,76,000", "₹2,07,000", "₹1,32,000"],
  "Apply each kind's commission rate to its own fare total",
  "20% of (3,90,000 + 2,70,000) = 1,32,000; 15% of 7,20,000 = 1,08,000. Total = ₹2,40,000.",
  ["Airport + local fare = 6,60,000 ⇒ 1,32,000", "Intercity: 15% of 7,20,000 = 1,08,000", "Total = 2,40,000"],
  why="₹2,76,000 takes 20% of every fare; ₹2,07,000 takes 15% of every fare; ₹1,32,000 leaves out the intercity "
      "commission.", secs=80, stim=sid)

drv = tf - comm
per = {k: f * (1 - c) for k, (n, f, c) in CAB.items()}
assert F(drv, 2400) == 475 and F(tf, 2400) == 575 and r2(sum(per.values()) / 3) == F("901.33") and F(comm, 2400) == 100
Q(T, "Paragraph data", A, "On average, how much did a driver receive per ride, after the commission?",
  "₹475", ["₹575", "₹901.33", "₹100"],
  "Drivers' total = total fare − commission; divide by all 2,400 rides",
  "Drivers received 13,80,000 − 2,40,000 = ₹11,40,000 for 2,400 rides: ₹475 per ride.",
  ["Drivers' total = 11,40,000", "÷ 2,400 = 475"],
  why="₹575 is the average fare before commission; ₹901.33 averages the three per-ride amounts (520, 2,040 and 144) "
      "without weighting by the number of rides; ₹100 is the average commission per ride.", secs=80, stim=sid)

new_tf = 720 * 650 + 300 * 2400 + 1350 * 180
assert new_tf == 1431000 and pct2(F(new_tf - tf, tf)) == "3.70%" and pct2(F(30, 2400)) == "1.25%"
assert pct2(F(51000, 660000)) == "7.73%"
Q(T, "Paragraph data", A, "On the next Sunday, airport rides rose by 20% and local rides fell by 10%; intercity "
  "rides and all fares were unchanged. By what percentage did the total fare change?",
  "Increase of 3.70%", ["Decrease of 1.25%", "Increase of 10.00%", "Increase of 7.73%"],
  "Find the change in each kind's fare total and compare with the old total of ₹13,80,000",
  "Airport fare rises by 20% of 3,90,000 = 78,000; local fare falls by 10% of 2,70,000 = 27,000. Net change = "
  "+51,000. 51,000 ÷ 13,80,000 = 3.70% increase.",
  ["Airport: +78,000", "Local: −27,000", "Net +51,000 ÷ 13,80,000 = +3.70%"],
  why="'Decrease of 1.25%' compares the number of rides (+120 − 150 = −30 of 2,400); 'increase of 10.00%' simply "
      "subtracts the percentages; 'increase of 7.73%' leaves the intercity fare out of the base.", secs=100,
  stim=sid)

# ================================================================ Missing DI (B2 I2 A1): one set of 5
T = "Missing DI"
BAT = {"Arjun": (18, 2, 640, F(40), 800, F(80)), "Bhavesh": (15, 3, 504, F(42), 630, F(80)),
       "Chetan": (20, 4, 560, F(35), 640, F(175, 2)), "Dinesh": (16, 1, 450, F(30), 500, F(90)),
       "Eshan": (12, 0, 342, F(57, 2), 450, F(76))}
for k, (inn, no, runs, avg, balls, sr) in BAT.items():
    assert F(runs, inn - no) == avg and F(runs * 100, balls) == sr, k
HIDE = {("Arjun", 4), ("Bhavesh", 1), ("Bhavesh", 5), ("Chetan", 2), ("Chetan", 5), ("Dinesh", 0), ("Dinesh", 5),
        ("Eshan", 2), ("Eshan", 4)}
shown = []
for k, row in BAT.items():
    shown.append([k] + ["—" if (k, i) in HIDE else N(x) for i, x in enumerate(row)])
sid = stimulus("data_table", "Five batsmen of a club cricket team, 2026 season (some values missing)",
               "The table gives, for five batsmen of a club team in the 2026 season, the innings played, the number "
               "of times not out, runs scored, batting average, balls faced and strike rate. Some values are missing "
               "(—). Batting average = runs ÷ (innings − not outs); strike rate = runs ÷ balls faced × 100.\n\n" +
               md_table(["Batsman", "Innings", "Not out", "Runs", "Average", "Balls faced", "Strike rate"], shown),
               {"columns": ["batsman", "innings", "not_outs", "runs", "average", "balls_faced", "strike_rate"],
                "rows": [[r[0]] + [None if c == "—" else float(c.replace(",", "")) for c in r[1:]] for r in shown]})
assert F(504, 42) == 12 and 15 - 12 == 3
Q(T, "Table with missing values", B, "How many times was Bhavesh not out?",
  "3", ["12", "15", "2"],
  "Dismissals = runs ÷ average; not outs = innings − dismissals",
  "Dismissals = 504 ÷ 42 = 12. Not outs = 15 − 12 = 3.",
  ["504 ÷ 42 = 12 dismissals", "15 − 12 = 3"],
  why="12 is the number of dismissals; 15 is the number of innings; 2 copies Arjun's not-out figure.", secs=35,
  stim=sid)

assert F(640 * 100, 80) == 800 and 640 * F(80, 100) == 512
Q(T, "Table with missing values", B, "How many balls did Arjun face?",
  "800", ["512", "640", "8,000"],
  "Balls faced = runs ÷ strike rate × 100",
  "Balls = 640 ÷ 80 × 100 = 800.",
  ["640 ÷ 80 = 8", "8 × 100 = 800"],
  why="512 multiplies the runs by 0.80 instead of dividing; 640 takes balls equal to runs (a strike rate of 100); "
      "8,000 slips a factor of 10.", secs=35, stim=sid)

assert r2(F(700 * 100, 640)) == F("109.38") and r2(F(640 * 100, 560)) == F("114.29")
Q(T, "Table with missing values", I, "What was Chetan's strike rate?",
  "87.5", ["109.38", "114.29", "80"],
  "Runs = average × dismissals; strike rate = runs ÷ balls × 100",
  "Dismissals = 20 − 4 = 16, so runs = 35 × 16 = 560. Strike rate = 560 ÷ 640 × 100 = 87.5.",
  ["Dismissals = 16", "Runs = 560", "560 ÷ 640 × 100 = 87.5"],
  why="109.38 takes runs as 35 × 20 = 700, forgetting the not outs; 114.29 divides balls by runs; 80 copies the "
      "strike rate of Arjun and Bhavesh.", secs=55, stim=sid)

runs_t = sum(v[2] for v in BAT.values())
assert runs_t == 2496 and runs_t + 140 == 2636 and runs_t - 342 == 2154 and runs_t - 560 == 1936
Q(T, "Table with missing values", I, "How many runs did the five batsmen score in all?",
  "2,496", ["2,636", "2,154", "1,936"],
  "Fill in the missing runs (Chetan, Eshan) from average × dismissals, then add",
  "Chetan = 35 × 16 = 560; Eshan = 28.5 × 12 = 342 (never out). Total = 640 + 504 + 560 + 450 + 342 = 2,496.",
  ["Chetan 560, Eshan 342", "640 + 504 + 450 = 1,594", "1,594 + 560 + 342 = 2,496"],
  why="2,636 takes Chetan's runs as 35 × 20 = 700; 2,154 leaves out Eshan; 1,936 leaves out Chetan.", secs=60,
  stim=sid)

x_ = 32 * (15 + 1) - 450
assert x_ == 62 and 32 * 17 - 450 == 94
Q(T, "Table with missing values", A, "In his next innings Dinesh is out, and his batting average becomes exactly 32. "
  "How many runs did he score in that innings?",
  "62", ["94", "32", "512"],
  "New runs total = new average × new number of dismissals",
  "Dinesh: innings = 450 ÷ 30 + 1 = 16 (15 dismissals, 1 not out). After being out once more he has 16 dismissals; "
  "an average of 32 needs 32 × 16 = 512 runs. Runs in that innings = 512 − 450 = 62.",
  ["Dismissals now = 15", "After: 16 dismissals, total 512", "512 − 450 = 62"],
  why="94 divides by 17 innings instead of 16 dismissals (32 × 17 − 450); 32 is the new average itself; 512 is the "
      "new career total.", secs=90, stim=sid)

# ================================================================ Quantity Comparison (B2 I5 A3)
assert F(25 * 18, 5) == 90 and 51 * F(5, 3) == 85
qc("Arithmetic-based comparison", B, "A speed of 25 m/s expressed in km/h",
   "The distance (km) covered in 1 hour 40 minutes at 51 km/h", [F(90)], [F(85)], ">", ["<", "<="],
   "1 m/s = 18/5 km/h; distance = speed × time",
   "Quantity I: 25 × 18/5 = 90 km/h. Quantity II: 51 × 5/3 = 85 km. 90 > 85.",
   ["I: 25 × 3.6 = 90", "II: 51 × 1⅔ = 85", "90 > 85"],
   why="'I < II' and 'I ≤ II' come from converting with 5/18 (25 m/s ≈ 6.9) or taking 1 h 40 min as 1.4 hours "
       "(71.4 km) and then mis-comparing.", secs=45)

assert 9 ** 3 == 729 and 32 * 24 == 768
qc("Quantity I vs II", B, "Volume (cm³) of a cube of edge 9 cm", "Area (cm²) of a rectangle measuring 32 cm × 24 cm",
   [F(729)], [F(768)], "<", [">", ">="],
   "Volume of a cube = a³; area of a rectangle = l × b",
   "Quantity I: 9³ = 729. Quantity II: 32 × 24 = 768. 729 < 768.",
   ["I: 729", "II: 768", "729 < 768"],
   why="'I > II' and 'I ≥ II' come from using 9 × 9 × 10 = 810 for the cube or 32 × 22 for the rectangle.", secs=40)

p1 = prob(DECK, lambda c: c[1] == "S" or c[0] == 1)
p2 = prob(DICE2, lambda w: sum(w) > 8)
assert p1 == F(4, 13) and p2 == F(5, 18)
qc("Arithmetic-based comparison", I, "The probability that a card drawn at random from a pack of 52 is a spade or an "
   "ace", "The probability that the total is greater than 8 when two fair dice are rolled", [p1], [p2], ">",
   ["<", "<="],
   "Count favourable outcomes; do not double-count the ace of spades",
   "Quantity I: 13 spades + 3 other aces = 16/52 = 4/13 ≈ 0.308. Quantity II: totals 9 to 12 occur 4 + 3 + 2 + 1 = "
   "10 ways of 36 = 5/18 ≈ 0.278. Quantity I > Quantity II.",
   ["I: 16/52 = 0.308", "II: 10/36 = 0.278", "I > II"],
   why="'I < II' and 'I ≤ II' come from counting only 13 spades for I (0.25) or counting totals of 8 and more for "
       "II (15/36 ≈ 0.417).", secs=70, by=BRUTE)

sol = [(x, y) for x in range(-20, 21) for y in range(-20, 21) if 2 * x + 3 * y == 23 and 3 * x - y == 7]
assert sol == [(4, 5)]
qc("Quantity I vs II", I, "The value of x, where 2x + 3y = 23 and 3x − y = 7",
   "The value of y, where 2x + 3y = 23 and 3x − y = 7", [F(4)], [F(5)], "<", [">", ">="],
   "Solve the pair of linear equations",
   "From 3x − y = 7, y = 3x − 7. Then 2x + 9x − 21 = 23, so 11x = 44, x = 4 and y = 5. Quantity I < Quantity II.",
   ["y = 3x − 7", "11x = 44 ⇒ x = 4", "y = 5", "4 < 5"],
   why="'I > II' and 'I ≥ II' come from swapping the values of x and y after solving.",
   secs=55, by=BRUTE)

assert 1 / (F(1, 20) + F(1, 30)) == 12 and F(195, F(54 * 5, 18)) == 13
qc("Arithmetic-based comparison", I, "Time (minutes) taken by two pipes that fill a tank alone in 20 minutes and 30 "
   "minutes to fill it together",
   "Time (seconds) taken by a 195 m long train running at 54 km/h to pass a signal pole", [F(12)], [F(13)], "<",
   [">", ">="],
   "Together: 1 ÷ (1/20 + 1/30); time to pass a pole = length ÷ speed in m/s",
   "Quantity I: 1/20 + 1/30 = 1/12, so 12 minutes. Quantity II: 54 km/h = 15 m/s, 195 ÷ 15 = 13 seconds. 12 < 13.",
   ["I: 12", "II: 195 ÷ 15 = 13", "12 < 13"],
   why="'I > II' and 'I ≥ II' come from averaging the pipe times (25) or using 54 km/h as 18 m/s (10.8 s).",
   secs=55)

ms_ = [m for m in range(-50, 50) if m * m - 30 * m + 200 < 0]
assert ms_ == list(range(11, 20)) and 6 * 3 // 2 == 9
qc("Quantity I vs II", I, "The number of diagonals of a hexagon",
   "An integer m for which m² − 30m + 200 < 0", [F(9)], [F(m) for m in ms_], "<", [">", ">="],
   "Diagonals of an n-gon = n(n − 3)/2; a quadratic is negative between its roots",
   "Quantity I: 6 × 3 ÷ 2 = 9. Quantity II: m² − 30m + 200 = (m − 10)(m − 20) < 0 for 10 < m < 20, so m is 11 to 19. "
   "Every possible m exceeds 9: Quantity I < Quantity II.",
   ["I: 9", "II: 10 < m < 20 ⇒ m ∈ {11, …, 19}", "9 < every m"],
   why="'I > II' and 'I ≥ II' come from counting a hexagon's diagonals as 6 × 5 ÷ 2 = 15 (that counts the sides "
       "too) or from taking m outside the roots.", secs=70, by=BRUTE)

avg_rt = F(15 * 15 - 3 * 3, 15)
assert avg_rt == F(72, 5) and F(35, F(5, 2)) == 14
qc("Arithmetic-based comparison", I, "Average speed (km/h) for the round trip of a boat that goes 24 km downstream and "
   "back, if its speed in still water is 15 km/h and the stream flows at 3 km/h",
   "Speed (km/h) of a cyclist who covers 35 km in 2½ hours", [avg_rt], [F(14)], ">", ["<", "<="],
   "Round-trip average = 2d ÷ (d/(b + s) + d/(b − s)) = (b² − s²)/b",
   "Quantity I: 24/18 + 24/12 = 1⅓ + 2 = 3⅓ h for 48 km, i.e. 14.4 km/h. Quantity II: 35 ÷ 2.5 = 14 km/h. "
   "14.4 > 14.",
   ["I: 48 ÷ 3⅓ = 14.4", "II: 14", "14.4 > 14"],
   why="'I < II' and 'I ≤ II' come from taking the round-trip average as (18 + 12)/2 − 3 = 12, or as the "
       "upstream speed 12.", secs=70)

p1 = prob(list(itertools.product("BG", repeat=4)), lambda s: s.count("G") == 2)
p2 = F(sum(1 for n in range(1, 31) if n > 1 and all(n % d for d in range(2, n))), 30)
assert p1 == F(3, 8) and p2 == F(1, 3)
qc("Arithmetic-based comparison", A, "The probability that a family of four children has exactly two girls (each "
   "child equally likely to be a boy or a girl)",
   "The probability that a number chosen at random from 1 to 30 is prime", [p1], [p2], ">", ["<", "<="],
   "Binomial count C(4, 2) of 16; there are 10 primes up to 30",
   "Quantity I: C(4, 2)/2⁴ = 6/16 = 0.375. Quantity II: primes 2, 3, 5, 7, 11, 13, 17, 19, 23, 29 = 10 of 30 = 0.333. "
   "Quantity I > Quantity II.",
   ["I: 6/16 = 0.375", "II: 10/30 = 0.333", "I > II"],
   why="'I < II' and 'I ≤ II' come from treating 'two girls' as one of five equally likely outcomes (0 to 4 "
       "girls), which gives 0.2.", secs=80, by=BRUTE)

r_ = [r for r in range(1, 20) if F(4, 3) * r ** 3 == 4 * r * r]
h_ = [h for h in range(1, 20) if F(1, 3) * 9 * h == 12]
assert r_ == [3] and h_ == [4]
qc("Quantity I vs II", A, "The radius (cm) of a sphere whose volume (in cm³) equals its surface area (in cm²) in "
   "number", "The height (cm) of a cone of base radius 3 cm whose volume is 12π cm³", [F(3)], [F(4)], "<",
   [">", ">="],
   "(4/3)πr³ = 4πr² gives r = 3; (1/3)πr²h = 12π gives h",
   "Quantity I: (4/3)πr³ = 4πr² ⇒ r = 3. Quantity II: (1/3)π × 9 × h = 12π ⇒ 3h = 12 ⇒ h = 4. 3 < 4.",
   ["I: r = 3", "II: 3h = 12 ⇒ h = 4", "3 < 4"],
   why="'I > II' and 'I ≥ II' come from dropping the 1/3 in the cone's volume (h = 4/3) or from solving "
       "(4/3)r³ = 4r² as r = 4.", secs=75, by=BRUTE)

lens = sorted({max(a, 48 // a) for a in range(1, 49) if 48 % a == 0})
assert lens == [8, 12, 16, 24, 48] and math.isqrt(100) * 4 // 4 == 10
qc("Quantity I vs II", A, "The length (cm) of a rectangle of area 48 cm² whose length and breadth are whole numbers "
   "of centimetres (length ≥ breadth)", "The side (cm) of a square of area 100 cm²",
   [F(x) for x in lens], [F(10)], "cbe", [">", "<="],
   "List every whole-number factor pair of 48",
   "Possible rectangles: 48 × 1, 24 × 2, 16 × 3, 12 × 4, 8 × 6, so the length is 48, 24, 16, 12 or 8. Quantity II = "
   "10. The length may be more or less than 10, so the relationship cannot be established.",
   ["Lengths: 8, 12, 16, 24, 48", "II = 10", "8 < 10 < 12 ⇒ cannot be established"],
   why="'I > II' assumes the rectangle cannot be 8 × 6; 'I ≤ II' and 'I < II' consider only the 8 × 6 rectangle.",
   secs=75, by=BRUTE)

# ================================================================ Data Sufficiency (Quant) (B2 I1 A1)
T = "Data Sufficiency (Quant)"
cands = [(F(r, 2), F(h, 2)) for r in range(1, 41) for h in range(1, 81)]
verdict = ds2_verdict(cands, lambda c: c[0] == 7, lambda c: c[1] == 2 * c[0] and 2 * F(22, 7) * c[0] * c[1] == 616,
                      lambda c: c[0] * c[0] * c[1])
assert verdict == "II"
Q(T, "Two-statement", B,
  f"{DS_PRE}\nQuestion: What is the volume of the cylinder?\n"
  "I. The radius of its base is 7 cm.\n"
  "II. Its height equals the diameter of its base, and its curved surface area is 616 cm². (Use π = 22/7.)",
  DS2["II"], [DS2["I"], DS2["both"], DS2["either"]],
  "Volume needs both r and h",
  "I gives r but not h. II: h = 2r and 2πrh = 4πr² = 616, so r² = 49, r = 7 and h = 14; the volume is "
  "22/7 × 49 × 14 = 2,156 cm³. So II alone is sufficient and I alone is not.",
  ["I: r only", "II: 4πr² = 616 ⇒ r = 7, h = 14", "II alone suffices"],
  why="'I alone' has no height; 'both' overlooks that II already fixes r; 'either' wrongly accepts I alone.",
  secs=50, by=BRUTE)

cands = [(d1, v1, 180 - d1, v2) for d1 in range(10, 180, 10) for v1 in (30, 36, 40, 45, 50, 60, 72)
         for v2 in (30, 36, 40, 45, 50, 60, 72)]
verdict = ds2_verdict(cands, lambda c: F(c[0], c[1]) + F(c[2], c[3]) == 4,
                      lambda c: c == (90, 60, 90, 36), lambda c: F(c[0] + c[2], F(c[0], c[1]) + F(c[2], c[3])))
assert verdict == "either"
Q(T, "Two-statement", B,
  f"{DS_PRE}\nQuestion: What is the average speed of a bus for its whole 180 km trip?\n"
  "I. The whole trip took 4 hours.\n"
  "II. The bus covered the first 90 km at 60 km/h and the remaining 90 km at 36 km/h.",
  DS2["either"], [DS2["I"], DS2["II"], DS2["both"]],
  "Average speed = total distance ÷ total time",
  "I: 180 ÷ 4 = 45 km/h. II: 90/60 + 90/36 = 1.5 + 2.5 = 4 hours, so again 45 km/h. Each statement alone is "
  "sufficient.",
  ["I: 180 ÷ 4 = 45", "II: time = 4 h ⇒ 45", "Either alone"],
  why="'I alone' and 'II alone' each overlook the other statement's sufficiency; 'both' is more than needed.",
  secs=45, by=BRUTE)

cands = [(ta, tb, cap) for ta in range(1, 41) for tb in range(1, 41) for cap in range(30, 1230, 30)]
conds = [lambda c: c[0] == 10, lambda c: F(c[2], c[1]) == 30, lambda c: F(1, c[0]) + F(1, c[1]) == F(1, 6)]
mp_ = suff_map(cands, conds, lambda c: c[2])
assert mp_ == {(0,): False, (1,): False, (2,): False, (0, 1): False, (0, 2): False, (1, 2): False, (0, 1, 2): True}
Q(T, "Three-statement", I,
  f"{DS3_PRE}\nQuestion: What is the capacity of the tank (in litres)?\n"
  "I. Pipe A alone fills the empty tank in 10 hours.\n"
  "II. Pipe B delivers 30 litres an hour.\n"
  "III. Pipes A and B together fill the empty tank in 6 hours.",
  "All three statements together are necessary",
  ["Only I and III together are sufficient", "Any two of the three statements together are sufficient",
   "Even all three statements together are not sufficient"],
  "Capacity = B's flow (litres per hour) × B's filling time; B's time comes from I and III",
  "I + III: 1/tB = 1/6 − 1/10 = 1/15, so B takes 15 hours, but no litres are given. II alone gives litres per hour "
  "without B's time. All three: capacity = 30 × 15 = 450 litres. No pair is enough: I + II and II + III leave B's "
  "time unknown.",
  ["I + III: B takes 15 h (no litres)", "II: 30 L/h", "All three: 450 L", "Every pair falls short"],
  why="'Only I and III' gives times, not litres; 'any two' fails because no pair fixes both B's time and its flow; "
      "'not sufficient' overlooks that all three give 450 litres.", secs=80, by=BRUTE)

cands = [(F(l_), F(v, 2)) for l_ in range(5, 605, 5) for v in range(1, 81)]
verdict = ds2_verdict(cands, lambda c: c[0] + 250 == 25 * c[1], lambda c: c[0] == 10 * (c[1] - F(5, 2)),
                      lambda c: c[1])
assert verdict == "both"
Q(T, "Two-statement", A,
  f"{DS_PRE}\nQuestion: What is the speed of the train?\n"
  "I. The train crosses a 250 m long platform in 25 seconds.\n"
  "II. The train passes a man jogging at 9 km/h in the same direction in 10 seconds.",
  DS2["both"], [DS2["I"], DS2["II"], DS2["neither"]],
  "Each statement is one equation in the train's length L and speed v",
  "I: L + 250 = 25v. II: L = 10(v − 2.5) (9 km/h = 2.5 m/s). Either alone has two unknowns. Together: "
  "25v − 250 = 10v − 25, so 15v = 225 and v = 15 m/s = 54 km/h (L = 125 m).",
  ["I: L + 250 = 25v", "II: L = 10(v − 2.5)", "Together: v = 15 m/s = 54 km/h"],
  why="'I alone' and 'II alone' treat one equation in two unknowns as enough; 'neither' misses that the two "
      "equations fix both L and v.", secs=90, by=BRUTE)

# ######################################################################## BATCH_010
BT = "010"

# ================================================================ Mixture and Alligation (B3 I2 A1)
T = "Mixture and Alligation"
x_ = F(56 * 100 - 40 * 50, 60)
assert x_ == 60 and F(5600 - 60 * 50, 40) == 65 and 2 * 56 - 50 == 62
Q(T, "Alligation rule", B, "A grocer mixes 40 kg of rice costing ₹50 per kg with 60 kg of another variety. The "
  "mixture costs him ₹56 per kg. What is the cost per kg of the second variety?",
  "₹60", ["₹65", "₹62", "₹56"],
  "Total cost of the mixture = cost of the first lot + cost of the second lot",
  "Mixture: 100 kg × 56 = ₹5,600. First lot: 40 × 50 = ₹2,000. Second lot: 5,600 − 2,000 = ₹3,600 for 60 kg, i.e. "
  "₹60 per kg.",
  ["Mixture cost = 5,600", "First lot = 2,000", "3,600 ÷ 60 = ₹60"],
  short="Alligation: 40 : 60 = (x − 56) : (56 − 50) ⇒ x − 56 = 4.",
  why="₹65 swaps the two quantities (60 kg at ₹50); ₹62 treats ₹56 as the simple average of the two prices; ₹56 is "
      "the mixture's own price.", secs=40)

milk = 50 * F(9, 10) ** 2
assert milk == F(81, 2) and 50 - milk == F(19, 2)
Q(T, "Replacement of mixture", B, "A can holds 50 litres of pure milk. 5 litres are taken out and replaced with water, "
  "and then 5 litres of the mixture are taken out and replaced with water once more. How much water is now in the "
  "can?",
  "9.5 litres", ["10 litres", "40.5 litres", "5 litres"],
  "After each replacement the milk is multiplied by (1 − 5/50) = 0.9",
  "Milk left = 50 × 0.9 × 0.9 = 40.5 litres, so water = 50 − 40.5 = 9.5 litres.",
  ["Milk = 50 × 0.9² = 40.5 L", "Water = 50 − 40.5 = 9.5 L"],
  why="10 litres forgets that the second 5 litres taken out already contained water; 40.5 litres is the milk; 5 "
      "litres counts only one replacement.", secs=40)

r_ = (F(75) - 48, F(48) - 30)
assert r_ == (27, 18) and F(27, 18) == F(3, 2)
assert (30 + 75) / F(2) == F(105, 2) and (5 * 30 + 3 * 75) / F(8) == F(375, 8)
Q(T, "Mixing solutions", B, "In what ratio must a 30% saline solution be mixed with a 75% saline solution to obtain "
  "a 48% saline solution?",
  "3 : 2", ["2 : 3", "1 : 1", "5 : 3"],
  "Alligation: (weaker : stronger) = (stronger − mean) : (mean − weaker)",
  "30% : 75% = (75 − 48) : (48 − 30) = 27 : 18 = 3 : 2.",
  ["75 − 48 = 27", "48 − 30 = 18", "27 : 18 = 3 : 2"],
  why="2 : 3 is inverted (it gives 57%); 1 : 1 gives 52.5%; 5 : 3 gives 46.875%.", secs=40)

fr = [F(2, 3), F(3, 5), F(4, 7)]
m_ = sum(fr)
w_ = 3 - m_
g = math.gcd(m_.numerator * 105 // m_.denominator, w_.numerator * 105 // w_.denominator)
assert m_ * 105 == 193 and w_ * 105 == 122 and g == 1
Q(T, "Mixing solutions", I, "Three vessels of equal capacity are full of milk–water mixtures in the ratios 2 : 1, "
  "3 : 2 and 4 : 3. Their contents are poured into one large drum. What is the ratio of milk to water in the drum?",
  "193 : 122", ["3 : 2", "122 : 193", "193 : 315"],
  "Equal volumes: add the milk fractions of the three vessels",
  "Milk fractions: 2/3, 3/5, 4/7. Taking each vessel as 105 units: milk 70 + 63 + 60 = 193, water 35 + 42 + 45 = "
  "122. Ratio = 193 : 122.",
  ["Vessel = 105 units", "Milk = 70 + 63 + 60 = 193", "Water = 35 + 42 + 45 = 122"],
  why="3 : 2 adds the ratio terms (2 + 3 + 4 : 1 + 2 + 3), which treats the vessels as unequal; 122 : 193 is "
      "inverted; 193 : 315 is milk to the whole mixture.", secs=70)

x_ = (F(30) * F(40, 100) - 30 * F(20, 100)) / (1 - F(20, 100))
assert x_ == F(15, 2) and (F(12) - 6) / F(6, 10) == 10
Q(T, "Replacement of mixture", I, "A tank holds 30 litres of a 20% acid solution. How many litres of it must be drawn "
  "off and replaced with pure acid so that the solution becomes 40% acid?",
  "7.5 litres", ["10 litres", "6 litres", "12 litres"],
  "Removing x litres removes 20% of x as acid; adding x litres of pure acid adds x",
  "Acid now = 6 litres. After the change: 6 − 0.2x + x = 40% of 30 = 12, so 0.8x = 6 and x = 7.5 litres.",
  ["Acid now = 6 L, needed = 12 L", "6 + 0.8x = 12", "x = 7.5 L"],
  why="10 litres adds pure acid without drawing any off (6 + x = 0.4(30 + x)); 6 litres is the acid already present; "
      "12 litres is the acid needed.", secs=65)

roots = [x for x in range(0, 100) if 50 * F(50 - x, 50) * F(50 - 2 * x, 50) == 36]
assert roots == [5, 70] and F(14, 3) * 3 == 14
Q(T, "Replacement of mixture", A, "A can holds 50 litres of pure milk. x litres are taken out and replaced with "
  "water; then 2x litres of the mixture are taken out and replaced with water. The can now holds 36 litres of milk. "
  "What is x?",
  "5 litres", ["4⅔ litres", "10 litres", "70 litres"],
  "Milk after two replacements = 50(1 − x/50)(1 − 2x/50); reject a root that does not fit the can",
  "50 × (50 − x)/50 × (50 − 2x)/50 = 36 ⇒ (50 − x)(50 − 2x) = 1,800 ⇒ 2x² − 150x + 700 = 0 ⇒ x² − 75x + 350 = 0 ⇒ "
  "(x − 5)(x − 70) = 0. Since 2x cannot exceed 50, x = 5 litres. Check: 50 × 0.9 × 0.8 = 36.",
  ["(50 − x)(50 − 2x) = 1,800", "x² − 75x + 350 = 0", "x = 5 or 70; 70 impossible", "x = 5 L"],
  why="4⅔ litres treats the milk removed as simply x + 2x = 14 litres; 10 litres is the second draw (2x); 70 litres "
      "is the other root of the quadratic, impossible in a 50-litre can.", secs=110, by=BRUTE)

# ================================================================ Time and Work (B1 I1 A2)
T = "Time and Work"
r_ = F(1, 28)
t_ = 1 / (4 * r_ + 2 * r_ + r_)
assert t_ == 4 and F(28, 4) == 7 and F(28, 2) == 14
Q(T, "Work efficiency", B, "P works twice as fast as Q, and Q works twice as fast as R. R alone can finish a job in "
  "28 days. In how many days can P, Q and R together finish it?",
  "4 days", ["7 days", "14 days", "9⅓ days"],
  "Efficiencies 4 : 2 : 1; add the daily rates",
  "R does 1/28 a day, Q 2/28 and P 4/28. Together: 7/28 = 1/4 a day, so 4 days.",
  ["Rates 4 : 2 : 1", "Together = 7/28 = 1/4", "4 days"],
  why="7 days is P's time alone; 14 days is Q's time alone; 9⅓ days (28 ÷ 3) treats the three as equally fast.",
  secs=40)

left = 1 - F(5, 20)
t_ = left / (F(1, 20) * F(5, 4))
assert t_ == 12 and left * 20 == 15 and 15 * F(3, 4) == F(45, 4)
Q(T, "Work efficiency", I, "A can finish a job alone in 20 days. After working for 5 days, he becomes 25% more "
  "efficient. In how many more days does he finish the job?",
  "12 days", ["15 days", "11¼ days", "17 days"],
  "Work left after 5 days, divided by the new daily rate (1.25 × 1/20)",
  "In 5 days A does 5/20 = 1/4. New rate = 1.25/20 = 1/16 a day. Remaining 3/4 takes (3/4) × 16 = 12 days.",
  ["Done: 1/4", "New rate = 1/16", "3/4 ÷ 1/16 = 12 days"],
  why="15 days ignores the improvement; 11¼ days cuts the time by 25% instead of dividing by 1.25; 17 days is the "
      "whole time, 5 + 12.", secs=55)

W = 12 * (4 * 3 + 4 * 2 + 8 * 1)
rest = W - 3 * 28
t_ = F(rest, 2 * 3 + 4 * 2 + 4 * 1)
assert W == 336 and rest == 252 and t_ == 14 and 3 + t_ == 17
eq = 16 * 12
assert 3 + F(eq - 3 * 16, 10) == F(87, 5)
Q(T, "Men-women-children", A, "A man, a woman and a child do work in the ratio 3 : 2 : 1 per day. A team of 4 men, "
  "4 women and 8 children can finish a job in 12 days. After 3 days, 2 men and 4 children leave. In how many days "
  "in all is the job finished?",
  "17 days", ["14 days", "17.4 days", "15 days"],
  "Count the job in child-days; then divide the remainder by the new team's daily output",
  "Daily output = 4 × 3 + 4 × 2 + 8 × 1 = 28 units, so the job = 28 × 12 = 336 units. After 3 days, 84 are done and "
  "252 remain. The new team (2 men, 4 women, 4 children) does 6 + 8 + 4 = 18 units a day, needing 252 ÷ 18 = 14 "
  "days. Total = 3 + 14 = 17 days.",
  ["Job = 336 units", "After 3 days: 252 left", "New output 18/day ⇒ 14 days", "Total 17 days"],
  why="14 days counts only the time after the change; 17.4 days treats everyone as equally efficient (16 people, "
      "then 10); 15 days assumes the job would only be delayed by the 3 days already worked.", secs=110)

rates = {"A": 3, "B": 2, "C": 1}  # per day, job = 30 units (A 10, B 15, C 30 days)
pairs = [("A", "B"), ("B", "C"), ("C", "A")]
done, day = F(0), 0
while True:
    rt = sum(rates[p] for p in pairs[day % 3])
    day += 1
    if done + rt >= 30:
        total = day - 1 + (30 - done) / rt
        break
    done += rt
assert total == F(22, 3) and F(30, 4) == F(15, 2) and F(30, 6) == 5
Q(T, "Alternate days", A, "A, B and C can finish a job alone in 10, 15 and 30 days respectively. They work in pairs "
  "in turn: A and B on day 1, B and C on day 2, C and A on day 3, A and B again on day 4, and so on. How long does "
  "the job take?",
  "7⅓ days", ["8 days", "7½ days", "5 days"],
  "Take the job as 30 units (A 3, B 2, C 1 a day); find a three-day cycle and finish the remainder",
  "Day outputs: A + B = 5, B + C = 3, C + A = 4, so a 3-day cycle does 12 units. Two cycles (6 days) do 24, leaving "
  "6. Day 7 (A + B) does 5, leaving 1. Day 8 (B + C, 3 a day) needs 1/3 of a day. Total = 7⅓ days.",
  ["Job = 30 units", "Cycle: 5 + 3 + 4 = 12 per 3 days", "6 days ⇒ 24; day 7 ⇒ 29", "Day 8: 1/3 day ⇒ 7⅓"],
  why="8 days counts the last day in full; 7½ days divides 30 by the average 4 units a day, ignoring the order of "
      "the pairs; 5 days has all three working every day.", secs=110)

# ================================================================ Pipes and Cisterns (B2 I2 A1)
T = "Pipes and Cisterns"
rt = F(1, 18) + F(1, 27)
assert F(5, 6) / rt == 9 and 1 / rt == F(54, 5) and F(18 + 27, 2) * F(5, 6) == F(75, 4)
Q(T, "Inlet and outlet", B, "Two pipes can fill a tank in 18 minutes and 27 minutes respectively. If both are opened "
  "together on the empty tank, how long will they take to fill five-sixths of it?",
  "9 minutes", ["10 minutes 48 seconds", "18¾ minutes", "13½ minutes"],
  "Combined rate = 1/18 + 1/27 = 5/54 of the tank per minute",
  "Combined rate = (3 + 2)/54 = 5/54 per minute. Time for 5/6 = (5/6) ÷ (5/54) = 9 minutes.",
  ["Rate = 5/54 per min", "(5/6) × (54/5) = 9 min"],
  why="10 min 48 s is the time for the full tank; 18¾ minutes takes 5/6 of the average of 18 and 27; 13½ minutes "
      "halves the slower pipe's time.", secs=40)

t_ = F(240, 6 - F(3, 2))
assert 240 / 40 == 6 and t_ == F(160, 3) and F(240, F(15, 2)) == 32 and F(240, F(3, 2)) == 160
Q(T, "Leak problems", B, "A tap fills a 240-litre tank in 40 minutes. A leak in the tank lets out 1.5 litres a "
  "minute. How long does the tap take to fill the tank while the leak is working?",
  "53⅓ minutes", ["40 minutes", "32 minutes", "160 minutes"],
  "Tap rate = 240 ÷ 40 = 6 L/min; net rate = 6 − 1.5",
  "Net filling rate = 6 − 1.5 = 4.5 litres a minute. Time = 240 ÷ 4.5 = 53⅓ minutes.",
  ["Tap = 6 L/min", "Net = 4.5 L/min", "240 ÷ 4.5 = 53⅓ min"],
  why="40 minutes ignores the leak; 32 minutes adds the leak to the tap (7.5 L/min); 160 minutes is how long the "
      "leak alone would take to empty the full tank.", secs=40)

part = 3 * F(1, 10)
t_ = (1 - part) / (F(1, 10) - F(1, 15))
assert part == F(3, 10) and t_ == 21 and 1 / (F(1, 10) - F(1, 15)) == 30
Q(T, "Inlet and outlet", I, "Pipe A fills a tank in 10 hours and pipe B empties the full tank in 15 hours. A is "
  "opened on the empty tank at 6:00 AM and B is opened at 9:00 AM. When will the tank be full?",
  "6:00 AM the next day", ["12:00 noon the next day", "3:00 PM the next day", "4:00 PM the same day"],
  "Fill with A alone for 3 hours, then the rest at the net rate 1/10 − 1/15 = 1/30 per hour",
  "By 9:00 AM A fills 3/10. The remaining 7/10 at 1/30 per hour takes 21 hours: 9:00 AM + 21 h = 6:00 AM the next "
  "day.",
  ["6–9 AM: 3/10", "Net rate = 1/30", "7/10 ⇒ 21 h ⇒ 6:00 AM next day"],
  why="12:00 noon the next day opens both pipes at 6:00 AM (30 hours); 3:00 PM the next day ignores A's 3-hour head "
      "start and adds 30 hours to 9:00 AM; 4:00 PM the same day ignores B altogether.", secs=65)

sol = [(a, b) for b in range(1, 200) for a in [F(b, 3)] if b - a == 32]
a_, b_ = sol[0]
assert sol == [(16, 48)] and 1 / (1 / a_ + F(1, b_)) == 12
Q(T, "Inlet and outlet", I, "Pipe A fills a tank three times as fast as pipe B, and takes 32 minutes less than B to "
  "fill it. How long will the two pipes take to fill the tank together?",
  "12 minutes", ["16 minutes", "48 minutes", "8 minutes"],
  "If A takes t minutes, B takes 3t, and 3t − t = 32",
  "2t = 32, so A takes 16 minutes and B 48 minutes. Together: 1/16 + 1/48 = 4/48 = 1/12, i.e. 12 minutes.",
  ["2t = 32 ⇒ A = 16, B = 48", "1/16 + 1/48 = 1/12", "12 min"],
  why="16 minutes is A's time alone; 48 minutes is B's; 8 minutes divides the 32-minute difference by 4.", secs=55,
  by=BRUTE)

ab = F(1, 6) + F(1, 8)
c_ = (4 * ab - 1) / 2
assert ab == F(7, 24) and c_ == F(1, 12) and 4 * ab - 1 == F(1, 6) and ab - F(1, 4) == F(1, 24)
Q(T, "Inlet and outlet", A, "Pipes A and B fill a cistern in 6 hours and 8 hours respectively, and pipe C empties it. "
  "All three are opened on the empty cistern at 7:00 AM. C is closed at 9:00 AM, and the cistern is full at "
  "11:00 AM. How long would C alone take to empty the full cistern?",
  "12 hours", ["24 hours", "6 hours", "8 hours"],
  "A and B run for 4 hours; whatever they deliver beyond one cistern was removed by C in its 2 hours",
  "A + B fill 1/6 + 1/8 = 7/24 per hour, so in 4 hours they deliver 28/24 = 7/6 of the cistern. C removed the "
  "extra 1/6 in 2 hours, i.e. 1/12 per hour, so C alone empties it in 12 hours.",
  ["A + B: 4 × 7/24 = 7/6", "C removed 1/6 in 2 h", "C's rate = 1/12 ⇒ 12 h"],
  why="24 hours assumes C stayed open all 4 hours; 6 hours takes C to remove 1/3 in its 2 hours; 8 hours is B's "
      "filling time.", secs=100)

# ================================================================ Speed, Time and Distance (B2 I2 A1)
T = "Speed, Time and Distance"
tb = F(20) / (F(4, 3) - 1)
assert tb == 60 and tb * F(4, 3) == 80
Q(T, "Average speed", B, "The speeds of A and B are in the ratio 3 : 4. Over the same route, A takes 20 minutes "
  "longer than B. How long does A take?",
  "80 minutes", ["60 minutes", "140 minutes", "100 minutes"],
  "Times are in the inverse ratio of speeds: A : B = 4 : 3",
  "Times are 4 : 3; the difference of 1 part = 20 minutes, so A takes 4 × 20 = 80 minutes (B takes 60).",
  ["Time ratio 4 : 3", "1 part = 20 min", "A = 80 min"],
  why="60 minutes is B's time; 140 minutes adds the two times; 100 minutes takes 5 parts.", secs=40)

v = F(800, 180) * F(18, 5)
assert v == 16 and (F(400, 80) * F(18, 5) + F(400, 100) * F(18, 5)) / 2 == F(81, 5)
Q(T, "Average speed", B, "A runner completes the first 400 m lap of a track in 80 seconds and the second 400 m lap "
  "in 100 seconds. What is her average speed over the two laps, in km/h?",
  "16 km/h", ["16.2 km/h", "4.44 km/h", "14.4 km/h"],
  "Average speed = total distance ÷ total time; 1 m/s = 3.6 km/h",
  "800 m in 180 s = 4.44 m/s = 4.44 × 3.6 = 16 km/h.",
  ["800 m in 180 s", "= 40/9 m/s", "× 3.6 = 16 km/h"],
  why="16.2 km/h averages the two lap speeds (18 and 14.4 km/h); 4.44 is the speed in m/s; 14.4 km/h is the second "
      "lap's speed only.", secs=45)

d_ = math.isqrt(18 ** 2 + 24 ** 2)
assert d_ == 30 and 18 * 18 + 24 * 24 == 900 and math.isqrt(144 + 256) == 20
Q(T, "Relative speed", I, "From a crossing, Asha cycles due north at 12 km/h and Babu cycles due east at 16 km/h, both "
  "starting at the same time. How far apart, in a straight line, are they after 1 hour 30 minutes?",
  "30 km", ["42 km", "6 km", "20 km"],
  "The two paths are at right angles: use Pythagoras on the distances covered",
  "Asha covers 12 × 1.5 = 18 km and Babu 16 × 1.5 = 24 km. Distance apart = √(18² + 24²) = √900 = 30 km.",
  ["18 km and 24 km", "√(324 + 576) = √900", "= 30 km"],
  why="42 km adds the two distances as if they rode in opposite directions; 6 km subtracts them as if they rode the "
      "same way; 20 km is the gap after only 1 hour.", secs=55)

d_ = [d for d in range(1, 1000) if F(5, 9) * d - F(4, 9) * d == 24]
assert d_ == [216]
Q(T, "Meeting and overtaking", I, "P and Q start at the same time from towns X and Y and travel towards each other. "
  "P is 25% faster than Q. They meet at a point 12 km from the midpoint of XY. What is the distance XY?",
  "216 km", ["108 km", "240 km", "432 km"],
  "Distances covered are in the ratio of speeds, 5 : 4; P covers 12 km more than half and Q 12 km less",
  "P covers 5/9 and Q 4/9 of XY. The difference, 1/9 of XY, is 12 + 12 = 24 km, so XY = 9 × 24 = 216 km.",
  ["Speed ratio 5 : 4", "Difference = 24 km = 1/9 of XY", "XY = 216 km"],
  why="108 km takes the difference as 12 km instead of 24; 240 km treats the 24 km as 10% of the distance; 432 km "
      "doubles the answer.", secs=70, by=BRUTE)

v2 = F(40 + 60, 2)
avg = 2 * 30 * v2 / (30 + v2)
assert avg == F(75, 2) and r2(2 * 30 * 48 / F(78)) == F("36.92") and r2(F(130, 3)) == F("43.33")
Q(T, "Average speed", A, "A truck covers the first half of a route at 30 km/h. For the second half of the route, it "
  "runs at 40 km/h for half the time it spends on that half and at 60 km/h for the other half of that time. What is "
  "its average speed for the whole route?",
  "37.5 km/h", ["40 km/h", "43.33 km/h", "36.92 km/h"],
  "Equal times: average = mean of the speeds; equal distances: average = harmonic mean",
  "On the second half the two speeds run for equal times, so that half's average is (40 + 60)/2 = 50 km/h. The two "
  "halves are equal distances, so the overall average = 2 × 30 × 50 ÷ (30 + 50) = 37.5 km/h.",
  ["Second half: equal times ⇒ 50 km/h", "Halves: equal distances", "2 × 30 × 50 ÷ 80 = 37.5 km/h"],
  why="40 km/h averages 30 and 50 arithmetically; 43.33 km/h averages 30, 40 and 60; 36.92 km/h treats the second "
      "half's speeds as covering equal distances (48 km/h).", secs=110)

# ================================================================ Boats and Streams (B1 I1 A1)
T = "Boats and Streams"
up = F(18, F(3, 2))
b_ = up + 3
assert up == 12 and b_ == 15 and F(18, b_ + 3) == 1 and F(18, 15) * 60 == 72 and F(18, 24) * 60 == 45
Q(T, "Upstream and downstream", B, "A boat goes 18 km upstream in 1 hour 30 minutes. The stream flows at 3 km/h. How "
  "long will the boat take to come back the same 18 km downstream?",
  "1 hour", ["1 hour 12 minutes", "45 minutes", "1 hour 30 minutes"],
  "Upstream speed + stream = still-water speed; downstream = still-water speed + stream",
  "Upstream speed = 18 ÷ 1.5 = 12 km/h, so the boat's speed = 12 + 3 = 15 km/h and its downstream speed = 18 km/h. "
  "Time = 18 ÷ 18 = 1 hour.",
  ["Upstream = 12 km/h", "Boat = 15, downstream = 18 km/h", "18 ÷ 18 = 1 h"],
  why="1 h 12 min uses the still-water speed 15 km/h; 45 minutes adds the stream twice (24 km/h); 1 h 30 min is "
      "the upstream time.", secs=40)

up, dn = F(2, 1), F(1, F(1, 6))
b_ = (up + dn) / 2
assert dn == 6 and b_ == 4 and F(5, b_) == F(5, 4) and F(5, 3) * 60 == 100 and F(5, 6) * 60 == 50
Q(T, "Speed of stream", I, "A boatman rows 2 km against the current in 1 hour and 1 km along the current in 10 "
  "minutes. How long would he take to row 5 km in still water?",
  "1 hour 15 minutes", ["1 hour 40 minutes", "50 minutes", "2 hours 30 minutes"],
  "Still-water speed = (downstream speed + upstream speed) ÷ 2",
  "Upstream speed = 2 km/h; downstream speed = 1 km in 1/6 h = 6 km/h. Still-water speed = (6 + 2)/2 = 4 km/h. "
  "Time for 5 km = 5/4 h = 1 hour 15 minutes.",
  ["Up = 2, down = 6 km/h", "Still water = 4 km/h", "5 ÷ 4 = 1¼ h"],
  why="1 h 40 min uses 3 km/h (taking the downstream speed as 4 km/h, i.e. 1 km per 15 minutes); 50 minutes uses the "
      "downstream speed; 2 h 30 min uses the upstream speed.", secs=55)

sol = [s for s in range(1, 20) if F(48, 6 * s) + F(48, 4 * s) == 10]
s_ = sol[0]
b_ = 5 * s_
new = F(48, b_ + 4 + s_) + F(48, b_ + 4 - s_)
assert sol == [2] and b_ == 10 and new == 7 and F(96, 16) == 6 and F(96, 12) == 8
Q(T, "Upstream and downstream", A, "A boat's speed in still water is five times the speed of the stream. It goes 48 km "
  "downstream and comes back in 10 hours in all. If the boat's still-water speed is raised by 4 km/h (the stream "
  "unchanged), how long will the same round trip take?",
  "7 hours", ["6 hours", "8 hours", "10 hours"],
  "First find the stream speed from the round trip, then recompute with the new boat speed",
  "Let the stream be s; boat = 5s, downstream 6s, upstream 4s. 48/(6s) + 48/(4s) = 8/s + 12/s = 20/s = 10, so "
  "s = 2 and the boat = 10 km/h. New boat speed = 14: 48/16 + 48/12 = 3 + 4 = 7 hours.",
  ["20/s = 10 ⇒ s = 2", "Boat = 10 ⇒ new 14 km/h", "48/16 + 48/12 = 7 h"],
  why="6 hours uses the new downstream speed both ways; 8 hours uses the new upstream speed both ways; 10 hours "
      "ignores the change.", secs=100, by=BRUTE)

# ================================================================ Problems on Trains (B1 I2 A2)
T = "Problems on Trains"
L = F(90 * 5, 18) * 16 - 180
assert L == 220 and 90 * 16 - 180 == 1260
Q(T, "Crossing a pole or platform", B, "A train running at 90 km/h crosses a 180 m long platform in 16 seconds. What "
  "is the length of the train?",
  "220 m", ["400 m", "580 m", "1,260 m"],
  "Distance covered while crossing = train + platform",
  "90 km/h = 25 m/s. In 16 s the train covers 400 m = train + 180, so the train is 220 m long.",
  ["25 m/s × 16 s = 400 m", "400 − 180 = 220 m"],
  why="400 m is the train and platform together; 580 m adds the platform instead of subtracting it; 1,260 m forgets "
      "to convert km/h to m/s (90 × 16 − 180).", secs=40)

rel = F(125, 10) * F(18, 5)
assert rel == 45 and rel + 6 == 51 and rel - 6 == 39
Q(T, "Crossing a pole or platform", I, "A 125 m long train passes a man running at 6 km/h in the same direction in "
  "10 seconds. What is the speed of the train?",
  "51 km/h", ["45 km/h", "39 km/h", "63 km/h"],
  "Same direction: relative speed = train − man; the train covers its own length",
  "Relative speed = 125 ÷ 10 = 12.5 m/s = 45 km/h. Train speed = 45 + 6 = 51 km/h.",
  ["12.5 m/s = 45 km/h", "45 + 6 = 51 km/h"],
  why="45 km/h is the relative speed; 39 km/h subtracts the man's speed instead of adding it; 63 km/h adds 18 km/h "
      "(treating 6 km/h as 5 m/s).", secs=50)

rel = F(500, 15) * F(18, 5)
assert rel == 120 and rel - 50 == 70 and rel + 50 == 170 and F(220, 15) * F(18, 5) == F(264, 5)
Q(T, "Trains crossing each other", I, "A 280 m long train running at 50 km/h crosses a 220 m long train coming from "
  "the opposite direction on a parallel track in 15 seconds. What is the speed of the second train?",
  "70 km/h", ["120 km/h", "170 km/h", "52.8 km/h"],
  "Opposite directions: relative speed = sum of the speeds; crossing distance = sum of the lengths",
  "Relative speed = (280 + 220) ÷ 15 = 100/3 m/s = 120 km/h. Second train = 120 − 50 = 70 km/h.",
  ["500 m in 15 s", "= 120 km/h", "120 − 50 = 70 km/h"],
  why="120 km/h is the relative speed; 170 km/h treats the trains as moving the same way; 52.8 km/h uses only the "
      "second train's length (220 ÷ 15 m/s).", secs=60)

# engine passes walker A (same direction, 6 km/h) at 10:00 and meets walker B (towards it, 6 km/h) at 10:06
d_ = F(60, 60) * 6 - F(6, 60) * 6
t_ = d_ / F(12, 60)
assert d_ == F(27, 5) and t_ == 27 and F(6, F(12, 60)) == 30 and F(54, 10) / F(6, 60) == 54
Q(T, "Trains crossing each other", A, "A train runs at 60 km/h. Its engine passes Arun, who is walking along the line "
  "in the same direction at 6 km/h, at 10:00 AM, and meets Bala, who is walking towards the train at 6 km/h, at "
  "10:06 AM. At what time do Arun and Bala meet?",
  "10:33 AM", ["10:36 AM", "10:30 AM", "10:54 AM"],
  "At 10:06 find the gap between the walkers; they then close it at 6 + 6 km/h",
  "In 6 minutes the engine goes 6 km past the point where it passed Arun, while Arun walks 0.6 km. So at 10:06 the "
  "gap between Arun and Bala is 6 − 0.6 = 5.4 km, closing at 12 km/h: 5.4 ÷ 12 = 0.45 h = 27 minutes. They meet at "
  "10:33 AM.",
  ["Engine: 6 km in 6 min", "Arun: 0.6 km ⇒ gap 5.4 km", "5.4 ÷ 12 = 27 min ⇒ 10:33"],
  why="10:36 AM forgets Arun's 0.6 km (6 ÷ 12 = 30 minutes after 10:06); 10:30 AM counts those 30 minutes from 10:00; "
      "10:54 AM closes the gap at only Bala's 6 km/h, from 10:00.", secs=110)

t_ = F(1200 + 160 + 140, F((52 + 56) * 5, 18))
assert t_ == 50 and F(1200, 30) == 40 and F(300, 30) == 10 and F(1350, 30) == 45
Q(T, "Trains crossing each other", A, "Two trains, 160 m and 140 m long, run towards each other on parallel tracks at "
  "52 km/h and 56 km/h. From the moment their engines are 1.2 km apart, how long will it be until the trains have "
  "completely passed each other?",
  "50 seconds", ["40 seconds", "10 seconds", "45 seconds"],
  "The engines must first meet (1,200 m) and then the trains must clear each other (160 + 140 m), at the relative "
  "speed",
  "Relative speed = 108 km/h = 30 m/s. Distance = 1,200 + 160 + 140 = 1,500 m. Time = 1,500 ÷ 30 = 50 seconds.",
  ["Relative speed = 30 m/s", "Distance = 1,500 m", "50 s"],
  why="40 seconds stops when the engines meet; 10 seconds counts only the crossing itself; 45 seconds adds only one "
      "train's length.", secs=90)

# ================================================================ Mensuration (B1 I4 A3)
T = "Mensuration"
assert 9 ** 2 + 12 ** 2 == 15 ** 2 and F(9 * 12, 2) == 54 and F(9 * 15, 2) == F(135, 2) and F(12 * 15, 2) == 90
Q(T, "2D areas and perimeters", B, "The sides of a triangle are 9 cm, 12 cm and 15 cm. What is its area?",
  "54 cm²", ["108 cm²", "67.5 cm²", "90 cm²"],
  "9² + 12² = 15², so the triangle is right-angled with legs 9 and 12",
  "81 + 144 = 225 = 15², so the angle between the 9 cm and 12 cm sides is 90°. Area = ½ × 9 × 12 = 54 cm².",
  ["9² + 12² = 15² ⇒ right angle", "Area = ½ × 9 × 12 = 54 cm²"],
  why="108 cm² forgets the ½; 67.5 cm² and 90 cm² take the hypotenuse 15 cm as one of the perpendicular sides.",
  secs=40)

hemi = F(2, 3) * 9 ** 3
bowl = 3 * 3 * 2
assert hemi / bowl == 27 and F(4, 3) * 729 / bowl == 54 and F(729, 9) == 81
Q(T, "Cylinder, cone and sphere", I, "A hemispherical bowl of internal radius 9 cm is full of soup. The soup is poured "
  "into cylindrical cups, each of internal radius 3 cm and height 2 cm. How many cups can be filled?",
  "27", ["54", "81", "18"],
  "Number of cups = volume of the hemisphere ÷ volume of one cup (π cancels)",
  "Hemisphere = (2/3)π × 9³ = 486π cm³. One cup = π × 3² × 2 = 18π cm³. Cups = 486 ÷ 18 = 27.",
  ["Hemisphere = 486π", "Cup = 18π", "486 ÷ 18 = 27"],
  why="54 uses a full sphere; 81 forgets the cup's height (729 ÷ 9); 18 is the volume of one cup in units of π, "
      "not the number of cups.", secs=55)

walls = 2 * 4 * (10 + 8)
area = walls + 10 * 8 - 2 * 1 - 2 * F(3, 2) * 1
assert walls == 144 and area == 219 and area * 25 == 5475 and (walls + 80) * 25 == 5600 and walls * 25 == 3600
assert (area + 80) * 25 == 7475
Q(T, "3D volume and surface area", I, "A room is 10 m long, 8 m wide and 4 m high. It has one door 2 m × 1 m and two "
  "windows, each 1.5 m × 1 m. What will it cost to whitewash the four walls and the ceiling at ₹25 per m²?",
  "₹5,475", ["₹5,600", "₹3,600", "₹7,475"],
  "Four walls = 2h(l + b); add the ceiling l × b; subtract the door and windows",
  "Walls = 2 × 4 × 18 = 144 m². Ceiling = 80 m². Openings = 2 + 2 × 1.5 = 5 m². Area = 144 + 80 − 5 = 219 m². "
  "Cost = 219 × 25 = ₹5,475.",
  ["Walls 144, ceiling 80", "Openings 5 m²", "219 × 25 = ₹5,475"],
  why="₹5,600 forgets to subtract the door and windows; ₹3,600 whitewashes only the walls, without deductions; "
      "₹7,475 also whitewashes the floor.", secs=70)

assert F(20 * 20, 2) == 200 and 20 * 20 == 400 and 10 * 10 == 100
Q(T, "2D areas and perimeters", I, "A square is drawn inside a circle of radius 10 cm so that all four of its corners "
  "lie on the circle. What is the area of the square?",
  "200 cm²", ["400 cm²", "100 cm²", "314 cm²"],
  "The diagonal of the square is a diameter; area of a square = diagonal² ÷ 2",
  "Diagonal = 2 × 10 = 20 cm. Area = 20² ÷ 2 = 200 cm².",
  ["Diagonal = 20 cm", "Area = 400 ÷ 2 = 200 cm²"],
  short="Side = 10√2 cm, area = 200 cm².",
  why="400 cm² takes the side equal to the diameter (the square around the circle); 100 cm² takes the side equal to "
      "the radius; 314 cm² is the area of the circle.", secs=45)

rs = [r for r in range(1, 30) if F(1, 3) * 36 * 24 == F(4, 3) * r ** 3]
assert rs == [6]
Q(T, "Cylinder, cone and sphere", I, "A solid metal cone with base radius 6 cm and height 24 cm is melted and recast "
  "into a solid sphere. What is the radius of the sphere?",
  "6 cm", ["12 cm", "3 cm", "9 cm"],
  "Volume is unchanged: (1/3)πr²h = (4/3)πR³",
  "(1/3) × 36 × 24 = 288 = (4/3)R³, so R³ = 216 and R = 6 cm.",
  ["Cone = 288π", "(4/3)R³ = 288 ⇒ R³ = 216", "R = 6 cm"],
  why="12 cm takes half the cone's height; 3 cm takes half its radius; 9 cm drops both the 1/3 and the 4/3 and "
      "estimates the cube root of 36 × 24 = 864 (about 9.5).", secs=60, by=BRUTE)

vol = math.isqrt(48 * 60 * 80)
dims = [(l, b, h) for l in range(1, 30) for b in range(1, 30) for h in range(1, 30)
        if l * b == 48 and b * h == 60 and h * l == 80]
assert vol == 480 and dims == [(8, 6, 10)] and 48 + 60 + 80 == 188
Q(T, "3D volume and surface area", A, "Three faces of a cuboid that meet at a corner have areas 48 cm², 60 cm² and "
  "80 cm². What is the volume of the cuboid?",
  "480 cm³", ["188 cm³", "960 cm³", "2,30,400 cm³"],
  "(lb)(bh)(hl) = (lbh)², so volume = √(product of the three face areas)",
  "48 × 60 × 80 = 2,30,400 = 480², so the volume = 480 cm³ (the edges are 8, 6 and 10 cm).",
  ["Product = 2,30,400", "√2,30,400 = 480", "Check: 8 × 6 × 10 = 480"],
  why="188 cm³ adds the areas; 960 cm³ doubles the volume (as in a surface-area formula); 2,30,400 cm³ forgets the "
      "square root.", secs=75, by=BRUTE)

vol = F(22, 7) * (5 ** 2 - 4 ** 2) * 140
assert vol == 3960 and vol * 8 / 1000 == F(3168, 100) and F(22, 7) * (100 - 64) * 140 * 8 / 1000 == F(12672, 100)
assert F(22, 7) * 25 * 140 * 8 / 1000 == 88
Q(T, "Cylinder, cone and sphere", A, "A metal pipe is 1.4 m long. Its external diameter is 10 cm and its internal "
  "diameter is 8 cm. If 1 cm³ of the metal weighs 8 g, what does the pipe weigh? (Use π = 22/7.)",
  "31.68 kg", ["126.72 kg", "88 kg", "3.96 kg"],
  "Volume of metal = π(R² − r²) × length",
  "R = 5 cm, r = 4 cm, length = 140 cm. Volume = 22/7 × (25 − 16) × 140 = 3,960 cm³. Weight = 3,960 × 8 g = "
  "31,680 g = 31.68 kg.",
  ["R² − r² = 9", "Volume = 22/7 × 9 × 140 = 3,960 cm³", "× 8 g = 31.68 kg"],
  why="126.72 kg uses the diameters as radii; 88 kg treats the pipe as a solid rod; 3.96 kg forgets the 8 g per "
      "cm³.", secs=90)

gap = 14 * 14 - 4 * F(1, 4) * F(22, 7) * 49
assert gap == 42 and F(22, 7) * 49 == 154
Q(T, "2D areas and perimeters", A, "Four equal circles, each of radius 7 cm, are placed so that each touches two "
  "others and their centres form a square. What is the area of the region enclosed between the four circles? "
  "(Use π = 22/7.)",
  "42 cm²", ["154 cm²", "196 cm²", "21 cm²"],
  "Square of centres (side 14 cm) minus four quarter-circles (one full circle)",
  "The centres form a square of side 2 × 7 = 14 cm, area 196 cm². Inside it lie four quarter-circles, together one "
  "circle of area 22/7 × 49 = 154 cm². The enclosed region = 196 − 154 = 42 cm².",
  ["Square = 196 cm²", "Four quarters = 154 cm²", "196 − 154 = 42 cm²"],
  why="154 cm² is the area of one circle; 196 cm² is the whole square; 21 cm² halves the answer.", secs=90)

# ================================================================ Probability (B2 I2 A1)
T = "Probability"
p = prob(DICE2, lambda w: sum(w) in (7, 11))
assert p == F(2, 9) and prob(DICE2, lambda w: sum(w) == 7) == F(1, 6)
Q(T, "Coins and dice", B, "Two fair dice are rolled. What is the probability that the total is 7 or 11?",
  "2/9", ["1/6", "1/18", "7/36"],
  "Count the outcomes for each total and add (the events cannot happen together)",
  "Total 7: 6 outcomes; total 11: (5, 6) and (6, 5), 2 outcomes. P = 8/36 = 2/9.",
  ["Total 7: 6 ways", "Total 11: 2 ways", "8/36 = 2/9"],
  why="1/6 counts only a total of 7; 1/18 counts only 11; 7/36 counts (5, 6) and (6, 5) as one outcome.", secs=40,
  by=BRUTE)

p = prob(DECK, lambda c: c[1] == "D" or (c[0] == 13 and c[1] in "SC"))
assert p == F(15, 52)
Q(T, "Cards", B, "One card is drawn at random from a well-shuffled pack of 52 cards. What is the probability that it "
  "is a diamond or a black king?",
  "15/52", ["17/52", "1/4", "7/26"],
  "The two events cannot overlap (no diamond is black), so add",
  "13 diamonds + 2 black kings = 15 favourable cards. P = 15/52.",
  ["Diamonds = 13", "Black kings = 2", "15/52"],
  why="17/52 adds all four kings; 1/4 counts only the diamonds; 7/26 (14/52) counts only one black king.", secs=40,
  by=BRUTE)

bag = ["R"] * 3 + ["G"] * 5 + ["Y"] * 2
p_rep = prob(list(itertools.product(range(10), repeat=2)), lambda w: bag[w[0]] != bag[w[1]])
p_norep = prob(list(itertools.permutations(range(10), 2)), lambda w: bag[w[0]] != bag[w[1]])
assert p_rep == F(31, 50) and p_norep == F(31, 45)
Q(T, "Balls from bags", I, "A bag contains 3 red, 5 green and 2 yellow balls. A ball is drawn, its colour noted and "
  "it is put back; then a second ball is drawn. What is the probability that the two balls are of different "
  "colours?",
  "31/50", ["19/50", "31/45", "3/5"],
  "P(different) = 1 − P(same colour); with replacement the draws are independent",
  "P(same) = (3/10)² + (5/10)² + (2/10)² = (9 + 25 + 4)/100 = 38/100. P(different) = 62/100 = 31/50.",
  ["P(same) = 38/100", "P(different) = 62/100", "= 31/50"],
  why="19/50 is the probability of the same colour; 31/45 is the answer without replacement; 3/5 is a guess based "
      "on the three colours alone.", secs=60, by=BRUTE)

p = prob(list(itertools.product(range(1, 7), repeat=3)), lambda w: sum(w) <= 5)
assert p == F(5, 108) and prob(list(itertools.product(range(1, 7), repeat=3)), lambda w: sum(w) < 5) == F(1, 54)
Q(T, "Coins and dice", I, "Three fair dice are rolled together. What is the probability that the total is at most 5?",
  "5/108", ["1/54", "1/36", "5/54"],
  "Count the outcomes with totals 3, 4 and 5",
  "Total 3: (1, 1, 1), 1 way. Total 4: one die shows 2, 3 ways. Total 5: (1, 1, 3) in 3 ways and (1, 2, 2) in 3 "
  "ways, 6 ways. Favourable = 10 of 216, P = 10/216 = 5/108.",
  ["Total 3: 1", "Total 4: 3", "Total 5: 6", "10/216 = 5/108"],
  why="1/54 leaves out the total of 5 (4/216); 1/36 counts only the total of 5 (6/216); 5/54 doubles "
      "the favourable count.", secs=70, by=BRUTE)

hands = list(itertools.combinations(range(52), 3))
aces = {0, 13, 26, 39}
p = prob(hands, lambda h: len(aces & set(h)) == 1)
assert p == F(1128, 5525) and prob(hands, lambda h: len(aces & set(h)) >= 1) == F(1201, 5525)
assert 3 * F(1, 13) * F(12, 13) ** 2 == F(432, 2197)
Q(T, "Cards", A, "Three cards are drawn together at random from a well-shuffled pack of 52 cards. What is the "
  "probability that exactly one of them is an ace?",
  "1128/5525", ["1201/5525", "432/2197", "3/13"],
  "Choose 1 of the 4 aces and 2 of the 48 non-aces, over C(52, 3)",
  "Favourable = 4 × C(48, 2) = 4 × 1,128 = 4,512. Total = C(52, 3) = 22,100. P = 4,512/22,100 = 1128/5525.",
  ["4 × C(48, 2) = 4,512", "C(52, 3) = 22,100", "P = 1128/5525"],
  why="1201/5525 is the probability of at least one ace; 432/2197 treats the draws as made with replacement; 3/13 "
      "multiplies 1/13 by the three cards.", secs=90, by=BRUTE)

# ================================================================ Permutation and Combination (B1 I1 A1)
T = "Permutation and Combination"
cnt = sum(1 for p in itertools.permutations("ABCDEFG") if {p[0], p[-1]} == {"A", "B"})
assert cnt == 240 and 2 * math.factorial(6) == 1440
Q(T, "Arrangements", B, "In how many ways can 7 people stand in a queue if two particular people, Anil and Bina, "
  "must be at the two ends?",
  "240", ["120", "5,040", "1,440"],
  "Fix the ends (2 ways), then arrange the other 5 in the middle",
  "Anil and Bina take the two ends in 2 ways; the other 5 people fill the middle in 5! = 120 ways. Total = 240.",
  ["Ends: 2 ways", "Middle: 5! = 120", "2 × 120 = 240"],
  why="120 forgets that Anil and Bina can swap ends; 5,040 is 7! with no condition; 1,440 arranges 6 people in the "
      "middle.", secs=40, by=BRUTE)

grp = ["B"] * 6 + ["G"] * 4
cnt = sum(1 for t in itertools.combinations(range(10), 5)
          if sum(grp[i] == "G" for i in t) >= 2 and sum(grp[i] == "B" for i in t) <= 3)
assert cnt == 186 and math.comb(6, 3) * math.comb(4, 2) == 120 and math.comb(10, 5) - 6 == 246
Q(T, "Selections", I, "A group of 5 is to be chosen from 6 boys and 4 girls so that it has at least 2 girls and at "
  "most 3 boys. In how many ways can this be done?",
  "186", ["120", "246", "180"],
  "Possible make-ups: 3 boys + 2 girls, 2 boys + 3 girls, 1 boy + 4 girls",
  "C(6, 3)C(4, 2) = 20 × 6 = 120; C(6, 2)C(4, 3) = 15 × 4 = 60; C(6, 1)C(4, 4) = 6. Total = 186.",
  ["3B 2G: 120", "2B 3G: 60", "1B 4G: 6", "Total 186"],
  why="120 counts only 3 boys and 2 girls; 246 removes only the all-boy groups from C(10, 5) = 252; 180 forgets the "
      "1 boy + 4 girls groups.", secs=70, by=BRUTE)

words = set(itertools.permutations("COMMITTEE", 4))
assert len(words) == 738 and math.perm(6, 4) == 360 and math.perm(9, 4) == 3024
assert len({tuple(sorted(w)) for w in words}) == 48
Q(T, "Word arrangements", A, "How many different 4-letter arrangements (not necessarily meaningful) can be made from "
  "the letters of the word COMMITTEE?",
  "738", ["360", "3,024", "48"],
  "Letters: C, O, I once each; M, T, E twice each. Split by how many letters repeat",
  "All four different (from 6 distinct letters): 6 × 5 × 4 × 3 = 360. One pair + two different letters: 3 choices "
  "of pair × C(5, 2) = 10 others × 4!/2! = 12 ⇒ 360. Two pairs: C(3, 2) = 3 × 4!/(2! 2!) = 6 ⇒ 18. Total = 360 + "
  "360 + 18 = 738.",
  ["All different: 360", "One pair: 3 × 10 × 12 = 360", "Two pairs: 3 × 6 = 18", "Total 738"],
  why="360 counts only arrangements with four different letters; 3,024 treats all nine letters as different "
      "(⁹P₄); 48 counts selections of letters, not arrangements.", secs=120, by=BRUTE)

# ================================================================ Tabular DI (B6 I3 A2): sets of 6 and 5
T = "Tabular DI"
SHG = {"Kalyani": (64, 192, 144), "Madhupur": (48, 168, 105), "Nalbari": (75, 210, 168),
       "Pratapgarh": (56, 140, 119), "Rajgir": (80, 256, 160)}
sid = stimulus("data_table", "Loans to self-help groups at five bank branches under a livelihood mission, 2025-26",
               "The table shows, for five branches of a bank, the number of self-help groups (SHGs) financed under a "
               "rural livelihood mission in 2025-26, the amount disbursed to them and the amount repaid by "
               "31 March 2026 (amounts in ₹ lakh).\n\n" +
               md_table(["Branch", "SHGs financed", "Amount disbursed (₹ lakh)", "Amount repaid (₹ lakh)"],
                        [[k, a, b, c] for k, (a, b, c) in SHG.items()]),
               {"columns": ["branch", "shgs_financed", "disbursed_rs_lakh", "repaid_rs_lakh"],
                "rows": [[k, a, b, c] for k, (a, b, c) in SHG.items()]})
n_ = sum(v[0] for v in SHG.values())
assert n_ == 323 and sum(v[1] for v in SHG.values()) == 966 and n_ - 80 == 243 and n_ - 48 == 275
Q(T, "Single table", B, "How many self-help groups did the five branches finance in all?",
  "323", ["966", "243", "275"],
  "Add the 'SHGs financed' column",
  "64 + 48 + 75 + 56 + 80 = 323.",
  ["64 + 48 + 75 = 187", "56 + 80 = 136", "187 + 136 = 323"],
  why="966 adds the amounts disbursed; 243 leaves out Rajgir; 275 leaves out Madhupur.", secs=35, stim=sid)

per = {k: F(b, a) for k, (a, b, c) in SHG.items()}
assert unique_max(per) == "Madhupur" and per["Madhupur"] == F(7, 2) and unique_max(
    {k: b for k, (a, b, c) in SHG.items()}) == "Rajgir"
Q(T, "Single table", B, "Which branch disbursed the largest average loan per SHG?",
  "Madhupur", ["Rajgir", "Kalyani", "Nalbari"],
  "Average per SHG = amount disbursed ÷ SHGs financed",
  "Kalyani 3.0, Madhupur 3.5, Nalbari 2.8, Pratapgarh 2.5, Rajgir 3.2 (₹ lakh per SHG). Madhupur is the highest.",
  ["Kalyani 192/64 = 3.0", "Madhupur 168/48 = 3.5", "Nalbari 2.8, Pratapgarh 2.5, Rajgir 3.2"],
  why="Rajgir disbursed the largest total but to the most SHGs (3.2 each); Kalyani (3.0) and Nalbari (2.8) are "
      "lower.", secs=50, stim=sid)

assert 256 - 160 == 96 and 256 + 160 == 416
Q(T, "Single table", B, "How much of the amount disbursed by the Rajgir branch was still unpaid on 31 March 2026?",
  "₹96 lakh", ["₹160 lakh", "₹416 lakh", "₹256 lakh"],
  "Unpaid = disbursed − repaid",
  "Rajgir: 256 − 160 = ₹96 lakh.",
  ["256 − 160 = 96"],
  why="₹160 lakh is the amount repaid; ₹416 lakh adds the two figures; ₹256 lakh is the amount disbursed.", secs=30,
  stim=sid)

rep = {k: F(c, b) for k, (a, b, c) in SHG.items()}
assert unique_max(rep) == "Pratapgarh" and rep["Pratapgarh"] == F(85, 100) and unique_max(
    {k: c for k, (a, b, c) in SHG.items()}) == "Nalbari"
Q(T, "Table with percentages", I, "Which branch had recovered the highest percentage of the amount it disbursed?",
  "Pratapgarh", ["Nalbari", "Kalyani", "Rajgir"],
  "Recovery % = repaid ÷ disbursed × 100",
  "Kalyani 75%, Madhupur 62.5%, Nalbari 80%, Pratapgarh 85%, Rajgir 62.5%. Pratapgarh is the highest.",
  ["Kalyani 144/192 = 75%", "Nalbari 168/210 = 80%", "Pratapgarh 119/140 = 85%", "Madhupur, Rajgir 62.5%"],
  why="Nalbari recovered the largest amount (₹168 lakh) but only 80%; Kalyani recovered 75% and Rajgir 62.5%.",
  secs=60, stim=sid)

rp = sum(v[2] for v in SHG.values())
assert rp == 696 and pct2(F(rp, 966)) == "72.05%" and pct2(F(270, 966)) == "27.95%" and pct2(F(966, 696)) == "138.79%"
assert sum(rep.values()) / 5 == F(73, 100)
Q(T, "Table with percentages", I, "Taking the five branches together, what percentage of the amount disbursed had "
  "been repaid by 31 March 2026 (correct to two decimal places)?",
  "72.05%", ["73.00%", "27.95%", "138.79%"],
  "Overall percentage = total repaid ÷ total disbursed, not the average of the five percentages",
  "Total repaid = 144 + 105 + 168 + 119 + 160 = 696. Total disbursed = 966. 696 ÷ 966 = 72.05%.",
  ["Repaid = 696", "Disbursed = 966", "696 ÷ 966 = 72.05%"],
  why="73.00% averages the five branch percentages without weighting; 27.95% is the share still unpaid; 138.79% "
      "divides disbursed by repaid.", secs=65, stim=sid)

assert (F(7, 2) - F(5, 2)) / F(5, 2) == F(2, 5) and pct2(F(1, F(7, 2))) == "28.57%" and pct2(F(28, 140)) == "20.00%"
assert pct2(F(8, 48)) == "16.67%"
Q(T, "Single table", A, "By what percentage was the average loan per SHG at Madhupur higher than at Pratapgarh?",
  "40.00%", ["28.57%", "20.00%", "16.67%"],
  "Find each average loan first; then (difference ÷ Pratapgarh's average) × 100",
  "Madhupur: 168 ÷ 48 = ₹3.5 lakh. Pratapgarh: 140 ÷ 56 = ₹2.5 lakh. Higher by 1 ÷ 2.5 = 40.00%.",
  ["Madhupur = 3.5", "Pratapgarh = 2.5", "1 ÷ 2.5 = 40%"],
  why="28.57% divides the difference by Madhupur's average; 20.00% compares the total amounts (168 and 140); "
      "16.67% compares the numbers of SHGs the wrong way (8 ÷ 48).", secs=80, stim=sid)

MED = {"University A": (42, 30, 28), "University B": (25, 31, 36), "University C": (48, 44, 40),
       "University D": (20, 26, 22), "University E": (30, 28, 45)}
sid = stimulus("data_table", "Medals won by five universities at an inter-university games, 2026",
               "The table shows the gold, silver and bronze medals won by five universities at an inter-university "
               "sports meet in 2026. For the overall trophy, a gold counts 5 points, a silver 3 points and a bronze "
               "1 point.\n\n" +
               md_table(["University", "Gold", "Silver", "Bronze"], [[k, g_, s_, b_] for k, (g_, s_, b_) in MED.items()]),
               {"columns": ["university", "gold", "silver", "bronze"],
                "rows": [[k, g_, s_, b_] for k, (g_, s_, b_) in MED.items()]})
gt, st, bt = (sum(v[i] for v in MED.values()) for i in range(3))
assert (gt, st, bt) == (165, 159, 171) and gt + st + bt == 495
Q(T, "Single table", B, "How many gold medals did the five universities win in all?",
  "165", ["159", "171", "495"],
  "Add the gold column",
  "42 + 25 + 48 + 20 + 30 = 165.",
  ["42 + 25 + 48 = 115", "20 + 30 = 50", "115 + 50 = 165"],
  why="159 is the silver total; 171 is the bronze total; 495 is all medals.", secs=30, stim=sid)

tot = {k: sum(v) for k, v in MED.items()}
second = sorted(tot, key=tot.get, reverse=True)[1]
assert second == "University E" and tot["University E"] == 103 and tot["University A"] == 100
assert len(set(tot.values())) == 5
Q(T, "Single table", B, "Which university won the second-highest number of medals in all?",
  "University E", ["University A", "University B", "University D"],
  "Total medals = gold + silver + bronze for each university",
  "Totals: A 100, B 92, C 132, D 68, E 103. Highest C, then E (103).",
  ["A 100, B 92, C 132", "D 68, E 103", "Second: E"],
  why="University A has more golds than E but fewer medals in all (100); B (92) and D (68) are lower.", secs=40,
  stim=sid)

assert F(42, 28) == F(3, 2) and F(42, 30) == F(7, 5)
Q(T, "Single table", B, "What is the ratio of gold medals to bronze medals won by University A?",
  "3 : 2", ["2 : 3", "7 : 5", "21 : 50"],
  "Read the two figures and simplify",
  "University A: 42 gold and 28 bronze. 42 : 28 = 3 : 2.",
  ["42 : 28", "÷ 14 ⇒ 3 : 2"],
  why="2 : 3 is inverted; 7 : 5 uses the silver count (42 : 30); 21 : 50 compares gold with all 100 medals.",
  secs=30, stim=sid)

pts = {k: 5 * g_ + 3 * s_ + b_ for k, (g_, s_, b_) in MED.items()}
assert pts["University E"] == 279 and 3 * 30 + 2 * 28 + 45 == 191 and 150 + 84 + 90 == 324
Q(T, "Single table", I, "How many trophy points did University E score?",
  "279", ["103", "191", "324"],
  "Points = 5 × gold + 3 × silver + 1 × bronze",
  "University E: 5 × 30 + 3 × 28 + 45 = 150 + 84 + 45 = 279.",
  ["5 × 30 = 150", "3 × 28 = 84", "150 + 84 + 45 = 279"],
  why="103 is the number of medals; 191 scores 3, 2 and 1 points; 324 counts a bronze as 2 points.", secs=45,
  stim=sid)

srt = sorted(pts.values(), reverse=True)
assert unique_max(pts) == "University C" and srt[:2] == [412, 328] and 412 - 328 == 84
assert 412 - pts["University E"] == 133 and 132 - 100 == 32
Q(T, "Single table", A, "By how many trophy points did the winning university lead the runner-up?",
  "84", ["133", "32", "6"],
  "Score all five universities before deciding who is second; the runner-up on points need not have the second most "
  "medals",
  "Points: A 328, B 254, C 412, D 200, E 279. C wins with 412 and A is runner-up with 328. Lead = 84 points.",
  ["A 328, B 254, C 412", "D 200, E 279", "412 − 328 = 84"],
  why="133 takes University E (second in medals) as the runner-up; 32 is C's lead over A in medals; 6 is the "
      "difference in golds between C and A.", secs=90, stim=sid)

# ================================================================ Bar Graph DI (B2 I2 A2): one set of 6
T = "Bar Graph DI"
APP = {"Mar": (45, 120), "Apr": (80, 150), "May": (125, 190), "Jun": (110, 140), "Jul": (60, 70), "Aug": (40, 35)}
sid = stimulus("chart", "Air conditioners and air coolers sold by an appliance store, March to August 2026",
               "The grouped bar chart shows the number of air conditioners and air coolers sold by an appliance "
               "store in each month from March to August 2026 (values read from the bars). The average selling "
               "price was ₹38,000 for an air conditioner and ₹9,500 for an air cooler.\n\n" +
               md_table(["Month", "Air conditioners", "Air coolers"], [[k, a, c] for k, (a, c) in APP.items()]),
               {"chart_type": "bar", "x": list(APP),
                "series": [{"name": "Air conditioners", "values": [a for a, c in APP.values()]},
                           {"name": "Air coolers", "values": [c for a, c in APP.values()]}]})
ac, co = sum(a for a, c in APP.values()), sum(c for a, c in APP.values())
assert (ac, co) == (460, 705) and ac + co == 1165 and ac - 40 == 420
Q(T, "Stacked or grouped bar", B, "How many air conditioners did the store sell from March to August?",
  "460", ["705", "1,165", "420"],
  "Add the six air-conditioner bars",
  "45 + 80 + 125 + 110 + 60 + 40 = 460.",
  ["45 + 80 + 125 = 250", "110 + 60 + 40 = 210", "250 + 210 = 460"],
  why="705 is the number of coolers; 1,165 adds both; 420 leaves out August.", secs=35, stim=sid)

assert [k for k, (a, c) in APP.items() if a > c] == ["Aug"]
Q(T, "Stacked or grouped bar", B, "In which month did the store sell more air conditioners than air coolers?",
  "August", ["July", "May", "June"],
  "Compare the two bars month by month",
  "Only in August (40 against 35) does the air-conditioner bar stand taller.",
  ["Mar–Jul: coolers ahead", "Aug: 40 > 35"],
  why="July is the closest other month (60 against 70) but coolers still lead; May has the most air conditioners, "
      "and June the second most, yet coolers outsell them in both.", secs=35, stim=sid)

assert F(co, 6) == F(235, 2) and F(co, 5) == 141 and r2(F(co, 7)) == F("100.71") and F(190 + 35, 2) == F(225, 2)
Q(T, "Simple bar", I, "What was the average number of air coolers sold per month over the six months?",
  "117.5", ["141", "100.71", "112.5"],
  "Average = total ÷ 6",
  "Coolers: 120 + 150 + 190 + 140 + 70 + 35 = 705. 705 ÷ 6 = 117.5.",
  ["Total = 705", "÷ 6 = 117.5"],
  why="141 divides by 5; 100.71 divides by 7; 112.5 is the mid-point of the highest (190) and lowest (35) bars.",
  secs=45, stim=sid)

assert pct2(F(190, 315)) == "60.32%" and pct2(F(125, 315)) == "39.68%" and pct2(F(190, 125)) == "152.00%"
assert pct2(F(125, 190)) == "65.79%"
Q(T, "Stacked or grouped bar", I, "In May, air coolers made up what percentage of the units sold of the two products "
  "together (correct to two decimal places)?",
  "60.32%", ["152.00%", "39.68%", "65.79%"],
  "Share = coolers ÷ (coolers + air conditioners) × 100",
  "May: 190 coolers and 125 air conditioners, 315 in all. 190 ÷ 315 = 60.32%.",
  ["Total = 315", "190 ÷ 315 = 60.32%"],
  why="152.00% divides coolers by air conditioners; 39.68% is the air-conditioner share; 65.79% divides air "
      "conditioners by coolers.", secs=45, stim=sid)

rev = {k: a * 38000 + c * 9500 for k, (a, c) in APP.items()}
assert rev["Apr"] == 4465000 and rev["Jun"] == 5510000
assert pct2(F(rev["Jun"] - rev["Apr"], rev["Apr"])) == "23.40%" and pct2(F(250 - 230, 230)) == "8.70%"
assert pct2(F(30, 80)) == "37.50%" and pct2(F(1045000, 5510000)) == "18.97%"
Q(T, "Stacked or grouped bar", A, "By what percentage was the store's revenue from the two products in June higher "
  "than in April (correct to two decimal places)?",
  "23.40%", ["8.70%", "37.50%", "18.97%"],
  "Revenue = units × average price for each product; the two prices differ greatly",
  "April: 80 × 38,000 + 150 × 9,500 = 30,40,000 + 14,25,000 = ₹44,65,000. June: 110 × 38,000 + 140 × 9,500 = "
  "41,80,000 + 13,30,000 = ₹55,10,000. Rise = 10,45,000 ÷ 44,65,000 = 23.40%.",
  ["April = 44,65,000", "June = 55,10,000", "10,45,000 ÷ 44,65,000 = 23.40%"],
  why="8.70% compares the units sold (230 and 250); 37.50% compares only the air conditioners; 18.97% divides the "
      "rise by June's revenue.", secs=100, stim=sid)

rc, ra = co * 9500, ac * 38000
assert pct2(F(rc, ra)) == "38.32%" and pct2(F(co, ac)) == "153.26%" and pct2(F(rc, rc + ra)) == "27.70%"
Q(T, "Stacked or grouped bar", A, "Over the six months, the revenue from air coolers was what percentage of the "
  "revenue from air conditioners (correct to two decimal places)?",
  "38.32%", ["153.26%", "27.70%", "25.00%"],
  "Revenue of each product over six months = total units × average price",
  "Coolers: 705 × 9,500 = ₹66,97,500. Air conditioners: 460 × 38,000 = ₹1,74,80,000. 66,97,500 ÷ 1,74,80,000 = "
  "38.32%.",
  ["Coolers = 66,97,500", "ACs = 1,74,80,000", "Ratio = 38.32%"],
  why="153.26% compares the units sold; 27.70% is the coolers' share of the combined revenue; 25.00% compares only "
      "the prices (9,500 ÷ 38,000).", secs=90, stim=sid)

# ================================================================ Pie Chart DI (B2 I3 A2): sets of 4 and 3
T = "Pie Chart DI"
HOUSE = {"Cement": 18, "Steel": 16, "Bricks and sand": 14, "Labour": 25, "Timber and fittings": 12,
         "Electrical and plumbing": 9, "Supervision and approvals": 6}
assert sum(HOUSE.values()) == 100
sid = stimulus("chart", "Cost of building a house, by head (percentages)",
               "The pie chart shows how the total cost of ₹48 lakh of building a house was divided among various "
               "heads, as percentages of the total.\n\n" +
               md_table(["Head", "Share of total cost (%)"], [[k, v] for k, v in HOUSE.items()]),
               {"chart_type": "pie", "unit": "percent", "labels": list(HOUSE), "values": list(HOUSE.values()),
                "total_rs_lakh": 48})
assert 48 * F(25, 100) == 12 and 48 * F(18, 100) == F(864, 100) and 48 * F(16, 100) == F(768, 100)
Q(T, "Percentage-based", B, "How much was spent on labour?",
  "₹12 lakh", ["₹25 lakh", "₹8.64 lakh", "₹7.68 lakh"],
  "Amount = share × total cost",
  "Labour = 25% of ₹48 lakh = ₹12 lakh.",
  ["25% of 48 = 12"],
  why="₹25 lakh reads the percentage as lakh; ₹8.64 lakh is cement (18%); ₹7.68 lakh is steel (16%).", secs=30,
  stim=sid)

assert 12 * F(36, 10) == F(432, 10) and 9 * F(36, 10) == F(324, 10)
Q(T, "Percentage-based", B, "If the data were drawn as a pie chart in degrees, what would be the central angle of "
  "the 'Timber and fittings' sector?",
  "43.2°", ["12°", "36°", "32.4°"],
  "Central angle = percentage × 3.6",
  "12% × 360° ÷ 100 = 43.2°.",
  ["12 × 3.6 = 43.2°"],
  why="12° reads the percentage as degrees; 36° is 10% of 360°; 32.4° is the electrical and plumbing sector (9%).",
  secs=30, stim=sid)

assert 48 * F(18 + 16 - 14, 100) == F(96, 10) and 48 * F(34, 100) == F(1632, 100) and 48 * F(14, 100) == F(672, 100)
Q(T, "Percentage-based", I, "By how much did the cost of cement and steel together exceed the cost of bricks and "
  "sand?",
  "₹9.6 lakh", ["₹16.32 lakh", "₹6.72 lakh", "₹20 lakh"],
  "Work with percentages first: (18 + 16 − 14)% of ₹48 lakh",
  "(18 + 16 − 14)% = 20% of ₹48 lakh = ₹9.6 lakh.",
  ["18 + 16 = 34%", "34 − 14 = 20%", "20% of 48 = 9.6 lakh"],
  why="₹16.32 lakh is cement and steel together, without subtracting; ₹6.72 lakh is bricks and sand alone; ₹20 lakh "
      "reads the 20% difference as lakh.", secs=50, stim=sid)

new_l, new_t = 12 * F(6, 5), 48 + 12 * F(1, 5)
assert pct2(new_l / new_t) == "28.57%" and pct2(F(12, new_t)) == "23.81%" and 25 * F(6, 5) == 30
Q(T, "Percentage-based", A, "If the labour cost had been 20% higher, with every other cost unchanged, what share of "
  "the total cost would labour have taken (correct to two decimal places)?",
  "28.57%", ["30.00%", "25.00%", "23.81%"],
  "A rise in one head also raises the total, so the new share = new labour ÷ new total",
  "Labour rises from ₹12 lakh to ₹14.4 lakh; the total rises from ₹48 lakh to ₹50.4 lakh. Share = 14.4 ÷ 50.4 = "
  "28.57%.",
  ["Labour = 14.4 lakh", "Total = 50.4 lakh", "14.4 ÷ 50.4 = 28.57%"],
  why="30.00% raises the share by 20% but forgets that the total also rises; 25.00% is the original share; 23.81% "
      "divides the old labour cost by the new total.", secs=90, stim=sid)

CC = {"Travel": (15, 18), "Dining": (12, 14), "Groceries": (20, 16), "Fuel": (10, 9), "Shopping": (28, 30),
      "Utilities": (15, 13)}
assert sum(a for a, b in CC.values()) == 100 and sum(b for a, b in CC.values()) == 100
sid = stimulus("chart", "Credit-card spending by a bank's customers by category, 2025 and 2026 (two pie charts)",
               "The two pie charts show how the credit-card spending of a bank's customers was divided among six "
               "categories in 2025 and in 2026, as percentages. Total spending was ₹240 crore in 2025 and ₹300 crore "
               "in 2026.\n\n" +
               md_table(["Category", "2025 share (%)", "2026 share (%)"], [[k, a, b] for k, (a, b) in CC.items()]),
               {"chart_type": "pie", "unit": "percent", "labels": list(CC),
                "series": [{"name": "2025", "values": [a for a, b in CC.values()], "total_rs_crore": 240},
                           {"name": "2026", "values": [b for a, b in CC.values()], "total_rs_crore": 300}]})
amt = {k: (240 * F(a, 100), 300 * F(b, 100)) for k, (a, b) in CC.items()}
assert amt["Travel"][1] - amt["Travel"][0] == 18 and 300 * F(3, 100) == 9 and 240 * F(3, 100) == F(72, 10)
Q(T, "Two pie charts", I, "By how much did spending on travel rise from 2025 to 2026?",
  "₹18 crore", ["₹9 crore", "₹7.2 crore", "₹54 crore"],
  "Convert each year's share into rupees with that year's own total",
  "2025: 15% of 240 = ₹36 crore. 2026: 18% of 300 = ₹54 crore. Rise = ₹18 crore.",
  ["2025: 36 crore", "2026: 54 crore", "Rise = 18 crore"],
  why="₹9 crore applies the 3-point rise in share to 2026's total; ₹7.2 crore applies it to 2025's total; ₹54 crore "
      "is the 2026 figure itself.", secs=50, stim=sid)

rose_share_fell = [k for k, (a, b) in CC.items() if b < a and amt[k][1] > amt[k][0]]
assert rose_share_fell == ["Fuel", "Utilities"] and amt["Groceries"][0] == amt["Groceries"][1] == 48
Q(T, "Two pie charts", I, "In how many categories did the spending in rupees rise from 2025 to 2026 even though the "
  "category's percentage share fell?",
  "2", ["3", "0", "1"],
  "A smaller share of a larger total can still be a larger amount; compare rupees, not percentages",
  "Shares fell for groceries, fuel and utilities. Groceries: 48 → 48 crore (no rise). Fuel: 24 → 27 crore (rise). "
  "Utilities: 36 → 39 crore (rise). So 2 categories.",
  ["Groceries 48 → 48", "Fuel 24 → 27", "Utilities 36 → 39", "Answer: 2"],
  why="3 counts groceries, whose spending stayed exactly the same; 0 assumes a falling share always means falling "
      "spending; 1 misses one of fuel and utilities.", secs=75, stim=sid)

d0, d1 = amt["Dining"]
assert (d0, d1) == (F(288, 10), 42) and pct2(F(d1 - d0, d0)) == "45.83%" and pct2(F(2, 12)) == "16.67%"
assert pct2(F(d1 - d0, d1)) == "31.43%"
Q(T, "Two pie charts", A, "By what percentage did spending on dining rise from 2025 to 2026 (correct to two decimal "
  "places)?",
  "45.83%", ["16.67%", "25.00%", "31.43%"],
  "Convert both shares to rupees, then (rise ÷ 2025 amount) × 100",
  "2025: 12% of 240 = ₹28.8 crore. 2026: 14% of 300 = ₹42 crore. Rise = 13.2 ÷ 28.8 = 45.83%.",
  ["2025: 28.8 crore", "2026: 42 crore", "13.2 ÷ 28.8 = 45.83%"],
  why="16.67% compares only the shares (12% to 14%); 25.00% is the rise in total spending; 31.43% divides the rise "
      "by the 2026 amount.", secs=80, stim=sid)

# ================================================================ Line Graph DI (B2 I3 A1): one set of 6
T = "Line Graph DI"
RES = {"Jan": (820, 640), "Feb": (760, 610), "Mar": (690, 580), "Apr": (610, 530), "May": (540, 470),
       "Jun": (580, 520)}
sid = stimulus("chart", "Water stored in two reservoirs on the first day of each month, January to June 2026",
               "The line graph shows the water stored (in million cubic metres) in two reservoirs, Kesar and Neela, "
               "on the first day of each month from January to June 2026 (values read from the graph). Kesar can "
               "hold 1,000 and Neela 800 million cubic metres when full.\n\n" +
               md_table(["Month (1st day)", "Kesar", "Neela"], [[k, a, b] for k, (a, b) in RES.items()]),
               {"chart_type": "line", "x": list(RES), "unit": "million cubic metres",
                "series": [{"name": "Kesar", "values": [a for a, b in RES.values()]},
                           {"name": "Neela", "values": [b for a, b in RES.values()]}]})
comb = {k: a + b for k, (a, b) in RES.items()}
assert unique_min(comb) == "May" and comb["May"] == 1010 and comb["Apr"] == 1140 and comb["Jun"] == 1100
Q(T, "Multiple lines", B, "On the first day of which month was the total water stored in the two reservoirs the "
  "lowest?",
  "May", ["April", "June", "March"],
  "Add the two lines for each month",
  "Totals: Jan 1,460, Feb 1,370, Mar 1,270, Apr 1,140, May 1,010, Jun 1,100. May is the lowest.",
  ["Mar 1,270, Apr 1,140", "May 1,010, Jun 1,100", "Lowest: May"],
  why="April (1,140) and March (1,270) are higher; June (1,100) is after the storage began to recover.", secs=40,
  stim=sid)

assert 820 - 540 == 280 and 820 - 580 == 240 and 640 - 470 == 170
Q(T, "Single line", B, "By how much did the water stored in Kesar fall from 1 January to 1 May?",
  "280 million m³", ["240 million m³", "170 million m³", "60 million m³"],
  "Fall = January value − May value on the Kesar line",
  "820 − 540 = 280 million cubic metres.",
  ["820 − 540 = 280"],
  why="240 runs to June instead of May; 170 is Neela's fall; 60 is only the January-to-February fall.", secs=30,
  stim=sid)

assert pct2(F(530, 800)) == "66.25%" and pct2(F(530, 1000)) == "53.00%" and pct2(F(800, 530)) == "150.94%"
assert pct2(F(530, 820)) == "64.63%"
Q(T, "Single line", I, "On 1 April, Neela held what percentage of its full capacity (correct to two decimal "
  "places)?",
  "66.25%", ["53.00%", "150.94%", "64.63%"],
  "Percentage of capacity = stored ÷ capacity × 100, using Neela's capacity of 800",
  "530 ÷ 800 = 66.25%.",
  ["530 ÷ 800", "= 66.25%"],
  why="53.00% uses Kesar's capacity (1,000); 150.94% divides capacity by storage; 64.63% divides by Kesar's January "
      "storage (820).", secs=40, stim=sid)

ks = sum(a for a, b in RES.values())
assert ks == 4000 and r2(F(ks, 6)) == F("666.67") and F(ks, 5) == 800 and F(820 + 540, 2) == 680
assert r2(F(ks, 7)) == F("571.43")
Q(T, "Single line", I, "What was the average water stored in Kesar on the first days of the six months (in million "
  "cubic metres, correct to two decimal places)?",
  "666.67", ["800", "680", "571.43"],
  "Average = sum of the six readings ÷ 6",
  "820 + 760 + 690 + 610 + 540 + 580 = 4,000. 4,000 ÷ 6 = 666.67.",
  ["Sum = 4,000", "÷ 6 = 666.67"],
  why="800 divides by 5; 680 is the mid-point of the highest and lowest readings; 571.43 divides by 7.", secs=45,
  stim=sid)

ms = list(RES)
falls = {f"{ms[i]}–{ms[i + 1]}": RES[ms[i]][1] - RES[ms[i + 1]][1] for i in range(5)}
assert unique_max(falls) == "Apr–May" and falls["Apr–May"] == 60 and falls["Mar–Apr"] == 50
Q(T, "Single line", I, "Between the first days of which two consecutive months did the water stored in Neela fall the "
  "most?",
  "April and May", ["March and April", "January and February", "May and June"],
  "Find the drop between each pair of neighbouring points on the Neela line",
  "Drops: Jan–Feb 30, Feb–Mar 30, Mar–Apr 50, Apr–May 60, May–Jun a rise of 50. The largest fall is April to May "
  "(60).",
  ["Jan–Feb 30, Feb–Mar 30", "Mar–Apr 50, Apr–May 60", "May–Jun: rise"],
  why="March–April (50) is the second-largest fall; January–February is only 30; between May and June the storage "
      "rose.", secs=55, stim=sid)

j_, u_ = F(1460, 1800) * 100, F(1100, 1800) * 100
assert j_ - u_ == 20 and r2(F(360, 1460) * 100) == F("24.66") and (F(82 - 58) + F(80 - 65)) / 2 == F(39, 2)
Q(T, "Multiple lines", A, "Taking the two reservoirs together, by how many percentage points did the water stored, "
  "as a percentage of their combined capacity, fall from 1 January to 1 June?",
  "20 percentage points", ["24.66 percentage points", "19.5 percentage points", "36 percentage points"],
  "Combined percentage = combined storage ÷ combined capacity (1,800) × 100 on each date",
  "1 January: 1,460 ÷ 1,800 = 81.11%. 1 June: 1,100 ÷ 1,800 = 61.11%. Fall = 20 percentage points.",
  ["Jan: 1,460/1,800 = 81.11%", "Jun: 1,100/1,800 = 61.11%", "Fall = 20 points"],
  why="24.66 is the percentage fall in storage (360 ÷ 1,460), not a fall in percentage points; 19.5 averages the "
      "two reservoirs' falls (24 and 15 points) without weighting by capacity; 36 divides the 360 fall by 10.",
  secs=100, stim=sid)

# ================================================================ Caselet DI (B3 I2 A2): sets of 4 and 3
T = "Caselet DI"
FLW = {"Roses": (1200, 12, F(90, 100), 30), "Lilies": (400, 35, F(75, 100), 60), "Orchids": (150, 90, F(80, 100), 150)}
sid = stimulus("passage", "A florist's roses, lilies and orchids in Valentine's week",
               "For Valentine's week a florist bought 1,200 roses at ₹12 each, 400 lilies at ₹35 each and 150 "
               "orchids at ₹90 each. She sold 90% of the roses at ₹30 each, 75% of the lilies at ₹60 each and 80% "
               "of the orchids at ₹150 each. Flowers left unsold wilted and were thrown away.")
sold = {k: n * f for k, (n, c, f, p) in FLW.items()}
assert all(x.denominator == 1 for x in sold.values())
waste = {k: FLW[k][0] - sold[k] for k in FLW}
assert sum(waste.values()) == 250 and waste["Roses"] + waste["Lilies"] == 220 and waste["Roses"] == 120
Q(T, "Paragraph data", B, "How many flowers in all were thrown away?",
  "250", ["1,500", "220", "120"],
  "Unsold = bought − sold, for each kind",
  "Roses 10% of 1,200 = 120; lilies 25% of 400 = 100; orchids 20% of 150 = 30. Total = 250.",
  ["120 + 100 + 30 = 250"],
  why="1,500 is the number sold; 220 leaves out the orchids; 120 counts only the roses.", secs=40, stim=sid)

rev = {k: sold[k] * FLW[k][3] for k in FLW}
cost = {k: FLW[k][0] * FLW[k][1] for k in FLW}
assert rev["Lilies"] == 18000 and 400 * 60 == 24000 and cost["Lilies"] == 14000 and rev["Lilies"] - cost["Lilies"] == 4000
Q(T, "Paragraph data", B, "How much did the florist receive from selling lilies?",
  "₹18,000", ["₹24,000", "₹14,000", "₹4,000"],
  "Revenue = number sold × selling price",
  "Lilies sold = 75% of 400 = 300; 300 × 60 = ₹18,000.",
  ["Sold = 300", "300 × 60 = 18,000"],
  why="₹24,000 assumes all 400 were sold; ₹14,000 is what the lilies cost; ₹4,000 is the profit on lilies.",
  secs=40, stim=sid)

po = rev["Orchids"] - cost["Orchids"]
assert po == 4500 and pct2(F(po, cost["Orchids"])) == "33.33%" and pct2(F(po, rev["Orchids"])) == "25.00%"
assert pct2(F(60, 90)) == "66.67%"
Q(T, "Paragraph data", I, "What was the florist's profit on orchids as a percentage of what the orchids cost "
  "(correct to two decimal places)?",
  "33.33%", ["66.67%", "25.00%", "40.00%"],
  "Profit = revenue from those sold − cost of all bought (unsold ones are a loss)",
  "Cost = 150 × 90 = ₹13,500. Sold = 120 at ₹150 = ₹18,000. Profit = ₹4,500. 4,500 ÷ 13,500 = 33.33%.",
  ["Cost = 13,500", "Revenue = 18,000", "4,500 ÷ 13,500 = 33.33%"],
  why="66.67% is the margin on each orchid sold (60 ÷ 90), ignoring the 30 thrown away; 25.00% divides the profit "
      "by the revenue; 40.00% is a guess based on the 20% thrown away.", secs=60, stim=sid)

tc, tr = sum(cost.values()), sum(rev.values())
assert (tc, tr) == (41900, 68400) and pct2(F(tr - tc, tc)) == "63.25%" and pct2(F(tr - tc, tr)) == "38.74%"
full = sum(FLW[k][0] * FLW[k][3] for k in FLW)
assert full == 82500 and pct2(F(full - tc, tc)) == "96.90%"
assert pct2(sum(F(rev[k] - cost[k], cost[k]) for k in FLW) / 3) == "62.30%"
Q(T, "Paragraph data", A, "What was the florist's overall profit percentage on the three kinds of flowers together "
  "(correct to two decimal places)?",
  "63.25%", ["38.74%", "96.90%", "62.30%"],
  "Overall profit % = (total revenue − total cost) ÷ total cost × 100",
  "Cost = 14,400 + 14,000 + 13,500 = ₹41,900. Revenue = 32,400 + 18,000 + 18,000 = ₹68,400. Profit = ₹26,500. "
  "26,500 ÷ 41,900 = 63.25%.",
  ["Cost = 41,900", "Revenue = 68,400", "26,500 ÷ 41,900 = 63.25%"],
  why="38.74% divides the profit by the revenue; 96.90% assumes every flower was sold; 62.30% averages the three "
      "separate profit percentages (125%, 28.57%, 33.33%) without weighting.", secs=100, stim=sid)

BUS = {"adults": (65, 2400), "seniors": (40, 1800), "children": (15, 1200)}
sid = stimulus("passage", "A tour operator's pilgrimage bus trip",
               "A tour operator ran a pilgrimage trip with 3 buses of 45 seats each, and 120 passengers travelled. "
               "The full fare was ₹2,400. Forty of the passengers were senior citizens, who got a 25% concession; 15 "
               "were children, who paid half the full fare; the rest paid the full fare. Hiring each bus cost the "
               "operator ₹45,000, and meals cost him ₹350 per passenger.")
assert sum(n for n, f in BUS.values()) == 120 and BUS["seniors"][1] == 2400 * F(3, 4) and BUS["children"][1] == 1200
assert 3 * 45 - 120 == 15
Q(T, "Paragraph data", B, "How many seats were empty on the trip?",
  "15", ["5", "25", "120"],
  "Seats = 3 × 45",
  "Seats = 135; passengers = 120; empty seats = 15.",
  ["3 × 45 = 135", "135 − 120 = 15"],
  why="5 is the average number of empty seats per bus; 25 miscounts the seats as 145; 120 is the number of "
      "passengers.", secs=30, stim=sid)

fare = sum(n * f for n, f in BUS.values())
assert fare == 246000 and 120 * 2400 == 288000 and fare + 15 * 1200 == 264000 and fare - 40 * 600 == 222000
Q(T, "Paragraph data", I, "How much did the operator collect in fares?",
  "₹2,46,000", ["₹2,88,000", "₹2,64,000", "₹2,22,000"],
  "Adults = 120 − 40 − 15 = 65; seniors pay 75% of ₹2,400 = ₹1,800; children pay ₹1,200",
  "65 × 2,400 = 1,56,000; 40 × 1,800 = 72,000; 15 × 1,200 = 18,000. Total = ₹2,46,000.",
  ["Adults: 1,56,000", "Seniors: 72,000", "Children: 18,000", "Total 2,46,000"],
  why="₹2,88,000 charges everyone the full fare; ₹2,64,000 charges the children the full fare; ₹2,22,000 gives the "
      "seniors 50% off instead of 25%.", secs=60, stim=sid)

cost = 3 * 45000 + 120 * 350
assert cost == 177000 and fare - cost == 69000 and fare - 135000 == 111000 and fare - 135000 - 135 * 350 == 63750
assert fare - 120 * 350 == 204000
Q(T, "Paragraph data", A, "What was the operator's profit on the trip?",
  "₹69,000", ["₹1,11,000", "₹63,750", "₹2,04,000"],
  "Profit = fares − (bus hire for 3 buses + meals for the passengers)",
  "Costs = 3 × 45,000 + 120 × 350 = 1,35,000 + 42,000 = ₹1,77,000. Profit = 2,46,000 − 1,77,000 = ₹69,000.",
  ["Fares = 2,46,000", "Costs = 1,77,000", "Profit = 69,000"],
  why="₹1,11,000 leaves out the meals; ₹63,750 pays for meals for all 135 seats; ₹2,04,000 leaves out the bus "
      "hire.", secs=90, stim=sid)

# ================================================================ Missing DI (B1 I2 A3): one set of 6
T = "Missing DI"
SH = {"Farah": (400, 250, F(1, 2)), "Gopal": (700, 180, F(4, 10)), "Hema": (250, 600, F(3, 10)),
      "Irfan": (1200, 95, F(1, 2)), "Jaya": (800, 320, F(1, 4))}
full_rows = {k: (n, p, n * p, r, n * p * r / 100) for k, (n, p, r) in SH.items()}
assert all(x[4].denominator == 1 for x in full_rows.values())
HIDE = {("Gopal", 0), ("Gopal", 4), ("Hema", 1), ("Hema", 3), ("Irfan", 2), ("Irfan", 4), ("Jaya", 0), ("Jaya", 2)}
shown = [[k] + ["—" if (k, i) in HIDE else (N(x) if i == 3 else ind(int(x))) for i, x in enumerate(row)]
         for k, row in full_rows.items()]
sid = stimulus("data_table", "Shares bought by five investors through a broker (some values missing)",
               "The table gives, for five investors who bought shares through a broker, the number of shares bought, "
               "the price per share, the value of the purchase, the brokerage rate (as a percentage of the value) "
               "and the brokerage paid. Some values are missing (—).\n\n" +
               md_table(["Investor", "Shares", "Price per share (₹)", "Value (₹)", "Brokerage rate (%)",
                         "Brokerage (₹)"], shown),
               {"columns": ["investor", "shares", "price_rs", "value_rs", "brokerage_pct", "brokerage_rs"],
                "rows": [[r[0]] + [None if c == "—" else float(c.replace(",", "")) for c in r[1:]] for r in shown]})
assert F(126000, 180) == 700 and F(126000 * 4, 1000) == 504
Q(T, "Table with missing values", B, "How many shares did Gopal buy?",
  "700", ["70", "7,000", "504"],
  "Shares = value ÷ price per share",
  "1,26,000 ÷ 180 = 700 shares.",
  ["1,26,000 ÷ 180 = 700"],
  why="70 and 7,000 slip a factor of 10; 504 is Gopal's brokerage in rupees.", secs=30, stim=sid)

assert F(450 * 100, 150000) == F(3, 10) and F(150000, 250) == 600
Q(T, "Table with missing values", I, "What brokerage rate did Hema pay?",
  "0.3%", ["3%", "0.03%", "0.45%"],
  "Rate = brokerage ÷ value × 100",
  "450 ÷ 1,50,000 × 100 = 0.3%.",
  ["450 ÷ 1,50,000 = 0.003", "= 0.3%"],
  why="3% and 0.03% misplace the decimal point; 0.45% divides 450 by 1,00,000 instead of 1,50,000.", secs=45,
  stim=sid)

vi, vj = 1200 * 95, F(640 * 100, F(1, 4))
assert vi == 114000 and vj == 256000 and vi + vj == 370000 and vi + F(640, F(1, 4)) == 116560
Q(T, "Table with missing values", I, "What was the total value of the shares bought by Irfan and Jaya together?",
  "₹3,70,000", ["₹1,14,000", "₹2,56,000", "₹1,16,560"],
  "Irfan: value = shares × price. Jaya: value = brokerage ÷ rate × 100",
  "Irfan: 1,200 × 95 = ₹1,14,000. Jaya: 640 ÷ 0.25 × 100 = ₹2,56,000. Together ₹3,70,000.",
  ["Irfan = 1,14,000", "Jaya = 2,56,000", "Total = 3,70,000"],
  why="₹1,14,000 and ₹2,56,000 are each investor alone; ₹1,16,560 forgets the × 100 for the percentage in Jaya's "
      "value (640 ÷ 0.25 = 2,560).", secs=60, stim=sid)

brk = {k: v[4] for k, v in full_rows.items()}
assert sum(brk.values()) == 2664 and 500 + 450 + 640 == 1590 and 2664 - 504 == 2160 and 2664 - 570 == 2094
Q(T, "Table with missing values", A, "What was the total brokerage paid by the five investors?",
  "₹2,664", ["₹1,590", "₹2,160", "₹2,094"],
  "Fill in the missing brokerage for Gopal (0.4% of 1,26,000) and Irfan (0.5% of 1,14,000), then add",
  "Gopal: 0.4% of 1,26,000 = 504. Irfan: 0.5% of 1,14,000 = 570. Total = 500 + 504 + 450 + 570 + 640 = ₹2,664.",
  ["Gopal 504", "Irfan 570", "500 + 504 + 450 + 570 + 640 = 2,664"],
  why="₹1,590 adds only the three given values; ₹2,160 leaves out Gopal; ₹2,094 leaves out Irfan.", secs=80,
  stim=sid)

tv, ts = sum(v[2] for v in full_rows.values()), sum(v[0] for v in full_rows.values())
assert (tv, ts) == (746000, 3350) and r2(F(tv, ts)) == F("222.69") and r2(F(tv + 2664, ts)) == F("223.48")
assert F(250 + 180 + 600 + 95 + 320, 5) == 289 and F(tv, 5) == 149200
Q(T, "Table with missing values", A, "What was the average price per share paid on all the shares bought by the five "
  "investors (excluding brokerage, correct to two decimal places)?",
  "₹222.69", ["₹289.00", "₹223.48", "₹1,49,200.00"],
  "Average price = total value ÷ total shares, after filling in every missing value",
  "Values: 1,00,000 + 1,26,000 + 1,50,000 + 1,14,000 + 2,56,000 = ₹7,46,000. Shares: 400 + 700 + 250 + 1,200 + 800 = "
  "3,350. Average = 7,46,000 ÷ 3,350 = ₹222.69.",
  ["Total value = 7,46,000", "Total shares = 3,350", "7,46,000 ÷ 3,350 = 222.69"],
  why="₹289.00 averages the five prices without weighting by the number of shares; ₹223.48 includes the brokerage; "
      "₹1,49,200 is the average value per investor.", secs=110, stim=sid)

pps = {k: v[4] / v[0] for k, v in full_rows.items()}
assert unique_max(pps) == "Hema" and pps["Hema"] == F(9, 5) and unique_max(brk) == "Jaya"
Q(T, "Table with missing values", A, "Which investor paid the highest brokerage per share bought?",
  "Hema", ["Jaya", "Farah", "Gopal"],
  "Brokerage per share = brokerage ÷ number of shares (fill in Gopal's and Jaya's shares first)",
  "Farah 500/400 = 1.25; Gopal 504/700 = 0.72; Hema 450/250 = 1.80; Irfan 570/1,200 = 0.475; Jaya 640/800 = 0.80. "
  "Hema is the highest.",
  ["Farah 1.25, Gopal 0.72", "Hema 1.80, Irfan 0.475", "Jaya 0.80 ⇒ Hema"],
  why="Jaya paid the most brokerage in all but spread over 800 shares; Farah (1.25) is second; Gopal pays only 0.72 "
      "per share.", secs=90, stim=sid)

# ================================================================ Quantity Comparison (B2 I2 A4)
assert 2 * (17 + 9) == 52 and F(22, 7) * 14 == 44
qc("Quantity I vs II", B, "Perimeter (cm) of a rectangle measuring 17 cm × 9 cm",
   "Circumference (cm) of a circle of diameter 14 cm (take π = 22/7)", [F(52)], [F(44)], ">", ["<", "<="],
   "Perimeter = 2(l + b); circumference = πd",
   "Quantity I: 2 × 26 = 52. Quantity II: 22/7 × 14 = 44. 52 > 44.",
   ["I: 52", "II: 44", "52 > 44"],
   why="'I < II' and 'I ≤ II' come from using 2πd = 88 for the circle or adding only two sides of the rectangle "
       "(26).", secs=40)

m6 = [n for n in range(10, 100) if n % 6 == 0]
assert len(m6) == 15 and 7 * 4 // 2 == 14
qc("Quantity I vs II", B, "The number of two-digit numbers divisible by 6", "The number of diagonals of a heptagon",
   [F(15)], [F(14)], ">", ["<", "<="],
   "Two-digit multiples of 6 run from 12 to 96; diagonals of an n-gon = n(n − 3)/2",
   "Quantity I: 12 = 6 × 2 to 96 = 6 × 16, so 16 − 2 + 1 = 15. Quantity II: 7 × 4 ÷ 2 = 14. 15 > 14.",
   ["I: 6 × 2 to 6 × 16 ⇒ 15", "II: 7 × 4 ÷ 2 = 14", "15 > 14"],
   why="'I < II' and 'I ≤ II' come from counting the multiples as 16 − 2 = 14 or the diagonals as 7 × 6 ÷ 2 = 21.",
   secs=45, by=BRUTE)

q1_, q2_ = 1 / (F(1, 8) - F(1, 24)), 1 / (F(1, 6) - F(1, 10))
assert (q1_, q2_) == (12, 15)
qc("Arithmetic-based comparison", I, "Hours taken to fill a tank by a pipe that alone fills it in 8 hours, while a "
   "leak that alone empties the full tank in 24 hours is open",
   "Hours taken by pipe P alone to fill a tank that pipes P and Q together fill in 6 hours and Q alone fills in 10 "
   "hours",
   [q1_], [q2_], "<", [">", ">="],
   "Net rate = fill rate − leak rate; P's rate = (P + Q)'s rate − Q's rate",
   "Quantity I: 1/8 − 1/24 = 2/24 = 1/12, so 12 hours. Quantity II: 1/6 − 1/10 = 2/30 = 1/15, so 15 hours. "
   "12 < 15.",
   ["I: 1/12 ⇒ 12", "II: 1/15 ⇒ 15", "12 < 15"],
   why="'I > II' and 'I ≥ II' come from subtracting the times for Quantity I (24 − 8 = 16, more than 15).",
   secs=60)

bs = [16 - s for s in range(3, 6)]
assert bs == [13, 12, 11]
qc("Arithmetic-based comparison", I, "Speed (km/h) of a boat in still water, if its downstream speed is 16 km/h and "
   "the stream's speed is a whole number of km/h greater than 2 and less than 6", "12.5",
   [F(b) for b in bs], [F(25, 2)], "cbe", [">", "<="],
   "Still-water speed = downstream speed − stream speed; list every allowed stream speed",
   "The stream can be 3, 4 or 5 km/h, so the boat's speed is 13, 12 or 11 km/h. 13 > 12.5 but 12 and 11 are less, "
   "so the relationship cannot be established.",
   ["Stream ∈ {3, 4, 5}", "Boat ∈ {13, 12, 11}", "Both sides of 12.5 ⇒ cannot be established"],
   why="'I > II' takes only a 3 km/h stream; 'I ≤ II' and 'I < II' take only 4 or 5 km/h.", secs=60, by=BRUTE)

grp = ["M"] * 5 + ["W"] * 4
p1 = prob(list(itertools.combinations(range(9), 3)), lambda t: all(grp[i] == "M" for i in t))
p2 = prob(DICE2, lambda w: w[0] == w[1])
assert p1 == F(5, 42) and p2 == F(1, 6)
qc("Arithmetic-based comparison", A, "The probability that 3 people chosen at random from 5 men and 4 women are all "
   "men", "The probability that two fair dice show the same number", [p1], [p2], "<", [">", ">="],
   "C(5, 3)/C(9, 3) against 6/36",
   "Quantity I: C(5, 3)/C(9, 3) = 10/84 = 5/42 ≈ 0.119. Quantity II: 6/36 = 1/6 ≈ 0.167. Quantity I < Quantity II.",
   ["I: 10/84 ≈ 0.119", "II: 6/36 ≈ 0.167", "I < II"],
   why="'I > II' and 'I ≥ II' come from using only the first pick (5/9 ≈ 0.56) for Quantity I, or from taking "
       "the chance of a doublet as 1/36.", secs=75, by=BRUTE)

v1, v2 = F(4, 3) * 27, F(4 * 10)
assert (v1, v2) == (36, 40)
qc("Quantity I vs II", A, "Volume (cm³) of a sphere of radius 3 cm", "Volume (cm³) of a cylinder of radius 2 cm and "
   "height 10 cm", [v1 * F(22, 7)], [v2 * F(22, 7)], "<", [">", ">="],
   "Sphere = (4/3)πr³; cylinder = πr²h; π is common to both",
   "Quantity I: (4/3)π × 27 = 36π. Quantity II: π × 4 × 10 = 40π. 36π < 40π.",
   ["I: 36π", "II: 40π", "I < II"],
   short="Compare 36 and 40; π cancels.",
   why="'I > II' and 'I ≥ II' come from using r instead of r² for the cylinder (π × 2 × 10 = 20π).", secs=70)

circ = math.factorial(4)
assert circ == 24 and math.comb(7, 3) == 35
qc("Arithmetic-based comparison", A, "The number of ways 5 people can sit around a round table (seatings that are "
   "rotations of each other count as the same)", "The number of ways of choosing 3 people from 7",
   [F(circ)], [F(35)], "<", [">", ">="],
   "Circular arrangements of n = (n − 1)!; C(n, r) = n!/(r!(n − r)!)",
   "Quantity I: (5 − 1)! = 24. Quantity II: C(7, 3) = 35. 24 < 35.",
   ["I: 4! = 24", "II: 35", "24 < 35"],
   why="'I > II' and 'I ≥ II' come from using 5! = 120 for the round table, forgetting that rotations are the same.",
   secs=60, by=BRUTE)

d_ = [d for d in range(1, 1000) if F(d, 40) - F(d, 50) == 1]
assert d_ == [200]
qc("Arithmetic-based comparison", A, "Distance (km) between two towns, if a car at 50 km/h reaches 1 hour earlier "
   "than it does at 40 km/h", "Distance (km) covered by a train at 80 km/h in t hours, where t is a whole number "
   "greater than 1 and less than 4", [F(200)], [F(160), F(240)], "cbe", ["<", ">="],
   "d/40 − d/50 = 1; list the possible values of t",
   "Quantity I: d(1/40 − 1/50) = d/200 = 1, so d = 200 km. Quantity II: t = 2 or 3, giving 160 or 240 km. 200 lies "
   "between them, so the relationship cannot be established.",
   ["I: d/200 = 1 ⇒ 200", "II: 160 or 240", "Cannot be established"],
   why="'I < II' uses only t = 3; 'I ≥ II' and 'I > II' use only t = 2.", secs=80, by=BRUTE)

# ================================================================ Data Sufficiency (Quant) (B1 I3 A2)
T = "Data Sufficiency (Quant)"
cands = [(r, g, o) for r in range(0, 21) for g in range(0, 21) for o in range(0, 6) if r + g + o > 0]
verdict = ds2_verdict(cands, lambda c: c == (4, 6, 0), lambda c: c[2] == 0 and 2 * c[1] == 3 * c[0] and c[0] > 0,
                      lambda c: F(c[1], sum(c)))
assert verdict == "either"
Q(T, "Two-statement", B,
  f"{DS_PRE}\nQuestion: A ball is drawn at random from a bag. What is the probability that it is green?\n"
  "I. The bag contains 4 red balls and 6 green balls, and nothing else.\n"
  "II. The bag contains only red and green balls, and there are 1.5 times as many green balls as red balls.",
  DS2["either"], [DS2["I"], DS2["II"], DS2["both"]],
  "A probability needs only the proportion of green balls",
  "I: P = 6/10 = 3/5. II: green : red = 3 : 2, so green is 3/5 of the bag, whatever its size. Each statement alone "
  "gives 3/5.",
  ["I: 6/10 = 3/5", "II: green : red = 3 : 2 ⇒ 3/5", "Either alone"],
  why="'I alone' assumes II is useless because it gives no counts, but a ratio is enough; 'II alone' overlooks I; "
      "'both' is more than needed.", secs=45, by=BRUTE)

cands = [(a, b) for a in range(1, 121) for b in range(1, 121)]
verdict = ds2_verdict(cands, lambda c: F(1, c[0]) + F(1, c[1]) == F(1, 12), lambda c: c[1] == 2 * c[0],
                      lambda c: c[1])
assert verdict == "both"
Q(T, "Two-statement", I,
  f"{DS_PRE}\nQuestion: How long does pipe B alone take to fill the tank?\n"
  "I. Pipes A and B together fill the tank in 12 hours.\n"
  "II. Pipe A is twice as efficient as pipe B.",
  DS2["both"], [DS2["I"], DS2["II"], DS2["neither"]],
  "Two unknown times need a combined rate and a ratio",
  "I alone: 1/a + 1/b = 1/12 has many solutions. II alone: only a ratio. Together: rates 2 : 1 make 3 parts = 1/12, "
  "so B's rate = 1/36 and B alone takes 36 hours.",
  ["I: one equation, two unknowns", "II: ratio only", "Together: B = 36 h"],
  why="'I alone' and 'II alone' each leave a free unknown; 'neither' misses that the two together fix B's time.",
  secs=55, by=BRUTE)

cands = [(a, b, c) for a in range(1, 61) for b in range(1, 61) for c in range(1, 61)]
verdict = ds2_verdict(cands, lambda x: F(1, x[0]) + F(1, x[1]) == F(1, 10), lambda x: 4 * x[1] * 5 == 4 * x[2] * 4,
                      lambda x: x[0])
assert verdict == "neither"
Q(T, "Two-statement", I,
  f"{DS_PRE}\nQuestion: In how many days can A alone finish the job?\n"
  "I. A and B together finish the job in 10 days.\n"
  "II. B is 25% more efficient than C.",
  DS2["neither"], [DS2["both"], DS2["I"], DS2["II"]],
  "II relates B to C, who does not appear in I; nothing fixes B's rate",
  "I gives a + b = 1/10 with two unknowns. II relates B and C only. Together, B's rate is still unknown (B could take "
  "15 days and A 30, or B 20 days and A 20), so A's time is not fixed.",
  ["I: one equation in A and B", "II: B and C only", "B's rate never fixed ⇒ not sufficient"],
  why="'Both' assumes II pins down B's rate, but it only links B to the unknown C; 'I alone' and 'II alone' are "
      "weaker still.", secs=60, by=BRUTE)

cands = [(l_, b_, h_) for l_ in range(1, 25) for b_ in range(1, 25) for h_ in range(1, 25)]
conds = [lambda c: 3 * c[0] == 4 * c[1] and 2 * c[0] == 4 * c[2], lambda c: c[0] * c[1] * c[2] == 192,
         lambda c: c[0] == 8]
mp_ = suff_map(cands, conds, lambda c: 2 * (c[0] * c[1] + c[1] * c[2] + c[2] * c[0]))
assert mp_ == {(0,): False, (1,): False, (2,): False, (0, 1): True, (0, 2): True, (1, 2): False, (0, 1, 2): True}
Q(T, "Three-statement", I,
  f"{DS3_PRE}\nQuestion: What is the total surface area of the cuboid?\n"
  "I. Its length, breadth and height are in the ratio 4 : 3 : 2.\n"
  "II. Its volume is 192 cm³.\n"
  "III. Its length is 8 cm.",
  "Either I and II together or I and III together are sufficient",
  ["Only I and II together are sufficient", "Any two of the three statements together are sufficient",
   "All three statements together are necessary"],
  "Total surface area needs all three edges",
  "I + II: 24k³ = 192, so k = 2 and the edges are 8, 6, 4: area = 2(48 + 24 + 32) = 208 cm². I + III: 4k = 8, k = 2, "
  "the same cuboid. II + III: breadth × height = 24, but 6 × 4 and 12 × 2 give different areas (208 and 272 cm²), "
  "so II + III fail.",
  ["I + II: k = 2 ⇒ 208 cm²", "I + III: k = 2 ⇒ 208 cm²", "II + III: b × h = 24, not fixed"],
  why="'Only I and II' overlooks that III can replace II; 'any two' wrongly accepts II + III; 'all three' is more "
      "than needed.", secs=80, by=BRUTE)

cands = [(V, w, x) for V in range(10, 81, 10) for w in (F(1, 5), F(1, 4), F(1, 3), F(1, 2)) for x in range(2, 11, 2)]


def final_ratio(c):
    V, w, x = c
    water = V * w * (1 - F(x, V))
    return water / (V - water)


verdict = ds2_verdict(cands, lambda c: c[0] == 40 and c[1] == F(1, 4), lambda c: c[2] == 8, final_ratio)
assert verdict == "both" and final_ratio((40, F(1, 4), 8)) == F(1, 4)
Q(T, "Two-statement", A,
  f"{DS_PRE}\nQuestion: A vessel holds a mixture of milk and water. Some of the mixture is drawn off and replaced "
  "with pure milk. What is the ratio of milk to water after this?\n"
  "I. The vessel held 40 litres of the mixture, of which 25% was water.\n"
  "II. 8 litres of the mixture were drawn off and replaced with milk.",
  DS2["both"], [DS2["I"], DS2["II"], DS2["neither"]],
  "The final ratio depends on the starting quantity, its water share and the amount replaced",
  "I alone does not say how much was replaced; II alone does not give the vessel's size or make-up. Together: water "
  "= 10 L at first; drawing off 8 of 40 litres removes 1/5 of it, leaving 8 L water, and milk becomes 32 L. Ratio = "
  "32 : 8 = 4 : 1.",
  ["I: no amount replaced", "II: no starting data", "Together: water 8 L, milk 32 L ⇒ 4 : 1"],
  why="'I alone' and 'II alone' each miss a needed quantity; 'neither' overlooks that together they fix the ratio.",
  secs=85, by=BRUTE)

cands = [(M, W) for M in range(1, 301) for W in range(1, 301)]
conds = [lambda c: F(3, c[0]) + F(4, c[1]) == F(1, 10), lambda c: F(2, c[0]) + F(6, c[1]) == F(1, 10),
         lambda c: F(6, c[0]) + F(8, c[1]) == F(1, 5)]
mp_ = suff_map(cands, conds, lambda c: c[0])
assert mp_ == {(0,): False, (1,): False, (2,): False, (0, 1): True, (0, 2): False, (1, 2): True, (0, 1, 2): True}
assert (50, 100) in [c for c in cands if all(f(c) for f in conds)]
Q(T, "Three-statement", A,
  f"{DS3_PRE}\nQuestion: In how many days can one man alone finish the job?\n"
  "I. 3 men and 4 women together finish the job in 10 days.\n"
  "II. 2 men and 6 women together finish the job in 10 days.\n"
  "III. 6 men and 8 women together finish the job in 5 days.",
  "Either I and II together or II and III together are sufficient",
  ["Any two of the three statements together are sufficient", "Only I and II together are sufficient",
   "All three statements together are necessary"],
  "Each statement is one equation in a man's rate m and a woman's rate w; check whether a pair is independent",
  "I: 3m + 4w = 1/10. II: 2m + 6w = 1/10. III: 6m + 8w = 1/5, which is just I doubled. I + II: subtracting gives "
  "m = 2w, so 10w = 1/10, w = 1/100, m = 1/50 — a man takes 50 days. II + III: the same as II + I. I + III: one "
  "equation repeated, so not sufficient.",
  ["III = 2 × I (no new information)", "I + II ⇒ m = 1/50 ⇒ 50 days", "II + III works; I + III does not"],
  why="'Any two' wrongly accepts I + III, which are the same equation; 'only I and II' overlooks II + III; 'all "
      "three' is more than needed.", secs=110, by=BRUTE)

# ######################################################################## checks and output
OUT = {}
for bt in ("009", "010"):
    plan = PKG["batches"][bt]
    qs, sts = QS[bt], STIMS[bt]
    assert len(qs) == plan["count"], (bt, len(qs))
    have = Counter((q["topic"], q["difficulty"]) for q in qs)
    want = Counter({(t["topic"], d): n for t in plan["topics"] for d, n in t["quota"].items() if n})
    assert have == want, (bt, set(have.items()) ^ set(want.items()))
    assert Counter(q["difficulty"] for q in qs) == Counter(plan["by_difficulty"]), bt
    subs = {t["topic"]: set(t["subtopics"]) for t in plan["topics"]}
    bad = [(q["topic"], q["subtopic"]) for q in qs if q["subtopic"] not in subs[q["topic"]]]
    assert not bad, bad
    assert qs[0]["question_id"] == plan["question_ids"][0] and qs[-1]["question_id"] == plan["question_ids"][1]
    assert sts[0]["stimulus_id"] == plan["stimulus_id_start"]
    for s in sts:  # every DI set has 3 to 6 questions
        assert 3 <= _set_pos[s["stimulus_id"]] <= 6, s["stimulus_id"]
    keys = Counter(q["correct_answer"] for q in qs)
    assert max(keys.values()) - min(keys.values()) <= 1, keys
    ids = {q["question_id"] for q in qs}
    for q in qs:
        if q["question_id"] in INDEPENDENT:
            q["verification"]["verified_by"].append("ai:independent-check")
    OUT[bt] = {
        "schema_version": "1.0",
        "batch_id": plan["batch_id"],
        "created_at": TODAY,
        "notes": f"{plan['batch_id']}, Quantitative Aptitude, package 2 fragment: {len(qs)} original questions "
                 f"({plan['by_difficulty']['Basic']} Basic, {plan['by_difficulty']['Intermediate']} Intermediate, "
                 f"{plan['by_difficulty']['Advanced']} Advanced) on mixtures, work, pipes, speed, boats, trains, "
                 f"mensuration, probability, permutations, DI, quantity comparison and data sufficiency, with "
                 f"{len(sts)} shared DI stimuli on new data sets. Every answer was recomputed by "
                 "tools/packages/QUANT_pkg2.py before writing (probabilities, arrangements and data-sufficiency "
                 "verdicts by enumeration); quantity-comparison values are at least 2% apart. Questions tagged "
                 "ai:independent-check were also re-solved blind by a separate solver. Pending human review.",
        "stimuli": sts,
        "questions": qs,
    }
assert INDEPENDENT <= {q["question_id"] for bt in QS for q in QS[bt]}

if "--dump" in sys.argv:  # blind copies for solvers: no key, no solution
    ids = None
    if "--ids" in sys.argv:
        ids = set(sys.argv[sys.argv.index("--ids") + 1].split(","))
    allq = QS["009"] + QS["010"]
    alls = STIMS["009"] + STIMS["010"]
    blind = [{"question_id": q["question_id"], "stimulus_id": q.get("stimulus_id"), "question_text": q["question_text"],
              "options": q["options"]} for q in allq if ids is None or q["question_id"] in ids]
    used = {q["stimulus_id"] for q in blind if q["stimulus_id"]}
    Path(sys.argv[sys.argv.index("--dump") + 1]).write_text(
        json.dumps({"stimuli": [s for s in alls if s["stimulus_id"] in used], "questions": blind}, indent=1,
                   ensure_ascii=False), encoding="utf-8")
    print(f"blind dump written ({len(blind)} questions)")
    sys.exit(0)

for bt, doc in OUT.items():
    out = ROOT / PKG["batches"][bt]["output"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    keys = Counter(q["correct_answer"] for q in doc["questions"])
    print(f"wrote {out.relative_to(ROOT)} ({len(doc['questions'])} questions, {len(doc['stimuli'])} stimuli, "
          f"keys {dict(sorted(keys.items()))}, independent-check "
          f"{sum('ai:independent-check' in q['verification']['verified_by'] for q in doc['questions'])})")
