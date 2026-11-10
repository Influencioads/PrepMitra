"""Builds batches/parts/BATCH_003_REAS.json: the 200 Reasoning Ability questions of BATCH_003.

Same method and helpers as tools/batch_002/reasoning.py, with new puzzle structures, noun sets and scenarios:
- puzzles and seating: the conditions are written once as (text, variables, test) triples; the text goes into the
  stimulus (or the question) and the test into an exhaustive backtracking search that must return exactly one
  arrangement. Every answer is then read off that arrangement;
- syllogisms: checked over every Venn-region model; inequalities: exhaustive integer assignments (with a growing
  value range as a cross-check);
- blood relations (explicit family tree), directions, coding (inferred rules are checked against a library of
  alternative simple rules), series, alphabet, number, ranking and input-output: recomputed in code; data
  sufficiency: each statement subset checked by enumerating models.
Verbal-reasoning items (assumptions, cause-effect, critical reasoning) are hand-written.
If any assertion fails, nothing is written. --draft prints quota gaps instead of asserting them.

    python tools/batch_003/reasoning.py        (run from docs/question-bank)
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
OUT = ROOT / "batches" / "parts" / "BATCH_003_REAS.json"
TODAY = "2026-11-05"
RA = "Reasoning Ability"
LETTERS = "ABCD"
FIRST_Q, FIRST_STIM = 405, 3001
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

# ---- L1 Basic (standalone): six persons facing north (seats 1..6 from the left; right = +1)
P = ["Mehul", "Nandini", "Omisha", "Pritam", "Rashmi", "Sudeep"]
conds = [("Rashmi sits at one of the extreme ends of the row.", ("Rashmi",), lambda r: r in (1, 6)),
         ("Pritam sits third to the right of Rashmi.", ("Pritam", "Rashmi"), lambda p, r: p == r + 3),
         ("Only one person sits between Pritam and Nandini.", ("Pritam", "Nandini"), lambda p, n: abs(p - n) == 2),
         ("Mehul sits immediately to the left of Nandini.", ("Mehul", "Nandini"), lambda m, n: m == n - 1),
         ("Omisha is not an immediate neighbour of Rashmi.", ("Omisha", "Rashmi"), lambda o, r: abs(o - r) != 1)]
L1 = unique(P, {p: range(1, 7) for p in P}, conds, [P])
at = {v: k for k, v in L1.items()}
assert [at[i] for i in range(1, 7)] == ["Rashmi", "Sudeep", "Omisha", "Pritam", "Mehul", "Nandini"]
ans = at[L1["Pritam"] - 2]
mcq(LIN, "Single row, facing north/south", "Basic",
    "Six persons Mehul, Nandini, Omisha, Pritam, Rashmi and Sudeep sit in a straight row, all facing north.\n"
    + bullets(conds) + "\n\nWho sits second to the left of Pritam?", ans, ["Omisha", "Mehul", "Rashmi"],
    "Facing north: the right is towards the east, the left towards the west",
    "Rashmi must be at the left end (from the right end there is no room for Pritam three seats to her right), so "
    "Rashmi = 1 and Pritam = 4. Nandini is two seats from Pritam: seat 2 or 6. Seat 2 would put Mehul at seat 1, "
    "Rashmi's seat, so Nandini = 6 and Mehul = 5. Omisha cannot sit next to Rashmi, so Omisha = 3 and Sudeep = 2. "
    f"Second to Pritam's left is seat 2: {ans}.",
    ["Rashmi at the right end leaves no seat three places to her right ⇒ Rashmi = 1, Pritam = 4",
     "Nandini = 2 or 6; Nandini = 2 needs Mehul at 1 (taken) ⇒ Nandini = 6, Mehul = 5",
     "Omisha not next to Rashmi ⇒ Omisha = 3, Sudeep = 2",
     "Left to right: Rashmi, Sudeep, Omisha, Pritam, Mehul, Nandini; second to the left of Pritam (4) = seat 2"],
    why_others_wrong="Omisha is immediately to Pritam's left; Mehul is immediately to his right; Rashmi is third to "
                     "his left.", seconds=45, verified_by=BRUTE)

# ---- L2 Intermediate: six persons on a straight bench with distances in metres (facing north; position = metres
#      east of Jasleen)
P = ["Gitanjali", "Hridaan", "Ishwari", "Jasleen", "Keshav", "Lakshya"]
IX = {p: i for i, p in enumerate(P)}
btw = lambda v, a, b: sum(1 for x in v if min(a, b) < x < max(a, b))
conds = [
    ("Jasleen sits at the extreme left end of the bench.", tuple(P), lambda *v: v[IX["Jasleen"]] == min(v)),
    ("Keshav sits 7 m to the right of Jasleen, and exactly one person sits between them.", tuple(P),
     lambda *v: v[IX["Keshav"]] - v[IX["Jasleen"]] == 7 and btw(v, v[IX["Keshav"]], v[IX["Jasleen"]]) == 1),
    ("Hridaan sits 3 m to the left of Keshav.", ("Hridaan", "Keshav"), lambda h, k: h == k - 3),
    ("Ishwari sits at the extreme right end of the bench, 13 m to the right of Keshav.", tuple(P),
     lambda *v: v[IX["Ishwari"]] == max(v) and v[IX["Ishwari"]] - v[IX["Keshav"]] == 13),
    ("Gitanjali sits 8 m to the left of Ishwari.", ("Gitanjali", "Ishwari"), lambda g, i: g == i - 8),
    ("Lakshya sits 2 m away from Gitanjali but not between Keshav and Gitanjali.",
     ("Lakshya", "Gitanjali", "Keshav"), lambda l, g, k: abs(l - g) == 2 and not min(k, g) < l < max(k, g)),
]
L2 = unique(P, {p: range(0, 26) for p in P} | {"Jasleen": [0]}, conds, [P])
assert [L2[p] for p in P] == [12, 4, 20, 0, 7, 14]
order_ = sorted(P, key=L2.get)
ARR = "West to east: " + ", ".join(f"{p} ({L2[p]} m)" for p in order_) + " (distances from Jasleen)"
sid = stimulus("puzzle", "Six persons on a bench, with distances",
               "Six persons Gitanjali, Hridaan, Ishwari, Jasleen, Keshav and Lakshya sit on a long straight bench, all "
               "facing north. The gaps between neighbours are not all equal; distances are measured along the bench.",
               conds,
               "Measure every position in metres east of Jasleen (the left end). Keshav = 7, and the one person between "
               "them is Hridaan at 7 − 3 = 4. Ishwari = 7 + 13 = 20 (the right end) and Gitanjali = 20 − 8 = 12. "
               "Lakshya is 2 m from Gitanjali: 10 lies between Keshav (7) and Gitanjali (12), so Lakshya = 14.\n\n"
               + table(["Person", "Metres east of Jasleen"], [(p, L2[p]) for p in order_]))
d = L2["Lakshya"] - L2["Hridaan"]
assert d == 10
puzzle_q(sid, LIN, "Single row, facing north/south", "Intermediate",
         "What is the distance between Hridaan and Lakshya?", f"{d} m", ["8 m", "12 m", "14 m"],
         "Positions on a line measured from one end",
         f"Hridaan is 4 m and Lakshya 14 m east of Jasleen, so they are {d} m apart.",
         ["Keshav 7, Hridaan 4 (the one person between Jasleen and Keshav)", "Ishwari 20, Gitanjali 12",
          "Lakshya = 12 ± 2; 10 is between Keshav and Gitanjali ⇒ 14", f"14 − 4 = {d} m"],
         why_others_wrong="8 m would place Lakshya at 12 (Gitanjali's spot); 12 m and 14 m measure from the wrong "
                          "starting points.", natural=lambda t: int(t.split()[0]), seconds=60)
ans = order_[order_.index("Keshav") + 2]
assert ans == "Lakshya"
puzzle_q(sid, LIN, "Single row, facing north/south", "Intermediate", "Who sits second to the right of Keshav?",
         ans, ["Gitanjali", "Ishwari", "Hridaan"], "Order on the line, ignoring the gaps",
         f"In order from the west: {', '.join(order_)}. Facing north, Keshav's right is towards the east: Gitanjali, "
         f"then {ans}.", [ARR, "East of Keshav: Gitanjali (12), Lakshya (14), Ishwari (20)"],
         why_others_wrong="Gitanjali is immediately to Keshav's right; Ishwari is third to his right; Hridaan is "
                          "immediately to his left.", seconds=50)
pairs6 = [(a, b) for a, b in itertools.combinations(order_, 2) if L2[b] - L2[a] == 6]
assert pairs6 == [("Lakshya", "Ishwari")]
puzzle_q(sid, LIN, "Single row, facing north/south", "Intermediate",
         "Which of the following pairs of persons sit exactly 6 m apart?", "Lakshya and Ishwari",
         ["Hridaan and Gitanjali", "Jasleen and Keshav", "Keshav and Lakshya"], "Differences of positions",
         "Lakshya is at 14 m and Ishwari at 20 m: 6 m apart. The other pairs are 8 m, 7 m and 7 m apart.",
         [ARR, "Lakshya–Ishwari: 20 − 14 = 6", "Hridaan–Gitanjali: 8; Jasleen–Keshav: 7; Keshav–Lakshya: 7"],
         seconds=55)

# ---- L3 Advanced (standalone): two rows of four seats placed back to back; Row 1 faces north, Row 2 faces south.
#      Seat r*10 + c: r = row, c = 1..4 from west to east; (1, c) and (2, c) are back to back.
P = ["Amrita", "Baldev", "Charu", "Dushyant", "Eeshan", "Gargi", "Himesh", "Indira"]
SEATS = [r * 10 + c for r in (1, 2) for c in range(1, 5)]
row_, col = lambda s: s // 10, lambda s: s % 10
RB = lambda s, k: s + k if row_(s) == 1 else s - k  # k-th to the right (north-facing: east; south-facing: west)
back = lambda s: s + 10 if row_(s) == 1 else s - 10
conds = [
    ("Charu sits at an extreme end of Row 1.", ("Charu",), lambda c: row_(c) == 1 and col(c) in (1, 4)),
    ("Amrita sits second to the left of Charu.", ("Amrita", "Charu"), lambda a, c: a == RB(c, -2)),
    ("Himesh sits immediately to the right of Amrita.", ("Himesh", "Amrita"), lambda h, a: h == RB(a, 1)),
    ("Baldev sits back to back with Himesh.", ("Baldev", "Himesh"), lambda b, h: b == back(h)),
    ("Indira sits immediately to the right of Baldev.", ("Indira", "Baldev"), lambda i, b: i == RB(b, 1)),
    ("Eeshan faces south and sits back to back with Gargi.", ("Eeshan", "Gargi"),
     lambda e, g: row_(e) == 2 and e == back(g)),
]
L3 = unique(P, {p: SEATS for p in P}, conds, [P])
at = {v: k for k, v in L3.items()}
assert [at[s] for s in SEATS] == ["Gargi", "Amrita", "Himesh", "Charu", "Eeshan", "Indira", "Baldev", "Dushyant"]
x_ = at[RB(L3["Indira"], -1)]
ans = at[back(L3[x_])]
assert x_ == "Baldev" and ans == "Himesh"
mcq(LIN, "Double row", "Advanced",
    "Eight persons Amrita, Baldev, Charu, Dushyant, Eeshan, Gargi, Himesh and Indira sit in two rows of four seats "
    "each. The rows are placed back to back: the persons in Row 1 face north and those in Row 2 face south, and each "
    "seat of Row 1 is directly back to back with one seat of Row 2.\n" + bullets(conds) +
    "\n\nWho sits back to back with the person who sits immediately to the left of Indira?", ans,
    ["Amrita", "Charu", "Dushyant"], "Back-to-back rows: 'right' points in opposite directions in the two rows",
    "Number the seats 1 to 4 from west to east in both rows. Charu is at an end of Row 1, and Amrita is two seats to "
    "her left (west), so Charu = seat 4 and Amrita = seat 2; Himesh is immediately to Amrita's right: seat 3. Baldev "
    "is behind Himesh in Row 2, seat 3. Baldev faces south, so his right is west: Indira = Row 2, seat 2. Eeshan "
    "(Row 2) and Gargi are back to back in the only fully free column, seat 1, and Dushyant takes Row 2, seat 4. "
    "Indira faces south, so her left is east: Baldev. The person back to back with Baldev is Himesh.",
    ["Row 1 (facing north): Charu = 4 (at seat 1 there is no seat two places to her left), Amrita = 2, Himesh = 3",
     "Row 2 (facing south): Baldev = 3 (behind Himesh), Indira = 2 (to Baldev's right = west)",
     "Column 1: Gargi (Row 1) and Eeshan (Row 2); Dushyant = Row 2, seat 4",
     "Immediately to Indira's left (east) = Baldev; back to back with Baldev = Himesh"],
    why_others_wrong="Amrita is back to back with Indira herself; Charu is back to back with Dushyant; Dushyant is in "
                     "Row 2, so he is not back to back with anyone in his own row.", seconds=120, verified_by=BRUTE)

# ---- L4 Advanced (standalone): seven persons in a row facing north, each of a different age
P = ["Jagdish", "Kamini", "Manoj", "Nalini", "Prerna", "Qamar", "Rohini"]
AGES = [21, 25, 29, 33, 37, 41, 45]
A_ = ["a" + p for p in P]
VV = P + A_
IXV = {v: i for i, v in enumerate(VV)}
seat_of_age = lambda v, age: next(v[IXV[p]] for p in P if v[IXV["a" + p]] == age)
conds = [
    ("Manoj sits exactly in the middle of the row.", ("Manoj",), lambda m: m == 4),
    ("Only one person sits between Manoj and the oldest person.", tuple(VV),
     lambda *v: abs(seat_of_age(v, 45) - v[IXV["Manoj"]]) == 2),
    ("The youngest person sits immediately to the right of the oldest person.", tuple(VV),
     lambda *v: seat_of_age(v, 21) == seat_of_age(v, 45) + 1),
    ("Nalini sits at the extreme right end and is 4 years older than the youngest person.", ("Nalini", "aNalini"),
     lambda n, a: n == 7 and a == 25),
    ("Jagdish sits immediately to the left of Nalini and is older than Manoj.",
     ("Jagdish", "Nalini", "aJagdish", "aManoj"), lambda j, n, aj, am: j == n - 1 and aj > am),
    ("Prerna is 29 years old and sits to the right of Manoj.", ("Prerna", "Manoj", "aPrerna"),
     lambda p, m, a: p > m and a == 29),
    ("Qamar is older than Prerna but younger than Manoj.", ("aQamar", "aPrerna", "aManoj"),
     lambda q, p, m: p < q < m),
    ("Qamar sits at an extreme end of the row, and Rohini is not the oldest.", ("Qamar", "aRohini"),
     lambda q, r: q in (1, 7) and r != 45),
]
L4 = unique(VV, {p: range(1, 8) for p in P} | {a: AGES for a in A_}, conds, [P, A_])
at = {L4[p]: p for p in P}
assert [(at[i], L4["a" + at[i]]) for i in range(1, 8)] == [
    ("Qamar", 33), ("Kamini", 45), ("Rohini", 21), ("Manoj", 37), ("Prerna", 29), ("Jagdish", 41), ("Nalini", 25)]
ans = L4["a" + at[1]] + L4["a" + at[7]]
assert ans == 58
mcq(LIN, "Single row, facing north/south", "Advanced",
    "Seven persons Jagdish, Kamini, Manoj, Nalini, Prerna, Qamar and Rohini sit in a straight row, all facing north. "
    "Their ages are 21, 25, 29, 33, 37, 41 and 45 years, one age each.\n" + bullets(conds) +
    "\n\nWhat is the sum of the ages of the two persons who sit at the extreme ends of the row?", str(ans),
    ["54", "62", "66"], "Seating combined with an age ranking",
    "Manoj = 4, Nalini = 7, Jagdish = 6, and Prerna (to Manoj's right) = 5; Qamar takes an end, so Qamar = 1. The "
    "oldest sits at 2 or 6. If at 6, the youngest would be Nalini at 7, but Nalini is 4 years older than the "
    "youngest: rejected. So the oldest is at 2 and the youngest at 3. Rohini is not the oldest, so Rohini = 3 (21) "
    "and Kamini = 2 (45); Nalini = 25. Qamar, Manoj and Jagdish share 33, 37, 41 with Prerna (29) < Qamar < Manoj < "
    f"Jagdish: Qamar 33, Manoj 37, Jagdish 41. The ends are Qamar (33) and Nalini (25): {ans}.",
    ["Seats: Manoj 4, Nalini 7, Jagdish 6, Prerna 5, Qamar 1",
     "Oldest at 6 would make Nalini the youngest, contradicting 'Nalini = youngest + 4' ⇒ oldest at 2, youngest at 3",
     "Rohini not oldest ⇒ Rohini 3 (21), Kamini 2 (45); Nalini 21 + 4 = 25",
     "29 < Qamar < Manoj < Jagdish ⇒ 33, 37, 41", f"Ends: Qamar 33 + Nalini 25 = {ans}"],
    why_others_wrong="62 and 66 come from putting Kamini or Rohini at the left end; 54 uses Qamar's age as 29.",
    natural=int, seconds=120, verified_by=BRUTE)

# ================================================================================================ CIRCULAR SEATING
CIR = "Circular Seating Arrangement"

# ---- C1 Basic: hexagonal table, six persons facing the centre, each with a different drink
#      (seats 0..5 anticlockwise; facing the centre, right = +1)
P = ["Bhavesh", "Chaitali", "Dhaval", "Eesha", "Faraz", "Hemlata"]
DR = ["Coffee", "Juice", "Lassi", "Milk", "Soup", "Tea"]
N = 6
D_ = ["d" + p for p in P]
VV = P + D_
IXV = {v: i for i, v in enumerate(VV)}
seat_of = lambda v, drink: next(v[IXV[p]] for p in P if v[IXV["d" + p]] == drink)
conds = [
    ("Dhaval sits opposite Bhavesh.", ("Dhaval", "Bhavesh"), lambda d, b: d == (b + 3) % N),
    ("Eesha sits immediately to the right of Bhavesh.", ("Eesha", "Bhavesh"), lambda e, b: e == (b + 1) % N),
    ("Chaitali sits second to the right of Dhaval.", ("Chaitali", "Dhaval"), lambda c, d: c == (d + 2) % N),
    ("Faraz sits immediately to the left of Chaitali.", ("Faraz", "Chaitali"), lambda f, c: f == (c - 1) % N),
    ("Bhavesh drinks Tea, and the person who drinks Coffee sits opposite him.", tuple(VV),
     lambda *v: v[IXV["dBhavesh"]] == "Tea" and seat_of(v, "Coffee") == (v[IXV["Bhavesh"]] + 3) % N),
    ("The person who drinks Milk sits between Eesha and Dhaval.", tuple(VV),
     lambda *v: {(seat_of(v, "Milk") - 1) % N, (seat_of(v, "Milk") + 1) % N} == {v[IXV["Eesha"]], v[IXV["Dhaval"]]}),
    ("The person who drinks Lassi sits immediately to the right of the person who drinks Soup.", tuple(VV),
     lambda *v: seat_of(v, "Lassi") == (seat_of(v, "Soup") + 1) % N),
]
C1 = unique(VV, {p: range(N) for p in P} | {"Bhavesh": [0]} | {d: DR for d in D_}, conds, [P, D_])
at = {C1[p]: p for p in P}
drk = {p: C1["d" + p] for p in P}
assert [(at[i], drk[at[i]]) for i in range(N)] == [("Bhavesh", "Tea"), ("Eesha", "Juice"), ("Hemlata", "Milk"),
                                                  ("Dhaval", "Coffee"), ("Faraz", "Soup"), ("Chaitali", "Lassi")]
ARR = "Anticlockwise from Bhavesh: " + ", ".join(f"{at[i]} ({drk[at[i]]})" for i in range(N))
sid = stimulus("puzzle", "Six friends at a hexagonal table, with drinks",
               "Six friends Bhavesh, Chaitali, Dhaval, Eesha, Faraz and Hemlata sit around a hexagonal table, one at "
               "each side, all facing the centre. Each of them drinks a different one of Coffee, Juice, Lassi, Milk, "
               "Soup and Tea. (Facing the centre, a person's right is anticlockwise.)", conds,
               "Fix Bhavesh. Dhaval is opposite him, Eesha immediately to his right, Chaitali two places to Dhaval's "
               "right (immediately to Bhavesh's left) and Faraz between Dhaval and Chaitali. Hemlata takes the seat "
               "between Eesha and Dhaval. Bhavesh drinks Tea and Dhaval, opposite him, Coffee. The Milk drinker sits "
               "between Eesha and Dhaval: Hemlata. Of Eesha, Faraz and Chaitali, the only Soup–Lassi pair with Lassi "
               "immediately to the right is Faraz (Soup) and Chaitali (Lassi), so Eesha drinks Juice.\n\n"
               + table(["Seat (anticlockwise from Bhavesh)", "Person", "Drink"],
                       [(i, at[i], drk[at[i]]) for i in range(N)]))
ans = drk[at[(C1["Eesha"] + 3) % N]]
assert ans == "Soup"
puzzle_q(sid, CIR, "Facing centre", "Basic", "What does the person who sits opposite Eesha drink?", ans,
         ["Milk", "Lassi", "Coffee"], "Opposite seats at a six-seat table",
         "Eesha sits immediately to Bhavesh's right; three seats on is Faraz, who drinks Soup.",
         [ARR, "Opposite Eesha: Faraz", "Faraz drinks Soup"],
         why_others_wrong="Milk is Hemlata's (Eesha's neighbour), Lassi is Chaitali's and Coffee is Dhaval's.",
         seconds=45)
ans = at[(C1["Chaitali"] - 2) % N]
assert ans == "Dhaval"
puzzle_q(sid, CIR, "Facing centre", "Basic", "Who sits second to the left of the person who drinks Lassi?", ans,
         ["Faraz", "Bhavesh", "Eesha"], "Facing the centre: the left is clockwise",
         "Chaitali drinks Lassi. Her left is clockwise: Faraz, then Dhaval.",
         [ARR, "Lassi: Chaitali", "Clockwise from Chaitali: Faraz, Dhaval"],
         why_others_wrong="Faraz is immediately to her left; Bhavesh is immediately to her right and Eesha second to "
                          "her right.", seconds=45)
stm = [("Eesha – Juice", drk["Eesha"] == "Juice"), ("Hemlata – Soup", drk["Hemlata"] == "Soup"),
       ("Faraz – Lassi", drk["Faraz"] == "Lassi"), ("Dhaval – Tea", drk["Dhaval"] == "Tea")]
t, f = one_true(stm)
puzzle_q(sid, CIR, "Facing centre", "Basic", "Which of the following person – drink pairs is correct?", t, f,
         "Reading an attribute off the final arrangement",
         "Bhavesh (Tea), Dhaval (Coffee), Hemlata (Milk), Faraz (Soup) and Chaitali (Lassi) are fixed, which leaves "
         "Juice for Eesha.", [ARR], seconds=40)

# ---- C2 Basic: square table, eight persons all facing the centre; even seats are corners, odd seats the middles
P = ["Kashish", "Lalitha", "Mukund", "Neelam", "Oorvi", "Parveen", "Raghu", "Sanjana"]
N = 8
corner = lambda s: s % 2 == 0
conds = [
    ("Kashish sits at one of the corners.", ("Kashish",), lambda k: corner(k)),
    ("Mukund sits opposite Kashish.", ("Mukund", "Kashish"), lambda m, k: m == (k + 4) % N),
    ("Neelam sits second to the right of Kashish.", ("Neelam", "Kashish"), lambda n, k: n == (k + 2) % N),
    ("Sanjana sits between Neelam and Mukund.", ("Sanjana", "Neelam", "Mukund"),
     lambda s, n, m: {(s - 1) % N, (s + 1) % N} == {n, m}),
    ("Lalitha sits immediately to the left of Kashish.", ("Lalitha", "Kashish"), lambda l, k: l == (k - 1) % N),
    ("Parveen sits at a corner.", ("Parveen",), lambda p: corner(p)),
    ("Oorvi is not an immediate neighbour of Kashish.", ("Oorvi", "Kashish"), lambda o, k: (o - k) % N not in (1, 7)),
]
C2 = unique(P, {p: range(N) for p in P} | {"Kashish": [0]}, conds, [P])
at = {v: k for k, v in C2.items()}
assert [at[i] for i in range(N)] == ["Kashish", "Raghu", "Neelam", "Sanjana", "Mukund", "Oorvi", "Parveen", "Lalitha"]
ARR = "Anticlockwise from Kashish (corner): " + ", ".join(
    f"{at[i]} ({'corner' if corner(i) else 'middle'})" for i in range(N))
sid = stimulus("puzzle", "Eight persons at a square table, all facing the centre",
               "Eight persons Kashish, Lalitha, Mukund, Neelam, Oorvi, Parveen, Raghu and Sanjana sit around a square "
               "table, all facing the centre. Four of them sit at the four corners and the other four at the middle "
               "of the four sides, so corner and middle seats alternate around the table.", conds,
               "Fix Kashish at a corner. Mukund is opposite her (also a corner) and Neelam two seats to her right (a "
               "corner). Sanjana sits between Neelam and Mukund, and Lalitha immediately to Kashish's left (a "
               "middle seat). The seats left are the middle seat to Kashish's right, the middle seat after Mukund and "
               "the corner after it. Parveen takes the corner. Oorvi cannot be next to Kashish, so Oorvi takes the "
               "middle seat after Mukund and Raghu the middle seat to Kashish's right.\n\n"
               + table(["Seat (anticlockwise from Kashish)", "Person", "Position"],
                       [(i, at[i], "corner" if corner(i) else "middle of a side") for i in range(N)]))
ans = at[(C2["Raghu"] + 4) % N]
assert ans == "Oorvi"
puzzle_q(sid, CIR, "Square and rectangular tables", "Basic", "Who sits opposite Raghu?", ans,
         ["Sanjana", "Parveen", "Lalitha"], "Opposite seats at a square table",
         "Raghu sits in the middle seat immediately to Kashish's right. Four seats on is the middle seat after "
         "Mukund: Oorvi.", [ARR, "Raghu = seat 1; opposite = seat 5 = Oorvi"],
         why_others_wrong="Sanjana and Lalitha are in middle seats but on the sides next to Raghu's side; Parveen sits "
                          "at a corner.", seconds=45)
k = (C2["Lalitha"] - C2["Sanjana"]) % N
between = [at[(C2["Lalitha"] - i) % N] for i in range(1, k)]
assert between == ["Parveen", "Oorvi", "Mukund"]
puzzle_q(sid, CIR, "Square and rectangular tables", "Basic",
         "How many persons sit between Lalitha and Sanjana when counted to the left of Lalitha?",
         num_word(len(between)), ["Two", "Four", "One"], "Facing the centre: the left is clockwise",
         "Lalitha faces the centre, so her left is clockwise: Parveen, Oorvi, Mukund and then Sanjana. Three persons "
         "sit between them.", [ARR, "Clockwise from Lalitha: Parveen, Oorvi, Mukund, Sanjana"],
         why_others_wrong="Two leaves out one of the three persons; Four counts Sanjana herself; One counts only Oorvi, "
                          "the one middle-seat person between them.", natural=by_num, seconds=50)
mids = [at[i] for i in range(N) if not corner(i)]
assert mids == ["Raghu", "Sanjana", "Oorvi", "Lalitha"]
puzzle_q(sid, CIR, "Square and rectangular tables", "Basic",
         "Which of the following groups of persons sit at the middle of the sides of the table?",
         "Raghu, Sanjana, Oorvi and Lalitha",
         ["Raghu, Neelam, Oorvi and Lalitha", "Kashish, Neelam, Mukund and Parveen", "Sanjana, Oorvi, Parveen and "
          "Lalitha"], "Corner and middle seats alternate",
         "Kashish, Neelam, Mukund and Parveen are at the corners, so the middle seats belong to Raghu, Sanjana, Oorvi "
         "and Lalitha.", [ARR], seconds=40)

# ---- C3 Intermediate (standalone): eight persons around a circle, all facing the centre
P = ["Abhay", "Bushra", "Cyril", "Daksha", "Elvin", "Feroze", "Gulshan", "Hansa"]
N = 8
conds = [
    ("Gulshan sits opposite Abhay.", ("Gulshan", "Abhay"), lambda g, a: g == (a + 4) % N),
    ("Hansa sits second to the right of Abhay.", ("Hansa", "Abhay"), lambda h, a: h == (a + 2) % N),
    ("Only two persons sit between Hansa and Feroze when counted to the left of Hansa.", ("Hansa", "Feroze"),
     lambda h, f_: (h - f_) % N == 3),
    ("Cyril sits immediately to the left of Gulshan.", ("Cyril", "Gulshan"), lambda c, g: c == (g - 1) % N),
    ("Elvin sits immediately to the right of Abhay.", ("Elvin", "Abhay"), lambda e, a: e == (a + 1) % N),
    ("Bushra is not an immediate neighbour of Feroze.", ("Bushra", "Feroze"), lambda b, f_: (b - f_) % N not in (1, 7)),
]
C3 = unique(P, {p: range(N) for p in P} | {"Abhay": [0]}, conds, [P])
at = {v: k for k, v in C3.items()}
assert [at[i] for i in range(N)] == ["Abhay", "Elvin", "Hansa", "Cyril", "Gulshan", "Bushra", "Daksha", "Feroze"]
x_ = at[(C3["Feroze"] + 2) % N]
ans = at[(C3[x_] - 3) % N]
assert x_ == "Elvin" and ans == "Daksha"
mcq(CIR, "Facing centre", "Intermediate",
    "Eight persons Abhay, Bushra, Cyril, Daksha, Elvin, Feroze, Gulshan and Hansa sit around a circular table, "
    "equally spaced and all facing the centre.\n" + bullets(conds) +
    "\n\nWho sits third to the left of the person who sits second to the right of Feroze?", ans,
    ["Bushra", "Abhay", "Hansa"], "Two-step position questions",
    "Number the seats anticlockwise from Abhay (0); facing the centre, right = anticlockwise. Gulshan = 4, Hansa = 2, "
    "Elvin = 1, Cyril = 3 (immediately to Gulshan's left, i.e. clockwise). Two persons between Hansa and Feroze on "
    "Hansa's left (clockwise: Elvin, Abhay) puts Feroze at 7. Bushra cannot be next to Feroze, so Bushra = 5 and "
    "Daksha = 6. Second to Feroze's right is Elvin (seat 1); third to Elvin's left (clockwise) is seat 6: Daksha.",
    ["Abhay 0, Elvin 1, Hansa 2, Gulshan 4, Cyril 3", "Clockwise from Hansa: Elvin, Abhay, then Feroze ⇒ Feroze 7",
     "Bushra not beside Feroze ⇒ Bushra 5, Daksha 6", "Second to the right of Feroze (7 + 2 = 1): Elvin",
     "Third to the left of Elvin (1 − 3 = 6): Daksha"],
    why_others_wrong="Bushra is third to the left of Abhay; Abhay is the person immediately to Elvin's left; Hansa is "
                     "immediately to Elvin's right.", seconds=75, verified_by=BRUTE)

# ---- C4 Intermediate (standalone): rectangular table with eight seats, three on each longer side and one at each
#      shorter side, all facing the centre. Seats 0..7 anticlockwise: 0 and 4 shorter sides; 1-3 and 5-7 longer sides;
#      across the table: 0-4, 1-7, 2-6, 3-5.
P = ["Jayant", "Kesari", "Leher", "Mitali", "Nayana", "Owais", "Pankhuri", "Ruchir"]
N = 8
SHORT = {0, 4}
across = lambda s: (8 - s) % N if s not in SHORT else (s + 4) % N
conds = [
    ("Jayant and Nayana sit at the two shorter sides.", ("Jayant", "Nayana"),
     lambda j, n: j in SHORT and n in SHORT),
    ("Mitali sits second to the right of Jayant.", ("Mitali", "Jayant"), lambda m, j: m == (j + 2) % N),
    ("Ruchir sits immediately to the right of Mitali.", ("Ruchir", "Mitali"), lambda r, m: r == (m + 1) % N),
    ("Kesari sits directly across the table from Mitali.", ("Kesari", "Mitali"), lambda k, m: k == across(m)),
    ("Owais sits immediately to the right of Nayana.", ("Owais", "Nayana"), lambda o, n: o == (n + 1) % N),
    ("Leher sits immediately to the right of Jayant.", ("Leher", "Jayant"), lambda l, j: l == (j + 1) % N),
]
C4 = unique(P, {p: range(N) for p in P} | {"Jayant": [0]}, conds, [P])
at = {v: k for k, v in C4.items()}
assert [at[i] for i in range(N)] == ["Jayant", "Leher", "Mitali", "Ruchir", "Nayana", "Owais", "Kesari", "Pankhuri"]
ans = at[across(C4["Owais"])]
assert ans == "Ruchir"
mcq(CIR, "Square and rectangular tables", "Intermediate",
    "Eight persons Jayant, Kesari, Leher, Mitali, Nayana, Owais, Pankhuri and Ruchir sit around a rectangular table, "
    "all facing the centre. One person sits at each of the two shorter sides and three persons sit along each of the "
    "two longer sides; each person on a longer side sits directly across the table from one person on the other "
    "longer side.\n" + bullets(conds) + "\n\nWho sits directly across the table from Owais?", ans,
    ["Leher", "Mitali", "Kesari"], "Rectangular table: 'across' pairs the seats of the two longer sides",
    "Going right (anticlockwise) from Jayant: Leher, Mitali and Ruchir fill the first longer side, then Nayana at the "
    "other shorter side, then Owais, Kesari and Pankhuri on the second longer side. Kesari is across from Mitali (the "
    "two middle seats). Owais is the first seat after Nayana, which is across from the last seat before Nayana: "
    "Ruchir.",
    ["Jayant (short side); Leher, Mitali, Ruchir on long side 1", "Nayana (other short side); Owais next to her",
     "Kesari across from Mitali (middle of long side 2); Pankhuri takes the last seat",
     "Across pairs: Leher–Pankhuri, Mitali–Kesari, Ruchir–Owais"],
    why_others_wrong="Leher is across from Pankhuri and Mitali from Kesari; Kesari sits beside Owais.", seconds=75,
    verified_by=BRUTE)

# ---- C5 Advanced: eight persons around a circle, some facing the centre (I) and some outside (O), with ages
P = ["Anvesha", "Bhairav", "Chandrika", "Dilnawaz", "Evan", "Ginni", "Hussain", "Ilina"]
N = 8
AG = [22, 26, 31, 35, 40, 44, 49, 53]
RC = lambda s, f, k: (s + (k if f == "I" else -k)) % N
F_ = ["f" + p for p in P]
A_ = ["a" + p for p in P]
VV = [x for p in P for x in (p, "f" + p, "a" + p)]
IXV = {v: i for i, v in enumerate(VV)}
conds = [
    ("Anvesha faces the centre, and Bhairav sits opposite her.", ("Anvesha", "fAnvesha", "Bhairav"),
     lambda a, fa, b: fa == "I" and b == (a + 4) % N),
    ("Chandrika faces the centre and sits second to the right of Anvesha.",
     ("Anvesha", "fAnvesha", "Chandrika", "fChandrika"), lambda a, fa, c, fc: fc == "I" and c == RC(a, fa, 2)),
    ("Hussain, the youngest of the eight, sits between Anvesha and Chandrika and faces outside.",
     ("Anvesha", "Chandrika", "Hussain", "fHussain", "aHussain"),
     lambda a, c, h, fh, ah: fh == "O" and ah == 22 and {(h - 1) % N, (h + 1) % N} == {a, c}),
    ("Evan sits immediately to the right of Chandrika.", ("Chandrika", "fChandrika", "Evan"),
     lambda c, fc, e: e == RC(c, fc, 1)),
    ("Ilina sits second to the left of Evan.", ("Evan", "fEvan", "Ilina"), lambda e, fe, i: i == RC(e, fe, -2)),
    ("Dilnawaz sits immediately to the right of Ilina.", ("Ilina", "fIlina", "Dilnawaz"),
     lambda i, fi, d: d == RC(i, fi, 1)),
    ("Bhairav is 4 years older than Hussain.", ("aBhairav", "aHussain"), lambda b, h: b == h + 4),
    ("The oldest person sits second to the right of Anvesha.", tuple(VV),
     lambda *v: v[IXV["a" + next(p for p in P if v[IXV[p]] == RC(v[IXV["Anvesha"]], v[IXV["fAnvesha"]], 2))]] == 53),
    ("Only two persons are older than Ilina.", ("aIlina",), lambda a: a == 44),
    ("Ginni is older than Anvesha.", ("aGinni", "aAnvesha"), lambda g, a: g > a),
    ("Evan is younger than Dilnawaz, and Dilnawaz is younger than Anvesha.", ("aEvan", "aDilnawaz", "aAnvesha"),
     lambda e, d, a: e < d < a),
    ("Exactly four persons face the centre.", tuple(F_), lambda *f_: f_.count("I") == 4),
    ("Dilnawaz and Ginni face the same direction.", ("fDilnawaz", "fGinni"), lambda a, b: a == b),
]
dom = {p: range(N) for p in P} | {"Anvesha": [0]} | {f: "IO" for f in F_} | {a: AG for a in A_}
C5 = unique(VV, dom, conds, [P, A_])
at = {C5[p]: p for p in P}
fc = {p: C5["f" + p] for p in P}
ag = {p: C5["a" + p] for p in P}
rt = lambda p, k: at[RC(C5[p], fc[p], k)]
assert [(at[i], fc[at[i]], ag[at[i]]) for i in range(N)] == [
    ("Anvesha", "I", 40), ("Hussain", "O", 22), ("Chandrika", "I", 53), ("Evan", "O", 31), ("Bhairav", "I", 26),
    ("Ilina", "I", 44), ("Dilnawaz", "O", 35), ("Ginni", "O", 49)]
FCN = {"I": "centre", "O": "outside"}
ARR = "Anticlockwise from Anvesha: " + ", ".join(f"{at[i]} ({FCN[fc[at[i]]]}, {ag[at[i]]})" for i in range(N))
sid = stimulus("puzzle", "Eight persons around a circle, with ages and mixed facing",
               "Eight persons Anvesha, Bhairav, Chandrika, Dilnawaz, Evan, Ginni, Hussain and Ilina sit around a "
               "circular table, equally spaced. Some of them face the centre and the others face outside. (For a "
               "person facing the centre the right is anticlockwise; for a person facing outside the right is "
               "clockwise.) Their ages are 22, 26, 31, 35, 40, 44, 49 and 53 years, one age each.", conds,
               "Fix Anvesha (facing the centre); Bhairav is opposite her and Chandrika two seats anticlockwise, with "
               "Hussain (22, facing outside) between them. Chandrika faces the centre, so Evan is the next seat "
               "anticlockwise. If Evan faced the centre, second to his left (clockwise) would be Chandrika's seat, so "
               "Evan faces outside and Ilina sits two seats anticlockwise from him, next to Bhairav. If Ilina faced "
               "outside, the seat to her right would be Bhairav's, so Ilina faces the centre and Dilnawaz sits next "
               "to her; Ginni takes the last seat, beside Anvesha. Anvesha, Chandrika and Ilina face the centre; "
               "exactly one more does, and Dilnawaz and Ginni face the same way, so both face outside and Bhairav "
               "faces the centre. Ages: Bhairav 26, Chandrika (second to Anvesha's right) 53, Ilina 44. Ginni, "
               "Anvesha, Dilnawaz and Evan share 31, 35, 40 and 49 with Ginni > Anvesha > Dilnawaz > Evan.\n\n"
               + table(["Seat (anticlockwise from Anvesha)", "Person", "Faces", "Age"],
                       [(i, at[i], FCN[fc[at[i]]], ag[at[i]]) for i in range(N)]))
ans = rt("Dilnawaz", -2)
assert ans == "Anvesha"
puzzle_q(sid, CIR, "Facing inside and outside", "Advanced", "Who sits second to the left of Dilnawaz?", ans,
         ["Ilina", "Bhairav", "Ginni"], "Facing outside: the left is anticlockwise",
         "Dilnawaz faces outside, so her left is anticlockwise: Ginni, then Anvesha.",
         [ARR, "Dilnawaz faces outside ⇒ left = anticlockwise", "Anticlockwise from Dilnawaz: Ginni, Anvesha"],
         why_others_wrong="Ilina and Bhairav are first and second to Dilnawaz's right; Ginni is immediately to her "
                          "left.", seconds=90)
ans = ag[rt("Bhairav", 1)]
assert ans == 44
puzzle_q(sid, CIR, "Facing inside and outside", "Advanced",
         "What is the age of the person who sits immediately to the right of Bhairav?", f"{ans} years",
         ["31 years", "35 years", "49 years"], "Combining position and attribute",
         "Bhairav faces the centre, so his right is anticlockwise: Ilina, aged 44.",
         [ARR, "Bhairav faces the centre ⇒ right = anticlockwise ⇒ Ilina", "Ilina: only Chandrika (53) and Ginni (49) "
          "are older ⇒ 44"], natural=lambda t: int(t.split()[0]), seconds=90)
outs = [p for p in P if fc[p] == "O"]
assert outs == ["Dilnawaz", "Evan", "Ginni", "Hussain"]
puzzle_q(sid, CIR, "Facing inside and outside", "Advanced", "Which of the following groups of persons face outside?",
         "Dilnawaz, Evan, Ginni and Hussain",
         ["Bhairav, Evan, Ginni and Hussain", "Dilnawaz, Evan, Ilina and Hussain", "Chandrika, Dilnawaz, Ginni and "
          "Hussain"], "Deducing facing directions from 'right/left' clues",
         "Hussain faces outside (given). Evan must face outside (else Ilina would land on Chandrika's seat). Ilina must "
         "face the centre (else Dilnawaz would land on Bhairav's seat). With exactly four facing the centre and "
         "Dilnawaz and Ginni facing the same way, both face outside.", [ARR], seconds=100)
x_ = next(p for p in P if ag[p] == 35)
ans = at[(C5[x_] + 4) % N]
assert x_ == "Dilnawaz" and ans == "Chandrika"
puzzle_q(sid, CIR, "Facing inside and outside", "Advanced", "Who sits opposite the person who is 35 years old?", ans,
         ["Hussain", "Evan", "Anvesha"], "Ages first, then the seat",
         "Ginni > Anvesha > Dilnawaz > Evan with the ages 49, 40, 35, 31, so Dilnawaz is 35. Opposite Dilnawaz is "
         "Chandrika.", [ARR, "Dilnawaz = 35", "Opposite Dilnawaz (seat 6): seat 2 = Chandrika"],
         why_others_wrong="Hussain is opposite Ilina, Evan opposite Ginni and Anvesha opposite Bhairav.", seconds=95)

# ---- C6 Advanced: a circle with an unknown number of persons, all facing the centre (positions anticlockwise from
#      Jharna; right = +1)
P = ["Jharna", "Kuber", "Lajwanti", "Mrinal", "Nishit", "Paromita"]
V = ["n"] + P
conds = [
    ("Kuber sits third to the right of Jharna.", ("n", "Jharna", "Kuber"), lambda n, j, k: k == (j + 3) % n),
    ("Only five persons sit between Jharna and Kuber when counted to the left of Jharna.", ("n", "Jharna", "Kuber"),
     lambda n, j, k: (j - k) % n - 1 == 5),
    ("Lajwanti sits second to the left of Kuber.", ("n", "Lajwanti", "Kuber"), lambda n, l, k: l == (k - 2) % n),
    ("Only two persons sit between Mrinal and Kuber.", ("n", "Mrinal", "Kuber"),
     lambda n, m, k: (m - k) % n - 1 == 2 or (k - m) % n - 1 == 2),
    ("Nishit sits immediately to the left of Jharna.", ("n", "Nishit", "Jharna"), lambda n, x, j: x == (j - 1) % n),
    ("Paromita sits immediately to the right of Kuber.", ("n", "Paromita", "Kuber"), lambda n, p, k: p == (k + 1) % n),
]
cfull = [("", ("n",) + tuple(P), lambda n, *v: max(v) < n)] + conds
sols = solve(V, {"n": range(6, 25)} | {p: range(0, 25) for p in P} | {"Jharna": [0]},
             [(vs, fn) for _, vs, fn in cfull], [P])
assert len(sols) == 1
C6 = sols[0]
N6 = C6["n"]
at = {C6[p]: p for p in P}
assert N6 == 9 and [C6[p] for p in P] == [0, 3, 1, 6, 8, 4]
seat = lambda s: at.get(s % N6, "an unnamed person")
ARR = f"{N6} persons; anticlockwise from Jharna: " + ", ".join(seat(i) for i in range(N6))
sid = stimulus("puzzle", "A circle of unknown size",
               "Some persons sit around a circular table, equally spaced and all facing the centre. The number of "
               "persons is not given. Jharna, Kuber, Lajwanti, Mrinal, Nishit and Paromita are among them; the others "
               "are not named.", conds,
               "Count positions anticlockwise (to the right) from Jharna = 0. Kuber = 3, with two persons between them "
               "on Jharna's right. Five persons sit between them on Jharna's left, so the circle has 2 + 5 + 2 = 9 "
               "persons. Lajwanti = 3 − 2 = 1, Paromita = 4 and Nishit = 8 (immediately to Jharna's left). Mrinal is "
               "three places from Kuber: 6 or 0; 0 is Jharna, so Mrinal = 6. Positions 2, 5 and 7 hold unnamed "
               "persons.\n\n" + table(["Position (anticlockwise from Jharna)", "Person"],
                                     [(i, seat(i)) for i in range(N6)]))
puzzle_q(sid, CIR, "Facing centre", "Advanced", "How many persons sit around the table?", str(N6),
         ["8", "10", "11"], "Total = persons between on both sides + the two persons themselves",
         "Between Jharna and Kuber there are two persons on one side (Kuber is third to her right) and five on the "
         f"other, so the circle has 2 + 5 + 2 = {N6} persons.",
         ["Right side: Kuber third to the right ⇒ 2 persons between", "Left side: 5 persons between",
          f"Total = 2 + 5 + 2 = {N6}"],
         why_others_wrong="8 forgets one of the two named persons; 10 and 11 count the between-persons as positions.",
         natural=int, seconds=80)
k = (C6["Mrinal"] - C6["Lajwanti"]) % N6
cnt = k - 1
assert cnt == 4
puzzle_q(sid, CIR, "Facing centre", "Advanced",
         "How many persons sit between Lajwanti and Mrinal when counted to the right of Lajwanti?", num_word(cnt),
         ["Three", "Five", "Two"], "Counting in a circle of known size",
         "Going right (anticlockwise) from Lajwanti (1): an unnamed person (2), Kuber (3), Paromita (4), an unnamed "
         "person (5), then Mrinal (6). Four persons sit between them.",
         [ARR, "Positions 2 to 5 lie between Lajwanti (1) and Mrinal (6)"], natural=by_num, seconds=80)
ans = seat(C6["Paromita"] - 4)
assert ans == "Jharna"
puzzle_q(sid, CIR, "Facing centre", "Advanced", "Who sits fourth to the left of Paromita?", ans,
         ["Lajwanti", "Nishit", "Mrinal"], "Facing the centre: the left is clockwise",
         "Paromita is at position 4; four places to her left (clockwise) is position 0: Jharna.",
         [ARR, "4 − 4 = 0 ⇒ Jharna"],
         why_others_wrong="Lajwanti is third to Paromita's left and Nishit fifth; Mrinal is second to her right.",
         seconds=80)
rel = next(f"{['Immediately', 'Second', 'Third'][kk - 1]} to the {sd}" for kk in (1, 2, 3)
           for sd, sg in (("right", 1), ("left", -1)) if seat(C6["Mrinal"] + sg * kk) == "Nishit")
assert rel == "Second to the right"
puzzle_q(sid, CIR, "Facing centre", "Advanced", "What is the position of Nishit with respect to Mrinal?", rel,
         ["Second to the left", "Third to the right", "Immediately to the right"],
         "Relative position in a circle of nine",
         "Mrinal is at 6 and Nishit at 8: two places anticlockwise, i.e. second to Mrinal's right.",
         [ARR, "From Mrinal (6), right = anticlockwise: 7 (unnamed), 8 (Nishit)"],
         why_others_wrong="Going left (clockwise) from Mrinal, Nishit is seventh, not second.", seconds=75)

# ================================================================================================ FLOOR PUZZLES
FLR = "Floor-Based Puzzles"

# ---- F1 Basic (standalone): floors numbered from the TOP (floor 1 is the topmost)
P = ["Gopika", "Harmeet", "Kanha", "Laxmi", "Tejal"]
conds = [("Kanha lives on floor 4.", ("Kanha",), lambda k: k == 4),
         ("Tejal lives on the floor immediately above Kanha's floor.", ("Tejal", "Kanha"), lambda t, k: t == k - 1),
         ("Only one person lives between Tejal and Gopika.", ("Tejal", "Gopika"), lambda t, g: abs(t - g) == 2),
         ("Gopika lives below Kanha.", ("Gopika", "Kanha"), lambda g, k: g > k),
         ("Laxmi lives above Harmeet.", ("Laxmi", "Harmeet"), lambda l, h: l < h)]
F1 = unique(P, {p: range(1, 6) for p in P}, conds, [P])
at = {v: k for k, v in F1.items()}
assert [at[i] for i in range(1, 6)] == ["Laxmi", "Harmeet", "Tejal", "Kanha", "Gopika"]
mcq(FLR, "Floor and flat", "Basic",
    "Five persons Gopika, Harmeet, Kanha, Laxmi and Tejal live on the five floors of a building, one on each floor. "
    "The floors are numbered from the top: floor 1 is the topmost floor and floor 5 the lowermost.\n" + bullets(conds)
    + "\n\nWho lives on floor 2?", at[2], ["Tejal", "Laxmi", "Kanha"],
    "Read the numbering: here a smaller floor number is higher up",
    "Floor 1 is the top. Kanha = 4 and Tejal, immediately above, = 3. Gopika is two floors from Tejal and below "
    "Kanha, so Gopika = 5. Floors 1 and 2 remain; Laxmi lives above Harmeet, so Laxmi = 1 and Harmeet = 2.",
    ["Kanha 4; 'immediately above' means one number smaller ⇒ Tejal 3", "Gopika = 3 ± 2 and below Kanha ⇒ 5",
     "Laxmi above Harmeet ⇒ Laxmi 1 (top), Harmeet 2"],
    why_others_wrong="Tejal is on floor 3; Laxmi on floor 1; Kanha on floor 4. Reading floor 1 as the bottom would "
                     "reverse the order.", seconds=40, verified_by=BRUTE)

# ---- F2 Basic (standalone): five floors with pets (floor 1 is the lowermost)
P = ["Darsh", "Elakshi", "Mahima", "Rudraksh", "Saket"]
PETS = ["Cat", "Dog", "Fish", "Parrot", "Rabbit"]
T_ = ["t" + p for p in P]
VV = P + T_
IXV = {v: i for i, v in enumerate(VV)}
fl_of = lambda v, pet: next(v[IXV[p]] for p in P if v[IXV["t" + p]] == pet)
conds = [("Rudraksh lives on the topmost floor and owns the Parrot.", ("Rudraksh", "tRudraksh"),
          lambda r, t: r == 5 and t == "Parrot"),
         ("Only one person lives between Rudraksh and Darsh.", ("Rudraksh", "Darsh"), lambda r, d: abs(r - d) == 2),
         ("Elakshi lives immediately above Darsh.", ("Elakshi", "Darsh"), lambda e, d: e == d + 1),
         ("Mahima lives below Saket.", ("Mahima", "Saket"), lambda m, s: m < s),
         ("The person who owns the Cat lives on floor 3.", tuple(VV), lambda *v: fl_of(v, "Cat") == 3),
         ("The person who owns the Dog lives immediately above the person who owns the Fish.", tuple(VV),
          lambda *v: fl_of(v, "Dog") == fl_of(v, "Fish") + 1)]
F2 = unique(VV, {p: range(1, 6) for p in P} | {t: PETS for t in T_}, conds, [P, T_])
assert [(p, F2[p], F2["t" + p]) for p in sorted(P, key=F2.get)] == [
    ("Mahima", 1, "Fish"), ("Saket", 2, "Dog"), ("Darsh", 3, "Cat"), ("Elakshi", 4, "Rabbit"),
    ("Rudraksh", 5, "Parrot")]
ans = next(p for p in P if F2["t" + p] == "Rabbit")
mcq(FLR, "Floor with attribute", "Basic",
    "Five persons Darsh, Elakshi, Mahima, Rudraksh and Saket live on the five floors of a building, one on each floor "
    "(floor 1 is the lowermost). Each owns a different pet among Cat, Dog, Fish, Parrot and Rabbit.\n"
    + bullets(conds) + "\n\nWho owns the Rabbit?", ans, ["Darsh", "Saket", "Mahima"],
    "Floors first, then the attribute",
    "Rudraksh = 5, so Darsh = 3 and Elakshi = 4; Mahima below Saket gives Mahima = 1 and Saket = 2. Darsh (floor 3) "
    "owns the Cat. The Dog–Fish pair needs two adjacent floors without the Cat or the Parrot: floors 2 and 1, so "
    "Saket owns the Dog and Mahima the Fish. Elakshi owns the Rabbit.",
    ["Rudraksh 5 (Parrot) ⇒ Darsh 3, Elakshi 4", "Mahima 1, Saket 2", "Cat on floor 3 = Darsh",
     "Dog immediately above Fish: only floors 2–1 are free of Cat and Parrot ⇒ Saket Dog, Mahima Fish",
     "Remaining: Elakshi – Rabbit"],
    why_others_wrong="Darsh owns the Cat, Saket the Dog and Mahima the Fish.", seconds=50, verified_by=BRUTE)

# ---- F3 Intermediate: ground floor 0 to floor 6, seven persons, seven cities
P = ["Bilal", "Chhaya", "Damodar", "Esther", "Gurleen", "Harsha", "Jeevika"]
CT = ["Agra", "Bhopal", "Kochi", "Nagpur", "Patna", "Surat", "Thane"]
K_ = ["c" + p for p in P]
VV = P + K_
IXV = {v: i for i, v in enumerate(VV)}
fl_of = lambda v, c: next(v[IXV[p]] for p in P if v[IXV["c" + p]] == c)
conds = [
    ("Damodar lives on floor 3 and works in Patna.", ("Damodar", "cDamodar"), lambda d, c: d == 3 and c == "Patna"),
    ("Only two persons live between Damodar and the person who works in Kochi, who lives above Damodar.",
     tuple(VV), lambda *v: fl_of(v, "Kochi") == v[IXV["Damodar"]] + 3),
    ("Esther works in Kochi.", ("cEsther",), lambda c: c == "Kochi"),
    ("Harsha lives on the ground floor.", ("Harsha",), lambda h: h == 0),
    ("The person who works in Surat lives immediately below Esther.", tuple(VV),
     lambda *v: fl_of(v, "Surat") == v[IXV["Esther"]] - 1),
    ("Bilal and Chhaya live on odd-numbered floors, and Bilal lives above Chhaya.", ("Bilal", "Chhaya"),
     lambda b, c: b % 2 == 1 and c % 2 == 1 and b > c),
    ("Gurleen lives immediately above the person who works in Bhopal.", tuple(VV),
     lambda *v: v[IXV["Gurleen"]] == fl_of(v, "Bhopal") + 1),
    ("The person who works in Thane lives between Chhaya and Damodar.", tuple(VV),
     lambda *v: min(v[IXV["Chhaya"]], v[IXV["Damodar"]]) < fl_of(v, "Thane") < max(v[IXV["Chhaya"]],
                                                                                    v[IXV["Damodar"]])),
    ("Jeevika does not work in Nagpur.", ("cJeevika",), lambda c: c != "Nagpur"),
]
F3 = unique(VV, {p: range(0, 7) for p in P} | {k: CT for k in K_}, conds, [P, K_])
at = {F3[p]: p for p in P}
cty = {p: F3["c" + p] for p in P}
assert [(at[i], cty[at[i]]) for i in range(7)] == [
    ("Harsha", "Nagpur"), ("Chhaya", "Bhopal"), ("Gurleen", "Thane"), ("Damodar", "Patna"), ("Jeevika", "Agra"),
    ("Bilal", "Surat"), ("Esther", "Kochi")]
ARR = "Ground floor (0) to floor 6: " + ", ".join(f"{at[i]} ({cty[at[i]]})" for i in range(7))
sid = stimulus("puzzle", "Seven persons from the ground floor up",
               "Seven persons Bilal, Chhaya, Damodar, Esther, Gurleen, Harsha and Jeevika live in a building that has a "
               "ground floor and six floors above it. The ground floor is numbered 0 and the topmost floor 6; one "
               "person lives on each floor. Each person works in a different city among Agra, Bhopal, Kochi, Nagpur, "
               "Patna, Surat and Thane.", conds,
               "Damodar = 3 (Patna); the Kochi worker, Esther, lives three floors higher: 6. The Surat worker lives "
               "on floor 5. Harsha = 0. Bilal and Chhaya take odd floors other than 3 with Bilal higher: Bilal = 5 "
               "(Surat) and Chhaya = 1. Floors 2 and 4 remain for Gurleen and Jeevika. Gurleen is immediately above "
               "the Bhopal worker: Gurleen = 4 would make Damodar (Patna) the Bhopal worker, so Gurleen = 2, Chhaya "
               "works in Bhopal and Jeevika = 4. The Thane worker lives between Chhaya (1) and Damodar (3): Gurleen. "
               "Jeevika does not work in Nagpur, so Jeevika works in Agra and Harsha in Nagpur.\n\n"
               + table(["Floor", "Person", "City"], [(i, at[i], cty[at[i]]) for i in range(6, -1, -1)]))
x_ = next(p for p in P if cty[p] == "Agra")
ans = at[F3[x_] + 1]
assert ans == "Bilal"
puzzle_q(sid, FLR, "Floor with attribute", "Intermediate",
         "Who lives on the floor immediately above the person who works in Agra?", ans,
         ["Damodar", "Esther", "Gurleen"], "Locate the attribute, then move one floor",
         "Jeevika works in Agra and lives on floor 4; floor 5 is Bilal's.", [ARR, "Agra: Jeevika (4) ⇒ floor 5: Bilal"],
         why_others_wrong="Damodar lives immediately below Jeevika; Esther is two floors above her; Gurleen is on "
                          "floor 2.", seconds=70)
nb = (at[F3["Damodar"] - 1], at[F3["Damodar"] + 1])
assert nb == ("Gurleen", "Jeevika")
puzzle_q(sid, FLR, "Floor with attribute", "Intermediate",
         "Which two persons live on the floors immediately below and immediately above Damodar's floor, "
         "respectively?", "Gurleen and Jeevika", ["Chhaya and Bilal", "Jeevika and Gurleen", "Gurleen and Bilal"],
         "Neighbouring floors of a fixed person",
         "Damodar lives on floor 3. Floor 2 is Gurleen's (she is immediately above the Bhopal worker, Chhaya) and "
         "floor 4 is Jeevika's.", [ARR, "Floor 2: Gurleen; floor 4: Jeevika"],
         why_others_wrong="'Jeevika and Gurleen' reverses the order asked; Chhaya is on floor 1 and Bilal on floor 5.",
         seconds=60)
ans = cty["Harsha"]
assert ans == "Nagpur"
puzzle_q(sid, FLR, "Floor with attribute", "Intermediate", "In which city does Harsha work?", ans,
         ["Agra", "Bhopal", "Thane"], "Elimination of the last attribute",
         "Patna, Kochi, Surat, Bhopal and Thane belong to Damodar, Esther, Bilal, Chhaya and Gurleen. Of Agra and "
         "Nagpur, Jeevika cannot take Nagpur, so Harsha works in Nagpur.", [ARR], seconds=60)
stm = [("Gurleen lives on floor 2", F3["Gurleen"] == 2),
       ("Chhaya works in Thane", cty["Chhaya"] == "Thane"),
       ("Bilal lives immediately above Damodar", F3["Bilal"] == F3["Damodar"] + 1),
       ("Two persons live between Esther and Jeevika", abs(F3["Esther"] - F3["Jeevika"]) - 1 == 2)]
t, f = one_true(stm)
puzzle_q(sid, FLR, "Floor with attribute", "Intermediate", "Which of the following statements is true?", t, f,
         "Checking statements against the final arrangement",
         "Gurleen lives on floor 2. Chhaya works in Bhopal, Jeevika (not Bilal) lives immediately above Damodar, and "
         "only Bilal lives between Esther and Jeevika.", [ARR], seconds=60)

# ---- F4 Intermediate: eight persons on four floors, two on each floor (floor 1 is the lowermost)
P = ["Kavita", "Manish", "Natasha", "Pallav", "Ronak", "Shalini", "Uttam", "Vibha"]
IX = {p: i for i, p in enumerate(P)}
conds = [
    ("Kavita lives on an odd-numbered floor, and Ronak lives on the floor immediately below Kavita's floor.",
     ("Kavita", "Ronak"), lambda k, r: k % 2 == 1 and r == k - 1),
    ("Manish lives on the topmost floor.", ("Manish",), lambda m: m == 4),
    ("Natasha lives on the same floor as Ronak.", ("Natasha", "Ronak"), lambda n, r: n == r),
    ("Pallav lives on a floor below Natasha's floor.", ("Pallav", "Natasha"), lambda p, n: p < n),
    ("Shalini lives neither on Kavita's floor nor on Manish's floor.", ("Shalini", "Kavita", "Manish"),
     lambda s, k, m: s not in (k, m)),
    ("Uttam lives on a floor above Shalini's floor but below Vibha's floor.", ("Uttam", "Shalini", "Vibha"),
     lambda u, s, v: s < u < v),
    ("Exactly two persons live on each floor.", tuple(P), lambda *v: all(v.count(f_) == 2 for f_ in range(1, 5))),
]
F4 = unique(P, {p: range(1, 5) for p in P}, conds)
FL = {f_: sorted(p for p in P if F4[p] == f_) for f_ in range(1, 5)}
assert FL == {1: ["Pallav", "Shalini"], 2: ["Natasha", "Ronak"], 3: ["Kavita", "Uttam"], 4: ["Manish", "Vibha"]}
ARR = "; ".join(f"Floor {f_}: {' and '.join(FL[f_])}" for f_ in range(4, 0, -1))
sid = stimulus("puzzle", "Eight persons, two on each of four floors",
               "Eight persons Kavita, Manish, Natasha, Pallav, Ronak, Shalini, Uttam and Vibha live in a four-storey "
               "building, two persons on each floor. Floor 1 is the lowermost and floor 4 the topmost.", conds,
               "Kavita is on an odd floor with Ronak one floor below, so Kavita = 3 and Ronak = 2 (Kavita = 1 leaves "
               "no floor below). Manish = 4. Natasha joins Ronak on floor 2, which is now full, and Pallav lives below "
               "it: floor 1. Shalini avoids floors 3 and 4, so she is on floor 1. Uttam lives between Shalini and "
               "Vibha: one place is left on floor 3 and one on floor 4, so Uttam = 3 and Vibha = 4.\n\n"
               + table(["Floor", "Persons"], [(f_, " and ".join(FL[f_])) for f_ in range(4, 0, -1)]))
FQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, FLR, "Floor and flat", "Intermediate", text, correct, wrongs, concept, expl, steps, **kw)
ans = next(p for p in FL[F4["Uttam"]] if p != "Uttam")
assert ans == "Kavita"
FQ("Who lives on the same floor as Uttam?", ans, ["Vibha", "Ronak", "Manish"], "Floors that hold two persons",
   "Floor 3 has room for one person besides Kavita, and Uttam must be above Shalini (floor 1) and below Vibha, so he "
   "is on floor 3 with Kavita.", [ARR], why_others_wrong="Vibha and Manish share floor 4; Ronak is on floor 2.",
   seconds=60)
FQ("On which floor does Natasha live?", f"Floor {F4['Natasha']}", ["Floor 1", "Floor 3", "Floor 4"],
   "Same-floor clue", "Natasha lives on Ronak's floor, and Ronak is one floor below Kavita (floor 3): floor 2.",
   [ARR], natural=lambda t: int(t.split()[1]), seconds=50)
lowr = [p for p in P if F4[p] == F4["Manish"] - 1]
assert lowr == ["Kavita", "Uttam"]
FQ("Which of the following persons lives on the floor immediately below Manish's floor?", "Uttam",
   ["Vibha", "Natasha", "Pallav"], "Floors holding two persons each",
   "Manish is on the top floor, 4. Floor 3 holds Kavita and Uttam, so Uttam is the one listed.",
   [ARR, "Floor 3: Kavita and Uttam"],
   why_others_wrong="Vibha shares Manish's floor; Natasha is on floor 2 and Pallav on floor 1.", seconds=50)
FQ("Which two persons live on floor 1?", " and ".join(FL[1]),
   ["Pallav and Natasha", "Shalini and Uttam", "Ronak and Shalini"], "Elimination",
   "Pallav must be below Natasha (floor 2), and Shalini avoids floors 3 and 4 while floor 2 is full: both are on "
   "floor 1.", [ARR], seconds=55)

# ---- F5 Advanced: a building with an unknown number of floors, one person on each floor (floor 1 = lowermost)
P = ["Aarush", "Bhoomika", "Chakor", "Devika", "Ekansh", "Fiona"]
V = ["n"] + P
conds = [
    ("Chakor lives on floor 4.", ("Chakor",), lambda c: c == 4),
    ("Only three persons live between Chakor and Devika, and Devika lives above Chakor.", ("Devika", "Chakor"),
     lambda d, c: d == c + 4),
    ("Aarush lives on the topmost floor, and only five persons live between Aarush and Devika.",
     ("n", "Aarush", "Devika"), lambda n, a, d: a == n and abs(a - d) == 6),
    ("Ekansh lives exactly midway between Chakor and Aarush.", ("Ekansh", "Chakor", "Aarush"),
     lambda e, c, a: 2 * e == c + a),
    ("Fiona lives as many floors below Chakor as Ekansh lives above Devika.", ("Fiona", "Chakor", "Ekansh", "Devika"),
     lambda f_, c, e, d: c - f_ == e - d and f_ < c),
    ("Only two persons live between Bhoomika and Aarush.", ("Bhoomika", "Aarush"), lambda b, a: abs(a - b) == 3),
]
cfull = conds + [("", tuple(V), lambda n, *v: max(v) <= n)]
F5 = unique(V, {"n": range(6, 41)} | {p: range(1, 41) for p in P}, cfull, [P])
NF = F5["n"]
assert NF == 14 and [F5[p] for p in P] == [14, 11, 4, 8, 9, 3]
ARR = f"{NF} floors; " + ", ".join(f"{p} {F5[p]}" for p in sorted(P, key=F5.get)) + " (others unnamed)"
sid = stimulus("puzzle", "A building of unknown height",
               "Some persons live in a building, one person on each floor; every floor is occupied. Floor 1 is the "
               "lowermost. The number of floors is not given. Aarush, Bhoomika, Chakor, Devika, Ekansh and Fiona live "
               "in the building; the other residents are not named.", conds,
               "Chakor = 4, so Devika = 8. Aarush is six floors from Devika and lives on the top floor, so Aarush = "
               "14 (2 is below Devika and cannot be the top): the building has 14 floors. Ekansh = (4 + 14) ÷ 2 = 9, "
               "one floor above Devika, so Fiona is one floor below Chakor: 3. Bhoomika is three floors from Aarush: "
               "11.\n\n" + table(["Floor", "Person"], [(F5[p], p) for p in sorted(P, key=F5.get, reverse=True)]))
puzzle_q(sid, FLR, "Floor and flat", "Advanced", "How many floors does the building have?", str(NF),
         ["12", "13", "15"], "Fixing the height from a 'topmost' clue",
         "Devika = 8 and Aarush, six floors away on the topmost floor, = 14, so the building has 14 floors.",
         ["Chakor 4 ⇒ Devika 4 + 4 = 8", "Aarush = 8 ± 6 and on top ⇒ 14", "Top floor = 14 ⇒ 14 floors"],
         why_others_wrong="12 and 13 drop the 'five persons between' count by one or two; 15 counts an extra floor.",
         natural=int, seconds=90)
gap = F5["Ekansh"] - F5["Fiona"] - 1
assert gap == 5
puzzle_q(sid, FLR, "Floor and flat", "Advanced", "How many persons live between Fiona and Ekansh?", num_word(gap),
         ["Four", "Six", "Three"], "Every floor is occupied, so persons between = floors between",
         "Ekansh = 9 (midway between 4 and 14) and Fiona = 3 (as far below Chakor as Ekansh is above Devika, i.e. one "
         "floor). Floors 4 to 8 lie between them: five persons.",
         [ARR, "Ekansh 9; Ekansh − Devika = 1 ⇒ Fiona = 4 − 1 = 3", "Between 3 and 9: floors 4–8 ⇒ 5"],
         natural=by_num, seconds=90)
puzzle_q(sid, FLR, "Floor and flat", "Advanced", "On which floor does Bhoomika live?", f"Floor {F5['Bhoomika']}",
         ["Floor 10", "Floor 12", "Floor 17"], "Distance from the top floor",
         "Two persons live between Bhoomika and Aarush (floor 14), so Bhoomika is three floors away: 11 (17 is above "
         "the top floor).", [ARR, "14 − 3 = 11"], natural=lambda t: int(t.split()[1]), seconds=80)

# ================================================================================================ BOX PUZZLES
BOX = "Box-Based Puzzles"

# ---- X1 Basic (standalone): five boxes in one stack (position 1 = bottom)
P = ["F", "J", "O", "T", "Z"]
conds = [("Box F is at the top of the stack.", ("F",), lambda f_: f_ == 5),
         ("Box T is placed immediately above box O.", ("T", "O"), lambda t, o: t == o + 1),
         ("Only one box is placed between box T and box Z.", ("T", "Z"), lambda t, z: abs(t - z) == 2),
         ("Box J is placed below box O.", ("J", "O"), lambda j, o: j < o)]
X1 = unique(P, {p: range(1, 6) for p in P}, conds, [P])
at = {v: k for k, v in X1.items()}
assert [at[i] for i in range(1, 6)] == ["J", "Z", "O", "T", "F"]
ans = at[X1["O"] - 1]
mcq(BOX, "Stacked boxes", "Basic",
    "Five boxes F, J, O, T and Z are kept one above another in a single stack. Position 1 is the bottom and position "
    "5 the top.\n" + bullets(conds) + "\n\nWhich box is kept immediately below box O?", f"Box {ans}",
    ["Box J", "Box T", "Box F"], "Placing a linked pair in a short stack",
    "F = 5. The pair O–T (T just above O) can sit at 1–2, 2–3 or 3–4. At 1–2, J could not be below O. At 2–3, Z "
    "would be at 1 or 5; 5 is F's and 1 leaves no place below O for J. So O = 3, T = 4, Z = 2 and J = 1. Below O is "
    "Z.", ["F at 5", "O–T at 3–4 is the only placement that fits Z (two from T) and J (below O)",
           "Bottom to top: J, Z, O, T, F"],
    why_others_wrong="J is at the bottom, two places below O; T is above O; F is at the top.", seconds=45,
    verified_by=BRUTE)

# ---- X2 Intermediate: nine boxes in three stacks of three (Left = 1, Middle = 2, Right = 3; level 1 = bottom)
P = ["B", "D", "G", "K", "M", "P", "S", "V", "X"]
SEATS = [s * 10 + l for s in (1, 2, 3) for l in (1, 2, 3)]
stk, lev = lambda x: x // 10, lambda x: x % 10
SNAME = {1: "left", 2: "middle", 3: "right"}
conds = [
    ("Box V is at level 2 of the middle stack.", ("V",), lambda v: v == 22),
    ("Box D is placed directly above box V.", ("D", "V"), lambda d, v: d == v + 1),
    ("Box K is at the bottom of the stack that holds box D.", ("K", "D"), lambda k, d: stk(k) == stk(d) and lev(k) == 1),
    ("Box G is at the bottom of the right stack.", ("G",), lambda g: g == 31),
    ("Box P is at the same level as box V but not in the same stack as box B.", ("P", "V", "B"),
     lambda p, v, b: lev(p) == lev(v) and stk(p) != stk(b)),
    ("Box B is placed directly below box X.", ("B", "X"), lambda b, x: x == b + 1 and stk(b) == stk(x)),
    ("Box S is at the bottom of its stack.", ("S",), lambda s: lev(s) == 1),
    ("Box S is not in the same stack as box M.", ("S", "M"), lambda s, m: stk(s) != stk(m)),
]
X2 = unique(P, {p: SEATS for p in P}, conds, [P])
at = {v: k for k, v in X2.items()}
assert [at[s] for s in SEATS] == ["S", "B", "X", "K", "V", "D", "G", "P", "M"]
ARR = "; ".join(f"{SNAME[s].capitalize()} stack (bottom to top): " + ", ".join(at[s * 10 + l] for l in (1, 2, 3))
                for s in (1, 2, 3))
sid = stimulus("puzzle", "Nine boxes in three stacks",
               "Nine boxes B, D, G, K, M, P, S, V and X are kept in three stacks, left, middle and right, with three "
               "boxes in each stack. Level 1 is the bottom of a stack and level 3 its top.", conds,
               "Middle stack: K (bottom), V, D. G is at the bottom of the right stack, so S, also at a bottom, is at "
               "the bottom of the left stack. P is at level 2 of the left or right stack. If P were in the left "
               "stack, B (not in P's stack) would have to be in the right stack with X above it: B at level 2, X at "
               "level 3; then M would join S in the left stack, which is not allowed. So P is at level 2 of the right "
               "stack, B and X fill levels 2 and 3 of the left stack, and M tops the right stack.\n\n"
               + table(["Level", "Left", "Middle", "Right"],
                       [(l, at[10 + l], at[20 + l], at[30 + l]) for l in (3, 2, 1)]))
XQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, BOX, "Stacked boxes", "Intermediate", text, correct, wrongs, concept, expl, steps, **kw)
ans = at[X2["P"] + 1]
assert ans == "M"
XQ("Which box is placed directly above box P?", f"Box {ans}", ["Box X", "Box D", "Box G"],
   "Stacks are separate columns",
   "P is at level 2 of the right stack; level 3 of that stack holds M.", [ARR],
   why_others_wrong="X and D are at level 3 but in other stacks; G is directly below P.", seconds=60)
tops = [at[s * 10 + 3] for s in (1, 2, 3)]
assert tops == ["X", "D", "M"]
XQ("Which boxes are at the top of the three stacks?", "X, D and M", ["X, V and M", "B, D and M", "X, D and P"],
   "Reading the top level", "Left: X; middle: D; right: M.", [ARR], seconds=55)
ans = next(p for p in P if stk(X2[p]) == 2 and lev(X2[p]) == lev(X2["B"]))
assert ans == "V"
XQ("Which box in the middle stack is at the same level as box B?", f"Box {ans}", ["Box P", "Box K", "Box D"],
   "Matching levels across stacks", "B is at level 2 of the left stack; level 2 of the middle stack holds V.",
   [ARR], why_others_wrong="P is at level 2 but in the right stack; K and D are at levels 1 and 3 of the middle "
                           "stack.", seconds=50)
stm = [("Box G is placed directly below box P", X2["G"] + 1 == X2["P"]),
       ("Box X is in the middle stack", stk(X2["X"]) == 2),
       ("Box K is placed directly below box D", X2["K"] + 1 == X2["D"]),
       ("Box M is at level 2", lev(X2["M"]) == 2)]
t, f = one_true(stm)
XQ("Which of the following statements is true?", t, f, "Checking statements against the stacks",
   "G (right, level 1) is directly below P (right, level 2). X is in the left stack, V lies between K and D, and M "
   "is at level 3.", [ARR], seconds=60)

# ---- X3 Intermediate: eight boxes in one stack, four colours, each colour used for exactly two boxes
P = ["C", "E", "H", "J", "L", "N", "R", "T"]
COL = ["Blue", "Green", "Red", "White"]
K_ = ["k" + p for p in P]
VV = P + K_
IXV = {v: i for i, v in enumerate(VV)}
cols_at = lambda v, c: sorted(v[IXV[p]] for p in P if v[IXV["k" + p]] == c)
conds = [
    ("Box T is placed fourth from the bottom and is blue.", ("T", "kT"), lambda t, k: t == 4 and k == "Blue"),
    ("The other blue box is at the top of the stack.", tuple(VV), lambda *v: cols_at(v, "Blue") == [4, 8]),
    ("Each green box is placed immediately below a blue box.", tuple(VV),
     lambda *v: [x + 1 for x in cols_at(v, "Green")] == cols_at(v, "Blue")),
    ("Box L is placed immediately above box T.", ("L", "T"), lambda l, t: l == t + 1),
    ("Box C is green and is placed above box L.", ("C", "kC", "L"), lambda c, k, l: k == "Green" and c > l),
    ("Box J is at the bottom and is red.", ("J", "kJ"), lambda j, k: j == 1 and k == "Red"),
    ("Exactly two boxes are placed between the two white boxes.", tuple(VV),
     lambda *v: len(cols_at(v, "White")) == 2 and cols_at(v, "White")[1] - cols_at(v, "White")[0] == 3),
    ("Box E is green.", ("kE",), lambda k: k == "Green"),
    ("Box N is placed below box R, and box H is blue.", ("N", "R", "kH"), lambda n, r, k: n < r and k == "Blue"),
]
X3 = unique(VV, {p: range(1, 9) for p in P} | {k: COL for k in K_}, conds, [P])
at = {X3[p]: p for p in P}
cl = {p: X3["k" + p] for p in P}
assert [(at[i], cl[at[i]]) for i in range(1, 9)] == [
    ("J", "Red"), ("N", "White"), ("E", "Green"), ("T", "Blue"), ("L", "White"), ("R", "Red"), ("C", "Green"),
    ("H", "Blue")]
ARR = "Bottom to top: " + ", ".join(f"{at[i]} ({cl[at[i]]})" for i in range(1, 9))
sid = stimulus("puzzle", "Eight boxes in four colours",
               "Eight boxes C, E, H, J, L, N, R and T are kept one above another in a single stack (position 1 is the "
               "bottom, 8 the top). Each box is Blue, Green, Red or White, and exactly two boxes are of each colour.",
               conds,
               "Blue boxes: T (4) and the top box (8). The green boxes sit just below them: positions 3 and 7. L = 5. "
               "C is green and above L, so C = 7; E, the other green box, = 3. J = 1 (red). Positions 2, 5 and 6 hold "
               "one red and two white boxes; the whites have two boxes between them, so they are at 2 and 5 and "
               "position 6 is red. H is blue, so H = 8; N below R puts N at 2 and R at 6.\n\n"
               + table(["Position", "Box", "Colour"], [(i, at[i], cl[at[i]]) for i in range(8, 0, -1)]))
XQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, BOX, "Boxes with weights or colours", "Intermediate", text, correct, wrongs, concept, expl, steps, **kw)
XQ("What is the colour of box R?", cl["R"], ["White", "Green", "Blue"], "Colour counts limit the choices",
   "After the blue, green and the red bottom box are placed, positions 2, 5 and 6 need one red and two white boxes. "
   "The whites must be three apart (2 and 5), so position 6, box R, is red.", [ARR], seconds=70)
assert cl["R"] == "Red"
ans = at[X3["C"] - 1]
assert ans == "R"
XQ("Which box is placed immediately below box C?", f"Box {ans}", ["Box L", "Box H", "Box T"],
   "Adjacent positions in the stack", "C is at 7; position 6 holds R.", [ARR],
   why_others_wrong="L is at 5, two places below C; H is above C; T is at 4.", seconds=60)
wh = [at[i] for i in range(1, 9) if cl[at[i]] == "White"]
assert wh == ["N", "L"]
XQ("Which two boxes are white?", "N and L", ["N and R", "L and R", "J and N"], "Using the 'two between' clue",
   "The white boxes are at positions 2 and 5: N and L.", [ARR], seconds=65)
mid = (X3["J"] + X3["C"]) // 2
assert (X3["J"] + X3["C"]) % 2 == 0 and at[mid] == "T"
XQ("Which box is placed exactly midway between box J and box C?", f"Box {at[mid]}", ["Box L", "Box E", "Box N"],
   "Midpoint of two positions", "J is at 1 and C at 7; the midpoint is position 4: T.", [ARR, "(1 + 7) ÷ 2 = 4"],
   seconds=55)

# ---- X4 Advanced (standalone): six boxes with weights
P = ["B", "F", "K", "Q", "W", "Y"]
WT = [5, 8, 11, 14, 17, 20]
W_ = ["w" + p for p in P]
VV = P + W_
IXV = {v: i for i, v in enumerate(VV)}
box_at = lambda v, pos_: next(p for p in P if v[IXV[p]] == pos_)
conds = [
    ("The heaviest box is placed third from the bottom.", tuple(VV), lambda *v: v[IXV["w" + box_at(v, 3)]] == 20),
    ("Box W is placed immediately below the heaviest box, and box F immediately above it.", ("W", "F"),
     lambda w, f_: w == 2 and f_ == 4),
    ("Box F weighs 3 kg less than box W.", ("wF", "wW"), lambda f_, w: f_ == w - 3),
    ("Box K weighs 8 kg and is placed above box Q.", ("K", "Q", "wK"), lambda k, q, wk: wk == 8 and k > q),
    ("The weights of the top box and the bottom box add up to 19 kg.", tuple(VV),
     lambda *v: v[IXV["w" + box_at(v, 1)]] + v[IXV["w" + box_at(v, 6)]] == 19),
    ("Box Y is heavier than box Q, and box B is placed above box Q.", ("wY", "wQ", "B", "Q"),
     lambda y, wq, b, q: y > wq and b > q),
]
X4 = unique(VV, {p: range(1, 7) for p in P} | {w: WT for w in W_}, conds, [P, W_])
at = {X4[p]: p for p in P}
wt = {p: X4["w" + p] for p in P}
assert [(at[i], wt[at[i]]) for i in range(1, 7)] == [("Q", 11), ("W", 17), ("Y", 20), ("F", 14), ("B", 5), ("K", 8)]
ans = wt["W"] - wt["B"]
assert ans == 12
mcq(BOX, "Boxes with weights or colours", "Advanced",
    "Six boxes B, F, K, Q, W and Y are kept one above another in a single stack (position 1 is the bottom, 6 the "
    "top). Their weights are 5, 8, 11, 14, 17 and 20 kg, one weight per box.\n" + bullets(conds) +
    "\n\nBy how many kilograms is box W heavier than box B?", f"{ans} kg", ["9 kg", "3 kg", "6 kg"],
    "Weights and positions solved together",
    "W = 2, the 20 kg box = 3, F = 4. K weighs 8 kg; F = W − 3, so (W, F) is (17, 14), (14, 11) or (11, 8), and "
    "the last fails because 8 kg is K's. The two ends add to 19: 8 + 11 or 5 + 14. If (W, F) = (14, 11), both pairs "
    "need a weight already used by W or F, so W = 17 and F = 14. Now 5 + 14 is impossible too, so the ends are K "
    "(8 kg) and an 11 kg box; K is above Q, so K cannot be at the bottom: K is on top and the 11 kg box at the "
    "bottom. B, Q and Y share position 1 (11 kg), 3 (20 kg) and 5 (5 kg). B is above Q, so Q is not at 5; Y is "
    "heavier than Q, so Q is not the 20 kg box: Q = 1 (11 kg). Then Y = 20 kg at position 3 and B = 5 kg at "
    f"position 5. W − B = 17 − 5 = {ans} kg.",
    ["W at 2, heaviest (20 kg) at 3, F at 4", "F = W − 3 with K = 8 ⇒ (W, F) = (17, 14) or (14, 11)",
     "Ends sum to 19: only K (8) on top + an 11 kg box at the bottom works, and it needs W = 17, F = 14",
     "B above Q and Y heavier than Q ⇒ Q = bottom (11 kg), Y = 20 kg (position 3), B = 5 kg (position 5)",
     f"17 − 5 = {ans} kg"],
    why_others_wrong="9 kg is W − K; 3 kg is W − F; 6 kg is Q − B.", natural=lambda t: int(t.split()[0]),
    seconds=120, verified_by=BRUTE)

# ================================================================================================ MONTH / DATE / YEAR
MON = "Month and Date-Based Puzzles"

# ---- M1 Basic: seven workshops from April to October, each person with a favourite colour
P = ["Anaya", "Bodhi", "Chinmayi", "Daivik", "Eila", "Girik", "Hiral"]
COLS = ["Blue", "Green", "Maroon", "Orange", "Pink", "White", "Yellow"]
K_ = ["k" + p for p in P]
VV = P + K_
IXV = {v: i for i, v in enumerate(VV)}
m_of = lambda v, c: next(v[IXV[p]] for p in P if v[IXV["k" + p]] == c)
conds = [
    ("Chinmayi's workshop is in a month that has 31 days, and only two workshops are held after hers.",
     ("Chinmayi",), lambda c: MDAYS[c] == 31 and 10 - c == 2),
    ("The person who likes White attends two months before Chinmayi.", tuple(VV),
     lambda *v: m_of(v, "White") == v[IXV["Chinmayi"]] - 2),
    ("Girik attends in the month immediately after the person who likes White.", tuple(VV),
     lambda *v: v[IXV["Girik"]] == m_of(v, "White") + 1),
    ("Eila attends in the month immediately after Chinmayi, and Bodhi attends after Eila.", ("Eila", "Chinmayi", "Bodhi"),
     lambda e, c, b: e == c + 1 and b > e),
    ("Daivik attends before Hiral, and neither of them likes White.", ("Daivik", "Hiral", "kDaivik", "kHiral"),
     lambda d, h, kd, kh: d < h and "White" not in (kd, kh)),
    ("The person who likes Maroon attends in the last month.", tuple(VV), lambda *v: m_of(v, "Maroon") == 10),
    ("Chinmayi likes Green, and the person who likes Yellow attends immediately before her.", tuple(VV),
     lambda *v: v[IXV["kChinmayi"]] == "Green" and m_of(v, "Yellow") == v[IXV["Chinmayi"]] - 1),
    ("Hiral likes neither Pink nor Orange, and Eila does not like Pink.", ("kHiral", "kEila"),
     lambda h, e: h not in ("Pink", "Orange") and e != "Pink"),
]
M1 = unique(VV, {p: range(4, 11) for p in P} | {k: COLS for k in K_}, conds, [P, K_])
at = {M1[p]: p for p in P}
cl = {p: M1["k" + p] for p in P}
assert [(at[m], cl[at[m]]) for m in range(4, 11)] == [
    ("Daivik", "Pink"), ("Hiral", "Blue"), ("Anaya", "White"), ("Girik", "Yellow"), ("Chinmayi", "Green"),
    ("Eila", "Orange"), ("Bodhi", "Maroon")]
ARR = "April to October: " + ", ".join(f"{MNAME[m]} – {at[m]} ({cl[at[m]]})" for m in range(4, 11))
sid = stimulus("puzzle", "Seven workshops from April to October, with colours",
               "Seven persons Anaya, Bodhi, Chinmayi, Daivik, Eila, Girik and Hiral attend a workshop, one person in "
               "each month from April to October of the same year. Each of them likes a different colour among Blue, "
               "Green, Maroon, Orange, Pink, White and Yellow.", conds,
               "Two workshops come after Chinmayi's, so hers is in August (31 days). White is two months earlier: "
               "June; Girik follows in July. Eila is in September and Bodhi, after her, in October. April, May and "
               "June remain for Anaya, Daivik and Hiral; Daivik and Hiral do not like White, so Anaya is in June and "
               "Daivik (April) is before Hiral (May). Chinmayi likes Green and Girik (July) Yellow; Bodhi (October) "
               "likes Maroon. Blue, Orange and Pink remain for Daivik, Hiral and Eila: Hiral takes Blue, and Eila, not "
               "Pink, takes Orange; Daivik likes Pink.\n\n"
               + table(["Month", "Person", "Colour"], [(MNAME[m], at[m], cl[at[m]]) for m in range(4, 11)]))
MQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, MON, "Month-based", "Basic", text, correct, wrongs, concept, expl, steps, **kw)
MQ("Who attends the workshop in May?", at[5], ["Daivik", "Anaya", "Girik"], "Ordering the remaining months",
   "Anaya must be the White lover in June, since Daivik and Hiral do not like White; Daivik is before Hiral, so "
   "Daivik is in April and Hiral in May.", [ARR], seconds=50)
MQ("Which colour does Eila like?", cl["Eila"], ["Pink", "Blue", "Maroon"], "Elimination of colours",
   "Blue, Orange and Pink are left for Daivik, Hiral and Eila. Hiral likes neither Pink nor Orange, so Blue; Eila "
   "does not like Pink, so Orange.", [ARR], seconds=50)
gap = M1["Girik"] - M1["Daivik"] - 1
assert gap == 2
MQ("How many persons attend between Daivik and Girik?", num_word(gap), ["One", "Three", "Four"],
   "Counting months between two persons", "Daivik is in April and Girik in July; Hiral (May) and Anaya (June) "
   "attend between them.", [ARR], natural=by_num, seconds=45)
x_ = next(p for p in P if cl[p] == "Maroon")
ans = at[M1[x_] - 1]
assert ans == "Eila"
MQ("Who attends immediately before the person who likes Maroon?", ans, ["Chinmayi", "Bodhi", "Girik"],
   "Attribute first, then the month before it",
   "Maroon belongs to the October workshop (Bodhi); the September workshop is Eila's.", [ARR],
   why_others_wrong="Bodhi himself likes Maroon; Chinmayi is two months before him; Girik is in July.", seconds=45)

# ---- M2 Intermediate: six appointments in a 30-day month whose 1st is a Monday
P = ["Nirmal", "Oishi", "Pavan", "Rasika", "Shubh", "Vedika"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
wd = lambda d: (d - 1) % 7  # 0 = Monday
nth = lambda d: (d - 1) // 7 + 1  # 'n-th <weekday> of the month'
conds = [
    ("Oishi's appointment is on the second Wednesday of the month.", ("Oishi",), lambda o: wd(o) == 2 and nth(o) == 2),
    ("Nirmal's appointment is exactly one week before Oishi's.", ("Nirmal", "Oishi"), lambda n, o: n == o - 7),
    ("Shubh's appointment is on the fourth Monday of the month.", ("Shubh",), lambda s: wd(s) == 0 and nth(s) == 4),
    ("Rasika's appointment is on a Friday before Shubh's.", ("Rasika", "Shubh"), lambda r, s: wd(r) == 4 and r < s),
    ("Pavan's appointment is on a Sunday, after Oishi's but before Rasika's.", ("Pavan", "Oishi", "Rasika"),
     lambda p, o, r: wd(p) == 6 and o < p < r),
    ("Vedika's appointment is on the last Saturday of the month.", ("Vedika",),
     lambda v: wd(v) == 5 and v + 7 > 30),
]
M2 = unique(P, {p: range(1, 31) for p in P}, conds, [P])
assert [M2[p] for p in P] == [3, 10, 14, 19, 22, 27]
order_ = sorted(P, key=M2.get)
ARR = "In date order: " + ", ".join(f"{p} – {M2[p]} ({DAYS[wd(M2[p])]})" for p in order_)
sid = stimulus("puzzle", "Six appointments in a month that starts on a Monday",
               "Six customers Nirmal, Oishi, Pavan, Rasika, Shubh and Vedika each have one appointment at a bank in "
               "the same month, on six different dates. The month has 30 days, and its 1st is a Monday.", conds,
               "Mondays fall on 1, 8, 15, 22, 29; Wednesdays on 3, 10, 17, 24; Fridays on 5, 12, 19, 26; Saturdays on "
               "6, 13, 20, 27; Sundays on 7, 14, 21, 28. Oishi = 10 (second Wednesday), Nirmal = 3, Shubh = 22 "
               "(fourth Monday), Vedika = 27 (last Saturday). Rasika is on a Friday before the 22nd: 5, 12 or 19, and "
               "a Sunday (Pavan) must fit between the 10th and Rasika's date, so Rasika = 19 and Pavan = 14.\n\n"
               + table(["Customer", "Date", "Day"], [(p, M2[p], DAYS[wd(M2[p])]) for p in order_]))
MQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, MON, "Date-based", "Intermediate", text, correct, wrongs, concept, expl, steps, **kw)
MQ("On which date is Pavan's appointment?", f"{M2['Pavan']}th", ["7th", "21st", "12th"],
   "Weekday of a date from the weekday of the 1st",
   "Pavan's Sunday must lie after the 10th (Oishi) and before Rasika's Friday, which itself is before the 22nd. The "
   "only fit is Sunday the 14th with Rasika on Friday the 19th.",
   [ARR, "Sundays: 7, 14, 21, 28; Fridays before the 22nd: 5, 12, 19", "10 < Pavan < Rasika < 22 ⇒ 14 and 19"],
   why_others_wrong="The 7th is before Oishi's appointment; the 21st is after every Friday before the 22nd; the 12th "
                    "is a Friday.", natural=lambda t: int(t[:-2]), seconds=70)
d = M2["Vedika"] - M2["Rasika"]
assert d == 8
MQ("How many days after Rasika's appointment is Vedika's appointment?", str(d), ["7", "5", "9"],
   "Difference of dates", "Rasika: 19th; Vedika: 27th (the last Saturday, since 27 + 7 > 30); 27 − 19 = 8.",
   [ARR, "27 − 19 = 8"], natural=int, seconds=60)
wk = sum(1 for p in P if wd(M2[p]) <= 4)
assert wk == 4
MQ("How many of the six appointments fall on a weekday from Monday to Friday?", num_word(wk),
   ["Three", "Five", "Two"], "Classifying dates by weekday",
   "Nirmal (Wednesday), Oishi (Wednesday), Rasika (Friday) and Shubh (Monday) are on weekdays; Pavan (Sunday) and "
   "Vedika (Saturday) are not.", [ARR], natural=by_num, seconds=60)
ans = order_[order_.index("Pavan") + 1]
assert ans == "Rasika"
MQ("Whose appointment comes immediately after Pavan's in date order?", ans, ["Shubh", "Oishi", "Vedika"],
   "Sorting by date", "In date order: Nirmal 3, Oishi 10, Pavan 14, Rasika 19, Shubh 22, Vedika 27.", [ARR],
   seconds=55)

# ---- M3 Advanced: eight persons joining in March, June, September or December of 2024 or 2025
P = ["Aadya", "Bhavin", "Darpan", "Eshwari", "Gyan", "Hetal", "Jagrut", "Kirtana"]
SLOT = [(y, m) for y in (2024, 2025) for m in (3, 6, 9, 12)]
SL = lambda i: f"{MNAME[SLOT[i][1]]} {SLOT[i][0]}"
conds = [
    ("Bhavin joined in June of one of the two years.", ("Bhavin",), lambda b: SLOT[b][1] == 6),
    ("Only three persons joined between Bhavin and Darpan, and Darpan joined before Bhavin.", ("Bhavin", "Darpan"),
     lambda b, d: b - d == 4),
    ("Aadya joined in December of the year in which Darpan joined.", ("Aadya", "Darpan"),
     lambda a, d: SLOT[a] == (SLOT[d][0], 12)),
    ("Eshwari joined immediately after Bhavin, and Gyan joined after Eshwari.", ("Eshwari", "Bhavin", "Gyan"),
     lambda e, b, g: e == b + 1 and g > e),
    ("Hetal joined before Kirtana, and both of them joined in the same year.", ("Hetal", "Kirtana"),
     lambda h, k: h < k and SLOT[h][0] == SLOT[k][0]),
]
M3 = unique(P, {p: range(8) for p in P}, conds, [P])
at = {v: k for k, v in M3.items()}
assert [at[i] for i in range(8)] == ["Hetal", "Darpan", "Kirtana", "Aadya", "Jagrut", "Bhavin", "Eshwari", "Gyan"]
ARR = "In time order: " + ", ".join(f"{SL(i)} – {at[i]}" for i in range(8))
sid = stimulus("puzzle", "Eight officers joining over two years",
               "Eight officers Aadya, Bhavin, Darpan, Eshwari, Gyan, Hetal, Jagrut and Kirtana joined a bank. Each "
               "joined in a different one of these eight months: March, June, September and December of 2024, and "
               "March, June, September and December of 2025.", conds,
               "List the eight months in time order (Mar 24, Jun 24, Sep 24, Dec 24, Mar 25, Jun 25, Sep 25, Dec 25). "
               "Bhavin joined in a June and Darpan four places earlier, so Bhavin = June 2025 and Darpan = June 2024. "
               "Aadya = December 2024. Eshwari = September 2025 and Gyan, after her, = December 2025. March 2024, "
               "September 2024 and March 2025 remain; Hetal and Kirtana joined in the same year with Hetal first, so "
               "Hetal = March 2024, Kirtana = September 2024 and Jagrut = March 2025.\n\n"
               + table(["Month", "Officer"], [(SL(i), at[i]) for i in range(8)]))
MQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, MON, "Year-based", "Advanced", text, correct, wrongs, concept, expl, steps, **kw)
MQ("Who joined in March 2025?", at[4], ["Kirtana", "Hetal", "Bhavin"], "Same-year pair placed last",
   "After Bhavin, Darpan, Aadya, Eshwari and Gyan are placed, March 2024, September 2024 and March 2025 are left. "
   "Hetal and Kirtana must share a year, which only 2024 allows, so Jagrut joined in March 2025.", [ARR], seconds=75)
gap = M3["Eshwari"] - M3["Kirtana"] - 1
assert gap == 3
MQ("How many officers joined between Kirtana and Eshwari?", num_word(gap), ["Two", "Four", "Five"],
   "Counting across the change of year", "Kirtana: September 2024; Eshwari: September 2025. Aadya, Jagrut and "
   "Bhavin joined in between.", [ARR], natural=by_num, seconds=70)
MQ("In which month and year did Bhavin join?", SL(M3["Bhavin"]), ["June 2024", "September 2025", "March 2025"],
   "Fixing a pair with 'three between'",
   "Bhavin joined in a June with three officers between him and the earlier Darpan, i.e. four places apart in the "
   "list. June 2024 → June 2025 is the only such pair, so Bhavin joined in June 2025.", [ARR], seconds=75)
ans = at[M3["Aadya"] - 1]
assert ans == "Kirtana"
MQ("Who joined immediately before Aadya?", ans, ["Darpan", "Hetal", "Jagrut"], "Adjacent months in the list",
   "Aadya joined in December 2024; September 2024 is Kirtana's.", [ARR], seconds=60)
stm = [("Gyan joined in December 2025", SL(M3["Gyan"]) == "December 2025"),
       ("Hetal joined in June 2024", SL(M3["Hetal"]) == "June 2024"),
       ("Darpan and Jagrut joined in the same year", SLOT[M3["Darpan"]][0] == SLOT[M3["Jagrut"]][0]),
       ("Two officers joined between Aadya and Bhavin", M3["Bhavin"] - M3["Aadya"] - 1 == 2)]
t, f = one_true(stm)
MQ("Which of the following statements is true?", t, f, "Checking statements against the timeline",
   "Gyan joined after Eshwari (September 2025), so in December 2025. Hetal joined in March 2024, Darpan in 2024 but "
   "Jagrut in 2025, and only Jagrut joined between Aadya and Bhavin.", [ARR], seconds=70)

# ================================================================================================ PUZZLES (OTHER)
OTH = "Puzzles (Other)"

# ---- O1 Basic (standalone): comparison with numbers
P = ["Kushal", "Madhuri", "Navin", "Payal", "Rajat"]
conds = [("Payal read 14 books, which is 5 more than Navin.", ("Payal", "Navin"), lambda p, n: p == 14 and n == 9),
         ("Madhuri read 2 books fewer than Payal.", ("Madhuri", "Payal"), lambda m, p: m == p - 2),
         ("Kushal read more books than Madhuri but fewer than Payal.", ("Kushal", "Madhuri", "Payal"),
          lambda k, m, p: m < k < p),
         ("Rajat read 3 books fewer than Kushal.", ("Rajat", "Kushal"), lambda r, k: r == k - 3)]
O1 = unique(P, {p: range(1, 31) for p in P}, conds)
assert [O1[p] for p in P] == [13, 12, 9, 14, 10]
cnt = sum(1 for p in P if O1[p] > O1["Rajat"])
assert cnt == 3
mcq(OTH, "Comparison and ordering", "Basic",
    "Five friends Kushal, Madhuri, Navin, Payal and Rajat read different numbers of books last year.\n"
    + bullets(conds) + "\n\nHow many of the friends read more books than Rajat?", num_word(cnt),
    ["Two", "Four", "One"], "Turning comparisons into numbers",
    "Payal 14, Navin 14 − 5 = 9, Madhuri 14 − 2 = 12. Kushal lies strictly between 12 and 14, so 13, and Rajat = "
    "13 − 3 = 10. More than 10: Payal, Kushal and Madhuri.",
    ["Payal 14; Navin 9; Madhuri 12", "12 < Kushal < 14 ⇒ Kushal 13", "Rajat 13 − 3 = 10",
     "Above 10: 14, 13, 12 ⇒ three friends"],
    why_others_wrong="Four wrongly counts Navin (9 < 10); Two leaves out Madhuri.", natural=by_num, seconds=45,
    verified_by=BRUTE)

# ---- O2 Basic (standalone): four designations
POSTS4 = ["Branch Manager", "Deputy Manager", "Assistant Manager", "Officer"]
P = ["Sapna", "Trilok", "Umesh", "Vasant"]
conds = [("Trilok is senior to Umesh but junior to Sapna.", ("Trilok", "Umesh", "Sapna"), lambda t, u, s: s < t < u),
         ("Umesh is not the Assistant Manager, and Vasant is not the Officer.", ("Umesh", "Vasant"),
          lambda u, v: u != 3 and v != 4),
         ("Vasant is senior to Trilok.", ("Vasant", "Trilok"), lambda v, t: v < t),
         ("Sapna is not the Branch Manager.", ("Sapna",), lambda s: s != 1)]
O2 = unique(P, {p: range(1, 5) for p in P}, conds, [P])
assert [O2[p] for p in P] == [2, 3, 4, 1]
ans = next(p for p in P if O2[p] == 2)
mcq(OTH, "Designation", "Basic",
    "Four employees Sapna, Trilok, Umesh and Vasant of a bank branch hold four different posts. In decreasing order "
    "of seniority the posts are: Branch Manager, Deputy Manager, Assistant Manager and Officer.\n" + bullets(conds)
    + "\n\nWho is the Deputy Manager?", ans, ["Trilok", "Vasant", "Umesh"], "Seniority as a ranking",
    "Sapna > Trilok > Umesh in seniority. Umesh cannot be the Assistant Manager, so he is the Officer. Vasant is "
    "senior to Trilok, so Trilok is the Assistant Manager. Sapna is not the Branch Manager, so Vasant is, and Sapna is "
    "the Deputy Manager.",
    ["Sapna > Trilok > Umesh", "Umesh ≠ Assistant Manager ⇒ Umesh = Officer",
     "Vasant senior to Trilok ⇒ Trilok = Assistant Manager", "Sapna ≠ Branch Manager ⇒ Vasant = Branch Manager, "
     "Sapna = Deputy Manager"],
    why_others_wrong="Trilok is the Assistant Manager, Vasant the Branch Manager and Umesh the Officer.", seconds=45,
    verified_by=BRUTE)

# ---- O3 Intermediate: seven hobby classes, one on each day from Monday to Sunday
P = ["Abeer", "Brinda", "Darius", "Elora", "Gauransh", "Ivaan", "Mehr"]
HB = ["Chess", "Cooking", "Dance", "Music", "Painting", "Pottery", "Yoga"]
H_ = ["h" + p for p in P]
VV = P + H_
IXV = {v: i for i, v in enumerate(VV)}
d_of = lambda v, h: next(v[IXV[p]] for p in P if v[IXV["h" + p]] == h)
conds = [
    ("Mehr's class is exactly in the middle of the week.", ("Mehr",), lambda m: m == 3),
    ("Only two classes are held between Mehr's class and the Cooking class, which is held after Mehr's.", tuple(VV),
     lambda *v: d_of(v, "Cooking") == v[IXV["Mehr"]] + 3),
    ("The Dance class is held on Friday.", tuple(VV), lambda *v: d_of(v, "Dance") == 4),
    ("Abeer attends the Music class, which is held two days before the Dance class.", tuple(VV),
     lambda *v: v[IXV["hAbeer"]] == "Music" and v[IXV["Abeer"]] == d_of(v, "Dance") - 2),
    ("Elora attends on Monday, and Gauransh attends the Chess class.", ("Elora", "hGauransh"),
     lambda e, g: e == 0 and g == "Chess"),
    ("Darius attends on the day immediately before Brinda.", ("Darius", "Brinda"), lambda d, b: d == b - 1),
    ("Ivaan attends after Darius, but not on Saturday.", ("Ivaan", "Darius"), lambda i, d: i > d and i != 5),
    ("Mehr attends neither Painting nor Yoga, and Brinda does not attend Yoga.", ("hMehr", "hBrinda"),
     lambda m, b: m not in ("Painting", "Yoga") and b != "Yoga"),
]
O3 = unique(VV, {p: range(7) for p in P} | {h: HB for h in H_}, conds, [P, H_])
at = {O3[p]: p for p in P}
hb = {p: O3["h" + p] for p in P}
assert [(at[i], hb[at[i]]) for i in range(7)] == [
    ("Elora", "Yoga"), ("Gauransh", "Chess"), ("Abeer", "Music"), ("Mehr", "Pottery"), ("Darius", "Dance"),
    ("Brinda", "Painting"), ("Ivaan", "Cooking")]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
ARR = "Monday to Sunday: " + ", ".join(f"{DAYS[i]} – {at[i]} ({hb[at[i]]})" for i in range(7))
sid = stimulus("puzzle", "Seven hobby classes in a week",
               "Seven persons Abeer, Brinda, Darius, Elora, Gauransh, Ivaan and Mehr each attend one hobby class in "
               "the same week, one class on each day from Monday to Sunday. The classes are Chess, Cooking, Dance, "
               "Music, Painting, Pottery and Yoga, one each.", conds,
               "Mehr = Thursday, Cooking = Sunday, Dance = Friday, and Music (Abeer) = Wednesday. Elora = Monday. "
               "Tuesday, Friday, Saturday and Sunday remain for Brinda, Darius, Gauransh and Ivaan. Darius–Brinda are "
               "consecutive: Friday–Saturday (Saturday–Sunday would leave no later day for Ivaan). Ivaan = Sunday "
               "(Cooking) and Gauransh = Tuesday (Chess); Darius takes Dance. Of Painting, Pottery and Yoga, Mehr "
               "takes Pottery, Brinda Painting and Elora Yoga.\n\n"
               + table(["Day", "Person", "Class"], [(DAYS[i], at[i], hb[at[i]]) for i in range(7)]))
OQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, OTH, "Day-based", "Intermediate", text, correct, wrongs, concept, expl, steps, **kw)
OQ("Which class does Brinda attend?", hb["Brinda"], ["Yoga", "Pottery", "Cooking"], "Day and attribute together",
   "Brinda attends on Saturday. Of the three classes left (Painting, Pottery, Yoga), Mehr has Pottery and Brinda "
   "cannot have Yoga, so Brinda attends Painting.", [ARR], seconds=60)
OQ("On which day is the Chess class held?", DAYS[O3["Gauransh"]], ["Saturday", "Monday", "Sunday"],
   "Placing the last free person", "Darius and Brinda take Friday and Saturday and Ivaan Sunday, so Gauransh, who "
   "attends Chess, takes the only day left: Tuesday.", [ARR], seconds=55)
gap = O3["Darius"] - O3["Elora"] - 1
assert gap == 3
OQ("How many classes are held between Elora's class and Darius's class?", num_word(gap), ["Two", "Four", "One"],
   "Counting days between", "Elora: Monday; Darius: Friday. Tuesday, Wednesday and Thursday lie between.", [ARR],
   natural=by_num, seconds=50)

# ---- O4 Intermediate: six officers, six designations, six cities
POSTS = ["Director", "Joint Director", "Deputy Director", "Assistant Director", "Section Officer", "Assistant"]
P = ["Nikunj", "Quresh", "Rutvi", "Saanvi", "Tanush", "Udit"]
CTS = ["Indore", "Jaipur", "Lucknow", "Mysuru", "Ranchi", "Shimla"]
K_ = ["c" + p for p in P]
VV = P + K_
IXV = {v: i for i, v in enumerate(VV)}
r_of = lambda v, c: next(v[IXV[p]] for p in P if v[IXV["c" + p]] == c)
conds = [
    ("Only two officers are senior to Nikunj.", ("Nikunj",), lambda n: n == 3),
    ("The officer posted in Jaipur is immediately junior to Nikunj, and Saanvi is posted in Jaipur.",
     ("Saanvi", "cSaanvi", "Nikunj"), lambda s, c, n: c == "Jaipur" and s == n + 1),
    ("Tanush is junior to Quresh, who is junior to Saanvi.", ("Tanush", "Quresh", "Saanvi"),
     lambda t, q, s: s < q < t),
    ("Rutvi is senior to Udit.", ("Rutvi", "Udit"), lambda r, u: r < u),
    ("The officer posted in Shimla is senior to the officer posted in Indore, and both are senior to Nikunj.",
     tuple(VV), lambda *v: r_of(v, "Shimla") < r_of(v, "Indore") < v[IXV["Nikunj"]]),
    ("The Assistant is posted in Lucknow.", tuple(VV), lambda *v: r_of(v, "Lucknow") == 6),
    ("Quresh is not posted in Ranchi.", ("cQuresh",), lambda c: c != "Ranchi"),
]
O4 = unique(VV, {p: range(1, 7) for p in P} | {k: CTS for k in K_}, conds, [P, K_])
at = {O4[p]: p for p in P}
ct = {p: O4["c" + p] for p in P}
assert [(at[i], ct[at[i]]) for i in range(1, 7)] == [
    ("Rutvi", "Shimla"), ("Udit", "Indore"), ("Nikunj", "Ranchi"), ("Saanvi", "Jaipur"), ("Quresh", "Mysuru"),
    ("Tanush", "Lucknow")]
ARR = "Most senior to most junior: " + ", ".join(f"{POSTS[i - 1]} – {at[i]} ({ct[at[i]]})" for i in range(1, 7))
sid = stimulus("puzzle", "Six officers, designations and postings",
               "Six officers Nikunj, Quresh, Rutvi, Saanvi, Tanush and Udit hold six different designations. In "
               "decreasing order of seniority the designations are: Director, Joint Director, Deputy Director, "
               "Assistant Director, Section Officer and Assistant. Each officer is posted in a different city among "
               "Indore, Jaipur, Lucknow, Mysuru, Ranchi and Shimla.", conds,
               "Nikunj is third (Deputy Director) and Saanvi fourth (Assistant Director, Jaipur). Quresh and Tanush "
               "are junior to Saanvi: Section Officer and Assistant, in that order. Rutvi (Director) is senior to Udit "
               "(Joint Director). The Shimla and Indore officers are the two above Nikunj, Shimla first: Rutvi – "
               "Shimla, Udit – Indore. Tanush (Assistant) is in Lucknow. Mysuru and Ranchi remain for Nikunj and "
               "Quresh; Quresh is not in Ranchi, so Quresh – Mysuru and Nikunj – Ranchi.\n\n"
               + table(["Designation", "Officer", "City"], [(POSTS[i - 1], at[i], ct[at[i]]) for i in range(1, 7)]))
OQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, OTH, "Designation", "Intermediate", text, correct, wrongs, concept, expl, steps, **kw)
OQ("Who is posted in Indore?", next(p for p in P if ct[p] == "Indore"), ["Rutvi", "Nikunj", "Quresh"],
   "Matching a city through seniority", "The Shimla and Indore officers are the two senior to Nikunj, with Shimla "
   "senior. Rutvi is senior to Udit, so Rutvi is in Shimla and Udit in Indore.", [ARR], seconds=60)
OQ("What is Quresh's designation?", POSTS[O4["Quresh"] - 1], ["Assistant", "Assistant Director", "Joint Director"],
   "Chained 'junior to' clues", "Saanvi (fourth) > Quresh > Tanush, and only the fifth and sixth posts are left: "
   "Quresh is the Section Officer.", [ARR], seconds=55)
x_ = next(p for p in P if ct[p] == "Ranchi")
cnt = 6 - O4[x_]
assert x_ == "Nikunj" and cnt == 3
OQ("How many officers are junior to the officer posted in Ranchi?", num_word(cnt), ["Two", "Four", "One"],
   "City first, then rank", "Nikunj is posted in Ranchi and is the Deputy Director (third); Saanvi, Quresh and "
   "Tanush are junior to him.", [ARR], natural=by_num, seconds=55)

# ---- O5 Advanced (standalone): ranking fixed by comparisons, scores fixed by arithmetic
P = ["Aneesh", "Dipali", "Faiz", "Harpreet", "Mrinalini", "Sohan"]
orders = []
for perm in itertools.permutations(P):  # perm[0] = highest score
    r = {p: i for i, p in enumerate(perm)}
    if (sum(1 for p in P if r[p] > r["Harpreet"]) == 3 and r["Dipali"] < r["Sohan"] < r["Aneesh"]
            and r["Mrinalini"] < r["Faiz"] < r["Harpreet"]):
        orders.append(perm)
assert orders == [("Mrinalini", "Faiz", "Harpreet", "Dipali", "Sohan", "Aneesh")]
sc = {"Faiz": 84, "Harpreet": 77, "Aneesh": 52}
sc["Mrinalini"] = sc["Faiz"] + 6
sc["Dipali"] = 2 * sc["Harpreet"] - sc["Faiz"]
sc["Sohan"] = (sc["Dipali"] + sc["Aneesh"]) // 2
assert (sc["Dipali"] + sc["Aneesh"]) % 2 == 0 and sorted(P, key=sc.get, reverse=True) == list(orders[0])
ans = sc["Mrinalini"] - sc["Sohan"]
assert ans == 29
mcq(OTH, "Comparison and ordering", "Advanced",
    "Six students Aneesh, Dipali, Faiz, Harpreet, Mrinalini and Sohan scored different marks in a test.\n"
    "- Harpreet scored more than exactly three of the others.\n- Sohan scored less than Dipali but more than Aneesh.\n"
    "- Faiz scored more than Harpreet but less than Mrinalini.\n- Faiz scored 84 and Mrinalini scored 6 more than "
    "Faiz.\n- Harpreet scored 77, which is exactly the average of Faiz's and Dipali's scores.\n- The lowest score in "
    "the group is 52.\n- Sohan's score is exactly the average of the two scores immediately above and below his own."
    "\n\nWhat is the difference between the scores of Mrinalini and Sohan?", str(ans), ["23", "38", "13"],
    "Order from comparisons, values from averages",
    "Harpreet is third from the top. Mrinalini > Faiz > Harpreet fills the top three, and Dipali > Sohan > Aneesh the "
    f"bottom three. Mrinalini = 84 + 6 = 90; Dipali = 2 × 77 − 84 = 70; Aneesh, the lowest, = 52; Sohan sits between "
    f"Dipali and Aneesh: (70 + 52) ÷ 2 = 61. 90 − 61 = {ans}.",
    ["Order: Mrinalini > Faiz > Harpreet > Dipali > Sohan > Aneesh", "Mrinalini = 90; Dipali = 154 − 84 = 70",
     "Lowest (Aneesh) = 52; Sohan = (70 + 52) ÷ 2 = 61", f"90 − 61 = {ans}"],
    why_others_wrong="23 is Faiz − Sohan; 38 is Mrinalini − Aneesh; 13 is Mrinalini − Harpreet.", natural=int,
    seconds=100, verified_by=BRUTE)

# ================================================================================================ SYLLOGISM
TWO, FEW, POSS = "Two-statement", "Only a few / Only", "Possibility cases"


def N(*pairs):  # redefined: the seating sections reuse the name N for a seat count
    return {s_: (s_, p_) for s_, p_ in pairs}


# ---- Basic (two statements)
syl_q("Basic", TWO, N(("camera", "cameras"), ("lens", "lenses"), ("tripod", "tripods")),
      [("all", "camera", "lens"), ("some", "lens", "tripod")],
      [("some", "tripod", "camera"), ("some", "lens", "camera")], ONLY_II,
      "All A are B converts to Some B are A",
      "Cameras exist and every camera is a lens, so some lenses are cameras (II). The tripods that are lenses may lie "
      "in the part of lenses that holds no camera, so I is not certain.",
      ["All cameras are lenses ⇒ Some lenses are cameras: II follows",
       "Some lenses are tripods: that overlap need not touch the camera part ⇒ I does not follow"],
      shortcut="All + Some (with the middle term in the second 'Some') gives no conclusion between the end terms.",
      seconds=35)
syl_q("Basic", TWO, N(("bottle", "bottles"), ("jar", "jars"), ("flask", "flasks")),
      [("no", "bottle", "jar"), ("all", "jar", "flask")],
      [("somenot", "flask", "bottle"), ("no", "flask", "bottle")], ONLY_I,
      "No + All: the 'All' set carries the 'not'",
      "Every jar is a flask and no jar is a bottle, so the flasks that are jars are not bottles: some flasks are not "
      "bottles (I). The flasks outside jars may be bottles, so II is not certain.",
      ["Jars ⊂ flasks; jars and bottles do not overlap", "Flasks that are jars are not bottles ⇒ I follows",
       "Other flasks may be bottles ⇒ II does not follow"],
      why="'Either' does not apply: 'Some flasks are not bottles' and 'No flask is a bottle' can both be true, so they "
          "are not a complementary pair.", seconds=35)
syl_q("Basic", TWO, N(("needle", "needles"), ("thread", "threads"), ("button", "buttons")),
      [("some", "needle", "thread"), ("some", "thread", "button")],
      [("some", "needle", "button"), ("no", "needle", "button")], EITHER,
      "Some + Some gives no definite conclusion; check for a complementary pair",
      "Two 'Some' statements give no definite link between needles and buttons, so neither I nor II is certain. But "
      "the two conclusions are 'Some' and 'No' about the same two terms: exactly one of them must be true. So either "
      "I or II follows.",
      ["Some + Some ⇒ no definite needle–button relation", "I alone is not certain; II alone is not certain",
       "I and II are complementary (same subject and predicate) ⇒ Either I or II follows"],
      why="'Either' takes the place of 'Both' (four-option rule); 'Neither' ignores the complementary pair.",
      seconds=40)
syl_q("Basic", TWO, N(("mirror", "mirrors"), ("frame", "frames"), ("glass", "glasses")),
      [("all", "mirror", "frame"), ("all", "frame", "glass")],
      [("all", "mirror", "glass"), ("some", "glass", "frame")], BOTH,
      "All + All = All",
      "Every mirror is a frame and every frame is a glass, so every mirror is a glass (I). Frames exist and all of "
      "them are glasses, so some glasses are frames (II).",
      ["Mirrors ⊂ frames ⊂ glasses ⇒ All mirrors are glasses: I follows",
       "All frames are glasses ⇒ Some glasses are frames: II follows"], shortcut="All + All ⇒ All.", seconds=30)
syl_q("Basic", TWO, N(("sparrow", "sparrows"), ("crow", "crows"), ("pigeon", "pigeons")),
      [("some", "sparrow", "crow"), ("no", "crow", "pigeon")],
      [("all", "sparrow", "pigeon"), ("some", "pigeon", "sparrow")], NEITHER,
      "Some + No = Some not",
      "The sparrows that are crows cannot be pigeons, so 'All sparrows are pigeons' is false (I). The other sparrows "
      "may or may not be pigeons, so II is possible but not certain.",
      ["Some sparrows are crows; no crow is a pigeon ⇒ Some sparrows are not pigeons",
       "That makes I (All sparrows are pigeons) false", "A sparrow–pigeon overlap is possible but not certain ⇒ II "
       "does not follow"], seconds=35)
syl_q("Basic", TWO, N(("cushion", "cushions"), ("pillow", "pillows"), ("quilt", "quilts")),
      [("all", "cushion", "pillow"), ("no", "quilt", "pillow")],
      [("no", "cushion", "quilt"), ("some", "quilt", "cushion")], ONLY_I,
      "All + No (reversed) = No",
      "Every cushion is a pillow and no quilt is a pillow, so no cushion can be a quilt (I). II contradicts I.",
      ["Cushions ⊂ pillows; quilts lie outside pillows", "So cushions and quilts never meet ⇒ I follows",
       "II says the opposite of I ⇒ does not follow"], seconds=30)
syl_q("Basic", TWO, N(("onion", "onions"), ("potato", "potatoes"), ("carrot", "carrots")),
      [("somenot", "onion", "potato"), ("all", "potato", "carrot")],
      [("some", "onion", "carrot"), ("some", "carrot", "potato")], ONLY_II,
      "'Some not' links nothing; 'All' converts",
      "Potatoes exist and every potato is a carrot, so some carrots are potatoes (II). The onions are tied to "
      "carrots by nothing (some onions lie outside potatoes, which says nothing about carrots), so I is not certain.",
      ["All potatoes are carrots ⇒ Some carrots are potatoes: II follows",
       "Some onions are not potatoes gives no onion–carrot link ⇒ I does not follow"], seconds=35)
# ---- Intermediate (only a few / only)
syl_q("Intermediate", FEW, N(("piano", "pianos"), ("flute", "flutes"), ("harp", "harps")),
      [("onlyfew", "piano", "flute"), ("no", "flute", "harp")],
      [("somenot", "piano", "harp"), ("poss_all", "piano", "harp")], ONLY_I,
      "'Only a few A are B' contains 'Some A are B'",
      "Some pianos are flutes, and no flute is a harp, so those pianos are not harps (I). For the same reason all "
      "pianos can never be harps, so II is impossible.",
      ["Only a few pianos are flutes ⇒ some pianos are flutes", "Those pianos are not harps ⇒ I follows",
       "Since some pianos are certainly not harps, 'all pianos being harps' is impossible ⇒ II does not follow"],
      seconds=45)
syl_q("Intermediate", FEW, N(("ladder", "ladders"), ("rope", "ropes"), ("pole", "poles")),
      [("only", "rope", "ladder"), ("some", "ladder", "pole")],
      [("some", "rope", "pole"), ("poss_all", "pole", "ladder")], BOTH,
      "'Only ropes are ladders' means All ladders are ropes",
      "Every ladder is a rope, so the ladders that are poles are ropes: some ropes are poles (I). Nothing keeps any "
      "pole out of ladders, so all poles being ladders is possible (II).",
      ["Only ropes are ladders ⇒ All ladders are ropes", "Some ladders are poles ⇒ Some ropes are poles: I follows",
       "No statement separates poles from ladders ⇒ II is possible: follows"],
      why="Reading 'Only ropes are ladders' as 'All ropes are ladders' loses conclusion I.", seconds=50)
syl_q("Intermediate", FEW, N(("blanket", "blankets"), ("sheet", "sheets"), ("towel", "towels")),
      [("onlyfew", "blanket", "sheet"), ("all", "sheet", "towel")],
      [("all", "blanket", "towel"), ("some", "towel", "blanket")], ONLY_II,
      "Only a few + All = Some",
      "Some blankets are sheets and every sheet is a towel, so some towels are blankets (II). The blankets that are "
      "not sheets may lie outside towels, so I is not certain.",
      ["Some blankets are sheets ⊂ towels ⇒ Some towels are blankets: II follows",
       "Blankets outside sheets need not be towels ⇒ I does not follow"], seconds=45)
syl_q("Intermediate", FEW, N(("eagle", "eagles"), ("hawk", "hawks"), ("falcon", "falcons")),
      [("onlyfew", "eagle", "hawk"), ("only", "falcon", "hawk")],
      [("all", "eagle", "falcon"), ("somenot", "falcon", "hawk")], NEITHER,
      "'Only falcons are hawks' = All hawks are falcons (not the reverse)",
      "Every hawk is a falcon, so some eagles (the hawks among them) are falcons, but the other eagles may lie outside "
      "falcons: I is not certain. The falcons may be exactly the hawks, so 'Some falcons are not hawks' is not certain "
      "either (II).",
      ["Only falcons are hawks ⇒ All hawks are falcons", "Definite: Some eagles are falcons (not 'All') ⇒ I fails",
       "Falcons and hawks may coincide ⇒ II fails"], seconds=55)
syl_q("Intermediate", FEW, N(("sofa", "sofas"), ("bench", "benches"), ("stool", "stools")),
      [("some", "sofa", "bench"), ("onlyfew", "bench", "stool")],
      [("somenot", "bench", "stool"), ("some", "sofa", "stool")], ONLY_I,
      "'Only a few B are C' also says 'Some B are not C'",
      "'Only a few benches are stools' means some benches are stools and some are not, so I follows directly. The "
      "sofas that are benches may all lie in the non-stool part, so II is not certain.",
      ["Only a few benches are stools ⇒ Some benches are not stools: I follows",
       "Sofa–bench overlap may avoid stools ⇒ II does not follow"], seconds=45)
# ---- Advanced (three statements, four terms)
syl_q("Advanced", POSS, N(("ruby", "rubies"), ("emerald", "emeralds"), ("sapphire", "sapphires"),
                          ("diamond", "diamonds")),
      [("all", "ruby", "emerald"), ("onlyfew", "emerald", "sapphire"), ("no", "sapphire", "diamond")],
      [("somenot", "emerald", "diamond"), ("poss_all", "ruby", "sapphire")], BOTH,
      "A definite 'some not' plus an unblocked possibility",
      "Some emeralds are sapphires and no sapphire is a diamond, so those emeralds are not diamonds (I). The rubies "
      "lie inside emeralds and could all sit in the emerald–sapphire part; nothing forbids it, so II is possible.",
      ["Only a few emeralds are sapphires ⇒ some emeralds are sapphires", "No sapphire is a diamond ⇒ Some emeralds "
       "are not diamonds: I follows", "Rubies ⊂ emeralds; the emerald–sapphire part can hold all rubies ⇒ II follows"],
      seconds=60)
syl_q("Advanced", POSS, N(("wallet", "wallets"), ("purse", "purses"), ("bag", "bags"), ("pouch", "pouches")),
      [("some", "wallet", "purse"), ("no", "purse", "bag"), ("all", "bag", "pouch")],
      [("poss_all", "wallet", "bag"), ("somenot", "pouch", "purse")], ONLY_II,
      "A possibility fails when a definite statement blocks it",
      "The wallets that are purses can never be bags, so all wallets being bags is impossible (I fails). Bags exist, "
      "every bag is a pouch and no bag is a purse, so some pouches are not purses (II).",
      ["Some wallets are purses; purses never meet bags ⇒ some wallets are certainly not bags ⇒ I fails",
       "All bags are pouches and no bag is a purse ⇒ Some pouches are not purses: II follows"], seconds=60)
syl_q("Advanced", POSS, N(("cookie", "cookies"), ("cake", "cakes"), ("bread", "breads"), ("pie", "pies")),
      [("onlyfew", "cookie", "cake"), ("all", "cake", "bread"), ("somenot", "bread", "pie")],
      [("some", "cookie", "pie"), ("no", "cake", "pie")], NEITHER,
      "Different pairs in the two conclusions: no 'either' case",
      "Pies are linked only by 'Some breads are not pies', which forces nothing about cookies or cakes. A cookie–pie "
      "overlap is possible but not certain (I), and cakes may or may not be pies (II). The conclusions are about "
      "different pairs, so 'either' does not apply.",
      ["Definite: some cookies are cakes, hence some cookies are breads", "Pies may or may not meet cookies ⇒ I not "
       "certain", "Pies may or may not meet cakes ⇒ II not certain", "Different term pairs ⇒ not an either–or"],
      seconds=60)

# ================================================================================================ INEQUALITY
DIRECT, CODED = "Direct inequality", "Coded inequality"


def ineq_q3(*a, **kw):
    """ineq_q with a cross-check: the verdict must not change when every variable gets a wider value range."""
    chains, conclusions = a[3], a[4]
    assert ineq_eval(chains, conclusions) == ineq_eval(
        chains, conclusions, dom=len({x for c in chains for r in parse_chain(c) for x in (r[0], r[2])}) + 3)
    return ineq_q(*a, **kw)


# ---- Basic: direct (the chain is shown as separate pairwise statements)
def direct_split(chains, conc):
    pairs = [f"{a_} {o_} {b_}" for c in chains for a_, o_, b_ in parse_chain(c)]
    return ("Statements: " + ", ".join(pairs) + "\n\nAssuming the statements to be true, decide which of the "
            "conclusions below definitely follow.", chains, [parse_chain(c)[0] for c in conc], conc)


s, ch, cc, ct = direct_split(["E = F ≥ G < H ≤ I > J"], ["E ≥ G", "I > G"])
ineq_q3("Basic", DIRECT, s, ch, cc, ct, BOTH,
        "E = F ≥ G gives E ≥ G. G < H ≤ I gives I > G. Both follow.",
        ["I: E = F ≥ G → E ≥ G, true", "II: G < H ≤ I → I > G, true"], seconds=30)
s, ch, cc, ct = direct_split(["M < N = O ≥ P > Q ≤ R"], ["M < P", "O > Q"])
ineq_q3("Basic", DIRECT, s, ch, cc, ct, ONLY_II,
        "M < N = O ≥ P: the direction turns at O, so M and P cannot be compared. O ≥ P > Q gives O > Q.",
        ["I: M < N = O ≥ P: reversal at O → no relation", "II: O ≥ P > Q → O > Q, true"], seconds=30)
s, ch, cc, ct = direct_split(["S ≤ T < U > V = W ≥ X"], ["S < U", "T > X"])
ineq_q3("Basic", DIRECT, s, ch, cc, ct, ONLY_I,
        "S ≤ T < U gives S < U. T and X lie on opposite sides of U (T < U > V), so they cannot be compared.",
        ["I: S ≤ T < U → S < U, true", "II: T < U > V = W ≥ X: reversal at U → no relation"], seconds=30)
s, ch, cc, ct = direct_split(["A > B ≥ C ≤ D = E > F"], ["A > E", "B > F"])
ineq_q3("Basic", DIRECT, s, ch, cc, ct, NEITHER,
        "Both comparisons cross C, where the direction reverses (B ≥ C ≤ D), so neither can be established.",
        ["I: A > B ≥ C ≤ D = E: reversal at C → no relation", "II: B ≥ C ≤ D = E > F: reversal at C → no relation"],
        seconds=30)
s, ch, cc, ct = direct_split(["K ≥ L ≥ M = N ≤ O < P"], ["K > M", "K = M"])
ineq_q3("Basic", DIRECT, s, ch, cc, ct, EITHER,
        "K ≥ L ≥ M gives only K ≥ M. Neither K > M nor K = M is certain on its own, but together they make up K ≥ M, "
        "so one of them must be true: either I or II follows.",
        ["K ≥ L ≥ M → K ≥ M (no strict sign on the path)", "I (K > M) alone: not certain; II (K = M) alone: not "
         "certain", "I or II together = K ≥ M ⇒ Either I or II follows"],
        why="'Either' takes the place of 'Both' (four-option rule); K > M and K = M cannot both hold.", seconds=35)
s, ch, cc, ct = direct_split(["U < V ≤ W = X < Y > Z"], ["U < X", "Z < W"])
ineq_q3("Basic", DIRECT, s, ch, cc, ct, ONLY_I,
        "U < V ≤ W = X gives U < X. W and Z lie on opposite sides of Y (X < Y > Z), so Z < W is not certain.",
        ["I: U < V ≤ W = X → U < X, true", "II: W = X < Y > Z: reversal at Y → no relation"], seconds=30)
s, ch, cc, ct = direct_split(["G = H > I ≥ J < K ≤ L"], ["G < K", "I ≥ J"])
ineq_q3("Basic", DIRECT, s, ch, cc, ct, ONLY_II,
        "G and K are separated by the turn at J (I ≥ J < K), so G < K is not certain. I ≥ J is given directly.",
        ["I: G = H > I ≥ J < K: reversal at J → no relation", "II: I ≥ J, given in the statement → true"], seconds=30)

# ---- Intermediate: coded
CODE_D = {"π": ">", "σ": "<", "ω": "=", "φ": "≥", "ψ": "≤"}
CODE_D_TXT = ("In the following question, the symbols π, σ, ω, φ and ψ are used with these meanings:\n"
              "'P π Q' means 'P is neither smaller than nor equal to Q'; 'P σ Q' means 'P is neither greater than nor "
              "equal to Q'; 'P ω Q' means 'P is neither greater than nor smaller than Q'; 'P φ Q' means 'P is not "
              "smaller than Q'; 'P ψ Q' means 'P is not greater than Q'.\nAssuming the statements to be true, find "
              "which of the conclusions I and II is/are definitely true.")
s, ch, cc, ct = coded(CODE_D_TXT, CODE_D, ["A φ B", "B π C", "D ψ C", "D ω E"], ["A π E", "B σ E"])
ineq_q3("Intermediate", CODED, s, ch, cc, ct, ONLY_I,
        "Decoded: A ≥ B > C ≥ D = E. So A > E (I follows) and B > E, which makes B < E false (II).",
        ["Decode: π → >, σ → <, ω → =, φ → ≥, ψ → ≤", "A ≥ B, B > C, D ≤ C, D = E ⇒ A ≥ B > C ≥ D = E",
         "I: A π E means A > E: true", "II: B σ E means B < E: false (B > E)"],
        concept="Decoding worded symbols, then reading the chain", seconds=55)
s, ch, cc, ct = coded(CODE_D_TXT, CODE_D, ["M σ N", "N ψ O", "P φ O", "Q π P"], ["Q π N", "M σ P"])
ineq_q3("Intermediate", CODED, s, ch, cc, ct, BOTH,
        "Decoded: M < N ≤ O ≤ P < Q. So Q > N and M < P: both follow.",
        ["Decode: M < N, N ≤ O, P ≥ O, Q > P", "Chain: M < N ≤ O ≤ P < Q", "I: Q π N means Q > N: true",
         "II: M σ P means M < P: true"], concept="Decoding worded symbols, then reading the chain", seconds=55)

# ---- Advanced
s, ch, cc, ct = direct(["R ≥ S", "T < S", "U = T", "V > R", "W ≤ U"], ["R > V", "W = T"])
ineq_q3("Advanced", DIRECT, s, ch, cc, ct, NEITHER,
        "Combined: V > R ≥ S > T = U ≥ W. R > V contradicts V > R, and W ≤ U = T gives only W ≤ T, so W = T is not "
        "certain. The two conclusions are about different pairs, so 'either' does not arise.",
        ["Rewrite: V > R, R ≥ S, S > T, T = U, U ≥ W", "Chain: V > R ≥ S > T = U ≥ W", "I: R > V: false",
         "II: W = T: only W ≤ T is certain → not definite"], concept="Combining five statements into one chain",
        seconds=60)
CODE_E = {"♠": ">", "♣": "<", "♥": "=", "♦": "≥", "◎": "≤"}
CODE_E_TXT = ("In the following question, 'A ♠ B' means 'A is greater than B'; 'A ♣ B' means 'A is smaller than B'; "
              "'A ♥ B' means 'A is equal to B'; 'A ♦ B' means 'A is either greater than or equal to B'; 'A ◎ B' "
              "means 'A is either smaller than or equal to B'.\nAssuming the statements to be true, find which of the "
              "conclusions I and II is/are definitely true.")
s, ch, cc, ct = coded(CODE_E_TXT, CODE_E, ["F ♦ G", "G ♥ H", "H ♠ I", "J ◎ I", "J ♣ K"], ["K ♠ H", "G ♠ J"])
ineq_q3("Advanced", CODED, s, ch, cc, ct, ONLY_II,
        "Decoded: F ≥ G = H > I ≥ J < K. K and H lie on opposite sides of J, so K > H is not certain. G = H > I ≥ J "
        "gives G > J.",
        ["Decode: F ≥ G, G = H, H > I, J ≤ I, J < K", "Chain: F ≥ G = H > I ≥ J < K",
         "I: K ♠ H means K > H: reversal at J → no relation", "II: G ♠ J means G > J: true"],
        concept="Decoding symbols in a five-statement chain", seconds=65)
s, ch, cc, ct = direct(["P ≤ Q", "R > Q", "S ≥ R", "T = S", "U < T"], ["T > P", "U > Q"])
ineq_q3("Advanced", DIRECT, s, ch, cc, ct, ONLY_I,
        "Combined: P ≤ Q < R ≤ S = T > U. So T > P. U lies below T on a separate branch, so U and Q cannot be "
        "compared.",
        ["Chain: P ≤ Q < R ≤ S = T and U < T", "I: P ≤ Q < R ≤ S = T → T > P, true",
         "II: Q < … ≤ T > U: reversal at T → no relation"], concept="Combining five statements into one chain",
        seconds=60)
s, ch, cc, ct = direct(["C ≥ D", "D > E", "F = E", "G ≤ F", "H ≥ C"], ["H > G", "D ≥ F"])
ineq_q3("Advanced", DIRECT, s, ch, cc, ct, BOTH,
        "Combined: H ≥ C ≥ D > E = F ≥ G. H > G (one strict sign on the path), and D > E = F gives D > F, which "
        "makes D ≥ F true as well.",
        ["Chain: H ≥ C ≥ D > E = F ≥ G", "I: H > G: true", "II: D > F, so D ≥ F is definitely true"],
        why="A strict relation (D > F) also makes the weaker 'D ≥ F' true.",
        concept="Combining five statements into one chain", seconds=60)
s, ch, cc, ct = coded(CODE_D_TXT, CODE_D, ["U π V", "W φ V", "W ψ X", "Y ω X", "Z σ Y"], ["X π V", "X ω V"])
ineq_q3("Advanced", CODED, s, ch, cc, ct, EITHER,
        "Decoded: U > V ≤ W ≤ X = Y > Z. From V to X: V ≤ W ≤ X, so X ≥ V. X > V and X = V are each uncertain, but "
        "one of them must hold: either I or II follows.",
        ["Decode: U > V, W ≥ V, W ≤ X, Y = X, Z < Y", "Chain: U > V ≤ W ≤ X = Y > Z ⇒ X ≥ V",
         "I (X > V) or II (X = V) together = X ≥ V ⇒ Either"],
        why="'Either' replaces 'Both' (four-option rule).", concept="Worded symbols; the either-or case", seconds=65)
CANDS = ["X ≥ W = Y > V ≥ Z", "X > Y ≥ W = V > Z", "Z ≤ V ≤ Y ≤ W = X", "X > V ≥ Z = W < Y"]
good = []
for e in CANDS:
    f1, f2, _ = ineq_eval([e], [("X", ">", "Z"), ("W", "≥", "Y")])
    if f1 and f2:
        good.append(e)
assert good == [CANDS[0]]
mcq(INQ, DIRECT, "Advanced",
    "In which of the following expressions are both 'X > Z' and 'W ≥ Y' definitely true?", good[0], CANDS[1:],
    "Testing every expression against both conclusions",
    "In X ≥ W = Y > V ≥ Z all signs from X to Z point the same way with one strict sign, so X > Z; and W = Y gives "
    "W ≥ Y. Every other expression fails one of the two.",
    ["X ≥ W = Y > V ≥ Z: X > Z true; W = Y ⇒ W ≥ Y true",
     "X > Y ≥ W = V > Z: X > Z true, but Y ≥ W gives W ≤ Y, so W ≥ Y is not certain",
     "Z ≤ V ≤ Y ≤ W = X: W ≥ Y true, but only X ≥ Z (no strict sign), so X > Z is not certain",
     "X > V ≥ Z = W < Y: X > Z true, but W < Y makes W ≥ Y false"],
    seconds=75, verified_by=EXHAUST)
CH = ["J > K ≥ L", "M ≤ L", "N > M", "O = K"]
CC = [("J", ">", "M"), ("N", ">", "L"), ("O", ">", "L"), ("N", "≥", "K")]
rels = [r for c in CH for r in parse_chain(c)]
vs = sorted({x for a_, _, b_ in rels for x in (a_, b_)})
sats = [dict(zip(vs, vals)) for vals in itertools.product(range(len(vs) + 2), repeat=len(vs))
        if all(REL[o](dict(zip(vs, vals))[a_], dict(zip(vs, vals))[b_]) for a_, o, b_ in rels)]
ok = [c for c in CC if all(REL[c[1]](v[c[0]], v[c[2]]) for v in sats)]
assert ok == [CC[0]]
mcq(INQ, DIRECT, "Advanced",
    "Statement: " + "; ".join(CH) + "\n\nWhich of the following conclusions is definitely true?",
    " ".join(CC[0]), [" ".join(c) for c in CC[1:]], "Checking each option against the combined chain",
    "Combined: J > K ≥ L ≥ M < N, with O = K. From J down to M every sign points the same way and one is strict, so "
    "J > M. N lies above M on a separate branch, so N cannot be compared with L or K; and O = K ≥ L gives only "
    "O ≥ L.",
    ["Chain: J > K ≥ L ≥ M < N; O = K", "J > M: J > K ≥ L ≥ M → true",
     "N > L and N ≥ K: N and L/K are joined only through M, where the direction turns → not definite",
     "O > L: O = K ≥ L gives only O ≥ L → not definite"],
    seconds=70, verified_by=EXHAUST)

# ================================================================================================ BLOOD RELATIONS
# ---- Basic (standalone)
F = Family().add("Gf", "M").add("Gm", "F").marry("Gf", "Gm").add("Sunita", "F", "Gf", "Gm")
F.add("Bro", "M", "Gf", "Gm").add("Wife", "F").marry("Bro", "Wife").add("Boy", "M", "Bro", "Wife")
assert [c for c in F.children("Gm") if F.g[c] == "M"] == ["Bro"]
ans = F.rel("Sunita", "Boy")
assert ans == "aunt"
mcq(BLD, "Direct relation", "Basic",
    "Introducing a boy, Sunita said, \"His father is the only son of my mother.\" How is Sunita related to the boy?",
    cap(ans), ["Mother", "Sister", "Grandmother"], "Collapsing 'the only son of my mother'",
    "Sunita's mother's only son is Sunita's brother. The boy's father is therefore Sunita's brother, so Sunita is "
    "the boy's father's sister: his aunt.",
    ["My mother's only son = Sunita's brother", "Boy's father = Sunita's brother",
     "Father's sister = aunt (paternal aunt)"],
    why_others_wrong="Mother would need Sunita to be the boy's parent, but his father is her brother; sister would "
                     "need the same father for both.", seconds=30, verified_by=RECOMP)
F = Family().add("Rf", "M").add("Rm", "F").marry("Rf", "Rm").add("Q", "M", "Rf", "Rm").add("S", "F", "Rf", "Rm")
F.add("P", "F").marry("P", "Q")
assert [c for c in F.children("Rf") if F.g[c] == "F"] == ["S"]
ans = F.rel("S", "P")
assert ans == "sister-in-law"
mcq(BLD, "Direct relation", "Basic",
    "P is the wife of Q. R is the father of Q. S is the only daughter of R. How is S related to P?", cap(ans),
    ["Sister", "Mother-in-law", "Daughter"], "Husband's sister = sister-in-law",
    "R is Q's father and S is R's daughter, so S is Q's sister. P is Q's wife, so S is P's husband's sister: her "
    "sister-in-law.", ["R is Q's father; S is R's daughter ⇒ S is Q's sister", "P is Q's wife",
                        "Husband's sister ⇒ sister-in-law"],
    why_others_wrong="Mother-in-law would be R's wife; S is not P's own sister or daughter.", seconds=30,
    verified_by=RECOMP)
F = Family().add("Gf", "M").add("Gm", "F").marry("Gf", "Gm").add("Rakesh", "M", "Gf", "Gm").add("Rw", "F")
F.marry("Rakesh", "Rw").add("Tanvi", "F", "Rakesh", "Rw")
assert [c for c in F.children("Gf") if F.g[c] == "M"] == ["Rakesh"]
ans = F.rel("Rakesh", "Tanvi")
assert ans == "father"
mcq(BLD, "Direct relation", "Basic",
    "Tanvi's father is the only son of Rakesh's father. Rakesh is a man. How is Rakesh related to Tanvi?", cap(ans),
    ["Uncle", "Grandfather", "Brother"], "'The only son of my father' is the man himself",
    "Rakesh is a son of his own father, and his father has only one son, so that only son is Rakesh. Tanvi's father "
    "is therefore Rakesh.",
    ["Rakesh's father's sons include Rakesh", "'Only son' ⇒ the only son is Rakesh", "Tanvi's father = Rakesh"],
    why_others_wrong="Uncle would need Rakesh's father to have a second son; grandfather and brother ignore the word "
                     "'only'.", seconds=30, verified_by=RECOMP)

# ---- Intermediate: coded set
CODE_BR = {"↑": "father", "↓": "daughter", "→": "sister", "←": "husband", "↔": "son"}
BTXT = ("In a certain code:\n'A ↑ B' means 'A is the father of B';\n'A ↓ B' means 'A is the daughter of B';\n"
        "'A → B' means 'A is the sister of B';\n'A ← B' means 'A is the husband of B';\n'A ↔ B' means 'A is the son "
        "of B'.\n\nEach question gives a coded expression; use only the relations it states.")
sid = stimulus("passage", "Arrow codes for relations", BTXT, None,
               "Decode each symbol from left to right, draw the persons as a family tree (fathers, mothers, spouses, "
               "children) and read the asked relation off the tree. A person's gender follows from the relation "
               "they are given (father, son, husband: male; daughter, sister: female) or from their spouse.")
BQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    BLD, "Coded blood relation", "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid,
    verified_by=RECOMP, **kw)
F = Family().add("P", "M").add("S", "F").marry("P", "S").add("Q", "F", "P", "S").add("R", "F", "P", "S")
F.check(coded_facts("P ↑ Q → R ↓ S", CODE_BR))
ans = F.rel("P", "S")
assert ans == "husband"
BQ("If 'P ↑ Q → R ↓ S', how is P related to S?", cap(ans), ["Father", "Brother", "Son"],
   "Two parents of the same child",
   "P is Q's father; Q is R's sister, so P is R's father too. R is S's daughter, so S is R's other parent. Since P is "
   "the father, S is the mother, and P is S's husband.",
   ["P ↑ Q: P is Q's father", "Q → R: Q and R are sisters ⇒ P is R's father", "R ↓ S: S is R's parent ⇒ S is the "
    "mother", "P is S's husband"],
   why_others_wrong="Father would make S P's child, but S is a parent of P's daughter R.", seconds=55)
F = Family().add("Kf", "M").add("Km", "F").marry("Kf", "Km").add("L", "F", "Kf", "Km").add("M", "M", "Kf", "Km")
F.add("K", "M").marry("K", "L").add("J", "M", "K", "L")
F.check(coded_facts("J ↔ K ← L → M", CODE_BR))
ans = F.rel("J", "M")
assert ans == "nephew"
BQ("If 'J ↔ K ← L → M', how is J related to M?", cap(ans), ["Son", "Cousin", "Brother-in-law"],
   "Mother's sibling's relation to the child",
   "J is K's son and K is L's husband, so L is J's mother. L is M's sister, so M is J's mother's sibling, and J is "
   "M's nephew.",
   ["J ↔ K: J is K's son", "K ← L: K is L's husband ⇒ L is J's mother", "L → M: L is M's sister",
    "J = son of M's sister ⇒ nephew"],
   why_others_wrong="Cousin is J's relation to M's children; brother-in-law is K's relation to M.", seconds=55)
F = Family().add("Uf", "M").add("Um", "F").marry("Uf", "Um").add("U", "F", "Uf", "Um").add("V", "M", "Uf", "Um")
F.add("X", "F").marry("V", "X").add("W", "M", "V", "X")
F.check(coded_facts("U → V ↑ W ↔ X", CODE_BR))
ans = F.rel("U", "X")
assert ans == "sister-in-law"
BQ("If 'U → V ↑ W ↔ X', how is U related to X?", cap(ans), ["Sister", "Mother-in-law", "Aunt"],
   "The other parent of a child is the father's wife",
   "U is V's sister; V is W's father; W is X's son, so X is W's other parent, i.e. V's wife. U is the sister of X's "
   "husband: X's sister-in-law.",
   ["U → V: U is V's sister", "V ↑ W: V is W's father", "W ↔ X: X is W's parent ⇒ X is V's wife",
    "Husband's sister ⇒ sister-in-law"],
   why_others_wrong="Aunt is U's relation to W, not to X; mother-in-law would be V's mother.", seconds=60)
opts = {"A ↑ B ↑ C": None, "A ↑ B ↓ C": None, "A ↔ B ↑ C": None, "A ← B ↓ C": None}
F1 = Family().add("A", "M").add("Aw", "F").marry("A", "Aw").add("B", "M", "A", "Aw").add("Bw", "F").marry("B", "Bw")
F1.add("C", "M", "B", "Bw")
F1.check(coded_facts("A ↑ B ↑ C", CODE_BR))
opts["A ↑ B ↑ C"] = F1.rel("A", "C")
F2 = Family().add("A", "M").add("C", "F").marry("A", "C").add("B", "F", "A", "C")
F2.check(coded_facts("A ↑ B ↓ C", CODE_BR))
opts["A ↑ B ↓ C"] = F2.rel("A", "C")
F3 = Family().add("B", "M").add("Bw", "F").marry("B", "Bw").add("A", "M", "B", "Bw").add("C", "M", "B", "Bw")
F3.check(coded_facts("A ↔ B ↑ C", CODE_BR))
opts["A ↔ B ↑ C"] = F3.rel("A", "C")
F4 = Family().add("C", "M").add("Cw", "F").marry("C", "Cw").add("B", "F", "C", "Cw").add("A", "M").marry("A", "B")
F4.check(coded_facts("A ← B ↓ C", CODE_BR))
opts["A ← B ↓ C"] = F4.rel("A", "C")
assert opts == {"A ↑ B ↑ C": "grandfather", "A ↑ B ↓ C": "husband", "A ↔ B ↑ C": "brother",
                "A ← B ↓ C": "son-in-law"}
BQ("Which of the following expressions means that A is the grandfather of C?", "A ↑ B ↑ C",
   ["A ↑ B ↓ C", "A ↔ B ↑ C", "A ← B ↓ C"], "Testing each expression",
   "'A ↑ B ↑ C': A is B's father and B is C's father, so A is C's grandfather. In 'A ↑ B ↓ C', C is the mother of "
   "A's daughter (A's wife); in 'A ↔ B ↑ C', A and C are both B's sons (brothers); in 'A ← B ↓ C', A is the husband "
   "of C's daughter (son-in-law).",
   ["A ↑ B ↑ C: father of father ⇒ grandfather", "A ↑ B ↓ C ⇒ A is C's husband",
    "A ↔ B ↑ C ⇒ A is C's brother", "A ← B ↓ C ⇒ A is C's son-in-law"], seconds=60)

# ---- Intermediate: family with professions (tree fixed by the relation clues; professions found by enumeration)
F = Family().add("Ramesh", "M").add("Savita", "F").marry("Ramesh", "Savita")
F.add("Vikas", "M", "Ramesh", "Savita").add("Anjali", "F", "Ramesh", "Savita").add("Pooja", "F").marry("Vikas", "Pooja")
F.add("Dhruv", "M", "Vikas", "Pooja").add("Kriti", "F", "Vikas", "Pooja")
MEM = ["Ramesh", "Savita", "Vikas", "Anjali", "Pooja", "Dhruv", "Kriti"]
PROF = ["Banker", "Doctor", "Engineer", "Lawyer", "Pilot", "Student", "Teacher"]
pclues = [
    lambda w: {w["Lawyer"], w["Teacher"]} == {"Ramesh", "Savita"},
    lambda w: w["Lawyer"] != "Savita",
    lambda w: F.rel(w["Engineer"], w["Banker"]) == "father",
    lambda w: F.rel(w["Doctor"], w["Teacher"]) == "daughter-in-law",
    lambda w: F.rel(w["Student"], w["Banker"]) == "brother",
]
sols = []
for perm in itertools.permutations(MEM):
    w = dict(zip(PROF, perm))
    if all(c(w) for c in pclues):
        sols.append(w)
assert len(sols) == 1
WHO = sols[0]
PR = {v: k for k, v in WHO.items()}
assert PR == {"Ramesh": "Lawyer", "Savita": "Teacher", "Vikas": "Engineer", "Pooja": "Doctor", "Anjali": "Pilot",
              "Dhruv": "Student", "Kriti": "Banker"}
FTXT = ("A family has seven members of three generations: Ramesh, Savita, Vikas, Anjali, Pooja, Dhruv and Kriti. "
        "Ramesh, Vikas and Dhruv are male; the others are female. Each member has a different profession among "
        "Banker, Doctor, Engineer, Lawyer, Pilot, Student and Teacher.\n\n"
        "- Ramesh and Savita are married to each other; Vikas and Anjali are their only children.\n"
        "- Pooja is the wife of Vikas, and Dhruv and Kriti are their children.\n"
        "- The Lawyer and the Teacher are the two members of the oldest generation, and Savita is not the Lawyer.\n"
        "- The Engineer is the father of the Banker.\n- The Doctor is the daughter-in-law of the Teacher.\n"
        "- The Student is the brother of the Banker.")
sid = stimulus("puzzle", "A three-generation family with professions", FTXT, None,
               "Ramesh is the Lawyer and Savita the Teacher. Savita's only daughter-in-law is Pooja: the Doctor. The "
               "Engineer is a father, and the only father outside the oldest generation is Vikas, so Vikas is the "
               "Engineer and the Banker is Dhruv or Kriti. The Student is the Banker's brother, so the Banker is "
               "Kriti and the Student Dhruv. Anjali is the Pilot.\n\n"
               + table(["Member", "Relation", "Profession"],
                       [("Ramesh", "grandfather", "Lawyer"), ("Savita", "grandmother", "Teacher"),
                        ("Vikas", "son of Ramesh and Savita", "Engineer"), ("Anjali", "daughter of Ramesh and Savita",
                                                                             "Pilot"),
                        ("Pooja", "wife of Vikas", "Doctor"), ("Dhruv", "son of Vikas and Pooja", "Student"),
                        ("Kriti", "daughter of Vikas and Pooja", "Banker")]))
BQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    BLD, "Family puzzle", "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid,
    verified_by=("script:enumerate-models", "ai:author-solve"), **kw)
BQ("What is Anjali's profession?", PR["Anjali"], ["Doctor", "Teacher", "Banker"], "Elimination after fixing the "
   "rest", "Lawyer, Teacher (oldest generation), Doctor (Savita's daughter-in-law), Engineer (the father), Banker and "
   "Student (the two children) are all taken by others, so Anjali is the Pilot.",
   ["Ramesh Lawyer, Savita Teacher", "Pooja Doctor", "Vikas Engineer", "Kriti Banker, Dhruv Student",
    "Anjali Pilot"], seconds=60)
ans = F.rel(WHO["Banker"], WHO["Engineer"])
assert ans == "daughter"
BQ("How is the Banker related to the Engineer?", cap(ans), ["Son", "Sister", "Niece"],
   "Profession → person → relation", "The Banker is Kriti and the Engineer is Vikas, her father: she is his "
   "daughter.", ["Banker = Kriti; Engineer = Vikas", "Kriti is Vikas's daughter"], seconds=55)
ans = F.rel(WHO["Lawyer"], WHO["Student"])
assert ans == "grandfather"
BQ("How is the Lawyer related to the Student?", cap(ans), ["Father", "Uncle", "Father-in-law"],
   "Two generations apart", "The Lawyer is Ramesh and the Student is Dhruv, the son of Ramesh's son Vikas: Ramesh is "
   "his grandfather.", ["Lawyer = Ramesh; Student = Dhruv", "Dhruv's father Vikas is Ramesh's son ⇒ grandfather"],
   seconds=55)
ans = F.rel(WHO["Pilot"], WHO["Doctor"])
assert ans == "sister-in-law"
BQ("How is the Pilot related to the Doctor?", cap(ans), ["Sister", "Daughter", "Mother-in-law"],
   "Husband's sister = sister-in-law", "The Pilot is Anjali and the Doctor is Pooja; Anjali is the sister of Pooja's "
   "husband Vikas, so she is Pooja's sister-in-law.", ["Pilot = Anjali; Doctor = Pooja",
                                                       "Anjali is Vikas's sister; Vikas is Pooja's husband"],
   seconds=55)

# ---- Advanced (standalone)
CODE_X = {"!": "mother", "?": "son", "~": "sister", "^": "husband", "=": "daughter"}
res = {}
G = Family().add("Mh", "M").add("M", "F").marry("Mh", "M").add("N", "M", "Mh", "M").add("Q", "F").marry("N", "Q")
G.check(coded_facts("M ! N ^ Q", CODE_X))
res["M ! N ^ Q"] = G.rel("M", "Q")
G = Family().add("Q", "M").add("M", "F").marry("Q", "M").add("N", "M", "Q", "M")
G.check(coded_facts("M ! N ? Q", CODE_X))
res["M ! N ? Q"] = G.rel("M", "Q")
G = Family().add("Pf", "M").add("Pm", "F").marry("Pf", "Pm").add("M", "F", "Pf", "Pm").add("N", "F", "Pf", "Pm")
G.add("Nh", "M").marry("Nh", "N").add("Q", "F", "Nh", "N")
G.check(coded_facts("M ~ N ! Q", CODE_X))
res["M ~ N ! Q"] = G.rel("M", "Q")
G = Family().add("N", "M").add("Q", "F").marry("N", "Q").add("M", "F", "N", "Q")
G.check(coded_facts("M = N ^ Q", CODE_X))
res["M = N ^ Q"] = G.rel("M", "Q")
assert res == {"M ! N ^ Q": "mother-in-law", "M ! N ? Q": "wife", "M ~ N ! Q": "aunt", "M = N ^ Q": "daughter"}
mcq(BLD, "Coded blood relation", "Advanced",
    "In a certain code:\n'A ! B' means 'A is the mother of B';\n'A ? B' means 'A is the son of B';\n'A ~ B' means "
    "'A is the sister of B';\n'A ^ B' means 'A is the husband of B';\n'A = B' means 'A is the daughter of B'.\n\n"
    "Which of the following expressions means that M is the mother-in-law of Q?", "M ! N ^ Q",
    ["M ! N ? Q", "M ~ N ! Q", "M = N ^ Q"], "Mother of one's spouse = mother-in-law",
    "'M ! N ^ Q': M is N's mother and N is Q's husband, so M is the mother of Q's husband: Q's mother-in-law. In "
    "'M ! N ? Q', N is the son of M and of Q, so M is Q's wife. In 'M ~ N ! Q', M is the sister of Q's mother (aunt). "
    "In 'M = N ^ Q', M is the daughter of N and of N's wife Q.",
    ["M ! N ^ Q ⇒ M is Q's husband's mother ⇒ mother-in-law", "M ! N ? Q ⇒ M and Q are N's parents ⇒ M is Q's wife",
     "M ~ N ! Q ⇒ M is Q's aunt", "M = N ^ Q ⇒ M is Q's daughter"], seconds=80, verified_by=RECOMP)
# four generations: generation numbers counted along recorded parent links
par = {"Jatin": ("Harish", "Ganga"), "Kamal": ("Jatin", "Indu"), "Manya": ("Kamal", "Leela")}
gen = {"Harish": 1, "Ganga": 1}
for c in ("Jatin", "Kamal", "Manya"):
    gen[c] = gen[par[c][0]] + 1
assert gen["Manya"] - gen["Ganga"] == 3
mcq(BLD, "Family puzzle", "Advanced",
    "A family has seven members: Ganga, Harish, Indu, Jatin, Kamal, Leela and Manya.\n"
    "- Ganga is the wife of Harish, and Jatin is their only child.\n- Jatin is married to Indu.\n"
    "- Kamal is the only son of Indu.\n- Leela's husband is the only grandson of Harish.\n"
    "- Manya is the daughter of Leela.\n\nHow is Manya related to Ganga?", "Great-granddaughter",
    ["Granddaughter", "Grandniece", "Great-grandmother"], "Counting generations along parent links",
    "Jatin is Ganga's son. Kamal is the son of Indu, Jatin's wife, so Kamal is Ganga's grandson; Harish has no other "
    "child, so Kamal is his only grandson and Leela is Kamal's wife. Manya is Kamal's daughter: three generations "
    "below Ganga, i.e. her great-granddaughter.",
    ["Generation 1: Harish + Ganga", "Generation 2: their only child Jatin (+ Indu)",
     "Generation 3: Kamal, son of Jatin and Indu = Harish's only grandson (+ Leela)",
     "Generation 4: Manya, daughter of Kamal and Leela ⇒ great-granddaughter of Ganga"],
    why_others_wrong="Granddaughter skips a generation; grandniece needs a sibling link that does not exist; "
                     "great-grandmother reverses the relation.", seconds=75, verified_by=RECOMP)

# ================================================================================================ DIRECTION SENSE
x, y = walk("S", [(None, 9), ("L", 12), ("L", 4)])
assert (x, y) == (12, -5)
mcq(DIR, "Distance and direction", "Basic",
    "Rakesh walks 9 m towards the south. He then turns left and walks 12 m, and then turns left again and walks 4 m. "
    "How far is he now from his starting point, and in which direction?", f"{dist(x, y)} m, {compass(x, y)}",
    ["13 m, South-West", "25 m, South-East", "15 m, North-East"], "Net displacement with a 5-12-13 triangle",
    "Left from south is east, and left from east is north. He ends 12 m east and 9 − 4 = 5 m south of the start: "
    "√(144 + 25) = 13 m, towards the south-east.",
    ["9 m south → (0, −9)", "Left from south = east; 12 m → (12, −9)", "Left from east = north; 4 m → (12, −5)",
     "√(12² + 5²) = 13 m; east and south ⇒ South-East"],
    why_others_wrong="South-West mixes up the first left turn; 25 m adds the legs; North-East ignores that he is "
                     "still south of the start.", seconds=40, verified_by=RECOMP)
# shadow: morning sun in the east, so shadows point west
face0 = [f for f in CW if turn(f, "L") == "W"]  # shadow (west) on his left
assert face0 == ["N"]
face1 = turn(turn(face0[0], "R"), "R")
side = {turn(face1, "R"): "To his right", turn(face1, "L"): "To his left", face1: "In front of him",
        turn(turn(face1, "R"), "R"): "Behind him"}["W"]
assert face1 == "S" and side == "To his right"
mcq(DIR, "Shadow-based", "Intermediate",
    "One morning after sunrise, Vivek was walking along a straight road and his shadow fell exactly to his left. He "
    "then turned right twice, 90° each time, and kept walking. Where does his shadow fall now?", side,
    ["To his left", "Behind him", "In front of him"], "Morning shadows point west",
    "In the morning the sun is in the east, so shadows point west. A shadow on his left means west is his left, so "
    "he was facing north. Two right turns make him face south, and for a person facing south the west is on the "
    "right.",
    ["Morning: sun in the east ⇒ shadow towards the west", "West on his left ⇒ facing north",
     "Two right turns: north → east → south", "Facing south, west is to the right ⇒ shadow to his right"],
    why_others_wrong="'To his left' ignores the turns; a shadow falls behind or in front only when facing east or "
                     "west.", seconds=50, verified_by=RECOMP)
x, y = walk("N", [(None, 1)] + [("R", k) for k in range(2, 11)])
assert (x, y) == (6, 5) and dist(x, y) == "√61"
mcq(DIR, "Distance and direction", "Advanced",
    "A robot starts at point O facing north. It moves 1 m forward, turns right and moves 2 m, turns right and moves "
    "3 m, and so on: before every move after the first it turns right, and each move is 1 m longer than the one "
    "before. It stops after its tenth move, of 10 m. How far is it from O, and in which direction?",
    f"{dist(x, y)} m, {compass(x, y)}", ["√61 m, North-West", "11 m, North-East", "5 m, East"],
    "A square spiral: add the moves in each direction",
    "The moves go north, east, south, west in turn. North: 1 + 5 + 9 = 15; south: 3 + 7 = 10; east: 2 + 6 + 10 = 18; "
    "west: 4 + 8 = 12. Net: 5 m north and 6 m east, so the distance is √(25 + 36) = √61 m, towards the north-east.",
    ["Directions repeat N, E, S, W: moves 1, 5, 9 north; 2, 6, 10 east; 3, 7 south; 4, 8 west",
     "North − south = 15 − 10 = 5", "East − west = 18 − 12 = 6", "√(5² + 6²) = √61 m, North-East"],
    why_others_wrong="North-West swaps east and west; 11 m adds the two net components; 5 m, East ignores the "
                     "northward component and the eastward sum.", seconds=90, verified_by=RECOMP)

# ================================================================================================ CODING-DECODING
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


# ---- Basic (standalone)
opp_ = lambda w: "".join(AL[26 - pos(c)] for c in w)
assert opp_("FOREST") == "ULIVHG"
ans = inferred([("FOREST", "ULIVHG")], "MARKET", opp_("MARKET"))
assert ans == "NZIPVG"
mcq(COD, LC, "Basic", "In a certain code language, FOREST is written as ULIVHG. How is MARKET written in that code "
    "language?", ans, ["NZIQVG", "LZIPVF", "OBJPWH"], "Opposite letters: A↔Z, B↔Y, C↔X, …",
    "F (6) ↔ U (21), O (15) ↔ L (12), R ↔ I, E ↔ V, S ↔ H, T ↔ G: each letter is replaced by its opposite, the "
    "letter whose position adds up with it to 27. MARKET: M ↔ N, A ↔ Z, R ↔ I, K ↔ P, E ↔ V, T ↔ G.",
    ["Check: F+U = 6+21 = 27, O+L = 15+12 = 27 …", "MARKET → N Z I P V G", f"Code: {ans}"],
    why_others_wrong="NZIQVG takes K as Q; LZIPVF and OBJPWH shift some letters instead of using opposites.",
    seconds=35, verified_by=RECOMP)
rs = lambda w: shift(w[::-1], 1)
assert rs("CANDLE") == "FMEOBD"
ans = inferred([("CANDLE", "FMEOBD")], "BUTTER", rs("BUTTER"))
assert ans == "SFUUVC"
mcq(COD, LC, "Basic", "In a certain code, CANDLE is written as FMEOBD. How is BUTTER written in that code?", ans,
    ["CVUUFS", "QDSSTA", "SFUUVD"], "Reverse the word, then move each letter one step forward",
    "CANDLE reversed is ELDNAC; moving each letter one step forward gives FMEOBD. BUTTER reversed is RETTUB, and one "
    f"step forward gives {ans}.", ["Check: CANDLE → ELDNAC → +1 → FMEOBD", "BUTTER → RETTUB", f"+1 → {ans}"],
    why_others_wrong="CVUUFS shifts without reversing; QDSSTA reverses and shifts backwards; SFUUVD gets the last "
                     "letter wrong.", seconds=40, verified_by=RECOMP)
pl = lambda w: "".join(shift(c, i + 1) for i, c in enumerate(w))
assert pl("SMILE") == "TOLPJ"
ans = inferred([("SMILE", "TOLPJ")], "BRAVE", pl("BRAVE"))
assert ans == "CTDZJ"
mcq(COD, LC, "Basic", "In a certain code, SMILE is written as TOLPJ. How is BRAVE written in that code?", ans,
    ["CSBWF", "CTDZK", "DTDZJ"], "Each letter moves forward by its own position number",
    "S + 1 = T, M + 2 = O, I + 3 = L, L + 4 = P, E + 5 = J. BRAVE: B + 1 = C, R + 2 = T, A + 3 = D, V + 4 = Z, "
    f"E + 5 = J → {ans}.", ["Check SMILE: +1, +2, +3, +4, +5 → TOLPJ", f"BRAVE → {ans}"],
    why_others_wrong="CSBWF moves every letter by 1; CTDZK adds 6 to the last letter; DTDZJ adds 2 to the first.",
    seconds=40, verified_by=RECOMP)
NRULES = {"sum": lambda w: sum(pos(c) for c in w), "sum×len": lambda w: sum(pos(c) for c in w) * len(w),
          "sum+len": lambda w: sum(pos(c) for c in w) + len(w), "product": lambda w: __import__("math").prod(
              pos(c) for c in w), "reverse-sum": lambda w: sum(27 - pos(c) for c in w),
          "weighted-left": lambda w: sum(pos(c) * (i + 1) for i, c in enumerate(w)),
          "weighted-right": lambda w: sum(pos(c) * (len(w) - i) for i, c in enumerate(w)),
          "ends-product": lambda w: pos(w[0]) * pos(w[-1]), "consonants-vowels": lambda w: sum(
              pos(c) if c not in VOW else -pos(c) for c in w), "sum-len": lambda w: sum(pos(c) for c in w) - len(w)}
ans = inferred([("BAG", 10), ("DIG", 20)], "HIDE", 26, NRULES)
mcq(COD, NC, "Basic", "In a certain code, BAG is written as 10 and DIG is written as 20. How is HIDE written in that "
    "code?", str(ans), ["22", "30", "104"], "Sum of the alphabet positions",
    "BAG: 2 + 1 + 7 = 10; DIG: 4 + 9 + 7 = 20. HIDE: 8 + 9 + 4 + 5 = 26.",
    ["B 2 + A 1 + G 7 = 10 ✓; D 4 + I 9 + G 7 = 20 ✓", "HIDE: 8 + 9 + 4 + 5 = 26"],
    why_others_wrong="22 leaves out D (4); 30 adds the number of letters; 104 multiplies the "
                     "sum by the number of letters.", natural=int, seconds=35, verified_by=RECOMP)
assert NRULES["sum+len"]("HIDE") == 30 and NRULES["sum×len"]("HIDE") == 104
# ---- Basic: sentence-coding set
SENTS = [(["green", "fields", "need", "rain"], ["ka", "mo", "zi", "lu"]),
         (["rain", "helps", "the", "crops"], ["zi", "pe", "ra", "ne"]),
         (["crops", "need", "care"], ["ne", "mo", "fa"]),
         (["care", "for", "green", "fields"], ["fa", "ka", "lu", "bo"])]
sid = stimulus("passage", "Four coded sentences about farming",
               "In a certain code language:\n" + "\n".join(f"'{' '.join(w)}' is written as '{' '.join(c)}'"
                                                           for w, c in SENTS)
               + "\n\n(The codes of the words in a sentence may appear in any order.)", None,
               "need = mo (sentences 1 and 3); rain = zi (sentences 1 and 2); crops = ne (sentences 2 and 3); care = "
               "fa (sentences 3 and 4); green and fields share {ka, lu} (sentences 1 and 4) and cannot be told apart; "
               "for = bo (sentence 4); helps and the share {pe, ra}.")
SQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    COD, SW, "Basic", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
assert sentence_solve(SENTS, "crops") == {"ne"}
SQ("What is the code for 'crops'?", "ne", ["zi", "mo", "fa"], "One common word, one common code",
   "'crops' appears in sentences 2 and 3, whose only common code is ne.",
   ["Sentence 2: zi pe ra ne; sentence 3: ne mo fa", "Common code: ne ⇒ crops = ne"], seconds=40)
assert sentence_solve(SENTS, "bo") == {"for"}
SQ("Which word is coded as 'bo'?", "for", ["care", "green", "fields"], "Eliminating the known words",
   "Sentence 4 is 'care for green fields' = 'fa ka lu bo'. care = fa (shared with sentence 3) and green and fields "
   "take ka and lu (shared with sentence 1), so bo = for.",
   ["care = fa (sentences 3 & 4)", "{green, fields} = {ka, lu} (sentences 1 & 4)", "Remaining: for = bo"],
   seconds=45)
assert sentence_solve(SENTS, "need") == {"mo"} and sentence_solve(SENTS, "rain") == {"zi"}
SQ("What is the code for 'need rain'?", "mo zi", ["mo ka", "zi lu", "ne zi"], "Codes of two words",
   "need appears in sentences 1 and 3 (common code mo), and rain in sentences 1 and 2 (common code zi).",
   ["need: {ka mo zi lu} ∩ {ne mo fa} = mo", "rain: {ka mo zi lu} ∩ {zi pe ra ne} = zi", "need rain = mo zi"],
   seconds=45)

# ---- Intermediate (standalone)
vc = lambda w: "".join(shift(c, 1 if c in VOW else -1) for c in w)
assert vc("TRAIN") == "SQBJM" and vc("BUS") == "AVR"
ans = inferred([("TRAIN", "SQBJM"), ("BUS", "AVR")], "METRO", vc("METRO"))
assert ans == "LFSQP"
mcq(COD, LC, "Intermediate",
    "In a certain code, TRAIN is written as SQBJM and BUS is written as AVR. How is METRO written in that code?", ans,
    ["LDSQN", "NFUSP", "LFSQN"], "Vowels and consonants move in opposite directions",
    "TRAIN: T−1 = S, R−1 = Q, A+1 = B, I+1 = J, N−1 = M. BUS: B−1 = A, U+1 = V, S−1 = R. Each vowel moves one step "
    "forward and each consonant one step back. METRO: M → L, E → F, T → S, R → Q, O → P.",
    ["Check TRAIN and BUS: vowels +1, consonants −1", "METRO: M−1 L, E+1 F, T−1 S, R−1 Q, O+1 P", f"Code: {ans}"],
    why_others_wrong="LDSQN moves every letter back; NFUSP moves every letter forward; LFSQN moves the final O back "
                     "instead of forward.", seconds=55, verified_by=RECOMP)
hr = lambda w: shift(w[:len(w) // 2][::-1] + w[len(w) // 2:][::-1], 1)
assert hr("MARKET") == "SBNUFL"
ans = inferred([("MARKET", "SBNUFL")], "PLANET", hr("PLANET"))
assert ans == "BMQUFO"
mcq(COD, LC, "Intermediate",
    "In a certain code, MARKET is written as SBNUFL. How is PLANET written in that code?", ans,
    ["UFOBMQ", "QMBOFU", "BMQOFU"], "Reverse each half, then move each letter one step forward",
    "MARKET → halves MAR | KET → reversed RAM | TEK → each letter +1 → SBN | UFL. PLANET → PLA | NET → ALP | TEN → "
    f"+1 → {ans}.", ["Check: MAR KET → RAM TEK → SBN UFL", "PLANET → ALP TEN", f"+1 → {ans}"],
    why_others_wrong="UFOBMQ reverses the whole word; QMBOFU only shifts; BMQOFU leaves the second half unreversed.",
    seconds=60, verified_by=RECOMP)
dcode = lambda n: "".join(str((int(d) + 3) % 10) for d in n)[::-1]
assert dcode("4721") == "4507" and dcode("3916") == "9426"
DRULES = {}
for k in range(1, 10):
    for rv in (False, True):
        DRULES[f"+{k},{rv}"] = lambda n, k=k, rv=rv: (lambda s: s[::-1] if rv else s)(
            "".join(str((int(d) + k) % 10) for d in n))
        DRULES[f"{k}-d,{rv}"] = lambda n, k=k, rv=rv: (lambda s: s[::-1] if rv else s)(
            "".join(str((k - int(d)) % 10) for d in n))
DRULES["pairswap"] = lambda n: n[1] + n[0] + n[3] + n[2]
ans = inferred([("4721", "4507"), ("3916", "9426")], "5803", dcode("5803"), DRULES)
assert ans == "6318"
mcq(COD, NC, "Intermediate",
    "In a certain code, 4721 is written as 4507 and 3916 is written as 9426. How is 5803 written in that code?", ans,
    ["8136", "3081", "6138"], "Add 3 to each digit (keeping the units digit), then reverse",
    "4721: 4+3 = 7, 7+3 = 10 → 0, 2+3 = 5, 1+3 = 4 → 7054, reversed 4507. 3916 → 6249 → 9426. 5803 → 8136 → "
    f"{ans}.", ["Check: 4721 → 7054 → 4507; 3916 → 6249 → 9426", "5803 → 8 1 3 6", f"Reverse → {ans}"],
    why_others_wrong="8136 skips the reversal; 3081 reverses without adding; 6138 reverses only part of the number.",
    seconds=60, verified_by=RECOMP)

# ---- Advanced: coding set with conditions on the word
def cond_code(w):
    if len(w) % 2 == 0:
        w = w[len(w) // 2:] + w[:len(w) // 2]
    else:
        m = len(w) // 2
        w = w[:m] + str(len(w)) + w[m + 1:]
    return "".join(shift(c, 1) if c in VOW else c for c in w)


CTXT = ("In a certain code language, each word is coded by the steps below.\n"
        "Step 1: If the word has an even number of letters, its first half and second half are interchanged. If the "
        "word has an odd number of letters, its middle letter is replaced by the number of letters in the word.\n"
        "Step 2: Every vowel (A, E, I, O, U) in the result of Step 1 is replaced by the letter that comes immediately "
        "after it in the English alphabet.\n\nEach question gives a word; choose its code.")
sid = stimulus("passage", "Coding by word length, then vowels", CTXT, None,
               "Count the letters first (even: swap the halves; odd: replace the middle letter by the count), then "
               "move every remaining vowel one step forward. Consonants and the inserted number do not change in "
               "Step 2.")
AQ = lambda word, correct, wrongs, expl, steps, **kw: mcq(
    COD, LC, "Advanced", f"What is the code for '{word}'?", correct, wrongs, "Conditional steps applied in order",
    expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
ans = cond_code("MARGIN")
assert ans == "GJNMBR"
AQ("MARGIN", ans, ["MBRGJN", "GINMAR", "HJONBS"],
   "MARGIN has 6 letters (even), so the halves MAR and GIN are interchanged: GINMAR. Its vowels I and A become J and "
   f"B: {ans}.", ["6 letters ⇒ swap halves: GIN MAR", "Vowels: I → J, A → B", f"Code: {ans}"],
   why_others_wrong="MBRGJN skips the swap; GINMAR skips Step 2; HJONBS shifts consonants too.", seconds=60)
ans = cond_code("PLANT")
assert ans == "PL5NT"
AQ("PLANT", ans, ["PLBNT", "NTAPL", "PL5OT"],
   "PLANT has 5 letters (odd), so the middle letter A is replaced by 5: PL5NT. No vowel is left, so Step 2 changes "
   "nothing.", ["5 letters ⇒ middle letter (3rd) → 5", "PL5NT has no vowel", f"Code: {ans}"],
   why_others_wrong="PLBNT applies only Step 2 to A; NTAPL swaps halves (that is for even lengths); PL5OT shifts N.",
   seconds=55)
ans = cond_code("OBTAINED")
assert ans == "JNFDPBTB"
AQ("OBTAINED", ans, ["PBTBJNFD", "INEDOBTA", "JNFDPBUB"],
   "OBTAINED has 8 letters, so OBTA and INED are interchanged: INEDOBTA. The vowels I, E, O, A become J, F, P, B: "
   f"{ans}.", ["8 letters ⇒ INED OBTA", "Vowels: I → J, E → F, O → P, A → B (twice)", f"Code: {ans}"],
   why_others_wrong="PBTBJNFD skips the swap; INEDOBTA skips Step 2; JNFDPBUB also shifts the consonant T.",
   seconds=70)
# ---- Advanced (standalone)
pr = lambda w: "".join(shift(c, len(w) - i) for i, c in enumerate(w))
assert pr("CODE") == "GRFF" and pr("HAND") == "LDPE"
ans = inferred([("CODE", "GRFF"), ("HAND", "LDPE")], "LAMP", pr("LAMP"))
assert ans == "PDOQ"
mcq(COD, LC, "Advanced",
    "In a certain code, CODE is written as GRFF and HAND is written as LDPE. How is LAMP written in that code?", ans,
    ["MCPT", "PDPQ", "QDOP"], "Shift by the position counted from the right end",
    "CODE: C+4 = G, O+3 = R, D+2 = F, E+1 = F. HAND: H+4 = L, A+3 = D, N+2 = P, D+1 = E. Each letter moves forward by "
    "its position counted from the right end. LAMP: L+4 = P, A+3 = D, M+2 = O, P+1 = Q.",
    ["Check CODE and HAND: +4, +3, +2, +1", "LAMP: L+4 P, A+3 D, M+2 O, P+1 Q", f"Code: {ans}"],
    why_others_wrong="MCPT counts positions from the left (+1, +2, +3, +4); PDPQ adds 3 to M; QDOP swaps the end "
                     "letters.", seconds=75, verified_by=RECOMP)
assert pl("LAMP") == "MCPT"
ans = inferred([("ACE", 22), ("BAD", 16)], "CAGE", 46, NRULES)
mcq(COD, NC, "Advanced",
    "In a certain code, ACE is written as 22 and BAD is written as 16. Using the same rule, how is CAGE written?",
    str(ans), ["16", "34", "64"], "Position value × place in the word, added up",
    "ACE: 1×1 + 3×2 + 5×3 = 1 + 6 + 15 = 22. BAD: 2×1 + 1×2 + 4×3 = 2 + 2 + 12 = 16. Each letter's alphabet position "
    "is multiplied by its place in the word and the products are added. CAGE: 3×1 + 1×2 + 7×3 + 5×4 = 3 + 2 + 21 + 20 "
    f"= {ans}.",
    ["Check ACE = 22 and BAD = 16 (plain sums would be 9 and 7)", "CAGE: 3 + 2 + 21 + 20", f"= {ans}"],
    why_others_wrong="16 is the plain sum of positions; 34 multiplies by the places counted from the right end; 64 multiplies "
                     "the sum by the number of letters.", natural=int, seconds=80, verified_by=RECOMP)
assert NRULES["sum"]("CAGE") == 16 and NRULES["weighted-right"]("CAGE") == 34 and NRULES["sum×len"]("CAGE") == 64

# ================================================================================================ ALPHANUMERIC SERIES
ALN = "Alphanumeric Series"
CONS = lambda t: is_l(t) and t not in VOW


def near(seq, i, k=3):
    """Wrong options: distinct elements near position i (0-based) other than seq[i]."""
    out = []
    for d in (1, -1, 2, -2, 3, -3, 4, -4):
        j = i + d
        if 0 <= j < len(seq) and seq[j] != seq[i] and seq[j] not in out:
            out.append(seq[j])
    return out[:k]


# ---- Basic (standalone)
SR = "T 6 # B 9 E 3 @ K 7 W % 2 U 8".split()
ans_i = 10 - 1 - 4  # 4th to the left of the 10th element from the left
ans = SR[ans_i]
assert ans == "E"
mcq(ALN, "Position-based", "Basic", series_intro(" ".join(SR)) +
    "\n\nWhich element is 4th to the left of the 10th element from the left end?", ans, near(SR, ans_i),
    "Moving left from a counted position", f"The 10th element from the left is {SR[9]}; four places to its left is "
    f"the 6th element, {ans}.", [f"10th from the left = {SR[9]}", "10 − 4 = 6th from the left", f"6th = {ans}"],
    seconds=35, verified_by=RECOMP)

# ---- Intermediate: set 1
SR = "M 3 # J 8 A @ 5 Q 2 W E % 7 K 9 $ U 4 R & 1 Y 6".split()
assert len(SR) == 24
sid = stimulus("data_table", "Arrangement of 24 letters, numbers and symbols",
               "Study the following arrangement of letters, numbers and symbols and answer the questions.\n\n"
               + " ".join(SR), None,
               "Positions from the left: " + ", ".join(f"{i + 1}: {t}" for i, t in enumerate(SR)) + ".")
AQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    ALN, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
hits = [w for w in windows(SR) if is_d(w[0]) and is_l(w[1]) and is_s(w[2])]
hits = [w for w in windows(SR) if is_d(w[0]) and is_l(w[1]) and is_s(w[2])]
a, w = count_opts(len(hits))
AQ("Symbol and number series", "How many letters in the arrangement are immediately preceded by a number and "
   "immediately followed by a symbol?", a, w, "Checking each letter's two neighbours",
   "Letters with a number before and a symbol after: " + ", ".join(" ".join(h) for h in hits) + f" — {len(hits)} in "
   "all.", ["Scan each letter: left neighbour a number? right neighbour a symbol?",
            "Matches: " + ", ".join(" ".join(h) for h in hits)], natural=by_num, seconds=60)
nonum = [t for t in SR if not is_d(t)]
ans = nonum[-7]
AQ("Position-based", "If all the numbers in the arrangement are removed, which element will be 7th from the right "
   "end?", ans, near(nonum, len(nonum) - 7), "Rebuilding the arrangement after deletions",
   "Without numbers the arrangement is " + " ".join(nonum) + f". Counting from the right, the 7th element is {ans}.",
   ["Remove 3, 8, 5, 2, 7, 9, 4, 1, 6", "New arrangement: " + " ".join(nonum), f"7th from the right: {ans}"],
   seconds=60)
ans_i = 12 - 1 - 5
ans = SR[ans_i]
AQ("Position-based", "Which element is 5th to the left of the 12th element from the left end?", ans, near(SR, ans_i),
   "Moving left from a counted position", f"The 12th element from the left is {SR[11]}; five places to its left is the "
   f"7th element, {ans}.", [f"12th = {SR[11]}", "12 − 5 = 7", f"7th = {ans}"], seconds=45)
vc_ = [w for w in windows(SR) if w[1] in VOW and CONS(w[2])]
a, w = count_opts(len(vc_))
AQ("Symbol and number series", "How many vowels in the arrangement are immediately followed by a consonant?", a, w,
   "Vowels and their right neighbours",
   "The vowels are A, E and U. A is followed by @, E by %, U by 4: " + (f"{len(vc_)} match" if vc_ else "none is "
   "followed by a consonant") + ".", ["Vowels: A (→ @), E (→ %), U (→ 4)", f"Followed by a consonant: {len(vc_)}"],
   natural=by_num, seconds=50)
assert len(vc_) == 0 and [t for t in SR if t in VOW] == ["A", "E", "U"]

# ---- Intermediate: set 2
SR = "5 R © 8 H I ★ 3 N D 7 # O 4 G £ 9 S 2 L ¥ A 6 P".split()
assert len(SR) == 24
sid = stimulus("data_table", "Arrangement with reversed blocks",
               "Study the following arrangement of letters, numbers and symbols and answer the questions.\n\n"
               + " ".join(SR), None,
               "Positions from the left: " + ", ".join(f"{i + 1}: {t}" for i, t in enumerate(SR)) + ".")
AQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    ALN, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
rv = SR[:12][::-1] + SR[12:]
ans = rv[8 - 1 + 6]
AQ("Position-based", "If the first twelve elements are written in reverse order, which element will be 6th to the "
   "right of the 8th element from the left end?", ans, near(rv, 13), "Rearranging a block, then counting",
   "After reversing the first twelve: " + " ".join(rv) + f". The 8th element is {rv[7]}; six places to its right is "
   f"the 14th, {ans}.", ["New order: " + " ".join(rv), f"8th = {rv[7]}", f"14th = {ans}"], seconds=70)
sym_between = [w for w in windows(SR) if is_s(w[1]) and is_l(w[0]) and is_d(w[2])]
a, w = count_opts(len(sym_between))
AQ("Symbol and number series", "How many symbols in the arrangement are immediately preceded by a letter and "
   "immediately followed by a number?", a, w, "Checking each symbol's two neighbours",
   "Matches: " + (", ".join(" ".join(h) for h in sym_between) or "none") + f" — {len(sym_between)} in all.",
   ["Symbols: ©, ★, #, £, ¥", "Letter before and number after: " + ", ".join(" ".join(h) for h in sym_between)],
   natural=by_num, seconds=60)
mid_i = (4 + (len(SR) - 6)) // 2  # 5th from the left (index 4) and 6th from the right (index len-6)
assert (4 + len(SR) - 6) % 2 == 0
ans = SR[mid_i]
AQ("Position-based", "Which element is exactly midway between the 5th element from the left end and the 6th element "
   "from the right end?", ans, near(SR, mid_i), "Converting a right-end position before taking the midpoint",
   f"The 5th from the left is position 5 ({SR[4]}); the 6th from the right is position {len(SR) - 5} "
   f"({SR[len(SR) - 6]}). Midway: position {mid_i + 1}, {ans}.",
   [f"6th from the right = {len(SR)} − 6 + 1 = {len(SR) - 5}th from the left", f"(5 + {len(SR) - 5}) ÷ 2 = {mid_i + 1}",
    f"{mid_i + 1}th = {ans}"], seconds=60)

# ---- Advanced (standalone)
SR = "8 F @ 3 K U 6 % T 1 Z $ 4 E 7 B # 9 M 2 & O 5 V".split()
evens = [i for i, t in enumerate(SR) if is_d(t) and int(t) % 2 == 0]
cnt = sum(1 for i in evens if (i > 0 and is_s(SR[i - 1])) or (i + 1 < len(SR) and is_s(SR[i + 1])))
a, w = count_opts(cnt)
mcq(ALN, "Symbol and number series", "Advanced", series_intro(" ".join(SR)) +
    "\n\nHow many even numbers in the arrangement have at least one symbol as an immediate neighbour?", a, w,
    "Checking both neighbours of each even number",
    "Even numbers and their neighbours: " + "; ".join(
        f"{SR[i]} ({SR[i - 1] if i else '—'}, {SR[i + 1] if i + 1 < len(SR) else '—'})" for i in evens) +
    f". With a symbol beside: {cnt}.",
    ["Even numbers: " + ", ".join(SR[i] for i in evens), "Check left and right neighbours for a symbol",
     f"Count = {cnt}"], natural=by_num, seconds=80, verified_by=RECOMP)
dropv = [t for t in SR if not (is_l(t) and t in VOW)]
k1 = dropv[9 - 1]
ans_i = dropv.index(k1) - 4
ans = dropv[ans_i]
mcq(ALN, "Position-based", "Advanced", series_intro(" ".join(SR)) +
    "\n\nIf all the vowels are removed from the arrangement, which element will be 4th to the left of the 9th element "
    "from the left end?", ans, near(dropv, ans_i), "Delete first, then count",
    "Without the vowels U, E and O: " + " ".join(dropv) + f". The 9th element is {k1}; four places to its left is the "
    f"5th, {ans}.", ["Remove U, E, O", "New arrangement: " + " ".join(dropv), f"9th = {k1}; 9 − 4 = 5th = {ans}"],
    seconds=75, verified_by=RECOMP)

# ================================================================================================ ALPHABET TEST
ABT = "Alphabet Test"
W = "CHAMPION"
nw = W[4:] + W[:4]
ans = nw[-3]
assert nw == "PIONCHAM" and ans == "H"
mcq(ABT, "Letter position", "Intermediate",
    "In the word 'CHAMPION', the 1st and 5th letters are interchanged, and so are the 2nd and 6th, the 3rd and 7th, "
    "and the 4th and 8th letters. Which letter will then be 3rd from the right end?", ans, ["A", "C", "O"],
    "Interchanging positions k and k + 4 swaps the two halves",
    f"Swapping 1↔5, 2↔6, 3↔7, 4↔8 exchanges the halves CHAM and PION: {nw}. From the right: M, A, {ans}.",
    [f"CHAM | PION → {nw}", f"3rd from the right = {ans}"],
    why_others_wrong="A is 2nd from the right; C is 5th from the left; O is the 3rd from the left.", seconds=45,
    verified_by=RECOMP)

# ================================================================================================ NUMBER-BASED
NUM = "Number Series (Reasoning)"
# ---- Basic set
NS = [647, 382, 915, 274, 536]
sid = stimulus("data_table", "Five three-digit numbers (set A)",
               "Study the following five three-digit numbers and answer the questions.\n\n" + "   ".join(map(str, NS)),
               None, "Digits of each number: " + "; ".join(f"{n}: {' '.join(str(n))}" for n in NS) + ".")
NQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    NUM, sub, "Basic", text, correct, wrongs, concept, expl,
    steps, stimulus=sid, verified_by=RECOMP, **kw)
add2 = {n: n + 2 for n in NS}
assert all(n % 10 <= 7 for n in NS)
big = [n for n in NS if add2[n] % 10 > add2[n] // 100]
a, w = count_opts(len(big))
NQ("Number-based digit operations", "If 2 is added to the last digit of each number, in how many of the new numbers "
   "will the last digit be greater than the first digit?", a, w, "Digit operation, then comparison",
   "New numbers: " + ", ".join(f"{n} → {add2[n]}" for n in NS) + ". Last digit greater than first: " +
   (", ".join(str(add2[n]) for n in big) or "none") + f". Count {len(big)}.",
   ["Add 2 to each units digit: " + ", ".join(str(add2[n]) for n in NS), "Compare last digit with first digit"],
   natural=by_num, seconds=45)
desc = sorted(NS, reverse=True)
NQ("Three-digit number questions", "If the numbers are arranged in descending order, which number will be third "
   "from the left?", str(desc[2]), [str(x) for x in desc if x != desc[2]][:3], "Ordering",
   "Descending: " + ", ".join(map(str, desc)) + f". Third from the left: {desc[2]}.", ["Descending: "
                                                                                      + " > ".join(map(str, desc))],
   seconds=35)
sw = {n: int(str(n)[::-1]) for n in NS}
diff = max(sw.values()) - min(sw.values())
NQ("Number-based digit operations", "If the first and the last digits of each number are interchanged, what is the "
   "difference between the largest and the smallest of the new numbers?", str(diff),
   [str(x) for x in (diff - 10, diff + 99, max(NS) - min(NS)) if x != diff], "Digit interchange, then extremes",
   "New numbers: " + ", ".join(f"{n} → {sw[n]}" for n in NS) + f". Largest {max(sw.values())}, smallest "
   f"{min(sw.values())}; difference {diff}.", ["Interchange first and last digits",
                                              f"{max(sw.values())} − {min(sw.values())} = {diff}"],
   natural=int, seconds=50)
assert max(NS) - min(NS) != diff
evs = [n for n in NS if sum(map(int, str(n))) % 2 == 0]
a, w = count_opts(len(evs))
NQ("Three-digit number questions", "How many of the numbers have an even sum of digits?", a, w, "Digit sums",
   "Digit sums: " + ", ".join(f"{n} → {sum(map(int, str(n)))}" for n in NS) + f". Even: {len(evs)}.",
   ["Digit sums: " + ", ".join(str(sum(map(int, str(n)))) for n in NS)], natural=by_num, seconds=40)

# ---- Advanced set: five four-digit numbers
NS = [5837, 2964, 7419, 3582, 6175]
sid = stimulus("data_table", "Five four-digit numbers",
               "Study the following five four-digit numbers and answer the questions.\n\n" + "   ".join(map(str, NS)),
               None, "Digits of each number: " + "; ".join(f"{n}: {' '.join(str(n))}" for n in NS) + ".")
NQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    NUM, "Number-based digit operations", "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid,
    verified_by=RECOMP, **kw)
asc = {n: int("".join(sorted(str(n)))) for n in NS}
best = max(NS, key=asc.get)
assert sorted(asc.values()).count(asc[best]) == 1
NQ("If the digits of each number are arranged in ascending order within the number, which original number will "
   "become the largest?", str(best), [str(x) for x in NS if x != best][:3], "Rearranging digits inside each number",
   "New numbers: " + ", ".join(f"{n} → {asc[n]}" for n in NS) + f". The largest new number, {asc[best]}, comes from "
   f"{best}.", ["Sort the digits of each number: " + ", ".join(f"{n}→{asc[n]}" for n in NS)], seconds=70)
tr = lambda n: int("".join(str(int(d) - 1) if int(d) % 2 else str((int(d) + 1) % 10) for d in str(n)))
over = [n for n in NS if sum(map(int, str(tr(n)))) > 20]
a, w = count_opts(len(over))
NQ("If 1 is subtracted from every odd digit and 1 is added to every even digit of each number, how many of the new "
   "numbers will have a digit sum greater than 20?", a, w, "Digit-wise transformation, then digit sums",
   "New numbers: " + ", ".join(f"{n} → {tr(n)} (sum {sum(map(int, str(tr(n))))})" for n in NS) +
   f". Sum above 20: {len(over)}.", ["Odd digits −1, even digits +1",
                                     "Digit sums: " + ", ".join(str(sum(map(int, str(tr(n))))) for n in NS)],
   natural=by_num, seconds=80)
rvn = {n: str(n)[::-1] for n in NS}
hi, lo = max(NS), min(NS)
ans = int(rvn[hi][1]) + int(rvn[lo][2])
NQ("If the digits of each number are reversed, what is the sum of the second digit of the reversed form of the "
   "highest original number and the third digit of the reversed form of the lowest original number?", str(ans),
   [str(x) for x in sorted({ans - 2, ans + 1, ans + 3, ans - 1} - {ans})[:3]], "Identify first, then transform",
   f"Highest original: {hi} → reversed {rvn[hi]}, second digit {rvn[hi][1]}. Lowest original: {lo} → reversed "
   f"{rvn[lo]}, third digit {rvn[lo][2]}. Sum = {ans}.", [f"{hi} → {rvn[hi]}", f"{lo} → {rvn[lo]}",
                                                        f"{rvn[hi][1]} + {rvn[lo][2]} = {ans}"],
   natural=int, seconds=70)
d3 = [n for n in NS if n % 3 == 0]
a, w = count_opts(len(d3))
NQ("How many of the numbers are exactly divisible by 3?", a, w, "Divisibility by 3 through the digit sum",
   "Digit sums: " + ", ".join(f"{n} → {sum(map(int, str(n)))}" for n in NS) + ". Divisible by 3 (digit sum a "
   f"multiple of 3): " + (", ".join(map(str, d3)) or "none") + f". Count {len(d3)}.",
   ["A number is divisible by 3 when its digit sum is", "Digit sums: " + ", ".join(
       str(sum(map(int, str(n)))) for n in NS)], natural=by_num, seconds=60)
pairs_ = [n for n in NS if n // 100 > n % 100]
a, w = count_opts(len(pairs_))
NQ("If each number is split into two two-digit numbers (the first two digits and the last two digits), in how many "
   "cases will the first two-digit number be greater than the second?", a, w, "Splitting a number into parts",
   "Splits: " + ", ".join(f"{n} → {n // 100} | {n % 100:02d}" for n in NS) + f". First part greater: {len(pairs_)}.",
   ["Splits: " + ", ".join(f"{n // 100}|{n % 100:02d}" for n in NS)], natural=by_num, seconds=60)

# ================================================================================================ RANKING
RNK = "Ranking and Order"
P = ["Ayaan", "Bela", "Chaman", "Dolly", "Eknath", "Farha"]
orders = [perm for perm in itertools.permutations(P)  # perm[0] = heaviest
          if perm.index("Chaman") == 3 and perm[0] == "Dolly"
          and perm.index("Ayaan") < perm.index("Bela") < perm.index("Farha") < perm.index("Eknath")]
assert orders == [("Dolly", "Ayaan", "Bela", "Chaman", "Farha", "Eknath")]
O_ = orders[0]
sid = stimulus("puzzle", "Six persons and their weights",
               "Six persons Ayaan, Bela, Chaman, Dolly, Eknath and Farha have different weights.\n\n"
               "- Chaman is heavier than only two persons.\n- Bela is heavier than Farha but lighter than Ayaan.\n"
               "- Dolly is the heaviest.\n- Eknath is lighter than Farha.", None,
               "Dolly is first and Chaman fourth (two persons lighter than him). Ayaan > Bela > Farha > Eknath fill "
               "places 2, 3, 5 and 6 in that order.\n\nHeaviest to lightest: " + ", ".join(O_))
RQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    RNK, "Comparison of heights/weights", "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid,
    verified_by=BRUTE, **kw)
RQ("Who is the second lightest?", O_[-2], ["Chaman", "Eknath", "Bela"], "Fixing places from 'only' clues",
   "Heaviest to lightest: " + ", ".join(O_) + f". Second lightest: {O_[-2]}.",
   ["Dolly 1st; Chaman 4th", "Ayaan > Bela > Farha > Eknath take 2nd, 3rd, 5th, 6th"], seconds=50)
RQ("How many persons are heavier than Bela?", num_word(O_.index("Bela")), ["One", "Three", "Four"],
   "Counting places above", "Only Dolly and Ayaan are heavier than Bela.", ["Order: " + ", ".join(O_)],
   natural=by_num, seconds=45)
cands = [51, 53, 55, 58]
okb = [c for c in cands if c > 55]
assert okb == [58]
RQ("If Farha weighs 48 kg and Chaman weighs 55 kg, which of the following can be Bela's weight?", "58 kg",
   ["51 kg", "53 kg", "55 kg"], "A heavier person must have a larger weight",
   "Bela is heavier than Chaman (she is 3rd, he is 4th), so her weight must be more than 55 kg. Only 58 kg fits; "
   "55 kg would equal Chaman's weight, but all weights are different.",
   ["Bela (3rd) > Chaman (4th) = 55 kg", "Only 58 kg exceeds 55 kg"], natural=lambda t: int(t.split()[0]),
   seconds=50)
# standalone
n_ = (9 + 5) + 14 - 1
assert n_ == 27
mcq(RNK, "Position in a row", "Intermediate",
    "In a row of girls facing north, Nisha is 9th from the left end. When she moves 5 places to her right, she "
    "becomes 14th from the right end. How many girls are there in the row?", str(n_), ["22", "28", "23"],
    "New position from both ends", "After moving 5 places right, Nisha is 9 + 5 = 14th from the left and 14th from "
    f"the right, so the row has 14 + 14 − 1 = {n_} girls.",
    ["New position from the left = 14", f"Total = 14 + 14 − 1 = {n_}"],
    why_others_wrong="22 uses her old position (9 + 14 − 1); 28 forgets to subtract her once; 23 subtracts 5 "
                     "instead of adding.", natural=int, seconds=45, verified_by=RECOMP)
total, r_top = 45, 16
ans = total - r_top + 1
assert ans == 30
mcq(RNK, "Position in a row", "Intermediate",
    "In a class of 45 students, Ravi is 16th from the top in rank. Later, five students ranked above Ravi are "
    "found to have failed and are removed from the ranking list. What is Ravi's rank from the bottom in the new "
    "list?", f"{ans}th", ["25th", "35th", "26th"], "Removing students above a person does not change the count below",
    "Below Ravi there were 45 − 16 = 29 students, and none of them was removed. So he is still 30th from the bottom "
    "(his rank from the top changes to 11th).",
    ["Students below Ravi = 45 − 16 = 29 (unchanged)", "Rank from the bottom = 29 + 1 = 30"],
    why_others_wrong="25th wrongly subtracts the five removed students from the bottom count; 35th and 26th mix up "
                     "the ends.", natural=lambda t: int(t[:-2]), seconds=50, verified_by=RECOMP)
c_front = (15 + 23) // 2
n_ = c_front + 18 - 1
assert n_ == 36
mcq(RNK, "Position in a row", "Intermediate",
    "In a queue, Amar is 15th from the front and Bhola is 23rd from the front. Charu stands exactly midway between "
    "them and is 18th from the back. How many people are there in the queue?", str(n_), ["37", "35", "41"],
    "Midpoint, then total from both ends",
    f"Charu is midway between the 15th and 23rd places: ({15} + {23}) ÷ 2 = {c_front}th from the front. With 18th "
    f"from the back, the queue has {c_front} + 18 − 1 = {n_} people.",
    [f"Charu = (15 + 23) ÷ 2 = {c_front}th from the front", f"Total = {c_front} + 18 − 1 = {n_}"],
    why_others_wrong="37 forgets to subtract Charu once; 35 subtracts twice; 41 uses Bhola's place.", natural=int,
    seconds=50, verified_by=RECOMP)

# ================================================================================================ INPUT-OUTPUT
dprod = lambda n: (n // 10) * (n % 10)


def prod_machine(nums):
    cur, steps = list(nums), []
    for k in range(len(cur) - 1):
        rest = cur[k:]
        nxt = min(rest, key=lambda x: (dprod(x), x))
        new = cur[:k] + [nxt] + [x for x in rest if x != nxt]
        if new != cur:
            cur = new
            steps.append(cur[:])
    return steps


INP = [57, 34, 82, 19, 66, 47, 25]
assert len({dprod(n) for n in INP}) == len(INP)
st = prod_machine(INP)
ans = " ".join(map(str, st[2]))
wr = [" ".join(map(str, st[1])), " ".join(map(str, st[3])), " ".join(map(str, sorted(INP)))]
assert ans not in wr and len(set(wr)) == 3
mcq(IOT, "Number rearrangement", "Intermediate",
    "A machine rearranges numbers step by step. In each step it takes, among the numbers not yet arranged, the one "
    "whose two digits have the smallest product, and places it immediately to the right of the numbers already "
    "arranged (in Step I, at the extreme left). The other numbers keep their order.\n\nInput: "
    + " ".join(map(str, INP)) + "\n\nWhich of the following is Step III?", ans, wr,
    "Selecting by product of digits",
    "Products of digits: " + ", ".join(f"{n} → {dprod(n)}" for n in INP) + ". In increasing order of product: "
    + ", ".join(str(n) for n in sorted(INP, key=dprod)) + ". " +
    " ".join(f"Step {ROMAN[i]}: {' '.join(map(str, s_))}." for i, s_ in enumerate(st[:3])),
    [f"Step {ROMAN[i]}: " + " ".join(map(str, s_)) for i, s_ in enumerate(st[:3])],
    why_others_wrong="The other lines are Step II, Step IV and the input sorted by value.", seconds=75,
    verified_by=RECOMP)


def vow_machine(words):
    """Each step: the unarranged word with the most vowels (ties: alphabetically first) is written in reverse and
    placed immediately to the left of the words already arranged at the right end."""
    cur, steps, n = list(words), [], len(words)
    done = []
    for k in range(n):
        rest = [w_ for w_ in cur[:n - k]]
        nxt = sorted(rest, key=lambda w_: (-sum(c in "aeiou" for c in w_), w_))[0]
        rest.remove(nxt)
        done = [nxt[::-1]] + done
        cur = rest + done
        steps.append(cur[:])
    return steps


INP = "garden ocean pilot mist audio rate".split()
assert len({sum(c in "aeiou" for c in w_) for w_ in INP}) >= 3
st = vow_machine(INP)
assert len(st) == 6
target = st[3]
k = st.index(target) + 1
assert k == 4
mcq(IOT, "Word rearrangement", "Advanced",
    "A machine rearranges words step by step. In each step it takes, among the words not yet arranged, the word with "
    "the most vowels (if two such words have the same number of vowels, the one that comes first in alphabetical "
    "order), writes it in reverse, and places it immediately to the left of the words already arranged at the right "
    "end (in Step I, at the extreme right). The other words keep their order. The machine stops when every word has "
    "been arranged.\n\nInput: " + " ".join(INP) + f"\n\nIn which step does the line read '{' '.join(target)}'?",
    f"Step {ROMAN[k - 1]}", ["Step III", "Step V", "Step VI"], "Selection by vowel count with a transformation",
    "Vowel counts: " + ", ".join(f"{w_} {sum(c in 'aeiou' for c in w_)}" for w_ in INP) + ". " +
    " ".join(f"Step {ROMAN[i]}: {' '.join(s_)}." for i, s_ in enumerate(st)),
    [f"Step {ROMAN[i]}: " + " ".join(s_) for i, s_ in enumerate(st)],
    natural=lambda t: ROMAN.index(t.split()[1]), seconds=90, verified_by=RECOMP)

# ================================================================================================ DATA SUFFICIENCY
def ds2_q(diff, question, st1, st2, models, f1, f2, answer, expected, drop, explanation, steps, seconds=50):
    got = ds2(models, f1, f2, answer)
    assert got == expected, (question, got)
    keys = [k_ for k_ in "ABENT" if k_ != drop]
    assert expected in keys and len(keys) == 4
    return fixed(DSF, "Two-statement", diff, DS_HEAD + f"Question: {question}\n\nI. {st1}\nII. {st2}",
                 [DS2[k_] for k_ in keys], DS2[expected], "Data sufficiency: test each statement alone, then together",
                 explanation, steps, seconds=seconds, verified_by=ENUM)


# ---- Basic
ages = [{"r": r, "s": s} for r in range(1, 80) for s in range(1, 80)]
ds2_q("Basic", "What is Ramu's present age?", "Ramu is 4 years older than Sonu.",
      "Sonu's present age is half of Ramu's present age.", ages, lambda d: d["r"] == d["s"] + 4,
      lambda d: 2 * d["s"] == d["r"], lambda d: d["r"], "T", "E",
      "I alone or II alone fits many pairs of ages. Together: R = S + 4 and R = 2S give S = 4 and R = 8.",
      ["I: R = S + 4: many values", "II: R = 2S: many values", "Together: 2S = S + 4 ⇒ S = 4, R = 8: sufficient"],
      seconds=40)
five = list("PQRST")
models = [dict(zip(five, p)) for p in itertools.permutations(range(5))]  # larger = taller
ds2_q("Basic", "Among five friends P, Q, R, S and T, each of a different height, who is the tallest?",
      "P is taller than Q and R but shorter than S.", "T is shorter than Q.", models,
      lambda m: m["P"] > m["Q"] and m["P"] > m["R"] and m["S"] > m["P"], lambda m: m["T"] < m["Q"],
      lambda m: max(five, key=m.get), "T", "E",
      "I leaves T unplaced (T could be taller than S). II alone places only T and Q. Together, T is below Q, which is "
      "below P and S, so S is the tallest.",
      ["I: S > P > Q, R; T unknown: not sufficient", "II: T < Q only: not sufficient",
       "I + II: T < Q < P < S ⇒ S is the tallest"], seconds=45)
week = [{"a": a, "b": b} for a in range(7) for b in range(7) if a != b]  # 0 = Monday
ds2_q("Basic", "On which day of the week did Anu visit the library?",
      "Anu visited after Wednesday but before Saturday.", "Anu visited on the day after Bina, who visited on "
      "Wednesday.", week, lambda d: 2 < d["a"] < 5, lambda d: d["b"] == 2 and d["a"] == 3,
      lambda d: d["a"], "B", "E",
      "I leaves Thursday or Friday. II: Bina visited on Wednesday, so Anu visited on Thursday.",
      ["I: Thursday or Friday: not sufficient", "II: the day after Wednesday = Thursday: sufficient"], seconds=40)
dirs = [{"f": f_} for f_ in CW]
ds2_q("Basic", "Which direction was Raj facing at first?", "After turning 90° clockwise, Raj faces south.",
      "If Raj turns 180°, he faces west.", dirs, lambda d: turn(d["f"], "R") == "S",
      lambda d: turn(turn(d["f"], "R"), "R") == "W", lambda d: d["f"], "E", "T",
      "I: a clockwise quarter turn ends at south only from east. II: a half turn ends at west only from east. Each "
      "statement alone gives east.", ["I: turn clockwise from east → south: sufficient",
                                       "II: turn 180° from east → west: sufficient", "Either statement alone"],
      seconds=40)
d1 = [(["blue", "sky"], ["ta", "mo"]), (["sky", "high"], ["mo", "ri"])]
d2 = [(["blue", "sea"], ["ta", "ke"])]
assert sentence_solve(d1, "blue") == {"ta"} and sentence_solve(d2, "blue") == {"ta", "ke"}
fixed(DSF, "Two-statement", "Basic",
      DS_HEAD + "Question: In a certain code language, what is the code for 'blue'?\n\n"
      "I. 'blue sky' is written as 'ta mo' and 'sky high' is written as 'mo ri'.\n"
      "II. 'blue sea' is written as 'ta ke'.", [DS2[k_] for k_ in "ABNT"], DS2["A"],
      "Data sufficiency with sentence coding",
      "I: sky = mo (common to both sentences), so blue = ta. II: blue is ta or ke; it cannot be fixed.",
      ["I: sky = mo ⇒ blue = ta: sufficient", "II: blue ∈ {ta, ke}: not sufficient", "I alone is sufficient"],
      seconds=40, verified_by=ENUM)
nums = [{"n": n} for n in range(10, 100)]
ds2_q("Basic", "What is the two-digit number N?", "The sum of the digits of N is 9.", "N is divisible by 9.", nums,
      lambda d: sum(map(int, str(d["n"]))) == 9, lambda d: d["n"] % 9 == 0, lambda d: d["n"], "N", "E",
      "Both statements describe the same set of numbers: 18, 27, 36, 45, 54, 63, 72, 81 and 90. Even together they "
      "do not fix N.", ["I: digit sum 9: many numbers", "II: multiples of 9: many numbers",
                        "Together: still 18, 27, …, 90 ⇒ not sufficient"], seconds=45)
# ---- Intermediate
months_ = [{"m": m} for m in range(1, 13)]
ds2_q("Intermediate", "In which month is Kiran's birthday?",
      "Kiran's birthday is in a month that has 31 days and comes after June but before November.",
      "Kiran's birthday month comes immediately after a month that has 30 days, and it comes before September.",
      months_, lambda d: MDAYS[d["m"]] == 31 and 6 < d["m"] < 11,
      lambda d: MDAYS[(d["m"] - 2) % 12 + 1] == 30 and d["m"] < 9, lambda d: d["m"], "T", "E",
      "I: July, August or October. II: months right after a 30-day month and before September: May or July. Only "
      "July satisfies both.",
      ["I: 31-day months between June and November: July, August, October", "II: after April → May; after June → "
       "July (both before September)", "Together: July ⇒ both statements needed"], seconds=60)
models = [dict(zip(five, p)) for p in itertools.permutations(range(1, 6))]
ds2_q("Intermediate", "Five persons P, Q, R, S and T live on the five floors of a building, one on each floor "
      "(floor 1 is the lowermost). Who lives on floor 3?",
      "Only two persons live below R, and S lives immediately above R.",
      "T lives above S, and Q lives on an even-numbered floor.", models,
      lambda m: m["R"] == 3 and m["S"] == 4, lambda m: m["T"] > m["S"] and m["Q"] % 2 == 0,
      lambda m: next(p for p in five if m[p] == 3), "A", "E",
      "I: two persons below R means R is on floor 3, which answers the question. II leaves several placements with "
      "different persons on floor 3.",
      ["I: R = 3 directly: sufficient", "II: e.g. Q 2, S 3, T 5 or Q 4, S 1, T 3: not sufficient",
       "I alone is sufficient"], seconds=55)
# ---- Advanced: three statements
models = [dict(zip(five, p)) for p in itertools.permutations(range(5))]
fns = [lambda m: m["P"] > m["Q"] and m["P"] > m["S"], lambda m: m["T"] > m["R"] > m["P"],
       lambda m: m["S"] > m["Q"]]
got = ds3(models, fns, lambda m: sorted(five, key=m.get, reverse=True)[2])
assert got == "I+II"
fixed(DSF, "Three-statement", "Advanced",
      DS3_HEAD + "Question: Among five friends P, Q, R, S and T, each of a different height, who is the third "
      "tallest?\n\nI. P is taller than Q and S.\nII. R is shorter than T but taller than P.\nIII. S is taller than "
      "Q.", [DS3[k_] for k_ in ("I+II", "II+III", "ALL", "NONE")], DS3["I+II"],
      "Three-statement data sufficiency: test every pair",
      "I + II: T > R > P, and P is above Q and S, so P is third. II + III: T > R > P and S > Q, but S may be above P. "
      "I + III: P > S > Q, but T and R are unplaced. So only I and II together are sufficient.",
      ["I + II: T > R > P > {Q, S} ⇒ P third: sufficient", "II + III: P vs S unknown: not sufficient",
       "I + III: T and R unplaced: not sufficient", "No single statement is sufficient"],
      seconds=80, verified_by=ENUM)
S1 = [(["gold", "coin"], ["pa", "ki"])]
S2 = [(["silver", "coin"], ["ki", "lo"])]
S3 = [(["silver", "gold"], ["lo", "pa"])]
suf = {}
for nm, ss in {"I": S1, "II": S2, "III": S3, "I+II": S1 + S2, "I+III": S1 + S3, "II+III": S2 + S3}.items():
    words = {w_ for ws, _ in ss for w_ in ws}
    suf[nm] = "gold" in words and len(sentence_solve(ss, "gold")) == 1
assert suf == {"I": False, "II": False, "III": False, "I+II": True, "I+III": True, "II+III": True}
fixed(DSF, "Three-statement", "Advanced",
      DS3_HEAD + "Question: In a certain code language, what is the code for 'gold'?\n\nI. 'gold coin' is written as "
      "'pa ki'.\nII. 'silver coin' is written as 'ki lo'.\nIII. 'silver gold' is written as 'lo pa'.",
      [DS3[k_] for k_ in ("I+II", "ALL", "ANY2", "NONE")], DS3["ANY2"], "Three-statement data sufficiency: every pair",
      "No statement alone fixes gold (II does not even contain it). I + II: coin = ki, so gold = pa. I + III: the only "
      "common code of the two sentences containing gold is pa. II + III: silver = lo, so gold = pa. Any two "
      "statements are sufficient.",
      ["I alone: gold ∈ {pa, ki}; III alone: gold ∈ {lo, pa}; II alone: no gold", "I + II: coin = ki ⇒ gold = pa",
       "I + III: common code pa ⇒ gold = pa", "II + III: silver = lo ⇒ gold = pa", "Any two are sufficient"],
      seconds=80, verified_by=ENUM)
ranks = [{"m": m, "s": s, "r": r} for m in range(1, 51) for s in range(1, 51) for r in range(1, 51)
         if len({m, s, r}) == 3]
ds2_q("Advanced", "What is Mohan's rank from the top in a class of 50 students?",
      "Mohan is 10 ranks above Sohan, who is 32nd from the bottom.",
      "Mohan is 5 ranks below Rina, who is 4th from the top.", ranks,
      lambda d: d["s"] == d["m"] + 10 and 50 - d["s"] + 1 == 32, lambda d: d["m"] == d["r"] + 5 and d["r"] == 4,
      lambda d: d["m"], "E", "T",
      "I: Sohan is 50 − 32 + 1 = 19th from the top, so Mohan is 9th. II: Rina is 4th, so Mohan is 9th. Each alone is "
      "sufficient.", ["I: Sohan 19th from the top ⇒ Mohan 19 − 10 = 9th: sufficient",
                      "II: Mohan = 4 + 5 = 9th: sufficient", "Either statement alone is sufficient"], seconds=60)
rows = [{"n": n, "h": h} for n in range(20, 41) for h in range(1, 41) if h <= n]
ds2_q("Advanced", "How many persons sit in the row, all facing north?",
      "Gita is 15th from the left end, and Hari sits sixth to the right of Gita.",
      "Hari is 4th from the right end.", rows, lambda d: d["h"] == 21,
      lambda d: d["n"] - d["h"] + 1 == 4, lambda d: d["n"], "T", "E",
      "I places Hari 21st from the left but says nothing about the right end. II gives Hari's place from the right "
      "only. Together: 21 + 4 − 1 = 24 persons.",
      ["I: Hari = 15 + 6 = 21st from the left: total unknown", "II: Hari 4th from the right: total unknown",
       "Together: 21 + 4 − 1 = 24 ⇒ both needed"], seconds=60)

# ================================================================================================ VERBAL REASONING
# Hand-written items. Each was solved by the author, then re-answered without the key (see the report); scenarios
# were chosen so that the keyed relationship does not depend on outside facts.
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


asm("Basic", "Announcement at a railway station: \"Passengers are advised to keep their luggage with them at all "
    "times.\"", "Luggage left unattended at the station may get lost or stolen.",
    "Most passengers travel without any luggage.", A_I,
    "The advice makes sense only if leaving luggage unattended carries a risk such as loss or theft, so I is "
    "implicit. The announcement is addressed to passengers who do carry luggage; it assumes nothing about most "
    "passengers travelling without it (II).",
    ["Why advise keeping luggage close? Because unattended luggage is at risk ⇒ I implicit",
     "II contradicts the purpose of the announcement ⇒ not implicit"],
    "Both and Only II accept II, which the announcement does not need (and which runs against it).", seconds=30)
asm("Intermediate", "The municipal corporation has decided to plant 10,000 saplings along the city's main roads just "
    "before the monsoon.", "Saplings planted just before the monsoon have a better chance of surviving.",
    "Saplings can be planted along the city's main roads.", A_B,
    "Choosing the time 'just before the monsoon' assumes that this timing helps the saplings survive (I). Deciding to "
    "plant saplings along the main roads assumes that saplings can be planted there (II); otherwise the plan could "
    "not be carried out.",
    ["The timing was chosen deliberately ⇒ it is believed to help survival: I implicit",
     "A plan to plant along the main roads presumes that planting there is possible: II implicit"],
    "Only I or Only II misses one of the two premises the decision rests on; Neither ignores both.", seconds=45)
asm("Intermediate", "An advertisement: \"Buy the AquaPure water purifier — the only purifier in the market tested by "
    "an independent laboratory.\"", "All other water purifiers in the market are of poor quality.",
    "Buyers give importance to independent testing when they choose a water purifier.", A_II,
    "The advertiser highlights independent testing because it expects buyers to value it (II). Saying that only "
    "AquaPure was independently tested does not assume that the untested purifiers are poor (I); they are simply "
    "untested.",
    ["The claim is used to persuade ⇒ buyers must value independent testing: II implicit",
     "'Not independently tested' ≠ 'of poor quality' ⇒ I not implicit"],
    "Only I and Both read a sweeping judgement on rivals into the advertisement.", seconds=45)
asm("Intermediate", "A bank has asked its customers to update their KYC details by 30 June, failing which their "
    "accounts may be frozen.", "Some customers of the bank have not yet updated their KYC details.",
    "The bank has the power to freeze accounts whose KYC details are not updated.", A_B,
    "A reminder with a deadline is sent only if some customers still need to update their details (I). Warning that "
    "accounts may be frozen assumes the bank is able to do so (II); otherwise the warning would be empty.",
    ["Reminder ⇒ some customers have not updated: I implicit", "Threat of freezing ⇒ the bank can freeze: II "
     "implicit"],
    "Only I or Only II drops one of two premises that the notice needs.", seconds=45)
asm("Intermediate", "The principal of a school said, \"Students who score above 90% in the annual examination this "
    "year will receive a certificate of merit.\"", "Most students of the school will score above 90% this year.",
    "Certificates of merit motivate only those students who are already toppers.", A_N,
    "The announcement sets a reward for high scorers. It does not assume that most students will qualify (I); a "
    "merit certificate is usually meant for a few. Nor does it assume anything about whom certificates motivate; if "
    "anything, it hopes to motivate all students (II).",
    ["I: 'most students above 90%' is not needed for the announcement ⇒ not implicit",
     "II: the 'only toppers' claim is extreme and runs against the purpose ⇒ not implicit"],
    "Each assumption adds a claim the principal does not need; Both and the 'Only' options accept at least one of "
    "them.", seconds=45)
asm("Intermediate", "To reduce crowding, the metro has increased the frequency of its trains during peak hours from "
    "one train every 6 minutes to one every 4 minutes.",
    "With more trains, the peak-hour passengers will be spread over more trains, so each train will be less "
    "crowded.", "Metro trains run almost empty outside the peak hours.", A_I,
    "The decision links more frequent trains to less crowding, which works only if the passengers are spread over "
    "the extra trains (I). Nothing in the statement depends on what happens outside the peak hours (II).",
    ["Aim: less crowding; means: more trains ⇒ passengers spread out: I implicit",
     "Non-peak occupancy is irrelevant to the decision ⇒ II not implicit"],
    "Only II and Both accept a claim about non-peak hours that the decision never relies on.", seconds=40)
asm("Intermediate", "An advertisement of a government department: \"Apply online for a duplicate PAN card and get it "
    "delivered to your home.\"", "Every person in the country has lost his or her PAN card.",
    "Some applicants find home delivery more convenient than collecting the card in person.", A_II,
    "Offering home delivery makes sense only if at least some applicants find it convenient (II). The service is for "
    "those who need a duplicate; it does not assume that everyone has lost the card (I), which is an extreme claim.",
    ["Home delivery is offered as a benefit ⇒ some applicants value it: II implicit",
     "'Every person has lost the card' is extreme and unnecessary ⇒ I not implicit"],
    "Only I and Both accept an extreme 'every person' claim.", seconds=40)

# ================================================================================================ CAUSE AND EFFECT
CAE = "Cause and Effect"
CE = {"A": "Statement I is the cause and statement II is its effect",
      "B": "Statement II is the cause and statement I is its effect",
      "C": "Both the statements I and II are independent causes",
      "D": "Both the statements I and II are effects of independent causes",
      "E": "Both the statements I and II are effects of some common cause"}
CE_HEAD = ("Below are two statements, I and II. They may be independent causes, effects of independent causes or of "
           "a common cause, or one may be the effect of the other. Decide the relationship.\n\n")


def ceq(diff, sub, s1, s2, answer, drop, explanation, steps, why, seconds=45):
    keys = [k_ for k_ in "ABCDE" if k_ != drop]
    assert answer in keys and len(keys) == 4
    return fixed(CAE, sub, diff, CE_HEAD + f"I. {s1}\nII. {s2}", [CE[k_] for k_ in keys], CE[answer],
                 "Cause and effect: look for a direct link, a shared trigger, or none", explanation, steps,
                 why_others_wrong=why, seconds=seconds, verified_by=HAND)


IND, COM = "Independent causes", "Common cause"
ceq("Basic", IND, "The electricity board cut off the power supply to the whole town for 12 hours on Sunday for "
    "repair work.", "Shops in the town that depend on electric equipment remained closed on Sunday.", "A", "C",
    "Without power for most of the day, shops that need electric equipment could not work, so they stayed shut. I "
    "explains II.", ["I: a 12-hour power cut on Sunday", "II: power-dependent shops closed the same day",
                     "No power → such shops cannot operate ⇒ I is the cause"],
    "II cannot cause I (shops closing does not cut the town's power); no third event is needed to explain both.",
    seconds=35)
ceq("Basic", IND, "Sales of umbrellas and raincoats in the city went up sharply this week.",
    "The city has received heavy rainfall every day this week.", "B", "C",
    "Daily heavy rain makes people buy rain gear, so II explains I: II is the cause and I its effect.",
    ["II: heavy rain all week", "I: more umbrellas and raincoats sold that week", "Rain → demand for rain gear"],
    "Umbrella sales cannot cause rain, so A is impossible; a separate common cause is not needed because the rain "
    "itself explains the sales.", seconds=35)
ceq("Basic", IND, "The state government declared a public holiday on Monday for the state assembly elections.",
    "A cricket match in the city drew a record crowd on Sunday.", "D", "C",
    "The holiday is the result of the election schedule, and the large crowd is the result of interest in the match. "
    "Neither explains the other, and no single event explains both: they are effects of independent causes.",
    ["I is an effect of the election calendar", "II is an effect of interest in the match (and it happened before "
     "the holiday)", "No link and no shared trigger"],
    "A common cause would need one event behind both an election holiday and a match crowd; the Sunday crowd also "
    "came before the Monday holiday, so I cannot have caused it.", seconds=40)
ceq("Basic", IND, "Low-lying areas along the river were flooded on Thursday.",
    "A dam upstream released a large amount of water into the river on Wednesday night.", "B", "C",
    "A large release of water from an upstream dam raises the river level downstream, flooding the low-lying areas "
    "the next day. II is the cause and I its effect.",
    ["II: large release from the dam on Wednesday night", "I: flooding downstream on Thursday",
     "More water in the river → flooding of low-lying areas"],
    "Flooding downstream cannot make an upstream dam release water, so A is impossible.", seconds=35)
ceq("Basic", COM, "All flights from the coastal city's airport were suspended on Friday.",
    "Fishermen in the coastal city were told not to go out to sea on Friday.", "E", "C",
    "Suspending flights does not keep fishermen ashore, and the fishing advisory does not ground flights. Both are "
    "standard precautions taken together when one event, such as a cyclone warning, threatens the coast.",
    ["No direct link between the two actions", "Both match the response to a single storm warning",
     "⇒ effects of a common cause"],
    "Effects of independent causes would need two unrelated reasons on the same day; one storm warning explains both.",
    seconds=40)
ceq("Advanced", IND, "The central bank raised the cash reserve ratio that banks must maintain by 0.5 percentage "
    "point.", "Several banks raised their lending rates in the following week.", "A", "C",
    "A higher cash reserve ratio locks up more of the banks' deposits with the central bank, leaving less money to "
    "lend and raising the banks' cost of funds; banks respond by raising lending rates. I comes first and explains "
    "II.", ["I: higher reserve requirement", "Less lendable money and higher cost of funds",
            "II: higher lending rates the next week ⇒ I is the cause"],
    "Banks' lending rates do not set the reserve ratio, so B is impossible; treating them as unrelated ignores the "
    "direct mechanism and the timing.", seconds=55)
ceq("Advanced", IND, "The number of applications for the bank's education loans doubled this year.",
    "At the start of this year the bank cut the interest rate on its education loans by 2 percentage points.", "B",
    "C", "A sharp rate cut makes the loans cheaper, and applications doubled in the same year, after the cut. II is "
    "the cause and I its effect.",
    ["II: cheaper education loans from the start of the year", "I: applications doubled this year",
     "Lower cost → more borrowers ⇒ II is the cause"],
    "Applications rising during the year cannot have caused a cut made at its start, so A fails.", seconds=50)
ceq("Advanced", COM, "Sales of woollen clothes in the northern states rose sharply this month.",
    "Demand for room heaters in the northern states rose sharply this month.", "E", "C",
    "Buying woollens does not make people buy heaters, or the other way round. Both are what one event, a spell of "
    "severe cold in the north, would produce in the same month: effects of a common cause.",
    ["No direct link between woollen sales and heater demand", "Both are typical responses to the same cold spell",
     "⇒ effects of a common cause"],
    "Effects of independent causes would need two unrelated reasons that happened to coincide in the same region and "
    "month; one cold spell explains both more simply.", seconds=50)
ceq("Advanced", IND, "A software company in the city reported a record profit this quarter.",
    "The city's traffic police introduced a one-way system in the business district this quarter.", "D", "C",
    "A company's profit results from its business performance, and a traffic plan from the police's assessment of "
    "congestion. Neither explains the other and no single event explains both: they are effects of independent "
    "causes.", ["I: outcome of the company's business", "II: outcome of a traffic decision",
                "No link and no shared trigger ⇒ effects of independent causes"],
    "A common cause would need one event driving both a company's profit and a traffic rule; nothing suggests one.",
    seconds=50)

# ================================================================================================ CRITICAL REASONING
CRT = "Critical Reasoning"
SW_, CA_, INFP = "Strengthen and weaken", "Course of action", "Inference from a passage"


def crq(diff, sub, text, correct, wrongs, concept, explanation, steps, why, seconds=60):
    return mcq(CRT, sub, diff, text, correct, wrongs, concept, explanation, steps, why_others_wrong=why,
               seconds=seconds, verified_by=HAND)


# ---- Basic
crq("Basic", CA_, "Statement: Many students of a village school drop out after Class 8 because the nearest school "
    "that teaches Classes 9 and 10 is 15 km away and there is no bus.\n\nWhich of the following is the most "
    "appropriate course of action?",
    "Provide free transport to the nearest secondary school or upgrade the village school to Class 10",
    ["Make the Class 8 examination harder so that fewer students pass",
     "Close the village school and send all children to the city",
     "Ask the students to walk 15 km each way to school"],
    "A course of action must remove the stated cause practically",
    "The stated cause of drop-outs is distance with no transport. Free transport, or classes up to 10 in the village, "
    "removes that cause directly.",
    ["Problem: drop-outs after Class 8", "Cause: secondary school 15 km away, no bus",
     "Remedy: bring the school closer or provide transport"],
    "A harder Class 8 exam pushes students out; closing the school or asking children to walk 30 km a day is "
    "impractical and harmful.", seconds=35)
crq("Basic", INFP, "A shop sold 120 umbrellas in June and 300 umbrellas in July. The total number of items of all "
    "kinds that the shop sold in July was the same as in June.\n\nWhich of the following can be inferred?",
    "Umbrellas made up a larger share of the items the shop sold in July than in June",
    ["It rained more in July than in June", "The shop cut the price of umbrellas in July",
     "The shop will sell more umbrellas in August than in July"],
    "Inference: only what the figures guarantee",
    "The total number of items sold was the same in both months, and umbrellas rose from 120 to 300, so umbrellas "
    "formed a larger share of the items sold in July.",
    ["Same total in both months", "Umbrellas: 120 → 300", "So the umbrella share of the total rose"],
    "Rain and a price cut are possible reasons that the data do not state; August sales are a prediction.",
    seconds=40)
# ---- Intermediate
crq("Intermediate", SW_, "Argument: The city should make helmets compulsory for pillion riders on two-wheelers, "
    "because this will reduce deaths in two-wheeler accidents.\n\nWhich of the following, if true, most strengthens "
    "the argument?",
    "In two-wheeler accidents in the city, pillion riders without helmets are four times as likely to die of head "
    "injuries as pillion riders wearing helmets",
    ["Helmets are now available in many colours and designs",
     "Most two-wheeler riders in the city are below 40 years of age",
     "Some pillion riders find helmets uncomfortable in summer"],
    "Strengthen: support the link between the proposal and the result",
    "The argument claims that helmets for pillion riders will reduce deaths. Evidence that unhelmeted pillion riders "
    "die far more often of head injuries directly supports that link.",
    ["Claim: helmets for pillion riders → fewer deaths", "Strengthener: evidence that helmets protect pillion riders "
     "in exactly such accidents"],
    "Colours and the riders' age do not bear on deaths; discomfort, if anything, hints at lower compliance and "
    "slightly weakens the plan.", seconds=55)
crq("Intermediate", SW_, "A café owner says that her new loyalty card has increased repeat visits, because repeat "
    "visits to the café rose by 15% in the three months after the card was launched.\n\nWhich of the following, if "
    "true, most weakens her claim?",
    "A large office complex opened next to the café during the same three months, and most of the new repeat "
    "customers work there",
    ["The loyalty card is given free to every customer",
     "Repeat visits at other cafés in the area fell during the same three months",
     "The café also sells packaged snacks"],
    "Weaken a causal claim: another cause for the same effect",
    "If a new office complex next door brought in most of the new regular customers, the rise in repeat visits may "
    "be due to the office crowd, not the card.",
    ["Claim: card → more repeat visits", "Alternative cause in the same period: a new office complex next door",
     "So the rise need not be due to the card"],
    "A free card does not affect the causal claim; falling visits at other cafés actually support it; snack sales are "
    "irrelevant.", seconds=55)
crq("Intermediate", INFP, "In a district, 60% of the households have an account in a public sector bank and 50% "
    "have an account in a private bank.\n\nWhich of the following must be true?",
    "At least 10% of the households have accounts in both a public sector bank and a private bank",
    ["Exactly 10% of the households have accounts in both kinds of bank",
     "40% of the households have an account only in a private bank",
     "Public sector banks serve their customers better than private banks"],
    "Overlap of two groups: the minimum overlap is the excess over 100%",
    "60% + 50% = 110%, which is more than 100%, so at least 10% of the households must be counted in both groups. The "
    "overlap could be larger (up to 50%), so 'exactly 10%' is not certain.",
    ["Public + private = 110% of households", "Since at most 100% of households exist, overlap ≥ 110% − 100% = 10%",
     "The overlap can be anything from 10% to 50%"],
    "'Exactly 10%' would need every household to have at least one account, which is not stated; the 'only private' "
    "share cannot be fixed; the quality claim is not about the numbers at all.", seconds=60)
crq("Intermediate", CA_, "Statement: A bank has found that many of its elderly customers are being cheated by "
    "callers who pretend to be bank officials and persuade them to share the one-time passwords (OTPs) sent to their "
    "phones.\n\nWhich of the following is the most appropriate course of action for the bank?",
    "Run awareness drives for elderly customers, by branch meetings and messages, stating that the bank never asks "
    "for an OTP over the phone",
    ["Stop sending OTPs to customers above 60 years of age",
     "Close the accounts of customers who have shared their OTPs",
     "Stop all phone banking services for every customer"],
    "A course of action should target the cause without harming customers",
    "The fraud works because elderly customers believe the callers. Teaching them that the bank never asks for an "
    "OTP attacks that cause directly and costs them nothing.",
    ["Problem: elderly customers share OTPs with fake callers", "Cause: they trust callers claiming to be the bank",
     "Remedy: awareness that the bank never asks for OTPs"],
    "Stopping OTPs removes a security layer; closing victims' accounts punishes them; ending phone banking for all is "
    "an extreme step that does not address the deception.", seconds=50)
crq("Intermediate", SW_, "Argument: Students who attend the school's optional evening classes score higher in the "
    "board examinations than those who do not. So the evening classes improve students' scores.\n\nWhich of the "
    "following, if true, most weakens the argument?",
    "Only students who were already among the top scorers of the school are allowed to join the evening classes",
    ["The evening classes are taken by the same teachers who teach the regular classes",
     "Some students find the evening classes tiring",
     "The board examination this year was equally difficult for all students"],
    "Weaken: show that the groups differed before the cause acted",
    "If only students who already scored high may join, their higher board scores can be explained by who joined, "
    "not by the classes. The argument's comparison then proves nothing about the classes' effect.",
    ["Claim: evening classes → higher scores", "Weakener: the class takes only students who were already top "
     "scorers (selection, not effect)"],
    "Same teachers and equal difficulty do not explain the score gap; tiredness is irrelevant to the observed "
    "difference.", seconds=55)
crq("Intermediate", INFP, "Passage: A city's bus company introduced air-conditioned buses on some routes. Over the "
    "next year, ridership on those routes rose by 25%, while ridership on the other routes did not change. During the "
    "same year, fares on all routes were raised by the same amount.\n\nWhich of the following can be inferred from "
    "the passage?",
    "Ridership on the routes with air-conditioned buses rose even though fares on those routes went up",
    ["Air-conditioning alone caused the rise in ridership on those routes",
     "All the city's bus routes should be given air-conditioned buses",
     "Ridership on the routes without air-conditioned buses fell"],
    "Inference: restate what the passage guarantees",
    "Fares rose on all routes, including those with the new buses, and ridership on those routes still rose by 25%. "
    "That is a direct combination of two stated facts.",
    ["Fares rose on every route", "Ridership on the air-conditioned routes rose 25%",
     "⇒ the rise happened despite the fare increase"],
    "The passage shows an association, not that air-conditioning alone caused it; a recommendation is not an "
    "inference; ridership on the other routes did not change.", seconds=55)
crq("Intermediate", SW_, "A hospital claims that its new appointment app has reduced the time patients wait at its "
    "outpatient department.\n\nWhich of the following, if true, most strengthens the claim?",
    "The number of outpatients and the number of doctors on duty were the same before and after the app was "
    "introduced, while the average waiting time fell from 90 minutes to 35 minutes",
    ["Thousands of patients have downloaded the app",
     "The app was developed by a well-known software firm",
     "Waiting times also fell at nearby hospitals that do not use the app"],
    "Strengthen: rule out other explanations",
    "With patient numbers and doctors unchanged, the large fall in waiting time cannot be explained by fewer patients "
    "or more doctors, which supports the app as the cause.",
    ["Claim: app → shorter waits", "Strengthener: the main alternative causes (load, staffing) did not change while "
     "waits fell"],
    "Downloads and the developer's name say nothing about waiting times; falling waits at hospitals without the app "
    "point to some other cause and weaken the claim.", seconds=55)
# ---- Advanced
crq("Advanced", SW_, "Argument: Since the state lowered the speed limit on its expressway from 120 km/h to 100 km/h "
    "last year, the number of fatal accidents on the expressway has fallen by 30%. So the lower speed limit has made "
    "the expressway safer.\n\nWhich of the following, if true, most seriously weakens the argument?",
    "For four months of the year since the limit was lowered, half of the expressway was closed for repairs, and "
    "traffic on it was about half the usual level",
    ["Before the change, most fatal accidents on the expressway involved vehicles driving above 100 km/h",
     "The expressway is about 300 km long and has six lanes",
     "Many drivers complained that the lower limit increases their travel time"],
    "Weaken: an alternative explanation for the drop",
    "Far fewer vehicles on a partly closed road would by itself mean fewer accidents. The 30% fall may then reflect "
    "lower traffic, not the speed limit, so the conclusion is undermined.",
    ["Conclusion: lower limit → fewer fatal accidents", "Alternative: much lower traffic during repairs in the same "
     "period", "The fall could be due to less traffic, not slower traffic"],
    "Speeding being behind most earlier accidents supports the argument; road length is irrelevant; complaints about "
    "travel time do not bear on safety.", seconds=75)
crq("Advanced", INFP, "Passage: Every customer of Bank X who has a credit card also has a savings account. Some "
    "customers who have savings accounts also have fixed deposits. No customer who has a fixed deposit has a home "
    "loan.\n\nWhich of the following must be true about the customers of Bank X?",
    "No customer who has a home loan has a fixed deposit",
    ["Some customers who have credit cards also have fixed deposits",
     "No customer who has a credit card has a home loan",
     "Every customer who has a savings account has a credit card"],
    "Must-be-true: use only the definite statements",
    "'No fixed-deposit holder has a home loan' means the two groups do not overlap, which can be stated from either "
    "side: no home-loan holder has a fixed deposit.",
    ["No FD holder has a home loan ⇔ no home-loan holder has an FD", "Credit-card holders ⊂ savings holders; the "
     "FD overlap is with 'some' savings holders only"],
    "Credit-card holders may or may not have fixed deposits or home loans (only some savings holders have FDs); 'All "
    "credit-card holders have savings accounts' does not reverse.", seconds=70)
crq("Advanced", CA_, "Statement: Inspections have found that several private ambulance operators in the city charge "
    "patients' families far more than the usual rate in emergencies.\n\nWhich of the following is the most "
    "appropriate course of action?",
    "Fix and publish the maximum ambulance charge per kilometre, and penalise operators who charge more",
    ["Ban all private ambulances in the city",
     "Advise families to bargain with the operator before putting the patient in the ambulance",
     "Take no action, since ambulances are needed in emergencies"],
    "A course of action should be practical, proportionate and aimed at the problem",
    "The problem is overcharging. A published price cap with penalties stops it while keeping private ambulances "
    "available.", ["Problem: overcharging in emergencies", "Remedy: a transparent cap plus enforcement",
                   "Keeps the service running"],
    "A total ban would leave patients without ambulances; bargaining in an emergency is impractical; doing nothing "
    "leaves the problem unsolved.", seconds=55)
crq("Advanced", SW_, "Argument: Our branch received 80 customer complaints last quarter and only 20 this quarter. "
    "So our customers are now much more satisfied with our service.\n\nWhich of the following, if true, most "
    "seriously weakens the argument?",
    "This quarter the branch removed its complaint register and stopped accepting written complaints at the counter",
    ["The branch hired two new staff members this quarter",
     "Complaints at other branches of the bank rose this quarter",
     "Most complaints last quarter were about the branch's air-conditioning"],
    "Weaken: attack the assumption that fewer recorded complaints means fewer unhappy customers",
    "The argument assumes that the number of recorded complaints reflects customer satisfaction. If the branch made "
    "complaining harder, the fall in complaints says little about satisfaction.",
    ["Evidence: recorded complaints fell 80 → 20", "Hidden assumption: recorded complaints track satisfaction",
     "Removing the complaint channel breaks that assumption"],
    "New staff could explain better service (it does not weaken); other branches' complaints are irrelevant; the "
    "topic of last quarter's complaints does not affect the comparison.", seconds=70)
crq("Advanced", SW_, "Argument: The city plans to build cycle lanes along its main roads, claiming that this will "
    "reduce car traffic on those roads.\n\nWhich of the following, if true, most strengthens the claim?",
    "On two main roads where cycle lanes were built as a trial, car traffic fell by 18%, while it stayed the same on "
    "similar roads without cycle lanes",
    ["Cycling is a healthy form of exercise", "The price of bicycles in the city has fallen this year",
     "Some shopkeepers on the main roads oppose the cycle lanes"],
    "Strengthen: a controlled comparison",
    "A trial where car traffic fell on roads with lanes but not on similar roads without them is direct evidence that "
    "the lanes reduce car traffic.", ["Claim: cycle lanes → less car traffic",
                                      "Trial vs comparable roads isolates the effect of the lanes"],
    "Health benefits and bicycle prices do not show any effect on car traffic; shopkeepers' opposition is irrelevant "
    "to the claim.", seconds=65)
crq("Advanced", INFP, "Passage: A company has 100 employees, 40 of whom work in Sales. This year, the average salary "
    "of the Sales employees rose by 10%, and the number of Sales employees did not change. The total salary paid to "
    "all 100 employees also rose by exactly 10%, and the number of employees outside Sales did not change "
    "either.\n\nWhich of the following must be true?",
    "The total salary paid to the 60 employees outside Sales rose by exactly 10%",
    ["Every Sales employee received a 10% raise",
     "The average salary outside Sales is the same as the average salary in Sales",
     "No employee of the company had a salary cut this year"],
    "Totals rising by the same percentage force the remainder to rise by that percentage",
    "Let the old totals be T (company) and S (Sales). New totals are 1.1T and 1.1S (same staff, average up 10%). The "
    "rest of the company then gets 1.1T − 1.1S = 1.1(T − S): exactly 10% more than before.",
    ["Sales total: S → 1.1S (40 employees, average +10%)", "Company total: T → 1.1T",
     "Others: 1.1T − 1.1S = 1.1(T − S) ⇒ +10%"],
    "A 10% rise in the average allows uneven individual raises; the two averages need not be equal; individual "
    "salaries could still fall while totals rise.", seconds=80)

# ================================================================================================ WRITE
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_003_plan.json").read_text(encoding="utf-8"))
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
        "batch_id": "BATCH_003",
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
