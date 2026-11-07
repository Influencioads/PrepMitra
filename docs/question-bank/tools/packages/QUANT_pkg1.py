"""QUANT package 1: Quantitative Aptitude topics Simplification, Approximation, Number Series, Wrong Number Series,
Quadratic Equations, Number System, Percentage, Ratio and Proportion, Problems on Ages, Average, Profit and Loss,
Discount, Simple Interest, Compound Interest and Partnership for BATCH_009 and BATCH_010.

Writes batches/parts/frag/BATCH_009_QUANT_pkg1.json (100 questions) and batches/parts/frag/BATCH_010_QUANT_pkg1.json
(98 questions), as laid down in batches/plans/packages/QUANT_pkg1.json.

Every answer is recomputed here before anything is written: arithmetic with exact fractions, series regenerated from
their rule and tested against the rival-rule library of tools/batch_008/quant.py (no library rule that fits the given
terms may land on a wrong option; for wrong-term series no rule may fit once a non-key option is removed), quadratic
roots substituted back into the equations with the relation guards of tools/batch_007/quant.py (a strict answer never
beside its weaker form, no wrong relation that also holds), approximation answers checked to be the nearest option by
a clear margin. Per-batch quotas, ID ranges, subtopics and balanced keys (seed 20261105 + 91) are asserted. If any
assertion fails, nothing is written.

All earlier stems of these topics (BATCH_000 to BATCH_007 and the BATCH_008 Quant builder) were read first; facts,
contexts and number templates here are new.

    python tools/packages/QUANT_pkg1.py          (run from docs/question-bank)
    python tools/packages/QUANT_pkg1.py --dump <file> [--ids a,b,...]   (blind copy: no key, no solution)
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
PKG = json.loads((ROOT / "batches" / "plans" / "packages" / "QUANT_pkg1.json").read_text(encoding="utf-8"))
RECOMPUTE = ["script:recompute", "ai:self-recheck"]
BRUTE = ["script:recompute", "script:brute-force-unique", "ai:self-recheck"]

# Questions re-answered blind by a separate fresh solver (stem and options only, dump made with --dump --ids) whose
# answer matched the key. Every fourth question of each fragment (BANK_QUANT_001603, _001607, ..., _001699 and
# BANK_QUANT_001802, _001806, ..., _001898: 50 questions) went to one fresh solver; all 50 answers matched the key.
# The solver noted that BANK_QUANT_001802 did not say how the student continued after 120 − 40; its stem was then
# tightened ("and then going strictly from left to right"), so it is left out of this set. No other question was
# changed after its blind check.
INDEPENDENT = ({f"BANK_QUANT_{n:06d}" for n in range(1603, 1703, 4)}
               | {f"BANK_QUANT_{n:06d}" for n in range(1806, 1900, 4)})

PENDING = {"009": [], "010": []}  # records before ordering, ID and key assignment

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
# ---------------------------------------------------------------- record builder
def Q(bt, topic, sub, diff, text, ans, wrong, concept, expl, steps, short=None, why=None, secs=None, by=None):
    """Stores one question for batch bt; IDs and balanced keys are assigned when the batch is finalised."""
    assert bt in PENDING and len(wrong) == 3, (bt, wrong)
    assert diff in (B, I, A)
    assert why, f"why_others_wrong missing: {text[:60]}"
    assert len({normalize(o) for o in [ans, *wrong]}) == 4, f"options not distinct: {[ans, *wrong]}"
    if secs is None:
        secs = {B: 40, I: 60, A: 100}[diff]
    PENDING[bt].append(dict(topic=topic, sub=sub, diff=diff, text=text, ans=ans, wrong=list(wrong), concept=concept,
                            expl=expl, steps=steps, short=short, why=why, secs=secs, by=list(by or RECOMPUTE)))


def nearest(exact, options, answer):
    """Approximation check: the answer is the option nearest the exact value, by a clear margin."""
    dist = sorted((abs(exact - o), o) for o in options)
    assert dist[0][1] == answer, (exact, dist)
    assert dist[1][0] >= 3 * dist[0][0] and dist[1][0] >= 1, (exact, dist)




APPROX = "What approximate value should come in place of the question mark (?)?\n"
QMARK = "What will come in place of the question mark (?)?\n"

# ---------------------------------------------------------------- series: rival-rule library
PRIMES = [p for p in range(2, 600) if all(p % d for d in range(2, int(p ** 0.5) + 1))]


def _solve(rows, rhs, need_check=True):
    """Exact Gaussian elimination. Returns the unique solution when the system is consistent and of full column
    rank (and, if need_check, has at least one more equation than unknowns), else None."""
    if not rows:
        return None
    m = len(rows[0])
    if len(rows) < m + (1 if need_check else 0):
        return None
    M = [[F(x) for x in r] + [F(b)] for r, b in zip(rows, rhs)]
    for c in range(m):
        p = next((r for r in range(c, len(M)) if M[r][c] != 0), None)
        if p is None:
            return None
        M[c], M[p] = M[p], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(len(M)):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    if any(M[r][m] != 0 for r in range(m, len(M))):
        return None
    return [M[i][m] for i in range(m)]


def _digits(t, prod=False):
    if t.denominator != 1:
        return F(0)
    ds = [int(c) for c in str(abs(t.numerator))]
    return F(math.prod(ds)) if prod else F(sum(ds))


def _closed(fs, s):
    def fam(seq):
        return [({i}, [f(i + s) for f in fs] + [1], t) for i, t in enumerate(seq)], len(fs) + 1
    return fam


def _rec1(mult, add):
    """t[i+1] = multiplier part + addition part; both may hold free parameters (columns)."""
    def fam(seq):
        eqs = []
        for i in range(len(seq) - 1):
            t, t1 = seq[i], seq[i + 1]
            mc, mr = mult(t, i)
            ac = add(i)
            eqs.append(({i, i + 1}, mc + ac, t1 - mr))
        return eqs, len(eqs[0][1])
    return fam


def _rec_k(cols, order):
    """Higher-order recurrences: cols(window) -> (columns, value subtracted from the new term)."""
    def fam(seq):
        eqs = []
        for i in range(len(seq) - order):
            w = seq[i:i + order + 1]
            c, r = cols(w)
            eqs.append((set(range(i, i + order + 1)), c, w[-1] - r))
        return eqs, len(eqs[0][1]) if eqs else 99
    return fam


_BASIS = {"n": lambda n: F(n), "n²": lambda n: F(n * n), "n³": lambda n: F(n ** 3), "2ⁿ": lambda n: F(2 ** n),
          "3ⁿ": lambda n: F(3 ** n), "n!": lambda n: F(math.factorial(n)), "pₙ": lambda n: F(PRIMES[n - 1]),
          "pₙ²": lambda n: F(PRIMES[n - 1] ** 2), "pₙ³": lambda n: F(PRIMES[n - 1] ** 3)}
FAMILIES = []  # (name, fam)
FAMILIES.append(("constant difference", _closed([_BASIS["n"]], 1)))
FAMILIES.append(("constant second difference", _closed([_BASIS["n"], _BASIS["n²"]], 1)))
FAMILIES.append(("constant third difference", _closed([_BASIS["n"], _BASIS["n²"], _BASIS["n³"]], 1)))
for s_ in range(1, 11):
    for k_ in ("n²", "n³", "2ⁿ", "3ⁿ", "n!", "pₙ", "pₙ²", "pₙ³"):
        FAMILIES.append((f"a·{k_} + c (n from {s_})", _closed([_BASIS[k_]], s_)))
    for k1, k2 in (("n²", "2ⁿ"), ("n³", "2ⁿ"), ("n", "2ⁿ"), ("n", "3ⁿ"), ("n²", "3ⁿ"), ("n", "n!"), ("n³", "n"),
                   ("n³", "n²"), ("pₙ", "n"), ("pₙ²", "pₙ"), ("pₙ²", "n"), ("pₙ³", "pₙ"), ("2ⁿ", "3ⁿ")):
        FAMILIES.append((f"a·{k1} + b·{k2} + c (n from {s_})", _closed([_BASIS[k1], _BASIS[k2]], s_)))

_MULTS = [("× k", lambda t, i: ([t], 0)), ("+ (difference)", lambda t, i: ([], t)),
          ("× (a + b·n)", lambda t, i: ([t, i * t], 0)),
          ("× k alternating", lambda t, i: ([t if i % 2 == 0 else F(0), t if i % 2 else F(0)], 0))]
for m_ in range(0, 11):
    _MULTS.append((f"× ({m_}, {m_ + 1}, …)", lambda t, i, m_=m_: ([], (i + m_) * t)))
for m_ in range(1, 8):
    _MULTS.append((f"× ({m_}/2, {m_ + 1}/2, …)", lambda t, i, m_=m_: ([], F(i + m_, 2) * t)))
_ADDS = [("", lambda i: []), ("+ c", lambda i: [F(1)]), ("+ (c + d·n)", lambda i: [F(i), F(1)]),
         ("+ (quadratic in n)", lambda i: [F(i * i), F(i), F(1)]), ("± c alternating", lambda i: [F((-1) ** i)]),
         ("+ c ± d alternating", lambda i: [F((-1) ** i), F(1)]), ("+ c·2ⁿ", lambda i: [F(2 ** i)]),
         ("+ c·2ⁿ + d", lambda i: [F(2 ** i), F(1)]), ("+ c·3ⁿ", lambda i: [F(3 ** i)])]
for s_ in range(0, 9):
    _ADDS += [(f"+ c·(n+{s_})", lambda i, s_=s_: [F(i + s_)]), (f"+ c·(n+{s_})²", lambda i, s_=s_: [F((i + s_) ** 2)]),
              (f"+ c·(n+{s_})³", lambda i, s_=s_: [F((i + s_) ** 3)]),
              (f"± c·(n+{s_}) alternating", lambda i, s_=s_: [F((-1) ** i * (i + s_))]),
              (f"± c·(n+{s_})² alternating", lambda i, s_=s_: [F((-1) ** i * (i + s_) ** 2)])]
for s_ in range(1, 7):
    _ADDS.append((f"+ c·prime(n+{s_})", lambda i, s_=s_: [F(PRIMES[i + s_ - 1])]))
for (mn, mf), (an, af) in itertools.product(_MULTS, _ADDS):
    if len(mf(F(1), 1)[0]) + len(af(1)) <= 4:
        FAMILIES.append((f"next = term {mn} {an}".strip(), _rec1(mf, af)))
FAMILIES += [
    ("next = a·(previous) + b·(one before) + c", _rec_k(lambda w: ([w[1], w[0], F(1)], 0), 2)),
    ("next = a·(previous) + b·(one before)", _rec_k(lambda w: ([w[1], w[0]], 0), 2)),
    ("next = sum of previous two + c", _rec_k(lambda w: ([F(1)], w[0] + w[1]), 2)),
    ("next = k·(product of previous two)", _rec_k(lambda w: ([w[0] * w[1]], 0), 2)),
    ("next = product of previous two + c", _rec_k(lambda w: ([F(1)], w[0] * w[1]), 2)),
    ("next = sum of previous three + c", _rec_k(lambda w: ([F(1)], w[0] + w[1] + w[2]), 3)),
    ("next = a·t₋₁ + b·t₋₂ + c·t₋₃", _rec_k(lambda w: ([w[2], w[1], w[0]], 0), 3)),
    ("next = term + k·(digit sum)", _rec1(lambda t, i: ([_digits(t)], t), lambda i: [])),
    ("next = term + k·(digit sum) + c", _rec1(lambda t, i: ([_digits(t)], t), lambda i: [F(1)])),
    ("next = term + k·(digit product)", _rec1(lambda t, i: ([_digits(t, True)], t), lambda i: [])),
    ("alternating operations: × a + b, then × c + d", _rec1(
        lambda t, i: ([t if i % 2 == 0 else F(0), t if i % 2 else F(0)], 0),
        lambda i: [F(1) if i % 2 == 0 else F(0), F(1) if i % 2 else F(0)])),
]
_SUBFAMS = [f for f in FAMILIES if f[0] in ("constant difference", "constant second difference",
                                            "next = term × k", "next = term × k + c")]
_SUBFAMS += [f for f in FAMILIES if f[0].startswith("a·n² + c") or f[0].startswith("a·n³ + c")]


def _fit(fam, seq, j=None):
    """(True, value at j) if the family fits seq with at least one check equation; seq[j] is unknown if j given."""
    if j is None:
        eqs, m = fam(seq)
        p = _solve([e[1] for e in eqs], [e[2] for e in eqs])
        return p is not None, None
    probe = {}
    for x in (F(0), F(1)):
        s2 = list(seq)
        s2[j] = x
        probe[x] = fam(s2)[0]
    eqs0, m = fam([F(0) if k == j else t for k, t in enumerate(seq)])
    free = [e for e in eqs0 if j not in e[0]]
    inv = [k for k, e in enumerate(eqs0) if j in e[0]]
    if len(free) < m or len(free) + len(inv) - 1 < m + 1:
        return False, None
    p = _solve([e[1] for e in free], [e[2] for e in free], need_check=False)
    if p is None:
        return False, None

    def resid(e):
        return sum(a * b for a, b in zip(e[1], p)) - e[2]
    for k in inv:
        r0, r1 = resid(probe[F(0)][k]), resid(probe[F(1)][k])
        if r0 == r1:
            continue
        x = -r0 / (r1 - r0)
        s2 = list(seq)
        s2[j] = x
        if all(resid(e) == 0 for e in fam(s2)[0]):
            return True, x
    return False, None


def _fit_alt(seq, j=None):
    """Alternating two-series: the odd-place and even-place terms each follow a simple rule (each checked)."""
    xs = None
    for par in (0, 1):
        sub = seq[par::2]
        jj = None if j is None or j % 2 != par else j // 2
        ok = False
        for _, fam in _SUBFAMS:
            good, x = _fit(fam, sub, jj)
            if good:
                ok = True
                if jj is not None:
                    xs = x
                break
        if not ok:
            return False, None
    return True, xs


def rival_rules_missing(seq, options, answer):
    """seq has None at the '?'. No library rule that fits every given term may produce a different option."""
    j = seq.index(None)
    hits = {}
    for v in options:
        s = [F(v) if t is None else F(t) for t in seq]
        for name, fam in FAMILIES:
            if _fit(fam, s)[0]:
                hits.setdefault(F(v), name)
                break
        else:
            if _fit_alt(s)[0]:
                hits.setdefault(F(v), "alternating two-series")
    rivals = {v: n for v, n in hits.items() if v != F(answer)}
    assert not rivals, (seq, rivals)
    SERIES_LOG.append((seq, answer, hits.get(F(answer), "(rule outside the library)")))


def rival_rules_wrong(shown, wrong_pos, correct, option_positions):
    """No library rule may fit the series with any non-key option position left out."""
    s = [F(t) for t in shown]
    found = None
    for j in option_positions:
        for name, fam in FAMILIES + [("alternating two-series", None)]:
            ok, x = _fit_alt(s, j) if fam is None else _fit(fam, s, j)
            if j == wrong_pos:
                if ok and x == F(correct) and found is None:
                    found = name
            else:
                assert not ok, (shown, j, name, x)
    SERIES_LOG.append((shown, correct, found or "(rule outside the library)"))


SERIES_LOG = []


# ================================================================ Simplification (009: B4 I2 A3; 010: B3 I6 A3)
T = "Simplification"
v = (23 * 9 + 8 + 17 ** 2) / F(1296, 36)
assert v == 14 and [F(1296, 36) * k - 289 for k in (13, 15, 16)] == [179, 251, 287]
Q("009", T, "BODMAS", B, QMARK + "1,296 ÷ 36 × ? − 17² = 23 × 9 + 8",
  "14", ["13", "15", "16"],
  "Work ÷ and × from left to right before − ; then undo the steps to find ?",
  "1,296 ÷ 36 = 36, so the left side is 36 × ? − 289. The right side is 207 + 8 = 215. So 36 × ? = 215 + 289 = 504 "
  "and ? = 14.",
  ["1,296 ÷ 36 = 36", "Right side = 207 + 8 = 215", "36 × ? = 215 + 289 = 504", "? = 504 ÷ 36 = 14"],
  why="With 13, 15 or 16 the left side becomes 179, 251 or 287, not 215.", secs=45)

v = (F("3.6") * F("0.25") + F("0.45")) / F("0.027")
assert v == 50 and r2(F("0.9") + F("0.45") / F("0.027")) == F("17.57")
Q("009", T, "Fractions and decimals", B, QMARK + "(3.6 × 0.25 + 0.45) ÷ 0.027 = ?",
  "50", ["5", "500", "17.57"],
  "Finish the bracket first; then remove the decimals by scaling numerator and denominator alike",
  "3.6 × 0.25 = 0.9 and 0.9 + 0.45 = 1.35. Then 1.35 ÷ 0.027 = 1,350 ÷ 27 = 50.",
  ["3.6 × 0.25 = 0.9", "0.9 + 0.45 = 1.35", "1.35 ÷ 0.027 = 1,350 ÷ 27 = 50"],
  why="5 and 500 misplace the decimal point when dividing by 0.027; 17.57 ignores the bracket and divides only 0.45 by "
      "0.027 (0.9 + 16.67).", secs=40)

sq = next(n * n for n in range(1, 1000) if all(n * n % d == 0 for d in (6, 10, 14)))
assert sq == 44100 and 1764 % 10 and 900 % 14 and math.isqrt(210) ** 2 != 210
Q("009", T, "Square and cube roots", B, "What is the smallest perfect square that is exactly divisible by each of 6, "
  "10 and 14?",
  "44,100", ["210", "1,764", "900"],
  "Find the LCM, then make every prime power in it even",
  "LCM(6, 10, 14) = 2 × 3 × 5 × 7 = 210. Each prime appears once, so multiply by 210 again: 210² = 44,100 is the "
  "smallest perfect square divisible by all three.",
  ["LCM = 2 × 3 × 5 × 7 = 210", "Every prime power must be even", "210 × 210 = 44,100"],
  why="210 is the LCM but not a perfect square; 1,764 = 42² is not divisible by 10; 900 = 30² is not divisible by "
      "14.", secs=45)

x_ = next(x for x in range(10) if 7 ** (x - 2) == 343)
assert x_ == 5 and (x_ + 1) ** 2 == 36
Q("009", T, "Surds and indices", B, "If 7^(x − 2) = 343, what is the value of (x + 1)²?",
  "36", ["25", "16", "49"],
  "Write 343 as a power of 7 and compare the indices",
  "343 = 7³, so x − 2 = 3 and x = 5. Then (x + 1)² = 6² = 36.",
  ["343 = 7³", "x − 2 = 3 ⇒ x = 5", "(5 + 1)² = 36"],
  why="25 is x² rather than (x + 1)²; 16 takes x = 3 (the index of 343, forgetting the − 2); 49 uses x + 2.",
  secs=35)

for a_, b_, c_ in [(2, 5, 7), (3, -1, 4), (6, 2, -3)]:
    assert (a_ - b_) * (a_ + b_) + (b_ - c_) * (b_ + c_) + (c_ - a_) * (c_ + a_) == 0
Q("009", T, "Surds and indices", I,
  "Simplify: (xᵃ ÷ xᵇ)^(a + b) × (xᵇ ÷ xᶜ)^(b + c) × (xᶜ ÷ xᵃ)^(c + a), where x > 0.",
  "1", ["0", "x^(a + b + c)", "x^(2a + 2b + 2c)"],
  "(xᵐ)ⁿ = x^(mn), and the indices of a product add",
  "The first factor is x^((a − b)(a + b)) = x^(a² − b²). Likewise the others are x^(b² − c²) and x^(c² − a²). The "
  "indices add to a² − b² + b² − c² + c² − a² = 0, so the product is x⁰ = 1.",
  ["(xᵃ ÷ xᵇ)^(a + b) = x^(a² − b²)", "Others: x^(b² − c²), x^(c² − a²)", "Sum of indices = 0", "x⁰ = 1"],
  why="0 confuses x⁰ with 0; x^(a + b + c) and x^(2a + 2b + 2c) add the outer indices instead of multiplying "
      "(a − b) by (a + b).", secs=60)

p_, q_ = 1 + F(27, 99), F(36, 99)
assert p_ == F(14, 11) and q_ == F(4, 11) and p_ / q_ == F(7, 2)
assert F(127, 99) / q_ == F(127, 36) and (1 + F(27, 90)) / F(36, 90) == F(13, 4)
Q("009", T, "Fractions and decimals", I,
  "What is the value of 1.272727… ÷ 0.363636…, where the digits 27 and 36 recur without end?",
  "7/2", ["127/36", "13/4", "7/4"],
  "A two-digit recurring block ab equals ab/99",
  "1.2727… = 1 + 27/99 = 14/11 and 0.3636… = 36/99 = 4/11. So the quotient is 14/11 ÷ 4/11 = 14/4 = 7/2.",
  ["1.2727… = 1 + 27/99 = 14/11", "0.3636… = 36/99 = 4/11", "14/11 ÷ 4/11 = 7/2"],
  why="127/36 writes 1.2727… as 127/99; 13/4 uses 90 instead of 99 as the denominator; 7/4 halves the correct value, "
      "as if the divisor were 0.7272….", secs=60)

x3 = 2 ** (1 / 3) + 4 ** (1 / 3)
assert abs(x3 ** 3 - 6 * x3 - 6) < 1e-9
Q("009", T, "Surds and indices", A, "If x = ∛2 + ∛4, what is the value of x³ − 6x?",
  "6", ["0", "2", "12"],
  "(a + b)³ = a³ + b³ + 3ab(a + b)",
  "Let a = ∛2 and b = ∛4. Then a³ = 2, b³ = 4 and ab = ∛8 = 2. So x³ = 2 + 4 + 3 × 2 × x = 6 + 6x, and x³ − 6x = 6.",
  ["a³ + b³ = 2 + 4 = 6", "ab = ∛8 = 2", "x³ = 6 + 3 × 2 × x = 6 + 6x", "x³ − 6x = 6"],
  why="0 drops a³ + b³; 2 keeps only a³; 12 counts a³ + b³ twice.", secs=80)

e_ = F(0)
for _ in range(4):
    e_ = (1 + e_) / 2
assert e_ == F(15, 16)
Q("009", T, "Surds and indices", A, "Express √(2√(2√(2√2))) as a power of 2.",
  "2^(15/16)", ["2^(7/8)", "2^(31/32)", "2"],
  "Work from the innermost root outwards: √(2 × 2ᵏ) = 2^((1 + k)/2)",
  "√2 = 2^(1/2). Then √(2 × 2^(1/2)) = 2^(3/4), √(2 × 2^(3/4)) = 2^(7/8) and √(2 × 2^(7/8)) = 2^(15/16).",
  ["Innermost: 2^(1/2)", "Next: 2^(3/4)", "Next: 2^(7/8)", "Outermost: 2^(15/16)"],
  why="2^(7/8) stops one root early; 2^(31/32) takes one root too many; 2 is the limit of the endless pattern, not "
      "this four-root value.", secs=75)

sols = [x for x in range(5, 200) if math.isqrt(x + 16) ** 2 == x + 16 and math.isqrt(x - 5) ** 2 == x - 5
        and math.isqrt(x + 16) + math.isqrt(x - 5) == 7]
assert sols == [9] and abs(math.sqrt(36) + math.sqrt(15) - 7) > 0.1 and abs(math.sqrt(27) + math.sqrt(6) - 7) > 0.1
Q("009", T, "Square and cube roots", A, "If √(x + 16) + √(x − 5) = 7, what is the value of x?",
  "9", ["20", "4", "11"],
  "Let a = √(x + 16), b = √(x − 5): a² − b² = 21 and a + b = 7, so a − b = 3",
  "a² − b² = (x + 16) − (x − 5) = 21. Since a + b = 7, a − b = 21 ÷ 7 = 3. So a = 5, giving x + 16 = 25 and x = 9. "
  "Check: √25 + √4 = 5 + 2 = 7.",
  ["a² − b² = 21", "a − b = 21 ÷ 7 = 3", "a = (7 + 3) ÷ 2 = 5", "x = 25 − 16 = 9"],
  why="20 gives √36 + √15 ≈ 9.87; 4 makes x − 5 negative; 11 gives √27 + √6 ≈ 7.65.", secs=80)

right, wrong_ = 120 - F(40, 5) * 2 + 6, F(120 - 40, 5) * 2 + 6
assert (right, wrong_) == (110, 38) and right - wrong_ == 72 and (120 - F(40, 10) + 6) - 38 == 84
Q("010", T, "BODMAS", B, "A student simplified 120 − 40 ÷ 5 × 2 + 6 by first working out 120 − 40 and then going "
  "strictly from left to right. By how much was his answer less than the correct value?",
  "72", ["84", "110", "38"],
  "Division and multiplication come before subtraction, working left to right",
  "Correct: 40 ÷ 5 × 2 = 16, so 120 − 16 + 6 = 110. Student: (120 − 40) ÷ 5 × 2 + 6 = 16 × 2 + 6 = 38. The "
  "difference is 110 − 38 = 72.",
  ["Correct: 120 − 16 + 6 = 110", "Student: 80 ÷ 5 × 2 + 6 = 38", "110 − 38 = 72"],
  why="84 takes the correct value as 120 − 40 ÷ 10 + 6 = 122; 110 and 38 are the two values, not their difference.",
  secs=40)

s_ = F(7, 3) + F(23, 6)
assert s_ == F(37, 6) and 7 - s_ == F(5, 6) and 7 - (5 + F(5, 6)) == F(7, 6) and 7 - (5 + F(1, 6)) == F(11, 6)
Q("010", T, "Fractions and decimals", B, "What must be added to 2⅓ + 3⅚ to make the sum 7?",
  "⅚", ["⅙", "1⅙", "1⅚"],
  "Add the whole numbers and the fractions separately, then subtract from 7",
  "2⅓ + 3⅚ = 5 + (2/6 + 5/6) = 5 + 7/6 = 6⅙. So 7 − 6⅙ = ⅚ must be added.",
  ["⅓ + ⅚ = 2/6 + 5/6 = 7/6 = 1⅙", "Sum = 5 + 1⅙ = 6⅙", "7 − 6⅙ = ⅚"],
  why="⅙ is the fractional part of the sum, not the shortfall; 1⅙ takes the sum as 5⅚, forgetting to carry 7/6 "
      "into the whole number; 1⅚ takes the sum as 5⅙.", secs=40)

v = F("0.09") * F("0.16") * F("2.25")
assert v == F("0.0324") and F("0.18") ** 2 == v
Q("010", T, "Square and cube roots", B, "What is the value of √(0.09 × 0.16 × 2.25)?",
  "0.18", ["1.8", "0.018", "0.0324"],
  "√(abc) = √a × √b × √c",
  "√0.09 = 0.3, √0.16 = 0.4 and √2.25 = 1.5. So the value is 0.3 × 0.4 × 1.5 = 0.18.",
  ["√0.09 = 0.3", "√0.16 = 0.4", "√2.25 = 1.5", "0.3 × 0.4 × 1.5 = 0.18"],
  why="1.8 and 0.018 misplace the decimal point; 0.0324 is the product before taking the square root.", secs=40)

sol = [(x, y) for x in range(0, 10) for y in range(0, 10) if 2 * x == 3 * y and x + y == 5]
assert sol == [(3, 2)] and 9 ** 3 == 27 ** 2
Q("010", T, "Surds and indices", I, "If 9ˣ = 27ʸ and x + y = 5, what is the value of x?",
  "3", ["2", "2.5", "4"],
  "Write both sides as powers of 3 and compare the indices",
  "9ˣ = 3^(2x) and 27ʸ = 3^(3y), so 2x = 3y. With x + y = 5: x = 3, y = 2. Check: 9³ = 729 = 27².",
  ["9ˣ = 3^(2x), 27ʸ = 3^(3y)", "2x = 3y", "x + y = 5 ⇒ x = 3, y = 2"],
  why="2 is the value of y (it comes from 3x = 2y); 2.5 assumes x = y; 4 gives y = 1, but 9⁴ ≠ 27.", secs=55)

r_ = 2 - 3 ** 0.5
assert abs(r_ ** 2 - (7 - 4 * 3 ** 0.5)) < 1e-12 and abs(r_ + 1 / r_ - 4) < 1e-12
Q("010", T, "Surds and indices", I, "If x = 7 − 4√3, what is the value of √x + 1/√x?",
  "4", ["2√3", "14", "√14"],
  "7 − 4√3 = (2 − √3)², and 1/(2 − √3) = 2 + √3",
  "(2 − √3)² = 4 − 4√3 + 3 = 7 − 4√3, so √x = 2 − √3 and 1/√x = 2 + √3. Their sum is 4.",
  ["x = (2 − √3)²", "√x = 2 − √3, 1/√x = 2 + √3", "Sum = 4"],
  short="(√x + 1/√x)² = x + 1/x + 2 = 14 + 2 = 16, so the value is 4.",
  why="2√3 is 1/√x − √x; 14 is x + 1/x; √14 forgets the + 2 in (√x + 1/√x)² = x + 1/x + 2.", secs=60)

num = F("0.1") ** 2 + F("0.01") ** 2 + F("0.009") ** 2
den = F("0.01") ** 2 + F("0.001") ** 2 + F("0.0009") ** 2
assert num / den == 100
Q("010", T, "Fractions and decimals", I,
  QMARK + "[(0.1)² + (0.01)² + (0.009)²] ÷ [(0.01)² + (0.001)² + (0.0009)²] = ?",
  "100", ["10", "1,000", "0.01"],
  "Each term of the numerator is 10 times the matching term of the denominator",
  "0.1 = 10 × 0.01, 0.01 = 10 × 0.001 and 0.009 = 10 × 0.0009, so every square in the numerator is 10² = 100 times "
  "the matching square below. The quotient is 100.",
  ["Numerator terms = 10 × denominator terms", "Squares scale by 10² = 100", "Quotient = 100"],
  why="10 forgets that the terms are squared; 1,000 cubes the factor 10; 0.01 inverts the quotient.", secs=50)

x_ = (F("0.02") * 21) ** 2
assert x_ == F("0.1764")
Q("010", T, "Square and cube roots", I, "If √x ÷ √441 = 0.02, what is the value of x?",
  "0.1764", ["0.42", "1.764", "0.01764"],
  "√441 = 21; find √x first and then square it",
  "√x = 0.02 × 21 = 0.42, so x = 0.42² = 0.1764.",
  ["√441 = 21", "√x = 0.02 × 21 = 0.42", "x = 0.42² = 0.1764"],
  why="0.42 is √x, not x; 1.764 and 0.01764 misplace the decimal point when squaring 0.42.", secs=50)

g_ = sum(F(1, 2 ** k) for k in range(1, 11))
assert g_ == F(1023, 1024)
Q("010", T, "Fractions and decimals", I, QMARK + "1/2 + 1/4 + 1/8 + 1/16 + … + 1/1024 = ?",
  "1023/1024", ["1", "511/512", "1025/1024"],
  "Each partial sum falls short of 1 by the last term added",
  "1/2 = 1 − 1/2, 1/2 + 1/4 = 1 − 1/4, and so on. After the term 1/1024 the sum is 1 − 1/1024 = 1023/1024.",
  ["Sum of first n terms = 1 − 1/2ⁿ", "Last term 1/1024 = 1/2¹⁰", "Sum = 1 − 1/1024 = 1023/1024"],
  why="1 is the sum of the endless series, not of these ten terms; 511/512 stops at 1/512; 1025/1024 adds the last "
      "term instead of subtracting it.", secs=55)

assert 1 - F(127, 343) == F(216, 343) and F(6, 7) ** 3 == F(216, 343) and F(6, 7) ** 2 == F(36, 49)
Q("010", T, "Square and cube roots", I, QMARK + "∛(1 − 127/343) = ?",
  "6/7", ["216/343", "36/49", "2/7"],
  "Combine into a single fraction first; then take the cube root of the numerator and the denominator",
  "1 − 127/343 = (343 − 127)/343 = 216/343. ∛216 = 6 and ∛343 = 7, so the value is 6/7.",
  ["1 − 127/343 = 216/343", "∛216 = 6, ∛343 = 7", "Value = 6/7"],
  why="216/343 forgets the cube root; 36/49 is (6/7)²; 2/7 treats ∛(1 − a) as 1 − ∛a with ∛127 ≈ 5.", secs=55)

x5 = (5 ** 0.5 + 3 ** 0.5) / (5 ** 0.5 - 3 ** 0.5)
assert abs(x5 + 1 / x5 - 8) < 1e-9 and abs(x5 ** 2 + 1 + x5 ** -2 - 63) < 1e-9
Q("010", T, "Surds and indices", A, "If x = (√5 + √3)/(√5 − √3) and y = (√5 − √3)/(√5 + √3), what is the value of "
  "x² + xy + y²?",
  "63", ["62", "64", "65"],
  "Here xy = 1; find x + y and use x² + xy + y² = (x + y)² − xy",
  "x = (√5 + √3)²/2 = (8 + 2√15)/2 = 4 + √15 and y = 4 − √15. So x + y = 8 and xy = 1. Then x² + xy + y² = 64 − 1 = "
  "63.",
  ["x = 4 + √15, y = 4 − √15", "x + y = 8, xy = 1", "(x + y)² − xy = 64 − 1 = 63"],
  why="62 is x² + y² (leaving out xy); 64 is (x + y)²; 65 adds xy to (x + y)² instead of subtracting it.", secs=90)

ex = sum(F(k, 2 ** k) for k in range(1, 60))
assert abs(float(ex) - 2) < 1e-12 and abs(math.prod((2 ** k) ** (1 / 2 ** k) for k in range(1, 60)) - 4) < 1e-9
Q("010", T, "Surds and indices", A,
  "Find the value of the endless product 2^(1/2) × 4^(1/4) × 8^(1/8) × 16^(1/16) × …",
  "4", ["2", "2√2", "8"],
  "Write every factor as a power of 2: (2ⁿ)^(1/2ⁿ) = 2^(n/2ⁿ); then add the indices",
  "The product is 2 raised to S = 1/2 + 2/4 + 3/8 + 4/16 + …. Then S/2 = 1/4 + 2/8 + 3/16 + …, and S − S/2 = 1/2 + "
  "1/4 + 1/8 + … = 1. So S = 2 and the product is 2² = 4.",
  ["Factor n = 2^(n/2ⁿ)", "S = Σ n/2ⁿ", "S − S/2 = 1/2 + 1/4 + … = 1 ⇒ S = 2", "Product = 2² = 4"],
  why="2 takes the sum of the indices as 1 (the series 1/2 + 1/4 + …); 2√2 takes it as 3/2; 8 takes it as 3.",
  secs=100)

s_ = sum(k * (k + 1) for k in range(1, 21))
assert s_ == 3080 == 20 * 21 * 22 // 3 and sum(k * k for k in range(1, 21)) == 2870
assert sum(k * (k + 1) for k in range(1, 22)) == 3542 and sum(k * (k - 1) for k in range(1, 21)) == 2660
Q("010", T, "BODMAS", A, QMARK + "1 × 2 + 2 × 3 + 3 × 4 + … + 20 × 21 = ?",
  "3,080", ["2,870", "3,542", "2,660"],
  "1 × 2 + 2 × 3 + … + n(n + 1) = n(n + 1)(n + 2)/3",
  "Each term is k² + k, so the sum is (1² + … + 20²) + (1 + … + 20) = 2,870 + 210 = 3,080. The formula gives "
  "20 × 21 × 22 ÷ 3 = 3,080 directly.",
  ["Σk² (k = 1 to 20) = 2,870", "Σk = 210", "Total = 3,080"],
  short="n(n + 1)(n + 2)/3 with n = 20: 20 × 21 × 22 ÷ 3 = 3,080.",
  why="2,870 adds only the squares; 3,542 includes one term too many (up to 21 × 22); 2,660 uses k(k − 1) in place "
      "of k(k + 1).", secs=90)


# ================================================================ Approximation (009: B1 I4 A4; 010: B4 I2 A3)
T = "Approximation"
ex = 0.1198 * 2500.3 + 3 / 8 * 639.7
nearest(ex, [540, 480, 600, 620], 540)
Q("009", T, "Percentage approximation", B, APPROX + "11.98% of 2,500.3 + 3/8 of 639.7 ≈ ?",
  "540", ["480", "600", "620"],
  "Round each number to the nearest convenient value, then work out the percentage and the fraction",
  "12% of 2,500 = 300 and 3/8 of 640 = 240. So ? ≈ 300 + 240 = 540.",
  ["11.98% ≈ 12%, 2,500.3 ≈ 2,500 ⇒ 300", "3/8 of 640 = 240", "300 + 240 = 540"],
  why="480 takes 3/8 of 640 as 180; 600 takes 12% of 2,500 as 360; 620 takes 3/8 of 640 as 320.", secs=40)

ex = 1849.3 ** 0.5 * 3374.6 ** (1 / 3) - 19.98 ** 2
nearest(ex, [245, 202, 1045, 645], 245)
Q("009", T, "Root approximation", I, APPROX + "√1,849.3 × ∛3,374.6 − 19.98² ≈ ?",
  "245", ["202", "1,045", "645"],
  "Recognise the perfect square, cube and square near each number",
  "√1,849 = 43, ∛3,375 = 15 and 20² = 400. So ? ≈ 43 × 15 − 400 = 645 − 400 = 245.",
  ["√1,849.3 ≈ 43", "∛3,374.6 ≈ 15", "43 × 15 = 645", "645 − 400 = 245"],
  why="202 takes ∛3,375 as 14 (43 × 14 − 400); 1,045 adds 20² instead of subtracting it; 645 forgets 20².",
  secs=55)

rhs = 39.02 * 2.01 + 11.97
ex = rhs * 7.98 / 12.03
nearest(ex, [60, 135, 90, 7.5], 60)
Q("009", T, "Mixed approximation", I, APPROX + "(? × 12.03) ÷ 7.98 ≈ 39.02 × 2.01 + 11.97",
  "60", ["135", "90", "7.5"],
  "Simplify the right side first, then undo the × 12 and ÷ 8",
  "Right side ≈ 39 × 2 + 12 = 90. So ? × 12 ÷ 8 = 90, giving ? = 90 × 8 ÷ 12 = 60.",
  ["39 × 2 + 12 = 90", "? × 1.5 = 90", "? = 60"],
  why="135 inverts the operations (90 × 12 ÷ 8); 90 is the right side itself; 7.5 divides 90 by 12 and forgets to "
      "multiply by 8.", secs=55)

ex = (418.1 - 13.98 * 11.97) / 1249.8 * 100
nearest(ex, [20, 25, 33, 47], 20)
Q("009", T, "Percentage approximation", I, APPROX + "?% of 1,249.8 ≈ 418.1 − 13.98 × 11.97",
  "20", ["25", "33", "47"],
  "Find the right side first, then express it as a percentage of 1,250",
  "13.98 × 11.97 ≈ 14 × 12 = 168. Right side ≈ 418 − 168 = 250. ?% of 1,250 = 250 gives ? = 250 ÷ 1,250 × 100 = 20.",
  ["14 × 12 = 168", "418 − 168 = 250", "250 ÷ 1,250 = 20%"],
  why="25 divides 250 by 1,000 instead of 1,250; 33 ignores the product (418 ÷ 1,250); 47 adds 168 instead of "
      "subtracting it (586 ÷ 1,250).", secs=60)

ex = (2.998 ** 2 - 25.01 ** 0.5) ** 3 - 6.02
nearest(ex, [58, 64, 70, 10], 58)
Q("009", T, "Root approximation", I, APPROX + "∛(? + 6.02) ≈ 2.998² − √25.01",
  "58", ["64", "70", "10"],
  "Evaluate the right side, cube it, and then subtract 6",
  "Right side ≈ 9 − 5 = 4. So ? + 6 ≈ 4³ = 64, and ? ≈ 58.",
  ["2.998² ≈ 9, √25.01 ≈ 5", "∛(? + 6) ≈ 4", "? + 6 ≈ 64 ⇒ ? ≈ 58"],
  why="64 forgets to subtract 6; 70 adds 6 instead; 10 squares 4 instead of cubing it (16 − 6).", secs=55)

ex = (20.98 ** 2 / 6.99 + 13.02) * 7.02 + 0.2398 * 450.2
nearest(ex, [640, 532, 424, 700], 640)
Q("009", T, "Percentage approximation", A,
  APPROX + "(? − 23.98% of 450.2) ÷ 7.02 ≈ 20.98² ÷ 6.99 + 13.02",
  "640", ["532", "424", "700"],
  "Simplify the right side, multiply back by 7, then add back the percentage",
  "Right side ≈ 441 ÷ 7 + 13 = 63 + 13 = 76. So ? − 24% of 450 ≈ 76 × 7 = 532, and ? ≈ 532 + 108 = 640.",
  ["21² ÷ 7 = 63", "63 + 13 = 76", "76 × 7 = 532", "24% of 450 = 108 ⇒ ? ≈ 640"],
  why="532 forgets to add back 24% of 450; 424 subtracts 108 instead of adding it; 700 takes 24% of 450 as 168.",
  secs=80)

ex = ((33.03 * 11.98 - 1296.2 ** 0.5 - 15.98 ** 2) / 3.99) ** 2
nearest(ex, [676, 576, 784, 26], 676)
Q("009", T, "Root approximation", A, APPROX + "√? × 3.99 + 15.98² ≈ 33.03 × 11.98 − √1,296.2",
  "676", ["576", "784", "26"],
  "Collect the known terms on one side, find √? and then square it",
  "Right side ≈ 33 × 12 − 36 = 396 − 36 = 360. 16² = 256, so √? × 4 ≈ 360 − 256 = 104 and √? ≈ 26. Then ? ≈ 26² = "
  "676.",
  ["33 × 12 = 396, √1,296 = 36", "360 − 256 = 104", "√? ≈ 104 ÷ 4 = 26", "? ≈ 676"],
  why="576 and 784 are 24² and 28², from slips of 8 in the subtraction; 26 is √?, not ?.", secs=85)

ex = (0.2198 * 2700.4 + 0.1803 * 1999.7) / 4799.6 * 100
nearest(ex, [20, 16, 24, 12], 20)
Q("009", T, "Percentage approximation", A, APPROX + "?% of 4,799.6 − 18.03% of 1,999.7 ≈ 21.98% of 2,700.4",
  "20", ["16", "24", "12"],
  "Move the known percentage to the right side, then divide by 48 (1% of 4,800)",
  "18% of 2,000 = 360 and 22% of 2,700 = 594. So ?% of 4,800 ≈ 594 + 360 = 954, and ? ≈ 954 ÷ 48 ≈ 19.9 ≈ 20.",
  ["18% of 2,000 = 360", "22% of 2,700 = 594", "?% of 4,800 = 954", "? ≈ 954 ÷ 48 ≈ 20"],
  why="16 takes 18% of 2,000 as 180 (774 ÷ 48); 24 divides 954 by 40 instead of 48; 12 leaves out the 18% term "
      "(594 ÷ 48).", secs=80)

c_ = 29.98 * 12.02 + 8.97 * 10.03
ex = (-7.02 + (7.02 ** 2 + 4 * c_) ** 0.5) / 2
nearest(ex, [18, 15, 21, 25], 18)
Q("009", T, "Mixed approximation", A, APPROX + "?² + 7.02 × ? ≈ 29.98 × 12.02 + 8.97 × 10.03   (? is positive)",
  "18", ["15", "21", "25"],
  "Round the right side, then look for a positive number with ? × (? + 7) equal to it",
  "Right side ≈ 30 × 12 + 9 × 10 = 360 + 90 = 450. ?² + 7? = ?(? + 7) = 450. Since 18 × 25 = 450, ? ≈ 18.",
  ["30 × 12 + 9 × 10 = 450", "?(? + 7) = 450", "18 × 25 = 450 ⇒ ? ≈ 18"],
  short="?² + 7? − 450 = 0 factorises as (? − 18)(? + 25) = 0.",
  why="15 gives 15 × 22 = 330; 21 gives 21 × 28 = 588; 25 is the other factor of 450, not the value of ?.", secs=85)

ex = 0.4502 * 1599.6 / 8.97
nearest(ex, [80, 90, 72, 64], 80)
Q("010", T, "Percentage approximation", B, APPROX + "45.02% of 1,599.6 ÷ 8.97 ≈ ?",
  "80", ["90", "72", "64"],
  "Round the percentage, the number and the divisor, then work left to right",
  "45% of 1,600 = 720, and 720 ÷ 9 = 80.",
  ["45% of 1,600 = 720", "720 ÷ 9 = 80"],
  why="90 divides 720 by 8; 72 divides by 10; 64 uses 36% instead of 45% (576 ÷ 9).", secs=35)

ex = (8.98 * 15.97 * 24.96) ** 0.5
nearest(ex, [60, 50, 120, 45], 60)
Q("010", T, "Root approximation", B, APPROX + "√8.98 × √15.97 × √24.96 ≈ ?",
  "60", ["50", "120", "45"],
  "Each number under a root is close to a perfect square",
  "√9 × √16 × √25 = 3 × 4 × 5 = 60.",
  ["√8.98 ≈ 3", "√15.97 ≈ 4", "√24.96 ≈ 5", "3 × 4 × 5 = 60"],
  why="50 adds 9, 16 and 25 instead of multiplying their roots; 120 doubles the product; 45 takes √16 as 3.", secs=35)

ex = 0.498 * 1201.3 + 0.249 * 799.6
nearest(ex, [800, 750, 900, 700], 800)
Q("010", T, "Mixed approximation", B, APPROX + "0.498 × 1,201.3 + 0.249 × 799.6 ≈ ?",
  "800", ["750", "900", "700"],
  "0.498 ≈ ½ and 0.249 ≈ ¼",
  "½ of 1,200 = 600 and ¼ of 800 = 200. So ? ≈ 600 + 200 = 800.",
  ["0.498 × 1,200 ≈ 600", "0.249 × 800 ≈ 200", "600 + 200 = 800"],
  why="750 takes ¼ of 800 as 150; 900 takes ¼ of 1,200 instead of 800 for the second part (600 + 300); 700 takes "
      "0.249 as 1/8.", secs=40)

ex = (199.8 - 39.97) / 640.2 * 100
nearest(ex, [25, 31, 6.25, 35], 25)
Q("010", T, "Percentage approximation", B, APPROX + "?% of 640.2 + 39.97 ≈ 199.8",
  "25", ["31", "6.25", "35"],
  "Subtract first, then find what percentage the remainder is of 640",
  "?% of 640 ≈ 200 − 40 = 160, so ? ≈ 160 ÷ 640 × 100 = 25.",
  ["200 − 40 = 160", "160 ÷ 640 = 0.25", "? ≈ 25"],
  why="31 forgets to subtract 40 (200 ÷ 640 ≈ 31%); 6.25 finds 40 as a percentage of 640; 35 adds 40 instead of "
      "subtracting it.",
  secs=40)

ex = (75.03 / 4.97 + 3.02) ** 2
nearest(ex, [324, 289, 361, 225], 324)
Q("010", T, "Root approximation", I, APPROX + "(√? − 3.02) × 4.97 ≈ 75.03",
  "324", ["289", "361", "225"],
  "Undo the steps in reverse order: ÷ 5, + 3, then square",
  "√? − 3 ≈ 75 ÷ 5 = 15, so √? ≈ 18 and ? ≈ 18² = 324.",
  ["75 ÷ 5 = 15", "√? ≈ 15 + 3 = 18", "? ≈ 324"],
  why="289 = 17² and 361 = 19² come from adding 2 or 4 instead of 3; 225 = 15² forgets to add 3.", secs=50)

ex = 4.98 ** 4 / 24.97 + 3.02 ** 5 / 8.99
nearest(ex, [52, 46, 61, 152], 52)
Q("010", T, "Mixed approximation", I, APPROX + "4.98⁴ ÷ 24.97 + 3.02⁵ ÷ 8.99 ≈ ?",
  "52", ["46", "61", "152"],
  "Write the powers of 5 and 3 and cancel with the divisors (25 = 5², 9 = 3²)",
  "5⁴ ÷ 25 = 5² = 25 and 3⁵ ÷ 9 = 3³ = 27. So ? ≈ 25 + 27 = 52.",
  ["5⁴ ÷ 5² = 25", "3⁵ ÷ 3² = 27", "25 + 27 = 52"],
  why="46 takes 3⁵ ÷ 9 as 21; 61 takes 3⁵ as 324 (324 ÷ 9 = 36); 152 takes 5⁴ ÷ 25 as 5³ = 125.",
  secs=50)

ex = ((16.97 * 5.02) * 8.02 - 979.6 / 7) / 3600.2 * 100
nearest(ex, [15, 19, 23, 30], 15)
Q("010", T, "Percentage approximation", A, APPROX + "(?% of 3,600.2 + 1/7 of 979.6) ÷ 8.02 ≈ 16.97 × 5.02",
  "15", ["19", "23", "30"],
  "Multiply out the ÷ 8 first, take away the known part, then divide by 36 (1% of 3,600)",
  "Right side ≈ 17 × 5 = 85, so the bracket ≈ 85 × 8 = 680. 1/7 of 980 = 140, so ?% of 3,600 ≈ 680 − 140 = 540 and "
  "? ≈ 540 ÷ 36 = 15.",
  ["17 × 5 = 85", "85 × 8 = 680", "680 − 140 = 540", "540 ÷ 36 = 15"],
  why="19 forgets to take away the 140 (680 ÷ 36); 23 adds 140 instead of subtracting it; 30 divides 540 by 18 "
      "instead of 36.", secs=80)

ex = (1155.8 ** 0.5 + 4227.1 ** 0.5 - 8460.2 ** 0.5) ** 3
nearest(ex, [343, 512, 216, 49], 343)
Q("010", T, "Root approximation", A, APPROX + "∛? ≈ √1,155.8 + √4,227.1 − √8,460.2",
  "343", ["512", "216", "49"],
  "Find the nearest perfect squares: 34² = 1,156, 65² = 4,225, 92² = 8,464",
  "Right side ≈ 34 + 65 − 92 = 7. So ? ≈ 7³ = 343.",
  ["√1,156 = 34", "√4,225 = 65", "√8,464 = 92", "34 + 65 − 92 = 7 ⇒ ? ≈ 343"],
  why="512 = 8³ and 216 = 6³ come from misjudging one root by 1; 49 squares 7 instead of cubing it.", secs=75)

ex = (4.002 ** 4 / 3.998 - 8.998 - 11.99 * 3.002) * 14.01
nearest(ex, [266, 238, 294, 770], 266)
Q("010", T, "Mixed approximation", A, APPROX + "? ÷ 14.01 + 11.99 × 3.002 ≈ 4.002⁴ ÷ 3.998 − 8.998",
  "266", ["238", "294", "770"],
  "Simplify the right side, subtract the product, then multiply by 14",
  "4⁴ ÷ 4 = 4³ = 64, so the right side ≈ 64 − 9 = 55. Then ? ÷ 14 ≈ 55 − 12 × 3 = 19, and ? ≈ 19 × 14 = 266.",
  ["4⁴ ÷ 4 = 64", "64 − 9 = 55", "55 − 36 = 19", "19 × 14 = 266"],
  why="238 and 294 are 17 × 14 and 21 × 14, from slips of 2 in the subtraction; 770 forgets to subtract 12 × 3 "
      "(55 × 14).", secs=85)


# ================================================================ Number Series (009: B4 I10 A4; 010: B1 I4 A5)
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
    return ", ".join("?" if x is None else N(x) for x in seq)


def series_q(bt, sub, diff, full, qpos, wrong, concept, expl, steps, short=None, why=None, secs=None):
    """Missing-term series: the full regenerated series, the position shown as '?', three wrong options."""
    shown = [None if k == qpos else t for k, t in enumerate(full)]
    ans = full[qpos]
    rival_rules_missing(shown, [ans, *wrong], ans)
    head = SERIES_Q if qpos == len(full) - 1 else MISSING_Q
    Q(bt, T, sub, diff, head + series_text(shown), N(ans), [N(w) for w in wrong], concept, expl, steps, short, why,
      secs, by=BRUTE)


s = series_from(1, lambda t, k: t + k, 7)
assert s == [1, 2, 4, 7, 11, 16, 22]
series_q("009", "Pattern: differences", B, s, 6, [21, 32, 25],
         "The differences grow by 1 each time: 1, 2, 3, 4, 5, …",
         "1 + 1 = 2, 2 + 2 = 4, 4 + 3 = 7, 7 + 4 = 11, 11 + 5 = 16. The next difference is 6, so the term is "
         "16 + 6 = 22.",
         ["Differences: 1, 2, 3, 4, 5", "Next difference: 6", "16 + 6 = 22"],
         why="21 adds 5 again; 32 doubles 16; 25 adds 9, the sum of the last two differences.", secs=30)

s = series_from(2, lambda t, k: 4 * t - 2, 6)
assert s == [2, 6, 22, 86, 342, 1366] and 342 * 4 == 1368 and 342 * 3 == 1026
series_q("009", "Pattern: multiply-add", B, s, 5, [1368, 1370, 1026],
         "Each term is 4 times the previous term minus 2",
         "2 × 4 − 2 = 6, 6 × 4 − 2 = 22, 22 × 4 − 2 = 86, 86 × 4 − 2 = 342. Next: 342 × 4 − 2 = 1,366.",
         ["× 4 − 2 at every step", "342 × 4 = 1,368", "1,368 − 2 = 1,366"],
         why="1,368 multiplies by 4 but does not subtract 2; 1,370 adds 2 instead; 1,026 multiplies by 3.", secs=40)

s = [n * n for n in range(14, 8, -1)]
assert s == [196, 169, 144, 121, 100, 81]
series_q("009", "Pattern: squares and cubes", B, s, 5, [79, 64, 90],
         "The terms are the squares of 14, 13, 12, 11, 10, … in falling order",
         "196 = 14², 169 = 13², 144 = 12², 121 = 11², 100 = 10². The next term is 9² = 81.",
         ["14², 13², 12², 11², 10²", "Next: 9²", "= 81"],
         why="79 subtracts 21 again (the last difference); 64 = 8² skips 9²; 90 subtracts 10, the square root of "
             "100.", secs=30)

s = series_from(90, lambda t, k: t - 7 * k, 6)
assert s == [90, 83, 69, 48, 20, -15]
series_q("009", "Missing number series", B, s, 3, [55, 41, 62],
         "The amounts subtracted are multiples of 7: 7, 14, 21, 28, 35",
         "90 − 7 = 83, 83 − 14 = 69, 69 − 21 = 48, 48 − 28 = 20, 20 − 35 = −15. The missing term is 48.",
         ["Subtract 7, 14, 21, 28, 35", "69 − 21 = 48", "Check: 48 − 28 = 20 ✓"],
         why="55 subtracts 14 again; 41 subtracts 28 too early; 62 subtracts only 7. None of them gives 20 after the "
             "next step.", secs=40)

s = series_from(5, lambda t, k: t + k ** 3, 6)
assert s == [5, 6, 14, 41, 105, 230]
series_q("009", "Pattern: differences", I, s, 5, [169, 210, 186],
         "The differences are the cubes 1, 8, 27, 64, …",
         "5 + 1 = 6, 6 + 8 = 14, 14 + 27 = 41, 41 + 64 = 105. The next difference is 5³ = 125, so the term is "
         "105 + 125 = 230.",
         ["Differences: 1³, 2³, 3³, 4³", "Next: 5³ = 125", "105 + 125 = 230"],
         why="169 adds 64 again; 210 doubles 105; 186 adds 9² = 81, taking the differences as squares.", secs=50)

s = series_from(10, lambda t, k: 2 * t - k * k, 6)
assert s == [10, 19, 34, 59, 102, 179]
series_q("009", "Pattern: multiply-add", I, s, 5, [168, 204, 145],
         "Each term is twice the previous term minus 1², 2², 3², 4², …",
         "10 × 2 − 1 = 19, 19 × 2 − 4 = 34, 34 × 2 − 9 = 59, 59 × 2 − 16 = 102. Next: 102 × 2 − 25 = 179.",
         ["× 2 − 1, × 2 − 4, × 2 − 9, × 2 − 16", "Next: × 2 − 25", "204 − 25 = 179"],
         why="168 subtracts 6² = 36 and skips 5²; 204 doubles without subtracting; 145 adds 43, the last term minus "
             "the one before it.", secs=55)

s = [n ** 3 + n * n + n for n in range(1, 7)]
assert s == [3, 14, 39, 84, 155, 258] and 216 + 36 == 252 and 216 + 6 == 222 and 155 + 71 + 20 == 246
series_q("009", "Pattern: squares and cubes", I, s, 5, [252, 222, 246],
         "Each term is n³ + n² + n for n = 1, 2, 3, …",
         "1 + 1 + 1 = 3, 8 + 4 + 2 = 14, 27 + 9 + 3 = 39, 64 + 16 + 4 = 84, 125 + 25 + 5 = 155. For n = 6: 216 + 36 "
         "+ 6 = 258.",
         ["n³ + n² + n for n = 1 to 5", "n = 6: 216 + 36 + 6", "= 258"],
         short="Differences 11, 25, 45, 71 have second differences 14, 20, 26 (rising by 6); next 32, so the next "
               "difference is 103.",
         why="252 leaves out the + n; 222 leaves out n²; 246 keeps the second difference at 20 instead of raising "
             "it to 32.", secs=60)

s = [n * 2 ** n for n in range(1, 7)]
assert s == [2, 8, 24, 64, 160, 384]
series_q("009", "Missing number series", I, s, 3, [48, 72, 56],
         "Each term is n × 2ⁿ: 1 × 2, 2 × 4, 3 × 8, …",
         "2 = 1 × 2, 8 = 2 × 4, 24 = 3 × 8, ? = 4 × 16 = 64, 160 = 5 × 32, 384 = 6 × 64. The missing term is 64.",
         ["n × 2ⁿ for n = 1, 2, 3", "n = 4: 4 × 16 = 64", "Check: 5 × 32 = 160 ✓"],
         why="48 doubles 24 and 72 triples it, but neither leads on to 160 by one rule; 56 adds 32, which breaks the "
             "pattern of the later terms.", secs=55)

s = series_from(7, lambda t, k: t + 2 * 3 ** (k - 1), 7)
assert s == [7, 9, 15, 33, 87, 249, 735] and 249 * 3 == 747 and 249 + 324 == 573
series_q("009", "Pattern: differences", I, s, 6, [411, 747, 573],
         "The differences are multiplied by 3 each time: 2, 6, 18, 54, 162, …",
         "7 + 2 = 9, 9 + 6 = 15, 15 + 18 = 33, 33 + 54 = 87, 87 + 162 = 249. The next difference is 486, so the term "
         "is 249 + 486 = 735.",
         ["Differences: 2, 6, 18, 54, 162", "Next: 162 × 3 = 486", "249 + 486 = 735"],
         why="411 adds 162 again; 747 triples the term instead of the difference; 573 only doubles the last "
             "difference (+324).", secs=55)

s = series_from(1, lambda t, k: 4 * t + k, 6)
assert s == [1, 5, 22, 91, 368, 1477] and 368 * 4 == 1472 and 368 * 5 == 1840
series_q("009", "Pattern: multiply-add", I, s, 5, [1476, 1472, 1840],
         "Each term is 4 times the previous term plus 1, 2, 3, 4, …",
         "1 × 4 + 1 = 5, 5 × 4 + 2 = 22, 22 × 4 + 3 = 91, 91 × 4 + 4 = 368. Next: 368 × 4 + 5 = 1,477.",
         ["× 4 + 1, × 4 + 2, × 4 + 3, × 4 + 4", "Next: × 4 + 5", "1,472 + 5 = 1,477"],
         why="1,476 adds 4 again; 1,472 multiplies by 4 and adds nothing; 1,840 multiplies by 5.", secs=50)

s = series_from(4, lambda t, k: t + k * k + 2, 7)
assert s == [4, 7, 13, 24, 42, 69, 107]
series_q("009", "Pattern: differences", I, s, 6, [96, 105, 111],
         "The differences are 2 more than the squares: 1 + 2, 4 + 2, 9 + 2, 16 + 2, …",
         "Differences: 3, 6, 11, 18, 27 = 1² + 2, 2² + 2, 3² + 2, 4² + 2, 5² + 2. The next is 6² + 2 = 38, so the "
         "term is 69 + 38 = 107.",
         ["Differences: 3, 6, 11, 18, 27", "= n² + 2", "Next: 36 + 2 = 38", "69 + 38 = 107"],
         why="96 adds 27 again; 105 adds 36 and forgets the + 2; 111 adds the previous term (42 + 69).", secs=55)

s = [math.prod(PRIMES[:k]) for k in range(1, 7)]
assert s == [2, 6, 30, 210, 2310, 30030]
series_q("009", "Missing number series", I, s, 3, [180, 240, 270],
         "Each term is the previous term multiplied by the next prime: × 3, × 5, × 7, × 11, × 13",
         "2 × 3 = 6, 6 × 5 = 30, 30 × 7 = 210, 210 × 11 = 2,310, 2,310 × 13 = 30,030. The missing term is 210.",
         ["Multipliers: 3, 5, 7, 11, 13 (primes)", "30 × 7 = 210", "Check: 210 × 11 = 2,310 ✓"],
         why="180, 240 and 270 multiply 30 by 6, 8 and 9, which are not the next prime, and none of them gives 2,310 "
             "when multiplied by 11.", secs=55)

s = [3 ** n - n * n for n in range(1, 7)]
assert s == [2, 5, 18, 65, 218, 693] and 729 - 6 == 723 and 729 + 36 == 765 and 218 * 3 == 654
series_q("009", "Pattern: squares and cubes", I, s, 5, [723, 765, 654],
         "Each term is 3ⁿ − n² for n = 1, 2, 3, …",
         "3 − 1 = 2, 9 − 4 = 5, 27 − 9 = 18, 81 − 16 = 65, 243 − 25 = 218. For n = 6: 729 − 36 = 693.",
         ["3ⁿ − n² for n = 1 to 5", "n = 6: 3⁶ = 729, 6² = 36", "729 − 36 = 693"],
         why="723 subtracts 6 instead of 6²; 765 adds 36; 654 only triples 218, ignoring the squares.", secs=60)

s = series_from(100, lambda t, k: t - k * (k + 1) // 2, 7)
assert s == [100, 99, 96, 90, 80, 65, 44]
series_q("009", "Pattern: differences", I, s, 6, [50, 45, 37],
         "The amounts subtracted are the triangular numbers 1, 3, 6, 10, 15, 21, …",
         "100 − 1 = 99, 99 − 3 = 96, 96 − 6 = 90, 90 − 10 = 80, 80 − 15 = 65. The next amount is 21, so the term is "
         "65 − 21 = 44.",
         ["Subtract 1, 3, 6, 10, 15", "These rise by 2, 3, 4, 5", "Next: 15 + 6 = 21", "65 − 21 = 44"],
         why="50 subtracts 15 again; 45 subtracts 20 (taking the steps to rise by 5); 37 subtracts 28 and skips 21.",
         secs=50)

s = [1, 2]
while len(s) < 7:
    s.append(s[-1] * s[-2] + 1)
assert s == [1, 2, 3, 7, 22, 155, 3411] and 22 * 155 == 3410 and 155 * 23 == 3565
series_q("009", "Pattern: multiply-add", A, s, 6, [3410, 3412, 3565],
         "From the third term on, each term is the product of the two terms before it, plus 1",
         "1 × 2 + 1 = 3, 2 × 3 + 1 = 7, 3 × 7 + 1 = 22, 7 × 22 + 1 = 155. Next: 22 × 155 + 1 = 3,411.",
         ["3 = 1 × 2 + 1", "7 = 2 × 3 + 1", "22 = 3 × 7 + 1, 155 = 7 × 22 + 1", "22 × 155 + 1 = 3,411"],
         why="3,410 forgets the + 1; 3,412 adds 2; 3,565 multiplies 155 by 23 (one more than 22).", secs=75)

s = [2 ** n + 3 ** n for n in range(1, 7)]
assert s == [5, 13, 35, 97, 275, 793] and 35 * 3 == 105 and 35 * 3 - 16 == 89
series_q("009", "Missing number series", A, s, 3, [81, 105, 89],
         "Each term is 2ⁿ + 3ⁿ (equivalently, × 3 and subtract 2, 4, 8, 16, …)",
         "5 = 2 + 3, 13 = 4 + 9, 35 = 8 + 27, ? = 16 + 81 = 97, 275 = 32 + 243, 793 = 64 + 729. The missing term is 97.",
         ["2ⁿ + 3ⁿ for n = 1, 2, 3", "n = 4: 16 + 81 = 97", "Check: 97 × 3 − 16 = 275 ✓"],
         why="81 is 3⁴ alone; 105 triples 35 without subtracting 8; 89 subtracts 16 one step too early. None of them "
             "leads to 275.", secs=80)

s = [64]
for k in range(2, 8):
    s.append(s[-1] / k if k % 2 == 0 else s[-1] * k)
assert s == [64, 32, 96, 24, 120, 20, 140]
series_q("009", "Pattern: multiply-add", A, [F(x) for x in s], 6, [120, 160, 100],
         "Divide by 2, multiply by 3, divide by 4, multiply by 5, … (the operations alternate and the numbers rise)",
         "64 ÷ 2 = 32, 32 × 3 = 96, 96 ÷ 4 = 24, 24 × 5 = 120, 120 ÷ 6 = 20. Next: 20 × 7 = 140.",
         ["÷ 2, × 3, ÷ 4, × 5, ÷ 6", "Next: × 7", "20 × 7 = 140"],
         why="120 multiplies by 6 instead of 7; 160 multiplies by 8; 100 multiplies by 5 again.", secs=70)

s = [n * n * (n + 2) for n in range(1, 7)]
assert s == [3, 16, 45, 96, 175, 288] and 36 * 7 == 252 and 36 * 9 == 324 and 175 + 79 + 22 == 276
series_q("009", "Pattern: squares and cubes", A, s, 5, [252, 324, 276],
         "Each term is n² × (n + 2) for n = 1, 2, 3, …",
         "1 × 3 = 3, 4 × 4 = 16, 9 × 5 = 45, 16 × 6 = 96, 25 × 7 = 175. For n = 6: 36 × 8 = 288.",
         ["n²(n + 2) for n = 1 to 5", "n = 6: 36 × 8", "= 288"],
         short="Differences 13, 29, 51, 79 have second differences 16, 22, 28; next 34, so the next difference is "
               "113.",
         why="252 multiplies 36 by 7 (n + 1); 324 multiplies by 9 (n + 3); 276 keeps the second difference at 22.",
         secs=75)

s = series_from(40, lambda t, k: t + 2 * k + 9, 6)
assert s == [40, 51, 64, 79, 96, 115]
series_q("010", "Pattern: differences", B, s, 5, [113, 117, 192],
         "The differences are consecutive odd numbers: 11, 13, 15, 17, …",
         "40 + 11 = 51, 51 + 13 = 64, 64 + 15 = 79, 79 + 17 = 96. The next difference is 19, so the term is 96 + 19 "
         "= 115.",
         ["Differences: 11, 13, 15, 17", "Next: 19", "96 + 19 = 115"],
         why="113 adds 17 again; 117 adds 21 and skips 19; 192 doubles 96.", secs=30)

s = series_from(1, lambda t, k: -3 * t + 1, 6)
assert s == [1, -2, 7, -20, 61, -182]
series_q("010", "Pattern: multiply-add", I, s, 5, [-183, 182, -122],
         "Each term is −3 times the previous term, plus 1",
         "1 × (−3) + 1 = −2, (−2) × (−3) + 1 = 7, 7 × (−3) + 1 = −20, (−20) × (−3) + 1 = 61. Next: 61 × (−3) + 1 = "
         "−182.",
         ["× (−3) + 1 at every step", "61 × (−3) = −183", "−183 + 1 = −182"],
         why="−183 forgets the + 1; 182 drops the minus sign; −122 multiplies by −2.", secs=50)

fib = [1, 1]
while len(fib) < 8:
    fib.append(fib[-1] + fib[-2])
s = [3]
for f_ in fib[:7]:
    s.append(s[-1] + f_)
assert s == [3, 4, 5, 7, 10, 15, 23, 36]
series_q("010", "Pattern: differences", I, s, 7, [31, 38, 39],
         "The differences are the Fibonacci numbers 1, 1, 2, 3, 5, 8, … (each the sum of the two before)",
         "Differences: 1, 1, 2, 3, 5, 8. The next is 5 + 8 = 13, so the term is 23 + 13 = 36.",
         ["Differences: 1, 1, 2, 3, 5, 8", "Next difference: 5 + 8 = 13", "23 + 13 = 36"],
         why="31 adds 8 again; 38 adds the last two terms (15 + 23); 39 doubles the last difference (+16).", secs=55)

s = [(n + 1) ** 3 - n ** 3 for n in range(1, 7)]
assert s == [7, 19, 37, 61, 91, 127]
series_q("010", "Pattern: squares and cubes", I, s, 5, [125, 121, 133],
         "Each term is the difference of consecutive cubes: 2³ − 1³, 3³ − 2³, 4³ − 3³, …",
         "8 − 1 = 7, 27 − 8 = 19, 64 − 27 = 37, 125 − 64 = 61, 216 − 125 = 91. Next: 343 − 216 = 127.",
         ["(n + 1)³ − n³ for n = 1 to 5", "n = 6: 7³ − 6³ = 343 − 216", "= 127"],
         short="Differences 12, 18, 24, 30 rise by 6; the next difference is 36.",
         why="125 is 5³ itself; 121 adds 30 again; 133 adds 42 and skips 36.", secs=50)

s = [(2 * n - 1) * 2 * n for n in range(1, 7)]
assert s == [2, 12, 30, 56, 90, 132]
series_q("010", "Missing number series", I, s, 4, [72, 110, 81],
         "Each term is the product of two consecutive numbers: 1 × 2, 3 × 4, 5 × 6, …",
         "2 = 1 × 2, 12 = 3 × 4, 30 = 5 × 6, 56 = 7 × 8, ? = 9 × 10 = 90, 132 = 11 × 12. The missing term is 90.",
         ["1 × 2, 3 × 4, 5 × 6, 7 × 8", "Next: 9 × 10 = 90", "Check: 11 × 12 = 132 ✓"],
         why="72 = 8 × 9 and 110 = 10 × 11 shift the pairs by one; 81 = 9² uses only one factor.", secs=50)

s = series_from(1, lambda t, k: 2 * t + k ** 3, 6)
assert s == [1, 3, 14, 55, 174, 473] and 174 * 2 + 216 == 564 and 174 * 2 + 64 == 412 and 174 * 3 == 522
series_q("010", "Pattern: multiply-add", A, s, 5, [564, 412, 522],
         "Each term is twice the previous term plus 1³, 2³, 3³, 4³, …",
         "1 × 2 + 1 = 3, 3 × 2 + 8 = 14, 14 × 2 + 27 = 55, 55 × 2 + 64 = 174. Next: 174 × 2 + 125 = 473.",
         ["× 2 + 1³, × 2 + 2³, × 2 + 3³, × 2 + 4³", "Next: × 2 + 5³", "348 + 125 = 473"],
         why="564 adds 6³ and skips 5³; 412 adds 4³ again; 522 triples 174 instead of doubling it and adding a "
             "cube.", secs=75)

s = [n * PRIMES[n - 1] for n in range(1, 8)]
assert s == [2, 6, 15, 28, 55, 78, 119]
series_q("010", "Missing number series", A, s, 6, [91, 133, 112],
         "The n-th term is n × (n-th prime): 1 × 2, 2 × 3, 3 × 5, 4 × 7, …",
         "2 = 1 × 2, 6 = 2 × 3, 15 = 3 × 5, 28 = 4 × 7, 55 = 5 × 11, 78 = 6 × 13. The 7th prime is 17, so the next "
         "term is 7 × 17 = 119.",
         ["Primes: 2, 3, 5, 7, 11, 13", "Term = position × prime", "7 × 17 = 119"],
         why="91 = 7 × 13 repeats the prime 13; 133 = 7 × 19 skips 17; 112 = 7 × 16 uses 16, which is not prime.",
         secs=80)

s = [n * n * (n * n - 1) for n in range(2, 8)]
assert s == [12, 72, 240, 600, 1260, 2352] and 7 ** 4 == 2401 and 7 ** 3 * 6 == 2058 and 48 * 47 == 2256
series_q("010", "Pattern: squares and cubes", A, s, 5, [2401, 2058, 2256],
         "Each term is n² × (n² − 1) = n⁴ − n² for n = 2, 3, 4, …",
         "4 × 3 = 12, 9 × 8 = 72, 16 × 15 = 240, 25 × 24 = 600, 36 × 35 = 1,260. For n = 7: 49 × 48 = 2,352.",
         ["n²(n² − 1) for n = 2 to 6", "n = 7: 49 × 48", "= 2,352"],
         why="2,401 is 7⁴ without subtracting 7²; 2,058 is 7³ × 6 (n³(n − 1)); 2,256 is 48 × 47, which shifts both "
             "factors down by one.", secs=80)

s = [f_ * f_ for f_ in [1, 2, 3, 5, 8, 13]]
assert s == [1, 4, 9, 25, 64, 169]
series_q("010", "Pattern: squares and cubes", A, s, 5, [121, 144, 128],
         "The terms are squares of 1, 2, 3, 5, 8, …, where each base is the sum of the two bases before it",
         "Bases: 1, 2, 3, 5, 8 (1 + 2 = 3, 2 + 3 = 5, 3 + 5 = 8). The next base is 5 + 8 = 13, so the term is "
         "13² = 169.",
         ["1², 2², 3², 5², 8²", "Next base: 5 + 8 = 13", "13² = 169"],
         why="121 = 11² and 144 = 12² use bases 8 + 3 and 8 + 4; 128 doubles 64 instead of squaring the next base.",
         secs=75)

s = [1, 2]
for k in range(1, 6):
    s.append((s[-1] + s[-2]) * k)
assert s == [1, 2, 3, 10, 39, 196, 1175] and (39 + 196) * 4 == 940 and (39 + 196) * 6 == 1410
series_q("010", "Pattern: multiply-add", A, s, 6, [940, 1410, 235],
         "From the third term on, add the two terms before and multiply by 1, 2, 3, 4, …",
         "(1 + 2) × 1 = 3, (2 + 3) × 2 = 10, (3 + 10) × 3 = 39, (10 + 39) × 4 = 196. Next: (39 + 196) × 5 = 1,175.",
         ["(1 + 2) × 1 = 3", "(2 + 3) × 2 = 10", "(3 + 10) × 3 = 39, (10 + 39) × 4 = 196", "(39 + 196) × 5 = 1,175"],
         why="940 multiplies the sum by 4 again; 1,410 multiplies by 6; 235 adds the two terms but does not "
             "multiply.", secs=85)

# ================================================================ Wrong Number Series (009: B1 I2 A1; 010: B2 I3 A2)
T = "Wrong Number Series"
WRONG_Q = "Find the wrong number in the series:\n"


def wrong_q(bt, sub, diff, good, shown, opt_pos, concept, expl, steps, why, secs):
    bad = [k for k, (a, b) in enumerate(zip(good, shown)) if a != b]
    assert len(bad) == 1 and bad[0] in opt_pos and len(opt_pos) == 4, (good, shown)
    rival_rules_wrong(shown, bad[0], good[bad[0]], opt_pos)
    ans = N(shown[bad[0]])
    wrong = [N(shown[k]) for k in opt_pos if k != bad[0]]
    Q(bt, T, sub, diff, WRONG_Q + series_text(shown), ans, wrong, concept, expl, steps, None, why, secs, by=BRUTE)


good = series_from(3, lambda t, k: 2 * t + 4, 7)
assert good == [3, 10, 24, 52, 108, 220, 444]
wrong_q("009", "Find the wrong term", B, good, [3, 10, 24, 52, 106, 220, 444], [1, 3, 4, 6],
        "Each term is twice the previous term plus 4",
        "3 × 2 + 4 = 10, 10 × 2 + 4 = 24, 24 × 2 + 4 = 52, 52 × 2 + 4 = 108, 108 × 2 + 4 = 220, 220 × 2 + 4 = 444. "
        "The fifth term should be 108, not 106.",
        ["× 2 + 4 at every step", "52 × 2 + 4 = 108 ≠ 106", "108 × 2 + 4 = 220 ✓"],
        why="10, 52 and 444 all fit; 220 confirms 108, since 106 × 2 + 4 = 216.", secs=40)

good = series_from(1, lambda t, k: t * k + 1, 7)
assert good == [1, 2, 5, 16, 65, 326, 1957]
wrong_q("009", "Find the wrong term", I, good, [1, 2, 5, 16, 66, 326, 1957], [2, 3, 4, 5],
        "Multiply by 1, 2, 3, 4, … and add 1 each time",
        "1 × 1 + 1 = 2, 2 × 2 + 1 = 5, 5 × 3 + 1 = 16, 16 × 4 + 1 = 65, 65 × 5 + 1 = 326, 326 × 6 + 1 = 1,957. The "
        "fifth term should be 65, not 66.",
        ["× 1 + 1, × 2 + 1, × 3 + 1", "16 × 4 + 1 = 65 ≠ 66", "65 × 5 + 1 = 326 ✓"],
        why="5, 16 and 326 fit; 326 confirms 65, since 66 × 5 + 1 = 331.", secs=55)

good = [n * math.factorial(n) for n in range(1, 8)]
assert good == [1, 4, 18, 96, 600, 4320, 35280]
wrong_q("009", "Find the wrong term", I, good, [1, 4, 20, 96, 600, 4320, 35280], [1, 2, 3, 5],
        "Each term is n × n! (equivalently (n + 1)! − n!)",
        "1 × 1 = 1, 2 × 2 = 4, 3 × 6 = 18, 4 × 24 = 96, 5 × 120 = 600, 6 × 720 = 4,320, 7 × 5,040 = 35,280. The "
        "third term should be 18, not 20.",
        ["n × n!: 1, 4, 18, 96, 600, 4,320, 35,280", "3 × 3! = 18 ≠ 20", "4 × 4! = 96 ✓"],
        why="4, 96 and 4,320 are 2 × 2!, 4 × 4! and 6 × 6!; only 20 breaks the rule.", secs=60)

good = series_from(2, lambda t, k: t * (k + 1) - k, 7)
assert good == [2, 3, 7, 25, 121, 721, 5041]
wrong_q("009", "Find the wrong term", A, good, [2, 3, 7, 25, 121, 723, 5041], [2, 3, 5, 6],
        "Multiply by 2, 3, 4, 5, … and subtract 1, 2, 3, 4, …",
        "2 × 2 − 1 = 3, 3 × 3 − 2 = 7, 7 × 4 − 3 = 25, 25 × 5 − 4 = 121, 121 × 6 − 5 = 721, 721 × 7 − 6 = 5,041. The "
        "sixth term should be 721, not 723.",
        ["× 2 − 1, × 3 − 2, × 4 − 3, × 5 − 4", "121 × 6 − 5 = 721 ≠ 723", "721 × 7 − 6 = 5,041 ✓"],
        why="7, 25 and 5,041 fit; 5,041 confirms 721, since 723 × 7 − 6 = 5,055.", secs=75)

good = series_from(5, lambda t, k: t + 7 * k, 7)
assert good == [5, 12, 26, 47, 75, 110, 152]
wrong_q("010", "Find the wrong term", B, good, [5, 12, 26, 47, 76, 110, 152], [1, 3, 4, 6],
        "The differences are multiples of 7: 7, 14, 21, 28, 35, 42",
        "5 + 7 = 12, 12 + 14 = 26, 26 + 21 = 47, 47 + 28 = 75, 75 + 35 = 110, 110 + 42 = 152. The fifth term should "
        "be 75, not 76.",
        ["Differences shown: 7, 14, 21, 29, 34, 42", "Expected: 7, 14, 21, 28, 35, 42", "47 + 28 = 75 ≠ 76"],
        why="12, 47 and 152 fit; 110 − 35 = 75 confirms that 76 is wrong.", secs=40)

good = series_from(5, lambda t, k: 2 * t - 3, 7)
assert good == [5, 7, 11, 19, 35, 67, 131]
wrong_q("010", "Find the wrong term", B, good, [5, 7, 11, 19, 35, 69, 131], [2, 4, 5, 6],
        "Each term is twice the previous term minus 3",
        "5 × 2 − 3 = 7, 7 × 2 − 3 = 11, 11 × 2 − 3 = 19, 19 × 2 − 3 = 35, 35 × 2 − 3 = 67, 67 × 2 − 3 = 131. The "
        "sixth term should be 67, not 69.",
        ["× 2 − 3 at every step", "35 × 2 − 3 = 67 ≠ 69", "67 × 2 − 3 = 131 ✓"],
        why="11, 35 and 131 fit; 131 confirms 67, since 69 × 2 − 3 = 135.", secs=40)

good = [2 * n * n + n + 7 for n in range(0, 7)]
assert good == [7, 10, 17, 28, 43, 62, 85]
wrong_q("010", "Find the wrong term", I, good, [7, 10, 17, 28, 44, 62, 85], [1, 3, 4, 5],
        "The differences rise by 4 each time: 3, 7, 11, 15, 19, 23",
        "7 + 3 = 10, 10 + 7 = 17, 17 + 11 = 28, 28 + 15 = 43, 43 + 19 = 62, 62 + 23 = 85. The fifth term should be "
        "43, not 44.",
        ["Differences shown: 3, 7, 11, 16, 18, 23", "Expected: 3, 7, 11, 15, 19, 23", "28 + 15 = 43 ≠ 44"],
        why="10, 28 and 62 fit; 62 − 19 = 43 confirms that 44 is wrong.", secs=50)

good = series_from(3, lambda t, k: 3 * t - 4, 7)
assert good == [3, 5, 11, 29, 83, 245, 731]
wrong_q("010", "Find the wrong term", I, good, [3, 5, 11, 29, 83, 245, 733], [2, 4, 5, 6],
        "Each term is 3 times the previous term minus 4",
        "3 × 3 − 4 = 5, 5 × 3 − 4 = 11, 11 × 3 − 4 = 29, 29 × 3 − 4 = 83, 83 × 3 − 4 = 245, 245 × 3 − 4 = 731. The "
        "last term should be 731, not 733.",
        ["× 3 − 4 at every step", "245 × 3 − 4 = 731 ≠ 733", "11, 83 and 245 all fit"],
        why="11, 83 and 245 each equal 3 × (previous) − 4; only the last term breaks the rule.", secs=50)

good = [n ** 4 - n for n in range(1, 8)]
assert good == [0, 14, 78, 252, 620, 1290, 2394]
wrong_q("010", "Find the wrong term", I, good, [0, 14, 78, 252, 622, 1290, 2394], [1, 3, 4, 6],
        "Each term is n⁴ − n for n = 1, 2, 3, …",
        "1 − 1 = 0, 16 − 2 = 14, 81 − 3 = 78, 256 − 4 = 252, 625 − 5 = 620, 1,296 − 6 = 1,290, 2,401 − 7 = 2,394. "
        "The fifth term should be 620, not 622.",
        ["n⁴ − n for n = 1 to 7", "5⁴ − 5 = 620 ≠ 622", "6⁴ − 6 = 1,290 ✓"],
        why="14, 252 and 2,394 are 2⁴ − 2, 4⁴ − 4 and 7⁴ − 7; only 622 breaks the rule.", secs=60)

good = series_from(1, lambda t, k: 2 * (t + k), 7)
assert good == [1, 4, 12, 30, 68, 146, 304]
wrong_q("010", "Find the wrong term", A, good, [1, 4, 12, 30, 68, 148, 304], [2, 3, 5, 6],
        "Add 1, 2, 3, 4, … to the term and then double",
        "(1 + 1) × 2 = 4, (4 + 2) × 2 = 12, (12 + 3) × 2 = 30, (30 + 4) × 2 = 68, (68 + 5) × 2 = 146, (146 + 6) × 2 "
        "= 304. The sixth term should be 146, not 148.",
        ["(t + 1) × 2, (t + 2) × 2, (t + 3) × 2", "(68 + 5) × 2 = 146 ≠ 148", "(146 + 6) × 2 = 304 ✓"],
        why="12, 30 and 304 fit; 304 confirms 146, since (148 + 6) × 2 = 308.", secs=75)

good = [2]
for k in range(7):
    good.append(good[-1] * 2 + 1 if k % 2 == 0 else good[-1] * 3 - 1)
assert good == [2, 5, 14, 29, 86, 173, 518, 1037]
wrong_q("010", "Find the wrong term", A, good, [2, 5, 14, 29, 86, 175, 518, 1037], [2, 3, 5, 7],
        "The operations alternate: × 2 + 1, then × 3 − 1",
        "2 × 2 + 1 = 5, 5 × 3 − 1 = 14, 14 × 2 + 1 = 29, 29 × 3 − 1 = 86, 86 × 2 + 1 = 173, 173 × 3 − 1 = 518, 518 × 2 + 1 = "
        "1,037. The sixth term should be 173, not 175.",
        ["× 2 + 1, × 3 − 1, × 2 + 1, × 3 − 1", "86 × 2 + 1 = 173 ≠ 175", "173 × 3 − 1 = 518 ✓"],
        why="14, 29 and 1,037 fit; 518 confirms 173, since 175 × 3 − 1 = 524.", secs=75)


# ================================================================ Quadratic Equations (009: B6 I1 A2; 010: B2 I9 A1)
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
    disc = b * b - 4 * a * c
    assert disc >= 0 and len(set(roots)) == (1 if disc == 0 else 2), (a, b, c, roots)


def qe(bt, sub, diff, pre, eq1, eq2, xs, ys, expect, wrong_syms, concept, expl, steps, short=None, why=None,
       secs=None):
    got = relation(xs, ys)
    assert got == expect, (eq1, eq2, got)
    assert "cbe" not in wrong_syms and expect not in wrong_syms and len(set(wrong_syms)) == 2
    if expect in (">", "<"):  # a strict answer never sits beside its weaker form
        assert {">": ">=", "<": "<="}[expect] not in wrong_syms
    if expect == "cbe":
        third = next(s_ for s_ in ("<", ">", "<=", ">=") if s_ not in wrong_syms)
        wrong = [REL[wrong_syms[0]], REL[wrong_syms[1]], REL[third]]
        no_true_distractor(xs, ys, [*wrong_syms, third])
    else:
        wrong = [REL[wrong_syms[0]], REL["cbe"], REL[wrong_syms[1]]]
        no_true_distractor(xs, ys, wrong_syms)
    Q(bt, T, sub, diff, f"{pre}\nI. {eq1}\nII. {eq2}", REL[expect], wrong, concept, expl, steps, short, why, secs)


xs, ys = [F(12), F(13)], [F(8), F(12)]
roots_check(1, -25, 156, xs), roots_check(1, -20, 96, ys)
qe("009", "Relation between roots", B, "Solve equations I and II and choose the relation between x and y that holds "
   "for every pair of roots.", "x² − 25x + 156 = 0", "y² − 20y + 96 = 0", xs, ys, ">=", [">", "<"],
   "Factorise; a root shared by both equations makes the relation non-strict",
   "I: (x − 12)(x − 13) = 0, so x = 12 or 13. II: (y − 8)(y − 12) = 0, so y = 8 or 12. The smallest x (12) equals "
   "the largest y (12), and every other pair has x > y. So x ≥ y.",
   ["I: 12 × 13 = 156, 12 + 13 = 25 ⇒ x = 12, 13", "II: 8 × 12 = 96, 8 + 12 = 20 ⇒ y = 8, 12",
    "min x = 12 = max y", "So x ≥ y"],
   why="x > y fails for the pair x = y = 12; x < y holds for no pair.", secs=40)

xs, ys = [F(-7), F(-8)], [F(-4), F(-6)]
roots_check(1, 15, 56, xs), roots_check(1, 10, 24, ys)
qe("009", "Relation between roots", B, "Each quadratic below has two negative roots. Factorise both and decide which "
   "relation holds.", "x² + 15x + 56 = 0", "y² + 10y + 24 = 0", xs, ys, "<", [">", ">="],
   "Factorise both; with negative roots, the larger number is the one nearer zero",
   "I: (x + 7)(x + 8) = 0, so x = −7 or −8. II: (y + 4)(y + 6) = 0, so y = −4 or −6. The largest x (−7) is below "
   "the smallest y (−6), so x < y.",
   ["I: x = −7, −8", "II: y = −4, −6", "max x = −7 < min y = −6"],
   why="x > y and x ≥ y treat 7 and 8 as larger than 4 and 6, ignoring the minus signs.", secs=40)

xs, ys = [F(7), F(-6)], [F(5), F(9)]
roots_check(1, -1, -42, xs), roots_check(1, -14, 45, ys)
qe("009", "Relation between roots", B, "Find the roots of I and II and decide which relation between x and y, if "
   "any, always holds.", "x² − x − 42 = 0", "y² − 14y + 45 = 0", xs, ys, "cbe", [">", "<"],
   "When one set of roots straddles the other, no single relation holds for every pair",
   "I: (x − 7)(x + 6) = 0, so x = 7 or −6. II: (y − 5)(y − 9) = 0, so y = 5 or 9. x = 7 is greater than y = 5 but "
   "less than y = 9, so no relation holds for every pair.",
   ["I: x = 7, −6", "II: y = 5, 9", "7 > 5 but 7 < 9", "Relationship cannot be established"],
   why="x > y fails for 7 and 9; x < y fails for 7 and 5; x ≤ y and x ≥ y fail for the same pairs.", secs=45)

xs, ys = [F(8), F(-6)], [F(-6), F(-8)]
roots_check(1, -2, -48, xs), roots_check(1, 14, 48, ys)
qe("009", "Relation between roots", B, "Solve both equations and choose the relation between x and y.",
   "x² − 2x − 48 = 0", "y² + 14y + 48 = 0", xs, ys, ">=", [">", "<="],
   "Factorise; compare the smallest x with the largest y",
   "I: (x − 8)(x + 6) = 0, so x = 8 or −6. II: (y + 6)(y + 8) = 0, so y = −6 or −8. The smallest x (−6) equals the "
   "largest y (−6), and every other pair has x > y. So x ≥ y.",
   ["I: x = 8, −6", "II: y = −6, −8", "min x = −6 = max y", "So x ≥ y"],
   why="x > y fails for the pair x = y = −6; x ≤ y holds only for that one pair.", secs=45)

xs, ys = [F(5), F(-12)], [F(12), F(14)]
roots_check(1, 7, -60, xs), roots_check(1, -26, 168, ys)
qe("009", "Relation between roots", B, "Equation I has a positive and a negative root, while II has two positive roots. "
   "Which relation between x and y holds?", "x² + 7x − 60 = 0", "y² − 26y + 168 = 0", xs, ys, "<", [">", ">="],
   "Factorise each equation; compare the largest x with the smallest y",
   "I: (x + 12)(x − 5) = 0, so x = 5 or −12. II: (y − 12)(y − 14) = 0, so y = 12 or 14. The largest x (5) is below "
   "the smallest y (12), so x < y.",
   ["I: x = 5, −12", "II: y = 12, 14", "max x = 5 < min y = 12"],
   why="x > y and x ≥ y take x = 12 from I (the root is −12, not 12).", secs=40)

xs, ys = [F(13), F(17)], [F(17)]
roots_check(1, -30, 221, xs), roots_check(1, -34, 289, ys)
qe("009", "Relation between roots", B, "Equation II is a perfect square. Solve both equations and choose the relation "
   "between x and y.", "x² − 30x + 221 = 0", "y² − 34y + 289 = 0", xs, ys, "<=", ["<", ">="],
   "A perfect-square quadratic has one repeated root",
   "I: (x − 13)(x − 17) = 0, so x = 13 or 17. II: (y − 17)² = 0, so y = 17 only. x = 17 equals y and x = 13 is less "
   "than y. So x ≤ y.",
   ["I: 13 × 17 = 221, 13 + 17 = 30 ⇒ x = 13, 17", "II: (y − 17)² = 0 ⇒ y = 17", "x ≤ 17 = y"],
   why="x < y fails for x = 17; x ≥ y fails for x = 13.", secs=45)

x_ = F(20)
assert 3 * (x_ + 4) - 2 * (x_ - 1) == 2 * x_ - 6
xs, ys = [x_], [F(20), F(21)]
roots_check(1, -41, 420, ys)
qe("009", "Linear vs quadratic", I, "Equation I is linear and equation II is quadratic. Solve both and choose the "
   "relation between x and y.", "3(x + 4) − 2(x − 1) = 2x − 6", "y² − 41y + 420 = 0", xs, ys, "<=", ["<", ">"],
   "Expand and solve the linear equation; factorise the quadratic",
   "I: 3x + 12 − 2x + 2 = 2x − 6, so x + 14 = 2x − 6 and x = 20. II: (y − 20)(y − 21) = 0, so y = 20 or 21. x = 20 "
   "equals one value of y and is less than the other. So x ≤ y.",
   ["I: x + 14 = 2x − 6 ⇒ x = 20", "II: 20 × 21 = 420, 20 + 21 = 41 ⇒ y = 20, 21", "x = 20 ≤ y"],
   why="x < y fails for y = 20; x > y holds for no value of y.", secs=60)

x_ = F(20, 7)
assert (x_ + 2) * (x_ + 3) == (x_ - 1) ** 2 + 25
xs, ys = [x_], [F(1), F(-2)]
roots_check(1, 1, -2, ys)
qe("009", "Linear vs quadratic", A, "Equation I looks quadratic. Simplify it, solve both equations and choose the "
   "relation between x and y.", "(x + 2)(x + 3) = (x − 1)² + 25", "y² + y − 2 = 0", xs, ys, ">", ["<", "<="],
   "The x² terms cancel, so equation I is really linear",
   "I: x² + 5x + 6 = x² − 2x + 1 + 25, so 7x = 20 and x = 20/7 ≈ 2.86. II: (y + 2)(y − 1) = 0, so y = 1 or −2. "
   "x ≈ 2.86 exceeds both values of y, so x > y.",
   ["I: x² cancels ⇒ 5x + 6 = −2x + 26", "7x = 20 ⇒ x = 20/7 ≈ 2.86", "II: y = 1, −2", "x > y"],
   why="x < y and x ≤ y would need x to be at most 1; treating I as a quadratic invents a second root that does not "
       "exist.", secs=85)

r3 = 3 ** 0.5
xs_f, ys_f = [3 * r3, r3], [1.0]
assert all(abs(x * x - 4 * r3 * x + 9) < 1e-9 for x in xs_f)
xs, ys = [F(3 * r3), F(r3)], [F(1)]
roots_check(1, -2, 1, ys)
qe("009", "Relation between roots", A, "Equation I has an irrational coefficient (√3 ≈ 1.732). Solve both equations "
   "and choose the relation between x and y.", "x² − 4√3x + 9 = 0", "y² − 2y + 1 = 0", xs, ys, ">", ["<", "<="],
   "Use the quadratic formula (or split 4√3x = 3√3x + √3x); II is a perfect square",
   "I: discriminant = 48 − 36 = 12, so x = (4√3 ± 2√3)/2 = 3√3 or √3, that is about 5.20 or 1.73. II: (y − 1)² = 0, "
   "so y = 1. Both values of x exceed 1, so x > y.",
   ["I: D = (4√3)² − 36 = 12, √D = 2√3", "x = 3√3 ≈ 5.20 or √3 ≈ 1.73", "II: y = 1", "min x ≈ 1.73 > 1"],
   why="x < y and x ≤ y fail because even the smaller root √3 is above 1; no root is shared, so the relation is "
       "strict.", secs=85)

xs, ys = [F(10), F(-7)], [F(-7), F(-10)]
roots_check(1, -3, -70, xs), roots_check(1, 17, 70, ys)
qe("010", "Relation between roots", B, "Solve both equations and choose the relation between x and y that holds for "
   "all their roots.", "x² − 3x − 70 = 0", "y² + 17y + 70 = 0", xs, ys, ">=", [">", "<"],
   "Factorise; compare the smallest x with the largest y",
   "I: (x − 10)(x + 7) = 0, so x = 10 or −7. II: (y + 7)(y + 10) = 0, so y = −7 or −10. The smallest x (−7) equals "
   "the largest y (−7), and every other pair has x > y. So x ≥ y.",
   ["I: x = 10, −7", "II: y = −7, −10", "min x = −7 = max y", "So x ≥ y"],
   why="x > y fails for the pair x = y = −7; x < y holds for no pair.", secs=40)

xs, ys = [F(15), F(16)], [F(16), F(19)]
roots_check(1, -31, 240, xs), roots_check(1, -35, 304, ys)
qe("010", "Relation between roots", B, "The two quadratics below have large constant terms. Factorise them and pick "
   "the relation that is true for every pair of roots.", "x² − 31x + 240 = 0", "y² − 35y + 304 = 0", xs, ys, "<=", ["<", ">"],
   "Factorise each equation and look for a common root",
   "I: (x − 15)(x − 16) = 0, so x = 15 or 16. II: (y − 16)(y − 19) = 0, so y = 16 or 19. The largest x (16) equals "
   "the smallest y (16), and every other pair has x < y. So x ≤ y.",
   ["I: 15 × 16 = 240 ⇒ x = 15, 16", "II: 16 × 19 = 304 ⇒ y = 16, 19", "max x = 16 = min y", "So x ≤ y"],
   why="x < y fails for x = y = 16; x > y holds for no pair.", secs=45)

xs, ys = [F(2, 3), F(-4)], [F(4), F(5, 2)]
roots_check(3, 10, -8, xs), roots_check(2, -13, 20, ys)
qe("010", "Relation between roots", I, "Equation I has one positive and one negative root. Solve I and II and compare "
   "x with y.", "3x² + 10x − 8 = 0", "2y² − 13y + 20 = 0", xs, ys, "<", [">", ">="],
   "Split the middle terms: 10x = 12x − 2x and −13y = −8y − 5y",
   "I: 3x² + 12x − 2x − 8 = (3x − 2)(x + 4) = 0, so x = 2/3 or −4. II: 2y² − 8y − 5y + 20 = (y − 4)(2y − 5) = 0, so "
   "y = 4 or 2.5. The largest x (0.67) is below the smallest y (2.5), so x < y.",
   ["I: (3x − 2)(x + 4) = 0 ⇒ x = 2/3, −4", "II: (y − 4)(2y − 5) = 0 ⇒ y = 4, 2.5", "max x ≈ 0.67 < min y = 2.5"],
   why="x > y and x ≥ y reverse the comparison; every root of I is below every root of II.", secs=65)

xs, ys = [F(3), F(9, 4)], [F(2), F(3, 5)]
roots_check(4, -21, 27, xs), roots_check(5, -13, 6, ys)
qe("010", "Relation between roots", I, "The roots of both equations below are positive. Solve them and mark the "
   "relation between x and y.", "4x² − 21x + 27 = 0", "5y² − 13y + 6 = 0", xs, ys, ">", ["<", "<="],
   "Factorise by splitting the middle term",
   "I: 4x² − 12x − 9x + 27 = (4x − 9)(x − 3) = 0, so x = 3 or 2.25. II: 5y² − 10y − 3y + 6 = (5y − 3)(y − 2) = 0, so "
   "y = 2 or 0.6. The smallest x (2.25) exceeds the largest y (2), so x > y.",
   ["I: (4x − 9)(x − 3) = 0 ⇒ x = 2.25, 3", "II: (5y − 3)(y − 2) = 0 ⇒ y = 0.6, 2", "min x = 2.25 > max y = 2"],
   why="x < y and x ≤ y fail for every pair; no root is shared, so the relation is strict.", secs=65)

xs, ys = [F(-5, 2), F(-4, 3)], [F(-2), F(-5, 3)]
roots_check(6, 23, 20, xs), roots_check(3, 11, 10, ys)
qe("010", "Relation between roots", I, "Both equations have negative fractional roots. Solve them and choose the "
   "relation between x and y, if any, that holds for all their roots.", "6x² + 23x + 20 = 0", "3y² + 11y + 10 = 0",
   xs, ys, "cbe", ["<", ">="],
   "Factorise and place all four roots on the number line",
   "I: 6x² + 15x + 8x + 20 = (2x + 5)(3x + 4) = 0, so x = −2.5 or −1.33. II: 3y² + 6y + 5y + 10 = (y + 2)(3y + 5) = "
   "0, so y = −2 or −1.67. x = −2.5 is below both values of y, but x = −1.33 is above both. No relation holds for "
   "every pair.",
   ["I: x = −2.5, −1.33", "II: y = −2, −1.67", "−2.5 < −2 but −1.33 > −1.67", "Relationship cannot be established"],
   why="x < y fails for x = −1.33; x ≥ y fails for x = −2.5; x > y and x ≤ y fail for the same pairs.", secs=70)

xs, ys = [F(5, 2), F(3, 4)], [F(5, 2), F(3)]
roots_check(8, -26, 15, xs), roots_check(2, -11, 15, ys)
qe("010", "Relation between roots", I, "Solve both equations and choose the relation between x and y that holds for "
   "every pair of roots.", "8x² − 26x + 15 = 0", "2y² − 11y + 15 = 0", xs, ys, "<=", ["<", ">"],
   "Factorise both; a common root makes the relation non-strict",
   "I: 8x² − 20x − 6x + 15 = (2x − 5)(4x − 3) = 0, so x = 2.5 or 0.75. II: 2y² − 5y − 6y + 15 = (2y − 5)(y − 3) = 0, "
   "so y = 2.5 or 3. The largest x (2.5) equals the smallest y (2.5), and every other pair has x < y. So x ≤ y.",
   ["I: (2x − 5)(4x − 3) = 0 ⇒ x = 2.5, 0.75", "II: (2y − 5)(y − 3) = 0 ⇒ y = 2.5, 3", "Common value 2.5 ⇒ x ≤ y"],
   why="x < y fails for x = y = 2.5; x > y holds for no pair.", secs=70)

x_ = F(8)
assert F("0.6") * x_ - F("1.5") == F("0.35") * x_ + F("0.5")
xs, ys = [x_], [F(9), F(13)]
roots_check(1, -22, 117, ys)
qe("010", "Linear vs quadratic", I, "Equation I is linear with decimal coefficients and equation II is quadratic. "
   "Solve both and choose the relation between x and y.", "0.6x − 1.5 = 0.35x + 0.5", "y² − 22y + 117 = 0", xs, ys,
   "<", [">", ">="],
   "Collect the x-terms of I; factorise II",
   "I: 0.6x − 0.35x = 0.5 + 1.5, so 0.25x = 2 and x = 8. II: (y − 9)(y − 13) = 0, so y = 9 or 13. x = 8 is below "
   "both values of y, so x < y.",
   ["I: 0.25x = 2 ⇒ x = 8", "II: 9 × 13 = 117, 9 + 13 = 22 ⇒ y = 9, 13", "x = 8 < 9"],
   why="x > y and x ≥ y would need x to be at least 9; solving I as 0.95x = 2 (adding the coefficients) is the usual "
       "slip.", secs=60)

xs, ys = [F(0), F(4)], [F(-1), F(-4)]
roots_check(1, -4, 0, xs), roots_check(1, 5, 4, ys)
qe("010", "Relation between roots", I, "Equation I has no constant term. Find all roots of I and II (do not divide "
   "by x) and choose the relation between x and y.", "x² − 4x = 0", "y² + 5y + 4 = 0", xs, ys, ">", ["<", "<="],
   "x² − 4x = x(x − 4): x = 0 is also a root",
   "I: x(x − 4) = 0, so x = 0 or 4. II: (y + 1)(y + 4) = 0, so y = −1 or −4. The smallest x (0) exceeds the largest "
   "y (−1), so x > y.",
   ["I: x(x − 4) = 0 ⇒ x = 0, 4", "II: y = −1, −4", "min x = 0 > max y = −1"],
   why="x < y and x ≤ y fail for every pair, even if x = 0 is (wrongly) dropped by dividing by x.", secs=50)

xs, ys = [F(4, 3), F(2, 3)], [F(1, 2), F(1, 5)]
roots_check(9, -18, 8, xs), roots_check(10, -7, 1, ys)
qe("010", "Relation between roots", I, "The roots of both equations are fractions. Solve them and choose the "
   "relation between x and y.", "9x² − 18x + 8 = 0", "10y² − 7y + 1 = 0", xs, ys, ">", ["<", "<="],
   "Split the middle term: −18x = −12x − 6x and −7y = −5y − 2y",
   "I: 9x² − 12x − 6x + 8 = (3x − 4)(3x − 2) = 0, so x = 4/3 or 2/3. II: 10y² − 5y − 2y + 1 = (2y − 1)(5y − 1) = 0, "
   "so y = 1/2 or 1/5. The smallest x (0.67) exceeds the largest y (0.5), so x > y.",
   ["I: (3x − 4)(3x − 2) = 0 ⇒ x = 1.33, 0.67", "II: (2y − 1)(5y − 1) = 0 ⇒ y = 0.5, 0.2", "min x ≈ 0.67 > max y = 0.5"],
   why="x < y and x ≤ y fail for every pair; no root is shared, so the relation is strict.", secs=70)

xs, ys = [F("0.8"), F("0.5")], [F("0.7"), F("0.4")]
roots_check(1, F("-1.3"), F("0.4"), xs), roots_check(1, F("-1.1"), F("0.28"), ys)
qe("010", "Relation between roots", I, "The equations below have decimal coefficients. Solve them and choose the "
   "relation between x and y, if any.", "x² − 1.3x + 0.4 = 0", "y² − 1.1y + 0.28 = 0", xs, ys, "cbe", [">", "<="],
   "Find two numbers with the given sum and product (or multiply by 100 and factorise)",
   "I: the roots add to 1.3 and multiply to 0.4, so x = 0.8 or 0.5. II: the roots add to 1.1 and multiply to 0.28, "
   "so y = 0.7 or 0.4. x = 0.5 is less than y = 0.7 but more than y = 0.4. No relation holds for every pair.",
   ["I: 0.8 + 0.5 = 1.3, 0.8 × 0.5 = 0.4", "II: 0.7 + 0.4 = 1.1, 0.7 × 0.4 = 0.28", "0.5 < 0.7 but 0.5 > 0.4",
    "Relationship cannot be established"],
   why="x > y fails for 0.5 and 0.7; x ≤ y fails for 0.8 and 0.7; x < y and x ≥ y fail for the same pairs.",
   secs=65)

xs, ys = [F(5), F(-1)], [F(5), F(10)]
for x in xs:
    assert (x - 2) ** 2 == 9
roots_check(1, -15, 50, ys)
qe("010", "Relation between roots", I, "Equation I is given as a square. Take both square roots, solve II, and compare "
   "x with y.", "(x − 2)² = 9", "y² − 15y + 50 = 0", xs, ys, "<=", ["<", ">="],
   "(x − 2)² = 9 means x − 2 = 3 or x − 2 = −3",
   "I: x − 2 = ±3, so x = 5 or −1. II: (y − 5)(y − 10) = 0, so y = 5 or 10. x = 5 equals one value of y and every "
   "other pair has x < y. So x ≤ y.",
   ["I: x = 2 ± 3 = 5, −1", "II: y = 5, 10", "max x = 5 = min y", "So x ≤ y"],
   why="x < y fails for x = y = 5; x ≥ y fails for x = −1.", secs=55)

xs = [F(1), F(2)]
assert all(4 ** int(x) - 6 * 2 ** int(x) + 8 == 0 for x in xs)
assert [x for x in range(-10, 11) if 4 ** x - 6 * 2 ** x + 8 == 0] == [1, 2]
ys = [F(2), F(3)]
roots_check(1, -5, 6, ys)
qe("010", "Relation between roots", A, "Equation I is exponential. Find every real x and y and choose the relation "
   "between them.", "2^(2x) − 6 × 2ˣ + 8 = 0", "y² − 5y + 6 = 0", xs, ys, "<=", ["<", ">="],
   "Put t = 2ˣ: equation I becomes a quadratic in t, and t must be positive",
   "I: t² − 6t + 8 = 0, so t = 2 or 4, that is 2ˣ = 2 or 2ˣ = 4, giving x = 1 or 2. II: (y − 2)(y − 3) = 0, so y = 2 "
   "or 3. The largest x (2) equals the smallest y (2), and every other pair has x < y. So x ≤ y.",
   ["I: (t − 2)(t − 4) = 0 with t = 2ˣ", "2ˣ = 2 or 4 ⇒ x = 1, 2", "II: y = 2, 3", "max x = 2 = min y ⇒ x ≤ y"],
   why="x < y fails for x = y = 2; x ≥ y would follow only if the roots t = 2, 4 were mistaken for the values of x.",
   secs=90)


# ================================================================ Number System (009: B1 I2 A2; 010: B2 I1 A1)
T = "Number System"
xs_ = [x for x in range(10) if int(f"35{x}72") % 9 == 0]
assert xs_ == [1]
Q("009", T, "Divisibility", B, "The five-digit number 35x72, where x is a digit, is divisible by 9. What is x?",
  "1", ["0", "8", "4"],
  "A number is divisible by 9 when the sum of its digits is divisible by 9",
  "Digit sum = 3 + 5 + x + 7 + 2 = 17 + x. The only digit that makes this a multiple of 9 is x = 1 (sum 18).",
  ["3 + 5 + 7 + 2 = 17", "17 + x must be 18", "x = 1"],
  why="0 gives a digit sum of 17, 8 gives 25 and 4 gives 21; none is a multiple of 9 (21 is only a multiple of 3).",
  secs=35)

assert (2341 * 4567 * 1234) % 9 == 4 and (1 * 4 * 1) == 4 and (2341 + 4567 + 1234) % 9 == 6
Q("009", T, "Remainders", I, "What is the remainder when 2,341 × 4,567 × 1,234 is divided by 9?",
  "4", ["6", "0", "1"],
  "A number leaves the same remainder on division by 9 as its digit sum; remainders of a product multiply",
  "2,341 → 2 + 3 + 4 + 1 = 10 → remainder 1. 4,567 → 22 → remainder 4. 1,234 → 10 → remainder 1. So the product "
  "leaves 1 × 4 × 1 = 4.",
  ["2,341 ≡ 1 (mod 9)", "4,567 ≡ 4 (mod 9)", "1,234 ≡ 1 (mod 9)", "1 × 4 × 1 = 4"],
  why="6 is the remainder of the sum 2,341 + 4,567 + 1,234, not of the product; 0 and 1 would need a factor "
      "divisible by 9 or every remainder to be 1.", secs=50)

fr = [F(3, 4), F(5, 6), F(9, 10)]
lcm_f = F(math.lcm(3, 5, 9), math.gcd(math.gcd(4, 6), 10))
assert lcm_f == F(45, 2) and all((lcm_f / f).denominator == 1 for f in fr)
assert all((F(45, 1) / f).denominator == 1 for f in fr) and math.gcd(math.gcd(3, 5), 9) == 1
assert (F(1, 60) / fr[0]).denominator != 1
Q("009", T, "HCF and LCM", I, "What is the LCM of the fractions 3/4, 5/6 and 9/10?",
  "45/2", ["45", "1/60", "135/2"],
  "LCM of fractions = LCM of the numerators ÷ HCF of the denominators",
  "LCM(3, 5, 9) = 45 and HCF(4, 6, 10) = 2, so the LCM is 45/2. Check: 45/2 ÷ 3/4 = 30, 45/2 ÷ 5/6 = 27 and "
  "45/2 ÷ 9/10 = 25, all whole numbers.",
  ["LCM of 3, 5, 9 = 45", "HCF of 4, 6, 10 = 2", "LCM = 45/2"],
  why="45 is a common multiple but not the least (45/2 already works); 1/60 is HCF of numerators ÷ LCM of "
      "denominators, the formula for the HCF; 135/2 uses the product 3 × 5 × 9 instead of the LCM.", secs=55)

cnt = sum(1 for d in range(1, 10801) if 10800 % d == 0 and d % 15 == 0)
assert 10800 == 2 ** 4 * 3 ** 3 * 5 ** 2 and cnt == 30 and sum(1 for d in range(1, 10801) if 10800 % d == 0) == 60
Q("009", T, "Divisibility", A, "How many divisors of 10,800 are multiples of 15?",
  "30", ["60", "24", "45"],
  "A divisor that is a multiple of 15 is 15 × (a divisor of 10,800 ÷ 15)",
  "10,800 = 2⁴ × 3³ × 5². A multiple of 15 must contain at least one 3 and one 5, so it is 15 × k with k a divisor "
  "of 720 = 2⁴ × 3² × 5. Number of such k = (4 + 1)(2 + 1)(1 + 1) = 30.",
  ["10,800 = 2⁴ × 3³ × 5²", "10,800 ÷ 15 = 720 = 2⁴ × 3² × 5", "Divisors of 720 = 5 × 3 × 2 = 30"],
  why="60 is the number of all divisors of 10,800; 24 counts the divisors of 720 as (4)(3)(2); 45 uses the exponents "
      "of 10,800 with only the 5 reduced, (5)(3)(3).", secs=85)

assert math.factorial(28) % 29 == 28 and math.factorial(27) % 29 == 1
Q("009", T, "Remainders", A, "What is the remainder when 28! (the product 1 × 2 × 3 × … × 28) is divided by 29?",
  "28", ["1", "0", "27"],
  "Wilson's theorem: for a prime p, (p − 1)! leaves remainder p − 1 when divided by p",
  "29 is prime, so 28! = (29 − 1)! ≡ −1 (mod 29). A remainder of −1 is the same as 29 − 1 = 28.",
  ["29 is prime", "(p − 1)! ≡ −1 (mod p)", "−1 ≡ 28 (mod 29)"],
  short="Pair each number from 2 to 27 with its inverse mod 29: the pairs multiply to 1, leaving 1 × 28 ≡ 28.",
  why="1 is the remainder of 27!, which forgets the factor 28; 0 would need 29 to divide 28!, but 29 is a prime "
      "larger than every factor; 27 subtracts 2 instead of 1 from 29.", secs=80)

L_ = math.lcm(2 ** 3 * 3 ** 2 * 5, 2 ** 2 * 3 ** 3 * 7)
assert L_ == 7560 == 2 ** 3 * 3 ** 3 * 5 * 7 and math.gcd(360, 756) == 36
Q("010", T, "HCF and LCM", B, "What is the LCM of 2³ × 3² × 5 and 2² × 3³ × 7?",
  "7,560", ["36", "2,72,160", "1,260"],
  "The LCM takes every prime to its highest power in either number",
  "Highest powers: 2³, 3³, 5 and 7. LCM = 8 × 27 × 5 × 7 = 7,560.",
  ["2: highest power 2³", "3: highest power 3³", "5 and 7 once each", "8 × 27 × 35 = 7,560"],
  why="36 = 2² × 3² is the HCF; 2,72,160 is the product of the two numbers (360 × 756); 1,260 uses the lower power "
      "of 2 and 3² instead of 3³.", secs=40)

assert (13 ** 2025 - 7 ** 2025) % 10 == 6 and pow(3, 2025, 10) == 3 and pow(7, 2025, 10) == 7
Q("010", T, "Unit digit", B, "What is the unit digit of 13²⁰²⁵ − 7²⁰²⁵?",
  "6", ["4", "0", "3"],
  "Unit digits of powers of 3 and 7 repeat every 4; 13²⁰²⁵ is the larger number, so borrow when needed",
  "2025 = 4 × 506 + 1, so 13²⁰²⁵ ends in 3 and 7²⁰²⁵ ends in 7. 13²⁰²⁵ is larger, so the difference ends in "
  "13 − 7 = 6 (borrowing 10).",
  ["Cycle of 3: 3, 9, 7, 1; of 7: 7, 9, 3, 1", "2025 leaves remainder 1 on division by 4", "Unit digits 3 and 7",
   "3 − 7 with a borrow: 13 − 7 = 6"],
  why="4 uses the third place of the cycles (7 − 3); 0 uses the second place (9 − 9); 3 is the unit digit of "
      "13²⁰²⁵ alone.", secs=45)

n_ = next(n for n in range(10000, 100000) if n % 7 == 0 and n % 11 == 0 and n % 13 == 0)
assert n_ == 10010 == 1001 * 10 and 10101 % 7 == 0 and 10101 % 13 == 0 and 10101 % 11 and 10001 % 1001
Q("010", T, "Divisibility", I, "What is the smallest five-digit number that is exactly divisible by 7, 11 and 13?",
  "10,010", ["10,001", "9,009", "10,101"],
  "A number divisible by 7, 11 and 13 is a multiple of their LCM, 7 × 11 × 13 = 1,001",
  "Multiples of 1,001: …, 9,009, 10,010, …. 9,009 has four digits, so the smallest five-digit multiple is "
  "10 × 1,001 = 10,010.",
  ["LCM(7, 11, 13) = 1,001", "9 × 1,001 = 9,009 (four digits)", "10 × 1,001 = 10,010"],
  why="10,001 = 73 × 137 is not a multiple of 1,001; 9,009 has only four digits; 10,101 = 1,001 × 10 + 91 is not a "
      "multiple of 1,001 (though it is divisible by 7 and 13).", secs=55)

cnt = [n for n in range(1, 1000) if n % 4 == 1 and n % 5 == 2]
assert len(cnt) == 50 and cnt[0] == 17 and cnt[-1] == 997
Q("010", T, "Remainders", A, "How many positive integers less than 1,000 leave a remainder of 1 when divided by 4 and "
  "a remainder of 2 when divided by 5?",
  "50", ["49", "200", "100"],
  "Find the smallest such number; the rest follow at intervals of LCM(4, 5) = 20",
  "Numbers leaving 2 on division by 5: 2, 7, 12, 17, … The first that leaves 1 on division by 4 is 17. So the "
  "numbers are 17, 37, 57, …, 997. Count = (997 − 17) ÷ 20 + 1 = 50.",
  ["Smallest: 17 (17 = 4 × 4 + 1 = 5 × 3 + 2)", "Step = LCM(4, 5) = 20", "Last below 1,000: 997",
   "(997 − 17) ÷ 20 + 1 = 50"],
  why="49 forgets to count the first term; 200 counts the numbers that satisfy only the remainder-2 condition; 100 "
      "divides 1,000 by 10 instead of 20.", secs=80)

# ================================================================ Percentage (009: B3 I3 A1; 010: B1 I2 A3)
T = "Percentage"
npa = F(48) * F(35, 1000) * 100
assert npa == 168
Q("009", T, "Basic percentage", B, "A bank's loan book is ₹48 crore, and 3.5% of it is classified as non-performing. "
  "How much is non-performing, in lakh rupees? (1 crore = 100 lakh)",
  "₹168 lakh", ["₹16.8 lakh", "₹1,680 lakh", "₹1.68 lakh"],
  "Find the percentage in crore, then convert: 1 crore = 100 lakh",
  "3.5% of ₹48 crore = 0.035 × 48 = ₹1.68 crore = 1.68 × 100 = ₹168 lakh.",
  ["3.5% of 48 = 1.68", "₹1.68 crore", "× 100 = ₹168 lakh"],
  why="₹16.8 lakh and ₹1,680 lakh use 10 and 1,000 lakh to a crore; ₹1.68 lakh is the answer in crore with the "
      "wrong unit.", secs=40)

pay = 50000 * F(90, 100) * F(30, 100)
assert pay == 13500 and 50000 * F(30, 100) == 15000 and 50000 * F(20, 100) == 10000
Q("009", T, "Income and expenditure", B, "Neha's monthly salary is ₹50,000. 10% of it is deducted for her provident "
  "fund. She spends 70% of the remaining (take-home) amount and saves the rest. How much does she save a month?",
  "₹13,500", ["₹15,000", "₹10,000", "₹31,500"],
  "Work on the take-home pay, not the gross salary",
  "Take-home = 90% of ₹50,000 = ₹45,000. She saves 30% of it: 0.3 × 45,000 = ₹13,500.",
  ["Take-home = ₹45,000", "Savings = 30% of take-home", "0.3 × 45,000 = ₹13,500"],
  why="₹15,000 takes 30% of the gross salary; ₹10,000 subtracts the 10% deduction from 30% (20% of ₹50,000); ₹31,500 "
      "is what she spends.", secs=40)

x_ = F(120) / (F(120, 100) * F(125, 100) - 1)
assert x_ == 240 and F(120) / F(45, 100) != 240
Q("009", T, "Successive change", B, "A number is increased by 20% and the result is then increased by 25%. The final "
  "value is 120 more than the original number. What is the original number?",
  "240", ["267", "200", "480"],
  "Successive increases multiply: 1.20 × 1.25 = 1.50",
  "After both increases the number is 1.2 × 1.25 = 1.5 times the original, that is 50% more. 50% of the number = "
  "120, so the number is 240.",
  ["1.2 × 1.25 = 1.5", "Increase = 50% of the number", "0.5 × N = 120 ⇒ N = 240"],
  why="267 adds the rates to 45%; 200 takes the increase as 60%; 480 takes it as 25%.", secs=40)

adults, kids = 12000 * F(60, 100), 12000 * F(40, 100)
new = adults * F(105, 100) + kids * F(90, 100)
assert new == 11880
Q("009", T, "Population and depreciation", I, "A village has 12,000 people, 60% of whom are adults. Over a year the "
  "number of adults rises by 5% and the number of children falls by 10%. What is the population at the end of the "
  "year?",
  "11,880", ["11,400", "11,520", "12,360"],
  "Apply each rate to its own group and add",
  "Adults: 7,200 × 1.05 = 7,560. Children: 4,800 × 0.90 = 4,320. Total = 7,560 + 4,320 = 11,880.",
  ["Adults 7,200, children 4,800", "7,200 × 1.05 = 7,560", "4,800 × 0.9 = 4,320", "Total 11,880"],
  why="11,400 applies a net −5% to everyone; 11,520 swaps the groups (takes adults as 40%); 12,360 forgets the "
      "fall in the number of children.",
  secs=55)

orig = F(16, 15) * F(90, 100) / F(120, 100)
assert orig == F(4, 5)
Q("009", T, "Basic percentage", I, "When the numerator of a fraction is increased by 20% and its denominator is "
  "decreased by 10%, the fraction becomes 16/15. What was the original fraction?",
  "4/5", ["8/9", "32/25", "24/25"],
  "The fraction is multiplied by 1.2 ÷ 0.9 = 4/3",
  "New fraction = original × 1.2/0.9 = original × 4/3. So original = 16/15 × 3/4 = 4/5.",
  ["Factor = 1.2 ÷ 0.9 = 4/3", "Original = 16/15 ÷ 4/3", "= 16/15 × 3/4 = 4/5"],
  why="8/9 undoes only the numerator change (÷ 1.2); 24/25 undoes only the denominator change (× 0.9); 32/25 "
      "multiplies by 1.2 instead of dividing.", secs=60)

sol = [x for x in range(1, 100) if (100 + x) * (100 + 2 * x) == 132 * 100]
assert sol == [10]
Q("009", T, "Successive change", I, "The price of an item is increased by x% and the new price is then increased by "
  "2x%. Overall the price rises by 32%. What is x?",
  "10", ["11", "12", "8"],
  "Write the two changes as factors: (1 + x/100)(1 + 2x/100) = 1.32",
  "Try x = 10: 1.10 × 1.20 = 1.32 ✓. (Algebraically 2x² + 300x − 3,200 = 0 gives x = 10, the positive root.)",
  ["(100 + x)(100 + 2x) = 13,200", "2x² + 300x − 3,200 = 0", "x = 10"],
  why="11 adds the rates (x + 2x = 33 ≈ 32); 12 gives 1.12 × 1.24 ≈ 1.389; 8 gives 1.08 × 1.16 ≈ 1.253.", secs=60)

orig = F(140800) / (1 - F(9, 10) * F(9, 10) * F(8, 10))
assert orig == 400000 and 140800 / F(40, 100) == 352000
Q("009", T, "Population and depreciation", A, "A machine depreciates by 10% a year in each of the first two years and "
  "by 20% in the third year, each time on its value at the start of that year. Its total loss in value over the three "
  "years is ₹1,40,800. What was its original value?",
  "₹4,00,000", ["₹3,52,000", "₹3,20,000", "₹4,40,000"],
  "Value after 3 years = original × 0.9 × 0.9 × 0.8; the loss is the rest",
  "0.9 × 0.9 × 0.8 = 0.648, so the machine loses 35.2% of its value. 35.2% of the original = ₹1,40,800, giving "
  "original = 1,40,800 ÷ 0.352 = ₹4,00,000.",
  ["Remaining factor = 0.9 × 0.9 × 0.8 = 0.648", "Loss = 1 − 0.648 = 35.2%", "1,40,800 ÷ 0.352 = ₹4,00,000"],
  why="₹3,52,000 adds the rates (40%); ₹3,20,000 takes the loss as 44%; ₹4,40,000 takes it as 32%.", secs=85)

sr = F(84, 60) * 100
assert sr == 140
Q("010", T, "Basic percentage", B, "A batter scores 84 runs off 60 balls. Her strike rate is the number of runs per "
  "100 balls. What is her strike rate?",
  "140", ["71.4", "124", "144"],
  "Strike rate = runs ÷ balls × 100",
  "84 ÷ 60 × 100 = 1.4 × 100 = 140.",
  ["84 ÷ 60 = 1.4", "× 100 = 140"],
  why="71.4 divides balls by runs; 124 adds 84 + 40 (the balls short of 100); 144 takes 84 ÷ 60 as 1.44.", secs=30)

basic = F(86400) / 12 / F(24, 100)
assert basic == 30000 and F(86400) / 12 / F(12, 100) == 60000
Q("010", T, "Income and expenditure", I, "Each month an employee puts 12% of her basic pay into her provident fund, "
  "and her employer adds an equal amount. In a year the total credited to her provident fund is ₹86,400. What is her "
  "monthly basic pay?",
  "₹30,000", ["₹60,000", "₹36,000", "₹3,60,000"],
  "Each month 12% + 12% = 24% of the basic pay is credited",
  "Monthly credit = 86,400 ÷ 12 = ₹7,200. This is 24% of the basic pay, so basic = 7,200 ÷ 0.24 = ₹30,000.",
  ["Monthly credit = ₹7,200", "= 24% of basic", "Basic = 7,200 ÷ 0.24 = ₹30,000"],
  why="₹60,000 ignores the employer's equal share (12% only); ₹36,000 divides the yearly total by 2.4; ₹3,60,000 is "
      "the yearly basic pay, not the monthly.", secs=55)

h_ = 25 * F(6, 5) ** 3
assert h_ == F(216, 5) and 25 * F(160, 100) == 40
Q("010", T, "Population and depreciation", I, "A sapling is 25 cm tall. Its height grows by 20% every month, each "
  "time on its height at the start of that month. How tall is it after 3 months?",
  "43.2 cm", ["40 cm", "36 cm", "51.84 cm"],
  "Growth compounds: height = 25 × 1.2³",
  "25 × 1.2 = 30, 30 × 1.2 = 36, 36 × 1.2 = 43.2 cm.",
  ["Month 1: 30 cm", "Month 2: 36 cm", "Month 3: 43.2 cm"],
  why="40 cm adds 20% of 25 three times (simple growth of 60%); 36 cm stops after 2 months; 51.84 cm runs for 4 "
      "months.", secs=50)

c_ = F(105, 125)
q_ = F(4) / (1 - c_)
assert c_ == F(84, 100) and q_ == 25
Q("010", T, "Successive change", A, "The price of cooking oil rises by 25%, and a family's spending on oil rises by "
  "only 5%. As a result the family now buys 4 litres less oil each month. How many litres did it buy each month "
  "before the price rise?",
  "25 litres", ["20 litres", "16 litres", "21 litres"],
  "Quantity = spending ÷ price, so the new quantity is 1.05 ÷ 1.25 = 0.84 of the old",
  "New quantity = 1.05/1.25 = 84% of the old, a fall of 16%. 16% of the old quantity = 4 litres, so the old "
  "quantity = 4 ÷ 0.16 = 25 litres.",
  ["Quantity factor = 1.05 ÷ 1.25 = 0.84", "Fall = 16%", "16% of Q = 4 ⇒ Q = 25 litres"],
  why="20 litres takes the fall as 20% (25 − 5); 16 litres is the 16% itself; 21 litres is the new quantity.",
  secs=75)

orig = F(364500) / F(9, 10) ** 3
assert orig == 500000 and orig * F(8, 10) ** 2 == 320000
Q("010", T, "Population and depreciation", A, "Two identical machines were bought at the same price. The first, bought "
  "3 years ago, depreciates by 10% a year and is now worth ₹3,64,500. The second, bought 2 years ago, depreciates by "
  "20% a year. What is the second machine worth now? (Each year's depreciation is on the value at the start of that "
  "year.)",
  "₹3,20,000", ["₹2,91,600", "₹3,00,000", "₹2,33,280"],
  "Find the common purchase price from the first machine, then depreciate it for the second",
  "Price = 3,64,500 ÷ 0.9³ = 3,64,500 ÷ 0.729 = ₹5,00,000. Second machine: 5,00,000 × 0.8² = ₹3,20,000.",
  ["0.9³ = 0.729", "Price = ₹5,00,000", "5,00,000 × 0.64 = ₹3,20,000"],
  why="₹2,91,600 applies 20% to ₹3,64,500 once; ₹3,00,000 uses simple depreciation (40% of ₹5,00,000); ₹2,33,280 "
      "depreciates ₹3,64,500 at 20% for 2 years.", secs=85)

S_ = next(s for s in range(50000, 500001, 100) if 6000 + 2500 + F(4, 100) * (s - 50000) == 4000 + F(6, 100) * (s - 20000))
assert S_ == 185000
Q("010", T, "Income and expenditure", A, "A salesman can choose between two pay plans. Plan P: ₹6,000 a month plus 5% "
  "commission on the first ₹50,000 of sales and 4% on sales above that. Plan Q: ₹4,000 a month plus 6% commission on "
  "sales above ₹20,000. At what monthly sales do the two plans pay the same?",
  "₹1,85,000", ["₹1,25,000", "₹3,20,000", "₹1,60,000"],
  "Write each plan's pay for sales S above ₹50,000 and equate",
  "Plan P: 6,000 + 2,500 + 0.04(S − 50,000) = 6,500 + 0.04S. Plan Q: 4,000 + 0.06(S − 20,000) = 2,800 + 0.06S. "
  "Equal when 0.02S = 3,700, that is S = ₹1,85,000. (Both pay ₹13,900.)",
  ["P = 6,500 + 0.04S", "Q = 2,800 + 0.06S", "0.02S = 3,700 ⇒ S = ₹1,85,000"],
  why="₹1,25,000 ignores Plan Q's ₹20,000 threshold (6,500 + 0.04S = 4,000 + 0.06S); ₹3,20,000 pays Plan P 5% on "
      "all sales; ₹1,60,000 pays Plan P 4% on all sales.",
  secs=95)


# ================================================================ Ratio and Proportion (009: B2 I3 A2; 010: B3 I3 A1)
T = "Ratio and Proportion"
part = F(2880, 16)
assert part * 2 == 360 and part * 7 == 1260 and part * 9 == 1620
Q("009", T, "Basic ratio", B, "₹2,880 is divided between Asha and Bina in the ratio 7 : 9. How much more does Bina get "
  "than Asha?",
  "₹360", ["₹1,260", "₹1,620", "₹180"],
  "Total parts = 7 + 9 = 16; the difference is 9 − 7 = 2 parts",
  "One part = 2,880 ÷ 16 = ₹180. Bina gets 2 parts more, that is ₹360.",
  ["7 + 9 = 16 parts", "1 part = ₹180", "Difference = 2 parts = ₹360"],
  why="₹1,260 and ₹1,620 are Asha's and Bina's shares; ₹180 is one part, not the two-part difference.", secs=35)

assert F(36000 + 6000, 48000 + 6000) == F(7, 9) and F(36000 + 12000, 48000 + 12000) == F(4, 5)
Q("009", T, "Coins and salary share", B, "A earns ₹36,000 a month and B earns ₹48,000. Each gets a raise of ₹6,000 "
  "a month. What is the new ratio of their salaries?",
  "7 : 9", ["3 : 4", "9 : 7", "4 : 5"],
  "Add the raise to each salary first; a ratio does not stay the same when equal amounts are added",
  "New salaries: ₹42,000 and ₹54,000. 42,000 : 54,000 = 7 : 9.",
  ["A: 36,000 + 6,000 = 42,000", "B: 48,000 + 6,000 = 54,000", "42 : 54 = 7 : 9"],
  why="3 : 4 is the old ratio; 9 : 7 reverses the new one; 4 : 5 adds ₹12,000 to each salary.", secs=35)

k_ = next(k for k in range(1, 50) if 9 * (3 * k + 8) == 7 * (4 * k + 8))
assert k_ == 16 and 3 * k_ + 4 * k_ - 8 == 104
Q("009", T, "Ages via ratio", I, "The present ages of A and B are in the ratio 3 : 4. Eight years from now the ratio "
  "will be 7 : 9. What was the sum of their ages 4 years ago?",
  "104 years", ["112 years", "120 years", "96 years"],
  "Let the ages be 3k and 4k and use the future ratio to find k",
  "9(3k + 8) = 7(4k + 8) gives 27k + 72 = 28k + 56, so k = 16. Ages now: 48 and 64, sum 112. Four years ago the sum "
  "was 112 − 8 = 104.",
  ["9(3k + 8) = 7(4k + 8)", "k = 16 ⇒ 48 and 64", "Sum now 112", "4 years ago: 112 − 2 × 4 = 104"],
  why="112 is the present sum; 120 is the sum 4 years from now; 96 is the sum 8 years ago.", secs=60)

r_ = F(11 + 3, 11 - 3)
assert r_ == F(7, 4) and F(49 + 16, 49 - 16) == F(65, 33)
Q("009", T, "Proportion", I, "If (a + b) : (a − b) = 11 : 3, what is (a² + b²) : (a² − b²)?",
  "65 : 33", ["11 : 3", "121 : 9", "33 : 65"],
  "Componendo and dividendo: a : b = (11 + 3) : (11 − 3)",
  "a : b = 14 : 8 = 7 : 4. Then a² + b² = 49 + 16 = 65 and a² − b² = 49 − 16 = 33 (in the same units), so the ratio "
  "is 65 : 33.",
  ["a : b = (11 + 3) : (11 − 3) = 7 : 4", "a² + b² = 65, a² − b² = 33", "Ratio = 65 : 33"],
  why="11 : 3 is the given ratio, not the one asked; 121 : 9 squares the given ratio; 33 : 65 is inverted.",
  secs=60)

S_ = F(300) / (F(4, 9) - F(5, 12))
assert S_ == 10800 and S_ * F(4, 9) == 4800 and S_ * F(5, 12) == 4500
Q("009", T, "Coins and salary share", I, "A sum of money was to be divided among A, B and C in the ratio 2 : 3 : 4, "
  "but by mistake it was divided in the ratio 3 : 4 : 5. As a result C got ₹300 less than his due share. What was "
  "the sum?",
  "₹10,800", ["₹3,600", "₹5,400", "₹7,200"],
  "C's due share is 4/9 of the sum and he got 5/12 of it",
  "4/9 − 5/12 = 16/36 − 15/36 = 1/36 of the sum = ₹300, so the sum = ₹10,800. Check: 4/9 of 10,800 = 4,800 and "
  "5/12 of 10,800 = 4,500.",
  ["Due: 4/9; received: 5/12", "4/9 − 5/12 = 1/36", "Sum = 300 × 36 = ₹10,800"],
  why="₹3,600, ₹5,400 and ₹7,200 multiply ₹300 by 12, 18 and 24 instead of 36 (they use only one of the "
      "denominators).", secs=70)

for a_, b_, c_ in [(1, 1, 1), (2, 2, 2), (1, 2, -3), (4, -1, -3)]:
    k_ = F(a_, b_ + c_)
    assert k_ == F(b_, c_ + a_) == F(c_, a_ + b_) and k_ in (F(1, 2), -1)
Q("009", T, "Basic ratio", A, "If a/(b + c) = b/(c + a) = c/(a + b) = k, where the denominators are not zero, what "
  "are the possible values of k?",
  "½ or −1", ["½ only", "−1 only", "2 or −1"],
  "Add numerators and denominators of equal ratios, but watch the case a + b + c = 0",
  "If a + b + c ≠ 0, adding gives k = (a + b + c)/(2(a + b + c)) = ½. If a + b + c = 0, then b + c = −a, so "
  "k = a/(−a) = −1. Example: a = 1, b = 2, c = −3 gives each ratio −1.",
  ["Case a + b + c ≠ 0: k = ½", "Case a + b + c = 0: b + c = −a ⇒ k = −1", "Both cases occur"],
  why="½ only misses the case a + b + c = 0 (for example 1, 2, −3); −1 only misses a = b = c; 2 inverts ½.",
  secs=85)

k_ = F(42 - 24, 3)
n_max = max(n for n in range(0, 200) if (42 / k_) ** 2 > n)
assert k_ == 6 and n_max == 48
Q("009", T, "Proportion", A, "An engine alone runs at 42 km/h. When it pulls wagons, its speed falls by an amount "
  "that varies as the square root of the number of wagons. With 9 wagons its speed is 24 km/h. What is the largest "
  "number of wagons it can pull and still move?",
  "48", ["49", "36", "7"],
  "Fall in speed = k√n; the engine moves only while 42 − k√n > 0",
  "With 9 wagons the fall is 42 − 24 = 18 = k × 3, so k = 6. The engine moves while 6√n < 42, that is √n < 7, "
  "n < 49. The largest whole number of wagons is 48.",
  ["Fall = 18 = k√9 ⇒ k = 6", "6√n < 42 ⇒ √n < 7", "n < 49 ⇒ at most 48 wagons"],
  why="With 49 wagons the speed is exactly 0, so it cannot move; 36 uses k = 7; 7 is the limit for √n, not n.",
  secs=85)

assert F(84, 12) * 5 == 35 and F(84, 12) * 4 == 28
Q("010", T, "Basic ratio", B, "The sides of a triangle are in the ratio 3 : 4 : 5 and its perimeter is 84 cm. How "
  "long is the longest side?",
  "35 cm", ["28 cm", "21 cm", "42 cm"],
  "The perimeter is the sum of the three sides: 3 + 4 + 5 = 12 parts",
  "One part = 84 ÷ 12 = 7 cm. The longest side = 5 × 7 = 35 cm.",
  ["12 parts = 84 cm", "1 part = 7 cm", "5 parts = 35 cm"],
  why="28 cm and 21 cm are the other two sides; 42 cm takes half the perimeter.", secs=30)

x_ = F(15 * 36, 27)
assert x_ == 20
Q("010", T, "Proportion", B, "If x : 15 :: 36 : 27, what is the value of x?",
  "20", ["11.25", "24", "48"],
  "In a proportion, product of extremes = product of means: x × 27 = 15 × 36",
  "x = 15 × 36 ÷ 27 = 540 ÷ 27 = 20.",
  ["x × 27 = 15 × 36", "x = 540 ÷ 27", "x = 20"],
  why="11.25 computes 15 × 27 ÷ 36; 24 adds 36 − 27 = 9 to 15; 48 computes 36 × 36 ÷ 27.", secs=35)

b_ = F(15000) / (1 - F(3, 5))
assert b_ == 37500 and b_ * F(3, 5) == 22500
Q("010", T, "Coins and salary share", B, "A's monthly salary is three-fifths of B's, and B earns ₹15,000 more than A. "
  "What is A's monthly salary?",
  "₹22,500", ["₹37,500", "₹9,000", "₹25,000"],
  "The ₹15,000 gap is 2/5 of B's salary",
  "B − A = B − 3B/5 = 2B/5 = ₹15,000, so B = ₹37,500 and A = 3/5 × 37,500 = ₹22,500.",
  ["B − 3B/5 = 2B/5", "2B/5 = 15,000 ⇒ B = 37,500", "A = 22,500"],
  why="₹37,500 is B's salary; ₹9,000 is 3/5 of ₹15,000; ₹25,000 takes the gap as 3/5 of B's salary.", secs=40)

k_ = next(k for k in range(1, 50) if 5 * k - 3 == 3 * (2 * k - 3))
assert k_ == 6 and 5 * k_ - 2 * k_ == 18
Q("010", T, "Ages via ratio", I, "The present ages of a teacher and a student are in the ratio 5 : 2. Three years ago "
  "the ratio was 3 : 1. How old was the teacher when the student was born?",
  "18 years", ["30 years", "12 years", "27 years"],
  "Let the ages be 5k and 2k; the teacher's age at the student's birth is the age gap 3k",
  "(5k − 3) = 3(2k − 3) gives 5k − 3 = 6k − 9, so k = 6. Ages: teacher 30, student 12. The gap, 18 years, was the "
  "teacher's age when the student was born.",
  ["5k − 3 = 3(2k − 3)", "k = 6 ⇒ 30 and 12", "Gap = 30 − 12 = 18"],
  why="30 and 12 are the present ages; 27 is the teacher's age three years ago.", secs=60)

v_ = F(7 * 3 - 2 * 5, 3 * 3 + 4 * 5)
assert v_ == F(11, 29) and F(7 * 5 - 2 * 3, 3 * 5 + 4 * 3) == F(29, 27)
Q("010", T, "Proportion", I, "If a : b = 3 : 5, what is (7a − 2b) : (3a + 4b)?",
  "11 : 29", ["29 : 27", "29 : 11", "21 : 29"],
  "Put a = 3k and b = 5k; k cancels",
  "7a − 2b = 21k − 10k = 11k and 3a + 4b = 9k + 20k = 29k. The ratio is 11 : 29.",
  ["a = 3k, b = 5k", "7a − 2b = 11k", "3a + 4b = 29k", "11 : 29"],
  why="29 : 27 swaps a and b (a = 5, b = 3); 29 : 11 inverts the answer; 21 : 29 drops the − 2b.", secs=50)

k_ = F(140, 15 - 8)
assert k_ == 20 and 6 * k_ * 1 + 4 * k_ * 2 + 3 * k_ * 5 == 580
Q("010", T, "Coins and salary share", I, "A piggy bank holds ₹1, ₹2 and ₹5 coins whose numbers are in the ratio "
  "6 : 4 : 3. The ₹5 coins are worth ₹140 more than the ₹2 coins. What is the total value of the coins?",
  "₹580", ["₹460", "₹290", "₹1,160"],
  "Take the numbers as 6k, 4k and 3k; their values are 6k, 8k and 15k rupees",
  "15k − 8k = 7k = 140, so k = 20. Values: ₹120 + ₹160 + ₹300 = ₹580.",
  ["Values: 6k, 8k, 15k", "7k = 140 ⇒ k = 20", "120 + 160 + 300 = ₹580"],
  why="₹460 leaves out the ₹1 coins; ₹290 and ₹1,160 use k = 10 and k = 40.", secs=60)

k_ = next(k for k in range(1, 50) if 2 * (2 * k + 6) == 7 * k - 6)
tot = 9 * k_
assert k_ == 6 and tot == 54 and tot // 2 - (2 * k_ + 6) == 9
Q("010", T, "Basic ratio", A, "In an office the ratio of officers to clerks is 2 : 7. After 6 clerks are promoted to "
  "officers (no one joins or leaves), the ratio becomes 1 : 2. How many more clerks must now be promoted to make the "
  "numbers of officers and clerks equal?",
  "9", ["15", "27", "6"],
  "Promotions move people between the groups; the total stays the same",
  "Let the numbers be 2k and 7k. (2k + 6) : (7k − 6) = 1 : 2 gives 4k + 12 = 7k − 6, so k = 6: 12 officers and 42 "
  "clerks, 54 in all. Now there are 18 officers and 36 clerks. Equal numbers means 27 each, so 9 more promotions.",
  ["2(2k + 6) = 7k − 6 ⇒ k = 6", "Total = 54", "Now 18 officers, 36 clerks", "27 each ⇒ 9 more"],
  why="15 counts from the original 12 officers; 27 is the number in each group at the end; 6 repeats the first "
      "promotion.", secs=85)

# ================================================================ Problems on Ages (009: B1 I2 A1; 010: B2 I2 A1)
T = "Problems on Ages"
r_ = F(63 - 27, 2)
assert r_ == 18
Q("009", T, "Present and future ages", B, "Riya was born when her mother was 27 years old. The sum of their present "
  "ages is 63 years. How old is Riya?",
  "18 years", ["45 years", "21 years", "36 years"],
  "The mother is always 27 years older: mother = Riya + 27",
  "Riya + (Riya + 27) = 63, so 2 × Riya = 36 and Riya = 18. Her mother is 45.",
  ["Mother = R + 27", "2R + 27 = 63", "R = 18"],
  why="45 is the mother's age; 21 divides 63 by 3; 36 is 63 − 27, which is twice Riya's age.", secs=35)

sol = [(a, b) for a in range(4, 100) for b in range(4, 100) if a - 3 == 2 * (b - 3) and 2 * (a + 7) == 3 * (b + 7)]
assert sol == [(23, 13)]
Q("009", T, "Present and future ages", I, "Three years ago A was twice as old as B. Seven years from now A will be "
  "1.5 times as old as B. What is the sum of their present ages?",
  "36 years", ["30 years", "50 years", "33 years"],
  "Write both conditions in terms of the present ages a and b",
  "a − 3 = 2(b − 3) gives a = 2b − 3. a + 7 = 1.5(b + 7) gives 2b + 4 = 1.5b + 10.5, so b = 13 and a = 23. Sum = "
  "36.",
  ["a = 2b − 3", "2b + 4 = 1.5b + 10.5", "b = 13, a = 23", "Sum = 36"],
  why="30 is the sum three years ago; 50 is the sum seven years from now; 33 takes A as 20.", secs=60)

k_ = F(65, 15 - 2)
assert k_ == 5 and F(75 + 5, 10 + 5) == F(16, 3)
Q("009", T, "Ratio-based ages", I, "The ages of a grandfather and his grandson are in the ratio 15 : 2, and the "
  "grandfather is 65 years older. What will be the ratio of their ages 5 years from now?",
  "16 : 3", ["15 : 2", "17 : 4", "3 : 16"],
  "The age gap of 65 years equals 15 − 2 = 13 parts",
  "13 parts = 65, so 1 part = 5: grandfather 75, grandson 10. In 5 years: 80 and 15, ratio 16 : 3.",
  ["13 parts = 65 years", "Ages: 75 and 10", "After 5 years: 80 : 15 = 16 : 3"],
  why="15 : 2 is the present ratio; 17 : 4 is the ratio 10 years from now (85 : 20); 3 : 16 is inverted.", secs=55)

sol = [(a, b) for a in range(5, 60) for b in range(5, a + 1) if a * b == 240 and (a - 4) * (b - 4) == 132]
assert sol == [(16, 15)] and 20 * 12 == 240 and 16 * 8 != 132
Q("009", T, "Present and future ages", A, "The product of the present ages of two brothers is 240. Four years ago the "
  "product of their ages was 132. How old is the elder brother?",
  "16 years", ["15 years", "20 years", "12 years"],
  "Expand (a − 4)(b − 4) = ab − 4(a + b) + 16 to find the sum of the ages",
  "240 − 4(a + b) + 16 = 132, so a + b = 31. Two numbers with sum 31 and product 240 are 16 and 15. The elder is 16.",
  ["(a − 4)(b − 4) = ab − 4(a + b) + 16", "256 − 4(a + b) = 132 ⇒ a + b = 31", "t² − 31t + 240 = 0 ⇒ 16, 15"],
  why="15 is the younger brother; 20 and 12 multiply to 240 but four years ago they give 16 × 8 = 128, not 132.",
  secs=80)

k_ = next(k for k in range(16, 100) if k + 5 == 3 * (k - 15))
assert k_ == 25
Q("010", T, "Present and future ages", B, "Five years from now, Kabir will be three times as old as he was 15 years "
  "ago. How old is Kabir now?",
  "25 years", ["20 years", "30 years", "35 years"],
  "Form one equation in Kabir's present age",
  "k + 5 = 3(k − 15) gives k + 5 = 3k − 45, so 2k = 50 and k = 25.",
  ["k + 5 = 3(k − 15)", "2k = 50", "k = 25"],
  why="20 is (5 + 15) alone; 30 is his age 5 years from now; 35 solves k + 5 = 3k − 45 as 2k = 70.", secs=40)

k_ = 4
assert 6 * k_ - 5 * k_ == 4 and 5 * k_ + 7 == 27
Q("010", T, "Ratio-based ages", B, "The present ages of P and Q are in the ratio 5 : 6, and Q is 4 years older than P. "
  "How old will P be 7 years from now?",
  "27 years", ["20 years", "31 years", "24 years"],
  "The age gap of 4 years is 6 − 5 = 1 part",
  "1 part = 4 years, so P = 5 × 4 = 20 and Q = 24. Seven years from now P will be 27.",
  ["1 part = 4 years", "P = 20, Q = 24", "P + 7 = 27"],
  why="20 is P's present age; 31 is Q's age 7 years from now; 24 is Q's present age.", secs=35)

sol = [(s, d) for s in range(13, 100) for d in range(13, 60) if s - 12 == 4 * (d - 12) and s + d + 12 == 76]
assert sol == [(44, 20)]
Q("010", T, "Present and future ages", I, "Twelve years ago, Sita was four times as old as her daughter. Six years "
  "from now, their ages will add up to 76 years. What is Sita's present age?",
  "44 years", ["20 years", "50 years", "32 years"],
  "Six years from now both are 6 years older, so the present sum is 76 − 12 = 64",
  "s + d = 64 and s − 12 = 4(d − 12), so s = 4d − 36. Then 5d − 36 = 64, d = 20 and s = 44.",
  ["Present sum = 76 − 12 = 64", "s = 4d − 36", "5d = 100 ⇒ d = 20", "s = 44"],
  why="20 is the daughter's age; 50 is Sita's age six years from now; 32 is her age twelve years ago.", secs=60)

k_ = F(8, 7 - 5)
assert k_ == 4 and 5 * k_ - 6 == 14
Q("010", T, "Ratio-based ages", I, "Six years from now the ages of X and Y will be in the ratio 7 : 5. X is 8 years "
  "older than Y. What is Y's present age?",
  "14 years", ["20 years", "22 years", "28 years"],
  "The age gap does not change: 7 − 5 = 2 parts = 8 years",
  "1 part = 4 years, so in six years X = 28 and Y = 20. Y's present age = 20 − 6 = 14.",
  ["2 parts = 8 years ⇒ 1 part = 4", "Y in 6 years = 20", "Y now = 14"],
  why="20 is Y's age six years from now; 22 is X's present age; 28 is X's age six years from now.", secs=55)

sol = [y for y in range(1900, 2027) if 2026 - y == sum(int(c) for c in str(y))]
assert sol == [2021]
Q("010", T, "Present and future ages", A, "In 2026, a child's age (in completed years) equals the sum of the digits of "
  "the year in which the child was born. How old is the child in 2026?",
  "5 years", ["7 years", "6 years", "4 years"],
  "If the child was born in 20ab, the age is 26 − 10a − b and the digit sum is 2 + a + b",
  "For a birth year 20ab: 26 − 10a − b = 2 + a + b, so 11a + 2b = 24. The only digits that work are a = 2, b = 1: "
  "born in 2021, age 5 = 2 + 0 + 2 + 1. (A birth year in the 1900s would need 11a + 2b = 116, which no digits "
  "satisfy.)",
  ["Born 20ab ⇒ age 26 − 10a − b", "Digit sum 2 + a + b", "11a + 2b = 24 ⇒ a = 2, b = 1", "Born 2021, age 5"],
  why="A child aged 7, 6 or 4 would be born in 2019, 2020 or 2022, with digit sums 12, 4 and 6, which do not match.",
  secs=90)

# ================================================================ Average (009: B1 I1 A1; 010: B1 I3 A2)
T = "Average"
assert F(sum(range(1, 50, 2)), 25) == 25
Q("009", T, "Simple average", B, "What is the average of the first 25 odd numbers (1, 3, 5, …, 49)?",
  "25", ["26", "24.5", "50"],
  "The sum of the first n odd numbers is n², so their average is n",
  "Sum = 25² = 625, and 625 ÷ 25 = 25. (Also: average = (first + last)/2 = (1 + 49)/2 = 25.)",
  ["Sum of first 25 odd numbers = 625", "625 ÷ 25 = 25"],
  why="26 takes the last number as 51; 24.5 averages 1 to 48; 50 adds the first and last numbers without halving.",
  secs=30)

assert 7 * 4 == 28
Q("009", T, "Replacement", I, "The average age of a 7-member committee today is the same as it was 4 years ago, because "
  "one old member has been replaced by a younger one. How much younger is the new member than the member replaced?",
  "28 years", ["4 years", "7 years", "32 years"],
  "In 4 years the total age of 7 people rises by 7 × 4 = 28; the replacement must cancel this",
  "Without the change the total would have grown by 28 years. For the average to stay the same, the new member must "
  "be 28 years younger than the member replaced.",
  ["Rise in total over 4 years = 7 × 4 = 28", "Average unchanged ⇒ total unchanged", "Age difference = 28 years"],
  why="4 years is the time gap; 7 is the committee size; 32 adds the 4 years again.", secs=55)

sol = [(n, x) for n in range(2, 200) for x in range(1, n + 1)
       if F(n * (n + 1) // 2 - x, n - 1) == F(602, 17)]
assert sol == [(69, 7)]
Q("009", T, "Simple average", A, "The numbers 1, 2, 3, …, n are written on a board and one of them is erased. The "
  "average of the remaining numbers is 35 7/17. Which number was erased?",
  "7", ["8", "17", "35"],
  "The average of the rest is close to n/2, and n − 1 must be a multiple of 17",
  "The average 602/17 needs n − 1 to be a multiple of 17, and n is about 2 × 35 = 70, so n − 1 = 68 and n = 69. Sum "
  "of 1 to 69 = 2,415. Remaining sum = 68 × 602/17 = 2,408, so the erased number is 2,415 − 2,408 = 7.",
  ["Average ≈ n/2 ⇒ n ≈ 70", "n − 1 multiple of 17 ⇒ n = 69", "Sum 1 to 69 = 2,415", "68 × 602/17 = 2,408 ⇒ 7"],
  why="Erasing 8, 17 or 35 leaves totals of 2,407, 2,398 or 2,380; only erasing 7 leaves 2,408.",
  secs=100)

x_ = 22 * 5 - (12 + 18 + 25 + 30)
assert x_ == 25
Q("010", T, "Simple average", B, "The average of 12, 18, 25, x and 30 is 22. What is x?",
  "25", ["22", "30", "20"],
  "Total = average × count",
  "Total = 22 × 5 = 110. The four known numbers add up to 85, so x = 110 − 85 = 25.",
  ["Total = 110", "Known sum = 85", "x = 25"],
  why="22 is the average itself; 30 takes the total as 115; 20 takes the known sum as 90.", secs=30)

m_ = F(4, F(9, 8) - 1)
assert m_ == 32 and m_ * F(9, 8) == 36
Q("010", T, "Simple average", I, "The average temperature from Monday to Thursday was 36°C and from Tuesday to Friday "
  "was 37°C. Friday's temperature was 9/8 of Monday's. What was Friday's temperature?",
  "36°C", ["32°C", "40°C", "37°C"],
  "The two four-day totals differ only by Friday − Monday",
  "Friday − Monday = 4 × 37 − 4 × 36 = 4°C. With F = 9M/8, F − M = M/8 = 4, so M = 32°C and F = 36°C.",
  ["F − M = 148 − 144 = 4", "F = 9M/8 ⇒ M/8 = 4", "M = 32, F = 36"],
  why="32°C is Monday's temperature; 40°C takes F − M as 8; 37°C is an average, not Friday's reading.", secs=60)

w_ = next(w for w in range(0, 41) if 36 * (40 - w) + 26 * w == 32 * 40)
assert w_ == 16
Q("010", T, "Weighted average", I, "The average age of the 40 employees of a branch is 32 years. The average age of "
  "the men is 36 and that of the women is 26. How many women work there?",
  "16", ["24", "20", "12"],
  "Weighted average (alligation): men : women = (32 − 26) : (36 − 32)",
  "Men : women = 6 : 4 = 3 : 2. So women = 2/5 × 40 = 16. Check: (24 × 36 + 16 × 26) ÷ 40 = 32.",
  ["Men : women = 6 : 4", "Women = 2/5 of 40", "= 16"],
  why="24 is the number of men; 20 assumes equal groups; 12 uses the ratio 7 : 3.", secs=55)

n_ = F(34 - 22, F(3, 2))
assert n_ == 8
Q("010", T, "Replacement", I, "When a 34-year-old member of a team retires and is replaced by a 22-year-old, the "
  "average age of the team falls by 1.5 years. How many members does the team have?",
  "8", ["12", "18", "6"],
  "The total falls by 34 − 22 = 12 years, spread over all the members",
  "Fall in total = 12 years = team size × 1.5. Team size = 12 ÷ 1.5 = 8.",
  ["Fall in total = 34 − 22 = 12", "Fall in average = 1.5", "Size = 12 ÷ 1.5 = 8"],
  why="12 is the fall in the total; 18 multiplies 12 by 1.5; 6 divides 12 by 2.", secs=50)

sol = [(n, F(24 * n) - 25 * (n - 1)) for n in range(2, 200) if F(24 * n - 64, n - 1) == 22]
assert sol == [(21, 4)]
Q("010", T, "Simple average", A, "The average of some numbers is 24. If the largest of them, 64, is removed, the "
  "average becomes 22. If instead only the smallest number is removed, the average becomes 25. What is the smallest "
  "number?",
  "4", ["5", "24", "9"],
  "First find how many numbers there are from the first removal",
  "24n − 64 = 22(n − 1) gives 2n = 42, so n = 21 and the total is 504. Removing the smallest: 504 − s = 25 × 20 = "
  "500, so s = 4.",
  ["24n − 64 = 22(n − 1) ⇒ n = 21", "Total = 504", "504 − s = 500 ⇒ s = 4"],
  why="5 takes 20 numbers in all (480 − 25 × 19); 24 is the average itself; 9 takes the total as 509.",
  secs=85)

D_ = 4 * 62 - 3 * 60
E_ = D_ + 3
A_ = 3 * 60 - (4 * 61 - D_ - E_)
assert (D_, E_, A_) == (68, 71, 75)
Q("010", T, "Replacement", A, "The average weight of A, B and C is 60 kg. When D joins them, the average becomes "
  "62 kg. Then E, who is 3 kg heavier than D, replaces A, and the average weight of B, C, D and E becomes 61 kg. What "
  "is A's weight?",
  "75 kg", ["65 kg", "71 kg", "68 kg"],
  "Work with totals: A + B + C, then D, then B + C",
  "A + B + C = 180 and A + B + C + D = 248, so D = 68 kg and E = 71 kg. B + C + D + E = 244, so B + C = 244 − 139 = "
  "105. A = 180 − 105 = 75 kg.",
  ["A + B + C = 180", "D = 248 − 180 = 68, E = 71", "B + C = 244 − 139 = 105", "A = 180 − 105 = 75"],
  why="65 kg takes E as 3 kg lighter than D; 71 kg and 68 kg are E's and D's weights.", secs=85)


# ================================================================ Profit and Loss (009: B2 I3 A3; 010: B1 I1 A1)
T = "Profit and Loss"
cp, sp = F(30, 12), F(30, 10)
assert (sp - cp) / cp == F(1, 5) and (sp - cp) / sp == F(1, 6)
Q("009", T, "Cost and selling price", B, "A vendor buys bananas at 12 for ₹30 and sells them at 10 for ₹30. What is "
  "his profit percentage?",
  "20%", ["16⅔%", "25%", "10%"],
  "Compare the cost and the selling price of one banana",
  "Cost of one banana = 30 ÷ 12 = ₹2.50; selling price = 30 ÷ 10 = ₹3. Profit = ₹0.50 on ₹2.50 = 20%.",
  ["CP = ₹2.50 each", "SP = ₹3 each", "Profit = 0.50 ÷ 2.50 = 20%"],
  why="16⅔% divides the profit by the selling price; 25% divides 0.50 by 2; 10% takes the gap of 2 bananas out of "
      "20.", secs=40)

cp = F(540) / F(30, 100)
assert cp == 1800 and cp * F(13, 10) == 2340 and F(540) / F(30, 100) * F(7, 10) == 1260
Q("009", T, "Marked price", B, "A shopkeeper marks a heater 30% above its cost price. Selling it at the marked price "
  "gives him a profit of ₹540. What is the cost price?",
  "₹1,800", ["₹2,340", "₹1,260", "₹2,160"],
  "At the marked price the profit is the full 30% of the cost price",
  "30% of CP = ₹540, so CP = 540 ÷ 0.3 = ₹1,800 (and the marked price is ₹2,340).",
  ["Profit = 30% of CP", "0.3 × CP = 540", "CP = ₹1,800"],
  why="₹2,340 is the marked price; ₹1,260 takes ₹540 as 30% of the marked price; ₹2,160 is 1,800 × 1.2.", secs=35)

g_ = F(104, 96) - 1
assert g_ == F(1, 12)
Q("009", T, "Dishonest dealer", I, "A cloth seller's metre rod is 4 cm short. He sells cloth at 4% above the cost "
  "price per metre, measuring with this rod. What is his actual gain percentage?",
  "8⅓%", ["8%", "4%", "4⅙%"],
  "He charges for 100 cm (at 1.04 × cost) but gives only 96 cm",
  "For each 'metre' he receives 1.04 × the cost of 100 cm while giving cloth costing 0.96 of that. Gain = 1.04 ÷ "
  "0.96 − 1 = 1/12 = 8⅓%.",
  ["Received: 1.04 × cost of 1 m", "Given: 96 cm = 0.96 × cost of 1 m", "1.04 ÷ 0.96 = 13/12 ⇒ 8⅓%"],
  why="8% simply adds 4% + 4%; 4% counts only the markup; 4⅙% counts only the short rod (4 ÷ 96).", secs=55)

net = -100 + 120 - 108 + F(1188, 10)
assert net == F(308, 10)
Q("009", T, "Successive transactions", I, "Ravi buys a used phone and sells it at a 20% profit. Later he buys it back "
  "at 10% less than he sold it for, and then sells it again at a 10% profit on the buy-back price. What is his "
  "overall profit as a percentage of the original cost?",
  "30.8%", ["18.8%", "32%", "30%"],
  "Track every rupee paid and received, starting from a cost of 100",
  "Cost 100. Sells for 120. Buys back for 90% of 120 = 108. Sells for 110% of 108 = 118.8. Net = −100 + 120 − 108 "
  "+ 118.8 = 30.8, a profit of 30.8% on the original cost.",
  ["Pays 100, receives 120", "Pays 108 (buy-back)", "Receives 118.8", "Net = 30.8 ⇒ 30.8%"],
  why="18.8% compares only the last sale with the original cost; 32% compounds 20% and 10%; 30% adds 20% and 10%.",
  secs=65)

c_ = F(1260 + 2 * 960, 3)
assert c_ == 1060 and 1260 - c_ == 2 * (c_ - 960)
Q("009", T, "Cost and selling price", I, "The profit made by selling an article for ₹1,260 is twice the loss made by "
  "selling it for ₹960. What is its cost price?",
  "₹1,060", ["₹1,110", "₹1,160", "₹1,080"],
  "Profit = 1,260 − CP and loss = CP − 960",
  "1,260 − C = 2(C − 960) gives 1,260 + 1,920 = 3C, so C = ₹1,060. Check: profit 200, loss 100.",
  ["1,260 − C = 2(C − 960)", "3C = 3,180", "C = ₹1,060"],
  why="₹1,110 makes the profit equal to the loss; ₹1,160 makes the loss twice the profit; ₹1,080 gives a profit of "
      "180 and a loss of 120.", secs=55)

sol = [x for x in range(1, 100) if (100 + x) * (200 - x) == 22100]
assert sol == [30, 70] and F(12, 10) * F(9, 10) == F(108, 100)
Q("009", T, "Marked price", A, "A trader marks his goods x% above cost and then allows a discount of (x/2)% on the "
  "marked price, making a profit of 10.5%. If the markup is less than 50%, what is x?",
  "30", ["70", "21", "20"],
  "(1 + x/100)(1 − x/200) = 1.105",
  "Try x = 30: 1.30 × 0.85 = 1.105 ✓. The equation x² − 100x + 2,100 = 0 has roots 30 and 70; since the markup is "
  "below 50%, x = 30.",
  ["(100 + x)(200 − x) = 22,100", "x² − 100x + 2,100 = 0", "x = 30 or 70 ⇒ x = 30"],
  why="70 also satisfies the equation but breaks the condition that the markup is below 50%; 21 doubles 10.5; 20 "
      "gives 1.2 × 0.9 = 1.08, only 8% profit.", secs=85)

g_ = F(108, 100) / (F(9, 10) * F(8, 10)) - 1
assert g_ == F(1, 2) and F(108, 80) - 1 == F(35, 100) and F(108, 90) - 1 == F(1, 5)
Q("009", T, "Dishonest dealer", A, "A grocer mixes 1 kg of stones into every 9 kg of lentils. He uses an 800 g weight "
  "in place of 1 kg and charges 8% above the cost price of lentils. What is his actual gain percentage?",
  "50%", ["38%", "35%", "20%"],
  "The customer pays for 1 kg of lentils but receives 800 g of mixture, of which 90% is lentils",
  "Lentils given per 'kg' sold = 0.8 × 0.9 = 0.72 kg. Money received = 1.08 × cost of 1 kg. Gain = 1.08 ÷ 0.72 − 1 "
  "= 0.5 = 50%.",
  ["Mixture given = 800 g", "Lentils in it = 90% ⇒ 720 g", "1.08 ÷ 0.72 = 1.5 ⇒ 50%"],
  why="38% adds 8% + 10% + 20%; 35% ignores the stones (1.08 ÷ 0.8); 20% ignores the short weight (1.08 ÷ 0.9).",
  secs=85)

r_ = F(15, 12) * F(95, 100) - 1
assert r_ == F(3, 16)
Q("009", T, "Cost and selling price", A, "A trader sells 12 articles for the price at which he bought 15. Out of the "
  "sale money he pays a commission of 5% to an agent. What is his net profit percentage?",
  "18.75%", ["25%", "20%", "31.25%"],
  "SP of one article = 15/12 of its CP; the commission takes 5% of the SP",
  "SP = 1.25 × CP. After commission he keeps 95% of SP = 1.25 × 0.95 = 1.1875 × CP, a profit of 18.75%.",
  ["SP : CP = 15 : 12 = 1.25", "Kept = 0.95 × 1.25 = 1.1875", "Profit = 18.75%"],
  why="25% ignores the commission; 20% subtracts 5 percentage points from 25%; 31.25% adds the commission instead of "
      "deducting it.", secs=80)

assert 3600 * F(85, 100) == 3060 and 3600 * F(115, 100) == 4140
Q("010", T, "Cost and selling price", B, "A bicycle bought for ₹3,600 is sold at a loss of 15%. What is the selling "
  "price?",
  "₹3,060", ["₹4,140", "₹540", "₹3,130"],
  "Selling price = 85% of the cost price",
  "Loss = 15% of 3,600 = ₹540, so SP = 3,600 − 540 = ₹3,060.",
  ["Loss = 0.15 × 3,600 = ₹540", "SP = 3,600 − 540 = ₹3,060"],
  why="₹4,140 adds 15%; ₹540 is the loss itself; ₹3,130 divides 3,600 by 1.15.", secs=30)

c_ = F(96, F(12, 100))
assert c_ == 800 and c_ * F(132, 100) == 1056
Q("010", T, "Marked price", I, "Selling an article at its marked price gives a profit of 32%. Selling it at a discount "
  "of ₹96 on the marked price gives a profit of 20%. What is the marked price?",
  "₹1,056", ["₹800", "₹960", "₹1,200"],
  "The ₹96 discount equals the drop in profit, 32% − 20% = 12% of the cost price",
  "12% of CP = ₹96, so CP = ₹800. Marked price = 1.32 × 800 = ₹1,056.",
  ["32% − 20% = 12% of CP", "CP = 96 ÷ 0.12 = ₹800", "MP = 1.32 × 800 = ₹1,056"],
  why="₹800 is the cost price; ₹960 is the selling price after the discount; ₹1,200 takes ₹96 as 8% of the marked "
      "price.", secs=55)

a_, b_ = F(12, 10) * F(9, 10), F(13, 10) * F(85, 100)
assert a_ == F(108, 100) and b_ == F(1105, 1000) and b_ - a_ == F(25, 1000)
Q("010", T, "Marked price", A, "Two shopkeepers buy the same item at the same cost. A marks it 20% above cost and "
  "allows a 10% discount; B marks it 30% above cost and allows a 15% discount. Which of them makes the larger "
  "profit, and by how much?",
  "B, by 2.5% of the cost price", ["A, by 2.5% of the cost price", "B, by 5% of the cost price",
                                   "Both make the same profit"],
  "Selling price = cost × (1 + markup) × (1 − discount)",
  "A: 1.2 × 0.9 = 1.08, an 8% profit. B: 1.3 × 0.85 = 1.105, a 10.5% profit. B earns 2.5% of the cost price more.",
  ["A: 1.20 × 0.90 = 1.080", "B: 1.30 × 0.85 = 1.105", "Difference = 0.025 of CP"],
  why="A earns less, not more; 5% subtracts the rates ((30 − 15) − (20 − 10)); the profits are 8% and 10.5%, not "
      "equal.", secs=75)

# ================================================================ Discount (009: B1 I2 A1; 010: B1 I1 A2)
T = "Discount"
v = 1250 * F(84, 100) * F(112, 100)
assert v == 1176 and 1250 * F(84, 100) == 1050 and 1250 * F(112, 100) == 1400
Q("009", T, "Single discount", B, "A kettle is marked ₹1,250. The shop allows a 16% discount and then adds 12% GST "
  "on the discounted price. How much does the buyer pay?",
  "₹1,176", ["₹1,050", "₹1,200", "₹1,400"],
  "Apply the discount first, then add GST on the reduced price",
  "Discounted price = 84% of 1,250 = ₹1,050. With 12% GST: 1,050 × 1.12 = ₹1,176.",
  ["1,250 × 0.84 = 1,050", "1,050 × 1.12 = 1,176"],
  why="₹1,050 leaves out the GST; ₹1,200 nets the rates to a 4% discount; ₹1,400 adds GST but forgets the "
      "discount.", secs=40)

p1, p2 = F(7, 10) * F(8, 10), F(3, 4) * F(3, 4)
assert p1 == F(56, 100) and p2 == F(5625, 10000) and p2 - p1 == F(25, 10000)
Q("009", T, "Successive discounts", I, "Which offer is cheaper for the buyer on the same marked price: successive "
  "discounts of 30% and 20%, or successive discounts of 25% and 25%? By how much?",
  "30% and 20%, by 0.25% of the marked price", ["25% and 25%, by 0.25% of the marked price",
                                                "Both cost the same", "30% and 20%, by 5% of the marked price"],
  "The buyer pays (1 − d₁)(1 − d₂) of the marked price",
  "30% then 20%: 0.7 × 0.8 = 0.56. 25% then 25%: 0.75 × 0.75 = 0.5625. The first offer costs 0.25% of the marked "
  "price less.",
  ["0.70 × 0.80 = 0.5600", "0.75 × 0.75 = 0.5625", "Difference = 0.0025 = 0.25%"],
  why="The 25% + 25% offer is dearer, not cheaper; both pairs add to 50% but the products differ; 5% is the gap "
      "between the first discounts.", secs=55)

assert 1 / F(8, 10) - 1 == F(1, 4)
Q("009", T, "Discount with profit", I, "A retailer gets a 20% trade discount on the list price from the wholesaler "
  "and sells the goods at the list price. What is his profit percentage?",
  "25%", ["20%", "16⅔%", "40%"],
  "His cost is 80% of the list price; profit is measured on cost",
  "Cost = 0.8 × list price; selling price = list price. Profit = 0.2 on 0.8 = 25%.",
  ["Cost = 80% of list", "Profit = 20% of list", "20 ÷ 80 = 25%"],
  why="20% measures the profit on the list price; 16⅔% divides 20 by 120; 40% doubles the discount.", secs=45)

M_ = F(462) / (F(9, 10) * F(98, 100) - F(75, 100))
assert M_ == 3500 and F(462) / F(15, 100) == 3080 and F(462) / F(14, 100) == 3300
Q("009", T, "Discount with profit", A, "A dealer buys a sewing machine from the maker at 25% off its marked price and "
  "sells it at 10% off the same marked price. He pays a card-processing fee of 2% of his selling price. His net gain "
  "is ₹462. What is the marked price?",
  "₹3,500", ["₹3,080", "₹3,300", "₹4,620"],
  "Net gain = 0.9M × 0.98 − 0.75M",
  "Selling price = 0.9M; after the fee he keeps 0.882M. Cost = 0.75M. Gain = 0.132M = 462, so M = ₹3,500.",
  ["Kept = 0.9 × 0.98 × M = 0.882M", "Gain = 0.882M − 0.75M = 0.132M", "M = 462 ÷ 0.132 = ₹3,500"],
  why="₹3,080 ignores the fee (462 ÷ 0.15); ₹3,300 takes the fee as 2% of the marked price (462 ÷ 0.14); ₹4,620 "
      "uses only the 10% discount.", secs=85)

assert F(480, 2520 + 480) == F(16, 100)
Q("010", T, "Single discount", B, "A coat is sold for ₹2,520 after a discount of ₹480. What is the rate of discount?",
  "16%", ["19.05%", "20%", "84%"],
  "Marked price = selling price + discount; the rate is discount ÷ marked price",
  "Marked price = 2,520 + 480 = ₹3,000. Rate = 480 ÷ 3,000 = 16%.",
  ["MP = ₹3,000", "480 ÷ 3,000 = 0.16", "Rate = 16%"],
  why="19.05% divides the discount by the selling price; 20% takes the marked price as ₹2,400; 84% is the price paid "
      "as a share of the marked price.", secs=35)

M_ = F(1768) / (F(8, 10) * F(85, 100))
assert M_ == 2600 and F(1768) / F(65, 100) == 2720 and F(1768) / F(8, 10) == 2210
Q("010", T, "Successive discounts", I, "After successive discounts of 20% and 15%, a fan costs ₹1,768. What is its "
  "marked price?",
  "₹2,600", ["₹2,720", "₹2,210", "₹2,386.80"],
  "Price paid = MP × 0.80 × 0.85 = 0.68 × MP",
  "0.68 × MP = 1,768, so MP = 1,768 ÷ 0.68 = ₹2,600.",
  ["0.8 × 0.85 = 0.68", "MP = 1,768 ÷ 0.68", "= ₹2,600"],
  why="₹2,720 adds the discounts to 35%; ₹2,210 undoes only the 20% discount; ₹2,386.80 adds 35% to 1,768.",
  secs=50)

M_ = F(1134, 1000) / (F(7, 10) * F(9, 10))
assert M_ == F(18, 10) and M_ * F(7, 10) == F(126, 100)
Q("010", T, "Discount with profit", A, "A store gives 30% off its marked prices, and a further 10% off the reduced "
  "price for prepaid orders. On a prepaid order it makes a profit of 13.4%. What is its profit percentage on a "
  "cash-on-delivery order, which gets only the 30% discount?",
  "26%", ["23.4%", "13.4%", "80%"],
  "Find the marked price as a multiple of cost from the prepaid order",
  "Prepaid: MP × 0.7 × 0.9 = 0.63 MP = 1.134 × cost, so MP = 1.8 × cost. Cash on delivery: 0.7 × 1.8 = 1.26 × cost, "
  "a profit of 26%.",
  ["0.63 MP = 1.134 C", "MP = 1.8 C", "COD price = 0.7 × 1.8 C = 1.26 C ⇒ 26%"],
  why="23.4% adds 10 points to 13.4%; 13.4% is the prepaid profit; 80% is the markup on cost.", secs=80)

x_, y_ = 10000 * F(85, 100) * F(9, 10), 10000 * F(8, 10) - 500
assert (x_, y_) == (7650, 7500) and 10000 * F(8, 10) - x_ == 350
Q("010", T, "Successive discounts", A, "A television is marked ₹10,000. Shop X offers successive discounts of 15% and "
  "10%. Shop Y offers a flat 20% discount followed by ₹500 cashback on the amount paid. Which shop is cheaper for "
  "the buyer, and by how much?",
  "Shop Y, by ₹150", ["Shop X, by ₹350", "Shop X, by ₹150", "Both cost the same"],
  "Work out the net amount at each shop",
  "Shop X: 10,000 × 0.85 × 0.9 = ₹7,650. Shop Y: 10,000 × 0.8 − 500 = ₹7,500. Shop Y is cheaper by ₹150.",
  ["X: 10,000 × 0.85 × 0.90 = 7,650", "Y: 8,000 − 500 = 7,500", "Y cheaper by ₹150"],
  why="Shop X, by ₹350 ignores Y's cashback (8,000 − 7,650); Shop X, by ₹150 reverses the comparison; 'both the "
      "same' adds X's discounts to 25%.", secs=70)

# ================================================================ Simple Interest (009: B1 I2 A1; 010: B1 I2 A1)
T = "Simple Interest"
assert F(2, 16) * 100 == F(25, 2)
Q("009", T, "Basic SI", B, "At what rate of simple interest per annum will a sum of money become three times itself "
  "in 16 years?",
  "12.5%", ["18.75%", "6.25%", "16%"],
  "Becoming three times means the interest is twice the principal",
  "Interest = 2P in 16 years, so the yearly rate = 200% ÷ 16 = 12.5%.",
  ["Interest = 3P − P = 2P", "Rate × 16 = 200%", "Rate = 12.5%"],
  why="18.75% takes the interest as 3P; 6.25% takes it as P (doubling); 16% treats the number of years as the "
      "rate.", secs=35)

si = 12000 * (F(6, 100) * 2 + F(8, 100) * 3)
assert si == 4320
Q("009", T, "SI with changing rates", I, "₹12,000 is lent at simple interest at 6% per annum for the first 2 years "
  "and 8% per annum for the next 3 years. What is the total interest for the 5 years?",
  "₹4,320", ["₹4,800", "₹3,600", "₹4,200"],
  "Add the interest of each period separately",
  "First 2 years: 12,000 × 6% × 2 = ₹1,440. Next 3 years: 12,000 × 8% × 3 = ₹2,880. Total = ₹4,320.",
  ["12,000 × 0.06 × 2 = 1,440", "12,000 × 0.08 × 3 = 2,880", "Total = 4,320"],
  why="₹4,800 uses 8% for all 5 years; ₹3,600 uses 6% throughout; ₹4,200 uses the plain average rate 7%.", secs=50)

assert F(9, 25) / 3 * 100 == 12
Q("009", T, "Basic SI", I, "The simple interest on a sum for 3 years is 9/25 of the sum. What is the rate per annum?",
  "12%", ["36%", "9%", "8⅓%"],
  "SI ÷ principal = rate × time",
  "9/25 = 36% of the sum in 3 years, so the yearly rate is 36% ÷ 3 = 12%.",
  ["9/25 = 36%", "Over 3 years", "Rate = 12%"],
  why="36% is the total for 3 years; 9% reads the numerator as the rate; 8⅓% divides 25 by 3.", secs=45)

stay = 40000 * (1 + F(8, 100) * 5)
due2 = 40000 * (1 + F(8, 100) * 2)
refi = due2 * (1 + F(6, 100) * 3)
assert (stay, due2, refi) == (56000, 46400, F(54752)) and stay - refi == 1248 and due2 * F(6, 100) == 2784
Q("009", T, "SI with changing rates", A, "Arun borrows ₹40,000 for 5 years at 8% per annum simple interest. After 2 "
  "years he takes a new loan at 6% per annum simple interest to pay off everything he then owes, and repays the new "
  "loan at the end of the 5th year. How much does he save compared with keeping the first loan?",
  "₹1,248", ["₹2,400", "₹2,784", "₹1,600"],
  "The new loan's principal is the full amount due after 2 years, interest included",
  "Keeping the first loan: 40,000 × 1.40 = ₹56,000. After 2 years he owes 40,000 × 1.16 = ₹46,400. The new loan for "
  "3 years at 6%: 46,400 × 1.18 = ₹54,752. Saving = 56,000 − 54,752 = ₹1,248.",
  ["Old loan: 40,000 × (1 + 0.40) = 56,000", "Due after 2 years: 46,400", "New: 46,400 × 1.18 = 54,752",
   "Saving = 1,248"],
  why="₹2,400 applies the 2% cut to ₹40,000 for 3 years, ignoring that the new principal is larger; ₹2,784 is "
      "one year's interest on ₹46,400; ₹1,600 applies the cut for 2 years only.", secs=95)

assert 15000 * F(7, 100) * F(146, 365) == 420
Q("010", T, "Basic SI", B, "What is the simple interest on ₹15,000 at 7% per annum for 146 days? (Take a year as 365 "
  "days.)",
  "₹420", ["₹1,050", "₹210", "₹840"],
  "Time in years = 146 ÷ 365 = 0.4",
  "SI = 15,000 × 7/100 × 146/365 = 15,000 × 0.07 × 0.4 = ₹420.",
  ["146 ÷ 365 = 0.4 year", "15,000 × 0.07 = 1,050 a year", "1,050 × 0.4 = ₹420"],
  why="₹1,050 is the interest for a full year; ₹210 uses 73 days; ₹840 takes 146 days as 0.8 of a year.", secs=40)

P_ = F(480) / (F(24, 100) - F(18, 100))
assert P_ == 8000
Q("010", T, "Basic SI", I, "The simple interest on a sum for 3 years at 8% per annum is ₹480 more than the simple "
  "interest on the same sum for 2 years at 9% per annum. What is the sum?",
  "₹8,000", ["₹48,000", "₹6,000", "₹2,000"],
  "Compare total rates: 3 × 8% = 24% and 2 × 9% = 18%",
  "The difference is 24% − 18% = 6% of the sum = ₹480, so the sum = 480 ÷ 0.06 = ₹8,000.",
  ["3 × 8% = 24%", "2 × 9% = 18%", "6% of P = 480 ⇒ P = 8,000"],
  why="₹48,000 uses the 1% gap between the rates; ₹6,000 divides 480 by 8%; ₹2,000 divides 480 by 24%.", secs=50)

si = 20000 * (F(7, 100) * F(9, 12) + F(8, 100) * F(15, 12))
assert si == 3050 and 20000 * (F(7, 100) * F(15, 12) + F(8, 100) * F(9, 12)) == 2950
Q("010", T, "SI with changing rates", I, "₹20,000 is deposited at simple interest. The rate is 7% per annum for the "
  "first 9 months and 8% per annum for the next 15 months. What is the total interest?",
  "₹3,050", ["₹2,950", "₹3,000", "₹3,200"],
  "Convert months to years and add the interest of each period",
  "9 months at 7%: 20,000 × 0.07 × 0.75 = ₹1,050. 15 months at 8%: 20,000 × 0.08 × 1.25 = ₹2,000. Total = ₹3,050.",
  ["20,000 × 0.07 × 9/12 = 1,050", "20,000 × 0.08 × 15/12 = 2,000", "Total = 3,050"],
  why="₹2,950 swaps the two periods; ₹3,000 uses 7.5% for 2 years; ₹3,200 uses 8% for the whole 2 years.",
  secs=55)

yr = 720
P_ = 13320 - 6 * yr
assert P_ == 9000 and F(yr, P_) == F(8, 100)
Q("010", T, "Basic SI", A, "A sum is lent at simple interest. The interest for the 4th year alone is ₹720, and the "
  "amount after 6 years is ₹13,320. What is the rate of interest per annum?",
  "8%", ["5.4%", "7.2%", "32%"],
  "Under simple interest every year's interest is the same",
  "Interest for 6 years = 6 × 720 = ₹4,320, so the principal = 13,320 − 4,320 = ₹9,000. Rate = 720 ÷ 9,000 = 8%.",
  ["Yearly interest = ₹720", "6 years: ₹4,320", "P = 13,320 − 4,320 = 9,000", "Rate = 720 ÷ 9,000 = 8%"],
  why="5.4% divides 720 by the amount ₹13,320; 7.2% takes the principal as ₹10,000; 32% is the interest for 4 "
      "years as a percentage.", secs=75)

# ================================================================ Compound Interest (009: B2 I2 A1; 010: B1 I3 A2)
T = "Compound Interest"
assert 8000 * F(115, 100) ** 2 == 10580
Q("009", T, "Annual compounding", B, "What amount will ₹8,000 grow to in 2 years at 15% per annum compound interest, "
  "compounded annually?",
  "₹10,580", ["₹10,400", "₹2,580", "₹9,200"],
  "Amount = P(1 + r)ⁿ",
  "8,000 × 1.15 = 9,200 after one year; 9,200 × 1.15 = ₹10,580 after two.",
  ["Year 1: 8,000 × 1.15 = 9,200", "Year 2: 9,200 × 1.15 = 10,580"],
  why="₹10,400 uses simple interest; ₹2,580 is the interest, not the amount; ₹9,200 is the amount after one year.",
  secs=40)

P_ = F(1500) / F(12, 100)
ci = P_ * (F(106, 100) ** 2 - 1)
assert P_ == 12500 and ci == 1545
Q("009", T, "CI vs SI difference", B, "The simple interest on a sum for 2 years at 6% per annum is ₹1,500. What is "
  "the compound interest on the same sum for 2 years at the same rate, compounded annually?",
  "₹1,545", ["₹1,500", "₹1,590", "₹14,045"],
  "Find the sum from the SI; for 2 years CI − SI = P × r²",
  "P = 1,500 ÷ 0.12 = ₹12,500. CI − SI = 12,500 × 0.06² = ₹45, so CI = ₹1,545.",
  ["P = 1,500 ÷ (2 × 6%) = 12,500", "CI − SI = 12,500 × 0.0036 = 45", "CI = 1,545"],
  why="₹1,500 is the simple interest; ₹1,590 adds 6% of ₹1,500 (interest on both years' interest); ₹14,045 is the "
      "amount, not the interest.", secs=50)

assert F(106, 100) ** 4 == F(11236, 10000) ** 2
Q("009", T, "Half-yearly and quarterly", I, "Ravi invests ₹50,000 for 2 years at 12% per annum compounded "
  "half-yearly. Mohan invests ₹50,000 for 2 years at 12.36% per annum compounded annually. Whose amount is larger at "
  "the end?",
  "Both amounts are equal", ["Ravi's", "Mohan's", "Ravi's, by 0.36% of the sum"],
  "Compare the growth factors: (1.06)⁴ for Ravi and (1.1236)² for Mohan",
  "12% compounded half-yearly is 6% per half-year, and 1.06² = 1.1236, an effective annual rate of 12.36%. So "
  "1.06⁴ = 1.1236² and both grow to the same amount.",
  ["Ravi: 1.06 per half-year", "1.06² = 1.1236", "Mohan: 1.1236 per year", "Same factor ⇒ equal amounts"],
  why="Ravi and Mohan earn exactly the same, because 12.36% is the effective annual rate of 12% compounded "
      "half-yearly; 0.36% is the gap between the quoted rates, not between the amounts.", secs=60)

P_ = F(6600) / F(11, 10) + F(7260) / F(11, 10) ** 2
assert P_ == 12000 and 6000 + F(7260) / F(11, 10) == 12600 and F(6600) / F(11, 10) + F(7260) / F(12, 10) == 12050
Q("009", T, "Instalments", I, "A loan taken at 10% per annum compound interest (compounded annually) is cleared by "
  "paying ₹6,600 at the end of the first year and ₹7,260 at the end of the second year. What was the loan?",
  "₹12,000", ["₹13,860", "₹12,600", "₹12,050"],
  "The loan equals the present value of the payments: each is divided by 1.1 for every year it is deferred",
  "6,600 ÷ 1.1 = ₹6,000 and 7,260 ÷ 1.1² = ₹6,000. The loan = 6,000 + 6,000 = ₹12,000.",
  ["6,600 ÷ 1.1 = 6,000", "7,260 ÷ 1.21 = 6,000", "Loan = 12,000"],
  why="₹13,860 adds the payments with no discounting; ₹12,600 discounts the second payment for only one year; "
      "₹12,050 discounts at simple interest (7,260 ÷ 1.2).", secs=65)

def ratio_ci_si(r):
    return ((1 + r) ** 3 - 1) / (3 * r)


assert ratio_ci_si(F(1, 10)) == F(331, 300)
assert all(ratio_ci_si(F(p, 100)) != F(331, 300) for p in (5, 11, 20))
Q("009", T, "CI vs SI difference", A, "For a certain sum and rate, the compound interest (compounded annually) and the "
  "simple interest for 3 years are in the ratio 331 : 300. What is the rate of interest per annum?",
  "10%", ["5%", "11%", "20%"],
  "CI : SI = [(1 + r)³ − 1] : 3r; for 3 years this equals 1 + r + r²/3",
  "(1 + r)³ − 1 = 3r + 3r² + r³, so CI/SI = 1 + r + r²/3 = 331/300. With r = 0.1: 1 + 0.1 + 0.01/3 = 331/300 ✓.",
  ["CI/SI = 1 + r + r²/3", "= 331/300 = 1 + 31/300", "r = 0.1 ⇒ 0.1 + 0.0033… = 31/300 ✓", "Rate = 10%"],
  why="5%, 11% and 20% give ratios of about 1.051, 1.114 and 1.213, not 331/300 ≈ 1.103.", secs=85)

P_ = F(13310) / F(11, 10) ** 3
assert P_ == 10000 and F(13310) / F(11, 10) == 12100
Q("010", T, "Annual compounding", B, "A sum amounts to ₹13,310 in 3 years at 10% per annum compound interest, "
  "compounded annually. What is the sum?",
  "₹10,000", ["₹3,310", "₹11,979", "₹12,100"],
  "Principal = amount ÷ (1.1)³",
  "1.1³ = 1.331, so the sum = 13,310 ÷ 1.331 = ₹10,000.",
  ["1.1³ = 1.331", "13,310 ÷ 1.331 = 10,000"],
  why="₹3,310 is the interest; ₹11,979 takes 10% off 13,310; ₹12,100 divides by 1.1 only once.", secs=35)

due = (50000 * F(106, 100) - 26500) * F(106, 100)
assert due == 28090 and 50000 * F(106, 100) ** 2 - 26500 == 29680 and 50000 * F(112, 100) - 26500 == 29500
Q("010", T, "Half-yearly and quarterly", I, "Meena borrows ₹50,000 at 12% per annum compound interest, compounded "
  "half-yearly. She repays ₹26,500 at the end of 6 months. How much must she pay at the end of the year to clear the "
  "loan?",
  "₹28,090", ["₹29,680", "₹26,500", "₹29,500"],
  "Interest is 6% per half-year; reduce the balance by the repayment before the second half-year's interest",
  "After 6 months: 50,000 × 1.06 = ₹53,000; after repaying ₹26,500 she owes ₹26,500. After another 6 months: "
  "26,500 × 1.06 = ₹28,090.",
  ["53,000 after 6 months", "53,000 − 26,500 = 26,500", "26,500 × 1.06 = 28,090"],
  why="₹29,680 charges interest on the full loan for the year and subtracts the repayment at the end; ₹26,500 "
      "leaves out the second half-year's interest; ₹29,500 compounds annually at 12%.", secs=60)

r_ = next(r for r in range(1, 30) if 10000 * (F(100 + r, 100) ** 2 - 1) == 2544)
assert r_ == 12 and 10000 * F(24, 100) == 2400
Q("010", T, "CI vs SI difference", I, "The compound interest on ₹10,000 for 2 years, compounded annually, is ₹2,544. "
  "What is the simple interest on the same sum for 2 years at the same rate?",
  "₹2,400", ["₹1,272", "₹2,544", "₹2,688"],
  "Find the rate from the amount: (1 + r)² = 12,544/10,000",
  "Amount = ₹12,544 = 10,000 × 1.12², so the rate is 12%. SI for 2 years = 10,000 × 0.12 × 2 = ₹2,400.",
  ["(1 + r)² = 1.2544 ⇒ r = 12%", "SI = 10,000 × 0.24", "= 2,400"],
  why="₹1,272 halves the CI; ₹2,544 is the CI itself; ₹2,688 adds P × r² (₹144) instead of subtracting it.",
  secs=55)

P_ = F(28090) / F(106, 100) ** 2
assert P_ == 25000 and P_ * F(106, 100) * F(6, 100) == 1590 and F(28090) * F(6, 100) == F(168540, 100)
Q("010", T, "Annual compounding", I, "A sum amounts to ₹28,090 in 2 years at 6% per annum compound interest, "
  "compounded annually. How much interest is earned in the second year alone?",
  "₹1,590", ["₹1,500", "₹3,090", "₹1,685.40"],
  "Second-year interest = 6% of the amount at the end of the first year",
  "Principal = 28,090 ÷ 1.06² = ₹25,000. After year 1: ₹26,500. Second-year interest = 6% of 26,500 = ₹1,590.",
  ["P = 28,090 ÷ 1.1236 = 25,000", "End of year 1: 26,500", "6% of 26,500 = 1,590"],
  why="₹1,500 is the first year's interest; ₹3,090 is the interest for both years; ₹1,685.40 takes 6% of the final "
      "amount.", secs=55)

r_ = F(496, 160) - 3
P_ = F(160) / r_ ** 2
assert r_ == F(1, 10) and P_ == 16000 and P_ * (F(11, 10) ** 3 - 1 - 3 * r_) == 496
Q("010", T, "CI vs SI difference", A, "On a certain sum at a certain rate, the difference between the compound "
  "interest (compounded annually) and the simple interest is ₹160 for 2 years and ₹496 for 3 years. What is the sum?",
  "₹16,000", ["₹4,000", "₹64,000", "₹1,600"],
  "For 2 years the difference is Pr²; for 3 years it is Pr²(3 + r)",
  "496 ÷ 160 = 3.1 = 3 + r, so r = 0.1 (10%). Then P × 0.01 = 160 gives P = ₹16,000.",
  ["d₂ = Pr² = 160", "d₃ = Pr²(3 + r) = 496", "3 + r = 3.1 ⇒ r = 10%", "P = 160 ÷ 0.01 = 16,000"],
  why="₹4,000 takes the rate as 20%; ₹64,000 takes it as 5%; ₹1,600 divides 160 by 0.1 instead of 0.1².",
  secs=90)

q_ = 160000 * F(105, 100) ** 4 - 160000
h_ = 160000 * F(110, 100) ** 2 - 160000
assert (q_, h_) == (34481, 33600) and q_ - h_ == 881 and q_ - 32000 == 2481
Q("010", T, "Half-yearly and quarterly", A, "On ₹1,60,000 at 20% per annum for 1 year, how much more interest is "
  "earned when the interest is compounded quarterly rather than half-yearly?",
  "₹881", ["₹2,481", "₹1,600", "₹34,481"],
  "Quarterly: 5% for 4 quarters; half-yearly: 10% for 2 half-years",
  "Quarterly: 1,60,000 × 1.05⁴ = ₹1,94,481, interest ₹34,481. Half-yearly: 1,60,000 × 1.1² = ₹1,93,600, interest "
  "₹33,600. Difference = ₹881.",
  ["1.05⁴ = 1.21550625 ⇒ 34,481", "1.1² = 1.21 ⇒ 33,600", "34,481 − 33,600 = 881"],
  why="₹2,481 compares quarterly with simple interest (₹32,000); ₹1,600 compares half-yearly with simple interest; "
      "₹34,481 is the quarterly interest itself.", secs=80)

# ================================================================ Partnership (009: B2 I1 A1; 010: B1 I1 A1)
T = "Partnership"
assert F(15000 * 32, 80) == 6000
Q("009", T, "Simple partnership", B, "A and B invest ₹32,000 and ₹48,000 in a business for the same period. Out of a "
  "profit of ₹15,000, what is A's share?",
  "₹6,000", ["₹9,000", "₹7,500", "₹5,000"],
  "For the same period, profit is shared in the ratio of capitals",
  "32,000 : 48,000 = 2 : 3. A's share = 2/5 × 15,000 = ₹6,000.",
  ["Ratio 2 : 3", "A = 2/5 of 15,000", "= 6,000"],
  why="₹9,000 is B's share; ₹7,500 splits equally; ₹5,000 takes A's share as one-third.", secs=35)

a_, b_ = 24000 * 10, 30000 * 6
assert F(14000 * b_, a_ + b_) == 6000
Q("009", T, "Compound partnership", B, "A invests ₹24,000 for 10 months and B invests ₹30,000 for 6 months in a "
  "business. Out of a profit of ₹14,000, what is B's share?",
  "₹6,000", ["₹8,000", "₹7,000", "₹4,000"],
  "Share profit in the ratio of capital × months",
  "A: 24,000 × 10 = 2,40,000. B: 30,000 × 6 = 1,80,000. Ratio 4 : 3, so B gets 3/7 × 14,000 = ₹6,000.",
  ["A: 2,40,000; B: 1,80,000", "Ratio 4 : 3", "B = 3/7 × 14,000 = 6,000"],
  why="₹8,000 is A's share; ₹7,000 splits equally; ₹4,000 takes B's share as 2/7.", secs=45)

b_share = F(46000 - 10000, 90000)
assert b_share == F(2, 5) and (1 - b_share) / b_share == F(3, 2)
Q("009", T, "Working partner", I, "A and B run a firm. B, the working partner, first takes 10% of the profit as "
  "commission, and the rest is shared in the ratio of their capitals. Out of a profit of ₹1,00,000, B receives "
  "₹46,000 in all. What is the ratio of A's capital to B's?",
  "3 : 2", ["2 : 3", "27 : 23", "1 : 1"],
  "Take away B's commission first; the rest of his receipt is his capital share",
  "Commission = ₹10,000, so ₹90,000 is shared. B's share of it = 46,000 − 10,000 = ₹36,000 = 2/5. A gets 3/5, so "
  "A : B = 3 : 2.",
  ["Commission = 10,000", "B's share of 90,000 = 36,000 = 2/5", "A : B = 3 : 2"],
  why="2 : 3 inverts the ratio; 27 : 23 compares their total receipts (54,000 : 46,000), commission included; 1 : 1 "
      "would give B ₹55,000.", secs=60)

w_ = next(w for w in range(0, 60001, 1000) if F(40000 * 12) == F(125, 100) * (60000 * 4 + (60000 - w) * 8))
assert w_ == 42000 and next(w for w in range(0, 60001, 1000) if F(75, 100) * 480000 == 240000 + (60000 - w) * 8) == 45000
Q("009", T, "Compound partnership", A, "A invests ₹40,000 in a business for the whole year. B invests ₹60,000 but "
  "withdraws part of it after 4 months, leaving the rest for the remaining 8 months. At the end of the year A's share "
  "of the profit is 25% more than B's. How much did B withdraw?",
  "₹42,000", ["₹18,000", "₹45,000", "₹30,000"],
  "Profit shares are in the ratio of capital × months",
  "A: 40,000 × 12 = 4,80,000. B's capital-months must be 4,80,000 ÷ 1.25 = 3,84,000. B: 60,000 × 4 + (60,000 − w) × "
  "8 = 3,84,000, so (60,000 − w) × 8 = 1,44,000, 60,000 − w = 18,000 and w = ₹42,000.",
  ["A = 4,80,000", "B = 4,80,000 ÷ 1.25 = 3,84,000", "2,40,000 + 8(60,000 − w) = 3,84,000", "w = 42,000"],
  why="₹18,000 is what B kept in the business; ₹45,000 takes B's share as 25% less than A's; ₹30,000 assumes B "
      "halved his capital.", secs=90)

assert F(36000 * 90, 120 + 150 + 90) == 9000
Q("010", T, "Simple partnership", B, "A, B and C invest ₹1.2 lakh, ₹1.5 lakh and ₹0.9 lakh in a business for the same "
  "period. Out of a profit of ₹36,000, what is C's share?",
  "₹9,000", ["₹12,000", "₹15,000", "₹10,800"],
  "Profit is shared in the ratio of capitals: 12 : 15 : 9 = 4 : 5 : 3",
  "Total parts = 12. C gets 3/12 × 36,000 = ₹9,000.",
  ["Ratio 4 : 5 : 3", "C = 3/12 of 36,000", "= 9,000"],
  why="₹12,000 and ₹15,000 are A's and B's shares; ₹10,800 takes C's share as 30%.", secs=35)

a_, b_ = 72000 * 12, 90000 * (12 - 4 - 2)
assert F(143000 * b_, a_ + b_) == 55000 and F(a_, b_) == F(8, 5) and F(143000 * 720000, a_ + 720000) == 65000
Q("010", T, "Compound partnership", I, "A starts a business with ₹72,000. Four months later B joins with ₹90,000, and "
  "B leaves 2 months before the end of the year. Out of a year's profit of ₹1,43,000, what is B's share?",
  "₹55,000", ["₹88,000", "₹65,000", "₹71,500"],
  "B's money is in the business for 12 − 4 − 2 = 6 months",
  "A: 72,000 × 12 = 8,64,000. B: 90,000 × 6 = 5,40,000. Ratio 8 : 5, so B gets 5/13 × 1,43,000 = ₹55,000.",
  ["B's months = 6", "8,64,000 : 5,40,000 = 8 : 5", "B = 5/13 × 1,43,000 = 55,000"],
  why="₹88,000 is A's share; ₹65,000 counts B for 8 months (ignoring that he left early); ₹71,500 splits "
      "equally.",
  secs=60)

sol = [p for p in range(0, 100) if F(p, 100) + (1 - F(p, 100)) / 6 == (1 - F(p, 100)) / 2]
assert sol == [25]
Q("010", T, "Working partner", A, "A, B and C invest capitals in the ratio 1 : 2 : 3. A manages the business and "
  "first takes a fixed percentage of the profit as salary; the rest is shared in the ratio of capitals. What "
  "percentage must A's salary be so that A and C receive equal amounts in total?",
  "25%", ["33⅓%", "20%", "50%"],
  "Let A's salary be s of the profit; A gets s + (1 − s)/6 and C gets (1 − s)/2",
  "s + (1 − s)/6 = (1 − s)/2. Multiply by 6: 6s + 1 − s = 3 − 3s, so 8s = 2 and s = 1/4 = 25%. Check with a profit "
  "of 100: A = 25 + 12.5 = 37.5 and C = 37.5.",
  ["A = s + (1 − s)/6", "C = (1 − s)/2", "8s = 2 ⇒ s = 25%"],
  why="33⅓% gives A 44.4 and C 33.3; 20% gives A 33.3 and C 40; 50% gives A 58.3 and C 25 (per 100 of profit).",
  secs=85)


# ================================================================ ordering, IDs, keys, checks and output
_rng = random.Random(20261105 + 91)
TOPIC_ORDER = PKG["topics"]
DIFF_ORDER = [B, I, A]
OUT = {}
for bt, plan in PKG["batches"].items():
    recs = sorted(PENDING[bt], key=lambda r: (TOPIC_ORDER.index(r["topic"]), DIFF_ORDER.index(r["diff"])))
    n = len(recs)
    # Balanced keys: as even as possible (98 = 25 A, 25 B, 24 C, 24 D), order fixed by the seed.
    keys = list("ABCD" * 25)[:n]
    _rng.shuffle(keys)
    first = int(plan["question_ids"][0].rsplit("_", 1)[1])
    questions = []
    for k, (r, key) in enumerate(zip(recs, keys)):
        qid = f"BANK_QUANT_{first + k:06d}"
        opts = list(r["wrong"])
        opts.insert(LETTERS.index(key), r["ans"])
        by = list(r["by"])
        if qid in INDEPENDENT:
            by.append("ai:independent-check")
        questions.append({
            "question_id": qid,
            "exam_mappings": default_mappings(SUBJECT, r["diff"]),
            "subject": SUBJECT, "topic": r["topic"], "subtopic": r["sub"], "difficulty": r["diff"],
            "question_type": "MCQ", "language": "en",
            "question_text": r["text"],
            "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(opts)],
            "correct_answer": key,
            "solution": {"concept": r["concept"], "explanation": r["expl"], "steps": r["steps"],
                         "shortcut": r["short"], "why_others_wrong": r["why"],
                         "final_answer": f"Option {key}: {r['ans']}"},
            "suggested_time_seconds": r["secs"],
            "source": {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                       "original_exam_year": None, "license_note": None},
            "verification": {"answer_verified": True, "solution_verified": True,
                             "review_status": "Pending Human Review", "verified_by": by, "verified_at": TODAY},
        })
    OUT[bt] = questions

if "--partial" in sys.argv:  # development aid: counts only, nothing written
    for bt, qs in OUT.items():
        print(bt, len(qs), dict(Counter((q["topic"][:12], q["difficulty"][0]) for q in qs)))
    sys.exit(0)

for bt, plan in PKG["batches"].items():
    qs = OUT[bt]
    have = Counter((q["topic"], q["difficulty"]) for q in qs)
    want = Counter({(t["topic"], d): n for t in plan["topics"] for d, n in t["quota"].items() if n})
    assert have == want, (bt, set(have.items()) ^ set(want.items()))
    assert len(qs) == plan["count"] and Counter(q["difficulty"] for q in qs) == Counter(plan["by_difficulty"])
    subs = {t["topic"]: set(t["subtopics"]) for t in plan["topics"]}
    assert all(q["subtopic"] in subs[q["topic"]] for q in qs), [
        (q["topic"], q["subtopic"]) for q in qs if q["subtopic"] not in subs[q["topic"]]]
    assert qs[0]["question_id"] == plan["question_ids"][0] and qs[-1]["question_id"] == plan["question_ids"][1]
    ids = [int(q["question_id"].rsplit("_", 1)[1]) for q in qs]
    assert ids == list(range(ids[0], ids[0] + len(ids)))
    # No shared stimuli in this package (no DI sets); the plan's stimulus_id_start is therefore unused.
    assert plan["stimulus_id_start"] == f"STIM_QUANT_{int(bt):03d}101"
    kc = Counter(q["correct_answer"] for q in qs)
    assert max(kc.values()) - min(kc.values()) <= 1 and len(kc) == 4, kc
assert INDEPENDENT <= {q["question_id"] for qs in OUT.values() for q in qs}
texts = [normalize(q["question_text"]) for qs in OUT.values() for q in qs]
assert len(texts) == len(set(texts)), "duplicate stem inside the package"

if "--dump" in sys.argv:  # blind copies for solvers: no key, no solution
    want_ids = None
    if "--ids" in sys.argv:
        want_ids = set(sys.argv[sys.argv.index("--ids") + 1].split(","))
    blind = [{"question_id": q["question_id"], "question_text": q["question_text"], "options": q["options"]}
             for qs in OUT.values() for q in qs if want_ids is None or q["question_id"] in want_ids]
    Path(sys.argv[sys.argv.index("--dump") + 1]).write_text(
        json.dumps({"questions": blind}, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"blind dump written ({len(blind)} questions)")
    sys.exit(0)

if "--keys" in sys.argv:  # answer keys for comparing a blind run
    print(json.dumps({q["question_id"]: q["correct_answer"] for qs in OUT.values() for q in qs}))
    sys.exit(0)

for bt, plan in PKG["batches"].items():
    qs = OUT[bt]
    kc = Counter(q["correct_answer"] for q in qs)
    nd = Counter(q["difficulty"] for q in qs)
    frag = {
        "schema_version": "1.0",
        "batch_id": plan["batch_id"],
        "created_at": TODAY,
        "notes": f"{plan['batch_id']}, Quantitative Aptitude, topic package QUANT_pkg1 (Simplification to "
                 f"Partnership): {len(qs)} original questions ({nd[B]} Basic, {nd[I]} Intermediate, {nd[A]} "
                 "Advanced), no shared stimuli. Every answer was recomputed by tools/packages/QUANT_pkg1.py before "
                 "writing; number series were also tested against a library of rival rules. Questions tagged "
                 "ai:independent-check were re-solved from the stem and options alone by a separate solver. Pending "
                 "human review.",
        "stimuli": [],
        "questions": qs,
    }
    out = ROOT / plan["output"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(qs)} questions, keys {dict(sorted(kc.items()))}, "
          f"independent-check {sum('ai:independent-check' in q['verification']['verified_by'] for q in qs)})")
print(f"series checked against the rival-rule library: {len(SERIES_LOG)}")
