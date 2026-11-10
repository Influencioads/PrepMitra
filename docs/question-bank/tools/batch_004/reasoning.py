"""Builds batches/parts/BATCH_004_REAS.json: the 200 Reasoning Ability questions of BATCH_004.

Same method and helpers as tools/batch_003/reasoning.py, with new puzzle structures, noun sets and scenarios:
- puzzles and seating: the conditions are written once as (text, variables, test) triples; the text goes into the
  stimulus (or the question) and the test into an exhaustive backtracking search that must return exactly one
  arrangement. Every answer is then read off that arrangement;
- syllogisms: checked over every Venn-region model; inequalities: exhaustive integer assignments (with a growing
  value range as a cross-check);
- blood relations (explicit family tree), directions, coding (inferred rules are checked against a library of
  alternative simple rules), series, alphabet, ranking and input-output: recomputed in code; data sufficiency: each
  statement subset checked by enumerating models.
Verbal-reasoning items (assumptions, conclusions, critical reasoning) are hand-written and were re-answered blind by a
separate solver.
If any assertion fails, nothing is written. --draft prints quota gaps instead of asserting them.

    python tools/batch_004/reasoning.py        (run from docs/question-bank)
"""

import datetime as dt
import itertools
import json
import string
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import default_mappings  # noqa: E402

ROOT = TOOLS.parent
OUT = ROOT / "batches" / "parts" / "BATCH_004_REAS.json"
TODAY = "2026-11-05"
RA = "Reasoning Ability"
LETTERS = "ABCD"
FIRST_Q, FIRST_STIM = 605, 4001
BRUTE = ("script:brute-force-unique", "ai:author-solve")
RECOMP = ("script:recompute", "ai:author-solve")
VENN = ("script:all-venn-models", "ai:author-solve")
EXHAUST = ("script:exhaustive-integers", "ai:author-solve")
ENUM = ("script:enumerate-models", "ai:author-solve")
HAND = ("ai:author-solve", "ai:independent-check")
OPT4 = ["Only conclusion I follows", "Only conclusion II follows", "Neither conclusion I nor II follows",
        "Both conclusions I and II follow"]
EITHER = "Either conclusion I or II follows"
ONLY_I, ONLY_II, NEITHER, BOTH = OPT4

QUESTIONS, STIMULI = [], []
KEYCOUNT = Counter()


# ------------------------------------------------------------------------------------------------ generic helpers
def solve(variables, domains, constraints, distinct_groups=()):
    """Exhaustive backtracking search; returns every assignment that satisfies all constraints.
    Each constraint (vars, fn) is tested as soon as its last variable is assigned, so pruning never skips a model."""
    order = list(variables)
    idx = {v: i for i, v in enumerate(order)}
    checks = [[] for _ in order]
    for vs, fn in constraints:
        checks[max(idx[v] for v in vs)].append((vs, fn))
    groups = {}
    for g in distinct_groups:
        for v in g:
            groups.setdefault(v, []).append(g)
    sols, cur = [], {}

    def rec(i):
        if i == len(order):
            sols.append(dict(cur))
            return
        v = order[i]
        for val in domains[v]:
            if any(cur.get(o) == val for g in groups.get(v, []) for o in g if o != v and o in cur):
                continue
            cur[v] = val
            if all(fn(*(cur[x] for x in vs)) for vs, fn in checks[i]):
                rec(i + 1)
            del cur[v]

    rec(0)
    return sols


def unique(variables, domains, conds, distinct_groups=()):
    sols = solve(variables, domains, [(vs, fn) for _, vs, fn in conds], distinct_groups)
    assert len(sols) == 1, f"{len(sols)} solutions: {sols[:3]}"
    return sols[0]


def place(correct, wrongs, natural=None):
    """Returns (options, key). natural=None: put the correct option on the least-used key so far (keeps A-D balanced);
    natural=callable: sort all four options by it (numbers stay in order) and let the key fall where it falls."""
    wrongs = list(wrongs)
    assert len(wrongs) == 3 and correct not in wrongs and len(set(wrongs)) == 3, (correct, wrongs)
    if natural:
        opts = sorted([correct] + wrongs, key=natural)
    else:
        n = len(QUESTIONS)
        k = min(LETTERS, key=lambda L: (KEYCOUNT[L], (LETTERS.index(L) - n) % 4))
        opts = wrongs[:]
        opts.insert(LETTERS.index(k), correct)
    return opts, LETTERS[opts.index(correct)]


WORDS = ["None", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"]


def num_word(n):
    return WORDS[n]


by_num = lambda t: WORDS.index(t) if t in WORDS else float(t.split()[0]) if t.split()[0].replace(".", "").isdigit() else 99


def q(topic, subtopic, difficulty, text, options, answer, concept, explanation, steps, shortcut=None,
      why_others_wrong=None, seconds=60, stimulus=None, verified_by=HAND, tags=None):
    assert answer in LETTERS and len(options) == 4 and len(set(options)) == 4, (text, options)
    out = {
        "question_id": f"BANK_REAS_{FIRST_Q + len(QUESTIONS):06d}",
        "exam_mappings": default_mappings(RA, difficulty),
        "subject": RA, "topic": topic, "subtopic": subtopic, "difficulty": difficulty,
        "question_type": "MCQ", "language": "en",
    }
    if stimulus:
        pos = sum(1 for x in QUESTIONS if x.get("stimulus_id") == stimulus) + 1
        out |= {"stimulus_id": stimulus, "set_position": pos}
    out |= {
        "question_text": text,
        "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(options)],
        "correct_answer": answer,
        "solution": {"concept": concept, "explanation": explanation, "steps": list(steps), "shortcut": shortcut,
                     "why_others_wrong": why_others_wrong,
                     "final_answer": f"Option {answer}: {options[LETTERS.index(answer)]}"},
        "suggested_time_seconds": seconds,
        "source": {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                   "original_exam_year": None, "license_note": None},
        "verification": {"answer_verified": True, "solution_verified": True,
                         "review_status": "Pending Human Review", "verified_by": list(verified_by),
                         "verified_at": TODAY},
    }
    if tags:
        out["tags"] = tags
    QUESTIONS.append(out)
    KEYCOUNT[answer] += 1
    return out


def mcq(topic, subtopic, difficulty, text, correct, wrongs, concept, explanation, steps, natural=None, **kw):
    opts, key = place(correct, wrongs, natural)
    return q(topic, subtopic, difficulty, text, opts, key, concept, explanation, steps, **kw)


def fixed(topic, subtopic, difficulty, text, options, correct_text, concept, explanation, steps, **kw):
    """For fixed option sets (Only I / Only II / Neither / Both, data sufficiency, cause-effect)."""
    assert correct_text in options
    return q(topic, subtopic, difficulty, text, options, LETTERS[options.index(correct_text)], concept, explanation,
             steps, **kw)


def conclusion_options(answer):
    """Four-option rule as applied in batch 1: Only I, Only II, Neither, Both; when the answer is 'Either I or II' it
    replaces 'Both' (impossible for two complementary conclusions) and 'Neither' stays."""
    if answer == EITHER:
        return [ONLY_I, ONLY_II, NEITHER, EITHER]
    return OPT4


def stimulus(kind, title, intro, conds, solution):
    sid = f"STIM_REAS_{FIRST_STIM + len(STIMULI):06d}"
    body = intro + "\n\n" + "\n".join(f"- {t}" for t, _, _ in conds) if conds else intro
    STIMULI.append({"stimulus_id": sid, "type": kind, "title": title, "content": body, "solution": solution})
    return sid


def one_true(statements):
    """statements: list of (text, bool). Exactly one must be true; returns (true_text, [false_texts])."""
    good = [t for t, ok in statements if ok]
    assert len(good) == 1 and len(statements) == 4, statements
    return good[0], [t for t, ok in statements if not ok]


def one_false(statements):
    bad = [t for t, ok in statements if not ok]
    assert len(bad) == 1 and len(statements) == 4, statements
    return bad[0], [t for t, ok in statements if ok]


def table(header, rows):
    return "| " + " | ".join(header) + " |\n|" + "---|" * len(header) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in r) + " |" for r in rows)


def puzzle_q(sid, topic, sub, diff, text, correct, wrongs, concept, explanation, steps, natural=None, seconds=60,
             **kw):
    return mcq(topic, sub, diff, text, correct, wrongs, concept, explanation, steps, natural=natural,
               seconds=seconds, stimulus=sid, verified_by=BRUTE, **kw)


def bullets(conds):
    return "\n".join(f"- {t}" for t, _, _ in conds)


ORDN = lambda k: f"{k}{'th' if 10 <= k % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(k % 10, 'th')}"
MON = "Month and Date-Based Puzzles"
MNAME = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
         "November", "December"]
MDAYS = {m: (dt.date(2026 + (m == 12), m % 12 + 1, 1) - dt.date(2026, m, 1)).days for m in range(1, 13)}
assert MDAYS[2] == 28 and MDAYS[4] == 30 and MDAYS[12] == 31
# ------------------------------------------------------------------------------------------------ shared helpers (syllogism, inequality, family tree, directions) reused from tools/batch_001/reasoning.py
SYL = "Syllogism"
INQ = "Inequality"
BLD = "Blood Relations"
DIR = "Direction Sense"
REL = {">": lambda a, b: a > b, "<": lambda a, b: a < b, "≥": lambda a, b: a >= b, "≤": lambda a, b: a <= b,
       "=": lambda a, b: a == b}


def article(w):
    return ("an " if w[0] in "aeiou" else "a ") + w


def syl_text(form, a, b, nouns):
    sa, pa = nouns[a]
    sb, pb = nouns[b]
    return {
        "all": f"All {pa} are {pb}.", "no": f"No {sa} is {article(sb)}.", "some": f"Some {pa} are {pb}.",
        "somenot": f"Some {pa} are not {pb}.", "onlyfew": f"Only a few {pa} are {pb}.",
        "only": f"Only {pa} are {pb}.",
        "poss_all": f"All {pa} being {pb} is a possibility.", "poss_some": f"Some {pa} being {pb} is a possibility.",
        "poss_no": f"No {sa} being {article(sb)} is a possibility.",
        "never_all": f"All {pa} can never be {pb}.",
    }[form]


def syllogism(nouns, statements, conclusions):
    """Checks two conclusions over every Venn-region model of up to four sets (2^(2^k) region subsets).
    Returns (follows_I, follows_II, either)."""
    terms = list(nouns)
    k = len(terms)
    assert k <= 4
    regions = list(itertools.product((0, 1), repeat=k))[1:]  # drop the region outside every set
    ix = {t: i for i, t in enumerate(terms)}
    mask = lambda pred: sum(1 << j for j, r in enumerate(regions) if pred(r))
    pairs = [(a, b) for a in terms for b in terms if a != b]
    ABm = {(a, b): mask(lambda r, a=a, b=b: r[ix[a]] and r[ix[b]]) for a, b in pairs}
    AnBm = {(a, b): mask(lambda r, a=a, b=b: r[ix[a]] and not r[ix[b]]) for a, b in pairs}
    AB = lambda a, b: ABm[(a, b)]
    AnB = lambda a, b: AnBm[(a, b)]
    holds = {
        "all": lambda m, a, b: m & AnB(a, b) == 0, "no": lambda m, a, b: m & AB(a, b) == 0,
        "some": lambda m, a, b: m & AB(a, b) != 0, "somenot": lambda m, a, b: m & AnB(a, b) != 0,
        "onlyfew": lambda m, a, b: m & AB(a, b) != 0 and m & AnB(a, b) != 0,
        "only": lambda m, a, b: m & AnB(b, a) == 0,
    }
    nonempty = [mask(lambda r, t=t: r[ix[t]]) for t in terms]
    models = [m for m in range(1 << len(regions))
              if all(m & ne for ne in nonempty) and all(holds[f](m, a, b) for f, a, b in statements)]
    assert models

    def follows(c):
        f, a, b = c
        if f.startswith("poss_"):
            base = {"poss_all": "all", "poss_some": "some", "poss_no": "no"}[f]
            return any(holds[base](m, a, b) for m in models)
        if f == "never_all":
            return all(not holds["all"](m, a, b) for m in models)
        return all(holds[f](m, a, b) for m in models)

    def true_in(c, m):
        f, a, b = c
        return holds[f](m, a, b)

    f1, f2 = follows(conclusions[0]), follows(conclusions[1])
    same_pair = {conclusions[0][1], conclusions[0][2]} == {conclusions[1][1], conclusions[1][2]}
    either = (same_pair and not f1 and not f2 and all(not x[0].startswith("poss_") for x in conclusions)
              and all(true_in(conclusions[0], m) or true_in(conclusions[1], m) for m in models))
    return f1, f2, either


def syl_q(diff, sub, nouns, statements, conclusions, expected, concept, explanation, steps, shortcut=None,
          why=None, seconds=45):
    f1, f2, either = syllogism(nouns, statements, conclusions)
    got = EITHER if either else BOTH if f1 and f2 else ONLY_I if f1 else ONLY_II if f2 else NEITHER
    assert got == expected, (statements, conclusions, got, expected)
    text = ("Statements:\n" + "\n".join(syl_text(f, a, b, nouns) for f, a, b in statements) +
            "\n\nConclusions:\nI. " + syl_text(*conclusions[0], nouns) + "\nII. " + syl_text(*conclusions[1], nouns))
    opts = conclusion_options(expected)
    return fixed(SYL, sub, diff, "In the question below, some statements are followed by two conclusions. Take the "
                 "statements to be true even if they seem to be at variance with commonly known facts, and decide "
                 "which of the conclusions logically follow.\n\n" + text, opts, expected, concept, explanation,
                 steps, shortcut=shortcut, why_others_wrong=why, seconds=seconds, verified_by=VENN)


def N(*pairs):
    return {s: (s, p) for s, p in pairs}

REL = {">": lambda a, b: a > b, "<": lambda a, b: a < b, "≥": lambda a, b: a >= b, "≤": lambda a, b: a <= b,
       "=": lambda a, b: a == b}


def parse_chain(s):
    """'P ≥ Q > R' -> [('P','≥','Q'), ('Q','>','R')]."""
    tok = s.split()
    return [(tok[i], tok[i + 1], tok[i + 2]) for i in range(0, len(tok) - 2, 2)]


def ineq_eval(chains, conclusions, dom=None):
    rels = [r for c in chains for r in parse_chain(c)]
    vs = sorted({x for a, _, b in rels for x in (a, b)} | {x for c in conclusions for x in (c[0], c[2])})
    res = []
    sats = []
    dom = dom or len(vs)  # values 0..k-1 realise every weak order of k variables
    for vals in itertools.product(range(dom), repeat=len(vs)):
        v = dict(zip(vs, vals))
        if all(REL[o](v[a], v[b]) for a, o, b in rels):
            sats.append(v)
    assert sats
    for a, o, b in conclusions:
        res.append(all(REL[o](v[a], v[b]) for v in sats))
    same_pair = {conclusions[0][0], conclusions[0][2]} == {conclusions[1][0], conclusions[1][2]}
    either = (same_pair and not res[0] and not res[1] and
              all(REL[conclusions[0][1]](v[conclusions[0][0]], v[conclusions[0][2]]) or
                  REL[conclusions[1][1]](v[conclusions[1][0]], v[conclusions[1][2]]) for v in sats))
    return res[0], res[1], either


def ineq_q(diff, sub, statement_text, chains, conclusions, concl_text, expected, explanation, steps, shortcut=None,
           why=None, seconds=40, concept="Reading a combined inequality chain"):
    f1, f2, either = ineq_eval(chains, conclusions)
    got = EITHER if either else BOTH if f1 and f2 else ONLY_I if f1 else ONLY_II if f2 else NEITHER
    assert got == expected, (chains, conclusions, got)
    text = (statement_text + "\n\nConclusions:\nI. " + concl_text[0] + "\nII. " + concl_text[1])
    return fixed(INQ, sub, diff, text, conclusion_options(expected), expected, concept, explanation, steps,
                 shortcut=shortcut, why_others_wrong=why, seconds=seconds, verified_by=EXHAUST)


def direct(chains, conc):
    return ("Statement: " + "; ".join(chains),
            chains, [parse_chain(c)[0] for c in conc], conc)


decode = lambda s, code: " ".join(code.get(t, t) for t in s.split())


def coded(intro, code, stmts, concs):
    text = intro + "\n\nStatements: " + ", ".join(stmts)
    return text, [decode(x, code) for x in stmts], [parse_chain(decode(c, code))[0] for c in concs], concs

class Family:
    """Explicit family tree: gender, (father, mother) and spouse for every member; rel() names x's relation to y."""

    def __init__(self):
        self.g, self.par, self.sp = {}, {}, {}

    def add(self, name, gender, father=None, mother=None):
        self.g[name], self.par[name] = gender, (father, mother)
        return self

    def marry(self, a, b):
        self.sp[a], self.sp[b] = b, a
        return self

    def parents(self, p):
        return {x for x in self.par.get(p, ()) if x}

    def siblings(self, p):
        return {o for o in self.g if o != p and self.parents(o) and self.parents(o) == self.parents(p)}

    def children(self, p):
        return {o for o in self.g if p in self.parents(o)}

    def rel(self, x, y):
        m = self.g[x] == "M"
        w = lambda a, b: a if m else b
        if self.sp.get(y) == x:
            return w("husband", "wife")
        if x in self.parents(y):
            return w("father", "mother")
        if y in self.parents(x):
            return w("son", "daughter")
        if x in self.siblings(y):
            return w("brother", "sister")
        if any(x in self.parents(p) for p in self.parents(y)):
            return w("grandfather", "grandmother")
        if any(y in self.parents(p) for p in self.parents(x)):
            return w("grandson", "granddaughter")
        if any(x in self.siblings(p) or self.sp.get(x) in self.siblings(p) for p in self.parents(y)):
            return w("uncle", "aunt")
        if any(y in self.siblings(p) or self.sp.get(y) in self.siblings(p) for p in self.parents(x)):
            return w("nephew", "niece")
        if any(a in self.siblings(b) for a in self.parents(x) for b in self.parents(y)):
            return "cousin"
        if self.sp.get(y) and x in self.parents(self.sp[y]):
            return w("father-in-law", "mother-in-law")
        if self.sp.get(x) and y in self.parents(self.sp[x]):
            return w("son-in-law", "daughter-in-law")
        if (self.sp.get(y) and x in self.siblings(self.sp[y])) or (self.sp.get(x) in self.siblings(y)):
            return w("brother-in-law", "sister-in-law")
        return None

    def check(self, facts):
        for x, r, y in facts:
            assert self.rel(x, y) == r, (x, r, y, self.rel(x, y))


def coded_facts(expr, code):
    tok = expr.split()
    return [(tok[i], code[tok[i + 1]], tok[i + 2]) for i in range(0, len(tok) - 2, 2)]


cap = lambda s: s[0].upper() + s[1:]

VEC = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}
CW = ["N", "E", "S", "W"]
NAME = {"N": "North", "E": "East", "S": "South", "W": "West"}
turn = lambda f, side: CW[(CW.index(f) + (1 if side == "R" else -1)) % 4]


def walk(start_face, moves):
    """moves: list of (turn 'L'/'R'/None, distance). Returns final (x, y)."""
    x = y = 0
    f = start_face
    for t, d in moves:
        if t:
            f = turn(f, t)
        x, y = x + VEC[f][0] * d, y + VEC[f][1] * d
    return x, y


def compass(dx, dy):
    ns = "North" if dy > 0 else "South" if dy < 0 else ""
    ew = "East" if dx > 0 else "West" if dx < 0 else ""
    return f"{ns}-{ew}" if ns and ew else ns or ew


def dist(dx, dy):
    d2 = dx * dx + dy * dy
    r = round(d2 ** 0.5)
    if r * r == d2:
        return f"{r}"
    for k in range(int(d2 ** 0.5), 1, -1):
        if d2 % (k * k) == 0:
            return f"{k}√{d2 // (k * k)}"
    return f"√{d2}"


cap = lambda s: s[0].upper() + s[1:]

# ------------------------------------------------------------------------------------------------ more shared helpers reused from batch 1 (coding, series, alphabet, data sufficiency)
COD = "Coding and Decoding"
AL = string.ascii_uppercase
pos = lambda c: AL.index(c) + 1
shift = lambda w, k: "".join(AL[(pos(c) - 1 + k) % 26] for c in w)


def sentence_solve(sentences, ask):
    """sentences: list of (words, codes). Enumerates every word→code bijection consistent with all sentences and
    returns the set of codes 'ask' can take (a word) or the set of words a code can stand for."""
    words = sorted({w for ws, _ in sentences for w in ws})
    codes = sorted({c for _, cs in sentences for c in cs})
    assert len(words) == len(codes)
    out = set()
    for perm in itertools.permutations(codes):
        m = dict(zip(words, perm))
        if all({m[w] for w in ws} == set(cs) for ws, cs in sentences):
            out.add(m[ask] if ask in m else next(w for w in words if m[w] == ask))
    return out

is_l = lambda t: t.isalpha() and len(t) == 1 and t in AL
is_d = lambda t: t.isdigit()
is_s = lambda t: not is_l(t) and not is_d(t)


def count_opts(c):
    lo = max(0, c - 1) if c < 3 else c - 2
    opts = [num_word(lo + i) for i in range(4)]
    assert num_word(c) in opts
    return num_word(c), [o for o in opts if o != num_word(c)]


def series_intro(sr):
    return "Study the following arrangement of letters, numbers and symbols and answer the question.\n\n" + sr


def windows(seq):
    return [(seq[i - 1], seq[i], seq[i + 1]) for i in range(1, len(seq) - 1)]


def letter_pairs(word):
    return [(word[i], word[j]) for i in range(len(word)) for j in range(i + 1, len(word))
            if abs(pos(word[j]) - pos(word[i])) == j - i]


DSF = "Data Sufficiency"
DS2 = {"A": "Statement I alone is sufficient, but statement II alone is not sufficient",
       "B": "Statement II alone is sufficient, but statement I alone is not sufficient",
       "E": "Either statement I alone or statement II alone is sufficient",
       "N": "Statements I and II together are not sufficient",
       "T": "Both statements I and II together are necessary"}
DS_HEAD = ("The question below is followed by two statements, I and II. Decide whether the data in the statements are "
           "sufficient to answer the question.\n\n")


def sufficient(models, stmt_fns, subset, answer):
    vals = {answer(m) for m in models if all(stmt_fns[i](m) for i in subset)}
    assert vals, subset
    return len(vals) == 1


def ds2(models, s1, s2, answer):
    a, b = sufficient(models, [s1, s2], [0], answer), sufficient(models, [s1, s2], [1], answer)
    t = sufficient(models, [s1, s2], [0, 1], answer)
    return "E" if a and b else "A" if a else "B" if b else "T" if t else "N"

DS3 = {"I+II": "Only statements I and II together are sufficient",
       "II+III": "Only statements II and III together are sufficient",
       "I+III": "Only statements I and III together are sufficient",
       "ALL": "All three statements I, II and III together are necessary",
       "NONE": "Even all three statements together are not sufficient",
       "ANY2": "Any two of the three statements together are sufficient"}


def ds3(models, fns, answer):
    suf = {s: sufficient(models, fns, list(s), answer) for r in (1, 2, 3) for s in itertools.combinations(range(3), r)}
    singles = any(suf[(i,)] for i in range(3))
    pairs = [p for p in itertools.combinations(range(3), 2) if suf[p]]
    assert not singles
    if len(pairs) == 3:
        return "ANY2"
    if len(pairs) == 1:
        return {(0, 1): "I+II", (1, 2): "II+III", (0, 2): "I+III"}[pairs[0]]
    assert not pairs
    return "ALL" if suf[(0, 1, 2)] else "NONE"

DS3_HEAD = ("The question below is followed by three statements, I, II and III. Decide which of the statements "
            "are sufficient to answer the question.\n\n")
IOT = "Input and Output"
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]


# ================================================================================================ LINEAR SEATING
LIN = "Linear Seating Arrangement"
SGL, DBL, UNK = "Single row, facing north/south", "Double row", "Unknown number of persons"

# ---- L1 Basic set: six persons facing north, each with a favourite fruit (seats 1..6 from the left; right = +1)
P = ["Ishan", "Jhanvi", "Kabir", "Lavanya", "Moksh", "Nysa"]
FR = ["Apple", "Banana", "Cherry", "Guava", "Kiwi", "Mango"]
F_ = ["f" + p for p in P]
VV = P + F_
IXV = {v: i for i, v in enumerate(VV)}
seat_of = lambda v, fr: next(v[IXV[p]] for p in P if v[IXV["f" + p]] == fr)
conds = [
    ("Kabir sits at the extreme right end of the row.", ("Kabir",), lambda k: k == 6),
    ("Nysa sits third to the left of Kabir.", ("Nysa", "Kabir"), lambda n, k: n == k - 3),
    ("The person who likes Guava sits immediately to the right of Nysa.", tuple(VV),
     lambda *v: seat_of(v, "Guava") == v[IXV["Nysa"]] + 1),
    ("Only one person sits between Ishan and the person who likes Guava.", tuple(VV),
     lambda *v: abs(v[IXV["Ishan"]] - seat_of(v, "Guava")) == 2),
    ("Lavanya likes Guava, and Ishan likes Mango.", ("fLavanya", "fIshan"),
     lambda l, i: l == "Guava" and i == "Mango"),
    ("Moksh is not an immediate neighbour of Ishan.", ("Moksh", "Ishan"), lambda m, i: abs(m - i) != 1),
    ("The person who likes Cherry sits immediately to the left of the person who likes Apple.", tuple(VV),
     lambda *v: seat_of(v, "Cherry") == seat_of(v, "Apple") - 1),
    ("Jhanvi does not like Banana.", ("fJhanvi",), lambda f: f != "Banana"),
]
L1 = unique(VV, {p: range(1, 7) for p in P} | {f: FR for f in F_}, conds, [P, F_])
at = {L1[p]: p for p in P}
fav = {p: L1["f" + p] for p in P}
assert [(at[i], fav[at[i]]) for i in range(1, 7)] == [
    ("Jhanvi", "Kiwi"), ("Ishan", "Mango"), ("Nysa", "Banana"), ("Lavanya", "Guava"), ("Moksh", "Cherry"),
    ("Kabir", "Apple")]
ARR = "Left to right: " + ", ".join(f"{at[i]} ({fav[at[i]]})" for i in range(1, 7))
sid = stimulus("puzzle", "Six persons in a row, with favourite fruits",
               "Six persons Ishan, Jhanvi, Kabir, Lavanya, Moksh and Nysa sit in a straight row, all facing north. Each "
               "of them likes a different fruit among Apple, Banana, Cherry, Guava, Kiwi and Mango. (Facing north, a "
               "person's right is towards the east end of the row.)", conds,
               "Step 1: Number the seats 1 to 6 from the left. Kabir = 6, so Nysa (third to his left) = 3.\n"
               "Step 2: The Guava-lover sits at seat 4, and Lavanya likes Guava, so Lavanya = 4.\n"
               "Step 3: Ishan is two seats from seat 4: seat 2 or seat 6; seat 6 is Kabir's, so Ishan = 2.\n"
               "Step 4: Seats 1 and 5 are left for Jhanvi and Moksh. Moksh cannot sit next to Ishan, so Moksh = 5 and "
               "Jhanvi = 1.\n"
               "Step 5: Ishan likes Mango. Cherry is immediately left of Apple; among the free seats 1, 3, 5, 6 the only "
               "adjacent pair is 5–6, so Moksh likes Cherry and Kabir Apple.\n"
               "Step 6: Jhanvi and Nysa share Banana and Kiwi; Jhanvi does not like Banana, so Jhanvi likes Kiwi and "
               "Nysa Banana.\n\n" + table(["Seat (from the left)", "Person", "Fruit"],
                                         [(i, at[i], fav[at[i]]) for i in range(1, 7)]))
ans = next(p for p in P if fav[p] == "Cherry")
assert ans == "Moksh"
puzzle_q(sid, LIN, SGL, "Basic", "Who likes Cherry?", ans, ["Kabir", "Nysa", "Jhanvi"],
         "Using an adjacency clue to place attributes",
         "Cherry is immediately to the left of Apple. After the seats are fixed, the only two neighbours whose fruits "
         "are still open are Moksh (seat 5) and Kabir (seat 6), so Moksh likes Cherry.",
         [ARR, "Free fruits after Guava and Mango: Apple, Banana, Cherry, Kiwi",
          "Only adjacent pair left: seats 5 and 6 ⇒ Moksh Cherry, Kabir Apple"],
         why_others_wrong="Kabir likes Apple, Nysa Banana and Jhanvi Kiwi.", seconds=45)
ans = at[L1["Ishan"] + 2]
assert ans == "Lavanya"
puzzle_q(sid, LIN, SGL, "Basic", "Who sits second to the right of the person who likes Mango?", ans,
         ["Nysa", "Moksh", "Jhanvi"], "Facing north: the right is towards the east",
         "Ishan likes Mango and sits at seat 2. Two seats to his right is seat 4: Lavanya.",
         [ARR, "Mango: Ishan (seat 2)", "2 + 2 = seat 4 ⇒ Lavanya"],
         why_others_wrong="Nysa is immediately to Ishan's right; Moksh is third to his right; Jhanvi is immediately to "
                          "his left.", seconds=40)
stm = [("Nysa – Banana", fav["Nysa"] == "Banana"), ("Kabir – Kiwi", fav["Kabir"] == "Kiwi"),
       ("Jhanvi – Apple", fav["Jhanvi"] == "Apple"), ("Moksh – Guava", fav["Moksh"] == "Guava")]
t, f = one_true(stm)
puzzle_q(sid, LIN, SGL, "Basic", "Which of the following person – fruit pairs is correct?", t, f,
         "Reading an attribute off the final arrangement",
         "From the final table: Jhanvi Kiwi, Ishan Mango, Nysa Banana, Lavanya Guava, Moksh Cherry, Kabir Apple.",
         [ARR], seconds=40)

# ---- L2 Intermediate set: two rows of four facing each other. Row 1 faces south (its right is west), Row 2 faces
#      north (its right is east). Seat r*10 + c, c = 1..4 from west to east; (1, c) faces (2, c).
P = ["Farid", "Gitali", "Hemant", "Inaya", "Jyotsna", "Kartik", "Lalima", "Mitul"]
SUB = ["Biology", "Chemistry", "Economics", "English", "Geography", "History", "Maths", "Physics"]
SEATS = [r * 10 + c for r in (1, 2) for c in range(1, 5)]
row_, col = lambda s: s // 10, lambda s: s % 10
RT = lambda s, k: s - k if row_(s) == 1 else s + k
opp = lambda s: s + 10 if row_(s) == 1 else s - 10
S_ = ["s" + p for p in P]
VV = P + S_
IXV = {v: i for i, v in enumerate(VV)}
seat_sub = lambda v, sub: next(v[IXV[p]] for p in P if v[IXV["s" + p]] == sub)
conds = [
    ("Gitali sits at an extreme end of Row 1.", ("Gitali",), lambda g: row_(g) == 1 and col(g) in (1, 4)),
    ("Kartik faces Gitali.", ("Kartik", "Gitali"), lambda k, g: k == opp(g)),
    ("Inaya sits second to the right of Kartik.", ("Inaya", "Kartik"), lambda i, k: i == RT(k, 2)),
    ("Mitul sits immediately to the left of Inaya.", ("Mitul", "Inaya"), lambda m, i: m == RT(i, -1)),
    ("Farid faces Mitul.", ("Farid", "Mitul"), lambda f, m: f == opp(m)),
    ("The person who teaches History sits immediately to the left of Farid.", tuple(VV),
     lambda *v: seat_sub(v, "History") == RT(v[IXV["Farid"]], -1)),
    ("Hemant teaches Physics and sits in Row 1.", ("Hemant", "sHemant"),
     lambda h, s: row_(h) == 1 and s == "Physics"),
    ("Jyotsna does not sit at an end of a row.", ("Jyotsna",), lambda j: col(j) in (2, 3)),
    ("The person who teaches Maths faces the person who teaches History.", tuple(VV),
     lambda *v: seat_sub(v, "Maths") == opp(seat_sub(v, "History"))),
    ("Lalima teaches Economics.", ("sLalima",), lambda s: s == "Economics"),
    ("Gitali teaches English, and the person who teaches Geography sits immediately to the left of Gitali.",
     tuple(VV), lambda *v: v[IXV["sGitali"]] == "English" and seat_sub(v, "Geography") == RT(v[IXV["Gitali"]], -1)),
    ("Kartik does not teach Biology.", ("sKartik",), lambda k: k != "Biology"),
]
L2 = unique(VV, {p: SEATS for p in P} | {s: SUB for s in S_}, conds, [P, S_])
at = {L2[p]: p for p in P}
sb = {p: L2["s" + p] for p in P}
assert [(at[s], sb[at[s]]) for s in SEATS] == [
    ("Gitali", "English"), ("Farid", "Geography"), ("Jyotsna", "History"), ("Hemant", "Physics"),
    ("Kartik", "Chemistry"), ("Mitul", "Biology"), ("Inaya", "Maths"), ("Lalima", "Economics")]
ARR = ("Row 1 (facing south), west to east: " + ", ".join(f"{at[10 + c]} ({sb[at[10 + c]]})" for c in range(1, 5))
       + "; Row 2 (facing north), west to east: " + ", ".join(f"{at[20 + c]} ({sb[at[20 + c]]})" for c in range(1, 5)))
sid = stimulus("puzzle", "Eight teachers in two facing rows",
               "Eight teachers Farid, Gitali, Hemant, Inaya, Jyotsna, Kartik, Lalima and Mitul sit in two parallel rows "
               "of four seats each. The persons in Row 1 face south and the persons in Row 2 face north, so each person "
               "in one row faces exactly one person in the other row. Each of them teaches a different subject among "
               "Biology, Chemistry, Economics, English, Geography, History, Maths and Physics.", conds,
               "Number the seats 1 to 4 from west to east in both rows. For Row 1 (facing south) the right is west; for "
               "Row 2 (facing north) the right is east.\n"
               "Step 1: Gitali is at an end of Row 1 and Kartik faces her. Inaya is second to Kartik's right (east), so "
               "Kartik must be at seat 1 (from seat 4 there is no room): Gitali = Row 1 seat 1, Kartik = Row 2 seat 1, "
               "Inaya = Row 2 seat 3.\n"
               "Step 2: Mitul is immediately to Inaya's left (west): Row 2 seat 2. Farid faces him: Row 1 seat 2.\n"
               "Step 3: Farid faces south, so his left is east: the History teacher sits at Row 1 seat 3. Jyotsna sits "
               "in a middle seat, and the only free middle seat is Row 1 seat 3, so Jyotsna teaches History. The Maths "
               "teacher faces her: Inaya.\n"
               "Step 4: Hemant is in Row 1, so he takes Row 1 seat 4; Lalima takes Row 2 seat 4.\n"
               "Step 5: Gitali teaches English; immediately to her left (east) is Farid: Geography. Hemant Physics, "
               "Lalima Economics. Kartik and Mitul share Biology and Chemistry; Kartik is not the Biology teacher, so "
               "Kartik teaches Chemistry and Mitul Biology.\n\n"
               + table(["Seat", "Row 1 (facing south)", "Row 2 (facing north)"],
                       [(c, f"{at[10 + c]} – {sb[at[10 + c]]}", f"{at[20 + c]} – {sb[at[20 + c]]}") for c in range(1, 5)]))
ans = sb[at[opp(L2["Hemant"])]]
assert ans == "Economics"
puzzle_q(sid, LIN, DBL, "Intermediate", "Which subject is taught by the person who faces Hemant?", ans,
         ["Maths", "Biology", "Chemistry"], "Facing pairs share the same seat number",
         "Hemant sits at Row 1 seat 4; facing him is Lalima (Row 2 seat 4), who teaches Economics.",
         [ARR, "Hemant: Row 1 seat 4 ⇒ faces Row 2 seat 4 = Lalima", "Lalima teaches Economics"],
         why_others_wrong="Maths is Inaya's (she faces Jyotsna), Biology is Mitul's (he faces Farid) and Chemistry is "
                          "Kartik's (he faces Gitali).", seconds=60)
ans = at[RT(L2["Jyotsna"], 2)]
assert ans == "Gitali"
puzzle_q(sid, LIN, DBL, "Intermediate", "Who sits second to the right of Jyotsna?", ans,
         ["Hemant", "Farid", "Mitul"], "Facing south: the right is west",
         "Jyotsna is in Row 1, which faces south, so her right is towards the west: Farid (seat 2), then Gitali "
         "(seat 1).", [ARR, "Jyotsna: Row 1 seat 3; right = west", "Seat 2 = Farid, seat 1 = Gitali"],
         why_others_wrong="Hemant is immediately to her left; Farid is immediately to her right; Mitul is in the other "
                          "row.", seconds=60)
ans = next(p for p in P if sb[p] == "Biology")
pair = at[opp(L2[ans])]
assert (ans, pair) == ("Mitul", "Farid")
puzzle_q(sid, LIN, DBL, "Intermediate", "Who teaches Biology, and whom does that person face?", f"{ans}; faces {pair}",
         ["Kartik; faces Gitali", "Mitul; faces Jyotsna", "Lalima; faces Hemant"],
         "Elimination of the last two subjects",
         "Six subjects are fixed by the clues (English, Geography, History, Maths, Physics, Economics). Kartik and Mitul "
         "share Biology and Chemistry, and Kartik does not teach Biology, so Mitul does. Mitul sits at Row 2 seat 2, "
         "facing Farid.", [ARR, "Kartik ≠ Biology ⇒ Mitul = Biology", "Mitul (Row 2 seat 2) faces Farid (Row 1 seat 2)"],
         seconds=60)
stm = [("Inaya sits at an extreme end of Row 2", col(L2["Inaya"]) in (1, 4)),
       ("The History teacher faces the Maths teacher", True),
       ("Kartik sits immediately to the right of Mitul", L2["Kartik"] == RT(L2["Mitul"], 1)),
       ("Gitali and Hemant sit next to each other", abs(L2["Gitali"] - L2["Hemant"]) == 1)]
t, f = one_true(stm)
puzzle_q(sid, LIN, DBL, "Intermediate", "Which of the following statements is true?", t, f,
         "Checking each statement against the arrangement",
         "Jyotsna (History) and Inaya (Maths) both sit at seat 3, so they face each other. Inaya is at seat 3, not an "
         "end; Kartik is to Mitul's left (west), not right; Gitali (seat 1) and Hemant (seat 4) are not neighbours.",
         [ARR], seconds=60)

# ---- L3 Intermediate (standalone): seven persons facing south (seats 1..7 from the WEST end; a south-facing
#      person's right is west, so 'k-th to the right' = seat - k)
P = ["Anshul", "Bipasha", "Chaitanya", "Dimple", "Eshaan", "Fatima", "Govind"]
conds = [("Dimple sits exactly in the middle of the row.", ("Dimple",), lambda d: d == 4),
         ("Fatima sits second to the right of Dimple.", ("Fatima", "Dimple"), lambda f, d: f == d - 2),
         ("Only two persons sit between Govind and Fatima.", ("Govind", "Fatima"), lambda g, f: abs(g - f) == 3),
         ("Chaitanya sits immediately to the left of Govind.", ("Chaitanya", "Govind"), lambda c, g: c == g + 1),
         ("Eshaan sits at the extreme left end of the row.", ("Eshaan",), lambda e: e == 7),
         ("Bipasha is not an immediate neighbour of Dimple.", ("Bipasha", "Dimple"), lambda b, d: abs(b - d) != 1)]
L3 = unique(P, {p: range(1, 8) for p in P}, conds, [P])
at = {v: k for k, v in L3.items()}
assert [at[i] for i in range(1, 8)] == ["Bipasha", "Fatima", "Anshul", "Dimple", "Govind", "Chaitanya", "Eshaan"]
x_ = at[L3["Govind"] + 1]   # immediately to the left of Govind (left = east)
ans = at[L3[x_] - 3]        # third to the right of that person (right = west)
assert x_ == "Chaitanya" and ans == "Anshul"
mcq(LIN, SGL, "Intermediate",
    "Seven persons Anshul, Bipasha, Chaitanya, Dimple, Eshaan, Fatima and Govind sit in a straight row, all facing "
    "south.\n" + bullets(conds) + "\n\nWho sits third to the right of the person who sits immediately to the left of "
    "Govind?", ans, ["Fatima", "Dimple", "Bipasha"], "Facing south: the right is towards the west",
    "Number the seats 1 to 7 from the west end. A person facing south has the west on the right and the east on the "
    "left. Dimple = 4, so Fatima (second to her right) = 2. Govind is three seats from Fatima, at 5 (seat −1 does not "
    "exist). Chaitanya is immediately to Govind's left: 6. Eshaan is at the left (east) end: 7. Seats 1 and 3 remain; "
    "seat 3 is next to Dimple, so Bipasha = 1 and Anshul = 3. The person immediately to Govind's left is Chaitanya "
    "(6); third to Chaitanya's right is seat 3: Anshul.",
    ["Facing south: right = west (towards seat 1), left = east", "Dimple 4 ⇒ Fatima 2 ⇒ Govind 5 ⇒ Chaitanya 6",
     "Eshaan at the left end = seat 7", "Bipasha not next to Dimple ⇒ Bipasha 1, Anshul 3",
     "Immediately left of Govind = Chaitanya (6); 6 − 3 = seat 3 ⇒ Anshul"],
    why_others_wrong="Fatima is fourth to Chaitanya's right; Dimple is second; Bipasha is fifth. Reading 'right' as "
                     "east (as if the row faced north) leads to the wrong seats.", seconds=75, verified_by=BRUTE)

# ---- L3b Intermediate (standalone): eight persons facing north; a midway question
P = ["Lalit", "Mansi", "Neel", "Omkar", "Qadir", "Rhea", "Sonia", "Trisha"]
conds = [("Rhea sits third from the left end of the row.", ("Rhea",), lambda r: r == 3),
         ("Only three persons sit between Rhea and Omkar.", ("Rhea", "Omkar"), lambda r, o: abs(r - o) == 4),
         ("Neel sits immediately to the right of Omkar.", ("Neel", "Omkar"), lambda n, o: n == o + 1),
         ("Sonia sits immediately to the left of Qadir.", ("Sonia", "Qadir"), lambda s, q: s == q - 1),
         ("Qadir is not an immediate neighbour of Omkar.", ("Qadir", "Omkar"), lambda q, o: abs(q - o) != 1),
         ("Trisha sits second to the right of Mansi.", ("Trisha", "Mansi"), lambda t, m: t == m + 2)]
L3b = unique(P, {p: range(1, 9) for p in P}, conds, [P])
at = {v: k for k, v in L3b.items()}
assert [at[i] for i in range(1, 9)] == ["Sonia", "Qadir", "Rhea", "Mansi", "Lalit", "Trisha", "Omkar", "Neel"]
assert (L3b["Qadir"] + L3b["Neel"]) % 2 == 0
ans = at[(L3b["Qadir"] + L3b["Neel"]) // 2]
assert ans == "Lalit"
mcq(LIN, SGL, "Intermediate",
    "Eight persons Lalit, Mansi, Neel, Omkar, Qadir, Rhea, Sonia and Trisha sit in a straight row, all facing "
    "north.\n" + bullets(conds) + "\n\nWho sits exactly midway between Qadir and Neel?", ans,
    ["Mansi", "Trisha", "Rhea"], "Testing both cases of a pair clue",
    "Rhea = seat 3, so Omkar (four seats away) = 7 and Neel = 8. Sonia sits immediately to Qadir's left, so the pair "
    "takes seats (1, 2), (4, 5) or (5, 6); (5, 6) puts Qadir next to Omkar. With Sonia 4 and Qadir 5, the free seats "
    "1, 2 and 6 contain no seat that is two places to the right of another, so Trisha and Mansi cannot be placed. "
    "Hence Sonia = 1, Qadir = 2, and in seats 4, 5, 6: Mansi 4, Lalit 5, Trisha 6. Midway between Qadir (2) and Neel "
    "(8) is seat 5: Lalit.",
    ["Rhea 3 ⇒ Omkar 7 (3 − 4 is off the row), Neel 8",
     "Sonia–Qadir pair: (1, 2), (4, 5) or (5, 6); (5, 6) puts Qadir next to Omkar",
     "Pair (4, 5) leaves seats 1, 2, 6: no 'Mansi + 2' fits ⇒ Sonia 1, Qadir 2",
     "Free seats 4, 5, 6 ⇒ Mansi 4, Lalit 5, Trisha 6", "Midway between 2 and 8 = seat 5 ⇒ Lalit"],
    why_others_wrong="Mansi (4) and Trisha (6) are one seat off the midpoint; Rhea sits next to Qadir.", seconds=80,
    verified_by=BRUTE)

# ---- L3c Intermediate (standalone): a row of unknown length facing north
V = ["n", "Pratik", "Sneha", "Tanuj"]
conds = [("Pratik sits sixth from the left end.", ("Pratik",), lambda p: p == 6),
         ("Only two persons sit between Pratik and Sneha, and Sneha sits to the right of Pratik.",
          ("Pratik", "Sneha"), lambda p, s: s - p == 3),
         ("Tanuj sits fourth to the right of Sneha.", ("Tanuj", "Sneha"), lambda t, s: t == s + 4),
         ("As many persons sit to the right of Tanuj as sit to the left of Pratik.", ("n", "Tanuj", "Pratik"),
          lambda n, t, p: n - t == p - 1)]
sols = solve(V, {"n": range(3, 40)} | {p: range(1, 40) for p in V[1:]},
             [(vs, fn) for _, vs, fn in conds] + [(("n", "Tanuj"), lambda n, t: t <= n)], [V[1:]])
assert len(sols) == 1 and sols[0]["n"] == 18
n_ = sols[0]["n"]
mcq(LIN, UNK, "Intermediate",
    "Some persons sit in a straight row, all facing north. The number of persons is not given.\n" + bullets(conds)
    + "\n\nHow many persons sit in the row?", str(n_), ["17", "19", "16"], "Fixing both ends from counts",
    "Pratik is 6th from the left, so 5 persons sit to his left. Sneha is 3 seats to his right (two persons between): "
    "9th. Tanuj is 4 seats to Sneha's right: 13th. Five persons sit to Tanuj's right, so the row has 13 + 5 = 18 "
    "persons.",
    ["Left of Pratik: 5 persons", "Sneha = 6 + 3 = 9th; Tanuj = 9 + 4 = 13th from the left",
     "Right of Tanuj = 5 ⇒ total = 13 + 5 = 18"],
    why_others_wrong="17 leaves out one person; 19 counts Tanuj twice; 16 places Sneha only two seats from Pratik.",
    natural=int, seconds=60, verified_by=BRUTE)

# ---- L4 Advanced set: nine seats in a row, seven persons, two vacant seats, mixed facing
P = ["Jivika", "Kanav", "Mehak", "Oindri", "Pushkar", "Riyansh", "Sahana"]
F_ = ["f" + p for p in P]
VV = [x for p in P for x in (p, "f" + p)]
IXV = {v: i for i, v in enumerate(VV)}
RS = lambda s, f, k: s + k if f == "N" else s - k
conds = [
    ("Pushkar sits in the middle seat of the row and faces south.", ("Pushkar", "fPushkar"),
     lambda p, f: p == 5 and f == "S"),
    ("Jivika sits immediately to the left of Pushkar.", ("Jivika", "Pushkar", "fPushkar"),
     lambda j, p, f: j == RS(p, f, -1)),
    ("Kanav sits second to the right of Pushkar.", ("Kanav", "Pushkar", "fPushkar"), lambda k, p, f: k == RS(p, f, 2)),
    ("Kanav and Jivika face opposite directions.", ("fKanav", "fJivika"), lambda a, b: a != b),
    ("Sahana sits immediately to the right of Kanav.", ("Sahana", "Kanav", "fKanav"),
     lambda s, k, f: s == RS(k, f, 1)),
    ("Mehak faces north and sits second to the left of Sahana.", ("Mehak", "fMehak", "Sahana", "fSahana"),
     lambda m, fm, s, fs: fm == "N" and m == RS(s, fs, -2)),
    ("Riyansh sits at an extreme end of the row and faces the same direction as Mehak.",
     ("Riyansh", "fRiyansh", "fMehak"), lambda r, fr, fm: r in (1, 9) and fr == fm),
    ("Oindri sits immediately to the left of Riyansh.", ("Oindri", "Riyansh", "fRiyansh"),
     lambda o, r, f: o == RS(r, f, -1)),
    ("Oindri and Sahana face the same direction.", ("fOindri", "fSahana"), lambda a, b: a == b),
    ("Exactly four persons face south.", tuple(F_), lambda *f: f.count("S") == 4),
]
L4 = unique(VV, {p: range(1, 10) for p in P} | {f: "NS" for f in F_}, conds, [P])
at = {L4[p]: p for p in P}
fc = {p: L4["f" + p] for p in P}
FN = {"N": "north", "S": "south"}
assert [(at.get(i), fc.get(at.get(i))) for i in range(1, 10)] == [
    (None, None), ("Sahana", "S"), ("Kanav", "S"), ("Mehak", "N"), ("Pushkar", "S"), ("Jivika", "N"), (None, None),
    ("Oindri", "S"), ("Riyansh", "N")]
cell = lambda i: f"{at[i]} ({FN[fc[at[i]]]})" if i in at else "vacant"
ARR = "Seats 1 to 9 from the west: " + ", ".join(cell(i) for i in range(1, 10))
sid = stimulus("puzzle", "Seven persons on nine seats, facing north or south",
               "Nine seats are placed in a straight row, numbered 1 to 9 from the west end. Seven persons Jivika, Kanav, "
               "Mehak, Oindri, Pushkar, Riyansh and Sahana sit on seven of them, so two seats are vacant. Some of the "
               "persons face north and the others face south. (Facing north, the right is east; facing south, the right "
               "is west.) A vacant seat is counted as a seat but not as a person.", conds,
               "Step 1: Pushkar = seat 5, facing south, so his right is west and his left is east. Jivika "
               "(immediately to his left) = 6 and Kanav (second to his right) = 3.\n"
               "Step 2: Riyansh faces north (like Mehak) and Oindri sits immediately to his left (west), so Riyansh "
               "cannot be at seat 1: Riyansh = 9 and Oindri = 8.\n"
               "Step 3: Suppose Kanav faced north. Then Jivika faces south, Sahana = 4, and Sahana must face north "
               "(facing south, the seat second to her left would be Jivika's seat 6), so Mehak = 2; Oindri faces north "
               "like Sahana. Only Pushkar and Jivika would face south, not four: rejected.\n"
               "Step 4: So Kanav faces south and Jivika north. Sahana = 2 (Kanav's right is west). Facing north, the "
               "seat second to Sahana's left would be seat 0, so Sahana faces south and Mehak = 4. Oindri faces south "
               "like Sahana. South-facing: Pushkar, Kanav, Sahana, Oindri (four). Seats 1 and 7 are vacant.\n\n"
               + table(["Seat", "Person", "Faces"],
                       [(i, at.get(i, "vacant"), FN.get(fc.get(at.get(i)), "—")) for i in range(1, 10)]))
vac = [i for i in range(1, 10) if i not in at]
assert vac == [1, 7]
puzzle_q(sid, LIN, SGL, "Advanced", "Which two seats are vacant?", "Seats 1 and 7",
         ["Seats 1 and 9", "Seats 3 and 7", "Seats 2 and 8"], "Deciding the facing first, then the seats",
         "Only the case with Kanav facing south gives exactly four south-facing persons. Then the occupied seats are "
         "2, 3, 4, 5, 6, 8 and 9, leaving seats 1 and 7 vacant.", [ARR], seconds=100)
k_ = RS(L4["Jivika"], fc["Jivika"], 3)
ans = at[k_]
assert ans == "Riyansh"
puzzle_q(sid, LIN, SGL, "Advanced", "Who sits in the third seat to the right of Jivika?", ans,
         ["Oindri", "Mehak", "Kanav"], "Vacant seats are counted as seats, not as persons",
         "Jivika (seat 6) faces north, so her right is east: seat 7 (vacant), seat 8 (Oindri), seat 9 (Riyansh). The "
         "third seat to her right is seat 9: Riyansh.",
         [ARR, "Jivika faces north ⇒ right = east", "6 + 3 = seat 9 ⇒ Riyansh"],
         why_others_wrong="Oindri is in the second seat to her right; Mehak and Kanav are to her left.", seconds=90)
south = sorted(p for p in P if fc[p] == "S")
assert south == ["Kanav", "Oindri", "Pushkar", "Sahana"]
puzzle_q(sid, LIN, SGL, "Advanced", "Which of the following groups consists only of persons who face south?",
         "Kanav, Oindri and Sahana", ["Jivika, Kanav and Pushkar", "Mehak, Oindri and Sahana",
                                       "Kanav, Pushkar and Riyansh"], "Facing directions from the rejected case",
         "Pushkar is given as facing south. Kanav must face south (otherwise only two persons face south), Sahana must "
         "face south (otherwise Mehak's seat would be off the row) and Oindri faces the same way as Sahana. Jivika, "
         "Mehak and Riyansh face north.", [ARR, "South: Pushkar, Kanav, Sahana, Oindri; north: Jivika, Mehak, Riyansh"],
         seconds=90)
persons_between = [at[i] for i in range(L4["Sahana"] + 1, L4["Riyansh"]) if i in at]
assert len(persons_between) == 5
puzzle_q(sid, LIN, SGL, "Advanced", "How many persons sit between Sahana and Riyansh?", num_word(len(persons_between)),
         ["Six", "Four", "Seven"], "Count persons, not seats",
         "Seats 3 to 8 lie between Sahana (2) and Riyansh (9). Seat 7 is vacant, so the persons between them are Kanav, "
         "Mehak, Pushkar, Jivika and Oindri: five.",
         [ARR, "Seats between 2 and 9: 3, 4, 5, 6, 7, 8 (six seats)", "Seat 7 is vacant ⇒ five persons"],
         why_others_wrong="Six counts the vacant seat as a person; Seven counts one end as well; Four leaves out one "
                          "person.", natural=by_num, seconds=80)

# ---- L5 Advanced (standalone): six persons facing north with numbered cards
P = ["Arpit", "Bhavya", "Devansh", "Hiya", "Kiaan", "Myra"]
CARDS = [3, 5, 7, 9, 11, 13]
C_ = ["c" + p for p in P]
VV = P + C_
IXV = {v: i for i, v in enumerate(VV)}
card_at = lambda v, s: next(v[IXV["c" + p]] for p in P if v[IXV[p]] == s)
conds = [
    ("The person holding card 13 sits at an extreme end of the row.", tuple(VV),
     lambda *v: any(v[IXV[p]] in (1, 6) and v[IXV["c" + p]] == 13 for p in P)),
    ("Hiya holds card 7 and sits third to the left of the person holding card 13.", tuple(VV),
     lambda *v: v[IXV["cHiya"]] == 7 and any(v[IXV["c" + p]] == 13 and v[IXV["Hiya"]] == v[IXV[p]] - 3 for p in P)),
    ("The card numbers of Hiya's two immediate neighbours add up to 12.", tuple(VV),
     lambda *v: 1 < v[IXV["Hiya"]] < 6 and card_at(v, v[IXV["Hiya"]] - 1) + card_at(v, v[IXV["Hiya"]] + 1) == 12),
    ("Kiaan sits immediately to the right of Hiya and holds a smaller number than Hiya.",
     ("Kiaan", "Hiya", "cKiaan", "cHiya"), lambda k, h, ck, ch: k == h + 1 and ck < ch),
    ("Myra sits at an extreme end and holds card 11.", ("Myra", "cMyra"), lambda m, c: m in (1, 6) and c == 11),
    ("Arpit's card number is 4 more than Devansh's.", ("cArpit", "cDevansh"), lambda a, d: a == d + 4),
    ("Devansh does not sit next to Kiaan.", ("Devansh", "Kiaan"), lambda d, k: abs(d - k) != 1),
]
L5 = unique(VV, {p: range(1, 7) for p in P} | {c: CARDS for c in C_}, conds, [P, C_])
at = {L5[p]: p for p in P}
cd = {p: L5["c" + p] for p in P}
assert [(at[i], cd[at[i]]) for i in range(1, 7)] == [("Myra", 11), ("Devansh", 9), ("Hiya", 7), ("Kiaan", 3),
                                                     ("Bhavya", 5), ("Arpit", 13)]
ans = cd["Bhavya"] + cd[at[L5["Bhavya"] - 3]]
assert ans == 14
mcq(LIN, SGL, "Advanced",
    "Six persons Arpit, Bhavya, Devansh, Hiya, Kiaan and Myra sit in a straight row, all facing north. Each holds a "
    "card with a different number among 3, 5, 7, 9, 11 and 13.\n" + bullets(conds) +
    "\n\nWhat is the sum of the card numbers of Bhavya and the person who sits third to the left of Bhavya?",
    str(ans), ["12", "16", "18"], "Seating combined with number arithmetic",
    "Myra (11) and the holder of 13 take the two ends. Hiya is three seats to the left of the 13-holder, so the 13 is "
    "at the right end (seat 6), Hiya = 3 and Myra = 1. Kiaan = 4 with a card smaller than 7: 3 or 5. Hiya's neighbours "
    "(seats 2 and 4) add up to 12, so seat 2 holds 9 (with Kiaan 3); with Kiaan 5, seat 2 would need 7, Hiya's own "
    "card. Cards 5 and 13 remain. Arpit = Devansh + 4 allows Arpit 13 / Devansh 9 or Arpit 9 / Devansh 5; the second "
    "puts Devansh at seat 5, next to Kiaan, so Devansh = seat 2 (9), Arpit = seat 6 (13) and Bhavya = seat 5 (5). "
    "Third to Bhavya's left is seat 2, Devansh (9): 5 + 9 = 14.",
    ["13 at an end with Hiya three seats to its left ⇒ 13 at seat 6, Hiya 3, Myra 1",
     "Kiaan 4 with 3 or 5; seat 2 + seat 4 = 12 ⇒ Kiaan 3, seat 2 = 9",
     "Cards 5 and 13 left; Devansh not beside Kiaan ⇒ Devansh 2 (9), Arpit 6 (13), Bhavya 5 (5)",
     "Third to the left of Bhavya (5) = seat 2 = Devansh (9); 5 + 9 = 14"],
    why_others_wrong="12 adds Kiaan's and Devansh's cards; 16 and 18 use Hiya's or Arpit's card in place of Bhavya's "
                     "or Devansh's.", natural=int, seconds=130, verified_by=BRUTE)

# ---- L6 Advanced (standalone): unknown number of persons, one clue with two cases
V = ["n", "Kavish", "Laila", "Mohan", "Nidhi", "Ojas"]
conds = [("Kavish sits seventh from the left end.", ("Kavish",), lambda k: k == 7),
         ("Exactly five persons sit between Kavish and Laila.", ("Kavish", "Laila"), lambda k, l: abs(k - l) == 6),
         ("Mohan sits third to the right of Laila.", ("Mohan", "Laila"), lambda m, l: m == l + 3),
         ("Only two persons sit between Mohan and Kavish.", ("Mohan", "Kavish"), lambda m, k: abs(m - k) == 3),
         ("Nidhi sits sixth to the right of Kavish and is fourth from the right end.", ("n", "Nidhi", "Kavish"),
          lambda n, d, k: d == k + 6 and n - d + 1 == 4),
         ("Ojas sits exactly midway between Mohan and the person at the right end of the row.", ("n", "Ojas", "Mohan"),
          lambda n, o, m: 2 * o == m + n)]
sols = solve(V, {"n": range(5, 40)} | {p: range(1, 40) for p in V[1:]},
             [(vs, fn) for _, vs, fn in conds] + [(("n",) + tuple(V[1:]), lambda n, *v: max(v) <= n)], [V[1:]])
assert len(sols) == 1
L6 = sols[0]
assert (L6["n"], L6["Laila"], L6["Mohan"], L6["Nidhi"], L6["Ojas"]) == (16, 1, 4, 13, 10)
cnt = L6["Ojas"] - L6["Laila"] - 1
assert cnt == 8
mcq(LIN, UNK, "Advanced",
    "Some persons sit in a straight row, all facing north. The number of persons is not given; Kavish, Laila, Mohan, "
    "Nidhi and Ojas are among them.\n" + bullets(conds) + "\n\nHow many persons sit between Laila and Ojas?",
    num_word(cnt), ["Seven", "Nine", "Ten"], "Resolving a two-sided clue with a second clue",
    "Kavish is 7th from the left, so Laila (six places away) is 1st or 13th. Mohan is three places to Laila's right "
    "(4th or 16th) and three places from Kavish (4th or 10th): only 4th fits both, so Laila = 1st and Mohan = 4th. "
    "Nidhi = 7 + 6 = 13th and is 4th from the right, so the row has 13 + 3 = 16 persons. Ojas is midway between Mohan "
    "(4th) and the right end (16th): (4 + 16) ÷ 2 = 10th. Between Laila (1st) and Ojas (10th) sit 8 persons.",
    ["Laila = 7 ± 6 ⇒ 1st or 13th", "Mohan = Laila + 3 ∈ {4, 16} and Kavish ± 3 ∈ {4, 10} ⇒ Mohan 4th, Laila 1st",
     "Nidhi = 13th and 4th from the right ⇒ 16 persons", "Ojas = (4 + 16) ÷ 2 = 10th",
     "Between 1st and 10th: 10 − 1 − 1 = 8"],
    why_others_wrong="Seven and Nine are off by one in the count; Ten is Ojas's own position.", natural=by_num,
    seconds=120, verified_by=BRUTE)

# ================================================================================================ CIRCULAR SEATING
CIR = "Circular Seating Arrangement"
CEN, INOUT, SQR = "Facing centre", "Facing inside and outside", "Square and rectangular tables"

# ---- C1 Basic (standalone): seven persons around a circle facing the centre (seats 0..6 anticlockwise; right = +1)
P = ["Ansh", "Bani", "Hari", "Kirat", "Meher", "Pavitra", "Sumer"]
N = 7
conds = [("Kirat sits second to the right of Ansh.", ("Kirat", "Ansh"), lambda k, a: k == (a + 2) % N),
         ("Meher sits immediately to the left of Ansh.", ("Meher", "Ansh"), lambda m, a: m == (a - 1) % N),
         ("Sumer sits third to the right of Kirat.", ("Sumer", "Kirat"), lambda s, k: s == (k + 3) % N),
         ("Hari sits between Ansh and Kirat.", ("Hari", "Ansh", "Kirat"),
          lambda h, a, k: {(h - 1) % N, (h + 1) % N} == {a, k}),
         ("Bani is not an immediate neighbour of Sumer.", ("Bani", "Sumer"), lambda b, s: (b - s) % N not in (1, N - 1))]
C1 = unique(P, {p: range(N) for p in P} | {"Ansh": [0]}, conds, [P])
at = {v: k for k, v in C1.items()}
assert [at[i] for i in range(N)] == ["Ansh", "Hari", "Kirat", "Bani", "Pavitra", "Sumer", "Meher"]
k = (C1["Bani"] - C1["Meher"]) % N
between = [at[(C1["Bani"] - i) % N] for i in range(1, k)]
assert between == ["Kirat", "Hari", "Ansh"]
mcq(CIR, CEN, "Basic",
    "Seven persons Ansh, Bani, Hari, Kirat, Meher, Pavitra and Sumer sit around a circular table, equally spaced and "
    "all facing the centre.\n" + bullets(conds) +
    "\n\nHow many persons sit between Bani and Meher when counted to the left of Bani?", num_word(len(between)),
    ["Two", "Four", "One"], "Facing the centre: the right is anticlockwise, the left clockwise",
    "Fix Ansh. Going anticlockwise (to the right): Hari (between Ansh and Kirat), Kirat (second to Ansh's right), "
    "then two seats, then Sumer (third to Kirat's right), then Meher (immediately to Ansh's left). The two seats "
    "between Kirat and Sumer go to Bani and Pavitra; Bani cannot sit next to Sumer, so Bani sits next to Kirat and "
    "Pavitra next to Sumer. To Bani's left (clockwise) come Kirat, Hari and Ansh, then Meher: three persons.",
    ["Anticlockwise from Ansh: Ansh, Hari, Kirat, _, _, Sumer, Meher",
     "Bani not next to Sumer ⇒ Bani next to Kirat, Pavitra next to Sumer",
     "Clockwise from Bani: Kirat, Hari, Ansh, Meher ⇒ three persons between"],
    why_others_wrong="Four counts Meher too; Two misses one person; counting to Bani's right (Pavitra, Sumer) gives "
                     "Two as well, which is the wrong direction.", natural=by_num, seconds=50, verified_by=BRUTE)

# ---- C2 Intermediate set: eight persons around a circle, all facing OUTSIDE (seats 0..7 anticlockwise; for a person
#      facing outside the right is clockwise, i.e. -1)
P = ["Ishwar", "Jasmin", "Lavina", "Naren", "Prisha", "Reyansh", "Udita", "Vaibhav"]
FL = ["Daisy", "Iris", "Lily", "Lotus", "Marigold", "Orchid", "Rose", "Tulip"]
N = 8
F_ = ["f" + p for p in P]
VV = P + F_
IXV = {v: i for i, v in enumerate(VV)}
RO = lambda s, k: (s - k) % N
sf = lambda v, fl: next(v[IXV[p]] for p in P if v[IXV["f" + p]] == fl)
conds = [
    ("Naren sits third to the right of Ishwar.", ("Naren", "Ishwar"), lambda n, i: n == RO(i, 3)),
    ("Udita sits opposite Naren.", ("Udita", "Naren"), lambda u, n: u == (n + 4) % N),
    ("Prisha sits immediately to the right of Ishwar.", ("Prisha", "Ishwar"), lambda p, i: p == RO(i, 1)),
    ("Only two persons sit between Reyansh and Prisha, and Reyansh is not an immediate neighbour of Naren.",
     ("Reyansh", "Prisha", "Naren"), lambda r, p, n: (r - p) % N in (3, 5) and (r - n) % N not in (1, 7)),
    ("Jasmin sits second to the left of Vaibhav.", ("Jasmin", "Vaibhav"), lambda j, v: j == RO(v, -2)),
    ("The person who likes Lotus sits opposite Ishwar, and Lavina likes Rose.", tuple(VV),
     lambda *v: sf(v, "Lotus") == (v[IXV["Ishwar"]] + 4) % N and v[IXV["fLavina"]] == "Rose"),
    ("The person who likes Orchid sits immediately to the right of the person who likes Rose.", tuple(VV),
     lambda *v: sf(v, "Orchid") == RO(sf(v, "Rose"), 1)),
    ("Udita likes Tulip, and the person who likes Daisy sits second to the right of Udita.", tuple(VV),
     lambda *v: v[IXV["fUdita"]] == "Tulip" and sf(v, "Daisy") == RO(v[IXV["Udita"]], 2)),
    ("Ishwar likes neither Iris nor Lily, and Naren does not like Lily.", ("fIshwar", "fNaren"),
     lambda i, n: i not in ("Iris", "Lily") and n != "Lily"),
]
C2 = unique(VV, {p: range(N) for p in P} | {"Ishwar": [0]} | {f: FL for f in F_}, conds, [P, F_])
at = {C2[p]: p for p in P}
fl = {p: C2["f" + p] for p in P}
assert [(at[i], fl[at[i]]) for i in range(N)] == [
    ("Ishwar", "Marigold"), ("Udita", "Tulip"), ("Reyansh", "Orchid"), ("Lavina", "Rose"), ("Vaibhav", "Lotus"),
    ("Naren", "Iris"), ("Jasmin", "Lily"), ("Prisha", "Daisy")]
ARR = "Clockwise from Ishwar (each person's right is the next seat clockwise): " + ", ".join(
    f"{at[(-i) % N]} ({fl[at[(-i) % N]]})" for i in range(N))
sid = stimulus("puzzle", "Eight persons facing away from a round table, with flowers",
               "Eight persons Ishwar, Jasmin, Lavina, Naren, Prisha, Reyansh, Udita and Vaibhav sit around a circular "
               "table, equally spaced, all facing away from the centre. Each likes a different flower among Daisy, "
               "Iris, Lily, Lotus, Marigold, Orchid, Rose and Tulip. (Facing outside, a person's right is clockwise and "
               "the left is anticlockwise.)", conds,
               "Step 1: Fix Ishwar. Counting clockwise (to his right): Prisha is 1st, Naren 3rd. Udita is opposite Naren, "
               "i.e. immediately to Ishwar's left.\n"
               "Step 2: Two persons between Reyansh and Prisha puts Reyansh 3 places from Prisha: either next to Naren "
               "(not allowed) or two places to Ishwar's left, beyond Udita. So, going anticlockwise from Ishwar: Udita, "
               "Reyansh, then two free seats, then Naren.\n"
               "Step 3: The free seats are the two between Reyansh and Naren and the one between Naren and Prisha. "
               "Jasmin is second to Vaibhav's left (two places anticlockwise): only Vaibhav next to Naren on the "
               "Reyansh side with Jasmin next to Naren on the Prisha side fits. Lavina takes the seat next to "
               "Reyansh.\n"
               "Step 4: Lotus is opposite Ishwar: Vaibhav. Lavina likes Rose and the person to her right (clockwise) "
               "likes Orchid: Reyansh. Udita likes Tulip; second to her right (clockwise) is Prisha: Daisy. Iris, Lily "
               "and Marigold remain for Ishwar, Naren and Jasmin: Ishwar Marigold, Naren Iris, Jasmin Lily.\n\n"
               + table(["Seat (anticlockwise from Ishwar)", "Person", "Flower"],
                       [(i, at[i], fl[at[i]]) for i in range(N)]))
ans = at[RO(C2["Vaibhav"], 2)]
assert ans == "Reyansh"
puzzle_q(sid, CIR, INOUT, "Intermediate", "Who sits second to the right of Vaibhav?", ans,
         ["Naren", "Udita", "Jasmin"], "Facing outside: the right is clockwise",
         "Vaibhav faces outside, so his right is clockwise: Lavina is immediately to his right and Reyansh second.",
         [ARR, "From Vaibhav clockwise: Lavina, Reyansh"],
         why_others_wrong="Naren is immediately to Vaibhav's left and Jasmin second to his left; Udita is third to his "
                          "right.", seconds=60)
ans = fl[at[(C2["Lavina"] + 4) % N]]
assert ans == "Daisy"
puzzle_q(sid, CIR, INOUT, "Intermediate", "Which flower does the person sitting opposite Lavina like?", ans,
         ["Iris", "Lily", "Marigold"], "Opposite seats in a circle of eight",
         "Lavina sits two places to Ishwar's left; opposite her is the seat immediately to Ishwar's right: Prisha, who "
         "likes Daisy.", [ARR, "Opposite Lavina: Prisha", "Prisha likes Daisy"],
         why_others_wrong="Iris is Naren's, Lily is Jasmin's and Marigold is Ishwar's.", seconds=60)
stm = [("Jasmin likes Lily and sits next to Prisha", fl["Jasmin"] == "Lily" and (C2["Jasmin"] - C2["Prisha"]) % N in (1, 7)),
       ("Reyansh likes Rose", fl["Reyansh"] == "Rose"),
       ("Naren sits opposite the person who likes Marigold", (C2["Naren"] - C2["Ishwar"]) % N == 4),
       ("Udita sits immediately to the right of Ishwar", C2["Udita"] == RO(C2["Ishwar"], 1))]
t, f = one_true(stm)
puzzle_q(sid, CIR, INOUT, "Intermediate", "Which of the following statements is true?", t, f,
         "Checking each statement against the arrangement",
         "Jasmin likes Lily and sits between Naren and Prisha. Reyansh likes Orchid; Naren sits opposite Udita (Tulip), "
         "not Ishwar (Marigold); Udita is immediately to Ishwar's left, not his right.", [ARR], seconds=60)

# ---- C3 Advanced (standalone): triangular table; corner seats face outside, middle-of-side seats face the centre.
#      Seats 0..5 anticlockwise, even = corners. Facing the centre: right = anticlockwise (+1); facing outside: -1.
P = ["Akshara", "Biren", "Dhriti", "Elango", "Hansika", "Jairus"]
corner = lambda s: s % 2 == 0
RT3 = lambda s, k: (s - k) % 6 if corner(s) else (s + k) % 6
conds = [("Akshara sits at a corner.", ("Akshara",), lambda a: corner(a)),
         ("Biren sits second to the right of Akshara.", ("Biren", "Akshara"), lambda b, a: b == RT3(a, 2)),
         ("Dhriti sits immediately to the left of Biren.", ("Dhriti", "Biren"), lambda d, b: d == RT3(b, -1)),
         ("Elango sits second to the right of Dhriti.", ("Elango", "Dhriti"), lambda e, d: e == RT3(d, 2)),
         ("Hansika does not sit at a corner.", ("Hansika",), lambda h: not corner(h))]
C3 = unique(P, {p: range(6) for p in P} | {"Akshara": [0]}, conds, [P])
at = {v: k for k, v in C3.items()}
assert [at[i] for i in range(6)] == ["Akshara", "Elango", "Jairus", "Hansika", "Biren", "Dhriti"]
x_ = at[RT3(C3["Hansika"], 1)]
ans = at[RT3(C3[x_], -2)]
assert x_ == "Biren" and ans == "Akshara"
mcq(CIR, SQR, "Advanced",
    "Six persons Akshara, Biren, Dhriti, Elango, Hansika and Jairus sit around a table shaped like an equilateral "
    "triangle: three of them at the three corners and three at the middle of the three sides, so corner and side "
    "seats alternate. The persons at the corners face away from the centre and those at the middle of the sides face "
    "the centre.\n" + bullets(conds) +
    "\n\nWho sits second to the left of the person who sits immediately to the right of Hansika?", ans,
    ["Jairus", "Dhriti", "Elango"], "Right and left depend on the way each seat faces",
    "Number the seats anticlockwise from Akshara (corner, seat 0); even seats are corners. A person facing the centre "
    "has the right anticlockwise; a person facing outside has the right clockwise. Akshara faces outside, so Biren "
    "(second to her right) is two seats clockwise: seat 4, a corner. Biren also faces outside, so his left is "
    "anticlockwise: Dhriti = seat 5 (a side seat, facing the centre). Elango is second to Dhriti's right "
    "(anticlockwise): seat 1. Hansika is not at a corner, so she takes side seat 3 and Jairus corner seat 2. Hansika "
    "faces the centre, so immediately to her right (anticlockwise) is seat 4: Biren. Second to Biren's left "
    "(anticlockwise, as he faces outside) is seat 0: Akshara.",
    ["Akshara 0 (corner, faces out) ⇒ right = clockwise ⇒ Biren = seat 4",
     "Biren faces out ⇒ left = anticlockwise ⇒ Dhriti = 5; Dhriti faces in ⇒ Elango = 5 + 2 = seat 1",
     "Hansika not at a corner ⇒ seat 3; Jairus seat 2",
     "Right of Hansika (faces in) = seat 4 = Biren; second to Biren's left (faces out) = seat 0 = Akshara"],
    why_others_wrong="Jairus and Elango come from treating every person as facing the centre; Dhriti is immediately "
                     "to Biren's left.", seconds=120, verified_by=BRUTE)

# ---- C4 Advanced (standalone): four married couples around a circle, all facing the centre (right = +1)
M = ["Pranjal", "Siddhant", "Vikram", "Yuvan"]
W = ["Bhavika", "Diksha", "Gayatri", "Nandita"]
P = M + W
V = P + ["hG"]  # hG = Gayatri's husband (Vikram or Yuvan); the other of the two is Nandita's husband
N = 8
IXV = {v: i for i, v in enumerate(V)}
nbr = lambda a, b: (a - b) % N in (1, N - 1)
wife = lambda h, hg: {"Pranjal": "Bhavika", "Siddhant": "Diksha", "Vikram": "Gayatri" if hg == "Vikram" else "Nandita",
                      "Yuvan": "Gayatri" if hg == "Yuvan" else "Nandita"}[h]
conds = [("Men and women sit alternately.", tuple(P),
          lambda *v: len({v[i] % 2 for i in range(4)}) == 1 and len({v[i] % 2 for i in range(4, 8)}) == 1
          and v[0] % 2 != v[4] % 2),
         ("No man sits next to his wife.", tuple(V),
          lambda *v: all(not nbr(v[IXV[m]], v[IXV[wife(m, v[IXV["hG"]])]]) for m in M)),
         ("Bhavika sits third to the right of Siddhant.", ("Bhavika", "Siddhant"), lambda b, s: b == (s + 3) % N),
         ("Yuvan sits immediately to the left of Diksha.", ("Yuvan", "Diksha"), lambda y, d: y == (d - 1) % N),
         ("Gayatri sits opposite Bhavika.", ("Gayatri", "Bhavika"), lambda g, b: g == (b + 4) % N)]
sols = solve(V, {p: range(N) for p in P} | {"Siddhant": [0], "hG": ["Vikram", "Yuvan"]},
             [(vs, fn) for _, vs, fn in conds], [P])
assert len(sols) == 1
C4 = sols[0]
at = {C4[p]: p for p in P}
assert [at[i] for i in range(N)] == ["Siddhant", "Nandita", "Vikram", "Bhavika", "Yuvan", "Diksha", "Pranjal",
                                     "Gayatri"] and C4["hG"] == "Vikram"
ans = at[(C4[C4["hG"]] + 4) % N]
assert ans == "Pranjal"
mcq(CIR, CEN, "Advanced",
    "Four married couples sit around a circular table, equally spaced and all facing the centre. The men are Pranjal, "
    "Siddhant, Vikram and Yuvan; the women are Bhavika, Diksha, Gayatri and Nandita. Pranjal is married to Bhavika and "
    "Siddhant to Diksha; Vikram and Yuvan are married to Gayatri and Nandita, in some order.\n" + bullets(conds) +
    "\n\nWho sits opposite Gayatri's husband?", ans, ["Siddhant", "Yuvan", "Vikram"],
    "Seating plus a hidden pairing fixed by a 'no spouse adjacent' rule",
    "Fix Siddhant at seat 0 and count anticlockwise (to the right); men take the even seats and women the odd seats. "
    "Bhavika = 3 and Gayatri (opposite) = 7. Diksha is a woman at an odd seat with Yuvan immediately to her left "
    "(one seat clockwise); Diksha cannot be at 1 (Yuvan would be on Siddhant's seat 0, and she would sit next to her "
    "own husband), so Diksha = 5 and Yuvan = 4. Nandita = 1. Pranjal and Vikram share seats 2 and 6; seat 2 is next to "
    "Bhavika, Pranjal's wife, so Pranjal = 6 and Vikram = 2. Vikram sits next to Nandita (seat 1), so Nandita cannot be "
    "his wife: Vikram is married to Gayatri, and Yuvan (between Bhavika and Diksha) to Nandita. Opposite Vikram "
    "(seat 2) is seat 6: Pranjal.",
    ["Siddhant 0; Bhavika 3; Gayatri 7", "Yuvan–Diksha: Diksha 1 is impossible (Yuvan on seat 0) ⇒ Diksha 5, Yuvan 4",
     "Nandita 1; Pranjal not next to Bhavika ⇒ Pranjal 6, Vikram 2",
     "Vikram sits next to Nandita ⇒ his wife is Gayatri", "Opposite Vikram (2) = seat 6 = Pranjal"],
    why_others_wrong="Siddhant sits opposite Yuvan, who is Nandita's husband; Vikram is Gayatri's husband himself.",
    seconds=140, verified_by=BRUTE)

# ================================================================================================ FLOOR PUZZLES
FLR = "Floor-Based Puzzles"
FF, FA = "Floor and flat", "Floor with attribute"

# ---- F1 Basic set: seven floors, seven persons, seven musical instruments (floor 1 = lowermost)
P = ["Aarohi", "Faisal", "Hemal", "Ilesh", "Jagat", "Keya", "Mridula"]
INS = ["Drum", "Flute", "Guitar", "Harmonium", "Piano", "Sitar", "Violin"]
I_ = ["i" + p for p in P]
VV = P + I_
IXV = {v: i for i, v in enumerate(VV)}
fl_of = lambda v, ins: next(v[IXV[p]] for p in P if v[IXV["i" + p]] == ins)
conds = [
    ("Jagat lives on floor 5 and plays the Guitar.", ("Jagat", "iJagat"), lambda j, i: j == 5 and i == "Guitar"),
    ("Only two persons live between Jagat and the person who plays the Sitar.", tuple(VV),
     lambda *v: abs(v[IXV["Jagat"]] - fl_of(v, "Sitar")) == 3),
    ("Keya plays the Sitar, and Faisal lives immediately above Keya.", ("iKeya", "Faisal", "Keya"),
     lambda i, f, k: i == "Sitar" and f == k + 1),
    ("Hemal plays the Flute and lives on the topmost floor.", ("Hemal", "iHemal"),
     lambda h, i: h == 7 and i == "Flute"),
    ("Mridula lives on an odd-numbered floor below Jagat's floor.", ("Mridula", "Jagat"),
     lambda m, j: m % 2 == 1 and m < j),
    ("Aarohi does not live on floor 4.", ("Aarohi",), lambda a: a != 4),
    ("The person who plays the Piano lives immediately below the person who plays the Violin.", tuple(VV),
     lambda *v: fl_of(v, "Piano") == fl_of(v, "Violin") - 1),
    ("Mridula does not play the Drum.", ("iMridula",), lambda i: i != "Drum"),
]
F1 = unique(VV, {p: range(1, 8) for p in P} | {i: INS for i in I_}, conds, [P, I_])
at = {F1[p]: p for p in P}
ins = {p: F1["i" + p] for p in P}
assert [(at[f], ins[at[f]]) for f in range(1, 8)] == [
    ("Mridula", "Harmonium"), ("Keya", "Sitar"), ("Faisal", "Piano"), ("Ilesh", "Violin"), ("Jagat", "Guitar"),
    ("Aarohi", "Drum"), ("Hemal", "Flute")]
ARR = "Bottom to top: " + ", ".join(f"{f} {at[f]} ({ins[at[f]]})" for f in range(1, 8))
sid = stimulus("puzzle", "Seven floors and seven instruments",
               "Seven persons Aarohi, Faisal, Hemal, Ilesh, Jagat, Keya and Mridula live on the seven floors of a "
               "building, one on each floor. The lowermost floor is floor 1 and the topmost floor 7. Each of them plays "
               "a different instrument among Drum, Flute, Guitar, Harmonium, Piano, Sitar and Violin.", conds,
               "Step 1: Jagat = 5 (Guitar) and Hemal = 7 (Flute). Keya plays the Sitar and lives three floors from "
               "Jagat: floor 2 (floor 8 does not exist). Faisal = 3.\n"
               "Step 2: Mridula lives on an odd floor below 5: floor 1 or 3; 3 is Faisal's, so Mridula = 1. Floors 4 "
               "and 6 remain for Aarohi and Ilesh; Aarohi is not on 4, so Aarohi = 6 and Ilesh = 4.\n"
               "Step 3: Piano is immediately below Violin. The free instruments are Drum, Harmonium, Piano and Violin "
               "for floors 1, 3, 4 and 6; the only consecutive pair is 3–4, so Faisal plays the Piano and Ilesh the "
               "Violin.\n"
               "Step 4: Mridula does not play the Drum, so she plays the Harmonium and Aarohi the Drum.\n\n"
               + table(["Floor", "Person", "Instrument"], [(f, at[f], ins[at[f]]) for f in range(7, 0, -1)]))
ans = next(p for p in P if ins[p] == "Violin")
assert ans == "Ilesh"
puzzle_q(sid, FLR, FA, "Basic", "Who plays the Violin?", ans, ["Faisal", "Aarohi", "Mridula"],
         "An adjacency clue between two attributes",
         "The Piano player lives immediately below the Violin player. With floors 1, 3, 4 and 6 still open, the only "
         "pair of consecutive floors is 3 and 4, so Ilesh (floor 4) plays the Violin.",
         [ARR, "Free floors for Drum, Harmonium, Piano, Violin: 1, 3, 4, 6", "Consecutive pair 3–4 ⇒ Piano 3, Violin 4"],
         why_others_wrong="Faisal plays the Piano, Aarohi the Drum and Mridula the Harmonium.", seconds=45)
cnt = abs(F1["Mridula"] - F1["Jagat"]) - 1
assert cnt == 3
puzzle_q(sid, FLR, FA, "Basic", "How many persons live between Mridula and the person who plays the Guitar?",
         num_word(cnt), ["Two", "Four", "One"], "Counting floors strictly between",
         "Mridula lives on floor 1 and the Guitar player, Jagat, on floor 5. Floors 2, 3 and 4 lie between them: three "
         "persons.", [ARR, "Floors between 1 and 5: 2, 3, 4"], natural=by_num, seconds=40)
ans = ins[at[F1["Jagat"] + 1]]
assert ans == "Drum"
puzzle_q(sid, FLR, FA, "Basic", "Which instrument is played by the person who lives immediately above Jagat?", ans,
         ["Flute", "Violin", "Harmonium"], "Floor above, then attribute",
         "Jagat lives on floor 5; floor 6 belongs to Aarohi, who plays the Drum.",
         [ARR, "Floor 6 = Aarohi ⇒ Drum"],
         why_others_wrong="The Flute is Hemal's (floor 7), the Violin is Ilesh's (floor 4, below Jagat) and the "
                          "Harmonium is Mridula's.", seconds=40)

# ---- F2 Basic (standalone): a basement, a ground floor and four floors above it
LV = ["the basement", "the ground floor", "floor 1", "floor 2", "floor 3", "floor 4"]  # level index 0..5
P = ["Omesh", "Prerit", "Rukmini", "Shalu", "Toshi", "Ved"]
conds = [("Shalu lives on the ground floor.", ("Shalu",), lambda s: s == 1),
         ("Prerit lives two levels above Shalu.", ("Prerit", "Shalu"), lambda p, s: p == s + 2),
         ("Only one person lives between Prerit and Ved.", ("Prerit", "Ved"), lambda p, v: abs(p - v) == 2),
         ("Toshi lives below Shalu.", ("Toshi", "Shalu"), lambda t, s: t < s),
         ("Rukmini does not live on floor 3.", ("Rukmini",), lambda r: r != 4)]
F2 = unique(P, {p: range(6) for p in P}, conds, [P])
at = {v: k for k, v in F2.items()}
assert [at[i] for i in range(6)] == ["Toshi", "Shalu", "Rukmini", "Prerit", "Omesh", "Ved"]
ans = at[F2["Rukmini"] + 1]
assert ans == "Prerit"
mcq(FLR, FF, "Basic",
    "Six persons Omesh, Prerit, Rukmini, Shalu, Toshi and Ved live in a building that has a basement, a ground floor and "
    "four floors above the ground floor (floors 1 to 4), one person on each of these six levels. The basement is the "
    "lowest level and floor 4 the highest.\n" + bullets(conds) + "\n\nWho lives on the level immediately above "
    "Rukmini?", ans, ["Shalu", "Omesh", "Ved"], "Counting levels that start below the ground floor",
    "Shalu is on the ground floor, so Prerit (two levels up) is on floor 2. Ved is two levels from Prerit: the ground "
    "floor (taken) or floor 4, so Ved = floor 4. Toshi is below the ground floor: the basement. Rukmini and Omesh take "
    "floors 1 and 3; Rukmini is not on floor 3, so Rukmini = floor 1 and Omesh = floor 3. Immediately above Rukmini "
    "(floor 1) is floor 2: Prerit.",
    ["Levels bottom to top: basement, ground, 1, 2, 3, 4", "Shalu ground ⇒ Prerit floor 2 ⇒ Ved floor 4",
     "Toshi below ground ⇒ basement", "Rukmini floor 1, Omesh floor 3", "Above floor 1: Prerit"],
    why_others_wrong="Shalu is immediately below Rukmini; Omesh is two levels above her; Ved is on the top level.",
    seconds=45, verified_by=BRUTE)

# ---- F3 Basic (standalone): seven floors, five persons, two vacant floors
P = ["Anupam", "Garvit", "Kalpana", "Shreya", "Yatin"]
conds = [("Kalpana lives on floor 6.", ("Kalpana",), lambda k: k == 6),
         ("Garvit lives three floors below Kalpana, and the floor immediately above Garvit's floor is vacant.",
          tuple(P), lambda *f: f[1] == f[2] - 3 and f[1] + 1 not in f),
         ("Shreya lives on an even-numbered floor.", ("Shreya",), lambda s: s % 2 == 0),
         ("Anupam lives on the floor immediately above Kalpana's floor.", ("Anupam", "Kalpana"), lambda a, k: a == k + 1),
         ("Yatin does not live on the lowermost floor.", ("Yatin",), lambda y: y != 1)]
F3 = unique(P, {p: range(1, 8) for p in P}, conds, [P])
vacant = sorted(set(range(1, 8)) - set(F3.values()))
assert F3 == {"Anupam": 7, "Garvit": 3, "Kalpana": 6, "Shreya": 2, "Yatin": 5} and vacant == [1, 4]
mcq(FLR, FF, "Basic",
    "A building has seven floors, numbered 1 (lowermost) to 7 (topmost). Five persons Anupam, Garvit, Kalpana, Shreya "
    "and Yatin live in it, one person per floor, so two floors are vacant.\n" + bullets(conds) +
    "\n\nWhich two floors are vacant?", "Floors 1 and 4", ["Floors 4 and 5", "Floors 1 and 2", "Floors 2 and 4"],
    "Placing persons, then reading the empty floors",
    "Kalpana = 6, Anupam = 7, Garvit = 3 and floor 4 is vacant. Shreya lives on an even floor: 2 (4 is vacant, 6 is "
    "taken). Floors 1 and 5 remain for Yatin; he is not on floor 1, so Yatin = 5 and floor 1 is vacant.",
    ["Kalpana 6, Anupam 7, Garvit 3, floor 4 vacant", "Shreya even ⇒ 2", "Yatin not on 1 ⇒ 5; floor 1 vacant"],
    why_others_wrong="Yatin lives on floor 5 and Shreya on floor 2, so those floors are occupied.", seconds=45,
    verified_by=BRUTE)

# ---- F4 Intermediate (standalone): six floors with car colours
P = ["Aadil", "Chandni", "Ekagra", "Gyanesh", "Lopa", "Rasik"]
CL = ["Black", "Blue", "Grey", "Red", "Silver", "White"]
C_ = ["c" + p for p in P]
VV = P + C_
IXV = {v: i for i, v in enumerate(VV)}
fcar = lambda v, c: next(v[IXV[p]] for p in P if v[IXV["c" + p]] == c)
conds = [
    ("The person who owns the Red car lives on floor 4.", tuple(VV), lambda *v: fcar(v, "Red") == 4),
    ("Chandni lives two floors above the Red car owner.", tuple(VV),
     lambda *v: v[IXV["Chandni"]] == fcar(v, "Red") + 2),
    ("Ekagra owns the White car, lives on an odd-numbered floor and lives below the Red car owner.", tuple(VV),
     lambda *v: v[IXV["cEkagra"]] == "White" and v[IXV["Ekagra"]] % 2 == 1 and v[IXV["Ekagra"]] < fcar(v, "Red")),
    ("Rasik lives immediately below Ekagra.", ("Rasik", "Ekagra"), lambda r, e: r == e - 1),
    ("Lopa owns the Blue car and lives above Gyanesh.", ("Lopa", "cLopa", "Gyanesh"),
     lambda l, c, g: c == "Blue" and l > g),
    ("Aadil does not own the Red car.", ("cAadil",), lambda c: c != "Red"),
    ("The Silver car owner lives immediately above the Black car owner.", tuple(VV),
     lambda *v: fcar(v, "Silver") == fcar(v, "Black") + 1),
]
F4 = unique(VV, {p: range(1, 7) for p in P} | {c: CL for c in C_}, conds, [P, C_])
at = {F4[p]: p for p in P}
car = {p: F4["c" + p] for p in P}
assert [(at[f], car[at[f]]) for f in range(1, 7)] == [("Aadil", "Black"), ("Rasik", "Silver"), ("Ekagra", "White"),
                                                     ("Gyanesh", "Red"), ("Lopa", "Blue"), ("Chandni", "Grey")]
ans = car[at[F4["Lopa"] - 4]]
assert ans == "Black"
mcq(FLR, FA, "Intermediate",
    "Six persons Aadil, Chandni, Ekagra, Gyanesh, Lopa and Rasik live on the six floors of a building, one on each "
    "floor (floor 1 is the lowermost). Each owns a car of a different colour among Black, Blue, Grey, Red, Silver and "
    "White.\n" + bullets(conds) + "\n\nWhich colour of car is owned by the person who lives four floors below Lopa?",
    ans, ["Silver", "White", "Grey"], "Floors and an attribute fixed together",
    "The Red car is on floor 4 and Chandni on floor 6. Ekagra (White) is on an odd floor below 4: 1 or 3; Rasik is "
    "immediately below him, so Ekagra = 3 and Rasik = 2. Lopa lives above Gyanesh; the free floors are 1, 4 and 5, "
    "and Lopa (Blue) cannot be the Red car owner on floor 4, so Lopa = 5. Gyanesh and Aadil share floors 1 and 4; "
    "Aadil does not own the Red car, so Gyanesh = 4 (Red) and Aadil = 1. Silver sits immediately above Black: among "
    "the free colours (Black, Grey, Silver) for floors 1, 2 and 6, only 1–2 are consecutive, so Aadil has Black, "
    "Rasik Silver and Chandni Grey. Four floors below Lopa (5) is floor 1: Black.",
    ["Red on 4; Chandni 6", "Ekagra odd and below 4 with Rasik just below ⇒ Ekagra 3 (White), Rasik 2",
     "Lopa (Blue) above Gyanesh, not on 4 ⇒ Lopa 5; Aadil not Red ⇒ Gyanesh 4 (Red), Aadil 1",
     "Silver just above Black on floors 1, 2, 6 ⇒ Aadil Black, Rasik Silver, Chandni Grey",
     "5 − 4 = floor 1 ⇒ Black"],
    why_others_wrong="Silver is Rasik's (three floors below Lopa), White is Ekagra's and Grey is Chandni's.",
    seconds=90, verified_by=BRUTE)

# ---- F5 Intermediate (standalone): three floors with a West flat and an East flat on each
P = ["Amrit", "Bulbul", "Deepika", "Ebin", "Hamsa", "Ishani"]
FLATS = [(f, s) for f in (1, 2, 3) for s in "WE"]
conds = [("Deepika lives in the East flat of the topmost floor.", ("Deepika",), lambda d: d == (3, "E")),
         ("Amrit lives in the flat directly below Deepika's flat.", ("Amrit", "Deepika"),
          lambda a, d: a == (d[0] - 1, d[1])),
         ("Bulbul lives on the same floor as Amrit.", ("Bulbul", "Amrit"), lambda b, a: b[0] == a[0]),
         ("Ebin lives on a floor below Bulbul's floor.", ("Ebin", "Bulbul"), lambda e, b: e[0] < b[0]),
         ("Ishani and Ebin both live in West flats.", ("Ishani", "Ebin"), lambda i, e: i[1] == "W" and e[1] == "W")]
F5 = unique(P, {p: FLATS for p in P}, conds, [P])
nm = lambda fs: f"the {'West' if fs[1] == 'W' else 'East'} flat of floor {fs[0]}"
assert F5 == {"Amrit": (2, "E"), "Bulbul": (2, "W"), "Deepika": (3, "E"), "Ebin": (1, "W"), "Hamsa": (1, "E"),
              "Ishani": (3, "W")}
at = {v: k for k, v in F5.items()}
ans = at[(F5["Bulbul"][0] - 1, F5["Bulbul"][1])]
assert ans == "Ebin"
mcq(FLR, FF, "Intermediate",
    "A three-storey building (floor 1 is the lowermost) has two flats on each floor: a West flat and an East flat, "
    "with each West flat directly above the West flat of the floor below, and likewise for the East flats. Six persons "
    "Amrit, Bulbul, Deepika, Ebin, Hamsa and Ishani live in these six flats, one in each.\n" + bullets(conds) +
    "\n\nWho lives in the flat directly below Bulbul's flat?", ans, ["Hamsa", "Ishani", "Amrit"],
    "Flats in a grid: 'directly below' keeps the side, 'same floor' keeps the floor",
    "Deepika = floor 3 East, so Amrit = floor 2 East and Bulbul = floor 2 West. The free flats are floor 3 West, "
    "floor 1 West and floor 1 East. Ebin is below Bulbul, so he is on floor 1, and he lives in a West flat: floor 1 "
    "West. Ishani also lives in a West flat, and the only one left is floor 3 West. Hamsa takes floor 1 East. Directly "
    "below Bulbul (floor 2 West) is floor 1 West: Ebin.",
    ["Deepika 3E ⇒ Amrit 2E ⇒ Bulbul 2W", "Ebin below floor 2 and in a West flat ⇒ 1W",
     "Ishani (West) ⇒ 3W; Hamsa ⇒ 1E", "Directly below 2W is 1W ⇒ Ebin"],
    why_others_wrong="Hamsa is directly below Amrit; Ishani is directly above Bulbul; Amrit lives beside Bulbul on "
                     "the same floor.", seconds=60, verified_by=BRUTE)

# ---- F6 Basic (standalone): six floors
P = ["Nalin", "Rupesh", "Sakshi", "Tanya", "Ujala", "Vinod"]
conds = [("Tanya lives on floor 2.", ("Tanya",), lambda t: t == 2),
         ("Vinod lives three floors above Tanya.", ("Vinod", "Tanya"), lambda v, t: v == t + 3),
         ("Sakshi lives immediately above Vinod.", ("Sakshi", "Vinod"), lambda s, v: s == v + 1),
         ("Nalin lives on a floor below Tanya's floor.", ("Nalin", "Tanya"), lambda n, t: n < t),
         ("Ujala does not live immediately above Tanya.", ("Ujala", "Tanya"), lambda u, t: u != t + 1)]
F6 = unique(P, {p: range(1, 7) for p in P}, conds, [P])
assert F6 == {"Nalin": 1, "Rupesh": 3, "Sakshi": 6, "Tanya": 2, "Ujala": 4, "Vinod": 5}
cnt = sum(1 for p in P if F6[p] > F6["Rupesh"])
assert cnt == 3
mcq(FLR, FF, "Basic",
    "Six persons Nalin, Rupesh, Sakshi, Tanya, Ujala and Vinod live on the six floors of a building, one on each floor. "
    "The lowermost floor is floor 1 and the topmost floor 6.\n" + bullets(conds) +
    "\n\nHow many persons live on floors above Rupesh's floor?", num_word(cnt), ["Two", "Four", "One"],
    "Fix the given floor, then build up and down from it",
    "Tanya = 2, Vinod = 5 and Sakshi = 6. Nalin is below Tanya: floor 1. Floors 3 and 4 remain; Ujala is not on floor 3 "
    "(immediately above Tanya), so Ujala = 4 and Rupesh = 3. Above floor 3 live Ujala, Vinod and Sakshi: three persons.",
    ["Tanya 2 ⇒ Vinod 5 ⇒ Sakshi 6", "Nalin below 2 ⇒ 1", "Ujala not on 3 ⇒ Ujala 4, Rupesh 3",
     "Above floor 3: floors 4, 5, 6 ⇒ three persons"],
    why_others_wrong="Two leaves out Ujala; Four counts Rupesh himself; One counts only the topmost floor.",
    natural=by_num, seconds=40, verified_by=BRUTE)

# ---- F7 Advanced set: eight floors, six persons, two vacant floors, home cities
P = ["Hrishi", "Jaspreet", "Kusum", "Prabhat", "Sanober", "Zara"]
CT = ["Bhopal", "Cuttack", "Jammu", "Madurai", "Shillong", "Udaipur"]
C_ = ["c" + p for p in P]
VV = P + C_
IXV = {v: i for i, v in enumerate(VV)}
vac_of = lambda v: set(range(1, 9)) - {v[IXV[p]] for p in P}
fcity = lambda v, c: next(v[IXV[p]] for p in P if v[IXV["c" + p]] == c)
conds = [
    ("Neither the topmost floor nor the lowermost floor is vacant, and exactly two floors lie between the two vacant "
     "floors.", tuple(P),
     lambda *f: 1 in f and 8 in f and (lambda w: w[1] - w[0] == 3)(sorted(set(range(1, 9)) - set(f)))),
    ("Hrishi lives on an even-numbered floor, and the floor immediately below his floor is vacant.", tuple(P),
     lambda *f: f[0] % 2 == 0 and f[0] - 1 not in f),
    ("Sanober lives immediately above Hrishi.", ("Sanober", "Hrishi"), lambda s, h: s == h + 1),
    ("Kusum lives on the lowermost floor and is from Madurai.", ("Kusum", "cKusum"),
     lambda k, c: k == 1 and c == "Madurai"),
    ("The person from Jammu lives immediately above a vacant floor.", tuple(VV),
     lambda *v: fcity(v, "Jammu") - 1 in vac_of(v)),
    ("Zara lives immediately above the person from Jammu.", tuple(VV),
     lambda *v: v[IXV["Zara"]] == fcity(v, "Jammu") + 1),
    ("Jaspreet lives on the topmost floor.", ("Jaspreet",), lambda j: j == 8),
    ("Hrishi is from Bhopal, and the person from Udaipur lives immediately above him.", tuple(VV),
     lambda *v: v[IXV["cHrishi"]] == "Bhopal" and fcity(v, "Udaipur") == v[IXV["Hrishi"]] + 1),
    ("Zara is not from Cuttack.", ("cZara",), lambda c: c != "Cuttack"),
]
F7 = unique(VV, {p: range(1, 9) for p in P} | {c: CT for c in C_}, conds, [P, C_])
at = {F7[p]: p for p in P}
cty = {p: F7["c" + p] for p in P}
assert [(f, at.get(f), cty.get(at.get(f))) for f in range(1, 9)] == [
    (1, "Kusum", "Madurai"), (2, None, None), (3, "Prabhat", "Jammu"), (4, "Zara", "Shillong"), (5, None, None),
    (6, "Hrishi", "Bhopal"), (7, "Sanober", "Udaipur"), (8, "Jaspreet", "Cuttack")]
ARR = "Bottom to top: " + ", ".join(f"{f} {at[f]} ({cty[at[f]]})" if f in at else f"{f} vacant" for f in range(1, 9))
sid = stimulus("puzzle", "Eight floors, six residents, two empty floors",
               "A building has eight floors, numbered 1 (lowermost) to 8 (topmost). Six persons Hrishi, Jaspreet, "
               "Kusum, Prabhat, Sanober and Zara live in it, one person per floor, so two floors are vacant. Each person "
               "is from a different city among Bhopal, Cuttack, Jammu, Madurai, Shillong and Udaipur.", conds,
               "Step 1: Kusum = 1 and Jaspreet = 8. The vacant floors are three apart (two floors between them) and "
               "neither is floor 1 or 8: (2, 5), (3, 6) or (4, 7).\n"
               "Step 2: Hrishi is on an even floor with a vacant floor just below, and Sanober is just above him. "
               "(2, 5): Hrishi 6, Sanober 7. (3, 6): Hrishi 4, Sanober 5. (4, 7): Hrishi would be 8, Jaspreet's floor; "
               "rejected.\n"
               "Step 3: Jammu is immediately above a vacant floor and Zara immediately above the Jammu person. Hrishi "
               "is from Bhopal, so Jammu cannot be on Hrishi's floor. Case (3, 6): Jammu = 7 and Zara = 8, Jaspreet's "
               "floor: rejected. Case (2, 5): Jammu = 3 and Zara = 4 (Jammu on 6 is Hrishi).\n"
               "Step 4: Floors 3 and 4 hold the Jammu person and Zara, so Prabhat (the only person left) = 3, from "
               "Jammu.\n"
               "Step 5: Udaipur is immediately above Hrishi: Sanober. Zara and Jaspreet share Cuttack and Shillong; Zara "
               "is not from Cuttack, so Zara is from Shillong and Jaspreet from Cuttack.\n\n"
               + table(["Floor", "Person", "City"],
                       [(f, at.get(f, "vacant"), cty.get(at.get(f), "—")) for f in range(8, 0, -1)]))
puzzle_q(sid, FLR, FA, "Advanced", "Which two floors are vacant?", "Floors 2 and 5",
         ["Floors 3 and 6", "Floors 4 and 7", "Floors 2 and 6"], "Listing the cases for the vacant floors",
         "The vacant floors are three apart: (2, 5), (3, 6) or (4, 7). (4, 7) puts Hrishi on floor 8, and (3, 6) puts "
         "Zara on floor 8; both clash with Jaspreet on the top floor. So floors 2 and 5 are vacant.",
         [ARR, "Cases (2, 5), (3, 6), (4, 7)", "(4, 7) and (3, 6) both need floor 8 for another person ⇒ (2, 5)"],
         seconds=120)
ans = cty[at[F7["Zara"] - 1]]
assert ans == "Jammu"
cnt = sum(1 for p in P if F7["Prabhat"] < F7[p] < F7["Sanober"])
assert cnt == 2
puzzle_q(sid, FLR, FA, "Advanced", "How many persons live between Prabhat and Sanober?", num_word(cnt),
         ["Three", "Four", "One"], "Count persons, not floors",
         "Prabhat is on floor 3 and Sanober on floor 7. Floors 4, 5 and 6 lie between them, but floor 5 is vacant, so "
         "only Zara and Hrishi live between them: two persons.",
         [ARR, "Floors 4, 5, 6 lie between 3 and 7", "Floor 5 is vacant ⇒ two persons (Zara, Hrishi)"],
         why_others_wrong="Three counts the vacant floor; Four counts one of the two end persons as well; One leaves "
                          "out Zara or Hrishi.", natural=by_num, seconds=100)
ans = at[F7["Jaspreet"] - 2]
assert ans == "Hrishi"
puzzle_q(sid, FLR, FA, "Advanced", "Who lives two floors below the person from Cuttack?", ans,
         ["Sanober", "Zara", "Prabhat"], "Attribute → floor → person",
         "The person from Cuttack is Jaspreet on floor 8. Two floors below, floor 6, is Hrishi's.",
         [ARR, "Cuttack = Jaspreet (8)", "8 − 2 = floor 6 ⇒ Hrishi"],
         why_others_wrong="Sanober is immediately below Jaspreet; Zara and Prabhat are further down.", seconds=100)
stm = [("Zara is from Shillong and lives immediately above the person from Jammu",
        cty["Zara"] == "Shillong" and F7["Zara"] == F7["Prabhat"] + 1),
       ("Sanober is from Bhopal", cty["Sanober"] == "Bhopal"),
       ("Jaspreet lives immediately above a vacant floor", F7["Jaspreet"] - 1 not in F7.values()),
       ("Prabhat lives on an even-numbered floor", F7["Prabhat"] % 2 == 0)]
t, f = one_true(stm)
puzzle_q(sid, FLR, FA, "Advanced", "Which of the following statements is true?", t, f,
         "Checking each statement against the final arrangement",
         "Zara (floor 4) is from Shillong and lives just above Prabhat, the person from Jammu (floor 3). Sanober is from "
         "Udaipur; the floor below Jaspreet (7) is Sanober's, not vacant; Prabhat is on floor 3, which is odd.",
         [ARR], seconds=100)

# ---- F8 Advanced set: two towers side by side, four floors each, with professions
P = ["Abhinav", "Bansuri", "Chiranjeev", "Devika", "Girija", "Mukul", "Noor", "Pragya"]
PR = ["Architect", "Banker", "Chef", "Dentist", "Editor", "Florist", "Judge", "Pilot"]
SPOTS = [(t, f) for t in "AB" for f in range(1, 5)]
J_ = ["j" + p for p in P]
VV = P + J_
IXV = {v: i for i, v in enumerate(VV)}
spot_job = lambda v, j: next(v[IXV[p]] for p in P if v[IXV["j" + p]] == j)
conds = [
    ("Devika lives on the topmost floor of Tower B.", ("Devika",), lambda d: d == ("B", 4)),
    ("Abhinav lives in Tower A, one floor below Devika's floor.", ("Abhinav", "Devika"),
     lambda a, d: a == ("A", d[1] - 1)),
    ("Pragya lives on the same floor as Abhinav, in the other tower.", ("Pragya", "Abhinav"),
     lambda p, a: p[1] == a[1] and p[0] != a[0]),
    ("Mukul lives directly below Pragya.", ("Mukul", "Pragya"), lambda m, p: m == (p[0], p[1] - 1)),
    ("Girija lives in the same tower as Abhinav, on an even-numbered floor.", ("Girija", "Abhinav"),
     lambda g, a: g[0] == a[0] and g[1] % 2 == 0),
    ("Noor lives in the same tower as Girija, on a floor above Girija's.", ("Noor", "Girija"),
     lambda n, g: n[0] == g[0] and n[1] > g[1]),
    ("Bansuri does not live in Tower B.", ("Bansuri",), lambda b: b[0] == "A"),
    ("Pragya is the Banker, and the Chef lives directly above the Banker.", tuple(VV),
     lambda *v: v[IXV["jPragya"]] == "Banker" and spot_job(v, "Chef") == ("B", v[IXV["Pragya"]][1] + 1)),
    ("The Judge lives on the same floor as the Chef, and the Pilot lives directly below the Judge.", tuple(VV),
     lambda *v: spot_job(v, "Judge")[1] == spot_job(v, "Chef")[1] and spot_job(v, "Judge") != spot_job(v, "Chef")
     and spot_job(v, "Pilot") == (spot_job(v, "Judge")[0], spot_job(v, "Judge")[1] - 1)),
    ("The Dentist lives in Tower B, but Mukul is not the Dentist.", tuple(VV),
     lambda *v: spot_job(v, "Dentist")[0] == "B" and v[IXV["jMukul"]] != "Dentist"),
    ("The Florist lives on floor 1, and Girija is not the Architect.", tuple(VV),
     lambda *v: spot_job(v, "Florist")[1] == 1 and v[IXV["jGirija"]] != "Architect"),
]
F8 = unique(VV, {p: SPOTS for p in P} | {j: PR for j in J_}, conds, [P, J_])
at = {F8[p]: p for p in P}
job = {p: F8["j" + p] for p in P}
assert [(s, at[s], job[at[s]]) for s in SPOTS] == [
    (("A", 1), "Bansuri", "Florist"), (("A", 2), "Girija", "Editor"), (("A", 3), "Abhinav", "Pilot"),
    (("A", 4), "Noor", "Judge"), (("B", 1), "Chiranjeev", "Dentist"), (("B", 2), "Mukul", "Architect"),
    (("B", 3), "Pragya", "Banker"), (("B", 4), "Devika", "Chef")]
ARR = "; ".join(f"floor {f}: A {at[('A', f)]} ({job[at[('A', f)]]}), B {at[('B', f)]} ({job[at[('B', f)]]})"
                for f in range(4, 0, -1))
sid = stimulus("puzzle", "Two towers of four floors, with professions",
               "Two towers, A and B, stand side by side; each has four floors, numbered 1 (lowermost) to 4 (topmost), "
               "with one flat per floor. Eight persons Abhinav, Bansuri, Chiranjeev, Devika, Girija, Mukul, Noor and "
               "Pragya live in these eight flats, one in each. Each has a different profession among Architect, Banker, "
               "Chef, Dentist, Editor, Florist, Judge and Pilot. 'Directly above/below' means in the same tower.",
               conds,
               "Step 1: Devika = B4, Abhinav = A3, Pragya = B3 (same floor, other tower) and Mukul = B2.\n"
               "Step 2: Girija is in Tower A on an even floor: A2 or A4. Noor is above Girija in Tower A, so Girija "
               "cannot be on A4: Girija = A2 and Noor = A4 (A3 is Abhinav's).\n"
               "Step 3: Bansuri is in Tower A, so Bansuri = A1 and Chiranjeev = B1.\n"
               "Step 4: Pragya (B3) is the Banker, so the Chef is Devika (B4). The Judge is on floor 4 in the other "
               "tower: Noor. The Pilot is directly below the Judge: Abhinav.\n"
               "Step 5: The Dentist is in Tower B but is not Mukul: Chiranjeev. The Florist is on floor 1: Bansuri. "
               "Girija and Mukul share Architect and Editor; Girija is not the Architect, so she is the Editor and "
               "Mukul the Architect.\n\n"
               + table(["Floor", "Tower A", "Tower B"],
                       [(f, f"{at[('A', f)]} – {job[at[('A', f)]]}", f"{at[('B', f)]} – {job[at[('B', f)]]}")
                        for f in range(4, 0, -1)]))
ans = next(p for p in P if job[p] == "Architect")
assert ans == "Mukul"
puzzle_q(sid, FLR, FA, "Advanced", "Who is the Architect?", ans, ["Girija", "Chiranjeev", "Bansuri"],
         "The last two professions are split by a negative clue",
         "After the Banker, Chef, Judge, Pilot, Dentist and Florist are placed, Girija and Mukul are left with Architect "
         "and Editor. Girija is not the Architect, so Mukul is.", [ARR], seconds=110)
ans = job[at[(F8["Girija"][0], F8["Girija"][1] + 1)]]
assert ans == "Pilot"
puzzle_q(sid, FLR, FA, "Advanced", "What is the profession of the person who lives directly above Girija?", ans,
         ["Judge", "Banker", "Florist"], "Directly above = same tower, next floor",
         "Girija lives in A2; directly above her, in A3, lives Abhinav, the Pilot.",
         [ARR, "Girija = A2 ⇒ A3 = Abhinav", "Abhinav is the Pilot (directly below the Judge, Noor)"],
         why_others_wrong="The Judge (Noor) is two floors above Girija; the Banker (Pragya) is on floor 3 of the other "
                          "tower; the Florist (Bansuri) is directly below Girija.", seconds=100)
ans = at[("A", F8[next(p for p in P if job[p] == "Dentist")][1])]
assert ans == "Bansuri"
puzzle_q(sid, FLR, FA, "Advanced", "Who lives in Tower A on the same floor as the Dentist?", ans,
         ["Girija", "Mukul", "Noor"], "Same floor, other tower",
         "The Dentist is Chiranjeev in B1, so the Tower A flat on the same floor is A1: Bansuri.",
         [ARR, "Dentist = Chiranjeev (B1)", "A1 = Bansuri"], seconds=100)
cnt = sum(1 for p in P if F8[p][0] == F8["Mukul"][0] and F8[p][1] > F8["Mukul"][1])
assert cnt == 2
puzzle_q(sid, FLR, FF, "Advanced", "How many persons live above Mukul in his own tower?", num_word(cnt),
         ["One", "Three", "Five"], "Counting within one tower",
         "Mukul lives in B2. Above him in Tower B are Pragya (B3) and Devika (B4): two persons.",
         [ARR, "Tower B above B2: B3 Pragya, B4 Devika"],
         why_others_wrong="Five counts the persons above floor 2 in both towers; Three adds Mukul himself or one Tower A "
                          "person; One leaves out Devika.", natural=by_num, seconds=90)

# ================================================================================================ BOX PUZZLES
BOX = "Box-Based Puzzles"
STK, BWC = "Stacked boxes", "Boxes with weights or colours"

# ---- X1 Basic (standalone): five boxes side by side on a shelf (position 1 = left end)
B = ["J", "L", "N", "Q", "T"]
conds = [("Box N is placed at the extreme left end of the shelf.", ("N",), lambda n: n == 1),
         ("Box T is placed third to the right of box N.", ("T", "N"), lambda t, n: t == n + 3),
         ("Box Q is placed immediately to the left of box T.", ("Q", "T"), lambda q, t: q == t - 1),
         ("Box J is not placed next to box Q.", ("J", "Q"), lambda j, q: abs(j - q) != 1)]
X1 = unique(B, {b: range(1, 6) for b in B}, conds, [B])
at = {v: k for k, v in X1.items()}
assert [at[i] for i in range(1, 6)] == ["N", "L", "Q", "T", "J"]
mcq(BOX, STK, "Basic",
    "Five boxes J, L, N, Q and T are placed side by side in a single line on a shelf, as seen from the front (left and "
    "right are as seen by the viewer).\n" + bullets(conds) + "\n\nWhich box is placed exactly in the middle of the "
    "line?", f"Box {at[3]}", ["Box L", "Box T", "Box J"], "A line of boxes works like a row of seats",
    "N = position 1 and T = 4; Q, immediately to the left of T, = 3. Positions 2 and 5 remain; J cannot be next to Q "
    "(positions 2 and 4 are next to it), so J = 5 and L = 2. The middle position, 3, holds box Q.",
    ["N 1 ⇒ T 4 ⇒ Q 3", "J not next to Q ⇒ J 5, L 2", "Middle (position 3) = Q"],
    why_others_wrong="L and T are on either side of the middle box; J is at the right end.", seconds=35,
    verified_by=BRUTE)

# ---- X2 Basic (standalone): six boxes in one stack (position 1 = bottom)
B = ["D", "F", "H", "I", "O", "Y"]
conds = [("Box H is kept third from the top.", ("H",), lambda h: h == 4),
         ("Box D is kept immediately below box H.", ("D", "H"), lambda d, h: d == h - 1),
         ("Only one box is kept between box D and box Y, and box Y is not at the bottom.", ("D", "Y"),
          lambda d, y: abs(d - y) == 2 and y != 1),
         ("Box O is kept above box Y.", ("O", "Y"), lambda o, y: o > y),
         ("Box F is kept below box I.", ("F", "I"), lambda f, i: f < i)]
X2 = unique(B, {b: range(1, 7) for b in B}, conds, [B])
at = {v: k for k, v in X2.items()}
assert [at[i] for i in range(1, 7)] == ["F", "I", "D", "H", "Y", "O"]
cnt = X2["O"] - X2["F"] - 1
assert cnt == 4
mcq(BOX, STK, "Basic",
    "Six boxes D, F, H, I, O and Y are kept one above another in a single stack. Position 1 is the bottom and "
    "position 6 the top.\n" + bullets(conds) + "\n\nHow many boxes are kept between box F and box O?", num_word(cnt),
    ["Three", "Five", "Two"], "Third from the top of six = position 4",
    "Third from the top of a six-box stack is position 4: H. D = 3. Y is two positions from D and not at the bottom, "
    "so Y = 5, and O (above Y) = 6. F and I take positions 1 and 2 with F below I: F = 1, I = 2. Between F (1) and O "
    "(6) are four boxes.",
    ["H = 6 − 3 + 1 = 4; D = 3", "Y = 3 ± 2, not 1 ⇒ 5; O above ⇒ 6", "F 1, I 2", "Between 1 and 6: four boxes"],
    why_others_wrong="Three and Two miss boxes; Five counts one of the end boxes.", natural=by_num, seconds=40,
    verified_by=BRUTE)

# ---- X3 Intermediate set: eight boxes in one stack, each holding different items
B = ["C", "F", "H", "K", "M", "R", "V", "Y"]
IT = ["Books", "Cups", "Files", "Lamps", "Pens", "Shoes", "Toys", "Watches"]
I_ = ["i" + b for b in B]
VV = B + I_
IXV = {v: i for i, v in enumerate(VV)}
pos_it = lambda v, it: next(v[IXV[b]] for b in B if v[IXV["i" + b]] == it)
conds = [
    ("Box V is kept fourth from the bottom.", ("V",), lambda v: v == 4),
    ("Only three boxes are kept between box V and the box containing Toys, and box R contains Toys.", tuple(VV),
     lambda *v: abs(v[IXV["V"]] - pos_it(v, "Toys")) == 4 and v[IXV["iR"]] == "Toys"),
    ("Box C is kept immediately above box V, and the box containing Pens is kept immediately above box C.", tuple(VV),
     lambda *v: v[IXV["C"]] == v[IXV["V"]] + 1 and pos_it(v, "Pens") == v[IXV["C"]] + 1),
    ("Box Y contains Pens, and box H is kept above box Y.", ("iY", "H", "Y"), lambda i, h, y: i == "Pens" and h > y),
    ("Box F is kept at the bottom of the stack.", ("F",), lambda f: f == 1),
    ("Box K contains Watches, and box M is kept immediately below box K.", ("iK", "M", "K"),
     lambda i, m, k: i == "Watches" and m == k - 1),
    ("The box containing Lamps is kept immediately below the box containing Books.", tuple(VV),
     lambda *v: pos_it(v, "Lamps") == pos_it(v, "Books") - 1),
    ("Box H contains Cups, and box M does not contain Books.", ("iH", "iM"), lambda h, m: h == "Cups" and m != "Books"),
    ("The box containing Shoes is kept at an odd-numbered position.", tuple(VV), lambda *v: pos_it(v, "Shoes") % 2 == 1),
]
# position-only consequences of the clues above (R holds Toys; Y holds Pens), added only to prune the search early
HID = [("", ("V", "R"), lambda v, r: abs(v - r) == 4), ("", ("C", "V"), lambda c, v: c == v + 1),
       ("", ("Y", "C"), lambda y, c: y == c + 1), ("", ("iR",), lambda i: i == "Toys"), ("", ("iY",), lambda i: i == "Pens")]
X3 = unique(VV, {b: range(1, 9) for b in B} | {i: IT for i in I_}, conds + HID, [B, I_])
at = {X3[b]: b for b in B}
it = {b: X3["i" + b] for b in B}
assert [(at[i], it[at[i]]) for i in range(1, 9)] == [
    ("F", "Shoes"), ("M", "Files"), ("K", "Watches"), ("V", "Lamps"), ("C", "Books"), ("Y", "Pens"), ("H", "Cups"),
    ("R", "Toys")]
ARR = "Bottom to top: " + ", ".join(f"{i} {at[i]} ({it[at[i]]})" for i in range(1, 9))
sid = stimulus("puzzle", "Eight boxes in a stack, with their contents",
               "Eight boxes C, F, H, K, M, R, V and Y are kept one above another in a single stack (position 1 is the "
               "bottom and 8 the top). Each box contains different items among Books, Cups, Files, Lamps, Pens, Shoes, "
               "Toys and Watches.", conds,
               "Step 1: V = 4. Toys are four positions from V: position 8 (position 0 does not exist), in box R.\n"
               "Step 2: C = 5 and the Pens box = 6; Y holds Pens, so Y = 6, and H (above Y) = 7. F = 1.\n"
               "Step 3: Positions 2 and 3 remain for K and M. M is immediately below K, so M = 2 and K = 3; K holds "
               "Watches.\n"
               "Step 4: H holds Cups. Books, Files, Lamps and Shoes remain for F (1), M (2), V (4) and C (5). Lamps is "
               "immediately below Books: V–C (4–5) or F–M (1–2). F–M would give M the Books, which is not allowed, so "
               "V holds Lamps and C Books.\n"
               "Step 5: Shoes is at an odd position: F (1); M holds Files.\n\n"
               + table(["Position", "Box", "Contents"], [(i, at[i], it[at[i]]) for i in range(8, 0, -1)]))
ans = next(b for b in B if it[b] == "Lamps")
assert ans == "V"
puzzle_q(sid, BOX, STK, "Intermediate", "Which box contains Lamps?", f"Box {ans}", ["Box C", "Box M", "Box F"],
         "An adjacency clue between two contents",
         "Lamps lie immediately below Books. The two possible pairs are V–C (positions 4–5) and F–M (positions 1–2); "
         "the second would put Books in M, which is ruled out, so V contains Lamps.", [ARR], seconds=70)
cnt = abs(X3["Y"] - pos_it([X3[v] for v in VV], "Files")) - 1
assert cnt == 3
puzzle_q(sid, BOX, STK, "Intermediate", "How many boxes are kept between box Y and the box containing Files?",
         num_word(cnt), ["Two", "Four", "Five"], "Contents → position → count",
         "Files are in box M at position 2 and box Y is at position 6. Positions 3, 4 and 5 lie between: three boxes.",
         [ARR, "Files = M (2); Y = 6", "Between: 3, 4, 5"], natural=by_num, seconds=60)
ans = it[at[X3["H"] - 1]]
assert ans == "Pens"
puzzle_q(sid, BOX, STK, "Intermediate", "What does the box kept immediately below box H contain?", ans,
         ["Toys", "Books", "Cups"], "Neighbouring positions in a stack",
         "Box H is at position 7; immediately below it is box Y at position 6, which contains Pens.",
         [ARR, "Below H (7) = Y (6) ⇒ Pens"],
         why_others_wrong="Toys are in R, above H; Books are in C (position 5); Cups are in H itself.", seconds=55)
stm = [("Box K – Watches – position 3", it["K"] == "Watches" and X3["K"] == 3),
       ("Box F – Files – position 1", it["F"] == "Files"), ("Box C – Lamps – position 5", it["C"] == "Lamps"),
       ("Box H – Toys – position 7", it["H"] == "Toys")]
t, f = one_true(stm)
puzzle_q(sid, BOX, STK, "Intermediate", "Which of the following box – contents – position combinations is correct?",
         t, f, "Reading three facts off the final stack",
         "K is at position 3 and contains Watches. F (position 1) holds Shoes, C (5) Books and H (7) Cups.", [ARR],
         seconds=60)

# ---- X4 Intermediate set: six coloured boxes in a cupboard with three shelves, two boxes (left, right) per shelf
B = ["B", "D", "G", "J", "L", "P"]
CO = ["Black", "Green", "Orange", "Purple", "White", "Yellow"]
SH = {3: "top", 2: "middle", 1: "bottom"}
SPOTS = [(s, side) for s in (1, 2, 3) for side in "LR"]
K_ = ["k" + b for b in B]
VV = B + K_
IXV = {v: i for i, v in enumerate(VV)}
spot_col = lambda v, c: next(v[IXV[b]] for b in B if v[IXV["k" + b]] == c)
conds = [
    ("Box D is on the top shelf, on the right side, and it is White.", ("D", "kD"),
     lambda d, k: d == (3, "R") and k == "White"),
    ("Box B is directly below box D.", ("B", "D"), lambda b, d: b == (d[0] - 1, d[1])),
    ("Box L is on the same shelf as box D.", ("L", "D"), lambda l, d: l[0] == d[0]),
    ("The Yellow box is on the same shelf as box B.", tuple(VV),
     lambda *v: spot_col(v, "Yellow")[0] == v[IXV["B"]][0] and spot_col(v, "Yellow") != v[IXV["B"]]),
    ("Box J is not on the middle shelf, and box G is on the right side.", ("J", "G"),
     lambda j, g: j[0] != 2 and g[1] == "R"),
    ("The Black box is directly above the Orange box.", tuple(VV),
     lambda *v: spot_col(v, "Black") == (spot_col(v, "Orange")[0] + 1, spot_col(v, "Orange")[1])),
    ("The Green box is directly above the Yellow box.", tuple(VV),
     lambda *v: spot_col(v, "Green") == (spot_col(v, "Yellow")[0] + 1, spot_col(v, "Yellow")[1])),
]
X4 = unique(VV, {b: SPOTS for b in B} | {k: CO for k in K_}, conds, [B, K_])
at = {X4[b]: b for b in B}
co = {b: X4["k" + b] for b in B}
assert [(s, at[s], co[at[s]]) for s in SPOTS] == [
    ((1, "L"), "J", "Purple"), ((1, "R"), "G", "Orange"), ((2, "L"), "P", "Yellow"), ((2, "R"), "B", "Black"),
    ((3, "L"), "L", "Green"), ((3, "R"), "D", "White")]
ARR = "; ".join(f"{SH[s].capitalize()} shelf: left {at[(s, 'L')]} ({co[at[(s, 'L')]]}), right {at[(s, 'R')]} "
                f"({co[at[(s, 'R')]]})" for s in (3, 2, 1))
sid = stimulus("puzzle", "Six coloured boxes in a three-shelf cupboard",
               "A cupboard has three shelves: top, middle and bottom. Each shelf holds two boxes, one on the left side "
               "and one on the right side, so the left boxes are directly above one another, and so are the right "
               "boxes. Six boxes B, D, G, J, L and P are kept in the cupboard, each of a different colour among Black, "
               "Green, Orange, Purple, White and Yellow.", conds,
               "Step 1: D = top-right (White), B = middle-right, L = top-left.\n"
               "Step 2: The free places are middle-left, bottom-left and bottom-right. G is on the right: bottom-right. "
               "J is not on the middle shelf: bottom-left. P takes middle-left.\n"
               "Step 3: The Yellow box shares B's shelf: P (middle-left). The Green box is directly above it: L.\n"
               "Step 4: Black is directly above Orange. The colours left are Black, Orange and Purple for B "
               "(middle-right), G (bottom-right) and J (bottom-left); the only vertical pair is B above G, so B is Black, "
               "G Orange and J Purple.\n\n"
               + table(["Shelf", "Left", "Right"],
                       [(SH[s], f"{at[(s, 'L')]} – {co[at[(s, 'L')]]}", f"{at[(s, 'R')]} – {co[at[(s, 'R')]]}")
                        for s in (3, 2, 1)]))
puzzle_q(sid, BOX, BWC, "Intermediate", "What is the colour of box J?", co["J"], ["Orange", "Black", "Yellow"],
         "The last colours follow from a vertical pair",
         "Black must be directly above Orange; among B, G and J only B (middle-right) is directly above another of them "
         "(G, bottom-right). So B is Black, G Orange, and J gets the remaining colour, Purple.", [ARR], seconds=60)
ans = at[(X4["L"][0] - 1, X4["L"][1])]
assert ans == "P"
puzzle_q(sid, BOX, BWC, "Intermediate", "Which box is kept directly below the Green box?", f"Box {ans}",
         ["Box B", "Box J", "Box D"], "Same side, one shelf lower",
         "The Green box is L (top-left). Directly below it, on the middle shelf's left side, is box P.",
         [ARR, "Green = L (top-left) ⇒ middle-left = P"],
         why_others_wrong="B is below D (right side); J is two shelves below L; D is beside L.", seconds=55)
ans = at[(X4["G"][0], "L")]
assert ans == "J"
puzzle_q(sid, BOX, BWC, "Intermediate", "Which box is kept on the same shelf as the Orange box?", f"Box {ans}",
         ["Box P", "Box B", "Box L"], "Colour → box → shelf",
         "The Orange box is G on the bottom shelf; the other box on that shelf is J.", [ARR], seconds=55)
stm = [("Box P is Yellow and is on the middle shelf", co["P"] == "Yellow" and X4["P"][0] == 2),
       ("Box L is directly above box B", X4["L"] == (X4["B"][0] + 1, X4["B"][1])),
       ("Box G is Black", co["G"] == "Black"), ("Box D is on the left side", X4["D"][1] == "L")]
t, f = one_true(stm)
puzzle_q(sid, BOX, BWC, "Intermediate", "Which of the following statements is true?", t, f,
         "Checking each statement against the cupboard",
         "P is Yellow on the middle shelf. L is above P, not B; G is Orange; D is on the right side.", [ARR],
         seconds=55)

# ---- X5 Advanced (standalone): nine boxes of three sizes; no two boxes of the same size touch
B = list("ACEGKMRTW")
Z_ = ["z" + b for b in B]
VV = B + Z_
IXV = {v: i for i, v in enumerate(VV)}
size_at = lambda v, p: next(v[IXV["z" + b]] for b in B if v[IXV[b]] == p)
conds = [
    ("Exactly three boxes are small, three are medium and three are large.", tuple(Z_),
     lambda *z: z.count("S") == 3 and z.count("M") == 3 and z.count("L") == 3),
    ("No two boxes of the same size are kept one directly on top of the other.", tuple(VV),
     lambda *v: all(size_at(v, i) != size_at(v, i + 1) for i in range(1, 9))),
    ("Box K is a large box kept at position 5.", ("K", "zK"), lambda k, z: k == 5 and z == "L"),
    ("Box W is small and is kept immediately above box K.", ("W", "K", "zW"), lambda w, k, z: w == k + 1 and z == "S"),
    ("The top box and the bottom box are both medium.", tuple(VV),
     lambda *v: size_at(v, 9) == "M" and size_at(v, 1) == "M"),
    ("Box A is kept at the top, and box T immediately below box A.", ("A", "T"), lambda a, t: a == 9 and t == 8),
    ("Box T is large, and box E is a small box kept below box K.", tuple(VV),
     lambda *v: v[IXV["zT"]] == "L" and v[IXV["zE"]] == "S" and v[IXV["E"]] < v[IXV["K"]]),
    ("Box G is kept immediately above box E.", ("G", "E"), lambda g, e: g == e + 1),
    ("Box R is kept at the bottom, and box C is medium.", ("R", "zC"), lambda r, z: r == 1 and z == "M"),
]
X5 = unique(VV, {b: range(1, 10) for b in B} | {z: "SML" for z in Z_}, conds, [B])
at = {X5[b]: b for b in B}
assert [(at[i], X5["z" + at[i]]) for i in range(1, 10)] == [
    ("R", "M"), ("E", "S"), ("G", "L"), ("M", "S"), ("K", "L"), ("W", "S"), ("C", "M"), ("T", "L"), ("A", "M")]
ans = at[X5["K"] - 1]
assert ans == "M"
mcq(BOX, BWC, "Advanced",
    "Nine boxes A, C, E, G, K, M, R, T and W are kept one above another in a single stack (position 1 is the bottom and "
    "9 the top). Each box is small, medium or large.\n" + bullets(conds) +
    "\n\nWhich box is kept immediately below box K?", f"Box {ans}", ["Box G", "Box E", "Box C"],
    "Counting sizes against the 'no two alike in contact' rule",
    "Fixed so far: R (1, medium), K (5, large), W (6, small), T (8, large), A (9, medium). Position 7 lies between a "
    "small box and a large box, so it must be medium. That gives three mediums (1, 7, 9) and two larges (5, 8), so "
    "positions 2, 3 and 4 hold the third large box and the two remaining small boxes. Position 4 touches K (large) "
    "and position 2 touches R (medium); the only order with no two alike touching is small, large, small. E is a small "
    "box below K with G directly above it: E = 2 (if E were 4, G would be on K's position), G = 3 (large). C is medium, "
    "so C = 7, and M takes position 4 (small), immediately below K.",
    ["Known: R1 M, K5 L, W6 S, T8 L, A9 M", "Position 7 between S and L ⇒ M (mediums complete: 1, 7, 9)",
     "Positions 2–4 = one L + two S with no repeats ⇒ S, L, S", "E small with G above ⇒ E 2, G 3",
     "C medium ⇒ 7; M ⇒ 4, immediately below K"],
    why_others_wrong="G is two places below K and E three; C is two places above K.", seconds=140, verified_by=BRUTE)

# ---- X6 Advanced (standalone): six boxes with weights fixed by ratios
B = ["P", "Q", "S", "U", "X", "Z"]
WT = [6, 9, 12, 18, 24, 30]
W_ = ["w" + b for b in B]
VV = B + W_
IXV = {v: i for i, v in enumerate(VV)}
conds = [
    ("The heaviest box is kept at the bottom.", tuple(VV),
     lambda *v: any(v[IXV[b]] == 1 and v[IXV["w" + b]] == 30 for b in B)),
    ("Box X weighs twice as much as box P.", ("wX", "wP"), lambda x, p: x == 2 * p),
    ("Box Z is kept immediately above box X and weighs twice as much as box X.", ("Z", "X", "wZ", "wX"),
     lambda z, x, wz, wx: z == x + 1 and wz == 2 * wx),
    ("Box P is kept immediately above box Z.", ("P", "Z"), lambda p, z: p == z + 1),
    ("Box S weighs half as much as box U, and box S is kept at the top.", ("wS", "wU", "S"),
     lambda s, u, ps: 2 * s == u and ps == 6),
    ("Box U is heavier than the box kept immediately below it.", tuple(VV),
     lambda *v: v[IXV["U"]] > 1 and v[IXV["wU"]] > next(v[IXV["w" + b]] for b in B if v[IXV[b]] == v[IXV["U"]] - 1)),
]
X6 = unique(VV, {b: range(1, 7) for b in B} | {w: WT for w in W_}, conds, [B, W_])
at = {X6[b]: b for b in B}
wt = {b: X6["w" + b] for b in B}
assert [(at[i], wt[at[i]]) for i in range(1, 7)] == [("Q", 30), ("X", 12), ("Z", 24), ("P", 6), ("U", 18), ("S", 9)]
ans = sum(wt[at[i]] for i in range(X6["Z"] + 1, 7))
assert ans == 33
mcq(BOX, BWC, "Advanced",
    "Six boxes P, Q, S, U, X and Z are kept one above another in a single stack (position 1 is the bottom and 6 the "
    "top). Their weights are 6, 9, 12, 18, 24 and 30 kg, one weight per box.\n" + bullets(conds) +
    "\n\nWhat is the total weight of the boxes kept above box Z?", f"{ans} kg", ["27 kg", "39 kg", "45 kg"],
    "Weight chains first, then positions",
    "Weights: X = 2P and Z = 2X = 4P. From the list, only P = 6, X = 12, Z = 24 works (P = 9 would need 36). S = U ÷ 2 "
    "from the remaining 9, 18, 30 gives S = 9, U = 18, and Q = 30, the heaviest, at the bottom. Positions: S = 6; X, Z, "
    "P are consecutive upwards in positions 2–4 or 3–5. If they were 3–5, U would be at 2, directly above Q (30 kg), "
    "but U must be heavier than the box below it. So X 2, Z 3, P 4, U 5. Above Z: P 6 + U 18 + S 9 = 33 kg.",
    ["Z = 2X = 4P ⇒ P 6, X 12, Z 24", "S = U/2 ⇒ S 9, U 18; Q 30 at the bottom",
     "X, Z, P consecutive; U above a lighter box ⇒ X 2, Z 3, P 4, U 5, S 6", "Above Z: 6 + 18 + 9 = 33 kg"],
    why_others_wrong="27 kg leaves out P; 39 kg counts Z itself in place of U; 45 kg also adds X, which is below Z.",
    natural=lambda t: int(t.split()[0]), seconds=130, verified_by=BRUTE)

# ================================================================================================ MONTH / DATE / YEAR
MB_, DB_, YB_ = "Month-based", "Date-based", "Year-based"

# ---- M1 Basic (standalone): five birthdays in five alternate months
P = ["Chaitra", "Dhanush", "Ketaki", "Puneet", "Shivam"]
MS = [3, 5, 7, 9, 11]
conds = [("Ketaki's birthday is in July.", ("Ketaki",), lambda k: k == 7),
         ("Only one of the five has a birthday month between Ketaki's month and Puneet's month.", ("Ketaki", "Puneet"),
          lambda k, p: abs(MS.index(k) - MS.index(p)) == 2),
         ("Puneet's birthday is in a month that has 30 days.", ("Puneet",), lambda p: MDAYS[p] == 30),
         ("Shivam's birthday month comes immediately before Ketaki's among the five months.", ("Shivam", "Ketaki"),
          lambda s, k: MS.index(s) == MS.index(k) - 1),
         ("Dhanush's birthday comes later in the year than Chaitra's.", ("Dhanush", "Chaitra"), lambda d, c: d > c)]
M1 = unique(P, {p: MS for p in P}, conds, [P])
assert M1 == {"Chaitra": 3, "Dhanush": 9, "Ketaki": 7, "Puneet": 11, "Shivam": 5}
ans = next(p for p in P if M1[p] == 9)
mcq(MON, MB_, "Basic",
    "Five friends Chaitra, Dhanush, Ketaki, Puneet and Shivam have their birthdays in five different months of the "
    "same year: March, May, July, September and November, one month each.\n" + bullets(conds) +
    "\n\nWhose birthday is in September?", ans, ["Puneet", "Chaitra", "Shivam"],
    "Using the number of days in a month",
    "Ketaki = July. Puneet is two places from July in the list: March or November; November has 30 days and March 31, "
    "so Puneet = November. Shivam is just before Ketaki: May. March and September remain; Dhanush comes later than "
    "Chaitra, so Chaitra = March and Dhanush = September.",
    ["Ketaki July", "Puneet: March or November; 30 days ⇒ November", "Shivam May",
     "Dhanush after Chaitra ⇒ Chaitra March, Dhanush September"],
    why_others_wrong="Puneet is in November, Chaitra in March and Shivam in May.", seconds=45, verified_by=BRUTE)

# ---- M2 Intermediate set: nine slots (7th, 15th, 23rd of May, June, July), eight persons, one slot unused
P = ["Aryan", "Falgun", "Ojal", "Prem", "Rinki", "Smita", "Tulsi", "Varun"]
SLOTS = [(m, d) for m in (5, 6, 7) for d in (7, 15, 23)]
SI = {s: i for i, s in enumerate(SLOTS)}
sname = lambda s: f"{s[1]} {MNAME[s[0]]}"
pbtw = lambda v, a, b: sum(1 for x in v if min(SI[a], SI[b]) < SI[x] < max(SI[a], SI[b]))
IXP = {p: i for i, p in enumerate(P)}
conds = [
    ("Prem's visit is on 15 June.", ("Prem",), lambda p: p == (6, 15)),
    ("Smita visits in July, and exactly two persons visit between Prem and Smita.", tuple(P),
     lambda *v: v[IXP["Smita"]][0] == 7 and pbtw(v, v[IXP["Prem"]], v[IXP["Smita"]]) == 2),
    ("Falgun visits on the 23rd of a month, after Smita.", ("Falgun", "Smita"),
     lambda f, s: f[1] == 23 and SI[f] > SI[s]),
    ("Ojal visits on the date immediately before Smita's date in the list of nine.", ("Ojal", "Smita"),
     lambda o, s: SI[o] == SI[s] - 1),
    ("Rinki visits on the 7th of a month that has 30 days.", ("Rinki",), lambda r: r[1] == 7 and MDAYS[r[0]] == 30),
    ("Varun visits on the date immediately after Prem's date.", ("Varun", "Prem"), lambda v_, p: SI[v_] == SI[p] + 1),
    ("Aryan visits on the 15th of a month, and Tulsi visits before Aryan.", ("Aryan", "Tulsi"),
     lambda a, t: a[1] == 15 and SI[t] < SI[a]),
]
M2 = unique(P, {p: SLOTS for p in P}, conds, [P])
at = {M2[p]: p for p in P}
assert [at.get(s) for s in SLOTS] == ["Tulsi", "Aryan", None, "Rinki", "Prem", "Varun", "Ojal", "Smita", "Falgun"]
ARR = "In date order: " + ", ".join(f"{sname(s)} {at.get(s, '(no visit)')}" for s in SLOTS)
sid = stimulus("puzzle", "Eight visits on nine possible dates",
               "Eight persons Aryan, Falgun, Ojal, Prem, Rinki, Smita, Tulsi and Varun each visit a museum once. The "
               "museum takes visitors only on the 7th, 15th and 23rd of May, June and July of the same year, so there "
               "are nine possible dates. Each person visits on a different date, so one of the nine dates has no "
               "visitor. 'Between' counts persons, not dates.", conds,
               "Step 1: Prem = 15 June and Varun = 23 June.\n"
               "Step 2: Smita visits in July with exactly two persons between her and Prem. After Prem come Varun "
               "(23 June) and then the July dates; Smita on 15 July puts Varun and the 7 July visitor between them. "
               "Smita on 7 July would leave one person between; Smita on 23 July would leave no date for Falgun after "
               "her. So Smita = 15 July, Ojal = 7 July and Falgun = 23 July.\n"
               "Step 3: Rinki is on the 7th of a 30-day month: June (May and July have 31 days), so Rinki = 7 June.\n"
               "Step 4: The May dates remain for Aryan, Tulsi and the empty date. Aryan is on the 15th: 15 May. Tulsi is "
               "before him: 7 May. Nobody visits on 23 May.\n\n"
               + table(["Date", "Visitor"], [(sname(s), at.get(s, "—")) for s in SLOTS]))
puzzle_q(sid, MON, DB_, "Intermediate", "On which date does nobody visit?", "23 May", ["7 July", "23 June", "15 May"],
         "The empty date comes out last", "All dates in June and July are taken (Rinki, Prem, Varun, Ojal, Smita, "
         "Falgun); in May, Tulsi takes the 7th and Aryan the 15th, so 23 May is empty.", [ARR], seconds=70)
order = [at[s] for s in SLOTS if s in at]
ans = order[order.index("Aryan") + 1]
assert ans == "Rinki"
puzzle_q(sid, MON, DB_, "Intermediate", "Who is the next visitor after Aryan?", ans, ["Prem", "Tulsi", "Varun"],
         "Skip the empty date", "Aryan visits on 15 May; 23 May has no visitor, so the next visitor is Rinki on 7 June.",
         [ARR, "After 15 May: 23 May (empty), then 7 June = Rinki"], seconds=60)
cnt = order.index("Varun") - order.index("Tulsi") - 1
assert cnt == 3
puzzle_q(sid, MON, DB_, "Intermediate", "How many persons visit between Tulsi and Varun?", num_word(cnt),
         ["Four", "Two", "Five"], "Count persons; the empty date is not a person",
         "Between Tulsi (7 May) and Varun (23 June) visit Aryan, Rinki and Prem: three persons. The empty 23 May is a "
         "date, not a person.", [ARR], natural=by_num, seconds=60)
ans = sname(M2["Ojal"])
puzzle_q(sid, MON, DB_, "Intermediate", "On which date does Ojal visit?", ans, ["15 July", "23 June", "7 June"],
         "Immediately before Smita in date order",
         "Smita visits on 15 July, and Ojal on the date just before it in the list of nine: 7 July.", [ARR],
         seconds=55)

# ---- M3 Intermediate set: holidays on the first Monday of six months of 2026
P = ["Ankit", "Gopi", "Kanchan", "Manas", "Rachit", "Vrinda"]
HM = [2, 3, 4, 5, 6, 7]
first_mon = {m: next(dt.date(2026, m, d) for d in range(1, 8) if dt.date(2026, m, d).weekday() == 0) for m in HM}
assert dt.date(2026, 1, 1).weekday() == 3  # Thursday
assert [first_mon[m].day for m in HM] == [2, 2, 6, 4, 1, 6]
day = lambda m: first_mon[m].day
conds = [("Ankit's holiday falls on the 1st of its month.", ("Ankit",), lambda a: day(a) == 1),
         ("Rachit's holiday is in the month immediately after Ankit's month.", ("Rachit", "Ankit"),
          lambda r, a: r == a + 1),
         ("Gopi's and Kanchan's holidays both fall on the 2nd of their months, and Gopi's month comes before "
          "Kanchan's.", ("Gopi", "Kanchan"), lambda g, k: day(g) == 2 and day(k) == 2 and g < k),
         ("Manas's holiday falls on an earlier date of its month than Vrinda's holiday does.", ("Manas", "Vrinda"),
          lambda m, v_: day(m) < day(v_))]
M3 = unique(P, {p: HM for p in P}, conds, [P])
assert M3 == {"Ankit": 6, "Gopi": 2, "Kanchan": 3, "Manas": 5, "Rachit": 7, "Vrinda": 4}
ds = lambda d: f"{d.day} {MNAME[d.month]} 2026"
ARR = "; ".join(f"{p}: {ds(first_mon[M3[p]])}" for p in sorted(P, key=M3.get))
sid = stimulus("puzzle", "Holidays on first Mondays of 2026",
               "Six employees Ankit, Gopi, Kanchan, Manas, Rachit and Vrinda each take one day off in 2026. Each takes "
               "the first Monday of a different month among February, March, April, May, June and July. 1 January 2026 "
               "is a Thursday.", conds,
               "Step 1: Find the first Monday of each month. 1 January is a Thursday, so 1 February (31 days later, "
               "31 = 4 weeks + 3 days) is a Sunday; 1 March (28 days later) is also a Sunday; 1 April is a Wednesday; "
               "1 May a Friday; 1 June a Monday; 1 July a Wednesday. First Mondays: 2 February, 2 March, 6 April, 4 May, "
               "1 June and 6 July.\n"
               "Step 2: Only June's first Monday is on the 1st, so Ankit = June and Rachit = July.\n"
               "Step 3: The 2nd occurs in February and March: Gopi = February, Kanchan = March.\n"
               "Step 4: April (6th) and May (4th) remain; Manas's date is earlier, so Manas = May and Vrinda = April.\n\n"
               + table(["Employee", "Month", "Date of holiday"],
                       [(p, MNAME[M3[p]], ds(first_mon[M3[p]])) for p in sorted(P, key=M3.get)]))
ans = ds(first_mon[M3["Vrinda"]])
assert ans == "6 April 2026"
puzzle_q(sid, MON, DB_, "Intermediate", "On which date is Vrinda's holiday?", ans,
         ["4 May 2026", "6 July 2026", "2 April 2026"], "Weekday of the 1st of each month",
         "Vrinda takes April's first Monday. 1 April 2026 is a Wednesday, so the first Monday is 6 April.",
         [ARR, "1 April 2026 = Wednesday ⇒ Mondays on 6, 13, 20, 27 April"],
         why_others_wrong="4 May is Manas's holiday and 6 July Rachit's; 2 April is a Thursday.", seconds=80)
ans = next(p for p in P if first_mon[M3[p]] == dt.date(2026, 5, 4))
puzzle_q(sid, MON, DB_, "Intermediate", "Whose holiday falls on 4 May 2026?", ans, ["Vrinda", "Rachit", "Ankit"],
         "Comparing dates within months", "April's and May's first Mondays fall on the 6th and the 4th. Manas's date "
         "is the earlier one, so Manas takes 4 May.", [ARR], seconds=70)
gap = (first_mon[M3["Vrinda"]] - first_mon[M3["Kanchan"]]).days
assert gap == 35
puzzle_q(sid, MON, DB_, "Intermediate", "How many days after Kanchan's holiday is Vrinda's holiday?", f"{gap} days",
         ["28 days", "42 days", "31 days"], "Both are Mondays, so the gap is a multiple of 7",
         "Kanchan's holiday is 2 March and Vrinda's 6 April. From 2 March to 2 April is 31 days, and 4 more days reach "
         f"6 April: {gap} days (five weeks, as expected for two Mondays).",
         [ARR, "2 March → 2 April = 31 days; → 6 April = 35 days"],
         natural=lambda t: int(t.split()[0]), seconds=70)
same = [p for p in P if p != "Rachit" and day(M3[p]) == day(M3["Rachit"])]
assert same == ["Vrinda"]
puzzle_q(sid, MON, DB_, "Intermediate", "Whose holiday falls on the same date of the month as Rachit's holiday?",
         same[0], ["Gopi", "Manas", "Ankit"], "Same day-of-month in different months",
         "Rachit's holiday is 6 July. The only other first Monday on the 6th is 6 April, Vrinda's.", [ARR],
         seconds=60)

# ---- M4 Advanced (standalone): year-based ages
P = ["Kedar", "Mira", "Sanjay", "Vasu", "Yogini"]
YRS = [1978, 1984, 1990, 2002, 2005]
age = lambda y: 2026 - y
conds = [("Kedar is exactly twice as old as Vasu.", ("Kedar", "Vasu"), lambda k, v_: age(k) == 2 * age(v_)),
         ("Only two of the five are older than Mira.", tuple(P), lambda *y: sum(1 for x in y if x < y[1]) == 2),
         ("Yogini was born in an earlier year than Kedar.", ("Yogini", "Kedar"), lambda y_, k: y_ < k)]
M4 = unique(P, {p: YRS for p in P}, conds, [P])
assert M4 == {"Kedar": 1984, "Mira": 1990, "Sanjay": 2002, "Vasu": 2005, "Yogini": 1978}
ans = age(M4["Mira"]) + age(M4["Sanjay"])
assert ans == 60
mcq(MON, YB_, "Advanced",
    "Five persons Kedar, Mira, Sanjay, Vasu and Yogini were born in five different years among 1978, 1984, 1990, 2002 "
    "and 2005. Ages are counted in completed years on their birthdays in 2026.\n" + bullets(conds) +
    "\n\nWhat is the sum of the ages of Mira and Sanjay in 2026?", str(ans), ["57", "66", "72"],
    "Ages from birth years, then ratio clues",
    "Ages in 2026: 48, 42, 36, 24 and 21. Mira has exactly two older persons, so she is 36 (born 1990). 'Twice as old' "
    "pairs: 48 and 24, or 42 and 21. Yogini is older than Kedar, so Kedar cannot be 48: Kedar 42, Vasu 21, and then "
    "Yogini 48 and Sanjay 24. Mira + Sanjay = 36 + 24 = 60.",
    ["Ages: 1978 → 48, 1984 → 42, 1990 → 36, 2002 → 24, 2005 → 21", "Two older than Mira ⇒ Mira 36",
     "Kedar = 2 × Vasu: (48, 24) or (42, 21); Yogini older than Kedar ⇒ Kedar 42, Vasu 21",
     "Yogini 48, Sanjay 24 ⇒ 36 + 24 = 60"],
    why_others_wrong="57 uses Vasu's age (21) for Sanjay; 66 uses Kedar's 42 with Sanjay; 72 doubles Mira's age.",
    natural=int, seconds=100, verified_by=BRUTE)

# ---- M5 Advanced (standalone): six trips in a non-leap year, with month lengths
P = ["Arun", "Bimal", "Garima", "Jeet", "Nalini", "Tejas"]
conds = [("Bimal is the only one of the six who travels in a month that has fewer than 30 days.", tuple(P),
          lambda *m: MDAYS[m[1]] < 30 and all(MDAYS[x] >= 30 for i, x in enumerate(m) if i != 1)),
         ("Exactly two months lie between Bimal's month and Garima's month.", ("Bimal", "Garima"),
          lambda b, g: abs(b - g) == 3),
         ("Arun travels in a month that has 30 days, and Tejas in the month immediately after Arun's.",
          ("Arun", "Tejas"), lambda a, t: MDAYS[a] == 30 and t == a + 1),
         ("Jeet travels in the last month of the year.", ("Jeet",), lambda j: j == 12),
         ("Nalini travels after Tejas but before Jeet, in a month that has 30 days.", ("Nalini", "Tejas", "Jeet"),
          lambda n, t, j: t < n < j and MDAYS[n] == 30),
         ("Garima travels before Arun, and Arun's and Nalini's months are exactly three months apart.",
          ("Garima", "Arun", "Nalini"), lambda g, a, n: g < a and n - a == 3)]
M5 = unique(P, {p: range(1, 13) for p in P}, conds, [P])
assert M5 == {"Arun": 6, "Bimal": 2, "Garima": 5, "Jeet": 12, "Nalini": 9, "Tejas": 7}
empty = [m for m in range(M5["Garima"] + 1, M5["Jeet"]) if m not in M5.values()]
assert empty == [8, 10, 11]
mcq(MON, MB_, "Advanced",
    "Six persons Arun, Bimal, Garima, Jeet, Nalini and Tejas each take one trip in the same year (not a leap year), "
    "in six different months.\n" + bullets(conds) +
    "\n\nIn how many of the months between Garima's month and Jeet's month does none of the six travel?",
    num_word(len(empty)), ["Two", "Four", "Six"], "Month lengths as clues",
    "Only February has fewer than 30 days, so Bimal = February and Garima (two months between) = May. Jeet = December. "
    "Arun is in a 30-day month (April, June, September or November) after May, with Tejas in the next month; Nalini is "
    "in a 30-day month after Tejas and before December, three months after Arun. June → Tejas July → Nalini September "
    "works; September would need Nalini in December (Jeet's month), and November would put Tejas in December, Jeet's "
    "month. So Arun June, Tejas July, Nalini September. The months between May and December are June to November; "
    "nobody travels in August, October and November: three months.",
    ["Bimal February ⇒ Garima May; Jeet December", "Arun 30-day month after May, Tejas next, Nalini = Arun + 3 "
     "(30 days, before December) ⇒ Arun June, Tejas July, Nalini September",
     "June–November: trips in June, July, September", "Empty: August, October, November ⇒ three"],
    why_others_wrong="Six counts every month between; Two and Four miscount the empty months.", natural=by_num,
    seconds=120, verified_by=BRUTE)

# ================================================================================================ PUZZLES (OTHER)
OTH = "Puzzles (Other)"
DSG, CMP, DAY = "Designation", "Comparison and ordering", "Day-based"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# ---- O1 Basic set: six friends and the number of stamps each collected (values fixed by arithmetic)
st = {"Pari": 42, "Ela": 18, "Sohail": 60}
st["Kush"] = st["Pari"] - 9
st["Gaurik"] = st["Kush"] - 6
st["Indrani"] = (st["Pari"] + st["Sohail"]) // 2
assert (st["Pari"] + st["Sohail"]) % 2 == 0 and len(set(st.values())) == 6
ORD = sorted(st, key=st.get, reverse=True)
assert ORD == ["Sohail", "Indrani", "Pari", "Kush", "Gaurik", "Ela"] and min(st.values()) == st["Ela"]
ARR = "Most to fewest: " + ", ".join(f"{p} {st[p]}" for p in ORD)
sid = stimulus("puzzle", "Six friends and their stamp collections",
               "Six friends Ela, Gaurik, Indrani, Kush, Pari and Sohail have collected different numbers of stamps.\n\n"
               "- Pari has 42 stamps, which is 9 more than Kush has.\n- Gaurik has 6 stamps fewer than Kush.\n"
               "- Sohail has 60 stamps.\n- Indrani's number of stamps is exactly midway between Pari's and Sohail's.\n"
               "- Ela has the fewest stamps, 18.", None,
               "Step 1: Kush = 42 − 9 = 33; Gaurik = 33 − 6 = 27.\nStep 2: Indrani = (42 + 60) ÷ 2 = 51.\n"
               "Step 3: Order from most to fewest: Sohail 60, Indrani 51, Pari 42, Kush 33, Gaurik 27, Ela 18.")
OQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    OTH, CMP, "Basic", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
OQ("Who has the third highest number of stamps?", ORD[2], ["Indrani", "Kush", "Sohail"], "Compute, then rank",
   "Sohail (60) and Indrani (51) have more stamps than Pari (42), so Pari is third.", [ARR], seconds=40)
ans = st["Indrani"] + st["Gaurik"]
assert ans == 78
OQ("How many stamps do Indrani and Gaurik have together?", str(ans), ["84", "69", "93"],
   "Values from the clues", "Indrani = 51 and Gaurik = 27, so together they have 78.",
   ["Indrani = (42 + 60) ÷ 2 = 51", "Gaurik = 33 − 6 = 27", "51 + 27 = 78"],
   why_others_wrong="84 uses Kush's 33 for Gaurik; 69 uses Ela's 18; 93 uses Pari's 42.",
   natural=int, seconds=45)
cnt = sum(1 for v in st.values() if v > 30)
assert cnt == 4
OQ("How many of the six friends have more than 30 stamps?", num_word(cnt), ["Three", "Five", "Two"],
   "Count after computing every value", "Sohail 60, Indrani 51, Pari 42 and Kush 33 are above 30; Gaurik (27) and Ela "
   "(18) are not.", [ARR], natural=by_num, seconds=40)

# ---- O2 Basic (standalone): six gym visits from Monday to Saturday
P = ["Abha", "Bittu", "Chinu", "Dinky", "Eva", "Firoz"]
conds = [("Chinu visits on Wednesday.", ("Chinu",), lambda c: c == 2),
         ("Eva visits two days after Chinu.", ("Eva", "Chinu"), lambda e, c: e == c + 2),
         ("Firoz visits on a day after Eva.", ("Firoz", "Eva"), lambda f, e: f > e),
         ("Abha visits on the day immediately before Bittu.", ("Abha", "Bittu"), lambda a, b: a == b - 1)]
O2 = unique(P, {p: range(6) for p in P}, conds, [P])
ans = next(p for p in P if O2[p] == 3)
assert ans == "Dinky" and O2 == {"Abha": 0, "Bittu": 1, "Chinu": 2, "Dinky": 3, "Eva": 4, "Firoz": 5}
mcq(OTH, DAY, "Basic",
    "Six persons Abha, Bittu, Chinu, Dinky, Eva and Firoz visit a gym on six different days from Monday to Saturday of "
    "the same week, one person per day.\n" + bullets(conds) + "\n\nWho visits on Thursday?", ans,
    ["Bittu", "Eva", "Firoz"], "Fixed day, then consecutive-day pairs",
    "Chinu = Wednesday and Eva = Friday. Firoz comes after Eva: Saturday. Monday, Tuesday and Thursday remain; Abha and "
    "Bittu need two consecutive days, which only Monday–Tuesday provides. So Dinky visits on Thursday.",
    ["Chinu Wednesday ⇒ Eva Friday ⇒ Firoz Saturday", "Abha–Bittu consecutive ⇒ Monday, Tuesday",
     "Thursday ⇒ Dinky"], why_others_wrong="Bittu visits on Tuesday, Eva on Friday and Firoz on Saturday.",
    seconds=40, verified_by=BRUTE)

# ---- O3 Intermediate (standalone): five officers, five posts, five departments (rank 1 = most senior)
P = ["Haresh", "Lipi", "Nitara", "Ozair", "Rajni"]
POSTS = ["General Manager", "Deputy General Manager", "Assistant General Manager", "Chief Manager",
         "Senior Manager"]
DEP = ["Audit", "Credit", "HR", "IT", "Treasury"]
D_ = ["d" + p for p in P]
VV = P + D_
IXV = {v: i for i, v in enumerate(VV)}
rk_dep = lambda v, d: next(v[IXV[p]] for p in P if v[IXV["d" + p]] == d)
conds = [("Lipi is senior to exactly three of the others.", ("Lipi",), lambda l: l == 2),
         ("The officer in Treasury is immediately junior to Lipi.", tuple(VV),
          lambda *v: rk_dep(v, "Treasury") == v[IXV["Lipi"]] + 1),
         ("Ozair works in HR and is junior to the officer in Treasury, but Ozair is not the most junior.", tuple(VV),
          lambda *v: v[IXV["dOzair"]] == "HR" and v[IXV["Ozair"]] > rk_dep(v, "Treasury") and v[IXV["Ozair"]] != 5),
         ("Haresh is senior to Rajni but junior to Nitara.", ("Haresh", "Rajni", "Nitara"),
          lambda h, r, n: n < h < r),
         ("The officer in IT is the most junior.", tuple(VV), lambda *v: rk_dep(v, "IT") == 5),
         ("Nitara does not work in Audit.", ("dNitara",), lambda d: d != "Audit")]
O3 = unique(VV, {p: range(1, 6) for p in P} | {d: DEP for d in D_}, conds, [P, D_])
assert {p: (O3[p], O3["d" + p]) for p in P} == {"Haresh": (3, "Treasury"), "Lipi": (2, "Audit"),
                                               "Nitara": (1, "Credit"), "Ozair": (4, "HR"), "Rajni": (5, "IT")}
mcq(OTH, DSG, "Intermediate",
    "Five officers Haresh, Lipi, Nitara, Ozair and Rajni of a bank hold five different posts. In decreasing order of "
    "seniority the posts are: " + ", ".join(POSTS) + ". Each officer works in a different department among Audit, "
    "Credit, HR, IT and Treasury.\n" + bullets(conds) + "\n\nIn which department does the Deputy General Manager "
    "work?", "Audit", ["Treasury", "Credit", "HR"], "Seniority ranks plus departments",
    "Lipi is senior to three, so she is second: the Deputy General Manager. Treasury is third. Ozair (HR) is below "
    "Treasury and not last: fourth. Ranks 1, 3 and 5 remain for Nitara > Haresh > Rajni, in that order. So Haresh is "
    "third (Treasury) and Rajni fifth (IT). Lipi and Nitara share Audit and Credit; Nitara is not in Audit, so Lipi, "
    "the Deputy General Manager, works in Audit.",
    ["Lipi 2nd (DGM); Treasury 3rd", "Ozair (HR) 4th", "Nitara 1st, Haresh 3rd (Treasury), Rajni 5th (IT)",
     "Nitara not Audit ⇒ Nitara Credit, Lipi Audit"],
    why_others_wrong="Treasury belongs to Haresh (AGM), Credit to Nitara (GM) and HR to Ozair (Chief Manager).",
    seconds=80, verified_by=BRUTE)

# ---- O4 Intermediate (standalone): eight lectures on Monday–Thursday of two consecutive weeks
SUBJ = ["Botany", "Civics", "Drawing", "Ethics", "Finance", "Geology", "Hindi", "Music"]
SLOT = [(w, d) for w in (1, 2) for d in range(4)]
sl = lambda i: f"{DAYS[SLOT[i][1]]} of week {SLOT[i][0]}"
conds = [("Geology is on Tuesday of the second week.", ("Geology",), lambda g: g == 5),
         ("Exactly three lectures are held between Geology and Ethics.", ("Geology", "Ethics"),
          lambda g, e: abs(g - e) == 4),
         ("Botany is held on the lecture day immediately after Ethics.", ("Botany", "Ethics"), lambda b, e: b == e + 1),
         ("Music is held on a Thursday, before Geology.", ("Music", "Geology"),
          lambda m, g: SLOT[m][1] == 3 and m < g),
         ("Civics is held on the lecture day immediately after Music.", ("Civics", "Music"), lambda c, m: c == m + 1),
         ("Drawing is the last lecture, and Hindi is held before Finance.", ("Drawing", "Hindi", "Finance"),
          lambda d, h, f: d == 7 and h < f)]
O4 = unique(SUBJ, {s: range(8) for s in SUBJ}, conds, [SUBJ])
at = {v: k for k, v in O4.items()}
assert [at[i] for i in range(8)] == ["Hindi", "Ethics", "Botany", "Music", "Civics", "Geology", "Finance", "Drawing"]
mcq(OTH, DAY, "Intermediate",
    "Eight lectures — Botany, Civics, Drawing, Ethics, Finance, Geology, Hindi and Music — are held one per day on "
    "Monday, Tuesday, Wednesday and Thursday of two consecutive weeks (eight lecture days in all; there are no "
    "lectures on other days).\n" + bullets(conds) + "\n\nWhich lecture is held on Wednesday of the second week?",
    at[6], ["Geology", "Drawing", "Hindi"], "Counting only lecture days",
    "Number the lecture days 1 to 8 (week 1 Monday = 1, …, week 2 Thursday = 8). Geology = 6. Ethics is four days "
    "away: day 2 (day 10 does not exist), and Botany = 3. Music is on a Thursday before day 6: day 4; Civics = 5 (the "
    "next lecture day, Monday of week 2). Drawing = 8. Days 1 and 7 remain; Hindi comes before Finance, so Hindi = 1 "
    "and Finance = 7, which is Wednesday of week 2.",
    ["Geology 6 ⇒ Ethics 2 ⇒ Botany 3", "Music Thursday before 6 ⇒ 4; Civics 5", "Drawing 8",
     "Hindi 1, Finance 7 = Wednesday of week 2"],
    why_others_wrong="Geology is on Tuesday and Drawing on Thursday of week 2; Hindi is on Monday of week 1.",
    seconds=75, verified_by=BRUTE)

# ---- O5 Advanced set: seven cooks, seven days, seven dishes (Monday = 0)
P = ["Aakriti", "Devesh", "Gulnaz", "Ishir", "Kamya", "Lakshit", "Mohini"]
DSH = ["Biryani", "Dosa", "Idli", "Khichdi", "Paratha", "Poha", "Upma"]
H_ = ["h" + p for p in P]
VV = P + H_
IXV = {v: i for i, v in enumerate(VV)}
d_dish = lambda v, h: next(v[IXV[p]] for p in P if v[IXV["h" + p]] == h)
conds = [
    ("Aakriti cooks on Thursday, and she cooks Biryani.", ("Aakriti", "hAakriti"),
     lambda a, h: a == 3 and h == "Biryani"),
    ("Only two persons cook between Aakriti and the person who cooks Poha.", tuple(VV),
     lambda *v: abs(v[IXV["Aakriti"]] - d_dish(v, "Poha")) == 3),
    ("Ishir cooks Poha, on a day before Aakriti's day.", ("Ishir", "hIshir", "Aakriti"),
     lambda i, h, a: h == "Poha" and i < a),
    ("Kamya cooks on the day immediately after Devesh, and Devesh cooks on neither Tuesday nor Friday.",
     ("Kamya", "Devesh"), lambda k, d: k == d + 1 and d not in (1, 4)),
    ("Lakshit cooks on a day after Aakriti's day, and Gulnaz cooks on a day before Mohini's day.",
     ("Lakshit", "Aakriti", "Gulnaz", "Mohini"), lambda l, a, g, m: l > a and g < m),
    ("Kamya cooks Khichdi, and the person who cooks Paratha cooks on Saturday.", tuple(VV),
     lambda *v: v[IXV["hKamya"]] == "Khichdi" and d_dish(v, "Paratha") == 5),
    ("The person who cooks Dosa cooks on the day immediately before the person who cooks Upma.", tuple(VV),
     lambda *v: d_dish(v, "Dosa") == d_dish(v, "Upma") - 1),
]
O5 = unique(VV, {p: range(7) for p in P} | {h: DSH for h in H_}, conds, [P, H_])
at = {O5[p]: p for p in P}
dish = {p: O5["h" + p] for p in P}
assert [(at[i], dish[at[i]]) for i in range(7)] == [
    ("Ishir", "Poha"), ("Gulnaz", "Dosa"), ("Mohini", "Upma"), ("Aakriti", "Biryani"), ("Lakshit", "Idli"),
    ("Devesh", "Paratha"), ("Kamya", "Khichdi")]
ARR = "; ".join(f"{DAYS[i]} {at[i]} ({dish[at[i]]})" for i in range(7))
sid = stimulus("puzzle", "A week of cooks and dishes",
               "Seven persons Aakriti, Devesh, Gulnaz, Ishir, Kamya, Lakshit and Mohini each cook a meal at a community "
               "kitchen on a different day of the same week, from Monday to Sunday. Each cooks a different dish among "
               "Biryani, Dosa, Idli, Khichdi, Paratha, Poha and Upma.", conds,
               "Step 1: Aakriti = Thursday (Biryani). Poha is three days away: Monday or Sunday; Ishir cooks Poha "
               "before Thursday, so Ishir = Monday.\n"
               "Step 2: Devesh and Kamya are on consecutive days. The free days are Tuesday, Wednesday, Friday, Saturday "
               "and Sunday, so the pair is Tue–Wed, Fri–Sat or Sat–Sun; Devesh is on neither Tuesday nor Friday, so "
               "Devesh = Saturday and Kamya = Sunday.\n"
               "Step 3: Tuesday, Wednesday and Friday remain. Lakshit is after Thursday: Friday. Gulnaz is before "
               "Mohini: Gulnaz Tuesday, Mohini Wednesday.\n"
               "Step 4: Kamya cooks Khichdi and Devesh (Saturday) Paratha. Dosa, Idli and Upma remain for Gulnaz "
               "(Tue), Mohini (Wed) and Lakshit (Fri); Dosa is the day before Upma, so Gulnaz Dosa, Mohini Upma and "
               "Lakshit Idli.\n\n" + table(["Day", "Cook", "Dish"], [(DAYS[i], at[i], dish[at[i]]) for i in range(7)]))
ans = next(p for p in P if dish[p] == "Upma")
puzzle_q(sid, OTH, DAY, "Advanced", "Who cooks Upma?", ans, ["Gulnaz", "Lakshit", "Devesh"],
         "A consecutive-day pair of dishes", "Dosa, Idli and Upma are left for Tuesday, Wednesday and Friday; Dosa is the "
         "day before Upma, which only Tuesday–Wednesday allows. Mohini (Wednesday) cooks Upma.", [ARR], seconds=100)
ans = DAYS[O5[next(p for p in P if dish[p] == "Idli")]]
puzzle_q(sid, OTH, DAY, "Advanced", "On which day is Idli cooked?", ans, ["Tuesday", "Wednesday", "Saturday"],
         "The last dish left", "Lakshit cooks on Friday, and after Dosa and Upma go to Tuesday and Wednesday, Idli is "
         "left for him.", [ARR], seconds=95)
cnt = abs(O5["Gulnaz"] - d_dish([O5[v] for v in VV], "Paratha")) - 1
assert cnt == 3
puzzle_q(sid, OTH, DAY, "Advanced", "How many persons cook between Gulnaz and the person who cooks Paratha?",
         num_word(cnt), ["Two", "Four", "One"], "Dish → day → count",
         "Paratha is cooked by Devesh on Saturday and Gulnaz cooks on Tuesday. Wednesday, Thursday and Friday lie "
         "between: three persons.", [ARR], natural=by_num, seconds=90)

# ---- O6 Advanced (standalone): heights fixed by sums and differences
h = {"Veer": 182, "Yash": 158}
h["Tinku"] = h["Veer"] - 7
# Sona = Rahi + 6 = (Wasu + 4) + 6 and Sona + Wasu = 334  =>  2·Wasu + 10 = 334
h["Wasu"] = (334 - 10) // 2
h["Rahi"] = h["Wasu"] + 4
h["Sona"] = h["Rahi"] + 6
assert h["Sona"] + h["Wasu"] == 334 and h["Wasu"] < h["Sona"] < h["Tinku"] and min(h.values()) == h["Yash"]
assert max(h.values()) == h["Veer"] and len(set(h.values())) == 6
O_ = sorted(h, key=h.get, reverse=True)
ans = h[O_[2]] - h[O_[-2]]
assert O_ == ["Veer", "Tinku", "Sona", "Rahi", "Wasu", "Yash"] and ans == 10
mcq(OTH, CMP, "Advanced",
    "Six persons Rahi, Sona, Tinku, Veer, Wasu and Yash have different heights.\n"
    "- Veer is the tallest, at 182 cm, and Tinku is 7 cm shorter than Veer.\n"
    "- Yash is the shortest, at 158 cm.\n- Sona is shorter than Tinku but taller than Wasu.\n"
    "- Rahi is 4 cm taller than Wasu, and Sona is 6 cm taller than Rahi.\n"
    "- The heights of Sona and Wasu add up to 334 cm.\n\n"
    "What is the difference between the heights of the third tallest and the second shortest persons?",
    f"{ans} cm", ["6 cm", "14 cm", "4 cm"], "Turn the chain of differences into one equation",
    "Sona = Rahi + 6 = Wasu + 10. With Sona + Wasu = 334: 2 × Wasu + 10 = 334, so Wasu = 162, Rahi = 166 and Sona = "
    "172. Tinku = 175. Tallest to shortest: Veer 182, Tinku 175, Sona 172, Rahi 166, Wasu 162, Yash 158. Third tallest "
    "(Sona, 172) minus second shortest (Wasu, 162) = 10 cm.",
    ["Sona = Wasu + 4 + 6 = Wasu + 10", "2W + 10 = 334 ⇒ W = 162; Rahi 166; Sona 172; Tinku 175",
     "Order: Veer, Tinku, Sona, Rahi, Wasu, Yash", "172 − 162 = 10 cm"],
    why_others_wrong="6 cm is Sona − Rahi; 14 cm is Yash's gap to Sona; 4 cm is Rahi − Wasu.",
    natural=lambda t: int(t.split()[0]), seconds=100, verified_by=RECOMP)

# ---- O7 Advanced (standalone): two branches, three posts each
P = ["Bala", "Daman", "Joshna", "Pinky", "Ravi", "Swati"]
POS3 = ["Manager", "Deputy Manager", "Officer"]
SPOTS = [(b, r) for b in ("North", "South") for r in range(3)]
conds = [("Joshna is a Manager, and Daman works in the same branch as Joshna.", ("Joshna", "Daman"),
          lambda j, d: j[1] == 0 and d[0] == j[0]),
         ("Pinky works in the South branch and holds the same post as Daman.", ("Pinky", "Daman"),
          lambda p, d: p[0] == "South" and p[1] == d[1]),
         ("Ravi is an Officer, and he does not work in Joshna's branch.", ("Ravi", "Joshna"),
          lambda r, j: r[1] == 2 and r[0] != j[0]),
         ("Swati holds a junior post to Daman's.", ("Swati", "Daman"), lambda s, d: s[1] > d[1])]
O7 = unique(P, {p: SPOTS for p in P}, conds, [P])
assert O7 == {"Bala": ("South", 0), "Daman": ("North", 1), "Joshna": ("North", 0), "Pinky": ("South", 1),
              "Ravi": ("South", 2), "Swati": ("North", 2)}
mcq(OTH, DSG, "Advanced",
    "A bank has two branches, North and South. Each branch has exactly three employees: a Manager, a Deputy Manager "
    "and an Officer (in decreasing order of seniority). The six employees are Bala, Daman, Joshna, Pinky, Ravi and "
    "Swati.\n" + bullets(conds) + "\n\nWho is the Manager of the South branch?", "Bala",
    ["Joshna", "Pinky", "Daman"], "Each post exists once per branch",
    "Daman and Pinky hold the same post, so they must be in different branches; Pinky is in South, so Daman (and "
    "therefore Joshna) is in North. Ravi is an Officer outside Joshna's branch: the South Officer. Pinky's post is "
    "Manager or Deputy Manager; Daman cannot be a Manager (Joshna is North's Manager), so both are Deputy Managers. "
    "Swati is junior to Daman: the North Officer. The only post left is South Manager: Bala.",
    ["Same post ⇒ different branches ⇒ Daman, Joshna in North", "Ravi = South Officer",
     "Daman not Manager ⇒ Daman and Pinky Deputy Managers", "Swati = North Officer ⇒ Bala = South Manager"],
    why_others_wrong="Joshna manages the North branch; Pinky and Daman are Deputy Managers.", seconds=90,
    verified_by=BRUTE)

# ================================================================================================ SYLLOGISM
TWO, FEW, POSS = "Two-statement", "Only a few / Only", "Possibility cases"


def N(*pairs):  # redefined: the seating sections reuse the name N for a seat count
    return {s_: (s_, p_) for s_, p_ in pairs}


# ---- Basic
syl_q("Basic", TWO, N(("spoon", "spoons"), ("fork", "forks"), ("knife", "knives")),
      [("all", "spoon", "fork"), ("no", "fork", "knife")],
      [("no", "spoon", "knife"), ("some", "knife", "fork")], ONLY_I,
      "All + No = No",
      "Every spoon lies inside forks, and forks and knives do not overlap, so no spoon can be a knife (I). Forks and "
      "knives never meet, so 'Some knives are forks' is false (II).",
      ["Spoons ⊂ forks; forks ∩ knives = ∅", "⇒ spoons ∩ knives = ∅: I follows", "II contradicts 'No fork is a knife'"],
      shortcut="All A are B + No B is C ⇒ No A is C.", seconds=30)
syl_q("Basic", TWO, N(("wolf", "wolves"), ("fox", "foxes"), ("jackal", "jackals")),
      [("some", "wolf", "fox"), ("all", "fox", "jackal")],
      [("all", "jackal", "wolf"), ("somenot", "wolf", "jackal")], NEITHER,
      "Some + All = Some (and nothing more)",
      "The wolves that are foxes are jackals, so some wolves are jackals — but that is not what either conclusion says. "
      "Jackals outside foxes may lie outside wolves, so I is not certain. The other wolves may or may not be jackals, so "
      "'Some wolves are not jackals' is not certain either (II).",
      ["Definite: Some wolves are jackals", "I (All jackals are wolves): jackals beyond foxes may not be wolves",
       "II: all wolves may be jackals ⇒ not certain"], seconds=35)
# ---- Intermediate
syl_q("Intermediate", FEW, N(("candle", "candles"), ("lantern", "lanterns"), ("torch", "torches")),
      [("onlyfew", "candle", "lantern"), ("all", "lantern", "torch")],
      [("some", "candle", "torch"), ("poss_all", "candle", "lantern")], ONLY_I,
      "'Only a few A are B' = some A are B and some A are not B",
      "Some candles are lanterns and every lantern is a torch, so some candles are torches (I). 'Only a few' also says "
      "some candles are not lanterns, so all candles being lanterns is impossible (II).",
      ["Candle ∩ lantern ⊂ torches ⇒ I follows", "Only a few ⇒ some candles are not lanterns ⇒ II impossible"],
      seconds=45)
syl_q("Intermediate", FEW, N(("hammer", "hammers"), ("nail", "nails"), ("screw", "screws")),
      [("onlyfew", "hammer", "nail"), ("no", "nail", "screw")],
      [("somenot", "hammer", "screw"), ("poss_all", "screw", "hammer")], BOTH,
      "A definite 'some not' plus an unblocked possibility",
      "The hammers that are nails cannot be screws, so some hammers are not screws (I). The screws may all lie in the "
      "part of hammers that is not nails; nothing forbids it, so II is possible.",
      ["Some hammers are nails; no nail is a screw ⇒ I follows",
       "Screws can sit inside hammers outside nails ⇒ II possible: follows"], seconds=50)
syl_q("Intermediate", POSS, N(("deer", "deer"), ("horse", "horses"), ("camel", "camels")),
      [("some", "deer", "horse"), ("no", "horse", "camel")],
      [("poss_all", "deer", "camel"), ("somenot", "camel", "horse")], ONLY_II,
      "A possibility fails when some members are definitely excluded",
      "The deer that are horses can never be camels, so 'all deer being camels' is impossible (I). Camels exist and none "
      "is a horse, so some camels are not horses (II).",
      ["Deer ∩ horses is non-empty and outside camels ⇒ I impossible", "No horse is a camel ⇒ II follows"],
      seconds=45)
syl_q("Intermediate", FEW, N(("banana", "bananas"), ("guava", "guavas"), ("papaya", "papayas")),
      [("only", "banana", "guava"), ("some", "guava", "papaya")],
      [("somenot", "papaya", "banana"), ("some", "papaya", "banana")], ONLY_II,
      "'Only bananas are guavas' = All guavas are bananas",
      "Every guava is a banana, so the papayas that are guavas are bananas: some papayas are bananas (II). The other "
      "papayas may or may not be bananas, so I is not certain.",
      ["Only bananas are guavas ⇒ guavas ⊂ bananas", "Guava ∩ papaya ⊂ bananas ⇒ II follows",
       "All papayas may be bananas ⇒ I not certain"],
      why="Reading 'Only bananas are guavas' as 'All bananas are guavas' would lose conclusion II.", seconds=50)
syl_q("Intermediate", TWO, N(("scarf", "scarves"), ("glove", "gloves"), ("sock", "socks")),
      [("some", "scarf", "glove"), ("no", "glove", "sock")],
      [("some", "scarf", "sock"), ("no", "scarf", "sock")], EITHER,
      "Some + No gives 'Some scarves are not socks' only; check the complementary pair",
      "The definite result is that some scarves (those that are gloves) are not socks. Whether any scarf is a sock is "
      "open, so neither I nor II is certain alone. But I and II are 'Some' and 'No' about the same two terms, so exactly "
      "one of them is true: either I or II follows.",
      ["Definite: Some scarves are not socks", "I and II each uncertain",
       "I and II form a complementary pair ⇒ Either I or II follows"],
      why="'Either' takes the place of 'Both' (four-option rule); 'Neither' ignores the complementary pair.",
      seconds=50)
syl_q("Intermediate", POSS, N(("train", "trains"), ("tram", "trams"), ("coach", "coaches"), ("cart", "carts")),
      [("all", "train", "tram"), ("onlyfew", "tram", "coach"), ("no", "coach", "cart")],
      [("somenot", "tram", "cart"), ("some", "train", "cart")], ONLY_I,
      "A 'some not' carried through a 'No' statement",
      "Some trams are coaches and no coach is a cart, so those trams are not carts (I). Trains lie inside trams, but "
      "they may all be in the coach part, away from carts, so 'Some trains are carts' is not certain (II).",
      ["Tram ∩ coach is non-empty and outside carts ⇒ I follows",
       "Trains may avoid carts entirely ⇒ II possible but not certain"], seconds=55)
syl_q("Intermediate", POSS, N(("singer", "singers"), ("dancer", "dancers"), ("actor", "actors")),
      [("all", "singer", "dancer"), ("somenot", "actor", "dancer")],
      [("somenot", "actor", "singer"), ("poss_all", "dancer", "actor")], BOTH,
      "'Some not' passes down to a subset",
      "Some actors lie outside dancers, and every singer is a dancer, so those actors are not singers (I). The actors "
      "outside dancers do not stop every dancer from being an actor, so II is possible.",
      ["Actors outside dancers are outside singers ⇒ I follows",
       "Dancers ⊂ actors is consistent with some actors outside dancers ⇒ II follows"], seconds=50)
syl_q("Intermediate", FEW, N(("crayon", "crayons"), ("brush", "brushes"), ("paint", "paints")),
      [("onlyfew", "crayon", "brush"), ("onlyfew", "brush", "paint")],
      [("somenot", "brush", "paint"), ("some", "crayon", "paint")], ONLY_I,
      "Two 'only a few' statements link nothing about the end terms",
      "'Only a few brushes are paints' says directly that some brushes are not paints (I). The crayons that are brushes "
      "may all fall in the non-paint part, so 'Some crayons are paints' is not certain (II).",
      ["Only a few brushes are paints ⇒ Some brushes are not paints: I follows",
       "Crayon ∩ brush may avoid paints ⇒ II not certain"], seconds=50)
syl_q("Intermediate", TWO, N(("bell", "bells"), ("whistle", "whistles"), ("horn", "horns")),
      [("some", "bell", "whistle"), ("somenot", "whistle", "horn")],
      [("somenot", "bell", "horn"), ("all", "horn", "whistle")], NEITHER,
      "'Some not' in the second statement gives no conclusion",
      "Bells are tied to whistles only by 'some', and 'Some whistles are not horns' says nothing about which whistles. "
      "All bells may be horns, so I is not certain; horns outside whistles are possible, so II is not certain.",
      ["Some + Some not ⇒ no definite bell–horn relation", "Nothing forces horns inside whistles"], seconds=45)
# ---- Advanced
syl_q("Advanced", POSS, N(("ticket", "tickets"), ("pass", "passes"), ("receipt", "receipts"), ("coupon", "coupons")),
      [("onlyfew", "ticket", "pass"), ("all", "pass", "receipt"), ("no", "receipt", "coupon")],
      [("somenot", "ticket", "coupon"), ("poss_all", "coupon", "ticket")], BOTH,
      "Four terms: a definite exclusion and a free region",
      "Some tickets are passes, passes lie inside receipts and receipts never meet coupons, so those tickets are not "
      "coupons (I). The tickets that are not passes may lie outside receipts, where coupons can be, so all coupons "
      "could be tickets (II).",
      ["Ticket ∩ pass ⊂ receipts, which exclude coupons ⇒ I follows",
       "Coupons can sit in tickets outside passes and receipts ⇒ II possible: follows"], seconds=65)
syl_q("Advanced", POSS, N(("oak", "oaks"), ("pine", "pines"), ("maple", "maples"), ("cedar", "cedars")),
      [("some", "oak", "pine"), ("only", "pine", "maple"), ("no", "maple", "cedar")],
      [("poss_all", "pine", "cedar"), ("somenot", "pine", "cedar")], ONLY_II,
      "'Only pines are maples' = All maples are pines",
      "Every maple is a pine and no maple is a cedar, so the pines that are maples are not cedars: some pines are not "
      "cedars (II), and for the same reason all pines can never be cedars (I fails).",
      ["Maples ⊂ pines; maples ∩ cedars = ∅", "⇒ Some pines are not cedars: II follows",
       "⇒ All pines being cedars is impossible: I fails"],
      why="Reading 'Only pines are maples' as 'All pines are maples' still gives II but hides why I fails.",
      seconds=65)

# ================================================================================================ INEQUALITY
DIRECT, CODED = "Direct inequality", "Coded inequality"
# Inequality items word their four fixed options as "... is true" (same meaning as the syllogism options)
IO4 = {ONLY_I: "Only conclusion I is true", ONLY_II: "Only conclusion II is true",
       NEITHER: "Neither conclusion I nor II is true", BOTH: "Both conclusions I and II are true",
       EITHER: "Either conclusion I or II is true"}


def ineq_q(diff, sub, statement_text, chains, conclusions, concl_text, expected, explanation, steps, shortcut=None,
           why=None, seconds=40, concept="Reading a combined inequality chain", stimulus=None):
    f1, f2, either = ineq_eval(chains, conclusions)
    got = EITHER if either else BOTH if f1 and f2 else ONLY_I if f1 else ONLY_II if f2 else NEITHER
    assert got == expected, (chains, conclusions, got)
    text = (statement_text + "\n\nConclusions:\nI. " + concl_text[0] + "\nII. " + concl_text[1])
    return fixed(INQ, sub, diff, text, [IO4[x] for x in conclusion_options(expected)], IO4[expected], concept,
                 explanation, steps, shortcut=shortcut, why_others_wrong=why, seconds=seconds, verified_by=EXHAUST,
                 stimulus=stimulus)


def ineq_q3(*a, **kw):
    """ineq_q with a cross-check: the verdict must not change when every variable gets a wider value range."""
    chains, conclusions = a[3], a[4]
    assert ineq_eval(chains, conclusions) == ineq_eval(
        chains, conclusions, dom=len({x for c in chains for r in parse_chain(c) for x in (r[0], r[2])}) + 3)
    return ineq_q(*a, **kw)


def chain_q(chain, conc):
    return ("Statement: " + chain + "\n\nConclusions:", [chain], [parse_chain(c)[0] for c in conc], conc)


def chain_text(chain, conc):
    s, ch, cc, ct = chain_q(chain, conc)
    return "Statement: " + chain, ch, cc, ct


# ---- Basic: one combined chain
s, ch, cc, ct = chain_text("J ≥ K > L ≤ M = N < O", ["J > L", "O > M"])
ineq_q3("Basic", DIRECT, s, ch, cc, ct, BOTH,
        "J ≥ K > L gives J > L. M = N < O gives O > M. Both follow.",
        ["I: J ≥ K > L → J > L, true", "II: M = N < O → O > M, true"], seconds=30)
s, ch, cc, ct = chain_text("D = E < F ≥ G > H ≤ I", ["D < G", "F > H"])
ineq_q3("Basic", DIRECT, s, ch, cc, ct, ONLY_II,
        "D = E < F ≥ G: the signs change direction at F, so D and G cannot be compared. F ≥ G > H gives F > H.",
        ["I: D = E < F ≥ G: reversal at F → no relation", "II: F ≥ G > H → F > H, true"], seconds=30)
s, ch, cc, ct = chain_text("W < X ≤ Y = Z ≥ A > B", ["W < Z", "A < X"])
ineq_q3("Basic", DIRECT, s, ch, cc, ct, ONLY_I,
        "W < X ≤ Y = Z gives W < Z. X and A lie on opposite sides of the turn at Z (X ≤ Y = Z ≥ A), so A < X is not "
        "certain.", ["I: W < X ≤ Y = Z → W < Z, true", "II: X ≤ … = Z ≥ A: reversal → no relation"], seconds=30)
s, ch, cc, ct = chain_text("G ≤ H < I > J ≥ K = L", ["G < J", "K ≥ H"])
ineq_q3("Basic", DIRECT, s, ch, cc, ct, NEITHER,
        "Both conclusions compare a term left of I with a term right of I, and the direction turns at I (H < I > J). "
        "Neither can be established.",
        ["I: G ≤ H < I > J: reversal at I → no relation", "II: H < I > J ≥ K: reversal at I → no relation"],
        seconds=30)
s, ch, cc, ct = chain_text("T ≥ U = V ≥ W < X > Y", ["T > W", "T = W"])
ineq_q3("Basic", DIRECT, s, ch, cc, ct, EITHER,
        "T ≥ U = V ≥ W gives only T ≥ W. T > W and T = W are each uncertain, but together they make up T ≥ W, so one "
        "of them must be true: either I or II follows.",
        ["T ≥ U = V ≥ W → T ≥ W (no strict sign)", "I alone and II alone are not certain",
         "I or II = T ≥ W ⇒ Either I or II follows"],
        why="'Either' takes the place of 'Both' (four-option rule); T > W and T = W cannot both hold.", seconds=35)
s, ch, cc, ct = chain_text("M > N = O ≥ P < Q < R", ["N > P", "R > P"])
ineq_q3("Basic", DIRECT, s, ch, cc, ct, ONLY_II,
        "N = O ≥ P gives only N ≥ P, so N > P is not certain. P < Q < R gives R > P.",
        ["I: N = O ≥ P → N ≥ P only → not certain", "II: P < Q < R → R > P, true"],
        why="A '≥' path never proves a strict '>'.", seconds=30)
s, ch, cc, ct = chain_text("A ≤ B = C < D ≥ E > F", ["A < D", "E < C"])
s = "Five statements are given: A ≤ B, B = C, C < D, D ≥ E and E > F. Treat all of them as true."
ineq_q3("Basic", DIRECT, s, ch, cc, ct, ONLY_I,
        "A ≤ B = C < D gives A < D. C and E lie on opposite sides of the turn at D, so E < C is not certain.",
        ["I: A ≤ B = C < D → A < D, true", "II: C < D ≥ E: reversal at D → no relation"], seconds=30)

# ---- Intermediate: coded
CODE_M = {"☼": ">", "♪": "<", "☾": "=", "♫": "≥", "✿": "≤"}
CODE_M_TXT = ("In the following question, the symbols ☼, ♪, ☾, ♫ and ✿ are used with these meanings:\n"
              "'A ☼ B' means 'A is greater than B'; 'A ♪ B' means 'A is less than B'; 'A ☾ B' means 'A is equal to "
              "B'; 'A ♫ B' means 'A is not less than B'; 'A ✿ B' means 'A is not greater than B'.\n"
              "Assuming the statements to be true, find which of the conclusions I and II is/are definitely true.")
CC_ = "Decoding worded symbols, then reading the chain"
SID_M = stimulus("passage", "Five worded inequality symbols", CODE_M_TXT, None,
                 "Decode: ☼ means >, ♪ means <, ☾ means =, ♫ means ≥ and ✿ means ≤. Rewrite every statement with the "
                 "ordinary signs, join them into one chain, and test each conclusion along the chain.")


def coded_m(stmts, concs):
    return ("Statements: " + ", ".join(stmts), [decode(x, CODE_M) for x in stmts],
            [parse_chain(decode(c, CODE_M))[0] for c in concs], concs)
s, ch, cc, ct = coded_m(["A ♫ B", "B ☼ C", "C ☾ D", "E ♪ D"], ["A ☼ D", "E ♪ B"])
ineq_q3("Intermediate", CODED, s, ch, cc, ct, BOTH,
        "Decoded: A ≥ B > C = D > E. So A > D (I) and E < B (II): both follow.",
        ["Decode: ☼ >, ♪ <, ☾ =, ♫ ≥, ✿ ≤", "A ≥ B, B > C, C = D, E < D ⇒ A ≥ B > C = D > E",
         "I: A > D, true", "II: E < B, true"], concept=CC_, stimulus=SID_M, seconds=55)
s, ch, cc, ct = coded_m(["F ✿ G", "G ♪ H", "I ♫ H", "I ☾ J"], ["J ☼ F", "G ♫ I"])
ineq_q3("Intermediate", CODED, s, ch, cc, ct, ONLY_I,
        "Decoded: F ≤ G < H ≤ I = J. So J > F (I follows). G < I, so 'G ≥ I' is false (II).",
        ["Decode: F ≤ G, G < H, I ≥ H, I = J", "Chain: F ≤ G < H ≤ I = J", "I: J ☼ F means J > F: true",
         "II: G ♫ I means G ≥ I: false"], concept=CC_, stimulus=SID_M, seconds=55)
s, ch, cc, ct = coded_m(["K ☼ L", "M ♫ L", "M ✿ N", "O ♪ N"], ["K ☼ M", "N ♫ L"])
ineq_q3("Intermediate", CODED, s, ch, cc, ct, ONLY_II,
        "Decoded: K > L ≤ M ≤ N > O. K and M lie on opposite sides of the turn at L, so K > M is not certain. "
        "L ≤ M ≤ N gives N ≥ L.",
        ["Decode: K > L, M ≥ L, M ≤ N, O < N", "Chain: K > L ≤ M ≤ N > O", "I: K > M: reversal at L → not certain",
         "II: N ≥ L: true"], concept=CC_, stimulus=SID_M, seconds=55)
s, ch, cc, ct = coded_m(["P ☾ Q", "Q ♫ R", "S ♪ R", "S ♫ T"], ["Q ☼ R", "Q ☾ R"])
ineq_q3("Intermediate", CODED, s, ch, cc, ct, EITHER,
        "Decoded: P = Q ≥ R > S ≥ T. Q ≥ R is given, so Q > R and Q = R are each uncertain, but one of them must be "
        "true: either I or II follows.",
        ["Decode: P = Q, Q ≥ R, S < R, S ≥ T", "Q ≥ R ⇒ (Q > R) or (Q = R)", "Either I or II follows"],
        why="'Either' replaces 'Both' (four-option rule).", concept=CC_, stimulus=SID_M, seconds=55)
s, ch, cc, ct = coded_m(["U ♪ V", "V ✿ W", "X ☼ W", "X ✿ Y", "Z ♪ Y"], ["Z ♪ W", "U ☾ V"])
ineq_q3("Intermediate", CODED, s, ch, cc, ct, NEITHER,
        "Decoded: U < V ≤ W < X ≤ Y > Z. W and Z lie on opposite sides of the turn at Y, so Z < W is not certain. "
        "U < V makes U = V false.",
        ["Decode: U < V, V ≤ W, X > W, X ≤ Y, Z < Y", "Chain: U < V ≤ W < X ≤ Y > Z",
         "I: Z < W: reversal at Y → not certain", "II: U = V: false (U < V)"], concept=CC_, stimulus=SID_M, seconds=60)

# ---- Advanced
s, ch, cc, ct = direct(["R > S", "T ≤ S", "U ≥ R", "V < T", "W = V"], ["U > W", "R > U"])
ineq_q3("Advanced", DIRECT, s, ch, cc, ct, ONLY_I,
        "Combined: U ≥ R > S ≥ T > V = W. From U down to W every sign points the same way with strict signs on the "
        "path, so U > W. R > U contradicts U ≥ R.",
        ["Rewrite: U ≥ R, R > S, S ≥ T, T > V, V = W", "Chain: U ≥ R > S ≥ T > V = W", "I: U > W: true",
         "II: R > U: false (U ≥ R)"], concept="Combining five statements into one chain", seconds=60)
CODE_N = {"⊳": ">", "⊲": "<", "≡": "=", "⊵": "≥", "⊴": "≤"}
CODE_N_TXT = ("Here 'P ⊳ Q' stands for 'P is greater than Q', 'P ⊲ Q' for 'P is smaller than Q', 'P ≡ Q' for 'P and Q "
              "are equal', 'P ⊵ Q' for 'P is either greater than or equal to Q', and 'P ⊴ Q' for 'P is either smaller "
              "than or equal to Q'. Take the five statements as true and test the two conclusions.")
s, ch, cc, ct = coded(CODE_N_TXT, CODE_N, ["B ⊵ C", "C ≡ D", "D ⊳ E", "F ⊴ E", "F ⊵ G"], ["B ⊳ G", "C ⊳ F"])
ineq_q3("Advanced", CODED, s, ch, cc, ct, BOTH,
        "Decoded: B ≥ C = D > E ≥ F ≥ G. B > G (one strict sign on the path) and C > F (C = D > E ≥ F).",
        ["Decode: ⊳ >, ⊲ <, ≡ =, ⊵ ≥, ⊴ ≤", "B ≥ C, C = D, D > E, F ≤ E, F ≥ G", "Chain: B ≥ C = D > E ≥ F ≥ G", "I: B > G: true",
         "II: C > F: true"], concept="Decoding a five-statement chain", seconds=65)
CH = ["G > H ≥ I", "J ≤ I", "K = J", "L > K"]
OPTS = [("J", ">", "G"), ("H", ">", "K"), ("L", ">", "I"), ("L", "≥", "H")]
rels = [r for c in CH for r in parse_chain(c)]
vs = sorted({x for a_, _, b_ in rels for x in (a_, b_)})
sats = [dict(zip(vs, vals)) for vals in itertools.product(range(len(vs) + 2), repeat=len(vs))
        if all(REL[o](dict(zip(vs, vals))[a_], dict(zip(vs, vals))[b_]) for a_, o, b_ in rels)]
never = [c for c in OPTS if not any(REL[c[1]](v[c[0]], v[c[2]]) for v in sats)]
always = [c for c in OPTS if all(REL[c[1]](v[c[0]], v[c[2]]) for v in sats)]
assert never == [OPTS[0]] and always == []
mcq(INQ, DIRECT, "Advanced",
    "Statement: " + "; ".join(CH) + "\n\nWhich of the following conclusions is definitely FALSE?",
    " ".join(OPTS[0]), [" ".join(c) for c in OPTS[1:]], "Definitely false = contradicted by the chain in every case",
    "Combined: G > H ≥ I ≥ J = K < L. So G > J always, which makes 'J > G' false in every case. H ≥ I ≥ J = K gives "
    "only H ≥ K, so H > K may or may not hold. L is above K but cannot be compared with I or H, so L > I and L ≥ H "
    "may be true or false.",
    ["Chain: G > H ≥ I ≥ J = K < L", "J > G: G > J always ⇒ definitely false",
     "H > K: only H ≥ K ⇒ not determined", "L > I, L ≥ H: L joins the chain only at K ⇒ not determined"],
    why_others_wrong="The other three are each possible but not certain; 'definitely false' needs a relation that the "
                     "chain rules out in every case.", seconds=75, verified_by=EXHAUST)
# ---- coding helpers reused from tools/batch_003/reasoning.py
VOW = set("AEIOU")
LC, SW, NC = "Letter coding", "Sentence/word coding", "Number coding"


def letter_rules():
    """A library of simple letter-coding rules used to make sure that no other rule fits the examples of an
    'inferred rule' question and gives a different answer."""
    R = {}
    opp = lambda w: "".join(AL[26 - pos(c)] for c in w)
    half = lambda w: w[len(w) // 2:] + w[:len(w) // 2]
    halfrev = lambda w: w[:len(w) // 2][::-1] + w[len(w) // 2:][::-1]
    pairswap = lambda w: "".join(w[i + 1] + w[i] for i in range(0, len(w) - 1, 2)) + (w[-1] if len(w) % 2 else "")
    oddeven = lambda w: w[0::2] + w[1::2]
    for k in range(-6, 7):
        for nm, f_ in (("id", lambda w: w), ("rev", lambda w: w[::-1]), ("opp", opp), ("half", half),
                       ("halfrev", halfrev), ("pairswap", pairswap), ("oddeven", oddeven)):
            R[f"{nm}+{k}"] = lambda w, f_=f_, k=k: shift(f_(w), k)
            R[f"{k}+{nm}"] = lambda w, f_=f_, k=k: f_(shift(w, k))
    for a in range(-3, 4):
        for b in range(-3, 4):
            R[f"alt{a},{b}"] = lambda w, a=a, b=b: "".join(shift(c, a if i % 2 == 0 else b) for i, c in enumerate(w))
            R[f"vc{a},{b}"] = lambda w, a=a, b=b: "".join(shift(c, a if c in VOW else b) for c in w)
    for sgn in (1, -1):
        R[f"posL{sgn}"] = lambda w, s=sgn: "".join(shift(c, s * (i + 1)) for i, c in enumerate(w))
        R[f"posR{sgn}"] = lambda w, s=sgn: "".join(shift(c, s * (len(w) - i)) for i, c in enumerate(w))
        R[f"rev+posL{sgn}"] = lambda w, s=sgn: "".join(shift(c, s * (i + 1)) for i, c in enumerate(w[::-1]))
        R[f"opp+posL{sgn}"] = lambda w, s=sgn: "".join(shift(c, s * (i + 1)) for i, c in enumerate(opp(w)))
    return R


LRULES = letter_rules()


def inferred(examples, target, expected, rules=LRULES):
    """Every rule in the library that reproduces all the examples must give the expected answer for the target."""
    fits = {n: f_(target) for n, f_ in rules.items() if all(f_(a) == b for a, b in examples)}
    assert fits and set(fits.values()) == {expected}, (examples, target, fits)
    return expected

NRULES = {"sum": lambda w: sum(pos(c) for c in w), "sum×len": lambda w: sum(pos(c) for c in w) * len(w),
          "sum+len": lambda w: sum(pos(c) for c in w) + len(w), "product": lambda w: __import__("math").prod(
              pos(c) for c in w), "reverse-sum": lambda w: sum(27 - pos(c) for c in w),
          "weighted-left": lambda w: sum(pos(c) * (i + 1) for i, c in enumerate(w)),
          "weighted-right": lambda w: sum(pos(c) * (len(w) - i) for i, c in enumerate(w)),
          "ends-product": lambda w: pos(w[0]) * pos(w[-1]), "consonants-vowels": lambda w: sum(
              pos(c) if c not in VOW else -pos(c) for c in w), "sum-len": lambda w: sum(pos(c) for c in w) - len(w)}

# ================================================================================================ BLOOD RELATIONS
DRB, CDB, FPZ = "Direct relation", "Coded blood relation", "Family puzzle"

# ---- Basic (standalone)
F = Family().add("C", "M").add("D", "F").marry("C", "D").add("A", "F", "C", "D").add("B", "M", "C", "D")
ans = F.rel("A", "D")
assert ans == "daughter"
mcq(BLD, DRB, "Basic", "A is the sister of B. B is the son of C. D is the wife of C. How is A related to D?",
    cap(ans), ["Sister", "Mother", "Niece"], "A sibling of a child is also a child of the same parents",
    "B is the son of C, and D is C's wife, so D is B's mother. A is B's sister, so A is also D's child: her daughter.",
    ["B is C's son; D is C's wife ⇒ D is B's mother", "A is B's sister ⇒ A is D's daughter"],
    why_others_wrong="Sister and mother would put A in D's generation or above; niece needs a sibling of D.",
    seconds=30, verified_by=RECOMP)
F = Family().add("Gf", "M").add("Gm", "F").marry("Gf", "Gm").add("Father", "M", "Gf", "Gm").add("Uncle", "M", "Gf", "Gm")
F.add("Mother", "F").marry("Father", "Mother").add("Arif", "M", "Father", "Mother")
assert F.siblings("Father") == {"Uncle"} and F.rel("Gf", "Arif") == "grandfather"
mcq(BLD, DRB, "Basic",
    "Pointing to a man in a photograph, Arif said, \"This man's son is my father's only brother.\" How is the man in "
    "the photograph related to Arif?", "Grandfather", ["Father", "Uncle", "Great-grandfather"],
    "The father of one's father's brother",
    "Arif's father's only brother is Arif's paternal uncle. The man in the photograph is the father of that uncle, and "
    "brothers share a father, so he is also the father of Arif's father: Arif's grandfather.",
    ["My father's only brother = Arif's uncle", "The man is that uncle's father",
     "The uncle's father is also Arif's father's father ⇒ grandfather"],
    why_others_wrong="Father would make the man's son Arif's brother; uncle is the man's son, not the man; "
                     "great-grandfather skips a generation.", seconds=35, verified_by=RECOMP)
F = Family().add("R", "M").add("Rw", "F").marry("R", "Rw").add("P", "M", "R", "Rw").add("Q", "F", "R", "Rw")
F.add("S", "F", "Gx", "Gy").add("Gx", "M").add("Gy", "F").marry("Gx", "Gy").add("R2", "M")
F.par["R"] = ("Gx", "Gy")
F.add("Sh", "M").marry("S", "Sh").add("T", "M", "Sh", "S")
assert F.rel("T", "Q") == "cousin"
mcq(BLD, DRB, "Basic",
    "P is the brother of Q. R is the father of P. S is the sister of R. T is the son of S. How is T related to Q?",
    "Cousin", ["Brother", "Nephew", "Uncle"], "Children of siblings are cousins",
    "R is the father of P and therefore also of Q (P and Q are siblings). S is R's sister, so she is Q's aunt, and her "
    "son T is Q's cousin.",
    ["R is the father of P and Q", "S is R's sister ⇒ Q's aunt", "S's son T ⇒ Q's cousin"],
    why_others_wrong="Brother would need the same parents as Q; nephew and uncle are one generation off.", seconds=35,
    verified_by=RECOMP)
F = Family().add("Mh", "M").add("M", "F").marry("Mh", "M").add("O", "F", "Mh", "M").add("N", "M").marry("N", "O")
assert F.rel("M", "N") == "mother-in-law"
ans = F.rel("O", "M")
assert ans == "daughter"
mcq(BLD, DRB, "Basic", "M is the mother-in-law of N, and N is the husband of O. N has only one wife. How is O related "
    "to M?", cap(ans), ["Daughter-in-law", "Sister", "Mother"], "A man's mother-in-law is his wife's mother",
    "M is N's mother-in-law, so M is the mother of N's wife. N's wife is O, so O is M's daughter.",
    ["Mother-in-law of a husband = mother of his wife", "N's wife = O ⇒ M is O's mother ⇒ O is M's daughter"],
    why_others_wrong="Daughter-in-law would be the wife of M's son; here M is the mother of N's wife.", seconds=30,
    verified_by=RECOMP)
F = Family().add("Gopal", "M").add("Gw", "F").marry("Gopal", "Gw").add("Mohan", "M", "Gopal", "Gw")
F.add("Lata", "F", "Gopal", "Gw").add("Rekha", "F").marry("Mohan", "Rekha").add("Lh", "M").marry("Lata", "Lh")
F.add("Ishan", "M", "Lh", "Lata")
ans = F.rel("Rekha", "Ishan")
assert ans == "aunt"
mcq(BLD, DRB, "Basic",
    "Rekha is the wife of Mohan. Mohan's father Gopal has only two children, Mohan and Lata. Ishan is Lata's son. How "
    "is Rekha related to Ishan?", "Aunt (wife of his mother's brother)", ["Mother", "Sister", "Grandmother"],
    "The wife of a maternal uncle",
    "Mohan and Lata are siblings, so Mohan is the brother of Ishan's mother: his maternal uncle. Rekha, Mohan's wife, "
    "is therefore Ishan's aunt.",
    ["Mohan and Lata are Gopal's two children ⇒ siblings", "Lata is Ishan's mother ⇒ Mohan is his maternal uncle",
     "Uncle's wife ⇒ aunt"], why_others_wrong="Ishan's mother is Lata; Rekha is in his mother's generation, so she is "
                                               "neither his sister nor his grandmother.", seconds=35,
    verified_by=RECOMP)

# ---- Intermediate (standalone): coded
CODE_Q = {"⊞": "son", "⊟": "wife", "⊠": "brother", "⊡": "mother"}
F = Family().add("Ph", "M").add("P", "F").marry("Ph", "P").add("Q", "M", "Ph", "P").add("R", "F", "Ph", "P")
F.add("S", "M").marry("S", "R")
F.check(coded_facts("P ⊡ Q ⊠ R ⊟ S", CODE_Q))
ans = F.rel("P", "S")
assert ans == "mother-in-law"
mcq(BLD, CDB, "Intermediate",
    "In a certain code:\n'A ⊞ B' means 'A is the son of B';\n'A ⊟ B' means 'A is the wife of B';\n'A ⊠ B' means "
    "'A is the brother of B';\n'A ⊡ B' means 'A is the mother of B'.\n\nIf 'P ⊡ Q ⊠ R ⊟ S', how is P related to S?",
    cap(ans), ["Mother", "Sister-in-law", "Grandmother"], "Decode left to right and keep track of generations",
    "P is Q's mother; Q is R's brother, so P is R's mother too. R is S's wife, so P is the mother of S's wife: S's "
    "mother-in-law.",
    ["P ⊡ Q: P is Q's mother", "Q ⊠ R: R is Q's sibling ⇒ P is R's mother", "R ⊟ S: R is S's wife",
     "Mother of one's wife ⇒ mother-in-law"],
    why_others_wrong="Mother is P's relation to R, not to S; sister-in-law and grandmother put P in the wrong "
                     "generation.", seconds=55, verified_by=RECOMP)

# ---- Advanced set: a three-generation family (relations read off an explicit tree)
F = Family().add("Raghav", "M").add("Sushila", "F").marry("Raghav", "Sushila")
F.add("Tarun", "M", "Raghav", "Sushila").add("Uma", "F", "Raghav", "Sushila").add("Vimla", "F").marry("Tarun", "Vimla")
F.add("Yash", "M").marry("Uma", "Yash").add("Kunal", "M", "Tarun", "Vimla").add("Ria", "F", "Yash", "Uma")
F.check([("Yash", "son-in-law", "Raghav"), ("Ria", "granddaughter", "Sushila"), ("Kunal", "grandson", "Sushila")])
FT = ("A family has eight members: Kunal, Raghav, Ria, Sushila, Tarun, Uma, Vimla and Yash. There are three married "
      "couples.\n\n- Raghav and Sushila are married to each other and have exactly two children, Tarun and Uma.\n"
      "- Vimla is Tarun's wife, and Kunal is their only child.\n- Yash is the son-in-law of Raghav.\n"
      "- Ria is the daughter of Yash.\n- Kunal and Ria are the only grandchildren of Sushila.")
sid = stimulus("puzzle", "A three-generation family with a son-in-law", FT, None,
               "Step 1: Raghav's children are Tarun and Uma. A son-in-law is the husband of one's daughter, and Raghav's "
               "only daughter is Uma, so Yash is Uma's husband.\n"
               "Step 2: Ria is Yash's daughter and a grandchild of Sushila, so her mother is Uma.\n"
               "Step 3: Tree: Raghav + Sushila → Tarun (+ Vimla) → Kunal; Uma (+ Yash) → Ria. Females: Sushila, Uma, "
               "Vimla and Ria.")
BQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    BLD, FPZ, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
ans = F.rel("Vimla", "Ria")
assert ans == "aunt"
BQ("How is Vimla related to Ria?", cap(ans), ["Mother", "Sister-in-law", "Grandmother"],
   "Wife of a parent's brother",
   "Ria's mother is Uma, and Uma's brother is Tarun. Vimla is Tarun's wife, so she is the wife of Ria's maternal "
   "uncle: Ria's aunt.", ["Yash = Uma's husband (Raghav's only daughter) ⇒ Ria's mother = Uma",
                          "Tarun = Uma's brother; Vimla = Tarun's wife ⇒ aunt"],
   why_others_wrong="Uma is Ria's mother; Vimla is Uma's sister-in-law, not Ria's; Sushila is Ria's grandmother.",
   seconds=80)
ans = F.rel("Yash", "Tarun")
assert ans == "brother-in-law"
BQ("How is Yash related to Tarun?", cap(ans), ["Brother", "Son-in-law", "Cousin"], "Sister's husband",
   "Yash is married to Uma, Tarun's sister, so Yash is Tarun's brother-in-law.",
   ["Son-in-law of Raghav ⇒ husband of Raghav's daughter Uma", "Uma is Tarun's sister ⇒ brother-in-law"],
   why_others_wrong="Yash is Raghav's son-in-law, not Tarun's; he shares no parent with Tarun.", seconds=75)
ans = F.rel("Sushila", "Yash")
assert ans == "mother-in-law"
BQ("How is Sushila related to Yash?", cap(ans), ["Mother", "Grandmother", "Aunt"], "Wife's mother",
   "Yash's wife is Uma, and Sushila is Uma's mother, so Sushila is Yash's mother-in-law.",
   ["Yash's wife = Uma", "Uma's mother = Sushila ⇒ mother-in-law"], seconds=70)

# ---- Advanced (standalone)
CODE_Z = {"∧": "father", "∨": "daughter", "≈": "husband", "∞": "sister", "∝": "son"}
F = Family().add("M", "M").add("N", "F").marry("M", "N").add("L", "M", "M", "N")
F.add("Nf", "M").add("Nm", "F").marry("Nf", "Nm").par["N"] = ("Nf", "Nm")
F.add("O", "F", "Nf", "Nm")
F.check(coded_facts("L ∝ M ≈ N ∞ O", CODE_Z))
ans = F.rel("L", "O")
assert ans == "nephew"
mcq(BLD, CDB, "Advanced",
    "In a certain code:\n'A ∧ B' means 'A is the father of B';\n'A ∨ B' means 'A is the daughter of B';\n'A ≈ B' "
    "means 'A is the husband of B';\n'A ∞ B' means 'A is the sister of B';\n'A ∝ B' means 'A is the son of B'.\n\n"
    "If 'L ∝ M ≈ N ∞ O', how is L related to O?", cap(ans), ["Son", "Brother", "Cousin"],
    "Mother's sister's relation to the child",
    "L is M's son and M is N's husband, so N is L's mother. N is O's sister, so O is L's maternal aunt, and L (a son) "
    "is O's nephew.",
    ["L ∝ M: L is M's son (male)", "M ≈ N: N is M's wife ⇒ L's mother", "N ∞ O: O is the sister of L's mother",
     "Son of one's sister ⇒ nephew"],
    why_others_wrong="Son would make O a parent of L; brother and cousin put L in the wrong generation or branch.",
    seconds=70, verified_by=RECOMP)
F = Family().add("Kh", "M").add("Kamla", "F").marry("Kh", "Kamla").add("Ramesh", "M", "Kh", "Kamla")
F.add("Sunita", "F").marry("Ramesh", "Sunita").add("Mohit", "M", "Ramesh", "Sunita")
F.add("Pallavi", "F", "Ramesh", "Sunita").add("Ajay", "M").marry("Pallavi", "Ajay")
assert [c for c in F.children("Kamla") if F.g[c] == "M"] == ["Ramesh"]
assert F.rel("Kamla", "Sunita") == "mother-in-law"
ans = F.rel("Ajay", "Mohit")
assert ans == "brother-in-law"
mcq(BLD, FPZ, "Advanced",
    "Kamla is the mother-in-law of Mohit's mother. Kamla has only one son, Ramesh, who has only one wife, Sunita. "
    "Sunita's daughter Pallavi, whose father is Ramesh, is married to Ajay. How is Ajay related to Mohit?", cap(ans),
    ["Brother", "Uncle", "Son-in-law"], "Identify the parents first, then the sibling's spouse",
    "Kamla's daughter-in-law must be the wife of her only son, Ramesh: Sunita. So Mohit's mother is Sunita and his "
    "father Ramesh. Pallavi is the daughter of Ramesh and Sunita, so she is Mohit's sister, and her husband Ajay is "
    "Mohit's brother-in-law.",
    ["Mother-in-law of Mohit's mother ⇒ Mohit's mother married Kamla's son", "Only son Ramesh, only wife Sunita ⇒ "
     "Mohit's parents are Ramesh and Sunita", "Pallavi = Mohit's sister ⇒ her husband is his brother-in-law"],
    why_others_wrong="Ajay is Ramesh's son-in-law, not Mohit's; he is neither Mohit's brother nor his uncle.",
    seconds=80, verified_by=RECOMP)

# ================================================================================================ DIRECTION SENSE
DD, PP, SH_ = "Distance and direction", "Point-to-point", "Shadow-based"
x, y = walk("N", [(None, 12), ("L", 5), ("L", 7)])
assert (x, y) == (-5, 5)
mcq(DIR, DD, "Basic",
    "Sameer walks 12 m towards the north. He then turns left and walks 5 m, and then turns left again and walks 7 m. "
    "How far is he now from his starting point, and in which direction?", f"{dist(x, y)} m, {compass(x, y)}",
    ["5√2 m, North-East", "13 m, North-West", "5 m, West"], "Net displacement",
    "Left from north is west, and left from west is south. He ends 5 m west and 12 − 7 = 5 m north of the start: "
    "√(25 + 25) = 5√2 m, towards the north-west.",
    ["12 m north → (0, 12)", "Left = west; 5 m → (−5, 12)", "Left = south; 7 m → (−5, 5)", "√(5² + 5²) = 5√2 m, NW"],
    why_others_wrong="North-East takes the first left as east; 13 m uses 12 and 5 as the legs; 5 m, West forgets the "
                     "remaining northward 5 m.", seconds=40, verified_by=RECOMP)
B_ = (0, 0)
A_ = (0, -4)
C_ = (A_[0] - 4, A_[1])
D_ = (C_[0], C_[1] + 6)
assert D_ == (-4, 2)
mcq(DIR, PP, "Basic",
    "Point A is 4 m south of point B. Point C is 4 m west of point A. Point D is 6 m north of point C. In which "
    "direction is point D with respect to point B?", compass(D_[0] - B_[0], D_[1] - B_[1]),
    ["South-West", "North-East", "West"], "Place every point on a grid",
    "Take B at (0, 0). A = (0, −4), C = (−4, −4) and D = (−4, 2). D is 4 m west and 2 m north of B: north-west.",
    ["B (0, 0) → A (0, −4) → C (−4, −4) → D (−4, 2)", "D − B = (−4, +2) ⇒ North-West"],
    why_others_wrong="South-West ignores that D is 2 m north of B; West ignores the north component.", seconds=40,
    verified_by=RECOMP)
ANG = {"N": 0, "NE": 45, "E": 90, "SE": 135, "S": 180, "SW": 225, "W": 270, "NW": 315}
ANAME = {"N": "North", "NE": "North-East", "E": "East", "SE": "South-East", "S": "South", "SW": "South-West",
         "W": "West", "NW": "North-West"}
fin = (ANG["NE"] + 225 - 90) % 360
ans = ANAME[next(k for k, v in ANG.items() if v == fin)]
assert ans == "South"
mcq(DIR, DD, "Basic",
    "A girl is facing north-east. She turns 225° clockwise and then 90° anticlockwise. Which direction is she facing "
    "now?", ans, ["West", "North", "South-West"], "Net turn = clockwise − anticlockwise",
    "The net turn is 225° − 90° = 135° clockwise. Starting from north-east (45°), 45° + 135° = 180°: south.",
    ["Net turn: 225° clockwise − 90° = 135° clockwise", "North-East = 45° ⇒ 45° + 135° = 180° = South"],
    why_others_wrong="West stops after the first turn; North turns the wrong way; South-West adds only 180°.",
    seconds=40, verified_by=RECOMP)

# ---- Intermediate set: a drone's route between landmarks
PTS = {"T": (0, 0)}
route = [("Q", "N", 9), ("R", "E", 12), ("S", "S", 14), ("U", "W", 20), ("V", "N", 11)]
cur = PTS["T"]
for nm_, d_, k_ in route:
    cur = (cur[0] + VEC[d_][0] * k_, cur[1] + VEC[d_][1] * k_)
    PTS[nm_] = cur
assert PTS == {"T": (0, 0), "Q": (0, 9), "R": (12, 9), "S": (12, -5), "U": (-8, -5), "V": (-8, 6)}
ARR = "Coordinates (east, north) in km with T at (0, 0): " + ", ".join(f"{k} {v}" for k, v in PTS.items())
sid = stimulus("data_table", "A drone's route between six landmarks",
               "A drone starts at landmark T and flies in straight lines: 9 km north to landmark Q, then 12 km east to "
               "landmark R, then 14 km south to landmark S, then 20 km west to landmark U, and finally 11 km north to "
               "landmark V, where it lands.", None,
               "Put T at (0, 0), with east and north positive.\nQ = (0, 9); R = (12, 9); S = (12, 9 − 14) = (12, −5); "
               "U = (12 − 20, −5) = (−8, −5); V = (−8, −5 + 11) = (−8, 6).")
DQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    DIR, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
dx, dy = PTS["R"][0] - PTS["T"][0], PTS["R"][1] - PTS["T"][1]
DQ(PP, "What is the straight-line distance between T and R, and in which direction is R from T?",
   f"{dist(dx, dy)} km, {compass(dx, dy)}", ["21 km, North-East", "15 km, North-West", "12 km, East"],
   "A 9-12-15 right triangle", "R is 12 km east and 9 km north of T: √(144 + 81) = 15 km, towards the north-east.",
   [ARR, "R − T = (12, 9)", "√(12² + 9²) = 15 km; east and north ⇒ North-East"],
   why_others_wrong="21 km adds the two legs; North-West swaps east for west; 12 km, East ignores the 9 km north.",
   seconds=55)
dx, dy = PTS["V"]
DQ(DD, "How far is the drone's landing point V from its starting point T, and in which direction?",
   f"{dist(dx, dy)} km, {compass(dx, dy)}", ["10 km, North-East", "14 km, North-West", "√164 km, South-West"],
   "Net displacement of the whole route",
   "V = (−8, 6): 8 km west and 6 km north of T, so √(64 + 36) = 10 km towards the north-west.",
   [ARR, "V − T = (−8, 6)", "√(8² + 6²) = 10 km; west and north ⇒ North-West"],
   why_others_wrong="North-East takes the 20 km leg as east; 14 km adds 8 and 6; South-West uses the point U.",
   seconds=60)
dx, dy = PTS["S"][0] - PTS["U"][0], PTS["S"][1] - PTS["U"][1]
DQ(PP, "In which direction is S with respect to U?", compass(dx, dy), ["West", "North-East", "South-East"],
   "Same north coordinate ⇒ a pure east–west direction",
   "S = (12, −5) and U = (−8, −5) are on the same east–west line, with S 20 km to the east of U.",
   [ARR, "S − U = (20, 0) ⇒ East"], why_others_wrong="West is U's direction from S; the other two need a north or "
                                                    "south difference, which is zero.", seconds=50)
dists = {k: (v[0] ** 2 + v[1] ** 2) ** 0.5 for k, v in PTS.items() if k != "T"}
near_ = min(dists, key=dists.get)
assert near_ == "Q" and sorted(dists.values())[1] > dists["Q"]
DQ(PP, "Which landmark (other than T) is nearest to T in a straight line?", near_, ["U", "V", "S"],
   "Compare straight-line distances",
   "Distances from T: Q 9 km, U √89 ≈ 9.4 km, V 10 km, S 13 km, R 15 km. Q is the nearest.",
   [ARR, "Q 9; U √(64 + 25) = √89; V 10; S √(144 + 25) = 13; R 15"],
   why_others_wrong="U is a close second (√89 ≈ 9.43 km); V is 10 km and S 13 km away.", seconds=65)

# ---- Intermediate (standalone)
# shadow: afternoon sun in the west, so shadows point east; walking towards the tip of a shadow = facing east
face = "E"
face2 = turn(face, "L")
assert NAME[face2] == "North"
mcq(DIR, SH_, "Intermediate",
    "At about 4 pm on a sunny day, Kriti stood beside a lamp post and then walked straight towards the tip of the post's "
    "shadow. After reaching the tip, she turned to her left and kept walking. In which direction was she walking "
    "then?", NAME[face2], ["South", "West", "East"], "Afternoon shadows point east",
    "In the afternoon the sun is in the west, so shadows point east. Walking towards the tip of the shadow means "
    "walking east. A left turn from east is north.",
    ["Afternoon: sun in the west ⇒ shadow towards the east", "Walking to the tip ⇒ facing east",
     "Left of east ⇒ north"], why_others_wrong="South is a right turn from east; West would be walking towards the "
                                                "sun; East ignores the turn.", seconds=50, verified_by=RECOMP)
x, y = walk("S", [(None, 6), ("R", 4), ("R", 11), ("L", 8)])
assert (x, y) == (-12, 5)
mcq(DIR, DD, "Intermediate",
    "A cyclist rides 6 km towards the south, turns right and rides 4 km, turns right again and rides 11 km, and then "
    "turns left and rides 8 km. How far is the cyclist from the starting point, and in which direction?",
    f"{dist(x, y)} km, {compass(x, y)}", ["13 km, North-East", "17 km, South-West", "12 km, West"],
    "Track the facing direction after each turn",
    "Right from south is west; right from west is north; left from north is west. Net: west 4 + 8 = 12 km and north "
    "11 − 6 = 5 km. √(144 + 25) = 13 km, towards the north-west.",
    ["South 6 → (0, −6)", "Right ⇒ west 4 → (−4, −6)", "Right ⇒ north 11 → (−4, 5)", "Left ⇒ west 8 → (−12, 5)",
     "√(12² + 5²) = 13 km, North-West"],
    why_others_wrong="North-East flips the east–west part; 17 km adds 12 and 5; 12 km, West ignores the 5 km north.",
    seconds=70, verified_by=RECOMP)
# clock: the '3' points north, so the '12' points west, the '6' east, the '9' south
CLK = {3: "North", 12: "West", 6: "East", 9: "South"}
mcq(DIR, PP, "Intermediate",
    "A wall clock is laid flat on a table so that the hour hand points towards the north when the time is exactly 3 "
    "o'clock. At 7:30 the same day, in which direction does the minute hand point?", CLK[6],
    ["West", "South-West", "North"], "Rotate the whole dial with the given reference",
    "At 3 o'clock the hour hand points at the '3', so the '3' faces north. Going clockwise around the dial, '6' is a "
    "quarter-turn after '3', so it faces east ('12' faces west and '9' south). At 7:30 the minute hand points at the "
    "'6': east.",
    ["'3' → north", "Clockwise quarter-turns: '6' → east, '9' → south, '12' → west",
     "7:30 ⇒ minute hand at '6' ⇒ east"],
    why_others_wrong="West is where the '12' points; South-West would be between '9' and '12'; North is the '3'.",
    seconds=70, verified_by=RECOMP)
b_face = (ANG["NE"] + 180) % 360
b_new = (b_face + 90) % 360
ans = ANAME[next(k for k, v in ANG.items() if v == b_new)]
assert ans == "North-West"
mcq(DIR, DD, "Intermediate",
    "Anu and Babli stand back to back. Anu faces north-east. Babli then turns 90° clockwise. Which direction does "
    "Babli face now?", ans, ["South-East", "North-East", "South-West"], "Back to back = opposite directions",
    "Standing back to back, Babli faces the opposite of north-east: south-west (225°). A 90° clockwise turn gives "
    "225° + 90° = 315°: north-west.",
    ["Back to back ⇒ Babli faces south-west (225°)", "225° + 90° = 315° = North-West"],
    why_others_wrong="South-East is a 90° anticlockwise turn; North-East is Anu's direction; South-West ignores the "
                     "turn.", seconds=55, verified_by=RECOMP)

# ---- Advanced (standalone)
ravi = walk("N", [(None, 10), ("R", 6), ("R", 4)])
sita = walk("E", [(None, 6), ("L", 14), ("L", 15)])
assert ravi == (6, 6) and sita == (-9, 14)
dx, dy = sita[0] - ravi[0], sita[1] - ravi[1]
mcq(DIR, DD, "Advanced",
    "Ravi and Sita start from the same point X. Ravi walks 10 m north, turns right and walks 6 m, then turns right "
    "again and walks 4 m. Sita walks 6 m east, turns left and walks 14 m, then turns left again and walks 15 m. How far "
    "is Sita from Ravi now, and in which direction from him?", f"{dist(dx, dy)} m, {compass(dx, dy)}",
    ["17 m, South-East", "23 m, North-West", "15 m, North"], "Put both end points on one grid",
    "Ravi: north 10, east 6, south 4 ⇒ (6, 6). Sita: east 6, north 14, west 15 ⇒ (−9, 14). Sita is 15 m west and 8 m "
    "north of Ravi: √(225 + 64) = 17 m, towards the north-west.",
    ["Ravi: (0, 10) → (6, 10) → (6, 6)", "Sita: (6, 0) → (6, 14) → (−9, 14)", "Difference (−15, +8)",
     "√(15² + 8²) = 17 m, North-West"],
    why_others_wrong="South-East is Ravi's direction from Sita; 23 m adds 15 and 8; 15 m, North ignores the west part.",
    seconds=100, verified_by=RECOMP)
x, y = walk("E", [(None, 5), ("L", 12), ("L", 10)])
assert (x, y) == (-5, 12)
mcq(DIR, SH_, "Advanced",
    "At 7 am on a clear day, Neha starts from point A and walks 5 km straight towards the sun. She then turns left and "
    "walks 12 km, and then turns left again and walks 10 km. How far is she from A, and in which direction?",
    f"{dist(x, y)} km, {compass(x, y)}", ["13 km, North-East", "13 km, South-West", "17 km, North-West"],
    "Fix the first direction from the morning sun",
    "At 7 am the sun is in the east, so she first walks east 5 km. Left from east is north (12 km), and left from north "
    "is west (10 km). Net: 5 km west and 12 km north, so √(25 + 144) = 13 km, towards the north-west.",
    ["Morning sun ⇒ first leg east: (5, 0)", "Left ⇒ north 12: (5, 12)", "Left ⇒ west 10: (−5, 12)",
     "√(5² + 12²) = 13 km, North-West"],
    why_others_wrong="North-East forgets that the 10 km west leg overshoots the start; South-West reverses both "
                     "parts; 17 km adds 5 and 12.", seconds=90, verified_by=RECOMP)

# ================================================================================================ CODING-DECODING
alt = lambda w: "".join(shift(c, 1 if i % 2 == 0 else -1) for i, c in enumerate(w))
assert alt("WINTER") == "XHOSFQ"
ans = inferred([("WINTER", "XHOSFQ")], "SUMMER", alt("SUMMER"))
assert ans == "TTNLFQ"
mcq(COD, LC, "Basic", "In a certain code language, WINTER is written as XHOSFQ. How is SUMMER written in that code "
    "language?", ans, ["TVNNFS", "RTLLDQ", "TTNLFS"], "Alternate letters move forward and backward",
    "W+1 = X, I−1 = H, N+1 = O, T−1 = S, E+1 = F, R−1 = Q: letters in odd places move one step forward and letters in "
    "even places one step back. SUMMER: S+1 = T, U−1 = T, M+1 = N, M−1 = L, E+1 = F, R−1 = Q.",
    ["Check WINTER: +1, −1, +1, −1, +1, −1", f"SUMMER → {ans}"],
    why_others_wrong="TVNNFS moves every letter forward; RTLLDQ moves every letter back; TTNLFS moves the last letter "
                     "forward instead of back.", seconds=40, verified_by=RECOMP)
assert inferred([("ACE", 15), ("BED", 40)], "DEAF", 120, NRULES) == 120
mcq(COD, NC, "Basic", "In a certain code, ACE is written as 15 and BED is written as 40. How is DEAF written in that "
    "code?", "120", ["16", "24", "480"], "Product of the alphabet positions",
    "ACE: 1 × 3 × 5 = 15; BED: 2 × 5 × 4 = 40. DEAF: 4 × 5 × 1 × 6 = 120.",
    ["A 1, C 3, E 5 ⇒ 1 × 3 × 5 = 15 ✓", "B 2, E 5, D 4 ⇒ 40 ✓", "DEAF: 4 × 5 × 1 × 6 = 120"],
    why_others_wrong="16 is the sum of the positions; 24 leaves out E (4 × 1 × 6); 480 multiplies the "
                     "product by the number of letters.", natural=int, seconds=40, verified_by=RECOMP)
SS = [(["mango", "is", "sweet"], ["ta", "po", "ki"]), (["sweet", "ripe", "fruit"], ["ki", "lu", "ra"]),
      (["fruit", "is", "fresh"], ["ra", "po", "ne"])]
assert sentence_solve(SS, "mango") == {"ta"}
mcq(COD, SW, "Basic",
    "In a certain code language, 'mango is sweet' is written as 'ta po ki', 'sweet ripe fruit' is written as 'ki lu "
    "ra' and 'fruit is fresh' is written as 'ra po ne'. (The codes of the words in a sentence may be in any order.) "
    "What is the code for 'mango'?", "ta", ["po", "ki", "ne"], "Remove the codes of the shared words",
    "'is' appears in sentences 1 and 3, whose common code is po. 'sweet' appears in sentences 1 and 2, common code ki. "
    "Sentence 1 is 'mango is sweet' = 'ta po ki', so mango = ta.",
    ["is = po (sentences 1 & 3)", "sweet = ki (sentences 1 & 2)", "mango = remaining code of sentence 1 = ta"],
    why_others_wrong="po is 'is', ki is 'sweet' and ne is 'fresh'.", seconds=40, verified_by=RECOMP)
oprev = lambda w: "".join(AL[26 - pos(c)] for c in w)[::-1]
assert oprev("GARDEN") == "MVWIZT"
ans = inferred([("GARDEN", "MVWIZT")], "PLANET", oprev("PLANET"), LRULES | {"opp-then-reverse": oprev})
assert ans == "GVMZOK"
mcq(COD, LC, "Intermediate",
    "In a certain code, GARDEN is written as MVWIZT. How is PLANET written in that code?", ans,
    ["KOZMVG", "GVMZOL", "TENALP"], "Opposite letters, then reverse",
    "Replace each letter by its opposite (A↔Z, B↔Y, …): GARDEN → TZIWVM, which reversed is MVWIZT. PLANET → KOZMVG "
    f"→ reversed {ans}.", ["Opposites of GARDEN: T Z I W V M", "Reverse: MVWIZT ✓", "PLANET → K O Z M V G",
                           f"Reverse: {ans}"],
    why_others_wrong="KOZMVG skips the reversal; GVMZOL takes the opposite of P as L; TENALP only reverses the word.",
    seconds=55, verified_by=RECOMP)
psm = lambda n: "".join(str((int(d) - 1) % 10) for d in n[1] + n[0] + n[3] + n[2])
assert psm("5274") == "1436" and psm("8193") == "0728"
DR2 = {}
for k_ in range(-9, 10):
    for nm_, f_ in (("id", lambda n: n), ("rev", lambda n: n[::-1]), ("pairswap", lambda n: n[1] + n[0] + n[3] + n[2]),
                    ("halfswap", lambda n: n[2:] + n[:2]), ("ends", lambda n: n[3] + n[1:3] + n[0])):
        DR2[f"{nm_}{k_}"] = lambda n, f_=f_, k_=k_: "".join(str((int(d) + k_) % 10) for d in f_(n))
        DR2[f"{k_}-{nm_}"] = lambda n, f_=f_, k_=k_: "".join(str((k_ - int(d)) % 10) for d in f_(n))
ans = inferred([("5274", "1436"), ("8193", "0728")], "6385", psm("6385"), DR2)
assert ans == "2547"
mcq(COD, NC, "Advanced",
    "In a certain code, 5274 is written as 1436 and 8193 is written as 0728. How is 6385 written in that code?", ans,
    ["3658", "5274", "2548"], "Swap the digits in pairs, then subtract 1 from each digit",
    "5274: swap the 1st–2nd and 3rd–4th digits → 2547, then subtract 1 from every digit → 1436. 8193 → 1839 → 0728. "
    f"6385 → 3658 → {ans}.", ["Check: 5274 → 2547 → 1436; 8193 → 1839 → 0728", "6385 → 3658", f"−1 each → {ans}"],
    why_others_wrong="3658 stops after the swap; 5274 subtracts 1 without swapping; 2548 does not reduce the last "
                     "digit.", seconds=70, verified_by=RECOMP)
VW = set("AEIOU")
WRULES = {}
for mv_nm, mv in (("first-to-end", lambda w: w[1:] + w[0]), ("last-to-front", lambda w: w[-1] + w[:-1]),
                  ("reverse", lambda w: w[::-1]), ("none", lambda w: w)):
    for ct_nm, ct in (("vowels", lambda w: sum(c in VW for c in w)), ("consonants", lambda w: sum(c not in VW for c in w)),
                      ("length", len), ("half-length", lambda w: len(w) // 2)):
        WRULES[f"{mv_nm}+{ct_nm}"] = lambda w, mv=mv, ct=ct: mv(w) + str(ct(w))
wc = WRULES["first-to-end+vowels"]
assert wc("LOAN") == "OANL2" and wc("CREDIT") == "REDITC2"
ans = inferred([("LOAN", "OANL2"), ("CREDIT", "REDITC2")], "SAVINGS", wc("SAVINGS"), WRULES)
assert ans == "AVINGSS2"
mcq(COD, LC, "Advanced",
    "In a certain code, LOAN is written as OANL2 and CREDIT is written as REDITC2. How is SAVINGS written in that "
    "code?", ans, ["AVINGSS5", "SSAVING2", "AVINGSS7"], "Two parts: a letter move and a count",
    "LOAN → OANL (first letter moved to the end) + 2 (its vowels O, A). CREDIT → REDITC + 2 (E, I). Other counts do "
    "not fit both: LOAN has 2 consonants but CREDIT has 4, and the lengths are 4 and 6. SAVINGS → AVINGSS + 2 (A, I).",
    ["Move: first letter to the end (LOAN → OANL, CREDIT → REDITC)",
     "Number: vowels (2 in LOAN, 2 in CREDIT); consonant counts 2 and 4 and lengths 4 and 6 do not fit",
     f"SAVINGS → AVINGSS, vowels A and I ⇒ {ans}"],
    why_others_wrong="AVINGSS5 counts the consonants; SSAVING2 moves the last letter to the front; AVINGSS7 uses the "
                     "word length.", seconds=75, verified_by=RECOMP)

# ================================================================================================ ALPHANUMERIC SERIES
ALN = "Alphanumeric Series"
PB, SN = "Position-based", "Symbol and number series"
CONS = lambda t: is_l(t) and t not in VOW


def near(seq, i, k=3):
    """Wrong options: distinct elements near position i (0-based) other than seq[i]."""
    out = []
    for d in (1, -1, 2, -2, 3, -3, 4, -4):
        j = i + d
        if 0 <= j < len(seq) and seq[j] != seq[i] and seq[j] not in out:
            out.append(seq[j])
    return out[:k]

# ---- Basic set (5 questions on one arrangement)
SR = "K 5 % M 2 E @ 9 R T 3 # A 7 L $ 6 U P 1 & W".split()
assert len(SR) == 22
sid = stimulus("data_table", "Arrangement of 22 letters, numbers and symbols",
               "Study the following arrangement of letters, numbers and symbols and answer the questions.\n\n"
               + " ".join(SR), None,
               "Positions from the left: " + ", ".join(f"{i + 1}: {t}" for i, t in enumerate(SR)) + ".")
AQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    ALN, sub, "Basic", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
i_ = len(SR) - 8          # 8th from the right (0-based index)
ans_i = i_ - 5            # 5th to the left of it
ans = SR[ans_i]
assert SR[i_] == "L" and ans == "T"
AQ(PB, "Which element is 5th to the left of the 8th element from the right end?", ans, near(SR, ans_i),
   "Convert a right-end position, then move left",
   f"The 8th element from the right is the {i_ + 1}th from the left ({SR[i_]}). Five places to its left is the "
   f"{ans_i + 1}th element: {ans}.", [f"8th from the right = {len(SR)} − 8 + 1 = {i_ + 1}th from the left = {SR[i_]}",
                                       f"{i_ + 1} − 5 = {ans_i + 1}th ⇒ {ans}"], seconds=40)
hits = [w for w in windows(SR) if is_s(w[1]) and is_d(w[2])]
a, w = count_opts(len(hits))
AQ(SN, "How many symbols in the arrangement are immediately followed by a number?", a, w,
   "Check the right neighbour of every symbol",
   "Symbols and their right neighbours: " + ", ".join(f"{SR[i]} → {SR[i + 1]}" for i in range(len(SR) - 1)
                                                     if is_s(SR[i])) + f". Followed by a number: {len(hits)}.",
   ["Symbols: " + ", ".join(t for t in SR if is_s(t)), "Matches: " + ", ".join(" ".join(h[1:]) for h in hits)],
   natural=by_num, seconds=45)
assert SR[-1] == "W" and not is_s(SR[-1])
nosym = [t for t in SR if not is_s(t)]
ans = nosym[10 - 1]
AQ(PB, "If all the symbols are removed from the arrangement, which element will be 10th from the left end?", ans,
   near(nosym, 9), "Delete first, then count",
   "Without symbols: " + " ".join(nosym) + f". The 10th element from the left is {ans}.",
   ["Remove " + ", ".join(t for t in SR if is_s(t)), "New arrangement: " + " ".join(nosym), f"10th = {ans}"],
   seconds=45)
lets = [i for i, t in enumerate(SR) if is_l(t)]
btw = [t for t in SR[SR.index("M") + 1:SR.index("U")] if is_l(t)]
assert btw == ["E", "R", "T", "A", "L"]
AQ(PB, "How many letters are there between M and U in the arrangement?", num_word(len(btw)),
   ["Four", "Six", "Eleven"], "Count only letters",
   "Between M (4th) and U (18th) the letters are E, R, T, A and L: five letters (numbers and symbols are not "
   "counted).", ["Elements between M and U: " + " ".join(SR[SR.index("M") + 1:SR.index("U")]),
                 "Letters among them: E, R, T, A, L"],
   why_others_wrong="Eleven counts letters, numbers and symbols together; Four and Six miscount the letters.",
   natural=by_num, seconds=45)
odd_after_cons = [w for w in windows(SR) if CONS(w[1]) and is_d(w[2]) and int(w[2]) % 2 == 1]
a, w = count_opts(len(odd_after_cons))
AQ(SN, "Count the consonants in the arrangement whose right-hand neighbour is an odd number. How many are there?", a, w,
   "Consonant + odd-number pairs",
   "Consonants followed by a number: " + ", ".join(f"{SR[i]} {SR[i + 1]}" for i in range(len(SR) - 1)
                                                   if CONS(SR[i]) and is_d(SR[i + 1])) +
   f". Of these, the number is odd in {len(odd_after_cons)} case(s): " +
   (", ".join(" ".join(h[1:]) for h in odd_after_cons) or "none") + ".",
   ["List each consonant's right neighbour", "Keep only odd numbers"], natural=by_num, seconds=50)

# ---- Intermediate (standalone)
SR = "B 8 © Q 4 I ★ 6 D N 3 £ O 9 G 2 ¥ S 7 H".split()
keep = SR[1::2]   # elements in even positions (2nd, 4th, ...) remain
ans = keep[-5]
mcq(ALN, PB, "Intermediate", series_intro(" ".join(SR)) +
    "\n\nIf every element in an odd position (1st, 3rd, 5th, …) of the arrangement is removed, which element will be "
    "5th from the right end of the new arrangement?", ans, near(keep, len(keep) - 5),
    "Removing alternate elements halves the arrangement",
    "Keeping only the elements in even positions gives " + " ".join(keep) + f". Counting from the right, the 5th is "
    f"{ans}.", ["Even positions: " + " ".join(keep), f"5th from the right: {ans}"], seconds=55, verified_by=RECOMP)
SR = "5 F # 8 K @ E 2 L % 9 M U 3 $ P 6 & R 4 A".split()
hit = [w for w in windows(SR) if is_d(w[1]) and CONS(w[0]) and is_s(w[2])]
a, w = count_opts(len(hit))
mcq(ALN, SN, "Intermediate", series_intro(" ".join(SR)) +
    "\n\nHow many numbers in the arrangement are immediately preceded by a consonant and immediately followed by a "
    "symbol?", a, w, "Both neighbours must match",
    "Numbers with both neighbours: " + "; ".join(f"{SR[i - 1]} {SR[i]} {SR[i + 1]}" for i in range(1, len(SR) - 1)
                                                if is_d(SR[i])) + f". Consonant before and symbol after: "
    + (", ".join(" ".join(h) for h in hit) or "none") + f" — {len(hit)}.",
    ["Check each number's left and right neighbour", "Matches: " + ", ".join(" ".join(h) for h in hit)],
    natural=by_num, seconds=60, verified_by=RECOMP)


# ---- Alphanumeric Advanced set (5 questions on one arrangement)
SR = "9 D £ 4 I 7 Q ★ F 2 © H O 5 ¥ S 8 A # 3 E 6 Z @ N 1".split()
assert len(SR) == 26
sid = stimulus("data_table", "Arrangement of 26 letters, numbers and symbols",
               "Study the following arrangement of letters, numbers and symbols and answer the questions.\n\n"
               + " ".join(SR), None,
               "Positions from the left: " + ", ".join(f"{i + 1}: {t}" for i, t in enumerate(SR)) + ".")
AQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    ALN, sub, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
nos = [t for t in SR if not is_s(t)]
i9 = len(nos) - 9
ans = nos[i9 + 4]
AQ(PB, "If all the symbols are removed, which element will be 4th to the right of the 9th element from the right "
   "end?", ans, near(nos, i9 + 4), "Delete, convert the right-end position, then move",
   f"Without the six symbols there are {len(nos)} elements: " + " ".join(nos) + f". The 9th from the right is the "
   f"{i9 + 1}th from the left ({nos[i9]}); four places to its right is the {i9 + 5}th: {ans}.",
   ["Remove £, ★, ©, ¥, #, @", "New arrangement: " + " ".join(nos),
    f"9th from the right = {len(nos)} − 9 + 1 = {i9 + 1}th from the left = {nos[i9]}",
    f"4 places to the right ⇒ {i9 + 5}th = {ans}"], seconds=80)
pairs_ = [(SR[i - 1], SR[i]) for i in range(1, len(SR)) if is_d(SR[i]) and SR[i - 1] in VOW]
ans = sum(int(b) for _, b in pairs_)
assert pairs_ == [("I", "7"), ("O", "5"), ("E", "6")] and ans == 18
AQ(SN, "What is the sum of all the numbers in the arrangement that are immediately preceded by a vowel?", str(ans),
   ["12", "21", "26"], "Vowel–number pairs",
   "The vowels are I, O, A and E. I is followed by 7, O by 5, E by 6, and A by the symbol #. Sum: 7 + 5 + 6 = 18.",
   ["Vowels: I, O, A, E", "Right neighbours: I → 7, O → 5, A → #, E → 6", "7 + 5 + 6 = 18"],
   why_others_wrong="12 leaves out 6; 21 adds the 3 that follows #; 26 adds the 8 before A.", natural=int,
   seconds=75)
hits = [w for w in windows(SR) if CONS(w[1]) and is_s(w[0]) and is_d(w[2])]
a, w = count_opts(len(hits))
AQ(SN, "Count the consonants that have a symbol on their immediate left and a number on their immediate right in "
   "this arrangement. How many such consonants are there?", a, w, "Both neighbours of each consonant",
   "Consonants with both neighbours: " + "; ".join(f"{SR[i - 1]} {SR[i]} {SR[i + 1]}" for i in range(1, len(SR) - 1)
                                                  if CONS(SR[i])) + ". Symbol before and number after: "
   + (", ".join(" ".join(h) for h in hits) or "none") + f" — {len(hits)}.",
   ["List each consonant with its two neighbours", "Keep symbol–consonant–number triples"], natural=by_num,
   seconds=80)
g = lambda i: f"{SR[i]} {SR[i + 2]} {SR[i + 1]}"
GOOD = [g(1), g(9), g(15)]
BAD = "O ¥ S"
all_g = {g(i) for i in range(len(SR) - 2)}
assert all(x in all_g for x in GOOD) and BAD not in all_g
AQ(PB, "Three of the following four groups are formed in the same way from the arrangement (an element, then the "
   "element two places to its right, then the element between them). Which group does NOT belong?", BAD, GOOD,
   "Read each group back into the arrangement",
   "In the arrangement D is followed by £ and then 4, so 'D 4 £' takes an element, the element two places to its "
   "right and then the element between them. '2 H ©' (from 2 © H) and 'S A 8' (from S 8 A) are formed the same way. "
   "O is followed by 5 and ¥, so the same rule would give 'O ¥ 5', not 'O ¥ S'.",
   ["Pattern: x, (x + 2), (x + 1)", "D £ 4 → D 4 £ ✓; 2 © H → 2 H © ✓; S 8 A → S A 8 ✓", "O 5 ¥ → O ¥ 5, not O ¥ S"],
   seconds=85)
rv = SR[:13][::-1] + SR[13:]
ans = rv[20 - 1 - 7]
assert ans == "9"
AQ(PB, "If the first thirteen elements of the arrangement are written in reverse order, which element will be 7th to "
   "the left of the 20th element from the left end?", ans, near(rv, 12), "Rearrange a block, then count",
   "After reversing the first thirteen: " + " ".join(rv) + f". The 20th element is {rv[19]} (unchanged, outside the "
   f"block); seven places to its left is the 13th, which is now {ans} (originally the 1st element).",
   ["New order: " + " ".join(rv), f"20th = {rv[19]}", f"20 − 7 = 13th ⇒ {ans}"], seconds=80)

# ================================================================================================ ALPHABET TEST
ABT = "Alphabet Test"
LP, WF, PRS = "Letter position", "Word formation", "Pairs of letters"
ev = AL[1::2]
ans = ev[-7]
assert ans == "N"
mcq(ABT, LP, "Intermediate", "If every letter in an odd-numbered position of the English alphabet (A, C, E, …) is "
    "removed, which letter will be 7th from the right end of the remaining letters?", ans, ["L", "P", "M"],
    "Keep the even-position letters", "The remaining letters are " + " ".join(ev) + f" (13 letters). Counting from the "
    f"right: Z, X, V, T, R, P, {ans}.", ["Remaining: " + " ".join(ev), f"7th from the right = 7th from the left of "
                                                                        f"the reversed list = {ans}"],
    why_others_wrong="L is 8th and P 6th from the right; M was removed (it is 13th, an odd position).", seconds=50,
    verified_by=RECOMP)
k3 = [c for i, c in enumerate(AL) if (i + 1) % 3 != 0]
ans = k3[9]
assert ans == "N"
mcq(ABT, LP, "Intermediate", "If every third letter of the English alphabet (C, F, I, …) is removed, which letter "
    "will be 10th from the left end of the remaining letters?", ans, ["M", "P", "O"],
    "Two of every three letters remain",
    "Remaining letters: " + " ".join(k3) + f". The 10th is {ans}.",
    ["Every block of three keeps its first two letters", "10th remaining = 2nd letter of the 5th block (M N O) = N"],
    shortcut="Ten remaining letters = five blocks of two; the 5th block is M N O, so the 10th is N.",
    why_others_wrong="M is the 9th remaining letter; O was removed; P is the 11th.", seconds=55, verified_by=RECOMP)
SRC = "INTERNATIONAL"
can = lambda wd: all(wd.count(c) <= SRC.count(c) for c in set(wd))
OPTS = ["ALTERNATION", "INTERVAL", "LATITUDE", "TERMINAL"]
assert [can(x) for x in OPTS] == [True, False, False, False]
mcq(ABT, WF, "Intermediate", "Which of the following words can be formed using the letters of the word "
    "'INTERNATIONAL', each letter used no more often than it appears in INTERNATIONAL?", OPTS[0], OPTS[1:],
    "Compare letter counts",
    "INTERNATIONAL has I×2, N×3, T×2, E, R, A×2, O and L. ALTERNATION needs A×2, L, T×2, E, R, N×3, I and O, all "
    "available. INTERVAL needs a V, LATITUDE needs U and D, and TERMINAL needs an M, none of which occur.",
    ["Letters available: A2 E1 I2 L1 N3 O1 R1 T2", "ALTERNATION: A2 E1 I1 L1 N3 O1 R1 T2 ✓",
     "INTERVAL (V), LATITUDE (U, D), TERMINAL (M) ✗"], seconds=60, verified_by=RECOMP)
DWORDS = ["BANNER", "BANK", "BANQUET", "BANJO", "BANDIT"]
srt = sorted(DWORDS)
ans = srt[2]
assert srt == ["BANDIT", "BANJO", "BANK", "BANNER", "BANQUET"] and ans == "BANK"
mcq(ABT, WF, "Intermediate", "If the words BANNER, BANK, BANQUET, BANJO and BANDIT are arranged in the order in which "
    "they appear in an English dictionary, which word will be third?", ans, ["BANJO", "BANNER", "BANDIT"],
    "Dictionary order is decided by the first letter that differs",
    "All five start with BAN, so compare the 4th letters: D (BANDIT), J (BANJO), K (BANK), N (BANNER), Q (BANQUET). "
    f"The third is {ans}.", ["Common prefix BAN", "4th letters: D < J < K < N < Q", "Order: " + ", ".join(srt)],
    why_others_wrong="BANJO is second, BANNER fourth and BANDIT first.", seconds=45, verified_by=RECOMP)
wd = "FLOWCHART"
pr = letter_pairs(wd)
a, w = count_opts(len(pr))
mcq(ABT, PRS, "Intermediate", f"How many pairs of letters are there in the word '{wd}' each of which has as many "
    "letters between them in the word as in the English alphabet (counting both forward and backward)?", a, w,
    "Compare the gap in the word with the gap in the alphabet",
    f"Pairs found: " + (", ".join(f"{x}{y}" for x, y in pr) or "none") + f" — {len(pr)} in all.",
    ["Positions in the word vs alphabet positions: " + ", ".join(f"{c} {pos(c)}" for c in wd),
     "A pair qualifies when |word gap| = |alphabet gap|"], natural=by_num, seconds=75, verified_by=RECOMP)
wd2 = "DISTANCE"
pr2 = letter_pairs(wd2)
a, w = count_opts(len(pr2))
mcq(ABT, PRS, "Intermediate", f"In the word '{wd2}', how many pairs of letters have the same number of letters "
    "between them in the word as between them in the English alphabet? Count a pair whether its letters appear in "
    "alphabetical or reverse order.", a, w,
    "Compare the gap in the word with the gap in the alphabet",
    f"Pairs found: " + (", ".join(f"{x}{y}" for x, y in pr2) or "none") + f" — {len(pr2)} in all.",
    ["Alphabet positions: " + ", ".join(f"{c} {pos(c)}" for c in wd2),
     "A pair qualifies when |word gap| = |alphabet gap|"], natural=by_num, seconds=75, verified_by=RECOMP)
bl = sorted(shift(c, 3) for c in "BLANKET")
ans = bl[2]
assert "".join(bl) == "DEHNOQW" and ans == "H"
mcq(ABT, LP, "Intermediate", "Each letter of the word 'BLANKET' is replaced by the letter three places after it in "
    "the English alphabet, and the new letters are then arranged in alphabetical order from left to right. Which "
    "letter will be third from the left?", ans, ["E", "N", "O"], "Transform, then sort",
    "B→E, L→O, A→D, N→Q, K→N, E→H, T→W gives E O D Q N H W. In alphabetical order: D E H N O Q W. The third is H.",
    ["+3: E O D Q N H W", "Sorted: D E H N O Q W", "3rd = H"],
    why_others_wrong="E is second; N fourth; O fifth.", seconds=55, verified_by=RECOMP)

# ================================================================================================ RANKING
RNK = "Ranking and Order"
PIR, CHW = "Position in a row", "Comparison of heights/weights"
ans = 41 - 13 + 1
assert ans == 29
mcq(RNK, PIR, "Basic", "Rohit ranks 13th from the top in a class of 41 students. What is his rank from the bottom?",
    f"{ans}th", ["28th", "30th", "27th"], "From the other end = total − rank + 1",
    "Rank from the bottom = 41 − 13 + 1 = 29th.", ["41 − 13 = 28 students below Rohit", "Rank from the bottom = 28 + 1 "
                                                   "= 29th"],
    why_others_wrong="28th forgets to add 1; 30th adds 2; 27th subtracts 1 instead of adding.",
    natural=lambda t: int(t[:-2]), seconds=30, verified_by=RECOMP)
tot = 5 + 8 + 1 + 5
assert tot == 19
mcq(RNK, PIR, "Basic", "In a queue, Asha is 5th from the front and Bina, who stands behind Asha, is 6th from the "
    "back. Exactly eight persons stand between Asha and Bina. How many persons are there in the queue?", str(tot),
    ["18", "20", "21"], "Front part + between + back part",
    "Asha's position from the front is 5. Eight persons stand between, so Bina is 5 + 8 + 1 = 14th from the front. She "
    f"is 6th from the back, so the queue has 14 + 6 − 1 = {tot} persons.",
    ["Bina = 5 + 9 = 14th from the front", f"Total = 14 + 6 − 1 = {tot}"],
    why_others_wrong="18 subtracts one person too many; 20 forgets to subtract Bina once; 21 counts both Asha and Bina "
                     "twice.", natural=int, seconds=40, verified_by=RECOMP)
P = list("ABCDE")
orders = [p for p in itertools.permutations(P) if p.index("A") < p.index("B") and p.index("B") < p.index("C")
          and p.index("D") < p.index("A") and p[-1] == "E"]
assert orders == [("D", "A", "B", "C", "E")]
mcq(RNK, CHW, "Basic", "Among five boys A, B, C, D and E, each of a different height, A is taller than B, C is "
    "shorter than B, D is taller than A, and E is the shortest. Who is the third tallest?", "B", ["A", "C", "D"],
    "Build the order from pairwise clues", "D > A > B > C, and E is last: D, A, B, C, E. The third tallest is B.",
    ["D > A > B > C", "E shortest ⇒ D, A, B, C, E", "Third = B"],
    why_others_wrong="A is second, D tallest, C fourth.", seconds=35, verified_by=BRUTE)
tot = 7 + 15 - 1
need = 30 - tot
assert need == 9
mcq(RNK, PIR, "Basic", "Anu is 7th from the left end and 15th from the right end of a row of girls. How many more "
    "girls must join the row so that there are 30 girls in it?", str(need), ["8", "10", "7"],
    "Total from both ends", f"The row has 7 + 15 − 1 = {tot} girls, so 30 − {tot} = {need} more are needed.",
    [f"Total = 7 + 15 − 1 = {tot}", f"30 − {tot} = {need}"],
    why_others_wrong="8 forgets to subtract Anu once (22 girls); 10 subtracts her twice; 7 is her position.",
    natural=int, seconds=35, verified_by=RECOMP)
passed = 31 - 6
ans = 31 - 7 + 1
assert ans == 25
mcq(RNK, PIR, "Intermediate", "In a class of 31 students, 6 students failed an examination and are ranked below all "
    "those who passed. Among the students who passed, Ravi is 7th from the top. What is Ravi's rank from the bottom "
    "in the whole class?", f"{ans}th", ["19th", "24th", "26th"], "Failed students sit below him, so they count",
    "Since everyone who failed is ranked below everyone who passed, Ravi is also 7th from the top of the whole class. "
    f"His rank from the bottom is 31 − 7 + 1 = {ans}th.",
    ["Failed students are below all passed students ⇒ Ravi is 7th from the top overall",
     f"From the bottom: 31 − 7 + 1 = {ans}"],
    why_others_wrong=f"19th is his rank from the bottom among the {passed} who passed only; 24th forgets to add 1; "
                     "26th adds 2.", natural=lambda t: int(t[:-2]), seconds=55, verified_by=RECOMP)

# ---- Advanced set: seven students and their marks
P = ["Ahana", "Dev", "Ira", "Jojo", "Kriti", "Moti", "Pia"]
orders = [p for p in itertools.permutations(P)  # p[0] = highest
          if p.index("Dev") == 4 and p.index("Pia") < p.index("Ira") < p.index("Jojo") and p[0] == "Kriti"
          and p.index("Dev") < p.index("Moti") < p.index("Ahana") and p.index("Jojo") < p.index("Dev")]
assert orders == [("Kriti", "Pia", "Ira", "Jojo", "Dev", "Moti", "Ahana")]
O_ = orders[0]
sid = stimulus("puzzle", "Seven students and their marks",
               "Seven students Ahana, Dev, Ira, Jojo, Kriti, Moti and Pia scored different marks in a test.\n\n"
               "- Dev scored more than only two students.\n- Ira scored more than Jojo but less than Pia.\n"
               "- Kriti scored the highest marks.\n- Moti scored less than Dev but more than Ahana.\n"
               "- Jojo scored more than Dev.", None,
               "Step 1: Kriti is 1st. Dev is above exactly two students: 5th.\nStep 2: Moti and Ahana are below Dev "
               "with Moti above Ahana: 6th and 7th.\nStep 3: Pia > Ira > Jojo fill 2nd, 3rd and 4th (Jojo is above "
               "Dev, so all three fit above him).\n\nHighest to lowest: " + ", ".join(O_))
RQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    RNK, CHW, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=BRUTE, **kw)
RQ("Who scored the third highest marks?", O_[2], ["Pia", "Jojo", "Dev"], "Fix the 'only' clue first",
   "Highest to lowest: " + ", ".join(O_) + f". Third: {O_[2]}.", ["Kriti 1st; Dev 5th", "Moti 6th, Ahana 7th",
                                                                 "Pia, Ira, Jojo ⇒ 2nd, 3rd, 4th"], seconds=70)
cands = [57, 64, 71, 73]
ok = [c for c in cands if 58 < c < 71]
assert ok == [64]
RQ("If Jojo scored 71 marks and Moti scored 58, which of the following can be Dev's score?", "64",
   ["57", "71", "73"], "A middle rank must lie strictly between its neighbours",
   "Dev is below Jojo and above Moti, so his marks are less than 71 and more than 58 (all marks are different). Only "
   "64 fits.", ["Jojo (4th) > Dev (5th) > Moti (6th)", "58 < Dev < 71 ⇒ 64"],
   why_others_wrong="57 is below Moti; 71 equals Jojo's marks; 73 is above Jojo.", natural=int, seconds=65)
cnt = O_.index("Jojo") - O_.index("Kriti") - 1
assert cnt == 2
RQ("How many students scored more than Jojo but less than Kriti?", num_word(cnt), ["One", "Three", "Four"],
   "Count strictly between two places", "Between Kriti (1st) and Jojo (4th) are Pia and Ira: two students.",
   ["Order: " + ", ".join(O_)], natural=by_num, seconds=60)
# ---- Advanced (standalone)
A_pos = 11
C_pos = A_pos + 8
B_pos = 2 * C_pos - A_pos
tot = B_pos + 16 - 1
assert (C_pos, B_pos, tot) == (19, 27, 42)
mcq(RNK, PIR, "Advanced",
    "Some persons sit in a row, all facing north. Amit is 11th from the left end and Bhola is 16th from the right "
    "end. Chetan sits exactly midway between Amit and Bhola, and exactly seven persons sit between Amit and Chetan. "
    "How many persons sit in the row?", str(tot), ["41", "43", "40"], "Midpoint doubles the distance",
    "Seven persons between Amit and Chetan put Chetan 8 places from Amit. Bhola cannot be to Amit's left (Chetan "
    "would be at position 3 and Bhola at −5), so Chetan is 19th and Bhola, as far again, is 27th from the left. "
    f"With Bhola 16th from the right, the row has 27 + 16 − 1 = {tot} persons.",
    ["Chetan = 11 + 8 = 19th (the left side is impossible)", "Bhola = 19 + 8 = 27th from the left",
     f"Total = 27 + 16 − 1 = {tot}"],
    why_others_wrong="41 subtracts Bhola twice; 43 forgets to subtract him once; 40 places Chetan 7 places away "
                     "instead of 8.", natural=int, seconds=80, verified_by=RECOMP)
ans = 60 - 15 - 23
assert ans == 22
mcq(RNK, PIR, "Advanced",
    "Class A has 28 students and class B has 32. In class A, Ritu is 9th from the top; in class B, Sonu is 11th from "
    "the bottom. The two classes are combined into one ranking list of 60 students, in which Ritu is 15th from the top "
    "and Sonu is 23rd from the bottom. How many students are ranked between Ritu and Sonu in the combined list?",
    str(ans), ["21", "23", "40"], "Only the combined-list positions matter",
    "In the combined list of 60, Ritu is 15th from the top and Sonu is 60 − 23 + 1 = 38th from the top. Between them "
    f"are 38 − 15 − 1 = {ans} students. The ranks within the old classes are not needed.",
    ["Sonu from the top = 60 − 23 + 1 = 38th", f"Between 15th and 38th: 38 − 15 − 1 = {ans}"],
    why_others_wrong="21 subtracts one too many; 23 forgets to exclude one end; 40 mixes the class ranks with the "
                     "combined ranks.", natural=int, seconds=70, verified_by=RECOMP)

# ================================================================================================ INPUT-OUTPUT
WR, NR, MM = "Word rearrangement", "Number rearrangement", "Mixed machine"


def run_machine(items, key, side="left", tf=None):
    """Each step takes the unarranged item with the smallest key, transforms it (if tf is given), and places it next
    to the items already arranged (at the left end, or at the right end). Every step must change the line; without a
    transformation the machine stops as soon as the line is final."""
    cur, rest, done, steps = list(items), list(items), [], []
    while rest:
        nxt = min(rest, key=key)
        rest.remove(nxt)
        done = done + [tf(nxt) if tf else nxt] if side == "left" else [tf(nxt) if tf else nxt] + done
        new = done + rest if side == "left" else rest + done
        if new == cur:
            assert tf is None and sorted(rest, key=key) == rest, ("a step changes nothing", cur)
            break
        cur = new
        steps.append(cur[:])
    return steps


line = lambda s: " ".join(map(str, s))
step_txt = lambda st: [f"Step {ROMAN[i]}: {line(s_)}" for i, s_ in enumerate(st)]

# ---- Basic (standalone): words in reverse alphabetical order to the left
INP = "chair bed lamp desk sofa table".split()
st = run_machine(INP, key=lambda w: [-ord(c) for c in w])
assert len(st) == 4 and st[-1] == ["table", "sofa", "lamp", "desk", "chair", "bed"]
mcq(IOT, WR, "Basic",
    "A word arrangement machine rearranges a line of words step by step. In each step it takes, among the words not "
    "yet arranged, the word that comes LAST in alphabetical order and places it at the left end, immediately to the "
    "right of the words already arranged (in Step I, at the extreme left). The other words keep their order. The "
    "machine stops when the arrangement is complete.\n\nInput: " + line(INP) + "\n\nWhich of the following is Step "
    "III?", line(st[2]), [line(st[1]), line(st[3]), line(sorted(INP))], "Reverse alphabetical selection",
    "Reverse alphabetical order: table, sofa, lamp, desk, chair, bed. " + " ".join(f"{t}." for t in step_txt(st)),
    step_txt(st), why_others_wrong="The other lines are Step II, Step IV and the words in plain alphabetical order.",
    seconds=50, verified_by=RECOMP)

# ---- Intermediate set: mixed machine (numbers by digit sum to the left, words in reverse alphabetical order to the
#      right)
INP = ["rose", 47, "lily", 85, "aster", 31, "tulip", 66, "daisy", 19]
dsum = lambda n: sum(map(int, str(n)))


def mixed(items):
    cur, steps = list(items), []
    nums_done, words_done = [], []
    while True:
        rest = [x for x in cur if x not in nums_done and x not in words_done]
        rn = [x for x in rest if isinstance(x, int)]
        rw = [x for x in rest if isinstance(x, str)]
        if not rn and not rw:
            break
        if rn:
            nums_done.append(max(rn, key=dsum))
        if rw:
            words_done.insert(0, max(rw))
        rest = [x for x in cur if x not in nums_done and x not in words_done]
        new = nums_done + rest + words_done
        assert new != cur
        cur = new
        steps.append(cur[:])
    return steps


assert len({dsum(n) for n in INP if isinstance(n, int)}) == 5
st = mixed(INP)
assert len(st) == 5
sid = stimulus("passage", "Machine: digit sums to the left, words to the right",
               "A word and number arrangement machine rearranges a line of words and numbers step by step. In each "
               "step it makes two moves: (1) among the numbers not yet arranged, the one with the largest sum of digits "
               "is placed at the left end, immediately to the right of the numbers already arranged there; (2) among "
               "the words not yet arranged, the one that comes last in alphabetical order is placed at the right end, "
               "immediately to the left of the words already arranged there. All other elements keep their order. The "
               "machine stops when every element has been arranged.\n\nInput: " + line(INP), None,
               "Digit sums: " + ", ".join(f"{n} → {dsum(n)}" for n in INP if isinstance(n, int)) +
               ", so the numbers are taken in the order 85, 66, 47, 19, 31. Words from last to first alphabetically: "
               "tulip, rose, lily, daisy, aster.\n\n" + "\n".join(step_txt(st)))
IQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    IOT, MM, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
IQ("Which of the following is Step III?", line(st[2]), [line(st[1]), line(st[3]), line(st[4])],
   "Two moves per step", "Each step places one number on the left and one word on the right. "
   + " ".join(f"{t}." for t in step_txt(st[:3])), step_txt(st[:3]),
   why_others_wrong="The other lines are Steps II, IV and V.", seconds=75)
IQ("How many steps does the machine take to complete the arrangement?", num_word(len(st)), ["Four", "Six", "Three"],
   "One number and one word per step", "There are five numbers and five words, and each step arranges one of each, so "
   f"the arrangement is complete after Step {ROMAN[len(st) - 1]}.", step_txt(st), natural=by_num, seconds=60)
s2 = st[1]
ans = s2[s2.index("lily") + 3]
IQ("In Step II, which element is 3rd to the right of 'lily'?", str(ans),
   [str(x) for x in near(s2, s2.index("lily") + 3)], "Read the step, then count",
   f"Step II: {line(s2)}. Three places to the right of 'lily' is {ans}.", [f"Step II: {line(s2)}"], seconds=60)
first = next(i for i, s_ in enumerate(st) if abs(s_.index(19) - s_.index("aster")) == 1)
IQ("In which step do '19' and 'aster' stand next to each other for the first time?", f"Step {ROMAN[first]}",
   [f"Step {ROMAN[i]}" for i in range(5) if i != first][:3], "Scan the steps in order",
   " ".join(f"{t}." for t in step_txt(st)) + f" The pair first appears side by side in Step {ROMAN[first]}.",
   step_txt(st), natural=lambda t: ROMAN.index(t.split()[1]), seconds=70)

# ---- Intermediate (standalone): numbers by the difference of their digits
INP = [64, 95, 30, 87, 19, 72]
dd = lambda n: abs(n // 10 - n % 10)
assert len({dd(n) for n in INP}) == len(INP)
st = run_machine(INP, key=lambda n: -dd(n))
target = st[2]
mcq(IOT, NR, "Intermediate",
    "A number arrangement machine rearranges numbers step by step. In each step it takes, among the numbers not yet "
    "arranged, the one whose two digits differ by the largest amount, and places it at the left end, immediately to "
    "the right of the numbers already arranged. The other numbers keep their order. The machine stops when the "
    "arrangement is complete.\n\nInput: " + line(INP) + f"\n\nIn which step does the line read '{line(target)}'?",
    "Step III", ["Step II", "Step IV", "Step V"], "Selection by the difference of digits",
    "Differences of digits: " + ", ".join(f"{n} → {dd(n)}" for n in INP) + ". " + " ".join(f"{t}." for t in
                                                                                         step_txt(st)),
    step_txt(st), natural=lambda t: ROMAN.index(t.split()[1]), seconds=70, verified_by=RECOMP)
assert len(st) == 4
# ---- Intermediate (standalone): words by their last letter
INP = "sky flower ocean cloud path song".split()
st = run_machine(INP, key=lambda w: w[-1])
s3 = st[2]
ans = s3[s3.index("path") + 2]
assert ans == "flower"
mcq(IOT, WR, "Intermediate",
    "A word arrangement machine rearranges words step by step. In each step it takes, among the words not yet "
    "arranged, the word whose LAST letter comes earliest in the alphabet, and places it at the left end, immediately "
    "to the right of the words already arranged. The other words keep their order.\n\nInput: " + line(INP) +
    "\n\nIn Step III, which word is second to the right of 'path'?", ans, ["sky", "ocean", "song"],
    "Selection by the last letter",
    "Last letters: " + ", ".join(f"{w_} {w_[-1]}" for w_ in INP) + ", so the order is cloud, song, path, ocean, "
    f"flower, sky. Step III: {line(s3)}. Two places to the right of 'path' is {ans}.", step_txt(st[:3]),
    seconds=70, verified_by=RECOMP)

# ---- Advanced (standalone): longest word first, with its first and last letters interchanged
INP = "kite elephant sun garden paper rainbow".split()
assert len({len(w_) for w_ in INP}) == len(INP)
swp = lambda w: w[-1] + w[1:-1] + w[0] if len(w) > 1 else w
st = run_machine(INP, key=lambda w: -len(w), tf=swp)
assert len(st) == 6
mcq(IOT, WR, "Advanced",
    "A machine rearranges words step by step. In each step it takes, among the words not yet arranged, the longest "
    "word, interchanges its first and last letters, and places it at the left end, immediately to the right of the "
    "words already arranged. The other words keep their order. The machine stops when every word has been "
    "arranged.\n\nInput: " + line(INP) + "\n\nWhich of the following is Step IV?", line(st[3]),
    [line(st[2]), line(st[4]), line(st[3][:4] + st[3][4:][::-1])],
    "Selection by length with a letter swap",
    "Lengths: " + ", ".join(f"{w_} {len(w_)}" for w_ in INP) + ". " + " ".join(f"{t}." for t in step_txt(st[:4])),
    step_txt(st[:4]), why_others_wrong="The first two wrong lines are Steps III and V; the last one changes the order "
                                       "of the words not yet arranged.", seconds=95,
    verified_by=RECOMP)

# ---- Advanced (standalone): closest to 50 first, replaced by its distance from 50
INP = [37, 62, 49, 81, 55, 23]
dist50 = lambda n: abs(n - 50)
assert len({dist50(n) for n in INP}) == len(INP)
st = run_machine(INP, key=dist50, tf=dist50)
ans = sum(st[3])
mcq(IOT, NR, "Advanced",
    "A number machine works step by step. In each step it takes, among the numbers not yet arranged, the number "
    "closest to 50, replaces it by its distance from 50 (for example, 47 becomes 3), and places the result at the left "
    "end, immediately to the right of the results already placed. The other numbers keep their order.\n\nInput: "
    + line(INP) + "\n\nWhat is the sum of all the numbers in Step IV?", str(ans),
    [str(sum(st[2])), str(sum(st[4])), str(sum(INP))], "Selection plus transformation",
    "Distances from 50: " + ", ".join(f"{n} → {dist50(n)}" for n in INP) + ". " + " ".join(
        f"{t}." for t in step_txt(st[:4])) + f" Sum of Step IV: {ans}.", step_txt(st[:4]),
    why_others_wrong="The other values are the sums of Step III, Step V and the input.", natural=int, seconds=100,
    verified_by=RECOMP)

# ================================================================================================ DATA SUFFICIENCY
grid = [{"p": (px, py), "q": (qx, qy)} for px in range(-10, 11) for py in range(-10, 11)
        for qx in range(-10, 11) for qy in range(-10, 11)]
got = ds2(grid, lambda m: m["p"] == (0, 6), lambda m: m["q"] == (8, 0),
          lambda m: round(((m["p"][0] - m["q"][0]) ** 2 + (m["p"][1] - m["q"][1]) ** 2) ** 0.5, 6))
assert got == "T"
fixed(DSF, "Two-statement", "Intermediate",
      DS_HEAD + "Question: What is the straight-line distance between village P and village Q?\n\n"
      "I. Village P is 6 km north of village R.\nII. Village Q is 8 km east of village R.",
      [DS2[k_] for k_ in "ABNT"], DS2["T"], "Data sufficiency: test each statement alone, then together",
      "I places P relative to R but says nothing about Q; II places Q relative to R but says nothing about P. Together, "
      "P and Q are the ends of a right angle at R with legs 6 km and 8 km, so PQ = 10 km.",
      ["I alone: Q unknown ⇒ not sufficient", "II alone: P unknown ⇒ not sufficient",
       "Together: √(6² + 8²) = 10 km ⇒ both needed"], seconds=50, verified_by=ENUM)
models = [{"n": n, "r": r, "s": s} for n in range(20, 61) for r in range(1, n + 1) for s in range(1, n + 1) if r != s]
fns = [lambda m: m["r"] == 12, lambda m: m["n"] - m["s"] + 1 == 20, lambda m: m["s"] == m["r"] + 4]
got = ds3(models, fns, lambda m: m["n"])
assert got == "ALL"
fixed(DSF, "Three-statement", "Advanced",
      DS3_HEAD + "Question: How many students are there in the class?\n\nI. Ravi is 12th from the top.\n"
      "II. Sita is 20th from the bottom.\nIII. Ravi is 4 ranks above Sita.",
      [DS3[k_] for k_ in ("I+III", "II+III", "ALL", "NONE")], DS3["ALL"],
      "Three-statement data sufficiency: test every pair",
      "To count the class we need one person's rank from both ends. I + III: Sita is 16th from the top, but her rank "
      "from the bottom is unknown. II + III: Ravi is 24th from the bottom, but his rank from the top is unknown. I + II: "
      "two different persons, with no link between them. All three: Sita is 16th from the top and 20th from the "
      "bottom, so the class has 16 + 20 − 1 = 35 students.",
      ["I + II: no link between Ravi and Sita ⇒ not sufficient", "I + III: Sita 16th from the top only",
       "II + III: Ravi 24th from the bottom only", "All three: 16 + 20 − 1 = 35 ⇒ all three needed"],
      seconds=80, verified_by=ENUM)

# ================================================================================================ VERBAL REASONING
# Hand-written items. Each was solved by the author and then re-answered blind (without keys) by a separate solver;
# scenarios were chosen so that the keyed answer does not depend on outside facts.
ASM = "Statement and Assumptions"
AOPT = ["Only assumption I is implicit", "Only assumption II is implicit", "Neither I nor II is implicit",
        "Both I and II are implicit"]
A_I, A_II, A_N, A_B = AOPT
A_HEAD = ("Read the statement and the two assumptions. An assumption is something supposed or taken for granted by "
          "the person making the statement. Decide which of the assumptions is/are implicit in the statement.\n\n")


def asm(diff, statement, a1, a2, answer, explanation, steps, why, seconds=45):
    return fixed(ASM, "Implicit assumptions", diff,
                 A_HEAD + f"Statement: {statement}\n\nAssumptions:\nI. {a1}\nII. {a2}", AOPT, answer,
                 "Implicit assumption: what the speaker must take for granted", explanation, steps,
                 why_others_wrong=why, seconds=seconds, verified_by=HAND)


# ---- Basic
asm("Basic", "Notice in a library: \"Books must be returned within 14 days. A fine of ₹5 per day will be charged after "
    "that.\"", "Some borrowers may keep books for longer than 14 days.",
    "The fine will encourage borrowers to return books on time.", A_B,
    "A rule with a late fine is needed only if some borrowers might keep books beyond the limit (I). Fixing a fine "
    "assumes that it will push borrowers to return books on time (II); otherwise the fine would serve no purpose.",
    ["Late-return rule ⇒ late returns are expected: I implicit", "A fine is meant to deter ⇒ II implicit"],
    "Each 'Only' option drops one premise of the notice; Neither ignores both.", seconds=35)
asm("Basic", "The principal has asked parents to send their children to school with raincoats during the monsoon.",
    "It is likely to rain while the children are on their way to or from school during the monsoon.",
    "All parents drop their children to school by car.", A_I,
    "Asking for raincoats makes sense only if rain is likely during the school journey (I). If all children came by "
    "car, raincoats would hardly be needed, so II runs against the request.",
    ["Raincoats are requested because rain is expected ⇒ I implicit", "II would make the request pointless ⇒ not "
     "implicit"], "Both and Only II accept II, which contradicts the purpose of the request.", seconds=30)
asm("Basic", "A notice beside the lift of an office building: \"To save electricity, please use the stairs if you are "
    "going up or down only one or two floors.\"", "People in the building never use the stairs.",
    "Using the lift for short trips uses electricity that could be saved.", A_II,
    "The notice links using the stairs for short trips to saving electricity, so it assumes that the lift uses "
    "electricity on such trips (II). It asks people to use the stairs more; it does not assume that they never use "
    "them (I).", ["Purpose: save electricity by avoiding short lift trips ⇒ II implicit",
                  "'Never use the stairs' is an extreme claim the notice does not need ⇒ I not implicit"],
    "Only I and Both accept an extreme 'never' claim.", seconds=35)
asm("Basic", "The municipal corporation has announced that the water supply will be cut for six hours on Sunday for "
    "pipeline repairs and has advised residents to store water in advance.",
    "Residents are able to store water in advance.",
    "Residents will need water during the six hours when the supply is cut.", A_B,
    "Advising residents to store water assumes they can do so (I) and that they will need water while the supply is "
    "off (II); without either premise the advice would be pointless.",
    ["Advice to store water ⇒ residents can store it: I implicit",
     "Storing water in advance matters only if water is needed during the cut ⇒ II implicit"],
    "Each 'Only' option drops one of two premises the advice rests on.", seconds=40)
asm("Basic", "An advertisement: \"Join our weekend yoga classes — the only classes in the city taught by a certified "
    "instructor.\"", "Everyone in the city wants to learn yoga.",
    "People who join yoga classes cannot attend classes on weekdays.", A_N,
    "The advertisement offers weekend classes and highlights the certified instructor. It does not need everyone to "
    "want yoga (I is an extreme generalisation), and offering weekend classes does not assume that no learner can "
    "come on weekdays (II).",
    ["I: 'everyone' is extreme and not needed ⇒ not implicit",
     "II: weekend classes suit some people; nothing says no one can attend on weekdays ⇒ not implicit"],
    "Each of the other options accepts at least one claim the advertiser does not need.", seconds=35)
# ---- Advanced
asm("Advanced", "The bank has decided to open its new branch in the industrial area rather than in the nearby "
    "residential colony.", "The bank expects the industrial area to bring it more business than the residential "
    "colony.", "The residential colony has no residents who need banking services.", A_I,
    "Choosing one location over another assumes that the chosen one is expected to be better for the bank, most "
    "naturally in business terms (I). The choice does not require the colony to have no banking needs at all (II); it "
    "only needs the industrial area to be the better option.",
    ["Preference for the industrial area ⇒ it is expected to be more useful: I implicit",
     "'No residents who need banking' is extreme; a weaker reason is enough ⇒ II not implicit"],
    "Only II and Both accept an extreme claim; Neither ignores the basis of the choice.", seconds=55)
asm("Advanced", "The state government plans to set up cold-storage units near major vegetable markets to reduce the "
    "wastage of vegetables.", "A significant part of the wastage happens because vegetables cannot be stored in cold "
    "conditions.", "Traders and farmers will be able to use cold-storage units located near the markets.", A_B,
    "The plan expects cold storage to reduce wastage, so it assumes that lack of cold storage is a real cause of the "
    "wastage (I). Placing the units near markets assumes the people who handle the vegetables there can use them (II); "
    "unusable units would not reduce wastage.",
    ["Remedy = cold storage ⇒ cause includes lack of cold storage: I implicit",
     "Units near markets must be usable by those who handle the produce ⇒ II implicit"],
    "Each 'Only' option drops one premise the plan needs; Neither ignores both.", seconds=55)
asm("Advanced", "An airline has announced that passengers who check in online can use a separate fast-track security "
    "lane at the airport.", "Most passengers prefer to check in at the airport counter.",
    "A separate lane can reduce the time that passengers who check in online spend in the security queue.", A_II,
    "Offering a fast-track lane as a benefit assumes the lane actually saves time for those passengers (II). The "
    "airline need not assume anything about what most passengers prefer (I); if anything, the offer hopes to move "
    "more passengers to online check-in.",
    ["Benefit offered = shorter security wait ⇒ II implicit",
     "Preference of 'most passengers' is not needed for the offer ⇒ I not implicit"],
    "Only I and Both accept a claim about majority preference that the announcement does not rely on.", seconds=55)
asm("Advanced", "The city's mayor said, \"The new cycle lanes have been a success: the number of people cycling on the "
    "main roads has doubled since they opened.\"", "Before the cycle lanes opened, nobody in the city cycled.",
    "Every cyclist in the city now rides only on the cycle lanes.", A_N,
    "The mayor assumes that the rise in cycling is due to the lanes, but neither assumption says that. 'Doubled' "
    "means there were cyclists before, so I contradicts the statement; II is an extreme claim about every cyclist "
    "that the mayor's success claim does not need.",
    ["'Doubled' implies some cyclists before ⇒ I contradicts the statement",
     "'Every cyclist only on the lanes' is extreme and unnecessary ⇒ II not implicit"],
    "The other options accept at least one claim the statement either contradicts or does not need.", seconds=55)

# ================================================================================================ STATEMENT-CONCLUSION
SCN = "Statement and Conclusions"
SC_HEAD = ("Read the statement and the two conclusions. Assume everything in the statement to be true, and decide "
           "which conclusion(s) logically follow from it.\n\n")
VC, INF = "Valid conclusions", "Inferences"


def scq(diff, sub, statement, c1, c2, answer, explanation, steps, why, seconds=45):
    return fixed(SCN, sub, diff, SC_HEAD + f"Statement: {statement}\n\nConclusions:\nI. {c1}\nII. {c2}",
                 conclusion_options(answer), answer, "A conclusion must follow from the statement alone", explanation,
                 steps, why_others_wrong=why, seconds=seconds, verified_by=HAND)


scq("Basic", VC, "All trains that leave from platform 3 go to Nagpur. The 5:10 pm train leaves from platform 3.",
    "The 5:10 pm train goes to Nagpur.", "No train that leaves from platform 1 goes to Nagpur.", ONLY_I,
    "The rule covers every train leaving from platform 3, and the 5:10 pm train is one of them, so I follows. The "
    "statement says nothing about trains from other platforms, so II does not follow.",
    ["All platform-3 trains → Nagpur; the 5:10 pm train is a platform-3 train ⇒ I",
     "Platform 1 is never mentioned ⇒ II does not follow"],
    "Only II and Both rely on information about platform 1 that is not given.", seconds=30)
scq("Intermediate", INF, "The price of milk rose from ₹54 to ₹60 a litre, while a family's monthly milk consumption "
    "stayed at 30 litres.", "The family's monthly spending on milk rose by ₹180.",
    "The family's total monthly expenses rose.", ONLY_I,
    "The increase is (60 − 54) × 30 = ₹180 a month, so I follows. The family's other expenses are not given; they may "
    "have fallen by more, so II does not follow.",
    ["Extra cost = ₹6 × 30 litres = ₹180 ⇒ I follows", "Other expenses unknown ⇒ II does not follow"],
    "Only II and Both assume that nothing else in the budget changed.", seconds=45)
scq("Intermediate", VC, "Some of the city's buses run on electricity, and every electric bus in the city was bought "
    "last year.", "All the buses the city bought last year run on electricity.",
    "Some of the city's buses were bought last year.", ONLY_II,
    "The electric buses exist and were all bought last year, so some of the city's buses were bought last year (II). "
    "The city may also have bought diesel or CNG buses last year, so I does not follow.",
    ["Electric buses exist and all were bought last year ⇒ II",
     "'All electric buses were bought last year' does not reverse to 'all buses bought last year are electric' ⇒ I "
     "fails"], "Only I and Both reverse an 'all' statement.", seconds=45)
scq("Intermediate", INF, "A survey of 200 visitors at a book fair found that 120 of them bought at least one book.",
    "Most people in the city buy books.", "The book fair will be held again next year.", NEITHER,
    "The survey covers only 200 fair visitors, who are not a sample of the whole city, so I does not follow. Nothing "
    "in the statement concerns future fairs, so II does not follow.",
    ["120 of 200 visitors (60%) bought a book — a fact about the visitors only",
     "I generalises to the whole city ⇒ does not follow", "II is a prediction ⇒ does not follow"],
    "The other options accept a generalisation or a prediction that the data cannot support.", seconds=40)
scq("Intermediate", VC, "The ATM at the railway station dispenses only ₹500 notes, and its limit is ₹20,000 per card "
    "per day.", "A customer cannot withdraw ₹1,200 from this ATM in a single withdrawal.",
    "A customer cannot withdraw more than ₹20,000 in a day from this ATM with one card.", BOTH,
    "With only ₹500 notes, every withdrawal is a multiple of ₹500, and ₹1,200 is not, so I follows. The daily limit of "
    "₹20,000 per card gives II directly.",
    ["Only ₹500 notes ⇒ amounts in multiples of 500 ⇒ ₹1,200 impossible: I", "Daily limit per card ₹20,000 ⇒ II"],
    "Only I or Only II misses one of two direct consequences; Neither ignores both.", seconds=40)
scq("Intermediate", INF, "The committee will meet on exactly one day next week, and that day will be either Monday or "
    "Tuesday.", "The committee will meet on Monday next week.", "The committee will meet on Tuesday next week.",
    EITHER, "The statement does not say which day, so neither conclusion is certain by itself. But the meeting is on "
    "exactly one of the two days, so one of the conclusions must be true: either I or II follows.",
    ["Exactly one meeting day, Monday or Tuesday", "I alone and II alone are not certain",
     "I and II cannot both be false, and cannot both be true ⇒ Either I or II follows"],
    "'Either' replaces 'Both' (four-option rule); 'Neither' ignores that one of the two must hold.", seconds=40)
scq("Intermediate", INF, "A train covered 360 km in exactly 4 hours without stopping.",
    "The train's average speed for the journey was 90 km/h.",
    "At some moment during the journey, the train's speed was at least 90 km/h.", BOTH,
    "Average speed = 360 ÷ 4 = 90 km/h, so I follows. If the speed had stayed below 90 km/h the whole time, the train "
    "would have covered less than 360 km in 4 hours, so at some moment it must have reached at least 90 km/h (II).",
    ["360 km ÷ 4 h = 90 km/h ⇒ I", "Always below 90 km/h ⇒ distance < 360 km, a contradiction ⇒ II"],
    "Only I misses that a speed can never stay below its own average throughout; Only II and Neither ignore the "
    "direct calculation.", seconds=55)

# ================================================================================================ CRITICAL REASONING
CRT = "Critical Reasoning"
SW_, CA_, INFP = "Strengthen and weaken", "Course of action", "Inference from a passage"


def crq(diff, sub, text, correct, wrongs, concept, explanation, steps, why, seconds=60):
    return mcq(CRT, sub, diff, text, correct, wrongs, concept, explanation, steps, why_others_wrong=why,
               seconds=seconds, verified_by=HAND)


# ---- Basic
crq("Basic", CA_, "Statement: Many passengers at a railway station miss train announcements because the loudspeakers "
    "on two platforms are not working.\n\nWhich of the following is the most appropriate course of action?",
    "Repair or replace the faulty loudspeakers and show train information on display screens",
    ["Stop making announcements at the station", "Ask passengers to reach the station three hours early",
     "Close the two platforms permanently"], "A course of action must remove the stated cause",
    "The cause is broken loudspeakers. Repairing them, with screens as a back-up, solves the problem directly.",
    ["Problem: missed announcements", "Cause: faulty loudspeakers on two platforms", "Remedy: fix them; add screens"],
    "Stopping announcements worsens the problem; arriving early does not help passengers hear; closing platforms is "
    "extreme.", seconds=30)
crq("Basic", INFP, "A bakery sold 400 loaves of bread in the first week of a month and 500 loaves in the second week, "
    "at the same price per loaf in both weeks.\n\nWhich of the following can be inferred?",
    "The bakery earned more from selling loaves in the second week than in the first",
    ["More customers visited the bakery in the second week", "The bakery will sell 600 loaves in the third week",
     "The bakery's bread became tastier in the second week"], "Inference: only what the figures guarantee",
    "Same price per loaf and 100 more loaves sold means higher revenue from loaves in the second week.",
    ["Revenue from loaves = price × number", "Same price, 500 > 400 ⇒ higher revenue in week 2"],
    "The same customers may simply have bought more; the third-week figure is a prediction; taste is not mentioned.",
    seconds=35)
crq("Basic", SW_, "Claim: Planting a thick row of trees along the school's boundary wall will reduce the noise from "
    "the nearby highway inside the classrooms.\n\nWhich of the following, if true, most strengthens the claim?",
    "Studies show that a dense belt of trees reduces the traffic noise reaching buildings behind it",
    ["Trees give shade to students during break time", "The highway was widened two years ago",
     "Some parents have offered to donate saplings"], "Strengthen: support the cause–effect link in the claim",
    "The claim links a row of trees to less noise. Evidence that tree belts reduce traffic noise behind them supports "
    "that link directly.", ["Claim: trees → less highway noise in classrooms",
                            "Strengthener: evidence that tree belts block traffic noise"],
    "Shade and donated saplings do not bear on noise; the widening of the highway explains the noise, not the remedy.",
    seconds=35)
crq("Basic", SW_, "A juice shop owner says that her sales rose last month because of her new radio advertisement.\n\n"
    "Which of the following, if true, most weakens her claim?",
    "Last month was the hottest month of the year, and sales at juice shops all over the city rose by about the same "
    "amount", ["The advertisement was played 50 times during the month", "The shop sells twelve flavours of juice",
               "Many people in the city listen to the radio"], "Weaken: another cause for the same effect",
    "If juice sales rose equally at shops that did not advertise, the hot weather explains the rise, not the "
    "advertisement.", ["Claim: advertisement → higher sales", "Alternative: a heatwave raised sales everywhere"],
    "The number of plays and radio listenership, if anything, support the claim; the number of flavours is "
    "irrelevant.", seconds=40)
crq("Basic", CA_, "Statement: Every monsoon, several students of a village school fall ill after drinking water from "
    "the school's water tank, which has not been cleaned for months.\n\nWhich of the following is the most appropriate "
    "course of action?", "Clean the tank regularly and test the drinking water before use",
    ["Close the school for the whole monsoon", "Ban students from drinking water at school",
     "Remove the water tank without providing another source of water"],
    "A course of action should fix the cause without causing new harm",
    "The illnesses come from an uncleaned tank, so regular cleaning and water testing remove the cause.",
    ["Problem: students fall ill", "Cause: dirty water tank", "Remedy: clean it regularly; test the water"],
    "Closing the school or removing water does not solve the problem and harms the students.", seconds=30)
crq("Basic", INFP, "In a class of 40 students, every student plays at least one of the two games, cricket and "
    "football. 25 students play cricket and 22 play football.\n\nWhich of the following must be true?",
    "Exactly 7 students play both games",
    ["No student plays both games", "17 students play only cricket", "10 students play only football"],
    "Two overlapping groups that cover everyone",
    "Since every student plays at least one game, both = 25 + 22 − 40 = 7. Then only cricket = 25 − 7 = 18 and only "
    "football = 22 − 7 = 15.", ["Cricket + football − both = 40", "Both = 47 − 40 = 7",
                                "Only cricket 18; only football 15"],
    "'No student plays both' would give only 47 > 40 places; 17 and 10 are not the correct 'only' counts (18 and 15).",
    seconds=45)
crq("Basic", CA_, "Statement: Customers of a bank branch complain that they have to stand in a long queue at the "
    "counter just to get their passbooks updated.\n\nWhich of the following is the most appropriate course of "
    "action?", "Install a self-service passbook printing machine at the branch",
    ["Stop issuing passbooks to all customers", "Allow passbooks to be updated only once a year",
     "Close the branch on its busiest days"], "A course of action should be practical and aimed at the problem",
    "The queue forms because passbook updates go through the counter. A self-service printer removes that load from "
    "the counter.", ["Problem: long counter queues", "Cause: passbook updates at the counter",
                     "Remedy: self-service passbook printer"],
    "The other steps cut the service itself or make it worse instead of removing the queue.", seconds=30)
# ---- Intermediate
crq("Intermediate", SW_, "Argument: The town should start a weekly farmers' market, because it will let farmers earn "
    "more by selling directly to buyers.\n\nWhich of the following, if true, most strengthens the argument?",
    "In nearby towns with weekly farmers' markets, farmers get about 30% more for the same produce than they get from "
    "middlemen", ["Many townspeople enjoy shopping on weekends", "The town has a large open ground near the bus stand",
                  "Some middlemen oppose the idea of a farmers' market"],
    "Strengthen: evidence for the claimed benefit",
    "The argument's key claim is that direct selling raises farmers' earnings. Evidence from comparable towns that "
    "farmers get more at such markets supports exactly that.",
    ["Claim: farmers' market → higher farmer earnings", "Strengthener: comparable towns show a 30% higher price"],
    "Weekend shopping and an open ground make the market feasible but do not show higher earnings; middlemen's "
    "opposition does not prove a benefit to farmers.", seconds=55)
crq("Intermediate", SW_, "A gym claims that its new 12-week programme helps members lose weight, because members who "
    "completed the programme lost 6 kg on average.\n\nWhich of the following, if true, most weakens the claim?",
    "Most members who joined the programme dropped out in the first month, and only those who were already losing "
    "weight steadily completed it", ["The programme includes three sessions a week",
                                     "The gym charges a higher fee for the programme",
                                     "Members who completed the programme were very satisfied with it"],
    "Weaken: the result may come from who was counted, not from the programme",
    "If only members who were already losing weight finished, the 6 kg average describes a self-selected group. The "
    "figure cannot show that the programme caused the loss.",
    ["Evidence: completers lost 6 kg on average", "Weakener: completers were a self-selected group already losing "
     "weight"], "Sessions per week and fees do not bear on the result; satisfaction is not evidence of weight loss.",
    seconds=55)
crq("Intermediate", INFP, "Passage: A city gets all its water from two lakes, A and B. Last year each lake supplied "
    "half of the city's water. This year lake A supplied 60% of the water, and the total supply was the same as last "
    "year.\n\nWhich of the following can be inferred?", "Lake B supplied less water this year than last year",
    ["Lake B is drying up", "The city's demand for water fell this year",
     "Lake A will supply 70% of the water next year"], "Shares of an unchanged total",
    "With the total unchanged, lake B's share fell from 50% to 40%, so it supplied less water than last year.",
    ["Total unchanged", "Lake B: 50% → 40% of the same total ⇒ less water"],
    "The passage gives no reason for the change (drying up is a guess); demand is not mentioned and the total supply "
    "did not change; next year's share is a prediction.", seconds=50)
# ---- Advanced
crq("Advanced", SW_, "Argument: Since the city started a free bus service for women, the number of women travelling by "
    "bus has risen by 40%. So the free service has increased the number of trips that women in the city make.\n\n"
    "Which of the following, if true, most seriously weakens the argument?",
    "Most of the new women bus riders earlier made the same trips by auto-rickshaw or shared taxi, and the total number "
    "of trips made by women in the city has not changed",
    ["Buses on some routes have become crowded during peak hours",
     "Many men have asked for free bus travel as well", "The free service costs the city a large amount every year"],
    "Weaken: the evidence shows a shift between modes, not more trips",
    "The conclusion is about the number of trips, but the evidence is about bus ridership. If the new riders only "
    "switched from other modes and total trips are unchanged, the conclusion fails.",
    ["Evidence: more women on buses", "Conclusion: more trips by women",
     "Weakener: riders switched modes; total trips unchanged"],
    "Crowding, men's demands and the cost of the scheme do not bear on whether women make more trips.", seconds=75)
crq("Advanced", INFP, "Passage: This year, the total deposits of Bank X rose by 8%. Its current-account deposits rose "
    "by 20%, and all its other deposits together rose by 5%.\n\nWhich of the following must be true?",
    "Last year, current-account deposits made up exactly 20% of the bank's total deposits",
    ["This year, current-account deposits are larger than all other deposits together",
     "The bank's other deposits fell this year",
     "The share of current-account deposits in total deposits fell this year"],
    "Weighted average of two growth rates",
    "Let last year's current-account deposits be C and other deposits O. Then 0.20C + 0.05O = 0.08(C + O), so 0.12C = "
    "0.03O and O = 4C. Current-account deposits were C ÷ 5C = 20% of the total.",
    ["0.20C + 0.05O = 0.08(C + O)", "0.12C = 0.03O ⇒ O = 4C", "Share last year = C / (C + 4C) = 20%"],
    "This year current deposits are 1.2C against 4.2C of others; other deposits rose by 5%; the current-account share "
    "rose (it grew faster than the total).", seconds=90)
crq("Advanced", CA_, "Statement: An audit found that many names on a district's ration-card list belong to people who "
    "died or moved away years ago, while several needy families in the district have no ration card.\n\nWhich of the "
    "following is the most appropriate course of action?",
    "Verify the list door to door, remove ineligible names and enrol the needy families who were left out",
    ["Stop the ration scheme in the district", "Cancel all ration cards and issue no new ones",
     "Take no action, since most cards on the list are genuine"],
    "A course of action should fix both errors without hurting eligible people",
    "There are two problems: ineligible names on the list and eligible families left out. Door-to-door verification "
    "with removal and fresh enrolment fixes both while keeping the scheme for genuine beneficiaries.",
    ["Problem 1: ineligible names", "Problem 2: needy families excluded",
     "Remedy: verify, remove and enrol — the scheme continues for genuine holders"],
    "Stopping the scheme or cancelling all cards punishes genuine beneficiaries; doing nothing leaves both problems in "
    "place.", seconds=60)
crq("Advanced", SW_, "A restaurant chain claims that its new online ordering system, and not any price cut, raised its "
    "orders by 25% over the last six months.\n\nWhich of the following, if true, most strengthens the claim?",
    "The chain did not change its prices in the last six months, and its outlets that had not yet adopted the system "
    "saw no rise in orders", ["Orders at rival restaurant chains also rose by about 25% in the same period",
                              "Customers often say they like discounts",
                              "The online system cost the chain a large amount to build"],
    "Strengthen: rule out the alternative and compare with a control group",
    "Unchanged prices rule out the price explanation, and outlets without the system seeing no rise point to the "
    "system as the cause of the increase.",
    ["Claim: ordering system (not prices) → 25% more orders", "No price change ⇒ the price explanation is ruled out",
     "Outlets without the system: no rise ⇒ supports the system as the cause"],
    "A similar rise at rivals points to a market-wide cause and weakens the claim; liking discounts and the system's "
    "cost do not bear on the cause of the rise.", seconds=75)
# ================================================================================================ WRITE
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_004_plan.json").read_text(encoding="utf-8"))
splan = next(s_ for s_ in plan["subjects"] if s_["subject"] == RA)
have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
CHECK_QUOTA = "--draft" not in sys.argv
for t in splan["topics"]:
    for d_, n_ in t["quota"].items():
        if CHECK_QUOTA:
            assert have[(t["topic"], d_)] == n_, (t["topic"], d_, have[(t["topic"], d_)], n_)
        elif have[(t["topic"], d_)] != n_:
            print("quota", t["topic"], d_, have[(t["topic"], d_)], "/", n_)
    assert all(x["subtopic"] in t["subtopics"] for x in QUESTIONS if x["topic"] == t["topic"]), t["topic"]
assert all(x["topic"] in {t["topic"] for t in splan["topics"]} for x in QUESTIONS)
for st_ in STIMULI:
    n_ = sum(1 for x in QUESTIONS if x.get("stimulus_id") == st_["stimulus_id"])
    assert 3 <= n_ <= 6, (st_["stimulus_id"], n_)
    assert len({x["difficulty"] for x in QUESTIONS if x.get("stimulus_id") == st_["stimulus_id"]}) == 1
assert STIMULI[0]["stimulus_id"] == splan["stimulus_id_start"]
print(f"{len(QUESTIONS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(KEYCOUNT.items()))}")
if CHECK_QUOTA:
    assert len(QUESTIONS) == splan["total"] == 200
    assert QUESTIONS[0]["question_id"] == splan["question_ids"][0]
    assert QUESTIONS[-1]["question_id"] == splan["question_ids"][1]
    assert max(KEYCOUNT.values()) - min(KEYCOUNT.values()) <= 12, KEYCOUNT
    doc = {
        "schema_version": "1.0",
        "batch_id": "BATCH_004",
        "created_at": TODAY,
        "notes": ("Reasoning Ability part of BATCH_003: 200 original questions (60 Basic, 80 Intermediate, 60 "
                  "Advanced) built by tools/batch_003/reasoning.py. New puzzle structures (a bench with distances, "
                  "back-to-back rows, a row with ages, a hexagonal table with drinks, a square table with everyone "
                  "facing the centre, an eight-seat rectangular table, a circle with ages and mixed facing, a "
                  "ten-seat rectangular table with persons facing across, floors numbered from the top, a ground "
                  "floor numbered 0, two persons per floor, a building of unknown height, three stacks of boxes, "
                  "boxes holding counted items, months with colours, appointment dates with weekdays, a two-year "
                  "month grid, a hobby week, designations with branches). Puzzles are brute-forced for a unique "
                  "arrangement; syllogisms are checked over every Venn-region model; inequalities over all integer "
                  "assignments; data sufficiency by enumerating models for each statement subset; blood relations, "
                  "directions, coding (inferred rules checked against alternative simple rules), series, alphabet, "
                  "ranking and input-output are recomputed in code. Verbal-reasoning items are hand-written. All "
                  "questions await human review."),
        "stimuli": STIMULI,
        "questions": QUESTIONS,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
