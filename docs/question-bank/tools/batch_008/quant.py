"""Writes batches/parts/BATCH_008_QUANT.json: the 199 Quantitative Aptitude questions of BATCH_008.

Every answer is recomputed here before the file is written: arithmetic with exact fractions, series regenerated
from their rule, quadratic roots substituted back, probabilities and arrangements counted by brute force,
data-sufficiency statements checked by enumerating candidate cases, approximation answers checked to be the option
nearest the exact value by a clear margin. If any assertion fails, nothing is written.

New in batch 8: every number series (missing-term and wrong-term) is also tested against a library of common
alternative rules (constant, second and third differences; x k + c with constant, n, n^2, n^3, 2^n or alternating
additions; multipliers n + m; closed forms a f(n) + b g(n) + c with n, n^2, n^3, 2^n, 3^n, n! and primes; sums and
linear combinations of the previous two or three terms; products of the previous two; alternating two-series;
digit sums). For a missing-term series, no rule that fits all the given terms may give a different option; for a
wrong-term series, no rule may fit the series once any option other than the key is removed.

Structure and helpers follow tools/batch_007/quant.py (relation-option guards, no-equal-quantity rule and 2% gap for
quantity comparison, balanced key shuffler with a new seed, approximation margin check, set-size asserts, no ties
where a maximum or minimum is asked). All earlier Quant stems (BATCH_000 to BATCH_007, 1,403 questions) and the 79
earlier DI titles were read first; DI themes, question types and number templates here are new.

    python tools/batch_008/quant.py          (run from docs/question-bank)
    python tools/batch_008/quant.py --dump <file> [--ids a,b,...]   (blind copy for solvers: no key, no solution)
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

# Balanced answer keys: 50 A, 50 B, 50 C and 49 D, order fixed by the seed (new seed for batch 8).
_rng = random.Random(20261105 + 8)
KEYS = list("ABCD" * 50)[:TOTAL]
_rng.shuffle(KEYS)

QUESTIONS, STIMULI = [], []
_set_pos = {}
_FIRST_ID = 1404
_FIRST_STIM = 8001
RECOMPUTE = ["script:recompute", "ai:self-recheck"]
BRUTE = ["script:recompute", "script:brute-force-unique", "ai:self-recheck"]

# Questions that a separate, fresh solver re-answered from the stem, options and data set alone (no key, no
# solution) and whose answer matched the key. Only these carry ai:independent-check. Every third question
# (BANK_QUANT_001404, _001407, ..., _001602: 67 questions) was given to three separate fresh solver agents (23, 22 and
# 22 questions, blind dumps made with --dump --ids); all 67 answers matched the key. No question was changed after its
# blind check.
INDEPENDENT = {f"BANK_QUANT_{n:06d}" for n in range(1404, 1603, 3)}

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


def unique_max(d):
    """The key of the largest value, asserting there is no tie for first place."""
    srt = sorted(d.values(), reverse=True)
    assert srt[0] != srt[1], ("tie for maximum", d)
    return max(d, key=d.get)


def unique_min(d):
    srt = sorted(d.values())
    assert srt[0] != srt[1], ("tie for minimum", d)
    return min(d, key=d.get)


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

# ================================================================ Simplification (B1 I4 A4)
T = "Simplification"
v = F(324, 18) * 5 - 7 * 13 + 6 ** 2
assert v == 35 and F(324, 90) - 91 + 36 == F(-514, 10) and 90 - 91 + 12 == 11 and 90 - (91 + 36) == -37
Q(T, "BODMAS", B, "Simplify: 324 ÷ 18 × 5 − 7 × 13 + 6²",
  "35", ["−51.4", "11", "−37"],
  "Powers first, then ÷ and × from left to right, then + and − from left to right",
  "324 ÷ 18 = 18, and 18 × 5 = 90. Next 7 × 13 = 91 and 6² = 36. So 90 − 91 + 36 = 35.",
  ["324 ÷ 18 × 5 = 18 × 5 = 90", "7 × 13 = 91", "6² = 36", "90 − 91 + 36 = 35"],
  why="−51.4 multiplies 18 × 5 first and divides 324 by 90 (3.6 − 91 + 36); 11 takes 6² as 6 × 2 = 12; −37 subtracts "
      "91 + 36 together, as if the − sign covered both terms.", secs=40)

v = F(5, 3) * F("2.4") / F("0.08") - F(15, 4) * F("1.6")
assert v == 44 and F(4) / F("0.8") - 6 == -1 and F("1.6") * F("2.4") / F("0.08") - 6 == 42 and 50 + 6 == 56
Q(T, "Fractions and decimals", I, QMARK + "1⅔ of 2.4 ÷ 0.08 − 3¾ × 1.6 = ?",
  "44", ["−1", "42", "56"],
  "'Of' is worked first; convert the mixed numbers to fractions (1⅔ = 5/3, 3¾ = 15/4)",
  "1⅔ of 2.4 = 5/3 × 2.4 = 4. 4 ÷ 0.08 = 50. 3¾ × 1.6 = 15/4 × 1.6 = 6. So 50 − 6 = 44.",
  ["5/3 × 2.4 = 4", "4 ÷ 0.08 = 400 ÷ 8 = 50", "15/4 × 1.6 = 6", "50 − 6 = 44"],
  why="−1 divides 4 by 0.8 instead of 0.08 (5 − 6); 42 rounds 1⅔ to 1.6 (1.6 × 2.4 ÷ 0.08 = 48); 56 adds the 6 "
      "instead of subtracting it.", secs=55)

sols = [(x, y) for x in range(-10, 11) for y in range(-10, 11) if 2 ** (x + y) == 64 and F(3) ** (x - y) == F(1, 9)]
assert sols == [(2, 4)] and 2 * 2 + 4 == 8
assert 2 * 4 + 2 == 10 and 2 + 4 == 6 and 2 * F(5, 2) + F(7, 2) == F(17, 2)
Q(T, "Surds and indices", I, "If 2^(x + y) = 64 and 3^(x − y) = 1/9, what is the value of 2x + y?",
  "8", ["10", "6", "8.5"],
  "Write both right sides as powers of the same base and compare exponents: 64 = 2⁶ and 1/9 = 3⁻²",
  "2^(x + y) = 2⁶ gives x + y = 6. 3^(x − y) = 3⁻² gives x − y = −2. Adding, 2x = 4, so x = 2 and y = 4. Then "
  "2x + y = 4 + 4 = 8.",
  ["x + y = 6", "x − y = −2 (since 1/9 = 3⁻²)", "x = 2, y = 4", "2x + y = 8"],
  why="10 drops the minus sign (x − y = 2 gives x = 4, y = 2); 6 is x + y, not 2x + y; 8.5 writes 1/9 as 3⁻¹ "
      "(x − y = −1 gives x = 2.5, y = 3.5).", secs=60)

assert 83 ** 2 == 6889 and 27 ** 3 == 19683 and 83 - 27 == 56
assert 87 ** 2 != 6889 and 87 - 27 == 60 and 83 - 37 == 46 and 83 + 27 == 110
Q(T, "Square and cube roots", I, QMARK + "√6,889 − ∛19,683 = ?",
  "56", ["60", "46", "110"],
  "Unit-digit method: a square ending in 9 has a root ending in 3 or 7; a cube ending in 3 has a cube root ending "
  "in 7",
  "6,889 lies between 80² = 6,400 and 90² = 8,100 and ends in 9, so its root is 83 or 87; 83² = 6,889. 19,683 lies "
  "between 20³ and 30³ and ends in 3, so its cube root ends in 7: 27³ = 19,683. 83 − 27 = 56.",
  ["√6,889: between 80 and 90, ends in 3 or 7; 83² = 6,889", "∛19,683: ends in 7; 27³ = 19,683", "83 − 27 = 56"],
  short="For the square root, 85² = 7,225 > 6,889, so the root is below 85: 83, not 87.",
  why="60 picks 87 as the square root (87² = 7,569); 46 takes the cube root as 37; 110 adds the two roots.", secs=55)

a_ = F(3, 4)
v = a_ ** 3 / (1 - a_) + (1 + a_ + a_ ** 2)
assert v == 4 and v == 1 / (1 - a_) and a_ ** 3 / (1 - a_) == F(27, 16) and 1 + a_ + a_ ** 2 == F(37, 16)
assert (F(9, 4) / F(1, 4)) + F(37, 16) == F(181, 16)
Q(T, "Fractions and decimals", I, QMARK + "(0.75)³ ÷ (1 − 0.75) + [1 + 0.75 + (0.75)²] = ?",
  "4", ["2.3125", "1.6875", "11.3125"],
  "1 + a + a² = (1 − a³)/(1 − a), so a³/(1 − a) + 1 + a + a² = 1/(1 − a)",
  "With a = 0.75: a³/(1 − a) + (1 − a³)/(1 − a) = 1/(1 − a) = 1/0.25 = 4. Directly: 0.421875 ÷ 0.25 = 1.6875 and "
  "1 + 0.75 + 0.5625 = 2.3125; 1.6875 + 2.3125 = 4.",
  ["(0.75)³ = 0.421875; ÷ 0.25 = 1.6875", "1 + 0.75 + 0.5625 = 2.3125", "1.6875 + 2.3125 = 4"],
  short="The whole expression equals 1/(1 − a) = 1/0.25 = 4.",
  why="2.3125 is only the bracket; 1.6875 is only the first term; 11.3125 cubes 0.75 by multiplying by 3 "
      "(2.25 ÷ 0.25 = 9, plus 2.3125).", secs=60)

ab = math.log(32) / math.log(4)
assert near(ab, 2.5) and near((math.log(5) / math.log(4)) * (math.log(32) / math.log(5)), 2.5)
Q(T, "Surds and indices", A, "If 4ᵃ = 5 and 5ᵇ = 32, what is the value of ab?",
  "5/2", ["5", "8", "2/5"],
  "Substitute one equation into the other: (4ᵃ)ᵇ = 4^(ab)",
  "5ᵇ = 32 and 5 = 4ᵃ, so (4ᵃ)ᵇ = 32, i.e. 4^(ab) = 32. Writing both as powers of 2: 2^(2ab) = 2⁵, so 2ab = 5 and "
  "ab = 5/2.",
  ["5 = 4ᵃ ⇒ 32 = 5ᵇ = 4^(ab)", "4^(ab) = 2^(2ab) and 32 = 2⁵", "2ab = 5 ⇒ ab = 5/2"],
  why="5 treats 4^(ab) as 2^(ab), forgetting that 4 = 2²; 8 divides 32 by 4 as if the exponents were factors; 2/5 "
      "inverts the result (it is the value of 1/(ab)).", secs=80)

v = sum(1 / (math.sqrt(k) + math.sqrt(k + 1)) for k in range(1, 100))
assert near(v, 9, 1e-9) and math.isqrt(100) - 1 == 9
Q(T, "Surds and indices", A, "Find the value of 1/(√1 + √2) + 1/(√2 + √3) + 1/(√3 + √4) + … + 1/(√99 + √100).",
  "9", ["10", "99", "11"],
  "Rationalise each term: 1/(√k + √(k + 1)) = √(k + 1) − √k, so the sum telescopes",
  "Each term equals √(k + 1) − √k. Adding them, (√2 − √1) + (√3 − √2) + … + (√100 − √99) = √100 − √1 = 10 − 1 = 9.",
  ["1/(√k + √(k+1)) = √(k+1) − √k", "All middle terms cancel", "√100 − √1 = 9"],
  why="10 forgets to subtract √1; 99 counts the terms instead of adding them; 11 adds √1 instead of subtracting it.",
  secs=75)

a_, b_, c_ = F("1.2"), F("0.8"), F("0.7")
num = a_ ** 3 + b_ ** 3 + c_ ** 3 - 3 * a_ * b_ * c_
den = a_ ** 2 + b_ ** 2 + c_ ** 2 - a_ * b_ - b_ * c_ - c_ * a_
assert num / den == F("2.7") and (a_ + b_ + c_) ** 2 == F("7.29") and 3 * a_ * b_ * c_ == F("2.016")
Q(T, "Fractions and decimals", A,
  "Find the value of [(1.2)³ + (0.8)³ + (0.7)³ − 3 × 1.2 × 0.8 × 0.7] ÷ [(1.2)² + (0.8)² + (0.7)² − 1.2 × 0.8 − "
  "0.8 × 0.7 − 0.7 × 1.2].",
  "2.7", ["7.29", "1", "2.016"],
  "a³ + b³ + c³ − 3abc = (a + b + c)(a² + b² + c² − ab − bc − ca)",
  "With a = 1.2, b = 0.8 and c = 0.7, the numerator is (a + b + c) times the denominator, so the value is "
  "a + b + c = 1.2 + 0.8 + 0.7 = 2.7.",
  ["Numerator = (a + b + c) × denominator", "Value = a + b + c", "= 2.7"],
  why="7.29 is (a + b + c)²; 1 assumes the numerator and denominator are equal; 2.016 is 3abc, one piece of the "
      "numerator.", secs=60)

v = sum(k ** 3 for k in range(13, 21))
assert v == 38016 and (20 * 21 // 2) ** 2 == 44100 and (12 * 13 // 2) ** 2 == 6084
assert 44100 - (13 * 14 // 2) ** 2 == 35819 and F(33, 2) ** 3 * 8 == F(287496, 8) and round(F(33, 2) ** 3 * 8) == 35937
Q(T, "Square and cube roots", A, "What is the value of 13³ + 14³ + 15³ + … + 20³?",
  "38,016", ["44,100", "35,819", "35,937"],
  "1³ + 2³ + … + n³ = [n(n + 1)/2]²; subtract the sum up to 12 from the sum up to 20",
  "Sum up to 20 = (20 × 21 ÷ 2)² = 210² = 44,100. Sum up to 12 = (12 × 13 ÷ 2)² = 78² = 6,084. Required sum = "
  "44,100 − 6,084 = 38,016.",
  ["Σ(1 to 20) k³ = 210² = 44,100", "Σ(1 to 12) k³ = 78² = 6,084", "44,100 − 6,084 = 38,016"],
  why="44,100 forgets to remove 1³ to 12³; 35,819 removes 1³ to 13³ (91² = 8,281), dropping 13³ as well; 35,937 "
      "multiplies the cube of the middle value 16.5 by 8, but cubes do not rise evenly.", secs=75)

# ================================================================ Approximation (B3 I10 A4)
T = "Approximation"
ex = 0.6498 * 1199.6 - 24.03 * 13.97
nearest(ex, [444, 780, 742, 468], 444)
assert 780 - 336 == 444 and 780 - 38 == 742 and 780 - 24 * 13 == 468
Q(T, "Percentage approximation", B, APPROX + "64.98% of 1,199.6 − 24.03 × 13.97 ≈ ?",
  "444", ["780", "742", "468"],
  "Round to 65%, 1,200, 24 and 14",
  "65% of 1,200 = 780 and 24 × 14 = 336. So the value ≈ 780 − 336 = 444.",
  ["65% of 1,200 = 780", "24 × 14 = 336", "780 − 336 = 444"],
  why="780 leaves out the product; 742 adds 24 and 14 instead of multiplying them; 468 cuts 13.97 down to 13 "
      "(24 × 13 = 312) instead of rounding it to 14.", secs=40)

ex = math.sqrt(1368.9) + 4095.7 ** (1 / 3) * 2.99
nearest(ex, [85, 159, 229, 53], 85)
assert 37 ** 2 == 1369 and 16 ** 3 == 4096 and 37 + 48 == 85 and (37 + 16) * 3 == 159 and 37 + 64 * 3 == 229
Q(T, "Root approximation", B, APPROX + "√1,368.9 + ∛4,095.7 × 2.99 ≈ ?",
  "85", ["159", "229", "53"],
  "1,369 = 37² and 4,096 = 16³; multiply before adding",
  "√1,369 = 37 and ∛4,096 = 16. Then 37 + 16 × 3 = 37 + 48 = 85.",
  ["√1,368.9 ≈ 37", "∛4,095.7 ≈ 16", "37 + 16 × 3 = 85"],
  why="159 adds before multiplying ((37 + 16) × 3); 229 takes the square root of 4,096 (64) instead of the cube root; "
      "53 forgets the × 3.", secs=40)

ex = 749.9 / 14.99 * 5.99 - 12.01 ** 2
nearest(ex, [156, 168, 444, -136], 156)
assert 300 - 144 == 156 and 300 - 132 == 168 and 300 + 144 == 444 and round(750 / 90 - 144) == -136
Q(T, "Mixed approximation", B, APPROX + "(749.9 ÷ 14.99) × 5.99 − 12.01² ≈ ?",
  "156", ["168", "444", "−136"],
  "750 ÷ 15 = 50; then × 6; 12² = 144",
  "749.9 ÷ 14.99 ≈ 750 ÷ 15 = 50; 50 × 6 = 300; 12.01² ≈ 144. So the value ≈ 300 − 144 = 156.",
  ["750 ÷ 15 = 50", "50 × 6 = 300", "300 − 144 = 156"],
  why="168 takes 12² as 12 × 11 = 132; 444 adds 144 instead of subtracting it; −136 divides 750 by 15 × 6 = 90 "
      "(ignoring the bracket) and gets 8.3 − 144.", secs=40)

ex = 7.98 * (17.03 * 8.97 - 0.3497 * 360.2)
nearest(ex, [216, 2232, 27, 360], 216)
assert 17 * 9 - 126 == 27 and 27 * 8 == 216 and (153 + 126) * 8 == 2232 and (153 - 108) * 8 == 360
Q(T, "Percentage approximation", I, APPROX + "(? ÷ 7.98) + 34.97% of 360.2 ≈ 17.03 × 8.97",
  "216", ["2,232", "27", "360"],
  "Round to 8, 35%, 360, 17 and 9; isolate ? ÷ 8",
  "35% of 360 = 126 and 17 × 9 = 153. So ? ÷ 8 ≈ 153 − 126 = 27, and ? ≈ 27 × 8 = 216.",
  ["35% of 360 = 126", "17 × 9 = 153", "? ÷ 8 = 27", "? = 216"],
  why="2,232 adds 126 to 153 instead of subtracting it; 27 stops at ? ÷ 8 and forgets to multiply by 8; 360 takes "
      "35% of 360 as 108 (30%).", secs=60)

ex = (12.97 ** 2 - 24.98) / 6.01
nearest(ex, [24, 144, 32, 138], 24)
assert (169 - 25) // 6 == 24 and 169 - 25 == 144 and round((169 + 25) / 6) == 32 and 169 - 25 - 6 == 138
Q(T, "Root approximation", I, APPROX + "√(? × 6.01 + 24.98) ≈ 12.97",
  "24", ["144", "32", "138"],
  "Square both sides first, then undo the + 25 and the × 6",
  "Squaring: ? × 6 + 25 ≈ 13² = 169. So ? × 6 ≈ 144 and ? ≈ 24.",
  ["? × 6 + 25 = 169", "? × 6 = 144", "? = 24"],
  why="144 forgets to divide by 6; 32 adds 25 to 169 instead of subtracting (194 ÷ 6); 138 reads × 6 as + 6 "
      "(169 − 25 − 6).", secs=60)

ex = (40.97 * 4.02 - 4199.7 / 5.98 / 6.99) ** (1 / 3)
nearest(ex, [4, 8, 16, 64], 4)
assert 4200 // 42 == 100 and 41 * 4 == 164 and 164 - 100 == 64 and 4 ** 3 == 64 and 8 ** 2 == 64 and 64 // 4 == 16
Q(T, "Mixed approximation", I, APPROX + "4,199.7 ÷ 5.98 ÷ 6.99 + ?³ ≈ 40.97 × 4.02",
  "4", ["8", "16", "64"],
  "4,200 ÷ 6 ÷ 7 = 100 and 41 × 4 = 164",
  "Left side: 4,200 ÷ 6 ÷ 7 = 100. Right side: 41 × 4 = 164. So ?³ ≈ 64 and ? ≈ 4.",
  ["4,200 ÷ 6 ÷ 7 = 100", "41 × 4 = 164", "?³ = 64", "? = 4"],
  why="8 takes the square root of 64 instead of the cube root; 16 reads ?³ as 4 × ? and divides 64 by 4; "
      "64 stops at ?³ and forgets to take the cube root.", secs=60)

ex = (0.375 * 1279.7 - 11.98 ** 2) / 8.02
nearest(ex, [42, 462, 336, 57], 42)
assert F(3, 8) * 1280 == 480 and (480 - 144) // 8 == 42 and 480 - 144 // 8 == 462 and (480 - 24) // 8 == 57
Q(T, "Percentage approximation", I, APPROX + "(37.5% of 1,279.7 − 11.98²) ÷ 8.02 ≈ ?",
  "42", ["462", "336", "57"],
  "37.5% = 3/8; work the bracket fully before dividing",
  "37.5% of 1,280 = 3/8 × 1,280 = 480. 12² = 144. (480 − 144) ÷ 8 = 336 ÷ 8 = 42.",
  ["3/8 × 1,280 = 480", "480 − 144 = 336", "336 ÷ 8 = 42"],
  why="462 divides only 144 by 8 (480 − 18), ignoring the bracket; 336 forgets the ÷ 8; 57 takes 12² as 12 × 2 = 24.",
  secs=60)

ex = ((13.98 * 6.02 + 41.97) / math.sqrt(195.9)) ** 3
nearest(ex, [729, 81, 9, 27], 729)
assert 14 * 6 + 42 == 126 and 126 // 14 == 9 and 9 ** 3 == 729 and 9 ** 2 == 81 and 42 // 14 == 3 and 3 ** 3 == 27
Q(T, "Root approximation", I, APPROX + "∛? × √195.9 ≈ 13.98 × 6.02 + 41.97",
  "729", ["81", "9", "27"],
  "√196 = 14; then cube the value of ∛?",
  "Right side ≈ 14 × 6 + 42 = 126. √195.9 ≈ 14, so ∛? ≈ 126 ÷ 14 = 9 and ? ≈ 9³ = 729.",
  ["14 × 6 + 42 = 126", "∛? = 126 ÷ 14 = 9", "? = 9³ = 729"],
  why="81 squares 9 instead of cubing it; 9 stops at ∛?; 27 divides only the 42 by 14 (∛? = 3) and cubes that.",
  secs=60)

ex = 3.01 ** 4 - 4.02 ** 3 + math.sqrt(1520.9)
nearest(ex, [56, 184, 17, 108], 56)
assert 39 ** 2 == 1521 and 81 - 64 + 39 == 56 and 81 + 64 + 39 == 184 and 81 - 64 == 17 and 81 - 12 + 39 == 108
Q(T, "Mixed approximation", I, APPROX + "3.01⁴ − 4.02³ + √1,520.9 ≈ ?",
  "56", ["184", "17", "108"],
  "3⁴ = 81, 4³ = 64 and 1,521 = 39²",
  "3.01⁴ ≈ 81, 4.02³ ≈ 64 and √1,520.9 ≈ 39. So 81 − 64 + 39 = 56.",
  ["3⁴ = 81", "4³ = 64", "√1,521 = 39", "81 − 64 + 39 = 56"],
  why="184 adds 4³ instead of subtracting it; 17 leaves out the square root; 108 takes 4³ as 4 × 3 = 12.", secs=55)

ex = 59.98 * 7.02 / 4.98 - 23.97
nearest(ex, [60, 84, 19, 108], 60)
assert F(60 * 7, 5) == 84 and 84 - 24 == 60 and round(60 * 5 / 7 - 24) == 19 and 84 + 24 == 108
Q(T, "Mixed approximation", I, APPROX + "(? + 23.97) : 59.98 ≈ 7.02 : 4.98",
  "60", ["84", "19", "108"],
  "Round to (? + 24) : 60 = 7 : 5 and cross-multiply",
  "(? + 24)/60 = 7/5, so ? + 24 = 60 × 7 ÷ 5 = 84 and ? = 84 − 24 = 60.",
  ["(? + 24) ÷ 60 = 7 ÷ 5", "? + 24 = 84", "? = 60"],
  why="84 forgets to subtract 24; 19 inverts the ratio (60 × 5 ÷ 7 ≈ 43, minus 24); 108 adds 24 instead of "
      "subtracting it.", secs=60)

ex = (2099.6 / 6.99) / (0.4495 - 0.1504)
nearest(ex, [1000, 500, 667, 90], 1000)
assert F(2100, 7) == 300 and F(300) / F(30, 100) == 1000 and F(300) / F(60, 100) == 500 and round(300 / 0.45) == 667
assert 300 * F(30, 100) == 90
Q(T, "Percentage approximation", I, APPROX + "44.95% of ? − 15.04% of ? ≈ 2,099.6 ÷ 6.99",
  "1,000", ["500", "667", "90"],
  "Both terms are percentages of the same ?, so combine them: 45% − 15% = 30% of ?",
  "2,100 ÷ 7 = 300. 45% of ? − 15% of ? = 30% of ?, so 30% of ? ≈ 300 and ? ≈ 1,000.",
  ["2,100 ÷ 7 = 300", "45% − 15% = 30%", "30% of ? = 300 ⇒ ? = 1,000"],
  why="500 adds the two percentages (60% of ? = 300); 667 uses only the 45% term; 90 multiplies 300 by 30% instead "
      "of dividing.", secs=60)

ex = (math.sqrt(168.9) - 3.98) ** 2
nearest(ex, [81, 9, 153, 289], 81)
assert (13 - 4) ** 2 == 81 and 169 - 16 == 153 and (13 + 4) ** 2 == 289
Q(T, "Root approximation", I, APPROX + "(√? + 3.98)² ≈ 168.9",
  "81", ["9", "153", "289"],
  "Take the square root of both sides first: √? + 4 ≈ 13",
  "√168.9 ≈ 13, so √? + 4 ≈ 13, √? ≈ 9 and ? ≈ 81.",
  ["√? + 4 = 13", "√? = 9", "? = 81"],
  why="9 stops at √?; 153 expands (√? + 4)² as ? + 16, missing the middle term (169 − 16); 289 adds 4 to 13 "
      "instead of subtracting (17²).", secs=55)

ex = 0.0049 * 2000.3 + 0.24 / 0.0599
nearest(ex, [14, 102, 10, 50], 14)
assert F("0.0049") * 2000 == F("9.8") and F("0.24") / F("0.06") == 4 and F("0.049") * 2000 + 4 == 102
assert F("9.8") + F("0.24") / F("0.6") == F("10.2") and F("9.8") + 40 == F("49.8")
Q(T, "Mixed approximation", I, APPROX + "0.0049 × 2,000.3 + 0.24 ÷ 0.0599 ≈ ?",
  "14", ["102", "10", "50"],
  "Count the decimal places carefully: 0.0049 × 2,000 = 9.8 and 0.24 ÷ 0.06 = 4",
  "0.0049 × 2,000 = 9.8 and 0.24 ÷ 0.06 = 24 ÷ 6 = 4. So the value ≈ 9.8 + 4 = 13.8 ≈ 14.",
  ["0.0049 × 2,000 = 9.8", "0.24 ÷ 0.06 = 4", "9.8 + 4 ≈ 14"],
  why="102 treats 0.0049 as 0.049 (98 + 4); 10 divides 0.24 by 0.6 instead of 0.06 (9.8 + 0.4); 50 divides by 0.006 "
      "(9.8 + 40).", secs=55)

ex = 249.9 / (6.402 + 3.598)
nearest(ex, [25, 12.5, 39, 2.5], 25)
assert F(250, 10) == 25 and F(250, 20) == F(25, 2) and round(250 / 6.4) == 39 and F(250, 100) == F(5, 2)
Q(T, "Percentage approximation", A, APPROX + "?% of 640.2 + ?% of 359.8 ≈ 249.9",
  "25", ["12.5", "39", "2.5"],
  "Both terms use the same ?%, so ?% × (640 + 360) = ?% of 1,000",
  "?% of 640 + ?% of 360 = ?% of 1,000 = 10 × ?. So 10 × ? ≈ 250 and ? ≈ 25.",
  ["640.2 + 359.8 = 1,000", "?% of 1,000 = 10 × ?", "10 × ? = 250 ⇒ ? = 25"],
  why="12.5 counts ? twice (20 × ? = 250); 39 uses only the 640 term (250 ÷ 6.4); 2.5 divides 250 by 100 instead "
      "of by 10.", secs=70)

ex = (math.sqrt(16.03) + 1.01) ** 3 + 7.02
nearest(ex, [132, 118, 32, 125], 132)
assert (4 + 1) ** 3 + 7 == 132 and 125 - 7 == 118 and 25 + 7 == 32
Q(T, "Root approximation", A, APPROX + "∛(? − 7.02) ≈ √16.03 + 1.01",
  "132", ["118", "32", "125"],
  "√16 = 4, so the cube root is about 5; cube it, then add back the 7",
  "√16.03 + 1.01 ≈ 4 + 1 = 5. So ? − 7 ≈ 5³ = 125 and ? ≈ 132.",
  ["Right side ≈ 5", "? − 7 = 125", "? = 132"],
  why="118 subtracts 7 from 125 instead of adding it; 32 squares 5 instead of cubing it (25 + 7); 125 forgets to add "
      "back the 7.", secs=70)

ex = math.sqrt(2808.9) * 2196.4 ** (1 / 3) / (0.3497 * 220.3 - 23.98)
nearest(ex, [13, 53, 7, 689], 13)
assert 53 ** 2 == 2809 and 13 ** 3 == 2197 and 53 * 13 == 689 and F(35, 100) * 220 == 77 and 77 - 24 == 53
assert round(689 / 101) == 7
Q(T, "Mixed approximation", A, APPROX + "(√2,808.9 × ∛2,196.4) ÷ ? ≈ 34.97% of 220.3 − 23.98",
  "13", ["53", "7", "689"],
  "2,809 = 53² and 2,197 = 13³; 35% of 220 = 77",
  "Left numerator ≈ 53 × 13 = 689. Right side ≈ 77 − 24 = 53. So 689 ÷ ? ≈ 53 and ? ≈ 689 ÷ 53 = 13.",
  ["√2,809 = 53, ∛2,197 = 13", "53 × 13 = 689", "Right side = 77 − 24 = 53", "? = 689 ÷ 53 = 13"],
  why="53 is the value of the right side, not of ?; 7 adds 24 to 77 instead of subtracting (689 ÷ 101); 689 forgets "
      "to divide by the right side.", secs=80)

ex = 7999.6 * 1.0499 ** 3
nearest(ex, [9261, 9200, 8820, 9724], 9261)
assert F(8000) * F(21, 20) ** 3 == 9261 and 8000 * F(115, 100) == 9200 and F(8000) * F(21, 20) ** 2 == 8820
assert round(F(8000) * F(21, 20) ** 4) == 9724
Q(T, "Percentage approximation", A, APPROX + "7,999.6 × (1.0499)³ ≈ ?",
  "9,261", ["9,200", "8,820", "9,724"],
  "1.05 = 21/20, so 8,000 × (21/20)³ = 21³ = 9,261",
  "7,999.6 ≈ 8,000 and 1.0499 ≈ 1.05 = 21/20. 8,000 × (21/20)³ = 8,000 × 9,261 ÷ 8,000 = 9,261.",
  ["8,000 = 20³", "(21/20)³ × 20³ = 21³", "21³ = 9,261"],
  short="This is ₹8,000 compounded at 5% for 3 years: 8,000 → 8,400 → 8,820 → 9,261.",
  why="9,200 adds 5% three times without compounding (15%); 8,820 compounds for only two years; 9,724 compounds for "
      "four years.", secs=70)

# ================================================================ Number Series (B7 I2 A2)
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


def series_q(sub, diff, full, qpos, wrong, concept, expl, steps, short=None, why=None, secs=None):
    """Missing-term series: the full regenerated series, the position shown as '?', three wrong options."""
    shown = [None if k == qpos else t for k, t in enumerate(full)]
    ans = full[qpos]
    rival_rules_missing(shown, [ans, *wrong], ans)
    head = SERIES_Q if qpos == len(full) - 1 else MISSING_Q
    Q(T, sub, diff, head + series_text(shown), N(ans), [N(w) for w in wrong], concept, expl, steps, short, why,
      secs, by=BRUTE)


s = series_from(31, lambda t, k: t + 2 ** k, 7)
assert s == [31, 33, 37, 45, 61, 93, 157] and diffs(s) == [2, 4, 8, 16, 32, 64]
series_q("Pattern: differences", B, s, 6, [125, 141, 186],
         "The differences double each time: 2, 4, 8, 16, 32, …",
         "31 + 2 = 33, 33 + 4 = 37, 37 + 8 = 45, 45 + 16 = 61, 61 + 32 = 93. The next difference is 64, so the term "
         "is 93 + 64 = 157.",
         ["Differences: 2, 4, 8, 16, 32", "Next difference: 64", "93 + 64 = 157"],
         why="125 repeats the last difference (93 + 32); 141 adds 48, taking the next difference as 32 + 16; 186 "
             "doubles the term instead of the difference.", secs=35)

s = series_from(2, lambda t, k: 3 * t - (2 * k - 1), 6)
assert s == [2, 5, 12, 31, 86, 249] and 86 * 3 - 7 == 251 and 86 * 3 == 258 and 86 * 2 == 172
series_q("Pattern: multiply-add", B, s, 5, [251, 258, 172],
         "Each term is 3 times the previous term minus 1, 3, 5, 7, … (the odd numbers)",
         "2 × 3 − 1 = 5, 5 × 3 − 3 = 12, 12 × 3 − 5 = 31, 31 × 3 − 7 = 86. Next: 86 × 3 − 9 = 249.",
         ["× 3 − 1, × 3 − 3, × 3 − 5, × 3 − 7", "Next: × 3 − 9", "86 × 3 − 9 = 249"],
         why="251 subtracts 7 again instead of 9; 258 multiplies by 3 and subtracts nothing; 172 doubles 86 instead of "
             "tripling it.", secs=45)

s = [n ** 3 - 1 for n in range(1, 7)]
assert s == [0, 7, 26, 63, 124, 215] and 6 ** 3 == 216 and 124 + 61 == 185
series_q("Pattern: squares and cubes", B, s, 5, [216, 217, 185],
         "Each term is one less than a perfect cube: n³ − 1 for n = 1, 2, 3, …",
         "0 = 1³ − 1, 7 = 2³ − 1, 26 = 3³ − 1, 63 = 4³ − 1, 124 = 5³ − 1. Next: 6³ − 1 = 215.",
         ["1³ − 1, 2³ − 1, 3³ − 1, 4³ − 1, 5³ − 1", "Next n = 6", "216 − 1 = 215"],
         why="216 is 6³ without subtracting 1; 217 adds 1 instead of subtracting it; 185 repeats the last difference "
             "(124 + 61).", secs=35)

s = series_from(1000, lambda t, k: t - 20 * k, 6)
assert s == [1000, 980, 940, 880, 800, 700] and 880 - 60 == 820 and 880 - 100 == 780 and (880 + 700) // 2 == 790
series_q("Missing number series", B, s, 4, [820, 780, 790],
         "The amounts subtracted rise by 20 each time: 20, 40, 60, 80, 100",
         "1,000 − 20 = 980, 980 − 40 = 940, 940 − 60 = 880, 880 − 80 = 800, 800 − 100 = 700. The missing term is 800.",
         ["Differences: −20, −40, −60", "Next: −80 ⇒ 880 − 80 = 800", "Check: 800 − 100 = 700 ✓"],
         why="820 subtracts 60 again; 780 subtracts 100, skipping 80 (and then 780 − 100 ≠ 700); 790 takes the "
             "midpoint of 880 and 700, which makes the two gaps equal (90 and 90).", secs=35)

s = [13]
for k in range(5):
    s.append(s[-1] * (2 if k % 2 == 0 else F(3, 2)))
assert s == [13, 26, 39, 78, 117, 234] and 78 * 2 == 156 and 78 * F(5, 2) == 195 and 78 + 26 == 104
series_q("Missing number series", B, s, 4, [156, 195, 104],
         "The multipliers alternate: × 2, × 1.5, × 2, × 1.5, …",
         "13 × 2 = 26, 26 × 1.5 = 39, 39 × 2 = 78, 78 × 1.5 = 117, 117 × 2 = 234. The missing term is 117.",
         ["× 2: 13 → 26", "× 1.5: 26 → 39", "× 2: 39 → 78", "× 1.5: 78 → 117", "Check: 117 × 2 = 234 ✓"],
         why="156 doubles 78 again (and 156 × 2 = 312, not 234); 195 multiplies by 2.5, reading the multipliers as "
             "rising (and 195 × 2 ≠ 234); 104 adds 26 "
             "(and 104 × 2 = 208, not 234).", secs=40)

s = series_from(2, lambda t, k: t + k * k + 1, 6)
assert s == [2, 4, 9, 19, 36, 62] and diffs(s) == [2, 5, 10, 17, 26] and 36 + 24 == 60 and 36 + 25 == 61
assert 36 + 2 * 17 == 70
series_q("Pattern: differences", B, s, 5, [60, 61, 70],
         "The differences are one more than the perfect squares: 1 + 1, 4 + 1, 9 + 1, 16 + 1, …",
         "Differences: 2, 5, 10, 17, i.e. 1² + 1, 2² + 1, 3² + 1, 4² + 1. The next difference is 5² + 1 = 26, so "
         "the term is 36 + 26 = 62.",
         ["Differences: 2, 5, 10, 17", "= n² + 1 for n = 1 to 4", "Next: 26 ⇒ 36 + 26 = 62"],
         short="The differences 2, 5, 10, 17 themselves rise by 3, 5, 7, so the next rise is 9: 17 + 9 = 26.",
         why="60 keeps the rise of the differences at 7 (17 + 7 = 24); 61 adds 5² = 25 and forgets the + 1; 70 doubles "
             "the last difference (36 + 34).", secs=40)

s = series_from(2, lambda t, k: t * (k + 1), 6)
assert s == [2, 4, 12, 48, 240, 1440] and 48 * 4 == 192 and 48 * 2 == 96 and 48 * 6 == 288
series_q("Missing number series", B, s, 4, [192, 96, 288],
         "The multipliers rise by 1 each time: × 2, × 3, × 4, × 5, × 6",
         "2 × 2 = 4, 4 × 3 = 12, 12 × 4 = 48, 48 × 5 = 240, 240 × 6 = 1,440. The missing term is 240.",
         ["× 2, × 3, × 4", "48 × 5 = 240", "Check: 240 × 6 = 1,440 ✓"],
         why="192 multiplies by 4 again (and 192 × 6 ≠ 1,440); 96 doubles 48; 288 multiplies by 6, skipping 5 (and "
             "288 × 6 ≠ 1,440).", secs=40)

s = [n ** 3 + (n + 1) ** 3 for n in range(0, 6)]
assert s == [1, 9, 35, 91, 189, 341] and 7 ** 3 == 343 and 189 + 98 + 42 == 329 and 6 ** 3 == 216
series_q("Pattern: squares and cubes", I, s, 5, [343, 329, 216],
         "Each term is the sum of two consecutive cubes: 0³ + 1³, 1³ + 2³, 2³ + 3³, …",
         "1 = 0 + 1, 9 = 1 + 8, 35 = 8 + 27, 91 = 27 + 64, 189 = 64 + 125. Next: 125 + 216 = 341.",
         ["1³ + 2³ = 9", "2³ + 3³ = 35", "3³ + 4³ = 91", "4³ + 5³ = 189", "5³ + 6³ = 341"],
         short="Differences 8, 26, 56, 98 have second differences 18, 30, 42, rising by 12; next 54, so the next "
               "difference is 152.",
         why="343 takes the terms to be cubes (7³); 329 keeps the second difference at 42 (98 + 42 = 140); 216 gives "
             "only 6³, missing the 5³ that is added to it.", secs=60)

s = [2, 3]
while len(s) < 7:
    s.append(s[-1] + 2 * s[-2])
assert s == [2, 3, 7, 13, 27, 53, 107] and 13 * 2 == 26 and 13 * 2 - 1 == 25 and 13 + 7 == 20
series_q("Missing number series", I, s, 4, [26, 25, 20],
         "From the third term on, each term is the previous term plus twice the term before it",
         "7 = 3 + 2 × 2, 13 = 7 + 2 × 3, ? = 13 + 2 × 7 = 27. Check: 27 + 2 × 13 = 53 and 53 + 2 × 27 = 107.",
         ["7 = 3 + 2 × 2", "13 = 7 + 2 × 3", "? = 13 + 2 × 7 = 27", "Check: 27 + 26 = 53 ✓, 53 + 54 = 107 ✓"],
         short="Equivalently the terms go × 2 − 1, × 2 + 1, × 2 − 1, …: 13 × 2 + 1 = 27.",
         why="26 doubles 13 but drops the alternating + 1; 25 subtracts 1 where 1 should be added (13 × 2 − 1); 20 adds "
             "the term before only once (13 + 7) instead of twice.", secs=60)

s = series_from(1, lambda t, k: t * k + k * k, 6)
assert s == [1, 2, 8, 33, 148, 765] and 148 * 5 + 16 == 756 and 148 * 5 == 740 and 148 * 5 + 5 == 745
series_q("Pattern: multiply-add", A, s, 5, [756, 740, 745],
         "Each term is (previous term × n) + n² for n = 1, 2, 3, …",
         "1 × 1 + 1 = 2, 2 × 2 + 4 = 8, 8 × 3 + 9 = 33, 33 × 4 + 16 = 148. Next: 148 × 5 + 25 = 765.",
         ["× 1 + 1², × 2 + 2², × 3 + 3², × 4 + 4²", "Next: × 5 + 5²", "148 × 5 + 25 = 765"],
         why="756 adds 4² again instead of 5²; 740 multiplies by 5 and adds nothing; 745 adds 5 instead of 5².",
         secs=90)

s = series_from(2, lambda t, k: t * (k + 1) - 1, 6)
assert s == [2, 3, 8, 31, 154, 923] and 8 * 4 == 32 and 8 * 4 + 1 == 33 and 8 * 3 == 24
series_q("Missing number series", A, s, 3, [32, 33, 24],
         "Each term is (previous term × 2, 3, 4, 5, 6) − 1",
         "2 × 2 − 1 = 3, 3 × 3 − 1 = 8, 8 × 4 − 1 = 31, 31 × 5 − 1 = 154, 154 × 6 − 1 = 923. The missing term is 31.",
         ["× 2 − 1, × 3 − 1", "8 × 4 − 1 = 31", "Check: 31 × 5 − 1 = 154 ✓, 154 × 6 − 1 = 923 ✓"],
         why="32 multiplies by 4 but forgets the − 1 (and 32 × 5 − 1 = 159); 33 adds 1 instead of subtracting it; 24 "
             "multiplies by 3 again.", secs=80)

# ================================================================ Wrong Number Series (B2 I1 A1)
T = "Wrong Number Series"
WRONG_Q = "Find the wrong number in the series:\n"


def wrong_q(sub, diff, good, shown, opt_pos, concept, expl, steps, why, secs):
    bad = [k for k, (a, b) in enumerate(zip(good, shown)) if a != b]
    assert len(bad) == 1 and bad[0] in opt_pos and len(opt_pos) == 4, (good, shown)
    rival_rules_wrong(shown, bad[0], good[bad[0]], opt_pos)
    ans = N(shown[bad[0]])
    wrong = [N(shown[k]) for k in opt_pos if k != bad[0]]
    Q(T, sub, diff, WRONG_Q + series_text(shown), ans, wrong, concept, expl, steps, None, why, secs, by=BRUTE)


good = series_from(7, lambda t, k: t * (k + 1), 7)
shown = [7, 14, 42, 168, 840, 5050, 35280]
assert good == [7, 14, 42, 168, 840, 5040, 35280]
wrong_q("Find the wrong term", B, good, shown, [2, 4, 5, 6],
        "The multipliers rise by 1: × 2, × 3, × 4, × 5, × 6, × 7",
        "7 × 2 = 14, 14 × 3 = 42, 42 × 4 = 168, 168 × 5 = 840, 840 × 6 = 5,040, 5,040 × 7 = 35,280. The sixth term "
        "should be 5,040, not 5,050.",
        ["× 2, × 3, × 4, × 5", "840 × 6 = 5,040 ≠ 5,050", "5,040 × 7 = 35,280 ✓"],
        why="42, 840 and 35,280 all fit; 35,280 confirms 5,040, since 5,050 × 7 = 35,350.", secs=40)

good = [10]
for k in range(6):
    good.append(good[-1] + (5 if k % 2 == 0 else -2))
shown = [10, 15, 13, 18, 16, 21, 20]
assert good == [10, 15, 13, 18, 16, 21, 19]
wrong_q("Find the wrong term", B, good, shown, [1, 3, 5, 6],
        "The steps alternate: + 5, − 2, + 5, − 2, …",
        "10 + 5 = 15, 15 − 2 = 13, 13 + 5 = 18, 18 − 2 = 16, 16 + 5 = 21, 21 − 2 = 19. The last term should be 19, "
        "not 20.",
        ["+ 5, − 2 repeated", "21 − 2 = 19 ≠ 20", "Odd places 10, 13, 16, 19 rise by 3"],
        why="15, 18 and 21 fit the + 5 steps; only 20 breaks the pattern (21 − 1).", secs=35)

good = series_from(5, lambda t, k: 2 * t + (2 * k - 1), 7)
shown = [5, 11, 25, 56, 117, 243, 497]
assert good == [5, 11, 25, 55, 117, 243, 497]
wrong_q("Find the wrong term", I, good, shown, [2, 3, 4, 5],
        "Each term is twice the previous term plus 1, 3, 5, 7, … (the odd numbers)",
        "5 × 2 + 1 = 11, 11 × 2 + 3 = 25, 25 × 2 + 5 = 55, 55 × 2 + 7 = 117, 117 × 2 + 9 = 243, 243 × 2 + 11 = 497. "
        "The fourth term should be 55, not 56.",
        ["× 2 + 1, × 2 + 3", "25 × 2 + 5 = 55 ≠ 56", "55 × 2 + 7 = 117 ✓"],
        why="25, 117 and 243 fit; 117 confirms 55, since 56 × 2 + 7 = 119.", secs=55)

good = [1, 1]
while len(good) < 7:
    good.append(2 * good[-1] + good[-2])
shown = [1, 1, 3, 7, 17, 43, 99]
assert good == [1, 1, 3, 7, 17, 41, 99]
wrong_q("Find the wrong term", A, good, shown, [3, 4, 5, 6],
        "From the third term on, each term is twice the previous term plus the term before that",
        "3 = 2 × 1 + 1, 7 = 2 × 3 + 1, 17 = 2 × 7 + 3, 41 = 2 × 17 + 7, 99 = 2 × 41 + 17. The sixth term should be 41, "
        "not 43.",
        ["3 = 2 × 1 + 1", "7 = 2 × 3 + 1, 17 = 2 × 7 + 3", "2 × 17 + 7 = 41 ≠ 43", "2 × 41 + 17 = 99 ✓"],
        why="7, 17 and 99 fit; 99 confirms 41, since 2 × 43 + 17 = 103.", secs=90)

# ================================================================ Quadratic Equations (B2 I3 A3)
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


xs, ys = [F(9), F(11)], [F(12), F(13)]
roots_check(1, -20, 99, xs), roots_check(1, -25, 156, ys)
qe("Relation between roots", B, "Solve both equations and choose the relation between x and y that holds for every "
   "pair of roots.", "x² − 20x + 99 = 0", "y² − 25y + 156 = 0", xs, ys, "<", [">", ">="],
   "Factorise: find two numbers with the given sum and product",
   "I: 9 + 11 = 20 and 9 × 11 = 99, so x = 9 or 11. II: 12 + 13 = 25 and 12 × 13 = 156, so y = 12 or 13. The "
   "largest x (11) is below the smallest y (12), so x < y.",
   ["I: (x − 9)(x − 11) = 0", "II: (y − 12)(y − 13) = 0", "max x = 11 < min y = 12"],
   why="x > y and x ≥ y reverse the comparison: every root of I is smaller than every root of II.", secs=40)

xs, ys = [F(5), F(-9)], [F(5)]
roots_check(1, 4, -45, xs), roots_check(1, -10, 25, ys)
qe("Relation between roots", B, "Find the roots of I and II and decide how x is related to y.",
   "x² + 4x − 45 = 0", "y² − 10y + 25 = 0", xs, ys, "<=", ["<", ">="],
   "Equation II is a perfect square, so it has one repeated root",
   "I: (x + 9)(x − 5) = 0, so x = 5 or −9. II: (y − 5)² = 0, so y = 5 only. x = 5 equals y and x = −9 is less than "
   "y, so x ≤ y.",
   ["I: x = 5, −9", "II: (y − 5)² = 0 ⇒ y = 5", "5 = 5 and −9 < 5 ⇒ x ≤ y"],
   why="x < y fails for x = 5 = y; x ≥ y fails for x = −9.", secs=45)

xs, ys = [F(5), F(-7, 3)], [F(7, 2), F(3)]
roots_check(3, -8, -35, xs), roots_check(2, -13, 21, ys)
qe("Relation between roots", I, "Solve the two equations and choose the relation between x and y, if any, that holds "
   "for all their roots.", "3x² − 8x − 35 = 0", "2y² − 13y + 21 = 0", xs, ys, "cbe", [">", "<="],
   "Split the middle term: −8x = −15x + 7x and −13y = −7y − 6y",
   "I: 3x² − 15x + 7x − 35 = (3x + 7)(x − 5) = 0, so x = 5 or −7/3. II: 2y² − 7y − 6y + 21 = (2y − 7)(y − 3) = 0, "
   "so y = 3.5 or 3. x = 5 is greater than both values of y, but x = −2.33 is smaller than both, so no single "
   "relation holds.",
   ["I: (3x + 7)(x − 5) = 0 ⇒ x = 5, −2.33", "II: (2y − 7)(y − 3) = 0 ⇒ y = 3.5, 3", "5 > y but −2.33 < y",
    "Relationship cannot be established"],
   why="x > y and x ≥ y fail for x = −7/3 (a sign slip that reads the root as +7/3 makes them look true); x ≤ y and "
       "x < y fail for x = 5.", secs=70)

xs, ys = [F(8)], [F(8), F(9)]
assert 5 * (8 - 2) == 2 * (8 + 7)
roots_check(1, -17, 72, ys)
qe("Linear vs quadratic", I, "Equation I is linear and equation II is quadratic. Solve both and choose the relation "
   "between x and y.", "5(x − 2) = 2(x + 7)", "y² − 17y + 72 = 0", xs, ys, "<=", ["<", ">"],
   "Solve the linear equation fully before comparing; a shared value makes the relation non-strict",
   "I: 5x − 10 = 2x + 14, so 3x = 24 and x = 8. II: (y − 8)(y − 9) = 0, so y = 8 or 9. x = 8 equals one root and is "
   "less than the other, so x ≤ y.",
   ["I: 3x = 24 ⇒ x = 8", "II: y = 8, 9", "8 = 8 and 8 < 9 ⇒ x ≤ y"],
   why="x < y overlooks that x = 8 equals the root y = 8; x > y reverses the comparison of 8 with 9.", secs=55)

xs, ys = [F(30)], [F(25), F(26)]
assert F(30, 3) + F(30, 5) == 16
roots_check(1, -51, 650, ys)
qe("Linear vs quadratic", I, "Solve the linear equation I and the quadratic equation II and state the relation "
   "between x and y.", "x/3 + x/5 = 16", "y² − 51y + 650 = 0", xs, ys, ">", ["<", "<="],
   "Clear the fractions in I with the LCM 15",
   "I: (5x + 3x)/15 = 16, so 8x = 240 and x = 30. II: 25 + 26 = 51 and 25 × 26 = 650, so y = 25 or 26. x = 30 is "
   "greater than both, so x > y.",
   ["I: 8x/15 = 16 ⇒ x = 30", "II: (y − 25)(y − 26) = 0", "30 > 26 > 25"],
   why="x < y and x ≤ y come from clearing the fractions wrongly: 8x = 16 (forgetting to multiply 16 by 15) "
       "gives x = 2, below both roots of II.", secs=55)

xs = [F(9), F(16)]
for x in xs:
    r_ = math.isqrt(int(x))
    assert x - 7 * r_ + 12 == 0
ys = [F(16), F(17)]
roots_check(1, -33, 272, ys)
qe("Relation between roots", A, "Equation I contains √x (the non-negative square root of x). Find every x and y and "
   "choose the relation between them.", "x − 7√x + 12 = 0", "y² − 33y + 272 = 0", xs, ys, "<=", ["<", ">="],
   "Treat I as a quadratic in √x: (√x)² − 7√x + 12 = 0",
   "I: (√x − 3)(√x − 4) = 0, so √x = 3 or 4 and x = 9 or 16. II: 16 + 17 = 33 and 16 × 17 = 272, so y = 16 or 17. "
   "x = 16 equals y = 16 and every other pair has x < y. So x ≤ y.",
   ["I: √x = 3 or 4 ⇒ x = 9, 16", "II: y = 16, 17", "Common value 16 ⇒ x ≤ y"],
   why="x < y misses the shared value 16 (it also follows from stopping at √x = 3, 4 without squaring); x ≥ y "
       "fails for x = 9.", secs=85)

xs, ys = [F(1), F(2), F(3)], [F(4), F(5)]
for x in xs:
    assert x ** 3 - 6 * x ** 2 + 11 * x - 6 == 0
roots_check(1, -9, 20, ys)
qe("Relation between roots", A, "Equation I is a cubic. Find all its real roots and the roots of II, then choose the "
   "relation between x and y.", "x³ − 6x² + 11x − 6 = 0", "y² − 9y + 20 = 0", xs, ys, "<", [">", ">="],
   "Try small integers: x = 1 makes the cubic zero, so (x − 1) is a factor",
   "x = 1 gives 1 − 6 + 11 − 6 = 0, so x³ − 6x² + 11x − 6 = (x − 1)(x² − 5x + 6) = (x − 1)(x − 2)(x − 3). So x = 1, "
   "2 or 3. II: (y − 4)(y − 5) = 0, so y = 4 or 5. The largest x (3) is below the smallest y (4), so x < y.",
   ["x = 1 is a root", "Cubic = (x − 1)(x − 2)(x − 3)", "II: y = 4, 5", "max x = 3 < min y = 4"],
   why="x > y and x ≥ y reverse the comparison: even the largest root of I (3) is below the smallest root of II "
       "(4).", secs=85)

r2_ = math.sqrt(2)
xs_f = [r2_, -3 * r2_]
for x in xs_f:
    assert near(x * x + 2 * r2_ * x - 6, 0)
ys = [F(3), F(-1)]
roots_check(1, -2, -3, ys)
assert all(x < 3 for x in xs_f) and xs_f[0] > -1 and xs_f[1] < -1
qe("Relation between roots", A, "Equation I has an irrational coefficient (√2 ≈ 1.414). Solve both equations and "
   "choose the relation between x and y, if any, that holds for all roots.", "x² + 2√2x − 6 = 0",
   "y² − 2y − 3 = 0", [F(1414, 1000), F(-4243, 1000)], ys, "cbe", ["<", ">="],
   "Look for factors of the form (x + a√2)(x − b√2) with ab × 2 = 6 and (a − b)√2 = 2√2",
   "I: (x + 3√2)(x − √2) = 0, since 3√2 × √2 = 6 and 3√2 − √2 = 2√2. So x = √2 ≈ 1.41 or −3√2 ≈ −4.24. II: "
   "(y − 3)(y + 1) = 0, so y = 3 or −1. x = 1.41 is less than 3 but greater than −1, so no relation holds.",
   ["I: (x + 3√2)(x − √2) = 0 ⇒ x ≈ 1.41, −4.24", "II: y = 3, −1", "1.41 < 3 but 1.41 > −1",
    "Relationship cannot be established"],
   why="x < y fails for x = 1.41, y = −1; x ≥ y fails for x = −4.24; x > y and x ≤ y fail for the same pairs.",
   secs=90)

# ================================================================ Number System (B2 I2 A1)
T = "Number System"
add = next(k for k in range(12) if (7385 + k) % 12 == 0)
assert add == 7 and 7385 % 12 == 5 and (7385 + 3) % 4 == 0 and (7385 + 3) % 3 != 0 and (7385 + 1) % 3 == 0
assert (7385 + 1) % 4 != 0 and (7385 + 5) % 12 != 0
Q(T, "Divisibility", B, "What is the least number that must be added to 7,385 so that the sum is exactly divisible "
  "by 12?",
  "7", ["5", "3", "1"],
  "Find the remainder on division by 12; the number to add is 12 minus that remainder",
  "12 × 615 = 7,380, so 7,385 leaves a remainder of 5. Adding 12 − 5 = 7 gives 7,392 = 12 × 616.",
  ["7,385 ÷ 12: remainder 5", "12 − 5 = 7", "7,392 = 12 × 616 ✓"],
  why="5 is the remainder, which would have to be subtracted, not added; 3 makes 7,388, divisible by 4 but not by 3 "
      "(digit sum 26); 1 makes 7,386, divisible by 3 but not by 4.", secs=40, by=BRUTE)

h = math.gcd(math.gcd(398 - 7, 436 - 11), 542 - 15)
assert h == 17 and 425 % 34 and 425 % 51 and 425 % 23 and 391 % 23 == 0
Q(T, "HCF and LCM", B, "What is the greatest number that divides 398, 436 and 542 leaving remainders 7, 11 and 15 "
  "respectively?",
  "17", ["34", "51", "23"],
  "Subtract each remainder first; the required number is the HCF of the results",
  "398 − 7 = 391, 436 − 11 = 425 and 542 − 15 = 527. 391 = 17 × 23, 425 = 17 × 25 and 527 = 17 × 31, so the HCF "
  "is 17.",
  ["391, 425, 527", "391 = 17 × 23, 425 = 17 × 25, 527 = 17 × 31", "HCF = 17"],
  why="34 = 2 × 17 does not divide the odd number 425; 51 = 3 × 17 does not divide 425 (digit sum 11); 23 divides "
      "391 but not 425 or 527.", secs=50, by=BRUTE)

rem = sum(math.factorial(k) for k in range(1, 101)) % 12
assert rem == 9 and all(math.factorial(k) % 12 == 0 for k in range(4, 101)) and (1 + 2) % 12 == 3
Q(T, "Remainders", I, "What is the remainder when 1! + 2! + 3! + … + 100! is divided by 12?",
  "9", ["0", "3", "1"],
  "From 4! = 24 onwards every factorial is a multiple of 12, so only the first three terms matter",
  "4! = 24 and every later factorial contains 24 as a factor, so each leaves remainder 0. The remainder therefore "
  "comes from 1! + 2! + 3! = 1 + 2 + 6 = 9.",
  ["n! is a multiple of 12 for n ≥ 4", "1! + 2! + 3! = 9", "Remainder = 9"],
  why="0 assumes every term is a multiple of 12; 3 also drops 3! = 6, which is not a multiple of 12; 1 keeps only 1!.",
  secs=50, by=BRUTE)

u = sum(n ** n for n in range(1, 11)) % 10
assert u == 7 and (sum(n ** n % 10 for n in range(1, 11)) - 3 + 7) % 10 == 1
assert (sum(n ** n % 10 for n in range(1, 11)) - 6 + 8) % 10 == 9 and sum(range(1, 11)) % 10 == 5
Q(T, "Unit digit", I, "What is the unit digit of 1¹ + 2² + 3³ + 4⁴ + … + 10¹⁰?",
  "7", ["1", "9", "5"],
  "Find the unit digit of each term from the cycle of its last digit, then add the unit digits",
  "Unit digits: 1¹ → 1, 2² → 4, 3³ → 7, 4⁴ → 6, 5⁵ → 5, 6⁶ → 6, 7⁷ → 3 (cycle 7, 9, 3, 1; 7 mod 4 = 3), "
  "8⁸ → 6 (cycle 8, 4, 2, 6; 8 mod 4 = 0), 9⁹ → 9, 10¹⁰ → 0. Sum = 47, so the unit digit is 7.",
  ["1, 4, 7, 6, 5, 6", "7⁷ → 3, 8⁸ → 6, 9⁹ → 9, 10¹⁰ → 0", "Sum = 47 ⇒ unit digit 7"],
  why="1 takes the unit digit of 7⁷ as 7 (sum 51); 9 takes the unit digit of 8⁸ as 8 (sum 49); 5 adds the bases "
      "1 + 2 + … + 10 = 55, ignoring the powers.", secs=70, by=BRUTE)

g = 0
for n in range(2, 200):
    g = math.gcd(g, n ** 5 - n)
assert g == 30 and (2 ** 5 - 2) == 30
Q(T, "Divisibility", A, "What is the largest number that divides n⁵ − n exactly for every natural number n?",
  "30", ["5", "6", "60"],
  "Factorise n⁵ − n = (n − 1)n(n + 1)(n² + 1) and test the smallest case n = 2",
  "(n − 1)n(n + 1) is a product of three consecutive integers, so it is divisible by 6. By Fermat's little "
  "theorem, n⁵ − n is also divisible by 5. So 30 always divides it. For n = 2, n⁵ − n = 30, so no number larger "
  "than 30 can always divide it.",
  ["n⁵ − n = (n − 1)n(n + 1)(n² + 1)", "Divisible by 2, 3 and 5 ⇒ by 30", "n = 2 gives exactly 30 ⇒ largest is 30"],
  why="5 and 6 always divide n⁵ − n but are not the largest such number; 60 fails for n = 2, where n⁵ − n = 30.",
  secs=80, by=BRUTE)

# ================================================================ Percentage (B3 I4 A2)
T = "Percentage"
x_ = F(391) / F(115, 100)
assert x_ == 340 and F(391) * F(85, 100) == F(33235, 100) and 391 - 15 == 376 and F(391) * F(115, 100) == F(44965, 100)
Q(T, "Basic percentage", B, "When a number is increased by 15%, it becomes 391. What is the number?",
  "340", ["332.35", "376", "449.65"],
  "After a 15% increase the number is 115% of the original, so divide by 1.15",
  "1.15 × number = 391, so number = 391 ÷ 1.15 = 340. Check: 340 + 15% of 340 = 340 + 51 = 391.",
  ["115% of x = 391", "x = 391 ÷ 1.15 = 340", "Check: 340 + 51 = 391 ✓"],
  why="332.35 takes 15% off 391 (15% of 391, not of the original); 376 subtracts 15 instead of 15%; 449.65 increases "
      "391 by a further 15%.", secs=40)

rent = 36000 * F(85, 100) * F(40, 100)
assert rent == 12240 and 36000 * F(40, 100) == 14400 and 36000 * F(85, 100) - rent == 18360 and 36000 * F(15, 100) == 5400
Q(T, "Income and expenditure", B, "Amit's monthly salary is ₹36,000. He saves 15% of it and spends 40% of the rest "
  "on rent. How much does he pay as rent each month?",
  "₹12,240", ["₹14,400", "₹18,360", "₹5,400"],
  "The 40% applies to what is left after saving, not to the whole salary",
  "Savings = 15% of 36,000 = 5,400, so the rest is 30,600. Rent = 40% of 30,600 = ₹12,240.",
  ["Rest = 85% of 36,000 = 30,600", "Rent = 40% of 30,600", "= ₹12,240"],
  why="₹14,400 takes 40% of the whole salary; ₹18,360 is what remains after rent (60% of 30,600); ₹5,400 is the "
      "saving, not the rent.", secs=40)

assert F(375, 2500) * 100 == 15 and F(375, 25000) * 100 == F(3, 2) and round(F(2500, 375), 2) == F(667, 100)
Q(T, "Basic percentage", B, "What percentage of 2.5 kg is 375 g?",
  "15%", ["1.5%", "150%", "6.67%"],
  "Convert to the same unit first: 2.5 kg = 2,500 g",
  "375 g out of 2,500 g = 375/2,500 = 0.15 = 15%.",
  ["2.5 kg = 2,500 g", "375 ÷ 2,500 = 0.15", "= 15%"],
  why="1.5% converts 2.5 kg to 25,000 g; 150% converts it to 250 g; 6.67% inverts the ratio (2,500 ÷ 375 = 6.67).",
  secs=35)

cut = 1 - F(110, 100) / (F(110, 100) ** 2)
assert cut == F(1, 11) and pct2(cut) == "9.09%"
Q(T, "Successive change", I, "The price of petrol rises by 10% and then by another 10%. A motorist cuts his "
  "consumption so that his spending on petrol rises by only 10% overall. By what percentage did he cut his "
  "consumption?",
  "9.09%", ["10%", "11%", "21%"],
  "Spending = price × consumption; two 10% rises make the price 1.21 times the original",
  "Price becomes 1.1 × 1.1 = 1.21 times. Spending must be 1.10 times, so consumption = 1.10 ÷ 1.21 = 10/11 of the "
  "original. The cut is 1/11 = 9.09%.",
  ["Price factor = 1.21", "Spending factor = 1.10", "Consumption = 1.10/1.21 = 10/11", "Cut = 1/11 = 9.09%"],
  why="10% simply matches the second 10% price rise; 11% subtracts the 10% target from the 21% price rise and "
      "treats the 11-point gap as the cut; 21% cuts consumption by the whole price rise.",
  secs=65)

val = 500000 * F(9, 10) ** 2
assert val == 405000 and F(486000, val) == F(6, 5) and F(486000 - 450000, 450000) == F(8, 100)
assert F(486000, 400000) == F(1215, 1000) and F(500000 - 486000, 500000) == F(28, 1000)
Q(T, "Population and depreciation", I, "A machine bought for ₹5,00,000 loses 10% of its value every year (on its "
  "value at the start of that year). At the end of 2 years it is sold for ₹4,86,000. By what percentage is the sale "
  "price above the machine's depreciated value at that time?",
  "20%", ["21.5%", "8%", "2.8%"],
  "Depreciated value after 2 years = 5,00,000 × 0.9²",
  "Value after 2 years = 5,00,000 × 0.9 × 0.9 = ₹4,05,000. The sale price exceeds it by 4,86,000 − 4,05,000 = "
  "81,000, which is 81,000 ÷ 4,05,000 = 20%.",
  ["Value = 5,00,000 × 0.81 = 4,05,000", "Excess = 81,000", "81,000 ÷ 4,05,000 = 20%"],
  why="21.5% depreciates by a flat 20% of the cost (₹4,00,000) instead of compounding; 8% depreciates for only one "
      "year (₹4,50,000); 2.8% compares the sale price with the purchase price (a fall of ₹14,000).", secs=65)

need = F(70, 100) * 60 - F(60, 100) * 40
assert need == 18 and F(70, 100) * 20 == 14 and F(80, 100) * 20 == 16
Q(T, "Basic percentage", I, "A cricket team won 60% of its first 40 matches. How many of its next 20 matches must it "
  "win so that it has won 70% of all its matches?",
  "18", ["14", "16", "42"],
  "Work with numbers of wins, not percentages: wins needed = 70% of the 60 matches",
  "Wins so far = 60% of 40 = 24. For 70% of 60 matches it needs 42 wins, so it must win 42 − 24 = 18 of the next 20.",
  ["Wins so far = 24", "Needed = 70% of 60 = 42", "42 − 24 = 18"],
  why="14 wins only 70% of the next 20 matches, which leaves the total at 38/60 = 63.3%; 16 raises the next-20 rate "
      "by just 10 points (80%), giving 40/60; 42 is the total number of wins needed, not the further wins.", secs=60)

xs_ = [x for x in range(1, 100) if F(100 + x, 100) * F(100 - x, 100) == F(96, 100)]
assert xs_ == [20]
Q(T, "Successive change", I, "A number is first increased by x% and the result is then decreased by x%. The final "
  "value is 4% less than the original number. What is x?",
  "20", ["2", "4", "16"],
  "An increase of x% followed by a decrease of x% gives a net change of −x²/100 %",
  "(1 + x/100)(1 − x/100) = 1 − x²/10,000 = 0.96, so x²/10,000 = 0.04, x² = 400 and x = 20.",
  ["Net change = −x²/100 %", "x²/100 = 4", "x² = 400 ⇒ x = 20"],
  why="2 solves x² = 4, dropping the /100; 4 takes the net loss of 4% to be x itself; 16 squares 4 instead of taking "
      "the square root of 400.", secs=60)

ch = F(60, 100) * F(120, 100) + F(25, 100) * F(92, 100) + F(15, 100) * F(110, 100) - 1
assert ch == F(115, 1000) and 20 - 8 + 10 == 22 and F(20 - 8 + 10, 3) == F(22, 3) and F(60, 100) * 20 == 12
Q(T, "Successive change", A, "A transporter's running cost per trip is 60% fuel, 25% maintenance and 15% insurance. "
  "The cost of fuel rises by 20%, maintenance cost falls by 8% and insurance cost rises by 10%. By what percentage "
  "does the running cost per trip rise?",
  "11.5%", ["22%", "7.33%", "12%"],
  "Weight each component's change by its share of the total cost",
  "Take the cost as 100: fuel 60 → 72, maintenance 25 → 23, insurance 15 → 16.5. New cost = 72 + 23 + 16.5 = 111.5, "
  "a rise of 11.5%.",
  ["Fuel: 60 × 1.20 = 72", "Maintenance: 25 × 0.92 = 23", "Insurance: 15 × 1.10 = 16.5", "Total 111.5 ⇒ +11.5%"],
  short="Net change = 0.6 × 20 − 0.25 × 8 + 0.15 × 10 = 12 − 2 + 1.5 = 11.5%.",
  why="22% adds the three changes without weighting them (20 − 8 + 10); 7.33% averages the three changes equally; "
      "12% counts only the fuel component (60% of 20%).", secs=75)

g0 = 50 + 20 + 30
g1 = 55 + 22 + 30
assert g1 - g0 == 7 and 50 * F(10, 100) == 5 and F(40, 100) * 10 == 4
Q(T, "Income and expenditure", A, "An officer's gross salary has three parts: basic pay is 50% of the gross, house "
  "rent allowance (HRA) is 40% of the basic pay, and the rest is a special allowance. The basic pay is raised by 10% "
  "(HRA stays at 40% of the new basic) and the special allowance is unchanged. By what percentage does the gross "
  "salary rise?",
  "7%", ["10%", "5%", "4%"],
  "Take the gross as 100 and split it into its parts before applying the rise",
  "Gross 100: basic 50, HRA 40% of 50 = 20, special 30. New basic = 55 and new HRA = 22, special still 30. New "
  "gross = 107, a rise of 7%.",
  ["Basic 50, HRA 20, special 30", "New basic 55, new HRA 22", "Gross 107 ⇒ +7%"],
  why="10% assumes the whole gross rises by 10%; 5% raises only the basic and forgets that HRA follows it; 4% counts "
      "only the HRA's share of the rise (40% of 10).", secs=75)

# ================================================================ Ratio and Proportion (B1 I2 A1)
T = "Ratio and Proportion"
ad = F(2, 3) * F(4, 5) * F(6, 7)
assert ad == F(16, 35) and F(2, 3) * F(4, 5) == F(8, 15)
Q(T, "Basic ratio", B, "If A : B = 2 : 3, B : C = 4 : 5 and C : D = 6 : 7, what is A : D?",
  "16 : 35", ["2 : 7", "35 : 16", "8 : 15"],
  "A/D = (A/B) × (B/C) × (C/D)",
  "A/D = 2/3 × 4/5 × 6/7 = 48/105 = 16/35, so A : D = 16 : 35.",
  ["A/D = 2/3 × 4/5 × 6/7", "= 48/105", "= 16/35"],
  why="2 : 7 takes the first term of the first ratio and the last term of the last; 35 : 16 inverts the answer "
      "(D : A); 8 : 15 stops at A : C.", secs=40)

sol = [x for x in range(1, 100) if (x + 4) ** 2 == x * (x + 10)]
assert sol == [8] and F(16, 10) * 10 == 16 and F(16, 6) == F(8, 3) and 8 + 4 == 12
Q(T, "Proportion", I, "If x + 4 is the mean proportional between x and x + 10, what is the value of x?",
  "8", ["1.6", "2⅔", "12"],
  "b is the mean proportional between a and c when b² = ac",
  "(x + 4)² = x(x + 10) gives x² + 8x + 16 = x² + 10x, so 2x = 16 and x = 8. Check: 12² = 144 = 8 × 18.",
  ["(x + 4)² = x(x + 10)", "x² + 8x + 16 = x² + 10x", "2x = 16 ⇒ x = 8", "Check: 12² = 8 × 18 ✓"],
  why="1.6 expands (x + 4)² as x² + 16, dropping the 8x (16 = 10x); 2⅔ expands it as x² + 4x + 16 (16 = 6x); 12 "
      "is x + 4, the mean proportional itself.", secs=60)

k_ = F(5500 - 100 - 150 - 50, 13)
assert k_ == 400 and 4 * k_ + 150 == 1750 and 4 * k_ == 1600 and r2(F(5500 * 4, 13)) == F(169231, 100)
assert 6 * k_ + 50 == 2450
Q(T, "Coins and salary share", I, "₹5,500 is divided among A, B and C so that, if ₹100, ₹150 and ₹50 are taken away "
  "from their shares respectively, the amounts left are in the ratio 3 : 4 : 6. What is B's share?",
  "₹1,750", ["₹1,600", "₹1,692.31", "₹2,450"],
  "Remove the deductions from the total first; share the rest in the ratio; then add each deduction back",
  "Total deducted = 100 + 150 + 50 = 300, leaving 5,200 in the ratio 3 : 4 : 6. One part = 5,200 ÷ 13 = 400. B's "
  "share = 4 × 400 + 150 = ₹1,750.",
  ["5,500 − 300 = 5,200", "One part = 5,200 ÷ 13 = 400", "B = 4 × 400 + 150 = 1,750"],
  why="₹1,600 forgets to add back B's ₹150; ₹1,692.31 divides the whole ₹5,500 in the ratio 3 : 4 : 6; ₹2,450 is "
      "C's share (6 × 400 + 50).", secs=60)

cands = [(a, b) for a in range(1, 50) for b in range(1, 50) if 3 * 5 * a + 5 * 12 * b == 2 * 5 * a + 7 * 12 * b
         and F(5 * a, 12 * b) == F(5, 6)]
assert all(a == 2 * b for a in range(1, 50) for b in range(1, 50) if 3 * a + 5 * b == 2 * a + 7 * b)
assert F(5 * 2, 12 * 1) == F(5, 6)
Q(T, "Basic ratio", A, "In class P the ratio of boys to girls is 3 : 2 and in class Q it is 5 : 7. When the two "
  "classes are combined, the numbers of boys and girls are equal. What is the ratio of the number of students in P "
  "to the number in Q?",
  "5 : 6", ["6 : 5", "2 : 1", "5 : 12"],
  "Let P have 5a students (3a boys, 2a girls) and Q have 12b (5b boys, 7b girls); equate total boys and girls",
  "Boys = 3a + 5b and girls = 2a + 7b. Equal totals give a = 2b. So P : Q = 5a : 12b = 10b : 12b = 5 : 6.",
  ["P = 5a (3a, 2a); Q = 12b (5b, 7b)", "3a + 5b = 2a + 7b ⇒ a = 2b", "5a : 12b = 10b : 12b = 5 : 6"],
  short="Alligation on the boys' share: P has 3/5 = 60% boys, Q has 5/12 ≈ 41.7%, target 50%; the gaps 8.3 and 10 "
        "give P : Q = 5 : 6.",
  why="6 : 5 inverts the answer; 2 : 1 is a : b, the multipliers, not the class sizes; 5 : 12 compares the ratio "
      "totals 5 and 12 directly.", secs=85)

# ================================================================ Problems on Ages (B1 I1 A1)
T = "Problems on Ages"
sols = [(m, s) for m in range(1, 80) for s in range(1, 40) if m + 2 * s == 55 and m + 7 == 2 * (s + 7)]
assert sols == [(31, 12)]
Q(T, "Present and future ages", B, "The present ages of a mother and her twin sons add up to 55 years. Seven years "
  "from now, the mother's age will equal the sum of the twins' ages then. What is the mother's present age?",
  "31 years", ["24 years", "38 years", "12 years"],
  "In 7 years each twin also ages 7 years, so the twins' sum grows by 14",
  "Let each twin be s years old. In 7 years: M + 7 = 2(s + 7), so M = 2s + 7. Then M + 2s = 4s + 7 = 55, so s = 12 "
  "and M = 31.",
  ["M + 7 = 2(s + 7) ⇒ M = 2s + 7", "4s + 7 = 55 ⇒ s = 12", "M = 31"],
  why="24 years is the twins' present total (2 × 12); 38 years is the mother's age 7 years from now; 12 years is "
      "each twin's age.", secs=45, by=BRUTE)

sols = [(a, b, c) for a in range(1, 90) for b in range(1, 90) for c in range(1, 90)
        if a + b - 10 == 60 and b + c == 80 and a + c + 10 == 88]
assert sols == [(34, 36, 44)]
Q(T, "Present and future ages", I, "Five years ago, the average age of A and B was 30 years. The average present age "
  "of B and C is 40 years. Five years from now, the average age of A and C will be 44 years. What is C's present "
  "age?",
  "44 years", ["34 years", "54 years", "49 years"],
  "Convert each average into a present-day sum first: add 5 years per person for the past, subtract for the future",
  "A + B now = 2 × 30 + 10 = 70. B + C = 80. A + C now = 2 × 44 − 10 = 78. Adding: 2(A + B + C) = 228, so "
  "A + B + C = 114 and C = 114 − 70 = 44.",
  ["A + B = 60 + 10 = 70", "B + C = 80", "A + C = 88 − 10 = 78", "A + B + C = 114 ⇒ C = 44"],
  why="34 years is A's age; 54 years ignores the ±10 adjustments (60 and 88 used as present sums); 49 years is C's "
      "age five years from now.", secs=70, by=BRUTE)

sols = [(a, b) for a in range(1, 80) for b in range(1, 80) if a > b and b - (a - b) == 6 and a + (a - b) == 42]
assert sols == [(30, 18)]
Q(T, "Present and future ages", A, "Ravi tells his younger cousin Arun: \"When I was as old as you are now, you were "
  "6 years old. When you are as old as I am now, I shall be 42.\" What is Ravi's present age?",
  "30 years", ["18 years", "24 years", "36 years"],
  "The age gap d stays the same: going back d years makes Ravi Arun's age; going forward d years makes Arun Ravi's",
  "Let the gap be d. d years ago Arun was 6, so Arun = 6 + d. In d years Ravi will be 42, so Ravi = 42 − d. Also "
  "Ravi = Arun + d = 6 + 2d. So 42 − d = 6 + 2d, giving d = 12 and Ravi = 30 (Arun = 18).",
  ["Arun = 6 + d", "Ravi = 42 − d = 6 + 2d", "3d = 36 ⇒ d = 12", "Ravi = 30, Arun = 18"],
  short="6, Arun, Ravi, 42 are equally spaced (gap d), so 3d = 42 − 6 = 36.",
  why="18 years is Arun's age; 24 years takes Ravi's age as the midpoint of 6 and 42 (that is "
      "the average of the two ages); 36 years is 42 − 6, three gaps rather than Ravi's age.", secs=80, by=BRUTE)

# ================================================================ Average (B1 I2 A3)
T = "Average"
new = 62 + F(30 * 3, 40)
assert new == F(257, 4) and 62 + F(30, 40) == F(6275, 100) and 62 + F(3, 40) == F(62075, 1000)
Q(T, "Simple average", B, "The average mark of 40 students in a test is 62. On re-checking, 3 marks are added to "
  "the score of each of 30 of these students. What is the new average of the class?",
  "64.25", ["65", "62.75", "62.075"],
  "The total rises by 30 × 3 = 90 marks; spread this over all 40 students",
  "Extra marks = 30 × 3 = 90. The average rises by 90 ÷ 40 = 2.25, so the new average is 62 + 2.25 = 64.25.",
  ["Extra marks = 90", "Rise = 90 ÷ 40 = 2.25", "New average = 64.25"],
  why="65 adds 3 to the average, as if all 40 students gained 3; 62.75 adds only 30 marks in all; 62.075 adds just 3 "
      "marks to the class total.", secs=40)

sols = [(m, x) for m in range(1, 60) for x in range(1, 100) if 10 * m == 9 * 18 + x and x == m + 9]
assert sols == [(19, 28)]
Q(T, "Simple average", I, "The average of the first nine of ten numbers is 18. The tenth number is 9 more than the "
  "average of all ten numbers. What is the tenth number?",
  "28", ["27", "19", "190"],
  "Let the average of all ten be m; write the total in two ways",
  "Total of ten = 10m. It is also 9 × 18 + x = 162 + x, with x = m + 9. So 10m = 171 + m, giving m = 19 and "
  "x = 28.",
  ["10m = 162 + x", "x = m + 9", "9m = 171 ⇒ m = 19", "x = 28"],
  why="27 adds 9 to the average of the first nine (18) instead of the average of all ten; 19 is the average of all "
      "ten; 190 is their total.", secs=60, by=BRUTE)

new = 40 + F(5 * 6 - 7 * 3, 12)
assert new == F(163, 4) and 40 + 6 - 3 == 43 and 40 + F(-30 + 21, 12) == F(157, 4) and 40 + 9 == 49
Q(T, "Replacement", I, "The average of 12 numbers is 40. Each of the first five numbers is increased by 6 and each of "
  "the other seven is decreased by 3. What is the new average?",
  "40.75", ["43", "39.25", "49"],
  "Find the net change in the total and divide by the count",
  "Change in total = 5 × 6 − 7 × 3 = 30 − 21 = 9. The average rises by 9 ÷ 12 = 0.75, to 40.75.",
  ["+5 × 6 = +30", "−7 × 3 = −21", "Net +9 ⇒ +0.75", "New average = 40.75"],
  why="43 adds 6 − 3 = 3 to the average, ignoring how many numbers change; 39.25 swaps the signs (−30 + 21); 49 adds "
      "the whole net change of 9 to the average without dividing by 12.", secs=60)

sols = [(x, y) for x in range(0, 21) for y in range(0, 21)
        if 3 + x + y + 4 == 20 and F(10 * 3 + 20 * x + 30 * y + 40 * 4, 20) == 26]
assert sols == [(6, 7)]
Q(T, "Weighted average", A, "In a quiz, the scores 10, 20, 30 and 40 were obtained by 3, x, y and 4 participants "
  "respectively. There were 20 participants in all and their mean score was 26. What is x?",
  "6", ["7", "6.5", "13"],
  "Two equations: the frequencies add up to 20, and Σ(score × frequency) = 26 × 20",
  "x + y = 20 − 7 = 13. Total score = 30 + 20x + 30y + 160 = 520, so 20x + 30y = 330, i.e. 2x + 3y = 33. With "
  "x + y = 13: y = 33 − 26 = 7 and x = 6.",
  ["x + y = 13", "30 + 20x + 30y + 160 = 520 ⇒ 2x + 3y = 33", "y = 7, x = 6"],
  why="7 is y, the frequency of the score 30; 6.5 splits the 13 missing participants equally; 13 is x + y.", secs=80,
  by=BRUTE)

nums = [int("".join(p)) for p in itertools.permutations("258")]
assert len(nums) == 6 and F(sum(nums), 6) == 555 and sum(nums) == 3330 and F(15 * 111, 6) == F(555, 2)
assert sum(nums) // 2 == 1665
Q(T, "Simple average", A, "Six different three-digit numbers can be formed using each of the digits 2, 5 and 8 "
  "exactly once. What is the average of these six numbers?",
  "555", ["3,330", "277.5", "1,665"],
  "Each digit appears in each place (hundreds, tens, units) exactly twice among the six numbers",
  "In each place the digits 2, 5 and 8 appear twice, so the sum of the six numbers is 2 × (2 + 5 + 8) × 111 = "
  "3,330. Average = 3,330 ÷ 6 = 555.",
  ["Each digit occurs twice in each place", "Sum = 2 × 15 × 111 = 3,330", "Average = 3,330 ÷ 6 = 555"],
  short="Average = (average digit) × 111 = 5 × 111 = 555.",
  why="3,330 is the sum of the six numbers, not their average; 277.5 divides by 6 twice (15 × 111 ÷ 6); 1,665 "
      "divides the sum by 2 instead of 6.", secs=70, by=BRUTE)

sols = [s for s in range(0, 500) if 10 * 50000 + 40 * 24000 + s * 15000 == 25000 * (50 + s)]
assert sols == [21] and (1460000 - 1250000) // 15000 == 14 and 1460000 // 10000 == 146 and 210000 // 5000 == 42
Q(T, "Weighted average", A, "A bank branch has 10 officers with an average monthly salary of ₹50,000, 40 clerks with "
  "an average of ₹24,000 and some sub-staff with an average of ₹15,000. The average salary of all the staff is "
  "₹25,000. How many sub-staff are there?",
  "21", ["146", "14", "42"],
  "Compare each group with the overall average: the surplus above ₹25,000 must equal the shortfall below it",
  "Officers are ₹25,000 above the average: surplus 10 × 25,000 = 2,50,000. Clerks are ₹1,000 below: shortfall "
  "40 × 1,000 = 40,000. Net surplus = 2,10,000, which the sub-staff (₹10,000 below the average each) must offset: "
  "2,10,000 ÷ 10,000 = 21.",
  ["Officers: +25,000 × 10 = +2,50,000", "Clerks: −1,000 × 40 = −40,000", "Net +2,10,000",
   "Sub-staff: −10,000 each ⇒ 21"],
  why="146 sets the total salary equal to 25,000 × s, forgetting the 50 officers and clerks on the right side; 14 "
      "divides the surplus by ₹15,000 (the sub-staff salary) instead of the ₹10,000 shortfall; 42 divides it by "
      "₹5,000.", secs=85, by=BRUTE)

# ================================================================ Profit and Loss (B2 I3 A3)
T = "Profit and Loss"
sp = (12500 + 500) * F(120, 100)
assert sp == 15600 and 12500 * F(6, 5) == 15000 and 12500 * F(6, 5) + 500 == 15500 and sp - 13000 == 2600
Q(T, "Cost and selling price", B, "A dealer buys a mobile phone for ₹12,500 and pays ₹500 for its transport. At what "
  "price must he sell it to make a profit of 20% on his total cost?",
  "₹15,600", ["₹15,000", "₹15,500", "₹2,600"],
  "Total cost includes transport; the profit percentage is applied to the total cost",
  "Total cost = 12,500 + 500 = ₹13,000. Selling price = 13,000 × 1.2 = ₹15,600.",
  ["Total cost = 13,000", "SP = 13,000 × 120%", "= ₹15,600"],
  why="₹15,000 ignores the transport cost; ₹15,500 adds the transport after taking 20% on the phone alone; ₹2,600 is "
      "the profit, not the selling price.", secs=35)

cost = (300 + 120) * F(105, 100)
assert cost == 441 and F("529.2") / cost == F(6, 5) and F("529.2") / 420 == F(126, 100)
assert r2(F("529.2") / 300 * 100 - 100) == F("76.4") and r2((F("529.2") - 441) / F("529.2") * 100) == F("16.67")
Q(T, "Cost and selling price", B, "A tailor's cost for a shirt is ₹300 for cloth and ₹120 for stitching, plus "
  "overheads equal to 5% of these two costs. He sells the shirt for ₹529.20. What is his profit percentage?",
  "20%", ["26%", "76.4%", "16.67%"],
  "Full cost = (cloth + stitching) × 1.05; profit % is on this full cost",
  "Cloth + stitching = ₹420. Overheads = 5% of 420 = ₹21, so the full cost is ₹441. Profit = 529.20 − 441 = 88.20, "
  "which is 88.20 ÷ 441 = 20%.",
  ["420 × 1.05 = 441", "Profit = 88.20", "88.20 ÷ 441 = 20%"],
  why="26% leaves out the overheads (529.20 ÷ 420); 76.4% counts only the cloth as cost; 16.67% takes the profit "
      "as a percentage of the selling price.", secs=45)

milk_per_litre = F(9, 10) * F(10, 11)
gain = 1 / milk_per_litre - 1
assert gain == F(2, 9) and pct2(gain) == "22.22%" and pct2(F(1, 9)) == "11.11%"
Q(T, "Dishonest dealer", I, "A milk vendor adds 1 litre of water to every 10 litres of milk. His 1-litre measure "
  "actually holds only 900 ml. He sells the mixture at the cost price of pure milk per litre. What is his gain "
  "percentage?",
  "22.22%", ["20%", "21%", "11.11%"],
  "Find how much pure milk the customer actually gets for the price of 1 litre",
  "A 'litre' sold is 0.9 litre of mixture, of which 10/11 is milk: 0.9 × 10/11 = 9/11 litre of milk. He is paid "
  "for 1 litre, so gain = (1 − 9/11) ÷ 9/11 = 2/9 = 22.22%.",
  ["Milk per 'litre' = 0.9 × 10/11 = 9/11 L", "Paid for 1 L, gives 9/11 L", "Gain = (11/9 − 1) = 2/9 = 22.22%"],
  short="Gain factor = (11/10) × (10/9) = 11/9.",
  why="20% adds the two 10% cheats; 21% compounds 10% and 10% (1.1 × 1.1), but the short measure gives 1/9 more, not "
      "1/10; 11.11% counts only the short measure and ignores the water.", secs=70)

old = 400 * 50
new = 600 * 40
assert F(new - old, old) == F(20, 100)
Q(T, "Cost and selling price", I, "A shop sells 400 electric irons a week at a profit of ₹50 each. It cuts the price "
  "of an iron by ₹10, and weekly sales rise by 50%. What happens to the shop's weekly profit?",
  "It rises by 20%", ["It rises by 30%", "It rises by 50%", "It falls by 20%"],
  "Weekly profit = profit per unit × units sold; the price cut comes straight out of the profit per unit",
  "Before: 400 × 50 = ₹20,000. After: profit per iron = 50 − 10 = ₹40 and sales = 600, so profit = 600 × 40 = "
  "₹24,000. The rise is 4,000 ÷ 20,000 = 20%.",
  ["Before: 400 × 50 = 20,000", "After: 600 × 40 = 24,000", "Change = +20%"],
  short="Profit factor = 1.5 × 0.8 = 1.2.",
  why="30% subtracts the 20% fall in unit profit from the 50% rise in sales instead of multiplying; 50% counts only "
      "the rise in sales; 'falls by 20%' counts only the drop in profit per iron.", secs=55)

net = 1000 - F(2, 100) * 1000 - 40
assert net == 940 and r2(F(net - 750, 750) * 100) == F("25.33") and r2(F(250, 750) * 100) == F("33.33")
assert r2(F(980 - 750, 750) * 100) == F("30.67") and F(960 - 750, 750) * 100 == 28
Q(T, "Cost and selling price", I, "An online seller lists a lamp at ₹1,000. The marketplace keeps a commission of 2% "
  "of the listed price, and the seller pays ₹40 for shipping each order. If the lamp costs him ₹750, what is his "
  "profit percentage on each sale?",
  "25.33%", ["33.33%", "30.67%", "28%"],
  "Net receipt = listed price − commission − shipping; profit % is on the cost",
  "Commission = 2% of 1,000 = ₹20. Net receipt = 1,000 − 20 − 40 = ₹940. Profit = 940 − 750 = ₹190, which is "
  "190 ÷ 750 = 25.33%.",
  ["Commission = ₹20", "Net = 1,000 − 20 − 40 = 940", "Profit = 190", "190 ÷ 750 = 25.33%"],
  why="33.33% ignores both charges; 30.67% subtracts the commission but forgets the shipping; 28% subtracts the "
      "shipping but forgets the commission.", secs=55)

xs_ = [x for x in range(1, 50) if F(90, 100) * F(100 + x, 100) ** 2 == F(1089, 1000)]
assert xs_ == [10] and F(189, 20) == F("9.45") and abs(math.sqrt(1.089) - 1.04355) < 1e-4
Q(T, "Successive transactions", A, "A sold an article to B at a loss of 10%. B sold it to C at a profit of x%, and C "
  "sold it to D at a profit of x%. D paid 8.9% more than A's cost. What is x?",
  "10%", ["9.45%", "4.36%", "21%"],
  "Multiply the factors: 0.9 × (1 + x/100)² = 1.089",
  "0.9 × (1 + x/100)² = 1.089, so (1 + x/100)² = 1.21 and 1 + x/100 = 1.1. So x = 10.",
  ["0.9 × (1 + x/100)² = 1.089", "(1 + x/100)² = 1.21", "1 + x/100 = 1.1 ⇒ x = 10"],
  why="9.45% adds the percentages (−10 + 2x = 8.9) instead of multiplying the factors; 4.36% ignores A's 10% loss "
      "((1 + x/100)² = 1.089); 21% stops at 1.21 and reads it as a single profit.", secs=75, by=BRUTE)

total_cost = 1000 * 150 + 60000
target = total_cost * F(120, 100)
price = (target - 800 * 300) / 200
assert total_cost == 210000 and price == 60 and (total_cost / F(80, 100) - 240000) / 200 == F(225, 2)
assert target / 1000 == 252 and F(12000, 800) == 15
Q(T, "Cost and selling price", A, "A manufacturer makes 1,000 table lamps. Each lamp costs ₹150 in materials and "
  "labour, and the fixed costs for the batch are ₹60,000. He sells 800 lamps at ₹300 each and clears the rest at a "
  "single lower price. At what price must the remaining lamps be sold for his overall profit to be 20% of his total "
  "cost?",
  "₹60", ["₹112.50", "₹252", "₹15"],
  "Total cost includes the fixed cost; target revenue = 1.2 × total cost",
  "Total cost = 1,000 × 150 + 60,000 = ₹2,10,000. Target revenue = 1.2 × 2,10,000 = ₹2,52,000. The 800 lamps bring "
  "in ₹2,40,000, so the other 200 must bring ₹12,000: ₹60 each.",
  ["Total cost = 2,10,000", "Target revenue = 2,52,000", "800 × 300 = 2,40,000", "12,000 ÷ 200 = ₹60"],
  why="₹112.50 takes the profit as 20% of revenue (2,10,000 ÷ 0.8); ₹252 is the target revenue per lamp over all "
      "1,000 lamps; ₹15 divides the shortfall of ₹12,000 by 800 instead of 200.", secs=90)

cost = 3 * 200 + 2 * 300
good = 3 * F(90, 100) + 2 * F(95, 100)
rev = good * 320
assert cost == 1200 and good == F(46, 10) and rev == 1472 and r2(F(rev - cost, cost) * 100) == F("22.67")
assert F(5 * 320 - 1200, 1200) * 100 == F(100, 3) and F(320 - 250, 250) * 100 == 28
assert r2(F(5 * F(925, 1000) * 320 - 1200, 1200) * 100) == F("23.33")
Q(T, "Cost and selling price", A, "A cloth dealer buys cloth X at ₹200 per metre and cloth Y at ₹300 per metre, in "
  "the ratio 3 : 2 by length. 10% of X and 5% of Y turn out to be damaged and cannot be sold. He sells all the rest "
  "at ₹320 per metre. What is his profit percentage?",
  "22.67%", ["33.33%", "28%", "23.33%"],
  "Take 3 m of X and 2 m of Y; subtract the damaged lengths before computing revenue",
  "Cost of 3 m of X and 2 m of Y = 600 + 600 = ₹1,200. Saleable length = 3 × 0.9 + 2 × 0.95 = 2.7 + 1.9 = 4.6 m. "
  "Revenue = 4.6 × 320 = ₹1,472. Profit = 272, which is 272 ÷ 1,200 = 22.67%.",
  ["Cost = 1,200 for 5 m", "Saleable = 2.7 + 1.9 = 4.6 m", "Revenue = 1,472", "Profit % = 272 ÷ 1,200 = 22.67%"],
  why="33.33% ignores the damage (5 m × 320); 28% compares ₹320 with the simple average cost ₹250, ignoring both "
      "the 3 : 2 ratio and the damage; 23.33% applies the average damage rate 7.5% to all 5 m.", secs=90)

# ================================================================ Discount (B1 I2 A1)
T = "Discount"
p_ = 4000 * F(75, 100) * F(80, 100)
assert p_ == 2400 and 4000 * F(55, 100) == 2200 and 4000 - p_ == 1600 and 4000 * F(75, 100) == 3000
Q(T, "Successive discounts", B, "A shop gives successive discounts of 25% and 20% on a jacket marked ₹4,000. How much "
  "does a customer pay?",
  "₹2,400", ["₹2,200", "₹1,600", "₹3,000"],
  "Apply the second discount to the already reduced price",
  "After 25% off: 4,000 × 0.75 = ₹3,000. After a further 20% off: 3,000 × 0.8 = ₹2,400.",
  ["4,000 × 0.75 = 3,000", "3,000 × 0.80 = 2,400"],
  why="₹2,200 adds the discounts (45% off); ₹1,600 is the total discount, not the price paid; ₹3,000 applies only "
      "the first discount.", secs=35)

pay = 3000 - min(F(20, 100) * 3000, 500)
eff = pay * F(95, 100)
assert pay == 2500 and eff == 2375 and 3000 * F(80, 100) * F(95, 100) == 2280 and 3000 * F(80, 100) == 2400
Q(T, "Successive discounts", I, "A shopping app offers 20% off, subject to a maximum discount of ₹500, and then 5% "
  "cashback on the amount paid. What is the effective cost of an item priced at ₹3,000?",
  "₹2,375", ["₹2,280", "₹2,500", "₹2,400"],
  "20% of 3,000 = 600 exceeds the cap, so the discount is only ₹500; cashback is on the amount actually paid",
  "20% of 3,000 = ₹600, but the cap limits the discount to ₹500, so the buyer pays ₹2,500. Cashback = 5% of 2,500 = "
  "₹125. Effective cost = 2,500 − 125 = ₹2,375.",
  ["20% = 600 > cap ⇒ discount 500", "Pay 2,500", "Cashback 125", "Effective cost 2,375"],
  why="₹2,280 ignores the cap (2,400 × 0.95); ₹2,500 forgets the cashback; ₹2,400 ignores both the cap and the "
      "cashback.", secs=55)

received = 40000 * F(875, 1000) - 3000 + 1200
assert received == 33200 and r2(F(received - 28000, 28000) * 100) == F("18.57")
assert F(35000 - 28000, 28000) * 100 == 25 and r2(F(32000 - 28000, 28000) * 100) == F("14.29")
assert r2(F(5200, 33200) * 100) == F("15.66")
Q(T, "Discount with profit", I, "A television marked ₹40,000 is sold at a 12.5% discount. The buyer also hands over "
  "his old set, for which the shop allows ₹3,000 off the price; the shop can resell the old set for only ₹1,200. If "
  "the new television cost the shop ₹28,000, what is the shop's profit percentage on the deal?",
  "18.57%", ["25%", "14.29%", "15.66%"],
  "The shop's receipts = cash received + what the old set is really worth to it",
  "Price after discount = 40,000 × 0.875 = ₹35,000. Cash received = 35,000 − 3,000 = ₹32,000. Adding the old set's "
  "real worth, ₹1,200, the shop gets ₹33,200. Profit = 5,200, which is 5,200 ÷ 28,000 = 18.57%.",
  ["After discount: 35,000", "Cash: 35,000 − 3,000 = 32,000", "Total value: 32,000 + 1,200 = 33,200",
   "Profit % = 5,200 ÷ 28,000 = 18.57%"],
  why="25% values the old set at the full ₹3,000 allowed for it (₹35,000 received); 14.29% treats the old set as "
      "worthless (₹32,000); 15.66% takes the profit as a percentage of the ₹33,200 received instead of the cost.",
  secs=80)

f_ = F(125, 100) * F(70, 100) * F(90, 100)
mp = F(126, 100) / f_
assert f_ == F(7875, 10000) and mp == F(16, 10)
assert r2((F(126, 100) / F(85, 100) - 1) * 100) == F("48.24") and F(126, 100) / F(63, 100) == 2
assert F(126, 100) / F(875, 1000) == F(144, 100)
Q(T, "Discount with profit", A, "Before a sale, a shop raises the marked price of a cooler by 25% and then "
  "advertises 'flat 30% off'. Card buyers get a further 10% off the sale price. Selling to a card buyer, the shop "
  "still makes a 26% profit on cost. By what percentage above cost was the original marked price?",
  "60%", ["48.24%", "100%", "44%"],
  "Chain the factors: card price = original MP × 1.25 × 0.70 × 0.90",
  "Card price = MP × 1.25 × 0.7 × 0.9 = 0.7875 MP. This equals 1.26 × cost, so MP = 1.26 ÷ 0.7875 = 1.6 × cost, "
  "i.e. 60% above cost.",
  ["1.25 × 0.70 × 0.90 = 0.7875", "0.7875 MP = 1.26 C", "MP = 1.6 C ⇒ 60% above cost"],
  why="48.24% adds and subtracts the percentages (1.25 − 0.30 − 0.10 = 0.85); 100% ignores the 25% price rise "
      "(0.7 × 0.9 = 0.63); 44% forgets the card discount (0.875).", secs=90)

# ================================================================ Simple Interest (B1 I1 A1)
T = "Simple Interest"
si = 6400 * F(75, 1000) * F(8, 3)
assert si == 1280 and 6400 * F(75, 1000) * F(28, 10) == 1344 and 6400 * F(75, 1000) * 2 == 960 and 6400 + si == 7680
Q(T, "Basic SI", B, "What is the simple interest on ₹6,400 at 7.5% per annum for 2 years 8 months?",
  "₹1,280", ["₹1,344", "₹960", "₹7,680"],
  "Convert the period to years: 2 years 8 months = 2 8/12 = 8/3 years",
  "SI = 6,400 × 7.5/100 × 8/3 = 480 × 8/3 = ₹1,280.",
  ["Yearly interest = 7.5% of 6,400 = 480", "Time = 8/3 years", "SI = 480 × 8/3 = 1,280"],
  why="₹1,344 reads 2 years 8 months as 2.8 years; ₹960 counts only the 2 whole years; ₹7,680 is the amount "
      "(principal + interest), not the interest.", secs=45)

rd = 2000 * F(6, 100) / 12 * sum(range(1, 13))
assert rd == 780 and 24000 * F(6, 100) == 1440 and 24000 * F(6, 100) / 2 == 720 and 2000 * F(6, 1200) * 66 == 660
Q(T, "Basic SI", I, "Ravi deposits ₹2,000 at the start of every month for 12 months in a recurring deposit that pays "
  "6% per annum simple interest. How much interest has he earned at the end of the 12th month?",
  "₹780", ["₹1,440", "₹720", "₹660"],
  "The first deposit earns interest for 12 months, the second for 11, …, the last for 1 month",
  "Interest on ₹2,000 for one month = 2,000 × 6% ÷ 12 = ₹10. The deposits earn for 12 + 11 + … + 1 = 78 months in "
  "all, so the interest = 78 × 10 = ₹780.",
  ["One deposit, one month: ₹10", "Months: 12 + 11 + … + 1 = 78", "Interest = 78 × 10 = ₹780"],
  why="₹1,440 gives every deposit a full year of interest; ₹720 gives each deposit 6 months on average instead of "
      "6.5; ₹660 counts the first deposit for only 11 months (11 + 10 + … + 1 = 66).", secs=70)

t2 = (2 - F(5 * 10, 100)) / F(12, 100)
assert t2 == F(25, 2) and 5 + t2 == F(35, 2) and F(200, 12) == F(50, 3)
Q(T, "SI with changing rates", A, "A sum doubles itself in 10 years at simple interest. After the first 5 years the "
  "rate is raised to 12% per annum. In how many years in all will the sum become three times itself?",
  "17.5 years", ["20 years", "12.5 years", "16⅔ years"],
  "Doubling in 10 years means 100% interest in 10 years, i.e. 10% a year; tripling needs 200% interest",
  "Rate = 100% ÷ 10 = 10%. In the first 5 years the interest is 50% of the sum. The remaining 150% at 12% a year "
  "takes 150 ÷ 12 = 12.5 years. Total = 5 + 12.5 = 17.5 years.",
  ["Rate = 10%", "First 5 years: 50%", "Remaining 150% at 12%: 12.5 years", "Total = 17.5 years"],
  why="20 years keeps the rate at 10% throughout; 12.5 years gives only the second phase; 16⅔ years applies 12% "
      "from the start (200 ÷ 12).", secs=80)

# ================================================================ Compound Interest (B2 I1 A1)
T = "Compound Interest"
amt = 5000 * F(120, 100) * F(110, 100)
assert amt == 6600 and 5000 * F(11, 10) ** 3 - 5000 == 1655 and 5000 * F(20, 100) * F(3, 2) == 1500
Q(T, "Annual compounding", B, "What is the compound interest on ₹5,000 for 1½ years at 20% per annum, compounded "
  "annually? (For the last half year, interest is at half the annual rate on the amount then due.)",
  "₹1,600", ["₹1,655", "₹1,500", "₹1,000"],
  "Compound for the full year, then add 10% (half of 20%) for the half year",
  "After 1 year: 5,000 × 1.2 = ₹6,000. For the next half year: 6,000 × 1.1 = ₹6,600. CI = 6,600 − 5,000 = ₹1,600.",
  ["1 year: 5,000 × 1.20 = 6,000", "½ year: 6,000 × 1.10 = 6,600", "CI = 1,600"],
  why="₹1,655 compounds half-yearly for 3 periods (5,000 × 1.1³ − 5,000); ₹1,500 is simple interest for 1½ years; "
      "₹1,000 stops after the first year.", secs=45)

ci = F(11, 10) ** 2 - 1
assert ci / F(2, 10) == F(21, 20)
Q(T, "CI vs SI difference", B, "On the same sum, what is the ratio of the compound interest (compounded annually) to "
  "the simple interest for 2 years at 10% per annum?",
  "21 : 20", ["11 : 10", "1 : 1", "121 : 100"],
  "For 2 years, CI = P(1.1² − 1) = 0.21P and SI = 0.20P",
  "CI = P × (1.21 − 1) = 0.21P. SI = P × 10% × 2 = 0.20P. Ratio = 0.21 : 0.20 = 21 : 20.",
  ["CI = 0.21P", "SI = 0.20P", "21 : 20"],
  why="11 : 10 compares one year's growth factor 1.1 with 1; 1 : 1 forgets the interest on interest in year 2; "
      "121 : 100 compares the CI amount with the principal.", secs=40)

amt = 20000 * F(105, 100) * F(110, 100) * F(120, 100)
assert amt == 27720 and amt - 20000 == 7720 and 20000 * F(35, 100) == 7000
assert 20000 * F(105, 100) * F(110, 100) + 4000 - 20000 == 7100
Q(T, "Annual compounding", I, "₹20,000 is invested at compound interest, compounded annually, at 5% for the first "
  "year, 10% for the second year and 20% for the third year. What is the compound interest for the three years?",
  "₹7,720", ["₹7,000", "₹27,720", "₹7,100"],
  "Multiply the yearly growth factors: 1.05 × 1.10 × 1.20",
  "Amount = 20,000 × 1.05 × 1.10 × 1.20 = 21,000 × 1.10 × 1.20 = 23,100 × 1.20 = ₹27,720. CI = 27,720 − 20,000 = "
  "₹7,720.",
  ["Year 1: 21,000", "Year 2: 23,100", "Year 3: 27,720", "CI = 7,720"],
  why="₹7,000 adds the rates as simple interest (35%); ₹27,720 is the amount, not the interest; ₹7,100 compounds the "
      "first two years but takes the 20% on the original ₹20,000.", secs=60)

pv = F(13310) / F(11, 10) ** 3 + F(14641) / F(11, 10) ** 4
assert pv == 20000 and F(13310) / F(11, 10) ** 3 + F(14641) / F(11, 10) ** 3 == 21000
assert F(13310) / F(11, 10) ** 3 == 10000 and 13310 + 14641 == 27951
Q(T, "Annual compounding", A, "How much must be invested now at 10% per annum compound interest (compounded annually) "
  "so that ₹13,310 can be withdrawn at the end of 3 years and a further ₹14,641 at the end of 4 years, leaving "
  "nothing?",
  "₹20,000", ["₹21,000", "₹10,000", "₹27,951"],
  "The investment equals the sum of the present values of the two withdrawals",
  "Present value of 13,310 due in 3 years = 13,310 ÷ 1.1³ = ₹10,000. Present value of 14,641 due in 4 years = "
  "14,641 ÷ 1.1⁴ = ₹10,000. Investment = ₹20,000.",
  ["13,310 ÷ 1.331 = 10,000", "14,641 ÷ 1.4641 = 10,000", "Total = 20,000"],
  why="₹21,000 discounts the second withdrawal for only 3 years (14,641 ÷ 1.331 = 11,000); ₹10,000 covers only one "
      "withdrawal; ₹27,951 adds the withdrawals without discounting.", secs=75)

# ================================================================ Partnership (B1 I1 A1)
T = "Partnership"
tot = F(45000, 3) * 12
assert tot == 180000 and 45000 * 3 == 135000
Q(T, "Simple partnership", B, "A, B and C invest for the same period and share the profit in the ratio 3 : 4 : 5. A "
  "invested ₹45,000. What was the total capital of the three partners?",
  "₹1,80,000", ["₹60,000", "₹75,000", "₹1,35,000"],
  "For the same period, profits are in the ratio of capitals, so one part = 45,000 ÷ 3",
  "One part = 45,000 ÷ 3 = ₹15,000. Total = (3 + 4 + 5) × 15,000 = ₹1,80,000.",
  ["One part = 15,000", "Total parts = 12", "Total = 1,80,000"],
  why="₹60,000 is B's capital; ₹75,000 is C's capital; ₹1,35,000 multiplies A's capital by 3 instead of dividing by 3 "
      "and multiplying by 12.", secs=40)

interest = 20000 * F(10, 100)
b_total = (32000 - interest) * F(2, 5) + interest
assert b_total == 14000 and 32000 * F(2, 5) == 12800 and 32000 * F(1, 2) == 16000 and b_total - interest == 12000
Q(T, "Simple partnership", I, "A and B invest ₹60,000 and ₹40,000 in a firm for a year. B also lends ₹20,000 to the "
  "firm at 10% per annum interest, which is paid before the profit is shared. The year's profit before this "
  "interest is ₹32,000, and the rest is shared in the ratio of capitals. How much does B receive in all?",
  "₹14,000", ["₹12,800", "₹16,000", "₹12,000"],
  "Pay the loan interest first; only the remainder is shared in the ratio 3 : 2; B gets both",
  "Interest to B = 10% of 20,000 = ₹2,000. Profit left = 32,000 − 2,000 = ₹30,000, shared 60 : 40 = 3 : 2. B's "
  "share = 2/5 × 30,000 = ₹12,000. B receives 12,000 + 2,000 = ₹14,000.",
  ["Interest = 2,000", "Remaining 30,000 in 3 : 2", "B's share = 12,000", "B total = 14,000"],
  why="₹12,800 shares the whole ₹32,000 and ignores the loan; ₹16,000 treats the loan as capital (60 : 60); ₹12,000 "
      "forgets to add the interest B earns on his loan.", secs=65)

fee = F(10, 100) * 120000
rest = 120000 - fee
b_ = fee + rest / 3 / 3 + rest * F(2, 3) * F(3, 10)
assert b_ == 45600 and fee + rest * F(3, 10) == 44400 and 120000 * F(3, 10) == 36000 and fee + rest * F(2, 3) * F(3, 10) == 33600
Q(T, "Working partner", A, "A, B and C invest ₹1,50,000, ₹90,000 and ₹60,000 in a firm. B manages it and first takes "
  "10% of the profit as a management fee. Of the remaining profit, one-third is shared equally among the three and "
  "the rest in the ratio of their capitals. Out of a profit of ₹1,20,000, how much does B receive in all?",
  "₹45,600", ["₹44,400", "₹36,000", "₹33,600"],
  "Fee first; then split the remainder into an equal part and a capital-ratio part (capitals 5 : 3 : 2)",
  "Fee = ₹12,000, leaving ₹1,08,000. Equal part = 1/3 × 1,08,000 = 36,000, so ₹12,000 each. Capital part = 72,000 "
  "in the ratio 5 : 3 : 2, so B gets 3/10 × 72,000 = ₹21,600. B's total = 12,000 + 12,000 + 21,600 = ₹45,600.",
  ["Fee = 12,000", "Equal share = 12,000", "Capital share = 3/10 × 72,000 = 21,600", "B = 45,600"],
  why="₹44,400 shares all of the ₹1,08,000 in the ratio of capitals, ignoring the equal one-third; ₹36,000 gives B "
      "30% of the whole profit with no fee and no equal part; ₹33,600 leaves out B's ₹12,000 from the equal part.",
  secs=90)

# ================================================================ Mixture and Alligation (B3 I2 A1)
T = "Mixture and Alligation"
salt = 15 * F(12, 100)
add_w = salt / F(9, 100) - 15
assert add_w == 5 and salt / F(9, 100) == 20 and 15 * F(3, 12) == F(15, 4) and salt == F(18, 10)
Q(T, "Mixing solutions", B, "How many litres of water must be added to 15 litres of a 12% salt solution to make it a "
  "9% salt solution?",
  "5 litres", ["20 litres", "3.75 litres", "1.8 litres"],
  "The amount of salt does not change when water is added",
  "Salt = 12% of 15 = 1.8 litres. In the new solution 1.8 litres must be 9%, so the total is 1.8 ÷ 0.09 = 20 "
  "litres. Water to add = 20 − 15 = 5 litres.",
  ["Salt = 1.8 L", "New total = 1.8 ÷ 0.09 = 20 L", "Water added = 5 L"],
  why="20 litres is the new total volume, not the water added; 3.75 litres takes the 3-point drop as a fraction of "
      "12 (15 × 3/12); 1.8 litres is the amount of salt.", secs=45)

r_ = F(25 - 16, 40 - 25)
assert r_ == F(3, 5) and F(9, 24) == F(3, 8) and F(40, 16) == F(5, 2)
Q(T, "Alligation rule", B, "A farm store has two fertilisers: type X contains 40% nitrogen and type Y contains 16% "
  "nitrogen. In what ratio must X and Y be mixed to get a fertiliser with 25% nitrogen?",
  "3 : 5", ["5 : 3", "3 : 8", "5 : 2"],
  "Alligation: X : Y = (target − Y) : (X − target)",
  "X : Y = (25 − 16) : (40 − 25) = 9 : 15 = 3 : 5.",
  ["25 − 16 = 9", "40 − 25 = 15", "9 : 15 = 3 : 5"],
  why="5 : 3 puts the differences the wrong way round; 3 : 8 compares 9 with 40 − 16 = 24, the whole gap; 5 : 2 is "
      "just the ratio of the two strengths, 40 : 16.", secs=40)

conc = (10 * F(30, 100) + 15 * F(20, 100) + 25 * F(10, 100)) / 50
assert conc == F(17, 100) and F(30 + 20 + 10, 3) == 20 and (25 * F(30, 100) + 15 * F(20, 100) + 10 * F(10, 100)) / 50 == F(23, 100)
Q(T, "Mixing solutions", B, "10 litres of a 30% acid solution, 15 litres of a 20% acid solution and 25 litres of a "
  "10% acid solution are mixed. What is the acid concentration of the mixture?",
  "17%", ["20%", "23%", "8.5%"],
  "Concentration = total acid ÷ total volume",
  "Acid = 3 + 3 + 2.5 = 8.5 litres in 50 litres, so the concentration is 8.5 ÷ 50 = 17%.",
  ["Acid: 3 + 3 + 2.5 = 8.5 L", "Volume: 50 L", "8.5 ÷ 50 = 17%"],
  why="20% averages the three strengths without weighting by volume; 23% pairs the volumes with the wrong strengths "
      "(25 L of 30%, 10 L of 10%); 8.5% is the litres of acid, not the percentage.", secs=45)

sols = [(a, b) for a in range(1, 200) for b in range(1, 200) if 2 * a + 3 * b == 5 * 38 and 3 * a + 2 * b == 5 * 42]
assert sols == [(50, 30)]
Q(T, "Alligation rule", I, "Two varieties of tea are mixed. When they are mixed in the ratio 2 : 3 (first : second), "
  "the blend costs ₹38 per 100 g; when mixed in the ratio 3 : 2, it costs ₹42 per 100 g. What is the cost of the "
  "costlier variety per 100 g?",
  "₹50", ["₹30", "₹40", "₹42"],
  "Write two equations in the two prices: 2a + 3b = 5 × 38 and 3a + 2b = 5 × 42",
  "2a + 3b = 190 and 3a + 2b = 210. Adding: 5(a + b) = 400, so a + b = 80. Subtracting: a − b = 20. So a = ₹50 and "
  "b = ₹30; the costlier variety costs ₹50 per 100 g.",
  ["2a + 3b = 190", "3a + 2b = 210", "a + b = 80, a − b = 20", "a = 50, b = 30"],
  why="₹30 is the cheaper variety; ₹40 is the average of the two prices (a + b = 80 halved); ₹42 is the price of the "
      "second blend, not of either variety.", secs=70, by=BRUTE)

gold = 30 * F(18, 24)
x_ = next(x for x in range(0, 500) if (gold + x) / (30 + x) == F(22, 24))
assert x_ == 60 and gold == F(45, 2)
Q(T, "Mixing solutions", I, "A jeweller has 30 g of 18-carat gold (18 parts pure gold in 24). How many grams of pure "
  "(24-carat) gold must he add to make the whole 22-carat?",
  "60 g", ["15 g", "30 g", "120 g"],
  "Alligation on purity: pure : 18-carat = (22 − 18) : (24 − 22)",
  "Pure : 18-carat = (22 − 18) : (24 − 22) = 4 : 2 = 2 : 1. With 30 g of 18-carat gold, the pure gold needed is "
  "2 × 30 = 60 g. Check: gold = 22.5 + 60 = 82.5 g in 90 g = 22/24 ✓.",
  ["Alligation: 4 : 2 = 2 : 1", "Pure gold = 2 × 30 = 60 g", "Check: 82.5/90 = 22/24 ✓"],
  why="15 g reverses the alligation ratio (1 : 2); 30 g assumes equal amounts give the midway purity, which would be "
      "21 carat; 120 g takes the ratio as 4 : 1, forgetting the 24 − 22 = 2.", secs=70)

V_ = next(V for V in range(17, 500) if F(5, 8) * (V - 16) + 16 == 3 * F(3, 8) * (V - 16))
assert V_ == 48 and next(V for V in range(1, 200) if F(5, 8) * V + 16 == 3 * F(3, 8) * V) == 32
Q(T, "Replacement of mixture", A, "A vessel holds milk and water in the ratio 5 : 3. 16 litres of the mixture are "
  "drawn off and replaced with pure milk, and the ratio of milk to water becomes 3 : 1. How many litres did the "
  "vessel hold?",
  "48 litres", ["32 litres", "12 litres", "64 litres"],
  "Water changes only when mixture is drawn off: after drawing 16 L, water = 3/8 of (V − 16); milk = 5/8 of "
  "(V − 16) + 16",
  "After the replacement, water = 3/8 (V − 16) and milk = 5/8 (V − 16) + 16. Milk = 3 × water gives 5/8 (V − 16) "
  "+ 16 = 9/8 (V − 16), so 16 = 1/2 (V − 16) and V = 48 litres. Check: 32 L left (20 milk, 12 water) + 16 milk = "
  "36 : 12 = 3 : 1 ✓.",
  ["Water = 3/8 (V − 16)", "Milk = 5/8 (V − 16) + 16", "16 = ½ (V − 16) ⇒ V = 48"],
  why="32 litres forgets that the 16 litres drawn off took away milk and water (it uses 5V/8 + 16 = 9V/8); 12 litres "
      "lets milk fall but keeps the water at 3V/8; 64 litres divides 16 by 1/4, the final water share.", secs=90,
  by=BRUTE)

# ================================================================ Time and Work (B1 I4 A3)
T = "Time and Work"
rate = F(1200, 40) + F(1200, 60)
assert rate == 50 and F(3000, rate) == 60 and F(3000, 30) == 100 and F(1200, rate) == 24
Q(T, "Work efficiency", B, "Printer P prints 1,200 pages in 40 minutes and printer Q prints 1,200 pages in 60 "
  "minutes. Working together, how long will they take to print 3,000 pages?",
  "60 minutes", ["125 minutes", "100 minutes", "24 minutes"],
  "Add the rates in pages per minute, not the times",
  "P prints 1,200 ÷ 40 = 30 pages a minute and Q prints 1,200 ÷ 60 = 20. Together 50 pages a minute, so 3,000 pages "
  "take 3,000 ÷ 50 = 60 minutes.",
  ["P: 30 pages/min", "Q: 20 pages/min", "Together 50 pages/min", "3,000 ÷ 50 = 60 min"],
  why="125 minutes averages the two times (50 minutes for 1,200 pages) and scales up; 100 minutes uses printer P "
      "alone; 24 minutes is the time for 1,200 pages, not 3,000.", secs=40)

b_days = 1 / ((1 - F(8, 12)) / 8)
assert b_days == 24
Q(T, "Alternate days", I, "A can finish a job alone in 12 days. A and B work on it on alternate days, A on the first "
  "day, and the job is finished in exactly 16 days. In how many days can B alone finish it?",
  "24 days", ["16 days", "28 days", "12 days"],
  "In 16 alternate days each person works 8 days",
  "A works on 8 of the 16 days and does 8/12 = 2/3 of the job. B does the other 1/3 in his 8 days, so B alone needs "
  "8 × 3 = 24 days.",
  ["A: 8 days ⇒ 2/3", "B: 8 days ⇒ 1/3", "B alone = 24 days"],
  why="16 days is the time taken together on alternate days; 28 days gives A 9 working days (B then does 1/4 in 7 "
      "days); 12 days assumes the two are equally fast.", secs=60, by=BRUTE)

done = 20 * 10
rest = 20 * 30 - done
days = rest / (15 + F(20, 2))
assert days == 16 and 10 + days == 26 and r2(10 + rest / F(35)) == F("21.43") and r2(10 + rest / F(15)) == F("36.67")
Q(T, "Men-women-children", I, "20 men can finish a job in 30 days. After 10 days, 5 of the men leave and 20 women "
  "join. A woman does half as much work in a day as a man. In how many days in all is the job finished?",
  "26 days", ["16 days", "36.67 days", "21.43 days"],
  "Count work in man-days; convert the women to men (2 women = 1 man)",
  "Total work = 20 × 30 = 600 man-days. In 10 days, 200 are done, leaving 400. The new team is 15 men + 20 women = "
  "15 + 10 = 25 men's worth, which takes 400 ÷ 25 = 16 days. Total = 10 + 16 = 26 days.",
  ["Work = 600 man-days", "Done: 200", "New team = 25 man-equivalents", "400 ÷ 25 = 16 ⇒ total 26 days"],
  why="16 days is only the time after the change; 36.67 days ignores the women (400 ÷ 15 = 26.67 days after the "
      "change); 21.43 days counts each woman as a full man (35 men).", secs=70)

a_, b_, c_ = F(1) - F(3, 4), F(3, 5) + F(3, 4) - 1, F(1) - F(3, 5)
assert (a_, b_, c_) == (F(1, 4), F(7, 20), F(2, 5)) and 24000 * b_ == 8400 and 24000 * a_ == 6000 and 24000 * c_ == 9600
Q(T, "Work and wages", I, "A, B and C together complete a job and are paid ₹24,000, shared in proportion to the work "
  "each did. A and B together did 3/5 of the work, and B and C together did 3/4 of it. What is B's share?",
  "₹8,400", ["₹8,000", "₹6,000", "₹9,600"],
  "A's part = 1 − (B + C) and C's part = 1 − (A + B); B's part is what remains",
  "A = 1 − 3/4 = 1/4 and C = 1 − 3/5 = 2/5. So B = 1 − 1/4 − 2/5 = 7/20. B's share = 7/20 × 24,000 = ₹8,400.",
  ["A = 1/4", "C = 2/5", "B = 7/20", "7/20 × 24,000 = 8,400"],
  why="₹8,000 splits the money equally; ₹6,000 is A's share (1/4); ₹9,600 is C's share (2/5).", secs=60)

t_ = next(t for t in range(1, 200) if t - F(t * 10, 14) == 8)
a_days = F(t_ * 10, 14)
tog = 1 / (1 / a_days + F(1, t_))
assert t_ == 28 and a_days == 20 and tog == F(35, 3) and 1 / (F(1, 12) + F(1, 20)) == F(15, 2) and F(20 + 28, 2) == 24
Q(T, "Work efficiency", I, "A is 40% more efficient than B and takes 8 days less than B to finish a job. In how many "
  "days can they finish it working together?",
  "11⅔ days", ["7½ days", "24 days", "20 days"],
  "Time is inversely proportional to efficiency: A's time = B's time ÷ 1.4",
  "If B takes t days, A takes t/1.4. Then t − t/1.4 = 8, so t × 0.4/1.4 = 8 and t = 28; A takes 20 days. Together: "
  "1/20 + 1/28 = 12/140, so they take 140/12 = 11⅔ days.",
  ["A = t/1.4", "t − t/1.4 = 8 ⇒ t = 28", "A = 20 days", "Together = 140/12 = 11⅔ days"],
  why="7½ days takes A's time as 40% less than B's (0.6t), giving 20 and 12 days; 24 days is the average of the two "
      "times; 20 days is A alone.", secs=70, by=BRUTE)

day, done = 0, 0
while done < 45:
    day += 1
    done += day
assert day == 9 and done == 45 and sum(range(1, 9)) == 36
Q(T, "Work efficiency", A, "One worker alone would take 45 days to finish a job. A contractor starts with one worker "
  "on day 1 and adds one more worker of the same efficiency every day (2 on day 2, 3 on day 3, and so on). On which "
  "day is the job finished?",
  "Day 9", ["Day 10", "Day 8", "Day 23"],
  "Work done by the end of day n = 1 + 2 + … + n worker-days",
  "The job needs 45 worker-days. By the end of day n, 1 + 2 + … + n = n(n + 1)/2 worker-days are done. n(n + 1)/2 = "
  "45 gives n = 9 (9 × 10 ÷ 2 = 45), so the job ends exactly on day 9.",
  ["Need 45 worker-days", "n(n + 1)/2 = 45", "n = 9"],
  why="Day 10 solves n(n + 1)/2 ≥ 45 but counts one day too many (55 worker-days by day 10); Day 8 stops at 36 "
      "worker-days, 9 short; Day 23 halves 45, as if two workers worked throughout.", secs=70, by=BRUTE)

per_day = 2 * F(1, 12) + 3 * F(1, 18)
boys = (F(1, 2) - per_day) / F(1, 36)
assert per_day == F(1, 3) and boys == 6 and F(1, 2) / F(1, 36) == 18 and (1 - per_day) * 36 == 24
assert (F(1, 2) - per_day) / F(1, 12) == 2
Q(T, "Men-women-children", A, "A man can finish a job in 12 days, a woman in 18 days and a boy in 36 days. How many "
  "boys must join 2 men and 3 women so that the job is finished in 2 days?",
  "6", ["18", "24", "2"],
  "In 2 days the team must do half the job each day",
  "2 men do 2/12 = 1/6 a day and 3 women do 3/18 = 1/6 a day, together 1/3 a day. To finish in 2 days they need "
  "1/2 a day, so the boys must do 1/2 − 1/3 = 1/6 a day. Each boy does 1/36, so 6 boys are needed.",
  ["Men + women: 1/6 + 1/6 = 1/3 per day", "Needed: 1/2 per day", "Boys: 1/6 ÷ 1/36 = 6"],
  why="18 leaves out the men and women (1/2 ÷ 1/36); 24 aims to finish in one day (1 − 1/3 = 2/3, × 36); 2 treats "
      "each boy as doing a man's work (1/6 ÷ 1/12).", secs=80)

b_rate = F(1, 12) - F(1, 20)
c_work = 1 - 4 * F(1, 12) - 6 * b_rate
assert b_rate == F(1, 30) and c_work == F(7, 15) and 18000 * c_work == 8400 and 18000 * 6 * b_rate == 3600
Q(T, "Work and wages", A, "A and B together can finish a job in 12 days, and A alone in 20 days. They work together "
  "for 4 days; then A leaves and C joins B, and B and C finish the job in another 6 days. The payment of ₹18,000 is "
  "shared in proportion to the work done. What is C's share?",
  "₹8,400", ["₹6,000", "₹3,600", "₹12,000"],
  "Find B's rate from A + B; C's work is whatever is left after A's and B's contributions",
  "B's rate = 1/12 − 1/20 = 1/30. In 4 days A and B do 4/12 = 1/3. B then works 6 more days: 6/30 = 1/5. C does the "
  "rest: 1 − 1/3 − 1/5 = 7/15. C's share = 7/15 × 18,000 = ₹8,400.",
  ["B = 1/30 per day", "First 4 days: 1/3", "B's last 6 days: 1/5", "C = 7/15 ⇒ ₹8,400"],
  why="₹6,000 splits the money equally among three; ₹3,600 is B's pay for his last 6 days (1/5); ₹12,000 gives C all "
      "of the last 2/3 of the job, forgetting B's part in it.", secs=90)

# ================================================================ Pipes and Cisterns (B1 I1 A1)
T = "Pipes and Cisterns"
assert F(3 * 8, 4) == 6 and F(8 * 4, 3) == F(32, 3) and 3 * 8 == 24
Q(T, "Inlet and outlet", B, "Three identical pipes together fill a tank in 8 hours. How long will four such pipes "
  "take to fill it?",
  "6 hours", ["10⅔ hours", "2 hours", "24 hours"],
  "More pipes, less time: the time varies inversely as the number of pipes",
  "Work = 3 × 8 = 24 pipe-hours. Four pipes take 24 ÷ 4 = 6 hours.",
  ["Work = 24 pipe-hours", "24 ÷ 4 = 6 hours"],
  why="10⅔ hours treats time as rising with the number of pipes (8 × 4/3); 2 hours divides 8 by 4; 24 hours is the "
      "time one pipe alone would take.", secs=35)

b_ = 1 / (F(1, 30))
assert b_ == 30 and 1 / (F(1, 10) - F(1, 30)) == 15 and 1 / (F(1, 10) + F(1, 30)) == F(15, 2)
Q(T, "Leak problems", I, "Pipe A alone fills a tank in 10 hours. A leak develops that alone would empty the full tank "
  "in 30 hours. A second pipe B is opened along with A so that the tank still fills in 10 hours. How long would B "
  "alone take to fill the tank?",
  "30 hours", ["15 hours", "10 hours", "7.5 hours"],
  "For the filling time to stay at 10 hours, B must exactly cancel the leak",
  "A + B − leak must equal A's rate 1/10, so B = leak = 1/30 of the tank per hour. B alone fills it in 30 hours.",
  ["Needed net rate = 1/10", "1/10 + B − 1/30 = 1/10", "B = 1/30 ⇒ 30 hours"],
  why="15 hours sets B equal to A's rate minus the leak (1/10 − 1/30); 10 hours assumes B must match A; 7.5 hours "
      "sets B to A's rate plus the leak (1/10 + 1/30).", secs=60)

c_ = F(1, 12) + F(1, 15) - F(1, 20)
assert c_ == F(1, 10) and 1 / (c_ - F(1, 12)) == 60 and r2(1 / ((F(1, 12) + F(1, 15) + F(1, 20)) - F(1, 12))) == F("8.57")
assert 1 / (F(1, 12) - F(1, 20)) == 30
Q(T, "Inlet and outlet", A, "A tank has two inlet pipes A and B, which fill it in 12 hours and 15 hours, and an "
  "outlet pipe C. With all three open, the empty tank fills in 20 hours. If the tank is full and only A and C are "
  "open, how long will it take to empty?",
  "60 hours", ["10 hours", "8.57 hours", "30 hours"],
  "Find C's rate from the three-pipe information first",
  "A + B − C = 1/20, so C = 1/12 + 1/15 − 1/20 = (5 + 4 − 3)/60 = 1/10. With A and C open, the net rate is 1/12 − "
  "1/10 = −1/60, so the full tank empties in 60 hours.",
  ["C = 1/12 + 1/15 − 1/20 = 1/10", "A − C = 1/12 − 1/10 = −1/60", "Empties in 60 hours"],
  why="10 hours is C alone, ignoring that A keeps filling; 8.57 hours takes C = 1/12 + 1/15 + 1/20 (adding the "
      "1/20 instead of subtracting it); 30 hours uses the three-pipe rate 1/20 as C's rate (1/12 − 1/20).", secs=85)

# ================================================================ Speed, Time and Distance (B2 I2 A2)
T = "Speed, Time and Distance"


def bounce_meetings(L, va, vb, tmax, dt=F(1, 8)):
    """Exact meeting times of two walkers starting at 0 and L, turning back at the ends (event-based)."""
    # positions are piecewise linear; check each small interval for a crossing using exact arithmetic
    def pos(v, start, t):
        d = (v * t + (0 if start == 0 else L)) % (2 * L) if start == 0 else (L - v * t) % (2 * L)
        return d if d <= L else 2 * L - d
    out, t = [], F(0)
    while t < tmax and len(out) < 5:
        a0, b0 = pos(va, 0, t), pos(vb, L, t)
        a1, b1 = pos(va, 0, t + dt), pos(vb, L, t + dt)
        if (a0 - b0) * (a1 - b1) < 0 or a1 == b1:
            lo, hi = t, t + dt
            for _ in range(60):
                mid = (lo + hi) / 2
                if (pos(va, 0, lo) - pos(vb, L, lo)) * (pos(va, 0, mid) - pos(vb, L, mid)) <= 0:
                    hi = mid
                else:
                    lo = mid
            out.append(round(float(hi), 6))
        t += dt
    return out


avg = F(24 + 36, 2 + F(1, 2) + 2)
assert avg == F(40, 3) and F(60, 4) == 15 and F(2 * 12 * 18, 30) == F(72, 5) and r2(F(60) / F("4.3")) == F("13.95")
Q(T, "Average speed", B, "A cyclist rides 24 km at 12 km/h, rests for 30 minutes, and then rides 36 km at 18 km/h. "
  "What is his average speed for the whole trip, including the rest?",
  "13⅓ km/h", ["15 km/h", "14.4 km/h", "13.95 km/h"],
  "Average speed = total distance ÷ total time, and the rest counts as time",
  "Riding time = 24 ÷ 12 + 36 ÷ 18 = 2 + 2 = 4 hours; with the rest, 4.5 hours. Distance = 60 km. Average speed = "
  "60 ÷ 4.5 = 13⅓ km/h.",
  ["Time: 2 h + 0.5 h + 2 h = 4.5 h", "Distance = 60 km", "60 ÷ 4.5 = 13⅓ km/h"],
  why="15 km/h leaves out the rest (60 ÷ 4); 14.4 km/h uses the equal-distance formula 2 × 12 × 18 ÷ 30, but the "
      "two distances differ and the rest is ignored; 13.95 km/h reads 30 minutes as 0.3 hour.", secs=45)

assert F(120, F(12, 5)) == 50 and 40 * F(6, 5) == 48 and F(120, 2) == 60 and r2(F(120) / F("2.24")) == F("53.57")
Q(T, "Average speed", B, "A car covers a distance in 3 hours at 40 km/h. At what speed must it travel to cover the "
  "same distance in 2 hours 24 minutes?",
  "50 km/h", ["48 km/h", "60 km/h", "53.57 km/h"],
  "Distance = 40 × 3 = 120 km; 2 hours 24 minutes = 2.4 hours",
  "Distance = 120 km. 2 h 24 min = 2 + 24/60 = 2.4 hours. Speed = 120 ÷ 2.4 = 50 km/h.",
  ["Distance = 120 km", "2 h 24 min = 2.4 h", "120 ÷ 2.4 = 50 km/h"],
  why="48 km/h raises the speed by 20% because the time falls by 20%, but speed must rise by 25% (3 ÷ 2.4 = 1.25); "
      "60 km/h uses 2 hours; 53.57 km/h reads 2 hours 24 minutes as 2.24 hours.", secs=40)

m = bounce_meetings(F(1000), F(5), F(3), F(600))
assert m[:2] == [125.0, 375.0]
Q(T, "Meeting and overtaking", I, "A and B start at the same moment from the two ends of a straight 1 km track and run "
  "towards each other at 5 m/s and 3 m/s. Each turns back at once on reaching an end and keeps running. After how "
  "many seconds do they meet for the second time?",
  "375 seconds", ["125 seconds", "250 seconds", "500 seconds"],
  "Between the start and the n-th meeting (head-on), together they cover (2n − 1) lengths of the track",
  "For the first meeting they cover 1 km together at 8 m/s: 125 s. For the second meeting they cover 3 km "
  "together: 3,000 ÷ 8 = 375 s. (A turns at 200 s; B turns at 333⅓ s; they meet 125 m from A's start at 375 s.)",
  ["1st meeting: 1,000 ÷ 8 = 125 s", "2nd meeting: 3,000 ÷ 8 = 375 s"],
  why="125 seconds is the first meeting; 250 seconds assumes they cover 2 km together, as if they met again after "
      "each covering one more length; 500 seconds uses the difference of the speeds (1,000 ÷ 2), as for overtaking.",
  secs=70, by=BRUTE)

v_ = next(v for v in range(41, 200) if F(40 + v, 2) == 48)
assert v_ == 56 and next(v for v in range(41, 200) if F(2 * 40 * v, 40 + v) == 48) == 60
Q(T, "Average speed", I, "For the first half of the journey time, a car runs at 40 km/h. At what speed must it run "
  "for the second half of the time so that its average speed for the whole journey is 48 km/h?",
  "56 km/h", ["60 km/h", "64 km/h", "44 km/h"],
  "When the two parts take equal times, the average speed is the simple average of the two speeds",
  "With equal times t: distance = 40t + vt and time = 2t, so the average is (40 + v)/2 = 48, giving v = 56 km/h.",
  ["Equal times ⇒ average = (40 + v)/2", "(40 + v)/2 = 48", "v = 56 km/h"],
  why="60 km/h treats the halves as equal distances (2 × 40 × v ÷ (40 + v) = 48); 64 km/h makes up the 8 km/h "
      "shortfall twice (48 + 2 × 8); 44 km/h averages 40 and 48.", secs=60, by=BRUTE)

m = bounce_meetings(F(400), F(60), F(40), F(20))
assert m[:2] == [4.0, 12.0]
Q(T, "Meeting and overtaking", A, "At 9:00 AM two cars start towards each other from towns X and Y, 400 km apart, at "
  "60 km/h and 40 km/h. Each car, on reaching the other town, turns back at once at the same speed. At what time do "
  "they meet for the second time?",
  "9:00 PM", ["1:00 PM", "5:00 PM", "7:00 PM"],
  "Up to the n-th head-on meeting the two cars together cover (2n − 1) × 400 km",
  "First meeting: 400 ÷ 100 = 4 h, at 1:00 PM. Second meeting: together they cover 3 × 400 = 1,200 km, taking "
  "12 hours, so at 9:00 PM. (The faster car turns at Y at 3:40 PM, the slower reaches X at 7:00 PM, and they meet "
  "80 km from X.)",
  ["1st meeting after 4 h", "2nd meeting: 1,200 ÷ 100 = 12 h", "9:00 AM + 12 h = 9:00 PM"],
  why="1:00 PM is the first meeting; 5:00 PM assumes they cover only 2 × 400 km together; 7:00 PM is when the slower "
      "car reaches X, before the cars have closed the gap.", secs=90, by=BRUTE)

sols = [(v, d) for v in range(10, 200) for d in range(1, 1000)
        if F(d, v) * F(1, 4) == F(3, 4) and F(d - 30, v) * F(1, 4) == F(36, 60)]
assert sols == [(50, 150)] and (60 + 150) == 210
assert F(30, 40) * F(1, 5) == F(3, 20)
Q(T, "Average speed", A, "A train runs at its usual speed for the first 60 km of a journey and then at 4/5 of its "
  "usual speed for the rest, arriving 45 minutes late. Had the slowdown begun 30 km later, it would have arrived "
  "36 minutes late. What is the train's usual speed?",
  "50 km/h", ["40 km/h", "62.5 km/h", "200 km/h"],
  "At 4/5 of the speed a stretch takes 5/4 of the time, so the delay is 1/4 of its normal time",
  "The delay on a slowed stretch = 1/4 of its normal time. Moving the slowdown 30 km later cuts the delay by 45 − 36 "
  "= 9 minutes, so 30 km at the usual speed takes 4 × 9 = 36 minutes. Usual speed = 30 ÷ 0.6 = 50 km/h. (The slowed "
  "stretch is 150 km, so the journey is 210 km.)",
  ["Delay = ¼ × normal time of the slowed stretch", "30 km cuts the delay by 9 min", "30 km takes 36 min normally",
   "Speed = 30 ÷ 0.6 = 50 km/h"],
  why="40 km/h takes the delay as 1/5 of the normal time (the speed falls by 1/5, but the time rises by 1/4); 62.5 "
      "km/h is 5/4 of the usual speed, confusing it with the slowed speed; 200 km/h takes the 9 minutes as the whole "
      "travel time of the 30 km.", secs=110, by=BRUTE)

# ================================================================ Boats and Streams (B1 I2 A1)
T = "Boats and Streams"
up = 21 - 3 - 3
assert up == 15 and F(36, up) == F(12, 5) and F(36, 18) == 2 and r2(F(36, 21)) == F("1.71")
Q(T, "Upstream and downstream", B, "A boat's downstream speed is 21 km/h and the stream flows at 3 km/h. How long "
  "will the boat take to go 36 km upstream?",
  "2 hours 24 minutes", ["2 hours", "1 hour 43 minutes", "2 hours 40 minutes"],
  "Still-water speed = downstream − stream; upstream = still-water − stream",
  "Still-water speed = 21 − 3 = 18 km/h, so upstream speed = 18 − 3 = 15 km/h. Time = 36 ÷ 15 = 2.4 h = 2 hours 24 "
  "minutes.",
  ["Still water = 18 km/h", "Upstream = 15 km/h", "36 ÷ 15 = 2.4 h = 2 h 24 min"],
  why="2 hours subtracts the stream only once (36 ÷ 18); 1 hour 43 minutes adds the stream to get the still-water "
      "speed (24) and so uses 21 km/h upstream; 2 hours 40 minutes reads 2.4 hours as 2 h 40 min.", secs=40)

d_ = next(d for d in range(1, 200) if F(d, 8) - F(d, 16) == 1)
assert d_ == 16 and F(1, 1) / (F(1, 8) + F(1, 16)) == F(16, 3) and 1 / (F(1, 8) - F(1, 12)) == 24
Q(T, "Speed of stream", I, "A boat whose speed in still water is 12 km/h takes 1 hour longer to go upstream to a place "
  "than to come back downstream. The stream flows at 4 km/h. How far is the place?",
  "16 km", ["5⅓ km", "24 km", "8 km"],
  "Upstream speed 8 km/h, downstream 16 km/h; the difference of the two times is 1 hour",
  "d/8 − d/16 = 1, so d/16 = 1 and d = 16 km. Check: 16 ÷ 8 = 2 h up and 16 ÷ 16 = 1 h down.",
  ["Up 8 km/h, down 16 km/h", "d/8 − d/16 = 1", "d = 16 km"],
  why="5⅓ km takes 1 hour as the total time for both legs; 24 km uses the still-water speed for the return "
      "(d/8 − d/12 = 1); 8 km multiplies the 8 km/h gap between the two speeds by 1 hour.", secs=55, by=BRUTE)

u0, d0 = F(30) / F(15, 4), F(30) / F(5, 2)
still, stream = (u0 + d0) / 2, (d0 - u0) / 2
new_up = still * F(6, 5) - stream
assert (u0, d0, still, stream) == (8, 12, 10, 2) and F(30) / new_up == 3
assert F(15, 4) / F(6, 5) == F(25, 8) and F(30, 12) == F(5, 2) and r2(F(30) / F("14.4")) == F("2.08")
Q(T, "Upstream and downstream", I, "A boat takes 3 hours 45 minutes to go 30 km upstream and 2 hours 30 minutes to "
  "come back. If its speed in still water is raised by 20% (the stream unchanged), how long will the 30 km upstream "
  "trip take?",
  "3 hours", ["3 hours 7½ minutes", "2 hours 30 minutes", "2 hours 5 minutes"],
  "Find the still-water and stream speeds first; only the still-water speed changes",
  "Upstream speed = 30 ÷ 3.75 = 8 km/h; downstream = 30 ÷ 2.5 = 12 km/h. Still water = 10 km/h, stream = 2 km/h. "
  "New still-water speed = 12 km/h, so upstream = 12 − 2 = 10 km/h and the trip takes 30 ÷ 10 = 3 hours.",
  ["Up 8, down 12 ⇒ still 10, stream 2", "New still speed = 12", "New upstream = 10 km/h", "30 ÷ 10 = 3 h"],
  why="3 hours 7½ minutes cuts the old time by 1/1.2, as if the upstream speed rose by 20%; 2 hours 30 minutes uses "
      "the new still-water speed and ignores the stream; 2 hours 5 minutes raises the downstream speed by 20% "
      "(30 ÷ 14.4).", secs=70)

gap = (12 - 4) * F(3, 2)
t_ = gap / ((20 - 4) - (12 - 4))
assert gap == 12 and t_ == F(3, 2)
assert (12 * F(3, 2)) / (20 - 12) == F(9, 4) and ((12 + 4) * F(3, 2)) / 8 == 3 and gap / (16 + 8) == F(1, 2)
Q(T, "Upstream and downstream", A, "A boat leaves a jetty at 6:00 AM and goes upstream; its speed in still water is "
  "12 km/h. At 7:30 AM a speedboat (20 km/h in still water) leaves the same jetty to catch it. The stream flows at "
  "4 km/h. At what time does the speedboat catch the boat?",
  "9:00 AM", ["9:45 AM", "10:30 AM", "8:00 AM"],
  "Both move upstream: subtract the stream from each speed; the chase closes at the difference",
  "Upstream speeds: boat 12 − 4 = 8 km/h, speedboat 20 − 4 = 16 km/h. By 7:30 AM the boat is 8 × 1.5 = 12 km ahead. "
  "The gap closes at 16 − 8 = 8 km/h, taking 1.5 hours. So the speedboat catches it at 9:00 AM.",
  ["Upstream: 8 and 16 km/h", "Head start = 12 km", "Closing speed = 8 km/h", "12 ÷ 8 = 1.5 h ⇒ 9:00 AM"],
  why="9:45 AM ignores the stream (head start 18 km, closing 8 km/h); 10:30 AM adds the stream as if going "
      "downstream (head start 24 km); 8:00 AM adds the two speeds (closing at 24 km/h), as for boats approaching each "
      "other.", secs=85)

# ================================================================ Problems on Trains (B1 I2 A1)
T = "Problems on Trains"
v_ = F(180 + 120, 20)
assert v_ == 15 and v_ * F(18, 5) == 54 and F(120, 20) * F(18, 5) == F(108, 5) and F(180, 20) * F(18, 5) == F(162, 5)
Q(T, "Crossing a pole or platform", B, "A train 180 m long passes completely through a 120 m long platform in 20 "
  "seconds. What is its speed?",
  "54 km/h", ["21.6 km/h", "32.4 km/h", "15 km/h"],
  "Distance covered = length of train + length of platform; 1 m/s = 3.6 km/h",
  "Distance = 180 + 120 = 300 m in 20 s, so speed = 15 m/s = 15 × 3.6 = 54 km/h.",
  ["Distance = 300 m", "300 ÷ 20 = 15 m/s", "15 × 18/5 = 54 km/h"],
  why="21.6 km/h counts only the platform (120 m); 32.4 km/h counts only the train (180 m); 15 km/h forgets to "
      "convert 15 m/s to km/h.", secs=40)

v_ = F(72 * 5, 18)
assert v_ == 20 and F(450 - 150, v_) == 15 and F(600, v_) == 30 and F(450, v_) == F(45, 2) and F(150, v_) == F(15, 2)
Q(T, "Crossing a pole or platform", I, "A 150 m long train running at 72 km/h passes through a 450 m long tunnel. For "
  "how many seconds is the whole train inside the tunnel?",
  "15 seconds", ["30 seconds", "22.5 seconds", "7.5 seconds"],
  "The train is wholly inside from when its rear enters until its front reaches the exit: 450 − 150 m",
  "Speed = 72 km/h = 20 m/s. The whole train is inside while its front moves from 150 m into the tunnel to the exit, "
  "a distance of 450 − 150 = 300 m, which takes 300 ÷ 20 = 15 seconds.",
  ["72 km/h = 20 m/s", "Fully inside for 450 − 150 = 300 m", "300 ÷ 20 = 15 s"],
  why="30 seconds is the time to pass completely through the tunnel (600 m); 22.5 seconds uses the tunnel length "
      "alone; 7.5 seconds is the time for the train to enter (its own length).", secs=60)

rel = F(250, 8) * F(18, 5)
assert rel == F(225, 2) and rel - 45 == F(135, 2) and rel + 45 == F(315, 2) and F(250, 8) - F(45 * 5, 18) == F(75, 4)
Q(T, "Trains crossing each other", I, "A passenger sitting in a train running at 45 km/h notices that a 250 m long "
  "train coming from the opposite direction on the parallel track takes 8 seconds to pass him. What is the speed of "
  "the other train?",
  "67.5 km/h", ["112.5 km/h", "157.5 km/h", "18.75 km/h"],
  "For a passenger (a point), only the other train's length is covered, at the sum of the two speeds",
  "Relative speed = 250 ÷ 8 = 31.25 m/s = 112.5 km/h. Since the trains move in opposite directions, the other train's "
  "speed = 112.5 − 45 = 67.5 km/h.",
  ["Relative speed = 31.25 m/s = 112.5 km/h", "Opposite directions: add speeds", "112.5 − 45 = 67.5 km/h"],
  why="112.5 km/h is the relative speed, not the train's own speed; 157.5 km/h treats the trains as moving in the "
      "same direction (adds 45); 18.75 km/h subtracts 45 km/h (12.5 m/s) from 31.25 m/s and leaves the answer in m/s.",
  secs=60)

sols = [(L, v) for L in range(10, 1000) for v in range(1, 100) if L + 200 == 25 * v and L + 300 == 20 * (v + 10)]
assert sols == [(300, 20)] and 20 * F(18, 5) == 72 and 30 * F(18, 5) == 108 and F(300, 20) - 10 == 5
Q(T, "Trains crossing each other", A, "A train passes a 200 m long platform in 25 seconds. The same train passes a "
  "300 m long train coming the other way at 36 km/h in 20 seconds. What is the speed of the first train?",
  "72 km/h", ["20 km/h", "108 km/h", "18 km/h"],
  "Write both crossings with the unknown length L: L + 200 = 25v and L + 300 = 20(v + 10), v in m/s",
  "36 km/h = 10 m/s. From the platform, L = 25v − 200. Against the other train, L + 300 = 20(v + 10), so "
  "25v − 200 + 300 = 20v + 200, giving 5v = 100 and v = 20 m/s = 72 km/h (and L = 300 m).",
  ["36 km/h = 10 m/s", "L = 25v − 200", "25v + 100 = 20v + 200 ⇒ v = 20 m/s", "= 72 km/h"],
  why="20 km/h forgets to convert 20 m/s; 108 km/h is the relative speed of the two trains (30 m/s); 18 km/h ignores "
      "the first train's own length in the second crossing (300 = 20(v + 10) gives v = 5 m/s).", secs=95, by=BRUTE)

# ================================================================ Mensuration (B1 I2 A2)
T = "Mensuration"
PI = F(22, 7)
r_ = F(132) / (2 * PI)
assert r_ == 21 and PI * r_ ** 2 == 1386 and 132 * r_ == 2772 and PI * 42 ** 2 == 5544 and PI * r_ == 66
Q(T, "2D areas and perimeters", B, "The circumference of a circular pond is 132 m. What is its area? (Use π = 22/7.)",
  "1,386 m²", ["2,772 m²", "5,544 m²", "66 m²"],
  "Find the radius from C = 2πr, then use A = πr²",
  "2πr = 132 gives r = 132 × 7 ÷ 44 = 21 m. Area = 22/7 × 21 × 21 = 1,386 m².",
  ["r = 132 ÷ (2 × 22/7) = 21 m", "Area = 22/7 × 441", "= 1,386 m²"],
  why="2,772 m² multiplies the circumference by the radius, forgetting the ½ in A = ½ × C × r; 5,544 m² uses the "
      "diameter 42 m as the radius; 66 m² is πr, half the circumference.", secs=40)

r_ = F(44) / (2 * PI)
V = PI * r_ ** 2 * 18
r_b = F(18) / (2 * PI)
assert r_ == 7 and V == 2772 and PI * r_b ** 2 * 44 == 1134 and PI * 14 ** 2 * 18 == 11088 and 44 * 18 == 792
Q(T, "Cylinder, cone and sphere", I, "A rectangular sheet of paper 44 cm × 18 cm is rolled along its length to form "
  "an open cylinder of height 18 cm. What is the volume of the cylinder? (Use π = 22/7.)",
  "2,772 cm³", ["1,134 cm³", "11,088 cm³", "792 cm³"],
  "Rolling along the length makes the 44 cm side the circumference of the base",
  "2πr = 44 gives r = 7 cm. Volume = πr²h = 22/7 × 49 × 18 = 2,772 cm³.",
  ["Circumference = 44 ⇒ r = 7 cm", "h = 18 cm", "V = 22/7 × 49 × 18 = 2,772 cm³"],
  why="1,134 cm³ rolls the other way (18 cm as the circumference, height 44 cm); 11,088 cm³ takes 14 cm, the "
      "diameter, as the radius; 792 cm³ is the area of the sheet, i.e. the curved surface in cm².", secs=60)

cyl, cone, hemi = F(1), F(1, 3), F(2, 3)
assert (cyl * 3, cone * 3, hemi * 3) == (3, 1, 2)
Q(T, "Cylinder, cone and sphere", I, "A cylinder, a cone and a hemisphere have the same base radius r, and the "
  "heights of the cylinder and the cone are also r. What is the ratio of their volumes (cylinder : cone : "
  "hemisphere)?",
  "3 : 1 : 2", ["3 : 1 : 4", "1 : 3 : 2", "1 : 1 : 1"],
  "Cylinder πr²h, cone ⅓πr²h, hemisphere ⅔πr³, with h = r",
  "Cylinder = πr³, cone = ⅓πr³, hemisphere = ⅔πr³. Ratio = 1 : ⅓ : ⅔ = 3 : 1 : 2.",
  ["Cylinder = πr³", "Cone = ⅓πr³", "Hemisphere = ⅔πr³", "3 : 1 : 2"],
  why="3 : 1 : 4 uses the volume of a whole sphere (4/3 πr³); 1 : 3 : 2 makes the cone three times the cylinder "
      "instead of one-third; 1 : 1 : 1 assumes equal radius and height mean equal volumes.", secs=50)

side = 12
assert F(side * side, 4) * 4 == 144 and F(36 * 4, 1) == 144  # (√3/4)a² = 36√3 ⇒ a² = 144
r_in2, r_out2 = F(side ** 2, 12), F(side ** 2, 3)
assert r_in2 == 12 and r_out2 == 48 and (side // 2) ** 2 == 36 and near(side / (4 * math.sqrt(3)), math.sqrt(3))
Q(T, "2D areas and perimeters", A, "The area of an equilateral triangle is 36√3 cm². What is the area of the circle "
  "inscribed in it?",
  "12π cm²", ["48π cm²", "36π cm²", "3π cm²"],
  "Side from (√3/4)a² = area; inradius of an equilateral triangle = a/(2√3)",
  "(√3/4)a² = 36√3 gives a² = 144 and a = 12 cm. Inradius = 12 ÷ (2√3) = 2√3 cm, so the incircle's area = "
  "π × (2√3)² = 12π cm².",
  ["a² = 144 ⇒ a = 12 cm", "r = a/(2√3) = 2√3 cm", "Area = π × 12 = 12π cm²"],
  short="The incircle of an equilateral triangle has area πa²/12.",
  why="48π cm² is the circumscribed circle (radius a/√3 = 4√3); 36π cm² takes the radius as half the side (6 cm); "
      "3π cm² uses a/(4√3) = √3 as the radius.", secs=80)

sa, vol = F(11, 10) ** 2 - 1, F(11, 10) ** 3 - 1
assert sa == F(21, 100) and vol == F(331, 1000) and (vol - sa) * 100 == F(121, 10)
Q(T, "Cylinder, cone and sphere", A, "The radius of a sphere is increased by 10%. By how many percentage points does "
  "the percentage increase in its volume exceed the percentage increase in its surface area?",
  "12.1", ["10", "33.1", "21"],
  "Surface area ∝ r² and volume ∝ r³",
  "Surface area grows by 1.1² − 1 = 21%. Volume grows by 1.1³ − 1 = 33.1%. The difference is 33.1 − 21 = 12.1 "
  "percentage points.",
  ["Surface area: 1.21 ⇒ +21%", "Volume: 1.331 ⇒ +33.1%", "33.1 − 21 = 12.1"],
  why="10 uses simple multiples (30% − 20%) instead of compounding; 33.1 is the rise in volume alone; 21 is the rise "
      "in surface area alone.", secs=75)

# ================================================================ Probability (B2 I2 A1)
T = "Probability"
D2 = list(itertools.product(range(1, 7), repeat=2))
p_ = F(sum(1 for a, b in D2 if (a * b) % 2 == 1), 36)
prods = {a * b for a, b in D2}
assert p_ == F(1, 4) and len(prods) == 18 and F(sum(1 for x in prods if x % 2), len(prods)) == F(1, 3)
Q(T, "Coins and dice", B, "Two fair dice are rolled. What is the probability that the product of the two numbers is "
  "odd?",
  "1/4", ["1/2", "3/4", "1/3"],
  "A product is odd only when both numbers are odd",
  "Each die shows an odd number with probability 1/2, so both are odd with probability 1/2 × 1/2 = 1/4 (9 of the 36 "
  "outcomes).",
  ["Odd × odd only", "3 × 3 = 9 outcomes", "9/36 = 1/4"],
  why="1/2 is the chance that one die is odd; 3/4 is the chance that the product is even; 1/3 counts distinct "
      "product values (6 odd values among the 18 possible products) instead of outcomes.", secs=35, by=BRUTE)

deck = [(r, s) for r in range(1, 14) for s in "SHDC"]
p_ = F(sum(1 for r, s in deck if (s in "SC" and r > 10) or (s in "HD" and r == 1)), 52)
assert p_ == F(2, 13) and F(6, 52) == F(3, 26) and F(2, 52) == F(1, 26) and F(16, 52) == F(4, 13)
Q(T, "Cards", B, "One card is drawn at random from a well-shuffled pack of 52 cards. What is the probability that it "
  "is a black face card or a red ace?",
  "2/13", ["3/26", "1/26", "4/13"],
  "Count the two groups separately; they do not overlap",
  "Black face cards: J, Q, K of spades and clubs = 6. Red aces: 2. Favourable = 8, so the probability is 8/52 = "
  "2/13.",
  ["Black face cards = 6", "Red aces = 2", "8/52 = 2/13"],
  why="3/26 counts only the black face cards; 1/26 counts only the red aces; 4/13 counts all 12 face cards and all "
      "4 aces.", secs=40, by=BRUTE)

eggs = [1] * 3 + [0] * 9
pairs = list(itertools.combinations(range(12), 2))
p_ = F(sum(1 for a, b in pairs if eggs[a] or eggs[b]), len(pairs))
assert p_ == F(5, 11) and F(36, 66) == F(6, 11) and F(3, 66) == F(1, 22)
Q(T, "Balls from bags", I, "A tray of 12 eggs contains 3 rotten ones. Two eggs are picked at random together. What is "
  "the probability that at least one of them is rotten?",
  "5/11", ["1/2", "6/11", "1/22"],
  "P(at least one) = 1 − P(none)",
  "P(neither rotten) = C(9, 2)/C(12, 2) = 36/66 = 6/11. So P(at least one rotten) = 1 − 6/11 = 5/11.",
  ["C(12, 2) = 66", "C(9, 2) = 36", "1 − 36/66 = 30/66 = 5/11"],
  why="1/2 adds 3/12 + 3/12 as if the two picks could not overlap; 6/11 is the probability that neither is rotten; "
      "1/22 is the probability that both are rotten.", secs=55, by=BRUTE)

diff_ = [(a, b) for a, b in D2 if a != b]
p_ = F(sum(1 for a, b in diff_ if a + b == 7), len(diff_))
assert p_ == F(1, 5) and F(6, 36) == F(1, 6) and F(3, 30) == F(1, 10) and F(6, 15) == F(2, 5)
Q(T, "Coins and dice", I, "Two fair dice are rolled and they show different numbers. Given this, what is the "
  "probability that the sum of the numbers is 7?",
  "1/5", ["1/6", "1/10", "2/5"],
  "Restrict the sample space to the 30 ordered outcomes with different numbers",
  "Outcomes with different numbers: 36 − 6 = 30. All 6 outcomes with sum 7 ((1, 6), (2, 5), …, (6, 1)) have "
  "different numbers. P = 6/30 = 1/5.",
  ["Sample space: 30 outcomes", "Sum 7: 6 outcomes", "6/30 = 1/5"],
  why="1/6 ignores the given condition (6/36); 1/10 counts sum-7 pairs unordered (3) but the outcomes ordered (30); "
      "2/5 counts them ordered (6) but the outcomes unordered (15).", secs=60, by=BRUTE)

toss = list(itertools.product("HT", repeat=6))
p_ = F(sum(1 for t in toss if t.count("H") > 3), 64)
assert p_ == F(11, 32) and F(math.comb(6, 4), 64) == F(15, 64) and F(sum(math.comb(6, k) for k in (3, 4, 5, 6)), 64) == F(21, 32)
Q(T, "Coins and dice", A, "A fair coin is tossed 6 times. What is the probability of getting more heads than tails?",
  "11/32", ["1/2", "15/64", "21/32"],
  "More heads than tails in 6 tosses means 4, 5 or 6 heads; count with C(6, k)",
  "Favourable outcomes = C(6, 4) + C(6, 5) + C(6, 6) = 15 + 6 + 1 = 22 out of 2⁶ = 64. P = 22/64 = 11/32.",
  ["4 heads: 15", "5 heads: 6", "6 heads: 1", "22/64 = 11/32"],
  short="By symmetry P(more H) = P(more T) = (1 − P(3 heads))/2 = (1 − 20/64)/2 = 11/32.",
  why="1/2 forgets the ties (3 heads and 3 tails, 20/64); 15/64 counts only exactly 4 heads; 21/32 includes the ties "
      "(3 or more heads).", secs=75, by=BRUTE)

# ================================================================ Permutation and Combination (B1 I1 A1)
T = "Permutation and Combination"
n_ = len(list(itertools.product(range(1, 6), repeat=3)))
assert n_ == 125 and math.perm(5, 3) == 60 and math.comb(5, 3) * 1 + 5 == 15 and 3 ** 5 == 243
Q(T, "Arrangements", B, "How many three-digit numbers can be formed from the digits 1, 2, 3, 4 and 5 if digits may "
  "be repeated?",
  "125", ["60", "15", "243"],
  "Each of the three places can be filled in 5 ways when repetition is allowed",
  "Hundreds, tens and units can each take any of the 5 digits: 5 × 5 × 5 = 125.",
  ["5 choices for each place", "5³ = 125"],
  why="60 forbids repetition (5 × 4 × 3); 15 adds 5 + 5 + 5 instead of multiplying; 243 is 3⁵, the exponent and base "
      "swapped.", secs=35, by=BRUTE)

perms = set(itertools.permutations("DEBIT"))
cnt = sum(1 for p in perms if p.index("E") < p.index("I"))
assert len(perms) == 120 and cnt == 60 and math.factorial(4) == 24 and 2 * math.factorial(4) == 48
Q(T, "Word arrangements", I, "In how many arrangements of the letters of the word DEBIT does the vowel E come before "
  "the vowel I (not necessarily next to it)?",
  "60", ["120", "24", "48"],
  "In exactly half of all arrangements E comes before I",
  "DEBIT has 5 different letters, so 5! = 120 arrangements. By symmetry, E is before I in exactly half: 60.",
  ["Total = 5! = 120", "E before I in half of them", "= 60"],
  why="120 counts all arrangements; 24 makes E and I a single block 'EI' (adjacent and in order); 48 lets the block "
      "be EI or IE, i.e. counts the vowels together.", secs=55, by=BRUTE)

people = ["H1", "W1", "H2", "W2", "H3", "W3"]


def canon(seat):
    k = seat.index("H1")
    return tuple(seat[k:] + seat[:k])


ok = set()
for p in itertools.permutations(people):
    if all(abs(p.index(f"H{i}") - p.index(f"W{i}")) in (1, 5) for i in (1, 2, 3)):
        ok.add(canon(list(p)))
assert len(ok) == 16 and math.factorial(3) * 8 == 48 and math.factorial(5) == 120
Q(T, "Arrangements", A, "Three married couples sit around a circular table. In how many ways can they be seated so "
  "that each husband sits next to his wife? (Seatings that are rotations of each other are the same.)",
  "16", ["48", "8", "120"],
  "Treat each couple as one unit: (3 − 1)! circular arrangements of the units, times 2 for each couple's order",
  "Three couple-units around a table: (3 − 1)! = 2 ways. Each couple can sit in 2 orders: 2³ = 8. Total = 2 × 8 = 16.",
  ["Units around table: 2! = 2", "Orders within couples: 2³ = 8", "2 × 8 = 16"],
  why="48 arranges the three units in a row (3! × 8), ignoring that rotations are the same; 8 forgets to arrange the "
      "units around the table; 120 is (6 − 1)!, all circular seatings with no condition.", secs=75, by=BRUTE)

# ================================================================ Tabular DI (B2 I5 A2): sets of 5 and 4
T = "Tabular DI"
FISH = {"Veraval": (120, 8, 450, 180), "Kochi": (150, 6, 520, 220), "Paradip": (90, 10, 380, 160),
        "Tuticorin": (110, 7, 600, 200), "Malpe": (80, 9, 500, 240)}
sid = stimulus("data_table", "Fish landed at five fishing harbours, October 2026",
               "The table shows, for five fishing harbours in October 2026, the number of boats that went out, the "
               "average number of trips per boat in the month, the average catch per trip (kg) and the average price "
               "the catch fetched (₹ per kg).\n\n" +
               md_table(["Harbour", "Boats", "Trips per boat", "Catch per trip (kg)", "Price (₹ per kg)"],
                        [[k, b, t, c, p] for k, (b, t, c, p) in FISH.items()]),
               {"columns": ["harbour", "boats", "trips_per_boat", "catch_per_trip_kg", "price_rs_per_kg"],
                "rows": [[k, *v] for k, v in FISH.items()]})
trips = {k: b * t for k, (b, t, c, p) in FISH.items()}
catch = {k: b * t * c for k, (b, t, c, p) in FISH.items()}
assert catch == {"Veraval": 432000, "Kochi": 468000, "Paradip": 342000, "Tuticorin": 462000, "Malpe": 360000}
assert catch["Malpe"] == 360000 and 80 * 500 == 40000 and 9 * 500 == 4500
Q(T, "Single table", B, "How many tonnes of fish were landed at Malpe in October 2026? (1 tonne = 1,000 kg)",
  "360 tonnes", ["40 tonnes", "3,600 tonnes", "4.5 tonnes"],
  "Total catch = boats × trips per boat × catch per trip",
  "Malpe: 80 boats × 9 trips × 500 kg = 3,60,000 kg = 360 tonnes.",
  ["80 × 9 = 720 trips", "720 × 500 kg = 3,60,000 kg", "= 360 tonnes"],
  why="40 tonnes leaves out the trips per boat (80 × 500 kg); 3,600 tonnes divides by 100 instead of 1,000; 4.5 "
      "tonnes is one boat's catch for the month (9 × 500 kg).", secs=40, stim=sid)

assert unique_max(catch) == "Kochi" and max(FISH, key=lambda k: FISH[k][2]) == "Tuticorin"
assert max(FISH, key=lambda k: FISH[k][1]) == "Paradip" and max(FISH, key=lambda k: FISH[k][0]) == "Kochi"
Q(T, "Single table", I, "Which harbour landed the largest quantity of fish in October 2026?",
  "Kochi", ["Tuticorin", "Veraval", "Paradip"],
  "Compare boats × trips × catch per trip for every harbour",
  "Totals (kg): Veraval 120 × 8 × 450 = 4,32,000; Kochi 150 × 6 × 520 = 4,68,000; Paradip 90 × 10 × 380 = "
  "3,42,000; Tuticorin 110 × 7 × 600 = 4,62,000; Malpe 80 × 9 × 500 = 3,60,000. Kochi is the largest.",
  ["Veraval 4,32,000", "Kochi 4,68,000", "Paradip 3,42,000", "Tuticorin 4,62,000", "Malpe 3,60,000"],
  why="Tuticorin has the largest catch per trip and comes a close second (4,62,000 kg); Veraval makes the most trips "
      "(960) but has a smaller catch per trip; Paradip has the most trips per boat but the smallest catch "
      "per trip.", secs=75, stim=sid)

g_ = F(catch["Kochi"] - catch["Paradip"], catch["Paradip"])
assert pct2(g_) == "36.84%" and pct2(F(126000, 468000)) == "26.92%" and pct2(F(60, 90)) == "66.67%"
Q(T, "Single table", I, "By what percentage did Kochi's catch exceed Paradip's catch in October 2026 (correct to two "
  "decimal places)?",
  "36.84%", ["26.92%", "66.67%", "13.68%"],
  "Percentage excess = difference ÷ the smaller (base) quantity × 100",
  "Kochi 4,68,000 kg, Paradip 3,42,000 kg. Difference = 1,26,000 kg. 1,26,000 ÷ 3,42,000 = 36.84%.",
  ["Kochi 4,68,000; Paradip 3,42,000", "Difference 1,26,000", "÷ 3,42,000 = 36.84%"],
  why="26.92% divides the difference by Kochi's catch instead of Paradip's; 66.67% compares only the numbers of boats "
      "(150 and 90); 13.68% misplaces the decimal point of 0.3684.", secs=60, stim=sid)

val_t = catch["Tuticorin"] * 200
assert val_t == 92400000 and 110 * 600 * 200 == 13200000 and catch["Kochi"] * 220 == 102960000
Q(T, "Single table", I, "What was the value of the fish landed at Tuticorin in October 2026?",
  "₹9.24 crore", ["₹1.32 crore", "₹92.4 crore", "₹10.30 crore"],
  "Value = total catch × price per kg; 1 crore = 1,00,00,000",
  "Tuticorin's catch = 110 × 7 × 600 = 4,62,000 kg. Value = 4,62,000 × 200 = ₹9,24,00,000 = ₹9.24 crore.",
  ["Catch = 4,62,000 kg", "× ₹200 = ₹9,24,00,000", "= ₹9.24 crore"],
  why="₹1.32 crore leaves out the 7 trips per boat; ₹92.4 crore slips one place in converting to crore; ₹10.30 crore "
      "is Kochi's value (4,68,000 × 220), read from the wrong row.", secs=60, stim=sid)

ov = F(sum(catch.values()), sum(trips.values()))
assert sum(trips.values()) == 4250 and sum(catch.values()) == 2064000 and r2(ov) == F("485.65")
assert F(450 + 520 + 380 + 600 + 500, 5) == 490 and r2(F(sum(b * c for b, t, c, p in FISH.values()), 550)) == F("494.91")
assert r2(F(2064000, 550)) == F("3752.73")
Q(T, "Single table", A, "Taking the five harbours together, what was the average catch per trip in October 2026 "
  "(correct to two decimal places)?",
  "485.65 kg", ["490 kg", "494.91 kg", "3,752.73 kg"],
  "Overall average = total catch ÷ total trips; the harbours have different numbers of trips",
  "Trips: 960 + 900 + 900 + 770 + 720 = 4,250. Catch: 20,64,000 kg. Average = 20,64,000 ÷ 4,250 = 485.65 kg.",
  ["Total trips = 4,250", "Total catch = 20,64,000 kg", "20,64,000 ÷ 4,250 = 485.65 kg"],
  why="490 kg is the simple average of the five catch-per-trip figures; 494.91 kg weights them by the number of "
      "boats instead of trips; 3,752.73 kg is the catch per boat, not per trip.", secs=90, stim=sid)

TOLL = {"Plaza 1": (4800, 65, 10), "Plaza 2": (6000, 70, 8), "Plaza 3": (3600, 55, 15), "Plaza 4": (5000, 60, 12)}
RATE = {"car": 90, "bus": 300, "truck": 420}
sid = stimulus("data_table", "Vehicles crossing four toll plazas on a highway in one day",
               "The table shows the number of vehicles that crossed four toll plazas on a highway on one day and the "
               "percentage of them that were cars and buses; all the remaining vehicles were trucks. The toll was ₹90 "
               "for a car, ₹300 for a bus and ₹420 for a truck at every plaza.\n\n" +
               md_table(["Plaza", "Vehicles", "Cars (%)", "Buses (%)"],
                        [[k, ind(n), c, b] for k, (n, c, b) in TOLL.items()]),
               {"columns": ["plaza", "vehicles", "cars_pct", "buses_pct"], "rows": [[k, *v] for k, v in TOLL.items()]})
cnt = {k: (n * F(c, 100), n * F(b, 100), n * F(100 - c - b, 100)) for k, (n, c, b) in TOLL.items()}
coll = {k: cv * 90 + bv * 300 + tv * 420 for k, (cv, bv, tv) in cnt.items()}
assert cnt["Plaza 3"] == (1980, 540, 1080) and cnt["Plaza 1"][2] == 1200
Q(T, "Table with percentages", B, "How many trucks crossed Plaza 3 on that day?",
  "1,080", ["1,980", "540", "1,200"],
  "Truck share = 100% − cars % − buses %",
  "At Plaza 3 trucks were 100 − 55 − 15 = 30% of 3,600 vehicles: 0.30 × 3,600 = 1,080.",
  ["Truck share = 30%", "30% of 3,600 = 1,080"],
  why="1,980 is the number of cars; 540 is the number of buses; 1,200 is the number of trucks at Plaza 1.", secs=40,
  stim=sid)

assert coll["Plaza 2"] == 1076400 and coll["Plaza 4"] == 1038000
assert 4200 * 90 + 480 * 300 + 1320 * 300 == 918000 and 4200 * 90 + 1320 * 420 == 932400
Q(T, "Table with percentages", I, "What was the total toll collected at Plaza 2 on that day?",
  "₹10.764 lakh", ["₹9.18 lakh", "₹9.324 lakh", "₹10.38 lakh"],
  "Find the number of each type of vehicle, multiply by its toll and add",
  "Plaza 2: cars 70% of 6,000 = 4,200, buses 8% = 480, trucks 22% = 1,320. Toll = 4,200 × 90 + 480 × 300 + "
  "1,320 × 420 = 3,78,000 + 1,44,000 + 5,54,400 = ₹10,76,400 = ₹10.764 lakh.",
  ["Cars 4,200 × 90 = 3,78,000", "Buses 480 × 300 = 1,44,000", "Trucks 1,320 × 420 = 5,54,400",
   "Total = ₹10,76,400"],
  why="₹9.18 lakh charges trucks the bus toll of ₹300; ₹9.324 lakh leaves out the buses; ₹10.38 lakh is Plaza 4's "
      "collection.", secs=70, stim=sid)

trucks = sum(c[2] for c in cnt.values())
alln = sum(n for n, c, b in TOLL.values())
assert trucks == 5000 and alln == 19400 and pct2(F(trucks, alln)) == "25.77%" and F(25 + 22 + 30 + 28, 4) == F(105, 4)
Q(T, "Table with percentages", I, "Taking all four plazas together, what percentage of the vehicles were trucks "
  "(correct to two decimal places)?",
  "25.77%", ["26.25%", "74.23%", "25.00%"],
  "Overall share = total trucks ÷ total vehicles; do not average the four percentages",
  "Trucks: 1,200 + 1,320 + 1,080 + 1,400 = 5,000. Vehicles: 4,800 + 6,000 + 3,600 + 5,000 = 19,400. Share = "
  "5,000 ÷ 19,400 = 25.77%.",
  ["Trucks = 5,000", "Vehicles = 19,400", "5,000 ÷ 19,400 = 25.77%"],
  why="26.25% is the simple average of the four truck percentages (25, 22, 30, 28), which ignores the different "
      "totals; 74.23% is the share of cars and buses; 25.00% divides 5,000 trucks by 20,000, rounding the total up.",
  secs=70, stim=sid)

car_rev = cnt["Plaza 1"][0] * 90
new = coll["Plaza 1"] - car_rev + cnt["Plaza 1"][0] * F(95, 100) * 99
chg = F(new - coll["Plaza 1"], coll["Plaza 1"])
assert coll["Plaza 1"] == 928800 and pct2(chg) == "1.36%" and pct2(F(car_rev, coll["Plaza 1"]) * F(1, 10)) == "3.02%"
assert F(11, 10) * F(95, 100) == F(1045, 1000)
Q(T, "Table with percentages", A, "At Plaza 1, the car toll is raised by 10% and, as a result, the number of cars "
  "falls by 5%; buses and trucks are unchanged. By what percentage does Plaza 1's total daily collection change "
  "(correct to two decimal places)?",
  "1.36% rise", ["4.50% rise", "5.00% rise", "3.02% rise"],
  "Only the car revenue changes, by the factor 1.10 × 0.95; weigh that change by the car share of the collection",
  "Plaza 1: 3,120 cars, 480 buses, 1,200 trucks; collection = 2,80,800 + 1,44,000 + 5,04,000 = ₹9,28,800. New car "
  "revenue = 2,964 × 99 = ₹2,93,436, up ₹12,636. Change = 12,636 ÷ 9,28,800 = 1.36% rise.",
  ["Collection = 9,28,800", "Car revenue: 2,80,800 → 2,93,436", "Rise = 12,636", "12,636 ÷ 9,28,800 = 1.36%"],
  why="4.50% is the rise in car revenue alone (1.10 × 0.95), not in the total; 5.00% subtracts 5 from 10; 3.02% "
      "applies the 10% rise to the car share of the collection but forgets the 5% fall in cars.", secs=100, stim=sid)

# ================================================================ Bar Graph DI (B2 I3 A1): one set of 6
T = "Bar Graph DI"
FERRY = {"Mon": (340, 120), "Tue": (310, 95), "Wed": (365, 140), "Thu": (290, 110), "Fri": (420, 150),
         "Sat": (510, 230)}
sid = stimulus("chart", "Adult and child tickets sold by a river ferry, Monday to Saturday",
               "The grouped bar chart shows the number of adult and child tickets sold by a river ferry service on "
               "each day of one week, Monday to Saturday (values read from the bars). An adult ticket costs ₹60 and "
               "a child ticket ₹35.\n\n" +
               md_table(["Day", "Adult tickets", "Child tickets"], [[k, a, c] for k, (a, c) in FERRY.items()]),
               {"chart_type": "bar", "x": list(FERRY),
                "series": [{"name": "Adult tickets", "values": [a for a, c in FERRY.values()]},
                           {"name": "Child tickets", "values": [c for a, c in FERRY.values()]}]})
child = sum(c for a, c in FERRY.values())
adult = sum(a for a, c in FERRY.values())
assert child == 845 and adult == 2235 and child + adult == 3080 and child - 230 == 615
Q(T, "Stacked or grouped bar", B, "How many child tickets were sold from Monday to Saturday?",
  "845", ["2,235", "3,080", "615"],
  "Add the six child bars",
  "120 + 95 + 140 + 110 + 150 + 230 = 845.",
  ["120 + 95 + 140 = 355", "110 + 150 + 230 = 490", "355 + 490 = 845"],
  why="2,235 is the adult total; 3,080 adds adults and children; 615 leaves out Saturday.", secs=35, stim=sid)

tot = {k: a + c for k, (a, c) in FERRY.items()}
assert unique_min(tot) == "Thu" and tot["Thu"] == 400 and tot["Tue"] == 405
assert min(FERRY, key=lambda k: FERRY[k][1]) == "Tue"
Q(T, "Stacked or grouped bar", B, "On which day was the total number of tickets sold the lowest?",
  "Thursday", ["Tuesday", "Monday", "Wednesday"],
  "Add the two bars for each day before comparing",
  "Totals: Mon 460, Tue 405, Wed 505, Thu 400, Fri 570, Sat 740. Thursday (400) is the lowest.",
  ["Mon 460, Tue 405, Wed 505", "Thu 400, Fri 570, Sat 740", "Lowest: Thursday"],
  why="Tuesday has the fewest child tickets and comes second-lowest (405); Monday (460) and Wednesday (505) are "
      "higher.", secs=40, stim=sid)

rev = {k: a * 60 + c * 35 for k, (a, c) in FERRY.items()}
assert rev["Sat"] == 38650 and 740 * 60 == 44400 and 740 * 35 == 25900 and 510 * 60 == 30600
Q(T, "Stacked or grouped bar", I, "What was the ferry's ticket revenue on Saturday?",
  "₹38,650", ["₹44,400", "₹25,900", "₹30,600"],
  "Revenue = adult tickets × ₹60 + child tickets × ₹35",
  "Saturday: 510 × 60 + 230 × 35 = 30,600 + 8,050 = ₹38,650.",
  ["Adults: 510 × 60 = 30,600", "Children: 230 × 35 = 8,050", "Total = ₹38,650"],
  why="₹44,400 charges every ticket the adult fare; ₹25,900 charges every ticket the child fare; ₹30,600 counts only "
      "the adult tickets.", secs=50, stim=sid)

assert pct2(F(150, 420)) == "35.71%" and pct2(F(150, 570)) == "26.32%" and pct2(F(270, 420)) == "64.29%"
Q(T, "Stacked or grouped bar", I, "On Friday, the number of child tickets was what percentage of the number of adult "
  "tickets (correct to two decimal places)?",
  "35.71%", ["26.32%", "280.00%", "64.29%"],
  "'A as a percentage of B' = A ÷ B × 100",
  "Friday: 150 child and 420 adult tickets. 150 ÷ 420 = 35.71%.",
  ["150 ÷ 420", "= 0.3571", "= 35.71%"],
  why="26.32% divides by Friday's total (570) instead of the adult tickets; 280.00% divides adults by children; "
      "64.29% is the gap between them as a share of the adult tickets (270 ÷ 420).", secs=45, stim=sid)

assert F(adult, 6) == F(745, 2) and r2(F(3080, 6)) == F("513.33") and r2(F(adult, 7)) == F("319.29") and F(adult, 5) == 447
Q(T, "Simple bar", I, "What was the average number of adult tickets sold per day from Monday to Saturday?",
  "372.5", ["513.33", "319.29", "447"],
  "Average = adult total ÷ number of days shown (6)",
  "Adult total = 340 + 310 + 365 + 290 + 420 + 510 = 2,235. Average = 2,235 ÷ 6 = 372.5.",
  ["Adult total = 2,235", "Days = 6", "2,235 ÷ 6 = 372.5"],
  why="513.33 averages all tickets (3,080 ÷ 6); 319.29 divides by 7, the days in a week, though only six days are "
      "shown; 447 divides by 5.", secs=50, stim=sid)

g_ = F(rev["Sat"] - rev["Wed"], rev["Wed"])
assert rev["Wed"] == 26800 and pct2(g_) == "44.22%" and pct2(F(740, 505) - 1) == "46.53%"
assert pct2(F(510, 365) - 1) == "39.73%" and pct2(F(11850, 38650)) == "30.66%"
Q(T, "Stacked or grouped bar", A, "By what percentage was Saturday's ticket revenue higher than Wednesday's (correct "
  "to two decimal places)?",
  "44.22%", ["46.53%", "39.73%", "30.66%"],
  "Compare revenues, not ticket counts; the two fares differ",
  "Wednesday: 365 × 60 + 140 × 35 = 21,900 + 4,900 = ₹26,800. Saturday: ₹38,650. Increase = 11,850 ÷ 26,800 = "
  "44.22%.",
  ["Wed revenue = 26,800", "Sat revenue = 38,650", "11,850 ÷ 26,800 = 44.22%"],
  why="46.53% compares the numbers of tickets (740 and 505) instead of revenue; 39.73% compares only the adult "
      "tickets; 30.66% divides the increase by Saturday's revenue instead of Wednesday's.", secs=90, stim=sid)

# ================================================================ Pie Chart DI (B3 I2 A4): sets of 5 and 4
T = "Pie Chart DI"
BAT = {"Willow (blade)": 126, "Cane handle": 51, "Labour": 72, "Grip and stickers": 18, "Varnish and finishing": 27,
       "Packing and transport": 36, "Overheads": 30}
assert sum(BAT.values()) == 360
sid = stimulus("chart", "Cost of making one cricket bat, by component (central angles)",
               "The pie chart shows how the total cost of making one cricket bat at a small factory is divided among "
               "its components; the central angle of each sector is given. The total cost of one bat is ₹2,880.\n\n" +
               md_table(["Component", "Central angle (degrees)"], [[k, v] for k, v in BAT.items()]),
               {"chart_type": "pie", "unit": "degrees", "labels": list(BAT), "values": list(BAT.values()),
                "total_cost_rs": 2880})
cost = {k: F(v, 360) * 2880 for k, v in BAT.items()}
assert cost["Willow (blade)"] == 1008 and cost["Labour"] == 576 and F(126, 360) * 100 == 35
Q(T, "Degree-based", B, "What is the cost of the willow (blade) in one bat?",
  "₹1,008", ["₹576", "₹1,260", "₹35"],
  "Cost of a component = (its angle ÷ 360°) × total cost",
  "126/360 × 2,880 = 126 × 8 = ₹1,008 (each degree stands for ₹2,880 ÷ 360 = ₹8).",
  ["₹ per degree = 2,880 ÷ 360 = 8", "126 × 8 = ₹1,008"],
  why="₹576 is the labour cost (72°), read from the wrong sector; ₹1,260 multiplies the angle by 10 instead of by "
      "₹8; ₹35 is willow's percentage share (126/360 = 35%), not its cost.", secs=35, stim=sid)

assert F(72, 360) * 100 == 20 and F(72, 288) * 100 == 25
Q(T, "Degree-based", B, "Labour accounts for what percentage of the total cost of a bat?",
  "20%", ["72%", "25%", "0.2%"],
  "Percentage share = angle ÷ 360 × 100",
  "72/360 × 100 = 20%.",
  ["72 ÷ 360 = 0.2", "= 20%"],
  why="72% reads the angle as a percentage; 25% divides by the other 288° instead of the full 360°; 0.2% forgets to "
      "multiply the fraction 0.2 by 100.", secs=30, stim=sid)

assert (36 - 18) * 8 == 144 and 36 * 8 == 288 and (36 + 18) * 8 == 432
Q(T, "Degree-based", B, "By how much does the cost of packing and transport exceed the cost of grip and stickers in "
  "one bat?",
  "₹144", ["₹18", "₹288", "₹432"],
  "Subtract the angles and convert: ₹8 per degree",
  "Difference in angle = 36° − 18° = 18°, worth 18 × 8 = ₹144.",
  ["36° − 18° = 18°", "18 × ₹8 = ₹144"],
  why="₹18 gives the difference in degrees, not rupees; ₹288 is the packing cost itself; ₹432 adds the two costs.",
  secs=35, stim=sid)

sp_ = 2880 * F(125, 100)
new_cost = 2880 + cost["Willow (blade)"] * F(20, 100)
pr_ = F(sp_ - new_cost, new_cost)
assert sp_ == 3600 and new_cost == F(154080, 50) and pct2(pr_) == "16.82%" and pct2(F(sp_ - new_cost, sp_)) == "14.40%"
assert 25 - F(35, 100) * 20 == 18
Q(T, "Degree-based", I, "The factory sells each bat at 25% above its cost. If the cost of willow rises by 20% while "
  "all other costs and the selling price stay the same, what will the profit percentage be (correct to two decimal "
  "places)?",
  "16.82%", ["18.00%", "5.00%", "14.40%"],
  "New cost = old cost + 20% of the willow cost; profit % is on the new cost",
  "Selling price = 2,880 × 1.25 = ₹3,600. Willow rises by 20% of 1,008 = ₹201.60, so the cost becomes ₹3,081.60. "
  "Profit = 518.40, which is 518.40 ÷ 3,081.60 = 16.82%.",
  ["SP = 3,600", "New cost = 2,880 + 201.60 = 3,081.60", "Profit = 518.40", "÷ 3,081.60 = 16.82%"],
  why="18.00% subtracts willow's share of the rise (35% × 20 = 7 points) from 25%, mixing percentages of different "
      "bases; 5.00% subtracts the whole 20%; 14.40% takes the profit as a percentage of the selling price.",
  secs=80, stim=sid)

oh_total = cost["Overheads"] * 5000
new_c = 2880 - cost["Overheads"] + oh_total / 6000
assert cost["Overheads"] == 240 and new_c == 2840 and 2880 * F(5, 6) == 2400 and 2880 - 240 * F(1, 5) == 2832
Q(T, "Degree-based", A, "The factory makes 5,000 bats a month, and the overheads are a fixed monthly amount equal to "
  "the overhead cost shown per bat times 5,000. If production rises to 6,000 bats a month with every other cost per "
  "bat unchanged, what will the cost of one bat be?",
  "₹2,840", ["₹2,880", "₹2,400", "₹2,832"],
  "A fixed monthly overhead is spread over more bats; only the overhead per bat changes",
  "Overhead per bat now = 30 × 8 = ₹240, so the monthly overhead = 240 × 5,000 = ₹12,00,000. Over 6,000 bats it is "
  "₹200 per bat. New cost = 2,880 − 240 + 200 = ₹2,840.",
  ["Overhead per bat = ₹240", "Monthly overhead = ₹12,00,000", "Per bat at 6,000 = ₹200", "Cost = ₹2,840"],
  why="₹2,880 keeps the overhead per bat unchanged; ₹2,400 scales the whole cost by 5/6, as if every cost were "
      "fixed; ₹2,832 cuts the overhead by one-fifth (to ₹192) instead of one-sixth.", secs=95, stim=sid)

EX = ["Bank PO", "Bank Clerk", "SSC", "Railways", "Insurance"]
P25 = dict(zip(EX, (25, 30, 20, 15, 10)))
P26 = dict(zip(EX, (28, 25, 22, 13, 12)))
assert sum(P25.values()) == 100 and sum(P26.values()) == 100
sid = stimulus("chart", "Students of a coaching institute by target exam, 2025 and 2026 (two pie charts)",
               "Two pie charts show how the students enrolled at a coaching institute were divided by the exam they "
               "were preparing for. The institute had 3,200 students in 2025 and 4,000 students in 2026.\n\n" +
               md_table(["Target exam", "2025 (% of 3,200)", "2026 (% of 4,000)"],
                        [[e, P25[e], P26[e]] for e in EX]),
               {"chart_type": "pie", "unit": "percent", "labels": EX,
                "series": [{"name": "2025", "total": 3200, "values": [P25[e] for e in EX]},
                           {"name": "2026", "total": 4000, "values": [P26[e] for e in EX]}]})
n25 = {e: 3200 * F(P25[e], 100) for e in EX}
n26 = {e: 4000 * F(P26[e], 100) for e in EX}
assert n25["Bank Clerk"] == 960 and n26["Bank Clerk"] == 1000 and pct2(F(40, 960)) == "4.17%"
assert pct2(F(5, 30)) == "16.67%"
Q(T, "Two pie charts", I, "By what percentage did the number of Bank Clerk students change from 2025 to 2026?",
  "4.17% increase", ["16.67% decrease", "5% decrease", "25% increase"],
  "Convert each year's percentage into a number of students before comparing",
  "2025: 30% of 3,200 = 960. 2026: 25% of 4,000 = 1,000. Change = 40 ÷ 960 = 4.17% increase.",
  ["2025: 960", "2026: 1,000", "40 ÷ 960 = 4.17% increase"],
  why="16.67% decrease compares the shares (25% against 30%) instead of the numbers; 5% decrease is the fall in "
      "share in percentage points; 25% increase is the growth of the whole institute.", secs=55, stim=sid)

grow = {e: F(n26[e] - n25[e], n25[e]) for e in EX}
assert unique_max(grow) == "Insurance" and grow["Insurance"] == F(1, 2) and grow["Bank PO"] == F(2, 5)
assert max(EX, key=lambda e: n26[e] - n25[e]) == "Bank PO" and max(EX, key=lambda e: n25[e]) == "Bank Clerk"
Q(T, "Two pie charts", A, "For which exam did the number of students rise by the largest percentage from 2025 to "
  "2026?",
  "Insurance", ["Bank PO", "SSC", "Bank Clerk"],
  "Compute the growth rate of each group from the actual numbers",
  "PO 800 → 1,120 (+40%); Clerk 960 → 1,000 (+4.17%); SSC 640 → 880 (+37.5%); Railways 480 → 520 (+8.33%); "
  "Insurance 320 → 480 (+50%). Insurance has the largest percentage rise.",
  ["PO +40%", "Clerk +4.17%", "SSC +37.5%", "Railways +8.33%", "Insurance +50%"],
  why="Bank PO has the largest rise in numbers (320) but only 40%; SSC rises by 37.5%; Bank Clerk had the most "
      "students in 2025 but grew only 4.17%.", secs=90, stim=sid)

FEE = {"Bank PO": 18000, "Bank Clerk": 18000, "SSC": 15000, "Railways": 15000, "Insurance": 12000}
rev26 = sum(n26[e] * FEE[e] for e in EX)
rev25 = sum(n25[e] * FEE[e] for e in EX)
assert rev26 == 64920000 and rev25 == 52320000 and 4000 * 16500 == 66000000 and 4000 * 18000 == 72000000
Q(T, "Two pie charts", A, "In 2026 the course fee was ₹18,000 for Bank PO and Bank Clerk, ₹15,000 for SSC and "
  "Railways, and ₹12,000 for Insurance. What was the institute's total fee income in 2026?",
  "₹6.492 crore", ["₹6.6 crore", "₹5.232 crore", "₹7.2 crore"],
  "Fee income = Σ (students in the group × that group's fee)",
  "2026 students: PO 1,120, Clerk 1,000, SSC 880, Railways 520, Insurance 480. Income = 2,120 × 18,000 + 1,400 × "
  "15,000 + 480 × 12,000 = 3,81,60,000 + 2,10,00,000 + 57,60,000 = ₹6,49,20,000 = ₹6.492 crore.",
  ["PO + Clerk: 2,120 × 18,000", "SSC + Railways: 1,400 × 15,000", "Insurance: 480 × 12,000",
   "Total = ₹6.492 crore"],
  why="₹6.6 crore charges every student the average of the five fees (₹16,500); ₹5.232 crore uses the 2025 numbers; "
      "₹7.2 crore charges every student ₹18,000.", secs=100, stim=sid)

lhs = n25["SSC"] + n25["Railways"]
rhs = n26["Bank PO"] + n26["Insurance"]
assert lhs == 1120 and rhs == 1600 and F(lhs, rhs) == F(7, 10) and F(20 + 15, 28 + 12) == F(7, 8)
assert n25["Bank PO"] + n25["Insurance"] == 1120
Q(T, "Two pie charts", A, "What is the ratio of the number of SSC and Railways students together in 2025 to the "
  "number of Bank PO and Insurance students together in 2026?",
  "7 : 10", ["7 : 8", "10 : 7", "1 : 1"],
  "Convert both sides to numbers of students; the two years have different totals",
  "2025: SSC 640 + Railways 480 = 1,120. 2026: PO 1,120 + Insurance 480 = 1,600. Ratio = 1,120 : 1,600 = 7 : 10.",
  ["2025 SSC + Railways = 1,120", "2026 PO + Insurance = 1,600", "1,120 : 1,600 = 7 : 10"],
  why="7 : 8 compares the percentages (35% : 40%) and ignores the different totals; 10 : 7 inverts the ratio; 1 : 1 "
      "takes PO and Insurance from 2025 (also 1,120) instead of 2026.", secs=80, stim=sid)

# ================================================================ Line Graph DI (B1 I2 A3): one set of 6
T = "Line Graph DI"
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
PET = dict(zip(MON, (84, 76, 92, 105, 118, 96)))
DSL = dict(zip(MON, (126, 120, 135, 142, 150, 130)))
sid = stimulus("chart", "Petrol and diesel sold by a highway fuel station, January to June 2026",
               "The line graph shows the quantities of petrol and diesel (in thousand litres) sold by a highway fuel "
               "station in each month from January to June 2026 (values read from the graph). Assume petrol sold at "
               "₹95 per litre and diesel at ₹88 per litre throughout.\n\n" +
               md_table(["Month (2026)", "Petrol (thousand litres)", "Diesel (thousand litres)"],
                        [[m, PET[m], DSL[m]] for m in MON]),
               {"chart_type": "line", "x": MON, "series": [{"name": "Petrol (thousand litres)",
                                                             "values": [PET[m] for m in MON]},
                                                            {"name": "Diesel (thousand litres)",
                                                             "values": [DSL[m] for m in MON]}]})
sd, sp = sum(DSL.values()), sum(PET.values())
assert sd == 803 and sp == 571 and sd + sp == 1374 and sd - 126 == 677
Q(T, "Multiple lines", B, "How much diesel did the station sell from January to June 2026?",
  "803 thousand litres", ["571 thousand litres", "1,374 thousand litres", "677 thousand litres"],
  "Add the six diesel values",
  "126 + 120 + 135 + 142 + 150 + 130 = 803 thousand litres.",
  ["126 + 120 + 135 = 381", "142 + 150 + 130 = 422", "381 + 422 = 803"],
  why="571 thousand litres is the petrol total; 1,374 adds petrol and diesel; 677 leaves out January.", secs=35,
  stim=sid)

gapm = {m: DSL[m] - PET[m] for m in MON}
assert unique_min(gapm) == "May" and gapm["Jun"] == 34 and min(PET, key=PET.get) == "Feb"
Q(T, "Multiple lines", I, "In which month was the gap between diesel sales and petrol sales the smallest?",
  "May", ["June", "April", "February"],
  "Subtract the two values month by month",
  "Gaps (thousand litres): Jan 42, Feb 44, Mar 43, Apr 37, May 32, Jun 34. The smallest is in May.",
  ["Jan 42, Feb 44, Mar 43", "Apr 37, May 32, Jun 34", "Smallest: May"],
  why="June is a close second (34); April's gap is 37; February has the lowest petrol sales but the largest gap (44).",
  secs=50, stim=sid)

assert pct2(F(118 - 76, 76)) == "55.26%" and pct2(F(42, 118)) == "35.59%" and pct2(F(118 - 84, 84)) == "40.48%"
Q(T, "Single line", I, "By what percentage did petrol sales rise from February to May 2026 (correct to two decimal "
  "places)?",
  "55.26%", ["35.59%", "42.00%", "40.48%"],
  "Percentage rise = (May − February) ÷ February × 100",
  "February 76, May 118 (thousand litres). Rise = 42 ÷ 76 = 55.26%.",
  ["Rise = 118 − 76 = 42", "42 ÷ 76 = 55.26%"],
  why="35.59% divides the rise by the May value; 42.00% gives the rise in thousand litres as if it were a percentage; "
      "40.48% measures from January (84) instead of February.", secs=50, stim=sid)

rv = PET["Apr"] * 1000 * 95 + DSL["Apr"] * 1000 * 88
assert rv == 22471000 and PET["Apr"] * 88000 + DSL["Apr"] * 95000 == 22730000
assert 247000 * 95 == 23465000 and 247000 * 88 == 21736000
Q(T, "Multiple lines", A, "What was the station's total fuel sales revenue in April 2026?",
  "₹224.71 lakh", ["₹227.30 lakh", "₹234.65 lakh", "₹217.36 lakh"],
  "Revenue = petrol litres × ₹95 + diesel litres × ₹88",
  "Petrol: 1,05,000 × 95 = ₹99,75,000. Diesel: 1,42,000 × 88 = ₹1,24,96,000. Total = ₹2,24,71,000 = ₹224.71 lakh.",
  ["Petrol: 1,05,000 × 95 = 99.75 lakh", "Diesel: 1,42,000 × 88 = 124.96 lakh", "Total = 224.71 lakh"],
  why="₹227.30 lakh swaps the two prices; ₹234.65 lakh charges all 2,47,000 litres the petrol price; ₹217.36 lakh "
      "charges them all the diesel price.", secs=75, stim=sid)

share = F(sp, sp + sd)
avg_share = sum(F(PET[m], PET[m] + DSL[m]) for m in MON) / 6
assert pct2(share) == "41.56%" and pct2(avg_share) == "41.39%" and pct2(F(sp, sd)) == "71.11%"
assert pct2(F(sd, sp + sd)) == "58.44%"
Q(T, "Multiple lines", A, "Over the six months taken together, what percentage of the fuel sold (by volume) was "
  "petrol (correct to two decimal places)?",
  "41.56%", ["41.39%", "71.11%", "58.44%"],
  "Overall share = total petrol ÷ total fuel; do not average the monthly shares",
  "Petrol = 571 and diesel = 803 thousand litres, so total fuel = 1,374. Petrol share = 571 ÷ 1,374 = 41.56%.",
  ["Petrol 571", "Total 1,374", "571 ÷ 1,374 = 41.56%"],
  why="41.39% averages the six monthly petrol shares, which gives every month equal weight; 71.11% divides petrol by "
      "diesel instead of by the total; 58.44% is diesel's share.", secs=85, stim=sid)

jul = DSL["Jun"] * F(DSL["May"], DSL["Apr"])
assert r2(jul) == F("137.32") and DSL["Jun"] + 8 == 138 and r2(150 * F(150, 142)) == F("158.45")
assert DSL["Jun"] * F(108, 100) == F("140.4")
Q(T, "Single line", A, "If diesel sales in July 2026 rise over June by the same percentage as they rose from April "
  "to May, how much diesel will be sold in July (thousand litres, correct to two decimal places)?",
  "137.32", ["138", "158.45", "140.40"],
  "Growth factor April → May = 150 ÷ 142; apply it to June's 130",
  "April to May: 142 → 150, a factor of 150/142 (about 5.63% growth). July = 130 × 150/142 = 137.32 thousand litres.",
  ["Factor = 150 ÷ 142 ≈ 1.0563", "July = 130 × 1.0563", "= 137.32"],
  why="138 adds the same 8 thousand litres instead of the same percentage; 158.45 applies the growth to May's 150 "
      "instead of June's 130; 140.40 takes the 8 thousand-litre rise as an 8% rise.", secs=80, stim=sid)

# ================================================================ Caselet DI (B5 I3 A1): sets of 5 and 4
T = "Caselet DI"
HOUSE = {"Red": (52, 28), "Blue": (46, 46), "Green": (42, 34), "Yellow": (42, 30)}  # (boys, girls)
tot_h = {k: b + g for k, (b, g) in HOUSE.items()}
assert sum(tot_h.values()) == 320 and tot_h["Red"] == 80 and tot_h["Yellow"] == 72 and tot_h["Blue"] == tot_h["Green"] + 16
assert HOUSE["Red"][1] == 80 * F(35, 100) and HOUSE["Green"][0] - HOUSE["Green"][1] == 8 and HOUSE["Yellow"][0] - HOUSE["Yellow"][1] == 12
sid = stimulus("passage", "Participants from four houses at a school's inter-house sports meet",
               "320 students took part in a school's inter-house sports meet, from the Red, Blue, Green and Yellow "
               "houses. 25% of the participants were from Red house. Yellow house sent 72 students, and Blue house "
               "sent 16 more students than Green house. 35% of Red's participants were girls. Blue sent equal numbers "
               "of boys and girls. Green sent 8 more boys than girls, and Yellow sent 12 more boys than girls.")
assert (320 - 80 - 72 - 16) // 2 + 16 == 92 and (320 - 80 - 72) // 2 == 84
Q(T, "Paragraph data", B, "How many students from Blue house took part in the meet?",
  "92", ["76", "84", "168"],
  "Blue + Green = 320 − Red − Yellow; Blue = Green + 16",
  "Red = 25% of 320 = 80. Blue + Green = 320 − 80 − 72 = 168. With Blue = Green + 16: 2 × Green + 16 = 168, so "
  "Green = 76 and Blue = 92.",
  ["Red = 80", "Blue + Green = 168", "Green = 76, Blue = 92"],
  why="76 is Green's number; 84 splits the 168 equally, ignoring the 16; 168 is Blue and Green together.", secs=45,
  stim=sid)

girls = sum(g for b, g in HOUSE.values())
assert girls == 138 and 320 - girls == 182 and girls - 34 + 42 == 146
Q(T, "Paragraph data", B, "How many girls took part in the meet in all?",
  "138", ["182", "160", "146"],
  "Work out the girls house by house",
  "Red: 35% of 80 = 28. Blue: 92 ÷ 2 = 46. Green: (76 − 8) ÷ 2 = 34. Yellow: (72 − 12) ÷ 2 = 30. Total = 28 + 46 + "
  "34 + 30 = 138.",
  ["Red 28, Blue 46", "Green 34, Yellow 30", "Total = 138"],
  why="182 is the number of boys; 160 assumes half the participants were girls; 146 takes Green's 42 boys as its "
      "girls.", secs=50, stim=sid)

assert HOUSE["Red"][0] == 52 and 320 * F(65, 100) == 208
Q(T, "Paragraph data", B, "How many boys from Red house took part?",
  "52", ["28", "65", "208"],
  "Boys = 65% of Red's 80 participants",
  "Red sent 25% of 320 = 80 students. Girls = 35% of 80 = 28, so boys = 80 − 28 = 52.",
  ["Red = 80", "Girls = 28", "Boys = 52"],
  why="28 is the number of Red girls; 65 is the boys' percentage read as a number; 208 takes 65% of all 320 "
      "participants instead of Red's 80.", secs=35, stim=sid)

assert F(HOUSE["Green"][1], HOUSE["Yellow"][0]) == F(17, 21) and F(34, 30) == F(17, 15)
Q(T, "Paragraph data", B, "What is the ratio of the number of girls from Green house to the number of boys from "
  "Yellow house?",
  "17 : 21", ["21 : 17", "17 : 15", "1 : 1"],
  "Green girls = (76 − 8)/2; Yellow boys = (72 + 12)/2",
  "Green girls = 34 and Yellow boys = 42. Ratio = 34 : 42 = 17 : 21.",
  ["Green girls = 34", "Yellow boys = 42", "34 : 42 = 17 : 21"],
  why="21 : 17 inverts the ratio; 17 : 15 uses Yellow's girls (30) instead of its boys; 1 : 1 compares Green's boys "
      "(42) with Yellow's boys (42).", secs=45, stim=sid)

assert pct2(F(46 - 30, 30)) == "53.33%" and pct2(F(16, 46)) == "34.78%"
Q(T, "Paragraph data", I, "By what percentage did the number of girls from Blue house exceed the number of girls "
  "from Yellow house (correct to two decimal places)?",
  "53.33%", ["34.78%", "16.00%", "153.33%"],
  "Excess % = difference ÷ Yellow's girls × 100",
  "Blue girls = 46, Yellow girls = 30. Difference = 16. 16 ÷ 30 = 53.33%.",
  ["Blue 46, Yellow 30", "Difference 16", "16 ÷ 30 = 53.33%"],
  why="34.78% divides the difference by Blue's 46; 16.00% gives the difference as a number, not a percentage; "
      "153.33% is Blue's girls as a percentage of Yellow's, not the excess.", secs=55, stim=sid)

SALE = {"Friday": (40, 75), "Saturday": (60, 105), "Sunday": (45, 120)}  # (pickle jars, papad packets)
assert SALE["Saturday"] == (40 * F(150, 100), 75 * F(140, 100)) and SALE["Sunday"][0] == 40 + 5
sid = stimulus("passage", "Pickle and papad sales of a self-help group at a three-day craft fair",
               "A women's self-help group sold jars of pickle and packets of papad at a three-day craft fair. A jar of "
               "pickle sold for ₹150 and cost the group ₹95 to make; a packet of papad sold for ₹60 and cost ₹38. On "
               "Friday the group sold 40 jars and 75 packets. On Saturday its pickle sales were 50% higher than on "
               "Friday and its papad sales 40% higher than on Friday. On Sunday it sold 5 more jars than on Friday "
               "and 120 packets of papad. The group paid a stall rent of ₹500 for each day of the fair.")
jars = sum(j for j, p in SALE.values())
pk = sum(p for j, p in SALE.values())
assert jars == 145 and pk == 300 and 40 + 60 == 100 and 40 + 60 + 65 == 165
Q(T, "Paragraph data", B, "How many jars of pickle did the group sell over the three days?",
  "145", ["100", "165", "300"],
  "Saturday = Friday × 1.5; Sunday = Friday + 5",
  "Friday 40, Saturday 40 × 1.5 = 60, Sunday 40 + 5 = 45. Total = 145.",
  ["Fri 40", "Sat 60", "Sun 45", "Total 145"],
  why="100 leaves out Sunday; 165 adds the 5 jars to Saturday's figure instead of Friday's; 300 is the number of "
      "papad packets.", secs=40, stim=sid)

sat = 60 * 150 + 105 * 60
assert sat == 15300 and 60 * 150 == 9000 and 60 * 55 + 105 * 22 == 5610 and 60 * 150 + 75 * 60 == 13500
Q(T, "Paragraph data", I, "What was the group's sales revenue on Saturday?",
  "₹15,300", ["₹9,000", "₹5,610", "₹13,500"],
  "Revenue = jars × ₹150 + packets × ₹60, using Saturday's quantities",
  "Saturday: 60 jars and 75 × 1.4 = 105 packets. Revenue = 60 × 150 + 105 × 60 = 9,000 + 6,300 = ₹15,300.",
  ["Jars: 60 × 150 = 9,000", "Packets: 105 × 60 = 6,300", "Revenue = 15,300"],
  why="₹9,000 counts only the pickle; ₹5,610 is Saturday's margin over making costs, not the revenue; ₹13,500 uses "
      "Friday's 75 packets of papad.", secs=50, stim=sid)

profit = jars * 55 + pk * 22 - 3 * 500
assert profit == 13075 and profit + 1500 == 14575 and profit + 1000 == 14075 and jars * 150 + pk * 60 == 39750
Q(T, "Paragraph data", I, "What was the group's profit for the three days after making costs and stall rent?",
  "₹13,075", ["₹14,575", "₹14,075", "₹39,750"],
  "Margin per jar = 150 − 95 = ₹55; per packet = 60 − 38 = ₹22; subtract three days' rent",
  "Margins: 145 jars × 55 = ₹7,975 and 300 packets × 22 = ₹6,600, total ₹14,575. Rent = 3 × 500 = ₹1,500. Profit = "
  "₹13,075.",
  ["Pickle margin = 7,975", "Papad margin = 6,600", "Rent = 1,500", "Profit = 13,075"],
  why="₹14,575 forgets the stall rent; ₹14,075 charges the rent for only one day; ₹39,750 is the total revenue, not "
      "the profit.", secs=75, stim=sid)

rise = F(15975 - profit, jars)
assert rise == 20 and r2(F(2900, 445)) == F("6.52") and r2(F(15975 - 14575, 145)) == F("9.66") and r2(F(2900, 60)) == F("48.33")
Q(T, "Paragraph data", A, "By how much should the price of a jar of pickle have been raised, with all quantities "
  "and other prices unchanged, for the group's three-day profit (after making costs and rent) to be ₹15,975?",
  "₹20", ["₹6.52", "₹9.66", "₹48.33"],
  "Extra profit needed ÷ number of jars sold",
  "Actual profit = ₹13,075. Extra needed = 15,975 − 13,075 = ₹2,900. Spread over 145 jars, each must cost ₹20 more.",
  ["Actual profit = 13,075", "Extra needed = 2,900", "2,900 ÷ 145 = ₹20"],
  why="₹6.52 spreads the extra over all 445 items, jars and packets; ₹9.66 forgets the rent and so needs only ₹1,400 "
      "extra; ₹48.33 spreads the extra over Saturday's 60 jars only.", secs=90, stim=sid)

# ================================================================ Missing DI (B1 I4 A3): two sets of 4
T = "Missing DI"
COACH = {"AC First": (48, F(75), 36, 3500), "AC 2-tier": (96, F(175, 2), 84, 2100),
         "AC 3-tier": (200, F(90), 180, 1450), "Sleeper": (480, F(90), 432, 560)}
for k, (s_, o_, p_, f_) in COACH.items():
    assert s_ * o_ / 100 == p_
assert COACH["AC 3-tier"][2] * COACH["AC 3-tier"][3] == 261000
shown = [["AC First", 48, "75%", "—", ind(3500), "—"], ["AC 2-tier", 96, "—", 84, ind(2100), "—"],
         ["AC 3-tier", 200, "90%", "—", "—", 261], ["Sleeper", 480, "—", 432, 560, "—"]]
sid = stimulus("data_table", "Seats, occupancy and fares on one run of an express train (some values missing)",
               "The table gives, for one run of an express train, the seats in each class, the percentage of seats "
               "occupied, the number of passengers, the fare per passenger and the fare revenue. Some values are "
               "missing (—); every passenger in a class paid the same fare.\n\n" +
               md_table(["Class", "Seats", "Occupancy", "Passengers", "Fare (₹)", "Revenue (₹ thousand)"], shown),
               {"columns": ["class", "seats", "occupancy_pct", "passengers", "fare_rs", "revenue_rs_thousand"],
                "rows": [[r[0], r[1], None if r[2] == "—" else float(r[2].rstrip("%")),
                          None if r[3] == "—" else r[3], None if r[4] == "—" else int(str(r[4]).replace(",", "")),
                          None if r[5] == "—" else r[5]] for r in shown]})
assert F(84, 96) * 100 == F(175, 2) and F(12, 96) * 100 == F(25, 2) and r2(F(96, 84) * 100) == F("114.29")
Q(T, "Table with missing values", B, "What was the occupancy of the AC 2-tier class?",
  "87.5%", ["12.5%", "114.29%", "84%"],
  "Occupancy = passengers ÷ seats × 100",
  "84 passengers in 96 seats: 84 ÷ 96 = 0.875 = 87.5%.",
  ["84 ÷ 96 = 0.875", "= 87.5%"],
  why="12.5% is the share of seats left empty; 114.29% divides seats by passengers; 84% reads the number of "
      "passengers as the percentage.", secs=35, stim=sid)

assert F(261000, 180) == 1450 and F(261000, 200) == 1305 and F(261000, 90) == 2900
Q(T, "Table with missing values", I, "What was the fare per passenger in the AC 3-tier class?",
  "₹1,450", ["₹1,305", "₹261", "₹2,900"],
  "Passengers = 90% of 200; fare = revenue ÷ passengers",
  "Passengers = 90% of 200 = 180. Revenue = ₹2,61,000. Fare = 2,61,000 ÷ 180 = ₹1,450.",
  ["Passengers = 180", "Revenue = ₹2,61,000", "Fare = ₹1,450"],
  why="₹1,305 divides the revenue by all 200 seats instead of the 180 passengers; ₹261 forgets that revenue is in "
      "₹ thousand; ₹2,900 divides by the occupancy figure 90.", secs=55, stim=sid)

pas = sum(v[2] for v in COACH.values())
seats = sum(v[0] for v in COACH.values())
assert pas == 732 and seats == 824 and pas - 36 == 696 and pas - 36 + 48 == 744
Q(T, "Table with missing values", I, "How many passengers travelled on this run in all four classes together?",
  "732", ["824", "696", "744"],
  "Fill in the missing passenger counts from seats × occupancy",
  "AC First: 75% of 48 = 36. AC 3-tier: 90% of 200 = 180. With 84 and 432 given, total = 36 + 84 + 180 + 432 = 732.",
  ["AC First 36", "AC 3-tier 180", "36 + 84 + 180 + 432 = 732"],
  why="824 is the number of seats; 696 leaves out AC First; 744 takes AC First as full (48 passengers).", secs=55,
  stim=sid)

occ = F(pas, seats)
assert pct2(occ) == "88.83%" and F(75 + F(175, 2) + 90 + 90, 4) == F(6850, 80) and pct2(F(696, 776)) == "89.69%"
assert pct2(1 - occ) == "11.17%"
Q(T, "Table with missing values", A, "What was the overall occupancy of the train across the four classes (correct to "
  "two decimal places)?",
  "88.83%", ["85.63%", "11.17%", "89.69%"],
  "Overall occupancy = total passengers ÷ total seats; the classes have very different sizes",
  "Passengers = 732 and seats = 48 + 96 + 200 + 480 = 824. Occupancy = 732 ÷ 824 = 88.83%.",
  ["Passengers = 732", "Seats = 824", "732 ÷ 824 = 88.83%"],
  why="85.63% averages the four class occupancies (75, 87.5, 90, 90) without weighting; 11.17% is the share of seats "
      "left empty; 89.69% leaves out the AC First class (696 ÷ 776).", secs=85, stim=sid)

VIL = {"Amla": (2400, 75, 1800, 1000, 800), "Bel": (3200, 80, 2560, 1440, 1120),
       "Chandan": (2000, 68, 1360, 760, 600), "Dhaniya": (2800, 85, 2380, 1340, 1040)}
for k, (pop, rt, lit, ml, fl) in VIL.items():
    assert pop * F(rt, 100) == lit and ml + fl == lit
vshown = [["Amla", ind(2400), "75%", "—", ind(1000), "—"], ["Bel", ind(3200), "—", ind(2560), ind(1440), "—"],
          ["Chandan", "—", "68%", ind(1360), "—", 600], ["Dhaniya", ind(2800), "85%", "—", "—", ind(1040)]]
sid = stimulus("data_table", "Population and literacy in four villages of a block (some values missing)",
               "The table gives the population, the literacy rate (literates as a percentage of the population), "
               "the number of literates and the numbers of male and female literates in four villages. Some values "
               "are missing (—).\n\n" +
               md_table(["Village", "Population", "Literacy rate", "Literates", "Male literates", "Female literates"],
                        vshown),
               {"columns": ["village", "population", "literacy_rate_pct", "literates", "male_literates",
                            "female_literates"],
                "rows": [[r[0]] + [None if c == "—" else (float(str(c).rstrip("%").replace(",", "")))
                                   for c in r[1:]] for r in vshown]})
assert F(1360, F(68, 100)) == 2000 and 1360 * F(68, 100) == F(4624, 5) and 1360 * F(132, 100) == F(8976, 5)
Q(T, "Table with missing values", I, "What is the population of Chandan?",
  "2,000", ["924.8", "1,795.2", "1,360"],
  "Population = literates ÷ literacy rate",
  "1,360 literates are 68% of the population, so the population = 1,360 ÷ 0.68 = 2,000.",
  ["68% of P = 1,360", "P = 1,360 ÷ 0.68 = 2,000"],
  why="924.8 multiplies 1,360 by 0.68 instead of dividing; 1,795.2 adds 32% of the literates, taking the "
      "non-literates as 32% of the literates; 1,360 is the number of literates.", secs=45, stim=sid)

assert pct2(F(800, 1800)) == "44.44%" and pct2(F(800, 2400)) == "33.33%" and F(800, 1000) * 100 == 80
Q(T, "Table with missing values", I, "In Amla, what percentage of the literates are female (correct to two decimal "
  "places)?",
  "44.44%", ["33.33%", "80.00%", "55.56%"],
  "Literates = 75% of 2,400; female literates = literates − male literates",
  "Literates = 75% of 2,400 = 1,800; female literates = 1,800 − 1,000 = 800. Share = 800 ÷ 1,800 = 44.44%.",
  ["Literates = 1,800", "Female = 800", "800 ÷ 1,800 = 44.44%"],
  why="33.33% divides by the whole population (2,400); 80.00% compares female with male literates; 55.56% is the "
      "male share.", secs=55, stim=sid)

ratio = {k: F(v[4], v[3]) for k, v in VIL.items()}
assert unique_max(ratio) == "Amla" and sorted(ratio, key=ratio.get, reverse=True)[1] == "Chandan"
assert max(VIL, key=lambda k: VIL[k][1]) == "Dhaniya" and max(VIL, key=lambda k: VIL[k][2]) == "Bel"
Q(T, "Table with missing values", A, "Which village has the highest ratio of female literates to male literates?",
  "Amla", ["Chandan", "Dhaniya", "Bel"],
  "Fill in the missing male and female figures, then compare female ÷ male",
  "Amla 800/1,000 = 0.800; Bel 1,120/1,440 = 0.778; Chandan 600/760 = 0.789 (male = 1,360 − 600); Dhaniya "
  "1,040/1,340 = 0.776 (literates = 85% of 2,800 = 2,380). Amla is the highest.",
  ["Amla 0.800", "Bel 0.778", "Chandan 0.789", "Dhaniya 0.776"],
  why="Chandan is a close second (0.789); Dhaniya has the highest literacy rate but the lowest female-to-male ratio; "
      "Bel has the most literates.", secs=100, stim=sid)

lit_all = sum(v[2] for v in VIL.values())
pop_all = sum(v[0] for v in VIL.values())
assert lit_all == 8100 and pop_all == 10400 and pct2(F(lit_all, pop_all)) == "77.88%" and F(75 + 80 + 68 + 85, 4) == 77
assert pct2(F(lit_all - 1360, pop_all - 2000)) == "80.24%"
Q(T, "Table with missing values", A, "Taking the four villages together, what percentage of the population is literate "
  "(correct to two decimal places)?",
  "77.88%", ["77.00%", "22.12%", "80.24%"],
  "Overall rate = total literates ÷ total population; the villages differ in size",
  "Literates: 1,800 + 2,560 + 1,360 + 2,380 = 8,100. Population: 2,400 + 3,200 + 2,000 + 2,800 = 10,400. Rate = "
  "8,100 ÷ 10,400 = 77.88%.",
  ["Literates = 8,100", "Population = 10,400", "8,100 ÷ 10,400 = 77.88%"],
  why="77.00% averages the four literacy rates without weighting; 22.12% is the non-literate share; 80.24% leaves out "
      "Chandan, whose population is missing from the table.", secs=95, stim=sid)

# ================================================================ Quantity Comparison (B2 I1 A2)
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


m7 = [k for k in range(101, 200) if k % 7 == 0]
sq = [k * k for k in range(1, 30) if 100 < k * k < 500]
assert len(m7) == 14 and len(sq) == 12 and m7[0] == 105 and m7[-1] == 196 and sq[0] == 121 and sq[-1] == 484
qc("Quantity I vs II", B, "The number of multiples of 7 between 100 and 200",
   "The number of perfect squares between 100 and 500", [F(14)], [F(12)], ">", ["<", "<="],
   "Count from the first to the last multiple (or root) in the range",
   "Quantity I: multiples of 7 from 105 = 7 × 15 to 196 = 7 × 28, i.e. 28 − 15 + 1 = 14. Quantity II: squares from "
   "121 = 11² to 484 = 22², i.e. 22 − 11 + 1 = 12. Quantity I > Quantity II.",
   ["I: 7 × 15 to 7 × 28 ⇒ 14", "II: 11² to 22² ⇒ 12", "14 > 12"],
   why="'I < II' and 'I ≤ II' come from miscounting the ranges, e.g. stopping the multiples of 7 at 189 (13 of "
       "them) while counting 10² = 100 and 23² = 529, which lie outside the range, as squares (14).", secs=50,
   by=BRUTE)

q1v, q2v = 5000 * F(8, 100) * 3, 4000 * F(32, 100)
assert q1v == 1200 and q2v == 1280
qc("Arithmetic-based comparison", B, "Simple interest (₹) on ₹5,000 at 8% per annum for 3 years",
   "Profit (₹) on an article that costs ₹4,000 and is sold at a 32% profit", [q1v], [q2v], "<", [">", ">="],
   "SI = P × R × T/100; profit = cost × profit%",
   "Quantity I: 5,000 × 8% × 3 = ₹1,200. Quantity II: 32% of 4,000 = ₹1,280. Quantity I < Quantity II.",
   ["I: 400 × 3 = 1,200", "II: 0.32 × 4,000 = 1,280", "1,200 < 1,280"],
   why="'I > II' and 'I ≥ II' come from compounding the interest (5,000 × 1.08³ − 5,000 ≈ ₹1,299) or from taking "
       "the profit on the selling price.", secs=45)

cs = [c for c in range(1, 30) if 10 < c < 17]
assert cs == [11, 12, 13, 14, 15, 16]
qc("Arithmetic-based comparison", I, "The length (cm) of the third side of a triangle whose other two sides are 7 cm "
   "and 10 cm, if the third side is a whole number of centimetres and is strictly the longest side",
   "12.5", [F(c) for c in cs], [F(25, 2)], "cbe", [">", "<="],
   "Triangle inequality: the third side must be less than 7 + 10 = 17; being the longest, it must exceed 10",
   "The third side c satisfies 10 < c < 17, so c can be 11, 12, 13, 14, 15 or 16. Some of these are less than 12.5 "
   "and some greater, so no single relation holds.",
   ["c < 7 + 10 = 17", "c > 10 (longest)", "c ∈ {11, …, 16}", "11 < 12.5 < 16 ⇒ cannot be established"],
   why="'I > II' and 'I ≥ II' consider only the larger possible sides (13 to 16); 'I ≤ II' and 'I < II' consider only "
       "11 and 12.", secs=60, by=BRUTE)

tz = sum(100 // 5 ** k for k in range(1, 4))
npr = sum(1 for p in range(2, 100) if all(p % d for d in range(2, p)))
assert tz == 24 and npr == 25
qc("Quantity I vs II", A, "The number of zeros at the end of 100! (the product 1 × 2 × … × 100)",
   "The number of prime numbers less than 100", [F(tz)], [F(npr)], "<", [">", ">="],
   "Trailing zeros of n! = ⌊n/5⌋ + ⌊n/25⌋ + …",
   "Quantity I: ⌊100/5⌋ + ⌊100/25⌋ = 20 + 4 = 24. Quantity II: there are 25 primes below 100 (2, 3, 5, …, 97). "
   "Quantity I < Quantity II.",
   ["I: 20 + 4 = 24", "II: 25 primes", "24 < 25"],
   why="'I > II' and 'I ≥ II' come from counting extra zeros (adding ⌊100/10⌋ = 10 as well, which double-counts "
       "the multiples of 10) or from leaving 2 out of the primes (24, which would make I ≥ II).", secs=75, by=BRUTE)

arr = [p for p in itertools.permutations("LOANS") if p[0] in "OA"]
assert len(arr) == 48 and math.comb(10, 2) == 45
qc("Arithmetic-based comparison", A, "The number of arrangements of the letters of the word LOANS that begin with a "
   "vowel", "The number of ways of choosing 2 members from a group of 10", [F(48)], [F(45)], ">", ["<", "<="],
   "Fix the first letter, arrange the rest; C(n, 2) = n(n − 1)/2",
   "Quantity I: the first letter is O or A (2 ways), and the other 4 letters can be arranged in 4! = 24 ways: 48. "
   "Quantity II: C(10, 2) = 45. Quantity I > Quantity II.",
   ["I: 2 × 4! = 48", "II: 10 × 9 ÷ 2 = 45", "48 > 45"],
   why="'I < II' and 'I ≤ II' come from fixing only one vowel at the start (4! = 24) or from counting ordered pairs "
       "for Quantity II (10 × 9 = 90).", secs=70, by=BRUTE)

# ================================================================ Data Sufficiency (Quant) (B1 I2 A2)
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


cands = [(F(p, 2), F(n, 2)) for p in range(1, 121) for n in range(1, 121)]
verdict = ds2_verdict(cands, lambda c: 3 * c[0] + 2 * c[1] == 110, lambda c: 2 * c[0] + 3 * c[1] == 115,
                      lambda c: c[0])
assert verdict == "both"
Q(T, "Two-statement", B,
  f"{DS_PRE}\nQuestion: What is the price of one pen?\n"
  "I. 3 pens and 2 notebooks together cost ₹110.\n"
  "II. 2 pens and 3 notebooks together cost ₹115.",
  DS2["both"], [DS2["I"], DS2["either"], DS2["neither"]],
  "Two unknowns need two independent equations",
  "I alone has two unknowns (pen and notebook), so many prices fit; so does II alone. Together: 3p + 2n = 110 and "
  "2p + 3n = 115 give p = ₹20 and n = ₹25.",
  ["I alone: one equation, two unknowns", "II alone: likewise", "I + II: p = 20, n = 25", "Both are needed"],
  why="'I alone' and 'either' treat a single equation in two unknowns as enough; 'neither' overlooks that the two "
      "equations together fix both prices.", secs=50, by=BRUTE)

isp = lambda n: n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))  # noqa: E731
cands = list(range(1, 200))
verdict = ds2_verdict(cands, lambda n: 20 < n < 30 and isp(n), lambda n: isp(n) and isp(n + 2), lambda n: n)
assert verdict == "both" and [n for n in range(21, 30) if isp(n)] == [23, 29]
Q(T, "Two-statement", I,
  f"{DS_PRE}\nQuestion: What is the value of the positive integer n?\n"
  "I. n is a prime number between 20 and 30.\n"
  "II. n + 2 is also a prime number.",
  DS2["both"], [DS2["I"], DS2["II"], DS2["neither"]],
  "List the candidates allowed by each statement and see whether one value remains",
  "I alone: n = 23 or 29. II alone: n could be 3, 5, 11, 17, 29, … Together: 23 + 2 = 25 is not prime but "
  "29 + 2 = 31 is, so n = 29.",
  ["I: n = 23 or 29", "II: many twin-prime starters", "I + II: n = 29", "Both are needed"],
  why="'I alone' forgets that 23 is also a prime between 20 and 30; 'II alone' ignores the infinitely many twin "
      "primes; 'neither' misses that only 29 survives both statements.", secs=60, by=BRUTE)

cands = [(F(v, 2), F(s, 2)) for v in range(1, 61) for s in range(0, 41) if s < v]
conds = [lambda c: c[0] + c[1] == 12, lambda c: c[1] == c[0] / 5, lambda c: c[0] - c[1] == 8]
mp_ = suff_map(cands, conds, lambda c: c[0])
assert mp_ == {(0,): False, (1,): False, (2,): False, (0, 1): True, (0, 2): True, (1, 2): True, (0, 1, 2): True}
Q(T, "Three-statement", I,
  f"{DS3_PRE}\nQuestion: What is the speed of the boat in still water?\n"
  "I. The boat covers 24 km downstream in 2 hours.\n"
  "II. The speed of the stream is one-fifth of the speed of the boat in still water.\n"
  "III. The boat covers 24 km upstream in 3 hours.",
  "Any two of the three statements together are sufficient",
  ["Only I and III together are sufficient", "All three statements together are necessary",
   "Only I and II together are sufficient"],
  "Each statement gives one equation in the boat speed b and stream speed s; any two independent ones fix b",
  "I: b + s = 12. II: s = b/5. III: b − s = 8. I + II: 6b/5 = 12, b = 10. I + III: b = 10. II + III: 4b/5 = 8, "
  "b = 10. Any two statements give b = 10 km/h; no single one does.",
  ["I + II: b = 10", "I + III: b = 10", "II + III: b = 10", "Answer: any two"],
  why="'Only I and III' overlooks that II can replace either of them; 'all three' is more than needed; 'only I and "
      "II' overlooks the other two pairs.", secs=75, by=BRUTE)

cands = [(F(l_), F(b_), F(h_, 2)) for l_ in range(1, 13) for b_ in range(1, 13) for h_ in range(1, 25)]
conds = [lambda c: (c[0], c[1]) == (6, 4), lambda c: c[0] * c[1] * c[2] == 72, lambda c: c[0] * c[1] == 24]
mp_ = suff_map(cands, conds, lambda c: 2 * c[2] * (c[0] + c[1]) * 20)
assert mp_ == {(0,): False, (1,): False, (2,): False, (0, 1): True, (0, 2): False, (1, 2): False, (0, 1, 2): True}
Q(T, "Three-statement", A,
  f"{DS3_PRE}\nQuestion: What will it cost to paint the four walls of a rectangular room at ₹20 per m² (ignore doors "
  "and windows)?\n"
  "I. The room is 6 m long and 4 m wide.\n"
  "II. The volume of the room is 72 m³.\n"
  "III. The floor area of the room is 24 m².",
  "Only I and II together are sufficient",
  ["Only I and III together are sufficient", "Any two of the three statements together are sufficient",
   "All three statements together are necessary"],
  "Area of four walls = 2h(l + b); all of l, b and h are needed",
  "I gives l and b but not h. I + II: h = 72 ÷ 24 = 3 m, walls = 2 × 3 × 10 = 60 m², cost ₹1,200. I + III: III "
  "repeats l × b = 24, so h is still unknown. II + III: h = 3 m, but l + b is unknown (6 × 4, 8 × 3, 12 × 2 all "
  "give 24 m²), so the wall area is not fixed.",
  ["I + II: h = 3 ⇒ cost ₹1,200", "I + III: no height", "II + III: perimeter unknown", "Answer: only I and II"],
  why="'Only I and III' has no height; 'any two' wrongly accepts II + III, where the floor's perimeter is not fixed; "
      "'all three' is more than needed, since III adds nothing to I + II.", secs=90, by=BRUTE)

cands = [F(q) for q in range(10, 400, 10)]
verdict = ds2_verdict(cands, lambda q: True, lambda q: True, lambda q: F(120 + q, 2 + q / 40))
assert verdict == "neither"
Q(T, "Two-statement", A,
  f"{DS_PRE}\nQuestion: What is the average speed of a car for its whole journey from P to R through Q?\n"
  "I. The car covers the 120 km from P to Q at 60 km/h.\n"
  "II. The car covers the stretch from Q to R at 40 km/h.",
  DS2["neither"], [DS2["both"], DS2["I"], DS2["II"]],
  "Average speed = total distance ÷ total time; the distance QR is needed",
  "I gives 2 hours for PQ. II gives the speed on QR but not its length. With QR = 40 km the average is "
  "160 ÷ 3 = 53⅓ km/h; with QR = 120 km it is 240 ÷ 5 = 48 km/h. So even both statements together do not fix it.",
  ["I: PQ takes 2 h", "II: QR speed only", "Different QR lengths give different averages", "Not sufficient"],
  why="'Both together' assumes QR is also 120 km (giving 48 km/h); 'I alone' and 'II alone' ignore the other "
      "stretch altogether.", secs=70, by=BRUTE)

# ================================================================ checks and output
assert len(QUESTIONS) == TOTAL, len(QUESTIONS)
assert len(STIMULI) == 10

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_008_plan.json").read_text(encoding="utf-8"))
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
    "batch_id": "BATCH_008",
    "created_at": TODAY,
    "notes": "BATCH_008, Quantitative Aptitude part: 199 original questions (60 Basic, 79 Intermediate, 60 Advanced) "
             "with 10 shared DI stimuli on new data sets. Every answer was recomputed by tools/batch_008/quant.py "
             "before writing; every number series was also tested against a library of common alternative rules "
             "(no other rule that fits the given terms produces another option); quantity-comparison values are at "
             "least 2% apart. Questions tagged ai:independent-check were also re-solved from the stem, options and "
             "data set alone by a separate solver. Pending human review.",
    "stimuli": STIMULI,
    "questions": QUESTIONS,
}
out = ROOT / "batches" / "parts" / "BATCH_008_QUANT.json"
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
      f"independent-check {len(INDEPENDENT)}, series checked {len(SERIES_LOG)})")
